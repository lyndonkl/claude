# Reference material for `project-investment-analysis`

Long-form backing for `SKILL.md`: the full input reference for every subcommand, the
worked examples the engine is tested against, and the survey tables the guidance leans on.

Source corpus: Damodaran's corporate finance packet (`cfpacket1spr20`), the Netflix Fit
case and presentation (Spring 2020), the acquisitions packet (`valpacket3`), and the
`capbudg.xls` / `returncalculator.xls` model family.

---

## 1. Input reference by subcommand

Every subcommand accepts JSON on stdin or `--in FILE`, and `--example` prints a payload
you can pipe straight back in.

### `npv`

| Field | Required | Meaning |
|---|---|---|
| `cash_flows` | yes, unless `streams` | Year 0 first; year 0 is not discounted |
| `discount_rate` | yes, unless `streams` | A number, or one rate per year after year 0 |
| `terminal` | no | `{cash_flow_next_year, growth_rate, cost_of_capital}` folded into the last year |
| `streams` | alternative | List of `{label, cash_flows, discount_rate, terminal}` |
| `profile_rates` | no | Rates to evaluate NPV at, for the NPV profile; single stream only |

The `terminal` block capitalizes the cash flow of the year *after* the forecast. Give
`cash_flow_next_year` explicitly whenever the last forecast year is still in growth mode.
Omitting it grows the last forecast year by `growth_rate`, which inherits growth-phase
economics into perpetuity — the single most expensive terminal-value error.

### `irr`

| Field | Required | Meaning |
|---|---|---|
| `cash_flows` | yes | The stream |
| `hurdle_rate` | no | Adds `npv_at_hurdle_rate` and a decision |
| `profile_rates` | no | Overrides the default 0%–50% profile grid |

Output fields worth reading: `sign_changes`, `conventional`, `roots`, `irr` (null when
there is not exactly one root), `reliable`, `note`, `npv_profile`.

The search runs from −99% to +1000%, finely below 100% and coarsely above.

### `mirr`

| Field | Required | Meaning |
|---|---|---|
| `cash_flows` | yes | The stream |
| `hurdle_rate` | yes | Default for both rates below, and the accept/reject benchmark |
| `reinvestment_rate` | no | Rate at which inflows compound to the horizon |
| `finance_rate` | no | Rate at which outflows discount back to today |

### `rationing`

| Field | Required | Meaning |
|---|---|---|
| `projects` | yes | Each `{label, cash_flows}` or `{label, npv, initial_investment}` |
| `discount_rate` | if streams given | Default rate; a project may override it |
| `budget` | no | Triggers selection under a capital constraint |

`initial_investment` defaults to the absolute value of year 0. Set it explicitly when the
outlay lands in a later year.

### `different-lives`

| Field | Required | Meaning |
|---|---|---|
| `projects` | yes, at least two | Each `{label, cash_flows}` or `{label, npv, life}` |
| `discount_rate` | yes | One common hurdle rate across the candidates |

Replication needs `cash_flows`. The common horizon is the least common multiple of the
lives, and the engine refuses beyond 200 years rather than pretend a project repeats that
many times.

### `payback`

| Field | Required | Meaning |
|---|---|---|
| `cash_flows` | yes | The stream |
| `discount_rate` | no | Adds discounted payback and `cost_of_time_years` |

Both periods interpolate within the crossing year. A stream that never recovers returns
`null` with an explanation rather than a fabricated year.

### `accounting-return`

| Field | Required | Meaning |
|---|---|---|
| `after_tax_operating_income` | yes, or the pair below | One entry per year, year 1 first |
| `operating_income` + `tax_rate` | alternative | Pre-tax income taxed at the marginal rate |
| `invested_capital` | yes | Beginning-of-year book capital, same length as income |
| `ending_invested_capital` | no | Closing capital for the final year, for the average basis |
| `cost_of_capital` | no | Adds return spread, EVA, and the PV of EVA |

### `incremental`

| Field | Required | Meaning |
|---|---|---|
| `total_cash_flows` | yes | The stream as the accounting system reports it |
| `tax_rate` | yes | Marginal rate for the project, not the effective rate |
| `sunk_investment` | no | Already-spent amount charged at year 0; added back |
| `sunk_asset_depreciation` | no | Annual depreciation on capitalized sunk assets; its tax shield is removed |
| `allocated_overhead_not_incremental` | no | Annual pre-tax allocation; added back after tax |
| `incremental_overhead` | no | Genuinely new overhead; charged after tax |
| `opportunity_cost_after_tax` | no | Already after tax; charged as given |
| `cannibalization` | no | `{lost_contribution_pre_tax, retained_share}` |
| `side_benefit_after_tax` | no | Credited as given |
| `discount_rate` | no | Adds NPV before and after the adjustments |

Per-year fields accept a scalar (applied to years 1 onward), a list of length `n` (years
1..n), or a list of length `n+1` (years 0..n).

### `synergy`

| Field | Required | Meaning |
|---|---|---|
| `mode` | no | `combined` or `cash_flows`; inferred from the keys present |
| `acquirer_standalone_value` | combined mode | Acquirer valued alone at its own rate |
| `target_standalone_value` | combined mode | Target alone, restructured if control value is also claimed |
| `combined_value_with_synergy` | combined mode | The merged business revalued |
| `combined_value_without_synergy` | no | Triggers the sum-of-parts check |
| `cash_flows` | cash-flow mode | After-tax synergy by year, starting at year 1 |
| `discount_rate` | cash-flow mode | The **receiving** business's cost of capital |
| `terminal` | no | Perpetuity closing the synergy schedule |
| `exchange_rate` | no | Synergy-currency units per unit of reporting currency |
| `acquisition` | no | `{target_standalone_value, price}` → ceiling price and verdict |

### `synergy-haircut`

| Field | Required | Meaning |
|---|---|---|
| `components` | yes | Each `{label, kind, value}` with `kind` of `cost` or `revenue` |
| `realization_rate` | no, per component | Defaults to the bundled median band for that kind |
| `customer_attrition_rate` | no, per component | Defaults to 3.5% for revenue, 0% for cost |
| `one_time_cost_to_achieve` | no, per component | Subtracted from the net |
| `competing_bidders` | no | Adds a note on how much synergy survives an auction |
| `table_path` | no | A replacement realization table |

### `control-value`

| Field | Required | Meaning |
|---|---|---|
| `status_quo_value` | yes | Equity value under existing management |
| `restructured_value` | yes | Equity value under the policies you would set (alias `optimal_value`) |
| `probability_of_change` | yes | Odds that management actually changes, as a fraction |
| `shares_outstanding` | no | Unlocks the whole per-share block |
| `status_quo_value_per_share` | no | Per-share values, as an alternative to a share count |
| `restructured_value_per_share` | no | Pairs with the field above |
| `market_price_per_share` | no | Backs out the odds the market is paying for |
| `implementation_delay_years` | no | Years before the changes land; needs `discount_rate` |
| `discount_rate` | with a delay | Rate that discounts the delayed gain |
| `share_classes` | no | `{voting_shares, non_voting_shares}` → the voting premium |

### `deal`

| Field | Required | Meaning |
|---|---|---|
| `target_standalone_value` | yes | The target's status-quo value |
| `restructured_value` | yes | The target under your policies (or give `value_of_control`) |
| `value_of_control` | alternative | The gap, when the restructured value is not to hand |
| `synergy_value` | no | Defaults to zero, which is the honest figure until it is valued |
| `price` | yes | What is being paid for the target |
| `target_discount_rate_used` | yes | Must be `true`: the target was valued at its own rate |
| `synergy_baseline` | with synergy | Must be `restructured_target`, never `status_quo` |
| `discount_rate_used` | no | Cross-checked against the field below |
| `target_cost_of_capital` | no | A gap wider than 5 basis points refuses the run |
| `pre_announcement_market_cap` | no | Gives the premium to justify and the undervaluation pre-check |
| `motive` | no | `undervaluation`, `control` or `synergy` → a verdict on that test |

### `control-premium`

| Field | Required | Meaning |
|---|---|---|
| `status_quo_equity_value` | yes | Equity under existing management |
| `optimal_equity_value` | yes | Equity under a value-maximising owner |
| `majority_pct` | no | Above 0.5; priced off the optimal value |
| `minority_pct` | no | Below 0.5; priced off the status-quo value |
| `rule_of_thumb_premium` | no | Defaults to 0.20, reported only as a comparison |
| `control_premium` | conversion mode | Give this alone to convert to a minority discount |
| `minority_discount` | conversion mode | Give this alone to convert to a control premium |

---

## 2. Worked examples used as test vectors

`selftest` runs 186 checks. These are the corpus figures behind them.

### Netflix Fit (Spring 2020) — the integrated case

Cost of capital 8.01% for the fitness project, 8.93% for Netflix Entertainment. Marginal
tax rate 25%. Inflation 1%.

| Line | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FCFF | −2,500.00 | 132.94 | 200.68 | 272.66 | −171.29 | 459.60 | 944.35 | 442.58 | 484.43 | 528.60 | 1,143.52 |
| Synergy after tax | | 56.25 | 56.81 | 57.38 | 57.95 | 58.53 | 59.12 | 59.71 | 60.31 | 60.91 | 61.52 |
| Incremental income after tax | | −60.00 | 8.14 | 80.55 | 157.36 | 238.68 | 211.59 | 251.70 | 294.03 | 338.70 | 385.83 |
| Invested capital (start) | | 2,450.00 | 2,253.53 | 2,057.26 | 1,861.21 | 2,185.69 | 1,877.66 | 1,629.70 | 1,381.97 | 1,134.47 | 887.23 |

Published results: stand-alone NPV $106.37m, IRR 8.69%. Synergy NPV $376.20m at 8.93%.
Total $482.57m, IRR with synergy 11.17%. Average ROC 10.76% without synergy on the
average-income-over-average-capital convention. On an infinite life with maintenance capex
above depreciation, year-11 steady-state FCFF is $244.33m, terminal value
$244.33 / (0.0801 − 0.01) = $3,486m, stand-alone NPV $365m and total $1,074m.

The stream changes sign three times, because of the $520.30m studio investment in year 4
and the $541.43m deferred-investment credit in year 6. It has one root, so the engine
returns it and marks it unreliable.

Classification decisions the case turns on: $250m of already-expensed fitness R&D is sunk
and excluded. The 4% allocation of firm-wide G&A is excluded. The separate $50m of new
G&A is included. The Mumbai studio is not free.

### Rio Disney

Incremental cash flows, 8.46% cost of capital, terminal value $11,275m at year 10:
−2,000; −1,000; −859; −267; 340; 466; 516; 555; 615; 681; 715 + 11,275. NPV = $3,296m,
IRR 12.60%. Payback 10.3 years, discounted payback 16.8 years.

Adjustment route from total to incremental cash flows, tax rate 36.1%:

| Item | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Cash flow to firm (total) | (2,500) | (982) | (921) | (361) | 198 | 285 | 314 | 332 | 367 | 407 | 434 |
| + Pre-project investment (sunk) | 500 | | | | | | | | | | |
| − Sunk depreciation × 36.1% | | 18 | 18 | 18 | 18 | 18 | 18 | 18 | 18 | 18 | 18 |
| + Non-incremental allocated G&A × (1−t) | | 0 | 80 | 112 | 160 | 200 | 220 | 242 | 266 | 292 | 298 |
| **Incremental cash flow** | **(2,000)** | **(1,000)** | **(860)** | **(267)** | **340** | **467** | **516** | **556** | **615** | **681** | **714** |

Project ROC: average 4.18% on the average-capital basis, 4.11% on the start-of-year basis,
against an 8.46% cost of capital. That reject verdict is unsafe — the parks last far
longer than the ten-year window.

Land opportunity cost: bought for $5m, sellable for $40m, gain taxed at 20%. The charge is
40 − 0.20 × (40 − 5) = **$33m**, not $5m and not $40m.

### Multiple IRRs

| Year | Project 1 | Project 2 |
|---|---|---|
| 0 | −1,000 | −1,000 |
| 1 | 800 | 200 |
| 2 | 1,000 | 300 |
| 3 | 1,300 | 400 |
| 4 | −2,200 | 500 |

Project 1 changes sign twice and has roots at 6.60% and 36.55%; its NPV profile is
hump-shaped, negative at low rates and negative again above 36%. Project 2 is conventional
with a single IRR of 12.83%.

### Scale and timing conflicts, 15% hurdle rate

| | Investment | Cash flows | NPV | IRR | PI |
|---|---|---|---|---|---|
| A (small) | 1,000,000 | 350K, 450K, 600K, 750K | 467,937 | 33.66% | 46.79% |
| B (large) | 10,000,000 | 3.0M, 3.5M, 4.5M, 5.5M | 1,358,664 | 20.88% | 13.59% |
| C (front-loaded) | 10,000,000 | 5.0M, 4.0M, 3.2M, 3.0M | 1,191,712 | 21.41% | 11.92% |

A versus B is the scale conflict: IRR and PI pick A, NPV picks B. B versus C is the timing
conflict at equal scale: IRR picks C, NPV picks B, and the cause is purely the
reinvestment assumption.

### MIRR

Invest 1,000, receive 300, 400, 500, 600 at a 15% hurdle rate. Compounded forward:
300(1.15)³ + 400(1.15)² + 500(1.15) + 600 = 2,160. Ordinary IRR 24.89%; MIRR solves
1,000(1+r)⁴ = 2,160 for **21.23%**. The 3.7-point gap is the reinvestment illusion.

### Unequal lives, 12% hurdle rate

| | Project A | Project B |
|---|---|---|
| Investment | 1,000 | 1,500 |
| Annual cash flow | 400 | 350 |
| Life | 5 years | 10 years |
| NPV | 442 | 478 |
| IRR | 28.7% | 19.4% |
| PV annuity factor | 3.6048 | 5.6502 |
| Equivalent annuity | 122.6 | 84.6 |
| Replicated NPV over 10 years | 693 | 478 |

Raw NPV picks B. Both repairs pick A, and so does IRR.

### Bookscape

The online venture: −1,150,000; 340,000; 415,000; 446,500; 720,730 at 18.12% gives NPV
$76,375. Side costs of $34,352 (the manager's incremental salary) and $1,610 (relocating
financial records) bring the adjusted NPV to $40,413. It survives.

The café: stand-alone NPV −$87,571 at 10.30%. It raises bookstore revenues by $500,000 in
year 1 growing 10% for four more years, at a 10% pre-tax margin taxed at 40%, so after-tax
synergy runs 30,000 / 33,000 / 36,300 / 39,930 / 43,923. PV of synergy = **$135,268**.
Total NPV +$47,697. A good investment, but only as an attachment to the bookstore.

### Tata Motors / Harman International

Harman stand-alone: normalizing the one-off working-capital spike moves 2014 FCFF from
−$94.64m to +$166.85m. At a 9.67% cost of capital and 2.75% stable growth, operating
assets are worth 166.85 / (0.0967 − 0.0275) = $2,476m; equity is 2,476 + 515 cash − 313
debt = **$2,678m**.

Synergy: Tata fits Harman audio as an optional upgrade on Indian cars, taking three years
to adapt the products. From year 4, Rs 10bn of after-tax operating income growing 4% in
perpetuity, at a 13.63% rupee cost of capital built from Tata's beta and India's country
risk premium. Value at end of year 3 = 10,000 / (0.1363 − 0.04) = Rs 103,814m; today
Rs 70,753m; at Rs 60/$ = **$1,179m**.

Ceiling price = 2,678 + 1,179 = **$3,857m** against a market price of $5,248m. Even
crediting the synergy in full the deal destroys about $1.4bn. Walk away.

### Combined-firm synergy

P&G / Gillette, equity values in $m:

| | P&G | Gillette | Combined, no synergy | Combined, synergy |
|---|---|---|---|---|
| Value of equity | 221,292 | 59,878 | 281,170 | 298,355 |

221,292 + 59,878 = 281,170 exactly, so the sum-of-parts check passes. Synergy =
298,355 − 281,170 = **$17,185m**, from $250m of annual cost savings and growth lifted from
11.58% to 12.50%.

AB InBev / SABMiller, operating assets in $m: 211,953 + 50,065 = 262,018 without synergy,
276,610 with. Synergy = **$14,592m**. The cost of capital is 7.51% in both combined
columns — the synergy runs through operations, not financing.

### Blockbuster, July 2005 — the value of control

| | Value of equity | Value per share |
|---|---|---|
| Status quo | $955m | $5.13 |
| Optimally managed | $2,323m | $12.47 |

186.3m shares. The gain from change is $7.34 a share. A control buyer can force the
change, so its ceiling is $12.47 and the maximum premium at the $9.50 price is $2.97.

| Date | Price | Implied probability |
|---|---|---|
| Before Carl Icahn's challenge | $8.20 | 41.8% |
| May 2005, after the challenge | $9.50 | 59.5% |

The lever here was margin, not reinvestment: after-tax operating income rises from 163 to
249, lifting ROC from 4.06% to 6.20% on the same $43m of reinvestment.

### Embraer — the voting premium

Status quo equity R$12,500m, optimal R$14,700m, 242.5m voting and 476.7m non-voting
shares, 20% probability of change. Every share owns the same cash flows, so the status quo
spreads over all 719.2m: R$17.38 a share. The expected control value is 0.20 × 2,200 =
R$440m, and it attaches to the voting shares alone: +R$1.81, giving R$19.19 and a **10.4%
premium**. At 50% odds the premium is 26%.

### AB InBev / SABMiller — the acid test

$ billions.

| Number | Value |
|---|---|
| Acquisition price | 104.0 |
| Status-quo value of SABMiller equity | 51.5 |
| Restructured value | 56.2 |
| Value of control | 4.7 |
| Value of synergy | 14.6 |
| Restructured + synergy | 70.8 |

Market capitalization was $75B the day the intent was announced, so the premium to justify
is $29B. All three tests fail, the widest by $33.2B. The premium is 272% of the combined
gains, which means the seller takes every dollar the deal creates and the buyer's
shareholders fund the difference.

### Minority discounts and stakes

`minoritydiscount.xls` default case: optimal 14,700, status quo 12,500. Minority discount
= 2,200 / 14,700 = **14.97%**; control premium = 2,200 / 12,500 = **17.6%**. A 51% stake is
0.51 × 14,700 = 7,497; a 49% stake is 0.49 × 12,500 = 6,125.

The shipped sheet stores `optimal + minority% × status quo` = 20,825 for the minority
stake, which is more than the whole firm. That is a spreadsheet bug, and the engine reports
it by name so nobody reconciles to it.

Kristin Kandy: $1.6m under existing management, $2.0m under better management. 51% is worth
$1,020,000 and 49% is worth $784,000 — two points of ownership worth $236,000.

The stylized target (revenues 100, after-tax operating income 12, cost of equity 20%) is
worth 60 as run. Lift the pre-tax margin from 20% to 30% and it is worth 90, a **50%**
premium. The rule of thumb would have paid 72. A target already run that way is worth 60
either way, and the premium is zero.

### Firm-level ROC and EVA

| Company | EBIT(1−t) | BV capital | ROC | Cost of capital | Spread |
|---|---|---|---|---|---|
| Disney | 6,920 | 54,899 | 12.61% | 7.81% | +4.80% |
| Vale | 12,432 | 119,402 | 10.41% | 8.20% | +2.22% |
| Baidu (¥) | 9,111 | 30,320 | 30.05% | 12.42% | +17.63% |
| Tata Motors (₹) | 120,905 | 575,983 | 20.99% | 11.44% | +9.55% |
| Bookscape | 1,775 | 19,136 | 9.28% | 10.30% | −1.02% |

Book capital is book debt plus book equity minus cash. Disney's EVA is 0.0480 × 54,899 =
$2,632m, which is identically 6,920 − 0.0781 × 54,899.

Globally, 52% of non-financial firms earn less than their cost of capital, 15% roughly
match it, and 33% beat it (January 2020).

---

## 3. Survey tables

Primary capital budgeting rule used by firms, share of firms:

| Decision rule | 1976 | 1986 | 1998 |
|---|---|---|---|
| IRR | 53.6% | 49.0% | 42.0% |
| Accounting return | 25.0% | 8.0% | 7.0% |
| NPV | 9.8% | 21.0% | 34.0% |
| Payback period | 8.9% | 19.0% | 14.0% |
| Profitability index | 2.7% | 3.0% | 3.0% |

Rule selection by circumstance:

| Firm circumstance | More defensible rule |
|---|---|
| Limited capital access, a stream of surplus-value projects, uncertain cash flows | IRR |
| Substantial funds, good capital access, few surplus projects, certain cash flows | NPV |
| Genuine capital rationing | Profitability index |
| Non-conventional cash flows | NPV only |

Sources of capital rationing:

| Cause | % of firms |
|---|---|
| Limit placed on borrowing by internal management | 69.1% |
| Maintenance of a target EPS or PE ratio | 14.9% |
| Debt limit imposed by an outside agreement | 10.7% |
| Debt limit placed by management external to the firm | 3.2% |
| Restrictive policy on retained earnings | 2.1% |

Rationing is overwhelmingly self-imposed. Treating it as immovable is a choice.

Post-merger synergy realization is in
[`data/synergy_realization.json`](data/synergy_realization.json) with its `as_of` date and
refresh note.

---

## 4. Uncertainty, options and post-mortems

The engine covers the deterministic decision measures. Three things sit beside them.

**Sensitivity and break-evens.** Vary the drivers the answer could plausibly turn on, one
at a time, and find the level at which NPV crosses zero. That break-even is the number a
manager can monitor. On the Vale mine it is an iron ore price near $90 a ton; on Netflix
Fit it is the subscriber renewal rate, which the base case sets near 100%. Re-run `npv`
across a grid of streams to build the table.

**Simulation.** Replace point estimates with distributions and read the output for two
things: whether the mean sits near the base case, and how bad the downside gets. Rio
Disney simulates to a mean NPV of $3.40bn against a $3.29bn base case, with a 12% chance
of a negative NPV. That 12% is not a rejection reason on its own — the discount rate
already charges for risk, and counting it twice rejects good projects.

**Options.** A project can buy the right to delay, to expand later, or to abandon. Those
are a call, a call and a put respectively, and a static DCF prices none of them. When a
marginal or negative NPV project carries real flexibility, value the option with
`option-valuation-toolkit` and add it explicitly rather than arguing the cash flows upward.

**Post-mortems.** For investments already made, re-forecast from today and work the ladder:
continue, divest, terminate, liquidate. Sunk costs are as irrelevant here as they were at
the start.

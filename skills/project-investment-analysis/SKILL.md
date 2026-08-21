---
name: project-investment-analysis
description: Evaluates a discrete investment, project or acquisition from its cash flow stream — NPV, IRR with every root reported when the stream has more than one, MIRR, profitability index and project selection under a capital budget, equivalent annuities and replication for unequal lives, payback and discounted payback, project return on capital and EVA, synergy value with the ceiling price it supports, the value of control and its expected value, the four-number acid test for a deal, and control premiums and minority discounts. Use when deciding whether to take a project, ranking competing projects, comparing projects with different lives, sizing a capital budget, testing whether a stream is truly incremental, valuing synergy or control, pricing a majority or minority stake, or setting the maximum price for an acquisition.
---

# Project and acquisition investment analysis

A project decision is one arithmetic question wrapped in two judgments. The judgments are
what belongs in the cash flow stream and what rate discounts it. The arithmetic is here.

The engine will not decide what is incremental for you, and it will not hide an awkward
answer. A stream with two internal rates of return comes back with both roots and a note
saying the IRR rule does not apply, rather than one root dressed up as the return.

## The script

`resources/project.py` — pure standard library, no installation needed. JSON on stdin (or
`--in FILE`), JSON out.

```bash
python3 resources/project.py <subcommand> --example      # show the input shape
python3 resources/project.py <subcommand> --in payload.json
python3 resources/project.py selftest                    # verify the engine
```

| Subcommand | Turns this | Into this |
|---|---|---|
| `npv` | one or more cash flow streams, each with its own rate | present values by year, NPV per stream, total, NPV profile |
| `irr` | a cash flow stream | every root in the searched range, sign-change count, NPV profile |
| `mirr` | a stream plus a reinvestment rate | modified IRR and the size of the reinvestment illusion |
| `rationing` | competing projects, optionally a budget | profitability index, both rankings, the best affordable set |
| `different-lives` | mutually exclusive projects of unequal life | equivalent annuities and replicated NPVs |
| `payback` | a stream and a rate | payback, discounted payback, and the cost of time between them |
| `accounting-return` | after-tax operating income and book capital by year | ROC on three conventions, return spread, EVA |
| `incremental` | a total cash flow stream and what is not incremental in it | the incremental stream, with every adjustment shown |
| `synergy` | combined-firm values, or a synergy cash flow schedule | synergy value and the maximum acquisition price |
| `synergy-haircut` | a split of cost and revenue synergies | what post-merger evidence says will actually arrive |
| `control-value` | a status-quo value, a restructured value, the odds of change | the value of control, its expected value, and the per-share effect |
| `deal` | the four numbers of an acquisition | the acid test by motive, the ceiling price, and who keeps the gains |
| `control-premium` | two valuations and a stake size | control premium, minority discount, and what each stake is worth |

Cash flow convention throughout: `cash_flows[0]` is the year-0 outlay and is not
discounted; `cash_flows[t]` lands at the end of year t.

## Build the stream before you run anything

Every number below is only as good as the stream feeding it. Work through this first.

```
Incremental cash flow checklist:
- [ ] Write the counterfactual: what the firm's cash flows look like without the project
- [ ] Exclude sunk costs, and the depreciation tax shield on any capitalized sunk asset
- [ ] Exclude allocated fixed overhead; include genuinely new overhead the project causes
- [ ] Charge the opportunity cost of every resource the firm already owns
- [ ] Charge cannibalization of existing products, at the share that would have been kept
- [ ] Credit side benefits, valued at the receiving business's rate
- [ ] Close the stream with salvage, working-capital recovery, or a terminal value
```

**Sunk costs are out.** Money already spent and unrecoverable does not change with the
decision. So does its depreciation tax shield: that shield exists whether or not the
project goes ahead, so leaving it in quietly keeps part of the sunk cost in the analysis.
The behavioural research says managers find this nearly impossible to do. The rule is
easy; the discipline is not.

**Allocated fixed overhead is out; incremental overhead is in.** A share of a central G&A
pool charged to the project on a sales basis is not caused by the project. New headcount
and new systems are. Split the pool empirically by regressing company G&A on company
revenues: the slope is the variable rate you charge, the intercept is the fixed pool you
do not. Treating the whole allocation as non-incremental is the opposite error and just as
wrong.

**Opportunity cost is in, priced at the best alternative use.** Never at zero because the
firm already owns the asset, and never at book value.

| Alternative use | What to charge |
|---|---|
| Sell it | Sale proceeds net of capital gains tax |
| Rent or lease it out | Present value of the after-tax rents foregone |
| Use it elsewhere in the business | Cost of replacing it |
| No alternative use, now or later | Zero — but verify the "or later" |

Excess capacity is the case that looks free and is not. "Already paid for and nobody else
wants it" is a sunk-cost argument in a different hat. Ask when capacity runs out without
the project, when it runs out with it, and what the firm does then. If the answer is
"build earlier", charge the present value of building earlier less the present value of
building later. If the answer is "cut production", charge the after-tax cash flow on the
lost sales.

**Cannibalization is in, at the share that would have been kept.** For an exclusive
differentiated product, diverted sales were not going anywhere else, so count all of them.
In a fiercely competitive market those customers might have left for a rival regardless,
so count only the share you would truly have retained.

**Side benefits are in, at the receiving business's rate.** See "Synergy" below.

The `incremental` subcommand runs the adjustment route: start from cash flows as the
accounting system reports them and back out what the firm would have spent anyway.

```bash
python3 resources/project.py incremental --example | python3 resources/project.py incremental
```

Building the stream directly from incremental revenue and cost lines is the other route.
The two must reconcile up to rounding. Do not mix them inside one model, or the
adjustments get counted twice.

## Choosing the rate

Match the rate to the cash flows on four dimensions: claimholder, business, geography and
currency. Cash flows to the firm discount at the cost of capital; cash flows to equity
discount at the cost of equity. A project in a different business from the parent takes
that business's risk, not the parent's. Build the rate with `cost-of-capital-toolkit`
(`wacc` subcommand, read `cost_of_capital`) and pass the number in here.

Never blend rates across streams that carry different risk. The `npv` subcommand takes a
`streams` list precisely so a project and its synergy can each carry their own rate and
still produce one total.

## NPV and IRR

```bash
echo '{"cash_flows": [-2000, -1000, -859, -267, 340, 466, 516, 555, 615, 681, 11990],
       "discount_rate": 0.0846, "profile_rates": [0.08, 0.12, 0.16, 0.20]}' \
  | python3 resources/project.py npv
```

NPV is the expected increase in firm value from taking the project. Report it as a dollar
statement, not a sign. A positive NPV that is thin relative to the investment is a thin
recommendation: the Netflix Fit case clears its hurdle by $106 million on a $2.4 billion
outlay, and small assumption changes flip it.

`irr` solves for the rate that drives NPV to zero, by scanning the whole plausible rate
domain for sign changes in NPV and bisecting each bracket it finds. Three outcomes:

- **One root, one sign change.** `irr` is the answer and `reliable` is true.
- **More than one root.** `irr` is null, `roots` lists them all, and the note tells you to
  decide on NPV at the actual cost of capital. This happens when the stream changes sign
  more than once — decommissioning, cleanup, restoration, or a mid-life capacity
  investment.
- **No root.** The stream never crosses zero. Usually the year-0 outlay is missing or has
  the wrong sign.

Read `sign_changes` even when a single root came back. A stream can change sign three
times and still have one root in the searched range; the rate is then descriptive rather
than a decision rule, and the engine marks it `reliable: false`.

Set `hurdle_rate` and the output carries a decision, falling back to NPV automatically
when the IRR rule does not apply.

## Ranking projects against each other

Independent projects are the exception. When candidates compete, NPV and IRR can disagree
for three reasons, and each has its own remedy.

| Conflict | What causes it | What to do |
|---|---|---|
| Multiple IRRs | More than one sign change in the stream | NPV only |
| Scale | NPV is dollars, IRR is a percentage | NPV, unless capital is rationed |
| Timing at equal scale | The reinvestment assumption | Compute `mirr`, then decide on NPV |
| Unequal lives | Longer projects accumulate more NPV | `different-lives` |

**MIRR** replaces the IRR's assumption that intermediate cash flows are reinvested at the
IRR itself. Outflows come back to today at the financing rate, inflows go forward to the
horizon at the reinvestment rate, and the gap between IRR and MIRR is the size of the
illusion. Both rates default to the hurdle rate, which is the standard treatment.

**Profitability index** is `NPV / initial investment` — value created per dollar of scarce
capital. The output also carries `pv_index_including_investment`, which is the same number
plus one, because both conventions are in circulation.

```bash
python3 resources/project.py rationing --in projects.json
```

Use the index only when capital is genuinely rationed. Applying it otherwise biases the
firm toward small projects and leaves value on the table. And check whether the constraint
is real: surveys put roughly 70% of capital rationing down to borrowing limits set by the
firm's own management, which is a policy, not a law of nature.

Give a `budget` and the engine also reports `best_selection`, the highest-NPV affordable
set found by exhaustive search when there are 16 projects or fewer. Projects are
indivisible, so taking them in index order can leave money idle; when it does, the output
sets `greedy_is_suboptimal` and quantifies the gap.

## Projects with different lives

Raw NPVs are not comparable across different lives. The longer project accumulates value
over more years and ties up capital for longer, and the comparison rewards it for both.

```bash
python3 resources/project.py different-lives --example \
  | python3 resources/project.py different-lives
```

The engine reports both repairs. **Equivalent annuity** divides each NPV by the annuity
factor over that project's own life, giving a level annual value. **Replication** repeats
each stream to the common multiple of the lives and discounts the whole thing; the
reinvestment at the start of a new cycle nets against the last receipt of the previous
one. The two should rank the projects identically, and `routes_agree` says whether they
did. They can part company when annual cash flows are irregular, in which case trust
replication.

Before using either, ask whether repetition is realistic. A one-off licence, a unique site
or a first-mover position cannot be repeated on the same terms, and then neither repair
applies. IRR needs no life adjustment at all, since it is a rate rather than a total.

## Payback

`payback` reports both the simple and the discounted period, interpolated within the
crossing year, and the gap between them as `cost_of_time_years`. That gap is often large:
Rio Disney pays back in 10.3 years undiscounted and 16.8 years discounted.

Payback describes how long capital is at risk. It ignores every cash flow after the
payback date, and in its simple form ignores the time value of money entirely. Use it as a
supplementary read, never as the decision rule.

## Accounting return and EVA

```bash
python3 resources/project.py accounting-return --in project-books.json
```

Feed after-tax operating income by year and beginning-of-year book capital by year, plus
the cost of capital. Book capital for a project is undepreciated fixed assets plus the
book value of non-cash working capital; for a firm it is book debt plus book equity minus
cash, taken from the previous year's balance sheet.

The output carries three averages, because the corpus itself uses two of them and they can
differ by several points:

- `average_roc_start_of_year_basis` — mean of the annual ratios, income over opening capital
- `average_roc_average_capital_basis` — mean of the annual ratios, income over average capital
- `roc_on_average_income_and_capital` — average income over average capital

On Netflix Fit those give 14.25% and 10.76% on the same numbers. Name the convention when
you quote the figure.

EVA converts the spread into dollars: `EVA = (ROC − cost of capital) × capital`, which is
identically the income left after every dollar of capital is charged its cost. The output
also discounts the EVA stream, which should track NPV when the book capital roll-forward
is consistent with the cash flows.

Read the level, not the trend. Book returns climb mechanically as the asset base
depreciates even when nothing improves — Netflix Fit's ROIC runs from −2.91% in year 1 to
44.06% in year 10 on an unchanging asset. And averaging over a truncated window on a
long-lived project loads the early losses in and leaves the mature years out. Rio Disney's
4.18% average ROC over ten years says reject; the perpetual-life DCF says +$3.3 billion.

## Synergy

A project can make the firm's other businesses more valuable. That benefit is real and it
is routinely abused, invoked qualitatively late in the process to override a negative NPV.
The discipline is to value it explicitly, in the original analysis, at the cost of capital
of the business that **receives** it.

Two routes, both in the `synergy` subcommand.

**Cash flow route** — for a project side benefit or a synergy you can schedule:

```bash
echo '{"mode": "cash_flows", "receiving_business": "Netflix Entertainment",
       "cash_flows": [56.25, 56.81, 57.38, 57.95, 58.53, 59.12, 59.71, 60.31, 60.91, 61.52],
       "discount_rate": 0.0893}' \
  | python3 resources/project.py synergy
```

`cash_flows` starts at year 1. Put zeros in front for the lag before the benefit arrives —
synergies that "start immediately" are almost always wrong. Add a `terminal` block with
`cash_flow_next_year` and `growth_rate` for a synergy that continues in perpetuity, and an
`exchange_rate` when the synergy is earned in another currency.

**Combined-firm route** — the definition, for a merger:

    synergy = value of the combined firm with synergy − (acquirer alone + target alone)

Pass `combined_value_without_synergy` as well and the engine runs the sum-of-parts check.
That value must equal the sum of the two stand-alone values exactly, because merely adding
two firms together creates nothing. A difference means an inconsistent assumption reached
the combined-firm model. Use the target's **restructured** value in the baseline when the
deal also claims control value, or the restructuring gains get counted twice.

Force every claimed synergy onto a valuation input before you value it. Higher returns on
new investment or more new investment raise growth. Cost savings raise the operating
margin. A more durable advantage lengthens the growth period. Tax benefits lower the
effective rate. Added debt capacity raises the debt ratio. If a claim moves none of these,
it is a buzz word. Diversification is not a synergy for a public firm, whose investors
diversify more cheaply on their own account.

Report the stand-alone number next to the combined one, always. Netflix Fit is $106
million alone and $483 million with synergy, and the whole recommendation turns on that
gap.

## The value of control

Control is worth the gap between the firm as it is run and the firm as it could be run.
Nothing else. Value the target twice, once under existing management and once under the
policies you would set, and subtract. Both valuations are full DCFs and belong in
`dcf-valuation-engine`. `control-value` does the arithmetic that follows.

```bash
echo '{"status_quo_value": 955, "restructured_value": 2323, "shares_outstanding": 186.3,
       "probability_of_change": 0.595, "market_price_per_share": 9.50}' \
  | python3 resources/project.py control-value
```

A gap is only worth having if someone can close it, so the second input is the odds that
management actually changes.

    expected value of control = probability of change × (restructured − status quo)

That one product explains four things at once. It sets what a hostile bidder can pay. It
puts a market price between the two values. It makes a voting share worth more than a
non-voting one. And it is the part a minority stake does not get.

A buyer who takes control can force the change, so its probability is 1 and its ceiling is
the whole restructured value. Blockbuster in 2005 was worth $5.13 a share as run and
$12.47 a share run well. At the $9.50 market price the most a bidder could justify was a
$2.97 premium, and paying all of it would have handed the entire improvement plan to the
seller.

Pass `market_price_per_share` and the engine inverts the identity to show the odds the
market is already paying for. Blockbuster traded at $8.20 before Carl Icahn's challenge
and $9.50 after, which reads as 41.8% and 59.5%. That 18-point move is the value of
activism, measured directly. Read a figure above 100% as a broken input rather than as
near certainty; the restructured value is usually the input at fault.

Two adjustments matter. Changes that take years arrive late, so pass
`implementation_delay_years` with a `discount_rate` and quote
`adjusted_value_of_control`. And where a firm has voting and non-voting shares, pass a
`share_classes` block. Every share owns the same cash flows, so the status quo spreads
across all of them and only the expected control value attaches to the voting class.
Embraer's voting shares carry a 10.4% premium at 20% odds and a 26% premium at 50%.

### Control premiums and minority discounts

`control-premium` turns the same gap into the two ratios deal practice quotes, and
converts between them.

    control premium   = (optimal − status quo) / status quo
    minority discount = (optimal − status quo) / optimal
    minority discount = control premium / (1 + control premium)

One gap, two denominators. A controlling stake is priced off the optimal value because it
can make the changes. A minority stake is priced off the status quo because it cannot. At
Kristin Kandy a 51% stake is worth $1.02 million and a 49% stake $784,000. Two points of
ownership are worth $236,000, and all of it is control.

The flat 20% control premium in circulation is not analysis. It is a survey average of
other people's deals, and averages of overpayments are still overpayments. A well-run
target carries a premium of zero however highly it is regarded. If you cannot name the
change, price it and defend it, there is nothing to pay for.

## Acquisitions are projects

Every rule above applies to a deal. The two mechanical ways to overpay are discounting the
target's cash flows at the acquirer's rate, and building the acquirer's cheap debt into
the target's cost of capital. A risky business does not become safe because a safe buyer
owns it. If lowering the discount rate is what makes the deal work, the deal does not
work.

    maximum price = target's stand-alone value + value of synergy

Pass an `acquisition` block to `synergy` and the engine computes that ceiling, the premium
over stand-alone value, and how much synergy is left for the acquirer at a given price.

```bash
python3 resources/project.py synergy --in deal.json
```

The ceiling is a walk-away point, not a target. Paying the full synergy value as a premium
hands the entire gain to the seller and leaves the acquirer with exactly nothing, which
the output shows as `synergy_retained_by_acquirer: 0`. Read
`synergy_required_to_justify_price` before bidding: on Tata Motors and Harman the market
price demanded about $2.75 billion of synergy and the credible figure was $1.18 billion.

### The acid test

There are three value-based reasons to buy a company, and each has its own benchmark.
`deal` takes the four numbers and runs all three at once.

| Motive | The deal makes sense only if |
|---|---|
| Undervaluation | price < status-quo value |
| Control | price < restructured value |
| Synergy | price < restructured value + synergy value |

```bash
python3 resources/project.py deal --example | python3 resources/project.py deal
```

The output splits the gains. The seller takes the premium over stand-alone value, the
acquirer keeps whatever is left under the ceiling, and `premium_share_of_combined_gains`
says which way the split went. AB InBev paid $104 billion for SABMiller against a ceiling
of $70.8 billion, so the premium came to 272% of every gain the deal could create.

`deal` refuses to run in two cases, both of them ways of reaching a price rather than a
value. It needs `target_discount_rate_used: true` to confirm the target was discounted at
its own cost of capital. And when synergy is claimed it needs
`synergy_baseline: "restructured_target"`, because baselining synergy on the status quo
puts the control gains inside the synergy figure and lets the deal claim them twice.

When all three tests fail, exactly two explanations remain: the synergy is underestimated,
or the buyer is overpaying. Pick one and say which.

`synergy-haircut` applies the post-merger evidence to a synergy schedule. Split the
schedule into cost and revenue components first — a single blended number hides that the
fragile half is the revenue half. Cost synergies land most of the time; roughly 70% of
mergers miss their expected revenue synergies. Revenue components also take a customer
attrition haircut for losses during integration.

Before trusting any synergy number, test it for concreteness. Can you name the plant, the
contract, the headcount and the month? Is a named person accountable for delivering it?
Are you one of several bidders, in which case competition bids the synergy into the price?

Two side notes on deal arithmetic. Goodwill is the acquisition price less the target's
adjusted book equity, which makes it the acquirer's own public estimate of the value it
must now create rather than an asset. And the base year has to be normalized before
anything is projected: on Harman, fixing a one-off working-capital spike alone moves free
cash flow from −$95 million to +$167 million.

## Working with the other engines

| You need | Run | Read |
|---|---|---|
| The project's cost of capital | `cost-of-capital-toolkit` → `wacc` | `cost_of_capital` |
| A bottom-up beta for a project in another business | `cost-of-capital-toolkit` → `beta` | `levered_beta` |
| The target's stand-alone value for an acquisition | `dcf-valuation-engine` → `value` | `equity_value` or `value_of_operating_assets` |
| Lease-adjusted operating income and invested capital | `financial-statement-normalization` | `adjusted_operating_income`, `invested_capital` |
| The value of an option to delay, expand or abandon | `option-valuation-toolkit` | option value |
| A cross-check across the whole artifact set | `valuation-consistency-checks` → `validate` | findings |

A negative NPV is not always a rejection. A project that buys the right to delay, to
expand later, or to abandon carries option value that a static DCF does not price. Value
it with `option-valuation-toolkit` and add it, rather than arguing the cash flows upward.

## Reference material

- [resources/reference.md](resources/reference.md) — the corpus worked examples used as
  test vectors, the decision-rule usage and capital-rationing surveys, side-cost pricing
  rules, and the full input reference for each subcommand.
- `resources/data/synergy_realization.json` — the McKinsey post-merger realization bands
  that drive `synergy-haircut`, tagged with an `as_of` date and a refresh note. Pass a
  replacement with `table_path` rather than editing the bundled copy.

## Common failures

| Symptom | Cause |
|---|---|
| IRR comes back null with a list of roots | The stream changes sign more than once; decide on NPV at the cost of capital |
| IRR looks implausibly high on a long project | The reinvestment assumption; run `mirr` to see the corrected figure |
| A large project loses to a small one | Ranked by IRR or profitability index when capital is not actually rationed |
| The longer-lived project always wins | Raw NPVs compared across unequal lives; run `different-lives` |
| Project ROC rises every year on a flat business | Book capital shrinking through depreciation, not improving performance |
| Average ROC says reject, NPV says accept | Accounting return averaged over a window shorter than the project's real life |
| A marginal project turns comfortable | Synergy folded into the total; report the stand-alone number beside it |
| Synergy value looks large and safe | Discounted at the project's or acquirer's rate instead of the receiving business's |
| Sum-of-parts check fails | An inconsistent assumption in the combined-firm model; the parts must add exactly |
| The deal only works at a lower discount rate | Risk transference or a debt subsidy; the deal does not work |
| Acquisition NPV positive but nothing left over | Paying the full synergy as premium hands the gain to the seller |
| A positive-NPV project keeps getting killed | Fixed allocated overhead charged to it; strip it with `incremental` |
| `deal` refuses to run | The target was valued at somebody else's rate, or the synergy was baselined on the status quo |
| Control value and synergy together look huge | The synergy baseline is the status-quo target, so the control gains are counted twice |
| The implied probability of change exceeds 100% | The restructured value is too low, or the market prices something outside your model |
| A premium is defended by a 20% rule of thumb | Nobody named the change; run `control-premium` and read the gap between the two valuations |

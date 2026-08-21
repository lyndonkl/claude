# Combination rules and worked routings

Real companies sit in several buckets at once. Boeing in March 2020 was mature, cyclical
and distressed. Tata Steel is emerging-market, cyclical and cross-holding-heavy. A
distressed emerging-market bank needs three sets of repairs, not one.

The S8 rules in the main skill make composition deterministic. This file carries the
exclusion detail, the composition arithmetic, the seven standard multi-branch shapes, and
routed real companies.

## Exclusion pairs in detail

A violation here is a hard error. The critic fails the run rather than warning.

**B7 normalize against B1 revenue-driven.** Normalization is legitimate only when the
trouble is temporary. Structural, life-cycle or leverage-driven losses route to B1 or B4.
Never both. The test is in `earnings_status`: `negative-transient` goes to B7,
`negative-structural` goes to B1.

**B7 normalize against a separate recovery assumption.** Normalized earnings *are* the
recovery. Assume a recovery in growth and margins on top and you have counted it twice. If
recovery takes time, ramp toward the normalized level. Do not add a second recovery.

**B5 against FCFF, WACC and enterprise value.** A financial service firm never gets a
firm-level valuation. There is no meaningful cost of capital when debt is raw material.
This also rules out EV/EBITDA, EV/Sales and EV/IC in the pricing route.

**Total beta against a diversified buyer.** One buyer identity per valuation. B13-I uses a
total beta because the buyer holds one asset. B13-II, B13-III and B14 use a market beta
because the buyer's investors are diversified.

**Illiquidity discount against a public buyer or an IPO.** The buyer's investors already
have a market to sell into.

**B12 option value against the same upside inside DCF growth.** Route each claim to exactly
one device. If the patent is valued as an option, its revenue comes out of the DCF.

**A higher discount rate for failure against B4 probability weighting.** Pick one channel.
The probability weight is the correct one, because failure is not a marginal, diversifiable
risk that a beta prices.

## Composition arithmetic

Probability-weighted branches compose multiplicatively on the going-concern value. Each
risk appears exactly once.

```
V = V_going_concern × Π_i (1 − p_i × loss_fraction_i) + Σ_i p_i × proceeds_i
```

Two practical limits. Never stack more than two probability weights without arguing that
the events are genuinely distinct — failure and regime change can be, failure and "business
risk" cannot. And a country risk premium in the cost of equity, plus a nationalization
scenario, plus a governance discount is three charges for one overlapping risk.

Probability hygiene. Every probability sits in `[0, 1]`. State whether it is annual or
cumulative, and convert with `P_n = 1 − (1−p)^n` when the model needs the cumulative one.
An implied `P(change)` at or outside `[0, 1]` means one of the two underlying valuations is
wrong, not that you found an arbitrage.

## The seven standard shapes

| Company shape | Route |
|---|---|
| Distressed emerging-market bank | Engine **B5**, using FCFE to regulatory capital rather than dividends, because payout is not capacity in a crisis. Rate stack from **B9**: local-currency riskfree built from the inflation differential, exposure-weighted ERP. Outer adjustment: probability of **equity wipeout**, not liquidation. Constraints `no-fcff-valuation`, `no-optimal-debt-ratio`. |
| Cyclical and distressed — a mature industrial in a shock | **B7** to normalize the base, then **B4** failure weighting on top. Do not normalize *and* assume the cycle recovers in the forecast. Cross-check with **B12** equity-as-call when `D/(D+E) > 50%`. |
| Young, intangible-heavy and private | **S3** capitalizes R&D first, because it changes invested capital and the sales-to-capital ratio. Then the **B1** engine, then **B13** for the rate identity and the discount stack, then **B4** with a failure probability from the sector survival table. |
| Commodity, emerging market, cross-holdings | **B6** engine at today's price. **B9** rate stack. **B11** bridge. Report the value as "worth X at today's commodity price" and state the macro view separately. |
| Multi-business with one financial division | **B10** decomposition. The financial division is valued by **B5** on equity and added as an equity-value block. Every other division is valued on enterprise value. Never blend a bank into a consolidated FCFF. |
| Mature, poorly governed, emerging market | **B2** status quo against optimal, using both return levers — new investments and existing assets. **B9** rate stack. `P(change)` from ownership, voting and activist evidence. Do not add a governance discount. |
| Declining with heavy cross-holdings | **B3** engine on the operating business. **B11** for the stakes. Note that holdings often exist to preserve control and will not be sold. |

## Ordering, restated

When several branches fire, the pipeline order is fixed. Each step consumes the previous
one's output.

1. **Clean accounts.** S3: leases, R&D through B8, one-times, owner salary.
2. **Fix base earnings.** B7 normalizes, or B1 abandons earnings and drives from revenue.
   Never both.
3. **Build the rate stack.** Bottom-up beta first. Then a total beta if B13-I. Then an
   exposure-weighted ERP or lambda if B9. Then a synthetic rating including the country
   spread if B9. Then divisional rates if B10.
4. **Run the engine.** One engine, per the R1 precedence list. Once per division if B10.
5. **Outer adjustments.** B4 failure weighting, B9 truncation weighting, B2 `P(change)`
   weighting. Multiplicative, and each applied exactly once.
6. **Equity bridge.** Debt including leases, minorities at market value, cash, B11
   cross-holdings, employee options valued as options.
7. **Discount stack.** B13 illiquidity, then minority. Key-person is already inside EBIT.
8. **Uncertainty.** Scenario grid, then simulation.
9. **Price comparison.** Gap, catalyst, expected return.

Two ordering traps. Capitalizing R&D after the rate stack leaves the coverage ratio and
therefore the synthetic rating on the old basis. Applying the illiquidity discount before
the bridge applies it to firm value rather than equity value.

## Routed examples

These are the course's own cases, run through the tree.

| Company and date | Signals | Route | Outcome |
|---|---|---|---|
| Amazon, Jan 2000 | pre-revenue economics, young growth, negative earnings, no comparables | S5 → **B1**, plus **B4** | Work backwards to a 10% mature retail margin. Value $35.08 against a price of $84. |
| Hormel, 2008 | mature, profitable, policies stable | S5 → **B2** | Status quo $31.91, optimally run $37.80. The gap is the value of control. |
| JC Penney | declining revenue, decline stage, leveraged | S5 → **B3**, handing to **B4** | DCF $4,841m, blended at 20% failure to $4,357m. |
| Las Vegas Sands, Feb 2009 | mature, distress markers, traded bonds far below par | S6 → **B4** | $8.12 going concern, $1.92 after a 76.66% bond-implied distress probability. |
| Deutsche Bank, Oct 2016 | financial service, crisis, capital ratios moving | S2 → **B5**, FCFE to regulatory capital | $22.97, then $20.67 after a 10% equity-wipeout probability. |
| Amgen, May 2007 | intangible-heavy, profitable | S3 → **B8** overlay, then standard | $42.73 unadjusted against $74.33 with R&D capitalized. |
| Shell, Mar 2016 | commodity, high-R² price driver | S2 → **B6** | $39.31 at a $40 oil price. Simulated median $36.99. |
| Tube Investments, 2000 | emerging market, mature, poorly governed | **B2** plus **B9** | Rs 61.57 status quo against Rs 111.3 with returns fixed. |
| Uber, Jun 2014 | young growth, private, business model unproven | **B1** plus **B13** | 10% failure probability, cost of capital 12% falling to 8%. Value $5.9bn. |
| Tesla, Nov 2021 | mature growth, scaling question, profitable | standard path | Failure probability 0%. Contested inputs are the 35% growth rate and the 4.00 sales-to-capital ratio. Value $571.29 against a price of $1,200. |

Two lessons run through the list. First, the branch changes the answer by more than any
input choice inside a branch — Amgen moves 74% on the B8 overlay alone. Second, the branch
names the two or three judgments worth arguing about. For B1 that is the mature end-state.
For B5 it is the sustainable ROE. For B6 it is the price basis and the long-run margin. For
B12 it is the exclusivity factor. For B13 it is `k` and the buyer's diversification. For
B15 it is synergy realization.

## Mode interaction

The mandate's `mode` selects what runs *after* the engine. It never selects the engine.

| Mode | Effect |
|---|---|
| `valuation` | Engine, then uncertainty, then price comparison. |
| `acquisition` | B15's four-number chain wraps whatever engine the target's own classification selected. |
| `restructuring` | Routes to B2 through S4, and the B2 output is the deliverable. |
| `ipo` | Routes to B14 through S4. The engine underneath may still be B1. |
| `corporate-finance` | Runs the capital-structure and payout stages. Both are suppressed entirely for B5 and B5b. |
| `project` | Skips the company engine. Runs `project-investment-analysis` instead. |

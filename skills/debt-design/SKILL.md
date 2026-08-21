---
name: debt-design
description: Matches the kind of debt a firm issues to the assets it finances — maturity, currency, fixed or floating, and features such as convertibility or commodity linkage — using asset duration and the sensitivity of firm value and operating income to interest rates, inflation, real growth and exchange rates. Use when advising on what debt to issue, reviewing an existing debt structure, choosing debt maturity or debt currency, deciding fixed versus floating, or after finding an optimal debt ratio.
---

# Debt design: matching debt to the assets it finances

The optimal debt ratio answers how much to borrow. This skill answers what to borrow.

The principle is matching. Debt cash flows should move with the cash flows of the assets
being financed. When they match, a downturn that cuts asset value also cuts the value of
the debt, and the firm never becomes technically insolvent for structural reasons. When
they do not match, the firm carries default risk that has nothing to do with its business.
A cyclical firm with flat payments defaults in a recession it would otherwise survive. A
firm earning euros and paying dollars defaults on a currency move.

That makes design a value question, not a paperwork question. Better matching lowers
default risk at any given debt level, which raises debt capacity, which raises the optimal
debt ratio and firm value.

## What you produce

A `debt_design` block inside `capital-structure.json`, plus its prose section in
`capital-structure.md`. Both artifacts belong to the `capital-structure-analyst`
(SPEC §3, §6). Do not write into another agent's artifact.

```json
"debt_design": {
  "target_duration": 4.3,
  "currency_mix": [{"currency": "USD", "share": 0.82}, {"currency": "EUR", "share": 0.12}],
  "fixed_floating_split": {"fixed": 0.6, "floating": 0.4},
  "special_features": ["payments linked to park attendance"],
  "convertible_yes_no": false,
  "regression_table": [],
  "existing_profile": {},
  "gap_table": [],
  "closure_instruments": ["swap fixed USD into floating EUR"]
}
```

`regression_table` carries coefficients **and** t-statistics, firm-level and bottom-up.
A coefficient reported without its t-statistic is not usable evidence.

## The script

Every number in that block comes from one engine:

```bash
python3 <skills>/debt-design/resources/macrosensitivity.py <subcommand> --in payload.json
```

| Subcommand | Takes | Gives |
|---|---|---|
| `regress` | one macro series against the firm's own history | slope, standard error, t-statistic, R-squared, observation count, and the duration the rate slope implies |
| `duration` | project cash flows and a discount rate | the present-value-weighted average time the cash arrives, and the maturity of a par bond that matches it |
| `debt-profile` | the four regression results | maturity, currency mix, fixed against floating, straight against convertible |
| `selftest` | nothing | runs the bundled worked examples and reports pass or fail |

Each reads JSON from stdin or `--in FILE` and prints JSON. Run any of them with
`--example` to see the payload shape.

The engine grades its own evidence and will not let a weak slope pose as a strong one.
Every slope comes back marked **finding**, **hint** or **noise**. A finding clears
`|t| > 2` on at least ten observations and may carry a financing decision. Anything
estimated on fewer than ten annual periods is capped at a hint however large its
t-statistic looks, because the sampling distribution behind it is too wide to trust.
Carry that grade into `regression_table` beside the coefficient.

## Preconditions

- `G3_financials` passed. Debt is defined economically, leases capitalized.
- `G4_discount_rate` passed when you intend to compute project duration, because duration
  needs a discount rate in the mandate currency.
- The optimal-ratio work (S7) has run, or you are told explicitly that only the design
  question is in scope.
- The firm is not a financial-service firm. For banks and insurers, debt is raw material
  rather than financing, and the `no-optimal-debt-ratio` constraint applies. Deposit and
  funding structure is a regulatory-capital question, not this one.

## The pipeline

```
Debt design progress:
- [ ] 1. Profile the asset cash flows (intuitive, project duration, or macro regressions)
- [ ] 2. Translate the profile into debt characteristics
- [ ] 3. Overlay tax deductibility
- [ ] 4. Overlay ratings agencies, analysts and regulators
- [ ] 5. Overlay bondholder fears and information asymmetry
- [ ] 6. Tabulate existing debt on the same dimensions and close the gap
- [ ] 7. Feed improved matching back into the optimal debt ratio, once
```

## 1. Profile the asset cash flows

Six characteristics decide everything downstream: duration, currency, inflation
sensitivity, cyclicality, uncertainty about future cash flows, and any specific driver
such as a commodity price or a visitor count.

There are three routes to that profile. They are not ranked. Pick by what the firm looks
like, and say which one you used.

| Route | Use it when | Weakness |
|---|---|---|
| **Intuitive** — reason business by business about project length, currency and drivers | Multi-business firms, and always as a sanity check on the other two | No numbers; cannot set a floating-rate share |
| **Project duration** — PV-weighted life of a typical project | Few, large, independent projects: a mine, a park, a plant | Needs a credible cash flow forecast and terminal value |
| **Historical macro regressions** — the firm's own value and income against macro variables | Long-listed firms with a stable business mix | Noisy; often insignificant; assumes the past business persists |

The intuitive route is worth doing first even when you plan to regress. Write one line per
business naming project length, revenue currency, and the driver of the cash flows. If the
regressions later contradict that line, one of the two is wrong, and finding out which is
the analysis.

Worked business-by-business profiles: [resources/worked-designs.md](resources/worked-designs.md).

## 2. Translate the profile into debt characteristics

| Asset characteristic | Debt characteristic |
|---|---|
| Long asset duration | Long debt duration |
| Revenues earned in several currencies | Debt split across those currencies, by revenue share |
| Operating income rises with inflation (pricing power) | Larger floating-rate share |
| Operating income rises with interest rates | Larger floating-rate share |
| High uncertainty about future cash flows | Shorter maturity |
| Low current cash flow, high expected growth | Convertible rather than straight debt |
| Cyclical income | Less debt overall, or payments tied to output |
| One dominant driver (commodity price, catastrophe, attendance) | A linked feature that ties debt service to that driver |

Two of these deserve care.

**Floating versus fixed is a pricing-power question.** A firm that can pass cost increases
to customers has operating income that rises with inflation, so floating-rate payments
rise when its cash flows rise. A firm selling to powerful buyers who refuse price
increases should hold fixed-rate debt. Giving that firm floating debt stacks interest-rate
risk on top of input-cost risk.

**Currency follows revenues, not incorporation or listing.** A firm expanding into a new
market should borrow in the currency it will earn there, not the currency it reports in.
Where costs and revenues sit in different currencies, match the debt to the net exposure
and say which side you matched.

## 3. Quantify duration when you have a project

Duration is the present-value-weighted average time at which cash arrives:

    duration = Σ t × PV(CF_t) ÷ Σ PV(CF_t)

Include the terminal value. It usually dominates. Omitting it is the single most common
error here, and it can halve the answer.

```bash
python3 <skills>/debt-design/resources/macrosensitivity.py duration --in project.json
```

```json
{
  "discount_rate": 0.0846,
  "cash_flows": [-2000, -1000, -859, -267, 340, 466, 516, 555, 615, 681, 715],
  "terminal_value": 11275,
  "coupon_rate": 0.05
}
```

Cash flows start at year 0. `terminal_value` is added to the final year; pass it, or fold
it into the last cash flow yourself. Leave it out and the output says so in `warnings`,
because that omission is silent and costly. The reply carries the year-by-year present
values, the weighted sum, the duration, and the share of the weighted sum the terminal
value accounts for — check that last number before you believe the first.

The same arithmetic gives a bond's duration. Pass the coupon stream with the face value
added to the final year.

Two facts govern how you use the number. Maturity exceeds duration for any
coupon-paying instrument, so setting maturity equal to asset duration overshoots. Pass
`coupon_rate` and the output solves for the maturity of a par bond whose duration hits
the target, which is the version you can actually take to a lender. And
project-specific financing is right only when projects are few, large and independent.
For a portfolio of small, interdependent projects, match at the firm level instead.

Mechanics, the bond-duration comparison, and a worked 19-year theme-park calculation:
[resources/duration.md](resources/duration.md).

## 4. Run the macro sensitivity regressions

Treat the firm as a portfolio of projects and let its own history describe it. Regress
annual changes in firm value, and separately in operating income, on four macro variables.
These are **eight separate univariate regressions**, not two multiple regressions. Running
one multiple regression produces different numbers and is not the method.

    Δfirm value = (market cap + debt)_t ÷ (market cap + debt)_(t−1) − 1
    Δoperating income = OI_t ÷ OI_(t−1) − 1

| Regressor | Change convention | What the slope tells you |
|---|---|---|
| 10-year government bond rate | **absolute** change in the rate | asset duration (firm value); fixed/floating (operating income) |
| Real GDP | **percentage** change | cyclicality |
| Inflation rate | **absolute** change in the rate | pricing power → floating-rate share |
| Trade-weighted currency index | **percentage** change | foreign-currency share of debt |

Mixing the change conventions is a silent error. The coefficients still print, and they
are wrong by a factor of a hundred.

Run them one at a time:

```bash
python3 <skills>/debt-design/resources/macrosensitivity.py regress --in macro.json
```

```json
{
  "dependent": "firm_value",
  "macro_variable": "interest_rate",
  "history": {"market_cap": [231814, 209728], "total_debt": [54136, 53427]},
  "macro_changes": [0.0027]
}
```

That is the shape, cut to two periods to fit; a real payload needs at least five.
`dependent` is `firm_value` or `operating_income`. `macro_variable` is one of
`interest_rate`, `gdp_growth`, `inflation`, `exchange_rate`, and the reply echoes the
change convention that variable expects so a mismatch is visible rather than silent.

Pass the raw history most recent period first and the engine builds the changes itself:
firm value as market cap **plus** debt, operating income as a percent change, both
compared against the period before. Eleven periods give ten change rows, so send ten
macro changes covering the same fiscal years. Or skip that and pass `dependent_changes`
directly.

The engine refuses rather than guesses. Operating income at or below zero in any period
is rejected by name, because a percent change off that base is meaningless and will
dominate the fit. A macro column with no variation, a series with a text placeholder in
it, and a sample too short to yield a standard error are all refused with an explanation.

The reply also carries a `warnings` list. It fires when you read a coefficient off the
dependent variable the method does not read it from, and when the sample is short.

### Reading a slope as a duration

The interest-rate slope on firm value is an empirical duration. Firm value falls when
rates rise, so the slope is negative, and the duration is its magnitude:

    asset duration = max(0, −slope of Δfirm value on Δ interest rate)

A slope of −4.34 means debt with a duration of about 4.3 years. The floor at zero matters:
a positive slope does not mean negative duration, it means the estimate carries no
information about maturity and you should fall back to another route.

The engine makes this reading for you. Any `interest_rate` regression comes back with
`implied_duration_years` and a `duration_note` that names it a duration. When the slope
is positive the note says the floor has bound and sends you elsewhere, rather than
printing a zero you might mistake for a short-duration firm.

### When the historical route fails

**A slope with |t| below 2 must not drive a financing decision.** This is common rather
than exceptional. Firm-level macro slopes are noisy, and a graded course team once found
exactly one significant coefficient across four firms.

Two other failure conditions:

- **Too few observations.** Fewer than about ten annual periods leaves standard errors
  wide enough to swamp any slope. Skip firms listed three years or less entirely.
- **A changed business.** The regression assumes future projects resemble past ones. After
  a large acquisition, a divestiture, or a shift in business mix, the history describes a
  company that no longer exists. Quarterly data buys observations but not relevance.

In all three cases switch to **bottom-up**: take sector coefficients for each business the
firm operates in and value-weight them, exactly as with bottom-up betas.

    firm coefficient = Σ (business value weight × sector coefficient)

Sector tables, the Disney reference regressions, the sign conventions that differ between
the sector sheet and the bottom-up estimator, and the data sources for each macro series:
[resources/macro-regressions.md](resources/macro-regressions.md).

### Turning the four slopes into a design

Hand the four results back, whether they came from the firm's own history or from
value-weighted sector coefficients:

```bash
python3 <skills>/debt-design/resources/macrosensitivity.py debt-profile --in slopes.json
```

```json
{
  "home_currency": "USD",
  "interest_rate": {"slope": -4.34, "t_statistic": 2.20, "observations": 28,
                    "dependent": "firm_value"},
  "gdp_growth": {"slope": 0.55, "t_statistic": 2.03, "observations": 28,
                 "dependent": "firm_value"},
  "inflation": {"slope": 8.1867, "t_statistic": 2.76, "observations": 28,
                "dependent": "operating_income"},
  "exchange_rate": {"slope": -1.67, "t_statistic": 2.13, "observations": 28,
                    "dependent": "operating_income"},
  "operating_income_on_interest_rate": {"slope": -7.9339, "t_statistic": 1.40,
                                        "observations": 28},
  "revenue_by_currency": [{"currency": "USD", "share": 0.82},
                          {"currency": "EUR", "share": 0.18}],
  "expected_revenue_growth": 0.06,
  "current_cash_flow_positive": true,
  "coupon_rate": 0.05
}
```

A `regress` reply drops straight into any of those slots. Four blocks are required; the
rest refine the answer. Each maps to one debt characteristic:

| Slope | Sets |
|---|---|
| `interest_rate` on firm value | target duration, and the par-bond maturity that matches it |
| `exchange_rate` | whether to borrow abroad; `revenue_by_currency` then sizes the split |
| `inflation` and `interest_rate`, both on operating income | the floating-rate share |
| `expected_revenue_growth` with `current_cash_flow_positive` | straight against convertible |
| `gdp_growth` | cyclicality, which adds output-linked features or argues for less debt |

Two behaviours are worth knowing before you read the output.

**It reads each slope off the dependent variable the method specifies.** Duration and
cyclicality come from firm value; inflation and currency come from operating income. Pass
`operating_income_on_interest_rate` so the floating-rate call uses the cash flows that
service the debt rather than the market value. Skip it and `convention_warnings` says so.

**Convertible is a growth call, not a cyclicality call.** A firm can be sharply cyclical
and still belong in straight debt if its current cash flows service it — cyclicality buys
output-linked features and a lower debt level instead. Convertible is for the firm whose
value sits in what has not been built yet: high expected growth, current cash flows that
cannot carry a coupon. Supply both fields or the engine declines the call and says why.

The floating-rate share comes back as a band with a number attached. The source method
sets that share by judgment and gives no formula, and the output says as much. Treat it as
a starting position to argue with, not an estimate.

## 5. The overlays

Matching sets the target. Four overlays can move it, and one can stop an issue entirely.
Apply them in this order and record any that bind.

### Tax deductibility

A perfectly matched instrument that does not deliver a tax deduction has thrown away the
main benefit of borrowing. Check deductibility in the relevant jurisdiction before
recommending anything structured.

Two limits bind at high debt levels. Interest above EBIT shelters nothing, and statutory
caps limit net interest deductions to a share of earnings. Both show up as a reduced tax
rate applied to the cost of debt, and the capital-structure schedule already handles them:
`t_used = MIN(t_EBIT, t_cap)`. If your design pushes the firm past either limit, the
schedule from `cost-of-capital-toolkit debt-schedule` will show it.

A large enough tax advantage can override matching. Say so explicitly when it does, and
quantify it, rather than letting an instrument be chosen for tax reasons in silence.

### Ratings agencies, analysts and regulators

Three audiences watch different numbers. Analysts watch earnings per share and comparables,
and dislike issues that dilute. Agencies watch ratios and prefer equity. Regulators watch
book measures.

The main practical case is a quasi-equity instrument. It benefits one specific firm: an
under-levered firm with a rating constraint that moving to its optimum would breach. That
firm captures debt-like tax benefits while keeping the rating. Do not generalize the trick.
Agencies now grant such instruments only partial equity credit, and a structure designed to
fool them will not.

Agencies also penalize speed. A rating-constrained firm should move gradually even when the
design is right.

### Bondholder fears

Where lenders cannot observe cash flows, or the assets are intangible rather than tangible
and liquid, agency costs are high and the firm pays a wide spread. Three features answer
that directly: convertible bonds, puttable bonds, and ratings-sensitive notes. Each gives
the lender a claim that improves if the borrower behaves badly, which is what lets the
coupon come down.

Check the existing covenant load before adding features. A firm already carrying tight
investment and financing covenants may be paying twice for the same protection.

### Information asymmetry

More uncertainty about future cash flows, or a credibility problem with lenders, argues
for shorter-term debt. Short maturities force the firm back to the market often, which is
costly, and that cost is what makes the commitment credible.

### Do not lock in a market mistake

This one can override the entire design. If the firm is under-rated, issuing long-dated
debt locks a rate far above its true default risk for the life of the bond. If the stock
is under-priced, issuing equity or equity-linked paper transfers wealth from existing
holders to new ones.

When the firm must finance while mispriced, use short-term or delayed structures until
the mistake corrects. State the mispricing claim and its evidence. "We think our stock is
cheap" is an assertion; a status-quo valuation against the market price is evidence.

Instrument menu, the deductibility checks, and the agency-cost features in detail:
[resources/overlays.md](resources/overlays.md).

## 6. Tabulate the gap and close it

Put the recommendation beside the existing debt profile on identical dimensions. The gap
table is the deliverable, not the recommendation alone.

| Dimension | Recommended | Actual | Gap |
|---|---|---|---|
| Duration / weighted-average maturity | 4.3 years | 7.92 years | too long |
| Foreign-currency share | 18% | 5.49% | too little |
| Floating-rate share | significant | 5.67% | too little |
| Convertible share | none | none | matched |

Compute the actual profile from the debt footnote: face-value weighted average maturity,
currency shares, fixed and floating split, convertible share. That side of the table is
arithmetic and should be sourced, not estimated.

Close the gap two ways. Swap existing debt into the recommended form, which is usually
cheaper and faster than refinancing. And issue new debt in the recommended form. Firm-level
matching improves even when a specific new issue does not match a specific new asset, so
do not wait for a perfectly matched project to appear.

Write the recommendation as one sentence naming maturity, currency, rate type and features.
"Six to eight year duration, in the currency mix where the new stores will earn revenue,
with a large floating-rate share given the pricing power" is a recommendation. "Better
matched debt" is not.

## 7. Feed the answer back

Improved matching raises debt capacity. Re-check the optimal debt ratio **once** with the
improved design, then stop. Running the loop repeatedly manufactures precision that the
10% grid and noisy inputs do not support.

## Common failures

| Symptom | Cause |
|---|---|
| Duration comes out implausibly short | Terminal value omitted from the cash flow stream |
| Recommended maturity equals asset duration exactly | Maturity confused with duration; maturity always exceeds it |
| Macro coefficients look enormous | Percentage changes used where absolute rate changes belong |
| Firm-level regressions produce a confident design | Slopes with t below 2 were read as if significant |
| Negative duration | Positive interest-rate slope, which should be floored at zero and routed to bottom-up |
| Percent change in operating income is meaningless | Operating income near zero or negative in a base period |
| Design recommends floating debt for a supplier to large retailers | Pricing power assumed rather than tested against the inflation slope |
| Debt currency matches the listing country | Currency matched to incorporation instead of where revenues arise |
| Design is elegant and the firm gets no tax deduction | Tax overlay skipped |
| Long-dated issue at a wide spread just before an upgrade | Market mistake locked in |
| Design treated as a footnote to the debt ratio | Matching raises debt capacity, so it changes the ratio itself |
| `regress` refuses a period by name | Operating income at or below zero there; drop it and re-run |
| Floating-rate call contradicts the pricing-power story | `operating_income_on_interest_rate` omitted, so the call fell back to the firm-value slope |
| `debt-profile` returns straight debt for an obviously cyclical firm | Correct: convertible is a growth call, and cyclicality buys output-linked features instead |

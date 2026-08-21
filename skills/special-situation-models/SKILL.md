---
name: special-situation-models
description: Values companies the standard DCF cannot handle, across five branches — distress (failure probability from a bond price or rating, blended with the distress-sale outcome), financial service firms (equity excess return and FCFE against regulatory capital, since a bank gets no FCFF and no optimal debt ratio), private companies (total beta for an undiversified owner, Silber and bid-ask illiquidity discounts), cyclical and commodity firms (mid-cycle normalized earnings), and young negative-earnings firms (a revenue and margin path plus survival odds, emitted as a dcf-valuation-engine payload). Also walks a private owner's value to an IPO offer price line by line. Use when valuing a bank, insurer, startup, distressed firm, private business, miner or deep cyclical, when pricing an IPO or a sale to a public buyer, or when asked about probability of distress, total beta, illiquidity discount, excess return models, normalized earnings, or negative-earnings valuation.
---

# Special situation models

A standard discounted cash flow model assumes a lot. It assumes the firm survives to reach
stable growth, that its debt is a financing choice, that its owner is diversified, that
this year's earnings say something about a normal year, and that there are earnings at all.

Five kinds of company break one of those assumptions. This skill repairs the specific
break. It does not replace the DCF, and for four of the five branches the answer still runs
through `dcf-valuation-engine`.

## Which branch applies

Answer this before running anything. The branch is a judgment about the company, and the
script does not guess it for you.

| The company is | Branch | Subcommand |
|---|---|---|
| At real risk of not surviving — high leverage, marginal operating income, a declining business | 1. Distress | `distress` |
| A bank, an insurer, or any firm whose raw material is money | 2. Financial service | `excess-return` |
| Not publicly traded, and the buyer cannot diversify | 3. Private company | `private` |
| At a point in a cycle, or driven by a commodity price | 4. Cyclical or commodity | `cyclical` |
| Young, growing fast, and losing money | 5. Young company | `young-company` |

More than one can apply. A young company usually needs branch 5 and branch 1 together. A
private cyclical needs 3 and 4. Run them in the order above, because each later branch
consumes the output of the earlier one.

One transition sits alongside the five: a private company on its way to a public listing,
or to a sale to a listed buyer. That is the `ipo` subcommand, and it consumes branch 3.

### What each branch forbids

This is the part that gets skipped, and it is where the damage happens.

**A bank gets no FCFF valuation and no optimal-debt-ratio analysis.** For an industrial
firm, debt is a source of capital, so you can separate operating from financing decisions.
For a bank, debt is raw material. Deposits are the input the business transforms into
loans. There is no meaningful firm value and no meaningful cost of capital, so do not run
`dcf-valuation-engine value` on a bank, and do not run
`cost-of-capital-toolkit debt-schedule` on one. Regulatory capital governs the financing
mix, not a tax-shield calculation. A bank that breaches its capital ratio can be taken over
and closed however good its earnings look.

**Distress risk does not belong in the discount rate.** Raise the rate *and*
probability-weight the value and you have counted the same risk twice. Pick the probability
weight.

**A total beta does not belong in a valuation for a diversified buyer.** It systematically
undervalues the business and hands the surplus to the buyer. The same applies to the
illiquidity discount: a listed acquirer's own shareholders can sell, so no discount
applies.

**A trailing return on equity does not survive re-regulation.** If the regulator is about
to demand more capital, the return earned on the old base is not the sustainable one.

**Normalized earnings and a recovery in growth are the same recovery.** Normalize the base
year or forecast the recovery, not both.

**A young company with no failure branch is not a valuation.** Roughly two-thirds of
startups are gone within seven years, and the value of the survivors is not the value of
the population.

## The script

`resources/special.py` — pure standard library, no installation needed. Every subcommand
takes JSON on stdin (or `--in FILE`) and prints JSON.

```bash
python3 resources/special.py <subcommand> --example    # show the input shape
python3 resources/special.py <subcommand> --in payload.json
python3 resources/special.py selftest                  # verify the engine
```

| Subcommand | Turns this | Into this |
|---|---|---|
| `distress` | a traded bond price, or a rating | annual and cumulative probability of failure, and the two-branch blend |
| `excess-return` | book equity, a return-on-equity path, a capital path | bank equity value, per share, both by residual income and by FCFE |
| `private` | a market beta with its R-squared, revenues, profitability | total beta, cost of equity, three illiquidity discounts |
| `ipo` | a private value, the offering terms and the cap table | the bridge from private value to offer price, step by step |
| `cyclical` | an earnings history, or a commodity price link | mid-cycle operating income, revenues at today's price |
| `young-company` | a revenue target and a margin target | a full `dcf.py value` payload plus survival odds |

Run `selftest` after editing anything. It reproduces the source models to nine decimals
and checks identities that a wrong port would break. Every case it runs is written up in
[resources/worked-examples.md](resources/worked-examples.md), with the payload alongside
the answer.

## 1. Distress adjustment

A going-concern model prices only the branch where the firm lives. The repair is an
explicit probability-weighted blend of two outcomes.

```
value = going-concern value × (1 − p) + distress-sale value × p
```

### Getting the probability

Five sources, in increasing order of information content. Pass whichever you have.

| Input | Source |
|---|---|
| `bond` | the market price of the firm's own traded bond — the sharpest and usually the most pessimistic |
| `rating` | the cumulative ten-year default rate for that rating class |
| `sector_survival` | long-run survival statistics, for a firm with no debt to price |
| `annual_probability` | your own estimate, stated per year |
| `cumulative_probability` | your own estimate, stated over the horizon |

The bond route prices the promised coupons and principal, weights each by the probability
the firm survives to pay it, and discounts at the **riskfree** rate. All the credit risk
sits in the survival weights. Discounting at the bond's own yield instead would count it
twice.

```bash
echo '{"bond": {"coupon_rate": 0.06375, "maturity_years": 7,
                "riskfree_rate": 0.03, "market_price": 529},
       "horizon_years": 10, "going_concern_value": 8.12,
       "distress": {"basis": "explicit", "proceeds": 2769,
                    "debt_face_value": 11000}}' \
  | python3 resources/special.py distress
```

Two modelling assumptions are baked in: recovery in distress is zero, and discounting is at
the riskfree rate. Both are choices. Assuming a positive recovery would lower the implied
probability for the same price.

Report the **cumulative** probability over your forecast horizon, not the annual one. For
Las Vegas Sands the difference between 13.54% a year and 76.66% over ten years is the
difference between a $7 stock and a $2 stock.

### Getting the distress-sale value

Set `distress.basis`:

- `book` — proceeds are a percentage of book equity plus book debt. The default recovery is
  50%. Cut it when the economy is weak and every peer is selling the same assets at once.
- `going_concern` — proceeds are a percentage of the going-concern value, for a firm that
  would be sold intact rather than broken up.
- `explicit` — you have an estimate of what the assets would fetch.

Add `debt_face_value` when you are valuing equity. Equity in distress is a residual: if
proceeds fall short of what lenders are owed, shareholders get nothing.

### The partial wipeout

A bailout can save the firm and destroy the equity. Set `equity_loss_fraction` instead of a
distress branch, and the blend becomes a single haircut:

```
adjusted value = going-concern value × (1 − probability × loss fraction)
```

Boeing in March 2020: a 20% failure probability with a 50% loss to equity is a 10% haircut,
not a 20% one.

### Where the number goes

`dcf-valuation-engine` already has a `failure` block that does the simple blend. Feed it the
cumulative probability from here. Use this subcommand's own blend when equity is a residual
against the face value of debt, or when the case is a partial wipeout — neither of those
fits in the DCF engine's block.

## 2. Financial service firms

Value the equity directly. See
[resources/financial-service-firms.md](resources/financial-service-firms.md) for the full
argument and for the choice among the three equity models.

```
value of equity = current book equity + PV of (return on equity − cost of equity) × book equity
```

Book value is close to irrelevant for an industrial firm. For a bank it is the opposite:
assets are marked to market, and regulatory ratios are computed on book equity. That gives
a bank a hard definition of reinvestment, which industrial firms lack.

Two reinvestment modes:

**`retention`** — book equity grows by retained earnings. This is the standard equity
excess return model. Give a high-growth return on equity, a retention or payout ratio, and
a stable block. Each driver fades to its stable value over the second half of the horizon
unless you set `fade_second_half: false`.

**`regulatory_capital`** — book equity is whatever the capital ratio requires. Give the
risk-adjusted assets, their growth rate, and the path of the Tier 1 or CET1 ratio. Use this
when ratios are moving or the bank is in crisis. Book equity often sits above regulatory
capital, so pass `required_book_equity` as a year-by-year list instead when the bank has
disclosed the path. Subtract any one-off hit to capital, such as a fine, with
`one_off_capital_hit`.

```bash
echo '{"book_equity": 64609, "forecast_years": 10,
       "reinvestment": "regulatory_capital",
       "regulatory_capital": {"risk_adjusted_assets": 445570, "asset_growth": 0.01,
                              "capital_ratio": {"start": 0.1241, "end": 0.1567,
                                                "converge_by": 10}},
       "return_on_equity": {"start": -0.137, "end": 0.0944, "converge_by": 10},
       "cost_of_equity": 0.102, "shares_outstanding": 1386,
       "probability_of_equity_wipeout": 0.10,
       "stable": {"return_on_equity": 0.0944, "growth_rate": 0.01,
                  "cost_of_equity": 0.0944}}' \
  | python3 resources/special.py excess-return
```

### Reading the output

`value_of_equity` and `value_of_equity_via_fcfe` should match, and `route_difference`
should be near zero. Residual income and discounted free cash flow to equity are the same
model written two ways. A gap means the book-equity rollforward disagrees with the cash
flows, which is the classic bank-model error.

Early `fcfe` is deeply negative for a bank rebuilding capital. That is correct, not a bug.
Every increase in the capital ratio is reinvestment and it comes out of shareholder cash
flow.

Three inputs carry the answer. Set the sustainable return on equity, not the trailing one.
Anchor the terminal return on equity on the cost of equity unless a franchise justifies
more. Anchor the target capital ratio on the peer distribution rather than the regulatory
minimum.

## 3. Private company adjustments

Two separate repairs, and the script runs both. Detail in
[resources/private-company-adjustments.md](resources/private-company-adjustments.md).

**Total beta**, for an owner who holds nothing else:

```
total beta = market beta / correlation with the market
correlation = square root of the average R-squared of the comparables' regressions
```

The square root is not optional. R-squared is a share of variance and betas are built from
standard deviations. Dividing a 1.18 beta by an R-squared of 0.25 gives 4.72; dividing by
the correlation of 0.50 gives 2.36.

**An illiquidity discount**, applied to equity value after the DCF:

```bash
echo '{"buyer": "private",
       "cost_of_equity": {"unlevered_market_beta": 1.18, "r_squared": 0.25,
                          "debt_equity_ratio": 0.1433, "tax_rate": 0.40,
                          "riskfree_rate": 0.0425, "equity_risk_premium": 0.04},
       "illiquidity": {"revenues_millions": 1.2, "positive_earnings": true,
                       "cash_to_firm_value": 0.05},
       "equity_value": 520990}' \
  | python3 resources/special.py private
```

Three routes come back. The flat 25% rule of thumb, the Silber-refined restricted-stock
number, and the bid-ask spread regression. They disagree by a lot — on the restaurant
above, by $83,000 on a $521,000 business. Prefer the bid-ask route: it is the most
firm-specific and it draws on an unbiased sample. Say which one you used.

Set `buyer` correctly. A `private` buyer gets the discount. A `public` or `ipo` buyer does
not, because the exit already exists, and the script zeroes the discount for them.

Assemble the cost of capital in `cost-of-capital-toolkit`. Its `rating` subcommand builds a
synthetic cost of debt from interest coverage, and `wacc` does the weighting. Lever the
beta and weight the cost of capital at the same debt-to-equity ratio.

## 4. Cyclical and commodity normalization

Keep macro out of the micro. If you build your own oil forecast into the valuation, the
answer is a blend of two opinions and no reader can tell which is doing the work.

**When a usable price driver exists**, regress revenues on the commodity price and run the
valuation at today's market price or the futures strip:

```bash
echo '{"commodity": {"history": {"price": [...], "revenue": [...]},
                     "price": 40, "price_ladder": [30, 40, 50, 60, 80]},
       "base_operating_margin": 0.0301, "target_operating_margin": 0.0935}' \
  | python3 resources/special.py cyclical
```

Pass `intercept` and `slope` instead of `history` if you fitted the regression elsewhere.
The output reports the R-squared and warns when the price explains less than half the
variation in revenues, which means the link is too weak to use.

Then state the answer as *"worth X at today's commodity price"*. State your macro
disagreement separately, and use the price ladder to quantify it.

**When no usable price driver exists**, normalize earnings instead. Three approaches:

| Approach | Formula | Use when |
|---|---|---|
| 1 | average EBIT over a full cycle | the firm's scale has not changed much |
| 2 | average pre-tax return on capital × current book capital | the firm has grown, so old dollar earnings understate it |
| 3 | aggregate historical margin × current revenues | revenues are meaningful but margins have collapsed |

Approach 3 is the default. The aggregate margin is the sum of EBIT over the sum of
revenues, not the average of the yearly margins. The two differ and the aggregate is the
one to use.

Normalization is only legitimate when the trouble is temporary. Evidence for: the sector is
in a known downturn, peers show the same pattern, the firm earned normal margins for years,
and the balance sheet can survive until recovery. Evidence against: falling market share, a
structural demand shift, leverage that forces asset sales. If the trouble is permanent, go
to branch 5 or branch 1 instead.

The normalized EBIT changes everything downstream. Recompute interest coverage, the
synthetic rating, the cost of debt and the return on capital with it. That chain lives in
`cost-of-capital-toolkit rating`, and lease capitalization lives in
`financial-statement-normalization`. Those two are circular with each other, so iterate.

Read `dcf_drivers` from the output for the base revenue and margin glide to paste into the
DCF payload. Set the terminal return on capital to the firm's own long-run average, not a
trough number.

## 5. Young companies with negative earnings

Work backwards from a mature end-state. Current earnings are meaningless and there is no
history to extrapolate, so specify the revenue scale, margin and return the business will
have when it grows up, then let the intermediate years converge to it.

```bash
python3 resources/special.py young-company --example > drivers.json
python3 resources/special.py young-company --in drivers.json > out.json
```

### The two shapes

**Revenue.** Either state the high-growth rates directly
(`mode: "explicit"`, `high_growth_rates: [1.50, 1.00, 0.75, 0.50, 0.30]`), or state the
revenue you expect in a given year (`mode: "target_revenue"`) and let the engine solve for
the growth rate that reaches it. Either way, growth then fades linearly to the stable rate
by the final year.

Cross-check the answer twice. Excess growth over the industry average dies within roughly
five years of an IPO. And `market_share_check` in the output compares year-10 revenue with
the total addressable market — if the implied share is implausible, the growth path is
wrong.

**Margin.** `style: "halving"` closes a fixed share of the gap to the target each year,
which is the shape the Amazon January 2000 valuation uses. `style: "linear"` runs a
straight line to a stated convergence year, which is the Ginzu convention. Set the target
margin from the mature sector's margin, not from the company's story.

### Survival

Required, not optional. Give `survival.probability_of_failure` directly, or
`survival.sector` to look up long-run survival, or `survival.years_since_founding` for the
startup table. The probability lands in the payload's `failure` block.

### The handoff to dcf-valuation-engine

`dcf_payload` in the output is a complete, valid input to
`dcf-valuation-engine/resources/dcf.py value`. These fields are produced here:

| Field | What this skill sets |
|---|---|
| `base_revenue`, `base_ebit`, `base_invested_capital` | passed through from your inputs |
| `forecast_years` | passed through |
| `revenue_growth` | a list, one rate per year, high-growth rates then a linear fade |
| `operating_margin` | a list, one margin per year, ramped to the target |
| `sales_to_capital` | a list, so reinvestment is charged against the revenue change |
| `tax_rate`, `cost_of_capital` | passed through as a number, list, or glide |
| `net_operating_loss_carryforward` | passed through, so the DCF engine's tax engine shelters early income |
| `terminal.growth_rate`, `.cost_of_capital`, `.return_on_capital`, `.operating_margin` | from your terminal block, with the target margin as the default |
| `failure.probability`, `.proceeds_basis`, `.proceeds_percent`, `.book_value_of_capital` | from the survival lookup and the distress block |
| `bridge`, `currency` | passed through if you supply them |

Fill in the bridge yourself: debt, cash, minority interests, non-operating assets, share
count, and the value of employee options. `missing_from_payload` lists what is still
outstanding. Value the options in `option-valuation-toolkit` and pass the result in;
inflating the share count instead understates their cost.

Then run the DCF:

```bash
python3 ../../dcf-valuation-engine/resources/dcf.py value --in payload.json
```

Read `forecast[].roic` from that output. If the imputed return on capital drifts to an
absurd level, the margin, the sales-to-capital ratio and the growth assumption contradict
each other.

Two things not to do. Do not use a regression beta for a young stock — Amazon's had an
R-squared of 0.17 and a standard error of 0.50. And do not hold the cost of capital
constant for ten years when the whole story is that the firm matures.

## 6. The private-to-public step

An offering changes who owns the business. That moves the discount rate, the illiquidity
discount, the cash in the firm and the share count, all at once. `ipo` runs the changes as
a ladder and prices each one separately, so the reader can see where the value went. Every
row of `bridge` carries the equity value and the value per share before and after one
adjustment.

```bash
python3 resources/special.py ipo --example | python3 resources/special.py ipo
```

| Step | Driven by | Skipped when |
|---|---|---|
| The owner's own value | `revaluation` or `value_of_operating_assets`, `cash`, `debt` | never |
| Remove the illiquidity discount | `illiquidity_discount` | it is absent or zero |
| Revalue at the market beta | `revaluation` | you supply an already-public value |
| Add the proceeds that stay in the firm | `proceeds` | nothing is being raised |
| Subtract options and warrants | `claims.options_and_warrants_value` | there are none |
| Pay non-converting liquidation preferences | `convertible_preferred` | every round converts |
| Restate on the post-offering share count | `shares` | never |
| Apply the offering discount | `offering_discount` | you do not state one |

**The discount rate.** Give a `cost_of_equity` block — the same one branch 3 takes, plus
`pre_tax_cost_of_debt` — and the script builds both costs of capital from the one bottom-up
beta: the private owner's off the total beta, the market's off the market beta. With a
`revaluation` block it then values the business as a growing perpetuity at each rate. For
the restaurant that is 13.25% against 8.76%, and equity of 521 against 1,484 on identical
cash flows. If your DCF already ran on a market beta, pass `value_of_operating_assets`
instead and the beta step drops out.

**Use of proceeds.** Read the prospectus, then classify.

| Use | `proceeds` field | Treatment |
|---|---|---|
| The owners cash out | `to_owners` | adds nothing; that money never reaches the business |
| Held for future reinvestment | `retained` | added dollar for dollar |
| Repays debt | `pay_down_debt` | shortens the bridge, but changes the debt ratio too |

The three must sum to `gross_proceeds`, or use `"use": "retained"` for a single bucket. The
debt-repayment case is only half-done here: the output warns that the cost of capital has
to be recomputed at the new debt ratio and the operating assets revalued.

**Prior claims and the share count.** Options and warrants come out of the numerator as a
value and stay out of the denominator. Everything that becomes common goes into the
denominator: `common_shares`, `restricted_stock_units`, `shares_owed_under_acquisitions`,
`new_primary_shares`, and the as-converted shares of any preferred that converts.

Each entry in `convertible_preferred` carries an `as_converted_shares` count and a
`liquidation_preference`, and takes whichever is worth more. Leave `converts` at its
`"auto"` default and the engine iterates to the fixed point, because each round's choice
moves the per-share value the others are choosing against. Force it with `true` or `false`
when the terms do. A round that takes its preference in cash keeps its shares out of the
count.

**The offering discount.** `offering_discount` is a pricing decision, not a change in
value: the bank guarantees the offer price and carries the placement risk, so it prices
below the number the model produced. Nothing is applied unless you state it. Average
first-day returns run 10–15% and are largest for the smallest deals. The separate
`underpricing` block sizes what that costs the owner — and the loss falls only on the stake
actually sold, so a 10% float loses a tenth of what a full float loses.

## Reference data

`resources/data/distress_reference.json` holds the rating-to-default mapping, the startup
survival table and long-run sector survival, each with an `as_of` date.
`resources/data/illiquidity_reference.json` holds the pre-computed Silber discount table
and the restricted-stock and pre-IPO study results.

Default rates and survival statistics are re-estimated annually, and the bid-ask
coefficients date from the end of 2000. Check the vintage. Pass a refreshed file with
`reference_path` rather than editing the bundled copy, and record which vintage the
valuation used.

## Related engines

Call these rather than rebuilding their arithmetic here.

| Need | Skill and subcommand |
|---|---|
| The DCF itself, sensitivity, implied expectations | `dcf-valuation-engine`: `value`, `sensitivity`, `implied` |
| Synthetic rating, cost of debt, bottom-up beta, WACC | `cost-of-capital-toolkit`: `rating`, `beta`, `wacc` |
| Lease and research capitalization, FCFF, invested capital | `financial-statement-normalization` |
| Employee options, equity as a call on a distressed firm | `option-valuation-toolkit` |
| Cross-checking the finished artifacts | `valuation-consistency-checks` |

## Common failures

| Symptom | Cause |
|---|---|
| Distressed firm still looks cheap after the adjustment | Annual probability used where the cumulative one belongs |
| Distress adjustment feels like it double-counts | Failure risk also loaded into the discount rate |
| Equity keeps a positive value in the distress branch | `debt_face_value` not supplied, so the residual test never ran |
| Bond solver returns zero | The bond trades above the riskfree-discounted value of its promised payments; there is no root |
| Bank equity value far above book | Terminal return on equity left above the cost of equity, so excess returns run forever |
| `route_difference` is not near zero | The book-equity path and the cash flows disagree; check the payout and capital ratio paths |
| Bank model shows a rising capital ratio and healthy cash flow | The increase in required capital was not charged as reinvestment |
| Private company beta looks about twice too high | Divided by R-squared instead of by the correlation |
| Illiquidity discount applied to a listed acquirer | `buyer` left at `private` when the buyer has a liquid exit |
| IPO value per share looks about a fifth too high | Restricted stock units or acquisition shares left out of the count |
| IPO value per share looks too low and options were valued carefully | Option shares counted in the denominator as well as subtracted |
| IPO proceeds lift value even though the founders are selling | Proceeds bucketed as `retained` when they belong in `to_owners` |
| Illiquidity discount barely moves with block size | Expected: the block term cancels in the Silber formula |
| Normalized earnings look healthy for a broken business | Normalization applied where survival, not the cycle, is the question |
| Commodity valuation disagrees with a colleague | Own price forecast embedded instead of today's market price |
| Young company worth billions | No failure probability, or a target margin nobody in the sector earns |
| Emitted payload rejected by the DCF engine | Terminal growth above the riskfree rate, or terminal reinvestment above 100% — both are real errors |

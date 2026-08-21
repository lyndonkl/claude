# Step 4: Connecting the narrative to the drivers of value

**Core idea:** This is the bridge itself. Each claim in the story maps to exactly one input in the intrinsic-value chain, and each input carries one sentence of story. The chain is fixed: total market × market share gives revenues; minus operating expenses gives operating income; minus taxes gives after-tax operating income; minus reinvestment gives after-tax cash flow. Those cash flows are then adjusted for time value and operating risk through the discount rate, and for failure through a probability of failure. In the compact form used in Damodaran's DIY models, the whole story reduces to five levers: revenue growth, operating margin, investment efficiency, cost of capital, and probability of failure. Each lever is best chosen against a reference distribution, not out of thin air.

**Formulas:**
- Revenues_t = Total market_t × Market share_t. Total market_t = Total market_0 × (1 + market growth)^t.
- EBIT_t = Revenues_t × Operating margin_t.
- EBIT(1−t)_t = EBIT_t × (1 − tax rate_t).
- Reinvestment_t = (Revenues_t − Revenues_{t−1}) / Sales-to-capital ratio_t. The sales-to-capital ratio is the revenue each dollar of invested capital supports.
- FCFF_t = EBIT(1−t)_t − Reinvestment_t.
- Expected growth = Reinvestment rate × Return on capital.
- Stable-period reinvestment rate = Stable growth / Stable return on capital.
- Expected value = Value of operating assets × (1 − probability of failure) + Distress proceeds × probability of failure.
- Implied CAGR from an end-state revenue target: CAGR = (Target revenues / Current revenues)^(1/n) − 1, over n years.

**Procedure:**
1. **List the story claims** from step 2 of [[story-to-numbers-process]].
2. **Assign each claim to one driver.** Market definition and market growth → total market. Competitive position and network effects → market share. Pricing power, revenue slice and cost structure → operating margin. Capital intensity → sales-to-capital. Business maturity and operating risk → cost of capital. Survival → probability of failure.
3. **Set the growth lever from an end-state, not a rate.** Pick the revenue you believe the company reaches in year 10, then back out the CAGR. This forces you to look at absolute dollars.
4. **Set the margin lever against a reference class.** Auto industry quartiles, technology median, software, FAANG. Choosing a margin far outside the class is allowed, but it is now an explicit claim.
5. **Set the investment-efficiency lever against industry sales-to-capital.** A ratio well above the industry means you are claiming unusually efficient growth, and the implied marginal ROIC will show it.
6. **Set the cost of capital from the market's distribution of costs of capital,** not from a theoretical construct. It is what investors currently demand. It is also not in the top five inputs driving value, so do not spend your day on it.
7. **Set failure risk explicitly** if the business could fail, and decide whether distress proceeds are tied to book value or to going-concern value.
8. **Decide the terminal-phase defaults.** Terminal growth defaults to the riskfree rate. Terminal return on capital defaults to the terminal cost of capital, meaning no excess returns. Override only with a stated competitive-advantage argument.
9. **Write the story link on each row.** If a row has no link, delete the row or find the claim.

**Reference data:** Uber, June 2014 — narrative claim to driver:

| Narrative claim | Driver | Value |
|---|---|---|
| Urban car service company competing with taxis and limos, possibly expanding demand | Total market | Global taxi/limo market $100 billion in 2013, growing 6%/yr |
| Competitive advantages against incumbents and newcomers, but no global network effects | Market share | 10% target share |
| Keeps 20% of car-service payments even under competition; low-infrastructure cost model | Operating margin | 40% target pre-tax operating margin |
| Owns no cars and little infrastructure | Reinvestment | Sales-to-capital ratio 5.00 |
| Young company still proving its model | Discount rate | Cost of capital 12% initially, declining to 8% |
| Has cash and capital but could still fail | Failure | 10% probability of failure |

Tesla, November 2021 — the five levers and their reference menus:

Growth lever (2030 revenue target → implied 5-year CAGR):

| Choice | 2030 revenues | CAGR |
|---|---|---|
| A1: BMW-like | $100 billion | 12.00% |
| A2: Ford & Honda-like | $150 billion | 18.00% |
| A3: Daimler-like | $200 billion | 22.50% |
| A4: Toyota & VW-like | $300 billion | 30.00% |
| A5: 20% auto market share | $500 billion | 40.00% |
| A6: Direct input (chosen) | — | 35.00% |

Profitability lever (target operating margin from 2025 on):

| Choice | Target margin |
|---|---|
| B1: Auto industry first quartile | −5.87% |
| B2: Auto industry median | 3.01% |
| B3: Auto industry third quartile | 7.52% |
| B4: Technology median | 10.25% |
| B5: Software | 21.24% |
| B6: FAANG aggregate | 19.87% |
| B7: Direct input (chosen) | 16.00% |

Investment-efficiency lever (sales to invested capital, first 5 years):

| Choice | Sales to capital |
|---|---|
| C1: Auto industry first quartile | 0.75 |
| C2: Auto industry median | 1.37 |
| C3: Auto industry third quartile | 2.42 |
| C4: Technology median | 1.51 |
| C5: Software | 2.30 |
| C6: FAANG aggregate | 1.27 |
| C7: Direct input (chosen) | 4.00 |

Risk lever (initial cost of capital):

| Choice | Initial cost of capital |
|---|---|
| D1: Automobile median | 5.24% |
| D2: Technology median | 7.16% |
| D3: All companies, first quartile | 4.57% |
| D4: All companies, median | 5.90% (5.88% in the workbook) |
| D5: All companies, third quartile | 7.01% |
| D6: Direct input (chosen) | 6.00% |

Failure lever:

| Choice | Probability of failure |
|---|---|
| E1: No chance | 0% |
| E2: Marginal profitability, high debt | 10% |
| E3: Money loser, high debt | 20% |
| E4: Low growth, money loser, high debt | 50% |

Terminal-phase defaults, each overridable:
- Terminal cost of capital drifts to a mature company's, set as riskfree rate + 4.5%.
- Terminal return on capital equals the terminal cost of capital, so no excess returns.
- No chance of failure.
- The effective tax rate migrates to the marginal rate by the terminal year.
- No NOL carried forward.
- Perpetual growth equals the riskfree rate.
- No trapped foreign cash and no extra tax liability on cash.

**Worked example:** Tesla, November 2021. Levers chosen: growth 35%, target margin 16% reached in year 5, sales-to-capital 4.00 for years 1–5 then 2.67 for years 6–10, initial cost of capital 6.00%, failure probability 0%. Two defaults overridden: terminal return on capital set to 15% against a terminal cost of capital of 6.06%, justified by "cost of entry will limit competition". Story links, row by row:
- Revenue growth ← growth in the EV market plus Tesla's early-mover advantage.
- Margin ← continued economies of scale and brand.
- Tax rate ← the global tax rate.
- Reinvestment ← capacity already built, so less reinvestment in the near years.
- Return on capital ← cost of entry will limit competition.
- Cost of capital ← moves to the median company's cost of capital.

Result: value per share $571.29.

**Determinism:**
- DETERMINISTIC: the entire chain once the levers are set. Total market path, share, revenues, margin path, tax path, reinvestment from sales-to-capital, FCFF, discounting, terminal value, failure adjustment, value per share. Also the CAGR implied by any end-state revenue target.
- JUDGMENT: every lever. Market definition and size need industry data and a view on substitution. Share needs a competitive assessment. Margin needs a reference class and a pricing-power view. Sales-to-capital needs industry comparables. Cost of capital needs the market distribution. Failure probability needs the debt load and profitability. Terminal ROC needs a moat argument.

**Pitfalls:**
- Setting a growth rate without checking the dollar revenues it implies.
- Picking a margin far above the industry with no stated source of pricing power.
- Choosing a sales-to-capital ratio far above the industry, which quietly assumes growth is nearly free. Tesla's 4.00 against an auto median of 1.37 is exactly this kind of claim, and it must be argued.
- Obsessing over the discount rate. It is not among the most critical inputs.
- Leaving terminal ROC above terminal cost of capital as an unexamined default, which grants a perpetual moat by accident.
- Mapping one claim to two drivers, which double counts it.

**Sources:**
- valpacket1spr21 p.269
- valpacket1spr20 p.265
- valuationmotleyfool p.3, p.8, p.15, p.16, p.17, p.18, p.19, p.21, p.24
- motley-fool-tesla-xlsx: `Master Inputs` (five levers with VLOOKUP scenario menus D2:E7, D10:E16, D19:E25, D28:E33, D36:E39), `Input sheet` B23-B30 and the override block B40-B61, `Valuation output` rows 2-9 (growth, margin interpolation, tax migration, reinvestment, FCFF)

**Related:** [[story-to-numbers-process]], [[narrative-numbers-bridge]], [[narrative-consistency-checks]], [[tesla-motley-fool-valuation]], [[uber-narrative-valuation]], [[narrative-scenario-grids]]

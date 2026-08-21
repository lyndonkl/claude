# Equity Valuation versus Firm Valuation

**Core idea:** Equity is a residual claim. Equity holders get whatever is left after everyone else is paid, not a contractual amount. There are two routes to its value, and they must not be mixed. The direct route discounts cash flows *to equity* at the cost of equity and produces equity value straight away. The indirect route discounts cash flows *to the firm* at the cost of capital, producing the value of the whole business, then subtracts outstanding debt. With consistent assumptions about cash flows, debt ratios, and risk, both routes give the same equity value. Staying consistent as you move between them is genuinely hard in practice, which is why most valuation errors are consistency errors rather than arithmetic ones.

**Formulas:**
- Direct (equity) route: `Value of equity = Σ_t E(FCFE_t) / (1 + cost of equity)^t`. `FCFE_t` = free cash flow to equity in year t, after operating expenses, interest expenses, net debt payments, and reinvestment.
- Indirect (firm) route: `Value of firm = Σ_t E(FCFF_t) / (1 + cost of capital)^t`, then `Value of equity = Value of firm − Outstanding debt`. `FCFF_t` = cash flow to the firm in year t, after operating expenses and taxes but *before* any debt payments.
- Cost of capital: `Cost of capital = Cost of equity × E/(D+E) + Cost of debt × (1 − tax rate) × D/(D+E)`. `E` and `D` = market values of equity and debt; `Cost of debt` = the rate at which the business can borrow long term *today*; `tax rate` captures the deductibility of interest.
- Consistency identity: `Equity value (direct) = Equity value (indirect)` if and only if the cash flow, debt ratio, and risk assumptions match across the two routes.

**Procedure:**
1. Pick the route. Use the firm route when the debt ratio is expected to change, or when leverage is heavy enough to make equity cash flows volatile. Use the equity route when the firm is a stable dividend payer or a financial institution where debt is raw material rather than financing.
2. Fix the four determinants of DCF value, and fix all four on the same route. They are: the cash flows, the expected growth rate, the length of the high growth period, and the discount rate.
3. Match the cash flow definition to the route. Firm route: pre-debt cash flows. Equity route: after-debt cash flows.
4. Match the growth measure to the route. Firm route: growth in operating earnings. Equity route: growth in net income or earnings per share.
5. Match the discount rate to the route. Firm route: cost of capital. Equity route: cost of equity.
6. Build the cost of capital from market values, not book values, and use today's long-term borrowing rate for the cost of debt. A historical coupon rate on old debt is the wrong number.
7. Forecast explicit cash flows through the high-growth period, from year 1 to year n. After year n the firm is in stable growth, growing at a constant rate forever, and that stage is captured in a terminal value.
8. Discount everything at the matched rate and sum. On the firm route, subtract outstanding debt at the end to reach equity value.
9. Run the consistency test if you have time. Value the same business both ways. A material gap means an assumption is out of alignment somewhere, and it is worth finding.

**Reference data:**

| Determinant | Firm valuation | Equity valuation |
|---|---|---|
| Cash flows | Pre-debt cash flow (FCFF), after operating expenses, taxes, and reinvestment | After-debt cash flow (FCFE or dividends), after interest and net debt payments |
| Expected growth | Growth in operating earnings | Growth in net income or EPS |
| High growth period | CF₁ through CFₙ forecast explicitly, then stable growth forever in a terminal value | Same structure |
| Discount rate | Cost of capital | Cost of equity |
| Output | Value of the entire firm, all claims | Value of equity claims only |
| Adjustment to reach equity | Subtract outstanding debt | None needed |

| Cost of capital input | What to use |
|---|---|
| Cost of equity | Riskfree rate + beta × equity risk premium, using the marginal investor's perspective |
| Cost of debt | Today's long-term borrowing rate, pre-tax, then multiplied by `(1 − tax rate)` |
| Weights | Market values of debt and equity, not book values |

**Worked example:** Suppose a firm has an 8% cost of equity, a 5% pre-tax cost of debt, a 25% tax rate, $600m of equity at market value and $400m of debt.

`Cost of capital = 0.08 × 600/1000 + 0.05 × (1 − 0.25) × 400/1000`
`= 0.048 + 0.0375 × 0.4 = 0.048 + 0.015 = 6.3%`

Now value the same business both ways in a simple stable-growth case. FCFF next year is $75m growing at 2% forever. Firm route: `Value of firm = 75 / (0.063 − 0.02) = $1,744m`, and `Equity value = 1744 − 400 = $1,344m`. For the equity route to agree, the FCFE must be the FCFF less after-tax interest and net debt repayment, and the growth and risk assumptions must line up. If the equity route gives a materially different number, one of those three has drifted.

**Determinism:**
- DETERMINISTIC: the cost of capital, given component costs, tax rate, and weights. The present value sums, given cash flows and rates. Firm value minus debt. FCFE, given operating cash flow, interest expense, new debt issued, debt repaid, and reinvestment.
- JUDGMENT: forecasting the cash flows and the growth rate. Setting the length of the high growth period. Estimating the cost of equity and the cost of debt. Choosing the debt ratio to use in the weights, especially if it is expected to change. Deciding which route fits the business. These need the financial statements, the firm's competitive position, its credit profile, and the market values of its securities.

**Pitfalls:**
- Discounting after-debt cash flows at the cost of capital, or pre-debt cash flows at the cost of equity. This is the classic mismatch, and it changes the answer by the full value of the debt.
- Subtracting debt after an equity-route valuation. The equity route already nets debt out through the cash flows; subtracting again double-counts it.
- Using book values for the debt and equity weights in the cost of capital.
- Using the historical coupon rate on existing debt as the cost of debt instead of today's borrowing rate.
- Forgetting the tax shield, or applying it to the cost of equity as well as the cost of debt.
- Mixing growth measures — applying operating-earnings growth to equity cash flows, for instance.
- Expecting the two routes to agree without checking that the debt ratio implied by the equity route's cash flows matches the weights used in the cost of capital.

**Sources:**
- `foundations_of_finance--valuing_equity p.2-4, p.8-12`

**Related:** [[stable-growth-equity-valuation]], [[cost-of-capital]], [[marginal-investor-and-beta]], [[present-value-of-the-five-cash-flow-types]], [[terminal-value]], [[finance-first-principles]], [[fcff-vs-fcfe]]

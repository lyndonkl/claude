# Cost of Equity and Cost of Capital

**Core idea:** The cost of equity is the return equity investors demand for holding the stock. It must reflect the risk *they* see, so higher perceived risk means a higher cost of equity. Different investors in the same business will have different costs of equity, and the one that belongs in a valuation is the marginal investor's. The cost of capital widens the lens to every provider of capital. It is a weighted average of the cost of equity and the after-tax cost of borrowing, weighted by how much of each the business actually uses. Two details do most of the damage when they go wrong: the cost of debt must be today's long-term borrowing rate rather than a historical coupon, and the weights must be market values rather than book values.

**Formulas:**
- Cost of equity (CAPM form): `Cost of equity = Riskfree rate + β × Equity risk premium`. `β` = the stock's beta as seen by a diversified marginal investor.
- Cost of capital: `Cost of capital = Cost of equity × E/(D+E) + Cost of debt × (1 − t) × D/(D+E)`. `E` = market value of equity; `D` = market value of debt; `Cost of debt` = the rate at which the business can borrow long term today, pre-tax; `t` = the marginal tax rate, capturing the deductibility of interest.
- After-tax cost of debt: `Cost of debt × (1 − t)`. The tax shield applies only to debt, never to equity.
- Cost of debt from a rating: `Cost of debt = Riskfree rate + Default spread for the firm's rating`.

**Procedure:**
1. Identify the marginal investor and confirm they are diversified. That determines whether only market risk is priced.
2. Estimate the cost of equity from the riskfree rate in the currency of the cash flows, the stock's beta, and the equity risk premium for the markets the firm operates in.
3. Estimate the pre-tax cost of debt as today's long-term borrowing rate. If the firm has traded bonds, use their yield to maturity. If not, add a rating-based default spread to the riskfree rate.
4. Apply the marginal tax rate, not the effective rate, to get the after-tax cost of debt. Only debt gets this treatment.
5. Compute the weights from market values. Market capitalization for equity; the market value of debt, or an estimate of it from the interest expense and average maturity, for debt.
6. Combine into the weighted average.
7. Keep the currency consistent. A cost of capital built on a US dollar riskfree rate belongs with dollar cash flows.
8. Reconcile with the route you are valuing on. Cost of capital pairs with pre-debt cash flows and gives firm value; cost of equity pairs with after-debt cash flows and gives equity value.

**Reference data:**

| Component | Correct input | Common wrong input |
|---|---|---|
| Cost of equity | Riskfree rate + β × equity risk premium, marginal investor's view | Historical average return on the stock |
| Cost of debt | Today's long-term borrowing rate, pre-tax | The coupon rate on existing debt |
| Tax adjustment | Marginal tax rate applied to debt only | Effective tax rate; or applying the shield to equity |
| Weights | Market values of debt and equity | Book values from the balance sheet |

**Worked example:** A firm has a cost of equity of 8%, a pre-tax cost of debt of 5%, a 25% marginal tax rate, $600m of equity at market value and $400m of debt at market value.

`E/(D+E) = 600/1000 = 0.60`, `D/(D+E) = 400/1000 = 0.40`
`After-tax cost of debt = 5% × (1 − 0.25) = 3.75%`
`Cost of capital = 8% × 0.60 + 3.75% × 0.40 = 4.80% + 1.50% = 6.30%`

The 8% cost of equity here is the same rate used to value Consolidated Edison's equity directly, at `$4.00 × 1.02 / (0.08 − 0.02) = $68.00` per share. The 6.30% cost of capital is the rate you would instead use on pre-debt cash flows, before subtracting the $400m of debt to reach equity value.

**Determinism:**
- DETERMINISTIC: the cost of capital, given the component costs, the tax rate, and the market-value weights. The after-tax cost of debt. The cost of equity, given a riskfree rate, a beta, and an equity risk premium.
- JUDGMENT: the beta and the equity risk premium. The marginal tax rate. Whether the firm's current debt ratio is the right one to use going forward, or whether it should trend toward a target. The market value of debt when the debt is not traded. Whether the marginal investor is diversified at all. These need the firm's financials, its credit profile, its shareholder register, and the risk premiums for the markets it operates in.

**Pitfalls:**
- Using the historical coupon on outstanding debt as the cost of debt. Borrowing costs are current market rates.
- Using book value weights. Book equity in particular bears no relation to market equity for most firms.
- Applying the effective tax rate rather than the marginal rate to the interest tax shield.
- Building a cost of capital in one currency and applying it to cash flows in another.
- Assuming the current debt ratio persists forever when the firm has announced a different target.
- Pairing the cost of capital with equity cash flows, which overstates equity value substantially.

**Sources:**
- `foundations_of_finance--valuing_equity p.5, p.10`

**Related:** [[equity-vs-firm-valuation]], [[marginal-investor-and-beta]], [[default-risk-and-default-spreads]], [[currency-consistent-valuation]], [[stable-growth-equity-valuation]], [[equity-risk-premium]], [[bottom-up-beta]]

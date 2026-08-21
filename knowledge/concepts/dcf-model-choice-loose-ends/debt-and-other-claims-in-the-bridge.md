# Subtracting debt and other claims on the way to equity value

**Core idea:** Getting from firm value to equity value means subtracting every claim that ranks ahead of common stock. Three questions decide the number. First, book or market value of debt? For a going concern the answer is market value, because the debt could be retired at its traded price. In liquidation the answer flips: creditors are owed face value. Second, what about obligations that are not debt for cost-of-capital purposes? Underfunded pension and health-care plans are subtracted here, once, and never also counted as cost-of-capital debt. Third, what about claims that may or may not materialize? Contingent liabilities enter at expected value, not at their headline amount.

**Formulas:**
- Going concern: `Value of Equity = Enterprise Value − Market Value of Debt − Other claims`.
- Liquidation: `Value of Equity = Liquidation Value of Assets − Face Value of Debt`.
- Market value of debt when it is not traded: `MV Debt = Interest Expense × [1 − (1 + k_d)^{−n}]/k_d + Face Value/(1 + k_d)^n`, treating total debt as one coupon bond with weighted-average maturity n and current pre-tax cost of debt k_d.
- Contingent liability: `Value = Probability the liability occurs × Expected size of the liability if it occurs`.
- Minority interest: subtract the estimated market value of the stake in consolidated subsidiaries you do not own (see [[cross-holdings]]).

**Reference data — what to subtract and how:**

| Claim | Basis | Notes |
|---|---|---|
| Interest-bearing debt and leases | Market value (going concern) | Face value if you are valuing a liquidation |
| Underfunded pension plans | Amount of the underfunding | Subtract once, in the bridge only |
| Underfunded health-care obligations | Amount of the underfunding | Same |
| Contingent liabilities (lawsuits, guarantees, environmental) | Probability × expected size | Not the plaintiff's claimed amount |
| Minority interests | Estimated market value of the outside stake | Book value is a poor proxy |

Double-counting rules, stated explicitly: do **not** also include a cash-flow line item for cash set aside to fund the pension shortfall; do **not** also count pension or health-care obligations as debt in the cost of capital.

**Procedure:**
1. Take the total debt figure from [[defining-debt-for-cost-of-capital]].
2. Convert it to market value. Use traded prices where they exist. Otherwise treat total debt as one coupon bond and discount at the current pre-tax cost of debt.
3. Decide the frame. Going concern → subtract market value. Immediate liquidation → value the assets at liquidation value and subtract face value of debt.
4. Read the pension and other post-employment benefit footnotes. Subtract any underfunding at the bridge stage, and check you have not also embedded it in cash flows or in the WACC.
5. Identify contingent liabilities from the legal and commitments notes. Estimate a probability and a size for each, and subtract the product.
6. Subtract the value of minority interests if your firm value came from consolidated statements.
7. Verify no claim has been counted twice, and none has been left out.

**Worked example (distressed telecom):** A DCF gives an enterprise value of **$1 billion**. The firm has **$1 billion face value** of debt, trading at **50% of face**, so the market value of debt is $500 million.
- Going concern: equity = 1,000 − 500 = **$500 million**. The market-value answer is right because the debt could effectively be retired at its traded price.
- Now suppose the liquidation value of the assets today is $1.2 billion and you intend to liquidate immediately. In liquidation, debt must be paid at face. Equity = 1,200 − 1,000 = **$200 million**.
Same firm, same debt, two frames, and a $300 million difference. The choice of frame is a judgment about whether the business continues.

**Second example (Heineken, September 2019, € millions):** operating assets are 51,691.19. The bridge subtracts **debt 19,709.52** and **minority interests 1,069.00**. It adds cash 1,751.60 and non-operating assets 1,401.00. Equity is 34,065.26. The minority-interest line alone is 3% of that.

**Determinism:**
- DETERMINISTIC: the subtraction arithmetic; the market value of debt given interest expense, maturity and the cost of debt; the expected value of a contingent liability given probability and size.
- JUDGMENT: whether the firm is a going concern or a liquidation candidate; the probability and magnitude of contingent liabilities; the market value of minority interests; the weighted-average maturity to use for non-traded debt. This needs the legal notes, credit market data, and a view on distress.

**Pitfalls:**
- Subtracting book debt from a market-based enterprise value, which flatters equity for a distressed firm and penalizes it for a firm whose debt trades above par.
- Using the market value of debt for a firm you are actually valuing in liquidation. Creditors get face value first.
- Counting pension underfunding as debt in the WACC and subtracting it again in the bridge.
- Subtracting the headline amount of a lawsuit rather than its probability-weighted expected value.
- Forgetting minority interests entirely after a consolidated DCF.

**Sources:**
- valpacket1spr21 p.240-241
- valpacket1spr20 p.236-237
- valpacket1spr21 p.203 (Heineken bridge: debt and minority interests)

**Related:** [[defining-debt-for-cost-of-capital]], [[equity-value-bridge]], [[cross-holdings]], [[other-non-operating-assets]], [[distressed-firm-valuation]], [[employee-option-per-share-approaches]]

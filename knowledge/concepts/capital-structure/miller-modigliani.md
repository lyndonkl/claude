# Miller-Modigliani: when capital structure is irrelevant

**Core idea:** Strip away every item in the debt trade-off and the financing mix stops mattering. Assume no taxes, no bankruptcy, managers who act for stockholders, honest dealing with lenders, and firms that know their future financing needs. In that world firm value comes from the quality of investments alone, and the cost of capital does not change with leverage. As leverage rises the cost of equity rises exactly enough to offset the substitution of cheaper debt for expensive equity. The theorem matters not as a description of reality but as a diagnostic: whenever a change in leverage moves value, you should be able to name which MM assumption it violates.

**Formulas:**
- MM proposition in cost-of-capital form: `Cost of capital = ke × E/(D+E) + kd × (1−t) × D/(D+E)` is invariant to D/(D+E) when t = 0 and default risk is unpriced.
- The offsetting mechanism is the levered-beta relation: `β_L = β_u × (1 + (1 − t) × D/E)`. With t = 0, `β_L = β_u × (1 + D/E)`, so the cost of equity rises linearly in D/E and exactly cancels the weight shift toward debt.

**Procedure:** Use MM as a checklist when someone claims a financing action creates value.
1. Ask which assumption is being violated. Taxes? Default risk / bankruptcy costs? Manager-stockholder agency? Lender-stockholder agency? Uncertainty about future financing needs?
2. If none is violated, the claimed gain is a transfer, not value creation.
3. If one is violated, quantify it through the corresponding channel: the tax benefit through the after-tax cost of debt ([[tax-benefit-of-debt]]), default risk through the synthetic rating ([[synthetic-rating-and-cost-of-debt]]), distress effects on operations through the enhanced approach ([[enhanced-cost-of-capital-approach]]), and direct/indirect bankruptcy costs through APV ([[apv-approach]]).
4. Remember the shape MM predicts: in the MM world, the cost of equity rises with leverage, the cost of debt rises as default risk increases, and the cost of capital stays flat. The real-world U-shape comes entirely from the tax benefit on the way down and from ratings deterioration plus the tax cap on the way up.

**Reference data:** The five conditions of the MM world, as taught: (a) no taxes; (b) managers have stockholder interests at heart; (c) no firm ever goes bankrupt; (d) equity investors are honest with lenders — no subterfuge, no loophole-hunting in loan agreements; (e) firms know their future financing needs with certainty.

**Worked example:** Take a firm with unlevered beta 0.90, riskfree rate 2.75%, ERP 5.76%, pre-tax cost of debt equal to the riskfree rate (no default risk), and no taxes. At 0% debt: ke = 2.75% + 0.90 × 5.76% = 7.93%; WACC = 7.93%. At 50% debt, D/E = 1.0 so β_L = 0.90 × 2 = 1.80, ke = 2.75% + 1.80 × 5.76% = 13.12%; WACC = 13.12% × 0.5 + 2.75% × 0.5 = 7.93%. Unchanged, as MM requires. Reintroduce a 36.1% tax rate and the same 50% mix gives β_L = 0.90 × (1 + 0.639) = 1.475, ke = 11.25%, WACC = 11.25% × 0.5 + 2.75% × 0.639 × 0.5 = 6.50% — the entire drop is the tax shield.

**Determinism:**
- DETERMINISTIC: verifying invariance numerically, given an unlevered beta, riskfree rate, ERP and a zero-tax, zero-default assumption.
- JUDGMENT: deciding which MM assumption a real financing decision violates and how much each violation is worth.

**Pitfalls:**
- Quoting MM as proof that capital structure does not matter in practice. Its assumptions are exactly the list of things that make debt matter.
- Forgetting that under MM the cost of *debt* also rises with leverage; only the weighted average stays flat.
- Assuming irrelevance implies indifference about the *kind* of debt. Even in an MM world, matching debt to asset cash flows still reduces default risk ([[debt-design-framework]]).

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.28-29

**Related:** [[debt-equity-tradeoff]], [[cost-of-capital-approach]], [[levered-beta-schedule]], [[tax-benefit-of-debt]], [[pecking-order]]

# Defining debt for cost of capital purposes

**Core idea:** "Debt" in a valuation is not whatever the balance sheet labels as a liability. It is defined by three characteristics, and a liability must have all three. There is a commitment to make fixed payments in the future. Those payments are tax deductible. Failure to make them can trigger default or hand control of the firm to the party owed. Apply that test and the boundary is clear: all interest-bearing liabilities count, short-term and long-term, and so do all leases, operating as well as capital. Accounts payable and supplier credit do not. The common error runs one way — analysts feel prudent counting everything as debt, which inflates the debt ratio and *understates* the cost of capital, since debt is the cheaper component.

**Formulas:**
- Three-part test: `Debt = liability with (fixed commitment) AND (tax-deductible payments) AND (default or loss-of-control consequence)`.
- `Total debt = Short-term interest-bearing debt + Long-term interest-bearing debt + Present value of all lease commitments`.
- Lease capitalization: `Debt value of leases = Σ_t Lease Commitment_t / (1 + pre-tax cost of debt)^t`.
- `Debt ratio = Market value of debt / (Market value of debt + Market value of equity)`.
- `WACC = k_e × E/(D+E) + k_d(1 − t) × D/(D+E)`.

**Reference data — the classification:**

| Item | Debt for cost of capital? | Reason |
|---|---|---|
| Short-term interest-bearing debt (notes, commercial paper, revolver draws) | Yes | Fixed, deductible, default consequence |
| Long-term interest-bearing debt (bonds, term loans) | Yes | Same |
| Capital (finance) leases | Yes | Already treated as debt in accounting |
| Operating leases | Yes | Economically identical to a secured loan |
| Accounts payable | No | No explicit interest, no default-to-control consequence |
| Supplier credit | No | Same |
| Underfunded pension / health-care obligations | No — handle in the bridge | Subtract from firm value instead ([[debt-and-other-claims-in-the-bridge]]) |
| Contingent liabilities | No — handle in the bridge | Subtract expected value instead |

**Procedure:**
1. Pull every liability from the balance sheet and the commitment footnotes.
2. Run the three-part test on each. All three conditions must hold.
3. Capitalize all lease commitments at the pre-tax cost of debt and add the result to debt. Also adjust operating income upward by the imputed interest portion, so the leases are treated consistently on both sides.
4. Exclude accounts payable and supplier credit.
5. Exclude pension underfunding and contingent liabilities from the cost-of-capital debt figure. They belong in the equity bridge, and counting them twice is the most common double count in this step.
6. Convert debt to market value for the weights (see [[debt-and-other-claims-in-the-bridge]]).
7. Compute the debt ratio and the WACC. Sanity-check the ratio against the sector average; a wild outlier usually means a classification error.

**Worked example (3M, September 2008):** the cost of capital is built from a debt ratio of 8% — interest-bearing debt only, not the full liability side of the balance sheet. Cost of equity = 3.72% + 1.15 × 4% = **8.32%**, with the beta relevered at a D/E of 8.8%. Pre-tax cost of debt = riskfree 3.72% + default spread 0.75% = 4.47%; after tax at 35%, `k_d = 2.91%`. `Cost of capital = 8.32%(0.92) + 2.91%(0.08) = 7.88%`. Suppose payables had been swept into debt. The debt ratio would jump, the WACC would fall toward the after-tax cost of debt, and firm value would be overstated. That is exactly the bias the "count everything as debt" instinct produces.

**Determinism:**
- DETERMINISTIC: the classification given each liability's characteristics; lease capitalization given commitments and a discount rate; the debt ratio and WACC given market values.
- JUDGMENT: the pre-tax cost of debt used to capitalize leases; how to treat hybrid securities such as convertibles and preferred stock (split convertibles into straight-debt and conversion-option components); whether an off-balance-sheet arrangement carries a real fixed commitment. This needs the debt footnotes, lease schedules and rating information.

**Pitfalls:**
- Counting accounts payable as debt "to be conservative". It is not conservative; it lowers your WACC and raises your value.
- Leaving operating leases out of debt, which understates leverage for retailers, restaurants and airlines.
- Counting pension underfunding both as debt in the WACC and as a subtraction in the equity bridge.
- Using the book debt ratio for the WACC weights when market values are available.
- Forgetting to adjust operating income after capitalizing leases, which leaves the numerator and denominator inconsistent.

**Sources:**
- valpacket1spr21 p.239
- valpacket1spr20 p.235
- valpacket1spr20 p.278 (3M cost-of-capital build)

**Related:** [[debt-and-other-claims-in-the-bridge]], [[equity-versus-firm-valuation]], [[equity-value-bridge]], [[cost-of-capital]], [[operating-lease-capitalization]], [[synthetic-rating]], [[cash-in-valuation]]

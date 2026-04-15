---
name: capital-structure-optimizer
description: Analyzes a company's debt-equity mix and determines the optimal capital structure that minimizes WACC. Computes WACC at each debt ratio from 0% to 90%, identifies the minimum, and recommends whether to add or reduce debt with specific debt type matching (maturity, currency, fixed vs floating). Use when analyzing capital structure, optimizing debt levels, evaluating leverage, or when user mentions optimal debt ratio, capital structure, leverage optimization, debt capacity, or recapitalization.
---
# Capital Structure Optimizer

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Manufacturing company, EBIT $300M, current debt ratio 20%, unlevered beta 0.9, riskfree rate 4%, ERP 5.5%, marginal tax rate 25%.

**Current state**:
- Current D/E = 20/80 = 0.25
- Levered beta = 0.9 x (1 + (1 - 0.25) x 0.25) = 1.069
- Cost of equity = 4% + 1.069 x 5.5% = 9.88%
- Interest coverage at 20% debt: high, rating AA, spread 1.00%
- Cost of debt = 4% + 1.00% = 5.00%, after-tax = 3.75%
- WACC = 9.88% x 0.80 + 3.75% x 0.20 = **8.65%**

**WACC schedule**:

| Debt Ratio | D/E   | Levered Beta | Cost of Equity | Rating | Spread | Cost of Debt (AT) | WACC     |
|------------|-------|-------------|----------------|--------|--------|--------------------|----------|
| 0%         | 0.00  | 0.900       | 8.95%          | --     | --     | --                 | 8.95%    |
| 10%        | 0.11  | 0.974       | 9.36%          | AAA    | 0.75%  | 3.56%              | 8.78%    |
| 20%        | 0.25  | 1.069       | 9.88%          | AA     | 1.00%  | 3.75%              | 8.65%    |
| 30%        | 0.43  | 1.189       | 10.54%         | A+     | 1.25%  | 3.94%              | 8.56%    |
| 40%        | 0.67  | 1.350       | 11.43%         | BBB    | 2.00%  | 4.50%              | 8.66%    |
| 50%        | 1.00  | 1.575       | 12.66%         | BB     | 3.50%  | 5.63%              | 9.14%    |
| 60%        | 1.50  | 1.913       | 14.52%         | B-     | 6.00%  | 7.50%              | 10.31%   |

**Optimal**: 30% debt ratio, WACC 8.56% (vs current 8.65% at 20%).

**Value enhancement**:
- Current firm value = $300M x (1 - 0.25) / 0.0865 = $2,601M
- Optimal firm value = $225M / 0.0856 = $2,628M
- Value gain: ~$27M

**Debt type recommendation**: Issue 10-year fixed-rate USD bonds (85% US revenue, long-lived manufacturing assets, stable cash flows favor fixed rate). Move from 20% to 30% debt gradually over 12-18 months.

## Workflow

Copy this checklist and track your progress:

```
Capital Structure Optimization Progress:
- [ ] Step 1: Establish current capital structure and cost of capital
- [ ] Step 2: Compute unlevered beta
- [ ] Step 3: Build WACC schedule across debt ratios (0-90%)
- [ ] Step 4: Identify optimal debt ratio
- [ ] Step 5: Determine appropriate debt type
- [ ] Step 6: Develop implementation path
```

**Step 1: Establish current capital structure and cost of capital**

Gather current debt level (market value), equity market value, EBIT, interest expense, marginal tax rate, riskfree rate, ERP, and current beta. See [resources/template.md](resources/template.md#current-capital-structure-inputs) for input template.

**Step 2: Compute unlevered beta**

Strip leverage effect from current equity beta to isolate business risk. Unlevered beta = Levered beta / (1 + (1 - t)(D/E)). See [resources/methodology.md](resources/methodology.md#unlevering-beta) for procedure and peer-based alternative.

**Step 3: Build WACC schedule across debt ratios (0-90%)**

For each debt ratio in 10% increments: relever beta, compute cost of equity, compute interest expense and interest coverage, look up synthetic rating, determine default spread and cost of debt, compute WACC. See [resources/template.md](resources/template.md#wacc-schedule-table) for the complete table template and [resources/methodology.md](resources/methodology.md#cost-of-capital-approach) for step-by-step mechanics.

**Step 4: Identify optimal debt ratio**

Find the debt ratio where WACC is minimized. Calculate value enhancement from moving to optimal. Compare optimal to industry average debt ratio as a reasonableness check. See [resources/methodology.md](resources/methodology.md#interpreting-the-optimal) for interpretation guidance.

**Step 5: Determine appropriate debt type**

Match debt characteristics to the company's asset and cash flow profile. Maturity should match asset duration, currency should match revenue currency, and fixed vs floating should match cash flow sensitivity. See [resources/methodology.md](resources/methodology.md#debt-type-matching) for matching criteria and [resources/template.md](resources/template.md#debt-type-matching-worksheet) for the matching worksheet.

**Step 6: Develop implementation path**

Choose between gradual adjustment (1-2 years) and immediate recapitalization (leveraged recap). Consider market conditions, company situation, and urgency. See [resources/template.md](resources/template.md#implementation-path-template) for gradual vs immediate frameworks. Validate using [resources/evaluators/rubric_capital_structure_optimizer.json](resources/evaluators/rubric_capital_structure_optimizer.json). Minimum standard: Average score of 3.5 or higher.

## Common Patterns

**Pattern 1: Under-Levered Company**
- **Diagnosis**: Current debt ratio well below optimal (by 10%+ of capital)
- **Typical profile**: Mature company with stable cash flows, high interest coverage, strong credit rating, accumulated cash
- **Action**: Issue debt and repurchase shares (or pay special dividend). Value increases because lower WACC raises present value of cash flows
- **Debt type**: Match to asset profile. Stable companies with long-lived assets favor long-term fixed-rate bonds
- **Implementation**: Can be gradual (annual debt issuance over 2-3 years) or immediate (leveraged recapitalization if large gap)
- **Example**: Tech company with no debt, WACC 10.5%. Optimal at 20% debt, WACC 9.2%. Issue bonds, repurchase shares

**Pattern 2: Over-Levered Company**
- **Diagnosis**: Current debt ratio above optimal, interest coverage thin, rating below investment grade
- **Typical profile**: Company post-acquisition, cyclical firm that added debt during boom, or firm facing industry decline
- **Action**: Reduce debt through asset sales, equity issuance, or retained earnings. Prioritize debt reduction when rating is below BBB
- **Debt type**: Focus on repaying highest-cost debt first. Renegotiate covenants if possible
- **Implementation**: Gradual through cash flow application to debt paydown. Equity issuance only as last resort (signals distress)
- **Example**: Retail company at 60% debt, rating B+. Optimal at 30%. Sell non-core assets, apply FCFE to debt reduction

**Pattern 3: Near-Optimal Company**
- **Diagnosis**: Current debt ratio within 5 percentage points of optimal. WACC difference less than 20 basis points
- **Typical profile**: Well-managed company that has already optimized, or company where WACC curve is flat near minimum
- **Action**: No restructuring needed. Focus on debt type matching and refinancing opportunities
- **Debt type**: Audit existing debt against matching criteria (maturity, currency, rate structure). Refinance mismatched debt
- **Implementation**: Opportunistic refinancing when market conditions are favorable
- **Example**: Industrial company at 25% debt, optimal at 30%. WACC difference 10 bps. Focus on refinancing near-term maturities to better match asset profile

## Guardrails

1. **Beta increases with leverage**: As debt rises, equity beta increases because equity holders bear more risk. At high debt ratios (60%+), beta increases rapidly and the cost of equity dominates, causing WACC to rise even as after-tax debt costs remain moderate.

2. **Synthetic rating drives cost of debt**: Interest coverage ratio determines the synthetic credit rating. At very low coverage (below 1.5x), default spreads jump significantly. Ensure the rating lookup uses the appropriate table for the company's size (large-cap vs small-cap firms have different spread schedules).

3. **Use marginal tax rate for the tax shield**: The tax benefit of debt depends on the marginal rate the company will pay on additional income, not the effective rate it pays on current income. If the company has large NOLs or is in a loss position, the tax shield may be reduced or eliminated.

4. **Debt type should match the asset and cash flow profile**: Match maturity to asset duration (long-lived assets warrant long-term debt), currency to the primary revenue currency (reduces exchange rate risk), and fixed vs floating to cash flow cyclicality (stable cash flows can support fixed-rate debt; cyclical cash flows may benefit from floating).

5. **Implementation pace depends on urgency and market conditions**: Gradual adjustment (1-2 years) is appropriate when the gap is moderate and markets are stable. Immediate recapitalization (leveraged recap) is appropriate when the gap is large and interest rates are favorable. Consider transaction costs and market signaling effects.

6. **Compare to industry average as a sanity check**: The optimal ratio should not be wildly different from industry norms without a clear reason. If the model suggests 50% debt for a tech company (industry average 10%), revisit assumptions.

7. **Consider indirect bankruptcy costs**: For companies where customer trust, employee retention, or supplier relationships are critical (airlines, warranty-dependent manufacturers, professional services), indirect costs of financial distress may exceed the direct costs. These firms should target a debt ratio below the pure WACC minimum.

## Quick Reference

**Key formulas:**

```
Debt to Capital Ratio = D / (D + E)
Debt to Equity Ratio = D / E

Unlevered Beta = Levered Beta / (1 + (1 - t) x (D/E))

Levered Beta = Unlevered Beta x (1 + (1 - t) x (D/E))

Cost of Equity = Riskfree Rate + Levered Beta x ERP

Interest Coverage = EBIT / Interest Expense

Cost of Debt (pre-tax) = Riskfree Rate + Default Spread (from synthetic rating)
Cost of Debt (after-tax) = Cost of Debt (pre-tax) x (1 - t)

WACC = ke x (E / (D+E)) + kd x (1 - t) x (D / (D+E))

Value Enhancement = Firm Value at Optimal WACC - Firm Value at Current WACC
                  = EBIT(1-t) / WACC_optimal - EBIT(1-t) / WACC_current
```

**Debt type matching criteria:**

| Dimension         | Match To                        | Rationale                                      |
|-------------------|---------------------------------|-------------------------------------------------|
| Maturity          | Asset duration / life           | Aligns debt service with asset cash generation  |
| Currency          | Revenue currency mix            | Reduces currency mismatch risk                  |
| Rate (fixed/float)| Cash flow stability             | Fixed for stable; floating for cyclical         |
| Seniority         | Collateral availability         | Secured if tangible assets; unsecured otherwise |
| Covenants         | Operational flexibility needs   | Fewer covenants for high-growth firms           |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Current state inputs, WACC schedule table, debt type matching worksheet, implementation path templates
- **[resources/methodology.md](resources/methodology.md)**: Cost of capital approach mechanics, trade-off framework, debt type matching methodology, APV alternative
- **[resources/evaluators/rubric_capital_structure_optimizer.json](resources/evaluators/rubric_capital_structure_optimizer.json)**: Quality rubric for capital structure analysis

**Inputs required:**
- EBIT (operating income)
- Current debt level (market value) and equity market value
- Current equity beta (or unlevered beta from comparable firms)
- Marginal tax rate
- Riskfree rate and equity risk premium
- Revenue breakdown by currency
- Asset duration or average asset life
- Cash flow volatility (for debt type matching)

**Outputs produced:**
- `capital-structure-analysis.md`: WACC schedule across debt ratios, optimal ratio identification, current vs optimal comparison, value enhancement estimate, debt type recommendation, implementation path

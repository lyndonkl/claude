---
name: valuation-reconciler
description: Synthesizes intrinsic (DCF) and relative (multiples) valuation outputs into a final value estimate and investment recommendation. Reconciles divergent valuations, reverse-engineers what the market is pricing in (implied growth, implied ROIC), computes margin of safety, and produces a buy/sell/hold recommendation with catalysts. Use when combining multiple valuation approaches, making investment recommendations, reconciling DCF with multiples, or when user mentions reconcile valuations, investment recommendation, margin of safety, implied growth rate, or what is the market pricing in.
---
# Valuation Reconciler

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: NovaBrands Inc. -- US consumer goods company, current price $65/share

**Valuation inputs**:
- DCF intrinsic value (FCFF two-stage): $85/share
- Relative valuation, PE regression (sector): $78/share
- Relative valuation, EV/EBITDA peer median: $90/share

**Reconciliation table**:

| Method | Value/Share | Key Assumptions | Confidence Weight |
|--------|------------|-----------------|-------------------|
| DCF (FCFF) | $85 | 8% revenue growth, 14% operating margin, 9% WACC | 50% |
| PE Regression | $78 | Sector regression R-squared 0.62, predicted PE 22x | 25% |
| EV/EBITDA Peers | $90 | Median peer 11x, adjusted for higher growth | 25% |

**Weighted estimate**: $85 x 0.50 + $78 x 0.25 + $90 x 0.25 = **$84.50/share**

**Implied analysis** (what the market prices at $65):
- Implied revenue growth: 4% (vs. our narrative's 8%)
- Implied ROIC: 10% (vs. our estimate of 15%)
- The market is pricing NovaBrands as a mature, low-growth consumer staple. Our narrative views it as a growth-stage branded goods company with pricing power.

**Margin of safety**: ($84.50 - $65) / $84.50 = **23%**

**Catalysts**:
1. Restructuring cost savings ($40M annualized) -- expected Q3
2. New product line launch into adjacent category -- expected Q4
3. Potential multiple re-rating if margins expand above 15%

**Recommendation**: Buy at $65, target range $80-$85, 12-month horizon. The 23% margin of safety provides a cushion even if growth reaches only 6% instead of 8%.

**Risk factors**: Private-label competition eroding brand premium; input cost inflation compressing margins; restructuring execution delays.

## Workflow

Copy this checklist and track your progress:

```
Valuation Reconciliation Progress:
- [ ] Step 1: Collect all valuation estimates
- [ ] Step 2: Identify sources of divergence
- [ ] Step 3: Reverse-engineer market implied assumptions
- [ ] Step 4: Assess catalysts for gap closure
- [ ] Step 5: Compute margin of safety and formulate recommendation
- [ ] Step 6: Write investment thesis
```

**Step 1: Collect all valuation estimates**

Gather intrinsic value (DCF), relative valuation estimates (PE, EV/EBITDA, PBV, EV/Sales), and any special-situation adjustments into a single reconciliation table. For each estimate, record the method, per-share value, key assumptions, and a confidence weight reflecting how appropriate that method is for this company type. See [resources/template.md](resources/template.md#reconciliation-table) for the reconciliation table format.

**Step 2: Identify sources of divergence**

Compare the highest and lowest valuations. Trace differences to specific assumptions: growth rate, discount rate, margin, multiple selection, peer universe. If DCF and relative values diverge by more than 20%, document the driver of the gap. See [resources/methodology.md](resources/methodology.md#three-lens-reconciliation-framework) for the divergence analysis framework.

**Step 3: Reverse-engineer market implied assumptions**

Back-solve for the growth rate and ROIC that would make the DCF value equal to the current market price. Compare these implied assumptions against your narrative, historical performance, and industry benchmarks. This reveals what the market is pricing in and where your view differs. See [resources/methodology.md](resources/methodology.md#implied-growth-and-roic-reverse-engineering) for the iterative calculation method.

**Step 4: Assess catalysts for gap closure**

If a value gap exists (intrinsic value differs from market price), identify specific, time-bound events that could cause the gap to close. Catalysts may include earnings reports, product launches, restructuring milestones, regulatory changes, or management actions. Assign estimated timing, value impact, and probability to each catalyst. See [resources/template.md](resources/template.md#catalyst-identification-template) for the catalyst template.

**Step 5: Compute margin of safety and formulate recommendation**

Calculate margin of safety as (intrinsic value - market price) / intrinsic value. Calibrate the required margin based on company characteristics: higher for volatile, unpredictable, or small-cap firms; lower for stable, predictable businesses. Formulate a buy/sell/hold recommendation with a specific price target and time horizon. See [resources/template.md](resources/template.md#recommendation-template) for the recommendation format.

**Step 6: Write investment thesis**

Synthesize the reconciliation into a one-page investment thesis linking business narrative to valuation to recommendation. Include the key risk factors that could invalidate the thesis. See [resources/template.md](resources/template.md#investment-thesis-template) for the thesis format. Validate using [resources/evaluators/rubric_valuation_reconciler.json](resources/evaluators/rubric_valuation_reconciler.json). **Minimum standard**: Average score >= 3.5.

## Common Patterns

**Pattern 1: Value Gap (DCF > Price)**
- **Setup**: Intrinsic value materially exceeds market price; one or more relative valuation methods support undervaluation
- **Implied analysis**: Market is pricing in lower growth, lower margins, or higher risk than your narrative
- **Catalyst requirement**: Identify at least one specific event with estimated timing that could cause re-rating
- **Recommendation**: Buy with stated margin of safety, price target, and time horizon
- **Key risk**: You may be wrong about the narrative; the market may know something you do not
- **Example**: Consumer brand trading at 12x earnings while peers trade at 18x; restructuring catalyst expected within 6 months

**Pattern 2: Overvaluation Signal (DCF < Price)**
- **Setup**: Intrinsic value materially below market price; relative valuation methods confirm richness
- **Implied analysis**: Market is pricing in higher growth or lower risk than your narrative supports
- **Action**: Sell/avoid; document what growth rate or margin the market is assuming and why it is implausible
- **Key risk**: Momentum may persist; short positions carry unlimited downside
- **Example**: Tech company at 80x earnings with implied 30% growth for 10 years; historical base rate for sustaining >25% growth beyond 5 years is below 5%

**Pattern 3: Fair Value / Convergence**
- **Setup**: DCF, relative, and market price all within 10-15% of each other; multiple methods agree
- **Implied analysis**: Market assumptions align with your narrative; no significant mispricing
- **Action**: Hold if owned; no compelling case to initiate position
- **Key risk**: A stable consensus can break quickly on new information
- **Example**: Mature utility with DCF value $52, peer EV/EBITDA implies $50, trading at $49; all methods converge within normal estimation error

## Guardrails

1. **Expect divergence between methods.** Different valuation methods should produce different numbers. If DCF, PE regression, and peer median all yield the same value, the analysis likely contains confirmation bias. Investigate whether assumptions were inadvertently aligned.

2. **Weight the method most appropriate for the company type.** DCF carries more weight for unique businesses with few comparables. Relative valuation carries more weight for commodity businesses in a well-defined peer group. Neither approach alone is sufficient.

3. **Calibrate margin of safety to uncertainty.** A 15% margin of safety may suffice for a stable, predictable utility; a 30-40% margin is appropriate for a volatile, high-growth, or distressed company. The required margin should increase with cash flow volatility, forecast horizon, and complexity.

4. **Validate implied assumptions against plausible ranges.** Reverse-engineered growth rates and ROIC should be compared to the company's own history, industry averages, and base rates. If the market implies 25% growth for a decade, check how many companies in the same industry have actually achieved that.

5. **Require specific, time-bound catalysts.** "The market will eventually recognize value" is not a catalyst. A catalyst has a what, a when, and an estimated impact: "Q3 earnings release showing restructuring savings of $40M, expected October, could close 30% of the value gap."

6. **State a time horizon for the recommendation.** A buy recommendation without a time horizon is incomplete. Specify whether the thesis depends on a 6-month, 12-month, or multi-year holding period, and what changes would trigger a reassessment.

7. **Document risk factors explicitly.** Every thesis must include at least two specific risk factors that could invalidate the recommendation. For buy recommendations, state what would cause you to sell. For sell recommendations, state what would cause you to reverse.

## Quick Reference

**Key formulas:**

```
Margin of Safety = (Intrinsic Value - Market Price) / Intrinsic Value

Value-to-Price Ratio = Intrinsic Value / Market Price

Implied Growth Rate = g such that DCF(g) = Market Price
  (iterate g in DCF model until output equals current price)

Implied ROIC = ROC such that DCF(ROC) = Market Price
  (iterate ROC in DCF model until output equals current price)

EVA Value Decomposition:
  Firm Value = Invested Capital + PV of Future EVA
  where EVA = (ROIC - WACC) x Invested Capital
  Growth premium = Firm Value - Invested Capital

Breakeven Sensitivity:
  What change in [growth / WACC / margin] flips buy to hold?
```

**Recommendation decision framework:**

| Value-to-Price | Margin of Safety | Catalysts | Recommendation |
|----------------|-----------------|-----------|----------------|
| > 1.30 | > 25% | Identified, time-bound | Buy |
| 1.15 - 1.30 | 15-25% | Identified, time-bound | Buy (moderate conviction) |
| 0.85 - 1.15 | < 15% | N/A | Hold / Fair value |
| 0.70 - 0.85 | Negative | Risk factors present | Sell / Avoid |
| < 0.70 | Deeply negative | Risk factors present | Sell (high conviction) |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Reconciliation table, implied assumptions worksheet, catalyst template, recommendation template, investment thesis template
- **[resources/methodology.md](resources/methodology.md)**: Three-lens reconciliation framework, implied growth/ROIC reverse engineering, catalyst analysis, margin of safety calibration, EVA value decomposition
- **[resources/evaluators/rubric_valuation_reconciler.json](resources/evaluators/rubric_valuation_reconciler.json)**: Quality criteria for reconciliation completeness, divergence analysis, catalyst specificity, recommendation clarity

**Inputs required:**

- **Intrinsic value** (from DCF model, per share)
- **Relative valuation estimates** (from peer comparison and/or sector regression, per share)
- **Special-situation adjustments** (if applicable, per share)
- **Current market price** (per share)
- **Key assumption ranges** (growth rate, discount rate, margin, for sensitivity analysis)
- **Business narrative** (from business-narrative-builder, for thesis framing)

**Outputs produced:**

- `valuation-reconciliation.md`: Reconciliation table, implied assumptions, divergence analysis, margin of safety, sensitivity matrix, catalyst assessment, buy/sell/hold recommendation with price target and time horizon, investment thesis, risk factors

**Cross-references to other skills:**

- `intrinsic-valuation-dcf` provides the DCF per-share value and sensitivity grid
- `relative-valuation-multiples` provides peer comparison and regression-implied values
- `special-situations-valuation` provides adjusted values for high-growth, distressed, private, or financial services firms
- `business-narrative-builder` provides the qualitative story that anchors the thesis

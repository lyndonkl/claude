# Pathways to the optimal debt ratio (and how to reconcile them)

**Core idea:** The financing decision has two halves: the right *mix* of debt and equity, and the right *kind* of debt. This note covers the first half's menu. There are five ways to define an optimal debt ratio, and a full analysis runs several and compares. Approach 1 minimizes the cost of capital. Approach 2 jointly optimizes the cost of capital and operating income by building in indirect bankruptcy costs. Approach 3 maximizes firm value directly by adding tax benefits and subtracting expected bankruptcy costs (APV). Approach 4 pushes the firm toward its peer group. Approach 5 asks what fits its life-cycle stage. The first three are intrinsic and can disagree with the last two, because sector and market averages describe practice, not value maximization.

**Formulas:**
- Approach 1: optimal `d* = argmin_d WACC(d)`, valid when cash flows are unaffected by d.
- Approach 2: optimal `d* = argmax_d V(d)` where operating income itself falls as the rating deteriorates.
- Approach 3 (APV): `V(d) = V_unlevered + Tax benefits(d) − Expected bankruptcy cost(d)`, optimal `d* = argmax_d V(d)`.
- Approach 4: `d* ≈ peer group average debt ratio`, adjusted for firm-specific differences, or `d* = predicted value from a cross-sectional regression`.
- Approach 5: `d*` = the ratio typical of the firm's life-cycle stage.

**Procedure:**
1. Start with the cost of capital approach; it needs the fewest extra assumptions ([[cost-of-capital-approach]]).
2. Re-run it with indirect bankruptcy costs to see how steep the penalty for overshooting is ([[enhanced-cost-of-capital-approach]]).
3. Run APV as an independent check on the dollar debt level ([[apv-approach]]).
4. Benchmark against the sector and against a market-wide regression ([[relative-and-regression-analysis]]).
5. Sanity-check against life-cycle stage ([[financing-life-cycle]]).
6. Reconcile. Where intrinsic approaches agree with each other and disagree with comparables, prefer the intrinsic answer but explain the gap — the regression-based number reflects what the average firm does, and average practice is not optimal practice.
7. Deliver the answer as a range plus a direction (under-levered / at the mix / over-levered), then move to the adjustment question ([[moving-to-the-optimal]]).

**Reference data:** Actual vs. optimal debt ratios for the case firms across all five approaches (2013 analyses):

| | Disney | Vale | Tata Motors | Baidu |
|---|---|---|---|---|
| Actual debt ratio | 11.58% | 35.48% | 29.28% | 5.23% |
| I. Operating income approach | 35.00% | — | — | — |
| II. Standard cost of capital | 40.00% | 30% (actual EBIT), 50% (normalized) | 20.00% | 10.00% |
| III. Enhanced cost of capital | 40.00% | 30% (actual), 40% (normalized) | 10.00% | 10.00% |
| IV. APV | 40.00% | 30.00% | 20.00% | 20.00% |
| V. Comparable — to industry | 28.54% | 26.03% | 18.72% | 1.83% |
| V. Comparable — to market regression | 18.86% | — | — | — |

Where this sits in the first-principles framework: the objective is to maximize the value of the business. The investment decision invests in assets earning more than a hurdle rate that reflects both risk and the debt/equity mix. The financing decision finds the right kind of debt and the right mix — the optimal mix maximizes firm value, and the right kind of debt matches the tenor of the assets. The dividend decision returns cash when no investment clears the hurdle rate.

**Worked example:** Disney. The cost of capital approach and the enhanced approach both give 40%; APV gives 40%; the industry comparison gives 28.54%; the market-wide regression gives 18.86%. Actual is 11.58%. Every method says under-levered, and the intrinsic methods agree tightly on 40%. The comparables are lower because US entertainment firms as a group are themselves conservatively financed (market D/C 15.44%). The recommendation is driven by the intrinsic number, with the comparables noting that a move to 40% would put Disney well above its peers.

**Determinism:**
- DETERMINISTIC: running each approach once its inputs are fixed, and assembling the comparison table.
- JUDGMENT: which approach to weight when they disagree; whether the peer group is well defined; whether the firm's operating income should be normalized before any of them are run.

**Pitfalls:**
- Reporting a single optimal number with false precision. The debt-ratio grid is in 10% steps and the inputs are noisy; the answer is a range.
- Treating the regression or industry number as an optimum. It is a description of average behavior with an R-squared as low as 8% market-wide.
- Running only the standard cost of capital approach on a firm where distress would visibly damage operations.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.3
- corporate_finance--lecture_slides--cfpacket2spr20 p.35-36
- corporate_finance--lecture_slides--cfpacket2spr20 p.87 (application test: estimate the optimal ratio, the new cost of capital, the value effect and the price effect)
- corporate_finance--lecture_slides--cfpacket2spr20 p.101
- corporate_finance--lecture_slides--cfpacket2spr20 p.103

**Related:** [[cost-of-capital-approach]], [[enhanced-cost-of-capital-approach]], [[apv-approach]], [[relative-and-regression-analysis]], [[financing-life-cycle]], [[moving-to-the-optimal]], [[debt-design-framework]]

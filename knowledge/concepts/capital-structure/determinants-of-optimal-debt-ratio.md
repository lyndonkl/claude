# What actually drives the optimal debt ratio

**Core idea:** Run the cost-of-capital schedule across many firms and the optimum turns out to depend on four things. Three are firm-specific: the marginal tax rate, the pre-tax cash flow return on value (EBITDA/EV), and operating risk. One is macro: the price of equity risk relative to debt risk. The tax rate sets the size of the benefit. Cash flow return sets how much interest the firm can cover before ratings fall apart. Operating risk enters twice, through a higher unlevered beta and through worse ratings at every debt level. The macro factor shifts every firm's optimum in the same direction at the same time. Knowing these four lets you predict roughly where a firm's optimum will land before running the model, and diagnose a surprising answer afterwards.

**Formulas:**
- `EBITDA/EV = EBITDA / Enterprise value` and `EBIT/EV = EBIT / Enterprise value` — pre-tax cash flow return measures. Higher values mean more interest coverage per dollar of debt, hence higher debt capacity.
- Macro ratio: `ERP / Baa default spread`, where the Baa spread = Baa bond rate − T.Bond rate. A high ratio means equity risk is expensively priced relative to debt risk, so debt is relatively cheap and optimal debt ratios rise.
- Operating risk enters through `β_u` and through the coverage-to-rating mapping (see [[levered-beta-schedule]], [[synthetic-rating-and-cost-of-debt]]).

**Procedure:**
1. Read the marginal tax rate. Zero tax rate → optimal debt ratio 0%. The optimum is non-decreasing in the tax rate, though it plateaus (Disney's stops rising at 40% debt once the tax rate exceeds 20%).
2. Compute EBITDA/EV and EBIT/EV. High values signal high debt capacity; low values signal a growth firm that can support very little debt.
3. Assess operating risk. Use the unlevered beta of the businesses and the historical variability of operating income. Normalize the income used for ratings — ratings should be based on normalized, not peak or trough, earnings.
4. Discount the cash-flow-return signal in emerging markets. Country risk raises the cost of debt at every rating and compresses the optimum, which is why Tata Motors' high 17.52% EBITDA/EV still yields only a 20% optimum.
5. Check the macro environment. Compare the current ERP/Baa-spread ratio against its historical median of 1.96 (1960–2019). Above the median, debt is relatively cheap; below it, equity is.
6. Use these four to predict the answer, then run the model. If the model disagrees with the prediction, find the input that is doing the work before trusting it.

**Reference data:** Pre-tax cash flow returns and optimal debt ratios for the case firms:

| Company | EBITDA | EBIT | Enterprise value | EBITDA/EV | EBIT/EV | Optimal $ debt | Optimal debt ratio |
|---|---|---|---|---|---|---|---|
| Disney | $12,517m | $10,032m | $133,908m | 9.35% | 7.49% | $55,136m | 40.00% |
| Vale | $20,167m | $15,667m | $112,352m | 17.95% | 13.94% | $35,845m | 30.00% |
| Tata Motors | ₹250,116 | ₹166,605 | ₹1,427,478 | 17.52% | 11.67% | ₹325,986 | 20.00% |
| Baidu | ¥13,073 | ¥10,887 | ¥342,269 | 3.82% | 3.18% | ¥35,280 | 10.00% |
| Bookscape | $4,150 | $2,536 | $42,636 | 9.73% | 5.95% | $13,091 | 30.00% |

Optimal debt ratio by hypothetical tax rate (same firms):

| Tax rate | Disney | Vale | Tata Motors | Baidu | Bookscape |
|---|---|---|---|---|---|
| 0% | 0% | 0% | 0% | 0% | 0% |
| 10% | 20% | 0% | 0% | 0% | 10% |
| 20% | 40% | 0% | 10% | 10% | 30% |
| 30% | 40% | 30% | 20% | 10% | 30% |
| 40% | 40% | 40% | 20% | 10% | 30% |
| 50% | 40% | 40% | 20% | 10% | 30% |

Macro reference: the median ratio of the equity risk premium to the Baa default spread over 1960–2019 is **1.96**. The ratio spiked in the mid-1960s and the late 1970s and has run in the 1.5–2 range in recent years.

**Worked example:** Compare Baidu and Tata Motors. Baidu's EBITDA/EV is 3.82%, so even modest borrowing swamps its operating income: at 20% debt its coverage already implies a CC rating and at 40% a D rating, driving the optimum to 10%. Tata Motors' EBITDA/EV is 17.52%, more than four times higher, yet its optimum is only 20%. The difference is country risk plus operating risk: its cost of debt starts at 9.22% at AAA (versus Baidu's 4.70%) and jumps to 15.32% by 30% debt. High cash flow returns buy debt capacity only when the cost of debt is low to begin with.

**Determinism:**
- DETERMINISTIC: EBITDA/EV and EBIT/EV from financials and market values; the ERP/Baa-spread ratio from published series; the re-optimization at each hypothetical tax rate, given the model.
- JUDGMENT: which tax rate applies; whether reported operating income is normal; how much to discount cash flow returns for country risk; whether the current macro pricing of equity vs. debt risk is temporary or persistent.

**Pitfalls:**
- Treating EBITDA/EV as a sufficient statistic. It ignores the level of interest rates and country risk.
- Basing ratings on a single peak year's operating income.
- Assuming the optimum rises without limit in the tax rate. It plateaus once the coverage-driven rating becomes the binding constraint.
- Ignoring the macro factor when comparing an optimum computed today with one computed in a different rate environment.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.83-86

**Related:** [[cost-of-capital-approach]], [[tax-benefit-of-debt]], [[optimal-debt-ratio-by-firm-type]], [[levered-beta-schedule]], [[synthetic-rating-and-cost-of-debt]], [[relative-and-regression-analysis]], [[equity-risk-premium]]

# DCF sensitivity grid (testing the story)

**Core idea:** A single DCF number hides how much of the answer is assumption. The equity valuation project requires a sensitivity grid for every company: pick the two inputs the value is most sensitive to, vary each over a plausible range, and report the value per share in a two-dimensional table. The grid produces the DCF Lo, DCF Base and DCF Hi figures that go into the final recommendation table. It also does argumentative work — if even the most conservative cell sits above the market price, the buy case is far stronger than a point estimate could make it. This is the "test how much the value shifts when the story changes" step of the narrative-and-numbers method.

**Formulas:** No new formula. The grid re-runs the chosen DCF model with one or two inputs varied:
- Value per share = f(growth-phase growth rate, growth-period length, stable growth rate, stable debt ratio, …).
- DCF Lo = minimum cell in the plausible range; DCF Hi = maximum; DCF Base = the cell at the chosen assumptions.

**Procedure:**
1. Identify the two inputs with the largest influence on value. In practice these are almost always the length of the high-growth period and a growth rate, either the high-growth rate or the stable growth rate.
2. Choose three plausible levels for each. Do not use symmetric ranges for their own sake; use the range the narrative supports.
3. Re-run the model at each combination and tabulate value per share.
4. Read the spread. A value that varies by a few percent is robust; a value that varies by 70% or more means the recommendation rests almost entirely on the growth assumption.
5. Apply the plausibility filter. Rule out cells the story cannot support — sustained growth above the economy's growth rate forever, or high growth sustained for ten years in a competitive innovative industry.
6. Report DCF Lo, Base and Hi into the final recommendation table. See [[valuation-triangulation-and-recommendation]].
7. State the argument the grid supports. Either "even the most conservative case says undervalued," or "the base case is reasonable because growth above X is unlikely," or "this valuation is a bet on the growth rate."
8. For a distressed or highly levered firm, extend the sensitivity to the drivers of survival — capital spending, depreciation and working capital needs during high growth.

**Reference data:** Sensitivity grids from the six-company equity valuation project (value per share).

Affiliated Computer Services — stable growth rate × growth-period length:

| Stable growth | Period 5 | Period 10 |
|---|---|---|
| 3% | $48.75 | $54.07 |
| 5% | $49.40 | $54.73 |
| 7% | $50.05 | $55.41 |

Apple — high growth rate × growth-period length:

| Growth rate | Period 5 | Period 10 |
|---|---|---|
| 10% | $22.58 | $23.59 |
| 15% | $24.06 | $27.06 |
| 20% | $25.68 | $31.52 |

Biosite — high growth rate × growth-period length:

| High growth rate | Period 5 | Period 10 |
|---|---|---|
| 28% | $65.52 | $161.80 |
| 20% | $42.92 | $77.55 |
| 14.97% | $32.76 | $48.50 |

Gundle Environmental — stable growth rate × stable-period debt ratio:

| Growth rate | Debt ratio 30% | Debt ratio 42% | Debt ratio 50% |
|---|---|---|---|
| 5% | $29.20 | $34.02 | $38.29 |
| 10% | $35.02 | $41.13 | $45.98 |
| 15% | $41.72 | $48.67 | $54.83 |

Infosys — stable growth rate × growth-period length (Rs per share):

| Stable growth | Period 5 | Period 10 |
|---|---|---|
| 3% | 3,651 | 4,464 |
| 5% | 4,270 | 5,156 |
| 7% | 5,682 | 6,733 |

Named key drivers per company: ACS — growth-period length and stable growth rate. Apple — growth rate and period (value varies by almost 70% across the grid). Biosite — high-growth rate and its length. Gundle — stable growth and stable debt ratio. Infosys — stable growth and period. Nextel Partners — growth-period length, high and stable growth rates, plus capital spending, depreciation and working capital needs during high growth.

**Worked example:** Gundle Environmental. Base case $41.13 per share against a $19.73 market price — a large apparent undervaluation. The sensitivity grid varies stable growth from 5% to 15% and the stable debt ratio from 30% to 50%. The lowest cell in the grid, 5% growth with a 30% debt ratio, still gives $29.20 — nearly 50% above the market price. That single fact carries the BUY recommendation: the conclusion does not depend on the growth assumption at all, because even the most conservative sensitivity case says undervalued.

**Determinism:** DETERMINISTIC — every cell of the grid, given the model and the varied inputs. Extracting Lo, Base and Hi is mechanical. JUDGMENT — which two inputs to vary, what range is plausible for each, and which cells to rule out as economically unreasonable. Ruling out sustained growth above the economy's growth rate, or high growth sustained for ten years in a competitive industry, needs a view of the industry's competitive dynamics.

**Pitfalls:**
- Presenting the full grid as if all cells were equally likely. Biosite's $161.80 top cell (28% growth for ten years) was explicitly rejected as unreasonable in a competitive innovative industry, yet it still appears as DCF Hi in the final table.
- Varying only inputs the value is insensitive to, producing a falsely tight range.
- Failing to notice a very wide range. Apple's value varies by almost 70% across its grid, which should temper any confident recommendation.
- Using the grid to justify a pre-chosen answer by selecting the range that produces it.
- Omitting the plausibility argument. The grid's value lies in what it lets you rule out, not in the cells themselves.

**Sources:**
- valuations--projects--eqprojspr19 p.4
- valuations--projects--valproject2 p.3, p.6, p.9, p.11, p.14, p.18

**Related:** [[dcf-model-selection]], [[valuation-triangulation-and-recommendation]], [[two-stage-fcff-company-valuation]], [[equity-valuation-project-blueprint]], [[recapitalization-value-and-stress-test]]

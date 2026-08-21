# Assessing existing and past investments

**Core idea:** The same tools that judge new projects judge old ones, and firms use them far too rarely. Two distinct questions arise. The **post-mortem** looks back: did this investment create value, and how did actuals compare to the original forecasts? The **go-forward** question looks ahead: should we keep, expand, or divest? The second question ignores everything already spent. Only newly forecast future cash flows matter. The post-mortem's value lies not in a single project but in the pattern across many: symmetric forecast errors point to chance, while errors that run persistently in one direction point to bias — usually managerial over-optimism, worse in over-confident managers.

**Formulas:** Notation for a project analyzed mid-life.
- `F_n` = forecast of the cash flow in period n, made in the initial analysis
- `A_n` = actual cash flow in period n
- `NF_t` = new forecast of the cash flow in period t, made at the analysis date and counted forward from it
- `r` = discount rate appropriate to the project
- `n` = remaining project life

- `PV of future cash flows = Σ_{t=0..n} NF_t / (1 + r)^t`
- Decision rules:
  - `PV < 0` → **liquidate** the project
  - `PV < Salvage value` → **terminate** the project
  - `PV < Divestiture value` → **divest** the project
  - `PV > 0` and `PV > Divestiture value` → **continue** the project
- Value of continuing as a growing perpetuity: `Value = Current cash flow × (1 + g) / (r − g)`
- Value of an expansion: `Value = Increase in cash flow next year / (r − g)`, compared against the expansion cost

**Procedure:**
1. Fix the analysis date. Everything before it is sunk: past outlays, past cash flows, and the original forecasts.
2. Post-mortem branch: line up actuals `A_n` against the original forecasts `F_n` for the elapsed periods. Compute the errors.
3. Aggregate errors across projects and across time. A roughly symmetric distribution says chance. A one-directional distribution says bias.
4. Do not attribute cause on a single project. Chance and bias are indistinguishable on one observation.
5. Go-forward branch: build fresh forecasts `NF_t` for the remaining life, informed by what has actually been learned.
6. Discount those at the project's current risk-adjusted rate.
7. Establish the alternatives' values: salvage value (scrap/shutdown recovery) and divestiture value (what a buyer would pay).
8. Apply the decision rules above. Continue only when the going-concern value beats both zero and the best exit.
9. Test an expansion separately as its own incremental project: does the incremental cash flow perpetuity beat the incremental investment?
10. Revisit as new information arrives, and translate a changed view into action — abandon, delay, resize — not into regret.

**Reference data:** Why actuals differ from forecasts:

| Cause | Mechanism | Diagnostic signature |
|---|---|---|
| Chance | Risk means actuals differ from expectations. Macro shifts (inflation, interest rates, economic growth) and micro shifts (competitors, company) make even best-information forecasts wrong. | Errors roughly symmetric: actuals beat forecasts about as often as they miss |
| Bias | Original forecasts were skewed. Capital-budgeting evidence shows managers tend to be over-optimistic about cash flows, worse with over-confident managers. | Errors run persistently in one direction |

Decision thresholds, in order of severity:

| Condition | Action |
|---|---|
| PV of remaining cash flows < 0 | Liquidate |
| PV < salvage value | Terminate |
| PV < divestiture value | Divest |
| PV > 0 and PV > divestiture value | Continue (and test expansion separately) |

**Worked example:** Disney California Adventure, early 2008 ($ millions).

Facts: DCA opened in 2001 at a cost of $1.5 billion. The original case assumed about 60% of Disneyland visitors would cross over and about $100 million a year of after-tax cash flow. Actual experience 2001–2007: only 6 million of 15 million Disneyland visitors came (40%), and cash flow averaged $50 million a year — half the forecast, persistently, which is the signature of bias rather than chance.

Inputs for the go-forward decision: 2008 theme-park cost of capital = 6.62%, perpetual growth = 2% (inflation), abandonment recovery = $500 million. Expansion costs $600 million. It raises annual after-tax cash flow from $50 million to $80 million and the cross-over rate from 40% to 60%.

| Alternative | Calculation | Value |
|---|---|---|
| Continue as is | 50 × 1.02 / (0.0662 − 0.02) | **$1,103M** |
| Abandon now | Recovery of original investment | **$500M** |
| Expand | Incremental 30 × 1.02 / (0.0662 − 0.02) = $662M vs $600M cost | **+$62M net** |

Verdict: continue rather than abandon, and take the expansion. The $1.5 billion spent in 2001 appears nowhere in the arithmetic.

A second illustration of the same discipline: after the Netflix Fit case was written, six weeks of events (early 2020) could plausibly have changed the answer. The instructor's challenge is the right one — if your view changed, what would you actually *do* differently, rather than merely express regret? A changed view must translate into abandoning, delaying, or resizing.

**Determinism:** DETERMINISTIC — given new forecast cash flows, a discount rate, a salvage value, and a divestiture value, a script computes the PV and returns liquidate/terminate/divest/continue. The growing-perpetuity valuations of status quo and expansion are closed-form. Comparing actuals to original forecasts is mechanical once both series exist. JUDGMENT — producing the new forecasts, estimating divestiture value, and attributing forecast error to chance versus bias. That judgment needs the elapsed operating history, a buyer's perspective on the asset, and a sample of the firm's past forecast errors across projects.

**Pitfalls:**
- Letting the original investment influence the keep/divest decision. It is sunk, however painful.
- Anchoring the new forecasts on the original ones instead of on what actually happened.
- Judging bias from one project. Only the cross-project error distribution is diagnostic.
- Comparing the continue value to zero and stopping there, without checking salvage and divestiture values. A project can be worth continuing on its own and still be worth more to a buyer.
- Doing the post-mortem and filing it. The point is to recalibrate future forecasts.
- Treating an expansion as automatically justified because the base business is healthy. It is its own incremental project with its own NPV test.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.226
- corporate_finance--lecture_slides--cfpacket1spr20 p.326-331
- corporate_finance--case--netflixfitpresentation p.22

**Related:** [[project-options]], [[accounting-returns-roc-roe-eva]], [[incremental-cash-flow-principle]], [[npv-and-irr-mechanics]], [[terminal-value-and-project-life]], [[uncertainty-payback-sensitivity-simulation]], [[investment-analysis-first-principles]]

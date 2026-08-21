# The seven sins in acquisitions (deal audit checklist)

**Core idea:** Acquisitions fail so consistently that the failure must be structural rather than accidental. Damodaran organizes the structure into seven recurring errors — the "seven sins" — each of which is a specific, testable defect in how a target gets valued or how a price gets set. The seven sins double as an audit checklist: run any live deal or any acquirer's process against all seven, mark each Passed/Failed, and record the rationalization you were given. A deal that fails several sins is not a deal that needs a better spreadsheet; it is a deal that needs to be abandoned.

**Formulas:** No formula. The checklist is the instrument. Each sin maps to a valuation input that is being misstated:

| Sin | Input being corrupted |
|---|---|
| 1. Risk transference | Discount rate (target's cost of equity replaced by acquirer's) |
| 2. Debt subsidies | Cost of capital (target's debt capacity/cost of debt replaced by acquirer's) |
| 3. Auto-pilot control | Price (arbitrary % premium bolted onto value) |
| 4. Elusive synergy | Cash flows / growth (unquantified benefits assumed) |
| 5. It's all relative | Price and terminal value (transaction and exit multiples) |
| 6. Verdict first, trial afterwards | Everything (valuation reverse-engineered to a pre-set price) |
| 7. It's not my fault | Post-deal delivery (no accountability, so no benefits) |

**Procedure:**
1. Get the deal's own valuation materials — the acquirer's DCF, the banker's fairness opinion, the synergy schedule, the premium justification.
2. Sin 1 — Risk transference: find the discount rate applied to the target's cash flows. Does it reflect the target's business risk, or the acquirer's? Fail if the acquirer's (lower) rate is used.
3. Sin 2 — Debt subsidies: find the cost of capital's debt component. Is the debt ratio and pre-tax cost of debt the target's own, or the acquirer's cheaper borrowing? Fail if the acquirer's.
4. Sin 3 — Control premium: is the premium a fixed rule-of-thumb percentage (e.g., "20% because Mergerstat says so"), or is it derived as restructured value minus status-quo value? Fail if a rule of thumb.
5. Sin 4 — Synergy: is each claimed synergy mapped to a specific valuation input (margin, ROC, reinvestment rate, growth period, tax rate, debt ratio) with a dollar value and a delivery date? Fail if it is a word ("synergy", "strategic fit", "optionality") without a number.
6. Sin 5 — Comparables and exit multiples: is the price set off what other acquirers paid, or is the terminal value an exit multiple? Fail if either.
7. Sin 6 — Bias: reconstruct the chronology. Was the price set (by the CEO, by a bidding contest, by a banker's pitch) before the valuation was produced? Fail if the valuation post-dates the price.
8. Sin 7 — Accountability: name the person whose compensation depends on the promised benefits arriving. If no name exists, fail.
9. Record each verdict and the rationalization offered. Deals that fail sins 3–6 are overpayment risks; a deal that fails sins 6 and 7 together will never be corrected internally.

**Reference data:** Acquisition testing sheet (the blank scorecard to fill in per deal):

| Test | Passed/Failed | Rationalization |
|---|---|---|
| Risk transference | | |
| Debt subsidies | | |
| Control premium | | |
| The value of synergy | | |
| Comparables and Exit Multiples | | |
| Bias | | |
| A successful acquisition strategy | | |

**Worked example:** HP's acquisition of Autonomy, audited against the sheet. Control premium: HP paid $5,200M over a $5,900M market value — a ~88% premium, with no restructuring plan disclosed → Failed. Synergy: the post-mortem attributed $4,451M of the price to "non-existent synergy" → Failed. Bias: CEO Leo Apotheker defended the deal by invoking that HP has "a pretty rigorous process... which is a D.C.F.-based model" taking "a very conservative view," and that Autonomy would be "on Day 1, accretive to H.P." — process invocation and accretion, not value → Failed. Accountability: the write-off a year later assigned blame across the old CEO, the bankers, Autonomy's managers and the auditors, i.e., to no one in particular → Failed. Four failures, $8.8B written off.

**Determinism:**
- DETERMINISTIC: none of the seven verdicts is computed; but each has a deterministic *test statistic* — the discount rate used vs the target's own cost of equity; the debt ratio used vs the target's; the premium as a % of market value; the ratio of unquantified to quantified synergy dollars; whether terminal value came from a multiple or a perpetuity formula.
- JUDGMENT: every Passed/Failed verdict, because it requires reading intent from documents and chronology; and the overall decision to walk away.

**Pitfalls:**
- Running the checklist after the deal is signed. The sheet is a pre-commitment device.
- Treating a single failure as fatal or a single pass as exculpatory — the sins compound (a rule-of-thumb premium plus a transaction-multiple price plus a verdict-first process is the standard failing deal).
- Accepting "we used a DCF" as a pass on sins 1, 2 and 5; a DCF with the acquirer's discount rate and an exit multiple terminal value commits three sins inside a DCF wrapper.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.89-90`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.89-90`

**Related:** [[target-discount-rate-discipline]], [[control-premium-rules-of-thumb]], [[synergy-taxonomy]], [[valuing-synergy]], [[transaction-and-exit-multiples]], [[deal-bias-and-ego]], [[acquisition-strategy-design]], [[acquisition-empirical-record]]

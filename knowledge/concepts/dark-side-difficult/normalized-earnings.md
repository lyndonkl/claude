# Normalizing earnings for cyclical and temporarily troubled firms

**Core idea:** Some firms lose money for reasons that will not last: a cyclical trough, a commodity price collapse, a one-time charge, a strike, a recall. Valuing them off current earnings produces nonsense, because the base year is not representative of the business. The repair is normalization — replace the current operating income with what the firm would earn in a normal year, then value it forward from there. Normalization is only legitimate when the problems really are temporary. If a firm's losses come from a broken business model, a permanent shift in demand, or crushing leverage, normalizing is wishful thinking, and the right models are the negative-earnings DCF or the distress-adjusted DCF instead.

**Formulas:** Three approaches, in order of the information they need:
- **Approach 1 — historical average earnings:** `Normalized EBIT = average EBIT over the last n years` (typically 5, spanning a full cycle). Use when the firm's scale has not changed much.
- **Approach 2 — historical average return on capital:** `Normalized EBIT = Average pre-tax return on capital × Current book capital`, with `Book capital = Book value of debt + Book value of equity`. Use when the firm has grown, so old dollar earnings understate today's business.
- **Approach 3 — sector operating margin:** `Normalized EBIT = Sector (or own aggregate historical) pre-tax operating margin × Current revenues`. Use when revenues are meaningful but margins have collapsed.
- The firm's own aggregate historical margin, which often serves as the "sector" margin: `Aggregate margin = Σ EBIT over n years / Σ Revenues over n years` — an aggregate, not an average of ratios.
- Downstream, the normalized EBIT feeds the interest coverage ratio and so the synthetic rating: `Coverage = Normalized EBIT / Interest expense` → rating → default spread → `Cost of debt = Riskfree rate + Spread`.

**Procedure:**
1. Decide whether the trouble is temporary. Evidence for temporary: the sector is in a known downturn, peers show the same pattern, the firm earned normal margins for years, and the balance sheet can survive until recovery. Evidence against: falling market share, structural demand shift, leverage that forces asset sales.
2. If the trouble is permanent or survival is in doubt, stop. Use [[young-company-valuation]] (the negative-earnings model) or [[distress-and-failure-adjusted-value]] instead.
3. Adjust the base year first for accounting distortions — capitalize R&D and operating leases if relevant — so you normalize a properly measured number ([[capitalizing-rd]]).
4. Pick the approach that matches the data you have. Approach 3 is the default when revenue is stable and margins are the problem.
5. Compute the normalized EBIT.
6. Recompute the derived numbers with the normalized figure: interest coverage, synthetic rating, cost of debt, return on capital, reinvestment rate.
7. Resolve the circularity. The rating depends on the normalized EBIT, the cost of debt depends on the rating, lease capitalization depends on the cost of debt, and the restated EBIT depends on the lease adjustment. Iterate to a fixed point (Excel does this with iterative calculation switched on).
8. Value the firm forward from the normalized base, and state in one line what the normalization added or removed.
9. If the firm will take time to recover, do not jump straight to the normal level. Ramp the margin toward it, exactly as in the declining-firm and young-company models.

**Reference data (1):** The normalization module (normearn.xls), stored example. Five-year history: revenues 2,032 / 2,376 / 2,779 / 3,155 / 3,248 (total 13,590); EBIT 186 / 454 / 529 / 448 / 383 (total 2,000). Per-year margins: 9.154%, 19.108%, 19.036%, 14.200%, 11.792%. Aggregate margin = 2,000/13,590 = **14.7167%**.

| Approach | Formula | Result |
|---|---|---|
| 1 — average EBIT | entered directly | 3,500 |
| 2 — average ROC × book capital | 0.22 × (0 + 11,722) | 2,578.84 |
| 3 — sector margin × current revenues | 0.1471670 × 12,154 | **1,788.67** (the branch selected) |

The normalized EBIT of 1,788.67 then drives the rating: coverage = 1,788.67/121 = 14.78 (the interest proxy is the operating-lease expense, since balance-sheet debt is zero) → the large-manufacturing table gives AAA → spread 0.75% → cost of debt = 5.1% + 0.75% = 5.85%.

**Reference data (2):** Synthetic-rating table used with normalized EBIT — large manufacturing firms. Lookup rule: find the row where `coverage > lower bound` and `coverage ≤ upper bound`. (The thresholds ending in `.999999` implement a strict "less than the next bound".)

| Coverage > | Coverage ≤ | Rating | Spread |
|---|---|---|---|
| −100000 | 0.199999 | D | 14.00% |
| 0.2 | 0.649999 | C | 12.70% |
| 0.65 | 0.799999 | CC | 11.50% |
| 0.8 | 1.249999 | CCC | 10.00% |
| 1.25 | 1.499999 | B− | 8.00% |
| 1.5 | 1.749999 | B | 6.50% |
| 1.75 | 1.999999 | B+ | 4.75% |
| 2.0 | 2.499999 | BB | 3.50% |
| 2.5 | 2.999999 | BBB | 2.25% |
| 3.0 | 4.249999 | A− | 2.00% |
| 4.25 | 5.499999 | A | 1.80% |
| 5.5 | 6.499999 | A+ | 1.50% |
| 6.5 | 8.499999 | AA | 1.00% |
| 8.5 | 100000 | AAA | 0.75% |

For smaller and riskier firms the coverage thresholds are higher at every rating (D up to 0.499999; AAA needs coverage above 12.5). For financial service firms they are far lower (AAA at coverage above 3.0, D below 0.049999), reflecting that banks operate at much thinner coverage. The spread column is identical across all three tables.

**Reference data (3):** Normalization for financial firms uses the same idea on the equity side. The equity excess-return model offers two routes: average net income over the last five years, or a normalized ROE applied to current book equity — see [[bank-fcfe-and-excess-return-models]].

**Worked example:** The stored normearn.xls case. The firm's revenues grew from 2,032 to 3,248 over five years while EBIT bounced between 186 and 529, so no single year is representative. Approach 1 would use the average EBIT of 400 — far too small, since current revenues are 12,154, several times the historical scale. Approach 3 fixes the scale problem: apply the aggregate five-year margin of 14.7167% to current revenues of 12,154, giving a normalized EBIT of **1,788.67**. That number then produces an AAA synthetic rating and a 5.85% cost of debt, which in turn discounts the lease commitments (156, 143, 122, 109, 97, then 448 spread over 3 years at 149.33 a year) into 838.94 of lease debt, adding 49.08 of imputed interest back to EBIT.

**Determinism:** DETERMINISTIC — (approach, five-year revenue and EBIT history, current revenues, book debt and equity, average ROC) → normalized EBIT; and (normalized EBIT, interest expense, firm type, riskfree rate) → coverage, rating, spread, cost of debt. The aggregate-margin calculation and the table lookup are pure computation. JUDGMENT: whether the trouble is temporary at all, which approach fits, how many years constitute a full cycle, what counts as the right sector margin, and how long the firm takes to get back to normal.

**Pitfalls:**
- Normalizing a permanently broken business. The three approaches will happily produce a healthy EBIT for a firm that will never earn it.
- Averaging dollar earnings (approach 1) for a firm that has grown several-fold. Use the margin or return-on-capital approach instead.
- Averaging the ratio of margins rather than computing the aggregate `ΣEBIT/ΣRevenues`. The two differ, and the aggregate is the one the model uses.
- Jumping to normalized earnings in year 1 when recovery will take years. Ramp instead.
- Ignoring the circularity between the rating, the cost of debt, the lease adjustment and the EBIT. Solve it, or your cost of debt is inconsistent with the earnings you normalized to.
- Dividing by zero interest expense in the coverage ratio. The convention is to substitute a debt-like charge, such as the operating-lease expense.
- Normalizing earnings and *also* assuming a recovery in growth and margins on top. That is the same recovery counted twice.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.352
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.343
- spreadsheet model doc: special-troubled.md — normearn.xls (Earnings Normalizer, Ratings estimator, Operating lease converter, Industry averages)
- spreadsheet model doc: focussed-eva-finsvc.md — eqexret.xls, Normalized Earnings sheet

**Related:** [[commodity-and-cyclical-valuation]], [[capitalizing-rd]], [[young-company-valuation]], [[distress-and-failure-adjusted-value]], [[bank-fcfe-and-excess-return-models]], [[synthetic-rating]], [[operating-lease-capitalization]], [[difficult-company-taxonomy]]

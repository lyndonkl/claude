# Synthetic versus actual ratings

**Core idea:** When a firm has an agency rating AND a synthetic rating, the two often disagree. The gap is informative, not embarrassing. A synthetic rating uses one ratio from one year; an agency rating uses many ratios, normalized earnings, qualitative factors and sector conventions. Damodaran's rule is to use the ACTUAL rating when one exists and is credible, and to use the synthetic rating as a diagnostic — it tells you what the firm's current numbers alone would justify. Three systematic reasons explain most divergences: extra information in the agency rating, sector-wide rating conventions the synthetic method cannot see, and country risk that drags emerging-market issuers below their financials.

**Formulas:** No formula. The comparison is:
- Synthetic rating = f(current EBIT / current interest expense, size class).
- Actual rating = agency judgment over many inputs.
- Diagnostic gap = notches between the two, plus the spread difference it implies. If the synthetic spread is 0.40% and the actual spread is 1.00%, the actual cost of debt is 60 basis points higher on the same riskfree rate.

**Procedure:**
1. Compute the synthetic rating from coverage ([[synthetic-rating]]).
2. Look up the firm's actual rating(s). If several bonds carry different ratings, take the median.
3. If they match within a notch, use the actual rating and move on.
4. If they differ materially, diagnose before choosing:
   - Is current EBIT unusually high or low versus a normalized figure? If current earnings are inflated, the synthetic rating is too good. Re-run with normalized EBIT.
   - Is the firm in a sector where agencies systematically rate below (or above) what the ratios imply? The synthetic method cannot see sector-wide conventions.
   - Is the firm domiciled in an emerging market? Agencies frequently cap or drag corporate ratings toward the sovereign rating. The synthetic rating, built only on the firm's financials, will look better.
   - Is the firm a bank or insurer? Do not synthesize.
   - Does the firm carry large off-balance-sheet obligations you did not capitalize? Add leases and re-run.
5. Choose: use the actual rating for the cost of debt in almost all cases. Use the synthetic rating when there is no rating, when ratings conflict badly, or when the actual rating is visibly stale relative to a large recent change in the firm's finances.
6. Document the gap and its cause in the valuation. It is a stated assumption, not a rounding error.

**Reference data:** Documented divergences from the corporate finance packet (2013/14 data):

| Company | Synthetic rating | Actual rating | Explanation given |
|---|---|---|---|
| Disney | Aaa/AAA (coverage 22.57, large cap) | A | (a) Synthetic uses interest coverage only, while the agency uses other ratios and qualitative factors. (b) Synthetic cannot allow for sector-wide rating biases. (c) Synthetic used 2013 operating income; the agency rating reflects normalized earnings. |
| Vale | Aa2/AA (coverage 11.67) | A− (on dollar debt) | Country risk. Vale is Brazil-based, and agencies rate it lower than its financials alone would justify. |
| Deutsche Bank | Not attempted | A | Defining "interest expense on debt" for a bank is not meaningful, so no synthetic rating is estimated. |
| Tata Motors | A3/A− (coverage 4.51) | AA− from CRISIL (local scale, company risk only) | The local rating measures company risk relative to Indian peers, so India's sovereign default spread has to be added separately. |

**Worked example:** Disney, 2013. Operating income $10,023m, interest expense $444m → coverage 22.57. As a large-cap developed-market firm, the large-firm column gives Aaa/AAA with a 0.40% spread → pre-tax cost of debt 2.75% + 0.40% = 3.15%. But S&P actually rates Disney A, spread 1.00% → pre-tax cost of debt 2.75% + 1.00% = 3.75%. Damodaran uses the ACTUAL rating. The 3.75% pre-tax rate, taxed at Disney's 36.1% marginal rate, gives the 2.40% after-tax cost of debt that flows into Disney's 7.81% cost of capital. Had the synthetic AAA been used instead, the after-tax cost of debt would have been 3.15% × 0.639 = 2.01%, and the cost of capital about 4 basis points lower on an 11.58% debt weight — small for Disney, but material for a firm with a 40% debt ratio and a wider gap.

**Determinism:**
- DETERMINISTIC: computing both ratings, and computing the cost-of-debt difference the gap implies.
- JUDGMENT: which rating to use, and why they diverge. The judgment needs the firm's multi-year earnings history (to test the normalization explanation), peer ratings in the same sector at similar coverage (to test the sector-bias explanation), the sovereign rating and spread (to test the country-risk explanation), and the date of the last rating action (to test staleness).

**Pitfalls:**
- Picking whichever rating gives the answer you want.
- Concluding that a firm is "underrated" or "overrated" from the synthetic rating alone. It is a one-ratio model.
- Ignoring the country-risk explanation for emerging-market issuers, which is the single most common source of a large gap.
- Treating an agency rating as always current. Agencies lag, especially after a large acquisition, a spin-off or a leveraged recapitalization.
- Producing a synthetic rating for a financial-service firm and taking it seriously.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.189-191
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.101-102, p.105
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.99-100, p.103
- spreadsheet doc `corpfin-ratings-risk` — ratings.xls purpose statement (sanity-check use of the synthetic rating)

**Related:** [[synthetic-rating]], [[interest-coverage-ratio]], [[cost-of-debt-estimation-routes]], [[country-risk-in-cost-of-debt]], [[default-spreads-over-time]], [[normalizing-earnings]]

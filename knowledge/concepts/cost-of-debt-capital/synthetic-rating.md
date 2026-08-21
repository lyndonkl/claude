# Synthetic rating

**Core idea:** A synthetic rating is a bond rating you estimate yourself from a firm's financials, instead of buying one from an agency. In its simplest and most-used form it uses one number: the interest coverage ratio. You classify the firm by size and type, find the coverage bracket the firm falls into, and read off the rating and its default spread. The pre-tax cost of debt is then the riskfree rate plus that spread. This is what makes the cost of debt computable for private firms, divisions, IPO candidates and unrated companies — and it doubles as a sanity check on an actual rating. The lookup tables are the whole method, so they must be reproduced exactly and refreshed as spreads move.

**Formulas:**
- Interest Coverage Ratio = EBIT / Interest Expenses. See [[interest-coverage-ratio]].
- Rating = table_lookup(coverage ratio, firm class), where the bracket rule is: lower bound < ICR ≤ upper bound.
- Default Spread = spread column of the same table row.
- Pre-tax cost of debt = Riskfree rate + Default Spread (+ Country default spread, if the firm bears sovereign risk — see [[country-risk-in-cost-of-debt]]).
- After-tax cost of debt = Pre-tax cost of debt × (1 − marginal tax rate).

Firm classes: (1) large manufacturing firm — market cap above roughly $5 billion; (2) smaller or riskier firm — market cap below roughly $5 billion; (3) financial-service firm — uses long-term interest expense only and a separate, much lower coverage scale.

**Procedure:**
1. Compute EBIT and interest expense; normalize and lease-adjust as needed ([[interest-coverage-ratio]]).
2. Classify the firm.
   - Market cap > $5 billion and a conventional operating business → large-firm column.
   - Market cap < $5 billion, or a young/risky/private business → small-or-risky column. This column demands HIGHER coverage for the same rating.
   - Bank, insurer, brokerage → financial-firm table, using long-term interest expense only. Damodaran declines to synthesize ratings for banks at all in the lecture material; treat the financial table as a last resort.
3. Find the row where lower bound < ICR ≤ upper bound. Read the rating and spread.
4. Pre-tax cost of debt = current long-term government bond rate in the valuation currency + spread.
5. If the firm is in an emerging market and bears sovereign risk, add the country default spread (or a fraction of it).
6. Compare with the actual rating if one exists and reconcile ([[synthetic-vs-actual-rating]]).
7. Refresh the spread column. Coverage brackets have been stable across editions; the SPREADS have not.

**Reference data:**

**(A) Most recent edition — January 2020 vintage, from wacccalc.xls `Synthetic rating` sheet.** Lookup rule: coverage > col 1 and ≤ col 2.

Large manufacturing firms (firm type 1):

| Coverage > | Coverage ≤ | Rating | Spread |
|---|---|---|---|
| −100000 | 0.199999 | D2/D | 12.00% |
| 0.2 | 0.649999 | Caa/CCC | 10.00% |
| 0.65 | 0.799999 | Ca2/CC | 8.00% |
| 0.8 | 1.249999 | C2/C | 7.00% |
| 1.25 | 1.499999 | B3/B− | 6.00% |
| 1.5 | 1.749999 | B2/B | 5.00% |
| 1.75 | 1.999999 | B1/B+ | 4.00% |
| 2 | 2.2499999 | Ba2/BB | 3.25% |
| 2.25 | 2.49999 | Ba1/BB+ | 2.75% |
| 2.5 | 2.999999 | Baa2/BBB | 1.75% |
| 3 | 4.249999 | A3/A− | 1.20% |
| 4.25 | 5.499999 | A2/A | 1.00% |
| 5.5 | 6.499999 | A1/A+ | 0.90% |
| 6.5 | 8.499999 | Aa2/AA | 0.70% |
| 8.5 | 100000 | Aaa/AAA | 0.40% |

Smaller and riskier firms (firm type 2):

| Coverage > | Coverage ≤ | Rating | Spread |
|---|---|---|---|
| −100000 | 0.499999 | D2/D | 12.00% |
| 0.5 | 0.799999 | Caa/CCC | 10.00% |
| 0.8 | 1.249999 | Ca2/CC | 8.00% |
| 1.25 | 1.499999 | C2/C | 7.00% |
| 1.5 | 1.999999 | B3/B− | 6.00% |
| 2 | 2.499999 | B2/B | 5.00% |
| 2.5 | 2.999999 | B1/B+ | 4.00% |
| 3 | 3.499999 | Ba2/BB | 3.25% |
| 3.5 | 3.9999999 | Ba1/BB+ | 2.75% |
| 4 | 4.499999 | Baa2/BBB | 1.75% |
| 4.5 | 5.999999 | A3/A− | 1.20% |
| 6 | 7.499999 | A2/A | 1.00% |
| 7.5 | 9.499999 | A1/A+ | 0.90% |
| 9.5 | 12.499999 | Aa2/AA | 0.70% |
| 12.5 | 100000 | Aaa/AAA | 0.40% |

CAUTION on these two tables: the rating labels in the bottom four rows are scrambled relative to spread monotonicity (Caa/CCC carries a 10% spread while C2/C carries 7%). Reproduce as-is if matching the sheet; if you need monotone labels, use the ratings.xls ordering in table (C) below.

Rating → spread map used for the "Actual rating" route in the same workbook: A1/A+ 0.90%; A2/A 1.00%; A3/A− 1.20%; Aa2/AA 0.70%; Aaa/AAA 0.40%; B1/B+ 4.00%; B2/B 5.00%; B3/B− 6.00%; Ba1/BB+ 2.75%; Ba2/BB 3.25%; Baa2/BBB 1.75%; C2/C 7.00%; Ca2/CC 8.00%; Caa/CCC 10.00%; D2/D 12.00%.

**(B) November 2013 vintage, used in every Disney/Vale/Bookscape worked example in the corporate finance packet.** Size split is explicit here: large cap > $5 billion vs small cap or risky < $5 billion.

| Large cap (>$5bn) coverage | Small cap or risky (<$5bn) coverage | Rating | Spread (11/13) |
|---|---|---|---|
| > 8.50 | > 12.5 | Aaa/AAA | 0.40% |
| 6.5 – 8.5 | 9.5 – 12.5 | Aa2/AA | 0.70% |
| 5.5 – 6.5 | 7.5 – 9.5 | A1/A+ | 0.85% |
| 4.25 – 5.5 | 6 – 7.5 | A2/A | 1.00% |
| 3 – 4.25 | 4.5 – 6 | A3/A− | 1.30% |
| 2.5 – 3 | 4 – 4.5 | Baa2/BBB | 2.00% |
| 2.25 – 2.5 | 3.5 – 4 | Ba1/BB+ | 3.00% |
| 2 – 2.25 | 3 – 3.5 | Ba2/BB | 4.00% |
| 1.75 – 2 | 2.5 – 3 | B1/B+ | 5.50% |
| 1.5 – 1.75 | 2 – 2.5 | B2/B | 6.50% |
| 1.25 – 1.5 | 1.5 – 2 | B3/B− | 7.25% |
| 0.8 – 1.25 | 1.25 – 1.5 | Caa/CCC | 8.75% |
| 0.65 – 0.8 | 0.8 – 1.25 | Ca2/CC | 9.50% |
| 0.2 – 0.65 | 0.5 – 0.8 | C2/C | 10.50% |
| < 0.2 | < 0.5 | D2/D | 12.00% |

(The printed slide shows the B1/B+ large-cap row as "1.75 – 2.25", overlapping the Ba2/BB row above it. Treat it as 1.75 – 2.00; every other edition of the table uses that bracket.)

**(C) ratings.xls vintage (spreads in the standalone rating spreadsheet).** Same brackets, different spreads and a monotone label ordering. Lookup: lower < ICR ≤ upper.

Large manufacturing firms:

| ICR > | ICR ≤ | Rating | Spread |
|---|---|---|---|
| −100000 | 0.199999 | D2/D | 17.44% |
| 0.2 | 0.649999 | C2/C | 13.09% |
| 0.65 | 0.799999 | Ca2/CC | 9.97% |
| 0.8 | 1.249999 | Caa/CCC | 9.46% |
| 1.25 | 1.499999 | B3/B− | 5.94% |
| 1.5 | 1.749999 | B2/B | 4.86% |
| 1.75 | 1.999999 | B1/B+ | 4.05% |
| 2.0 | 2.2499999 | Ba2/BB | 2.77% |
| 2.25 | 2.49999 | Ba1/BB+ | 2.31% |
| 2.5 | 2.999999 | Baa2/BBB | 1.71% |
| 3.0 | 4.249999 | A3/A− | 1.33% |
| 4.25 | 5.499999 | A2/A | 1.18% |
| 5.5 | 6.499999 | A1/A+ | 1.07% |
| 6.5 | 8.499999 | Aa2/AA | 0.85% |
| 8.5 | 100000 | Aaa/AAA | 0.69% |

Smaller and riskier firms:

| ICR > | ICR ≤ | Rating | Spread |
|---|---|---|---|
| −100000 | 0.499999 | D2/D | 17.44% |
| 0.5 | 0.799999 | C2/C | 13.09% |
| 0.8 | 1.249999 | Ca2/CC | 9.97% |
| 1.25 | 1.499999 | Caa/CCC | 9.46% |
| 1.5 | 1.999999 | B3/B− | 5.94% |
| 2.0 | 2.499999 | B2/B | 4.86% |
| 2.5 | 2.999999 | B1/B+ | 4.05% |
| 3.0 | 3.499999 | Ba2/BB | 2.77% |
| 3.5 | 3.9999999 | Ba1/BB+ | 2.31% |
| 4.0 | 4.499999 | Baa2/BBB | 1.71% |
| 4.5 | 5.999999 | A3/A− | 1.33% |
| 6.0 | 7.499999 | A2/A | 1.18% |
| 7.5 | 9.499999 | A1/A+ | 1.07% |
| 9.5 | 12.499999 | Aa2/AA | 0.85% |
| 12.5 | 100000 | Aaa/AAA | 0.69% |

Financial-service firms (keyed on LONG-TERM interest coverage; note how much lower every threshold is):

| ICR > | ICR ≤ | Rating | Spread |
|---|---|---|---|
| −100000 | 0.049999 | D2/D | 17.44% |
| 0.05 | 0.099999 | C2/C | 13.09% |
| 0.1 | 0.199999 | Ca2/CC | 9.97% |
| 0.2 | 0.299999 | Caa/CCC | 9.46% |
| 0.3 | 0.399999 | B3/B− | 5.94% |
| 0.4 | 0.499999 | B2/B | 4.86% |
| 0.5 | 0.599999 | B1/B+ | 4.05% |
| 0.6 | 0.749999 | Ba2/BB | 2.77% |
| 0.75 | 0.899999 | Ba1/BB+ | 2.31% |
| 0.9 | 1.199999 | Baa2/BBB | 1.71% |
| 1.2 | 1.49999 | A3/A− | 1.33% |
| 1.5 | 1.99999 | A2/A | 1.18% |
| 2.0 | 2.49999 | A1/A+ | 1.07% |
| 2.5 | 2.99999 | Aa2/AA | 0.85% |
| 3.0 | 100000 | Aaa/AAA | 0.69% |

**(D) 2004 vintage** (used in the Embraer example in the valuation packets; kept for reconciling that worked example). Same brackets as (B); spreads: AAA 0.35%, AA 0.50%, A+ 0.70%, A 0.85%, A− 1.00%, BBB 1.50%, BB+ 2.00%, BB 2.50%, B+ 3.25%, B 4.00%, B− 6.00%, CCC 8.00%, CC 10.00%, C 12.00%, D 20.00%.

**Worked example:** The five running companies, November 2013 table (B).

| Company | Coverage | Size / class | Column used | Synthetic rating |
|---|---|---|---|---|
| Disney | 22.57 | Large cap, developed | Large (>8.5 → AAA) | Aaa/AAA |
| Vale | 11.67 | Large cap, emerging | Large (6.5-8.5 is AA; 11.67 > 8.5) | Aaa/AAA by the large table; the slide reports AA after emerging-market treatment |
| Tata Motors | 4.51 | Large cap, emerging | Large (4.25-5.5 → A) then adjusted; slide reports A− | A3/A− |
| Baidu | 23.72 | Small cap, emerging | Small (>12.5 → AAA) | Aaa/AAA |
| Bookscape | 5.16 | Small cap, private | Small (4.5-6 → A−) | A3/A− |

Bookscape end-to-end: coverage 5.16 → small-firm column → 4.5-6 bracket → A3/A−, spread 1.30%. Pre-tax cost of debt = 2.75% + 1.30% = 4.05%. After tax at 40%: 2.43%.

Second worked example, from ratings.xls with its own spread column: a small/risky firm with EBIT 50, interest expense 8, riskfree 3%. ICR = 50/8 = 6.25 → small-firm table row (6.0, 7.499999] → A2/A, spread 1.18% → pre-tax cost of debt = 3% + 1.18% = 4.18%.

**Determinism:**
- DETERMINISTIC and fully scriptable: `synthetic_rating(icr, firm_type) -> (rating, spread)` from the tables above, then `cost_of_debt = riskfree + spread + country_spread`. Given EBIT, interest expense, firm type, riskfree rate and (optionally) lease inputs, a script produces the rating, spread and pre-tax cost of debt with no discretion.
- JUDGMENT: which firm class the company belongs to — the $5 billion line is a guide, not a law, and "riskier" is a qualitative call about a young, cyclical or highly volatile business. That judgment needs market cap, sector, business age and earnings volatility.
- JUDGMENT: whether the table applies at all. It was built on US companies; it travels well for large manufacturers in markets with US-like interest rates, and badly for small firms in high-rate markets.
- JUDGMENT: which vintage of spreads to use, and whether to refresh from current market data.

**Pitfalls:**
- Reading the large-firm column for a small firm. The small-firm column requires substantially higher coverage for the same rating; using the wrong column gives an artificially good rating and too low a cost of debt.
- Using a stale spread column. The brackets barely change; the spreads change a lot (compare 12.00% vs 17.44% vs 20.00% for a D rating across the vintages above).
- Treating the synthetic rating as a better rating than the agency's. It uses ONE ratio; agencies use many ratios plus qualitative judgment.
- Applying it to banks and insurers with an ordinary coverage ratio.
- Ignoring the interest-rate-level problem in emerging markets, which makes locally-financed firms look uncreditworthy.
- Forgetting that the synthetic rating for a firm with leases is circular and needs iteration.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.188-189, p.191, p.193
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.102-105
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.100-103
- spreadsheet doc `corpfin-ratings-risk` — ratings.xls, all three lookup tables, the $5bn size note, and the reimplementation notes
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls `Synthetic rating` sheet, both firm-type tables and the rating→spread map

**Related:** [[interest-coverage-ratio]], [[synthetic-vs-actual-rating]], [[cost-of-debt-estimation-routes]], [[default-spreads-over-time]], [[country-risk-in-cost-of-debt]], [[operating-leases-as-debt]], [[wacc-calculator-workflow]]

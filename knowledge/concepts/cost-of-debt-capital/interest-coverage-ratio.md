# Interest coverage ratio

**Core idea:** The interest coverage ratio is operating income divided by interest expense. It measures how many times over the firm's operating earnings cover its contractual interest bill. It is the single input to Damodaran's synthetic rating, so getting it right determines the whole cost of debt. Three adjustments matter in practice. Normalize EBIT when the current year is unrepresentative. Add imputed lease interest to interest expense when you capitalize operating leases. Scale the ratio down when local interest rates are far above US rates, because the table was calibrated on US firms.

**Formulas:**
- Interest Coverage Ratio (ICR) = EBIT / Interest Expenses.
  - EBIT = earnings before interest and taxes = operating income.
  - Interest Expenses = total interest on debt for the same period. For financial-service firms, use LONG-TERM interest expense only.
- Lease-adjusted version: ICR_adj = (EBIT + Current lease expense − Depreciation on the leased asset) / (Interest expense + r_d × Debt value of leases).
  - r_d = pre-tax cost of debt; Depreciation on leased asset = Debt value of leases / lease life. See [[operating-leases-as-debt]].
  - Short-cut variant of the numerator: EBIT + r_d × Debt value of leases.
- Normalized version: ICR = (Average EBIT over a cycle) / (Current-year interest expense).
- Interest-rate adjustment for emerging markets: ICR_adjusted = ICR / k, where k = local long-term interest rate / US long-term interest rate. If local rates are twice US rates, halve the ratio before the table lookup.

**Procedure:**
1. Pull operating income (EBIT) from the most recent income statement, and interest expense from the same statement.
2. Decide whether the current EBIT is representative.
   - Sector or firm in a temporary trough or spike → replace with a normalized EBIT, typically an average over the last 3 years or a full cycle.
   - Keep interest expense at the CURRENT year figure; the debt burden is a stock, not a cycle average.
3. If the firm has material operating leases, capitalize them and use the lease-adjusted numerator and denominator. This creates a circularity: lease debt needs a cost of debt, the cost of debt needs a rating, the rating needs the lease-adjusted coverage. Solve by fixed-point iteration (see step 6).
4. If the firm is a financial-service firm, strip out interest on deposits and short-term funding and use only long-term interest expense — then use the financial-firm coverage table, whose thresholds are far lower.
5. If the firm operates in a market whose long-term rates are much higher than US rates, divide the ratio by the rate ratio k before looking up the rating.
6. Iterate to convergence when leases are involved: start with r_d = riskfree + a guessed spread; compute lease debt; compute adjusted ICR; look up the rating and spread; recompute r_d; repeat. It converges in a few passes. Cap the iterations and keep the last value to avoid oscillating between two adjacent buckets.
7. Feed the final ratio to [[synthetic-rating]].

Edge-case rules:
- Interest expense = 0 with positive EBIT → ratio is infinite → top bucket (Aaa/AAA).
- Negative EBIT → negative ratio → falls in the bottom bucket (D2/D). The lookup tables use a lower bound of −100,000 to catch this; clamp anything below.
- Interest expense near zero → the ratio explodes but the table's +100,000 upper bound caps it at the top rating.

**Reference data:** Interest coverage ratios for the corporate finance packet's running companies (2013 data, currency in millions of each firm's reporting currency):

| Company | Operating income (EBIT) | Interest expense | Interest coverage ratio |
|---|---|---|---|
| Disney | $10,023 | $444 | 22.57 |
| Vale | $15,667 | $1,342 | 11.67 |
| Tata Motors | Rs 166,605 | Rs 36,972 | 4.51 |
| Baidu | CY 11,193 | CY 472 | 23.72 |
| Bookscape | $2,536 | $492 | 5.16 |

Normalization example (Embraer, 2004 valuation packet): average EBIT 2001-2003 = 462.1; 2003 interest expense = 129.70; ICR = 462.1 / 129.70 = 3.56. Single-year 2003 EBIT would have been far lower, because 9/11 and its aftermath crushed aircraft demand in 2002-2003.

**Worked example:** Facebook as set up in wacccalc.xls. Reported pre-tax operating income is 1,500 and reported interest expense on debt is 56. Operating leases: current lease expense 180, commitments 156/150/145/143/140 for years 1-5, plus a 600 lump beyond year 5, discounted at a 3.5% pre-tax cost of debt. Lease capitalization gives a debt value of leases of 1,127.92 and a straight-line depreciation of 125.32 over the 9-year lease life. So EBIT_adj = 1,500 + 180 − 125.32 = 1,554.68 and Interest_adj = 56 + 0.035 × 1,127.92 = 95.48. Lease-adjusted coverage = 1,554.68 / 95.48 = 16.28, which is above 8.5 and therefore Aaa/AAA on the large-firm table. Compare the unadjusted ratio: 1,500 / 56 = 26.8 — same rating here, but the adjustment can move the rating in a leveraged retailer or restaurant chain.

**Determinism:**
- DETERMINISTIC: EBIT and interest expense → ratio. Lease commitments plus r_d → lease debt, lease depreciation, imputed lease interest, and hence the adjusted ratio. The fixed-point iteration is fully mechanical.
- JUDGMENT: whether to normalize EBIT, and over what window. That needs the firm's own earnings history, the sector's cycle, and knowledge of one-off events (a strike, a crisis, an asset sale, a write-off).
- JUDGMENT: the interest-rate scaling factor k for emerging markets, and whether to apply it at all.
- JUDGMENT: for a financial-service firm, which interest expense counts as long-term.

**Pitfalls:**
- Using a single depressed or inflated year of EBIT, which mechanically produces a distressed or pristine rating.
- Using EBITDA instead of EBIT. The table is calibrated on EBIT.
- Ignoring operating leases, which flatters the ratio twice: it leaves interest out of the denominator and leaves lease rent in the numerator as an operating cost.
- Averaging interest expense over the same window as normalized EBIT. Current debt service, not average debt service, is what the firm must cover.
- Applying the US-calibrated table unadjusted to a small firm in a high-rate emerging market. The rate level mechanically depresses coverage even for an equally creditworthy firm.
- Applying the ordinary table to a bank. Damodaran does not attempt a synthetic rating for Deutsche Bank for exactly this reason.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.188, p.190, p.193
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.102, p.105
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.100, p.103
- spreadsheet doc `corpfin-ratings-risk` — ratings.xls `Start here Ratings sheet` (ICR = D10) and `Operating Leases` sheet, including the circularity and Excel-iteration note
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls `Synthetic rating` sheet (lease-adjusted F5, F6, coverage D9 = 16.2832)

**Related:** [[synthetic-rating]], [[operating-leases-as-debt]], [[cost-of-debt-estimation-routes]], [[synthetic-vs-actual-rating]], [[wacc-calculator-workflow]], [[normalizing-earnings]]

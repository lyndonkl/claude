# The WACC calculator workflow

**Core idea:** Damodaran's wacccalc.xls encodes the whole cost-of-capital estimation as one executable pipeline. It matters here because it fixes the ORDER of computation, exposes the one genuine circularity in the process, and shows exactly which inputs are user choices and which are table lookups. The order is not arbitrary: leases must be capitalized before the synthetic rating can be computed, the synthetic rating is needed for the cost of debt, and the cost of debt is needed to discount the leases. That loop is solved by iteration. Anyone reimplementing the cost of capital as code should follow this sequence.

**Formulas:** The pipeline, in order.
1. Market value of equity = Shares outstanding × Current price per share.
2. Lease capitalization at the current pre-tax cost of debt r_d → Debt value of leases, lease depreciation, EBIT adjustment ([[operating-leases-as-debt]]).
3. Lease-adjusted EBIT = Reported EBIT + Lease EBIT adjustment. Lease-adjusted interest = Reported interest + r_d × Lease debt.
4. Interest coverage = Lease-adjusted EBIT / Lease-adjusted interest.
5. Synthetic rating and spread = table lookup(coverage, firm type). Cost of debt = Riskfree + Rating spread + Country default spread ([[synthetic-rating]]).
6. Market value of straight debt = Interest expense × [1 − (1 + r_d)^(−M)] / r_d + Book debt / (1 + r_d)^M.
7. Straight-debt value of convertible, same formula on the convertible's own terms; equity portion = Market value of convertible − that value.
8. MV_debt = MV straight debt + straight-debt piece of convertible + lease debt. MV_preferred = Preferred shares × Preferred price.
9. Unlevered beta from the chosen approach; Levered beta = Unlevered beta × [1 + (1 − t) × MV_debt / MV_equity].
10. ERP from the chosen approach. Cost of equity = Riskfree + Levered beta × ERP.
11. After-tax cost of debt = r_d × (1 − t). Cost of preferred = Preferred dividend / Preferred price.
12. Total capital = MV equity + MV debt + MV preferred. Weights = component / total.
13. WACC = Σ weight × component cost.

**Procedure:**
1. Enter company metadata: company name, country of incorporation, US industry, global industry.
2. Enter lease data if the firm has operating leases: current-year lease expense, commitments for years 1-5, and the lump sum beyond year 5.
3. Enter shares outstanding and current market price.
4. Choose the beta approach from five options and supply what it needs:
   - Direct input: a levered (regression) beta, used as the final levered beta.
   - Single Business (US) or Single Business (Global): the industry unlevered beta is looked up.
   - Multibusiness (US) or Multibusiness (Global): enter revenues per business. The model looks up each business's EV/Sales and unlevered beta, values each business as revenues × EV/Sales, and takes the VALUE-weighted average unlevered beta.
5. Enter the riskfree rate. Choose the ERP approach from four options:
   - Will input: a directly supplied ERP.
   - Country of incorporation: look up that country's ERP.
   - Operating countries: enter revenues by country; the model weights each country's ERP by revenue share.
   - Operating regions: enter revenues by region; the model weights each region's ERP (a GDP-weighted average of its countries' ERPs) by revenue share.
6. Enter straight debt: book value, interest expense, average maturity.
7. Choose the cost-of-debt approach: Direct input, Actual rating (which looks the spread up in the rating→spread map), or Synthetic rating (which drives the coverage-based lookup and creates the circularity).
8. Choose the tax approach: input a rate directly, or use the marginal rate of the country of incorporation.
9. Enter convertible terms and preferred terms if any.
10. Enable iterative calculation. Then run the pipeline in the order above until the cost of debt stops moving.

Reimplementation notes:
- The circularity appears only when the cost-of-debt approach is Synthetic rating AND the firm has leases. Seed r_d = riskfree + a guessed spread, loop lease PV → coverage → rating → spread → r_d, and stop when the spread is stable. It converges in a few passes. Cap the iterations and keep the last value; a firm sitting on a bracket boundary can oscillate between two adjacent ratings.
- With no leases, the loop disappears entirely.
- Guard divisions: preferred price 0; average of the first five lease commitments 0; year-6 lump 0; convertible maturity 0.
- Interest expense near 0 with positive EBIT sends coverage to the top bracket via the +100,000 upper bound. Negative EBIT sends it to D2/D via the −100,000 lower bound.
- Multi-business calculators renormalize weights over the entered rows only.
- All percentages are decimal fractions.
- The saved file has a manual override worth noting: the tax rate cell holds 0.40 while the direct-input cell holds 0.35 and the US table rate is 0.25. The 0.40 is what flows downstream into the relevered beta and after-tax cost of debt. Do not assume the dropdown always wins.

**Reference data:** Input surface of wacccalc.xls, `Cost of Capital worksheet`.

| Block | Inputs |
|---|---|
| Metadata | Company, country of incorporation, US industry, global industry |
| Leases | Has leases (Yes/No); current lease expense; commitments years 1-5; lump beyond year 5 |
| Equity | Shares outstanding; current market price per share |
| Beta | Approach ∈ {Direct input, Single Business (US), Single Business (Global), Multibusiness (US), Multibusiness (Global)}; direct levered beta |
| Premiums | Riskfree rate; ERP approach ∈ {Will input, Country of incorporation, Operating countries, Operating regions}; direct ERP |
| Straight debt | Book value; interest expense; average maturity; cost-of-debt approach ∈ {Direct input, Synthetic rating, Actual rating}; direct rate; actual rating; synthetic firm type ∈ {1, 2}; pre-tax operating income |
| Tax | Approach ∈ {Will input, country lookup}; direct tax rate |
| Convertible | Book value; interest expense; maturity; market value |
| Preferred | Number of shares; market price per share; annual dividend per share |
| Side calculators | Operating-countries ERP; operating-regions ERP; multi-business US; multi-business global |

Reference tables shipped inside the model: US industry averages and global industry averages (each keyed by industry name, supplying unlevered beta and EV/Sales among 26 columns); country risk and taxes (country → default spread, ERP, marginal tax rate, country risk premium); regional ERPs; the two coverage → rating → spread tables; and the rating → spread map.

**Worked example:** Facebook, as configured in the saved workbook.
1. Equity: 2,407 shares × $37.53 = 90,334.71.
2. Leases: expense 180; commitments 156 / 150 / 145 / 143 / 140; lump 600; r_d 3.5%. n₆ = round(600 / 146.8) = 4. Annualized year-6+ payment = 150. Lease debt = 1,127.92. Lease depreciation = 1,127.92 / 9 = 125.32. EBIT adjustment = 180 − 125.32 = +54.68.
3. Synthetic-rating side calculation: adjusted EBIT = 1,500 + 54.68 = 1,554.68; adjusted interest = 56 + 0.035 × 1,127.92 = 95.48; coverage = 16.28 → Aaa/AAA, spread 0.40%, implied cost of debt 2.9%. (Not used here: the cost-of-debt approach is Direct input at 3.5%.)
4. Straight debt: 56 × 2.801637 + 1,000 / 1.035³ = 1,058.83. Convertible: none. MV_debt = 1,058.83 + 1,127.92 = 2,186.75. Preferred: none.
5. Beta: Single Business (Global), Advertising → unlevered beta 1.0965. Levered = 1.0965 × [1 + 0.60 × 2,186.75 / 90,334.71] = 1.1124.
6. ERP: Operating regions, revenues Asia 56 / Caribbean 100 / Middle East 631 / North America 374 / Western Europe 168 (total 1,329) against region ERPs 7.26% / 14.37% / 6.85% / 5.75% / 6.88% → weighted ERP 7.127%.
7. Cost of equity = 2.5% + 1.1124 × 7.127% = 10.4288%. After-tax cost of debt = 3.5% × 0.60 = 2.10%.
8. Total capital = 92,521.47. Weights: equity 97.6365%, debt 2.3635%.
9. **WACC = 0.976365 × 10.4288% + 0.023635 × 2.10% = 10.23%.**

**Determinism:**
- DETERMINISTIC: the entire pipeline once the approach flags and raw inputs are set. Given {shares, price, lease schedule, book debt, interest expense, maturity, riskfree rate, tax rate, industry name, revenue-by-region, convertible terms, preferred terms}, a script produces the WACC with no discretion, including the fixed-point iteration.
- JUDGMENT: every approach flag. Which beta approach, which ERP approach, which cost-of-debt approach, which tax approach, and firm type 1 or 2 for the synthetic rating. Those choices need the firm's business mix, geographic revenue mix, rating status, size and jurisdiction.
- JUDGMENT: the direct-input beta branch is ambiguous even in the model — it is not exercised in the saved file, so whether a directly supplied regression beta should be unlevered and relevered or used as-is must be stated by the implementer. The convention in this spreadsheet family is to use it directly as the levered beta.
- JUDGMENT: the seed value and stopping rule for the iteration when the model oscillates between adjacent rating brackets.

**Pitfalls:**
- Running the steps out of order — computing the rating before capitalizing leases produces a different rating and a different cost of debt.
- Leaving iterative calculation off, which yields a reference error or a silently stale cost of debt.
- Assuming the dropdown selection determines the tax rate. The saved file's manually overridden tax cell shows otherwise.
- Using revenue weights instead of value weights in the multi-business beta. The model uses revenues × EV/Sales to get value, then weights by value.
- Forgetting that the preferred component enters the total capital denominator even when its cost is irrelevant.
- Treating the industry-average tables as current. They are a January snapshot and need refreshing.

**Sources:**
- spreadsheet doc `valuation-inputs-1` — wacccalc.xls, all sheets: `Cost of Capital worksheet`, `Operating lease converter`, `Synthetic rating`, `Industry Averages(US)`, `Global industry averages`, `Country risk and taxes`, `Country equity risk premiums`, `Answer keys`; plus the reimplementation notes and edge cases
- spreadsheet doc `corpfin-ratings-risk` — ratings.xls, the standalone version of the rating/lease loop and its iteration requirement
- corporate_finance--lecture_slides--cfpacket1spr20 p.200, p.203
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.115
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.112

**Related:** [[cost-of-capital-assembly]], [[synthetic-rating]], [[interest-coverage-ratio]], [[operating-leases-as-debt]], [[market-value-of-debt]], [[market-value-weights]], [[convertible-debt-decomposition]], [[preferred-stock-cost]], [[country-risk-in-cost-of-debt]], [[bottom-up-beta]], [[equity-risk-premium]]

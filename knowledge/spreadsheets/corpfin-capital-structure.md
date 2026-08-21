# Damodaran Corporate Finance — Capital Structure Models

Source files (from Damodaran's 2020 spreadsheet collection, "Corporate Finance Spreadsheets"):
`capstru.xlsx`, `apv.xls`, `levbeta.xls`, `macrodur.xls`.

Notation used below: `t` = marginal tax rate, `rf` = riskfree (long-term government bond) rate, `ERP` = equity risk premium, `kd` = pre-tax cost of debt, `ke` = cost of equity, `d` = debt-to-capital ratio D/(D+E). Cell references are `Sheet!Cell`. `.xls` files dump computed values only, so every formula in those sections is reconstructed from labels/values and marked "(inferred)"; all inferred formulas were numerically verified against the values in the sheet unless noted.

---

### capstru.xlsx

**Purpose:** Cost-of-capital approach to the **optimal capital structure** of a non-financial firm. At each debt ratio from 0% to 90% (10% steps) the model relevers beta, computes a synthetic bond rating from the interest coverage ratio, gets a pre-tax cost of debt from the rating, computes WACC, and values the firm; the optimal debt ratio is the one that **maximizes firm value** (not necessarily the one that minimizes WACC, if indirect bankruptcy costs are on). Includes the post-2017 US tax-reform option limiting interest deductibility to 30% of EBITDA (through 2022) or EBIT (after). Damodaran uses it in Applied Corporate Finance ch. 8 / Corporate Finance: Theory and Practice ch. 18. **The workbook is deliberately circular** (interest rate at each debt level depends on coverage, which depends on the interest rate); Excel iteration must be on — a Python port must solve each debt-level's rating/rate by fixed-point iteration.

Sheets: `READ ME 1ST`, `FAQs` (documentation only), `Inputs`, `Marginal tax rate by country` (reference), `Operating leases`, `Default Spreads and Ratios`, `Optimal Capital Structure` (main engine), `Repurchase price Worksheet`, `Summary Table`, `Input choices page` (dropdown lists + indirect-bankruptcy-cost table), `Sheet1` (empty).

#### Inputs (sheet `Inputs`) — example values are for Facebook, Jan 2019

| Label | Cell | Example value |
|---|---|---|
| Company name | B7 | Facebook |
| Date of analysis | B8 | 2019-01-01 |
| EBITDA (earnings before interest, depreciation & amortization) | B10 | 19565 (=17484+2081) |
| Depreciation and amortization | B11 | 2081 |
| Capital spending | B12 | 5739 |
| Interest expense on debt | B13 | 10 |
| Marginal tax rate (for pre-tax cost of debt) | B14 | 0.40 |
| Current bond rating on debt (if available) | B15 | "Not rated" |
| Current pre-tax cost of debt | B16 | 0.0322 |
| Number of shares outstanding | B18 | 2905.8 |
| Market price per share | B19 | 190 |
| Beta of the stock | B20 | 1.05 |
| Cash and marketable securities | B21 | 38289 |
| Book value of debt | B22 | 0 |
| Can you estimate MV of interest-bearing debt? (Yes/No) | B23 | No |
| If so, market value of interest-bearing debt | B24 | (blank) |
| Do you want me to estimate MV of debt? (Yes/No) | B25 | No |
| If yes, weighted average maturity of debt (yrs) | B26 | 7.9226 |
| Do you have any operating leases? (Yes/No) | B27 | Yes |
| Restrictions on interest deductions for tax? (Yes/No) | B29 | No |
| If yes, measure the restriction is tied to (EBITDA/EBIT) | B30 | EBITDA |
| Max % of that measure deductible | B31 | 0.30 |
| Incorporate indirect bankruptcy costs? (Yes/No) | B33 | No |
| If yes, magnitude of indirect bankruptcy costs (Low/Medium/High) | B34 | Medium |
| Current riskfree rate (currency of analysis) | B36 | 0.0255 |
| Equity risk premium (CAPM) | B37 | 0.0596 |
| Country default spread (added to cost of debt) | B38 | 0 |
| Which spread/ratio table (1 = large/stable firms, 2 = small/risky firms) | B41 | 1 |
| Assume existing debt refinanced at the 'new' rate? (Yes/No) | B42 | Yes |
| Adjust current rating & cost of debt to synthetic rating? (Yes/No) | B43 | Yes |

All numbers in consistent units (000s, millions, billions). Units of B10–B13, B21, B22: currency; B18 in shares (same scale).

#### Logic

**Step 1 — Operating lease conversion (sheet `Operating leases`)**, used only if `Inputs!B27="Yes"`.
Inputs on this sheet: current-year operating lease expense `E7` (269); lease commitments years 1–5 `B10:B14` (277, 284, 272, 256, 220); lump sum for "year 6 and beyond" `B15` (1131); reported EBIT `D20 = Inputs!B10-Inputs!B11` (17484); reported interest `D21 = Inputs!B13` (10).

- Discount rate: `C17 = IF(Inputs!B43="Yes", 'Default Spreads and Ratios'!D10, Inputs!B16)` → synthetic-rating-based kd if adjusting to synthetic (circular with step 2), else the entered kd. Example: 0.0321603.
- Years embedded in the year-6 lump: `D23 = ROUND(B15/AVERAGE(B10:B14), 0)` → ROUND(1131/261.8)=4.
- PV of each of years 1–5: `C27..C31 = B_yr/(1+C17)^yr`.
- Year-6+ annuity payment: `B32 = IF(B15>0, IF(D23>0, B15/D23, B15), 0)` → 282.75.
- PV of the year-6+ annuity (as a D23-year annuity deferred 5 years): `C32 = IF(D23>0, (B32*(1-(1+C17)^(-D23))/C17)/(1+C17)^5, B15/(1+C17)^6)` → 892.55.
- **Debt value of leases** `C33 = SUM(C27:C32)` → 2088.20.
- **Restated EBIT** `F36 = D20 + E7 - C33/(5+D23)` → 17484 + 269 − 2088.20/9 = 17520.98 (adds back lease expense, subtracts straight-line depreciation of the lease "asset" over 5+D23 years).
- **Restated interest expense** `F37 = D21 + C33*C17` → 10 + 67.157 = 77.157.
- **Restated depreciation** `F38 = Inputs!B11 + C33/(5+D23)` → 2081 + 232.02 = 2313.02.

**Step 2 — Synthetic rating for the current firm (sheet `Default Spreads and Ratios`)**
- `C2 = Inputs!B41` (table choice). EBIT used: `F3 = IF(Inputs!B27="Yes", 'Operating leases'!F36, Inputs!B10-Inputs!B11)`. Interest used: `F4 = IF(Inputs!B27="Yes", Inputs!B13 + 'Operating leases'!C33*'Operating leases'!C17, Inputs!B13)`. `F5 = Inputs!B36` (rf).
- Interest coverage ratio: `D7 = IF(F4>0, F3/F4, 10000000)` → 227.08.
- Estimated rating: `D8 = IF(C2=1, VLOOKUP(D7, A15:D29, 3), IF(C2=2, VLOOKUP(D7, A34:D48, 3), ...))` — approximate-match VLOOKUP on the coverage table below (largest lower bound ≤ coverage). → "Aaa/AAA".
- Estimated default spread: `D9 = VLOOKUP(D7, table, 4) + Inputs!B38` (country default spread added) → 0.0066603.
- Estimated cost of debt: `D10 = F5 + D9` → 0.0321603.

**Step 3 — Main engine (sheet `Optimal Capital Structure`)**

Current-firm block:
- MV equity `C4 = Inputs!B18*Inputs!B19` → 552,102.
- MV interest-bearing debt `C5 = IF(Inputs!B23="Yes", Inputs!B24, IF(Inputs!B25="Yes", Inputs!B13*(1-(1+Inputs!B16)^(-Inputs!B26))/Inputs!B16 + Inputs!B22/(1+Inputs!B16)^Inputs!B26, Inputs!B22))` — i.e. use given MV; else, if estimating, price the book debt as a bond (interest expense as coupon annuity over the average maturity + book value as face, discounted at kd); else book value. → 0.
- Lease debt `C7 = IF(Inputs!B27="Yes", 'Operating leases'!C33, 0)` → 2088.20.
- Adjusted EBITDA `I4 = IF(Inputs!B27="Yes", 'Operating leases'!F36+'Operating leases'!F38, Inputs!B10)` → 19834. Depreciation `I5 = IF(leases,'Operating leases'!F38, Inputs!B11)` → 2313.02. Interest `I8 = IF(leases,'Operating leases'!F37, Inputs!B13)` → 77.157. Tax rate `I6 = Inputs!B14`; capex `I7 = Inputs!B12`; beta `F4 = Inputs!B20`; rating `F5 = Inputs!B15`; rf `F7 = Inputs!B36`; kd `F8 = Inputs!B16`; ERP `C8 = Inputs!B37`.
- Enterprise value `J14 = C4+C5+C7-Inputs!B21` → 552,102+0+2088.20−38,289 = 515,901.20.
- Current D/(D+E) `E12 = (C5+C7)/(C5+C7+C4)` → 0.0037680.
- Current ke `E15 = F7 + F4*C8` → 0.0255+1.05×0.0596 = 0.088080.
- Current interest coverage `K25 = IF(I8>0, (F42-J41)/I8, 10000000)` where F42=current EBITDA (I4), J41=current depreciation (I5), i.e. EBIT/interest → 227.08; synthetic rating `K26 = VLOOKUP(K25, D82:G96, 3)`; synthetic rate `K27 = VLOOKUP(K25, D82:G96, 4)` → 0.0321603; drop in operating income at current rating `K30 = VLOOKUP(K25, D82:H96, 5)` → 0.
- Company's current interest rate `J42 = IF(Inputs!B43="Yes", K27, F8)`.
- Current after-tax cost of debt `E17 = IF(Inputs!B43="Yes", K27*(1-I6), F8*(1-I6))` → 0.0192962.
- Current WACC `E19 = E15*(1-E12) + E17*E12` → 0.0878208.
- Current FCFF `J16 = (I4-I5)*(1-I6) + I5 - I7` (working capital ignored) → 7086.61.
- **Implied growth rate** `J17 = IF(J16>0, (J14*J15 - J16)/(J14 + J16), "NA")` with J15=E19 (current WACC) → 0.0730806. This is the perpetual growth g solving EV = FCFF·(1+g)/(WACC−g).
- Growth used for perpetual-growth valuation `E20 = IF(J17>F7, F7, IF(J17="NA", 6%, J17))` — capped at rf → 0.0255.
- Adjusted (distress-normalized) EBITDA `F44 = IF(B42=0, F42, F42/(1+K30))` where B42 = current total debt (C5+C7) and K30 = drop-in-EBITDA fraction for the current synthetic rating (≤0) — i.e. gross EBITDA up to what it would be without current distress → 19834.

Ratings/interest worksheet (rows 46–68), one column per debt ratio d ∈ {0, 0.1, …, 0.9}:
- `D/E = d/(1-d)` (row 47).
- `$Debt = d*(B42+F41)` = d × (current debt + current equity) — capital base held fixed at current total capital (row 48).
- **Unlevered beta** `B49 = B41/(1+(1-B43)*B42/F41)` (current beta unlevered at current D/E with marginal tax rate; the trailing `*(1+(1-B43)*B47)` term is ×1 since B47=0) → 1.0476226.
- **Levered beta** at d: `row49 = B49*(1+(1-t_d)*D/E_d)` where `t_d` = row-68 tax rate for that column (so the relever uses the possibly-reduced tax rate).
- **Cost of equity** `row50 = rf + beta_d*ERP`.
- % drop in EBITDA `row51 = VLOOKUP(coverage_d(row 62), D82:H96, 5)` (0 for the d=0 column).
- EBITDA at d `row52 = IF(Inputs!B33="No", F44, F44*(1+drop_d))` — indirect bankruptcy costs shrink EBITDA with worsening rating.
- Depreciation `row53` = current depreciation (constant). EBIT `row54 = EBITDA_d − deprec`.
- **Interest expense** `row55 = IF(Inputs!B42="Yes", rate_d*Debt_d, IF(d < E12, (Inputs!B13/Inputs!B22)*Debt_d, Inputs!B13 + rate_d*(Debt_d - C5)))` — if refinancing, all debt at the new rate (circular with rows 62–65); if not refinancing, existing debt keeps its old average rate (interest/book debt) and only incremental debt pays the new rate.
- Taxable income `row56 = EBIT − interest`; Tax `row57`: if no deduction restriction (`Inputs!B29="No"`): `t*TaxableIncome`; if restriction tied to EBITDA: `IF(interest < B31*EBITDA, t*TaxableIncome, (EBIT - B31*EBITDA)*t)`; if tied to EBIT: `IF(interest < B31*EBIT, t*TaxableIncome, (EBIT - B31*EBIT)*t)`. (Note: tax can be negative — full loss offset assumed.)
- Net income `row58 = row56 − row57`; +Deprec `row59`; Funds from operations `row60 = NI + deprec`.
- **Pre-tax interest coverage** `row62 = TaxableIncome/Interest + 1` (= EBIT/interest); shown as "∞" for the zero-debt column. `Funds/Debt row63 = FFO/Debt`.
- **Likely rating** `row64 = VLOOKUP(coverage, D82:G96, 3)` (d=0 column hardcoded to the top rating F96); **pre-tax cost of debt** `row65 = VLOOKUP(coverage, D82:G96, 4)` (d=0 column = G96, the AAA rate). The lookup table D82:H96 (see Reference data) holds rate = default spread + rf + country default spread.
- Tax rate under the deduction constraint `row66`: if `Inputs!B29="No"` → t; if measure = EBIT: `IF(interest < B31*EBIT, t, t*(B31*EBIT)/interest)`; else (EBITDA): `IF(interest < B31*EBITDA, t, t*(B31*EBITDA)/interest)`.
- Tax rate under the interest>EBIT limit `row67 = IF(interest < EBIT, t, t*EBIT/interest)` (tax benefit only on interest covered by EBIT).
- **Tax rate for after-tax kd** `row68 = MIN(row66, row67)`.

Cost-of-capital block (rows 70–77):
- `Cost of equity row73 = row50`; **after-tax cost of debt** `row74 = row65*(1-row68)`; **WACC** `row75 = ke_d*(1-d) + kd_after_tax_d*d`.
- **Firm value at each d** `row77`: if `Inputs!B33="No"` (no indirect bankruptcy costs) **or** implied growth is "NA":
  `V_d = E21*(1 + (E19 - WACC_d)/(WACC_d - E20))` — current EV grown by the perpetuity effect of the WACC change, with growth E20 (= min(implied g, rf); the annualized savings (WACC_current−WACC_d)×EV are valued as a growing perpetuity at (WACC_d − g)).
  Otherwise (IBC on and implied g available): `V_d = (EBIT_d*(1-t) - (I7 - I5))*(1+J17)/(WACC_d - J17)` — FCFF perpetuity with the implied growth rate (note: here EBIT_d already reflects the EBITDA drop; net capex uses current capex−current depreciation).
- Optimal selector `row76 = IF(V_d = MAX(all V), 1, 0)`; optimal outputs are sumproducts of row 76 with the respective rows: `F12` optimal debt ratio (Σ ind×d), `F14` optimal beta, `F15` optimal ke, `F17` optimal after-tax kd, `F19` optimal WACC, `F21` optimal firm value.
- Value per share: current `E22 = (E21 + Inputs!B21 - C5 - C7)/C6` (EV + cash − debt − leases over shares) → 190; at optimal `F22 = (F21-E21)/C6 + E22` — the entire value gain accrues to today's shareholders → 206.75.

**Step 4 — Repurchase price worksheet** (what happens if the firm levers up to the optimal and buys back stock at a chosen price):

| Item | Cell | Formula | Example |
|---|---|---|---|
| Current stock price | B2 | `='Optimal Capital Structure'!E22` | 190 |
| Shares before buyback | B3 | `=Inputs!B18` | 2905.8 |
| Expected buyback price | B4 | user input | 67.71 |
| Current debt | B6 | `='Optimal Capital Structure'!B42` | 2088.20 |
| Debt at optimal | B7 | `=F12*(B42+F41)` | 110,838.04 |
| New debt issued | B8 | `=B7-B6` | 108,749.84 |
| Shares bought back | B9 | `=B8/B4` | 1606.11 |
| Shares after buyback | B10 | `=B3-B9` | 1299.69 |
| Enterprise value after buyback | B12 | `='Optimal Capital Structure'!F21` | 564,585.24 |
| Equity value after buyback | B15 | `=B12+Inputs!B21-B7` (EV + cash − debt) | 492,036.20 |
| Value per remaining share | B17 | `=B15/B10` | 378.58 |

**Summary Table sheet:** pure display — two tables (debt ratio → beta, ke, rating, kd, tax rate, after-tax kd, WACC, enterprise value; and debt ratio → $debt, interest, coverage, rating, kd, tax rate, after-tax kd), all cell references into `Optimal Capital Structure` (rows 48/49/55/62/64/65/67/73/77). Note the tax-rate column shown is row 67 (interest-limit tax rate), and after-tax kd is recomputed as `E*(1-F)`.

#### Reference data

**Ratings table 1 — "For large manufacturing firms"** (`Default Spreads and Ratios'!A15:E29`; used when `Inputs!B41=1`). Lookup: interest coverage ratio > col1 and ≤ col2 → rating, default spread, drop in EBITDA (for indirect bankruptcy costs).

| Coverage > | Coverage ≤ | Rating | Default spread | Drop in EBITDA |
|---|---|---|---|---|
| -100000 | 0.199999 | D2/D | 0.14335607034015696 | -0.50 |
| 0.2 | 0.649999 | C2/C | 0.10755403832538094 | -0.40 |
| 0.65 | 0.799999 | Ca2/CC | 0.088 | -0.40 |
| 0.8 | 1.249999 | Caa/CCC | 0.0777645323482633 | -0.40 |
| 1.25 | 1.499999 | B3/B- | 0.046159909223396155 | -0.25 |
| 1.5 | 1.749999 | B2/B | 0.03776719845550594 | -0.20 |
| 1.75 | 1.999999 | B1/B+ | 0.03147266537958828 | -0.20 |
| 2 | 2.2499999 | Ba2/BB | 0.02152617442092565 | -0.20 |
| 2.25 | 2.49999 | Ba1/BB+ | 0.019341413179589748 | -0.20 |
| 2.5 | 2.999999 | Baa2/BBB | 0.01591065804294902 | -0.10 |
| 3 | 4.249999 | A3/A- | 0.012863935805589465 | -0.02 |
| 4.25 | 5.499999 | A2/A | 0.011379635520329143 | 0 |
| 5.5 | 6.499999 | A1/A+ | 0.010307640869863355 | 0 |
| 6.5 | 8.499999 | Aa2/AA | 0.008246112695890684 | 0 |
| 8.5 | 100000 | Aaa/AAA | 0.006660321792834782 | 0 |

**Ratings table 2 — "For smaller and riskier firms"** (`A34:E48`; used when `Inputs!B41=2`). Same ratings/spreads/drops as table 1 (columns D and E reference table 1 cell-for-cell), but with **higher coverage thresholds**:

| Coverage > | Coverage ≤ | Rating | Default spread | Drop in EBITDA |
|---|---|---|---|---|
| -100000 | 0.499999 | D2/D | 0.14335607034015696 | -0.50 |
| 0.5 | 0.799999 | C2/C | 0.10755403832538094 | -0.40 |
| 0.8 | 1.249999 | Ca2/CC | 0.088 | -0.40 |
| 1.25 | 1.499999 | Caa/CCC | 0.0777645323482633 | -0.40 |
| 1.5 | 1.999999 | B3/B- | 0.046159909223396155 | -0.25 |
| 2 | 2.499999 | B2/B | 0.03776719845550594 | -0.20 |
| 2.5 | 2.999999 | B1/B+ | 0.03147266537958828 | -0.20 |
| 3 | 3.499999 | Ba2/BB | 0.02152617442092565 | -0.20 |
| 3.5 | 3.9999999 | Ba1/BB+ | 0.019341413179589748 | -0.20 |
| 4 | 4.499999 | Baa2/BBB | 0.01591065804294902 | -0.10 |
| 4.5 | 5.999999 | A3/A- | 0.012863935805589465 | -0.02 |
| 6 | 7.499999 | A2/A | 0.011379635520329143 | 0 |
| 7.5 | 9.499999 | A1/A+ | 0.010307640869863355 | 0 |
| 9.5 | 12.499999 | Aa2/AA | 0.008246112695890684 | 0 |
| 12.5 | 100000 | Aaa/AAA | 0.006660321792834782 | 0 |

The main-sheet working copy (`'Optimal Capital Structure'!D82:H96`) mirrors the chosen table with **interest rate = default spread + rf + country default spread** in column G.

**Indirect bankruptcy cost table (`Input choices page'!A19:D34`)** — drop in EBITDA by rating for Low/Medium/High IBC. The "Drop in EBITDA" column actually wired into the ratings tables equals the **Medium** column; `Inputs!B34` (Low/Medium/High) exists as a dropdown, and to honor it a port should substitute the corresponding column below for the drop values:

| Rating | Low IBC | Medium | High IBC |
|---|---|---|---|
| D2/D | -0.30 | -0.50 | -1.00 |
| Caa/CCC | -0.25 | -0.40 | -0.50 |
| Ca2/CC | -0.25 | -0.40 | -0.50 |
| C2/C | -0.25 | -0.40 | -0.50 |
| B3/B- | -0.15 | -0.25 | -0.30 |
| B2/B | -0.10 | -0.20 | -0.25 |
| B1/B+ | -0.10 | -0.20 | -0.25 |
| Ba2/BB | -0.10 | -0.20 | -0.25 |
| Ba1/BB+ | -0.10 | -0.20 | -0.25 |
| Baa2/BBB | -0.05 | -0.10 | -0.15 |
| A3/A- | 0 | -0.02 | -0.05 |
| A2/A | 0 | 0 | -0.02 |
| A1/A+ | 0 | 0 | 0 |
| Aa2/AA | 0 | 0 | 0 |
| Aaa/AAA | 0 | 0 | 0 |

Other dropdown lists on `Input choices page`: ratings list (Aaa/AAA … D2/D, "Not rated"), Yes/No, IBC magnitude (High/Medium/Low), type of firm (1/2), earnings measure (EBITDA/EBIT).

**Marginal tax rate by country (sheet `Marginal tax rate by country`)** — informational lookup for choosing `Inputs!B14` (KPMG-style 2021 corporate marginal rates; not referenced by any formula). Verbatim:

| Country | Tax rate in 2021 |
|---|---|
|---|---|
| Afghanistan | 0.2 |
| Albania | 0.15 |
| Algeria | 0.26 |
| Andorra | 0.1 |
| Angola | 0.25 |
| Anguilla | 0 |
| Antigua and Barbuda | 0.25 |
| Argentina | 0.25 |
| Armenia | 0.18 |
| Aruba | 0.25 |
| Australia | 0.3 |
| Austria | 0.25 |
| Azerbaijan | 0.2 |
| Bahamas | 0 |
| Bahrain | 0 |
| Bangladesh | 0.325 |
| Barbados | 0.055 |
| Belarus | 0.18 |
| Belgium | 0.25 |
| Benin | 0.3 |
| Bermuda | 0 |
| Bolivia | 0.25 |
| Bonaire, Saint Eustatius and Saba | 0.25 |
| Bosnia and Herzegovina | 0.1 |
| Botswana | 0.22 |
| Brazil | 0.34 |
| Brunei Darussalam | 0.185 |
| Bulgaria | 0.1 |
| Burkina Faso | 0.28 |
| Burundi | 0.3 |
| Cambodia | 0.2 |
| Cameroon | 0.33 |
| Canada | 0.265 |
| Cayman Islands | 0 |
| Chile | 0.27 |
| China | 0.25 |
| Colombia | 0.31 |
| Congo | 0.28 |
| Congo (Democratic Republic of the) | 0.3 |
| Costa Rica | 0.3 |
| Croatia | 0.18 |
| Curacao | 0.22 |
| Cyprus | 0.125 |
| Czech Republic | 0.19 |
| Denmark | 0.22 |
| Djibouti | 0.25 |
| Dominica | 0.25 |
| Dominican Republic | 0.27 |
| Ecuador | 0.25 |
| Egypt | 0.225 |
| El Salvador | 0.3 |
| Estonia | 0.2 |
| Ethiopia | 0.3 |
| Fiji | 0.2 |
| Finland | 0.2 |
| France | 0.265 |
| Gabon | 0.3 |
| Gambia | 0.27 |
| Georgia | 0.15 |
| Germany | 0.3 |
| Ghana | 0.25 |
| Gibraltar | 0.1 |
| Greece | 0.24 |
| Grenada | 0.28 |
| Guatemala | 0.25 |
| Guernsey | 0 |
| Honduras | 0.25 |
| Hong Kong SAR | 0.165 |
| Hungary | 0.09 |
| Iceland | 0.2 |
| India | 0.3 |
| Indonesia | 0.22 |
| Iraq | 0.35 |
| Ireland | 0.125 |
| Isle of Man | 0 |
| Israel | 0.23 |
| Italy | 0.24 |
| Ivory Coast | 0.25 |
| Jamaica | 0.25 |
| Japan | 0.3062 |
| Jersey | 0 |
| Jordan | 0.2 |
| Kazakhstan | 0.2 |
| Kenya | 0.3 |
| Korea, Republic of | 0.25 |
| Kuwait | 0.15 |
| Kyrgyzstan | 0.1 |
| Latvia | 0.2 |
| Lebanon | 0.17 |
| Libya | 0.2 |
| Liechtenstein | 0.125 |
| Lithuania | 0.15 |
| Luxembourg | 0.2494 |
| Macau | 0.12 |
| Macedonia | 0.1 |
| Madagascar | 0.2 |
| Malawi | 0.3 |
| Malaysia | 0.24 |
| Malta | 0.35 |
| Mauritania | 0.25 |
| Mauritius | 0.15 |
| Mexico | 0.3 |
| Moldova | 0.12 |
| Monaco | 0.33 |
| Mongolia | 0.25 |
| Montenegro | 0.09 |
| Morocco | 0.31 |
| Mozambique | 0.32 |
| Myanmar | 0.25 |
| Namibia | 0.32 |
| Netherlands | 0.25 |
| New Zealand | 0.28 |
| Nicaragua | 0.3 |
| Nigeria | 0.3 |
| Norway | 0.22 |
| Oman | 0.15 |
| Pakistan | 0.29 |
| Palestinian Territory | 0.15 |
| Panama | 0.25 |
| Papua New Guinea | 0.3 |
| Paraguay | 0.1 |
| Peru | 0.295 |
| Philippines | 0.3 |
| Poland | 0.19 |
| Portugal | 0.21 |
| Qatar | 0.1 |
| Romania | 0.16 |
| Russia | 0.2 |
| Rwanda | 0.3 |
| Saint Kitts and Nevis | 0.33 |
| Saint Lucia | 0.3 |
| Saint Vincent and the Grenadines | 0.3 |
| Samoa | 0.27 |
| Saudi Arabia | 0.2 |
| Senegal | 0.3 |
| Serbia | 0.15 |
| Sierra Leone | 0.3 |
| Singapore | 0.17 |
| Sint Maarten (Dutch part) | 0.35 |
| Slovakia | 0.21 |
| Slovenia | 0.19 |
| Solomon Islands | 0.3 |
| South Africa | 0.28 |
| Spain | 0.25 |
| Sri Lanka | 0.24 |
| St Maarten | 0.35 |
| Sudan | 0.35 |
| Suriname | 0.36 |
| Swaziland | 0.275 |
| Sweden | 0.20600000000000002 |
| Switzerland | 0.1493 |
| Syria | 0.28 |
| Taiwan | 0.2 |
| Tanzania | 0.3 |
| Thailand | 0.2 |
| Trinidad and Tobago | 0.3 |
| Tunisia | 0.15 |
| Turkey | 0.2 |
| Turkmenistan | 0.2 |
| Turks and Caicos Islands | 0 |
| Uganda | 0.3 |
| Ukraine | 0.18 |
| United Arab Emirates | 0.55 |
| United Kingdom | 0.19 |
| United States | 0.27 |
| Uruguay | 0.25 |
| Uzbekistan | 0.075 |
| Vanuatu | 0 |
| Venezuela | 0.34 |
| Vietnam | 0.2 |
| Yemen | 0.2 |
| Zambia | 0.35 |
| Zimbabwe | 0.24 |
| Americas average | 0.2733 |
| Asia average | 0.2113 |
| EU average | 0.2087 |
| Europe average | 0.1912 |
| Global average | 0.2379 |
| Latin America average | 0.2736 |
| North America average | 0.2675 |
| Oceania average | 0.2843 |
| OECD average | 0.2305 |
| South America average | 0.2736 |

#### Outputs

Summary on `Inputs!E9:G15` (mirrors `Optimal Capital Structure`): current vs optimal **debt-to-capital** (`E12`/`F12`: 0.00377 → 0.20), **cost of capital** (`E19`/`F19`: 8.782% → 8.245%), **enterprise value** (`J14`/`F21`: 515,901.20 → 564,585.24), **value per share** (`E22`/`F22`: 190 → 206.75). Plus the per-debt-ratio schedule (Summary Table) and the buyback price analysis (`Repurchase price Worksheet'!B17`).

#### Worked example (Facebook, values in the sheet)

1. Leases: debt value 2088.20 at kd=3.21603%; restated EBIT 17,520.98, restated interest 77.157, restated depreciation 2313.02, EBITDA 19,834.
2. Current: coverage = (19834−2313.02)/77.157 = 227.08 → Aaa/AAA, spread 0.66603%, kd = 2.55%+0.666% = 3.216%; ke = 8.808%; D/(D+E) = 2088.2/554,190.2 = 0.377%; WACC = 8.782%; EV = 515,901.2; FCFF = 17,520.98×0.6+2313.02−5739 = 7086.61; implied g = (515,901.2×0.08782−7086.61)/(515,901.2+7086.61) = 7.308% → capped at rf = 2.55%.
3. Unlevered beta = 1.05/(1+0.6×2088.2/552,102) = 1.04762.
4. Schedule (d: beta, rating, pre-tax kd, tax rate row 68, WACC, firm value):
   - 0%: 1.04762, Aaa/AAA, 3.216%, 0.40, 8.794%, 514,930.5
   - 10%: 1.11746, Aaa/AAA (cov 9.83), 3.216%, 0.40, 8.482%, 541,995.5
   - 20%: 1.20477, A3/A- (cov 4.12), 3.836%, 0.40, **8.245%**, **564,585.2** ← optimal
   - 30%: 1.31701, Caa/CCC (cov 1.02), 10.326%, 0.40, 9.138%, 488,004.9
   - 40%: 1.58008, C2/C (cov 0.594), 13.305%, 0.23761 (interest 29,494.9 > EBIT so t×EBIT/interest), 11.238%, 370,069.8
   - 50%–90%: rating stays C2/C at kd 13.305%; tax rate falls (0.19009, 0.15841, 0.13578, 0.11881, 0.10561); WACC rises 12.313% → 16.616%; value falls 329,303.0 → 228,581.2.
5. Optimal d = 0.20; value gain 48,684.04; value/share 190 → 206.75. Buyback at 67.71: 108,749.8 new debt buys 1606.11 shares; remaining-share value 378.58.

#### Reimplementation notes

- Inputs: as listed above (floats; rates as decimals; Yes/No booleans; table_choice ∈ {1,2}; restriction_measure ∈ {EBITDA, EBIT}; ibc_magnitude ∈ {Low, Medium, High}; lease commitments list of 5 + lump).
- **Circularity #1 (lease kd):** if `adjust_to_synthetic`, lease discount rate = synthetic kd, which depends on restated EBIT/interest, which depend on lease debt value. Iterate to convergence (start from entered kd).
- **Circularity #2 (per-debt-level rate):** with refinancing, interest = rate×debt and rate = f(EBIT/interest). Solve by fixed-point iteration per column (a stable approach: iterate rating→rate→interest→coverage→rating until the rating stops changing; may cycle between two ratings — Excel's iteration settles on one; detect 2-cycles and pick the worse rating or dampen).
- VLOOKUP is **approximate-match on the lower-bound column**: rating row = last row whose lower bound ≤ coverage. Coverage for zero debt is +∞ → top rating hard-coded.
- Edge cases:
  - Zero interest → coverage set to 10,000,000 (top rating).
  - Negative EBIT gives negative coverage → D rating (lower bound −100,000).
  - Negative taxable income produces negative tax (full offset assumed). The *tax-benefit* rate (rows 66–68) still caps the after-tax kd benefit.
  - FCFF ≤ 0 → implied growth = "NA" → use the perpetual-growth branch with g fixed at min(rf, 6% default).
  - B42=0 (no current debt) skips the EBITDA normalization.
  - Current book debt = 0 makes the non-refinancing branch divide by `Inputs!B22`. Require refinance=Yes or debt>0.
- Do not forget: capital base for $Debt is (current MV equity + current total debt incl. leases), constant across d; EV subtracts cash; the drop-in-EBITDA feature only affects EBITDA when `indirect_bankruptcy_costs=Yes`, but rows 51's lookup runs regardless.

---

### apv.xls

**Purpose:** **Adjusted Present Value** approach to optimal capital structure: Value(levered) = Value(unlevered) + PV(tax benefits of debt) − expected bankruptcy costs, evaluated at debt ratios 0–90%; the optimal is the ratio maximizing levered firm value. Companion to capstru (same course chapters); uses a ratings table that carries a **bankruptcy probability** per rating instead of a drop-in-EBITDA. Values-only .xls: all formulas below are (inferred) and were verified numerically. Example company: Hormel (analysis date 2009-04-21, Excel serial 39924).

Sheets: `READ ME FIRST`, `FAQs` (docs), `Inputs`, `Operating Lease Information`, `Default Spreads and Ratios`, `Adjusted Present Value` (engine), `Input choices page` (dropdown lists only: ratings list, Yes/No, High/Medium/Low, firm type 1/2).

#### Inputs (sheet `Inputs`)

| Label | Cell | Example |
|---|---|---|
| Company name | B2 | Hormel |
| Date of analysis | B3 | 39924 (2009-04-21) |
| EBITDA | B5 | 635 |
| Depreciation & amortization | B6 | 126 |
| Capital spending | B7 | 126 |
| Interest expense on debt | B8 | 28 |
| Tax rate on ordinary income | B9 | 0.40 |
| **Cost of bankruptcy as % of firm market value** | B10 | 0.25 |
| Current rating on debt (if available) | B11 | Aaa/AAA |
| Interest rate based upon rating | B12 | 0.0275 |
| Number of shares outstanding | B14 | 134.526 |
| Market price per share | B15 | 31.08 |
| Beta of the stock | B16 | 0.83 |
| Book value of debt | B17 | 450 |
| Can you estimate MV of outstanding debt? | B18 | No |
| If so, MV of debt | B19 | (blank) |
| Estimate MV of debt? | B20 | Yes |
| If yes, average maturity of debt (yrs) | B21 | 0 |
| Any operating leases? | B22 | Yes |
| Current LT government bond rate | B24 | 0.0235 |
| Risk premium (CAPM) | B25 | 0.06 |
| Country default spread | B26 | 0 |
| Spread/ratio table choice (1 large/stable, 2 smaller/riskier) | B29 | 2 |
| Existing debt refinanced at the new rate? | B30 | Yes |
| Adjust current rating to synthetic? | B31 | Yes |

#### Logic (all inferred, verified)

**Operating lease conversion (`Operating Lease Information`)** — same structure as capstru with one difference in the year-6 count and the EBIT restatement:
- Inputs: current lease expense E7=21.9; commitments yrs 1–5 B10:B14 = 10, 8.07, 6.76, 5.21, 4.51; yr-6+ lump B15 = 11.94; kd C17 = 0.0289 (synthetic, since B31=Yes); reported EBIT D20 = 509; reported interest D21 = 28.
- Years in yr-6 lump `D23 = INT(B15/AVERAGE(B10:B14))` → INT(11.94/6.91)=1. (capstru uses ROUND; here the value 1 only matches INT/TRUNC.)
- PV years 1–5 = commitment/(1+kd)^t; yr-6 annuity payment = B15/D23 = 11.94; PV = (11.94×(1−1.0289^−1)/0.0289)/1.0289^5 = 10.0639.
- Debt value of leases `C33 = ΣPV` = 42.1723.
- Restated EBIT `F36 = D20 + E7` = 509+21.9 = 530.9 (**adds back the full lease expense; no lease-depreciation subtraction in this older model**).
- Restated interest `F37 = D21 + C33*C17` = 28 + 1.2188 = 29.2188.

**Synthetic rating (`Default Spreads and Ratios`)**: firm type C2 = Inputs!B29 (=2); EBIT F3 = 530.9 (restated); interest F4 = 29.2188; rf F5 = 0.0235. Coverage `D7 = F3/F4` = 18.1698 (→ 10,000,000 if interest ≤ 0, per capstru pattern); rating `D8` via approximate VLOOKUP in the chosen table → Aaa/AAA; spread `D9` = 0.0054; cost of debt `D10 = rf + spread (+ country spread)` = 0.0289.

**Main engine (`Adjusted Present Value`)**
- MV equity `C4 = shares×price` = 4181.068; MV debt `C5` (same three-branch logic as capstru; here estimate-MV=Yes with maturity 0 collapses to book) = 450; lease debt `C7` = 42.1723; total current debt `B43 = C5+C7` = 492.1723.
- Current EBITDA `I4 = restated EBIT + depreciation` = 656.9; depreciation `I5` = 126; interest `I8` = 29.2188; tax `I6` = 0.4.
- Current firm value `D90 = C4 + C5 + C7` = 4673.240 (**cash is NOT subtracted in this model**).
- Tax benefit on current debt `D91 = t × (C5+C7)` = 0.4×492.1723 = 196.869.
- Expected current bankruptcy cost `D92 = p_current × BC% × D90` = 0.0007×0.25×4673.240 = 0.81782, where p_current = bankruptcy probability of the current (synthetic) rating and BC% = Inputs!B10.
- **Unlevered firm value** `D93 = D90 − D91 + D92` = 4477.189.
- For each debt ratio d ∈ {0,…,0.9}:
  - `$Debt_d = d × D90` (current firm value as capital base) — e.g. 0.1×4673.240 = 467.324.
  - Interest_d = kd_d × Debt_d (refinanced; kd_d from the synthetic-rating loop below — circular).
  - EBITDA/deprec/EBIT constant (no drop-in-EBITDA mechanism here); taxable income = EBIT − interest; tax = t×taxable (negative allowed); coverage = EBIT/interest ("∞" at d=0); FFO = NI + deprec; Funds/Debt = FFO/Debt.
  - Rating_d = approx-VLOOKUP(coverage) in the working table (rate = spread + rf: e.g. Aaa 0.0289, Ca2/CC 0.1298); p_default_d from the same row's bankruptcy probability. d=0 column hardcoded "AAA"/top rate/top-row probability.
  - Effective tax rate for the tax benefit `row68 = IF(interest < EBIT, t, t×EBIT/interest)` — e.g. at d=0.9: 0.4×530.9/545.928 = 0.388989.
  - **Tax benefits_d = t_eff_d × Debt_d** (e.g. 0.4×467.324 = 186.930; at 90%: 0.388989×4205.916 = 1636.055).
  - **Expected bankruptcy cost_d = p_default_d × BC% × (UnleveredValue + TaxBenefits_d)** — e.g. d=0.3: 0.0051×0.25×(4477.189+560.789) = 6.4234; d=0.9: 0.7×0.25×6113.24 = 1069.818.
  - **Levered firm value_d = UnleveredValue + TaxBenefits_d − ExpectedBankruptcyCost_d**.
  - Index variable row = 1 where levered value is the max.
- Ancillary beta/ke rows (not used in the APV value): unlevered beta = 0.83/(1+0.6×492.1723/4181.068) = 0.775245; levered beta_d = unl×(1+(1−t_eff_d)×D/E_d) (uses the column's effective tax rate — verified at d=0.9); ke_d = rf + beta_d×ERP.
- Outputs `F10 = MAX(levered values)` = 5823.311; `F11` = corresponding debt ratio = 0.8.

#### Reference data

**Ratings table 1 — "For large or stable firms"** (`Default Spreads and Ratios'!A15:E29`, table choice 1). Note the rating ladder ordering here differs from capstru in the B/BB range (Ba1/BB+ sits below Ba2/BB, B1/B+ below B2/B — kept verbatim):

| Coverage > | Coverage ≤ | Rating | Default spread | Bankruptcy probability |
|---|---|---|---|---|
| -100000 | 0.199999 | D2/D | 0.186025 | 1.00 |
| 0.2 | 0.649999 | C2/C | 0.13951875 | 0.85 |
| 0.65 | 0.799999 | Ca2/CC | 0.1063 | 0.70 |
| 0.8 | 1.249999 | Caa/CCC | 0.08636875 | 0.5901 |
| 1.25 | 1.499999 | B3/B- | 0.04365625 | 0.45 |
| 1.5 | 1.749999 | Ba1/BB+ | 0.03571875 | 0.10 |
| 1.75 | 1.999999 | Ba2/BB | 0.029765625 | 0.1663 |
| 2 | 2.2499999 | B1/B+ | 0.0238125 | 0.25 |
| 2.25 | 2.49999 | B2/B | 0.01984375 | 0.368 |
| 2.5 | 2.999999 | Baa2/BBB | 0.0127 | 0.0754 |
| 3 | 4.249999 | A3/A- | 0.01125 | 0.025 |
| 4.25 | 5.499999 | A2/A | 0.0099 | 0.0066 |
| 5.5 | 6.499999 | A1/A+ | 0.009 | 0.006 |
| 6.5 | 8.499999 | Aa2/AA | 0.0072 | 0.0051 |
| 8.5 | 100000 | Aaa/AAA | 0.0054 | 0.0007 |

**Ratings table 2 — "For smaller and riskier firms"** (`A35:E49`, table choice 2; used in the Hormel example):

| Coverage > | Coverage ≤ | Rating | Default spread | Bankruptcy probability |
|---|---|---|---|---|
| -100000 | 0.499999 | D2/D | 0.186025 | 1.00 |
| 0.5 | 0.799999 | C2/C | 0.13951875 | 0.85 |
| 0.8 | 1.249999 | Ca2/CC | 0.1063 | 0.70 |
| 1.25 | 1.499999 | Caa/CCC | 0.08636875 | 0.5901 |
| 1.5 | 1.999999 | B3/B- | 0.04365625 | 0.45 |
| 2 | 2.499999 | Ba1/BB+ | 0.03571875 | 0.10 |
| 2.5 | 2.999999 | Ba2/BB | 0.029765625 | 0.1663 |
| 3 | 3.499999 | B1/B+ | 0.0238125 | 0.25 |
| 3.5 | 3.9999999 | B2/B | 0.01984375 | 0.368 |
| 4 | 4.499999 | Baa2/BBB | 0.0127 | 0.0754 |
| 4.5 | 5.999999 | A3/A- | 0.01125 | 0.025 |
| 6 | 7.499999 | A2/A | 0.0099 | 0.0066 |
| 7.5 | 9.499999 | A1/A+ | 0.009 | 0.006 |
| 9.5 | 12.499999 | Aa2/AA | 0.0072 | 0.0051 |
| 12.5 | 100000 | Aaa/AAA | 0.0054 | 0.0007 |

Note the probability column is **non-monotonic** in places (Ba1/BB+ 0.10 < Ba2/BB 0.1663; B2/B 0.368 > Baa2 0.0754) — reproduce verbatim; this is why the levered value at d=0.8 (rating Ba1/BB+, p=0.10) beats d=0.7 (B1/B+, p=0.25) in the example.

#### Outputs

`F10` maximum firm value (5823.311), `F11` optimal debt ratio (0.80); APV schedule rows 106–116 (debt ratio, $debt, tax rate, unlevered value, tax benefits, rating, probability of default, expected bankruptcy cost, levered value); ratings comparison block (current coverage 18.170, synthetic rating Aaa/AAA, synthetic rate 0.0289, current rate 0.0275, current bankruptcy probability 0.0007).

#### Worked example (Hormel)

Unlevered value 4477.189. Full schedule:

| d | $ Debt | Tax benefit | Rating | p(default) | Expected bankruptcy cost | Levered value |
|---|---|---|---|---|---|---|
| 0.0 | 0 | 0 | AAA | 0.0007 | 0.784 | 4476.41 |
| 0.1 | 467.32 | 186.93 | Aaa/AAA | 0.0007 | 0.816 | 4663.30 |
| 0.2 | 934.65 | 373.86 | Aaa/AAA | 0.0007 | 0.849 | 4850.20 |
| 0.3 | 1401.97 | 560.79 | Aa2/AA | 0.0051 | 6.42 | 5031.55 |
| 0.4 | 1869.30 | 747.72 | A1/A+ | 0.006 | 7.84 | 5217.07 |
| 0.5 | 2336.62 | 934.65 | A2/A | 0.0066 | 8.93 | 5402.91 |
| 0.6 | 2803.94 | 1121.58 | A3/A- | 0.025 | 34.99 | 5563.77 |
| 0.7 | 3271.27 | 1308.51 | B1/B+ | 0.25 | 361.61 | 5424.09 |
| **0.8** | **3738.59** | **1495.44** | **Ba1/BB+** | **0.10** | **149.32** | **5823.31 (optimal)** |
| 0.9 | 4205.92 | 1636.06 (t_eff 0.388989) | Ca2/CC | 0.70 | 1069.82 | 5043.43 |

#### Reimplementation notes

- Inputs as listed (floats, decimals, booleans, table_choice ∈ {1,2}); bankruptcy cost fraction is a first-class input (0.25 example).
- Same two circularities as capstru (lease kd via synthetic rating; per-debt-level rate via coverage). Same approximate-match lookup semantics.
- Branches: MV-of-debt three-way branch (given MV / bond-price estimate / book); maturity 0 makes the bond-price estimate collapse to book value (annuity factor 0, discount factor 1); leases optional; d=0 column: coverage ∞, top rating, tax benefit 0, BC = p_top×BC%×V_unlev.
- Effective tax rate caps the tax benefit when interest > EBIT: t_eff = t×EBIT/interest (guard interest>0). Negative EBIT → coverage negative → D rating, p=1, t_eff for tax benefit should floor at 0 (sheet's example never hits EBIT<0; README states optimal will be 0% for persistently negative operating income).
- The FAQ/README differences vs capstru worth keeping: value base for $Debt is firm value **including cash** (no cash netting anywhere in apv), and there is no growing-perpetuity revaluation — APV is purely additive.

---

### levbeta.xls

**Purpose:** Utility to **unlever and relever betas**. Takes a regression beta (which reflects the average leverage over the regression period), unlevers it at the average D/E, then relevers it at the current D/E, a full 0–90% debt-ratio schedule, and any custom D/E. Uses the levered-beta formula β_L = β_u × (1 + (1−t)×D/E). Single populated sheet `Sheet1` (Sheet2–Sheet16 empty). Values-only .xls; formulas (inferred), all verified.

**Inputs:**

| Label | Cell | Example |
|---|---|---|
| Current (regression) beta of the company | E3 | 1.4 |
| Marginal tax rate | E4 | 0.36 |
| Average debt/equity ratio over the regression period | E5 | 0.14 |
| Current market value of equity | E7 | 50889.038 |
| Current book value of debt | E8 | 12342 |
| Average maturity of debt (yrs) | E9 | 5 |
| Interest expense, most recent 12 months | E10 | 876.282 |
| Current market interest rate on the company's debt | E11 | 0.075 |
| Estimated debt value of operating leases (optional) | A13 row | (blank) |
| Custom debt/equity ratio for relevering | E33 | 0.35 |

**Logic (inferred):**
- Market value of debt `E12 = E10×(1−(1+E11)^−E9)/E11 + E8/(1+E11)^E9` (interest as coupon annuity + book value as face, at the market rate) → 876.282×4.04588 + 12342×0.696559 = 12,142.263. (Operating lease debt, if entered, would be added to debt — inferred from label, not exercised in the sheet.)
- **Unlevered beta** `E17 = E3/(1+(1−E4)×E5)` = 1.4/(1+0.64×0.14) = 1.284875.
- **Current beta at current D/E** `E18 = E17×(1+(1−E4)×E12/E7)` = 1.284875×(1+0.64×0.238623) = 1.481083.
- Schedule rows 21–30 for debt-to-capital 0–0.9: `D/E = d/(1−d)`; `beta = E17×(1+(1−t)×D/E)`; `effect of leverage = beta − E17`.
- Custom: `E35 = E17×(1+(1−E4)×E33)` = 1.284875×1.224 = 1.572687.

**Reference data:** none (no lookup tables).

**Outputs:** unlevered beta (E17 = 1.284875), current-leverage beta (E18 = 1.481083), levered-beta schedule (C21:C30 = 1.284875, 1.376244, 1.490455, 1.637298, 1.833089, 2.107195, 2.518355, 3.203622, 4.574156, 8.685756; effects D21:D30 = beta − 1.284875), custom-D/E beta (E35 = 1.572687).

**Worked example:** regression beta 1.4, t = 36%, average D/E 0.14 → β_u = 1.284875. MV debt = 12,142.263; current D/E = 12,142.263/50,889.038 = 0.23862 → current β = 1.481083. At target D/E 0.35 → β = 1.572687.

**Reimplementation:** inputs (beta: float, tax_rate: decimal, avg_de: decimal, mv_equity, bv_debt, maturity_years, interest_expense, market_rate, lease_debt=0, custom_de). MV-debt step optional — if the user supplies MV debt directly, use it; maturity 0 → MV = book value (annuity factor → 0, discount → 1); rate 0 must be guarded (limit: interest×maturity + book). No branches otherwise. Edge case: d = 1.0 would make D/E infinite — schedule stops at 0.9.

---

### macrodur.xls

**Purpose:** **Macroeconomic risk profile of a firm for debt design** — estimates how firm value and operating income respond to interest rates (duration of assets), real GDP (cyclicality), inflation, and the dollar, either **top-down** (time-series regressions on the firm's own history) or **bottom-up** (sector averages by SIC code). Damodaran uses the output to match debt characteristics (maturity, fixed/floating, currency mix) to the firm's assets. Values-only .xls; formulas (inferred), regression slopes verified by OLS.

Sheets: `Read me first` (docs; notes ≤3 years of listing → skip; macro data from FRED/St. Louis Fed; if regression output is unintuitive use sector averages), `Inputs for top down`, `Duration Calculator`, `Bottom up Estimator`, `Annual Data`, `Quarterly Data`, `Sector Averages by SIC`.

#### Inputs

**`Inputs for top down`:** number of periods `E2` (11; up to 48; annual or quarterly), then per period (period 1 = most recent): Operating Income (B), Market Cap (C), Total Debt (D). Example (a large firm, 2018 back to 2008):

| Period | Operating Income | Market Cap | Total Debt |
|---|---|---|---|
| 1 | 27801 | 231814 | 54136 |
| 2 | 26558 | 209728 | 53427 |
| 3 | 25542 | 197142 | 49864 |
| 4 | 24002 | 202286 | 41320 |
| 5 | 22798 | 184946 | 42218 |
| 6 | 21952 | 201590 | 44671 |
| 7 | 20497 | 197007 | 39018 |
| 8 | 18713 | 192048 | 38729 |
| 9 | 17091 | 221861 | 31052 |
| 10 | 12673 | 232147 | 26466 |
| 11 | 11334 | 210081 | 25388 |

**`Duration Calculator` inputs (rows 12+):** per period, Change in OI (B), Change in Firm Value (C), Change in LT Bond Rate (D), Change in GDP (E), Change in Inflation (F), Change in Currency (G). The firm columns are derived from the top-down inputs; the macro columns are **pasted by the user from the Annual/Quarterly Data worksheets** matching the firm's fiscal years (sheet header warns the canned layout assumes the most recent year is 2018 and annual data). With n input periods you get n−1 change rows.

Derivations (inferred, verified): `ChgOI_i = OI_i/OI_{i+1} − 1`; `ChgFV_i = (MC_i+Debt_i)/(MC_{i+1}+Debt_{i+1}) − 1`. Example row 1: 27801/26558−1 = 0.046803; 285,950/263,155−1 = 0.086622. Macro changes: bond-rate change is an **absolute** change in the rate (e.g. 0.00273411 for 2018); GDP, dollar are % changes; inflation change is the change in the CPI inflation rate (absolute).

#### Logic

**Top-down (`Duration Calculator`)** — for each of the two dependent variables y ∈ {Change in Firm Value (col C), Change in OI (col B)}, compute four **separate univariate OLS slopes** against the four macro-change columns (verified: values match numpy polyfit exactly; these are simple regressions, not one multiple regression):
- `C4/D4` slope of y vs Change in LT bond rate → 6.081218 (FV), −1.462709 (OI).
- **Duration of the firm's assets** `C5/D5 = IF(slope > 0, 0, −slope)` (inferred from C5=0 with positive slope and D5=+1.462709) — duration is the negative interest-rate sensitivity, floored at zero.
- **Cyclicality** `C6/D6` = slope of y vs Change in GDP → −1.386655 (FV), −0.433924 (OI).
- **Sensitivity to inflation** `C7/D7` = slope of y vs Change in Inflation → 0.955412 (FV), −1.601873 (OI).
- **Sensitivity to dollar movements** `C8/D8` = slope of y vs Change in Currency → −0.279654 (FV), −0.581120 (OI).
Sheet note: for detailed output run a full regression via Excel's data-analysis tool. Sector sheet guidance: prefer **firm-value** numbers for duration and cyclicality, **operating-income** numbers for inflation and currency.

**Bottom-up (`Bottom up Estimator`)** — two options:
- Option 1 (4-digit SIC): rows list each business's SIC code, value (or revenue), weight `C = value/Σvalue`, and Duration/Cyclicality/Inflation/Currency for that SIC; the Firm row = Σ weight × measure. Example: single business SIC 5311, value 100, weight 1 → firm duration 3.010090, cyclicality −0.297745, inflation 1.906778, currency 0.693889. Comparing to the `Sector Averages by SIC` row for 5311 (−3.01009, 0.297745 firm-value cols; −1.90678, −0.693889 OI cols) shows the per-SIC values used here are the **sign-flipped** sector-sheet values: Duration = −(FV duration), Cyclicality = −(FV cyclicality), Inflation = −(OI inflation), Currency = −(OI currency) (inferred from this one example).
- Option 2 (business classification): same weighting against a built-in 2-digit-SIC broad-industry table (below). Example: "GENERAL MERCHANDISE STORES", value 100 → firm duration 4.219394, cyclicality 0.928614, inflation 0.628639, currency 0.457645. Caveat: the 2-digit table does **not** follow the option-1 sign-flip pattern (e.g. its SIC-1 row shows duration +5.08461 = −(FV duration) but inflation −0.453324 and currency −6.35810 equal the sector sheet's OI values unflipped). Treat both bottom-up tables as verbatim reference data rather than deriving one from the other.

#### Reference data

**Broad industry groups (2-digit SIC) — `Bottom up Estimator'!J9:O77`** (verbatim; Duration/Cyclicality/Inflation/Currency as stored for option 2):

| SIC 2-digit | Broad Industry Group | Duration | Cyclicality | Inflation | Currency |
|---|---|---|---|---|---|
|---|---|---|---|---|---|
| 1 | AGRICULTURAL PRODUCTION-CROPS | 5.08461 | 0.224635 | -0.453324 | -6.3581 |
| 2 | AGRICULTURAL PRODUCTION-LIVESTOCK | 2.04086 | 0.920741 | 1.67151 | 1.49201 |
| 79 | AMUSEMENT & RECREATION SERVICES | 5.01463 | 0.693472 | 0.576898 | -1.13619 |
| 56 | APPAREL & ACCESSORY STORES | 6.63049 | 0.940827 | 1.37531 | -0.712066 |
| 23 | APPAREL & OTHER FINISHED PRODUCTS-MFRS | 5.36807 | 1.00367 | 0.460302 | -0.492438 |
| 75 | AUTO REPAIR SERVICES & PARKING | 4.22415 | 0.781115 | 2.27547 | -2.08454 |
| 55 | AUTOMOTIVE DEALERS & SERVICE STATIONS | 6.3533 | 0.471316 | 0.262971 | 1.40864 |
| 15 | BUILDING CONSTRUCTION-GEN CONTRACTORS | 5.69099 | 1.03646 | 3.25962 | 0.115239 |
| 52 | BUILDING MATERIALS & HARDWARE | 5.335 | 0.60643 | -1.75653 | -0.864859 |
| 73 | BUSINESS SERVICES | 5.43172 | 0.720114 | 0.666798 | -1.61179 |
| 28 | CHEMICALS & ALLIED PRODUCTS MFRS | 4.09556 | 0.741069 | 1.71314 | -0.727012 |
| 12 | COAL MINING | 3.77459 | 0.394236 | 0.949735 | -0.568745 |
| 48 | COMMUNICATIONS | 6.58532 | 0.960027 | 0.098327 | -0.945235 |
| 17 | CONSTRUCTION-SPECIAL TRADE CONTRACTORS | 5.2291 | 0.605706 | -5.96073 | -5.87141 |
| 60 | DEPOSITORY INSTITUTIONS | 4.95862 | 1.01127 | -1.0665 | 0.661831 |
| 58 | EATING & DRINKING PLACES | 7.55175 | 0.597805 | 0.289708 | -1.77538 |
| 82 | EDUCATIONAL SERVICES | 8.40907 | 0.579938 | 2.19864 | -2.27681 |
| 49 | ELECTRIC GAS & SANITARY SERVICES | 5.10323 | 0.46222 | 1.8794 | -2.05789 |
| 36 | ELECTRONIC & OTHER ELECTRICAL EQUIP MFR | 5.44029 | 0.838211 | 2.46968 | -0.475462 |
| 87 | ENGINEERING & ACCOUNTING & MGMT SVCS | 5.27651 | 0.899431 | -1.58001 | -0.147644 |
| 34 | FABRICATED METAL PRODUCTS MFRS | 5.17727 | 0.714112 | 0.859664 | -0.607409 |
| 20 | FOOD & KINDRED PRODUCTS MFRS | 4.82946 | 0.793873 | 0.0664734 | -0.0481076 |
| 54 | FOOD STORES | 3.41122 | 0.9144 | 2.22694 | -1.474 |
| 8 | FORESTRY | 5.33116 | 1.81714 | 3.16399 | 3.29076 |
| 25 | FURNITURE & FIXTURES MFRS | 5.50504 | 0.880924 | 0.103197 | -0.10614 |
| 53 | GENERAL MERCHANDISE STORES | 4.21939 | 0.928614 | 0.628639 | 0.457645 |
| 80 | HEALTH SERVICES | 4.88447 | 0.655601 | 1.50042 | -0.0883573 |
| 16 | HEAVY CONSTRUCTION EXCEPT BUILDING | 1.81346 | 1.02199 | 4.19421 | -0.491808 |
| 67 | HOLDING & OTHER INVESTMENT OFFICES | 4.45334 | 1.12535 | 0.133113 | -0.765408 |
| 57 | HOME FURNITURE & FURNISHINGS STORES | 5.73823 | 0.764517 | 0.950209 | 0.987861 |
| 70 | HOTELS ROOMING HOUSES & CAMPS | 5.87472 | 0.720177 | 0.336808 | -0.835146 |
| 35 | INDUSTRIAL & COMMERCIAL MACHINERY MFRS | 4.53089 | 0.892861 | -0.253533 | -0.997186 |
| 64 | INSURANCE AGENTS BROKERS & SERVICE | 5.46667 | -0.154803 | -0.801299 | -3.19658 |
| 63 | INSURANCE CARRIERS | 7.28094 | 0.705137 | -1.08153 | -1.55592 |
| 31 | LEATHER & LEATHER PRODUCTS MFRS | 5.90857 | 0.879546 | -0.677509 | -2.11268 |
| 41 | LOCAL/SUBURBAN TRANSIT & HWY PASSENGER | 2.3987 | 0.836789 | -1.23281 | -3.6366 |
| 24 | LUMBER & WOOD PRODS EXCEPT FURNTR MFRS | 5.93332 | 0.737009 | 0.286141 | 0.414773 |
| 38 | MEASURING & ANALYZING INSTRUMENTS-MFRS | 4.98069 | 0.553707 | 0.961607 | -0.688271 |
| 10 | METAL MINING | 2.76193 | 0.746906 | 0.807022 | 0.760843 |
| 14 | MINING & QUARRYING-NONMETALLIC MINERALS | 2.78601 | 0.889969 | 1.62721 | 1.86976 |
| 39 | MISCELLANEOUS MANUFACTURING INDS MFRS | 4.21571 | 0.829934 | 0.153158 | -2.90438 |
| 76 | MISCELLANEOUS REPAIR SERVICES | 4.55584 | 0.0599302 | 4.91239 | 0.424165 |
| 59 | MISCELLANEOUS RETAIL | 4.01829 | 0.820816 | 1.35882 | 1.07112 |
| 78 | MOTION PICTURES | 5.35807 | 0.505593 | 4.33927 | -2.45298 |
| 42 | MOTOR FREIGHT TRANSPORTATION/WAREHOUSE | 5.12171 | 0.496088 | 1.32275 | -4.91136 |
| 99 | NONCLASSIFIED ESTABLISHMENTS | 3.4299 | 1.36966 | 1.61383 | 3.59164 |
| 61 | NONDEPOSITORY CREDIT INSTITUTIONS | 4.19486 | 0.733482 | 1.01104 | 0.314481 |
| 13 | OIL & GAS EXTRACTION | 4.20893 | 0.530962 | 2.99243 | -2.50443 |
| 26 | PAPER & ALLIED PRODUCTS MFRS | 3.37856 | 0.801473 | 1.80204 | -0.24238 |
| 72 | PERSONAL SERVICES | 5.55982 | 0.63771 | 1.0413 | -0.975877 |
| 29 | PETROLEUM REFINING & RELATED INDS MFRS | 2.45306 | 0.510077 | -0.0155643 | 0.563553 |
| 46 | PIPELINES EXCEPT NATURAL GAS | 1.57361 | 0.630184 | 1.45912 | -1.75344 |
| 33 | PRIMARY METAL INDUSTRIES MFRS | 3.53453 | 1.07952 | 2.95113 | 1.52622 |
| 27 | PRINTING PUBLISHING & ALLIED INDUSTRIES | 4.09595 | 0.661639 | 3.29096 | -1.11507 |
| 40 | RAILROAD TRANSPORTATION | 5.76127 | 0.235189 | 2.40835 | -1.95391 |
| 65 | REAL ESTATE | 3.71767 | 1.01001 | -0.526829 | -0.957422 |
| 30 | RUBBER & MISCELLANEOUS PLASTICS MFRS | 5.29091 | 0.730345 | 1.45607 | -1.0788 |
| 62 | SECURITY & COMMODITY BROKERS | 6.69303 | 0.907257 | -1.14618 | -1.16954 |
| 83 | SOCIAL SERVICES | 1.10564 | 1.13778 | -7.34239 | -2.05701 |
| 32 | STONE CLAY GLASS & CONCRETE PRODS MFRS | 5.45914 | 0.719616 | 0.541514 | -1.96328 |
| 22 | TEXTILE MILL PRODUCTS MFRS | 3.72057 | 0.711384 | 2.36071 | 0.515998 |
| 21 | TOBACCO PRODUCTS MFRS | 8.73869 | 0.352284 | -0.395604 | -3.89021 |
| 45 | TRANSPORTATION BY AIR | 2.69752 | 0.975507 | -0.979744 | 0.648018 |
| 37 | TRANSPORTATION EQUIPMENT MFRS | 4.55659 | 0.856534 | 0.682394 | -0.988688 |
| 47 | TRANSPORTATION SERVICES | 6.40887 | 0.969637 | 2.76692 | 0.591115 |
| 44 | WATER TRANSPORTATION | 6.07573 | 0.641933 | 5.57889 | -4.77512 |
| 50 | WHOLESALE TRADE-DURABLE GOODS | 3.78907 | 0.766545 | 0.628693 | -0.2982 |
| 51 | WHOLESALE TRADE-NONDURABLE GOODS | 4.38365 | 0.805087 | -0.270923 | -0.439572 |

**`Annual Data` (A1:I38)** — annual macro series 1987–2020 with the change columns the calculator consumes. Column meanings: T.Bond Rate = ten-year US treasury rate (FRED DGS10); Change in rate (absolute); Real GDP (FRED GDPC1, billions of chained dollars); % Chg in GDP; CPI = CPI inflation rate (FRED CPIAUCSL_PC1); Change in CPI (absolute change in the inflation rate); Weighted Dollar = trade-weighted dollar index (FRED TWEXBANL; series changed to DTWEXBGS in 2006); % Change in $. Verbatim:

| Date | T.Bond Rate | Change in rate | Real GDP | % Chg in GDP | CPI | Change in CPI | Weighted Dollar | % Change in $ |
|---|---|---|---|---|---|---|---|---|
| 2020 | 0.0093 | -0.0097135 | 18780.3 | -0.0228642 | 0.0129 | -0.00977613 | 111.563 | -0.0271419 |
| 2019 | 0.0192 | -0.0074983 | 19219.8 | 0.0232235 | 0.0229 | 0.00333497 | 114.675 | -0.00772705 |
| 2018 | 0.0269 | 0.00273411 | 18783.5 | 0.0307177 | 0.0195 | -0.00156694 | 115.568 | 0.0498594 |
| 2017 | 0.0241 | -0.000390434 | 18223.8 | 0.0247171 | 0.0211 | 0.000179349 | 110.08 | -0.0698337 |
| 2016 | 0.0245 | 0.00176005 | 17784.2 | 0.0187876 | 0.0209169 | 0.014238 | 118.344 | 0.0441236 |
| 2015 | 0.0227 | 0.000978761 | 17456.2 | 0.0200001 | 0.0065851 | -9.02972e-05 | 113.343 | 0.10812 |
| 2014 | 0.0217 | -0.00844332 | 17113.9 | 0.0270227 | 0.006676 | -0.00834333 | 102.284 | 0.0932754 |
| 2013 | 0.0304 | 0.0123796 | 16663.6 | 0.0261412 | 0.0151457 | -0.00240695 | 93.5574 | 0.0271619 |
| 2012 | 0.0178 | -0.0010796 | 16239.1 | 0.0146857 | 0.017595 | -0.0126387 | 91.0834 | -0.0145283 |
| 2011 | 0.0189 | -0.0136496 | 16004.1 | 0.0160935 | 0.0306207 | 0.0160126 | 92.4262 | 0.0211192 |
| 2010 | 0.033 | -0.0052961 | 15750.6 | 0.0256945 | 0.0143779 | -0.0133866 | 90.5146 | -0.0258071 |
| 2009 | 0.0385 | 0.0156479 | 15356.1 | 0.00182874 | 0.0281412 | 0.0283698 | 92.9124 | -0.0581784 |
| 2008 | 0.0225 | -0.0172049 | 15328 | -0.0275308 | -0.0002223 | -0.03968 | 98.6518 | 0.100651 |
| 2007 | 0.0404 | -0.00639862 | 15762 | 0.0197348 | 0.0410881 | 0.0154581 | 89.6304 | -0.0762724 |
| 2006 | 0.0471 | 0.00306543 | 15456.9 | 0.025907 | 0.0252398 | -0.00788254 | 97.0312 | -0.0192 |
| 2005 | 0.0439 | 0.00143899 | 15066.6 | 0.0312611 | 0.0333855 | -3.64807e-05 | 110.798 | -0.0257032 |
| 2004 | 0.0424 | -0.000287715 | 14609.9 | 0.0328179 | 0.0334232 | 0.0128105 | 113.721 | -0.0461655 |
| 2003 | 0.0427 | 0.0042377 | 14145.6 | 0.0432636 | 0.020352 | -0.00434298 | 119.225 | -0.0596061 |
| 2002 | 0.0383 | -0.0118017 | 13559 | 0.0209454 | 0.0248027 | 0.00862764 | 126.782 | 0.00585189 |
| 2001 | 0.0507 | -0.000475647 | 13280.9 | 0.00153486 | 0.0160367 | -0.0177148 | 126.045 | 0.054432 |
| 2000 | 0.0512 | -0.0124941 | 13260.5 | 0.0297348 | 0.0343602 | 0.00739819 | 119.538 | 0.0290212 |
| 1999 | 0.0645 | 0.0172002 | 12877.6 | 0.0480665 | 0.026764 | 0.0105257 | 116.167 | 0.00240491 |
| 1998 | 0.0465 | -0.0104019 | 12287 | 0.0487911 | 0.0160692 | -0.00088626 | 115.888 | 0.109728 |
| 1997 | 0.0575 | -0.00638918 | 11715.4 | 0.0448786 | 0.0169705 | -0.016268 | 104.429 | 0.0715423 |
| 1996 | 0.0643 | 0.00805077 | 11212.2 | 0.0442122 | 0.0337882 | 0.00826252 | 97.457 | 0.0518028 |
| 1995 | 0.0558 | -0.020957 | 10737.5 | 0.0219967 | 0.0253165 | -0.000640854 | 92.6571 | 0.0196239 |
| 1994 | 0.0784 | 0.0189927 | 10506.4 | 0.0411576 | 0.025974 | -0.00207721 | 90.8738 | 0.0846252 |
| 1993 | 0.0583 | -0.0081537 | 10091 | 0.0260856 | 0.0281096 | -0.00151262 | 83.7836 | 0.0893097 |
| 1992 | 0.067 | -9.37119e-05 | 9834.51 | 0.0438298 | 0.0296671 | -0.000135171 | 76.9144 | 0.0345229 |
| 1991 | 0.0671 | -0.0126758 | 9421.57 | 0.0116642 | 0.0298063 | -0.0308157 | 74.3477 | 0.0411429 |
| 1990 | 0.0808 | 0.00138979 | 9312.94 | 0.00602876 | 0.0625495 | 0.0154373 | 71.4097 | 0.0673378 |
| 1989 | 0.0793 | -0.0110867 | 9257.13 | 0.0274381 | 0.046396 | 0.00218213 | 66.9045 | 0.0982011 |
| 1988 | 0.0914 | 0.00284848 | 9009.91 | 0.037989 | 0.0441176 | 0.000763236 | 60.9219 | 0.00822509 |
| 1987 | 0.0883 | 0.0149212 | 8680.16 | 0.044793 | 0.0433213 | 0.0310802 | 60.4249 | -0.0308555 |
| 1986 | 0.0723 | -0.0162385 | 8308.02 | 0.0290815 | 0.0118721 | -0.0250913 | 62.3487 | -0.0715785 |
| 1985 | 0.09 | -0.0228597 | 8073.24 | 0.0418224 | 0.0379147 | -0.0024213 | 67.1556 | 0.117206 |
| 1984 | 0.1155 |  | 7749.15 |  | 0.0404339 |  | 60.1103 |  |

**`Quarterly Data` (146 rows)** — same idea quarterly, 1987Q1–2020Q4, date coded as year.quarter-ish decimal (e.g. 2020.12 = Dec-2020 quarter-end). Columns A–G parallel the annual sheet (T.Bond rate, change, Real GDP chained 2012$, % chg, CPI, change); the sheet also carries per-currency exchange rates (Yen-Dollar, DM-Dollar, Dollar-Euro, Dollar-BP with their change columns, H–O — omitted below for space; use FRED if needed), the Trade-Weighted Broad Dollar and its change (P–Q), Brent oil prices and change (R–S), and London gold fixing (T–U). Verbatim (columns A–G, P–T):

| Date | T.Bond Rate | Change in rate | Real GDP (Chained 2012 $) | % Chg in GDP | CPI | Change in CPI | Trade-Weighted Dollar (Broad) | Change in Weighted Dollar | Oil prices (Brent Crude) | Change in oil prices | Gold prices |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2020.12 | 0.0093 | 0.00237789 | 18780.3 | 0.00988378 | 0.0129 | -0.00118472 | 111.563 | -0.0486194 | 51.22 | 0.270968 | 1891.1 |
| 2020.09 | 0.0069 | 0.000297944 | 18596.5 | 0.0747874 | 0.0141 | 0.00690267 | 117.264 | -0.0291164 | 40.3 | -0.0321806 | 1883.4 |
| 2020.06 | 0.0066 | -0.000397377 | 17302.5 | -0.0898612 | 0.0071 | -0.0080429 | 120.781 | -0.0162732 | 41.64 | 1.80404 | 1770.7 |
| 2020.03 | 0.007 | -0.0121152 | 19010.8 | -0.0108702 | 0.0152 | -0.00758471 | 122.779 | 0.0706649 | 14.85 | -0.780876 | 1604.65 |
| 2019.12 | 0.0192 | 0.00235479 | 19219.8 | 0.00515974 | 0.0229 | 0.00547463 | 114.675 | -0.027775 | 67.77 | 0.111166 | 1523 |
| 2019.09 | 0.0168 | -0.00314713 | 19121.1 | 0.00521768 | 0.0173 | 0.000688096 | 117.951 | 0.0294492 | 60.99 | -0.0967121 | 1487.6 |
| 2019.06 | 0.02 | -0.00401961 | 19021.9 | 0.00499702 | 0.0166 | -0.00196734 | 114.577 | -0.00488365 | 67.52 | -0.00603562 | 1413.2 |
| 2019.03 | 0.0241 | 0.0232702 | 18927.3 | 0.00759387 | 0.0186 | -0.000835755 | 115.139 | -0.00371037 | 67.93 | 0.343287 | 1291.15 |
| 2018.12 | 0.000269 | -0.0302229 | 18784.6 | 0.00641089 | 0.0194513 | -0.00317995 | 115.568 | 0.0154539 | 50.57 | -0.388661 | 1281.65 |
| 2018.09 | 0.0305 | 0.00194081 | 18665 | 0.00828654 | 0.0226931 | -0.0056493 | 113.809 | 0.00483748 | 82.72 | 0.0681818 | 1183.5 |
| 2018.06 | 0.0285 | 0.00106952 | 18511.6 | 0.0102387 | 0.0284706 | 0.00474967 | 113.261 | 0.0537905 | 77.44 | 0.121994 | 1250.55 |
| 2018.03 | 0.0274 | 0.00330932 | 18324 | 0.00549859 | 0.0235857 | 0.00240224 | 107.48 | -0.0236156 | 69.02 | 0.0343174 | 1323.9 |
| 2017.12 | 0.024 | 0.000683594 | 18223.8 | 0.00567937 | 0.0211268 | -0.00111465 | 110.08 | -4.72363e-05 | 66.73 | 0.170291 | 1296.5 |
| 2017.09 | 0.0233 | 0.000195446 | 18120.8 | 0.00698483 | 0.022265 | 0.00542668 | 110.085 | -0.0169868 | 57.02 | 0.21113 | 1286.95 |
| 2017.06 | 0.0231 | -0.000879679 | 17995.2 | 0.00739668 | 0.0167175 | -0.00715489 | 111.987 | -0.0244117 | 47.08 | -0.0980843 | 1243.25 |
| 2017.03 | 0.024 | -0.000488281 | 17863 | 0.00443304 | 0.023992 | 0.00308274 | 114.789 | -0.030037 | 52.2 | -0.0502183 | 1241.7 |
| 2016.12 | 0.0245 | 0.00829673 | 17784.2 | 0.00437574 | 0.0208353 | 0.00578879 | 118.344 | 0.0540341 | 54.96 | 0.139303 | 1159.1 |
| 2016.09 | 0.016 | 0.00108268 | 17706.7 | 0.00477906 | 0.0149259 | 0.00441343 | 112.277 | 0.0010494 | 48.24 | 0.00395421 | 1327.9 |
| 2016.06 | 0.0149 | -0.00285742 | 17622.5 | 0.00565599 | 0.0104466 | 0.00181346 | 112.159 | 0.0203915 | 48.05 | 0.307483 | 1317 |
| 2016.03 | 0.0178 | -0.00481431 | 17523.4 | 0.00384671 | 0.0086142 | 0.00197291 | 109.918 | -0.0302163 | 36.75 | 0.00382409 | 1233.6 |
| 2015.12 | 0.0227 | 0.00205339 | 17456.2 | 0.000999094 | 0.0066243 | 0.00645941 | 113.343 | 0.0180704 | 36.61 | -0.225841 | 1062.25 |
| 2015.09 | 0.0206 | -0.00284147 | 17438.8 | 0.00240116 | 0.0001221 | -0.00178718 | 111.331 | 0.045175 | 47.29 | -0.215885 | 1122.5 |
| 2015.06 | 0.0235 | 0.00400586 | 17397 | 0.00824614 | 0.0019095 | 0.00200308 | 106.519 | -0.00856576 | 60.31 | 0.1233 | 1175 |
| 2015.03 | 0.0194 | -0.00225623 | 17254.7 | 0.00822715 | -9.74e-05 | -0.00662925 | 107.439 | 0.0504028 | 53.69 | -0.0285869 | 1179.25 |
| 2014.12 | 0.0217 | -0.00342566 | 17113.9 | 0.00471851 | 0.0065312 | -0.0102424 | 102.284 | 0.0487891 | 55.27 | -0.416183 | 1199.25 |
| 2014.9 | 0.0252 | -9.75419e-05 | 17033.6 | 0.0120891 | 0.0168405 | -0.00368721 | 97.5258 | 0.0463524 | 94.67 | -0.147348 | 1210 |
| 2014.6 | 0.0253 | -0.00195065 | 16830.1 | 0.0125387 | 0.0205898 | 0.00437286 | 93.2055 | -0.0110077 | 111.03 | 0.0479471 | 1313 |
| 2014.3 | 0.0273 | -0.00301762 | 16621.7 | -0.00251764 | 0.0161269 | 0.000982653 | 94.2429 | 0.00732705 | 105.95 | -0.0363802 | 1294 |
| 2013.12 | 0.0304 | 0.00388199 | 16663.6 | 0.00798249 | 0.0151284 | 0.00411879 | 93.5574 | 0.00685425 | 109.95 | 0.0194715 | 1201.5 |
| 2013.9 | 0.0264 | 0.00116913 | 16531.7 | 0.00783415 | 0.0109473 | -0.00614335 | 92.9205 | -0.0146769 | 107.85 | 0.0522978 | 1335.75 |
| 2013.6 | 0.0252 | 0.00634023 | 16403.2 | 0.00123396 | 0.0171579 | 0.00193716 | 94.3046 | 0.0216951 | 102.49 | -0.0550433 | 1203.25 |
| 2013.3 | 0.0187 | 0.000883479 | 16383 | 0.00885675 | 0.0151875 | -0.00237148 | 92.3021 | 0.01338 | 108.46 | -0.0211191 | 1602.5 |
| 2012.12 | 0.0178 | 0.00127726 | 16239.1 | 0.00113873 | 0.017595 | -0.00186931 | 91.0834 | 0.00274346 | 110.8 | -0.00502874 | 1664 |
| 2012.9 | 0.0165 | -0.000196754 | 16220.7 | 0.00134948 | 0.0194972 | 0.00290192 | 90.8342 | -0.0223378 | 111.36 | 0.182542 | 1781 |
| 2012.6 | 0.0167 | -0.00550802 | 16198.8 | 0.00430202 | 0.0165387 | -0.00913895 | 92.9096 | 0.0270873 | 94.17 | -0.236934 | 1569.5 |
| 2012.3 | 0.0223 | 0.00332583 | 16129.4 | 0.00782993 | 0.0258288 | -0.00467125 | 90.4593 | -0.0212808 | 123.41 | 0.141734 | 1660.75 |
| 2011.12 | 0.0189 | -0.000294435 | 16004.1 | 0.0115928 | 0.0306207 | -0.0072825 | 92.4262 | 0.00463479 | 108.09 | 0.0253273 | 1574.5 |
| 2011.9 | 0.0192 | -0.0123626 | 15820.7 | -0.000277787 | 0.0381262 | 0.00298904 | 91.9998 | 0.0638447 | 105.42 | -0.0563065 | 1629 |
| 2011.6 | 0.0318 | -0.00281062 | 15825.1 | 0.00714973 | 0.0350232 | 0.00853198 | 86.4786 | -0.0176224 | 111.71 | -0.0447238 | 1508 |
| 2011.3 | 0.0347 | 0.00164299 | 15712.8 | -0.00240441 | 0.0261924 | 0.0115129 | 88.0299 | -0.0274508 | 116.94 | 0.254317 | 1431 |
| 2010.12 | 0.033 | 0.00745402 | 15750.6 | 0.00501903 | 0.0143779 | 0.00314952 | 90.5146 | -0.00905284 | 93.23 | 0.154265 | 1410.25 |
| 2010.9 | 0.0253 | -0.00429143 | 15672 | 0.00737211 | 0.0111831 | -3.21406e-05 | 91.3415 | -0.0484606 | 80.77 | 0.0777956 | 1311 |
| 2010.6 | 0.0297 | -0.00844906 | 15557.3 | 0.00922028 | 0.0112156 | -0.0115169 | 95.9934 | 0.0333126 | 74.94 | -0.0675625 | 1240.5 |
| 2010.3 | 0.0384 | -9.6302e-05 | 15415.1 | 0.0038478 | 0.0228617 | -0.0051615 | 92.8987 | -0.000147451 | 80.37 | 0.0315749 | 1109.5 |
| 2009.12 | 0.0385 | 0.00519981 | 15356.1 | 0.0109838 | 0.0281412 | 0.0407732 | 92.9124 | -0.00298635 | 77.91 | 0.183683 | 1104 |
| 2009.9 | 0.0331 | -0.00212951 | 15189.2 | 0.00364111 | -0.0137794 | -0.00150849 | 93.1907 | -0.0330518 | 65.82 | -0.0336221 | 1001.25 |
| 2009.6 | 0.0353 | 0.00792041 | 15134.1 | -0.0014399 | -0.0122917 | -0.0079243 | 96.3761 | -0.0586074 | 68.11 | 0.47648 | 941 |
| 2009.3 | 0.0271 | 0.00447863 | 15155.9 | -0.011227 | -0.0044648 | -0.00426153 | 102.376 | 0.037752 | 46.13 | 0.287828 | 918.5 |
| 2008.12 | 0.0225 | -0.0156479 | 15328 | -0.0216381 | -0.0002223 | -0.0497666 | 98.6518 | 0.0679225 | 35.82 | -0.61698 | 865 |
| 2008.9 | 0.0385 | -0.0013481 | 15667 | -0.00541356 | 0.0495332 | 0.000165312 | 92.3773 | 0.0647195 | 93.52 | -0.324277 | 897 |
| 2008.6 | 0.0399 | 0.00519281 | 15752.3 | 0.00516387 | 0.0493597 | 0.00915863 | 86.7621 | 0.000853635 | 138.4 | 0.352487 | 932.75 |
| 2008.3 | 0.0345 | -0.00570324 | 15671.4 | -0.005747 | 0.039749 | -0.00128791 | 86.6881 | -0.032827 | 102.33 | 0.0923356 | 937.25 |
| 2007.12 | 0.0404 | -0.00528643 | 15762 | 0.00607842 | 0.0410881 | 0.0122466 | 89.6304 | -0.0144506 | 93.68 | 0.156972 | 836.5 |
| 2007.9 | 0.0459 | -0.0042069 | 15666.7 | 0.00543271 | 0.0283383 | 0.00137173 | 90.9446 | -0.0339359 | 80.97 | 0.121158 | 737.75 |
| 2007.6 | 0.0503 | 0.00361801 | 15582.1 | 0.00572872 | 0.0269277 | -0.00102665 | 94.1393 | -0.0226229 | 72.22 | 0.0547685 | 648.5 |
| 2007.3 | 0.0465 | -0.00057334 | 15493.3 | 0.00235493 | 0.027982 | 0.00266756 | 96.3183 | -0.00734712 | 68.47 | 0.161296 | 663.5 |
| 2006.12 | 0.0471 | 0.000668513 | 15456.9 | 0.00851865 | 0.0252398 | 0.00499308 | 97.0312 | -0.0109494 | 58.96 | -0.00220003 | 635.7 |
| 2006.9 | 0.0464 | -0.00487385 | 15326.4 | 0.00154633 | 0.0201207 | -0.0212686 | 98.1054 | -0.00145448 | 59.09 | -0.19276 | 601.75 |
| 2006.6 | 0.0515 | 0.00275796 | 15302.7 | 0.002337 | 0.0418172 | 0.00733142 | 98.2483 | -0.0229883 | 73.2 | 0.108084 | 600.4 |
| 2006.3 | 0.0486 | 0.00448217 | 15267 | 0.0133029 | 0.0341792 | 0.000767469 | 100.56 | -0.01 | 66.06 | 0.132328 | 584 |
| 2005.12 | 0.0439 | -0.000670562 | 15066.6 | 0.00631463 | 0.0333855 | -0.0135794 | 111.651 | 0.0102956 | 58.34 | -0.0544571 | 513 |
| 2005.9 | 0.0434 | 0.00268045 | 14972.1 | 0.00891334 | 0.0474183 | 0.0210117 | 110.513 | -0.0100825 | 61.7 | 0.114523 | 473.4 |
| 2005.6 | 0.0394 | -0.0015358 | 14839.8 | 0.00461561 | 0.0254103 | -0.00649311 | 111.639 | 0.0227126 | 55.36 | 0.0402104 | 436.8 |
| 2005.3 | 0.045 | 0.00115009 | 14771.6 | 0.0110696 | 0.0320684 | -0.0013127 | 109.16 | 0.00170684 | 53.22 | 0.317979 | 427.5 |
| 2004.12 | 0.0424 | 0.000959325 | 14609.9 | 0.0100167 | 0.0334232 | 0.00777174 | 108.974 | -0.0499963 | 40.38 | -0.154523 | 438 |
| 2004.9 | 0.0414 | -0.00460918 | 14465 | 0.00945328 | 0.0253917 | -0.00612937 | 114.709 | -0.00913908 | 47.76 | 0.437688 | 412.35 |
| 2004.6 | 0.0462 | 0.00726439 | 14329.5 | 0.00762076 | 0.0316767 | 0.0138376 | 115.767 | 0.0135192 | 33.22 | 0.0288015 | 393.75 |
| 2004.3 | 0.0386 | -0.00394762 | 14221.1 | 0.00533747 | 0.0174008 | -0.00290073 | 114.222 | -0.00225192 | 32.29 | 0.0656766 | 423 |
| 2003.12 | 0.0427 | 0.00297305 | 14145.6 | 0.0114817 | 0.020352 | -0.00336276 | 114.48 | -0.0349046 | 30.3 | 0.0786757 | 417.25 |
| 2003.9 | 0.0396 | 0.00404002 | 13985.1 | 0.0169821 | 0.0237832 | 0.00419561 | 118.621 | 0.0108998 | 28.09 | -0.0273546 | 384.5 |
| 2003.6 | 0.0354 | -0.00280085 | 13751.5 | 0.0086026 | 0.0194878 | -0.0105585 | 117.342 | -0.0451742 | 28.88 | 0.02959 | 345.15 |
| 2003.3 | 0.0383 | 0 | 13634.3 | 0.00554767 | 0.0302521 | 0.00528938 | 122.893 | -0.0173316 | 28.05 | -0.0687251 | 335.35 |
| 2002.12 | 0.0383 | 0.00192623 | 13559 | 0.00154823 | 0.0248027 | 0.00940932 | 125.061 | -0.00796023 | 30.12 | 0.034696 | 342.75 |
| 2002.9 | 0.0363 | -0.0118691 | 13538.1 | 0.00444571 | 0.01516 | 0.00440108 | 126.064 | 0.00420436 | 29.11 | 0.14923 | 322.4 |
| 2002.6 | 0.0486 | -0.00534045 | 13478.2 | 0.00605733 | 0.0106922 | -0.00290534 | 125.536 | -0.0262072 | 25.33 | -0.000394633 | 319.05 |
| 2002.3 | 0.0542 | 0.00332005 | 13397 | 0.00874514 | 0.0136286 | -0.00237572 | 128.915 | 0.0119632 | 25.34 | 0.309561 | 303 |
| 200112 | 0.0507 | 0.00447321 | 13280.9 | 0.00272371 | 0.0160367 | -0.00972898 | 127.391 | 0.0118733 | 19.35 | -0.115226 | 276.5 |
| 200109 | 0.046 | -0.00783939 | 13244.8 | -0.00415038 | 0.0259217 | -0.00586585 | 125.896 | -0.0104608 | 21.87 | -0.165586 | 290.85 |
| 200106 | 0.0542 | 0.00464807 | 13300 | 0.00584556 | 0.0319396 | 0.00204954 | 127.227 | 0.0133459 | 26.21 | 0.115319 | 269.9 |
| 200103 | 0.0493 | -0.00181073 | 13222.7 | -0.00285178 | 0.0298246 | -0.00440425 | 125.551 | 0.0211316 | 23.5 | 0.040744 | 259.05 |
| 200012 | 0.0512 | -0.0064688 | 13260.5 | 0.0062289 | 0.0343602 | -0.000197997 | 122.953 | 0.0144201 | 22.58 | -0.205489 | 272.65 |
| 200009 | 0.058 | -0.00217391 | 13178.4 | 0.00133555 | 0.034565 | -0.00269137 | 121.205 | 0.0210984 | 28.42 | -0.100063 | 274.1 |
| 200006 | 0.0603 | 0 | 13160.8 | 0.0183116 | 0.0373494 | -0.000262207 | 118.701 | 0.0173776 | 31.58 | 0.316931 | 289.15 |
| 200003 | 0.0603 | -0.00396114 | 12924.2 | 0.0036176 | 0.0376214 | 0.0104637 | 116.674 | 0.0107439 | 23.98 | -0.0381067 | 275.9 |
| 9912 | 0.0645 | 0.00516674 | 12877.6 | 0.0169959 | 0.026764 | 0.000452197 | 115.433 | -0.00170198 | 24.93 | 0.0848564 | 290.85 |
| 9909 | 0.059 | 0.000849858 | 12662.4 | 0.0130966 | 0.0262997 | 0.00647345 | 115.63 | -0.0139646 | 22.98 | 0.354154 | 303.75 |
| 9906 | 0.0581 | 0.00529251 | 12498.7 | 0.00769159 | 0.019656 | 0.00232627 | 117.268 | -0.00163375 | 16.97 | 0.129827 | 261.2 |
| 9903 | 0.0525 | 0.00570071 | 12403.3 | 0.00946472 | 0.017284 | 0.00119416 | 117.46 | 0.0276394 | 15.02 | 0.425047 | 279.8 |
| 9812 | 0.0465 | 0.00200669 | 12287 | 0.0161588 | 0.0160692 | 0.00177271 | 114.3 | -0.0329973 | 10.54 | -0.283481 | 287.45 |
| 9809 | 0.0444 | -0.00957488 | 12091.6 | 0.0125257 | 0.014268 | -0.0019341 | 118.201 | 0.00708362 | 14.71 | 0.242399 | 294.1 |
| 9806 | 0.0544 | -0.00218134 | 11942 | 0.00925807 | 0.0162297 | 0.00242317 | 117.369 | 0.0279448 | 11.84 | -0.146359 | 295.75 |
| 9803 | 0.0567 | -0.000757074 | 11832.5 | 0.0099948 | 0.0137672 | -0.0031598 | 114.179 | 0.0172783 | 13.87 | -0.125473 | 299.9 |
| 9712 | 0.0575 | -0.00349882 | 11715.4 | 0.00858817 | 0.0169705 | -0.00513633 | 112.239 | 0.0622274 | 15.86 | -0.205411 | 289.2 |
| 9709 | 0.0612 | -0.00367508 | 11615.6 | 0.0125085 | 0.022194 | -0.000138623 | 105.664 | 0.0349535 | 19.96 | 0.0954995 | 328.75 |
| 9706 | 0.0651 | -0.0038494 | 11472.1 | 0.01662 | 0.0223357 | -0.00520084 | 102.096 | -0.00544642 | 18.22 | -0.0167296 | 334.05 |
| 9703 | 0.0692 | 0.00458287 | 11284.6 | 0.00645564 | 0.0276527 | -0.0059704 | 102.655 | 0.037653 | 18.53 | -0.224686 | 349.5 |
| 9612 | 0.0643 | -0.0027248 | 11212.2 | 0.0103838 | 0.0337882 | 0.00362018 | 98.9296 | 0.0116256 | 23.9 | -0.010352 | 369.55 |
| 9609 | 0.0672 | -9.37031e-05 | 11097 | 0.00896991 | 0.0300457 | 0.00177711 | 97.7927 | -0.000205495 | 24.15 | 0.252593 | 379.3 |
| 9606 | 0.0673 | 0.00365408 | 10998.3 | 0.0166785 | 0.0282152 | -0.000217853 | 97.8128 | 0.0125475 | 19.28 | -0.0516478 | 381.3 |
| 9603 | 0.0634 | 0.00714689 | 10817.9 | 0.00748947 | 0.0284392 | 0.00303635 | 96.6007 | 0.0108165 | 20.33 | 0.0900804 | 396.7 |
| 9512 | 0.0558 | -0.00558818 | 10737.5 | 0.00679021 | 0.0253165 | -0.000132252 | 95.567 | 0.0183516 | 18.65 | 0.124849 | 386.7 |
| 9509 | 0.0617 | -0.000376754 | 10665.1 | 0.00850678 | 0.0254521 | -0.00485045 | 93.8448 | 0.0391442 | 16.58 | 0 | 383.75 |
| 9506 | 0.0621 | -0.00932116 | 10575.1 | 0.00298341 | 0.030426 | 0.00247839 | 90.3097 | -0.0261845 | 16.58 | -0.0778643 | 387.6 |
| 9503 | 0.072 | -0.00597015 | 10543.6 | 0.00354756 | 0.0278722 | 0.00184673 | 92.738 | 0.00756395 | 17.98 | 0.107825 | 386.55 |
| 9412 | 0.0784 | 0.00204006 | 10506.4 | 0.0114552 | 0.025974 | -0.00358801 | 92.0418 | 0.0226276 | 16.23 | -0.0298864 | 382.5 |
| 9409 | 0.0762 | 0.00260175 | 10387.4 | 0.00584515 | 0.0296552 | 0.00457163 | 90.0052 | -0.0218591 | 16.73 | -0.0412607 | 395.35 |
| 9406 | 0.0734 | 0.00531023 | 10327 | 0.0135505 | 0.024948 | -0.00153159 | 92.0166 | 0.0112703 | 17.45 | 0.316981 | 385.4 |
| 9403 | 0.0677 | 0.00880397 | 10189 | 0.00970216 | 0.0265178 | -0.00155068 | 90.9911 | 0.0396844 | 13.25 | 0.00531108 | 389.7 |
| 9312 | 0.0583 | 0.00406312 | 10091 | 0.0136011 | 0.0281096 | 0.000456761 | 87.518 | 0.036937 | 13.18 | -0.235055 | 390.65 |
| 9309 | 0.054 | -0.00379507 | 9955.64 | 0.00477315 | 0.02764 | -0.0022757 | 84.4005 | 0.0203192 | 17.23 | -0.0114745 | 352.65 |
| 9306 | 0.058 | -0.00217391 | 9908.35 | 0.0058242 | 0.0299786 | -0.000209228 | 82.7197 | 0.00379214 | 17.43 | -0.0679144 | 379 |
| 9303 | 0.0603 | -0.00631897 | 9850.97 | 0.001674 | 0.0301941 | 0.000511554 | 82.4072 | 0.0192616 | 18.7 | 0.047619 | 336.9 |
| 9212 | 0.067 | 0.00309278 | 9834.51 | 0.0104316 | 0.0296671 | -0.000252412 | 80.8499 | 0.0655937 | 17.85 | -0.115461 | 332.9 |
| 9209 | 0.0637 | -0.00723888 | 9732.98 | 0.00988272 | 0.029927 | -0.000213704 | 75.8731 | -0.00486856 | 20.18 | -0.0203883 | 349 |
| 9206 | 0.0714 | -0.00373343 | 9637.73 | 0.0108435 | 0.0301471 | -0.00170073 | 76.2443 | -0.0141265 | 20.6 | 0.079099 | 343.4 |
| 9203 | 0.0754 | 0.00771806 | 9534.35 | 0.0119705 | 0.0318991 | 0.00202811 | 77.3368 | 0.0433154 | 19.09 | 0.075493 | 341.5 |
| 9112 | 0.0671 | -0.00712211 | 9421.57 | 0.00348499 | 0.0298063 | -0.00403571 | 74.126 | -0.0132269 | 17.75 | -0.171722 | 353.4 |
| 9109 | 0.0747 | -0.00716479 | 9388.84 | 0.00505297 | 0.0339623 | -0.01257 | 75.1196 | -0.0149347 | 21.43 | 0.159632 | 350.5 |
| 9106 | 0.0824 | 0.00175536 | 9341.64 | 0.00779719 | 0.0469592 | -0.00119613 | 76.2585 | 0.0391933 | 18.48 | 0.0266667 | 366.9 |
| 9103 | 0.0805 | -0.000277649 | 9269.37 | -0.00467844 | 0.0482115 | -0.0136785 | 73.3824 | 0.0380375 | 18 | -0.365079 | 354 |
| 9012 | 0.0808 | -0.00684678 | 9312.94 | -0.00910379 | 0.0625495 | 0.000800716 | 70.6934 | 0.00263375 | 28.35 | -0.308537 | 391 |
| 9009 | 0.0882 | 0.0035839 | 9398.5 | 0.000665229 | 0.0616987 | 0.0140927 | 70.5077 | -0.0371076 | 41 | 1.60648 | 406.1 |
| 9006 | 0.0843 | -0.00202896 | 9392.25 | 0.00362908 | 0.0467365 | -0.00538502 | 73.2249 | 0.00370504 | 15.73 | -0.123677 | 352.4 |
| 9003 | 0.0865 | 0.00662678 | 9358.29 | 0.0109279 | 0.0523732 | 0.00567973 | 72.9546 | 0.0480462 | 17.95 | -0.147268 | 372.2 |
| 8912 | 0.0793 | -0.0035208 | 9257.13 | 0.00197047 | 0.046396 | 0.00195385 | 69.6101 | 0.00255644 | 21.05 | 0.15469 | 401 |
| 8909 | 0.0831 | 0.00193888 | 9238.92 | 0.00740881 | 0.0443515 | -0.00703154 | 69.4326 | 0.0205349 | 18.23 | -0.00273523 | 369 |
| 8906 | 0.081 | -0.0111008 | 9170.98 | 0.00763269 | 0.0516949 | 0.00263185 | 68.0355 | 0.0579369 | 18.28 | -0.106112 | 371.15 |
| 8903 | 0.093 | 0.00146386 | 9101.51 | 0.010166 | 0.048927 | 0.00458507 | 64.3096 | 0.0446806 | 20.45 | 0.260012 | 382.3 |
| 8812 | 0.0914 | 0.00247389 | 9009.91 | 0.013325 | 0.0441176 | 0.00217341 | 61.5591 | -0.028618 | 16.23 | 0.360436 | 410.15 |
| 8809 | 0.0887 | 0.000459263 | 8891.43 | 0.00585929 | 0.0418483 | 0.0021123 | 63.3727 | 0.0467854 | 11.93 | -0.158674 | 396.15 |
| 8806 | 0.0882 | 0.00229737 | 8839.64 | 0.0131387 | 0.0396476 | 0.00127274 | 60.5403 | 0.0210862 | 14.18 | -0.0939297 | 436.85 |
| 8803 | 0.0857 | -0.00239477 | 8725.01 | 0.00516626 | 0.0383244 | -0.00481247 | 59.2901 | 0.0110328 | 15.65 | -0.110795 | 458 |
| 8712 | 0.0883 | -0.00735091 | 8680.16 | 0.0171705 | 0.0433213 | 0.000569336 | 58.6431 | -0.0376706 | 17.6 | -0.047619 | 486.5 |
| 8709 | 0.0963 | 0.011402 | 8533.64 | 0.00867612 | 0.0427273 | 0.00503507 | 60.9387 | 0.00595099 | 18.48 |  | 459.15 |
| 8706 | 0.0838 | 0.00802731 | 8460.23 | 0.010789 | 0.0374771 | 0.00873542 | 60.5782 | 0.00166839 |  |  | 447.1 |
| 8703 | 0.0751 | 0.00260441 | 8369.93 | 0.00745171 | 0.0284143 | 0.0160852 | 60.4773 | -0.031227 |  |  | 419 |
| 8612 | 0.0723 | -0.00205166 | 8308.02 | 0.00537076 | 0.0118721 | -0.00563727 | 62.4267 | 0.0201408 |  |  | 390.9 |
| 8609 | 0.0745 | 0.000930665 | 8263.64 | 0.00957032 | 0.0175763 | -9.64055e-05 | 61.1942 | -0.0181452 |  |  | 421.2 |
| 8606 | 0.0735 | -0.000372613 | 8185.3 | 0.00450384 | 0.0176744 | -0.00379414 | 62.3251 | -0.00966105 |  |  | 345.5 |
| 8603 | 0.0739 | -0.0149921 | 8148.6 | 0.00933504 | 0.0215356 | -0.0160338 | 62.9331 | -0.0323656 |  |  | 345.5 |
| 8512 | 0.09 | -0.0120183 | 8073.24 | 0.00743292 | 0.0379147 | 0.00524224 | 65.0381 | -0.0403368 |  |  | 327 |
| 8509 | 0.1031 | 0.000543922 | 8013.67 | 0.0152712 | 0.0324737 | -0.00403933 | 67.7718 | -0.00633979 |  |  | 326.5 |
| 8506 | 0.1025 | -0.0126984 | 7893.14 | 0.00880455 | 0.0366442 | -0.00121228 | 68.2042 | -0.0149126 |  |  | 316.5 |
| 8503 | 0.1165 | 0.000895656 | 7824.25 | 0.00969087 | 0.0379009 | -0.0024405 | 69.2367 | 0.0627683 |  |  | 329.8 |
| 8412 | 0.1155 |  | 7749.15 |  | 0.0404339 |  | 65.1475 |  |  |  | 309 |

**`Sector Averages by SIC` (A11:J404)** — per-4-digit-SIC regression coefficients computed from quarterly operating income and firm value changes aggregated by SIC, quarterly Compustat data 1987–1997. Two blocks: "Using firm value" (C–F) and "Using operating income" (G–J), each with Duration, Cyclicality, Inflation, Currency (duration here is the raw slope: negative duration = value falls as rates rise). Sheet guidance: look up the firm's SIC; use firm-value columns for duration/cyclicality and operating-income columns for inflation/currency. Last row is the overall "Market". Verbatim:

| SIC | Industry | Duration | Cyclicality | Inflation | Currency | Duration | Cyclicality | Inflation | Currency |
|---|---|---|---|---|---|---|---|---|---|
| 100 | Agricultural Production-Crops | -5.08461 | 0.224635 | -3.64844 | -2.68775 | -8.28735 | -0.303525 | -0.453324 | -6.3581 |
| 200 | Agricultural Prod-Livestock & Animal Specialties | -2.04086 | 0.920741 | 0.326922 | -0.0781758 | -11.5895 | 3.19687 | 1.67151 | 1.49201 |
| 800 | Forestry | -5.33116 | 1.81714 | 0.686234 | 1.27533 | -6.57709 | 2.93941 | 3.16399 | 3.29076 |
| 1000 | Metal Mining | -0.836351 | 0.928408 | -1.52903 | 0.119125 | -3.65427 | 2.6489 | 3.36223 | 2.94328 |
| 1040 | Gold and Silver Ores | -2.22004 | 0.642118 | 4.25668 | -0.051748 | 2.69393 | 2.6081 | -2.11865 | 3.65167 |
| 1090 | Miscellaneous Metal Ores | -5.22941 | 0.670192 | -0.524447 | -1.43372 | -6.81406 | 0.0983389 | 1.17748 | -4.31243 |
| 1220 | Bituminous Coal & Lignite Mining | -3.77459 | 0.394236 | -0.352543 | -1.90846 | -3.468 | 1.30096 | 0.949735 | -0.568745 |
| 1311 | Crude Petroleum & Natural Gas | -3.40877 | 0.47441 | 1.57753 | -0.893189 | -6.61491 | 1.76707 | 3.61318 | 0.684251 |
| 1381 | Drilling Oil & Gas Wells | -3.71173 | 0.658118 | 3.46825 | -0.473382 | -5.26306 | -0.150009 | 3.82543 | -3.90761 |
| 1382 | Oil & Gas Field Exploration Services | -3.13677 | 1.18543 | 3.2461 | 0.348407 | -13.4617 | 0.478026 | 0.634149 | -5.15413 |
| 1389 | Oil & Gas Field Services, NEC | -6.57846 | -0.194109 | 0.0979707 | -3.54318 | -7.12479 | 0.669553 | 3.89696 | -1.64023 |
| 1400 | Mining & Quarrying of Nonmetallic Minerals (No Fuels) | -2.78601 | 0.889969 | -1.72413 | -0.362775 | -8.13406 | 2.84644 | 1.62721 | 1.86976 |
| 1531 | Operative Builders | -8.05908 | 1.55438 | -1.9166 | -0.0663003 | -5.76887 | 4.94749 | 1.21176 | 7.5762 |
| 1540 | General Bldg Contractors - Nonresidential Bldgs | -3.32291 | 0.518532 | -6.71031 | -2.15332 | -12.6872 | -0.697822 | 5.30749 | -7.34572 |
| 1600 | Heavy Construction Other Than Bldg Const - Contractors | -0.60262 | 1.59708 | 0.946336 | 2.15114 | -9.40587 | 3.10472 | 3.96529 | 2.58449 |
| 1623 | Water, Sewer, Pipeline, Comm & Power Line Construction | -3.0243 | 0.446913 | 0.575728 | -1.52256 | -0.623756 | -0.207647 | 4.42313 | -3.5681 |
| 1700 | Construction - Special Trade Contractors | -5.2291 | 0.605706 | -4.9257 | -2.23892 | -9.84285 | 0.0217283 | -5.96073 | -5.87141 |
| 2000 | Food and Kindred Products | -9.11412 | 1.14326 | 1.83026 | -1.26147 | -15.5547 | 3.18542 | 4.10025 | 1.0325 |
| 2011 | Meat Packing Plants | -2.29489 | 0.772542 | 0.365007 | -0.324154 | -7.93183 | 2.4537 | 1.27593 | 1.17438 |
| 2013 | Sausages & Other Prepared Meat Products | -4.13857 | 0.0604436 | -2.3983 | -3.09775 | 1.88772 | 1.01024 | 1.06038 | -0.746675 |
| 2015 | Poultry Slaughtering and Processing | -7.48697 | 0.0818767 | -3.04617 | -3.95166 | -13.2327 | 0.461119 | -4.16001 | -5.43218 |
| 2020 | Dairy Products | -5.41262 | 1.48836 | -0.225381 | 0.259525 | -6.89651 | 2.697 | 1.51571 | 2.17618 |
| 2024 | Ice Cream & Frozen Desserts | -5.97368 | 0.555385 | -2.29779 | -2.17316 | -3.73981 | 2.56894 | -0.179505 | 1.71794 |
| 2030 | Canned, Frozen & Preserved Fruit, Veg & Food Specialties | -2.39545 | 0.824105 | -1.08302 | -0.261418 | 0.271058 | 2.14881 | 1.55063 | 3.52737 |
| 2033 | Canned, Fruits, Veg, Preserves, Jams & Jellies | -1.50785 | 1.31618 | -0.748456 | 0.749816 | -2.30372 | 3.05471 | 0.611142 | 3.86336 |
| 2040 | Grain Mill Products | -3.83279 | 0.773719 | -1.37136 | -0.414659 | -0.35074 | 0.439154 | 2.64292 | -1.11868 |
| 2050 | Bakery Products | -4.27157 | 0.318589 | -0.530449 | -1.88666 | -9.35747 | 1.87806 | 2.03484 | 0.14347 |
| 2052 | Cookies & Crackers | -4.73972 | 1.21161 | -3.90696 | -0.468264 | -4.30303 | 0.900765 | -6.13328 | -1.68217 |
| 2060 | Sugar & Confectionery Products | -4.74123 | 0.27975 | -2.67426 | -2.41468 | -0.234346 | 0.613348 | 3.55966 | -1.11209 |
| 2070 | Fats & Oils | -3.2906 | 0.44756 | 3.75413 | -1.00797 | -11.3166 | 0.276618 | -4.61056 | -5.33757 |
| 2080 | Beverages | -9.47284 | 1.30383 | -5.68727 | -1.84993 | -12.1418 | 3.29161 | -4.11313 | 1.35342 |
| 2082 | Malt Beverages | -3.72543 | 0.270419 | -3.90634 | -1.83207 | 0.670974 | 1.13573 | 1.38054 | 0.277374 |
| 2086 | Bottled & Canned Soft Drinks & Carbonated Waters | -4.68908 | 2.51162 | -0.568564 | 2.61879 | -9.49055 | 3.99309 | 1.87647 | 4.11285 |
| 2090 | Miscellaneous Food Preparations & Kindred Products | -5.01339 | 0.136578 | -2.05404 | -3.16336 | -6.25824 | 0.0200883 | -1.28194 | -4.76731 |
| 2100 | Tobacco Products | -6.16034 | -0.670501 | -2.04807 | -5.22954 | -8.54182 | -0.987299 | -2.96548 | -7.33107 |
| 2111 | Cigarettes | -11.317 | 1.37507 | -2.7602 | -1.54076 | -16.2772 | 2.49678 | 2.17427 | -0.449362 |
| 2200 | Textile Mill Products | -2.27288 | 0.493618 | -2.53295 | -1.70091 | -0.917099 | 1.15129 | -0.663845 | -0.595211 |
| 2211 | Broadwoven Fabric Mills, Cotton | -8.63849 | 1.41051 | -4.61864 | -1.16368 | -11.8509 | 2.75723 | -6.70223 | 0.147111 |
| 2221 | Broadwoven Fabric Mills, Man Made Fiber & Silk | -0.0147432 | 1.5259 | -0.492054 | 1.93253 | -1.01486 | 1.69281 | 8.67824 | 2.18972 |
| 2250 | Knitting Mills | -3.13501 | 0.707636 | -4.91762 | -1.25159 | -3.30812 | 1.77795 | 5.24256 | 1.53937 |
| 2253 | Knit Outerwear Mills | -2.70391 | 0.12504 | -2.88136 | -2.04496 | -7.74405 | 0.877781 | 2.31298 | -2.37047 |
| 2273 | Carpets & Rugs | -5.55841 | 0.00559723 | -0.458629 | -3.20269 | -4.89342 | 2.25561 | 5.29653 | 2.18547 |
| 2300 | Apparel & Other Finished Prods of Fabrics & Similar Matl | -3.19178 | 1.15993 | -6.974 | -0.308112 | -3.56654 | 0.74652 | -0.369919 | -1.48402 |
| 2320 | "Men's & Boys' Furnishings, Work Clothing, & Allied Garments" | -5.99745 | 0.476127 | -0.19977 | -2.18898 | 0.889842 | 1.74926 | 2.7142 | 1.19953 |
| 2330 | "Women's, Misses', and Juniors Outerwear" | -6.51434 | 1.90772 | -3.34574 | 0.522122 | -10.1638 | 2.40821 | -0.404084 | -0.0259106 |
| 2340 | "Women's, Misses', Children's & Infant's Undergarments" | -6.01864 | 0.61897 | 1.99099 | -1.58055 | -0.058807 | 2.0826 | 0.0876771 | 1.41767 |
| 2390 | Miscellaneous Fabricated Textile Products | -5.11811 | 0.855603 | -1.74713 | -1.48184 | -8.77909 | 0.705267 | 0.27363 | -3.56946 |
| 2400 | Lumber & Wood Products (No Furniture) | -9.57816 | 1.01175 | -4.28816 | -2.06772 | -10.7008 | 1.9581 | 0.406931 | -0.208264 |
| 2421 | Sawmills & Planing Mills, General | -3.41015 | 0.873057 | -3.90789 | -0.714843 | -1.51277 | 2.52919 | -1.13356 | 2.61129 |
| 2430 | Millwood, Veneer, Plywood, & Structural Wood Members | -4.7947 | 0.797814 | -0.615887 | -0.869947 | -1.26025 | 1.37569 | 1.35251 | 0.826692 |
| 2451 | Mobile Homes | -5.95027 | 0.26541 | 0.47629 | -2.26629 | -13.5863 | 1.71655 | 0.518683 | -1.57063 |
| 2510 | Household Furniture | -8.60332 | 0.7876 | 2.11427 | -1.93087 | -11.7038 | 1.96677 | 3.06907 | -0.745731 |
| 2511 | Wood Household Furniture, (No Upholstered) | -7.21978 | 0.0533831 | -6.60754 | -4.35231 | -8.97931 | 0.602061 | 1.90912 | -3.02499 |
| 2522 | Office Furniture  | -6.88045 | 0.507389 | -4.24883 | -2.64653 | -6.55505 | 2.7455 | -1.53121 | 1.70318 |
| 2531 | Public Bldg & Related Furniture | -0.65429 | 1.61127 | -1.61935 | 2.14771 | -6.84911 | 1.07795 | -0.0915811 | -1.14789 |
| 2540 | Partitions, Shelvg, Lockers, & office & Store Fixtures | -5.12376 | 0.908425 | -3.18243 | -1.5884 | -3.36 | 1.75171 | -2.99545 | -0.00923321 |
| 2590 | Miscellaneous Furniture & Fixtures | -4.54864 | 1.41747 | -6.79744 | -0.127759 | -7.10512 | 2.71974 | 0.259237 | 2.58783 |
| 2600 | Papers & Allied Products | -3.86544 | 0.194258 | -2.93355 | -2.34432 | -8.70399 | -0.211503 | 2.16445 | -4.62313 |
| 2611 | Pulp Mills | -4.3015 | 1.98092 | -1.08324 | 1.6187 | -6.63402 | 3.01348 | -0.0413461 | 2.76865 |
| 2621 | Paper Mills | -2.67838 | 0.398731 | -1.29677 | -0.944051 | -4.66922 | 0.935446 | 0.692317 | -0.565564 |
| 2631 | Paperboard Mills | -0.200612 | 0.468521 | -3.15873 | -0.927742 | -0.488698 | 0.347082 | 2.34658 | -0.971055 |
| 2650 | Paperboard Containers & Boxes | -1.76399 | 1.09739 | 0.765066 | 0.792258 | -5.72935 | 2.32352 | 3.21847 | 2.02433 |
| 2670 | Converted Paper & Paperboard Prods (No Containers/Boxes) | -4.72291 | -0.146865 | -2.50663 | -3.37641 | -3.77319 | 0.0759056 | -0.743607 | -2.83217 |
| 2673 | Plastics, Foil & Coated Paper Bags | -6.1171 | 1.61736 | -6.29042 | -0.200714 | 4.46716 | 1.79296 | 4.97737 | 2.50226 |
| 2711 | Newspapers: Publishing or Publishing & Printing | -3.92449 | 1.10132 | -1.84819 | 0.121916 | -10.0817 | 3.75213 | 4.05956 | 4.3711 |
| 2721 | Periodicals: Publishing or Publishing & Printing | -4.60941 | 1.38595 | -1.00645 | 0.338394 | -5.6572 | 3.58956 | 2.27863 | 4.81629 |
| 2731 | Books: Publishing or Publishing & Printing | -1.06895 | 0.782089 | 6.58533 | 0.418552 | -7.50259 | 0.504889 | 9.62439 | -2.90287 |
| 2750 | Commercial Printing | -6.77567 | 0.23241 | -3.45907 | -2.80972 | -9.87702 | 0.814109 | 1.93837 | -2.17643 |
| 2761 | Manifold Business Forms | -1.99693 | 1.16038 | -0.472419 | 1.1437 | -4.53116 | 2.02649 | 3.97075 | 2.32634 |
| 2771 | Greeting Cards | -7.26352 | 0.163117 | -0.683198 | -2.80216 | -5.36782 | -1.16599 | -0.165458 | -7.42759 |
| 2780 | Blankbooks, Looseleaf Binders & Bookbinding & Related Work | -6.53152 | 0.292119 | -1.03082 | -2.79586 | -9.54692 | 0.395838 | 2.91196 | -3.29493 |
| 2790 | Service Industries For The Printing Trade | -0.597117 | 0.175728 | -4.24521 | -2.12487 | -7.03485 | -0.244547 | 1.70944 | -4.6325 |
| 2800 | Chemicals & Allied Products | -8.97368 | 1.52158 | -1.09668 | -0.793645 | -16.6504 | 2.76676 | 2.1118 | -0.258968 |
| 2810 | Industrial Inorganic Chemicals | -2.82422 | 0.866997 | 0.339923 | -0.154916 | -9.02426 | 0.370462 | 2.92159 | -3.44815 |
| 2820 | Plastic Material, Synth Resin/Rubber, Cellulos (No Glass) | -0.729678 | 0.648886 | -1.38017 | -0.0283699 | -1.53292 | 0.215037 | 3.79705 | -2.08898 |
| 2821 | Plastic Materials, Synth Resins & Nonvulcan Elastomers | -0.982233 | 0.804383 | -2.24811 | 0.135496 | -1.71231 | 2.10583 | 0.660967 | 2.54649 |
| 2834 | Pharmaceutical Preparations | -7.91943 | 1.32092 | -2.70775 | -0.776322 | -8.56945 | 3.69849 | 0.842072 | 4.36139 |
| 2835 | In Vitro & In Vivo Diagnostic Substances | -2.46097 | 1.06834 | -1.08276 | 0.332791 | -1.31742 | 1.06444 | 1.43401 | 0.122148 |
| 2836 | Biological Products, (No Diagnostic Substances) | -6.81088 | 0.116675 | -2.73997 | -3.26716 | -6.12599 | -0.24083 | -0.173537 | -4.16306 |
| 2840 | Soap, Detergents, Cleaning Preparations, Perfumes, Cosmetics | -3.18357 | 0.527805 | 0.352725 | -0.667247 | 1.03455 | 0.196472 | 1.71916 | -2.15992 |
| 2842 | Specialty Cleaning, Polishing and Sanitation Preparations | -3.97588 | 0.230126 | 2.31928 | -1.70549 | -3.99531 | 0.0893266 | 3.26638 | -2.71323 |
| 2844 | Perfumes, Cosmetics & Other Toilet Preparations | -5.05219 | 1.00822 | -4.78639 | -1.24131 | -7.59761 | 2.90996 | -1.95919 | 1.946 |
| 2851 | Paints, Varnishes, Lacquers, Enamels & Allied Prods | -3.40771 | 0.814095 | -2.045 | -0.257413 | -5.541 | 2.07959 | 1.1683 | 1.5929 |
| 2860 | Industrial Organic Chemicals | -3.05453 | 0.225426 | -4.61922 | -2.07109 | -3.82838 | 0.103465 | -2.60711 | -3.33002 |
| 2870 | Agricultural Chemicals | -1.87165 | 1.42201 | 4.19391 | 1.83606 | -5.81827 | 1.505 | 7.12969 | 0.260908 |
| 2890 | Miscellaneous Chemical Products | -5.18014 | 0.418285 | -3.72447 | -2.31597 | -8.20487 | 1.39674 | 1.27119 | -0.771461 |
| 2891 | Adhesives & Sealants | -5.00671 | 0.122292 | 2.02886 | -2.24468 | -5.93009 | 0.101075 | 4.11471 | -2.80124 |
| 2911 | Petroleum Refining | -6.30514 | 0.893667 | -2.85765 | -1.48922 | -10.1643 | 1.84528 | 2.79131 | -0.361002 |
| 2950 | Asphalt Paving & Roofing Materials | -0.587785 | 0.493083 | -1.24604 | -1.11919 | -1.1034 | 3.66484 | -5.08741 | 4.48991 |
| 2990 | Miscellaneous Products of Petroleum & Coal | -0.466249 | 0.14348 | -1.52237 | -1.60155 | -0.299298 | -0.122056 | 2.24941 | -2.43825 |
| 3011 | Tires & Inner Tubes | -5.29766 | 0.919255 | -6.17155 | -1.0998 | -5.96495 | 1.5366 | 1.57809 | 0.804658 |
| 3021 | Rubber & Plastics Footwear | -3.29274 | 0.605243 | -2.15811 | -1.36101 | 2.73354 | 0.234331 | 0.0865268 | -2.03303 |
| 3050 | Gaskets, Packg & Sealg Devices & Rubber & Plastics Hose | -7.79117 | 0.517607 | -3.79378 | -3.09276 | -7.67701 | 2.03002 | 1.81004 | 0.420233 |
| 3060 | Fabricated Rubber Products, NEC | -5.05348 | 1.57399 | 0.281829 | 0.645426 | -11.9516 | -0.900613 | 4.82749 | -7.80514 |
| 3080 | Miscellaneous Plastics Products | -3.84485 | 0.616742 | -2.20579 | -1.74398 | -1.23308 | 1.54991 | 4.77087 | 1.03365 |
| 3081 | Unsupported Plastics Film & Sheet | -3.87424 | 0.161616 | -4.31255 | -2.76388 | -4.40328 | 1.09489 | -6.0996 | -1.68763 |
| 3089 | Plastics Products, NEC | -7.88222 | 0.717967 | -0.0206682 | -1.99981 | -5.8327 | 2.30121 | 3.21909 | 1.71567 |
| 3100 | Leather & Leather Products | -9.2237 | 1.22536 | -1.49698 | -1.53934 | -8.26498 | 1.70442 | -5.18003 | -2.05846 |
| 3140 | Footwear, (No Rubber) | -2.59345 | 0.533731 | -0.581591 | -1.10744 | -3.02257 | 0.48185 | 3.82501 | -2.1669 |
| 3211 | Flat Glass | -8.69625 | 1.19594 | -2.59263 | -1.62285 | -11.5833 | 2.65624 | -2.51311 | 0.215573 |
| 3220 | Glass & Glassware, Pressed or Blown | -1.17277 | 1.0516 | -2.64471 | 0.0441381 | -2.04795 | 1.58641 | 3.26856 | 1.0186 |
| 3221 | Glass Containers | -8.63273 | -0.003306 | -1.76696 | -4.18062 | -10.27 | -0.702622 | -0.343122 | -6.78047 |
| 3231 | Glass Products, Made of Purchased Glass | -7.7925 | 0.179489 | -1.52369 | -3.51332 | -15.8731 | 0.221937 | 1.70931 | -6.09155 |
| 3241 | Cement, Hydraulic | -1.21606 | 1.34008 | 0.956549 | 1.30583 | -8.49146 | 2.43849 | 3.22503 | 0.708209 |
| 3250 | Structural Clay Products | -4.84027 | 1.13297 | -2.21081 | -0.765039 | -5.35639 | 2.63323 | -1.54275 | 1.52157 |
| 3260 | Pottery & Related Products | -7.10764 | 0.18925 | -5.89936 | -4.02819 | -5.87684 | 0.332776 | 3.53232 | -3.39373 |
| 3270 | Concrete, Gypsum & Plaster Products | -2.84481 | 1.08846 | -0.752883 | -0.0596545 | -6.07717 | 0.486007 | -0.295205 | -2.93486 |
| 3290 | Abrasive, Asbestos & Misc Nonmetallic Mineral Prods | -6.82925 | 0.302066 | -6.97847 | -3.56707 | -8.64682 | 1.31454 | -2.1674 | -1.93285 |
| 3310 | Steel Works, Blast Furnaces & Rolling & Finishing Mills | -4.15608 | 0.337563 | 2.57107 | -1.97617 | -6.53584 | 1.35558 | 7.11451 | -0.466282 |
| 3312 | Steel Works, Blast Furnaces & Rolling Mills (Coke Ovens) | -3.81646 | 1.07862 | -0.362198 | 0.213697 | -11.2114 | 1.04339 | -0.707871 | -3.32798 |
| 3317 | Steel Pipe & Tubes | -5.82091 | 0.337971 | -0.658094 | -2.71231 | -2.06207 | 2.14068 | 4.26547 | 1.79744 |
| 3320 | Iron & Steel Foundries | -4.27558 | 1.0535 | 2.65751 | -0.00526513 | -6.68427 | 1.09358 | 6.50685 | -0.628646 |
| 3330 | Primary Smelting & Refining of Nonferrous Metals | -7.13121 | 1.87898 | -2.01319 | 0.3073 | -10.3663 | 3.77293 | 2.13647 | 3.38879 |
| 3334 | Primary Production of Aluminum | 1.08419 | 0.660137 | 0.845906 | 0.574021 | 0.239693 | 1.09341 | 2.09268 | 0.855099 |
| 3341 | Secondary Smelting & Refining of Nonferrous Metals | -1.51891 | 0.666879 | -1.76454 | -0.960536 | 4.79493 | 1.96 | 5.80653 | 3.99992 |
| 3350 | Rolling Drawing & Extruding of Nonferrous Metals | -3.84608 | 1.3696 | -3.77638 | -0.134353 | -8.55223 | 3.6373 | 0.108321 | 3.61931 |
| 3357 | Drawing & Insulating of Nonferrous Wire | -4.01359 | 1.81481 | -3.59125 | 0.993206 | -9.95236 | 2.02705 | 0.221639 | -0.323242 |
| 3360 | Nonferrous Foundries (Castings) | -1.47833 | 1.87382 | 0.302893 | 2.24121 | -11.1865 | 1.08369 | 6.0969 | -2.55146 |
| 3390 | Miscellaneous Primary Metal Products | -3.90688 | 0.802813 | -5.69715 | -1.18036 | 0.457786 | 5.33384 | -1.17912 | 10.4254 |
| 3411 | Metal Cans | -5.1874 | 1.80052 | 0.391601 | 1.21552 | -3.24001 | 3.27529 | 4.81294 | 4.75679 |
| 3420 | Cutlery, Handtools & General Hardware | -9.99947 | 0.597876 | -5.33732 | -3.23973 | -9.89553 | 2.45584 | 0.326778 | 1.39199 |
| 3430 | Heating Equip, Except Elec & Warm Air; & Plumbing Fixtures | -2.63044 | 0.434973 | -0.24857 | -0.882849 | -3.67067 | 1.5423 | 0.921565 | 0.760365 |
| 3440 | Fabricated Structural Metal Products | -3.62099 | 0.750109 | 0.0753518 | -0.729396 | -4.26284 | 1.33429 | -1.49233 | -0.371607 |
| 3442 | Metal Doors, Sash, Frames, Moldings & Trim | -5.80775 | -0.0997064 | -0.459088 | -3.29068 | -4.01517 | -0.155288 | 9.10394 | -2.85024 |
| 3443 | Fabricated Plate Work (Boiler Shops) | -4.2121 | 0.547114 | -1.95037 | -1.72523 | -2.49784 | 1.21551 | -1.83149 | -0.946748 |
| 3444 | Sheet Metal Work | -6.95854 | 0.539704 | -3.49152 | -2.85102 | -4.82235 | 2.02593 | -4.37495 | -0.150967 |
| 3448 | Prefabricated Metal Buildings & Components | -3.24118 | 1.26841 | 0.978277 | 0.319445 | -11.7671 | -0.607127 | 6.76371 | -6.59693 |
| 3452 | Screw Machine Products | -4.18108 | 0.831306 | -3.25367 | -1.18799 | 0.526375 | 2.43448 | 4.83665 | 3.73236 |
| 3460 | Metal Forgings & Stampings | -6.49635 | 0.842058 | -2.03549 | -1.32249 | -17.8295 | 0.915659 | -6.02779 | -5.33789 |
| 3470 | Coating, Engraving & Allied Services | -7.98285 | 0.883757 | -4.73451 | -1.94674 | -1.95804 | 3.04201 | -1.22943 | 3.89596 |
| 3480 | Ordnance & Accessories, (No Vehicles/Guided Missiles) | 0.325757 | 1.05829 | 3.12722 | 0.773767 | -8.1225 | 0.687732 | -1.4812 | -3.73597 |
| 3490 | Miscellaneous Fabricated Metal Products | -7.3121 | -0.170945 | -2.0673 | -4.26757 | -8.48884 | 0.814126 | 0.847224 | -2.44342 |
| 3510 | Engines & Turbines | -3.61604 | 0.894538 | -0.43594 | -0.200342 | -5.56875 | 3.28314 | -2.03804 | 3.50208 |
| 3523 | Farm Machinery & Equipment | -7.75166 | 1.17706 | -1.43921 | -1.41455 | -10.5276 | 2.34115 | 0.779047 | -0.154288 |
| 3524 | Lawn & Garden Tractors & Home Lawn & Gardens Equip | -7.32421 | -0.469392 | -0.170249 | -4.78499 | -8.06857 | 0.400164 | 3.43235 | -4.12075 |
| 3530 | Construction, Mining & Materials Handling Machinery & Equip | -5.2069 | 1.25947 | -1.53188 | -0.187809 | -7.51665 | 2.41103 | 0.798698 | 1.38125 |
| 3531 | Construction Machinery & Equip | -0.413602 | 0.643819 | -0.0216427 | -0.0185461 | -4.35476 | 0.83059 | 6.8921 | -0.916022 |
| 3532 | Mining Machinery & Equip (No Oil & Gas Field Mach & Equip) | -1.70631 | 2.62987 | -1.29005 | 3.84751 | -7.77371 | 2.80574 | 0.661338 | 2.11096 |
| 3533 | Oil & Gas Field Machinery & Equipment | -4.3502 | 0.918576 | -2.33642 | -0.995011 | -5.06905 | 1.38272 | -2.15484 | -0.935159 |
| 3537 | Industrial Trucks, Tractors, Trailers & Stackers | -8.08942 | 1.51675 | -4.87611 | -0.77374 | -13.4422 | 3.00338 | -2.3921 | 1.00787 |
| 3540 | Metalworkg Machinery & Equipment | -3.22499 | 1.5003 | -5.55001 | 0.176029 | -7.30692 | 2.61746 | -8.65142 | 0.502819 |
| 3541 | Machine Tools, Metal Cutting Types | -6.19595 | 1.28242 | -3.47312 | -0.800074 | -17.2168 | 1.22263 | -2.68084 | -4.31614 |
| 3550 | Special Industry Machinery (No Metalworking Machinery) | -5.25998 | 1.62151 | -2.17137 | 0.489411 | -11.052 | 2.39158 | 2.33152 | 0.703785 |
| 3555 | Printing Trades Machinery & Equipment | -0.83393 | 0.758479 | 1.81033 | -0.22264 | -5.2376 | 1.70135 | 1.51652 | -0.29053 |
| 3559 | Special Industry Machinery, NEC | -6.25861 | 0.434792 | -4.50529 | -2.91204 | -10.4944 | -0.407221 | -2.01861 | -6.3454 |
| 3560 | General Industrial Machinery & Equipment | -5.28746 | -0.0282357 | -3.08901 | -3.3547 | -8.47979 | 1.53819 | 1.62389 | -0.559271 |
| 3561 | Pumps & Pumping Equipment | -5.43258 | 0.549979 | -5.59201 | -2.41778 | -8.41642 | -0.162483 | 3.62789 | -4.32922 |
| 3562 | Ball & Roller Bearings | -0.753221 | 0.734165 | -1.62795 | -0.191134 | -0.517509 | 2.63678 | 0.588005 | 3.65086 |
| 3564 | Industrial & Commercial Fans & Blowers & Air Purifying Equip | -6.77603 | -0.481079 | -1.24443 | -4.7511 | -10.7936 | -0.657933 | -1.94725 | -7.24095 |
| 3567 | Industrial Process Furnaces & Ovens | -2.52717 | 0.983452 | -5.0672 | -0.74367 | -7.78657 | 1.63763 | -2.62297 | -1.67452 |
| 3569 | General Industrial Machinery & Equipment, NEC | -4.5271 | 1.80319 | -3.24411 | 0.885881 | -1.00616 | 4.11572 | 0.462057 | 7.04373 |
| 3570 | Computer & office Equipment | -3.32702 | -0.003717 | -1.14807 | -2.6525 | -11.1809 | 0.287884 | 2.43029 | -4.28676 |
| 3571 | Electronic Computers | -0.910805 | 0.960946 | -0.671932 | 0.203778 | -4.33383 | 0.0785317 | 1.86884 | -3.62645 |
| 3572 | Computer Storage Devices | -5.30439 | 0.153564 | -0.917199 | -2.95467 | -10.5233 | 0.939409 | -0.177025 | -3.31522 |
| 3575 | Computer Terminals | -1.66779 | 1.15384 | -1.50971 | 0.16561 | 0.954716 | 1.60313 | 4.13759 | 0.782358 |
| 3576 | Computer Communications Equipment | -2.86909 | 0.700901 | -0.172003 | -0.939281 | -6.06012 | 1.31193 | -6.37693 | -1.88258 |
| 3577 | Computer Peripheral Equipment, NEC | -7.5452 | 0.570692 | -4.76655 | -2.92565 | -2.6559 | 0.325992 | -0.160125 | -2.75187 |
| 3578 | Calculating & Accounting Machines (No Electronic Computers) | -5.49986 | 0.570977 | -4.29256 | -2.17464 | -16.4914 | -0.47565 | -5.20259 | -8.58145 |
| 3579 | Office Machines, NEC | -7.08904 | 1.25448 | -7.13629 | -1.48061 | -9.19948 | 2.15441 | -1.80396 | -0.0203974 |
| 3580 | Refrigeration & Service Industry Machinery | -6.03699 | 1.63824 | -7.04195 | -0.21021 | -9.598 | 2.96764 | -1.21579 | 1.72932 |
| 3585 | Air-Cond & Warm Air Heatg Equip & Comm & Indl Refrig Equip | -5.78932 | 1.15041 | -0.0740955 | -0.365194 | -9.87165 | 4.03787 | -3.78086 | 3.83897 |
| 3590 | Misc Industrial & Commercial Machinery & Equipment | -4.35168 | 0.905837 | -1.7722 | -0.866049 | -5.46496 | 1.02205 | 4.46721 | -0.822605 |
| 3600 | Electronic & Other Electrical Equipment (No Computer Equip) | -3.49068 | 1.09411 | 0.828319 | 0.101016 | -5.14535 | 1.91868 | 4.88783 | 1.50085 |
| 3612 | Power, Distribution & Specialty Transformers | -5.39792 | 1.0328 | 2.28697 | -0.333999 | -12.0741 | -0.742361 | 7.37825 | -6.34717 |
| 3620 | Electrical Industrial Apparatus | -4.53064 | 0.940773 | 0.700838 | -0.638575 | -6.98314 | 1.43341 | 2.34623 | -0.580339 |
| 3621 | Motors & Generators | -1.89784 | 2.11326 | -2.98558 | 2.65023 | -3.08457 | 3.27387 | 2.09935 | 4.59829 |
| 3630 | Household Appliances | -10.0931 | 0.813629 | -7.71871 | -3.34151 | -11.996 | 1.99667 | -4.40328 | -1.3838 |
| 3634 | Electric Housewares & Fans | -6.11703 | 0.370833 | -2.52324 | -2.73199 | -9.65537 | 0.141059 | -1.01478 | -5.42344 |
| 3640 | Electric Lighting & Wiring Equipment | -3.22606 | 0.589358 | -1.24978 | -0.505178 | -7.50411 | 1.49798 | 2.05077 | 0.152952 |
| 3651 | Household Audio & Video Equipment | -5.74029 | 0.668586 | 1.55356 | -1.44734 | -4.94086 | 0.304286 | 4.22945 | -2.74458 |
| 3652 | Phonograph Records & Prerecorded Audio Tapes & Disks | -9.67315 | 0.143001 | -2.72009 | -4.27239 | -12.4078 | 1.82474 | 0.865487 | -1.49303 |
| 3661 | Telephone & Telegraph Apparatus | -5.05564 | 1.48869 | -2.47427 | 0.099814 | -10.9933 | 3.3483 | 1.9371 | 2.52409 |
| 3663 | Radio & TV Broadcasting & Communications Equipment | -3.81505 | 1.37357 | -1.18157 | 0.710529 | -10.2115 | 2.3908 | 2.37987 | 1.0156 |
| 3669 | Communications Equipment, NEC | -7.80004 | -0.521114 | -0.342237 | -5.01775 | -11.9712 | 0.069793 | 3.10151 | -4.74424 |
| 3670 | Electronic Components & Accessories | -2.74634 | 1.11736 | -0.966939 | -0.0522164 | -0.743988 | 2.42063 | 3.67282 | 3.23484 |
| 3672 | Printed Circuit Boards | -5.08915 | -0.0696638 | -4.75343 | -3.85067 | -1.96478 | 2.03417 | 1.25437 | 1.71659 |
| 3674 | Semiconductors & Related Devices | -5.01226 | 2.07498 | -1.25116 | 1.78251 | -5.53232 | 3.60086 | 3.41277 | 5.22698 |
| 3677 | Electronic Coils, Transformers & Other Inductors | -10.4395 | 0.223749 | 0.466447 | -3.85283 | -9.6144 | -1.08561 | 13.2676 | -6.68401 |
| 3678 | Electronic Connectors | -5.0618 | 0.845008 | -2.15578 | -1.29902 | -5.03318 | 1.68251 | -1.22115 | 0.216247 |
| 3679 | Electronic Components, NEC | -4.16461 | 1.22696 | -0.321001 | -0.0625483 | -9.64289 | 3.40036 | -2.63411 | 2.41103 |
| 3690 | Miscellaneous Electrical Machinery, Equipment & Supplies | -4.01447 | 0.400127 | -4.49346 | -2.43691 | -5.38883 | 0.717082 | 3.31374 | -2.23065 |
| 3711 | Motor Vehicles & Passenger Car Bodies | -3.56208 | 1.60602 | -2.21503 | 0.860558 | -8.64887 | 2.51151 | -2.93293 | 0.5912 |
| 3713 | Truck & Bus Bodies | -3.24731 | 0.337111 | -4.1673 | -2.6707 | -10.1055 | 1.13681 | 0.739345 | -2.95382 |
| 3714 | Motor Vehicle Parts & Accessories | -4.67777 | 1.80354 | -4.50432 | 0.739044 | -1.58803 | 4.10031 | -0.10476 | 6.70029 |
| 3715 | Truck Trailers | -4.45312 | 1.00717 | -2.12936 | -0.668272 | -9.96186 | 0.90869 | -2.08599 | -2.64602 |
| 3716 | Motor Homes | -2.23552 | 1.03198 | 1.99419 | 0.139651 | -9.32168 | -0.360614 | 2.35258 | -6.28872 |
| 3720 | Aircraft & Parts | -4.04517 | 0.150116 | -4.30754 | -2.50172 | -6.23663 | -0.277528 | -1.6727 | -4.18111 |
| 3721 | Aircraft | -5.70645 | 0.623974 | -3.42193 | -2.29908 | -4.3642 | 2.63792 | -2.13404 | 2.01821 |
| 3724 | Aircraft Engines & Engine Parts | -4.80238 | 0.0568314 | -4.29078 | -3.18731 | -8.42539 | -0.131337 | 1.80928 | -4.64297 |
| 3728 | Aircraft Parts & Auxiliary Equipment, NEC | -6.27403 | 0.492713 | -3.89536 | -2.73667 | -15.3527 | 0.891878 | 1.71823 | -4.10088 |
| 3730 | Ship & Boat Building & Repairing | -3.45807 | 1.34097 | -2.67327 | 0.233049 | 1.13507 | 2.01389 | -0.667325 | 1.86444 |
| 3743 | Railroad Equipment | -5.6792 | 1.11751 | 1.81711 | -0.338264 | 0.617352 | 1.05809 | 9.45963 | 0.880636 |
| 3751 | Motorcycles, Bicycles & Parts | -1.56739 | 1.37247 | -3.12985 | 0.55878 | -1.06883 | 3.74265 | 2.35719 | 6.26997 |
| 3760 | Guided Missiles & Space Vehicles & Parts | -6.94116 | 0.51905 | -4.30012 | -2.8716 | -11.5204 | 1.25816 | 1.84939 | -2.38669 |
| 3790 | Miscellaneous Transportation Equipment | -7.14257 | 0.532025 | -2.00895 | -2.5777 | -13.4117 | 0.714815 | -1.13438 | -4.96619 |
| 3812 | Search, Detection, Navigation, Guidance, Aeronautical Sys | -3.72842 | 0.0767649 | -2.26897 | -2.2882 | -2.61987 | 0.343014 | -1.40567 | -2.23141 |
| 3822 | Auto Controls For Regulating Residential & Comml Environments | -4.02797 | 0.200858 | -3.00285 | -2.22299 | -8.58632 | 0.910466 | 1.5328 | -2.25036 |
| 3823 | Industrial Instruments For Measurement, Display, and Control | -2.19324 | 2.09469 | -1.81378 | 2.35452 | -1.07259 | 3.48378 | -2.26838 | 4.93299 |
| 3824 | Totalizing Fluid Meters & Counting Devices | -3.40179 | 1.09873 | -3.59271 | -0.28358 | -2.63905 | 1.98817 | 3.73942 | 1.94506 |
| 3825 | Instruments For Meas & Testing of Electricity & Elec Signals | -4.23097 | 0.70406 | -2.78125 | -1.12679 | -4.87214 | 0.823706 | -0.169841 | -1.27012 |
| 3826 | Laboratory Analytical Instruments | -3.56193 | 1.17917 | -1.25443 | 0.0679421 | -3.90908 | 2.09676 | 4.30804 | 2.25201 |
| 3827 | Optical Instruments & Lenses | -7.72147 | -0.165103 | -6.72572 | -5.18048 | -12.5117 | -0.471242 | -3.48479 | -7.62268 |
| 3829 | Measuring & Controlling Devices, NEC | -5.6685 | 0.624118 | -5.13694 | -2.50024 | -11.0854 | 2.06311 | 0.480043 | -0.348813 |
| 3841 | Surgical & Medical Instruments & Apparatus | -5.52819 | 0.566723 | -1.59664 | -1.98694 | -7.83414 | 1.47379 | 2.47822 | -0.682348 |
| 3842 | Orthopedic, Prosthetic & Surgical Appliances & Supplies | -5.00161 | 0.990093 | 4.69109 | -0.0920552 | -7.1395 | 2.10993 | 3.59928 | 1.37916 |
| 3843 | Dental Equipment & Supplies | -9.3609 | 0.112041 | -5.41943 | -4.57839 | -6.52373 | 1.54641 | -1.61367 | -0.728784 |
| 3844 | X-Ray Apparatus & Tubes & Related Irradiation Apparatus | -8.00589 | -0.368769 | -8.1419 | -5.79724 | -11.6584 | 0.496274 | 5.13547 | -4.0885 |
| 3845 | Electromedical & Electrotherapeutic Apparatus | -6.05797 | 0.736679 | -2.23712 | -1.90226 | -9.19631 | 1.70782 | 1.21654 | -0.624421 |
| 3851 | Ophthalmic Goods | -3.91504 | 1.03472 | -4.58564 | -0.827923 | -1.91107 | 2.66233 | -2.28395 | 2.83862 |
| 3861 | Photographic Equipment & Supplies | -3.52732 | 0.146242 | -0.906043 | -2.52193 | -3.61136 | 0.801442 | 3.22639 | -1.46176 |
| 3873 | Watches, Clocks, Clockwork Operated Devices/Parts | -3.75974 | -0.171708 | 0.663783 | -2.82528 | -2.12677 | -0.206797 | 0.895799 | -3.05097 |
| 3910 | Jewelry, Silverware & Plated Ware | -2.2903 | 1.47405 | -4.01706 | 0.614421 | -1.57958 | -0.458124 | -0.49261 | -4.54359 |
| 3911 | Jewelry, Precious Metal | 2.45048 | 1.64156 | 2.40765 | 2.7729 | -11.3937 | 2.42853 | 2.5033 | -0.0997045 |
| 3931 | Musical Instruments | -4.04584 | -0.144659 | 0.268426 | -2.81129 | -4.15995 | -0.327093 | 1.40269 | -3.46282 |
| 3942 | Dolls & Stuffed Toys | -4.88439 | 0.134465 | -5.51037 | -3.00995 | -9.68015 | -0.801502 | -2.21358 | -7.91748 |
| 3944 | "Games, Toys & Children's Vehicles (No Dolls & Bicycles)" | -6.50513 | 0.689435 | -7.28058 | -2.30318 | -10.3491 | 0.359223 | 0.819879 | -4.74459 |
| 3949 | Sporting & Athletic Goods, NEC | -5.96981 | 1.15748 | -4.05698 | -1.10445 | -5.42393 | 1.88551 | 1.84529 | 0.117815 |
| 3950 | "Pens, Pencils & Other Artists' Materials" | -4.58417 | 0.391644 | -2.53888 | -2.25051 | -7.75313 | 1.35328 | 2.36811 | -0.99195 |
| 3960 | Costume Jewelry & Novelties | -4.47865 | 0.668314 | -2.46553 | -1.87247 | -5.79261 | 1.66332 | 3.31417 | -0.121402 |
| 3990 | Miscellaneous Manufacturing Industries | -7.63356 | 1.45711 | -7.34513 | -1.15605 | -13.1881 | 1.08396 | -8.16882 | -4.37569 |
| 4011 | Railroads, Line-Haul Operating | -5.76127 | 0.235189 | -3.41603 | -2.75608 | -9.98761 | 1.06817 | 2.40835 | -1.95391 |
| 4100 | Local & Suburban Transit & Interurban Hwy Passenger Trans | -2.3987 | 0.836789 | 3.45685 | 0.220901 | 0.27614 | -0.213241 | -1.23281 | -3.6366 |
| 4213 | Trucking (No Local) | -2.79486 | 0.755069 | -3.87848 | -0.871285 | 0.351273 | 1.39008 | 7.09382 | 1.48423 |
| 4220 | Public Warehousing & Storage | -7.44856 | 0.237107 | -6.65262 | -4.15826 | -12.2078 | -1.88348 | -4.44831 | -11.3069 |
| 4400 | Water Transportation | -4.52785 | 0.815613 | -0.248 | -1.15032 | -8.21401 | -0.455363 | 5.57326 | -5.47822 |
| 4412 | Deep Sea Foreign Transportation of Freight | -7.6236 | 0.468252 | -0.681963 | -2.46777 | -10.208 | 0.0127392 | 5.58453 | -4.07201 |
| 4512 | Air Transportation, Scheduled | -3.43052 | 1.42176 | -4.44123 | 0.485686 | -1.63815 | 2.62227 | -5.25238 | 1.98233 |
| 4513 | Air Courier Services | -3.59829 | 0.0416673 | -0.733831 | -2.49866 | -6.36287 | 2.36961 | 2.39077 | 2.30256 |
| 4522 | Air Transportation, Nonscheduled | -1.79749 | 1.81781 | 0.450139 | 2.01711 | -7.12346 | 3.04201 | -0.400717 | 2.42567 |
| 4581 | Airports, Flying Fields & Airport Terminal Services | -1.9638 | 0.620795 | -0.934132 | -0.832746 | -4.38406 | 0.170805 | -0.656654 | -4.11849 |
| 4610 | Pipe Lines (No Natural Gas) | -1.57361 | 0.630184 | -1.81901 | -0.653722 | -2.8045 | 0.447486 | 1.45912 | -1.75344 |
| 4700 | Transportation Services | -4.72618 | 0.693809 | -4.6992 | -1.4993 | -1.01055 | 0.193758 | 3.90116 | -0.588634 |
| 4731 | Arrangement of Transportation of Freight & Cargo | -8.09156 | 1.24547 | -0.618399 | -1.21328 | -9.08012 | 2.99832 | 1.63268 | 1.77086 |
| 4812 | Radiotelephone Communications | -9.55018 | 0.981204 | -3.537 | -2.48404 | -15.9442 | 2.01939 | -1.96416 | -2.45516 |
| 4813 | Telephone Communications (No Radiotelephone) | -7.11611 | 1.55279 | -2.92978 | -0.221889 | -9.62196 | 2.83182 | -1.27526 | 1.36721 |
| 4832 | Radio Broadcasting Stations | -4.49604 | 0.702736 | -3.05463 | -1.58175 | -13.5137 | 1.97534 | 3.02869 | -1.15371 |
| 4833 | Television Broadcasting Stations | -6.592 | 1.75705 | -2.67139 | 0.189144 | -14.319 | 2.82792 | 1.3783 | 0.209625 |
| 4841 | Cable & Other Pay Television Services | -6.8916 | 0.125668 | -2.30104 | -3.5489 | -3.90022 | 0.820637 | 1.77122 | -1.29907 |
| 4899 | Communications Services, NEC | -4.86601 | 0.640716 | -1.51012 | -1.42761 | -4.49943 | 0.47976 | -2.34883 | -2.3403 |
| 4911 | Electric Services | -8.15483 | 0.527335 | -2.79731 | -2.44029 | -4.63801 | -0.472312 | 2.48656 | -4.5488 |
| 4922 | Natural Gas Transmission | -1.87039 | 1.32623 | -2.1585 | 0.817874 | -4.29774 | 2.20132 | 0.34654 | 1.66894 |
| 4923 | Natural Gas Transmission & Distribution | -5.14312 | -0.30821 | 0.118736 | -2.98615 | -9.95016 | 1.67835 | -1.57942 | -1.92575 |
| 4924 | Natural Gas Distribution | -9.28557 | 0.997804 | -2.76935 | -2.16751 | -6.76984 | 1.42125 | 3.07078 | -1.42111 |
| 4931 | Electric & Other Services Combined | -7.45339 | 0.095967 | -3.1758 | -2.79625 | -0.735557 | -0.818932 | 0.361367 | -4.58751 |
| 4932 | Gas & Other Services Combined | -5.69194 | 0.254469 | -4.26057 | -2.27223 | -4.92889 | 1.69176 | -0.329304 | -0.512175 |
| 4941 | Water Supply | -5.69487 | -0.038313 | -3.56285 | -2.93849 | -4.92743 | 0.439774 | 2.71931 | -2.05938 |
| 4953 | Refuse Systems | -3.61735 | 0.719668 | -3.06889 | -1.44063 | -7.23747 | 1.56117 | -0.761172 | -0.877966 |
| 4955 | Hazardous Waste Management | -3.73042 | 0.128302 | 0.123147 | -1.94423 | -0.798427 | -0.954576 | 0.536213 | -4.97665 |
| 4961 | Steam & Air-Conditioning Supply | -2.60727 | 0.226007 | 1.73079 | -1.51206 | -4.29903 | 0.246259 | 3.90742 | -2.18049 |
| 4991 | Co-generation Services & Small Power Producers | -2.88635 | 1.15516 | -1.81869 | -0.243173 | 0.261408 | 0.359248 | 9.91512 | -1.21587 |
| 5000 | Wholesale-Durable Goods | -1.90226 | 1.52435 | -1.0041 | 1.79622 | -4.08935 | 0.476524 | 1.34895 | -1.02912 |
| 5013 | Wholesale-Motor Vehicle Supplies & New Parts | -2.30743 | 0.4283 | -2.30571 | -0.793124 | -5.12356 | 1.21473 | 1.26022 | 0.459528 |
| 5031 | Wholesale-Lumber, Plywood, millwork & Wood Panels | -3.7373 | 0.258059 | -4.24309 | -2.65659 | -1.81739 | 1.71676 | 2.56854 | 1.20767 |
| 5040 | Wholesale-Professional & Commercial Equipment & Supplies | -3.44436 | 1.37835 | -1.00386 | 0.327727 | -12.2694 | 1.36683 | -5.01136 | -3.31526 |
| 5045 | Wholesale-Computers & Peripheral Equipment & Software | -4.05466 | 1.44598 | -0.598649 | 0.535665 | -7.89557 | 1.72448 | 2.95814 | -0.476211 |
| 5047 | Wholesale-Medical, Dental & Hospital Equipment & Supplies | -6.22675 | -0.11051 | -5.88366 | -4.27768 | 0.384491 | 0.0522378 | 1.9171 | -2.32532 |
| 5051 | Wholesale-Metals Service Centers & Offices | -6.01449 | 1.24999 | 1.46243 | 0.0123979 | -13.5711 | 1.4895 | 0.552357 | -2.62507 |
| 5063 | Wholesale-Electrical Apparatus & Equipment, Wiring Supplies | -3.972 | 0.374987 | -5.6879 | -2.74867 | -5.86018 | 1.1443 | -6.20379 | -2.4157 |
| 5065 | Wholesale-Electronic Parts & Equipment, NEC | -4.28688 | 0.121338 | -0.489541 | -2.09326 | -5.83568 | 0.0635174 | -1.12548 | -3.25527 |
| 5070 | Wholesale-Hardware & Plumbing & Heating Equipment & Supplies | -3.64148 | 1.36854 | 0.971943 | 0.689475 | -3.57643 | 2.1976 | 6.77897 | 2.21624 |
| 5080 | Wholesale-Machinery, Equipment & Supplies | -2.90615 | 0.772939 | -1.31144 | -0.486464 | -2.01162 | 2.06998 | 4.56677 | 2.42816 |
| 5084 | Wholesale-Industrial Machinery & Equipment | -3.2194 | 1.41169 | -4.73757 | 0.398454 | 1.04549 | 1.34476 | 0.682176 | 1.86131 |
| 5090 | Wholesale-Misc Durable Goods | -2.5147 | 0.711964 | -1.89185 | -0.98297 | -1.76919 | 3.52167 | -1.23423 | 4.94972 |
| 5094 | Wholesale-Jewelry, Watches, Precious Stones & Metals | -5.39201 | -0.13462 | -0.710989 | -3.62332 | -10.5548 | 1.83392 | 3.78558 | -0.982432 |
| 5099 | Wholesale-Durable Goods, NEC | -3.21611 | 0.696825 | 0.944015 | -0.90518 | -10.493 | 2.13038 | -3.41355 | -1.17123 |
| 5110 | Wholesale-Paper & Paper Products | -5.57968 | 0.503729 | -0.865576 | -1.92508 | -8.91749 | 0.651409 | 2.99015 | -2.80683 |
| 5122 | "Wholesale-Drugs, Proprietaries & Druggists' Sundries" | -5.50482 | 1.76802 | -2.44884 | 0.615226 | -6.71798 | 2.98781 | -0.875803 | 2.79877 |
| 5140 | Wholesale-Groceries & Related Products | -7.21496 | 0.317867 | -4.44034 | -2.80968 | -5.71243 | 0.667997 | -4.55075 | -2.3544 |
| 5141 | Wholesale-Groceries, General Line (merchandise) | -3.81827 | 1.11723 | -3.26256 | -0.624508 | -5.73421 | 1.31552 | -4.84644 | -1.79774 |
| 5150 | Wholesale-Farm Product Raw Materials | -8.17006 | 0.10209 | -0.911554 | -3.60754 | -4.27278 | 2.42277 | -3.98907 | 1.05864 |
| 5160 | Wholesale-Chemicals & Allied Products | 0.717329 | 0.792001 | -3.22898 | -0.34571 | 3.18467 | 1.00578 | 0.742299 | 0.340946 |
| 5171 | Wholesale-Petroleum Bulk Stations & Terminals | -3.47229 | 0.795666 | -3.8326 | -1.15343 | -6.21727 | 1.77348 | 2.27447 | -0.48143 |
| 5172 | Wholesale-Petroleum & Petroleum Products (No Bulk Stations) | -4.25233 | 0.785786 | -0.0957296 | -0.945244 | -3.1541 | 0.422524 | 4.17708 | -2.35741 |
| 5190 | Wholesale-Miscellaneous Non-durable Goods | -2.15775 | 1.06339 | 1.57525 | 0.333797 | -6.90029 | 2.7697 | 1.63977 | 1.6433 |
| 5200 | Retail-Building Materials, Hardware, Garden Supply | -4.83225 | 0.804557 | -3.91864 | -1.74141 | 1.17347 | 0.848426 | -2.65811 | -1.71364 |
| 5211 | Retail-Lumber & Other Building Materials Dealers | -6.56033 | 0.725661 | -5.10574 | -1.93418 | -5.05553 | 2.08401 | -0.418575 | 1.44526 |
| 5271 | Retail-Mobile Home Dealers | -4.61242 | 0.289072 | -2.49417 | -2.23734 | -5.14905 | 0.419102 | -2.19289 | -2.32619 |
| 5311 | Retail-Department Stores | -3.01009 | 0.297745 | -2.65994 | -2.01738 | -9.72619 | 1.96619 | -1.90678 | -0.693889 |
| 5331 | Retail-Variety Stores | -5.04278 | 1.28287 | -1.73009 | -0.0875274 | -13.8659 | 2.7393 | 2.35451 | 0.398854 |
| 5399 | Retail-Misc General Merchandise Stores | -4.60531 | 1.20522 | -4.02508 | -0.660625 | -16.2701 | 3.70854 | 1.43818 | 1.66797 |
| 5411 | Retail-Grocery Stores | -3.76316 | 0.0955348 | -2.91981 | -2.28696 | -7.88074 | 1.42808 | -0.449492 | -0.550825 |
| 5412 | Retail-Convenience Stores | -3.05927 | 1.73326 | 2.66624 | 2.11318 | -5.17045 | 0.512962 | 4.90337 | -2.39717 |
| 5500 | Retail-Auto Dealers & Gasoline Stations | -5.4983 | 0.339729 | -1.09778 | -2.83309 | -6.41343 | 1.67972 | 1.73401 | -0.554437 |
| 5531 | Retail-Auto & Home Supply Stores | -7.20831 | 0.602903 | -3.53128 | -2.57001 | -9.28988 | 3.73306 | -1.20807 | 3.37173 |
| 5600 | Retail-Apparel & Accessory Stores | -6.27038 | 1.41255 | -4.14926 | -0.478119 | -15.3137 | 2.9333 | 2.76547 | 0.424729 |
| 5621 | "Retail-Women's Clothing Stores" | -6.58918 | 0.722843 | -4.03843 | -1.9502 | -11.9847 | 2.13027 | 2.31875 | -0.540395 |
| 5651 | Retail-Family Clothing Stores | -8.1589 | 0.997849 | -4.97893 | -2.01607 | -17.6242 | 2.12221 | -1.67915 | -1.9862 |
| 5661 | Retail-Shoe Stores | -5.5035 | 0.630066 | -1.64079 | -1.6843 | -12.4292 | 2.14312 | 2.09618 | -0.7464 |
| 5700 | Retail-Home Furniture, Furnishings & Equipment Stores | -6.72328 | 1.20089 | -3.14224 | -0.874396 | -13.0864 | 2.89566 | 0.860694 | 0.872674 |
| 5712 | Retail-Furniture Stores | -6.77781 | 0.745364 | -0.180599 | -1.52921 | -5.45104 | 1.22173 | -1.37812 | -1.359 |
| 5731 | Retail-Radio, TV & Consumer Electronics Stores | -3.78141 | 0.759343 | -0.787215 | -0.67931 | -10.9081 | 3.49618 | -1.58286 | 2.46513 |
| 5734 | Retail-Computer & Computer Software Stores | -7.0448 | 0.105111 | 0.0592871 | -3.38732 | -8.56766 | 0.679389 | 4.40452 | -2.70988 |
| 5735 | Retail-Record & Prerecorded Tape Stores | -4.36383 | 1.01188 | -1.71148 | -0.859786 | -8.62714 | 4.50522 | 2.44681 | 5.67038 |
| 5810 | Retail-Eating & Drinking Places | -10.3677 | 0.679013 | -3.71691 | -3.3885 | -12.754 | 1.24513 | -0.547308 | -3.34182 |
| 5812 | Retail-Eating Places | -4.7358 | 0.516596 | -4.21377 | -1.56614 | -4.70711 | 0.974455 | 1.12672 | -0.208928 |
| 5900 | Retail-Miscellaneous Retail | -5.81744 | 0.960478 | -2.46159 | -1.235 | 2.0341 | 2.26265 | 4.54758 | 3.20747 |
| 5912 | Retail-Drug Stores and Proprietary Stores | -2.27706 | 0.463572 | -0.276185 | -0.669279 | -10.9428 | 3.36755 | 2.5818 | 2.51042 |
| 5940 | Retail-Miscellaneous Shopping Goods Stores | -4.0525 | 0.578259 | -4.38181 | -2.14657 | -7.89475 | 2.83157 | 1.08736 | 1.79534 |
| 5944 | Retail-Jewelry Stores | -5.1957 | 0.426622 | -0.986839 | -2.14985 | -13.2823 | 2.78012 | 2.51686 | 0.396903 |
| 5945 | Retail-Hobby, Toy & Game Shops | -5.15733 | -0.0209473 | -2.81638 | -3.10414 | -14.7767 | 2.62745 | 2.05908 | -0.224355 |
| 5960 | Retail-Nonstore Retailers | -1.61075 | 1.06974 | -1.04986 | 0.432849 | -4.90663 | 1.59126 | 0.442721 | 0.0854405 |
| 5961 | Retail-Catalog & Mail-Order Houses | -5.77475 | 1.53406 | -5.79397 | -0.0505317 | -12.1277 | 3.13391 | -0.420561 | 1.38732 |
| 5990 | Retail-Retail Stores, NEC | -2.26077 | 1.55474 | -2.79521 | 0.770343 | -6.83928 | 1.81037 | -1.94429 | -0.58957 |
| 6021 | National Commercial Banks | -4.41086 | 0.694799 | -6.69843 | -1.5548 | -1.12476 | 1.91848 | -2.6072 | 1.35029 |
| 6022 | State Commercial Banks | -5.52454 | 0.274232 | -5.43976 | -2.52581 | -5.45597 | 1.4878 | 2.34172 | -0.313938 |
| 6029 | Commercial Banks, NEC | -9.9433 | 1.9176 | -0.478609 | -0.13541 | -16.2386 | 3.61653 | 1.7546 | 1.46157 |
| 6035 | Savings Institution, Federally Chartered | -3.19949 | 1.30312 | -4.32558 | 0.15969 | -2.36333 | 3.5742 | -4.67294 | 4.43531 |
| 6036 | Savings Institutions, Not Federally Chartered | -1.96062 | 2.06625 | -5.67771 | 1.95769 | -5.44887 | 2.25498 | -4.53078 | 0.937704 |
| 6099 | Functions Related To Depository Banking, NEC | -4.71292 | -0.188355 | 0.535113 | -3.11869 | -6.80818 | -0.144443 | 1.31561 | -3.89995 |
| 6111 | Federal & Federally Sponsored Credit Agencies | -5.9264 | 0.434547 | -8.80732 | -2.97443 | -1.48281 | 0.123909 | -1.43378 | -1.01276 |
| 6141 | Personal Credit Institutions | -2.76742 | 1.65655 | -4.32422 | 0.976429 | 1.39132 | 3.14073 | 3.68975 | 5.90773 |
| 6153 | Short-Term Business Credit Institutions | -5.24504 | 0.545458 | -4.34864 | -2.45895 | -6.85347 | 0.470206 | -3.62981 | -3.67097 |
| 6159 | Miscellaneous Business Credit Institution | -4.61053 | 0.621752 | -3.42751 | -1.92356 | -5.02878 | 1.3275 | -2.6863 | -0.580202 |
| 6162 | Mortgage Bankers & Loan Correspondents | -3.1391 | 1.31027 | -0.395403 | 0.346235 | -3.26071 | 2.65949 | 4.49627 | 3.389 |
| 6172 | Finance Lessors | -4.47804 | 0.859669 | -3.07117 | -1.12154 | -7.94373 | 0.159582 | 1.82921 | -3.4509 |
| 6199 | Finance Services | -3.19749 | -0.293865 | 2.65371 | -2.9932 | 2.46256 | 1.61986 | 4.81197 | 1.61948 |
| 6200 | Security & Commodity Brokers, Dealers, Exchanges & Services | -4.60117 | 1.10203 | -0.357194 | -0.563691 | 1.29071 | 2.73805 | -3.00796 | 3.06086 |
| 6211 | Security Brokers, Dealers & Flotation Companies | -10.1648 | 0.728532 | -7.8067 | -3.10643 | -13.4469 | 0.488898 | 0.453082 | -4.32997 |
| 6282 | Investment Advice | -5.31312 | 0.891211 | -2.03047 | -1.08561 | -9.2065 | 0.971801 | -0.88367 | -2.23952 |
| 6311 | Life Insurance | -8.89455 | 1.28665 | -0.230932 | -1.14718 | -12.9829 | 2.36585 | -3.9305 | -1.25837 |
| 6321 | Accident & Health Insurance | -9.30652 | -0.047156 | -5.18297 | -5.13571 | -9.19182 | -2.11951 | -2.70801 | -10.6395 |
| 6324 | Hospital & Medical Service Plans | -7.821 | -0.48182 | -4.42786 | -5.34445 | -5.70526 | -0.46868 | 0.533604 | -5.39808 |
| 6331 | Fire, Marine & Casualty Insurance | -7.71794 | 0.669875 | -1.86494 | -2.05108 | -12.0366 | 2.24488 | 3.96052 | 0.169547 |
| 6351 | Surety Insurance | -3.28017 | 0.729991 | -3.30112 | -1.38154 | -3.49885 | 1.47408 | 1.66509 | 0.237435 |
| 6361 | Title Insurance | -8.37919 | 0.798931 | -4.32713 | -2.34337 | -7.32039 | 4.08608 | -0.913163 | 4.53849 |
| 6399 | Insurance Carriers, NEC | -5.56724 | 1.97949 | -2.83751 | 0.949332 | 0.278088 | 2.36256 | -6.17823 | 1.45904 |
| 6411 | Insurance Agents, Brokers & Service | -5.46667 | -0.154803 | -3.00308 | -3.45223 | -0.717764 | -0.144207 | -0.801299 | -3.19658 |
| 6500 | Real Estate | -4.61242 | 0.289072 | -2.49417 | -2.23734 | -5.14905 | 0.419102 | -2.19289 | -2.32619 |
| 6510 | Real Estate Operators (No Developers) & Lessors | -0.259904 | 2.24708 | -2.1072 | 3.13561 | -1.88757 | 2.44699 | -0.386135 | 2.12835 |
| 6512 | Operators of Nonresidential Buildings | -3.33989 | 0.775469 | -1.97214 | -0.610166 | -6.10018 | 0.221482 | 0.141736 | -2.91156 |
| 6513 | Operators of Apartment Buildings | -4.30661 | 1.18834 | -6.06228 | -0.972393 | -4.57089 | 0.933116 | 0.0186161 | -2.21817 |
| 6519 | Lessors of Real Property, NEC | -5.03919 | 0.958185 | 0.318349 | -0.731068 | -3.63178 | 3.29268 | -1.95059 | 3.40294 |
| 6531 | Real Estate Agents & Managers (For Others) | -4.25439 | 1.25882 | -3.68051 | -0.507874 | -7.65618 | 2.85822 | 5.38693 | 2.17927 |
| 6532 | Real Estate Dealers (For Their Own Account) | -3.76825 | 0.829822 | 2.53424 | -0.516817 | -2.92195 | -1.42668 | -1.06877 | -7.37572 |
| 6552 | Land Subdividers & Developers (No Cemeteries) | -4.16072 | 0.533297 | -3.26226 | -1.67582 | -8.15785 | 2.13813 | -4.16352 | -0.538286 |
| 6792 | Oil Royalty Traders | -4.81676 | 0.0190635 | 1.79167 | -2.13825 | -5.23068 | 0.607489 | -1.18966 | -2.41009 |
| 6794 | Patent Owners & Lessors | -1.78476 | 2.58759 | -2.93829 | 3.38723 | -3.29644 | 2.40631 | 1.07386 | 1.92054 |
| 6795 | Mineral Royalty Traders | -5.64506 | 0.665022 | -2.11736 | -1.96195 | -10.4413 | 0.792864 | 3.29279 | -3.60917 |
| 6798 | Real Estate Investment Trusts | -3.45534 | 0.889678 | -3.66119 | -0.41683 | -1.99527 | 1.30256 | -0.0762151 | 0.969899 |
| 6799 | Investors, NEC | -6.56477 | 1.46542 | -2.06717 | -0.375404 | -5.53704 | 1.78368 | -2.43521 | -0.698214 |
| 7011 | Hotels & Motels | -5.87472 | 0.720177 | -3.24129 | -1.62337 | -11.1464 | 1.59951 | 0.336808 | -0.835146 |
| 7200 | Services-Personal Services | -5.55982 | 0.63771 | -1.84034 | -1.95734 | -15.521 | 2.40636 | 1.0413 | -0.975877 |
| 7310 | Services-Advertising | -6.97169 | 0.882534 | -3.05238 | -1.83654 | -16.2213 | 0.872632 | -0.180754 | -4.64586 |
| 7311 | Services-Advertising Agencies | -10.352 | 0.498994 | -1.41631 | -3.27804 | -16.1988 | 3.52281 | 2.79529 | 1.54791 |
| 7320 | Services-Consumer Credit Reporting, Collection Agencies | -4.51117 | 0.90614 | -1.54722 | -1.06086 | -9.75547 | 1.79237 | 1.43406 | -0.730933 |
| 7331 | Services-Direct Mail Advertising Services | -1.70363 | 2.07454 | -1.14065 | 2.69284 | -7.66645 | 0.799875 | -0.105197 | -3.15798 |
| 7340 | Services-To Dwellings & Other Buildings | -4.11943 | 0.390564 | -1.60247 | -1.39756 | -7.16694 | 3.13437 | 0.429746 | 2.60653 |
| 7350 | Services-Miscellaneous Equipment Rental & Leasing | -8.45646 | 1.08565 | -3.98604 | -1.99251 | -15.6079 | 1.57608 | -3.55976 | -3.30922 |
| 7359 | Services-Equipment Rental & Leasing, NEC | -8.49683 | 1.37521 | -2.28728 | -0.820228 | -8.51395 | 2.05294 | -1.41833 | 0.304221 |
| 7361 | Services-Employment Agencies | -10.1227 | -0.798874 | -1.24586 | -6.59159 | -3.7432 | 0.9358 | -4.37789 | -2.68982 |
| 7363 | Services-Help Supply Services | -8.54396 | 0.217454 | -5.09478 | -4.13691 | -21.2781 | -0.648343 | -4.74931 | -9.78831 |
| 7370 | Services-Computer Programming, Data Processing, Etc. | -3.50201 | 0.547711 | -2.29604 | -1.57043 | -13.4117 | 2.27619 | 2.62778 | -0.143423 |
| 7371 | Services-Computer Programming Services | -0.860446 | 1.96725 | 0.725142 | 2.7576 | -4.50497 | 0.213706 | 2.91281 | -2.88461 |
| 7372 | Services-Prepackaged Software | -2.91029 | 0.366744 | -0.304411 | -1.24361 | -4.16368 | 0.887405 | 2.58059 | -1.08847 |
| 7373 | Services-Computer Integrated Systems Design | -3.33963 | 1.42401 | -2.77526 | 0.411281 | -8.78498 | 1.97491 | -0.569314 | -0.279356 |
| 7374 | Services-Computer Processing & Data Preparation | -4.45631 | -0.0918062 | 0.0252157 | -2.76098 | -8.60195 | 0.312667 | 0.907112 | -3.22738 |
| 7377 | Services-Computer Rental & Leasing | -4.98715 | 0.662545 | 3.16177 | -1.17906 | -7.24535 | 1.09523 | 4.06333 | -0.915875 |
| 7380 | Services-Miscellaneous Business Services | -2.40449 | 0.490117 | -2.93145 | -1.33127 | -3.03642 | 1.16354 | -1.00344 | -0.304125 |
| 7381 | Services-Detective, Guard & Armored Car Services | -8.8155 | -0.219212 | -1.83787 | -4.74268 | -9.37434 | 0.756126 | 1.2291 | -3.25893 |
| 7385 | Services-Telephone Interconnect Systems | -1.04729 | 0.881191 | 0.561211 | -0.206664 | -7.09936 | 1.56834 | 7.5612 | -0.138258 |
| 7389 | Services-Business Services, NEC | -7.60164 | 1.02141 | 0.130731 | -1.31268 | -13.6978 | 3.3284 | 2.09211 | 1.47986 |
| 7500 | Services-Automotive Repair, Services & Parking | -1.88246 | 0.777227 | 0.441919 | -0.213471 | -1.28934 | 0.496669 | 0.913436 | -1.06745 |
| 7510 | Services-Auto Rental & Leasing (No Drivers) | -6.56584 | 0.785004 | -0.828703 | -1.65455 | -10.2767 | 0.597288 | 3.63751 | -3.10163 |
| 7600 | Services-Miscellaneous Repair Services | -4.55584 | 0.0599302 | -0.408057 | -3.02025 | -2.52692 | 1.58189 | 4.91239 | 0.424165 |
| 7812 | Services-Motion Picture & Video Tape Production | -3.70283 | 0.560368 | 1.40917 | -1.23053 | -4.13091 | -0.32532 | 2.33122 | -4.08312 |
| 7819 | Services-Allied To Motion Picture Production | -5.1106 | 0.460451 | 1.31235 | -1.8707 | -0.363909 | -0.0273964 | 4.83939 | -2.78687 |
| 7822 | Services-Motion Picture & Video Tape Distribution | -3.337 | 1.38679 | 1.26093 | 0.935338 | -7.65865 | 1.1946 | 2.29607 | -1.864 |
| 7830 | Services-Motion Picture Theaters | -7.24148 | 0.567443 | 0.810746 | -2.09338 | -12.0648 | 1.25252 | 7.64192 | -1.92617 |
| 7841 | Services-Video Tape Rental | -7.39844 | -0.447086 | -1.13959 | -4.95604 | -7.14723 | 1.09828 | 4.58772 | -1.60473 |
| 7900 | Services-Amusement & Recreation Services | -3.83165 | 0.291197 | -0.246177 | -2.11955 | -9.99099 | 1.57288 | -0.532806 | -2.26906 |
| 7948 | Services-Racing, Including Track Operation | -6.47439 | 0.223222 | -1.45357 | -3.21072 | -15.6166 | 1.87218 | 0.720303 | -2.53927 |
| 7990 | Services-Miscellaneous Amusement & Recreation | -4.96883 | 1.35677 | -2.75281 | 0.236648 | 1.46203 | 0.823273 | -0.591822 | -0.810251 |
| 7997 | Services-Membership Sports & Recreation Clubs | -4.78364 | 0.9027 | -0.373062 | -0.866082 | -2.79436 | 1.54054 | 2.71192 | 1.07382 |
| 8000 | Services-Health Services | -5.60738 | 1.09131 | -7.8707 | -1.67077 | 6.8086 | 3.72693 | 0.0104011 | 7.22564 |
| 8011 | Services-Offices & Clinics of Doctors of Medicine | -4.44075 | 0.853849 | -0.997702 | -1.00114 | -3.3132 | 1.08798 | 5.04692 | -0.320901 |
| 8051 | Services-Skilled Nursing Care Facilities | -2.7652 | 0.0343054 | -3.97622 | -2.55595 | -4.04449 | -0.332916 | -2.37276 | -4.3685 |
| 8060 | Services-Hospitals | -6.75024 | 0.291998 | -1.4447 | -3.13123 | -4.36848 | -0.468579 | 1.69992 | -4.83596 |
| 8062 | Services-General Medical & Surgical Hospitals, NEC | -6.10736 | -0.592537 | 1.35231 | -4.40029 | -5.05913 | 0.0255067 | 5.31361 | -2.87225 |
| 8071 | Services-Medical Laboratories | -5.29164 | 0.838162 | -1.12617 | -1.16449 | -7.50727 | -0.067891 | 1.35522 | -4.80488 |
| 8082 | Services-Home Health Care Services | -5.76351 | 1.70022 | -2.31688 | 0.345467 | -4.60157 | 2.37946 | -8.78041 | 0.307977 |
| 8090 | Services-Misc Health & Allied Services, NEC | -2.58636 | 1.35541 | 2.41429 | 0.832011 | -2.2973 | 5.4683 | 6.87597 | 10.5613 |
| 8093 | Services-Specialty Outpatient Facilities, NEC | -4.64782 | 0.327686 | -4.4444 | -2.77492 | -1.04531 | 0.106774 | 4.35494 | -1.68767 |
| 8200 | Services-Educational Services | -8.40907 | 0.579938 | -4.51956 | -3.06613 | -7.92207 | 1.08751 | 2.19864 | -2.27681 |
| 8300 | Services-Social Services | -1.10564 | 1.13778 | -3.74907 | -0.182406 | 1.56323 | 0.925458 | -7.34239 | -2.05701 |
| 8700 | Services-Engineering, Accounting, Research, Management | -5.26084 | 1.56972 | 0.308216 | 0.638952 | -11.7544 | 0.952555 | -1.79441 | -3.68422 |
| 8711 | Services-Engineering Services | -3.99844 | 1.38794 | 0.227248 | 0.797855 | -6.29642 | 2.01306 | 3.15594 | 0.812293 |
| 8731 | Services-Commercial Physical & Biological Research | -7.58118 | 0.839399 | -0.741554 | -1.88697 | -10.3605 | 2.50666 | 0.290859 | 0.545216 |
| 8734 | Services-Testing Laboratories | -4.57524 | 0.36803 | -4.20515 | -2.41778 | -6.3535 | 0.415568 | -2.16129 | -2.80131 |
| 8741 | Services-Management Services | -4.40801 | 1.57886 | -3.27613 | 0.554655 | -6.30553 | 3.069 | 0.0887388 | 3.3274 |
| 8742 | Services-Management Consulting Services | -5.80862 | 0.0159948 | -5.51603 | -4.09516 | -7.05425 | 2.24644 | -8.27038 | -0.278897 |
| 8744 | Services-Facilities Support Management Services | -5.30327 | 0.536069 | -2.72098 | -2.33662 | -2.88714 | 2.13547 | -2.36952 | 1.04601 |
| 9995 | Non-Operating Establishments | -3.4299 | 1.36966 | -0.751517 | 0.224617 | -8.85896 | 3.64423 | 1.61383 | 3.59164 |
| Market |  | -6.21501 | 0.936178 | -1.08243 | -2.03 | -9.3813 | 1.96447 | 1.26716 | -2.03 |

#### Outputs

`Duration Calculator'!C4:D8`: regression slope vs interest rates, asset duration, cyclicality, inflation sensitivity, dollar sensitivity — each computed on firm value (col C) and operating income (col D). `Bottom up Estimator` Firm rows (B17.. and B31..): value-weighted duration/cyclicality/inflation/currency from SIC or business-classification tables.

#### Worked example

Top-down, 11 annual periods (2018 most recent): 10 change observations. Change in OI (period 1) = 0.046803, change in firm value = 0.086622; macro changes for 2018: rate +0.0027341, GDP +0.030718, inflation −0.0015669, dollar +0.049859. OLS slopes: firm value vs rates 6.0812 (positive → duration 0), vs GDP −1.3867, vs inflation 0.9554, vs dollar −0.2797; operating income vs rates −1.4627 (→ duration 1.4627), vs GDP −0.4339, vs inflation −1.6019, vs dollar −0.5811. Bottom-up: a pure department-store firm (SIC 5311) → duration 3.0101, cyclicality −0.2977, inflation 1.9068, currency 0.6939; via the 2-digit "General Merchandise Stores" group → 4.2194 / 0.9286 / 0.6286 / 0.4576.

#### Reimplementation notes

- Inputs: list of (operating_income, market_cap, total_debt) most-recent-first (4 ≤ n ≤ 48), plus matched macro change series (or raw macro levels and derive the changes exactly as the data sheets do: absolute change for the bond rate and inflation rate, percent change for GDP and the dollar); for bottom-up, list of (sic_code_or_industry, value) pairs.
- Computation: percent changes for OI and firm value (MC+debt); four univariate OLS slopes per dependent variable; duration = max(0, −slope_rates); bottom-up = value-weighted average of table rows.
- Branches/edge cases:
  - n−1 change observations must be ≥ 2 for a slope. The README says skip firms listed ≤ 3 years.
  - OI ≤ 0 in any period makes its percent change meaningless — guard.
  - Blank/padded rows must be filtered (the sheet pads with spaces).
  - If a 4-digit SIC is missing from the table, fall back to the 2-digit broad group.
  - Keep the sign conventions straight. The sector sheet stores raw slopes. The bottom-up option-1 values are the sign-flipped firm-value duration/cyclicality and operating-income inflation/currency.

---

## Cross-model notes for the Python port

- All four models share Damodaran's core toolkit: bottom-up/relevered betas (β_L = β_u(1+(1−t)D/E)), synthetic ratings from interest coverage via threshold tables, kd = rf + default spread + country default spread, MV-of-debt-from-book bond pricing, and operating-lease capitalization. Implement these once and share.
- capstru (cost-of-capital approach) and apv (APV approach) are the two classic answers to "what is the optimal debt ratio"; capstru's ratings tables carry a drop-in-EBITDA column (indirect bankruptcy costs), apv's carry a bankruptcy-probability column (direct expected bankruptcy costs). The numeric spreads differ between the two files (different vintages) — keep each model's own table.
- Both optimal-structure models are iterative by design; replicate Excel's iterative calculation with per-debt-level fixed-point loops and a convergence/2-cycle guard.

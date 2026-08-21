# Valuation Inputs Spreadsheets — batch 1 (wacccalc, implprem, ImpliedROCROE)

Source: Aswath Damodaran, 2020 spreadsheet collection, folder `Valuation Inputs Spreadsheet`.
All three files are legacy `.xls`; dumps expose computed VALUES only, so every formula below was reconstructed from labels, layout, and numeric verification. Reconstructed logic is flagged "(inferred)"; every inferred formula was verified to reproduce the stored values to the shown precision unless noted otherwise. Long-format numbers in reference tables are rounded to 6 significant digits (source cells store full double precision; percentages are stored as decimal fractions, e.g. 0.0575 = 5.75%).

---

### wacccalc.xls

**Purpose:** Damodaran's full cost-of-capital calculator. It takes a company's market data, debt, preferred stock, operating leases, business mix, and geographic revenue mix. From those it estimates five things:
1. the debt value of operating leases (capitalization);
2. a synthetic bond rating and cost of debt from interest coverage;
3. bottom-up or direct betas;
4. an equity risk premium (ERP) by one of four approaches;
5. the market-value-weighted WACC. He uses it at the start of any DCF to build the discount rate. Sheets: `Cost of Capital worksheet` (main), `Operating lease converter`, `Synthetic rating`, `Industry Averages(US)`, `Global industry averages`, `Country risk and taxes`, `Country equity risk premiums`, `Answer keys` (dropdown lists).

#### Sheet: Cost of Capital worksheet

**Inputs** (main input block, column B):

| Label | Cell | Example value |
|---|---|---|
| Company | B3 | Facebook |
| Country of incorporation | B4 | United States |
| Industry (US) | B5 | Advertising |
| Industry (Global) | B6 | Advertising |
| Do you have operating leases? (Yes/No) | B7 | Yes |
| Current year's lease expense | B9 | 180 |
| Lease commitment year 1 | B10 | 156 |
| Lease commitment year 2 | B11 | 150 |
| Lease commitment year 3 | B12 | 145 |
| Lease commitment year 4 | B13 | 143 |
| Lease commitment year 5 | B14 | 140 |
| Lease commitments beyond year 5 (lump sum) | B15 | 600 |
| Number of shares outstanding | B17 | 2407 |
| Current market price per share | B18 | 37.53 |
| Approach for estimating beta | B20 | Single Business(Global) |
| If direct input: levered (regression) beta | B21 | 1.2 |
| Riskfree rate | B23 | 0.025 |
| Approach for ERP | B24 | Operating regions |
| Direct input ERP (used if "Will input") | B25 | 0.0575 |
| Book value of straight debt | B29 | 1000 |
| Interest expense on debt | B30 | 56 |
| Average maturity of debt (years) | B31 | 3 |
| Approach for pre-tax cost of debt | B32 | Direct input |
| If direct input: pre-tax cost of debt | B33 | 0.035 |
| If actual rating: the rating | B34 | Baa2/BBB |
| If synthetic rating: type of company (1 or 2) | B35 | 1 |
| Pre-tax operating income (for synthetic rating) | B36 | 1500 |
| Approach for marginal tax rate | B38 | Will input |
| If direct input: tax rate | B39 | 0.35 |
| Book value of convertible debt | B42 | 0 |
| Interest expense on convertible | B43 | 0 |
| Maturity of convertible bond (years) | B44 | 0 |
| Market value of convertible | B45 | 0 |
| Number of preferred shares | B50 | 0 |
| Current market price per preferred share | B51 | 70 |
| Annual preferred dividend per share | B52 | 5 |

Side calculators (columns H–L, all rows are user inputs except lookup/derived columns):

- **Operating Countries ERP calculator** (H2:L22): up to ~19 rows of {Country (col H), Revenues (col I)}. Example: Argentina 19, France 81.
- **Operating Regions ERP calculator** (H24:L35): fixed region list (Africa, Asia, Australia & New Zealand, Caribbean, Central and South America, Eastern Europe & Russia, Middle East, North America, Western Europe); user enters Revenues per region (col I). Example: Asia 56, Caribbean 100, Middle East 631, North America 374, Western Europe 168 (total 1329).
- **Multi Business (US Industry Averages)** (H39:L52): up to ~13 rows of {Business = US industry name (col H), Revenues (col I)}. Example: Advertising 84, Entertainment 16.
- **Multi Business (Global Industry Averages)** (H55:L68): same, using global industry names. Example: Advertising 84, Internet software and services 16.

Dropdown option lists (`Answer keys` sheet):

- Yes/No: {Yes, No}
- Book-or-Market: {B, V}
- ERP choices: {Will input, Country of incorporation, Operating countries, Operating regions}
- Cost of debt: {Direct input, Synthetic rating, Actual rating}
- Synthetic-rating firm type: {1, 2}
- Beta: {Direct input, Single Business(US), Single Business(Global), Multibusiness(US), Multibusiness(Global)}

**Logic** (all inferred from values; each step verified numerically):

*Equity market value*
- MV_equity (B62) = shares × price = B17 × B18. (2407 × 37.53 = 90,334.71)

*Unlevered beta (B22), by B20 approach:*
- Direct input: use B21, the levered (regression) beta. This branch is inferred and was not exercised in the saved state, so its exact handling could not be verified. A port should either treat B21 as the final levered beta and skip relevering, or unlever it at the market D/E and relever. Damodaran's convention in this sheet family is to use the regression beta directly as the levered beta.
- Single Business(US): lookup Unlevered Beta for industry B5 in `Industry Averages(US)`.
- Single Business(Global): lookup Unlevered Beta for industry B6 in `Global industry averages`. (Saved state: Advertising global → 1.0965182129122983 = B22.)
- Multibusiness(US): from the US multi-business calculator — for each business row: EV/Sales (J) = lookup in US industry table; Estimated Value (K) = Revenues × EV/Sales; Unlevered Beta (L) = lookup. Company unlevered beta (L52) = Σ(K_i × L_i) / Σ(K_i) — value-weighted average. (Saved: 163.444×0.826443 + 49.7617×0.986107, total value 213.206 → 0.863708.)
- Multibusiness(Global): identical using the global table (L68 = 1.05102 in saved state).

*ERP used in cost of equity (B26), by B24 approach:*
- Will input: B26 = B25.
- Country of incorporation: lookup ERP for B4 in `Country risk and taxes` (col ERP).
- Operating countries: in the countries calculator, ERP (J) = lookup country in `Country risk and taxes` col ERP; Weight (K) = Revenues / total revenues; B26 = Σ weights × ERPs (L22). (Saved example: 0.19×0.17 + 0.81×0.0635 = 0.083735 — not selected.)
- Operating regions: region ERP (J) = lookup region in the regional block at the bottom of `Country risk and taxes` (identical values appear in the region block of `Country equity risk premiums`, which are GDP-weighted averages of country ERPs); Weight = Revenues/total; B26 = Σ weight × ERP = L35. (Saved: B26 = 0.0712735, selected approach.)

*Pre-tax cost of debt (B37), by B32 approach:*
- Direct input: B37 = B33. (Saved: 0.035.)
- Actual rating: B37 = riskfree + default spread for rating B34, looked up in the rating→spread list on `Synthetic rating` (G38:H53).
- Synthetic rating: B37 = cost of debt from the `Synthetic rating` sheet (riskfree + synthetic-rating spread + country default spread), driven by B35 (firm type) and B36 (operating income). Circular with the lease converter (leases discounted at the cost of debt, which depends on lease-adjusted coverage) — Excel iteration must be on.

*Tax rate (B40):*
- B40 = IF(B38 = "Will input", B39, marginal tax rate of country B4 from `Country risk and taxes`) (inferred). NOTE: in the saved file B40 = 0.40 while B39 = 0.35 and the US marginal rate in the table is 0.25 — the saved cell appears to have been manually overridden. B40 (0.40) is the rate actually used everywhere downstream (verified in the relevered beta and after-tax cost of debt).

*Debt components:*
- MV of straight debt (C55) = B30 × [1 − (1+B37)^−B31]/B37 + B29/(1+B37)^B31 — interest as an annuity plus face value discounted at the current pre-tax cost of debt over average maturity. (56×2.801637 + 1000/1.035³ = 1058.8344 ✓)
- Straight-debt value of convertible (C56) = B43 × [1 − (1+B37)^−B44]/B37 + B42/(1+B37)^B44 (inferred; 0 in saved state). Equity portion of convertible (C58) = B45 − C56 (goes to equity, not debt).
- Debt value of operating leases (C57) = result of `Operating lease converter` (1127.9205); 0 if B7 = "No".
- MV_debt (C62) = C55 + C56 + C57 = 2186.7549.
- MV_preferred (D62) = B50 × B51 = 0.

*Costs and WACC:*
- Levered beta (C59) = B22 × [1 + (1 − B40) × MV_debt/MV_equity] = 1.0965182 × (1 + 0.6 × 0.0242072) = 1.1124444.
- Cost of equity (B64) = B23 + C59 × B26 = 0.025 + 1.1124444 × 0.0712735 = 0.1042878.
- After-tax cost of debt (C64) = B37 × (1 − B40) = 0.035 × 0.6 = 0.021.
- Cost of preferred (D64) = B52 / B51 = 5/70 = 0.0714286.
- Total capital (E62) = B62 + C62 + D62 = 92,521.465. Weights (row 63) = component MV / E62.
- **WACC (E64)** = Σ weight × component cost = 0.9763649×0.1042878 + 0.0236351×0.021 + 0×0.0714286 = **0.1023193** (10.23%).

**Outputs:**

| Cell | Meaning | Saved value |
|---|---|---|
| C55 | Market value of straight debt | 1058.8344 |
| C56 | Straight-debt value inside the convertible | 0 |
| C57 | Debt value of operating leases | 1127.9205 |
| C58 | Equity value in the convertible | 0 |
| C59 | Levered beta for equity | 1.1124444 |
| B26 | ERP used in cost of equity | 0.0712735 |
| B62 / C62 / D62 / E62 | Market values: equity / debt / preferred / total capital | 90334.71 / 2186.7549 / 0 / 92521.465 |
| B63 / C63 / D63 | Capital weights: equity / debt / preferred | 0.976365 / 0.023635 / 0 |
| B64 / C64 / D64 | Component costs: equity / after-tax debt / preferred | 0.1042878 / 0.021 / 0.0714286 |
| E64 | **Cost of capital (WACC)** | 0.1023193 |

#### Sheet: Operating lease converter

**Inputs:** current-year operating lease expense (E4 = 180); commitments years 1–5 (B7:B11 = 156, 150, 145, 143, 140); lump-sum commitment for year 6 and beyond (B12 = 600). Pre-tax cost of debt (C15 = 0.035) is linked from the main sheet (B37). All linked from B9:B15 of the main sheet.

**Logic (inferred, verified):**
1. Years embedded in the year-6+ lump sum: D18 = ROUND(B12 / AVERAGE(B7:B11), 0) = ROUND(600/146.8, 0) = 4.
2. Annualized year-6+ commitment: B27 = B12 / D18 = 150.
3. PV of each explicit year t = 1..5: C(21+t) = B(21+t) / (1+r)^t with r = C15. (156/1.035 = 150.7246, …, 140/1.035⁵ = 117.8762.)
4. PV of year-6+ block as a D18-year annuity starting in year 6: C27 = B27 × [1 − (1+r)^−D18]/r ÷ (1+r)^5 = 150 × 3.673079 / 1.187686 = 463.8951. (The in-sheet comment says "annuity for ten years" but the computation actually uses the D18 = 4-year annuity.)
5. **Debt value of leases** C28 = Σ C22:C27 = 1127.9205.
6. Straight-line depreciation on the lease "asset": F31 = C28 / (5 + D18) = 1127.9205/9 = 125.3245.
7. Adjustment to pre-tax operating earnings: F32 = current lease expense − depreciation = E4 − F31 = 180 − 125.3245 = 54.6755 (add to EBIT).
8. Adjustment to total debt: F33 = C28. Adjustment to depreciation: F34 = F31.

**Outputs:** C28 debt value of leases (1127.9205); F31/F34 depreciation (125.3245); F32 EBIT adjustment (+54.6755); F33 debt adjustment (+1127.9205).

#### Sheet: Synthetic rating

**Inputs:** firm type C4 (1 = large manufacturing firm, 2 = smaller/riskier firm; linked from main B35); EBIT F5; current interest expense F6; long-term riskfree rate F7 (linked from B23 = 0.025). In this workbook F5 and F6 are lease-adjusted links (inferred, verified): F5 = B36 + lease EBIT adjustment = 1500 + 54.6755 = 1554.6755; F6 = B30 + r_d × lease debt = 56 + 0.035 × 1127.9205 = 95.4772. For financial firms use only long-term interest expense (sheet note).

**Logic:**
- Interest coverage ratio D9 = F5 / F6 = 16.2832.
- Rating D10 = table lookup of D9 in the firm-type-specific coverage table below (type 1 → large-firm table, type 2 → small-firm table) (inferred). Saved: 16.2832 ≥ 8.5 → Aaa/AAA.
- Default spread D11 = spread column of the same table row (0.004).
- Country default spread D12 = default spread of the country of incorporation (0 for US) (inferred).
- **Estimated cost of debt** D13 = F7 + D11 + D12 = 0.025 + 0.004 + 0 = 0.029.
- Requires Excel iteration (circularity with lease capitalization when the synthetic-rating approach drives the cost of debt).

**Reference data — synthetic rating tables (verbatim).**

For large manufacturing firms (used when firm type = 1). Lookup: coverage ratio > col1 and ≤ col2:

| > | ≤ | Rating | Spread |
|---|---|---|---|
| -100000 | 0.199999 | D2/D | 0.12 |
| 0.2 | 0.649999 | Caa/CCC | 0.10 |
| 0.65 | 0.799999 | Ca2/CC | 0.08 |
| 0.8 | 1.249999 | C2/C | 0.07 |
| 1.25 | 1.499999 | B3/B- | 0.06 |
| 1.5 | 1.749999 | B2/B | 0.05 |
| 1.75 | 1.999999 | B1/B+ | 0.04 |
| 2 | 2.2499999 | Ba2/BB | 0.0325 |
| 2.25 | 2.49999 | Ba1/BB+ | 0.0275 |
| 2.5 | 2.999999 | Baa2/BBB | 0.0175 |
| 3 | 4.249999 | A3/A- | 0.012 |
| 4.25 | 5.499999 | A2/A | 0.01 |
| 5.5 | 6.499999 | A1/A+ | 0.009 |
| 6.5 | 8.499999 | Aa2/AA | 0.007 |
| 8.5 | 100000 | Aaa/AAA | 0.004 |

For smaller and riskier firms (firm type = 2):

| > | ≤ | Rating | Spread |
|---|---|---|---|
| -100000 | 0.499999 | D2/D | 0.12 |
| 0.5 | 0.799999 | Caa/CCC | 0.10 |
| 0.8 | 1.249999 | Ca2/CC | 0.08 |
| 1.25 | 1.499999 | C2/C | 0.07 |
| 1.5 | 1.999999 | B3/B- | 0.06 |
| 2 | 2.499999 | B2/B | 0.05 |
| 2.5 | 2.999999 | B1/B+ | 0.04 |
| 3 | 3.499999 | Ba2/BB | 0.0325 |
| 3.5 | 3.9999999 | Ba1/BB+ | 0.0275 |
| 4 | 4.499999 | Baa2/BBB | 0.0175 |
| 4.5 | 5.999999 | A3/A- | 0.012 |
| 6 | 7.499999 | A2/A | 0.01 |
| 7.5 | 9.499999 | A1/A+ | 0.009 |
| 9.5 | 12.499999 | Aa2/AA | 0.007 |
| 12.5 | 100000 | Aaa/AAA | 0.004 |

Rating → spread list (G38:H53; used for the "Actual rating" cost-of-debt approach):

| Rating | Spread |
|---|---|
| A1/A+ | 0.009 |
| A2/A | 0.01 |
| A3/A- | 0.012 |
| Aa2/AA | 0.007 |
| Aaa/AAA | 0.004 |
| B1/B+ | 0.04 |
| B2/B | 0.05 |
| B3/B- | 0.06 |
| Ba1/BB+ | 0.0275 |
| Ba2/BB | 0.0325 |
| Baa2/BBB | 0.0175 |
| C2/C | 0.07 |
| Ca2/CC | 0.08 |
| Caa/CCC | 0.10 |
| D2/D | 0.12 |

#### Reference data — Industry Averages(US) (rows 2–96 = 95 industries + Total Market)

The lookup key is Industry Name. The main model uses only two columns: Unlevered Beta and EV/Sales. The full 26-column table is reproduced for reuse.

| Industry Name | Number of firms | Annual Average Revenue growth - Last 5 years | Pre-tax Operating Margin | After-tax ROC | Average effective tax rate | Unlevered Beta | Equity (Levered) Beta | Cost of equity | Std deviation in stock prices | Pre-tax cost of debt | Market Debt/Capital | Cost of capital | Sales/Capital | EV/Sales | EV/EBITDA | EV/EBIT | Price/Book | Trailing PE | Non-cash WC as % of Revenues | Cap Ex as % of Revenues | Net Cap Ex as % of Revenues | Reinvestment Rate | ROE | Dividend Payout Ratio | Equity Reinvestment Rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Advertising | 52 | 0.0544147 | 0.112807 | 0.408648 | 0.334785 | 0.826443 | 1.18127 | 0.089623 | 0.51525 | 0.0367 | 0.336086 | 0.0669026 | 3.77757 | 1.94576 | 9.7597 | 17.2002 | 5.51598 | 30.3499 | 0.0117356 | 0.027379 | 0.0105721 | 0.180626 | 0.179214 | 0.725041 | 0.725041 |
| Aerospace/Defense | 93 | 0.040666 | 0.122085 | 0.371806 | 0.28268 | 1.058 | 1.15985 | 0.0883915 | 0.50145 | 0.0367 | 0.159347 | 0.0778154 | 3.57495 | 1.57375 | 10.3458 | 12.935 | 3.61398 | 31.1465 | 0.277976 | 0.0249134 | 0.04809 | 0.759121 | 0.245367 | 0.309974 | 0.309974 |
| Air Transport | 22 | 0.101721 | 0.0802011 | 0.095016 | 0.168864 | 0.610752 | 0.978562 | 0.0779673 | 0.5332 | 0.0367 | 0.449055 | 0.0528439 | 1.457 | 1.78045 | 8.08739 | 22.2156 | 4.00429 | 28.1074 | 0.041196 | 0.0932097 | 0.0608145 | 0.907849 | 0.0284006 | 0.0510077 | 0.0510077 |
| Apparel | 64 | 0.0819582 | 0.129205 | 0.181198 | 0.280938 | 0.859974 | 0.992663 | 0.0787781 | 0.562386 | 0.0367 | 0.171691 | 0.0690333 | 1.57687 | 2.37377 | 12.3897 | 18.4899 | 4.5466 | 27.8194 | 0.270237 | 0.0318236 | 0.0566155 | 0.771483 | 0.184794 | 0.263957 | 0.263957 |
| Auto & Truck | 22 | 0.302571 | 0.0249355 | 0.033055 | 0.0621259 | 0.59008 | 1.095 | 0.0846624 | 0.435215 | 0.0317 | 0.514436 | 0.0508936 | 1.38385 | 0.969697 | 14.5309 | 41.1329 | 2.13936 | 15.063 | -0.00643465 | 0.0593308 | 0.0623766 | 3.52325 | 0.186063 | 0.359005 | 0.359005 |
| Auto Parts | 75 | 0.0910197 | 0.0675067 | 0.181646 | 0.254289 | 1.14371 | 1.34817 | 0.0992197 | 0.538922 | 0.0367 | 0.222659 | 0.0820305 | 3.02695 | 0.829924 | 8.15595 | 12.1423 | 2.72774 | 20.3514 | 0.0939531 | 0.0380138 | 0.0632525 | 1.33172 | 0.158446 | 0.210362 | 0.210362 |
| Bank (Money Center) | 13 | 0.0999889 | -0.00240402 | -0.000244996 | 0.306619 | 0.337662 | 0.806816 | 0.0680919 | 0.399782 | 0.0317 | 0.686187 | 0.0344194 | 0.138515 | 8.00961 | NA | NA | 1.04523 | 17.2609 | NA | 0.0129873 | 0.00409402 | NA | 0.0820826 | 0.231517 | 0.231517 |
| Banks (Regional) | 676 | 0.134506 | -0.00353192 | -0.00076851 | 0.276639 | 0.372229 | 0.526089 | 0.0519501 | 0.374059 | 0.0317 | 0.437227 | 0.0375522 | 0.274249 | 5.4271 | NA | NA | 1.18051 | 47.602 | NA | 0.0636659 | 0.00534127 | NA | 0.0887219 | 0.268256 | 0.268256 |
| Beverage (Alcoholic) | 22 | 0.0849422 | 0.214033 | 0.158475 | 0.259856 | 0.894395 | 1.05553 | 0.0823927 | 0.551369 | 0.0367 | 0.179505 | 0.0715555 | 0.809541 | 4.60146 | 17.3246 | 21.291 | 3.35268 | 32.9342 | 0.221159 | 0.0727423 | 0.0702546 | 0.424938 | 0.136552 | 0.244853 | 0.244853 |
| Beverage (Soft) | 46 | 0.0471692 | 0.187558 | 0.27577 | 0.243779 | 0.975486 | 1.13753 | 0.0871079 | 0.619429 | 0.0367 | 0.187274 | 0.0749186 | 1.55659 | 3.30108 | 14.2631 | 17.6268 | 5.92523 | 36.736 | 0.000126929 | 0.0453464 | 0.0452951 | 0.316223 | 0.278754 | 0.558827 | 0.558827 |
| Broadcasting | 28 | 0.0956145 | 0.230804 | 0.199803 | 0.311049 | 0.83336 | 1.29616 | 0.096229 | 0.621231 | 0.0367 | 0.415408 | 0.065402 | 1.06006 | 3.45319 | 10.6778 | 14.9611 | 2.56777 | 24.7875 | 0.228202 | 0.0302585 | 0.0569246 | 0.439211 | 0.188029 | 0.100943 | 0.100943 |
| Brokerage & Investment Banking | 46 | 0.0978292 | 0.00111714 | 0.000169023 | 0.278205 | 0.41141 | 1.15946 | 0.088369 | 0.447721 | 0.0317 | 0.752192 | 0.0362053 | 0.175831 | 5.85266 | NA | NA | 1.28792 | 33.1811 | NA | 0.0189033 | 0.0255393 | -527.967 | 0.103815 | 0.157996 | 0.157996 |
| Building Materials | 39 | 0.083365 | 0.0775487 | 0.154118 | 0.231676 | 0.927774 | 1.11588 | 0.085863 | 0.435238 | 0.0317 | 0.243759 | 0.0695694 | 2.40576 | 1.36165 | 11.809 | 17.5969 | 3.2279 | 32.8282 | 0.173293 | 0.0329291 | 0.0470143 | 0.968864 | 0.14808 | 0.188952 | 0.188952 |
| Business & Consumer Services | 177 | 0.0409608 | 0.0978292 | 0.239521 | 0.356239 | 0.996262 | 1.19385 | 0.0903462 | 0.527674 | 0.0367 | 0.233177 | 0.0744141 | 2.82289 | 1.58997 | 10.1573 | 16.027 | 3.5145 | 91.6679 | 0.145054 | 0.0296472 | 0.0463989 | 0.905399 | 0.124264 | 0.299045 | 0.299045 |
| Cable TV | 18 | 0.03159 | 0.191209 | 0.173273 | 0.34198 | 0.695488 | 0.913013 | 0.0741982 | 0.528321 | 0.0367 | 0.309404 | 0.0580541 | 1.14963 | 2.84844 | 9.20407 | 14.8198 | 5.67333 | 55.6683 | 0.0127161 | 0.118973 | 0.0202617 | 0.178116 | 0.314281 | 0.211473 | 0.211473 |
| Chemical (Basic) | 46 | 0.141679 | 0.121023 | 0.180387 | 0.321044 | 0.752759 | 0.935056 | 0.0754657 | 0.503224 | 0.0367 | 0.287284 | 0.0601116 | 1.67271 | 1.15669 | 6.4799 | 9.41271 | 1.82242 | 35.4038 | 0.196543 | 0.0647967 | 0.102204 | 1.38254 | 0.147153 | 0.697343 | 0.697343 |
| Chemical (Diversified) | 10 | 0.079025 | 0.107062 | 0.136617 | 0.258569 | 0.987204 | 1.17276 | 0.089134 | 0.411414 | 0.0317 | 0.249221 | 0.0716601 | 1.6473 | 1.52881 | 9.55669 | 14.2369 | 2.80709 | 18.3963 | 0.232262 | 0.0570845 | 0.0559353 | 0.881308 | 0.216045 | 0.362666 | 0.362666 |
| Chemical (Specialty) | 103 | 0.0872631 | 0.14739 | 0.224096 | 0.275761 | 0.912811 | 1.02586 | 0.0806872 | 0.517978 | 0.0367 | 0.176003 | 0.0703616 | 1.71003 | 2.37582 | 11.8451 | 16.1575 | 3.98867 | 23.731 | 0.208628 | 0.0608171 | 0.102667 | 0.979627 | 0.192189 | 0.280205 | 0.280205 |
| Coal & Related Energy | 42 | 0.0119667 | 0.00614588 | 0.00377687 | 0.00822157 | 0.832008 | 1.64223 | 0.116128 | 0.746246 | 0.0417 | 0.524747 | 0.0683194 | 0.640149 | 1.76445 | 8.91105 | 66.8104 | 1.31918 | 11.3965 | 0.0555517 | 0.13798 | 0.0147722 | -0.599924 | -0.0640773 | 0.00512257 | 0.00512257 |
| Computer Services | 119 | 0.131357 | 0.0953464 | 0.373938 | 0.203078 | 0.98577 | 1.15963 | 0.088379 | 0.594051 | 0.0367 | 0.216061 | 0.0740414 | 4.38073 | 1.03141 | 8.3948 | 10.7862 | 5.05218 | 21.258 | 0.114391 | 0.0166941 | 0.0280949 | 0.537393 | 0.320128 | 0.263951 | 0.263951 |
| Computers/Peripherals | 64 | 0.0433845 | 0.198013 | 0.309769 | 0.253654 | 1.17194 | 1.2106 | 0.0913094 | 0.663533 | 0.0417 | 0.0864773 | 0.0855769 | 1.68509 | 2.4463 | 9.99537 | 12.638 | 4.49701 | 47.1298 | 0.0497612 | 0.0435349 | 0.0722781 | 0.41979 | 0.25043 | 0.277441 | 0.277441 |
| Construction Supplies | 55 | 0.0897881 | 0.100261 | 0.124156 | 0.290177 | 1.22103 | 1.60082 | 0.113747 | 0.472618 | 0.0317 | 0.312171 | 0.0841759 | 1.48133 | 1.5084 | 10.3427 | 14.8828 | 3.03687 | 24.7324 | 0.171715 | 0.0534648 | 0.0645502 | 0.940908 | 0.195022 | 0.328855 | 0.328855 |
| Diversified | 23 | 0.0896357 | 0.151569 | 0.0765626 | 0.215531 | 0.699278 | 0.998263 | 0.0791001 | 0.328485 | 0.0317 | 0.378445 | 0.0563631 | 0.586824 | 2.95627 | 14.0323 | 19.4619 | 1.83535 | 22.7794 | 0.0222322 | 0.0719162 | 0.0981265 | 0.922583 | 0.109984 | 0.258329 | 0.258329 |
| Drugs (Biotechnology) | 400 | 0.168391 | 0.274658 | 0.136347 | 0.201115 | 1.06165 | 1.10415 | 0.0851884 | 0.930608 | 0.0517 | 0.0781775 | 0.0809536 | 0.502592 | 10.8049 | 19.0568 | 36.3937 | 8.61712 | 223.022 | 0.234812 | 0.0372416 | 0.229602 | 1.5462 | 0.119399 | 0.220486 | 0.220486 |
| Drugs (Pharmaceutical) | 151 | 0.162922 | 0.249363 | 0.184004 | 0.19418 | 0.949322 | 1.02719 | 0.0807636 | 0.750435 | 0.0417 | 0.118303 | 0.0741689 | 0.7729 | 4.71543 | 13.5807 | 18.7899 | 4.02374 | 49.1274 | 0.246907 | 0.0381848 | 0.0782132 | 0.437631 | 0.17059 | 0.618531 | 0.618531 |
| Education | 42 | 0.0326923 | 0.0683477 | 0.0996628 | 0.298138 | 0.946816 | 1.1274 | 0.0865256 | 0.701903 | 0.0417 | 0.282759 | 0.0691343 | 1.65663 | 1.4211 | 7.5613 | 20.1449 | 2.24566 | 1476.1 | 0.100671 | 0.0494625 | 0.0355932 | 1.25025 | 0.0376303 | 0.251407 | 0.251407 |
| Electrical Equipment | 126 | 0.293944 | 0.131467 | 0.295597 | 0.317701 | 1.14292 | 1.23772 | 0.092869 | 0.653409 | 0.0417 | 0.144292 | 0.0830789 | 2.38796 | 1.92598 | 10.1472 | 13.7365 | 3.69319 | 28.8351 | 0.212695 | 0.0407295 | 0.0756513 | 1.03861 | 0.126089 | 0.495993 | 0.495993 |
| Electronics (Consumer & Office) | 28 | 0.022 | 0.0856857 | 0.182912 | 0.250521 | 1.37859 | 1.3721 | 0.100596 | 0.561594 | 0.0367 | 0.0424472 | 0.0972602 | 2.21895 | 2.08866 | 19.552 | 28.4888 | 5.70017 | 53.395 | 0.194644 | 0.0271813 | 0.0904898 | 1.66488 | 0.128067 | 0.294772 | 0.294772 |
| Electronics (General) | 189 | 0.0613163 | 0.0926883 | 0.113471 | 0.267529 | 1.01434 | 1.02775 | 0.0807958 | 0.690137 | 0.0417 | 0.128111 | 0.0736503 | 1.3375 | 1.65984 | 11.0224 | 18.0162 | 2.21136 | 59.0628 | 0.212137 | 0.0445381 | 0.0696312 | 1.19508 | 0.0866545 | 0.145454 | 0.145454 |
| Engineering/Construction | 56 | 0.0504452 | 0.0445825 | 0.177931 | 0.34583 | 1.19096 | 1.3073 | 0.0968696 | 0.479085 | 0.0317 | 0.214523 | 0.0801691 | 4.65189 | 0.542862 | 7.5985 | 12.0823 | 1.58399 | 26.6687 | 0.156651 | 0.0171373 | 0.0468644 | 1.7032 | 0.0527342 | 0.138842 | 0.138842 |
| Entertainment | 84 | 0.162624 | 0.195624 | 0.308661 | 0.291492 | 0.986107 | 1.2057 | 0.0910277 | 0.584802 | 0.0367 | 0.215836 | 0.0761333 | 1.6455 | 3.11011 | 11.7069 | 15.7862 | 3.54192 | 41.7465 | 0.110804 | 0.0395315 | 0.0225054 | 0.922088 | 0.17837 | 0.229728 | 0.229728 |
| Environmental & Waste Services | 103 | 0.163725 | 0.127902 | 0.195278 | 0.428231 | 0.94163 | 1.28439 | 0.0955526 | 0.656055 | 0.0417 | 0.288642 | 0.0751939 | 1.62973 | 2.21662 | 9.96726 | 17.1739 | 3.01718 | 63.6071 | 0.145222 | 0.0687814 | 0.0260409 | 0.402215 | 0.0567789 | 0.949778 | 0.949778 |
| Farming/Agriculture | 37 | 0.17016 | 0.0534361 | 0.0972138 | 0.319199 | 0.579094 | 0.843254 | 0.0701871 | 0.415903 | 0.0317 | 0.376802 | 0.0509072 | 2.0066 | 0.71216 | 9.64856 | 13.2826 | 1.8959 | 30.1726 | 0.102422 | 0.0264221 | 0.0413579 | 0.901979 | 0.135387 | 0.259988 | 0.259988 |
| Financial Svcs. (Non-bank & Insurance) | 288 | 0.124876 | 0.0692165 | 0.00185078 | 0.285368 | 0.0632074 | 0.667704 | 0.060093 | 0.387978 | 0.0317 | 0.923469 | 0.0221634 | 0.032803 | 31.6698 | NA | NA | 1.8332 | 66.1408 | NA | 0.103913 | 0.118607 | 2.29521 | -0.0222825 | 0.0985458 | 0.0985458 |
| Food Processing | 96 | 0.0912634 | 0.120107 | 0.265018 | 0.306266 | 0.823653 | 0.993819 | 0.0788446 | 0.420482 | 0.0317 | 0.213888 | 0.0660488 | 2.5566 | 1.81509 | 11.9132 | 15.0796 | 3.52598 | 26.8652 | 0.107609 | 0.0335612 | 0.0993207 | 1.16118 | 0.181668 | 0.402217 | 0.402217 |
| Food Wholesalers | 14 | 0.1072 | 0.032976 | 0.212605 | 0.367808 | 1.25731 | 1.41296 | 0.102945 | 0.357284 | 0.0317 | 0.146004 | 0.0906919 | 7.45118 | 0.515387 | 11.2139 | 15.6008 | 3.63716 | 29.917 | 0.0796528 | 0.0127932 | 0.0181352 | 1.05321 | 0.160972 | 0.581975 | 0.581975 |
| Furn/Home Furnishings | 27 | 0.0605588 | 0.0825224 | 0.152998 | 0.21565 | 0.921454 | 1.0898 | 0.0843635 | 0.542397 | 0.0367 | 0.210159 | 0.0712615 | 2.16781 | 1.27903 | 10.3571 | 15.4172 | 2.95016 | 24.8091 | 0.143882 | 0.0386704 | 0.0513241 | 0.997706 | 0.116167 | 0.263641 | 0.263641 |
| Green & Renewable Energy | 26 | 0.2892 | 0.153957 | 0.0436334 | 0.243823 | 0.676261 | 1.31969 | 0.0975823 | 0.531847 | 0.0367 | 0.523722 | 0.0580086 | 0.289232 | 9.23065 | 14.3195 | 52.0251 | 1.34501 | 20.9774 | 0.120669 | 1.24949 | 1.72541 | 16.3653 | 0.00309695 | 0.0268986 | 0.0268986 |
| Healthcare Products | 261 | 0.0896672 | 0.17107 | 0.160532 | 0.255801 | 0.904155 | 0.989273 | 0.0785832 | 0.644821 | 0.0367 | 0.135442 | 0.0709222 | 1.00498 | 3.69598 | 14.4871 | 21.0557 | 3.74911 | 76.4487 | 0.264561 | 0.0501761 | 0.115125 | 1.0272 | 0.112332 | 0.373934 | 0.373934 |
| Healthcare Support Services | 138 | 0.103023 | 0.0454628 | 0.370972 | 0.385298 | 0.907813 | 1.05379 | 0.082293 | 0.467225 | 0.0317 | 0.210462 | 0.0689764 | 9.40893 | 0.612368 | 10.4895 | 13.4286 | 2.83528 | 60.0986 | -0.0245763 | 0.00771182 | 0.0117329 | 0.654096 | 0.122666 | 0.181361 | 0.181361 |
| Heathcare Information and Technology | 127 | 0.149191 | 0.126729 | 0.175578 | 0.226241 | 0.836316 | 0.949821 | 0.0763147 | 0.704907 | 0.0417 | 0.164932 | 0.0678546 | 1.47425 | 3.6715 | 17.5655 | 29.7684 | 4.09997 | 254.404 | 0.233327 | 0.0338314 | 0.244923 | 2.76818 | 0.103914 | 0.125361 | 0.125361 |
| Homebuilding | 35 | 0.132924 | 0.102193 | 0.0956827 | 0.313465 | 0.920378 | 1.28651 | 0.0956744 | 0.537821 | 0.0367 | 0.377957 | 0.0678362 | 1.14332 | 1.60103 | 14.4353 | 15.5872 | 1.69323 | 22.8464 | 0.998948 | 0.00596032 | 0.0547645 | 2.98604 | 0.143441 | 0.0630051 | 0.0630051 |
| Hospitals/Healthcare Facilities | 56 | 0.115685 | 0.128431 | 0.0946833 | 0.22462 | 0.588886 | 0.972759 | 0.0776336 | 0.431119 | 0.0317 | 0.430458 | 0.0524029 | 0.827805 | 2.7041 | 12.2374 | 21.0077 | 2.77086 | 52.8862 | 0.217323 | 0.0491261 | 0.074219 | 1.25368 | 0.104785 | 0.823888 | 0.823888 |
| Hotel/Gaming | 80 | 0.0745721 | 0.152296 | 0.086145 | 0.18021 | 0.82845 | 1.18083 | 0.0895979 | 0.495537 | 0.0317 | 0.353324 | 0.0646611 | 0.63844 | 3.4586 | 12.9659 | 22.5581 | 3.54569 | 28.3702 | 0.0621866 | 0.07944 | 0.0298363 | 0.199517 | 0.0576575 | 1.26857 | 1.26857 |
| Household Products | 135 | 0.121249 | 0.165082 | 0.303761 | 0.276586 | 0.910083 | 1.02788 | 0.0808029 | 0.616294 | 0.0367 | 0.158902 | 0.0714622 | 2.05463 | 2.66314 | 12.7985 | 16.1311 | 4.91823 | 67.1107 | 0.113278 | 0.039411 | 0.0577277 | 0.415391 | 0.193133 | 0.592904 | 0.592904 |
| Information Services | 67 | 0.0699117 | 0.224443 | 0.359706 | 0.302521 | 1.04455 | 1.11498 | 0.0858112 | 0.427134 | 0.0317 | 0.117478 | 0.0779647 | 1.95207 | 3.96461 | 14.0659 | 17.694 | 5.48495 | 50.4016 | 0.150119 | 0.0308367 | 0.0543793 | 0.386273 | 0.216587 | 0.229559 | 0.229559 |
| Insurance (General) | 24 | 0.0482806 | 0.140235 | 0.0767742 | 0.26451 | 0.803871 | 1.02931 | 0.0808856 | 0.353452 | 0.0317 | 0.300884 | 0.0622712 | 0.677601 | 1.55889 | 8.22988 | 11.1186 | 0.888658 | 43.7156 | -0.111444 | 0.0169807 | 0.0339974 | 0.31232 | 0.0739226 | 0.171685 | 0.171685 |
| Insurance (Life) | 25 | 0.0497513 | 0.141188 | 0.0873221 | 0.266567 | 0.753801 | 1.04177 | 0.0816016 | 0.344791 | 0.0317 | 0.415995 | 0.055568 | 0.817045 | 1.50603 | 9.79403 | 10.6659 | 1.02942 | 20.0306 | 0.134285 | 0.00162255 | 0.0111802 | 0.133683 | 0.101265 | 0.242884 | 0.242884 |
| Insurance (Prop/Cas.) | 52 | 0.0950254 | 0.147058 | 0.119934 | 0.286074 | 0.692924 | 0.829115 | 0.0693741 | 0.367338 | 0.0317 | 0.247569 | 0.056908 | 1.04807 | 1.37858 | 8.59475 | 9.36715 | 1.29589 | 17.6772 | -0.222472 | 0.00693537 | 0.0252819 | 0.290829 | 0.124087 | 0.231171 | 0.231171 |
| Investments & Asset Management | 148 | 0.157274 | 0.185567 | 0.0654617 | 0.158683 | 0.728675 | 1.09823 | 0.0848482 | 0.416319 | 0.0317 | 0.425519 | 0.0568371 | 0.378618 | 4.941 | 20.7865 | 24.6862 | 1.1936 | 19.0471 | NA | 0.0191651 | 0.0147023 | 0.0550527 | 0.134516 | 0.483135 | 0.483135 |
| Machinery | 137 | 0.0695631 | 0.132212 | 0.241587 | 0.28953 | 1.11236 | 1.22662 | 0.0922306 | 0.462177 | 0.0317 | 0.169668 | 0.0798091 | 2.1648 | 1.7971 | 10.4573 | 13.5649 | 3.14769 | 161.094 | 0.229463 | 0.0302902 | 0.0740829 | 0.885161 | 0.166572 | 0.253584 | 0.253584 |
| Metals & Mining | 124 | 0.0376056 | 0.160909 | 0.132395 | 0.335193 | 0.905158 | 1.28092 | 0.095353 | 0.744877 | 0.0417 | 0.336379 | 0.0716945 | 0.837821 | 1.83086 | 6.47151 | 11.1197 | 1.41707 | 25.7989 | 0.123879 | 0.198896 | 0.10525 | 1.0908 | 0.0214529 | 2.6166 | 2.6166 |
| Office Equipment & Services | 25 | 0.0171824 | 0.0942287 | 0.214054 | 0.320141 | 0.99914 | 1.34258 | 0.0988985 | 0.498747 | 0.0317 | 0.341592 | 0.0716127 | 2.79065 | 1.21359 | 8.90598 | 12.7692 | 4.25148 | 19.6775 | 0.104209 | 0.0302661 | 0.0491744 | 0.915589 | 0.277691 | 0.303623 | 0.303623 |
| Oil/Gas (Integrated) | 8 | 0.047225 | 0.12249 | 0.159914 | 0.376426 | 0.764286 | 0.807802 | 0.0681486 | 0.33558 | 0.0317 | 0.0995743 | 0.0632567 | 1.52782 | 1.13878 | 5.90094 | 9.30176 | 1.64928 | 9.46789 | 0.0207462 | 0.132531 | 0.0664073 | 0.979235 | 0.168335 | 0.336457 | 0.336457 |
| Oil/Gas (Production and Exploration) | 392 | 0.26593 | 0.239108 | 0.118405 | 0.414624 | 0.914187 | 1.26675 | 0.0945379 | 0.719289 | 0.0417 | 0.325145 | 0.0719345 | 0.532699 | 2.68071 | 5.08841 | 10.8701 | 1.34636 | 29.3927 | -0.0279635 | 0.620619 | 0.383382 | 2.49476 | 0.0625278 | 0.554036 | 0.554036 |
| Oil/Gas Distribution | 85 | 0.227994 | 0.0741479 | 0.1027 | 0.175342 | 0.668999 | 0.96423 | 0.0771432 | 0.431532 | 0.0317 | 0.3232 | 0.0583578 | 1.45305 | 1.93394 | 16.0256 | 25.0299 | 2.22609 | 113.531 | 0.032273 | 0.129634 | 0.138412 | 2.21044 | 0.0957051 | 1.58352 | 1.58352 |
| Oilfield Svcs/Equip. | 161 | 0.183137 | 0.0608608 | 0.177984 | 0.286817 | 1.31878 | 1.54328 | 0.110438 | 0.652319 | 0.0417 | 0.216468 | 0.091948 | 3.28417 | 0.635755 | 6.92452 | 10.3886 | 1.73832 | 18.3966 | 0.0892355 | 0.0380728 | 0.0365044 | 0.960475 | 0.140356 | 0.304857 | 0.304857 |
| Packaging & Container | 26 | 0.0623575 | 0.0988248 | 0.194751 | 0.266132 | 0.695103 | 0.947236 | 0.0761661 | 0.3106 | 0.0317 | 0.32704 | 0.057477 | 2.4077 | 1.36231 | 9.09494 | 13.7769 | 3.57972 | 26.9911 | 0.116214 | 0.0425596 | 0.0699108 | 0.916043 | 0.206474 | 0.262848 | 0.262848 |
| Paper/Forest Products | 22 | 0.0873631 | 0.0795239 | 0.135528 | 0.194268 | 0.594997 | 0.835454 | 0.0697386 | 0.449419 | 0.0317 | 0.337829 | 0.0526044 | 1.92651 | 1.1867 | 9.05433 | 14.9285 | 3.10912 | 36.8706 | 0.128166 | 0.0486576 | 0.0140157 | 0.29983 | 0.0994434 | 0.6159 | 0.6159 |
| Power | 82 | 0.0573623 | 0.163472 | 0.0697094 | 0.306767 | 0.528526 | 0.829384 | 0.0693896 | 0.297016 | 0.0317 | 0.430975 | 0.0476815 | 0.538297 | 2.96764 | 9.89488 | 18.1428 | 1.84516 | 22.0254 | 0.115573 | 0.215335 | 0.146502 | 1.31269 | 0.0952991 | 0.653904 | 0.653904 |
| Precious Metals | 147 | 0.232208 | 0.067641 | 0.0260261 | 0.44834 | 1.04621 | 1.29317 | 0.096057 | 0.93693 | 0.0517 | 0.289763 | 0.0772117 | 0.390335 | 2.57156 | 6.11313 | 30.1341 | 0.973588 | 17.8698 | 0.305186 | 0.166512 | -0.077278 | 0.276923 | -0.0689516 | 0.00255476 | 0.00255476 |
| Publshing & Newspapers | 43 | 0.00118556 | 0.0944239 | 0.144276 | 0.181565 | 0.882965 | 1.14713 | 0.0876601 | 0.504224 | 0.0367 | 0.321544 | 0.0665539 | 1.79447 | 1.61459 | 9.56836 | 17.1719 | 1.74174 | 53.6095 | 0.122613 | 0.0387893 | 0.0713433 | 1.08282 | 0.199697 | 0.205013 | 0.205013 |
| R.E.I.T. | 213 | 0.191785 | 0.205024 | 0.0255932 | 0.0222876 | 0.426594 | 0.786004 | 0.0668953 | 0.315466 | 0.0317 | 0.469543 | 0.0444158 | 0.126401 | 12.0681 | 22.6715 | 51.8983 | 2.10722 | 43.4519 | 0.412468 | 0.0470438 | -0.00227399 | 0.120242 | 0.0774059 | 1.2484 | 1.2484 |
| Real Estate (Development) | 18 | 0.28522 | 0.120965 | 0.0328467 | 0.698154 | 0.818868 | 1.0216 | 0.0804418 | 0.436524 | 0.0317 | 0.312344 | 0.061257 | 0.292624 | 6.72303 | 27.7582 | 55.2942 | 1.84715 | 147.176 | 0.264887 | 0.0972953 | 0.0904278 | 1.98846 | 0.00496751 | 0 | 0 |
| Real Estate (General/Diversified) | 11 | 0.207 | 0.435195 | 0.19422 | 0.207933 | 1.475 | 1.81903 | 0.126294 | 0.459678 | 0.0317 | 0.216083 | 0.103114 | 0.49265 | 4.17559 | 8.22645 | 9.16697 | 1.81622 | 70.4532 | 0.0779076 | 0.312156 | 0.307289 | 1.01015 | 0.246471 | 0.016547 | 0.016547 |
| Real Estate (Operations & Services) | 52 | 0.172371 | 0.102529 | 0.181191 | 0.224081 | 0.894889 | 1.30231 | 0.096583 | 0.500535 | 0.0367 | 0.36443 | 0.06941 | 1.93412 | 2.47856 | 14.8587 | 23.7403 | 2.68789 | 48.96 | 0.0665706 | 0.0398321 | 0.0391194 | 0.59173 | 0.163573 | 0.064154 | 0.064154 |
| Recreation | 68 | 0.0479025 | 0.127015 | 0.156014 | 0.23188 | 0.986534 | 1.21182 | 0.0913795 | 0.504074 | 0.0367 | 0.240333 | 0.0747102 | 1.38267 | 2.07399 | 10.4122 | 16.3553 | 3.65931 | 32.9393 | 0.203694 | 0.0690861 | 0.0676848 | 0.855481 | 0.24833 | 0.495327 | 0.495327 |
| Reinsurance | 4 | 0.2615 | 0.135278 | 0.118231 | 0.306519 | 1.12478 | 1.34617 | 0.0991048 | 0.212035 | 0.0267 | 0.273177 | 0.076408 | 1.03471 | 1.07079 | 6.70689 | 7.71614 | 0.977354 | 13.2823 | 0.335264 | 0.00790912 | 0.00622622 | 0.248451 | 0.108881 | 0.0619942 | 0.0619942 |
| Restaurant/Dining | 79 | 0.060218 | 0.133786 | 0.150899 | 0.32979 | 0.739284 | 0.892699 | 0.0730302 | 0.444334 | 0.0317 | 0.217969 | 0.0612577 | 1.32906 | 2.98018 | 11.8551 | 21.6823 | 7.79551 | 40.5258 | 0.00777283 | 0.0686402 | 0.0456528 | 0.528184 | 0.32274 | 0.476826 | 0.476826 |
| Retail (Automotive) | 30 | 0.0983187 | 0.0477304 | 0.112651 | 0.36529 | 0.846293 | 1.1754 | 0.0892854 | 0.48055 | 0.0317 | 0.33419 | 0.0658034 | 2.90534 | 0.980148 | 12.5848 | 20.5262 | 6.27095 | 19.4436 | 0.0979675 | 0.0203533 | 0.0386859 | 1.47477 | 0.323375 | 0.0349389 | 0.0349389 |
| Retail (Building Supply) | 5 | 0.0740333 | 0.098294 | 0.162801 | 0.370632 | 1.29043 | 1.44231 | 0.104633 | 0.507137 | 0.0367 | 0.162908 | 0.0911745 | 2.38783 | 1.73717 | 12.415 | 17.6732 | 9.58891 | 29.9017 | 0.0716333 | 0.01758 | -0.00348672 | -0.102532 | 0.303643 | 0.383792 | 0.383792 |
| Retail (Distributors) | 90 | 0.133228 | 0.0924667 | 0.148695 | 0.354944 | 0.81148 | 1.11518 | 0.0858228 | 0.520608 | 0.0367 | 0.324312 | 0.0651308 | 1.93357 | 1.39059 | 12.229 | 15.0167 | 3.32678 | 29.2375 | 0.196496 | 0.0658327 | 0.0804065 | 1.48834 | 0.167899 | 0.299035 | 0.299035 |
| Retail (General) | 23 | 0.0367121 | 0.0453715 | 0.120962 | 0.341881 | 0.850615 | 1.03212 | 0.081047 | 0.463605 | 0.0317 | 0.238817 | 0.0662339 | 3.39005 | 0.764895 | 9.56749 | 16.5704 | 3.54448 | 27.6515 | 0.0442244 | 0.0248866 | 0.0187759 | 0.675065 | 0.171525 | 0.402297 | 0.402297 |
| Retail (Grocery and Food) | 21 | 0.0410909 | 0.0202214 | 0.0651452 | 0.351074 | 0.74728 | 1.04825 | 0.0819746 | 0.51832 | 0.0367 | 0.359538 | 0.0604186 | 4.18051 | 0.555228 | 9.18842 | 27.4368 | 4.20354 | 31.8274 | 0.0086097 | 0.0260679 | 0.0294824 | 2.37125 | 0.390523 | 0.138664 | 0.138664 |
| Retail (Online) | 46 | 0.0659856 | 0.0398645 | 0.173822 | 0.223443 | 1.39227 | 1.39523 | 0.101926 | 0.701644 | 0.0417 | 0.0699438 | 0.0965466 | 4.7838 | 2.26796 | 24.5102 | 59.6152 | 8.19716 | 59.4571 | -0.00670356 | 0.0475862 | 0.0767519 | 2.85264 | 0.119069 | 0.202126 | 0.202126 |
| Retail (Special Lines) | 128 | 0.0648136 | 0.0593144 | 0.109343 | 0.358176 | 0.845975 | 1.0744 | 0.0834779 | 0.514189 | 0.0367 | 0.293043 | 0.0654681 | 2.31712 | 1.21385 | 9.39845 | 20.4074 | 4.01125 | 35.5876 | 0.103589 | 0.0251666 | 0.0299565 | 0.966502 | 0.157846 | 0.301359 | 0.301359 |
| Rubber& Tires | 4 | 0.0431 | 0.0889182 | 0.216226 | 0.239012 | 0.654227 | 1.02102 | 0.0804087 | 0.49538 | 0.0317 | 0.467353 | 0.0517185 | 2.81209 | 0.744548 | 5.30681 | 8.40306 | 2.59306 | 13.7002 | 0.130285 | 0.0554685 | 0.0558348 | 0.885117 | 0.523554 | 0.116194 | 0.116194 |
| Semiconductor | 100 | 0.110821 | 0.209022 | 0.137467 | 0.2175 | 1.16836 | 1.21447 | 0.0915318 | 0.571234 | 0.0367 | 0.0971034 | 0.084782 | 0.728305 | 3.2138 | 10.2924 | 15.894 | 3.43593 | 92.9981 | 0.195402 | 0.109658 | 0.14507 | 0.938281 | 0.161114 | 0.38142 | 0.38142 |
| Semiconductor Equip | 47 | 0.104656 | 0.11518 | 0.0968293 | 0.202855 | 1.17385 | 1.23308 | 0.0926024 | 0.601827 | 0.0367 | 0.149853 | 0.0820254 | 0.898498 | 2.75834 | 12.2078 | 21.5735 | 2.75917 | 48.989 | 0.199332 | 0.111351 | 0.166585 | 2.43548 | 0.0555052 | 0.647898 | 0.647898 |
| Shipbuilding & Marine | 14 | -0.0018 | 0.0943216 | 0.0659939 | 0.162947 | 0.940669 | 1.36183 | 0.100005 | 0.714496 | 0.0417 | 0.349035 | 0.0738326 | 0.750301 | 1.9007 | 9.44274 | 19.5003 | 1.57735 | 13.3939 | 0.0908699 | 0.117313 | 0.0430644 | 0.6824 | 0.207637 | 0.0433004 | 0.0433004 |
| Shoe | 13 | 0.118781 | 0.123906 | 0.216513 | 0.245232 | 0.824947 | 0.842528 | 0.0701454 | 0.407963 | 0.0317 | 0.0684231 | 0.0666472 | 2.18795 | 2.50919 | 15.1718 | 20.2641 | 5.83386 | 21.8786 | 0.21382 | 0.00567209 | 0.00737457 | 0.110044 | 0.240941 | 0.253304 | 0.253304 |
| Software (Entertainment) | 20 | 0.01954 | 0.136406 | 0.137993 | 0.123474 | 1.13181 | 1.11508 | 0.0858173 | 0.69842 | 0.0417 | 0.147506 | 0.0768493 | 1.02755 | 2.86088 | 13.1105 | 18.1909 | 2.74672 | 48.1405 | 0.260893 | 0.0214233 | 0.0484391 | 0.404705 | 0.0711777 | 0.121342 | 0.121342 |
| Software (Internet) | 327 | 0.115197 | 0.203038 | 0.152474 | 0.350623 | 1.29361 | 1.28619 | 0.0956561 | 0.724797 | 0.0417 | 0.052922 | 0.0919179 | 0.785763 | 6.32007 | 21.1032 | 33.7551 | 4.14742 | 157.208 | 0.146671 | 0.115757 | 0.202802 | 1.80348 | 0.13484 | 0.00622535 | 0.00622535 |
| Software (System & Application) | 259 | 0.15901 | 0.263576 | 0.226416 | 0.225184 | 1.06111 | 1.10395 | 0.085177 | 0.618486 | 0.0367 | 0.0884109 | 0.0795932 | 0.919325 | 4.93236 | 14.3161 | 18.4059 | 4.61687 | 85.7314 | 0.123584 | 0.0450413 | 0.132574 | 0.750796 | 0.187681 | 0.375066 | 0.375066 |
| Steel | 40 | 0.0617712 | 0.0460975 | 0.0803523 | 0.303187 | 0.903706 | 1.31298 | 0.0971964 | 0.524477 | 0.0367 | 0.390371 | 0.0678497 | 2.02681 | 0.748818 | 8.62751 | 16.1369 | 1.58433 | 52.0136 | 0.208493 | 0.0350613 | 0.0494101 | 1.73866 | -0.139895 | 0.010514 | 0.010514 |
| Telecom (Wireless) | 21 | 0.0351178 | 0.0143196 | 0.00916568 | 0.217845 | 0.508684 | 1.15007 | 0.0878289 | 0.53045 | 0.0367 | 0.606892 | 0.04789 | 0.678883 | 1.81366 | 7.78733 | 120.937 | 1.3223 | 66.0161 | 0.0487985 | 0.141406 | -0.222015 | -12.1978 | -0.047459 | 0.0525787 | 0.0525787 |
| Telecom. Equipment | 126 | 0.0691496 | 0.189021 | 0.140987 | 0.191798 | 1.19699 | 1.24265 | 0.0931522 | 0.627373 | 0.0367 | 0.104887 | 0.0856913 | 0.816099 | 3.05137 | 12.0146 | 15.8589 | 2.8592 | 77.3676 | 0.169037 | 0.0370858 | 0.049138 | 0.321596 | 0.143954 | 0.373893 | 0.373893 |
| Telecom. Services | 77 | 0.0644932 | 0.224846 | 0.257106 | 0.311433 | 0.691107 | 1.06845 | 0.0831361 | 0.555986 | 0.0367 | 0.395518 | 0.0589636 | 1.29668 | 2.36517 | 6.03213 | 10.5265 | 3.19983 | 32.0044 | -0.0301696 | 0.154596 | 0.019364 | 0.067622 | 0.237236 | 0.550244 | 0.550244 |
| Tobacco | 20 | 0.074895 | 0.407799 | 1.00069 | 0.324725 | 0.945 | 1.08562 | 0.084123 | 0.417353 | 0.0317 | 0.164895 | 0.0733879 | 2.80052 | 4.98987 | 11.5475 | 12.2419 | 955.6 | 19.9158 | 0.159688 | 0.0259578 | 0.0277462 | 0.160632 | -0.541419 | 0.819526 | 0.819526 |
| Transportation | 21 | 0.145007 | 0.0823167 | 0.199752 | 0.358358 | 0.765212 | 0.857089 | 0.0709826 | 0.423571 | 0.0317 | 0.173764 | 0.0619534 | 3.03542 | 1.50059 | 10.6368 | 18.2468 | 6.0367 | 25.1071 | 0.0828465 | 0.047377 | 0.0208443 | 0.527721 | 0.24275 | 0.419012 | 0.419012 |
| Transportation (Railroads) | 10 | 0.1069 | 0.316802 | 0.163538 | 0.369882 | 0.920001 | 1.0476 | 0.0819371 | 0.307302 | 0.0317 | 0.168138 | 0.0713583 | 0.655962 | 4.43033 | 10.509 | 13.9829 | 3.77607 | 25.8059 | 0.028307 | 0.183003 | 0.103018 | 0.507127 | 0.204402 | 0.312644 | 0.312644 |
| Trucking | 30 | 0.0669696 | 0.097857 | 0.0974375 | 0.392312 | 0.917303 | 1.32435 | 0.09785 | 0.484946 | 0.0317 | 0.399983 | 0.0663193 | 1.37107 | 1.63463 | 9.97416 | 16.6962 | 4.34694 | 27.8389 | 0.0575137 | 0.171497 | 0.14965 | 2.6042 | 0.193557 | 0.108645 | 0.108645 |
| Unclassified | 8 | 0.02 | -0.341076 | -0.121806 | 0.295477 | 0.136306 | 0.104256 | 0.0276947 | 7 | 7 | 0.207956 | 7 | 0.372873 | 3.69104 | 114.72 | NA | 1.44415 | 18.8685 | NA | 0.156048 | 0.182682 | NA | -0.11893 | 0 | 0 |
| Utility (General) | 21 | 0.00449952 | 0.159067 | 0.0662182 | 0.312725 | 0.419086 | 0.592407 | 0.0557634 | 0.230224 | 0.0267 | 0.380024 | 0.0406599 | 0.599722 | 2.83246 | 10.5801 | 17.8075 | 2.07812 | 20.1189 | 0.0715874 | 0.235082 | 0.14034 | 1.32748 | 0.110016 | 0.640612 | 0.640612 |
| Utility (Water) | 19 | 0.0686769 | 0.305677 | 0.0885265 | 0.317119 | 0.766327 | 1.08551 | 0.0841171 | 0.382123 | 0.0317 | 0.334077 | 0.0623697 | 0.341136 | 5.19364 | 11.379 | 16.7045 | 2.17654 | 19.8054 | 0.0655294 | 0.30709 | 0.179636 | 0.914968 | 0.100773 | 0.528478 | 0.528478 |
| Total Market | 7887 | 0.115386 | 0.11256 | 0.073588 | 0.280939 | 0.704036 | 1.06412 | 0.0828868 | 0.535978 | 0.0367 | 0.398089 | 0.0586564 | 0.731731 | 2.60231 | 14.729 | 22.7965 | 2.5776 | 60.4915 | -0.166212 | 0.0668261 | 0.0620678 | 0.853004 | 0.144883 | 0.372225 | 0.372225 |

#### Reference data — Global industry averages (same 26 columns, global universe)

| Industry Name | Number of firms | Annual Average Revenue growth - Last 5 years | Pre-tax Operating Margin | After-tax ROC | Average effective tax rate | Unlevered Beta | Equity (Levered) Beta | Cost of equity | Std deviation in stock prices | Pre-tax cost of debt | Market Debt/Capital | Cost of capital | Sales/Capital | EV/Sales | EV/EBITDA | EV/EBIT | Price/Book | Trailing PE | Non-cash WC as % of Revenues | Cap Ex as % of Revenues | Net Cap Ex as % of Revenues | Reinvestment Rate | ROE | Dividend Payout Ratio | Equity Reinvestment Rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Advertising | 253 | 0.09715 | 0.0886178 | 0.282119 | 0.305522 | 1.09652 | 1.27241 | 0.113059 | 0.567182 | 0.0463 | 0.233054 | 0.0942636 | 3.77764 | 1.5086 | 9.78486 | 16.2102 | 2.50328 | 63.9324 | -0.0627245 | 0.0183953 | 0.0144523 | 0.378402 | 0.102104 | 0.513876 | 0.513876 |
| Aerospace/Defense | 208 | 0.0690688 | 0.100358 | 0.2434 | 0.275411 | 0.973467 | 1.07854 | 0.0991391 | 0.478988 | 0.0413 | 0.180954 | 0.0864308 | 2.78424 | 1.3757 | 10.3374 | 13.9774 | 3.26147 | 36.8073 | 0.211061 | 0.0333131 | 0.046085 | 0.943684 | 0.210452 | 0.325292 | 0.325292 |
| Air Transport | 158 | 0.0860995 | 0.0521775 | 0.0517185 | 0.191122 | 0.642689 | 1.08836 | 0.0998444 | 0.435518 | 0.0413 | 0.490591 | 0.0650447 | 1.16217 | 1.41019 | 8.261 | 26.9722 | 2.30494 | 23.9625 | -0.0239504 | 0.0999101 | 0.0538011 | 1.25071 | 0.110883 | 0.326852 | 0.326852 |
| Apparel | 1174 | 0.108643 | 0.123742 | 0.149516 | 0.256066 | 0.725548 | 0.820831 | 0.0806356 | 0.517917 | 0.0463 | 0.198945 | 0.0710414 | 1.44053 | 1.73185 | 9.40418 | 13.5924 | 2.26643 | 53.2048 | 0.238466 | 0.0427885 | 0.0578179 | 0.848249 | 0.120716 | 0.432105 | 0.432105 |
| Auto & Truck | 125 | 0.107899 | 0.058942 | 0.0647283 | 0.229977 | 0.83876 | 1.28092 | 0.11367 | 0.450542 | 0.0413 | 0.452736 | 0.0752963 | 1.2617 | 0.935681 | 9.19357 | 15.5055 | 1.42779 | 31.1578 | 0.0228346 | 0.0708979 | 0.0688305 | 1.63548 | 0.146778 | 0.296208 | 0.296208 |
| Auto Parts | 632 | 0.114374 | 0.0685476 | 0.111456 | 0.249963 | 1.14626 | 1.24943 | 0.111409 | 0.477936 | 0.0413 | 0.202427 | 0.0947089 | 2.01286 | 0.808608 | 7.38943 | 11.7071 | 1.84047 | 43.4998 | 0.0991064 | 0.0545155 | 0.056399 | 1.21455 | 0.133156 | 0.228433 | 0.228433 |
| Bank (Money Center) | 604 | 0.129243 | -0.000274695 | -2.49169e-05 | 0.242921 | 0.385404 | 1.02388 | 0.0952143 | 0.352378 | 0.0413 | 0.733853 | 0.0465567 | 0.11272 | 9.36818 | NA | NA | 1.10794 | 22.9216 | NA | 0.0431401 | 0.0473572 | NA | 0.10256 | 0.367168 | 0.367168 |
| Banks (Regional) | 911 | 0.123438 | -0.00170074 | -0.000348574 | 0.279755 | 0.493979 | 0.655875 | 0.0687919 | 0.367945 | 0.0413 | 0.532053 | 0.0475726 | 0.261913 | 4.39237 | NA | NA | 0.956753 | 37.9583 | NA | 0.0551399 | 0.0244269 | NA | 0.0854858 | 0.234476 | 0.234476 |
| Beverage (Alcoholic) | 216 | 0.0736554 | 0.192295 | 0.133838 | 0.220037 | 0.687155 | 0.790619 | 0.0784665 | 0.430518 | 0.0413 | 0.188159 | 0.0691419 | 0.835319 | 3.32651 | 12.303 | 16.5828 | 2.86251 | 34.363 | 0.0681005 | 0.0536848 | 0.037447 | 0.332871 | 0.140999 | 0.547255 | 0.547255 |
| Beverage (Soft) | 108 | 0.0457665 | 0.152089 | 0.218364 | 0.253469 | 0.80941 | 0.931266 | 0.0885649 | 0.429626 | 0.0413 | 0.192024 | 0.0771097 | 1.64073 | 2.62933 | 13.6065 | 17.2684 | 4.65867 | 64.5345 | 0.0162889 | 0.0341858 | 0.0307153 | -0.346908 | 0.207868 | 0.581326 | 0.581326 |
| Broadcasting | 138 | 0.0518758 | 0.165442 | 0.156082 | 0.302448 | 1.05278 | 1.34811 | 0.118494 | 0.505846 | 0.0463 | 0.29368 | 0.0932129 | 1.17246 | 2.48291 | 10.593 | 14.9118 | 2.35654 | 28.7317 | 0.129164 | 0.0345281 | 0.0281856 | 0.327559 | 0.0863612 | 0.5567 | 0.5567 |
| Brokerage & Investment Banking | 551 | 0.0849829 | 0.00291458 | 0.00043777 | 0.261229 | 0.452756 | 1.04808 | 0.0969523 | 0.567267 | 0.0463 | 0.671421 | 0.0536172 | 0.173145 | 6.95943 | NA | NA | 1.74028 | 248.96 | NA | 0.0263102 | 0.0236646 | -23.1577 | 0.0901344 | 0.277216 | 0.277216 |
| Building Materials | 432 | 0.0934125 | 0.0739776 | 0.098466 | 0.282136 | 0.799764 | 0.960022 | 0.0906296 | 0.47419 | 0.0413 | 0.271273 | 0.0738868 | 1.62944 | 1.11171 | 9.31603 | 14.7817 | 1.75004 | 41.8762 | 0.171007 | 0.0384661 | 0.0416163 | 0.935492 | 0.0850413 | 0.394704 | 0.394704 |
| Business & Consumer Services | 759 | 0.0787241 | 0.0825832 | 0.216386 | 0.30079 | 0.907405 | 1.04696 | 0.0968714 | 0.507011 | 0.0463 | 0.218705 | 0.0827734 | 3.20547 | 1.30744 | 10.1325 | 15.5703 | 3.17436 | 44.502 | 0.094485 | 0.0277934 | 0.0357863 | 0.731194 | 0.152079 | 0.654817 | 0.654817 |
| Cable TV | 64 | 0.10797 | 0.186318 | 0.157217 | 0.312958 | 0.70523 | 0.964682 | 0.0909642 | 0.438753 | 0.0413 | 0.328994 | 0.0705487 | 1.02484 | 3.56143 | 10.9189 | 19.0731 | 5.78595 | 116.115 | 0.134818 | 0.125032 | 0.0273918 | 0.246149 | 0.237474 | 0.299088 | 0.299088 |
| Chemical (Basic) | 731 | 0.102445 | 0.0959573 | 0.109347 | 0.183877 | 0.752594 | 0.949579 | 0.0898798 | 0.464004 | 0.0413 | 0.302522 | 0.0714351 | 1.36142 | 1.06575 | 7.01839 | 10.3836 | 1.44844 | 78.1531 | 0.134238 | 0.0539819 | 0.0560287 | 0.986047 | 0.0891489 | 0.629426 | 0.629426 |
| Chemical (Diversified) | 85 | 0.0876136 | 0.0807556 | 0.0921747 | 0.277705 | 1.13727 | 1.42234 | 0.123824 | 0.437295 | 0.0413 | 0.289397 | 0.0963561 | 1.4471 | 1.12059 | 8.46464 | 13.608 | 1.90624 | 26.7392 | 0.19546 | 0.0591511 | 0.0599553 | 1.09206 | 0.12429 | 0.465557 | 0.465557 |
| Chemical (Specialty) | 700 | 0.104689 | 0.108975 | 0.119529 | 0.260178 | 0.916383 | 1.02837 | 0.095537 | 0.493511 | 0.0413 | 0.190939 | 0.0828153 | 1.32253 | 1.74264 | 10.8746 | 15.7876 | 2.58146 | 34.2212 | 0.174646 | 0.0700197 | 0.0814061 | 1.09074 | 0.123151 | 0.476052 | 0.476052 |
| Coal & Related Energy | 321 | 0.184345 | 0.0968489 | 0.0736017 | 0.236338 | 1.05102 | 1.3805 | 0.12082 | 0.72214 | 0.0513 | 0.350583 | 0.0910519 | 0.806918 | 1.72368 | 8.5504 | 16.4848 | 1.30278 | 70.52 | 0.0244879 | 0.133902 | 0.111923 | 1.88419 | 0.0449914 | 1.17148 | 1.17148 |
| Computer Services | 934 | 0.0921063 | 0.0792179 | 0.233613 | 0.237713 | 0.922282 | 0.986918 | 0.0925607 | 0.529655 | 0.0463 | 0.160724 | 0.082893 | 3.61704 | 1.03065 | 9.55779 | 12.7272 | 3.4439 | 54.5948 | 0.121883 | 0.0171869 | 0.021203 | 0.541399 | 0.196846 | 0.313894 | 0.313894 |
| Computers/Peripherals | 329 | 0.0418035 | 0.11528 | 0.175867 | 0.236033 | 1.12538 | 1.13132 | 0.102929 | 0.552969 | 0.0463 | 0.111535 | 0.0950638 | 1.77878 | 1.29914 | 7.89541 | 11.2614 | 2.51166 | 76.737 | 0.0856226 | 0.0488559 | 0.0583505 | 0.627275 | 0.182562 | 0.26449 | 0.26449 |
| Construction Supplies | 751 | 0.0727032 | 0.0782364 | 0.0793114 | 0.244894 | 0.893402 | 1.15451 | 0.104594 | 0.4814 | 0.0413 | 0.323363 | 0.0801206 | 1.19775 | 1.37066 | 10.0688 | 16.7369 | 1.68414 | 36.1605 | 0.162738 | 0.0531154 | 0.0517572 | 1.26202 | 0.0889553 | 0.542541 | 0.542541 |
| Diversified | 378 | 0.0875898 | 0.100365 | 0.0785171 | 0.177605 | 0.76164 | 1.08051 | 0.0992808 | 0.388836 | 0.0413 | 0.397182 | 0.0713308 | 0.916309 | 1.69107 | 11.2674 | 16.4585 | 1.33585 | 26.9222 | 0.0459093 | 0.0582485 | 0.0610275 | 0.812166 | 0.107493 | 0.299292 | 0.299292 |
| Drugs (Biotechnology) | 782 | 0.165358 | 0.239302 | 0.124623 | 0.194436 | 1.12039 | 1.1578 | 0.10483 | 0.853779 | 0.0563 | 0.0764401 | 0.0998291 | 0.531898 | 10.1184 | 19.7543 | 38.9747 | 7.84437 | 108.437 | 0.246124 | 0.0443633 | 0.21341 | 1.62339 | 0.105784 | 0.29307 | 0.29307 |
| Drugs (Pharmaceutical) | 877 | 0.124047 | 0.209082 | 0.139043 | 0.204026 | 0.852663 | 0.907191 | 0.0868363 | 0.553856 | 0.0463 | 0.114306 | 0.080615 | 0.767678 | 3.9307 | 13.6089 | 18.6907 | 3.7185 | 81.2634 | 0.19485 | 0.0436133 | 0.0765723 | 0.545399 | 0.150007 | 0.61726 | 0.61726 |
| Education | 170 | 0.115291 | 0.0943342 | 0.119317 | 0.23901 | 1.02202 | 1.13596 | 0.103262 | 0.566629 | 0.0463 | 0.217458 | 0.0878544 | 1.4938 | 1.86204 | 9.42447 | 18.9804 | 2.21139 | 310.111 | 0.0840906 | 0.0536998 | 0.0614648 | 1.20912 | 0.0609962 | 0.62789 | 0.62789 |
| Electrical Equipment | 838 | 0.117852 | 0.0751456 | 0.118148 | 0.252505 | 0.98851 | 1.09881 | 0.100594 | 0.499931 | 0.0413 | 0.210319 | 0.0855179 | 1.80987 | 1.31283 | 11.2177 | 16.7626 | 2.22766 | 333.334 | 0.223171 | 0.0373115 | 0.0480912 | 1.0025 | 0.0775867 | 0.571586 | 0.571586 |
| Electronics (Consumer & Office) | 151 | 0.0182994 | 0.0293631 | 0.0485543 | 0.387086 | 1.06727 | 1.21665 | 0.109056 | 0.523591 | 0.0463 | 0.288072 | 0.0869761 | 1.8911 | 0.518371 | 6.9856 | 15.4912 | 1.46885 | 34.8978 | 0.0687027 | 0.0301908 | 0.0278593 | 1.21268 | 0.0234709 | 1.01575 | 1.01575 |
| Electronics (General) | 1227 | 0.0610625 | 0.0625631 | 0.0861495 | 0.242176 | 1.0426 | 1.07719 | 0.099042 | 0.524535 | 0.0463 | 0.178405 | 0.0871545 | 1.60486 | 1.07288 | 9.06588 | 16.7118 | 1.78092 | 54.1879 | 0.184817 | 0.0497254 | 0.0542853 | 1.53812 | 0.0911112 | 0.31529 | 0.31529 |
| Engineering/Construction | 1148 | 0.0535106 | 0.0458049 | 0.0860275 | 0.281462 | 0.885736 | 1.25217 | 0.111606 | 0.524508 | 0.0463 | 0.446157 | 0.0762719 | 2.24582 | 0.670281 | 9.16849 | 14.1914 | 1.47504 | 103.83 | 0.116684 | 0.0309549 | 0.0329371 | 1.51488 | 0.076226 | 0.671943 | 0.671943 |
| Entertainment | 350 | 0.0733169 | 0.169551 | 0.229107 | 0.291898 | 0.935265 | 1.12117 | 0.1022 | 0.597246 | 0.0463 | 0.216707 | 0.0870761 | 1.49363 | 2.98362 | 11.7857 | 17.1419 | 3.29359 | 213.791 | 0.103883 | 0.0413492 | 0.0265043 | 0.944989 | 0.152487 | 0.259392 | 0.259392 |
| Environmental & Waste Services | 307 | 0.0906917 | 0.0940337 | 0.143913 | 0.358251 | 1.00074 | 1.26671 | 0.11265 | 0.628787 | 0.0463 | 0.266759 | 0.0912453 | 1.73892 | 1.72071 | 10.2281 | 17.8884 | 2.61129 | 41.2335 | 0.112966 | 0.058929 | 0.0293886 | 0.655151 | 0.0593108 | 0.866126 | 0.866126 |
| Farming/Agriculture | 408 | 0.118068 | 0.0600197 | 0.0813001 | 0.277117 | 0.644797 | 0.901658 | 0.086439 | 0.461777 | 0.0413 | 0.376195 | 0.0647969 | 1.54551 | 0.93495 | 10.7111 | 15.1654 | 1.58637 | 31.2933 | 0.188184 | 0.0379746 | 0.0467719 | 1.19206 | 0.0968028 | 0.377732 | 0.377732 |
| Financial Svcs. (Non-bank & Insurance) | 966 | 0.173974 | 0.0825526 | 0.00355957 | 0.231574 | 0.104016 | 0.786584 | 0.0781767 | 0.452696 | 0.0413 | 0.89522 | 0.0340722 | 0.052341 | 19.4764 | 155.855 | NA | 1.29948 | 111.519 | NA | 0.0738114 | 0.0826276 | 1.58194 | 0.248362 | 3.33908 | 3.33908 |
| Food Processing | 1247 | 0.08495 | 0.0858499 | 0.142204 | 0.269913 | 0.664897 | 0.772014 | 0.0771306 | 0.425049 | 0.0413 | 0.208069 | 0.0670974 | 1.99632 | 1.43492 | 11.8068 | 16.4791 | 2.68877 | 159.963 | 0.108126 | 0.0450043 | 0.0697811 | 1.15193 | 0.126438 | 0.514546 | 0.514546 |
| Food Wholesalers | 125 | 0.0521896 | 0.0311108 | 0.15644 | 0.293626 | 0.536194 | 0.807366 | 0.0796688 | 0.455434 | 0.0413 | 0.445105 | 0.0570758 | 6.07912 | 0.371256 | 7.70682 | 11.8699 | 1.2518 | 63.6866 | 0.029737 | 0.0160025 | 0.0161711 | 0.909006 | 0.106774 | 0.50992 | 0.50992 |
| Furn/Home Furnishings | 303 | 0.0704117 | 0.0762184 | 0.160897 | 0.198431 | 0.992007 | 1.00963 | 0.0941912 | 0.497327 | 0.0413 | 0.167099 | 0.0832828 | 2.54981 | 0.965841 | 9.24131 | 12.5185 | 2.28851 | 48.1678 | 0.104432 | 0.0305874 | 0.0364232 | 0.508727 | 0.153492 | 0.372832 | 0.372832 |
| Green & Renewable Energy | 167 | 0.0890046 | 0.339182 | 0.0815367 | 0.236194 | 0.743079 | 1.2009 | 0.107924 | 0.534501 | 0.0463 | 0.421431 | 0.0761003 | 0.259359 | 6.20233 | 10.8416 | 18.0348 | 1.53751 | 45.9889 | 0.00847404 | 0.359509 | 0.303983 | 1.20058 | 0.0780003 | 0.874031 | 0.874031 |
| Healthcare Products | 642 | 0.0987843 | 0.161679 | 0.1569 | 0.24471 | 0.902901 | 0.973237 | 0.0915784 | 0.586948 | 0.0463 | 0.128015 | 0.084004 | 1.0652 | 3.51171 | 14.4909 | 21.0321 | 3.69558 | 60.7662 | 0.257351 | 0.0514453 | 0.122832 | 1.14369 | 0.114512 | 0.389608 | 0.389608 |
| Healthcare Support Services | 335 | 0.10582 | 0.0460448 | 0.288121 | 0.363648 | 0.949193 | 1.11155 | 0.101509 | 0.476972 | 0.0413 | 0.229294 | 0.0848625 | 7.48021 | 0.629384 | 10.2297 | 13.5198 | 2.48795 | 52.0804 | 0.00457798 | 0.0101726 | 0.0157781 | 0.763352 | 0.113806 | 0.250523 | 0.250523 |
| Heathcare Information and Technology | 285 | 0.127975 | 0.121273 | 0.155594 | 0.223438 | 1.00712 | 1.13673 | 0.103317 | 0.684291 | 0.0513 | 0.164877 | 0.0922031 | 1.38155 | 3.37584 | 16.4603 | 28.1269 | 3.93181 | 123.001 | 0.222324 | 0.0362963 | 0.19352 | 2.27787 | 0.096476 | 0.176033 | 0.176033 |
| Homebuilding | 160 | 0.0841713 | 0.0833663 | 0.0808355 | 0.276612 | 1.00772 | 1.33688 | 0.117688 | 0.513337 | 0.0463 | 0.365253 | 0.0865401 | 1.20726 | 1.18669 | 10.4041 | 13.8515 | 1.35863 | 35.8191 | 0.668922 | 0.00814763 | 0.0213585 | 1.37863 | 0.121663 | 0.196183 | 0.196183 |
| Hospitals/Healthcare Facilities | 199 | 0.112509 | 0.114674 | 0.0812522 | 0.197505 | 0.557544 | 0.83251 | 0.0814742 | 0.419237 | 0.0413 | 0.383419 | 0.0613201 | 0.829137 | 2.82759 | 13.2321 | 24.1351 | 2.88387 | 71.5832 | 0.132842 | 0.0594038 | 0.0757965 | 1.24551 | 0.122443 | 0.598401 | 0.598401 |
| Hotel/Gaming | 665 | 0.11489 | 0.122706 | 0.092782 | 0.170286 | 0.747612 | 0.937418 | 0.0890066 | 0.469827 | 0.0413 | 0.285956 | 0.0718216 | 0.873496 | 2.50099 | 11.736 | 19.9827 | 2.29044 | 50.5309 | -0.00802726 | 0.0701233 | 0.0475681 | 0.488456 | 0.0968485 | 0.536575 | 0.536575 |
| Household Products | 465 | 0.0899843 | 0.151107 | 0.235579 | 0.272102 | 0.909497 | 0.97826 | 0.091939 | 0.503859 | 0.0463 | 0.126965 | 0.0843809 | 1.82173 | 2.56458 | 13.2751 | 16.8424 | 4.26008 | 63.6539 | 0.101443 | 0.0409309 | 0.0550406 | 0.503715 | 0.175877 | 0.543309 | 0.543309 |
| Information Services | 185 | 0.0668225 | 0.217399 | 0.35828 | 0.296809 | 0.996183 | 1.06006 | 0.0978121 | 0.514468 | 0.0463 | 0.117052 | 0.0901566 | 1.97787 | 3.78315 | 13.721 | 17.3538 | 5.22517 | 35.1396 | 0.138506 | 0.0305472 | 0.0494895 | 0.371263 | 0.223585 | 0.258996 | 0.258996 |
| Insurance (General) | 233 | 0.133905 | 0.0933611 | 0.143161 | 0.273609 | 0.631557 | 0.715193 | 0.0730509 | 0.350491 | 0.0413 | 0.293046 | 0.0601155 | 1.81083 | 0.810556 | 7.09863 | 8.36761 | 1.07006 | 20.4537 | 0.0436543 | 0.00785776 | 0.012425 | 0.084764 | 0.107654 | 0.424061 | 0.424061 |
| Insurance (Life) | 124 | 0.147062 | 0.0910087 | 0.121278 | 0.245937 | 0.938214 | 1.03632 | 0.0961078 | 0.367528 | 0.0413 | 0.328526 | 0.0740316 | 1.65846 | 0.964111 | 9.81829 | 10.5804 | 1.35361 | 29.7291 | 0.0475099 | 0.00617819 | 0.00806682 | 0.0797968 | 0.109512 | 0.316974 | 0.316974 |
| Insurance (Prop/Cas.) | 220 | 0.11147 | 0.111316 | 0.124804 | 0.231129 | 0.523028 | 0.596428 | 0.0645235 | 0.373273 | 0.0413 | 0.239676 | 0.0559878 | 1.34993 | 1.01606 | 8.50636 | 9.04881 | 1.21997 | 16.128 | -0.256304 | 0.00652659 | 0.0133343 | 0.185567 | 0.106854 | 0.303498 | 0.303498 |
| Investments & Asset Management | 914 | 0.110916 | 0.227765 | 0.0821045 | 0.157601 | 0.651029 | 0.891924 | 0.0857402 | 0.47247 | 0.0413 | 0.384062 | 0.0639139 | 0.389024 | 4.69197 | 16.3264 | 17.9688 | 1.27425 | 131.394 | NA | 0.0202317 | -0.0304801 | -0.141501 | 0.122539 | 0.453118 | 0.453118 |
| Machinery | 1272 | 0.0728681 | 0.0971793 | 0.122665 | 0.271705 | 1.05648 | 1.12259 | 0.102302 | 0.48153 | 0.0413 | 0.173813 | 0.0895455 | 1.54653 | 1.49251 | 10.8304 | 15.0688 | 2.35451 | 54.5777 | 0.23455 | 0.0384273 | 0.0536377 | 0.962011 | 0.117739 | 0.36572 | 0.36572 |
| Metals & Mining | 1589 | 0.134713 | 0.12054 | 0.116725 | 0.310276 | 1.06544 | 1.43142 | 0.124476 | 0.793397 | 0.0513 | 0.318676 | 0.0962522 | 1.00709 | 1.37065 | 6.81207 | 11.1029 | 1.2805 | 65.7071 | 0.0988753 | 0.129556 | 0.0989241 | 1.34214 | 0.0799741 | 0.698513 | 0.698513 |
| Office Equipment & Services | 155 | 0.0404804 | 0.0787138 | 0.127303 | 0.310755 | 0.738873 | 0.914289 | 0.087346 | 0.480722 | 0.0413 | 0.304841 | 0.0695323 | 1.98765 | 1.11493 | 8.46845 | 13.9926 | 2.36414 | 203.752 | 0.129538 | 0.035423 | 0.0433491 | 0.910474 | 0.109662 | 0.375518 | 0.375518 |
| Oil/Gas (Integrated) | 55 | 0.1045 | 0.0923379 | 0.0999286 | 0.377284 | 1.17398 | 1.39573 | 0.121913 | 0.403312 | 0.0413 | 0.27352 | 0.0964749 | 1.45157 | 0.756639 | 4.60305 | 8.18763 | 1.03066 | 15.0086 | 0.0333305 | 0.113483 | 0.0609251 | 1.11938 | 0.114081 | 0.449407 | 0.449407 |
| Oil/Gas (Production and Exploration) | 1140 | 0.236363 | 0.234903 | 0.117209 | 0.349447 | 1.10152 | 1.48353 | 0.128218 | 0.739441 | 0.0513 | 0.319813 | 0.0986963 | 0.537607 | 2.42451 | 4.82518 | 10.0351 | 1.19637 | 52.2547 | -0.00333874 | 0.510458 | 0.34136 | 2.13097 | 0.0822876 | 0.528871 | 0.528871 |
| Oil/Gas Distribution | 215 | 0.151516 | 0.0769709 | 0.0838981 | 0.178867 | 0.847298 | 1.23191 | 0.110151 | 0.455495 | 0.0413 | 0.345756 | 0.0820613 | 1.20376 | 2.00582 | 15.6453 | 25.1159 | 2.11763 | 90.5207 | 0.0308803 | 0.14793 | 0.146006 | 2.27933 | 0.0915488 | 1.38992 | 1.38992 |
| Oilfield Svcs/Equip. | 586 | 0.130026 | 0.0413775 | 0.104804 | 0.273021 | 1.04785 | 1.38457 | 0.121112 | 0.56139 | 0.0463 | 0.334234 | 0.0914651 | 2.95946 | 0.54595 | 7.76318 | 13.0125 | 1.4528 | 607.037 | 0.0797995 | 0.0356941 | 0.030828 | 1.15348 | 0.0997313 | 0.402518 | 0.402518 |
| Packaging & Container | 398 | 0.0820377 | 0.0849863 | 0.117166 | 0.253617 | 0.605692 | 0.789633 | 0.0783957 | 0.447211 | 0.0413 | 0.315723 | 0.0627719 | 1.70375 | 1.20258 | 8.73668 | 14.0256 | 2.21051 | 36.7287 | 0.141037 | 0.0530404 | 0.0646884 | 1.04272 | 0.112004 | 0.447297 | 0.447297 |
| Paper/Forest Products | 303 | 0.0558082 | 0.063508 | 0.0561068 | 0.222395 | 0.616622 | 0.959463 | 0.0905894 | 0.470269 | 0.0413 | 0.429613 | 0.0640911 | 0.997497 | 1.19463 | 9.17945 | 18.3674 | 1.29023 | 66.5262 | 0.166916 | 0.0633496 | 0.0406121 | 0.886983 | 0.0452415 | 0.735383 | 0.735383 |
| Power | 574 | 0.1186 | 0.124635 | 0.0679912 | 0.24895 | 0.510592 | 0.870175 | 0.0841786 | 0.382126 | 0.0413 | 0.491926 | 0.0569906 | 0.663881 | 1.93787 | 8.65233 | 15.4859 | 1.29469 | 37.7938 | 0.0260367 | 0.15911 | 0.115514 | 1.30995 | 0.0815396 | 0.685167 | 0.685167 |
| Precious Metals | 1079 | 0.332547 | 0.0532176 | 0.0264229 | 0.419523 | 1.20626 | 1.48066 | 0.128011 | 0.958288 | 0.0613 | 0.262186 | 0.105699 | 0.510733 | 2.25901 | 7.63242 | 39.2227 | 1.07506 | 1831.07 | 0.139441 | 0.247953 | 0.133741 | 5.48815 | -0.0632497 | 0.00756874 | 0.00756874 |
| Publshing & Newspapers | 373 | 0.00674337 | 0.0846782 | 0.107067 | 0.181825 | 0.864811 | 1.02093 | 0.0950027 | 0.520422 | 0.0463 | 0.247192 | 0.0795303 | 1.49408 | 1.63315 | 9.61423 | 16.8791 | 1.92697 | 37.6378 | 0.0834235 | 0.0340576 | 0.0450625 | 0.735169 | 0.133967 | 0.377889 | 0.377889 |
| R.E.I.T. | 482 | 0.134659 | 0.295313 | 0.0331599 | 0.0262758 | 0.449971 | 0.785897 | 0.0781274 | 0.2985 | 0.0413 | 0.444923 | 0.0562295 | 0.114906 | 12.6161 | 22.7971 | 37.39 | 1.68656 | 32.3977 | 0.347978 | 0.0880099 | 0.101034 | 0.453118 | 0.104822 | 0.699493 | 0.699493 |
| Real Estate (Development) | 703 | 0.157762 | 0.215671 | 0.0913792 | 0.301138 | 0.784975 | 1.16247 | 0.105165 | 0.485299 | 0.0413 | 0.474246 | 0.0690016 | 0.518803 | 2.68793 | 11.3768 | 12.084 | 0.995376 | 49.7606 | 1.64649 | 0.04016 | 0.0674739 | 1.85091 | 0.142748 | 0.378569 | 0.378569 |
| Real Estate (General/Diversified) | 449 | 0.094683 | 0.198541 | 0.0488525 | 0.191681 | 0.703452 | 1.07664 | 0.0990029 | 0.494993 | 0.0413 | 0.441142 | 0.068082 | 0.291793 | 3.91643 | 14.4075 | 19.0707 | 0.923312 | 76.8312 | 0.78646 | 0.0664469 | 0.0688066 | 0.854112 | 0.0893667 | 0.269402 | 0.269402 |
| Real Estate (Operations & Services) | 577 | 0.101918 | 0.306821 | 0.0522816 | 0.194059 | 0.548192 | 0.919083 | 0.0876901 | 0.438566 | 0.0413 | 0.472463 | 0.0599187 | 0.196417 | 6.25774 | 15.876 | 18.7893 | 0.978599 | 35.0192 | 0.203465 | 0.0730484 | 0.0964586 | 0.46254 | 0.0800202 | 0.400975 | 0.400975 |
| Recreation | 293 | 0.0414327 | 0.108199 | 0.0982452 | 0.26922 | 0.945121 | 1.06553 | 0.0982054 | 0.491014 | 0.0413 | 0.216292 | 0.0832173 | 1.09332 | 1.96926 | 10.7075 | 17.4061 | 2.57213 | 56.7164 | 0.17619 | 0.0556277 | 0.0521754 | 0.734068 | 0.118084 | 0.420725 | 0.420725 |
| Reinsurance | 40 | 0.140811 | 0.124971 | 0.149947 | 0.114989 | 1.06973 | 1.20602 | 0.108292 | 0.283445 | 0.0413 | 0.248704 | 0.0885497 | 1.33871 | 0.813877 | 6.51532 | 6.45597 | 0.909262 | 11.1353 | -0.419829 | 0.00144974 | 0.00235022 | 0.014912 | 0.136602 | 0.27392 | 0.27392 |
| Restaurant/Dining | 306 | 0.0671471 | 0.0965202 | 0.120072 | 0.313185 | 0.697258 | 0.841487 | 0.0821187 | 0.411476 | 0.0413 | 0.246106 | 0.0690238 | 1.58265 | 2.1136 | 11.4794 | 21.2876 | 5.18666 | 44.7485 | -0.0117164 | 0.0552202 | 0.0412257 | 0.611772 | 0.195509 | 0.501455 | 0.501455 |
| Retail (Automotive) | 149 | 0.0964158 | 0.042958 | 0.0998956 | 0.329798 | 0.720365 | 0.958571 | 0.0905254 | 0.439229 | 0.0413 | 0.337433 | 0.0697343 | 2.98289 | 0.812992 | 11.715 | 18.7365 | 3.56564 | 88.651 | 0.0836352 | 0.0264646 | 0.0373033 | 1.34052 | 0.193555 | 0.231893 | 0.231893 |
| Retail (Building Supply) | 50 | 0.0798681 | 0.0809947 | 0.117132 | 0.35684 | 0.896952 | 1.02666 | 0.0954143 | 0.356387 | 0.0413 | 0.204321 | 0.0818261 | 2.07502 | 1.40756 | 11.0411 | 17.3704 | 4.8382 | 30.5485 | 0.0725518 | 0.0202834 | 0.00323282 | 0.0379219 | 0.194115 | 0.378566 | 0.378566 |
| Retail (Distributors) | 889 | 0.0941763 | 0.0378402 | 0.0617557 | 0.276033 | 0.584865 | 0.929304 | 0.088424 | 0.493493 | 0.0413 | 0.484567 | 0.0595855 | 2.02265 | 0.671356 | 11.523 | 17.3226 | 1.27083 | 218.459 | 0.141083 | 0.0275837 | 0.0312098 | 1.51252 | 0.0961043 | 0.364468 | 0.364468 |
| Retail (General) | 231 | 0.0881867 | 0.0416655 | 0.0900686 | 0.326182 | 0.730705 | 0.928394 | 0.0883587 | 0.401389 | 0.0413 | 0.308201 | 0.0700366 | 2.81178 | 0.756211 | 9.2961 | 17.8818 | 2.3168 | 31.218 | 0.0092666 | 0.0311302 | 0.0252987 | 0.99217 | 0.125158 | 0.406217 | 0.406217 |
| Retail (Grocery and Food) | 180 | 0.102359 | 0.0315112 | 0.0729955 | 0.28842 | 0.598829 | 0.845903 | 0.0824358 | 0.364127 | 0.0413 | 0.408219 | 0.0605855 | 3.05853 | 0.612093 | 8.04521 | 19.3797 | 1.81312 | 33.0262 | -0.0352563 | 0.0312602 | 0.0441339 | 1.73084 | 0.10177 | 0.592272 | 0.592272 |
| Retail (Online) | 115 | 0.193361 | 0.0433866 | 0.17099 | 0.262942 | 1.40487 | 1.41654 | 0.123408 | 0.720325 | 0.0513 | 0.0844436 | 0.116019 | 4.44494 | 2.18565 | 23.7211 | 52.0846 | 7.47245 | 73.1524 | 0.00209985 | 0.0438327 | 0.0711932 | 2.45729 | 0.11517 | 0.21123 | 0.21123 |
| Retail (Special Lines) | 540 | 0.0568744 | 0.0628791 | 0.111346 | 0.326744 | 0.871478 | 1.03103 | 0.0957279 | 0.471692 | 0.0413 | 0.245935 | 0.079295 | 2.27011 | 1.22341 | 9.90455 | 19.2071 | 3.44755 | 28.6823 | 0.097544 | 0.0240809 | 0.0269307 | 0.845514 | 0.140462 | 0.36009 | 0.36009 |
| Rubber& Tires | 89 | 0.0887207 | 0.109572 | 0.124435 | 0.322958 | 0.933726 | 1.1309 | 0.102899 | 0.437897 | 0.0413 | 0.283887 | 0.0818942 | 1.45644 | 0.956277 | 5.83781 | 8.65391 | 1.65665 | 19.6238 | 0.195772 | 0.0497789 | 0.0447278 | 0.581192 | 0.145533 | 0.296553 | 0.296553 |
| Semiconductor | 564 | 0.082748 | 0.175629 | 0.126529 | 0.178503 | 1.23497 | 1.27173 | 0.11301 | 0.532741 | 0.0463 | 0.114679 | 0.103767 | 0.80071 | 2.80973 | 9.47562 | 16.2114 | 2.95761 | 49.998 | 0.180174 | 0.135847 | 0.167501 | 1.30501 | 0.149574 | 0.368558 | 0.368558 |
| Semiconductor Equip | 259 | 0.125955 | 0.109501 | 0.0853659 | 0.182432 | 1.35337 | 1.40421 | 0.122522 | 0.577085 | 0.0463 | 0.13466 | 0.110388 | 0.867312 | 2.69689 | 13.8039 | 23.0078 | 2.74515 | 41.7661 | 0.273031 | 0.0756276 | 0.092364 | 1.3495 | 0.0544094 | 0.504263 | 0.504263 |
| Shipbuilding & Marine | 354 | 0.031758 | 0.0779621 | 0.0464594 | 0.264391 | 0.825865 | 1.25692 | 0.111947 | 0.494903 | 0.0413 | 0.440991 | 0.0753282 | 0.684054 | 1.76261 | 9.49796 | 22.06 | 1.21862 | 45.152 | 0.000305187 | 0.123382 | 0.09288 | 1.74254 | 0.0654207 | 0.54649 | 0.54649 |
| Shoe | 95 | 0.0965815 | 0.097961 | 0.147141 | 0.236602 | 0.838297 | 0.861209 | 0.0835348 | 0.49819 | 0.0413 | 0.10524 | 0.0777861 | 1.87336 | 1.79323 | 12.9949 | 18.2365 | 3.35441 | 25.5168 | 0.206882 | 0.0171058 | 0.0167753 | 0.389195 | 0.157751 | 0.43866 | 0.43866 |
| Software (Entertainment) | 119 | 0.00738617 | 0.126245 | 0.0981828 | 0.305397 | 1.3458 | 1.1906 | 0.107185 | 0.687381 | 0.0513 | 0.0948116 | 0.100427 | 0.877367 | 2.39995 | 10.2539 | 15.4388 | 2.08905 | 52.5368 | 0.178788 | 0.0337148 | 0.0480167 | 0.354138 | 0.0830371 | 0.184656 | 0.184656 |
| Software (Internet) | 759 | 0.10798 | 0.204125 | 0.171402 | 0.328129 | 1.35309 | 1.33672 | 0.117676 | 0.687597 | 0.0513 | 0.0522728 | 0.113402 | 0.909086 | 6.17856 | 20.7321 | 31.8551 | 4.55005 | 145.129 | 0.0758659 | 0.099539 | 0.167039 | 1.41825 | 0.147807 | 0.0721804 | 0.0721804 |
| Software (System & Application) | 991 | 0.095306 | 0.237996 | 0.219655 | 0.230376 | 1.0994 | 1.12348 | 0.102366 | 0.623364 | 0.0463 | 0.0813506 | 0.0966746 | 1.03492 | 4.48933 | 14.2409 | 18.2673 | 4.40809 | 69.2625 | 0.129817 | 0.0401794 | 0.113022 | 0.712411 | 0.177269 | 0.379137 | 0.379137 |
| Steel | 757 | 0.0582386 | 0.048329 | 0.0521759 | 0.29212 | 0.793604 | 1.27785 | 0.113449 | 0.542269 | 0.0463 | 0.4734 | 0.0750854 | 1.24786 | 0.783278 | 7.46749 | 15.3634 | 0.944107 | 47.4457 | 0.130629 | 0.0568258 | 0.0583163 | 1.79951 | 0.00645269 | 5.1988 | 5.1988 |
| Telecom (Wireless) | 117 | 0.0908704 | 0.134971 | 0.0968719 | 0.294522 | 0.875855 | 1.1669 | 0.105483 | 0.475704 | 0.0413 | 0.327879 | 0.0803766 | 0.826888 | 2.00392 | 6.41565 | 14.7061 | 1.7389 | 24.4559 | -0.0697678 | 0.178381 | 0.0904716 | 1.02912 | 0.23024 | 0.280971 | 0.280971 |
| Telecom. Equipment | 484 | 0.0584815 | 0.12383 | 0.115245 | 0.199206 | 1.14962 | 1.17578 | 0.106121 | 0.573845 | 0.0463 | 0.117201 | 0.0974819 | 1.04595 | 2.19535 | 12.0758 | 16.615 | 2.73195 | 107.832 | 0.17127 | 0.031369 | 0.0411448 | 0.435688 | 0.137215 | 0.409484 | 0.409484 |
| Telecom. Services | 308 | 0.0552862 | 0.160721 | 0.136396 | 0.277013 | 0.692309 | 1.01256 | 0.0944015 | 0.505018 | 0.0463 | 0.386332 | 0.0704522 | 0.992531 | 2.0194 | 5.9121 | 12.4506 | 1.94759 | 29.5348 | -0.0065209 | 0.135488 | 0.00827576 | 0.0949356 | 0.149125 | 0.61307 | 0.61307 |
| Tobacco | 61 | 0.0838436 | 0.286076 | 0.52266 | 0.292395 | 0.687881 | 0.765038 | 0.0766297 | 0.390278 | 0.0413 | 0.144339 | 0.0697419 | 2.23637 | 3.6799 | 11.5946 | 12.8479 | 10.8048 | 25.4105 | 0.169023 | 0.032602 | 0.0202354 | 0.113946 | 0.596424 | 0.709462 | 0.709462 |
| Transportation | 225 | 0.104522 | 0.0865492 | 0.115701 | 0.300446 | 0.695191 | 0.879656 | 0.0848593 | 0.428117 | 0.0413 | 0.318883 | 0.067018 | 1.69474 | 1.32253 | 9.30908 | 15.2017 | 2.36457 | 29.7814 | 0.0336771 | 0.0414979 | 0.0177944 | 0.513313 | 0.138855 | 0.52246 | 0.52246 |
| Transportation (Railroads) | 53 | 0.0504532 | 0.213645 | 0.0887794 | 0.313609 | 0.80864 | 1.00104 | 0.093575 | 0.322689 | 0.0413 | 0.262363 | 0.0766093 | 0.556278 | 3.28508 | 10.3197 | 15.4671 | 2.51956 | 25.9485 | -0.000398297 | 0.157564 | 0.120204 | 0.817373 | 0.138325 | 0.28437 | 0.28437 |
| Trucking | 190 | 0.0541939 | 0.0760746 | 0.0919475 | 0.337015 | 0.681226 | 0.956211 | 0.0903559 | 0.419979 | 0.0413 | 0.385731 | 0.0666543 | 1.55932 | 1.15371 | 8.21316 | 14.9437 | 2.32847 | 29.5598 | 0.0480454 | 0.0968955 | 0.0813275 | 1.67498 | 0.105067 | 0.26027 | 0.26027 |
| Unclassified | 33 | 0.07555 | 0.193846 | 0.0637732 | 0.0874674 | 0.610217 | 0.859246 | 0.0833939 | 0.580541 | 0.0463 | 0.362409 | 0.0649169 | 0.358221 | 6.88706 | 14.4081 | 22.9161 | 2.36493 | 89.4766 | -1.18423 | 0.103568 | 0.161009 | 0.910884 | -0.0714694 | 0.000454282 | 0.000454282 |
| Utility (General) | 56 | 0.0199932 | 0.0993881 | 0.0744379 | 0.326909 | 0.511731 | 0.797539 | 0.0789633 | 0.320845 | 0.0413 | 0.4572 | 0.0560789 | 0.990997 | 1.40684 | 8.28529 | 14.1354 | 1.44667 | 28.9877 | 0.00861582 | 0.113725 | 0.0616779 | 0.873517 | 0.0202133 | 3.57989 | 3.57989 |
| Utility (Water) | 98 | 0.129835 | 0.262179 | 0.0918754 | 0.200494 | 0.729442 | 0.9755 | 0.0917409 | 0.42617 | 0.0413 | 0.328913 | 0.071075 | 0.414124 | 4.95497 | 12.8264 | 18.5989 | 2.15276 | 51.536 | 0.062477 | 0.190093 | 0.137323 | 0.72553 | 0.136861 | 0.55951 | 0.55951 |
| Total Market | 42410 | 0.0993905 | 0.0905192 | 0.059291 | 0.26091 | 0.705381 | 1.07221 | 0.0986848 | 0.514723 | 0.0463 | 0.44237 | 0.0693668 | 0.761858 | 2.00008 | 12.5447 | 20.2424 | 1.77752 | 90.5999 | -0.939891 | 0.0659718 | 0.0564714 | 0.972319 | 0.114236 | 0.544063 | 0.544063 |

#### Reference data — Country risk and taxes (lookup key for country ERP, default spread, marginal tax rate, CRP)

Columns: Country | Country Default Spread | ERP | Marginal tax rate | CRP.

| Country | Country Default Spread | ERP | Marginal tax rate | CRP |
|---|---|---|---|---|
| Abu Dhabi | 0.005 | 0.065 | 0.55 | 0.0075 |
| Albania | 0.045 | 0.125 | 0.15 | 0.0675 |
| Andorra | 0.0075 | 0.0688 | 0.19 | 0.0113 |
| Angola | 0.03 | 0.1025 | 0.35 | 0.045 |
| Anguilla | 0.0575 | 0.1437 | 0.1667 | 0.0862 |
| Argentina | 0.075 | 0.17 | 0.35 | 0.1125 |
| Armenia | 0.03 | 0.1025 | 0.2 | 0.045 |
| Aruba | 0.065 | 0.155 | 0.28 | 0.0975 |
| Australia | 0 | 0.0575 | 0.3 | 0 |
| Austria | 0 | 0.0575 | 0.25 | 0 |
| Azerbaijan | 0.022 | 0.0905 | 0.25 | 0.033 |
| Bahamas | 0.019 | 0.086 | 0 | 0.0285 |
| Bahrain | 0.019 | 0.086 | 0 | 0.0285 |
| Bangladesh | 0.036 | 0.1115 | 0.275 | 0.054 |
| Barbados | 0.065 | 0.155 | 0.25 | 0.0975 |
| Belarus | 0.065 | 0.155 | 0.18 | 0.0975 |
| Belgium | 0.006 | 0.0665 | 0.3399 | 0.009 |
| Belize | 0.09 | 0.1925 | 0.3399 | 0.135 |
| Benin | 0.0399 | 0.1173 | 0.2785 | 0.0598 |
| Bermuda | 0.007 | 0.068 | 0 | 0.0105 |
| Bolivia | 0.036 | 0.1115 | 0.25 | 0.054 |
| Bosnia and Herzegovina | 0.065 | 0.155 | 0.1 | 0.0975 |
| Botswana | 0.0085 | 0.0703 | 0.22 | 0.01275 |
| Brazil | 0.019 | 0.086 | 0.25 | 0.0285 |
| British Virgin Islands | 0.0575 | 0.1437 | 0.1667 | 0.0862 |
| Bulgaria | 0.019 | 0.086 | 0.1 | 0.0285 |
| Burkina Faso | 0.065 | 0.155 | 0.1 | 0.0975 |
| Cambodia | 0.055 | 0.14 | 0.2 | 0.0825 |
| Cameroon | 0.055 | 0.14 | 0.2 | 0.0825 |
| Canada | 0 | 0.0575 | 0.265 | 0 |
| Cape Verde | 0.055 | 0.14 | 0.265 | 0.0825 |
| Cayman Islands | 0.055 | 0.14 | 0 | 0.0825 |
| Channel Islands | 0.0075 | 0.0688 | 0 | 0.0113 |
| Chile | 0.006 | 0.0665 | 0.2 | 0.009 |
| China | 0.006 | 0.0665 | 0.25 | 0.009 |
| Colombia | 0.019 | 0.086 | 0.25 | 0.0285 |
| Congo (Democratic Republic of) | 0.065 | 0.155 | 0.2785 | 0.0975 |
| Congo (Republic of) | 0.036 | 0.1115 | 0.2785 | 0.054 |
| Cook Islands | 0.045 | 0.125 | 0.25 | 0.0675 |
| Costa Rica | 0.025 | 0.095 | 0.3 | 0.0375 |
| Croatia | 0.025 | 0.095 | 0.2 | 0.0375 |
| Cuba | 0.09 | 0.1925 | 0.2 | 0.135 |
| Curaçao | 0.0575 | 0.1437 | 0.275 | 0.0862 |
| Cyprus | 0.065 | 0.155 | 0.125 | 0.0975 |
| Czech Republic | 0.007 | 0.068 | 0.19 | 0.0105 |
| Denmark | 0 | 0.0575 | 0.245 | 0 |
| Dominican Republic | 0.045 | 0.125 | 0.28 | 0.0675 |
| Ecuador | 0.065 | 0.155 | 0.22 | 0.0975 |
| Egypt | 0.075 | 0.17 | 0.25 | 0.1125 |
| El Salvador | 0.036 | 0.1115 | 0.3 | 0.054 |
| Estonia | 0.007 | 0.068 | 0.21 | 0.0105 |
| Falkland Islands | 0.028 | 0.0995 | 0 | 0.042 |
| Fiji | 0.045 | 0.125 | 0.2 | 0.0675 |
| Finland | 0 | 0.0575 | 0.2 | 0 |
| France | 0.004 | 0.0635 | 0.3333 | 0.006 |
| Gabon | 0.036 | 0.1115 | 0.3333 | 0.054 |
| Georgia | 0.036 | 0.1115 | 0.15 | 0.054 |
| Germany | 0 | 0.0575 | 0.2958 | 0 |
| Ghana | 0.055 | 0.14 | 0.25 | 0.0825 |
| Gibraltar | 0.0075 | 0.0688 | 0.1 | 0.0113 |
| Greece | 0.075 | 0.17 | 0.26 | 0.1125 |
| Greenland | 0.0075 | 0.0688 | 0.26 | 0.0113 |
| Guatemala | 0.025 | 0.095 | 0.28 | 0.0375 |
| Honduras | 0.065 | 0.155 | 0.3 | 0.0975 |
| Hong Kong | 0.004 | 0.0635 | 0.3 | 0.006 |
| Hungary | 0.025 | 0.095 | 0.19 | 0.0375 |
| Iceland | 0.022 | 0.0905 | 0.2 | 0.033 |
| India | 0.022 | 0.0905 | 0.3399 | 0.033 |
| Indonesia | 0.022 | 0.0905 | 0.25 | 0.033 |
| Ireland | 0.016 | 0.0815 | 0.125 | 0.024 |
| Isle of Man | 0.004 | 0.0635 | 0 | 0.006 |
| Israel | 0.007 | 0.068 | 0.265 | 0.0105 |
| Italy | 0.019 | 0.086 | 0.314 | 0.0285 |
| Ivory Coast | 0.045 | 0.125 | 0.2785 | 0.0675 |
| Jamaica | 0.1 | 0.2075 | 0.25 | 0.15 |
| Japan | 0.007 | 0.068 | 0.3564 | 0.0105 |
| Jordan | 0.045 | 0.125 | 0.14 | 0.0675 |
| Kazakhstan | 0.019 | 0.086 | 0.2 | 0.0285 |
| Kenya | 0.045 | 0.125 | 0.3 | 0.0675 |
| Korea | 0.006 | 0.0665 | 0.3 | 0.009 |
| Kuwait | 0.005 | 0.065 | 0.15 | 0.0075 |
| Kyrgyzstan | 0.0222 | 0.0908 | 0.2 | 0.0333 |
| Laos | 0.0101 | 0.0726 | 0.2191 | 0.0151 |
| Latvia | 0.016 | 0.0815 | 0.15 | 0.024 |
| Lebanon | 0.055 | 0.14 | 0.15 | 0.0825 |
| Liechtenstein | 0 | 0.0575 | 0.125 | 0 |
| Lithuania | 0.016 | 0.0815 | 0.15 | 0.024 |
| Luxembourg | 0 | 0.0575 | 0.2922 | 0 |
| Macau | 0.005 | 0.065 | 0.12 | 0.0075 |
| Macedonia | 0.036 | 0.1115 | 0.1 | 0.054 |
| Malawi | 0.0399 | 0.1173 | 0.3 | 0.0598 |
| Malaysia | 0.012 | 0.0755 | 0.25 | 0.018 |
| Malta | 0.012 | 0.0755 | 0.35 | 0.018 |
| Marshall Islands | 0.0101 | 0.0726 | 0 | 0.0151 |
| Mauritius | 0.016 | 0.0815 | 0.15 | 0.024 |
| Mexico | 0.012 | 0.0755 | 0.3 | 0.018 |
| Moldova | 0.065 | 0.155 | 0.25 | 0.0975 |
| Monaco | 0 | 0.0575 | 0.3 | 0 |
| Mongolia | 0.055 | 0.14 | 0.3 | 0.0825 |
| Montenegro | 0.036 | 0.1115 | 0.09 | 0.054 |
| Montserrat | 0.022 | 0.0905 | 0.2 | 0.033 |
| Morocco | 0.025 | 0.095 | 0.3 | 0.0375 |
| Mozambique | 0.045 | 0.125 | 0.32 | 0.0675 |
| Namibia | 0.022 | 0.0905 | 0.33 | 0.033 |
| Netherlands | 0 | 0.0575 | 0.25 | 0 |
| Netherlands Antilles | 0 | 0.0575 | 0.2 | 0 |
| New Zealand | 0 | 0.0575 | 0.28 | 0 |
| Nicaragua | 0.065 | 0.155 | 0.2715 | 0.0975 |
| Niger | 0.0399 | 0.1173 | 0.2785 | 0.0598 |
| Nigeria | 0.036 | 0.1115 | 0.3 | 0.054 |
| Norway | 0 | 0.0575 | 0.27 | 0 |
| Oman | 0.007 | 0.068 | 0.12 | 0.0105 |
| Pakistan | 0.075 | 0.17 | 0.34 | 0.1125 |
| Palestinian Authority | 0.075 | 0.17 | 0.2 | 0.1125 |
| Panama | 0.019 | 0.086 | 0.25 | 0.0285 |
| Papua New Guinea | 0.045 | 0.125 | 0.3 | 0.0675 |
| Paraguay | 0.03 | 0.1025 | 0.1 | 0.045 |
| Peru | 0.012 | 0.0755 | 0.3 | 0.018 |
| Philippines | 0.019 | 0.086 | 0.3 | 0.0285 |
| Poland | 0.0085 | 0.0703 | 0.19 | 0.01275 |
| Portugal | 0.025 | 0.095 | 0.23 | 0.0375 |
| Qatar | 0.005 | 0.065 | 0.1 | 0.0075 |
| Reunion | 0 | 0.0575 | 0 | 0 |
| Romania | 0.022 | 0.0905 | 0.16 | 0.033 |
| Russia | 0.019 | 0.086 | 0.2 | 0.0285 |
| Rwanda | 0.055 | 0.14 | 0.2785 | 0.0825 |
| Samoa | 0.055 | 0.14 | 0.27 | 0.0825 |
| Saudi Arabia | 0.006 | 0.0665 | 0.2 | 0.009 |
| Senegal | 0.045 | 0.125 | 0.2785 | 0.0675 |
| Serbia | 0.045 | 0.125 | 0.15 | 0.0675 |
| Sierra Leone | 0.0399 | 0.1173 | 0.3 | 0.0598 |
| Singapore | 0 | 0.0575 | 0.17 | 0 |
| Slovakia | 0.0085 | 0.0703 | 0.22 | 0.01275 |
| Slovenia | 0.025 | 0.095 | 0.17 | 0.0375 |
| South Africa | 0.019 | 0.086 | 0.28 | 0.0285 |
| Spain | 0.019 | 0.086 | 0.3 | 0.0285 |
| Sri Lanka | 0.045 | 0.125 | 0.28 | 0.0675 |
| St. Maarten | 0.016 | 0.0815 | 0.2 | 0.024 |
| St. Vincent & the Grenadines | 0.065 | 0.155 | 0.2 | 0.0975 |
| Sudan | 0.0399 | 0.1173 | 0.35 | 0.0598 |
| Suriname | 0.036 | 0.1115 | 0.345 | 0.054 |
| Sweden | 0 | 0.0575 | 0.22 | 0 |
| Switzerland | 0 | 0.0575 | 0.1792 | 0 |
| Taiwan | 0.006 | 0.0665 | 0.17 | 0.009 |
| Tanzania | 0.0399 | 0.1173 | 0.3 | 0.0598 |
| Thailand | 0.016 | 0.0815 | 0.2 | 0.024 |
| Togo | 0.0399 | 0.1173 | 0.2785 | 0.0598 |
| Trinidad & Tobago | 0.016 | 0.0815 | 0.25 | 0.024 |
| Tunisia | 0.036 | 0.1115 | 0.25 | 0.054 |
| Turkey | 0.022 | 0.0905 | 0.2 | 0.033 |
| Turks & Caicos Islands | 0.022 | 0.0905 | 0.2 | 0.033 |
| Uganda | 0.045 | 0.125 | 0.3 | 0.0675 |
| Ukraine | 0.1 | 0.2075 | 0.18 | 0.15 |
| United Arab Emirates | 0.005 | 0.065 | 0.55 | 0.0075 |
| United Kingdom | 0.004 | 0.0635 | 0.21 | 0.006 |
| United States | 0 | 0.0575 | 0.4 | 0 |
| Uruguay | 0.019 | 0.086 | 0.25 | 0.0285 |
| Venezuela | 0.075 | 0.17 | 0.34 | 0.1125 |
| Vietnam | 0.045 | 0.125 | 0.22 | 0.0675 |
| Zambia | 0.045 | 0.125 | 0.35 | 0.0675 |
| Zimbabwe | 0.0399 | 0.1173 | 0.2785 | 0.0598 |

Regional block at the bottom of the same sheet (rows 165–175; used by the Operating Regions ERP calculator):

| Region | Default Spread | ERP | Tax Rate |
|---|---|---|---|
| Africa | 0.0399 | 0.1173 | 0.2785 |
| Asia | 0.0101 | 0.0726 | 0.2191 |
| Australia & New Zealand | 0 | 0.0575 | 0.26 |
| Caribbean | 0.0575 | 0.1437 | 0.1492 |
| Central and South America | 0.028 | 0.0995 | 0.2715 |
| Eastern Europe & Russia | 0.0222 | 0.0908 | 0.1638 |
| Middle East | 0.0073 | 0.0685 | 0.1922 |
| North America | 0 | 0.0575 | 0.3325 |
| Western Europe | 0.0075 | 0.0688 | 0.1968 |
| Global | 0.0143 | 0.0718 | 0.2357 |

#### Reference data — Country equity risk premiums (GDP weights and region mapping)

Columns: Country | GDP (in billions) | Adj. Default Spread | Total Risk Premium | Country Risk Premium | Region. (Total Risk Premium = mature-market ERP 0.0575 + Country Risk Premium.)

| Country | GDP (in billions) | Adj. Default Spread | Total Risk Premium | Country Risk Premium | Region |
|---|---|---|---|---|---|
| Abu Dhabi | 390 | 0.005 | 0.065 | 0.0075 | Middle East |
| Albania | 12.9 | 0.045 | 0.125 | 0.0675 | Eastern Europe & Russia |
| Andorra (Principality of) | 4.5 | 0.016 | 0.0815 | 0.024 | Western Europe |
| Angola | 124.2 | 0.03 | 0.1025 | 0.045 | Africa |
| Argentina | 609.9 | 0.075 | 0.17 | 0.1125 | Central and South America |
| Armenia | 10.4 | 0.03 | 0.1025 | 0.045 | Eastern Europe & Russia |
| Aruba | 2.6 | 0.065 | 0.155 | 0.0975 | Caribbean |
| Australia | 1560.4 | 0 | 0.0575 | 0 | Australia & New Zealand |
| Austria | 428.3 | 0 | 0.0575 | 0 | Western Europe |
| Azerbaijan | 73.4 | 0.022 | 0.0905 | 0.033 | Eastern Europe & Russia |
| Bahamas | 8.4 | 0.019 | 0.086 | 0.0285 | Caribbean |
| Bahrain | 32.9 | 0.019 | 0.086 | 0.0285 | Middle East |
| Bangladesh | 150 | 0.036 | 0.1115 | 0.054 | Asia |
| Barbados | 3.7 | 0.065 | 0.155 | 0.0975 | Caribbean |
| Belarus | 71.7 | 0.065 | 0.155 | 0.0975 | Eastern Europe & Russia |
| Belgium | 524.8 | 0.006 | 0.0665 | 0.009 | Western Europe |
| Belize | 1.6 | 0.09 | 0.1925 | 0.135 | Central and South America |
| Bermuda | 5.557 | 0.007 | 0.068 | 0.0105 | Caribbean |
| Bolivia | 30.6 | 0.036 | 0.1115 | 0.054 | Central and South America |
| Bosnia and Herzegovina | 17.9 | 0.065 | 0.155 | 0.0975 | Eastern Europe & Russia |
| Botswana | 14.8 | 0.0085 | 0.0703 | 0.0128 | Africa |
| Brazil | 2245.7 | 0.019 | 0.086 | 0.0285 | Central and South America |
| Bulgaria | 54.5 | 0.019 | 0.086 | 0.0285 | Eastern Europe & Russia |
| Burkina Faso | 11.6 | 0.065 | 0.155 | 0.0975 | Africa |
| Cambodia | 15.2 | 0.055 | 0.14 | 0.0825 | Asia |
| Cameroon | 29.6 | 0.055 | 0.14 | 0.0825 | Africa |
| Canada | 1826.8 | 0 | 0.0575 | 0 | North America |
| Cayman Islands | 1.897 | 0.006 | 0.0665 | 0.009 | Caribbean |
| Cape Verde | 4 | 0.055 | 0.14 | 0.0825 | Africa |
| Chile | 277.2 | 0.006 | 0.0665 | 0.009 | Central and South America |
| China | 9240.3 | 0.006 | 0.0665 | 0.009 | Asia |
| Colombia | 378.4 | 0.019 | 0.086 | 0.0285 | Central and South America |
| Congo (Democratic Republic of) | 32.7 | 0.065 | 0.155 | 0.0975 | Africa |
| Congo (Republic of) | 14.1 | 0.036 | 0.1115 | 0.054 | Africa |
| Cook Islands | 1.2 | 0.045 | 0.125 | 0.0675 | Australia & New Zealand |
| Costa Rica | 49.6 | 0.025 | 0.095 | 0.0375 | Central and South America |
| Côte d'Ivoire | 31.1 | 0.045 | 0.125 | 0.0675 | Africa |
| Croatia | 57.9 | 0.025 | 0.095 | 0.0375 | Eastern Europe & Russia |
| Cuba | 60.8 | 0.09 | 0.1925 | 0.135 | Caribbean |
| Curacao | 1 | 0.012 | 0.0755 | 0.018 | Caribbean |
| Cyprus | 21.9 | 0.065 | 0.155 | 0.0975 | Western Europe |
| Czech Republic | 208.9 | 0.007 | 0.068 | 0.0105 | Eastern Europe & Russia |
| Denmark | 335.9 | 0 | 0.0575 | 0 | Western Europe |
| Dominican Republic | 61.2 | 0.045 | 0.125 | 0.0675 | Caribbean |
| Ecuador | 94.5 | 0.065 | 0.155 | 0.0975 | Central and South America |
| Egypt | 272 | 0.075 | 0.17 | 0.1125 | Africa |
| El Salvador | 24.3 | 0.036 | 0.1115 | 0.054 | Central and South America |
| Estonia | 24.9 | 0.007 | 0.068 | 0.0105 | Eastern Europe & Russia |
| Ethiopia | 47.5 | 0.045 | 0.125 | 0.0675 | Africa |
| Fiji | 3.9 | 0.045 | 0.125 | 0.0675 | Asia |
| Finland | 267.3 | 0 | 0.0575 | 0 | Western Europe |
| France | 2806.4 | 0.004 | 0.0635 | 0.006 | Western Europe |
| Gabon | 19.3 | 0.036 | 0.1115 | 0.054 | Africa |
| Georgia | 16.1 | 0.036 | 0.1115 | 0.054 | Eastern Europe & Russia |
| Germany | 3730.3 | 0 | 0.0575 | 0 | Western Europe |
| Ghana | 48.1 | 0.055 | 0.14 | 0.0825 | Africa |
| Greece | 242.2 | 0.075 | 0.17 | 0.1125 | Western Europe |
| Guatemala | 53.8 | 0.025 | 0.095 | 0.0375 | Central and South America |
| Guernsey (States of) | 0.5 | 0.004 | 0.0635 | 0.006 | Western Europe |
| Honduras | 18.6 | 0.065 | 0.155 | 0.0975 | Central and South America |
| Hong Kong | 274 | 0.004 | 0.0635 | 0.006 | Asia |
| Hungary | 133.4 | 0.025 | 0.095 | 0.0375 | Eastern Europe & Russia |
| Iceland | 15.3 | 0.022 | 0.0905 | 0.033 | Western Europe |
| India | 1876.8 | 0.022 | 0.0905 | 0.033 | Asia |
| Indonesia | 868.4 | 0.022 | 0.0905 | 0.033 | Asia |
| Ireland | 232.1 | 0.016 | 0.0815 | 0.024 | Western Europe |
| Isle of Man | 1.4 | 0.004 | 0.0635 | 0.006 | Western Europe |
| Israel | 290.6 | 0.007 | 0.068 | 0.0105 | Middle East |
| Italy | 2149.5 | 0.019 | 0.086 | 0.0285 | Western Europe |
| Jamaica | 14.4 | 0.1 | 0.2075 | 0.15 | Caribbean |
| Japan | 4919.6 | 0.007 | 0.068 | 0.0105 | Asia |
| Jersey (States of) | 1 | 0.004 | 0.0635 | 0.006 | Western Europe |
| Jordan | 33.7 | 0.045 | 0.125 | 0.0675 | Middle East |
| Kazakhstan | 321.9 | 0.019 | 0.086 | 0.0285 | Eastern Europe & Russia |
| Kenya | 55.2 | 0.045 | 0.125 | 0.0675 | Africa |
| Korea | 1304.6 | 0.006 | 0.0665 | 0.009 | Asia |
| Kuwait | 175.8 | 0.005 | 0.065 | 0.0075 | Middle East |
| Latvia | 31 | 0.016 | 0.0815 | 0.024 | Eastern Europe & Russia |
| Lebanon | 44.4 | 0.055 | 0.14 | 0.0825 | Middle East |
| Liechtenstein | 10.5 | 0 | 0.0575 | 0 | Western Europe |
| Lithuania | 45.9 | 0.016 | 0.0815 | 0.024 | Eastern Europe & Russia |
| Luxembourg | 60.1 | 0 | 0.0575 | 0 | Western Europe |
| Macao | 51.8 | 0.005 | 0.065 | 0.0075 | Asia |
| Macedonia | 10.2 | 0.036 | 0.1115 | 0.054 | Eastern Europe & Russia |
| Malaysia | 313.2 | 0.012 | 0.0755 | 0.018 | Asia |
| Malta | 9.6 | 0.012 | 0.0755 | 0.018 | Western Europe |
| Mauritius | 11.9 | 0.016 | 0.0815 | 0.024 | Asia |
| Mexico | 1260.9 | 0.012 | 0.0755 | 0.018 | Central and South America |
| Moldova | 8 | 0.065 | 0.155 | 0.0975 | Eastern Europe & Russia |
| Mongolia | 11.5 | 0.055 | 0.14 | 0.0825 | Asia |
| Montenegro | 4.4 | 0.036 | 0.1115 | 0.054 | Eastern Europe & Russia |
| Montserrat | 1.5 | 0.022 | 0.0905 | 0.033 | Caribbean |
| Morocco | 103.8 | 0.025 | 0.095 | 0.0375 | Africa |
| Mozambique | 15.6 | 0.045 | 0.125 | 0.0675 | Africa |
| Namibia | 13.1 | 0.022 | 0.0905 | 0.033 | Africa |
| Netherlands | 853.54 | 0 | 0.0575 | 0 | Western Europe |
| New Zealand | 185.8 | 0 | 0.0575 | 0 | Australia & New Zealand |
| Nicaragua | 11.3 | 0.065 | 0.155 | 0.0975 | Central and South America |
| Nigeria | 521.8 | 0.036 | 0.1115 | 0.054 | Africa |
| Norway | 512.6 | 0 | 0.0575 | 0 | Western Europe |
| Oman | 80 | 0.007 | 0.068 | 0.0105 | Middle East |
| Pakistan | 232.3 | 0.075 | 0.17 | 0.1125 | Asia |
| Panama | 42.7 | 0.019 | 0.086 | 0.0285 | Central and South America |
| Papua New Guinea | 15.3 | 0.045 | 0.125 | 0.0675 | Asia |
| Paraguay | 29 | 0.03 | 0.1025 | 0.045 | Central and South America |
| Peru | 202.4 | 0.012 | 0.0755 | 0.018 | Central and South America |
| Philippines | 272.1 | 0.019 | 0.086 | 0.0285 | Asia |
| Poland | 525.9 | 0.0085 | 0.0703 | 0.0128 | Eastern Europe & Russia |
| Portugal | 227.3 | 0.025 | 0.095 | 0.0375 | Western Europe |
| Qatar | 203.2 | 0.005 | 0.065 | 0.0075 | Middle East |
| Ras Al Khaimah (Emirate of) | 5.2 | 0.0085 | 0.0703 | 0.0128 | Middle East |
| Romania | 189.6 | 0.022 | 0.0905 | 0.033 | Eastern Europe & Russia |
| Russia | 2096.8 | 0.019 | 0.086 | 0.0285 | Eastern Europe & Russia |
| Rwanda | 7.5 | 0.055 | 0.14 | 0.0825 | Africa |
| Saudi Arabia | 748.5 | 0.006 | 0.0665 | 0.009 | Middle East |
| Senegal | 14.8 | 0.045 | 0.125 | 0.0675 | Africa |
| Serbia | 45.5 | 0.045 | 0.125 | 0.0675 | Eastern Europe & Russia |
| Sharjah | 1 | 0.012 | 0.0755 | 0.018 | Middle East |
| Singapore | 297.9 | 0 | 0.0575 | 0 | Asia |
| Slovakia | 97.7 | 0.0085 | 0.0703 | 0.0128 | Eastern Europe & Russia |
| Slovenia | 48 | 0.025 | 0.095 | 0.0375 | Eastern Europe & Russia |
| South Africa | 350.6 | 0.019 | 0.086 | 0.0285 | Africa |
| Spain | 1393 | 0.019 | 0.086 | 0.0285 | Western Europe |
| Sri Lanka | 67.2 | 0.045 | 0.125 | 0.0675 | Asia |
| St. Maarten | 1.5 | 0.016 | 0.0815 | 0.024 | Caribbean |
| St. Vincent & the Grenadines | 0.713 | 0.065 | 0.155 | 0.0975 | Caribbean |
| Suriname | 5.3 | 0.036 | 0.1115 | 0.054 | Central and South America |
| Sweden | 579.7 | 0 | 0.0575 | 0 | Western Europe |
| Switzerland | 685.4 | 0 | 0.0575 | 0 | Western Europe |
| Taiwan | 970.9 | 0.006 | 0.0665 | 0.009 | Asia |
| Thailand | 387.3 | 0.016 | 0.0815 | 0.024 | Asia |
| Trinidad and Tobago | 24.6 | 0.016 | 0.0815 | 0.024 | Caribbean |
| Tunisia | 47 | 0.036 | 0.1115 | 0.054 | Africa |
| Turkey | 822.1 | 0.022 | 0.0905 | 0.033 | Western Europe |
| Turks and Caicos Islands | 1.5 | 0.016 | 0.0815 | 0.024 | Caribbean |
| Uganda | 21.5 | 0.045 | 0.125 | 0.0675 | Africa |
| Ukraine | 177.4 | 0.1 | 0.2075 | 0.15 | Eastern Europe & Russia |
| United Arab Emirates | 402.3 | 0.005 | 0.065 | 0.0075 | Middle East |
| United Kingdom | 2678.5 | 0.004 | 0.0635 | 0.006 | Western Europe |
| United States of America | 16768.4 | 0 | 0.0575 | 0 | North America |
| Uruguay | 55.7 | 0.019 | 0.086 | 0.0285 | Central and South America |
| Venezuela | 438.3 | 0.075 | 0.17 | 0.1125 | Central and South America |
| Vietnam | 171.4 | 0.045 | 0.125 | 0.0675 | Asia |
| Zambia | 26.8 | 0.045 | 0.125 | 0.0675 | Africa |

Region aggregates at the bottom of the same sheet (rows 148–158; GDP-weighted averages of the country rows — full precision versions of the regional ERPs above):

| Region | ERP | CRP | Default Spread |
|---|---|---|---|
| Africa | 0.117299 | 0.0597993 | 0.0398662 |
| Asia | 0.0726351 | 0.0151351 | 0.0100901 |
| Australia & New Zealand | 0.0575464 | 4.63546e-05 | 3.09031e-05 |
| Caribbean | 0.143686 | 0.0861859 | 0.0574573 |
| Central and South America | 0.0995471 | 0.0420471 | 0.0280314 |
| Eastern Europe & Russia | 0.0907806 | 0.0332806 | 0.0221871 |
| Middle East | 0.0684538 | 0.0109538 | 0.0073025 |
| North America | 0.0575 | 0 | 0 |
| Western Europe | 0.0687943 | 0.0112943 | 0.00752953 |
| Global | 0.0718381 | 0.0143381 | 0.00955872 |

**Worked example (saved state — Facebook illustration):**
1. Leases: commitments 156/150/145/143/140 plus a 600 lump sum. 600/146.8 rounds to 4 years → a 150/yr annuity. Discount everything at 3.5% → lease debt 1127.9205. Depreciation = 1127.9205/9 = 125.3245. EBIT adjustment = +54.6755.
2. Equity: 2407 × 37.53 = 90,334.71.
3. Straight debt MV: 56×(1−1.035⁻³)/0.035 + 1000×1.035⁻³ = 1058.8344. Total debt = 1058.8344 + 0 + 1127.9205 = 2186.7549.
4. Beta: approach Single Business(Global) → Advertising unlevered beta 1.0965182; relever at D/E = 2186.7549/90,334.71 = 0.0242072 with t = 0.40 → 1.0965182 × (1 + 0.6×0.0242072) = 1.1124444.
5. ERP: Operating regions — revenues Asia 56, Caribbean 100, Middle East 631, North America 374, Western Europe 168 (total 1329); region ERPs 0.0726/0.1437/0.0685/0.0575/0.0688 → weighted ERP = 0.0712735.
6. Cost of equity = 0.025 + 1.1124444 × 0.0712735 = 0.1042878. After-tax cost of debt = 0.035 × 0.6 = 0.021.
7. Weights: equity 90,334.71/92,521.465 = 0.976365; debt 0.023635. WACC = 0.976365×0.1042878 + 0.023635×0.021 = **0.1023193**.
8. Synthetic-rating side calc (not driving cost of debt here since approach = Direct input): coverage = 1554.6755/95.4772 = 16.2832 → Aaa/AAA, spread 0.004, cost of debt would be 0.029.

**Reimplementation notes:**
- Inputs:
  - company metadata (strings); lease flag (bool) plus 7 lease floats; shares and price (floats)
  - beta approach (enum of 5) plus direct beta; riskfree rate (decimal fraction)
  - ERP approach (enum of 4) plus direct ERP, plus per-country or per-region revenue dicts
  - straight debt: book value, interest expense, maturity
  - cost-of-debt approach (enum of 3) plus direct rate, actual rating (string key into the spread table), firm type (1|2), and pre-tax operating income
  - tax approach plus direct tax rate; convertible (4 floats); preferred (3 floats)
  - Reference tables ship as data: industry→{unlevered beta, EV/Sales}; country→{ERP, default spread, marginal tax}; region→ERP; the two coverage→rating→spread tables; the rating→spread map.
- Order of computation: leases first (needs pre-tax cost of debt), then synthetic rating (needs lease-adjusted EBIT/interest), then cost of debt. When cost-of-debt approach = Synthetic rating this is circular: iterate to a fixed point (start with r_d = riskfree + last spread, loop lease PV → coverage → spread → r_d until converged; Excel uses iterative calculation).
- Edge cases:
  - No leases → all lease outputs are 0. The circularity disappears.
  - Year-6+ lump sum of 0 → D18 divides by zero unless guarded. Treat as 0 years and skip the annuity.
  - AVERAGE of the first five commitments = 0 → guard the D18 division.
  - Interest expense near 0 with positive EBIT → coverage explodes. The ±100000 table bounds cap it, so the result is the top rating.
  - Negative EBIT → negative coverage → D2/D (0.12 spread) via the −100000 lower bound.
  - Convertible maturity of 0 → skip the PV formula and return book/market values as-is.
  - Preferred price of 0 → guard the cost-of-preferred division.
  - Multibusiness calculators: renormalize weights over the entered rows only.
  - The direct-input beta branch is inferred (see above). Document whichever assumption the port chooses.
- Percent values are decimal fractions throughout. Book-or-market "B/V" answer-key list exists but the saved sheet exposes no cell using it (likely legacy).

---

### implprem.xls

**Purpose:** Implied equity risk premium calculator (dividend-discount version). Inputs: the current level of an equity index, its dividend yield, and growth assumptions. It does two things. (a) It computes the intrinsic value of the index for a trial risk premium. (b) It backs out the risk premium that makes intrinsic value equal the actual index level. That solved premium is Damodaran's "implied ERP" — his preferred forward-looking ERP estimate. The solve uses Excel Solver/Goal Seek; the sheet includes a screenshot note ("Enter current level of index where you see 759.64"). Only `Sheet1` has content; Sheet2–Sheet16 are empty stubs.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Level of the index | C2 | 1418.3 |
| Current dividend yield | C3 | 0.0375 |
| Expected earnings growth rate, next 5 years | C4 | 0.06 |
| Current long-term bond rate (riskfree) | C5 | 0.047 |
| Risk premium (trial value for the valuation block) | C6 | 0.0491 |
| Expected long-term growth rate | C7 | 0.047 |

**Logic (inferred, verified):**

Base dividends D₀ = C2 × C3 = 1418.3 × 0.0375 = 53.18625.

*Block 1 — Intrinsic value at the trial premium (rows 10–14), r = C5 + C6 = 0.0961:*
- Expected dividends year t = D₀ × (1+C4)^t, t = 1..5 (B11:F11 = 56.3774, 59.7601, 63.3457, 67.1464, 71.1752).
- Terminal value F12 = D₅ × (1+C7) / (r − C7) = 71.1752 × 1.047 / (0.0961 − 0.047) = 1517.7278.
- Present values B13:F13 = D_t / (1+r)^t, with the year-5 cell F13 = (D₅ + TV) / (1+r)⁵ = 1004.2608.
- Intrinsic value of index B14 = Σ B13:F13 = 1200.0564.

*Block 2 — Implied premium (rows 16–22):* identical structure, but discounted at r* = C5 + C16. **C16 is the implied risk premium** (0.04157534555252903 in the saved state). Solver/Goal Seek sets C16 so that the block's intrinsic value B22 equals the index level C2 (B22 = 1418.2999996 ≈ 1418.3). Terminal value F20 = D₅ × (1+C7)/(r* − C7) = 74.52045/0.0415753 = 1792.4189. F21 = (D₅+TV)/(1+r*)⁵ = 1219.1548.
- Note: cell G19 (75.8016) equals D₅ × 1.065. That matches no current input (D₅×(1+C7) = 74.5204). The terminal value does not use it. It appears to be a stale leftover cell — ignore it in a port.

**Reference data:** none.

**Outputs:** B14 intrinsic value of the index at the trial premium (1200.0564); C16 implied risk premium (0.0415753 = 4.16%); B22 reconstruction check (≈ index level).

**Worked example:** D₀ = 53.18625; dividends grow 6%/yr → year 5 = 71.1752. At r = 9.61%: TV = 1517.73, PV sum = 1200.06 < 1418.3, so the trial premium 4.91% is too high. Solving PV(r* = 0.047 + p) = 1418.3 gives p = 0.0415753: TV = 1792.42, PVs 51.7901 + 50.4306 + 49.1068 + 47.8177 + 1219.1548 = 1418.30.

**Reimplementation:** inputs {index_level: float, dividend_yield: fraction, growth_5yr: fraction, bond_rate: fraction, long_term_growth: fraction} (+ optional trial premium for the valuation block). Function 1: intrinsic_value(premium) = Σ_{t=1..5} D₀(1+g)^t/(1+r)^t + D₅(1+g_lt)/((r−g_lt)(1+r)⁵), r = bond_rate + premium. Function 2: implied_premium = root of intrinsic_value(p) − index_level (Brent/bisection; bracket p in (g_lt − bond_rate + ε, 0.20]). Constraint/edge cases: requires r > g_lt (premium > g_lt − bond_rate) or the TV is negative/undefined; zero dividend yield → premium undefined (value is 0 for all r); Damodaran commonly sets g_lt = bond_rate (as here). Extended versions of this model use cash yield (dividends + buybacks); this file is dividends-only.

---

### ImpliedROCROE.xls

**Purpose:** Terminal-value consistency checker. It takes terminal-year after-tax operating earnings, terminal-year FCFF, the perpetual growth rate, and the perpetual cost of capital. It reports the reinvestment rate embedded in the terminal cash flow, plus the return on capital that reinvestment rate implies. The point: check whether your terminal-value assumptions imply an implausible perpetual ROC (e.g., far above the cost of capital). Works identically for equity valuation by substituting net income / FCFE / cost of equity / ROE. Only `Sheet1` has content; Sheet2–Sheet3 are empty stubs.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| After-tax operating earnings EBIT(1−t) in terminal year (net income for equity valuation) | B2 | 1035 |
| Free cash flow to firm in terminal year (FCFE for equity valuation) | B3 | 750 |
| Perpetual growth rate | B4 | 0.04 |
| Cost of capital in perpetuity (cost of equity for equity valuation) | B5 | 0.0935 |

**Logic (inferred, verified):**
- Reinvestment rate in perpetuity B8 = 1 − B3/B2 = 1 − 750/1035 = 0.2753623.
- Implied return on capital (equity) in perpetuity B9 = B4 / B8 = g / reinvestment rate = 0.04 / 0.2753623 = 0.1452632.
- "Edification" cell B12 = B4 / B5 = the reinvestment rate you would need if ROC equaled the cost of capital = 0.04/0.0935 = 0.4278075.

**Reference data:** none.

**Outputs:** B8 embedded reinvestment rate (27.54%); B9 implied perpetual ROC/ROE (14.53%) — compare to cost of capital (9.35%): here the terminal assumptions imply value-creating excess returns forever; B12 ROC-neutral reinvestment rate (42.78%).

**Worked example:** FCFF 750 out of EBIT(1−t) 1035 means 285 reinvested → reinvestment rate 27.536%. Growing 4% forever on 27.536% reinvestment requires ROC = 0.04/0.275362 = 14.526%. If ROC were forced to the 9.35% cost of capital, sustaining 4% growth would require reinvesting 42.781% of after-tax operating income (FCFF would be 1035 × (1−0.427807) = 592.22).

**Reimplementation:** inputs {terminal_earnings: float, terminal_fcf: float, growth: fraction, discount_rate: fraction}. Outputs {reinvestment_rate, implied_return, roc_neutral_reinvestment_rate}. Edge cases:
- terminal_earnings ≤ 0 → reinvestment rate undefined (raise/None).
- terminal_fcf > terminal_earnings → negative reinvestment rate → negative implied return. Flag as inconsistent with positive perpetual growth.
- reinvestment rate = 0 with g > 0 → implied ROC infinite (flag).
- g = 0 → implied ROC 0; no reinvestment is needed.
- discount_rate = 0 → B12 undefined.

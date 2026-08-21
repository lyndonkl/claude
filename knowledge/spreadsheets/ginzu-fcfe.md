# Damodaran Model Spreadsheets — Big Picture Valuation

Source folder: `/Users/kushaldsouza/Downloads/2020/Spreadsheets/Big Picture Valuation Spreadsheets/`

### fcfeginzu.xls

**Purpose:** Damodaran's "Ginzu"-style Free Cash Flow to Equity (FCFE) discount model. It values the **equity** of a firm directly. It projects FCFE (net income minus equity reinvestment) over a high-growth phase of up to 15 years, adds a terminal stable-growth equity value, discounts everything at the **cost of equity**, and adds back current cash and marketable securities. It supports fundamental growth estimation (g = equity reinvestment rate × non-cash ROE). It optionally normalizes net income and reinvestment (net cap ex, working-capital change, net debt issued). It optionally capitalizes R&D. A 3-stage variant gradually adjusts growth, reinvestment, and cost of equity toward stable levels in the second half. Setting the high-growth period to 0 collapses it to a stable-growth-only model. This is a legacy .xls of 2020/2021 vintage (the Country ERP tab says "Updated January 1, 2021"; mature-market ERP 4.72%). The .xls dump exposes values only, not formulas. All formulas below were reconstructed from labels, layout, and exact numeric verification, and are marked "(inferred)". Every inferred formula reproduces the sheet's stored values to full float precision unless noted.

Workbook sheets: `Read me first` (documentation), `Inputs`, `FCFE Valuation` (output), `Normalized Earnings`, `Normalized Reinvestment`, `R&D converter`, `Beta calculator` (standalone helper), `ERP calculator` (standalone helper), `Industry averages` (reference data), `Country ERP` (reference data), `Input Page` (dropdown list data: Yes→1, No→2, and the list 1..15 for the growth-period picker). Caution on `Read me first`: its text is stale boiler-plate from the *dividend*-discount version of the model. It talks about dividends and payout ratios, while the actual model uses FCFE and equity reinvestment.

**Inputs:**

Sheet `Inputs` (the only sheet the user must fill for the core valuation). Example values are for the firm currently loaded (looks like Johnson & Johnson-scale data, in millions of currency):

| Label | Cell | Example value | Notes |
|---|---|---|---|
| Net Income | B2 | 4096 | current-year, in currency |
| Interest income from cash and marketable securities (after-tax) | B3 | 132 | last year's |
| Do you want to capitalize R&D expenses? | B4 | Yes | Yes/No; drives R&D converter adjustments |
| Book Value of Equity — current / last year | B5 / C5 | 12072 / 10237 | |
| Cash and Marketable Securities — current / last year | B6 / C6 | 2475 / 1918 | |
| Market Value of Equity | B7 | 357352 | (used by helper sheets; not in core chain) |
| Number of shares outstanding | B8 | 62224 | |
| Current Capital Expenditures | B9 | 11986 | |
| Current Depreciation | B10 | 9767 | |
| Change in non-cash Working capital in most recent year | B11 | 214 | |
| Net Debt Issued (Paid) during the year | B12 | −1951 | negative = net repayment |
| Normalize net income/EPS? | B13 | No | Yes/No; if Yes uses `Normalized Earnings` sheet |
| Normalize reinvestment needs? | B14 | Yes | Yes/No; if Yes uses `Normalized Reinvestment` sheet |
| Normalized Net Income (computed) | B16 | 2655.84 | from `Normalized Earnings` |
| Normalized Net Capital Expenditures (computed) | B17 | 4242.6098 | from `Normalized Reinvestment` |
| Normalized Working Capital Change (computed) | B18 | 336.3054 | from `Normalized Reinvestment` |
| Normalized Net Debt issued (computed) | B19 | 1864.6179 | from `Normalized Reinvestment` |
| Beta of the stock | B22 | 0.8 | |
| Riskfree rate | B23 | 0.02 | decimal |
| Equity Risk Premium | B24 | 0.06 | decimal |
| Length of high growth period | B27 | 15 | integer 0–15 (0 ⇒ stable-growth-only) |
| Calculate growth from fundamentals? | B29 | Yes | Yes/No |
| If No: expected growth rate in earnings, high growth | B30 | (empty) | decimal |
| Adjusted Net Income (computed) | B32 | 4325.8 | see Logic step 2 |
| Non-cash ROE (computed) | B33 | 0.519990 | see Logic step 3 |
| Equity Reinvestment Rate (computed) | B34 | 0.684737 | see Logic step 4 |
| Override high-growth inputs? | B35 | No | Yes/No |
| If yes: Non-cash ROE override | B37 | 0.15 | |
| If yes: Equity Reinvestment Rate override | B38 | 0.684737 | |
| Override stable-period ROE? | B39 | No | Yes/No |
| If yes: stable ROE | B41 | 0.15 | default 0.15; used in stable ERR even when B39=No (inferred) |
| Gradually adjust inputs during second half? | B43 | No | Yes/No; Yes ⇒ 3-stage model |
| Growth rate in stable growth period | B46 | 0.02 | decimal |
| Stable equity reinvestment ratio from fundamentals (computed) | B48 | 0.133333 | = g_stable / ROE_stable |
| Change this stable equity reinvestment rate? | B49 | No | Yes/No |
| If yes: stable-period equity reinvestment rate | B50 | (empty) | |
| Will the beta change in the stable period? | B52 | Yes | Yes/No |
| If yes: beta for stable period | B53 | 0.8 | |

Sheet `R&D converter` inputs (used when B4 = Yes):

| Label | Cell | Example |
|---|---|---|
| Amortization period for R&D (years, max 10; use lookup table below) | F6 | 5 |
| Current year's R&D expense | F7 | 1771 |
| R&D expenses, past years −1 … −N (rows A11:B20; only N rows needed) | B11:B15 | 1678, 1529, 1367, 1267, 1205 |

Sheet `Normalized Earnings` inputs (used when B13 = Yes):

| Label | Cell | Example |
|---|---|---|
| Approach chooser (1 = 5-yr average NI, 2 = normalized ROE) | B2 | 2 |
| Net Income, years −5…current (row 5, cols B–F) | B5:F5 | (blank), 15320, 11460, 21510, 25330 |
| 5-yr average NI (computed, =AVERAGE of populated cells, inferred) | G5 | 18405 |
| Normalized ROE (approach 2) | B8 | 0.22 |

Sheet `Normalized Reinvestment` inputs (used when B14 = Yes). Note: the example values on this sheet are for a *different* firm than the Inputs sheet (stale sample data) — the computed normalized values on Inputs B17:B19 come from these cells regardless:

| Label | Cell | Example |
|---|---|---|
| Net cap ex approach chooser (1 = 5-yr avg ratio to EBIT, 2 = industry avg) | B2 | 1 |
| Net Cap Ex, years −5…current (row 5, C–F populated) | C5:F5 | 2141, 3127, 3812, 2219 |
| EBIT, years −5…current (row 6) | C6:F6 | 21510, 14970, 23183, 35872 |
| Avg NetCapEx / Avg EBIT (computed) | G7 | 0.118271 |
| Industry average net cap ex / EBIT (approach 2) | B9 | 0.22 |
| Working-capital approach chooser (1 = current WC/Revenue ratio, 2 = industry avg) | B12 | 1 |
| Total non-cash working capital, current year | B14 | 1748 |
| Revenues in current year | B15 | 263989 |
| Revenues last year | B16 | 213199 |
| Industry average non-cash WC / Revenues (approach 2) | B19 | 0.22 |
| Net-debt approach chooser (1 = current book debt ratio, 2 = industry avg) | B22 | 1 |
| Book value of debt in current year | B24 | 8293 |
| Industry average debt to capital ratio (approach 2) | B27 | 0.15 |

**Logic:** (all formulas inferred from values; each verified to reproduce the stored numbers exactly)

Let `NI` = B2, `IntInc` = B3 (after-tax interest income on cash), `BVE0`/`BVE-1` = B5/C5, `Cash0`/`Cash-1` = B6/C6, `n` = B27, `rf` = B23, `ERP` = B24.

*Step 1 — R&D capitalization (sheet `R&D converter`, active when Inputs!B4 = "Yes"):*
- Amortization period `N` = F6 (integer, 1–10). For past year −k (k = 1…N): unamortized fraction = `1 − k/N`; unamortized amount = `R&D_−k × (1 − k/N)`; amortization this year = `R&D_−k / N`. The current year's R&D is fully unamortized (fraction 1).
- Value of Research Asset (D35) = `R&D_0 + Σ_{k=1..N} R&D_−k × (1 − k/N)` = 4831.
- Amortization of asset for current year (D37 = E35) = `Σ_{k=1..N} R&D_−k / N` = 1409.2.
- Adjustment to Operating Income (D39) = `R&D_0 − amortization` = 1771 − 1409.2 = **361.8** (add to reported EBIT/NI).
- Tax Effect of R&D Expensing (D40) = 137.0 — informational only, not used downstream; formula not recoverable from the .xls values (137/361.8 ≈ 0.3787, plausibly marginal tax rate × D39 with a stale tax rate) (inferred, unverified).
- If Inputs!B4 = "No": R&D adjustment = 0 (inferred).

*Step 2 — Adjusted (non-cash) net income (Inputs!B32):*
`AdjNI = NI − IntInc + RnD_adjustment` = 4096 − 132 + 361.8 = **4325.8** (verified exact).
Separately, the projection base used on the valuation sheet is `NI_noncash = NI_used − IntInc`, where `NI_used = Normalized NI (B16) if B13="Yes" else NI` (inferred for the normalized branch; with B13="No" here, base = 4096 − 132 = **3964**, verified exact — note the base is NOT R&D-adjusted).

*Step 3 — Non-cash ROE (Inputs!B33):*
`ROE_hg = AdjNI / (BVE−1 − Cash−1)` = 4325.8 / (10237 − 1918) = 4325.8 / 8319 = **0.5199903835** (verified exact). Beginning-of-year book equity net of cash; the research asset is NOT added to the denominator in this version. If B35 = "Yes", replaced by the override B37 (inferred).

*Step 4 — Equity reinvestment rate, high growth (Inputs!B34):*
Equity reinvestment `= NetCapEx + ΔWC − NetDebtIssued`. With B14 = "Yes" the three components are the normalized values B17, B18, B19; otherwise `NetCapEx = B9 − B10`, `ΔWC = B11`, `NetDebtIssued = B12` (inferred).
`ERR_hg = (NetCapEx + ΔWC − NetDebtIssued) / (NI − IntInc)` = (4242.6098 + 336.3054 − 1864.6179) / 3964 = 2714.2973 / 3964 = **0.6847369525** (verified exact). Note the denominator is NI net of interest income but WITHOUT the R&D adjustment — inconsistent with Step 3's numerator; this is what the sheet actually does. If B35 = "Yes", replaced by override B38 (inferred).

*Step 5 — Normalization sub-models:*
- Normalized Net Income (Inputs!B16), sheet `Normalized Earnings`: approach 1 ⇒ `AVERAGE(NI_−5 … NI_0)` (blanks ignored, G5 = 18405); approach 2 ⇒ `Normalized ROE × BVE0` = 0.22 × 12072 = **2655.84** (approach 2 selected via B2 = 2; verified exact).
- Normalized Net Cap Ex (Inputs!B17), sheet `Normalized Reinvestment`: approach 1 ⇒ `(AVG NetCapEx_5yr / AVG EBIT_5yr) × EBIT_current` = (2824.75 / 23883.75) × 35872 = 0.1182708 × 35872 = **4242.6098** (verified exact); approach 2 ⇒ `B9 × EBIT_current` (inferred).
- Normalized ΔWC (Inputs!B18): approach 1 ⇒ `(WC_current / Rev_current) × (Rev_current − Rev_prior)` = (1748/263989) × 50790 = **336.3054** (verified exact); approach 2 ⇒ `B19 × (Rev_current − Rev_prior)` (inferred).
- Normalized Net Debt Issued (Inputs!B19): approach 1 ⇒ `BookDebtRatio × (NormNetCapEx + NormΔWC)` where `BookDebtRatio = BVD / (BVD + BVE0)` = 8293/(8293+12072) = 0.4072183; 0.4072183 × 4578.9152 = **1864.6179** (verified exact); approach 2 ⇒ same with `B27` as the debt ratio (inferred).

*Step 6 — Discount rate:*
`CoE_hg = rf + β × ERP` = 0.02 + 0.8 × 0.06 = **0.068**.
`CoE_stable = rf + β_stable × ERP` with `β_stable = B53 if B52="Yes" else B22` = 0.02 + 0.8 × 0.06 = **0.068** (inferred).

*Step 7 — Expected growth, high growth phase (FCFE Valuation!D6):*
If B29 = "Yes": `g_hg = ERR_hg × ROE_hg` = 0.6847370 × 0.5199904 = **0.3560566** (verified exact). If B29 = "No": `g_hg = B30` (inferred).

*Step 8 — High-growth projection (FCFE Valuation rows 11–17, years t = 1…n, n ≤ 15):*
- `NI_t = NI_noncash × (1 + g_hg)^t` (year 1: 3964 × 1.3560566 = 5375.4085, verified).
- `ERR_t = ERR_hg` (constant when B43 = "No"; with B43 = "Yes" the sheet gradually adjusts g, ERR and CoE linearly toward stable levels over the second half of the period (inferred from the Read-me text; not active in this workbook)).
- `FCFE_t = NI_t × (1 − ERR_t)` for t = 1…10. **Sheet bug (verified exactly): for t = 11…15 the sheet computes `FCFE_t = NI_t × ERR_t`** (e.g. year 11: 113028.9617 × 0.6847370 = 77395.1068, matching the stored value; the intended 113028.9617 × 0.3152630 = 35633.85). A faithful port must replicate this to match the sheet's outputs; a corrected port should use `NI_t × (1 − ERR_t)` throughout.
- `CoE_t = CoE_hg` (row 15; constant here).
- Cumulative discount factor: `CumCoE_t = Π_{s=1..t} (1 + CoE_s)` (row 16; = 1.068^t here).
- `PV_t = FCFE_t / CumCoE_t` (row 17).

*Step 9 — Stable growth / terminal value:*
- `g_st` = B46 = 0.02.
- `ROE_st` = B41 (0.15) — used even though B39 = "No" (inferred; B41 appears to be the live stable-ROE cell with 0.15 as its default).
- `ERR_st` = `g_st / ROE_st` = 0.02/0.15 = **0.1333333** (B48, verified), unless B49 = "Yes" in which case B50 is used (inferred).
- Terminal price (FCFE Valuation!D22) = `NI_n × (1 + g_st) × (1 − ERR_st) / (CoE_stable − g_st)` = 382209.1187 × 1.02 × 0.8666667 / 0.048 = **7039017.9361** (verified exact).

*Step 10 — Value aggregation:*
- `PV(FCFE, high growth)` (E24) = `Σ_{t=1..n} PV_t` = 378283.9168.
- `PV(Terminal)` (E25) = `TV / CumCoE_n` = 7039017.9361 / 2.6826795 = 2623875.8446 (verified).
- `Value of equity in operating assets` (E26) = E24 + E25 = 3002159.7614.
- `+ Cash and Marketable Securities` (E27 = Inputs!B6) = 2475.
- `Value of equity in firm` (E28) = 3004634.7614.
- `Value per share` (E29) = E28 / shares = 3004634.7614 / 62224 = **48.2874** (verified).

*Helper sheet — `Beta calculator` (standalone bottom-up beta; does NOT feed Inputs!B22 automatically):* for each business line, user enters Revenues, EV/Sales multiple, and Unlevered Beta; `Estimated Value = Revenues × EV/Sales`; company unlevered beta = value-weighted average = `Σ(EstValue_i × β_u,i) / Σ EstValue_i`. Example: Healthcare Products (rev 11254.408, EV/S 7.418861, β_u 0.800892; value 83494.888) + Electronics (rev 3791.592, EV/S 3.655559, β_u 1.001356; value 13860.387) ⇒ company β_u = **0.829432** (verified exact). (Multiples/betas are meant to be picked from `Industry averages`.)

*Helper sheet — `ERP calculator` (standalone weighted ERP; does NOT feed Inputs!B24 automatically):* two alternative tables. (a) By country (up to ~10 rows + 2 free-input rows): enter Revenues per country. ERP is looked up from `Country ERP` col D (inferred VLOOKUP). `Weight = Rev_i / ΣRev`; weighted ERP = Σ Weight × ERP. Example: Albania only, ERP 0.0907990, weighted ERP 0.0907990. (b) By region: the same computation over the 9 regions, with the regional ERPs from `Country ERP` rows 185–193. Example revenues: Caribbean 10, Middle East 30, North America 35, Western Europe 15 (total 90) ⇒ weighted ERP **0.0596016** (verified). The last two rows of each table are free-input rows for e.g. "Rest of the World".

**Reference data:**

*Mature-market ERP (Country ERP!B1):* **0.0472** (updated January 1, 2021). Country ERP = mature ERP + country risk premium; CRP = adjusted default spread × (equity vol / bond vol) scalar already baked into the stored numbers.

*R&D amortization-period lookup (R&D converter!A44:B142), plus rule-of-thumb (D46:F51): Non-technological Service 2 yrs; Retail/Tech Service 3 yrs; Light Manufacturing 5 yrs; Heavy Manufacturing 10 yrs; Research with Patenting 10 yrs; Long Gestation Period 10 yrs. Full table:*

| Industry Name | Amortization Period (years) |
|---|---|
| Advertising | 2 |
| Aerospace/Defense | 10 |
| Air Transport | 10 |
| Aluminum | 5 |
| Apparel | 3 |
| Auto & Truck | 10 |
| Auto Parts (OEM) | 5 |
| Auto Parts (Replacement) | 5 |
| Bank | 2 |
| Bank (Canadian) | 2 |
| Bank (Foreign) | 2 |
| Bank (Midwest) | 2 |
| Beverage (Alcoholic) | 3 |
| Beverage (Soft Drink) | 3 |
| Building Materials | 5 |
| Cable TV | 10 |
| Canadian Energy | 10 |
| Cement & Aggregates | 10 |
| Chemical (Basic) | 10 |
| Chemical (Diversified) | 10 |
| Chemical (Specialty) | 10 |
| Coal/Alternate Energy | 5 |
| Computer & Peripherals | 5 |
| Computer Software & Svcs | 3 |
| Copper | 5 |
| Diversified Co. | 5 |
| Drug | 10 |
| Drugstore | 3 |
| Educational Services | 3 |
| Electric Util. (Central) | 10 |
| Electric Utility (East) | 10 |
| Electric Utility (West) | 10 |
| Electrical Equipment | 10 |
| Electronics | 5 |
| Entertainment | 3 |
| Environmental | 5 |
| Financial Services | 2 |
| Food Processing | 3 |
| Food Wholesalers | 3 |
| Foreign Electron/Entertn | 5 |
| Foreign Telecom. | 10 |
| Furn./Home Furnishings | 3 |
| Gold/Silver Mining | 5 |
| Grocery | 2 |
| Healthcare Info Systems | 3 |
| Home Appliance | 5 |
| Homebuilding | 5 |
| Hotel/Gaming | 3 |
| Household Products | 3 |
| Industrial Services | 3 |
| Insurance (Diversified) | 3 |
| Insurance (Life) | 3 |
| Insurance (Prop/Casualty) | 3 |
| Internet | 3 |
| Investment Co. (Domestic) | 3 |
| Investment Co. (Foreign) | 3 |
| Investment Co. (Income) | 3 |
| Machinery | 10 |
| Manuf. Housing/Rec Veh | 5 |
| Maritime | 10 |
| Medical Services | 3 |
| Medical Supplies | 5 |
| Metal Fabricating | 10 |
| Metals & Mining (Div.) | 5 |
| Natural Gas (Distrib.) | 10 |
| Natural Gas (Diversified) | 10 |
| Newspaper | 3 |
| Office Equip & Supplies | 5 |
| Oilfield Services/Equip. | 5 |
| Packaging & Container | 5 |
| Paper & Forest Products | 10 |
| Petroleum (Integrated) | 5 |
| Petroleum (Producing) | 5 |
| Precision Instrument | 5 |
| Publishing | 3 |
| R.E.I.T. | 3 |
| Railroad | 5 |
| Recreation | 5 |
| Restaurant | 2 |
| Retail (Special Lines) | 2 |
| Retail Building Supply | 2 |
| Retail Store | 2 |
| Securities Brokerage | 2 |
| Semiconductor | 5 |
| Semiconductor Cap Equip | 5 |
| Shoe | 3 |
| Steel (General) | 5 |
| Steel (Integrated) | 5 |
| Telecom. Equipment | 10 |
| Telecom. Services | 5 |
| Textile | 5 |
| Thrift | 2 |
| Tire & Rubber | 5 |
| Tobacco | 5 |
| Toiletries/Cosmetics | 3 |
| Trucking/Transp. Leasing | 5 |
| Utility (Foreign) | 10 |
| Water Utility | 10 |

*Country ERP table (Country ERP!A4:F181, verbatim; rates as decimals):*

| Country | Moody's rating | Adj. Default Spread | Equity Risk Premium | Country Risk Premium | Corporate Tax Rate |
|---|---|---|---|---|---|
| Abu Dhabi | Aa2 | 0.00438489 | 0.0520055 | 0.0048055 | 0.55 |
| Albania | B1 | 0.0397829 | 0.090799 | 0.043599 | 0.15 |
| Algeria | NR | 0.0795658 | 0.134398 | 0.087198 | 0.26 |
| Andorra (Principality of) | Caa1 | 0.0662517 | 0.119807 | 0.0726068 | 0.1 |
| Angola | Caa1 | 0.0662517 | 0.119807 | 0.0726068 | 0.3 |
| Argentina | Ca | 0.106035 | 0.163406 | 0.116206 | 0.3 |
| Armenia | Ba3 | 0.0318104 | 0.0820617 | 0.0348617 | 0.18 |
| Aruba | Baa1 | 0.0141114 | 0.062665 | 0.015465 | 0.25 |
| Australia | Aaa | 0 | 0.0472 | 0 | 0.3 |
| Austria | Aa1 | 0.00350791 | 0.0510444 | 0.0038444 | 0.25 |
| Azerbaijan | Ba2 | 0.0265485 | 0.0762951 | 0.0290951 | 0.2 |
| Bahamas | Ba2 | 0.0265485 | 0.0762951 | 0.0290951 | 0 |
| Bahrain | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0 |
| Bangladesh | Ba3 | 0.0318104 | 0.0820617 | 0.0348617 | 0.25 |
| Barbados | Caa1 | 0.0662517 | 0.119807 | 0.0726068 | 0.055 |
| Belarus | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.18 |
| Belgium | Aa3 | 0.00534159 | 0.053054 | 0.00585398 | 0.29 |
| Belize | Caa3 | 0.0883356 | 0.144009 | 0.096809 | 0.2825 |
| Benin | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.3 |
| Bermuda | A2 | 0.00749418 | 0.055413 | 0.00821304 | 0 |
| Bolivia | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.25 |
| Bosnia and Herzegovina | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.1 |
| Botswana | A2 | 0.00749418 | 0.055413 | 0.00821304 | 0.22 |
| Brazil | Ba2 | 0.0265485 | 0.0762951 | 0.0290951 | 0.34 |
| British Virgin Islands | NR | 0.0302 | 0.0803 | 0.0331 | 0.1698 |
| Brunei | NR | 0.00749418 | 0.055413 | 0.00821304 | 0 |
| Bulgaria | Baa1 | 0.0141114 | 0.062665 | 0.015465 | 0.1 |
| Burkina Faso | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.28 |
| Cambodia | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.2 |
| Cameroon | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.33 |
| Canada | Aaa | 0 | 0.0472 | 0 | 0.265 |
| Cape Verde | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0 |
| Cayman Islands | Aa3 | 0.00534159 | 0.053054 | 0.00585398 | 0 |
| Chile | A1 | 0.00621857 | 0.0540151 | 0.00681508 | 0.27 |
| China | A1 | 0.00621857 | 0.0540151 | 0.00681508 | 0.25 |
| Colombia | Baa2 | 0.016822 | 0.0656357 | 0.0184357 | 0.32 |
| Congo (Democratic Republic of) | Caa1 | 0.0662517 | 0.119807 | 0.0726068 | 0.35 |
| Congo (Republic of) | Caa2 | 0.0795658 | 0.134398 | 0.087198 | 0.3 |
| Cook Islands | B1 | 0.0397829 | 0.090799 | 0.043599 | 0.2843 |
| Costa Rica | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.3 |
| Croatia | Ba1 | 0.0220839 | 0.0714023 | 0.0242023 | 0.18 |
| Cuba | Caa2 | 0.0795658 | 0.134398 | 0.087198 | 0.2736 |
| Curaçao | A3 | 0.0106035 | 0.0588206 | 0.0116206 | 0.22 |
| Cyprus | Ba2 | 0.0265485 | 0.0762951 | 0.0290951 | 0.125 |
| Czech Republic | Aa3 | 0.00534159 | 0.053054 | 0.00585398 | 0.19 |
| Denmark | Aaa | 0 | 0.0472 | 0 | 0.22 |
| Dominican Republic | Ba3 | 0.0318104 | 0.0820617 | 0.0348617 | 0.27 |
| Ecuador | Caa3 | 0.0883356 | 0.144009 | 0.096809 | 0.25 |
| Egypt | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.225 |
| El Salvador | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.3 |
| Estonia | A1 | 0.00621857 | 0.0540151 | 0.00681508 | 0.2 |
| Ethiopia | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.3 |
| Fiji | Ba3 | 0.0318104 | 0.0820617 | 0.0348617 | 0.2 |
| Finland | Aa1 | 0.00350791 | 0.0510444 | 0.0038444 | 0.2 |
| France | Aa2 | 0.00438489 | 0.0520055 | 0.0048055 | 0.28 |
| Gabon | Caa1 | 0.0662517 | 0.119807 | 0.0726068 | 0.3 |
| Gambia | NR | 0.0574819 | 0.110196 | 0.0629958 | 0.31 |
| Georgia | Ba2 | 0.0265485 | 0.0762951 | 0.0290951 | 0.15 |
| Germany | Aaa | 0 | 0.0472 | 0 | 0.3 |
| Ghana | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.25 |
| Greece | Ba3 | 0.0318104 | 0.0820617 | 0.0348617 | 0.24 |
| Guatemala | Ba1 | 0.0220839 | 0.0714023 | 0.0242023 | 0.25 |
| Guernsey | Aaa | 0 | 0.0472 | 0 | 0 |
| Guinea | NR | 0.106035 | 0.163406 | 0.116206 | 0.2825 |
| Guinea-Bissau | NR | 0.0662517 | 0.119807 | 0.0726068 | 0.2825 |
| Guyana | NR | 0.0486324 | 0.100497 | 0.0532974 | 0.2736 |
| Haiti | NR | 0.106035 | 0.163406 | 0.116206 | 0.2736 |
| Honduras | B1 | 0.0397829 | 0.090799 | 0.043599 | 0.25 |
| Hong Kong | Aa3 | 0.00534159 | 0.053054 | 0.00585398 | 0.165 |
| Hungary | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.09 |
| Iceland | A2 | 0.00749418 | 0.055413 | 0.00821304 | 0.2 |
| India | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.3 |
| Indonesia | Baa2 | 0.016822 | 0.0656357 | 0.0184357 | 0.15 |
| Iran | NR | 0.0795658 | 0.134398 | 0.087198 | 0.2113 |
| Iraq | Caa1 | 0.0662517 | 0.119807 | 0.0726068 | 0.15 |
| Ireland | A2 | 0.00749418 | 0.055413 | 0.00821304 | 0.125 |
| Isle of Man | Aa3 | 0.00534159 | 0.053054 | 0.00585398 | 0 |
| Israel | A1 | 0.00621857 | 0.0540151 | 0.00681508 | 0.23 |
| Italy | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.24 |
| Ivory Coast | Ba3 | 0.0318104 | 0.0820617 | 0.0348617 | 0.25 |
| Jamaica | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.25 |
| Japan | A1 | 0.00621857 | 0.0540151 | 0.00681508 | 0.3062 |
| Jersey | Aaa | 0 | 0.0472 | 0 | 0 |
| Jordan | B1 | 0.0397829 | 0.090799 | 0.043599 | 0.2 |
| Kazakhstan | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.2 |
| Kenya | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.3 |
| Korea, D.P.R. | NR | 0.106035 | 0.163406 | 0.116206 | 0.2113 |
| Kuwait | A1 | 0.00621857 | 0.0540151 | 0.00681508 | 0.15 |
| Kyrgyzstan | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.1 |
| Laos | Caa2 | 0.0106035 | 0.0588206 | 0.0116206 | 0.2113 |
| Latvia | A3 | 0.0106035 | 0.0588206 | 0.0116206 | 0.2 |
| Lebanon | C | 0.175 | 0.238987 | 0.191787 | 0.17 |
| Liberia | NR | 0.106035 | 0.163406 | 0.116206 | 0.2825 |
| Libya | NR | 0.0795658 | 0.134398 | 0.087198 | 0.2 |
| Liechtenstein | Aaa | 0 | 0.0472 | 0 | 0.125 |
| Lithuania | A3 | 0.0106035 | 0.0588206 | 0.0116206 | 0.15 |
| Luxembourg | Aaa | 0 | 0.0472 | 0 | 0.2494 |
| Macao | Aa3 | 0.00534159 | 0.053054 | 0.00585398 | 0.12 |
| Macedonia | Ba3 | 0.0318104 | 0.0820617 | 0.0348617 | 0.1 |
| Madagascar | NR | 0.0574819 | 0.110196 | 0.0629958 | 0.2 |
| Malawi | NR | 0.0795658 | 0.134398 | 0.087198 | 0.3 |
| Malaysia | A3 | 0.0106035 | 0.0588206 | 0.0116206 | 0.24 |
| Mali | Caa1 | 0.0662517 | 0.119807 | 0.0726068 | 0.2825 |
| Malta | A2 | 0.00749418 | 0.055413 | 0.00821304 | 0.35 |
| Mauritius | Baa1 | 0.0141114 | 0.062665 | 0.015465 | 0.15 |
| Mexico | Baa1 | 0.0141114 | 0.062665 | 0.015465 | 0.3 |
| Moldova | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.12 |
| Mongolia | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.25 |
| Montenegro | B1 | 0.0397829 | 0.090799 | 0.043599 | 0.09 |
| Montserrat | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.2113 |
| Morocco | Ba1 | 0.0220839 | 0.0714023 | 0.0242023 | 0.31 |
| Mozambique | Caa2 | 0.0795658 | 0.134398 | 0.087198 | 0.32 |
| Myanmar | NR | 0.0574819 | 0.110196 | 0.0629958 | 0.25 |
| Namibia | Ba3 | 0.0318104 | 0.0820617 | 0.0348617 | 0.32 |
| Netherlands | Aaa | 0 | 0.0472 | 0 | 0.25 |
| New Zealand | Aaa | 0 | 0.0472 | 0 | 0.28 |
| Nicaragua | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.3 |
| Niger | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.2825 |
| Nigeria | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.3 |
| Norway | Aaa | 0 | 0.0472 | 0 | 0.22 |
| Oman | Ba3 | 0.0318104 | 0.0820617 | 0.0348617 | 0.15 |
| Pakistan | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.35 |
| Panama | Baa1 | 0.0141114 | 0.062665 | 0.015465 | 0.25 |
| Papua New Guinea | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.3 |
| Paraguay | Ba1 | 0.0220839 | 0.0714023 | 0.0242023 | 0.1 |
| Peru | A3 | 0.0106035 | 0.0588206 | 0.0116206 | 0.295 |
| Philippines | Baa2 | 0.016822 | 0.0656357 | 0.0184357 | 0.3 |
| Poland | A2 | 0.00749418 | 0.055413 | 0.00821304 | 0.19 |
| Portugal | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.21 |
| Qatar | Aa3 | 0.00534159 | 0.053054 | 0.00585398 | 0.1 |
| Ras Al Khaimah (Emirate of) | Aaa | 0 | 0.0472 | 0 | 0 |
| Romania | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.16 |
| Russia | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.2 |
| Rwanda | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.3 |
| Saint Lucia | NR | 0.0302 | 0.0803 | 0.0331 | 0.1698 |
| Saudi Arabia | A1 | 0.00621857 | 0.0540151 | 0.00681508 | 0.2 |
| Senegal | Ba3 | 0.0318104 | 0.0820617 | 0.0348617 | 0.3 |
| Serbia | Ba3 | 0.0318104 | 0.0820617 | 0.0348617 | 0.15 |
| Sharjah | Baa2 | 0.016822 | 0.0656357 | 0.0184357 | 0 |
| Sierra Leone | NR | 0.0795658 | 0.134398 | 0.087198 | 0.3 |
| Singapore | Aaa | 0 | 0.0472 | 0 | 0.17 |
| Slovakia | A2 | 0.00749418 | 0.055413 | 0.00821304 | 0.21 |
| Slovenia | A3 | 0.0106035 | 0.0588206 | 0.0116206 | 0.19 |
| Solomon Islands | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.3 |
| Somalia | NR | 0.106035 | 0.163406 | 0.116206 | 0.2825 |
| South Africa | Ba2 | 0.0265485 | 0.0762951 | 0.0290951 | 0.28 |
| South Korea | Aa2 | 0.00438489 | 0.0520055 | 0.0048055 | 0.25 |
| Spain | Baa1 | 0.0141114 | 0.062665 | 0.015465 | 0.25 |
| Sri Lanka | Caa1 | 0.0662517 | 0.119807 | 0.0726068 | 0.28 |
| St. Maarten | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.2736 |
| St. Vincent & the Grenadines | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.2736 |
| Sudan | NR | 0.175 | 0.238987 | 0.191787 | 0.35 |
| Suriname | Caa3 | 0.0883356 | 0.144009 | 0.096809 | 0.36 |
| Swaziland | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.275 |
| Sweden | Aaa | 0 | 0.0472 | 0 | 0.214 |
| Switzerland | Aaa | 0 | 0.0472 | 0 | 0.1484 |
| Syria | NR | 0.175 | 0.238987 | 0.191787 | 0.28 |
| Taiwan | Aa3 | 0.00534159 | 0.053054 | 0.00585398 | 0.2 |
| Tajikistan | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.1912 |
| Tanzania | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.3 |
| Thailand | Baa1 | 0.0141114 | 0.062665 | 0.015465 | 0.2 |
| Togo | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.2825 |
| Trinidad and Tobago | Ba1 | 0.0220839 | 0.0714023 | 0.0242023 | 0.3 |
| Tunisia | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.25 |
| Turkey | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.22 |
| Turks and Caicos Islands | Baa1 | 0.0141114 | 0.062665 | 0.015465 | 0 |
| Uganda | B2 | 0.0486324 | 0.100497 | 0.0532974 | 0.3 |
| Ukraine | B3 | 0.0574819 | 0.110196 | 0.0629958 | 0.18 |
| United Arab Emirates | Aa2 | 0.00438489 | 0.0520055 | 0.0048055 | 0.55 |
| United Kingdom | Aa3 | 0.00534159 | 0.053054 | 0.00585398 | 0.19 |
| United States | Aaa | 0 | 0.0472 | 0 | 0.27 |
| Uruguay | B1 | 0.0397829 | 0.090799 | 0.043599 | 0.25 |
| Venezuela | C | 0.175 | 0.238987 | 0.191787 | 0.34 |
| Vietnam | Ba3 | 0.0318104 | 0.0820617 | 0.0348617 | 0.2 |
| Yemen | NR | 0.175 | 0.238987 | 0.191787 | 0.2825 |
| Zambia | Ca | 0.106035 | 0.163406 | 0.116206 | 0.35 |
| Zimbabwe | NR | 0.106035 | 0.163406 | 0.116206 | 0.24 |

*Regional ERP table (Country ERP!A184:E193 plus Global row 195, verbatim):*

| Region | ERP | Default Spread | Tax rate | CRP |
|---|---|---|---|---|
| Africa | 0.0966419 | 0.0451144 | 0.283142 | 0.0494419 |
| Asia | 0.0574677 | 0.00936901 | 0.256958 | 0.0102677 |
| Australia & New Zealand | 0.0472327 | 2.98223e-05 | 0.297403 | 3.26829e-05 |
| Caribbean | 0.100313 | 0.0484638 | 0.242518 | 0.0531126 |
| Central and South America | 0.0871004 | 0.0364081 | 0.310394 | 0.0399004 |
| Eastern Europe & Russia | 0.0679805 | 0.0189617 | 0.183075 | 0.0207805 |
| Middle East | 0.0625018 | 0.0139625 | 0.329559 | 0.0153018 |
| North America | 0.0472 | 0 | 0.269624 | 0 |
| Western Europe | 0.0555975 | 0.00766247 | 0.244065 | 0.00839748 |
| Global | 0.0576303 | 0.00951739 | 0.261339 | 0.0104303 |

*Industry averages (sheet `Industry averages`, verbatim, ~95 US industries; used for bottom-up betas, EV/Sales, and normalization benchmarks; "NA" = not meaningful; ratios as decimals; floats shown to 6 significant digits — the sheet stores full precision):*

| Industry Name | Number of firms | Annual Average Revenue growth - Last 5 years | Pre-tax Operating Margin (Unadjusted) | After-tax ROC | Average effective tax rate | Unlevered Beta | Equity (Levered) Beta | Cost of equity | Std deviation in stock prices | Pre-tax cost of debt | Market Debt/Capital | Cost of capital | Sales/Capital | EV/Sales | EV/EBITDA | EV/EBIT | Price/Book | Trailing PE | Non-cash WC as % of Revenues | Cap Ex as % of Revenues | Net Cap Ex as % of Revenues | Reinvestment Rate | ROE | Dividend Payout Ratio | Equity Reinvestment Rate | Pre-tax Operating Margin (Lease & R&D adjusted) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Advertising | 61 | 0.083146 | 0.0997898 | 0.515119 | 0.214738 | 0.774409 | 1.07632 | 0.0601022 | 0.577364 | 0.02998 | 0.436624 | 0.0434158 | 5.16893 | 1.82797 | 8.86031 | 16.0813 | 5.72958 | 45.3752 | -0.00574586 | 0.0175 | -0.0191184 | -0.316706 | 0.0293327 | 9.12847 | 9.12847 | 0.103123 |
| Aerospace/Defense | 72 | 0.0528356 | 0.0755582 | 0.191149 | 0.246217 | 0.912411 | 1.06541 | 0.0595874 | 0.348929 | 0.0258 | 0.248399 | 0.0494643 | 2.60599 | 2.01177 | 12.1527 | 20.31 | 4.43692 | 107.384 | 0.43564 | 0.0276829 | -0.0133395 | 0.369322 | 0.0854319 | 1.20552 | 1.20552 | 0.0789221 |
| Air Transport | 17 | -0.0682292 | -0.189906 | -0.160654 | 0.887578 | 0.919622 | 1.60816 | 0.0852053 | 0.461508 | 0.02998 | 0.617385 | 0.0461126 | 0.883238 | 1.9728 | 34.4254 | NA | 3.22415 | 13.4675 | 0.0170444 | 0.118329 | 0.01799 | NA | -0.470269 | 0.000864253 | 0.000864253 | -0.193518 |
| Apparel | 51 | -0.0355531 | 0.0548723 | 0.0754226 | 0.314099 | 0.941363 | 1.09822 | 0.0611359 | 0.478436 | 0.02998 | 0.282584 | 0.0500444 | 1.33913 | 2.02584 | 14.6887 | 33.9763 | 4.11169 | 22.7618 | 0.249623 | 0.0251721 | 0.00155314 | -1.46723 | -0.081881 | 0.00324527 | 0.00324527 | 0.0591386 |
| Auto & Truck | 19 | 0.121917 | 0.0193335 | 0.0117091 | 0.284806 | 1.05 | 1.28283 | 0.0698494 | 0.45237 | 0.02998 | 0.278841 | 0.0564751 | 0.742704 | 3.58284 | 45.7299 | 177.76 | 7.57876 | 261.56 | -0.0693914 | 0.102444 | 0.0461151 | 1.84403 | 0.0448852 | 0.645799 | 0.645799 | 0.0173328 |
| Auto Parts | 52 | 0.0402104 | 0.0400989 | 0.0645865 | 0.326452 | 1.09381 | 1.2035 | 0.0661051 | 0.431649 | 0.02998 | 0.195955 | 0.05744 | 1.82234 | 1.59739 | 10.0698 | 23.2824 | 4.7756 | 55.5647 | 0.138412 | 0.0371128 | 0.0208745 | 0.300695 | -0.143107 | 0.00418224 | 0.00418224 | 0.0385071 |
| Bank (Money Center) | 7 | -0.00776833 | 0 | -0.000133079 | 0.140435 | 0.598479 | 0.827708 | 0.0483678 | 0.215882 | 0.0192 | 0.683737 | 0.0248802 | 0.142835 | 5.31698 | NA | NA | 1.00312 | 14.8627 | NA | 0.0105672 | 0.0105672 | NA | 0.0741321 | 0.469501 | 0.469501 | -0.00111127 |
| Banks (Regional) | 598 | 0.088246 | 0 | -0.000810559 | 0.189516 | 0.600109 | 0.644875 | 0.0397381 | 0.194833 | 0.0192 | 0.379836 | 0.0299679 | 0.239305 | 4.47271 | NA | NA | 1.0755 | 15.3852 | NA | 0.043659 | 0.0200835 | NA | 0.0821638 | 0.443522 | 0.443522 | -0.00405254 |
| Beverage (Alcoholic) | 23 | 0.1439 | 0.238743 | 0.144302 | 0.183565 | 0.676031 | 0.778264 | 0.0460341 | 0.37008 | 0.0258 | 0.189667 | 0.0408751 | 0.63934 | 5.29953 | 17.6062 | 22.2129 | 3.45092 | 32.3896 | 0.152547 | 0.0637922 | 0.0449066 | 0.241096 | 0.101032 | 0.415798 | 0.415798 | 0.238408 |
| Beverage (Soft) | 41 | 0.27075 | 0.199771 | 0.267363 | 0.186006 | 0.707455 | 0.791261 | 0.0466475 | 0.49695 | 0.02998 | 0.177636 | 0.0422489 | 1.37496 | 5.07507 | 20.735 | 25.2225 | 8.49634 | 116.717 | -0.095445 | 0.0541647 | 0.0740617 | 0.370089 | 0.288572 | 0.741929 | 0.741929 | 0.201128 |
| Broadcasting | 29 | 0.057983 | 0.192951 | 0.169217 | 0.231608 | 0.653361 | 1.12904 | 0.0625907 | 0.455576 | 0.02998 | 0.548978 | 0.0402444 | 0.979946 | 2.0808 | 7.84359 | 10.9312 | 1.58271 | 12.4199 | 0.157117 | 0.0274472 | -0.0105186 | 1.11056 | 0.00238502 | 0.00169738 | 0.00169738 | 0.190297 |
| Brokerage & Investment Banking | 39 | 0.0951435 | 0.00421208 | -2.893e-05 | 0.221765 | 0.576942 | 1.13184 | 0.0627228 | 0.359028 | 0.0258 | 0.686399 | 0.0325976 | 0.215965 | 4.93067 | NA | NA | 1.51655 | 82.1984 | NA | 0.0523928 | 0.0274482 | NA | 0.120761 | 0.208419 | 0.208419 | -0.00014972 |
| Building Materials | 42 | 0.0747328 | 0.108039 | 0.241657 | 0.262598 | 0.970355 | 1.08849 | 0.0606767 | 0.339932 | 0.0258 | 0.208164 | 0.0519666 | 2.59246 | 1.99532 | 13.2711 | 18.1671 | 4.97699 | 25.6341 | 0.154534 | 0.0244336 | 0.00452789 | -0.0246136 | 0.205385 | 0.21488 | 0.21488 | 0.109831 |
| Business & Consumer Services | 169 | 0.0753336 | 0.0887941 | 0.183299 | 0.238398 | 0.830021 | 0.926793 | 0.0530446 | 0.456454 | 0.02998 | 0.198189 | 0.0468692 | 2.15716 | 2.96567 | 17.397 | 31.2073 | 5.84946 | 44.2206 | 0.138368 | 0.0313652 | 0.00344509 | -0.11508 | 0.0680907 | 0.658692 | 0.658692 | 0.0917539 |
| Cable TV | 13 | 0.0669875 | 0.181518 | 0.11087 | 0.223275 | 0.700509 | 0.942966 | 0.053808 | 0.320159 | 0.0258 | 0.341947 | 0.0418487 | 0.756996 | 3.8523 | 11.1107 | 20.1975 | 3.12676 | 63.6767 | -0.0134787 | 0.109441 | -0.0174479 | -0.150093 | 0.114659 | 0.262047 | 0.262047 | 0.180743 |
| Chemical (Basic) | 48 | 0.225073 | 0.0721258 | 0.0952613 | 0.0911708 | 0.761775 | 0.993478 | 0.0561921 | 0.48059 | 0.02998 | 0.355328 | 0.044002 | 1.34957 | 1.51741 | 10.0098 | 20.7025 | 2.96135 | 45.8639 | 0.157817 | 0.0632938 | 0.0316443 | 0.182402 | -0.0181726 | 0.00439148 | 0.00439148 | 0.0727598 |
| Chemical (Diversified) | 5 | 0.28994 | 0.058127 | 0.059258 | 0.057041 | 1.03607 | 1.36272 | 0.0736205 | 0.361612 | 0.0258 | 0.367488 | 0.0534871 | 1.03193 | 1.71935 | 13.3813 | 29.2506 | 2.17847 | 17.1861 | 0.17676 | 0.0507431 | 0.0239198 | -0.687907 | 0.132535 | 0.518444 | 0.518444 | 0.0581557 |
| Chemical (Specialty) | 97 | 0.0593542 | 0.120655 | 0.118414 | 0.181689 | 0.818212 | 0.926592 | 0.0530351 | 0.385413 | 0.0258 | 0.202252 | 0.0461179 | 1.03915 | 3.27349 | 15.5579 | 26.5325 | 3.09721 | 58.8646 | 0.212884 | 0.0637165 | 0.023085 | 0.104857 | 0.025 | 1.63689 | 1.63689 | 0.12184 |
| Coal & Related Energy | 29 | -0.141845 | -0.0870214 | -0.0749637 | 0 | 0.562177 | 0.827671 | 0.048366 | 0.42274 | 0.02998 | 0.486203 | 0.0354911 | 0.870192 | 1.08293 | 5.78523 | NA | 1.35789 | 37.6804 | 0.0774553 | 0.112869 | -0.071878 | NA | -0.416638 | 0.0223758 | 0.0223758 | -0.0861462 |
| Computer Services | 116 | 0.09404 | 0.0757878 | 0.229802 | 0.129351 | 0.940194 | 1.11725 | 0.0620344 | 0.458909 | 0.02998 | 0.284416 | 0.0506153 | 3.02983 | 1.43233 | 10.7033 | 17.9554 | 4.00098 | 27.8603 | 0.120857 | 0.0180505 | -0.00133984 | -0.165771 | 0.134996 | 0.755716 | 0.755716 | 0.0802152 |
| Computers/Peripherals | 52 | 0.04061 | 0.15552 | 0.278169 | 0.141734 | 1.13942 | 1.18407 | 0.0651883 | 0.428664 | 0.02998 | 0.0855483 | 0.0614838 | 1.80635 | 5.14064 | 24.7634 | 32.8918 | 22.896 | 27.2546 | -0.0908312 | 0.027159 | 0.00170438 | -0.00244326 | 0.505307 | 0.268323 | 0.268323 | 0.159761 |
| Construction Supplies | 46 | 0.0350244 | 0.0941104 | 0.0993276 | 0.229869 | 0.872215 | 1.0211 | 0.0574957 | 0.333908 | 0.0258 | 0.258048 | 0.0475191 | 1.20678 | 2.26533 | 15.2338 | 23.4705 | 3.82022 | 108.397 | 0.172307 | 0.0521314 | 0.0196324 | -0.0825777 | 0.132037 | 0.49846 | 0.49846 | 0.0924782 |
| Diversified | 29 | 0.00507636 | 0.180642 | 0.134447 | 0.207596 | 0.892924 | 1.0248 | 0.0576707 | 0.299374 | 0.0258 | 0.229214 | 0.0487688 | 0.792749 | 2.79735 | 11.3736 | 15.1209 | 1.85718 | 27.9836 | 0.0148349 | 0.0507739 | 0.0296954 | 0.204858 | 0.106208 | 0.143214 | 0.143214 | 0.181428 |
| Drugs (Biotechnology) | 547 | 0.326399 | 0.0954414 | 0.0621917 | 0.119511 | 0.851496 | 0.886212 | 0.0511292 | 0.50102 | 0.02998 | 0.134197 | 0.0472048 | 0.483365 | 8.73444 | 14.3955 | 57.628 | 7.18063 | 480.184 | 0.131362 | 0.0356296 | 0.376489 | 7.21549 | -0.0118784 | 0.00125844 | 0.00125844 | 0.129152 |
| Drugs (Pharmaceutical) | 287 | 0.326554 | 0.240201 | 0.203109 | 0.162982 | 0.837279 | 0.908218 | 0.0521679 | 0.554524 | 0.02998 | 0.153838 | 0.0475093 | 0.814863 | 5.5546 | 14.3204 | 22.2677 | 5.04234 | 34.5421 | 0.262256 | 0.0500538 | 0.0973906 | 0.489171 | 0.189789 | 0.608553 | 0.608553 | 0.25377 |
| Education | 38 | 0.0100889 | 0.0926135 | 0.0988917 | 0.166546 | 1.07062 | 1.14768 | 0.0634705 | 0.557267 | 0.02998 | 0.195704 | 0.0553322 | 1.16688 | 2.80635 | 14.4279 | 31.2059 | 2.91744 | 26.6313 | 0.0747145 | 0.0387543 | 0.0269576 | 0.614076 | -0.0566281 | 0.000587531 | 0.000587531 | 0.0882498 |
| Electrical Equipment | 122 | 0.0421161 | 0.12602 | 0.221215 | 0.172127 | 1.00136 | 1.05904 | 0.0592865 | 0.551194 | 0.02998 | 0.133074 | 0.0543094 | 1.80338 | 3.65556 | 15.9576 | 22.8283 | 6.27509 | 106.019 | 0.209957 | 0.0378667 | 0.0449205 | 0.36522 | 0.176672 | 0.435471 | 0.435471 | 0.128362 |
| Electronics (Consumer & Office) | 22 | 0.0169417 | 0.0199043 | 0.0466075 | 0.112806 | 1.01082 | 0.955353 | 0.0543926 | 0.549089 | 0.02998 | 0.0867835 | 0.0515716 | 1.82016 | 1.31663 | 18.9611 | 59.5184 | 4.26304 | 14.6215 | 0.132551 | 0.0167561 | 0.00974315 | -1.12446 | -0.0488572 | 0 | 0 | 0.0258206 |
| Electronics (General) | 157 | 0.0287724 | 0.0746722 | 0.110846 | 0.198495 | 0.858211 | 0.885267 | 0.0510846 | 0.438651 | 0.02998 | 0.118813 | 0.0476154 | 1.48977 | 2.54367 | 17.5178 | 32.1208 | 4.14108 | 69.7619 | 0.205151 | 0.0419467 | 0.0424506 | 0.599645 | 0.0666852 | 0.414804 | 0.414804 | 0.0790347 |
| Engineering/Construction | 61 | 0.0357003 | 0.0410327 | 0.1485 | 0.21895 | 0.955633 | 1.05642 | 0.059163 | 0.420426 | 0.02998 | 0.220187 | 0.050955 | 3.79646 | 0.899473 | 10.8531 | 19.7955 | 2.31822 | 34.5249 | 0.179394 | 0.0169562 | 0.103192 | 2.83751 | 0.0253691 | 0.527882 | 0.527882 | 0.043132 |
| Entertainment | 118 | 0.063537 | 0.074408 | 0.0796458 | 0.0673128 | 0.838756 | 0.882817 | 0.050969 | 0.680622 | 0.040925 | 0.131912 | 0.0481864 | 1.0663 | 6.809 | 36.2568 | 89.2415 | 5.48912 | 1157.13 | 0.00651299 | 0.0518129 | 0.0028006 | 0.166812 | -0.028668 | 0.00111919 | 0.00111919 | 0.0750624 |
| Environmental & Waste Services | 86 | 0.0787917 | 0.119172 | 0.191896 | 0.206769 | 0.821935 | 0.954408 | 0.054348 | 0.504308 | 0.02998 | 0.201267 | 0.0478144 | 1.63028 | 3.34084 | 14.9784 | 27.4187 | 4.68076 | 549.579 | 0.0955603 | 0.0748874 | 0.0282593 | 0.224954 | 0.0621018 | 0.947627 | 0.947627 | 0.120962 |
| Farming/Agriculture | 32 | -0.00769937 | 0.0655487 | 0.0912458 | 0.218685 | 0.686112 | 0.874699 | 0.0505858 | 0.452993 | 0.02998 | 0.310601 | 0.0416714 | 1.47586 | 1.35162 | 14.7079 | 20.1292 | 3.20905 | 23.8193 | 0.129996 | 0.0306153 | 0.0134505 | 0.387265 | 0.140292 | 0.389322 | 0.389322 | 0.0661317 |
| Financial Svcs. (Non-bank & Insurance) | 235 | 0.0908278 | 0.123166 | 0.003987 | 0.192127 | 0.109105 | 0.797101 | 0.0469232 | 0.277386 | 0.0258 | 0.899587 | 0.0216545 | 0.037411 | 31.4863 | NA | NA | 2.22993 | 21.8645 | NA | 0.0699068 | 0.13198 | 1.22625 | 0.642825 | 0.238597 | 0.238597 | 0.122321 |
| Food Processing | 101 | 0.0684884 | 0.127989 | 0.175309 | 0.250201 | 0.532117 | 0.636327 | 0.0393346 | 0.325572 | 0.0258 | 0.248191 | 0.0342466 | 1.48012 | 2.19359 | 12.8831 | 16.8265 | 2.56671 | 375.195 | 0.0526542 | 0.0321304 | 0.020938 | 0.151239 | 0.101179 | 0.609763 | 0.609763 | 0.129528 |
| Food Wholesalers | 18 | 0.120125 | 0.0155849 | 0.08886 | 0.0387202 | 0.806676 | 1.03462 | 0.0581342 | 0.580329 | 0.02998 | 0.359047 | 0.0451192 | 5.8166 | 0.543616 | 15.872 | 35.361 | 5.01741 | 8.6353 | 0.0538161 | 0.0101548 | 0.0261255 | 0.875557 | -0.0502568 | 0.00199422 | 0.00199422 | 0.0153567 |
| Furn/Home Furnishings | 40 | 0.0508444 | 0.0797926 | 0.145941 | 0.189165 | 0.779488 | 0.883245 | 0.0509892 | 0.405229 | 0.02998 | 0.254058 | 0.0435951 | 1.87871 | 1.31084 | 9.73342 | 15.8164 | 2.68118 | 125.498 | 0.106044 | 0.0274221 | 0.0137225 | -0.268316 | 0.133702 | 0.271742 | 0.271742 | 0.0815821 |
| Green & Renewable Energy | 25 | -0.0009 | 0.261193 | 0.0689336 | 0.430343 | 0.678764 | 0.98185 | 0.0556433 | 0.560417 | 0.02998 | 0.390473 | 0.0424618 | 0.271028 | 13.1527 | 22.9404 | 50.7628 | 1.68016 | 40.6726 | -1.58246 | 0.356871 | 0.258198 | 1.10114 | -0.205889 | 0.00145349 | 0.00145349 | 0.258825 |
| Healthcare Products | 265 | 0.139001 | 0.142363 | 0.132184 | 0.136415 | 0.800892 | 0.833584 | 0.0486452 | 0.461895 | 0.02998 | 0.0965571 | 0.0460613 | 0.963177 | 7.41886 | 28.5289 | 49.2488 | 5.77454 | 317.981 | 0.251628 | 0.051532 | 0.11833 | 1.13464 | 0.105491 | 0.301072 | 0.301072 | 0.140906 |
| Healthcare Support Services | 129 | 0.175439 | 0.0496888 | 0.352718 | 0.240537 | 0.738808 | 0.850774 | 0.0494566 | 0.444916 | 0.02998 | 0.240723 | 0.0428195 | 7.71543 | 0.682084 | 10.361 | 13.6284 | 2.90887 | 104.176 | -0.053313 | 0.00740918 | 0.00684623 | 0.195717 | 0.165983 | 0.256273 | 0.256273 | 0.0484477 |
| Heathcare Information and Technology | 139 | 0.150239 | 0.1314 | 0.163522 | 0.164274 | 0.753504 | 0.790903 | 0.0466306 | 0.424486 | 0.02998 | 0.107938 | 0.0439597 | 1.24453 | 7.33387 | 29.3167 | 50.4877 | 7.11966 | 162.961 | 0.230696 | 0.0382416 | 0.000724692 | 0.102832 | 0.141101 | 0.10554 | 0.10554 | 0.136881 |
| Homebuilding | 30 | 0.135222 | 0.118118 | 0.135766 | 0.203044 | 1.32903 | 1.45895 | 0.0781626 | 0.365573 | 0.0258 | 0.246577 | 0.0635335 | 1.36576 | 1.2092 | 9.54493 | 10.2268 | 1.75068 | 17.3421 | 0.660964 | 0.00735338 | 0.00631101 | -0.101478 | 0.17702 | 0.0758222 | 0.0758222 | 0.118209 |
| Hospitals/Healthcare Facilities | 32 | 0.0423655 | 0.101951 | 0.13176 | 0.203154 | 0.807725 | 1.2831 | 0.0698624 | 0.492114 | 0.02998 | 0.498502 | 0.0459458 | 1.51241 | 1.53552 | 8.96546 | 16.1832 | 5.7799 | 44.6067 | 0.0337263 | 0.0591866 | 0.0139277 | -0.260961 | 0.706385 | 0.109113 | 0.109113 | 0.0948578 |
| Hotel/Gaming | 66 | -0.00379595 | -0.103381 | -0.0523661 | 0.233404 | 1.18983 | 1.56468 | 0.0831531 | 0.436942 | 0.02998 | 0.364013 | 0.0608509 | 0.381804 | 8.07826 | 38.3248 | NA | 6.09657 | 64.1717 | 0.156699 | 0.18514 | 0.129963 | NA | -0.304042 | 0.00500764 | 0.00500764 | -0.140132 |
| Household Products | 140 | 0.141768 | 0.181967 | 0.349908 | 0.202369 | 0.683785 | 0.730004 | 0.0437562 | 0.546567 | 0.02998 | 0.129285 | 0.0409286 | 2.01703 | 4.09342 | 17.5998 | 22.3269 | 9.05877 | 36.292 | 0.0885296 | 0.0364695 | 0.0127043 | -0.0257484 | 0.315966 | 0.608527 | 0.608527 | 0.182716 |
| Information Services | 77 | 0.121921 | 0.233952 | 0.243352 | 0.203464 | 0.974619 | 1.00992 | 0.0569682 | 0.423733 | 0.02998 | 0.0856475 | 0.0539635 | 1.14155 | 10.5436 | 31.7026 | 44.4802 | 8.38306 | 71.13 | 0.0679032 | 0.0307393 | -0.00146836 | -0.0707527 | 0.143469 | 0.324139 | 0.324139 | 0.236107 |
| Insurance (General) | 21 | 0.0551221 | 0.128313 | 0.0925595 | 0.192993 | 0.558785 | 0.682338 | 0.0415063 | 0.30122 | 0.0258 | 0.289837 | 0.034935 | 0.819386 | 1.97274 | 9.98612 | 15.0082 | 1.44876 | 50.3628 | -0.154392 | 0.00775087 | -0.0316502 | -0.444707 | 0.0148801 | 1.92788 | 1.92788 | 0.129222 |
| Insurance (Life) | 26 | 0.0334505 | 0.0847795 | 0.043332 | 0.130036 | 0.64448 | 0.976417 | 0.0553869 | 0.306765 | 0.0258 | 0.545341 | 0.0354531 | 0.602094 | 1.31062 | 12.5091 | 15.0045 | 0.59088 | 28.986 | 0.0134644 | 0.00162369 | -0.00386064 | 0.0263748 | 0.056058 | 0.379548 | 0.379548 | 0.0847902 |
| Insurance (Prop/Cas.) | 55 | 0.0308551 | 0.108474 | 0.107373 | 0.194597 | 0.578196 | 0.643217 | 0.0396599 | 0.229341 | 0.0192 | 0.20036 | 0.0345219 | 1.10571 | 1.44422 | 9.68583 | 12.3319 | 1.54325 | 22.1233 | -0.528046 | 0.0106376 | 0.00365077 | 0.134654 | 0.0919365 | 0.383934 | 0.383934 | 0.108941 |
| Investments & Asset Management | 348 | 0.00650322 | 0.169491 | 0.0723546 | 0.185224 | 0.784933 | 0.929237 | 0.05316 | 0.28855 | 0.0258 | 0.31139 | 0.0424712 | 0.453071 | 5.87152 | 26.1717 | 30.5971 | 2.05016 | 625.406 | NA | 0.0291591 | 0.0530704 | 0.462278 | 0.123469 | 0.526966 | 0.526966 | 0.167447 |
| Machinery | 125 | 0.0343967 | 0.130748 | 0.214219 | 0.21031 | 0.957649 | 1.04794 | 0.0587626 | 0.342806 | 0.0258 | 0.164243 | 0.0522046 | 1.77869 | 3.06352 | 16.7024 | 23.0822 | 4.54672 | 46.0869 | 0.23307 | 0.0243721 | 0.0399401 | 0.206248 | 0.126481 | 0.453744 | 0.453744 | 0.132116 |
| Metals & Mining | 86 | 0.0401992 | 0.114651 | 0.107496 | 0.519839 | 0.819146 | 0.903723 | 0.0519557 | 0.678403 | 0.040925 | 0.192619 | 0.0477026 | 0.970985 | 2.99619 | 13.9012 | 25.9202 | 3.28651 | 44.4197 | 0.142954 | 0.0897604 | 0.0103253 | -0.0746088 | 0.0267374 | 1.97355 | 1.97355 | 0.112624 |
| Office Equipment & Services | 22 | 0.00783571 | 0.0750059 | 0.128391 | 0.239997 | 0.834309 | 1.0003 | 0.056514 | 0.311116 | 0.0258 | 0.323507 | 0.0443242 | 1.97211 | 1.11942 | 8.82047 | 14.7734 | 2.60212 | 33.0345 | 0.0665926 | 0.0281215 | 0.00369256 | -0.106605 | 0.0636277 | 0.917712 | 0.917712 | 0.0751081 |
| Oil/Gas (Integrated) | 3 | -0.0124 | -0.0427427 | -0.0233373 | 0.256274 | 0.987813 | 1.26061 | 0.068801 | 0.263884 | 0.0258 | 0.306011 | 0.0535105 | 0.644972 | 1.53542 | 10.7734 | NA | 1.049 | 52.4963 | 0.0538645 | 0.111034 | -0.0672501 | NA | -0.0618855 | 0.0447771 | 0.0447771 | -0.0395801 |
| Oil/Gas (Production and Exploration) | 278 | -0.0117097 | -0.213985 | -0.0632868 | 0.285947 | 0.810794 | 1.18339 | 0.065156 | 0.562763 | 0.02998 | 0.418864 | 0.0470315 | 0.307839 | 2.90751 | 6.39415 | NA | 1.20887 | 26.1344 | 0.0128957 | 0.388222 | -0.228472 | NA | -0.370856 | 0.0167726 | 0.0167726 | -0.206988 |
| Oil/Gas Distribution | 57 | 0.107407 | 0.174321 | 0.0901001 | 0.0874013 | 0.60255 | 1.15694 | 0.0639074 | 0.407778 | 0.02998 | 0.564637 | 0.0401802 | 0.543227 | 2.42487 | 9.12333 | 13.9457 | 1.24019 | 37.0828 | 0.0697281 | 0.134813 | 0.0501487 | 0.364771 | 0.0128078 | 0.0465929 | 0.0465929 | 0.173762 |
| Oilfield Svcs/Equip. | 135 | -0.068566 | 0.00474018 | 0.0129326 | 0.0436584 | 0.835147 | 1.20774 | 0.0663051 | 0.502675 | 0.02998 | 0.436421 | 0.0469194 | 1.88014 | 0.734258 | 11.3476 | 95.775 | 1.30324 | 31.7761 | 0.114068 | 0.0413991 | -0.000793931 | -0.398253 | -0.266309 | 0.00304158 | 0.00304158 | 0.00696364 |
| Packaging & Container | 26 | 0.0252242 | 0.096641 | 0.122487 | 0.253826 | 0.682343 | 0.921621 | 0.0528005 | 0.292155 | 0.0258 | 0.355304 | 0.0407321 | 1.47177 | 1.71698 | 10.3352 | 17.4786 | 3.7573 | 24.2523 | 0.0723061 | 0.0533905 | 0.0217766 | 0.227659 | 0.0975908 | 0.649447 | 0.649447 | 0.0986075 |
| Paper/Forest Products | 15 | 0.005061 | 0.0584319 | 0.0837734 | 0.210868 | 0.959188 | 1.13872 | 0.0630475 | 0.356696 | 0.0258 | 0.272856 | 0.0509836 | 1.48211 | 0.943691 | 7.70904 | 15.6451 | 1.60621 | 20.0468 | 0.154002 | 0.0385103 | -0.0028966 | -0.279113 | 0.0469452 | 1.17517 | 1.17517 | 0.0600846 |
| Power | 55 | 0.0101168 | 0.198205 | 0.0680221 | 0.110225 | 0.430899 | 0.666537 | 0.0407605 | 0.198599 | 0.0192 | 0.438461 | 0.0290341 | 0.38499 | 4.36548 | 11.886 | 22.2572 | 1.90135 | 21.9535 | 0.0257093 | 0.351073 | 0.205547 | 1.19534 | 0.0768682 | 0.875886 | 0.875886 | 0.196117 |
| Precious Metals | 93 | 0.0316509 | 0.214791 | 0.0987439 | 0.181321 | 0.752681 | 0.757222 | 0.0450409 | 0.677634 | 0.040925 | 0.112623 | 0.0433329 | 0.461318 | 4.81662 | 10.299 | 21.447 | 2.19162 | 86.4542 | 0.119929 | 0.129977 | -0.0818646 | -0.442238 | 0.0826992 | 0.31908 | 0.31908 | 0.216393 |
| Publishing & Newspapers | 29 | 0.00308118 | 0.056434 | 0.104819 | 0.237932 | 1.10589 | 1.40817 | 0.0757657 | 0.374695 | 0.0258 | 0.350657 | 0.0558022 | 2.09407 | 1.16724 | 9.76859 | 21.7646 | 2.07283 | 48.9363 | 0.115952 | 0.0269353 | 0.0056288 | -0.0491195 | -0.141845 | 0.00542554 | 0.00542554 | 0.0531337 |
| R.E.I.T. | 238 | 0.0680842 | 0.232332 | 0.0204935 | 0.0247422 | 0.794342 | 1.20588 | 0.0662175 | 0.324047 | 0.0258 | 0.434152 | 0.0456458 | 0.108943 | 12.8534 | 22.7172 | 61.4297 | 2.11475 | 62.9994 | 0.896502 | 0.0323838 | -0.153069 | -0.751258 | 0.0216914 | 4.30493 | 4.30493 | 0.190522 |
| Real Estate (Development) | 25 | -0.199248 | -0.0363845 | -0.0141334 | 0.273171 | 0.564116 | 0.848547 | 0.0493514 | 0.606959 | 0.02998 | 0.486386 | 0.0359923 | 0.217054 | 5.99743 | 47.5744 | NA | 1.18757 | 15.9556 | -0.0341292 | 0.338268 | 0.216903 | NA | -0.00129874 | 0 | 0 | -0.0670207 |
| Real Estate (General/Diversified) | 11 | 0.0920425 | 0.0693038 | 0.0195593 | 0.185 | 0.758866 | 0.780768 | 0.0461523 | 0.209932 | 0.0192 | 0.226119 | 0.0388857 | 0.331154 | 6.81446 | 25.2542 | 78.4013 | 1.18663 | 52.4131 | 3.01008 | 0.0257304 | -0.0299107 | 4.97444 | 0.0200175 | 0.676118 | 0.676118 | 0.0637428 |
| Real Estate (Operations & Services) | 61 | 0.0209512 | 0.0413141 | 0.0797113 | 0.104879 | 0.755881 | 0.920893 | 0.0527661 | 0.347217 | 0.0258 | 0.289724 | 0.0429352 | 2.04667 | 1.56205 | 14.8237 | 32.3081 | 3.21197 | 56.8281 | 0.140078 | 0.0121786 | -0.00635765 | -0.936778 | 0.0471333 | 0.39081 | 0.39081 | 0.0407084 |
| Recreation | 69 | 0.0262241 | 0.0681067 | 0.0865201 | 0.225577 | 0.774219 | 0.866605 | 0.0502038 | 0.563999 | 0.02998 | 0.196781 | 0.0446312 | 1.42457 | 3.73309 | 22.5932 | 52.0575 | 10.3705 | 155.394 | 0.15664 | 0.0456032 | 0.113778 | 2.0678 | -0.0719203 | 0.00708309 | 0.00708309 | 0.0644244 |
| Reinsurance | 2 | 0.0911 | 0.0426928 | 0.0374343 | 0.251445 | 1.1288 | 1.16255 | 0.0641725 | 0.252283 | 0.0258 | 0.278078 | 0.0515648 | 1.01724 | 0.807497 | 12.924 | 19.1842 | 0.749021 | 15.2006 | -0.0760276 | 0.00292025 | -0.00982347 | -0.171423 | 0.0241937 | 0.361495 | 0.361495 | 0.0420918 |
| Restaurant/Dining | 79 | 0.00836894 | 0.113621 | 0.0724012 | 0.186901 | 1.11094 | 1.3448 | 0.0727746 | 0.536255 | 0.02998 | 0.252059 | 0.0599475 | 1.1413 | 5.26809 | 23.5316 | 80.2486 | NA | 58.9132 | 0.0284498 | 0.0582228 | 0.0247139 | 0.487153 | NA | 1.14332 | 1.14332 | 0.0655293 |
| Retail (Automotive) | 30 | 0.0319788 | 0.0642896 | 0.101017 | 0.23182 | 0.989955 | 1.2983 | 0.0705798 | 0.428188 | 0.02998 | 0.332059 | 0.0544104 | 2.08549 | 1.23547 | 11.5629 | 19.837 | 5.98789 | 17.5209 | 0.10951 | 0.0181023 | 0.0172036 | -0.231608 | 0.362756 | 0.0372346 | 0.0372346 | 0.0548248 |
| Retail (Building Supply) | 15 | 0.0641692 | 0.127885 | 0.374737 | 0.239361 | 1.43645 | 1.54483 | 0.0822161 | 0.406039 | 0.02998 | 0.153146 | 0.0729767 | 3.46332 | 2.06223 | 12.5878 | 16.4928 | 40.0671 | 140.109 | 0.0445948 | 0.0206841 | 0.00202278 | -0.264541 | 0.00268658 | 0.455055 | 0.455055 | 0.125051 |
| Retail (Distributors) | 85 | 0.0467227 | 0.0769952 | 0.116738 | 0.250205 | 0.754493 | 0.970964 | 0.0551295 | 0.419743 | 0.02998 | 0.313831 | 0.0446965 | 1.6831 | 1.49397 | 13.8762 | 18.7788 | 3.38742 | 138.445 | 0.155371 | 0.0368184 | 0.0507805 | 0.631139 | 0.0967154 | 0.52366 | 0.52366 | 0.0790074 |
| Retail (General) | 17 | 0.0241214 | 0.0462957 | 0.146735 | 0.244202 | 0.815816 | 0.898978 | 0.0517318 | 0.389109 | 0.0258 | 0.175894 | 0.0459452 | 4.09728 | 0.934013 | 12.2943 | 22.8115 | 5.43461 | 22.7017 | 0.000580141 | 0.0200528 | 0.000228704 | -0.427998 | 0.206406 | 0.361199 | 0.361199 | 0.0409221 |
| Retail (Grocery and Food) | 14 | 0.0627857 | 0.0347794 | 0.0962799 | 0.234346 | 0.152225 | 0.242109 | 0.0207275 | 0.377189 | 0.0258 | 0.485438 | 0.0198083 | 4.11343 | 0.387768 | 5.7469 | 14.3095 | 2.50568 | 14.4135 | -0.0019838 | 0.0228822 | 0.0011047 | -0.147165 | 0.306265 | 0.128487 | 0.128487 | 0.0270664 |
| Retail (Online) | 75 | 0.0928341 | 0.0573728 | 0.110418 | 0.161296 | 1.13769 | 1.16412 | 0.0642465 | 0.528659 | 0.02998 | 0.066689 | 0.0614215 | 1.8008 | 4.70689 | 33.1863 | 83.8342 | 18.6244 | 131.273 | -0.0369773 | 0.0772451 | 0.0354515 | 0.553686 | 0.270546 | 0.0566067 | 0.0566067 | 0.0628529 |
| Retail (Special Lines) | 85 | 0.0557057 | 0.0289173 | 0.0528963 | 0.245527 | 1.03685 | 1.282 | 0.0698105 | 0.490095 | 0.02998 | 0.325504 | 0.0542107 | 2.29448 | 1.10054 | 11.3997 | 43.753 | 5.51344 | 55.9919 | 0.0474944 | 0.0178486 | 0.000504258 | -1.79339 | -0.00640358 | 0.00319609 | 0.00319609 | 0.025065 |
| Rubber& Tires | 3 | -0.0421333 | -0.0049665 | 0.000103801 | 0.159035 | 0.547996 | 1.09396 | 0.0609347 | 0.438272 | 0.02998 | 0.636234 | 0.0360902 | 1.06835 | 0.740633 | 9.84117 | NA | 1.04492 | 24.8928 | 0.136272 | 0.0562508 | -0.00532683 | NA | -0.256864 | 0.000675849 | 0.000675849 | 8.47115e-05 |
| Semiconductor | 70 | 0.0377052 | 0.240902 | 0.173907 | 0.107672 | 0.961703 | 1.00199 | 0.0565941 | 0.372553 | 0.0258 | 0.0885123 | 0.0532518 | 0.748002 | 7.15908 | 18.0434 | 29.3011 | 6.87472 | 726.522 | 0.174354 | 0.127613 | 0.160608 | 0.798328 | 0.221328 | 0.421019 | 0.421019 | 0.247927 |
| Semiconductor Equip | 40 | 0.084925 | 0.222144 | 0.278925 | 0.128325 | 1.06885 | 1.07038 | 0.059822 | 0.359055 | 0.0258 | 0.0743577 | 0.0567742 | 1.29552 | 5.14385 | 18.6927 | 22.8564 | 7.87179 | 55.871 | 0.278184 | 0.0371172 | 0.0116279 | 0.285944 | 0.322347 | 0.233087 | 0.233087 | 0.231832 |
| Shipbuilding & Marine | 11 | 0.0310143 | 0.0511134 | 0.0374141 | 0.243917 | 0.744116 | 1.03515 | 0.058159 | 0.298302 | 0.0258 | 0.383306 | 0.0430855 | 0.676179 | 1.73952 | 10.6683 | 30.644 | 1.13139 | 49.9872 | 0.0857237 | 0.0972849 | 0.0710075 | 1.24477 | -0.0569705 | 0.00156783 | 0.00156783 | 0.056632 |
| Shoe | 11 | -0.0011125 | 0.0921551 | 0.208959 | 0.13438 | 0.978275 | 0.983209 | 0.0557075 | 0.315049 | 0.0258 | 0.0642931 | 0.0533368 | 2.50472 | 5.04583 | 35.8329 | 56.488 | 14.87 | 46.1813 | 0.203827 | 0.00761791 | -0.0212546 | -0.306613 | 0.23701 | 0.482749 | 0.482749 | 0.0893454 |
| Software (Entertainment) | 101 | -0.00412905 | 0.206104 | 0.147335 | 0.120154 | 0.959545 | 0.958695 | 0.0545504 | 0.626141 | 0.02998 | 0.0254921 | 0.0537177 | 0.679622 | 8.16276 | 25.0901 | 38.0428 | 6.23326 | 157.385 | 0.0540582 | 0.140382 | 0.0993651 | 0.67796 | 0.177142 | 0.00263078 | 0.00263078 | 0.217939 |
| Software (Internet) | 36 | 0.19336 | 0.0505944 | 0.0665775 | 0.059714 | 0.748983 | 0.77313 | 0.0457917 | 0.327251 | 0.0258 | 0.0811457 | 0.0436042 | 1.0057 | 15.6705 | 19.2081 | 95.4389 | 15.1874 | 67.8886 | 0.10576 | 0.0789899 | 0.0695019 | 2.17239 | -0.112286 | 0.00178117 | 0.00178117 | 0.0677843 |
| Software (System & Application) | 388 | 0.189275 | 0.233043 | 0.222771 | 0.141353 | 0.894009 | 0.911687 | 0.0523316 | 0.479706 | 0.02998 | 0.061499 | 0.0504592 | 0.91831 | 11.8235 | 30.4238 | 43.935 | 14.0738 | 148.992 | 0.131485 | 0.0680368 | 0.055987 | 0.33689 | 0.28088 | 0.29354 | 0.29354 | 0.249038 |
| Steel | 32 | 0.00472318 | 0.0355326 | 0.0581002 | 0.245288 | 0.784841 | 0.952674 | 0.0542662 | 0.393192 | 0.0258 | 0.334402 | 0.0424176 | 1.70272 | 0.934815 | 9.739 | 23.0612 | 1.55285 | 35.7261 | 0.216911 | 0.0695824 | 0.0557344 | 0.284926 | -0.0284095 | 0.0064673 | 0.0064673 | 0.036302 |
| Telecom (Wireless) | 16 | 0.0652743 | 0.124817 | 0.102228 | 0.226455 | 0.392854 | 0.531014 | 0.0343639 | 0.397789 | 0.0258 | 0.353047 | 0.0288811 | 0.837351 | 3.67017 | 10.1412 | 29.5467 | 2.35559 | 24.6831 | 0.109924 | 0.153337 | 0.0351523 | 1.68195 | 0.089104 | 0.0303591 | 0.0303591 | 0.126519 |
| Telecom. Equipment | 96 | 0.316475 | 0.186873 | 0.217988 | 0.179024 | 0.83219 | 0.869374 | 0.0503344 | 0.431085 | 0.02998 | 0.128902 | 0.0466673 | 1.20251 | 3.56418 | 13.9222 | 18.524 | 4.83998 | 50.6781 | 0.168365 | 0.0294828 | 0.0334734 | 0.117145 | 0.171004 | 0.647071 | 0.647071 | 0.188558 |
| Telecom. Services | 58 | 0.0779096 | 0.194566 | 0.137778 | 0.167075 | 0.421809 | 0.659046 | 0.040407 | 0.435297 | 0.02998 | 0.453968 | 0.0319988 | 0.751889 | 2.50639 | 6.76123 | 13.1162 | 1.72882 | 22.2727 | 0.0118463 | 0.126273 | -0.0236472 | -0.0218788 | 0.112683 | 0.519192 | 0.519192 | 0.190731 |
| Tobacco | 15 | 0.528233 | 0.427991 | 0.453261 | 0.346661 | 0.612708 | 0.721841 | 0.0433709 | 0.244882 | 0.0192 | 0.23262 | 0.0365424 | 1.15673 | 4.81543 | 10.4829 | 11.2037 | NA | 54.6184 | 0.13101 | 0.0175434 | 0.0123872 | 0.00687049 | -0.00231081 | 1.64953 | 1.64953 | 0.429156 |
| Transportation | 21 | 0.0941608 | 0.0627678 | 0.133171 | 0.223659 | 0.786948 | 0.907385 | 0.0521286 | 0.286762 | 0.0258 | 0.240665 | 0.0441158 | 2.45157 | 1.55673 | 12.9595 | 25.627 | 6.77493 | 48.6059 | 0.0796931 | 0.0588128 | 0.0226288 | 0.68341 | 0.227679 | 0.554423 | 0.554423 | 0.0607319 |
| Transportation (Railroads) | 6 | -0.0147 | 0.39125 | 0.129678 | 0.23116 | 0.741134 | 0.844808 | 0.049175 | 0.16834 | 0.0192 | 0.183945 | 0.0427077 | 0.397017 | 8.09994 | 15.4581 | 20.9349 | 5.823 | 28.5508 | 0.016536 | 0.163567 | 0.0444704 | 0.128298 | 0.214746 | 0.410275 | 0.410275 | 0.386909 |
| Trucking | 35 | 0.0306421 | -0.0288225 | -0.0403566 | 0.216753 | 0.945991 | 1.11179 | 0.0617764 | 0.387838 | 0.0258 | 0.252378 | 0.0509387 | 0.836361 | 2.72924 | 10.0641 | NA | 4.81173 | 46.7383 | 0.0607238 | -0.00801258 | -0.0867077 | NA | -0.176956 | 0.00271007 | 0.00271007 | -0.0507321 |
| Utility (General) | 16 | 0.022685 | 0.204033 | 0.0678509 | 0.117172 | 0.485585 | 0.739778 | 0.0442175 | 0.184447 | 0.0192 | 0.427567 | 0.0313043 | 0.37307 | 4.13662 | 12.1518 | 20.5295 | 1.84043 | 18.7309 | 0.0901345 | 0.311465 | 0.198968 | 1.10396 | 0.0748571 | 1.00898 | 1.00898 | 0.201497 |
| Utility (Water) | 17 | 0.127391 | 0.304629 | 0.0805017 | 0.187485 | 0.572902 | 0.733968 | 0.0439433 | 0.359609 | 0.0258 | 0.288051 | 0.0367105 | 0.298736 | 9.78618 | 20.9249 | 32.1628 | 3.50739 | 62.3921 | 0.169492 | 0.472768 | 0.966202 | 3.94538 | 0.0824657 | 0.663664 | 0.713056 | 0.302089 |
| Total Market | 7582 | 0.0886044 | 0.0962017 | 0.0605061 | 0.177601 | 0.748151 | 0.941533 | 0.0537404 | 0.412054 | 0.02998 | 0.325808 | 0.0433618 | 0.66747 | 3.64625 | 20.0173 | 36.461 | 3.81385 | 103.246 | -0.361015 | 0.0559671 | 0.025665 | 0.331598 | 0.0824657 | 0.713056 | 0.713056 | 0.0960704 |
| Total Market (without financials) | 6253 | 0.0940412 | 0.0993009 | 0.105844 | 0.177434 | 0.861777 | 0.978306 | 0.055476 | 0.44773 | 0.02998 | 0.200663 | 0.0487356 | 1.11375 | 3.19696 | 16.521 | 30.6243 | 4.75011 | 87.0773 | 0.0828112 | 0.0591149 | 0.0253902 | 0.293989 | 0.0777509 | 0.839675 | 0.839675 | 0.0992975 |

**Outputs:** (sheet `FCFE Valuation`)

| Cell | Label | Example value | Meaning |
|---|---|---|---|
| D3 | Cost of Equity | 0.068 | high-growth CoE = rf + β·ERP |
| D4 | Net Income | 4096 | as input (or normalized) |
| D5 | Net Income without interest income from cash | 3964 | projection base |
| D6 | Growth rate in Net Income | 0.3560566 | high-growth g |
| D7 | Equity Reinvestment Rate, high growth | 0.6847370 | |
| Rows 11–17, cols C..Q | Year-by-year table (t = 1..n) | see below | growth, NI, ERR, FCFE, CoE, cumulative CoE, PV |
| D19 | Growth Rate in Stable Phase | 0.02 | |
| D20 | Equity Reinvestment rate in stable | 0.1333333 | |
| D21 | Cost of Equity in Stable Phase | 0.068 | |
| D22 | Price at the end of growth phase | 7039017.9361 | terminal equity value at year n |
| E24 | PV of FCFEs in high growth phase | 378283.9168 | |
| E25 | PV of Terminal Equity Value | 2623875.8446 | |
| E26 | Value of equity in operating assets | 3002159.7614 | E24 + E25 |
| E27 | Value of Cash and Marketable Securities | 2475 | added back |
| E28 | Value of equity in firm | 3004634.7614 | E26 + E27 |
| E29 | **Value per share** | **48.2874** | E28 / shares outstanding |

**Worked example:** (numbers currently in the sheet; currency in millions except per-share)

1. R&D: N = 5; R&D history (current, −1…−5) = 1771, 1678, 1529, 1367, 1267, 1205. Research asset = 1771 + 1678(0.8) + 1529(0.6) + 1367(0.4) + 1267(0.2) + 1205(0.0) = 4831. Amortization = (1678+1529+1367+1267+1205)/5 = 1409.2. NI adjustment = 1771 − 1409.2 = +361.8.
2. AdjNI = 4096 − 132 + 361.8 = 4325.8. Non-cash ROE = 4325.8 / (10237 − 1918) = 0.5199904.
3. Normalized reinvestment: NetCapEx = (2824.75/23883.75)·35872 = 4242.6098; ΔWC = (1748/263989)·(263989−213199) = 336.3054; NetDebt = [8293/(8293+12072)]·(4242.6098+336.3054) = 1864.6179.
4. ERR_hg = (4242.6098 + 336.3054 − 1864.6179)/(4096 − 132) = 2714.2973/3964 = 0.6847370.
5. g_hg = 0.6847370 × 0.5199904 = 0.3560566. CoE = 0.02 + 0.8(0.06) = 0.068 (both phases; stable beta also 0.8).
6. Projection base NI = 3964. Year 1: NI = 5375.4085, FCFE = 5375.4085 × (1−0.6847370) = 1694.6677, PV = 1694.6677/1.068 = 1586.7675. Year 10: NI = 83351.2105, FCFE = 26277.5566, PV = 13610.4490. Year 11 (sheet bug branch): FCFE = 113028.9617 × 0.6847370 = 77395.1068, PV = 37534.4213. Year 15: NI = 382209.1187, FCFE = 261712.7072, PV = 97556.4570.
7. Stable: ERR_st = 0.02/0.15 = 0.1333333. TV = 382209.1187 × 1.02 × (1−0.1333333)/(0.068−0.02) = 7039017.9361. PV(TV) = 7039017.9361/1.068^15 = 7039017.9361/2.6826795 = 2623875.8446.
8. Σ PV(FCFE, yrs 1–15) = 378283.9168. Equity (operating) = 3002159.7614; + cash 2475 = 3004634.7614; ÷ 62224 shares = **48.2874 per share**.

**Reimplementation:** what a Python port needs.

*Inputs* (name: type, units):
- net_income: float, currency; interest_income_after_tax: float, currency (last year's, on cash); bv_equity_current, bv_equity_prior: float; cash_current, cash_prior: float; mv_equity: float (helper only); shares_outstanding: float; capex, depreciation: float; change_wc: float; net_debt_issued: float (negative = repaid).
- capitalize_rnd: bool; rnd_amort_years: int 1–10; rnd_current: float; rnd_history: list[float] length = amort_years (year −1 first).
- normalize_income: bool + (approach: 1|2, ni_history: list[float] up to 5, normalized_roe: float).
- normalize_reinvestment: bool + (capex_approach: 1|2, netcapex_history/ebit_history: list[float], ebit_current: float, industry_netcapex_to_ebit: float; wc_approach: 1|2, wc_current, rev_current, rev_prior: float, industry_wc_to_rev: float; debt_approach: 1|2, book_debt: float, industry_debt_ratio: float).
- beta, riskfree, erp: float (decimals); growth_years: int 0–15; growth_from_fundamentals: bool; growth_override: float; hg_override: bool + roe_hg_override, err_hg_override; stable_roe: float (default 0.15); adjust_second_half: bool (3-stage flag); g_stable: float; stable_err_override: Optional[float]; beta_changes: bool + stable_beta: float.

*Core computation* (see Logic for exact formulas): rnd_adjustment → adj_ni → roe_hg → err_hg → g_hg → project NI from base = (normalized NI if normalize_income else NI) − interest_income → FCFE_t → discount at CoE → TV → value per share.

*Branches:*
- capitalize_rnd False ⇒ rnd_adjustment = 0.
- normalize_income / normalize_reinvestment switch component sources (see Steps 4–5); each normalization block has its own approach-1/approach-2 branch.
- growth_from_fundamentals False ⇒ g_hg = growth_override (ERR_hg still computed and still used for FCFE).
- hg_override True ⇒ replace computed ROE_hg/ERR_hg with the overrides.
- growth_years = 0 ⇒ stable-growth-only: value = NI_base × (1+g_st) × (1−ERR_st)/(CoE_st − g_st) + cash, then ÷ shares (inferred from the Read-me; not exercised in the workbook).
- adjust_second_half True ⇒ 3-stage: for t in the second half of the growth period, linearly interpolate g, ERR, and CoE from high-growth values to stable values. This branch is inferred from the Read-me and is not exercised in the workbook. Verify the exact ramp conventions against a live run before trusting them.
- beta_changes ⇒ CoE_stable uses stable_beta; else the high-growth beta.
- stable ERR = g_stable/stable_roe unless stable_err_override given.

*Edge cases and pitfalls:*
- **Sheet bug to decide on:** for growth periods longer than 10 years, years 11+ use FCFE = NI × ERR instead of NI × (1−ERR) (verified exact). Port both modes: `faithful=True` reproduces the sheet; `faithful=False` computes FCFE = NI × (1−ERR) for all years. With the example inputs the faithful value/share is 48.2874; the corrected FCFE stream would be far lower for years 11–15.
- Denominator inconsistency (replicate as-is): ROE_hg numerator includes the R&D adjustment, but the ERR_hg denominator and the projection base (NI − interest income) do not.
- ROE_hg uses beginning-of-period book equity net of cash and does NOT add the research asset to the denominator.
- Negative or zero denominators: NI − interest_income ≤ 0 makes ERR/growth meaningless (sheet would produce nonsense; a port should raise or require normalization). (bv_equity_prior − cash_prior) ≤ 0 breaks ROE. CoE_stable ≤ g_stable makes TV negative/infinite — validate.
- ERR > 1 ⇒ negative FCFE (allowed; equity issuance implied). Negative net_debt_issued raises equity reinvestment.
- The average in Normalized Earnings/Reinvestment ignores blank cells (Excel AVERAGE semantics), so fewer than 5 populated years just average what's there.
- growth_years is capped at 15 by the sheet layout (columns C..Q).
- Cash added back is the *current* cash balance; interest income is stripped from earnings to avoid double counting.
- Helper sheets (`Beta calculator`, `ERP calculator`) are standalone: their outputs must be manually copied into beta/ERP inputs.
- Units: all rates as decimals; monetary inputs in a consistent currency unit; per-share output = equity value / shares in the same share units.

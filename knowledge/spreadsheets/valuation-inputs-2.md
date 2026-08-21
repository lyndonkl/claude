# Valuation Inputs Spreadsheets — Batch 2 (Damodaran 2020 archive)

Files covered: `R&DConv.xls`, `cpxest.xls`, `readme1s.xls` (all legacy .xls — dumps show computed values only; all formula logic below reconstructed from labels/values and flagged "(inferred)" where not directly verifiable).

---

### R&DConv.xls — R&D Converter (R&D capitalizer)

**Purpose:** Converts R&D expense from an operating expense to a capital expense (capitalizes the "research asset"). Damodaran uses this whenever valuing firms with significant R&D (tech, pharma) so that operating income, net income, book value of capital/equity, cap ex, depreciation, and return on capital reflect R&D as an investment rather than an expense. The sheet notes it can also be used to capitalize other intangibles (e.g. human-capital / training expenses, advertising for brand names) by the same mechanics.

Three sheets: `Inputs`, `R&D capitalizer` (output), `Amortizable Lives Look-up Table` (reference).

**Inputs** (sheet `Inputs`; all currency figures in same units, here $ millions):

| Label | Cell | Example value |
|---|---|---|
| Pre-tax Operating income (EBIT), current year | B8 | 3195 |
| Tax rate | B9 | 0.40 |
| Net Income, current year | B10 | 1025 |
| Book value of capital, current year | B11 | 5256 |
| Capital expenditures, current year | B12 | 655 |
| Depreciation & Amortization, current year | B13 | 525 |
| Amortization period for R&D, years (`N`) | F15 | 5 |
| Current year's R&D expense | F16 | 1594 |
| R&D expense, year −1 | B20 | 1026 |
| R&D expense, year −2 | B21 | 698 |
| R&D expense, year −3 | B22 | 399 |
| R&D expense, year −4 | B23 | 211 |
| R&D expense, year −5 | B24 | 89 |

The user must enter past R&D for exactly `N` prior years (rows below the horizon stay 0). Column A (Year: −1, −2, … −N) auto-fills from `N` (inferred); the sheet says "Do not input numbers in the first column". Input rows A20:B39 allow up to 20 past years, so N can be up to 20 (inferred from layout).

**Logic** (sheet `R&D capitalizer`, straight-line amortization; all formulas inferred from values):

For each year t = 0 (current), −1, −2, … −N, with R&D expense `RD_t` and amortization life `N`:

1. Unamortized portion (fraction), col C: `unam_frac_t = max(0, 1 − |t|/N)` — current year = 1.0, year −1 = (N−1)/N, …, year −N = 0.
2. Unamortized value, col D: `unam_t = RD_t × unam_frac_t`
3. Amortization this year, col E: `amort_t = RD_t / N` for past years (t = −1 … −N); `amort_0 = 0` (current year's R&D is not amortized in the current year).
4. Value of Research Asset (D24): `RA = Σ unam_t` over t = 0 … −N.
5. Total amortization of research asset this year (E24, echoed in D27): `AM = Σ amort_t = Σ_{t=-1}^{-N} RD_t / N`.
6. Expenditure on asset in current year (D26): `= RD_0`.

Adjusted ("With capitalizing") financials, rows 30–36 (col B = unadjusted input, col C = adjusted):

- Operating income: `EBIT_adj = EBIT + RD_0 − AM` (C30)
- Operating income after taxes: `EBIT_adj_AT = EBIT×(1−tax) + RD_0 − AM` (C31). Note: the R&D add-back is NOT tax-effected — the firm already got the tax deduction for expensing R&D, so only the pre-tax EBIT is multiplied by (1−t). Equivalently C31 = B31 + RD_0 − AM.
- Net Income: `NI_adj = NI + RD_0 − AM` (C32)
- Book value of capital: `BV_adj = BV + RA` (C33). (The same adjustment applies to book equity — RA is added to book equity too, per the sheet's stated purpose.)
- Return on capital: `ROC = after-tax operating income / BV of capital`, i.e. B34 `= B31/B33`, C34 `= C31/C33` (beginning-of-period BV as entered).
- Capital expenditures: `CapEx_adj = CapEx + RD_0` (C35)
- Depreciation & Amortization: `DA_adj = DA + AM` (C36)

**Reference data** (sheet `Amortizable Lives Look-up Table`) — guidance for choosing `N` by industry. Guideline categories (cells D3:F8):

| Firm type | Amortization period |
|---|---|
| Non-technological Service | 2 years |
| Retail, Tech Service | 3 years |
| Light Manufacturing | 5 years |
| Heavy Manufacturing | 10 years |
| Research, with Patenting | 10 years |
| Long Gestation Period | 10 years |

Industry table (A2:B99), verbatim:

| Industry Name | Amortization Period (yrs) |
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

**Outputs** (sheet `R&D capitalizer`):

| Cell | Meaning | Example value |
|---|---|---|
| D24 | Value of Research Asset (add to book capital and book equity) | 3035.4 |
| E24 / D27 | Amortization of research asset, current year | 484.6 |
| D26 | Expenditure on research asset, current year (= current R&D) | 1594 |
| C30 | Adjusted operating income (EBIT) | 4304.4 |
| C31 | Adjusted after-tax operating income | 3026.4 |
| C32 | Adjusted net income | 2134.4 |
| C33 | Adjusted book value of capital | 8291.4 |
| C34 | Adjusted return on capital | 0.36500 (36.50%) |
| C35 | Adjusted capital expenditures | 2249 |
| C36 | Adjusted depreciation & amortization | 1009.6 |
| B30–B36 | Same items without capitalizing (echo of inputs; B31 = EBIT×(1−t) = 1917; B34 = 1917/5256 = 0.36473) | — |

**Worked example** (values in sheet; N = 5):

| Year | R&D | Unamortized frac | Unamortized value | Amortization this yr |
|---|---|---|---|---|
| 0 (current) | 1594 | 1.0 | 1594.0 | 0 |
| −1 | 1026 | 0.8 | 820.8 | 205.2 |
| −2 | 698 | 0.6 | 418.8 | 139.6 |
| −3 | 399 | 0.4 | 159.6 | 79.8 |
| −4 | 211 | 0.2 | 42.2 | 42.2 |
| −5 | 89 | 0.0 | 0.0 | 17.8 |
| **Sum** | | | **RA = 3035.4** | **AM = 484.6** |

- EBIT_adj = 3195 + 1594 − 484.6 = 4304.4
- After-tax: 3195×0.6 + 1594 − 484.6 = 1917 + 1109.4 = 3026.4
- NI_adj = 1025 + 1109.4 = 2134.4
- BV_adj = 5256 + 3035.4 = 8291.4
- ROC: without = 1917/5256 = 36.47%; with = 3026.4/8291.4 = 36.50%
- CapEx_adj = 655 + 1594 = 2249; D&A_adj = 525 + 484.6 = 1009.6

**Reimplementation:**

- Inputs: `ebit` (float, currency), `tax_rate` (float 0–1), `net_income` (float), `book_capital` (float), `capex` (float), `depreciation` (float), `amort_years N` (int ≥ 1), `rd_current` (float), `rd_past` (list of floats, length N, ordered year −1 … −N).
- Outputs: `research_asset`, `amortization_current`, and dict of adjusted vs unadjusted {ebit, ebit_after_tax, net_income, book_capital, roc, capex, depreciation}.
- Branches/edge cases:
  - `len(rd_past)` must equal N; pad with 0 if fewer years of history exist (the sheet uses 0 for missing years, which understates RA — flag as data-quality warning).
  - N = 1 degenerate case: RA = rd_current only; year −1's R&D fully amortized.
  - Unamortized fraction for year −k is `(N−k)/N`; year −N contributes 0 to RA but `RD_{−N}/N` to amortization — do not drop it.
  - ROC divides by book capital: guard `book_capital ≤ 0` and `book_capital + RA = 0`.
  - Do NOT tax-effect the (R&D − amortization) adjustment to after-tax income — a common porting mistake.
  - Adjustment can lower income if AM > rd_current (declining R&D spender) — allowed, not an error.
  - Optional helper: industry → amortization-period lookup from the table above (exact string match on Value Line industry names).

---

### cpxest.xls — Capital Expenditure Estimation (stable growth)

**Purpose:** A guide-plus-calculator for estimating net capital expenditures (and change in working capital) in a DCF's stable-growth phase. Presents Damodaran's three approaches and computes Approach 3's reinvestment rate from the stable growth rate and return on capital. Also carries a reference table of cap-ex/depreciation and net-capex ratios by sector (Value Line sectors, late-1990s data). Only `Sheet1` has content; Sheet2–Sheet16 are empty stubs.

**Inputs** (Sheet1):

| Label | Cell | Example value |
|---|---|---|
| Expected Growth Rate in Operating Income (stable, g) | D18 | 0.05 |
| Expected Return on Capital (ROC) | D19 | 0.15 |

**Logic:**

Three documented approaches (text in rows 1–16):

1. **Approach 1 — Net Cap Ex = 0** (Cap Ex = 100% of Depreciation). Most common in stable growth; the sheet warns it is "the most dangerous" combined with positive growth, and defensible only when stable growth ≈ 0.
2. **Approach 2 — Industry average ratios.** Set the firm's CapEx/Depreciation (or Net CapEx/Sales, or Net CapEx/EBIT(1−t)) to the sector average from Table 1 below.
3. **Approach 3 — Fundamental (growth/ROC).** The only computed cell:
   - F20: `reinvestment_rate = g / ROC` (inferred; 0.05/0.15 = 0.33333 matches). Label: "Expected Net Capital Ex and Chg in WC as % of after-tax EBIT".
   - G20 annotation restates it as "(Cap Ex = 133.33 Deprec'n − Change in WC)" — i.e. for this example the implied gross CapEx is 133.33% of depreciation net of the WC change (inferred: NetCapEx + ΔWC = 0.3333 × EBIT(1−t)).
   - Usage per rows 21–24: reinvestment for the next year = reinvestment_rate × current after-tax EBIT. The sheet's example: after-tax EBIT in year 5 = $100m, g = 5%. Net Cap Ex + ΔWC in year 6 = 0.3333 × 100 = $33.33m. Note the sheet applies the rate to year-5 EBIT(1−t) directly, without growing it first.

**Reference data** — Table 1: Cap Expenditure/Depreciation Ratios by Sector (rows 27–117). Depreciation and Cap Ex are per-firm sector averages in $ millions; ratios are unitless. Verbatim (ratios rounded to 4 decimals, $ to 2):

| Industry | Depreciation | Cap Ex | Cap Ex/Deprec'n | Net CapEx/Sales | Net CapEx/EBIT(1-t) |
|---|---|---|---|---|---|
| Advertising | 39.51 | 31.13 | 0.7881 | -0.0092 | -0.0982 |
| Aerospace/Defense | 101.56 | 90.23 | 0.8885 | -0.0036 | -0.0390 |
| Air Transport | 179.56 | 264.82 | 1.4748 | 0.0240 | 0.2483 |
| Aluminum | 196.02 | 254.49 | 1.2983 | 0.0155 | 0.1490 |
| Apparel | 13.74 | 13.78 | 1.0033 | 0.0001 | 0.0011 |
| Auto & Truck | 2134.54 | 2387.37 | 1.1184 | 0.0079 | 0.0734 |
| Auto Parts (OEM) | 80.54 | 99.37 | 1.2339 | 0.0083 | 0.1136 |
| Auto Parts (Replacement) | 26.90 | 38.70 | 1.4385 | 0.0123 | 0.1686 |
| Beverage (Alcoholic) | 69.67 | 116.23 | 1.6683 | 0.0242 | 0.2375 |
| Beverage (Soft Drink) | 305.78 | 405.59 | 1.3264 | 0.0159 | 0.1314 |
| Building Materials | 25.47 | 47.23 | 1.8543 | 0.0201 | 0.2903 |
| Cable TV | 184.31 | 240.12 | 1.3028 | 0.0564 | 0.2116 |
| Canadian Energy | 277.27 | 441.82 | 1.5935 | 0.0646 | 0.4071 |
| Cement & Aggregates | 27.00 | 38.78 | 1.4366 | 0.0248 | 0.1724 |
| Chemical (Basic) | 324.22 | 435.46 | 1.3431 | 0.0195 | 0.1031 |
| Chemical (Diversified) | 215.83 | 338.22 | 1.5671 | 0.0346 | 0.2886 |
| Chemical (Specialty) | 37.88 | 56.50 | 1.4916 | 0.0226 | 0.1942 |
| Coal/Alternate Energy | 42.10 | 154.08 | 3.6602 | 0.2027 | 0.4968 |
| Computer & Peripherals | 73.75 | 95.71 | 1.2978 | 0.0118 | 0.1109 |
| Computer Software & Svcs | 30.49 | 35.05 | 1.1494 | 0.0105 | 0.0615 |
| Copper | 173.80 | 307.86 | 1.7713 | 0.0653 | 0.3668 |
| Diversified Co. | 56.74 | 67.80 | 1.1951 | 0.0064 | 0.0787 |
| Drug | 45.95 | 49.58 | 1.0791 | 0.0046 | 0.0199 |
| Drugstore | 43.09 | 94.31 | 2.1890 | 0.0163 | 0.3857 |
| Electric Util. (Central) | 206.01 | 202.30 | 0.9820 | -0.0018 | -0.0087 |
| Electric Utility (East) | 283.37 | 255.83 | 0.9028 | -0.0104 | -0.0488 |
| Electric Utility (West) | 256.51 | 264.99 | 1.0331 | 0.0037 | 0.0157 |
| Electrical Equipment | 84.06 | 110.36 | 1.3129 | 0.0092 | 0.0785 |
| Electronics | 16.77 | 27.40 | 1.6338 | 0.0225 | 0.2630 |
| Entertainment | 89.29 | 91.76 | 1.0276 | 0.0018 | 0.0186 |
| Environmental | 47.65 | 54.55 | 1.1447 | 0.0114 | 0.0662 |
| Financial Services | 23.34 | 32.66 | 1.3994 | 0.0101 | 0.0513 |
| Food Processing | 99.68 | 130.80 | 1.3122 | 0.0090 | 0.1151 |
| Food Wholesalers | 78.06 | 130.31 | 1.6694 | 0.0088 | 0.3649 |
| Foreign Diversified | 786.84 | 698.36 | 0.8876 | -0.0046 | -0.0332 |
| Foreign Electron/Entertn | 1225.30 | 1596.37 | 1.3028 | 0.0118 | 0.2059 |
| Foreign Telecom. | 1054.72 | 977.78 | 0.9271 | -0.0070 | -0.0325 |
| Furn./Home Furnishings | 19.00 | 20.34 | 1.0706 | 0.0020 | 0.0263 |
| Gold/Silver Mining | 33.58 | 69.08 | 2.0568 | 0.1211 | 0.5773 |
| Grocery | 91.33 | 162.13 | 1.7753 | 0.0147 | 0.3694 |
| Healthcare Info Systems | 21.39 | 14.91 | 0.6972 | -0.0142 | -0.1018 |
| Home Appliance | 54.93 | 63.79 | 1.1613 | 0.0059 | 0.0860 |
| Homebuilding | 9.12 | 11.53 | 1.2635 | 0.0046 | 0.0608 |
| Hotel/Gaming | 33.19 | 103.42 | 3.1162 | 0.0989 | 0.7655 |
| Household Products | 116.57 | 160.57 | 1.3775 | 0.0151 | 0.1193 |
| Industrial Services | 13.13 | 16.69 | 1.2710 | 0.0069 | 0.1024 |
| Insurance (Diversified) | 5.79 | 24.06 | 4.1567 | 0.0207 | 0.1013 |
| Insurance (Life) | 1.23 | 5.10 | 4.1628 | 0.0006 | 0.0080 |
| Investment Co. (Domestic) | 0.41 | 0.70 | 1.7059 | 0.0040 | 0.0266 |
| Investment Co. (Foreign) | 2.19 | 3.24 | 1.4797 | 0.0076 | 0.0216 |
| Machinery | 28.61 | 36.75 | 1.2843 | 0.0084 | 0.0935 |
| Manuf. Housing/Rec Veh | 7.55 | 15.31 | 2.0268 | 0.0129 | 0.2263 |
| Maritime | 34.43 | 70.60 | 2.0506 | 0.0693 | 0.5726 |
| Medical Services | 28.48 | 33.24 | 1.1668 | 0.0051 | 0.0566 |
| Medical Supplies | 21.39 | 28.40 | 1.3279 | 0.0099 | 0.1044 |
| Metal Fabricating | 17.55 | 25.52 | 1.4541 | 0.0140 | 0.1469 |
| Metals & Mining (Div.) | 97.29 | 194.15 | 1.9956 | 0.0663 | 0.5073 |
| Natural Gas (Distrib.) | 82.19 | 120.41 | 1.4649 | 0.0389 | 0.2489 |
| Natural Gas (Diversified) | 115.80 | 206.80 | 1.7859 | 0.0474 | 0.3527 |
| Newspaper | 134.21 | 117.09 | 0.8725 | -0.0070 | -0.0607 |
| Office Equip & Supplies | 59.79 | 67.93 | 1.1362 | 0.0039 | 0.0482 |
| Oilfield Services/Equip. | 56.40 | 88.89 | 1.5762 | 0.0351 | 0.2746 |
| Packaging & Container | 48.88 | 71.74 | 1.4677 | 0.0236 | 0.2221 |
| Paper & Forest Products | 126.99 | 189.64 | 1.4934 | 0.0303 | 0.2784 |
| Petroleum (Integrated) | 1073.78 | 1662.54 | 1.5483 | 0.0286 | 0.2535 |
| Petroleum (Producing) | 48.11 | 91.14 | 1.8944 | 0.1275 | 0.4887 |
| Precision Instrument | 19.88 | 27.80 | 1.3988 | 0.0178 | 0.1495 |
| Publishing | 52.42 | 46.66 | 0.8901 | -0.0062 | -0.0570 |
| R.E.I.T. | 1.83 | 6.56 | 3.5840 | 0.0049 | 0.0193 |
| Railroad | 247.24 | 513.68 | 2.0777 | 0.0842 | 0.4799 |
| Recreation | 21.55 | 41.19 | 1.9114 | 0.0483 | 0.3938 |
| Restaurant | 26.28 | 71.58 | 2.7233 | 0.0861 | 0.6376 |
| Retail (Special Lines) | 19.64 | 31.90 | 1.6242 | 0.0126 | 0.2300 |
| Retail Building Supply | 40.21 | 159.06 | 3.9561 | 0.0392 | 0.7107 |
| Retail Store | 121.82 | 191.71 | 1.5737 | 0.0107 | 0.1996 |
| Securities Brokerage | 36.60 | 39.59 | 1.0816 | 0.0012 | 0.0031 |
| Semiconductor | 127.83 | 237.87 | 1.8608 | 0.0731 | 0.3813 |
| Semiconductor Cap Equip | 35.74 | 89.26 | 2.4975 | 0.0599 | 0.3429 |
| Shoe | 12.62 | 25.55 | 2.0252 | 0.0162 | 0.1949 |
| Steel (General) | 29.00 | 69.67 | 2.4021 | 0.0483 | 0.6373 |
| Steel (Integrated) | 159.19 | 240.39 | 1.5101 | 0.0433 | 0.5870 |
| Telecom. Equipment | 26.88 | 35.25 | 1.3112 | 0.0132 | 0.1656 |
| Telecom. Services | 273.95 | 393.14 | 1.4351 | 0.0520 | 0.2057 |
| Textile | 26.86 | 32.63 | 1.2151 | 0.0088 | 0.1187 |
| Tire & Rubber | 97.44 | 158.36 | 1.6251 | 0.0200 | 0.2394 |
| Tobacco | 348.25 | 330.00 | 0.9476 | -0.0012 | -0.0107 |
| Toiletries/Cosmetics | 31.41 | 53.58 | 1.7055 | 0.0202 | 0.1836 |
| Trucking/Transp. Leasing | 55.87 | 99.66 | 1.7837 | 0.0517 | 0.5888 |
| Utility (Foreign) | 1945.99 | 4154.35 | 2.1348 | 0.2618 | 0.8178 |
| Water Utility | 21.43 | 51.39 | 2.3978 | 0.1664 | 0.6616 |

Consistency check on the table (inferred relationships): `Cap Ex/Deprec'n = CapEx / Depreciation` holds exactly for every row; Net CapEx = CapEx − Depreciation; the /Sales and /EBIT(1−t) denominators are not in the sheet (sector aggregates used in Damodaran's dataset). Negative Net CapEx ratios occur where sector CapEx < Depreciation.

**Outputs:**

| Cell | Meaning | Example value |
|---|---|---|
| F20 | Reinvestment rate: (Net Cap Ex + ΔWC) as fraction of after-tax operating income = g / ROC | 0.3333 |

**Worked example:** g = 5%, ROC = 15% ⇒ reinvestment rate = 0.05/0.15 = 33.33%. Sheet's own example: after-tax EBIT year 5 = $100m ⇒ Net Cap Ex + ΔWC in year 6 = 0.3333 × $100m = $33.33m.

**Reimplementation:**

- Core function: `stable_reinvestment_rate(g: float, roc: float) -> float` returning `g / roc`. Guard `roc <= 0` (undefined — raise or return None) and `g > roc` (rate > 1, meaning reinvestment exceeds after-tax operating income — warn). `g = 0` ⇒ rate 0 (Approach 1's zero-net-capex case is then internally consistent).
- Then `reinvestment = rate × ebit_after_tax` for the stable year.
- Alternative estimators (Approach 2): expose the sector table as a lookup (`capex = ratio × depreciation`, or `net_capex = ratio × sales`, or `net_capex = ratio × ebit_after_tax`), keyed by exact sector name. Note this table has 90 sectors and its own name set (includes 'Foreign Diversified', 'Insurance (Diversified)', etc.; lacks some names present in the R&DConv lookup) — do not assume the two industry lists are identical.
- Data is late-1990s vintage; treat as illustrative defaults, refreshable from Damodaran's current datasets.

---

### readme1s.xls — Readme / model-selection guide

**Purpose:** Documentation sheet for the original valuation-spreadsheet diskette accompanying Damodaran's valuation book. No calculations. Contains (a) usage notes, (b) a model-choice decision table mapping firm characteristics to the right DCF/option model, and (c) a file index mapping spreadsheet filenames to models. Useful to the knowledge base as the routing logic for which valuation model to apply.

**Inputs:** None (pure documentation; single sheet `Readme1st`).

**Logic:** The model-choice table is a rule table: match a firm on six characteristics → recommended model. (This is the same logic implemented interactively in `model.xls` / MODELCHO.) Decision dimensions: earnings sign; earnings normalcy (Normal / Abnormal / Cyclical / Troubled / Start-up); growth (Stable / Moderate / High); source of growth (General / Specific / Either); Dividends vs FCFE (=FCFE / ≠FCFE); leverage (Stable / Unstable); other factors.

**Reference data** — Model choice table (A47:H65), verbatim:

| Earnings sign | Normalcy | Growth | Source of g | Dividends vs FCFE | Leverage | Other factors | Valuation Model |
|---|---|---|---|---|---|---|---|
| +'ve | Normal | Stable | NA | =FCFE | Stable | NA | Gordon Growth |
| +'ve | Normal | Stable | NA | ≠FCFE | Stable | NA | FCFE Stable |
| +'ve | Normal | Stable | NA | NA | Unstable | NA | FCFF Stable |
| +'ve | Normal | Moderate | General | =FCFE | Stable | NA | H Model |
| +'ve | Normal | Moderate | Specific | =FCFE | Stable | NA | 2 stage DDM |
| +'ve | Normal | Moderate | Specific | ≠FCFE | Stable | NA | 2 stage FCFE |
| +'ve | Normal | Moderate | Either | NA | Unstable | NA | 2 stage FCFF |
| +'ve | Normal | High | Either | =FCFE | Stable | NA | 3 stage DDM |
| +'ve | Normal | High | Either | ≠FCFE | Stable | NA | 3 stage FCFE |
| +'ve | Normal | High | Either | NA | Unstable | NA | 3 stage FCFF |
| +'ve | Abnormal | NA | NA | NA | Stable | NA | Normalized EPS |
| +'ve | Abnormal ("Abnomal" sic) | NA | NA | NA | Unstable | NA | Normalized FCFF |
| -'ve | Cyclical | NA | NA | NA | Stable | NA | Normalized EPS |
| -'ve | Cyclical | NA | NA | NA | Unstable | NA | Normalized FCFF |
| -'ve | Troubled | NA | NA | NA | Either | Turn around | FCFF Model |
| -'ve | Troubled | NA | NA | NA | Either | Bankruptcy | Option Model |
| -'ve | Start-up | NA | NA | NA | Either | Many lines | FCFF Model |
| -'ve | Start-up | NA | NA | NA | Either | Single line | Option Model |

(NA = Not Applicable.)

File index (A69:D86) — Expanded vs Simple filenames:

| Expanded file | Simple file | Model |
|---|---|---|
| MODELCHO.* | — | Model Choice |
| NEWGORDO.* | — | Gordon Growth Model |
| NEWDDM2S.* | XDDM2.* | Two-Stage DDM |
| NEWDDMHM.* | XDDMH.* | The H Model |
| NEWDDM3S.* | — | Three-Stage DDM |
| NEWFCFES.* | — | FCFE Stable Growth Model |
| NEWFCFE2.* | XFCFE2.* | Two-Stage FCFE Model |
| NEWFCFE3.* | — | Three-Stage FCFE Model |
| NEWFCFF2.* | XFCFF2.* | Two-Stage FCFF Model |
| DETAILVA.* | — | General FCFF Model |
| NEWNORME.* | — | Normalized EPS Model |
| — | XEQUITYM.* | Multiples for Equity |
| — | XMULTCF.* | Multiples for firm |
| NEWRESTR.* | — | Corporate Restructuring |
| EQUITYOP.* | — | Equity as an Option |
| NEWPRODU.* | — | Natural Resource Option (label likely swapped with next row — NEWPRODU = Product Option, NEWNATRE = Natural Resource, inferred from filenames) |
| NEWNATRE.* | — | Product Option (see note above) |

Other content: requirements note (Lotus 3.x / Excel 4), three program groups (I. DCF: DDM/FCFE/FCFF variants; II. Relative valuation: PE/PBV/PS multiples; III. Option pricing: equity as option, product patents/start-ups, natural-resource firms), and usage sequence (run MODELCHO first if unsure, enter inputs in requested units, check warning page, then output page). Simple versions require fewer inputs but allow fewer options.

**Outputs:** None.

**Worked example:** N/A (no computation). Routing example: positive normal earnings, high growth, dividends ≠ FCFE, stable leverage → 3-stage FCFE model.

**Reimplementation:** Implement the model-choice table as a rule-matching function: inputs `earnings_sign` ("positive"/"negative"), `normalcy` ("normal"/"abnormal"/"cyclical"/"troubled"/"startup"), `growth` ("stable"/"moderate"/"high"), `growth_source` ("general"/"specific"), `dividends_equal_fcfe` (bool), `leverage_stable` (bool), `other` ("turnaround"/"bankruptcy"/"many_lines"/"single_line"/None); output: model name string. Match rules top-down; "NA"/"Either" fields are wildcards. Edge cases: negative earnings routes on normalcy + other factors, not growth; unstable leverage always pushes toward FCFF variants; no rule covers negative + normal (treat as troubled/cyclical prompt).

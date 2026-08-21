# ginzu-fcff-lambda

### fcffginzulambda.xls

**Source:** `/Users/kushaldsouza/Downloads/2020/Spreadsheets/Big Picture Valuation Spreadsheets/fcffginzulambda.xls` (.xls — values only; all formulas below are reconstructed from labels/values and verified numerically against the sheet unless marked otherwise; anything not verified is flagged "(inferred)").

**Purpose:** Damodaran's full-featured "Ginzu" FCFF valuation model, in the **lambda variant for emerging-market companies**. It values a firm with positive (or normalizable-to-positive) operating income using a 2-stage or 3-stage FCFF DCF, where the cost of equity uses a **lambda coefficient on the country risk premium** (`CoE = Rf + beta·MatureERP + lambda·CountryERP`) instead of scaling country risk by beta. It is also **dual-currency**: financial-statement inputs are entered in local currency and converted to US$ at fiscal-year exchange rates; the DCF runs in dollars; the per-share value is converted back to local currency at the current exchange rate. The example loaded in the sheet is a Korean-style conglomerate (Hyundai cross-holdings) with a Brazilian-Real-labelled currency axis ("$R/$", "value per share in BR"). Requires Excel iterative calculation (circular references: market value of debt ↔ cost of debt, warrant value ↔ adjusted stock price).

Supporting worksheets: earnings normalizer, R&D capitalizer, operating-lease converter, synthetic-rating estimator, bottom-up beta, cross-holdings valuer, business-breakdown beta, terminal-value sensitivity, industry averages reference table.

---

## Sheet: Read me first

Instructional text only. Key facts: enable Excel iteration (circular reasoning is intentional); model handles up to 15 years of high growth (the FCFF display table shows up to 10 columns); can run as 2-stage, 3-stage (answer "Yes" to "adjust inputs during second half of high growth"), or pure stable-growth (set high-growth length = 0). Units must be consistent throughout. Output is on the "Valuation Model" sheet.

---

## Sheet: Master Inputs Start here

All user inputs. Current example values shown.

### Preprocessing toggles
| Cell | Label | Value |
|---|---|---|
| B4 | Capitalize R&D expenses? | No |
| B5 | Convert operating leases to debt? | No |
| B6 | Normalize operating income? | No |

### From current financials (local currency)
| Cell | Label | Value | Notes |
|---|---|---|---|
| B10 | Current EBIT | 1751 | must be positive (else normalize or use highgrowth.xls) |
| B11 | Current interest expense | 11.4 | |
| B12 | Current capital spending | 911 | |
| B13 | Current depreciation & amortization | 392 | |
| B14 | Tax rate (for after-tax operating income) | 0.275 | |
| B15 | Marginal tax rate | 0.275 | |
| B16 | Current revenues | 15533 | C16 = previous year-end revenues = 12554 |
| B17 | Current non-cash working capital | −5813 | |
| B18 | Chg. working capital | 135 | |
| B19 | Book value of debt | 188 | C19 = previous year-end = 187 |
| B20 | Book value of equity | 5492 | C20 = previous year-end = 4479 |
| B22 | Cash & marketable securities | 3612 | C22 = previous year-end = 1276 |
| B23 | Value of non-operating assets | 3937.068 | fed by Cross Holdings sheet total (D11) |
| B24 | Minority interests (book value) | 0 | |
| B25 | Price-to-book ratio of sector with minority holdings | 2.1 | |

(Stray helper values I23 = 0.145082, I25 = 0.1307366 — purpose not identifiable from values; appear to be scratch cells, not part of the dependency chain.)

### Market data
| Cell | Label | Value |
|---|---|---|
| B27 | Is your stock currently traded? | Yes |
| B29 | Current stock price (local currency) | 365 |
| B30 | Number of shares outstanding | 76 |
| B31 | Market value of debt | 185.5815 (computed, see Logic) |
| F27 | Average maturity of debt (years) | 3 |
| B33 | If not traded: use book value debt ratio? | No |
| B34 | If no: debt ratio to use in valuation | 0.35 |

### General market data
| Cell | Label | Value |
|---|---|---|
| B37 | Long-term treasury bond rate (Rf) | 0.05 |
| B38 | Mature market equity premium | 0.06 |
| B39 | Country equity risk premium | 0.0263 |
| B40 | Exchange rate for fiscal-year items (local/$) | 2.0 (C40 = previous year-end rate = 1.9) |
| B41 | Exchange rate for current price conversions | 2.05 |

### Ratings
| Cell | Label | Value |
|---|---|---|
| B43 | Estimate synthetic rating? | No |
| B44 | If yes: type of firm (1=large mfg, 2=smaller/riskier, 3=financial service) | 2 |
| B45 | If no: current rating of firm | AAA |
| B46 | Cost of debt associated with rating | 0.0655 |

### Equity options
| Cell | Label | Value |
|---|---|---|
| B49 | Equity options/warrants outstanding? | No |
| B50 | Number of options | 2.23 |
| B51 | Average strike price | 13.85 |
| B52 | Average maturity (years) | 1.5 |
| B53 | Std deviation in stock price | 0.3 |
| B54 | Use stock price (P) or estimated value (V) to value options | P |

### Valuation inputs — high growth
| Cell | Label | Value |
|---|---|---|
| B58 | Length of high growth period (years) | 5 |
| B59 | Beta for high growth period | 1.5 |
| B60 | **Lambda (both phases)** | 0.25 |
| B61 | Keep debt ratio computed from inputs? | Yes |
| B62 | (if yes) computed debt ratio | 0.0066455739 (computed = MV debt/(MV debt + MV equity)) |
| B63 | (if no) debt ratio to use | 0.07 |
| B64 | Keep existing working-capital-to-revenue ratio? | Yes |
| B65 | (if yes) WC as % of revenues | −0.3742355 (= B17/B16) |
| B66 | (if no) WC/revenue ratio to use | 0.12 |
| B67 | Compute growth from fundamentals? | Yes |
| B68 | (if no) expected growth in operating income | 0.15 |
| B70 | (computed from inputs) Return on capital | 0.3744764 |
| B71 | (computed from inputs) Reinvestment rate | 0.5151736 |
| B72 | Change these inputs? | Yes |
| B73 | (override) Return on capital | 0.30 |
| B74 | (override) Reinvestment rate | 0.50 |
| B76 | Gradually adjust high-growth inputs in second half (3-stage)? | No |

### Valuation inputs — stable growth
| Cell | Label | Value |
|---|---|---|
| B79 | Stable growth rate | 0.05 |
| B80 | Stable-period beta | 1.2 |
| B81 | Country risk premium for equity in stable period | 0.008 |
| B82 | Stable-period debt ratio | 0.10 |
| B83 | Stable-period pre-tax cost of debt | 0.0575 |
| B84 | Stable-period tax rate | 0.275 |
| B86 | Compute stable reinvestment from fundamentals? | Yes |
| B87 | (if yes) stable-period return on capital | 0.11576875 (here set equal to stable cost of capital → excess returns = 0) |
| B88 | (if no) capex as % of depreciation in stable growth | 1.2 |

### Computed helper formulas on this sheet (all verified)
- **Market value of debt (B31)**, treating book debt as a coupon bond priced at the current cost of debt kd (B46) with maturity M (F27):
  `MV_debt = IntExp·(1 − (1+kd)^−M)/kd + BV_debt/(1+kd)^M = 11.4·(1−1.0655^−3)/0.0655 + 188/1.0655^3 = 30.18 + 155.40 = 185.5815` ✓
- **Computed debt ratio (B62)**: `MV_debt/(MV_debt + Price·Shares) = 185.5815/(185.5815 + 365·76) = 0.0066455739` ✓
- **ROC from inputs (B70)**: `EBIT·(1−t) / (BV_debt_prev + BV_equity_prev − Cash_prev) = 1751·0.725/(187 + 4479 − 1276) = 1269.475/3390 = 0.3744764` ✓ (uses previous-year-end book values, i.e. beginning invested capital)
- **Reinvestment rate from inputs (B71)**: `(CapEx − Deprec + ChgWC)/(EBIT·(1−t)) = (911 − 392 + 135)/1269.475 = 0.5151736` ✓

---

## Sheet: Historical Numbers

Informational side sheet (4 years of history, 2003–2007 columns; not part of the valuation dependency chain). Rows: EBIT(1−t), BV of debt, BV of equity, Cash holdings, Invested Capital (= BVdebt + BVequity − cash of the prior year-end), ROIC (= EBIT(1−t)/beginning invested capital; e.g. 2007: 1269.475/3390 = 0.374476), Cap ex, Depreciation, Chg in WC, Reinvestment (= capex − deprec + ΔWC), Reinvestment Rate (= reinvestment/EBIT(1−t)). Aggregate column sums; H2 = 535.36875 (average EBIT(1−t)), H7 = 0.1579259 (aggregate ROIC = 2141.475·?/…, aggregate EBIT(1−t)/aggregate invested capital variants). Values: EBIT(1−t) by year: −98, 91, 879, 1269.475; ROIC: −0.03136, 0.020468, 0.218602, 0.374476.

---

## Sheet: Cross Holdings Valuation

Values the non-operating cross-holdings; its total feeds Master Inputs B23.

Two blocks:
1. **Minority (market-traded) holdings**: `Value = %held × market cap of holding`.
2. **Majority/consolidated (unlisted) holdings**: `Value = book value × sector P/B` (the "Total Market Cap" column here is derived backwards: Value/%held).

| Holding | % held | Total mkt cap | Value of holding | Book value | Sector P/B |
|---|---|---|---|---|---|
| Hyundai Merchant Marine | 0.176 | 4806 | 845.856 | | |
| Hyundai Motors | 0.0346 | 17540 | 606.884 | | |
| Hyundai Elevator | 0.0216 | 688 | 14.8608 | | |
| Hyundai Corp | 0.0036 | 602 | 2.1672 | | |
| Others | ? | ? | 84.2 (direct input) | | |
| Hyundai Oil Bank | 0.1987 | 1825.767 (derived) | 362.78 = 329.8·1.1 | 329.8 | 1.1 |
| Hyundai Samho | 0.9492 | 2026.233 (derived) | 1923.3 = 1068.5·1.8 | 1068.5 | 1.8 |
| Hyundai Finance | 0.6749 | 143.755 (derived) | 97.02 = 88.2·1.1 | 88.2 | 1.1 |
| **Total (D11 → Master B23)** | | | **3937.068** | | |

---

## Sheet: Business Breakdown

Computes a value-weighted unlevered beta across business segments (feeds nothing automatically; the user copies the result into the Bottom-up Beta sheet or beta input). `Value = Revenues × EV/Sales`; `Weight = Value/ΣValue`; bottom row F8 = Σ(weight·unlevered beta).

| Business | Revenues | EV/Sales | Value | Weight | Unlevered beta |
|---|---|---|---|---|---|
| Shipbuilding | 8341 | 3.23 | 26941.43 | 0.63730 | 1.6 |
| Offshore & Engineering | 2563 | 1.97 | 5049.11 | 0.11944 | 1.44 |
| Industrial plant | 1200 | 1.55 | 1860.00 | 0.04400 | 1.29 |
| Engine and Machinery | 2252 | 1.36 | 3062.72 | 0.07245 | 1.21 |
| Electro Electric System | 1753 | 1.80 | 3155.40 | 0.07464 | 1.19 |
| Construction Equipment | 1823 | 1.21 | 2205.83 | 0.05218 | 1.29 |
| **Total** | | | **42274.49** | 1.0 | **1.4922177 (weighted)** |

---

## Sheet: Earnings Normalizer

Used only if Master B6 = "Yes". Normalizes EBIT by one of three approaches, selected by code in D2 (1, 2, or 3):

| Approach (D2) | Method | Cell | Example |
|---|---|---|---|
| 1 | Historical average EBIT | D5 = average of last 5 years' EBIT = 4850/5 = 970 | selected (D2=1) |
| 2 | Historical average pre-tax ROC × invested capital | D8 = 0.22 (input ROC) | `Normalized EBIT = ROC_avg × invested capital` (inferred) |
| 3 | Sector pre-tax operating margin × current revenues | D11 = 0.1095798 (here = firm's own 5-yr aggregate margin; label says look up industry average) | `= margin × revenues` (inferred) |

**Normalized EBIT (D14) = 970** (approach 1 selected).

Worksheet data (last 5 years, columns −5 … −1, plus Total):

| Row | −5 | −4 | −3 | −2 | −1 | Total |
|---|---|---|---|---|---|---|
| Revenues | 6571 | 10231 | 9133 | 8342 | 9983 | 44260 |
| EBIT | 1243 | 1740 | 794 | 546 | 527 | 4850 |
| Operating margin | 0.18916 | 0.17007 | 0.08694 | 0.06545 | 0.05279 | 0.10958 (aggregate) |
| Net cap ex | 282 | −112 | −27 | 151.76 | 196.02 | 490.78 |
| Non-cash WC | 26.07 | 305.82 | 915.03 | −222.74 | 1502.90 | 2527.08 |

(WC detail rows: Inventory, Accounts Rec, Other Current Assets, Accounts Payable, Other Current Liabilities per year — WC = Inv + AR + OCA − AP − OCL.)

Derived ratios (verified):
- Net capex as % of EBIT(1−t) (B32) = `ΣNetCapEx / (ΣEBIT·(1−t)) = 490.78/(4850·0.725) = 0.1395748`
- Non-cash WC as % of revenue (B33) = `ΣWC/ΣRevenues = 2527.08/44260 = 0.0570962`
- **Normalized reinvestment (B35)** = `CurrentEBIT·(1−t)·(netcapex%) + (Rev − Rev_prev)·(WC%) = 1751·0.725·0.1395748 + (15533−12554)·0.0570962 = 177.19 + 170.09 = 347.276` ✓

---

## Sheet: R&D converter

Used only if Master B4 = "Yes". Capitalizes R&D as an asset amortized straight-line over N years.

**Inputs:** amortization life N (F6 = 5, max 10; look-up table below), current-year R&D (F7 = 1594), past R&D for years −1 … −N (B11:B20): −1: 1026, −2: 698, −3: 399, −4: 211, −5: 89.

**Logic (verified):** for age a = 0 (current) … N:
- Unamortized fraction = `1 − a/N` (current year = 1.0; year −N = 0)
- Unamortized portion = `R&D_a × (1 − a/N)`
- Amortization this year = `R&D_a / N` for a = 1…N (none for current year)
- **Value of research asset (D35)** = Σ unamortized portions = 1594 + 820.8 + 418.8 + 159.6 + 42.2 + 0 = **3035.4**
- **Current-year amortization (D37/E35)** = Σ(past R&D)/N = (1026+698+399+211+89)/5 = **484.6**
- **Adjustment to operating income (D39)** = `Current R&D − amortization = 1594 − 484.6 = 1109.4` (add to reported EBIT)
- **Tax effect of R&D expensing (D40)** = `Adjustment × marginal tax rate = 1109.4 × 0.275 = 305.085`
- Downstream (inferred, standard Ginzu behavior; toggles are "No" in this copy so unexercised here): adjusted EBIT = EBIT + D39; research asset added to book equity/invested capital; amortization added to depreciation and current R&D added to capex.

**Reference table — R&D amortization periods by industry (verbatim):**
Rule-of-thumb block: Non-technological Service 2 years; Retail/Tech Service 3 years; Light Manufacturing 5 years; Heavy Manufacturing 10 years; Research with Patenting 10 years; Long Gestation Period 10 years.

| Industry | Yrs | Industry | Yrs | Industry | Yrs |
|---|---|---|---|---|---|
| Advertising | 2 | Electronics | 5 | Natural Gas (Diversified) | 10 |
| Aerospace/Defense | 10 | Entertainment | 3 | Newspaper | 3 |
| Air Transport | 10 | Environmental | 5 | Office Equip & Supplies | 5 |
| Aluminum | 5 | Financial Services | 2 | Oilfield Services/Equip. | 5 |
| Apparel | 3 | Food Processing | 3 | Packaging & Container | 5 |
| Auto & Truck | 10 | Food Wholesalers | 3 | Paper & Forest Products | 10 |
| Auto Parts (OEM) | 5 | Foreign Electron/Entertn | 5 | Petroleum (Integrated) | 5 |
| Auto Parts (Replacement) | 5 | Foreign Telecom. | 10 | Petroleum (Producing) | 5 |
| Bank | 2 | Furn./Home Furnishings | 3 | Precision Instrument | 5 |
| Bank (Canadian) | 2 | Gold/Silver Mining | 5 | Publishing | 3 |
| Bank (Foreign) | 2 | Grocery | 2 | R.E.I.T. | 3 |
| Bank (Midwest) | 2 | Healthcare Info Systems | 3 | Railroad | 5 |
| Beverage (Alcoholic) | 3 | Home Appliance | 5 | Recreation | 5 |
| Beverage (Soft Drink) | 3 | Homebuilding | 5 | Restaurant | 2 |
| Building Materials | 5 | Hotel/Gaming | 3 | Retail (Special Lines) | 2 |
| Cable TV | 10 | Household Products | 3 | Retail Building Supply | 2 |
| Canadian Energy | 10 | Industrial Services | 3 | Retail Store | 2 |
| Cement & Aggregates | 10 | Insurance (Diversified) | 3 | Securities Brokerage | 2 |
| Chemical (Basic) | 10 | Insurance (Life) | 3 | Semiconductor | 5 |
| Chemical (Diversified) | 10 | Insurance (Prop/Casualty) | 3 | Semiconductor Cap Equip | 5 |
| Chemical (Specialty) | 10 | Internet | 3 | Shoe | 3 |
| Coal/Alternate Energy | 5 | Investment Co. (Domestic) | 3 | Steel (General) | 5 |
| Computer & Peripherals | 5 | Investment Co. (Foreign) | 3 | Steel (Integrated) | 5 |
| Computer Software & Svcs | 3 | Investment Co. (Income) | 3 | Telecom. Equipment | 10 |
| Copper | 5 | Machinery | 10 | Telecom. Services | 5 |
| Diversified Co. | 5 | Manuf. Housing/Rec Veh | 5 | Textile | 5 |
| Drug | 10 | Maritime | 10 | Thrift | 2 |
| Drugstore | 3 | Medical Services | 3 | Tire & Rubber | 5 |
| Educational Services | 3 | Medical Supplies | 5 | Tobacco | 5 |
| Electric Util. (Central) | 10 | Metal Fabricating | 10 | Toiletries/Cosmetics | 3 |
| Electric Utility (East) | 10 | Metals & Mining (Div.) | 5 | Trucking/Transp. Leasing | 5 |
| Electric Utility (West) | 10 | Natural Gas (Distrib.) | 10 | Utility (Foreign) | 10 |
| Electrical Equipment | 10 | | | Water Utility | 10 |

---

## Sheet: Operating lease converter

Used only if Master B5 = "Yes". Converts operating-lease commitments to debt.

**Inputs:** current-year operating lease expense (E3 = 121); commitments year 1–5 (B6:B10 = 156, 143, 122, 109, 97); lump sum "6 and beyond" (B11 = 448); pre-tax cost of debt (C14 = 0.0655, links to rating result); reported EBIT (D17 = 1751); reported debt (D18 = 185.5815).

**Logic (verified):**
- Years embedded in the year-6+ lump sum (D20): `round(B11 / average(yr1..yr5 commitments)) = round(448/125.4) = 3` (inferred rounding; sheet note: "I use the average lease expense over the first five years to estimate the number of years of expenses in yr 6")
- Annualized year-6+ commitment (B29): `448/3 = 149.3333`
- PV of years 1–5: `C_t/(1+kd)^t` → 146.410, 125.959, 100.855, 84.569, 70.632
- PV of year-6+ (C29): annuity of 149.3333 for D20=3 years, discounted back 5 years: `149.3333·(1−1.0655^−3)/0.0655 / 1.0655^5 = 287.7308` ✓ (the sheet comment "annuity for ten years" is stale; the number matches a 3-year annuity, i.e. the D20 estimate)
- **Debt value of leases (C30) = 816.15715**
- Depreciation on lease asset (F33) = `C30 / (5 + D20) = 816.157/8 = 102.0196` (straight line over remaining lease life = 5 + years-in-lump) ✓
- **Adjustment to operating earnings (F34)** = `C30 × kd = 816.157·0.0655 = 53.4583` (add to EBIT; this is the imputed interest portion — the sheet adds back lease interest, not full lease expense less depreciation)
- **Adjustment to total debt (F35)** = C30 = 816.157 (add to book and market debt) (downstream wiring inferred; toggle is "No" here)

---

## Sheet: Ratings estimator

Used if Master B43 = "Yes". Synthetic rating from interest coverage.

**Inputs:** firm type (C2 = 2; 1 = large manufacturing, 2 = smaller/riskier, 3 = financial service), EBIT (F3 = 1751), interest expense (F4 = 11.4), long-term government bond rate (F5 = 0.05).

**Logic:** `coverage = EBIT/InterestExpense = 1751/11.4 = 153.596` → look up rating band in the table for the chosen firm type → default spread → `cost of debt = Rf + spread = 0.05 + 0.004 = 0.054`. Output here: rating AAA, spread 0.004, cost of debt 0.054. (Edge case: if interest expense = 0 coverage is infinite → top band; if EBIT ≤ 0 coverage negative → bottom band.)

**Reference table 1 — large manufacturing firms (type 1), verbatim:**

| coverage > | ≤ | Rating | Spread |
|---|---|---|---|
| −100000 | 0.199999 | D | 0.12 |
| 0.2 | 0.649999 | C | 0.105 |
| 0.65 | 0.799999 | CC | 0.095 |
| 0.8 | 1.249999 | CCC | 0.0875 |
| 1.25 | 1.499999 | B− | 0.0725 |
| 1.5 | 1.749999 | B | 0.065 |
| 1.75 | 1.999999 | B+ | 0.055 |
| 2.0 | 2.2499999 | BB | 0.04 |
| 2.25 | 2.49999 | BB+ | 0.03 |
| 2.5 | 2.999999 | BBB | 0.02 |
| 3.0 | 4.249999 | A− | 0.013 |
| 4.25 | 5.499999 | A | 0.01 |
| 5.5 | 6.499999 | A+ | 0.0085 |
| 6.5 | 8.499999 | AA | 0.007 |
| 8.5 | 100000 | AAA | 0.004 |

**Reference table 2 — financial service firms (type 3), long-term interest coverage, verbatim** (final column "Operating Income Decline" is an auxiliary series stored alongside; not used in this workbook's chain):

| coverage > | ≤ | Rating | Spread | Op. income decline |
|---|---|---|---|---|
| −100000 | 0.049999 | D | 0.12 | 0.15 |
| 0.05 | 0.099999 | C | 0.105 | 0.10 |
| 0.1 | 0.199999 | CC | 0.095 | 0.08 |
| 0.2 | 0.299999 | CCC | 0.0875 | 0.06 |
| 0.3 | 0.399999 | B− | 0.0725 | 0.05 |
| 0.4 | 0.499999 | B | 0.065 | 0.045 |
| 0.5 | 0.599999 | B+ | 0.055 | 0.04 |
| 0.6 | 0.749999 | BB | 0.04 | 0.03 |
| 0.75 | 0.899999 | BB+ | 0.03 | 0.025 |
| 0.9 | 1.199999 | BBB | 0.02 | 0.015 |
| 1.2 | 1.49999 | A− | 0.013 | 0.013 |
| 1.5 | 1.99999 | A | 0.01 | 0.012 |
| 2.0 | 2.49999 | A+ | 0.0085 | 0.0115 |
| 2.5 | 2.99999 | AA | 0.007 | 0.009 |
| 3.0 | 100000 | AAA | 0.004 | 0.007 |

**Reference table 3 — smaller and riskier firms (type 2), verbatim:**

| coverage > | ≤ | Rating | Spread |
|---|---|---|---|
| −100000 | 0.499999 | D | 0.12 |
| 0.5 | 0.799999 | C | 0.105 |
| 0.8 | 1.249999 | CC | 0.095 |
| 1.25 | 1.499999 | CCC | 0.0875 |
| 1.5 | 1.999999 | B− | 0.0725 |
| 2.0 | 2.499999 | B | 0.065 |
| 2.5 | 2.999999 | B+ | 0.055 |
| 3.0 | 3.499999 | BB | 0.04 |
| 3.5 | 3.9999999 | BB+ | 0.03 |
| 4.0 | 4.499999 | BBB | 0.02 |
| 4.5 | 5.999999 | A− | 0.013 |
| 6.0 | 7.499999 | A | 0.01 |
| 7.5 | 9.499999 | A+ | 0.0085 |
| 9.5 | 12.499999 | AA | 0.007 |
| 12.5 | 100000 | AAA | 0.004 |

---

## Sheet: Bottom-up Beta

**Inputs:** unlevered beta for sector (D2 = 1.49; look up in Industry averages or Business Breakdown result).
**Pulled from model:** firm's current market D/E ratio (D5 = 0.00669003 = MV_debt/MV_equity = 185.5815/27740), tax rate (D6 = 0.275).
**Output (verified):** `levered beta (D8) = unlevered × (1 + (1−t)·D/E) = 1.49·(1 + 0.725·0.0066900) = 1.4972269`. (Stray helper N7 = 1.6363636, not in the chain.) The user then copies this into Master B59 manually.

---

## Sheet: Option Value

Dilution-adjusted Black–Scholes for management options/warrants (used if Master B49 = "Yes"; here "No", so contributes 0 to the valuation, but the sheet computes anyway from Master's option inputs). Works in local currency (stock price 365).

**Inputs (mirrors Master):** stock price S = 365, strike K = 13.85, expiration t = 1.5, σ = 0.3, dividend yield y = 0, T-bond rate r = 0.05, #warrants M = 2.23, #shares N_s = 76. If Master B54 = "V", the model's own estimated per-share value replaces the market price (inferred).

**Logic (verified, circular — iterate to convergence):**
- Adjusted S = `(S·N_s + OptionValue·M)/(N_s + M)` → 364.62298
- Adjusted K = K = 13.85; Variance = σ² = 0.09; div-adjusted rate = r − y = 0.05
- `d1 = [ln(S_adj/K) + (r − y + σ²/2)·t]/(σ·√t) = 9.28922`; N(d1) = 1.0
- `d2 = d1 − σ·√t = 8.92180`; N(d2) = 1.0
- `Value per option = S_adj·e^(−y·t)·N(d1) − K·e^(−r·t)·N(d2) = 364.623 − 13.85·e^(−0.075) = 351.77373`
- `Value of all options = 351.77373 × 2.23 = 784.45542`

---

## Sheet: Terminal Value

Terminal-value calculator plus a sensitivity table demonstrating that when stable ROC = stable cost of capital, terminal value is invariant to the stable growth rate.

**Values (all verified against Valuation Model):** terminal-year EBIT(1−t) = 1340.51802 (= year-5 EBIT(1−t) × 1.05); g = 0.05; stable cost of capital = 0.11576875; stable ROC = 0.11576875; reinvestment rate = `g/ROC = 0.4318955`; **Terminal value = EBIT(1−t)·(1−RR)/(CoC − g) = 761.55435/0.06576875 = 11579.2735**.

Sensitivity table (g from 0 to 0.05, step 0.01): RR = g/ROC → FCFF = EBIT(1−t)·(1−RR) → TV always 11579.27 (because ROC = CoC). E.g. g=0: RR=0, FCFF=1340.518, TV=11579.27; g=0.03: RR=0.2591373, FCFF=993.1398, TV=11579.27.

---

## Sheet: Valuation Model (the output sheet)

### Input summary block (rows 3–29)
Two columns: **Local currency (D)** and **Dollar (E)**. Conversion rules (verified):
- Fiscal-year flow/current items ÷ B40 (=2.0): EBIT, interest expense, capex, depreciation, revenues, WC, ΔWC. E.g. 1751/2 = 875.5.
- Previous-year-end book values ÷ C40 (=1.9): adjusted BV debt 187/1.9 = 98.42105, BV equity 4479/1.9 = 2357.36842.
- "Normalized EBIT (before adjustments)" D3 = normalized EBIT if Master B6=Yes else current EBIT; "Adjusted EBIT" D4 = D3 + R&D adjustment + lease adjustment when those toggles are Yes (inferred; both No here so D4 = 1751). Similarly adjusted interest/capex/depreciation/debt/equity would fold in lease interest, R&D capex/amortization and research asset (inferred).
- Invested capital D15 = `BV_debt_prev + BV_equity_prev − Cash_prev = 187 + 4479 − 1276 = 3390` (local); E15 = 3390/1.9 = 1784.21053.

Right column of the same block repeats the valuation parameters: high-growth (D) vs stable (E): length 5/Forever; growth 0.15/0.05; debt ratio 0.0066456/0.10; beta 1.5/1.2; lambda 0.25/0.25; Rf 0.05/0.05; mature ERP 0.06/0.06; country risk premium 0.0263/0.008; cost of debt 0.0655/0.0575; tax rates 0.275; ROC 0.30/0.11576875; reinvestment rate 0.50/0.4318955.

### Discount rate (rows 32–36, verified)
- **Cost of equity (lambda form):** `CoE = Rf + beta·MatureERP + lambda·CRP = 0.05 + 1.5·0.06 + 0.25·0.0263 = 0.146575`
- After-tax cost of debt = `kd·(1 − marginal t) = 0.0655·0.725 = 0.0474875`
- Cost of capital = `CoE·E/(D+E) + ATkd·D/(D+E) = 0.146575·0.9933544 + 0.0474875·0.0066456 = 0.14591651`
- Debt ratio source: Master B62 if B61=Yes; else B63. If stock not traded: book ratio or B34 (inferred branch).

### High-growth FCFF table (rows 42–52; columns Current, 1…n, n ≤ 10; unused year columns hold blanks; final column S = "Terminal Year")
Per year t (all verified):
- Expected growth rate g_t = 0.15 (constant here; if Master B76 = "Yes", inputs glide linearly toward stable values over the second half — 3-stage mode (inferred))
- Cumulated growth CG_t = Π(1+g_i) (1.15, 1.3225, 1.5208750, 1.7490062, 2.0113572)
- Reinvestment rate RR_t = 0.5
- `EBIT(1−t)_t = EBIT$(1−t)_0 × CG_t` where EBIT$(1−t)_0 = 875.5·0.725 = 634.7375 → 729.94812, 839.44034, 965.35640, 1110.15985, 1276.68383
- `ΔWC_t = WC% × RevLC_0 × CG_{t−1} × g_t ÷ FX?` — **computed off local-currency revenues**: ΔWC_1 = −0.3742355·15533·0.15 = −871.95 (matches sheet; note the model mixes local revenue base with dollar cash flows here — replicate as-is or normalize deliberately). Series: −871.95, −1002.7425, −1153.15387, −1326.12696, −1525.04600.
- `(CapEx − Deprec)_t = RR_t·EBIT(1−t)_t − ΔWC_t` (plug so total reinvestment = RR·EBIT(1−t)): 1236.92406, 1422.46267, 1635.83207, 1881.20688, 2163.38792
- `FCFF_t = EBIT(1−t)_t·(1 − RR_t)` = 364.97406, 419.72017, 482.67820, 555.07993, 638.34192
- Cost of capital per year 0.14591651 (constant in 2-stage; would vary in 3-stage); cumulated CoC_t = Π(1+CoC_i): 1.1459165, 1.3131246, 1.5047312, 1.7242963, 1.9758996
- `PV_t = FCFF_t / CumCoC_t`: 318.49970, 319.63468, 320.77370, 321.91678, 323.06394
- Current column (t=0): EBIT(1−t) = 634.7375; CapEx−Dep = 455.5−196 = 259.5; ΔWC = 67.5; FCFF = 307.7375 (display only).
- Terminal-year column S (verified): EBIT(1−t) = 1276.68383·1.05 = 1340.51802; ΔWC = −0.3742355·15533·CG_5·0.05 = −584.60097; CapEx−Dep = RR_stable·EBIT(1−t) − ΔWC = 578.96368+584.60097 = 1163.56464; FCFF = 1340.51802·(1−0.4318955) = 761.55435.

### Stable phase (rows 54–62, verified)
- RR_stable: if Master B86=Yes: `g/ROC_stable = 0.05/0.11576875 = 0.4318955`; if No: derived from capex%-of-depreciation input B88 (inferred).
- CoE_stable = `Rf + beta_st·MatureERP + lambda·CRP_st = 0.05 + 1.2·0.06 + 0.25·0.008 = 0.124`
- ATkd_stable = 0.0575·0.725 = 0.0416875; CoC_stable = 0.124·0.9 + 0.0416875·0.1 = 0.11576875
- Terminal value = `FCFF_terminal/(CoC_st − g) = 761.55435/0.06576875 = 11579.27355`

### Final valuation (rows 64–75, verified; all in US$)
| Row | Item | Formula | Value |
|---|---|---|---|
| F64 | PV of high-growth FCFF | Σ PV_t | 1603.88880 |
| F65 | PV of terminal value | TV / CumCoC_5 = 11579.27355/1.9758996 | 5860.25396 |
| F66 | Value of operating assets | F64 + F65 | 7464.14276 |
| F67 | Cash & non-operating assets | (Cash_LC + NonOp_LC)/FX_current = (3612 + 3937.068)/2.05 | 3682.47220 |
| F68 | Value of firm | F66 + F67 | 11146.61496 |
| F69 | − MV of outstanding debt | MV_debt_LC/FX_current = 185.5815/2.05 | 90.52757 |
| F70 | − Minority interest | MI_book × sector P/B = 0·2.1 | 0 |
| F71 | MV of equity | F68 − F69 − F70 | 11056.08739 |
| F72 | − Value of equity options | from Option Value sheet if B49=Yes (÷FX_current, inferred) | 0 |
| F73 | Value of equity in common stock | F71 − F72 | 11056.08739 |
| F74 | **Value per share (US$)** | F73 / shares = /76 | **145.47483** |
| F75 | **Value per share (local, "BR")** | F74 × FX_current = ×2.05 | **298.22341** |

---

## Sheet: Industry averages (reference data, verbatim)

Lookup table for beta, margins, reinvestment, WC ratios, EV/Sales, etc. "NA" = not available. Values in decimal fractions unless a ratio.

| Industry Name | Number of firms | Levered Beta | Unlevered Beta | Std Dev: Equity | Market D/E | Market Debt/Capital | ROE | ROC | Effective Tax Rate | Pre-tax Operating Margin | After-tax Operating Margin | Net Margin | Cap Ex/ Depreciation | Non-cash WC/ Revenues | Payout Ratio | Reinvestment Rate | Sales/Capital | EV/Sales |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Advertising | 31 | 2.02 | 1.75 | 1.0129 | 0.4326 | 0.302 | 0.0889 | 0.1054 | 0.1073 | 0.1027 | 0.0744 | 0.0363 | 0.5418 | -0.1984 | 0.4375 | -0.4614 | 1.42 | 1.14 |
| Aerospace/Defense | 64 | 1.1 | 1.03 | 0.6132 | 0.2566 | 0.2042 | 0.34 | 0.1853 | 0.2072 | 0.1016 | 0.0731 | 0.0678 | 1.2628 | 0.0289 | 0.2913 | 0.1477 | 2.53 | 0.93 |
| Air Transport | 36 | 1.21 | 1.1 | 0.648 | 0.2432 | 0.1956 | 1.089 | 0.1645 | 0.2054 | 0.0878 | 0.0686 | 0.0376 | 1.2222 | -0.0925 | 0.1891 | 0.0554 | 2.4 | 1.78 |
| Apparel | 57 | 1.3 | 1.22 | 0.8882 | 0.1838 | 0.1553 | 0.1734 | 0.1402 | 0.1608 | 0.1097 | 0.076 | 0.0672 | 1.0324 | 0.1724 | 0.1885 | 0.2213 | 1.85 | 1.19 |
| Auto Parts | 51 | 1.7 | 1.59 | 0.8058 | 0.2765 | 0.2166 | 0.2259 | 0.1582 | 0.1899 | 0.0649 | 0.0498 | 0.051 | 0.9608 | 0.0559 | 0.2374 | 0.1516 | 3.18 | 0.59 |
| Automotive | 12 | 1.59 | 0.96 | 0.6891 | 1.3457 | 0.5737 | 0.1846 | 0.0696 | 0.2407 | 0.0699 | 0.0494 | 0.0336 | 0.8704 | 0.1937 | 0.2224 | -0.2237 | 1.41 | 0.73 |
| Bank | 426 | 0.77 | 0.38 | 0.6115 | 1.5611 | 0.6095 | 0.076 | NA | 0.1597 | NA | NA | NA | NA | NA | 0.3353 | 0 | NA | NA |
| Bank (Midwest) | 45 | 0.93 | 0.73 | 0.556 | 0.5952 | 0.3731 | 0.0908 | NA | 0.1777 | NA | NA | NA | NA | NA | 0.3836 | 0 | NA | NA |
| Beverage | 34 | 0.88 | 0.77 | 0.6605 | 0.2652 | 0.2096 | 0.2458 | 0.1295 | 0.1914 | 0.2045 | 0.156 | 0.1399 | 0.8724 | 0.0108 | 0.4635 | -0.0246 | 0.83 | 3.03 |
| Biotechnology | 158 | 1.03 | 1.16 | 1.1311 | 0.1348 | 0.1188 | 0.1515 | -0.1333 | 0.0249 | -0.0779 | -0.1373 | 0.0911 | 0.8442 | -0.0583 | 0.5934 | NA | 0.97 | 4.49 |
| Building Materials | 45 | 1.5 | 0.89 | 0.7883 | 0.9433 | 0.4854 | -0.0517 | 0.0258 | 0.1117 | 0.0417 | 0.0316 | -0.0401 | 0.48 | 0.0766 | NA | -1.0683 | 0.82 | 1.22 |
| Cable TV | 21 | 1.37 | 0.98 | 0.5077 | 0.6806 | 0.405 | 0.1613 | 0.088 | 0.2735 | 0.1958 | 0.1243 | 0.0902 | 0.8532 | -0.0965 | 0.1803 | -0.3082 | 0.71 | 2.21 |
| Chemical (Basic) | 16 | 1.36 | 1.24 | 0.4927 | 0.2735 | 0.2147 | 0.2583 | 0.1366 | 0.209 | 0.1209 | 0.0956 | 0.1246 | 1.2681 | 0.0968 | 0.3079 | 0.2924 | 1.43 | 1.52 |
| Chemical (Diversified) | 31 | 1.51 | 1.39 | 0.5631 | 0.2237 | 0.1828 | 0.1926 | 0.1381 | 0.2173 | 0.132 | 0.093 | 0.0879 | 1.0437 | 0.1558 | 0.3168 | 0.4792 | 1.48 | 1.62 |
| Chemical (Specialty) | 70 | 1.28 | 1.15 | 0.716 | 0.2115 | 0.1746 | 0.185 | 0.1225 | 0.1758 | 0.111 | 0.0787 | 0.0804 | 0.9678 | 0.126 | 0.4043 | 0.1299 | 1.56 | 1.56 |
| Coal | 20 | 1.53 | 1.32 | 0.5552 | 0.289 | 0.2242 | 0.2424 | 0.1526 | 0.1275 | 0.1594 | 0.1253 | 0.12 | 1.4173 | 0.0361 | 0.3378 | 0.3748 | 1.22 | 1.78 |
| Computer Software | 184 | 1.04 | 1.18 | 0.8203 | 0.0749 | 0.0697 | 0.7913 | 0.4506 | 0.1227 | 0.3135 | 0.2462 | 0.2478 | 0.6472 | -0.1116 | 0.2161 | -0.0905 | 1.83 | 3.07 |
| Computers/Peripherals | 87 | 1.3 | 1.33 | 0.9769 | 0.1023 | 0.0928 | 0.5252 | 0.3209 | 0.1177 | 0.1415 | 0.1083 | 0.1074 | 1.0358 | -0.0197 | 0.0861 | 0.0122 | 2.96 | 1.39 |
| Diversified Co. | 107 | 1.14 | 0.71 | 0.75 | 1.0224 | 0.5055 | 0.3328 | 0.0801 | 0.1555 | 0.1409 | 0.1176 | 0.0921 | 0.8924 | 0.7165 | 0.3681 | 0.0167 | 0.68 | 2.11 |
| Drug | 279 | 1.12 | 1.08 | 1.0344 | 0.1546 | 0.1339 | 0.2264 | 0.1502 | 0.0536 | 0.2191 | 0.1696 | 0.1799 | 0.3739 | 0.0753 | 0.4912 | -0.2869 | 0.89 | 2.85 |
| E-Commerce | 57 | 1.03 | 1.08 | 0.8813 | 0.064 | 0.0602 | 0.1647 | 0.1308 | 0.1233 | 0.1439 | 0.1087 | 0.1073 | 1.2844 | -0.116 | 0.0189 | -0.0256 | 1.2 | 4.55 |
| Educational Services | 34 | 0.83 | 0.92 | 0.7824 | 0.1233 | 0.1097 | 0.5322 | 0.3434 | 0.2517 | 0.208 | 0.1291 | 0.1186 | 1.3138 | -0.0782 | 0.0283 | 0.0807 | 2.66 | 1.14 |
| Electric Util. (Central) | 21 | 0.75 | 0.48 | 0.2337 | 0.8616 | 0.4628 | 0.1077 | 0.0638 | 0.3182 | 0.1772 | 0.1158 | 0.0889 | 1.5854 | 0.0898 | 0.6388 | 0.5689 | 0.55 | 2.26 |
| Electric Utility (East) | 21 | 0.7 | 0.49 | 0.183 | 0.6616 | 0.3982 | 0.1191 | 0.0689 | 0.3314 | 0.1913 | 0.1266 | 0.0977 | 2.0107 | 0.0833 | 0.6622 | 0.8235 | 0.54 | 2.51 |
| Electric Utility (West) | 14 | 0.75 | 0.49 | 0.1985 | 0.8454 | 0.4581 | 0.0988 | 0.0611 | 0.313 | 0.1679 | 0.1138 | 0.0853 | 2.1061 | -0.0059 | 0.567 | 1.1743 | 0.54 | 2.19 |
| Electrical Equipment | 68 | 1.33 | 1.35 | 0.6776 | 0.1266 | 0.1124 | 0.2302 | 0.1503 | 0.1702 | 0.1319 | 0.0995 | 0.1212 | 0.8614 | 0.1228 | 0.294 | 0.0917 | 1.51 | 1.54 |
| Electronics | 139 | 1.07 | 1.08 | 0.8993 | 0.2233 | 0.1825 | 0.222 | 0.1572 | 0.1036 | 0.0599 | 0.0448 | 0.0463 | 1.0397 | 0.1063 | 0.1197 | 0.1861 | 3.51 | 0.47 |
| Engineering & Const | 25 | 1.22 | 1.39 | 0.6503 | 0.1199 | 0.1071 | 0.1544 | 0.1358 | 0.2626 | 0.0472 | 0.0335 | 0.0347 | 0.8423 | 0.033 | 0.0631 | -0.0901 | 4.05 | 0.46 |
| Entertainment | 77 | 1.63 | 1.31 | 1.0837 | 0.4099 | 0.2907 | 0.1146 | 0.0945 | 0.1538 | 0.1772 | 0.1217 | 0.1012 | 0.7938 | 0.0172 | 0.2584 | -0.093 | 0.78 | 1.89 |
| Entertainment Tech | 40 | 1.23 | 1.48 | 0.7691 | 0.0976 | 0.0889 | 0.1508 | 0.1169 | 0.1159 | 0.1048 | 0.0904 | 0.0962 | 0.7889 | -0.1791 | 0.1157 | -0.2503 | 1.29 | 1.87 |
| Environmental | 82 | 0.81 | 0.6 | 0.9214 | 0.437 | 0.3041 | 0.11 | 0.0756 | 0.1171 | 0.1522 | 0.0948 | 0.0753 | 0.9646 | 0.0048 | 0.4673 | -0.0026 | 0.8 | 2.07 |
| Financial Svcs. (Div.) | 225 | 1.31 | 0.5 | 0.8227 | 2.5149 | 0.7155 | -3.0309 | 0.0595 | 0.1918 | 0.4349 | 0.3384 | 0.0508 | 3.1233 | 0.1108 | NA | 0.1338 | 0.18 | 6.67 |
| Food Processing | 112 | 0.91 | 0.77 | 0.6068 | 0.2953 | 0.228 | 0.1785 | 0.1188 | 0.2 | 0.0908 | 0.0652 | 0.0536 | 1.3977 | 0.0801 | 0.4525 | 0.2588 | 1.82 | 1.08 |
| Foreign Electronics | 9 | 1.09 | 1.24 | 0.354 | 0.4209 | 0.2962 | 0.0625 | 0.0783 | 0.3512 | 0.0527 | 0.0323 | 0.0183 | 0.7366 | 0.0147 | 0.5137 | -0.3915 | 2.43 | 0.37 |
| Funeral Services | 6 | 1.14 | 0.85 | 0.3935 | 0.566 | 0.3614 | 0.1234 | 0.0781 | 0.3084 | 0.1564 | 0.0982 | 0.0748 | 0.7863 | 0.0376 | 0.4981 | -0.0351 | 0.79 | 1.86 |
| Furn/Home Furnishings | 35 | 1.81 | 1.65 | 0.809 | 0.2439 | 0.1961 | 0.1166 | 0.095 | 0.2043 | 0.0643 | 0.0458 | 0.0376 | 0.6582 | 0.1345 | 0.2783 | -0.1243 | 2.08 | 0.92 |
| Healthcare Information | 25 | 1.17 | 1.2 | 0.6579 | 0.0635 | 0.0597 | 0.11 | 0.0945 | 0.2219 | 0.1211 | 0.0764 | 0.0881 | 0.5833 | 0.02 | 0.1222 | -0.4014 | 1.24 | 3.82 |
| Heavy Truck & Equip | 21 | 1.8 | 1.48 | 0.6992 | 0.4366 | 0.3039 | 0.3024 | 0.1088 | 0.2062 | 0.0913 | 0.0664 | 0.0848 | 0.9981 | 0.2435 | 0.3422 | 0.9467 | 1.64 | 1.34 |
| Homebuilding | 23 | 1.45 | 1.02 | 0.7 | 1.0028 | 0.5007 | -0.3582 | -0.0209 | 0.0512 | -0.0156 | -0.0209 | -0.0564 | 0.598 | 0.7653 | NA | NA | 1 | 1.23 |
| Hotel/Gaming | 51 | 1.74 | 1.28 | 0.7909 | 0.5207 | 0.3424 | 0.0564 | 0.0695 | 0.1453 | 0.1261 | 0.1013 | 0.0629 | 1.0945 | -0.0212 | 0.4037 | -0.0079 | 0.69 | 2.58 |
| Household Products | 26 | 1.07 | 0.95 | 0.6224 | 0.1899 | 0.1596 | 0.218 | 0.1452 | 0.2512 | 0.1738 | 0.1279 | 0.1166 | 1.1715 | 0.047 | 0.4897 | 0.0597 | 1.13 | 2.21 |
| Human Resources | 23 | 1.24 | 1.4 | 0.7827 | 0.1031 | 0.0935 | 0.0725 | 0.0767 | 0.2535 | 0.0191 | 0.0118 | 0.0166 | 0.696 | 0.0481 | 0.5059 | 0.2753 | 6.48 | 0.29 |
| Industrial Services | 137 | 0.93 | 0.81 | 0.7443 | 0.3271 | 0.2465 | 0.1376 | -0.535 | 0.1903 | -0.214 | -0.2367 | 0.0326 | 1.2745 | 0.1025 | 0.2498 | NA | 2.26 | 0.85 |
| Information Services | 27 | 1.07 | 0.89 | 0.481 | 0.3021 | 0.232 | 0.156 | 0.1083 | 0.1893 | 0.1933 | 0.1506 | 0.1194 | 0.644 | -0.0161 | 0.3873 | -0.2397 | 0.72 | 2.94 |
| Insurance (Life) | 30 | 1.58 | 1.54 | 0.5335 | 0.6414 | 0.3908 | 0.1045 | NA | 0.2804 | NA | NA | NA | NA | NA | 0.2939 | 0.0024 | NA | NA |
| Insurance (Prop/Cas.) | 49 | 0.91 | 1.01 | 0.3788 | 0.236 | 0.191 | 0.1332 | NA | 0.1936 | NA | NA | NA | 98.1235 | NA | 0.2346 | 0.5773 | NA | NA |
| Internet | 186 | 1.09 | 1.24 | 1.1709 | 0.0271 | 0.0263 | 0.3973 | 0.3275 | 0.0687 | 0.1825 | 0.1458 | 0.16 | 1.5437 | -0.0844 | 0.0066 | 0.0482 | 2.25 | 3.91 |
| IT Services | 60 | 1.06 | 1.14 | 0.6945 | 0.0609 | 0.0574 | 0.3611 | 0.2695 | 0.1915 | 0.1443 | 0.1032 | 0.1059 | 0.761 | 0.0288 | 0.3287 | -0.0473 | 2.61 | 1.75 |
| Machinery | 100 | 1.2 | 1.14 | 0.5721 | 0.1912 | 0.1605 | 0.1459 | 0.126 | 0.2215 | 0.1105 | 0.0822 | 0.0726 | 0.7532 | 0.1627 | 0.2538 | 0.0844 | 1.53 | 1.37 |
| Maritime | 52 | 1.4 | 0.58 | 0.6919 | 1.7038 | 0.6301 | 0.0488 | 0.0476 | 0.0555 | 0.1481 | 0.1369 | 0.0078 | 3.1685 | 0.0332 | 0.2525 | 2.1504 | 0.35 | 2.69 |
| Med Supp Invasive | 83 | 0.85 | 0.8 | 0.7918 | 0.1608 | 0.1385 | 0.2213 | 0.1588 | 0.1186 | 0.2222 | 0.1728 | 0.1664 | 0.8488 | 0.2214 | 0.2291 | 0.015 | 0.92 | 2.52 |
| Med Supp Non-Invasive | 146 | 1.03 | 1.07 | 0.8489 | 0.1302 | 0.1152 | 0.2956 | 0.1924 | 0.1273 | 0.0648 | 0.0481 | 0.0489 | 0.7877 | 0.0304 | 0.3729 | -0.0321 | 4 | 0.73 |
| Medical Services | 122 | 0.91 | 0.78 | 0.7626 | 0.4945 | 0.3309 | 0.3281 | 0.1855 | 0.1993 | 0.1111 | 0.0739 | 0.0484 | 0.919 | -0.0559 | 0.0882 | -0.2553 | 2.51 | 0.68 |
| Metal Fabricating | 24 | 1.59 | 1.63 | 0.6898 | 0.1549 | 0.1341 | 0.1866 | 0.1478 | 0.2655 | 0.1507 | 0.1089 | 0.0784 | 1.5415 | 0.1802 | 0.257 | 0.3262 | 1.36 | 1.67 |
| Metals & Mining (Div.) | 73 | 1.33 | 1.28 | 1.0438 | 0.141 | 0.1236 | 0.2479 | 0.1948 | 0.1104 | 0.3157 | 0.2188 | 0.0736 | 1.581 | 0.0622 | 0.3351 | 0.2326 | 0.89 | 2.47 |
| Natural Gas (Div.) | 29 | 1.33 | 1.06 | 0.4877 | 0.3707 | 0.2704 | 0.0904 | 0.071 | 0.2198 | 0.2894 | 0.175 | 0.1272 | 2.9708 | -0.0426 | 0.3381 | 2.7648 | 0.41 | 3.37 |
| Natural Gas Utility | 22 | 0.66 | 0.46 | 0.249 | 0.6738 | 0.4026 | 0.1098 | 0.0809 | 0.3016 | 0.128 | 0.0857 | 0.051 | 1.8403 | 0.0553 | 0.6728 | 0.4996 | 0.94 | 1.45 |
| Newspaper | 13 | 1.76 | 1.42 | 0.9074 | 0.4635 | 0.3167 | 0.1673 | 0.1105 | 0.2513 | 0.1459 | 0.0902 | 0.0311 | 0.456 | -0.0313 | 0.1456 | -0.323 | 1.23 | 1.31 |
| Office Equip/Supplies | 24 | 1.38 | 1.04 | 0.6426 | 0.6303 | 0.3866 | 0.1805 | 0.1036 | 0.2105 | 0.0665 | 0.0459 | 0.0407 | 0.6117 | 0.0678 | 0.2806 | -0.2089 | 2.26 | 0.55 |
| Oil/Gas Distribution | 13 | 0.96 | 0.65 | 0.5661 | 0.583 | 0.3683 | 0.1135 | 0.0683 | 0.137 | 0.1845 | 0.1446 | 0.098 | 2.8022 | -0.0001 | 0.7398 | 1.24 | 0.47 | 3.56 |
| Oilfield Svcs/Equip. | 93 | 1.55 | 1.39 | 0.6237 | 0.2292 | 0.1864 | 0.1048 | 0.0854 | 0.1739 | 0.1511 | 0.1128 | 0.1072 | 1.4322 | 0.1689 | 0.4188 | 0.7061 | 0.76 | 2.38 |
| Packaging & Container | 26 | 1.16 | 0.88 | 0.4159 | 0.5182 | 0.3413 | 0.1752 | 0.104 | 0.2423 | 0.1012 | 0.0702 | 0.1346 | 0.9261 | 0.0901 | 0.2438 | 1.0881 | 1.48 | 1.06 |
| Paper/Forest Products | 32 | 1.36 | 0.96 | 0.9384 | 0.5986 | 0.3745 | 0.084 | 0.1101 | 0.1061 | 0.1201 | 0.0984 | 0.0463 | 0.5463 | 0.1019 | 0.4321 | -0.2689 | 1.12 | 1.06 |
| Petroleum (Integrated) | 20 | 1.18 | 1.12 | 0.3899 | 0.1919 | 0.161 | 0.1476 | 0.1008 | 0.2741 | 0.0976 | 0.0565 | 0.0799 | 1.9287 | 0.0198 | 0.3899 | 0.8767 | 1.78 | 0.87 |
| Petroleum (Producing) | 176 | 1.34 | 1.13 | 0.8811 | 0.2488 | 0.1992 | 0.0946 | 0.135 | 0.1114 | 0.2574 | 0.191 | 0.1069 | 1.9231 | 0.0228 | 0.095 | 0.6409 | 0.71 | 2.2 |
| Pharmacy Services | 19 | 1.12 | 1 | 0.5943 | 0.2048 | 0.17 | 0.1482 | 0.1118 | 0.2467 | 0.0511 | 0.0314 | 0.0291 | 0.9952 | 0.0368 | 0.2026 | 0.0555 | 3.56 | 0.53 |
| Pipeline MLPs | 27 | 0.98 | 0.72 | 0.349 | 0.4097 | 0.2906 | 0.1271 | 0.086 | 0.0637 | 0.0895 | 0.0868 | 0.0711 | 1.8461 | 0.0088 | 0.3353 | 0.4379 | 0.99 | 1.97 |
| Power | 93 | 1.35 | 0.65 | 0.9719 | 1.4882 | 0.5981 | 0.0695 | 0.0756 | 0.0866 | 0.1454 | 0.1088 | 0.0149 | 1.8113 | 0.1094 | 0.1375 | 0.6425 | 0.69 | 1.48 |
| Precious Metals | 84 | 1.15 | 1.14 | 0.9087 | 0.082 | 0.0757 | 0.0909 | 0.0957 | 0.0751 | 0.333 | 0.2402 | 0.3024 | 2.03 | 0.0721 | 0.2671 | 0.6224 | 0.4 | 5.33 |
| Precision Instrument | 77 | 1.28 | 1.33 | 0.6533 | 0.1594 | 0.1375 | 0.1537 | 0.121 | 0.1394 | 0.1074 | 0.088 | 0.0957 | 0.4846 | 0.1514 | 0.1124 | 0.0204 | 1.38 | 1.64 |
| Property Management | 31 | 1.13 | 0.59 | 0.8221 | 1.4063 | 0.5844 | 0.1074 | 0.0518 | 0.1859 | 0.1563 | 0.1295 | 0.0918 | 2.2763 | -0.0302 | 0.2766 | 1.3737 | 0.4 | 2.85 |
| Public/Private Equity | 11 | 2.18 | 1.62 | 0.7754 | 0.5987 | 0.3745 | 0.3596 | -0.0014 | 0.0379 | -0.0258 | -0.0048 | 0.623 | 5.5433 | 0.3162 | 0.1728 | NA | 0.3 | 3.43 |
| Publishing | 24 | 1.25 | 0.89 | 0.6498 | 0.6328 | 0.3876 | 0.3194 | 0.1138 | 0.1855 | 0.121 | 0.0833 | 0.0622 | 0.7565 | 0.0081 | 0.2502 | -0.0851 | 1.37 | 1.15 |
| R.E.I.T. | 5 | 1.47 | 1.15 | 0.4961 | 0.3471 | 0.2577 | 0.1558 | 0.1407 | 0.0104 | 1.2907 | 1.2601 | 1.1355 | 0.895 | -0.1012 | 0.9136 | -0.0196 | 0.11 | 14.13 |
| Railroad | 12 | 1.44 | 1.24 | 0.4295 | 0.2515 | 0.2009 | 0.1643 | 0.111 | 0.2374 | 0.2843 | 0.1856 | 0.1786 | 1.7552 | -0.0176 | 0.3463 | 0.3617 | 0.6 | 3.44 |
| Recreation | 56 | 1.45 | 1.11 | 0.7055 | 0.4869 | 0.3275 | 0.1106 | 0.0826 | 0.1737 | 0.1151 | 0.0926 | 0.0728 | 1.747 | -0.0096 | 0.4267 | 0.5056 | 0.89 | 1.6 |
| Reinsurance | 13 | 0.93 | 1.05 | 0.304 | 0.2354 | 0.1906 | 0.1329 | NA | 0.0722 | NA | NA | NA | NA | NA | 0.1587 | 0.505 | NA | NA |
| Restaurant | 63 | 1.27 | 1.19 | 0.6837 | 0.1277 | 0.1132 | 0.3825 | 0.2032 | 0.2157 | 0.1582 | 0.1117 | 0.107 | 1.2428 | -0.0482 | 0.4673 | 0.0836 | 1.82 | 2.5 |
| Retail (Hardlines) | 75 | 1.77 | 1.65 | 0.9279 | 0.2433 | 0.1957 | 0.2291 | 0.1499 | 0.2304 | 0.075 | 0.0499 | 0.0386 | 2.1962 | 0.084 | 0.1962 | 0.864 | 3 | 0.83 |
| Retail (Softlines) | 47 | 1.44 | 1.57 | 0.6091 | 0.0561 | 0.0532 | 0.3627 | 0.2874 | 0.2464 | 0.0939 | 0.0582 | 0.0556 | 0.9655 | 0.034 | 0.2108 | 0.0099 | 4.94 | 0.87 |
| Retail Automotive | 20 | 1.37 | 1.12 | 0.5202 | 0.3811 | 0.2759 | 0.2053 | 0.0989 | 0.3443 | 0.0688 | 0.0446 | 0.0435 | 1.4044 | 0.1356 | 0.0249 | 0.4076 | 2.22 | 0.92 |
| Retail Building Supply | 8 | 1.04 | 0.97 | 0.3761 | 0.1406 | 0.1233 | 0.1606 | 0.1218 | 0.3139 | 0.0813 | 0.0513 | 0.0514 | 0.7827 | 0.0588 | 0.4732 | -0.0628 | 2.37 | 1.04 |
| Retail Store | 37 | 1.29 | 1.14 | 0.6771 | 0.2558 | 0.2037 | 0.2101 | 0.136 | 0.2502 | 0.0584 | 0.0383 | 0.0345 | 1.2902 | 0.0088 | 0.2916 | 0.1497 | 3.55 | 0.59 |
| Retail/Wholesale Food | 30 | 0.75 | 0.64 | 0.4002 | 0.4134 | 0.2925 | 0.1643 | 0.1038 | 0.3121 | 0.0318 | 0.0207 | 0.0416 | 1.2058 | -0.0001 | 0.2862 | 0.2306 | 5.02 | 0.35 |
| Securities Brokerage | 28 | 1.2 | 0.43 | 0.4431 | 4.3056 | 0.8115 | NA | 0.1039 | 0.2622 | 0.4878 | 0.3558 | 0.1145 | 0.8669 | 1.2316 | 0.1093 | -1.2666 | 0.29 | 3.08 |
| Semiconductor | 141 | 1.5 | 1.69 | 0.7052 | 0.0835 | 0.077 | 0.391 | 0.2841 | 0.1101 | 0.2276 | 0.1813 | 0.1782 | 1.0832 | 0.0693 | 0.3053 | 0.0583 | 1.57 | 2.06 |
| Semiconductor Equip | 12 | 1.79 | 2.42 | 0.687 | 0.152 | 0.132 | 0.6576 | 0.4044 | 0.1517 | 0.2165 | 0.183 | 0.163 | 1.0587 | 0.1251 | 0.113 | 0.0258 | 2.21 | 0.97 |
| Shoe | 19 | 1.25 | 1.38 | 0.5552 | 0.0218 | 0.0213 | 0.3049 | 0.2741 | 0.2431 | 0.1134 | 0.0822 | 0.0844 | 1.2384 | 0.1628 | 0.2589 | 0.1907 | 3.33 | 1.52 |
| Steel | 32 | 1.68 | 1.4 | 0.5694 | 0.464 | 0.3169 | 0.0728 | 0.0594 | 0.2103 | 0.0583 | 0.049 | 0.0352 | 0.6643 | 0.1141 | 0.3426 | -0.0639 | 1.21 | 0.78 |
| Telecom. Equipment | 99 | 1.02 | 1.28 | 0.8777 | 0.1296 | 0.1148 | 0.2993 | 0.233 | 0.1316 | 0.1087 | 0.0853 | 0.0722 | 0.6098 | -0.0338 | 0.5372 | -0.2125 | 2.73 | 1.25 |
| Telecom. Services | 74 | 0.98 | 0.82 | 0.6858 | 0.3409 | 0.2542 | 0.1647 | 0.137 | 0.1422 | 0.2274 | 0.1656 | 0.0511 | 0.9555 | -0.1238 | 0.4363 | -0.0554 | 0.83 | 1.85 |
| Telecom. Utility | 25 | 0.88 | 0.54 | 0.604 | 0.9615 | 0.4902 | 0.1829 | 0.0834 | 0.2942 | 0.1583 | 0.1121 | 0.085 | 0.7644 | -0.0776 | 0.8094 | -0.3732 | 0.74 | 1.75 |
| Thrift | 148 | 0.71 | 0.75 | 0.5393 | 0.2933 | 0.2268 | -0.0214 | NA | 0.1243 | NA | NA | NA | NA | NA | NA | 0 | NA | NA |
| Tobacco | 11 | 0.85 | 0.78 | 0.4153 | 0.1871 | 0.1576 | 0.7421 | 0.2798 | 0.3103 | 0.2061 | 0.1524 | 0.0846 | 0.6469 | -0.0244 | 0.6756 | -0.042 | 1.84 | 2.36 |
| Toiletries/Cosmetics | 15 | 1.3 | 1.2 | 0.6034 | 0.2064 | 0.1711 | 0.6253 | 0.1954 | 0.203 | 0.1085 | 0.0724 | 0.0737 | 1.1416 | 0.0855 | 0.2504 | 0.1339 | 2.7 | 1.48 |
| Trucking | 36 | 1.24 | 1.08 | 0.5988 | 0.2777 | 0.2173 | 0.0819 | 0.0907 | 0.2548 | 0.0637 | 0.042 | 0.0274 | 1.5692 | 0.0503 | 0.4107 | 0.9407 | 2.16 | 1.28 |
| Utility (Foreign) | 4 | 0.96 | 0.48 | 0.3268 | 1.5503 | 0.6079 | 0.0312 | 0.0456 | 0.2607 | 0.116 | 0.0781 | 0.0055 | 1.6469 | 0.0752 | 0.0032 | 1.3229 | 0.58 | 1.39 |
| Water Utility | 11 | 0.66 | 0.43 | 0.1889 | 0.8142 | 0.4488 | 0.0844 | 0.0542 | 0.3522 | 0.2661 | 0.1805 | 0.1225 | 2.5002 | 0.0751 | 0.4816 | 1.0715 | 0.3 | 4.39 |
| Wireless Networking | 57 | 1.27 | 1.12 | 0.7503 | 0.2706 | 0.213 | 0.2134 | -0.1821 | 0.1212 | -0.1147 | -0.1591 | 0.0796 | 0.8553 | 0.0762 | 0.0913 | NA | 1.14 | 1.91 |
| Total Market | 5891 | 1.15 | 0.92 | 0.7508 | 0.4664 | 0.3181 | 0.1607 | 0.1221 | 0.1548 | 0.1724 | 0.1262 | 0.0832 | 1.2547 | 0.0701 | 0.3792 | 0.0865 | 0.97 | 1.67 |

---

## Worked example (values currently in the sheet)

Firm: emerging-market conglomerate; all statement inputs in local currency (millions).

1. EBIT = 1751 LC → $875.5 at FX 2.0. After-tax: 875.5·0.725 = 634.7375.
2. MV debt = 11.4·(1−1.0655⁻³)/0.0655 + 188/1.0655³ = 185.58 LC. MV equity = 365·76 = 27740 LC. Debt ratio = 0.66456%.
3. CoE(high) = 0.05 + 1.5·0.06 + 0.25·0.0263 = 14.6575%. ATkd = 4.74875%. WACC = 14.5917%.
4. g = ROC·RR = 0.30·0.50 = 15% (user overrode computed ROC 37.45%, RR 51.52%).
5. Five years of FCFF = EBIT(1−t)·1.15^t·0.5 → PVs 318.50 … 323.06, sum 1603.89.
6. Terminal: EBIT(1−t)₆ = 1276.684·1.05 = 1340.518; stable RR = 0.05/0.11576875 = 0.431895; FCFF = 761.554; CoC_st = 0.9·0.124 + 0.1·0.0416875 = 0.11576875; TV = 761.554/0.0657688 = 11579.27; PV = 11579.27/1.97590 = 5860.25.
7. Operating assets 7464.14 + (3612+3937.07)/2.05 = 3682.47 non-operating → firm 11146.61; − debt 90.53 − MI 0 − options 0 → equity 11056.09 → **$145.47/share → 298.22 local at FX 2.05**.

---

## Reimplementation notes

**Inputs** (name: type, units):
- Toggles: capitalize_rnd, convert_leases, normalize_income, stock_traded, use_book_debt_ratio, keep_computed_debt_ratio, keep_wc_ratio, growth_from_fundamentals, override_fundamentals, three_stage (adjust inputs in 2nd half), stable_reinvest_from_fundamentals, has_options, option_price_basis ("P"/"V") — all bool/enum.
- Statement (float, local currency): ebit, interest_expense, capex, depreciation, revenues, revenues_prev, noncash_wc, chg_wc, bv_debt, bv_debt_prev, bv_equity, bv_equity_prev, cash, cash_prev, nonop_assets, minority_interest_bv, sector_pb.
- Market: stock_price, shares, avg_debt_maturity; rates: rf, mature_erp, crp_high, crp_stable, fx_fiscal, fx_fiscal_prev, fx_current; rating: firm_type ∈ {1,2,3} or (rating, cost_of_debt).
- Valuation: n_high (int, 0–10 columns supported), beta_high, beta_stable, **lambda** (single value, both phases), g_stable, debt_ratio_stable, kd_stable, tax_rate, marginal_tax_rate, tax_stable, roc_high, rr_high (or overrides), roc_stable or capex_pct_dep_stable.
- Options: n_options, strike, maturity, sigma; normalizer/R&D/lease sub-inputs as documented above.

**Outputs:** wacc_high, wacc_stable, per-year FCFF schedule, terminal value, value_of_operating_assets, firm_value, equity_value, value_per_share_usd, value_per_share_local; plus sub-model outputs (mv_debt, synthetic rating/spread, levered beta, lease debt, research asset, option value).

**Branches:**
1. EBIT source: raw → normalized (3 normalizer approaches) → + R&D adjustment → + lease adjustment.
2. Debt ratio: traded (computed MV ratio vs user ratio) vs non-traded (book vs input).
3. Growth: fundamental (ROC·RR, with optional overrides) vs direct input.
4. 2-stage vs 3-stage (linear glide of growth/beta/debt-ratio/RR over 2nd half of high-growth period — inferred, not exercised in this copy) vs stable-only (n_high = 0).
5. Rating: synthetic (3 lookup tables by firm type) vs user-supplied kd.
6. Stable reinvestment: g/ROC vs capex-as-%-of-depreciation.
7. Options: none vs dilution-adjusted BS (price basis P or V — V makes valuation circular with per-share value).

**Edge cases / quirks to preserve or consciously fix:**
- Circularities requiring fixed-point iteration: (a) MV debt uses kd which may come from the synthetic rating which uses interest coverage; (b) warrant value ↔ adjusted stock price; (c) option value basis "V" ↔ per-share value.
- Negative EBIT: model refuses — must normalize first or use another model.
- **ΔWC in forecast years is computed from local-currency revenues while the rest of the DCF is in dollars** (verified above). A faithful port must replicate; a clean port should convert revenues to dollars first (here FX is constant so effect = factor 2 on ΔWC, offset inside the net-capex plug, leaving FCFF unchanged — FCFF = EBIT(1−t)·(1−RR) regardless; only the ΔWC/netcapex split is affected).
- Net capex is a plug (reinvestment − ΔWC); total reinvestment is driven solely by RR·EBIT(1−t).
- Three FX rates: fiscal-year average (flows/current balance items), prior year-end (prior book values), current spot (cash + non-op + MV debt + per-share conversion). Cash in F67 converts at the current spot rate even though it is a fiscal-year balance item.
- Negative working capital (as here) makes ΔWC negative and inflates the netcapex plug; allowed.
- Rating lookup boundaries use the "greater than / ≤" bands exactly as tabulated (upper bounds like 2.2499999); coverage above 8.5/3.0/12.5 → AAA, below the floor → D.
- Terminal value: guard CoC_stable > g_stable; RR_stable = g/ROC gives 0 excess-return TV when ROC = CoC (the loaded example does exactly this).
- Lease year-6+ lump: divide by round(lump/avg first-5) years, discount as an annuity over that many years, then discount 5 years back; lease-asset depreciation straight-line over (5 + that estimate).
- R&D: max 10 years amortization; unamortized fraction linear.
- Display table supports max 10 forecast years despite read-me claiming 15; unused columns blank.

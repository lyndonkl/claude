# Damodaran Big-Picture Valuation Spreadsheets — fcffginzu.xlsx

Source: `/Users/kushaldsouza/Downloads/2020/Spreadsheets/Big Picture Valuation Spreadsheets/fcffginzu.xlsx` (.xlsx — live formulas visible; everything below is verbatim from formulas unless flagged "(inferred)").

### fcffginzu.xlsx

**Purpose:** Damodaran's flagship "Ginzu" FCFF (free cash flow to firm) valuation model. It values any firm with positive (or normalizable-to-positive) operating income, allowing up to 15 years of high growth. It can run as a 2-stage model (constant high-growth inputs, then stable growth), a 3-stage model (inputs fade linearly to stable levels over the second half of the high-growth period — set "adjust inputs in second half" = Yes), or a pure stable-growth model (high-growth length = 0). Sub-modules capitalize R&D, convert operating leases to debt, normalize earnings, estimate a synthetic bond rating from interest coverage, value employee options/warrants (dilution-adjusted Black-Scholes), and build a bottom-up cost of capital. Damodaran uses it as the general-purpose intrinsic-valuation workhorse for mature and growth firms alike.

**IMPORTANT — circularity:** the workbook deliberately contains circular references (Excel iterative calculation must be on). Circles: (a) synthetic cost of debt → operating-lease PV → adjusted EBIT/interest → coverage ratio → rating → cost of debt; (b) option value → per-share value → option value (when valuing options at estimated value); (c) market debt ratio → option value F69 → equity value → debt ratio; (d) stable reinvestment rate when computed as (S43−S46)/S43. A Python port must solve these by fixed-point iteration (or algebraically).

Sheets: `Read me first` (instructions only), `Master Inputs Start here`, `Valuation Model`, `Earnings Normalizer`, `R&D converter`, `Operating lease converter`, `Stories to Numbers`, `Option Value`, `Cost of capital worksheet`, `Ratings estimator`, `US Industry averages`, `Global Industry averages`, `Country ERP`, `Trailing 12-month numbers`, `Answers` (dropdown lists only). All sheets documented below. Units must be consistent (e.g. all in millions).

---

## Sheet: Master Inputs Start here

**Inputs** (label — cell — current example value; column C sometimes holds the *previous year-end* value):

Setup:
- Company name — B4 — "Caramba"
- Date of valuation — B5 — 2017-04-01
- Capitalize R&D expenses? — B6 — "No" (Yes → fill R&D converter sheet)
- Convert operating leases to debt? — B7 — "Yes" (Yes → fill Operating lease converter)
- Normalize operating income? — B8 — "No" (Yes → fill Earnings Normalizer)
- Country of incorporation — B9 — "Chile" (drives country default spread lookup in Ratings estimator)

From current financials:
- Current Operating Income (EBIT) — B12 — 1337.925 (must be positive, else normalize)
- Current Interest Expense — B13 — 255.258
- Current Capital Spending — B14 — 603.392
- Current Depreciation & Amortization — B15 — 356.2 (entered as `=1694.1-1337.9`)
- Effective tax rate (for operating income) — B16 — 0.31654 (`=373.3/1179.3`)
- Marginal tax rate (for cost of debt) — B17 — 0.34
- Current Revenues — B18 — 7010.31 ; previous year-end C18 = 6345.7
- Current Non-cash Working Capital — B19 — 483.7 (`=705.3+875.2+384.6-497.4-984`)
- Chg. Working Capital — B20 — −62.0 ; label C20 "Previous year-end"
- Book Value of Debt — B21 — 2609 ; previous year-end C21 = 2207.2
- Book Value of Equity — B22 — 915.4 ; previous year-end C22 = 1306.1
- Cash & Marketable Securities — B24 — 960.2 ; previous C24 = 1286.9
- Value of Non-operating Assets — B25 — 609.8 ; previous C25 = 566.6
- Minority interests — B26 — 17.7 ; previous C26 = 0

Market data:
- Is stock currently traded? — B29 — "Yes"
- Current Stock Price — B31 — 38.34
- Number of shares outstanding — B32 — 441.7058 (here `=16935/B31`, i.e. market cap / price)
- Market Value of Debt — B33 — `=B21` (2609)
- If not traded: use book value debt ratio? — B35 — "No"; if no, debt ratio to use — B36 — 0.35

General market data:
- Long Term Riskfree rate — B39 — 0.03
- Equity Risk Premium — B40 — 0.0785

Ratings:
- Estimate synthetic rating? — B43 — "Yes"
- If yes, type of firm — B44 — 2 (1 = large manufacturing, 2 = smaller/riskier, 3 = financial service — see Answers sheet J column). **Quirk:** the Ratings estimator sheet actually reads its own cell `'Ratings estimator'!C4` (currently 1), NOT B44 — B44 is not referenced by any formula. A port should use one firm-type input and treat B44/C4 as the same thing.
- If not, current rating — B45 — "BBB" (informational)
- Cost of debt for that rating — B46 — 0.0575 (used when B43="No")

Equity options outstanding:
- Options outstanding? — B49 — "No"
- Number of options — B50 — 50.998; Average strike — B51 — 40.35; Average maturity (yrs) — B52 — 8.3; Std dev of stock price — B53 — 0.25
- Value option off stock price or estimated value/share? — B54 — "Current Price" (other choice: "Estimated Value" → circular)

High growth period:
- Length of high growth period — B58 — 10 (0–15; 0 makes it a stable-growth model)
- Beta for high growth — B59 — 1.14
- Keep debt ratio computed from inputs? — B60 — "Yes"
  - Computed debt ratio — B61 (formula):
    `=IF(B29="Yes", IF(B7="Yes", 1-(B31*B32+'Valuation Model'!F69)/(B33+B31*B32+'Valuation Model'!F69+'Operating lease converter'!C30), 1-(B31*B32)/(B33+B31*B32)), IF(B35="Yes", B21/(B21+B22), B36))`
    i.e. market D/(D+E) with option value counted in equity and lease debt in debt; falls back to book ratio or B36 for untraded firms. Currently 0.193108.
  - If no, debt ratio to use — B62 — 0.07
- Keep existing WC/revenue ratio? — B63 — "Yes"; computed B64 `=B19/B18` = 0.0689984; else B65 — 0.12
- Compute growth from fundamentals? — B66 — "Yes"; if No, growth rate — B67 — 0.15
- Computed fundamentals:
  - Return on Capital — B69: `=IF(B6="Yes", ('Valuation Model'!D3*(1-'Valuation Model'!D7)+'R&D converter'!D40)/('Valuation Model'!D11+'Valuation Model'!D12-C24-C25), ('Valuation Model'!D3*(1-'Valuation Model'!D7))/('Valuation Model'!D11+'Valuation Model'!D12-C24-C25))` = adjusted EBIT×(1−marginal tax) [+ R&D tax effect if capitalizing] ÷ (prior-year adjusted BV debt + prior-year adjusted BV equity − prior cash − prior non-operating assets). Currently 0.340504.
  - Reinvestment Rate — B70: `=('Valuation Model'!D5-'Valuation Model'!D6+'Valuation Model'!D10)/'Valuation Model'!C43` = (adj CapEx − adj Depreciation + ΔWC) / current adjusted EBIT(1−t_eff). Currently 0.508400.
- Override these? — B71 — "No"; overrides: ROC B72 — 0.33, RR B73 — `=B70`
- Gradually adjust high-growth inputs in second half? — B75 — "Yes" (this is the 2-stage vs 3-stage switch)

Stable growth period:
- Stable growth rate — B78 — 0.03 (should be ≤ riskfree rate)
- Stable beta — B79 — 1
- Stable ERP — B80 — 0.075
- Stable debt ratio — B81 — 0.3
- Stable pre-tax cost of debt — B82 — 0.09
- Stable tax rate — B83 — 0.34
- Compute stable reinvestment from fundamentals? — B85 — "Yes"; stable ROC — B86 — 0.25; if No: CapEx as % of depreciation in stable growth — B87 — 1.2

---

## Sheet: Valuation Model (the engine and output)

### Input summary block (rows 2–12) — adjusted current-year numbers

- D2 Normalized EBIT: `=IF(MI!B8="Yes",'Earnings Normalizer'!D14,MI!B12)` (MI = Master Inputs)
- D3 Adjusted EBIT: D2 + R&D adjustment `'R&D converter'!D39` (if B6=Yes) + lease adjustment `'Operating lease converter'!F34` (if B7=Yes). Currently 1601.2675.
- D4 Adjusted Interest Expense: `=IF(MI!B7="Yes", MI!B13 + LeaseDebt(C30)*PreTaxCostOfDebt(C14), MI!B13)` = 323.6534
- D5 Adjusted CapEx: MI!B14 + current R&D `'R&D converter'!F7` (if B6=Yes) + current lease expense `'Operating lease converter'!E3` (if B7=Yes) = 1107.392
- D6 Adjusted Depreciation: MI!B15 + R&D amortization `'R&D converter'!D37` (if B6=Yes) + lease depreciation `'Operating lease converter'!F33` (if B7=Yes) = 596.8575
- D7 Tax Rate on Income: `=MI!B17` (marginal, 0.34) — used for after-tax cost of debt AND in D3×(1−D7) for ROC
- D8 Current Revenues `=MI!B18`; D9 Non-cash WC `=MI!B19`
- D10 Chg. Working Capital: `=IF(MI!B20<0,(MI!B18-MI!C18)*(MI!B19/MI!B18),MI!B20)` — if the entered ΔWC is negative, replace with ΔRevenue × (WC/Revenue). = 45.8570
- D11 Adjusted BV of Debt (prior year): `=IF(MI!B7="Yes",MI!C21+'Operating lease converter'!F35,MI!C21)` = 3651.1451
- D12 Adjusted BV of Equity (prior year): `=IF(MI!B6="Yes",MI!C22+'R&D converter'!D35-'R&D converter'!D24+'R&D converter'!E35,MI!C22)` (prior BV equity + research asset − current-year R&D layer + current amortization ⇒ research asset as of prior year) = 1306.1

### Assumption columns: D = high growth, E = stable (rows 14–24), with diagnostics in F

- D14 length N `=MI!B58`; E14 "Forever"
- D15 high-growth g: `=IF(MI!B66="Yes", D23*D24, MI!B67)` (ROC × RR = 0.173112); E15 stable g `=MI!B78`
- D16 debt ratio: `=IF(MI!B60="Yes",MI!B61,MI!B62)`; E16 `=MI!B81`
- D17 beta `=MI!B59`; E17 `=MI!B79` (diagnostic: cap 1.20 / floor 0.80)
- D18 riskfree `=MI!B39`; E18 `=D18`
- D19 ERP `=MI!B40`; E19 `=MI!B80`
- D20 pre-tax cost of debt: `=IF(MI!B43="Yes",'Ratings estimator'!D13,MI!B46)` = 0.0473670; E20 `=MI!B82`
- D21 effective tax `=MI!B16`; E21 `=MI!B83`
- D22 marginal tax `=MI!B17`; E22 `=MI!B83`
- D23 ROC: `=IF(MI!B71="Yes",MI!B72,MI!B69)`; E23 `=MI!B86`
- D24 RR: `=IF(MI!B71="Yes",MI!B73,MI!B70)`; E24 stable RR: `=IF(MI!B85="Yes", MI!B78/MI!B86, (S43-S46)/S43)` = g/ROC_stable = 0.12
- H24 imputed stable ROC: `=IF(E24<0.0001,"Infinite ROC…",E15/E24)`

Diagnostics (column F, informational strings only): N>10 warning; stable g > riskfree warning; stable debt ratio = high-growth ratio note; stable beta outside [0.8,1.2]; stable cost of debt > rf+3% or < rf; stable tax < 35% (US note); stable ROC > stable WACC+5% or < WACC.

### Cost of capital (high growth), rows 27–31

- D27 Cost of equity `=D18+D17*D19` = 0.11949
- D28 E/(D+E) `=1-D30`; D30 = D16
- D29 After-tax cost of debt `=D20*(1-D7)` (marginal tax) = 0.0312622
- D31 Cost of capital `=D27*D28+D29*D30` = 0.1024525

### Year-by-year projection (columns D…R = years 1…15, C = current, S = terminal year)

Row 37 year indices: `=IF(D14<k," ",k)` — years beyond N are blanked to " ".

Row 38 Expected growth g_t (per year t, columns D–R):
`=IF($D$14<t," ", IF(MI!$B$75="Yes", IF(t<MI!$B$58/2, $D$15, $D$51+(($D$15-$D$51)/(MI!$B$58/2))*(MI!$B$58-t)), $D$15))`
i.e. 2-stage: g_t = g_high for all t; 3-stage (B75=Yes): g_t = g_high for t < N/2, then linear fade g_t = g_stable + (g_high−g_stable)·(N−t)/(N/2) reaching g_stable at t=N. (D51 = stable g.)

Row 39 Cumulated growth: `=Π(1+g_1..g_t)`.

Row 40 Reinvestment rate RR_t: same fade structure with $D$24 (high) and $D$52 (stable RR, see below):
`=IF(t<N/2, D24, D52+((D24-D52)/(N/2))*(N-t))` when B75="Yes", else D24.

Row 41 EBIT: C41 base `=IF(MI!B6="yes",D3+'R&D converter'!D40,D3)` (adds R&D tax effect if capitalizing) = 1601.2675; then EBIT_t = EBIT_{t−1}×(1+g_t).

Row 42 tax rate (for cash flow): C42 `=MI!B16` (effective); t_i `=$S$42-($D$14-i)*($S$42-$C$42)/$D$14` with S42 `=MI!B83` — linear ramp from effective tax rate toward the stable tax rate, reaching S42 in year N.

Row 43 EBIT(1−t): C43 `=C41*(1-C42)`; per year `=EBIT_t*(1-t_t)`.
S43 (terminal-year EBIT(1−t)): `=(MAX(C43:R43)/(1-D22))*(1-E22)*(1+D51)` — takes the max after-tax EBIT over the path, grosses it up to pre-tax at the *marginal* rate D22, re-taxes at the stable rate E22, grows one year at stable g.

Row 44 (CapEx−Depreciation): C44 `=D5-D6`; per year `=RR_t*EBIT(1-t)_t - ΔWC_t` (i.e. total reinvestment minus the WC component).
S44 terminal: `=IF(MI!B85="yes", E24*S43-S45, (MI!B87-1)*D6*(1+D34)^D14*(1+D51))` — fundamentals: stable RR × terminal NOPAT − terminal ΔWC; else (CapEx/Depr − 1) × current adjusted depreciation grown at g_high^N then ×(1+g_stable).

Row 45 ΔWC: C45 `=D10`; year 1 `=D8*(cumgrowth_1-1)*D35`; year t `=D8*(cumgrowth_t-cumgrowth_{t-1})*D35` where D35 = WC/revenues `=IF(MI!B63="Yes",MI!B64,MI!B65)`.
S45 terminal: `=(D8*(1+D34)^D14*(1+D51)-D8*(1+D34)^D14)*D35` — note it grows revenue N years at **D34** (the *initial* fundamental growth, `=IF(MI!B66="No",MI!B67,IF(MI!B71="No",MI!B69*MI!B70,MI!B72*MI!B73))`, NOT the faded path), then one stable-growth year.

Row 46 FCFF: `=EBIT(1-t) - (CapEx-Depr) - ΔWC` per year; S46 `=S43-S44-S45`.

Row 47 Cost of capital per year: same N/2 fade structure between $D$31 (high, D31) and $D$58 (stable WACC) when B75="Yes"; else D31 throughout.

Row 48 Cumulated cost of capital: `=Π(1+wacc_1..wacc_t)`.

Row 49 Present value: `=FCFF_t / cumWACC_t`.

### Stable phase block (rows 51–59)

- D51 stable g `=MI!B78` = 0.03
- D52 stable RR `=(S44+S45)/S43` = 0.12
- D53 terminal FCFF `=S46` = 3222.2229
- D54 stable cost of equity `=E18+E17*E19` = 0.105
- D55 `=1-E16` = 0.7; D56 stable AT cost of debt `=E20*(1-E22)` = 0.0594; D57 `=1-D55`
- D58 stable cost of capital `=D54*D55+D56*D57` = 0.09132
- D59 terminal value `=D53/(D58-D51)` = 52547.666

### Valuation block (rows 61–73) — **Outputs**

- F61 PV of FCFF in high growth `=SUM(D49:R49)` = 8579.819
- F62 PV of terminal value `=IF(MI!B58=0, D59, D59/MAX(D48:R48))` = 20424.904
- F63 Value of operating assets `=F61+F62` = 29004.722
- F64 + Cash & non-operating assets `=MI!B24+MI!B25` = 1570
- F65 Value of Firm `=F63+F64` = 30574.722
- F66 − Market value of debt `=IF(MI!B7="Yes", IF(MI!B29="Yes",MI!B33+LeaseDebt, MI!B21+LeaseDebt), IF(MI!B29="Yes",MI!B33,MI!B21))` = 4052.945 (LeaseDebt = 'Operating lease converter'!F35)
- F67 − Minority interests `=MI!B26` = 17.7
- F68 Market value of equity `=F65-F66-F67` = 26504.077
- F69 − Value of equity options `=IF(MI!B49="Yes",'Option Value'!D27*(1-MI!B17),0)` (option value is tax-effected at the marginal rate) = 0
- F70 Value of equity in common stock `=F68-F69` = 26504.077
- F71 Value per share `=F70/MI!B32` = **60.0039**
- F72 Stock price `=MI!B31` = 38.34
- F73 % under/over valued `=F72/F71-1` = **−36.10%** (negative ⇒ undervalued)

---

## Sheet: Earnings Normalizer

**Purpose:** produce a positive normalized EBIT when current EBIT is negative/depressed. Used when MI!B8="Yes" (feeds Valuation Model D2).

**Inputs:** D2 approach selector (1, 2, or 3) — currently 3; D5 average historical EBIT (approach 1) — 3500; D8 historical average pre-tax ROC (approach 2) — 0.22; D11 sector pre-tax operating margin (approach 3) — `=G21` (defaults to own 5-yr aggregate margin; user may type an industry-average margin). Worksheet rows 18–21: last 5 years of Revenues (B19:F19 = 2032, 2376, 2779, 3155, 3248) and EBIT (B20:F20 = 186, 454, 529, 448, 383), with totals G19=13590, G20=2000 and margins row 21 (`=EBIT/Rev` per year; G21 `=G20/G19` = 0.147167).

**Logic:** D14 `=IF(D2=1, D5, IF(D2=2, D8*(MI!B21+MI!B22), D11*MI!B18))`
- Approach 1: historical average EBIT.
- Approach 2: historical avg pre-tax ROC × (current BV debt + current BV equity).
- Approach 3: sector (or own aggregate) pre-tax margin × current revenues.
Currently: 0.147167 × 7010.31 = 1031.687.

**Output:** D14 Normalized EBIT.

---

## Sheet: R&D converter

**Purpose:** capitalize R&D — restates EBIT, capex, depreciation, and book equity as if R&D were a capital expense amortized straight-line over an industry-specific life. Used when MI!B6="Yes".

**Inputs:** F6 amortization life N_rd (years, max 10) — 5; F7 current-year R&D — 1771; B11:B20 past R&D for years −1…−N_rd (needed count auto-driven by F6): −1:1678, −2:1529, −3:1367, −4:1267, −5:1205. (A12:A20 auto-fill year indices: `=IF((0-A_prev)<$F$6, IF(A_prev>-1,, A_prev-1),)` — 0 beyond the life.)

**Logic (rows 24–34, one row per vintage):**
- Unamortized fraction: current year = 1; year −k: `=(N_rd + (−k))/N_rd` = (N_rd−k)/N_rd (0 for k ≥ N_rd).
- Unamortized value D = R&D × fraction; amortization this year E = R&D_{−k}/N_rd for k=1…N_rd (current year contributes none).
- D35 Value of Research Asset `=SUM(D24:D34)` = 4831
- E35 total current amortization `=SUM(E25:E34)` = 1409.2 ; D37 `=E35`
- D39 Adjustment to Operating Income `=F7-D37` = 361.8 (add to reported EBIT)
- D40 Tax Effect of R&D Expensing `=(F7-D37)*MI!B17` = 123.012 (added to EBIT(1−t) in ROC (MI!B69) and to base-year EBIT C41)

**Outputs consumed elsewhere:** D39 (EBIT adj), D37 (depreciation adj), F7 (capex adj), D35/E35/D24 (book-equity adj in Valuation Model D12), D40 (tax effect).

**Reference data — R&D amortization-period lookup (A45:B142), guidance box: Non-technological Service 2 yrs; Retail/Tech Service 3; Light Manufacturing 5; Heavy Manufacturing 10; Research with Patenting 10; Long Gestation Period 10:**

| Industry | Yrs | | Industry | Yrs | | Industry | Yrs |
|---|---|---|---|---|---|---|---|
| Advertising | 2 | | Electric Utility (West) | 10 | | Natural Gas (Diversified) | 10 |
| Aerospace/Defense | 10 | | Electrical Equipment | 10 | | Newspaper | 3 |
| Air Transport | 10 | | Electronics | 5 | | Office Equip & Supplies | 5 |
| Aluminum | 5 | | Entertainment | 3 | | Oilfield Services/Equip. | 5 |
| Apparel | 3 | | Environmental | 5 | | Packaging & Container | 5 |
| Auto & Truck | 10 | | Financial Services | 2 | | Paper & Forest Products | 10 |
| Auto Parts (OEM) | 5 | | Food Processing | 3 | | Petroleum (Integrated) | 5 |
| Auto Parts (Replacement) | 5 | | Food Wholesalers | 3 | | Petroleum (Producing) | 5 |
| Bank | 2 | | Foreign Electron/Entertn | 5 | | Precision Instrument | 5 |
| Bank (Canadian) | 2 | | Foreign Telecom. | 10 | | Publishing | 3 |
| Bank (Foreign) | 2 | | Furn./Home Furnishings | 3 | | R.E.I.T. | 3 |
| Bank (Midwest) | 2 | | Gold/Silver Mining | 5 | | Railroad | 5 |
| Beverage (Alcoholic) | 3 | | Grocery | 2 | | Recreation | 5 |
| Beverage (Soft Drink) | 3 | | Healthcare Info Systems | 3 | | Restaurant | 2 |
| Building Materials | 5 | | Home Appliance | 5 | | Retail (Special Lines) | 2 |
| Cable TV | 10 | | Homebuilding | 5 | | Retail Building Supply | 2 |
| Canadian Energy | 10 | | Hotel/Gaming | 3 | | Retail Store | 2 |
| Cement & Aggregates | 10 | | Household Products | 3 | | Securities Brokerage | 2 |
| Chemical (Basic) | 10 | | Industrial Services | 3 | | Semiconductor | 5 |
| Chemical (Diversified) | 10 | | Insurance (Diversified) | 3 | | Semiconductor Cap Equip | 5 |
| Chemical (Specialty) | 10 | | Insurance (Life) | 3 | | Shoe | 3 |
| Coal/Alternate Energy | 5 | | Insurance (Prop/Casualty) | 3 | | Steel (General) | 5 |
| Computer & Peripherals | 5 | | Internet | 3 | | Steel (Integrated) | 5 |
| Computer Software & Svcs | 3 | | Investment Co. (Domestic) | 3 | | Telecom. Equipment | 10 |
| Copper | 5 | | Investment Co. (Foreign) | 3 | | Telecom. Services | 5 |
| Diversified Co. | 5 | | Investment Co. (Income) | 3 | | Textile | 5 |
| Drug | 10 | | Machinery | 10 | | Thrift | 2 |
| Drugstore | 3 | | Manuf. Housing/Rec Veh | 5 | | Tire & Rubber | 5 |
| Educational Services | 3 | | Maritime | 10 | | Tobacco | 5 |
| Electric Util. (Central) | 10 | | Medical Services | 3 | | Toiletries/Cosmetics | 3 |
| Electric Utility (East) | 10 | | Medical Supplies | 5 | | Trucking/Transp. Leasing | 5 |
| | | | Metal Fabricating | 10 | | Utility (Foreign) | 10 |
| | | | Metals & Mining (Div.) | 5 | | Water Utility | 10 |
| | | | Natural Gas (Distrib.) | 10 | | | |

---

## Sheet: Operating lease converter

**Purpose:** convert operating-lease commitments to debt and restate EBIT/depreciation/debt. Used when MI!B7="Yes".

**Inputs:** E3 current-year operating lease expense — 504; commitment schedule B6:B10 for years 1–5 — 453, 371, 265, 180, 122; B11 "6 and beyond" lump sum — 259.

**Logic:**
- C14 pre-tax cost of debt (discount rate): `=IF(MI!B43="Yes",'Ratings estimator'!D13,MI!B46)` = 0.0473670 (circular with ratings — see above)
- D20 number of years embedded in the yr-6+ lump: `=IF(B11>0, ROUND(B11/AVERAGE(B6:B10),0), 0)` = 1 (avg of yrs 1–5 = 278.2; 259/278.2 rounds to 1)
- C24:C28 PV of yrs 1–5: `=B_t/(1+C14)^t`
- B29 annualized yr-6+ commitment: `=IF(B11>0, IF(D20>0, B11/D20, B11), 0)`
- C29 PV of yr-6+ as an annuity of D20 years starting year 6: `=IF(D20>0, (B29*(1-(1+C14)^(-D20))/C14)/(1+C14)^5, B29/(1+C14)^6)` = 196.203
- C30 Debt value of leases `=SUM(C24:C29)` = 1443.945
- F33 Depreciation on lease asset (straight line over 5+D20 yrs): `=C30/(5+D20)` = 240.658
- F34 Adjustment to Operating Earnings: `=E3-F33` (lease expense − depreciation) = 263.342
- F35 Adjustment to total debt: `=C30`

**Outputs consumed elsewhere:** C30/F35 (debt), F33 (depreciation adj), F34 (EBIT adj), C30×C14 (imputed lease interest added to interest expense), E3 (added to capex in Valuation Model D5).

---

## Sheet: Stories to Numbers (output/summary only, no inputs)

Recasts the valuation as a story table: high-growth vs stable growth rate, ROC, cost of capital, ROC−WACC spread, reinvestment rate, growth split into "new investment growth" (ROC×RR) and "efficiency growth" (g − ROC×RR). Valuation decomposition:
- E20 Value of assets in place `='Valuation Model'!C41/'Valuation Model'!D58` (current EBIT after adj ÷ stable WACC — a no-growth perpetuity; note it uses pre-tax C41) = 17534.686
- E21 Value created by growth `=OperatingAssets − E20` = 11470.037; F20/F21 percentage split.
Then repeats the value bridge (PV high-growth CF, terminal value, PV TV, +cash, −debt & minorities, −options, per-share, price, % under/over). All cells are references to Valuation Model — no new logic.

---

## Sheet: Option Value

**Purpose:** dilution-adjusted Black–Scholes value of employee options/warrants; feeds Valuation Model F69.

**Inputs (all pulled from Master Inputs except dividend yield):** D2 stock price `=IF(MI!B54="Current Price",MI!B31,'Valuation Model'!F71)` (using estimated value F71 creates circularity) = 38.34; D3 strike `=MI!B51` = 40.35; D4 maturity `=MI!B52` = 8.3; D5 σ `=MI!B53` = 0.25; **D6 annualized dividend yield — direct input on this sheet — 0**; D7 T-bond rate `=MI!B39` = 0.03; D8 # warrants `=MI!B50` = 50.998; D9 # shares `=MI!B32` = 441.7058.

**Logic (warrant dilution):**
- C15 Adjusted S: `=(C13*F14 + C26*F13)/(F14+F13)` = (S·n_shares + W·n_warrants)/(n_shares+n_warrants) — W is the option value itself (C26), so this is circular; solve iteratively. = 35.5739
- C16 Adjusted K = strike; F16 variance = σ²; F18 div-adjusted rate = r − y
- B20 d1 `=(LN(C15/C16)+(F18+F16/2)*C17)/(SQRT(F16)*SQRT(C17))` = 0.530926; B21 N(d1) via NORMSDIST = 0.702265
- B23 d2 `=B20-SQRT(F16)*SQRT(C17)` = −0.189317; B24 N(d2) = 0.424922
- C26 value per option `=EXP(-y*T)*S_adj*N(d1) - K*EXP(-r*T)*N(d2)` = 11.6159
- D27 value of all options `=C26*D8` = 592.389

(Note the model applies (1−marginal tax) to D27 in Valuation Model F69.)

---

## Sheet: Cost of capital worksheet (standalone helper; NOT auto-wired into the valuation — its results are meant to be copied into MI!B59/B40 etc.)

**Inputs:** B4 shares `=MI!B32`; B5 price `=MI!B31`; B7 unlevered beta `=K48` (from the US multi-business calculator below; can be typed); B8 riskfree `=MI!B39`; B9 ERP `=K18` (from the operating-countries calculator); B12 BV straight debt `=MI!B21`; B13 interest expense `=MI!B13`; B14 average debt maturity — 5; B15 pre-tax cost of debt — 0.0365; B16 tax `=MI!B17`; B18:B21 convertible debt (BV, interest, maturity, market value) — all 0; B23 lease debt `=IF(MI!B7="Yes",'Operating lease converter'!C30,0)`; B26:B28 preferred (shares 0, price 70, dividend 5).

**Logic:**
- C31 market value of straight debt (price the book debt as a coupon bond): `=B13*(1-(1+B15)^-B14)/B15 + B12/(1+B15)^B14` = 3328.482
- C32 straight-debt portion of convertible: same formula on B19/B18/B20; C34 equity portion `=B21-C32`
- C33 lease debt `=B23`
- C35 levered beta: `=B7*(1+(1-B16)*(C38/B38))` (D/E in market values) = 1.26967
- Row 38 market values: equity B38 `=B4*B5`; debt C38 `=C31+C32+C33`; preferred D38 `=B26*B27`; capital E38 = sum
- Row 39 weights; Row 40 component costs: equity `=B8+C35*B9`, debt `=B15*(1-B16)`, preferred `=B28/B27`; E40 WACC `=ΣwᵢcostᵢB` = 0.077592
- ERP calculators: country table (G4:K18) — per row ERP `=VLOOKUP(country,'Country ERP'!A5:F181,4)`, weight = revenues/total, K18 = Σ weighted ERP. Region table (G20:K32) — ERPs from 'Country ERP' rows 185–193. Example: Chile 100% → 0.0493589.
- Multi-business bottom-up beta, US (G35:K48) and Global (G51:K64): per business, EV/Sales `=VLOOKUP(business, industry-averages A2:Z95, col 15)` and unlevered beta `=VLOOKUP(…, col 7)`; estimated value = revenues × EV/Sales; company unlevered beta K48/K64 = value-weighted average of business betas.

**Outputs:** E40 WACC, C35 levered beta, K18/K32 weighted ERPs, K48/K64 unlevered betas, C31 market value of debt.

---

## Sheet: Ratings estimator

**Purpose:** synthetic bond rating from interest coverage, → company default spread, + country default spread → pre-tax cost of debt. Feeds Valuation Model D20 and the lease converter's discount rate when MI!B43="Yes".

**Inputs:** C4 type of firm — 1 = large manufacturing (market cap > $5B (inferred)), 2 = smaller/riskier, 3 = financial service. (See quirk note: MI!B44 is ignored.) F5 EBIT `=IF(MI!B7="No", MI!B12, MI!B12+'Operating lease converter'!F34)` = 1601.2675; F6 interest expense `=IF(MI!B7="Yes", MI!B13+'Operating lease converter'!C30*C14_lease, MI!B13)` = 323.6534; F7 riskfree `=MI!B39`.

**Logic:**
- D9 interest coverage ratio: `=IF(F6=0, 1000000, IF(F5<0, -100000, F5/F6))` = 4.94748 (zero interest ⇒ +1,000,000 ⇒ AAA; negative EBIT ⇒ −100,000 ⇒ D)
- D10 rating: `=IF(C4=1, VLOOKUP(D9,A19:D33,3), IF(C4=2, VLOOKUP(D9,A38:D52,3), VLOOKUP(D9,F19:I33,3)))` = "A2/A". VLOOKUP is range-lookup on the lower bound (column A/F = "greater than" threshold). **Note: the type-3 (financial service) table at F19:I33 is EMPTY in this workbook — type 3 would #N/A. A port should either reuse table 1 or flag unsupported.** (The G38:H53 block is a plain rating→spread list, apparently unused by formulas.)
- D11 company default spread: same VLOOKUPs, column 4 = 0.0113796
- D12 country default spread: `=VLOOKUP(MI!B9,'Country ERP'!A5:F179,3)` (Chile → 0.00598739)
- D13 estimated cost of debt: `=F7+D11+D12` = 0.0473670

**Reference data — coverage → rating → spread (VERBATIM, full precision):**

Table 1, large manufacturing firms (A19:D33). "If interest coverage ratio is > col1 and ≤ col2":

| > | ≤ | Rating | Spread |
|---|---|---|---|
| -100000 | 0.199999 | D2/D | 0.14335607034015696 |
| 0.2 | 0.649999 | Caa/CCC | 0.10755403832538094 |
| 0.65 | 0.799999 | Ca2/CC | 0.088 |
| 0.8 | 1.249999 | C2/C | 0.0777645323482633 |
| 1.25 | 1.499999 | B3/B- | 0.046159909223396155 |
| 1.5 | 1.749999 | B2/B | 0.03776719845550594 |
| 1.75 | 1.999999 | B1/B+ | 0.03147266537958828 |
| 2 | 2.2499999 | Ba2/BB | 0.02152617442092565 |
| 2.25 | 2.49999 | Ba1/BB+ | 0.019341413179589748 |
| 2.5 | 2.999999 | Baa2/BBB | 0.01591065804294902 |
| 3 | 4.249999 | A3/A- | 0.012863935805589465 |
| 4.25 | 5.499999 | A2/A | 0.011379635520329143 |
| 5.5 | 6.499999 | A1/A+ | 0.010307640869863355 |
| 6.5 | 8.499999 | Aa2/AA | 0.008246112695890684 |
| 8.5 | 100000 | Aaa/AAA | 0.006660321792834782 |

Table 2, smaller and riskier firms (A38:D52); spreads are cell references to table 1 (same values, different coverage bands):

| > | ≤ | Rating | Spread |
|---|---|---|---|
| -100000 | 0.499999 | D2/D | 0.14335607034015696 |
| 0.5 | 0.799999 | Caa/CCC | 0.10755403832538094 |
| 0.8 | 1.249999 | Ca2/CC | 0.088 |
| 1.25 | 1.499999 | C2/C | 0.0777645323482633 |
| 1.5 | 1.999999 | B3/B- | 0.046159909223396155 |
| 2 | 2.499999 | B2/B | 0.03776719845550594 |
| 2.5 | 2.999999 | B1/B+ | 0.03147266537958828 |
| 3 | 3.499999 | Ba2/BB | 0.02152617442092565 |
| 3.5 | 3.9999999 | Ba1/BB+ | 0.019341413179589748 |
| 4 | 4.499999 | Baa2/BBB | 0.01591065804294902 |
| 4.5 | 5.999999 | A3/A- | 0.012863935805589465 |
| 6 | 7.499999 | A2/A | 0.011379635520329143 |
| 7.5 | 9.499999 | A1/A+ | 0.010307640869863355 |
| 9.5 | 12.499999 | Aa2/AA | 0.008246112695890684 |
| 12.5 | 100000 | Aaa/AAA | 0.006660321792834782 |

Auxiliary rating→spread list at G38:H53 (order as in sheet; not referenced by any formula):
A1/A+ 0.010307640869863355; A2/A 0.011379635520329143; A3/A- 0.012863935805589465; Aa2/AA 0.008246112695890684; Aaa/AAA 0.006660321792834782; B1/B+ 0.03147266537958828; B2/B 0.03776719845550594; B3/B- 0.046159909223396155; Ba1/BB+ 0.019341413179589748; Ba2/BB 0.02152617442092565; Baa2/BBB 0.01591065804294902; C2/C 0.10755403832538094; Ca2/CC 0.088; Caa/CCC 0.0777645323482633; D2/D 0.14335607034015696. (Note C2/C, Caa/CCC spreads here differ from table 1 — they appear swapped/misassigned in this list.)

---

## Sheet: Trailing 12-month numbers (standalone helper)

**Purpose:** build trailing-12-month inputs from the last 10-K plus interim statements. TTM flow = Last 10K − first-X-months of last year + first-X-months of current year: `E = B - C + D` for Revenues (5089−2242+3271=6118), R&D (1399−858+637=1178), EBIT (538−(−362)+935=1835), Interest expense (51−24+29=56). Balance-sheet items are point-in-time (B = last 10K, D = most recent): BV equity 11755/12349, BV debt 2356/2167, cash & cross holdings 9626/10252, non-operating assets 0/0, minorities 0/0. Effective tax rates computed per period (`=tax/pre-tax income`): 0.41003, 0.22307, 0.38899. Lease commitments yrs 1–5 + beyond from last 10-K: 142, 128, 117, 110, 102, 252. Purely a staging sheet — nothing references it; user copies results into Master Inputs.

---

## Sheet: Answers (dropdown source lists, no logic)

Yes/No; Current Price / Estimated Value; ERP choices: Will input / Country of incorporation / Operating countries / Operating regions; Cost of debt: Direct input / Synthetic rating / Actual rating; Synthetic rating firm type: 1, 2 (3 implied for financial service); Book or Market Value: B / V; Beta choices: Direct input / Single Business (US) / Single Business (Global) / Multibusiness (US) / Multibusiness (Global); Ratings list Aaa/AAA … D2/D.

---

## Worked example (values currently in workbook — "Caramba", valuation date 2017-04-01)

1. Leases converted (B7=Yes): discount rate 0.0473670 (synthetic, circular) → lease debt 1443.945; lease depreciation 240.658; EBIT adjustment +263.342.
2. Adjusted base year: EBIT = 1337.925 + 263.342 = 1601.267; interest = 255.258 + 1443.945×0.0473670 = 323.653; capex = 603.392 + 504 = 1107.392; depreciation = 356.2 + 240.658 = 596.858; ΔWC: input −62 < 0 → (7010.31−6345.7)×0.0689984 = 45.857.
3. Synthetic rating: coverage = 1601.267/323.653 = 4.9475; with firm type C4=1 → A2/A, spread 0.0113796; + Chile country spread 0.0059874 + rf 0.03 → cost of debt 0.0473670 (consistent fixed point).
4. Fundamentals: ROC = 1601.267×(1−0.34)/(3651.145+1306.1−1286.9−566.6) = 0.340504; RR = (1107.392−596.858+45.857)/1094.396 = 0.508400; g_high = 0.340504×0.508400 = 0.173112.
5. Cost of capital: Ke = 0.03+1.14×0.0785 = 0.11949; Kd_AT = 0.0473670×0.66 = 0.0312622; debt ratio = 1 − 16935/(16935+2609+1443.945) = 0.193108 → WACC = 0.1024525. Stable: Ke = 0.03+1×0.075 = 0.105; Kd_AT = 0.09×0.66 = 0.0594; 70/30 → WACC 0.09132.
6. 3-stage fade (B75=Yes, N=10): years 1–5 g=0.173112, RR=0.508400, WACC=0.1024525; years 6–10 linear fade to g=0.03, RR=0.12, WACC=0.09132. Tax rate ramps 0.316544→0.34 linearly over all 10 years.
7. FCFF path (yrs 1–10): 628.97, 735.32, 859.63, 1004.94, 1174.81, 1551.58, 1960.71, 2379.34, 2778.99, 3128.37; PVs sum to F61 = 8579.82.
8. Terminal: S43 = (3554.968/0.66)×0.66×1.03 = 3661.617; stable RR (fundamentals) = 0.03/0.25 = 0.12 → reinvestment 439.394 (S44=367.764 + S45=71.630); FCFF_T = 3222.223; TV = 3222.223/(0.09132−0.03) = 52547.67; PV = 52547.67/2.572725 = 20424.90.
9. Equity: 8579.82+20424.90 = 29004.72 +1570 cash/non-op −4052.95 debt(incl leases) −17.7 minorities −0 options = 26504.08 → /441.7058 shares = **60.00/share** vs price 38.34 → 36.1% undervalued.

---

## Reimplementation notes (Python port)

**Inputs** (name : type : units): company profile (name str, country str); flags (capitalize_rd, convert_leases, normalize_earnings, is_traded, use_book_debt_ratio, estimate_synthetic_rating, has_options, use_fundamental_growth, override_roc_rr, fade_second_half, stable_fundamental_reinvestment : bool); current & prior financials (ebit, interest_expense, capex, depreciation, revenues & prior, non_cash_wc, chg_wc, bv_debt & prior, bv_equity & prior, cash & prior, non_operating_assets & prior, minority_interests : float, currency units); tax rates (effective, marginal, stable : fraction); market (price, shares, mv_debt, riskfree, erp : float); rating (firm_type int∈{1,2}, or direct cost_of_debt); options (count, strike, maturity_yrs, sigma, dividend_yield, value_at: "price"|"estimated"); high growth (n_years int 0–15, beta, debt_ratio or computed, wc_to_rev or computed, growth or ROC×RR, roc, rr); stable (growth, beta, erp, debt_ratio, pretax_kd, tax, roc or capex_to_depr); optional sub-model inputs (rd_life int ≤10, rd_history list; lease_expense, lease_commitments[5], lease_beyond; normalizer approach∈{1,2,3} + its parameter).

**Outputs:** value of operating assets, firm value, equity value, value per share, % under/over valued, plus intermediate vectors (g_t, RR_t, tax_t, EBIT_t, FCFF_t, WACC_t, PV_t), terminal value, lease debt, research asset, synthetic rating/spread/cost of debt, option value.

**Branches:** every Yes/No flag above; lease yr-6 annuity (D20>0 vs =0); ΔWC<0 replacement rule; N=0 (pure stable: value = TV directly, no discounting of TV); fade only when fade_second_half and t ≥ N/2 (strictly: t < N/2 keeps high-growth value); rating tables by firm type (type 3 table missing — see note); coverage edge cases (interest=0 → 1e6, EBIT<0 → −1e5); options valued at market price vs estimated per-share value (iterate); E24 stable RR non-fundamental branch uses terminal-year identities ((S43−S46)/S43) — circular, solve simultaneously.

**Edge cases:** negative EBIT must be normalized (model not designed for it); iteration required for lease/rating/option/debt-ratio circularities — seed cost of debt with rf + small spread and iterate to convergence (Excel does ~100 iterations); years beyond N must be excluded (Excel blanks them with " "); terminal S43 uses MAX of the after-tax EBIT path (guards against fade producing a lower final year); terminal ΔWC uses the *unfaded* initial growth D34 compounded N years — replicate exactly, do not "fix" silently; VLOOKUP range-match semantics = bisect on lower bounds (last row whose threshold ≤ coverage); country lookup range A5:F179 misses the last two country rows (180–181, incl. the user-input rows) — replicate or extend consciously; ROC denominator uses PRIOR-year invested capital net of prior cash and non-operating assets and can be ≤ 0 (guard); Master-Inputs B44 vs Ratings-estimator C4 firm-type duplication (use one input); string comparisons in Excel IFs are case-insensitive ("Yes"/"yes").

---

## Reference data (VERBATIM tables)

### Country ERP sheet

Header: A1 'Mature Market ERP +' — **B1 = 0.0424** (mature-market ERP; note C1 says "Updated January 1, 2022" even though the folder is labeled 2020). Every country ERP is `=B1 + Country Risk Premium`; changing B1 shifts all ERPs. Lookup columns: 3 = Adj. Default Spread (used by Ratings estimator D12), 4 = Equity Risk Premium (used by cost-of-capital ERP calculators).

Country table (A4:F181, values to 6 significant digits):

| Country | Moody's rating | Adj. Default Spread | Equity Risk Premium | Country Risk Premium | Corporate Tax Rate |
|---|---|---|---|---|---|
| Abu Dhabi | Aa2 | 0.00422187 | 0.0473069 | 0.0049069 | 0.55 |
| Albania | B1 | 0.0383039 | 0.086919 | 0.044519 | 0.15 |
| Algeria | 62.25 | 0.0553449 | 0.106725 | 0.064325 | 0.26 |
| Andorra (Principality of) | Baa2 | 0.0161966 | 0.0612247 | 0.0188247 | 0.1898 |
| Angola | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.25 |
| Argentina | Ca | 0.102093 | 0.161058 | 0.118658 | 0.25 |
| Armenia | Ba3 | 0.0306278 | 0.0779973 | 0.0355973 | 0.18 |
| Aruba | Baa2 | 0.0161966 | 0.0612247 | 0.0188247 | 0.25 |
| Australia | Aaa | 0 | 0.0424 | 0 | 0.3 |
| Austria | Aa1 | 0.0033775 | 0.0463255 | 0.00392552 | 0.25 |
| Azerbaijan | Ba2 | 0.0255615 | 0.0721091 | 0.0297091 | 0.2 |
| Bahamas | Ba3 | 0.0306278 | 0.0779973 | 0.0355973 | 0 |
| Bahrain | B2 | 0.0468244 | 0.096822 | 0.054422 | 0 |
| Bangladesh | Ba3 | 0.0306278 | 0.0779973 | 0.0355973 | 0.325 |
| Barbados | Caa1 | 0.0637887 | 0.116539 | 0.0741388 | 0.055 |
| Belarus | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.18 |
| Belgium | Aa3 | 0.00514301 | 0.0483775 | 0.0059775 | 0.25 |
| Belize | Caa3 | 0.0850516 | 0.141252 | 0.0988518 | 0.2718 |
| Benin | B1 | 0.0383039 | 0.086919 | 0.044519 | 0.3 |
| Bermuda | A2 | 0.00721557 | 0.0507863 | 0.00838634 | 0 |
| Bolivia | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.25 |
| Bosnia and Herzegovina | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.1 |
| Botswana | A3 | 0.0102093 | 0.0542658 | 0.0118658 | 0.22 |
| Brazil | Ba2 | 0.0255615 | 0.0721091 | 0.0297091 | 0.34 |
| Brunei | 79 | 0.00721557 | 0.0507863 | 0.00838634 | 0.185 |
| Bulgaria | Baa1 | 0.0135868 | 0.0581913 | 0.0157913 | 0.1 |
| Burkina Faso | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.28 |
| Cambodia | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.2 |
| Cameroon | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.33 |
| Canada | Aaa | 0 | 0.0424 | 0 | 0.265 |
| Cape Verde | B3 | 0.0553449 | 0.106725 | 0.064325 | 0 |
| Cayman Islands | Aa3 | 0.00514301 | 0.0483775 | 0.0059775 | 0 |
| Chile | A1 | 0.00598739 | 0.0493589 | 0.00695888 | 0.27 |
| China | A1 | 0.00598739 | 0.0493589 | 0.00695888 | 0.25 |
| Colombia | Baa2 | 0.0161966 | 0.0612247 | 0.0188247 | 0.31 |
| Congo (Democratic Republic of) | Caa1 | 0.0637887 | 0.116539 | 0.0741388 | 0.3 |
| Congo (Republic of) | Caa2 | 0.0766078 | 0.131438 | 0.089038 | 0.28 |
| Cook Islands | B1 | 0.0383039 | 0.086919 | 0.044519 | 0.2843 |
| Costa Rica | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.3 |
| Côte d'Ivoire | Ba3 | 0.0306278 | 0.0779973 | 0.0355973 | 0.25 |
| Croatia | Ba1 | 0.0212629 | 0.0671129 | 0.0247129 | 0.18 |
| Cuba | Ca | 0.102093 | 0.161058 | 0.118658 | 0.2718 |
| Curacao | Baa2 | 0.0161966 | 0.0612247 | 0.0188247 | 0.22 |
| Cyprus | Ba1 | 0.0212629 | 0.0671129 | 0.0247129 | 0.125 |
| Czech Republic | Aa3 | 0.00514301 | 0.0483775 | 0.0059775 | 0.19 |
| Denmark | Aaa | 0 | 0.0424 | 0 | 0.22 |
| Dominican Republic | Ba3 | 0.0306278 | 0.0779973 | 0.0355973 | 0.27 |
| Ecuador | Caa3 | 0.0850516 | 0.141252 | 0.0988518 | 0.25 |
| Egypt | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.225 |
| El Salvador | Caa1 | 0.0637887 | 0.116539 | 0.0741388 | 0.3 |
| Estonia | A1 | 0.00598739 | 0.0493589 | 0.00695888 | 0.2 |
| Ethiopia | Caa2 | 0.0766078 | 0.131438 | 0.089038 | 0.3 |
| Fiji | B1 | 0.0383039 | 0.086919 | 0.044519 | 0.2 |
| Finland | Aa1 | 0.0033775 | 0.0463255 | 0.00392552 | 0.2 |
| France | Aa2 | 0.00422187 | 0.0473069 | 0.0049069 | 0.265 |
| Gabon | Caa1 | 0.0637887 | 0.116539 | 0.0741388 | 0.3 |
| Gambia | 65.75 | 0.0468244 | 0.096822 | 0.054422 | 0.31 |
| Georgia | Ba2 | 0.0255615 | 0.0721091 | 0.0297091 | 0.15 |
| Germany | Aaa | 0 | 0.0424 | 0 | 0.3 |
| Ghana | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.25 |
| Greece | Ba3 | 0.0306278 | 0.0779973 | 0.0355973 | 0.24 |
| Guatemala | Ba1 | 0.0212629 | 0.0671129 | 0.0247129 | 0.25 |
| Guernsey (States of) | Aa3 | 0.00514301 | 0.0483775 | 0.0059775 | 0 |
| Guinea | 57.5 | 0.0766078 | 0.131438 | 0.089038 | 0.2915 |
| Guinea-Bissau | 62.75 | 0.0553449 | 0.106725 | 0.064325 | 0.2915 |
| Guyana | 66.25 | 0.0383039 | 0.086919 | 0.044519 | 0.1864 |
| Haiti | 56.25 | 0.0850516 | 0.141252 | 0.0988518 | 0.1864 |
| Honduras | B1 | 0.0383039 | 0.086919 | 0.044519 | 0.25 |
| Hong Kong | Aa3 | 0.00514301 | 0.0483775 | 0.0059775 | 0.165 |
| Hungary | Baa2 | 0.0161966 | 0.0612247 | 0.0188247 | 0.09 |
| Iceland | A2 | 0.00721557 | 0.0507863 | 0.00838634 | 0.2 |
| India | Baa3 | 0.0187298 | 0.0641688 | 0.0217688 | 0.3 |
| Indonesia | Baa2 | 0.0161966 | 0.0612247 | 0.0188247 | 0.35 |
| Iran | 63.75 | 0.0553449 | 0.106725 | 0.064325 | 0.2023 |
| Iraq | Caa1 | 0.0637887 | 0.116539 | 0.0741388 | 0.35 |
| Ireland | A2 | 0.00721557 | 0.0507863 | 0.00838634 | 0.125 |
| Isle of Man | Aa3 | 0.00514301 | 0.0483775 | 0.0059775 | 0 |
| Israel | A1 | 0.00598739 | 0.0493589 | 0.00695888 | 0.23 |
| Italy | Baa3 | 0.0187298 | 0.0641688 | 0.0217688 | 0.24 |
| Jamaica | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.25 |
| Japan | A1 | 0.00598739 | 0.0493589 | 0.00695888 | 0.3062 |
| Jersey (States of) | Aaa | 0 | 0.0424 | 0 | 0 |
| Jordan | B1 | 0.0383039 | 0.086919 | 0.044519 | 0.2 |
| Kazakhstan | Baa2 | 0.0161966 | 0.0612247 | 0.0188247 | 0.2 |
| Kenya | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.3 |
| Korea | Aa2 | 0.00422187 | 0.0473069 | 0.0049069 | 0.25 |
| Korea, D.P.R. | 51.5 | 0.102093 | 0.161058 | 0.118658 | 0.231 |
| Kuwait | A1 | 0.00598739 | 0.0493589 | 0.00695888 | 0.15 |
| Kyrgyzstan | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.1 |
| Laos | Caa2 | 0.0766078 | 0.131438 | 0.089038 | 0.2281 |
| Latvia | A3 | 0.0102093 | 0.0542658 | 0.0118658 | 0.2 |
| Lebanon | C | 0.175 | 0.245795 | 0.203395 | 0.17 |
| Liberia | 59 | 0.0766078 | 0.131438 | 0.089038 | 0.2915 |
| Libya | 66.25 | 0.0383039 | 0.086919 | 0.044519 | 0.2 |
| Liechtenstein | Aaa | 0 | 0.0424 | 0 | 0.125 |
| Lithuania | A2 | 0.00721557 | 0.0507863 | 0.00838634 | 0.15 |
| Luxembourg | Aaa | 0 | 0.0424 | 0 | 0.2494 |
| Macao | Aa3 | 0.00514301 | 0.0483775 | 0.0059775 | 0.2281 |
| Macedonia | Ba3 | 0.0306278 | 0.0779973 | 0.0355973 | 0.1 |
| Madagascar | 63.5 | 0.0553449 | 0.106725 | 0.064325 | 0.2 |
| Malawi | 59.75 | 0.0766078 | 0.131438 | 0.089038 | 0.3 |
| Malaysia | A3 | 0.0102093 | 0.0542658 | 0.0118658 | 0.24 |
| Maldives | Caa1 | 0.0637887 | 0.116539 | 0.0741388 | 0.2281 |
| Mali | Caa1 | 0.0637887 | 0.116539 | 0.0741388 | 0.2281 |
| Malta | A2 | 0.00721557 | 0.0507863 | 0.00838634 | 0.35 |
| Mauritius | Baa2 | 0.0161966 | 0.0612247 | 0.0188247 | 0.15 |
| Mexico | Baa1 | 0.0135868 | 0.0581913 | 0.0157913 | 0.3 |
| Moldova | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.12 |
| Mongolia | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.25 |
| Montenegro | B1 | 0.0383039 | 0.086919 | 0.044519 | 0.09 |
| Montserrat | Baa3 | 0.0187298 | 0.0641688 | 0.0217688 | 0.2718 |
| Morocco | Ba1 | 0.0212629 | 0.0671129 | 0.0247129 | 0.31 |
| Mozambique | Caa2 | 0.0766078 | 0.131438 | 0.089038 | 0.32 |
| Myanmar | 53 | 0.102093 | 0.161058 | 0.118658 | 0.25 |
| Namibia | Ba3 | 0.0306278 | 0.0779973 | 0.0355973 | 0.32 |
| Netherlands | Aaa | 0 | 0.0424 | 0 | 0.25 |
| New Zealand | Aaa | 0 | 0.0424 | 0 | 0.28 |
| Nicaragua | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.3 |
| Niger | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.2281 |
| Nigeria | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.3 |
| Norway | Aaa | 0 | 0.0424 | 0 | 0.22 |
| Oman | Ba3 | 0.0306278 | 0.0779973 | 0.0355973 | 0.15 |
| Pakistan | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.29 |
| Panama | Baa2 | 0.0161966 | 0.0612247 | 0.0188247 | 0.25 |
| Papua New Guinea | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.3 |
| Paraguay | Ba1 | 0.0212629 | 0.0671129 | 0.0247129 | 0.1 |
| Peru | Baa1 | 0.0135868 | 0.0581913 | 0.0157913 | 0.295 |
| Philippines | Baa2 | 0.0161966 | 0.0612247 | 0.0188247 | 0.3 |
| Poland | A2 | 0.00721557 | 0.0507863 | 0.00838634 | 0.19 |
| Portugal | Baa2 | 0.0161966 | 0.0612247 | 0.0188247 | 0.21 |
| Qatar | Aa3 | 0.00514301 | 0.0483775 | 0.0059775 | 0.1 |
| Ras Al Khaimah (Emirate of) | A3 | 0.0102093 | 0.0542658 | 0.0118658 | 0 |
| Romania | Baa3 | 0.0187298 | 0.0641688 | 0.0217688 | 0.16 |
| Russia | Baa3 | 0.0187298 | 0.0641688 | 0.0217688 | 0.2 |
| Rwanda | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.3 |
| Saudi Arabia | A1 | 0.00598739 | 0.0493589 | 0.00695888 | 0.2 |
| Senegal | Ba3 | 0.0306278 | 0.0779973 | 0.0355973 | 0.3 |
| Serbia | Ba2 | 0.0255615 | 0.0721091 | 0.0297091 | 0.15 |
| Sharjah | Baa3 | 0.0187298 | 0.0641688 | 0.0217688 | 0 |
| Sierra Leone | 57 | 0.0850516 | 0.141252 | 0.0988518 | 0.3 |
| Singapore | Aaa | 0 | 0.0424 | 0 | 0.17 |
| Slovakia | A2 | 0.00721557 | 0.0507863 | 0.00838634 | 0.21 |
| Slovenia | A3 | 0.0102093 | 0.0542658 | 0.0118658 | 0.19 |
| Solomon Islands | Caa1 | 0.0637887 | 0.116539 | 0.0741388 | 0.3 |
| Somalia | 51.5 | 0.102093 | 0.161058 | 0.118658 | 0.2915 |
| South Africa | Ba2 | 0.0255615 | 0.0721091 | 0.0297091 | 0.28 |
| Spain | Baa1 | 0.0135868 | 0.0581913 | 0.0157913 | 0.25 |
| Sri Lanka | Caa2 | 0.0766078 | 0.131438 | 0.089038 | 0.24 |
| St. Maarten | Ba2 | 0.0255615 | 0.0721091 | 0.0297091 | 0.2718 |
| St. Vincent & the Grenadines | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.2718 |
| Sudan | 36.25 | 0.175 | 0.245795 | 0.203395 | 0.35 |
| Suriname | Caa3 | 0.0850516 | 0.141252 | 0.0988518 | 0.36 |
| Swaziland | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.275 |
| Sweden | Aaa | 0 | 0.0424 | 0 | 0.206 |
| Switzerland | Aaa | 0 | 0.0424 | 0 | 0.1493 |
| Syria | 45.5 | 0.175 | 0.245795 | 0.203395 | 0.28 |
| Taiwan | Aa3 | 0.00514301 | 0.0483775 | 0.0059775 | 0.2 |
| Tajikistan | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.2281 |
| Tanzania | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.3 |
| Thailand | Baa1 | 0.0135868 | 0.0581913 | 0.0157913 | 0.2 |
| Togo | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.2281 |
| Trinidad and Tobago | Ba2 | 0.0255615 | 0.0721091 | 0.0297091 | 0.3 |
| Tunisia | Caa1 | 0.0637887 | 0.116539 | 0.0741388 | 0.15 |
| Turkey | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.2 |
| Turks and Caicos Islands | Baa1 | 0.0135868 | 0.0581913 | 0.0157913 | 0 |
| Uganda | B2 | 0.0468244 | 0.096822 | 0.054422 | 0.3 |
| Ukraine | B3 | 0.0553449 | 0.106725 | 0.064325 | 0.18 |
| United Arab Emirates | Aa2 | 0.00422187 | 0.0473069 | 0.0049069 | 0.55 |
| United Kingdom | Aa3 | 0.00514301 | 0.0483775 | 0.0059775 | 0.19 |
| United States | Aaa | 0 | 0.0424 | 0 | 0.27 |
| Uruguay | Baa2 | 0.0161966 | 0.0612247 | 0.0188247 | 0.25 |
| Uzbekistan | B1 | 0.0383039 | 0.086919 | 0.044519 | 0.075 |
| Venezuela | C | 0.175 | 0.245795 | 0.203395 | 0.34 |
| Vietnam | Ba3 | 0.0306278 | 0.0779973 | 0.0355973 | 0.2 |
| Yemen, Republic | 52.75 | 0.102093 | 0.161058 | 0.118658 | 0.2 |
| Zambia | Ca | 0.102093 | 0.161058 | 0.118658 | 0.35 |
| Zimbabwe | 61 | 0.0637887 | 0.116539 | 0.0741388 | 0.25 |

Regional aggregates (A184:E194) — used by the Operating Regions ERP calculator ('Country ERP' rows 185–193; B = B1 + E):

| Region | Weighted Average: ERP | Default Spread | Tax rate | CRP |
|---|---|---|---|---|
| Africa | 0.094863 | 0.0451389 | 0.274636 | 0.052463 |
| Asia | 0.0528004 | 0.00894847 | 0.265253 | 0.0104004 |
| Australia & New Zealand | 0.0424111 | 9.5278e-06 | 0.297243 | 1.10737e-05 |
| Caribbean | 0.110741 | 0.0588005 | 0.240648 | 0.0683413 |
| Central and South America | 0.0802935 | 0.0326034 | 0.302999 | 0.0378935 |
| Eastern Europe & Russia | 0.0635488 | 0.0181963 | 0.182283 | 0.0211488 |
| Middle East | 0.0584081 | 0.0137733 | 0.296992 | 0.0160081 |
| North America | 0.0424 | 0 | 0.269636 | 0 |
| Western Europe | 0.0507215 | 0.00715979 | 0.239352 | 0.00832151 |
| Global | 0.0525938 | 0.00877072 | 0.260664 | 0.0101938 |


### US Industry averages sheet (A1:AA95)

Reference data snapshot (US firms; formulas link to an external Damodaran data workbook, so only values survive here). VLOOKUP consumers: 'Cost of capital worksheet' multi-business calculator reads column 7 (Unlevered Beta, col G) and column 15 (EV/Sales, col O) from range A2:Z95. The Earnings Normalizer's "sector margin" approach expects a margin from column D (Pre-tax Operating Margin, Unadjusted) or AA (Lease & R&D adjusted). All ratios are decimals (0.10 = 10%). Values to 6 significant digits:

| Industry Name | Number of firms | Annual Average Revenue growth - Last 5 years | Pre-tax Operating Margin (Unadjusted) | After-tax ROC | Average effective tax rate | Unlevered Beta | Equity (Levered) Beta | Cost of equity | Std deviation in stock prices | Pre-tax cost of debt | Market Debt/Capital | Cost of capital | Sales/Capital | EV/Sales | EV/EBITDA | EV/EBIT | Price/Book | Trailing PE | Non-cash WC as % of Revenues | Cap Ex as % of Revenues | Net Cap Ex as % of Revenues | Reinvestment Rate | ROE | Dividend Payout Ratio | Equity Reinvestment Rate | Pre-tax Operating Margin (Lease & R&D adjusted) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Advertising | 49 | 0.0713158 | 0.106153 | 0.501981 | 0.237987 | 1.10182 | 1.34042 | 0.0719339 | 0.566968 | 0.03578 | 0.339791 | 0.0563665 | 4.80594 | 2.03466 | 9.93564 | 17.51 | 4.09953 | 88.1025 | -0.00440807 | 0.016526 | 0.0211722 | -0.0132714 | 0.20183 | 1.14215 | 1.14215 | 0.110732 |
| Aerospace/Defense | 73 | 0.0493976 | 0.0781333 | 0.147624 | 0.167463 | 1.11041 | 1.28105 | 0.0694165 | 0.382322 | 0.0316 | 0.227509 | 0.0588717 | 1.98483 | 2.32655 | 13.3763 | 22.2659 | 4.60349 | 37.0124 | 0.466134 | 0.0258727 | 0.00577646 | 0.462125 | 0.0908757 | 0.80351 | 0.80351 | 0.0797471 |
| Air Transport | 21 | -0.0699583 | -0.231356 | -0.198093 | 0.212234 | 0.914138 | 1.58291 | 0.0822153 | 0.401931 | 0.03578 | 0.60526 | 0.0482627 | 0.883836 | 2.13567 | 17.6049 | NA | 3.71457 | 3708.23 | 0.00946887 | 0.0714212 | -0.0223864 | NA | -0.27283 | 0 | 0 | -0.236794 |
| Apparel | 39 | 0.061162 | 0.119572 | 0.203536 | 0.199275 | 1.09835 | 1.22658 | 0.0671071 | 0.43487 | 0.03578 | 0.2401 | 0.057266 | 1.82315 | 1.81604 | 9.49015 | 14.1654 | 3.82805 | 36.1158 | 0.202867 | 0.0180496 | 0.0308393 | 0.285081 | 0.207837 | 0.29271 | 0.29271 | 0.126953 |
| Auto & Truck | 26 | 0.119371 | 0.0525843 | 0.047412 | 0.170538 | 1.02077 | 1.12931 | 0.0629826 | 0.547769 | 0.03578 | 0.165705 | 0.0568742 | 0.833981 | 4.88459 | 39.0738 | 83.0923 | 9.88093 | 55.5045 | -0.0470946 | 0.13119 | 0.096462 | 2.37774 | 0.136825 | 0.0278743 | 0.0278743 | 0.0589104 |
| Auto Parts | 38 | 0.0610781 | 0.0640241 | 0.147711 | 0.242473 | 1.21259 | 1.39807 | 0.0743781 | 0.371404 | 0.0316 | 0.240564 | 0.0620348 | 2.43982 | 1.06211 | 7.86236 | 13.85 | 2.94667 | 30.4275 | 0.136665 | 0.0319726 | 0.039769 | 1.28637 | 0.06717 | 0.488633 | 0.488633 | 0.0694334 |
| Bank (Money Center) | 7 | 0.0461333 | 0 | -8.974e-05 | 0.154019 | 1.03251 | 1.11721 | 0.0624699 | 0.22231 | 0.025 | 0.630169 | 0.0346039 | 0.271597 | 4.00474 | NA | NA | 1.21493 | 8.99735 | NA | 0.00990767 | 0.00990767 | NA | 0.14969 | 0.196974 | 0.196974 | -0.00038731 |
| Banks (Regional) | 563 | 0.11739 | 3.19304e-08 | -0.000818885 | 0.210428 | 0.841274 | 0.697988 | 0.0446947 | 0.196785 | 0.025 | 0.256917 | 0.0379006 | 0.377693 | 3.56634 | NA | NA | 1.39079 | 28.8428 | NA | 0.0249762 | 0.0559081 | NA | 0.125342 | 0.260753 | 0.260753 | -0.00268645 |
| Beverage (Alcoholic) | 21 | 0.145687 | 0.230295 | 0.152849 | 0.270201 | 0.720525 | 0.819365 | 0.0498411 | 0.37866 | 0.0316 | 0.176386 | 0.0451187 | 0.721389 | 4.77509 | 16.7239 | 20.7018 | 3.315 | 54.5376 | 0.148776 | 0.0680546 | 0.0286772 | 0.152264 | 0.0438549 | 0.844471 | 0.844471 | 0.230143 |
| Beverage (Soft) | 32 | 0.204723 | 0.206662 | 0.27304 | 0.233304 | 1.11555 | 1.21569 | 0.0666451 | 0.482654 | 0.03578 | 0.142713 | 0.0608615 | 1.37901 | 4.96509 | 20.0013 | 23.9248 | 8.4222 | 111.14 | -0.0781654 | 0.0453 | 0.0168203 | 0.111005 | 0.327977 | 0.763155 | 0.763155 | 0.207387 |
| Broadcasting | 28 | 0.0964426 | 0.183197 | 0.172219 | 0.197754 | 0.811272 | 1.3521 | 0.0724288 | 0.487694 | 0.03578 | 0.538793 | 0.0474776 | 1.07371 | 1.8478 | 7.32978 | 10.1709 | 1.33035 | 8.8337 | 0.112768 | 0.0240944 | 0.0277785 | 1.1831 | 0.193468 | 0.157995 | 0.157995 | 0.181327 |
| Brokerage & Investment Banking | 31 | 0.179595 | 0.013087 | 0.00366082 | 0.21287 | 0.67007 | 1.17498 | 0.0649192 | 0.317394 | 0.0316 | 0.645997 | 0.0378835 | 0.300266 | 5.20349 | NA | NA | 1.73852 | 12.6242 | NA | 0.0381123 | -0.0280339 | -14.8022 | 0.216106 | 0.175612 | 0.175612 | 0.0136779 |
| Building Materials | 44 | 0.0845433 | 0.116332 | 0.304407 | 0.24906 | 1.08715 | 1.18713 | 0.0654345 | 0.34535 | 0.0316 | 0.157872 | 0.058746 | 3.10166 | 2.13509 | 13.673 | 18.1052 | 5.12221 | 28.097 | 0.175122 | 0.0241032 | 0.0451071 | 0.803697 | 0.312618 | 0.151006 | 0.151006 | 0.118169 |
| Business & Consumer Services | 160 | 0.0538894 | 0.0911729 | 0.232641 | 0.248371 | 0.986113 | 1.08919 | 0.0612818 | 0.411734 | 0.03578 | 0.182945 | 0.054849 | 2.74492 | 2.65377 | 16.0125 | 26.6483 | 4.86481 | 269.884 | 0.127107 | 0.0240604 | 0.0306632 | 0.670325 | 0.136736 | 0.302982 | 0.302982 | 0.0940843 |
| Cable TV | 11 | 0.174187 | 0.192258 | 0.127719 | 0.24675 | 0.664139 | 0.934129 | 0.0547071 | 0.200732 | 0.025 | 0.37545 | 0.0410193 | 0.811782 | 3.33102 | 10.1789 | 17.3436 | 2.90849 | 27.3256 | -0.00763094 | 0.0993971 | -0.0175111 | -0.0982403 | 0.163839 | 0.197549 | 0.197549 | 0.192059 |
| Chemical (Basic) | 35 | 0.20387 | 0.14932 | 0.273095 | 0.207919 | 0.937128 | 1.16242 | 0.0643868 | 0.450189 | 0.03578 | 0.309187 | 0.052555 | 2.00226 | 1.20378 | 5.61897 | 7.87503 | 2.50942 | 14.701 | 0.152298 | 0.0508306 | 0.0346304 | 0.594048 | 0.472421 | 0.275352 | 0.275352 | 0.151432 |
| Chemical (Diversified) | 4 | 0.0805625 | 0.0971804 | 0.13744 | 0.108834 | 1.20791 | 1.50282 | 0.0788196 | 0.372916 | 0.0316 | 0.321565 | 0.0608918 | 1.45204 | 1.33476 | 8.66491 | 13.7871 | 2.61919 | 11.7475 | 0.187032 | 0.0424363 | 0.0147907 | 0.323287 | 0.281157 | 0.273349 | 0.273349 | 0.0984182 |
| Chemical (Specialty) | 81 | 0.0793447 | 0.133279 | 0.150213 | 0.15982 | 0.997723 | 1.10275 | 0.0618565 | 0.407237 | 0.03578 | 0.162956 | 0.0560329 | 1.22148 | 3.32652 | 15.4079 | 24.497 | 3.48771 | 34.0009 | 0.205575 | 0.0669628 | 0.0419834 | 0.449435 | 0.159966 | 0.297347 | 0.297347 | 0.136658 |
| Coal & Related Energy | 18 | -0.218443 | -0.0320878 | -0.0404494 | 0.0331522 | 0.819711 | 0.915629 | 0.0539227 | 0.585697 | 0.03578 | 0.294027 | 0.0457477 | 1.51864 | 1.36017 | 8.17764 | NA | 2.60635 | 19.4346 | 0.058455 | 0.106885 | -0.0113849 | NA | -0.143982 | 0.000589904 | 0.000589904 | -0.0268417 |
| Computer Services | 83 | 0.0887145 | 0.0648065 | 0.214069 | 0.220913 | 1.05762 | 1.19882 | 0.0659301 | 0.484425 | 0.03578 | 0.21223 | 0.057481 | 3.36655 | 1.53197 | 11.9678 | 21.9757 | 4.83554 | 38.496 | 0.160662 | 0.0171841 | -0.0096061 | -0.279789 | 0.14611 | 0.756919 | 0.756919 | 0.0691868 |
| Computers/Peripherals | 46 | 0.166779 | 0.207819 | 0.449288 | 0.132455 | 1.24877 | 1.28675 | 0.0696581 | 0.512738 | 0.03578 | 0.0704293 | 0.0665917 | 2.22005 | 5.32534 | 21.295 | 25.4515 | 26.2958 | 14.9712 | -0.0755426 | 0.0299132 | 0.00818548 | 0.0561465 | 0.00607877 | 0.148789 | 0.148789 | 0.21265 |
| Construction Supplies | 48 | 0.0627641 | 0.110292 | 0.128839 | 0.20975 | 0.979649 | 1.10858 | 0.0621036 | 0.400064 | 0.03578 | 0.218394 | 0.0542448 | 1.30487 | 2.38725 | 14.2636 | 21.0597 | 3.76774 | 724.655 | 0.193564 | 0.0483651 | 0.0348813 | 0.53346 | 0.171673 | 0.366174 | 0.366174 | 0.113089 |
| Diversified | 22 | 0.00279 | 0.301189 | 0.214453 | 0.193594 | 0.702141 | 0.754388 | 0.0470861 | 0.30111 | 0.0316 | 0.184479 | 0.0426552 | 0.770128 | 2.81328 | 7.89389 | 9.27778 | 1.88304 | 103.877 | 0.052771 | 0.0418393 | 0.0050326 | 0.0420278 | 0.199159 | 0.0696422 | 0.0696422 | 0.300342 |
| Drugs (Biotechnology) | 581 | 0.308573 | 0.123654 | 0.0729687 | 0.113842 | 0.972233 | 0.992949 | 0.057201 | 0.507986 | 0.03578 | 0.132693 | 0.0530767 | 0.465873 | 7.06236 | 11.2932 | 40.4182 | 5.99046 | 321.365 | 0.127885 | 0.0361572 | 0.116578 | 1.79862 | -0.00764356 | 0.00059719 | 0.00059719 | 0.157275 |
| Drugs (Pharmaceutical) | 298 | 0.428481 | 0.247103 | 0.196643 | 0.115274 | 1.00982 | 1.0763 | 0.0607349 | 0.561665 | 0.03578 | 0.128089 | 0.0563011 | 0.687018 | 5.24833 | 13.6726 | 20.6761 | 5.42809 | 45.6903 | 0.184463 | 0.0489243 | 0.0743814 | 0.349967 | 0.145543 | 0.893589 | 0.893589 | 0.291608 |
| Education | 35 | 0.00810421 | 0.05924 | 0.0710394 | 0.232379 | 1.10332 | 1.12608 | 0.0628458 | 0.415016 | 0.03578 | 0.204478 | 0.055336 | 1.16616 | 2.72434 | 12.3393 | 38.9263 | 2.35307 | 1160.4 | 0.0420637 | 0.0492751 | 0.201039 | 6.01956 | 0.086105 | 0.0710865 | 0.0710865 | 0.0650491 |
| Electrical Equipment | 104 | 0.0583578 | 0.113987 | 0.227794 | 0.190355 | 1.19433 | 1.24541 | 0.0679052 | 0.576591 | 0.03578 | 0.120426 | 0.0628731 | 1.99421 | 3.98323 | 17.1938 | 28.2444 | 5.17004 | 52.4135 | 0.224975 | 0.0479066 | 0.11528 | 1.57999 | 0.167965 | 0.461469 | 0.461469 | 0.12001 |
| Electronics (Consumer & Office) | 16 | 0.014991 | 0.0480056 | 0.183222 | 0.117817 | 1.05716 | 0.975972 | 0.0564812 | 0.525378 | 0.03578 | 0.0707696 | 0.0543325 | 3.42602 | 1.54901 | 18.9492 | 29.6139 | 3.96701 | 107.942 | 0.0937681 | 0.0119153 | 0.00278647 | 0.228274 | 0.435742 | 0 | 0 | 0.0559035 |
| Electronics (General) | 137 | 0.0841353 | 0.103706 | 0.175928 | 0.178773 | 1.05102 | 1.08528 | 0.0611159 | 0.434455 | 0.03578 | 0.113086 | 0.0571583 | 1.77221 | 2.87714 | 16.6452 | 26.4289 | 4.54427 | 36.6211 | 0.211861 | 0.0388256 | 0.0887101 | 1.15704 | 0.147238 | 0.184644 | 0.184644 | 0.1062 |
| Engineering/Construction | 48 | 0.0882804 | 0.0469614 | 0.159878 | 0.234809 | 0.973963 | 1.05809 | 0.059963 | 0.36356 | 0.0316 | 0.203778 | 0.0524446 | 3.73328 | 1.05886 | 12.6317 | 21.2284 | 2.96229 | 65.9086 | 0.195578 | 0.0219096 | 0.0360363 | 0.975054 | 0.064844 | 0.0881939 | 0.0881939 | 0.0495226 |
| Entertainment | 108 | 0.226133 | 0.0867215 | 0.100604 | 0.12544 | 0.964248 | 1.01228 | 0.0580208 | 0.596294 | 0.03578 | 0.132195 | 0.0538036 | 1.17854 | 6.37336 | 31.5819 | 70.4648 | 5.13389 | 765.058 | -0.00104376 | 0.039603 | 0.0267653 | 0.408855 | 0.04276 | 0.159252 | 0.159252 | 0.0874865 |
| Environmental & Waste Services | 58 | -0.004016 | 0.129384 | 0.255626 | 0.218184 | 1.08618 | 1.24033 | 0.0676902 | 0.430136 | 0.03578 | 0.172631 | 0.0605138 | 2.07207 | 3.62964 | 15.9651 | 27.3798 | 5.77858 | 46.3309 | 0.0974752 | 0.0654619 | 0.111536 | 1.09565 | 0.139475 | 0.464757 | 0.464757 | 0.131107 |
| Farming/Agriculture | 36 | 0.0684131 | 0.0750305 | 0.134756 | 0.192291 | 0.847865 | 1.03032 | 0.0587855 | 0.464456 | 0.03578 | 0.269109 | 0.0499947 | 1.90783 | 1.26468 | 12.8719 | 16.3532 | 3.23429 | 31.2098 | 0.123664 | 0.0261202 | 0.0176933 | 0.928795 | 0.266022 | 0.18315 | 0.18315 | 0.0764593 |
| Financial Svcs. (Non-bank & Insurance) | 223 | 0.112967 | 0.14065 | 0.00585649 | 0.193052 | 0.151759 | 0.927231 | 0.0544146 | 0.285213 | 0.0316 | 0.878989 | 0.0268613 | 0.0487052 | 25.0395 | 104.281 | 114.386 | 2.3869 | 21.8568 | NA | 0.0545904 | 0.083078 | 0.616859 | 0.00275725 | 0.153948 | 0.153948 | 0.142005 |
| Food Processing | 92 | 0.129877 | 0.134707 | 0.195383 | 0.233136 | 0.632414 | 0.750875 | 0.0469371 | 0.276898 | 0.0316 | 0.233823 | 0.041356 | 1.60434 | 2.23489 | 12.6181 | 16.2291 | 2.5895 | 51.3063 | 0.0592259 | 0.0350793 | 0.0505262 | 0.556004 | 0.134439 | 0.461286 | 0.461286 | 0.136111 |
| Food Wholesalers | 15 | 0.17189 | 0.0193386 | 0.122908 | 0.17525 | 1.08348 | 1.40156 | 0.0745261 | 0.540091 | 0.03578 | 0.319377 | 0.0590661 | 7.24121 | 0.521829 | 14.6874 | 28.0807 | 4.63395 | 47.6505 | 0.0656737 | 0.00811741 | 0.0152434 | 1.52842 | 0.111801 | 0.840827 | 0.840827 | 0.0185712 |
| Furn/Home Furnishings | 32 | 0.0619224 | 0.10946 | 0.247558 | 0.200109 | 0.993069 | 1.1088 | 0.0621132 | 0.447704 | 0.03578 | 0.222704 | 0.0540972 | 2.5259 | 1.24915 | 8.07906 | 11.1908 | 2.86227 | 13.4435 | 0.128199 | 0.0281942 | 0.0277614 | 0.696837 | 0.253984 | 0.220753 | 0.220753 | 0.110971 |
| Green & Renewable Energy | 20 | -0.24637 | 0.236571 | 0.0572669 | 0.283449 | 1.09526 | 1.58811 | 0.082436 | 0.817559 | 0.081225 | 0.399856 | 0.0731826 | 0.248263 | 10.3798 | 16.8741 | 40.4482 | 1.90557 | 64.6731 | -1.2669 | 0.372956 | 0.129268 | 1.23018 | -0.241202 | 0.00199531 | 0.00199531 | 0.234031 |
| Healthcare Products | 244 | 0.189475 | 0.176852 | 0.186437 | 0.141552 | 0.91238 | 0.938128 | 0.0548766 | 0.438122 | 0.03578 | 0.0793163 | 0.0525957 | 1.03777 | 7.00397 | 24.1617 | 37.629 | 6.30473 | 91.0344 | 0.233349 | 0.0507394 | 0.0734616 | 0.508377 | 0.14182 | 0.252597 | 0.252597 | 0.187082 |
| Healthcare Support Services | 131 | 0.179645 | 0.0426515 | 0.320468 | 0.224721 | 0.949847 | 1.05784 | 0.0599523 | 0.468572 | 0.03578 | 0.197116 | 0.0532833 | 8.32786 | 0.779551 | 13.1678 | 18.1122 | 3.58967 | 35.9106 | -0.063872 | 0.0074561 | 0.0163893 | 0.52286 | 0.146844 | 0.272322 | 0.272322 | 0.0416959 |
| Heathcare Information and Technology | 142 | 0.158682 | 0.180879 | 0.230645 | 0.171069 | 0.908888 | 0.941682 | 0.0550273 | 0.462843 | 0.03578 | 0.0886409 | 0.0524649 | 1.22329 | 7.7762 | 25.5993 | 39.3919 | 5.78521 | 94.11 | 0.195429 | 0.0454141 | 0.171077 | 1.28271 | 0.197382 | 0.0658172 | 0.0658172 | 0.195016 |
| Homebuilding | 29 | 0.202543 | 0.162826 | 0.229208 | 0.222014 | 1.58556 | 1.68521 | 0.086553 | 0.394749 | 0.0316 | 0.180133 | 0.0751173 | 1.72912 | 1.36637 | 8.04086 | 8.38689 | 2.19742 | 13.4838 | 0.620161 | 0.00544245 | 0.00540936 | 0.46744 | 0.273756 | 0.0582906 | 0.0582906 | 0.162903 |
| Hospitals/Healthcare Facilities | 31 | -0.0164785 | 0.128509 | 0.231684 | 0.209375 | 0.963582 | 1.41352 | 0.0750334 | 0.523135 | 0.03578 | 0.415121 | 0.0547282 | 2.04431 | 1.67936 | 8.7824 | 13.4341 | 5.92054 | 17.7422 | 0.10919 | 0.0491592 | 0.0294388 | 0.469304 | 0.95707 | 0.0875534 | 0.0875534 | 0.124523 |
| Hotel/Gaming | 66 | 0.0217989 | -0.0910908 | -0.0468875 | 0.26135 | 1.43743 | 1.79441 | 0.0911829 | 0.438673 | 0.03578 | 0.315119 | 0.0706801 | 0.394644 | 8.86988 | 27.8179 | NA | 7.56052 | 78.2091 | 0.143732 | 0.0841235 | 0.0183381 | NA | -0.402099 | 0.000412251 | 0.000412251 | -0.127253 |
| Household Products | 118 | 0.117029 | 0.184102 | 0.397789 | 0.194569 | 0.920072 | 0.979634 | 0.0566365 | 0.585677 | 0.03578 | 0.111756 | 0.053226 | 2.27998 | 4.37853 | 18.8834 | 23.5379 | 10.3855 | 49.4274 | 0.0706553 | 0.0368917 | 0.0245921 | 0.165807 | 0.359451 | 0.577927 | 0.577927 | 0.18532 |
| Information Services | 79 | 0.131246 | 0.237803 | 0.2904 | 0.195019 | 1.20387 | 1.25051 | 0.0681216 | 0.464408 | 0.03578 | 0.0939565 | 0.0641752 | 1.3428 | 8.74913 | 25.8128 | 35.1897 | 7.63699 | 106.393 | 0.0678964 | 0.0274767 | 0.0387525 | 0.267372 | 0.175069 | 0.276994 | 0.276994 | 0.243098 |
| Insurance (General) | 23 | 0.0592731 | 0.169613 | 0.129723 | 0.17208 | 0.810909 | 0.922164 | 0.0541997 | 0.371507 | 0.0316 | 0.210369 | 0.0476506 | 0.862954 | 2.37691 | 10.0016 | 13.8689 | 1.94586 | 54.6464 | -0.0696068 | 0.00983029 | -0.012813 | 0.0455865 | 0.135042 | 0.288362 | 0.288362 | 0.169738 |
| Insurance (Life) | 24 | 0.064553 | 0.120605 | 0.0649128 | 0.184637 | 0.882988 | 1.22433 | 0.0670117 | 0.318132 | 0.0316 | 0.480788 | 0.0458841 | 0.62626 | 1.34725 | 9.18442 | 10.5863 | 0.752617 | 99.9357 | 0.0679742 | 0.00161034 | 0.00120862 | 0.00810022 | 0.078577 | 0.263423 | 0.263423 | 0.12092 |
| Insurance (Prop/Cas.) | 52 | 0.041376 | 0.157007 | 0.173798 | 0.200024 | 0.784777 | 0.861418 | 0.0516241 | 0.292443 | 0.0316 | 0.190129 | 0.0461948 | 1.27297 | 1.31 | 7.0269 | 8.24056 | 1.55888 | 21.51 | -0.49026 | 0.00691495 | 0.0100861 | 0.220682 | 0.156389 | 0.270934 | 0.270934 | 0.157609 |
| Investments & Asset Management | 687 | 0.115799 | 0.162307 | 0.0972352 | 0.146777 | 0.965118 | 1.04833 | 0.0595493 | 0.319699 | 0.0316 | 0.218337 | 0.051584 | 0.610226 | 5.41779 | 22.2579 | 26.0179 | 2.78421 | 84.0547 | NA | 0.0186271 | 0.0428162 | 0.307093 | 0.237691 | 0.314405 | 0.314405 | 0.161625 |
| Machinery | 111 | 0.0529566 | 0.146713 | 0.272154 | 0.190876 | 1.17826 | 1.24713 | 0.0679781 | 0.347534 | 0.0316 | 0.123689 | 0.0624232 | 2.037 | 3.24952 | 16.2714 | 21.6537 | 4.67739 | 40.9641 | 0.22638 | 0.0213475 | 0.0268145 | 0.33887 | 0.211343 | 0.277474 | 0.277474 | 0.149312 |
| Metals & Mining | 74 | 0.165733 | 0.264702 | 0.361241 | 0.339843 | 1.128 | 1.17293 | 0.0648322 | 0.680763 | 0.046725 | 0.153776 | 0.0601077 | 1.39857 | 2.69922 | 7.60454 | 9.98098 | 3.4634 | 49.0055 | 0.115875 | 0.0660344 | 0.00841897 | 0.169115 | 0.289568 | 0.359518 | 0.359518 | 0.263754 |
| Office Equipment & Services | 18 | 0.00444857 | 0.0586221 | 0.134655 | 0.184515 | 1.11147 | 1.38331 | 0.0737525 | 0.310057 | 0.0316 | 0.325493 | 0.057255 | 2.42981 | 1.31466 | 11.5733 | 21.6964 | 2.69943 | 38.427 | 0.0666719 | 0.0270989 | 0.112236 | 2.10279 | 0.0850105 | 0.713356 | 0.713356 | 0.0607985 |
| Oil/Gas (Integrated) | 4 | 0.060275 | 0.0719351 | 0.0512101 | 0.280777 | 1.25093 | 1.4654 | 0.0772329 | 0.287132 | 0.0316 | 0.210924 | 0.0658082 | 0.856843 | 1.59366 | 8.41561 | 21.4143 | 1.58488 | 22.8384 | 0.0355245 | 0.0543121 | -0.0588458 | -0.697781 | 0.0114574 | 6.82759 | 6.82759 | 0.0741569 |
| Oil/Gas (Production and Exploration) | 183 | 0.174164 | -0.0257352 | -0.0154042 | 0.182098 | 1.12799 | 1.31973 | 0.0710564 | 0.554756 | 0.03578 | 0.237377 | 0.0603894 | 0.642009 | 3.10424 | 8.27843 | NA | 2.20296 | 31.0143 | -0.111715 | 0.201683 | -0.115951 | NA | 0.0330142 | 1.25352 | 1.25352 | -0.0244931 |
| Oil/Gas Distribution | 21 | 0.238908 | 0.164779 | 0.0681076 | 0.202841 | 0.864511 | 1.39562 | 0.0742745 | 0.449805 | 0.03578 | 0.465687 | 0.0518493 | 0.455474 | 3.5872 | 13.0484 | 21.622 | 1.94776 | 262.077 | 0.0257683 | 0.0968377 | -0.00488255 | -0.0705512 | 0.0643652 | 1.96705 | 1.96705 | 0.165704 |
| Oilfield Svcs/Equip. | 100 | 0.0104954 | 0.0118054 | 0.0282204 | 0.264374 | 1.17917 | 1.4958 | 0.0785219 | 0.496346 | 0.03578 | 0.351184 | 0.060119 | 2.22632 | 0.735234 | 12.2751 | 51.6399 | 1.57761 | 48.8968 | 0.0736746 | 0.0241532 | -0.00740235 | -1.53969 | 0.0562223 | 0.889035 | 0.889035 | 0.0132012 |
| Packaging & Container | 26 | 0.0492033 | 0.0972508 | 0.154027 | 0.232208 | 0.778296 | 1.00971 | 0.0579115 | 0.263842 | 0.0316 | 0.33193 | 0.0463459 | 1.87118 | 1.63382 | 10.2281 | 16.5192 | 3.33353 | 20.0291 | 0.105502 | 0.0547875 | 0.0343484 | 0.572853 | 0.210178 | 0.322117 | 0.322117 | 0.0992168 |
| Paper/Forest Products | 11 | 0.015075 | 0.186424 | 0.448894 | 0.222782 | 0.998496 | 1.21352 | 0.0665531 | 0.306075 | 0.0316 | 0.292401 | 0.053838 | 2.71152 | 1.14122 | 4.82893 | 6.06544 | 2.84392 | 15.6403 | 0.113413 | 0.0287349 | 0.058668 | 0.319713 | 0.436709 | 0.109963 | 0.109963 | 0.18811 |
| Power | 50 | 0.0433187 | 0.187724 | 0.0605784 | 0.185188 | 0.557464 | 0.833073 | 0.0504223 | 0.194943 | 0.025 | 0.417032 | 0.0370054 | 0.383809 | 4.41447 | 12.3642 | 23.2712 | 2.08307 | 25.2459 | 0.0363814 | 0.332247 | 0.210091 | 1.42554 | 0.0814459 | 0.820297 | 0.820297 | 0.187016 |
| Precious Metals | 76 | 0.0797917 | 0.275787 | 0.147498 | 0.363926 | 0.987377 | 0.989452 | 0.0570528 | 0.562884 | 0.03578 | 0.107204 | 0.0537366 | 0.550483 | 4.24665 | 8.47789 | 14.5982 | 2.13435 | 22.8325 | 0.118635 | 0.173688 | 0.0171311 | 0.178474 | 0.0799167 | 0.782382 | 0.782382 | 0.276515 |
| Publishing & Newspapers | 21 | 0.0151813 | 0.077882 | 0.157654 | 0.211524 | 1.46426 | 1.69372 | 0.0869138 | 0.308002 | 0.0316 | 0.269041 | 0.0697366 | 2.2837 | 1.31237 | 9.57326 | 17.0306 | 2.04345 | 24.656 | 0.118612 | 0.0275678 | 0.0568445 | 0.905137 | 0.0844334 | 0.346483 | 0.346483 | 0.0779749 |
| R.E.I.T. | 238 | 0.0815933 | 0.238845 | 0.027483 | 0.0479303 | 0.988222 | 1.34874 | 0.0722867 | 0.326473 | 0.0316 | 0.349803 | 0.0550699 | 0.137416 | 14.228 | 26.8099 | 64.774 | 2.80508 | 62.7956 | 1.07092 | 0.028417 | -0.0335983 | -0.191723 | 0.0781189 | 1.12381 | 1.12381 | 0.20396 |
| Real Estate (Development) | 19 | -0.08428 | 0.0743586 | 0.0128843 | 0.213337 | 0.742441 | 1.06254 | 0.0601518 | 0.513223 | 0.03578 | 0.444254 | 0.0450328 | 0.256146 | 5.227 | 26.8377 | 93.9368 | 1.42694 | 494.994 | -0.106647 | 0.00580507 | -0.0835818 | -5.53621 | -0.0046114 | 0 | 0 | 0.051646 |
| Real Estate (General/Diversified) | 10 | 0.091 | 0.154572 | 0.0501013 | 0.206379 | 0.833266 | 0.906437 | 0.0535329 | 0.306987 | 0.0316 | 0.208903 | 0.0471687 | 0.362864 | 6.0613 | 19.9341 | 32.2319 | 1.33441 | 68.4544 | 2.5099 | 0.0173422 | 0.000725535 | 1.151 | 0.0628984 | 0.313146 | 0.313146 | 0.153303 |
| Real Estate (Operations & Services) | 51 | 0.0548619 | 0.0029081 | -0.0279793 | 0.229153 | 0.871125 | 1.14534 | 0.0636624 | 0.414286 | 0.03578 | 0.360469 | 0.0501293 | 1.34757 | 2.18287 | 20.8435 | NA | 3.65523 | 35.2658 | 0.268351 | 0.0143016 | 0.0101509 | NA | -0.108147 | 0.000692483 | 0.000692483 | -0.0225184 |
| Recreation | 60 | 0.0759969 | 0.113383 | 0.18444 | 0.19757 | 1.07363 | 1.22759 | 0.0671498 | 0.503546 | 0.03578 | 0.228268 | 0.0577839 | 1.85364 | 2.73283 | 13.32 | 24.0476 | 5.35204 | 28.2053 | 0.162066 | 0.0460354 | -0.0435953 | -0.299857 | 0.227629 | 0.479855 | 0.479855 | 0.107434 |
| Reinsurance | 2 | 0.10415 | 0.0734251 | 0.066892 | 0.22726 | 1.29503 | 1.37127 | 0.0732417 | 0.259455 | 0.0316 | 0.279797 | 0.0592032 | 1.19164 | 0.687828 | 7.48059 | 9.43935 | 0.751893 | 12.9871 | 0.0209112 | 0.00294688 | -0.00295051 | 0.098321 | 0.0582658 | 0.151873 | 0.151873 | 0.0728682 |
| Restaurant/Dining | 70 | 0.0470963 | 0.16434 | 0.147241 | 0.160689 | 1.33217 | 1.55739 | 0.0811333 | 0.427577 | 0.03578 | 0.214742 | 0.0693195 | 1.28971 | 5.12289 | 19.3241 | 41.1995 | NA | 31.3257 | 0.00231082 | 0.0497117 | 0.0183064 | 0.190355 | NA | 0.474326 | 0.474326 | 0.122899 |
| Retail (Automotive) | 32 | 0.146971 | 0.070347 | 0.154721 | 0.229429 | 1.12149 | 1.39803 | 0.0743766 | 0.44492 | 0.03578 | 0.278511 | 0.0609364 | 2.86899 | 1.17017 | 12.1613 | 18.4239 | 7.0608 | 14.0109 | 0.0827453 | 0.0169091 | 0.0339683 | 0.56414 | 0.471813 | 0.042642 | 0.042642 | 0.0628512 |
| Retail (Building Supply) | 16 | 0.174281 | 0.144039 | 0.546171 | 0.238465 | 1.41896 | 1.52463 | 0.0797444 | 0.447346 | 0.03578 | 0.118507 | 0.0733895 | 4.54641 | 2.63319 | 14.8674 | 18.5277 | 116.152 | 21.7789 | 0.0657031 | 0.0212661 | 0.0333873 | 0.517323 | 0.00974961 | 0.339007 | 0.339007 | 0.142166 |
| Retail (Distributors) | 68 | 0.0409634 | 0.0961538 | 0.162748 | 0.237519 | 1.06451 | 1.28108 | 0.0694176 | 0.431014 | 0.03578 | 0.244602 | 0.0588268 | 1.87739 | 1.84581 | 14.68 | 18.7593 | 4.22883 | 34.7027 | 0.156148 | 0.0566686 | 0.0760126 | 1.11723 | 0.195468 | 0.282043 | 0.282043 | 0.0981708 |
| Retail (General) | 16 | 0.0388785 | 0.0554049 | 0.208769 | 0.27823 | 1.03836 | 1.11555 | 0.0623993 | 0.338817 | 0.0316 | 0.138271 | 0.0569609 | 4.98633 | 0.963855 | 11.8436 | 18.7709 | 5.89092 | 42.239 | 0.00990324 | 0.0225495 | 0.00543319 | 0.273066 | 0.200581 | 0.3533 | 0.3533 | 0.0513402 |
| Retail (Grocery and Food) | 15 | 0.0324125 | 0.0253057 | 0.0700716 | 0.206066 | 0.212007 | 0.299676 | 0.0278062 | 0.342691 | 0.0316 | 0.405625 | 0.0258843 | 4.42309 | 0.44613 | 7.60332 | 24.0975 | 3.34675 | 17.7897 | -0.00875626 | 0.0235292 | 0.0052934 | 0.171528 | 0.1488 | 0.332494 | 0.332494 | 0.0182739 |
| Retail (Online) | 60 | 0.102 | 0.0599288 | 0.121816 | 0.154995 | 1.065 | 1.10381 | 0.0619015 | 0.588177 | 0.03578 | 0.0754342 | 0.0592023 | 1.7691 | 3.73324 | 26.2247 | 66.033 | 12.9033 | 144.261 | -0.0311344 | 0.108959 | 0.0724311 | 2.2109 | 0.441098 | 0.0133763 | 0.0133763 | 0.0714688 |
| Retail (Special Lines) | 76 | 0.11783 | 0.0686035 | 0.172763 | 0.237663 | 1.22896 | 1.44339 | 0.0762999 | 0.455723 | 0.03578 | 0.257911 | 0.0633578 | 2.99169 | 1.11101 | 8.46434 | 16.2034 | 5.44787 | 19.1374 | 0.056681 | 0.0180742 | 0.00961755 | 0.50997 | 0.352297 | 0.235007 | 0.235007 | 0.0676857 |
| Rubber& Tires | 2 | 0.042015 | 0.0540314 | 0.0728128 | 0.348103 | 0.589213 | 1.15651 | 0.0641358 | 0.47055 | 0.03578 | 0.607156 | 0.0410539 | 1.57532 | 0.87582 | 7.25678 | 15.3187 | 1.33123 | 17.5734 | 0.118114 | 0.0513607 | 0.114333 | 2.93693 | 0.0958544 | 0 | 0 | 0.0561781 |
| Semiconductor | 67 | 0.0662517 | 0.274184 | 0.217046 | 0.0873956 | 1.13582 | 1.16245 | 0.0643881 | 0.374564 | 0.0316 | 0.0634663 | 0.0617656 | 0.797641 | 8.68918 | 21.2746 | 31.3299 | 7.44673 | 582.021 | 0.174515 | 0.130191 | 0.0578553 | 0.289443 | 0.319062 | 0.289413 | 0.289413 | 0.290766 |
| Semiconductor Equip | 34 | 0.139942 | 0.26976 | 0.372445 | 0.105098 | 1.34142 | 1.33904 | 0.0718752 | 0.332228 | 0.0316 | 0.0479782 | 0.0695335 | 1.46456 | 6.07976 | 19.426 | 22.3146 | 10.2888 | 44.4435 | 0.28907 | 0.0427813 | 0.03366 | 0.4564 | 0.463794 | 0.151113 | 0.151113 | 0.279205 |
| Shipbuilding & Marine | 8 | 0.163933 | 0.172617 | 0.150082 | 0.195166 | 0.802317 | 0.991099 | 0.0571226 | 0.510373 | 0.03578 | 0.275173 | 0.0485913 | 0.877117 | 1.68592 | 6.49104 | 9.4717 | 1.49424 | 10.4778 | 0.0875633 | 0.116116 | 0.0500347 | 0.531251 | 0.102873 | 0.148602 | 0.148602 | 0.17675 |
| Shoe | 12 | 0.0638 | 0.155595 | 0.40946 | 0.131388 | 1.18849 | 1.18582 | 0.0653788 | 0.347149 | 0.0316 | 0.0546129 | 0.0630681 | 2.95507 | 4.85007 | 25.7745 | 31.3222 | 13.654 | 21.5758 | 0.171915 | 0.00777086 | 0.00274403 | 0.0643845 | 0.479087 | 0.23923 | 0.23923 | 0.153717 |
| Software (Entertainment) | 88 | 0.22906 | 0.311188 | 0.254601 | 0.163615 | 1.20755 | 1.20402 | 0.0661504 | 0.54606 | 0.03578 | 0.0199795 | 0.0653506 | 0.797907 | 8.1175 | 20.5129 | 25.6539 | 7.52088 | 34.6456 | 0.0610951 | 0.112833 | 0.0901777 | 0.486795 | 0.314044 | 0.00359456 | 0.00359456 | 0.325883 |
| Software (Internet) | 36 | 0.2206 | -0.022844 | 0.0164509 | 0.120593 | 0.975064 | 1.00438 | 0.0576857 | 0.38094 | 0.0316 | 0.071277 | 0.0552183 | 0.758396 | 17.0667 | 22.9781 | NA | 10.4996 | 62.864 | 0.106762 | 0.0653927 | 0.146117 | NA | -0.112863 | 0.00147624 | 0.00147624 | 0.0213888 |
| Software (System & Application) | 375 | 0.177223 | 0.240217 | 0.250316 | 0.104251 | 1.12245 | 1.14146 | 0.063498 | 0.457399 | 0.03578 | 0.0537315 | 0.0614896 | 0.995958 | 12.8387 | 32.7167 | 46.5071 | 14.5167 | 130.773 | 0.120526 | 0.0706974 | 0.176172 | 0.891947 | 0.304675 | 0.287168 | 0.287168 | 0.259402 |
| Steel | 28 | 0.199733 | 0.161292 | 0.372505 | 0.175479 | 0.982557 | 1.13317 | 0.0631464 | 0.331282 | 0.0316 | 0.24739 | 0.0532314 | 2.65643 | 0.882484 | 4.45909 | 5.42856 | 1.84133 | 13.1835 | 0.231354 | 0.0403384 | 0.0406756 | 0.902453 | 0.400477 | 0.0845026 | 0.0845026 | 0.161754 |
| Telecom (Wireless) | 17 | -0.0159629 | 0.116994 | 0.0518064 | 0.154045 | 0.62723 | 0.964761 | 0.0560059 | 0.481577 | 0.03578 | 0.439171 | 0.0428806 | 0.539016 | 2.95963 | 7.78547 | 30.0206 | 1.92307 | 52.3394 | 0.0826673 | 0.169275 | -0.0110293 | 0.724316 | 0.059312 | 0.0243703 | 0.0243703 | 0.0993232 |
| Telecom. Equipment | 82 | 0.0665884 | 0.1956 | 0.268421 | 0.185533 | 1.05686 | 1.08314 | 0.0610253 | 0.405293 | 0.03578 | 0.0803081 | 0.0582221 | 1.38696 | 4.73565 | 18.1591 | 23.5157 | 6.14564 | 65.1471 | 0.192572 | 0.0252956 | 0.092631 | 0.735326 | 0.249287 | 0.46151 | 0.46151 | 0.204015 |
| Telecom. Services | 42 | 0.101218 | 0.209424 | 0.153329 | 0.23964 | 0.509153 | 0.846018 | 0.0509712 | 0.386723 | 0.0316 | 0.501205 | 0.036986 | 0.784582 | 2.43851 | 6.60619 | 11.715 | 1.53096 | 37.3028 | -0.0158004 | 0.113061 | 0.052744 | 0.386678 | 0.10413 | 0.980285 | 0.980285 | 0.207576 |
| Tobacco | 16 | 0.069115 | 0.442498 | 0.644484 | 0.245353 | 0.862249 | 0.997353 | 0.0573878 | 0.248828 | 0.025 | 0.206232 | 0.0493163 | 1.58288 | 5.05743 | 10.6956 | 11.3733 | NA | 14.6423 | 0.133781 | 0.0152622 | 0.0432166 | 0.0989917 | NA | 1.18177 | 1.18177 | 0.443664 |
| Transportation | 17 | 0.108591 | 0.0824653 | 0.210506 | 0.233336 | 0.715815 | 0.791078 | 0.0486417 | 0.283353 | 0.0316 | 0.186314 | 0.043877 | 3.0324 | 1.52029 | 11.4165 | 18.7379 | 6.20255 | 28.2274 | 0.0821219 | 0.052218 | 0.0210254 | 0.701587 | 0.402374 | 0.320611 | 0.320611 | 0.0810937 |
| Transportation (Railroads) | 4 | 0.0167 | 0.419479 | 0.153055 | 0.231397 | 0.647608 | 0.732447 | 0.0461558 | 0.163942 | 0.025 | 0.166232 | 0.0415169 | 0.445484 | 8.55387 | 15.8694 | 20.5795 | 7.75585 | 24.7071 | 0.0277077 | 0.129128 | 0.0326855 | 0.102993 | 0.283482 | 0.356272 | 0.356272 | 0.415648 |
| Trucking | 34 | 0.0760318 | 0.0517303 | 0.0576228 | 0.239849 | 1.27849 | 1.43872 | 0.0761016 | 0.329918 | 0.0316 | 0.207969 | 0.0650722 | 1.31329 | 2.58783 | 9.93295 | 31.3039 | 4.89835 | 20.7149 | 0.0495529 | 0.120607 | 0.0784772 | 3.25082 | 0.0554278 | 0.344137 | 0.344137 | 0.0524689 |
| Utility (General) | 16 | 0.0273069 | 0.192268 | 0.0591178 | 0.121025 | 0.596219 | 0.891795 | 0.0529121 | 0.188282 | 0.025 | 0.409042 | 0.0387338 | 0.34551 | 4.81242 | 14.2975 | 25.3779 | 2.08803 | 21.9373 | 0.114025 | 0.34443 | 0.206693 | 1.25229 | 0.0844414 | 0.807664 | 0.807664 | 0.189596 |
| Utility (Water) | 14 | 0.145792 | 0.301549 | 0.0728825 | 0.12526 | 0.61418 | 0.765305 | 0.0475489 | 0.270945 | 0.0316 | 0.255628 | 0.0412909 | 0.270532 | 10.3938 | 22.422 | 34.6213 | 3.94416 | 43.4155 | 0.182227 | 0.446128 | 0.322737 | 1.30493 | 0.181221 | 0.569801 | 0.330616 | 0.299358 |

### Global Industry averages sheet (A1:AA95)

Identical layout and column meanings to the US sheet, computed over global firms. Used by the "Multi Business (Global Industry Averages)" calculator (VLOOKUP cols 7 and 15 of A2:Z95):

| Industry Name | Number of firms | Annual Average Revenue growth - Last 5 years | Pre-tax Operating Margin (Unadjusted) | After-tax ROC | Average effective tax rate | Unlevered Beta | Equity (Levered) Beta | Cost of equity | Std deviation in stock prices | Pre-tax cost of debt | Market Debt/Capital | Cost of capital | Sales/Capital | EV/Sales | EV/EBITDA | EV/EBIT | Price/Book | Trailing PE | Non-cash WC as % of Revenues | Cap Ex as % of Revenues | Net Cap Ex as % of Revenues | Reinvestment Rate | ROE | Dividend Payout Ratio | Equity Reinvestment Rate | Pre-tax Operating Margin (Lease & R&D adjusted) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Advertising | 348 | 0.0493011 | 0.0845431 | 0.212548 | 0.310046 | 1.18466 | 1.29202 | 0.0830603 | 0.382796 | 0.0404 | 0.245552 | 0.0699998 | 2.7953 | 1.75148 | 12.2449 | 19.0038 | 2.73363 | 74.8121 | -0.0420513 | 0.0142563 | -0.00895238 | -0.313137 | 0.0563345 | 0.73983 | 0.73983 | 0.0881879 |
| Aerospace/Defense | 272 | 0.0860367 | 0.0749995 | 0.12703 | 0.156914 | 1.11169 | 1.22314 | 0.0794374 | 0.331944 | 0.0404 | 0.206086 | 0.0692226 | 1.84319 | 2.13981 | 14.5802 | 23.3494 | 4.3241 | 70.1717 | 0.417903 | 0.0309306 | 0.0126126 | 0.587547 | 0.144223 | 0.447944 | 0.447944 | 0.0760201 |
| Air Transport | 151 | -0.0881397 | -0.214492 | -0.108376 | 0.189387 | 0.939547 | 1.59243 | 0.0988618 | 0.309298 | 0.0404 | 0.558227 | 0.0603497 | 0.520425 | 3.25032 | 24.0388 | NA | 2.75183 | 721.842 | -0.0822456 | 0.122118 | -0.0215508 | NA | -0.367183 | 0.00353245 | 0.00353245 | -0.217942 |
| Apparel | 1170 | 0.0185645 | 0.139876 | 0.17908 | 0.242024 | 0.903344 | 0.954341 | 0.0652983 | 0.31365 | 0.0404 | 0.140298 | 0.0603281 | 1.46291 | 3.12805 | 16.1945 | 21.7127 | 4.13124 | 39.2412 | 0.220059 | 0.0370769 | 0.0676154 | 0.568915 | 0.167306 | 0.358134 | 0.358134 | 0.141967 |
| Auto & Truck | 152 | 0.0802998 | 0.0664275 | 0.0631513 | 0.231542 | 1.1106 | 1.35421 | 0.0863315 | 0.314859 | 0.0404 | 0.323696 | 0.0680557 | 1.03297 | 1.65776 | 14.1787 | 23.2954 | 2.27249 | 96.3203 | 0.0460136 | 0.0688827 | 0.0303565 | 0.6373 | 0.12849 | 0.18454 | 0.18454 | 0.0684718 |
| Auto Parts | 728 | 0.0438323 | 0.0568711 | 0.0794829 | 0.229471 | 1.43605 | 1.52621 | 0.0953784 | 0.297996 | 0.0404 | 0.218006 | 0.0810976 | 1.64242 | 0.965669 | 8.63036 | 16.0352 | 1.76096 | 54.5367 | 0.117456 | 0.045363 | 0.0262591 | 0.83229 | 0.0911653 | 0.309662 | 0.309662 | 0.0579761 |
| Bank (Money Center) | 610 | 0.0871595 | 0.00150711 | 0.000199267 | 0.193085 | 0.590604 | 1.03252 | 0.0694107 | 0.204236 | 0.0338 | 0.730917 | 0.0369441 | 0.14974 | 6.35365 | NA | NA | 0.849166 | 28.8839 | NA | 0.0325059 | 0.0316136 | 20.9119 | 0.112423 | 0.273491 | 0.273491 | 0.00167369 |
| Banks (Regional) | 816 | 0.090463 | 0.00010329 | -0.000198789 | 0.203687 | 0.66677 | 0.737233 | 0.0538785 | 0.192155 | 0.0338 | 0.639594 | 0.0354027 | 0.22939 | 4.4604 | NA | NA | 0.939148 | 24.9035 | NA | 0.0473939 | 0.0798446 | NA | 0.0978131 | 0.266411 | 0.266411 | -0.00108171 |
| Beverage (Alcoholic) | 219 | 0.0558078 | 0.217949 | 0.130238 | 0.260705 | 0.860183 | 0.920902 | 0.0635395 | 0.252048 | 0.0404 | 0.12924 | 0.0591882 | 0.723175 | 5.30098 | 19.766 | 24.1954 | 4.44812 | 44.8515 | 0.0880922 | 0.0419663 | 0.00381457 | 0.000619046 | 0.14566 | 0.438901 | 0.438901 | 0.218284 |
| Beverage (Soft) | 100 | 0.0753152 | 0.17191 | 0.222039 | 0.244336 | 0.815904 | 0.883821 | 0.061589 | 0.306838 | 0.0404 | 0.142818 | 0.0570592 | 1.45474 | 4.19093 | 19.4018 | 24.2643 | 6.65541 | 70.24 | -0.0517637 | 0.0447945 | 0.04136 | 0.286459 | 0.24732 | 0.754152 | 0.754152 | 0.172413 |
| Broadcasting | 139 | 0.0180597 | 0.157398 | 0.148439 | 0.227607 | 0.812203 | 1.09402 | 0.0726457 | 0.328373 | 0.0404 | 0.403557 | 0.055384 | 1.13937 | 1.5854 | 7.33947 | 9.97269 | 1.13642 | 41.5996 | 0.0968955 | 0.0334655 | 0.0153615 | 0.728831 | 0.133463 | 0.250468 | 0.250468 | 0.156622 |
| Brokerage & Investment Banking | 599 | 0.154942 | 0.0184522 | 0.00365983 | 0.219639 | 0.453834 | 0.916449 | 0.0633052 | 0.302701 | 0.0404 | 0.663548 | 0.0411205 | 0.219457 | 6.11185 | 145.398 | NA | 1.4822 | 35.4003 | NA | 0.0301992 | -0.00237995 | -10.3681 | 0.147084 | 0.369751 | 0.369751 | 0.0193544 |
| Building Materials | 449 | 0.0630216 | 0.113229 | 0.18208 | 0.235231 | 1.05337 | 1.11884 | 0.0739512 | 0.280339 | 0.0404 | 0.151466 | 0.0672747 | 1.92073 | 2.00165 | 12.8831 | 17.4288 | 3.3422 | 66.2767 | 0.163147 | 0.0379755 | 0.0329597 | 0.496924 | 0.169854 | 0.273405 | 0.273405 | 0.114697 |
| Business & Consumer Services | 948 | 0.0599591 | 0.0841613 | 0.195132 | 0.255224 | 1.03666 | 1.1059 | 0.0732701 | 0.323425 | 0.0404 | 0.155018 | 0.0665426 | 2.71555 | 2.34819 | 17.0779 | 26.1981 | 4.47061 | 83.4495 | 0.0990173 | 0.022459 | 0.0187326 | 0.41382 | 0.154011 | 0.397151 | 0.397151 | 0.0860054 |
| Cable TV | 54 | 0.0362659 | 0.190223 | 0.130087 | 0.250144 | 0.715209 | 0.991863 | 0.067272 | 0.253941 | 0.0404 | 0.368714 | 0.053482 | 0.804911 | 3.24695 | 9.79443 | 17.0761 | 2.67137 | 30.6336 | 0.00721162 | 0.107858 | -0.0117781 | -0.0560671 | 0.152194 | 0.252047 | 0.252047 | 0.190226 |
| Chemical (Basic) | 854 | 0.101838 | 0.125485 | 0.136933 | 0.19099 | 1.02199 | 1.13612 | 0.07486 | 0.295189 | 0.0404 | 0.223478 | 0.0648061 | 1.27688 | 1.59766 | 8.80023 | 12.333 | 1.92227 | 71.653 | 0.127013 | 0.0839927 | 0.0598902 | 0.860744 | 0.179042 | 0.294073 | 0.294073 | 0.127358 |
| Chemical (Diversified) | 71 | 0.060421 | 0.11509 | 0.110009 | 0.211535 | 1.14763 | 1.40315 | 0.0889059 | 0.248028 | 0.0338 | 0.306195 | 0.0693357 | 1.19284 | 1.20267 | 6.93248 | 10.3659 | 1.44405 | 19.8168 | 0.166957 | 0.0535033 | 0.023175 | 0.448613 | 0.133992 | 0.368791 | 0.368791 | 0.114971 |
| Chemical (Specialty) | 898 | 0.0951498 | 0.135995 | 0.14707 | 0.2015 | 1.03948 | 1.10694 | 0.073325 | 0.307647 | 0.0404 | 0.137179 | 0.0673641 | 1.25224 | 2.90433 | 14.5576 | 20.9792 | 3.36054 | 45.9671 | 0.177308 | 0.0721854 | 0.0465842 | 0.563172 | 0.154596 | 0.334727 | 0.334727 | 0.138547 |
| Coal & Related Energy | 206 | 0.102478 | 0.17168 | 0.180465 | 0.224993 | 1.09104 | 1.12695 | 0.0743774 | 0.449006 | 0.04458 | 0.291635 | 0.0622993 | 1.12486 | 1.23717 | 4.70886 | 6.79132 | 1.1762 | 51.0367 | -0.0185692 | 0.0710844 | 0.0379495 | 0.264461 | 0.134619 | 0.634384 | 0.634384 | 0.173072 |
| Computer Services | 1040 | 0.0884134 | 0.071006 | 0.212161 | 0.23769 | 1.08725 | 1.11948 | 0.0739847 | 0.317802 | 0.0404 | 0.110716 | 0.0691007 | 3.44457 | 1.66935 | 15.8766 | 22.3708 | 4.72325 | 77.4909 | 0.143961 | 0.0147348 | 0.0124084 | 0.342475 | 0.162037 | 0.453505 | 0.453505 | 0.0738927 |
| Computers/Peripherals | 336 | 0.0420037 | 0.134208 | 0.227312 | 0.170357 | 1.32739 | 1.35456 | 0.0863497 | 0.338659 | 0.0404 | 0.084819 | 0.0815593 | 1.87957 | 2.79425 | 15.5573 | 20.6027 | 6.76652 | 41.6337 | 0.0222487 | 0.0469252 | 0.0328273 | 0.370296 | 0.34075 | 0.257428 | 0.257428 | 0.137175 |
| Construction Supplies | 784 | 0.0742345 | 0.0997 | 0.103108 | 0.214138 | 1.02193 | 1.15719 | 0.0759682 | 0.284282 | 0.0404 | 0.265543 | 0.0637276 | 1.18772 | 1.53599 | 9.69964 | 14.4132 | 1.6546 | 83.1805 | 0.110585 | 0.0535918 | 0.0357967 | 0.635033 | 0.112614 | 0.487211 | 0.487211 | 0.101961 |
| Diversified | 318 | 0.0793339 | 0.170948 | 0.12454 | 0.184569 | 0.819452 | 1.05387 | 0.0705337 | 0.238748 | 0.0338 | 0.362329 | 0.0540325 | 0.850059 | 1.83189 | 8.38314 | 10.344 | 1.20047 | 35.8128 | -0.200722 | 0.0455524 | 0.035727 | 0.293522 | 0.153111 | 0.140031 | 0.140031 | 0.171359 |
| Drugs (Biotechnology) | 1223 | 0.27256 | 0.108662 | 0.0705061 | 0.127127 | 1.1008 | 1.10449 | 0.0731961 | 0.454207 | 0.04458 | 0.104828 | 0.0689784 | 0.491988 | 7.87057 | 14.1329 | 52.1429 | 5.87739 | 188.72 | 0.178682 | 0.0563195 | 0.137883 | 2.43818 | -0.0126523 | 0.00174692 | 0.00174692 | 0.145531 |
| Drugs (Pharmaceutical) | 1371 | 0.177845 | 0.214437 | 0.155339 | 0.160897 | 1.01951 | 1.07756 | 0.0717797 | 0.397863 | 0.0404 | 0.12883 | 0.0663807 | 0.723728 | 4.30722 | 14.0176 | 19.3956 | 3.90707 | 54.4375 | 0.150452 | 0.0486961 | 0.0574335 | 0.391811 | 0.125959 | 0.743144 | 0.743144 | 0.234487 |
| Education | 244 | 0.0777738 | 0.0961401 | 0.0844277 | 0.178215 | 0.997308 | 1.06318 | 0.0710234 | 0.323764 | 0.0404 | 0.235346 | 0.0613385 | 0.951058 | 2.73821 | 12.4144 | 24.5661 | 2.14198 | 172.07 | -0.00971189 | 0.0828342 | 0.153249 | 2.08129 | 0.0350868 | 0.809011 | 0.809011 | 0.101494 |
| Electrical Equipment | 999 | 0.0856754 | 0.0709826 | 0.112328 | 0.195697 | 1.0807 | 1.09634 | 0.0727675 | 0.337176 | 0.0404 | 0.109227 | 0.0680821 | 1.70497 | 2.61971 | 21.8183 | 34.2074 | 3.77 | 66.4108 | 0.216368 | 0.0551959 | 0.0631842 | 1.41786 | 0.0958871 | 0.508062 | 0.508062 | 0.0747678 |
| Electronics (Consumer & Office) | 138 | 0.0254224 | 0.063684 | 0.116673 | 0.183599 | 1.18683 | 1.29074 | 0.0829927 | 0.315366 | 0.0404 | 0.232382 | 0.0706483 | 1.68094 | 1.0566 | 9.89884 | 16.0259 | 1.89004 | 167.973 | 0.0396188 | 0.0473387 | 0.0654613 | 1.4956 | 0.146494 | 0.221925 | 0.221925 | 0.0769628 |
| Electronics (General) | 1425 | 0.0730618 | 0.0834228 | 0.143367 | 0.168443 | 1.31158 | 1.30033 | 0.0834976 | 0.310285 | 0.0404 | 0.11551 | 0.0773032 | 1.57647 | 1.94309 | 14.6151 | 22.4976 | 3.03017 | 70.1456 | 0.185486 | 0.0595457 | 0.0634127 | 1.28983 | 0.133001 | 0.318636 | 0.318636 | 0.10123 |
| Engineering/Construction | 1267 | 0.0348621 | 0.0480726 | 0.0905371 | 0.242839 | 0.84476 | 1.12342 | 0.0741917 | 0.294324 | 0.0404 | 0.466191 | 0.0535301 | 2.10783 | 0.625236 | 8.96095 | 12.2524 | 1.04593 | 76.3743 | 0.155091 | 0.0361864 | 0.026091 | 1.12466 | 0.104462 | 0.571666 | 0.571666 | 0.0505933 |
| Entertainment | 734 | 0.0705569 | 0.0932439 | 0.112096 | 0.212046 | 1.107 | 1.14191 | 0.0751647 | 0.386384 | 0.0404 | 0.132998 | 0.0691408 | 1.18451 | 4.91961 | 24.128 | 45.3781 | 4.02811 | 133.634 | 0.0125899 | 0.0366547 | 0.0270759 | 0.409216 | 0.0476014 | 0.545629 | 0.545629 | 0.102062 |
| Environmental & Waste Services | 353 | 0.084489 | 0.110652 | 0.125556 | 0.201071 | 0.895972 | 1.04445 | 0.0700378 | 0.337446 | 0.0404 | 0.233749 | 0.060649 | 1.28503 | 3.02109 | 15.3801 | 25.7643 | 3.40693 | 67.9873 | 0.11989 | 0.0825784 | 0.107517 | 1.67008 | 0.0947712 | 0.608429 | 0.608429 | 0.112169 |
| Farming/Agriculture | 417 | 0.105325 | 0.0726044 | 0.0998782 | 0.20704 | 0.767626 | 0.949012 | 0.065018 | 0.303269 | 0.0404 | 0.300569 | 0.0544541 | 1.52702 | 1.28179 | 12.195 | 16.8707 | 2.25953 | 69.9667 | 0.145174 | 0.0490962 | 0.0326073 | 1.21409 | 0.14076 | 0.334103 | 0.334103 | 0.0747047 |
| Financial Svcs. (Non-bank & Insurance) | 1102 | 0.0905216 | 0.101221 | 0.00649434 | 0.17832 | 0.195822 | 0.887264 | 0.0617701 | 0.300193 | 0.0404 | 0.841855 | 0.0349163 | 0.0750818 | 15.5256 | 74.4384 | 90.5156 | 1.50756 | 41.8326 | NA | 0.0522281 | 0.0663547 | 0.86419 | 0.252749 | 0.183744 | 0.183744 | 0.101872 |
| Food Processing | 1377 | 0.0919442 | 0.0925078 | 0.138489 | 0.217268 | 0.768545 | 0.859012 | 0.060284 | 0.267934 | 0.0404 | 0.197557 | 0.0542759 | 1.76238 | 1.7922 | 13.6838 | 18.9453 | 2.77753 | 60.0414 | 0.100139 | 0.0499464 | 0.0394338 | 0.711646 | 0.135773 | 0.520144 | 0.520144 | 0.0926328 |
| Food Wholesalers | 160 | 0.0513342 | 0.0224235 | 0.0951796 | 0.270104 | 0.603297 | 0.86239 | 0.0604617 | 0.300634 | 0.0404 | 0.429885 | 0.0473115 | 5.05167 | 0.451341 | 11.987 | 20.2911 | 2.14877 | 24.8297 | 0.0472956 | 0.0112013 | 0.0124074 | 1.09209 | 0.0649238 | 0.907866 | 0.907866 | 0.0220458 |
| Furn/Home Furnishings | 359 | 0.0906829 | 0.0899057 | 0.217564 | 0.178068 | 1.14573 | 1.13951 | 0.0750384 | 0.290809 | 0.0404 | 0.156424 | 0.0679733 | 2.73244 | 1.3898 | 11.6308 | 15.1295 | 3.28028 | 27.38 | 0.0412331 | 0.0331469 | 0.0249219 | 0.504911 | 0.206294 | 0.462125 | 0.462125 | 0.0940451 |
| Green & Renewable Energy | 239 | 0.164065 | 0.334859 | 0.0803234 | 0.167411 | 0.759353 | 1.00681 | 0.0680584 | 0.326604 | 0.0404 | 0.341203 | 0.055029 | 0.266234 | 8.8092 | 15.8514 | 25.6546 | 2.3456 | 91.9923 | 0.0695641 | 0.366883 | 0.254343 | 1.09308 | 0.102627 | 0.856005 | 0.856005 | 0.334314 |
| Healthcare Products | 852 | 0.160281 | 0.19025 | 0.1921 | 0.164285 | 1.00516 | 1.03014 | 0.0692854 | 0.380646 | 0.0404 | 0.0819021 | 0.0660573 | 1.04585 | 5.88733 | 20.9742 | 29.4623 | 5.30943 | 83.313 | 0.226389 | 0.0566509 | 0.0976849 | 0.677007 | 0.163486 | 0.300215 | 0.300215 | 0.198221 |
| Healthcare Support Services | 445 | 0.162069 | 0.0443951 | 0.249193 | 0.230408 | 0.853296 | 0.959799 | 0.0655854 | 0.346947 | 0.0404 | 0.215668 | 0.0578831 | 6.63598 | 0.784387 | 12.683 | 17.2867 | 2.99638 | 36.2616 | -0.0224112 | 0.0096067 | 0.0154106 | 0.552024 | 0.133422 | 0.306186 | 0.306186 | 0.0437543 |
| Heathcare Information and Technology | 455 | 0.160673 | 0.173813 | 0.20985 | 0.176659 | 1.03069 | 1.05559 | 0.0706238 | 0.395434 | 0.0404 | 0.074149 | 0.0676021 | 1.20505 | 8.39962 | 29.0376 | 44.2736 | 6.31264 | 83.5932 | 0.206387 | 0.0660788 | 0.187772 | 1.50917 | 0.179992 | 0.0906943 | 0.0906943 | 0.186088 |
| Homebuilding | 168 | 0.115348 | 0.136955 | 0.14906 | 0.230256 | 1.36803 | 1.47615 | 0.0927452 | 0.293323 | 0.0404 | 0.24712 | 0.077208 | 1.46055 | 1.22586 | 8.02774 | 9.46147 | 1.74931 | 17.0316 | 0.570916 | 0.00883863 | 0.00554368 | 0.343449 | 0.198154 | 0.195601 | 0.195601 | 0.128468 |
| Hospitals/Healthcare Facilities | 223 | 0.0871541 | 0.113431 | 0.12182 | 0.205534 | 0.736653 | 0.962122 | 0.0657076 | 0.290272 | 0.0404 | 0.327652 | 0.0539659 | 1.30747 | 2.4365 | 13.5215 | 21.5 | 3.89307 | 96.2302 | 0.0933461 | 0.0647885 | 0.0374656 | 0.579659 | 0.211108 | 0.241279 | 0.241279 | 0.110739 |
| Hotel/Gaming | 654 | -0.0901821 | -0.0798221 | -0.0350402 | 0.272107 | 0.949519 | 1.19435 | 0.0779227 | 0.322519 | 0.0404 | 0.328941 | 0.0621167 | 0.388931 | 6.5791 | 24.7131 | NA | 3.36267 | 160.442 | 0.00500545 | 0.10452 | 0.00815757 | NA | -0.163745 | 0.00587105 | 0.00587105 | -0.0959886 |
| Household Products | 575 | 0.0474997 | 0.157247 | 0.250885 | 0.224628 | 0.997516 | 1.04085 | 0.0698484 | 0.357154 | 0.0404 | 0.0995095 | 0.0658704 | 1.80311 | 3.82125 | 18.8092 | 23.9755 | 6.37917 | 49.0774 | 0.0578725 | 0.0357368 | 0.0216905 | 0.188179 | 0.190553 | 0.746142 | 0.746142 | 0.15811 |
| Information Services | 266 | 0.11343 | 0.202271 | 0.260417 | 0.197446 | 1.22686 | 1.26755 | 0.081773 | 0.397471 | 0.0404 | 0.0970744 | 0.0767347 | 1.47181 | 7.92242 | 26.3034 | 36.6722 | 7.24243 | 84.2737 | 0.0293002 | 0.0280728 | 0.0409485 | 0.388554 | 0.159232 | 0.292625 | 0.292625 | 0.206069 |
| Insurance (General) | 215 | 0.0641441 | 0.103239 | 0.14195 | 0.226379 | 0.717759 | 0.78421 | 0.0563494 | 0.230256 | 0.0338 | 0.28119 | 0.047532 | 1.60842 | 0.976443 | 7.98633 | 9.34012 | 1.29796 | 23.9653 | -0.000549862 | 0.00594128 | 0.00122348 | -0.0173775 | 0.121915 | 0.407847 | 0.407847 | 0.103265 |
| Insurance (Life) | 142 | 0.100394 | 0.104188 | 0.109426 | 0.164895 | 0.996728 | 1.07699 | 0.0717498 | 0.22916 | 0.0338 | 0.519029 | 0.047481 | 1.26101 | 0.826036 | 7.25413 | 7.63802 | 0.873293 | 44.1454 | -0.971998 | 0.00508117 | 0.00604961 | 0.0854267 | 0.10047 | 0.290227 | 0.290227 | 0.104232 |
| Insurance (Prop/Cas.) | 231 | 0.054199 | 0.115394 | 0.132959 | 0.191365 | 0.818309 | 0.883738 | 0.0615846 | 0.259468 | 0.0404 | 0.219023 | 0.0546388 | 1.36271 | 1.04458 | 7.65428 | 8.8721 | 1.2323 | 25.4166 | -0.453383 | 0.00723351 | 0.0129338 | 0.25173 | 0.129107 | 0.305266 | 0.305266 | 0.115497 |
| Investments & Asset Management | 1706 | 0.281224 | 0.202242 | 0.100859 | 0.141144 | 0.71914 | 0.861626 | 0.0604215 | 0.314716 | 0.0404 | 0.311635 | 0.0509012 | 0.523879 | 4.56945 | 14.7826 | 16.4077 | 2.02519 | 55.3448 | NA | 0.0128312 | 0.0416752 | 0.23792 | 0.196694 | 0.304437 | 0.304437 | 0.202009 |
| Machinery | 1421 | 0.0689302 | 0.0994956 | 0.1314 | 0.218106 | 1.12505 | 1.14366 | 0.0752566 | 0.277138 | 0.0404 | 0.117634 | 0.0699178 | 1.52479 | 2.38377 | 16.3034 | 22.9522 | 3.33946 | 53.6167 | 0.251217 | 0.0385638 | 0.0306651 | 0.565517 | 0.125081 | 0.39593 | 0.39593 | 0.10194 |
| Metals & Mining | 1706 | 0.186234 | 0.159782 | 0.216054 | 0.298259 | 1.01204 | 1.09754 | 0.0728306 | 0.530665 | 0.04458 | 0.206231 | 0.0646085 | 1.40409 | 1.49011 | 6.37501 | 8.75838 | 2.06655 | 309.056 | 0.107437 | 0.0642288 | 0.0302474 | 0.475738 | 0.188989 | 0.395023 | 0.395023 | 0.160918 |
| Office Equipment & Services | 145 | 0.0214156 | 0.0718066 | 0.123219 | 0.254913 | 1.05162 | 1.1006 | 0.0729915 | 0.297725 | 0.0404 | 0.210843 | 0.0639 | 1.93703 | 1.17363 | 10.0656 | 15.3572 | 2.02761 | 64.4075 | 0.121356 | 0.0277462 | 0.0491582 | 0.901618 | 0.0829035 | 0.442991 | 0.442991 | 0.073259 |
| Oil/Gas (Integrated) | 46 | 0.0732121 | 0.119045 | 0.104745 | 0.386413 | 1.14895 | 1.27882 | 0.0823661 | 0.246938 | 0.0338 | 0.211415 | 0.0702363 | 1.13645 | 1.47156 | 7.02904 | 12.3063 | 1.70088 | 19.9493 | 0.0233422 | 0.0823836 | -0.00980966 | -0.0516946 | 0.116434 | 0.696929 | 0.696929 | 0.11962 |
| Oil/Gas (Production and Exploration) | 642 | 0.211859 | 0.124955 | 0.0635879 | 0.278404 | 1.20877 | 1.4593 | 0.0918593 | 0.507344 | 0.04458 | 0.279344 | 0.0754069 | 0.530345 | 2.84524 | 6.23357 | 21.4119 | 1.56445 | 38.5955 | -0.035671 | 0.224048 | 0.00441573 | 0.303454 | 0.0611066 | 0.700857 | 0.700857 | 0.126532 |
| Oil/Gas Distribution | 165 | 0.151522 | 0.12396 | 0.0624317 | 0.186409 | 0.745269 | 1.16468 | 0.0763624 | 0.283289 | 0.0404 | 0.451891 | 0.0553537 | 0.573702 | 2.67896 | 12.9481 | 21.4159 | 1.57205 | 65.4748 | 0.0430203 | 0.106966 | 0.0362442 | 0.371035 | 0.0691066 | 1.40676 | 1.40676 | 0.124409 |
| Oilfield Svcs/Equip. | 457 | 0.0566004 | 0.0437722 | 0.0735168 | 0.230548 | 1.05969 | 1.35908 | 0.0865878 | 0.365753 | 0.0404 | 0.348631 | 0.0668148 | 1.84888 | 0.809479 | 9.63997 | 17.5795 | 1.40935 | 49.7983 | 0.0653631 | 0.0382818 | 0.0118064 | 0.704382 | 0.0881367 | 0.398235 | 0.398235 | 0.0444584 |
| Packaging & Container | 414 | 0.0543688 | 0.0915231 | 0.121512 | 0.221683 | 0.803195 | 0.961377 | 0.0656684 | 0.281076 | 0.0404 | 0.266102 | 0.0561429 | 1.58704 | 1.64831 | 11.0051 | 17.7455 | 2.61719 | 34.6408 | 0.139316 | 0.0642461 | 0.0414753 | 0.740366 | 0.144263 | 0.36393 | 0.36393 | 0.0928936 |
| Paper/Forest Products | 272 | 0.0547215 | 0.141598 | 0.124635 | 0.214247 | 0.894646 | 1.12065 | 0.074046 | 0.285354 | 0.0404 | 0.336675 | 0.0591737 | 1.0149 | 1.41049 | 6.98658 | 9.80905 | 1.35771 | 24.7941 | 0.185433 | 0.074804 | 0.0360776 | 0.360164 | 0.16842 | 0.237685 | 0.237685 | 0.142798 |
| Power | 541 | 0.0740769 | 0.112731 | 0.0575609 | 0.210612 | 0.539242 | 0.850571 | 0.05984 | 0.219397 | 0.0338 | 0.471257 | 0.0434175 | 0.609762 | 2.26344 | 10.3865 | 19.7505 | 1.35919 | 50.3138 | 0.00422689 | 0.164739 | 0.0865556 | 1.06696 | 0.0786036 | 0.821307 | 0.821307 | 0.112745 |
| Precious Metals | 947 | 0.252017 | 0.249782 | 0.228357 | 0.266764 | 0.988173 | 0.998098 | 0.0676 | 0.511526 | 0.04458 | 0.128008 | 0.0631661 | 0.952622 | 2.5021 | 6.25213 | 9.13128 | 1.97525 | 73.346 | 0.116437 | 0.155222 | 0.1009 | 0.660691 | 0.170374 | 0.366128 | 0.366128 | 0.250231 |
| Publishing & Newspapers | 337 | -0.000193529 | 0.0657545 | 0.0834778 | 0.206377 | 0.940295 | 0.932657 | 0.0641578 | 0.274071 | 0.0404 | 0.206412 | 0.0570807 | 1.44904 | 1.34321 | 11.379 | 19.5378 | 1.43439 | 40.2211 | 0.106984 | 0.0307248 | 0.029517 | 0.388989 | 0.162563 | 0.187803 | 0.187803 | 0.0664882 |
| R.E.I.T. | 812 | 0.0809107 | 0.312515 | 0.0342606 | 0.05796 | 0.766758 | 1.06554 | 0.0711474 | 0.239207 | 0.0338 | 0.363558 | 0.0543671 | 0.121736 | 13.4806 | 26.1465 | 40.9638 | 1.93702 | 126.291 | 0.746155 | 0.0870439 | 0.101416 | 0.372095 | 0.0681931 | 0.949187 | 0.949187 | 0.289226 |
| Real Estate (Development) | 893 | 0.0847955 | 0.140216 | 0.0777871 | 0.329231 | 0.516198 | 0.999628 | 0.0676804 | 0.27273 | 0.0404 | 0.672313 | 0.0422612 | 0.66756 | 1.44189 | 8.94344 | 9.69762 | 0.517473 | 68.1305 | 1.80555 | 0.026775 | 0.0243987 | 0.64795 | 0.118513 | 0.59687 | 0.59687 | 0.14051 |
| Real Estate (General/Diversified) | 344 | 0.072855 | 0.152918 | 0.0377492 | 0.3027 | 0.614121 | 1.03026 | 0.0692915 | 0.246063 | 0.0338 | 0.532765 | 0.0456901 | 0.289098 | 3.23946 | 12.6509 | 18.8773 | 0.710222 | 69.4402 | 1.03977 | 0.0754058 | 0.0683335 | 1.04311 | 0.0382982 | 0.765775 | 0.765775 | 0.151719 |
| Real Estate (Operations & Services) | 739 | 0.071725 | 0.182566 | 0.0366844 | 0.236162 | 0.625502 | 0.898026 | 0.0623362 | 0.263358 | 0.0404 | 0.422046 | 0.0486347 | 0.236688 | 5.67222 | 21.6078 | 30.0838 | 1.17459 | 33.157 | 0.267676 | 0.0329738 | 0.0715966 | 1.0969 | 0.0732752 | 0.320995 | 0.320995 | 0.17996 |
| Recreation | 324 | 0.0129824 | 0.104793 | 0.101016 | 0.226184 | 1.02369 | 1.10266 | 0.0730998 | 0.317719 | 0.0404 | 0.197857 | 0.0645468 | 1.11086 | 2.87625 | 15.3786 | 25.7359 | 3.37238 | 56.2803 | 0.328001 | 0.0567843 | 0.00322319 | 0.258444 | 0.0961117 | 0.598936 | 0.598936 | 0.102431 |
| Reinsurance | 38 | 0.0647587 | 0.0603183 | 0.0889265 | 0.179188 | 1.44084 | 1.48013 | 0.0929549 | 0.245019 | 0.0338 | 0.244103 | 0.0763649 | 1.66648 | 0.650555 | 10.0157 | 10.1927 | 0.935779 | 108.664 | -0.433675 | 0.00139349 | 0.00837897 | 0.402698 | 0.0732005 | 0.475092 | 0.475092 | 0.0601626 |
| Restaurant/Dining | 385 | -0.0212777 | 0.0969601 | 0.0981546 | 0.180041 | 1.01036 | 1.19222 | 0.0778106 | 0.29146 | 0.0404 | 0.241178 | 0.0662488 | 1.41045 | 3.43695 | 18.4966 | 41.9824 | 13.5015 | 99.5264 | -0.0111415 | 0.0441405 | 0.00171035 | 0.0171246 | 0.458952 | 0.612793 | 0.612793 | 0.077867 |
| Retail (Automotive) | 196 | 0.0612993 | 0.0535669 | 0.125515 | 0.233315 | 0.88668 | 1.09601 | 0.0727503 | 0.297038 | 0.0404 | 0.294722 | 0.060113 | 3.09921 | 0.862709 | 11.044 | 16.6306 | 3.63521 | 30.8638 | 0.0924248 | 0.0190083 | 0.0211519 | 0.610045 | 0.244947 | 0.257393 | 0.257393 | 0.0501683 |
| Retail (Building Supply) | 98 | 0.0519242 | 0.128699 | 0.339691 | 0.24108 | 1.10546 | 1.19964 | 0.0782013 | 0.288443 | 0.0404 | 0.138678 | 0.0714991 | 3.352 | 2.23404 | 14.0373 | 17.6516 | 15.5488 | 26.9909 | 0.0718084 | 0.0214659 | 0.0243582 | 0.495599 | 0.649741 | 0.325879 | 0.325879 | 0.12658 |
| Retail (Distributors) | 1002 | 0.0819098 | 0.0429447 | 0.0734931 | 0.237876 | 0.646488 | 0.8706 | 0.0608936 | 0.296766 | 0.0404 | 0.391985 | 0.0487335 | 2.03181 | 0.810255 | 13.1491 | 18.3662 | 1.71682 | 137.264 | 0.156573 | 0.028562 | 0.0238327 | 1.09502 | 0.126448 | 0.372944 | 0.372944 | 0.0432427 |
| Retail (General) | 204 | -0.024462 | 0.0536288 | 0.120094 | 0.280505 | 0.868122 | 1.01863 | 0.06868 | 0.246997 | 0.0338 | 0.250609 | 0.0577313 | 2.95402 | 0.981096 | 11.6421 | 19.3778 | 3.4884 | 52.2067 | -0.0123891 | 0.0261087 | 0.00381483 | 0.207831 | 0.128998 | 0.415668 | 0.415668 | 0.050253 |
| Retail (Grocery and Food) | 184 | 0.0359687 | 0.0431345 | 0.108557 | 0.239183 | 0.534664 | 0.688853 | 0.0513337 | 0.226864 | 0.0338 | 0.348593 | 0.0421511 | 3.2757 | 0.724993 | 10.5132 | 17.3862 | 2.59862 | 33.3695 | -0.0399954 | 0.0274629 | 0.0258609 | 0.878319 | 0.160677 | 0.360457 | 0.360457 | 0.0415464 |
| Retail (Online) | 353 | 0.140586 | 0.0313456 | 0.0658942 | 0.0896848 | 1.40488 | 1.43162 | 0.090403 | 0.438986 | 0.04458 | 0.0851264 | 0.0855133 | 1.70826 | 3.96031 | 26.5505 | 106.244 | 7.68737 | 84.9207 | -0.0584683 | 0.089749 | 0.0798971 | 5.43194 | 0.266766 | 0.0325225 | 0.0325225 | 0.0415422 |
| Retail (Special Lines) | 479 | 0.0126133 | 0.0612691 | 0.132793 | 0.248718 | 1.08621 | 1.20794 | 0.0786375 | 0.316351 | 0.0404 | 0.227941 | 0.0675218 | 2.59908 | 1.2014 | 10.53 | 18.5732 | 3.74507 | 36.5308 | 0.0625206 | 0.0173557 | 0.000548989 | 0.209196 | 0.157946 | 0.324424 | 0.324424 | 0.0613957 |
| Rubber& Tires | 90 | 0.0410993 | 0.102383 | 0.101234 | 0.223459 | 1.09776 | 1.2588 | 0.081313 | 0.255828 | 0.0404 | 0.281185 | 0.0668485 | 1.15776 | 1.21612 | 7.087 | 11.7046 | 1.45629 | 63.2489 | 0.20811 | 0.0575111 | 0.0292392 | 0.605102 | 0.132452 | 0.315424 | 0.315424 | 0.104309 |
| Semiconductor | 581 | 0.081461 | 0.220161 | 0.186619 | 0.115961 | 1.55309 | 1.56664 | 0.0975051 | 0.343566 | 0.0404 | 0.0665986 | 0.0930009 | 0.879542 | 6.58345 | 18.6553 | 29.3993 | 5.98937 | 139.053 | 0.153134 | 0.162757 | 0.0947567 | 0.62748 | 0.247463 | 0.313113 | 0.313113 | 0.234412 |
| Semiconductor Equip | 324 | 0.118235 | 0.232669 | 0.251172 | 0.14496 | 1.93372 | 1.91387 | 0.11577 | 0.330736 | 0.0404 | 0.039271 | 0.112396 | 1.19659 | 6.81063 | 24.3863 | 28.9732 | 8.57804 | 46.5037 | 0.270485 | 0.0645547 | 0.0505452 | 0.491182 | 0.303447 | 0.217435 | 0.217435 | 0.240596 |
| Shipbuilding & Marine | 348 | 0.0648844 | 0.235185 | 0.19977 | 0.102278 | 0.986017 | 1.12354 | 0.0741985 | 0.289009 | 0.0404 | 0.29123 | 0.0612892 | 0.95161 | 1.85331 | 6.13735 | 7.6689 | 1.53243 | 23.6857 | 0.0102003 | 0.0820397 | 0.0399024 | 0.224794 | 0.353779 | 0.140303 | 0.140303 | 0.23729 |
| Shoe | 84 | -0.0316134 | 0.118529 | 0.200493 | 0.173063 | 1.12947 | 1.13735 | 0.0749248 | 0.304897 | 0.0404 | 0.0760694 | 0.0714976 | 1.97671 | 3.77147 | 24.5238 | 31.5575 | 7.57508 | 65.0896 | 0.18057 | 0.0157488 | -0.00141563 | 0.0795486 | 0.24505 | 0.284738 | 0.284738 | 0.117676 |
| Software (Entertainment) | 317 | 0.121989 | 0.268964 | 0.2119 | 0.155617 | 1.27978 | 1.27832 | 0.0823398 | 0.413545 | 0.04458 | 0.0351798 | 0.0806028 | 0.814281 | 7.66561 | 21.0005 | 27.7675 | 6.03302 | 57.3715 | 0.0206634 | 0.0974832 | 0.0769244 | 0.442926 | 0.319732 | 0.02583 | 0.02583 | 0.285526 |
| Software (Internet) | 151 | 0.209201 | 0.0120616 | 0.0379499 | 0.136108 | 1.10845 | 1.12947 | 0.0745102 | 0.366296 | 0.0404 | 0.063411 | 0.0716797 | 1.17045 | 10.6475 | 44.8866 | NA | 9.98517 | 303.711 | 0.0273121 | 0.0675684 | 0.0964027 | 40.0463 | 0.0425424 | 0.29678 | 0.29678 | 0.0335383 |
| Software (System & Application) | 1603 | 0.145828 | 0.203194 | 0.213767 | 0.125454 | 1.20084 | 1.2143 | 0.0789724 | 0.395922 | 0.0404 | 0.0543537 | 0.0763036 | 1.03789 | 11.0953 | 33.0668 | 47.3259 | 11.5321 | 167.001 | 0.140826 | 0.0607151 | 0.154688 | 0.936699 | 0.204677 | 0.35856 | 0.35856 | 0.222749 |
| Steel | 709 | 0.129882 | 0.149805 | 0.20855 | 0.20453 | 1.06758 | 1.25333 | 0.0810253 | 0.318656 | 0.0404 | 0.30823 | 0.0652583 | 1.6224 | 0.797187 | 4.12328 | 5.22686 | 1.18912 | 48.9176 | 0.136718 | 0.0494315 | 0.031576 | 0.496506 | 0.255746 | 0.3029 | 0.3029 | 0.151711 |
| Telecom (Wireless) | 101 | 0.00273099 | 0.140463 | 0.088252 | 0.295779 | 0.717593 | 1.00249 | 0.067831 | 0.251219 | 0.0404 | 0.426244 | 0.0516511 | 0.734846 | 2.10735 | 6.60109 | 15.1736 | 1.34905 | 27.2207 | -0.124414 | 0.161509 | -0.00488487 | -0.0574454 | 0.139912 | 0.398088 | 0.398088 | 0.141092 |
| Telecom. Equipment | 465 | 0.034432 | 0.112099 | 0.14256 | 0.29824 | 1.16732 | 1.17127 | 0.0767088 | 0.325497 | 0.0404 | 0.0956743 | 0.0722277 | 1.27989 | 2.9215 | 17.3721 | 24.5563 | 4.22865 | 87.0286 | 0.228112 | 0.0332362 | 0.0558855 | 0.85861 | 0.113736 | 0.593717 | 0.593717 | 0.121033 |
| Telecom. Services | 296 | 0.080951 | 0.15783 | 0.10602 | 0.207287 | 0.576438 | 0.855855 | 0.060118 | 0.28129 | 0.0404 | 0.435809 | 0.0469364 | 0.783956 | 2.17805 | 6.86862 | 13.7975 | 1.47542 | 90.4908 | -0.00385245 | 0.14745 | -0.000602835 | -0.0463597 | 0.128575 | 0.572344 | 0.572344 | 0.157134 |
| Tobacco | 55 | 0.0304071 | 0.34453 | 0.224955 | 0.235685 | 0.728929 | 0.854793 | 0.0600621 | 0.272447 | 0.0404 | 0.230762 | 0.0530953 | 0.777115 | 3.67099 | 8.48051 | 10.6231 | 3.52763 | 21.3062 | 0.168485 | 0.0232466 | -0.0395736 | -0.131774 | 0.26171 | 0.86302 | 0.86302 | 0.344775 |
| Transportation | 295 | 0.0851744 | 0.0724579 | 0.112906 | 0.236334 | 0.852938 | 1.01443 | 0.068459 | 0.281537 | 0.0404 | 0.285641 | 0.0574369 | 1.85432 | 1.34009 | 11.1233 | 17.786 | 2.51263 | 54.7542 | 0.0444817 | 0.0456417 | 0.0124827 | 0.565492 | 0.178997 | 0.370261 | 0.370261 | 0.073499 |
| Transportation (Railroads) | 51 | -0.000599333 | 0.154036 | 0.0452545 | 0.239944 | 0.667512 | 0.825737 | 0.0585338 | 0.178706 | 0.0338 | 0.281035 | 0.0491073 | 0.361181 | 5.26084 | 17.8659 | 32.8013 | 2.65326 | 42.9159 | 0.0642496 | 0.17324 | 0.120379 | 1.11551 | 0.062059 | 0.694534 | 0.694534 | 0.156239 |
| Trucking | 232 | 0.0374525 | 0.0557924 | 0.0576998 | 0.249629 | 0.920809 | 1.1302 | 0.0745485 | 0.282637 | 0.0404 | 0.303008 | 0.0610111 | 1.19625 | 1.84693 | 9.76634 | 24.2774 | 2.90897 | 71.564 | 0.0703221 | 0.0792561 | 0.0412747 | 1.59624 | 0.0821524 | 0.225428 | 0.225428 | 0.0577875 |
| Utility (General) | 54 | 0.033781 | 0.123683 | 0.0703052 | 0.208623 | 0.521651 | 0.803648 | 0.0573719 | 0.185429 | 0.0338 | 0.453398 | 0.0426908 | 0.684447 | 2.4316 | 11.0517 | 19.6451 | 1.70814 | 19.6086 | -0.195895 | 0.158708 | 0.0930122 | 1.03188 | 0.0952751 | 0.671093 | 0.671093 | 0.123275 |
| Utility (Water) | 104 | 0.110979 | 0.250668 | 0.072912 | 0.298356 | 0.514465 | 0.728959 | 0.0534433 | 0.261782 | 0.0404 | 0.405354 | 0.0438885 | 0.344222 | 4.94094 | 13.1817 | 19.5486 | 1.74959 | 72.5506 | 0.020003 | 0.234664 | 0.141866 | 1.2542 | 0.132174 | 0.839281 | 0.386005 | 0.25035 |

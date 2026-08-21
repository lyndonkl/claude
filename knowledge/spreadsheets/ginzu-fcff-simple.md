### fcffsimpleginzu.xlsx

**Purpose:** Damodaran's flagship all-purpose FCFF (free cash flow to firm) DCF valuation model — the "Ginzu" spreadsheet. It values any non-financial company from ~15 base-year inputs plus a handful of forecast "value driver" assumptions (revenue growth, target operating margin, sales-to-capital ratio). It builds a 10-year FCFF forecast with automatic fade of growth, margin, tax rate and cost of capital toward stable-growth values. It then adds a terminal value, adjusts for probability of failure, and backs out equity value per share. Built-in helper modules: cost-of-capital builder (bottom-up betas, multi-region ERP, synthetic/actual debt rating), R&D capitalizer, operating-lease-to-debt converter, employee-option (dilution-adjusted Black-Scholes) valuer, trailing-12-month input builder, and reference data updated January 2022 (industry averages, country ERPs, rating spreads). Damodaran uses this as his default company valuation model; the copy in the file is loaded with a worked valuation of SK Innovation (Korea), valuation date 2022-01-01.

**IMPORTANT — circular references:** the workbook requires Excel iterative calculation ("check the iteration box"). Two deliberate circularities exist. (1) Synthetic-rating cost of debt: lease debt PV uses pre-tax cost of debt; in synthetic-rating mode that depends on interest coverage, which includes imputed lease interest. (2) Option value: the dilution-adjusted stock price uses the option value being computed. A Python port must solve these by fixed-point iteration (or algebra).

Sheets: `Input sheet`, `Valuation output`, `Stories to Numbers`, `Diagnostics`, `Summary Sheet`, `Option value`, `Cost of capital worksheet`, `R& D converter`, `Operating lease converter`, `Country equity risk premiums`, `Synthetic rating`, `Industry Averages(US)`, `Industry Average Beta (Global)`, `Trailing 12 month`, `Answer keys`. All have content; none skipped.

---

## Inputs

### Input sheet (the master input page)

Company / base year (units must be internally consistent; per-share outputs are in (currency ÷ share-count units)):

| Label | Cell | Example value (SK Innovation) |
|---|---|---|
| Date of valuation | B1 | 2022-01-01 |
| Company name | B2 | SK Innovation |
| Country of incorporation | B5 | Korea |
| Industry (US) | B6 | Software (System & Application) |
| Industry (Global) | B7 | Software (System & Application) |
| Revenues — this year / last year | B8 / C8 | 32,357,222 / 49,306,938 |
| Operating income (EBIT) — this year / last year | B9 / C9 | −250,829 / 1,113,646 |
| Years since last 10K (for D8/D9 columns) | D8, D9 | 1.25 |
| Interest expense — this / last | B10 / C10 | 351,778 / 349,904 |
| Book value of equity — this / last | B11 / C11 | 14,405,108 / 17,468,081 |
| Book value of debt — this / last | B12 / C12 | 16,715,192 / 14,751,920 |
| Capitalize R&D? (Yes/No) | B13 | Yes |
| Have operating lease commitments? (Yes/No) | B14 | No |
| Cash and marketable securities | B15 | 6,699,463 |
| Cross holdings & non-operating assets | B16 | 0 |
| Minority interests | B17 | 0 |
| Number of shares outstanding | B18 | 83.6 |
| Current stock price | B19 | 273,500 |
| Effective tax rate | B20 | 0.25 |
| Marginal tax rate | B21 | 0.25 |

Value drivers:

| Label | Cell | Example |
|---|---|---|
| Revenue growth rate for next year | B23 | 0.50 |
| Operating margin for next year | B24 | 0.03 |
| CAGR revenue growth, years 2–5 | B25 | 0.05 |
| Target pre-tax operating margin (year 10) | B26 | 0.075 |
| Year of convergence (for margin) | B27 | 10 |
| Sales-to-capital ratio, next year | B28 | 10 |
| Sales-to-capital ratio, years 2–5 | B29 | 5 |
| Sales-to-capital ratio, years 6–10 | B30 | 1.5 |

Market numbers:

| Label | Cell | Example |
|---|---|---|
| Riskfree rate | B32 | 0.0169 |
| Initial cost of capital | B33 | 0.07312245558 — formula `='Cost of capital worksheet'!E50` (can be hard-typed instead) |

Other inputs (employee options):

| Label | Cell | Example |
|---|---|---|
| Employee options outstanding? (Yes/No) | B35 | No |
| Number of options outstanding | B36 | 7.72 |
| Average strike price | B37 | 1.29 |
| Average maturity | B38 | 7 |
| Std deviation on stock price | B39 | 0.45 |

Default-assumption overrides (each is a Yes/No flag + a conditional value):

| Assumption | Override flag | Value cell | Example |
|---|---|---|---|
| Stable cost of capital after yr 10 = rf + mature-market ERP (label says "riskfree + 4.5%"; the formula actually uses rf + mature ERP of 4.24%) | B43 = No | B44 = 0.075 | not used |
| Stable-period ROC = cost of capital (competitive advantages fade) | B46 = No | B47 = 0.10 | not used |
| Probability of failure (default 0) | B49 = Yes | B50 = 0.12 | used |
| Distress proceeds tied to "B" (book capital) or "V" (estimated fair value) | B51 | "V" | |
| Distress proceeds as % of book/fair value | B52 | 0.5 | |
| Effective tax → marginal tax by terminal year (override keeps effective forever) | B54 = No | — | |
| NOL carried into year 1 (default 0) | B56 = Yes | B57 = 731.4 (`=474.8+256.6`) | |
| Riskfree rate changes after year 10 | B59 = Yes | B60 = 0.02 | |
| Growth in perpetuity ≠ riskfree rate | B62 = No | B63 = −0.05 | not used |
| Trapped cash / cash discount | B65 = No | B66 = 140,000; B67 = 0.15 (foreign tax rate / discount) | not used |

Yes/No answers, ERP-approach choices, beta approaches, rating symbols etc. come from dropdowns whose allowed values are on the `Answer keys` sheet (see Reference data).

### Cost of capital worksheet inputs

| Label | Cell | Example |
|---|---|---|
| Shares outstanding | B6 | `='Input sheet'!B18` |
| Market price/share | B7 | `='Input sheet'!B19` |
| Approach for estimating beta | B9 | "Multibusiness(Global)" — allowed: Direct input / Single Business(US) / Single Business(Global) / Multibusiness(US) / Multibusiness(Global) |
| Direct-input levered beta | B10 | 1.2 (unused here) |
| Riskfree rate | B12 | `='Input sheet'!B32` |
| ERP approach | B13 | "Operating regions" — allowed: Will input / Country of incorporation / Operating countries / Operating regions |
| Direct-input ERP | B14 | 0.06 (unused) |
| Book value of straight debt | B18 | `='Input sheet'!B12` |
| Interest expense on debt | B19 | `='Input sheet'!B10` |
| Average maturity of debt | B20 | 3 |
| Approach for pre-tax cost of debt | B21 | "Actual rating" — allowed: Direct input / Synthetic rating / Actual rating |
| Direct-input pre-tax cost of debt | B22 | 0.04 (unused) |
| Actual rating (if that approach) | B23 | "Baa2/BBB" |
| Type of company for synthetic rating (1=large manufacturing, 2=small/risky, 3=financial service) | B24 | 2 |
| Marginal tax rate | B26 | `='Input sheet'!B21` |
| Convertible debt: book value / interest expense / maturity / market value | B28–B31 | 0/0/0/0 |
| Preferred: # shares / price / annual dividend per share | B36–B38 | 0 / 70 / 5 |

ERP calculator input blocks (user fills country/region/business names + revenue weights):
- Operating **countries** ERP: rows G5:H17 (country name, revenues). Example: United States 15,000; Australia 6,000; "Rest of the World" 7,782 with hand-entered ERP 0.0618. The last two rows of each block are free-input rows where the user may type an ERP directly.
- Operating **regions** ERP: rows G21:H31 — region names auto-linked to the regional ERP table; user enters revenues. Example: Asia 27,899; North America 4,355; Western Europe 5,389; plus a free-input row "South Korea", revenue 66,423, hand-entered ERP 0.052.
- Multibusiness (US) bottom-up beta: G36:H47 (business name from US industry list, revenues). Example: Computers/Peripherals 25,484; Entertainment 18,805; Computer Services 37,190; Telecom. Equipment 166,699.
- Multibusiness (Global) bottom-up beta: G52:H63. Example: Oil/Gas (Production and Exploration) 81,363; Chemical (Basic) 14,862; Chemical (Specialty) 4,608; Electronics (General) 2,010; Metals & Mining 59,269.

### R& D converter inputs

| Label | Cell | Example |
|---|---|---|
| Amortization life (years, max 10) | F6 | 5 |
| Current year's R&D expense | F7 | 251,563 |
| Past R&D expenses, years −1 … −(life−1) | B11:B20 | −1: 253,611; −2: 227,441; −3: 233,578; −4: 195,693; −5: 145,318 |

(Year labels A12:A20 auto-fill: `A12 =IF((0-A11)<$F$6,IF(A11>-1,,A11-1),)` — i.e. keep decrementing while |year| < life.)

### Operating lease converter inputs

| Label | Cell | Example |
|---|---|---|
| Operating lease expense in current year | E4 | 295 |
| Lease commitments years 1–5 | B7:B11 | 287, 235, 194, 151, 98 |
| Commitment year 6 and beyond (lump sum) | B12 | 605 |

(Pre-tax cost of debt C15 auto-links to `'Cost of capital worksheet'!B25`.)

### Option value inputs

All auto-linked from Input sheet: stock price D2, strike D3, expiration D4, std dev D5, T-bond rate D7, # options D8, # shares D9. Dividend yield D6 = 0 is typed on this sheet.

### Trailing 12 month (standalone helper, not linked into the model)

Inputs: Last 10K value (col B), first-X-months of last year (col C), first-X-months of current year (col D) for revenues, EBIT, interest, etc. Output E = B − C + D (trailing-12-month figure), which the user copies into the Input sheet by hand. Example rows in the file are Amazon-like numbers (revenues 15,794.34 / 7,608.13 / 9,444.11 → TTM 17,630.32). It also computes effective tax rates as taxes/pre-tax-income ratios typed directly (e.g. `B14 ==15885/61372`), and holds lease-commitment figures to copy into the lease converter.

---

## Logic

### Step 0 — helper modules feeding the base year

**R&D capitalization** (used because Input!B13 = "Yes"):
- Unamortized fraction of R&D from year −k (k = 1..life−1): `(life − k)/life`; current year's expense counts fully (factor 1).
- Value of research asset `D35 = Σ (expense_k × unamortized fraction_k)` over current + past years = **723,486.2**.
- Amortization this year `D37 = Σ_{k≥1} (expense_k / life)` = 211,128.2.
- Adjustment to operating income `D39 = current R&D − amortization = F7 − D37` = **40,434.8** (add to EBIT).
- Tax effect `D40 = D39 × marginal tax` = 10,108.7 — computed but **not used** anywhere else.

**Operating lease conversion** (module present; Input!B14 = "No" so it does not feed this valuation):
- Pre-tax cost of debt `C15 ='Cost of capital worksheet'!B25` (source of circularity 1).
- Years embedded in the year-6+ lump: `D18 =IF(B12>0,ROUND(B12/AVERAGE(B7:B11),0),0)` → 3.
- PV of each commitment year t=1..5: `C22 =B22/(1+$C$15)^A22` etc.
- Year 6+: annuity of `B27 =IF(B12>0,IF(D18>0,B12/D18,B12),0)` per year for D18 years, discounted as `C27 =IF(D18>0,(B27*(1-(1+C15)^(-D18))/C15)/(1+$C$15)^5,B27/(1+C15)^6)`.
- Debt value of leases `C28 = ΣC22:C27` = 1,373.17.
- Straight-line depreciation on lease asset `F31 = C28/(5+D18)` = 171.65.
- Adjustment to operating earnings `F32 = E4 − F31` = 123.35 (add to pre-tax EBIT).
- Adjustment to total debt `F33 = C28`.

**Adjusted base-year numbers** (Valuation output col B):
- `B5 (EBIT) =IF(Input!B14="Yes", IF(Input!B13="Yes", Input!B9 + Lease!F32 + RnD!D39, Input!B9 + Lease!F32), IF(Input!B13="Yes", Input!B9 + RnD!D39, Input!B9))` → −250,829 + 40,434.8 = **−210,394.2**.
- Invested capital `B39 =` BV equity + BV debt − cash (+ lease debt F33 if leases) (+ research asset D35 if R&D): `=IF(Input!B14="Yes", IF(Input!B13="Yes", B11+B12-B15+Lease!F33+RnD!D35, B11+B12-B15+Lease!F33), IF(Input!B13="Yes", B11+B12-B15+RnD!D35, B11+B12-B15))` → 14,405,108 + 16,715,192 − 6,699,463 + 723,486.2 = **25,144,323.2**.

### Step 1 — cost of capital (Cost of capital worksheet)

**Unlevered beta** (B11), by approach B9:
`=IF(B9="Single Business(US)", VLOOKUP(Input!B6, 'Industry Averages(US)'!A2:G95, 7), IF(B9="Multibusiness(US)", K48, IF(B9="Single Business(Global)", VLOOKUP(Input!B7, 'Industry Average Beta (Global)'!A2:G95, 7), K64)))`
- Multibusiness bottom-up (US block shown; Global identical with its own table): for each business i, `EV/Sales_i = VLOOKUP(name, industry table, col 15)`; `EstValue_i = Revenues_i × EV/Sales_i`; `UnlevBeta_i = VLOOKUP(name, col 7)`; company unlevered beta `K48 (or K64) = Σ UnlevBeta_i × EstValue_i / Σ EstValue_i`.
- Example (Global): K64 = **1.14316151**.
- If B9 = "Direct Input", B11 is bypassed later (C45 uses B10 directly).

**ERP** (B15):
`=IF(B13="Will Input", B14, IF(B13="Country of Incorporation", VLOOKUP(Input!B5, 'Country equity risk premiums'!A5:E181, 4), IF(B13="Operating regions", K32, K18)))`
- Operating-countries calculator: `I_i =IF(H_i=0,0,VLOOKUP(country, 'Country equity risk premiums'!$A$5:$D$181, 4))` (or hand-typed in the two free rows); weight `J_i = H_i/ΣH`; `K18 = Σ I_i×J_i`.
- Operating-regions calculator: region ERPs pre-linked from the regional table rows 185–193 (`I21 ='Country equity risk premiums'!B185` etc.); weight by revenues; `K32 = Σ I×J` = **0.05174663** in the example (weights: Asia 0.2681, North America 0.0418, Western Europe 0.0518, South Korea free-row 0.6383 @ 0.052).

**Pre-tax cost of debt** (B25):
`=IF(B21="Direct Input", B22, IF(B21="Synthetic Rating", 'Synthetic rating'!D13, B12 + VLOOKUP(B23, 'Synthetic rating'!G39:H53, 2)))`
- Actual-rating branch: riskfree + spread looked up from the rating→spread list (G39:H53). NOTE: that list is NOT sorted and the VLOOKUP is approximate-match; in Excel it happens to resolve; a Python port should use exact match on the rating string. Example: 0.0169 + 0.01591066 = **0.03281066**.
- Synthetic-rating branch: see Synthetic rating sheet below.

**Market value of debt** (converts book debt to market using cost of debt as YTM over average maturity):
`C41 = B19*(1-(1+B25)^(-B20))/B25 + B18/(1+B25)^B20` → 16,161,914.12 (interest expense as an annuity + book value as balloon).
Convertible: straight-debt portion `C42 = B29*(1-(1+B25)^(-B30))/B25 + B28/(1+B25)^B30`; equity portion of convertible `C44 = B31 − C42`. Lease debt `C43 = B33 =IF(Input!B14="Yes", Lease!F33, 0)`.

**Capital structure & WACC:**
- Market equity `B48 = B6×B7` = 22,864,600. Debt `C48 = C41+C42+C43` = 16,161,914.12. Preferred `D48 = B36×B37` = 0. Total `E48 = ΣB48:D48`.
- Levered beta `C45 =IF(B9="Direct Input", B10, B11*(1+(1-B26)*(C48/B48)))` → 1.14316151 × (1 + 0.75×0.70687...) = **1.74919699**.
- Weights `B49..D49 = component/E48` → equity 0.58587349, debt 0.41412651, preferred 0.
- Cost of equity `B50 = B12 + C45×B15` → 0.0169 + 1.74919699×0.05174663 = **0.10741506**.
- After-tax cost of debt `C50 = B25×(1-B26)` → 0.02460799.
- Cost of preferred `D50 = B38/B37` → 0.07142857 (weight 0 here).
- **WACC `E50 = B49×B50 + C49×C50 + D49×D50` = 0.07312245558** → feeds Input!B33.

### Step 2 — synthetic rating (Synthetic rating sheet)

- EBIT for coverage `F5 =IF(Input!B14="Yes", Input!B9 + Lease!F32, Input!B9)` → −250,829 (lease-adjusted but NOT R&D-adjusted).
- Interest for coverage `F6 =IF(Input!B14="Yes", CoC!B19 + Lease!C28×Lease!C15, CoC!B19)` → 351,778 (adds imputed lease interest = lease debt × pre-tax cost of debt — circular with B25 when synthetic mode is on).
- Interest coverage ratio `D9 =IF(F6=0, 1000000, IF(F5<0, -100000, F5/F6))` → **−100000** (negative EBIT ⇒ sentinel, maps to D rating).
- Rating `D10 =IF(C4=1, VLOOKUP(D9, A19:D33, 3), IF(C4=2, VLOOKUP(D9, A38:D52, 3), VLOOKUP(D9, F19:I33, 3)))` (C4 = CoC!B24; type 1 = large manufacturing table, type 2 = small/risky table, type 3 = financial service — **the F19:I33 financial-service table is EMPTY in this workbook, so type 3 would error**). Approximate-match VLOOKUP on the ascending "greater than" column = the intended range lookup.
- Company default spread `D11` = same lookup, column 4 → 0.14335607 (D2/D).
- Country default spread `D12 =VLOOKUP(Input!B5, 'Country equity risk premiums'!A5:C181, 3)` → Korea 0.00422187.
- **Synthetic cost of debt `D13 = F7 + D11 + D12`** (rf + company spread + country spread) → 0.16447795 (not used here since actual rating chosen).

### Step 3 — 10-year forecast (Valuation output, columns C..L = years 1..10, M = terminal)

Growth (row 2):
- `C2 = Input!B23` (yr 1); `D2 = Input!B25`; `E2=F2=G2` = same (yrs 2–5).
- Years 6–10 fade linearly to terminal growth: `H2 = G2-((G2-$M$2)/5)`, `I2 = G2-((G2-$M$2)/5)*2`, … `L2 = G2-((G2-$M$2)/5)*5`.
- Terminal growth `M2 =IF(Input!B62="Yes", Input!B63, IF(Input!B59="Yes", Input!B60, Input!B32))` (perpetuity-growth override, else post-yr-10 riskfree override, else riskfree) → 0.02.

Revenues (row 3): `B3 = Input!B8`; `C3 = B3*(1+C2)`; … `M3 = L3*(1+M2)`.

EBIT margin (row 4):
- `B4 = B5/B3` (adjusted base margin); `C4 = Input!B24`.
- Years 2–5: `D4 =IF(D1>Input!$B$27, Input!$B$26, Input!$B$26-((Input!$B$26-$C$4)/Input!$B$27)*(Input!$B$27-D1))` — linear convergence from **year-1 margin C4** to target B26 by year B27.
- Years 6–10: same formula **but anchored on the base-year margin $B$4** instead of $C$4: `H4 =IF(H1>Input!$B$27, Input!$B$26, Input!$B$26-((Input!$B$26-$B$4)/Input!$B$27)*(Input!$B$27-H1))`. This is a quirk of the sheet (it produces a kink: yr5 margin 0.0525 → yr6 0.04240) — reproduce verbatim for fidelity.
- `M4 = L4` (target reached if B27 ≤ 10).

EBIT (row 5): `C5 = C4*C3` etc. `B5` = adjusted base EBIT (Step 0). `N5 = M5-B5` (informational).

Tax rate (row 6): `B6 = Input!B20` (effective); constant through year 5 (`C6=B6 … G6=F6`); years 6–10 ramp to terminal: `H6 = G6+($M$6-$G$6)/5` (each cell = previous + 1/5 of the year5→terminal gap); `M6 =IF(Input!B54="Yes", Input!B20, Input!B21)`.

NOL (row 10): `B10 =IF(Input!B56="Yes", Input!B57, 0)`; then `C10 =IF(C5<0, B10-C5, IF(B10>C5, B10-C5, 0))` — losses add to the carryforward; profits burn it down; hits 0 once EBIT exceeds the carryforward.

EBIT(1−t) (row 7): `B7 =IF(B5>0, B5*(1-B6), B5)`;
`C7 =IF(C5>0, IF(C5<B10, C5, C5-(C5-B10)*C6), C5)` — no tax while EBIT ≤ prior-year NOL; only the excess over prior NOL is taxed. Terminal: `M7 = M5*(1-M6)` (no NOL shield).

Sales-to-capital (row 38): `C38 = Input!B28`; `D38 = Input!B29`; `E38=F38` = same; `G38 = Input!B30`; `H38..L38` = same.

Reinvestment (row 8): `C8 =IF(C3>B3, (C3-B3)/C38, 0)` (year 1 floors at 0 if revenue shrinks); `D8 = (D3-C3)/D38` … `L8 = (L3-K3)/L38` (years 2–10 have NO floor — negative reinvestment possible if revenues decline).
Terminal: `M8 =IF(M2>0, (M2/M40)*M7, 0)` — reinvestment rate = g/ROC applied to terminal EBIT(1−t); zero if terminal growth ≤ 0.

FCFF (row 9): `C9 = C7 - C8` (each year); `M9 = M7 - M8`.

Invested capital (row 39): `B39` from Step 0; `C39 = B39 + C8`; cumulative through `L39`.
ROIC (row 40): `B40 = B7/B39` … `L40 = L7/L39`. Terminal ROC `M40 =IF(Input!B46="Yes", Input!B47, L12)` (default: terminal ROC = terminal cost of capital).

Cost of capital (row 12): `C12 = Input!B33`; constant through G12 (yrs 1–5); years 6–10 fade linearly: `H12 = G12-($G$12-$M$12)/5` … `L12 = K12-($G$12-$M$12)/5`.
Terminal `M12 =IF(Input!B43="Yes", Input!B44, IF(Input!B59="Yes", Input!B60 + 'Country equity risk premiums'!B1, Input!B32 + 'Country equity risk premiums'!B1))` — i.e. (possibly-updated) riskfree + mature-market ERP (B1 = 0.0424). Example: 0.02 + 0.0424 = **0.0624**.

Discounting (rows 13–14): cumulative discount factor `C13 = 1/(1+C12)`; `D13 = C13*(1/(1+D12))`; … `L13`. `PV(FCFF)_t = FCFF_t × CDF_t` (row 14).

### Step 4 — terminal value, failure risk, equity bridge (Valuation output col B)

- `B16 = M9` (terminal FCFF); `B17 = M12`; **Terminal value `B18 = B16/(B17-M2)`**.
- `B19 = B18 × L13` (PV of TV, discounted with the year-10 cumulative factor).
- `B20 = SUM(C14:L14)`; `B21 = B19 + B20` (sum of PV).
- Probability of failure `B22 =IF(Input!B49="Yes", Input!B50, 0)`.
- Proceeds if firm fails `B23 =IF(Input!B51="B", (Input!B11+Input!B12)×Input!B52, B21×Input!B52)` (book capital × pct, or going-concern value × pct).
- **Value of operating assets `B24 = B21×(1-B22) + B23×B22`**.
- Debt `B25 =IF(Input!B14="Yes", Input!B12 + Lease!C28, Input!B12)` (book debt + lease debt; note: book here, market in WACC).
- Minority interests `B26 = Input!B17`.
- Cash `B27 =IF(Input!B65="YES", Input!B15 - Input!B66×(Input!B21-Input!B67), Input!B15)` — trapped-cash haircut = trapped amount × (marginal tax − foreign tax). (String compare is case-insensitive in Excel; a port should treat "Yes"/"YES" alike.)
- Non-operating assets `B28 = Input!B16`.
- **Value of equity `B29 = B24 - B25 - B26 + B27 + B28`**.
- Value of options `B30 =IF(Input!B35="No", 0, 'Option value'!D27)`.
- Equity in common stock `B31 = B29 - B30`; shares `B32 = Input!B18`; **value/share `B33 = B31/B32`**; price `B34 = Input!B19`; price as % of value `B35 = B34/B33`.

### Step 5 — employee options (Option value sheet; dilution-adjusted Black–Scholes, iterative)

- S = D2, K = D3, T = D4, σ = D5, q = D6, r = D7, n_options = D8, n_shares = D9. Variance `F16 = D5^2`; div-adjusted rate `F18 = F15 - F17` (F15 = T-bond rate, F17 = q; F18 is the drift used in d1).
- Adjusted S `C15 = (C13×F14 + C26×F13)/(F14 + F13)` — value-weighted with the option value C26 itself (circular; iterate).
- `d1 = (LN(C15/C16) + (F18 + F16/2)×T) / (σ×√T)`; `d2 = d1 - σ×√T`; N() = standard normal CDF (NORMSDIST).
- Value per option `C26 = e^(−q·T)·C15·N(d1) − K·e^(−F15·T)·N(d2)` (strike discounted at the raw T-bond rate F15).
- Value of all options `D27 = C26 × D8`. Example: with S = 273,500 and K = 1.29 the options are ultra-deep in the money: value/option ≈ 273,498.75, D27 ≈ 2,111,410.34 — but B30 = 0 because Input!B35 = "No".

### Reporting sheets (derived only — no new logic)

- **Stories to Numbers**: narrative text (A3), an assumptions table, the year-by-year cash-flow table and the value bridge — every number cell links to Valuation output / Input sheet. Value bridge: adjustment for distress `D33 = D32 − Valuation!B24`; value of equity `D36 = D32 - D33 - D34 + D35`.
- **Summary Sheet**: three re-derivations — (income: taxes `G = E − H`), (reinvestment: `E = ΔRevenue / SalesToCapital`, capital invested cumulates, implied ROC `H = B/G`), (discounting: cumulated cost of capital `C41 = C40*(1+B41)` starting `C40 = 1+B40`; `F49 = (FCFF10 + TV)/C49`; `F50 = ΣF40:F49` = value of operating assets, matches B21).
- **Diagnostics**: marginal ROIC over 10 yrs `B6 = (ΔEBIT(1−t) over 10y)/(Δ invested capital over 10y)` = 0.45973660; average compounded WACC `B8 = (1/L13)^(1/10) − 1` = 0.06989872; value/price `B9 = B33/B34` = 1.18278862 with advisory text `B10 =IF(B9="NA","Value is negative…",IF(B9>2,"Value seems high…",IF(B9<0.5,"Value seems low…"," ")))`, plus a static table of which input to nudge.
- **Input sheet comparison block (E19:K33)**: company vs industry — e.g. `I22 =IF(C8>0,(B8/C8)^(1/D8)-1,"NA")` (annualized recent revenue growth using "years since last 10K"), `J22 =VLOOKUP(B6,'Industry Averages(US)'!A2:S95,3)`, `I24 = B8/Valuation!B39` (sales/capital), `I25 = Valuation!B7/Valuation!B39` (ROIC), industry std-dev col 10, industry cost of capital col 13, industry sales/capital col 14. QUIRK: the "Industry (Global data)" cells K26 and K27 look up **B6 (the US industry name)** in the Global table, not B7 — verbatim: `K26 =VLOOKUP(B6,'Industry Average Beta (Global)'!A2:Z95,10)`, `K27 =VLOOKUP(B6,'Industry Average Beta (Global)'!A2:Z95,13)`.

---

## Reference data

### Synthetic rating: interest coverage → rating → default spread

Table 1 — **large manufacturing firms** (Cost-of-capital "type of company" = 1), range A19:D33. Lookup: coverage ratio ≥ col1 and ≤ col2.

| > | ≤ | Rating | Spread |
|---|---|---|---|
| -100000 | 0.199999 | D2/D | 0.14335607034015696 |
| 0.2 | 0.649999 | C2/C | 0.10755403832538094 |
| 0.65 | 0.799999 | Ca2/CC | 0.088 |
| 0.8 | 1.249999 | Caa/CCC | 0.0777645323482633 |
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

Table 2 — **smaller and riskier firms** (type = 2), range A38:D52:

| > | ≤ | Rating | Spread |
|---|---|---|---|
| -100000 | 0.499999 | D2/D | 0.14335607034015696 |
| 0.5 | 0.799999 | C2/C | 0.10755403832538094 |
| 0.8 | 1.249999 | Ca2/CC | 0.088 |
| 1.25 | 1.499999 | Caa/CCC | 0.0777645323482633 |
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

(Type = 3, financial-service firms, points at F19:I33 which is **empty** in this workbook — a port should raise an error or supply its own table for type 3.)

Rating → spread list (for the "Actual rating" cost-of-debt branch), range G39:H53 — order as in the sheet (unsorted; use exact match):

| Rating | Spread |
|---|---|
| A1/A+ | 0.010307640869863355 |
| A2/A | 0.011379635520329143 |
| A3/A- | 0.012863935805589465 |
| Aa2/AA | 0.008246112695890684 |
| Aaa/AAA | 0.006660321792834782 |
| B1/B+ | 0.03147266537958828 |
| B2/B | 0.03776719845550594 |
| B3/B- | 0.046159909223396155 |
| Ba1/BB+ | 0.019341413179589748 |
| Ba2/BB | 0.02152617442092565 |
| Baa2/BBB | 0.01591065804294902 |
| C2/C | 0.10755403832538094 |
| Ca2/CC | 0.088 |
| Caa/CCC | 0.0777645323482633 |
| D2/D | 0.14335607034015696 |

Cumulative default probabilities by rating and horizon (years 1–10), J17:T24 — informational only (no formula references it; useful for choosing Input!B50):

| Rating | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| AAA | 0 | 0.0003 | 0.0013 | 0.0024 | 0.0035 | 0.0045 | 0.0051 | 0.0059 | 0.0064 | 0.0070 |
| AA | 0.0002 | 0.0006 | 0.0012 | 0.0021 | 0.0031 | 0.0042 | 0.0050 | 0.0058 | 0.0065 | 0.0072 |
| A | 0.0005 | 0.0014 | 0.0023 | 0.0035 | 0.0047 | 0.0062 | 0.0079 | 0.0093 | 0.0108 | 0.0124 |
| BBB | 0.0016 | 0.0045 | 0.0078 | 0.0117 | 0.0158 | 0.0198 | 0.0233 | 0.0267 | 0.0300 | 0.0332 |
| BB | 0.0061 | 0.0192 | 0.0348 | 0.0505 | 0.0652 | 0.0785 | 0.0901 | 0.1004 | 0.1097 | 0.1178 |
| B | 0.0333 | 0.0771 | 0.1155 | 0.1458 | 0.1693 | 0.1883 | 0.2036 | 0.2160 | 0.2270 | 0.2374 |
| CCC/C | 0.2708 | 0.3664 | 0.4141 | 0.4410 | 0.4619 | 0.4709 | 0.4826 | 0.4905 | 0.4976 | 0.5038 |

### Answer keys (allowed dropdown values)

| List | Values |
|---|---|
| Yes/No | Yes, No |
| Book or Market Value (distress proceeds base) | B, V |
| ERP choices | Will input, Country of incorporation, Operating countries, Operating regions |
| Cost of debt | Direct input, Synthetic rating, Actual rating |
| Synthetic rating firm type | 1, 2 |
| Beta | Direct input, Single Business(US), Single Business(Global), Multibusiness(US), Multibusiness(Global) |
| Ratings | Aaa/AAA, Aa2/AA, A1/A+, A2/A, A3/A-, Baa2/BBB, Ba1/BB+, Ba2/BB, B1/B+, B2/B, B3/B-, C2/C, Ca2/CC, Caa/CCC, D2/D |

### Country equity risk premiums (sheet 'Country equity risk premiums', updated January 1, 2022)

Header cell B1 = **0.0424 = mature-market ERP**; every country ERP (col D) = `$B$1 + CRP` (col E). Rows 5–181. Column C = adjusted default spread (used as the country default spread in the synthetic-rating cost of debt); column E = country risk premium; column F = corporate tax rate. Where the Moody's rating column shows a number (e.g. 62.25) the country is unrated and the number is a composite risk score.

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

Regional aggregates (rows 185–193; row 194 = Global). These feed the Operating-regions ERP calculator. The last-listed region rows in the calculator (G30, G31) are free-input rows:


| Region | Weighted Avg ERP | Default Spread | Tax rate | CRP |
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

### Industry Averages (US) — sheet 'Industry Averages(US)', rows 2–95

94 industries. Full column list (A..AA = cols 1..27): Industry Name, Number of firms, Annual Average Revenue growth - Last 5 years, Pre-tax Operating Margin (Unadjusted), After-tax ROC, Average effective tax rate, Unlevered Beta, Equity (Levered) Beta, Cost of equity, Std deviation in stock prices, Pre-tax cost of debt, Market Debt/Capital, Cost of capital, Sales/Capital, EV/Sales, EV/EBITDA, EV/EBIT, Price/Book, Trailing PE, Non-cash WC as % of Revenues, Cap Ex as % of Revenues, Net Cap Ex as % of Revenues, Reinvestment Rate, ROE, Dividend Payout Ratio, Equity Reinvestment Rate, Pre-tax Operating Margin (Lease & R&D adjusted).

The model's formulas only read columns 3 (rev growth), 4 (pre-tax margin), 5 (after-tax ROC), 7 (unlevered beta), 10 (std dev), 13 (cost of capital), 14 (sales/capital), 15 (EV/Sales). Those columns are reproduced verbatim below (values to 6 significant figures; the remaining columns exist in the sheet but no formula references them):


| Industry Name | Number of firms | Annual Average Revenue growth - Last 5 years | Pre-tax Operating Margin (Unadjusted) | After-tax ROC | Unlevered Beta | Std deviation in stock prices | Cost of capital | Sales/Capital | EV/Sales |
|---|---|---|---|---|---|---|---|---|---|
| Advertising | 49 | 0.0713158 | 0.106153 | 0.501981 | 1.10182 | 0.566968 | 0.0563665 | 4.80594 | 2.03466 |
| Aerospace/Defense | 73 | 0.0493976 | 0.0781333 | 0.147624 | 1.11041 | 0.382322 | 0.0588717 | 1.98483 | 2.32655 |
| Air Transport | 21 | -0.0699583 | -0.231356 | -0.198093 | 0.914138 | 0.401931 | 0.0482627 | 0.883836 | 2.13567 |
| Apparel | 39 | 0.061162 | 0.119572 | 0.203536 | 1.09835 | 0.43487 | 0.057266 | 1.82315 | 1.81604 |
| Auto & Truck | 26 | 0.119371 | 0.0525843 | 0.047412 | 1.02077 | 0.547769 | 0.0568742 | 0.833981 | 4.88459 |
| Auto Parts | 38 | 0.0610781 | 0.0640241 | 0.147711 | 1.21259 | 0.371404 | 0.0620348 | 2.43982 | 1.06211 |
| Bank (Money Center) | 7 | 0.0461333 | 0 | -8.974e-05 | 1.03251 | 0.22231 | 0.0346039 | 0.271597 | 4.00474 |
| Banks (Regional) | 563 | 0.11739 | 3.19304e-08 | -0.000818885 | 0.841274 | 0.196785 | 0.0379006 | 0.377693 | 3.56634 |
| Beverage (Alcoholic) | 21 | 0.145687 | 0.230295 | 0.152849 | 0.720525 | 0.37866 | 0.0451187 | 0.721389 | 4.77509 |
| Beverage (Soft) | 32 | 0.204723 | 0.206662 | 0.27304 | 1.11555 | 0.482654 | 0.0608615 | 1.37901 | 4.96509 |
| Broadcasting | 28 | 0.0964426 | 0.183197 | 0.172219 | 0.811272 | 0.487694 | 0.0474776 | 1.07371 | 1.8478 |
| Brokerage & Investment Banking | 31 | 0.179595 | 0.013087 | 0.00366082 | 0.67007 | 0.317394 | 0.0378835 | 0.300266 | 5.20349 |
| Building Materials | 44 | 0.0845433 | 0.116332 | 0.304407 | 1.08715 | 0.34535 | 0.058746 | 3.10166 | 2.13509 |
| Business & Consumer Services | 160 | 0.0538894 | 0.0911729 | 0.232641 | 0.986113 | 0.411734 | 0.054849 | 2.74492 | 2.65377 |
| Cable TV | 11 | 0.174187 | 0.192258 | 0.127719 | 0.664139 | 0.200732 | 0.0410193 | 0.811782 | 3.33102 |
| Chemical (Basic) | 35 | 0.20387 | 0.14932 | 0.273095 | 0.937128 | 0.450189 | 0.052555 | 2.00226 | 1.20378 |
| Chemical (Diversified) | 4 | 0.0805625 | 0.0971804 | 0.13744 | 1.20791 | 0.372916 | 0.0608918 | 1.45204 | 1.33476 |
| Chemical (Specialty) | 81 | 0.0793447 | 0.133279 | 0.150213 | 0.997723 | 0.407237 | 0.0560329 | 1.22148 | 3.32652 |
| Coal & Related Energy | 18 | -0.218443 | -0.0320878 | -0.0404494 | 0.819711 | 0.585697 | 0.0457477 | 1.51864 | 1.36017 |
| Computer Services | 83 | 0.0887145 | 0.0648065 | 0.214069 | 1.05762 | 0.484425 | 0.057481 | 3.36655 | 1.53197 |
| Computers/Peripherals | 46 | 0.166779 | 0.207819 | 0.449288 | 1.24877 | 0.512738 | 0.0665917 | 2.22005 | 5.32534 |
| Construction Supplies | 48 | 0.0627641 | 0.110292 | 0.128839 | 0.979649 | 0.400064 | 0.0542448 | 1.30487 | 2.38725 |
| Diversified | 22 | 0.00279 | 0.301189 | 0.214453 | 0.702141 | 0.30111 | 0.0426552 | 0.770128 | 2.81328 |
| Drugs (Biotechnology) | 581 | 0.308573 | 0.123654 | 0.0729687 | 0.972233 | 0.507986 | 0.0530767 | 0.465873 | 7.06236 |
| Drugs (Pharmaceutical) | 298 | 0.428481 | 0.247103 | 0.196643 | 1.00982 | 0.561665 | 0.0563011 | 0.687018 | 5.24833 |
| Education | 35 | 0.00810421 | 0.05924 | 0.0710394 | 1.10332 | 0.415016 | 0.055336 | 1.16616 | 2.72434 |
| Electrical Equipment | 104 | 0.0583578 | 0.113987 | 0.227794 | 1.19433 | 0.576591 | 0.0628731 | 1.99421 | 3.98323 |
| Electronics (Consumer & Office) | 16 | 0.014991 | 0.0480056 | 0.183222 | 1.05716 | 0.525378 | 0.0543325 | 3.42602 | 1.54901 |
| Electronics (General) | 137 | 0.0841353 | 0.103706 | 0.175928 | 1.05102 | 0.434455 | 0.0571583 | 1.77221 | 2.87714 |
| Engineering/Construction | 48 | 0.0882804 | 0.0469614 | 0.159878 | 0.973963 | 0.36356 | 0.0524446 | 3.73328 | 1.05886 |
| Entertainment | 108 | 0.226133 | 0.0867215 | 0.100604 | 0.964248 | 0.596294 | 0.0538036 | 1.17854 | 6.37336 |
| Environmental & Waste Services | 58 | -0.004016 | 0.129384 | 0.255626 | 1.08618 | 0.430136 | 0.0605138 | 2.07207 | 3.62964 |
| Farming/Agriculture | 36 | 0.0684131 | 0.0750305 | 0.134756 | 0.847865 | 0.464456 | 0.0499947 | 1.90783 | 1.26468 |
| Financial Svcs. (Non-bank & Insurance) | 223 | 0.112967 | 0.14065 | 0.00585649 | 0.151759 | 0.285213 | 0.0268613 | 0.0487052 | 25.0395 |
| Food Processing | 92 | 0.129877 | 0.134707 | 0.195383 | 0.632414 | 0.276898 | 0.041356 | 1.60434 | 2.23489 |
| Food Wholesalers | 15 | 0.17189 | 0.0193386 | 0.122908 | 1.08348 | 0.540091 | 0.0590661 | 7.24121 | 0.521829 |
| Furn/Home Furnishings | 32 | 0.0619224 | 0.10946 | 0.247558 | 0.993069 | 0.447704 | 0.0540972 | 2.5259 | 1.24915 |
| Green & Renewable Energy | 20 | -0.24637 | 0.236571 | 0.0572669 | 1.09526 | 0.817559 | 0.0731826 | 0.248263 | 10.3798 |
| Healthcare Products | 244 | 0.189475 | 0.176852 | 0.186437 | 0.91238 | 0.438122 | 0.0525957 | 1.03777 | 7.00397 |
| Healthcare Support Services | 131 | 0.179645 | 0.0426515 | 0.320468 | 0.949847 | 0.468572 | 0.0532833 | 8.32786 | 0.779551 |
| Heathcare Information and Technology | 142 | 0.158682 | 0.180879 | 0.230645 | 0.908888 | 0.462843 | 0.0524649 | 1.22329 | 7.7762 |
| Homebuilding | 29 | 0.202543 | 0.162826 | 0.229208 | 1.58556 | 0.394749 | 0.0751173 | 1.72912 | 1.36637 |
| Hospitals/Healthcare Facilities | 31 | -0.0164785 | 0.128509 | 0.231684 | 0.963582 | 0.523135 | 0.0547282 | 2.04431 | 1.67936 |
| Hotel/Gaming | 66 | 0.0217989 | -0.0910908 | -0.0468875 | 1.43743 | 0.438673 | 0.0706801 | 0.394644 | 8.86988 |
| Household Products | 118 | 0.117029 | 0.184102 | 0.397789 | 0.920072 | 0.585677 | 0.053226 | 2.27998 | 4.37853 |
| Information Services | 79 | 0.131246 | 0.237803 | 0.2904 | 1.20387 | 0.464408 | 0.0641752 | 1.3428 | 8.74913 |
| Insurance (General) | 23 | 0.0592731 | 0.169613 | 0.129723 | 0.810909 | 0.371507 | 0.0476506 | 0.862954 | 2.37691 |
| Insurance (Life) | 24 | 0.064553 | 0.120605 | 0.0649128 | 0.882988 | 0.318132 | 0.0458841 | 0.62626 | 1.34725 |
| Insurance (Prop/Cas.) | 52 | 0.041376 | 0.157007 | 0.173798 | 0.784777 | 0.292443 | 0.0461948 | 1.27297 | 1.31 |
| Investments & Asset Management | 687 | 0.115799 | 0.162307 | 0.0972352 | 0.965118 | 0.319699 | 0.051584 | 0.610226 | 5.41779 |
| Machinery | 111 | 0.0529566 | 0.146713 | 0.272154 | 1.17826 | 0.347534 | 0.0624232 | 2.037 | 3.24952 |
| Metals & Mining | 74 | 0.165733 | 0.264702 | 0.361241 | 1.128 | 0.680763 | 0.0601077 | 1.39857 | 2.69922 |
| Office Equipment & Services | 18 | 0.00444857 | 0.0586221 | 0.134655 | 1.11147 | 0.310057 | 0.057255 | 2.42981 | 1.31466 |
| Oil/Gas (Integrated) | 4 | 0.060275 | 0.0719351 | 0.0512101 | 1.25093 | 0.287132 | 0.0658082 | 0.856843 | 1.59366 |
| Oil/Gas (Production and Exploration) | 183 | 0.174164 | -0.0257352 | -0.0154042 | 1.12799 | 0.554756 | 0.0603894 | 0.642009 | 3.10424 |
| Oil/Gas Distribution | 21 | 0.238908 | 0.164779 | 0.0681076 | 0.864511 | 0.449805 | 0.0518493 | 0.455474 | 3.5872 |
| Oilfield Svcs/Equip. | 100 | 0.0104954 | 0.0118054 | 0.0282204 | 1.17917 | 0.496346 | 0.060119 | 2.22632 | 0.735234 |
| Packaging & Container | 26 | 0.0492033 | 0.0972508 | 0.154027 | 0.778296 | 0.263842 | 0.0463459 | 1.87118 | 1.63382 |
| Paper/Forest Products | 11 | 0.015075 | 0.186424 | 0.448894 | 0.998496 | 0.306075 | 0.053838 | 2.71152 | 1.14122 |
| Power | 50 | 0.0433187 | 0.187724 | 0.0605784 | 0.557464 | 0.194943 | 0.0370054 | 0.383809 | 4.41447 |
| Precious Metals | 76 | 0.0797917 | 0.275787 | 0.147498 | 0.987377 | 0.562884 | 0.0537366 | 0.550483 | 4.24665 |
| Publishing & Newspapers | 21 | 0.0151813 | 0.077882 | 0.157654 | 1.46426 | 0.308002 | 0.0697366 | 2.2837 | 1.31237 |
| R.E.I.T. | 238 | 0.0815933 | 0.238845 | 0.027483 | 0.988222 | 0.326473 | 0.0550699 | 0.137416 | 14.228 |
| Real Estate (Development) | 19 | -0.08428 | 0.0743586 | 0.0128843 | 0.742441 | 0.513223 | 0.0450328 | 0.256146 | 5.227 |
| Real Estate (General/Diversified) | 10 | 0.091 | 0.154572 | 0.0501013 | 0.833266 | 0.306987 | 0.0471687 | 0.362864 | 6.0613 |
| Real Estate (Operations & Services) | 51 | 0.0548619 | 0.0029081 | -0.0279793 | 0.871125 | 0.414286 | 0.0501293 | 1.34757 | 2.18287 |
| Recreation | 60 | 0.0759969 | 0.113383 | 0.18444 | 1.07363 | 0.503546 | 0.0577839 | 1.85364 | 2.73283 |
| Reinsurance | 2 | 0.10415 | 0.0734251 | 0.066892 | 1.29503 | 0.259455 | 0.0592032 | 1.19164 | 0.687828 |
| Restaurant/Dining | 70 | 0.0470963 | 0.16434 | 0.147241 | 1.33217 | 0.427577 | 0.0693195 | 1.28971 | 5.12289 |
| Retail (Automotive) | 32 | 0.146971 | 0.070347 | 0.154721 | 1.12149 | 0.44492 | 0.0609364 | 2.86899 | 1.17017 |
| Retail (Building Supply) | 16 | 0.174281 | 0.144039 | 0.546171 | 1.41896 | 0.447346 | 0.0733895 | 4.54641 | 2.63319 |
| Retail (Distributors) | 68 | 0.0409634 | 0.0961538 | 0.162748 | 1.06451 | 0.431014 | 0.0588268 | 1.87739 | 1.84581 |
| Retail (General) | 16 | 0.0388785 | 0.0554049 | 0.208769 | 1.03836 | 0.338817 | 0.0569609 | 4.98633 | 0.963855 |
| Retail (Grocery and Food) | 15 | 0.0324125 | 0.0253057 | 0.0700716 | 0.212007 | 0.342691 | 0.0258843 | 4.42309 | 0.44613 |
| Retail (Online) | 60 | 0.102 | 0.0599288 | 0.121816 | 1.065 | 0.588177 | 0.0592023 | 1.7691 | 3.73324 |
| Retail (Special Lines) | 76 | 0.11783 | 0.0686035 | 0.172763 | 1.22896 | 0.455723 | 0.0633578 | 2.99169 | 1.11101 |
| Rubber& Tires | 2 | 0.042015 | 0.0540314 | 0.0728128 | 0.589213 | 0.47055 | 0.0410539 | 1.57532 | 0.87582 |
| Semiconductor | 67 | 0.0662517 | 0.274184 | 0.217046 | 1.13582 | 0.374564 | 0.0617656 | 0.797641 | 8.68918 |
| Semiconductor Equip | 34 | 0.139942 | 0.26976 | 0.372445 | 1.34142 | 0.332228 | 0.0695335 | 1.46456 | 6.07976 |
| Shipbuilding & Marine | 8 | 0.163933 | 0.172617 | 0.150082 | 0.802317 | 0.510373 | 0.0485913 | 0.877117 | 1.68592 |
| Shoe | 12 | 0.0638 | 0.155595 | 0.40946 | 1.18849 | 0.347149 | 0.0630681 | 2.95507 | 4.85007 |
| Software (Entertainment) | 88 | 0.22906 | 0.311188 | 0.254601 | 1.20755 | 0.54606 | 0.0653506 | 0.797907 | 8.1175 |
| Software (Internet) | 36 | 0.2206 | -0.022844 | 0.0164509 | 0.975064 | 0.38094 | 0.0552183 | 0.758396 | 17.0667 |
| Software (System & Application) | 375 | 0.177223 | 0.240217 | 0.250316 | 1.12245 | 0.457399 | 0.0614896 | 0.995958 | 12.8387 |
| Steel | 28 | 0.199733 | 0.161292 | 0.372505 | 0.982557 | 0.331282 | 0.0532314 | 2.65643 | 0.882484 |
| Telecom (Wireless) | 17 | -0.0159629 | 0.116994 | 0.0518064 | 0.62723 | 0.481577 | 0.0428806 | 0.539016 | 2.95963 |
| Telecom. Equipment | 82 | 0.0665884 | 0.1956 | 0.268421 | 1.05686 | 0.405293 | 0.0582221 | 1.38696 | 4.73565 |
| Telecom. Services | 42 | 0.101218 | 0.209424 | 0.153329 | 0.509153 | 0.386723 | 0.036986 | 0.784582 | 2.43851 |
| Tobacco | 16 | 0.069115 | 0.442498 | 0.644484 | 0.862249 | 0.248828 | 0.0493163 | 1.58288 | 5.05743 |
| Transportation | 17 | 0.108591 | 0.0824653 | 0.210506 | 0.715815 | 0.283353 | 0.043877 | 3.0324 | 1.52029 |
| Transportation (Railroads) | 4 | 0.0167 | 0.419479 | 0.153055 | 0.647608 | 0.163942 | 0.0415169 | 0.445484 | 8.55387 |
| Trucking | 34 | 0.0760318 | 0.0517303 | 0.0576228 | 1.27849 | 0.329918 | 0.0650722 | 1.31329 | 2.58783 |
| Utility (General) | 16 | 0.0273069 | 0.192268 | 0.0591178 | 0.596219 | 0.188282 | 0.0387338 | 0.34551 | 4.81242 |
| Utility (Water) | 14 | 0.145792 | 0.301549 | 0.0728825 | 0.61418 | 0.270945 | 0.0412909 | 0.270532 | 10.3938 |

### Industry Average Beta (Global) — sheet 'Industry Average Beta (Global)', rows 2–95

Same 94 industry names and same 27-column layout as the US sheet, computed over global firms. Same used-columns extract, verbatim:


| Industry Name | Number of firms | Annual Average Revenue growth - Last 5 years | Pre-tax Operating Margin (Unadjusted) | After-tax ROC | Unlevered Beta | Std deviation in stock prices | Cost of capital | Sales/Capital | EV/Sales |
|---|---|---|---|---|---|---|---|---|---|
| Advertising | 348 | 0.0493011 | 0.0845431 | 0.212548 | 1.18466 | 0.382796 | 0.0699998 | 2.7953 | 1.75148 |
| Aerospace/Defense | 272 | 0.0860367 | 0.0749995 | 0.12703 | 1.11169 | 0.331944 | 0.0692226 | 1.84319 | 2.13981 |
| Air Transport | 151 | -0.0881397 | -0.214492 | -0.108376 | 0.939547 | 0.309298 | 0.0603497 | 0.520425 | 3.25032 |
| Apparel | 1170 | 0.0185645 | 0.139876 | 0.17908 | 0.903344 | 0.31365 | 0.0603281 | 1.46291 | 3.12805 |
| Auto & Truck | 152 | 0.0802998 | 0.0664275 | 0.0631513 | 1.1106 | 0.314859 | 0.0680557 | 1.03297 | 1.65776 |
| Auto Parts | 728 | 0.0438323 | 0.0568711 | 0.0794829 | 1.43605 | 0.297996 | 0.0810976 | 1.64242 | 0.965669 |
| Bank (Money Center) | 610 | 0.0871595 | 0.00150711 | 0.000199267 | 0.590604 | 0.204236 | 0.0369441 | 0.14974 | 6.35365 |
| Banks (Regional) | 816 | 0.090463 | 0.00010329 | -0.000198789 | 0.66677 | 0.192155 | 0.0354027 | 0.22939 | 4.4604 |
| Beverage (Alcoholic) | 219 | 0.0558078 | 0.217949 | 0.130238 | 0.860183 | 0.252048 | 0.0591882 | 0.723175 | 5.30098 |
| Beverage (Soft) | 100 | 0.0753152 | 0.17191 | 0.222039 | 0.815904 | 0.306838 | 0.0570592 | 1.45474 | 4.19093 |
| Broadcasting | 139 | 0.0180597 | 0.157398 | 0.148439 | 0.812203 | 0.328373 | 0.055384 | 1.13937 | 1.5854 |
| Brokerage & Investment Banking | 599 | 0.154942 | 0.0184522 | 0.00365983 | 0.453834 | 0.302701 | 0.0411205 | 0.219457 | 6.11185 |
| Building Materials | 449 | 0.0630216 | 0.113229 | 0.18208 | 1.05337 | 0.280339 | 0.0672747 | 1.92073 | 2.00165 |
| Business & Consumer Services | 948 | 0.0599591 | 0.0841613 | 0.195132 | 1.03666 | 0.323425 | 0.0665426 | 2.71555 | 2.34819 |
| Cable TV | 54 | 0.0362659 | 0.190223 | 0.130087 | 0.715209 | 0.253941 | 0.053482 | 0.804911 | 3.24695 |
| Chemical (Basic) | 854 | 0.101838 | 0.125485 | 0.136933 | 1.02199 | 0.295189 | 0.0648061 | 1.27688 | 1.59766 |
| Chemical (Diversified) | 71 | 0.060421 | 0.11509 | 0.110009 | 1.14763 | 0.248028 | 0.0693357 | 1.19284 | 1.20267 |
| Chemical (Specialty) | 898 | 0.0951498 | 0.135995 | 0.14707 | 1.03948 | 0.307647 | 0.0673641 | 1.25224 | 2.90433 |
| Coal & Related Energy | 206 | 0.102478 | 0.17168 | 0.180465 | 1.09104 | 0.449006 | 0.0622993 | 1.12486 | 1.23717 |
| Computer Services | 1040 | 0.0884134 | 0.071006 | 0.212161 | 1.08725 | 0.317802 | 0.0691007 | 3.44457 | 1.66935 |
| Computers/Peripherals | 336 | 0.0420037 | 0.134208 | 0.227312 | 1.32739 | 0.338659 | 0.0815593 | 1.87957 | 2.79425 |
| Construction Supplies | 784 | 0.0742345 | 0.0997 | 0.103108 | 1.02193 | 0.284282 | 0.0637276 | 1.18772 | 1.53599 |
| Diversified | 318 | 0.0793339 | 0.170948 | 0.12454 | 0.819452 | 0.238748 | 0.0540325 | 0.850059 | 1.83189 |
| Drugs (Biotechnology) | 1223 | 0.27256 | 0.108662 | 0.0705061 | 1.1008 | 0.454207 | 0.0689784 | 0.491988 | 7.87057 |
| Drugs (Pharmaceutical) | 1371 | 0.177845 | 0.214437 | 0.155339 | 1.01951 | 0.397863 | 0.0663807 | 0.723728 | 4.30722 |
| Education | 244 | 0.0777738 | 0.0961401 | 0.0844277 | 0.997308 | 0.323764 | 0.0613385 | 0.951058 | 2.73821 |
| Electrical Equipment | 999 | 0.0856754 | 0.0709826 | 0.112328 | 1.0807 | 0.337176 | 0.0680821 | 1.70497 | 2.61971 |
| Electronics (Consumer & Office) | 138 | 0.0254224 | 0.063684 | 0.116673 | 1.18683 | 0.315366 | 0.0706483 | 1.68094 | 1.0566 |
| Electronics (General) | 1425 | 0.0730618 | 0.0834228 | 0.143367 | 1.31158 | 0.310285 | 0.0773032 | 1.57647 | 1.94309 |
| Engineering/Construction | 1267 | 0.0348621 | 0.0480726 | 0.0905371 | 0.84476 | 0.294324 | 0.0535301 | 2.10783 | 0.625236 |
| Entertainment | 734 | 0.0705569 | 0.0932439 | 0.112096 | 1.107 | 0.386384 | 0.0691408 | 1.18451 | 4.91961 |
| Environmental & Waste Services | 353 | 0.084489 | 0.110652 | 0.125556 | 0.895972 | 0.337446 | 0.060649 | 1.28503 | 3.02109 |
| Farming/Agriculture | 417 | 0.105325 | 0.0726044 | 0.0998782 | 0.767626 | 0.303269 | 0.0544541 | 1.52702 | 1.28179 |
| Financial Svcs. (Non-bank & Insurance) | 1102 | 0.0905216 | 0.101221 | 0.00649434 | 0.195822 | 0.300193 | 0.0349163 | 0.0750818 | 15.5256 |
| Food Processing | 1377 | 0.0919442 | 0.0925078 | 0.138489 | 0.768545 | 0.267934 | 0.0542759 | 1.76238 | 1.7922 |
| Food Wholesalers | 160 | 0.0513342 | 0.0224235 | 0.0951796 | 0.603297 | 0.300634 | 0.0473115 | 5.05167 | 0.451341 |
| Furn/Home Furnishings | 359 | 0.0906829 | 0.0899057 | 0.217564 | 1.14573 | 0.290809 | 0.0679733 | 2.73244 | 1.3898 |
| Green & Renewable Energy | 239 | 0.164065 | 0.334859 | 0.0803234 | 0.759353 | 0.326604 | 0.055029 | 0.266234 | 8.8092 |
| Healthcare Products | 852 | 0.160281 | 0.19025 | 0.1921 | 1.00516 | 0.380646 | 0.0660573 | 1.04585 | 5.88733 |
| Healthcare Support Services | 445 | 0.162069 | 0.0443951 | 0.249193 | 0.853296 | 0.346947 | 0.0578831 | 6.63598 | 0.784387 |
| Heathcare Information and Technology | 455 | 0.160673 | 0.173813 | 0.20985 | 1.03069 | 0.395434 | 0.0676021 | 1.20505 | 8.39962 |
| Homebuilding | 168 | 0.115348 | 0.136955 | 0.14906 | 1.36803 | 0.293323 | 0.077208 | 1.46055 | 1.22586 |
| Hospitals/Healthcare Facilities | 223 | 0.0871541 | 0.113431 | 0.12182 | 0.736653 | 0.290272 | 0.0539659 | 1.30747 | 2.4365 |
| Hotel/Gaming | 654 | -0.0901821 | -0.0798221 | -0.0350402 | 0.949519 | 0.322519 | 0.0621167 | 0.388931 | 6.5791 |
| Household Products | 575 | 0.0474997 | 0.157247 | 0.250885 | 0.997516 | 0.357154 | 0.0658704 | 1.80311 | 3.82125 |
| Information Services | 266 | 0.11343 | 0.202271 | 0.260417 | 1.22686 | 0.397471 | 0.0767347 | 1.47181 | 7.92242 |
| Insurance (General) | 215 | 0.0641441 | 0.103239 | 0.14195 | 0.717759 | 0.230256 | 0.047532 | 1.60842 | 0.976443 |
| Insurance (Life) | 142 | 0.100394 | 0.104188 | 0.109426 | 0.996728 | 0.22916 | 0.047481 | 1.26101 | 0.826036 |
| Insurance (Prop/Cas.) | 231 | 0.054199 | 0.115394 | 0.132959 | 0.818309 | 0.259468 | 0.0546388 | 1.36271 | 1.04458 |
| Investments & Asset Management | 1706 | 0.281224 | 0.202242 | 0.100859 | 0.71914 | 0.314716 | 0.0509012 | 0.523879 | 4.56945 |
| Machinery | 1421 | 0.0689302 | 0.0994956 | 0.1314 | 1.12505 | 0.277138 | 0.0699178 | 1.52479 | 2.38377 |
| Metals & Mining | 1706 | 0.186234 | 0.159782 | 0.216054 | 1.01204 | 0.530665 | 0.0646085 | 1.40409 | 1.49011 |
| Office Equipment & Services | 145 | 0.0214156 | 0.0718066 | 0.123219 | 1.05162 | 0.297725 | 0.0639 | 1.93703 | 1.17363 |
| Oil/Gas (Integrated) | 46 | 0.0732121 | 0.119045 | 0.104745 | 1.14895 | 0.246938 | 0.0702363 | 1.13645 | 1.47156 |
| Oil/Gas (Production and Exploration) | 642 | 0.211859 | 0.124955 | 0.0635879 | 1.20877 | 0.507344 | 0.0754069 | 0.530345 | 2.84524 |
| Oil/Gas Distribution | 165 | 0.151522 | 0.12396 | 0.0624317 | 0.745269 | 0.283289 | 0.0553537 | 0.573702 | 2.67896 |
| Oilfield Svcs/Equip. | 457 | 0.0566004 | 0.0437722 | 0.0735168 | 1.05969 | 0.365753 | 0.0668148 | 1.84888 | 0.809479 |
| Packaging & Container | 414 | 0.0543688 | 0.0915231 | 0.121512 | 0.803195 | 0.281076 | 0.0561429 | 1.58704 | 1.64831 |
| Paper/Forest Products | 272 | 0.0547215 | 0.141598 | 0.124635 | 0.894646 | 0.285354 | 0.0591737 | 1.0149 | 1.41049 |
| Power | 541 | 0.0740769 | 0.112731 | 0.0575609 | 0.539242 | 0.219397 | 0.0434175 | 0.609762 | 2.26344 |
| Precious Metals | 947 | 0.252017 | 0.249782 | 0.228357 | 0.988173 | 0.511526 | 0.0631661 | 0.952622 | 2.5021 |
| Publishing & Newspapers | 337 | -0.000193529 | 0.0657545 | 0.0834778 | 0.940295 | 0.274071 | 0.0570807 | 1.44904 | 1.34321 |
| R.E.I.T. | 812 | 0.0809107 | 0.312515 | 0.0342606 | 0.766758 | 0.239207 | 0.0543671 | 0.121736 | 13.4806 |
| Real Estate (Development) | 893 | 0.0847955 | 0.140216 | 0.0777871 | 0.516198 | 0.27273 | 0.0422612 | 0.66756 | 1.44189 |
| Real Estate (General/Diversified) | 344 | 0.072855 | 0.152918 | 0.0377492 | 0.614121 | 0.246063 | 0.0456901 | 0.289098 | 3.23946 |
| Real Estate (Operations & Services) | 739 | 0.071725 | 0.182566 | 0.0366844 | 0.625502 | 0.263358 | 0.0486347 | 0.236688 | 5.67222 |
| Recreation | 324 | 0.0129824 | 0.104793 | 0.101016 | 1.02369 | 0.317719 | 0.0645468 | 1.11086 | 2.87625 |
| Reinsurance | 38 | 0.0647587 | 0.0603183 | 0.0889265 | 1.44084 | 0.245019 | 0.0763649 | 1.66648 | 0.650555 |
| Restaurant/Dining | 385 | -0.0212777 | 0.0969601 | 0.0981546 | 1.01036 | 0.29146 | 0.0662488 | 1.41045 | 3.43695 |
| Retail (Automotive) | 196 | 0.0612993 | 0.0535669 | 0.125515 | 0.88668 | 0.297038 | 0.060113 | 3.09921 | 0.862709 |
| Retail (Building Supply) | 98 | 0.0519242 | 0.128699 | 0.339691 | 1.10546 | 0.288443 | 0.0714991 | 3.352 | 2.23404 |
| Retail (Distributors) | 1002 | 0.0819098 | 0.0429447 | 0.0734931 | 0.646488 | 0.296766 | 0.0487335 | 2.03181 | 0.810255 |
| Retail (General) | 204 | -0.024462 | 0.0536288 | 0.120094 | 0.868122 | 0.246997 | 0.0577313 | 2.95402 | 0.981096 |
| Retail (Grocery and Food) | 184 | 0.0359687 | 0.0431345 | 0.108557 | 0.534664 | 0.226864 | 0.0421511 | 3.2757 | 0.724993 |
| Retail (Online) | 353 | 0.140586 | 0.0313456 | 0.0658942 | 1.40488 | 0.438986 | 0.0855133 | 1.70826 | 3.96031 |
| Retail (Special Lines) | 479 | 0.0126133 | 0.0612691 | 0.132793 | 1.08621 | 0.316351 | 0.0675218 | 2.59908 | 1.2014 |
| Rubber& Tires | 90 | 0.0410993 | 0.102383 | 0.101234 | 1.09776 | 0.255828 | 0.0668485 | 1.15776 | 1.21612 |
| Semiconductor | 581 | 0.081461 | 0.220161 | 0.186619 | 1.55309 | 0.343566 | 0.0930009 | 0.879542 | 6.58345 |
| Semiconductor Equip | 324 | 0.118235 | 0.232669 | 0.251172 | 1.93372 | 0.330736 | 0.112396 | 1.19659 | 6.81063 |
| Shipbuilding & Marine | 348 | 0.0648844 | 0.235185 | 0.19977 | 0.986017 | 0.289009 | 0.0612892 | 0.95161 | 1.85331 |
| Shoe | 84 | -0.0316134 | 0.118529 | 0.200493 | 1.12947 | 0.304897 | 0.0714976 | 1.97671 | 3.77147 |
| Software (Entertainment) | 317 | 0.121989 | 0.268964 | 0.2119 | 1.27978 | 0.413545 | 0.0806028 | 0.814281 | 7.66561 |
| Software (Internet) | 151 | 0.209201 | 0.0120616 | 0.0379499 | 1.10845 | 0.366296 | 0.0716797 | 1.17045 | 10.6475 |
| Software (System & Application) | 1603 | 0.145828 | 0.203194 | 0.213767 | 1.20084 | 0.395922 | 0.0763036 | 1.03789 | 11.0953 |
| Steel | 709 | 0.129882 | 0.149805 | 0.20855 | 1.06758 | 0.318656 | 0.0652583 | 1.6224 | 0.797187 |
| Telecom (Wireless) | 101 | 0.00273099 | 0.140463 | 0.088252 | 0.717593 | 0.251219 | 0.0516511 | 0.734846 | 2.10735 |
| Telecom. Equipment | 465 | 0.034432 | 0.112099 | 0.14256 | 1.16732 | 0.325497 | 0.0722277 | 1.27989 | 2.9215 |
| Telecom. Services | 296 | 0.080951 | 0.15783 | 0.10602 | 0.576438 | 0.28129 | 0.0469364 | 0.783956 | 2.17805 |
| Tobacco | 55 | 0.0304071 | 0.34453 | 0.224955 | 0.728929 | 0.272447 | 0.0530953 | 0.777115 | 3.67099 |
| Transportation | 295 | 0.0851744 | 0.0724579 | 0.112906 | 0.852938 | 0.281537 | 0.0574369 | 1.85432 | 1.34009 |
| Transportation (Railroads) | 51 | -0.000599333 | 0.154036 | 0.0452545 | 0.667512 | 0.178706 | 0.0491073 | 0.361181 | 5.26084 |
| Trucking | 232 | 0.0374525 | 0.0557924 | 0.0576998 | 0.920809 | 0.282637 | 0.0610111 | 1.19625 | 1.84693 |
| Utility (General) | 54 | 0.033781 | 0.123683 | 0.0703052 | 0.521651 | 0.185429 | 0.0426908 | 0.684447 | 2.4316 |
| Utility (Water) | 104 | 0.110979 | 0.250668 | 0.072912 | 0.514465 | 0.261782 | 0.0438885 | 0.344222 | 4.94094 |

---

## Outputs

All on `Valuation output`:

| Cell | Meaning | Example value |
|---|---|---|
| B16 | Terminal-year FCFF | 2,691,836.83 |
| B17 | Terminal cost of capital | 0.0624 |
| B18 | Terminal value (end of year 10) | 63,486,717.76 |
| B19 | PV(terminal value) | 32,303,991.78 |
| B20 | PV(CF over next 10 years) | 7,121,239.68 |
| B21 | Sum of PV (going-concern operating value) | 39,425,231.46 |
| B22 | Probability of failure | 0.12 |
| B23 | Proceeds if firm fails | 19,712,615.73 |
| B24 | Value of operating assets (failure-weighted) | 37,059,717.57 |
| B25 | − Debt (book, incl. lease debt) | 16,715,192 |
| B26 | − Minority interests | 0 |
| B27 | + Cash | 6,699,463 |
| B28 | + Non-operating assets | 0 |
| B29 | Value of equity | 27,043,988.57 |
| B30 | − Value of options | 0 |
| B31 | Value of equity in common stock | 27,043,988.57 |
| B32 | Number of shares | 83.6 |
| **B33** | **Estimated value per share** | **323,492.686** |
| B34 | Current price | 273,500 |
| B35 | Price as % of value | 0.845460 |

Secondary outputs: full year-by-year table (revenues, margins, EBIT, taxes, EBIT(1−t), reinvestment, FCFF, NOL, invested capital, ROIC, cost of capital, discount factors, PV) in rows 2–14 and 38–40; Diagnostics!B6 marginal ROIC = 0.459737; Diagnostics!B9 value/price = 1.182789; Summary Sheet F50 cross-check of operating value; Cost of capital worksheet E50 = initial WACC 0.07312245558; Synthetic rating D10/D11/D13 = rating, spread, synthetic cost of debt; R&D converter D35/D37/D39 = research asset, amortization, EBIT adjustment; Lease converter C28/F31/F32/F33 = lease debt, depreciation, EBIT adjustment, debt adjustment; Option value D27 = value of all options.

---

## Worked example (SK Innovation, as saved in the file)

Units: millions of KRW; shares in millions; per-share results in KRW.

1. **R&D capitalization** (life 5): research asset = 251,563×1 + 253,611×0.8 + 227,441×0.6 + 233,578×0.4 + 195,693×0.2 + 145,318×0 = **723,486.2**. Amortization = (253,611 + 227,441 + 233,578 + 195,693 + 145,318)/5 = **211,128.2**. EBIT adjustment = 251,563 − 211,128.2 = **+40,434.8**.
2. **Adjusted base year**: EBIT = −250,829 + 40,434.8 = **−210,394.2** (margin −0.0065022 on revenues 32,357,222). Invested capital = 14,405,108 + 16,715,192 − 6,699,463 + 723,486.2 = **25,144,323.2**. No lease adjustment (B14 = No).
3. **Cost of capital**: unlevered beta = Multibusiness(Global) weighted average = 1.143162 (weights from revenues × EV/Sales across Oil/Gas P&E, Chemical Basic, Chemical Specialty, Electronics General, Metals & Mining). ERP = Operating-regions mix = 0.0517466. Cost of debt = actual rating Baa2/BBB: 0.0169 + 0.0159107 = 0.0328107; market value of debt = 351,778×annuity(3y) + 16,715,192/1.0328107³ = 16,161,914.12. Market equity = 83.6 × 273,500 = 22,864,600. Levered beta = 1.143162×(1 + 0.75×16,161,914.12/22,864,600) = 1.749197. Cost of equity = 0.0169 + 1.749197×0.0517466 = 0.1074151. **WACC = 0.585873×0.1074151 + 0.414127×0.0328107×0.75 = 0.0731225**.
4. **Forecast** (year: revenue growth / revenue / margin / EBIT / EBIT(1−t) / reinvestment / FCFF):
   - Y1: 0.50 / 48,535,833 / 0.03 / 1,456,074.99 / 1,092,239.09 (NOL 731.4 shields that amount; tax only on excess) / 1,617,861.10 (ΔRev/10) / **−525,622.01**
   - Y2: 0.05 / 50,962,624.65 / 0.039 / 1,987,542.36 / 1,490,656.77 / 485,358.33 (ΔRev/5) / 1,005,298.44
   - Y3: 0.05 / 53,510,755.88 / 0.0435 / 2,327,717.88 / 1,745,788.41 / 509,626.25 / 1,236,162.16
   - Y4: 0.05 / 56,186,293.68 / 0.048 / 2,696,942.10 / 2,022,706.57 / 535,107.56 / 1,487,599.01
   - Y5: 0.05 / 58,995,608.36 / 0.0525 / 3,097,269.44 / 2,322,952.08 / 1,872,876.46 (ΔRev/1.5) / 450,075.62
   - Y6: 0.044 / 61,591,415.13 / 0.0423991 (kink — years 6–10 anchor on base-year margin) / 2,611,420.99 / 1,958,565.74 / 1,730,537.85 / 228,027.89
   - Y7: 0.038 / 63,931,888.90 / 0.0505493 / 3,231,714.15 / 2,423,785.62 / 1,560,315.85 / 863,469.77
   - Y8: 0.032 / 65,977,709.35 / 0.0586996 / 3,872,862.07 / 2,904,646.55 / 1,363,880.30 / 1,540,766.26
   - Y9: 0.026 / 67,693,129.79 / 0.0668498 / 4,525,270.61 / 3,393,952.96 / 1,143,613.63 / 2,250,339.33
   - Y10: 0.020 / 69,046,992.39 / 0.075 / 5,178,524.43 / 3,883,893.32 / 902,575.06 / 2,981,318.26
5. **Cost of capital path**: 0.0731225 for years 1–5, fading by (0.0731225 − 0.0624)/5 per year to 0.0624 at year 10 (terminal = 0.02 post-yr-10 rf + 0.0424 mature ERP). Cumulative discount factor year 10 = 0.5088307.
6. **Terminal year**: growth 0.02 (= overridden post-yr-10 rf); revenue 70,427,932.23; margin 0.075; EBIT 5,282,094.92; tax 0.25 (marginal); EBIT(1−t) 3,961,571.19; terminal ROC = terminal WACC = 0.0624 so reinvestment rate = 0.02/0.0624 = 0.320513 → reinvestment 1,269,734.36; **terminal FCFF 2,691,836.83**; TV = 2,691,836.83/(0.0624 − 0.02) = **63,486,717.76**.
7. **Value**: PV(TV) = 63,486,717.76 × 0.5088307 = 32,303,991.78; PV of 10-yr FCFF = 7,121,239.68; sum = 39,425,231.46. Failure: p = 0.12, proceeds = 0.5 × 39,425,231.46 ("V") = 19,712,615.73. Operating assets = 39,425,231.46×0.88 + 19,712,615.73×0.12 = **37,059,717.57**. Equity = 37,059,717.57 − 16,715,192 + 6,699,463 = 27,043,988.57. Options = 0 (flag "No"). **Value/share = 27,043,988.57/83.6 = 323,492.69** vs price 273,500 → price is 84.5% of value (undervalued).

---

## Reimplementation notes (Python port)

**Inputs** (name : type : units):
- company meta: country (str, must match ERP table key), industry_us / industry_global (str, must match industry-table keys).
- base year: revenues, ebit, interest_expense, bv_equity, bv_debt, cash, cross_holdings, minority_interests (float, currency units); shares_outstanding (float); stock_price (float); effective_tax_rate, marginal_tax_rate (float, decimals).
- drivers: g_next_year, g_years_2_5, margin_next_year, target_margin (decimals); convergence_year (int, default 10); sales_to_capital_1, sales_to_capital_2_5, sales_to_capital_6_10 (float).
- market: riskfree (decimal); cost_of_capital_initial (decimal — either from the CoC builder or given directly).
- flags + conditional values: capitalize_rnd (bool → rnd_life int ≤ 10, rnd_current float, rnd_past list ordered year −1 first, length life−1); has_leases (bool → lease_expense_current, commitments year 1–5, commitment_6_plus); has_options (bool → n_options, strike, maturity, stddev, dividend_yield); override_terminal_wacc (bool, value); override_terminal_roc (bool, value); failure (bool → prob_failure, proceeds_base "B"|"V", proceeds_pct); keep_effective_tax (bool); has_nol (bool → nol_carryforward); override_rf_after_10 (bool, value); override_terminal_growth (bool, value); trapped_cash (bool → amount, foreign_tax_rate).
- CoC builder: beta_approach + (direct beta | industry name(s) with revenues), erp_approach + (direct erp | country | country-revenue pairs | region-revenue pairs incl. free rows with hand-set ERPs), debt: book value, interest expense, avg maturity, cost-of-debt approach + (rate | rating str | firm_type 1/2), convertible (book, interest, maturity, market value), preferred (shares, price, dividend).
- reference data: mature_market_erp (0.0424 in this vintage), country table, region table, two synthetic-rating tables, rating→spread map, two industry tables.

**Computation order**: (1) lease converter + R&D converter (iterate lease↔cost-of-debt if synthetic rating); (2) cost of capital; (3) adjusted base EBIT and invested capital; (4) 10-year arrays; (5) terminal year; (6) discount, TV, failure adjustment, equity bridge; (7) options (iterate value↔adjusted S; or solve the deep-ITM case directly).

**Branches to reproduce exactly**:
- Margin path: years 2–5 interpolate target←year-1 margin; years 6–10 interpolate target←BASE-year margin (the kink is in the original; decide consciously whether to keep it — keep for fidelity).
- EBIT(1−t): if EBIT ≤ 0 → no tax; else tax only (EBIT − prior-year NOL) when EBIT > prior NOL, no tax when EBIT ≤ prior NOL. NOL rolls: grows by |EBIT| in loss years, shrinks by EBIT in profit years, floors at 0.
- Reinvestment year 1 floors at 0 when revenue declines; years 2–10 do NOT floor (can be negative). Terminal reinvestment = (g/ROC_terminal)×EBIT(1−t), 0 if g ≤ 0.
- Tax rate: effective for years 1–5, linear 5-step ramp to marginal (or stays effective if keep_effective_tax) in years 6–10.
- Growth: yr1 rate, constant yrs 2–5, linear fade yrs 6–10 to terminal g; terminal g = override, else post-10 rf, else rf.
- WACC: constant yrs 1–5, linear fade yrs 6–10 to terminal WACC = override, else (post-10 rf or rf) + mature_market_erp.
- Terminal ROC default = terminal WACC (makes growth value-neutral); overridable.
- Coverage-ratio sentinels: interest = 0 → ratio 1,000,000 (best rating); EBIT < 0 → −100,000 (worst). Rating table choice by firm type (1 large, 2 small/risky); firm type 3 (financial) has no table in this file.
- Distress proceeds base: "B" → (bv_equity + bv_debt)×pct; "V" → going-concern operating value×pct.
- Trapped cash: cash − trapped×(marginal_tax − foreign_tax) when flag set (case-insensitive "Yes").
- Options subtracted from equity only when has_options; Black–Scholes with dilution: S_adj = (S×n_shares + V_opt×n_options)/(n_shares + n_options), d1 uses (r − q + σ²/2), strike discounted at r, S term multiplied by e^(−qT).
- Debt in equity bridge is BOOK debt (+ lease debt); debt in WACC weights is estimated MARKET value (annuity + balloon at cost of debt over avg maturity). Keep both.
- VLOOKUPs on coverage/thresholds are range lookups (bisect on the ">" column); VLOOKUPs on names/ratings should be exact-match in the port (the sheet's approximate-match on unsorted text lists is an Excel quirk that happens to work).

**Edge cases**: negative base EBIT (handled via NOL + no-tax branch — the example exercises it); revenue decline (negative reinvestment yrs 2–10, zero yr 1); coverage sentinels; terminal g ≤ 0 (zero terminal reinvestment; TV denominator grows); g approaching terminal WACC → TV blows up (guard: require terminal WACC > terminal g); missing industry/country name → KeyError (Excel returns wrong row on approximate match — do NOT replicate); firm type 3 synthetic rating unsupported; probability-of-failure default 0 when flag off; options flag off ⇒ skip option module even if option inputs present; year-of-convergence B27 < 10 caps the margin path at the target (the IF(year > B27, target, …) branch); iteration needed for lease/synthetic-rating and option circularities.

**Vintage note**: all reference data is the January 2022 update (mature-market ERP 4.24%; industry averages from year-end 2021 data). A port should treat these tables as replaceable data files, keyed by the exact strings above.

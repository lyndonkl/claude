# ginzu-fcff-corona — Damodaran "Simple Ginzu" FCFF valuation (Corona edition)

### fcffsimpleginzuCorona.xlsx

**Purpose:** Damodaran's flagship all-purpose intrinsic (DCF) valuation model — the "Ginzu" spreadsheet — in the special COVID-era edition he used in March 2020. It values any non-financial firm from ~15 inputs. The engine forecasts Free Cash Flow to the Firm (FCFF) over a 10-year explicit period plus a terminal value. It discounts at a cost of capital that fades to a mature-market level. It then adjusts for failure risk, cash, cross holdings, debt, minority interests and employee options. The workbook currently values **Boeing as of 2020-03-27** (units: US$ millions). It bundles helper modules: cost-of-capital builder, synthetic bond rating, R&D capitalizer, operating-lease-to-debt converter, dilution-adjusted Black-Scholes option valuer, a "story to numbers" narrative sheet, diagnostics, and reference tables (country ERPs updated Jan 1 2021; US and Global industry averages).

**Requires Excel iterative calculation** (circular references: cost of debt ↔ lease debt ↔ EBIT ↔ rating; option value ↔ diluted stock price). A Python port must solve these fixed points iteratively.

---

## Sheet: Input sheet

All user inputs live here (plus a few on 'Cost of capital worksheet'). Current example values are Boeing's.

### Inputs — base-year company numbers

| Label | Cell | Example value |
|---|---|---|
| Date of valuation | B1 | 2020-03-27 |
| Company name | B2 | Boeing |
| Country of incorporation | B5 | United States |
| Industry (US) | B6 | Aerospace/Defense |
| Industry (Global) | B7 | Aerospace/Defense |
| Revenues — this year (last 10K) | B8 | 76,559 |
| Revenues — last year | C8 | 101,127 |
| Years since last 10K | D8 | 1 |
| Operating income (EBIT) — this year / last year | B9 / C9 | −2,102 / 11,843 |
| Interest expense — this year / last year | B10 / C10 | 722 / 475 |
| Book value of equity — this year / last year | B11 / C11 | −8,617 / 339 |
| Book value of debt — this year / last year | B12 / C12 | 28,532 / 13,847 |
| Capitalize R&D? (Yes/No) | B13 | Yes |
| Have operating lease commitments? (Yes/No) | B14 | No |
| Cash and marketable securities | B15 | 10,030 |
| Cross holdings & other non-operating assets | B16 | 0 |
| Minority interests | B17 | 0 |
| Number of shares outstanding | B18 | 566 |
| Current stock price | B19 | 127.68 |
| Effective tax rate | B20 | 0.25 |
| Marginal tax rate | B21 | 0.25 |

### Inputs — value drivers

| Label | Cell | Example |
|---|---|---|
| Revenue growth rate next year (year 1) | B23 | −0.10 |
| Operating margin next year (year 1) | B24 | −0.05 |
| Compounded annual revenue growth, years 2–5 | B25 | 0.15 |
| Target pre-tax operating margin (year 10) | B26 | 0.05474920636 (formula `=K23`, i.e. global industry margin) |
| Year of convergence (margin reaches target) | B27 | 3 |
| Sales-to-capital ratio (reinvestment) | B28 | 3.8007367250 (formula `=I24`, company's own current ratio) |

### Inputs — market numbers

| Label | Cell | Example |
|---|---|---|
| Riskfree rate | B30 | 0.0085 |
| Initial cost of capital | B31 | 0.056828 (`='Cost of capital worksheet'!E50` — can be typed over) |

### Inputs — employee options

| Label | Cell | Example |
|---|---|---|
| Employee options outstanding? (Yes/No) | B33 | No |
| Number of options | B34 | 7.72 |
| Average strike price | B35 | 1.29 |
| Average maturity (years) | B36 | 7 |
| Standard deviation of stock price | B37 | 0.45 |

### Inputs — default-assumption overrides (each a Yes/No flag + a value used only if Yes)

| Assumption (default) | Override flag | Value cell | Example |
|---|---|---|---|
| Stable-period cost of capital = riskfree + mature-market ERP (see M12 note) | B41 = No | B42 = 0.075 | not used |
| Stable-period ROC = stable cost of capital (competitive advantage fades) | B44 = No | B45 = 0.10 | not used |
| No chance of failure | B47 = No | B48 = 0.20 (prob. of failure) | not used |
| Failure proceeds tied to: "B" (book capital) or "V" (fair value) | — | B49 = "V" | |
| Distress proceeds as % of book/fair value | — | B50 = 0.50 | |
| Effective tax rate converges to marginal rate by terminal year (if overridden, stays at effective) | B52 = No | — | |
| No NOL carryforward into year 1 | B54 = No | B55 = 250 | not used |
| Today's riskfree rate prevails forever (if overridden, rf changes after year 10) | **B57 = Yes** | **B58 = 0.02** | used |
| Perpetuity growth = riskfree rate | B60 = No | B61 = −0.05 | not used |
| No trapped cash / cash tax liability | B63 = No | B64 = 140,000 (trapped cash); B65 = 0.15 (tax rate on it) | not used |

### Computed feedback cells (Input sheet, right block)

- `I22 =IF(C8>0,(B8/C8)^(1/D8)-1,"NA")` — most-recent-year revenue CAGR (−0.2429).
- `I23 ='Valuation output'!B4` — current pre-tax margin (−0.0310).
- `I24 =B8/'Valuation output'!B39` — current sales/capital (3.8007).
- `I25 ='Valuation output'!B7/'Valuation output'!B39` — current ROIC (−0.1178).
- J/K columns 22–27: industry comparisons via `VLOOKUP(B6, 'Industry Average Beta (US)'!A2:S95, n)` and the Global analog, with n = 3 (revenue growth), 4 (pre-tax margin), 14 (sales/capital), 5 (ROC), 10 (stddev of stock), 13 (cost of capital). J30–J32 echo year-10 revenues, EBIT, ROIC from the Valuation output sheet.

---

## Sheet: Valuation output (the core engine)

Columns: B = base year, C..L = years 1–10, M = terminal year. Rows are the model.

### Row 2 — Revenue growth rate
- `C2 ='Input sheet'!B23` (year-1 growth).
- `D2 ='Input sheet'!B25`; `E2=D2; F2=E2; G2=F2` (years 2–5 constant at CAGR input).
- Years 6–10 fade linearly to terminal growth: `H2 =G2-((G2-$M$2)/5)`, `I2 =G2-((G2-$M$2)/5)*2`, … `L2 =G2-((G2-$M$2)/5)*5`.
- Terminal: `M2 =IF(B60="Yes", B61, IF(B57="Yes", B58, B30))` (Input-sheet refs) — perpetuity growth = override growth, else post-yr-10 riskfree, else current riskfree. Example: 0.02.

### Row 3 — Revenues
- `B3 ='Input sheet'!B8`; each year `Ct = C(t−1)*(1+growth_t)`; `M3 =L3*(1+M2)`.

### Row 4 — EBIT (operating) margin
- `B4 =B5/B3` (adjusted base margin, −0.031001). `C4 ='Input sheet'!B24` (year-1 margin).
- Years 2–10 converge linearly to target margin by the convergence year:
  `D4 =IF(D1>'Input sheet'!$B$27, $B$26, $B$26-(($B$26-$C$4)/$B$27)*($B$27-D1))` (`$B$26/$B$27` on Input sheet)
  i.e. margin_t = target if t > convergence_year, else target − ((target − year1_margin)/conv_year)·(conv_year − t).
  **Quirk (verbatim):** columns D–G anchor the ramp on `$C$4` (year-1 margin) but columns H–L anchor on `$B$4` (base-year margin). With convergence year ≤ 5 this never matters (the IF short-circuits to target); with convergence year > 5 the ramp slope changes at year 6. Port faithfully or flag.
- `M4 =L4`.

### Row 5 — EBIT
- Base year is *adjusted* EBIT:
  `B5 =IF(leases="Yes", IF(R&D="Yes", B9+lease_adj+R&D_adj, B9+lease_adj), IF(R&D="Yes", B9+R&D_adj, B9))`
  where lease_adj = 'Operating lease converter'!F32 and R&D_adj = 'R& D converter'!D39. Example: −2102 + (−271.4) = −2373.4.
- Years 1–10 and terminal: `EBIT_t = margin_t × revenue_t`.

### Row 6 — Tax rate
- `B6 ='Input sheet'!B20` (effective). Years 1–5 constant at effective. Years 6–10: `H6 =G6+($M$6-$G$6)/5` etc. (linear to terminal rate).
- `M6 =IF('Input sheet'!B52="Yes", B20_effective, B21_marginal)`.

### Row 7 — EBIT(1−t) with NOL shield
- `B7 =IF(B5>0, B5*(1-B6), B5)` (no tax benefit recorded on base-year loss).
- Years 1–10 (verbatim pattern, year t, prior NOL = row 10 previous column):
  `C7 =IF(C5>0, IF(C5<B10, C5, C5-(C5-B10)*C6), C5)`
  i.e. if EBIT ≤ 0 → no tax; if EBIT ≤ prior NOL → fully shielded, no tax; else tax only the excess over the NOL.
- `M7 =M5*(1-M6)` (no NOL in terminal year).

### Row 8 — Reinvestment
- Year 1: `C8 =IF(C3>B3, (C3-B3)/'Input sheet'!B28, 0)` — **floored at 0** if revenues decline.
- Years 2–10: `D8 =(D3-C3)/D38` — Δrevenue / sales-to-capital, **no floor** (can be negative if revenues fall).
- Terminal: `M8 =IF(M2>0, (M2/M40)*M7, 0)` — reinvestment = (g/terminal ROC) × terminal EBIT(1−t); zero if g ≤ 0.
- `N8 =SUM(C8:M8)` (info only).

### Row 9 — FCFF: `FCFF_t = EBIT(1−t)_t − Reinvestment_t` for every column including terminal.

### Row 10 — NOL balance
- `B10 =IF('Input sheet'!B54="Yes", B55, 0)`.
- `C10 =IF(C5<0, B10-C5, IF(B10>C5, B10-C5, 0))` — losses add to NOL; profits burn it down; floor at 0 once EBIT ≥ NOL. Same pattern all years.

### Row 12 — Cost of capital
- `C12 ='Input sheet'!B31` for years 1–5 (constant). Years 6–10 fade linearly: `H12 =G12-($G$12-$M$12)/5`, … `L12 = terminal`.
- Terminal: `M12 =IF(B41="Yes", B42, IF(B57="Yes", B58 + 'Country equity risk premiums'!B1, B30 + 'Country equity risk premiums'!B1))`
  — stable cost of capital = (post-yr-10 riskfree, else current riskfree) + **mature-market ERP** ('Country equity risk premiums'!B1 = 0.0472). (Sheet text says "riskfree + 4.5%"; the formula actually uses the mature ERP cell.) Example: 0.02 + 0.0472 = 0.0672.

### Row 13 — Cumulated discount factor: `C13 =1/(1+C12)`; `D13 =C13*(1/(1+D12))`; …

### Row 14 — PV(FCFF): `Ct14 = FCFF_t × DF_t`.

### Terminal value and equity bridge (column B, rows 16–35)

- `B16 =M9` (terminal FCFF); `B17 =M12`; `B18 =B16/(B17-M2)` (Gordon growth terminal value).
- `B19 =B18*L13` (PV of TV, discounted with the year-10 cumulated factor).
- `B20 =SUM(C14:L14)`; `B21 =B19+B20` (sum of PV).
- `B22 =IF(B47="Yes", B48, 0)` (probability of failure).
- `B23 =IF(B49="B", (BV_equity+BV_debt)*B50, B21*B50)` (distress proceeds).
- `B24 =B21*(1-B22) + B23*B22` (value of operating assets, failure-weighted).
- `B25 =IF(leases="Yes", BV_debt + 'Operating lease converter'!C28, BV_debt)` (debt incl. lease debt).
- `B26 = minority interests`; `B28 = non-operating assets`.
- `B27 =IF('Input sheet'!B63="YES", B15 - B64*(B21_marg... )` verbatim: `=IF('Input sheet'!B63="YES",'Input sheet'!B15-'Input sheet'!B64*('Input sheet'!B21-'Input sheet'!B65),'Input sheet'!B15)` — cash, less (trapped cash × (marginal rate − foreign rate)) if the trapped-cash override is on. (Excel string compare is case-insensitive, so "Yes" triggers it.)
- `B29 =B24-B25-B26+B27+B28` (value of equity).
- `B30 =IF('Input sheet'!B33="No", 0, 'Option value'!D27)` (value of employee options).
- `B31 =B29-B30`; `B32 = shares`; `B33 =B31/B32` (**value per share**); `B34 = price`; `B35 =B34/B33` (price as % of value).

### Rows 38–40 — Implied variables
- Row 38: sales-to-capital, constant at Input B28 for years 1–10.
- `B39` invested capital (base) = `BV_equity + BV_debt − cash` (+ 'Operating lease converter'!F33 if leases; + 'R& D converter'!D35 research asset if R&D). Example: −8617+28532−10030+10258.2 = 20,143.2.
- `C39 =B39+C8` … (capital accumulates by reinvestment).
- Row 40 ROIC: `B40 =B7/B39`, … `L40 =L7/L39`.
- `M40 =IF('Input sheet'!B44="Yes", B45, L12)` — terminal ROC = override, else terminal cost of capital (0.0672).

---

## Sheet: Cost of capital worksheet

Builds the initial cost of capital. User-input cells here (beyond Input-sheet pulls):

| Label | Cell | Example |
|---|---|---|
| Approach for estimating beta | B9 | "Single Business(US)" (choices: Direct input / Single Business(US) / Single Business(Global) / Multibusiness(US) / Multibusiness(Global)) |
| Direct levered/regression beta (if Direct input) | B10 | 1.2 |
| Approach for ERP | B13 | "Operating regions" (choices: Will input / Country of incorporation / Operating countries / Operating regions) |
| Direct ERP (if Will input) | B14 | 0.06 |
| Average maturity of debt (years) | B20 | 3 |
| Approach for pre-tax cost of debt | B21 | "Actual rating" (choices: Direct input / Synthetic rating / Actual rating) |
| Direct pre-tax cost of debt | B22 | 0.04 |
| Actual rating (if chosen) | B23 | "Baa2/BBB" |
| Firm type for synthetic rating | B24 | 2 (1 = large manufacturing, 2 = smaller/riskier, 3 = financial) |
| Convertible debt: book value / interest / maturity / market value | B28–B31 | 0, 0, 0, 0 |
| Preferred: # shares / price / dividend per share | B36–B38 | 0, 70, 5 |
| Operating-countries ERP table: country + revenues | G5:H17 | US 8,013; "Rest of the World" 7,782 @ ERP 0.0739 (manual) |
| Operating-regions ERP table: revenues per region | H21:H31 | Africa 1,113; Asia 10,662; Aus&NZ 2,006; Caribbean 0; C&S America 1,015; E.Europe&Russia 0; Middle East 9,272; North America 44,700; W.Europe 10,336; China (manual row, ERP 0.0638) 5,684 |
| Multi-business (US) table: business + revenues | G36:H47 | e.g. Computers/Peripherals 25,484 … |
| Multi-business (Global) table: business + revenues | G52:H63 | Beverage (Alcoholic) 35,538 |

Logic:

1. **Unlevered beta** `B11 =IF(B9="Single Business(US)", VLOOKUP(Industry_US, 'Industry Average Beta (US)'!A2:G95, 7), IF(B9="Multibusiness(US)", K48, IF(B9="Single Business(Global)", VLOOKUP(Industry_Global, …Global…, 7), K64)))`. Multibusiness betas K48/K64 = value-weighted average of business unlevered betas, weights = revenues × industry EV/Sales (col 15): `J = H*I`, `K48 =Σ beta_i · J_i / ΣJ`.
2. **ERP** `B15 =IF(B13="Will Input", B14, IF(B13="Country of Incorporation", VLOOKUP(country, 'Country equity risk premiums'!A5:E181, 4), IF(B13="Operating regions", K32, K18)))`. The operating-countries (K18) and operating-regions (K32) blocks compute revenue-weighted ERPs: `weight = revenue/total`, `weighted ERP = Σ w_i·ERP_i`; country ERPs via `VLOOKUP(country, 'Country equity risk premiums'!$A$5:$D$181, 4)`, region ERPs pulled from rows 185–193 of the country sheet. Example K32 = 0.05342843.
3. **Pre-tax cost of debt** `B25 =IF(B21="Direct Input", B22, IF(B21="Synthetic Rating", 'Synthetic rating'!D13, B12 + VLOOKUP(B23, 'Synthetic rating'!G39:H53, 2)))`. Example (actual rating Baa2/BBB): 0.0085 + 0.0171 = 0.0256. **Note:** the G39:H53 rating→spread list is NOT sorted and the VLOOKUP omits FALSE; a port should use exact-match lookup on the rating string.
4. **Market value of straight debt** (bond-pricing of book debt): `C41 =B19*(1-(1+B25)^(-B20))/B25 + B18/(1+B25)^B20` (interest expense as annuity + book value as balloon). Example: 28,507.98.
5. Convertible split: straight-debt part `C42 =B29*(1-(1+B25)^(-B30))/B25 + B28/(1+B25)^B30`; equity part `C44 =B31-C42`. Lease debt `B33/C43 = 'Operating lease converter'!F33 if leases else 0`.
6. **Levered beta** `C45 =IF(B9="Direct Input", B10, B11*(1+(1-B26)*(C48/B48)))` with tax rate B26 = marginal, D/E = market debt / market equity. Example: 0.9124·(1+0.75·(28,507.98/72,266.88)) = 1.18236.
7. Market values: equity `B48 =shares×price` (72,266.88); debt `C48 =C41+C42+C43`; preferred `D48 =B36*B37`; capital `E48 =ΣB48:D48`.
8. Component costs: cost of equity `B50 =B12 + C45*B15` (0.0085+1.18236·0.0534284=0.0716716); after-tax cost of debt `C50 =B25*(1-B26)` (0.0192); cost of preferred `D50 =B38/B37`.
9. **Cost of capital** `E50 =B49*B50 + C49*C50 + D49*D50` = 0.717112·0.0716716 + 0.282888·0.0192 = **0.056828** → feeds Input sheet B31.

---

## Sheet: Synthetic rating

Interest-coverage-based rating and cost of debt.

- `C4 ='Cost of capital worksheet'!B24` (firm type 1/2/3).
- `F5 =` EBIT (+ lease adjustment if leases = Yes): `=IF('Input sheet'!B14="Yes", B9+'Operating lease converter'!F32, B9)`. Example: −2102.
- `F6 =` interest expense (+ lease-debt × pre-tax cost of debt if leases): `=IF('Input sheet'!B14="Yes", B19+'Operating lease converter'!C28*'Operating lease converter'!C15, B19)`. Example: 722. (This is one of the circular loops.)
- `F7 =` riskfree rate.
- **Coverage** `D9 =IF(F6=0, 1000000, IF(F5<0, -100000, F5/F6))` — no interest → 1,000,000 (AAA); negative EBIT → −100,000 (D). Example: −100,000.
- **Rating** `D10 =IF(C4=1, VLOOKUP(D9, A19:D33, 3), IF(C4=2, VLOOKUP(D9, A38:D52, 3), VLOOKUP(D9, F19:I33, 3)))` (approximate-match on lower bound). **Note:** the financial-firm table F19:I33 is EMPTY in this workbook — firm type 3 would #N/A; port should treat type 3 as unsupported here or supply a table.
- **Company default spread** `D11` = same lookup, column 4. Example: 0.1744 (D rating).
- **Country default spread** `D12 =VLOOKUP(country, 'Country equity risk premiums'!A5:C181, 3)`. Example US: 0.
- **Cost of debt** `D13 =F7 + D11 + D12`. Example: 0.1829.

### Reference table — large manufacturing firms (firm type 1), A19:D33

| Coverage > | Coverage ≤ | Rating | Spread |
|---|---|---|---|
| −100000 | 0.199999 | D2/D | 0.1744 |
| 0.2 | 0.649999 | C2/C | 0.1309 |
| 0.65 | 0.799999 | Ca2/CC | 0.0997 |
| 0.8 | 1.249999 | Caa/CCC | 0.0946 |
| 1.25 | 1.499999 | B3/B− | 0.0594 |
| 1.5 | 1.749999 | B2/B | 0.0486 |
| 1.75 | 1.999999 | B1/B+ | 0.0405 |
| 2 | 2.2499999 | Ba2/BB | 0.0277 |
| 2.25 | 2.49999 | Ba1/BB+ | 0.0231 |
| 2.5 | 2.999999 | Baa2/BBB | 0.0171 |
| 3 | 4.249999 | A3/A− | 0.0133 |
| 4.25 | 5.499999 | A2/A | 0.0118 |
| 5.5 | 6.499999 | A1/A+ | 0.0107 |
| 6.5 | 8.499999 | Aa2/AA | 0.0085 |
| 8.5 | 100000 | Aaa/AAA | 0.0069 |

### Reference table — smaller and riskier firms (firm type 2), A38:D52

| Coverage > | Coverage ≤ | Rating | Spread |
|---|---|---|---|
| −100000 | 0.499999 | D2/D | 0.1744 |
| 0.5 | 0.799999 | C2/C | 0.1309 |
| 0.8 | 1.249999 | Ca2/CC | 0.0997 |
| 1.25 | 1.499999 | Caa/CCC | 0.0946 |
| 1.5 | 1.999999 | B3/B− | 0.0594 |
| 2 | 2.499999 | B2/B | 0.0486 |
| 2.5 | 2.999999 | B1/B+ | 0.0405 |
| 3 | 3.499999 | Ba2/BB | 0.0277 |
| 3.5 | 3.9999999 | Ba1/BB+ | 0.0231 |
| 4 | 4.499999 | Baa2/BBB | 0.0171 |
| 4.5 | 5.999999 | A3/A− | 0.0133 |
| 6 | 7.499999 | A2/A | 0.0118 |
| 7.5 | 9.499999 | A1/A+ | 0.0107 |
| 9.5 | 12.499999 | Aa2/AA | 0.0085 |
| 12.5 | 100000 | Aaa/AAA | 0.0069 |

### Reference table — rating → spread ("Spread in 2021"), G39:H53 (used by actual-rating branch; UNSORTED — use exact match)

| Rating | Spread |
|---|---|
| A1/A+ | 0.0107 |
| A2/A | 0.0118 |
| A3/A− | 0.0133 |
| Aa2/AA | 0.0085 |
| Aaa/AAA | 0.0069 |
| B1/B+ | 0.0405 |
| B2/B | 0.0486 |
| B3/B− | 0.0594 |
| Ba1/BB+ | 0.0231 |
| Ba2/BB | 0.0277 |
| Baa2/BBB | 0.0171 |
| C2/C | 0.1309 |
| Ca2/CC | 0.0997 |
| Caa/CCC | 0.0946 |
| D2/D | 0.1744 |

---

## Sheet: R& D converter

Capitalizes R&D as an asset amortized straight-line over N years.

Inputs: `F6` = amortization life N (example 5, max 10); `F7` = current-year R&D (3,219); `B11:B20` = R&D for past years −1…−N (3,269; 3,179; 4,626; 3,331; 3,047). Year labels in A11:A20 auto-fill: `A12 =IF((0-A11)<$F$6, IF(A11>-1,, A11-1),)`.

Logic (output block, rows 24–34; year index a = 0 for current, −k for k years ago):
- Unamortized fraction: current year = 1; past year a: `C =IF(a<0, (N+a)/N, 0)` (e.g. −1 → 4/5 = 0.8, −5 → 0).
- Unamortized value `D = R&D × fraction`; this-year amortization for past year a: `E =IF(a<0, R&D_a/N, 0)`.
- **Value of research asset** `D35 =SUM(D24:D34)` = 10,258.2 → added to invested capital and book equity.
- **Current-year amortization** `D37 =E35 =SUM(E25:E34)` = 3,490.4.
- **Adjustment to operating income** `D39 =F7 − D37` = 3,219 − 3,490.4 = **−271.4** → added to EBIT (positive raises EBIT).
- Tax effect (info): `D40 =D39×marginal rate` = −67.85.

---

## Sheet: Operating lease converter

Converts lease commitments into debt. (Boeing example has B14 = No, so its outputs are not used in the valuation, but the sheet is populated.)

Inputs: `E4` = current-year operating lease expense (295); `B7:B11` = commitments years 1–5 (287, 235, 194, 151, 98); `B12` = commitments year 6-and-beyond lump sum (605).

Logic:
- `C15 ='Cost of capital worksheet'!B25` (pre-tax cost of debt, 0.0256) — discount rate (circular with cost of debt when leases are on).
- Years embedded in the lump: `D18 =IF(B12>0, ROUND(B12/AVERAGE(B7:B11),0), 0)` → ROUND(605/193,0) = 3.
- PV of each year-t commitment: `C =B/(1+r)^t`.
- Year-6+ annuity: `B27 =IF(B12>0, IF(D18>0, B12/D18, B12), 0)` = 201.67/yr; `C27 =IF(D18>0, (B27*(1-(1+r)^(-D18))/r)/(1+r)^5, B27/(1+r)^6)` = 506.99.
- **Debt value of leases** `C28 =SUM(C22:C27)` = 1,412.92 → added to debt (Valuation output B25) and to invested capital (F33).
- Straight-line depreciation on lease asset: `F31 =C28/(5+D18)` = 176.61.
- **Adjustment to operating earnings** `F32 =E4 − F31` = 118.39 → added to EBIT.
- `F33 =C28` (add to debt); `F34 =F31` (add to depreciation).

---

## Sheet: Option value

Dilution-adjusted Black-Scholes for employee options (used only if Input B33 = "Yes"). Inputs pulled from Input sheet: stock price S (127.68), strike K (1.29), maturity T (7), σ (0.45), # options M (7.72), # shares N (566), riskfree r (0.0085); dividend yield q entered here at `D6` (0).

- Adjusted S (circular): `C15 =(S·N + W·M)/(N+M)` where W is the option value itself (C26).
- Variance `F16 =σ²`; div-adjusted rate `F18 =F15−F17` (verbatim: T-bond rate minus dividend yield — note it discounts the strike with the *raw* T-bond rate F15 and grows with F18).
- `d1 =(LN(S_adj/K) + (F18 + σ²/2)·T) / (σ·√T)`; `N(d1) =NORMSDIST(d1)`; `d2 =d1 − σ·√T`.
- Value per option `C26 =e^(−q·T)·S_adj·N(d1) − K·e^(−r·T)·N(d2)` = 126.448.
- **Value of all options** `D27 =C26×M` = 976.18 (unused here since B33 = No).

---

## Sheet: Country equity risk premiums

`B1 = 0.0472` — **mature-market ERP** (labeled "Mature Market ERP +", updated Jan 1 2021). Every country ERP = B1 + country risk premium (CRP): `D =$B$1+E`. Column C (Adj. Default Spread) feeds the synthetic-rating country spread; column D feeds ERP lookups; column F is a corporate tax-rate reference (unused by formulas). The last rows of the table are user-editable slots (e.g. "Saint Lucia"/"British Virgin Islands" rows hold placeholder 0.0331 CRP values).

Full table (A5:F181; ADS = adjusted default spread, ERP = equity risk premium, CRP = country risk premium, values rounded to 6 dp):

| Country | Moody's | ADS | ERP | CRP | Corp tax |
|---|---|---|---|---|---|
| Abu Dhabi | Aa2 | 0.004385 | 0.052006 | 0.004806 | 0.55 |
| Albania | B1 | 0.039783 | 0.090799 | 0.043599 | 0.15 |
| Algeria | NR | 0.079566 | 0.134398 | 0.087198 | 0.26 |
| Andorra (Principality of) | Caa1 | 0.066252 | 0.119807 | 0.072607 | 0.1 |
| Angola | Caa1 | 0.066252 | 0.119807 | 0.072607 | 0.3 |
| Argentina | Ca | 0.106035 | 0.163406 | 0.116206 | 0.3 |
| Armenia | Ba3 | 0.031810 | 0.082062 | 0.034862 | 0.18 |
| Aruba | Baa1 | 0.014111 | 0.062665 | 0.015465 | 0.25 |
| Australia | Aaa | 0 | 0.0472 | 0 | 0.3 |
| Austria | Aa1 | 0.003508 | 0.051044 | 0.003844 | 0.25 |
| Azerbaijan | Ba2 | 0.026549 | 0.076295 | 0.029095 | 0.2 |
| Bahamas | Ba2 | 0.026549 | 0.076295 | 0.029095 | 0 |
| Bahrain | B2 | 0.048632 | 0.100497 | 0.053297 | 0 |
| Bangladesh | Ba3 | 0.031810 | 0.082062 | 0.034862 | 0.25 |
| Barbados | Caa1 | 0.066252 | 0.119807 | 0.072607 | 0.055 |
| Belarus | B3 | 0.057482 | 0.110196 | 0.062996 | 0.18 |
| Belgium | Aa3 | 0.005342 | 0.053054 | 0.005854 | 0.29 |
| Belize | Caa3 | 0.088336 | 0.144009 | 0.096809 | 0.2825 |
| Benin | B2 | 0.048632 | 0.100497 | 0.053297 | 0.3 |
| Bermuda | A2 | 0.007494 | 0.055413 | 0.008213 | 0 |
| Bolivia | B2 | 0.048632 | 0.100497 | 0.053297 | 0.25 |
| Bosnia and Herzegovina | B3 | 0.057482 | 0.110196 | 0.062996 | 0.1 |
| Botswana | A2 | 0.007494 | 0.055413 | 0.008213 | 0.22 |
| Brazil | Ba2 | 0.026549 | 0.076295 | 0.029095 | 0.34 |
| British Virgin Islands | NR | 0.0302 | 0.0803 | 0.0331 | 0.1698 |
| Brunei | NR | 0.007494 | 0.055413 | 0.008213 | 0 |
| Bulgaria | Baa1 | 0.014111 | 0.062665 | 0.015465 | 0.1 |
| Burkina Faso | B2 | 0.048632 | 0.100497 | 0.053297 | 0.28 |
| Cambodia | B2 | 0.048632 | 0.100497 | 0.053297 | 0.2 |
| Cameroon | B2 | 0.048632 | 0.100497 | 0.053297 | 0.33 |
| Canada | Aaa | 0 | 0.0472 | 0 | 0.265 |
| Cape Verde | B2 | 0.048632 | 0.100497 | 0.053297 | 0 |
| Cayman Islands | Aa3 | 0.005342 | 0.053054 | 0.005854 | 0 |
| Chile | A1 | 0.006219 | 0.054015 | 0.006815 | 0.27 |
| China | A1 | 0.006219 | 0.054015 | 0.006815 | 0.25 |
| Colombia | Baa2 | 0.016822 | 0.065636 | 0.018436 | 0.32 |
| Congo (Democratic Republic of) | Caa1 | 0.066252 | 0.119807 | 0.072607 | 0.35 |
| Congo (Republic of) | Caa2 | 0.079566 | 0.134398 | 0.087198 | 0.3 |
| Cook Islands | B1 | 0.039783 | 0.090799 | 0.043599 | 0.2843 |
| Costa Rica | B2 | 0.048632 | 0.100497 | 0.053297 | 0.3 |
| Croatia | Ba1 | 0.022084 | 0.071402 | 0.024202 | 0.18 |
| Cuba | Caa2 | 0.079566 | 0.134398 | 0.087198 | 0.2736 |
| Curaçao | A3 | 0.010603 | 0.058821 | 0.011621 | 0.22 |
| Cyprus | Ba2 | 0.026549 | 0.076295 | 0.029095 | 0.125 |
| Czech Republic | Aa3 | 0.005342 | 0.053054 | 0.005854 | 0.19 |
| Denmark | Aaa | 0 | 0.0472 | 0 | 0.22 |
| Dominican Republic | Ba3 | 0.031810 | 0.082062 | 0.034862 | 0.27 |
| Ecuador | Caa3 | 0.088336 | 0.144009 | 0.096809 | 0.25 |
| Egypt | B2 | 0.048632 | 0.100497 | 0.053297 | 0.225 |
| El Salvador | B3 | 0.057482 | 0.110196 | 0.062996 | 0.3 |
| Estonia | A1 | 0.006219 | 0.054015 | 0.006815 | 0.2 |
| Ethiopia | B2 | 0.048632 | 0.100497 | 0.053297 | 0.3 |
| Fiji | Ba3 | 0.031810 | 0.082062 | 0.034862 | 0.2 |
| Finland | Aa1 | 0.003508 | 0.051044 | 0.003844 | 0.2 |
| France | Aa2 | 0.004385 | 0.052006 | 0.004806 | 0.28 |
| Gabon | Caa1 | 0.066252 | 0.119807 | 0.072607 | 0.3 |
| Gambia | NR | 0.057482 | 0.110196 | 0.062996 | 0.31 |
| Georgia | Ba2 | 0.026549 | 0.076295 | 0.029095 | 0.15 |
| Germany | Aaa | 0 | 0.0472 | 0 | 0.3 |
| Ghana | B3 | 0.057482 | 0.110196 | 0.062996 | 0.25 |
| Greece | Ba3 | 0.031810 | 0.082062 | 0.034862 | 0.24 |
| Guatemala | Ba1 | 0.022084 | 0.071402 | 0.024202 | 0.25 |
| Guernsey | Aaa | 0 | 0.0472 | 0 | 0 |
| Guinea | NR | 0.106035 | 0.163406 | 0.116206 | 0.2825 |
| Guinea-Bissau | NR | 0.066252 | 0.119807 | 0.072607 | 0.2825 |
| Guyana | NR | 0.048632 | 0.100497 | 0.053297 | 0.2736 |
| Haiti | NR | 0.106035 | 0.163406 | 0.116206 | 0.2736 |
| Honduras | B1 | 0.039783 | 0.090799 | 0.043599 | 0.25 |
| Hong Kong | Aa3 | 0.005342 | 0.053054 | 0.005854 | 0.165 |
| Hungary | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.09 |
| Iceland | A2 | 0.007494 | 0.055413 | 0.008213 | 0.2 |
| India | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.3 |
| Indonesia | Baa2 | 0.016822 | 0.065636 | 0.018436 | 0.15 |
| Iran | NR | 0.079566 | 0.134398 | 0.087198 | 0.2113 |
| Iraq | Caa1 | 0.066252 | 0.119807 | 0.072607 | 0.15 |
| Ireland | A2 | 0.007494 | 0.055413 | 0.008213 | 0.125 |
| Isle of Man | Aa3 | 0.005342 | 0.053054 | 0.005854 | 0 |
| Israel | A1 | 0.006219 | 0.054015 | 0.006815 | 0.23 |
| Italy | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.24 |
| Ivory Coast | Ba3 | 0.031810 | 0.082062 | 0.034862 | 0.25 |
| Jamaica | B2 | 0.048632 | 0.100497 | 0.053297 | 0.25 |
| Japan | A1 | 0.006219 | 0.054015 | 0.006815 | 0.3062 |
| Jersey | Aaa | 0 | 0.0472 | 0 | 0 |
| Jordan | B1 | 0.039783 | 0.090799 | 0.043599 | 0.2 |
| Kazakhstan | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.2 |
| Kenya | B2 | 0.048632 | 0.100497 | 0.053297 | 0.3 |
| Korea, D.P.R. | NR | 0.106035 | 0.163406 | 0.116206 | 0.2113 |
| Kuwait | A1 | 0.006219 | 0.054015 | 0.006815 | 0.15 |
| Kyrgyzstan | B2 | 0.048632 | 0.100497 | 0.053297 | 0.1 |
| Laos | Caa2 | 0.010603 | 0.058821 | 0.011621 | 0.2113 |
| Latvia | A3 | 0.010603 | 0.058821 | 0.011621 | 0.2 |
| Lebanon | C | 0.175 | 0.238987 | 0.191787 | 0.17 |
| Liberia | NR | 0.106035 | 0.163406 | 0.116206 | 0.2825 |
| Libya | NR | 0.079566 | 0.134398 | 0.087198 | 0.2 |
| Liechtenstein | Aaa | 0 | 0.0472 | 0 | 0.125 |
| Lithuania | A3 | 0.010603 | 0.058821 | 0.011621 | 0.15 |
| Luxembourg | Aaa | 0 | 0.0472 | 0 | 0.2494 |
| Macao | Aa3 | 0.005342 | 0.053054 | 0.005854 | 0.12 |
| Macedonia | Ba3 | 0.031810 | 0.082062 | 0.034862 | 0.1 |
| Madagascar | NR | 0.057482 | 0.110196 | 0.062996 | 0.2 |
| Malawi | NR | 0.079566 | 0.134398 | 0.087198 | 0.3 |
| Malaysia | A3 | 0.010603 | 0.058821 | 0.011621 | 0.24 |
| Mali | Caa1 | 0.066252 | 0.119807 | 0.072607 | 0.2825 |
| Malta | A2 | 0.007494 | 0.055413 | 0.008213 | 0.35 |
| Mauritius | Baa1 | 0.014111 | 0.062665 | 0.015465 | 0.15 |
| Mexico | Baa1 | 0.014111 | 0.062665 | 0.015465 | 0.3 |
| Moldova | B3 | 0.057482 | 0.110196 | 0.062996 | 0.12 |
| Mongolia | B3 | 0.057482 | 0.110196 | 0.062996 | 0.25 |
| Montenegro | B1 | 0.039783 | 0.090799 | 0.043599 | 0.09 |
| Montserrat | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.2113 |
| Morocco | Ba1 | 0.022084 | 0.071402 | 0.024202 | 0.31 |
| Mozambique | Caa2 | 0.079566 | 0.134398 | 0.087198 | 0.32 |
| Myanmar | NR | 0.057482 | 0.110196 | 0.062996 | 0.25 |
| Namibia | Ba3 | 0.031810 | 0.082062 | 0.034862 | 0.32 |
| Netherlands | Aaa | 0 | 0.0472 | 0 | 0.25 |
| New Zealand | Aaa | 0 | 0.0472 | 0 | 0.28 |
| Nicaragua | B3 | 0.057482 | 0.110196 | 0.062996 | 0.3 |
| Niger | B3 | 0.057482 | 0.110196 | 0.062996 | 0.2825 |
| Nigeria | B2 | 0.048632 | 0.100497 | 0.053297 | 0.3 |
| Norway | Aaa | 0 | 0.0472 | 0 | 0.22 |
| Oman | Ba3 | 0.031810 | 0.082062 | 0.034862 | 0.15 |
| Pakistan | B3 | 0.057482 | 0.110196 | 0.062996 | 0.35 |
| Panama | Baa1 | 0.014111 | 0.062665 | 0.015465 | 0.25 |
| Papua New Guinea | B2 | 0.048632 | 0.100497 | 0.053297 | 0.3 |
| Paraguay | Ba1 | 0.022084 | 0.071402 | 0.024202 | 0.1 |
| Peru | A3 | 0.010603 | 0.058821 | 0.011621 | 0.295 |
| Philippines | Baa2 | 0.016822 | 0.065636 | 0.018436 | 0.3 |
| Poland | A2 | 0.007494 | 0.055413 | 0.008213 | 0.19 |
| Portugal | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.21 |
| Qatar | Aa3 | 0.005342 | 0.053054 | 0.005854 | 0.1 |
| Ras Al Khaimah (Emirate of) | Aaa | 0 | 0.0472 | 0 | 0 |
| Romania | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.16 |
| Russia | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.2 |
| Rwanda | B2 | 0.048632 | 0.100497 | 0.053297 | 0.3 |
| Saint Lucia | NR | 0.0302 | 0.0803 | 0.0331 | 0.1698 |
| Saudi Arabia | A1 | 0.006219 | 0.054015 | 0.006815 | 0.2 |
| Senegal | Ba3 | 0.031810 | 0.082062 | 0.034862 | 0.3 |
| Serbia | Ba3 | 0.031810 | 0.082062 | 0.034862 | 0.15 |
| Sharjah | Baa2 | 0.016822 | 0.065636 | 0.018436 | 0 |
| Sierra Leone | NR | 0.079566 | 0.134398 | 0.087198 | 0.3 |
| Singapore | Aaa | 0 | 0.0472 | 0 | 0.17 |
| Slovakia | A2 | 0.007494 | 0.055413 | 0.008213 | 0.21 |
| Slovenia | A3 | 0.010603 | 0.058821 | 0.011621 | 0.19 |
| Solomon Islands | B3 | 0.057482 | 0.110196 | 0.062996 | 0.3 |
| Somalia | NR | 0.106035 | 0.163406 | 0.116206 | 0.2825 |
| South Africa | Ba2 | 0.026549 | 0.076295 | 0.029095 | 0.28 |
| South Korea | Aa2 | 0.004385 | 0.052006 | 0.004806 | 0.25 |
| Spain | Baa1 | 0.014111 | 0.062665 | 0.015465 | 0.25 |
| Sri Lanka | Caa1 | 0.066252 | 0.119807 | 0.072607 | 0.28 |
| St. Maarten | Baa3 | 0.019453 | 0.068519 | 0.021319 | 0.2736 |
| St. Vincent & the Grenadines | B3 | 0.057482 | 0.110196 | 0.062996 | 0.2736 |
| Sudan | NR | 0.175 | 0.238987 | 0.191787 | 0.35 |
| Suriname | Caa3 | 0.088336 | 0.144009 | 0.096809 | 0.36 |
| Swaziland | B3 | 0.057482 | 0.110196 | 0.062996 | 0.275 |
| Sweden | Aaa | 0 | 0.0472 | 0 | 0.214 |
| Switzerland | Aaa | 0 | 0.0472 | 0 | 0.1484 |
| Syria | NR | 0.175 | 0.238987 | 0.191787 | 0.28 |
| Taiwan | Aa3 | 0.005342 | 0.053054 | 0.005854 | 0.2 |
| Tajikistan | B3 | 0.057482 | 0.110196 | 0.062996 | 0.1912 |
| Tanzania | B2 | 0.048632 | 0.100497 | 0.053297 | 0.3 |
| Thailand | Baa1 | 0.014111 | 0.062665 | 0.015465 | 0.2 |
| Togo | B3 | 0.057482 | 0.110196 | 0.062996 | 0.2825 |
| Trinidad and Tobago | Ba1 | 0.022084 | 0.071402 | 0.024202 | 0.3 |
| Tunisia | B2 | 0.048632 | 0.100497 | 0.053297 | 0.25 |
| Turkey | B2 | 0.048632 | 0.100497 | 0.053297 | 0.22 |
| Turks and Caicos Islands | Baa1 | 0.014111 | 0.062665 | 0.015465 | 0 |
| Uganda | B2 | 0.048632 | 0.100497 | 0.053297 | 0.3 |
| Ukraine | B3 | 0.057482 | 0.110196 | 0.062996 | 0.18 |
| United Arab Emirates | Aa2 | 0.004385 | 0.052006 | 0.004806 | 0.55 |
| United Kingdom | Aa3 | 0.005342 | 0.053054 | 0.005854 | 0.19 |
| United States | Aaa | 0 | 0.0472 | 0 | 0.27 |
| Uruguay | B1 | 0.039783 | 0.090799 | 0.043599 | 0.25 |
| Venezuela | C | 0.175 | 0.238987 | 0.191787 | 0.34 |
| Vietnam | Ba3 | 0.031810 | 0.082062 | 0.034862 | 0.2 |
| Yemen | NR | 0.175 | 0.238987 | 0.191787 | 0.2825 |
| Zambia | Ca | 0.106035 | 0.163406 | 0.116206 | 0.35 |
| Zimbabwe | NR | 0.106035 | 0.163406 | 0.116206 | 0.24 |

### Regional averages (rows 185–193, + Global row 195) — used by the operating-regions ERP calculator

| Region | ERP | Default spread | Tax rate | CRP |
|---|---|---|---|---|
| Africa | 0.096642 | 0.045114 | 0.283142 | 0.049442 |
| Asia | 0.057468 | 0.009369 | 0.256958 | 0.010268 |
| Australia & New Zealand | 0.047233 | 0.0000298 | 0.297403 | 0.0000327 |
| Caribbean | 0.100313 | 0.048464 | 0.242518 | 0.053113 |
| Central and South America | 0.087100 | 0.036408 | 0.310394 | 0.039900 |
| Eastern Europe & Russia | 0.067981 | 0.018962 | 0.183075 | 0.020781 |
| Middle East | 0.062502 | 0.013962 | 0.329559 | 0.015302 |
| North America | 0.0472 | 0 | 0.269624 | 0 |
| Western Europe | 0.055597 | 0.007662 | 0.244065 | 0.008397 |
| Global | 0.057630 | 0.009517 | 0.261339 | 0.010430 |

---

## Sheets: Industry Average Beta (US) and (Global)

94 industry rows + "Total Market" and "Total Market (without financials)". Each sheet has 27 columns:

| # | Column | # | Column | # | Column |
|---|---|---|---|---|---|
| 1 | Industry Name | 10 | Std deviation in stock prices | 19 | Trailing PE |
| 2 | Number of firms | 11 | Pre-tax cost of debt | 20 | Non-cash WC %Rev |
| 3 | Annual Average Revenue growth (last 5 yrs) | 12 | Market Debt/Capital | 21 | CapEx %Rev |
| 4 | Pre-tax Operating Margin (Unadjusted) | 13 | Cost of capital | 22 | Net CapEx %Rev |
| 5 | After-tax ROC | 14 | Sales/Capital | 23 | Reinvestment Rate |
| 6 | Average effective tax rate | 15 | EV/Sales | 24 | ROE |
| 7 | Unlevered Beta | 16 | EV/EBITDA | 25 | Dividend Payout |
| 8 | Equity (Levered) Beta | 17 | EV/EBIT | 26 | Equity Reinvestment Rate |
| 9 | Cost of equity | 18 | Price/Book | 27 | Pre-tax Operating Margin (Lease & R&D adjusted) |

**Only columns 3, 4, 5, 7, 10, 13, 14, 15 are read by any formula in the workbook** (VLOOKUPs from Input sheet and Cost of capital worksheet). Those columns, verbatim (rounded 6 dp), for both sheets:

### Industry Average Beta (US) — A2:O95 key columns

| Industry | RevGrowth5y | PretaxMargin | AfterTaxROC | UnleveredBeta | StdDevStock | CostOfCapital | Sales/Cap | EV/Sales |
|---|---|---|---|---|---|---|---|---|
| Advertising | 0.083146 | 0.09979 | 0.515119 | 0.774409 | 0.577364 | 0.043416 | 5.168934 | 1.827975 |
| Aerospace/Defense | 0.052836 | 0.075558 | 0.191149 | 0.912411 | 0.348929 | 0.049464 | 2.605988 | 2.011768 |
| Air Transport | -0.068229 | -0.189906 | -0.160654 | 0.919622 | 0.461508 | 0.046113 | 0.883238 | 1.972802 |
| Apparel | -0.035553 | 0.054872 | 0.075423 | 0.941363 | 0.478436 | 0.050044 | 1.339131 | 2.025844 |
| Auto & Truck | 0.121917 | 0.019334 | 0.011709 | 1.049999 | 0.45237 | 0.056475 | 0.742704 | 3.58284 |
| Auto Parts | 0.04021 | 0.040099 | 0.064587 | 1.093811 | 0.431649 | 0.05744 | 1.822344 | 1.597395 |
| Bank (Money Center) | -0.007768 | 0 | -0.000133 | 0.598479 | 0.215882 | 0.02488 | 0.142835 | 5.316985 |
| Banks (Regional) | 0.088246 | 0 | -0.000811 | 0.600109 | 0.194833 | 0.029968 | 0.239305 | 4.472711 |
| Beverage (Alcoholic) | 0.1439 | 0.238743 | 0.144302 | 0.676031 | 0.37008 | 0.040875 | 0.63934 | 5.299532 |
| Beverage (Soft) | 0.27075 | 0.199771 | 0.267363 | 0.707455 | 0.49695 | 0.042249 | 1.374958 | 5.075069 |
| Broadcasting | 0.057983 | 0.192951 | 0.169217 | 0.653361 | 0.455576 | 0.040244 | 0.979946 | 2.080804 |
| Brokerage & Investment Banking | 0.095143 | 0.004212 | -0.0000290 | 0.576942 | 0.359028 | 0.032598 | 0.215965 | 4.930672 |
| Building Materials | 0.074733 | 0.108039 | 0.241657 | 0.970355 | 0.339932 | 0.051967 | 2.592457 | 1.995315 |
| Business & Consumer Services | 0.075334 | 0.088794 | 0.183299 | 0.830021 | 0.456454 | 0.046869 | 2.157163 | 2.965665 |
| Cable TV | 0.066987 | 0.181518 | 0.11087 | 0.700509 | 0.320159 | 0.041849 | 0.756996 | 3.852297 |
| Chemical (Basic) | 0.225073 | 0.072126 | 0.095261 | 0.761775 | 0.48059 | 0.044002 | 1.349574 | 1.517412 |
| Chemical (Diversified) | 0.28994 | 0.058127 | 0.059258 | 1.036068 | 0.361612 | 0.053487 | 1.031931 | 1.719351 |
| Chemical (Specialty) | 0.059354 | 0.120655 | 0.118414 | 0.818212 | 0.385413 | 0.046118 | 1.039151 | 3.273487 |
| Coal & Related Energy | -0.141845 | -0.087021 | -0.074964 | 0.562177 | 0.42274 | 0.035491 | 0.870192 | 1.082935 |
| Computer Services | 0.09404 | 0.075788 | 0.229802 | 0.940194 | 0.458909 | 0.050615 | 3.029834 | 1.432328 |
| Computers/Peripherals | 0.04061 | 0.15552 | 0.278169 | 1.139419 | 0.428664 | 0.061484 | 1.806351 | 5.14064 |
| Construction Supplies | 0.035024 | 0.09411 | 0.099328 | 0.872215 | 0.333908 | 0.047519 | 1.206776 | 2.265331 |
| Diversified | 0.005076 | 0.180642 | 0.134447 | 0.892924 | 0.299374 | 0.048769 | 0.792749 | 2.797347 |
| Drugs (Biotechnology) | 0.326399 | 0.095441 | 0.062192 | 0.851496 | 0.50102 | 0.047205 | 0.483365 | 8.734441 |
| Drugs (Pharmaceutical) | 0.326554 | 0.240201 | 0.203109 | 0.837279 | 0.554524 | 0.047509 | 0.814863 | 5.554598 |
| Education | 0.010089 | 0.092613 | 0.098892 | 1.070624 | 0.557267 | 0.055332 | 1.166878 | 2.806348 |
| Electrical Equipment | 0.042116 | 0.12602 | 0.221215 | 1.001356 | 0.551194 | 0.054309 | 1.80338 | 3.655559 |
| Electronics (Consumer & Office) | 0.016942 | 0.019904 | 0.046607 | 1.010825 | 0.549089 | 0.051572 | 1.820155 | 1.316629 |
| Electronics (General) | 0.028772 | 0.074672 | 0.110846 | 0.858211 | 0.438651 | 0.047615 | 1.48977 | 2.543668 |
| Engineering/Construction | 0.0357 | 0.041033 | 0.1485 | 0.955633 | 0.420426 | 0.050955 | 3.796458 | 0.899473 |
| Entertainment | 0.063537 | 0.074408 | 0.079646 | 0.838756 | 0.680622 | 0.048186 | 1.066304 | 6.808996 |
| Environmental & Waste Services | 0.078792 | 0.119172 | 0.191896 | 0.821935 | 0.504308 | 0.047814 | 1.630277 | 3.340837 |
| Farming/Agriculture | -0.007699 | 0.065549 | 0.091246 | 0.686112 | 0.452993 | 0.041671 | 1.475858 | 1.351616 |
| Financial Svcs. (Non-bank & Insurance) | 0.090828 | 0.123166 | 0.003987 | 0.109105 | 0.277386 | 0.021655 | 0.037411 | 31.486335 |
| Food Processing | 0.068488 | 0.127989 | 0.175309 | 0.532117 | 0.325572 | 0.034247 | 1.480116 | 2.193589 |
| Food Wholesalers | 0.120125 | 0.015585 | 0.08886 | 0.806676 | 0.580329 | 0.045119 | 5.8166 | 0.543616 |
| Furn/Home Furnishings | 0.050844 | 0.079793 | 0.145941 | 0.779488 | 0.405229 | 0.043595 | 1.878711 | 1.310845 |
| Green & Renewable Energy | -0.0009 | 0.261193 | 0.068934 | 0.678764 | 0.560417 | 0.042462 | 0.271028 | 13.152748 |
| Healthcare Products | 0.139001 | 0.142363 | 0.132184 | 0.800892 | 0.461895 | 0.046061 | 0.963177 | 7.418861 |
| Healthcare Support Services | 0.175439 | 0.049689 | 0.352718 | 0.738808 | 0.444916 | 0.04282 | 7.715434 | 0.682084 |
| Heathcare Information and Technology | 0.150239 | 0.1314 | 0.163522 | 0.753504 | 0.424486 | 0.04396 | 1.244529 | 7.333875 |
| Homebuilding | 0.135222 | 0.118118 | 0.135766 | 1.329031 | 0.365573 | 0.063534 | 1.365761 | 1.209195 |
| Hospitals/Healthcare Facilities | 0.042365 | 0.101951 | 0.13176 | 0.807725 | 0.492114 | 0.045946 | 1.512409 | 1.535518 |
| Hotel/Gaming | -0.003796 | -0.103381 | -0.052366 | 1.189825 | 0.436942 | 0.060851 | 0.381804 | 8.078257 |
| Household Products | 0.141768 | 0.181967 | 0.349908 | 0.683785 | 0.546567 | 0.040929 | 2.017032 | 4.093421 |
| Information Services | 0.121921 | 0.233952 | 0.243352 | 0.974619 | 0.423733 | 0.053963 | 1.14155 | 10.543643 |
| Insurance (General) | 0.055122 | 0.128313 | 0.09256 | 0.558785 | 0.30122 | 0.034935 | 0.819386 | 1.972744 |
| Insurance (Life) | 0.033451 | 0.084779 | 0.043332 | 0.64448 | 0.306765 | 0.035453 | 0.602094 | 1.310624 |
| Insurance (Prop/Cas.) | 0.030855 | 0.108474 | 0.107373 | 0.578196 | 0.229341 | 0.034522 | 1.105707 | 1.444217 |
| Investments & Asset Management | 0.006503 | 0.169491 | 0.072355 | 0.784933 | 0.28855 | 0.042471 | 0.453071 | 5.871516 |
| Machinery | 0.034397 | 0.130748 | 0.214219 | 0.957649 | 0.342806 | 0.052205 | 1.778686 | 3.063524 |
| Metals & Mining | 0.040199 | 0.114651 | 0.107496 | 0.819146 | 0.678403 | 0.047703 | 0.970985 | 2.996189 |
| Office Equipment & Services | 0.007836 | 0.075006 | 0.128391 | 0.834309 | 0.311116 | 0.044324 | 1.972114 | 1.119424 |
| Oil/Gas (Integrated) | -0.0124 | -0.042743 | -0.023337 | 0.987813 | 0.263884 | 0.053511 | 0.644972 | 1.535422 |
| Oil/Gas (Production and Exploration) | -0.01171 | -0.213985 | -0.063287 | 0.810794 | 0.562763 | 0.047032 | 0.307839 | 2.907511 |
| Oil/Gas Distribution | 0.107407 | 0.174321 | 0.0901 | 0.60255 | 0.407778 | 0.04018 | 0.543227 | 2.424865 |
| Oilfield Svcs/Equip. | -0.068566 | 0.00474 | 0.012933 | 0.835147 | 0.502675 | 0.046919 | 1.880141 | 0.734258 |
| Packaging & Container | 0.025224 | 0.096641 | 0.122487 | 0.682343 | 0.292155 | 0.040732 | 1.471769 | 1.716983 |
| Paper/Forest Products | 0.005061 | 0.058432 | 0.083773 | 0.959188 | 0.356696 | 0.050984 | 1.48211 | 0.943691 |
| Power | 0.010117 | 0.198205 | 0.068022 | 0.430899 | 0.198599 | 0.029034 | 0.38499 | 4.365478 |
| Precious Metals | 0.031651 | 0.214791 | 0.098744 | 0.752681 | 0.677634 | 0.043333 | 0.461318 | 4.816617 |
| Publishing & Newspapers | 0.003081 | 0.056434 | 0.104819 | 1.105893 | 0.374695 | 0.055802 | 2.094068 | 1.167241 |
| R.E.I.T. | 0.068084 | 0.232332 | 0.020494 | 0.794342 | 0.324047 | 0.045646 | 0.108943 | 12.853446 |
| Real Estate (Development) | -0.199248 | -0.036384 | -0.014133 | 0.564116 | 0.606959 | 0.035992 | 0.217054 | 5.997432 |
| Real Estate (General/Diversified) | 0.092042 | 0.069304 | 0.019559 | 0.758866 | 0.209932 | 0.038886 | 0.331154 | 6.814457 |
| Real Estate (Operations & Services) | 0.020951 | 0.041314 | 0.079711 | 0.755881 | 0.347217 | 0.042935 | 2.046669 | 1.562055 |
| Recreation | 0.026224 | 0.068107 | 0.08652 | 0.774219 | 0.563999 | 0.044631 | 1.424572 | 3.733091 |
| Reinsurance | 0.0911 | 0.042693 | 0.037434 | 1.128798 | 0.252283 | 0.051565 | 1.017237 | 0.807497 |
| Restaurant/Dining | 0.008369 | 0.113621 | 0.072401 | 1.110935 | 0.536255 | 0.059948 | 1.141299 | 5.268089 |
| Retail (Automotive) | 0.031979 | 0.06429 | 0.101017 | 0.989955 | 0.428188 | 0.05441 | 2.085486 | 1.235471 |
| Retail (Building Supply) | 0.064169 | 0.127885 | 0.374737 | 1.436453 | 0.406039 | 0.072977 | 3.463321 | 2.062228 |
| Retail (Distributors) | 0.046723 | 0.076995 | 0.116738 | 0.754493 | 0.419743 | 0.044696 | 1.683097 | 1.493973 |
| Retail (General) | 0.024121 | 0.046296 | 0.146735 | 0.815816 | 0.389109 | 0.045945 | 4.097281 | 0.934013 |
| Retail (Grocery and Food) | 0.062786 | 0.034779 | 0.09628 | 0.152225 | 0.377189 | 0.019808 | 4.113427 | 0.387768 |
| Retail (Online) | 0.092834 | 0.057373 | 0.110418 | 1.137691 | 0.528659 | 0.061421 | 1.8008 | 4.70689 |
| Retail (Special Lines) | 0.055706 | 0.028917 | 0.052896 | 1.036853 | 0.490095 | 0.054211 | 2.294483 | 1.100543 |
| Rubber& Tires | -0.042133 | -0.004966 | 0.000104 | 0.547996 | 0.438272 | 0.03609 | 1.06835 | 0.740633 |
| Semiconductor | 0.037705 | 0.240902 | 0.173907 | 0.961703 | 0.372553 | 0.053252 | 0.748002 | 7.159085 |
| Semiconductor Equip | 0.084925 | 0.222144 | 0.278925 | 1.06885 | 0.359055 | 0.056774 | 1.295517 | 5.143852 |
| Shipbuilding & Marine | 0.031014 | 0.051113 | 0.037414 | 0.744116 | 0.298302 | 0.043086 | 0.676179 | 1.739523 |
| Shoe | -0.001113 | 0.092155 | 0.208959 | 0.978275 | 0.315049 | 0.053337 | 2.504718 | 5.045832 |
| Software (Entertainment) | -0.004129 | 0.206104 | 0.147335 | 0.959545 | 0.626141 | 0.053718 | 0.679622 | 8.16276 |
| Software (Internet) | 0.19336 | 0.050594 | 0.066578 | 0.748983 | 0.327251 | 0.043604 | 1.005697 | 15.670514 |
| Software (System & Application) | 0.189275 | 0.233043 | 0.222771 | 0.894009 | 0.479706 | 0.050459 | 0.91831 | 11.823496 |
| Steel | 0.004723 | 0.035533 | 0.0581 | 0.784841 | 0.393192 | 0.042418 | 1.702717 | 0.934815 |
| Telecom (Wireless) | 0.065274 | 0.124817 | 0.102228 | 0.392854 | 0.397789 | 0.028881 | 0.837351 | 3.670172 |
| Telecom. Equipment | 0.316475 | 0.186873 | 0.217988 | 0.83219 | 0.431085 | 0.046667 | 1.202508 | 3.564183 |
| Telecom. Services | 0.07791 | 0.194566 | 0.137778 | 0.421809 | 0.435297 | 0.031999 | 0.751889 | 2.506385 |
| Tobacco | 0.528233 | 0.427991 | 0.453261 | 0.612708 | 0.244882 | 0.036542 | 1.15673 | 4.815429 |
| Transportation | 0.094161 | 0.062768 | 0.133171 | 0.786948 | 0.286762 | 0.044116 | 2.451574 | 1.556732 |
| Transportation (Railroads) | -0.0147 | 0.39125 | 0.129678 | 0.741134 | 0.16834 | 0.042708 | 0.397017 | 8.099944 |
| Trucking | 0.030642 | -0.028822 | -0.040357 | 0.945991 | 0.387838 | 0.050939 | 0.836361 | 2.729235 |
| Utility (General) | 0.022685 | 0.204033 | 0.067851 | 0.485585 | 0.184447 | 0.031304 | 0.37307 | 4.136622 |
| Utility (Water) | 0.127391 | 0.304629 | 0.080502 | 0.572902 | 0.359609 | 0.036711 | 0.298736 | 9.786175 |
| Total Market | 0.088604 | 0.096202 | 0.060506 | 0.748151 | 0.412054 | 0.043362 | 0.66747 | 3.646253 |
| Total Market (without financials) | 0.094041 | 0.099301 | 0.105844 | 0.861777 | 0.44773 | 0.048736 | 1.113748 | 3.196959 |

### Industry Average Beta (Global) — same industry list, key columns

| Industry | RevGrowth5y | PretaxMargin | AfterTaxROC | UnleveredBeta | StdDevStock | CostOfCapital | Sales/Cap | EV/Sales |
|---|---|---|---|---|---|---|---|---|
| Advertising | 0.049684 | 0.04637 | 0.093416 | 0.988281 | 0.372439 | 0.060432 | 2.140103 | 1.70769 |
| Aerospace/Defense | 0.078385 | 0.054749 | 0.114234 | 1.002481 | 0.325628 | 0.063361 | 2.11348 | 1.927151 |
| Air Transport | -0.026244 | -0.146403 | -0.092361 | 0.917789 | 0.32755 | 0.058678 | 0.64572 | 2.494585 |
| Apparel | -0.019447 | 0.078953 | 0.087542 | 0.853766 | 0.311841 | 0.055745 | 1.231962 | 2.903571 |
| Auto & Truck | 0.008959 | 0.026116 | 0.020198 | 1.011046 | 0.308261 | 0.062234 | 0.862867 | 1.526867 |
| Auto Parts | 0.018494 | 0.026241 | 0.034017 | 1.278855 | 0.299378 | 0.07368 | 1.381497 | 1.046965 |
| Bank (Money Center) | 0.084532 | 0.001954 | 0.000211 | 0.479302 | 0.211817 | 0.032375 | 0.122406 | 7.748114 |
| Banks (Regional) | 0.070974 | -0.000191 | -0.000311 | 0.541609 | 0.192597 | 0.030694 | 0.180619 | 4.941278 |
| Beverage (Alcoholic) | 0.073401 | 0.202723 | 0.114945 | 0.734154 | 0.242778 | 0.050411 | 0.677865 | 5.863689 |
| Beverage (Soft) | 0.063919 | 0.150044 | 0.198081 | 0.650912 | 0.312022 | 0.046371 | 1.472125 | 3.794832 |
| Broadcasting | 0.013249 | 0.147875 | 0.129623 | 0.685877 | 0.312318 | 0.048347 | 0.995529 | 1.797006 |
| Brokerage & Investment Banking | 0.083588 | 0.010291 | 0.001497 | 0.417081 | 0.296411 | 0.037102 | 0.194277 | 6.619303 |
| Building Materials | 0.019864 | 0.086164 | 0.122051 | 0.90934 | 0.275073 | 0.058347 | 1.664588 | 1.80972 |
| Business & Consumer Services | 0.073679 | 0.076074 | 0.161971 | 0.91306 | 0.322414 | 0.059131 | 2.452622 | 2.174791 |
| Cable TV | 0.018461 | 0.181206 | 0.112737 | 0.784631 | 0.306428 | 0.054887 | 0.730235 | 3.666179 |
| Chemical (Basic) | 0.056104 | 0.064869 | 0.0583 | 0.931175 | 0.285226 | 0.059322 | 1.042467 | 1.759117 |
| Chemical (Diversified) | 0.033375 | 0.038086 | 0.031248 | 1.048032 | 0.248874 | 0.063224 | 0.973325 | 1.367885 |
| Chemical (Specialty) | 0.053703 | 0.097073 | 0.088309 | 0.987684 | 0.302692 | 0.063461 | 1.061557 | 2.751614 |
| Coal & Related Energy | 0.065714 | 0.121829 | 0.105315 | 0.895941 | 0.408693 | 0.053998 | 0.924865 | 1.233318 |
| Computer Services | 0.061538 | 0.069187 | 0.191755 | 1.002572 | 0.310211 | 0.06304 | 3.211905 | 1.441639 |
| Computers/Peripherals | 0.005844 | 0.100616 | 0.150953 | 1.234927 | 0.315119 | 0.076827 | 1.652359 | 2.801669 |
| Construction Supplies | 0.037298 | 0.093248 | 0.09453 | 0.948901 | 0.287334 | 0.059018 | 1.158255 | 1.590479 |
| Diversified | 0.056422 | 0.124338 | 0.085535 | 0.732508 | 0.23451 | 0.048103 | 0.794487 | 1.815946 |
| Drugs (Biotechnology) | 0.248749 | 0.062091 | 0.04852 | 0.968539 | 0.456265 | 0.062379 | 0.48981 | 10.370147 |
| Drugs (Pharmaceutical) | 0.169831 | 0.168537 | 0.124955 | 0.92572 | 0.399173 | 0.060604 | 0.755963 | 4.383469 |
| Education | 0.127041 | 0.072132 | 0.075527 | 0.949946 | 0.326636 | 0.060626 | 1.092355 | 4.876808 |
| Electrical Equipment | 0.063009 | 0.056853 | 0.081676 | 1.057914 | 0.32303 | 0.065734 | 1.537208 | 2.340295 |
| Electronics (Consumer & Office) | 0.008118 | 0.048279 | 0.072057 | 1.145109 | 0.34395 | 0.066906 | 1.566464 | 1.077383 |
| Electronics (General) | 0.05039 | 0.061342 | 0.086882 | 1.245457 | 0.310363 | 0.074006 | 1.515814 | 1.891331 |
| Engineering/Construction | 0.037296 | 0.049305 | 0.088906 | 0.766754 | 0.292401 | 0.04767 | 2.015524 | 0.602765 |
| Entertainment | 0.084709 | 0.077101 | 0.087515 | 1.040906 | 0.394519 | 0.065825 | 1.159469 | 5.434875 |
| Environmental & Waste Services | 0.098499 | 0.103268 | 0.116238 | 0.867902 | 0.352469 | 0.057392 | 1.257121 | 2.79593 |
| Farming/Agriculture | 0.061948 | 0.067614 | 0.074183 | 0.707734 | 0.307172 | 0.049778 | 1.221944 | 1.446837 |
| Financial Svcs. (Non-bank & Insurance) | 0.089805 | 0.091703 | 0.005192 | 0.164209 | 0.296833 | 0.030299 | 0.066212 | 17.207044 |
| Food Processing | 0.070595 | 0.094159 | 0.139666 | 0.70733 | 0.26947 | 0.049113 | 1.721802 | 1.869758 |
| Food Wholesalers | 0.047614 | 0.018836 | 0.076941 | 0.541666 | 0.300935 | 0.041024 | 4.774107 | 0.446798 |
| Furn/Home Furnishings | 0.047407 | 0.071599 | 0.149483 | 1.024186 | 0.280933 | 0.061402 | 2.368731 | 1.677304 |
| Green & Renewable Energy | 0.120601 | 0.343662 | 0.072304 | 0.693474 | 0.311492 | 0.05033 | 0.235435 | 8.971672 |
| Healthcare Products | 0.121139 | 0.144706 | 0.131444 | 0.928424 | 0.383157 | 0.061063 | 0.964996 | 6.506149 |
| Healthcare Support Services | 0.128892 | 0.050154 | 0.265546 | 0.755186 | 0.332015 | 0.051181 | 6.243759 | 0.728469 |
| Heathcare Information and Technology | 0.157928 | 0.1288 | 0.14923 | 0.971336 | 0.401006 | 0.063834 | 1.184947 | 8.660473 |
| Homebuilding | 0.064338 | 0.10444 | 0.095043 | 1.158298 | 0.283329 | 0.067628 | 1.264356 | 1.212887 |
| Hospitals/Healthcare Facilities | 0.057737 | 0.092632 | 0.085372 | 0.657148 | 0.271749 | 0.047698 | 1.156761 | 2.66443 |
| Hotel/Gaming | -0.009498 | -0.057503 | -0.03028 | 0.847223 | 0.314613 | 0.055899 | 0.455782 | 5.260045 |
| Household Products | 0.05946 | 0.158203 | 0.223729 | 0.871788 | 0.352386 | 0.05787 | 1.588286 | 3.844776 |
| Information Services | 0.155749 | 0.201826 | 0.210926 | 1.141319 | 0.385407 | 0.072706 | 1.204379 | 9.665671 |
| Insurance (General) | 0.056345 | 0.084411 | 0.103025 | 0.660939 | 0.23272 | 0.042592 | 1.449514 | 1.044069 |
| Insurance (Life) | 0.093163 | 0.096786 | 0.107006 | 0.964689 | 0.238538 | 0.044422 | 1.299638 | 0.910687 |
| Insurance (Prop/Cas.) | 0.043125 | 0.083399 | 0.094468 | 0.654704 | 0.245122 | 0.043754 | 1.33431 | 1.03764 |
| Investments & Asset Management | 0.096098 | 0.171008 | 0.046153 | 0.549693 | 0.303699 | 0.041756 | 0.291737 | 5.789814 |
| Machinery | 0.035749 | 0.07818 | 0.095479 | 1.073356 | 0.273372 | 0.066476 | 1.405688 | 2.217153 |
| Metals & Mining | 0.155645 | 0.080992 | 0.086514 | 0.829009 | 0.538045 | 0.055474 | 1.101203 | 1.638759 |
| Office Equipment & Services | 0.031731 | 0.066815 | 0.106868 | 1.006404 | 0.293148 | 0.060535 | 1.908882 | 1.15856 |
| Oil/Gas (Integrated) | 0.007351 | 0.062526 | 0.045901 | 1.078487 | 0.247041 | 0.066593 | 0.853837 | 1.660873 |
| Oil/Gas (Production and Exploration) | 0.066731 | -0.07498 | -0.021942 | 0.931157 | 0.507114 | 0.062372 | 0.31876 | 2.782273 |
| Oil/Gas Distribution | 0.096824 | 0.167915 | 0.080683 | 0.646041 | 0.313148 | 0.049372 | 0.535138 | 2.376714 |
| Oilfield Svcs/Equip. | -0.022513 | 0.012733 | 0.021184 | 0.910161 | 0.376232 | 0.059361 | 1.646165 | 0.846273 |
| Packaging & Container | 0.028064 | 0.088048 | 0.101786 | 0.707192 | 0.286777 | 0.049794 | 1.354136 | 1.66419 |
| Paper/Forest Products | 0.032528 | 0.070263 | 0.053841 | 0.784383 | 0.294385 | 0.053026 | 0.870456 | 1.567223 |
| Power | 0.064164 | 0.133833 | 0.061485 | 0.510048 | 0.224127 | 0.03954 | 0.554484 | 2.439134 |
| Precious Metals | 0.358046 | 0.192546 | 0.143409 | 0.866806 | 0.547794 | 0.056817 | 0.77356 | 3.517192 |
| Publishing & Newspapers | -0.002898 | 0.053111 | 0.067448 | 0.841379 | 0.291339 | 0.05156 | 1.446 | 1.195614 |
| R.E.I.T. | 0.08602 | 0.331922 | 0.02877 | 0.657655 | 0.239918 | 0.04704 | 0.097125 | 13.479584 |
| Real Estate (Development) | 0.06888 | 0.173091 | 0.08284 | 0.522977 | 0.264384 | 0.039703 | 0.571031 | 1.854741 |
| Real Estate (General/Diversified) | 0.054101 | 0.162928 | 0.038878 | 0.59745 | 0.244007 | 0.042427 | 0.28406 | 3.348591 |
| Real Estate (Operations & Services) | 0.080427 | 0.232248 | 0.046013 | 0.534906 | 0.250259 | 0.042564 | 0.223438 | 6.459547 |
| Recreation | 0.004286 | 0.08048 | 0.06671 | 0.934607 | 0.332104 | 0.059264 | 0.946944 | 3.373054 |
| Reinsurance | 0.042927 | 0.037979 | 0.051771 | 1.25209 | 0.287912 | 0.069063 | 1.534487 | 0.66818 |
| Restaurant/Dining | -0.00529 | 0.060159 | 0.054161 | 0.903975 | 0.319635 | 0.06012 | 1.458856 | 3.365257 |
| Retail (Automotive) | 0.035019 | 0.048965 | 0.083952 | 0.819806 | 0.304837 | 0.055415 | 2.280771 | 0.958424 |
| Retail (Building Supply) | 0.028206 | 0.116237 | 0.249827 | 1.056717 | 0.281861 | 0.066853 | 2.778116 | 1.843848 |
| Retail (Distributors) | 0.066209 | 0.036528 | 0.05228 | 0.568299 | 0.291022 | 0.042763 | 1.675329 | 0.80827 |
| Retail (General) | -0.011408 | 0.043138 | 0.086637 | 0.836012 | 0.257279 | 0.055589 | 2.713833 | 0.964501 |
| Retail (Grocery and Food) | 0.037351 | 0.043094 | 0.11087 | 0.468996 | 0.219146 | 0.036105 | 3.396215 | 0.635442 |
| Retail (Online) | 0.133815 | 0.047502 | 0.086685 | 1.311422 | 0.398387 | 0.081464 | 1.759944 | 5.063374 |
| Retail (Special Lines) | 0.015053 | 0.034693 | 0.063931 | 0.958848 | 0.320354 | 0.060409 | 2.236089 | 1.304402 |
| Rubber& Tires | 0.003056 | 0.056216 | 0.044224 | 0.858695 | 0.256079 | 0.05455 | 0.999416 | 1.180229 |
| Semiconductor | 0.045546 | 0.181926 | 0.139578 | 1.432088 | 0.324003 | 0.087702 | 0.798218 | 5.955689 |
| Semiconductor Equip | 0.071497 | 0.188442 | 0.186074 | 1.73128 | 0.337036 | 0.1038 | 1.082622 | 5.575316 |
| Shipbuilding & Marine | 0.015927 | 0.081759 | 0.049673 | 0.763362 | 0.262904 | 0.051485 | 0.683929 | 1.927638 |
| Shoe | -0.058951 | 0.06258 | 0.094543 | 0.986242 | 0.293521 | 0.063543 | 1.720434 | 3.734927 |
| Software (Entertainment) | 0.081434 | 0.197799 | 0.139999 | 1.130081 | 0.423507 | 0.072605 | 0.726476 | 7.991227 |
| Software (Internet) | 0.238285 | 0.036441 | 0.055094 | 0.931567 | 0.347671 | 0.061149 | 1.262802 | 11.151366 |
| Software (System & Application) | 0.143663 | 0.198195 | 0.193069 | 1.061331 | 0.40586 | 0.068707 | 0.975721 | 10.192195 |
| Steel | 0.057177 | 0.044113 | 0.045429 | 0.933125 | 0.304028 | 0.058416 | 1.144438 | 0.987992 |
| Telecom (Wireless) | 0.011297 | 0.141722 | 0.08579 | 0.630423 | 0.26769 | 0.04611 | 0.736149 | 2.287421 |
| Telecom. Equipment | 0.087317 | 0.108117 | 0.124931 | 1.088683 | 0.342677 | 0.0669 | 1.214009 | 2.524688 |
| Telecom. Services | 0.099895 | 0.150805 | 0.102741 | 0.511808 | 0.291939 | 0.041686 | 0.79025 | 2.15999 |
| Tobacco | 0.118535 | 0.328051 | 0.185831 | 0.551038 | 0.246296 | 0.040632 | 0.678522 | 3.874372 |
| Transportation | 0.056397 | 0.058872 | 0.077663 | 0.767144 | 0.260184 | 0.051913 | 1.549888 | 1.528837 |
| Transportation (Railroads) | 0.017566 | 0.15267 | 0.052393 | 0.619091 | 0.172815 | 0.044643 | 0.398916 | 4.831799 |
| Trucking | 0.025367 | 0.014467 | 0.004465 | 0.806369 | 0.293824 | 0.054439 | 0.9951 | 1.743796 |
| Utility (General) | 0.025762 | 0.118628 | 0.066507 | 0.488038 | 0.177297 | 0.038392 | 0.695911 | 2.378706 |
| Utility (Water) | 0.084437 | 0.267861 | 0.072712 | 0.588925 | 0.273894 | 0.044349 | 0.324618 | 5.010387 |
| Total Market | 0.06617 | 0.080037 | 0.049432 | 0.791779 | 0.323568 | 0.051554 | 0.690571 | 2.663895 |
| Total Market (without financials) | 0.064141 | 0.083062 | 0.077235 | 0.894132 | 0.330758 | 0.05836 | 1.035133 | 2.305158 |

---

## Secondary sheets (derived / informational)

- **Stories to Numbers** — narrative sheet. Free-text "story" (A3) plus a table that mirrors assumptions and outputs from the other sheets (all formulas, no new logic). Note E13 "Marginal ROIC" = Diagnostics!B6; F12 terminal reinvestment rate = `M2/M40` (g/ROC = 0.02/0.0672 = 0.29762).
- **Diagnostics** — sanity checks.
  - B2/B3: invested capital at start/end. B4: the change over 10 yrs. B5: change in EBIT(1−t) over 10 yrs.
  - **B6 marginal ROIC = B5/B4** (0.43889 for Boeing — flags aggressive reinvestment efficiency). B7: ending ROIC.
  - B8 compounded average WACC `=(1/'Valuation output'!L13)^(1/10)-1`. B9: value/price.
  - B10 verdict text: `IF(B9="NA","Value is negative…", IF(B9>2,"Value seems high…", IF(B9<0.5,"Value seems low…"," ")))`. Rows 12–15: advice text.
- **Summary Sheet** — a re-derivation of the valuation in three blocks (income statement view, reinvestment view, discount view). Almost all cell echoes. **Known internal inconsistency:** its year-1 reinvestment `E16 =(B3−B2)/S2C` is NOT floored at zero. With declining year-1 revenues, its year-1 FCFF (−1,430.8) and value of operating assets F50 (70,605.3) therefore differ from the Valuation output sheet (−3,445.2 and 68,699.3). The Valuation output sheet is the authoritative one.
- **Trailing 12 month** — standalone helper to build TTM inputs: `TTM = Last 10K − first X months of last year + first X months of current year` (`E =B−C+D`) for revenues, EBIT, interest expense, etc.; effective tax rates computed as taxes/taxable income. Contains leftover data from a different (non-Boeing) company; not linked to the valuation.
- **Answer keys** — dropdown lists for data validation:
  - Yes/No; B/V; synthetic-rating firm type (1, 2); the 15 rating strings.
  - ERP choices: Will input / Country of incorporation / Operating countries / Operating regions.
  - Cost of debt: Direct input / Synthetic rating / Actual rating.
  - Beta approach: Direct input / Single Business(US) / Single Business(Global) / Multibusiness(US) / Multibusiness(Global).

---

## Outputs

| Output | Cell | Meaning | Boeing value |
|---|---|---|---|
| Terminal value | Valuation output B18 | FCFF_terminal/(WACC_terminal − g) | 106,021.86 |
| PV of terminal value | B19 | | 59,239.48 |
| PV of 10-yr FCFF | B20 | | 9,459.84 |
| Value of operating assets | B24 | failure-weighted | 68,699.32 |
| Value of equity | B29 | after debt, minorities, cash, holdings | 50,197.32 |
| Value of equity in common stock | B31 | after option overhang | 50,197.32 |
| **Estimated value per share** | **B33** | B31/shares | **88.69** |
| Price as % of value | B35 | 127.68/88.69 | 1.4397 (≈44% overvalued) |

## Worked example (Boeing, numbers currently in sheet)

1. Base year. Revenues 76,559; reported EBIT −2,102. R&D capitalization (5-yr life; current 3,219; past 3,269/3,179/4,626/3,331/3,047) gives research asset 10,258.2 and amortization 3,490.4. The EBIT adjustment is −271.4 → adjusted EBIT −2,373.4; margin −3.10%. Invested capital = −8,617 + 28,532 − 10,030 + 10,258.2 = 20,143.2. Sales/capital = 76,559/20,143.2 = 3.8007; ROIC = −11.78%.
2. Cost of capital.
   - Unlevered beta 0.91241 (Aerospace/Defense, US table). ERP 0.05343 (revenue-weighted operating regions).
   - Market equity = 566 × 127.68 = 72,266.9. Pre-tax cost of debt = 0.0085 + 0.0171 (Baa2/BBB) = 2.56%. Market debt = PV of a 722 annuity for 3 yrs plus a 28,532 balloon at 2.56% = 28,508.0.
   - Levered beta = 0.91241·(1 + 0.75·0.39447) = 1.18236. Cost of equity = 0.0085 + 1.18236·0.05343 = 7.167%. After-tax cost of debt = 2.56%·0.75 = 1.92%.
   - Weights 71.71% equity / 28.29% debt → **WACC 5.683%**.
3. Forecast: growth −10%, then +15% (yrs 2–5), fading to g = 2% (post-yr-10 rf override) by yr 10. Margin −5% in yr 1 converging to 5.475% by yr 3. Revenues: 68,903 → 170,108 (yr 10); terminal 173,510. EBIT yr 1 −3,445 (NOL builds to 3,445, burns off by yr 3). Reinvestment = Δrev/3.8007 (0 in yr 1 since revenue falls). FCFF: −3,445, −1,148, 1,083, 707, 813, 1,630, 2,614, 3,729, 4,918, 6,107.
4. WACC constant 5.683% yrs 1–5, fading to terminal 0.02+0.0472 = 6.72% by yr 10. Cumulated DF yr 10 = 0.558748.
5. Terminal: ROC = WACC = 6.72%; reinvestment rate g/ROC = 0.29762; terminal EBIT(1−t) = 7,124.7; terminal FCFF = 5,004.2; TV = 5,004.2/(0.0672−0.02) = 106,021.9; PV = 59,239.5. Sum PV = 68,699.3.
6. No failure adjustment (B47 = No). Equity = 68,699.3 − 28,532 + 10,030 = 50,197.3; no options → **value/share = 50,197.3/566 = 88.69** vs price 127.68 → price/value 1.44.

## Reimplementation notes (Python port)

**Inputs** (name : type, units):

- Identity: valuation_date : date; company, country, industry_us, industry_global : str. Industry strings must exactly match the table names.
- Base-year financials ($m): revenues, ebit, interest_expense, bv_equity, bv_debt, cash, cross_holdings, minority_interests : float. Prior-year values only feed the informational CAGR. years_since_10k : float.
- Market: shares : float (millions); price : float ($); riskfree : float; wacc_initial : float (or build it via the cost-of-capital module).
- Taxes: effective_tax_rate, marginal_tax_rate : float.
- Value drivers: growth_yr1, margin_yr1, cagr_yrs2_5, target_margin : float; convergence_year : int (1–10); sales_to_capital : float.
- Flags with sub-inputs: capitalize_rnd (rnd_life int ≤ 10, current and past R&D list); has_leases (current lease expense, commitments yrs 1–5, lump beyond yr 5); has_options (n_options, strike, maturity, sigma, dividend_yield).
- Overrides: stable_wacc_override; stable_roc_override; prob_failure (tie_to ∈ {B, V}, distress_pct); keep_effective_tax; nol_carryforward; rf_after_yr10; growth_override; trapped_cash (amount, foreign_tax_rate).
- Cost-of-capital module: beta_approach, direct_beta; erp_approach, direct_erp; debt_maturity; cod_approach, direct_cod, actual_rating, firm_type ∈ {1, 2}; convertible (bv, interest, maturity, mv); preferred (n, price, dps); revenue splits by country, region, or business.

**Outputs**: per-year vectors (growth, revenues, margin, EBIT, tax rate, EBIT(1−t), NOL, reinvestment, FCFF, WACC, DF, PV, invested capital, ROIC), terminal block, value of operating assets, equity value, value per share, price/value.

**Branches & edge cases**:
- Negative base earnings: base EBIT(1−t) = EBIT (no tax credit). NOL accumulates from forecast losses and shields later profits. When EBIT > 0, tax applies only to max(0, EBIT − prior NOL); exact rule: if EBIT < NOL_prev, tax = 0.
- Year-1 reinvestment floored at 0 when revenues shrink; years 2–10 NOT floored (negative reinvestment = capital release). Terminal reinvestment = 0 if g ≤ 0.
- Margin ramp: target if t > convergence_year; else linear from year-1 margin (the workbook switches the anchor to base-year margin for t ≥ 6 — only matters if convergence_year > 5).
- Growth/tax/WACC all fade linearly over years 6–10 to terminal values.
- Terminal WACC default = rf(terminal) + mature_market_ERP (0.0472), NOT literally rf+4.5%. Terminal ROC default = terminal WACC.
- Failure: V_op = V_going·(1−p) + proceeds·p, proceeds = pct × (book capital or V_going).
- Circular fixed points: (a) synthetic rating: cost of debt → lease PV → adjusted EBIT/interest → coverage → spread → cost of debt; iterate to convergence; (b) option value: option value → diluted stock price → option value.
- Synthetic-rating coverage sentinels: interest = 0 → 1,000,000 (AAA); EBIT < 0 → −100,000 (D/spread 0.1744). Firm-type 3 (financials) table is absent — raise or require direct input.
- Lookups: rating tables are lower-bound range lookups (use bisect on the ">" column); the actual-rating→spread list and industry/country tables must use exact-match on name.
- Country default spread added to cost of debt on top of company spread (0 for Aaa countries).
- Trapped cash: cash_adj = cash − trapped × (marginal_rate − foreign_rate) when override on.
- Iteration guardrail from sheet: Excel iterative calc must be on; a Python port should cap iterations and check convergence of (cost of debt, option value).
- Units: everything in the same currency-millions as inputs except per-share outputs.

# Damodaran — Motley Fool Presentation spreadsheets

### TeslaNov2021DIY.xlsx

**Purpose:** A "do-it-yourself" FCFF (free cash flow to the firm) DCF valuation of Tesla, dated 2021-11-01, built by Aswath Damodaran for a Motley Fool presentation. It is his standard young/growth-company valuation template (the "fcffsimpleginzu" family) with a simplified front-end ("Master Inputs") that reduces the whole valuation to five story levers: revenue growth, operating margin, investment efficiency (sales-to-capital), cost of capital, and probability of failure. Each lever is chosen from a menu of preset scenarios (e.g. "A4: $300 billion (Toyota & VW-like)") or entered directly. The engine is a 10-year, two-stage FCFF model with a terminal value, failure-probability adjustment, and dilution-adjusted Black-Scholes valuation of employee options. Helper sheets convert R&D to a capital asset, convert operating leases to debt, build a bottom-up cost of capital, assign a synthetic bond rating from interest coverage, and carry Damodaran's country ERP and industry-average datasets (Jan 2021 vintage).

**Workbook-level notes:**
- Units: $ millions throughout (shares in millions, per-share values in $).
- The workbook REQUIRES Excel iterative calculation to be enabled: the option value uses the estimated value/share, which itself subtracts the option value (deliberate circular reference). A Python port must solve this by fixed-point iteration.
- Sheets: `Master Inputs`, `Input sheet`, `Valuation output`, `Stories to Numbers`, `Diagnostics`, `Summary Sheet`, `Option value`, `Cost of capital worksheet`, `R& D converter`, `Operating lease converter`, `Country equity risk premiums`, `Synthetic rating`, `Industry Average Beta (US)`, `Industry Average Beta (Global)`, `Trailing 12 month`, `Answer keys`. All have content; none are empty stubs.
- Dependency chain: `Master Inputs` → `Input sheet` → (`R& D converter`, `Operating lease converter` adjustments) → `Valuation output` (+ `Option value`) → reporting sheets (`Stories to Numbers`, `Diagnostics`, `Summary Sheet`). `Cost of capital worksheet`, `Synthetic rating`, `Country equity risk premiums`, and the two Industry Average Beta sheets are the supporting estimation stack (in THIS workbook the valuation takes its cost of capital directly from Master Inputs, not from the cost-of-capital worksheet — see below).

---

## Sheet: Master Inputs (the DIY front-end)

Yellow cells (the only required inputs) are choice strings picked from dropdown menus; each is translated to a number by VLOOKUP into a scenario table on the same sheet.

**Inputs (current values):**
| Lever | Choice cell | Current choice | Resolved value cell | Formula | Current value |
|---|---|---|---|---|---|
| Growth: revenues in 2030 | B4 | "A6: Direct Input (Enter % growth rate)" | B5 | `=VLOOKUP(B4,D2:E7,2)` | 0.35 |
| Profitability: op. margin in 2025+ | B9 | "B7: Direct Input" | B10 | `=VLOOKUP(B9,D10:E16,2)` | 0.16 |
| Investment efficiency: sales/invested capital | B14 | "C7: Direct Input" | B15 | `=VLOOKUP(B14,D19:E25,2)` | 4 |
| Risk: initial cost of capital | B19 | "D6: Direct Input" | B20 | `=VLOOKUP(B19,D28:E33,2)` | 0.06 |
| Risk: probability of failure | B21 | "E1: No chance" | (resolved on Input sheet B47) | `=VLOOKUP('Master Inputs'!B21,'Master Inputs'!D36:E40,2)` | 0 |

Note: when a "Direct Input" choice is selected, the user edits the number in the E-column of the scenario table itself (E7, E16, E25, E33), which the VLOOKUP then returns. The direct-input rows currently hold 0.35, 0.16, 4, 0.06.

**Reference data (scenario menus, verbatim):**

Growth lever (D2:E7) — CAGR for next 5 years implied by 2030 revenue targets:
| Choice (D) | CAGR next 5 yrs (E) |
|---|---|
| A1: $100 billion (BMW-like) | 0.12 |
| A2: $150 billion (Ford & Honda-like) | 0.18 |
| A3: $200 billion (Daimler-like) | 0.225 |
| A4: $300 billion (Toyota & VW -like) | 0.30 |
| A5: $500 billion (20% auto market share) | 0.40 |
| A6: Direct Input (Enter % growth rate) | 0.35 |

Profitability lever (D10:E16) — target operating margin in 2025 and beyond:
| Choice (D) | Target operating margin (E) |
|---|---|
| B1: Auto Industry First Quartile | -0.0587 |
| B2: Auto Industry Median | 0.0301 |
| B3: Auto Industry Third Quartile | 0.0752 |
| B4: Technology Median | 0.1025 |
| B5: Software | 0.2124 |
| B6: FAANG Aggregate | 0.1987 |
| B7: Direct Input | 0.16 |

Investment-efficiency lever (D19:E25) — sales-to-capital ratio for first 5 years:
| Choice (D) | Sales to Capital, 1st 5 years (E) |
|---|---|
| C1: Auto Industry First Quartile | 0.75 |
| C2: Auto Industry Median | 1.37 |
| C3: Auto Industry Third Quartile | 2.42 |
| C4: Technology Median | 1.51 |
| C5: Software | 2.30 |
| C6: FAANG Aggregate | 1.27 |
| C7: Direct Input | 4 |

Cost-of-capital lever (D28:E33) — initial cost of capital:
| Choice (D) | Initial cost of capital (E) |
|---|---|
| D1: Automobile Median | 0.0524 |
| D2: Technology Median | 0.0716 |
| D3: All companies - First Quartile | 0.0457 |
| D4: All companies - Median | 0.0588 |
| D5: All companies - Third Quartile | 0.0701 |
| D6: Direct Input | 0.06 |

Failure lever (D36:E39):
| Choice (D) | Probability of failure (E) |
|---|---|
| E1: No chance | 0 |
| E2: 10% (Marginal profitability, High Debt) | 0.1 |
| E3: 20% (Money loser, High Debt) | 0.2 |
| E4: 50% (Low Growth, Money loser, High Debt) | 0.5 |

**Echo/feedback cells (computed):**
- B6 `='Valuation output'!L3` — year-10 revenues, 414,233.4
- B11 `='Valuation output'!L5` — year-10 EBIT, 66,277.3
- B16 `='Valuation output'!L40` — year-10 ROIC, 0.3424
- B24:B27 — echo the four resolved inputs from the Input sheet
- B30 `='Valuation output'!B29` — equity value, 692,626.9
- B31 `='Valuation output'!B33` — value/share, 571.29

---

## Sheet: Input sheet (full model inputs)

**Inputs — company/base-year block:**
| Label | Cell | Current value |
|---|---|---|
| Date of valuation | B1 | 2021-11-01 |
| Company name | B2 | Tesla |
| Country of incorporation | B5 | United States |
| Industry (US) | B6 | Auto & Truck |
| Industry (Global) | B7 | Auto & Truck |
| Revenues — this year / last year | B8 / C8 | 46,848 / 31,536 |
| Years since last 10K (D7:D9 header col) | D8, D9 | 0.75 |
| Operating income (EBIT) — this / last | B9 / C9 | 4,586 / 1,951 |
| Interest expense — this / last | B10 / C10 | 529 / 784 |
| Book value of equity — this / last | B11 / C11 | 28,494 / 23,679 |
| Book value of debt — this / last | B12 / C12 | 10,158 / 13,337 |
| Capitalize R&D? | B13 | "Yes" |
| Have operating lease commitments? | B14 | "No" |
| Cash & marketable securities — this / last | B15 / C15 | 16,095 / 19,384 |
| Cross holdings / non-operating assets | B16 | 0 |
| Minority interests | B17 | 0 |
| Shares outstanding (millions) | B18 | 1,123 |
| Current stock price | B19 | 1,200 |
| Effective tax rate | B20 | `=490/4087` = 0.119892 (hard-coded from Tesla's financials) |
| Marginal tax rate | B21 | 0.25 |

**Value drivers (pulled from Master Inputs):**
| Label | Cell | Formula | Value |
|---|---|---|---|
| Revenue CAGR next 5 yrs | B23 | `='Master Inputs'!B5` | 0.35 |
| Target pre-tax operating margin (label says year 10; convergence controlled by B25) | B24 | `='Master Inputs'!B10` | 0.16 |
| Year of convergence (margin reaches target in this year) | B25 | input | 5 |
| Sales/capital ratio years 1–5 | B27 | `=VLOOKUP('Master Inputs'!B14,'Master Inputs'!D19:E25,2)` | 4 |
| Sales/capital ratio years 6–10 | C27 | `=B27*(2/3)` | 2.6667 |

**Market numbers:** Riskfree rate B29 = 0.0156; Initial cost of capital B30 `='Master Inputs'!B20` = 0.06.

**Employee options:** Have options? B32 = "Yes"; number outstanding B33 = 101.62; average strike B34 = 69.04; average maturity B35 = 5.8; std dev of stock price B36 = 0.30.

**Default assumptions with override switches (Yes/No dropdowns):**
| # | Default | Override cell | Current | If-yes value cell | Current |
|---|---|---|---|---|---|
| 1 | Terminal cost of capital = riskfree + 4.5% | B40 | "No" | B41 (terminal WACC) | 0.05 |
| 2 | Terminal ROC = terminal cost of capital | B43 | "Yes" | B44 (terminal ROC) | 0.15 |
| 3 | No chance of failure | B46 | "Yes" | B47 = `=VLOOKUP('Master Inputs'!B21,'Master Inputs'!D36:E40,2)` | 0 |
| — | Distress proceeds tied to | B48 | "V" | ("B"=book value of capital, "V"=estimated fair value) | — |
| — | Distress proceeds as % of B or V | B49 | 0.5 | — | — |
| 4 | Effective tax rate → marginal rate by terminal year | B51 | "No" | (if "Yes": tax stays at effective rate) | — |
| 5 | No NOL carried forward | B53 | "No" | B54 (NOL into year 1) | 250 (inactive) |
| 6 | Perpetual growth = riskfree rate | B56 | "No" | B57 (perpetual growth) | 0.01 (inactive) |
| 7 | No trapped cash | B59 | "No" | B60 trapped cash = 140,000; B61 avg foreign tax rate = 0.15 (both inactive) |

Note the sign convention on override 4: "No" means the tax rate DOES migrate from effective to marginal; "Yes" freezes it at the effective rate.

**Computed feedback block (E19:K27, informational only):**
- I22 company revenue growth most recent year: `=IF(C8>0,(B8/C8)^(1/D8)-1,"NA")` = 0.6950 (annualizes using D8 = years since last 10K = 0.75).
- I23 current pre-tax margin `='Valuation output'!B4` = 0.120611; I24 sales/capital `=B8/'Valuation output'!B39` = 1.6841; I25 ROIC `='Valuation output'!B7/'Valuation output'!B39` = 0.178765.
- J-column = US industry averages, K-column = global, all via VLOOKUP into the Industry Average Beta sheets, e.g. J22 `=VLOOKUP(B6,'Industry Average Beta (US)'!A2:S95,3)` (revenue growth, col 3), J23 col 4 (pre-tax margin), J24 col 14 (sales/capital), J25 col 5 (after-tax ROC), J26 col 10 (std dev of stock), J27 col 13 (cost of capital). Same column indices for the Global sheet.
- J30/J31/J32 echo year-10 revenues / EBIT / ROIC from the Valuation output.

---

## Sheet: Valuation output (the DCF engine)

Layout: column B = base year, C:L = years 1–10, M = terminal year. Row-by-row:

**Row 2 — revenue growth rate:**
- C2 `='Input sheet'!B23` (0.35); D2:G2 `=C2` … (constant for years 1–5).
- H2:L2 decline linearly to the terminal rate: `H2 =G2-((G2-$M$2)/5)`, `I2 =G2-((G2-$M$2)/5)*2`, … `L2 =G2-((G2-$M$2)/5)*5` (so year 10 growth = terminal growth).
- M2 terminal growth `=IF('Input sheet'!B56="Yes",'Input sheet'!B57,'Input sheet'!B29)` → riskfree 0.0156 (no override).

**Row 3 — revenues:** B3 `='Input sheet'!B8`; each year `=prev*(1+g)`; M3 `=L3*(1+M2)`.

**Row 4 — EBIT margin:** B4 `=B5/B3` (base margin from ADJUSTED EBIT, see row 5) = 0.120611.
- Years 1–10 (t = year index in row 1): `=IF(t>B25_conv, target, target - ((target - base)/conv_year)*(conv_year - t))` — verbatim for C4: `=IF(C1>'Input sheet'!$B$25,'Input sheet'!$B$24,'Input sheet'!$B$24-(('Input sheet'!$B$24-$B$4)/'Input sheet'!$B$25)*('Input sheet'!$B$25-C1))`. I.e. linear interpolation from base margin to target margin over `Year of convergence` years, flat at target afterwards. M4 `=L4`.

**Row 5 — EBIT:** base B5 adds the converter adjustments:
`=IF(B14="Yes", IF(B13="Yes", B9 + lease_F32 + rd_D39, B9 + lease_F32), IF(B13="Yes", B9 + rd_D39, B9))` (B13 = capitalize R&D?, B14 = leases?; lease_F32 = 'Operating lease converter'!F32, rd_D39 = 'R& D converter'!D39). Here: 4,586 + 1,064.4 = 5,650.4. Years 1–10 and terminal: `=margin*revenues`. N5 `=M5-B5` (informational: change in EBIT).

**Row 6 — tax rate:** B6 `='Input sheet'!B20` (effective, 0.119892); C6:G6 constant `=prev`; H6:L6 migrate linearly to marginal: `=G6+($M$6-$G$6)/5` each year (cumulative via chaining); M6 `=IF('Input sheet'!B51="Yes",'Input sheet'!B20,'Input sheet'!B21)` → 0.25.

**Row 7 — EBIT(1−t) with NOL shelter:** B7 `=IF(B5>0,B5*(1-B6),B5)`.
Years 1–10 (example C7): `=IF(C5>0, IF(C5<B10, C5, C5-(C5-B10)*C6), C5)` — if EBIT ≤ 0, no tax; if positive but less than the NOL carried in (prior-year NOL balance, row 10), fully sheltered (no tax); else tax only the excess over the NOL. M7 `=M5*(1-M6)` (no NOL logic in terminal year).

**Row 8 — reinvestment:** years 1–10: `=(Rev_t − Rev_{t−1}) / SalesToCapital_t` (row 38). Terminal: M8 `=IF(M2>0,(M2/M40)*M7,0)` — reinvestment rate = g/ROC applied to after-tax EBIT, zero if terminal growth ≤ 0. N8 `=SUM(C8:M8)` (informational).

**Row 9 — FCFF:** `=EBIT(1−t) − reinvestment` each year incl. terminal.

**Row 10 — NOL balance:** B10 `=IF('Input sheet'!B53="Yes",'Input sheet'!B54,0)`. Each year (example C10): `=IF(C5<0, B10-C5, IF(B10>C5, B10-C5, 0))` — losses add to the NOL; positive EBIT draws it down to zero. (All zero in current run.)

**Row 12 — cost of capital:** C12 `='Input sheet'!B30` (0.06); D12:G12 `=prev`; H12:L12 `=prev-($G$12-$M$12)/5` (linear walk to terminal). M12 `=IF('Input sheet'!B40="Yes",'Input sheet'!B41,'Input sheet'!B29+0.045)` → 0.0156+0.045 = 0.0606.

**Row 13 — cumulated discount factor:** C13 `=1/(1+C12)`; then `=prev*(1/(1+r_t))`. L13 = 0.5574476.

**Row 14 — PV(FCFF):** `=FCFF_t * DF_t` for years 1–10.

**Terminal-value / equity block (column B):**
- B16 terminal cash flow `=M9` = 45,233.17
- B17 terminal cost of capital `=M12` = 0.0606
- B18 terminal value `=B16/(B17-M2)` = 45,233.17/(0.0606−0.0156) = 1,005,181.6
- B19 PV(terminal value) `=B18*L13` = 560,336.0 (discounted with the YEAR-10 cumulative factor)
- B20 PV of years 1–10 `=SUM(C14:L14)` = 126,353.9
- B21 sum of PV `=B19+B20` = 686,689.9
- B22 probability of failure `=IF('Input sheet'!B46="Yes",'Input sheet'!B47,0)` = 0
- B23 proceeds if firm fails `=IF('Input sheet'!B48="B",('Input sheet'!B11+'Input sheet'!B12)*'Input sheet'!B49, B21*'Input sheet'!B49)` — "B": distress% × (BV equity + BV debt); "V": distress% × going-concern operating value. = 343,344.95 (V-mode, unused since p=0)
- B24 value of operating assets `=B21*(1-B22)+B23*B22` = 686,689.9
- B25 − Debt `=IF('Input sheet'!B14="Yes",'Input sheet'!B12+'Operating lease converter'!C28,'Input sheet'!B12)` = 10,158
- B26 − Minority interests `='Input sheet'!B17` = 0
- B27 + Cash `=IF('Input sheet'!B59="YES",'Input sheet'!B15-'Input sheet'!B60*('Input sheet'!B21-'Input sheet'!B61),'Input sheet'!B15)` = 16,095 (trapped-cash haircut = trapped_cash × (marginal_tax − foreign_tax) when override is "YES")
- B28 + Non-operating assets `='Input sheet'!B16` = 0
- B29 value of equity `=B24-B25-B26+B27+B28` = 692,626.9
- B30 − value of options `=IF('Input sheet'!B32="No",0,'Option value'!D27)` = 51,070.25
- B31 equity in common stock `=B29-B30` = 641,556.7
- B32 shares `='Input sheet'!B18` = 1,123
- B33 value/share `=B31/B32` = **571.29**
- B34 price `='Input sheet'!B19` = 1,200
- B35 price as % of value `=B34/B33` = 2.1005 (i.e. price is 210% of value → overvalued on these inputs)

**Implied-variables block (rows 37–40):**
- Row 38 sales-to-capital: C38:G38 `='Input sheet'!B27` (4); H38:L38 `='Input sheet'!C27` (2.6667).
- Row 39 invested capital: base B39 `=IF(B14="Yes", IF(B13="Yes", BVE+BVD-Cash+lease_F33+rd_D35, BVE+BVD-Cash+lease_F33), IF(B13="Yes", BVE+BVD-Cash+rd_D35, BVE+BVD-Cash))` where lease_F33 = lease debt value, rd_D35 = value of research asset. Here 28,494+10,158−16,095+5,261.4 = 27,818.4. Years 1–10: `=prev + reinvestment_t`.
- Row 40 ROIC: `=EBIT(1−t)_t / InvestedCapital_t` per year; M40 terminal ROC `=IF('Input sheet'!B43="Yes",'Input sheet'!B44,'Valuation output'!L12)` → override active → 0.15.

---

## Sheet: Option value (dilution-adjusted Black–Scholes)

Values the employee options that are subtracted from equity. **Deliberately circular:** stock price input D2 `='Valuation output'!B33` (the model's own value/share, which subtracts D27 of this sheet). Excel resolves via iteration; a port must iterate to a fixed point.

**Inputs:**
- D2 stock price (S) = 571.2882 (circular, `='Valuation output'!B33`)
- D3 strike (K) `='Input sheet'!B34` = 69.04
- D4 maturity (T) `='Input sheet'!B35` = 5.8
- D5 σ `='Input sheet'!B36` = 0.30
- D6 dividend yield (q) = 0 (direct input)
- D7 riskfree (r) `='Input sheet'!B29` = 0.0156
- D8 # options (W) `='Input sheet'!B33` = 101.62
- D9 # shares (N) `='Input sheet'!B18` = 1,123

**Logic (verbatim):**
- C15 dilution-adjusted spot: `=(C13*F14+C26*F13)/(F14+F13)` → S_adj = (S·N + C·W)/(N + W) where C = value per option C26 (circular within the sheet too).
- F16 variance `=D5^2`; F18 "div-adj interest rate" `=F15-F17` (NOTE: this is riskfree − dividend yield; F15 is the T-bond rate).
- B20 d1 `=(LN(C15/C16)+(F18+(F16/2))*C17)/(((F16)^(0.5))*(C17^0.5))` = 3.39747
- B21 N(d1) `=NORMSDIST(B20)` = 0.99966
- B23 d2 `=B20-((F16^0.5)*(C17^(0.5)))` = 2.67497; B24 N(d2) = 0.99626
- C26 value per option `=((EXP((0-F17)*C17))*C15*B21-C16*(EXP((0-F15)*C17))*B24)` → C·= e^(−qT)·S_adj·N(d1) − K·e^(−rT)·N(d2) = 502.561
- D27 value of all options `=C26*D8` = 51,070.25

---

## Sheet: R& D converter (capitalize R&D)

Converts R&D from operating expense to a capital asset (straight-line amortization). Active because Input sheet B13 = "Yes".

**Inputs:** F6 amortization life = 5 years (max 10); F7 current-year R&D = 2,375; B11:B15 past R&D by year (−1…−5): 1,491; 1,390; 1,460; 1,378; 834. Year labels A12:A20 auto-extend: `=IF((0-A11)<$F$6,IF(A11>-1,,A11-1),)` (adds years −2, −3, … until the amortization life is covered; unused rows become 0).

**Logic:** for each year row (current = year 0 with unamortized fraction 1, past year −k):
- Unamortized portion C: `=IF(A<0,($F$6+A)/$F$6,0)` → (life − k)/life; current year C24 = 1.
- Unamortized value D = R&D × C.
- Amortization this year E: `=IF(A<0,B/$F$6,0)` → past_R&D/life (current year contributes no amortization).
- D35 value of research asset `=SUM(D24:D34)` = 5,261.4 (added to invested capital).
- D37 = E35 = current-year amortization `=SUM(E25:E34)` = 1,310.6.
- D39 adjustment to operating income `=F7-D37` = 2,375 − 1,310.6 = **+1,064.4** (added to EBIT).
- D40 tax effect `=D39*'Input sheet'!B21` = 266.1 (informational).

**Worked numbers (life = 5):**
- Unamortized fractions and values: year −1 → 0.8 (1,192.8); year −2 → 0.6 (834); year −3 → 0.4 (584); year −4 → 0.2 (275.6); year −5 → 0 (0).
- Research asset = 2,375 + 1,192.8 + 834 + 584 + 275.6 = 5,261.4.
- Amortization = 298.2 + 278 + 292 + 275.6 + 166.8 = 1,310.6.

---

## Sheet: Operating lease converter (leases → debt)

Inactive in this run (Input sheet B14 = "No") but fully populated with sample data.

**Inputs:** E4 current-year lease expense = 275.65; commitments B7:B11 years 1–5 = 209.2, 258.4, 228.7, 182.3, 153.5; B12 "6 and beyond" lump = 477.9. Discount rate C15 `='Cost of capital worksheet'!B25` (pre-tax cost of debt) = 0.0396.

**Logic:**
- D18 years embedded in the yr-6+ lump: `=IF(B12>0,ROUND(B12/AVERAGE(B7:B11),0),0)` = ROUND(477.9/206.42) = 2.
- Year 1–5 PV: `=B/(1+C15)^year`.
- Year 6+ annuity: B27 `=IF(B12>0,IF(D18>0,B12/D18,B12),0)` = 238.95/yr; C27 `=IF(D18>0,(B27*(1-(1+C15)^(-D18))/C15)/(1+$C$15)^5,B27/(1+C15)^6)` — annuity of B27 for D18 years, discounted back 5 years = 371.35.
- C28 debt value of leases `=SUM(C22:C27)` = 1,297.70.
- F31 depreciation on lease asset `=C28/(5+D18)` (straight line over 5+D18 yrs) = 185.386.
- F32 adjustment to operating earnings `=E4-F31` = **+90.264** (add to EBIT when active).
- F33 adjustment to total debt `=C28` = 1,297.70 (add to debt and invested capital when active). F34 = F31.

---

## Sheet: Cost of capital worksheet (standalone estimator)

Computes a bottom-up WACC. **In this workbook the DCF does NOT use this WACC** — the valuation's cost of capital comes from Master Inputs (0.06). This sheet still matters because its pre-tax cost of debt B25 feeds the Operating lease converter, and it demonstrates the full estimation stack.

**Inputs:**
| Label | Cell | Current |
|---|---|---|
| Shares outstanding | B6 | `='Input sheet'!B18` = 1,123 |
| Market price/share | B7 | `='Input sheet'!B19` = 1,200 |
| Approach for beta | B9 | "Multibusiness(Global)" (choices: Direct Input / Single Business(US) / Single Business(Global) / Multibusiness(US) / Multibusiness(Global)) |
| Direct-input levered beta | B10 | 1.2 (unused) |
| Riskfree rate | B12 | `='Input sheet'!B29` = 0.0156 |
| ERP approach | B13 | "Operating countries" (choices: Will Input / Country of Incorporation / Operating countries / Operating regions) |
| Direct-input ERP | B14 | 0.06 (unused) |
| BV straight debt | B18 | `='Input sheet'!B12` = 10,158 |
| Interest expense | B19 | `='Input sheet'!B10` = 529 |
| Average debt maturity | B20 | 3 |
| Cost-of-debt approach | B21 | "Actual rating" (choices: Direct Input / Synthetic Rating / Actual rating) |
| Direct-input pre-tax cost of debt | B22 | 0.04 (unused) |
| Actual rating | B23 | "Ba2/BB" |
| Type of company for synthetic rating (1=large mfg, 2=small/risky, 3=financial) | B24 | 1 |
| Marginal tax rate | B26 | `='Input sheet'!B21` = 0.25 |
| Convertible debt: BV / interest / maturity / MV | B28:B31 | 0,0,0,0 |
| Debt value of operating leases | B33 | `=IF('Input sheet'!B14="Yes",'Operating lease converter'!F33,0)` = 0 |
| Preferred: # shares / price / dividend per share | B36:B38 | 0 / 70 / 5 |

**Beta logic:**
- B11 unlevered beta: `=IF(B9="Single Business(US)",VLOOKUP('Input sheet'!B6,'Industry Average Beta (US)'!A2:G95,7),IF(B9="Multibusiness(US)",K48,IF(B9="Single Business(Global)",VLOOKUP('Input sheet'!B7,'Industry Average Beta (Global)'!A2:G95,7),'Cost of capital worksheet'!K64)))` → Multibusiness(Global) → K64 = 0.764437.
- Multibusiness calculators (G34:K48 US; G50:K64 Global): for each business segment enter name + revenues; `EV/Sales =VLOOKUP(name, beta_sheet, 15)`; `Estimated Value = revenues × EV/Sales`; `Unlevered Beta =VLOOKUP(name, beta_sheet, 7)`; company unlevered beta = value-weighted average of segment betas (K48/K64). Current segments: Auto & Truck rev 29,542 and Green & Renewable Energy rev 1,994. Global: EV/Sales 0.904405 / 6.757514 → values 26,717.9 / 13,474.5 → weighted beta K64 = 0.764437.
- C45 levered beta: `=IF(B9="Direct Input",B10,B11*(1+(1-B26)*(C48/B48)))` = 0.7644×(1+0.75×(10,510/1,347,600)) = 0.768909.

**ERP logic:**
- B15 ERP used: `=IF(B13="Will Input",B14,IF(B13="Country of Incorporation",VLOOKUP('Input sheet'!B5,'Country equity risk premiums'!A5:E190,4),IF(B13="Operating regions",K32,K18)))` → Operating countries → K18 = 0.0564702.
- Operating-countries calculator (G4:K18): rows of {country, revenues}; `ERP =VLOOKUP(country,'Country equity risk premiums'!$A$5:$D$190,4)`; weight = rev/total; K18 = Σ weight×ERP. Current: United States of America 15,207 @ 0.052; China 6,662 @ 0.058940; Rest of the World 9,667 @ 0.0618 (ERP entered directly); total 31,536 → weighted ERP 0.0564702. (The last two rows of each calculator are free-input rows.) NOTE: the lookup name "United States of America" only works because VLOOKUP is run without exact-match and the table is alphabetical; the country table's exact entry is "United States".
- Operating-regions calculator (G20:K32): same pattern using the regional ERP block at 'Country equity risk premiums' rows 194–202 (Africa…Western Europe). Current: Asia 7,440 (=3159+4281) @ 0.062130, North America 93,864 @ 0.052 → K32 = 0.052744.

**Cost of debt logic:**
- B25 pre-tax cost of debt: `=IF(B21="Direct Input",B22,IF(B21="Synthetic Rating",'Synthetic rating'!D13,B12+VLOOKUP('Cost of capital worksheet'!B23,'Synthetic rating'!G39:H53,2)))` → Actual rating "Ba2/BB" → 0.0156 + 0.024 = **0.0396**.
- C41 market value of straight debt (bond-pricing): `=B19*(1-(1+B25)^(-B20))/B25+B18/(1+B25)^B20` = 529×annuity(3.96%,3) + 10,158/(1.0396)^3 = 10,509.99.
- C42 straight-debt portion of convertible: same formula with B29/B30/B28 → 0. C43 lease debt = B33. C44 equity portion of convertible `=B31-C42`.

**WACC assembly (rows 47–50):**
- Market values: equity B48 `=B6*B7` = 1,347,600; debt C48 `=C41+C42+C43` = 10,509.99; preferred D48 `=B36*B37` = 0; capital E48 = 1,358,110.
- Weights row 49 = component/E48 → equity 0.992261, debt 0.007739.
- Component costs row 50: cost of equity B50 `=B12+C45*B15` = 0.0156+0.768909×0.0564702 = 0.059020; after-tax cost of debt C50 `=B25*(1-B26)` = 0.0297; preferred D50 `=B38/B37` = 0.071429.
- E50 cost of capital `=B49*B50+C49*C50+D49*D50` = **0.058793** (not wired into the DCF here).

---

## Sheet: Synthetic rating (interest coverage → rating → default spread)

**Inputs (auto-fed):**
- C4 firm type `='Cost of capital worksheet'!B24` = 1. Codes: 1 = large manufacturing, 2 = smaller/riskier, 3 = financial service.
- F5 EBIT `=IF('Input sheet'!B14="Yes",'Input sheet'!B9+'Operating lease converter'!F32,'Input sheet'!B9)` = 4,586.
- F6 interest expense `=IF('Input sheet'!B14="Yes",'Cost of capital worksheet'!B19+'Operating lease converter'!C28*'Operating lease converter'!C15,'Cost of capital worksheet'!B19)` = 529. When leases are active, lease debt × pre-tax cost of debt is added as imputed interest.
- F7 long-term riskfree `='Input sheet'!B29` = 0.0156.

**Logic:**
- D9 interest coverage ratio: `=IF(F6=0,1000000,IF(F5<0,-100000,F5/F6))` — zero interest → 1,000,000 (forces top rating); negative EBIT → −100,000 (forces D rating). Here 4,586/529 = 8.66919.
- D10 rating: `=IF(C4=1,VLOOKUP(D9,A19:D33,3),(IF(C4=2,VLOOKUP(D9,A38:D52,3),VLOOKUP(D9,F19:I33,3))))` → "Aaa/AAA". **Warning:** the financial-firm table F19:I33 is EMPTY in this workbook; firm type 3 would fail. Range-lookup semantics: VLOOKUP finds the largest lower-bound ≤ ratio (column A is the "greater than" threshold).
- D11 company default spread: same VLOOKUPs, column 4 → 0.0063.
- D12 country default spread: `=VLOOKUP('Input sheet'!B5,'Country equity risk premiums'!A5:C179,3)`. For "United States" this approximate-match lookup returns 0.0133509, not the true US spread of 0. The range stops at row 179, so the lookup lands on the last row ≤ "United States" within A5:A179. Reproduce this quirk or fix it deliberately.
- D13 estimated cost of debt: `=F7+D11+D12` = 0.0156+0.0063+0.0133509 = 0.0352509.

**Reference data (verbatim). Table 1 — large manufacturing firms (A19:D33), lookup on coverage ratio:**
| > | ≤ | Rating | Spread |
|---|---|---|---|
| -100000 | 0.199999 | D2/D | 0.151164 |
| 0.2 | 0.649999 | Caa/CCC | 0.113412 |
| 0.65 | 0.799999 | Ca2/CC | 0.086424 |
| 0.8 | 1.249999 | C2/C | 0.082 |
| 1.25 | 1.499999 | B3/B- | 0.05148 |
| 1.5 | 1.749999 | B2/B | 0.04212 |
| 1.75 | 1.999999 | B1/B+ | 0.0351 |
| 2 | 2.2499999 | Ba2/BB | 0.024 |
| 2.25 | 2.49999 | Ba1/BB+ | 0.02 |
| 2.5 | 2.999999 | Baa2/BBB | 0.0156 |
| 3 | 4.249999 | A3/A- | 0.012168 |
| 4.25 | 5.499999 | A2/A | 0.010764 |
| 5.5 | 6.499999 | A1/A+ | 0.00975 |
| 6.5 | 8.499999 | Aa2/AA | 0.0078 |
| 8.5 | 100000 | Aaa/AAA | 0.0063 |

**Table 2 — smaller and riskier firms (A38:D52); spreads reference Table 1 cells (identical spread values, different coverage thresholds):**
| > | ≤ | Rating | Spread |
|---|---|---|---|
| -100000 | 0.499999 | D2/D | 0.151164 |
| 0.5 | 0.799999 | Caa/CCC | 0.113412 |
| 0.8 | 1.249999 | Ca2/CC | 0.086424 |
| 1.25 | 1.499999 | C2/C | 0.082 |
| 1.5 | 1.999999 | B3/B- | 0.05148 |
| 2 | 2.499999 | B2/B | 0.04212 |
| 2.5 | 2.999999 | B1/B+ | 0.0351 |
| 3 | 3.499999 | Ba2/BB | 0.024 |
| 3.5 | 3.9999999 | Ba1/BB+ | 0.02 |
| 4 | 4.499999 | Baa2/BBB | 0.0156 |
| 4.5 | 5.999999 | A3/A- | 0.012168 |
| 6 | 7.499999 | A2/A | 0.010764 |
| 7.5 | 9.499999 | A1/A+ | 0.00975 |
| 9.5 | 12.499999 | Aa2/AA | 0.0078 |
| 12.5 | 100000 | Aaa/AAA | 0.0063 |

**Table 3 — rating → spread direct lookup (G38:H53), used by "Actual rating" cost-of-debt approach:**
| Rating | Spread |
|---|---|
| A1/A+ | 0.00975 |
| A2/A | 0.010764 |
| A3/A- | 0.012168 |
| Aa2/AA | 0.0078 |
| Aaa/AAA | 0.0063 |
| B1/B+ | 0.0351 |
| B2/B | 0.04212 |
| B3/B- | 0.05148 |
| Ba1/BB+ | 0.02 |
| Ba2/BB | 0.024 |
| Baa2/BBB | 0.0156 |
| C2/C | 0.113412 |
| Ca2/CC | 0.086424 |
| Caa/CCC | 0.082 |
| D2/D | 0.151164 |

(Note: in Table 3 the C2/C and Caa/CCC spreads are swapped relative to Tables 1–2 — reproduce as-is.)

---

## Sheet: Country equity risk premiums (reference data, Jan-2021 vintage)

B1 mature-market ERP = 0.052. For every country: `Equity Risk Premium (D) = $B$1 + Country Risk Premium (E)`; C = adjusted default spread (from Moody's rating); E = country risk premium (default spread scaled up for equity-market volatility — precomputed values, no formula in sheet); F = corporate tax rate. Lookups used elsewhere: col 3 (C, default spread) by the Synthetic rating sheet; col 4 (D, ERP) by the cost-of-capital calculators. A regional aggregate block sits at rows 193–202 (Africa … Western Europe) plus "Global" at row 204, used by the Operating-regions ERP calculator.

**Full country table (A4:F190, verbatim; ERP column D = 0.052 + CRP):**


| Country | Moody's rating | Adj. Default Spread | Equity Risk Premium | Country Risk Premium | Corporate Tax Rate |
|---|---|---|---|---|---|
| Abu Dhabi | Aa2 | 0.00414857 | 0.0568936 | 0.00489362 | 0.55 |
| Albania | B1 | 0.0376389 | 0.0963985 | 0.0443985 | 0.15 |
| Algeria | NA | 0.054384 | 0.116151 | 0.0641509 | 0.26 |
| Andorra (Principality of) | Baa2 | 0.0159154 | 0.0707737 | 0.0187737 | 0.1 |
| Angola | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.3 |
| Anguilla | NA | 0.0459509 | 0.106203 | 0.0542033 | 0.238808 |
| Antigua & Barbuda | NA | 0.0459509 | 0.106203 | 0.0542033 | 0.238808 |
| Argentina | Caa2 | 0.0752778 | 0.140797 | 0.088797 | 0.3 |
| Armenia | Ba3 | 0.030096 | 0.087501 | 0.035501 | 0.2 |
| Aruba | Baa1 | 0.0133509 | 0.0677486 | 0.0157486 | 0.25 |
| Australia | Aaa | 0 | 0.052 | 0 | 0.3 |
| Austria | Aa1 | 0.00331886 | 0.0559149 | 0.0039149 | 0.25 |
| Azerbaijan | Ba2 | 0.0251177 | 0.0816287 | 0.0296287 | 0.2 |
| Bahamas | Baa3 | 0.0184046 | 0.0737099 | 0.0217099 | 0 |
| Bahrain | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0 |
| Bangladesh | Ba3 | 0.030096 | 0.087501 | 0.035501 | 0.25 |
| Barbados | Caa1 | 0.0626812 | 0.125938 | 0.0739382 | 0.055 |
| Belarus | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.18 |
| Belgium | Aa3 | 0.00505372 | 0.0579613 | 0.00596132 | 0.29 |
| Belize | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.3236 |
| Benin | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.3 |
| Bermuda | A2 | 0.00709029 | 0.0603636 | 0.00836364 | 0 |
| Bolivia | Ba3 | 0.030096 | 0.087501 | 0.035501 | 0.25 |
| Bosnia and Herzegovina | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.1 |
| Botswana | A2 | 0.00709029 | 0.0603636 | 0.00836364 | 0.22 |
| Brazil | Ba2 | 0.0251177 | 0.0816287 | 0.0296287 | 0.34 |
| British Virgin Islands | NA | 0.0459509 | 0.106203 | 0.0542033 | 0.238808 |
| Brunei | NA | 0.00331886 | 0.0559149 | 0.0039149 | 0.185 |
| Bulgaria | Baa2 | 0.0159154 | 0.0707737 | 0.0187737 | 0.1 |
| Burkina Faso | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.28 |
| Cambodia | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.2 |
| Cameroon | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.33 |
| Canada | Aaa | 0 | 0.052 | 0 | 0.265 |
| Cape Verde | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0 |
| Cayman Islands | Aa3 | 0.00505372 | 0.0579613 | 0.00596132 | 0 |
| Channel Islands | NA | 0.00687424 | 0.0601088 | 0.00810879 | 0.25037 |
| Chile | A1 | 0.00588343 | 0.05894 | 0.00694004 | 0.27 |
| China | A1 | 0.00588343 | 0.05894 | 0.00694004 | 0.25 |
| Colombia | Baa2 | 0.0159154 | 0.0707737 | 0.0187737 | 0.33 |
| Congo (Democratic Republic of) | Caa1 | 0.0626812 | 0.125938 | 0.0739382 | 0.35 |
| Congo (Republic of) | Caa2 | 0.0752778 | 0.140797 | 0.088797 | 0.3236 |
| Cook Islands | B1 | 0.0376389 | 0.0963985 | 0.0443985 | 0.2843 |
| Costa Rica | B1 | 0.0376389 | 0.0963985 | 0.0443985 | 0.3 |
| Croatia | Ba2 | 0.0251177 | 0.0816287 | 0.0296287 | 0.18 |
| Cuba | Caa2 | 0.0752778 | 0.140797 | 0.088797 | 0.2724 |
| Curaçao | Baa1 | 0.0133509 | 0.0677486 | 0.0157486 | 0.22 |
| Cyprus | Ba2 | 0.0251177 | 0.0816287 | 0.0296287 | 0.125 |
| Czech Republic | Aa3 | 0.00505372 | 0.0579613 | 0.00596132 | 0.19 |
| Denmark | Aaa | 0 | 0.052 | 0 | 0.22 |
| Dominican Republic | Ba3 | 0.030096 | 0.087501 | 0.035501 | 0.27 |
| Ecuador | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.25 |
| Egypt | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.225 |
| El Salvador | B3 | 0.0753 | 0.1408 | 0.0888 | 0.3 |
| Estonia | A1 | 0.00588343 | 0.05894 | 0.00694004 | 0.2 |
| Ethiopia | B1 | 0.0376389 | 0.0963985 | 0.0443985 | 0.3 |
| Falkland Islands | NA | 0.0274145 | 0.0843379 | 0.0323379 | 0.310231 |
| Fiji | Ba3 | 0.030096 | 0.087501 | 0.035501 | 0.2 |
| Finland | Aa1 | 0.00331886 | 0.0559149 | 0.0039149 | 0.2 |
| France | Aa2 | 0.00414857 | 0.0568936 | 0.00489362 | 0.31 |
| Gabon | Caa1 | 0.0626812 | 0.125938 | 0.0739382 | 0.3 |
| Gambia | NA | 0.054384 | 0.116151 | 0.0641509 | 0.31 |
| Georgia | Ba2 | 0.0251177 | 0.0816287 | 0.0296287 | 0.15 |
| Germany | Aaa | 0 | 0.052 | 0 | 0.3 |
| Ghana | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.25 |
| Gibraltar | NA | 0.00687424 | 0.0601088 | 0.00810879 | 0.25037 |
| Greece | B1 | 0.0376389 | 0.0963985 | 0.0443985 | 0.28 |
| Greenland | NA | 0.00687424 | 0.0601088 | 0.00810879 | 0.25037 |
| Guatemala | Ba1 | 0.0208937 | 0.0766461 | 0.0246461 | 0.25 |
| Guernsey | Baa1 | 0.0133509 | 0.0677486 | 0.0157486 | 0 |
| Guinea | NA | 0.0835749 | 0.150584 | 0.0985842 | 0.2915 |
| Guinea-Bissau | NA | 0.054384 | 0.116151 | 0.0641509 | 0.2915 |
| Guyana | NA | 0.054384 | 0.116151 | 0.0641509 | 0.1864 |
| Haiti | NA | 0.0752778 | 0.140797 | 0.088797 | 0.1864 |
| Honduras | B1 | 0.0376389 | 0.0963985 | 0.0443985 | 0.25 |
| Hong Kong | Aa2 | 0.00414857 | 0.0568936 | 0.00489362 | 0.165 |
| Hungary | Baa3 | 0.0184046 | 0.0737099 | 0.0217099 | 0.09 |
| Iceland | A2 | 0.00709029 | 0.0603636 | 0.00836364 | 0.2 |
| India | Baa2 | 0.0159154 | 0.0707737 | 0.0187737 | 0.3 |
| Indonesia | Baa2 | 0.0159154 | 0.0707737 | 0.0187737 | 0.25 |
| Iran | NA | 0.054384 | 0.116151 | 0.0641509 | 0.2023 |
| Iraq | Caa1 | 0.0626812 | 0.125938 | 0.0739382 | 0.15 |
| Ireland | A2 | 0.00709029 | 0.0603636 | 0.00836364 | 0.125 |
| Isle of Man | Aa2 | 0.00414857 | 0.0568936 | 0.00489362 | 0 |
| Israel | A1 | 0.00588343 | 0.05894 | 0.00694004 | 0.23 |
| Italy | Baa3 | 0.0184046 | 0.0737099 | 0.0217099 | 0.24 |
| Ivory Coast | Ba3 | 0.030096 | 0.087501 | 0.035501 | 0.25 |
| Jamaica | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.25 |
| Japan | A1 | 0.00588343 | 0.05894 | 0.00694004 | 0.3062 |
| Jersey | A1 | 0.00588343 | 0.05894 | 0.00694004 | 0 |
| Jordan | B1 | 0.0376389 | 0.0963985 | 0.0443985 | 0.2 |
| Kazakhstan | Baa3 | 0.0184046 | 0.0737099 | 0.0217099 | 0.2 |
| Kenya | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.3 |
| Korea, D.P.R. | NA | 0.10032 | 0.170337 | 0.118337 | 0.231 |
| Kuwait | Aa2 | 0.00414857 | 0.0568936 | 0.00489362 | 0.15 |
| Kyrgyzstan | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.1 |
| Laos | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.2 |
| Latvia | A3 | 0.010032 | 0.0638337 | 0.0118337 | 0.2 |
| Lebanon | Caa2 | 0.0752778 | 0.140797 | 0.088797 | 0.17 |
| Liberia | NA | 0.14 | 0.217143 | 0.165143 | 0.2915 |
| Libya | NA | 0.0251177 | 0.0816287 | 0.0296287 | 0.2 |
| Liechtenstein | Aaa | 0 | 0.052 | 0 | 0.125 |
| Lithuania | A3 | 0.010032 | 0.0638337 | 0.0118337 | 0.15 |
| Luxembourg | Aaa | 0 | 0.052 | 0 | 0.2601 |
| Macao | Aa3 | 0.00505372 | 0.0579613 | 0.00596132 | 0.12 |
| Macedonia | Ba3 | 0.030096 | 0.087501 | 0.035501 | 0.1 |
| Madagascar | NA | 0.0460115 | 0.106275 | 0.0542747 | 0.2 |
| Malawi | NA | 0.054384 | 0.116151 | 0.0641509 | 0.3 |
| Malaysia | A3 | 0.010032 | 0.0638337 | 0.0118337 | 0.24 |
| Mali | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.2824 |
| Malta | A2 | 0.00709029 | 0.0603636 | 0.00836364 | 0.35 |
| Mauritius | Baa1 | 0.0133509 | 0.0677486 | 0.0157486 | 0.15 |
| Mexico | A3 | 0.010032 | 0.0638337 | 0.0118337 | 0.3 |
| Moldova | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.12 |
| Mongolia | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.25 |
| Montenegro | B1 | 0.0376389 | 0.0963985 | 0.0443985 | 0.09 |
| Montserrat | Baa3 | 0.0184046 | 0.0737099 | 0.0217099 | 0.2724 |
| Morocco | Ba1 | 0.0208937 | 0.0766461 | 0.0246461 | 0.31 |
| Mozambique | Caa2 | 0.0752778 | 0.140797 | 0.088797 | 0.32 |
| Myanmar | NA | 0.054384 | 0.116151 | 0.0641509 | 0.25 |
| Namibia | Ba2 | 0.0251177 | 0.0816287 | 0.0296287 | 0.32 |
| Netherlands | Aaa | 0 | 0.052 | 0 | 0.25 |
| Netherlands Antilles | NA | 0.0459509 | 0.106203 | 0.0542033 | 0.238808 |
| New Zealand | Aaa | 0 | 0.052 | 0 | 0.28 |
| Nicaragua | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.3 |
| Niger | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.3236 |
| Nigeria | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.3 |
| Norway | Aaa | 0 | 0.052 | 0 | 0.22 |
| Oman | Ba1 | 0.0208937 | 0.0766461 | 0.0246461 | 0.15 |
| Pakistan | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.3 |
| Palestinian Authority | NA | 0.013352 | 0.0677499 | 0.0157499 | 0.273658 |
| Panama | Baa1 | 0.0133509 | 0.0677486 | 0.0157486 | 0.25 |
| Papua New Guinea | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.3 |
| Paraguay | Ba1 | 0.0208937 | 0.0766461 | 0.0246461 | 0.1 |
| Peru | A3 | 0.010032 | 0.0638337 | 0.0118337 | 0.295 |
| Philippines | Baa2 | 0.0159154 | 0.0707737 | 0.0187737 | 0.3 |
| Poland | A2 | 0.00709029 | 0.0603636 | 0.00836364 | 0.19 |
| Portugal | Baa3 | 0.0184046 | 0.0737099 | 0.0217099 | 0.21 |
| Qatar | Aa3 | 0.00505372 | 0.0579613 | 0.00596132 | 0.1 |
| Ras Al Khaimah (Emirate of) | Caa1 | 0.0626812 | 0.125938 | 0.0739382 | 0 |
| Reunion | NA | 0.00858798 | 0.0621303 | 0.0101303 | 0.261175 |
| Romania | Baa3 | 0.0184046 | 0.0737099 | 0.0217099 | 0.16 |
| Russia | Baa3 | 0.0184046 | 0.0737099 | 0.0217099 | 0.2 |
| Rwanda | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.3 |
| Saint Lucia | NA | 0.0459509 | 0.106203 | 0.0542033 | 0.238808 |
| Saudi Arabia | A1 | 0.00588343 | 0.05894 | 0.00694004 | 0.2 |
| Senegal | Ba3 | 0.030096 | 0.087501 | 0.035501 | 0.3 |
| Serbia | Ba3 | 0.030096 | 0.087501 | 0.035501 | 0.15 |
| Sharjah | A3 | 0.010032 | 0.0638337 | 0.0118337 | 0 |
| Sierra Leone | NA | 0.0835749 | 0.150584 | 0.0985842 | 0.3 |
| Singapore | Aaa | 0 | 0.052 | 0 | 0.17 |
| Slovakia | A2 | 0.00709029 | 0.0603636 | 0.00836364 | 0.21 |
| Slovenia | Baa1 | 0.0133509 | 0.0677486 | 0.0157486 | 0.19 |
| Solomon Islands | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.3 |
| Somalia | NA | 0.10032 | 0.170337 | 0.118337 | 0.2915 |
| South Africa | Baa3 | 0.0184046 | 0.0737099 | 0.0217099 | 0.28 |
| South Korea | Aa2 | 0.00414857 | 0.0568936 | 0.00489362 | 0.25 |
| Spain | Baa1 | 0.0133509 | 0.0677486 | 0.0157486 | 0.25 |
| Sri Lanka | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.28 |
| St. Maarten | Baa3 | 0.0184046 | 0.0737099 | 0.0217099 | 0.35 |
| St. Vincent & the Grenadines | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.3 |
| Sudan | NA | 0.14 | 0.217143 | 0.165143 | 0.35 |
| Suriname | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.36 |
| Swaziland | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.275 |
| Sweden | Aaa | 0 | 0.052 | 0 | 0.214 |
| Switzerland | Aaa | 0 | 0.052 | 0 | 0.18 |
| Syria | NA | 0.10032 | 0.170337 | 0.118337 | 0.28 |
| Taiwan | Aa3 | 0.00505372 | 0.0579613 | 0.00596132 | 0.2 |
| Tajikistan | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.3019 |
| Tanzania | B1 | 0.0376389 | 0.0963985 | 0.0443985 | 0.3 |
| Thailand | Baa1 | 0.0133509 | 0.0677486 | 0.0157486 | 0.2 |
| Togo | B3 | 0.054384 | 0.116151 | 0.0641509 | 0.3236 |
| Trinidad and Tobago | Ba1 | 0.0208937 | 0.0766461 | 0.0246461 | 0.25 |
| Tunisia | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.25 |
| Turkey | B1 | 0.0376389 | 0.0963985 | 0.0443985 | 0.22 |
| Turks and Caicos Islands | Baa1 | 0.0133509 | 0.0677486 | 0.0157486 | 0 |
| Uganda | B2 | 0.0460115 | 0.106275 | 0.0542747 | 0.3 |
| Ukraine | Caa1 | 0.0626812 | 0.125938 | 0.0739382 | 0.18 |
| United Arab Emirates | Aa2 | 0.00414857 | 0.0568936 | 0.00489362 | 0.55 |
| United Kingdom | Aa2 | 0.00414857 | 0.0568936 | 0.00489362 | 0.19 |
| United States | Aaa | 0 | 0.052 | 0 | 0.25 |
| Uruguay | B1 | 0.0376389 | 0.0963985 | 0.0443985 | 0.25 |
| Venezuela | C | 0.15 | 0.228939 | 0.176939 | 0.34 |
| Vietnam | Ba3 | 0.030096 | 0.087501 | 0.035501 | 0.2 |
| Yemen | NA | 0.10032 | 0.170337 | 0.118337 | 0.2 |
| Zambia | Caa2 | 0.0752778 | 0.140797 | 0.088797 | 0.35 |
| Zimbabwe | NA | 0.10032 | 0.170337 | 0.118337 | 0.25 |

**Regional aggregate block (rows 193–202 + Global, verbatim):**
| Region | ERP | Default Spread | Tax rate | CRP |
|---|---|---|---|---|
| Africa | 0.0988809 | 0.0397433 | 0.284916 | 0.0468809 |
| Asia | 0.0621303 | 0.00858798 | 0.261175 | 0.0101303 |
| Australia & New Zealand | 0.0520325 | 2.75402e-05 | 0.297489 | 3.24861e-05 |
| Caribbean | 0.106203 | 0.0459509 | 0.238808 | 0.0542033 |
| Central and South America | 0.0847932 | 0.0278005 | 0.309565 | 0.0327932 |
| Eastern Europe & Russia | 0.0733833 | 0.0181277 | 0.183598 | 0.0213833 |
| Middle East | 0.0677499 | 0.013352 | 0.273658 | 0.0157499 |
| North America | 0.052 | 0 | 0.251155 | 0 |
| Western Europe | 0.0601088 | 0.00687424 | 0.25037 | 0.00810879 |
| Global | 0.0618 | 0.0083 | 0.257 | 0.0098 |

(Regional ERP = 0.052 + regional CRP, same formula as countries.)

---

## Sheets: Industry Average Beta (US) and (Global) — reference data, Jan-2021 vintage

Two identically structured sheets: header in row 1, 94 industry rows (rows 2–95), plus "Total Market" (row 96) and "Total Market (without financials)" (row 97). 27 columns A–AA. Column indices used by lookups elsewhere: 3 = revenue growth, 4 = pre-tax operating margin (unadjusted), 5 = after-tax ROC, 7 = unlevered beta, 10 = std deviation in stock prices, 13 = cost of capital, 14 = sales/capital, 15 = EV/Sales. Full tables are reproduced below (US first, then Global).

**Industry Average Beta (US) — full table:**

| Industry Name | Number of firms | Annual Average Revenue growth - Last 5 years | Pre-tax Operating Margin (Unadjusted) | After-tax ROC | Average effective tax rate | Unlevered Beta | Equity (Levered) Beta | Cost of equity | Std deviation in stock prices | Pre-tax cost of debt | Market Debt/Capital | Cost of capital | Sales/Capital | EV/Sales | EV/EBITDA | EV/EBIT | Price/Book | Trailing PE | Non-cash WC as % of Revenues | Cap Ex as % of Revenues | Net Cap Ex as % of Revenues | Reinvestment Rate | ROE | Dividend Payout Ratio | Equity Reinvestment Rate | Pre-tax Operating Margin (Lease & R&D adjusted) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Advertising | 47 | 0.189846 | 0.120716 | 0.635138 | 0.241449 | 0.934953 | 1.43961 | 0.0940598 | 0.623768 | 0.0367 | 0.459705 | 0.0634734 | 5.43193 | 1.93895 | 9.20147 | 15.1177 | 5.98243 | 23.7713 | 0.000522772 | 0.0221029 | 0.0689634 | 0.653833 | 0.260839 | 1.01335 | 1.01335 | 0.121978 |
| Aerospace/Defense | 77 | 0.0352607 | 0.113667 | 0.33933 | 0.190634 | 1.07852 | 1.23158 | 0.0832424 | 0.387396 | 0.0327 | 0.195361 | 0.0717713 | 3.1505 | 2.26617 | 14.9367 | 19.7666 | 6.09057 | 44.2645 | 0.374736 | 0.0279057 | 0.0583023 | 1.04366 | 0.314203 | 0.441441 | 0.441441 | 0.117474 |
| Air Transport | 18 | 0.0484167 | 0.11601 | 0.13692 | 0.230401 | 0.843673 | 1.43535 | 0.0938381 | 0.317396 | 0.0327 | 0.508425 | 0.0585976 | 1.50452 | 1.33929 | 6.53698 | 12.0031 | 2.34292 | 10.5494 | 0.0116183 | 0.107702 | 0.0542979 | 0.613293 | 0.282028 | 0.150777 | 0.150777 | 0.111615 |
| Apparel | 51 | -0.0256372 | 0.105761 | 0.163391 | 0.156068 | 0.829641 | 1.0551 | 0.074065 | 0.511019 | 0.0367 | 0.294623 | 0.0603533 | 1.71571 | 1.89135 | 10.9302 | 17.5649 | 3.72598 | 54.5722 | 0.23726 | 0.0251563 | 0.0178647 | 0.304881 | 0.167233 | 0.430542 | 0.430542 | 0.107138 |
| Auto & Truck | 13 | 0.143133 | 0.0340754 | 0.0289103 | 0.0554399 | 0.525735 | 1.09507 | 0.0761439 | 0.350189 | 0.0327 | 0.622538 | 0.0440091 | 0.874448 | 1.25975 | 14.3869 | 36.5548 | 1.81866 | 16.7637 | -0.0553929 | 0.0945006 | 0.0508809 | 1.18369 | 0.124287 | 0.515764 | 0.515764 | 0.0351051 |
| Auto Parts | 46 | 0.0498103 | 0.0724212 | 0.170002 | 0.185176 | 0.946994 | 1.21097 | 0.0821704 | 0.50433 | 0.0367 | 0.33715 | 0.0637467 | 2.46311 | 0.754592 | 6.38228 | 10.184 | 1.94772 | 17.5804 | 0.126199 | 0.0430824 | 0.0619002 | 1.02999 | 0.125642 | 0.263059 | 0.263059 | 0.0743658 |
| Bank (Money Center) | 7 | 0.02112 | 0 | -0.000255435 | 0.17744 | 0.559541 | 1.00086 | 0.0712449 | 0.177446 | 0.0272 | 0.639962 | 0.0387061 | 0.204238 | 7.27849 | NA | NA | 1.27092 | 10.2265 | NA | 0.0149986 | 0.0149986 | NA | 0.128027 | 0.274011 | 0.274011 | -0.00155086 |
| Banks (Regional) | 611 | 0.101348 | 0 | -0.000626013 | 0.203302 | 0.431316 | 0.566983 | 0.0486831 | 0.182632 | 0.0272 | 0.386201 | 0.0377601 | 0.25787 | 5.95447 | NA | NA | 1.37391 | 15.407 | NA | 0.0350678 | 0.00615837 | NA | 0.120479 | 0.297694 | 0.297694 | -0.00294126 |
| Beverage (Alcoholic) | 21 | 0.107733 | 0.221133 | 0.149476 | 0.183891 | 0.918883 | 1.12634 | 0.0777694 | 0.424625 | 0.0367 | 0.238267 | 0.0657979 | 0.723915 | 4.61831 | 16.3246 | 20.8745 | 2.99355 | 38.6911 | 0.166109 | 0.0725224 | 0.0549354 | 0.416128 | 0.0688449 | 0.670036 | 0.670036 | 0.221113 |
| Beverage (Soft) | 34 | 0.307464 | 0.204009 | 0.262071 | 0.0975579 | 1.09071 | 1.2189 | 0.0825826 | 0.570769 | 0.0367 | 0.161344 | 0.0736994 | 1.32999 | 4.88142 | 19.9207 | 23.7306 | 8.04826 | 39.869 | -0.0769179 | 0.0470228 | 0.0876013 | 0.485116 | 0.402494 | 0.574387 | 0.574387 | 0.20528 |
| Broadcasting | 27 | 0.095402 | 0.21993 | 0.21471 | 0.0724389 | 0.729937 | 1.21368 | 0.0823113 | 0.326515 | 0.0327 | 0.4961 | 0.0536435 | 1.13449 | 2.71681 | 9.05843 | 12.4436 | 2.07923 | 8.55694 | 0.216198 | 0.0275552 | 0.295251 | 1.66266 | 0.933947 | 0.381473 | 0.381473 | 0.218308 |
| Brokerage & Investment Banking | 39 | 0.0665925 | 0.00546403 | 0.00039983 | 0.199629 | 0.567674 | 1.46092 | 0.0951676 | 0.273616 | 0.0327 | 0.728547 | 0.0437012 | 0.198119 | 6.16838 | NA | NA | 1.27345 | 18.0495 | NA | 0.0780335 | 0.0743579 | -71.6864 | 0.140569 | 0.222122 | 0.222122 | 0.0023069 |
| Building Materials | 42 | 0.123069 | 0.090145 | 0.186537 | 0.248259 | 1.01853 | 1.23165 | 0.0832457 | 0.307784 | 0.0327 | 0.242849 | 0.0689854 | 2.41607 | 1.6043 | 12.2797 | 17.3552 | 3.98765 | 25.4176 | 0.159149 | 0.0281018 | 0.0182734 | 0.301025 | 0.140514 | 0.267456 | 0.267456 | 0.0922139 |
| Business & Consumer Services | 165 | 0.0956941 | 0.101863 | 0.21937 | 0.202369 | 0.894887 | 1.06592 | 0.074628 | 0.437973 | 0.0367 | 0.232572 | 0.0636731 | 2.27747 | 2.39144 | 13.9954 | 22.5666 | 5.00267 | 47.5383 | 0.14663 | 0.034753 | 0.0114244 | 0.216463 | 0.102364 | 0.738226 | 0.738226 | 0.105042 |
| Cable TV | 14 | 0.0377857 | 0.179466 | 0.121462 | 0.212187 | 0.776608 | 1.11457 | 0.0771574 | 0.250275 | 0.0327 | 0.375671 | 0.0573849 | 0.792367 | 3.43857 | 10.12 | 18.5517 | 2.61124 | 80.572 | 0.014944 | 0.111887 | 0.165752 | 1.24403 | 0.117557 | 0.231506 | 0.231506 | 0.179305 |
| Chemical (Basic) | 43 | 0.0678218 | 0.0829804 | 0.116816 | 0.258776 | 0.992957 | 1.36683 | 0.090275 | 0.519584 | 0.0367 | 0.379216 | 0.0664792 | 1.50218 | 1.29995 | 8.24158 | 15.4015 | 2.11544 | 16.1102 | 0.160894 | 0.0551762 | 0.0592333 | 0.757195 | 0.0915734 | 0.908624 | 0.908624 | 0.083326 |
| Chemical (Diversified) | 6 | -0.047995 | 0.107489 | 0.117845 | 0.230997 | 1.21472 | 1.85286 | 0.115549 | 0.359186 | 0.0327 | 0.440278 | 0.0754731 | 1.23649 | 1.35188 | 7.93929 | 12.5254 | 1.89233 | 10.4804 | 0.199968 | 0.0566172 | 0.00469553 | 0.0657999 | 0.100651 | 0.627214 | 0.627214 | 0.108142 |
| Chemical (Specialty) | 94 | 0.0678219 | 0.125682 | 0.129296 | 0.254287 | 0.964857 | 1.13519 | 0.0782299 | 0.483612 | 0.0367 | 0.22195 | 0.066976 | 1.12504 | 2.09079 | 10.5642 | 16.3776 | 2.61177 | 25.3383 | 0.163265 | 0.0512554 | 0.0470132 | 0.611031 | 0.0568456 | 0.639942 | 0.639942 | 0.128948 |
| Coal & Related Energy | 22 | -0.116871 | 0.0663012 | 0.126968 | 0.0265271 | 1.04866 | 1.3959 | 0.091787 | 0.547092 | 0.0367 | 0.443489 | 0.0632875 | 1.8585 | 0.616618 | 2.2516 | 6.3252 | 0.857999 | 10.2957 | 0.0593591 | 0.0792542 | -0.00849059 | 0.126521 | 0.11589 | 0.168122 | 0.168122 | 0.0689866 |
| Computer Services | 106 | 0.158277 | 0.0764594 | 0.248914 | 0.247606 | 0.952866 | 1.20302 | 0.0817572 | 0.455214 | 0.0367 | 0.308653 | 0.0650183 | 3.36575 | 1.28184 | 10.3615 | 15.9199 | 3.80761 | 29.1332 | 0.127705 | 0.0146252 | 0.109103 | 1.7986 | 0.172869 | 0.521356 | 0.521356 | 0.0810886 |
| Computers/Peripherals | 48 | -0.0192068 | 0.155053 | 0.226412 | 0.158016 | 1.64008 | 1.74801 | 0.110096 | 0.504059 | 0.0367 | 0.134131 | 0.099021 | 1.51981 | 3.22658 | 15.1291 | 20.7986 | 11.0269 | 28.9187 | -0.0812867 | 0.0351092 | 0.00673555 | 0.093064 | 0.399929 | 0.26844 | 0.26844 | 0.158573 |
| Construction Supplies | 44 | 0.04333 | 0.119259 | 0.159809 | 0.221468 | 1.1036 | 1.36362 | 0.0901084 | 0.299071 | 0.0327 | 0.286415 | 0.0713244 | 1.56861 | 1.68191 | 10.4987 | 13.9779 | 3.40804 | 39.5809 | 0.150842 | 0.0516588 | 0.0440329 | 0.650852 | 0.247774 | 0.285463 | 0.285463 | 0.120892 |
| Diversified | 23 | 0.15158 | 0.137161 | 0.115546 | 0.178984 | 1.24848 | 1.40185 | 0.0920963 | 0.38157 | 0.0327 | 0.237569 | 0.0760435 | 0.907165 | 2.44624 | 12.9207 | 17.8435 | 1.93084 | 22.7752 | 0.055529 | 0.0569748 | 0.0279702 | 0.286042 | 0.0786002 | 0.182226 | 0.182226 | 0.136532 |
| Drugs (Biotechnology) | 503 | 0.318941 | 0.112548 | 0.0864186 | 0.148777 | 1.38917 | 1.43345 | 0.0937395 | 0.674473 | 0.0442 | 0.127265 | 0.0860285 | 0.428418 | 7.32804 | 13.2942 | 45.7683 | 7.07862 | 77.5556 | 0.131363 | 0.0404415 | 0.0958966 | 1.64062 | -0.0093674 | 0.0010228 | 0.0010228 | 0.202392 |
| Drugs (Pharmaceutical) | 267 | 0.317205 | 0.24854 | 0.182928 | 0.131935 | 1.28566 | 1.36159 | 0.0900027 | 0.771367 | 0.0692 | 0.12991 | 0.0850528 | 0.7622 | 5.4364 | 14.5655 | 21.0764 | 6.33194 | 58.1835 | 0.206699 | 0.0515716 | 0.0947033 | 0.435607 | 0.215081 | 0.613941 | 0.613941 | 0.243367 |
| Education | 35 | 0.027605 | 0.0875006 | 0.10845 | 0.284794 | 1.35601 | 1.6056 | 0.102691 | 0.376441 | 0.0327 | 0.251944 | 0.0829978 | 1.31131 | 2.58734 | 14.4607 | 29.2665 | 2.5098 | 22.1956 | 0.123051 | 0.0519965 | 0.0579713 | 1.21318 | 0.128999 | 0.0455849 | 0.0455849 | 0.0884273 |
| Electrical Equipment | 113 | 0.091217 | 0.136098 | 0.255953 | 0.180884 | 1.30712 | 1.44474 | 0.0943267 | 0.536717 | 0.0367 | 0.173526 | 0.0827348 | 1.89756 | 2.56049 | 12.8184 | 17.788 | 4.84666 | 29.8498 | 0.197323 | 0.0444274 | 0.055372 | 0.537539 | 0.20082 | 0.367956 | 0.367956 | 0.140336 |
| Electronics (Consumer & Office) | 20 | 0.0586073 | -0.0126683 | -0.0211714 | 0.627762 | 1.25079 | 1.27542 | 0.0855217 | 0.621705 | 0.0367 | 0.171278 | 0.0755881 | 1.87492 | 0.914238 | 15.6468 | NA | 2.75539 | 64.2358 | 0.173047 | 0.0171734 | 0.00197841 | NA | -0.101115 | 0 | 0 | -0.011983 |
| Electronics (General) | 153 | 0.0785503 | 0.0887208 | 0.139738 | 0.186796 | 1.07092 | 1.15096 | 0.0790498 | 0.427786 | 0.0367 | 0.154246 | 0.0711023 | 1.62763 | 1.99255 | 13.0737 | 21.6885 | 3.27268 | 125.824 | 0.211439 | 0.0537266 | 0.0666631 | 1.06024 | 0.112911 | 0.246695 | 0.246695 | 0.0918448 |
| Engineering/Construction | 54 | 0.08433 | 0.0389248 | 0.145544 | 0.245076 | 1.32504 | 1.5973 | 0.10226 | 0.331927 | 0.0327 | 0.281978 | 0.0803401 | 3.9179 | 0.702528 | 9.75265 | 16.427 | 1.86604 | 18.7076 | 0.177374 | 0.0177737 | 0.0280322 | 1.18652 | 0.0342603 | 0.368619 | 0.368619 | 0.0410213 |
| Entertainment | 107 | 0.0804774 | 0.135234 | 0.185727 | 0.20408 | 1.2017 | 1.33319 | 0.0885257 | 0.555724 | 0.0367 | 0.167123 | 0.0783311 | 1.40634 | 4.7188 | 21.8499 | 34.9127 | 3.70206 | 47.684 | 0.0249329 | 0.0527891 | 0.0819356 | 0.832119 | 0.176602 | 0.221392 | 0.221392 | 0.134586 |
| Environmental & Waste Services | 82 | 0.210257 | 0.120986 | 0.200015 | 0.20966 | 1.04851 | 1.26851 | 0.0851623 | 0.443353 | 0.0367 | 0.240626 | 0.0712933 | 1.69405 | 3.0814 | 13.9297 | 24.9131 | 4.28959 | 735.049 | 0.0995212 | 0.083942 | 0.0569546 | 0.537994 | 0.106822 | 0.534611 | 0.534611 | 0.123167 |
| Farming/Agriculture | 31 | 0.000246875 | 0.0401772 | 0.0627303 | 0.211758 | 0.627451 | 0.893625 | 0.0656685 | 0.46876 | 0.0367 | 0.384196 | 0.0510139 | 1.58685 | 1.07768 | 13.9157 | 23.7612 | 2.54616 | 73.1894 | 0.115061 | 0.0355022 | 0.0289374 | 1.33057 | 0.0914145 | 0.562444 | 0.562444 | 0.0419758 |
| Financial Svcs. (Non-bank & Insurance) | 232 | 0.108685 | 0.0750974 | 0.00234588 | 0.198305 | 0.0982631 | 0.732438 | 0.0572868 | 0.257033 | 0.0327 | 0.898189 | 0.0278605 | 0.0370255 | 30.1547 | NA | NA | 2.22394 | 83.0045 | NA | 0.0824342 | 0.0836743 | 2.02924 | 0.000748642 | 0.159593 | 0.159593 | 0.0739654 |
| Food Processing | 88 | 0.0423644 | 0.120044 | 0.155549 | 0.148159 | 0.696808 | 0.875322 | 0.0647167 | 0.315291 | 0.0327 | 0.272078 | 0.0537815 | 1.36497 | 2.29865 | 14.2641 | 18.841 | 2.58115 | 42.2544 | 0.0652594 | 0.0360662 | 0.0277294 | 0.278686 | 0.0190313 | 3.03822 | 3.03822 | 0.121807 |
| Food Wholesalers | 17 | 0.228563 | 0.0271518 | 0.168246 | 0.191663 | 0.657766 | 0.868023 | 0.0643372 | 0.315806 | 0.0327 | 0.305332 | 0.0521812 | 6.78007 | 0.599284 | 13.9497 | 22.2224 | 5.92796 | 47.9826 | 0.0724285 | 0.0118032 | 0.0243378 | 1.13877 | 0.155129 | 0.506394 | 0.506394 | 0.0269104 |
| Furn/Home Furnishings | 35 | 0.0971258 | 0.0708735 | 0.133571 | 0.2203 | 0.818327 | 1.0766 | 0.075183 | 0.433843 | 0.0367 | 0.325925 | 0.05965 | 1.96154 | 1.1087 | 9.26938 | 14.8028 | 2.20523 | 14.7933 | 0.132747 | 0.0326308 | 0.0485466 | 0.865416 | 0.169746 | 0.242196 | 0.242196 | 0.0741312 |
| Green & Renewable Energy | 22 | 0.194825 | 0.118191 | 0.0139347 | 0.326611 | 0.593773 | 1.07233 | 0.0749613 | 0.537612 | 0.0367 | 0.529711 | 0.0498337 | 0.164531 | 9.93816 | 17.1519 | 123.234 | 1.68254 | 26.2347 | 0.030935 | 0.382586 | 0.411499 | 8.13495 | -0.0580012 | 0.00116329 | 0.00116329 | 0.0859127 |
| Healthcare Products | 242 | 0.134012 | 0.15001 | 0.158687 | 0.124964 | 0.981819 | 1.04297 | 0.0734344 | 0.530857 | 0.0367 | 0.11697 | 0.0680643 | 1.02642 | 5.94234 | 22.6697 | 37.5535 | 5.12799 | 84.4262 | 0.24304 | 0.0512371 | 0.0621508 | 0.708652 | 0.0977604 | 0.302721 | 0.302721 | 0.159911 |
| Healthcare Support Services | 128 | 0.184398 | 0.0436915 | 0.379104 | 0.235952 | 0.946238 | 1.17032 | 0.0800566 | 0.499545 | 0.0367 | 0.285236 | 0.0650727 | 9.69445 | 0.690101 | 11.7377 | 16.0462 | 2.86154 | 51.6405 | -0.0517866 | 0.00757614 | 0.0514886 | 1.67866 | 0.131568 | 0.383733 | 0.383733 | 0.0426265 |
| Heathcare Information and Technology | 129 | 0.181705 | 0.12578 | 0.143964 | 0.132981 | 1.1527 | 1.24492 | 0.0839358 | 0.53864 | 0.0367 | 0.127908 | 0.0767204 | 1.1438 | 5.41341 | 23.4917 | 40.4565 | 5.28324 | 99.8107 | 0.221438 | 0.0399205 | 0.0453198 | 0.591056 | 0.111717 | 0.0853847 | 0.0853847 | 0.130715 |
| Homebuilding | 32 | 0.336442 | 0.101517 | 0.112524 | 0.235598 | 0.664056 | 0.827682 | 0.0622395 | 0.365507 | 0.0327 | 0.306532 | 0.0506788 | 1.3314 | 1.21095 | 10.9454 | 11.8867 | 1.62776 | 16.2609 | 0.730804 | 0.00819527 | 0.0128931 | 0.560976 | 0.152565 | 0.072612 | 0.072612 | 0.101846 |
| Hospitals/Healthcare Facilities | 36 | 0.0520177 | 0.107595 | 0.153125 | 0.214821 | 0.625562 | 1.22174 | 0.0827303 | 0.426321 | 0.0367 | 0.565559 | 0.0515084 | 1.59131 | 1.62732 | 9.37358 | 15.5993 | 6.31566 | 38.9376 | 0.122745 | 0.0636446 | 0.0353508 | 0.552939 | 0.621268 | 0.23617 | 0.23617 | 0.104025 |
| Hotel/Gaming | 65 | 0.0835058 | 0.192202 | 0.116395 | 0.174184 | 0.914445 | 1.26161 | 0.0848037 | 0.341034 | 0.0327 | 0.360655 | 0.0630639 | 0.715765 | 3.78455 | 12.7368 | 20.314 | 3.85276 | 134.204 | 0.0785061 | 0.0957319 | 0.0493881 | 0.398085 | 0.162283 | 0.543047 | 0.543047 | 0.185883 |
| Household Products | 127 | 0.17417 | 0.174304 | 0.281812 | 0.269204 | 0.937057 | 1.03001 | 0.0727604 | 0.509069 | 0.0367 | 0.146559 | 0.0661308 | 1.7127 | 3.73656 | 16.5724 | 21.3176 | 8.19988 | 33.2277 | 0.0878202 | 0.0410995 | 0.0517124 | 0.332654 | 0.105949 | 1.5258 | 1.5258 | 0.174922 |
| Information Services | 69 | 0.131213 | 0.282827 | 0.415243 | 0.188607 | 1.03152 | 1.09313 | 0.0760427 | 0.377976 | 0.0327 | 0.106238 | 0.0705695 | 1.58593 | 9.17459 | 26.352 | 32.2503 | 6.5808 | 46.227 | 0.0718181 | 0.0319405 | 0.170975 | 0.805242 | 0.305232 | 0.249126 | 0.249126 | 0.285516 |
| Insurance (General) | 19 | 0.0779873 | 0.121845 | 0.0961165 | 0.214215 | 0.592699 | 0.742626 | 0.0578165 | 0.31002 | 0.0327 | 0.292856 | 0.0480669 | 0.9323 | 1.95312 | 10.2657 | 15.8931 | 1.47934 | 67.5718 | -0.0966732 | 0.00753401 | 0.0382901 | 0.493615 | 0.0741846 | 0.420469 | 0.420469 | 0.122876 |
| Insurance (Life) | 24 | 0.0149925 | 0.132884 | 0.0819954 | 0.198223 | 0.732481 | 1.07615 | 0.0751598 | 0.251282 | 0.0327 | 0.49367 | 0.0501629 | 0.724038 | 1.36066 | 9.53289 | 10.2326 | 0.711842 | 21.0522 | 0.0703106 | 0.00160411 | 0.00230159 | 0.0974226 | 0.104388 | 0.260681 | 0.260681 | 0.132884 |
| Insurance (Prop/Cas.) | 51 | 0.0705019 | 0.106735 | 0.104777 | 0.197808 | 0.589072 | 0.678286 | 0.0544708 | 0.217098 | 0.0272 | 0.208605 | 0.0473635 | 1.13559 | 1.48506 | 11.396 | 13.8029 | 1.53287 | 29.5968 | -0.518544 | 0.0119763 | 0.00626343 | 0.136032 | 0.10584 | 0.358173 | 0.358173 | 0.107328 |
| Investments & Asset Management | 192 | 0.00895367 | 0.17458 | 0.0731413 | 0.172617 | 0.860183 | 1.02729 | 0.0726193 | 0.278759 | 0.0327 | 0.352353 | 0.0556731 | 0.460215 | 4.58174 | 21.9754 | 25.7863 | 1.67588 | 79.9366 | NA | 0.0347386 | 0.0828054 | 0.607789 | 0.133138 | 0.493283 | 0.493283 | 0.171736 |
| Machinery | 120 | 0.0350013 | 0.138397 | 0.244941 | 0.223309 | 1.09852 | 1.24702 | 0.0840449 | 0.353917 | 0.0327 | 0.192633 | 0.0725794 | 1.98101 | 2.58163 | 13.878 | 18.3478 | 4.0896 | 36.0983 | 0.233962 | 0.0290055 | 0.087753 | 0.89461 | 0.200299 | 0.280018 | 0.280018 | 0.140963 |
| Metals & Mining | 92 | 0.148425 | 0.112764 | 0.112565 | 0.532921 | 1.08657 | 1.31028 | 0.0873347 | 0.73255 | 0.0442 | 0.276462 | 0.0723547 | 1.01092 | 2.039 | 9.58415 | 17.4348 | 1.85936 | 727.096 | 0.162187 | 0.106549 | 0.0281305 | 0.384112 | 0.0327011 | 2.0298 | 2.0298 | 0.113576 |
| Office Equipment & Services | 22 | 0.0373857 | 0.0884924 | 0.174774 | 0.229397 | 1.24423 | 1.64528 | 0.104755 | 0.312796 | 0.0327 | 0.354343 | 0.0763257 | 2.2488 | 1.20362 | 8.76806 | 13.286 | 2.96226 | 34.5346 | 0.0954872 | 0.0326977 | 0.0119193 | 0.21577 | 0.182211 | 0.385725 | 0.385725 | 0.0915674 |
| Oil/Gas (Integrated) | 4 | -0.064775 | 0.0732639 | 0.0535896 | 0.302511 | 1.11747 | 1.30065 | 0.0868336 | 0.286224 | 0.0327 | 0.211476 | 0.0736568 | 0.959939 | 1.60663 | 9.1727 | 21.7428 | 1.40515 | 22.6721 | 0.0432428 | 0.104771 | 0.071228 | 1.37089 | 0.0784834 | 0.890736 | 0.890736 | 0.0739611 |
| Oil/Gas (Production and Exploration) | 269 | -0.0372693 | 0.198702 | 0.0903142 | 0.193668 | 1.07671 | 1.47822 | 0.0960674 | 0.593651 | 0.0367 | 0.360568 | 0.0713532 | 0.463944 | 2.71154 | 4.89466 | 13.2854 | 1.18988 | 8.66002 | 0.0197859 | 0.455587 | 0.142586 | 0.791709 | 0.063623 | 0.2736 | 0.2736 | 0.202156 |
| Oil/Gas Distribution | 24 | 0.149381 | 0.209037 | 0.0798938 | 0.223418 | 0.617519 | 1.01608 | 0.0720359 | 0.326577 | 0.0327 | 0.472826 | 0.0495715 | 0.404251 | 4.436 | 12.8694 | 20.6759 | 1.58129 | 69.407 | 0.0374558 | 0.300162 | 0.206717 | 1.25596 | 0.0390994 | 3.03214 | 3.03214 | 0.209042 |
| Oilfield Svcs/Equip. | 136 | 0.0148862 | 0.0416118 | 0.11592 | 0.209552 | 1.21865 | 1.57915 | 0.101316 | 0.53497 | 0.0367 | 0.327288 | 0.0771648 | 2.79097 | 0.735972 | 8.58291 | 16.7768 | 1.46616 | 25.4384 | 0.0797976 | 0.0400352 | 0.0157835 | 0.436015 | -0.0839707 | 0.00315528 | 0.00315528 | 0.0437349 |
| Packaging & Container | 24 | 0.0551621 | 0.101376 | 0.168341 | 0.217096 | 0.678174 | 0.990357 | 0.0706986 | 0.331374 | 0.0327 | 0.397366 | 0.0523508 | 1.85187 | 1.59359 | 9.50899 | 15.3215 | 3.09748 | 20.6089 | 0.10271 | 0.0530233 | 0.119768 | 1.48069 | 0.159553 | 0.449727 | 0.449727 | 0.103497 |
| Paper/Forest Products | 15 | 0.188848 | 0.0540352 | 0.0936853 | 0.196186 | 1.25437 | 1.53666 | 0.0991066 | 0.373667 | 0.0327 | 0.282876 | 0.0780092 | 1.90869 | 0.770474 | 7.53435 | 14.029 | 1.58639 | 24.9175 | 0.140242 | 0.0469653 | 0.0176665 | 0.392606 | 0.0204507 | 1.79432 | 1.79432 | 0.0547892 |
| Power | 52 | 0.0349545 | 0.183216 | 0.0647599 | 0.17047 | 0.378435 | 0.575829 | 0.0491431 | 0.184872 | 0.0272 | 0.420334 | 0.0370614 | 0.412471 | 4.11426 | 12.0303 | 22.7259 | 2.01101 | 23.7369 | 0.0543383 | 0.341339 | 0.213117 | 1.3995 | 0.0571394 | 0.975873 | 0.975873 | 0.181022 |
| Precious Metals | 83 | 0.140799 | 0.145096 | 0.0806645 | 0.271782 | 1.33205 | 1.43507 | 0.0938238 | 0.826426 | 0.0692 | 0.155195 | 0.0873174 | 0.56822 | 5.05471 | 13.6506 | 34.1715 | 1.74426 | 76.8447 | 0.139668 | 0.151484 | -0.0591047 | -0.179457 | 0.129002 | 0.207703 | 0.207703 | 0.144495 |
| Publishing & Newspapers | 31 | 0.00129556 | 0.0543386 | 0.104744 | 0.259475 | 0.756784 | 1.06751 | 0.0747105 | 0.381782 | 0.0327 | 0.403227 | 0.0544743 | 2.13902 | 1.07084 | 9.1787 | 19.7663 | 1.59374 | 28.0495 | 0.134765 | 0.0322108 | 0.00189683 | -0.0513198 | -0.0378505 | 0.0080401 | 0.0080401 | 0.0532907 |
| R.E.I.T. | 234 | 0.10673 | 0.271509 | 0.0292493 | 0.0217675 | 0.42562 | 0.683839 | 0.0547596 | 0.198565 | 0.0272 | 0.45763 | 0.0390357 | 0.127068 | 13.4849 | 22.6448 | 51.0055 | 2.26062 | 48.0009 | 0.892505 | 0.0369432 | -0.0978753 | -0.436394 | 0.0548796 | 1.92435 | 1.92435 | 0.234688 |
| Real Estate (Development) | 20 | -0.025032 | 0.102756 | 0.0208321 | 0.225289 | 0.891074 | 1.23615 | 0.0834798 | 0.472236 | 0.0367 | 0.411847 | 0.060435 | 0.280689 | 5.36638 | 26.106 | 68.3351 | 1.58049 | 48.4867 | 0.0431827 | 0.0334862 | -0.0501227 | -2.09894 | 0.0336746 | 0.000468248 | 0.000468248 | 0.0758765 |
| Real Estate (General/Diversified) | 12 | 0.02414 | 0.29911 | 0.0741202 | 0.163332 | 1.50172 | 1.63261 | 0.104095 | 0.213498 | 0.0272 | 0.312386 | 0.0779502 | 0.269239 | 6.57429 | 7.6753 | 13.4832 | 0.883869 | 110.211 | 3.45672 | 0.0319531 | -0.0590398 | 1.3357 | 0.0570981 | 0.22052 | 0.22052 | 0.294583 |
| Real Estate (Operations & Services) | 57 | 0.0348143 | 0.0574773 | 0.114694 | 0.222678 | 0.675048 | 0.932613 | 0.0676959 | 0.391522 | 0.0327 | 0.370287 | 0.0517103 | 2.10559 | 1.38945 | 12.6039 | 22.9818 | 2.57858 | 32.4585 | 0.115822 | 0.0128298 | 0.00637901 | 0.554666 | 0.119168 | 0.192327 | 0.192327 | 0.0576786 |
| Recreation | 63 | 0.0547452 | 0.095767 | 0.140805 | 0.235777 | 0.754029 | 0.901775 | 0.0660923 | 0.475304 | 0.0367 | 0.251955 | 0.0563751 | 1.62902 | 2.35241 | 13.3102 | 23.2386 | 6.03673 | 30.5105 | 0.186722 | 0.0507182 | 0.0400615 | 0.739226 | 0.0426834 | 2.64948 | 2.64948 | 0.0940451 |
| Reinsurance | 2 | 0.06635 | 0.0660968 | 0.0589955 | 0.210257 | 0.769854 | 0.819046 | 0.0617904 | 0.148716 | 0.0272 | 0.224877 | 0.0524827 | 1.09422 | 1.12393 | 14.9148 | 17.1886 | 1.05663 | 57.3991 | -0.0407527 | 0.00240344 | -0.00065072 | 0.122791 | 0.0500221 | 0.182633 | 0.182633 | 0.0653882 |
| Restaurant/Dining | 77 | 0.0791726 | 0.156919 | 0.190771 | 0.204907 | 0.751896 | 0.97298 | 0.069795 | 0.387567 | 0.0327 | 0.294059 | 0.0564829 | 1.53003 | 4.25847 | 16.8792 | 31.8381 | NA | 38.0001 | 0.00393395 | 0.0631486 | 0.0221583 | 0.26503 | NA | 0.539126 | 0.539126 | 0.133449 |
| Retail (Automotive) | 26 | 0.0469667 | 0.0563037 | 0.0947535 | 0.234943 | 0.868519 | 1.33258 | 0.0884943 | 0.373701 | 0.0327 | 0.421536 | 0.061529 | 2.25984 | 1.18937 | 13.9049 | 23.6426 | 6.45296 | 16.6193 | 0.127479 | 0.02139 | 0.0170165 | 0.493261 | 0.346009 | 0.0442089 | 0.0442089 | 0.0487785 |
| Retail (Building Supply) | 17 | 0.0634123 | 0.111954 | 0.28826 | 0.251512 | 1.15097 | 1.35886 | 0.0898606 | 0.472946 | 0.0367 | 0.204541 | 0.0771104 | 3.09864 | 2.02952 | 13.6004 | 18.5694 | 43.0479 | 238.796 | 0.0773527 | 0.0241691 | 0.0074314 | 0.257577 | 0.948065 | 0.537074 | 0.537074 | 0.109312 |
| Retail (Distributors) | 80 | 0.0722627 | 0.0835076 | 0.135738 | 0.232182 | 0.893715 | 1.27898 | 0.0857069 | 0.428308 | 0.0367 | 0.378341 | 0.0636943 | 1.78669 | 1.39533 | 12.6602 | 16.1407 | 2.95613 | 897.323 | 0.170935 | 0.073262 | 0.092433 | 1.37586 | 0.164713 | 0.289079 | 0.289079 | 0.0862921 |
| Retail (General) | 18 | 0.0150687 | 0.0417994 | 0.138182 | 0.249419 | 0.945727 | 1.1437 | 0.0786724 | 0.404022 | 0.0367 | 0.243021 | 0.0662425 | 4.2034 | 0.878543 | 12.2056 | 22.5743 | 4.843 | 18.6365 | 0.0199783 | 0.02449 | 0.0048751 | 0.170145 | 0.181426 | 0.444415 | 0.444415 | 0.0388998 |
| Retail (Grocery and Food) | 13 | 0.0556857 | 0.0229063 | 0.0712722 | 0.241421 | 0.345103 | 0.587787 | 0.0497649 | 0.371814 | 0.0327 | 0.491505 | 0.0373594 | 4.26185 | 0.486548 | 8.92812 | 25.3718 | 2.68816 | 395.144 | -0.00123272 | 0.0278784 | 0.00646585 | 0.42707 | 0.181119 | 0.341948 | 0.341948 | 0.0191741 |
| Retail (Online) | 70 | 0.182711 | 0.0670736 | 0.0999483 | 0.14316 | 1.15942 | 1.23013 | 0.0831666 | 0.559672 | 0.0367 | 0.11401 | 0.0768229 | 1.65002 | 3.41824 | 22.8201 | 53.4761 | 13.5012 | 243.824 | -0.00988708 | 0.052648 | -0.00210908 | 0.218825 | 0.224052 | 0.0359604 | 0.0359604 | 0.0624006 |
| Retail (Special Lines) | 89 | 0.0765294 | 0.0576187 | 0.12045 | 0.223297 | 0.690346 | 1.03032 | 0.0727767 | 0.449477 | 0.0367 | 0.413731 | 0.0540547 | 2.44772 | 1.18739 | 9.71576 | 21.287 | 4.56868 | 23.7933 | 0.0800177 | 0.023883 | 0.00548094 | 0.272108 | 0.19919 | 0.400908 | 0.400908 | 0.0558403 |
| Rubber& Tires | 4 | -0.06165 | 0.0551457 | 0.0611709 | 0.419699 | 0.453181 | 0.982989 | 0.0703154 | 0.575892 | 0.0367 | 0.640327 | 0.0429156 | 1.28956 | 0.742826 | 5.92552 | 12.4367 | 0.80022 | 21.5491 | 0.192671 | 0.0543741 | 0.00302458 | 0.773457 | 0.0369947 | 0.764268 | 0.764268 | 0.0597217 |
| Semiconductor | 72 | 0.0834766 | 0.24618 | 0.170033 | 0.140822 | 1.23689 | 1.2866 | 0.0861031 | 0.436946 | 0.0367 | 0.105546 | 0.0799204 | 0.712832 | 5.37563 | 13.7096 | 21.6569 | 5.01293 | 97.0937 | 0.169434 | 0.141192 | 0.156988 | 0.709627 | 0.202943 | 0.439142 | 0.439142 | 0.253706 |
| Semiconductor Equip | 39 | 0.05314 | 0.192211 | 0.221382 | 0.135196 | 1.25348 | 1.27847 | 0.0856803 | 0.410637 | 0.0367 | 0.10852 | 0.0793693 | 1.22857 | 3.99857 | 15.709 | 20.4265 | 5.85096 | 39.7252 | 0.290048 | 0.0433709 | 0.119878 | 0.690353 | 0.276491 | 0.29196 | 0.29196 | 0.199051 |
| Shipbuilding & Marine | 10 | 0.0977833 | 0.0741095 | 0.060183 | 0.228179 | 1.57139 | 2.17355 | 0.132225 | 0.340543 | 0.0327 | 0.357799 | 0.0936897 | 0.756524 | 1.97917 | 11.3213 | 23.3082 | 1.3401 | 25.1269 | 0.167623 | 0.129796 | 0.104703 | 1.73739 | 0.0269362 | 0.321058 | 0.321058 | 0.0836442 |
| Shoe | 11 | 0.0311875 | 0.124733 | 0.3057 | 0.152994 | 0.83361 | 0.86816 | 0.0643443 | 0.375639 | 0.0327 | 0.0808979 | 0.061123 | 2.90537 | 3.55035 | 22.0798 | 29.027 | 12.2114 | 23.09 | 0.207642 | 0.00647332 | -0.00838799 | -0.0399561 | 0.401572 | 0.267804 | 0.267804 | 0.122315 |
| Software (Entertainment) | 86 | 0.135345 | 0.226438 | 0.170123 | 0.18774 | 1.28587 | 1.28833 | 0.0861932 | 0.613731 | 0.0367 | 0.0365992 | 0.084046 | 0.708631 | 6.75874 | 20.596 | 30.2729 | 5.12448 | 33.9796 | 0.0669345 | 0.167072 | 0.127303 | 0.856061 | 0.18492 | 0 | 0 | 0.245666 |
| Software (Internet) | 30 | 0.309192 | 0.0915084 | 0.111214 | 0.153483 | 1.5032 | 1.67283 | 0.106187 | 0.447814 | 0.0367 | 0.169535 | 0.0928511 | 1.02108 | 7.63686 | 20.2293 | 58.7596 | 9.38647 | 66.7509 | 0.097008 | 0.0780814 | 0.0953223 | 1.56714 | 0.0613662 | 0.0257772 | 0.0257772 | 0.109937 |
| Software (System & Application) | 363 | 0.150381 | 0.222509 | 0.200289 | 0.112416 | 1.14916 | 1.19646 | 0.0814159 | 0.495022 | 0.0367 | 0.0881885 | 0.0766633 | 0.853019 | 8.76596 | 24.0048 | 35.6244 | 9.91715 | 110.902 | 0.130794 | 0.065155 | 0.0717994 | 0.443789 | 0.279145 | 0.30546 | 0.30546 | 0.240576 |
| Steel | 32 | 0.0228967 | 0.0775053 | 0.163138 | 0.182755 | 1.28557 | 1.61869 | 0.103372 | 0.393879 | 0.0327 | 0.3196 | 0.0781726 | 2.28954 | 0.701439 | 6.24179 | 8.90159 | 1.43503 | 14.3382 | 0.196113 | 0.0502986 | 0.0332261 | 0.362715 | 0.184094 | 0.196588 | 0.196588 | 0.0785107 |
| Telecom (Wireless) | 18 | 0.0348 | 0.10389 | 0.0565456 | 0.25255 | 0.596908 | 1.14293 | 0.0786323 | 0.418491 | 0.0367 | 0.567458 | 0.0496311 | 0.591218 | 2.42726 | 6.6389 | 23.8707 | 1.54241 | 25.6624 | 0.0184947 | 0.22941 | 0.0337838 | 1.23924 | 0.0114702 | 0.138044 | 0.138044 | 0.101631 |
| Telecom. Equipment | 91 | 0.0486081 | 0.192821 | 0.206965 | 0.219798 | 0.835979 | 0.894386 | 0.0657081 | 0.462957 | 0.0367 | 0.146922 | 0.0600982 | 1.06273 | 3.50226 | 13.4227 | 17.72 | 4.9997 | 57.039 | 0.181336 | 0.0316669 | 0.0954687 | 0.625498 | 0.175784 | 0.53306 | 0.53306 | 0.203183 |
| Telecom. Services | 67 | 0.100815 | 0.182923 | 0.130502 | 0.182071 | 0.666584 | 1.04816 | 0.0737044 | 0.544733 | 0.0367 | 0.44194 | 0.0532959 | 0.755654 | 2.84726 | 7.93168 | 15.74 | 2.12631 | 742.091 | 0.0225491 | 0.123041 | -0.0278633 | -0.249359 | 0.0566774 | 1.70557 | 1.70557 | 0.180223 |
| Tobacco | 17 | 0.03837 | 0.393372 | 0.541112 | 0.298916 | 1.42632 | 1.68027 | 0.106574 | 0.384852 | 0.0327 | 0.222149 | 0.0883469 | 1.55372 | 5.18922 | 12.3003 | 13.1638 | 89.121 | 24.2986 | 0.162775 | 0.025531 | 0.0265096 | 0.19179 | -0.00053629 | 1.43693 | 1.43693 | 0.393517 |
| Transportation | 18 | 0.1435 | 0.0503863 | 0.104533 | 0.215348 | 0.95727 | 1.30517 | 0.0870688 | 0.279851 | 0.0327 | 0.351631 | 0.0650765 | 2.44707 | 1.3481 | 12.3891 | 27.5323 | 4.92706 | 58.5341 | 0.0738708 | 0.0706125 | 0.0358951 | 1.2256 | 0.216138 | 0.599812 | 0.599812 | 0.0489637 |
| Transportation (Railroads) | 8 | 0.0007825 | 0.386915 | 0.154382 | 0.233834 | 1.89198 | 2.24043 | 0.135702 | 0.182467 | 0.0272 | 0.207838 | 0.111738 | 0.460409 | 6.32416 | 12.5583 | 16.5514 | 4.90754 | 20.4824 | 0.0261128 | 0.162961 | 0.0593727 | 0.191321 | 0.234366 | 0.338563 | 0.338563 | 0.382083 |
| Trucking | 33 | 0.129844 | -0.0461536 | 0.00326579 | 0.26636 | 1.04107 | 1.37217 | 0.0905531 | 0.418538 | 0.0367 | 0.36659 | 0.0674476 | 1.14472 | 1.93414 | 9.07552 | NA | 2.81156 | 18.3584 | 0.0549794 | 0.194351 | 0.17408 | NA | -0.320709 | 0.0013725 | 0.0013725 | -0.00382897 |
| Utility (General) | 16 | 0.0227269 | 0.174515 | 0.0662603 | 0.144287 | 0.189688 | 0.283928 | 0.0339642 | 0.131126 | 0.0272 | 0.401001 | 0.028525 | 0.442941 | 4.2604 | 14.1255 | 24.6509 | 2.10822 | 23.7211 | 0.0418362 | 0.275706 | 0.266686 | 1.85509 | 0.110674 | 0.754313 | 0.754313 | 0.17283 |
| Utility (Water) | 17 | 0.0754082 | 0.302556 | 0.0786665 | 0.222587 | 0.565321 | 0.684513 | 0.0547947 | 0.178805 | 0.0272 | 0.263379 | 0.0457358 | 0.290399 | 8.82924 | 19.0187 | 29.1004 | 3.34333 | 48.1291 | 0.072291 | 0.448203 | 0.322099 | 1.33046 | 0.136291 | 0.666013 | 0.459692 | 0.301028 |
| Total Market | 7053 | 0.101481 | 0.107012 | 0.0731472 | 0.185709 | 0.829454 | 1.12884 | 0.0778997 | 0.423564 | 0.0367 | 0.367105 | 0.0594069 | 0.728578 | 3.15812 | 17.5401 | 28.9886 | 3.21385 | 70.8515 | -0.232016 | 0.0614944 | 0.0517881 | 0.656475 | 0.136291 | 0.459692 | 0.459692 | 0.108139 |
| Total Market (without financials) | 5878 | 0.105258 | 0.111539 | 0.129589 | 0.18428 | 1.01248 | 1.20953 | 0.0820955 | 0.464061 | 0.0367 | 0.240148 | 0.0689905 | 1.21668 | 2.62482 | 13.7541 | 22.9733 | 3.88523 | 76.8328 | 0.0890633 | 0.0648499 | 0.0538813 | 0.668223 | 0.132964 | 0.524178 | 0.524178 | 0.112922 |

**Industry Average Beta (Global) — full table:**

| Industry Name | Number of firms | Annual Average Revenue growth - Last 5 years | Pre-tax Operating Margin (Unadjusted) | After-tax ROC | Average effective tax rate | Unlevered Beta | Equity (Levered) Beta | Cost of equity | Std deviation in stock prices | Pre-tax cost of debt | Market Debt/Capital | Cost of capital | Sales/Capital | EV/Sales | EV/EBITDA | EV/EBIT | Price/Book | Trailing PE | Non-cash WC as % of Revenues | Cap Ex as % of Revenues | Net Cap Ex as % of Revenues | Reinvestment Rate | ROE | Dividend Payout Ratio | Equity Reinvestment Rate | Pre-tax Operating Margin (Lease & R&D adjusted) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Advertising | 312 | 0.0908533 | 0.0873314 | 0.201017 | 0.268069 | 0.957482 | 1.18397 | 0.0923693 | 0.463852 | 0.045 | 0.330511 | 0.0728908 | 2.64071 | 1.70797 | 11.1011 | 18.3217 | 2.20241 | 66.3211 | -0.0242898 | 0.0206012 | 0.0309 | 0.542453 | 0.0732741 | 0.784614 | 0.784614 | 0.0908824 |
| Aerospace/Defense | 238 | 0.0804255 | 0.0960127 | 0.216488 | 0.20492 | 1.05343 | 1.18487 | 0.0924249 | 0.370201 | 0.041 | 0.197621 | 0.08018 | 2.48642 | 1.99941 | 14.6883 | 20.6934 | 5.18996 | 43.888 | 0.333373 | 0.0327961 | 0.0481357 | 1.04788 | 0.220348 | 0.453397 | 0.453397 | 0.0979975 |
| Air Transport | 159 | 0.0713753 | 0.0846102 | 0.0664439 | 0.221156 | 0.651567 | 1.09579 | 0.0869199 | 0.30606 | 0.041 | 0.515821 | 0.0577982 | 1.01344 | 1.63601 | 8.15873 | 20.9078 | 2.00309 | 21.6842 | -0.0292326 | 0.112226 | 0.0440202 | 0.718667 | 0.117406 | 0.436187 | 0.436187 | 0.0781125 |
| Apparel | 1161 | 0.00899621 | 0.115375 | 0.150892 | 0.25122 | 0.700375 | 0.802376 | 0.0687869 | 0.362993 | 0.041 | 0.216611 | 0.0604855 | 1.4846 | 2.30433 | 12.5775 | 19.0544 | 3.01066 | 31.9812 | 0.228492 | 0.0432172 | 0.0281519 | 0.573601 | 0.118605 | 0.531595 | 0.531595 | 0.119031 |
| Auto & Truck | 134 | 0.0497352 | 0.0478624 | 0.0459658 | 0.223226 | 0.854059 | 1.3743 | 0.104131 | 0.336242 | 0.041 | 0.534423 | 0.0647614 | 1.05567 | 0.904405 | 9.80859 | 18.3705 | 1.02997 | 35.276 | 0.0463058 | 0.0699724 | 0.0413234 | 1.32032 | 0.0854579 | 0.45197 | 0.45197 | 0.0500773 |
| Auto Parts | 682 | 0.0527755 | 0.0533948 | 0.0745879 | 0.260331 | 1.11142 | 1.26116 | 0.0971396 | 0.346745 | 0.041 | 0.281053 | 0.0783999 | 1.6247 | 0.75176 | 7.07736 | 13.6084 | 1.29095 | 36.5156 | 0.115375 | 0.0617666 | 0.0516716 | 1.43178 | 0.0695872 | 0.483122 | 0.483122 | 0.0553068 |
| Bank (Money Center) | 595 | 0.163912 | 0.00115393 | 0.000177879 | 0.195719 | 0.401801 | 0.807331 | 0.0690931 | 0.225366 | 0.0355 | 0.7114 | 0.0387045 | 0.138959 | 7.61752 | NA | NA | 0.943141 | 14.3776 | NA | 0.0361817 | 0.0335807 | 32.4004 | 0.109357 | 0.354487 | 0.354487 | 0.00161666 |
| Banks (Regional) | 862 | 0.0836584 | -0.000209995 | -0.000201325 | 0.182766 | 0.464905 | 0.633495 | 0.05835 | 0.19976 | 0.0355 | 0.609546 | 0.0388607 | 0.213609 | 4.90434 | NA | NA | 0.720519 | 14.9315 | NA | 0.0332035 | 0.0178209 | NA | 0.109136 | 0.257829 | 0.257829 | -0.00115916 |
| Beverage (Alcoholic) | 216 | 0.0926456 | 0.215995 | 0.132427 | 0.245694 | 0.800588 | 0.900627 | 0.0748588 | 0.291717 | 0.041 | 0.183817 | 0.0666981 | 0.743224 | 4.2692 | 15.5399 | 19.68 | 3.6412 | 32.8583 | 0.0869699 | 0.0492055 | 0.0140998 | 0.135177 | 0.154023 | 0.451639 | 0.451639 | 0.216318 |
| Beverage (Soft) | 94 | 0.0990202 | 0.160335 | 0.202081 | 0.129759 | 0.709289 | 0.792482 | 0.0681754 | 0.343771 | 0.041 | 0.170287 | 0.0617535 | 1.40023 | 3.64399 | 17.5831 | 22.4904 | 5.78107 | 72.4755 | -0.0441894 | 0.047075 | 0.0557121 | 0.408749 | 0.267917 | 0.585825 | 0.585825 | 0.161704 |
| Broadcasting | 138 | 0.0351672 | 0.171587 | 0.162623 | 0.130148 | 0.685241 | 0.96951 | 0.0791157 | 0.336872 | 0.041 | 0.402114 | 0.0595518 | 1.14371 | 2.02789 | 8.45545 | 11.7122 | 1.56221 | 46.471 | 0.16959 | 0.0381389 | 0.147273 | 1.12225 | 0.317583 | 0.422489 | 0.422489 | 0.171479 |
| Brokerage & Investment Banking | 559 | 0.112846 | 0.00975237 | 0.00148847 | 0.212622 | 0.436641 | 1.00015 | 0.0810091 | 0.362933 | 0.041 | 0.685578 | 0.0463558 | 0.175116 | 7.15378 | NA | NA | 1.41333 | 60.356 | NA | 0.0533371 | 0.0482582 | -18.7679 | 0.0900057 | 0.49319 | 0.49319 | 0.00990281 |
| Building Materials | 426 | 0.0494076 | 0.0800945 | 0.107289 | 0.265856 | 0.82985 | 0.964784 | 0.0788237 | 0.314201 | 0.041 | 0.243786 | 0.067034 | 1.60062 | 1.40128 | 10.7547 | 16.8987 | 2.14532 | 29.1922 | 0.172244 | 0.0424289 | 0.0317192 | 0.669849 | 0.101649 | 0.38446 | 0.38446 | 0.0824873 |
| Business & Consumer Services | 868 | 0.103662 | 0.0856789 | 0.188097 | 0.252668 | 0.880423 | 0.999295 | 0.0809565 | 0.414908 | 0.045 | 0.208329 | 0.0710564 | 2.54202 | 1.92843 | 9.73264 | 21.4501 | 4.2169 | 44.5557 | 0.0946007 | 0.0285656 | 0.0203872 | 0.432474 | 0.14181 | 0.516277 | 0.516277 | 0.0893849 |
| Cable TV | 61 | 0.0155683 | 0.166933 | 0.108316 | 0.237341 | 0.791034 | 1.17219 | 0.0916413 | 0.306888 | 0.041 | 0.416196 | 0.0661792 | 0.756219 | 3.37539 | 9.65798 | 19.3683 | 2.42204 | 39.4664 | 0.0111507 | 0.12725 | 0.109093 | 0.871614 | 0.191208 | 0.165846 | 0.165846 | 0.16722 |
| Chemical (Basic) | 793 | 0.0647177 | 0.0791784 | 0.0783726 | 0.205633 | 0.903286 | 1.06491 | 0.0850112 | 0.321912 | 0.041 | 0.27913 | 0.0697852 | 1.17069 | 1.30774 | 9.60386 | 16.0757 | 1.49173 | 36.3796 | 0.122417 | 0.0905895 | 0.0670586 | 1.17423 | 0.0813213 | 0.710296 | 0.710296 | 0.0800253 |
| Chemical (Diversified) | 73 | 0.0270632 | 0.0842462 | 0.0754834 | 0.24298 | 0.952335 | 1.21755 | 0.0944446 | 0.299365 | 0.041 | 0.327659 | 0.0734805 | 1.07937 | 1.21154 | 8.18692 | 14.1894 | 1.29848 | 19.5407 | 0.18889 | 0.0775551 | 0.0604086 | 1.09203 | 0.125153 | 0.40967 | 0.40967 | 0.0859624 |
| Chemical (Specialty) | 829 | 0.0754654 | 0.106758 | 0.107567 | 0.227609 | 0.981894 | 1.11713 | 0.0882385 | 0.366801 | 0.041 | 0.210668 | 0.0760671 | 1.17184 | 2.03166 | 11.4819 | 18.6069 | 2.27831 | 30.0374 | 0.176809 | 0.069607 | 0.0593288 | 0.923668 | 0.109462 | 0.475814 | 0.475814 | 0.108877 |
| Coal & Related Energy | 224 | 0.0888298 | 0.166415 | 0.147585 | 0.234044 | 1.27444 | 1.45148 | 0.108902 | 0.554626 | 0.045 | 0.343865 | 0.0829514 | 0.980731 | 1.13615 | 4.52754 | 6.66031 | 0.938626 | 17.1243 | -0.0220574 | 0.0782895 | 0.0401362 | 0.331705 | 0.130557 | 0.567668 | 0.567668 | 0.167085 |
| Computer Services | 969 | 0.0866746 | 0.0703864 | 0.198315 | 0.252773 | 0.980648 | 1.08009 | 0.0859494 | 0.39387 | 0.041 | 0.193697 | 0.0752019 | 3.27696 | 1.23333 | 11.7945 | 16.7634 | 3.36701 | 37.8037 | 0.137772 | 0.0167517 | 0.0506391 | 1.04288 | 0.163924 | 0.383715 | 0.383715 | 0.0729976 |
| Computers/Peripherals | 332 | 0.032743 | 0.0999332 | 0.135763 | 0.196921 | 1.34931 | 1.41245 | 0.10649 | 0.376699 | 0.041 | 0.146416 | 0.0953581 | 1.50842 | 1.83779 | 11.7625 | 18.138 | 3.81227 | 43.6702 | 0.0270903 | 0.0399411 | 0.0203932 | 0.278441 | 0.181765 | 0.340543 | 0.340543 | 0.102537 |
| Construction Supplies | 747 | 0.0504248 | 0.103928 | 0.114554 | 0.227048 | 0.956171 | 1.14918 | 0.0902194 | 0.350803 | 0.041 | 0.314568 | 0.0714219 | 1.28259 | 1.34978 | 8.54602 | 12.4961 | 1.61698 | 36.0304 | 0.112948 | 0.0489325 | 0.0244935 | 0.561217 | 0.1203 | 0.493271 | 0.493271 | 0.105442 |
| Diversified | 319 | 0.0749414 | 0.113086 | 0.0873492 | 0.177746 | 0.690802 | 0.930363 | 0.0766964 | 0.266157 | 0.041 | 0.404335 | 0.0580026 | 0.902117 | 1.58949 | 9.69231 | 13.7781 | 1.08447 | 27.0494 | -0.136898 | 0.0510885 | 0.0342362 | 0.524427 | 0.0824159 | 0.307072 | 0.307072 | 0.113856 |
| Drugs (Biotechnology) | 1024 | 0.229976 | 0.0897304 | 0.0718408 | 0.151835 | 1.40241 | 1.42785 | 0.107441 | 0.620746 | 0.045 | 0.109486 | 0.0993384 | 0.440563 | 7.92521 | 16.0345 | 64.0074 | 6.75264 | 156.28 | 0.184337 | 0.0548742 | 0.0974634 | 2.48231 | -0.0206652 | 0.00229053 | 0.00229053 | 0.164846 |
| Drugs (Pharmaceutical) | 1263 | 0.134381 | 0.180889 | 0.119519 | 0.156966 | 1.19851 | 1.29679 | 0.0993418 | 0.520298 | 0.045 | 0.154543 | 0.0891563 | 0.713534 | 4.13279 | 14.4989 | 22.151 | 3.66402 | 66.8754 | 0.17687 | 0.0497784 | 0.0622258 | 0.469735 | 0.110253 | 0.744713 | 0.744713 | 0.185706 |
| Education | 211 | 0.0637585 | 0.114338 | 0.111743 | 0.190268 | 1.02348 | 1.13667 | 0.089446 | 0.3939 | 0.041 | 0.214536 | 0.076792 | 1.13776 | 3.18311 | 15.1713 | 27.6563 | 2.76602 | 57.3901 | 0.0307826 | 0.068339 | 0.0849897 | 1.22199 | 0.117599 | 0.341536 | 0.341536 | 0.113216 |
| Electrical Equipment | 902 | 0.0789468 | 0.0707346 | 0.11584 | 0.20165 | 1.14629 | 1.28046 | 0.0983325 | 0.382176 | 0.041 | 0.22417 | 0.0831182 | 1.3243 | 1.70204 | 10.3609 | 16.5871 | 2.27753 | 53.3097 | 0.237902 | 0.0474041 | 0.036555 | 0.827387 | 0.0669646 | 0.671327 | 0.671327 | 0.099918 |
| Electronics (Consumer & Office) | 142 | 0.0142164 | 0.0482446 | 0.0940581 | 0.111958 | 1.3 | 1.45127 | 0.108888 | 0.408554 | 0.045 | 0.279649 | 0.0877878 | 1.84117 | 0.775131 | 7.93891 | 14.7175 | 1.63401 | 56.4658 | 0.0241358 | 0.0439645 | 0.0368511 | 1.21719 | 0.131331 | 0.236993 | 0.236993 | 0.0564019 |
| Electronics (General) | 1345 | 0.0611619 | 0.0605484 | 0.0861158 | 0.210001 | 1.38172 | 1.39929 | 0.105676 | 0.39667 | 0.041 | 0.150604 | 0.0943489 | 1.55394 | 1.45737 | 13.0926 | 23.0954 | 2.37316 | 54.1111 | 0.17294 | 0.0644578 | 0.0502717 | 1.38967 | 0.0790485 | 0.487863 | 0.487863 | 0.0636892 |
| Engineering/Construction | 1208 | 0.0467898 | 0.0528594 | 0.0950974 | 0.250381 | 0.809988 | 1.10046 | 0.0872084 | 0.365286 | 0.041 | 0.476016 | 0.0601967 | 2.07439 | 0.640784 | 8.21507 | 11.6172 | 1.11094 | 52.5618 | 0.154078 | 0.0336732 | 0.0352397 | 1.56878 | 0.0957234 | 0.529387 | 0.529387 | 0.0554313 |
| Entertainment | 660 | 0.133692 | 0.117698 | 0.127766 | 0.225737 | 1.17049 | 1.25957 | 0.0970413 | 0.480117 | 0.045 | 0.163326 | 0.0866527 | 1.23379 | 3.90492 | 19.0336 | 32.6338 | 3.25024 | 52.2523 | 0.0510755 | 0.0460128 | 0.0518649 | 0.722851 | 0.091069 | 0.375857 | 0.375857 | 0.114137 |
| Environmental & Waste Services | 325 | 0.116996 | 0.104282 | 0.125309 | 0.222328 | 1.01089 | 1.21658 | 0.0943845 | 0.438241 | 0.045 | 0.270071 | 0.0779238 | 1.35461 | 2.47616 | 13.4583 | 22.7828 | 2.94648 | 139.86 | 0.115789 | 0.0956868 | 0.0742674 | 1.26747 | 0.0772053 | 0.692436 | 0.692436 | 0.106807 |
| Farming/Agriculture | 406 | 0.0835742 | 0.0470321 | 0.0538369 | 0.199059 | 0.600476 | 0.81652 | 0.0696609 | 0.38163 | 0.041 | 0.36967 | 0.0551706 | 1.27973 | 1.20359 | 13.8139 | 23.8643 | 1.83487 | 79.746 | 0.156933 | 0.0493702 | 0.0341073 | 1.12794 | 0.0674681 | 0.544357 | 0.544357 | 0.0479285 |
| Financial Svcs. (Non-bank & Insurance) | 1059 | 0.132395 | 0.0677423 | 0.00392505 | 0.181902 | 0.149564 | 0.789162 | 0.0679702 | 0.3453 | 0.041 | 0.862788 | 0.0356094 | 0.069887 | 15.9736 | 152.523 | NA | 1.35136 | 69.4478 | NA | 0.0689228 | 0.069558 | 1.95106 | 0.206226 | 0.211488 | 0.211488 | 0.0664553 |
| Food Processing | 1262 | 0.0639886 | 0.0852895 | 0.119364 | 0.213842 | 0.650117 | 0.749957 | 0.0655474 | 0.320189 | 0.041 | 0.215422 | 0.0579894 | 1.65765 | 1.73295 | 13.7177 | 20.0804 | 2.74763 | 41.6767 | 0.105047 | 0.046081 | 0.0376929 | 0.623047 | 0.0794082 | 0.745293 | 0.745293 | 0.08567 |
| Food Wholesalers | 151 | 0.155956 | 0.0241587 | 0.106732 | 0.26081 | 0.518493 | 0.756416 | 0.0659465 | 0.34198 | 0.041 | 0.427331 | 0.0507833 | 5.20844 | 0.481395 | 11.4273 | 19.2739 | 2.07353 | 51.7536 | 0.0484348 | 0.0150099 | 0.0172355 | 0.984568 | 0.09127 | 0.54521 | 0.54521 | 0.0248255 |
| Furn/Home Furnishings | 328 | 0.0649118 | 0.0742704 | 0.155554 | 0.185768 | 1.00585 | 1.02622 | 0.0826205 | 0.344007 | 0.041 | 0.193459 | 0.0725301 | 2.40842 | 1.1889 | 10.9252 | 15.2763 | 2.7211 | 28.3717 | 0.0477242 | 0.0348351 | 0.0263392 | 0.544231 | 0.142614 | 0.492101 | 0.492101 | 0.0771199 |
| Green & Renewable Energy | 213 | 0.237363 | 0.356479 | 0.0711056 | 0.16701 | 0.58673 | 0.886969 | 0.0740147 | 0.380255 | 0.041 | 0.435185 | 0.0550616 | 0.230759 | 6.75751 | 11.5695 | 19.2326 | 1.72018 | 105.77 | 0.0484742 | 0.287672 | 0.137574 | 0.699007 | 0.10431 | 0.778405 | 0.778405 | 0.348605 |
| Healthcare Products | 739 | 0.113778 | 0.14871 | 0.140197 | 0.152783 | 1.13313 | 1.19592 | 0.0931078 | 0.483566 | 0.045 | 0.110604 | 0.0865078 | 0.967568 | 5.17303 | 21.3479 | 33.2282 | 4.56124 | 52.1861 | 0.24356 | 0.0535611 | 0.0642847 | 0.73056 | 0.0969496 | 0.380061 | 0.380061 | 0.156537 |
| Healthcare Support Services | 402 | 0.183645 | 0.045005 | 0.27228 | 0.236251 | 0.818386 | 1.01011 | 0.0816245 | 0.398179 | 0.041 | 0.293546 | 0.0666063 | 7.26584 | 0.722388 | 11.5531 | 16.1336 | 2.54862 | 36.1818 | -0.0124594 | 0.0100413 | 0.0464031 | 1.57309 | 0.122732 | 0.390526 | 0.390526 | 0.0441139 |
| Heathcare Information and Technology | 389 | 0.171554 | 0.123046 | 0.130772 | 0.157575 | 1.22538 | 1.29559 | 0.0992673 | 0.537554 | 0.045 | 0.107555 | 0.0921867 | 1.09756 | 5.70929 | 24.8148 | 42.3529 | 5.53251 | 770.422 | 0.20891 | 0.0562045 | 0.0640224 | 0.852209 | 0.101845 | 0.152688 | 0.152688 | 0.128843 |
| Homebuilding | 167 | 0.113427 | 0.106946 | 0.1054 | 0.238677 | 0.748287 | 0.8857 | 0.0739363 | 0.322901 | 0.041 | 0.301374 | 0.0608346 | 1.35306 | 1.15402 | 9.28678 | 11.47 | 1.58441 | 16.1766 | 0.595405 | 0.0120652 | 0.0125762 | 0.620016 | 0.147655 | 0.218178 | 0.218178 | 0.0999094 |
| Hospitals/Healthcare Facilities | 206 | 0.0781431 | 0.10339 | 0.0952253 | 0.216763 | 0.503974 | 0.780058 | 0.0674076 | 0.31469 | 0.041 | 0.444808 | 0.0509744 | 1.21666 | 2.21807 | 12.002 | 22.9209 | 3.423 | 39.7226 | 0.0755859 | 0.0692381 | 0.0569841 | 0.959291 | 0.128741 | 0.396496 | 0.396496 | 0.0935372 |
| Hotel/Gaming | 639 | 0.132157 | 0.143273 | 0.0880226 | 0.186086 | 0.684905 | 0.89595 | 0.0745697 | 0.346684 | 0.041 | 0.346643 | 0.0592805 | 0.766576 | 3.02555 | 12.3882 | 22.4347 | 2.37553 | 53.1471 | 0.0012774 | 0.0860295 | 0.0546008 | 0.573501 | 0.11444 | 0.529544 | 0.529544 | 0.133606 |
| Household Products | 536 | 0.0790467 | 0.1639 | 0.22836 | 0.243754 | 0.964118 | 1.031 | 0.0829157 | 0.405825 | 0.045 | 0.125701 | 0.0766959 | 1.59554 | 3.40381 | 16.0971 | 20.5209 | 5.96405 | 73.7682 | 0.067098 | 0.0382105 | 0.0347246 | 0.302577 | 0.163022 | 0.743932 | 0.743932 | 0.165309 |
| Information Services | 215 | 0.149398 | 0.2533 | 0.368264 | 0.194818 | 1.04583 | 1.10246 | 0.0873322 | 0.412585 | 0.045 | 0.108051 | 0.0815086 | 1.6505 | 8.12414 | 25.2969 | 31.2116 | 6.2777 | 39.0679 | 0.0686932 | 0.0325734 | 0.141053 | 0.786643 | 0.2733 | 0.263985 | 0.263985 | 0.255922 |
| Insurance (General) | 216 | 0.0647352 | 0.0953337 | 0.134428 | 0.241632 | 0.535517 | 0.613959 | 0.0571427 | 0.268281 | 0.041 | 0.297635 | 0.0492019 | 1.66331 | 1.07905 | 9.05104 | 11.0529 | 1.32893 | 28.4379 | -0.0106242 | 0.00728135 | 0.0223651 | 0.358749 | 0.0962109 | 0.497857 | 0.497857 | 0.0953806 |
| Insurance (Life) | 137 | 0.103593 | 0.0920842 | 0.11583 | 0.166616 | 0.977848 | 0.991516 | 0.0804757 | 0.258905 | 0.041 | 0.449285 | 0.0580057 | 1.48842 | 0.887212 | 8.84831 | 9.52048 | 1.02927 | 24.8996 | -1.00441 | 0.00692696 | 0.00461273 | 0.0629419 | 0.112314 | 0.290337 | 0.290337 | 0.0924702 |
| Insurance (Prop/Cas.) | 223 | 0.058856 | 0.0872356 | 0.0962976 | 0.180457 | 0.50237 | 0.555456 | 0.0535272 | 0.247339 | 0.0355 | 0.228277 | 0.0473293 | 1.32569 | 1.11224 | 10.5614 | 12.5327 | 1.2953 | 42.8144 | -0.37719 | 0.00858484 | 0.0013951 | 0.116366 | 0.0958562 | 0.366381 | 0.366381 | 0.0872789 |
| Investments & Asset Management | 1066 | 0.106709 | 0.187695 | 0.0527043 | 0.167974 | 0.549273 | 0.812263 | 0.0693978 | 0.371068 | 0.041 | 0.477657 | 0.0508004 | 0.311907 | 4.87729 | 20.1445 | 24.6839 | 1.35535 | 119.482 | NA | 0.0260379 | 0.143611 | 1.19905 | 0.102475 | 0.488327 | 0.488327 | 0.182643 |
| Machinery | 1332 | 0.0550722 | 0.0901875 | 0.122194 | 0.237702 | 1.16453 | 1.25198 | 0.0965723 | 0.350865 | 0.041 | 0.180571 | 0.0846349 | 1.50222 | 1.76465 | 12.2112 | 17.9708 | 2.54044 | 37.2968 | 0.252575 | 0.043177 | 0.0509647 | 0.964496 | 0.103305 | 0.445018 | 0.445018 | 0.0980661 |
| Metals & Mining | 1529 | 0.114049 | 0.0896528 | 0.100966 | 0.313301 | 1.09406 | 1.33464 | 0.10168 | 0.712858 | 0.0525 | 0.312382 | 0.0821026 | 1.16213 | 1.25953 | 7.5705 | 13.1965 | 1.44108 | 155.378 | 0.0945704 | 0.078915 | 0.0456771 | 0.768388 | 0.0755974 | 0.767215 | 0.767215 | 0.0907927 |
| Office Equipment & Services | 146 | 0.0313212 | 0.0723816 | 0.131613 | 0.26841 | 0.937645 | 1.04456 | 0.083754 | 0.363884 | 0.041 | 0.252479 | 0.0702992 | 2.08618 | 1.06393 | 9.29028 | 14.1322 | 2.0261 | 28.8601 | 0.136441 | 0.0260651 | 0.00942842 | 0.348652 | 0.0918905 | 0.472032 | 0.472032 | 0.0753507 |
| Oil/Gas (Integrated) | 49 | 0.0075078 | 0.1311 | 0.136952 | 0.395747 | 1.14018 | 1.29579 | 0.0992796 | 0.288157 | 0.041 | 0.207308 | 0.0850133 | 1.38189 | 1.42209 | 6.76631 | 11.0082 | 1.74228 | 23.5612 | 0.0275066 | 0.0902995 | 0.0344198 | 0.399302 | 0.141519 | 0.63509 | 0.63509 | 0.129189 |
| Oil/Gas (Production and Exploration) | 773 | -0.00960206 | 0.219813 | 0.0909817 | 0.270021 | 1.14432 | 1.55148 | 0.115081 | 0.636873 | 0.045 | 0.362078 | 0.085519 | 0.432118 | 2.7746 | 5.136 | 12.2562 | 1.11151 | 21.4943 | 0.0302228 | 0.351229 | 0.111073 | 0.66129 | 0.0622274 | 0.56668 | 0.56668 | 0.223106 |
| Oil/Gas Distribution | 160 | 0.162663 | 0.137641 | 0.0724263 | 0.174663 | 0.826499 | 1.28452 | 0.0985833 | 0.335642 | 0.041 | 0.444841 | 0.0682806 | 0.588667 | 2.85623 | 12.7969 | 20.5802 | 1.57109 | 25.8881 | 0.0329924 | 0.170967 | 0.105932 | 0.922423 | 0.0720242 | 1.24743 | 1.24743 | 0.136948 |
| Oilfield Svcs/Equip. | 508 | -0.00900406 | 0.0401231 | 0.0821906 | 0.259316 | 1.06412 | 1.40857 | 0.106249 | 0.449673 | 0.045 | 0.358279 | 0.0801616 | 2.24174 | 0.738899 | 9.45098 | 17.8273 | 1.42676 | 32.9717 | 0.0573752 | 0.042438 | 0.0227123 | 0.699983 | 0.000145023 | 0.00635209 | 0.00635209 | 0.0408813 |
| Packaging & Container | 400 | 0.0588779 | 0.0894635 | 0.116742 | 0.229583 | 0.607321 | 0.816899 | 0.0696844 | 0.354071 | 0.041 | 0.354224 | 0.0557912 | 1.55091 | 1.43056 | 9.32872 | 15.5782 | 2.24399 | 31.0358 | 0.138297 | 0.0595094 | 0.0849773 | 1.24233 | 0.0991978 | 0.524424 | 0.524424 | 0.0913995 |
| Paper/Forest Products | 279 | 0.0651504 | 0.0767269 | 0.0650639 | 0.219118 | 0.740906 | 1.02671 | 0.0826508 | 0.353461 | 0.041 | 0.397313 | 0.0619159 | 0.980193 | 1.30406 | 9.4237 | 16.7256 | 1.26831 | 31.859 | 0.187928 | 0.0688009 | 0.0681586 | 1.23222 | 0.0543216 | 0.725484 | 0.725484 | 0.0771675 |
| Power | 538 | 0.0697159 | 0.126202 | 0.0616863 | 0.194657 | 0.50506 | 0.824737 | 0.0701688 | 0.265972 | 0.041 | 0.486346 | 0.050858 | 0.602798 | 2.25422 | 9.68069 | 17.8448 | 1.33002 | 29.2909 | 0.0145841 | 0.159029 | 0.0823772 | 0.911751 | 0.0785677 | 0.689657 | 0.689657 | 0.124407 |
| Precious Metals | 844 | 0.185595 | 0.0971117 | 0.0680519 | 0.343212 | 0.998343 | 1.07645 | 0.0857246 | 0.81369 | 0.0775 | 0.16001 | 0.0812215 | 0.716403 | 3.13654 | 11 | 29.8107 | 2.04003 | 75.4068 | 0.122998 | 0.174076 | 0.0751073 | 1.68895 | 0.0355967 | 1.00124 | 1.00124 | 0.0987734 |
| Publishing & Newspapers | 352 | 0.0096153 | 0.0594567 | 0.0724249 | 0.241972 | 0.852022 | 0.956619 | 0.078319 | 0.379462 | 0.041 | 0.284801 | 0.0646896 | 1.46193 | 1.21775 | 10.0725 | 19.7654 | 1.43821 | 88.4912 | 0.125081 | 0.0354173 | 0.0185129 | 0.376109 | 0.0279242 | 1.26545 | 1.26545 | 0.0583545 |
| R.E.I.T. | 753 | 0.112833 | 0.359936 | 0.0348266 | 0.0337311 | 0.345237 | 0.532485 | 0.0521076 | 0.185366 | 0.0355 | 0.434831 | 0.0409189 | 0.108242 | 13.7767 | 23.0584 | 36.5739 | 1.67496 | 65.4754 | 0.668929 | 0.0629529 | 0.0165111 | 0.0561104 | 0.0611415 | 1.18694 | 1.18694 | 0.331096 |
| Real Estate (Development) | 842 | 0.120978 | 0.203838 | 0.0910698 | 0.354457 | 0.635863 | 1.07524 | 0.0856496 | 0.330367 | 0.041 | 0.600168 | 0.0525284 | 0.54584 | 2.10195 | 9.45224 | 10.108 | 0.85552 | 48.4907 | 1.61311 | 0.0290869 | 0.0487854 | 1.33773 | 0.128255 | 0.570203 | 0.570203 | 0.203297 |
| Real Estate (General/Diversified) | 383 | 0.0863011 | 0.198322 | 0.0488699 | 0.226693 | 0.642276 | 1.01207 | 0.081746 | 0.299015 | 0.041 | 0.494872 | 0.0563675 | 0.289382 | 3.43266 | 12.7858 | 16.872 | 0.725061 | 39.2576 | 0.843165 | 0.0866746 | 0.102738 | 1.30725 | 0.0765584 | 0.408574 | 0.408574 | 0.198687 |
| Real Estate (Operations & Services) | 691 | 0.0788038 | 0.229995 | 0.0411979 | 0.20495 | 0.493779 | 0.715896 | 0.0634424 | 0.315707 | 0.041 | 0.419557 | 0.0496056 | 0.207138 | 5.63514 | 17.0156 | 23.0049 | 1.00995 | 429.934 | 0.21015 | 0.0466038 | 0.0457014 | 0.368862 | 0.0811435 | 0.302055 | 0.302055 | 0.232174 |
| Recreation | 315 | 0.0387552 | 0.110423 | 0.100892 | 0.25324 | 0.838213 | 0.924367 | 0.0763259 | 0.37724 | 0.041 | 0.219587 | 0.066255 | 1.07376 | 2.51414 | 13.3588 | 21.6786 | 2.96937 | 40.7294 | 0.229002 | 0.0619002 | 0.0392036 | 0.953645 | 0.0768217 | 0.661963 | 0.661963 | 0.110288 |
| Reinsurance | 34 | 0.0468126 | 0.0589888 | 0.0763198 | 0.176817 | 0.919904 | 0.949215 | 0.0778615 | 0.23607 | 0.0355 | 0.191099 | 0.0680227 | 1.49073 | 0.878994 | 13.2191 | 14.8441 | 1.11494 | 19.6098 | -0.455141 | 0.00437726 | 0.00686545 | 0.278236 | 0.0611659 | 0.590329 | 0.590329 | 0.0589457 |
| Restaurant/Dining | 376 | 0.066971 | 0.109784 | 0.153008 | 0.22432 | 0.6672 | 0.847205 | 0.0715573 | 0.343998 | 0.041 | 0.293363 | 0.0595017 | 1.82525 | 2.78012 | 14.9862 | 27.4602 | 13.2507 | 75.3651 | -0.0151106 | 0.0486121 | 0.0230439 | 0.328717 | 0.421043 | 0.528502 | 0.528502 | 0.10075 |
| Retail (Automotive) | 184 | 0.0815734 | 0.0428594 | 0.0787349 | 0.250182 | 0.662416 | 0.976746 | 0.0795629 | 0.344488 | 0.041 | 0.421932 | 0.0588461 | 2.5074 | 0.85591 | 12.0864 | 21.2711 | 3.08783 | 42.5236 | 0.111432 | 0.0250905 | 0.0180964 | 0.770435 | 0.148621 | 0.341664 | 0.341664 | 0.0388307 |
| Retail (Building Supply) | 93 | 0.0414172 | 0.0977604 | 0.190602 | 0.257022 | 0.902901 | 1.08261 | 0.0861053 | 0.36343 | 0.041 | 0.230696 | 0.0732688 | 2.48652 | 1.79051 | 12.8813 | 18.8661 | 9.45611 | 65.7665 | 0.0801456 | 0.0242122 | 0.00649774 | 0.266198 | 0.329047 | 0.544027 | 0.544027 | 0.0948783 |
| Retail (Distributors) | 982 | 0.11518 | 0.0410069 | 0.0679195 | 0.233322 | 0.600529 | 0.920394 | 0.0760803 | 0.360682 | 0.041 | 0.47797 | 0.0542766 | 1.94368 | 0.719184 | 10.9006 | 16.715 | 1.28476 | 114.375 | 0.13943 | 0.0299566 | 0.0260478 | 0.46959 | 0.104369 | 0.404663 | 0.404663 | 0.0421855 |
| Retail (General) | 210 | 0.0156188 | 0.0429481 | 0.0836794 | 0.280049 | 0.855148 | 1.11939 | 0.0883785 | 0.291039 | 0.041 | 0.334736 | 0.0689921 | 2.76378 | 0.909444 | 11.2178 | 23.1883 | 2.85285 | 36.0102 | -0.00425417 | 0.0287033 | 0.00742721 | 0.328914 | 0.114657 | 0.501989 | 0.501989 | 0.0391294 |
| Retail (Grocery and Food) | 170 | 0.03248 | 0.0369109 | 0.0775601 | 0.268761 | 0.494938 | 0.727461 | 0.0641571 | 0.293054 | 0.041 | 0.437502 | 0.0494158 | 3.02642 | 0.739937 | 9.4734 | 22.4793 | 2.07179 | 243.189 | -0.0382072 | 0.0285817 | 0.00761014 | 0.296594 | 0.10177 | 0.567977 | 0.567977 | 0.0328764 |
| Retail (Online) | 297 | 0.144306 | 0.0506397 | 0.0668642 | 0.135466 | 1.23211 | 1.28205 | 0.0984308 | 0.518707 | 0.045 | 0.106347 | 0.0915186 | 1.58728 | 3.57833 | 23.7251 | 63.8107 | 7.51261 | 82.737 | -0.00497292 | 0.0467001 | 0.00506891 | 0.662546 | 0.167479 | 0.0895976 | 0.0895976 | 0.0478045 |
| Retail (Special Lines) | 479 | 0.0296802 | 0.0562634 | 0.11989 | 0.250905 | 0.748553 | 0.956785 | 0.0783293 | 0.375075 | 0.041 | 0.325338 | 0.0627566 | 2.45914 | 1.18574 | 10.2976 | 19.6956 | 3.34612 | 28.5816 | 0.0748701 | 0.0219836 | 0.00332951 | 0.243331 | 0.14114 | 0.414304 | 0.414304 | 0.0598785 |
| Rubber& Tires | 89 | 0.00635612 | 0.0856938 | 0.0859913 | 0.256125 | 0.720967 | 0.936451 | 0.0770727 | 0.286248 | 0.041 | 0.35424 | 0.0605616 | 1.16784 | 1.04322 | 6.63463 | 11.7953 | 1.22774 | 44.0172 | 0.212349 | 0.0580714 | 0.0337827 | 0.642921 | 0.0974565 | 0.413625 | 0.413625 | 0.0883605 |
| Semiconductor | 542 | 0.043407 | 0.181876 | 0.126065 | 0.145164 | 1.52958 | 1.57035 | 0.116248 | 0.388949 | 0.041 | 0.108413 | 0.106947 | 0.736144 | 4.38762 | 13.1089 | 23.7121 | 3.85702 | 80.321 | 0.170062 | 0.17069 | 0.139861 | 0.907499 | 0.145472 | 0.486334 | 0.486334 | 0.189017 |
| Semiconductor Equip | 291 | 0.0626273 | 0.163411 | 0.150994 | 0.161555 | 1.82108 | 1.83945 | 0.132878 | 0.409957 | 0.045 | 0.0932167 | 0.123608 | 1.02834 | 3.91126 | 17.3142 | 23.3731 | 4.64499 | 52.1327 | 0.29049 | 0.0688012 | 0.0822847 | 0.626724 | 0.173234 | 0.396022 | 0.396022 | 0.170245 |
| Shipbuilding & Marine | 345 | 0.0393031 | 0.0809 | 0.0444301 | 0.184674 | 0.708403 | 1.12974 | 0.0890179 | 0.338985 | 0.041 | 0.502599 | 0.0595883 | 0.625545 | 1.90805 | 9.57596 | 23.0898 | 1.05908 | 25.9695 | 0.0133693 | 0.0940756 | 0.0442345 | 0.675434 | 0.0517967 | 0.763182 | 0.763182 | 0.08155 |
| Shoe | 78 | -0.00372667 | 0.0974326 | 0.166605 | 0.179381 | 0.89886 | 0.953928 | 0.0781528 | 0.343747 | 0.041 | 0.115932 | 0.072624 | 2.0124 | 2.66787 | 18.8352 | 26.7822 | 5.98923 | 27.9651 | 0.199963 | 0.0168775 | -0.00282186 | 0.0468142 | 0.208015 | 0.368418 | 0.368418 | 0.0993163 |
| Software (Entertainment) | 280 | 0.16814 | 0.221527 | 0.163204 | 0.188738 | 1.17643 | 1.17593 | 0.0918726 | 0.552619 | 0.045 | 0.047687 | 0.0890858 | 0.759567 | 6.85561 | 21.158 | 30.9762 | 5.33176 | 90.6125 | 0.0310006 | 0.134862 | 0.0893038 | 0.579367 | 0.186972 | 0.036248 | 0.036248 | 0.238352 |
| Software (Internet) | 131 | 0.290074 | 0.0512778 | 0.0835007 | 0.156943 | 1.21968 | 1.29444 | 0.0991963 | 0.466744 | 0.045 | 0.129987 | 0.0906482 | 1.46181 | 5.03707 | 19.6279 | 53.9034 | 8.02903 | 62.0653 | 0.0357232 | 0.0768122 | 0.0820667 | 2.45645 | 0.00428249 | 5.80314 | 5.80314 | 0.0615347 |
| Software (System & Application) | 1375 | 0.151564 | 0.196291 | 0.181917 | 0.140002 | 1.24529 | 1.28312 | 0.0984971 | 0.504538 | 0.045 | 0.0851567 | 0.0929566 | 0.93091 | 7.70524 | 24.3466 | 35.5706 | 8.13277 | 99.4363 | 0.13721 | 0.0561654 | 0.0827022 | 0.590512 | 0.21169 | 0.32639 | 0.32639 | 0.21244 |
| Steel | 695 | 0.0640777 | 0.0743041 | 0.0644363 | 0.198889 | 0.822506 | 1.12566 | 0.0887658 | 0.370891 | 0.041 | 0.41413 | 0.0646209 | 0.986567 | 0.76403 | 5.92198 | 9.88241 | 0.901533 | 47.7266 | 0.13906 | 0.0493411 | 0.0270018 | 0.622087 | 0.0521454 | 0.609548 | 0.609548 | 0.0753918 |
| Telecom (Wireless) | 103 | 0.0291575 | 0.137842 | 0.0845659 | 0.280978 | 0.609311 | 0.901401 | 0.0749066 | 0.339743 | 0.041 | 0.432029 | 0.0557057 | 0.684471 | 2.31688 | 6.80642 | 15.9572 | 1.56404 | 30.6423 | -0.0518837 | 0.125597 | 0.00630773 | 0.229344 | 0.0627721 | 0.899944 | 0.899944 | 0.143648 |
| Telecom. Equipment | 474 | 0.0552776 | 0.10754 | 0.11143 | 0.239135 | 1.26553 | 1.31914 | 0.100723 | 0.426603 | 0.045 | 0.148259 | 0.0907469 | 1.11193 | 2.37018 | 14.1797 | 20.8836 | 3.63755 | 119.537 | 0.211344 | 0.0371413 | 0.0431971 | 0.69866 | 0.0769011 | 0.817749 | 0.817749 | 0.110214 |
| Telecom. Services | 317 | 0.0987671 | 0.15019 | 0.106238 | 0.233626 | 0.586761 | 0.889 | 0.0741402 | 0.390226 | 0.041 | 0.433023 | 0.055227 | 0.811916 | 2.35347 | 7.06091 | 15.5434 | 1.73506 | 92.7352 | 0.0150554 | 0.129452 | -0.0332476 | -0.305302 | 0.0775612 | 1.00794 | 1.00794 | 0.150991 |
| Tobacco | 54 | 0.0258259 | 0.319726 | 0.193221 | 0.271329 | 0.865627 | 1.03791 | 0.083343 | 0.295265 | 0.041 | 0.24469 | 0.0704038 | 0.732389 | 4.02881 | 11.1024 | 12.5415 | 3.4963 | 18.3251 | 0.193204 | 0.0354131 | 0.0232733 | 0.196994 | 0.208378 | 0.946643 | 0.946643 | 0.321116 |
| Transportation | 265 | 0.114581 | 0.0690741 | 0.101909 | 0.231975 | 0.794086 | 1.08767 | 0.0864179 | 0.327442 | 0.041 | 0.389504 | 0.0646233 | 1.77672 | 1.30486 | 10.4676 | 18.46 | 1.85637 | 85.8334 | 0.0309776 | 0.0521787 | 0.041031 | 0.980047 | 0.124009 | 0.607651 | 0.607651 | 0.0705185 |
| Transportation (Railroads) | 52 | 0.0703651 | 0.231812 | 0.0948385 | 0.248804 | 0.827269 | 1.04411 | 0.0837261 | 0.191455 | 0.0355 | 0.282283 | 0.0675373 | 0.520776 | 3.71075 | 10.9134 | 15.8219 | 2.47812 | 24.1784 | 0.100243 | 0.170651 | 0.118755 | 0.718314 | 0.15299 | 0.285748 | 0.285748 | 0.234585 |
| Trucking | 208 | 0.0608661 | 0.0189058 | 0.0426184 | 0.26864 | 0.654017 | 0.941328 | 0.0773741 | 0.325637 | 0.041 | 0.427405 | 0.057324 | 1.19721 | 1.46732 | 8.84417 | 46.0361 | 1.99907 | 21.0531 | 0.0802833 | 0.106014 | 0.0837704 | 14.6024 | -0.0388965 | 0.00336242 | 0.00336242 | 0.0409521 |
| Utility (General) | 52 | 0.0171982 | 0.0947637 | 0.0587045 | 0.185127 | 0.41409 | 0.654408 | 0.0596424 | 0.201263 | 0.0355 | 0.460422 | 0.0443261 | 0.762173 | 2.27735 | 12.5831 | 24.1037 | 1.71822 | 419.587 | -0.0189349 | 0.130844 | 0.0913008 | 1.17661 | 0.122356 | 0.589345 | 0.589345 | 0.0944539 |
| Utility (Water) | 99 | 0.117425 | 0.280301 | 0.076682 | 0.233136 | 0.693238 | 0.948737 | 0.077832 | 0.26754 | 0.041 | 0.38063 | 0.0598019 | 0.335069 | 4.9809 | 12.4705 | 17.8269 | 1.86071 | 30.3524 | 0.025092 | 0.257887 | 0.176035 | 1.1776 | 0.106868 | 0.623891 | 0.485344 | 0.277985 |
| Total Market | 44394 | 0.0837887 | 0.0928224 | 0.0614618 | 0.224375 | 0.79436 | 1.07702 | 0.0857601 | 0.392196 | 0.041 | 0.414918 | 0.0628164 | 0.752072 | 2.28317 | 14.0803 | 23.0803 | 1.90106 | 65.2442 | -1.17431 | 0.0587168 | 0.0396679 | 0.691296 | 0.106868 | 0.485344 | 0.485344 | 0.0941545 |
| Total Market (without financials) | 39677 | 0.080443 | 0.0978389 | 0.0977948 | 0.235812 | 0.915548 | 1.11233 | 0.0879421 | 0.403059 | 0.045 | 0.284864 | 0.072415 | 1.13134 | 1.88921 | 11.1865 | 18.6627 | 2.26151 | 66.0653 | 0.10921 | 0.0632418 | 0.0409958 | 0.69362 | 0.104097 | 0.547234 | 0.547234 | 0.0993745 |

---

## Sheet: Stories to Numbers (reporting only)

No new inputs except free-text narrative (A3, the "story") and the "Link to story" text notes in column G. Everything else mirrors the Valuation output: assumptions block (rows 8–14), year-by-year cash-flow table (rows 16–27: revenues, margin, EBIT, EBIT(1−t), reinvestment, FCFF), and the value build (rows 29–39). One derived cell of note: F12 stable-period reinvestment rate `='Valuation output'!M2/'Valuation output'!M40` = g/ROC = 0.0156/0.15 = 0.104. D13 marginal ROIC `=Diagnostics!B6`. A Python port can regenerate this sheet entirely from the engine's outputs.

## Sheet: Diagnostics (derived checks)

- B2 invested capital at start `='Valuation output'!B39` = 27,818.4
- B3 invested capital at end `='Valuation output'!L39` = 145,185.4
- B4 change over 10 years `=B3-B2` = 117,367.0
- B5 change in EBIT(1−t) over 10 years `='Valuation output'!L5-'Valuation output'!B5` = 60,626.9 (NOTE: uses pre-tax EBIT cells L5/B5 despite the after-tax label — reproduce verbatim)
- B6 marginal ROIC `=B5/B4` = 0.516559
- B7 ROIC at end `='Valuation output'!L40` = 0.342376
- B8 average compounded WACC `=(1/'Valuation output'!L13)^(1/10)-1` = 0.060180
- B9 value as % of price `='Valuation output'!B33/'Valuation output'!B34` = 0.476074
- B10 verdict: `=IF(B9="NA","Value is negative. See below",IF(B9>2,"Value seems high. See below",IF(B9<0.5,"Value seems low. See below"," ")))` → "Value seems low. See below"

Guidance table (rows 11–15, text): if value looks too low → increase revenue growth / increase target margin / decrease sales-to-capital / raise terminal ROC vs cost of capital; if too high → do the opposite.

## Sheet: Summary Sheet (restatement of the engine)

Pure re-derivation of the Valuation output in tabular form; no new inputs. Three tables:
1. Rows 1–12: per-year revenues, growth, margin, pre-tax operating income (`=B*D`), NOL, taxes (`=E-H`, backed out), after-tax operating income (all linked to Valuation output).
2. Rows 14–25: after-tax operating income, change in revenues, sales-to-capital, reinvestment (`=ΔRev/S2C`), FCFF, cumulative capital invested, implied ROC (`=ATOI/capital`).
3. Rows 27–37: per-year cost of capital only (beta/cost-of-equity/debt columns are headers with blank bodies — the granular WACC build is not populated in this workbook).
4. Rows 39–50: discounting check — cumulated cost of capital `=prev*(1+r_t)`, FCFF, terminal value added in year 10, `PV = (FCFF + TV)/cumulated factor`, F50 `=SUM(F40:F49)` = 686,689.9 (ties to 'Valuation output'!B21).

## Sheet: Trailing 12 month (standalone helper; sample data is NOT Tesla)

Utility for building trailing-12-month financials from a fiscal-year 10-K plus two part-year periods. Core formula, every row: `Trailing 12M (E) = Last 10K (B) − First X months of last year (C) + First X months of current year (D)`. Rows: Revenues, R&D, Operating income/EBIT, Interest expenses, Book equity/debt (point-in-time, no formula), Cash, effective tax rate (`=taxes/pretax income` per period, e.g. B14 `=15885/61372`), lease commitments year 1–5 and beyond, G&A, Marketing, Content Costs. The populated numbers (revenues 17,630.3 TTM, content costs, etc.) are leftovers from a different company (a streaming firm), kept as a worked example of the technique. Not linked into the Tesla valuation.

## Sheet: Answer keys (dropdown lists)

Validation lists for the dropdowns:
- Yes/No
- B/V (book vs fair-value distress proceeds)
- ERP choices: {Will input, Country of incorporation, Operating countries, Operating regions}
- Cost of debt: {Direct input, Synthetic rating, Actual rating}
- Synthetic rating firm type: {1, 2}
- Beta: {Direct input, Single Business(US), Single Business(Global), Multibusiness(US), Multibusiness(Global)}
- Ratings: {Aaa/AAA, Aa2/AA, A1/A+, A2/A, A3/A-, Baa2/BBB, Ba1/BB+, Ba2/BB, B1/B+, B2/B, B3/B-, C2/C, Ca2/CC, Caa/CCC, D2/D}

---

## Outputs (whole workbook)

| Output | Cell | Current value | Meaning |
|---|---|---|---|
| Value of operating assets | Valuation output B24 | 686,689.9 | PV of 10-yr FCFF + PV of terminal value, failure-adjusted |
| Value of equity | Valuation output B29 | 692,626.9 | Operating assets − debt − minority + cash + non-op assets |
| Value of options | Valuation output B30 | 51,070.2 | Dilution-adjusted BS value of employee options |
| Estimated value / share | Valuation output B33 | **571.29** | (Equity − options)/shares — the headline answer |
| Price as % of value | Valuation output B35 | 2.1005 | 1200/571.29 → stock ~110% overvalued on these inputs |
| Diagnostics verdict | Diagnostics B10 | "Value seems low. See below" | Sanity-check message |

## Worked example (current sheet state, end to end)

1. Master Inputs: growth 35%, target margin 16% (by year 5), sales/capital 4 (years 1–5) → 2.667 (years 6–10), initial WACC 6%, failure probability 0. Overrides: terminal ROC 15% ("Yes" on B43); everything else default. Riskfree 1.56%.
2. Base year: revenues 46,848. EBIT = 4,586 + R&D adjustment 1,064.4 = 5,650.4 → base margin 12.06%. Invested capital = 28,494 + 10,158 − 16,095 + 5,261.4 (research asset) = 27,818.4.
3. Years 1–5: revenues grow 35%/yr to 210,068.0; margin interpolates 12.85% → 16% by year 5; tax rate fixed at 11.99%; reinvestment = ΔRev/4. Year 1: EBIT 8,126.3, EBIT(1−t) 7,152.0, reinvestment 4,099.2, FCFF 3,052.8, PV at 6% = 2,880.0.
4. Years 6–10: growth fades 28.312% → 1.56%; margin flat 16%; tax rate walks to 25%; sales/capital 2.667; WACC walks 6% → 6.06%. Year 10: revenues 414,233.4, EBIT 66,277.3, EBIT(1−t) 49,708.0, reinvestment 2,386.0, FCFF 47,322.0, cumulative DF 0.557448, PV 26,379.5.
5. Terminal year: g 1.56%, revenues 420,695.4, EBIT(1−t) 50,483.5, reinvestment = (0.0156/0.15)×50,483.5 = 5,250.3, FCFF 45,233.2. TV = 45,233.2/(0.0606−0.0156) = 1,005,181.6; PV(TV) = ×0.557448 = 560,336.0.
6. PV years 1–10 = 126,353.9. Operating assets = 686,689.9 (failure prob 0). Equity = 686,689.9 − 10,158 + 16,095 = 692,626.9.
7. Options (iterated to convergence):
   - S_adj = (571.288×1123 + 502.561×101.62)/1224.62 = 565.585.
   - d1 = 3.39747, N(d1) = 0.99966. d2 = 2.67497, N(d2) = 0.99626.
   - Value/option = 565.585×0.99966 − 69.04×e^(−0.0156×5.8)×0.99626 = 502.561. Total = 51,070.2.
8. Value/share = (692,626.9 − 51,070.2)/1,123 = **571.29** vs price 1,200 → price/value 2.10; Diagnostics flags "Value seems low."

## Reimplementation notes (Python port)

**Inputs (name, type, units):**
- Base year: revenues, ebit, interest_expense, bv_equity, bv_debt, cash, non_operating_assets, minority_interests (float, $M); shares_outstanding, stock_price (float); effective_tax_rate, marginal_tax_rate (float, decimals); riskfree_rate (float).
- Drivers: growth_yrs_1_5, target_margin, convergence_year (int, default 5), sales_to_capital_1_5 (yrs 6–10 = ×2/3), initial_wacc.
- Flags/overrides:
  - capitalize_rnd (bool) + rnd inputs {life int ≤10, current_rnd, past_rnd list}
  - has_leases (bool) + lease inputs {current_expense, commitments[5], beyond_lump, pre_tax_cost_of_debt}
  - override_terminal_wacc (bool, value); override_terminal_roc (bool, value)
  - failure_prob (float) + distress_mode ("B"|"V") + distress_pct
  - freeze_tax_at_effective (bool); nol_carryforward (float)
  - override_perpetual_growth (bool, value)
  - trapped_cash (float) + foreign_tax_rate
  - has_options (bool) + {n_options, strike, maturity, sigma, dividend_yield}
- Optional cost-of-capital stack: beta approach + segments, ERP approach + country revenue weights, cost-of-debt approach + rating or firm type.

**Outputs:** per-year schedule (growth, revenues, margin, EBIT, tax rate, EBIT(1−t), NOL, reinvestment, FCFF, S2C, invested capital, ROIC, WACC, DF, PV), terminal block, value bridge (operating assets → equity → per share), diagnostics.

**Branches and edge cases:**
- Iteration: option value ↔ value/share is circular. Iterate: start S = equity/shares ignoring options; compute option value (itself circular through S_adj — solve that inner fixed point too, or jointly); subtract; recompute until |Δvalue/share| < tol. Converges fast (contraction).
- Negative EBIT: no taxes (`EBIT(1−t) = EBIT` when EBIT ≤ 0); losses accumulate in the NOL balance and shelter later profits (full shelter while EBIT < NOL, marginal taxation above it).
- Zero interest expense → coverage ratio 1,000,000 (best rating); negative EBIT → coverage −100,000 (worst rating).
- Terminal growth ≤ 0 → terminal reinvestment = 0. Terminal g must stay < terminal WACC or the TV denominator flips sign — the sheet does not guard this; a port should validate.
- Sales-to-capital of 0 would divide by zero in reinvestment — validate.
- Stage boundaries: growth constant years 1–5, then 5 equal linear steps to terminal g reached AT year 10 (year-10 growth = terminal g). Margin converges by `convergence_year` (not year 10). Tax rate constant years 1–5, 5 equal steps to marginal at year 10. WACC constant years 1–5, 5 equal steps to terminal WACC at year 10. Sales/capital jumps once at year 6.
- Distress proceeds: "B" mode uses (BV equity + BV debt) × pct — book values, not invested capital; "V" uses the pre-failure sum-of-PV × pct.
- All range VLOOKUPs (rating tables, coverage tables, scenario menus) are approximate-match on a sorted first column: pick the last row whose key ≤ lookup value. Replicate with bisect, not exact match.
- Known quirks to reproduce (or consciously fix):
  - The country default spread lookup range A5:C179 truncates the alphabet. It returns a wrong spread for late-alphabet countries like "United States".
  - Diagnostics B5 uses pre-tax EBIT despite its after-tax label.
  - Table 3 (rating→spread) has the C2/C and Caa/CCC spread values swapped vs the coverage tables.
  - Base-year margin divides R&D/lease-adjusted EBIT by unadjusted revenues.
- The DCF's cost of capital is the Master-Inputs number, NOT the bottom-up WACC worksheet output. Keep the worksheet as an optional estimator module.
- Units: everything $ millions; options and shares in millions so option value nets directly off equity value.

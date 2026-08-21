# Damodaran spreadsheet documentation — fcffsimpleginzu.xlsx

Source: `/Users/kushaldsouza/Downloads/2020/Spreadsheets/Big Picture Valuation Spreadsheets/fcffsimpleginzu.xlsx` (January 2022 data vintage; workbook says "Updated on January 2022 with 2022 Industry averages and risk premiums"). All formulas below are verbatim from the .xlsx unless flagged "(inferred)". The workbook requires Excel iterative calculation because the cost of capital depends on the synthetic rating, which depends on the cost of debt (circularity when the synthetic-rating path is used).

### fcffsimpleginzu.xlsx

**Purpose:** Damodaran's flagship "Ginzu" simple FCFF (free cash flow to firm) valuation model. It values any company from a small set of story-driven inputs: base-year financials, a revenue-growth path, a target operating margin, sales-to-capital ratios for reinvestment, and a cost of capital that fades to a mature-company level. It produces a 10-year explicit forecast plus terminal value, adjusts for probability of failure, nets out debt/minority interests, adds cash/cross-holdings, subtracts employee-option value, and delivers an intrinsic value per share compared to price. Damodaran uses it as his default DCF for almost any publicly traded non-financial company ("stories to numbers"). Sub-modules: cost-of-capital builder (bottom-up beta, multi-region ERP, synthetic rating), R&D capitalizer, operating-lease converter, Black-Scholes employee-option valuer, trailing-12-month input helper.

The workbook currently contains a worked valuation of **SK Innovation** (Korea, valued 2022-01-01, units = millions of KRW; share counts in millions).

---

## Sheet: "Input sheet" (all user inputs)

**Inputs** (label — cell — current example value):

Base year financials:
- Date of valuation — B1 — 2022-01-01
- Company name — B2 — "SK Innovation"
- Country of incorporation — B5 — "Korea" (must match a row in 'Country equity risk premiums' A5:A181)
- Industry (US) — B6 — "Software (System & Application)" (must match 'Industry Averages(US)' col A)
- Industry (Global) — B7 — "Software (System & Application)" (must match 'Industry Average Beta (Global)' col A)
- Revenues: This year — B8 — 32,357,222; Last year — C8 — 49,306,938; Years since last 10K — D8 — 1.25
- Operating income (EBIT): This year — B9 — −250,829; Last year — C9 — 1,113,646; D9 — 1.25
- Interest expense — B10 — 351,778 (C10 last year 349,904)
- Book value of equity — B11 — 14,405,108 (C11 17,468,081)
- Book value of debt — B12 — 16,715,192 (C12 14,751,920)
- Capitalize R&D? — B13 — "Yes" (Yes/No; if Yes, fill the 'R& D converter' sheet)
- Operating lease commitments? — B14 — "No" (Yes/No; if Yes, fill 'Operating lease converter')
- Cash and marketable securities — B15 — 6,699,463
- Cross holdings and other non-operating assets — B16 — 0
- Minority interests — B17 — 0
- Number of shares outstanding — B18 — 83.6
- Current stock price — B19 — 273,500
- Effective tax rate — B20 — 0.25
- Marginal tax rate — B21 — 0.25

Value drivers:
- Revenue growth rate for next year — B23 — 0.50
- Operating margin for next year — B24 — 0.03
- CAGR revenue growth, years 2–5 — B25 — 0.05 ("Growth lever")
- Target pre-tax operating margin (year 10) — B26 — 0.075 ("Profitability lever")
- Year of convergence (for margin) — B27 — 10
- Sales-to-capital ratio, next year — B28 — 10
- Sales-to-capital ratio, years 2–5 — B29 — 5
- Sales-to-capital ratio, years 6–10 — B30 — 1.5

Market numbers:
- Riskfree rate — B32 — 0.0169
- Initial cost of capital — B33 — `='Cost of capital worksheet'!E50` = 0.07312245558035507 (computed, not typed)

Employee options:
- Options outstanding? — B35 — "No"
- Number of options — B36 — 7.72; Average strike — B37 — 1.29; Average maturity — B38 — 7; Std dev of stock price — B39 — 0.45

Default-assumption overrides (each is a Yes/No toggle plus a conditional input):
- Override stable-period cost of capital? — B43 — "No"; if Yes, cost of capital after year 10 — B44 — 0.075. Default: riskfree + mature-market ERP.
- Override "ROC = cost of capital after year 10"? — B46 — "No"; if Yes, stable ROC — B47 — 0.10
- Override "no chance of failure"? — B49 — "Yes"; probability of failure — B50 — 0.12
- Tie distress proceeds to — B51 — "V" ("B" = book value of capital, "V" = estimated fair value)
- Distress proceeds as % of book/fair value — B52 — 0.50
- Override "effective tax rate → marginal by terminal year"? — B54 — "No" (if Yes, tax rate stays at effective forever)
- Override "no NOL carryforward"? — B56 — "Yes"; NOL carried into year 1 — B57 — `=474.8+256.6` = 731.4
- Override "today's riskfree rate prevails in perpetuity"? — B59 — "Yes"; riskfree rate after year 10 — B60 — 0.02
- Override "perpetuity growth = riskfree rate"? — B62 — "No"; if Yes, growth in perpetuity — B63 — −0.05 (can be negative)
- Override "no trapped cash"? — B65 — "No"; trapped cash — B66 — 140,000; average foreign tax rate on it — B67 — 0.15

**Diagnostic feedback block (Input sheet, columns E–K, computed):**
- I22 company revenue growth (most recent year, annualized): `=IF(C8>0,(B8/C8)^(1/D8)-1,"NA")` → −0.28608
- J22/K22 industry growth: `=VLOOKUP(B6,'Industry Averages(US)'!A2:S95,3)` / `=VLOOKUP(B7,'Industry Average Beta (Global)'!A2:N95,3)`
- I23 company pre-tax margin `='Valuation output'!B4`; J23/K23 industry margin = VLOOKUP col 4
- I24 sales-to-capital `=B8/'Valuation output'!B39`; J24/K24 = VLOOKUP col 14
- I25 ROIC `='Valuation output'!B7/'Valuation output'!B39`; J25/K25 = VLOOKUP col 5
- J26/K26 industry std dev of stock prices = VLOOKUP col 10; J27/K27 industry cost of capital = VLOOKUP col 13
- J30 revenues in year 10 `='Valuation output'!M3`; J31 pre-tax operating income in year 10 `='Valuation output'!M5`; J32 ROIC in year 10 `='Valuation output'!L40`

---

## Sheet: "Valuation output" (the DCF engine)

Layout: column B = base year, C..L = years 1–10, M = terminal year. Row-by-row logic:

**Row 2 — Revenue growth rate:**
- C2 `='Input sheet'!B23` (year-1 growth)
- D2 `='Input sheet'!B25`; E2..G2 `=previous` (years 2–5 constant at CAGR input)
- H2..L2 linear fade to terminal growth over years 6–10: H2 `=G2-((G2-$M$2)/5)`, I2 `=G2-((G2-$M$2)/5)*2`, ... L2 `=G2-((G2-$M$2)/5)*5`
- M2 terminal growth `=IF('Input sheet'!B62="Yes",'Input sheet'!B63,IF('Input sheet'!B59="Yes",'Input sheet'!B60,'Input sheet'!B32))` — i.e. explicit override > post-year-10 riskfree > current riskfree.

**Row 3 — Revenues:** B3 `='Input sheet'!B8`; each year `=prev*(1+growth)`; M3 `=L3*(1+M2)`.

**Row 4 — EBIT (operating) margin:**
- B4 `=B5/B3` (base margin from adjusted EBIT)
- C4 `='Input sheet'!B24` (next-year margin)
- D4..G4 `=IF(year>B27, B26, B26-((B26-$C$4)/B27)*(B27-year))` — linear convergence from the *year-1* margin C4 to target B26 by year B27
- H4..L4 same formula but anchored on the *base-year* margin `$B$4`: `=IF(year>B27,B26,B26-((B26-$B$4)/B27)*(B27-year))`. NOTE: this anchor switch (C4 for years 2–5, B4 for years 6–10) is exactly what the spreadsheet does — with a negative base margin it produces the non-monotone dip seen at year 6 (0.0525 → 0.0424). Reproduce verbatim for fidelity.
- M4 `=L4`.

**Row 5 — EBIT:** yearly `=margin*revenue`. Base-year B5 folds in R&D and lease adjustments:
`=IF(B14="Yes", IF(B13="Yes", B9+'Operating lease converter'!F32+'R& D converter'!D39, B9+'Operating lease converter'!F32), IF(B13="Yes", B9+'R& D converter'!D39, B9))` (refs to Input sheet) → −250,829 + 40,434.8 = −210,394.2. N5 `=M5-B5` (info only).

**Row 6 — Tax rate:** B6 `='Input sheet'!B20` (effective); C6..G6 `=prev` ; H6..L6 ramp to marginal: `=prev+($M$6-$G$6)/5`; M6 `=IF('Input sheet'!B54="Yes",'Input sheet'!B20,'Input sheet'!B21)`.

**Row 10 — NOL (compute before row 7):** B10 `=IF('Input sheet'!B56="Yes",'Input sheet'!B57,0)`; each year `=IF(EBIT_t<0, NOL_{t-1}-EBIT_t, IF(NOL_{t-1}>EBIT_t, NOL_{t-1}-EBIT_t, 0))` — losses add to the NOL; profits burn it down to 0.

**Row 7 — EBIT(1−t) with NOL shield:** B7 `=IF(B5>0,B5*(1-B6),B5)`. Years 1–10 (e.g. C7): `=IF(C5>0, IF(C5<B10, C5, C5-(C5-B10)*C6), C5)` — if EBIT ≤ 0 no taxes; if EBIT < prior NOL, fully sheltered; else tax only the excess over prior NOL. M7 `=M5*(1-M6)` (no NOL in terminal year).

**Row 38 — Sales-to-capital ratio:** C38 `='Input sheet'!B28`; D38 `='Input sheet'!B29`; E38,F38 `=prev`; G38 `='Input sheet'!B30`; H38..L38 `=prev`. (So year 1 uses B28, years 2–4 use B29, years 5–10 use B30. Note: year 5 already uses the "years 6–10" ratio — the labels on the Input sheet say 2–5 and 6–10, but the grid switches at year 5.)

**Row 8 — Reinvestment:** C8 `=IF(C3>B3,(C3-B3)/C38,0)` (year 1 floors at 0 if revenue shrinks); D8..L8 `=(Rev_t-Rev_{t-1})/S2C_t` (no floor); terminal M8 `=IF(M2>0,(M2/M40)*M7,0)` — reinvestment rate = g/ROC applied to terminal EBIT(1−t), zero if terminal growth ≤ 0. N8 `=SUM(C8:M8)`.

**Row 9 — FCFF:** `=EBIT(1-t) − Reinvestment` each year, incl. M9.

**Row 12 — Cost of capital:** C12 `='Input sheet'!B33` (initial WACC); D12..G12 `=prev`; H12..L12 linear fade: `=prev-($G$12-$M$12)/5`; M12 terminal `=IF('Input sheet'!B43="Yes",'Input sheet'!B44, IF('Input sheet'!B59="Yes", 'Input sheet'!B60+'Country equity risk premiums'!B1, 'Input sheet'!B32+'Country equity risk premiums'!B1))` — default is riskfree (post-10 if overridden) + mature-market ERP ('Country equity risk premiums'!B1 = 0.0424). (Comment in sheet says "riskfree + 4.5%", implementation uses the mature-market ERP cell.)

**Row 13 — Cumulated discount factor:** C13 `=1/(1+C12)`; thereafter `=prev*(1/(1+r_t))`.

**Row 14 — PV(FCFF):** `=FCFF_t * DF_t`.

**Rows 39–40 — Invested capital & ROIC:**
- B39 invested capital base `= BV equity + BV debt − Cash (+ lease debt F33 if leases) (+ R&D asset D35 if R&D)`; verbatim: `=IF(B14="Yes",IF(B13="Yes",B11+B12-B15+'Operating lease converter'!F33+'R& D converter'!D35, B11+B12-B15+'Operating lease converter'!F33), IF(B13="Yes", B11+B12-B15+'R& D converter'!D35, B11+B12-B15))` → 14,405,108+16,715,192−6,699,463+723,486.2 = 25,144,323.2
- C39..L39 `=prev + Reinvestment_t`
- Row 40 ROIC `=EBIT(1-t)_t / InvCap_t`; M40 terminal ROC `=IF('Input sheet'!B46="Yes",'Input sheet'!B47,'Valuation output'!L12)` — default: terminal ROC = terminal cost of capital.

**Terminal value & equity bridge (column B, rows 16–35):**
- B16 terminal cash flow `=M9`
- B17 terminal cost of capital `=M12`
- B18 terminal value `=B16/(B17-M2)`
- B19 PV(TV) `=B18*L13` (discounted at year-10 cumulative factor)
- B20 PV of years 1–10 `=SUM(C14:L14)`
- B21 Sum of PV `=B19+B20`
- B22 probability of failure `=IF('Input sheet'!B49="Yes",'Input sheet'!B50,0)`
- B23 proceeds if firm fails `=IF('Input sheet'!B51="B",('Input sheet'!B11+'Input sheet'!B12)*'Input sheet'!B52, B21*'Input sheet'!B52)`
- B24 value of operating assets `=B21*(1-B22)+B23*B22`
- B25 − Debt `=IF('Input sheet'!B14="Yes",'Input sheet'!B12+'Operating lease converter'!C28,'Input sheet'!B12)`
- B26 − Minority interests `='Input sheet'!B17`
- B27 + Cash `=IF('Input sheet'!B65="YES",'Input sheet'!B15-'Input sheet'!B66*('Input sheet'!B21-'Input sheet'!B67),'Input sheet'!B15)` — NOTE: the trapped-cash penalty is `trapped_cash × (marginal_tax − foreign_tax)`. Also note the comparison string is "YES" while the input dropdown holds "Yes"/"No"; in Excel text comparison is case-insensitive so "Yes" triggers it — in Python compare case-insensitively.
- B28 + Non-operating assets `='Input sheet'!B16`
- B29 value of equity `=B24-B25-B26+B27+B28`
- B30 − value of options `=IF('Input sheet'!B35="No",0,'Option value'!D27)`
- B31 equity in common stock `=B29-B30`
- B32 shares `='Input sheet'!B18`; B33 value/share `=B31/B32`; B34 price `='Input sheet'!B19`; B35 price as % of value `=B34/B33`.

---

## Sheet: "Cost of capital worksheet"

Computes the initial (year 1–5) cost of capital, E50, consumed by Input sheet B33.

**Inputs:**
- B6 shares `='Input sheet'!B18`; B7 price `='Input sheet'!B19`
- B9 approach for beta — "Multibusiness(Global)" (choices per Answer keys: Direct input / Single Business(US) / Single Business(Global) / Multibusiness(US) / Multibusiness(Global))
- B10 direct-input levered beta — 1.2 (used only if B9="Direct Input")
- B12 riskfree `='Input sheet'!B32`
- B13 ERP approach — "Operating regions" (choices: Will input / Country of incorporation / Operating countries / Operating regions)
- B14 direct ERP — 0.06
- B18 book value of straight debt `='Input sheet'!B12`; B19 interest expense `='Input sheet'!B10`; B20 average maturity — 3
- B21 approach for pre-tax cost of debt — "Actual rating" (choices: Direct input / Synthetic rating / Actual rating)
- B22 direct pre-tax cost of debt — 0.04; B23 actual rating — "Baa2/BBB"; B24 type of company for synthetic rating — 2 (1 = large manufacturing, 2 = smaller/riskier, 3 = financial service — the third lookup table F19:I33 is empty in this workbook)
- B26 marginal tax rate `='Input sheet'!B21`
- B28–B31 convertible debt: book value 0, interest 0, maturity 0, market value 0
- B33 debt value of operating leases `=IF('Input sheet'!B14="Yes",'Operating lease converter'!F33,0)`
- B36–B38 preferred: # shares 0, price 70, dividend/share 5

**Beta:**
- B11 unlevered beta `=IF(B9="Single Business(US)", VLOOKUP('Input sheet'!B6,'Industry Averages(US)'!A2:G95,7), IF(B9="Multibusiness(US)", K48, IF(B9="Single Business(Global)", VLOOKUP('Input sheet'!B7,'Industry Average Beta (Global)'!A2:G95,7), K64)))` → 1.14316 (Multibusiness Global)
- C45 levered beta `=IF(B9="Direct Input", B10, B11*(1+(1-B26)*(C48/B48)))` → 1.14316×(1+0.75×(16,161,914/22,864,600)) = 1.74920

**Multibusiness beta calculators (bottom-up, revenue-weighted by estimated value):**
- US version rows 36–48: per business, I `=VLOOKUP(business,'Industry Averages(US)'!A2:S95,15)` (EV/Sales), J `=Revenues*EV/Sales`, K `=VLOOKUP(...,7)` (unlevered beta); K48 = Σ K_i × J_i/J48 (value-weighted average). Example rows: Computers/Peripherals 25,484; Entertainment 18,805; Computer Services 37,190; Telecom. Equipment 166,699.
- Global version rows 52–64, identical structure against 'Industry Average Beta (Global)': Oil/Gas (Production and Exploration) 81,363; Chemical (Basic) 14,862; Chemical (Specialty) 4,608; Electronics (General) 2,010; Metals & Mining 59,269 → K64 = 1.1431615148698169 (this is the beta actually used).

**ERP:**
- B15 `=IF(B13="Will Input", B14, IF(B13="Country of Incorporation", VLOOKUP('Input sheet'!B5,'Country equity risk premiums'!A5:E181,4), IF(B13="Operating regions", K32, K18)))` → 0.05174663 (Operating regions)
- Operating *countries* calculator (G5:K18): per country, ERP `=VLOOKUP(country,'Country equity risk premiums'!$A$5:$D$181,4)`, weight = revenues/total, K18 = Σ weight×ERP. Current rows: United States 15,000 (ERP .0424), Australia 6,000 (.0424), Rest of the World 7,782 with hand-entered ERP .0618 → K18 = 0.047645.
- Operating *regions* calculator (G21:K32): region ERPs pulled from 'Country equity risk premiums' rows 185–193 (GDP-weighted regional averages); last rows free-form (here "South Korea" 66,423 with ERP .052 typed in). Current: Asia 27,899 (.0528), North America 4,355 (.0424), Western Europe 5,389 (.05072), South Korea 66,423 (.052) → K32 = 0.0517466 (used).

**Cost of debt:**
- B25 pre-tax cost of debt `=IF(B21="Direct Input", B22, IF(B21="Synthetic Rating", 'Synthetic rating'!D13, B12+VLOOKUP(B23,'Synthetic rating'!G39:H53,2)))` → 0.0169 + spread(Baa2/BBB)=0.01591065804294902 → 0.03281066. (Actual-rating path = riskfree + rating spread from the G39:H53 rating→spread list; NO country default spread is added on this path, while the synthetic path D13 includes it.)
- C41 market value of straight debt `=B19*(1-(1+B25)^(-B20))/B25 + B18/(1+B25)^B20` (bond-pricing: interest as annuity + face at maturity) → 16,161,914
- C42 straight-debt value inside convertible `=B29*(1-(1+B25)^(-B30))/B25+B28/(1+B25)^B30`; C44 equity part of convertible `=B31-C42`
- C43 lease debt `=B33`

**Weights and WACC (rows 47–50):**
- B48 MV equity `=B6*B7` = 22,864,600; C48 MV debt `=C41+C42+C43`; D48 preferred `=B36*B37`; E48 total
- Weights row 49 `=component/E48` → E: 0.585873, D: 0.414127, P: 0
- B50 cost of equity `=B12+C45*B15` = 0.0169+1.74920×0.0517466 = 0.10741506
- C50 after-tax cost of debt `=B25*(1-B26)` = 0.02460799
- D50 cost of preferred `=B38/B37` = 0.0714286
- **E50 cost of capital `=B49*B50+C49*C50+D49*D50` = 0.07312245558035507**

---

## Sheet: "Synthetic rating"

**Inputs (auto-fed):** C4 firm type `='Cost of capital worksheet'!B24` (1/2/3); F5 EBIT `=IF('Input sheet'!B14="Yes",'Input sheet'!B9+'Operating lease converter'!F32,'Input sheet'!B9)` (lease-adjusted, NOT R&D-adjusted) → −250,829; F6 interest expense `=IF('Input sheet'!B14="Yes",'Cost of capital worksheet'!B19+'Operating lease converter'!C28*'Operating lease converter'!C15,'Cost of capital worksheet'!B19)` (adds imputed lease interest = lease debt × pre-tax cost of debt when leases on) → 351,778; F7 riskfree `='Input sheet'!B32`.

**Logic:**
- D9 interest coverage ratio `=IF(F6=0, 1000000, IF(F5<0, -100000, F5/F6))` — zero interest → +1,000,000 (best rating); negative EBIT → −100,000 (worst, D rating).
- D10 rating `=IF(C4=1, VLOOKUP(D9,A19:D33,3), IF(C4=2, VLOOKUP(D9,A38:D52,3), VLOOKUP(D9,F19:I33,3)))` (range lookup on the lower bound column; table F19:I33 for financial-service firms is EMPTY in this workbook — type 3 would #N/A/#REF)
- D11 company default spread — same VLOOKUPs, column 4
- D12 country default spread `=VLOOKUP('Input sheet'!B5,'Country equity risk premiums'!A5:C181,3)` → 0.00422187 (Korea)
- D13 cost of debt `=F7+D11+D12`
- Current outputs: coverage −100,000 → rating "D2/D", company spread 0.14335607, cost of debt 0.16447795 (not used, since B21="Actual rating").

**Reference table 1 — large manufacturing firms (type 1), A19:D33.** Interval is (greater than, ≤ to]:

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

**Reference table 2 — smaller and riskier firms (type 2), A38:D52:**

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

**Reference table 3 — rating → spread list (G39:H53), used by the "Actual rating" cost-of-debt path:**

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

(Note: this list is stored alphabetically; the VLOOKUP on it is effectively an exact-match need — Excel's default range VLOOKUP works here because the list happens to be sorted ascending as text. A Python port should do an exact dict lookup.)

**Reference table 4 — cumulative default probabilities by rating, 1–10 year horizons (J17:T24; informational, not referenced by formulas):**

| Rating | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| AAA | 0 | 0.0003 | 0.0013 | 0.0024 | 0.0035 | 0.0045 | 0.0051 | 0.0059 | 0.0064 | 0.007 |
| AA | 0.0002 | 0.0006 | 0.0012 | 0.0021 | 0.0031 | 0.0042 | 0.005 | 0.0058 | 0.0065 | 0.0072 |
| A | 0.0005 | 0.0014 | 0.0023 | 0.0035 | 0.0047 | 0.0062 | 0.0079 | 0.0093 | 0.0108 | 0.0124 |
| BBB | 0.0016 | 0.0045 | 0.0078 | 0.0117 | 0.0158 | 0.0198 | 0.0233 | 0.0267 | 0.03 | 0.0332 |
| BB | 0.0061 | 0.0192 | 0.0348 | 0.0505 | 0.0652 | 0.0785 | 0.0901 | 0.1004 | 0.1097 | 0.1178 |
| B | 0.0333 | 0.0771 | 0.1155 | 0.1458 | 0.1693 | 0.1883 | 0.2036 | 0.216 | 0.227 | 0.2374 |
| CCC/C | 0.2708 | 0.3664 | 0.4141 | 0.441 | 0.4619 | 0.4709 | 0.4826 | 0.4905 | 0.4976 | 0.5038 |

---

## Sheet: "R& D converter"

Capitalizes R&D as an asset amortized straight-line over N years.

**Inputs:** F6 amortization years N — 5 (max 10); F7 current-year R&D — 251,563; B11..B20 past R&D by year (year −1 first): −1: 253,611; −2: 227,441; −3: 233,578; −4: 195,693; −5: 145,318. (Column A auto-fills year indices: A12 `=IF((0-A11)<$F$6, IF(A11>-1,, A11-1),)` — extends back only N years.)

**Logic (rows 24–34):** for year index a (0 = current, −k = k years ago):
- unamortized fraction C `= 1` for current year, else `=IF(a<0, (N+a)/N, 0)`
- unamortized value D `=B*C`
- amortization this year E `=IF(a<0, B/N, 0)` (current year's R&D not amortized this year)
- **D35 Value of research asset** `=SUM(D24:D34)` → 723,486.2 (added to invested capital)
- E35 = D37 amortization of asset for current year `=SUM(E25:E34)` → 211,128.2
- **D39 adjustment to operating income** `=F7-D37` = 251,563 − 211,128.2 = 40,434.8 (added to reported EBIT; positive = increase)
- D40 tax effect `=D39*'Input sheet'!B21` (informational)

---

## Sheet: "Operating lease converter"

Converts lease commitments to debt (pre-IFRS16 style). Not active in this valuation (Input B14 = "No") but fully wired.

**Inputs:** E4 current-year operating lease expense — 295; B7..B11 commitments years 1–5 — 287, 235, 194, 151, 98; B12 "6 and beyond" lump sum — 605.

**Logic:**
- C15 pre-tax cost of debt `='Cost of capital worksheet'!B25` (circular with WACC sheet; needs iteration or a two-pass solve)
- D18 years embedded in yr-6 lump `=IF(B12>0, ROUND(B12/AVERAGE(B7:B11),0), 0)` → 3
- Rows 22–26 PV of each year-t commitment `=B_t/(1+C15)^t`
- B27 annuitized post-5 commitment `=IF(B12>0, IF(D18>0, B12/D18, B12), 0)` → 201.667
- C27 PV of the tail `=IF(D18>0, (B27*(1-(1+C15)^(-D18))/C15)/(1+C15)^5, B27/(1+C15)^6)` (annuity of B27 for D18 years, discounted back 5 years)
- **C28 debt value of leases** `=SUM(C22:C27)` → 1,373.17
- F31 depreciation on lease asset `=C28/(5+D18)` (straight line) → 171.65
- **F32 adjustment to operating earnings** `=E4-F31` → 123.35 (add to pre-tax EBIT)
- **F33 adjustment to total debt** `=C28`; F34 adjustment to depreciation `=C28/(5+D18)`

---

## Sheet: "Option value" (employee options, Black-Scholes with dilution)

**Inputs (auto-fed):** D2 stock price `='Input sheet'!B19`; D3 strike `=B37`; D4 expiration `=B38`; D5 σ `=B39`; D6 dividend yield — 0 (typed); D7 T-bond rate `=B32`; D8 # options `=B36`; D9 # shares `=B18`.

**Logic (warrant valuation with dilution — note the circularity: adjusted S depends on option value C26):**
- C15 adjusted S `=(S*N_sh + OptVal*N_opt)/(N_sh+N_opt)` i.e. `=(C13*F14+C26*F13)/(F14+F13)`
- C16 adjusted K `=C14`; F16 variance `=σ²`; F18 div-adjusted rate `=F15-F17` (NOTE: verbatim `=F15-F17` = riskfree − dividend yield)
- B20 d1 `=(LN(C15/C16)+(F18+F16/2)*T)/(σ·√T)` verbatim `=(LN(C15/C16)+(F18+(F16/2))*C17)/(((F16)^(0.5))*(C17^0.5))`
- B21 N(d1) `=NORMSDIST(B20)`; B23 d2 `=B20-σ·√T`; B24 N(d2)
- C26 value per option `=EXP(-q*T)*S_adj*N(d1) - K_adj*EXP(-rf*T)*N(d2)` verbatim `=((EXP((0-F17)*C17))*C15*B21-C16*(EXP((0-F15)*C17))*B24)`
- **D27 value of all options** `=C26*D8` → 2,111,410.34 (only subtracted from equity if Input B35="Yes"; here "No" → 0 used)
- Python port: solve the fixed point on C26 (iterate until option value converges), as Excel does with iterative calc.

---

## Sheet: "Country equity risk premiums"

- **B1 mature-market ERP = 0.0424** ("Mature Market ERP +", updated January 1, 2022). Every country ERP in column D `=$B$1+CRP`. Changing B1 shifts all ERPs.
- Columns: A Country, B Moody's rating (or a numeric composite score where unrated), C adjusted default spread, D equity risk premium (=B1+E), E country risk premium, F corporate tax rate.
- Rows 5–181: 177 countries (verbatim table below). Rows 184–194: GDP-weighted regional aggregates (Africa, Asia, Australia & NZ, Caribbean, Central and South America, Eastern Europe & Russia, Middle East, North America, Western Europe, Global) with columns: Weighted Average ERP (=B1+CRP), Default Spread, Tax rate, CRP.
- Used by: Valuation output M12 (B1), Cost of capital worksheet B15/I-column VLOOKUPs (col 4), Synthetic rating D12 (col 3).

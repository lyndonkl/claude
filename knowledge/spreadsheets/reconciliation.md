# Damodaran Valuation Model Reconciliation Spreadsheets

Source folder: `/Users/kushaldsouza/Downloads/2020/Spreadsheets/Valuation Model Reconciliation/`

All four workbooks are legacy `.xls` files: the dumps expose **computed values only, no live formulas**. Every formula below was reconstructed from labels, layout, and arithmetic verification of the values in the sheet, and is therefore **(inferred)** unless noted. Each inferred formula was numerically verified against the sheet's current values (agreement to floating-point precision unless flagged).

---

### fcfevsddm.xls

Sheet: `NewFCFE2Stage` (65 rows x 14 cols). Title (B1): "Comparing DDM and FCFE Models: Two Stage Valuation".

**Purpose:** Demonstrates why a two-stage Dividend Discount Model and a two-stage FCFE model give different values for the same firm when dividends < FCFE. The reconciliation is exact: the difference equals the present value lost (or gained) because the cash that builds up inside the firm is reinvested at a rate other than the cost of equity. If the cash buildup is assumed reinvested at the cost of equity, the two models produce identical values. Damodaran uses this as a teaching/reconciliation model, not a primary valuation tool.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Current Net Income | D3 | 100 (currency) |
| Current Dividends | D4 | 30 (currency) |
| Current Capital Expenditures | D5 | 75 (currency) |
| Current Depreciation | D6 | 50 (currency) |
| Current Revenue | D7 | 1000 |
| Current Working Capital | D8 | 50 (currency) |
| Net Debt Cashflow (current) | D9 | 10 |
| Length of extraordinary growth period (years) | E11 | 5 |
| Growth rate, high growth period | E12 | 0.10 |
| Beta of the stock | D15 | 1.0 |
| Riskfree rate | D16 | 0.05 |
| Risk premium | D17 | 0.04 |
| Growth rate in stable growth period | E19 | 0.04 |
| Return on equity in stable growth | E20 | 0.12 |
| Will beta change in stable period? (Yes/No) | E21 | "No" |
| If yes, beta for stable period | E22 | 1.0 |
| Reinvest cash buildup at cost of equity? (Yes/No) | H24 | "No" |
| If not, rate of return earned on cash | H25 | 0.07 |

**Logic:** (all inferred; every step verified against sheet values)

Let n = E11 (high-growth years, sheet layout supports up to 10; columns D..M are years 1..10, N is Terminal Year; with n=5 only D..H populated), g_h = E12, g_s = E19.

1. Cost of equity (D28): `ke = rf + beta * premium` = 0.05 + 1.0*0.04 = **0.09**. If E21 = "Yes", stable-period cost of equity uses E22 instead of D15: `ke_s = rf + beta_stable * premium`; else `ke_s = ke`.
2. Echo cells: D31 = D3 (Net Income), D32 = E12 (growth). Growth-rate table (rows 36–38): capital spending, depreciation, and revenues all grow at g_h in high growth (D36=D37=D38=0.10) and g_s in stable (E36=E37=E38=0.04). Working capital as % of revenues (E40) = D8/D7 = 0.05. Rate cash builds up gets invested at (E41) = ke if H24="Yes", else H25 (= 0.07 here).
3. High-growth years t = 1..n:
   - `NI_t = NI_0 * (1+g_h)^t` (row 44)
   - `(CapEx-Dep)_t = (CapEx_0 - Dep_0) * (1+g_h)^t` (row 45) — both grow at g_h so the net figure does too
   - `ΔWC_t = (WC%) * (Rev_t - Rev_{t-1})` where `Rev_t = Rev_0*(1+g_h)^t` (row 46)
   - `NetDebtCF_t = NetDebtCF_0 * (1+g_h)^t` (row 47)
   - `FCFE_t = NI_t - (CapEx-Dep)_t - ΔWC_t + NetDebtCF_t` (row 48)
   - `Div_t = Div_0 * (1+g_h)^t` (row 49)
   - `PV(FCFE_t) = FCFE_t / (1+ke)^t` (row 50); `PV(Div_t) = Div_t / (1+ke)^t` (row 51)
   - Cash buildup (row 52), recursive: `CB_1 = FCFE_1 - Div_1`; `CB_t = CB_{t-1}*(1+r_cash) + (FCFE_t - Div_t)` where r_cash = E41. Terminal-year cash buildup N52 = CB_n (carried, not grown further).
4. Terminal year (column N):
   - `NI_T = NI_n * (1+g_s)` (N44)
   - `ΔWC_T = WC% * Rev_n * g_s` (N46)
   - `NetDebtCF_T = NetDebtCF_n * (1+g_s)` (N47)
   - `FCFE_T = NI_T * (1 - g_s/ROE_s)` (N48) — terminal FCFE is forced to be consistent with the stable ROE: retention = g/ROE. Verified: 167.493 * (1 − 0.04/0.12) = 111.662.
   - `(CapEx-Dep)_T` (N45) is a **plug**: `NI_T - FCFE_T - ΔWC_T + NetDebtCF_T` = 69.359. It is NOT grown from year n; it is whatever makes the terminal reinvestment consistent with g_s/ROE_s.
5. Terminal price (E58 = F58): `P_n = FCFE_T / (ke_s - g_s)` = 111.662/(0.09−0.04) = 2233.24. The DDM uses the **same** terminal price (stable-phase dividends are assumed to equal FCFE — payout adjusts in steady state). E55/F55 echo g_s; E56/F56 echo FCFE_T; E57/F57 echo ke_s.
6. Final values (rows 62–65):
   - FCFE model: `PV(FCFE high growth)` F62 = Σ_t FCFE_t/(1+ke)^t = 413.481; `PV(terminal price)` F63 = P_n/(1+ke)^n = 1451.453; `Value (FCFE)` F65 = F62 + F63 = **1864.934**.
   - DDM: `PV(dividends)` G62 = Σ_t Div_t/(1+ke)^t = 154.179; PV(terminal price) G63 = 1451.453 (same); `PV of cash buildup in terminal year` G64 = CB_n/(1+ke)^n = 384.723/1.09^5 = 250.043; `Value (DDM)` G65 = G62 + G63 + G64 = **1855.676**.
   - H65 = F65 − G65 = **9.258** = value difference caused by cash being reinvested at 7% instead of ke = 9%. If H24 = "Yes" (cash reinvested at ke), H65 = 0 and the models reconcile exactly.

**Reference data:** none (no lookup tables in this workbook).

**Outputs:**
- D28: cost of equity (0.09)
- F65: value of the stock under the FCFE model (1864.934)
- G65: value of the stock under the DDM including the accumulated-cash asset (1855.676)
- H65: difference between the two (9.258)
- Row 52 / N52: cash balance built up by end of high growth (384.723)

**Worked example (values currently in sheet):** NI_0=100, Div_0=30, CapEx_0=75, Dep_0=50, Rev_0=1000, WC_0=50, NetDebt_0=10, g_h=10% for 5 yrs, g_s=4%, ROE_s=12%, ke=0.05+1.0×0.04=9%, cash reinvested at 7%.
Year 1: NI=110, CapEx−Dep=27.5, ΔWC=0.05×100=5, NetDebt=11 → FCFE=88.5; Div=33; CB_1=55.5. Year 5: NI=161.051, FCFE=129.573, Div=48.315, CB_5=384.723 (e.g. CB_2 = 55.5×1.07 + (97.35−36.3) = 120.435). Terminal: NI_T=167.493, FCFE_T=167.493×(2/3)=111.662, P_5=111.662/0.05=2233.241. FCFE value = 413.481+1451.453=1864.934. DDM value = 154.179+1451.453+250.043=1855.676. Difference 9.258.

**Reimplementation notes:**
- Inputs: floats as listed (currency amounts, decimal rates), int n (1–10), two Yes/No booleans (`beta_changes_in_stable`, `cash_reinvested_at_ke`), optional `stable_beta`, `cash_return_rate`.
- Outputs: `value_fcfe`, `value_ddm`, `difference`, plus per-year cashflow table and terminal-year components.
- Branches: (a) stable ke depends on `beta_changes_in_stable`; (b) cash reinvestment rate = ke vs user rate; (c) n may be < 10 — only compute n columns.
- Edge cases. When Div_t exceeds FCFE_t, the "cash buildup" goes negative — a cash drawdown; the recursion still works. ke_s must exceed g_s or the terminal price is undefined. ROE_s must be nonzero. When ROE_s falls below g_s, the terminal retention exceeds 1 and FCFE_T goes negative — validate. Terminal (CapEx−Dep) is a plug; do not grow it. WC% is derived from current WC / current revenue, not an independent input.

---

### fcffvsfcfe.xls

Sheet: `Sheet1` (44 rows x 9 cols). Sheet2/Sheet3 empty.

**Purpose:** Demonstrates that a firm (FCFF/WACC) valuation and an equity (FCFE/cost-of-equity) valuation are internally consistent: discounting FCFF at the cost of capital and subtracting debt yields exactly the same equity value as discounting FCFE at the cost of equity — **provided** the debt ratio is kept constant at market value each year (debt each year = debt ratio × that year's firm value, interest on beginning debt, new debt issued = change in debt). Two-stage model: 5 high-growth years then stable growth in perpetuity.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Earnings before interest and taxes (EBIT, year 0) | C2 | 100 |
| Expected growth for next 5 years | C3 | 0.10 |
| Expected growth after year 5 | C4 | 0.05 |
| Tax rate | C5 | 0.40 |
| Debt ratio for the firm (D/V, market value) | C6 | 0.20 |
| Cost of equity | C7 | 0.12 |
| Pre-tax cost of debt | C8 | 0.07 |
| Return on capital in high growth | C9 | 0.12 |
| Return on capital in stable growth | C10 | 0.10 |

NOTE: cell comments in the sheet (H21..I44) say "30% of each year's firm value" and "Computed using a 70% Equity; 30% Debt ratio" — these annotations are **stale/wrong**; the actual numbers use the input debt ratio C6 = 20% (verified: WACC 0.1044 = 0.8×0.12 + 0.2×0.042, and Debt/FirmValue = 123.401/617.006 = 0.20).

**Logic:** (inferred, verified) Years t=1..5 high growth at g_h=C3; column H is Terminal Year (year 6 onward, growing at g_s=C4 forever).

FCFF block (rows 12–23):
1. `ReinvestmentRate_high = g_h / ROC_high` = 0.10/0.12 = 0.8333; `ReinvestmentRate_stable = g_s / ROC_stable` = 0.05/0.10 = 0.5 (row 13).
2. `EBIT_t = EBIT_0 * (1+g_h)^t` for t≤5; `EBIT_T = EBIT_5 * (1+g_s)` (row 14). Taxes = EBIT×t (row 15). `EBIT(1-t)_t` (row 16). `Reinvestment_t = EBIT(1-t)_t × RR_t` (row 17). `FCFF_t = EBIT(1-t)_t × (1 − RR_t)` (row 18).
3. Costs (rows 40–43, constant all years): after-tax kd = 0.07×(1−0.4) = 0.042; `WACC = (1−DR)×ke + DR×kd_at` = 0.8×0.12 + 0.2×0.042 = **0.1044**.
4. `TerminalValue_5 = FCFF_T / (WACC − g_s)` = 50.731/0.0544 = 932.556 (G19).
5. `PV_t = FCFF_t/(1+WACC)^t` for t=1..4; year 5 PV = (FCFF_5 + TV_5)/(1+WACC)^5 (row 20). `Value of Firm` B21 = Σ PV = **617.006**. Row 21 C..G also shows firm value at the start of each future year, rolled forward: `V_t = V_{t-1}×(1+WACC) − FCFF_t` (C21 = 617.006×1.1044 − 11 = 670.422; G21 equals the terminal value 932.556).
6. `Value of Equity` B22 = V_0 × (1−DR) = 493.605; `Value of Debt` B23 = V_0 × DR = 123.401.

FCFE block (rows 25–35), built to be consistent with the firm valuation:
7. `Debt_t = DR × V_t` using the year-by-year firm values from row 21 (row 38: 123.401, 134.084, …, terminal H38 = 186.511×1.05 = 195.837 — terminal debt grows at g_s).
8. `InterestExp_t = pre-tax kd × Debt_{t-1}` (row 26; C26 = 0.07×123.401 = 8.638).
9. `EBT_t = EBIT_t − InterestExp_t`; `Taxes = EBT×t`; `NetIncome_t = EBT_t×(1−t)` (rows 27–29).
10. `NewDebtIssued_t = Debt_t − Debt_{t-1}` (row 31; terminal H31 = Debt_5 × g_s = 186.511×0.05 = 9.326).
11. `FCFE_t = NetIncome_t − Reinvestment_t + NewDebtIssued_t` (row 32) — same total reinvestment as the FCFF block.
12. `TerminalValueOfEquity_5 = TV_firm_5 − Debt_5 = 932.556 − 186.511 = 746.045` (G33). (Equivalently FCFE_T/(ke − g_s) = 52.223/0.07 = 746.045 — both hold exactly.)
13. `PV_t = FCFE_t/(1+ke)^t`; year 5 PV = (FCFE_5 + TVE_5)/(1+ke)^5 (row 34). `Value of Equity` B35 = Σ = **493.605** = B22 exactly. That equality is the point of the model.

**Reference data:** none.

**Outputs:**
- B21: Value of firm (FCFF @ WACC) = 617.006
- B22: Value of equity = firm − debt = 493.605
- B23: Value of debt = 123.401
- B35: Value of equity (FCFE @ ke) = 493.605 — identical to B22
- Rows 21/38: year-by-year firm value and debt schedule

**Worked example:** EBIT_0=100, g=10%/5yr then 5%, t=40%, DR=20%, ke=12%, kd=7%, ROC 12%/10%. Year 1: EBIT 110, EBIT(1−t) 66, reinvestment 55, FCFF 11. Terminal FCFF = 101.462×0.5 = 50.731; TV = 932.556; V_0 = 617.006; equity 493.605, debt 123.401. FCFE year 1: NI = (110 − 8.638)×0.6 = 60.817; FCFE = 60.817 − 55 + 10.683 = 16.500; PV stream at 12% sums to 493.605.

**Reimplementation notes:**
- Inputs: ebit0, g_high, g_stable, tax_rate, debt_ratio, cost_of_equity, pretax_cost_of_debt, roc_high, roc_stable (all floats); n fixed at 5 (generalize to parameter).
- Outputs: firm value, equity value (both routes), debt value, full year-by-year table (EBIT, FCFF, FCFE, debt, interest, new debt).
- Key structural requirements for reconciliation to hold: (1) reinvestment rate = g/ROC in each phase; (2) debt = DR × contemporaneous firm value (compute firm values first, then the debt schedule); (3) interest on beginning-of-year debt; (4) terminal debt/new-debt grow at g_stable.
- Edge cases: WACC must exceed g_stable; ke must exceed g_stable; ROC=0 → division by zero in reinvestment rate; if g > ROC, reinvestment rate > 1 and FCFF is negative (allowed arithmetically but flag). DR=0 collapses FCFE to FCFF net of nothing (both discounted streams still reconcile since WACC=ke).

---

### fcffeva.xls

Sheets: `FCFF Valuation` (66 rows x 12 cols) and `EVA Valuation` (22 rows x 14 cols); Sheet3–Sheet16 empty.

**Purpose:** Values the same firm two ways and proves they are equivalent. Route 1: a 10-year two-stage FCFF DCF (5 high-growth years, 5-year linear transition, stable perpetuity). Route 2: an EVA / economic-profit valuation, where Firm value = Capital invested + PV of expected EVA + a terminal-capital reconciling adjustment. Both give firm value 80,367.50. Damodaran uses it to show DCF and EVA are the same model when assumptions are consistent.

#### Sheet "FCFF Valuation"

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Current revenues | D3 | 12406 |
| Current capital invested (naive: BV debt + BV equity) | D4 | 20000 |
| Current depreciation | D5 | 233 |
| Current capital expenditures | D6 | 298 |
| Change in working capital last year | D7 | 115 |
| Value of current debt outstanding | D8 | 0 |
| Number of shares outstanding | D9 | 1500 |
| High growth: revenue growth next 5 years | E12 | 0.25 |
| Operating expenses as % of revenues in year 5 (= 1 − pre-tax operating margin; includes depreciation) | E13 | 0.70 |
| High growth: debt ratio for financing investments | E14 | 0.0 |
| High growth: growth in capex & depreciation | E15 | 0.25 |
| Working capital as % of revenues | E16 | 0.075 |
| Tax rate on corporate income | E17 | 0.36 |
| Beta (high growth) | E18 | 1.25 |
| Current long-term bond rate (riskfree) | E19 | 0.065 |
| Market risk premium | E20 | 0.055 |
| Cost of borrowing (high growth) | E21 | 0.085 |
| Stable: revenue growth | E23 | 0.06 |
| Stable: operating expenses as % of revenues | E24 | 0.75 |
| Stable: capex as a percent (multiple) of depreciation | E25 | 2.0 |
| Stable: debt ratio | E26 | 0.05 |
| Stable: interest rate on debt | E27 | 0.075 |
| Stable: beta | E28 | 1.1 |

**Logic:** (inferred, verified) Years 1–5 = high growth; years 6–10 = linear transition; terminal = stable perpetuity from year 11 on. Columns C..L = years 1..10; column B = Base year. (Year labels row 64: 1995–2004.)

1. Revenue growth (row 31): g_t = 0.25 for t=1..5; linear decline to 0.06 over t=6..10: step = (g_high − g_stable)/5 = 0.038 → 0.212, 0.174, 0.136, 0.098, 0.06. Depreciation growth (row 32) uses the identical schedule.
2. `Rev_t = Rev_{t-1} × (1+g_t)` (row 33).
3. Operating-expense ratio (row 35): 0.70 for base and t=1..5 (E13); linear to 0.75 by year 10: +0.01/yr → 0.71, 0.72, 0.73, 0.74, 0.75. `$OpEx_t = ratio_t × Rev_t` (row 36). `EBIT_t = Rev_t − OpEx_t` (row 37). Tax rate constant 0.36 (row 38). `EBIT(1−t)_t` (row 40).
4. `Dep_t = Dep_{t-1} × (1+g_t)` using the row-32 schedule (row 41): base 233 → year 10 = 1337.714.
5. CapEx (row 42): t=1..5: `CapEx_t = CapEx_{t-1} × 1.25` (E15) → year 5 = 909.424. Year-10 target: `CapEx_10 = E25 × Dep_10` = 2×1337.714 = 2675.428. Years 6–10: **linear dollar interpolation** from CapEx_5 to the target: increment = (2675.428 − 909.424)/5 = 353.201 per year (verified: year 6 = 1262.625).
6. `ΔWC_t = E16 × (Rev_t − Rev_{t-1})` = 0.075 × revenue change (row 43).
7. `FCFF_t = EBIT(1−t)_t + Dep_t − CapEx_t − ΔWC_t` (row 44).
8. Cost of equity (row 48). High growth (t=1..5): 0.065 + 1.25×0.055 = 0.13375. Stable (t=10): 0.065 + 1.1×0.055 = 0.1255. Over t=6..10 ke ramps linearly (step −0.00165/yr); equivalently beta steps from 1.25 to 1.1 by 0.03/yr.
9. Capital-structure ramp: Proportion of debt (row 51) = 0 for t=1..5 (E14), then +0.01/yr to 0.05 by year 10 (E26). Proportion of equity (row 49) = complement. After-tax cost of debt (row 50): high = 0.085×(1−0.36) = 0.0544; stable = 0.075×0.64 = 0.048; linear ramp between over t=6..10 (0.05312, 0.05184, 0.05056, 0.04928, 0.048).
10. `WACC_t = ke_t × E%_t + kd_at,t × D%_t` (row 52). `CumWACC_t = Π_{s=1..t}(1+WACC_s)` (row 53).
11. Terminal value (L45): `FCFF_11 = FCFF_10 × (1+g_stable)` = 9756.085×1.06 = 10341.45; `TV_10 = FCFF_11/(WACC_stable − g_stable)` = 10341.45/(0.121625 − 0.06) = **167812.58**.
12. `PV_t = FCFF_t / CumWACC_t` for t=1..9; `PV_10 = (FCFF_10 + TV_10)/CumWACC_10` (row 55).
13. `Value of Firm` C58 = Σ PV = **80367.50**. `Value of Equity` C60 = C58 − Debt(D8=0) = 80367.50. `Per share` C61 = C60/D9 = **53.578**.
14. Firm value by year (row 65): rolled forward `V_t = V_{t-1}×(1+WACC_t) − FCFF_t` (verified: 80367.50×1.13375 − 2663.578 = 88453.07). $ Value of debt by year (row 66) = D%_t × V_t (0 through year 5, then e.g. 0.01×123541.74 = 1235.42).

**Outputs (FCFF sheet):** C58 firm value 80367.50; C60 equity 80367.50; C61 value per share 53.578; L45 terminal value 167812.58; rows 65–66 forward firm/debt values.

#### Sheet "EVA Valuation"

No independent inputs — everything derives from the FCFF sheet. Columns C..L = years 1..10, M = Terminal Year.

**Logic:** (inferred, verified)
1. Capital invested schedule (rows 17–20): `CI_end,t = CI_begin,t + NetCapEx_t + ΔWC_t` where `NetCapEx_t = CapEx_t − Dep_t` (row 18; C18 = 372.5 − 291.25 = 81.25) and ΔWC from FCFF row 43. `CI_begin,1 = D4 = 20000`; `CI_begin,t = CI_end,t-1`. Row 14 repeats beginning capital per year. Ending capital year 10 = 29300.831.
2. `EBIT(1−t)` row 2 copied from FCFF sheet row 40; terminal M2 = EBIT(1−t)_10 × 1.06 = 12079.945.
3. Capital charge (row 3): `WACC_t × CI_begin,t` (C3 = 0.13375×20000 = 2675).
4. `EVA_t = EBIT(1−t)_t − WACC_t × CI_begin,t` (row 4).
5. ROC (row 13): `ROC_t = EBIT(1−t)_t / CI_begin,t` (C13 = 2977.44/20000 = 0.148872). Terminal ROC M13 = 0.41691 (implied — see step 6).
6. Terminal capital invested (M14, "(Adjusted to reflect terminal ROC)"). The FCFF sheet implies terminal reinvestment = `EBIT(1−t)_T − FCFF_T`, with FCFF_T = FCFF_10 × 1.06. That fixes the terminal reinvestment rate at g/ROC_T, so ROC_T = g_s / (reinvestment/EBIT(1−t)_T) = 0.41691 (M13). The adjusted terminal capital is `CI_T = EBIT(1−t)_T / ROC_T` = 12079.945/0.41691 = **28974.902**. Note CI_T ≠ CI_end,10 = 29300.831 — that gap drives step 10.
7. Terminal EVA (L5): `EVA_T = EBIT(1−t)_T − WACC_stable × CI_T` = 12079.945 − 0.121625×28974.902 = 8555.872 (M4); capitalized: `TerminalEVA = EVA_T / (WACC_stable − g_stable)` = 8555.872/0.061625 = **138837.68**.
8. `PV_t = EVA_t / CumWACC_t` (row 6; CumWACC row 22 identical to FCFF row 53); `PV_10 = (EVA_10 + TerminalEVA)/CumWACC_10` = 43229.10.
9. `PV of EVA` B7 = Σ = 60463.43.
10. `PV of Chg Capital in Yr 10` B9 = (CI_T_adjusted − CI_end,10)/CumWACC_10 = (28974.902 − 29300.831)/3.39747 = **−95.933**. Sheet note C9: "This reconciles the assumptions on stable growth, ROC and Capital Invested".
11. `Firm Value` B10 = PV of EVA + Capital Invested + PV of capital change = 60463.43 + 20000 − 95.93 = **80367.50** — identical to the FCFF sheet's C58.

**Reference data:** no lookup tables. The only "tables" are the deterministic transition ramps (revenue growth, opex ratio, beta/ke, debt ratio, after-tax kd), all linear interpolations between the high-growth and stable inputs over years 6–10, documented above.

**Worked example:** Revenues 12406 → 15507.5 (yr 1, +25%) → 71226.09 (yr 10). Year 1: EBIT = 15507.5×0.30 = 4652.25; EBIT(1−t) = 2977.44; +Dep 291.25 − CapEx 372.5 − ΔWC 232.61 → FCFF 2663.58; PV = 2663.58/1.13375 = 2349.35. WACC ramps 0.13375 → 0.121625. TV_10 = 9756.09×1.06/0.061625 = 167812.58. Firm value 80367.50; per share 80367.50/1500 = 53.58. EVA route: EVA_1 = 2977.44 − 2675 = 302.44; PV of EVA 60463.43; +20000 capital −95.93 adjustment = 80367.50.

**Reimplementation notes:**
- Inputs: the 20 floats listed above plus implicit structure (5 high-growth years, 5 transition years — generalize as n_high, n_transition).
- Outputs: firm value, equity value, per-share value, terminal value, full 10-year cashflow/WACC table, EVA decomposition (PV of EVA, capital invested, terminal-capital adjustment).
- Branches/rules a port must reproduce exactly:
  - (a) Transition ramps are linear per-year steps: revenue growth, dep growth, opex ratio (+0.01/yr here; generally (stable−high)/n_transition), beta (hence ke), debt proportion, after-tax kd.
  - (b) CapEx transition is linear in **dollars** to the year-10 target (stable capex/dep multiple × Dep_10). It is not a growth rate.
  - (c) Discounting uses cumulative products of time-varying WACC, not a constant rate.
  - (d) Terminal FCFF = FCFF_10 × (1+g_s). Grow the whole FCFF; do not rebuild it from components.
  - (e) EVA uses beginning-of-year capital.
  - (f) Terminal capital must be adjusted to EBIT(1−t)_T/ROC_T, with the PV of the difference added. Otherwise EVA will not reconcile with DCF.
- Edge cases: WACC_stable must exceed g_stable. Zero shares → per-share division by zero. Debt input D8 subtracts from firm value only at the valuation date. Negative EBIT years flow through, with tax still applied at the flat rate (no NOL handling). If the stable capex multiple < 1, net capex turns negative in transition (allowed).

---

### GrossvsNet.xls

Sheets: `Cash and Eq Multiples` (4x6) and `DCf Valuation` (28x5); Sheet3 empty.

**Purpose:** Shows (1) how holding cash distorts blended equity multiples (PE, P/BV) relative to the operating business, and (2) that the Gross Debt and Net Debt approaches to DCF valuation make different assumptions about how cash is funded, require different adjusted costs of debt, and yield identical equity values only at a 0% tax rate — with the net debt approach yielding a lower equity value as the tax rate rises.

#### Sheet "Cash and Eq Multiples"

A static illustration table (values, no visible dependencies beyond simple ratios). Verbatim:

| Component | Capital Invested | After-tax Earnings | Value | PE | P/BV |
|---|---|---|---|---|---|
| Operating Assets | 1000 | 125 | 1250 | 10 | 1.25 |
| Cash | 250 | 10 | 250 | 25 | 1.0 |
| Firm | 1250 | 135 | 1500 | 11.1111 | 1.2 |

Logic (inferred): Firm row = column sums; `PE = Value / After-tax Earnings`; `P/BV = Value / Capital Invested`. Cash value = cash earnings capitalized at the riskfree rate (10/0.04 = 250, consistent with the DCF sheet's 4% riskfree rate) — cash trades at PE = 1/rf = 25 and P/BV = 1. Point: mixing cash (PE 25) with operations (PE 10) pushes the blended firm PE to 11.11, so gross multiples of cash-rich firms are inflated.

#### Sheet "DCf Valuation"

**Inputs:**

| Label | Cell(s) | Example value |
|---|---|---|
| Total debt (gross) | B2 | 500 |
| Cash | B4 (and B15) | 250 |
| Unlevered beta of operating assets | B6/C6 | 1.42 |
| Operating Earnings (after-tax, perpetual) | B21/C21 | 125 |
| Cash Earnings | B22/C22 | 10 |
| Tax Rate | B24/C24 | 0.40 |
| Riskfree rate | B26/C26 | 0.04 |
| Risk premium | B27/C27 | 0.05 |
| Cost of debt for the firm (stated, blended) | B28/C28 | 0.059 |

Column B = Gross Debt Approach; column C = Net Debt Approach (net debt C2 = 500 − 250 = 250; cash C4 blank/netted out).

**Logic:** (inferred, verified; the model is **circular** — equity value depends on levered beta which depends on equity value — and must be solved iteratively, as Excel does with iterative calculation.)

Common: firm interest expense = stated kd × gross debt = 0.059 × 500 = 29.5.

Gross Debt Approach (column B):
1. Cash is assumed funded with the same debt/equity mix as the operating assets. Debt allocated to cash = Cash × (D/V) = 250 × (500/1491.246) = 83.82, assumed riskfree; adjusted cost of debt on the rest: `kd_gross = (Interest − rf × Cash × D/V) / (D − Cash × D/V)` = (29.5 − 0.04×83.82)/416.18 = **0.0628268** (B10). Sheet note D10: "Cost of debt used has to be adjusted to reflect assumptions about cash holdings."
2. `LeveredBeta = UnleveredBeta × (1 + (1−t) × D/E)` = 1.42 × (1 + 0.6 × 500/991.246) = **1.849762** (B8).
3. `ke = rf + LeveredBeta × premium` = 0.04 + 1.849762×0.05 = **0.1324881** (B9).
4. `WACC = ke × E/V + kd_gross × (1−t) × D/V`, V = E + D = 1491.246 → 0.1324881×0.664713 + 0.0628268×0.6×0.335287 = **0.1007053** (B12).
5. `OperatingAssets = OperatingEarnings / WACC` (flat perpetuity, earnings already after-tax) = 125/0.1007053 = **1241.246** (B14).
6. `FirmValue = OperatingAssets + Cash` = 1491.246 (B16); `Equity = FirmValue − Debt` = 1491.246 − 500 = **991.246** (B18 = B3). (Fixed point of the circular system.)

Net Debt Approach (column C):
1. Cash (250) is assumed entirely funded with riskfree debt at rf; the remaining debt (250) carried by operating assets absorbs all remaining interest: `kd_net = (Interest − rf × Cash)/(D − Cash)` = (29.5 − 0.04×250)/250 = 19.5/250 = **0.078** (C10).
2. `LeveredBeta = 1.42 × (1 + 0.6 × NetDebt/Equity)` = 1.42×(1 + 0.6×250/924.775) = **1.650326** (C8).
3. `ke = 0.04 + 1.650326×0.05 = 0.1225163` (C9).
4. `WACC = ke × E/(E+ND) + kd_net × (1−t) × ND/(E+ND)`, E+ND = 1174.775 → 0.1225163×0.787193 + 0.078×0.6×0.212807 = **0.1064034** (C12).
5. `OperatingAssets = 125/0.1064034 = 1174.775` (C14); Cash = 0 (netted); FirmValue = 1174.775 (C16); `Equity = 1174.775 − 250 = 924.775` (C18 = C3).

Result: gross-debt equity 991.25 vs net-debt equity 924.77. Sheet commentary (E15:E27, verbatim substance): the two approaches differ in how cash is assumed funded; the stated firm-wide cost of debt can never be used directly in either WACC; at a 0% tax rate (with the cost-of-debt adjustments this sheet makes) the two approaches give the same equity value; as the tax rate rises they diverge, the net debt approach yielding a **lower** value because it assumes the tax benefit of debt funding cash is fully offset by tax on the cash's interest income.

**Reference data:** only the multiples table above (reproduced verbatim).

**Outputs:**
- B18 / C18 (= B3 / C3): equity value under gross (991.246) vs net (924.775) debt approaches
- B8/C8 levered betas; B9/C9 costs of equity; B10/C10 adjusted costs of debt; B12/C12 costs of capital; B14/C14 operating-asset values; B16/C16 firm values
- Sheet 1: blended PE 11.11 and P/BV 1.20 vs operating PE 10 / P/BV 1.25

**Worked example:** traced fully in the Logic section (all numbers above are the sheet's current values).

**Reimplementation notes:**
- Inputs: gross_debt, cash, unlevered_beta, operating_earnings_after_tax, cash_earnings, tax_rate, riskfree, risk_premium, stated_cost_of_debt (floats); approach flag (gross|net).
- Outputs: equity value, plus intermediates (levered beta, ke, adjusted kd, WACC, operating-asset value, firm value) per approach.
- Must solve a fixed point: iterate E → beta → ke → (kd adjustment for gross, which also depends on V) → WACC → OA value → E until convergence (simple fixed-point iteration converges quickly from E₀ = book/naive guess; ~1e-9 in <50 iterations). The net approach's kd adjustment is closed-form; the gross approach's kd depends on D/V and is inside the loop.
- Edge cases: cash ≥ gross debt makes net debt ≤ 0 (levered beta ≤ unlevered; kd_net formula divides by D − cash → guard zero/negative); interest allocated to cash exceeding total interest makes adjusted kd negative (guard); WACC must be > 0 for the perpetuity; earnings are perpetual with **zero growth** — do not add a growth term; operating earnings are after-tax (tax rate enters only beta levering and after-tax kd).

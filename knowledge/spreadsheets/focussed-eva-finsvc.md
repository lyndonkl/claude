# Damodaran model spreadsheets: evavaln.xls (FCFF vs EVA) and eqexret.xls (equity excess returns)

Both workbooks are legacy .xls — only computed values were visible. All formulas below were reconstructed from labels, layout, and by numerically verifying every relationship against the values in the sheets; any relationship that could not be read directly is flagged "(inferred)". Every "(inferred)" formula reproduced the sheet's stored values to full precision.

---

### evavaln.xls (Focussed Valuation Model Spreadsheet)

**Purpose:** Demonstrates that a Free-Cash-Flow-to-Firm (DCF) valuation and an Economic Value Added (EVA / excess-return-on-capital) valuation of the same firm yield **exactly the same firm value** when the assumptions are consistent. Two-stage model: 5 explicit high-growth years, a 5-year linear transition (years 6–10), and stable growth thereafter. Damodaran uses this as a teaching/reconciliation model: value = capital invested + PV of expected EVA, and that must equal PV of FCFF.

Sheets with content: `FCFF Valuation` (66r x 12c), `EVA Valuation` (22r x 14c). Sheets `Sheet3`–`Sheet16` are empty stubs (skipped). Layout: column B = "Base" (year 0), columns C..L = forecast years 1..10, column M (EVA sheet only) = terminal year (year 11).

#### Inputs (all on sheet `FCFF Valuation`)

Current inputs:

| Label | Cell | Example value |
|---|---|---|
| Current revenues of the firm | D3 | 12406 |
| Current capital invested in the firm (naive: BV debt + BV equity, per note in E4) | D4 | 20000 |
| Current depreciation | D5 | 233 |
| Current capital expenditures | D6 | 298 |
| Change in working capital in last year | D7 | 115 |
| Value of current debt outstanding | D8 | 0 |
| Number of shares outstanding | D9 | 1500 |

High growth period (years 1–5):

| Label | Cell | Example value |
|---|---|---|
| Growth rate in revenues for the next 5 years | E12 | 0.25 |
| Operating expenses as % of revenues in the fifth year (= 1 − pre-tax operating margin; includes depreciation, per note in F13) | E13 | 0.70 |
| Debt used in financing investments (proportion) | E14 | 0.0 |
| Growth rate in capital expenditures & depreciation | E15 | 0.25 |
| Working capital as a percent of revenues | E16 | 0.075 |
| Tax rate on corporate income | E17 | 0.36 |
| Beta for cost of equity (high growth) | E18 | 1.25 |
| Current long-term bond rate (riskfree) | E19 | 0.065 |
| Market risk premium | E20 | 0.055 |
| Cost of borrowing money (pre-tax, high growth) | E21 | 0.085 |

Stable period (year 10 onward):

| Label | Cell | Example value |
|---|---|---|
| Growth rate in revenues (stable) | E23 | 0.06 |
| Operating expenses as % of revenues in stable period | E24 | 0.75 |
| Capital expenditures as a percent (multiple) of depreciation in stable period | E25 | 2.0 |
| Debt used in financing investments (stable proportion) | E26 | 0.05 |
| Interest rate of debt in stable period (pre-tax) | E27 | 0.075 |
| Beta in stable period | E28 | 1.1 |

#### Logic — sheet `FCFF Valuation` (all formulas inferred and numerically verified)

Notation: `g_hi = E12`, `g_st = E23`, `t` = year index 1..10. Transition = years 6..10, linear interpolation over 5 steps.

1. **Revenue growth path** (row 31; depreciation growth row 32 is identical):
   - Years 1–5: `g_t = g_hi` (0.25)
   - Years 6–10: `g_t = g_hi − (g_hi − g_st) · (t−5)/5` → 0.212, 0.174, 0.136, 0.098, 0.06
2. **Revenues** (row 33): `Rev_0 = D3`; `Rev_t = Rev_{t−1} · (1 + g_t)`
3. **Operating expense ratio** (row 35): base and years 1–5 = `E13` (0.70); years 6–10 linear to `E24`: `oe_t = E13 + (E24 − E13)·(t−5)/5` → 0.71, 0.72, 0.73, 0.74, 0.75
4. **$ Operating expenses** (row 36): `OpEx_t = Rev_t · oe_t`
5. **EBIT** (row 37): `EBIT_t = Rev_t − OpEx_t = Rev_t · (1 − oe_t)`
6. **Tax rate** (row 38): constant `E17` in all years
7. **EBIT(1−t)** (row 40): `EBIT_t · (1 − E17)`
8. **Depreciation** (row 41): `Dep_0 = D5`; `Dep_t = Dep_{t−1} · (1 + gdep_t)` where `gdep_t` = row 32 (same path as revenue growth: E15 for years 1–5, then linear decline to g_st). Note E15 is a separate input from E12 (both 0.25 in example).
9. **Capital expenditures** (row 42):
   - Years 1–5: `Capex_t = Capex_{t−1} · (1 + E15)` starting from `Capex_0 = D6`
   - Year 10 target: `Capex_10 = E25 · Dep_10` (stable capex = multiple of depreciation)
   - Years 6–9: linear interpolation: `Capex_t = Capex_5 + (Capex_10 − Capex_5)·(t−5)/5`
10. **Change in working capital** (row 43): `ΔWC_0 = D7` (input); `ΔWC_t = E16 · (Rev_t − Rev_{t−1})` for t ≥ 1
11. **FCFF** (row 44): `FCFF_t = EBIT(1−t)_t + Dep_t − Capex_t − ΔWC_t`
12. **Terminal value** (L45): `TV = FCFF_10 · (1 + g_st) / (WACC_st − g_st)` where `WACC_st` = year-10 cost of capital. (Verified: 9756.085·1.06/0.061625 = 167812.58.)
13. **Cost of equity** (row 48): years 1–5 `ke = E19 + E18·E20`; years 6–10 beta declines linearly from E18 to E28, so `ke_t = E19 + β_t·E20` with `β_t = E18 − (E18 − E28)·(t−5)/5` → 0.13375 flat, then 0.1321, 0.13045, 0.1288, 0.12715, 0.1255
14. **Proportion of debt** (row 51): years 1–5 = `E14`; years 6–10 linear to `E26` → 0, then 0.01..0.05. Proportion of equity (row 49) = 1 − that.
15. **After-tax cost of debt** (row 50): years 1–5 `kd = E21·(1 − E17)` = 0.0544; year 10 `= E27·(1 − E17)` = 0.048; years 6–9 linear interpolation between the two.
16. **Cost of capital** (row 52): `WACC_t = ke_t · we_t + kd_t · wd_t`
17. **Cumulative WACC** (row 53): `Cum_t = ∏_{s=1..t} (1 + WACC_s)`
18. **Present value** (row 55): `PV_t = FCFF_t / Cum_t` for t = 1..9; `PV_10 = (FCFF_10 + TV) / Cum_10`
19. **Firm valuation** (C58–C61):
    - `Value of Firm (C58) = Σ_{t=1..10} PV_t`
    - `− Value of Debt (C59) = D8`
    - `Value of Equity (C60) = C58 − C59`
    - `Value per Share (C61) = C60 / D9`
20. **Value of firm by year** (rows 64–66, an auxiliary rollforward labeled with calendar years 1995–2004): `V_0 = C58`; `V_t = V_{t−1}·(1 + WACC_t) − FCFF_t`. `$ Value of Debt by year (row 66) = wd_t · V_t`.

#### Logic — sheet `EVA Valuation` (all formulas inferred and numerically verified)

Columns C..L = years 1..10, M = terminal year. Pulls EBIT(1−t), WACC, cumulated WACC, net capex and ΔWC from the FCFF sheet.

1. **Capital invested rollforward** (rows 17–20):
   - `Capital_begin_1 = D4` (20000)
   - `NetCapex_t = Capex_t − Dep_t` (row 18)
   - `ΔWC_t` (row 19) = FCFF sheet row 43
   - `Capital_end_t = Capital_begin_t + NetCapex_t + ΔWC_t`; `Capital_begin_{t+1} = Capital_end_t`
   - Row 14 "Capital Invested" repeats beginning-of-year capital for years 1..10.
2. **EBIT(1−t)** (row 2): same as FCFF sheet row 40; terminal year `M2 = EBIT(1−t)_10 · (1 + g_st)` = 12079.94
3. **Capital charge** (row 3, "− WACC (CI)"): `Charge_t = WACC_t · Capital_begin_t`
4. **EVA** (row 4): `EVA_t = EBIT(1−t)_t − WACC_t · Capital_begin_t`
5. **ROC** (row 13): `ROC_t = EBIT(1−t)_t / Capital_begin_t`
6. **Terminal-year adjustment** (M13/M14, note N14 "(Adjusted to reflect terminal ROC)"):
   - Terminal reinvestment rate implied by the FCFF sheet: `RR_term = (EBIT(1−t)_term − FCFF_term)/EBIT(1−t)_term` where `FCFF_term = FCFF_10·(1+g_st)` (inferred; RR_term = 0.14392)
   - Terminal ROC `M13 = g_st / RR_term` = 0.41691 (sustainable-growth identity g = ROC × reinvestment rate)
   - Adjusted terminal capital `M14 = EBIT(1−t)_term / ROC_term` = 28974.90 (vs. unadjusted ending capital of year 10, L20 = 29300.83)
7. **Terminal EVA** (M4): `EVA_term = EBIT(1−t)_term − WACC_st · Capital_term(adj)` = 12079.94 − 0.121625·28974.90 = 8555.87
8. **Terminal value of EVA** (L5): `TV_EVA = EVA_term / (WACC_st − g_st)` = 8555.87/0.061625 = 138837.68
9. **PV of EVA** (row 6): `PV_t = EVA_t / CumWACC_t` for t = 1..9; `PV_10 = (EVA_10 + TV_EVA)/CumWACC_10`. `CumWACC` (row 22) identical to FCFF sheet row 53.
10. **Firm value bridge** (B7–B10):
    - `PV of EVA (B7) = Σ PV_t` = 60463.43
    - `+ Capital Invested (B8) = D4` = 20000
    - `+ PV of Chg Capital in Yr 10 (B9) = (Capital_term(adj) − Capital_end_10) / CumWACC_10` = (28974.90 − 29300.83)/3.39747 = −95.93 (inferred; note C9: "This reconciles the assumptions on stable growth, ROC and Capital Invested")
    - `= Firm Value (B10) = B7 + B8 + B9` = 80367.50 — **identical to FCFF sheet C58**, which is the whole point of the workbook.

#### Reference data

No lookup/rating tables in this workbook. The only "tables" are the deterministic linear transition schedules (years 6–10) documented in the logic above. Transition values currently in the sheet:

| Year | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|
| Revenue & deprec. growth | 0.212 | 0.174 | 0.136 | 0.098 | 0.060 |
| Opex % of revenue | 0.71 | 0.72 | 0.73 | 0.74 | 0.75 |
| Cost of equity | 0.1321 | 0.13045 | 0.1288 | 0.12715 | 0.1255 |
| Debt proportion | 0.01 | 0.02 | 0.03 | 0.04 | 0.05 |
| After-tax cost of debt | 0.05312 | 0.05184 | 0.05056 | 0.04928 | 0.048 |
| Cost of capital (WACC) | 0.1313102 | 0.1288778 | 0.1264528 | 0.1240352 | 0.121625 |

#### Outputs

| Cell | Meaning | Value in sheet |
|---|---|---|
| FCFF!C58 | Value of firm (DCF) | 80,367.4966 |
| FCFF!C59 | Value of debt | 0 |
| FCFF!C60 | Value of equity | 80,367.4966 |
| FCFF!C61 | Value of equity per share | 53.5783 |
| EVA!B7 | PV of EVA | 60,463.4295 |
| EVA!B9 | PV of terminal capital adjustment | −95.9329 |
| EVA!B10 | Firm value (EVA route) | 80,367.4966 (= FCFF!C58) |

#### Worked example (values currently in sheet)

Base: Rev 12406, opex 70% → EBIT 3721.8 → EBIT(1−t) 2381.95; Dep 233, Capex 298, ΔWC 115 → FCFF₀ 2201.95.
Year 1: Rev 15507.5 (×1.25); EBIT(1−t) 2977.44; Dep 291.25; Capex 372.5; ΔWC 0.075·(15507.5−12406)=232.61 → FCFF₁ 2663.58; WACC 0.13375 → PV 2349.35.
Year 5: Rev 37860.11, FCFF₅ 6502.87, PV 3471.51. Year 6 capex jumps to 909.42 + (2675.43−909.42)/5 = 1262.62 (interpolating toward 2× terminal depreciation 1337.71 → 2675.43).
Year 10: FCFF₁₀ 9756.09; TV = 9756.09·1.06/(0.121625−0.06) = 167,812.58; PV₁₀ = (9756.09+167812.58)/3.39747 = 52,264.96.
Sum of PVs = 80,367.50; debt 0; ÷1500 shares = **$53.58/share**.
EVA route: EVA₁ = 2977.44 − 0.13375·20000 = 302.44 … EVA₁₀ = 8031.94. Terminal ROC = 0.06/0.14392 = 0.41691. Adjusted terminal capital = 28,974.90. Terminal EVA = 8555.87. TV_EVA = 138,837.68. PV of EVA 60,463.43 + capital 20,000 − 95.93 = **80,367.50**. Matches.

#### Reimplementation notes (Python)

Inputs (name, type, units):

- Base year ($, float): revenues_0, capital_invested_0, depreciation_0, capex_0, chg_wc_0 (display only, not used downstream), debt_value; shares (count, float).
- High growth (fractions, float): g_high, opex_pct_high, debt_ratio_high, g_capex_deprec_high, wc_pct_rev, tax_rate, beta_high, riskfree, risk_premium, cost_of_debt_high (pre-tax).
- Stable (fractions, float): g_stable, opex_pct_stable, capex_to_deprec_stable (a multiple, not a fraction), debt_ratio_stable, cost_of_debt_stable (pre-tax), beta_stable.

Structure: the sheet hard-codes 5 high-growth years + 5 transition years. A port should parameterize n_high and n_transition with default 5/5. All transitions are linear interpolations over the transition window. Growth rates, opex ratio, beta (via cost of equity), and debt ratio interpolate between high and stable values. After-tax cost of debt interpolates between the two after-tax rates. Capex is different: it interpolates in **dollar levels** between capex_5 and capex_10 = multiple × dep_10, not in growth rates.

Outputs: per-year arrays (revenues, ebit_after_tax, depreciation, capex, chg_wc, fcff, wacc, cum_wacc, pv), terminal_value, firm_value, equity_value, value_per_share; EVA side: capital schedule, eva array, terminal_roc, adjusted_terminal_capital, pv_eva, firm_value_eva (assert ≈ firm_value).

Edge cases / branches:
- `WACC_stable ≤ g_stable` → terminal value division blows up; validate and raise.
- Terminal ROC computation divides by reinvestment rate `(EBIT(1−t)_term − FCFF_term)/EBIT(1−t)_term`; if terminal FCFF ≥ terminal EBIT(1−t) (zero/negative reinvestment) this divides by ≤ 0 — guard it.
- opex ≥ 1 gives negative EBIT; model carries it through mechanically (no floor).
- ΔWC base-year input is not used in forecasts (forecast ΔWC comes purely from wc_pct_rev × revenue change).
- Depreciation growth uses its own input (E15) in years 1–5 but reuses the *revenue* transition path in years 6–10 (row 32 = row 31 there).
- The equality FCFF-value = EVA-value only holds because of the year-10 capital adjustment term (B9); include it.

---

### eqexret.xls (Financial Service Firms — Equity Excess Return Model)

**Purpose:** Values the **equity** of a financial-services firm (bank/insurer) directly, as `Value of equity = Current book equity invested + PV of expected excess equity returns`, where excess equity return = Net income − (Cost of equity × Beginning book equity). Damodaran uses this for financial service firms because their debt is raw material rather than capital and FCFF/capex are ill-defined — so he works with equity earnings, book equity, and cost of equity. Two-stage (10-year high growth with optional gradual second-half fade to stable levels, then perpetual stable growth). The example firm's numbers match his classic State Bank of India / large-bank illustration style.

Sheets: `Read me first` (documentation text), `Inputs`, `Normalized Earnings`, `Excess Return Valuation`.

Note: the `Read me first` sheet contains boilerplate describing a **dividend discount model**. It covers high-growth dividends plus a terminal price, fundamental growth = retention × ROE, an option to make it 3-stage by fading inputs in the second half of the high-growth period, and a stable-only mode via high-growth length = 0. The mechanics described (fundamental growth, second-half fade, stable-growth-only option) apply to this workbook's excess-return engine as well. The text was carried over from the DDM template.

#### Inputs (sheet `Inputs`)

Current financials:

| Label | Cell | Example value |
|---|---|---|
| Net income (last year, currency) | B2 | 4791 |
| Book value of equity — current | B3 | 17997 |
| Book value of equity — prior year (unlabeled companion cell) | C3 | 15518 |
| Current earnings per share | B4 | 4.75 |
| Current dividends per share | B5 | 0.92 |
| Number of shares outstanding | B6 | 1120.713 |
| Normalize the net income/EPS? (Yes/No) | B7 | "No" |

Discount rate:

| Label | Cell | Example value |
|---|---|---|
| Beta of the stock | B10 | 1.15 |
| Riskfree rate | B11 | 0.05 |
| Risk premium | B12 | 0.04 |

High growth period:

| Label | Cell | Example value |
|---|---|---|
| Length of high growth period (years) | B15 | 10 |
| ROE (computed from fundamentals; see logic) | B18 | 0.308738 |
| Retention (computed; see logic) | B19 | 0.806316 |
| Change these inputs for high growth? (Yes/No) | B20 | "Yes" |
| If yes: ROE override | B22 | 0.25 |
| If yes: Retention override | B23 | 0.806316 |
| Change inputs for stable period? (Yes/No) | B24 | "Yes" |
| If yes: stable ROE | B26 | 0.15 |
| Gradually adjust inputs during second half? (Yes/No) | B28 | "Yes" |

Stable growth period:

| Label | Cell | Example value |
|---|---|---|
| Growth rate in stable period | B31 | 0.05 |
| Stable payout from fundamentals (computed; see logic) | B33 | 0.666667 |
| Change this payout ratio? (Yes/No) | B34 | "No" |
| If yes: stable payout override | B35 | (blank) |
| Will beta change in stable period? (Yes/No) | B37 | "Yes" |
| If yes: stable-period beta | B38 | 1.1 |
| Risk premium in stable period | B39 | 0.04 |

Sheet `Normalized Earnings` (used only if Inputs!B7 = "Yes"):

| Label | Cell | Example value |
|---|---|---|
| Approach chosen (1 or 2) | B2 | 1 |
| Net income, years −5..current (Approach 1) | B5:F5 | 1662, 2533, 1876, 1933, 2122 |
| Average net income (Approach 1 result) | G5 | 2025.2 (= AVERAGE(B5:F5), inferred) |
| Normalized ROE (Approach 2) | B8 | 0.22 |

#### Logic (all formulas inferred and numerically verified)

Derived inputs (on `Inputs`):
- Fundamental ROE `B18 = NetIncome / BV_equity_prior = 4791/15518 = 0.308738`
- Fundamental retention `B19 = 1 − DPS/EPS = 1 − 0.92/4.75 = 0.806316`
- Stable payout from fundamentals `B33 = 1 − g_stable/ROE_stable = 1 − 0.05/0.15 = 0.666667`
- Effective high-growth ROE/retention = overrides (B22/B23) if B20="Yes" else fundamentals (B18/B19). Effective stable ROE = B26 if B24="Yes". Effective stable payout = B35 if B34="Yes" else B33.
- Normalization (if B7="Yes"): Approach 1 → NI = average of last 5 years' NI; Approach 2 → NI = normalized ROE × BV of equity (inferred; not active in this sheet since B7="No").

Sheet `Excess Return Valuation` (columns B..K = years 1..10, L = terminal year):

Header block: `ROE (B2) = 0.25`, `Retention (B3) = 0.806316`, `Expected growth (B4) = B2·B3 = 0.201579`, `Cost of equity (B5) = riskfree + beta·premium = 0.05 + 1.15·0.04 = 0.096`.

With B28 = "Yes", the second half of the 10-year period (years 6–10) fades linearly to stable values over 5 steps; years 1–5 hold high-growth values:

1. **ROE path** (row 19): years 1–5 = 0.25; years 6–10: `ROE_t = ROE_hi − (ROE_hi − ROE_st)·(t−5)/5` → 0.23, 0.21, 0.19, 0.17, 0.15; terminal = 0.15
2. **Payout path** (row 21): years 1–5 = `1 − retention` = 0.193684; years 6–10 linear to stable payout 0.666667 (increment 0.094596/yr); terminal = 0.666667
3. **Cost of equity path** (row 16): years 1–5 = 0.096; years 6–10 linear to stable `ke_st = riskfree + beta_st·premium_st = 0.05 + 1.1·0.04 = 0.094` (decrement 0.0004/yr); terminal = 0.094
4. **Book equity rollforward** (rows 15, 22, 23): `BV_begin_1 = current BV = 17997`; `NI_t = ROE_t · BV_begin_t` (rows 8 and 20, identical); `Div_t = NI_t · payout_t`; `Retained_t = NI_t − Div_t`; `BV_begin_{t+1} = BV_begin_t + Retained_t`
5. **Equity cost** (rows 9/17): `EqCost_t = ke_t · BV_begin_t`
6. **Excess equity return** (row 10): `XR_t = NI_t − EqCost_t`
7. **Terminal year** (col L): `BV_term = BV_begin_10 + Retained_10 = 73370.15`; `NI_term = ROE_st · BV_term = 11005.52`; `EqCost_term = ke_st · BV_term = 6896.79`; `XR_term = 4108.73`
8. **Terminal value of excess returns** (K11): `TV = XR_term / (ke_st − g_st) = 4108.73/(0.094 − 0.05) = 93380.20`
9. **Cumulated cost of equity** (row 12): `Cum_t = ∏_{s=1..t}(1 + ke_s)`
10. **PV** (row 13): `PV_t = XR_t / Cum_t` for t = 1..9; `PV_10 = (XR_10 + TV)/Cum_10`
11. **Valuation** (B25–B29): `Equity invested (B25) = current BV = 17997`; `PV of equity excess returns (B26) = Σ PV_t = 65993.76`; `Value of equity (B27) = B25 + B26 = 83990.76`; `Value per share (B29) = B27 / shares (B28 = 1120.713) = 74.944`

#### Reference data

No rating/spread lookup tables. The fade schedules currently in the sheet (years 6–10, driven by the linear interpolation above):

| Year | 6 | 7 | 8 | 9 | 10 | Terminal |
|---|---|---|---|---|---|---|
| ROE | 0.23 | 0.21 | 0.19 | 0.17 | 0.15 | 0.15 |
| Dividend payout | 0.288281 | 0.382877 | 0.477474 | 0.572070 | 0.666667 | 0.666667 |
| Cost of equity | 0.0956 | 0.0952 | 0.0948 | 0.0944 | 0.0940 | 0.0940 |

Normalized-earnings history table (Normalized Earnings!B5:G5): NI year −5 = 1662, −4 = 2533, −3 = 1876, −2 = 1933, current = 2122, average = 2025.2.

#### Outputs

| Cell | Meaning | Value in sheet |
|---|---|---|
| Excess Return Valuation!B25 | Equity invested currently (book value) | 17,997 |
| Excess Return Valuation!B26 | PV of equity excess returns | 65,993.76 |
| Excess Return Valuation!B27 | Value of equity | 83,990.76 |
| Excess Return Valuation!B29 | Value per share | 74.94 |

#### Worked example (values currently in sheet)

ke = 0.05 + 1.15·0.04 = 0.096. Year 1: NI = 0.25·17997 = 4499.25; equity cost = 0.096·17997 = 1727.71; XR₁ = 2771.54; PV = 2771.54/1.096 = 2528.78. Payout 0.193684 → dividends 871.43, retained 3627.82 → BV₂ = 21624.82. Year 6 fades begin: ROE 0.23 → NI 10367.87, ke 0.0956, payout 0.288281. Year 10: BV 69876.34, NI = 0.15·69876.34 = 10481.45, XR₁₀ = 3913.07. Terminal: BV 73370.15, NI 11005.52, XR 4108.73. TV = 4108.73/0.044 = 93,380.20. PV₁₀ = (3913.07 + 93380.20)/2.48729 = 39,116.18. Σ PV = 65,993.76. Add 17,997 book equity → 83,990.76. Divide by 1120.713 shares → **74.94 per share**.

#### Reimplementation notes (Python)

Inputs:

- Current financials (float, currency unless noted): net_income, bv_equity_current, bv_equity_prior, eps, dps, shares (count).
- Normalization: normalize (bool); if true, approach (1|2) plus ni_history (list of 5 floats) for approach 1 or normalized_roe (fraction) for approach 2.
- Discount rate (fractions): beta, riskfree, risk_premium.
- High growth: n_high (int, sheet uses 10); optional overrides roe_high and retention_high (fractions); fade_second_half (bool).
- Stable: g_stable, roe_stable (fractions); optional payout_stable override; optional beta_stable and premium_stable (else reuse high-growth beta/premium).

Branches:
- normalize="Yes": replace NI with 5-yr average (approach 1) or normalized_roe × BV (approach 2, inferred) before computing fundamental ROE.
- override flags for high-growth ROE/retention and stable ROE.
- payout_stable defaults to `1 − g_stable/roe_stable`; overridable.
- fade_second_half="Yes": linear fade of ROE, payout, and ke over the last floor(n/2) years (sheet: years 6–10 of 10). "No" would hold high-growth values through year n, then jump to stable in the terminal year (inferred from Read-me text; not exercised in this sheet).
- Read-me states n_high = 0 collapses to a stable-growth-only model — support it.

Outputs: per-year arrays (bv_begin, roe, ni, ke, equity_cost, excess_return, payout, dividends, retained, cum_ke, pv), terminal block, tv_excess_returns, pv_excess_returns, equity_value, value_per_share.

Edge cases:
- `ke_stable ≤ g_stable` → terminal value invalid; validate.
- `roe_stable = 0` → payout formula divides by zero.
- `roe_stable < g_stable` → payout `1 − g/ROE` goes negative (retention > 1); the sheet carries it mechanically, a port should at least warn.
- Negative net income / negative fundamental ROE: model is mechanical (NI = ROE·BV), so a negative ROE input produces negative NI and negative excess returns — normalization (B7) is the intended remedy; no floor is applied.
- Fundamental ROE uses **prior-year** book equity (NI_last / BV_prior), while the valuation rolls forward from **current** book equity — keep both BV inputs distinct.
- Growth rate (retention × ROE) is displayed but the engine is BV-rollforward driven; NI growth emerges from ROE × growing BV, do not grow NI directly.

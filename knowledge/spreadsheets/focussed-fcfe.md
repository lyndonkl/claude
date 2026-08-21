# Damodaran Focussed Valuation Models — FCFE family (fcfest, fcfe2st, fcfe3st)

Source: `/Users/kushaldsouza/Downloads/2020/Spreadsheets/Focussed Valuation Model Spreadsheet/`
All three files are legacy `.xls`; dumps show computed values only. Every formula below was
reconstructed from labels, layout, and by reproducing each stored value numerically to full float
precision — all reconstructions verified to match; formulas are still flagged "(inferred)" per
convention. All models are per-share (Damodaran notes aggregate-company numbers work too).

Common notation: `EPS` = earnings per share, `DPS` = dividends per share, `DR` = debt financing
ratio, `ke` = cost of equity, `g` = growth rate, `gn` = stable growth rate, `RR` = reinvestment
rate, `t` = tax rate. CAPM: `ke = riskfree + beta * risk_premium`. All rates are decimals in the
sheets (0.06 = 6%) despite labels saying "(in percent)".

---

### fcfest.xls — sheet `NewFCFEStableGrowth` (73 rows x 8 cols)

**Purpose:** FCFE stable-growth (Gordon-growth) model. It values the equity of a firm already in
steady state that will grow at a constant rate forever. It uses free cash flow to equity instead
of dividends. Damodaran uses it for firms whose dividends differ from what they could afford to
pay (Dividends ≠ FCFE). This is his single-stage FCFE model.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Current Earnings per share | D21 | 5.45 |
| Capital Spending/share | D23 | 2.0 |
| Depreciation / share | D24 | 1.7469204927211646 |
| Chg. Working Capital/share | D25 | 0.6 |
| Desired debt financing ratio (for capex; label at B26) | D26 | 0.2997 |
| Offset capital expenditures by depreciation in future? (Yes/No) | G27 | "No" |
| Recompute reinvestment rate from fundamentals? (Yes/No) | G29 | "Yes" |
| If yes: expected perpetual return on equity (ROE) | G30 | 0.12 |
| Desired debt financing ratio (repeat, for working capital; label at B31) | D31 | 0.2997 |
| Directly entering cost of equity? (Yes/No) | F33 | "No" |
| If yes: cost of equity | D34 | (empty) |
| If no: Beta of the stock | D36 | 1.1 |
| If no: Riskfree rate | D37 | 0.07 |
| If no: Risk Premium | D38 | 0.055 |
| Expected Growth Rate (forever) | D40 | 0.06 |

Note: the debt ratio appears twice (D26 and D31) with identical values; layout suggests D26
applies to capex and D31 to working capital (inferred). Both terms use (1−DR) identically.

**Logic (all inferred, numerically verified):**

1. Cost of equity (D58):
   - If F33 = "Yes": `ke = D34`.
   - Else CAPM: `ke = D37 + D36*D38` = 0.07 + 1.1*0.055 = **0.1305**.
2. Reinvestment rate implied by the input line items (G28):
   `RR_inputs = [ (CapEx − Depr)*(1−DR) + ΔWC*(1−DR) ] / EPS`
   = [(2.0−1.746920)*0.7003 + 0.6*0.7003] / 5.45 = 0.10961680.
   If G27 = "Yes" (offset capex by depreciation), net capex = 0, so
   `RR_inputs = ΔWC*(1−DR)/EPS` (inferred branch).
3. Reinvestment rate actually used:
   - If G29 = "Yes" (recompute from fundamentals): `RR = g / ROE` = 0.06/0.12 = **0.5**.
   - Else: `RR = RR_inputs`.
4. FCFE per share (F56): `FCFE = EPS * (1 − RR)` = 5.45 * 0.5 = **2.725**.
   (Equivalently EPS − (1−DR)(CapEx−Depr) − (1−DR)ΔWC when using input line items.)
   Display quirk: when RR is recomputed from fundamentals, the sheet back-solves the displayed
   "(Capital Spending − Depreciation)" line so the components still add up.
   E53 = [EPS*RR − (1−DR)*ΔWC] / (1−DR) = (2.725 − 0.42018)/0.7003 = 3.29119. This is display
   only. F53 = (1−DR)*E53 = 2.30482. F55 = (1−DR)*ΔWC = 0.42018.
   Check: 5.45 − 2.30482 − 0.42018 = 2.725.
5. Gordon Growth value (F61): `Value = FCFE * (1+g) / (ke − g)`
   = 2.725*1.06 / (0.1305−0.06) = 2.8885/0.0705 = **40.9716**.

**Reference data:** none (no lookup tables). The only table is the output sensitivity table below.

**Outputs:**

| Cell | Meaning | Value |
|---|---|---|
| G28 | Reinvestment rate implied by inputs | 0.10961680347658136 |
| D58 | Cost of equity | 0.1305 |
| F56 | FCFE per share | 2.725 |
| F61 | Gordon Growth Model value per share | 40.97163120567375 |
| B64:C73 | Sensitivity table: value vs growth rate | see below |
| B45/C45:C47 | Warnings area (empty in this sheet; presumably flags e.g. g ≥ ke — content not recoverable) | blank |

Sensitivity table (B64:C73), verbatim values. Recomputed as `Value = FCFE*(1+g)/(ke−g)` holding
FCFE fixed at 2.725 and ke at 0.1305 — only g varies (inferred, verified at g=0.10 and g=0.02):

| Growth rate | Value |
|---|---|
| 0.10 | 98.27868852459018 |
| 0.09 | 73.3395061728395 |
| 0.08 | 58.27722772277228 |
| 0.07 | 48.19421487603305 |
| 0.06 | 40.97163120567375 |
| 0.05 | 35.543478260869556 |
| 0.04 | 31.31491712707182 |
| 0.03 | 27.927860696517413 |
| 0.02 | 25.15384615384615 |

**Worked example (values currently in sheet):**
EPS 5.45; ke = 0.07 + 1.1*0.055 = 0.1305. Recompute-from-fundamentals = Yes with ROE 0.12 and
g 0.06 → RR = 0.5 → FCFE = 5.45*(1−0.5) = 2.725. Value = 2.725*1.06/(0.1305−0.06) = 40.97.
(Had recompute been "No": FCFE = 5.45 − 0.7003*(2.0−1.746920) − 0.7003*0.6 = 5.45 − 0.17723 −
0.42018 = 4.85258, value = 4.85258*1.06/0.0705 = 72.96 — inferred branch.)

**Reimplementation notes:**
- Inputs: eps (float, currency/share), capex (float), depreciation (float), chg_wc (float),
  debt_ratio (float 0–1), offset_capex_with_depr (bool), recompute_rr_from_fundamentals (bool),
  stable_roe (float, required if recompute), direct_cost_of_equity (float | None), beta, riskfree,
  risk_premium (floats, used when ke not given), growth (float).
- Outputs: cost_of_equity, fcfe, reinvestment_rate, value_per_share, sensitivity table (g → value).
- Branches: (a) ke direct vs CAPM; (b) RR from fundamentals (g/ROE) vs from line items;
  (c) offset capex with depreciation (net capex = 0).
- Edge cases: raise/warn if g ≥ ke (division by ≤0); warn if g materially above nominal economy
  growth (sheet text says stable g "cannot be significantly higher than the nominal growth rate in
  the economy"); RR from fundamentals requires ROE ≠ 0; FCFE ≤ 0 makes value meaningless; negative
  EPS invalidates the RR = reinvestment/EPS formulation.

---

### fcfe2st.xls — sheet `NewFCFE2Stage` (139 rows x 14 cols)

**Purpose:** Two-stage FCFE discount model. Values equity of a firm with an initial
high-growth period (up to 10 years; sheet header says "upto 6" but columns D–M hold years 1–10)
followed by stable growth forever. Growth drops abruptly (not gradually) at the stage boundary.
Used when FCFE, not dividends, is the right cash-flow measure.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Current Earnings per share | D21 | 4.0 |
| Current Dividends per share | D22 | 0.25 |
| Current Capital Spending/sh | D23 | 3.7 |
| Current Depreciation / share | D24 | 1.7 |
| Current Revenues/ share | D25 | 20.0 |
| Working Capital/ share | D26 | 8.0 |
| Chg. Working Capital/share | D27 | 1.0 |
| Length of extraordinary growth period (years) | E29 | 5 |
| Enter cost of equity directly? (Yes/No) | E31 | "No" |
| If yes: cost of equity | E32 | (empty) |
| If no: Beta of the stock | D34 | 1.3 |
| If no: Riskfree rate | D35 | 0.07 |
| If no: Risk Premium | D36 | 0.055 |
| Use historical growth rate? (Yes/No) | E39 | "Yes" |
| If yes: EPS from five years ago | E40 | 0.49 |
| Outside estimate of growth? (Yes/No) | E42 | "Yes" |
| If yes: estimated growth | E43 | 0.19 |
| Calculate growth from fundamentals? (Yes/No) | F45 | "Yes" |
| Net Income Currently | D47 | 1077.0 |
| Interest Expense Currently | D48 | 53.85 |
| Book Value of Debt: current / last year | D49 / E49 | 600.0 / 550.0 |
| Book Value of Equity: current / last year | D50 / E50 | 5445.0 / 5130.0 |
| Tax Rate on Income | D51 | 0.36 |
| Change fundamental inputs for high-growth period? (Yes/No) | F55 | "No" |
| If yes: ROC / D/E / Retention / Interest Rate overrides | C57 / E57 / C58 / E58 | (echo computed: 0.19568… / 0.11019… / 0.9375 / 0.08975) |
| Weight: historical growth | E61 | 0.1 |
| Weight: outside prediction | E62 | 0.4 |
| Weight: fundamental estimate | E63 | 0.5 |
| Stable-period growth rate | E65 | 0.06 |
| Beta changes in stable period? (Yes/No) | E68 | "Yes" |
| If yes: stable-period beta | E69 | 1.1 |
| Capex/depr/WC grow at same rate as earnings? (Yes/No) | F72 | "No" |
| If not — high-growth rates: Capital Spending / Depreciation / Revenues | C75 / D75 / E75 | 0.2 / 0.2 / 0.18 |
| Stable-growth: Revenues growth (capex & depr say "Do not enter") | E76 | 0.06 |
| Keep current working-capital-to-revenues fraction? (Yes/No) | F78 | "Yes" |
| If no: WC as percent of revenues | E79 | 0.4 |
| Use current debt ratio as desired mix? (Yes/No) | F81 | "Yes" |
| If no: desired debt proportion — Capital Spending | E83 | (empty) |
| If no: desired debt proportion — Working Capital | E84 | (empty) |
| Stable period: capex offset by depreciation? (Yes/No) | F87 | "No" |
| Compute stable reinvestment rate from fundamentals? (Yes/No) | F88 | "Yes" |
| If yes: return on equity in stable growth period | F89 | 0.12 |
| If no: capex as % of depreciation in stable growth | F90 | 1.5 |

**Logic (all inferred, numerically verified):**

*Cost of equity*
1. High-growth ke (D93) = E32 if E31="Yes", else `riskfree + beta_hg * premium`
   = 0.07 + 1.3*0.055 = **0.1415**.
2. Stable ke (E127) = `riskfree + beta_stable * premium` = 0.07 + 1.1*0.055 = **0.1305**
   (beta_stable = E69 if E68="Yes", else beta_hg; if ke entered directly it presumably applies to
   both stages).

*Debt ratios*
3. If F81="Yes": `DR_capex = DR_wc = BV_Debt_current / (BV_Debt_current + BV_Equity_current)`
   = 600/6045 = **0.09925558** (E95, E96). Else the user-entered E83/E84.

*Current FCFE (E98:E101)*
4. `FCFE_0 = EPS − (CapEx − Depr)*(1−DR_capex) − ΔWC*(1−DR_wc)`
   = 4.0 − (3.7−1.7)*0.9007444 − 1.0*0.9007444 = 4.0 − 1.8014888 − 0.9007444 = **1.2977667**.

*High-growth earnings growth rate (D105:D108)*
5. Historical (D105): `g_hist = (EPS_now / EPS_5yrs_ago)^(1/5) − 1` = (4.0/0.49)^0.2 − 1
   = **0.52185327** (0 if E39="No").
6. Outside (D106): E43 = 0.19 (0 if E42="No").
7. Fundamental (D107), Damodaran's levered-growth formula (0 if F45="No"):
   - `ROC = (Net Income + Interest Expense*(1−t)) / (BV_Debt_last + BV_Equity_last)`
     = (1077 + 53.85*0.64)/(550+5130) = 1111.464/5680 = **0.19568028** (C53). Uses LAST-YEAR
     (beginning) book values, columns E49/E50.
   - `D/E = BV_Debt_current / BV_Equity_current` = 600/5445 = **0.11019284** (E53). Current-year.
   - `Retention b = 1 − DPS/EPS` = 1 − 0.25/4.0 = **0.9375** (C54).
   - `Interest rate i = Interest Expense / BV_Debt_current` = 53.85/600 = **0.08975** (E54).
   - If F55="Yes" these four are replaced by the C57/E57/C58/E58 overrides.
   - `g_fund = b * [ ROC + (D/E) * (ROC − i*(1−t)) ]`
     = 0.9375*(0.19568028 + 0.11019284*(0.19568028 − 0.08975*0.64)) = **0.19773128**.
8. Weighted average (D108): `g_hg = w_hist*g_hist + w_out*g_out + w_fund*g_fund`
   = 0.1*0.52185327 + 0.4*0.19 + 0.5*0.19773128 = **0.22705097**.

*Growth rates for line items (D112:E114)*
9. If F72="Yes": capex, depreciation and revenues all grow at g_hg in high growth.
   Else use C75/D75/E75 (0.2/0.2/0.18 here). In stable phase revenues grow at E76 (0.06);
   capex and depreciation are handled by the stable reinvestment logic (step 13).
10. WC-to-revenues ratio (E116): if F78="Yes", `wc_pct = WC_0/Rev_0` = 8/20 = **0.4**;
    else the E79 entry.

*High-growth projections, years i = 1..n (n = E29, columns D..M; sheet supports n ≤ 10)*
11. Row 119 `Earnings_i = EPS * (1+g_hg)^i` (yr1 = 4*1.22705097 = 4.90820388).
    Row 120 `NetCapex_i = (CapEx_0*(1+g_cx)^i − Depr_0*(1+g_dep)^i) * (1−DR_capex)`
      (yr1 = (3.7*1.2 − 1.7*1.2)*0.9007444 = 2.16178660).
    Row 121 `ΔWC_i = wc_pct * (Rev_i − Rev_{i−1}) * (1−DR_wc)` with `Rev_i = Rev_0*(1+g_rev)^i`
      (yr1 = 0.4*(23.6−20)*0.9007444 = 1.29707196).
    Row 122 `FCFE_i = Earnings_i − NetCapex_i − ΔWC_i` (yr1 = 1.44934532).
    Row 123 `PV_i = FCFE_i / (1+ke_hg)^i` (yr1 = 1.44934532/1.1415 = 1.26968490).

*Terminal year (column N) and terminal value*
12. `Earnings_T = Earnings_n * (1+gn)` = 11.12686980*1.06 = **11.79448199** (N119).
13. Stable reinvestment:
    - If F88="Yes" (fundamentals): `RR_stable = gn / ROE_stable` = 0.06/0.12 = 0.5, and
      `FCFE_T = Earnings_T * (1 − RR_stable)` = **5.89724099** (N122).
      Display back-solve: `ΔWC_T = wc_pct*(Rev_n*(1+g_rev_stable) − Rev_n)*(1−DR_wc)`
      = 0.4*(20*1.18^5)*0.06*0.9007444 = 0.98912881 (N121), and
      `NetCapex_T = Earnings_T*RR_stable − ΔWC_T` = 4.90811218 (N120) so components sum to FCFE_T.
    - Else if F87="Yes": stable net capex = 0 (capex offset by depreciation), FCFE_T =
      Earnings_T − ΔWC_T (inferred branch).
    - Else: stable capex = F90 * stable depreciation, i.e. `NetCapex_T = (F90 − 1) * Depr_T *
      (1−DR_capex)` with Depr_T = Depr_0*(1+g_dep)^n*(1+gn); FCFE_T = Earnings_T − NetCapex_T −
      ΔWC_T (inferred branch, not active in sheet).
14. Terminal price (E128): `P_n = FCFE_T / (ke_stable − gn)` = 5.89724099/(0.1305−0.06)
    = **83.64880841**. (FCFE_T is already the year-n+1 flow; no extra (1+g) factor.)

*Value (F130:F132)*
15. `PV_highgrowth = Σ PV_i` = **8.40368507**.
    `PV_terminal = P_n / (1+ke_hg)^n` = 83.64880841/1.1415^5 = **43.15987514**.
    `Value per share = PV_highgrowth + PV_terminal` = **51.56356021**.

*Value-of-growth decomposition (E136:E139)*
16. `Value of assets in place = FCFE_0 / ke_stable` = 1.2977667/0.1305 = **9.94457279**.
    `Value of stable growth = FCFE_0*(1+gn)/(ke_stable − gn) − assets in place`
    = 1.2977667*1.06/0.0705 − 9.94457279 = **9.56794855**.
    `Value of extraordinary growth = total value − FCFE_0*(1+gn)/(ke_stable − gn)`
    = 51.56356021 − 19.51252134 = **32.05103887**.
    Sum (E139) = 51.56356021 = total value.

**Reference data:** none — no lookup/rating tables in this model.

**Outputs:**

| Cell | Meaning | Value |
|---|---|---|
| D93 | Cost of equity, high growth | 0.14150000000000001 |
| E95 / E96 | Debt proportion for capex / for WC | 0.09925558312655088 (both) |
| E101 | Current FCFE per share | 1.2977667493796528 |
| D108 | Weighted-average high-growth rate | 0.22705096962023416 |
| Rows 119–123, cols D–H, N | Year-by-year Earnings / NetCapex / ΔWC / FCFE / PV + terminal year | see worked example |
| E126 | FCFE in stable phase (terminal-year FCFE) | 5.897240992667129 |
| E127 | Cost of equity in stable phase | 0.1305 |
| E128 | Price at end of growth phase | 83.64880840662593 |
| F130 | PV of FCFE in high-growth phase | 8.403685071141142 |
| F131 | PV of terminal price | 43.15987513887654 |
| F132 | **Value of the stock** | 51.56356021001768 |
| E136–E139 | Assets in place / stable growth / extraordinary growth / total | 9.94457 / 9.56795 / 32.05104 / 51.56356 |

**Worked example (sheet values):** ke_hg = 0.1415; DR = 600/6045 = 0.099256; FCFE_0 = 1.297767.
g_hg = 0.1*0.521853 + 0.4*0.19 + 0.5*0.197731 = 0.227051. Years 1–5 FCFE: 1.449345, 1.897927,
2.471042, 3.201279, 4.129455; PVs at 14.15%: 1.269685, 1.456558, 1.661316, 1.885471, 2.130655
(sum 8.403685). Terminal: Earnings_T = 11.126870*1.06 = 11.794482; RR = 0.06/0.12 = 0.5 →
FCFE_T = 5.897241; P_5 = 5.897241/0.0705 = 83.648808; PV = 83.648808/1.1415^5 = 43.159875.
Value = 8.403685 + 43.159875 = **51.5636**.

**Reimplementation notes:**

Inputs a Python port needs:
- Per-share floats (currency): eps, dps, capex, depreciation, revenues, working_capital,
  chg_working_capital.
- n_high (int years, 1–10).
- Cost of equity: either ke_direct (float), or beta_hg + riskfree + premium (floats).
- Growth estimators, each with an on/off toggle: use_historical (bool) + eps_5yr_ago;
  use_outside (bool) + g_outside; use_fundamental (bool) + its inputs. The fundamental inputs
  are net_income, interest_expense, bv_debt_now, bv_debt_prior, bv_equity_now, bv_equity_prior,
  tax_rate, plus optional overrides for roc, de, retention, int_rate.
- Weights w_hist, w_out, w_fund. They should sum to 1. The sheet does not enforce this.
- g_stable (float); stable_beta (optional float).
- Optional per-item growth rates g_capex, g_depr, g_rev. Default: all equal g_hg.
- Optional wc_pct override. Default: WC/Rev.
- Optional DR overrides for capex and WC. Default: book debt ratio.
- Stable-phase reinvestment mode, one of three: offset (bool), fundamentals (roe_stable),
  or capex_as_pct_of_depr (float).

Outputs: per-year table (earnings, net capex, ΔWC, FCFE, PV), terminal FCFE and price, PV
splits, value per share, growth-value decomposition.

Branches: 5-way growth estimation and weighting; toggles for each estimator zero it out; DR
source; WC ratio source; stable reinvestment 3-way; stable beta change.

Edge cases:
- Historical growth needs eps_5yr_ago > 0 and eps > 0. A fractional exponent of a negative
  ratio fails — return 0/NaN and warn.
- ke_stable ≤ gn breaks the terminal value.
- Retention is undefined for eps = 0.
- Negative FCFE years are fine. They appear in fcfe3st.
- Fundamental ROC uses prior-year book values, but D/E and the interest rate use current-year
  values. Keep that asymmetry.
- The terminal ΔWC uses the STABLE revenue growth rate (E76). It applies that rate to year-n
  revenues, which grew at the HIGH-GROWTH revenue rate.

---

### fcfe3st.xls — sheet `NewFCFE3Stage` (163 rows x 14 cols)

**Purpose:** Three-stage FCFE discount model. Values equity of a firm with (1) an initial
extraordinary-growth phase, (2) a transition phase in which growth declines linearly to the stable
rate (beta may also drift linearly to its stable level), and (3) stable growth forever. The
relationship between capital spending and depreciation changes consistently with the growth rate.
Used for firms with very high current growth that will fade gradually, where FCFE ≠ dividends.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Current Earnings per share | D23 | 0.85 |
| Current Dividends per share | D24 | 0.0 |
| Current Capital Spending/sh | D25 | 1.0 |
| Current Depreciation / share | D26 | 0.8 |
| Current Revenues/ share | D27 | 12.5 |
| Working Capital/ share | D28 | 5.0 |
| Chg. Working Capital/share | D29 | 0.5 |
| Enter cost of equity directly? (Yes/No) | E31 | "No" |
| If yes: cost of equity | E32 | (empty) |
| If no: Beta (initial high-growth stage) | D34 | 1.1 |
| Riskfree rate | D35 | 0.07 |
| Risk Premium | D36 | 0.055 |
| Length of extraordinary growth period (years) | E40 | 5 |
| Use historical growth rate? (Yes/No) | E42 | "No" |
| If yes: EPS from five years ago | E43 | 0.9 |
| Outside estimate of growth? (Yes/No) | E45 | "Yes" |
| If yes: estimated growth | E46 | 0.2 |
| Calculate growth from fundamentals? (Yes/No) | F48 | "No" |
| Net Income Currently | D50 | 10.0 |
| Interest Expense Currently | D51 | 2.5 |
| Book Value of Debt: current / last year | D52 / E52 | 16.1 / 15.2 |
| Book Value of Equity: current / last year | D53 / E53 | 29.5 / 28.1 |
| Tax Rate on Income | D54 | 0.45 |
| Change fundamental inputs for high-growth period? (Yes/No) | F58 | "No" |
| If yes: ROC / D/E / Retention / Interest Rate | C60 / E60 / C61 / E61 | 0.25 / 0.5457627 / 1.0 / 0.1552795 |
| Change fundamental inputs for stable period? (Yes/No) | F62 | "Yes" |
| If yes: ROC / D/E / Interest Rate (stable) | C64 / E64 / E65 | 0.2 / 0.5457627 / 0.14 |
| Weight: historical / outside / fundamental growth | E68 / E69 / E70 | 0.0 / 1.0 / 0.0 |
| Length of transition period (years) | E73 | 10 |
| Beta adjusts gradually to stable beta? (Yes/No) | F75 | "Yes" |
| If no: beta for transition period | (B76 row, cell empty) | — |
| Stable-period growth rate | E79 | 0.05 |
| Beta changes in stable period? (Yes/No) | E81 | "Yes" |
| If yes: stable-period beta | E82 | 0.9 |
| Capex/depr/WC grow at same rate as earnings? (Yes/No) | F85 | "Yes" |
| If not — growth rates, High Growth: CapSp / Depr / Rev | C88 / D88 / E88 | 0.2 / 0.2 / 0.18 |
| If not — Transition: CapSp / Depr / Rev | C89 / D89 / E89 | 0.12 / 0.12 / 0.12 |
| If not — Stable: Rev only (capex/depr "Do not enter") | E90 | 0.06 |
| Keep current WC-to-revenues fraction? (Yes/No) | F92 | "Yes" |
| If no: WC as percent of revenues | F93 | (empty) |
| Use current debt ratio as desired mix? (Yes/No) | F95 | "No" |
| If no: desired debt proportion — Capital Spending | E97 | 0.15 |
| If no: desired debt proportion — Working Capital | E98 | 0.15 |
| Stable: capex offset by depreciation? (Yes/No) | F101 | "No" |
| Stable: compute reinvestment rate from fundamentals? (Yes/No) | F102 | "Yes" |
| If yes: return on equity in stable period | F103 | 0.12 |
| If no: capex as % of depreciation in steady state (>100%) | F104 | 1.25 |

**Logic (all inferred, numerically verified):**

*Setup*
1. High-growth ke (D108) = E32 if direct, else `rf + beta_hg*premium` = 0.07+1.1*0.055 = **0.1305**.
2. DR_capex, DR_wc (E111, E112): book ratio `BVD/(BVD+BVE)` if F95="Yes", else E97/E98 = **0.15**.
3. Current FCFE (E114:E117): `FCFE_0 = EPS − (CapEx−Depr)*(1−DR_capex) − ΔWC*(1−DR_wc)`
   = 0.85 − 0.2*0.85 − 0.5*0.85 = **0.255**.
4. High-growth g (D121:D124): same three-estimator machinery as fcfe2st (historical CAGR over 5
   years, outside estimate, fundamental g = b*[ROC + D/E*(ROC − i*(1−t))]), except each estimator
   contributes 0 when its Yes/No toggle is "No" (here D121 = D123 = 0 because E42/F48 = "No").
   The sheet echoes the fundamental inputs at C56/E56/C57/E57.
   ROC = (10+2.5*0.55)/(15.2+28.1) = 0.26270208, using prior-year book values.
   D/E = 16.1/29.5 = 0.54576271. Retention = 1 − 0/0.85 = 1.0. i = 2.5/16.1 = 0.15527950.
   Weighted g_hg = 0*0 + 1.0*0.2 + 0*0 = **0.2**.
   The stable-period fundamental overrides (C64/E64/E65, active since F62="Yes") could feed a
   fundamentals-based stable growth rate. In this sheet the stable g actually used is the
   direct entry E79 (0.05). With F102="Yes", the stable reinvestment uses ROE F103 instead.
   So these overrides are dormant in this configuration (inferred).
5. Line-item growth (rows 128–130): F85="Yes" → capex, depreciation and revenues grow at the
   earnings growth rate in every phase: g_hg in high growth, the declining earnings g in
   transition ("Earnings g"), and gn = 0.05 in stable. (If F85="No", the phase-specific rates
   C88:E90 are used instead; stable capex/depr come from the stable reinvestment logic.)
6. wc_pct (E132) = WC_0/Rev_0 = 5/12.5 = **0.4** (F92="Yes"; else F93).

*Phase 1 — high growth, years 1..n1 (n1 = E40 = 5; columns D..M support up to 10 years)*
7. Rows 136–140, same construction as fcfe2st:
   `E_i = 0.85*1.2^i`; `NetCapex_i = (1.0−0.8)*1.2^i*(1−0.15)`;
   `ΔWC_i = 0.4*(Rev_i − Rev_{i−1})*(1−0.15)`, Rev_i = 12.5*1.2^i;
   `FCFE_i = E_i − NetCapex_i − ΔWC_i`; `PV_i = FCFE_i/(1.1305)^i`.
   Year 1: E = 1.02, NetCapex = 0.204, ΔWC = 0.85, FCFE = **−0.034**, PV = −0.0300752.
   All five high-growth FCFEs are negative (−0.034, −0.0408, −0.04896, −0.058752, −0.0705024).

*Phase 2 — transition, years n1+1 .. n1+n2 (n2 = E73 = 10; columns D..M = years 6..15)*
8. Growth declines linearly (row 144): `g_j = g_hg − j*(g_hg − gn)/n2` for j = 1..n2
   → 0.185, 0.17, 0.155, 0.14, 0.125, 0.11, 0.095, 0.08, 0.065, 0.05.
9. Cumulated growth (row 145): `cum_j = Π_{k≤j}(1+g_k) − 1` (0.185, 0.38645, …, 2.01469465).
10. `Earnings_j = Earnings_n1 * (1+cum_j)`; NetCapex and ΔWC grow the same way (with F85="Yes"
    revenues also compound at g_j, so `ΔWC_j = wc_pct*(Rev_j − Rev_{j−1})*(1−DR_wc)`).
    `FCFE_j = Earnings_j − NetCapex_j − ΔWC_j` — turns positive from year 6 (0.0486467) and grows
    to 3.58287122 by year 15.
11. Beta drift (row 150): if F75="Yes", beta declines linearly from beta_hg to beta_stable over
    the transition: `beta_j = beta_hg − j*(beta_hg − beta_stable)/n2` (1.08, 1.06, …, 0.90).
    If "No", the entered transition beta is used flat (inferred). `ke_j = rf + beta_j*premium`
    (0.1294, 0.1283, …, 0.1195).
12. PV in transition (row 152) uses the cumulative discount factor with the year-specific ke:
    `PV_j = FCFE_j / [ (1+ke_hg)^n1 * Π_{k≤j}(1+ke_k) ]`
    (year 6: 0.0486467/(1.1305^5 * 1.1294) = 0.02332665).
13. End-of-Life Index (row 153): 0 for every transition year except the last, which is 1 — a
    flag marking the final transition year so the terminal price is discounted at the right
    column when n2 < 10 (inferred).

*Phase 3 — stable growth / terminal value*
14. Terminal-year earnings (N146) = `Earnings_15 * (1+gn)` = 6.37629625*1.05 = **6.69511106**.
15. Stable ke (E157) = `rf + beta_stable*premium` = 0.07+0.9*0.055 = **0.1195**.
16. Stable reinvestment — same 3-way branch as fcfe2st: here F102="Yes" →
    `RR_stable = gn/ROE_stable` = 0.05/0.12 = 0.41667; `FCFE_T = Earnings_T*(1−RR_stable)` =
    **3.90548145** (N149/E156). Display back-solve: `ΔWC_T = wc_pct*Rev_15*gn*(1−DR_wc)` =
    0.4*93.76901*0.05*0.85 = 1.59407406 (N148); `NetCapex_T = Earnings_T*RR_stable − ΔWC_T` =
    1.19555555 (N147). Alternatives: F101="Yes" → net capex 0; else capex = F104 * depreciation
    (net capex = (F104−1)*Depr_T*(1−DR_capex)) (inferred branches, inactive).
17. Terminal price (E158): `P = FCFE_T / (ke_stable − gn)` = 3.90548145/0.0695 = **56.19397770**.

*Value (F160:F163)*
18. `PV high growth = Σ years 1..5 PV` = **−0.17003738** (negative FCFE early years).
    `PV transition = Σ years 6..15 PV` = **3.36018099**.
    `PV terminal = P / [ (1+ke_hg)^n1 * Π_{k=1..n2}(1+ke_k) ]` = 56.19397770 / (1.1305^5 *
    1.1294*1.1283*1.1272*1.1261*1.125*1.1239*1.1228*1.1217*1.1206*1.1195) = **9.41786797**.
    `Value of the stock = sum` = **12.60801158**.

**Reference data:** none — no lookup/rating tables in this model.

**Outputs:**

| Cell | Meaning | Value |
|---|---|---|
| D108 | Cost of equity, initial phase | 0.1305 |
| E111 / E112 | Debt proportions (capex / WC) | 0.15 / 0.15 |
| E117 | Current FCFE per share | 0.25500000000000006 |
| D124 | Weighted-average high-growth rate | 0.2 |
| Rows 136–140 (D–H) | High-growth yearly Earnings/NetCapex/ΔWC/FCFE/PV | e.g. yr1: 1.02 / 0.204 / 0.85 / −0.034 / −0.0300752 |
| Rows 144–152 (D–M, N) | Transition yearly g, cumulated g, Earnings, NetCapex, ΔWC, FCFE, beta, ke, PV; terminal-year column N | e.g. yr6: g 0.185, FCFE 0.0486467, beta 1.08, ke 0.1294, PV 0.0233267 |
| E156 | FCFE in terminal year | 3.9054814502214876 |
| E157 | Cost of equity in stable phase | 0.11950000000000001 |
| E158 | Price at end of growth phase | 56.193977701028594 |
| F160 | PV of FCFE, high-growth phase | −0.1700373758747565 |
| F161 | PV of FCFE, transition phase | 3.3601809899892734 |
| F162 | PV of terminal price | 9.417867969902808 |
| F163 | **Value of the stock** | 12.608011584017325 |

**Worked example (sheet values):** EPS 0.85, g_hg 0.2 for 5 years, ke 0.1305, DR 0.15,
wc_pct 0.4. High-growth FCFE all negative (reinvestment exceeds earnings): PV sum −0.170037.
Transition: g falls 0.185 → 0.05 in steps of 0.015; beta falls 1.08 → 0.90 in steps of 0.02;
FCFE goes 0.048647 (yr6) → 3.582871 (yr15); PV sum 3.360181. Terminal: Earnings_T = 6.695111,
RR = 0.05/0.12 → FCFE_T = 3.905481, P = 3.905481/(0.1195−0.05) = 56.193978, PV = 9.417868.
Value = −0.170037 + 3.360181 + 9.417868 = **12.6080**.

**Reimplementation notes:**
- Inputs: everything from the two-stage model, plus n_transition (int), transition beta handling
  (gradual bool | fixed transition beta), stable beta, and optional per-phase line-item growth
  rates (high / transition / stable-revenue). Stable-period fundamental overrides (roc_stable,
  de_stable, i_stable) exist but are dormant when stable g is entered directly and stable RR
  comes from ROE.
- Outputs: three-phase yearly table (year, g, earnings, net capex, ΔWC, FCFE, beta, ke, PV),
  terminal FCFE/price, phase PV subtotals, value per share.
- Key mechanics a port must reproduce exactly:
  - (a) Linear decline of g and beta over the transition, with step = (start − stable)/
    n_transition. The first transition year is already one step down.
  - (b) Cumulative compounding of earnings and line items with the year-specific g.
  - (c) Cumulative discounting. High-growth years discount at constant ke_hg. Transition year j
    discounts at (1+ke_hg)^n1 * Π(1+ke_k). The terminal price discounts through the END of the
    transition.
  - (d) Terminal FCFE = terminal-year earnings * (1 − gn/ROE_stable). Terminal earnings =
    last-transition-year earnings * (1+gn).
  - (e) ΔWC always = wc_pct * ΔRevenues * (1−DR_wc). Revenue growth drives working-capital drag.
- Edge cases:
  - Negative FCFE in early years is normal — keep the sign.
  - If the growth toggles zero out all estimators, the weighted g is 0.
  - Historical CAGR is undefined for non-positive EPS.
  - ke_stable ≤ gn breaks the terminal value.
  - Retention = 1 when DPS = 0.
  - Division by zero occurs if BV debt = 0 (interest rate) or ROE_stable = 0.
  - When n1 or n2 < 10, only the populated columns are used. The End-of-Life index marks the
    last transition column.
  - Labels say "(in percent)" but every rate is a decimal fraction.

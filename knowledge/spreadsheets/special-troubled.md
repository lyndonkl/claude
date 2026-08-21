# Troubled Firms — Damodaran model spreadsheets

Source folder: `/Users/kushaldsouza/Downloads/2020/Spreadsheets/Troubled Firms/`
All three files are legacy `.xls`; dumps expose computed values only, so every formula below was reconstructed from labels, layout, and numeric verification. Reconstructed logic is flagged "(inferred)"; each inferred formula was verified to reproduce the sheet's values to full float precision unless noted.

---

### distress.xls

**Purpose:** Estimates the market-implied (annual and cumulative) probability of distress for a firm from the traded price of one of its bonds. Damodaran uses this when valuing distressed firms: the going-concern DCF value is blended with a distress-sale value using this probability. The sheet prices the bond's promised cash flows, survival-adjusted by an annual distress probability `p`, discounted at the riskfree rate; Excel Solver is used to find the `p` that makes model price = market price.

Only `Sheet1` has content (`Sheet2`, `Sheet3` are empty stubs).

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Coupon Rate = | C2 | 0.12 |
| Maturity of bond = (years) | C3 | 8 |
| Riskfree rate = | C4 | 0.05 |
| Market price of bond = | C5 | 653 (per 1000 face) |
| Probability of distress (Annual) = | D36 | 0.13531709403063646 — **this is the solver's decision variable**, not a computed cell |

Instructions printed on the sheet (E1:E4): "To estimate the probability of distress: 1. Open solver (from tools). 2. Set the value [D34] equal to the market price of bond. 3. Solve for the probability of distress [by changing D36]."

**Logic (all inferred, verified):**

Face value is 1000. Cash-flow schedule for years t = 1..25 (rows 8–32):

1. `CF_t (col B) = CouponRate × 1000` for `t < Maturity`; `= CouponRate × 1000 + 1000` for `t = Maturity`; `= 0` for `t > Maturity`. (In the sheet: 120 for years 1–7, 1120 in year 8, 0 in years 9–25.)
2. Survival-adjusted cash flow: `C_t = CF_t × (1 − p)^t`  where `p` = D36.
3. Present value: `D_t = C_t / (1 + rf)^t`.
4. `Value of bond (D34) = Σ_{t=1..25} D_t` (D33 is a stray 0 in the sum column below year 25).
5. Solver: choose `p` so that `D34 = C5` (market price).
6. `Probability of distress over 5 years (D37) = 1 − (1 − p)^5`.
7. `Probability of distress over 10 years (D38) = 1 − (1 − p)^10`.

**Reference data:** none.

**Outputs:**

| Cell | Meaning | Current value |
|---|---|---|
| D34 | Model value of bond at current `p` | 652.9999998281918 (≈ market price 653; solver already run) |
| D36 | Annual probability of distress `p` | 0.13531709403063646 |
| D37 | Cumulative probability of distress within 5 years | 0.5166247973245933 |
| D38 | Cumulative probability of distress within 10 years | 0.7663484134385095 |

**Worked example (values currently in sheet):** 8-year 12% coupon bond, face 1000, rf 5%, price 653. With p = 0.1353171: year 1 CF = 120 → survival-adjusted 120×(0.8646829)¹ = 103.76194871632362 → PV 103.76.../1.05 = 98.82090353935583. Year 8 CF = 1120 → 1120×0.8646829⁸ = 350.004 → PV /1.05⁸ = 236.896. Sum of PVs = 653.00 = market price, so p solves. 5-yr cumulative = 1−0.8646829⁵ = 0.51662; 10-yr = 0.76635.

**Reimplementation notes:**
- Inputs: `coupon_rate` (decimal), `maturity` (int years, ≤ 25 in the sheet but a port need not cap it), `riskfree_rate` (decimal), `market_price` (currency per 1000 face), optional `face = 1000`.
- Replace Solver with a 1-D root-finder (bisection/Brent on p ∈ [0, 1)) for `f(p) = Σ CF_t(1−p)^t/(1+rf)^t − market_price`. `f` is monotonically decreasing in p, so the root is unique when `market_price` is below the riskfree-discounted promised value and above 0.
- Outputs: `p_annual`, `p_cumulative(n) = 1 − (1−p)^n` (sheet reports n = 5, 10), and model bond value.
- Edge cases: price above the default-free value → no root in [0,1); return p = 0 or raise. Price near 0 → p → 1. Coupon may be 0 (zero-coupon bond still works). The model discounts at the riskfree rate and treats recovery in distress as zero. Both are modeling assumptions, not bugs.

---

### fcffneg.xls

**Purpose:** "A General FCFF Valuation Model — An n-stage Model." Values a firm with **currently negative operating income** and negative FCFF by forecasting year-by-year revenue growth, margin improvement (EBITDA/Revenue path), capex/depreciation paths, and a net-operating-loss (NOL) carryforward that suppresses taxes until exhausted. Damodaran uses this for young or troubled firms whose earnings cannot be normalized — money-losing growth firms. The example in the sheet has EBIT of −1396 on revenues of 3789, priced at 12.57/share: the classic Amazon-style early-2000s case. Three sheets: `Valuation` (inputs + full model), `Summary` (year-by-year FCFF table mirroring the Valuation rows), `Option Valuation` (dilution-adjusted Black–Scholes for management options/warrants, netted from equity).

#### Sheet "Valuation"

**Inputs (rows 20–89):**

| Label | Cell | Example value |
|---|---|---|
| Current EBIT = | D21 | −1396 |
| Current Net Income = | D22 | −1667 (informational; not used downstream (inferred)) |
| Current Dividends = | D23 | 0 (informational) |
| Current Interest Expense = | D24 | 390 (informational) |
| Current Capital Spending | D25 | 4289 |
| Current Depreciation = | D26 | 1381 |
| Tax Rate on Income = | D27 | 0.35 |
| Current Revenues = | D28 | 3789 |
| Current Working Capital = | D29 | −110.5 |
| Chg. Working Capital = | D30 | −63 (informational) |
| Cash and Non-operating assets = | D31 | 1477 |
| Book Value of Debt = | D32 | 7271 |
| Book Value of Equity = | D33 | 15807 |
| NOL carried forward = | D34 | 2075 |
| Is the firm publicly traded? | F37 | "Yes" |
| If yes: market price per share = | F39 | 12.57 |
| … & number of shares outstanding = | F40 | 886.467 |
| … & Market Value of Debt = | F41 | 7271 |
| If no: use book value debt ratio? | (F43) | blank |
| If no: debt-to-capital ratio to use = | (F44) | blank |
| Length of extraordinary growth period (years) = | E46 | 10 |
| Enter cost of equity directly? | E49 | "No" |
| If yes: cost of equity = | (F50) | blank |
| Beta of the stock = | D52 | 2.0 |
| Riskfree rate = | D53 | 0.054 |
| Risk Premium = | D54 | 0.04 |
| Cost of debt (pre-tax, for cost of capital) = | E56 | 0.089 |
| Year-by-year table, years 1..n (B62:G71) | see below | see below |
| Growth rate in stable period = | E73 | 0.05 |
| EBITDA as % of Revenue in stable phase = | E74 | 0.33 |
| Working Capital as % of Revenue in stable phase = | E75 | 0.03 |
| Will the beta change in the stable period? | E77 | "Yes" |
| If yes: beta for stable period = | E78 | 1.0 |
| Change the debt ratio in stable growth? | F80 | "No" |
| If yes: stable-period debt ratio = | F81 | 0.15 (unused since F80 = No) |
| Will cost of debt change in stable period? | E83 | "Yes" |
| If yes: new (pre-tax) cost of debt = | E84 | 0.08 |
| Compute stable reinvestment from fundamentals? | F87 | "Yes" |
| If yes: return on capital in stable growth = | F88 | 0.09 |
| If no: capex as % of depreciation in steady state = | F89 | 1.1 (unused since F87 = Yes) |

Year-by-year earnings inputs (B62:G71), one row per year 1..10 (n = E46 rows are used):

| Year | Growth rate in Revenue (C) | EBITDA/Revenue (D) | Growth rate in Capital Spending (E) | Growth rate in Depreciation (F) | Working Capital as % of Revenue (G) |
|---|---|---|---|---|---|
| 1 | 0.00 | 0.000 | −0.20 | 0.10 | 0.03 |
| 2 | 0.30 | 0.075 | −0.50 | 0.10 | 0.03 |
| 3 | 0.25 | 0.150 | −0.50 | 0.10 | 0.03 |
| 4 | 0.20 | 0.225 | −0.50 | 0.10 | 0.03 |
| 5 | 0.10 | 0.300 | 0.05 | −0.50 | 0.03 |
| 6 | 0.10 | 0.306 | 0.05 | −0.50 | 0.03 |
| 7 | 0.10 | 0.312 | 0.05 | 0.05 | 0.03 |
| 8 | 0.08 | 0.318 | 0.05 | 0.05 | 0.03 |
| 9 | 0.06 | 0.324 | 0.05 | 0.05 | 0.03 |
| 10 | 0.05 | 0.330 | 0.05 | 0.05 | 0.03 |

C72 "Compounded Avg" = geometric mean revenue growth = (Rev_n/Rev_0)^(1/n) − 1 = 0.07747655 (inferred, informational).

**Logic (all inferred, verified to float precision against the sheet):**

*Capital-structure weights and base costs (rows 92–96):*
- `MV equity = price × shares = 12.57 × 886.467 = 11142.89` (if publicly traded; else book or user debt ratio per F43/F44).
- `E/(D+E) (D93) = MVE/(MVE + MV debt) = 0.6051350407232987`; `D/(D+E) (D95) = 0.3948649592767013`. Held **constant for all years** including terminal (F80 = "No"); if F80 = "Yes", the stable-period debt ratio F81 replaces it in the stable phase.
- `Cost of equity (D92) = rf + β × premium = 0.054 + 2.0×0.04 = 0.134` (or F50 directly if E49 = "Yes").
- `After-tax cost of debt (D94) = kd × (1 − tax rate) = 0.089×0.65 = 0.05785`.
- `Cost of capital (D96) = ke×E/(D+E) + kd(1−t)×D/(D+E) = 0.1039310333510792`. **Note:** D96 is a headline display using the marginal tax rate; the per-year discounting below uses year-specific tax rates instead.

*Forecast table (columns C..L = years 1..10, M = terminal year; rows 99–112):*
1. `Revenues_t = Revenues_{t−1} × (1 + g_t)`; Revenues_0 = D28; year 1 uses g_1 (here 0, so year 1 revenue = current revenue). Terminal: `Rev_T = Rev_n × (1 + g_stable)`.
2. `EBITDA_t = Revenues_t × (EBITDA/Rev)_t`; terminal uses E74. `Operating Expenses_t = Revenues_t − EBITDA_t`.
3. `Depreciation_t = Depreciation_{t−1} × (1 + gdep_t)`; Dep_0 = D26. Terminal: `Dep_T = Dep_n × (1 + g_stable)`.
4. `EBIT_t = EBITDA_t − Depreciation_t` (can be negative for early years).
5. NOL rollforward (row 111, end-of-year balances): `NOL_1_start = D34`; `NOL_t = max(0, NOL_{t−1,end} − max(EBIT_t, 0)) + max(−EBIT_t, 0)` — i.e. losses add to the NOL, profits draw it down, floor at 0. (Verified: NOL end-of-year = 3594.1, 4895.68, 5810.22, 6169.72, 4742.46, 2512.26, 0, 0, 0, 0.)
6. Taxes (row 104, "EBIT*t"): `Taxes_t = tax_rate × max(0, EBIT_t − NOL_available_t)` where NOL_available is the carryforward at the start of year t. Zero while EBIT ≤ 0 or fully sheltered. Year 7: (2537.503 − 2512.259)×0.35 = 8.8357.
7. Effective tax rate row 115: `Taxes_t / EBIT_t` when EBIT > 0 else 0 (0, …, 0, 0.0034820, 0.35, 0.35, 0.35; terminal 0.35).
8. `EBIT(1−t)_t = EBIT_t − Taxes_t` (row 105). Negative EBIT passes through untaxed (no tax refund).
9. `Capital Spending_t = CapEx_{t−1} × (1 + gcapex_t)`; CapEx_0 = D25.
10. `Chg. Working Capital_t = wc%_t × (Revenues_t − Revenues_{t−1})` (so year 1 with 0 revenue growth ⇒ ΔWC = 0; the current-WC level D29 is NOT used in the forecast). Terminal: `wc%_stable × (Rev_T − Rev_n)`.
11. `FCFF_t = EBIT(1−t)_t + Depreciation_t − CapEx_t − ΔWC_t` (row 109).
12. Terminal-year reinvestment: since F87 = "Yes", `reinvestment_T = EBIT(1−t)_T × (g_stable / ROC_stable)` = 2243.0588 × (0.05/0.09) = 1246.14; `FCFF_T = EBIT(1−t)_T × (1 − g/ROC) = 996.9150096829808`. The displayed terminal CapEx row is backed out: `CapEx_T = reinvestment_T + Dep_T − ΔWC_T = 1873.5476557442935`. If F87 = "No", instead `CapEx_T = F89 × Dep_T` (capex as % of depreciation) and FCFF_T = EBIT(1−t)_T + Dep_T − CapEx_T − ΔWC_T.

*Year-specific cost of capital (rows 114–121):* beta and pre-tax cost of debt hold their high-growth values through year n/2. They then move linearly to their stable values over years n/2+1 .. n (years 6–10 here):
- `Beta_t`: 2.0 for years 1–5, then 1.8, 1.6, 1.4, 1.2, 1.0; terminal 1.0.
- `ke_t = rf + Beta_t × premium` (0.134 → 0.094).
- Pre-tax `kd_t`: 0.089 for years 1–5, then linear to 0.08: 0.0872, 0.0854, 0.0836, 0.0818, 0.08. Displayed row 118 "Cost of Debt" is **after-tax at that year's effective tax rate**: `kd_t × (1 − taxrate_t)` → 0.089 (t=0), …, 0.0872, 0.08510263 (yr 7, t=0.00348), 0.05434, 0.05317, 0.052.
- `WACC_t = ke_t × E/(D+E) + kd_t × (1 − taxrate_t) × D/(D+E)` (row 120): 0.11623107683254844 for years 1–5 (NOL ⇒ no tax shield on debt), then 0.110679, 0.105010, 0.088022, 0.082719, 0.077416.
- `Cum.WACC_t = Π_{i=1..t} (1 + WACC_i)` (row 121; ends 2.6993671021484515).
- `PV_t = FCFF_t / Cum.WACC_t` (row 110).
- Row 112 "Index" = 1 in the final high-growth year, 0 elsewhere (internal marker for terminal-value placement (inferred)).

*Terminal value and equity (rows 123–140):*
- `Stable WACC (E129) = ke_stable × E/(D+E) + kd_stable(1−t) × D/(D+E) = 0.094×0.605135 + 0.052×0.394865 = 0.07741567171037855`.
- `Terminal value (E130) = FCFF_T / (WACC_stable − g_stable) = 996.915/(0.0774157−0.05) = 36362.961309665305`.
- `PV of high-growth FCFF (F132) = Σ_{t=1..n} PV_t = 2446.419060292443`.
- `PV of terminal value (F133) = E130 / Cum.WACC_n = 36362.96/2.699367 = 13470.92112100043`.
- `Value of firm (F134) = F132 + F133 = 15917.340181292873`.
- `+ Cash and marketable securities (F135) = D31 = 1477`.
- `− Market value of debt (F136) = F41 = 7271`.
- `Market value of equity (F137) = F134 + F135 − F136 = 10123.340181292871`.
- `− Value of options outstanding (F138) = 299.7312206641817` (from Option Valuation sheet).
- `Value of equity in common stock (F139) = 9823.60896062869`.
- `Value per share (F140) = F139 / shares = 9823.609/886.467 = 11.081753703892744`.

#### Sheet "Summary"

Pure display: one row per year 1..10 plus "Term. Year". Columns: Year, Revenues, EBITDA, Depreciation, EBIT, NOL at beginning of year, Taxes, EBIT(1−t), Capital Expenditures, Depreciation, Change in working capital, FCFF. All values are identical to the Valuation-sheet rows. Note its NOL column is *beginning*-of-year: 2075, 3594.1, 4895.68, 5810.22, 6169.72, 4742.46, 2512.26, 0, 0, 0; terminal 0. Stray cell H15 = 0.4166666666666667 with no label (ignore). A port does not need this sheet — it is a reshaped view.

#### Sheet "Option Valuation"

**Purpose:** Value outstanding management options/warrants with the dilution-adjusted Black–Scholes so their value can be subtracted from equity (feeds F138 on Valuation).

**Inputs:**

| Label | Cell | Example |
|---|---|---|
| Current stock price = | D2 | 12.57 |
| Strike price = | D3 | 13.375 |
| Expiration (years) = | D4 | 8.4 |
| Standard deviation in stock prices (volatility) = | D5 | 0.5 |
| Annualized dividend yield = | D6 | 0.0 |
| Treasury bond rate = | D7 | 0.065 |
| Number of warrants (options) outstanding = | D8 | 38 |
| Number of shares outstanding = | D9 | 886.467 |

**Logic (inferred, verified; note the S-adjustment is circular — the sheet relies on Excel iterative calculation):**
1. `Variance = σ² = 0.25`; `Div.-adj. interest rate (F18) = r − y = 0.065`.
2. Dilution-adjusted spot (C15, circular): `S_adj = (S × n_shares + C × n_warrants) / (n_shares + n_warrants)` where `C` is the call value computed in step 4. Converges to 12.377533660622165. Adjusted K (C16) = K unchanged.
3. `d1 = [ln(S_adj/K) + (r − y + σ²/2)·T] / (σ√T) = 1.047861608710055`; `d2 = d1 − σ√T = −0.401276065908889`; `N(d1) = 0.8526488137460766`, `N(d2) = 0.3441084414595671` (standard normal CDF).
4. `Value of the call (C26) = S_adj·e^{−yT}·N(d1) − K·e^{−rT}·N(d2) = 7.887663701688993`.
5. `Value of options (C28) = C × n_warrants = 299.7312206641817` → subtracted from equity on the Valuation sheet. (No adjustment for vesting, taxes, or exercise proceeds beyond the dilution formula.)

**Reference data:** none in this workbook.

**Outputs:** F134 firm value 15917.34; F137 equity 10123.34; F138 option value 299.73; F139 common equity 9823.61; F140 **value per share 11.08** vs market price 12.57.

**Worked example (full chain, current sheet values):** Revenues grow 3789 → 11821.05 by year 10 (schedule above). EBITDA margin ramps 0% → 33%, so EBITDA 0 → 3830.02. Depreciation 1381 → ×1.1 three years, ×0.5 twice, then ×1.05 → 614.41 in year 10. EBIT is negative through year 4 (−1519.1, −1301.58, −914.54, −359.50), turns positive year 5 (1427.26). NOL of 2075 grows with early losses to a peak 6169.72 (end year 4) and is exhausted during year 7, so taxes are 0 for years 1–6, 8.84 in year 7, full 35% thereafter. CapEx falls 4289 → 428.9 by year 4 then grows 5%/yr. FCFF: −3431.2, −1380.27, 28.83, 1196.58, 1965.71, 2238.44, 2536.10, 1804.04, 1965.35, 2112.90. WACC starts at 11.623% (no tax shield), declines to 7.742% as beta (2→1), kd (8.9%→8%), and the tax shield phase in over years 6–10. PV of high-growth FCFF = 2446.42. Terminal: FCFF_T = 2243.06×(1−0.05/0.09) = 996.92; TV = 996.92/0.027416 = 36362.96; PV = 13470.92. Firm 15917.34 + cash 1477 − debt 7271 = equity 10123.34; minus options 299.73 → 9823.61; ÷ 886.467 shares = **11.08 per share**.

**Reimplementation notes:**
- Inputs: scalars listed above (floats, currency units consistent; rates as decimals) plus three parallel arrays of length n (revenue growth, EBITDA margin, capex growth, dep growth, wc% — five arrays) and the stable-phase block. Booleans: publicly_traded, direct_cost_of_equity, beta_changes, debt_ratio_changes, cost_of_debt_changes, reinvestment_from_fundamentals.
- Branches: (a) weights from market values vs book vs user ratio; (b) ke direct vs CAPM; (c) stable debt ratio override; (d) stable kd override; (e) terminal reinvestment from g/ROC vs capex-as-%-of-dep.
- The beta and pre-tax-kd transition runs over the **second half** of the high-growth period: for year t in (n/2, n], `x_t = x_high − (x_high − x_stable) × (t − n/2)/(n/2)` (verified for n = 10; for odd n the sheet's exact midpoint convention is unverified — flag it).
- NOL/tax engine is the heart: taxes_t = taxrate × max(0, EBIT_t − NOL_start_t); NOL_end = NOL_start − min(NOL_start, max(EBIT_t,0)) + max(−EBIT_t, 0). Negative EBIT gets no refund. WACC must use the year's **effective** tax rate for the debt shield.
- ΔWC is driven by revenue *changes*, not by the current WC level; negative revenue growth would release working capital (negative ΔWC) — allow it.
- Terminal value requires `WACC_stable > g_stable`; validate. FCFF_T from fundamentals can be ≤ 0 if g ≥ ROC — validate.
- Option value: solve the circularity by fixed-point iteration (initialize C with plain BS on S; converges in a few iterations) or closed-form root-finding. Subtract from equity before dividing by (undiluted) share count.
- Per-year FCFF discounting uses the cumulative product of (1+WACC_t), not a single rate.

---

### normearn.xls

**Purpose:** "FCFF valuation model … designed to value firms with operating income that is either positive or can be normalized to be positive." This workbook (as distributed here) contains the **earnings-normalization module and its supporting converters** for a troubled firm whose current EBIT is negative or unrepresentative. The pieces: an Earnings Normalizer (3 methods), a Master Inputs sheet, an R&D capitalizer, an operating-lease-to-debt converter, a synthetic-ratings estimator, and an industry-averages lookup table. The Read-me references a "valuation model worksheet" and a "bottom-up beta estimator" but **neither sheet exists in this file** — the seven sheets listed below are all of it. The Read-me also warns: the spreadsheet has deliberate circular references (enable iterative calculation in Excel); in Python, resolve with fixed-point iteration. Damodaran uses this when a firm's problems are temporary (cyclical trough, one-time troubles): value it on normalized earnings rather than actual ones.

Sheets: `Read me first` (instructions, no computation), `Earnings Normalizer & Output`, `Master Inputs Start here`, `R&D converter`, `Operating lease converter`, `Ratings estimator`, `Industry averages`.

Cross-sheet wiring (inferred from matching values):
- Master B10 (EBIT 3455) → lease converter D17.
- Lease-converter kd C14 ← Ratings estimator D10.
- Ratings estimator EBIT F3 ← Normalizer D14.
- Ratings estimator interest F4 = 121 = current operating-lease expense (lease converter E3). In this example the firm has no balance-sheet debt (interest expense 0). The lease commitment interest is therefore the only debt-like charge.
- Ratings firm-type C2 ← Master B22. Master rf B21 → Ratings F5.
- Normalizer D11 note says "! Look at industry average". The user may paste a margin from the Industry averages sheet. In the current sheet, D11 equals the firm's own 5-year aggregate margin from the worksheet below it.

#### Sheet "Master Inputs Start here"

**Inputs:**

| Label | Cell | Example (col C = previous year-end where shown) |
|---|---|---|
| Capitalize R&D expenses? | B4 | "Yes" → go to R&D Converter |
| Convert operating leases to debt? | B5 | "Yes" → go to Operating lease converter |
| Normalize operating income? | B6 | "No" → (Earnings Normalizer) |
| Current EBIT = | B10 | 3455 ("If negative, go back and choose to normalize earnings.") |
| Current Interest Expense = | B11 | 0 |
| Current Capital Spending | B12 | 3100 |
| Current Depreciation & Amort'n = | B13 | 486 |
| Tax Rate on Income = | B14 | 0.35 |
| Current Revenues = | B15 | 12154 (prev: C15 = 8488) |
| Current Non-cash Working Capital = | B16 | −404 |
| Chg. Working Capital = | B17 | −700 |
| Book Value of Debt = | B18 | 0 (prev: C18 = 0) |
| Book Value of Equity = | B19 | 11722 (prev: C19 = 7191) |
| Current riskfree (long-term govt bond) rate | B21 | 0.051 |
| Type of firm (1 = large manufacturing, 2 = smaller/riskier, 3 = financial service) | B22 | 1 |

(The valuation sheet that would consume most of these is absent from this file; the values still feed the converters as wired above.)

#### Sheet "Earnings Normalizer & Output"

**Inputs:**

| Label | Cell | Example |
|---|---|---|
| Approach used to normalize earnings (1, 2, or 3) | D2 | 3 |
| If 1 — Average EBIT (historical average, entered directly) = | D5 | 3500 |
| If 2 — Historical average pre-tax return on capital = | D8 | 0.22 |
| If 3 — Pre-tax operating margin for sector ("! Look at industry average") = | D11 | 0.14716703458425312 |
| Worksheet: last 5 years Revenues (years −5..−1) | B19:F19 | 2032, 2376, 2779, 3155, 3248 |
| Worksheet: last 5 years EBIT (years −5..−1) | B20:F20 | 186, 454, 529, 448, 383 |

**Logic (inferred, verified):**
- Worksheet totals: `G19 = ΣRevenues = 13590`; `G20 = ΣEBIT = 2000`; per-year `OperatingMargin_i = EBIT_i/Revenues_i` (row 21: 0.09154, 0.19108, 0.19036, 0.14200, 0.11792); aggregate `G21 = G20/G19 = 0.14716703458425312`. In the current sheet D11 simply equals G21 (firm's own aggregate 5-yr margin used as the "sector" margin).
- `Normalized EBIT (D14)`:
  - approach 1: `= D5` (historical average EBIT);
  - approach 2: `= D8 × book capital = D8 × (BV debt + BV equity)` = 0.22 × (0 + 11722) = 2578.84 (inferred — consistent with the master-input book values; not the branch currently selected, so unverified against a displayed value);
  - approach 3: `= D11 × Current Revenues` = 0.14716703 × 12154 = **1788.6681383370124** ✓ (matches D14).

**Output:** D14 Normalized EBIT = 1788.6681383370124 → feeds Ratings estimator F3 (and would feed the missing valuation sheet).

#### Sheet "R&D converter"

**Purpose:** Capitalizes R&D: builds a research asset, computes current-year amortization, and adjusts operating income (and, per the header text, net income / book value — those adjustments are stated but not displayed as cells here beyond the ones below).

**Inputs:**

| Label | Cell | Example |
|---|---|---|
| Amortization period N (years, max 10; "if in doubt use lookup table") | F6 | 5 |
| Current year's R&D expense = | F7 | 1594 |
| Past R&D expenses, years −1..−N | B11:B20 | −1: 1026, −2: 698, −3: 399, −4: 211, −5: 89 (rows for −6..−10 zero/unused) |

**Logic (inferred, verified):** for lag k = 0 (current) .. N:
- `Unamortized fraction_k = (N − k)/N` (current year k=0 → 1.0; year −N → 0). Col C rows 24–29: 1, 0.8, 0.6, 0.4, 0.2, 0.
- `Unamortized value_k (col D) = R&D_{−k} × fraction_k`: 1594, 820.8, 418.8, 159.6, 42.2, 0.
- `Amortization this year_k (col E, k ≥ 1) = R&D_{−k} / N`: 205.2, 139.6, 79.8, 42.2, 17.8.
- `Value of Research Asset (D35) = Σ col D = 3035.4` (add to book value of equity/invested capital).
- `Amortization of asset for current year (D37 = E35) = Σ col E = 484.6`.
- `Adjustment to Operating Income (D39) = current R&D − amortization = 1594 − 484.6 = 1109.4` ("a positive number indicates an increase in operating income — add to reported EBIT").
- `Tax Effect of R&D Expensing (D40) = tax rate × D39 = 0.35 × 1109.4 = 388.29` (tax rate from Master B14 (inferred)).

**Reference data — R&D amortization-period lookup (A45:B142, verbatim):**

Rule-of-thumb panel (D46:F51): Non-technological Service — 2 years; Retail, Tech Service — 3 years; Light Manufacturing — 5 years; Heavy Manufacturing — 10 years; Research, with Patenting — 10 years; Long Gestation Period — 10 years.

| Industry | Yrs | Industry | Yrs | Industry | Yrs |
|---|---|---|---|---|---|
| Advertising | 2 | Electric Utility (West) | 10 | Natural Gas (Diversified) | 10 |
| Aerospace/Defense | 10 | Electrical Equipment | 10 | Newspaper | 3 |
| Air Transport | 10 | Electronics | 5 | Office Equip & Supplies | 5 |
| Aluminum | 5 | Entertainment | 3 | Oilfield Services/Equip. | 5 |
| Apparel | 3 | Environmental | 5 | Packaging & Container | 5 |
| Auto & Truck | 10 | Financial Services | 2 | Paper & Forest Products | 10 |
| Auto Parts (OEM) | 5 | Food Processing | 3 | Petroleum (Integrated) | 5 |
| Auto Parts (Replacement) | 5 | Food Wholesalers | 3 | Petroleum (Producing) | 5 |
| Bank | 2 | Foreign Electron/Entertn | 5 | Precision Instrument | 5 |
| Bank (Canadian) | 2 | Foreign Telecom. | 10 | Publishing | 3 |
| Bank (Foreign) | 2 | Furn./Home Furnishings | 3 | R.E.I.T. | 3 |
| Bank (Midwest) | 2 | Gold/Silver Mining | 5 | Railroad | 5 |
| Beverage (Alcoholic) | 3 | Grocery | 2 | Recreation | 5 |
| Beverage (Soft Drink) | 3 | Healthcare Info Systems | 3 | Restaurant | 2 |
| Building Materials | 5 | Home Appliance | 5 | Retail (Special Lines) | 2 |
| Cable TV | 10 | Homebuilding | 5 | Retail Building Supply | 2 |
| Canadian Energy | 10 | Hotel/Gaming | 3 | Retail Store | 2 |
| Cement & Aggregates | 10 | Household Products | 3 | Securities Brokerage | 2 |
| Chemical (Basic) | 10 | Industrial Services | 3 | Semiconductor | 5 |
| Chemical (Diversified) | 10 | Insurance (Diversified) | 3 | Semiconductor Cap Equip | 5 |
| Chemical (Specialty) | 10 | Insurance (Life) | 3 | Shoe | 3 |
| Coal/Alternate Energy | 5 | Insurance (Prop/Casualty) | 3 | Steel (General) | 5 |
| Computer & Peripherals | 5 | Internet | 3 | Steel (Integrated) | 5 |
| Computer Software & Svcs | 3 | Investment Co. (Domestic) | 3 | Telecom. Equipment | 10 |
| Copper | 5 | Investment Co. (Foreign) | 3 | Telecom. Services | 5 |
| Diversified Co. | 5 | Investment Co. (Income) | 3 | Textile | 5 |
| Drug | 10 | Machinery | 10 | Thrift | 2 |
| Drugstore | 3 | Manuf. Housing/Rec Veh | 5 | Tire & Rubber | 5 |
| Educational Services | 3 | Maritime | 10 | Tobacco | 5 |
| Electric Util. (Central) | 10 | Medical Services | 3 | Toiletries/Cosmetics | 3 |
| Electric Utility (East) | 10 | Medical Supplies | 5 | Trucking/Transp. Leasing | 5 |
|  |  | Metal Fabricating | 10 | Utility (Foreign) | 10 |
|  |  | Metals & Mining (Div.) | 5 | Water Utility | 10 |
|  |  | Natural Gas (Distrib.) | 10 |  |  |

#### Sheet "Operating lease converter"

**Inputs:**

| Label | Cell | Example |
|---|---|---|
| Operating lease expense in current year = | E3 | 121 |
| Lease commitments years 1–5 (from footnote) | B6:B10 | 156, 143, 122, 109, 97 |
| Commitment "6 and beyond" (lump sum) | B11 | 448 |
| Reported Operating Income (EBIT) = | D17 | 3455 (← Master B10) |
| Reported Debt = | D18 | 0 |

**Logic (inferred, verified):**
- `Pre-tax cost of debt (C14) = 0.058499999999999996` ← Ratings estimator D10 ("! If you do not have a cost of debt, use the ratings estimator"). Note the circularity: the ratings estimator uses lease expense as interest, whose conversion uses this kd — iterate.
- `Years embedded in yr-6+ lump (D20) = int( B11 / mean(B6:B10) )` = int(448/125.4) = int(3.573) = 3 (sheet note: "I use the average lease expense over the first five years to estimate the number of years of expenses in yr 6"; truncation, not rounding, reproduces the sheet).
- Annualized yr-6+ commitment (B29) = `B11 / D20` = 448/3 = 149.33333333333334.
- PV years 1–5 (C24:C28): `commitment_t / (1+kd)^t` = 147.3784, 127.6305, 102.8696, 86.8286, 72.9991.
- PV of yr-6+ (C29): annuity of B29 for D20 years, valued at end of year 5, discounted back: `B29 × (1 − (1+kd)^−D20)/kd / (1+kd)^5 = 301.2380076126116`. (The on-sheet note says "annuity for ten years" but the computation uses D20 = 3 years — the note is stale.)
- `Debt Value of leases (C30) = Σ PV = 838.944208386745` → add to debt.
- `Depreciation on Operating Lease Asset (F33) = C30 / (5 + D20) = 838.944/8 = 104.86802604834313` (straight line over total lease life (inferred)).
- `Adjustment to Operating Earnings (F34) = C30 × kd = 49.07823619062458` (on-sheet note: "PV of operating leases * Pre-tax cost of debt" — add this imputed interest to EBIT; equivalently EBIT_adj = EBIT + lease expense − lease depreciation under the fuller treatment, but this sheet adds only the interest portion).
- `Adjustment to Total Debt outstanding (F35) = C30 = 838.944208386745`.

#### Sheet "Ratings estimator"

**Inputs:**

| Label | Cell | Example |
|---|---|---|
| Type of firm (1 large mfg, 2 smaller/riskier, 3 financial service) | C2 | 1 |
| Normalized EBIT ("add back only long-term interest for financial firms") | F3 | 1788.6681383370124 (← Normalizer D14) |
| Current interest expenses ("only long-term for financial firms") | F4 | 121 |
| Current long-term government bond rate | F5 | 0.051 |

**Logic (inferred, verified):**
- `Interest coverage ratio (D7) = F3 / F4 = 14.78238130857035`. (Division by zero when interest = 0 — the sheet sidesteps it here by using lease expense 121 as the interest number.)
- `Rating (D8)`: look up D7 in the table for the selected firm type — find the row where `coverage > col-A(lower)` and `coverage ≤ col-B(upper)`. 14.78 > 8.5 → **AAA**.
- `Default spread (D9)`: same row → 0.0075.
- `Cost of debt (D10) = F5 + D9 = 0.051 + 0.0075 = 0.0585` → feeds lease converter.

**Reference data (verbatim — exact thresholds matter):**

*Table 1 — Large manufacturing firms (A15:D28). "If interest coverage ratio is > lower and ≤ upper":*

| > | ≤ | Rating | Spread |
|---|---|---|---|
| −100000 | 0.199999 | D | 0.14 |
| 0.2 | 0.649999 | C | 0.127 |
| 0.65 | 0.799999 | CC | 0.115 |
| 0.8 | 1.249999 | CCC | 0.10 |
| 1.25 | 1.499999 | B− | 0.08 |
| 1.5 | 1.749999 | B | 0.065 |
| 1.75 | 1.999999 | B+ | 0.0475 |
| 2.0 | 2.499999 | BB | 0.035 |
| 2.5 | 2.999999 | BBB | 0.0225 |
| 3.0 | 4.249999 | A− | 0.02 |
| 4.25 | 5.499999 | A | 0.018 |
| 5.5 | 6.499999 | A+ | 0.015 |
| 6.5 | 8.499999 | AA | 0.01 |
| 8.5 | 100000 | AAA | 0.0075 |

*Table 2 — Financial service firms (F15:J28), on long-term interest coverage; the extra "Operating Income Decline" column is carried in the sheet (used in Damodaran's rating-drift analyses) and reproduced verbatim:*

| > | ≤ | Rating | Spread | Operating Income Decline |
|---|---|---|---|---|
| −100000 | 0.049999 | D | 0.14 | −0.50 |
| 0.05 | 0.099999 | C | 0.127 | −0.40 |
| 0.1 | 0.199999 | CC | 0.115 | −0.40 |
| 0.2 | 0.299999 | CCC | 0.10 | −0.40 |
| 0.3 | 0.399999 | B− | 0.08 | −0.25 |
| 0.4 | 0.499999 | B | 0.065 | −0.20 |
| 0.5 | 0.599999 | B+ | 0.0475 | −0.20 |
| 0.6 | 0.799999 | BB | 0.035 | −0.20 |
| 0.8 | 0.999999 | BBB | 0.0225 | −0.20 |
| 1.0 | 1.49999 | A− | 0.02 | −0.175 |
| 1.5 | 1.99999 | A | 0.018 | −0.15 |
| 2.0 | 2.49999 | A+ | 0.015 | −0.10 |
| 2.5 | 2.99999 | AA | 0.01 | −0.05 |
| 3.0 | 100000 | AAA | 0.0075 | 0.00 |

*Table 3 — Smaller and riskier firms (A33:D46):*

| > | ≤ | Rating | Spread |
|---|---|---|---|
| −100000 | 0.499999 | D | 0.14 |
| 0.5 | 0.799999 | C | 0.127 |
| 0.8 | 1.249999 | CC | 0.115 |
| 1.25 | 1.499999 | CCC | 0.10 |
| 1.5 | 1.999999 | B− | 0.08 |
| 2.0 | 2.499999 | B | 0.065 |
| 2.5 | 2.999999 | B+ | 0.0475 |
| 3.0 | 3.499999 | BB | 0.035 |
| 3.5 | 4.499999 | BBB | 0.0225 |
| 4.5 | 5.999999 | A− | 0.02 |
| 6.0 | 7.499999 | A | 0.018 |
| 7.5 | 9.499999 | A+ | 0.015 |
| 9.5 | 12.499999 | AA | 0.01 |
| 12.5 | 100000 | AAA | 0.0075 |

#### Sheet "Industry averages"

Pure reference lookup (94 industries, Value Line-era classification; header row misspells "Inudstry"). Columns: Number of firms; Cap Ex/Depreciation; ROC; Reinvestment Rate; Unlevered Beta; MV Debt-to-Capital Ratio; Non-Cash Working Capital/Sales; Pre-tax Operating Margin; Std Deviation in Equity. "NA" appears for banks/insurers/thrifts in CapEx/Dep, NCWC/Sales, and Operating Margin. Values below rounded to 4 decimals (sheet stores full float precision; ratios are statistical averages, so 4 decimals preserves all practical precision).

| Industry | #Firms | CapEx/Dep | ROC | Reinv. Rate | Unlev. Beta | D/(D+E) | NCWC/Sales | Pre-tax Op. Margin | σ(Equity) |
|---|---|---|---|---|---|---|---|---|---|
| Advertising | 31 | 0.8611 | 0.1231 | −0.1248 | 1.0568 | 0.0846 | −0.1749 | 0.1584 | 0.4817 |
| Aerospace/Defense | 41 | 0.8342 | 0.1193 | 0.0434 | 0.6724 | 0.3076 | 0.1038 | 0.1045 | 0.4493 |
| Air Transport | 38 | 2.6310 | 0.1260 | 0.2923 | 0.8411 | 0.4448 | −0.1196 | 0.1230 | 0.5015 |
| Apparel | 46 | 1.2618 | 0.1510 | 0.2025 | 0.6481 | 0.3220 | 0.2240 | 0.1324 | 0.5450 |
| Auto & Truck | 20 | 0.8919 | 0.0896 | 0.0857 | 0.5951 | 0.5437 | 0.2834 | 0.1505 | 0.3979 |
| Auto Parts (OEM) | 31 | 1.4826 | 0.1628 | 0.1684 | 0.5914 | 0.3906 | 0.0665 | 0.1132 | 0.4630 |
| Auto Parts (Replacement) | 28 | 1.1664 | 0.1247 | 0.2390 | 0.3879 | 0.5460 | 0.1712 | 0.1179 | 0.4963 |
| Bank | 178 | NA | 0.2174 | 0.0 | 0.7006 | 0.3313 | NA | NA | 0.2881 |
| Bank (Canadian) | 7 | NA | 0.3407 | 0.0 | 0.9853 | 0.2339 | NA | NA | 0.2703 |
| Bank (Foreign) | 2 | NA | 0.4181 | 0.0 | 1.3285 | 0.1664 | NA | NA | 0.3324 |
| Bank (Midwest) | 34 | NA | 0.2026 | 0.0 | 0.7078 | 0.3432 | NA | NA | 0.2716 |
| Beverage (Alcoholic) | 22 | 0.9800 | 0.0852 | 0.0101 | 0.5322 | 0.2090 | 0.0484 | 0.1644 | 0.3706 |
| Beverage (Soft Drink) | 15 | 1.1083 | 0.1754 | 0.0220 | 0.6974 | 0.1169 | 0.0034 | 0.2000 | 0.3811 |
| Building Materials | 42 | 1.7240 | 0.1796 | 0.1860 | 0.6614 | 0.3261 | 0.0805 | 0.1202 | 0.4009 |
| Cable TV | 21 | 1.0364 | 0.0474 | −0.2825 | 1.0054 | 0.3164 | −0.3063 | 0.2456 | 0.7194 |
| Canadian Energy | 16 | 2.1203 | 0.0920 | 0.2680 | 0.5776 | 0.3410 | 0.0259 | 0.2548 | 0.3310 |
| Cement & Aggregates | 13 | 2.0122 | 0.1798 | 0.2494 | 0.6766 | 0.2010 | 0.1275 | 0.2414 | 0.3650 |
| Chemical (Basic) | 14 | 1.1947 | 0.1366 | 0.0707 | 0.7438 | 0.2566 | 0.1607 | 0.1917 | 0.4282 |
| Chemical (Diversified) | 34 | 1.1294 | 0.1533 | 0.0339 | 0.6757 | 0.2146 | 0.1542 | 0.1837 | 0.3493 |
| Chemical (Specialty) | 83 | 1.1251 | 0.1320 | 0.0738 | 0.6170 | 0.2947 | 0.1542 | 0.1620 | 0.4528 |
| Computer & Peripherals | 155 | 0.9470 | 0.1349 | 0.0024 | 1.1185 | 0.0291 | 0.0659 | 0.1224 | 0.7796 |
| Computer Software & Svcs | 418 | 0.9033 | 0.1871 | −0.0274 | 1.0812 | 0.0207 | −0.0277 | 0.2478 | 0.7816 |
| Copper | 2 | 3.0254 | 0.0741 | 0.7502 | 0.4994 | 0.5299 | 0.2499 | 0.1517 | 0.3564 |
| Diversified Co. | 93 | 1.2380 | 0.1261 | 0.0611 | 0.7234 | 0.2298 | 0.0840 | 0.1409 | 0.4251 |
| Drug | 272 | 1.4587 | 0.2381 | 0.1070 | 0.8751 | 0.0316 | 0.0802 | 0.2869 | 0.8089 |
| Drugstore | 10 | 2.4897 | 0.1422 | 0.3847 | 0.8307 | 0.1303 | 0.0941 | 0.0708 | 0.4062 |
| Educational Services | 29 | 1.2154 | 0.1186 | 0.0595 | 0.8585 | 0.0488 | 0.0362 | 0.1651 | 0.5615 |
| Electric Util. (Central) | 34 | 1.4780 | 0.1075 | 0.1328 | 0.3144 | 0.5344 | 0.0579 | 0.2332 | 0.2355 |
| Electric Utility (East) | 36 | 1.1538 | 0.1135 | 0.0437 | 0.3494 | 0.4663 | 0.0329 | 0.2861 | 0.2283 |
| Electric Utility (West) | 17 | 1.1485 | 0.1190 | 0.0376 | 0.3284 | 0.5066 | −0.0258 | 0.2232 | 0.2554 |
| Electrical Equipment | 87 | 1.0396 | 0.1667 | 0.0246 | 0.8474 | 0.0311 | 0.0394 | 0.1707 | 0.6461 |
| Electronics | 142 | 1.1528 | 0.0794 | 0.1027 | 0.9577 | 0.0582 | 0.1799 | 0.0931 | 0.6492 |
| Entertainment | 91 | 0.8649 | 0.0663 | −0.0024 | 0.7928 | 0.1793 | 0.0708 | 0.2217 | 0.4822 |
| Environmental | 55 | 0.9851 | 0.1136 | 0.0464 | 0.3961 | 0.5594 | 0.1314 | 0.2560 | 0.6488 |
| Financial Svcs. (Div.) | 185 | 1.5085 | 0.1308 | 0.2389 | 0.8147 | 0.3138 | 1.3206 | 0.9434 | 0.4160 |
| Food Processing | 94 | 1.1420 | 0.1432 | 0.0279 | 0.6708 | 0.2375 | 0.0163 | 0.1276 | 0.3772 |
| Food Wholesalers | 23 | 2.0642 | 0.1080 | 0.2304 | 0.5823 | 0.2651 | 0.0156 | 0.0440 | 0.3652 |
| Foreign Electron/Entertn | 13 | 1.0668 | 0.0871 | 0.0682 | 0.9007 | 0.1618 | 0.1439 | 0.0988 | 0.3548 |
| Foreign Telecom. | 16 | 0.8215 | 0.2005 | −0.0349 | 1.0589 | 0.0597 | 0.0742 | 0.3284 | 0.3947 |
| Furn./Home Furnishings | 35 | 1.5176 | 0.1814 | 0.2383 | 0.7306 | 0.2090 | 0.1524 | 0.1337 | 0.3856 |
| Gold/Silver Mining | 31 | 1.2241 | 0.0721 | 0.0555 | 0.6275 | 0.1277 | 0.0694 | 0.3333 | 0.5931 |
| Grocery | 27 | 1.7561 | 0.1425 | 0.1822 | 0.5781 | 0.2848 | 0.0104 | 0.0669 | 0.3912 |
| Healthcare Info Systems | 32 | 1.0073 | 0.1066 | 0.0564 | 0.8368 | 0.1336 | 0.0608 | 0.1606 | 1.1107 |
| Home Appliance | 12 | 1.0527 | 0.2395 | 0.0847 | 0.8043 | 0.2655 | 0.1011 | 0.1325 | 0.4076 |
| Homebuilding | 58 | 2.5324 | 0.0943 | 0.5747 | 0.5038 | 0.5298 | 0.3604 | 0.1242 | 0.4168 |
| Hotel/Gaming | 54 | 2.1577 | 0.0822 | 0.2072 | 0.5515 | 0.5012 | −0.0244 | 0.2475 | 0.4995 |
| Household Products | 30 | 1.0980 | 0.2258 | 0.0665 | 0.7098 | 0.1368 | 0.0668 | 0.2038 | 0.4069 |
| Industrial Services | 187 | 1.0430 | 0.1180 | 0.1617 | 0.8207 | 0.1734 | 0.0903 | 0.1003 | 0.5002 |
| Insurance (Life) | 34 | NA | 0.2960 | 0.0393 | 0.8675 | 0.1830 | NA | NA | 0.3761 |
| Insurance (Prop/Casualty | 59 | 494.0556 | 0.0001 | 70.0072 | 0.8229 | 0.0765 | −2.0353 | 0.3843 | 0.3406 |
| Internet | 304 | 1.6076 | 0.0188 | −0.9339 | 2.1151 | 0.0123 | −0.2100 | 0.0836 | 1.2631 |
| Investment Co. | 26 | 3.2332 | 0.0970 | 0.6180 | 0.5672 | 0.0271 | 0.1823 | 0.3401 | 0.1731 |
| Investment Co. (Foreign) | 20 | 0.4140 | 0.0621 | −0.1867 | 1.1514 | 0.0313 | −0.0535 | 0.5509 | 0.3316 |
| Machinery | 126 | 1.1936 | 0.1149 | 0.0893 | 0.6237 | 0.3057 | 0.2132 | 0.1247 | 0.4263 |
| Manuf. Housing/Rec Veh | 21 | 1.4869 | 0.1272 | 0.2068 | 0.6870 | 0.3327 | 0.1522 | 0.0810 | 0.4173 |
| Maritime | 16 | 1.6749 | 0.0816 | 0.2326 | 0.4185 | 0.5765 | 0.0698 | 0.1803 | 0.3971 |
| Medical Services | 163 | 1.0858 | 0.1312 | 0.0924 | 0.7928 | 0.2567 | 0.0506 | 0.1161 | 0.6474 |
| Medical Supplies | 194 | 1.1458 | 0.1871 | 0.1719 | 0.7997 | 0.0756 | 0.1335 | 0.1418 | 0.6358 |
| Metal Fabricating | 42 | 1.2529 | 0.1504 | 0.1200 | 0.7361 | 0.1871 | 0.1740 | 0.1421 | 0.4408 |
| Metals & Mining (Div.) | 35 | 1.3353 | 0.1089 | 0.1354 | 0.7142 | 0.2819 | 0.1596 | 0.1607 | 0.4865 |
| Natural Gas (Distrib.) | 43 | 1.8413 | 0.1125 | 0.2140 | 0.3960 | 0.4501 | 0.0447 | 0.2203 | 0.2423 |
| Natural Gas (Diversified | 37 | 2.2613 | 0.1032 | 0.3836 | 0.5713 | 0.2840 | 0.0123 | 0.1398 | 0.3880 |
| Newspaper | 20 | 0.8571 | 0.1253 | −0.0272 | 0.7517 | 0.1654 | −0.0281 | 0.2389 | 0.3324 |
| Office Equip & Supplies | 31 | 0.9998 | 0.1262 | 0.0498 | 0.6862 | 0.3352 | 0.1964 | 0.1246 | 0.4471 |
| Oilfield Services/Equip. | 72 | 1.6698 | 0.0667 | 0.0957 | 0.9809 | 0.1458 | 0.1824 | 0.1663 | 0.5566 |
| Packaging & Container | 36 | 0.9231 | 0.1141 | 0.0264 | 0.4721 | 0.5240 | 0.1091 | 0.1641 | 0.3783 |
| Paper & Forest Products | 55 | 0.8865 | 0.1105 | 0.0231 | 0.5796 | 0.3961 | 0.1146 | 0.1564 | 0.3552 |
| Petroleum (Integrated) | 43 | 1.3314 | 0.1675 | 0.0838 | 0.7151 | 0.1105 | 0.0064 | 0.1580 | 0.3330 |
| Petroleum (Producing) | 96 | 1.6100 | 0.1156 | 0.2267 | 0.5985 | 0.2791 | −0.0028 | 0.3727 | 0.5829 |
| Precision Instrument | 89 | 1.0999 | 0.1455 | 0.0363 | 0.8584 | 0.0679 | 0.1578 | 0.1702 | 0.6218 |
| Publishing | 49 | 1.1889 | 0.1936 | 0.0397 | 0.7461 | 0.1997 | −0.0089 | 0.1980 | 0.5112 |
| R.E.I.T. | 155 | 3.9517 | 0.0660 | 0.3516 | 0.6550 | 0.0889 | −0.2388 | 0.5904 | 0.2425 |
| Railroad | 16 | 1.9534 | 0.1100 | 0.1734 | 0.5802 | 0.3987 | −0.0704 | 0.2560 | 0.3814 |
| Recreation | 87 | 1.7111 | 0.1041 | 0.1795 | 0.7352 | 0.2021 | 0.0550 | 0.1651 | 0.6211 |
| Restaurant | 93 | 1.8460 | 0.1739 | 0.1421 | 0.6813 | 0.1836 | −0.0472 | 0.1647 | 0.4504 |
| Retail (Special Lines) | 205 | 1.6103 | 0.1694 | 0.1787 | 1.1075 | 0.1266 | 0.0871 | 0.0932 | 0.6270 |
| Retail Building Supply | 12 | 4.6371 | 0.1782 | 0.3803 | 0.8409 | 0.0263 | 0.0814 | 0.1000 | 0.3998 |
| Retail Store | 31 | 1.8930 | 0.1325 | 0.2524 | 0.9633 | 0.1668 | 0.1103 | 0.0791 | 0.4119 |
| Securities Brokerage | 32 | 1.2502 | 0.1488 | 0.5137 | 0.8226 | 0.5350 | 1.6489 | 0.5747 | 0.5478 |
| Semiconductor | 99 | 1.0919 | 0.1809 | 0.0353 | 1.3237 | 0.0177 | 0.0704 | 0.2607 | 0.7617 |
| Semiconductor Cap Equip | 7 | 0.9749 | 0.1692 | 0.0157 | 1.9141 | 0.0056 | 0.1585 | 0.2399 | 0.6802 |
| Shoe | 26 | 1.5594 | 0.1449 | 0.2742 | 0.8920 | 0.1418 | 0.2209 | 0.1034 | 0.5233 |
| Steel (General) | 30 | 1.7073 | 0.1034 | 0.1703 | 0.5953 | 0.3905 | 0.1700 | 0.1076 | 0.4413 |
| Steel (Integrated) | 19 | 1.4833 | 0.1049 | 0.1936 | 0.6666 | 0.4776 | 0.1397 | 0.1258 | 0.4076 |
| Telecom. Equipment | 116 | 1.5732 | 0.1382 | 0.2525 | 1.0904 | 0.0364 | 0.2518 | 0.1732 | 0.8615 |
| Telecom. Services | 175 | 1.7278 | 0.1213 | 0.1762 | 1.0790 | 0.1734 | −0.0486 | 0.3429 | 0.6736 |
| Textile | 27 | 1.3670 | 0.0986 | 0.1684 | 0.3305 | 0.6859 | 0.2255 | 0.1164 | 0.4808 |
| Thrift | 133 | NA | 0.0926 | 0.0 | 0.2592 | 0.7673 | NA | NA | 0.3101 |
| Tire & Rubber | 10 | 1.5236 | 0.1107 | 0.1562 | 0.6326 | 0.4146 | 0.1661 | 0.1010 | 0.4361 |
| Tobacco | 12 | 0.7755 | 0.2607 | −0.0192 | 0.5597 | 0.2340 | 0.0158 | 0.1582 | 0.4165 |
| Toiletries/Cosmetics | 20 | 1.6622 | 0.2166 | 0.1040 | 0.8607 | 0.1361 | 0.1495 | 0.1843 | 0.4891 |
| Trucking/Transp. Leasing | 51 | 1.9004 | 0.1618 | 0.3556 | 0.5077 | 0.5892 | 0.2374 | 0.1940 | 0.4295 |
| Utility (Foreign) | 2 | 2.1558 | 0.1253 | 0.5011 | 1.0282 | 0.3165 | −0.0791 | 0.4490 | 0.3797 |
| Water Utility | 15 | 2.5410 | 0.0674 | 0.2089 | 0.4188 | 0.4555 | 0.0176 | 0.3950 | 0.2882 |

**Outputs (workbook level):**
- Normalized EBIT: Normalizer D14 = 1788.668.
- R&D adjustments: research asset 3035.4; amortization 484.6; EBIT adj +1109.4; tax effect 388.29.
- Lease adjustments: lease debt 838.944; lease-asset depreciation 104.868; EBIT adj +49.078.
- Synthetic rating AAA; spread 0.0075; cost of debt 0.0585.

**Worked example (chain, current sheet values):** The firm's 5-year history (revenues 2032→3248, EBIT 186→383) gives an aggregate margin 2000/13590 = 14.7167%. Approach 3 applies that margin to current revenues 12154 → normalized EBIT 1788.67. With interest proxy 121 (the operating-lease expense; balance-sheet debt is 0), coverage = 1788.67/121 = 14.78 → large-firm table → AAA → spread 0.75% → kd = 5.1% + 0.75% = 5.85%. That kd discounts lease commitments (156, 143, 122, 109, 97, then 448 spread as 149.33/yr for 3 years) to a lease debt of 838.94, adding 49.08 of imputed interest to EBIT and 838.94 to debt. Separately, capitalizing R&D (current 1594; prior years 1026, 698, 399, 211, 89; 5-yr amortization) creates a 3035.4 research asset and raises EBIT by 1109.4.

**Reimplementation notes:**
- Module 1 `normalize_ebit(approach, avg_ebit, avg_roc, sector_margin, current_revenues, bv_debt, bv_equity) -> float`: branch on approach ∈ {1,2,3} as above. Approach-2 capital base = current book debt + equity (inferred; unverified branch — flag in port). Edge case: all three can still yield ≤ 0 EBIT for deeply troubled firms; the master sheet then directs users to a different model (highgrowth.xls).
- Module 2 `capitalize_rnd(N: int (1..10), current_rnd: float, past_rnd: list[float] length N ordered year −1..−N)`: returns research_asset = Σ_{k=0..N} rnd_{−k}·(N−k)/N, amortization = Σ_{k=1..N} rnd_{−k}/N, ebit_adjustment = current_rnd − amortization (may be negative for shrinking R&D), tax_effect = tax_rate·ebit_adjustment. If fewer than N past years available, missing years are 0 (sheet behavior).
- Module 3 `capitalize_leases(current_lease_exp, commitments_1_5: list[5], beyond: float, kd: float)`. Steps:
  - `n_beyond = int(beyond / mean(commitments_1_5))` — truncate, not round. Guard mean = 0 and n_beyond = 0. If 0, treat the lump as a single year-6 payment or skip it.
  - `annuity = beyond / n_beyond`
  - `lease_debt = Σ commitments_t/(1+kd)^t + annuity·(1−(1+kd)^−n_beyond)/kd/(1+kd)^5`
  - `depreciation = lease_debt/(5+n_beyond)`
  - `ebit_adjustment = lease_debt·kd`; `debt_adjustment = lease_debt`
- Module 4 `synthetic_rating(firm_type ∈ {1,2,3}, ebit, interest_expense, rf)`. coverage = ebit/interest. Handle interest ≤ 0: the sheet convention substitutes a debt-like charge such as lease expense; with truly zero interest, return AAA / +∞ coverage. Table lookup uses a strict `>` lower bound and a `≤` upper bound (thresholds like 0.199999 implement "< 0.2"). cost_of_debt = rf + spread. Ship all three tables exactly as above.
- Circularity: rating → kd → lease debt → (interest / restated EBIT) → rating. Iterate to a fixed point (converges fast; the sheet uses Excel iteration).
- Industry-averages table: ship as a keyed dict; parse "NA" as None. Watch the truncated sheet labels ("Insurance (Prop/Casualty", "Natural Gas (Diversified") and the Prop/Casualty row's degenerate values (CapEx/Dep 494.06, reinvestment 70.01) — data artifacts, keep verbatim but do not "fix".

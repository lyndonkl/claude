# Focussed Valuation Model Spreadsheets — FCFF family (Damodaran, 2020 archive)

Source directory: `/Users/kushaldsouza/Downloads/2020/Spreadsheets/Focussed Valuation Model Spreadsheet/`

All four files are legacy `.xls`; dumps expose computed VALUES only, no live formulas. Every
formula below was reconstructed from labels, layout, and by numerically reproducing the values
in the sheet (verified to the precision shown) — treat all formulas as "(inferred)" unless noted,
but they are numerically confirmed against the sheet contents.

Common notation: `t` = tax rate, `g` = growth rate, `rf` = riskfree rate, `ERP` = equity risk
premium, `WACC` = cost of capital, `EBIT(1-t)` = after-tax operating income, `ChgWC` = change in
non-cash working capital, `FCFF = EBIT(1-t) + Depreciation - CapEx - ChgWC`.

---

### fcffst.xls

Sheets: `Sheet1` (empty), `NewFCFFStableGrowth` (the model).

**Purpose:** Values a firm already in steady state — a single-stage (stable-growth) FCFF
perpetuity model. Used when a firm grows at or below the nominal growth rate of the economy
forever, with a known, constant leverage. This is the Gordon-growth model applied to FCFF and
discounted at WACC; it returns firm (enterprise) value, not equity value per share.

**Inputs** (all on `NewFCFFStableGrowth`):

| Label | Cell | Example value |
|---|---|---|
| Current EBIT (currency) | D21 | 1535 |
| Current tax rate | D22 | 0.36 |
| Capital expenditures (currency) | D24 | 550 |
| Depreciation (currency) | D25 | 400 |
| Change in working capital (currency; "If negative, enter zero.") | D26 | 160 |
| Change the CapEx/Depreciation ratio? (Yes/No) | F27 | "Yes" |
| If so, CapEx as a percent of depreciation | F28 | 1.25 |
| Debt ratio (D/(D+E), in percent) | D29 | 0.2997 |
| Directly entering cost of equity? (Yes/No) | F31 | "No" |
| If yes, cost of equity | D32 | (blank) |
| Beta of the stock | D34 | 1.1 |
| Riskfree rate | D35 | 0.07 |
| Risk premium | D36 | 0.055 |
| Cost of debt (pre-tax) | D38 | 0.085 |
| Expected growth rate forever | D40 | 0.05 |

Sheet note at F40:F43: the stable growth rate "cannot be significantly higher than the nominal
growth rate in the economy in which the firm operates. It can be lower."

There is a "Warnings:" block at B45:C47, blank in this workbook (its trigger conditions are not
recoverable from the value dump).

**Logic** (all inferred, numerically verified):

1. Effective CapEx:
   - If F27 = "Yes": `CapEx_used = F28 × Depreciation` (here 1.25 × 400 = 500).
   - If "No": `CapEx_used = D24` as entered.
2. `EBIT(1-t) = D21 × (1 − D22)` → F51 = 1535 × 0.64 = 982.4
3. `NetCapEx = CapEx_used − Depreciation` → F52 = 500 − 400 = 100
4. `ChgWC = D26` (user told to floor at zero) → F53 = 160
5. `FCFF = EBIT(1-t) − NetCapEx − ChgWC` → F54 = 722.4
6. Cost of equity D56: if F31 = "Yes" use D32; else CAPM `ke = rf + β×ERP` = 0.07 + 1.1×0.055 = 0.1305
7. After-tax cost of debt D57: `kd_AT = D38 × (1 − t)` = 0.085 × 0.64 = 0.0544
8. Cost of capital D58: `WACC = ke×(1 − DebtRatio) + kd_AT×DebtRatio`
   = 0.1305×0.7003 + 0.0544×0.2997 = 0.10769283
9. Value of firm F61: `V = FCFF × (1+g) / (WACC − g)` = 722.4×1.05 / (0.10769283 − 0.05)
   = 13,147.56

**Reference data:** none (no lookup tables). The only table is the output sensitivity table below.

**Outputs:**

| Cell | Meaning | Value |
|---|---|---|
| F51 | EBIT(1−t) | 982.4 |
| F52 | CapEx − Depreciation | 100 |
| F53 | Change in working capital | 160 |
| F54 | Base-year FCFF | 722.4 |
| D56 | Cost of equity | 0.1305 |
| D57 | After-tax cost of debt | 0.0544 |
| D58 | Cost of capital (WACC) | 0.10769283 |
| F61 | **Value of firm** (enterprise value) | 13,147.56 |

Sensitivity table (B64:C71), `Value(g) = FCFF×(1+g)/(WACC−g)` with WACC held fixed (verbatim values):

| Growth rate | Value |
|---|---|
| 0.07 | 20,507.03 |
| 0.06 | 16,055.75 |
| 0.05 | 13,147.56 |
| 0.04 | 11,098.61 |
| 0.03 | 9,577.10 |
| 0.02 | 8,402.60 |
| 0.01 | 7,468.55 |

**Worked example:** EBIT 1535, t 36% → 982.4 after-tax. CapEx overridden to 1.25×Depr =
500, so net CapEx = 100. FCFF = 982.4 − 100 − 160 = 722.4. ke = 0.07 + 1.1×0.055 = 13.05%;
kd_AT = 5.44%; at 29.97% debt, WACC = 10.7693%. Firm value = 722.4×1.05/0.057693 = 13,147.56.

**Reimplementation:**
- Inputs: `ebit: float`, `tax_rate: float (0–1)`, `capex: float`, `depreciation: float`,
  `chg_wc: float (>=0)`, `override_capex_ratio: bool`, `capex_to_depreciation: float`,
  `debt_ratio: float (0–1)`, `cost_of_equity: Optional[float]` (else `beta, riskfree, erp`),
  `pretax_cost_of_debt: float`, `stable_growth: float`. All rates as decimals; currency amounts
  in same units.
- Outputs: `fcff`, `cost_of_equity`, `after_tax_cost_of_debt`, `wacc`, `firm_value`, plus an
  optional growth-sensitivity vector.
- Branches: (a) CapEx override on/off; (b) direct ke vs CAPM.
- Edge cases: require `stable_growth < wacc` (else division by zero / negative value —
  the sheet has no guard); clamp `chg_wc` at 0 per the sheet's instruction; negative EBIT gives
  a negative valuation (the model is not intended for that — warn); it values the FIRM only,
  no cash/debt/share-count bridge to equity per share.

---

### fcff2st.xls

Sheets: `NewFCFF2Stage` (the model; only sheet).

**Purpose:** Two-stage FCFF discount model: an initial constant-parameter high-growth period
(1–10 years) followed by stable growth forever. Growth in the high-growth period can be a
weighted blend of historical, analyst (outside), and fundamental (ROC × reinvestment rate)
growth. Produces firm value, then bridges to equity value per share (adds cash, subtracts
debt and the value of employee equity options). The header notes "For a richer version of this
model, try the fcffginzu.xls spreadsheet."

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Current EBIT | D20 | 5186 |
| Current interest expense | D21 | 118 (not used in any verified output) |
| Current capital spending | D22 | 2152 |
| Current depreciation & amortization | D23 | 1228 |
| Tax rate on income | D24 | 0.2849 |
| Current revenues | D25 | 16701 |
| Current non-cash working capital | D26 | 3755 |
| Change in working capital (last year) | D27 | 499 |
| Cash and marketable securities | D28 | 500 |
| Value of equity options issued by firm | D29 | 1500 |
| Book value of debt: current / last year | D30 / E30 | 1479 / 1315 |
| Book value of equity: current / last year | D31 / E31 | 12941 / 12156 |
| Is the firm publicly traded? (Yes/No) | F34 | "Yes" |
| If yes: market price per share | F36 | 125.5 |
| If yes: number of shares outstanding | F37 | 993.57 |
| If yes: market value of debt | F38 | 1822 |
| If not traded: use book value debt ratio? (Yes/No) | F40 | "No" |
| If no: debt-to-capital ratio to use | F41 | (blank) |
| Length of extraordinary growth period (years) | E43 | 5 |
| Change debt ratio in stable period? (Yes/No) | F45 | "No" |
| If yes: stable-period debt ratio | F46 | (blank) |
| Enter cost of equity directly? (Yes/No) | E49 | "No" |
| If yes: cost of equity | F50 | (blank) |
| Beta of the stock | D52 | 0.8 |
| Riskfree rate | D53 | 0.053 |
| Risk premium | D54 | 0.055 |
| Cost of debt (pre-tax) | E56 | 0.055 |
| Use historical growth rate? (Yes/No) | E59 | "No" |
| EBIT from five years ago (for historical growth) | E60 | 800 |
| Have an outside estimate of growth? (Yes/No) | E62 | "Yes" |
| If yes: estimated growth | E63 | 0.125 |
| Calculate growth from fundamentals? (Yes/No) | F65 | "Yes" |
| (computed) ROC | C67 | 0.275296 (computed, see logic) |
| (computed) Reinvestment rate | C68 | 0.383712 (computed, see logic) |
| Override ROC/reinv. rate for high growth? (Yes/No) | F69 | "No" |
| If yes: ROC / Reinv. rate overrides | C71 / C72 | 0.10 / 1.00 |
| Weight on historical growth | E75 | 0 |
| Weight on outside growth | E76 | 0 |
| Weight on fundamental growth | E77 | 1.0 |
| Stable-period growth rate | E79 | 0.06 |
| Beta changes in stable period? (Yes/No) | E82 | "No" |
| If yes: stable-period beta | E83 | 1.0 |
| Cost of debt changes in stable period? (Yes/No) | E85 | "No" |
| If yes: new cost of debt | F86 | (blank) |
| CapEx/Depr/WC grow at same rate as earnings? (Yes/No) | F89 | "Yes" |
| If not: high-growth rates for CapEx / Depr / Revenues | C92 / D92 / E92 | 0.06 / 0.06 / 0.06 |
| Stable-growth rate for revenues (CapEx/Depr say "Do not enter") | E93 | 0.06 |
| Keep current fraction of working capital to revenues? (Yes/No) | F95 | "Yes" |
| If no: WC as percent of revenues | F96 | (blank) |
| Stable period: CapEx offset by depreciation? (Yes/No) | F99 | "No" |
| Stable period: compute reinvestment from fundamentals? (Yes/No) | F100 | "Yes" |
| Return on capital in perpetuity | F101 | 0.12 |
| If not fundamentals: CapEx as % of depreciation in stable period | F102 | 1.2 |

**Logic** (inferred; every number verified against the sheet):

*Cost of capital (high-growth phase):*
1. ke (D106): direct entry if E49="Yes", else CAPM: `0.053 + 0.8×0.055 = 0.097`.
2. Weights: if publicly traded, `MV_equity = price × shares = 125.5×993.57 = 124,693.035`,
   `MV_debt = F38 = 1822`. `E/(D+E)` (D107) = 0.98559855; `D/(D+E)` (D109) = 0.01440145.
   If not traded: book debt ratio (from D30, D31) if F40="Yes", else the entered ratio F41.
3. kd_AT (D108) = `0.055 × (1 − 0.2849) = 0.0393305`.
4. WACC (D110) = `0.097×0.98559855 + 0.0393305×0.01440145 = 0.09616948`.

*Base-year FCFF:*
5. `EBIT(1−t)` (E113) = 5186×0.7151 = 3708.5086
6. `CapEx − Depr` (E114) = 2152 − 1228 = 924
7. `ChgWC` (E115) = 499
8. `Current FCFF` (E116) = 3708.5086 − 924 − 499 = 2285.5086

*Growth-rate estimation (high-growth phase):*
9. Historical growth (D120) = `(EBIT_now / EBIT_5yrs_ago)^(1/5) − 1`
   = (5186/800)^0.2 − 1 = 0.45327735 (computed even though E59="No"; the weight controls use).
10. Outside estimate (D121) = E63 = 0.125.
11. Fundamental growth: `ROC = EBIT(1−t) / (BV_debt_lastyr + BV_equity_lastyr)`
    = 3708.5086/(1315+12156) = 3708.5086/13471 = 0.27529572 (C67; beginning-of-year book
    capital, no cash netting). `ReinvRate = (CapEx − Depr + ChgWC)/EBIT(1−t)`
    = (924+499)/3708.5086 = 0.38371220 (C68).
    If F69="Yes", replace both with C71/C72. `g_fund = ROC × ReinvRate` (D122)
    = 0.27529572×0.38371220 = 0.10563433.
12. Weighted average g (D123) = `Σ weight_i × g_i` = 0×0.4533 + 0×0.125 + 1×0.10563433
    = 0.10563433.

*Growth rates for CapEx/Depreciation/Revenues (rows 127–129):* if F89="Yes" all three equal
the weighted-average earnings growth in the high-growth phase (0.10563433 here); otherwise use
the user-entered rates C92:E92. Stable-phase revenue growth = E93 input row, but effectively
the stable growth E79 (both 0.06 here). Working capital % of revenues (E131): if F95="Yes",
`= D26/D25` = 3755/16701 = 0.22483684; else F96.

*High-growth phase projections, years i = 1..N (N = E43 = 5; grid supports up to 10):*
13. `EBIT(1−t)_i = EBIT(1−t)_0 × (1+g)^i` (row 134). Year 1: 3708.5086×1.10563433 = 4100.2544.
14. `(CapEx − Depr)_i = 924 × (1+g_capex)^i` (row 135; grown as a net number). Year 1: 1021.6061.
15. `Revenues_i = 16701 × (1+g_rev)^i`; `ChgWC_i = WC% × (Rev_i − Rev_{i−1})` (row 136).
    Year 1: 0.22483684 × 16701×0.10563433 = 396.6569.
16. `FCFF_i` (row 137) = 13 − 14 − 15. Year 1: 2681.9914.
17. `PV_i = FCFF_i / (1+WACC)^i` (row 138). Year 1: 2681.9914/1.09616948 = 2446.6941.

*Stable phase / terminal value:*
18. Stable-phase ke (E142): new beta if E82="Yes", else same as high-growth ke = 0.097.
    Stable kd_AT (E144): new cost of debt if E85="Yes", else same = 0.0393305. Stable weights
    (E143/E145): F46 if F45="Yes", else same as high-growth = 0.98559855/0.01440145.
    Stable WACC (E146) = 0.09616948.
19. Terminal-year FCFF components (column N of rows 134–137):
    `EBIT(1−t)_T = EBIT(1−t)_N × (1+g_stable)` = 6127.1266×1.06 = 6494.7542.
    Reinvestment: since F100="Yes" (fundamentals): `ReinvRate_stable = g_stable / ROC_perpetuity`
    = 0.06/0.12 = 0.5, so total reinvestment = 0.5×6494.7542 = 3247.3771. The sheet splits it:
    `ChgWC_T = WC% × Rev_N × g_stable` = 0.22483684×27,595.5×0.06 = 372.2363, and
    `(CapEx − Depr)_T = total reinvestment − ChgWC_T` = 2875.1408.
    (If F100="No": if F99="Yes", CapEx = Depreciation so net CapEx = 0; else
    CapEx = F102 × Depreciation. — inferred from labels, not exercised in this workbook.)
    `FCFF_T` (E141) = 6494.7542 − 3247.3771 = 3247.3771.
20. `TerminalValue = FCFF_T / (WACC_stable − g_stable)` (E147)
    = 3247.3771/0.03616948 = 89,782.256.

*Valuation bridge:*
21. `PV of high-growth FCFF` (F149) = Σ PV_i = 12,446.562.
22. `PV of terminal value` (F150) = 89,782.256/1.09616948^5 = 56,728.591.
23. `Firm value` (F151) = 12,446.562 + 56,728.591 = 69,175.152.
24. `MV equity` (F154) = Firm + Cash − MV debt = 69,175.152 + 500 − 1822 = 67,853.152.
25. `Value per share` (F156) = (MV equity − option value)/shares
    = (67,853.152 − 1500)/993.57 = 66.7826.

**Reference data:** none (no lookup tables).

**Outputs:**

| Cell | Meaning | Value |
|---|---|---|
| D106–D110 | ke, E/(D+E), kd_AT, D/(D+E), WACC | 0.097, 0.98560, 0.03933, 0.01440, 0.09617 |
| E113–E116 | Base EBIT(1−t), net CapEx, ChgWC, current FCFF | 3708.51, 924, 499, 2285.51 |
| D120–D123 | Historical / outside / fundamental / weighted growth | 0.45328, 0.125, 0.10563, 0.10563 |
| D134:H138, N134:N137 | Year-by-year FCFF table + terminal year | see worked example |
| E140–E147 | Stable g, FCFF, ke, weights, kd_AT, WACC, terminal value | 0.06 … 89,782.26 |
| F149 | PV of high-growth FCFF | 12,446.56 |
| F150 | PV of terminal value | 56,728.59 |
| F151 | **Value of the firm** | 69,175.15 |
| F154 | Market value of equity | 67,853.15 |
| F156 | **Value per share** | 66.78 |

**Worked example** (values in the sheet; 5-year high growth at g = 10.5634%):

| Year | EBIT(1−t) | −(CapEx−Depr) | −ChgWC | FCFF | PV @9.617% |
|---|---|---|---|---|---|
| 1 | 4100.25 | 1021.61 | 396.66 | 2681.99 | 2446.69 |
| 2 | 4533.38 | 1129.52 | 438.56 | 2965.30 | 2467.82 |
| 3 | 5012.26 | 1248.84 | 484.88 | 3278.54 | 2489.13 |
| 4 | 5541.73 | 1380.76 | 536.10 | 3624.87 | 2510.62 |
| 5 | 6127.13 | 1526.62 | 592.74 | 4007.78 | 2532.30 |
| Terminal | 6494.75 | 2875.14 | 372.24 | 3247.38 | — |

TV = 3247.38/(0.09617−0.06) = 89,782.26; PV(TV) = 56,728.59; firm = 69,175.15;
+cash 500 − debt 1822 = equity 67,853.15; − options 1500; ÷ 993.57 shares = **66.78/share**.

**Reimplementation:**
- Inputs: base financials (`ebit, interest_expense, capex, depreciation, tax_rate, revenues,
  noncash_wc, chg_wc, cash, option_value, bv_debt_now, bv_debt_prior, bv_equity_now,
  bv_equity_prior`), market data (`is_public: bool, price, shares, mv_debt` or
  `use_book_debt_ratio: bool` / `debt_ratio: float`), `high_growth_years: int (1–10)`,
  cost-of-capital inputs (`ke_direct or beta/rf/erp`, `pretax_kd`), growth inputs
  (`ebit_5yr_ago`, `outside_growth`, `use_fundamental: bool`, optional `roc_override,
  reinv_override`, `weights: (w_hist, w_outside, w_fund)`), stable inputs (`g_stable`,
  optional `stable_beta, stable_kd, stable_debt_ratio`, `stable_reinv_from_fundamentals: bool`,
  `roc_perpetuity`, `stable_capex_offset: bool`, `stable_capex_to_depr`), projection options
  (`grow_with_earnings: bool` else per-item growth rates, `keep_wc_ratio: bool` else `wc_pct`).
- Outputs: cost-of-capital block, growth block, per-year FCFF table, terminal value, PV split,
  firm value, equity value, value per share.
- Branches: public vs private weights; direct ke vs CAPM; fundamental ROC/reinv override;
  the three-way growth weighting; stable-period overrides for beta / kd / debt ratio; terminal
  reinvestment mode (fundamentals `g/ROC` vs capex-offset vs capex-as-%-of-depreciation);
  item growth = earnings growth vs per-item.
- Edge cases:
  - ROC uses PRIOR-year book capital. Rows 30/31 hold both columns — use E30+E31, not D30+D31.
  - Negative or zero `EBIT(1−t)` breaks ROC and the reinvestment rate. Guard for it.
  - Weights should sum to 1; the sheet does not enforce this.
  - Require `g_stable < WACC_stable`.
  - `high_growth_years ≤ 10` (the projection grid's width).
  - Historical growth is undefined if `ebit_5yr_ago ≤ 0`.
  - Terminal-year ChgWC = `WC% × Rev_N × g_stable`, NOT a reinvestment-rate split of WC.
  - The interest expense input is collected but feeds no verified output cell.

---

### fcff3st.xls

Sheets: `Sheet1` (the model); `Sheet2`–`Sheet16` empty stubs.

**Purpose:** Three-stage (high growth → linear transition → stable) FCFF valuation with
year-by-year cost of capital. Five years of constant high growth, five transition years in
which revenue growth, operating margin, beta, debt ratio, and cost of debt all glide linearly
to their stable-period levels, then a growing perpetuity. Margins are driven by a target
pre-tax operating margin path (revenues × margin ⇒ EBIT), which suits firms whose margins are
converging to a target. Bridges to equity value per share (cash, debt, employee options).
The example in the sheet is a 1995-vintage high-growth firm (years labeled 1995–2004,
terminal value "in '05").

**Inputs** (Sheet1):

*Current inputs:*

| Label | Cell | Example value |
|---|---|---|
| Current revenues | D3 | 12406 |
| Current operating income (EBIT) | D4 | 855 |
| Current capital expenditures | D5 | 233 |
| Current dollar depreciation | D6 | 298 |
| Change in working capital last year | D7 | 115 |
| Value of current debt outstanding | D8 | 0 |
| Cash and marketable securities | D9 | 850 |
| Value of equity options issued by the firm | D10 | 1500 |
| Number of shares outstanding | D11 | 1500 |

*High-growth period (years 1–5):*

| Label | Cell | Example value |
|---|---|---|
| Revenue growth rate for next 5 years | E14 | 0.30 |
| (computed) current pre-tax operating margin | E15 | 0.0689183 (= D4/D3) |
| Target pre-tax operating margin in year 5 (note: "Operating Expenses include depreciation: This is equal to (1-EBIT/Sales)") | E16 | 0.30 |
| Debt ratio for financing investments (high growth) | E17 | 0.0 |
| Growth rate in CapEx & depreciation | E18 | 0.30 |
| Working capital as a percent of revenues | E19 | 0.075 |
| Tax rate on corporate income | E20 | 0.36 |
| Beta for cost of equity (high growth) | E21 | 1.25 |
| Current long-term bond rate (riskfree) | E22 | 0.065 |
| Market risk premium | E23 | 0.055 |
| Cost of borrowing (pre-tax, high growth) | E24 | 0.085 |

*Stable period (year 10 on):*

| Label | Cell | Example value |
|---|---|---|
| Stable revenue growth rate | E26 | 0.06 |
| Pre-tax operating margin in perpetuity | E27 | 0.25 |
| Compute reinvestment from fundamentals? (Yes/No) | E28 | "Yes" |
| Return on capital in perpetuity | E29 | 0.12 |
| CapEx as a percent of depreciation in stable period (used if E28="No") | E30 | 2.0 |
| Debt ratio in stable period | E31 | 0.05 |
| Interest rate on debt in stable period (pre-tax) | E32 | 0.075 |
| Beta in stable period | E33 | 1.1 |

**Logic** (inferred; verified):

*Parameter paths over 10 years (columns C..L = years 1..10; column B = base):*
1. Revenue growth (row 36): years 1–5 = E14 (0.30); years 6–10 decline linearly to E26:
   `g_i = g_high − (g_high − g_stable)×(i−5)/5` → 0.252, 0.204, 0.156, 0.108, 0.06.
   Depreciation growth (row 37) follows the identical path (base rate E18; here E18 = E14 so
   indistinguishable — most likely row 37 = E18 for years 1–5 then linear to E26).
2. Revenues (row 38): `Rev_i = Rev_{i−1}×(1+g_i)`; base 12406 → year 10: 94,272.02.
3. Operating-expense ratio "% of Revenues" (row 40, = COGS/Rev): base = `1 − EBIT/Rev`
   = 1 − 855/12406 = 0.9310817. Years 1–5: linear from base to `1 − E16` = 0.70
   (step (0.9310817−0.70)/5 = 0.0462163). Years 6–10: linear from 0.70 to `1 − E27` = 0.75
   (step 0.01): 0.71, 0.72, 0.73, 0.74, 0.75.
4. `$COGS_i` (row 41) = ratio × Rev_i. `EBIT_i` (row 42) = Rev_i − COGS_i
   (i.e., Rev × pre-tax margin; depreciation is inside COGS per the E16 note).
5. Tax rate (row 43) constant = E20. `EBIT(1−t)_i` (row 45) = EBIT_i×(1−0.36).
6. Depreciation (row 46): `Dep_i = Dep_{i−1}×(1+gdep_i)` with the row-37 path; 298 → 2264.47.
7. CapEx (row 47): years 1–5: `CapEx_i = CapEx_{i−1}×(1+E18)` (233 → 865.11 in year 5).
   Year 10 CapEx is solved so that total year-10 reinvestment matches the stable-period rule
   (see 9). Years 6–9 interpolate linearly between year-5 and year-10 CapEx.
   Step = (9406.024 − 865.113)/5 = 1708.182 → 2573.29, 4281.48, 5989.66, 7697.84, 9406.02.
8. ChgWC (row 48): `ChgWC_i = E19 × (Rev_i − Rev_{i−1})`; base-year value is the D7 input.
9. Stable-period reinvestment (year 10): since E28 = "Yes",
   `ReinvRate_stable = g_stable/ROC_perpetuity = 0.06/0.12 = 0.5`, so
   `FCFF_10 = EBIT(1−t)_10 × (1 − 0.5)` = 15,083.52×0.5 = 7541.76, and year-10 CapEx is
   back-solved: `CapEx_10 = EBIT(1−t)_10×ReinvRate + Dep_10 − ChgWC_10`
   = 7541.76 + 2264.47 − 400.21 = 9406.02. (If E28 = "No": `CapEx_10 = E30 × Dep_10` — inferred
   from labels, not exercised here.)
10. `FCFF_i` (row 49) = EBIT(1−t)_i + Dep_i − CapEx_i − ChgWC_i.

*Cost of capital by year (rows 53–58):*
11. ke (row 53): years 1–5 = `E22 + E21×E23` = 0.065 + 1.25×0.055 = 0.13375; year 10
    = `E22 + E33×E23` = 0.1255; years 6–9 linear (step 0.00165): 0.1321, 0.13045, 0.1288, 0.12715.
12. Debt ratio (row 56): years 1–5 = E17 (0); year 10 = E31 (0.05); years 6–9 linear
    (0.01, 0.02, 0.03, 0.04). Equity proportion (row 54) = 1 − debt ratio.
13. kd_AT (row 55): years 1–5 = `E24×(1−t)` = 0.0544; year 10 = `E32×(1−t)` = 0.048;
    years 6–9 linear (step 0.00128): 0.05312, 0.05184, 0.05056, 0.04928.
14. `WACC_i` (row 57) = ke_i×(1−DR_i) + kd_AT_i×DR_i. Years 1–5: 0.13375; year 6: 0.1313102;
    … year 10: 0.121625.
15. Cumulative WACC (row 58): `Cum_i = Π_{j≤i}(1+WACC_j)`. Year 1: 1.13375 … year 10: 3.3974708.

*Discounting and valuation:*
16. Terminal value (L50): `TV = FCFF_10×(1+g_stable)/(WACC_10 − g_stable)`
    = 7541.76×1.06/0.061625 ≈ 129,724.42 (sheet value; formula reproduces it to <0.001%).
17. PV (row 60): `PV_i = FCFF_i / Cum_i` for years 1–9; year 10: `PV_10 = (FCFF_10 + TV)/Cum_10`
    = (7541.76+129,724.42)/3.3974708 = 40,402.46.
18. `Value of firm` (C63) = Σ PV_1..10 = 66,666.83.
19. `Value of equity` (C66) = firm + cash − debt = 66,666.83 + 850 − 0 = 67,516.83.
20. `Value of equity per share` (C68) = (equity − options)/shares
    = (67,516.83 − 1500)/1500 = 44.011.

*Auxiliary rows 71–73 (year labels 1995–2004):*
21. `Value of firm by year` (row 72): rolls the valuation forward:
    `V_i = V_{i−1}×(1+WACC_i) − FCFF_i` (V_1 = C63 rolled? — verified: V_1996 = 66,666.83×1.13375
    − 993.76 = 74,589.76; C72 itself equals the year-1 firm value 66,666.83).
22. `$ Value of debt` (row 73) = DebtRatio_i × V_i (e.g. 2000: 0.01×101,893.25 = 1018.93).

**Reference data:** none (no lookup tables).

**Outputs:**

| Cell | Meaning | Value |
|---|---|---|
| Row 49 (C..L) | FCFF years 1–10 | 993.76 … 7541.76 |
| L50 | Terminal value at year 10 | 129,724.42 |
| Row 57 | WACC by year | 0.13375 → 0.121625 |
| Row 60 | PV by year (year 10 includes TV) | 876.53 … 40,402.46 |
| C63 | **Value of firm** | 66,666.83 |
| C66 | Value of equity | 67,516.83 |
| C68 | **Value of equity per share** | 44.011 |
| Rows 72–73 | Firm value and implied $ debt by calendar year | 66,666.83 → 122,381.53 |

**Worked example** (sheet values):

| Year | Rev growth | Revenues | COGS% | EBIT | EBIT(1−t) | +Dep | −CapEx | −ChgWC | FCFF | WACC | PV |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Base | — | 12,406 | 0.93108 | 855 | 547.2 | 298 | 233 | 115 | 497.2 | — | — |
| 1 | 0.30 | 16,127.8 | 0.88487 | 1856.87 | 1188.40 | 387.40 | 302.90 | 279.14 | 993.76 | 0.13375 | 876.53 |
| 2 | 0.30 | 20,966.1 | 0.83865 | 3382.91 | 2165.06 | 503.62 | 393.77 | 362.88 | 1912.03 | 0.13375 | 1487.51 |
| 3 | 0.30 | 27,256.0 | 0.79243 | 5657.45 | 3620.77 | 654.71 | 511.90 | 471.74 | 3291.84 | 0.13375 | 2258.84 |
| 4 | 0.30 | 35,432.8 | 0.74622 | 8992.26 | 5755.05 | 851.12 | 665.47 | 613.26 | 5327.43 | 0.13375 | 3224.40 |
| 5 | 0.30 | 46,062.6 | 0.70 | 13,818.78 | 8844.02 | 1106.45 | 865.11 | 797.24 | 8288.12 | 0.13375 | 4424.56 |
| 6 | 0.252 | 57,670.4 | 0.71 | 16,724.41 | 10,703.62 | 1385.28 | 2573.29 | 870.58 | 8645.02 | 0.131310 | 4079.42 |
| 7 | 0.204 | 69,435.1 | 0.72 | 19,441.84 | 12,442.78 | 1667.88 | 4281.48 | 882.36 | 8946.82 | 0.128878 | 3739.84 |
| 8 | 0.156 | 80,267.0 | 0.73 | 21,672.10 | 13,870.14 | 1928.07 | 5989.66 | 812.39 | 8996.16 | 0.126453 | 3338.33 |
| 9 | 0.108 | 88,935.9 | 0.74 | 23,123.33 | 14,798.93 | 2136.30 | 7697.84 | 650.16 | 8587.22 | 0.124035 | 2834.94 |
| 10 | 0.06 | 94,272.0 | 0.75 | 23,568.01 | 15,083.52 | 2264.47 | 9406.02 | 400.21 | 7541.76 | 0.121625 | 40,402.46 (incl. TV) |

TV = 7541.76×1.06/(0.121625−0.06) = 129,724.42. Firm = Σ PV = 66,666.83; + cash 850 − debt 0
= 67,516.83; − options 1500; ÷ 1500 shares = **44.01/share**.

**Reimplementation:**
- Inputs: current (`revenues, ebit, capex, depreciation, chg_wc, debt, cash, option_value,
  shares`); high-growth (`g_rev_high, target_margin_yr5, debt_ratio_high, g_capex_dep,
  wc_pct_of_rev, tax_rate, beta_high, riskfree, erp, pretax_kd_high`); stable (`g_stable,
  margin_perpetuity, reinvest_from_fundamentals: bool, roc_perpetuity, capex_to_dep_stable,
  debt_ratio_stable, pretax_kd_stable, beta_stable`). The 5+5 structure is hard-coded
  (years 1–5 constant, 6–10 linear transition).
- Outputs: 10-year projection table (revenues, margin path, EBIT, FCFF), per-year WACC and
  cumulative discount factors, terminal value, firm value, equity value, value per share,
  firm-value-by-year roll-forward.
- Branches: stable reinvestment from fundamentals (`reinv = g/ROC`, back-solve year-10 CapEx)
  vs CapEx = ratio × depreciation; that's the only Yes/No switch.
- Edge cases:
  - The margin path can pass through negative EBIT if the current margin is negative. The
    formula still works, but taxes stay at the flat rate with NO NOL tracking — negative EBIT
    gets a negative tax, i.e. a credit.
  - Require `g_stable < WACC_10`.
  - The year 6–9 CapEx interpolation depends on the back-solved year-10 CapEx. Compute year
    10 first.
  - Discounting uses cumulative products of year-specific WACCs, not a single rate.
  - Base-year (`year 0`) FCFF is displayed but never discounted or added to value.

---

### fcffgen.xls

Sheets: `The Valuation of Amazon` (the main model), `Option Valuation` (dilution-adjusted
Black–Scholes for employee options/warrants), `Sheet1` (FCFF/PV summary table mirroring the
main sheet), `What-If` (static sensitivity results).

#### Sheet "The Valuation of Amazon" — general n-stage FCFF model

**Purpose:** The most flexible of the four: an n-stage FCFF model with fully year-specific
inputs for each of up to 10 years — revenue growth, operating-expense margin, CapEx growth,
depreciation growth, and WC% of revenues. It adds net-operating-loss (NOL) carryforward tax
logic for money-losing firms, plus a beta/debt-ratio glide to stable values. Built for young
high-growth loss-making firms — the worked case is Amazon circa 1998–99 (negative EBIT,
NOL = 1500, 84/share market price). Bridges to equity per share after subtracting debt and the
dilution-adjusted value of options from the `Option Valuation` sheet.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Current EBIT | D21 | −410 |
| Current net income | D22 | −442 (not used in verified outputs) |
| Current dividends | D23 | 0 (not used in verified outputs) |
| Current interest expense | D24 | 74 (not used in verified outputs) |
| Current capital spending | D25 | 242.6667 |
| Current depreciation | D26 | 30.6667 |
| Tax rate on income (marginal) | D27 | 0.35 |
| Current revenues | D28 | 1117 |
| Current working capital | D29 | −110.5 (not used in ChgWC calc — see logic) |
| Change in working capital (last year) | D30 | −63 (not used in projections) |
| Book value of debt | D31 | 348.68 |
| Book value of equity | D32 | 138 |
| NOL carried forward | D33 | 1500 |
| Is the firm publicly traded? (Yes/No) | F36 | "Yes" |
| If yes: market price per share | F38 | 84 |
| If yes: number of shares outstanding | F39 | 340.79 |
| If yes: market value of debt | F40 | 349 |
| If not traded: use book value debt ratio? / debt ratio to use | (B42/B43) | (blank) |
| Length of extraordinary growth period (years) | E45 | 10 |
| Enter cost of equity directly? (Yes/No) | E48 | "No" |
| If yes: cost of equity | E49 | 0.1535 (present but inactive) |
| Beta of the stock | D51 | 1.6 |
| Riskfree rate | D52 | 0.065 |
| Risk premium | D53 | 0.04 |
| Cost of debt (pre-tax) | E55 | 0.08 |
| Stable-period growth rate | E72 | 0.06 |
| Operating expenses as % of revenue in stable phase | E73 | 0.90 |
| Working capital as % of revenue in stable phase | E74 | 0.03 |
| Beta changes in stable period? / stable beta | E76 / E77 | "Yes" / 1.0 |
| Change debt ratio in stable period? / stable debt ratio | F79 / F80 | "Yes" / 0.15 |
| Cost of debt changes in stable period? / new cost of debt | E82 / E83 | "Yes" / 0.08 |
| Stable period: CapEx offset by depreciation? (Yes/No) | F86 | "No" |
| If no: CapEx as % of depreciation in steady state (>100%) | F87 | 1.1 |

Year-specific input table (B59:G70), VERBATIM:

| Year | Growth rate in revenue | Operating expense as % of revenue | Growth rate in capital spending | Growth rate in depreciation | Working capital as % of revenue |
|---|---|---|---|---|---|
| 1 | 1.50 | 1.15 | 0.75 | 1.00 | 0.03 |
| 2 | 1.00 | 1.02 | 0.50 | 0.75 | 0.03 |
| 3 | 0.75 | 1.00 | 0.30 | 0.50 | 0.03 |
| 4 | 0.50 | 0.99 | 0.252 | 0.30 | 0.03 |
| 5 | 0.30 | 0.98 | 0.204 | 0.252 | 0.03 |
| 6 | 0.252 | 0.964 | 0.156 | 0.204 | 0.03 |
| 7 | 0.204 | 0.948 | 0.108 | 0.156 | 0.03 |
| 8 | 0.156 | 0.932 | 0.06 | 0.108 | 0.03 |
| 9 | 0.108 | 0.916 | 0.06 | 0.06 | 0.03 |
| 10 | 0.06 | 0.90 | 0.06 | 0.06 | 0.03 |

Compounded average revenue growth (C71) = `(Π(1+g_i))^(1/10) − 1` = 0.4266180.

**Logic** (inferred; verified):

*Cost of capital, initial (D90:D94):*
1. ke = `rf + β×ERP` = 0.065 + 1.6×0.04 = 0.129 (or E49 directly if E48="Yes").
2. Market weights: MV_equity = 84×340.79 = 28,626.36; MV_debt = 349.
   E/(D+E) = 0.9879553; D/(D+E) = 0.0120447.
3. kd_AT = `0.08×(1−0.35)` = 0.052. NOTE: uses the MARGINAL tax rate throughout, even in
   years when NOLs make the effective tax rate zero (row 115 is constant 0.052).
4. WACC = 0.129×0.9879553 + 0.052×0.0120447 = 0.1280726.

*Projections, years i = 1..10 (columns C..L; column M = terminal year):*
5. `Rev_i = Rev_{i−1}×(1+g_rev_i)`; year 1: 1117×2.5 = 2792.5; year 10: 39,005.88;
   terminal: ×1.06 = 41,346.24.
6. `COGS_i = OpExp%_i × Rev_i` (year 1: 1.15×2792.5 = 3211.375; terminal uses E73 = 0.90).
7. `Dep_i = Dep_{i−1}×(1+g_dep_i)` (year 1: 30.6667×2.0 = 61.333; terminal: ×1.06 = 481.30).
8. `EBIT_i = Rev_i − COGS_i − Dep_i` (can be negative; year 1: −480.21).
9. NOL / tax logic (rows 101, 108, 112):
   - If `EBIT_i ≤ 0`: tax = 0; `NOL_i = NOL_{i−1} − EBIT_i` (losses accumulate).
   - If `EBIT_i > 0` and `NOL_{i−1} ≥ EBIT_i`: tax = 0; `NOL_i = NOL_{i−1} − EBIT_i`.
   - If `EBIT_i > 0` and `NOL_{i−1} < EBIT_i`: `tax = t×(EBIT_i − NOL_{i−1})`; `NOL_i = 0`.
   - Row 101 `EBIT*t` is that tax; row 112 shows the effective tax rate `tax/EBIT`
     (e.g. year 8: 0.35×(1322.87−631.07)=242.13 → effective 0.18303; years 9+ full 0.35).
   - Row 109 `Index` = 1 in the final year (internal flag marking end of growth period).
10. `EBIT(1−t)_i = EBIT_i − tax_i` (row 102).
11. `CapEx_i = CapEx_{i−1}×(1+g_capex_i)` (year 1: 242.667×1.75 = 424.667). Terminal-year
    CapEx: since F86="No", `CapEx_T = F87 × Dep_T` = 1.1×481.299 = 529.429. (If F86="Yes",
    CapEx_T = Dep_T — inferred from label.)
12. `ChgWC_i = WC%_i × (Rev_i − Rev_{i−1})` (year 1: 0.03×1675.5 = 50.265; the current-WC
    level D29 and last-year change D30 are NOT used). Terminal: 0.03×(41,346.24−39,005.88)
    = 70.211.
13. `FCFF_i = EBIT(1−t)_i + Dep_i − CapEx_i − ChgWC_i` (row 106). Negative for years 1–9
    in this case; terminal-year FCFF = 2256.320.

*Year-specific cost of capital (rows 112–118):*
14. Beta (row 113): constant at D51 for years 1–5, then linear glide to the stable beta E77
    over years 6–10: 1.6, …, 1.6, 1.48, 1.36, 1.24, 1.12, 1.0. (Glide over the last 5 years
    of the growth period — inferred pattern.)
15. ke_i = `rf + β_i×ERP` (row 114): 0.129 → 0.105.
16. Debt ratio (row 116): market-value ratio 0.0120447 for years 1–5, linear glide to F80
    = 0.15 over years 6–10 (step 0.0275907). Cost of debt (row 115) is a constant kd_AT
    = 0.052 here, because initial and stable pre-tax kd are both 0.08. A differing stable kd
    would presumably glide the same way; that case is not observable in this workbook.
17. `WACC_i` (row 117) = ke_i×(1−DR_i) + kd_AT_i×DR_i: 0.1280726 (yrs 1–5) → 0.09705 (yr 10
    and terminal). Cumulative WACC (row 118) = `Π(1+WACC_j)`: 1.1280726 … 3.0629456.
18. `PV_i = FCFF_i / CumWACC_i` (row 107).

*Terminal value and bridge:*
19. Stable-phase block (E120:E127): g = 0.06; FCFF_T = 2256.320; ke_stable = 0.105;
    E/(D+E) = 0.85, D/(D+E) = 0.15, kd_AT = 0.052; `WACC_stable = 0.105×0.85 + 0.052×0.15
    = 0.09705`. `TV = FCFF_T/(WACC_stable − g)` = 2256.320/0.03705 = 60,899.332 (E127).
20. `PV of high-growth FCFF` (F129) = Σ PV_1..10 = −3841.259.
21. `PV of terminal value` (F130) = TV / CumWACC_10 = 60,899.332/3.0629456 = 19,882.603.
22. `Value of the firm` (F131) = −3841.259 + 19,882.603 = 16,041.345. (No cash added in this
    model — there is no cash input.)
23. `MV of equity` (F133) = firm − MV debt = 16,041.345 − 349 = 15,692.345.
24. `Value of options outstanding` (F134) = 2891.939, pulled from the `Option Valuation` sheet.
25. `Value of equity in common stock` (F135) = 15,692.345 − 2891.939 = 12,800.406.
26. `Value of equity per share` (F136) = 12,800.406/340.79 = **37.561**.

**Worked example** (sheet values, Amazon):

| Year | Revenues | COGS | Dep | EBIT | Tax | EBIT(1−t) | CapEx | ChgWC | FCFF | NOL end | WACC | PV |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2792.5 | 3211.37 | 61.33 | −480.21 | 0 | −480.21 | 424.67 | 50.27 | −893.81 | 1980.21 | 0.12807 | −792.33 |
| 2 | 5585.0 | 5696.70 | 107.33 | −219.03 | 0 | −219.03 | 637.00 | 83.78 | −832.47 | 2199.24 | 0.12807 | −654.18 |
| 3 | 9773.75 | 9773.75 | 161.00 | −161.00 | 0 | −161.00 | 828.10 | 125.66 | −953.76 | 2360.24 | 0.12807 | −664.40 |
| 4 | 14,660.63 | 14,514.02 | 209.30 | −62.69 | 0 | −62.69 | 1036.78 | 146.61 | −1036.78 | 2422.94 | 0.12807 | −640.23 |
| 5 | 19,058.81 | 18,677.64 | 262.04 | 119.13 | 0 | 119.13 | 1248.28 | 131.95 | −999.05 | 2303.80 | 0.12807 | −546.89 |
| 6 | 23,861.63 | 23,002.61 | 315.50 | 543.52 | 0 | 543.52 | 1443.02 | 144.08 | −728.08 | 1760.28 | 0.13131 | −355.43 |
| 7 | 28,729.41 | 27,235.48 | 364.72 | 1129.21 | 0 | 1129.21 | 1598.86 | 146.03 | −250.97 | 631.07 | 0.11487 | −109.89 |
| 8 | 33,211.19 | 31,484.21 | 404.11 | 1322.87 | 242.13 | 1080.74 | 1694.79 | 134.45 | −344.40 | 0 | 0.10866 | −136.02 |
| 9 | 36,798.00 | 34,295.74 | 428.35 | 2073.91 | 725.87 | 1348.04 | 1796.48 | 107.60 | −127.69 | 0 | 0.10272 | −45.73 |
| 10 | 39,005.88 | 35,729.39 | 454.06 | 2822.44 | 987.85 | 1834.58 | 1904.27 | 66.24 | 318.13 | 0 | 0.09705 | 103.87 |
| Terminal | 41,346.24 | 37,211.61 | 481.30 | 3653.32 | 1278.66 | 2374.66 | 529.43 | 70.21 | 2256.32 | — | 0.09705 | — |

(Verbatim row-117 WACC values: years 1–5 = 0.1280726; then 0.1213383, 0.1148689, 0.1086644,
0.1027248, 0.09705.)

TV = 60,899.33; PV(TV) = 19,882.60; PV(FCFF) = −3841.26; firm = 16,041.34; − debt 349;
− options 2891.94; ÷ 340.79 shares = **37.56/share** vs market price 84.

#### Sheet "Option Valuation" — warrants/options with dilution

**Purpose:** Values the firm's outstanding employee options/warrants with a dilution-adjusted
Black–Scholes, feeding F134 of the main sheet.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Current stock price | D2 | 84 |
| Strike price on the option | D3 | 13.375 |
| Expiration of the option (years) | D4 | 8.4 |
| Standard deviation in stock prices (volatility) | D5 | 0.5 |
| Annualized dividend yield on stock | D6 | 0.0 |
| Treasury bond rate | D7 | 0.065 |
| Number of warrants (options) outstanding | D8 | 38 |
| Number of shares outstanding | D9 | 340.79 |

**Logic** (inferred; verified):
1. Dilution-adjusted stock price (C15, "DO NOT ENTER" — computed, circular):
   `S_adj = (S×N_shares + C×N_warrants)/(N_shares + N_warrants)` where `C` is the call value
   from step 5 — a circular reference solved iteratively (Excel iterative calc). Verified:
   (84×340.79 + 76.10366×38)/378.79 = 83.20784.
2. Adjusted K (C16) = K = 13.375 (no adjustment). Variance (F16) = σ² = 0.25.
   Dividend-adjusted interest rate (F18) = rf − y = 0.065.
3. `d1 = [ln(S_adj/K) + (rf − y + σ²/2)×T] / (σ√T)` = [ln(6.22114) + 0.19×8.4]/(0.5×√8.4)
   = 2.3627530 (B20); `N(d1)` = 0.9909301 (B21).
4. `d2 = d1 − σ√T` = 0.9136153 (B23); `N(d2)` = 0.8195405 (B24).
5. `Call = S_adj×e^(−yT)×N(d1) − K×e^(−rf×T)×N(d2)` = 83.20784×0.99093 −
   13.375×e^(−0.546)×0.81954 = 76.10366 (C26).
6. `Value of options` (C28) = Call × N_warrants = 76.10366×38 = 2891.939 → feeds main sheet F134.

#### Sheet "Sheet1" — FCFF/PV summary

A 12-row copy of the valuation cash flows: columns Year (1–10), FCFF, Terminal Value (only
year 10 = 60,899.33), Present Value; D12 = 16,041.34 = firm value. NOTE: here `PV_10`
(19,986.47) = (FCFF_10 + TV)/CumWACC_10, i.e. it includes the TV, unlike row 107 of the main
sheet. Purely a presentation/chart-source table; no new logic.

#### Sheet "What-If" — sensitivity results (static values, VERBATIM)

| Revenue growth | Value per share |
|---|---|
| 0.41 | 37.97 |
| 0.45 | 61.43 |
| 0.50 | 96.59 |

| EBITDA/Sales | Value per share |
|---|---|
| 0.06 | 7.59 |
| 0.08 | 22.67 |
| 0.10 | 37.74 |
| 0.12 | 52.81 |
| 0.14 | 67.89 |

These are pasted results of manual what-if runs (compounded avg revenue growth 0.4266 and the
stable margin around 10% EBITDA/Sales bracket the base-case 37.56/share); no formulas to port.

**Reimplementation (fcffgen):**
- Inputs: base financials (`ebit, capex, depreciation, tax_rate_marginal, revenues,
  nol_carryforward, bv_debt, bv_equity`; `net_income, dividends, interest_expense,
  working_capital, chg_wc` are collected but unused in the value chain), market data
  (`price, shares, mv_debt` or private-firm debt-ratio options), `n_years: int (≤10)`,
  per-year vectors of length n: `g_revenue[], opexp_pct_of_rev[], g_capex[], g_depreciation[],
  wc_pct_of_rev[]`, cost-of-capital (`beta, riskfree, erp, pretax_kd`, optional direct ke),
  stable inputs (`g_stable, opexp_pct_stable, wc_pct_stable, stable_beta, stable_debt_ratio,
  stable_pretax_kd, capex_offset_by_dep: bool, capex_to_dep_stable`),
  option-valuation inputs (`stock_price, strike, expiration_yrs, volatility, dividend_yield,
  tbond_rate, n_warrants, n_shares`).
- Outputs: full projection table (revenues, COGS, depreciation, EBIT, tax, EBIT(1−t), CapEx,
  ChgWC, FCFF, NOL balance), per-year beta/ke/debt-ratio/WACC/cum-WACC, PV vector, terminal
  value, firm value, equity value, option value, value per share.
- Branches: NOL three-way tax logic (see step 9 — the key differentiator of this model);
  terminal CapEx = dep vs ratio×dep; direct ke vs CAPM; public vs private weights; stable
  overrides for beta/debt-ratio/kd. Beta and debt ratio glide linearly from the initial value
  to the stable value over the LAST FIVE years of the growth period (constant before that) —
  hard-coded pattern in this workbook; make the glide-start a parameter.
- Edge cases:
  - Negative-EBIT years pay zero tax and GROW the NOL. This differs from fcff3st's
    negative-tax (credit) behavior.
  - Partial NOL exhaustion in a year (year 8 above) taxes only the excess over the NOL.
  - kd_AT always uses the marginal rate, even when the effective tax is 0. Replicate exactly,
    or expose as an option.
  - FCFF can stay negative for most of the horizon, so the PV of the growth phase can be
    negative.
  - The option value needs an iterative fixed-point solve for S_adj. It converges fast:
    iterate C → S_adj → C.
  - N() is the standard normal CDF.
  - Require `g_stable < WACC_stable`.
  - No cash is added in the equity bridge, unlike fcff2st and fcff3st.

---

## Cross-model summary for the Python port

| Model | Stages | Growth driver | Tax treatment | Discounting | Equity bridge |
|---|---|---|---|---|---|
| fcffst | 1 (perpetuity) | single g | flat rate | single WACC, Gordon growth | none (firm value only) |
| fcff2st | 2 | blended hist/outside/fundamental (ROC×reinv) | flat rate | single WACC both phases (overridable pieces) | + cash − debt − options, ÷ shares |
| fcff3st | 3 (5 const + 5 linear glide + stable) | revenue growth + margin convergence | flat rate (negative EBIT ⇒ tax credit) | year-specific WACC, cumulative product | + cash − debt − options, ÷ shares |
| fcffgen | n (≤10, fully year-specific) + stable | per-year revenue growth + per-year margin | marginal rate with NOL carryforward | year-specific WACC, cumulative product | − debt − BS-with-dilution option value, ÷ shares (no cash) |

Shared building blocks worth one implementation each: CAPM ke; WACC from market-value weights;
fundamental growth `g = ROC × ReinvRate`; stable reinvestment `ReinvRate = g/ROC`; terminal
value `FCFF_T/(WACC − g)`; ChgWC as `WC% × ΔRevenue`; dilution-adjusted Black–Scholes.

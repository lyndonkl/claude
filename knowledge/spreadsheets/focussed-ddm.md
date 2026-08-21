# Damodaran Focussed Valuation Models — Dividend Discount Models

Source folder: `/Users/kushaldsouza/Downloads/2020/Spreadsheets/Focussed Valuation Model Spreadsheet/`

All three files are legacy `.xls` workbooks, each containing exactly ONE populated sheet named after the file (`ddmst.xls`, `ddm2st.xls`, `ddm3st.xls`). Dumps show computed values only (no live formulas), so ALL formulas below are reconstructed from labels, layout, and by numerically verifying against the values in the sheets. Every formula is therefore "(inferred)" unless noted; each one was verified to reproduce the sheet's numbers to the shown precision.

Common conventions across all three models:
- All rates (payout, growth, riskfree, premium, tax) are stored as decimals (0.06 = 6%) even though labels say "(in percent)".
- Cost of equity via CAPM: `ke = riskfree + beta * risk_premium`, unless the user answers "Yes" to entering cost of equity directly.
- Historical growth is a 5-year CAGR from EPS five years ago: `g_hist = (EPS0 / EPS_-5)^(1/5) - 1`.
- Fundamental growth: `g_fund = ROE * retention`, with `retention = 1 - DPS0/EPS0` and `ROE = NetIncome / BookValueOfEquity_lastyear`.
- Terminal (stable) payout from fundamentals: `payout_stable = 1 - g_stable / ROE_stable`.
- None of the three models contains lookup/reference tables (no rating tables, no spread tables). The only tables present are output sensitivity tables, reproduced verbatim below.

---

### ddmst.xls

**Purpose:** Gordon Growth Model (stable-growth, single-stage DDM). Values equity per share of a stable firm that pays out dividends roughly equal to FCFE and grows at a constant rate forever. Damodaran uses it for mature, steady-state firms whose stable growth rate is at or below the nominal growth of the economy.

**Sheet:** single sheet `ddmst.xls`, 56 rows x 6 cols.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Current Earnings per share (currency) | D18 | 4.33 |
| Current Payout Ratio (decimal) | D19 | 0.63 |
| Are you directly entering the cost of equity? (Yes/No) | F21 | "No" |
| If yes, cost of equity (decimal) | D22 (inferred location; blank in sheet) | (empty) |
| Beta of the stock | D24 | 0.95 |
| Riskfree rate (decimal) | D25 | 0.07 |
| Risk Premium (decimal) | D26 | 0.055 |
| Expected Growth Rate forever (decimal) | D28 | 0.06 |

Sheet note next to D28: "The expected growth rate for a stable firm cannot be significantly higher than the nominal growth rate in the economy in which the firm operates. It can be lower."

**Logic:** (all inferred, numerically verified)

1. `DPS0 (D39) = EPS0 * payout = 4.33 * 0.63 = 2.7279`
2. `ke (D41) = IF(F21="Yes", D22, riskfree + beta * premium) = 0.07 + 0.95*0.055 = 0.12225`
3. `g (D42) = D28 = 0.06`
4. `Value (F44) = DPS0 * (1 + g) / (ke - g) = 2.7279 * 1.06 / (0.12225 - 0.06) = 46.450988`
5. Sensitivity table (B47:C56): for g from 0.08 down to 0.00 in steps of 0.01, `Value = DPS0 * (1+g) / (ke - g)` holding ke and DPS0 fixed. Verified: at g=0, 2.7279/0.12225 = 22.3141.

**Warnings block (B33:C35):** present but empty in this sheet. Cells contain only blank strings. The warning logic could not be recovered from the value dump. A port should at minimum raise/warn when `g >= ke`, since the formula divides by ke − g. It should also warn when payout > 1 or < 0. (inferred)

**Reference data:** none (no lookup tables in this workbook).

**Outputs:**

| Cell | Meaning | Value |
|---|---|---|
| D39 | Current dividends per share | 2.7279 |
| D41 | Cost of equity | 0.12225 |
| D42 | Expected growth rate | 0.06 |
| F44 | **Gordon Growth Model value per share** | 46.450987951807235 |
| B47:C56 | Value vs. growth-rate sensitivity table | see below |

Sensitivity table verbatim (B47:C56):

| Growth rate | Value |
|---|---|
| 0.08 | 69.73093491124261 |
| 0.07 | 55.86321531100479 |
| 0.06 | 46.450987951807235 |
| 0.05 | 39.644221453287194 |
| 0.04 | 34.492595744680855 |
| 0.03 | 30.45785365853659 |
| 0.02 | 27.212303178484106 |
| 0.01 | 24.545024498886413 |
| 0.00 | 22.314110429447855 |

**Worked example (values currently in sheet):**
EPS0 = 4.33, payout = 0.63 → DPS0 = 2.7279. ke = 0.07 + 0.95×0.055 = 0.12225. g = 0.06. Value = 2.7279 × 1.06 / (0.12225 − 0.06) = 2.891574 / 0.06225 = **46.45 per share**.

**Reimplementation notes:**
- Inputs: `eps0: float (currency/share)`, `payout: float (0–1)`, `use_direct_ke: bool`, `ke_direct: float|None`, `beta: float`, `riskfree: float`, `risk_premium: float`, `g: float`.
- Output: `value_per_share: float`; optionally the sensitivity series value(g') for g' in [0, 0.08] step 0.01 (or generalize: base g ± range).
- Branches: ke = ke_direct if use_direct_ke else CAPM.
- Edge cases: raise/warn if `g >= ke` (division by zero/negative); warn if `g` materially exceeds nominal economy growth (Damodaran's stated constraint); negative EPS or payout outside [0,1] makes the model inapplicable (dividends must be positive).

---

### ddm2st.xls

**Purpose:** Two-Stage Dividend Discount Model. Values equity per share of a firm with an initial high-growth phase (constant high growth, constant payout) followed by an abrupt drop to stable growth forever. Damodaran uses it for firms with moderate, finite-horizon extraordinary growth. Also decomposes value into assets-in-place, stable growth, and extraordinary growth components.

**Sheet:** single sheet `ddm2st.xls`, 132 rows x 12 cols.

**Assumptions (stated in sheet):** (1) higher growth in first period; (2) growth drops abruptly to stable rate at end of first period; (3) payout ratio is consistent with the expected growth rate.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Current Earnings per share | D21 | 5.49 |
| Current Dividends per share | D22 | 2.3058 |
| Length of extraordinary growth period (years) | E24 | 5 |
| Enter cost of equity directly? (Yes/No) | E26 | "No" |
| If yes, cost of equity | E27 (inferred; blank) | (empty) |
| Beta of the stock | D29 | 0.95 |
| Riskfree rate | D30 | 0.07 |
| Risk Premium | D31 | 0.055 |
| Use historical growth rate? (Yes/No) | E33 | "Yes" |
| If yes, EPS from five years ago | E34 | 1.62 |
| Outside estimate of growth? (Yes/No) | E36 | "Yes" |
| If yes, estimated growth | E37 | 0.17 |
| Calculate growth from fundamentals? (Yes/No) | F39 | "Yes" |
| Net Income currently | D41 | 2122 |
| Book Value of Equity: current / last year | D42 / E42 | 6237 / 6155 |
| Tax Rate on Income | D43 | 0.40 |
| Override ROE/retention for high-growth period? (Yes/No) | G47 | "Yes" |
| If yes: ROE (high growth) | C49 | 0.34476035743298133 |
| If yes: Retention (high growth) | C50 | 0.5800000000000001 |
| Override inputs for stable period? (Yes/No) | G51 | "Yes" |
| If yes: ROE (stable) | C53 | 0.34476035743298133 |
| Weight on historical growth | E57 | 0.4 |
| Weight on outside growth | E58 | 0.4 |
| Weight on fundamental growth | E59 | 0.19999999999999996 (likely `=1-E57-E58`, inferred) |
| Stable-period growth rate | E61 | 0.08 |
| Change stable payout ratio? (Yes/No) | E64 | "No" |
| If yes, stable payout ratio | E65 (blank) | (empty) |
| Beta changes in stable period? (Yes/No) | E67 | "No" |
| If yes, stable-period beta | (cell next to B68; blank) | (empty) |

Computed helper cells shown among inputs (not user-entered):
- C45 `ROE = NetIncome / BV_lastyear = 2122 / 6155 = 0.34476035743298133` (inferred: uses LAST year's book value E42, not current D42; 2122/6237 = 0.34022 does not match). The tax-rate input (D43) does not enter this equity-ROE computation in the values shown; it appears unused in this equity-only model (inferred).
- C46 `Retention = 1 - DPS0/EPS0 = 1 - 2.3058/5.49 = 0.58`
- E63 `Stable payout from fundamentals = 1 - g_stable / ROE_stable = 1 - 0.08/0.34476035743298133 = 0.7679547596606975`

**Logic:** (all inferred, numerically verified)

1. Cost of equity: `ke (D80) = IF(E26="Yes", E27, D30 + D29*D31) = 0.07 + 0.95*0.055 = 0.12225`. Stable-phase cost of equity (E99): same unless E67="Yes", in which case `ke_stable = riskfree + stable_beta*premium` (inferred from the Yes/No question; example uses "No" so E99 = 0.12225).
2. Growth-rate estimates:
   - `g_hist (D86) = (EPS0/EPS_-5)^(1/5) - 1 = (5.49/1.62)^0.2 - 1 = 0.2764725090252995`
   - `g_outside (D87) = E37 = 0.17`
   - `g_fund (D88) = ROE_hg * retention_hg = 0.34476035743298133 * 0.58 = 0.1999610073111292` (uses the possibly-overridden high-growth ROE C49 and retention C50)
   - Weights (E86:E88) copied from E57:E59.
   - `g_high (D89) = 0.4*0.2764725 + 0.4*0.17 + 0.2*0.1999610 = 0.21858120507234563`
   - Behavior when a source is answered "No": the corresponding growth rate is treated as 0 but its weight is still applied as entered (see ddm3st worked example where fundamental = "No" gives g_fund = 0 with weight 0.4). (inferred)
3. High-growth payout: `payout_hg (E91) = retention answer: 1 - C50 = 1 - 0.58 = 0.41999999999999993` (i.e., 1 − retention used in fundamental growth).
4. Dividends in high-growth phase, year t = 1..n (row 95, up to 10 columns): `Div_t = EPS0 * (1+g_high)^t * payout_hg`. Year 1: 5.49*1.2185812*0.42 = 2.8098045426558143. Columns beyond n are blank.
5. Stable phase:
   - `g_stable (E97) = E61 = 0.08`
   - `payout_stable (E98) = IF(E64="Yes", E65, 1 - g_stable/ROE_stable) = 0.7679547596606975`
   - `ke_stable (E99) = 0.12225` (see step 1)
   - Terminal price at end of year n: `P_n (E100) = EPS0*(1+g_high)^n * (1+g_stable) * payout_stable / (ke_stable - g_stable)` = 5.49*1.2185812^5*1.08*0.7679548/0.04225 = 289.5858921157306.
6. Present values (discount at ke of high-growth phase):
   - `PV(dividends) (F102) = Σ_{t=1..n} Div_t / (1+ke)^t = 14.860287167483582`
   - `PV(terminal) (F103) = P_n / (1+ke)^n = 289.5858921157306 / 1.12225^5 = 162.6781893518095`
   - `Value of stock (F104) = F102 + F103 = 177.53847651929308`
7. Value-of-growth decomposition (B107:E111):
   - `Value of assets in place (E108) = DPS0 / ke = 2.3058 / 0.12225 = 18.861349693251533` (perpetuity of current dividend, no growth)
   - `Value of stable growth (E109) = DPS0*(1+g_stable)/(ke - g_stable) - DPS0/ke = 58.94116 - 18.86135 = 40.07981007006209`
   - `Value of extraordinary growth (E110) = TotalValue - DPS0*(1+g_stable)/(ke - g_stable) = 177.53848 - 58.94116 = 118.59731675597948`
   - `Value of the stock (E111) = sum of the three = 177.5384765192931`

**Reference data:** none (no lookup tables). Two output sensitivity tables, verbatim:

Table 1 (C114:D132) — Value of extraordinary growth as first-phase growth rate varies (rows are g_high from base−0.10 to base+0.06, step 0.01; base weighted g_high = 0.21858120507234563 reproduces the base extraordinary-growth value 118.5973):

| Growth Rate: First phase | Extraordinary Growth |
|---|---|
| 0.11858120507234562 | 58.496907927679665 |
| 0.12858120507234563 | 63.63069146008231 |
| 0.13858120507234564 | 68.94595315602106 |
| 0.14858120507234565 | 74.44751012686015 |
| 0.15858120507234566 | 80.14026432103739 |
| 0.16858120507234567 | 86.02920326611115 |
| 0.17858120507234568 | 92.11940081080866 |
| 0.1885812050723457 | 98.41601786707403 |
| 0.1985812050723457 | 104.92430315211621 |
| 0.2085812050723457 | 111.64959393045709 |
| 0.2185812050723457 | 118.59731675597945 |
| 0.22858120507234572 | 125.7729882139752 |
| 0.23858120507234573 | 133.18221566319312 |
| 0.24858120507234574 | 140.83069797788698 |
| 0.2585812050723457 | 148.72422628986388 |
| 0.26858120507234573 | 156.8686847305316 |
| 0.27858120507234574 | 165.27005117294746 |

(inferred: each row recomputes the full model with that g_high and subtracts `DPS0*(1+g_stable)/(ke-g_stable)`; the base row matches E110.)

Table 2 (F114:G125) — Value of extraordinary growth as the length of the growth period varies (0–10 years; row n=5 matches E110 = 118.597…):

| Growth period (years) | Value |
|---|---|
| 0 | 48.83061209420611 |
| 1 | 60.58520260298098 |
| 2 | 73.3487785150459 |
| 3 | 87.20794867851785 |
| 4 | 102.25675623397018 |
| 5 | 118.59731675597948 |
| 6 | 136.34051117118787 |
| 7 | 155.6067381547634 |
| 8 | 176.52673111073827 |
| 9 | 199.24244527994907 |
| 10 | 223.90802099516034 |

(inferred: recomputes value with n-year high-growth phase minus the stable-growth-only value; note row n=0 is 48.83, not 0 — the exact n=0 convention could not be fully reverse-engineered from values alone; it does not equal TotalValue(n=0) − 58.94 = 0. Flag for a port: reproduce rows n>=1 by `Value(n) − DPS0*(1+g_stable)/(ke−g_stable)`; the n=0 row of the original is left as an open question.)

**Warnings block (B71:B77):** present, all blank strings in the current sheet; warning logic unrecoverable from the value dump. A port should warn when: g_stable >= ke_stable; stable payout < 0 (happens when g_stable > ROE_stable); weights don't sum to 1. (inferred)

**Outputs:**

| Cell | Meaning | Value |
|---|---|---|
| D80 | Cost of equity (high growth) | 0.12225 |
| D89 | Weighted-average high-growth rate | 0.21858120507234563 |
| E91 | High-growth payout ratio | 0.42 |
| C95:G95 | Dividends, years 1–5 | 2.8098, 3.4240, 4.1724, 5.0844, 6.1958 |
| E100 | Price at end of growth phase | 289.5858921157306 |
| F102 | PV of high-growth dividends | 14.860287167483582 |
| F103 | PV of terminal price | 162.6781893518095 |
| **F104** | **Value of the stock** | **177.53847651929308** |
| E108 | Value of assets in place | 18.861349693251533 |
| E109 | Value of stable growth | 40.07981007006209 |
| E110 | Value of extraordinary growth | 118.59731675597948 |

**Worked example (values in sheet):**
- Base inputs: EPS0 = 5.49, DPS0 = 2.3058, n = 5. ke = 0.07 + 0.95×0.055 = 0.12225.
- Growth estimates: g_hist = (5.49/1.62)^(1/5)−1 = 27.647%. g_outside = 17%. ROE = 2122/6155 = 34.476%. Retention = 1−2.3058/5.49 = 0.58. g_fund = 0.34476×0.58 = 19.996%.
- Weighted: g_high = 0.4(27.647%) + 0.4(17%) + 0.2(19.996%) = 21.858%. payout_hg = 0.42.
- Dividends: Div_t = 5.49×1.21858^t×0.42 → 2.8098 … 6.1958 for t = 1..5. PV at 12.225% = 14.8603.
- Terminal: payout_stable = 1 − 0.08/0.34476 = 0.76795. EPS_5 = 5.49×1.21858^5 = 14.7519. P_5 = 14.7519×1.08×0.76795/(0.12225−0.08) = 289.586. PV = 289.586/1.12225^5 = 162.678.
- Value = 14.860 + 162.678 = **177.538 per share**.
- Decomposition: assets-in-place 18.861 + stable growth 40.080 + extraordinary growth 118.597 = 177.538.

**Reimplementation notes:**
- Inputs: `eps0, dps0: float`; `n_high: int (years)`; `use_direct_ke: bool, ke_direct: float|None, beta, riskfree, risk_premium: float`; `use_hist: bool, eps_5yr_ago: float|None`; `use_outside: bool, g_outside: float|None`; `use_fund: bool, net_income: float|None, bv_equity_current: float|None, bv_equity_prior: float|None, tax_rate: float|None (appears unused)`; `roe_hg_override, retention_hg_override: float|None`; `roe_stable_override: float|None`; `w_hist, w_outside, w_fund: float`; `g_stable: float`; `payout_stable_override: float|None`; `stable_beta: float|None`.
- Outputs: `ke, g_high, payout_hg, dividends[1..n], terminal_price, pv_dividends, pv_terminal, value_per_share, value_assets_in_place, value_stable_growth, value_extraordinary_growth`.
- Branches: direct-ke vs CAPM; each growth source on/off ("No" → that growth = 0, weight still applied as entered); ROE/retention overrides for high-growth and stable phases; stable payout override; stable beta change (recompute ke_stable).
- Edge cases:
  - ROE uses the PRIOR-year book value.
  - g_stable >= ke_stable breaks the terminal value.
  - g_stable > ROE_stable gives a negative stable payout.
  - Negative or zero `eps_5yr_ago` breaks the CAGR and needs a guard.
  - n_high is capped at 10 in the sheet layout. A port need not keep that cap, but the sheet has it.
  - Dividends must be > 0 for the decomposition to be meaningful.

---

### ddm3st.xls

**Purpose:** Three-Stage Dividend Discount Model. Values equity per share of a firm with three phases. Phase 1 is an initial period of constant high growth. Phase 2 is a transition in which growth declines linearly to the stable rate, while payout (and optionally beta) adjust linearly to their stable levels. Phase 3 is stable growth forever. Damodaran uses it for firms currently in extraordinary growth expected to fade gradually rather than abruptly.

**Sheet:** single sheet `ddm3st.xls`, 121 rows x 12 cols.

**Assumptions (stated in sheet):** (1) firm currently in extraordinary growth; (2) it lasts a specified initial period; (3) growth declines linearly over the transition to the stable rate; (4) payout changes consistently with the growth rate.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Current Earnings per share | D22 | 1.43 |
| Current Dividends per share | D23 | 0.56 |
| Enter cost of equity directly? (Yes/No) | E25 | "No" |
| If yes, cost of equity | E26 (inferred; blank) | (empty) |
| Beta of the stock | D28 | 1.1 |
| Riskfree rate | D29 | 0.07 |
| Risk Premium | D30 | 0.055 |
| Length of extraordinary growth period (years) | E33 | 10 |
| Use historical growth rate? (Yes/No) | E35 | "Yes" |
| If yes, EPS from five years ago | E36 | 0.61 |
| Outside estimate of growth? (Yes/No) | E38 | "Yes" |
| If yes, estimated growth | E39 | 0.17 |
| Calculate growth from fundamentals? (Yes/No) | F41 | "No" |
| Net Income currently | D43 | 0 |
| Book Value of Equity: current / last year | D44 / E44 | 0 / 0 |
| Tax Rate on Income | D45 | 0 |
| Override ROE/retention for high-growth period? (Yes/No) | G49 | "No" |
| If yes: ROE / Retention (high growth) | C51 / C52 | "NA" / 0.6083916083916083 (computed) |
| Override inputs for stable period? (Yes/No) | G53 | "Yes" |
| If yes: ROE (stable) | C55 | 0.2 |
| Weight on historical growth | E59 | 0.2 |
| Weight on outside growth | E60 | 0.4 |
| Weight on fundamental growth | E61 | 0.4 |
| Length of transition period (years) | E64 | 8 |
| Payout adjusts gradually to stable payout? (Yes/No) | G66 | "Yes" |
| If no, payout ratio for transition period | (near B67; blank) | (empty) |
| Beta adjusts gradually to stable beta? (Yes/No) | G69 | "Yes" |
| If no, beta for transition period | (near B70; blank) | (empty) |
| Growth rate in stable period | E73 | 0.08 |
| Change stable payout ratio? (Yes/No) | E76 | "No" |
| If yes, stable payout ratio | (near B77; blank) | (empty) |
| Beta changes in stable period? (Yes/No) | E79 | "No" |
| If yes, beta for stable period | (near B80; blank) | (empty) |

Computed helper cells among inputs:
- C47 ROE = "NA" (Net income and book value are 0 because fundamentals answered "No" → division not possible; sheet shows the string "NA")
- C48 `Retention = 1 - DPS0/EPS0 = 1 - 0.56/1.43 = 0.6083916083916083`
- E75 `Stable payout from fundamentals = 1 - g_stable/ROE_stable = 1 - 0.08/0.2 = 0.6000000000000001`

**Logic:** (all inferred, numerically verified)

*Phase 1 — Initial high growth (years 1..n1, n1 = E33 = 10):*
1. `ke_high (D84) = IF(E25="Yes", E26, riskfree + beta*premium) = 0.07 + 1.1*0.055 = 0.1305`
2. Growth estimates (D89:D91 with weights E89:E91 = E59:E61):
   - `g_hist = (1.43/0.61)^(1/5) - 1 = 0.18577213512567559`
   - `g_outside = 0.17`
   - `g_fund = 0` (fundamentals answered "No" → 0; NOTE: its 0.4 weight is STILL applied)
   - `g_high (D92) = 0.2*0.18577214 + 0.4*0.17 + 0.4*0 = 0.10515442702513512`
3. `payout_hg (E94) = 1 - retention = 1 - 0.6083916083916083 = 0.39160839160839167`
4. Year t = 1..n1 (row 97 years, row 98 earnings, row 99 dividends, row 100 PVs; layout supports up to 10 years):
   - `E_t = EPS0 * (1+g_high)^t` (E_1 = 1.43*1.10515443 = 1.5803708306459432)
   - `Div_t = E_t * payout_hg` (Div_1 = 0.6188864791340758)
   - `PV_t = Div_t / (1+ke_high)^t` (PV_1 = 0.5474449174118318)

*Phase 2 — Transition (years n1+1 .. n1+n2, n2 = E64 = 8; layout supports up to 10 transition years):*
5. Growth declines linearly to g_stable: for j = 1..n2 (year = n1+j),
   `g_j (row 104) = g_high - (g_high - g_stable) * j / n2`
   (year 11: 0.10515443 − 0.02515443×1/8 = 0.10201012364699323; year 18 = 0.08 exactly)
6. Payout adjusts linearly to stable payout (because G66 = "Yes"):
   `payout_j (row 105) = payout_hg + (payout_stable - payout_hg) * j / n2`
   (year 11: 0.39160839 + 0.20839161×1/8 = 0.4176573426573427; year 18 = 0.6). If G66 = "No", the transition payout is the constant entered next to B67 (inferred).
7. Beta (row 108): since stable beta is unchanged (E79 = "No") and G69 = "Yes", beta stays 1.1 throughout; in general (inferred) `beta_j = beta_high + (beta_stable - beta_high) * j / n2` when adjusting gradually, else the constant transition beta from the B70 input. `ke_j (row 109) = riskfree + beta_j * premium` (all 0.1305 here).
8. `E_{n1+j} (row 106) = E_{n1+j-1} * (1 + g_j)` (year 11: 3.886563×1.10201012 = 4.283031799811177)
9. `Div_{n1+j} (row 107) = E_{n1+j} * payout_j` (year 11: 4.283032×0.41765734 = 1.788839680026032)
10. `PV (row 110) = Div / (1+ke)^year`, ke varying by year if beta drifts (constant 0.1305 here; year 11 PV: 1.78884/1.1305^11 = 0.4640824939472954). With drifting ke the discount factor should be the cumulative product Π(1+ke_t) (inferred — cannot be distinguished from the constant-ke case in this example).

*Phase 3 — Stable phase and value:*
11. `g_stable (E113) = 0.08`; `payout_stable (E114) = IF(E76="Yes", override, 1 - g_stable/ROE_stable) = 0.6`; `ke_stable (E115) = 0.1305` (recomputed with stable beta if E79 = "Yes").
12. Terminal price at end of transition (year N = n1+n2 = 18):
    `P_N (E116) = E_N * (1+g_stable) * payout_stable / (ke_stable - g_stable) = 7.800170274744381 * 1.08 * 0.6 / 0.0505 = 100.08931362444277`
13. `PV of high-growth dividends (F118) = Σ_{t=1..10} PV_t = 4.953896409065219`
14. `PV of transition dividends (F119) = Σ_{t=11..18} PV_t = 3.988446909448224`
15. `PV of terminal price (F120) = P_N / (1+ke)^N = 100.089314 / 1.1305^18 = 11.003162091777472`
16. `Value of the stock (F121) = F118 + F119 + F120 = 19.945505410290917`

**Reference data:** none (no lookup tables in this workbook). No sensitivity tables either.

**Warnings:** no warnings block visible in the value dump of this sheet (the ddm2st-style warning area does not appear). A port should still validate: g_stable < ke_stable; ROE_stable > g_stable (else stable payout <= 0); weights sum to 1; eps_5yr_ago > 0.

**Outputs:**

| Cell | Meaning | Value |
|---|---|---|
| D84 | Cost of equity (high growth) | 0.1305 |
| D92 | Weighted-average high-growth rate | 0.10515442702513512 |
| E94 | High-growth payout ratio | 0.39160839160839167 |
| C98:L98 | Earnings, years 1–10 | 1.5804 → 3.8866 |
| C99:L99 | Dividends, years 1–10 | 0.6189 → 1.5220 |
| C100:L100 | PV of dividends, years 1–10 | 0.5474 → 0.4464 |
| C104:J110 | Transition table (growth, payout, earnings, dividends, beta, ke, PV), years 11–18 | see logic above |
| E116 | Price at end of transition phase | 100.08931362444277 |
| F118 | PV of dividends, high-growth phase | 4.953896409065219 |
| F119 | PV of dividends, transition phase | 3.988446909448224 |
| F120 | PV of terminal price | 11.003162091777472 |
| **F121** | **Value of the stock** | **19.945505410290917** |

Transition-phase table verbatim (years 11–18):

| Year | Growth Rate | Payout Ratio | Earnings | Dividends | Beta | Cost of Equity | Present Value |
|---|---|---|---|---|---|---|---|
| 11 | 0.10201012364699323 | 0.4176573426573427 | 4.283031799811177 | 1.788839680026032 | 1.1 | 0.1305 | 0.4640824939472954 |
| 12 | 0.09886582026885134 | 0.4437062937062938 | 4.706477251937083 | 2.088293577869986 | 1.1 | 0.1305 | 0.47923083363770036 |
| 13 | 0.09572151689070944 | 0.4697552447552448 | 5.156988393704119 | 2.4225223450844355 | 1.1 | 0.1305 | 0.491756857434556 |
| 14 | 0.09257721351256755 | 0.4958041958041959 | 5.634408009309898 | 2.7935631318886145 | 1.1 | 0.1305 | 0.501615048521202 |
| 15 | 0.08943291013442566 | 0.5218531468531469 | 6.138309514467198 | 3.2032961364833197 | 1.1 | 0.1305 | 0.5087900267246532 |
| 16 | 0.08628860675628376 | 0.5479020979020979 | 6.667975690309413 | 3.6533978694807168 | 1.1 | 0.1305 | 0.5132960287884311 |
| 17 | 0.08314430337814187 | 0.5739510489510489 | 7.222379884022574 | 4.145292510357711 | 1.1 | 0.1305 | 0.5151759114733102 |
| 18 | 0.07999999999999997 | 0.5999999999999999 | 7.800170274744381 | 4.680102164846628 | 1.1 | 0.1305 | 0.5144997089210761 |

**Worked example (values in sheet):**
- Base inputs: EPS0 = 1.43, DPS0 = 0.56. ke = 0.07 + 1.1×0.055 = 0.1305. n1 = 10, n2 = 8.
- Growth estimates: g_hist = (1.43/0.61)^(1/5)−1 = 18.577%. g_outside = 17%. g_fund = 0 (source disabled but weight 0.4 kept).
- Weighted: g_high = 0.2(18.577%) + 0.4(17%) + 0.4(0) = 10.515%. payout_hg = 1−0.56/1.43 = 39.161%.
- High-growth phase: earnings compound at 10.515% to 3.8866 in year 10. Dividends run 0.6189→1.5220. Their PVs sum to 4.9539.
- Transition: growth falls 10.515%→8% linearly over 8 years. Payout rises 39.161%→60% linearly. Earnings reach 7.8002 in year 18. Dividend PVs sum to 3.9884.
- Stable phase: ROE_stable = 0.2 (override) → payout_stable = 1−0.08/0.2 = 0.6. P_18 = 7.8002×1.08×0.6/(0.1305−0.08) = 100.0893. PV = 100.0893/1.1305^18 = 11.0032.
- Value = 4.9539 + 3.9884 + 11.0032 = **19.9455 per share**.

**Reimplementation notes:**
- Inputs: `eps0, dps0: float`; `use_direct_ke: bool, ke_direct: float|None, beta, riskfree, risk_premium: float`; `n_high: int`; `use_hist: bool, eps_5yr_ago: float|None`; `use_outside: bool, g_outside: float|None`; `use_fund: bool, net_income, bv_current, bv_prior, tax_rate: float|None`; overrides `roe_hg, retention_hg, roe_stable: float|None`; `w_hist, w_outside, w_fund: float`; `n_transition: int`; `payout_adjusts_gradually: bool, payout_transition: float|None`; `beta_adjusts_gradually: bool, beta_transition: float|None`; `g_stable: float`; `payout_stable_override: float|None`; `stable_beta: float|None`.
- Outputs: per-year schedule (growth, payout, beta, ke, earnings, dividends, PV) for years 1..n_high+n_transition, terminal price, the three PV subtotals, and value per share.
- Branches:
  - Direct ke vs CAPM.
  - Each growth source on/off. Off means that estimate is 0 while its weight is still applied. This is the sheet's observed behavior and it materially lowers g_high. A port should reproduce it and optionally warn.
  - Linear vs constant transition payout.
  - Linear vs constant transition beta. Recompute ke per year from beta. With time-varying ke, discount transition and terminal cash flows with the cumulative product of (1+ke_t) (inferred).
  - Stable payout override. Stable beta change.
- Edge cases:
  - ROE = "NA" when book value is 0. Fundamental growth is then treated as 0.
  - g_stable >= ke_stable breaks the terminal value.
  - ROE_stable <= g_stable makes payout_stable <= 0.
  - Sheet layout caps both n_high and n_transition at 10 years.
  - Retention derived from DPS0/EPS0 fails for negative EPS.
  - Linear ramps use step `j/n_transition` and end exactly at the stable values in the final transition year.

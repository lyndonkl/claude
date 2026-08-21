# Damodaran Corporate Finance Spreadsheets — ratings, risk, riskchecker, returncalculator

Source folder: `/Users/kushaldsouza/Downloads/2020/Spreadsheets/Corporate Finance Spreadsheets/`
All four files are legacy `.xls`; dumps expose computed VALUES only. All formula logic below was reconstructed from labels, layout, and by numerically re-deriving every output from the inputs — each reconstruction was verified to reproduce the sheet's numbers to full precision unless flagged otherwise. Anything reconstructed is marked "(inferred)".

---

### ratings.xls

Sheets: `Start here Ratings sheet` (main), `Operating Leases` (sub-model). Sheet4–Sheet16 are empty stubs.

**Purpose:** Estimates a *synthetic bond rating* for a firm from its interest coverage ratio, then a default spread and a pre-tax cost of debt. Damodaran uses this when a firm has no traded/rated bonds, or to sanity-check an actual rating, in cost-of-capital estimation. The `Operating Leases` sheet converts operating-lease commitments into debt and adjusts operating income; when the firm has leases, that adjustment feeds back into the coverage ratio (circular — Excel iteration must be on, per the note in A3).

**Inputs — `Start here Ratings sheet`:**

| Label | Cell | Example value |
|---|---|---|
| Type of firm (1 = large manufacturing, 2 = smaller or riskier firm, 3 = financial service firm) | C4 | 2 |
| Do you have any operating lease or rental commitments? (Yes/No) | F5 | "No" |
| Current EBIT (add back only long-term interest expense for financial firms) | F6 | 50.0 |
| Current interest expenses (only long-term interest expense for financial firms) | F7 | 8.0 |
| Current long-term government bond rate (riskfree rate) | F8 | 0.03 |

Note in I4: "Small: <$5 billion" — the large/small firm distinction is by size, roughly $5bn (market cap). Cells O1:P3 hold the dropdown lists ("Yes"/"No"; 1/2/3).

**Inputs — `Operating Leases` sheet:**

| Label | Cell | Example value |
|---|---|---|
| Operating lease expense in current year | E2 | 25.0 |
| Lease commitment, year 1 (next year) | B5 | 24.0 |
| Lease commitment, year 2 | B6 | 22.0 |
| Lease commitment, year 3 | B7 | 22.0 |
| Lease commitment, year 4 | B8 | 21.0 |
| Lease commitment, year 5 | B9 | 20.0 |
| Lease commitment, "6 and beyond" (lump sum of all later years) | B10 | 111.0 |
| Pre-tax cost of debt | C12 | 0.0418 (linked to ratings output D13 — circular) (inferred) |
| Reported Operating Income (EBIT) | D15 | 50.0 |
| Reported Debt (interest-bearing, from balance sheet) | D16 | 92.97 |
| Reported Interest Expenses | D17 | 8.0 |

**Logic (inferred throughout; verified numerically):**

*Ratings sheet, no leases (F5 = "No"):*
1. Interest coverage ratio: `ICR = EBIT / InterestExpense` → D10 = 50/8 = 6.25.
2. Range-lookup ICR in the spread table selected by firm type (tables below): find the row where `lower < ICR ≤ upper`; return Rating (D11) and Spread (D12).
3. Cost of debt: `D13 = RiskfreeRate + Spread` = 0.03 + 0.0118 = 0.0418.

*Ratings sheet, with leases (F5 = "Yes"). This branch is inferred — it cannot be verified from stored values since F5="No".* EBIT and interest expense are replaced by lease-adjusted versions from the `Operating Leases` sheet. EBIT_adj = EBIT + current lease expense − depreciation on leased asset. Interest_adj = InterestExpense + PreTaxCostOfDebt × DebtValueOfLeases. The calculation is circular: cost of debt depends on the rating, the rating depends on the lease-adjusted ICR, and the ICR depends on cost of debt. Hence the requirement to enable Excel iteration (A3). Hence also the troubleshooting note in F11:F12 — on REF! errors, set F5 to No and back to Yes.

*Operating Leases sheet:*
1. Years embedded in the year-6+ lump sum: `n6 = ROUND(B10 / AVERAGE(B5:B9), 0)` — D19 = round(111 / 21.8) = 5. (The note E19–E20 says: average lease expense over the first five years is used to estimate the number of years of expenses in year 6.)
2. Annualized year-6+ commitment: `B28 = B10 / n6` = 111/5 = 22.2.
3. PV of each of years 1–5: `C(22+t) = Commitment_t / (1 + kd)^t` (kd = pre-tax cost of debt, C12). E.g. C23 = 24/1.0418 = 23.0371.
4. PV of year-6+ block: annuity of B28 for n6 years, discounted back 5 years: `C28 = B28 × [1 − (1+kd)^−n6] / kd × (1+kd)^−5` = 22.2 × 4.4294 × 0.81485 = 80.1265. (The D28 comment says "annuity for ten years" but the actual annuity length is n6 = D19; verified numerically.)
5. Debt value of leases: `C29 = SUM(C23:C28)` = 177.0144.
6. Depreciation on leased asset (straight line over total lease life 5 + n6 years): `D39 = C29 / (5 + n6)` = 177.0144/10 = 17.7014.
7. Adjusted operating income: `F32 = D40 = EBIT + CurrentLeaseExpense − Depreciation` = 50 + 25 − 17.7014 = 57.2986.
8. Adjusted debt: `F33 = ReportedDebt + DebtValueOfLeases` = 92.97 + 177.0144 = 269.9844.

**Reference data (verbatim):**

*Table 1 — Large manufacturing firms (A17:D33). Lookup: lower < ICR ≤ upper.*

| ICR > | ICR ≤ | Rating | Spread |
|---|---|---|---|
| -100000 | 0.199999 | D2/D | 0.1744 |
| 0.2 | 0.649999 | C2/C | 0.1309 |
| 0.65 | 0.799999 | Ca2/CC | 0.0997 |
| 0.8 | 1.249999 | Caa/CCC | 0.0946 |
| 1.25 | 1.499999 | B3/B- | 0.0594 |
| 1.5 | 1.749999 | B2/B | 0.0486 |
| 1.75 | 1.999999 | B1/B+ | 0.0405 |
| 2.0 | 2.2499999 | Ba2/BB | 0.0277 |
| 2.25 | 2.49999 | Ba1/BB+ | 0.0231 |
| 2.5 | 2.999999 | Baa2/BBB | 0.0171 |
| 3.0 | 4.249999 | A3/A- | 0.0133 |
| 4.25 | 5.499999 | A2/A | 0.0118 |
| 5.5 | 6.499999 | A1/A+ | 0.0107 |
| 6.5 | 8.499999 | Aa2/AA | 0.0085 |
| 8.5 | 100000 | Aaa/AAA | 0.0069 |

*Table 2 — Financial service firms (F17:I33), keyed on the LONG-TERM interest coverage ratio:*

| ICR > | ICR ≤ | Rating | Spread |
|---|---|---|---|
| -100000 | 0.049999 | D2/D | 0.1744 |
| 0.05 | 0.099999 | C2/C | 0.1309 |
| 0.1 | 0.199999 | Ca2/CC | 0.0997 |
| 0.2 | 0.299999 | Caa/CCC | 0.0946 |
| 0.3 | 0.399999 | B3/B- | 0.0594 |
| 0.4 | 0.499999 | B2/B | 0.0486 |
| 0.5 | 0.599999 | B1/B+ | 0.0405 |
| 0.6 | 0.749999 | Ba2/BB | 0.0277 |
| 0.75 | 0.899999 | Ba1/BB+ | 0.0231 |
| 0.9 | 1.199999 | Baa2/BBB | 0.0171 |
| 1.2 | 1.49999 | A3/A- | 0.0133 |
| 1.5 | 1.99999 | A2/A | 0.0118 |
| 2.0 | 2.49999 | A1/A+ | 0.0107 |
| 2.5 | 2.99999 | Aa2/AA | 0.0085 |
| 3.0 | 100000 | Aaa/AAA | 0.0069 |

*Table 3 — Smaller and riskier firms (A36:D52):*

| ICR > | ICR ≤ | Rating | Spread |
|---|---|---|---|
| -100000 | 0.499999 | D2/D | 0.1744 |
| 0.5 | 0.799999 | C2/C | 0.1309 |
| 0.8 | 1.249999 | Ca2/CC | 0.0997 |
| 1.25 | 1.499999 | Caa/CCC | 0.0946 |
| 1.5 | 1.999999 | B3/B- | 0.0594 |
| 2.0 | 2.499999 | B2/B | 0.0486 |
| 2.5 | 2.999999 | B1/B+ | 0.0405 |
| 3.0 | 3.499999 | Ba2/BB | 0.0277 |
| 3.5 | 3.9999999 | Ba1/BB+ | 0.0231 |
| 4.0 | 4.499999 | Baa2/BBB | 0.0171 |
| 4.5 | 5.999999 | A3/A- | 0.0133 |
| 6.0 | 7.499999 | A2/A | 0.0118 |
| 7.5 | 9.499999 | A1/A+ | 0.0107 |
| 9.5 | 12.499999 | Aa2/AA | 0.0085 |
| 12.5 | 100000 | Aaa/AAA | 0.0069 |

(Header note A15: spreads can be updated from bondsonline.com.)

**Outputs:**

| Cell | Meaning | Current value |
|---|---|---|
| D10 | Interest coverage ratio | 6.25 |
| D11 | Estimated bond rating (Moody's/S&P notation) | "A2/A" |
| D12 | Estimated default spread | 0.0118 |
| D13 | Estimated pre-tax cost of debt (= riskfree + spread) | 0.0418 |
| Op.Leases C29 | Debt value of operating leases | 177.0144 |
| Op.Leases F32 / D40 | Lease-adjusted operating income | 57.2986 |
| Op.Leases F33 | Lease-adjusted debt | 269.9844 |

**Worked example (values currently in sheet):** Firm type 2 (small/risky), no leases used in the rating; EBIT 50, interest 8, riskfree 3%. ICR = 50/8 = 6.25 → small-firm table row (6.0, 7.499999] → rating A2/A, spread 1.18% → cost of debt = 3% + 1.18% = 4.18%. That 4.18% flows into the Operating Leases sheet as the discount rate. PV of the year 1–5 commitments (24, 22, 22, 21, 20) = 23.04 + 20.27 + 19.46 + 17.83 + 16.30. The year-6 block of 111 becomes 5 years of 22.2, with PV 80.13. Lease debt = 177.01. Depreciation = 177.01/10 = 17.70. Adjusted OI = 50 + 25 − 17.70 = 57.30. Adjusted debt = 92.97 + 177.01 = 269.98.

**Reimplementation notes:**
- Inputs: firm_type ∈ {1: large, 2: small/risky, 3: financial}; has_leases: bool; ebit: float (currency); interest_expense: float; riskfree_rate: float (decimal); plus lease inputs (current lease expense, commitments years 1–5, lump for 6+, reported EBIT/debt/interest) when has_leases.
- Core function: `synthetic_rating(icr, firm_type) -> (rating, spread)` via the three tables; interval is (lower, upper] but any consistent handling works given the .999999 gaps.
- Edge cases: interest expense = 0 → ICR infinite → treat as top bucket (Aaa/AAA); negative EBIT → negative ICR → falls in the first bucket (lower bound −100000, i.e. D rating); ICR below −100000 is unhandled in the sheet — clamp to the first bucket. Financial firms use long-term interest only and a much lower ICR scale.
- With leases, solve the circularity by fixed-point iteration. Start with kd = riskfree + some spread. Compute lease debt and the adjusted ICR. Re-rate, recompute kd, and repeat until the spread is stable. It converges in a few iterations. Guard against oscillation between adjacent buckets by capping iterations and keeping the last value.
- n6 = round(lump / mean(first five commitments)); if the first five commitments are all zero this divides by zero — guard (treat lump as one year or skip). Depreciation life = 5 + n6, straight line.

---

### risk.xls

Sheet: `Risk&RetWS` (only sheet).

**Purpose:** A teaching spreadsheet for running a market-model (CAPM) regression from raw price data. It computes stock and market returns from a price/dividend/split series. From those it estimates beta, alpha, Jensen's alpha, a variance decomposition (systematic vs. firm-specific risk), R², the CAPM expected return, and forecast prices. Damodaran uses it in the risk-and-return section of corporate finance to show how a beta regression is built by hand.

**Inputs:**

| Label | Cell | Example value |
|---|---|---|
| Current riskfree rate | C1 | 0.065 |
| Number of periods of data | C2 | 53 |
| Risk premium for stocks | G1 | 0.055 |
| Riskfree rate during regression period (annual) | G2 | 0.06 |
| Current stock price | J1 | 35.0 |
| Current annual DPS (dividends per share) | J2 | 0.0 |
| Per period t = 1..60 (rows 4–63): Price(Stock) col C; DPS(Stock) col D (blank/0 most periods); Split Factor col E; Index Level col F | C4:F63 | e.g. row 4: price 30.75, split 1.0, index 179.63 |

Column B ("Index") is an include-flag: 1 for rows in the sample (t ≤ C2, rows 4–56), 0 for rows 57–63 beyond the chosen sample — flagged-0 rows show returns of exactly 0, i.e. `return = flag × raw_return` (inferred). Data frequency is generic "periods"; the current setup behaves like monthly data.

**Logic (all inferred; every value verified numerically):**
1. Stock return, t ≥ 2: `R_j,t = (Price_t × SplitFactor_t + DPS_t − Price_{t−1}) / Price_{t−1}` (col G). Verified on the split row 37: (26×1.5 − 57.75)/57.75 = −0.32468.
2. Market return: `R_m,t = (Index_t − Index_{t−1}) / Index_{t−1}` (col H). (No dividends on the index.)
3. Cols I, J, K accumulate regression sums. I = (R_j,t − R̄_j)². J = (R_m,t − R̄_m)². K = (R_j,t − R̄_j)(R_m,t − R̄_m). Here R̄ are sample means over the included returns (rows 5–56, giving 52 return observations from 53 price observations).
4. Beta (D68): `β = ΣK / ΣJ` = 1.77881 (OLS slope).
5. Alpha/intercept (D67): `α = R̄_j − β·R̄_m` = −0.0044722.
6. Per-period riskfree during period: `rf_p = (1 + G2)^(1/12) − 1` (geometric de-annualization; 12 ⇒ monthly data) (inferred from D69). `Rf(1−β)` (D69) = rf_p × (1 − β) = −0.0037909.
7. Jensen's alpha per period (D70): `α − rf_p(1−β)` = −0.0006813. (Positive ⇒ outperformed CAPM expectation.)
8. Variance statistics. Var(stock) D73 = sample variance of R_j = ΣI/(n−1) = 0.0191105. Var(market) D74 = ΣJ/(n−1) = 0.0027799. Systematic variance D75 = β²·Var(market) = 0.0087961. Unsystematic variance D76 = Var(stock) − systematic = 0.0103144. R² D77 = systematic/total = 0.46028.
9. Expected return (D84): `E(R) = C1 + β × G1` = 0.065 + 1.77881×0.055 = 0.16283 (uses CURRENT riskfree C1 and premium G1; D82/D83 echo those inputs).
10. Predicted prices (D90:D94): compound at the expected return, net of dividends. `P_1 = P_0 × (1 + E(R)) − DPS_annual`. Each later year: `P_{t+1} = P_t × (1 + E(R)) − DPS_annual` (inferred). With DPS = 0 here it is exactly 35 × 1.16283^t. Years 1–5: 40.699, 47.326, 55.033, 63.994, 74.414.

**Reference data:** none (the 60 rows of price/index history are example data, not a lookup table).

**Outputs:**

| Cell | Meaning | Current value |
|---|---|---|
| D67 | Intercept (alpha, per period) | −0.0044722 |
| D68 | Slope (beta) | 1.77881 |
| D69 | Rf(1−β), per period | −0.0037909 |
| D70 | Jensen's alpha = intercept − Rf(1−β), per period | −0.0006813 |
| D73 | Variance of the stock (per period) | 0.0191105 |
| D74 | Variance of the market | 0.0027799 |
| D75 | Systematic variance β²σ²_m | 0.0087961 |
| D76 | Unsystematic variance | 0.0103144 |
| D77 | R² | 0.46028 |
| D84 | CAPM expected return (annual) | 0.16283 |
| D90–D94 | Predicted prices years 1–5 | 40.699 / 47.326 / 55.033 / 63.994 / 74.414 |

**Worked example:** 53 monthly price observations (rows 4–56) → 52 return pairs. The stock fell from 30.75 with heavy swings, including a 1.5 split in period 34. The index rose 179.63 → 320.52. β = 1.779, α = −0.45%/month. The in-period riskfree rate is 6%/yr (0.487%/month). Jensen's alpha = −0.45% − 0.487%×(1−1.779) = −0.068%/month (slight underperformance). 46% of the stock's variance is market-driven. Forward-looking: E(R) = 6.5% + 1.779×5.5% = 16.28%; price forecast compounds 35 at 16.28%.

**Reimplementation notes:**
- Inputs: arrays price[t], dps[t] (default 0), split_factor[t] (default 1), index[t]; n_periods; current_rf, risk_premium, period_rf_annual, current_price, annual_dps; periods_per_year (12 here — needed to de-annualize rf: rf_p = (1+rf_annual)^(1/ppy) − 1).
- Outputs: beta, alpha, jensens_alpha_per_period, var_stock, var_market, systematic_var, unsystematic_var, r_squared, expected_return, predicted_prices[1..5].
- Edge cases: fewer than 3 return observations → regression undefined. Zero market variance → beta undefined. Missing DPS cells are 0. The split factor multiplies the END price of the period. Only the first n_periods rows enter the regression. Sample variance uses n−1.

---

### riskchecker.xls

Sheets: `Check numbers`, `Past T.Bill rates`, `Country Risk Premiums`, `Regional Risk Premiums`, `ERP calculator`.

**Purpose:** A companion "checker" for students/analysts running beta regressions (e.g., from Bloomberg). Given raw beta, its standard error, and the regression intercept, it reproduces the numbers you should get. Those are Jensen's alpha (per-period and annualized), beta confidence ranges, and the CAPM expected return. The reference sheets supply past riskfree rates by currency, plus Damodaran's January-update country and regional equity-risk-premium tables. The `ERP calculator` computes a revenue-weighted ERP for a multinational.

**Inputs — `Check numbers`:**

| Label | Cell | Example value |
|---|---|---|
| Weekly or monthly returns? ("W" or "M") | B2 | "W" |
| Current riskfree rate (today's 10-yr govt bond rate, right currency) | B3 | 0.0206 |
| Risk premium (historical, implied, or country-augmented; weighted avg if multi-country) | B4 | 0.0578 |
| Beta (raw) | B5 | 1.192 |
| Std error of beta | B6 | 0.076 |
| Intercept (Bloomberg pages report it in %, i.e. 0.05 means 0.05%) | B7 | 0.00078 |
| Past riskfree rate, annual (2-yr average from the T.Bill worksheet) | B8 | 0.0025 |

**Inputs — `ERP calculator`:** BY COUNTRY block (rows 7–16): country name (col A), revenues/earnings/assets (col B) — example: Argentina 19, Brazil 4, Chile 130, Honduras 23, Mexico 7, USA 6. BY REGION block (rows 24–33): region + amount — example: Caribbean 10, Financial Center 30, Middle East 35, North America 15, Western Europe 10. The ERP in col C is looked up from the country/regional tables (inferred).

**Logic (inferred; verified numerically):**

*Check numbers:*
1. Periods per year: `ppy = 52 if B2="W" else 12`.
2. Per-period past riskfree: `rf_p = B8 / ppy` (simple division, NOT geometric — verified: 0.0025/52 = 4.8077e−5).
3. `Rf(1−Beta)` (B11) = rf_p × (1 − B5) = 4.8077e−5 × (−0.192) = −9.2308e−6.
4. Jensen's alpha per period (B12) = B7 − B11 = 0.00078 − (−9.2308e−6) = 0.00078923.
5. Jensen's alpha annualized (B13) = (1 + B12)^ppy − 1 = 1.00078923^52 − 1 = 0.0418769.
6. 67% beta range (B14/C14) = B5 ± 1×B6 → [1.116, 1.268]. 95% range (B15/C15) = B5 ± 2×B6 → [1.04, 1.344]. (Upper bound in col B, lower in col C.)
7. Expected return (B16) = B3 + B5 × B4 = 0.0206 + 1.192×0.0578 = 0.0894976.

*ERP calculator:* weight_i = amount_i / Σ amounts; weighted ERP = Σ weight_i × ERP_i. Country ERPs come from `Country Risk Premiums` col E (rating-based total ERP); regional ERPs from `Regional Risk Premiums` col D (the weighted-average total ERP for the region — note the region table's col C/D labels are swapped relative to their contents, see below).

*Country Risk Premiums relationships (verified on every row):*
- Rating → default spread: fixed map (see table below, col "Default Spread").
- Country risk premium (col F) = default spread × 1.5 (the 1.5 is the assumed relative equity-to-bond volatility multiplier).
- Total equity risk premium (col E) = 0.058 + CRP, where 5.8% is the mature-market ERP.
- CDS-based (cols G–I): CRP_cds (col I) = (CDS_spread − 0.0067) × 1.5, where 0.0067 is the US CDS spread (netted out so the US CRP is 0); Total ERP_cds (col H) = 0.058 + CRP_cds. "NA" where no CDS trades.

**Reference data (verbatim):**

*`Past T.Bill rates` — average riskfree rate by currency:*

| Currency | Avg riskfree, last 2 years | Avg riskfree, last 5 years |
|---|---|---|
| US $ | 0.002 | 0.005 |
| Euro | 0.0025 | 0.006 |
| £ | 0.01 | 0.02 |
| Yen | 0.003 | 0.005 |
| Brazilian Real | 0.05 | 0.07 |
| Indian Rupee | 0.06 | 0.07 |
| Chinese Yuan | 0.03 | 0.04 |
| Swiss Franc | 0.005 | 0.0075 |

(If currency not listed, use 4% as the average riskfree rate.)

*Moody's local-currency rating → default spread (extracted from the country table; complete set of ratings that appear):*

| Rating | Default spread |
|---|---|
| Aaa | 0.0000 |
| Aa1 | 0.0025 |
| Aa2 | 0.0050 |
| Aa3 | 0.0070 |
| A1 | 0.0085 |
| A2 | 0.0100 |
| A3 | 0.0115 |
| Baa1 | 0.0150 |
| Baa2 | 0.0175 |
| Baa3 | 0.0200 |
| Ba1 | 0.0240 |
| Ba2 | 0.0275 |
| Ba3 | 0.0325 |
| B1 | 0.0400 |
| B2 | 0.0500 |
| B3 | 0.0600 |
| Caa1 | 0.0700 |
| Caa3 | 0.1000 |

*`Country Risk Premiums` (rows 3–120). Cols: Country | Region | Rating | Rating-based default spread | Total ERP | CRP | CDS spread | CDS Total ERP | CDS CRP. Mature-market ERP = 5.8%; CRP = spread × 1.5; CDS CRP = (CDS − 0.0067) × 1.5. Full table:*

| Country | Region | Rating | Dflt sprd | Total ERP | CRP | CDS sprd | CDS ERP | CDS CRP |
|---|---|---|---|---|---|---|---|---|
| Albania | Eastern Europe & Russia | B1 | 0.04 | 0.118 | 0.06 | NA | NA | NA |
| Angola | Africa | Ba3 | 0.0325 | 0.10675 | 0.04875 | NA | NA | NA |
| Argentina | Central and South America | B3 | 0.06 | 0.148 | 0.09 | 0.1307 | 0.244 | 0.186 |
| Armenia | Eastern Europe & Russia | Ba2 | 0.0275 | 0.09925 | 0.04125 | NA | NA | NA |
| Australia | Australia & New Zealand | Aaa | 0 | 0.058 | 0 | 0.0086 | 0.06085 | 0.00285 |
| Austria | Western Europe | Aaa | 0 | 0.058 | 0 | 0.0079 | 0.0598 | 0.0018 |
| Azerbaijan | Eastern Europe & Russia | Baa3 | 0.02 | 0.088 | 0.03 | NA | NA | NA |
| Bahamas | Caribbean | Baa1 | 0.015 | 0.0805 | 0.0225 | NA | NA | NA |
| Bahrain | Middle East | Baa1 | 0.015 | 0.0805 | 0.0225 | 0.0252 | 0.08575 | 0.02775 |
| Bangladesh | Asia | Ba3 | 0.0325 | 0.10675 | 0.04875 | NA | NA | NA |
| Barbados | Caribbean | Baa3 | 0.02 | 0.088 | 0.03 | NA | NA | NA |
| Belarus | Eastern Europe & Russia | B3 | 0.06 | 0.148 | 0.09 | NA | NA | NA |
| Belgium | Western Europe | Aa3 | 0.007 | 0.0685 | 0.0105 | 0.0124 | 0.06655 | 0.00855 |
| Belize | Central and South America | Caa3 | 0.10 | 0.208 | 0.15 | NA | NA | NA |
| Bermuda | Caribbean | Aa2 | 0.005 | 0.0655 | 0.0075 | NA | NA | NA |
| Bolivia | Central and South America | Ba3 | 0.0325 | 0.10675 | 0.04875 | NA | NA | NA |
| Bosnia and Herzegovina | Eastern Europe & Russia | B3 | 0.06 | 0.148 | 0.09 | NA | NA | NA |
| Botswana | Africa | A2 | 0.01 | 0.073 | 0.015 | NA | NA | NA |
| Brazil | Central and South America | Baa2 | 0.0175 | 0.08425 | 0.02625 | 0.0144 | 0.06955 | 0.01155 |
| Bulgaria | Eastern Europe & Russia | Baa2 | 0.0175 | 0.08425 | 0.02625 | 0.0141 | 0.0691 | 0.0111 |
| Cambodia | Asia | B2 | 0.05 | 0.133 | 0.075 | NA | NA | NA |
| Canada | North America | Aaa | 0 | 0.058 | 0 | NA | NA | NA |
| Cayman Islands | Caribbean | Aa3 | 0.007 | 0.0685 | 0.0105 | NA | NA | NA |
| Chile | Central and South America | Aa3 | 0.007 | 0.0685 | 0.0105 | 0.0099 | 0.0628 | 0.0048 |
| China | Asia | Aa3 | 0.007 | 0.0685 | 0.0105 | 0.0102 | 0.06325 | 0.00525 |
| Colombia | Central and South America | Baa3 | 0.02 | 0.088 | 0.03 | 0.0135 | 0.0682 | 0.0102 |
| Costa Rica | Central and South America | Baa3 | 0.02 | 0.088 | 0.03 | 0.0391 | 0.1066 | 0.0486 |
| Croatia | Eastern Europe & Russia | Baa3 | 0.02 | 0.088 | 0.03 | 0.0299 | 0.0928 | 0.0348 |
| Cuba | Caribbean | Caa1 | 0.07 | 0.163 | 0.105 | NA | NA | NA |
| Cyprus | Western Europe | B3 | 0.06 | 0.148 | 0.09 | 0.0655 | 0.1462 | 0.0882 |
| Czech Republic | Eastern Europe & Russia | A1 | 0.0085 | 0.07075 | 0.01275 | 0.0089 | 0.0613 | 0.0033 |
| Denmark | Western Europe | Aaa | 0 | 0.058 | 0 | 0.0069 | 0.0583 | 0.0003 |
| Dominican Republic | Caribbean | B1 | 0.04 | 0.118 | 0.06 | NA | NA | NA |
| Ecuador | Central and South America | Caa1 | 0.07 | 0.163 | 0.105 | NA | NA | NA |
| Egypt | Africa | B2 | 0.05 | 0.133 | 0.075 | 0.0576 | 0.13435 | 0.07635 |
| El Salvador | Central and South America | Ba3 | 0.0325 | 0.10675 | 0.04875 | NA | NA | NA |
| Estonia | Eastern Europe & Russia | A1 | 0.0085 | 0.07075 | 0.01275 | 0.0095 | 0.0622 | 0.0042 |
| Fiji Islands | Asia | B1 | 0.04 | 0.118 | 0.06 | NA | NA | NA |
| Finland | Western Europe | Aaa | 0 | 0.058 | 0 | 0.006 | 0.05695 | -0.00105 |
| France | Western Europe | Aa1 | 0.0025 | 0.06175 | 0.00375 | 0.0144 | 0.06955 | 0.01155 |
| Georgia | Eastern Europe & Russia | Ba3 | 0.0325 | 0.10675 | 0.04875 | NA | NA | NA |
| Germany | Western Europe | Aaa | 0 | 0.058 | 0 | 0.0082 | 0.06025 | 0.00225 |
| Greece | Western Europe | Caa3 | 0.10 | 0.208 | 0.15 | NA | NA | NA |
| Guatemala | Central and South America | Ba1 | 0.024 | 0.094 | 0.036 | NA | NA | NA |
| Honduras | Central and South America | B2 | 0.05 | 0.133 | 0.075 | NA | NA | NA |
| Hong Kong | Asia | Aa1 | 0.0025 | 0.06175 | 0.00375 | 0.0103 | 0.0634 | 0.0054 |
| Hungary | Eastern Europe & Russia | Ba1 | 0.024 | 0.094 | 0.036 | 0.0316 | 0.09535 | 0.03735 |
| Iceland | Western Europe | Baa3 | 0.02 | 0.088 | 0.03 | 0.0216 | 0.08035 | 0.02235 |
| India | Asia | Baa3 | 0.02 | 0.088 | 0.03 | NA | NA | NA |
| Indonesia | Asia | Baa3 | 0.02 | 0.088 | 0.03 | 0.0181 | 0.0751 | 0.0171 |
| Ireland | Western Europe | Ba1 | 0.024 | 0.094 | 0.036 | 0.0254 | 0.08605 | 0.02805 |
| Isle of Man | Financial Center | Aaa | 0 | 0.058 | 0 | NA | NA | NA |
| Israel | Middle East | A1 | 0.0085 | 0.07075 | 0.01275 | 0.0161 | 0.0721 | 0.0141 |
| Italy | Western Europe | Baa2 | 0.0175 | 0.08425 | 0.02625 | 0.0303 | 0.0934 | 0.0354 |
| Jamaica | Caribbean | B3 | 0.06 | 0.148 | 0.09 | NA | NA | NA |
| Japan | Asia | Aa3 | 0.007 | 0.0685 | 0.0105 | 0.0132 | 0.06775 | 0.00975 |
| Jordan | Middle East | Ba2 | 0.0275 | 0.09925 | 0.04125 | NA | NA | NA |
| Kazakhstan | Eastern Europe & Russia | Baa2 | 0.0175 | 0.08425 | 0.02625 | 0.0197 | 0.0775 | 0.0195 |
| Kenya | Africa | B1 | 0.04 | 0.118 | 0.06 | NA | NA | NA |
| Korea | Asia | Aa3 | 0.007 | 0.0685 | 0.0105 | 0.0113 | 0.0649 | 0.0069 |
| Kuwait | Middle East | Aa2 | 0.005 | 0.0655 | 0.0075 | NA | NA | NA |
| Latvia | Eastern Europe & Russia | Baa3 | 0.02 | 0.088 | 0.03 | 0.017 | 0.07345 | 0.01545 |
| Lebanon | Middle East | B1 | 0.04 | 0.118 | 0.06 | 0.0472 | 0.11875 | 0.06075 |
| Lithuania | Eastern Europe & Russia | Baa1 | 0.015 | 0.0805 | 0.0225 | 0.0158 | 0.07165 | 0.01365 |
| Luxembourg | Western Europe | Aaa | 0 | 0.058 | 0 | NA | NA | NA |
| Macao | Asia | Aa3 | 0.007 | 0.0685 | 0.0105 | NA | NA | NA |
| Malaysia | Asia | A3 | 0.0115 | 0.07525 | 0.01725 | 0.0114 | 0.06505 | 0.00705 |
| Malta | Western Europe | A3 | 0.0115 | 0.07525 | 0.01725 | NA | NA | NA |
| Mauritius | Africa | Baa1 | 0.015 | 0.0805 | 0.0225 | NA | NA | NA |
| Mexico | Central and South America | Baa1 | 0.015 | 0.0805 | 0.0225 | 0.0136 | 0.06835 | 0.01035 |
| Moldova | Eastern Europe & Russia | B3 | 0.06 | 0.148 | 0.09 | NA | NA | NA |
| Mongolia | Asia | B1 | 0.04 | 0.118 | 0.06 | NA | NA | NA |
| Montenegro | Eastern Europe & Russia | Ba3 | 0.0325 | 0.10675 | 0.04875 | NA | NA | NA |
| Morocco | Africa | Ba1 | 0.024 | 0.094 | 0.036 | 0.0279 | 0.0898 | 0.0318 |
| Namibia | Africa | Baa3 | 0.02 | 0.088 | 0.03 | NA | NA | NA |
| Netherlands | Western Europe | Aaa | 0 | 0.058 | 0 | 0.0083 | 0.0604 | 0.0024 |
| New Zealand | Australia & New Zealand | Aaa | 0 | 0.058 | 0 | 0.0072 | 0.05875 | 0.00075 |
| Nicaragua | Central and South America | B3 | 0.06 | 0.148 | 0.09 | NA | NA | NA |
| Nigeria | Africa | Ba3 | 0.0325 | 0.10675 | 0.04875 | NA | NA | NA |
| Norway | Western Europe | Aaa | 0 | 0.058 | 0 | 0.0041 | 0.0541 | -0.0039 |
| Oman | Middle East | A1 | 0.0085 | 0.07075 | 0.01275 | NA | NA | NA |
| Pakistan | Asia | Caa1 | 0.07 | 0.163 | 0.105 | 0.079 | 0.16645 | 0.10845 |
| Panama | Central and South America | Baa2 | 0.0175 | 0.08425 | 0.02625 | 0.0136 | 0.06835 | 0.01035 |
| Papua New Guinea | Asia | B1 | 0.04 | 0.118 | 0.06 | NA | NA | NA |
| Paraguay | Central and South America | B1 | 0.04 | 0.118 | 0.06 | NA | NA | NA |
| Peru | Central and South America | Baa2 | 0.0175 | 0.08425 | 0.02625 | 0.0138 | 0.06865 | 0.01065 |
| Philippines | Asia | Ba1 | 0.024 | 0.094 | 0.036 | 0.0159 | 0.0718 | 0.0138 |
| Poland | Eastern Europe & Russia | A2 | 0.01 | 0.073 | 0.015 | 0.013 | 0.06745 | 0.00945 |
| Portugal | Western Europe | Ba3 | 0.0325 | 0.10675 | 0.04875 | 0.0493 | 0.1219 | 0.0639 |
| Qatar | Middle East | Aa2 | 0.005 | 0.0655 | 0.0075 | 0.0128 | 0.06715 | 0.00915 |
| Romania | Eastern Europe & Russia | Baa3 | 0.02 | 0.088 | 0.03 | 0.0281 | 0.0901 | 0.0321 |
| Russia | Eastern Europe & Russia | Baa1 | 0.015 | 0.0805 | 0.0225 | 0.0182 | 0.07525 | 0.01725 |
| Saudi Arabia | Middle East | Aa3 | 0.007 | 0.0685 | 0.0105 | 0.0078 | 0.05965 | 0.00165 |
| Senegal | Africa | B1 | 0.04 | 0.118 | 0.06 | NA | NA | NA |
| Singapore | Asia | Aaa | 0 | 0.058 | 0 | NA | NA | NA |
| Slovakia | Eastern Europe & Russia | A2 | 0.01 | 0.073 | 0.015 | 0.0142 | 0.06925 | 0.01125 |
| Slovenia | Eastern Europe & Russia | Baa2 | 0.0175 | 0.08425 | 0.02625 | 0.0259 | 0.0868 | 0.0288 |
| South Africa | Africa | Baa1 | 0.015 | 0.0805 | 0.0225 | 0.0203 | 0.0784 | 0.0204 |
| Spain | Western Europe | Baa3 | 0.02 | 0.088 | 0.03 | 0.0314 | 0.09505 | 0.03705 |
| Sri Lanka | Asia | B1 | 0.04 | 0.118 | 0.06 | NA | NA | NA |
| St. Maarten | Africa | Baa1 | 0.015 | 0.0805 | 0.0225 | NA | NA | NA |
| St. Vincent & the Grenadines | Caribbean | B2 | 0.05 | 0.133 | 0.075 | NA | NA | NA |
| Suriname | Caribbean | Ba3 | 0.0325 | 0.10675 | 0.04875 | NA | NA | NA |
| Sweden | Western Europe | Aaa | 0 | 0.058 | 0 | 0.0041 | 0.0541 | -0.0039 |
| Switzerland | Western Europe | Aaa | 0 | 0.058 | 0 | 0.0076 | 0.05935 | 0.00135 |
| Taiwan | Asia | Aa3 | 0.007 | 0.0685 | 0.0105 | NA | NA | NA |
| Thailand | Asia | Baa1 | 0.015 | 0.0805 | 0.0225 | 0.0143 | 0.0694 | 0.0114 |
| Trinidad and Tobago | Caribbean | Baa1 | 0.015 | 0.0805 | 0.0225 | NA | NA | NA |
| Tunisia | Africa | Baa3 | 0.02 | 0.088 | 0.03 | 0.0421 | 0.1111 | 0.0531 |
| Turkey | Western Europe | Ba1 | 0.024 | 0.094 | 0.036 | 0.0179 | 0.0748 | 0.0168 |
| Ukraine | Eastern Europe & Russia | B3 | 0.06 | 0.148 | 0.09 | 0.0651 | 0.1456 | 0.0876 |
| United Arab Emirates | Middle East | Aa2 | 0.005 | 0.0655 | 0.0075 | NA | NA | NA |
| United Kingdom | Western Europe | Aaa | 0 | 0.058 | 0 | 0.0074 | 0.05905 | 0.00105 |
| United States of America | North America | Aaa | 0 | 0.058 | 0 | 0.0067 | 0.058 | 0 |
| Uruguay | Central and South America | Baa3 | 0.02 | 0.088 | 0.03 | NA | NA | NA |
| Venezuela | Central and South America | B1 | 0.04 | 0.118 | 0.06 | 0.0655 | 0.1462 | 0.0882 |
| Vietnam | Asia | B2 | 0.05 | 0.133 | 0.075 | 0.0274 | 0.08905 | 0.03105 |
| Zambia | Africa | B1 | 0.04 | 0.118 | 0.06 | NA | NA | NA |

*`Regional Risk Premiums` (weighted averages of the country table). CAUTION: the header labels of cols C and D are swapped relative to their contents. Col C actually holds the weighted-average COUNTRY risk premium. Col D holds the weighted-average TOTAL ERP. Proof: col D = col C + 0.058 on every row. The Grand Total row alone follows the printed headers. Documented here with corrected semantics:*

| Region | Default spread (wtd avg) | CRP (wtd avg) [sheet col C] | Total ERP (wtd avg) [sheet col D] |
|---|---|---|---|
| Africa | 0.0285969 | 0.0428953 | 0.1008953 |
| Asia | 0.0103656 | 0.0155484 | 0.0735484 |
| Australia & New Zealand | 0 | 0 | 0.058 |
| Caribbean | 0.0451587 | 0.0677382 | 0.1257382 |
| Central and South America | 0.0225526 | 0.0338290 | 0.0918290 |
| Eastern Europe & Russia | 0.0178708 | 0.0268062 | 0.0848062 |
| Financial Center | 0 | 0 | 0.058 |
| Middle East | 0.0077189 | 0.0115783 | 0.0695783 |
| North America | 0 | 0 | 0.058 |
| Western Europe | 0.0074759 | 0.0112138 | 0.0692138 |
| Grand Total | 0.0233 | 0.093 (ERP) | 0.035 (CRP) |

**Outputs — `Check numbers`:** B11 Rf(1−β) = −9.2308e−6. B12 Jensen's alpha per period = 0.00078923. B13 annualized Jensen's alpha = 0.0418769. B14/C14 67% beta range = 1.268 / 1.116. B15/C15 95% range = 1.344 / 1.04. B16 expected return = 0.0894976.
**Outputs — `ERP calculator`:** E17 country-weighted ERP = 0.0847857. Its example amounts: Argentina 19, Brazil 4, Chile 130, Honduras 23, Mexico 7, USA 6; total 189. E34 region-weighted ERP = 0.0699476. Its example amounts: Caribbean 10, Financial Center 30, Middle East 35, North America 15, Western Europe 10; total 100.

**Worked example (Check numbers):** Weekly returns, beta 1.192 ± 0.076, intercept 0.00078, past annual T-bill 0.25% → weekly rf 0.000048077 → Rf(1−β) = −0.0000092 → weekly Jensen's α = 0.000789 → annualized (1.000789)^52 − 1 = 4.19%. 95% beta range 1.04–1.344. Expected return = 2.06% + 1.192 × 5.78% = 8.95%.

**Worked example (ERP by country):** Chile carries weight 130/189 = 0.688 at ERP 6.85%. Argentina: 0.1005 at 14.8%. Honduras: 0.1217 at 13.3%. Brazil: 0.0212 at 8.425%. Mexico: 0.037 at 8.05%. US: 0.0317 at 5.8%. Weighted ERP = 8.479%.

**Reimplementation notes:**
- Inputs (checker): frequency ∈ {"W","M"}; current_rf, risk_premium, beta, se_beta, intercept, past_rf_annual (all decimals). Outputs as listed. Per-period rf uses SIMPLE division by 52/12 (unlike risk.xls, which uses geometric); annualization of alpha is geometric.
- Constants for the ERP machinery: mature_market_erp = 0.058; equity_vol_multiplier = 1.5; us_cds = 0.0067; rating→spread map above. Formulas: CRP = spread×1.5; total ERP = 0.058 + CRP; CDS variant nets the US CDS first.
- ERP calculator: guard against zero total weight; countries not in the table have no ERP (require explicit input or raise); blank rows contribute 0.
- Edge cases: CDS columns can produce slightly negative CRPs (Finland, Norway, Sweden) — keep, don't clamp; "NA" CDS → fall back to rating-based numbers; preserve the regional-table column-swap correction noted above if reproducing the sheet exactly.

---

### returncalculator.xls

Sheets: `Input Sheet`, `Accounting Return Output`, ` Lease Converter- Last yr ` (note: leading/trailing spaces in the sheet name), `Lease converter- This yr`, `R&D Converter`.

**Purpose:** Computes accounting returns from financial statements: return on invested capital (ROIC), return on equity (ROE), and non-cash ROE. It applies Damodaran's standard adjustments. Operating leases are capitalized (converted to debt, with operating income restated). R&D can optionally be capitalized into an amortized research asset. Goodwill and cash are stripped from invested capital, with user-controlled partial add-backs. Used to judge whether a firm earns more than its cost of capital. Numbers in the sheet are an example large firm (values in millions).

**Inputs — `Input Sheet`:**

| Label | Cell | Example value |
|---|---|---|
| Operating Income (this year's income statement) | B2 | 27801 |
| Taxable Income | B3 | 25737 |
| Taxes Paid | B4 | 7981 |
| Net Income | B5 | 16999 |
| Interest income on cash (if available) | B6 | 187 |
| Interest expenses on debt | B7 | 2251 |
| Cash & Marketable Securities (previous year's balance sheet, asset side) | B10 | 6550 |
| Goodwill (previous year) | B11 | 20651 |
| Capitalize R&D? (Yes/No) | B12 | "No" |
| Short-term interest-bearing debt (previous year, liability side) | B15 | 4047 |
| Long-term interest-bearing debt (previous year) | B16 | 47079 |
| Shareholder Equity (previous year) | B17 | 71315 |
| Minority Interest (separate it if consolidated in equity) | B18 | 4446 |
| Operating lease commitments? (Yes/No) — if yes fill the lease converter with LAST year's commitments | B19 | "Yes" |
| Pre-tax cost of debt for converting leases | B20 | 0.0261 |
| Use effective tax rate for after-tax operating income? (Yes/No) | B24 | "Yes" |
| (computed) effective tax rate if Yes | B25 | 0.3100983 = TaxesPaid/TaxableIncome (inferred) |
| If No, tax rate to use | B26 | (blank) |
| Keep the "exclude goodwill" assumption? (Yes/No) | B29 | "Yes" |
| If No, portion of goodwill to leave in invested capital (%) | B30 | 0.5 |
| Keep the "net out cash" assumption? (Yes/No) | B33 | "No" |
| If No, portion of cash to leave in invested capital (%) | B34 | 0.2 |

**Inputs — lease converter sheets (identical structure, two copies: last year's commitments → beginning-of-year lease debt for the capital base; this year's commitments → end-of-year lease debt and this year's income adjustment):**

| Label | Cell | Last-yr value | This-yr value |
|---|---|---|---|
| Operating lease expense in current year | E7 | 2400 | 2600 |
| Commitments years 1–5 | B10:B14 | 1644, 1590, 1525, 1428, 1312 | 1722, 1598, 1480, 1384, 1246 |
| Commitment "6 and beyond" | B15 | 8916 | 9373 |
| Pre-tax cost of debt | C17 | 0.0261 | 0.0261 |
| Reported EBIT / Debt / Interest | D20/D21/D22 | 27801 / 51126 / 2251 | same |

**Inputs — `R&D Converter`:**

| Label | Cell | Example value |
|---|---|---|
| Amortization period for R&D (years, max 10; use lookup table) | F6 | 5 |
| Current year's R&D expense | F7 | 1771 |
| R&D expense years −1..−5 (as many years as the amortization period; the Year column auto-fills) | B11:B15 | 1678, 1529, 1367, 1267, 1205 |

**Logic (inferred; every number verified):**

*Lease converters (same algorithm as ratings.xls Operating Leases sheet):*
1. `n6 = ROUND(B15_lump / AVERAGE(commitments yrs 1–5), 0)` — last-yr: round(8916/1499.8) = 6; this-yr: round(9373/1486) = 6.
2. Annualized 6+ commitment = lump/n6 (1486; 1562.1667).
3. PV years 1–5 at kd; PV of 6+ block = annuity(lump/n6, n6 yrs, kd) × (1+kd)^−5.
4. Debt value of leases C34 = sum of PVs (last-yr 14134.785; this-yr 14446.505).
5. Depreciation on leased asset D39 = DebtValue/(5+n6) (last-yr 14134.785/11 = 1284.980; this-yr 14446.505/11 = 1313.319).
6. Adjustment to operating income D40 = CurrentLeaseExpense − Depreciation (last-yr 1115.020; this-yr 1286.681). (Add to reported EBIT.)

*R&D Converter:* with amortization period N and straight-line amortization:
1. Current year's R&D: unamortized fraction 1.0, unamortized value = expense (row 24).
2. Year −k (k = 1..N): unamortized fraction = (N−k)/N; unamortized value = expense × (N−k)/N; amortization this year = expense/N.
3. Value of research asset D35 = Σ unamortized values = 1771 + 1342.4 + 917.4 + 546.8 + 253.4 = 4831.
4. Amortization for current year D37 = Σ (past-year expense / N) = (1678+1529+1367+1267+1205)/5 = 1409.2 (E35 shows the same total).
5. Adjustment to operating income D39 = CurrentR&D − Amortization = 1771 − 1409.2 = 361.8 (positive ⇒ add to reported EBIT).
6. Tax effect of R&D expensing D40 = 0.38 × D39 = 137.484 — the 0.38 marginal tax rate appears hardcoded (inferred; 137.484/361.8 = 0.38 exactly). This is the extra tax benefit the firm got from expensing R&D; it is added back to after-tax income ("+ Tax adjustment for R&D" rows in the output sheet).

*`Accounting Return Output` (ROIC block, col B):*
1. B2 stated operating income = Input B2 = 27801.
2. B3 adjustment for leases = This-yr converter D40 = 1286.681 (0 if B19 = "No").
3. B4 adjustment for R&D = R&D converter D39 if B12 = "Yes" else 0 (here 0).
4. B5 adjusted operating income = B2+B3+B4 = 29087.681.
5. B6 tax rate used = effective rate 0.3100983 (B24="Yes") else B26.
6. B7 after-tax operating income = B5 × (1 − B6) = 20067.641.
7. B8 tax adjustment for R&D = R&D converter D40 if capitalizing R&D else 0; B9 = B7 + B8 = 20067.641.
8. Capital base (all PREVIOUS-year balance sheet). B11 debt = 4047+47079 = 51126. B12 equity = 71315. B13 minority interests = 4446. B14 goodwill subtracted = 20651 (full, since B29 = "Yes"). B15 cash subtracted = 5240 = Cash × (1 − portion kept) = 6550 × 0.8 (inferred). That 0.8 follows from B33 = "No" and B34 = 0.2. If B33 = "Yes", the full 6550 would be subtracted.
9. B16 invested capital = B11 + B12 + B13 − B14 − B15 = 100996.
10. B17 capitalized leases = LAST-yr converter C34 = 14134.785 (beginning-of-period lease debt matches the beginning-of-period capital base).
11. B18 capitalized R&D = research-asset value (0 here; 4831 if capitalizing).
12. B19 goodwill add-back = Goodwill × B30 if B29 = "No" else 0 (here 0).
13. B20 cash add-back = Cash × B34 if B33 = "No" else 0 = 1310. CAUTION (observed quirk, likely a sheet bug): since B15 already subtracted only 80% of cash, adding back another 1310 leaves 2×20% = 40% of cash in adjusted invested capital. A faithful port must reproduce B15 = 5240 and B20 = +1310 to match the sheet.
14. B21 adjusted invested capital = B16 + B17 + B18 + B19 + B20 = 116440.785.
15. B23 ROIC = after-tax operating income (unadjusted: stated EBIT × (1−t) = 27801 × 0.6899017) / invested capital = 19180.257/100996 = 0.1899081. (Verified: uses UNADJUSTED after-tax EBIT over unadjusted capital.)
16. B24 adjusted ROIC = B9 / B21 = 20067.641/116440.785 = 0.1723420.

*ROE block (col B, rows 27–41):* Net income 16999 (+R&D adjustment + tax adjustment if capitalizing, here 0) = adjusted net income 16999. Book value of equity 71315 − goodwill 20651 = invested equity 50664; + capitalized R&D + goodwill add-back = adjusted book equity 50664. ROE B40 = 16999/50664 = 0.3355242; adjusted ROE B41 = adjusted NI/adjusted equity = 0.3355242. (No cash adjustment in this block.)

*Non-cash ROE block (cols F/I, rows 27–44):* I28 after-tax interest income on cash = 187 × (1 − 0.3100983) = 129.0116; I29 non-cash net income = 16999 − 129.0116 = 16869.988; (+R&D adjustments = 0) → I32 adjusted NI. Equity: 71315 − goodwill 20651 − cash 5240 = I37 45424; + capitalized R&D + goodwill add-back + cash add-back 1310 → I41 46734. I43 non-cash ROE = 16869.988/45424 = 0.3713893; I44 adjusted non-cash ROE = 16869.988/46734 = 0.3609789. (The same 80%-cash quirk applies: 5240 out, 1310 back.)

**Reference data (verbatim) — R&D amortization period by industry (`R&D Converter` A44:B142), plus the rule-of-thumb table (D46:F51):**

Rule of thumb: Non-technological Service — 2 years; Retail, Tech Service — 3 years; Light Manufacturing — 5 years; Heavy Manufacturing — 10 years; Research with Patenting — 10 years; Long Gestation Period — 10 years.

| Industry | Years | | Industry | Years |
|---|---|---|---|---|
| Advertising | 2 | | Insurance (Prop/Casualty) | 3 |
| Aerospace/Defense | 10 | | Internet | 3 |
| Air Transport | 10 | | Investment Co. (Domestic) | 3 |
| Aluminum | 5 | | Investment Co. (Foreign) | 3 |
| Apparel | 3 | | Investment Co. (Income) | 3 |
| Auto & Truck | 10 | | Machinery | 10 |
| Auto Parts (OEM) | 5 | | Manuf. Housing/Rec Veh | 5 |
| Auto Parts (Replacement) | 5 | | Maritime | 10 |
| Bank | 2 | | Medical Services | 3 |
| Bank (Canadian) | 2 | | Medical Supplies | 5 |
| Bank (Foreign) | 2 | | Metal Fabricating | 10 |
| Bank (Midwest) | 2 | | Metals & Mining (Div.) | 5 |
| Beverage (Alcoholic) | 3 | | Natural Gas (Distrib.) | 10 |
| Beverage (Soft Drink) | 3 | | Natural Gas (Diversified) | 10 |
| Building Materials | 5 | | Newspaper | 3 |
| Cable TV | 10 | | Office Equip & Supplies | 5 |
| Canadian Energy | 10 | | Oilfield Services/Equip. | 5 |
| Cement & Aggregates | 10 | | Packaging & Container | 5 |
| Chemical (Basic) | 10 | | Paper & Forest Products | 10 |
| Chemical (Diversified) | 10 | | Petroleum (Integrated) | 5 |
| Chemical (Specialty) | 10 | | Petroleum (Producing) | 5 |
| Coal/Alternate Energy | 5 | | Precision Instrument | 5 |
| Computer & Peripherals | 5 | | Publishing | 3 |
| Computer Software & Svcs | 3 | | R.E.I.T. | 3 |
| Copper | 5 | | Railroad | 5 |
| Diversified Co. | 5 | | Recreation | 5 |
| Drug | 10 | | Restaurant | 2 |
| Drugstore | 3 | | Retail (Special Lines) | 2 |
| Educational Services | 3 | | Retail Building Supply | 2 |
| Electric Util. (Central) | 10 | | Retail Store | 2 |
| Electric Utility (East) | 10 | | Securities Brokerage | 2 |
| Electric Utility (West) | 10 | | Semiconductor | 5 |
| Electrical Equipment | 10 | | Semiconductor Cap Equip | 5 |
| Electronics | 5 | | Shoe | 3 |
| Entertainment | 3 | | Steel (General) | 5 |
| Environmental | 5 | | Steel (Integrated) | 5 |
| Financial Services | 2 | | Telecom. Equipment | 10 |
| Food Processing | 3 | | Telecom. Services | 5 |
| Food Wholesalers | 3 | | Textile | 5 |
| Foreign Electron/Entertn | 5 | | Thrift | 2 |
| Foreign Telecom. | 10 | | Tire & Rubber | 5 |
| Furn./Home Furnishings | 3 | | Tobacco | 5 |
| Gold/Silver Mining | 5 | | Toiletries/Cosmetics | 3 |
| Grocery | 2 | | Trucking/Transp. Leasing | 5 |
| Healthcare Info Systems | 3 | | Utility (Foreign) | 10 |
| Home Appliance | 5 | | Water Utility | 10 |
| Homebuilding | 5 | | | |
| Hotel/Gaming | 3 | | | |
| Household Products | 3 | | | |
| Industrial Services | 3 | | | |
| Insurance (Diversified) | 3 | | | |
| Insurance (Life) | 3 | | | |

**Outputs (`Accounting Return Output`):**

| Cell | Meaning | Current value |
|---|---|---|
| B23 | Return on invested capital (unadjusted) | 0.1899081 |
| B24 | Adjusted ROIC (leases/R&D/goodwill/cash adjustments) | 0.1723420 |
| B40 | Return on equity (goodwill-stripped) | 0.3355242 |
| B41 | Adjusted ROE | 0.3355242 |
| I43 | Non-cash ROE | 0.3713893 |
| I44 | Adjusted non-cash ROE | 0.3609789 |
| Lease conv. C34 | Debt value of leases (last yr / this yr) | 14134.785 / 14446.505 |
| R&D conv. D35 / D37 / D39 / D40 | Research asset / current amortization / OI adjustment / tax effect | 4831 / 1409.2 / 361.8 / 137.484 |

**Worked example:** EBIT 27801 + this-year lease adjustment 1286.68 = 29087.68; taxed at the effective rate 31.01% → 20067.64 after-tax. Capital (prior year): debt 51126 + equity 71315 + minority 4446 − goodwill 20651 − cash 5240 = 100996; + last-year lease debt 14134.78 + cash add-back 1310 = 116440.78. Adjusted ROIC = 20067.64/116440.78 = 17.23% (vs. unadjusted 18.99%). ROE = 16999/(71315−20651) = 33.55%. Non-cash: strip 187×(1−0.3101) = 129.01 of after-tax interest income and 5240 of cash (add back 1310) → 16869.99/46734 = 36.10% adjusted non-cash ROE.

**Reimplementation notes:**
- Inputs, income statement: operating_income, taxable_income, taxes_paid, net_income, interest_income_on_cash, interest_expense (floats, currency). Inputs, prior-year balance sheet: cash, goodwill, st_debt, lt_debt, equity, minority_interest. Flags: capitalize_rnd, has_leases, use_effective_tax_rate, exclude_goodwill, net_out_cash. Also: pre_tax_cost_of_debt; optional overrides (manual tax rate, goodwill_pct_kept, cash_pct_kept); two lease schedules (last-year and this-year commitments plus current lease expense each); R&D series (amort_period N ≤ 10, current expense, past N expenses newest-first).
- Shared lease function: `capitalize_leases(commitments_1_5, lump_6plus, lease_expense, kd) -> (debt_value, depreciation, oi_adjustment)` with n6 = round(lump/mean(first5)); guard mean = 0. Reused by ratings.xls too.
- R&D function returns (research_asset, amortization, oi_adjustment, tax_effect); tax_effect uses a marginal rate — the sheet hardcodes 0.38.
- Effective tax rate = taxes_paid/taxable_income; guard taxable_income ≤ 0 (negative earnings → fall back to marginal rate). Damodaran's note: marginal rate is more robust but understates returns.
- Timing convention: income adjustments use THIS year's lease converter; capital adjustments use LAST year's lease debt (beginning-of-period capital).
- Reproduce the cash quirk exactly if matching the sheet: cash subtracted = cash×(1−pct_kept) when net_out_cash="No", and pct_kept×cash is ALSO added back in the adjusted-capital step (net effect: 2×pct kept). A "corrected" implementation would subtract full cash then add back pct once — flag which behavior you implement.
- Unadjusted ROIC uses stated EBIT×(1−t)/unadjusted capital; adjusted ROIC uses fully adjusted numerator and denominator. ROE strips goodwill but not cash; non-cash ROE strips both cash and its after-tax interest income.
- Edge cases: zero/negative equity → ROE meaningless (return None/NaN); missing R&D history years → treat as 0; amortization period must be ≥ 1 and ≤ 10; lease sheet names contain stray spaces (` Lease Converter- Last yr `) if ever re-read programmatically.

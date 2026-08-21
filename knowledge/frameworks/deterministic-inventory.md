# Deterministic computation inventory

Every computation in this corpus that a script can perform, consolidated into **84 calculator modules (M01–M84)** organised into **17 stages (S0–S16)** and ordered by dependency. Judgment lives in the inputs; everything documented here is a pure function of named inputs plus versioned reference tables.

This is an operational document. A system can be built directly from it: each module below states its exact inputs (name/type/units), outputs, computation outline (formulas, branches, iteration), the reference tables it needs, edge cases, and one test vector drawn from a worked example in the corpus. Concept files are cited per module — go there for *why*; this document states only what is needed to *orchestrate* correctly.

---

## 0. Global conventions (bind these before any module runs)

| Rule | Statement |
|---|---|
| **R1 Units** | One currency and one scale (usually millions) for every monetary input in a run. Shares and options in the same scale so per-share output is currency-per-share. Rates always decimals (0.0785, never 7.85). Labels in the source spreadsheets sometimes say "(in percent)"; the stored values are decimals. |
| **R2 Currency consistency** | Cash flows, discount rate, growth rate and riskfree rate must all be in the same currency and the same nominal/real basis. Convert with M02, never by mixing. Switch to real terms when expected inflation ≥ 10%. |
| **R3 Claimholder matching** | Equity flows (dividends, FCFE, net income, ROE) → cost of equity. Firm flows (FCFF, EBIT(1−t), ROC) → cost of capital. Never cross. |
| **R4 Timing convention** | All annual cash flows are end-of-year unless a module says otherwise. Invested-capital denominators are **beginning-of-period**. Reinvestment is charged in the year revenue changes. |
| **R5 Adjust once** | Every adjustment (leases, R&D, cash, options, pensions, cross-holdings) is applied exactly once. If leases are capitalised, they appear in EBIT, depreciation, debt, invested capital and interest — and nowhere else. |
| **R6 Growth cap** | Nominal stable growth ≤ riskfree rate in the same currency (proxy for nominal economy growth). This is a hard validation, not a guideline. |
| **R7 Terminal solvency** | Every perpetuity requires `discount rate > growth rate`, strictly. Reject otherwise; do not clamp silently. |
| **R8 Lookup semantics** | Coverage/threshold tables are *range* lookups: pick the last row whose lower bound ≤ value (bisect on the ">" column). Name-keyed tables (country, industry, rating) must be **exact match** in a port — the sheets use approximate match on unsorted text and that is a bug to fix, not replicate (see D-quirks). |
| **R9 Vintage** | Every reference table is a dated artefact. Every run records `(table_name, vintage)`. Mixing a 2021 ERP with 2004 spreads is a validation failure. |
| **R10 Iteration** | Circular chains (registered in §18) are solved by damped fixed-point iteration: seed, iterate to `|Δ| < 1e-9` or 200 iterations, then error. Rating loops may 2-cycle between adjacent brackets; detect and take the worse rating (or dampen). |
| **R11 Faithful vs corrected** | Where a source spreadsheet contains a defect, both behaviours are implementable. Every such module carries a `faithful: bool` flag and the register in §19 lists them. Default `faithful=False` (corrected) except where matching a published number is the goal. |
| **R12 Guard, don't clamp** | Negative or zero denominators (EBIT, invested capital, book equity, revenues, sales-to-capital, ROE, ROC, correlation) raise rather than return a silently wrong number. |

**Stage dependency spine:**
`S0 primitives → S1 reference data → S2 base-year cleansing → S3 cost of debt → S4 cost of equity → S5 growth/tax/reinvestment → S6 cash flows → S7 DCF engines → S8 equity bridge → S9 distress → {S10 capital structure, S11 projects, S12 relative valuation, S13 private, S14 real options, S15 acquisitions, S16 payout/governance/narrative/deliverables}`

Everything from S10 onward consumes S0–S9 and may consume each other (S10 feeds S15's restructured value; S14 feeds S8's option drag; S12 feeds S4's bottom-up beta weights).

---

## Module index

| ID | Module | Stage | Depends on |
|---|---|---|---|
| M01 | `pv_kernel` | S0 | — |
| M02 | `rate_kernel` | S0 | M01 |
| M03 | `stats_kernel` | S0 | — |
| M04 | `normal_cdf` | S0 | — |
| M05 | `solver_kernel` | S0 | — |
| M06 | `country_risk_service` | S1 | — |
| M07 | `industry_averages_service` | S1 | — |
| M08 | `ratings_spread_service` | S1 | — |
| M09 | `rnd_life_service` | S1 | — |
| M10 | `misc_reference_service` | S1 | — |
| M11 | `ttm_builder` | S2 | — |
| M12 | `rnd_capitalizer` | S2 | M09 |
| M13 | `operating_lease_capitalizer` | S2 | M01, M20 |
| M14 | `earnings_normalizer` | S2 | M03, M07 |
| M15 | `statement_ratio_engine` | S2 | — |
| M16 | `accounting_returns_engine` | S2 | M12, M13, M32 |
| M17 | `private_statement_cleanup` | S2 | M01, M13 |
| M18 | `interest_coverage` | S3 | M13, M14 |
| M19 | `synthetic_rating` | S3 | M08, M18 |
| M20 | `cost_of_debt_router` | S3 | M06, M08, M19, M23 |
| M21 | `debt_market_value` | S3 | M01, M20 |
| M22 | `lease_rating_fixpoint` | S3 | M05, M13, M18, M19, M20 |
| M23 | `riskfree_builder` | S4 | M02, M06 |
| M24 | `erp_builder` | S4 | M06, M25 |
| M25 | `implied_erp_solver` | S4 | M01, M05 |
| M26 | `beta_engine` | S4 | M03, M07, M21 |
| M27 | `cost_of_equity_assembler` | S4 | M23, M24, M26, M02 |
| M28 | `wacc_assembler` | S4 | M20, M21, M27, M02 |
| M29 | `fundamental_growth` | S5 | M16 |
| M30 | `historical_growth` | S5 | M03 |
| M31 | `reinvestment_engine` | S5 | M12, M13 |
| M32 | `tax_engine` | S5 | M06 |
| M33 | `top_down_revenue_engine` | S5 | M31 |
| M34 | `terminal_value_engine` | S5 | M23, M28, M29 |
| M35 | `fcff_builder` | S6 | M31, M32 |
| M36 | `fcfe_builder` | S6 | M31, M32 |
| M37 | `dividend_capacity_builder` | S6 | M15, M36 |
| M38 | `stable_growth_valuator` | S7 | M34, M35, M36, M37 |
| M39 | `two_stage_engine` | S7 | M28, M34, M35, M36 |
| M40 | `three_stage_engine` | S7 | M39 |
| M41 | `n_stage_engine` | S7 | M32, M40 |
| M42 | `ginzu_simple_fcff_engine` | S7 | M12, M13, M28, M32, M33, M34, M46, M48 |
| M43 | `ginzu_full_fcff_engine` | S7 | M12, M13, M14, M22, M29, M34, M46 |
| M44 | `excess_return_engine` | S7 | M16, M28, M34 |
| M45 | `model_equivalence_tests` | S7 | M38–M44 |
| M46 | `employee_option_valuer` | S8 | M04, M05, M71 |
| M47 | `cross_holdings_and_nonoperating` | S8 | M07 |
| M48 | `failure_distress_adjuster` | S8 | M50 |
| M49 | `equity_bridge_and_per_share` | S8 | M21, M46, M47, M48 |
| M50 | `bond_implied_distress_probability` | S9 | M01, M05 |
| M51 | `equity_as_option_engine` | S9 | M03, M71 |
| M52 | `optimal_capital_structure_schedule` | S10 | M05, M19, M26, M28, M32 |
| M53 | `enhanced_coc_ibc` | S10 | M08, M52 |
| M54 | `apv_engine` | S10 | M08, M19, M32 |
| M55 | `recap_value_and_buyback_engine` | S10 | M26, M28, M52 |
| M56 | `downside_stress_and_rating_constraint` | S10 | M03, M52 |
| M57 | `debt_design_regressions` | S10 | M01, M03, M10 |
| M58 | `capital_budgeting_engine` | S11 | M01, M05, M28 |
| M59 | `decision_rules_toolkit` | S11 | M01, M05 |
| M60 | `equity_side_project_engine` | S11 | M01, M27 |
| M61 | `multiple_constructor` | S12 | M21, M46 |
| M62 | `intrinsic_multiple_deriver` | S12 | M29, M34 |
| M63 | `multiple_distribution_stats` | S12 | M03 |
| M64 | `regression_pricing_engine` | S12 | M03, M10 |
| M65 | `market_and_country_pe_engine` | S12 | M03, M25 |
| M66 | `sum_of_the_parts_engine` | S12 | M28, M39, M64, M49 |
| M67 | `private_cost_of_capital` | S13 | M19, M26, M28 |
| M68 | `illiquidity_discount_engine` | S13 | M10 |
| M69 | `control_and_minority_discount` | S13 | M74 |
| M70 | `ipo_and_vc_adjustments` | S13 | M27, M46, M49 |
| M71 | `black_scholes_engine` | S14 | M04 |
| M72 | `binomial_and_decision_tree_engine` | S14 | — |
| M73 | `real_option_mappers` | S14 | M01, M71, M72 |
| M74 | `control_value_engine` | S15 | M42/M43, M52 |
| M75 | `synergy_engine` | S15 | M01, M26, M28, M39 |
| M76 | `deal_arithmetic` | S15 | M61, M74, M75 |
| M77 | `payout_analyzer` | S16 | M27, M36 |
| M78 | `payout_benchmark_engine` | S16 | M10, M64 |
| M79 | `ex_dividend_and_clientele_engine` | S16 | M03 |
| M80 | `governance_arithmetic` | S16 | M03 |
| M81 | `narrative_consistency_screens` | S16 | M29, M34, M42 |
| M82 | `scenario_and_simulation_engine` | S16 | M05, M42 |
| M83 | `value_vs_price_engine` | S16 | M27, M49 |
| M84 | `model_selector_and_deliverable_assembler` | S16 | all |

---

## S0 — Primitives

### M01 `pv_kernel`
**Purpose.** All present/future value arithmetic. Every other module discounts through this one; nothing re-implements discounting.

**Inputs.** `cash_flows: list[float]` (currency, index = period, index 0 = today); `rate: float` or `rates: list[float]` (decimal per period); `n: int` (periods); `A: float` (level flow); `g: float` (growth, decimal); `m: int` (periods/year).

**Outputs.** `pv`, `fv`, `annuity_pv`, `annuity_fv`, `growing_annuity_pv`, `perpetuity_pv`, `growing_perpetuity_pv`, `pvaf`, `loan_payment`, `cumulative_discount_factors: list[float]`, `duration`.

**Computation.**
- `PV = CF_t/(1+r)^t`; `FV = CF_0*(1+r)^t`.
- Annuity: `PV = A*[1 − (1+r)^(−n)]/r`; `FV = A*[((1+r)^n − 1)/r]`; `PVAF(r,n) = [1 − (1+r)^(−n)]/r`.
- Growing annuity: `PV = A(1+g)*[1 − (1+g)^n/(1+r)^n]/(r−g)`. **Branch `g == r`:** `PV = n*A*(1+g)/(1+r)`.
- Perpetuity `A/r`; growing perpetuity `CF_1/(r−g)`, requires `r > g`.
- Amortising loan: `Payment = L*r/(1 − (1+r)^(−n))`; `Interest_t = Balance_{t−1}*r`; `Principal_t = Payment − Interest_t`.
- **Time-varying rates (mandatory whenever WACC or cost of equity moves by year):** `CDF_t = Π_{i=1..t} 1/(1+r_i)`, `PV_t = CF_t * CDF_t`. Never use `(1+r̄)^t`.
- Deferred annuity (used by lease and resource modules): `PV = A*[1−(1+r)^(−n)]/r / (1+r)^d` where `d` = deferral years.
- PV-weighted duration: `D = Σ t*PV(CF_t) / Σ PV(CF_t)`. Bond duration: `D = [Σ t*C_t/(1+r)^t + N*F/(1+r)^N] / [Σ C_t/(1+r)^t + F/(1+r)^N]`.

**Reference tables.** None.

**Edge cases.** `r ≤ 0` breaks annuity formulas (limit: `A*n`); `g = r` branch above; `r ≤ g` in any perpetuity → raise (R7); rate 0 in the deferred annuity → undiscounted `A*n`.

**Test vector.** Gulf Oil developed reserves: `A=915, r=0.125, n=10` → `PV = 915*(1 − 1.125^−10)/0.125 = 5,065.83`.

**Concepts.** concepts/finance-foundations/present-value-of-the-five-cash-flow-types.md, concepts/finance-foundations/time-value-of-money-and-discount-rates.md, concepts/project-returns/time-value-and-cash-flow-timing.md, concepts/capital-structure/project-duration-and-project-financing.md

---

### M02 `rate_kernel`
**Purpose.** Convert rates between compounding frequencies, between real and nominal, and between currencies. Also builds expected exchange-rate paths.

**Inputs.** `stated_rate, ear, m`; `nominal, real, inflation`; `rate_in_currency_A, infl_A, infl_B`; `spot_fx, infl_domestic, infl_foreign, horizon`; `r_domestic, r_foreign` (for interest-rate parity).

**Outputs.** `ear`, `stated`, `real_rate`, `nominal_rate`, `converted_rate`, `fx_path: list[float]`, `forward_rate`.

**Computation.**
- Discrete `EAR = (1+r/m)^m − 1`; continuous `EAR = e^r − 1`; inverse `r = m*[(1+EAR)^(1/m) − 1]`.
- Fisher exact: `(1+nominal) = (1+real)*(1+inflation)`. Approximation `nominal ≈ real + inflation` only for small values.
- Real cash flow: `Real CF_t = Nominal CF_t/(1+i)^t`.
- **Differential-inflation currency conversion (the canonical form, applies to ke, kd and WACC identically):** `rate_X = (1+rate_US)*(1+E[infl_X])/(1+E[infl_US]) − 1`.
- PPP exchange path: `FX_t = FX_0 * [(1+infl_foreign)/(1+infl_domestic)]^t`. Interest-rate parity: `F_t = S*[(1+r_dom)/(1+r_for)]^t`.
- Intrinsic riskfree rate: `= expected inflation + expected real GDP growth`; `Fed effect = actual 10-yr bond rate − intrinsic rate`; `market-implied inflation = nominal 10-yr − TIPS 10-yr`.

**Reference tables.** None (inflation forecasts are inputs).

**Edge cases.** Direction of the FX quote decides which inflation goes in the numerator — a `$/foreign` quote falling means the foreign currency depreciating. Negative riskfree rates are legal and must flow through untouched (they lower the growth cap in R6).

**Test vector.** ginzu-fcff-lambda per-share conversion: `145.47483 US$ × 2.05 (local/US$) = 298.22341` local.

**Concepts.** concepts/finance-foundations/compounding-frequency-and-effective-rates.md, concepts/finance-foundations/real-vs-nominal-conversion.md, concepts/finance-foundations/fisher-equation-and-intrinsic-riskfree-rate.md, concepts/finance-foundations/exchange-rate-forecasting-with-parity.md, concepts/cost-of-debt-capital/currency-conversion-of-discount-rates.md, concepts/dark-side-difficult/currency-consistency-and-invariance.md, concepts/project-returns/currency-and-inflation-consistency.md

---

### M03 `stats_kernel`
**Purpose.** All regressions, moments and distributional statistics. Betas, alphas, macro sensitivities, multiple regressions and sector fits all route through here.

**Inputs.** `y: list[float]`, `X: list[list[float]]` (or single `x`), `weights: list[float] | None` (WLS by market cap), `intercept: bool`, `periods_per_year: int`, `series: list[float]`.

**Outputs.** `slope(s)`, `intercept`, `std_errors`, `t_stats`, `r_squared`, `adj_r_squared`, `residuals`, `mean`, `median`, `stdev`, `variance`, `percentiles`, `correlation_matrix`, `cagr`.

**Computation.**
- OLS (`b = ΣK/ΣJ` in the univariate case where `K = Σ(y−ȳ)(x−x̄)`, `J = Σ(x−x̄)²`), plus WLS when weights supplied.
- `R² = systematic variance / total variance`; `systematic = β²·Var(market)`; `unsystematic = Var(stock) − systematic`. Sample variance uses `n−1`.
- Beta confidence: 67% = `β ± 1·SE`; 95% = `β ± 2·SE`. t-stat thresholds for keeping a regressor: **>2 good, 1–2 marginal, <1 drop**.
- Return construction with splits and dividends: `R_t = (P_t·SplitFactor_t + DPS_t − P_{t−1})/P_{t−1}`.
- Arithmetic mean vs geometric `(end/begin)^(1/n) − 1` (arithmetic ≥ geometric always; gap widens with volatility).
- Percentiles and median for skewed multiple distributions (mean >> median is the expected shape).
- Two-asset variance: `σ²_p = w1²σ1² + w2²σ2² + 2w1w2ρσ1σ2`.

**Reference tables.** None.

**Edge cases.** <3 observations → undefined. Zero market variance → beta undefined. Negative or zero base breaks CAGR — return `None` and flag rather than using the negative-base workarounds silently (M30 exposes those explicitly).

**Test vector.** risk.xls, 53 monthly price observations: `beta = 1.77881`, `intercept = −0.0044722`, `Var(stock) = 0.0191105`, `Var(market) = 0.0027799`, `systematic = 0.0087961`, `R² = 0.46028`.

**Concepts.** concepts/cost-of-equity/regression-beta.md, concepts/cost-of-equity/jensen-alpha.md, concepts/finance-foundations/diversification-and-the-mean-variance-framework.md, concepts/relative-valuation/multiple-distribution-statistics.md, concepts/deliverables-worked-examples/regression-performance-diagnostics.md

---

### M04 `normal_cdf`
**Purpose.** `N(d)`, the cumulative standard normal, required by every option module.

**Inputs.** `d: float`. **Outputs.** `N(d): float in (0,1)`.

**Computation.** Use a standard CDF implementation. The corpus also ships a lookup table from `d = −3.00` to `+3.00` in steps of 0.05 (e.g. `N(−3.00)=0.0013`, `N(0)=0.5000`, `N(1.00)=0.8413`, `N(3.00)=0.9987`); interpolate if reproducing hand-computed lecture numbers exactly.

**Edge cases.** Deep in/out of the money produce `N(d) → 1` or `0`; the option value then degenerates to intrinsic value — correct, not an error.

**Test vector.** `N(1.1362) = 0.8720`, `N(−0.8512) = 0.2076` (Avonex patent).

**Concepts.** concepts/real-options/black-scholes-model.md, concepts/finance-foundations/black-scholes-and-put-call-parity.md

---

### M05 `solver_kernel`
**Purpose.** The three numerical operations the corpus needs: 1-D root finding, fixed-point iteration for circular models, and grid argmin/argmax.

**Inputs.** `f: callable`, `bracket: (lo, hi)`, `x0`, `tol=1e-9`, `max_iter=200`, `damping: float`, `grid: list`.

**Outputs.** `root`, `fixed_point`, `converged: bool`, `iterations`, `argmin/argmax`.

**Computation.**
- Root find (Brent/bisection) for: IRR, YTM, implied ERP, bond-implied distress probability, breakeven growth, implied growth in a scenario grid.
- Fixed point for the circular chains registered in §18. Seed from the register, damp if oscillating, cap iterations, then raise.
- Grid search over a debt-ratio schedule (0%–90% in 10% steps) for `argmin WACC` or `argmax firm value`.

**Edge cases.** Multiple IRRs when the cash-flow stream changes sign more than once — return **all** roots and flag (the number of IRRs can equal the number of sign changes). No root in bracket → report the bound rather than an arbitrary value. Rating fixed points may 2-cycle between adjacent brackets: detect the cycle and take the worse rating.

**Test vector.** capbudg.xls stream (t=0 outflow −62,484 plus 10 years of NATCF with year-10 salvage) → `IRR = 0.2355393602386762`.

**Concepts.** concepts/project-returns/npv-vs-irr-conflicts.md, concepts/cost-of-debt-capital/wacc-calculator-workflow.md, concepts/capital-structure/synthetic-rating-and-cost-of-debt.md

---

## S1 — Reference-data services

All four table services are **versioned lookups**, not computations. They exist as modules because the vintage choice is a first-class input (R9) and because the sheets' lookup semantics are a documented hazard (R8).

### M06 `country_risk_service`
**Purpose.** Country → sovereign rating, adjusted default spread, equity risk premium, country risk premium, corporate marginal tax rate. Plus regional aggregates.

**Inputs.** `country: str` (exact key), `vintage: str`, or `region: str`.

**Outputs.** `moodys_rating`, `adj_default_spread`, `erp`, `crp`, `corporate_tax_rate`, `mature_market_erp`.

**Computation.** Pure lookup, plus the two identities that hold in every vintage:
- `ERP_country = mature_market_ERP + CRP_country`
- `CRP = adjusted default spread × relative equity-market volatility multiplier`
Multiplier by vintage: **1.10 (Jan 2021)**, 1.18 (Jan 2020), 1.5 in the older `riskchecker` table, 1.1796 in the divginzu table. Mature-market ERP by vintage: **0.0424 (Jan 2022)**, **0.0472 (Jan 2021)**, **0.052 (Tesla/Jan-2021 DIY sheet)**, 0.0569 (divginzu), 0.058 (riskchecker).
CDS variant: `CRP_cds = (sovereign CDS − US CDS 0.0067) × 1.5`; `ERP_cds = 0.058 + CRP_cds`.
Weighted company ERP: `ERP_company = Σ w_i × ERP_i` with `w_i` = revenue (or production/asset) share; free "rest of world" rows accept a hand-entered ERP.

**Reference tables.** Country ERP table (~177 rows × {rating, adj default spread, ERP, CRP, tax rate}) per vintage; regional aggregate block (Africa, Asia, Australia & NZ, Caribbean, Central & South America, Eastern Europe & Russia, Middle East, North America, Western Europe, Global); rating → sovereign default spread map; `Past T.Bill rates` by currency (US$ 0.002/0.005, Euro 0.0025/0.006, £ 0.01/0.02, Yen 0.003/0.005, BRL 0.05/0.07, INR 0.06/0.07, CNY 0.03/0.04, CHF 0.005/0.0075; default 4% if absent).

**Edge cases.** Unrated countries appear with a numeric composite risk score in the rating column (e.g. `62.25`) — the spread is still populated. **Known sheet defect (see §19-Q3):** the synthetic-rating country lookup ranges stop short of the last alphabetical rows (`A5:C179` vs a 181-row table), returning a wrong spread for late-alphabet countries such as "United States". Use exact match. CDS-based CRPs can go slightly negative (Finland, Norway, Sweden) — keep, do not clamp.

**Test vector.** Jan-2022 vintage, `country="Chile"` → `adj_default_spread = 0.00598739`, `erp = 0.0493589` (= 0.0424 + 0.00695888).

**Concepts.** concepts/cost-of-equity/country-risk-premium.md, concepts/cost-of-equity/operation-weighted-erp.md, concepts/cost-of-debt-capital/country-risk-in-cost-of-debt.md, concepts/dark-side-difficult/country-risk-exposure.md

---

### M07 `industry_averages_service`
**Purpose.** Industry → the 26 companion statistics every bottom-up estimate and benchmark comparison needs.

**Inputs.** `industry: str` (exact key), `universe: "US" | "Global"`, `vintage: str`.

**Outputs.** `n_firms, revenue_growth_5y, pretax_operating_margin, after_tax_roc, effective_tax_rate, unlevered_beta, levered_beta, cost_of_equity, stddev_stock, pretax_cost_of_debt, market_debt_to_capital, cost_of_capital, sales_to_capital, ev_sales, ev_ebitda, ev_ebit, price_to_book, trailing_pe, noncash_wc_pct_rev, capex_pct_rev, net_capex_pct_rev, reinvestment_rate, roe, dividend_payout, equity_reinvestment_rate, pretax_margin_lease_rnd_adjusted`.

**Computation.** Lookup. Consumers and their column: bottom-up beta uses **unlevered beta (col 7)**; business-value weights use **EV/Sales (col 15)**; the earnings normaliser uses the pre-tax operating margin (col 4 unadjusted or col 26 lease/R&D-adjusted); benchmark blocks use cols 3, 4, 5, 10, 13, 14.
Value-weighted blend: `EstValue_i = Revenues_i × EV/Sales_i`; `β_u,firm = Σ β_u,i × EstValue_i / Σ EstValue_i`.

**Reference tables.** US and Global industry tables (94–95 industries + Total Market) per vintage. Older vintages carry a different column set (CapEx/Depreciation, reinvestment rate, NCWC/Sales, σ(equity)).

**Edge cases.** `NA` entries for banks/insurers/thrifts in margin, sales/capital, EV/EBITDA and NCWC columns — parse as `None`, never as 0. Degenerate rows exist and must be kept verbatim (Insurance Prop/Casualty CapEx/Dep 494.06, reinvestment 70.01). Truncated sheet labels (`"Insurance (Prop/Casualty"`, `"Natural Gas (Diversified"`) are the actual keys. **Known sheet defect (§19-Q4):** two comparison cells look up the *US* industry name in the *Global* table.

**Test vector.** Jan-2022 US, `industry="Aerospace/Defense"` → `unlevered_beta = 1.11041`, `ev_sales = 2.32655`, `sales_to_capital = 1.98483`.

**Concepts.** concepts/cost-of-equity/bottom-up-beta.md, concepts/relative-valuation/industry-average-multiples.md, concepts/dcf-cashflows-growth/net-capital-expenditures.md

---

### M08 `ratings_spread_service`
**Purpose.** All rating-related tables: coverage → rating → spread by firm type and vintage; rating → spread direct map; drop-in-EBITDA by rating and severity; bankruptcy probability by rating; cumulative default probability by rating and horizon.

**Inputs.** `coverage: float`, `firm_type: 1|2|3`, `vintage: str`, `rating: str`, `ibc_severity: "Low"|"Medium"|"High"`, `horizon_years: int`.

**Outputs.** `rating`, `default_spread`, `ebitda_drop`, `bankruptcy_probability`, `cumulative_default_probability`.

**Computation.** Range lookup per R8: last row whose lower bound ≤ coverage. Firm types: **1 = large manufacturing (market cap ≳ $5bn), 2 = smaller/riskier, 3 = financial service** (much lower coverage scale, long-term interest only).

Vintages that must all be shippable (spreads differ by a factor of 3 across them):

| Vintage | AAA | BBB | D |
|---|---|---|---|
| 2020 Ginzu (`ratings.xls`) | 0.006660321792834782 | 0.01591065804294902 | 0.14335607034015696 |
| Jan-2021 (Corona/Tesla sheets) | 0.0069 / 0.0063 | 0.0171 / 0.0156 | 0.1744 / 0.151164 |
| `wacccalc.xls` | 0.004 | 0.0175 | 0.12 |
| `normearn.xls` / legacy | 0.0075 | 0.0225 | 0.14 |
| `apv.xls` | 0.0054 | 0.0127 | 0.186025 |

Type-1 coverage brackets (2020 vintage): `(−100000, 0.199999] D2/D · (0.2, 0.649999] · (0.65, 0.799999] · (0.8, 1.249999] · (1.25, 1.499999] B3/B− · (1.5, 1.749999] B2/B · (1.75, 1.999999] B1/B+ · (2, 2.2499999] Ba2/BB · (2.25, 2.49999] Ba1/BB+ · (2.5, 2.999999] Baa2/BBB · (3, 4.249999] A3/A− · (4.25, 5.499999] A2/A · (5.5, 6.499999] A1/A+ · (6.5, 8.499999] Aa2/AA · (8.5, 100000] Aaa/AAA`. Type 2 shifts every threshold up (D2/D to 0.499999, AAA from 12.5). Type 3 (financial) uses a compressed scale (AAA from coverage 3.0; D below 0.049999).

Indirect-bankruptcy EBITDA drop by rating and severity (Low/Medium/High): `D2/D −0.30/−0.50/−1.00`; `Caa,Ca,C −0.25/−0.40/−0.50`; `B3 −0.15/−0.25/−0.30`; `B2,B1,Ba2,Ba1 −0.10/−0.20/−0.25`; `Baa2 −0.05/−0.10/−0.15`; `A3 0/−0.02/−0.05`; `A2 0/0/−0.02`; `A1, Aa2, Aaa 0/0/0`.

Bankruptcy probability by rating (apv.xls, **non-monotonic — reproduce verbatim**): `Aaa 0.0007, Aa2 0.0051, A1 0.006, A2 0.0066, A3 0.025, Baa2 0.0754, B2 0.368, B1 0.25, Ba2 0.1663, Ba1 0.10, Caa 0.5901, Ca2 0.70, C2 0.85, D2 1.00`.

Cumulative default probability (years 1–10): `AAA 0→0.0070; AA 0.0002→0.0072; A 0.0005→0.0124; BBB 0.0016→0.0332; BB 0.0061→0.1178; B 0.0333→0.2374; CCC/C 0.2708→0.5038`.

**Edge cases.** **Type 3 tables are empty in the Ginzu/Corona/Tesla workbooks** — either supply the financial-service table from `ratings.xls`/`fcffginzulambda` or raise. The direct rating→spread list is unsorted and, in three workbooks, has `C2/C` and `Caa/CCC` swapped relative to the coverage tables (§19-Q5) — use exact match on the rating string and pick which table is authoritative.

**Test vector.** `coverage = 4.94748, firm_type = 1, vintage = 2020` → `rating = "A2/A"`, `default_spread = 0.011379635520329143`.

**Concepts.** concepts/cost-of-debt-capital/synthetic-rating.md, concepts/cost-of-debt-capital/default-spreads-over-time.md, concepts/capital-structure/enhanced-cost-of-capital-approach.md, concepts/capital-structure/apv-approach.md

---

### M09 `rnd_life_service`
**Purpose.** Industry → R&D amortisable life, plus the six-category rule of thumb.

**Inputs.** `industry: str`. **Outputs.** `amortization_years: int (1–10)`.

**Computation.** Lookup over ~98 Value-Line industry names. Rule of thumb when the industry is absent: **Non-technological service 2; Retail / tech service 3; Light manufacturing 5; Heavy manufacturing 10; Research with patenting 10; Long gestation period 10.**

**Edge cases.** Life caps at 10 in every workbook that uses it (`R&DConv.xls` allows up to 20 by layout). The same table is reused for capitalising advertising/brand and recruiting/training spend.

**Test vector.** `"Drug" → 10`; `"Computer Software & Svcs" → 3`; `"Semiconductor" → 5`.

**Concepts.** concepts/dcf-cashflows-growth/rnd-capitalization.md, concepts/dark-side-difficult/capitalizing-rd.md

---

### M10 `misc_reference_service`
**Purpose.** Everything else the corpus ships as a table.

**Inputs.** `table_name: str`, key. **Outputs.** table row.

**Tables.**
- **Flotation costs** by issue size and security type (3.5% for equity issues above $50M rising to ~22% under $1M) — consumed by M79/M77.
- **Cap-ex/Depreciation ratios by sector** (`cpxest.xls`, 90 sectors): Depreciation, CapEx, CapEx/Dep, NetCapEx/Sales, NetCapEx/EBIT(1−t) — consumed by M31's stable-growth estimator.
- **Historical stock and T-bill returns** (US annual 1928–2020: S&P 500 total return, 3-month T-Bill, 10-yr T-Bond) — consumed by M24 and M77.
- **Illiquidity discount table** by revenue and profitability (5→1000 $m; profitable 0.2626→0.1579; unprofitable 0.3421→0.2542) — consumed by M68.
- **Sector macro sensitivity coefficients by SIC** (2-digit broad-industry and 4-digit tables: duration, cyclicality, inflation, currency) — consumed by M57.
- **Posted regression coefficient sets** (PE/PEG/PBV/EV-EBITDA/EV-Sales/EV-IC by region and vintage; sector regressions; country PE; E/P vs rates; payout/yield regressions; PEG log-growth; complexity PBV) — consumed by M64, M65, M78.
- **Multiple distribution percentiles** by market and vintage (US trailing PE Jan-2021: median 20.30, mean 103.25, 10th 7.68, 90th 96.80; % of firms with positive PE by region) — consumed by M63.
- **Sector survival / failure rates** by life-cycle stage — consumed by M48.

**Edge cases.** The sector macro tables carry sign conventions that differ between the 4-digit and 2-digit blocks (§19-Q9) — ship both verbatim and do not derive one from the other. The `cpxest` sector name set is **not** the same as the R&D-life set.

**Test vector.** `cpxest` `"Restaurant"` → `CapEx/Dep = 2.7233`, `NetCapEx/Sales = 0.0861`, `NetCapEx/EBIT(1−t) = 0.6376`.

**Concepts.** concepts/dividend-policy/bad-reasons-for-paying-dividends.md, concepts/dcf-cashflows-growth/net-capital-expenditures.md, concepts/cost-of-equity/historical-equity-risk-premium.md, concepts/asset-based-private/silber-restricted-stock-regression.md, concepts/capital-structure/macro-sensitivity-regressions.md

---

## S2 — Base-year cleansing

Order inside this stage is fixed: **M11 → (M12, M13) → M14 → M15/M16**. Leases and R&D must be capitalised before any coverage ratio, return or reinvestment number is computed, because they change EBIT, depreciation, debt, capex and invested capital simultaneously.

### M11 `ttm_builder`
**Purpose.** Build trailing-12-month flow items from the last annual filing plus two interim periods.

**Inputs.** For each line item: `last_10k: float`, `prior_year_ytd: float`, `current_year_ytd: float`. Balance-sheet items: `last_10k`, `most_recent` (point-in-time). Optional `years_since_last_10k: float` (e.g. 0.75, 1.25).

**Outputs.** `ttm_value` per flow line; `point_in_time` per stock line; `effective_tax_rate = taxes/pretax_income` per period; `annualised_recent_growth`.

**Computation.** `TTM = last_10k − prior_year_ytd + current_year_ytd`, applied identically to revenues, EBIT, interest expense, R&D, taxes, G&A, marketing. Balance-sheet items are **not** summed — take the most recent. `Annualised recent revenue growth = (Rev_now/Rev_last10k)^(1/years_since_last_10k) − 1` (guard `Rev_last10k > 0`, else `NA`).

**Reference tables.** None.

**Edge cases.** The two interim windows must cover the same number of months. Lease commitment schedules come from the last 10-K only. This is a staging step — in every source workbook it is a standalone sheet whose output is copied by hand into the model; a port should wire it directly.

**Test vector.** `Revenues: 5089 − 2242 + 3271 = 6118`; `EBIT: 538 − (−362) + 935 = 1835`; `Interest: 51 − 24 + 29 = 56`.

**Concepts.** concepts/dcf-cashflows-growth/reported-to-actual-earnings.md, concepts/narrative-numbers/landscape-survey.md

---

### M12 `rnd_capitalizer`
**Purpose.** Convert R&D (or advertising/training) from an expense into an amortised research asset, and restate every affected line.

**Inputs.** `life_years: int (1–10)`; `rnd_current: float`; `rnd_past: list[float]` ordered year −1 first, length = `life_years`; `marginal_tax_rate: float`; base-year `ebit`, `net_income`, `book_capital`, `capex`, `depreciation`.

**Outputs.** `research_asset`, `amortization_current`, `ebit_adjustment`, `tax_effect`, `adjusted_ebit`, `adjusted_after_tax_ebit`, `adjusted_net_income`, `adjusted_book_capital`, `adjusted_capex`, `adjusted_depreciation`, `adjusted_net_capex`, `adjusted_roc`.

**Computation.**
- Unamortised fraction for spending `k` years ago: `max(0, (life − k)/life)`; current year counts fully at 1.0.
- `Research asset RA = Σ_{k=0..life} RD_{−k} × (life − k)/life`.
- `Amortisation AM = Σ_{k=1..life} RD_{−k}/life` (current-year R&D is not amortised this year).
- `EBIT adjustment = RD_0 − AM` — **can be negative** for a shrinking R&D spender; that is correct.
- `Adjusted EBIT = EBIT + RD_0 − AM`; `Adjusted net income = NI + RD_0 − AM`.
- **`Adjusted after-tax operating income = EBIT×(1−t) + RD_0 − AM`. The add-back is NOT tax-effected** — the firm already took the deduction. This is the single most common porting error.
- `Adjusted book capital (and book equity) = book + RA`; `Adjusted capex = capex + RD_0`; `Adjusted D&A = D&A + AM`; `Adjusted net capex = net capex + RD_0 − AM`.
- `Tax effect = (RD_0 − AM) × marginal tax` — informational in most sheets; `returncalculator.xls` hardcodes 0.38 here (§19-Q6).

**Reference tables.** M09 for the life.

**Edge cases.** Missing prior years are treated as 0 (understates the asset — flag as a data-quality warning). `life = 1` degenerates to `RA = RD_0`. Year `−life` contributes 0 to the asset but `RD_{−life}/life` to amortisation — do not drop it.

**Test vector.** `life=5, RD_0=1594, past=[1026, 698, 399, 211, 89]` → `RA = 3035.4`, `AM = 484.6`, `EBIT adjustment = +1109.4`.

**Concepts.** concepts/dcf-cashflows-growth/rnd-capitalization.md, concepts/dark-side-difficult/capitalizing-rd.md, concepts/accounting-statements/expense-classification-and-depreciation.md

---

### M13 `operating_lease_capitalizer`
**Purpose.** Convert disclosed operating-lease commitments into a debt equivalent and restate EBIT, depreciation, debt and interest.

**Inputs.** `commitments: list[float]` years 1–5; `lump_beyond: float` (year 6 and beyond); `current_lease_expense: float`; `pretax_cost_of_debt: float`; `reported_ebit`, `reported_debt`, `reported_interest`.

**Outputs.** `n_beyond`, `annual_tail_payment`, `pv_by_year: list[float]`, `pv_tail`, `lease_debt`, `lease_life`, `lease_depreciation`, `ebit_adjustment_full`, `ebit_adjustment_shortcut`, `adjusted_debt`, `adjusted_interest`.

**Computation.**
1. `n_beyond = ROUND(lump / mean(commitments), 0)` — **Excel half-away-from-zero rounding**, not banker's rounding. `apv.xls` and `normearn.xls` use `INT()` truncation instead (§19-Q7); expose as a flag `tail_rule: "round"|"trunc"`.
2. `annual_tail = lump / n_beyond` (0 if `lump = 0` or `n_beyond = 0`).
3. `PV_t = commitment_t/(1+kd)^t` for t = 1..5.
4. `PV_tail = annual_tail × [1 − (1+kd)^(−n_beyond)]/kd / (1+kd)^5`; if `n_beyond = 0`, `PV_tail = lump/(1+kd)^6`.
5. `lease_debt = Σ PV_t + PV_tail`; `lease_life = 5 + n_beyond`; `lease_depreciation = lease_debt / lease_life`.
6. **Full method:** `adjusted EBIT = reported EBIT + current lease expense − lease depreciation`.
   **Short-cut method:** `adjusted EBIT = reported EBIT + kd × lease_debt` (imputed interest only). Both appear in the corpus; `oplease.xls` reports both, `apv.xls` adds the full lease expense with no depreciation subtraction. Expose `ebit_rule: "full"|"shortcut"|"full_expense"`.
7. `adjusted_debt = reported debt + lease_debt`; `adjusted_interest = reported interest + kd × lease_debt`; `adjusted_depreciation = reported depreciation + lease_depreciation`; `adjusted_capex += current lease expense` (Ginzu convention).

**Reference tables.** None. `kd` arrives from M20 and is circular — resolve in M22.

**Edge cases.** All five commitments zero → division by zero computing `n_beyond`; guard. Very large tails relative to near-term commitments (ground leases, airport gates) make the ROUND heuristic unreliable — flag. Post-IFRS-16/ASC-842 filings already report a lease liability; decide once whether to use it or recompute, never both (R5).

**Test vector.** `oplease.xls`: commitments `[2000, 2000, 2000, 1800, 1600]`, lump 8000, kd 0.0548 → `n_beyond = 4`, `annual_tail = 2000`, `lease_debt = 13,448.731193418043`, `lease_depreciation = 1,494.3034659353382`, `adjusted EBIT (shortcut) = 10,736.990469399308`, `adjusted EBIT (full) = 11,005.696534064662`, `adjusted debt = 38,448.73119341805`.

**Concepts.** concepts/cost-of-debt-capital/operating-leases-as-debt.md, concepts/dcf-cashflows-growth/operating-lease-capitalization.md, concepts/accounting-statements/liabilities-debt-and-leases.md, concepts/dcf-model-choice-loose-ends/defining-debt-for-cost-of-capital.md

---

### M14 `earnings_normalizer`
**Purpose.** Produce a usable EBIT (or net income) when the current year is negative, depressed or unrepresentative.

**Inputs.** `approach: 1|2|3`; `history: {revenues: list[float], ebit: list[float]}` (typically 5 years); `avg_ebit: float` (approach 1 direct); `avg_pretax_roc: float` (approach 2); `sector_margin: float` (approach 3); `current_revenues`, `bv_debt`, `bv_equity`; equity variants: `ni_history`, `normalized_roe`, `bv_equity_current`.

**Outputs.** `normalized_ebit`, `normalized_net_income`, `aggregate_margin`, `per_year_margins`.

**Computation.**
- **Approach 1 (dollar averaging):** `normalized EBIT = mean(EBIT over the cycle)`. Use when firm size has not changed much.
- **Approach 2 (return-based):** `normalized EBIT = average pre-tax ROC × current book capital`, `book capital = BV debt + BV equity`. Use when the firm has grown. Equity analogue: `normalized NI = average ROE × current book equity`.
- **Approach 3 (margin-based):** `normalized EBIT = sector (or own aggregate) pre-tax operating margin × current revenues`.
- Own aggregate margin: `Σ EBIT / Σ Revenues` over the window — a **ratio of sums**, not a mean of ratios.
- Excel `AVERAGE` semantics: blank years are skipped, so a 3-year history averages 3 values.

**Reference tables.** M07 for the sector margin.

**Edge cases.** All three approaches can still yield EBIT ≤ 0 for a deeply troubled firm — then abandon current earnings and route to M33 (revenue-driven forecasting). Approach 2's capital base is *current* book capital in the sheets (unverified branch in the Ginzu workbook — flag). Normalising changes the coverage ratio, so M18/M19 must re-run downstream.

**Test vector.** `normearn.xls` approach 3: revenues history `[2032,2376,2779,3155,3248]`, EBIT `[186,454,529,448,383]` → `aggregate margin = 2000/13590 = 0.14716703458425312`; `× current revenues 12,154 = 1,788.6681383370124`.

**Concepts.** concepts/dcf-cashflows-growth/normalizing-depressed-earnings.md, concepts/dark-side-difficult/normalized-earnings.md, concepts/accounting-statements/extraordinary-items-and-pro-forma-earnings.md, concepts/capital-structure/optimal-debt-ratio-by-firm-type.md

---

### M15 `statement_ratio_engine`
**Purpose.** The whole deterministic ladder of the three financial statements: subtotals, reconciliation ties, working capital, reinvestment, payout, quality-of-earnings.

**Inputs.** Income statement lines (`revenues, cogs, other_operating_expenses, financial_expenses, taxes, nci, shares_basic, shares_diluted, oci`); balance-sheet lines (current assets/liabilities detail, cash, debt tranches with rates and maturities, goodwill, intangibles, equity components); cash-flow lines (CFO components, investing lines, financing lines).

**Outputs.** `gross_profit, ebit, pretax_income, net_income, eps_basic, eps_diluted, comprehensive_income, net_income_to_parent`; `cfo, cfi, cff, net_change_in_cash`; `noncash_working_capital`, `change_in_ncwc`, `wc_to_revenue`; `net_operating_reinvestment`, `net_capex`, `reinvestment_rate`; `net_debt_issued`, `cash_returned`, `payout_ratio`, `augmented_payout_ratio`; `fcfe_predebt`, `fcfe_after_debt`, `payout_gap`; `qoe_ratio`, `accruals`; `six_ties: dict[str,bool]`; `total_debt`, `weighted_avg_interest_rate`, `weighted_avg_maturity`, `refinancing_share`; `book_value_per_share`, `equity_rollforward_residual`; `segment_margins`, `segment_roc`, `revenue_weights_by_region`; `sign_triple`, `asset_age_ratio`.

**Computation.**
- Income ladder: `Gross = Rev − COGS`; `EBIT = Gross − other opex`; `Pretax = EBIT − financial expenses`; `NI = Pretax − taxes`; `NI to parent = consolidated NI − NCI`; `EPS = NI to common / weighted shares`; `Comprehensive = NI + OCI`.
- `CFO = NI + D&A + other non-cash ± Δ(AR, Inventory, other CA, AP, taxes due)`; `Net change in cash = CFO + CFI + CFF (+ FX effect)`.
- `NCWC = non-cash current assets − non-debt current liabilities` (exclude cash & marketable securities; exclude short-term debt and current portion of LTD). **The debt reclassification must happen first.** `Effect on CFO = −ΔNCWC`. `w = NCWC/Revenues`.
- `Net operating reinvestment = capex − operating divestitures + cash acquisitions`; `Net capex = capex − D&A`; `Reinvestment rate = net operating reinvestment / EBIT(1−t)`.
- `CFF = debt raised − debt repaid + new equity − dividends − buybacks`; `Net debt issued = raised − repaid`; `Cash returned = dividends + buybacks`; `Payout = dividends/NI`; `Augmented payout = (dividends+buybacks)/NI`.
- `FCFE before debt = CFO − capex + divestitures − cash acquisitions`; `FCFE after debt = + debt raised − debt repaid`; `Payout gap = FCFE after debt − cash returned`.
- `Cash flow = Earnings + non-cash expenses − capex − ΔNCWC`; `QoE = CFO/NI`; `Accruals = NI − CFO`.
- **Six reconciliation ties** (assert all): balance-sheet identity `A = L + E`; income statement net income ties to the CFO starting line; retained-earnings roll-forward `RE_end = RE_begin + NI − dividends − buyback charges`; D&A on the income statement ties to the cash-flow add-back; ending cash ties to the balance sheet; segment revenues plus eliminations tie to consolidated revenue.
- Debt statistics: `Total debt = LTD + ST interest-bearing + current portion + lease debt`; `weighted avg rate = Σ(amount×rate)/Σ amount`; `refinancing pressure = debt due in next N years / total debt`.
- Equity: `SE = paid-in + retained earnings + AOCI − treasury`; roll-forward `E_end = E_begin + NI − dividends − buybacks + new equity + ΔAOCI` (report the residual).
- Life-cycle diagnostics: `sign triple = (sign CFO, sign CFI, sign CFF)`; `asset age = accumulated depreciation / gross PP&E`; `revenue growth`.
- Segment: `margin_i = segment EBIT_i / segment revenues_i`; `ROC_i ≈ segment EBIT_i / (identifiable assets_i + investments_i)`; `weight_i = segment revenue_i / consolidated revenue` (these weights feed M06/M24).

**Reference tables.** None.

**Edge cases.** Negative net income makes payout ratios meaningless (pass through, flag). Interest-bearing short-term borrowing left inside current liabilities corrupts NCWC and every downstream reinvestment number. Interest netted against interest income in the filing must be traced before the FCFF add-back.

**Test vector.** `dividends.xls` year 1: `FCFE_predebt = 6136 − (2796−2192) − (−133) = 5665`; `+ net debt issued 1881 → FCFE_actual = 7546`; `cash returned = 1324 + 4087 = 5411` → `cash/FCFE = 0.717`.

**Concepts.** concepts/accounting-statements/income-statement-structure.md, concepts/accounting-statements/cash-flow-statement-structure.md, concepts/accounting-statements/cash-flow-from-operations-and-working-capital.md, concepts/accounting-statements/investing-cash-flows-and-reinvestment.md, concepts/accounting-statements/financing-cash-flows-and-cash-returned.md, concepts/accounting-statements/potential-dividends-fcfe.md, concepts/accounting-statements/earnings-versus-cash-flows.md, concepts/accounting-statements/liabilities-debt-and-leases.md, concepts/accounting-statements/shareholders-equity-book-value.md, concepts/accounting-statements/segment-and-geographic-reporting.md, concepts/accounting-statements/role-of-accounting-and-three-statements.md, concepts/accounting-statements/life-cycle-patterns-in-financial-statements.md

---

### M16 `accounting_returns_engine`
**Purpose.** ROIC, ROE, non-cash ROE and EVA on both an unadjusted and a fully adjusted basis.

**Inputs.** `operating_income, taxable_income, taxes_paid, net_income, interest_income_on_cash, interest_expense`; prior-year balance sheet `cash, goodwill, st_debt, lt_debt, equity, minority_interest`; flags `capitalize_rnd, has_leases, use_effective_tax_rate, exclude_goodwill, net_out_cash`; overrides `manual_tax_rate, goodwill_pct_kept, cash_pct_kept`; lease outputs from M13 for **both** last year and this year; R&D outputs from M12; `cost_of_capital`, `cost_of_equity`.

**Outputs.** `effective_tax_rate, adjusted_operating_income, after_tax_operating_income, invested_capital, adjusted_invested_capital, roic, adjusted_roic, roe, adjusted_roe, noncash_roe, adjusted_noncash_roe, roc_spread, roe_spread, eva`.

**Computation.**
- `Effective tax rate = taxes paid / taxable income` (guard `taxable income ≤ 0`; fall back to marginal).
- `Adjusted operating income = stated EBIT + this-year lease adjustment + this-year R&D adjustment`.
- `After-tax operating income = adjusted EBIT × (1 − t)`; add the R&D tax adjustment when capitalising.
- `Invested capital = ST debt + LT debt + equity + minority interest − goodwill − cash` (all **prior-year**), then `+ last-year lease debt + research asset + goodwill add-back + cash add-back`.
- `ROIC = unadjusted after-tax EBIT / unadjusted invested capital`; `Adjusted ROIC = adjusted after-tax operating income / adjusted invested capital`.
- `ROE = NI / book equity`; `Non-cash ROE = (NI − after-tax interest income on cash) / (book equity − cash)`.
- `Return spread (firm) = ROC − WACC`; `(equity) = ROE − cost of equity`; `EVA = (ROC − WACC) × invested capital` (beginning-of-period).
- **Timing rule:** income adjustments use *this* year's lease converter; capital adjustments use *last* year's lease debt.

**Reference tables.** None.

**Edge cases.** Zero/negative book equity makes ROE meaningless — return `None`. Six standard ROIC distortions (write-offs, goodwill, stale book values, leases, R&D, life-cycle position) are corrected by the flags above; each correction is applied once. **Known sheet defect (§19-Q6):** when `net_out_cash="No"`, `returncalculator.xls` subtracts `cash×(1−pct_kept)` *and* adds back `pct_kept×cash`, leaving 2× the kept fraction in adjusted capital.

**Test vector.** `returncalculator.xls`: `ROIC = 0.1899081`, `adjusted ROIC = 0.1723420`, `ROE = 0.3355242`, `non-cash ROE = 0.3713893`, `adjusted non-cash ROE = 0.3609789`.

**Concepts.** concepts/project-returns/accounting-returns-roc-roe-eva.md, concepts/dcf-cashflows-growth/return-on-invested-capital.md, concepts/deliverables-worked-examples/return-spread-and-eva-analysis.md, concepts/cost-of-debt-capital/hurdle-rate-choice.md

---

### M17 `private_statement_cleanup`
**Purpose.** Restate a private firm's statements: market salary for owner labour, personal expenses out, leases as debt, key-person haircut.

**Inputs.** `reported_operating_income, market_salary, salary_actually_paid, personal_expenses, lease_payment, lease_years_remaining, pretax_cost_of_debt, tax_rate, key_person_share k`.

**Outputs.** `adjusted_operating_income`, `lease_debt`, `imputed_interest`, `adjusted_taxable_income`, `adjusted_net_income`, `post_key_person_operating_income`.

**Computation.**
- `Adjusted OI = reported OI − (market salary − salary paid) + personal expenses added back`.
- `Lease debt = payment × [1 − (1+kd)^(−n)]/kd` (level annuity form) or M13 for a schedule.
- `Adjusted OI (after lease reclassification) = reported OI + lease expense − depreciation on the leased asset`; the packet's simplification adds back the full lease expense.
- `Imputed interest = kd × lease debt`; `Adjusted taxable income = adjusted OI − imputed interest`; `Adjusted NI = adjusted taxable income × (1 − t)`.
- **Key-person haircut, applied after the salary adjustment:** `Post-departure OI = adjusted OI × (1 − k)`. The salary adjustment prices the owner's *work*; `k` prices the owner's *pull*. Both, never one twice.

**Reference tables.** None (market salary is an input).

**Edge cases.** Lease debt feeds the coverage ratio, which sets the rating, which sets `kd`, which discounts the lease — circular (§18-C4). Short operating histories make the restated series unrepresentative; flag rather than extrapolate.

**Test vector.** No isolated numeric vector; the chain is exercised end-to-end in `private-to-private-valuation` (restaurant case) which terminates at **$453,880** after the illiquidity discount — assert the pipeline reproduces that.

**Concepts.** concepts/asset-based-private/private-company-statement-cleanup.md, concepts/asset-based-private/key-person-discount.md, concepts/asset-based-private/private-company-valuation-framework.md

---

## S3 — Cost of debt and the debt boundary

### M18 `interest_coverage`
**Purpose.** The coverage ratio that drives every synthetic rating, with the lease and normalisation adjustments already folded in.

**Inputs.** `ebit: float`, `interest_expense: float`, `lease_debt: float`, `lease_ebit_adjustment: float`, `pretax_cost_of_debt: float`, `has_leases: bool`, `normalize: bool`, `normalized_ebit: float`, `local_rate: float`, `us_rate: float`, `firm_is_financial: bool`.

**Outputs.** `coverage_ratio: float`, `ebit_used`, `interest_used`.

**Computation.**
- `EBIT_used = normalized EBIT (if normalising) else reported EBIT`, `+ lease EBIT adjustment` when leases are on.
- `Interest_used = reported interest + pretax_cost_of_debt × lease_debt` when leases are on. **Financial firms: long-term interest expense only.**
- `Coverage = EBIT_used / Interest_used`.
- **Sentinels (mandatory, they drive the table lookup):** `interest == 0 → 1,000,000` (forces the top rating); `EBIT < 0 → −100,000` (forces D). Some sheets use `10,000,000` for the zero-interest case — either works because both exceed the top bracket.
- Emerging-market scaling: `Coverage_adjusted = Coverage / k`, `k = local long-term rate / US long-term rate`. Apply before the lookup.

**Reference tables.** None directly.

**Edge cases.** A firm with no balance-sheet debt but material leases has `interest = lease expense` as the practical proxy (`normearn.xls` does exactly this). Coverage below −100,000 is unhandled by the tables — clamp to the first bucket.

**Test vector.** Caramba: `EBIT = 1337.925 + 263.342 (lease) = 1601.2675`; `interest = 255.258 + 1443.945 × 0.0473670 = 323.6534`; `coverage = 4.94748`.

**Concepts.** concepts/cost-of-debt-capital/interest-coverage-ratio.md, concepts/capital-structure/synthetic-rating-and-cost-of-debt.md

---

### M19 `synthetic_rating`
**Purpose.** Coverage → rating → company default spread.

**Inputs.** `coverage_ratio: float`, `firm_type: 1|2|3`, `vintage: str`.

**Outputs.** `rating: str`, `company_default_spread: float`, `ebitda_drop: float` (when the IBC table is in use), `bankruptcy_probability: float` (APV vintage).

**Computation.** `rating, spread = M08.lookup(coverage, firm_type, vintage)` under R8 semantics. Nothing else.

**Reference tables.** M08.

**Edge cases.** Firm type 3 missing in several workbooks (§19-Q2). The `d = 0` column of a debt-ratio schedule has infinite coverage and is hard-coded to the top rating in every sheet — reproduce that rather than dividing by zero.

**Test vector.** `ratings.xls`: `EBIT 50, interest 8, firm_type 2, rf 0.03` → `coverage 6.25` → `rating "A2/A"`, `spread 0.0118`.

**Concepts.** concepts/cost-of-debt-capital/synthetic-rating.md, concepts/cost-of-debt-capital/synthetic-vs-actual-rating.md

---

### M20 `cost_of_debt_router`
**Purpose.** Produce a pre-tax and after-tax cost of debt by one of four routes, with country risk and subsidy handled explicitly.

**Inputs.** `approach: "direct"|"actual_rating"|"synthetic"|"traded_bond_ytm"`; `direct_rate`; `actual_rating: str`; `bond_price, coupon, maturity, face` (YTM route); `riskfree_rate`; `country: str`, `lambda_country: float in [0,1]`, `country_risk_already_in_rating: bool`; `marginal_tax_rate`; subsidy inputs `subsidized_rate, face_amount, remaining_life, subsidy_discount_rate`.

**Outputs.** `pretax_cost_of_debt`, `after_tax_cost_of_debt`, `company_spread`, `country_spread_applied`, `subsidy_pv`.

**Computation.**
- Base: `pretax kd = riskfree + company default spread (+ λ × country default spread)`.
- `actual_rating` route: spread from the M08 rating→spread map (exact match).
- `synthetic` route: spread from M19; country spread from M06 col "adj default spread".
- `traded_bond_ytm` route: solve `price = coupon × PVAF(n, ytm) + face/(1+ytm)^n` for `ytm` via M05; `kd = ytm`; implied spread `= ytm − riskfree`.
- **Country-risk branch:** a *global*-scale rating already embeds sovereign risk → add nothing. A *local*-scale rating or an explicit build-up → add `λ × country default spread`. Getting this wrong double-counts or omits several percentage points.
- If the local government bond rate itself carries sovereign default risk, strip it before use as the riskfree rate (M23) — otherwise country risk enters twice.
- **After-tax:** `kd_AT = kd × (1 − marginal tax rate)`. Marginal, never effective. The interest tax shield lives here and nowhere else — it is never inside FCFF.
- **Subsidised debt:** use the *fair* rate in the WACC. Value the subsidy separately: `annual saving = (fair rate − subsidised rate) × face`; `subsidy PV = Σ after-tax annual saving / (1+r_subsidy)^t`; add to firm value.
- **Currency:** convert an existing kd across currencies with M02 rather than rebuilding.

**Reference tables.** M06 (country spreads), M08 (rating spreads).

**Edge cases.** Accounting cost of debt (`interest expense / book debt`) is **wrong** and must never be produced. Multiple agency ratings → use the median. Convertible and floating-rate bonds are excluded from the YTM route (straight bonds only).

**Test vector.** Caramba: `riskfree 0.03 + company spread 0.0113796 (A2/A) + Chile country spread 0.0059874 = 0.0473670`; `after-tax = 0.0473670 × (1 − 0.34) = 0.0312622`.

**Concepts.** concepts/cost-of-debt-capital/cost-of-debt-estimation-routes.md, concepts/cost-of-debt-capital/after-tax-cost-of-debt.md, concepts/cost-of-debt-capital/country-risk-in-cost-of-debt.md, concepts/cost-of-debt-capital/subsidized-debt.md, concepts/finance-foundations/default-risk-and-default-spreads.md, concepts/finance-foundations/bond-valuation-and-yield-to-maturity.md

---

### M21 `debt_market_value`
**Purpose.** Convert book debt to market value, split convertibles, price preferred, assemble the total debt claim and the capital weights.

**Inputs.** `book_debt, interest_expense, avg_maturity_years, pretax_cost_of_debt`; convertible `(book, interest, maturity, market_value)`; preferred `(shares, price, annual_dividend)`; `lease_debt`; `shares_outstanding, price_per_share`; `cash`; `convention: "gross"|"net"`; per-tranche schedule `[(amount, rate, maturity)]`.

**Outputs.** `mv_straight_debt`, `convertible_debt_portion`, `convertible_equity_portion`, `mv_preferred`, `cost_of_preferred`, `total_mv_debt`, `mv_equity`, `total_capital`, `weights: {equity, debt, preferred}`, `net_debt`, `weighted_avg_maturity`.

**Computation.**
- **Price total debt as one coupon bond:** `MV debt = interest expense × [1 − (1+kd)^(−M)]/kd + book debt/(1+kd)^M`. `M = weighted-average maturity = Σ(tranche amount/total)×tranche maturity`; **default M = 3 years** when the schedule is unavailable. `M = 0` collapses the formula to book value.
- **Convertible split:** straight-debt portion by the same bond formula on the convertible's own coupon/maturity **at the straight-bond rate**; `equity portion = market value of convertible − straight-debt portion` and goes into equity, not debt.
- **Preferred:** `cost = annual dividend / price`, **no (1−t) factor**; `MV preferred = shares × price`. If `PS/(D+E+PS) < 5%`, folding preferred into debt is acceptable.
- `Total debt for the weights = MV straight debt + straight-debt half of convertible + lease debt`.
- `MV equity = shares × price` (+ option value counted in equity in the Ginzu computed-debt-ratio branch).
- Weights = component / total capital.
- **Net-debt convention:** `net debt = total debt − cash`; if used anywhere (relevering beta), it must be used everywhere (weights), and cash is then *not* added back at the end of the valuation. Never mix.

**Reference tables.** None.

**Edge cases.** `kd = 0` breaks the annuity form. Interest expense that does not correspond to balance-sheet debt (mid-year issuance, capitalised interest, netted interest income) breaks the synthetic-bond assumption — flag. Net debt can be negative (cash > debt), producing a levered beta below the unlevered beta — legal.

**Test vector.** `wacccalc.xls`: `interest 56, book 1000, M = 3, kd 0.035` → `MV straight debt = 1,058.8344`; with lease debt 1,127.9205 → `total MV debt = 2,186.7549`; `MV equity = 2407 × 37.53 = 90,334.71`; `weights = 0.976365 / 0.023635 / 0`.

**Concepts.** concepts/cost-of-debt-capital/market-value-of-debt.md, concepts/cost-of-debt-capital/market-value-weights.md, concepts/cost-of-debt-capital/convertible-debt-decomposition.md, concepts/cost-of-debt-capital/preferred-stock-cost.md, concepts/cost-of-debt-capital/net-debt-vs-gross-debt.md, concepts/cost-of-debt-capital/what-counts-as-debt.md

---

### M22 `lease_rating_fixpoint`
**Purpose.** Resolve the corpus's most pervasive circularity: cost of debt → lease PV → adjusted EBIT and interest → coverage → rating → cost of debt.

**Inputs.** everything M13, M18, M19, M20 need, plus `seed_kd: float`, `tol`, `max_iter`, `damping`.

**Outputs.** converged `pretax_cost_of_debt`, `lease_debt`, `adjusted_ebit`, `adjusted_interest`, `coverage`, `rating`, `iterations`, `converged: bool`.

**Computation.**
```
kd ← seed (riskfree + a small spread, or the entered kd)
repeat:
    lease_debt, lease_ebit_adj ← M13(commitments, lump, lease_expense, kd)
    ebit_used, interest_used   ← M18(ebit, interest, lease_debt, lease_ebit_adj, kd, ...)
    rating, spread             ← M19(coverage, firm_type, vintage)
    kd_new                     ← M20(riskfree, spread, country_spread, λ)
    if |kd_new − kd| < tol: stop
    kd ← kd + damping × (kd_new − kd)
```
**Only runs when `approach = "synthetic"` AND leases are being capitalised.** With a direct or actual-rating cost of debt, the chain is acyclic and this module is a pass-through.

**Reference tables.** via M08.

**Edge cases.** 2-cycles between adjacent rating brackets: detect the repeat and take the worse rating (conservative) or increase damping. Excel runs ~100 iterations and settles arbitrarily — a port must be deterministic and say which convention it used.

**Test vector.** Caramba converges to `kd = 0.0473670`, `lease_debt = 1,443.945`, `coverage = 4.94748`, `rating = A2/A` — the fixed point is self-consistent: 0.0473670 discounts the leases that produce the 4.94748 coverage that returns the 0.0113796 spread that rebuilds 0.0473670.

**Concepts.** concepts/cost-of-debt-capital/wacc-calculator-workflow.md, concepts/cost-of-debt-capital/interest-coverage-ratio.md

---

## S4 — Cost of equity and cost of capital

### M23 `riskfree_builder`
**Purpose.** A riskfree rate in the currency of the cash flows.

**Inputs.** `currency`, `government_bond_rate`, `sovereign_rating`, `spread_route: "hard_currency_bond"|"cds"|"rating_table"`, `hard_currency_bond_rate, matching_treasury_rate`, `sovereign_cds, us_cds`, `expected_inflation_local, expected_inflation_us, riskfree_us`, `tips_rate`, `euro_sovereign_rates: list[float]`.

**Outputs.** `riskfree_rate`, `sovereign_default_spread`, `real_riskfree_rate`, `intrinsic_riskfree_rate`, `fed_effect`.

**Computation.**
- Default convention: **10-year government bond of a default-free (Aaa/AAA) issuer in that currency**.
- Multi-issuer currency (Euro): `riskfree = min(sovereign 10-year rates in that currency)`.
- Otherwise `riskfree = local government bond rate − sovereign default spread`, with the spread from one of three routes: (a) sovereign hard-currency bond rate − matching Treasury; (b) sovereign 10-yr CDS − US CDS; (c) rating-table lookup on the **local-currency** rating.
- Build-up: `riskfree = expected inflation + expected real rate`; fallback `real riskfree ≈ long-run real GDP growth` when no indexed bond exists.
- Differential inflation (M02) when a US$ rate is trusted more than the local bond market.
- Real analysis: `real riskfree = TIPS yield`.
- Diagnostics: `intrinsic riskfree = inflation + real GDP growth`; `Fed effect = actual 10-yr − intrinsic`.

**Reference tables.** M06 (rating → sovereign spread), M10 (past riskfree by currency for Jensen's alpha).

**Edge cases. Do not normalise a low or negative riskfree rate.** The course position is explicit: use today's rate, and keep growth and inflation assumptions consistent with it (R6 binds harder at low rates). Negative rates are legal throughout.

**Test vector.** Chile local build: `local bond rate − 0.00598739 (Chile adj default spread)`. In the Caramba run the analyst supplies `riskfree = 0.03` directly and the country spread is added to the *cost of debt* instead — either placement is valid, both is not.

**Concepts.** concepts/cost-of-equity/riskfree-rate-fundamentals.md, concepts/cost-of-equity/currency-riskfree-rate.md, concepts/cost-of-equity/riskfree-rate-normalization.md, concepts/finance-foundations/yield-curve-and-growth-signals.md

---

### M24 `erp_builder`
**Purpose.** An equity risk premium for the company, by any of the accepted routes, including geographic weighting.

**Inputs.** `approach: "direct"|"historical"|"implied"|"country_of_incorporation"|"operating_countries"|"operating_regions"`; `direct_erp`; historical `(stock_returns, riskless_returns, period, averaging: "arithmetic"|"geometric", riskless_instrument: "tbill"|"tbond")`; `mature_market_erp`; `country_weights: list[(name, revenue)]` or `region_weights`; free rows with hand-entered ERPs; `lambda: float`; `baa_spread` (cross-check).

**Outputs.** `erp_used`, `company_crp`, `standard_error`, `erp_to_baa_ratio`.

**Computation.**
- Historical: `ERP = mean(stock returns) − mean(riskless returns)` over the chosen window; `SE = annualised σ(stock returns)/√n` (e.g. 20%/√90 = 2.1%). Arithmetic ≥ geometric.
- Implied: delegate to M25 (this is the course default).
- Country: `ERP_country = mature ERP + CRP` (M06). Three CRP methods: raw default spread; relative equity volatility `ERP_US × (σ_country equity/σ_US equity)`; **melded (default)** `default spread × (σ country equity/σ country bond)`, the multiplier being a single number per vintage (1.10 in Jan-2021).
- Operation-weighted: `ERP_company = Σ w_i × ERP_i`, weights from revenues (or production, assets, operating income). The last two rows of each calculator accept a hand-entered "Rest of the World" ERP.
- Four attachment choices, which must be chosen once and stated: (1) `Rf + β×matureERP + CRP_incorporation`; (2) `Rf + β×matureERP + Σw_i CRP_i`; (3) `Rf + β×(matureERP + CRP_incorporation)`; (4) `Rf + β×(matureERP + Σw_i CRP_i)`; plus (5) the lambda form in M27.
- Cross-check: `ERP / Baa default spread` has a median of ~2.02 over 1960–2020.

**Reference tables.** M06, M10 (historical return series).

**Edge cases.** Mixing an ERP vintage with a spread vintage violates R9. Weighted ERPs need weights that sum to the total revenue base; a missing region silently under-weights risk.

**Test vector.** SK Innovation operating-regions blend: `Asia 0.2681, North America 0.0418, Western Europe 0.0518, South Korea free-row 0.6383 @ 0.052` → `ERP = 0.05174663`.

**Concepts.** concepts/cost-of-equity/equity-risk-premium-basics.md, concepts/cost-of-equity/historical-equity-risk-premium.md, concepts/cost-of-equity/choosing-an-equity-risk-premium.md, concepts/cost-of-equity/country-risk-premium.md, concepts/cost-of-equity/operation-weighted-erp.md

---

### M25 `implied_erp_solver`
**Purpose.** Back the forward-looking equity risk premium out of the current index level.

**Inputs.** `index_level: float`; `base_cash_flow: float` (trailing dividends **+ buybacks**, the "cash yield" measure) or `dividend_yield`; `growth_next_5y: float`; `terminal_growth: float` (set equal to the riskfree rate by convention); `riskfree_rate: float`; optional `payout_path: list[float]`, `earnings_path: list[float]`.

**Outputs.** `implied_expected_return r`, `implied_erp = r − riskfree`, `intrinsic_index_value(trial_premium)`.

**Computation.**
```
CF_t = CF_0 × (1 + g_high)^t          for t = 1..5      (or earnings×payout path)
TV_5 = CF_5 × (1 + g_terminal) / (r − g_terminal)
V(r) = Σ_{t=1..5} CF_t/(1+r)^t + TV_5/(1+r)^5
solve V(r) = index_level for r      (M05 root find)
implied ERP = r − riskfree
```
Bracket `r` in `(g_terminal + ε, g_terminal + 0.20]` — the terminal value is undefined below the lower bound.

**Reference tables.** None.

**Edge cases.** Zero cash yield → the premium is undefined (value is 0 for all r). Crisis years need a normalised base cash flow (the 2008 buyback haircut, the COVID earnings-recovery path) — that normalisation is judgment supplied as an input, not computed here.

**Test vector.** `implprem.xls`: index 1418.3, dividend yield 0.0375, `g_high` 0.06, bond rate 0.047, `g_terminal` 0.047 → `implied premium = 0.04157534555252903`; the reconstruction check returns 1418.2999996.

**Concepts.** concepts/cost-of-equity/implied-equity-risk-premium.md, concepts/relative-valuation/market-pe-vs-bond-alternative.md, concepts/dark-side-difficult/market-and-macro-crisis-valuation.md

---

### M26 `beta_engine`
**Purpose.** Every beta the corpus uses: regression, bottom-up, unlevered, relevered, cash-corrected, divisional, total, merged. Plus Jensen's alpha.

**Inputs.** Regression route: `stock_prices, dividends, split_factors, index_levels, n_periods, periods_per_year, past_riskfree_annual, riskfree_deannualisation: "simple"|"geometric"`. Bottom-up route: `businesses: list[(industry, revenues)]`, `universe`, `tax_rate`, `de_ratio`, `cash_to_firm_value`, `debt_beta`. Divisional: `identifiable_assets_by_division, total_debt`. Total beta: `average_r_squared` or `correlation`.

**Outputs.** `regression_beta, intercept, std_error, r_squared, jensens_alpha_period, jensens_alpha_annual, beta_67_range, beta_95_range, adjusted_beta, unlevered_beta, levered_beta, total_beta, divisional_betas, portfolio_beta, bottom_up_std_error`.

**Computation.**
- Regression `R_j = a + b·R_m` via M03; returns include dividends and split factors.
- `Jensen's alpha = a − Rf_period × (1 − β)`; `Rf_period = Rf_annual / periods_per_year` (simple, `riskchecker`) or `(1+Rf_annual)^(1/ppy) − 1` (geometric, `risk.xls`) — pick one and be consistent. `Annualised alpha = (1 + alpha_period)^ppy − 1`.
- `Bloomberg adjusted beta = 0.67 × raw + 0.33 × 1.0`.
- **Unlever:** `β_u = β_L / (1 + (1−t)·D/E)`. **Relever:** `β_L = β_u × (1 + (1−t)·D/E)`. Debt-beta variant: `β_L = β_u(1+(1−t)D/E) − β_debt(1−t)D/E`. Zero-tax variant `β_L = β_u(1 + D/E)` (MM check).
- **Cash correction:** `business β_u = company β_u / (1 − Cash/Firm value)`.
- **Bottom-up:** per business `β_u,i` from M07 col 7; `EstValue_i = Revenues_i × EV/Sales_i` (M07 col 15); `β_u,firm = Σ β_u,i × EstValue_i / Σ EstValue_i`; then relever at the firm's market D/E. `SE = mean(comparable SEs)/√n_firms`.
- **Divisional:** `allocated debt_i = total debt × (identifiable assets_i / total)`; `D/E_i = allocated debt_i/(division value_i − allocated debt_i)`; relever `β_u,i` at `D/E_i`.
- **Total beta** (undiversified owner): `β_total = β_market / ρ`, `ρ = √(average R² of comparables)`. Lever after dividing: `levered total β = (β_u/ρ)(1+(1−t)D/E)`.
- **Portfolio / merged firm:** value-weighted average of component betas.
- `D/E from a debt ratio d`: `D/E = d/(1−d)`.
- Non-traded firms: use the **median** comparable levered beta and the **median** comparable D/E, and assume the industry median market D/E going forward.

**Reference tables.** M07.

**Edge cases.** `ρ = 0` → total beta undefined (R12). A stock that dominates its own index produces a meaningless regression. Regression betas must be checked for company change inside the window. **Direct-input beta branch is ambiguous in the source workbooks** (§19-Q8) — the family convention is to treat a supplied regression beta as the *levered* beta and skip relevering; state the choice.

**Test vector.** `levbeta.xls`: `β = 1.4, t = 0.36, avg D/E = 0.14` → `β_u = 1.284875`; relever at `D/E = 12,142.263/50,889.038 = 0.238623` → `β_L = 1.481083`; at custom `D/E = 0.35` → `1.572687`.

**Concepts.** concepts/cost-of-equity/regression-beta.md, concepts/cost-of-equity/jensen-alpha.md, concepts/cost-of-equity/levering-and-unlevering-beta.md, concepts/cost-of-equity/bottom-up-beta.md, concepts/cost-of-equity/non-traded-asset-betas.md, concepts/cost-of-equity/total-beta.md, concepts/cost-of-equity/beta-determinants.md, concepts/capital-structure/levered-beta-schedule.md

---

### M27 `cost_of_equity_assembler`
**Purpose.** Combine riskfree rate, relative risk and premium into a cost of equity, under any country-risk attachment, in any currency.

**Inputs.** `riskfree_rate, beta (or total beta), erp, mature_erp, crp, lambda, attachment: 1..5, private_company_premium, direct_cost_of_equity`.

**Outputs.** `cost_of_equity`, `cost_of_equity_by_division`, `cost_of_equity_converted`.

**Computation.**
- CAPM: `ke = Rf + β × ERP`.
- Attachment variants (choose exactly one): `Rf + β·matureERP + CRP`; `Rf + β·(matureERP + CRP)`; `Rf + β·matureERP + Σw_i CRP_i`; `Rf + β·(matureERP + Σw_i CRP_i)`; **lambda:** `Rf + β·matureERP + λ·CRP`.
- Lambda estimation: revenue-based `λ = (firm % domestic revenue)/(average firm % domestic revenue)`; or the slope of `firm returns` on `sovereign bond returns`.
- Private-firm premium alternative (not preferred): `ke = Rf + levered *market* beta × ERP + flat private premium`.
- Currency conversion via M02: `ke_X = (1+ke_US)(1+infl_X)/(1+infl_US) − 1`. Cross-check by direct rebuild in the local currency; the two should agree.
- Multi-factor / APM forms: `ke = Rf + Σ β_j × premium_j`.

**Reference tables.** M06.

**Edge cases.** Attaching country risk in two places (inside the ERP *and* as an additive CRP) double-counts — R5. If the marginal investor is not diversified, switch to total beta (M67), not a bolt-on premium.

**Test vector.** ginzu-fcff-lambda: `ke = 0.05 + 1.5 × 0.06 + 0.25 × 0.0263 = 0.146575`; stable phase `0.05 + 1.2 × 0.06 + 0.25 × 0.008 = 0.124`.

**Concepts.** concepts/cost-of-equity/capm-cost-of-equity.md, concepts/cost-of-equity/cost-of-equity-assembly.md, concepts/cost-of-equity/lambda-country-risk-exposure.md, concepts/cost-of-equity/alternative-relative-risk-measures.md

---

### M28 `wacc_assembler`
**Purpose.** The weighted average cost of capital, company-wide or divisional, in any currency, and its schedule across debt ratios.

**Inputs.** `cost_of_equity, pretax_cost_of_debt, cost_of_preferred, marginal_tax_rate, weights (from M21), tax_used_override`; divisional inputs; currency-conversion inputs.

**Outputs.** `wacc`, `after_tax_cost_of_debt`, `wacc_by_division`, `wacc_converted`, `wacc_schedule` (delegated to M52).

**Computation.**
- `WACC = ke × E/(D+E+PS) + kd × (1 − t_used) × D/(D+E+PS) + kps × PS/(D+E+PS)`, all at **market** values.
- `t_used` comes from M32 (it may be below the marginal rate when interest exceeds EBIT or a deductibility cap binds).
- Divisional: use divisional beta, divisional D/E and the company-wide cost of debt and tax rate (debt is raised at the corporate level).
- Currency conversion: apply M02 to the assembled WACC, or rebuild directly in the local currency; use the second as a check on the first.
- Net-debt convention: debt weight uses net debt and the resulting value is the operating business excluding cash — do not add cash back afterwards.

**Reference tables.** None.

**Edge cases.** Preferred below 5% of capital may be folded into debt. A private firm or division with no market equity uses the industry median market D/E. Consistency assertion: the D/E used to relever the beta must be the D/E implied by the weights.

**Test vector.** `wacccalc.xls` Facebook: `ke = 0.025 + 1.1124444 × 0.0712735 = 0.1042878`; `kd_AT = 0.035 × 0.6 = 0.021`; weights `0.976365/0.023635` → `WACC = 0.1023193`.

**Concepts.** concepts/cost-of-debt-capital/cost-of-capital-assembly.md, concepts/cost-of-debt-capital/divisional-cost-of-capital.md, concepts/cost-of-debt-capital/wacc-calculator-workflow.md, concepts/cost-of-debt-capital/hurdle-rate-choice.md, concepts/finance-foundations/cost-of-capital.md

---

## S5 — Growth, tax and reinvestment

### M29 `fundamental_growth`
**Purpose.** Growth from what the firm reinvests and what it earns on it — the only internally consistent growth source.

**Inputs.** `reinvestment_rate, roc, roc_next, roc_current, improvement_years n`; equity route `retention_ratio, roe, roe_next, payout_ratio`; `equity_reinvestment_rate, noncash_roe`; decomposition inputs `ebit, tax_rate, bv_debt, bv_equity, cash, interest_expense`.

**Outputs.** `g_operating, g_equity, efficiency_growth, new_investment_growth, roe_decomposition, implied_reinvestment_rate`.

**Computation.**
- Operating, stable return: `g_EBIT = reinvestment rate × ROC`.
- Operating, changing return: `g_EBIT = ROC_next × RR + (ROC_next − ROC_current)/ROC_current`; spread the efficiency term over `n` years as `[1 + (ROC_{t+n} − ROC_t)/ROC_t]^(1/n) − 1`.
- Equity: `g_EPS = retention × ROE`, constraint `g_EPS ≤ ROE`; changing-ROE version adds the same efficiency term.
- Non-cash version: `NI_noncash = NI − after-tax interest income on cash`; `non-cash ROE = NI_noncash/(BV equity − cash)`; `g = equity reinvestment rate × non-cash ROE`.
- **ROE decomposition:** `ROE = ROC + (D/E)[ROC − i(1−t)]` where `i = interest expense / book debt`. Leverage raises ROE iff `ROC > i(1−t)`.
- Inverted for planning (this is the terminal-year form): `reinvestment rate = g / ROC`; equity `payout = 1 − g/ROE`.
- Growth decomposition for reporting: `new-investment growth = RR × ROC`; `efficiency growth = g − RR × ROC`.
- Regulatory shock: `new ROE = old ROE / (1 + % increase in required book equity)`.

**Reference tables.** None.

**Edge cases.** ROC must be measured on **beginning-of-period** capital (R4). Capital net of cash and cross-holdings. `ROC ≤ 0` makes `g/ROC` meaningless. Efficiency growth is a one-off, not perpetual — it must be dropped in the stable phase.

**Test vector.** Caramba: `ROC = 1601.267×(1−0.34)/(3651.145 + 1306.1 − 1286.9 − 566.6) = 0.340504`; `RR = (1107.392 − 596.858 + 45.857)/1094.396 = 0.508400`; `g = 0.340504 × 0.508400 = 0.173112`.

**Concepts.** concepts/dcf-cashflows-growth/fundamental-growth-operating.md, concepts/dcf-cashflows-growth/fundamental-growth-equity.md, concepts/dcf-cashflows-growth/return-on-invested-capital.md, concepts/dcf-cashflows-growth/value-of-growth.md, concepts/dark-side-difficult/return-improvement-and-governance-drag.md

---

### M30 `historical_growth`
**Purpose.** Growth statistics from a historical earnings or revenue series, with the negative-base workarounds made explicit.

**Inputs.** `series: list[float]`, `metric: str`, `window: int`, `averaging: "arithmetic"|"geometric"|"regression"`, `negative_base_rule: "higher"|"absolute"|"regression"|"reject"`.

**Outputs.** `annual_growth_rates, arithmetic_mean, geometric_mean, stdev, regression_slope, regression_growth_proxy, cagr`.

**Computation.** `arithmetic = mean(yearly % changes)`; `geometric = (end/begin)^(1/n) − 1`, `n` = observations − 1; regression `Earnings_t = a + b·t`, growth proxy `= b / mean(earnings)`. Negative-base workarounds: divide the change by the higher of the two values, or by `|starting value|`, or use the regression slope. `Arithmetic ≥ geometric` always; the gap widens with volatility.

**Reference tables.** None.

**Edge cases.** **Default should be `reject`**: a growth rate computed off a negative or tiny base is not a forecast, it is an artefact. Acquisitions and restructurings break comparability across the window. Blended growth in the focussed models: `g_hg = w_hist·g_hist + w_outside·g_outside + w_fund·g_fund`; a toggle set to "No" contributes **0 while its weight is still applied** (a real behaviour, materially lowering `g_hg` — §19-Q10).

**Test vector.** `fcfe2st.xls`: `g_hist = (4.0/0.49)^(1/5) − 1 = 0.52185327`; blended `0.1×0.52185327 + 0.4×0.19 + 0.5×0.19773128 = 0.22705097`.

**Concepts.** concepts/dcf-cashflows-growth/historical-growth.md, concepts/dcf-cashflows-growth/analyst-growth-estimates.md, concepts/dcf-model-choice-loose-ends/multistage-model-mechanics.md

---

### M31 `reinvestment_engine`
**Purpose.** Net capex, change in working capital, and the sales-to-capital shortcut — the three ways the corpus charges for growth.

**Inputs.** `capex, depreciation, acquisitions, acquisition_amortisation, rnd_current, rnd_amortisation`; `ncwc_current, ncwc_prior, revenues, revenues_prior, wc_pct_of_revenue`; `sales_to_capital by phase`; `ebit_after_tax`; stable inputs `g_stable, roc_stable, capex_to_depreciation_stable`; sector ratios from M10.

**Outputs.** `net_capex, adjusted_net_capex, change_in_wc, reinvestment, reinvestment_rate, invested_capital_path, imputed_roic_path, marginal_roic`.

**Computation.**
- `Net capex = capex − depreciation`; `Adjusted net capex = net capex + RD_0 − RD amortisation + acquisitions − acquisition amortisation`.
- `NCWC = non-cash current assets − non-debt current liabilities`; `w = NCWC/Revenues`; **forecast** `ΔWC_t = w × (Rev_t − Rev_{t−1})` — driven by the revenue *change*, never the level.
- `Reinvestment = adjusted net capex + ΔWC`; `Reinvestment rate = reinvestment / EBIT(1−t)`.
- **Sales-to-capital shortcut** (young/changing-margin firms): `Reinvestment_t = (Rev_t − Rev_{t−1}) / sales_to_capital_t`, which bundles net capex, acquisitions, capitalised R&D and ΔWC into one number. Phase-varying ratio (year 1, years 2–5, years 6–10) is the Ginzu convention; the Tesla sheet sets years 6–10 to `2/3 × years 1–5`.
- `Invested capital_t = Invested capital_{t−1} + Reinvestment_t`; `Imputed ROIC_t = EBIT(1−t)_t / Invested capital_{t−1}`.
- `Marginal ROIC = Δ EBIT(1−t) over the horizon / Δ invested capital over the horizon`.
- **Stable-phase estimators (three, choose one):** fundamentals `Reinvestment = (g/ROC) × EBIT(1−t)`; sector ratio `capex = (sector CapEx/Dep) × depreciation`; capex-as-%-of-depreciation `net capex = (ratio − 1) × depreciation`.
- Base invested capital `= BV equity + BV debt − cash (+ research asset)(+ lease debt)`.

**Reference tables.** M10 (sector capex ratios).

**Edge cases.** **Year-1 reinvestment is floored at 0 when revenue falls; years 2+ are not** (negative reinvestment = capital release, correct for declining firms). Terminal reinvestment is 0 when `g ≤ 0`. `sales_to_capital = 0` → raise. Negative working-capital business models are real; fade the ratio toward zero deliberately rather than assuming it persists.

**Test vector.** SK Innovation year 1: `ΔRev = 48,535,833 − 32,357,222 = 16,178,611`; `/ sales_to_capital 10 = 1,617,861.10`.

**Concepts.** concepts/dcf-cashflows-growth/net-capital-expenditures.md, concepts/dcf-cashflows-growth/non-cash-working-capital.md, concepts/dark-side-difficult/sales-to-capital-reinvestment.md, concepts/project-returns/earnings-vs-cash-flows.md

---

### M32 `tax_engine`
**Purpose.** Effective vs marginal rates, the NOL waterfall, the convergence ramp and the two deductibility caps.

**Inputs.** `taxes_paid, taxable_income` (effective); `marginal_tax_rate`; `country` (for the statutory rate) or `revenue_weights_by_country`; `opening_nol`; `ebit_path: list[float]`; `converge: bool`, `convergence_years: int`; cap inputs `ebit, ebitda, interest_expense, cap_measure: "EBITDA"|"EBIT", cap_pct (0.30)`.

**Outputs.** `effective_tax_rate, tax_rate_path, taxes_path, nol_path, after_tax_ebit_path, t_ebit_limited, t_statutory_cap, t_used`.

**Computation.**
- `Effective = taxes paid / pre-tax income`. `Marginal` = statutory rate of the domicile, or a revenue-weighted blend.
- **NOL waterfall, per year:**
  - `EBIT_t ≤ 0`: taxes = 0; `NOL_t = NOL_{t−1} + |EBIT_t|`; `EBIT(1−t)_t = EBIT_t` (no refund).
  - `0 < EBIT_t ≤ NOL_{t−1}`: taxes = 0; `NOL_t = NOL_{t−1} − EBIT_t`; `EBIT(1−t)_t = EBIT_t`.
  - `EBIT_t > NOL_{t−1}`: `taxes = (EBIT_t − NOL_{t−1}) × t_marginal`; `NOL_t = 0`; `EBIT(1−t)_t = EBIT_t − taxes`.
  - Reported effective rate in the crossover year is a partial rate between 0 and marginal.
- **Convergence ramp:** hold the effective rate for years 1–5, then five equal steps to the terminal rate: `t_{n+1} = t_n + (t_marginal − t_5)/5`. Terminal rate = marginal, unless the "keep effective forever" override is set. (The Ginzu-full variant ramps linearly across *all* N years toward the stable rate instead — `t_i = t_stable − (N−i)(t_stable − t_effective)/N`.)
- **Cap 1 (EBIT limit):** `t_EBIT = t` if `interest ≤ EBIT`, else `t × EBIT/interest`.
- **Cap 2 (statutory 30% limit, post-2017 US):** `t_cap = t` if `interest ≤ 0.30 × M`, else `t × (0.30 × M)/interest`, `M = EBITDA through 2022, EBIT after`.
- **`t_used = min(t_EBIT, t_cap)`** — this is the rate that enters the after-tax cost of debt.
- Consistency: the tax rate used for EBIT(1−t) and the one in `kd(1−t)` must be the same.

**Reference tables.** M06 (country corporate tax rates).

**Edge cases.** Negative EBIT gets no tax credit in the NOL engine, but the plain `EBIT × (1−t)` form used in `capbudg` and `fcff3st` produces a **negative tax** (implicit full loss offset). Two different behaviours — expose `loss_offset: "nol"|"full_credit"` and state which the model uses.

**Test vector.** SK Innovation year 1: `EBIT = 1,456,074.99`, opening NOL `731.4`, marginal `0.25` → `taxes = (1,456,074.99 − 731.4) × 0.25 = 363,835.90` → `EBIT(1−t) = 1,092,239.09`.

**Concepts.** concepts/dcf-cashflows-growth/tax-rate-and-nols.md, concepts/capital-structure/tax-benefit-of-debt.md, concepts/cost-of-debt-capital/after-tax-cost-of-debt.md

---

### M33 `top_down_revenue_engine`
**Purpose.** Build revenues from market size and share, and drive margins to a target — the route for money-losers and firms with changing margins.

**Inputs.** `market_size_now, market_growth, target_share_by_year, revenue_slice`; or `revenue_growth_path`; `base_margin, target_margin, convergence_year`, `convergence_rule: "linear"|"speed"`, `speed_s`; `sales_to_capital by phase`; `tax_rule`.

**Outputs.** `revenue_path, margin_path, ebit_path, implied_cagr, reinvestment_path, invested_capital_path, roic_path, fcff_path`.

**Computation.**
- `Market_t = Market_0 × (1 + g_market)^t`; `Revenues_t = Market_t × share_t × revenue_slice`.
- `Implied CAGR between milestones = (Rev_b/Rev_a)^(1/(b−a)) − 1`.
- Direct path: `Rev_t = Rev_{t−1} × (1 + g_t)` with `g_1` given, years 2–5 a single CAGR, years 6–10 fading linearly to terminal: `g_{5+k} = g_5 − k(g_5 − g_terminal)/5`.
- **Margin convergence, linear:** `Margin_t = Target − (Target − Anchor)/Y × (Y − t)` for `t ≤ Y`, `= Target` for `t > Y`, where `Y` = convergence year and `Anchor` = the year-1 margin.
- **Margin convergence, speed-of-convergence:** `Margin_t = Target − (Target − Margin_{t−1})/(1 + 1/s)`; with `s = 1.5` the remaining gap shrinks 60% a year.
- `EBIT_t = Rev_t × Margin_t`; taxes via M32; reinvestment via M31; `FCFF_t = EBIT(1−t)_t − Reinvestment_t`; `ROIC_t = EBIT(1−t)_t/Invested capital_t`.

**Reference tables.** M07 (target-margin reference class, sales-to-capital anchors).

**Edge cases. Known sheet defect (§19-Q1):** the Ginzu-family margin ramp anchors years 2–5 on the **year-1 margin** but years 6–10 on the **base-year margin**, producing a kink at year 6 whenever `convergence_year > 5` (SK Innovation: yr5 0.0525 → yr6 0.04240). Expose `margin_anchor: "year1"|"base"|"faithful"`. Also: the base-year margin divides *adjusted* EBIT by *unadjusted* revenues.

**Test vector.** `revgrowth.xls`: `Rev_0 = 100`, market `100,000` growing 3%, share 2.5% at yr 5 and 6% at yr 10 → `Rev_5 = 2,898.185`, `Rev_10 = 8,063.498`, `CAGR_1–5 = 0.960764`, `CAGR_6–10 = 0.227099`, `CAGR_1–10 = 0.551145`.

**Concepts.** concepts/dcf-cashflows-growth/top-down-revenue-growth.md, concepts/dark-side-difficult/young-company-valuation.md, concepts/narrative-numbers/narrative-to-value-drivers.md

---

### M34 `terminal_value_engine`
**Purpose.** Close every valuation, and police the assumptions that make the closing honest.

**Inputs.** `terminal_cash_flow` or `(terminal_ebit_after_tax, g_stable, roc_stable)`; `discount_rate_stable`; `riskfree_rate`; `exit_multiple, terminal_metric` (alternative); `n` (end of the explicit period); `cumulative_discount_factor_n`.

**Outputs.** `terminal_value, pv_terminal_value, terminal_reinvestment_rate, terminal_reinvestment, implied_perpetual_roc, roc_neutral_reinvestment_rate, share_of_value_in_tv, screens: dict[str,bool]`.

**Computation.**
- Growing perpetuity: `TV_n = CF_{n+1}/(r_stable − g)`, `r` matched to the flow (WACC for FCFF, ke for FCFE/dividends).
- Firm form with reinvestment built in: `TV_n = EBIT_{n+1}(1−t)(1 − g/ROC)/(WACC − g)`.
- **Stable reinvestment `= g/ROC` (firm), stable payout `= 1 − g/ROE` (equity).** Zero when `g ≤ 0`.
- `PV(TV) = TV_n × CDF_n` where `CDF_n` is the *cumulative* factor from M01 (not `(1+r̄)^n`).
- **Default terminal ROC = terminal cost of capital** (makes growth value-neutral). Override only with a moat argument.
- **Default terminal WACC = (post-year-10 riskfree, else riskfree) + mature-market ERP.** The sheet labels say "riskfree + 4.5%"; the formula uses the mature ERP cell — reproduce the formula, not the label.
- Exit-multiple alternative: `TV_n = exit multiple × metric_n`. Convert it back into its implied `g` and `ROC` and check them against the perpetuity form; a stationarity assumption is embedded.
- **Reverse consistency checks (run always):** `embedded reinvestment rate = 1 − FCFF_terminal/EBIT(1−t)_terminal`; `implied perpetual ROC = g / embedded reinvestment rate`; `ROC-neutral reinvestment rate = g / cost of capital`.
- **Screens:** `g ≤ riskfree` (R6); `r_stable > g` (R7); `terminal ROC within [WACC, WACC + 5%]` else warn; `stable beta in [0.8, 1.2]` else warn; `stable cost of debt in [rf, rf + 3%]` else warn; `share of value in TV` reported.

**Reference tables.** None.

**Edge cases.** In the Ginzu-full engine the terminal after-tax EBIT is built as `S43 = (MAX(EBIT(1−t) over the path)/(1 − t_marginal)) × (1 − t_stable) × (1 + g)` — a MAX over the path, grossed up at the marginal rate and re-taxed at the stable rate (guards against a fade producing a lower final year). Reproduce exactly if matching that workbook (§19-Q11). Terminal ΔWC in the same engine grows revenue N years at the **unfaded initial** growth rate, not the faded path (§19-Q12).

**Test vector.** `ImpliedROCROE.xls`: `EBIT(1−t)_T = 1035`, `FCFF_T = 750`, `g = 0.04`, `r = 0.0935` → `embedded RR = 1 − 750/1035 = 0.2753623`; `implied ROC = 0.04/0.2753623 = 0.1452632`; `ROC-neutral RR = 0.04/0.0935 = 0.4278075`.

**Concepts.** concepts/dcf-cashflows-growth/terminal-value.md, concepts/dcf-model-choice-loose-ends/growth-pattern-and-stage-count.md, concepts/project-returns/terminal-value-and-project-life.md, concepts/acquisitions-control-enhancement/transaction-and-exit-multiples.md

---

## S6 — Cash-flow definitions

### M35 `fcff_builder`
**Purpose.** Free cash flow to the firm, by any of the three equivalent pathways.

**Inputs.** `ebit (adjusted), tax_rate, capex, depreciation, change_in_wc, reinvestment, reinvestment_rate`.

**Outputs.** `fcff`, `reinvestment`, `reinvestment_rate`.

**Computation.** Three identical routes — implement one, assert the others:
1. `FCFF = EBIT(1−t) − (capex − depreciation) − ΔNCWC`
2. `FCFF = EBIT(1−t) − Reinvestment`
3. `FCFF = EBIT(1−t) × (1 − reinvestment rate)`, with `reinvestment rate = g/ROC` in the fundamental form.
**The interest tax shield is NOT in FCFF.** It lives in `kd(1−t)` inside the WACC (M28). EBIT must already be lease- and R&D-adjusted (M12/M13) and tax-consistent with M32.

**Reference tables.** None.

**Edge cases.** Negative FCFF is normal for growth firms — the PV of the growth phase can legitimately be negative (Amazon 1998: `PV(FCFF yrs 1–10) = −3,841.259`). Reinvestment rate > 1 is possible and means the firm is raising capital.

**Test vector.** `fcffst.xls`: `EBIT 1535, t 0.36` → `EBIT(1−t) = 982.4`; `capex override 1.25 × 400 = 500`, `net capex 100`, `ΔWC 160` → `FCFF = 722.4`.

**Concepts.** concepts/dcf-cashflows-growth/fcff.md, concepts/finance-foundations/equity-vs-firm-valuation.md, concepts/dcf-model-choice-loose-ends/dcf-model-choice-framework.md

---

### M36 `fcfe_builder`
**Purpose.** Free cash flow to equity in all five variants, including the bank regulatory-capital form.

**Inputs.** `net_income, depreciation, capex, change_in_wc, new_debt_issued, debt_repaid, preferred_dividends`; `debt_ratio DR`; `interest_income_after_tax`; bank inputs `risk_adjusted_assets_path, tier1_ratio_path, roe_path, opening_book_equity`.

**Outputs.** `fcfe_full, fcfe_target_ratio, fcfe_predebt, equity_reinvestment, equity_reinvestment_rate, fcfe_bank, tier1_path, book_equity_path`.

**Computation.**
- **Full:** `FCFE = NI + D&A − capex − ΔNCWC + (new debt issued − debt repaid) − preferred dividends`.
- **Modified grouping:** `FCFE = NI − [(capex − D&A) + ΔWC] + net debt issued`.
- **Target-debt-ratio (stable leverage):** `FCFE = NI − (1 − DR)(capex − D&A) − (1 − DR)ΔWC`. Use the **book** DR for historical FCFE, the **market** DR for forecasts.
- **Pre-debt:** `FCFE_predebt = NI − (capex − D&A) − ΔWC` (the dividends.xls row 6).
- **Equity-reinvestment view:** `Equity reinvestment = (capex − D&A) + ΔWC − Δdebt`; `rate = equity reinvestment / NI`; `FCFE = NI × (1 − rate)`.
- **From the cash-flow statement:** `FCFE = CFO − capex − cash acquisitions − (debt repaid − debt issued)`. Cross-check identity: `FCFE = dividends + buybacks − stock issuances + Δcash balance`.
- **Bank / financial-service form:** `Tier1_t = risk-adjusted assets_t × Tier1 ratio_t`; `Investment in regulatory capital_t = Tier1_t − Tier1_{t−1}`; `NI_t = book equity_t × ROE_t`; `book equity_{t+1} = book equity_t + investment in regulatory capital_t`; **`FCFE_t = NI_t − investment in regulatory capital_t`**. Simple loan-book version: `FCFE = NI − (new loans − old loans) × capital ratio`.
- Non-cash variant: strip after-tax interest income on cash from NI and add cash back at the end.

**Reference tables.** None.

**Edge cases.** Equity reinvestment rate > 1 → negative FCFE (implies equity issuance) — allowed. `NI − interest income ≤ 0` makes the rate meaningless — normalise first. Whether reported capex includes acquisitions changes the answer materially; state the convention.

**Test vector.** `fcfeginzu`: `NetCapEx 4242.6098 + ΔWC 336.3054 − net debt 1864.6179 = 2714.2973`; `/ (4096 − 132) = ERR 0.6847370`; year 1 `NI = 3964 × 1.3560566 = 5375.4085`, `FCFE = 5375.4085 × (1 − 0.6847370) = 1694.6677`.

**Concepts.** concepts/dcf-cashflows-growth/fcfe.md, concepts/dividend-policy/fcfe-potential-dividends.md, concepts/dividend-policy/fcfe-for-banks.md, concepts/dark-side-difficult/bank-fcfe-and-excess-return-models.md, concepts/accounting-statements/potential-dividends-fcfe.md

---

### M37 `dividend_capacity_builder`
**Purpose.** What was actually returned, what could have been returned, and the gap.

**Inputs.** `dividends, buybacks, stock_issuance, net_income, fcfe_variants, market_cap, shares, eps, dps, price`.

**Outputs.** `cash_returned, augmented_payout_ratio, payout_ratio, dividend_yield, retention_ratio, buyback_share, effective_total_yield, cash_to_fcfe_by_variant, payout_gap, cumulated_cash_path`.

**Computation.**
- `Cash returned (augmented dividends) = dividends + buybacks`; net form subtracts stock issuance.
- `Payout = dividends/NI`; `Augmented payout = (dividends + buybacks)/NI`; `Retention = 1 − payout`.
- `Dividend yield = DPS/price = total dividends/market cap`; `Yield = payout / PE`.
- `Buyback share = buybacks/(dividends + buybacks)`; `Effective total yield = (dividends + net buybacks)/market cap`.
- `Cash paid as % of FCFE` computed **for each FCFE variant** (pre-debt, actual-debt, target-ratio) — the three can disagree enough to flip a verdict.
- `Cumulated cash_t = Cumulated cash_{t−1} + FCFE_t − cash returned_t`.

**Reference tables.** None.

**Edge cases.** Negative net income makes payout ratios meaningless. Buybacks that merely offset option dilution are not a return of cash — the netting decision is judgment supplied as a flag.

**Test vector.** `dividends.xls` 5-year aggregates: `cash returned 19,869`; `/ FCFE_predebt 17,301 = 1.1484307265475984`; `/ FCFE_actual 27,126 = 0.732470692324707`; `/ FCFE_target 18,064.54 = 1.0998896900399782`.

**Concepts.** concepts/dividend-policy/cash-returned-dividends-and-buybacks.md, concepts/dividend-policy/dividend-payout-and-yield-measures.md, concepts/dividend-policy/dividend-decision-sequence.md, concepts/accounting-statements/life-cycle-financing-and-dividend-capacity.md

---

## S7 — DCF engines

Seven engines, differing only in how many stages, how inputs move between them, and which cash flow they discount. **M84 selects among them.**

### M38 `stable_growth_valuator`
**Purpose.** Single-stage (Gordon) valuation on dividends, FCFE or FCFF.

**Inputs.** `base_cash_flow` (DPS₀, FCFE₀ or FCFF₀) or `(eps, payout)`; `growth g`; `discount_rate r` (ke or WACC); optional `roe_stable/roc_stable` to derive the payout or reinvestment rate; optional `capex_override_ratio`, `offset_capex_with_depreciation: bool`, `debt_financing_ratio DR`.

**Outputs.** `value` (per share or firm), `reinvestment_rate`, `payout_ratio`, `sensitivity_table(g → value)`.

**Computation.**
- `Value = CF_0 × (1 + g)/(r − g)`; forward form `CF_1/(r − g)`.
- Derived reinvestment: `RR = g/ROC` (firm) or `payout = 1 − g/ROE` (equity); then `FCFF = EBIT(1−t)(1 − RR)`, `FCFE = NI(1 − g/ROE)`.
- Line-item alternative (FCFE stable): `RR_inputs = [(capex − dep)(1−DR) + ΔWC(1−DR)]/EPS`; branch `offset_capex_with_depreciation` sets net capex to 0.
- Sensitivity: sweep `g` holding `CF` and `r` fixed.

**Edge cases.** `r ≤ g` → reject (R7). `g` materially above nominal economy growth → reject (R6). Negative EPS invalidates the reinvestment-rate formulation.

**Test vector.** `ddmst.xls`: `EPS 4.33 × payout 0.63 = DPS 2.7279`; `ke = 0.07 + 0.95×0.055 = 0.12225`; `g = 0.06` → `Value = 2.7279 × 1.06/0.06225 = 46.450987951807235`. Firm analogue `fcffst.xls`: `722.4 × 1.05/(0.10769283 − 0.05) = 13,147.56`.

**Concepts.** concepts/finance-foundations/stable-growth-equity-valuation.md, concepts/dcf-model-choice-loose-ends/multistage-model-mechanics.md, concepts/narrative-numbers/three-approaches-to-valuation.md

---

### M39 `two_stage_engine`
**Purpose.** Constant high growth for `n` years, then an abrupt switch to stable growth.

**Inputs.** base financials; `n: int (1–10)`; growth inputs (direct, fundamental `ROC×RR`, or the three-way blend from M30); per-item growth rates for capex/depreciation/revenues or "grow with earnings"; `wc_pct_of_revenue`; stable block `(g_stable, beta_stable, kd_stable, debt_ratio_stable, roc_stable/roe_stable, capex_to_dep_stable, offset_capex: bool)`; discount rates from M27/M28; bridge inputs.

**Outputs.** per-year table `(earnings, net capex, ΔWC, cash flow, PV)`; `terminal_cash_flow, terminal_value, pv_high_growth, pv_terminal, firm_value, equity_value, value_per_share`; growth-value decomposition.

**Computation.**
- Year `i`: `EBIT(1−t)_i = EBIT(1−t)_0 × (1+g)^i`; `(capex − dep)_i = (capex − dep)_0 × (1+g_capex)^i`; `Rev_i = Rev_0(1+g_rev)^i`; `ΔWC_i = w × (Rev_i − Rev_{i−1})` (equity variants multiply the last two by `(1 − DR)`); `CF_i = earnings − net capex − ΔWC`; `PV_i = CF_i/(1+r_hg)^i`.
- Terminal: `earnings_T = earnings_n(1+g_stable)`; reinvestment by one of three rules — fundamentals `RR = g/ROC` (or `g/ROE`), capex offset by depreciation, or `capex = ratio × depreciation`. **Display back-solve:** `ΔWC_T = w × Rev_n × g_stable × (1−DR)` and `net capex_T = earnings_T × RR − ΔWC_T`, so the components still add to `CF_T`.
- `TV_n = CF_T/(r_stable − g_stable)`; `PV(TV) = TV_n/(1+r_hg)^n` (two-stage discounts the terminal value at the **high-growth** rate).
- Bridge: `+ cash − MV debt − options`, `÷ shares`.
- Growth-value decomposition: `assets in place = CF_0/r_stable`; `stable-growth value = CF_0(1+g_stable)/(r_stable − g_stable) − assets in place`; `extraordinary growth = total − CF_0(1+g_stable)/(r_stable − g_stable)`.

**Edge cases.** `n ≤ 10` in the sheet layouts (a port need not keep the cap). Weights of the three growth estimators should sum to 1; the sheets do not enforce it. `ROC` uses **prior-year** book capital (`E30+E31`, not `D30+D31`).

**Test vector.** `fcff2st.xls`: `g_hg = 0.10563433`, `WACC = 0.09616948`, 5 years → `PV high growth = 12,446.562`, `TV = 89,782.256`, `PV(TV) = 56,728.591`, `firm = 69,175.152`, `equity = 67,853.152`, `per share = 66.7826`. Equity analogue `fcfe2st.xls` → `51.56356021001768`; `ddm2st.xls` → `177.53847651929308`.

**Concepts.** concepts/dcf-model-choice-loose-ends/multistage-model-mechanics.md, concepts/dcf-model-choice-loose-ends/equity-versus-firm-valuation.md, concepts/dcf-cashflows-growth/dcf-case-valuations.md

---

### M40 `three_stage_engine`
**Purpose.** High growth, a linear transition, then stable growth — with the discount rate itself moving.

**Inputs.** everything M39 needs plus `n1` (high-growth years), `n2` (transition years), `beta_stable`, `payout_stable`, `beta_adjusts_gradually: bool`, `payout_adjusts_gradually: bool`, per-phase line-item growth rates.

**Outputs.** three-phase per-year table (growth, payout, beta, discount rate, earnings, net capex, ΔWC, cash flow, cumulative discount factor, PV); `pv_phase1, pv_phase2, pv_terminal, value`.

**Computation.**
- Transition year `j = 1..n2`: `g_j = g_hg − (g_hg − g_stable)·j/n2`; `payout_j = payout_hg + (payout_stable − payout_hg)·j/n2`; `beta_j = beta_hg − (beta_hg − beta_stable)·j/n2`; `r_j = riskfree + beta_j × ERP`. The **first** transition year is already one step down; the last equals the stable value exactly.
- Cumulative growth in transition: `cum_j = Π_{k≤j}(1 + g_k) − 1`; earnings and line items compound with the year-specific `g`.
- **Discounting:** phase-1 flows at `(1 + r_hg)^i`; transition-year `j` at `(1 + r_hg)^{n1} × Π_{k≤j}(1 + r_k)`; the terminal price discounts through the **end of the transition**.
- Margin-driven variant (`fcff3st`): the parameter that ramps is the operating-expense ratio `1 − margin`, and revenue/depreciation growth, beta, debt ratio and cost of debt all interpolate linearly over years 6–10. Year-10 capex is **back-solved** from the stable reinvestment rule and years 6–9 interpolate linearly in **dollars** to that target.
- "End-of-life index" row = 1 in the final transition year, 0 elsewhere — the marker for where the terminal value attaches when `n2 < 10`.

**Edge cases.** Odd `n` for the "second half" fade: define fade start = `floor(n/2)` and document it. With time-varying `r`, never use a single average rate.

**Test vector.** `fcff3st.xls`: revenue growth 0.30 for 5 years fading `0.252 → 0.06`; opex ratio `0.9310817 → 0.70 → 0.75`; WACC `0.13375 → 0.121625`; `TV = 7541.76 × 1.06/(0.121625 − 0.06) = 129,724.42`; `firm = 66,666.83`; `per share = 44.011`. Equity analogue `fcfe3st.xls` → `12.608011584017325`; `ddm3st.xls` → `19.945505410290917`.

**Concepts.** concepts/dcf-model-choice-loose-ends/multistage-model-mechanics.md, concepts/dcf-model-choice-loose-ends/growth-pattern-and-stage-count.md

---

### M41 `n_stage_engine`
**Purpose.** Fully year-specific inputs for up to 10 years, with an NOL tax engine — the money-losing-firm model.

**Inputs.** base financials incl. `nol_carryforward`; per-year vectors of length `n`: `g_revenue[], opex_pct_of_revenue[], g_capex[], g_depreciation[], wc_pct_of_revenue[]` (or `ebitda_margin[]`); stable block; beta/debt-ratio glide targets; option inputs.

**Outputs.** full projection table (revenues, COGS/EBITDA, depreciation, EBIT, taxes, NOL balance, EBIT(1−t), capex, ΔWC, FCFF), per-year beta/ke/debt ratio/WACC/cumulative WACC, PVs, terminal value, firm value, equity value, value per share.

**Computation.**
- `Rev_t = Rev_{t−1}(1 + g_t)`; `COGS_t = opex_pct_t × Rev_t` **or** `EBITDA_t = margin_t × Rev_t`; `Dep_t = Dep_{t−1}(1 + g_dep,t)`; `EBIT_t = Rev_t − COGS_t − Dep_t` or `EBITDA_t − Dep_t`.
- NOL/tax via M32 (`loss_offset = "nol"`).
- `CapEx_t = CapEx_{t−1}(1 + g_capex,t)`; terminal capex `= ratio × Dep_T` or `= Dep_T` if offset.
- `ΔWC_t = wc_pct_t × (Rev_t − Rev_{t−1})` — the current WC *level* input is not used in the forecast.
- `FCFF_t = EBIT(1−t)_t + Dep_t − CapEx_t − ΔWC_t`.
- Beta and debt ratio hold their initial values through the first half, then glide linearly to stable over the **last five years**; some variants (higrowth) step the debt ratio and kd by `1/(11−t)` of the total gap, giving a convex, back-loaded path. `kd_AT` may use the year's **effective** rate (fcffneg) or always the marginal rate (fcffgen) — expose the flag.
- Discount with cumulative products of year-specific WACCs.

**Edge cases.** `fcffgen` pays **no tax and grows the NOL** in loss years; `fcff3st` applies a flat rate and produces a **negative tax** in loss years. Different models, different behaviour — do not unify silently. FCFF can be negative for most of the horizon, making `PV(high growth)` negative.

**Test vector.** `fcffneg.xls`: WACC `0.11623 → 0.077416`; `FCFF_T = 2243.06 × (1 − 0.05/0.09) = 996.915`; `TV = 36,362.96`; `firm = 15,917.34`; `+cash 1477 − debt 7271 = equity 10,123.34`; `− options 299.73`; `÷ 886.467 shares = 11.081753703892744`. `fcffgen.xls` (Amazon) → `37.561`.

**Concepts.** concepts/dark-side-difficult/young-company-valuation.md, concepts/dcf-cashflows-growth/tax-rate-and-nols.md, concepts/dcf-cashflows-growth/normalizing-depressed-earnings.md

---

### M42 `ginzu_simple_fcff_engine`
**Purpose.** The flagship: a pure function from ~25 inputs to a value per share. Ten explicit years, driver-based, with fades, NOLs, failure risk, options and the full equity bridge. This is the default engine for a normal company.

**Inputs (complete surface).**
- *Identity:* `valuation_date, company, country (ERP key), industry_us, industry_global`.
- *Base year (currency units):* `revenues, revenues_prior, years_since_last_10k, ebit, ebit_prior, interest_expense, bv_equity, bv_debt, cash, cross_holdings, minority_interests`.
- *Market:* `shares_outstanding, stock_price, riskfree_rate, initial_cost_of_capital`.
- *Taxes:* `effective_tax_rate, marginal_tax_rate`.
- *Drivers:* `growth_year1, cagr_years_2_5, margin_year1, target_margin, convergence_year (int 1–10), sales_to_capital_1, sales_to_capital_2_5, sales_to_capital_6_10`.
- *Flags + sub-inputs:* `capitalize_rnd → (rnd_life, rnd_current, rnd_past[])`; `has_leases → (lease_expense, commitments[5], lump_beyond)`; `has_options → (n_options, strike, maturity, sigma, dividend_yield)`.
- *Overrides:* `terminal_wacc`, `terminal_roc`, `prob_failure + distress_base ("B"|"V") + distress_pct`, `keep_effective_tax`, `nol_carryforward`, `riskfree_after_year10`, `perpetual_growth`, `trapped_cash + foreign_tax_rate`.
- *Optional CoC stack:* beta approach + segments, ERP approach + geography weights, cost-of-debt approach + rating/firm type, convertible and preferred terms, debt maturity.

**Outputs.** Per-year vectors `(growth, revenues, margin, EBIT, tax rate, EBIT(1−t), NOL, reinvestment, FCFF, sales-to-capital, invested capital, ROIC, WACC, cumulative DF, PV)`; terminal block; `going_concern_value, prob_failure, distress_proceeds, value_of_operating_assets, value_of_equity, value_of_options, value_of_common_equity, value_per_share, price_as_pct_of_value`; diagnostics `(marginal_roic, average_compounded_wacc, value_to_price, verdict_text)`.

**Computation (ordered — this is the canonical pipeline).**
1. M12 R&D, M13 leases (iterate with M22 if synthetic rating).
2. Adjusted base EBIT `= reported EBIT + lease adj + R&D adj`; base margin `= adjusted EBIT / revenues`; invested capital `= BV equity + BV debt − cash (+ lease debt)(+ research asset)`.
3. M28 initial WACC (or take the supplied number — note the Tesla sheet takes it from the front-end and **does not** use its own CoC worksheet).
4. Growth path: `g_1` given; `g_2..g_5 = CAGR`; `g_6..g_10` fade in five equal steps to terminal; `g_terminal = override, else post-yr-10 riskfree, else riskfree`.
5. Revenues; margins via M33; `EBIT_t = margin_t × Rev_t`.
6. Tax path via M32 (effective yrs 1–5, five steps to marginal); NOL waterfall.
7. Reinvestment via M31 (year-1 floor at 0; phase-varying sales-to-capital); `FCFF_t = EBIT(1−t)_t − Reinvestment_t`.
8. WACC path: constant yrs 1–5, five linear steps to terminal `= override, else (post-yr-10 rf or rf) + mature-market ERP`. Cumulative DF; PVs.
9. Terminal: `ROC_terminal = override, else terminal WACC`; `reinvestment = (g/ROC)×EBIT(1−t)_T`, 0 if `g ≤ 0`; `TV = FCFF_T/(WACC_T − g)`; `PV(TV) = TV × CDF_10`.
10. `Going concern = PV(TV) + Σ PV(FCFF)`; failure adjustment via M48; equity bridge via M49; options via M46 (iterate).

**Reference tables.** M06, M07, M08, M09.

**Edge cases.** Negative base EBIT is *supported* (that is the point). Year-1 reinvestment floors at 0; later years do not. Terminal `g ≤ 0` → zero terminal reinvestment. Margin kink (§19-Q1). Trapped cash: `cash_used = cash − trapped × (marginal − foreign tax)`; string compare is case-insensitive in the sheets. **Debt in the equity bridge is BOOK debt (+ lease debt); debt in the WACC weights is estimated MARKET debt.** Keep both.

**Test vector (full end-to-end).** SK Innovation, 2022-01-01, KRW millions:
`R&D life 5, current 251,563, past [253,611, 227,441, 233,578, 195,693, 145,318]` → `RA 723,486.2`, `AM 211,128.2`, `EBIT adj +40,434.8`; adjusted EBIT `−210,394.2`; invested capital `25,144,323.2`; WACC `0.0731225`; `g` 0.50 then 0.05 fading to 0.02; margin `0.03 → 0.075` by year 10; sales/capital `10 / 5 / 1.5`; NOL 731.4; failure `p=0.12`, `"V"`, 50%.
→ `TV = 2,691,836.83/(0.0624 − 0.02) = 63,486,717.76`; `PV(TV) = 32,303,991.78`; `PV(10 yrs) = 7,121,239.68`; `going concern = 39,425,231.46`; `operating assets = 37,059,717.57`; `equity = 27,043,988.57`; **`value per share = 323,492.686`** vs price 273,500 → `price/value = 0.845460`.
Secondary vectors: Boeing (2020-03-27) → **88.69**/share, price/value 1.4397. Tesla (2021-11-01) → **571.29**/share, price/value 2.1005.

**Concepts.** concepts/dcf-cashflows-growth/fcff-forecast-engine.md, concepts/dark-side-difficult/young-company-valuation.md, concepts/narrative-numbers/tesla-motley-fool-valuation.md, concepts/dcf-cashflows-growth/dcf-case-valuations.md

---

### M43 `ginzu_full_fcff_engine`
**Purpose.** The fundamentals-driven Ginzu variant: up to 15 high-growth years, growth from `ROC × RR` rather than a revenue path, 2-stage / 3-stage / pure-stable by switch, with the earnings normaliser, cross-holdings and dual-currency support.

**Inputs.** As M42 plus: `high_growth_years n (0–15)`, `fade_second_half: bool` (the 2-stage/3-stage switch), `compute_growth_from_fundamentals: bool`, `roc_override, rr_override`, `keep_computed_debt_ratio: bool + debt_ratio_override`, `keep_wc_ratio: bool + wc_ratio_override`, `stable block (g, beta, erp, debt_ratio, pretax_kd, tax, roc or capex_to_dep)`, `normalize_operating_income: bool`, `lambda`, `fx_fiscal, fx_prior, fx_current`, `sector_pb_for_minority_interest`.

**Outputs.** as M42, plus `roc_computed, rr_computed, g_high, imputed_stable_roc, assets_in_place_value, growth_value`, and dual-currency per-share values.

**Computation.**
- `ROC = adjusted EBIT × (1 − marginal t) [+ R&D tax effect] / (prior BV debt + prior BV equity − prior cash − prior non-operating assets)`; `RR = (adjusted capex − adjusted depreciation + ΔWC)/current adjusted EBIT(1−t_effective)`; `g_high = ROC × RR`.
- **ΔWC replacement rule:** if the entered ΔWC is negative, replace it with `ΔRevenue × (NCWC/Revenue)`.
- **Computed debt ratio:** `1 − (price×shares + option value)/(MV debt + price×shares + option value + lease debt)` — option value sits in equity, creating circularity C3.
- Fade structure (when `fade_second_half`): for `t < n/2` hold `g_high`, `RR_high`, `WACC_high`; thereafter `x_t = x_stable + (x_high − x_stable)(n − t)/(n/2)`, reaching stable exactly at `t = n`.
- Tax ramp across all `n` years from effective to stable.
- Terminal block per M34 including the MAX-of-path and unfaded-ΔWC quirks (§19-Q11, Q12).
- `n = 0` collapses to pure stable growth: value = TV directly, **no discounting of the TV**.
- Dual currency: fiscal-year flows ÷ current FX, prior-year book values ÷ prior FX, per-share result × current FX.
- Cross-holdings sheet: minority traded holdings `= %held × market cap`; majority unlisted `= book value × sector P/B`; total feeds "non-operating assets".
- Lambda cost of equity: `ke = Rf + β×matureERP + λ×CRP` (both phases).

**Edge cases.** ROC denominator can be ≤ 0 — guard. `Stable RR` has a non-fundamental branch computed from terminal identities `(S43 − S46)/S43`, which is circular — solve simultaneously. Firm-type input is duplicated across two cells in the workbook; use one.

**Test vector.** Caramba (2017-04-01): leases → debt 1,443.945, EBIT adj +263.342; adjusted EBIT 1,601.267; coverage 4.9475 → A2/A → kd 0.0473670; `ROC 0.340504 × RR 0.508400 = g 0.173112`; WACC `0.1024525` (high) / `0.09132` (stable); `PV high growth = 8,579.82`; `TV = 3,222.223/(0.09132 − 0.03) = 52,547.67`, `PV(TV) = 20,424.90`; `operating assets 29,004.72 + 1,570 − 4,052.95 − 17.7 = 26,504.08`; **`per share = 60.0039`** vs price 38.34 → 36.1% undervalued. Lambda variant: **`145.47483` US$ = `298.22341` local**.

**Concepts.** concepts/dcf-cashflows-growth/fcff-forecast-engine.md, concepts/dcf-cashflows-growth/fundamental-growth-operating.md, concepts/dark-side-difficult/cross-holdings.md, concepts/cost-of-equity/lambda-country-risk-exposure.md

---

### M44 `excess_return_engine`
**Purpose.** Value as `capital invested + PV of excess returns`. Two forms: EVA at the firm level, equity excess returns for financial firms.

**Inputs.** Firm: `capital_invested_0, ebit_after_tax_path, wacc_path, net_capex_path, change_wc_path, g_stable, roc_terminal`. Equity/bank: `book_equity_0, roe_path, payout_path, cost_of_equity_path, g_stable, roe_stable, shares`.

**Outputs.** `capital_path, capital_charge_path, eva_path, pv_eva, terminal_eva, terminal_value_of_eva, terminal_capital_adjustment, firm_value`; bank: `book_equity_path, ni_path, equity_cost_path, excess_return_path, terminal_excess_return, tv, equity_value, value_per_share`.

**Computation.**
- **Firm/EVA:** `Capital_end,t = Capital_begin,t + net capex_t + ΔWC_t`; `EVA_t = EBIT(1−t)_t − WACC_t × Capital_begin,t` (**beginning** capital); `ROC_t = EBIT(1−t)_t/Capital_begin,t`.
- Terminal reconciliation (**mandatory or the routes do not agree**): `RR_terminal = (EBIT(1−t)_T − FCFF_T)/EBIT(1−t)_T`; `ROC_terminal = g_stable/RR_terminal`; `Adjusted terminal capital = EBIT(1−t)_T/ROC_terminal`; `EVA_T = EBIT(1−t)_T − WACC_stable × adjusted terminal capital`; `TV_EVA = EVA_T/(WACC_stable − g_stable)`.
- `Firm value = Σ PV(EVA) + Capital invested + PV(adjusted terminal capital − ending capital in the final explicit year)`.
- `MVA = market value − capital invested = PV of expected EVA`.
- **Equity excess return (banks):** `NI_t = ROE_t × BV_begin,t`; `Equity cost_t = ke_t × BV_begin,t`; `XR_t = NI_t − equity cost_t`; `Div_t = NI_t × payout_t`; `BV_{t+1} = BV_t + (NI_t − Div_t)`; `TV = XR_{n+1}/(ke_stable − g_stable)`; `Value of equity = current book equity + Σ PV(XR)`.
- Discount with cumulative products of the year-specific rate.

**Edge cases.** Ending vs beginning capital in the charge is a classic error. Terminal FCFF ≥ terminal EBIT(1−t) makes `RR_terminal ≤ 0` and the terminal ROC undefined — guard. Naive book capital (debt + equity) needs the lease/R&D/goodwill adjustments from M16 or every EVA number is corrupt.

**Test vector.** `fcffeva.xls` / `evavaln.xls`: `PV of EVA 60,463.43 + capital 20,000 + terminal adjustment (−95.93) = 80,367.4966` — **identical to the FCFF route's 80,367.4966**; per share `53.578`. Bank: `eqexret.xls` → `equity invested 17,997 + PV excess returns 65,993.76 = 83,990.76`; `÷ 1,120.713 shares = 74.944`.

**Concepts.** concepts/acquisitions-control-enhancement/eva-and-dcf-equivalence.md, concepts/acquisitions-control-enhancement/gaming-eva.md, concepts/dark-side-difficult/bank-fcfe-and-excess-return-models.md, concepts/dividend-policy/fcfe-for-banks.md

---

### M45 `model_equivalence_tests`
**Purpose.** The unit tests that prove a model is internally consistent. Run them automatically after every valuation.

**Inputs.** outputs of two engines run on one consistent assumption set.

**Outputs.** `pass/fail` per test plus the reconciling term.

**Tests.**
- **T1 FCFF ↔ FCFE.** Impose `Debt_t = DR × V_t` (compute firm values first, then the debt schedule), `Interest_t = kd × Debt_{t−1}`, `New debt_t = Debt_t − Debt_{t−1}`, `NI_t = (EBIT_t − Interest_t)(1−t)`, `FCFE_t = NI_t − Reinvestment_t + New debt_t`, `TV^equity = TV^firm − Debt_n`. Assert `Σ FCFF/(1+WACC)^t + PV(TV^firm) − Debt_0 == Σ FCFE/(1+ke)^t + PV(TV^equity)`. *Vector:* `fcffvsfcfe.xls` → firm 617.006, debt 123.401, **equity 493.605 by both routes**.
- **T2 DDM ↔ FCFE.** `CB_1 = FCFE_1 − Div_1`; `CB_t = CB_{t−1}(1+r_cash) + (FCFE_t − Div_t)`; `V_DDM = Σ PV(Div) + PV(P_n) + CB_n/(1+ke)^n`. Assert `V_FCFE − V_DDM == 0` **iff `r_cash == ke`**. *Vector:* `fcfevsddm.xls` → FCFE 1864.934, DDM 1855.676, difference **9.258** at `r_cash = 7%` vs `ke = 9%`.
- **T3 EVA ↔ DCF.** As in M44; the terminal-capital adjustment is the reconciling term. *Vector:* both 80,367.4966.
- **T4 Gross ↔ net debt.** With the cost-of-debt adjustments (`kd_gross = (Interest − rf×Cash×D/V)/(D − Cash×D/V)`, `kd_net = (Interest − rf×Cash)/(D − Cash)`), the two equity values agree **only at a 0% tax rate**; above that the net-debt approach gives a lower value. *Vector:* `GrossvsNet.xls` at t = 40% → gross equity **991.246**, net equity **924.775**.
- **T5 Sum-of-parts additivity.** Combined-firm value with no synergy must equal the sum of stand-alone values exactly (M75).
- **T6 Terminal consistency.** `implied perpetual ROC` from M34 within a stated band of the terminal WACC.
- **T7 Currency invariance.** Value converted at the spot rate must match the value built directly in the other currency (M02).

**Concepts.** concepts/dcf-model-choice-loose-ends/fcff-fcfe-reconciliation.md, concepts/dcf-model-choice-loose-ends/ddm-fcfe-reconciliation.md, concepts/dcf-model-choice-loose-ends/cash-in-valuation.md, concepts/dark-side-difficult/currency-consistency-and-invariance.md

---

## S8 — The equity bridge

### M46 `employee_option_valuer`
**Purpose.** Dilution-adjusted Black-Scholes value of employee options and warrants — the claim that must be subtracted before dividing by shares.

**Inputs.** `stock_price S` (market price, or the model's own value per share — the latter is circular), `strike K`, `maturity T` (years; use the *effective*, not contractual, life), `sigma`, `dividend_yield q`, `riskfree r`, `n_options`, `n_shares`, `vesting_probability`, `marginal_tax_rate`, `value_at: "price"|"estimated_value"`, `tax_effect: bool`.

**Outputs.** `adjusted_stock_price, d1, d2, N(d1), N(d2), value_per_option, total_option_value, after_tax_option_value, iterations`.

**Computation.**
```
S_adj = (S × n_shares + C × n_options)/(n_shares + n_options)      # circular in C
d1 = [ln(S_adj/K) + (r − q + σ²/2)T]/(σ√T)
d2 = d1 − σ√T
C  = S_adj·e^(−qT)·N(d1) − K·e^(−rT)·N(d2)                          # strike discounted at the RAW riskfree rate
Total = C × n_options   (× vesting probability, if used)
```
Solve the `S_adj ↔ C` fixed point with M05 (converges in a few iterations from plain Black-Scholes on `S`). When `value_at = "estimated_value"` there is a **second, outer** circularity: `S` is the model's own value per share, which subtracts this option value. Solve jointly.
`After-tax option value = total × (1 − marginal tax)` — the Ginzu-full engine applies this; the simple engine does not. Expose the flag.

**Reference tables.** M04.

**Edge cases.** Deep in-the-money grants (`S >> K`) give `N(d1) ≈ N(d2) ≈ 1` and `C ≈ S_adj − K·e^(−rT)` — correct, but a warning that the option is really a share equivalent. `T = 0` or `σ = 0` degenerate. **Alternatives that must NOT be combined with this one (R5):** diluted share count, or treasury-stock `(equity + n_options×K)/diluted shares`. The option-drag answer always sits between the other two for at- or in-the-money grants — use that as a test.

**Test vector.** `fcffgen` Option Valuation: `S 84, K 13.375, T 8.4, σ 0.5, q 0, r 0.065, n_options 38, n_shares 340.79` → `S_adj = 83.20784`, `d1 = 2.3627530`, `N(d1) = 0.9909301`, `d2 = 0.9136153`, `N(d2) = 0.8195405`, `C = 76.10366`, `total = 2,891.939`. Tesla (circular through value/share): `S = 571.288`, `S_adj = 565.585`, `C = 502.561`, `total = 51,070.25`.

**Concepts.** concepts/dcf-model-choice-loose-ends/valuing-employee-options.md, concepts/dcf-model-choice-loose-ends/employee-option-per-share-approaches.md, concepts/dark-side-difficult/dilution-and-employee-options.md, concepts/dcf-model-choice-loose-ends/restricted-stock-and-future-grants.md

---

### M47 `cross_holdings_and_nonoperating`
**Purpose.** Value what the operating DCF does not cover, and remove what it over-covers.

**Inputs.** per holding `(name, ownership_pct, is_consolidated: bool, subsidiary_equity_value | book_value, sector_price_to_book, subsidiary_debt)`; `minority_interest_book`, `sector_pb_for_minority`; `overfunded_pension (plan_assets, plan_liabilities, tax_on_withdrawal, claimability_prob)`; `unutilized_assets_market_value`; `trapped_cash, marginal_tax_rate, foreign_tax_rate`; `operating_cash_pct`.

**Outputs.** `value_of_minority_holdings, market_value_of_minority_interest, other_addable_assets, cash_adjusted, composition_percentages`.

**Computation.**
- **Three-step sum of the parts:** `Parent equity = un-consolidated parent value − parent debt + Σ_j ownership%_j × (Value_j − Debt_j)`.
- **Majority (consolidated) holding:** already inside operating value → **subtract** the minority interest at estimated **market** value: `≈ minority interest book × sector P/B`.
- **Minority (unconsolidated) holding:** not in operating value → **add** `ownership% × subsidiary equity value`, or the approximation `ownership% × (book equity × sector P/B)`.
- **Cash:** add at face when it earns a fair riskless return (`value = cash earnings/riskfree`, i.e. `PE = 1/rf`, `P/BV = 1`). Trapped-cash haircut: `cash − trapped × (marginal tax − foreign tax)`. Marginal-value-of-cash discount when `ROIC < WACC`: `discount = underperformance/required return`.
- **Add only what is not already in the flows** (R5). Overfunded pension: `(plan assets − liabilities) × (1 − tax) × claimability probability`. Unutilised assets at appraised market value. **Never add brand, goodwill, or operating PP&E.**
- Composition check: `% operating + % holdings + % cash = 100%`.

**Reference tables.** M07 (sector P/B).

**Edge cases.** Circular cross-holdings (two group companies owning each other) need simultaneous solution or an explicit convention. Listed subsidiaries: choose market value or your own DCF, and say which.

**Test vector.** `fcffginzulambda` Cross Holdings sheet: minority traded `0.176 × 4,806 = 845.856`; majority unlisted `329.8 × 1.1 = 362.78`; total **`3,937.068`** → feeds "value of non-operating assets".

**Concepts.** concepts/dcf-model-choice-loose-ends/cross-holdings.md, concepts/dcf-model-choice-loose-ends/cash-in-valuation.md, concepts/dcf-model-choice-loose-ends/marginal-value-of-cash.md, concepts/dcf-model-choice-loose-ends/other-non-operating-assets.md, concepts/dark-side-difficult/cross-holdings.md

---

### M48 `failure_distress_adjuster`
**Purpose.** Blend a going-concern value with a distress value using an explicit probability.

**Inputs.** `going_concern_value`, `prob_failure`, `distress_base: "B"|"V"`, `distress_pct`, `bv_equity`, `bv_debt`, `face_value_of_debt`, `equity_loss_fraction` (partial-wipeout variant), `annual_probability`, `horizon_years`.

**Outputs.** `distress_proceeds, value_of_operating_assets, adjusted_value, cumulative_probability`.

**Computation.**
- `Proceeds = (bv_equity + bv_debt) × distress_pct` (**"B"**, book capital) or `going_concern_value × distress_pct` (**"V"**, fair value). Model default `distress_pct = 0.50`.
- `Value of operating assets = going_concern × (1 − p) + proceeds × p`.
- Equity level: `Equity = DCF equity × (1 − p) + distress equity × p`; **`distress equity = 0` whenever `proceeds < face value of debt`**.
- Partial wipeout (survival with dilution/expropriation): `Adjusted value = DCF value × (1 − p × equity_loss_fraction)` (Boeing: 20% × 50% = a 10% haircut).
- `Cumulative p over n years = 1 − (1 − p_annual)^n`.

**Reference tables.** M10 (sector survival rates), M08 (cumulative default probability by rating).

**Edge cases.** The probability may come from M50 (bond-implied), a rating table, or judgment — record the source. Do not apply a failure probability *and* a distress-adjusted cost of capital for the same risk.

**Test vector.** SK Innovation: `going concern 39,425,231.46`, `p = 0.12`, `"V"`, `50%` → `proceeds = 19,712,615.73`; `operating assets = 39,425,231.46 × 0.88 + 19,712,615.73 × 0.12 = 37,059,717.57`.

**Concepts.** concepts/dark-side-difficult/distress-and-failure-adjusted-value.md, concepts/dark-side-difficult/truncation-and-political-risk.md, concepts/narrative-numbers/life-cycle-uncertainty.md

---

### M49 `equity_bridge_and_per_share`
**Purpose.** The chain from operating-asset value to value per share. Every adjustment exactly once.

**Inputs.** `value_of_operating_assets, cash_adjusted, cross_holdings_value, other_non_operating_assets, market_value_of_debt (or book debt + lease debt), other_claims (pension underfunding, contingent liabilities), minority_interest_value, option_value, restricted_shares_granted, shares_outstanding`; `frame: "going_concern"|"liquidation"`; `complexity_discount_pct`.

**Outputs.** `value_of_firm, value_of_equity, value_of_common_stock, value_per_share, price_as_pct_of_value`.

**Computation.**
```
  Value of operating assets
+ Cash and marketable securities            (M47; trapped-cash haircut applied)
+ Value of cross holdings                   (M47)
+ Value of other non-operating assets       (M47)
= Value of firm
− Value of debt                             (MARKET value in the going-concern frame; FACE value in liquidation)
− Other claims                              (pension shortfall, contingent liabilities × probability, minority interests)
= Value of equity
− Value of equity options                   (M46)
= Value of common stock
÷ Shares outstanding                        (ACTUAL, plus already-granted restricted shares; NOT diluted)
= Value per share
```
Contingent liability `= probability × expected size`. Liquidation frame: `Equity = liquidation value of assets − face value of debt`. Optional firm-level complexity discount from M64's PBV regression (`−0.003 of P/BV per 10-K page`).

**Reference tables.** None.

**Edge cases.** **The classic double counts:** cash counted in the flows *and* added back; a pension shortfall in the WACC *and* in the bridge; option value subtracted *and* diluted shares used; brand value added on top of brand-driven margins. Book debt in the bridge but market debt in the weights is the Ginzu convention and is intentional — state it.

**Test vector.** Tesla: `operating assets 686,689.9 − debt 10,158 − minorities 0 + cash 16,095 + non-op 0 = equity 692,626.9`; `− options 51,070.25 = 641,556.7`; `÷ 1,123 shares = 571.29`; `price/value = 1,200/571.29 = 2.1005`.

**Concepts.** concepts/dcf-model-choice-loose-ends/equity-value-bridge.md, concepts/dcf-model-choice-loose-ends/debt-and-other-claims-in-the-bridge.md, concepts/dcf-model-choice-loose-ends/complexity-discount.md, concepts/dcf-model-choice-loose-ends/restricted-stock-and-future-grants.md

---

## S9 — Distress

### M50 `bond_implied_distress_probability`
**Purpose.** Read the market's annual probability of distress out of a traded bond price.

**Inputs.** `coupon_rate, maturity_years, riskfree_rate, market_price, face = 1000, recovery_rate = 0`.

**Outputs.** `p_annual, cumulative_probability(n), model_price(p)`.

**Computation.**
```
ModelPrice(π) = Σ_{t=1..T} [coupon × (1−π)^t/(1+rf)^t] + face × (1−π)^T/(1+rf)^T
solve ModelPrice(π) = market price for π            # monotone decreasing in π → unique root
P(distress within n years) = 1 − (1 − π)^n
```
The model discounts at the **riskfree** rate and assumes **zero recovery** — both are modelling assumptions, not defects.

**Reference tables.** None.

**Edge cases.** A price above the riskfree-discounted promised value has no root in `[0,1)` — return `π = 0` or raise. Prices near zero drive `π → 1`. When several bonds trade, the choice of bond is judgment; run all and report the range. Illiquidity in the bond price inflates the implied probability.

**Test vector.** `distress.xls`: 8-year 12% coupon, face 1000, `rf = 5%`, price 653 → **`π = 0.13531709403063646`**; 5-year cumulative `0.5166247973245933`; 10-year `0.7663484134385095`; model price at that π = 652.9999998.

**Concepts.** concepts/dark-side-difficult/bond-implied-distress-probability.md, concepts/dark-side-difficult/distress-and-failure-adjusted-value.md

---

### M51 `equity_as_option_engine`
**Purpose.** Value the equity of a levered firm as a call on firm value — plus the three consequences that fall out of it.

**Inputs.** `firm_value S, face_value_of_debt K, debt_life t, sigma_firm, riskfree r`; troubled-firm estimation inputs `(w_equity, w_debt, sigma_equity, sigma_debt, rho_ED, face_by_tranche, duration_by_tranche, coupon_cumulation)`; conglomerate inputs `(V1, V2, K1, K2, σ1, σ2, ρ12)`; risk-shift inputs `(project_npv, sigma_new)`; **trigger** `market_debt_to_capital`.

**Outputs.** `equity_value, implied_debt_value, implied_interest_rate, default_spread_implied, sigma_firm, option_life, wealth_transfer, sensitivity_table`.

**Computation.**
- `E = S·N(d1) − K·e^(−rt)·N(d2)`, `d1 = [ln(S/K) + (r + σ²/2)t]/(σ√t)`, `d2 = d1 − σ√t`.
- `Implied debt value = S − E`; `implied interest rate = (K/debt value)^(1/t) − 1`; `default spread = that rate − r`.
- **Firm-value variance from traded securities:** `σ²_firm = w_E²σ_E² + w_D²σ_D² + 2 w_E w_D ρ_ED σ_E σ_D`.
- **Option life from a debt schedule:** `t = Σ(Face_i × Duration_i)/Σ Face_i` (face-value-weighted duration; fall back to weighted maturity). **Strike** `K` = short-term debt at face + long-term debt at `face + cumulated nominal coupons`.
- **Distressed-equity decomposition:** `Δ firm value = Δ equity value + Δ debt value`; `debtholders' share of the loss = Δfirm − Δequity`. Equity stays strictly positive for any `S > 0` while `t > 0` and `σ > 0`.
- **Risk shifting:** recompute `E` with `S_new = S_old + NPV` and `σ_new`; stockholders take the project whenever `E_new > E_old`, even at negative NPV; `transfer = E_new − E_old = D_old − D_new`.
- **Conglomerate merger:** `σ²_combined` by the two-asset formula; `V = V1 + V2`, `K = K1 + K2`; `transfer to bondholders = (E1 + E2) − E_combined`, positive whenever `ρ12 < 1`.
- **Trigger rule for using this model at all:** the firm is loss-making **and** its market-value debt-to-capital ratio **> 50%**.

**Reference tables.** M04.

**Edge cases.** The naive "new equity = new firm value − old market value of debt" is wrong — debt absorbs part of the loss. Distress usually raises `σ`, and acceleration/covenant breaches shorten the effective `t`; holding both fixed after a shock overstates equity.

**Test vector.** Base case: `S = 100m, K = 80m, t, σ, r` → `E = 75.94m`, `implied debt = 24.06m`, `implied rate = 12.77%`. After a catastrophic drop: `E = 30.44m`, `debt = 19.56m`. Risk shift (σ 40% → 50%, NPV −2m): `E 75.94 → 77.71`, `D 24.06 → 20.29`, transfer **1.77m**. Conglomerate: `σ²_combined = 0.154`, transfer **2.98m**. Eurotunnel: duration **10.93 yrs**, `σ²_firm = 0.0335`, `E = £122m`, `D = £2,190m`, implied yield **13.65%**.

**Concepts.** concepts/real-options/equity-as-call-option.md, concepts/real-options/distressed-equity-time-value.md, concepts/real-options/risk-shifting-and-stockholder-bondholder-conflict.md, concepts/real-options/conglomerate-merger-wealth-transfer.md, concepts/real-options/equity-option-inputs-troubled-firms.md, concepts/deliverables-worked-examples/equity-as-call-option-valuation.md

---

## S10 — Capital structure

### M52 `optimal_capital_structure_schedule`
**Purpose.** The cost-of-capital approach: rebuild beta, rating, cost of debt, tax rate, WACC and firm value at every debt ratio from 0% to 90%, then pick the optimum.

**Inputs.** `ebitda, depreciation, capital_spending, interest_expense, marginal_tax_rate, current_rating, current_pretax_kd, shares, price, cash, book_debt, mv_debt (given/estimate/book), avg_maturity, lease inputs, riskfree_rate, erp, country_default_spread, table_choice (1|2), refinance_existing_debt: bool, adjust_to_synthetic: bool, deduction_restriction: bool + measure ("EBITDA"|"EBIT") + cap_pct, indirect_bankruptcy_costs: bool + severity, grid = 0.0..0.9 step 0.1`.

**Outputs.** per debt ratio: `d, D/E, $debt, interest, coverage, rating, pretax_kd, t_used, after_tax_kd, levered_beta, cost_of_equity, WACC, firm_value, is_optimal`; plus `current_debt_ratio, current_WACC, current_EV, implied_growth, optimal_debt_ratio, optimal_WACC, optimal_EV, value_per_share_current, value_per_share_optimal`.

**Computation.**
1. Lease capitalisation and the current synthetic rating (M13, M18, M19, M22).
2. Current block: `MV equity = shares × price`; `EV = MV equity + MV debt + lease debt − cash`; `current d = (MV debt + lease debt)/(MV debt + lease debt + MV equity)`; `ke`, `kd_AT`, `WACC`.
3. `FCFF = (EBITDA − depreciation)(1 − t) + depreciation − capex` (working capital ignored in this engine).
4. **Implied growth backed out of the current price:** `g = (EV × WACC_current − FCFF)/(EV + FCFF)`; then `g_used = min(g, riskfree)`; if FCFF ≤ 0, `g` is "NA" → use the perpetual-growth branch with `g = min(riskfree, 0.06)`.
5. `Unlevered beta = current beta/(1 + (1 − t)·current D/E)`.
6. For each `d` in the grid — **capital base held constant at (current MV equity + current total debt incl. leases)**:
   - `$Debt(d) = d × capital base`; `D/E = d/(1−d)`.
   - `Interest(d) = kd(d) × $Debt(d)` if refinancing; else `old interest + kd(d) × ($Debt(d) − current debt)` above the current ratio, and `(old interest/book debt) × $Debt(d)` below it.
   - Coverage → rating → spread → `kd(d) = riskfree + spread + country spread`. **Circular** — fixed-point per column (§18-C2).
   - Tax caps via M32 → `t_used(d) = min(t_EBIT, t_cap)`.
   - `β_L(d) = β_u(1 + (1 − t_used(d))·D/E)`; `ke(d) = rf + β_L(d)·ERP`; `kd_AT(d) = kd(d)(1 − t_used(d))`; `WACC(d) = ke(d)(1−d) + kd_AT(d)·d`.
   - **Firm value, no-IBC branch:** `V(d) = EV_current × [1 + (WACC_current − WACC(d))/(WACC(d) − g_used)]`.
     **IBC branch (or when implied g exists):** `V(d) = [EBIT(d)(1 − t) − (capex − depreciation)] × (1 + g)/(WACC(d) − g)`.
   - Optimal `d* = argmax V(d)` (equivalently `argmin WACC` when cash flows do not move with `d`).
7. `Value per share at the optimum = (V(d*) − EV_current)/shares + current price` — the whole gain accrues to today's holders.

**Reference tables.** M08 (coverage/rating/spread + drop-in-EBITDA), M06 (country spread).

**Edge cases.** Zero interest → coverage sentinel → top rating; the `d = 0` column is hard-coded to the top rating. Negative taxable income produces a negative tax (full offset assumed) but the *tax-benefit* rate is still capped. Non-refinancing branch divides by book debt — require `refinance = True` or `book debt > 0`. Rating 2-cycles: §18-C2.

**Test vector.** `capstru.xlsx` Facebook: leases → debt 2,088.20 at kd 3.21603%; restated EBIT 17,520.98, interest 77.157; coverage 227.08 → Aaa/AAA; `ke = 8.808%`; current `d = 0.377%`; `WACC = 8.782%`; `EV = 515,901.2`; implied `g = 7.308%` capped to 2.55%; `β_u = 1.04762`.
Schedule: `0% → WACC 8.794%, V 514,930.5`; `10% → 8.482%, 541,995.5`; **`20% → A3/A−, kd 3.836%, WACC 8.245%, V 564,585.2 (optimal)`**; `30% → Caa/CCC, 9.138%, 488,004.9`; `40% → C2/C, t_used 0.23761, 11.238%, 370,069.8`. Value per share `190 → 206.75`.

**Concepts.** concepts/capital-structure/cost-of-capital-approach.md, concepts/capital-structure/synthetic-rating-and-cost-of-debt.md, concepts/capital-structure/levered-beta-schedule.md, concepts/capital-structure/tax-benefit-of-debt.md, concepts/deliverables-worked-examples/optimal-debt-ratio-wacc-schedule.md

---

### M53 `enhanced_coc_ibc`
**Purpose.** The same schedule with operating income falling as the rating deteriorates — indirect bankruptcy costs made explicit.

**Inputs.** M52's, plus `ibc_severity: "Low"|"Medium"|"High"`, `current_rating_drop`.

**Outputs.** M52's, plus `ebitda_by_debt_ratio, ebit_by_debt_ratio` and a value cliff that is steeper than M52's.

**Computation.** `EBITDA(d) = EBITDA_base × (1 + drop(rating(d)))` where `drop` is the negative fraction from M08's IBC table at the chosen severity. `EBIT(d) = EBITDA(d) − depreciation` (depreciation held constant). The rest follows M52, with `EBIT(d)` feeding **both** the coverage ratio and the value. **Normalisation:** if the firm is *already* distressed at its current rating, gross the base up first: `EBITDA_base = current EBITDA/(1 + drop(current rating))`. Adds a second fixed-point loop (rating → drop → EBITDA → coverage → rating).

**Edge cases.** The drop lookup runs regardless of the flag in the sheet; only the EBITDA substitution is gated. Severity is a pure assumption about how customers, suppliers and employees would punish distress.

**Test vector.** Structural: with `severity = "Medium"`, a `Caa/CCC` rating applies a **−0.40** EBITDA haircut; a `Baa2/BBB` rating applies **−0.10**; `A2/A` and above apply 0. Assert the schedule's optimum shifts to a lower debt ratio than M52's on the same inputs.

**Concepts.** concepts/capital-structure/enhanced-cost-of-capital-approach.md, concepts/capital-structure/downside-risk-and-rating-constraints.md

---

### M54 `apv_engine`
**Purpose.** The additive route: unlevered value plus tax benefits minus expected bankruptcy costs, at every debt ratio.

**Inputs.** `mv_equity, mv_debt, lease_debt, marginal_tax_rate, bankruptcy_cost_pct_of_value, ebitda, depreciation, interest_expense, riskfree, erp, beta, table_choice, grid`.

**Outputs.** per `d`: `$debt, t_eff, tax_benefit, rating, p_default, expected_bankruptcy_cost, levered_value`; plus `unlevered_value, optimal_d, max_levered_value`.

**Computation.**
- `Current firm value = MV equity + MV debt + lease debt` (**cash is NOT netted in this model**).
- `Current tax benefit = t × current total debt`; `Current expected bankruptcy cost = p(current rating) × BC% × current firm value`.
- **`Unlevered value = current firm value − current tax benefit + current expected bankruptcy cost`.**
- Per `d`: `$Debt = d × current firm value`; interest `= kd(d) × $Debt` (rating loop as in M52); `t_eff = t` if `interest ≤ EBIT`, else `t × EBIT/interest`; **`Tax benefit = $Debt × t_eff`**; `p_default` from M08's APV probability column; **`Expected bankruptcy cost = p_default × BC% × (unlevered value + tax benefit)`**; `Levered value = unlevered + tax benefit − expected bankruptcy cost`; `d* = argmax`.
- Ancillary (not in the value): `β_u = β/(1+(1−t)D/E)`; `β_L(d) = β_u(1+(1−t_eff)D/E)`; `ke(d) = rf + β_L(d)·ERP`.

**Reference tables.** M08 (APV vintage with bankruptcy probabilities).

**Edge cases.** The APV probability column is **non-monotonic** (Ba1/BB+ 0.10 sits below Ba2/BB 0.1663; B2/B 0.368 above Baa2 0.0754) — this is why the Hormel optimum lands at 80% rather than 70%. Reproduce verbatim. No growing-perpetuity revaluation here; APV is purely additive. `maturity = 0` in the MV-of-debt estimate collapses to book value.

**Test vector.** `apv.xls` Hormel: `current firm value 4,673.240`, `tax benefit 196.869`, `expected BC 0.81782` → **`unlevered value = 4,477.189`**. Schedule: `0.7 → B1/B+, p 0.25, BC 361.61, levered 5,424.09`; **`0.8 → Ba1/BB+, p 0.10, tax benefit 1,495.44, BC 149.32, levered 5,823.31 (optimal)`**; `0.9 → Ca2/CC, p 0.70, BC 1,069.82, levered 5,043.43`.

**Concepts.** concepts/capital-structure/apv-approach.md, concepts/capital-structure/pathways-to-the-optimal-debt-ratio.md

---

### M55 `recap_value_and_buyback_engine`
**Purpose.** Price the move to the optimal ratio, and the buyback that executes it — including the EPS effect and the wealth transfer.

**Inputs.** `ev_current, wacc_old, wacc_new, fcff, riskfree, growth_g, shares, price, debt_current, debt_at_optimal, buyback_price, cash`; buyback-sheet inputs `beta, debt, cash, kd_existing, kd_new, net_income, interest_income, fair_value_per_share, shares_bought, cash_funding, debt_funding, erp, tax_rate`.

**Outputs.** `excess_debt_capacity, implied_growth, value_gain_full, value_gain_incremental, ev_after, rational_buyback_price, value_per_remaining_share, post_buyback_beta/ke/kd/WACC/EV/equity/price, wealth_transfer, transfer_per_share, price_with_transfer, eps_before/after, pe_before/after`.

**Computation.**
- `Excess debt capacity = optimal d × total capital − current debt`.
- `FCFF = EBIT(1−t) + depreciation − capex − ΔNCWC`; `implied g = (EV × WACC_old − FCFF)/(EV + FCFF)`.
- **Full revaluation:** `New firm value = FCFF(1+g)/(WACC_new − g)`; `value gain = new − current EV`.
- **Incremental method:** `annual saving = EV × (WACC_old − WACC_new)`; `increase = annual saving/(WACC_new − g)` with `g = riskfree`; `EV after = EV + increase`.
- `Rational (indifference) buyback price = current price + value gain/shares`.
- General buyback arithmetic at any price `P`: `shares after = shares − (increase in debt)/P`; `equity after = optimal EV + cash − debt at optimal`; `value per remaining share = equity after/shares after`.
- **Buyback value/EPS engine (`buybacks.xls`):** `E1_mech = E0 − buyback price × shares bought`; `D1 = debt + new debt`; `β_u = β0/(1+(1−t)D/E0)`; `β1 = β_u(1+(1−t)D1/E1_mech)`; `ke1 = rf + β1·ERP`; **`kd1_AT = cost of NEW debt × (1−t), applied to ALL debt`** (§19-Q13); `WACC1`; **`EV1 = EV0 × (WACC0 − rf)/(WACC1 − rf)`** (a growing-perpetuity revaluation with `g = rf`); `Firm1 = EV1 + cash remaining`; `E1_value = Firm1 − D1`; `Price1 = E1_value/shares1`.
- **Wealth transfer:** `(fair value per share − buyback price) × shares bought`; `per remaining share = transfer/shares1`; `price with transfer = Price1 + that`.
- **EPS:** `NI1 = NI − interest income from cash − new debt × kd_new × (1−t)` (§19-Q14: the sheet subtracts the **full, un-prorated, pre-tax** interest income); `EPS1 = NI1/shares1`; `PE1 = Price1/EPS1`. **EPS accretion is not value creation** — report both and say so.

**Reference tables.** None.

**Edge cases.** `WACC1 ≤ rf` breaks the EV revaluation — guard. The sheet does not check that `cash funding + debt funding == buyback cost`, nor that cash funding ≤ cash — validate. Buying back all shares breaks per-share math.

**Test vector.** `buybacks.xls`: buy 200 shares at 65 (cost 13,000; 3,000 cash + 10,000 new debt at 4.25%). `D/E 0.133 → 0.2426`; `β 1.2 → 1.2730917537161761`; `ke 0.0875 → 0.09115458768580881`; `WACC 0.07986939269349298 → 0.07833534933086801`; `EV1 = 132,030 × (0.079869 − 0.0275)/(0.078335 − 0.0275) = 136,014.23041905585`; `equity 110,984.23041905585`; **`Price1 = 61.65790578836436`**; transfer `(75 − 65) × 200 = 2,000` → `+1.1111111111111112`/share → `62.769016899475474`; `EPS 2.00 → 2.047222`; `PE 30.0 → 30.11783729146699`.
Capstru companion: Facebook buyback at 67.71 → `108,749.84` new debt buys `1,606.11` shares → `1,299.69` remain → **`378.58`**/share.

**Concepts.** concepts/capital-structure/recapitalization-and-buyback-price.md, concepts/dividend-policy/buyback-value-and-eps-effect.md, concepts/deliverables-worked-examples/recapitalization-value-and-stress-test.md, concepts/capital-structure/moving-to-the-optimal.md

---

### M56 `downside_stress_and_rating_constraint`
**Purpose.** Stress the optimum against bad earnings and price the cost of a rating floor.

**Inputs.** `ebit_history: list[float]`, `haircuts: list[float]`, `n_sigma`, `required_rating`, plus M52's full input set.

**Outputs.** `stdev_of_pct_change_in_ebit, stressed_ebit, optimal_ratio_by_haircut, constrained_optimal_ratio, cost_of_constraint`.

**Computation.** `σ(% change in EBIT)` from the firm's own history. For each haircut `h`: `EBIT_h = EBIT × (1 − h)` and re-run M52 → record the optimal ratio. Standard stress: `stressed EBIT = expected EBIT − n_sigma × σ(EBIT)` (the deliverable uses `n_sigma = 3`), fed into the same coverage → rating → spread → WACC machinery. `Cost of a rating constraint = firm value at the unconstrained optimum − firm value at the highest debt ratio consistent with the required rating`.

**Test vector.** Structural assertion: re-running M52's Facebook schedule with `EBIT × (1 − h)` must move the argmax monotonically downward in `h`; the cost of an `A3/A−` floor is `V(d*) − V(d_max consistent with A3/A−)`.

**Concepts.** concepts/capital-structure/downside-risk-and-rating-constraints.md, concepts/deliverables-worked-examples/recapitalization-value-and-stress-test.md, concepts/deliverables-worked-examples/qualitative-debt-tradeoff.md

---

### M57 `debt_design_regressions`
**Purpose.** Turn the firm's macro exposures and asset duration into debt-design parameters, and benchmark its debt ratio against peers.

**Inputs.** Top-down: `operating_income[], market_cap[], total_debt[]` by period; macro series `Δ(long bond rate) (absolute), %ΔGDP, Δ(inflation rate) (absolute), %Δ(dollar)`. Bottom-up: `businesses: list[(sic_code, value)]`. Duration: `project cash flows, discount rate`; `bond coupons, face, maturity, yield`. Regression benchmarking: peer panel or posted coefficients.

**Outputs.** `duration_fv, duration_oi, cyclicality, inflation_sensitivity, currency_sensitivity, slopes_with_t_stats, firm_coefficients_bottom_up, project_duration, bond_duration, predicted_debt_ratio, over_under_levered`.

**Computation.**
- `ΔV_t = (MarketCap_t + Debt_t)/(MarketCap_{t−1} + Debt_{t−1}) − 1`; `ΔOI_t = OI_t/OI_{t−1} − 1`.
- **Four separate univariate OLS regressions per dependent variable** (not one multiple regression): `ΔV` (and `ΔOI`) on each of the four macro changes.
- `Duration of assets = max(0, −slope of ΔV on Δ interest rates)`; `Cyclicality = slope on %ΔGDP`; `Inflation sensitivity = slope on Δ inflation`; `Currency sensitivity = slope on %Δ dollar`.
- Reading rule: prefer **firm-value** slopes for duration and cyclicality, **operating-income** slopes for inflation and currency.
- Bottom-up: `firm coefficient = Σ weight_i × sector coefficient_i`, weights = business values.
- `Project duration = Σ t·PV(CF_t)/Σ PV(CF_t)`; bond duration via M01.
- **Peer/market benchmarking:** `Debt ratio = a + b·(tax rate) + c·(earnings variability) + d·(EBITDA/EV) …`. Posted fits: global auto sector `Debt/capital = 0.09 + 0.63·ETR + 1.01·(EBITDA/EV) − 0.93·(Capex/EV)`, R² 21%; US market-wide 2014 `DFR = 0.27 − 0.24·ETR − 0.10·g − 0.065·INST − 0.338·CVOI + 0.59·(E/V)`, R² 8%. Verdict: `actual > predicted → over-levered`.

**Reference tables.** M10 (sector macro coefficients by 2- and 4-digit SIC).

**Edge cases.** **Variable conventions differ by variable:** bond-rate and inflation changes are **absolute** rate changes; GDP and the dollar are **percentage** changes. Mixing them silently inverts signs. The 4-digit and 2-digit sector tables use different sign conventions (§19-Q9). An 8% R² regression is weak evidence — report it.

**Test vector.** `macrodur.xls`: slope of ΔFirmValue on Δbond rate `= +6.081218` → `duration_FV = 0` (floored); slope of ΔOI `= −1.462709` → `duration_OI = 1.462709`; `cyclicality = −1.386655 (FV) / −0.433924 (OI)`; `inflation = 0.955412 / −1.601873`; `currency = −0.279654 / −0.581120`.

**Concepts.** concepts/capital-structure/macro-sensitivity-regressions.md, concepts/capital-structure/project-duration-and-project-financing.md, concepts/capital-structure/relative-and-regression-analysis.md, concepts/capital-structure/debt-design-framework.md, concepts/deliverables-worked-examples/debt-design-deliverable.md

---

## S11 — Project analysis

### M58 `capital_budgeting_engine`
**Purpose.** A full project cash-flow model from revenue and expense assumptions to NPV, IRR and ROC.

**Inputs.** `initial_investment, opportunity_cost, lifetime (≤10), salvage_value, depreciation_method (1=SL, 2=DDB), tax_credit_rate, other_nondepreciable_investment, initial_working_capital, wc_pct_of_revenues, wc_salvageable_fraction, revenue_year1, variable_pct_of_revenues, fixed_year1, tax_rate, discount_approach (1=direct, 2=CAPM/WACC), direct_rate, beta, riskless_rate, market_risk_premium, debt_ratio, pretax_cost_of_borrowing, g_revenue[9], g_fixed[9]`.

**Outputs.** `discount_rate, initial_outlay, annual table (revenues, variable, fixed, EBITDA, depreciation, EBIT, tax, EBIT(1−t), ΔWC, NATCF, book value schedule), salvage flows, discounted CF, npv, irr, roc`.

**Computation.**
- `r = direct_rate` or `ke(1 − DR) + kd(1 − t)·DR`, `ke = Rf + β·MRP`.
- `Net investment = investment × (1 − tax credit rate)`; `Initial outlay = net investment + initial WC + opportunity cost + other investment`; `CF_0 = −outlay`.
- `Rev_1` given; `Rev_t = Rev_{t−1}(1 + g_rev,t)`; `Variable_t = pct × Rev_t`; `Fixed_t = Fixed_{t−1}(1 + g_fixed,t)`; `EBITDA_t = Rev − Var − Fixed`.
- Depreciation: SL `= (investment − salvage)/lifetime`; **DDB `= min((2/lifetime) × BV_begin,t, BV_begin,t − salvage)`**, `BV_end = BV_begin − Dep`; book value parks at salvage.
- `EBIT_t = EBITDA_t − Dep_t`; `Tax_t = t × EBIT_t` (**negative EBIT → negative tax, implicit full loss offset**); `EBIT(1−t)_t`.
- `WC_t = wc_pct × Rev_t`; `ΔWC_1 = wc_pct × Rev_1 − initial WC`; `ΔWC_t = wc_pct × (Rev_t − Rev_{t−1})` for `t ≥ 2`.
- `NATCF_t = EBIT(1−t)_t + Dep_t − ΔWC_t`.
- Salvage in the **final project year** (year = `lifetime`, not necessarily year 10): equipment salvage; `WC salvage = salvageable fraction × WC_lifetime`.
- `DCF_t = (NATCF_t + equipment salvage_t + WC salvage_t)/(1+r)^t`; `NPV = Σ_{t=0..L} DCF_t`; `IRR` on the stream including `t = 0` and final-year salvage.
- **`ROC = mean(EBIT(1−t)_t)/mean(BV_begin,t)` using beginning-of-year *equipment* book value only** — working capital and opportunity cost are excluded from the denominator.
- `LifetimeIndex_t = 1 if t ≤ lifetime else 0` zeroes years beyond the life.

**Reference tables.** None.

**Edge cases.** The DDB cap at `BV − salvage` is the regression test (year 8 = 485.7600000000075 in the worked example). Year-1 ΔWC can be nonzero or negative when the entered initial WC ≠ `wc_pct × Rev_1`.

**Test vector.** `capbudg.xls`: `r = 0.1295 × 0.7 + 0.09 × 0.6 × 0.3 = 0.10685`; `outlay = 45,000 + 10,000 + 7,484 = 62,484`; DDB schedule `10,000, 8,000, 6,400, 5,120, 4,096, 3,276.8, 2,621.44, 485.76, 0, 0`; year-10 DCF `= (17,569.2 + 10,000 + 14,641)/1.10685^10 = 15,294.303917302585`; **`NPV = 47,927.64998482676`, `IRR = 0.2355393602386762`, `ROC = 0.6011971746005914`**.

**Concepts.** concepts/project-returns/capital-budgeting-model.md, concepts/project-returns/earnings-vs-cash-flows.md, concepts/project-returns/project-hurdle-rate-selection.md

---

### M59 `decision_rules_toolkit`
**Purpose.** Every investment decision measure and the rules for choosing between conflicting ones.

**Inputs.** `cash_flows: list[float]` (t=0 first), `hurdle_rate`, `rate_grid`, `lives: list[int]`, `capital_budget`.

**Outputs.** `npv, npv_profile, irr(s), sign_changes, mirr, profitability_index, payback, discounted_payback, equivalent_annuity, replicated_npv, ranking`.

**Computation.**
- `NPV = Σ CF_t/(1+r)^t`; accept if `NPV > 0`. `IRR` solves `NPV(r) = 0`; accept if `IRR > hurdle`. NPV profile = NPV over a rate grid.
- **Multiple IRRs:** count sign changes; the number of IRRs can equal that count. Return all roots and flag.
- `MIRR`: compound intermediate flows forward at the hurdle rate to `TV = Σ CF_t(1+r)^{n−t}`, then solve `Investment(1+MIRR)^n = TV`.
- `Profitability index = NPV / initial investment` — the capital-rationing ranking rule.
- `Payback` = first year cumulated undiscounted CF turns positive (interpolate within the year); `discounted payback` uses cumulated PVs.
- **Different lives:** `Equivalent annuity = NPV / PVAF(r, n)`; or replicate each project to the least common multiple of the lives and compare replicated NPVs.
- Hurdle-rate matching (R3): firm flows → cost of capital; equity flows → cost of equity.
- Break-even and sensitivity: recompute `NPV(x)` and `IRR(x)` over a grid of one input.

**Edge cases.** Scale and timing conflicts between NPV and IRR — NPV wins unless capital is genuinely rationed, then PI. IRR's reinvestment assumption is the reason MIRR exists.

**Test vector.** Rio Disney (lecture case): `NPV = $3,296M`, `IRR = 12.60%` at a hurdle rate of 8.46% → accept on both.

**Concepts.** concepts/project-returns/npv-and-irr-mechanics.md, concepts/project-returns/npv-vs-irr-conflicts.md, concepts/project-returns/comparing-projects-different-lives.md, concepts/project-returns/uncertainty-payback-sensitivity-simulation.md, concepts/project-returns/investment-analysis-first-principles.md

---

### M60 `equity_side_project_engine`
**Purpose.** The same project seen from the equity investors' side, with explicit project financing.

**Inputs.** `loan_amount, loan_rate, loan_years`, project operating assumptions, `cost_of_equity, tax_rate, salvage_value`.

**Outputs.** `amortization schedule (payment, interest, principal, balance)`, `income statement`, `book equity roll-forward`, `roe_by_year, average_roe, equity_spread, cash_flow_to_equity, equity_npv, equity_irr`.

**Computation.**
- `Payment = Loan × r/(1 − (1+r)^(−n))`; `Interest_t = Balance_{t−1} × r`; `Principal_t = Payment − Interest_t`.
- `BV equity_t = BV assets + BV working capital − debt outstanding`; `ROE_t = NI_t / average BV equity_t` where `average = (BV_{t−1} + BV_t)/2`.
- `CF to equity_t = NI_t + D&A_t − CapEx_t − ΔWC_t − Principal repayments_t (+ salvage in the final year)`.
- `Equity NPV = Σ CF to equity_t/(1 + ke)^t`; `equity IRR` by root find.
- `Equity spread = ROE − cost of equity`.
- Side costs and synergies: `Adjusted NPV = stand-alone NPV − PV(after-tax side costs) + PV(synergy at the receiving business's cost of capital)`. Opportunity cost of an owned resource: `after-tax proceeds = market value − t_cg × (market value − book value)`, or the PV of foregone rentals, or replacement cost. Excess capacity: PV of lost sales, or `PV(earlier capacity investment) − PV(later capacity investment)`.
- Incremental-cash-flow adjustments: sunk costs charged at t=0 and their depreciation tax shield removed; allocated overhead split by an OLS of `G&A on revenues` — the slope is the incremental cost per revenue dollar.

**Edge cases.** Cost of equity must be the *business's*, not the company's, when the project differs in risk.

**Test vector.** Netflix Fit: `TV = CF_11/(r_Fit − g) = 244.33/(0.0801 − 0.01) = $3,486M`; `Project ERP = 5.25% + Σ(revenue weight × regional CRP) = 6.27%`; total NPV `= NPV(FCFF at 8.01%) + NPV(synergy at 8.93%)`.

**Concepts.** concepts/project-returns/equity-side-project-analysis.md, concepts/project-returns/opportunity-costs-and-side-costs.md, concepts/project-returns/project-synergies.md, concepts/project-returns/incremental-cash-flow-principle.md, concepts/project-returns/netflix-fit-case.md

---

## S12 — Relative valuation

### M61 `multiple_constructor`
**Purpose.** Build any multiple consistently, with the numerator, denominator, timing and share-count conventions pinned.

**Inputs.** `mv_equity, mv_debt, cash, minority_interest, book_equity, book_debt`; denominators `eps (current|trailing|forward), net_income, book_value, revenues, ebitda, ebit, fcff, fcfe, invested_capital, users/subscribers`; `share_count_convention: "primary"|"fully_diluted"|"partially_diluted"|"actual_plus_option_value"`.

**Outputs.** `firm_value, enterprise_value, invested_capital, multiple`, `consistency_check: bool`, `uniformity_report`.

**Computation.**
- `Firm value = MV equity + MV debt`; **`Enterprise value = MV equity + MV debt − cash`**; `Invested capital = BV equity + BV debt − cash`.
- `Multiple = numerator/denominator`. **Consistency test:** equity numerator with equity denominator; firm/EV numerator with operating denominator. `Price/EBITDA` is inconsistent and must be rejected.
- Cash comes out of EV because interest income is not in EBITDA or EBIT.
- Cross-holdings: a consolidated but partly owned subsidiary puts 100% of its EBITDA in the denominator while you own part of the equity — subtract minority interests.
- Timing variants for PE: current (last fiscal-year EPS), trailing (last 12 months), forward (next-year forecast). Never mix across firms.
- Share-count convention: primary ignores options; fully diluted counts all; the preferred route is `actual shares` with option value subtracted (M46) — and the drag answer brackets the other two.

**Edge cases.** Negative denominators make the multiple non-computable — the firm silently drops out of the sample, which biases every comparison (record the drop count, M63).

**Test vector.** `EV/EBITDA = (MV equity + MV debt − cash)/EBITDA`; Ryder System `5,158.04/1,838.26 = 2.81` against a trucking-sector average of 5.61 — and the low multiple is *deserved* once CapEx/EBITDA is controlled for.

**Concepts.** concepts/relative-valuation/multiple-definition-tests.md, concepts/relative-valuation/four-step-multiple-framework.md, concepts/relative-valuation/pricing-vs-value.md

---

### M62 `intrinsic_multiple_deriver`
**Purpose.** Turn any multiple back into the DCF it came from, and produce the justified value of that multiple from fundamentals.

**Inputs.** `ke, wacc, g, gn, n, payout, payout_stable, reinvestment_rate, roe, roc, net_margin, after_tax_operating_margin, tax_rate, depreciation_to_ebitda, capex_to_ebitda, wc_change_to_ebitda`.

**Outputs.** the justified multiple, its companion variable, and a sensitivity grid.

**Computation (the master map, all in stable growth; subscript 1 = next year).**
Equity side: `P/Div₁ = 1/(ke − g)` · `P/E₁ = Payout/(ke − g)` · `P/E₀ = Payout(1+g)/(ke − g)` · `P/BV = ROE × Payout(1+gn)/(ke − gn)` = **`(ROE − gn)/(ke − gn)`** · `P/Sales₁ = Net margin × Payout/(ke − g)`.
Enterprise side: `EV/FCFF₁ = 1/(WACC − g)` · `EV/EBIT₁(1−t) = (1 − RIR)/(WACC − g)` · `EV/EBIT₁ = (1−t)(1 − RIR)/(WACC − g)` · `EV/Sales₁ = ATOM × (1 − RIR)/(WACC − g)` · `EV/IC = ROIC × (1 − RIR)/(WACC − g)` = **`(ROC − g)/(WACC − g)`**.
`EV/EBITDA = (1−t)/(WACC−g) + [Dep×t/EBITDA]/(WACC−g) − [CapEx/EBITDA]/(WACC−g) − [ΔWC/EBITDA]/(WACC−g)`.
Two-stage PE: `PE = Payout(1+g)[1 − (1+g)^n/(1+r)^n]/(r−g) + Payout_n(1+g)^n(1+gn)/[(r−gn)(1+r)^n]`. **A negative denominator in the first term when `r < g` is normal — the bracket is also negative, so the term is positive.**
`PEG = PE/growth in percentage points`; intrinsic PEG = the two-stage PE expression divided by `g`.
Brand value: `= [(V/S)_branded − (V/S)_generic] × Sales`, holding revenues, capital turnover, cost of capital and growth period fixed and letting `ROC = margin × sales/capital` and `g = RIR × ROC` adjust.
**Companion variables:** PE → growth; PEG → risk, payout, level of growth; PBV → ROE; EV/IC → ROIC; EV/Sales & PS → margin; EV/EBITDA → reinvestment needs, tax rate, cost of capital.

**Edge cases. Internal consistency is mandatory:** `g = (1 − payout) × ROE` and `g = RIR × ROC`. Feeding inconsistent triples produces a "justified" multiple no firm could sustain (the corpus's own example: ROE 15%, payout 40%, g 4% is inconsistent — sustainable g is 9%). Never assume linearity in growth or beta.

**Test vector.** Two-stage lecture case: `g 25% for 5 years, payout 20%, then g 8% with payout 50%, β 1.0, rf 6%, ERP 5.5% → r = 11.5%` → **`intrinsic PE = 28.75`**, **`PEG = 1.15`**. EV/EBITDA: `t 0.36, CapEx/EBITDA 0.30, Dep/EBITDA 0.20, WACC 0.10, g 0.05` → `12.80 + 1.44 − 6.00 − 0 = 8.24`. PBV: `(0.2022 − 0.04)/(0.09 − 0.04) = 3.24`. Brand: Coca-Cola `79,611.25 − 15,371.24 = $64,240M`.

**Concepts.** concepts/relative-valuation/intrinsic-multiple-derivation.md, concepts/relative-valuation/intrinsic-pe-fundamentals.md, concepts/relative-valuation/peg-ratio.md, concepts/relative-valuation/book-value-multiples.md, concepts/relative-valuation/ev-ebitda-multiple.md, concepts/relative-valuation/ev-sales-and-brand-value.md

---

### M63 `multiple_distribution_stats`
**Purpose.** Locate a multiple in its current distribution — and count what dropped out.

**Inputs.** `multiples: list[float|None]` across a universe, `universe_size: int`, `region`, `vintage`.

**Outputs.** `n_computable, drop_count, drop_pct, mean, median, percentiles (10/25/75/90), max`, `firm_percentile`.

**Computation.** Standard order statistics. **Report the median, never the mean** — the distributions are bounded at zero and unbounded above, so the mean sits far above the median (US trailing PE Jan-2021: mean 103.25, median 20.30). Record how many firms have no computable multiple and why (negative earnings, negative book value); PE samples silently drop money-losers, so a PE conclusion describes a biased subsample. Outliers lie almost entirely on the positive side — cap or use percentiles rather than trimming. Re-check by region and by vintage: the same number flips meaning (6× EBITDA was mid-distribution in the US in 2010, cheap by 2021's median of 16.6, and normal in Japan at a median of 8.46).

**Reference tables.** M10 (posted percentile tables by market and vintage).

**Test vector.** US Jan-2021: `7,584 firms, 2,481 with a trailing PE (67% drop)`, `mean 103.25`, `median 20.30`, `10th 7.68`, `90th 96.80`.

**Concepts.** concepts/relative-valuation/multiple-distribution-statistics.md, concepts/relative-valuation/comparable-selection-and-controls.md

---

### M64 `regression_pricing_engine`
**Purpose.** Predicted multiples from a fitted or posted regression, at sector, market, cross-market and young-company level.

**Inputs.** `mode: "fit"|"apply"`; fit: `panel of (multiple, fundamentals)`, `spec: list[str]`, `weights`; apply: `coefficient_set_id (region, multiple, vintage)`, firm fundamentals `(payout, beta, growth, roe, roic, debt_ratio, tax_rate, operating_margin, ln_revenues, cash_to_rev)`.

**Outputs.** `coefficients, t_stats, r_squared, predicted_multiple, predicted_price, over_under_pct`.

**Computation.**
- Generic: `Multiple = a + Σ b_i × Fundamental_i`; `Over/under (%) = actual/predicted − 1`.
- Drop regressors with `|t| < 1`; re-run. If the intercept is negative and predictions go negative, re-run through the origin.
- Check the correlation matrix — wrong-sign coefficients usually mean multicollinearity, not a finding.
- **Unit hazard:** SPSS output enters payout and growth in absolute percent (25 → 25); the slide-form equations use decimals with coefficients scaled by 100. Both appear in the corpus. `PE = 4.104 + 0.174·Payout% + 1.714·Beta + 2.304·Growth%` ≡ `PE = 5.91 + 17.10·Payout + 228.40·Growth` (decimal, beta dropped).
- **Posted coefficient library (Jan-2021 unless noted), by region:** PE (US R² 39.4% … Japan 23.8%); PEG on `ln(growth)` (US 11.3% … Japan 33.2%); PBV incl. ROE (US 45.2%, EM 48.3%); EV/EBITDA on `DFR, g, tax rate` (US 26.7% … Japan 10.3%); EV/Sales on `tax, DFR, g, margin` (US 31.2%); **EV/IC on `DFR, g, ROIC` — the strongest family, R² 50–63%**. Prefer the multiple with the highest regional R² when they conflict.
- Sector fits: telecom `PE = 13.1151 + 121.223·Growth − 13.8531·EmergingMarket`, R² 66.2%; European banks `PBV = 2.27 + 3.63·ROE − 2.68·σ`, R² 79%; US grocery `PS = 0.07 + 10.49·Net margin` (2007) drifting to `0.557 + 8.50·Net margin` (2015, R² 0.291).
- **Young/money-losing companies:** conventional companion variables fail (internet 2000: `PS = 81.36 − 7.54·Net margin`, R² 0.04). Three routes: (1) survival/growth proxies `PS = 30.61 − 2.77·ln(Rev) + 6.42·RevGrowth + 5.11·(Cash/Rev)`, R² 31.8%; (2) **forward multiple with the full six-step haircut** — value in year N, discount at the **risk-adjusted** cost of capital (not the riskfree rate), subtract dilution from equity to be issued, multiply by `(1 − p_failure)`, adjust for debt and cash, subtract the option overhang; (3) let the market pick the metric by correlating value with every candidate operating metric and pricing on the winner.
- Complexity: `PBV = 0.65 + 15.31·ROE − 0.55·Beta + 3.04·g − 0.003·(10-K pages)`.

**Reference tables.** M10.

**Edge cases.** Coefficients drift violently year to year (the market price of growth ranged 0.41 → 2.62 over two decades) — always state the vintage. R² below ~15% is weak evidence; say so rather than acting.

**Test vector.** Telebras: `predicted PE = 13.12 + 121.22(0.075) − 13.85(1) = 8.35`; actual 8.9 → **+6.6% overvalued** despite having one of the sector's two lowest PEs. Cross-market: European industrial `ROIC 14%, DFR 25%, g 4%` → `EV/IC = 3.77 − 0.925 + 0.032 + 0.868 = 3.75`; with IC €2,000m → €7,500m. Tesla forward-value waterfall: `68,271 → 52,050 (riskfree discount) → 27,750 (risk-adjusted) → 12,814 (dilution) → 12,174 (10% failure) → 11,797 (debt/cash) → 8,152 (options)`.

**Concepts.** concepts/relative-valuation/sector-regressions.md, concepts/relative-valuation/market-wide-regressions.md, concepts/relative-valuation/cross-market-multiple-regressions.md, concepts/relative-valuation/pricing-young-companies.md, concepts/asset-based-private/market-multiple-regression.md, concepts/asset-based-private/peg-ratio-regression.md, concepts/dcf-model-choice-loose-ends/complexity-discount.md, concepts/deliverables-worked-examples/relative-valuation-comparables-regression.md, concepts/deliverables-worked-examples/market-wide-multiple-regression.md

---

### M65 `market_and_country_pe_engine`
**Purpose.** Apply the same pricing logic to whole markets.

**Inputs.** `country_panel: (PE, interest_rate, real_gdp_growth, country_risk_score)`; index inputs `(index_PE, normalized_PE, cape, shiller_PE, tbond_rate, tbill_rate)`.

**Outputs.** `predicted_country_pe, over_under, tbond_pe, shiller_to_bond_ratio, predicted_earnings_yield, predicted_market_pe`.

**Computation.**
- **Country PE:** `PE = 16.16 − 7.94·InterestRate + 154.40·RealGDPGrowth − 0.1116·CountryRisk` (rates as decimals, risk score 0–100, R² 73%). Verdict: actual below predicted → relatively cheap.
- **Market vs bonds:** `T.Bond PE = 1/T.Bond rate`; `relative measure = Shiller PE / T.Bond PE` compared with its own long-run average (~1.06 for 1970–2020).
- **Earnings-yield regression:** `E/P = 0.0359 + 0.5534·T.BondRate − 0.1559·(T.Bond − T.Bill)` (1960–2020, R² 44.81%); through-2008 version `0.0256 + 0.7044·Rate − 0.3289·Spread`, R² 50.71%. `Predicted market PE = 1/predicted E/P`.
- Index-level intrinsic value and implied ERP delegate to M25.

**Reference tables.** M10.

**Edge cases.** The risk-score coefficient is scale-specific — a different 0–100 scale invalidates it. A June-2000 equation applied to today's rates is meaningless; refit. Sixteen observations with three predictors is a thin sample.

**Test vector.** Venezuela, June 2000: `16.16 − 7.94(0.15) + 154.40(0.035) − 0.1116(45) = 15.35` vs actual PE 20 → **30% expensive**, despite a mid-pack headline number. Start of 2021: `T.Bond PE = 1/0.0093 = 107.53`; `Shiller/T.Bond = 0.51` vs a 1.06 average; regression `E/P = 0.0359 + 0.5534(0.0093) − 0.1559(0.0085) = 0.0397` → predicted PE ≈ 25 vs actual 27.19.

**Concepts.** concepts/relative-valuation/country-pe-regression.md, concepts/relative-valuation/market-pe-vs-bond-alternative.md, concepts/dark-side-difficult/market-and-macro-crisis-valuation.md

---

### M66 `sum_of_the_parts_engine`
**Purpose.** Value a multi-business firm division by division, both intrinsically and by pricing, then bridge to equity.

**Inputs.** per division `(name, sector, revenues, ebit, d_and_a, capital_invested, allocated_reinvestment, scalar for the chosen multiple)`; `corporate_expenses`; company-wide `tax_rate, riskfree, erp, cost_of_debt, debt_ratio`; `sector regression coefficients` (M64); bridge inputs.

**Outputs.** per division `(unlevered beta, levered beta, cost of equity, cost of capital, ROC, RIR, growth, value)`; `capitalized_corporate_expense_drag, sum_of_parts_value, market_enterprise_value, conglomerate_discount, equity_value, value_per_share`.

**Computation.**
- **Divisional cost of capital:** `β_L,i = β_u,i(1 + (1−t)D/E)` using the **company-wide** D/E unless a division's own financing is known; `ke_i = rf + β_L,i·ERP`; `WACC_i = ke_i(1 − d) + kd(1−t)d`.
- **Divisional fundamentals:** `ROC_i = EBIT_i(1−t)/capital invested_i`; `RIR_i = allocated reinvestment_i/EBIT_i(1−t)`; `g_i = RIR_i × ROC_i`.
- **Intrinsic route:** `FCFF_i,t = EBIT_i,t(1−t)(1 − RIR_i)`; `TV_i = FCFF_i,n+1/(WACC_i − g_stable)` with `RIR_stable = g_stable/ROC_stable`. **Zero-growth rule: a division earning below its cost of capital is valued at zero growth.**
- **Pricing route:** crude `Value_i = scalar_i × median sector multiple_i`; refined `predicted multiple_i = f_sector(division fundamentals)` from M64, e.g. `EV/EBITDA = a + b·TaxRate + c·ROC`, `EV/Revenues = a + b·margin`, `EV/Capital = a + b·ROC`. `EBITDA_i = normalised EBIT_i + D&A_i` when only EBIT is reported.
- **Corporate expense drag:** `= corporate expenses × (1 − t)(1 + g)/(WACC_company − g)`.
- `Sum of parts = Σ Value_i − corporate drag`; then the M49 bridge (`+ cash − debt − financing-arm debt − minority interests − options ÷ shares`).
- `Conglomerate discount = 1 − market EV / sum-of-parts value`.
- Run **both** routes and compare four numbers: intrinsic SOTP, relative SOTP, whole-company DCF, market EV. The spread is the finding.

**Reference tables.** M07, M10.

**Edge cases.** Coarse segment reporting makes the "parts" arbitrary. Corporate G&A allocation drives divisional ROC materially. A division would not carry the parent's leverage standalone — flag when using the company-wide D/E.

**Test vector.** No single numeric vector for the whole engine in the corpus (UTC/GE tables are per-division). Assert instead: `Σ division values − capitalized corporate drag + cash − debt − minority interests − options == equity value`, and that the intrinsic and relative routes are reported side by side with the market EV.

**Concepts.** concepts/asset-based-private/sum-of-the-parts-framework.md, concepts/asset-based-private/sum-of-the-parts-dcf.md, concepts/asset-based-private/sum-of-the-parts-pricing.md, concepts/asset-based-private/asset-based-valuation-overview.md, concepts/asset-based-private/liquidation-valuation.md, concepts/cost-of-debt-capital/divisional-cost-of-capital.md

---

## S13 — Private companies and discounts

### M67 `private_cost_of_capital`
**Purpose.** Build a discount rate for a firm with no market prices, for a buyer who may not be diversified.

**Inputs.** `unlevered_beta (bottom-up), average_r_squared or correlation ρ, mode: "total_beta"|"private_premium", private_premium, riskfree, erp, tax_rate, debt_choice: "industry"|"target", industry_debt_to_capital, target_debt_to_capital, cost_of_debt_mode: "direct"|"synthetic", pretax_cost_of_debt, ebit, interest_or_lease_expense, long_bond_rate`.

**Outputs.** `rho, total_unlevered_beta, levered_total_beta, cost_of_equity, coverage, rating, spread, pretax_cost_of_debt, after_tax_cost_of_debt, weights, wacc`.

**Computation.**
- `ρ = √(average R² of the comparables)`; **`total unlevered beta = unlevered market beta / ρ`**; `levered total beta = total β_u × (1 + (1−t)·D/E)`; `ke = rf + levered total β × ERP`.
- Spreadsheet form from a debt-to-capital ratio: `total levered β = (β_u/ρ)(1 + (1−t)·(D/C)/(1 − D/C))`.
- Alternative (offered, not preferred): `ke = rf + levered **market** beta × ERP + flat private-company premium`.
- `Coverage = operating income / interest expense`, **with lease payments counted as interest when the firm has no conventional debt** → M19 → `kd = rf + spread` → `kd_AT = kd(1−t)`.
- `D/(D+E) = (D/E)/(1 + D/E)`; `WACC = ke × E/(D+E) + kd_AT × D/(D+E)`.
- **Buyer-type switch (this is the whole point):** undiversified individual → total beta; publicly traded / diversified buyer → **market** beta, no total-beta scaling; partially diversified fund → `perceived beta = market beta / ρ_fund`, giving an answer between the two.

**Reference tables.** M07 (comparable betas and R²), M08 (rating spreads).

**Edge cases.** `ρ = 0` → division by zero. `D/C = 1` → division by zero in `D/E`. The comparable set drives everything: the restaurant case moves the beta from 0.86 to 1.18 purely on peer selection. `ρ` must be the correlation coefficient R, often derived as `√R²`.

**Test vector.** `pvtdiscrate.xls`: `β_u = 1.02, ρ = 0.45, D/C = 0.15, t = 0.4, rf = 0.06, ERP = 0.055, kd = 0.07` → `total levered β = (1.02/0.45)(1 + 0.6 × 0.15/0.85) = 2.506666666666667`; `ke = 0.06 + 0.055 × 2.50667 = 0.19786666666666666`; `kd_AT = 0.042`; **`WACC = 0.17448666666666665`**. Synthetic branch: `EBIT 10,000/interest 2,500 = coverage 4.0` → BBB → spread 0.0225 → `kd = 0.0825`.

**Concepts.** concepts/asset-based-private/total-beta.md, concepts/asset-based-private/private-company-cost-of-capital.md, concepts/cost-of-equity/total-beta.md, concepts/cost-of-equity/non-traded-asset-betas.md, concepts/asset-based-private/private-to-public-sale.md

---

### M68 `illiquidity_discount_engine`
**Purpose.** Size the marketability discount by three routes.

**Inputs.** `route: "fixed"|"silber"|"bid_ask"`; `base_discount = 0.25`; `revenues ($m)`; `block_fraction (decimal, 1.0 = whole company)`; `positive_earnings: bool → DERN ∈ {0,1}`; `cash_to_value`; `trading_volume_to_value (0 for a private firm)`; `customer_relationship: bool → DCUST`.

**Outputs.** `discount (fraction)`, `value_after_discount`.

**Computation.**
- **Fixed:** 20–30%, typically 25%. No firm-specific input.
- **Silber-refined:** `S(Rev, Block%, DERN) = 4.33 + 0.036·ln(Rev) − 0.142·ln(Block%) + 0.174·DERN (+ 0.332·DCUST)`; `d(·) = (100 − e^S)/100`; **`Discount = BaseDiscount − [d(10, Block%, 1) − d(Rev, Block%, DERN)]`** — the subject firm's predicted discount versus a $10M-revenue profitable anchor, shifting the 25% base by the gap. **The block term appears identically in both halves and cancels exactly** (§19-Q15) — block size has no effect as the formula is written.
- **Bid-ask spread regression:** `Spread = 0.145 − 0.0022·ln(Revenues) − 0.015·DERN − 0.016·(Cash/Value) − 0.11·(Volume/Value)`; for a private firm `Volume/Value = 0` and the fitted spread **is** the discount.
- Apply as `Final value = equity value × (1 − discount)`.

**Reference tables.** M10 (pre-computed discount-by-revenue table, profitable and unprofitable columns).

**Edge cases.** `Revenues ≤ 0` or `block ≤ 0` break the logs. Unprofitable small firms get discounts **above** the 25% base — intended. **No discount applies when the buyer is a public/diversified acquirer or in an IPO** — the discount is a function of the buyer, not the firm.

**Test vector.** `liqdisc.xls`: `base 0.25, revenues 209, block 1.0, DERN 1` → `S_anchor = 3.932977, d_anchor = 0.489466`; `S_firm = 4.042398, d_firm = 0.430425` → **`discount = 0.190955`**. Bid-ask: `0.145 − 0.0022·ln(209) − 0.015 − 0.016(0.03) − 0 =` **`0.1177668646456774`**.

**Concepts.** concepts/asset-based-private/illiquidity-discount.md, concepts/asset-based-private/silber-restricted-stock-regression.md, concepts/asset-based-private/bid-ask-spread-illiquidity-regression.md

---

### M69 `control_and_minority_discount`
**Purpose.** Price a stake given the gap between optimally-run and status-quo value.

**Inputs.** `optimal_equity_value, status_quo_equity_value, majority_pct, minority_pct`.

**Outputs.** `value_of_control, minority_discount, majority_stake_value, minority_stake_value`.

**Computation.** `Value of control = optimal − status quo`; **`Minority discount = (optimal − status quo)/optimal`**; `Majority stake = majority% × optimal value` (stake > 50%); `Minority stake = minority% × status quo value` (stake < 50%). Equivalently `minority% × optimal × (1 − minority discount)`.

**Edge cases.** `optimal < status quo` → a negative "discount", meaning incumbent management beats the alternative — flag as invalid rather than proceeding. Meaningful only when `status quo ≤ market price ≤ optimal`. A 50/50 stake is not controlling. **A well-run private firm has almost no minority discount** because the two values coincide. **Known sheet defect (§19-Q16):** `minoritydiscount.xls` stores `B8 = B2 + B5×B3` (optimal + minority% × status quo = 20,825), which exceeds the whole firm; the intended formula is `minority% × status quo`.

**Test vector.** `optimal 14,700, status quo 12,500, majority 51%, minority 49%` → `minority discount = 2,200/14,700 = 0.14965986394557823`; `majority stake = 7,497`; `minority stake = 6,125`. Kristin Kandy: `0.51 × $2.0M = $1.02M` vs `0.49 × $1.6M = $784,000` — two percentage points of ownership worth $236,000.

**Concepts.** concepts/asset-based-private/minority-discount.md, concepts/acquisitions-control-enhancement/voting-premium-and-minority-discount.md, concepts/acquisitions-control-enhancement/expected-value-of-control.md

---

### M70 `ipo_and_vc_adjustments`
**Purpose.** The three IPO-specific value adjustments, the underpricing cost, and the stage-varying discount rate.

**Inputs.** `value_of_operating_assets, cash, debt, ipo_proceeds, proceeds_use: "to_owners"|"pay_down_debt"|"retained"`, `option_value, convertible_preferred_shares, rsus, shares_owed_under_acquisitions, common_shares`; `underpricing_pct, fraction_offered, total_value, offer_price, first_day_close`; VC: `market_beta, rho_by_stage: list[float], riskfree, erp, cash_flow_path, transition_year n, g_stable`.

**Outputs.** `value_of_equity, value_of_common_stock, value_per_share, cost_of_underpricing, first_day_return, cost_of_equity_by_stage, cumulated_discount_factors, firm_value`.

**Computation.**
- `Value of equity = operating assets + cash + retained IPO proceeds − debt`; `Value of common stock = equity − options/warrants/special claims`; `Value per share = common stock / share count`, **the count including every claim that converts to common (convertible preferred, RSUs, shares owed under acquisition agreements) but excluding options**, which are handled by subtraction.
- **Proceeds branch:** taken out by owners → add nothing; used to repay debt → change the debt ratio, recompute the WACC, revalue; retained as cash → add dollar for dollar.
- Use the **market** beta and **no illiquidity discount** for an IPO.
- `Cost of underpricing = underpricing% × (fraction offered × total value investors would pay)`; `First-day return = (close − offer)/offer`.
- **VC stage-varying rate:** `perceived beta_stage = market beta / ρ_stage`; `ke_t = rf + perceived beta_t × ERP`; **`Cumulated COE_t = Π_{s=1..t}(1 + ke_s)`** — not `(1+r)^t` with a single rate; `PV(CF_t) = CF_t/Cumulated COE_t`; `TV_n = CF_{n+1}/(ke_post-transition − g)`; `Firm value = Σ PV + TV_n/Cumulated COE_n`.
- Option maturity convention in IPO work: **half the stated life**.

**Edge cases.** Double-counting the option pool (both in the share count and as a subtraction) is the standard error. `ρ_stage = 0` breaks the perceived beta.

**Test vector.** No complete numeric chain in the corpus for the IPO bridge (Twitter is described qualitatively). Structural assertions: (a) `value per share` with proceeds "taken out by owners" must be strictly below the "retained as cash" case by exactly `proceeds/shares`; (b) the VC engine must reproduce a *falling* cost of equity as `ρ_stage` rises from founder to VC to public, and its cumulated factor must differ from a single-rate compounding.

**Concepts.** concepts/asset-based-private/ipo-valuation.md, concepts/asset-based-private/ipo-pricing-and-underpricing.md, concepts/asset-based-private/vc-stage-varying-cost-of-equity.md, concepts/asset-based-private/private-to-public-sale.md, concepts/asset-based-private/private-to-private-valuation.md

---

## S14 — Contingent claims

### M71 `black_scholes_engine`
**Purpose.** The closed-form option price used by every real-option and equity-as-option module.

**Inputs.** `S, K, t (years), r, sigma, y (dividend yield / value leakage), kind: "call"|"put"`.

**Outputs.** `d1, d2, N(d1), N(d2), value, delta`.

**Computation.**
```
Standard call:            C = S·N(d1) − K·e^(−rt)·N(d2)
                          d1 = [ln(S/K) + (r + σ²/2)t]/(σ√t),  d2 = d1 − σ√t
Dividend-adjusted call:   C = S·e^(−yt)·N(d1) − K·e^(−rt)·N(d2)
                          d1 = [ln(S/K) + (r − y + σ²/2)t]/(σ√t)
Put (parity):             P = K·e^(−rt)(1 − N(d2)) − S·e^(−yt)(1 − N(d1))
```
`N(d1)` is the delta; the embedded replicating portfolio is "buy `N(d1)` units, borrow `K·e^(−rt)·N(d2)`".
**Every real option in this corpus uses the dividend-adjusted form** — real options are never dividend-protected, and omitting `y` is the single largest overstatement error. `σ` is the standard deviation of `ln(value)`, not of cash flows. Match `r` to the option's life (an 11-year option takes an 11-year bond rate).

**Reference tables.** M04.

**Edge cases.** Admissibility gate: Black-Scholes assumes a **continuous price process with no jumps** and European exercise. Real assets usually jump and are usually exercised early → prefer M72. `t = 0` or `σ = 0` degenerate to intrinsic value.

**Test vector.** Avonex: `S = 3,422, K = 2,875, t = 17, r = 0.067, σ² = 0.224, y = 1/17 = 0.0589` → `d1 = 1.1362, N(d1) = 0.8720, d2 = −0.8512, N(d2) = 0.2076` → **`C = $907M`**.

**Concepts.** concepts/real-options/black-scholes-model.md, concepts/finance-foundations/black-scholes-and-put-call-parity.md, concepts/real-options/option-payoffs-and-determinants.md

---

### M72 `binomial_and_decision_tree_engine`
**Purpose.** Backward induction where early exercise or jumps matter — and the decision-tree roll-back that is its close relative.

**Inputs.** Binomial: `S0, up/down factors or an explicit price tree, K, r per period, n_periods, kind, american: bool`. Tree: `nodes with (type: chance|decision, probabilities, payoffs, discount rate per node)`.

**Outputs.** `option_value, delta_at_each_node, borrowing_at_each_node, node_values`; tree: `node values, root value, optimal action at each decision node`.

**Computation.**
- Terminal payoffs `max(S − K, 0)` / `max(K − S, 0)`.
- At each node solve `S_u·D − (1+r)·B = C_u` and `S_d·D − (1+r)·B = C_d` → **`D = (C_u − C_d)/(S_u − S_d)`**, `B = (S_d·D − C_d)/(1+r)`, `Value = D·S − B`.
- **American:** at each node take `max(continuation value, immediate exercise value)`.
- **Model choice rule:** shrink the interval — if price changes shrink too, the limit is normal and Black-Scholes applies; if they stay large, the limit is Poisson (jumps) and it does not. Early exercise likely → binomial.
- **Decision tree:** roll back with `Σ probability × branch value` at chance nodes and **`max(available actions)` at decision nodes** — the max is where optionality enters. Two reconciliations with option pricing: node-specific discount rates (Copeland), or discount every branch at the riskfree rate, take the probability-weighted expectation, then adjust that expectation for market risk.

**Edge cases.** Forgetting the max-with-exercise step at each node silently turns an American option European. An untraded underlying means no arbitrage enforces the value — the number is an estimate, not a price.

**Test vector.** Two-period call, `K = 40`, `r = 11%/period`, tree `50 → {70, 35}`, `70 → {100, 50}`, `35 → {50, 25}`: upper node `D = 1, B = 36.04, C = 33.96`; lower node `D = 0.4, B = 9.01, C = 4.99`; root `D = 0.8278, B = 21.61`, **`C = $19.42`**.

**Concepts.** concepts/real-options/replicating-portfolio-and-binomial-model.md, concepts/real-options/decision-trees-vs-option-pricing.md, concepts/finance-foundations/replicating-portfolio-and-binomial-model.md

---

### M73 `real_option_mappers`
**Purpose.** Map each real option onto `(S, K, t, σ, y, r)`, price it, and scale it for the exclusivity it actually has.

**Inputs (by option).**
- *Delay / patent:* `V` (PV of project cash flows now), `I` (investment in PV dollars), `t` (exclusivity/patent life), `σ²`, `r`, `y = 1/n`.
- *Natural resource:* `reserves, price_per_unit, production_cost_per_unit, development_cost_per_unit, development_lag, relinquishment_life, σ² (resource price), y (net production revenue % of developed-reserve value), r`; developed reserves `FCFF, remaining_life, WACC`; `debt, shares`.
- *Expand:* `CF, k, n` (annuity for `S`), `I_exp` (K), `t` (entry window), `σ`, `r`, `exclusivity_factor`.
- *Abandon:* `S` (PV of remaining project flows), `K` (salvage), `t` (exit-right life), `σ²`, `y = 1/project life`, `r`, `static_npv`.
- *Financing flexibility:* `S` (expected annual reinvestment as % of firm value), `K` ((internal funds + normal external access)/value), `σ²` (variance in `ln(Reinvestment/Value)`), `T = 1`, `excess_return`, `wacc`, `wacc_at_optimal`.
- *Firm with patents:* `commercial DCF, patent option values, R&D_0, g, m (value created per R&D dollar), k, N`.

**Outputs.** option value, the exercise rule, and the aggregated firm value.

**Computation.**
- **Delay / patent:** `Payoff = max(V − I, 0)`; value by the dividend-adjusted call (M71); **`y = 1/n`**, `n` = years of exclusivity remaining. **Exercise rule: hold while `C > V − I`; exercise when `C ≤ V − I`.** The optimal exercise date is where the decaying option value crosses the flat `V − K` line — recompute for `t = n, n−1, …, 1`.
- **Natural resource:** `S = Reserves × (price − production cost)/(1 + y)^lag` (**the development-lag discount is mandatory**); `K = Reserves × development cost per unit`; `t` = relinquishment life (or inventory-exhaustion horizon); `σ²` from the resource price (widen for reserve uncertainty). `Firm value = PV(developed reserves as a finite annuity at the WACC) + option value of undeveloped reserves`; `Equity = firm − debt`; `per share = equity/shares`. **Do not value producing reserves as options.**
- **Expand:** `S = CF × [1 − (1+k)^(−n)]/k`; `K = I_exp`; `t` = entry window; `Value of company = DCF of the existing business + option value`.
- **Abandon (the only put):** `Payoff = max(salvage − PV of remaining flows, 0)`; `y = 1/project life`; `NPV with option = static NPV + put value`.
- **Financing flexibility:** annual option value as % of firm value, then `Value of flexibility = option value% × (excess return/WACC)`; `Cost of flexibility = current WACC − WACC at the optimal debt ratio`; maintain flexibility iff value > cost.
- **Firm with patents:** `Firm value = DCF of commercial products + Σ patent option values + PV of excess value from future R&D`, where `R&D_t = R&D_0(1+g)^t`, `Excess value_t = (m − 1)·R&D_t`, summed over the competitive-advantage window `N` and discounted at `k`; after `N`, `m = 1` and the term contributes nothing.
- **Exclusivity scaler (gate, applies to every option above):** `Claimed value = model value × exclusivity factor ∈ [0,1]`. Zero competitive advantage or zero excess return on the second investment ⇒ factor 0.
- **Three admissibility tests before any premium is added:** option test (a specifiable underlying and contingency with a finite horizon), exclusivity test (can rivals take the same contingency?), pricing test (is the underlying traded, is the option traded, is exercise cost knowable?).

**Reference tables.** M04.

**Edge cases. Double counting is the standing hazard:** patents valued as options must not also drive a high growth rate in the DCF of commercial products; an expansion option must not be embedded in the base-case forecast as well. A deep out-of-the-money real option is not worthless — which is exactly why the exclusivity gate matters.

**Test vector.** Gulf Oil (natural resource): `S = 3,038 × (22.38 − 7)/1.05² = $42,380.44M`; `K = 3,038 × 10 = $30,380M`; `t = 12, σ² = 0.03, r = 9%, y = 5%` → `d1 = 1.6548, N(d1) = 0.9510, d2 = 1.0548, N(d2) = 0.8542` → **`C = $13,306M`**; developed reserves `915 × (1 − 1.125^−10)/0.125 = $5,065.83M`; firm `18,372 − debt 9,900 = equity 8,472`; **`per share = 8,472/165.3 = $51.25`** against a $70 bid.
Secondary: Secure Mail expansion `S = 40 × (1 − 1.12^−10)/0.12 = $226M`, `K = 500`, `t = 5`, `σ = 0.5` → **`C = $56M`**. Airbus abandonment: put **$73.23M**; `NPV with option = −20 + 73.23 = $53.23M`. Disney flexibility: `1.6092% × (0.0647/0.1222) = 0.85%` value vs `12.22% − 11.64% = 0.58%` cost → maintain. Biogen firm-with-patents: contractual annuity `50 × (1 − 1.07^−12)/0.07 = $397.13M`; future R&D `R&D_0 = 100, g = 20%, m = 1.25, k = 15%, N = 10` → **`$318.30M`**.

**Concepts.** concepts/real-options/real-options-framework.md, concepts/real-options/option-to-delay.md, concepts/real-options/patent-valuation-as-option.md, concepts/real-options/natural-resource-options.md, concepts/real-options/option-to-expand.md, concepts/real-options/option-to-abandon.md, concepts/real-options/financing-flexibility-option.md, concepts/real-options/valuing-a-firm-with-patents.md, concepts/real-options/opportunities-are-not-options.md, concepts/project-returns/project-options.md, concepts/narrative-numbers/contingent-claim-valuation.md

---

## S15 — Acquisitions and control

### M74 `control_value_engine`
**Purpose.** Value the firm twice — as run and as it could be run — and convert the gap into a control value, an expected value, an implied probability and a share-class premium.

**Inputs.** Two full assumption sets for M42/M43 (`status_quo` and `restructured`), each yielding an equity value and a per-share value; `probability_of_change P`, `implementation_delay k`, `discount_rate r`, `market_price_per_share`, `voting_shares V`, `non_voting_shares NV`, `ownership_pct`.

**Outputs.** `status_quo_value, optimal_value, value_of_control, value_of_control_per_share, expected_value_per_share, adjusted_control_value (delayed), implied_probability P*, max_hostile_bid, max_premium_per_share, value_per_voting_share, value_per_non_voting_share, voting_premium_pct`.

**Computation.**
- Restructuring works through the same four levers: `g = RR × ROC` (raise either), `EBIT = revenues × margin` (raise the margin), `ROC = margin × capital turnover`, and the debt ratio that **minimises WACC** (delegate the whole schedule to M52).
- `Value of control = optimal value − status quo value`.
- **`Expected value of control = P × (optimal − status quo)`**; `Market value identity: price = status quo + P × (optimal − status quo)`.
- **Inverted:** `P* = (market price/share − status quo/share)/(optimal/share − status quo/share)`. Bounds: `P* ≤ 0` → the market prices no chance of change; `P* ≥ 1` → your optimal value is too low or the market sees something you have not modelled.
- **Hostile bid ceiling:** in a control acquisition you can *ensure* the change, so `P = 1` and the maximum price is the **optimal** value; `max premium per share = optimal/share − current price`. Do not pay all of it.
- **Delay:** `Adjusted control value = (optimal − status quo)/(1 + r)^k`.
- **Two share classes (extreme case, non-voting completely unprotected):** `value per non-voting share = status quo value/(V + NV)` — **every share owns the same cash flows**; `value per voting share = that + P × (optimal − status quo)/V`; `voting premium % = (voting − non-voting)/non-voting`.
- **Private stakes:** controlling (>50%) priced off optimal value, minority off status quo (M69).
- Value-creation gate: growth adds value only when `ROIC > WACC`; if `ROIC < WACC`, raising the reinvestment rate raises growth *and destroys value*.

**Reference tables.** via M52.

**Edge cases.** Assigning the status-quo value only to voting shares is wrong. Protective charter provisions and tag-along rights leak control value to the non-voting class and shrink the premium. `P*` above 1 is a signal that an input is wrong, not a very high probability.

**Test vector.** Blockbuster 2005: status quo equity $955M → **$5.13/share**; optimal $2,323M → **$12.47/share**; gain $7.34/share. At a $9.50 price → `P* = 4.37/7.34 = 59.5%`; before Icahn at $8.20 → `P* = 41.8%` — activism moved the odds ~18 points, worth $1.30/share. Embraer voting premium: `status quo 12,500 / (242.5 + 476.7) = R$17.38` per non-voting share; `+ 0.20 × 2,200/242.5 = R$1.81` → `R$19.19` per voting share → **10.4% premium**.

**Concepts.** concepts/acquisitions-control-enhancement/status-quo-valuation.md, concepts/acquisitions-control-enhancement/restructured-value-and-value-of-control.md, concepts/acquisitions-control-enhancement/expected-value-of-control.md, concepts/acquisitions-control-enhancement/implied-probability-of-management-change.md, concepts/acquisitions-control-enhancement/voting-premium-and-minority-discount.md, concepts/acquisitions-control-enhancement/paths-to-value-creation.md, concepts/acquisitions-control-enhancement/growth-quality-and-excess-returns.md, concepts/dark-side-difficult/value-of-control-and-restructuring.md, concepts/deliverables-worked-examples/value-of-control-and-synergy.md

---

### M75 `synergy_engine`
**Purpose.** Value synergy as a difference of two DCFs, with the sum-of-parts identity as a built-in test.

**Inputs.** stand-alone assumption sets for acquirer and target (the **restructured** target when control value is also being claimed); combined-firm status-quo inputs (value-weighted betas and debt ratios, revenue-weighted margins); synergy overlay `(margin_uplift, roc_uplift, reinvestment_rate, growth_period_extension, tax_rate_change, debt_ratio_change)`; NOL inputs `(nol, acquirer_tax_rate, annual_taxable_income, discount_rate)`; delivery inputs `(expected_synergy, actual_synergy, customer_attrition_rate, premium_paid)`.

**Outputs.** `v_acquirer, v_target, v_combined_no_synergy, v_combined_with_synergy, value_of_synergy, tax_synergy_pv, years_to_absorb_nol, realization_rate, adjusted_revenue_synergy, synergy_retained_by_acquirer`, `sum_of_parts_check: bool`.

**Computation.**
1. Value the acquirer stand-alone at its own WACC.
2. Value the target stand-alone at the **target's own** risk and debt capacity (M76 sin 1/2). Use the **restructured** target value here when control value is also claimed, or the two overlap.
3. `V_combined_no_synergy = V_acquirer + V_target`. **Assert equality with the sum of the parts** — merely adding two firms creates nothing.
4. Build combined status-quo inputs: revenues add; margins blend by revenue; betas and debt ratios blend by value.
5. Overlay the synergy assumptions, re-run the DCF.
6. **`Value of synergy = (5) − (3)`.**
7. **Tax/NOL synergy:** `Maximum benefit = NOL × acquirer tax rate` **only if usable at once**; otherwise `annual saving = min(taxable income, remaining NOL) × tax rate`, `years to absorb = NOL/annual taxable income`, and the value is the PV of that stream — materially below the maximum.
8. **Delivery haircuts:** `Realization rate = actual/expected`; `Adjusted revenue synergy = gross × (1 − attrition rate)` with observed integration attrition **2%–5%**; `Synergy retained = value of synergy − premium paid`, which goes to zero as bidders multiply.

**Edge cases.** Do not let the combined firm inherit a lower cost of capital purely from combining — in the AB InBev case the cost of capital is identical in both combined columns; synergy runs through operations, not financing. Diversification lowers the cost of equity only for **private or closely held** firms.

**Test vector.** P&G/Gillette: `V_no_synergy = 221,292 + 59,878 = 281,170` (identity holds); with $250M of annual cost savings and growth 11.58% → 12.50%, `V_with_synergy = 298,355` → **`synergy = $17,185M`**. AB InBev/SABMiller: `211,953 + 50,065 = 262,018` (identity holds); with synergy `276,610` → **`$14,592M`**. NOL: `$2bn NOL, 36% rate, $500M taxable income/yr` → max benefit $720M, but 4 years to absorb at $180M/yr, so the PV is well below $720M.

**Concepts.** concepts/acquisitions-control-enhancement/valuing-synergy.md, concepts/acquisitions-control-enhancement/synergy-taxonomy.md, concepts/acquisitions-control-enhancement/synergy-delivery-odds.md, concepts/acquisitions-control-enhancement/target-discount-rate-discipline.md, concepts/acquisitions-control-enhancement/abinbev-sabmiller-case.md, concepts/project-returns/acquisitions-as-projects.md

---

### M76 `deal_arithmetic`
**Purpose.** The price side of a deal: build-up, goodwill, premium, the acid test, exit multiples and the EPS-accretion trap.

**Inputs.** `pre_deal_book_equity, intangibles_added, pre_deal_market_equity, acquisition_price, write_off_components`; `status_quo_value, restructured_value, synergy_value, motive`; `precedent_multiple, target_metric`; `pe_acquirer, pe_target`; `discount_rate_used, target_cost_of_equity, debt_ratio_used, target_debt_ratio`; `announcement CARs, market caps`.

**Outputs.** `post_deal_adjusted_book_equity, goodwill, acquirer_premium_pct, premium_to_justify, acid_test verdicts, write_off_attribution, transaction_price, implied_exit_growth_and_roc, eps_accretive: bool, wealth_transfer_from_debt_subsidy, recovery_ratio, seven_sins_test_statistics`.

**Computation.**
- **Price build-up:** `Post-deal adjusted book equity = pre-deal book equity + intangibles added`; `Pre-deal market equity = that + market premium over adjusted book`; `Acquisition price = pre-deal market equity + acquirer's premium`; **`Goodwill = acquisition price − post-deal adjusted book equity`**; `Acquirer premium % = (price − pre-deal market equity)/pre-deal market equity`.
- **Write-off attribution:** `Total write-off = premium for non-existent synergy + accounting impropriety + post-deal deterioration`; `Residual value = price − total write-off`.
- **Acid test (four numbers, three inequalities):** undervaluation → `price < status quo value`; control → `price < restructured value`; synergy → `price < restructured value + synergy value`. `Value of control = restructured − status quo`; `Premium to justify = price − pre-announcement market cap`.
- **Transaction multiples:** `Price = precedent multiple × target metric`. **Exit multiple in a terminal value:** `TV_n = exit multiple × metric_n` — convert it back into its implied `g` and `ROC` (M34) and compare with the perpetuity form; the exit multiple embeds a stationarity assumption.
- **EPS accretion:** an all-stock deal is accretive whenever `PE_acquirer > PE_target`. **This is arithmetic, not value.** Report it and label it.
- **Debt-subsidy wealth transfer (sins 1–2):** `Transfer = V(target discounted at the acquirer's WACC) − V(target discounted at the target's WACC)` — exactly the amount handed to the seller for the buyer's financing strength.
- **Market's synergy verdict:** `Acquirer value change = CAR × acquirer market cap`; if `≈ −premium`, the market expects zero synergy. `Recovery ratio = later divestiture proceeds / original price paid`; `< 1` → value destroyed and admitted.
- **Seven-sins test statistics** (each verdict is judgment, each statistic is not): discount rate used vs the target's own cost of equity; debt ratio used vs the target's; premium as a % of market value; ratio of unquantified to quantified synergy dollars; whether the terminal value came from a multiple or a perpetuity; the chronology gap between the price discussion and the completed valuation; the input that had to be flexed to reach the price.
- **Strategy odds scoring:** `target size = target value/acquirer value` bucketed at `<5%, 5–9.99%, 10–19.99%, >20%`; sole bidder vs auction; private/subsidiary vs public target; cash vs stock; cost vs growth synergies.

**Edge cases.** Never justify a premium over market by pointing to the premium over **book**. Purchase-accounting intangibles are a revaluation, not value creation. Goodwill is a residual, never a cash source in an intrinsic valuation.

**Test vector.** HP/Autonomy: `2,067 + 2,533 = 4,600 adjusted book equity`; `+1,300 = 5,900 pre-deal market equity`; `+5,200 = 11,100 price` → **`goodwill = 11,100 − 4,600 = 6,500`**; **`acquirer premium = 5,200/5,900 ≈ 88%`**. Write-off: `4,451 (non-existent synergy) + 749 + 1,700 (impropriety) + 1,900 (deterioration)`; `residual = 2,300`. Acid test: AB InBev/SABMiller lands at a **−$33B** verdict.

**Concepts.** concepts/acquisitions-control-enhancement/acquisition-price-buildup-and-goodwill.md, concepts/acquisitions-control-enhancement/three-reasons-and-acid-test.md, concepts/acquisitions-control-enhancement/transaction-and-exit-multiples.md, concepts/acquisitions-control-enhancement/target-discount-rate-discipline.md, concepts/acquisitions-control-enhancement/control-premium-rules-of-thumb.md, concepts/acquisitions-control-enhancement/seven-sins-of-acquisitions.md, concepts/acquisitions-control-enhancement/acquisition-strategy-design.md, concepts/acquisitions-control-enhancement/acquisition-empirical-record.md, concepts/acquisitions-control-enhancement/deal-bias-and-ego.md, concepts/governance-objective/value-destroying-acquisitions.md

---

## S16 — Payout, governance, narrative, deliverables

### M77 `payout_analyzer`
**Purpose.** The full dividend-policy assessment: what was returned, what could have been, whether management can be trusted with the difference, and a five-year forecast.

**Inputs.** `n_years (1–10)`, `current_debt_ratio`, `use_target_ratio: bool + target_debt_ratio`; per-year arrays (most recent first) `net_income[], depreciation[], capex[], chg_noncash_wc[], net_debt_issued[], dividends[], buybacks[], bv_equity[], stock_return[], tbill_rate[], market_return[]`; `beta`; forecast block `g_revenues, g_ni, g_capex, g_depreciation, g_dividends, wc_pct_revenues, base revenues/NI/capex/depreciation/dividends`.

**Outputs.** per year `fcfe_predebt, fcfe_actual, fcfe_target, cash_returned, payout_ratio, cash_pct_of_fcfe, roe, required_return, roe_minus_coe, jensens_alpha`; aggregates `agg_ni, agg_dividends, agg_buybacks, agg_cash, cash_payout_ratio, agg_fcfe (3 variants), cash_pct_of_each_fcfe, average_roe, average_required_return, average_stock_return, roe_minus_required, actual_minus_required`; forecast `revenues_t, ni_t, chg_wc_t, fcfe_t, expected_dividends_t, cash_available_for_buybacks_t`; `matrix_quadrant`.

**Computation.**
- Per year: `FCFE_predebt = NI − (capex − depreciation) − ΔWC`; `FCFE_actual = + net debt issued`; **`FCFE_target = NI − (capex − depreciation)(1 − DR) − ΔWC(1 − DR)`**; `cash returned = dividends + buybacks`; `payout = dividends/NI`; `cash % of FCFE`.
- `ROE_t = NI_t/BV equity_t`; `Required return_t = Rf_t + β(Rm_t − Rf_t)`; `ROE − required`; **`Jensen's alpha_t = stock return_t − required return_t`**.
- Aggregates over the `n_years` used; note the sheet reports **both** ratio-of-sums and mean-of-ratios for the payout ratio and they differ — keep both.
- `Cumulated cash_t = cumulated cash_{t−1} + FCFE_t − cash returned_t`.
- **Forecast (5 years):** `Rev_t = Rev_0(1+g_rev)^t`; `NI_t = NI_0(1+g_ni)^t`; `CapEx_t`, `Dep_t` likewise; **`ΔWC_t = wc_pct × (Rev_t − Rev_{t−1})`** (the change, not the level); `FCFE_t = NI_t − (CapEx_t − Dep_t)(1−DR) − ΔWC_t(1−DR)`; `Expected dividends_t = Div_0(1+g_div)^t`; **`Cash available for buybacks_t = FCFE_t − expected dividends_t`**.
- **Dividend matrix quadrant:** cash axis `surplus if cash returned < FCFE`; quality axis `good projects if ROE > ke and/or ROC > WACC`, cross-checked with Jensen's alpha.

**Reference tables.** M10 (historical stock and T-bill returns to populate the required-return inputs).

**Edge cases. Known sheet defect (§19-Q17):** `dividends.xls` computes average ROE as `Σ NI over ALL TEN input rows / Σ BV over all ten`, ignoring `n_years` — every other statistic respects `n_years`. Negative NI makes the payout ratio meaningless; negative FCFE makes `cash % of FCFE` negative — the sheet passes both through. Which FCFE variant defines the cash axis can flip the matrix quadrant.

**Test vector.** `dividends.xls` (5 years): `agg cash returned 19,869`; `cash payout ratio = 19,869/23,895 = 0.8315128688010044`; `cash/FCFE_predebt = 1.1484307265475984`; `cash/FCFE_actual = 0.732470692324707`; `cash/FCFE_target = 1.0998896900399782`; `average ROE (ten-row quirk) = 41,261/1,368,002 = 0.0301615056118339`; `average required return = 0.11224093867256421`; `ROE − required = −0.08207943306073032`; `actual − required = +0.06419906132743577`. Forecast year 1: `NI 6,442.8 − 560.7641 − 112.1475 = FCFE 5,769.888383978806`; `dividends 1,390.2`; **`buyback capacity 4,379.688383978806`**.

**Concepts.** concepts/dividend-policy/cash-trust-assessment.md, concepts/dividend-policy/payout-forecasting.md, concepts/dividend-policy/dividend-matrix.md, concepts/dividend-policy/fcfe-potential-dividends.md, concepts/dividend-policy/dividend-decision-sequence.md, concepts/deliverables-worked-examples/dividend-policy-deliverable.md

---

### M78 `payout_benchmark_engine`
**Purpose.** Benchmark payout and yield against peers and against a cross-sectional regression.

**Inputs.** peer panel `(market_cap, dividends, buybacks, net_income, fcfe)`; firm `(beta BETA, expected_growth EGR, debt_ratio DCAP, actual payout, actual yield)`; `coefficient_vintage`.

**Outputs.** `group_yield, group_payout, group_median, firm_relative_position, predicted_payout, predicted_yield, payout_gap, yield_gap`, plus a buyback-inclusive comparison.

**Computation.**
- `Group yield = Σ dividends/Σ market cap` (value-weighted) **or** the median of individual yields (size-neutral). `Group payout = Σ dividends/Σ NI` — this differs, sometimes hugely, from the mean of individual payout ratios when peers have losses.
- `Cash return/FCFE` per peer, compared with the group median; report `NA` when `FCFE ≤ 0`.
- **Market regressions (US, January 2014, all decimals):**
  `PYT = 0.649 − 0.296·BETA − 0.800·EGR + 0.300·DCAP` (R² 19.6%; t-stats 32.16, 15.40, 8.90, 7.33)
  `YLD = 0.0324 − 0.0154·BETA − 0.038·EGR + 0.023·DCAP` (R² 25.8%; t-stats 38.81, 19.41, 13.25, 13.45)
  where `PYT = dividends/NI`, `YLD = dividends/price`, `DCAP = debt/(debt + market equity)`.
- `Payout gap = actual − predicted`; negative → the firm pays less than the fundamentals-based norm.
- **Always add buybacks back before drawing a conclusion** — dividend-only analysis mis-ranks firms systematically.
- Life-cycle benchmark: payout and yield by expected-growth class (lookup).

**Reference tables.** M10.

**Edge cases.** R² of 20–26% means the gap is weak evidence. Coefficient vintage matters (R9). Peer-group definition (sector boundary, geography, size filter, loss-makers in or out) drives the answer.

**Test vector.** Coefficient evaluation is the vector: a firm with `BETA = 1.0, EGR = 0.10, DCAP = 0.20` → `PYT = 0.649 − 0.296 − 0.080 + 0.060 = 0.333` and `YLD = 0.0324 − 0.0154 − 0.0038 + 0.0046 = 0.0178`. Compare with actual; the corpus provides no single firm-level numeric example for this pair.

**Concepts.** concepts/dividend-policy/peer-group-payout-analysis.md, concepts/dividend-policy/market-regression-payout-prediction.md, concepts/dividend-policy/dividend-life-cycle.md, concepts/dividend-policy/dividend-empirical-facts.md

---

### M79 `ex_dividend_and_clientele_engine`
**Purpose.** The tax arithmetic around the ex-dividend day, the capture trade, and the clientele and signalling statistics.

**Inputs.** `price_cum P_b, price_ex P_a, dividend D, tax_ordinary t_o, tax_capital_gains t_cg, shares N`; clientele `(beta, investor_age, investor_income, differential_tax_rate)`; dual-class `(price_cash_dividend_share, price_equivalent_non_cash_share)`; signalling `(returns, market model, event window, market_cap)`; `flotation_cost_fraction f, dividend_maintained, cost_of_equity ke, growth g, mandated_payout m`.

**Outputs.** `drop_ratio k, predicted_ratio, implied_t_o, capture_profit, dual_class_premium, predicted_yield, CAR, expected_announcement_loss, pv_of_permanent_dividend_increase, flotation_cost, external_shortfall`.

**Computation.**
- **Indifference condition:** `P_b − (P_b − P)t_cg = P_a − (P_a − P)t_cg + D(1 − t_o)` ⟹ **`(P_b − P_a)/D = (1 − t_o)/(1 − t_cg)`**.
- Observed `k = (P_b − P_a)/D`; invert for the marginal investor's implied `t_o` given an assumed `t_cg`.
- **Dividend capture (tax-exempt investor):** `profit per share = D(1 − k)`; `total = N·D(1 − k)` before transaction costs.
- **Clientele regression (US evidence):** `Dividend Yield = 0.0422 − 2.145·Beta + 3.131·(Age/100) − 3.726·(Income/1000) − 2.849·(differential tax rate)`.
- **Dual-class premium** for cash-dividend shares `= P_cash/P_equivalent − 1`.
- **Signalling:** `AR_t = R_t − E[R_t]` from a market model; `CAR(t1,t2) = Σ AR_t`; asymmetry `|CAR on decreases|/CAR on increases ≈ 5–6×` (roughly −4.5% vs +1%); `expected announcement loss ≈ market cap × |CAR|`.
- **Cost of preserving a dividend by issuing equity** `≈ dividend maintained × f`; **PV of a permanent dividend increase** `≈ ΔD/(ke − g)` versus a one-time buyback which commits nothing.
- **Mandated minimum payout:** required dividends `= m × NI`; external funding needed `= max(0, m·NI − FCFE)`.
- **Wealth transfer to stockholders from a dividend:** book cash and equity both fall by `D`, so `D/E` and `net debt` rise mechanically; coverage falls if the payout is debt-funded; measure with paired stock and bond CARs.

**Reference tables.** M10 (flotation costs).

**Edge cases.** Microstructure (bid-ask bounce, tick size, market moves on the day) contaminates `k`. The clientele regression is old and low-R² — treat its absolute predictions with care.

**Test vector.** Formula assertion: with `t_o = t_cg`, `k = 1` (the price drops by the full dividend) and the capture profit is zero. With `t_o = 0.40, t_cg = 0.20`, `k = 0.60/0.80 = 0.75` and a tax-exempt investor's capture profit is `0.25 × D` per share. The corpus states the mechanism without a single numeric worked case.

**Concepts.** concepts/dividend-policy/ex-dividend-day-and-dividend-capture.md, concepts/dividend-policy/clientele-effect.md, concepts/dividend-policy/dividend-signaling.md, concepts/dividend-policy/dividend-wealth-transfer.md, concepts/dividend-policy/managing-dividend-changes.md, concepts/dividend-policy/bad-reasons-for-paying-dividends.md, concepts/dividend-policy/three-schools-of-dividend-thought.md

---

### M80 `governance_arithmetic`
**Purpose.** Every countable governance quantity, plus the two decision matrices that turn booleans into an objective and a screen.

**Inputs.** holdings table `[(holder, shares, class)]`, `class_voting_rights: {class: votes_per_share}`, pyramid layers; director list `[(name, role, committee_memberships, tenure, age, shares_held, other_boards, fee)]`; charter provisions list; `is_publicly_traded T, markets_efficient E, lenders_protected B`; `firm_roe, peer_roe, two_year_relative_return, insider_ownership_pct`; governance index provisions; `institutional_shares, insider_shares, shares_outstanding, float`; greenmail `(buyback_price, raider_cost, shares_bought)`; `bond_price_before, bond_price_after`; acquisition `(bid_value, target_market_cap_30d_prior, acquirer_CAR, acquirer_market_cap, divestiture_proceeds, original_price)`.

**Outputs.** `economic_stake, voting_stake, control_wedge, group_control, look_through_interest, top_n_concentration`; `inside_director_count, outside_pct, calpers_tests: (bool, bool, bool), board_size_vs_benchmark, director_stake_to_fee`; `objective: "stock price"|"stockholder wealth"|"firm value"`; `takeover_target: bool`; `governance_index, implied_value_effect`; `institutional_pct_of_shares, institutional_pct_of_float, insider_pct`; `greenmail_transfer, bondholder_loss_pct, acquisition_premium_$ and %, market_synergy_verdict, recovery_ratio`.

**Computation.**
- `Economic stake = shares owned/total shares`; **`Voting stake = (shares owned × votes per share)/total votes`**; `Control wedge = voting − economic`; `Group control = Σ affiliated stakes`; `Look-through interest = product of ownership fractions down each pyramid layer`. Control test: `>50%` outright; largest block with the rest splintered → de facto control.
- **CalPERS board tests:** (1) majority outside directors? (2) chair independent of the company (not the CEO)? (3) compensation and audit committees entirely outsiders? `Inside directors = employees + ex-managers`; `outside % = (total − inside)/total`.
- **Modified objective matrix (a pure lookup on three booleans):** `T=Y,E=Y,B=Y → maximize stock price`; `T=Y,E=N,B=Y → maximize stockholder wealth`; `T=Y,E=N,B=N → maximize firm value`; `T=N,B=Y → stockholder wealth`; `T=N,B=N → firm value`.
- **Hostile-takeover target screen:** poor `ROE` versus peers **and** poor two-year relative stock return **and** low insider ownership.
- **Governance index:** count of the 24 investor-protection provisions; higher index = fewer protections; evidence: a long-strongest/short-weakest portfolio earned **+8.5%** a year, and each index point toward fewer protections associated with **−8.9%** of market value (1999).
- `Greenmail transfer = (buyback price − raider's average cost) × shares bought`.
- `Bondholder loss % = (price before − price after)/price before`.
- `Acquisition premium $ = bid value − target market cap 30 days prior`; `%` likewise; `market's synergy verdict = acquirer CAR × acquirer market cap`; if `≈ −premium`, the market expects zero synergy. `Recovery ratio = divestiture proceeds/original price`; `<1` → value destroyed.
- `Institutional % of float = institutional shares/float`, `float = shares outstanding − closely held`; **it can exceed 100%** when reported holdings overlap or the float definition lags.

**Reference tables.** None (ISS QuickScore is a vendor input, 1 = best, 10 = worst).

**Edge cases.** Every boolean feeding the objective matrix is judgment with **no threshold in the source** — the matrix is deterministic, its inputs are not. A nominally "outside" director may have undisclosed ties; the count is mechanical, the independence call is not.

**Test vector.** Disney 1997 board **fails all three CalPERS tests** — the only S&P 500 company to do so. Objective matrix: `(T=Yes, E=No, B=No) → maximize firm value`.

**Concepts.** concepts/governance-objective/ownership-and-control-structure-analysis.md, concepts/governance-objective/board-independence-assessment.md, concepts/governance-objective/modified-objective-function.md, concepts/governance-objective/self-correction-and-counter-forces.md, concepts/governance-objective/governance-legislation-and-payoff.md, concepts/governance-objective/managerial-entrenchment-and-takeover-defenses.md, concepts/governance-objective/stockholder-bondholder-conflict.md, concepts/governance-objective/value-destroying-acquisitions.md, concepts/governance-objective/classical-objective-function-assumptions.md, concepts/deliverables-worked-examples/governance-analysis-deliverable.md, concepts/deliverables-worked-examples/stockholder-analysis-marginal-investor.md

---

### M81 `narrative_consistency_screens`
**Purpose.** Every screen that can falsify a valuation from its own outputs. Run automatically; report violations before the value.

**Inputs.** model outputs `(g_terminal, riskfree, implied_revenues, total_market_size, operating_margin_path, terminal_depreciation, terminal_capex, reinvestment_rate, roc_path, wacc_path, marginal_roic, growth_period_length)`; external `economy_growth`.

**Outputs.** `screens: dict[name → pass|fail|warn]` with the offending number attached.

**Computation.**
**Impossible (hard fail, never allow):**
- `g_terminal ≤ economy nominal growth`, in practice `g_terminal ≤ riskfree rate` in the same currency.
- `implied revenues / total market size ≤ 100%`.
- `operating margin ≤ 100%` at every point on the path (earnings growth cannot outrun revenue growth long enough to break this).
- `terminal depreciation ≤ terminal capex` (no depreciation without cap ex in perpetuity).
**Implausible (warn, requires extraordinary justification):** growth forever with no reinvestment; high growth and rising margins with no competitive response; high returns in a business with no risk.
**Improbable (warn, internally inconsistent pairings on the growth/risk/reinvestment triangle):** high growth with low risk; high growth with low reinvestment; low risk with high reinvestment.
**Supporting identities used by the screens:** `g = RR × ROC` (so low reinvestment + high growth forces an implausible ROC); `RR_stable = g/ROC_stable`; `marginal ROIC = Δ EBIT(1−t)/Δ invested capital over the forecast`; `terminal excess return = ROC_terminal − WACC_terminal` (default 0).
**Big-market delusion (sector-level):** `imputed sector revenue_i = breakeven revenues_i × (% of company i's revenue from the sector)`; `aggregate = Σ_i`; fail if `aggregate > credible total sector revenue`, or equivalently if `Σ implied market shares > 100%`.
**Bias test:** over a record of valuations, the count of upward revisions should roughly equal the count of downward revisions.
**Completeness test:** count inputs with no story attached and story claims with no driver; both counts should be zero.

**Test vector.** Uber June 2014: `terminal reinvestment rate = g/ROC = 2.5%/25% = 10%` — assert the screen accepts it; substituting `ROC = WACC = 8%` would force `RR = 31.25%` and a materially lower value, which is the screen doing its job. Tesla: `terminal RR = 0.0156/0.15 = 0.104`; `marginal ROIC = 0.516559` — flag as aggressive against the auto-industry ROIC distribution.

**Concepts.** concepts/narrative-numbers/narrative-consistency-checks.md, concepts/narrative-numbers/big-market-delusion.md, concepts/narrative-numbers/possible-plausible-probable.md, concepts/narrative-numbers/narrative-numbers-bridge.md, concepts/narrative-numbers/valuation-misconceptions.md, concepts/dcf-cashflows-growth/value-of-growth.md

---

### M82 `scenario_and_simulation_engine`
**Purpose.** Turn one value into a distribution: sensitivity grids, breakeven solves, scenario grids and Monte Carlo.

**Inputs.** `model: callable` (usually M42), `drivers_to_vary: list[str]`, `ranges: dict[str, list]`, `scenario_definitions: list[dict]`, `distributions: dict[str, spec]`, `correlations: matrix`, `n_trials`, `random_seed`, `market_price`.

**Outputs.** `grid: 2-D table of value per share`, `lo/base/hi`, `spread = max/min`, `breakeven_scenario`, `simulated_values`, `percentiles`, `p_value_le_zero`, `percentile_of_market_price`, `plausibility_filter_result`.

**Computation.**
- **Two-way sensitivity grid:** re-run the model over a grid of two drivers (usually compounded revenue growth × target operating margin, or growth-phase growth × growth-period length). `DCF Lo/Base/Hi` = min/base/max cell inside the *plausible* range; apply the plausibility filter first (rule out sustained growth above the economy's growth rate, or a ten-year high-growth phase in a competitive industry).
- **Scenario grid:** each cell is the model evaluated at the driver set implied by that combination of story levels; report `spread = max/min` — a 100× spread says the value is a statement about the story, not the arithmetic.
- **Breakeven solve:** find the input combination at which model value equals the market price (M05), then judge whether it is probable.
- **Monte Carlo:** draw each uncertain input from its distribution **jointly, respecting the correlation structure** (revenue and margin positively correlated; payout and earnings shortfalls negatively), recompute, repeat `n_trials`; report the 10th/50th/90th percentiles, the fraction of trials with value ≤ 0, and **the percentile at which the market price sits** (a price at the 85th–90th percentile means overvalued in most but not all scenarios). The median simulated value is **not** the base-case value — lognormal growth inputs pull mean and median apart.
- Deterministic given a fixed seed.

**Edge cases.** Drawing correlated inputs independently is the standard error and understates the tail. Simulating an input that the value is insensitive to wastes the run — check the sensitivity grid first.

**Test vector.** Tesla `Diagnostics`: `value/price = 571.29/1,200 = 0.476074` → verdict rule `IF(ratio > 2, "high"; ratio < 0.5, "low")` → **"Value seems low"**. Uber: `expected value = 6,595 × (1 − 0.10) = $5,895M`. Grid assertion: with the model fixed, every cell must be reproducible from its own driver set and the base cell must equal the headline value.

**Concepts.** concepts/narrative-numbers/narrative-scenario-grids.md, concepts/narrative-numbers/monte-carlo-valuation-simulation.md, concepts/dark-side-difficult/scenario-analysis-and-simulation.md, concepts/deliverables-worked-examples/dcf-sensitivity-analysis.md, concepts/project-returns/uncertainty-payback-sensitivity-simulation.md, concepts/narrative-numbers/uber-narrative-valuation.md

---

### M83 `value_vs_price_engine`
**Purpose.** Convert a value estimate and a market price into a gap, an expected return and a decision.

**Inputs.** `value_per_share, price_per_share, cost_of_equity, expected_dividend_next_year, margin_of_safety, holding_period`; revision log `[(date, direction)]`.

**Outputs.** `gap_pct, price_as_pct_of_value, expected_price_in_one_year, expected_annual_return, buy_threshold_price, unbiasedness_ratio, verdict`.

**Computation.**
- `% difference = (price − value)/value` (positive = overvalued); `price as % of value = price/value`.
- **`E[P_1] = value today × (1 + cost of equity) − expected dividend`**; `E[return] = (E[P_1] + D_1 − price paid)/price paid`.
- `Margin of safety: buy only when price ≤ value × (1 − margin)`; size the margin to the uncertainty in the gap.
- Implied breakeven growth: solve `model value(g) = price` (M05); closed form for the Gordon case: **`g = (ke·P − DPS_0)/(P + DPS_0)`**.
- Target price if the market corrects: `Expected P_1 = value today × (1 + g)`.
- **Unbiasedness test:** `count(upward revisions) ≈ count(downward revisions)` over a long record.

**Edge cases.** A gap is not an opportunity without a closing mechanism — the catalyst is judgment, the arithmetic is not. Relative-valuation verdicts are relative: "cheap versus this peer group" can coexist with "expensive in absolute terms".

**Test vector.** Tesla: `price/value = 1,200/571.29 = 2.1005` → 110% overvalued on those inputs. Gordon breakeven: with `ke = 0.12225, DPS_0 = 2.7279, P = 46.45` the closed form returns `g = 0.06`, reproducing the base case.

**Concepts.** concepts/dark-side-difficult/value-versus-price.md, concepts/narrative-numbers/value-vs-price-gap.md, concepts/dcf-model-choice-loose-ends/model-choice-case-studies.md

---

### M84 `model_selector_and_deliverable_assembler`
**Purpose.** Route a company to the right engine, apply the eligibility screens, and assemble the two standard deliverables.

**Inputs.** `earnings_positive: bool, normalcy: "normal"|"abnormal"|"cyclical"|"troubled"|"startup", growth: "stable"|"moderate"|"high", growth_source: "general"|"specific"|"either", dividends_equal_fcfe: bool, leverage_stable: bool, other: "turnaround"|"bankruptcy"|"many_lines"|"single_line"|None, inflation_rate, can_estimate_capex: bool, debt_ratio_changing: bool, market_debt_to_capital, expected_revenue_growth, sustainable_advantage: bool, inflation_expectation, sector, country`; plus every module's headline output.

**Outputs.** `model_type, earnings_basis, cash_flow_choice, growth_period, growth_pattern, real_or_nominal, option_pricing_trigger: bool, eligibility: dict[str,bool], scorecard: table, triangulation_table, recommendation`.

**Computation — decision rules (each a mechanical test on judgment-supplied booleans).**
- **Model type:** DCF, unless earnings are negative **because of too much debt AND bankruptcy is likely** → equity-as-option (M51). Even then, do the DCF first.
- **Earnings basis:** positive → current earnings. Negative and cyclical/one-time/leverage-driven → normalised earnings (M14). Negative because start-up → revenue-driven forecasting (M33).
- **Cash flow:** cannot estimate capex/WC → dividends. Can estimate, leverage stable → FCFE. Leverage expected to change → FCFF.
- **Dividends-vs-FCFE screen:** `Dividend coverage = Σ_5yr (dividends + buybacks)/Σ_5yr FCFE`; **below 80% or above 110% → use FCFE, not dividends**; exceptions: banks (FCFE not estimable → dividends) and private firms/IPOs.
- **Growth period:** firm growth > economy growth **and** a sustainable advantage → 10+ years; advantage not sustainable → 5–10; growth ≤ economy → under 5 or none.
- **Growth pattern:** `g ≤ g_econ` → stable; moderately above → 2-stage; far above (the `g_econ + 10%` threshold) with shifting leverage → 3-stage or n-stage.
- **Real vs nominal:** expected inflation ≥ 10% → switch to real cash flows and a real discount rate.
- **Option-pricing trigger:** loss-making **and** market-value debt-to-capital **> 50%** → run M51 alongside the DCF.
- **Full model-choice rule table** (from `readme1s`): +ve/normal/stable/=FCFE/stable leverage → Gordon growth; +ve/normal/stable/≠FCFE → FCFE stable; +ve/normal/stable/unstable leverage → FCFF stable; +ve/normal/moderate/general/=FCFE → H model; …/specific/=FCFE → 2-stage DDM; …/specific/≠FCFE → 2-stage FCFE; …/either/unstable → 2-stage FCFF; +ve/normal/high/either/=FCFE → 3-stage DDM; …/≠FCFE → 3-stage FCFE; …/unstable → 3-stage FCFF; +ve/abnormal/stable → normalized EPS; +ve/abnormal/unstable → normalized FCFF; −ve/cyclical/stable → normalized EPS; −ve/cyclical/unstable → normalized FCFF; −ve/troubled/turnaround → FCFF; −ve/troubled/bankruptcy → option model; −ve/start-up/many lines → FCFF; −ve/start-up/single line → option model.
- **Company-selection screens (all testable from data):** public listing; ≥1 year of trading history; ≥1 annual statement; **exclude** banks, insurance, investment banks, REITs and captive-finance arms; most-recent net income sign; **expected revenue growth > 25%** for the high-growth requirement; country of incorporation; service-sector classification.
- **Corporate-finance scorecard (16 rows, each an output of another module):** Power (M80) · Approach (M26) · Beta (M26) · Jensen's alpha (M26) · R² (M26) · ROE − COE (M16) · ROC − WACC (M16) · EVA (M16) · Current debt ratio (M21) · Optimal debt ratio (M52) · Change in WACC (M55) · Change in value (M55) · Dividends (M37) · FCFE (M36) · Value/share (M49) · Price/share (market).
- **Triangulation:** assemble DCF (M42/M43) · DCF Lo/Base/Hi (M82) · sector regression price (M64) · market-wide regression price (M64) · equity-as-option value (M51, only if triggered) · value of control and synergy (M74/M75). **Weighting rule: when comparables selection is ambiguous, weight the DCF above the relative-valuation regressions.** Decision: preferred estimate above price → BUY; below → SELL. Discard economically implausible predictions.
- **Dependency order for the corporate-finance deliverable:** governance → stockholder analysis → risk/return → cost of capital → return spreads → qualitative debt trade-off → optimal debt ratio → recapitalisation and stress test → debt design → dividend policy → dividend framework → valuation → scorecard. Each part consumes the last; Part III feeds Parts IV, VI, VII and X; Part VI's optimal ratio becomes Part X's growth-phase discount rate.

**Test vector.** `model.xls`: positive earnings, 15% growth vs a 5% nominal economy (3% inflation + 2% real), sustainable advantage, 4% debt ratio expected to change, capex estimable → **`DCF · current earnings · FCFF (value firm) · 10+ years · three-stage`**; and `FCFE = 200 − 50×0.96 − 25×0.96 = 128` against dividends of 100, flagging that the firm pays out less than it can.

**Concepts.** concepts/dcf-model-choice-loose-ends/dcf-model-choice-framework.md, concepts/dcf-model-choice-loose-ends/equity-versus-firm-valuation.md, concepts/dcf-model-choice-loose-ends/dividends-versus-fcfe.md, concepts/dcf-model-choice-loose-ends/discount-rate-cash-flow-matching.md, concepts/dcf-model-choice-loose-ends/growth-pattern-and-stage-count.md, concepts/deliverables-worked-examples/dcf-model-selection.md, concepts/deliverables-worked-examples/project-company-selection.md, concepts/deliverables-worked-examples/corporate-finance-project-blueprint.md, concepts/deliverables-worked-examples/equity-valuation-project-blueprint.md, concepts/deliverables-worked-examples/project-executive-summary-scorecard.md, concepts/deliverables-worked-examples/valuation-triangulation-and-recommendation.md, concepts/dark-side-difficult/difficult-company-taxonomy.md

---

## 17. Orchestration recipes

Named pipelines. Each is an ordered module list; a system exposes these as entry points.

| Recipe | Modules, in order |
|---|---|
| **P1 Standard company valuation** | M11 → M12/M13 → M22 (if synthetic) → M15/M16 → M23 → M24 (or M25) → M26 → M27 → M18→M19→M20→M21 → M28 → M29/M30 → M32 → M31 → M33 → M42 → M34 → M46 → M47 → M48 → M49 → M45 → M81 → M82 → M83 |
| **P2 Fundamentals-driven (Ginzu-full) valuation** | M11 → M12/M13 → M14 (if normalising) → M22 → M29 → M43 → M34 → M46 → M47 → M49 → M45 → M81 |
| **P3 Young / money-losing firm** | M11 → M12 → M33 → M32 (NOL) → M31 (sales-to-capital) → M42 with `prob_failure` → M50 (if a bond trades) → M48 → M46 → M49 → M82 → M81 |
| **P4 Financial-service firm** | M15 → M36 (bank form) or M44 (equity excess return) → M27 → M38/M39 (DDM) → M49 → M45 |
| **P5 Declining / distressed firm** | M14 → M33 (negative growth, margin recovery) → M31 (negative reinvestment) → M42 → M50 → M48 → M51 (if debt/capital > 50%) → M49 |
| **P6 Cyclical / commodity firm** | M03 (regress revenues on the commodity price) → M14 (normalise margins and ROC) → M42 → M82 (simulate the price) → M49 |
| **P7 Emerging-market firm** | M06 → M23 (strip sovereign spread) → M24 (operation-weighted ERP) → M27 (lambda attachment) → M02 (currency) → M47 (cross-holdings) → M48 (truncation/political risk) → P1 |
| **P8 Optimal capital structure** | M13 → M22 → M26 (unlever) → M32 → M52 → M53 (optional) → M54 (cross-check) → M56 → M55 → M57 |
| **P9 Project analysis** | M28 (divisional hurdle rate) → M58 → M59 → M60 (if project-financed) → M73 (embedded options) → M82 (sensitivity/simulation) |
| **P10 Relative valuation** | M61 → M63 → M62 → M64 → M65 (market/country level) → M83 |
| **P11 Private company** | M17 → M67 → M42 or M38 → M49 → M68 → M69 → (M70 for an IPO or a sale to a public buyer) |
| **P12 Acquisition** | P1 on the acquirer → P1 on the target (**at the target's own risk and debt capacity**) → M52 on the target → M74 → M75 → M76 → M45 (T5 sum-of-parts identity) |
| **P13 Governance / activist** | M80 → P1 status quo → M52 + M74 restructured → M74 implied probability → M69/M74 stake and share-class pricing |
| **P14 Payout policy** | M36 → M37 → M77 → M78 → M79 → M55 (buyback alternative) |
| **P15 Corporate-finance deliverable** | M80 → (stockholder analysis, M80) → M26 → M28 → M16 → (qualitative trade-off) → M52 → M55/M56 → M57 → M77 → M78 → M39/M42 → M84 scorecard |
| **P16 Equity-valuation deliverable** | M84 model select → M42 → M82 (Lo/Base/Hi) → M64 sector → M64 market-wide → M51 (if triggered) → M74/M75 → M84 triangulation |

---

## 18. Circularity register

Every deliberate circular reference in the corpus, with its resolver. Nothing else in the inventory is circular.

| ID | Chain | Seed | Resolver | Modules |
|---|---|---|---|---|
| **C1** | cost of debt → lease PV → adjusted EBIT & interest → coverage → rating → cost of debt | `riskfree + a small spread`, or the entered kd | M22 fixed point; detect 2-cycles between adjacent rating brackets | M13, M18, M19, M20, M22 |
| **C2** | debt ratio → $debt → interest → coverage → rating → cost of debt → interest (per column of the optimal-structure schedule) | previous column's kd | Fixed point **per debt-ratio column**; same 2-cycle hazard | M52, M53, M54 |
| **C3** | option value → per-share value → option value (when options are valued off the *estimated* value rather than the market price); and, inside the option, `S_adj` depends on the option value being solved for | plain Black-Scholes on the market price; per-share value ignoring options | Joint fixed point (inner `S_adj ↔ C`, outer `value/share ↔ option value`); converges in <20 iterations | M46, M42, M43 |
| **C4** | market debt ratio → option value in equity → equity value → market debt ratio (Ginzu-full computed debt ratio) | current market cap without option value | Same loop as C3, extended | M43, M21 |
| **C5** | equity value → levered beta → cost of equity → WACC → operating-asset value → equity value (gross-vs-net-debt comparison) | book/naive equity value | Simple fixed point; the net-debt kd adjustment is closed-form, the gross one is inside the loop | M45-T4 |
| **C6** | stable reinvestment rate computed from terminal identities `(EBIT(1−t)_T − FCFF_T)/EBIT(1−t)_T` rather than from `g/ROC` | `g/ROC` | Solve simultaneously, or prefer the `g/ROC` branch | M34, M43 |
| **C7** | rating → EBITDA haircut → EBIT → coverage → rating (indirect bankruptcy costs) | no-haircut EBITDA | Nested inside C2 | M53 |
| **C8** | private-firm lease debt → coverage → rating → cost of debt → lease debt | riskfree + spread | Same as C1 | M17, M67 |

**Policy.** `tol = 1e-9`, `max_iter = 200`, damping available, and a hard error on non-convergence. Excel's ~100 iterations settle arbitrarily; a port must be deterministic and record which convention it used.

---

## 19. Source-defect register

Behaviours in the source spreadsheets that are wrong but that a faithful port may need to reproduce. Every one is gated by a flag (R11).

| ID | Defect | Where | Faithful behaviour | Corrected behaviour |
|---|---|---|---|---|
| **Q1** | Margin ramp anchors years 2–5 on the **year-1** margin and years 6–10 on the **base-year** margin, producing a kink at year 6 whenever `convergence_year > 5` | M33, M42 | reproduce the kink (SK Innovation yr5 0.0525 → yr6 0.04240) | single anchor throughout |
| **Q2** | Firm-type-3 (financial service) rating table is **empty** in the Ginzu / Corona / Tesla workbooks | M08, M19 | `#N/A` | supply the financial-service table from `ratings.xls` / `fcffginzulambda`, or raise |
| **Q3** | Country-spread `VLOOKUP` range stops short of the full table, returning a wrong spread for late-alphabet countries (e.g. "United States" → 0.0133509 instead of 0) | M06 | reproduce the wrong spread | exact match on the full table |
| **Q4** | Two comparison cells look up the **US** industry name in the **Global** industry table | M07 | reproduce | look up the global name |
| **Q5** | In the direct rating→spread list, `C2/C` and `Caa/CCC` spreads are swapped relative to the coverage tables | M08 | reproduce | reconcile to the coverage table |
| **Q6** | `returncalculator.xls` subtracts `cash × (1 − pct_kept)` **and** adds back `pct_kept × cash`, leaving 2× the kept fraction in adjusted capital; the R&D tax effect hardcodes a 0.38 rate | M16, M12 | reproduce both | subtract full cash then add back once; use the supplied marginal rate |
| **Q7** | Lease tail-year count uses `ROUND` in most workbooks but `INT` truncation in `apv.xls` and `normearn.xls` | M13 | expose `tail_rule` | pick one and document |
| **Q8** | Direct-input beta branch is ambiguous — never exercised in the saved files | M26 | treat the supplied regression beta as the **levered** beta and skip relevering (family convention) | unlever at the regression-period D/E, relever at the target |
| **Q9** | Bottom-up macro sensitivity tables use different sign conventions at 4-digit vs 2-digit SIC | M57, M10 | ship both verbatim | do not derive one from the other |
| **Q10** | A growth-estimator toggle set to "No" contributes **0** while its weight is still applied, materially lowering the blended growth rate | M30 | reproduce | renormalise the weights over the active estimators |
| **Q11** | Terminal after-tax EBIT built as `MAX(EBIT(1−t) over the path)` grossed up at the marginal rate and re-taxed at the stable rate | M34, M43 | reproduce | grow the final-year value at `g` |
| **Q12** | Terminal ΔWC grows revenue `N` years at the **unfaded initial** growth rate rather than the faded path | M34, M43 | reproduce | use the actual revenue path |
| **Q13** | `buybacks.xls` applies the cost of **new** debt to **all** post-buyback debt | M55 | reproduce | blend old and new debt costs |
| **Q14** | `buybacks.xls` EPS sheet subtracts the **full, un-prorated, pre-tax** interest income on cash even though only part of the cash is used | M55 | reproduce | prorate and tax-effect |
| **Q15** | Silber refined-discount formula contains the block-size term identically in the anchor and the subject, so **block size cancels and has no effect** | M68 | reproduce | fix the anchor's block at a constant |
| **Q16** | `minoritydiscount.xls` stores `optimal + minority% × status quo` for the minority stake value (exceeds the whole firm) | M69 | reproduce the literal cell | `minority% × status quo value` |
| **Q17** | `dividends.xls` average ROE sums net income and book equity over **all ten** input rows, ignoring `n_years` | M77 | reproduce | restrict to `n_years` |
| **Q18** | `fcfeginzu` computes `FCFE = NI × ERR` (not `NI × (1 − ERR)`) for years 11–15 | M39/M41 (FCFE variant) | reproduce (the published 48.2874/share depends on it) | `NI × (1 − ERR)` throughout |
| **Q19** | `fcfeginzu` ROE numerator includes the R&D adjustment while the reinvestment-rate denominator and the projection base do not | M36 | reproduce | one consistent earnings base |
| **Q20** | Corona `Summary Sheet` year-1 reinvestment is **not** floored at zero, so it disagrees with the authoritative `Valuation output` sheet | M42 | the `Valuation output` sheet is authoritative | floor year 1 |
| **Q21** | `growthbreakdown.xls` labels a cell "pre-tax operating margin" but computes it after tax; its "EV/…" actual-total multiples use **market equity**, not enterprise value | M62-adjacent | reproduce | correct the labels and the numerator |
| **Q22** | Excel string comparisons are case-insensitive (`"Yes"`, `"YES"`, `"yes"` all trigger) | all flag branches | accept any case | normalise on input |

---

## 20. Cross-cutting validation rules

Run these after every valuation. A failure blocks publication of the number, not the run.

**Consistency (hard fails)**
1. **V1** Currency and inflation basis identical across cash flows, discount rate, growth rate and riskfree rate (R2).
2. **V2** Claimholder match: the numerator's claimants equal the discount rate's claimants (R3).
3. **V3** `g_terminal ≤ riskfree rate` in the valuation currency (R6).
4. **V4** `r_stable > g_stable` in every perpetuity (R7).
5. **V5** Every adjustment applied exactly once — leases, R&D, cash, options, pensions, cross-holdings (R5). Check by asserting each appears in exactly the expected set of lines.
6. **V6** Gross-vs-net-debt convention is uniform: if the beta was levered with net debt, the weights use net debt and cash is **not** added back.
7. **V7** Growth, reinvestment and return obey `g = RR × ROC` (firm) and `g = (1 − payout) × ROE` (equity) in every phase, including the terminal one.
8. **V8** Tax rate used in `EBIT(1−t)` equals the one in `kd(1−t)`.
9. **V9** The `D/E` used to relever the beta equals the `D/E` implied by the WACC weights.
10. **V10** Reference-table vintages are mutually consistent (R9).
11. **V11** Invested-capital denominators are beginning-of-period (R4).
12. **V12** Weights sum to 1 (capital structure weights, geographic ERP weights, growth-estimator weights, business-value weights).

**Model-equivalence assertions (M45)**
13. **V13** FCFF and FCFE routes agree under constant market-value leverage (T1).
14. **V14** DDM and FCFE agree iff retained cash earns the cost of equity (T2).
15. **V15** EVA and DCF agree once the terminal-capital adjustment is included (T3).
16. **V16** Combined-firm value with no synergy equals the sum of stand-alone values (T5).
17. **V17** Value is invariant to the currency it is computed in (T7).

**Plausibility screens (warn, from M81)**
18. **V18** Implied revenue ≤ total market size; implied market shares sum to ≤ 100% across the sector.
19. **V19** Operating margin ≤ 100% at every point; terminal depreciation ≤ terminal capex.
20. **V20** Implied perpetual ROC within a stated band of the terminal WACC; terminal excess return defaults to zero.
21. **V21** Marginal ROIC over the forecast is plausible against the sector distribution.
22. **V22** Stable beta in `[0.8, 1.2]`; stable cost of debt in `[rf, rf + 3%]`; stable ROC in `[WACC, WACC + 5%]`.
23. **V23** Share of value in the terminal value reported; a very high share is a warning about the growth-period length, not an error.
24. **V24** Diagnostics verdict: `value/price > 2` → "value seems high"; `< 0.5` → "value seems low"; negative value → "value is negative".

**Data integrity**
25. **V25** No name-keyed lookup falls back to an approximate match (R8); a missing key raises.
26. **V26** `NA` cells in reference tables parse as null, never as zero.
27. **V27** Every circular chain converged (§18); non-convergence raises.
28. **V28** Every defect flag (§19) is recorded in the run's provenance so the number can be reproduced.

---

## 21. Reference-data registry

Ship these as versioned data files, keyed by exact strings, never embedded in code.

| Table | Key | Vintages present in the corpus | Consumed by |
|---|---|---|---|
| Country ERP / default spread / tax rate | country name | Jan-2022 (mature ERP 0.0424), Jan-2021 (0.0472 and 0.052), divginzu (0.0569), riskchecker (0.058) | M06, M20, M23, M24, M27 |
| Regional ERP aggregates | region name | with each country vintage | M06, M24 |
| Rating → sovereign default spread | Moody's rating | several | M06, M23 |
| Past riskfree by currency | currency | one | M26 (Jensen's alpha) |
| Coverage → rating → spread, firm types 1/2/3 | coverage bracket | 2020 Ginzu, Jan-2021 (two variants), wacccalc, normearn/legacy, apv, lambda | M08, M19, M52, M54, M67 |
| Rating → spread (direct) | rating string | with each coverage vintage | M08, M20 |
| Rating → EBITDA drop (Low/Medium/High) | rating | one | M08, M53 |
| Rating → bankruptcy probability | rating | apv vintage | M08, M54 |
| Rating → cumulative default probability (yrs 1–10) | rating | one | M08, M48 |
| US and Global industry averages (26 columns) | industry name | Jan-2022, Jan-2021, and older column sets | M07, M14, M26, M31, M64, M66 |
| R&D amortisable life | industry name | one (~98 rows) + six-category rule of thumb | M09, M12 |
| CapEx/Depreciation ratios by sector | sector name | one (90 sectors, late-1990s) | M10, M31 |
| Flotation costs by issue size and security | size band | one | M10, M79 |
| Historical US stock / T-Bill / T-Bond returns | year (1928–2020) | one | M10, M24, M77 |
| Illiquidity discount by revenue and profitability | revenue band | one | M10, M68 |
| Sector macro sensitivities (duration, cyclicality, inflation, currency) | SIC (2-digit and 4-digit) | one each, **different sign conventions** | M10, M57 |
| Posted regression coefficient sets (PE, PEG, PBV, EV/EBITDA, EV/Sales, EV/IC, country PE, E/P, payout, yield, complexity, young-company) | (multiple, region, vintage) | Jan-2021 primary, Jan-2020 and older for drift | M10, M64, M65, M78 |
| Multiple distribution percentiles | (multiple, market, vintage) | Jan-2021 primary | M10, M63 |
| Sector survival / failure rates by life-cycle stage | sector, stage | one | M10, M48 |
| Standard normal CDF | `d` (−3.00 to +3.00, step 0.05) | one | M04, M71 |
| Dropdown / enum vocabularies | list name | one | all flag branches |

**Enum vocabularies (bind these exactly).** Yes/No · `B`/`V` (distress-proceeds base) · ERP approach: `Will input`, `Country of incorporation`, `Operating countries`, `Operating regions` · Cost of debt: `Direct input`, `Synthetic rating`, `Actual rating` · Beta: `Direct input`, `Single Business(US)`, `Single Business(Global)`, `Multibusiness(US)`, `Multibusiness(Global)` · Synthetic-rating firm type: `1`, `2` (`3` implied for financial service) · Ratings: `Aaa/AAA, Aa2/AA, A1/A+, A2/A, A3/A−, Baa2/BBB, Ba1/BB+, Ba2/BB, B1/B+, B2/B, B3/B−, C2/C, Ca2/CC, Caa/CCC, D2/D` · Depreciation method: `1 = straight line`, `2 = double declining balance` · Normalisation approach: `1 = average EBIT`, `2 = average ROC × capital`, `3 = sector margin × revenues` · Capex estimation: `1 = grow with revenue`, `2 = % of revenue`, `3 = sales-to-capital`.

# The FCFF forecast engine (reference implementation)

**Core idea:** This is the full machinery that turns a base year plus a handful of value-driver assumptions into a value per share. It is the canonical 10-year FCFF model: a revenue path, a margin path converging on a target, reinvestment driven by a sales-to-capital ratio, an NOL-aware tax path that ramps from the effective to the marginal rate, a cost of capital that fades toward a mature level, a terminal value with reinvestment tied to `g/ROC`, an optional probability of failure, and an equity bridge to a per-share number. Everything in this area's other notes plugs into one slot of this engine. Learning the engine is how you see which assumptions are load-bearing.

**Formulas:**

*Base year (after cleansing):*
- `Adjusted EBIT = Reported EBIT + lease adjustment (if leases capitalized) + R&D adjustment (if R&D capitalized)`
- `Invested capital = BV equity + BV debt − cash + lease debt (if any) + research asset (if any)`
- `Base margin = Adjusted EBIT / Revenues`

*Forecast years t = 1..10:*
- Growth: `g_1` given; `g_2..g_5` = a single CAGR; `g_6..g_10` fade linearly to terminal `g`: `g_(5+k) = g_5 − k × (g_5 − g_terminal)/5`.
- Terminal growth: `g_terminal =` explicit override, else the post-year-10 riskfree rate, else the riskfree rate. **It cannot exceed the riskfree rate / nominal economy growth.**
- Revenues: `Rev_t = Rev_(t−1) × (1 + g_t)`; terminal `Rev = Rev_10 × (1 + g_terminal)`.
- Margin: `Margin_1` given; years 2..10 interpolate linearly to the target margin by the convergence year `Y`: `Margin_t = Target − (Target − Anchor)/Y × (Y − t)`, and `= Target` once `t > Y`.
- `EBIT_t = Rev_t × Margin_t`.
- Tax: `t_1..t_5 =` effective rate; `t_6..t_10` ramp in five equal steps to the terminal rate; terminal rate = marginal (or effective if explicitly overridden).
- NOL: `NOL_t = NOL_(t−1) + |EBIT_t|` if `EBIT_t < 0`, else `max(0, NOL_(t−1) − EBIT_t)`.
- `EBIT(1−t)_t` = `EBIT_t` if `EBIT_t <= 0`; = `EBIT_t` if `0 < EBIT_t <= NOL_(t−1)`; = `EBIT_t − (EBIT_t − NOL_(t−1)) × t_t` otherwise. Terminal: `EBIT × (1 − t_terminal)` with no shield.
- Reinvestment: `Reinv_t = (Rev_t − Rev_(t−1)) / SalesToCapital_t`, with `SalesToCapital` set by phase (year 1, years 2–5, years 6–10). Year 1 floors at zero when revenue falls; later years may be negative.
- `FCFF_t = EBIT(1−t)_t − Reinv_t`.
- `Invested capital_t = Invested capital_(t−1) + Reinv_t`; `ROIC_t = EBIT(1−t)_t / Invested capital_t`.
- Cost of capital: constant at the initial WACC for years 1–5, then fades linearly over years 6–10 to the terminal WACC. `Terminal WACC =` override, else `(post-year-10 riskfree rate or riskfree rate) + mature-market ERP`.
- Discounting uses the **cumulative product** of year-specific rates: `CDF_t = PROD over i=1..t of 1/(1 + WACC_i)`; `PV(FCFF_t) = FCFF_t × CDF_t`.

*Terminal value and value:*
- `Terminal ROC =` override, else the terminal cost of capital (which makes terminal growth value-neutral by construction).
- `Terminal reinvestment = (g_terminal / Terminal ROC) × EBIT(1−t)_terminal`, and 0 if `g_terminal <= 0`.
- `Terminal FCFF = EBIT(1−t)_terminal − Terminal reinvestment`
- `Terminal value = Terminal FCFF / (Terminal WACC − g_terminal)`; `PV(TV) = TV × CDF_10`.
- `Going-concern value = PV(TV) + SUM of PV(FCFF_1..10)`
- `Proceeds if the firm fails = ` (BV equity + BV debt) × pct, or Going-concern value × pct, depending on the chosen base.
- `Value of operating assets = Going-concern value × (1 − p_failure) + Proceeds × p_failure`
- `Value of equity = Operating assets − Debt (book, incl. lease debt) − Minority interests + Cash + Non-operating assets`
- `Value per share = (Value of equity − Value of employee options) / Shares outstanding`
- Trapped-cash haircut (optional): `Cash used = Cash − Trapped amount × (Marginal tax rate − Foreign tax rate)`.
- Employee options, dilution-adjusted Black–Scholes: `S_adj = (S × n_shares + V_option × n_options)/(n_shares + n_options)`; `d1 = [ln(S_adj/K) + (r − q + σ²/2)T]/(σ√T)`; `d2 = d1 − σ√T`; `V_option = S_adj e^(−qT) N(d1) − K e^(−rT) N(d2)`. Circular — iterate to a fixed point.
- Diagnostics: `Marginal ROIC = ΔEBIT(1−t) over 10 years / ΔInvested capital over 10 years`; `Average compounded WACC = (1/CDF_10)^(1/10) − 1`; `Value/price ratio`.

**Procedure:**
1. **Cleanse the base year.** Run the R&D converter and the operating-lease converter; feed their EBIT adjustments into base EBIT and their asset values into invested capital.
2. **Build the cost of capital** (bottom-up or multi-business beta, revenue-weighted ERP, synthetic or actual rating for the cost of debt, market-value weights). Note the circularity: lease debt is discounted at the pre-tax cost of debt, which in synthetic-rating mode depends on interest coverage, which includes imputed lease interest. Iterate.
3. **Set the value drivers** — next year's revenue growth and margin, the years 2–5 CAGR, the target margin and convergence year, and the sales-to-capital ratios by phase.
4. **Run the 10-year table** in the order: growth -> revenues -> margin -> EBIT -> NOL/tax -> EBIT(1−t) -> reinvestment -> FCFF -> invested capital -> ROIC.
5. **Fade the discount rate** from the initial WACC to the terminal WACC over years 6–10 and discount with the cumulative product, not a constant rate.
6. **Build the terminal year**, tying the reinvestment rate to `g/ROC` and defaulting terminal ROC to the terminal cost of capital.
7. **Apply the failure probability** if the firm has real distress risk; choose whether the recovery is based on book capital or on a fraction of going-concern value.
8. **Bridge to equity and to a per-share value**; subtract employee options (solving the circularity by iteration).
9. **Read the diagnostics** before shipping: marginal ROIC over the forecast, average compounded WACC, and value versus price. A value/price ratio above 2 or below 0.5 is a prompt to re-examine assumptions, not a conclusion.

**Reference data:**
- Structural conventions baked into the standard model: 10-year explicit forecast; growth constant in years 2–5 then linear fade over 6–10; tax rate constant years 1–5 then five equal steps; cost of capital constant years 1–5 then linear fade; terminal WACC = riskfree rate + mature-market ERP; terminal ROC = terminal WACC unless overridden.
- Mature-market ERP in the January 2022 vintage: **4.24%**.
- Cumulative default probabilities by rating (useful for choosing a failure probability):
  | Rating | 1yr | 5yr | 10yr |
  |---|---|---|---|
  | AAA | 0.00% | 0.35% | 0.70% |
  | AA | 0.02% | 0.31% | 0.72% |
  | A | 0.05% | 0.47% | 1.24% |
  | BBB | 0.16% | 1.58% | 3.32% |
  | BB | 0.61% | 6.52% | 11.78% |
  | B | 3.33% | 16.93% | 23.74% |
  | CCC/C | 27.08% | 46.19% | 50.38% |
- Two documented quirks of the reference spreadsheet worth knowing about: (a) the margin interpolation for years 2–5 anchors on the **year-1** margin while years 6–10 anchor on the **base-year** margin, producing a visible kink at year 6; (b) debt in the equity bridge is **book** debt plus lease debt, while debt in the WACC weights is the **estimated market value** of debt. Both are deliberate in the original; reproduce or fix them consciously.

**Worked example — SK Innovation, 1 January 2022 (KRW millions, shares in millions):**
```
Base year: revenues 32,357,222; reported EBIT −250,829; R&D capitalized (5-yr life)
  research asset 723,486.2, amortization 211,128.2, EBIT adjustment +40,434.8
  -> adjusted EBIT −210,394.2 (margin −0.65%)
  invested capital = 14,405,108 + 16,715,192 − 6,699,463 + 723,486.2 = 25,144,323.2

Cost of capital: unlevered beta 1.1432 (multi-business global), ERP 5.175% (revenue-weighted
  by operating region), pre-tax cost of debt 3.281% (Baa2/BBB rating), levered beta 1.7492,
  cost of equity 10.742%, weights E 58.6% / D 41.4% -> WACC 7.312%

Drivers: revenue growth 50% in year 1 then 5% CAGR years 2-5; margin 3% in year 1 rising to
  a 7.5% target by year 10; sales-to-capital 10 (yr 1), 5 (yrs 2-5), 1.5 (yrs 6-10);
  NOL carried in 731.4; effective tax 25% = marginal 25%

Year 1: revenue 48,535,833; margin 3%; EBIT 1,456,075; reinvestment 1,617,861; FCFF −525,622
Year 5: revenue 58,995,608; margin 5.25%; EBIT 3,097,269; reinvestment 1,872,876; FCFF 450,076
Year 10: revenue 69,046,992; margin 7.5%; EBIT 5,178,524; EBIT(1−t) 3,883,893;
         reinvestment 902,575; FCFF 2,981,318

Terminal: g 2% (= overridden post-year-10 riskfree rate); WACC 6.24% (= 2% + 4.24% mature ERP);
  ROC = WACC = 6.24% -> reinvestment rate 2%/6.24% = 32.05%
  EBIT(1−t) 3,961,571 − reinvestment 1,269,734 = terminal FCFF 2,691,837
  Terminal value = 2,691,837/(0.0624 − 0.02) = 63,486,718

Value: PV(TV) = 63,486,718 × 0.5088307 = 32,303,992; PV(10-yr FCFF) = 7,121,240
  Going-concern value 39,425,231; failure probability 12%, recovery 50% of going-concern value
  Operating assets = 39,425,231 × 0.88 + 19,712,616 × 0.12 = 37,059,718
  − debt 16,715,192 + cash 6,699,463 = equity 27,043,989; / 83.6 shares
  = value per share 323,493 vs price 273,500 -> price is 84.5% of value
Diagnostics: marginal ROIC over 10 years 45.97%; average compounded WACC 6.99%
```

**Determinism:**
- DETERMINISTIC: everything above, given the base-year financials, the value drivers, the discount-rate inputs and the reference tables. This is a pure function from ~25 numbers to a value per share, and the two circularities (lease debt / synthetic rating; option value / adjusted share price) are solved by fixed-point iteration.
- JUDGMENT: every driver — next year's growth and margin, the years 2–5 CAGR, the target margin and how fast to get there, the sales-to-capital ratios, the failure probability and recovery rate, whether to allow terminal excess returns, and the entire cost-of-capital assumption set. The engine's value is that it makes each of these an explicit, named, single number.

**Pitfalls:**
- Discounting with a constant WACC when the WACC path fades — you must use the cumulative product of year-specific rates.
- Letting terminal growth exceed the riskfree rate, or setting a terminal WACC that does not exceed terminal growth (the terminal value explodes or goes negative).
- Assuming terminal growth with no terminal reinvestment. The engine forces `g/ROC` for exactly this reason.
- Defaulting terminal ROC above the terminal cost of capital without an argument for a perpetual moat.
- Subtracting market-value debt in the equity bridge while the model uses book debt (or vice versa) — pick one and know which.
- Applying a failure probability *and* separately using a distress-adjusted discount rate: that double-counts.
- Ignoring the diagnostics. A marginal ROIC of 46% or a value/price of 3.0 is telling you an input is wrong.
- Porting the model without iteration turned on, silently getting the wrong cost of debt or option value.

**Sources:**
- spreadsheet:fcffsimpleginzu.xlsx — the complete model: Input sheet, Valuation output, Cost of capital worksheet, R&D converter, Operating lease converter, Synthetic rating, Option value, Diagnostics, Summary Sheet, and the January 2022 reference tables (mature ERP 4.24%, country ERPs, rating spreads, default probabilities, industry averages)
- spreadsheet:higrowth.xls — the earlier high-growth variant (speed-of-convergence margins, beta/debt-ratio convergence schedules, relative-valuation cross-check)
- valpacket1spr21 p.117-119, p.198, p.206, p.210, p.217 / valpacket1spr20 p.114-116, p.195, p.202, p.206, p.213 (the underlying structure: cash flow, discount rate, growth pattern, terminal value)
- cfpacket2spr20 p.249, p.261, p.263-264 (the same engine hand-built for Baidu and Disney)

**Related:** [[top-down-revenue-growth]], [[fcff]], [[terminal-value]], [[tax-rate-and-nols]], [[net-capital-expenditures]], [[rnd-capitalization]], [[operating-lease-capitalization]], [[return-on-invested-capital]], [[dcf-case-valuations]], [[cost-of-capital]], [[synthetic-rating]], [[employee-options]], [[equity-value-bridge]]

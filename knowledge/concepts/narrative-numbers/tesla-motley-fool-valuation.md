# Worked example: Tesla, November 2021, narrative to value per share

**Core idea:** This is the story process run end to end on a live, liquid, heavily-argued stock, using Damodaran's do-it-yourself FCFF template. The narrative is titled "The Payoff to Flexibility — A Plausible Path to Auto Dominance." Five story levers set the whole model. A ten-year, two-stage FCFF engine turns them into cash flows. A terminal value, an option overhang and a share count turn those into $571.29 per share, against a market price of $1,200. The value is a statement about the story, and the deck says so: change the levers and the answer moves by hundreds of dollars a share. The case is also the cleanest demonstration that more than 80% of a growth company's value can sit in the terminal value, which is a feature, not a bug.

**Formulas:**
- Revenue growth: 35.00% for years 1–5, then five equal linear steps down to the terminal rate, reaching 1.56% at year 10. Growth_t (years 6–10) = Growth_5 − ((Growth_5 − g_terminal)/5) × (t − 5).
- Margin convergence: Margin_t = Target − ((Target − Base margin)/Convergence year) × (Convergence year − t) for t ≤ convergence year; Target thereafter. Base 12.06%, target 16.00%, convergence year 5.
- EBIT_t = Revenues_t × Margin_t. EBIT(1−t)_t = EBIT_t × (1 − tax rate_t). Tax rate is constant at the effective 11.99% for years 1–5, then steps linearly to the 25% marginal rate by year 10.
- Reinvestment_t = (Revenues_t − Revenues_{t−1}) / Sales-to-capital_t. Sales-to-capital is 4.00 for years 1–5 and 2.67 for years 6–10 (the workbook sets years 6–10 as two-thirds of the years 1–5 ratio).
- FCFF_t = EBIT(1−t)_t − Reinvestment_t.
- Cumulated discount factor_t = Π_{s=1..t} 1/(1 + cost of capital_s). PV(FCFF_t) = FCFF_t × cumulated discount factor_t.
- Terminal reinvestment rate = Terminal growth / Terminal return on capital = 1.56% / 15.00% = 10.40%.
- Terminal value = Terminal FCFF / (Terminal cost of capital − Terminal growth) = 45,233.17 / (0.0606 − 0.0156) = $1,005,181.62M.
- Value of operating assets = PV(terminal value) + PV(cash flows over the next 10 years), then adjusted for failure: Expected value = Value × (1 − p_failure) + Distress proceeds × p_failure.
- Value of equity = Operating assets − Debt − Minority interests + Cash + Non-operating assets.
- Value per share = (Value of equity − Value of options) / Number of shares.
- Base-year EBIT adjustment for capitalised R&D: Adjusted EBIT = Reported EBIT + Current-year R&D − Amortisation of past R&D.

**Procedure:**
1. **Get the base year right.** Trailing 12-month revenues $46,848M and EBIT $4,586M. Capitalise R&D with a five-year life: current-year R&D $2,375M, past five years $1,491M, $1,390M, $1,460M, $1,378M, $834M. Research asset = $5,261.4M; amortisation = $1,310.6M; EBIT adjustment = 2,375 − 1,310.6 = +$1,064.4M. Adjusted EBIT = $5,650.4M, giving a base margin of 12.06%. No operating leases to convert.
2. **Set invested capital.** Book equity 28,494 + book debt 10,158 − cash 16,095 + research asset 5,261.4 = $27,818.4M. That gives base ROIC of 17.88% and sales-to-capital of 1.68.
3. **Get perspective.** Tesla's 69.50% revenue growth, 12.06% margin and 17.88% ROIC against a US auto industry at 14.31%, 3.41% and 2.89%. The largest global automakers earn 0.3% to 8.5% margins on low single-digit growth.
4. **Choose the five levers** against their reference menus. See [[narrative-to-value-drivers]].
5. **Override the defaults you mean to override.** Terminal return on capital set to 15% against a terminal cost of capital of 6.06%, on the argument that entry costs limit competition. Everything else left at default.
6. **Run the ten-year schedule and the terminal year.**
7. **Value the employee options and subtract them.** 101.62 million options, average strike $69.04, average maturity 5.80 years, volatility 30%, riskfree 1.56%. Use a dilution-adjusted Black-Scholes. The calculation is circular, because the stock price input is the model's own value per share, which in turn nets out the option value. Solve by iteration.
8. **Build the bridge to value per share and compare with price.**
9. **Read the diagnostics.** Marginal ROIC, ending ROIC, average compounded WACC, and value as a percent of price.

**Reference data:** Chosen drivers, November 2021:

| Driver | Value |
|---|---|
| Compounded revenue growth, next 5 years | 35.00% |
| Target pre-tax operating margin | 16.00% |
| Year of convergence to target margin | 5 |
| Sales to capital, years 1–5 | 4.00 |
| Sales to capital, years 6–10 | 2.67 |
| Riskfree rate | 1.56% |
| Initial cost of capital | 6.00% |
| Terminal cost of capital | 6.06% |
| Terminal return on capital (override) | 15.00% |
| Probability of failure | 0.00% |
| Effective / marginal tax rate | 11.99% / 25.00% |
| Shares outstanding | 1,123.00 million |
| Stock price | $1,200.00 |

Cash-flow forecast ($ millions):

| Year | Rev growth | Revenues | Margin | EBIT | Tax rate | EBIT(1−t) | Reinvestment | FCFF | Cost of capital | Cum. DF | PV(FCFF) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Base | — | 46,848.00 | 12.06% | 5,650.40 | 11.99% | 4,972.96 | — | — | — | — | — |
| 1 | 35.00% | 63,244.80 | 12.85% | 8,126.27 | 11.99% | 7,151.99 | 4,099.20 | 3,052.79 | 6.00% | 0.9434 | 2,879.99 |
| 2 | 35.00% | 85,380.48 | 13.64% | 11,643.06 | 11.99% | 10,247.15 | 5,533.92 | 4,713.23 | 6.00% | 0.8900 | 4,194.76 |
| 3 | 35.00% | 115,263.65 | 14.42% | 16,626.15 | 11.99% | 14,632.80 | 7,470.79 | 7,162.01 | 6.00% | 0.8396 | 6,013.36 |
| 4 | 35.00% | 155,605.92 | 15.21% | 23,671.13 | 11.99% | 20,833.14 | 10,085.57 | 10,747.57 | 6.00% | 0.7921 | 8,513.08 |
| 5 | 35.00% | 210,068.00 | 16.00% | 33,610.88 | 11.99% | 29,581.19 | 13,615.52 | 15,965.67 | 6.00% | 0.7473 | 11,930.48 |
| 6 | 28.31% | 269,542.45 | 16.00% | 43,126.79 | 14.59% | 36,833.99 | 22,302.92 | 14,531.08 | 6.01% | 0.7049 | 10,242.68 |
| 7 | 21.62% | 327,828.31 | 16.00% | 52,452.53 | 17.19% | 43,434.08 | 21,857.20 | 21,576.89 | 6.02% | 0.6648 | 14,344.99 |
| 8 | 14.94% | 376,792.75 | 16.00% | 60,286.84 | 19.80% | 48,352.64 | 18,361.66 | 29,990.98 | 6.04% | 0.6270 | 18,803.94 |
| 9 | 8.25% | 407,870.61 | 16.00% | 65,259.30 | 22.40% | 50,642.62 | 11,654.20 | 38,988.42 | 6.05% | 0.5912 | 23,051.08 |
| 10 | 1.56% | 414,233.39 | 16.00% | 66,277.34 | 25.00% | 49,708.01 | 2,386.04 | 47,321.96 | 6.06% | 0.5574 | 26,379.51 |
| Terminal | 1.56% | 420,695.43 | 16.00% | 67,311.27 | 25.00% | 50,483.45 | 5,250.28 | 45,233.17 | 6.06% | — | — |

Value bridge ($ millions except per-share):

| Line | Value |
|---|---|
| Terminal cash flow | 45,233.17 |
| Terminal cost of capital | 6.06% |
| Terminal value | 1,005,181.62 |
| PV(terminal value) | 560,336.04 |
| PV(cash flows, next 10 years) | 126,353.86 |
| Value of operating assets | 686,689.91 |
| Probability of failure | 0.00% |
| Proceeds if the firm fails | 343,344.95 (unused at p = 0) |
| − Debt | 10,158.00 |
| − Minority interests | 0 |
| + Cash | 16,095.00 |
| + Non-operating assets | 0 |
| Value of equity | 692,626.91 |
| − Value of options | 51,070.25 |
| Value of equity in common stock | 641,556.66 |
| Number of shares | 1,123.00 |
| **Estimated value per share** | **$571.29** |
| Price | $1,200.00 |
| Price as % of value | 210.05% |

Option valuation detail (dilution-adjusted Black-Scholes, solved by iteration): dilution-adjusted spot S_adj = (571.288 × 1,123 + 502.561 × 101.62) / 1,224.62 = 565.585. d1 = 3.39747, N(d1) = 0.99966. d2 = 2.67497, N(d2) = 0.99626. Value per option = 565.585 × 0.99966 − 69.04 × e^(−0.0156 × 5.8) × 0.99626 = $502.561. Total option value = 502.561 × 101.62 = $51,070.25M.

Diagnostics: invested capital rises from 27,818.4 to 145,185.4 over ten years, a change of 117,367.0. Marginal ROIC = 51.66%. ROIC at year 10 = 34.24%. Average compounded WACC = 6.02%. Value as a percent of price = 47.61%, which trips the workbook's "Value seems low. See below" flag.

**Worked example:** Trace year 1. Revenues = 46,848 × 1.35 = $63,244.80M. Margin interpolates from the 12.06% base toward the 16% target over five years, giving 12.85%. EBIT = 63,244.80 × 12.85% = $8,126.27M. Tax at the effective 11.99% leaves EBIT(1−t) = $7,151.99M. Revenue rose by $16,396.80M, so reinvestment = 16,396.80 / 4.00 = $4,099.20M. FCFF = 7,151.99 − 4,099.20 = $3,052.79M. Discounted at 6.00%, PV = $2,879.99M. Repeat for ten years, add the terminal value of $1,005,181.62M discounted at the year-10 factor of 0.5574, and the operating assets come to $686,689.91M.

**Determinism:**
- DETERMINISTIC: the entire engine. Base-year cleanup (R&D life, R&D history → research asset, EBIT adjustment, invested capital). The growth, margin, tax and WACC paths. Reinvestment, FCFF, discounting, terminal value, the failure adjustment, the option value (given S, K, T, sigma, r, share and option counts, solved to a fixed point), and value per share. All diagnostics.
- JUDGMENT: the five levers and the two overrides. The 35% growth rate needs a view on EV market size and Tesla's share of it. The 16% margin needs a view on pricing power against an industry median of 3.01%. The 4.00 sales-to-capital needs a view on capacity already built, against an auto median of 1.37. The 6.00% cost of capital comes from the market distribution. The 15% terminal ROC needs a durable-moat argument. The 0% failure probability needs a view on the balance sheet. Also the choice to capitalise R&D over five years, and the 30% volatility used for the options.

**Pitfalls:**
- Reporting $571.29 as "the" value. It is the value of one story. Move the growth lever to A5 (20% auto market share, 40% CAGR) or the margin lever to B5 (software, 21.24%) and the answer changes dramatically.
- Ignoring the R&D capitalisation. Without it EBIT is $4,586M, not $5,650.4M, and both the base margin and invested capital are wrong.
- Missing the option overhang. $51.07 billion of option value is $45.48 per share.
- Treating a high terminal-value share as a modelling error. More than 80% of equity value sitting in the terminal value is normal for a growth company.
- Leaving the terminal ROC override on without stating the moat. A terminal ROC of 15% against a 6.06% terminal cost of capital is a claim of perpetual excess returns.
- A sales-to-capital ratio of 4.00 against an industry median of 1.37 implies a marginal ROIC of 51.66%. That must be argued, not assumed. See [[narrative-consistency-checks]].
- Reproducing the workbook without handling the circular option calculation. It needs iteration to a fixed point, not a single pass.

**Sources:**
- valuationmotleyfool p.11, p.12, p.13, p.14, p.15, p.16, p.17, p.18, p.19, p.20, p.21, p.22, p.23, p.24
- valuationmotleyfool p.3, p.4, p.5, p.8 (the DCF structure the engine implements)
- motley-fool-tesla-xlsx: `Master Inputs`, `Input sheet`, `Valuation output` (rows 2-14 and the value block B16-B35), `Option value`, `R& D converter`, `Diagnostics`, `Stories to Numbers`, `Summary Sheet`

**Related:** [[narrative-to-value-drivers]], [[landscape-survey]], [[narrative-consistency-checks]], [[value-vs-price-gap]], [[narrative-numbers-bridge]], [[uber-narrative-valuation]], [[narrative-scenario-grids]], [[story-to-numbers-process]]

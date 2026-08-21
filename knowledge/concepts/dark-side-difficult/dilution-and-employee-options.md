# Dilution and employee options in a young-company DCF

**Core idea:** A young growth company will almost certainly have more shares outstanding in five years than today. It must issue equity to fund growth or pay for acquisitions, and its employee options will be exercised if it succeeds. Analysts often "fix" this by inflating the share count. That is double counting. A properly built DCF already contains both effects even though it divides by **today's** share count: future equity needs show up as negative free cash flow in the early years, and their present value is exactly the dilution; existing options are valued as options and subtracted from equity value. Future option grants are handled by expensing stock-based compensation in the forecast earnings.

**Formulas:**
- Dilution from future issuance is implicit: `Equity value today = PV(all FCFF including the negative early years) + non-operating assets − debt`. The negative early FCFF reduces that value by exactly the present value of the equity that must be raised.
- Existing options, dilution-adjusted Black-Scholes:
  - `S_adj = (S × n_shares + W × n_options) / (n_shares + n_options)` — circular, because `W` is the option value being solved for. Solve by fixed-point iteration (start with plain Black-Scholes on `S`).
  - `d1 = [ln(S_adj/K) + (r − q + σ²/2) × T] / (σ√T)`; `d2 = d1 − σ√T`.
  - `W = S_adj × e^(−qT) × N(d1) − K × e^(−rT) × N(d2)`, with `N(·)` the standard normal CDF.
  - `Value of options outstanding = W × n_options`.
- Per-share value: `Value per share = (Value of equity − Value of options outstanding) / n_shares` using the **undiluted** current share count.

Symbols: `S` current stock price; `K` average strike; `T` average maturity in years; `σ` annualized standard deviation of the stock price; `r` riskfree (T-bond) rate; `q` annualized dividend yield; `n_shares` shares outstanding; `n_options` options/warrants outstanding; `W` value per option.

**Procedure:**
1. Build the DCF normally and let early FCFF go negative wherever reinvestment exceeds after-tax operating income. Do not truncate those years at zero.
2. Forecast operating income **after** stock-based compensation expense. Do not add SBC back as a "non-cash charge" — the grants are real compensation and the future dilution they cause is already priced by expensing them.
3. Collect the option inputs: number outstanding, average strike, average maturity, stock-price volatility, riskfree rate, dividend yield.
4. Value the options with the dilution-adjusted Black-Scholes above, iterating to convergence on `S_adj`.
5. Subtract the total option value from equity value, then divide by the current (undiluted) share count.
6. Do **not** apply any further dilution adjustment, and do not use fully diluted or treasury-method share counts on top of step 5.

**Reference data:** Option-valuation inputs and outputs from the negative-earnings model (fcffneg.xls, Option Valuation sheet) — a complete, reproducible instance.

| Input | Value |
|---|---|
| Current stock price S | 12.57 |
| Strike price K | 13.375 |
| Expiration T (years) | 8.4 |
| Volatility σ | 0.50 |
| Dividend yield q | 0.0 |
| Riskfree rate r | 0.065 |
| Options/warrants outstanding | 38 |
| Shares outstanding | 886.467 |

Intermediate and output values: `S_adj` converges to 12.377534; `d1` = 1.047862; `d2` = −0.401276; `N(d1)` = 0.852649; `N(d2)` = 0.344108; `W` = 7.887664; total option value = 7.887664 × 38 = **299.7312**, subtracted from equity of 10,123.34 to give 9,823.61, then divided by 886.467 shares → $11.08 per share.

Option overhangs in the packet's valuations: Amazon (Jan 2000) $2,892m of options valued at the then-$84 stock price, against equity of $14,847m; Amgen (May 2007) $479m against equity of $87,226m; Hormel (2008) $53m of management options deducted in the status-quo valuation.

**Worked example:** Amazon, January 2000. The present value of the negative FCFF in the first six years reduced equity value by **$3.09 billion — about a 16% cut**. That number *is* the dilution from the equity Amazon would have to raise; no share-count adjustment is needed or allowed on top of it. Separately, the $2,892m option value was subtracted, leaving $11,955m of common equity and a value of $35.08 per share.

**Determinism:** DETERMINISTIC — (S, K, T, σ, r, q, n_options, n_shares) → S_adj, d1, d2, W, total option value, and then (equity value, option value, share count) → value per share. The dilution effect itself is deterministic given the FCFF path. JUDGMENT: the volatility estimate, the average strike and maturity when the option pool is heterogeneous, whether to treat unvested options at all, and how much future stock-based compensation to build into forecast margins.

**Pitfalls:**
- Adding an explicit dilution haircut on top of a DCF that already carries negative early FCFF — the single most common double count.
- Using a fully diluted share count **and** subtracting the option value.
- Adding back stock-based compensation because "it isn't a cash expense". The source calls this out as a ploy.
- Valuing options at intrinsic value (max(S−K, 0)) instead of as options; deep out-of-the-money employee options still carry large time value.
- Ignoring the dilution adjustment inside Black-Scholes when the option pool is large relative to shares outstanding.
- Forgetting that the option value must be recomputed if the stock price used in the model changes.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.304
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.299
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.295
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.290
- spreadsheet model doc: special-troubled.md — fcffneg.xls, Option Valuation sheet
- spreadsheet model doc: ginzu-fcff-corona.md — Option value sheet

**Related:** [[young-company-valuation]], [[sales-to-capital-reinvestment]], [[value-versus-price]], [[option-pricing]], [[equity-bridge]]

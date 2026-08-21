# Commodity and cyclical companies: keep macro out of the micro

**Core idea:** The value of an oil company depends on the price of oil, and the value of a steel maker depends on the cycle. If you build your own oil forecast into the valuation, the answer becomes a blend of two opinions — your view on oil and your view on the company — and no reader can tell which is doing the work. Worse, you cannot act on it, because you no longer know whether you are buying a good company or a bet on a commodity. The discipline is to separate macro from micro: run the valuation at the **current market price** of the commodity, or at the futures strip, and then state your macro disagreement separately. If you think oil is going to $80, say so as a second statement, or better, express the uncertainty as a distribution and simulate.

**Formulas:**
- Commodity-driven revenue, fitted from history: `Revenues = a + b × Commodity price`. For Shell (annual data, 1989–2015): `Revenues ($m) = 39,992.77 + 4,039.40 × Average oil price per barrel`, with an R² of **96.44%**.
- `Pre-tax operating income = Revenues × Operating margin`.
- `FCFF = After-tax operating income + Depreciation − Capital expenditures − Change in working capital`.
- `Terminal value = Terminal-year FCFF / (Terminal cost of capital − g)`.
- Normalization anchors, all drawn from the firm's own long history rather than the current trough: revenue growth = historical compounded growth; operating margin = long-run average margin; terminal return on capital = long-run average ROC.
- Equity bridge: `Value of equity = Operating assets + Cash + Cross holdings − Debt − Minority interests`.

**Procedure:**
1. Identify the macro driver — the commodity price for a commodity firm, the economic cycle for a cyclical.
2. Establish the link empirically. Regress the company's revenues on the commodity price over as long a history as you have, and report the R². For Shell the R² of 96.44% means the oil price essentially *is* the revenue model.
3. Set the base revenue from **today's** market price (or the futures curve), not from your own forecast. Shell, March 2016: `39,992.77 + 4,039.40 × 40 = $201,569m` at a $40 oil price.
4. Normalize the margin. Do not use the trough margin as the forecast margin; converge to the long-run average. Shell's base margin was 3.01%, converging to its 2000–2015 average of 9.35%.
5. Normalize the return on capital for the terminal year (Shell: 12.37%, its historical average).
6. Grow revenues at the firm's own historical compounded rate unless you have a reason to differ (Shell: 3.91% a year).
7. Value the firm and report the answer as *"worth X at today's commodity price"*.
8. State your macro view separately, then quantify it: rerun at other prices, or draw the price from a distribution and simulate ([[scenario-analysis-and-simulation]]).
9. For a deep cyclical with no usable commodity price link, normalize earnings instead ([[normalized-earnings]]).

**Reference data:** Shell, March 2016, oil-price-neutral FCFF valuation at $40 per barrel. $ millions.

| Item | Base | Yr 1 | Yr 2 | Yr 3 | Yr 4 | Yr 5 | Terminal |
|---|---|---|---|---|---|---|---|
| Revenues | 201,569 | 209,450 | 217,639 | 226,149 | 234,991 | 244,180 | 249,063 |
| Operating margin | 3.01% | 6.18% | 7.76% | 8.56% | 8.95% | 9.35% | 9.35% |
| FCFF | — | 3,246.14 | 5,788.19 | 7,269.29 | 8,205.44 | 9,203.68 | 13,011.34 |
| Present value | — | 2,953.45 | 4,791.47 | 5,474.95 | 5,622.81 | 140,940.73 (includes terminal value) | — |

Other inputs: base operating income $6,065m; tax rate 30%; base after-tax operating income $4,245.5m; base depreciation $26,714m; base capital expenditure $31,854m; revenue growth 3.91% a year; cost of capital 9.91% in years 1–5 falling to 8.00% in the terminal year; terminal ROC 12.37%; terminal value $216,855.71m.

Equity bridge: operating assets $159,783.41m + cash $31,752m + cross holdings $33,566m (long-term joint-venture investments) − debt $58,379m − minority interests $1,245m = equity $165,477.41m; ÷ 4,209.7m shares = **$39.31 per share**.

Simulation on the same model, drawing the steady-state oil price from a right-skewed distribution and the target operating margin from a roughly normal one:

| Percentile | Value per share |
|---|---|
| 0% | $6.55 |
| 10% | $23.90 |
| 20% | $27.73 |
| 30% | $30.89 |
| 40% | $33.88 |
| 50% | $36.99 |
| 60% | $40.28 |
| 70% | $44.22 |
| 80% | $49.24 |
| 90% | $57.49 |
| 100% | $197.11 |

**Worked example:** Shell at $40 oil. The regression turns the oil price into revenue: `39,992.77 + 4,039.40 × 40 = $201,569m`. The base margin of 3.01% is a trough number, so it converges over five years to the 9.35% long-run average, lifting after-tax operating income even without revenue growth beyond 3.91% a year. Terminal FCFF of $13,011.34m at a terminal cost of capital of 8.00% gives a terminal value of $216,855.71m. The final answer is **$39.31 per share at a $40 oil price** — and the point of saying it that way is that a reader who thinks oil will be $60 can rerun the regression rather than argue with the DCF. The simulation makes the same statement in one picture: a median of $36.99 with a plausible range from the low $20s to the high $50s.

**Determinism:** DETERMINISTIC — (regression coefficients, oil price) → revenues; (revenues, margin path, tax rate, depreciation, cap ex, working-capital change) → FCFF; (FCFF path, cost-of-capital path, terminal inputs) → value per share. The regression itself is deterministic given the historical revenue and price series. JUDGMENT: which commodity price to use (spot, futures strip, or an average), the historical window for the normalization anchors, whether the long-run margin is still achievable after a structural change, and the input distributions for the simulation.

**Pitfalls:**
- Embedding your own commodity forecast in the valuation. The resulting number cannot be attributed to company analysis or to macro analysis.
- Using the trough margin as the forecast margin, or the peak margin at the top of the cycle. Both mistake a point in the cycle for the business.
- Extrapolating trough revenues at a normal growth rate without recognising that the price will move.
- Treating the finite life of the resource as irrelevant. For a commodity firm, reserves cap growth permanently.
- Forgetting that the risk can lie dormant for years. A long stretch of prosperity in a cyclical business is not evidence that the cycle is dead.
- Skipping the cross holdings and minority interests in the equity bridge — for Shell they were worth about $33.6bn and −$1.2bn respectively ([[cross-holdings]]).
- Presenting a single point estimate when the driver is a volatile price. The simulation costs almost nothing and carries far more information.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.352-357
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.343-348

**Related:** [[normalized-earnings]], [[scenario-analysis-and-simulation]], [[cross-holdings]], [[difficult-company-taxonomy]], [[market-and-macro-crisis-valuation]], [[fcff-valuation]], [[terminal-value]]

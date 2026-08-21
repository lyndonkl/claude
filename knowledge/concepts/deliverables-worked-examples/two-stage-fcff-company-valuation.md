# Two-stage FCFF valuation as a project deliverable

**Core idea:** Part X of the corporate finance project values the firm as a going concern with a two-stage FCFF model, and the inputs come from the earlier parts rather than from thin air. Growth in the high-growth phase is derived from fundamentals — reinvestment rate times return on capital — not from analyst forecasts. The growth-phase discount rate uses the capital structure the project recommended. The stable phase sets beta to 1.0 and caps growth near the economy's growth rate. The output is a value per share, compared against the market price, plus an answer to the project's real question: which variable drives the value, and what would a value-enhancer do?

**Formulas:**
- Expected growth rate = Reinvestment rate × Return on capital.
- FCFF = EBIT × (1 − t) − Reinvestment. t = marginal tax rate.
- Operational assets = PV(growth-phase FCFF) + PV(terminal / stable-phase value).
- Terminal value at the end of the growth phase = FCFF_stable / (WACC_stable − g_stable).
- Equity value = Operational assets + Cash + Non-operating investments − Debt − Minority interest − Value of equity options.
- Value per share = Equity value / Shares outstanding.

**Procedure:**
1. **Choose the growth pattern** — stable, 2-stage or 3-stage — and the length of the high-growth phase. Mature firms get shorter phases; growth firms and firms in transition get longer ones.
2. **Set the growth-phase inputs**: reinvestment rate and ROC. Derive growth as their product rather than assuming it.
3. **Set the growth-phase WACC** using the recommended (optimal) capital structure from Part VI.
4. **Set the stable-phase inputs**: beta = 1.0, a stable debt ratio, a stable ROC, a stable reinvestment rate, and a stable growth rate at or below the economy's long-run growth rate.
5. **Compute current FCFF** = EBIT × (1 − t) − reinvestment.
6. **Discount** the growth-phase cash flows at the growth-phase WACC and the terminal value at the stable-phase WACC. Sum to get operational assets.
7. **Bridge to equity**: add cash and non-operating investments, subtract debt, minority interest and the value of employee equity options.
8. **Divide by shares** and compare to the market price.
9. **Explain the gap.** A large positive gap between price and value usually means the market expects higher growth than you assumed; a negative gap may reflect uncertainty the model does not capture.
10. **Name the key variable** driving the value and state the value-enhancement path a hired manager would follow.

**Reference data:** Spring 2015 valuation assumptions.

| Valuation input | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| WACC, growth phase | 6.58% | 6.13% | 6.29% | 6.39% |
| WACC, stable phase | 6.33% | 5.32% | 6.88% | 4.79% |
| Debt ratio, stable phase | 30% | 50% | 20% | 60% |
| Beta, stable phase | 1.00 | 1.00 | 1.00 | 1.00 |
| Reinvestment rate, growth | 18.59% | 20% | 30% | 36.62% |
| Reinvestment rate, stable | 25.00% | 15% | 25.00% | 25.00% |
| ROC, growth | 22.14% | 20.10% | 21.94% | 5.58% |
| ROC, stable | 10.00% | 15.00% | 10% | 10.00% |
| Growth rate, growth phase | 4.12% | 4.02% | 6.58% | 2.05% |
| Growth rate, stable phase | 2.50% | 2.25% | 2.50% | 2.50% |
| Growth period (years) | 5 | 5 | 10 | 10 |

FCFF valuation output:

| FCFF valuation | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| EBIT × (1−t) ($m) | 1,815 | 5,179 | 462 | 1,022 |
| Reinvestment ($m) | 338 | 1,036 | 33 | 374 |
| FCFF ($m) | 1,478 | 4,143 | 429 | 648 |
| PV growth phase ($m) | 6,800 | 19,200 | 3,533 | 5,084 |
| PV stable phase ($m) | 35,746 | 126,865 | 10,748 | 18,995 |
| Operational assets ($m) | 42,546 | 146,065 | 14,280 | 24,079 |
| Cash ($m) | 1,708 | 2,078 | 419 | 438 |
| Non-operating investments ($m) | 135 | 1,234 | 339 | 233 |
| Debt ($m) | 7,870 | 52,166 | 534 | 6,829 |
| Minority interest ($m) | 2 | 0 | 0 | 14 |
| Equity value ($m) | 32,830 | 95,977 | 12,988 | 16,566 |
| Equity options ($m) | 772 | 1,825 | 324 | 292 |
| Shares outstanding (m) | 753.10 | 961.12 | 31.00 | 304.57 |
| Value per share | $42.57 | $97.96 | $408.50 | $53.43 |
| Current share price | $49.78 | $98.23 | $633.82 | $49.78 |

Verdicts: McDonald's fairly valued; Starbucks and especially Chipotle trade well above the estimate; Tyson trades slightly below.

Published data sets for this part: betas by industry; growth fundamentals by industry; cap ex and working capital by industry.

**Worked example:** Starbucks, 2015. Growth-phase growth = 18.59% reinvestment × 22.14% ROC ≈ 4.12%. Stable-phase growth = 25% × 10% = 2.50%. Current FCFF = $1,815m − $338m = $1,478m. Discounting five years of growth-phase cash flows at 6.58% gives a PV of $6,800m; the stable-phase value discounted back is $35,746m. Operational assets = $42,546m. Bridge: + $1,708m cash + $135m non-operating investments − $7,870m debt − $2m minority interest = $32,830m of equity value. Subtract $772m of equity options and divide by 753.10m shares → $42.57 per share against a $49.78 market price. The team's reading: the market is pricing in higher growth than the 4.12% fundamental rate implies.

**Determinism:** DETERMINISTIC — given the assumption table plus balance-sheet inputs, a script produces growth rates, FCFF, both present values, operational assets, the equity bridge and value per share exactly. The comparison to market price is mechanical. JUDGMENT — the growth pattern and phase length, the reinvestment rates, the stable ROC, the stable capital structure, the option value, and the explanation for any price-value gap. Naming the key value driver and the value-enhancement path is pure reasoning; it needs the competitive story and the results of Parts IV, VI and IX.

**Pitfalls:**
- Assuming a growth rate directly instead of deriving it from reinvestment × ROC. Tyson's 2.05% growth looks low only because its ROC is 5.58%; assuming a higher growth rate without raising ROC would create value out of nothing.
- Letting stable-phase growth exceed the economy's growth rate. All four firms here are capped at 2.25-2.50%.
- Forgetting the equity-options deduction. It is $772m at Starbucks and $1,825m at McDonald's — roughly $1-2 per share.
- Using market debt in the bridge that differs from the debt used in the WACC weights without saying why.
- Concluding "overvalued" from the DCF alone. The gap may be the market's growth expectation, and the project asks *why* the gap exists.
- Using the current capital structure in the growth phase after recommending a different optimum, or vice versa, without stating which was chosen.

**Sources:**
- corporate_finance--project--cfproj p.13
- corporate_finance--project--food2015 p.17-18, p.2

**Related:** [[cost-of-capital-buildup-deliverable]], [[optimal-debt-ratio-wacc-schedule]], [[return-spread-and-eva-analysis]], [[dcf-model-selection]], [[dcf-sensitivity-analysis]], [[project-executive-summary-scorecard]]

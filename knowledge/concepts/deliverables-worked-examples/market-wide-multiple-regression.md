# Relative valuation against the whole market (market-wide regression)

**Core idea:** Step 4 of the equity valuation project widens the comparison from the sector to every listed firm. Damodaran posts a market-wide regression of each common multiple on its fundamental drivers, fitted across all firms in a market. Plug the target firm's fundamentals into that equation, get a predicted multiple, convert it to a price, and compare it to the market price. This catches the case where a whole sector is mispriced — a sector regression cannot detect that, because it takes the sector's own pricing as the benchmark. The trade-off is fit: a market-wide equation explains less of any individual firm and can produce nonsense for unusual firms.

**Formulas:** The posted regressions take the form Multiple = Σ (coefficient × fundamental driver), with drivers chosen to match the multiple:
- Predicted price = Predicted multiple × the matching per-share denominator.
- The same under/over-valued comparison as the sector version: predicted price above market price = undervalued.

**Procedure:**
1. Take the *latest* posted market-wide regression for the multiple chosen in Step 3. It must be the same multiple used for the sector comparison so the two are comparable.
2. Assemble the firm's values for each driver in the equation — typically some combination of growth, beta, payout ratio, return on equity or capital, operating margin, reinvestment rate and debt-to-capital.
3. Evaluate the equation to get the predicted multiple.
4. Convert to a predicted price using the firm's own earnings, book value, sales or book capital per share.
5. Compare to the market price and to the sector-regression price from Step 3.
6. **Handle non-US firms.** If the firm has an ADR listed in the US, the US market regression may be used. As an optional stretch, fit your own regression in the foreign market using the 50 largest firms there to limit the workload.
7. **Apply the plausibility test.** Discard any regression whose predicted price is economically implausible and say why.
8. **Interpret disagreement between the two regressions.** Look at what each weights. If the market equation weights growth heavily and the sector equation weights margins, a gap between them says the sector is pricing growth differently from the market as a whole.

**Reference data:** Market-wide regressions applied in the six-company equity valuation project.

| Firm | Multiple | Market regression | Predicted multiple → price | Market price |
|---|---|---|---|---|
| ACS | PBV | 0.159 ROE + 0.358 Beta + 0.117 Growth − 0.011 Payout (R² = 48%) | 2.65 → $48.36 (final table lists 2.54) | $50.50 |
| Apple | PE | 1.228 g − 0.011 Payout + 11.75 Beta | 23.4 → $18.31 | $20.85 |
| Biosite | Value-to-Sales | 0.264 g(rev) + 0.150 Operating Margin − 0.009 Reinvestment Rate − 0.048 Debt/Capital | 4.315 → $29.68 | $26.12 |
| Gundle | P/BV | 0.159 ROE + 0.358 Beta + 0.117 g − 0.011 Payout | 2.42 → $31.49 | $19.73 |
| Infosys | PEG | 12.393 + 1.474 Beta − 0.015 Payout − 4.55 ln(g) (R² = 41.8%) | 0.34 → Rs 16.82 | Rs 4,912 |
| Nextel Partners | Value/Book Capital | 1.89 + 0.10 g(rev) + 0.061 ROC − 0.043 Debt/Capital | 1.87 → $12.15 | $11.72 |

Symbols: ROE = return on equity; ROC = return on capital; Beta = market beta; g = expected earnings growth; g(rev) = expected revenue growth; Payout = dividends/earnings; Operating Margin = operating income/sales; Reinvestment Rate = reinvestment/after-tax operating income; Debt/Capital = debt/(debt+equity).

**Worked example:** Two opposite outcomes from the same step.

*It works:* ACS. The market PBV regression predicts 2.65, implying $48.36 per share. The DCF gives $48.75 and the peer average $47.75. Three independent methods land within a dollar of each other, and the authors note that "the market regression works well for ACS." That agreement is itself evidence, and it makes the $50.50 market price look modestly high.

*It fails:* Infosys. Using its ADR listing, the US market PEG regression predicts a PEG of 0.34, implying a price of Rs 16.82 against a market price of Rs 4,912 — three orders of magnitude off. The prediction is economically implausible, so the regression is rejected outright rather than averaged in. The stated reason: the equation is fitted on US firms and cannot handle a company with Infosys's growth-and-risk combination in a different market.

*It arbitrates:* Biosite. The market VS regression gives $29.68, much closer to the $32.76 DCF than the comparables regression's $22.50. The authors argue the market comparison is the more accurate one here, because the market regression weights growth heavily while the comparables regression weights margins, and growth appears undervalued within the Medical Supply sector.

**Determinism:** DETERMINISTIC — evaluating the posted equation at the firm's driver values, converting to a price, and comparing to the market price and to the sector prediction. JUDGMENT — whether the posted regression applies to this firm at all, whether to use the US regression for a foreign firm via its ADR, whether to fit a local regression instead, and whether a prediction is plausible. Judging *why* the market and sector regressions disagree requires knowing which drivers each weights and what the sector is currently pricing.

**Pitfalls:**
- Averaging in an implausible prediction rather than discarding it. Infosys's Rs 16.82 would destroy any weighted average it entered.
- Using a US market regression for a foreign firm without an ADR, or without acknowledging that the fit was estimated on a different market.
- Using a different multiple in Step 4 from the one chosen in Step 3, which makes the two comparisons incomparable.
- Using a stale posted regression. The step specifies the *latest* one; coefficients move with the market.
- Treating close agreement between the market regression and the DCF as confirmation without checking that both are not driven by the same input, typically the growth rate.

**Sources:**
- valuations--projects--eqprojspr19 p.6
- valuations--projects--valproject2 p.3, p.6, p.9, p.12, p.14, p.19

**Related:** [[relative-valuation-comparables-regression]], [[valuation-triangulation-and-recommendation]], [[dcf-model-selection]], [[equity-valuation-project-blueprint]]

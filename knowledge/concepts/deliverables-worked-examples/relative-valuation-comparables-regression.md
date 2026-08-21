# Relative valuation against comparables (peer average and sector regression)

**Core idea:** Step 3 of the equity valuation project prices the firm against its peers using one multiple, two ways. The simple way is the peer average, adjusted qualitatively for differences. The better way is a sector regression: regress the multiple across the peer firms on the fundamentals that drive it, then plug in the target firm's own fundamentals to get a predicted multiple. The regression is superior because it *controls* for the differences the simple average only hand-waves at. Choosing the multiple is itself part of the analysis — try several and keep the one whose regression has the highest R².

**Formulas:**
- Predicted multiple = regression equation evaluated at the target firm's fundamentals.
- Predicted price = Predicted multiple × the corresponding per-share denominator (earnings for PE, book value for PBV, sales for VS, book capital for Value/BV Capital, PE ÷ growth for PEG).
- Peer-average price = Average peer multiple × the target's denominator.
- Undervalued when predicted price > market price; overvalued when predicted price < market price.

**Procedure:**
1. **Define the peer set by defensible criteria.** Typical screens: same industry classification, revenues above a size floor, similar growth. State the criteria; they are the part most open to challenge.
2. **Clean the sample.** Remove negative-earnings firms when using earnings multiples — a negative PE is meaningless. Remove outliers so the sample reflects the target.
3. **Try several multiples.** Run regressions for each candidate and compare R². Pick the multiple with the best fit and use it for the whole group.
4. **Choose explanatory variables** from the multiple's own drivers: ROE for PBV, payout/beta/growth for PE, growth/margin/leverage for value-to-sales, ROC/leverage for value-to-book-capital.
5. **Limit the number of variables when the sample is small.** With few comparables, use one explanatory variable.
6. **Report the regression properly**: coefficients, standard errors, t-statistics, p-values, standard error of the estimate, R² and adjusted R².
7. **Compute both estimates** — the peer-average price and the regression-predicted price — and report them separately. They often disagree substantially.
8. **Sanity-check the prediction.** Discard any regression whose predicted price is economically implausible.
9. **Interpret the divergence.** If the market regression weights growth heavily and the comparables regression weights margins, the gap between them tells you what the sector is currently pricing.

**Reference data:** Sector-comparables regressions from the six-company equity valuation project.

| Firm | Peer set | Multiple | Regression |
|---|---|---|---|
| ACS | 77 US computer software/services firms, screened on size and growth | PBV | PBV = 0.608 + 15.926 × ROE. Constant SE 0.2642, t 2.30, p 0.024; ROE SE 1.733, t 9.19, p 0. S = 1.309, R² = 52.6%, adj R² = 52.0% |
| Apple | 37 computer services firms with revenues > $100m | PE | PE = −56.2 − 107 × Payout + 62.0 × Value Line Beta + 270 × Growth in EPS. R² = 29.7% |
| Biosite | 51 Medical Supply firms | Value-to-Sales | VS = −1.331 + 16.507 × Growth + 21.26 × Operating Margin − 3.031 × Debt/Capital. Constant SE 1.0785, t −1.235, p 0.223; Growth SE 5.576, t 2.961, p 0.0048; Margin SE 3.906, t 5.445, p 1.95e-06; Debt/Capital SE 2.485, t −1.220, p 0.229. S = 1.7066, R² = 56.2%, adj R² = 53.3% |
| Gundle | 25 environmental-industry firms, negative-earnings firms eliminated | P/BV | P/BV = 1.11 + 7.74 × ROE. R² = 27.2% (one variable only, because the sample is small) |
| Infosys | 50 mostly US computer software/services firms, screened on size and growth | PEG | PEG = 5.035 − 1.6009 × ln(Growth) + 1.2863 × Value Line Beta + 0.517 × Payout. Constant SE 1.223, t 4.12, p 0; ln Growth SE 0.364, t −4.4, p 0; Beta SE 0.5779, t 2.23, p 0.03; Payout SE 1.257, t 0.41, p 0.683. S = 1.095, R² = 31.3%, adj R² = 27.3% |
| Nextel Partners | 53 wireless networking firms, four outliers removed | Value/BV Capital | V/BV Capital = 1.6417 − 0.6444 × ROC − 0.6933 × Market Debt/Capital. Constant SE 0.2248, t 7.3, p 0; ROC SE 0.1809, t −3.56, p 0.001; Debt/Capital SE 0.4983, t −1.39, p 0.17. S = 1.167, R² = 25.2%, adj R² = 22.3% |

Symbols: ROE = return on equity; ROC = return on capital; Payout = dividends/earnings; Growth = expected growth (revenue growth for VS, EPS growth for PE); Operating Margin = operating income/sales; Debt/Capital = debt/(debt+equity); PBV/P/BV = price-to-book; VS = value-to-sales; PEG = PE divided by expected growth.

Prices implied by each approach:

| Firm | Peer-average multiple → price | Regression multiple → price | DCF base | Market price |
|---|---|---|---|---|
| ACS | PBV 2.618 → $47.75 | PBV 3.283 → $59.87 | $48.75 | $50.50 |
| Apple | PE 61.64 → $48.31 | PE 31.45 → $24.53 | $27.06 | $20.85 |
| Biosite | VS 3.314 → $22.64 | VS 3.294 → $22.50 | $32.76 | $26.12 |
| Gundle | P/BV 1.69 → $22.06 | P/BV 2.271 → $29.57 | $41.13 | $19.73 |
| Infosys | PEG 2.22 → Rs 9,043 | PEG 1.303 → Rs 5,307 | Rs 4,270 | Rs 4,912 |
| Nextel | V/BV Capital 1.80 → $11.65 | V/BV Capital 1.36 → $8.82 | $11.08 | $11.72 |

**Worked example:** Affiliated Computer Services. The peer set was 77 firms, primarily US computer software and services companies, screened on size and growth. Both PE and PBV regressions were run; PBV against ROE gave the higher R² at 52.6%, so PBV was chosen. The fitted equation is PBV = 0.608 + 15.926 × ROE, and the ROE coefficient is strongly significant (t = 9.19, p = 0). Plugging in ACS's own ROE gives a predicted PBV of 3.283 and a predicted price of $59.87 — well above the $50.50 market price, implying undervaluation. The simple peer average PBV of 2.618 implies $47.75, implying overvaluation. The two peer-based methods disagree by 25%, which is exactly why the final recommendation weights the DCF more heavily.

**Determinism:** DETERMINISTIC — the regression fit (coefficients, standard errors, t-statistics, p-values, R²), the predicted multiple from the target's fundamentals, the implied price, the peer-average multiple and its implied price. Given the peer sample and the variable list, a script produces all of it. JUDGMENT — the peer criteria, which multiple to adopt, which explanatory variables to include, which observations count as outliers, and whether a prediction is plausible enough to keep.

**Pitfalls:**
- Leaving negative-earnings firms in an earnings-multiple sample. Gundle's set explicitly eliminated them.
- Over-fitting a small sample. With 25 comparables, Gundle's analysis used a single explanatory variable on purpose.
- Reading a low R² as fatal. Apple's PE regression at 29.7% and Nextel's at 25.2% were still used, but they justify weighting the DCF more heavily.
- Ignoring a counter-intuitive coefficient. Nextel's regression has a *negative* ROC coefficient: among loss-making wireless firms, higher ROC associates with lower multiples in-sample. That is a warning about the sample, not a finding about value.
- Treating the peer average and the regression as interchangeable. They disagreed for every single company in this project, sometimes by a factor of two (Apple: $48.31 vs $24.53).
- Choosing peers to produce a desired answer. Ambiguity in comparables selection is the stated reason the project's authors weight DCF above regressions.

**Sources:**
- valuations--projects--eqprojspr19 p.5
- valuations--projects--valproject2 p.3, p.6, p.9, p.12, p.14, p.19

**Related:** [[market-wide-multiple-regression]], [[valuation-triangulation-and-recommendation]], [[dcf-model-selection]], [[equity-valuation-project-blueprint]]

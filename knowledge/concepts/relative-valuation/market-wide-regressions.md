# Market-wide pricing regressions

**Core idea:** Instead of hand-picking a dozen peers, use every firm in the market. Regress the multiple on proxies for risk, growth and payout across the whole cross-section, then plug in your firm's fundamentals to get a predicted multiple. The benchmark is now the entire market rather than a peer group you chose, which removes one source of analyst bias. Three things then need watching: the assumed linearity, the instability of the relationship across years, and the correlation among the predictors. The regression's growth coefficient has a nice reading of its own. It is the market price of an extra percentage point of expected growth, and it swings by a factor of five across years.

**Formulas:**
- Standard US PE specification: `Trailing PE = a + b × Payout + c × Beta + d × Expected EPS growth (next 5 years)`
- Prediction and comparison: predicted PE from the equation, versus the traded PE. Below predicted → cheap relative to the market.
- Unit warning: the SPSS output enters payout and growth as absolute percent (25% → 25). The slide-form equation restates them as decimals (25% → 0.25) with the coefficients scaled by 100. Both appear in the source; check which you are using.

**Procedure:**
1. Pick the dependent multiple and the market universe (US, region, or global).
2. Choose predictors from the multiple's intrinsic derivation: payout, beta, expected growth for PE; add ROE for PBV; use debt ratio, growth and tax rate for EV/EBITDA.
3. Run the regression, weighted by market cap if you want the result to reflect where the money is (the lecture regressions use weighted least squares by market cap).
4. Inspect the t-statistics. Above 2 is very good, 1 to 2 is marginal, below 1 is noise.
5. Drop insignificant variables and re-run, even when theory says the variable should matter. In pricing, the market decides what matters. Explanatory power rarely suffers: dropping the insignificant beta in January 2021 moved R² only from 0.396 to 0.389.
6. Check the intercept. If it is negative, predicted multiples can come out negative, which is nonsense. One imperfect fix is to re-run through the origin (no intercept).
7. Check the correlation matrix. Wrong-sign coefficients usually mean multicollinearity, not a discovery.
8. Plug your firm's payout, beta and growth in, get the predicted multiple, and compare with the traded one.
9. State the benchmark explicitly. Market-wide pricing and peer-group pricing can disagree, since the peer group may itself be mispriced against the market.

**Reference data:**

**US PE regression, January 2021** (all US stocks, WLS weighted by market cap; payout and growth in absolute percent):
`Trailing PE = 4.104 + 0.174 × Payout + 1.714 × Beta + 2.304 × Expected EPS growth`

| Predictor | B | Std. Error | Std. Beta | t | Sig. |
|---|---|---|---|---|---|
| Constant | 4.104 | 2.828 | — | 1.451 | .147 |
| Payout ratio | .174 | .017 | .259 | 10.087 | .000 |
| Beta | 1.714 | 2.709 | .015 | .633 | .527 |
| Expected EPS growth (5 yrs) | 2.304 | .087 | .681 | 26.512 | .000 |

R = .629, R² = .396, adjusted R² = .394.

**After dropping the insignificant beta:**
`Trailing PE = 5.913 + 0.171 × Payout + 2.284 × Expected EPS growth` (R = .623, R² = .389). Constant t = 3.584, payout t = 9.921, growth t = 26.336. In decimal form this is the equation used for firm-level application: `Predicted PE = 5.91 + 17.10 × Payout + 228.40 × Growth`.

Raw explanatory power of growth alone: the scatter of trailing PE against expected EPS growth for US stocks in January 2021 has R² of only 0.072. Growth matters, but one variable is not enough.

**Negative-intercept fix (2019 US data, regression through the origin):**
`Trailing PE = 1.373 × Expected EPS growth + 1.208 × Beta + 0.235 × Payout`

| Predictor | B | Std. Error | t | Sig. |
|---|---|---|---|---|
| Expected EPS growth | 1.373 | .069 | 19.871 | .000 |
| Beta | 1.208 | 1.032 | 1.171 | .242 |
| Payout ratio | .235 | .007 | 32.225 | .000 |

**Multicollinearity evidence (US stocks, January 2021 Pearson correlations):**

| Pair | Correlation | N |
|---|---|---|
| Trailing PE vs Payout | .144 | 2320 |
| Trailing PE vs Expected growth | .270 | 1109 |
| Trailing PE vs Beta | .071 | 2293 |
| Payout vs Expected growth | −.220 | 1138 |
| Payout vs Beta | .080 | 2364 |
| Expected growth vs Beta | −.093 | 1591 |

High-growth firms tend to pay out less and, in some years, carry more risk. The predictors overlap, so coefficients are unstable and can flip sign.

**The market price of growth, January 2000 to January 2021** (growth coefficient from the annual US PE regression, with the implied equity risk premium):

| Date | Price of an extra % of growth | Implied ERP |
|---|---|---|
| Jan-21 | 2.28 | 4.72% |
| Jan-20 | 1.37 | 5.20% |
| Jan-19 | 1.40 | 5.96% |
| Jan-18 | 1.14 | 5.08% |
| Jan-17 | 1.71 | 5.69% |
| Jan-16 | 0.75 | 6.12% |
| Jan-15 | 0.99 | 5.78% |
| Jan-14 | 1.49 | 4.96% |
| Jan-13 | 0.58 | 5.78% |
| Jan-12 | 0.41 | 6.04% |
| Jan-11 | 0.84 | 5.20% |
| Jan-10 | 0.55 | 4.36% |
| Jan-09 | 0.78 | 6.43% |
| Jan-08 | 1.427 | 4.37% |
| Jan-07 | 1.178 | 4.16% |
| Jan-06 | 1.131 | 4.07% |
| Jan-05 | 0.914 | 3.65% |
| Jan-04 | 0.812 | 3.69% |
| Jan-03 | 2.621 | 4.10% |
| Jan-02 | 1.003 | 3.62% |
| Jan-01 | 1.457 | 2.75% |
| Jan-00 | 2.105 | 2.05% |

(For comparison, the January 2020 US regression was `PE = 9.39 − 6.03 × Beta + 20.23 × Payout + 137.19 × Growth`, R² 25.2%, with all three predictors significant. The coefficients differ sharply from 2021 — that instability is the point.)

**Worked example — Disney:** expected growth 15%, dividend payout 20%. Using the January 2021 decimal-form equation:
```
Predicted PE = 5.91 + 17.10(0.20) + 228.40(0.15)
             = 5.91 + 3.42 + 34.26 ≈ 43.6
```
Disney trades at 35 times earnings, below its predicted PE. Against the whole US market, given its growth and payout, Disney looks cheap. Run the same firm through the January 2020 equation (beta 1.25, same growth and payout) and predicted PE is about 26.5 against a traded 25 — roughly fair. Same company, same method, different year, different verdict.

**Determinism:** DETERMINISTIC — estimating the regression from market data; computing predicted multiples from payout, beta and growth; the t-statistic thresholds; the over/under comparison. JUDGMENT — the choice of predictors and universe, whether to weight by market cap, whether to drop the intercept, how much to trust an unstable relationship, and what a gap between predicted and actual means.

**Pitfalls:**
- Assuming linearity. PE is not a linear function of growth, and PEG needs a log transform of growth before it behaves.
- Assuming stability. Coefficients swing hard year to year; the growth coefficient ranged from 0.41 to 2.62 over two decades.
- Multicollinearity. Correlated predictors make individual coefficients unreliable and can produce wrong signs.
- Keeping an insignificant variable "because fundamentals say so". It adds noise to the prediction.
- Overloading a small sample with predictors.
- Negative intercepts producing negative predicted multiples; the through-origin fix is imperfect but usable.
- Treating a market-relative verdict as absolute. If the whole market is overpriced, so is your "cheap" stock ([[pricing-vs-value]]).

**Sources:**
- valpacket2spr21 p.81-90
- valpacket2spr20 p.81-88, p.92

**Related:** [[sector-regressions]], [[cross-market-multiple-regressions]], [[peg-ratio]], [[intrinsic-pe-fundamentals]], [[comparable-selection-and-controls]], [[pricing-vs-value]], [[implied-equity-risk-premium]], [[bottom-up-beta]]

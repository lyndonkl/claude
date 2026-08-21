# Market-wide multiple regression

**Core idea:** Instead of pricing a stock against a hand-picked peer group, use the entire cross-section of firms in a market. Run a multiple regression with the multiple (e.g., trailing PE) as the dependent variable. Use proxies for risk, growth and payout as the independent variables. This controls for fundamental differences statistically rather than by picking "similar" firms. Every firm in the market then informs the predicted multiple for any one firm. The stock is then judged cheap or expensive by comparing its actual multiple to the regression-predicted multiple. The regression's growth coefficient doubles as a measure of what the market is paying for an extra point of growth in that year.

**Formulas:**
- Canonical US PE regression (January 2021, weighted least squares weighted by market cap; payout and growth entered in absolute percent, i.e. 25% entered as 25):
  `Trailing PE = 4.104 + 0.174*(Payout ratio) + 1.714*(Beta) + 2.304*(Expected EPS growth, next 5 yrs)` — R² = 0.396; beta insignificant (t = 0.633).
- Re-run without the insignificant variable (Jan 2021): `Trailing PE = 5.913 + 0.171*(Payout) + 2.284*(Growth)` — R² = 0.389, all coefficients significant. Equivalent decimal form: `PE = 5.91 + 17.10*(Payout) + 228.40*(Growth)` with payout/growth as decimals.
- No-intercept fix (2019 US, when the intercept was negative): `Trailing PE = 1.373*(Growth %) + 1.208*(Beta) + 0.235*(Payout %)`, regression through the origin.
- Symbols: Payout ratio = dividends / net income, most recent year (set to 0 if net income < 0); Beta = regression or bottom-up beta; Growth = consensus expected EPS growth over the next 5 years.

**Procedure:**
1. Assemble the cross-section for the market (all US firms, say) with the multiple and the fundamental proxies (beta for risk, expected 5-yr EPS growth, payout ratio). Run WLS weighted by market cap.
2. Check t-statistics: t > 2 = significant (keep); t between 1 and 2 = marginal; t < 1 = noise. Drop any insignificant variable and re-run — even if theory says it should matter, in pricing the market decides what matters (Jan 2021: dropping beta cut R² only from .396 to .389).
3. If the intercept is negative (risking negative predicted multiples for some firms), re-run the regression through the origin — an imperfect but usable fix.
4. Plug the subject firm's payout, growth (and beta if retained) into the fitted equation to get the predicted PE.
5. Compare actual PE to predicted PE: actual < predicted → cheap relative to the whole market given its fundamentals; actual > predicted → expensive. Note this can disagree with a peer-group comparison, because the peer group itself may be mispriced relative to the market.
6. Read the growth coefficient as the market price of an extra 1% of expected growth and compare it with history (see Reference data) to judge whether growth is being priced richly or cheaply this year.

**Reference data:** Market price of an extra % of EPS growth (US PE regression coefficient, decimal-growth scale) and the implied equity risk premium, each January (through Jan 2021):

| Date | Price of extra % growth | Implied ERP | | Date | Price of extra % growth | Implied ERP |
|---|---|---|---|---|---|---|
| Jan-21 | 2.28 | 4.72% | | Jan-10 | 0.55 | 4.36% |
| Jan-20 | 1.37 | 5.20% | | Jan-09 | 0.78 | 6.43% |
| Jan-19 | 1.40 | 5.96% | | Jan-08 | 1.427 | 4.37% |
| Jan-18 | 1.14 | 5.08% | | Jan-07 | 1.178 | 4.16% |
| Jan-17 | 1.71 | 5.69% | | Jan-06 | 1.131 | 4.07% |
| Jan-16 | 0.75 | 6.12% | | Jan-05 | 0.914 | 3.65% |
| Jan-15 | 0.99 | 5.78% | | Jan-04 | 0.812 | 3.69% |
| Jan-14 | 1.49 | 4.96% | | Jan-03 | 2.621 | 4.10% |
| Jan-13 | 0.58 | 5.78% | | Jan-02 | 1.003 | 3.62% |
| Jan-12 | 0.41 | 6.04% | | Jan-01 | 1.457 | 2.75% |
| Jan-11 | 0.84 | 5.20% | | Jan-00 | 2.105 | 2.05% |

Growth was priced richest in Jan 2000, Jan 2003 and Jan 2021; cheapest in Jan 2010–2013.

**Worked example:** Disney (Jan 2021 regression): expected growth 15%, payout 20%. Predicted PE = 5.91 + 17.10(0.20) + 228.40(0.15) = 5.91 + 3.42 + 34.26 ≈ 43.6. Disney traded at 35× earnings — below the regression prediction, so Disney looked cheap relative to the entire US market given its growth and payout. (The Jan 2020 edition of the same exercise: predicted PE = 9.39 − 6.03(1.25) + 20.23(0.20) + 137.19(0.15) ≈ 26.5 vs. actual 25× — roughly fairly priced.)

**Determinism:**
- DETERMINISTIC: given fitted coefficients and a firm's (payout, beta, growth) → predicted PE; the comparison predicted vs. actual; the t-stat classification (>2 / 1–2 / <1); fitting the regression itself once the sample and spec are fixed.
- JUDGMENT: choice of proxies and functional form; deciding to drop a variable or drop the intercept; interpreting under/overvaluation (relative to market ≠ absolute); reconciling market-regression vs. peer-group verdicts.

**Pitfalls:** (1) The regression assumes linearity between PE and the proxies — may be wrong. (2) The PE–fundamentals relationship is not stable over time (coefficients swing year to year), so predictions from a stale regression are unreliable. (3) Multicollinearity: the independent variables are correlated with each other (Jan 2021 US: growth vs. payout −0.220, growth vs. beta −0.093, payout vs. beta +0.080, all significant). That makes individual coefficients unreliable and can flip their signs. A wrong-sign coefficient is usually a multicollinearity symptom, not a real effect. (4) Don't overload small-sample regressions with variables. (5) A negative intercept can produce nonsensical negative predicted multiples.

**Sources:**
- valpacket2spr21 p.81-90
- valpacket2spr20 p.81-88, p.92

**Related:** [[peg-ratio-regression]], [[cross-market-multiple-regressions]], [[multiples-application-discipline]], [[pe-ratio]], [[implied-equity-risk-premium]], [[comparable-firm-pricing]]

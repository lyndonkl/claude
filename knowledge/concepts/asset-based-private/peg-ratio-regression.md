# PEG ratio regression

**Core idea:** The PEG ratio (PE divided by expected growth) is often treated as growth-neutral — "a lower PEG is cheaper regardless of growth." It is not: across US stocks, PEG falls as expected growth rises, and the relationship is nonlinear. Comparing raw PEGs therefore biases you toward calling high-growth firms cheap. The fix is the same market-wide regression discipline used for PE, but with the natural log of growth as the regressor to handle the nonlinearity; a firm is then judged against its regression-predicted PEG, not against peers' raw PEGs.

**Formulas:**
- Nonlinearity evidence (US): PEG vs. raw growth scatter R² = 0.022 (negative slope); PEG vs. ln(growth) R² = 0.053. Log-transforming growth is the standard fix.
- Canonical US PEG regression (Jan 2021 packet): `PEG = 5.626 + 0.004*(Payout ratio) − 0.660*ln(Growth) − 1.138*(Beta)` — R² = 0.116, all coefficients significant. (Payout in absolute percent; growth as used in lnGrowth.)
- Jan 2020 edition (richer spec): `PEG = 1.036 − 1.515*(Beta) + 1.362*(Payout) + 0.898*(Net Profit Margin) − 1.079*ln(Growth)` — R² = 0.454.
- Symbols: PEG = PE / expected EPS growth; Payout = dividends/net income (0 if NI < 0); Beta = regression or bottom-up beta; Growth = expected EPS growth next 5 years.

**Procedure:**
1. Never compare raw PEG ratios across firms with different growth rates — the measure is biased against low-growth firms (their PEGs are mechanically high).
2. Regress PEG on payout, beta and ln(growth) across the market (WLS by market cap).
3. Plug the subject firm's fundamentals into the fitted equation → predicted PEG.
4. Actual PEG below predicted → cheap for its fundamentals; above → expensive.
5. Expect low explanatory power (R² ≈ 12% in Jan 2021): PEG ratios are far less explainable by fundamentals than PE ratios, so hold conclusions loosely.

**Reference data:** Signs to expect in any market: PEG falls with growth (negative ln(g) coefficient) and with beta; rises mildly with payout. Regional Jan 2021 PEG regressions are in [[cross-market-multiple-regressions]].

**Worked example:** Take a firm with payout 25 (%), beta 1.2, expected growth 20%. Jan 2021 US equation: PEG = 5.626 + 0.004(25) − 0.660·ln(20) − 1.138(1.2) = 5.626 + 0.10 − 1.977 − 1.366 ≈ 2.38. If the firm's actual PEG is 1.5, it is cheap relative to the market after controlling for its risk, payout and growth level.

**Determinism:**
- DETERMINISTIC: (payout, beta, growth) → predicted PEG via the fitted equation; the actual-vs-predicted comparison.
- JUDGMENT: choice of transformation and regressors; interpreting a low-R² prediction; the decision to use PEG at all rather than PE with growth as a regressor.

**Pitfalls:** PEG is not neutral to growth — the very thing it is advertised to control for; the PEG–growth relation is negative and nonlinear, so raw-PEG screens systematically flag high-growth firms as bargains. Fit quality is poor (R² ~0.12 in 2021), so PEG regressions are noisier than PE regressions.

**Sources:**
- valpacket2spr21 p.91-93
- valpacket2spr20 p.89-91

**Related:** [[market-multiple-regression]], [[cross-market-multiple-regressions]], [[pe-ratio]], [[multiples-application-discipline]]

# The Fisher Equation and the Intrinsic Riskfree Rate

**Core idea:** Interest rates come in four flavors: market-determined (set by demand and supply), market-influenced (priced off a market rate), entity-set (a bank or card issuer picks the number), and negotiated (bargaining power decides). Only the market-determined ones obey economics, and the Fisher equation is the core of that economics. A nominal interest rate is the real interest rate plus expected inflation. The real rate compensates investors for deferring consumption, and empirically it tracks real growth in the economy. That gives a powerful practical tool: an *intrinsic* riskfree rate equal to inflation plus real GDP growth. Over 1954-2019 the actual 10-year US Treasury bond rate tracked this intrinsic rate closely. Low rates after 2008 therefore came mostly from low inflation and low real growth, not from central bank fiat alone.

**Formulas:**
- Fisher equation: `Nominal interest rate = Real interest rate + Expected inflation`. `Nominal rate` = the stated market rate; `Real rate` = compensation for deferring consumption; `Expected inflation` = anticipated inflation over the life of the instrument.
- Intrinsic riskfree rate: `Intrinsic riskfree rate = Inflation rate + Real GDP growth rate`, using real GDP growth as the proxy for the real interest rate.
- Smoothed version: `Smoothed intrinsic rate = 10-year average inflation + 10-year average real GDP growth`.
- Fed Effect: `Fed Effect = 10-year T.Bond rate − Intrinsic riskfree rate`. This is the gap between the market rate and what fundamentals imply.
- Market-implied expected inflation: `Expected inflation ≈ Nominal 10-year T.Bond rate − 10-year TIPS rate`. TIPS holders are compensated separately for inflation, so the TIPS rate is a direct market measure of the real rate.

**Procedure:**
1. Decide which rate you actually need. If you need a riskfree rate for valuation, you need a market-determined government bond rate, not a bank's posted rate.
2. Look up the current 10-year government bond rate in the currency of your cash flows.
3. Build the intrinsic riskfree rate as a cross-check. Add expected inflation to expected real GDP growth for that economy.
4. Compare. If the market rate sits far from the intrinsic rate, do not simply assume the market is wrong. Ask which of the two inputs (inflation expectations, real growth expectations) the market disagrees with.
5. Use TIPS where available to decompose the market rate. The TIPS yield is the real rate; the nominal-minus-TIPS spread is the market's expected inflation. In July 2019 that gave roughly 0.15% real and roughly 1.75% expected inflation.
6. Handle central bank effects with restraint. Compute the Fed Effect as the residual. Historically it has stayed mostly within ±5%, was strongly positive (about +8.5%) only in the early 1980s, and has been modestly negative since 2008. Do not build a valuation on the belief that the central bank sets long rates.
7. Watch for negative nominal rates. They are possible and not an error, when deflation combines with very low or negative real growth.

**Reference data:**

Decade averages, US (Damodaran, Foundations of Finance Session 11; data through 2019):

| Decade | T.Bond rate | Inflation | Real GDP growth | Intrinsic riskfree rate |
|---|---|---|---|---|
| 1954-59 | 3.47% | 1.53% | 2.82% | 4.34% |
| 1960-69 | 4.89% | 2.53% | 4.53% | 7.06% |
| 1970-79 | 7.48% | 7.44% | 3.24% | 10.68% |
| 1980-89 | 10.27% | 5.13% | 3.15% | 8.28% |
| 1990-99 | 6.43% | 2.95% | 3.23% | 6.18% |
| 2000-09 | 4.20% | 2.57% | 1.82% | 4.39% |
| 2010-19 | 2.50% | 1.79% | 2.21% | 3.99% |

10-year TIPS rate versus 10-year nominal T.Bond rate, 2003-2019 (approximate, read from Damodaran's chart). The difference is the market's expected inflation:

| Year | 10-yr TIPS (real) | 10-yr T.Bond (nominal) |
|---|---|---|
| 2003 | 2.00% | 4.25% |
| 2004 | 1.65% | 4.20% |
| 2005 | 2.05% | 4.40% |
| 2006 | 2.40% | 4.70% |
| 2007 | 1.70% | 4.00% |
| 2008 | 2.15% | 2.20% |
| 2009 | 1.45% | 3.85% |
| 2010 | 1.00% | 3.30% |
| 2011 | −0.10% | 1.90% |
| 2012 | −0.65% | 1.75% |
| 2013 | 0.80% | 3.05% |
| 2014 | 0.50% | 2.15% |
| 2015 | 0.70% | 2.25% |
| 2016 | 0.50% | 2.45% |
| 2017 | 0.45% | 2.40% |
| 2018 | 1.00% | 2.70% |
| 2019 | 0.15% | 1.90% |

Long-run US Treasury rate landmarks, 1928-2019. Short rates sat near 0% and the 10-year near 2-3% through the 1930s and 1940s. Both peaked near 14% around 1981. The 3-month bill was near 0% from 2008 to 2015. Both were around 1.5-2% in 2019. The 10-year normally sits above the 3-month, and the short rate is far more volatile.

**Worked example:** Take the 2010-19 decade. Average inflation was 1.79% and average real GDP growth was 2.21%, so the intrinsic riskfree rate was `1.79% + 2.21% = 4.00%` (3.99% with unrounded inputs). The actual average 10-year T.Bond rate was 2.50%. The Fed Effect was therefore `2.50% − 3.99% = −1.49%`: market rates ran about 150 basis points below fundamentals over the decade. That is a real but modest gap. Compare it with the 1970s, when the intrinsic rate of 10.68% towered over the actual 7.48% rate, a Fed Effect of −3.20% in a decade of 7.44% inflation.

**Determinism:**
- DETERMINISTIC: `Intrinsic riskfree rate = inflation + real GDP growth`. `Fed Effect = T.Bond rate − intrinsic rate`. `Expected inflation = nominal rate − TIPS rate`. Given any two of the three Fisher terms, the third. All are exact arithmetic on published series.
- JUDGMENT: estimating *expected* inflation and *expected* real growth for a forward-looking intrinsic rate. Also: how much of an observed Fed Effect to attribute to central bank action rather than to mis-estimated expectations, and whether a given government's bond rate is genuinely riskfree. Those judgments need inflation forecasts, GDP forecasts, the sovereign's rating, and knowledge of the central bank's balance-sheet operations.

**Pitfalls:**
- Believing that central banks set interest rates. They set only a few rates directly, and their influence over the rest comes largely from the perception of their power. The Fed Effect residual is usually small.
- Attributing post-2008 low rates entirely to quantitative easing. Low inflation and weak real growth explain most of it. Quantitative easing (central banks buying government bonds, and later backstopping corporate bond and lending markets) matters at the margin. Critics add that this activism rewards risk takers by shielding them from their mistakes and raises the odds of future inflation.
- Using a historical average riskfree rate in a valuation instead of today's market rate. The Fisher decomposition explains rates; it does not license you to normalize them.
- Treating a negative nominal rate as impossible or as a data error.
- Confusing the *real* rate (TIPS) with the *nominal* rate when building a discount rate, which double-counts or omits inflation.

**Sources:**
- `foundations_of_finance--interest_rates p.2-9`

**Related:** [[yield-curve-and-growth-signals]], [[inflation-measurement-and-causes]], [[real-vs-nominal-conversion]], [[currency-consistent-valuation]], [[default-risk-and-default-spreads]], [[time-value-of-money-and-discount-rates]]

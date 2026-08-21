# Pricing whole markets: the country PE regression

**Core idea:** Country PE ratios differ enormously, and the low ones attract the word "cheap". Russia traded near 4 times earnings in March 2014 while Greece was above 20. That gap is not a free lunch. A market's PE is driven by the same fundamentals as a company's: the level of interest rates (the discount rate), real growth in the economy, and risk. Regress country PEs on those three variables, and you get a predicted PE for each market. Compare actual with predicted and you have a fundamentals-adjusted verdict rather than a headline number.

**Formulas:**
- `PE = 16.16 − 7.94 × Interest Rate + 154.40 × Real GDP Growth − 0.1116 × Country Risk`
- Interest rate and real GDP growth enter as decimals. Country Risk is a 0-100 score where higher means riskier. R² = 73%.
- Verdict: actual PE below predicted PE means relatively cheap on fundamentals. Above means relatively expensive.

**Procedure:**
1. Collect, for each market, the PE ratio, a long-term local interest rate, expected real GDP growth, and a country risk score on a consistent scale.
2. Regress PE on the three variables across the set of markets.
3. Check the signs against theory. Higher rates should lower PE, higher real growth should raise it, higher risk should lower it. If a sign is wrong, suspect collinearity or a bad risk measure.
4. Evaluate the fitted equation for each market to get a predicted PE.
5. Rank markets by actual minus predicted, or by the percentage gap.
6. Treat a large negative gap as a candidate, not a conclusion. Ask what the three variables omit: currency risk, governance, accounting quality, the sector mix of the index.
7. Re-estimate whenever rates or risk scores move materially. This regression is a snapshot, not a constant.

**Reference data — 16 emerging markets, June 2000 (the estimation sample and its fitted values):**

| Country | PE Ratio | Interest Rate | Real GDP Growth | Country Risk | Predicted PE |
|---|---|---|---|---|---|
| Argentina | 14 | 18.00% | 2.50% | 45 | 13.57 |
| Brazil | 21 | 14.00% | 4.80% | 35 | 18.55 |
| Chile | 25 | 9.50% | 5.50% | 15 | 22.22 |
| Hong Kong | 20 | 8.00% | 6.00% | 15 | 23.11 |
| India | 17 | 11.48% | 4.20% | 25 | 18.94 |
| Indonesia | 15 | 21.00% | 4.00% | 50 | 15.09 |
| Malaysia | 14 | 5.67% | 3.00% | 40 | 15.87 |
| Mexico | 19 | 11.50% | 5.50% | 30 | 20.39 |
| Pakistan | 14 | 19.00% | 3.00% | 45 | 14.26 |
| Peru | 15 | 18.00% | 4.90% | 50 | 16.71 |
| Philippines | 15 | 17.00% | 3.80% | 45 | 15.65 |
| Singapore | 24 | 6.50% | 5.20% | 5 | 23.11 |
| South Korea | 21 | 10.00% | 4.80% | 25 | 19.98 |
| Thailand | 21 | 12.75% | 5.50% | 25 | 20.85 |
| Turkey | 12 | 25.00% | 2.00% | 35 | 13.35 |
| Venezuela | 20 | 15.00% | 3.50% | 45 | 15.35 |

Reading the table: Hong Kong (20 vs 23.11) and Malaysia (14 vs 15.87) look cheap after controlling for fundamentals. Chile (25 vs 22.22) and Venezuela (20 vs 15.35) look expensive. Note that Venezuela's headline PE of 20 is high while Malaysia's 14 is low, yet the fundamentals reverse the ranking.

Emerging market PE levels, March 2014 (bar-chart data behind the "Russia looks cheap" discussion): Greece highest at roughly 20x (labelled 27x). Philippines about 18, Mexico about 17, India about 14. Most markets sat between 9 and 15. China was about 8.5 and Russia lowest, near 4.

**Worked example:** Venezuela in June 2000. Interest rate 15%, real GDP growth 3.5%, country risk 45.
```
Predicted PE = 16.16 − 7.94(0.15) + 154.40(0.035) − 0.1116(45)
             = 16.16 − 1.19 + 5.40 − 5.02 = 15.35
```
Actual PE was 20. Venezuela traded 30% above its fundamentals-implied PE — expensive, not cheap, despite sitting mid-pack on the raw number.

**Determinism:** DETERMINISTIC — estimating the regression from country data; computing predicted PEs; ranking actual against predicted. JUDGMENT — the choice of risk score and growth forecast, whether three variables suffice, and what a residual means for an investor who must also bear currency and governance risk.

**Pitfalls:**
- Calling a low-PE market cheap. Low PEs usually pair with high interest rates, low growth and high country risk, all of which justify them.
- Comparing country PEs measured on different accounting standards or index compositions.
- Using a risk score on a different scale than the one the regression was fitted on; the coefficient is scale-specific.
- Extrapolating a June 2000 equation to today. Rates and risk premia have shifted enormously; refit before use.
- Ignoring the small sample. Sixteen observations with three predictors is thin, so coefficients are fragile.

**Sources:**
- valpacket2spr21 p.27-30
- valpacket2spr20 p.27-30

**Related:** [[intrinsic-pe-fundamentals]], [[market-pe-vs-bond-alternative]], [[sector-regressions]], [[market-wide-regressions]], [[cross-market-multiple-regressions]], [[multiple-distribution-statistics]], [[country-risk-premium]]

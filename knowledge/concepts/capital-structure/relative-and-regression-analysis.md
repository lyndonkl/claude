# Relative analysis: industry averages and cross-sectional regressions

**Core idea:** The comparables approach says the safest place for a firm is near its peer group's debt ratio, with subjective adjustments for what makes the firm different. The simple version compares the firm to an industry average. The better version runs a cross-sectional regression of debt ratios on the fundamentals that should drive them (tax rate, earnings variability, cash flow return, growth, institutional ownership), then plugs in the firm's own values to get a predicted debt ratio. Actual above predicted means over-levered relative to sector or market practice; actual below means under-levered. The critical caveat: a regression predicts *typical* behavior, not *optimal* behavior, and the fit is often weak.

**Formulas:**
- Sector regression form: `Debt Ratio = a + b×(Tax rate) + c×(Earnings variability) + d×(EBITDA/Firm value)`, with a, b, c, d estimated by OLS across firms in the sector.
- Global auto sector (56 firms): `Debt to capital = 0.09 + 0.63×(Effective Tax Rate) + 1.01×(EBITDA/EV) − 0.93×(Capex/EV)`, R² = 21%.
- US market-wide (2014, all listed US firms): `DFR = 0.27 − 0.24×ETR − 0.10×g − 0.065×INST − 0.338×CVOI + 0.59×(E/V)`, R² = 8%; t-statistics: intercept 15.79, ETR 9.00, g 2.71, INST 3.55, CVOI 3.10, E/V 6.85.
  - `DFR` = Debt / (Debt + market value of equity)
  - `ETR` = effective tax rate over the most recent twelve months
  - `g` = expected growth (revenue growth)
  - `INST` = fraction of shares held by institutions
  - `CVOI` = standard deviation of operating income over the last 10 years ÷ average operating income over the last 10 years
  - `E/V` = EBITDA / (market value of equity + debt − cash)
- Verdict rule: `actual > predicted` → over-levered; `actual < predicted` → under-levered.

**Procedure:**
1. Define the comparable group carefully — same business, similar size, and (for global sectors) a market-cap floor to exclude micro caps.
2. Compute the firm's and the group's debt-to-capital ratios on both book and market bases, and the net-debt versions as well. Peer groups holding net cash produce negative net debt ratios, which changes the reading.
3. Adjust the raw average for firm-specific differences. Higher tax rate → higher debt ratio. Lower insider ownership → higher debt ratio (more discipline from debt). More stable income → higher debt ratio. More intangible assets → lower debt ratio.
4. For a quantitative version, regress debt ratios across the sector on the proxies you believe drive them. Check t-statistics for significance and R² for predictive power.
5. Plug the firm's own values into the fitted equation to get a predicted debt ratio.
6. Compare actual to predicted and state the verdict.
7. Compare that verdict to the intrinsic optimum. Explain the gap; do not average the two.

**Reference data:** Case firms vs. their comparable groups (2013):

| Company | D/C book | D/C market | Net D/C book | Net D/C market | Comparable group | Group D/C book | Group D/C market | Group net D/C book | Group net D/C market |
|---|---|---|---|---|---|---|---|---|---|
| Disney | 22.88% | 11.58% | 17.70% | 8.98% | US Entertainment | 39.03% | 15.44% | 24.92% | 9.93% |
| Vale | 39.02% | 35.48% | 34.90% | 31.38% | Global diversified mining & iron ore (cap > $1b) | 34.43% | 26.03% | 26.01% | 17.90% |
| Tata Motors | 58.51% | 29.28% | 22.44% | 19.25% | Global autos (cap > $1b) | 35.96% | 18.72% | 3.53% | 0.17% |
| Baidu | 32.93% | 5.23% | 20.12% | 2.32% | Global online advertising | 6.37% | 1.83% | −27.13% | −2.76% |

Readings: Disney is under-levered on market values (11.58% vs 15.44%); Vale is over-levered (35.48% vs 26.03%); Tata Motors is over-levered (29.28% vs 18.72%); Baidu is above peers who hold net cash.

**Worked example:** Two regressions applied.
- *Tata Motors, sector regression*: ETR = 0.252, EBITDA/EV = 0.1167, Capex/EV = 0.1949. Predicted debt ratio = 0.09 + 0.63(0.252) + 1.01(0.1167) − 0.93(0.1949) = **18.54%**. Actual is 29.28%, so Tata Motors is over-levered relative to auto-industry fundamentals — consistent with its 20% cost-of-capital optimum.
- *Disney, market-wide regression*: ETR = 31.02%, g = 6.45%, INST = 70.2%, CVOI = 0.0296, E/V = 9.35%. Predicted = 0.27 − 0.24(0.3102) − 0.10(0.0645) − 0.065(0.702) − 0.338(0.0296) + 0.59(0.0935) = **18.86%**. That is far below the 40% cost-of-capital optimum. The gap is informative rather than contradictory: 18.86% is what a typical US firm with Disney's characteristics *does*, while 40% is what maximizes Disney's value.

**Determinism:**
- DETERMINISTIC: ratio computation from financials; the OLS fit given a dataset; plugging firm values into fitted coefficients to get a predicted ratio; the over/under verdict against a threshold.
- JUDGMENT: defining the comparable group; choosing explanatory variables; deciding how much weight to give a regression with an 8% R²; sizing the subjective adjustments to an industry average; deciding whether "typical" is a defensible target at all.

**Pitfalls:**
- Confusing the predicted ratio with an optimal ratio. The market-wide regression explains only 8% of the variation in debt ratios.
- Note the sign flip on the tax rate between the two regressions: positive in the auto-sector fit (+0.63) and negative market-wide (−0.24). A coefficient sign that contradicts theory is a warning about the sample, not a finding.
- Comparing a firm's market debt ratio to a peer group's book ratio.
- Ignoring net debt when peers hold large cash balances.
- Using a sector average built from a group with a handful of dominant firms.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.95-100

**Related:** [[pathways-to-the-optimal-debt-ratio]], [[cost-of-capital-approach]], [[determinants-of-optimal-debt-ratio]], [[debt-equity-tradeoff]], [[moving-to-the-optimal]]

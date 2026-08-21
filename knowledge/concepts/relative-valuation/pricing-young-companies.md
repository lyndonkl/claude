# Pricing young, money-losing companies

**Core idea:** Conventional multiples collapse when a whole sector loses money. Internet stocks in early 2000 all had negative margins, and price-to-sales ratios ranging from near zero to 30, with no relationship between the two. Regressing PS on current margin produced an R² of 0.04. The fix is not to abandon pricing but to change what you price on. Three routes work. Replace current fundamentals with proxies for survival and future growth. Use a forward multiple applied to a future year, then haircut it back properly. Or let the market tell you which operating metric it is actually paying for, and use that. Each route is still relative valuation, and each still says only "cheap versus these peers", who may all be collectively overpriced.

**Formulas:**

Route 1 — survival and growth proxies (internet stocks, early 2000):
`PS = 30.61 − 2.77 × ln(Rev) + 6.42 × Rev Growth + 5.11 × (Cash/Rev)`
- t-statistics: ln(Rev) 0.66, Rev Growth 2.63, Cash/Rev 3.49. R² = 31.8%.
- ln(Rev) = natural log of revenues, a size control. Rev Growth = revenue growth rate as a decimal. Cash/Rev = cash balance divided by revenues, the survival proxy.

Route 2 — forward multiples, discounted back. Apply every haircut in order:
1. Value in year N from the forward multiple.
2. Discount N years at the **risk-adjusted cost of capital**, not the riskfree rate.
3. Subtract expected dilution from new equity issued to finance growth.
4. Multiply by (1 − probability of failure).
5. Adjust for debt and cash to reach equity value.
6. Subtract the value of the option overhang to reach common equity value.

Route 3 — market-implied pricing metric:
- Compute the correlation of market cap and enterprise value with each candidate operating metric across the sector.
- Price on the metric with the highest correlation: `Value = metric × sector multiple per unit of metric` (median or average).

**Procedure:**
1. Confirm the problem. Regress the multiple on the conventional companion variable across the sector. A near-zero R² and an insignificant slope means current fundamentals are uninformative.
2. Ask what actually separates survivors from failures in this sector. Typical answers: revenue scale, revenue growth, cash on hand relative to burn.
3. Build the proxy regression on those variables and check significance. Keep the size control in even if it is insignificant, because it prevents scale from driving the fit.
4. Compute the predicted multiple for your firm and compare with the actual.
5. If forecasts of a future profitable year exist, run route 2 in parallel. Estimate the year-N value, then apply all six steps. Skipping any step overstates today's value, usually by a large factor.
6. If neither route works, run route 3. Build the correlation matrix of value against every available operating metric, pick the winner, and apply the sector's per-unit multiple.
7. Report the result as relative, and say explicitly what would have to be true for the whole sector to be correctly priced.

**Reference data:**

Failure of current fundamentals (internet stocks, early 2000): `PS = 81.36 − 7.54 × Net Margin`, t-statistic on the margin 0.49, R² = 0.04. Almost every firm had margins between −0.9 and −0.1, with PS ratios spread from near 0 to about 30.

Tesla forward-value waterfall (the full haircut sequence, $ millions):

| Step | Value |
|---|---|
| Estimated value in year 10 | 68,271 |
| Discounted 10 years at the riskfree rate of 2.75% | 52,050 |
| Discounted at the risk-adjusted cost of capital of 10.03% instead | 27,750 |
| After dilution from new equity issued to finance growth | 12,814 |
| After a 10% failure risk | 12,174 |
| After adjusting for debt and cash (equity value) | 11,797 |
| After the overhang of 25.06m options (common equity value) | 8,152 |

The year-10 value of 68,271 becomes 8,152 today. Discounting alone leaves 52,050. Dilution, failure risk, debt and options do most of the work.

Social media sector, October 2013 ($ millions except users):

| Company | Market Cap | Enterprise Value | Revenues | EBITDA | Net Income | Users (m) | EV/User | EV/Revenue | EV/EBITDA | PE |
|---|---|---|---|---|---|---|---|---|---|---|
| Facebook | 173,540 | 160,090 | 7,870 | 3,930 | 1,490 | 1,230.0 | $130.15 | 20.34 | 40.74 | 116.47 |
| LinkedIn | 23,530 | 19,980 | 1,530 | 182 | 27 | 277.0 | $72.13 | 13.06 | 109.78 | 871.48 |
| Pandora | 7,320 | 7,150 | 655 | −18 | −29 | 73.4 | $97.41 | 10.92 | NA | NA |
| Groupon | 6,690 | 5,880 | 2,440 | 125 | −95 | 43.0 | $136.74 | 2.41 | 47.04 | NA |
| Netflix | 25,900 | 25,380 | 4,370 | 277 | 112 | 44.0 | $576.82 | 5.81 | 91.62 | 231.25 |
| Yelp | 6,200 | 5,790 | 233 | 2.4 | −10 | 120.0 | $48.25 | 24.85 | 2412.50 | NA |
| OpenTable | 1,720 | 1,500 | 190 | 63 | 33 | 14.0 | $107.14 | 7.89 | 23.81 | 52.12 |
| Zynga | 4,200 | 2,930 | 873 | 74 | −37 | 27.0 | $108.52 | 3.36 | 39.59 | NA |
| Zillow | 3,070 | 2,860 | 197 | −13 | −12.45 | 34.5 | $82.90 | 14.52 | NA | NA |
| Trulia | 1,140 | 1,120 | 144 | −6 | −18 | 54.4 | $20.59 | 7.78 | NA | NA |
| TripAdvisor | 13,510 | 12,860 | 945 | 311 | 205 | 260.0 | $49.46 | 13.61 | 41.35 | 65.90 |
| **Average** | | | | | | | **$130.01** | **11.32** | **350.80** | **267.44** |
| **Median** | | | | | | | **$97.41** | **10.92** | **44.20** | **116.47** |

Correlation matrix across that sector:

| | Market Cap | Enterprise Value | Revenues | EBITDA | Net Income | Users |
|---|---|---|---|---|---|---|
| Market Cap | 1.00 | | | | | |
| Enterprise value | 0.9998 | 1.00 | | | | |
| Revenues | 0.8933 | 0.8966 | 1.00 | | | |
| EBITDA | 0.9709 | 0.9701 | 0.8869 | 1.00 | | |
| Net Income | 0.8978 | 0.8971 | 0.8466 | 0.9716 | 1.00 | |
| Number of users | 0.9812 | 0.9789 | 0.8053 | 0.9354 | 0.8453 | 1.00 |

Users correlate more strongly with market cap (0.9812) and enterprise value (0.9789) than revenues, EBITDA or net income do. In October 2013 the market priced social media on users.

**Worked examples:**

*Amazon, early 2000 (route 1).* ln(Rev) = 7.1039, revenue growth = 1.9946 (about 199%), Cash/Rev = 0.3069.
```
Predicted PS = 30.61 − 2.77(7.1039) + 6.42(1.9946) + 5.11(0.3069) = 30.42
```
Actual PS was 25.63. Amazon was undervalued *relative to other internet stocks* — a group that was itself collectively overpriced. The relative verdict says nothing about the absolute one.

*Twitter at IPO (route 3).* Twitter had 240 million users. Applying the sector EV/User: 240m × $97.41 (median) ≈ $23.4 billion; 240m × $130.01 (average) ≈ $31.2 billion.

**Determinism:** DETERMINISTIC — the proxy regression and its predicted multiple; the correlation matrix and the choice of highest-correlation metric; the per-unit pricing arithmetic; each discounting and adjustment step in the forward-multiple waterfall once its assumption is set. JUDGMENT — which survival proxies to use, the cost of capital, the dilution estimate, the failure probability, whether the market's chosen metric will still matter next year, and the size of the collective-overpricing risk.

**Pitfalls:**
- Regressing price on current fundamentals when the sector is priced on expected ones.
- Discounting a forward value at the riskfree rate. For Tesla that alone overstated value by nearly a factor of two.
- Forgetting dilution. Young firms fund growth by issuing equity, and existing holders bear that.
- Ignoring failure risk and option overhang.
- Applying a per-user or per-subscriber multiple without asking whether the users monetize. Netflix's $576.82 EV/User against Trulia's $20.59 shows how little the metric means across different business models.
- Treating a relative verdict inside a bubble as an absolute buy signal.

**Sources:**
- valpacket2spr21 p.75-80
- valpacket2spr20 p.75-80

**Related:** [[ev-sales-and-brand-value]], [[sector-regressions]], [[comparable-selection-and-controls]], [[pricing-vs-value]], [[multiple-definition-tests]], [[young-company-valuation]], [[failure-probability]], [[employee-options]]

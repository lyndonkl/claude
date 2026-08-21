# Applying the schedule to different firm types

**Core idea:** The cost-of-capital schedule is the same machine for every firm, but four situations demand a modified input. A firm with volatile earnings needs a decision about current versus normalized operating income, and the answer moves the optimum a lot. A young growth firm has small operating income relative to market value, so ratings collapse quickly and the optimum sits near zero. A private firm has no market equity value and an undiversified owner, so you estimate equity from comparables and use total betas. A family-group company may be leaning on the debt capacity of affiliates, which explains an apparently over-levered balance sheet. Recognizing which case you are in matters more than any refinement of the arithmetic.

**Formulas:**
- Normalized operating income: `EBIT_normalized = Average pre-tax operating margin over N years × Current revenues`, or simply the average EBIT over N years.
- Private-firm equity value from comparables: `E = Net Income × Average PE of publicly traded comparables`.
- Private-firm cost of equity uses `Total beta = Market beta / Correlation of the firm with the market` ([[levered-beta-schedule]]).
- Everything else is the standard schedule from [[cost-of-capital-approach]].

**Procedure:**
1. **Volatile earnings (commodity, cyclical).** Compute the pre-tax operating margin for each of the last 3–5 years. If the range is wide, run the schedule twice: once with the last-twelve-month EBIT and once with normalized EBIT. Report both optima and say which you would act on, given where you think you are in the cycle.
2. **Young growth firm.** Check EBITDA/EV. If it is low (single digits), expect ratings to deteriorate within one or two 10% steps and the optimum to land at 0–10%. Do not force a "reasonable" leverage target on it.
3. **Private firm.** Estimate equity value from a comparable-company multiple. Capitalize leases as the only debt if that is all there is. Use total beta at every debt ratio, which raises the cost of equity everywhere and typically lowers the optimum relative to an otherwise identical public firm.
4. **Group/affiliated company.** Compare the standalone optimum with the actual ratio. If the firm looks over-levered, ask whether group affiliates provide implicit support that lenders are pricing.
5. **Emerging-market firm.** Add the country default spread to the cost of debt at every rating and use a country-risk-adjusted ERP. High local riskfree rates compress the optimum even when cash-flow returns look strong.

**Reference data:** Four completed schedules (2013 case analyses).

*Tata Motors* (Indian rupees; actual debt ratio 29%, optimum 20% at WACC 12.41%):

| d | Beta | ke | Rating | kd pre-tax | Tax rate | kd after-tax | WACC | EV (₹m) |
|---|---|---|---|---|---|---|---|---|
| 0% | 0.8601 | 12.76% | Aaa/AAA | 9.22% | 32.45% | 6.23% | 12.76% | 1,286,997 |
| 10% | 0.9247 | 13.22% | Aa2/AA | 9.52% | 32.45% | 6.43% | 12.54% | 1,333,263 |
| **20%** | **1.0054** | **13.80%** | **A3/A-** | **10.12%** | **32.45%** | **6.84%** | **12.41%** | **1,363,774** |
| 30% | 1.1092 | 14.55% | B2/B | 15.32% | 32.45% | 10.35% | 13.29% | 1,185,172 |
| 40% | 1.2475 | 15.54% | Caa/CCC | 17.57% | 32.45% | 11.87% | 14.07% | 1,061,143 |
| 50% | 1.4412 | 16.93% | Ca2/CC | 18.32% | 32.45% | 12.38% | 14.65% | 984,693 |
| 60% | 1.7610 | 19.23% | Ca2/CC | 18.32% | 30.18% | 12.79% | 15.37% | 904,764 |
| 70% | 2.3749 | 23.65% | C2/C | 19.32% | 24.53% | 14.58% | 17.30% | 741,800 |
| 80% | 3.5624 | 32.19% | C2/C | 19.32% | 21.46% | 15.17% | 18.58% | 663,028 |
| 90% | 7.1247 | 57.81% | C2/C | 19.32% | 19.08% | 15.63% | 19.85% | 599,379 |

*Vale* (commodity firm; optimum 30% at WACC 8.62% on last-12-month EBIT):

| d | Beta | ke | Rating | kd pre-tax | kd after-tax | WACC | EV ($m) |
|---|---|---|---|---|---|---|---|
| 0% | 0.8440 | 8.97% | Aaa/AAA | 5.15% | 3.40% | 8.97% | 98,306 |
| 10% | 0.9059 | 9.43% | Aaa/AAA | 5.15% | 3.40% | 8.83% | 100,680 |
| 20% | 0.9833 | 10.00% | Aaa/AAA | 5.15% | 3.40% | 8.68% | 103,171 |
| **30%** | **1.0827** | **10.74%** | **A1/A+** | **5.60%** | **3.70%** | **8.62%** | **104,183** |
| 40% | 1.2154 | 11.71% | A3/A- | 6.05% | 3.99% | 8.63% | 104,152 |
| 50% | 1.4011 | 13.08% | B1/B+ | 10.25% | 6.77% | 9.92% | 85,298 |
| 60% | 1.6796 | 15.14% | B3/B- | 12.00% | 7.92% | 10.81% | 75,951 |
| 70% | 2.1438 | 18.56% | B3/B- | 12.00% | 7.92% | 11.11% | 73,178 |
| 80% | 3.0722 | 25.41% | Ca2/CC | 14.25% | 9.41% | 12.61% | 62,090 |
| 90% | 5.8574 | 45.95% | Ca2/CC | 14.25% | 9.41% | 13.06% | 59,356 |

Vale's operating history (tax rate 34% throughout): revenues $48,469 / 48,058 / 61,123 / 47,343m; EBITDA $19,861 / 17,662 / 34,183 / 26,299m; EBIT $15,487 / 13,346 / 30,206 / 23,033m; pre-tax operating margin 31.95% / 27.77% / 49.42% / 48.65%, averaging 39.45% on average revenues of $51,248m and average EBIT of $20,518m. Substituting the three-year average EBIT raises Vale's optimum from **30% to 50%**.

*Baidu* (young growth firm; optimum 0–10%, min WACC 12.38% at 10%; actual 5.23%):

| d | Beta | ke | Rating | kd pre-tax | Tax rate | kd after-tax | WACC | EV (¥m) |
|---|---|---|---|---|---|---|---|---|
| 0% | 1.3021 | 12.54% | Aaa/AAA | 4.70% | 25.00% | 3.53% | 12.54% | 337,694 |
| **10%** | **1.4106** | **13.29%** | **A3/A-** | **5.60%** | **25.00%** | **4.20%** | **12.38%** | **343,623** |
| 20% | 1.5463 | 14.23% | Ca2/CC | 13.80% | 25.00% | 10.35% | 13.45% | 306,548 |
| 30% | 1.7632 | 15.74% | Caa/CCC | 14.80% | 17.38% | 12.23% | 14.68% | 272,853 |
| 40% | 2.0675 | 17.85% | D2/D | 16.30% | 11.83% | 14.37% | 16.46% | 235,510 |
| 50%–90% | 2.4810 → 12.4049 | 20.72% → 89.59% | D2/D | 16.30% | 9.47% → 5.26% | 14.76% → 15.44% | 17.74% → 22.86% | 214,337 → 157,646 |

*Bookscape* (private firm, total betas, 40% tax rate; optimum 30% at WACC 9.25%; actual 27.81%):

| d | Total beta | ke | Rating | kd pre-tax | Tax rate | kd after-tax | WACC | EV ($000s) |
|---|---|---|---|---|---|---|---|---|
| 0% | 1.3632 | 10.25% | Aaa/AAA | 3.15% | 40.00% | 1.89% | 10.25% | 37,387 |
| 10% | 1.4540 | 10.75% | Aaa/AAA | 3.15% | 40.00% | 1.89% | 9.86% | 39,416 |
| 20% | 1.5676 | 11.37% | A1/A+ | 3.60% | 40.00% | 2.16% | 9.53% | 41,345 |
| **30%** | **1.7137** | **12.18%** | **A3/A-** | **4.05%** | **40.00%** | **2.43%** | **9.25%** | **43,112** |
| 40% | 1.9084 | 13.25% | Caa/CCC | 11.50% | 40.00% | 6.90% | 10.71% | 35,224 |
| 50% | 2.2089 | 14.90% | Ca2/CC | 12.25% | 37.96% | 7.60% | 11.25% | 32,979 |
| 60% | 2.8099 | 18.20% | C2/C | 13.25% | 29.25% | 9.37% | 12.91% | 27,598 |
| 70% | 3.7466 | 23.36% | C2/C | 13.25% | 25.07% | 9.93% | 13.96% | 25,012 |
| 80% | 5.6198 | 33.66% | C2/C | 13.25% | 21.93% | 10.34% | 15.01% | 22,869 |
| 90% | 11.4829 | 65.91% | D2/D | 14.75% | 17.51% | 12.17% | 17.54% | 18,952 |

**Worked example:** Vale's normalization decision. Its last-twelve-month EBIT of $15,487m gives an optimal debt ratio of 30% (WACC 8.62%, EV $104,183m), with 40% nearly tied (8.63%). But the pre-tax operating margin over four years ranged from 27.77% to 49.42%, averaging 39.45%. Re-running the schedule with three-year average EBIT ($20,518m) pushes the optimum to 50%. The 20-point swing comes entirely from the coverage ratio, since a higher EBIT sustains an investment-grade rating at higher leverage. The analyst's call — current or normalized — is the whole answer here, and it should turn on whether commodity prices at the analysis date are above or below mid-cycle.

**Determinism:**
- DETERMINISTIC: each schedule, once EBIT, beta, tax rate, riskfree rate, ERP and capital base are fixed; the normalized EBIT calculation itself; the private-firm equity estimate given a PE multiple and net income.
- JUDGMENT: whether to normalize and over how many years; which comparables set the PE multiple for a private firm; the correlation used for a total beta; whether group support justifies leverage above the standalone optimum; the country risk adjustments in an emerging market.

**Pitfalls:**
- Running a commodity firm's optimum off peak-cycle earnings and recommending a large debt increase at the top of the cycle.
- Forcing a growth firm toward peer leverage. Baidu at 20% debt is already rated CC.
- Using a market beta for a private firm whose owner holds all of his wealth in it.
- Reading Tata Motors' 29% actual against a 20% optimum as pure error, without asking about the group's aggregate debt capacity.
- Mixing units. The Bookscape schedule is in thousands while the equity estimate ($31.5m) is quoted in millions; the ratio 12,136/(12,136+31,500) = 27.81% only works when both are in the same units.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.68-71

**Related:** [[cost-of-capital-approach]], [[levered-beta-schedule]], [[synthetic-rating-and-cost-of-debt]], [[downside-risk-and-rating-constraints]], [[determinants-of-optimal-debt-ratio]], [[financing-life-cycle]], [[total-beta]], [[country-risk-premium]]

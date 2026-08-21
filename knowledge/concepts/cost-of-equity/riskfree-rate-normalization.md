# Low and negative riskfree rates: the normalization debate

**Core idea:** When today's riskfree rate looks abnormally low, analysts are tempted to replace it with a "normalized" historical average. Damodaran's position is that you should not. Use the current market rate, and make every other assumption consistent with it. The reason is that low rates are not an accident of central bank policy. A riskfree rate is intrinsically the sum of expected inflation and expected real growth, and by that decomposition the low rates since 2008 are mostly explained by low inflation and low real growth. Negative rates are the same story pushed further: they signal expected deflation and/or negative expected real growth. If you normalize the riskfree rate upward while leaving growth and inflation assumptions untouched, you build a systematic bias into every valuation you do.

**Formulas:**
- Intrinsic riskfree rate = Expected inflation rate + Expected real GDP growth rate.
- The Fed Effect = Actual ten-year T.Bond rate − Intrinsic riskfree rate. (A measure of how far the central bank has pushed rates away from fundamentals.)
- Consistency requirement: in a stable-growth DCF, the perpetual nominal growth rate must be ≤ the riskfree rate in that currency, because the riskfree rate is itself inflation + real growth for that economy.

**Procedure:**
1. Take the current 10-year government bond rate in your currency as the riskfree rate. Do not swap in a historical average.
2. Decompose it as a sanity check: intrinsic riskfree rate = expected inflation + expected real GDP growth. Compare with the actual rate. A large gap is the "Fed effect"; historically it has been small.
3. Force consistency downstream. A 0.93% US riskfree rate means:
   - your perpetual growth rate cannot exceed roughly 0.93%;
   - your inflation assumptions in revenue and cost growth must be low;
   - your expected return on stocks is the riskfree rate plus the ERP, so it will be low too (5.65% at the start of 2021).
4. If you insist on normalizing, normalize *everything* together — riskfree rate, inflation, real growth, and the equity risk premium — and state that you are valuing a hypothetical future economy, not today's.
5. For a negative riskfree rate (Swiss Franc, Japanese Yen, Euro, and at times the Croatian Kuna and Bulgarian Lev), use it as is. Then check that inflation and growth assumptions in that currency are correspondingly negative or near zero. Do not floor the rate at zero.
6. Cross-check the resulting expected return on stocks (riskfree + ERP) against history. If it is implausible, the error is usually in the ERP or the growth assumptions, not in the observed bond rate.

**Reference data:**

Ten-year US T.Bond rate versus its intrinsic components (period averages, through 2020):

| Period | Ten-year T.Bond rate | Inflation | Real GDP growth | Intrinsic riskfree rate | Fed Effect |
|---|---|---|---|---|---|
| 1954-2020 | 5.65% | 3.50% | 2.92% | 6.42% | −0.78% |
| 1954-1980 | 5.83% | 4.49% | 3.50% | 7.98% | −2.15% |
| 1981-2008 | 6.88% | 3.26% | 3.04% | 6.30% | +0.58% |
| 2010-2020 | 2.25% | 1.76% | 1.74% | 3.50% | −1.03% |

(Spring 2020 edition, 1954-2019: T.Bond 5.72%, inflation 3.53%, real growth 3.01%, intrinsic 6.54%, difference −0.82%; 2010-2019: 2.38% / 1.86% / 1.72% / 3.58% / −1.03%.)

Context for the "too low" argument: the US 10-year T.Bond rate was 0.93% on 1/1/2021 and 1.92% on 1/1/2020, against a 30-year historical average of roughly 5-6%.

**Worked example:** On January 1, 2021 an analyst valuing a US company argues the 0.93% T.Bond rate is "artificially low" and substitutes a normalized 5%. If she leaves her ERP at 4.72% and her perpetual growth rate at 2%, her cost of equity for a beta-1 firm jumps from 5.65% to 9.72% — a 4-percentage-point discount-rate increase with no offsetting change in cash flows. Every company she values now looks overvalued. The internally consistent alternative keeps the riskfree rate at 0.93%, caps perpetual growth at 0.93%, and produces a cost of equity of 5.65% for the same beta-1 firm.

**Determinism:**
- DETERMINISTIC: (expected inflation, expected real GDP growth) → intrinsic riskfree rate; (actual T.Bond rate, intrinsic rate) → Fed effect; (riskfree rate, ERP) → expected return on stocks.
- JUDGMENT: whether to normalize at all (the course says no); the inflation and real-growth forecasts used in the decomposition; how far negative rates can go, and whether there is a bound; whether a currency's negative rate is a durable feature or a temporary distortion.

**Pitfalls:**
- **Selective normalization** — raising the riskfree rate while leaving growth, inflation, and the ERP untouched. This is the single most common error and it biases all values downward.
- Treating low rates as purely a central-bank artifact. The decomposition says otherwise.
- Flooring negative rates at zero "because a rate cannot be negative". Several currencies had negative 10-year rates in 2020 and 2021.
- Letting a perpetual growth rate exceed the riskfree rate after normalizing downward, or leaving a 2-3% terminal growth rate against a 0.93% riskfree rate.
- Assuming the ERP is constant while the riskfree rate moves. Since 2008 the expected return on stocks has been fairly stable while rates fell, which mechanically raised implied ERPs (see [[implied-equity-risk-premium]]).

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.42-44, p.73
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.42-44
- corporate_finance--lecture_slides--cfpacket1spr20 p.107

**Related:** [[riskfree-rate-fundamentals]], [[currency-riskfree-rate]], [[implied-equity-risk-premium]], [[choosing-an-equity-risk-premium]], [[terminal-value]], [[stable-growth-assumptions]]

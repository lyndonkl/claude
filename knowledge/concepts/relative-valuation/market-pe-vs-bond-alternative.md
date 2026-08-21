# Is the market expensive? PE levels against the bond alternative

**Core idea:** A market PE cannot be judged against its own history alone. What you should pay per dollar of earnings depends on what the alternatives yield. Convert the Treasury bond into a PE — one divided by the ten-year rate — and compare. At the start of 2021 every stock PE measure sat above its long-run average, which reads as expensive. The T.Bond PE was 107.53. The ratio of Shiller PE to T.Bond PE was 0.51, less than half its 1970-2020 average of 1.06. On its own history the market was expensive. Against bonds it was cheap. Both statements are true, and the second one is the one that governs an allocation decision.

**Formulas:**
- `T.Bond PE = 1 / T.Bond rate` — the price paid per dollar of Treasury income.
- `Relative measure = Shiller PE / T.Bond PE`. Compare with its own historical average.
- `E/P (earnings yield) = 1 / PE` for the index.
- Earnings-yield regression, 1960-2020: `E/P = 0.0359 + 0.5534 × T.Bond Rate − 0.1559 × (T.Bond Rate − T.Bill Rate)`. t-statistics 6.17, 7.01, −0.79. R² = 44.81%.
- Same regression through 2008: `E/P = 0.0256 + 0.7044 × T.Bond Rate − 0.3289 × (T.Bond Rate − T.Bill Rate)`. t-statistics 4.71, 7.10, 1.46. R² = 50.71%.
- Predicted market PE = 1 / predicted E/P.

Symbols: T.Bond Rate = ten-year Treasury rate; T.Bill Rate = short-term Treasury rate; the difference is the term-structure (expected-growth) proxy. All rates as decimals.

PE variants used for the index:
- PE — index price over current earnings.
- Normalized PE — price over average earnings.
- CAPE — cyclically adjusted PE.
- Shiller PE — CAPE on inflation-adjusted ten-year average earnings.

**Procedure:**
1. Compute the index PE on at least two bases: raw PE and a normalized or Shiller PE. Cyclical earnings make the raw number jumpy.
2. Compare each with its own long-run average. Note the verdict but do not stop there.
3. Compute the T.Bond PE as one over the current ten-year rate.
4. Compute the Shiller PE / T.Bond PE ratio and compare with its historical average (about 1.06 for 1970-2020).
5. If the ratio is below its average, stocks are cheap relative to bonds even when their own PE looks high.
6. As a cross-check, run or apply the E/P regression on the T.Bond rate and the term-structure spread to get a predicted earnings yield, then invert it for a predicted market PE.
7. Treat the regression cautiously in the post-2008 era. The fit fell from 50.71% to 44.81% and the term-structure variable lost significance once rates were managed near zero.

**Reference data — S&P 500 PE variants by period (start-of-year values, averaged):**

| Period | PE | Normalized PE | CAPE | Shiller PE | T.Bond PE | Shiller PE / T.Bond PE |
|---|---|---|---|---|---|---|
| 1970-2020 | 16.61 | 21.40 | 18.71 | 20.36 | 23.43 | 1.06 |
| 1990-2020 | 19.51 | 25.33 | 23.04 | 25.79 | 30.84 | 1.09 |
| 2001-2010 | 18.98 | 23.54 | 21.72 | 24.88 | 38.81 | 0.77 |
| 2011-2020 | 18.95 | 24.48 | 23.03 | 25.25 | 51.23 | 0.54 |
| Start of 2021 | 27.19 | 31.39 | 29.36 | 29.36 | 107.53 | 0.51 |

Prior-edition comparison (start of 2020): PE 19.90, Normalized PE 28.28, CAPE 26.53, Shiller PE 26.53, T.Bond PE 52.08, ratio 0.51.

Correlations behind the regression, 1960-2020: E/P versus T.Bond rate 0.6788; E/P versus bond-bill spread −0.1184; T.Bond rate versus bond-bill spread −0.0630.

Long-run pattern: the S&P 500 earnings yield tracks the ten-year Treasury rate closely across six decades. Both peaked in the 12-14% range around 1980 and fell together. The Shiller PE / T.Bond PE ratio spiked near 2.8 around 2000 and fell to roughly 0.25-0.5 by 2020.

**Worked example:** Start of 2021. Shiller PE 29.36, ten-year Treasury rate about 0.93%, so T.Bond PE = 1/0.0093 = 107.53. Ratio = 29.36/107.53 = 0.27 on those exact numbers, and 0.51 on the averaged series in the table. Either way it sits far below the 1.06 long-run average. Now the regression cross-check. Take a T.Bond rate of 0.93% and a bond-bill spread of about 0.85%. Predicted E/P = 0.0359 + 0.5534(0.0093) − 0.1559(0.0085) = 0.0397. That implies a market PE of about 25. The actual PE of 27.19 is close to that. Stocks were roughly in line with what rates justified.

**Determinism:** DETERMINISTIC — the T.Bond PE, the Shiller-to-bond ratio, the earnings-yield regression, and the predicted market PE from current rates. JUDGMENT — which earnings measure to normalize on, whether the historical relationship still holds after the post-2008 regime change, and whether "cheap relative to bonds" is an argument for owning stocks when both may be expensive together.

**Pitfalls:**
- Declaring the market expensive from a PE above its historical average, without looking at rates.
- Using raw PE on cyclical or crisis earnings; normalized or Shiller measures are steadier.
- Assuming the E/P-to-rates link is stable. The relationship weakened materially after 2008.
- Forgetting that the relative-cheapness argument compares two possibly overpriced assets. Cheap versus bonds is still a relative statement ([[pricing-vs-value]]).

**Sources:**
- valpacket2spr21 p.31-34
- valpacket2spr20 p.31-34

**Related:** [[intrinsic-pe-fundamentals]], [[country-pe-regression]], [[multiple-distribution-statistics]], [[pricing-vs-value]], [[market-wide-regressions]], [[implied-equity-risk-premium]], [[riskfree-rate]]

# The Yield Curve and What It Signals About Growth

**Core idea:** The yield curve plots market interest rates on bonds from one issuer against their maturities. Its slope is either upward (long rates above short rates), flat, or inverted (long rates below short rates). Every treasury rate on the curve decomposes into expected inflation plus an expected real interest rate. If inflation expectations are similar across horizons, investors demand a maturity premium for lending longer, which tilts the curve upward — the usual shape for most of the last century. Inversions are famous because every US recession since 1955 was preceded by the term spread falling to or below zero. But the folklore overstates the case. When you measure the *continuous* relationship between the slope and subsequent real GDP growth rather than the binary inverted/not-inverted flag, the correlations are weak and sometimes carry the wrong sign.

**Formulas:**
- Rate decomposition: `Interest rate at maturity m = Expected inflation over m + Expected real interest rate over m`.
- Term spread (slope): `Slope = Long rate − Short rate`. Common pairs are 10yr−3mo, 10yr−2yr, 5yr−2yr, 2yr−1yr, 1yr−3mo.
- Slope classification: `Slope > 0` → upward sloping; `Slope ≈ 0` → flat; `Slope < 0` → inverted.
- Correlation test: `corr(Slope_t, Real GDP growth_{t+1})` over a chosen sample, computed for each slope pair and each forward horizon.

**Procedure:**
1. Pull the full set of yields for one issuer across maturities on one date. Use a single issuer; mixing issuers mixes in default spreads.
2. Plot rate against maturity and classify the overall slope by comparing the long end with the short end.
3. Scan for local inversions, not just the overall shape. A curve that rises from end to end can still invert in the middle, and that is what triggers headlines.
4. Compute the specific spread pairs you care about, and state which pair you used. Different pairs give different answers, sometimes opposite ones.
5. Interpret with the Fisher decomposition. A flattening curve means either lower expected inflation at the long end, or a lower expected real rate at the long end, or a higher short rate. Decide which before drawing an economic conclusion.
6. Check the monetary policy overlay. Every inversion episode has coincided with rising Fed Funds rates. A more positive slope goes with easier policy, so the slope partly measures policy stance rather than an independent forecast.
7. Resist the binary. If you are going to use the curve as a growth signal, run the continuous correlation between slope and later growth over your sample rather than counting inversions. Then report the correlation, not a yes/no recession call.

**Reference data:**

US Treasury yield curves at the start of each year, 2009-2018 (Damodaran, Foundations of Finance Session 11):

| Date | 1 Mo | 3 Mo | 6 Mo | 1 Yr | 2 Yr | 3 Yr | 5 Yr | 7 Yr | 10 Yr | 20 Yr | 30 Yr |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1/2/09 | 0.04% | 0.08% | 0.28% | 0.40% | 0.88% | 1.14% | 1.72% | 2.07% | 2.46% | 3.22% | 2.83% |
| 1/4/10 | 0.05% | 0.08% | 0.18% | 0.45% | 1.09% | 1.66% | 2.65% | 3.36% | 3.85% | 4.60% | 4.65% |
| 1/3/11 | 0.11% | 0.15% | 0.19% | 0.29% | 0.61% | 1.03% | 2.02% | 2.74% | 3.36% | 4.18% | 4.39% |
| 1/3/12 | 0.01% | 0.02% | 0.06% | 0.12% | 0.27% | 0.40% | 0.89% | 1.41% | 1.97% | 2.67% | 2.98% |
| 1/2/13 | 0.07% | 0.08% | 0.12% | 0.15% | 0.27% | 0.37% | 0.76% | 1.25% | 1.86% | 2.63% | 3.04% |
| 1/2/14 | 0.01% | 0.07% | 0.09% | 0.13% | 0.39% | 0.76% | 1.72% | 2.41% | 3.00% | 3.68% | 3.92% |
| 1/2/15 | 0.02% | 0.02% | 0.11% | 0.25% | 0.66% | 1.07% | 1.61% | 1.92% | 2.12% | 2.41% | 2.69% |
| 1/4/16 | 0.17% | 0.22% | 0.49% | 0.61% | 1.02% | 1.31% | 1.73% | 2.06% | 2.24% | 2.64% | 2.98% |
| 1/3/17 | 0.52% | 0.53% | 0.65% | 0.89% | 1.22% | 1.50% | 1.94% | 2.26% | 2.45% | 2.78% | 3.04% |
| 1/2/18 | 1.29% | 1.44% | 1.61% | 1.83% | 1.92% | 2.01% | 2.25% | 2.38% | 2.46% | 2.64% | 2.81% |

The curve was steeply upward sloping coming out of the 2008 crisis, with near-zero short rates against 3-4.6% long rates in 2010-11. It flattened sharply as short rates rose after 2015. By January 2018 it ran from 1.29% at 1 month to only 2.81% at 30 years.

US Treasury curve on December 4, 2018, the "inversion blip":

| Maturity | 1 Mo | 3 Mo | 6 Mo | 1 Yr | 2 Yr | 3 Yr | 5 Yr | 7 Yr | 10 Yr | 20 Yr | 30 Yr |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Yield | 2.37% | 2.42% | 2.58% | 2.71% | 2.80% | 2.81% | 2.79% | 2.84% | 2.91% | 3.05% | 3.16% |

Correlations between yield curve slope measures and subsequent real GDP growth:

| 1962 through 2018 | 1 yr vs 3 mth | 2 yr vs 1 yr | 5 yr vs 2 yr | 10 yr vs 2 yr | 10 yr vs 3 mth |
|---|---|---|---|---|---|
| Real GDP growth, next quarter | 0.0821 | 0.0884 | −0.1176 | −0.1554 | −0.1884 |
| Real GDP growth, next year | 0.1577 | 0.2897 | 0.0432 | −0.0147 | −0.0839 |

| 2008 through 2018 | 1 yr vs 3 mth | 2 yr vs 1 yr | 5 yr vs 2 yr | 10 yr vs 2 yr | 10 yr vs 3 mth |
|---|---|---|---|---|---|
| Real GDP growth, next quarter | −0.4939 | −0.1228 | −0.0974 | −0.1044 | −0.0891 |
| Real GDP growth, next year | −0.5332 | 0.0112 | 0.0314 | −0.0074 | −0.0512 |

A positive correlation supports the base hypothesis that flatter or inverted curves precede weaker growth. Over 1962-2018 every correlation is below 0.29 in absolute value, so the relationship is weak. Short-end slopes correlate positively with future growth while long-end slopes correlate negatively — the two ends disagree. Over 2008-2018 the 1yr-vs-3mo slope correlates strongly *negatively* (−0.49 to −0.53), the opposite of the folklore.

For context on the raw spread series: the US term spread ranged roughly from −3% around 1980 to +3.5%, and had fallen to about +0.75% by 2018. Every NBER-dated recession in 1955-2018 was preceded by the spread touching zero or below.

**Worked example:** On December 4, 2018 the curve rose overall, from 2.37% at 1 month to 3.16% at 30 years. But the 5-year yield of 2.79% sat *below* both the 3-year (2.81%) and the 2-year (2.80%). The 5yr-minus-2yr spread was −1 basis point. That local inversion set off recession warnings even though the 10yr-minus-3mo spread was still comfortably positive at `2.91% − 2.42% = +0.49%`. The example shows why you must name the pair: on the same day, one spread was inverted and another said easy conditions.

**Determinism:**
- DETERMINISTIC: computing any spread from a set of yields; classifying the slope; detecting local inversions; computing correlations between slope series and subsequent GDP growth. Inputs `{yield by maturity}` → slope, classification, inversion flags. Inputs `{slope series, GDP growth series}` → correlation matrix.
- JUDGMENT: what an observed slope implies about future growth or recession probability; which spread pair is the right signal; whether the current episode resembles past ones; how much of the slope reflects monetary policy rather than growth expectations. That judgment needs the policy rate path, inflation expectations by horizon, and the state of the credit cycle.

**Pitfalls:**
- Treating inversion as a foolproof recession predictor. Both the slope and growth are continuous variables, and the continuous evidence is weak.
- Cherry-picking the spread pair after seeing the answer. Different pairs disagree, and in 2008-2018 the short-end pair had the wrong sign entirely.
- Reading a local inversion in the belly of the curve as a full inversion.
- Ignoring that inversions coincide with Fed tightening, which makes the slope partly a policy-stance measure rather than an independent forecast.
- Building yield curves across issuers with different credit quality, which contaminates the slope with default spreads.

**Sources:**
- `foundations_of_finance--interest_rates p.10-18`

**Related:** [[fisher-equation-and-intrinsic-riskfree-rate]], [[bond-valuation-and-yield-to-maturity]], [[interest-rate-risk-and-bond-propositions]], [[inflation-measurement-and-causes]], [[default-risk-and-default-spreads]]

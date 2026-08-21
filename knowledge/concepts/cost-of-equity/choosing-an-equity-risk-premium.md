# Choosing which equity risk premium to use

**Core idea:** Historical and implied premiums can differ by several percentage points, and the one you pick applies to every company you value. So the choice is a systematic bias, not a rounding decision. The right premium follows from what you believe about markets. If you think premiums revert to historical norms, use the historical premium. If you think the market is right in aggregate — or you want a market-neutral valuation — use today's implied premium. If you think the market errs in aggregate but is right over time, use the average implied premium over a long window. The empirical evidence favors implied premiums: the current implied premium is positively correlated with future returns, while the historical premium is *negatively* correlated with them.

**Formulas:**
- Directional bias rule: if the ERP you use > the implied ERP, your discount rates are too high, your values too low, and stocks look overvalued. If your ERP < the implied ERP, values are too high and stocks look cheap.
- Cross-market sanity check: ERP / (Baa corporate bond rate − T.Bond rate). Median = 2.02 over 1960-2020 (1.96 through 2019). Large deviations from ~2 signal that equity and credit markets are pricing risk inconsistently.
- Expected return on stocks = T.Bond rate + ERP. Use this as a plausibility test on the pair.

**Procedure:**
1. State your market assumption explicitly, then read the premium off the decision table below.
2. Compute the current implied premium anyway, even if you plan to use a historical one — it is the benchmark against which your choice creates bias.
3. Compare. If your chosen premium sits far above the implied premium, expect most of the companies you value to come out "overvalued", and be able to defend why.
4. Run the credit cross-check: divide your ERP by the current Baa default spread and compare to the historical median of ~2.
5. Run the level cross-check: add the riskfree rate to your ERP and ask whether the resulting expected return on stocks is plausible.
6. Be consistent across the whole valuation and across companies. Do not use an implied premium for one firm and a historical one for its comparable.
7. For non-US markets, the same logic applies, but the mature-market premium is the base and country risk is added on top — see [[country-risk-premium]].

**Reference data:**

Decision rule:

| If you assume this about markets | Premium to use |
|---|---|
| Premiums revert to historical norms, and your period will yield those norms | Historical risk premium |
| Market is correct in the aggregate, or your valuation should be market neutral | Current implied equity risk premium |
| Market makes mistakes even in aggregate, but is correct over time | Average implied equity risk premium over time |

Predictive power of ERP measures (US data):

| Predictor | Corr. with implied premium next year | Corr. with actual return next 5 years | Corr. with actual return next 10 years |
|---|---|---|---|
| Current implied premium | 0.763 | 0.427 | 0.500 |
| Average implied premium, last 5 years | 0.718 | 0.326 | 0.450 |
| Historical premium | −0.497 | −0.437 | −0.454 |
| Default-spread-based premium | 0.047 | 0.143 | 0.160 |

Candidate premiums as of January 1, 2021, all for the same US market:

| Measure | Value |
|---|---|
| Implied ERP (current) | 4.72% |
| Average implied ERP 1960-2020 | 4.21% |
| Average implied ERP 2001-2020 | 4.95% |
| Average implied ERP 2011-2020 | 5.53% |
| Historical geometric, stocks − T.Bonds, 1928-2020 | 4.84% |
| Historical arithmetic, stocks − T.Bonds, 1928-2020 | 6.43% |
| Historical arithmetic, stocks − T.Bills, 1928-2020 | 8.28% |

Cross-asset context: since about 1998 the implied ERP, the Baa corporate default spread, and the real-estate risk premium implied by cap rates have moved together. In the 1980s the real-estate premium was strongly negative (roughly −5% to −6%), meaning property was priced as if safer than bonds and stocks. Convergence since then is evidence that US stock, bond, and real-estate markets became integrated — which is also why the 2008 crisis hit all three at once.

**Worked example:** In January 2021 the implied premium is 4.72%. An investment bank uses the 1928-2020 arithmetic stocks-over-T.Bills premium of 8.28%. For a beta-1 US company the bank's cost of equity is 0.93% + 8.28% = 9.21%, against a market-neutral 5.65%. That extra 3.56 percentage points of discount rate drives values sharply down, so the bank's analysts conclude that most stocks are overvalued — an artifact of the premium choice, not a market insight. Had they used the 1928-2020 geometric stocks-over-T.Bonds premium of 4.84%, they would have been within 12 basis points of the implied premium and essentially unbiased.

**Determinism:**
- DETERMINISTIC: computing every candidate premium; computing the ERP/Baa-spread ratio; computing the expected return on stocks; computing the direction and size of the valuation bias from the gap between your premium and the implied premium.
- JUDGMENT: which market assumption you hold; whether to use the point-in-time implied premium or a multi-year average of it; how much weight the predictive-correlation evidence deserves; whether an unusual ERP/Baa ratio signals mispricing or a regime change.

**Pitfalls:**
- Defaulting to a large arithmetic historical premium because it is conventional. It builds a permanent downward bias into every valuation.
- Switching premium sources between companies or between the valuation and its comparables.
- Using a stale premium. Premiums moved from 4.83% to 7.75% and back within 2020.
- Assuming a higher ERP is "conservative". It is conservative for a buyer and aggressive for a seller; it is not neutral.
- Reading the negative historical-premium correlations as noise. They are consistent across 5- and 10-year horizons.
- Using the implied premium while claiming to disagree with market pricing. The implied premium *is* the market's price of risk; using it means you are taking market pricing as given in aggregate.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.72-77
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.70, p.72-75
- corporate_finance--lecture_slides--cfpacket1spr20 p.128

**Related:** [[implied-equity-risk-premium]], [[historical-equity-risk-premium]], [[equity-risk-premium-basics]], [[country-risk-premium]], [[riskfree-rate-normalization]], [[cost-of-equity-assembly]]

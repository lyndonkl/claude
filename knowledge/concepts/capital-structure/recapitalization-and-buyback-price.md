# Valuing a move to the optimal: firm value, per-share value and the buyback price

**Core idea:** Finding the optimal debt ratio is only half the job. You then have to say what the move is worth, and who captures it. Two methods value the firm-level gain. The full-valuation route backs the growth rate implied by today's price out of the current cost of capital, then revalues the firm at the new, lower cost of capital. The incremental route capitalizes only the annual financing-cost saving. Once you have the gain, the per-share answer depends on the price at which stock is bought back. There is exactly one "rational" buyback price: the one at which the post-buyback value per share equals the buyback price itself, leaving sellers and holders indifferent. Buy back below it and value transfers from sellers to remaining holders.

**Formulas:**
- `Excess debt capacity = Optimal debt ratio × Total capital − Current debt`.
- `FCFF = EBIT(1 − t) + Depreciation − Capex − Δ Non-cash working capital`.
- Implied growth from the current price: `g = (EV × WACC_current − FCFF) / (EV + FCFF)`.
- Full revaluation: `New firm value = FCFF × (1 + g) / (WACC_new − g)`; `Value gain = New value − Current EV`.
- Incremental method: `Annual savings = EV × (WACC_old − WACC_new)`; `Increase in value = Annual savings / (WACC_new − g)`, with g taken as the riskfree rate; `EV after recap = Current EV + Increase in value`.
- Rational (indifference) per-share gain: `Δ per share = Value gain / Shares outstanding`; `Rational price = Current price + Δ per share`.
- General buyback arithmetic at any price P: `Shares after = Shares before − (Increase in debt / P)`; `Equity value after = Optimal EV + Cash − Debt at optimal`; `Value per remaining share = Equity value after / Shares after`.

**Procedure:**
1. Compute the optimal dollar debt and the excess (or excess-of-optimal) debt capacity.
2. Compute the firm-level value gain by at least one of the two methods. The incremental method is more conservative; the full valuation method is more sensitive to the implied growth rate.
3. Decide the use of proceeds. A buyback and a project-funding plan give the same optimal ratio as long as the business mix and tax rate are unchanged ([[downside-risk-and-rating-constraints]]).
4. If buying back stock, compute the rational price = current price + gain per share. Announce and expect the price to move toward it.
5. If the buyback happens at some other price P, run the general arithmetic in step 5 of the formulas to see who gains.
6. Verify the fixed point: buying back at the rational price must return a post-buyback value per share equal to that price. If it does not, your inputs are inconsistent.
7. Present the recommendation with answers to three questions management always asks: why should we do it, what if something goes wrong, and what if we do not want to buy back stock?

**Reference data:** None beyond the firm's own inputs. The capstru.xlsx `Repurchase price Worksheet` implements the general buyback arithmetic directly: current price, shares before, chosen buyback price, current debt, debt at optimal, new debt issued, shares bought back, shares after, enterprise value after, equity value after (EV + cash − debt), and value per remaining share.

**Worked example:** Disney, 2013 (current price $67.71, 1,800m shares, equity $121,878m, debt $15,961m, cash $3,931m, EV = $133,908m, WACC 7.81% → 7.16% at the 40% optimum).
- *FCFF*: 10,032 × (1 − 0.361) + 2,485 − 5,239 − 0 = $3,657m.
- *Implied growth*: (133,908 × 0.0781 − 3,657) / (133,908 + 3,657) = 4.94%.
- *Full revaluation*: 3,657 × 1.0494 / (0.0716 − 0.0494) = $172,935m, a gain of $39,027m.
- *Incremental*: annual savings = 133,908 × (0.0781 − 0.0716) = 10,458 − 9,592 = $866m; capitalized at (7.16% − 2.75%) → $19,623m; post-recap EV = 133,908 + 19,623 = $153,531m.
- *Rational price*: 19,623 / 1,800 = $10.90 per share → $67.71 + $10.90 = $78.61.
- *Buyback at the old price $67.71*: new debt = 55,136 − 15,961 = $39,175m; shares repurchased = 39,175/67.71 = 578.57m, leaving 1,221.43m; equity after = 153,531 + 3,931 − 55,136 = $102,326m; value per remaining share = 102,326 / 1,221.43 = **$83.78**. Remaining holders gain at the expense of sellers.
- *Buyback at $78.61 (the proof)*: shares after = 1,800 − 39,175/78.61 = 1,301.65m; equity after = $102,326m; value per share = 102,326 / 1,301.65 = **$78.61**. The price reproduces itself, confirming it is the indifference point.

**Determinism:**
- DETERMINISTIC: EBIT, tax rate, depreciation, capex, working capital change, current EV, old and new WACC, riskfree rate, share count and buyback price → FCFF, implied growth, value gain, rational price, and post-buyback value per share. The fixed-point check is arithmetic.
- JUDGMENT: whether the implied growth rate is credible (it is backed out of the market price and can be absurd), which valuation method to trust, what growth rate to use in the incremental method, and whether the value gain really accrues entirely to today's shareholders.

**Pitfalls:**
- Using the full-valuation gain and the incremental gain interchangeably. For Disney they differ by a factor of two ($39.0B vs $19.6B), because the implied growth rate of 4.94% is far above the 2.75% riskfree rate used in the incremental method.
- Assuming the buyback price is the pre-announcement price. If the market believes the recapitalization creates value, the price moves first.
- Forgetting cash when converting enterprise value to equity value.
- Recommending a $39 billion borrowing without a downside analysis ([[downside-risk-and-rating-constraints]]).
- Assuming the optimal ratio changes if the proceeds fund projects instead of buybacks. It does not, as long as the projects are in the same businesses and the tax rate is unchanged.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.55-61
- corpfin-capital-structure — capstru.xlsx, sheets `Optimal Capital Structure` (J16-J17, E20-E22, F21-F22) and `Repurchase price Worksheet`

**Related:** [[cost-of-capital-approach]], [[downside-risk-and-rating-constraints]], [[moving-to-the-optimal]], [[fcff]], [[implied-growth-rate]]

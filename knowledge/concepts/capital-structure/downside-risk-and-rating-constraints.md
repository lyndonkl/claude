# Downside risk, safety buffers and rating constraints

**Core idea:** The optimal debt ratio is computed from one number — operating income — held fixed. Real operating income moves. Two protections exist. You can stress-test: recompute the optimum with EBIT knocked down by successive amounts, or under explicit macro scenarios, and see how far the answer holds. Or you can constrain: require a minimum bond rating (or cap the book debt ratio) at the optimum. Both work, but they protect against the same risk, so use one, not both. Every constraint has a price, measured as the firm value given up relative to the unconstrained optimum, and management should be told what that price is.

**Formulas:**
- `Safety buffer test`: for each haircut h, set `EBIT_h = EBIT × (1 − h)` and re-run the full schedule; record the optimal debt ratio at each h.
- `Standard deviation of % change in EBIT` — the natural scale for choosing haircuts, computed from the firm's own operating income history.
- `Cost of a rating constraint = Firm value at the unconstrained optimum − Firm value at the highest debt ratio consistent with the required rating`.

**Procedure:**
1. Identify the key driver. In this framework it is operating income; tax rates and macro variables matter less.
2. Build the firm's EBIT history and compute the standard deviation of annual percentage changes, plus the actual declines in past recessions and the worst single year.
3. **Sensitivity route:** re-run the optimal-capital-structure schedule with EBIT cut by 10%, 20%, … 60%. Report the debt ratio at which the optimum first shifts down. That is the safety buffer.
4. **Scenario route:** for a cyclical firm, define distinct macro scenarios (boom, normal, recession), set EBIT for each, and compute an optimum per scenario.
5. **Constraint route:** ask management for the minimum acceptable rating. Find the highest debt ratio whose synthetic rating meets it, and price the constraint as forgone firm value.
6. Choose one protection. A rating constraint already protects against downside operating income, so do not additionally haircut EBIT.
7. Separate the reasons for a rating constraint before accepting it: protection against downside risk in operating income, a genuine feedback effect (a ratings drop that itself hurts operating income — which is better handled by [[enhanced-cost-of-capital-approach]]), and the ego factor in high ratings.
8. Confirm that the use of proceeds does not change the answer. The optimal ratio is a function of business risk and the tax rate. It stays the same whether the debt funds buybacks or projects, as long as the projects are in the same business mix and the tax rate is unchanged. Recompute only if the firm moves into entirely different businesses or faces a materially different tax rate.

**Reference data:** Disney's EBIT history 1987–2013 ($ millions) and year-over-year changes:

| Year | EBIT | % chg | Year | EBIT | % chg |
|---|---|---|---|---|---|
| 1987 | 756 | — | 2001 | 2,832 | 12.16% |
| 1988 | 848 | 12.17% | 2002 | 2,384 | −15.82% |
| 1989 | 1,177 | 38.80% | 2003 | 2,713 | 13.80% |
| 1990 | 1,368 | 16.23% | 2004 | 4,048 | 49.21% |
| 1991 | 1,124 | −17.84% | 2005 | 4,107 | 1.46% |
| 1992 | 1,287 | 14.50% | 2006 | 5,355 | 30.39% |
| 1993 | 1,560 | 21.21% | 2007 | 6,829 | 27.53% |
| 1994 | 1,804 | 15.64% | 2008 | 7,404 | 8.42% |
| 1995 | 2,262 | 25.39% | 2009 | 5,697 | −23.06% |
| 1996 | 3,024 | 33.69% | 2010 | 6,726 | 18.06% |
| 1997 | 3,945 | 30.46% | 2011 | 7,781 | 15.69% |
| 1998 | 3,843 | −2.59% | 2012 | 8,863 | 13.91% |
| 1999 | 3,580 | −6.84% | 2013 | 9,450 | 6.62% |
| 2000 | 2,525 | −29.47% | | | |

Standard deviation of % change in EBIT = 19.17%. Recession declines: 2009 −23.06%, 2002 −15.82%, 1991 −22.00%, 1981-82 +12% (it rose); worst single year −29.47% (2000).

Disney's safety buffer (optimum re-computed at each EBIT haircut):

| EBIT drops by | EBIT | Optimal debt ratio |
|---|---|---|
| 0% | $10,032m | 40% |
| 10% | $9,029m | 40% |
| 20% | $8,025m | 40% |
| 30% | $7,022m | 40% |
| 40% | $6,019m | 30% |
| 50% | $5,016m | 30% |
| 60% | $4,013m | 20% |

**Worked example:** Disney's rating constraint. At the unconstrained 40% optimum the synthetic rating is A, and firm value is $153,531m. Requiring AA moves the optimum to 30%, where value is $147,835m, so the constraint costs 153,531 − 147,835 = **$5,696m**. Requiring AAA moves it to 20%, value $141,406m, a cost of **$12,125m**. The AA constraint is cheap; the AAA constraint is not. Separately, the safety-buffer table shows the 40% optimum survives an EBIT drop of 30% — more than Disney's worst recorded annual decline of 29.47% and well above one standard deviation (19.17%). Disney has room; a rating constraint would be paying for protection it already has.

**Determinism:**
- DETERMINISTIC: EBIT history → percentage changes and their standard deviation; a haircut schedule → re-optimized debt ratios; firm values at two debt ratios → the cost of a constraint. All scriptable given the base model.
- JUDGMENT: which haircuts or scenarios to run; whether past volatility represents future volatility; what minimum rating (if any) management should accept; whether the rating constraint is protecting the firm or protecting management's self-image.

**Pitfalls:**
- Double-protecting. A rating constraint and a downside EBIT haircut guard the same risk; applying both leaves the firm arbitrarily under-levered.
- Accepting a rating constraint without pricing it.
- Using a normal-year EBIT for a cyclical or commodity firm without checking the recession value ([[optimal-debt-ratio-by-firm-type]]).
- Assuming the optimal ratio depends on what the money is spent on.
- Confusing "the rating would fall" with "operating income would fall." The second effect is real but belongs in the enhanced approach, not in a blanket constraint.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.62-67

**Related:** [[cost-of-capital-approach]], [[enhanced-cost-of-capital-approach]], [[synthetic-rating-and-cost-of-debt]], [[optimal-debt-ratio-by-firm-type]], [[recapitalization-and-buyback-price]], [[moving-to-the-optimal]]

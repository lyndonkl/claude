# Facing uncertainty with a Monte Carlo simulation

**Core idea:** A point estimate hides how much you do not know. A simulation replaces the two or three inputs you are least sure about with probability distributions, runs the same valuation thousands of times, and returns a distribution of values instead of one number. That output answers questions a point estimate cannot: how often is equity worth nothing, where does the market price sit inside the plausible range, and how wide is the middle of the distribution. This is the right tool for a **narrative shift** — the business model gets better or worse, changing market size, share or profitability — as opposed to a narrative break or a narrative expansion, which need probabilities and real options respectively.

**Formulas:**
- Value_trial = Model(one random draw from each input distribution). Repeat N times, then read percentiles off the sorted output.
- Median simulated value is not the base-case value. Skew, especially from lognormal growth inputs, pulls the mean and median apart.
- Report the 10th and 90th percentiles as a working range, and the fraction of trials with value ≤ 0 as the failure-like tail.
- Correlations matter: draw correlated inputs jointly, not independently.

**Procedure:**
1. **Build and finish the base-case valuation first.** The simulation varies inputs of an existing model; it does not replace the model.
2. **Pick the three or four inputs that both matter and are genuinely uncertain.** Growth, take rate, target margin, investment efficiency and the equity risk premium are the usual candidates. Do not distribute everything.
3. **Choose a distribution shape per input, and justify it.** Lognormal for a growth rate that cannot go below −100% and has a long right tail. Triangular when you can state a minimum, a likeliest and a maximum. Uniform when you have a range and no view inside it. A minimum-extreme distribution when downside surprises dominate.
4. **Set the correlations.** If lower earnings mean less cash returned, that correlation belongs in the simulation. Getting the sign right matters more than the exact number.
5. **Run enough trials.** Damodaran's Paytm run used 100,000.
6. **Read the output as a distribution.** Median, 10th and 90th percentiles, and the share of trials below zero. Treat the 0th and 100th percentiles as artefacts of the tails, not as a range.
7. **Locate the market price in the distribution.** If price sits near the median, the market is inside your uncertainty band and you have no edge. If it sits beyond the 90th percentile, you have a case.
8. **Do not double-count risk.** The discount rate already carries risk. The simulation is about the range of outcomes, not an extra risk premium.

**Reference data:** Paytm, valued ahead of its September 2021 IPO. Four inputs were given distributions:
- GMV growth rate in years 1–5: lognormal.
- Target take rate (revenue/GMV) in year 10: triangular.
- Target operating margin in year 10: minimum-extreme, correlated 0.50 with the take rate.
- Sales to invested capital in years 2–10: uniform.

Simulated value of equity, 100,000 trials (₹ millions):

| Percentile | Value of equity |
|---|---|
| 0.0% | −2,242,001 |
| 10.0% | 627,263 |
| 20.0% | 843,180 |
| 30.0% | 992,398 |
| 40.0% | 1,121,771 |
| 50.0% | 1,246,824 |
| 60.0% | 1,378,339 |
| 70.0% | 1,528,468 |
| 80.0% | 1,717,973 |
| 90.0% | 2,010,052 |
| 100.0% | 8,020,677 |

Findings: equity value was negative in about 3% of trials. The median of ₹1,246,824M sat *below* the base-case DCF value of ₹1,456,708M, and extreme outliers explain the divergence. A sensible extreme range is the 10th to 90th percentile, ₹627,263M to ₹2,010,052M.

Second example — the S&P 500 index valuation of 1 November 2020, simulated. Input distributions:
- 2020 earnings: likeliest 130.2, scale 6.
- 2021 earnings: likeliest 166.2, scale 8, correlated 0.80 with 2020 earnings.
- Share of lost earnings recouped by 2024: triangular, minimum 60%, maximum 100%.
- Equity risk premium: expected value 5.58%, relative standard deviation 15%.
- Cash returned as a percent of earnings in 2020: likeliest 75.00%, scale 5%, correlated −0.5 with earnings. Weaker earnings mean less cash returned.

| Percentile | Forecast intrinsic index value |
|---|---|
| 0% | 2,203.59 |
| 10% | 2,817.08 |
| 20% | 2,906.30 |
| 30% | 2,973.67 |
| 40% | 3,033.43 |
| 50% | 3,091.51 |
| 60% | 3,150.60 |
| 70% | 3,217.16 |
| 80% | 3,299.18 |
| 90% | 3,415.91 |
| 100% | 4,495.29 |

The index traded at 3,270, which sits between the 70th and 80th percentiles. The market was at the upper-middle of the plausible range rather than obviously wrong.

**Worked example:** Paytm, above. The base-case DCF said ₹1,456,708M of equity value. The simulation said the median outcome was ₹1,246,824M, with a one-in-thirty chance of the equity being worthless and a 10th-to-90th range of roughly ₹627,000M to ₹2,010,000M. That changes the investment conversation. A point estimate 17% above the simulated median, in a distribution that wide, is not a precise claim about value. It is one draw from a very broad range.

**Determinism:**
- DETERMINISTIC: the simulation mechanics. Given the distributions, correlations, trial count and random seed, the percentile table is reproducible exactly.
- JUDGMENT: which inputs get distributions, what shape each takes, the parameters of each shape, and the correlation structure. That judgment needs historical volatility of the input, industry ranges, and a causal view of what moves with what.

**Pitfalls:**
- Distributing every input, which manufactures a wide range with no information in it.
- Ignoring correlation and drawing inputs independently, which understates the tails.
- Quoting the minimum and maximum as the range. Use the 10th and 90th percentiles instead.
- Assuming the simulation median equals the base case. For Paytm it did not.
- Adding a risk premium to the discount rate *and* simulating the same risk, which double counts it.
- Using simulation on a narrative break. A binary end-of-story event needs a probability and a consequence, not a distribution over a continuing model. See [[narrative-updating-feedback-loop]].

**Sources:**
- valuationmotleyfool p.26
- valpacket1spr21 p.292
- valpacket1spr21 p.274 (narrative shift → Monte Carlo or scenario analysis)
- valpacket1spr20 p.270

**Related:** [[narrative-updating-feedback-loop]], [[narrative-scenario-grids]], [[life-cycle-uncertainty]], [[bermuda-triangle-of-valuation]], [[possible-plausible-probable]]

# Scenario tables and Monte Carlo simulation

**Core idea:** A single number hides everything interesting about a difficult valuation. Two tools open it up. A two-way sensitivity table shows how value moves across the two inputs that matter most, and it always reveals the same uncomfortable truth: some combination of assumptions justifies any market price. The right question is never "is there a scenario that justifies the price?" — there always is — but "is that scenario **probable**?" A Monte Carlo simulation answers the probability question directly. Replace point estimates with distributions, run the model thousands of times, and you get everything a standard valuation gives plus two things it cannot: the spread of plausible values, and the likelihood that the firm is under- or over-valued.

**Formulas:**
- Two-way sensitivity: value per share `V(x, y)` evaluated on a grid of the two chosen drivers, usually compounded revenue growth and target operating margin.
- Simulation: draw each uncertain input from its distribution, respecting the correlation structure, recompute the model, and collect the output. Report percentiles of the value distribution, not just the mean.
- Position of the market price in the distribution: `Percentile(price) = share of simulated values below the current price`. A price at the 85th–90th percentile means the stock is overvalued in most, but not all, scenarios.
- Correlations matter and must be signed correctly. Revenue and margin are usually positively correlated; the payout ratio and earnings shortfalls are negatively correlated (a bad earnings year means less cash returned).

**Procedure:**
1. Finish the base valuation first. The simulation is the same model with distributions swapped in, not a different model.
2. Identify the two or three inputs that actually drive value. For a young company: revenue growth and target margin. For a commodity firm: the commodity price and the margin. For an index: earnings, the recovery fraction and the equity risk premium.
3. Build the two-way table over a defensible range of both drivers, and mark the cells that reach the current market price.
4. Judge probability, not possibility. Ask what the price-justifying cells imply about market share, industry margins and the competitive landscape.
5. For the simulation, choose a distribution per input and say why:
   - Uniform when you know only the range.
   - Normal when you have a central estimate and a symmetric error.
   - Triangular when you have a minimum, a likeliest and a maximum.
   - Right-skewed (lognormal-type) for prices that cannot go below zero but can spike.
6. Specify correlations between inputs. Independent draws on correlated inputs understate the tails and produce impossible combinations.
7. Run it, then report the percentile table and where the market price sits.
8. Use the result as a decision input: a stock overvalued at the median but undervalued in the top decile is a different proposition from one overvalued everywhere.

**Reference data (1):** Amazon, January 2000 — value per share by compounded revenue growth (rows) and target operating margin (columns). The market price was $84.

| Growth \ Margin | 6% | 8% | 10% | 12% | 14% |
|---|---|---|---|---|---|
| 30% | $(1.94) | $2.95 | $7.84 | $12.71 | $17.57 |
| 35% | $1.41 | $8.37 | $15.33 | $22.27 | $29.21 |
| 40% | $6.10 | $15.93 | $25.74 | $35.54 | $45.34 |
| 45% | $12.59 | $26.34 | $40.05 | $53.77 | $67.48 |
| 50% | $21.47 | $40.50 | $59.52 | $78.53 | $97.54 |
| 55% | $33.47 | $59.60 | $85.72 | $111.84 | $137.95 |
| 60% | $49.53 | $85.10 | $120.66 | $156.22 | $191.77 |

Only the most aggressive corners reach $84: 60% growth with margins of 8% or better, 55% growth with 10% or better, and 50% growth with 14%. Every one of those requires Amazon to become both enormous and highly profitable — possible, but the table forces the reader to say how probable.

**Reference data (2):** Amazon, September 2018 — simulation inputs and output. Revenue growth uniform between 5% and 25%, correlated 0.40 with the margin; operating margin normal with a mean of 12.50% and a standard deviation of 2.00%; sales-to-invested-capital triangular with a minimum of 3.95, a likeliest of 5.95 and a maximum of 7.95; cost of capital drawn with a location of 5.00%, a mean of 7.97% and a standard deviation of 0.80%. Base case $1,255.09; simulation mean $1,343.67; median $1,241.98. The market price of $1,970 sat around the 85th–90th percentile.

| Percentile | Value/share | Percentile | Value/share |
|---|---|---|---|
| 0% | $234.29 | 60% | $1,411.82 |
| 10% | $705.19 | 70% | $1,605.37 |
| 20% | $832.65 | 80% | $1,837.98 |
| 30% | $957.69 | 90% | $2,152.15 |
| 40% | $1,092.41 | 100% | $3,887.62 |
| 50% | $1,241.97 | | |

**Reference data (3):** Shell, March 2016 — the oil price drawn from a right-skewed distribution and the target margin from a roughly normal one, with everything else (tax rate, revenue growth, cost of capital) held fixed. Point estimate $39.31; simulated median $36.99; 10th percentile $23.90; 90th percentile $57.49.

**Reference data (4):** S&P 500, November 2020 — a simulation of an index valuation. 2020 earnings likeliest 130.2 with scale 6; 2021 earnings likeliest 166.2 with scale 8; the two correlated at **0.80**. The share of lost earnings recouped by 2024 is triangular between 60% and 100%. The equity risk premium has an expected value of 5.58% with a relative standard deviation of 15%. Cash returned as a percent of earnings in 2020 is likeliest 75.00% with scale 5%, correlated **−0.5** with earnings — weaker earnings means less cash returned.

| Percentile | Intrinsic index value | Percentile | Intrinsic index value |
|---|---|---|---|
| 0% | 2,203.59 | 60% | 3,150.60 |
| 10% | 2,817.08 | 70% | 3,217.16 |
| 20% | 2,906.30 | 80% | 3,299.18 |
| 30% | 2,973.67 | 90% | 3,415.91 |
| 40% | 3,033.43 | 100% | 4,495.29 |
| 50% | 3,091.51 | | |

The index traded at 3,270, which sits between the 70th and 80th percentiles — inside the plausible band rather than clearly wrong.

**Worked example:** Amazon, January 2000. The base valuation gave $35.08 per share against a price of $84. The sensitivity table shows exactly what the market had to believe: at the base 10% target margin, the market price needed a compounded revenue growth rate of about 55%, against the 40%-ish rate in the base case. Read the other way, at the base growth rate the market needed a margin far above the 10% retail-industry average. Neither is impossible. The 2014 retrospective settled it: Amazon's revenues eventually beat the forecast, and its operating margin fell to 0.11%. The aggressive-growth-plus-high-margin corner never arrived.

**Determinism:** DETERMINISTIC — the model itself, so each cell of the sensitivity table and each simulation draw is a reproducible computation; the percentile table given a fixed random seed; and the position of the market price within the output distribution. JUDGMENT: which two drivers deserve the table, the ranges to span, the shape of each input distribution, the correlation structure, and above all the probability you attach to the price-justifying scenarios. That last judgment needs market-size data, industry margin distributions and competitive analysis.

**Pitfalls:**
- Confusing possibility with probability. A scenario exists for every price; that is a fact about arithmetic, not evidence about the company.
- Drawing correlated inputs independently. High revenue growth with a low margin, or collapsing earnings with an unchanged payout, are combinations that cannot happen.
- Simulating inputs that barely move value while holding the real driver fixed. The output spread then understates the true uncertainty.
- Reporting only the mean. The median and the percentile of the market price carry the decision-relevant information.
- Treating the simulation as a substitute for judgment. Someone still chose every distribution.
- Using the simulation range as a "target price band". It is a statement about your uncertainty, not about where the price will trade.
- Forgetting that a simulation of a single company still misses model risk: if the structure of the model is wrong, every draw is wrong.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.307
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.292
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.354
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.357
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.298
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.303
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.345
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.348

**Related:** [[commodity-and-cyclical-valuation]], [[young-company-valuation]], [[market-and-macro-crisis-valuation]], [[value-versus-price]], [[distress-and-failure-adjusted-value]], [[difficult-company-taxonomy]], [[sensitivity-analysis]]

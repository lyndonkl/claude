# Value of recapitalising, benchmarking and the EBIT stress test

**Core idea:** Finding the WACC-minimising debt ratio is only half of Part VI. The other half converts the WACC saving into dollars of firm value and per-share price, then asks how fragile that answer is. Two valuation methods are used: capitalise the annual saving with no growth, or grow FCFF in perpetuity at the lower discount rate. Two robustness checks follow: benchmark the current debt ratio against the industry average and a cross-sectional regression, and re-run the whole optimum with EBIT set three standard deviations below expectation. The stress test is what separates a firm that can move to the optimum from one that only appears to.

**Formulas:**
- Increase in firm value (no growth) = (WACC_old − WACC_new) × Enterprise value / WACC_new. This capitalises the annual cost saving as a perpetuity at the new WACC.
- Firm value (perpetual growth) = FCFF × (1 + g) / (WACC − g). g = perpetual growth rate; FCFF = current free cash flow to the firm.
- Increase in value per share = Increase in firm value / Shares outstanding.
- New stock price = Old price + increase per share. A variant assumes buybacks execute at the *old* price, which changes the per-share result because fewer or more shares are retired.
- Stressed EBIT = Expected EBIT − 3 × standard deviation of EBIT. Feed this into the same coverage → rating → spread → WACC machinery.

**Procedure:**
1. Take WACC_old (current structure) and WACC_new (at the optimum) from the schedule.
2. Compute the no-growth value increase by capitalising the annual saving, and translate it into a per-share figure and a new price.
3. Repeat with the perpetual-growth formula using current FCFF and a defensible perpetual growth rate. Report both; the growth version gives the larger number.
4. Report both buyback conventions where the recapitalisation is executed via share repurchase — at the new price and at the old price.
5. **Benchmark the current ratio.** Compare the market debt ratio to (a) the industry average and (b) the debt ratio predicted by a cross-sectional regression run on worldwide company data.
6. **Stress test.** Set EBIT three standard deviations below expected and re-run the full debt-ratio grid. Record how far the optimum moves.
7. Convert the stress result into a pace recommendation. A large downward shift in the optimum under stress argues for moving gradually.
8. State the caveat explicitly: the only rating-change criterion in the synthetic rating is the interest coverage ratio, which may understate rating risk.

**Reference data:** Spring 2015 value impact of moving to the optimal capital structure.

| Firm value impact | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| EV ($m, before) | 64,308 | 140,035 | 21,334 | 20,549 |
| EV ($m, after, no growth) | 68,773 | 150,071 | 22,733 | 22,174 |
| Increase in firm value ($m) | 4,465 | 10,035 | 1,398 | 1,626 |
| Increase in value per share | $6 | $10 | $45 | $5 |
| New stock price | $83.14 | $106.57 | $729.62 | $46.01 |
| New price (buybacks at old price) | $85.91 | $102.92 | $747.36 | $16.62 |
| FCFF ($m) | 1,478 | 4,117 | 935 | 648 |
| Perpetual growth rate | 4.18% | 3.10% | 1.83% | 3.09% |
| EV ($m, after, perpetual growth) | 78,272 | 161,935 | 23,359 | 23,980 |
| Increase in firm value ($m) | 13,964 | 21,900 | 2,025 | 3,431 |
| Increase in value per share | $19 | $23 | $65 | $11 |
| New stock price | $95.75 | $118.92 | $749.84 | $51.94 |
| New price (buybacks at old price) | $104.43 | $125.76 | $775.54 | $59.81 |

Summary of the effect: WACC falls 39-51 bps and firm value rises 9.5-21.7% (SBUX +21.71%, MCD +15.64%, CMG +9.49%, TSN +18.59%).

Stressed WACC schedule, EBIT three standard deviations below expected; optimum marked:

| Debt ratio | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| 10% | 6.55% | 6.22% | 6.12% | 6.59% |
| 20% | 6.38% | 6.06% | 6.04%* | 6.43% |
| 30% | 6.30%* | 5.94% | 7.95% | 6.34%* |
| 40% | 8.25% | 5.86%* | 9.33% | 8.85% |
| 50% | 9.54% | 9.06% | 10.38% | 10.33% |
| 60% | 11.13% | 10.65% | 11.43% | 11.38% |
| 70% | 12.18% | 11.70% | 12.48% | 12.43% |
| 80% | 13.23% | 12.75% | 13.53% | 13.48% |
| 90% | 14.28% | 13.80% | 14.58% | 14.53% |

Debt ratio benchmarking:

| Benchmark | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| Debt ratio (market) | 11.92% | 34.99% | 2.45% | 39.72% |
| Industry average | 20.96% | 21.80% | 21.80% | 21.39% |
| Estimated debt ratio (world regression) | 22.29% | 20.93% | 18.72% | 29.76% |

**Worked example:** Tyson Foods, 2015. Base case: the optimum is 60%, WACC falls from 6.39% to 5.88% (−51 bps), and the perpetual-growth calculation lifts enterprise value from $20,549m to $23,980m, a gain of $3,431m or 18.59%, worth about $11 per share. Under stress the picture changes completely. With EBIT three standard deviations below expected, Tyson's optimum collapses from 60% to 30% — the steepest fall in the group, consistent with its 16.16% EBIT growth volatility. Benchmarking adds a second warning: at 39.72% market leverage Tyson already sits well above both the 21.39% industry average and the 29.76% ratio predicted by the worldwide regression. Conclusion: the value gain is real but should be captured gradually, because rating agencies penalise firms that move quickly past their expected ratio.

**Determinism:** DETERMINISTIC — value increase (both methods), per-share amounts, new prices under both buyback conventions, the stressed WACC schedule, and the regression-predicted debt ratio, given WACC before and after, enterprise value, FCFF, growth rate, share count, EBIT volatility and the regression coefficients. JUDGMENT — the perpetual growth rate, whether the recapitalisation actually happens via buybacks and at what price, how many standard deviations of stress to apply, and the pace recommendation. That last one needs the rating-agency stance, the pipeline of pending transactions, and management's risk appetite.

**Pitfalls:**
- Quoting only the perpetual-growth value increase. It is systematically larger and more assumption-dependent than the no-growth version. Report both.
- Ignoring the buyback execution price. Tyson's new price under the no-growth, old-price-buyback convention is $16.62 against $46.01 under the other convention — an implausible spread that signals the convention is doing real work in the answer.
- Skipping the stress test for a firm with volatile EBIT. The base-case optimum is meaningless there.
- Treating the industry average and the regression prediction as interchangeable. Starbucks and Chipotle sit far below both; McDonald's and Tyson sit above the regression prediction, which is the rating-relevant comparison.
- Forgetting that firms with stable earnings, low insider ownership and low intangible assets can safely run above the industry average. The benchmark is a reference point, not a cap.

**Sources:**
- corporate_finance--project--food2015 p.12-13, p.2
- corporate_finance--project--cfproj p.9-10

**Related:** [[optimal-debt-ratio-wacc-schedule]], [[qualitative-debt-tradeoff]], [[debt-design-deliverable]], [[value-of-control-and-synergy]], [[project-executive-summary-scorecard]]

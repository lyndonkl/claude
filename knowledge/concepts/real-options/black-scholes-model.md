# The Black-Scholes model and the dividend adjustment

**Core idea:** Black-Scholes is the continuous-time limit of the binomial model. It prices a European call as a function of five inputs and embeds a replicating portfolio inside the formula: buy `N(d1)` units of the underlying and borrow `K x e^(-rt) x N(d2)`. The original model valued European options that were dividend-protected. Real options are never dividend-protected — value leaks out while you wait — so almost every real-option application in this material uses the **dividend-adjusted** version, where a yield `y` discounts the underlying asset value. Getting `y` right matters as much as getting volatility right, because real-option lives run 5 to 17 years.

**Formulas:**

Standard Black-Scholes call:
- `C = S x N(d1) - K x e^(-r*t) x N(d2)`
- `d1 = [ln(S/K) + (r + sigma^2 / 2) x t] / (sigma x sqrt(t))`
- `d2 = d1 - sigma x sqrt(t)`

Dividend-adjusted (constant yield) call and put — the form used for every real option here:
- `C = S x e^(-y*t) x N(d1) - K x e^(-r*t) x N(d2)`
- `d1 = [ln(S/K) + (r - y + sigma^2 / 2) x t] / (sigma x sqrt(t))`
- `d2 = d1 - sigma x sqrt(t)`
- `P = K x e^(-r*t) x (1 - N(d2)) - S x e^(-y*t) x (1 - N(d1))`

Symbols:
- `S` = current value of the underlying asset
- `K` = strike (exercise) price
- `t` = life to expiration, in years
- `r` = riskless interest rate corresponding to the life of the option (a government bond rate of matching maturity/duration)
- `sigma` = standard deviation of `ln(value)` of the underlying asset; `sigma^2` = variance in `ln(value)`
- `y` = dividend yield = dividends (or value leakage) / current value of the asset, assumed constant over the option's life
- `N(.)` = cumulative standard normal distribution; `N(d1)` is the option delta

**Procedure:**
1. Estimate the five (or six) inputs. Map each to its business meaning for the specific real option — see [[option-to-delay]], [[patent-valuation-as-option]], [[natural-resource-options]], [[option-to-expand]], [[option-to-abandon]], [[financing-flexibility-option]], [[equity-as-call-option]].
2. Match `r` to the option's life. For an option with an 11-year duration, use a bond of roughly 11-year duration, not a short rate.
3. Compute `d1` using the dividend-adjusted numerator if there is any cost of delay. Compute `d2 = d1 - sigma x sqrt(t)`.
4. Look up `N(d1)` and `N(d2)` in the table below (interpolate between 0.05 steps, or use a normal CDF function).
5. Apply the call or put formula.
6. Check the model is admissible before quoting the number: continuous price process, no jumps, and either European exercise or an early-exercise decision you have handled separately. If early exercise or jumps matter, switch to [[replicating-portfolio-and-binomial-model]].
7. Sanity-check the direction of each input against [[option-payoffs-and-determinants]].

**Reference data:**

Cumulative standard normal distribution `N(d)`, `d` from -3.00 to +3.00 in steps of 0.05. `N(d1)` is the area under the normal curve to the left of `d1`.

| d | N(d) | d | N(d) | d | N(d) |
|---|------|---|------|---|------|
| -3.00 | 0.0013 | -1.00 | 0.1587 | 1.05 | 0.8531 |
| -2.95 | 0.0016 | -0.95 | 0.1711 | 1.10 | 0.8643 |
| -2.90 | 0.0019 | -0.90 | 0.1841 | 1.15 | 0.8749 |
| -2.85 | 0.0022 | -0.85 | 0.1977 | 1.20 | 0.8849 |
| -2.80 | 0.0026 | -0.80 | 0.2119 | 1.25 | 0.8944 |
| -2.75 | 0.0030 | -0.75 | 0.2266 | 1.30 | 0.9032 |
| -2.70 | 0.0035 | -0.70 | 0.2420 | 1.35 | 0.9115 |
| -2.65 | 0.0040 | -0.65 | 0.2578 | 1.40 | 0.9192 |
| -2.60 | 0.0047 | -0.60 | 0.2743 | 1.45 | 0.9265 |
| -2.55 | 0.0054 | -0.55 | 0.2912 | 1.50 | 0.9332 |
| -2.50 | 0.0062 | -0.50 | 0.3085 | 1.55 | 0.9394 |
| -2.45 | 0.0071 | -0.45 | 0.3264 | 1.60 | 0.9452 |
| -2.40 | 0.0082 | -0.40 | 0.3446 | 1.65 | 0.9505 |
| -2.35 | 0.0094 | -0.35 | 0.3632 | 1.70 | 0.9554 |
| -2.30 | 0.0107 | -0.30 | 0.3821 | 1.75 | 0.9599 |
| -2.25 | 0.0122 | -0.25 | 0.4013 | 1.80 | 0.9641 |
| -2.20 | 0.0139 | -0.20 | 0.4207 | 1.85 | 0.9678 |
| -2.15 | 0.0158 | -0.15 | 0.4404 | 1.90 | 0.9713 |
| -2.10 | 0.0179 | -0.10 | 0.4602 | 1.95 | 0.9744 |
| -2.05 | 0.0202 | -0.05 | 0.4801 | 2.00 | 0.9772 |
| -2.00 | 0.0228 | 0.00 | 0.5000 | 2.05 | 0.9798 |
| -1.95 | 0.0256 | 0.05 | 0.5199 | 2.10 | 0.9821 |
| -1.90 | 0.0287 | 0.10 | 0.5398 | 2.15 | 0.9842 |
| -1.85 | 0.0322 | 0.15 | 0.5596 | 2.20 | 0.9861 |
| -1.80 | 0.0359 | 0.20 | 0.5793 | 2.25 | 0.9878 |
| -1.75 | 0.0401 | 0.25 | 0.5987 | 2.30 | 0.9893 |
| -1.70 | 0.0446 | 0.30 | 0.6179 | 2.35 | 0.9906 |
| -1.65 | 0.0495 | 0.35 | 0.6368 | 2.40 | 0.9918 |
| -1.60 | 0.0548 | 0.40 | 0.6554 | 2.45 | 0.9929 |
| -1.55 | 0.0606 | 0.45 | 0.6736 | 2.50 | 0.9938 |
| -1.50 | 0.0668 | 0.50 | 0.6915 | 2.55 | 0.9946 |
| -1.45 | 0.0735 | 0.55 | 0.7088 | 2.60 | 0.9953 |
| -1.40 | 0.0808 | 0.60 | 0.7257 | 2.65 | 0.9960 |
| -1.35 | 0.0885 | 0.65 | 0.7422 | 2.70 | 0.9965 |
| -1.30 | 0.0968 | 0.70 | 0.7580 | 2.75 | 0.9970 |
| -1.25 | 0.1056 | 0.75 | 0.7734 | 2.80 | 0.9974 |
| -1.20 | 0.1151 | 0.80 | 0.7881 | 2.85 | 0.9978 |
| -1.15 | 0.1251 | 0.85 | 0.8023 | 2.90 | 0.9981 |
| -1.10 | 0.1357 | 0.90 | 0.8159 | 2.95 | 0.9984 |
| -1.05 | 0.1469 | 0.95 | 0.8289 | 3.00 | 0.9987 |
| -1.00 | 0.1587 | 1.00 | 0.8413 | | |

**Worked example:** Biogen's Avonex patent, valued as a dividend-adjusted call.

Inputs:

| Input | Value | Source |
|---|---|---|
| `S` | $3,422 million | PV of cash flows from introducing the drug now |
| `K` | $2,875 million | PV of cost of developing the drug for commercial use |
| `t` | 17 years | Patent life |
| `r` | 6.7% | 17-year T-bond rate |
| `sigma^2` | 0.224 | Industry-average firm variance for biotech firms |
| `y` | 5.89% | Cost of delay = 1/17 |

Outputs: `d1` = 1.1362, `N(d1)` = 0.8720; `d2` = -0.8512, `N(d2)` = 0.2076.

`C = 3,422 x e^(-0.0589 x 17) x 0.8720 - 2,875 x e^(-0.067 x 17) x 0.2076 = $907 million`.

Note the effect of the dividend adjustment. Without it the call would be far larger; the 5.89% annual cost of delay compounded over 17 years cuts the underlying's effective value by roughly two thirds.

**Determinism:** **DETERMINISTIC**: everything downstream of the inputs. A script takes `(S, K, t, r, sigma, y, call/put)` and returns `d1`, `d2`, `N(d1)`, `N(d2)`, and the option value. The `N(d)` lookup is a table read or a normal CDF call. **JUDGMENT**: all six inputs when the underlying is a real asset. Asset value `S` comes from a DCF you build. Volatility `sigma` comes from a proxy you choose. Candidates are comparable-firm variance, resource-price variance, or a capital-budgeting simulation. Yield `y` comes from a theory of value leakage, often the `1/n` heuristic. Life `t` comes from reading a patent life, a relinquishment period, or a competitive window. Rate `r` is the only near-mechanical input. Even it requires matching maturity to the option's life. Also **JUDGMENT**: whether Black-Scholes is admissible at all, given jumps and early exercise.

**Pitfalls:**
- Omitting the dividend/cost-of-delay yield on a long-dated real option. This is the single largest overstatement error in real-option valuation.
- Using a short-term riskless rate for a long-dated option. Match `r` to the option's life or duration.
- Feeding in a variance of *cash flows* where the formula wants the variance of `ln(value)` of the underlying.
- Using Black-Scholes when the underlying jumps or when early exercise is likely — the normal case for real options. See [[replicating-portfolio-and-binomial-model]].
- Quoting the output to the dollar. When the underlying is untraded, no arbitrage enforces the value, and the estimate inherits every error in the capital budgeting behind `S`.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.16-19
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.16-19

**Related:** [[replicating-portfolio-and-binomial-model]], [[option-payoffs-and-determinants]], [[patent-valuation-as-option]], [[natural-resource-options]], [[option-to-expand]], [[option-to-abandon]], [[equity-as-call-option]], [[real-options-framework]]

# Black-Scholes and Put-Call Parity

**Core idea:** Black-Scholes is the binomial model taken to its continuous limit. It prices a European call as a function of just five inputs: the current value of the underlying, the strike price, the time to expiration, the riskless rate, and the variance of the natural log of the underlying's value. Its structure is the replicating portfolio in closed form. You buy `N(d1)` shares of the underlying and borrow `K·e^(−rt)·N(d2)`, and `N(d1)` is the option delta. The original model assumed the option was European and dividend-protected. A dividend adjustment discounts the asset price at the dividend yield. Put values then follow from put-call parity, an arbitrage condition that ties the put, the call, the stock, and a riskfree bond together.

**Formulas:**
- Black-Scholes call value: `C = S·N(d1) − K·e^(−rt)·N(d2)`
  where `d1 = [ln(S/K) + (r + σ²/2)·t] / (σ·√t)` and `d2 = d1 − σ·√t`.
- Symbols: `S` = current value of the underlying asset; `K` = strike price; `t` = time to expiration, in years; `r` = riskless rate matching the option's life, continuously compounded; `σ` = standard deviation of `ln(value)` of the underlying, so `σ²` is the variance; `N(·)` = cumulative standard normal distribution function.
- Embedded replicating portfolio: buy `N(d1)` shares (the option delta), borrow `K·e^(−rt)·N(d2)`.
- Dividend-adjusted call: `C = S·e^(−yt)·N(d1) − K·e^(−rt)·N(d2)`
  where `d1 = [ln(S/K) + (r − y + σ²/2)·t] / (σ·√t)` and `d2 = d1 − σ·√t`.
- Dividend yield: `y = dividends / current value of the asset`, expressed as a continuous yield.
- Put via put-call parity: `P = K·e^(−rt)·(1 − N(d2)) − S·e^(−yt)·(1 − N(d1))`.

**Procedure:**
1. Confirm the model fits. Black-Scholes assumes a continuous price process with no jumps in asset prices. If the underlying is prone to jumps, the limiting distribution is Poisson rather than normal and the model does not apply.
2. Gather the five inputs. `S`, `K`, and `t` come from the contract and the market. `r` is the riskless rate for the option's life, in the currency of the underlying.
3. Estimate `σ` as the standard deviation of the log value of the underlying, annualized. For a traded asset use the historical or implied volatility. For a non-traded asset use a comparable.
4. If the underlying pays dividends, estimate the dividend yield `y` and use the adjusted form. This adjustment is valid only if the yield is expected to stay unchanged over the option's life.
5. Compute `d1`, then `d2 = d1 − σ√t`.
6. Look up or compute `N(d1)` and `N(d2)` from the cumulative standard normal.
7. Assemble the call value. Read `N(d1)` as the delta and `K·e^(−rt)·N(d2)` as the borrowing, which gives you the hedge as well as the price.
8. Get the put from put-call parity rather than pricing it independently. That guarantees the two are internally consistent.
9. If early exercise matters or the underlying jumps, switch to the binomial model. But recognize that a synthetic binomial tree built from the asset's variance produces a value very close to Black-Scholes anyway, so the practical gain is often small.

**Reference data:** Cumulative standard normal `N(d)`, for `d` from −3.00 to 3.00 in steps of 0.05 (Damodaran, Foundations of Finance Session 9). `N(d1)` is the area under the standard normal density to the left of `d1`.

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

**Worked example:** Price a one-year European call on a non-dividend-paying stock. Inputs: `S = 50`, `K = 40`, `t = 1`, `r = 11%` (matching the binomial example's riskless rate), `σ = 40%`.

`ln(S/K) = ln(1.25) = 0.2231`
`d1 = [0.2231 + (0.11 + 0.16/2) × 1] / (0.40 × 1) = [0.2231 + 0.19] / 0.40 = 1.0328`
`d2 = 1.0328 − 0.40 = 0.6328`
From the table, `N(1.05) = 0.8531` and `N(1.00) = 0.8413`, so `N(1.0328) ≈ 0.8491`. Likewise `N(0.65) = 0.7422` and `N(0.60) = 0.7257`, so `N(0.6328) ≈ 0.7365`.
`C = 50 × 0.8491 − 40 × e^(−0.11) × 0.7365 = 42.46 − 40 × 0.8958 × 0.7365 = 42.46 − 26.39 = $16.07`

The delta is 0.8491, so you replicate the call by holding 0.849 shares and borrowing $26.39. Compare that with the two-period binomial example on the same strike and rate, which gave a delta of 0.8278 and borrowing of $21.61 — the same structure, reached by a different route.

The matching put, by put-call parity with `y = 0`:
`P = 40 × 0.8958 × (1 − 0.7365) − 50 × (1 − 0.8491) = 35.83 × 0.2635 − 50 × 0.1509 = 9.44 − 7.55 = $1.89`

**Determinism:**
- DETERMINISTIC: everything once the five inputs are set. Inputs `(S, K, t, r, σ)` → `d1`, `d2`, `N(d1)`, `N(d2)`, call value, delta, and borrowing. Inputs `(S, K, t, r, y, σ)` → dividend-adjusted call and, through put-call parity, the put. The `N(d)` lookup is exact.
- JUDGMENT: the volatility `σ`, which is the input the answer is most sensitive to and the one never directly observed. The dividend yield `y` and whether it will hold constant. The effective life `t` for a real option. Whether the continuous-process assumption is defensible for this underlying. These need a price history or a comparable asset, the payout policy, and a view on whether the asset jumps.

**Pitfalls:**
- Using Black-Scholes when the underlying's value jumps. The model explicitly assumes a continuous price process with no jumps.
- Applying the dividend adjustment when the dividend yield is expected to change over the option's life. The adjustment is valid only for a constant yield.
- Using the standard deviation of the *value* rather than of `ln(value)`.
- Pricing a put independently instead of deriving it from put-call parity, which lets the call and put values drift out of arbitrage-consistent alignment.
- Using an American option's full stated life as `t` without asking whether early exercise will cut it short.
- Assuming the binomial model is meaningfully better for real options. Building realistic end nodes is the hard part, and a synthetic tree from the asset's variance lands near the Black-Scholes value.
- Mismatching the riskless rate's horizon to the option's life, or its currency to the underlying's.

**Sources:**
- `foundations_of_finance--valuing_options p.12-16`

**Related:** [[replicating-portfolio-and-binomial-model]], [[option-payoffs-and-value-determinants]], [[compounding-frequency-and-effective-rates]], [[real-options]]

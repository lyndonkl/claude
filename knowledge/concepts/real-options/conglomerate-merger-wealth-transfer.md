# Conglomerate mergers and the wealth transfer to bondholders

**Core idea:** Buy another firm at exactly its fair market value and, in an efficient market, your stock price should not move. The option model says otherwise. When two firms with imperfectly correlated cash flows combine, the variance of the merged firm's value is lower than the value-weighted average of the two variances. Equity is a call on the firm, and calls are long volatility. So the diversification itself reduces equity value and raises debt value — a pure transfer from stockholders to bondholders, with no change in total firm value. Conglomerate mergers not followed by an increase in leverage are likely to produce exactly this redistribution.

**Formulas:**
- Variance of the combined firm's value:
  - `sigma^2_combined = w1^2 x sigma1^2 + w2^2 x sigma2^2 + 2 x w1 x w2 x rho12 x sigma1 x sigma2`
  - `w1`, `w2` = value weights of the two firms; `sigma1`, `sigma2` = standard deviations of the two firms' values; `rho12` = correlation between the firms' values/cash flows.
- Combined firm value: `V_combined = V1 + V2` (no synergy assumed).
- Combined face value of debt: `K_combined = K1 + K2`.
- Equity of the combined firm: the Black-Scholes call on `V_combined` with strike `K_combined`, variance `sigma^2_combined`, and the common debt maturity.
- Wealth transfer: `Transfer to bondholders = (E1 + E2) - E_combined`, since total firm value is unchanged.
- Whenever `rho12 < 1`, `sigma^2_combined` is below the value-weighted average variance, so the transfer is positive.

**Procedure:**
1. Value each firm's equity and debt separately as options, using [[equity-as-call-option]]. Record `E1`, `D1`, `E2`, `D2`.
2. Compute the value weights `w1` and `w2` from the two firm values.
3. Estimate the correlation `rho12` between the two firms' values or cash flows. This is the input that decides whether there is a transfer at all.
4. Compute the combined variance with the portfolio formula.
5. Value the combined firm's equity as one call: underlying `V1 + V2`, strike `K1 + K2`, the combined variance, and the debt maturity.
6. Compute the combined debt value as `V_combined - E_combined`.
7. Compare `E_combined` with `E1 + E2`. The shortfall is the wealth transferred to bondholders.
8. Consider releveraging. Increasing debt after the merger raises variance-driven equity value and can offset the transfer. Without it, expect stockholders to lose.

**Reference data:**

Two-firm setup used in the packet. Ten-year bond rate = 10%.

| Item | Firm A | Firm B |
|---|---|---|
| Value of the firm | $100 million | $150 million |
| Face value of debt (10-yr zeros) | $80 million | $50 million |
| Maturity of debt | 10 years | 10 years |
| Std. dev. in value | 40% | 50% |
| Correlation between cash flows | 0.4 (between A and B) | — |

Option values before and after the merger ($ millions):

| Item | Firm A | Firm B | Combined firm |
|---|---|---|---|
| Value of equity | 75.94 | 134.47 | **207.43** |
| Value of debt | 24.06 | 15.53 | **42.57** |
| Value of the firm | 100.00 | 150.00 | 250.00 |

**Worked example:** The conglomerate merger.

*The question posed.* As a manager you buy another firm with a fair market value of $150 million for exactly $150 million. In an efficient market your firm's stock price will (a) increase, (b) decrease, or (c) remain unchanged.

*Combined variance.* Weights are 0.4 and 0.6 (100 and 150 out of 250):

`sigma^2_combined = (0.4)^2 (0.16) + (0.6)^2 (0.25) + 2 (0.4)(0.6)(0.4)(0.4)(0.5) = 0.154`

That is a combined standard deviation of about 39.2% — below Firm B's 50% and even marginally below Firm A's 40%. Diversification has reduced volatility. (The packet's expansion of the cross-product term uses the correlation 0.4 alongside the sigma terms 0.4 and 0.5.)

*The transfer.* Sum of standalone equities = `75.94 + 134.47 = $210.41 million`. Combined equity = `$207.43 million`. Stockholders lose **$2.98 million**, and bondholders gain the same amount — their combined claim rises from `24.06 + 15.53 = $39.59 million` to `$42.57 million`.

Answer: (b), once the option effect is taken into account. Nothing was overpaid and no value was destroyed. The loss is purely a redistribution across claim holders.

**Determinism:** **DETERMINISTIC**: the combined-variance formula (weights, variances and correlation give 0.154 exactly); the three option valuations; the subtraction that produces the $2.98 million transfer. A script takes `(V1, V2, K1, K2, sigma1, sigma2, rho12, t, r)` and returns every number in the tables above. **JUDGMENT**: the correlation `rho12` between the two firms' cash flows, which is estimated from history and drives the entire result — at `rho12` = 1 there is no transfer at all. The two standalone firm-value variances. The assumption of zero synergy, which isolates the option effect but is rarely true in a real deal. And whether management will releverage after the merger, which is the practical remedy.

**Pitfalls:**
- Concluding that a fairly priced acquisition is neutral for the acquirer's stockholders. Under the option model it is mildly negative when the two businesses are imperfectly correlated.
- Confusing this with the separate argument that diversification does not lower the cost of equity for a publicly traded firm. That argument is about investors diversifying on their own account; this one is about the split of a fixed firm value between debt and equity.
- Using a simple weighted average of the two variances. The portfolio formula with the correlation term is the point; the weighted average would miss the diversification effect entirely.
- Forgetting to add the two debt face values when valuing the combined equity call.
- Ignoring the remedy. Releveraging after a diversifying merger restores variance and can return the transferred value to stockholders.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.74-76
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.74-76

**Related:** [[equity-as-call-option]], [[risk-shifting-and-stockholder-bondholder-conflict]], [[distressed-equity-time-value]], [[option-payoffs-and-determinants]], [[synergy-valuation]], [[optimal-capital-structure]], [[diversification-and-cost-of-equity]]

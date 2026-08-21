# Replicating portfolios and the binomial option pricing model

**Core idea:** Option pricing rests on one trick: build a portfolio of the underlying asset plus riskfree borrowing or lending that produces exactly the option's cash flows in every future state. By arbitrage, the option must be worth what that replicating portfolio costs. The binomial model applies this trick node by node, working backward through a tree of possible asset prices. Most practitioners valuing real options prefer the binomial model to Black-Scholes for two reasons. Early exercise is the rule rather than the exception with real options. And real asset values are generally discontinuous — they jump.

**Formulas:**
- Replication: `Call = Borrowing + D x (underlying asset)`. `Put = Lending - D x (underlying asset)`, i.e. short `D` units of the underlying plus lending.
- `D` = option delta = number of units of the underlying held in the replicating portfolio.
- At any binomial node, solve the two-equation system:
  - `S_u x D - (1 + r) x B = C_u`
  - `S_d x D - (1 + r) x B = C_d`
  - Then `Option value at the node = D x S - B`.
- Symbols: `S` = asset price at the node; `S_u`, `S_d` = asset prices in the up and down successor states; `C_u`, `C_d` = option values in those states; `D` = delta (units of the asset bought); `B` = amount borrowed at the riskless rate; `r` = riskless rate per period.
- Closed form for delta at a node: `D = (C_u - C_d) / (S_u - S_d)`; then `B = (S_d x D - C_d) / (1 + r)`.

**Procedure:**
1. Build the price tree for the underlying asset over the option's life, one node per state per period.
2. Compute the option's value at every terminal node from the payoff function: `max(S - K, 0)` for a call, `max(K - S, 0)` for a put.
3. Step back one period. At each node, solve the two equations above for `D` and `B` using the two successor option values.
4. Set the node's option value to `D x S - B`.
5. For an American-style option (early exercise possible — the normal case for real options), take the maximum of that continuation value and the immediate exercise value at each node.
6. Repeat until you reach the root. The root value is the option value.
7. Choose between binomial and Black-Scholes with the limiting-distribution rule. As the time interval shrinks toward zero, one of two limits appears. If price changes get smaller as the interval shrinks, the limit is the **normal** distribution and the price process is continuous — Black-Scholes applies. If price changes stay large as the interval shrinks, the limit is the **Poisson** distribution, which allows jumps — Black-Scholes does not apply, and you need a jump (Poisson-based) model or a binomial tree.
8. Note the structural resemblance to a capital-budgeting decision tree. A binomial tree with outcomes at each node looks much like one; the difference lies entirely in the discount rates used ([[decision-trees-vs-option-pricing]]).

**Reference data:**

Model-choice rules taught in the packet:

| Condition | Preferred model |
|---|---|
| Price process continuous, no jumps, European exercise | Black-Scholes |
| Early exercise likely (typical for real options) | Binomial |
| Underlying value discontinuous / jumpy (typical for real assets) | Binomial, or a Poisson/jump model |
| Underlying traded, option traded, exercise cost known | Either; estimates are trustworthy |
| Underlying not traded | Either; estimates are noisy and unarbitraged |

**Worked example:** Two-period binomial call. Strike `K` = $40, `t` = 2 periods, `r` = 11% per period, so `(1 + r)` = 1.11. Stock tree: 50 goes to 70 or 35; 70 goes to 100 or 50; 35 goes to 50 or 25.

Terminal call values: at 100 → 60; at 50 → 10; at 25 → 0.

Upper node (`S` = 70): solve `100D - 1.11B = 60` and `50D - 1.11B = 10`. Subtracting, `50D = 50`, so `D` = 1 and `B` = 36.04. Call = `1 x 70 - 36.04` = **33.96**.

Lower node (`S` = 35): solve `50D - 1.11B = 10` and `25D - 1.11B = 0`. Subtracting, `25D = 10`, so `D` = 0.4 and `B` = 9.01. Call = `0.4 x 35 - 9.01` = **4.99**.

Root (`S` = 50): solve `70D - 1.11B = 33.96` and `35D - 1.11B = 4.99`. Subtracting, `35D = 28.97`, so `D` = 0.8278 and `B` = 21.61. Call = `0.8278 x 50 - 21.61` = **$19.42**.

**Determinism:** **DETERMINISTIC**: given the price tree, the strike, and the per-period riskless rate, every delta, every borrowing amount, and every node value is solved by linear algebra and backward induction. A script takes `(S_0, up/down factors or the full tree, K, r, number of periods, call/put, American/European)` and returns the option value plus the delta at each node. **JUDGMENT**: constructing the price tree for a real asset. The up and down magnitudes encode your volatility estimate. The number of periods encodes how finely decisions actually get made. Whether the process jumps decides whether a tree with fixed up/down factors is even the right structure. Choosing between binomial and Black-Scholes is judgment about the price process and early exercise.

**Pitfalls:**
- Using Black-Scholes when the underlying value jumps. Black-Scholes explicitly assumes a continuous price process with no jumps; jump processes require Poisson-based models.
- Using a European formula for a real option that will obviously be exercised early. Early exercise is the rule with real options, not the exception.
- Forgetting the max-with-exercise-value step at each node when the option is American.
- Applying the model to an untraded underlying and then treating the answer as a market price. Replication is what makes the value enforceable; without a traded underlying there is no arbitrage to enforce it.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.13-15, p.20
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.13-15, p.20

**Related:** [[black-scholes-model]], [[option-payoffs-and-determinants]], [[decision-trees-vs-option-pricing]], [[real-options-framework]]

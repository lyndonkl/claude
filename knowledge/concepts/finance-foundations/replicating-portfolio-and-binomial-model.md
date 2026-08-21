# The Replicating Portfolio and the Binomial Model

**Core idea:** Every option pricing model rests on one idea: you can build a portfolio of the underlying asset and riskfree borrowing or lending whose cash flows exactly match the option's, in every state of the world. If two things have identical cash flows, arbitrage forces them to have identical prices. So the option is worth whatever the replicating portfolio costs. A call is replicated by borrowing money and buying D units of the underlying stock. A put is replicated by short selling D units and lending. That D is the option delta — the number of shares in the replicating position. The binomial model applies this node by node, working backward through a tree of possible prices, and it is the most transparent way to see where an option value actually comes from.

**Formulas:**
- Replication structure: `Call = Borrowing + Buying D units of the underlying`. `Put = Short selling D units of the underlying + Lending`. `D` = option delta.
- At each binomial node, solve two equations in two unknowns:
  `S_up × D − (1+r) × B = C_up`
  `S_down × D − (1+r) × B = C_down`
  `S_up, S_down` = the two possible next-period stock prices from this node; `C_up, C_down` = the option values in those two states; `r` = the riskless rate per period; `D` = shares held; `B` = amount borrowed.
- Solving gives `D = (C_up − C_down) / (S_up − S_down)` and `B = (S_down × D − C_down) / (1+r)`.
- Option value at the node: `Value = D × S − B`, where `S` = the stock price at that node.

**Procedure:**
1. Check the three preconditions before using any replication-based model. The underlying asset must be traded, which supplies observable prices and volatility and makes replication physically possible. An active market for the option itself must exist. And you must be able to borrow and lend at the riskfree rate. If any fails, the arbitrage argument weakens and the value becomes an estimate rather than a no-arbitrage price.
2. Build the price tree forward. Start from today's price and lay out the up and down moves for each period, out to expiration.
3. Compute the option payoff at every terminal node using `max(S − K, 0)` for a call or `max(K − S, 0)` for a put.
4. Step back one period. At each node in the second-to-last layer, solve the two-equation system for `D` and `B` using the terminal payoffs you just computed.
5. Compute the node value as `D × S − B` and record it. That value becomes the `C_up` or `C_down` input for the layer below.
6. Repeat backward, layer by layer, until you reach today's node. The value there is the option value.
7. Read off the hedge. The `D` at the current node tells you how many shares to hold to replicate the option right now, and `B` tells you how much to borrow.
8. Decide whether the tree is worth the effort. Building realistic end nodes is genuinely difficult in practice. You can construct a synthetic tree from the asset's variance, but the value it produces will be very close to Black-Scholes anyway.

**Reference data:**

| Precondition for replication-based pricing | Why it is needed |
|---|---|
| Underlying asset is traded | Supplies observable prices and volatility; makes the hedge executable |
| Active market for the option | Lets arbitrage actually close the gap |
| Borrowing and lending at the riskfree rate | The `B` leg of the replicating portfolio must be financeable |

| Limiting behavior as the time step shrinks (t → 0) | Distribution | Implication |
|---|---|---|
| Price changes get smaller as the interval shortens | Normal; continuous price process | Black-Scholes applies |
| Price changes stay large as the interval shortens | Poisson; price jumps | Black-Scholes does not apply |

| When to prefer the binomial model | When Black-Scholes is fine |
|---|---|
| Early exercise matters, which is the rule rather than the exception with real options | European-style, no early exercise |
| Underlying values are discontinuous and jump | Underlying moves continuously |

**Worked example:** A two-period tree. Strike `K = $40`, `t = 2` periods, riskless rate `r = 11%` per period, so `1 + r = 1.11`. The stock starts at $50. After one period it is either $70 or $35. Terminal prices are $100, $50, or $25, with call payoffs of $60, $10, and $0.

Upper node, `S = 70`. Solve `100D − 1.11B = 60` and `50D − 1.11B = 10`. Subtracting: `50D = 50`, so `D = 1` and `B = (50 × 1 − 10)/1.11 = 36.04`. Node value = `1 × 70 − 36.04 = $33.96`.

Lower node, `S = 35`. Solve `50D − 1.11B = 10` and `25D − 1.11B = 0`. Subtracting: `25D = 10`, so `D = 0.4` and `B = (25 × 0.4 − 0)/1.11 = 9.01`. Node value = `0.4 × 35 − 9.01 = $4.99`.

Initial node, `S = 50`. Now use the two node values as the payoffs. Solve `70D − 1.11B = 33.96` and `35D − 1.11B = 4.99`. Subtracting: `35D = 28.97`, so `D = 0.8278` and `B = (35 × 0.8278 − 4.99)/1.11 = 21.61`. Call value = `0.8278 × 50 − 21.61 = $19.42`.

The call is worth $19.42 today, and you replicate it by buying 0.8278 shares and borrowing $21.61. (Source: Damodaran, Foundations of Finance Session 9.)

**Determinism:**
- DETERMINISTIC: everything in the backward induction. Inputs `(tree of stock prices, strike, riskless rate per period)` → `D`, `B`, and the option value at every node, and hence today's value. A script computes this exactly.
- JUDGMENT: constructing the tree in the first place — the size of the up and down moves and therefore the terminal nodes. Whether the preconditions for replication hold, particularly for real options on non-traded assets. Whether the price process is continuous or jump-prone. Whether early exercise is likely. These need a volatility estimate for the underlying, the contract's exercise terms, and the liquidity of both the asset and the option.

**Pitfalls:**
- Using replication-based pricing when the underlying is not traded. The arbitrage argument, and therefore the price, no longer holds strictly. This is the central weakness of real option valuation.
- Assuming the binomial model is more accurate because it looks more granular. Deriving realistic end nodes is the hard part, and a synthetic tree built from the asset's variance lands very close to Black-Scholes.
- Forgetting to check for early exercise at each node when valuing an American option.
- Applying Black-Scholes to an underlying whose price jumps. The limiting distribution is then Poisson, not normal, and the model's core assumption fails.
- Mixing up the sign of `B`. It is money borrowed for a call and money lent for a put.

**Sources:**
- `foundations_of_finance--valuing_options p.8-11, p.16`

**Related:** [[option-payoffs-and-value-determinants]], [[black-scholes-and-put-call-parity]], [[finance-first-principles]], [[real-options]]

# Backing out the market's implied probability of management change

**Core idea:** If a market price sits between a firm's status-quo value and its optimal value, the gap is not noise. It is the market's bet on the odds of management changing. Invert the expected-value-of-control identity and you can read that probability directly off the stock price. This turns an abstract governance question into a number you can test. If your own assessment of the odds differs from the market's, you have a position. The technique also measures events: compare the implied probability before and after an activist appears, and you see exactly how much the market repriced the odds.

**Formulas:**
- Forward identity: `Expected value per share = Status quo value per share + P × (Optimal value per share − Status quo value per share)`.
- Inverted: `P = (Market price per share − Status quo value per share) / (Optimal value per share − Status quo value per share)`.

Symbols: `P` = market-implied probability that management policies change; `Market price per share` = observed price; `Status quo value per share` = DCF value under existing management divided by shares outstanding; `Optimal value per share` = DCF value under restructured policies divided by shares outstanding.

Bounds and their meaning:
- `P ≤ 0` (price at or below status-quo value): the market assigns no chance of change, and the stock may be cheap even without a change.
- `0 < P < 1`: the normal case; the market prices partial odds.
- `P ≥ 1` (price above optimal value): the market either disagrees with your optimal value, sees value you have not modelled, or is simply overpricing the stock.

**Procedure:**
1. Build the status-quo DCF and divide by shares outstanding.
2. Build the restructured DCF and divide by shares outstanding.
3. Take the current market price per share.
4. Apply the inverted formula to solve for `P`.
5. Interpret the bounds. A `P` above 1 usually means your optimal value is too low or the market is pricing something outside your model — investigate before trading on it.
6. Compare `P` against your own assessment of the odds, built from governance structure, board composition, ownership and activist presence.
7. If your probability is higher than the market's and the value gap is large, the stock is attractive on governance grounds. If lower, the market has already paid for a change you doubt.
8. Re-run the calculation around events — an activist filing, a governance rule change, a hostile bid in the sector — to measure how much the odds moved.

**Reference data:**

Blockbuster, 2005, $ millions and per share:

| | Value of equity | Value per share |
|---|---|---|
| Status quo | $955 million | $5.13 |
| Optimally managed | $2,323 million | $12.47 |

Observed prices and the implied probabilities they carry:

| Date / condition | Price | Implied P |
|---|---|---|
| Before Carl Icahn's challenge | $8.20 | 41.8% |
| May 2005, after Icahn's successful challenge | $9.50 | 59.5% |

**Worked example:** Blockbuster's status-quo value is $5.13 per share and its optimal value is $12.47 per share, so the value gain from change is $7.34 per share.

At the May 2005 price of $9.50, solve `9.50 = 5.13 + P × (12.47 − 5.13)`. That gives `P = 4.37 / 7.34 = 59.5%`. The market was pricing roughly a 60% chance that Blockbuster's policies would change.

Before Carl Icahn arrived the stock traded at $8.20. The same arithmetic gives `P = (8.20 − 5.13) / 7.34 = 41.8%`. Icahn's successful challenge of management raised the market's assessed probability by about 18 percentage points, worth $1.30 per share. That is the value of activism, measured directly.

**Determinism:**
- DETERMINISTIC: the inversion itself. Given market price, status-quo value per share and optimal value per share, `P` is a single division. A script computes it, flags the out-of-bounds cases, and computes the change in `P` between two dates.
- JUDGMENT: both value inputs. The status-quo DCF and, especially, the optimal DCF carry all the usual estimation judgment. A wrong optimal value produces a wrong probability, so the technique is only as good as the restructuring case behind it.

**Pitfalls:**
- Treating `P` as an objective probability. It is a residual, and it absorbs every error in your two valuations.
- Reporting `P > 100%` as a very high probability. It is a signal that a valuation input is wrong.
- Using book values or analyst targets instead of your own two DCFs.
- Forgetting the share count. Both values must be per share, on the same share base, including or excluding options consistently.
- Reading a rising `P` as good news for a holder. A high implied probability means the change is already paid for; the upside is gone if the change is delivered and the downside is large if it is not.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.150`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.150`

**Related:** [[expected-value-of-control]], [[restructured-value-and-value-of-control]], [[status-quo-valuation]], [[voting-premium-and-minority-discount]], [[corporate-governance]]

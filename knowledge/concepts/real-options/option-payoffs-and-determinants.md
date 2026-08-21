# Option payoffs and the six determinants of option value

**Core idea:** Every real option in this material is mapped onto a plain call or put. A call pays off when the underlying asset rises above the strike. A put pays off when it falls below the strike. Both have a floor: the holder can walk away and lose only the premium. That truncated downside is why volatility *raises* the value of both calls and puts. Six variables drive option value, and knowing their directional effects lets you sanity-check any real-option number before you compute it.

**Formulas:**
- Call payoff at expiration: `max(S - K, 0)`. Net payoff subtracts the premium paid.
- Put payoff at expiration: `max(K - S, 0)`. Net payoff subtracts the premium paid.
- Symbols: `S` = price/value of the underlying asset at expiration; `K` = strike (exercise) price.
- Call breakeven on a net basis: `S = K + premium`. Put breakeven: `S = K - premium`.

**Procedure:**
1. Identify which side of the option you hold. If the payoff rises with the underlying, it is a call (option to delay, patent, undeveloped reserve, expansion option, equity in a levered firm). If it rises as the underlying falls, it is a put (option to abandon).
2. Name `S` and `K` explicitly in business terms. For a delay option, `S` = PV of project cash flows and `K` = initial investment. For an abandonment option, `S` = PV of remaining project cash flows and `K` = salvage value.
3. Draw or state the payoff: flat below (above) the strike, one-for-one above (below) it.
4. Before valuing, run the comparative statics in the table below. Ask whether each input moves the value in the direction your intuition expects. A real-option value that falls when you raise volatility signals an input or sign error.
5. Note two inputs that trip people up. **Variance raises BOTH call and put values.** **Dividends (any cash flow or value leakage from the underlying before exercise) lower call value and raise put value** — this is the "cost of delay" that appears in every real-option application here.

**Reference data:**

Six determinants of option value and the direction of their effect:

| # | Variable | Effect on CALL value | Effect on PUT value |
|---|---|---|---|
| 1 | Value of the underlying asset (S) | Increases | Decreases |
| 2 | Variance in value of the underlying (sigma^2) | Increases | Increases |
| 3 | Expected dividends on the asset (y) | Decreases | Increases |
| 4 | Strike price (K) | Decreases | Increases |
| 5 | Life of the option (t) | Increases | Increases |
| 6 | Level of interest rates (r) | Increases | Decreases |

Rationale for the non-obvious rows. Row 2: options have limited downside and depend on volatility for upside, so both sides gain. Row 3: dividends reduce the price appreciation of the underlying, which hurts the right to buy and helps the right to sell. Row 6: a higher rate makes the right to buy at a fixed future price more valuable and the right to sell at a fixed future price less valuable.

**Worked example:** Secure Mail's expansion option (see [[option-to-expand]]). The underlying is the PV of cash flows from entering the database software market, `S` = $226 million. The strike is the cost of entry, `K` = $500 million. The option is deep out of the money: `S` is less than half of `K`, so a static NPV test says the expansion is worth nothing today. Yet the option is worth $56 million. Two determinants do the work: an annualized standard deviation of 50% (row 2) and a five-year window before the right expires (row 5). Raise either and the $56 million rises; shorten the window toward zero and it collapses to `max(226 - 500, 0) = 0`.

**Determinism:** **DETERMINISTIC**: the payoff functions. Given `S`, `K`, and a premium, the payoff and breakeven are pure arithmetic. Given all six inputs and a model, the option value is arithmetic ([[black-scholes-model]], [[replicating-portfolio-and-binomial-model]]). **JUDGMENT**: every one of the six inputs when the underlying is a real asset. Estimating `S` requires a full DCF of the project. Estimating `sigma^2` requires choosing a proxy — comparable-firm variance, resource-price variance, or a capital-budgeting simulation. Estimating `y` requires a theory of how value leaks while you wait. Estimating `t` requires reading the legal or competitive window. The comparative statics themselves are directional facts, not estimates, and can be used to audit any of these choices.

**Pitfalls:**
- Assuming higher variance hurts a put. It helps both calls and puts.
- Forgetting the dividend/cost-of-delay term. Ignoring it overstates every call-type real option, sometimes badly, because real-option lives are long (17-year patents, 12-year relinquishment periods).
- Treating a deep out-of-the-money real option as worthless. With enough volatility and time it can carry large value — which is exactly why the exclusivity test in [[real-options-framework]] matters so much.
- Reading the net payoff diagram (which subtracts the premium) as the gross payoff used in valuation formulas.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.8-9, p.11
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.8-9, p.11

**Related:** [[real-options-framework]], [[black-scholes-model]], [[replicating-portfolio-and-binomial-model]], [[option-to-delay]], [[option-to-abandon]], [[option-to-expand]], [[equity-as-call-option]]

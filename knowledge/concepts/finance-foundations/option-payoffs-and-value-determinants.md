# Option Payoffs and the Determinants of Option Value

**Core idea:** An option gives its holder the right, but not the obligation, to buy or sell a set quantity of an underlying asset at a fixed strike price, at or before expiration. A call is the right to buy; a put is the right to sell. American options can be exercised any time during their life; European options only at expiration. The defining feature of both is asymmetry: the holder participates in favorable moves and simply walks away from unfavorable ones, losing at most the premium paid. That asymmetry is why volatility raises the value of both calls and puts, which is the single most counterintuitive fact in option pricing. For an option to exist at all, three ingredients are required: a clearly defined underlying asset whose value changes unpredictably, payoffs contingent on a specified event, and a finite period in which that event must occur.

**Formulas:**
- Call gross payoff at expiration: `max(S − K, 0)`. `S` = price of the underlying asset at expiration; `K` = strike (exercise) price.
- Call net payoff: `max(S − K, 0) − premium paid`. Downside is limited to the premium; upside is unlimited. The net payoff turns positive once `S > K + premium`.
- Put gross payoff at expiration: `max(K − S, 0)`.
- Put net payoff: `max(K − S, 0) − premium paid`. The payoff is highest when the asset price is lowest and flat-negative above the strike.
- Dividend yield: `y = dividends / current value of the asset`. Dividends reduce the price-appreciation component of the underlying.

**Procedure:**
1. Confirm the claim is genuinely option-like before reaching for an option model. Check all three ingredients: a defined underlying asset with unpredictable value, a payoff contingent on a specified event, and a finite expiration.
2. Classify it. Right to buy or right to sell? Exercisable throughout its life (American) or only at expiration (European)?
3. Write the payoff function explicitly as `max(S − K, 0)` or `max(K − S, 0)`, then subtract the premium to get the net payoff.
4. Identify the breakeven. For a call it is `K + premium`; for a put it is `K − premium`.
5. Before valuing, run the comparative statics to predict the direction of any input change. Use the table below. This catches sign errors in a model before they propagate.
6. Pay particular attention to volatility. If the analysis treats higher variance as reducing value, it is not treating the claim as an option.
7. Estimate the six inputs: value of the underlying, its variance, expected dividends, the strike, the time to expiration, and the riskless rate.

**Reference data:** Direction of effect on option value (Damodaran, Foundations of Finance Session 9):

| Variable increases | Effect on call value | Effect on put value | Why |
|---|---|---|---|
| Value of underlying asset | Up | Down | The right to buy at a fixed price gains; the right to sell loses |
| Variance in the underlying's value | Up | Up | Limited downside plus greater dispersion means more upside for both |
| Expected dividends on the underlying | Down | Up | Dividends reduce the price-appreciation component of the asset |
| Strike price | Down | Up | A higher fixed buy price is worse for a call, better for a put |
| Life of the option | Up | Up | More time for a favorable move, with the same capped downside |
| Riskless interest rate | Up | Down | The right to buy at a fixed *future* price gains as rates rise |

Grouping of the variables: three relate to the underlying asset (value, variance, dividends), two to the option contract (strike, life), and one to the market (interest rates).

**Worked example:** A call with a strike of `K = $40` on a stock currently at $50, in the two-period binomial setting Damodaran uses. At expiration the stock can end at $100, $50, or $25. The gross call payoffs are `max(100 − 40, 0) = $60`, `max(50 − 40, 0) = $10`, and `max(25 − 40, 0) = $0`. Note what the third outcome shows: a 50% fall in the stock from $50 to $25 costs the option holder only the premium, while the 100% rise to $100 pays $60. That is the asymmetry in numbers. A put with the same $40 strike would pay `max(40 − 100, 0) = $0`, `max(40 − 50, 0) = $0`, and `max(40 − 25, 0) = $15` in the same three states — the mirror image. (Source: Damodaran, Foundations of Finance Session 9.)

**Determinism:**
- DETERMINISTIC: the payoff at expiration, given `S`, `K`, and the premium. The breakeven price. The direction of every comparative static in the table.
- JUDGMENT: identifying whether a real-world claim is an option at all, which is the hard part with real options such as patents, undeveloped reserves, and expansion rights. Estimating the variance of the underlying, especially for a non-traded asset. Estimating the expected dividend yield and the option's effective life. These need the contract terms, a price history or a comparable asset for volatility, and a view on the payout policy of the underlying.

**Pitfalls:**
- Treating higher volatility as bad for the option holder. It raises the value of both calls and puts, because the downside is capped at the premium.
- Confusing gross and net payoff. A call that finishes in the money can still lose money if `S − K` is less than the premium.
- Forgetting the dividend effect. Dividends transfer value out of the underlying and away from call holders.
- Applying option machinery to a claim that lacks one of the three ingredients — most commonly a claim with no finite expiration, or no genuinely uncertain underlying.
- Assuming American and European options are interchangeable. Early exercise is common with real options, and it matters.

**Sources:**
- `foundations_of_finance--valuing_options p.2-7`

**Related:** [[replicating-portfolio-and-binomial-model]], [[black-scholes-and-put-call-parity]], [[finance-first-principles]], [[real-options]]

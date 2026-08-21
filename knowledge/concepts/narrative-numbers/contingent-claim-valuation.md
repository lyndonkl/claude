# Contingent claim (real option) valuation

**Core idea:** Some claims pay off only if an event happens, and a DCF built on expected cash flows understates them. A security can be valued as an option when it has three traits. Its value derives from an underlying asset that itself has value. Its payoff depends on where the underlying ends up against an exercise price. And it has a fixed life. Some claims are options by name — listed options, warrants, contingent value rights, LEAPs. Others are options in substance: equity in a deeply distressed firm, undeveloped natural-resource reserves, patents, and the right to expand into a new market. In the story process this is the treatment for the *possible* layer of a narrative — the part you cannot assign a probability to. See [[possible-plausible-probable]].

**Formulas:**
- Call payoff at expiration = max(S − K, 0). S = value of the underlying asset at expiration. K = strike (exercise) price.
- Put payoff at expiration = max(K − S, 0).
- Dilution-adjusted Black-Scholes value per call = S_adj × N(d1) − K × e^(−r×t) × N(d2). S_adj = the underlying price adjusted for dilution from new shares issued on exercise. r = riskless rate. t = maturity in years. N(d1), N(d2) = cumulative standard normal probabilities from the Black-Scholes d1 and d2 terms.
- Option value rises with the size of the possible market and with the exclusivity of the firm's access to it.

**Procedure:**
1. **Test the three traits.** Underlying asset with value; payoff contingent on an exercise price; fixed life. All three must hold or it is not an option.
2. **Value the underlying first.** Option pricing is an addendum, never a stand-alone approach. You cannot price the option on a project without a value and a variance for that project.
3. **Decide where the optionality is already counted.** If you raised the DCF growth rate because of the patent, you have already paid for it. Do not also add the patent's option value.
4. **Feed the option model.** Inputs: current value of the underlying, variance of that value, exercise price, life. For real options these are the hard part — projects do not trade.
5. **Add the option value to the DCF value, once.** For Uber in June 2014 the car-ownership market entered as option value of $2–3 billion on top of a $5.9 billion DCF value.
6. **Remember the sign of risk.** For an option-like claim, more variance raises value. That reverses the usual intuition, so state it explicitly when you present the number.

**Reference data:**

| Category | Examples |
|---|---|
| Direct options | Listed options (traded on an exchange); warrants (calls issued by the company itself, proceeds to the company); contingent value rights (puts issued by the firm, proceeds to the company); scores and LEAPs (long-term listed calls) |
| Indirect / real options | Equity in a deeply troubled firm with negative earnings and high leverage (a call on the firm's assets); natural-resource reserves (a call on the resource, since the firm chooses whether to extract); a patent or exclusive licence (a call on the product, for the patent's life); the right to expand an existing investment into new markets or products |

Advantages: option pricing lets you value claims nothing else can value — distressed equity, a no-revenue biotech. It also reframes value drivers, since variance becomes a positive.

Disadvantages: real-option inputs are hard to obtain; the approach is an addendum to another valuation; and double counting is easy.

**Worked example:** Uber, June 2014. The car-ownership market — people giving up owning cars — was classed as *possible* rather than probable. It was excluded from the DCF cash flows and added as option value. Damodaran's narrative produced $5.9 billion of failure-adjusted operating-asset value plus $2–3 billion of option value. Bill Gurley's narrative produced $53.4 billion plus $10 billion or more of option value. The option layer is a meaningful slice in both, and its size scales with the market being optioned.

**Determinism:**
- DETERMINISTIC: the payoff functions max(S−K,0) and max(K−S,0); the Black-Scholes value given S, K, t, sigma, r and a dilution adjustment.
- JUDGMENT: whether a claim really has the three option traits; the value and variance of a non-traded underlying; the effective life; and above all whether the optionality has already been embedded in the DCF.

**Pitfalls:**
- Double counting. Raising DCF growth for a patent *and* adding the patent's option value counts it twice.
- Treating option pricing as a stand-alone method when it always sits on top of another valuation.
- Guessing a variance for a project that does not trade and presenting the result as precise.
- Using option value as a rescue for a story that fails the possible/plausible/probable test. Option value is the right home for genuinely unassessable upside, not for wishful growth.

**Sources:**
- valintrospr21 p.18-23
- valintrospr20 p.18-23
- valintrospr20-repost p.18-23
- valpacket1spr21 p.261, p.263, p.272 (possible layer → option value; Uber option value)
- valpacket1spr20 p.257, p.259, p.268

**Related:** [[three-approaches-to-valuation]], [[possible-plausible-probable]], [[uber-narrative-valuation]], [[narrative-updating-feedback-loop]]

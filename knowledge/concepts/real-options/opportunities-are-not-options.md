# Opportunities are not options: scaling option value for exclusivity

**Core idea:** Black-Scholes will return a positive number for any opportunity you feed it. That number is not the value you can claim. Damodaran's caution is that an *opportunity* becomes a valuable *option* only under three conditions, each of which is a sliding scale rather than a yes/no. The first investment must be a prerequisite for the second. You must have some competitive advantage on the second investment. And the second investment must earn excess returns. Where any scale sits at zero, the computed option value collapses to zero regardless of what the model says. This is the practical form of the exclusivity test, and it is the single most common place where real-options analysis is abused.

**Formulas:**
- `Claimed option value = Model option value x Exclusivity factor`
- The exclusivity factor runs from 0 to 1 and is set by judgment along the three scales below. Zero competitive advantage → factor 0. Exclusive right → factor 1.
- Zero-value conditions (either is sufficient): no competitive advantage on the second investment, or zero excess returns on the second investment.
- Excess return, the quantity that must be positive and sustainable: `Excess return = Return on capital on the second investment - Cost of capital`.

**Procedure:**
1. **Scale 1 — Is the first investment necessary for the second?** Place it between "not necessary" and "pre-requisite". If the firm could take the second investment without the first, the first buys no option and the premium is zero.
2. **Scale 2 — Competitive advantage on the second investment.** Place it between "zero competitive advantage" (option has no value) and "exclusive right" (firm captures 100% of option value). Use the barrier ladder in the reference table to locate the case.
3. **Scale 3 — Excess returns on the second investment.** Place it between "zero excess returns" (option has no value) and "large sustainable excess returns" (option has high value). A second investment that earns exactly its cost of capital produces no option value, however volatile it is.
4. Combine the three readings into a single exclusivity factor between 0 and 1. Be explicit about it in writing — an unstated factor of 1.0 is the default error.
5. Multiply the modelled option value by the factor and add only that to the DCF value.
6. If any scale reads zero, add nothing. Do not compromise at "a bit of value anyway".

**Reference data:**

Barriers to entry, ordered from weakest to strongest competitive advantage. The stronger the barrier, the larger the share of option value the firm can claim.

| Rank | Barrier | Typical exclusivity |
|---|---|---|
| 1 (weakest) | First-mover advantage | Very low; easily eroded |
| 2 | Technological edge | Low; competitors catch up |
| 3 | Brand name | Moderate |
| 4 | Telecom licences | High; legally granted |
| 5 (strongest) | Pharmaceutical patents | Highest; legally granted and enforced |

The three sliding scales:

| Scale | Zero-value end | Full-value end |
|---|---|---|
| Necessity of the first investment | Not necessary | Pre-requisite |
| Competitive advantage on the second investment | Zero competitive advantage → no option value | Exclusive right → 100% of option value |
| Excess returns on the second investment | Zero excess returns → no value | Large sustainable excess returns → high value |

**Worked example:** Secure Mail's option to enter database software, modelled at $56 million in [[option-to-expand]]. Run the three scales.

*Scale 1.* Is the anti-virus business a prerequisite for entering database software? Partly. The customer base and technology transfer, but a well-funded entrant could enter the database market without owning an anti-virus company. This sits mid-scale, not at "pre-requisite".

*Scale 2.* What is the barrier? Customer relationships and technological edge — ranks 2 and 3 on the ladder, well below a telecom licence or a pharmaceutical patent.

*Scale 3.* Would database software earn excess returns for Secure Mail? That requires a view on whether it can out-earn its cost of capital in a market it has never operated in.

Verdict: the honest claimed value is materially below $56 million. By contrast, run the same three scales on Biogen's Avonex patent ([[patent-valuation-as-option]]): the patent is a legal prerequisite, sits at rank 5 on the barrier ladder, and the drug earns large excess returns. There the factor sits close to 1, and the $907 million is defensible.

**Determinism:** **JUDGMENT throughout.** This concept exists precisely to gate a deterministic computation with a non-computable assessment. Locating a case on the three scales takes several kinds of knowledge. You need the industry's competitive structure. You need the legal or contractual protections in place and how long they last. You need to know whether rivals have substitute routes to the same market. And you need a view on whether the second investment can out-earn its cost of capital. The only **DETERMINISTIC** step is the multiplication `model value x factor`, and it is arithmetically trivial. There is no data feed that returns the exclusivity factor.

**Pitfalls:**
- Defaulting the exclusivity factor to 1.0 by never mentioning it. Every unqualified real-option premium does this implicitly.
- Confusing "we have a head start" with an option. First-mover advantage is the weakest barrier on the ladder.
- Ignoring the excess-return condition. A perfectly exclusive right to a business that earns exactly its cost of capital is worth nothing.
- Using volatility to rescue a case with no barriers. High variance multiplies zero.
- Letting "strategic options" or "real options" serve as a buzzword to justify a price already agreed. The burden of proof sits with the party arguing for the premium.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.48
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.48

**Related:** [[option-to-expand]], [[real-options-framework]], [[patent-valuation-as-option]], [[financing-flexibility-option]], [[excess-returns-and-value-creation]], [[competitive-advantage-period]]

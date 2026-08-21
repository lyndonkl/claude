# Real options — concept index

Source: Damodaran, *Valuation Packet 3: Real Options, Acquisition Valuation and Value Enhancement*, Spring 2020 and Spring 2021 editions, pages 3-83. The two editions teach this module identically; each note below merges them.

## Concepts

| Slug | Covers | Determinism |
|---|---|---|
| [[real-options-framework]] | The premium claim, the four real options, and the three sequential tests (option test, exclusivity test, pricing test) that gate any real-option premium | JUDGMENT |
| [[option-payoffs-and-determinants]] | Call and put payoff functions; the six determinants of option value and the direction of each effect | MIXED (payoffs deterministic, inputs judgment) |
| [[replicating-portfolio-and-binomial-model]] | Replication, the option delta, node-by-node backward induction, limiting distributions (normal vs Poisson), binomial-vs-Black-Scholes model choice | MIXED (tree arithmetic deterministic, tree construction judgment) |
| [[black-scholes-model]] | The Black-Scholes call formula, the dividend-adjusted call and put used for every real option here, and the full N(d) lookup table | MIXED (formula deterministic, all six inputs judgment) |
| [[decision-trees-vs-option-pricing]] | Staged-investment intuition, roll-back mechanics, the Copeland and riskfree reconciliations, the FDA-pipeline pharma tree | MIXED (roll-back deterministic, tree and discount rates judgment) |
| [[option-to-delay]] | Exclusive rights as a call on the project; why negative NPV today does not make the rights worthless; the 1/n cost of delay | MIXED |
| [[patent-valuation-as-option]] | Product patents as calls; input mapping; the Avonex/Biogen valuation; optimal exercise timing; the three-test verdict for patents | MIXED (valuation deterministic, S and sigma judgment) |
| [[valuing-a-firm-with-patents]] | Three-part firm value: DCF of commercial products + option value of patents + excess value from future R&D; the full Biogen sum-of-parts | MIXED (arithmetic deterministic, value multiple and window judgment) |
| [[natural-resource-options]] | Undeveloped reserves as calls; the development-lag adjustment; net production revenue as dividend yield; the Gulf Oil valuation | MIXED (chain deterministic, reserves and variance judgment) |
| [[option-to-expand]] | Strategic options as calls on future expansion; the Secure Mail start-up valuation; why expansion-option estimates are the noisiest | MIXED |
| [[opportunities-are-not-options]] | The three sliding scales (prerequisite, competitive advantage, excess returns) and the barrier ladder used to scale computed option value down | JUDGMENT |
| [[option-to-abandon]] | Exit rights as puts; the Airbus/Lear joint venture; the 1/n project-life yield; cost-flexibility implications for company selection | MIXED |
| [[financing-flexibility-option]] | Excess debt capacity and cash as a call on reinvestment needs; security design; the Disney valuation of flexibility against its cost | MIXED (mostly deterministic from history plus a WACC schedule) |
| [[equity-as-call-option]] | Residual claim plus limited liability as a call on the firm; the base $100m/$80m example; implied debt value and implied interest rate | MIXED (valuation deterministic, firm value and variance judgment) |
| [[distressed-equity-time-value]] | Why a catastrophic value drop does not wipe out equity; loss sharing with debtholders; the sensitivity table down to $10m firm value | MIXED |
| [[risk-shifting-and-stockholder-bondholder-conflict]] | Why levered equity holders take risky negative-NPV projects; the -$2m NPV / 40%-to-50% volatility example and the wealth transfer | MIXED |
| [[conglomerate-merger-wealth-transfer]] | Why a fairly priced diversifying merger hurts stockholders; the combined-variance formula; the $2.98m transfer to bondholders | MIXED (formulas deterministic, correlation judgment) |
| [[equity-option-inputs-troubled-firms]] | Workarounds for the model's four broken assumptions; firm-value variance from stock and bond volatilities; weighted duration; the Eurotunnel valuation | MIXED (formulas deterministic, DCF assumptions judgment) |

## How these connect, and the order to use them

Start with **[[real-options-framework]]**. It is a gate, not a technique: three sequential tests decide whether any option premium is admissible at all, and most real options fail the second one. Only after passing the gate do you reach for machinery.

The machinery layer is three notes. **[[option-payoffs-and-determinants]]** tells you which side of the option you hold. It also tells you how each input should move the answer, so use it to audit every number you later produce. **[[replicating-portfolio-and-binomial-model]]** and **[[black-scholes-model]]** are the two pricing engines. Prefer the binomial engine when early exercise or jumps matter, which is the normal case for real assets. **[[decision-trees-vs-option-pricing]]** is the alternative route when the pricing test fails but genuine optionality exists. It also carries the core intuition of the module: staging an investment so you can learn and stop turns a bad bet into a good one.

Then work through the four project-level options in the packet's order. **[[option-to-delay]]** is the general form. **[[patent-valuation-as-option]]** and **[[natural-resource-options]]** are its two concrete applications, and the ones where the three tests come closest to passing. **[[valuing-a-firm-with-patents]]** aggregates patent options into a whole-firm valuation. That is where the double-counting discipline bites. **[[option-to-expand]]** is the weakest application. Read it alongside **[[opportunities-are-not-options]]**, which supplies the scaling factor that keeps expansion premiums honest. **[[option-to-abandon]]** is the only put in the set. It is also the one that most often flips a live investment decision.

The capital-structure applications come last. **[[financing-flexibility-option]]** prices the option to take unanticipated projects against the cost of staying below the optimal debt ratio. **[[equity-as-call-option]]** re-reads the balance sheet itself as an option. Three consequences follow directly. **[[distressed-equity-time-value]]** explains why bankrupt firms' stock trades above zero. **[[risk-shifting-and-stockholder-bondholder-conflict]]** explains why levered equity holders gamble. **[[conglomerate-merger-wealth-transfer]]** explains why a fairly priced diversifying merger still hurts stockholders. **[[equity-option-inputs-troubled-firms]]** closes the loop. It supplies the real-world estimation procedures and the Eurotunnel example that puts them together.

One thread runs through every concept. The arithmetic is almost always mechanical; the inputs almost never are. Take any worked example here — Avonex, Gulf Oil, Secure Mail, Airbus, Disney, Eurotunnel. A script could reproduce the final number exactly from the stated inputs. The whole analytical burden sits in producing those inputs, and in deciding whether the option deserved to be valued at all.

# Real options framework: the three tests

**Core idea:** Real-option advocates claim that traditional discounted cash flow (DCF) valuation underestimates investments with embedded options. They argue you should pay a *premium* on top of a DCF value. Four such options recur. **Delay**: defer the investment. **Flexibility**: alter production schedules as prices change. **Expansion**: enter new markets or products after favorable early outcomes. **Abandonment**: stop if early outcomes are bad. Damodaran allows the premium only when three sequential tests pass: an option genuinely exists, it has significant economic value, and an option pricing model can price it. Real options are everywhere. Most are worth nothing, because anyone can exercise them. The lasting payoff of real-options thinking is not the numeric premium. It is the recognition that building flexibility and escape hatches into large decisions has value. It also explains why firms behave as they do in investment analysis and capital-structure choices.

**Formulas:**
- No single formula; the framework is a gate on whether the option-pricing formulas in [[black-scholes-model]] and [[replicating-portfolio-and-binomial-model]] may be applied at all.
- Adjusted value with an option premium: `Value = DCF value of assets in place + Value of embedded real option(s)`, where the second term is admitted only if all three tests below are passed.
- Scaling rule for partial exclusivity: `Claimed option value = Full option value x Exclusivity factor`, where the exclusivity factor runs from 0 (perfect competition) to 1 (complete exclusivity).

**Procedure:**
1. **Test 1 — Is there an option embedded in this action?** An option is the right (not obligation) to buy or sell a specified quantity of an underlying asset at a fixed strike/exercise price at or before expiration. Require BOTH: (a) a clearly defined underlying asset whose value changes over time in unpredictable ways, and (b) payoffs that are contingent on a specified event occurring **within a finite period**. Write down explicitly: what is the underlying asset? what is the contingency under which a payoff occurs? If you cannot name both, stop — there is no option and no premium.
2. **Test 2 — Does the option have significant economic value?** The test is *restriction on competition*. In a perfectly competitive product market, no contingency, however positive, generates positive NPV, because competitors compete the excess returns away — so the option is worth zero no matter how volatile the underlying. Classify: full exclusivity (you and only you can exploit the contingency) → full option value; no barriers to competition → zero option value; partial barriers → scale the value down in proportion.
3. **Test 3 — Can an option pricing model value it?** Option pricing rests on a replicating portfolio and arbitrage. Score three conditions: (a) is the underlying asset traded (giving observable prices and volatility and permitting replication)? (b) is there an active marketplace for the option itself? (c) is the cost of exercising known with some certainty? Trust the model output roughly in proportion to how many hold. When they fail — as they typically do for real assets — value estimates are far more imprecise and can deviate dramatically from any market price, because arbitrage cannot enforce discipline.
4. If all three pass, price the option. Prefer the binomial model when early exercise matters or values jump; see [[replicating-portfolio-and-binomial-model]].
5. If Test 1 or Test 2 fails, add **nothing** to the DCF value. If Test 3 fails but Tests 1 and 2 pass, use a decision tree instead ([[decision-trees-vs-option-pricing]]) and treat any numeric option value as an order-of-magnitude indication, not a price.
6. Guard against double counting: if you value an option separately (a patent, an expansion opportunity), remove the corresponding optimism (high growth rate, hoped-for new markets) from the DCF piece.

**Reference data:**

Taxonomy of real options taught in the packet, with the option type and where each is developed:

| Real option | Option type | Underlying asset | Strike | Concept note |
|---|---|---|---|---|
| Option to delay / defer | Call | PV of project cash flows | Initial investment | [[option-to-delay]] |
| Product patent | Call | PV of cash flows from the drug/product | PV of development cost | [[patent-valuation-as-option]] |
| Undeveloped natural resource reserve | Call | Value of the reserve | Development cost | [[natural-resource-options]] |
| Option to expand | Call | PV of cash flows from expansion | Cost of expansion | [[option-to-expand]] |
| Option to abandon | Put | PV of remaining project cash flows | Salvage / abandonment value | [[option-to-abandon]] |
| Financing flexibility | Call | Actual reinvestment needs | Fundable reinvestment needs | [[financing-flexibility-option]] |
| Equity in a levered firm | Call | Value of the firm's assets | Face value of debt | [[equity-as-call-option]] |

Exclusivity ladder (weakest to strongest barrier to competition, and hence lowest to highest share of option value captured):

| Rank | Barrier |
|---|---|
| 1 (weakest) | First-mover advantage |
| 2 | Technological edge |
| 3 | Brand name |
| 4 | Telecom licenses |
| 5 (strongest) | Pharmaceutical patents |

**Worked example:** Biogen's patent on Avonex, a multiple sclerosis drug.

- *Test 1.* The underlying asset is the drug Biogen would develop. The contingency: if the PV of cash flows from development exceeds development cost, Biogen develops and earns the difference. Otherwise it shelves the patent and earns zero. An option exists.
- *Test 2.* The patent bars competitors from developing a *similar* product. It does not stop them developing *other* products to treat the same disease. Exclusivity is real but partial.
- *Test 3.* The underlying product is not traded. So PV and volatility must be estimated, and no replicating position or arbitrage is possible. The patent itself is bought and sold, though less often than oil reserves or mines. The exercise cost of converting the patent to commercial production can be estimated fairly precisely by experienced drug firms.
- *Verdict.* The option value can be estimated. But it is only as good as the underlying capital budgeting. The approach works best for a publicly traded firm whose value comes mostly from one or a few patents. There you can use the firm's own market value and its variance as option inputs. See [[patent-valuation-as-option]] for the resulting $907 million.

**Determinism:** The three tests are entirely **JUDGMENT**. Test 1 requires identifying an underlying asset and articulating a contingency with a finite horizon — that is a reading of the business and the contract/legal structure. Test 2 requires assessing competitive structure: how many firms could exploit the same contingency, what legal or economic barriers exist, and how long they last. Test 3 requires assessing whether the underlying trades, whether the option trades, and whether exercise cost is knowable. Nothing here is computable from a data feed. What IS **DETERMINISTIC**, once the tests are passed and inputs supplied, is the option value itself (Black-Scholes or binomial arithmetic) and the summation `DCF value + option value`.

**Pitfalls:**
- Paying a real-option premium on a DCF value without running the exclusivity test. Most real options are worth nothing precisely because there is no exclusivity — anyone can exercise them, and competition eliminates the excess return.
- Confusing volatility with value. High variance raises option value only when there is a restriction on competition; in a perfectly competitive market no contingency produces positive NPV regardless of volatility.
- Applying option pricing models to real assets and then quoting the output to the dollar. The underlying is not traded, replication is impossible, and no arbitrage disciplines the estimate — errors are far larger than in financial-option pricing.
- Double counting: valuing patents (or an expansion opportunity) as options while also building the growth those same patents would produce into the DCF of existing products.
- Treating "real options" as a buzzword that justifies a price already decided on. Damodaran lists "real options" alongside "synergy" (1980s) and "strategic considerations" (1990s) as premium-justifying language of the 2000s; the burden of proof belongs on the party arguing for the premium.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.3, p.6-7, p.10, p.12, p.23-24, p.83
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.3, p.6-7, p.10, p.12, p.23-24, p.83

**Related:** [[option-payoffs-and-determinants]], [[replicating-portfolio-and-binomial-model]], [[black-scholes-model]], [[decision-trees-vs-option-pricing]], [[option-to-delay]], [[option-to-expand]], [[option-to-abandon]], [[opportunities-are-not-options]], [[patent-valuation-as-option]], [[natural-resource-options]], [[financing-flexibility-option]], [[equity-as-call-option]], [[dcf-valuation]], [[value-of-control]], [[synergy-valuation]]

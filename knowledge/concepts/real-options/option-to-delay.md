# The option to delay (option to defer)

**Core idea:** Traditional investment analysis is static. It asks only whether a project is good *if taken today*. When a firm holds exclusive rights to a project or product for a specific period, that framing is wrong. A project that fails today's test — negative NPV, or IRR below the hurdle rate — does not make the *rights* worthless. Circumstances may change before exclusivity expires, and the firm can wait. The rights are therefore a call option: the underlying asset is the present value of the project's expected cash flows, and the strike is the initial investment required.

**Formulas:**
- Payoff from the delay option at any point: `max(V - I, 0)`
  - `V` = present value of expected cash flows from taking the project
  - `I` = initial investment required to take the project
- Equivalently: `Payoff = V - I if V > I; 0 if V <= I`. Note `V - I` is exactly the project's NPV, so the option pays off precisely when NPV turns positive.
- Option value from the dividend-adjusted Black-Scholes call (see [[black-scholes-model]]):
  - `C = V x e^(-y*t) x N(d1) - I x e^(-r*t) x N(d2)`
  - `t` = remaining period of exclusive rights; `y` = annual cost of delay; `sigma^2` = variance in `ln(V)`; `r` = riskless rate matched to `t`.
- Cost-of-delay heuristic: `y = 1/n`, where `n` = number of years of exclusivity remaining. Each year of delay means one less year of value-creating cash flows.

**Procedure:**
1. Confirm exclusivity. Without exclusive rights for a defined period there is no delay option — a competitor takes the project and the contingency yields no excess return. Run the exclusivity test in [[real-options-framework]].
2. Set `V` = the PV of expected cash flows from taking the project **now**. This is a full DCF of the project. Noise in this estimate is not a problem for the option value; it is a source of it.
3. Set `I` = the initial investment required, expressed in present-value dollars and assumed constant over the option's life.
4. Set `t` = the length of the exclusive rights (patent life, licence term, contractual window).
5. Set `sigma^2` = variance in `ln(V)`. Use variance in cash flows or values of similar assets/firms, or the variance in present value produced by a capital-budgeting simulation.
6. Set `y` = the annual cost of delay. Default to `1/n`.
7. Compute the call value. Compare it with the static NPV `V - I`.
8. Apply the exercise rule. Hold the option while its computed value exceeds the value from exercising immediately (`V - I`). Exercise — take the project — once the option value falls below `V - I`. See [[patent-valuation-as-option]] for the timing chart.
9. If the option value exceeds zero but `V - I` is negative, the rights are worth holding even though the project is currently unattractive.

**Reference data:**

Mapping from business facts to option inputs for a delay option:

| Option input | Business meaning | Estimation route |
|---|---|---|
| `S` (underlying value) | PV of cash inflows from taking the project now | Full DCF of the project |
| `K` (strike) | Cost of making the investment | Capital-budgeting cost estimate, constant in PV dollars |
| `t` (life) | Remaining period of exclusive rights | Patent life, licence term, relinquishment period |
| `sigma^2` (variance) | Variance in `ln(project value)` | Comparable assets/firms, or capital-budgeting simulation |
| `y` (dividend yield) | Cost of delay | `1/n`, `n` = years of exclusivity remaining |
| `r` (riskless rate) | Riskless rate for the option's life | Government bond of matching maturity |

**Worked example:** Biogen's Avonex patent. `V` = $3,422 million, `I` = $2,875 million, so the static NPV of developing today is about $547 million and the project is already positive. `t` = 17 years, `y` = 1/17 = 5.89%, `sigma^2` = 0.224, `r` = 6.7%. The delay option is worth $907 million — roughly $360 million more than exercising today. That gap is the value of waiting. Full computation in [[patent-valuation-as-option]].

**Determinism:** **DETERMINISTIC**: the payoff function `max(V - I, 0)`; the cost-of-delay heuristic `y = 1/n`; the Black-Scholes arithmetic once all six inputs are fixed; the comparison of option value against `V - I` that produces the exercise decision. **JUDGMENT**: whether exclusivity exists and for how long — this is a legal and competitive reading, and it sets both `t` and whether the option has any value at all. Also judgment: the DCF that produces `V`; the choice of volatility proxy; whether `I` really stays constant in PV dollars over a 17-year window; and whether `1/n` is the right description of how value leaks while you wait.

**Pitfalls:**
- Concluding that a negative-NPV project means worthless rights. That is the specific error this concept corrects.
- Claiming a delay option without exclusivity. If competitors can take the same project, waiting destroys value rather than creating it.
- Holding the option past its optimal exercise point. The cost of delay grows relative to time value as expiry nears; there is a crossover after which waiting destroys value.
- Assuming `I` is fixed for a 17-year option. Development costs evolve; the constant-strike assumption is a simplification, not a fact.
- Double counting: valuing the rights as an option and also assuming the project's cash flows in the DCF of the firm.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.24-26, p.29
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.24-26, p.29

**Related:** [[real-options-framework]], [[patent-valuation-as-option]], [[natural-resource-options]], [[black-scholes-model]], [[option-payoffs-and-determinants]], [[npv-and-investment-decision-rules]]

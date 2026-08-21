# The option to abandon

**Core idea:** A firm may hold the right to abandon a project if cash flows do not measure up. If abandoning saves it from further losses, that right makes the project more valuable. The structure is a put. The underlying asset is the present value of the project's remaining cash flows. The strike is the salvage or abandonment value. Below the salvage value the firm exits and collects the strike; above it, the firm continues. The practical consequence is large: an abandonment option can turn a negative-NPV project into one worth taking, and it changes how you should value companies with different cost structures.

**Formulas:**
- Abandonment payoff: `max(Salvage value - PV of remaining project cash flows, 0)`.
- Put value (dividend-adjusted Black-Scholes):
  - `P = K x e^(-r*t) x (1 - N(d2)) - S x e^(-y*t) x (1 - N(d1))`
  - `d1 = [ln(S/K) + (r - y + sigma^2/2) x t] / (sigma x sqrt(t))`, `d2 = d1 - sigma x sqrt(t)`
- Symbols: `S` = PV of cash flows from the project; `K` = salvage value from abandonment; `t` = life of the abandonment option (how long the exit right lasts); `sigma^2` = variance in the PV of project cash flows; `y` = dividend yield capturing the annual erosion of project PV; `r` = riskless rate matched to `t`.
- Dividend-yield heuristic for a finite-life project: `y = 1/n`, where `n` = project life in years. The project's PV drops by roughly `1/n` each year as cash flows are paid out.
- Decision rule: `NPV with abandonment option = Static NPV + Put value`. Take the project if this is positive.

**Procedure:**
1. Identify the exit right and its source. It must be a real, enforceable right: a contractual buyout, a put to a partner, a resale market with a known price. A vague ability to "walk away" is not an abandonment option.
2. Set `S` = the firm's share of the PV of expected cash flows from the project.
3. Set `K` = the salvage or abandonment value the firm would receive on exit.
4. Set `t` = the period over which the exit right is exercisable. This is usually much shorter than the project life. Do not confuse the two.
5. Set `sigma^2` = the variance in the PV of project cash flows. A Monte Carlo simulation of the project's cash flows is the standard route.
6. Set `y = 1/n` where `n` is the **project** life, not the option life.
7. Set `r` = a government bond rate matching `t`.
8. Compute the put value.
9. Add it to the static NPV. If the total is positive, take the project even though the standalone NPV is negative.
10. Feed the insight back into structuring. When negotiating a joint venture or a large project, deliberately build in the exit right; it has quantifiable value.

**Reference data:**

Input mapping for an abandonment option:

| Option input | Business meaning | Note |
|---|---|---|
| `S` | PV of the firm's share of project cash flows | From the project DCF |
| `K` | Salvage / abandonment value | Contractual buyout price, or resale value |
| `t` | Life of the abandonment option | Duration of the exit right, not the project life |
| `sigma^2` | Variance in PV of project cash flows | Typically from a simulation |
| `y` | Annual erosion of project PV | Heuristic `1/n`, `n` = project life |
| `r` | Riskless rate | Government bond matched to `t` |

Valuation implications for company selection (other things equal, attach more value to firms with):

| Feature | Why it raises abandonment option value |
|---|---|
| More cost flexibility — more variable costs, fewer fixed costs | Lowers the loss from shutting down, raising the effective salvage value |
| Fewer long-term contracts / obligations with employees and customers | Long-term commitments add directly to the cost of abandoning |

Both features cost the firm some value in normal operation. That cost must be weighed against the increase in the abandonment option's value.

**Worked example:** Airbus and Lear Aircraft joint venture.

Airbus is considering a joint venture with Lear Aircraft to produce a small commercial airplane (40-50 passengers, short haul). Airbus must invest $500 million for a 50% share. Its share of the PV of expected cash flows is $480 million, so the static NPV is **-$20 million**. Lear offers to buy Airbus's 50% share any time over the next five years for $400 million if Airbus decides to exit. A simulation of the cash flows yields a variance in PV of 0.16. The project has a life of 30 years.

| Input | Value |
|---|---|
| `S` = PV of cash flows from project | $480 million |
| `K` = salvage value from abandonment | $400 million |
| `sigma^2` = variance in underlying asset value | 0.16 |
| `t` = life of the abandonment option | 5 years |
| `y` = 1 / project life = 1/30 | 0.033 |
| `r` = five-year riskless rate | 6% |

`N(d1)` = 0.7882, `N(d2)` = 0.4624.

`P = 400 x e^(-0.06 x 5) x (1 - 0.4624) - 480 x e^(-0.033 x 5) x (1 - 0.7882) = $73.23 million`.

Decision: `NPV with abandonment option = -20 + 73.23 = +$53.23 million`. Airbus should enter the joint venture. The exit right, not the aircraft economics, is what makes the deal worth doing.

**Determinism:** **DETERMINISTIC**: the payoff rule; the `1/n` dividend-yield heuristic; the Black-Scholes put value given `(S, K, t, sigma, y, r)`; the addition `static NPV + put value` and the resulting accept/reject decision. A script computes $73.23 million and $53.23 million from the table above. **JUDGMENT**: the variance of 0.16, which comes out of a simulation whose distributional assumptions are themselves estimates. The PV of $480 million for Airbus's share. Whether the exit right is genuinely enforceable and for exactly five years. Whether `1/n` describes this project's value decay — a 30-year aircraft program does not shed value evenly. And the qualitative company-selection implications, which are entirely a matter of reasoning about cost structure and contractual commitments.

**Pitfalls:**
- Using the project life as the option life. Here the project runs 30 years but the exit right lasts only 5. Using 30 would massively overstate the put.
- Using the option life in the `1/n` yield. The heuristic uses the **project** life (30), giving `y` = 0.033.
- Claiming an abandonment option with no counterparty. Somebody must be obliged to buy, or there must be a liquid resale market at a known price.
- Ignoring the cost of the flexibility. Shifting to variable costs and avoiding long-term contracts is not free; the direct cost must be weighed against the option value gained.
- Adding the put value to a project whose NPV already assumes an orderly wind-down. That double counts the exit.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.50-54
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.50-54

**Related:** [[real-options-framework]], [[black-scholes-model]], [[option-payoffs-and-determinants]], [[decision-trees-vs-option-pricing]], [[option-to-expand]], [[simulation]], [[operating-leverage]]

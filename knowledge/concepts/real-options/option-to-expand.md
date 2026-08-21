# The option to expand

**Core idea:** Taking a project today may create the opportunity to take other valuable projects later. If it does, a project with negative NPV can still be worth taking, because the option it creates more than compensates. Firms call these "strategic options" and use them to justify negative-NPV or negative-return investments. The structure is a call. The underlying asset is the present value of cash flows from the future expansion. The strike is the additional investment needed to expand. The life is the window during which the firm can still enter. This is the standard way to value a young company whose DCF looks small relative to its ambitions.

**Formulas:**
- Expansion payoff: `max(V_exp - I_exp, 0)`
  - `V_exp` = PV of expected cash flows from the expansion
  - `I_exp` = additional investment required to expand
- Option value (Black-Scholes call): `C = S x N(d1) - K x e^(-r*t) x N(d2)` with `S = V_exp`, `K = I_exp`, `t` = window over which the firm has the right to enter, `sigma` = volatility of value in the target business, `r` = riskless rate matched to `t`.
- Underlying value as an annuity of expansion cash flows: `S = CF x (1 - (1 + k)^(-n)) / k`, with `CF` = expected annual after-tax cash flow, `k` = cost of capital for that business, `n` = years of cash flows.
- Total value: `Value of company = DCF value of existing business + Value of the option to expand`.
- Adjust for partial exclusivity: `Claimed value = C x Exclusivity factor` — see [[opportunities-are-not-options]].

**Procedure:**
1. Confirm the first investment is a **prerequisite** for the second. If the firm could enter the second market without doing the first project, the first project is not buying an option.
2. Define the expansion precisely: which market, which product, what it would cost, what it would earn. Vagueness here is the main reason expansion-option numbers are unreliable.
3. Estimate `S`. Project the expansion's after-tax cash flows and discount them at a cost of capital appropriate to **that** business, not the current one. An annuity is often adequate.
4. Estimate `K` = the cost of entering the new market today. Note it may evolve over time, which the constant-strike assumption ignores.
5. Set `t` = the period over which the firm realistically retains the right or ability to enter.
6. Set `sigma` from the volatility of firm values in the target industry — typically the annualized standard deviation of value at publicly traded firms in that business.
7. Set `r` = a government bond rate matching `t`.
8. Value the call.
9. Run the exclusivity screen before adding it. Assess competitive advantage on the second investment and whether that investment earns excess returns. Scale the option value down accordingly.
10. Add the scaled option value to the DCF value of the existing business.

**Reference data:**

The three-test verdict for expansion options:

| Test | Verdict |
|---|---|
| Option test | Passes if the first investment is a prerequisite. Underlying = the expansion project; payoff = `PV of expansion CF - expansion cost` if positive, else 0. |
| Exclusivity test | Varies widely. Strong: exclusive government licences. Weaker: brand name, market knowledge. Weakest: first-mover advantage. |
| Pricing test | Weak. Underlying not traded, so value and volatility must be estimated. Licences sometimes trade; diffuse expansion options do not. Exercise cost is not known precisely and may evolve over time. |
| Overall | Option pricing yields extremely noisy estimates for expansion options and may attach inappropriate premiums to DCF values. |

Barrier-strength ranking used to scale the value: exclusive licences > brand name / market knowledge > first mover.

**Worked example:** Secure Mail, a small anti-virus software company.

DCF value of the existing anti-virus business: $115 million. Secure Mail could use its customer base and technology to enter database software within the next 5 years.

| Input | Value | Derivation |
|---|---|---|
| `S` | $226 million | PV of $40 million/year after-tax for 10 years at 12% = `40 x (1 - 1.12^(-10)) / 0.12` |
| `K` | $500 million | Cost of developing the database program today |
| `t` | 5 years | Window during which entry is feasible |
| `sigma` | 50% | Annualized std deviation in firm value at publicly traded database companies |
| `r` | 3% | Five-year treasury bond rate |
| `k` (for the annuity) | 12% | Cost of capital for private database-software companies |

Call value = **$56 million**.

| Component | $ millions |
|---|---|
| DCF valuation of the firm | 115 |
| Value of option to expand into database market | 56 |
| **Value of company with option to expand** | **171** |

Note the option is deep out of the money: `S` = $226 million against `K` = $500 million. Entering today would destroy $274 million of value. Yet the option is worth $56 million, because volatility is 50% and the window is 5 years long.

**Determinism:** **DETERMINISTIC**: the annuity that produces `S` ($226 million from `CF` = 40, `k` = 12%, `n` = 10); the Black-Scholes call given `(S, K, t, sigma, r)`; the addition to the DCF value. A script handles all of it. **JUDGMENT**: almost everything upstream. Whether the expansion is a genuine option or just an aspiration. Whether the first investment is truly a prerequisite. The expansion's cash flows ($40 million a year for 10 years is a forecast for a market the firm has not entered). The entry cost, which is not known precisely and may change. The 5-year window. The choice of comparable public database firms for volatility. And the exclusivity scaling factor, which can legitimately take the $56 million down to near zero.

**Pitfalls:**
- Treating every opportunity as an option. Damodaran devotes a whole slide to this; see [[opportunities-are-not-options]]. Zero competitive advantage or zero excess returns on the second investment means zero option value, whatever Black-Scholes returns.
- Using "strategic options" as a label to wave through negative-NPV projects without ever specifying the expansion, its cost, or its cash flows.
- Discounting the expansion's cash flows at the current business's cost of capital. Use the target business's.
- Assuming a fixed exercise cost. Entry costs into a new market evolve, sometimes rising as competitors establish themselves.
- Quoting the number precisely. Expansion-option estimates are the noisiest in the real-options toolkit, precisely because nothing is traded and the exercise cost is soft.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.44-47, p.49
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.44-47, p.49

**Related:** [[opportunities-are-not-options]], [[real-options-framework]], [[black-scholes-model]], [[option-to-delay]], [[option-payoffs-and-determinants]], [[young-company-valuation]], [[dcf-valuation]]

# Financing flexibility as an option

**Core idea:** Firms routinely hold more cash and less debt than their optimum would suggest. They do it to meet unexpected future needs — an acquisition, a sudden investment opportunity. That financing flexibility has value, but it also has a cost: operating below the optimal debt ratio means a higher cost of capital and lower firm value. The option framing makes both sides measurable. Flexibility is a call option on reinvestment needs: the underlying is actual reinvestment needs, the strike is the level of reinvestment the firm can fund without flexibility, and exercising means taking unanticipated investments. Crucially, the option to take a project is worth nothing if the project has zero NPV — so the raw option value must be scaled by the excess returns the firm earns.

**Formulas:**
- Payoff when the flexibility is used: `(S - K) x Excess Return / WACC`
  - `S` = actual reinvestment needs (as % of firm value)
  - `K` = reinvestment needs financeable without flexibility (as % of firm value)
  - `Excess Return / WACC` = PV of excess returns in perpetuity; it converts the extra investment taken into value created
- `Excess Return = Return on capital - Cost of capital`
- Annual value of flexibility, as % of firm value: `Value of Flexibility = Option value % x (Excess Return / WACC)`
- Annual cost of flexibility: `Cost = Current cost of capital - Cost of capital at the optimal debt ratio`
- Decision rule: maintain flexibility if `Value of Flexibility > Cost of Flexibility`.
- Option inputs: `S` = expected annual reinvestment needs as % of firm value; `sigma^2` = variance in annual reinvestment needs, measured as the variance in `ln(Reinvestment/Value)`; `K` = `(Internal funds + normal access to external funds) / Value`; `T` = 1 year, so the model produces an annual value.

**Procedure:**
1. Establish the two capital-structure applications of option pricing. First, **security design**: most complex financial instruments decompose into a simple bond or common stock plus a combination of options. If those securities are publicly issued and traded, the options must be priced. Even in non-traded instruments such as bank loans, the options must be priced into the interest rate. Second, **valuing flexibility**, which is what the rest of this procedure covers.
2. Build the firm's cost-of-capital schedule across debt ratios and locate the optimal debt ratio — the one that minimizes cost of capital.
3. Compute the **cost** of flexibility: the current cost of capital minus the cost of capital at the optimal debt ratio. This is what the firm pays annually to stay under-levered.
4. Compute `S`: the average of reinvestment divided by firm value over the last 5 years.
5. Compute `sigma^2`: the variance over the last 5 years in `ln(Reinvestment/Value)`.
6. Compute `K`: the average over the last 5 years of `(internal funds + normal access to external funds) / Value`. This is the capital constraint.
7. Set `T` = 1 year, giving an annual value for flexibility.
8. Value the call. The output is a percentage of firm value — the value of the *option to take a project*.
9. Scale it for project quality. Multiply by `Excess Return / WACC`. If the firm earns no excess returns, this factor is zero and flexibility is worth nothing regardless of how volatile its reinvestment needs are.
10. Compare value against cost. Maintain flexibility if value exceeds cost; otherwise move toward the optimal debt ratio.

**Reference data:**

Input estimation table for the flexibility option (Disney figures):

| Model input | Estimated as | Measures | For Disney |
|---|---|---|---|
| `S` | Expected annual reinvestment needs (as % of firm value) | Magnitude of reinvestment needs | Average of Reinvestment/Value over last 5 years = 5.3% |
| `sigma^2` | Variance in annual reinvestment needs | Volatility of investment needs | Variance over last 5 years in `ln(Reinvestment/Value)` = 0.375 |
| `K` | (Internal funds + normal access to external funds) / Value | The capital constraint | Average over last 5 years = 4.8% |
| `T` | 1 year | Produces an annual value for flexibility | T = 1 |

Disney's cost of capital by debt ratio (used to locate the optimum and price the cost of flexibility):

| Debt Ratio | Cost of Equity | Cost of Debt | Cost of Capital |
|---|---|---|---|
| 0.00% | 13.00% | 4.61% | 13.00% |
| 10.00% | 13.43% | 4.61% | 12.55% |
| Current: 18% | 13.85% | 4.80% | 12.22% |
| 20.00% | 13.96% | 4.99% | 12.17% |
| 30.00% | 14.65% | 5.28% | 11.84% |
| **40.00%** | 15.56% | 5.76% | **11.64%** (optimum) |
| 50.00% | 16.85% | 6.56% | 11.70% |
| 60.00% | 18.77% | 7.68% | 12.11% |
| 70.00% | 21.97% | 7.68% | 11.97% |
| 80.00% | 28.95% | 7.97% | 12.17% |
| 90.00% | 52.14% | 9.42% | 13.69% |

Three determinants of the value of flexibility:

| Determinant | Direction |
|---|---|
| Capital constraints, internal | More internal operating cash flow → lower flexibility value. Firms with small or negative operating cash flows value it most. |
| Capital constraints, external | Easier access to financial markets → lower flexibility value. |
| Unpredictability of reinvestment needs | More unpredictable → higher flexibility value. |
| Capacity to earn excess returns | Greater capacity → higher flexibility value. Firms that cannot earn or sustain excess returns get **zero** value from flexibility. |

**Worked example:** Disney.

*Option value.* With `S` = 5.3%, `K` = 4.8%, `sigma^2` = 0.375, `T` = 1, the option is worth **1.6092%** of firm value. That is the value of the option to take a project.

*Scaling for project quality.* Disney earns a return on projects of 18.69% against a cost of capital of 12.22%, so the excess return is 6.47%. Treating those excess returns as perpetual:
`Value of Flexibility = 1.6092% x (0.0647 / 0.1222) = 0.85% of value per year`.

*Cost.* Disney's current debt ratio is 18%, with a cost of capital of 12.22%. The optimum is 40%, at 11.64%. So the annual cost of maintaining flexibility is `12.22% - 11.64% = 0.58%`.

*Verdict.* `0.85% > 0.58%`, so it pays Disney to maintain financing flexibility.

**Determinism:** **DETERMINISTIC**, and a script can do all of it from a financial-statement history plus a cost-of-capital schedule:
- Computing `S`, `sigma^2` and `K` as 5-year historical averages and variances from reported reinvestment, funding and firm-value data.
- The option value, given those inputs and `T` = 1.
- The scaling multiplication `1.6092% x (0.0647/0.1222) = 0.85%`.
- Locating the minimum of the cost-of-capital schedule (40%, 11.64%).
- The subtraction `12.22% - 11.64% = 0.58%`, and the final comparison and verdict.
 **JUDGMENT**: choosing the 5-year estimation window and treating backward-looking averages as forward-looking expectations. Defining "normal access to external funds" — the `K` input is a claim about how much the firm could raise routinely. Assuming excess returns persist in perpetuity, which is what makes `Excess Return / WACC` the right multiplier. Building the cost-of-capital schedule itself, which requires ratings, default spreads, and levered betas at every debt ratio.

**Pitfalls:**
- Reporting the raw option value (1.6092%) as the value of flexibility. It is the value of an option to take *a* project. Unscaled, it implicitly assumes every project is infinitely valuable.
- Ignoring the excess-return condition. A firm that earns exactly its cost of capital gets zero value from flexibility, no matter how volatile its reinvestment needs.
- Ignoring the cost side. Flexibility is not free; it is priced as the gap between the current and optimal cost of capital.
- Assuming all firms should hold flexibility. Firms with large internal cash flows and easy market access should value it least; the constrained, volatile, high-excess-return firm values it most.
- Confusing this with an operational real option. This is an option on the firm's *financing* capacity, and the underlying is measured as a percentage of firm value.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.55-61
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.55-61

**Related:** [[real-options-framework]], [[opportunities-are-not-options]], [[option-to-expand]], [[black-scholes-model]], [[optimal-capital-structure]], [[cost-of-capital]], [[excess-returns-and-value-creation]], [[equity-as-call-option]]

# Valuing a product patent as a call option

**Core idea:** A product patent gives a firm the right to develop and market a product. The firm will do so only if the present value of expected cash flows from product sales exceeds the cost of development. Otherwise it shelves the patent and incurs no further cost. That asymmetry is a call option. The underlying asset is the product; the strike is the development cost; the life is the patent life; the cost of delay is the annual erosion of a finite patent. This is the cleanest real-option application in the material, because patents give genuine (if partial) exclusivity and drug firms can estimate exercise cost fairly precisely.

**Formulas:**
- Patent payoff: `max(V - I, 0)`, where `V` = PV of expected cash flows from developing the product and `I` = PV of the costs of developing the product.
- Value of the patent (dividend-adjusted Black-Scholes call):
  - `C = S x e^(-y*t) x N(d1) - K x e^(-r*t) x N(d2)`
  - `d1 = [ln(S/K) + (r - y + sigma^2/2) x t] / (sigma x sqrt(t))`, `d2 = d1 - sigma x sqrt(t)`
- Cost of delay: `y = 1/n`, `n` = years of patent life remaining.
- Exercise rule: exercise (develop commercially) when `C <= S - K`; keep holding while `C > S - K`.
- Symbols: `S` = `V` = PV of cash inflows from taking the project now; `K` = `I` = cost of the investment in PV dollars; `t` = patent life; `sigma^2` = variance in `ln` of the underlying value; `r` = riskless rate matched to `t`; `y` = annual cost of delay.

**Procedure:**
1. Run the three tests from [[real-options-framework]] on the patent. Option test: underlying = the product the patent would generate; contingency = payoff is `PV of development cash flows - cost of development` if positive, else zero. Exclusivity test: patents block competitors from similar products, but not from *other* products treating the same condition — partial exclusivity. Pricing test: the underlying product is not traded, the patent itself is traded (though less often than oil reserves or mines), and the exercise cost is estimable by experienced drug firms.
2. Estimate `S`: the present value of cash inflows from launching the product now. This is a full capital-budgeting exercise. The noise in it is what gives the option value.
3. Estimate `sigma^2`: the variance in cash flows of similar assets or firms, or the variance in present value produced by a capital-budgeting simulation. In practice Damodaran uses industry-average firm variance.
4. Set `K`: the cost of making the investment, assumed constant in present-value dollars. The option is exercised when the investment is made.
5. Set `t` = the life of the patent.
6. Set `y = 1/n`, the annual cost of delay.
7. Set `r` = the government bond rate matching the patent life.
8. Value the call. Compare it with the exercise value `S - K`.
9. Determine optimal exercise timing. Recompute the option value for each declining level of remaining patent life, holding the other inputs fixed, and plot it against the horizontal line `S - K`. The crossing point is the optimal exercise date.
10. Prefer this approach when the firm is publicly traded and most of its value comes from one or a few patents. There you can use the firm's own market value and its variance as option inputs.

**Reference data:**

Estimation process for each patent-option input (Damodaran's mapping table):

| # | Input | Estimation process |
|---|---|---|
| 1 | Value of the underlying asset | PV of cash inflows from taking the project now. Noisy — but the noise adds option value. |
| 2 | Variance in value of the underlying asset | Variance in cash flows of similar assets/firms; or variance in PV from a capital-budgeting simulation. |
| 3 | Exercise price on the option | Cost of making the investment in the project. Assumed constant in present-value dollars. |
| 4 | Expiration of the option | Life of the patent. |
| 5 | Dividend yield | Cost of delay = `1/n`. Each year of delay is one less year of value-creating cash flows. |

The three-test verdict for patents and technology:

| Test | Verdict for patents |
|---|---|
| Option test | Passes. Underlying and contingency are both clearly specifiable. |
| Exclusivity test | Partial. Blocks similar products, not alternative treatments for the same disease. |
| Pricing test | Mixed. Underlying not traded (no replication, no arbitrage); option itself traded but thinly; exercise cost estimable fairly precisely. |
| Overall | Value can be estimated, but is only as good as the capital budgeting behind it. Best case: publicly traded firm with value concentrated in one or a few patents. |

**Worked example:** Biogen's 17-year patent on Avonex, a multiple sclerosis drug Biogen planned to produce and sell itself.

| Input | Value |
|---|---|
| `S` = PV of cash flows from introducing the drug now | $3,422 million |
| `K` = PV of cost of developing the drug commercially | $2,875 million |
| `t` = patent life | 17 years |
| `r` = 17-year T-bond rate | 6.7% |
| `sigma^2` = industry-average firm variance, biotech | 0.224 |
| `y` = cost of delay = 1/17 | 5.89% |

Outputs: `d1` = 1.1362, `N(d1)` = 0.8720; `d2` = -0.8512, `N(d2)` = 0.2076.

`C = 3,422 x e^(-0.0589 x 17) x 0.8720 - 2,875 x e^(-0.067 x 17) x 0.2076 = $907 million`.

*Optimal exercise.* The static exercise value is `S - K` = 3,422 - 2,875, roughly $550 million, and it is a horizontal line. The option value starts at $907 million with 17 years left and decays as remaining life shortens, approaching zero at 1 year. The two lines cross at about **8 years of remaining patent life**. Early in patent life, waiting is worth more than exercising. Late in patent life, the cost of delay dominates and Biogen should convert the patent to a commercial product.

**Determinism:** **DETERMINISTIC**: the payoff rule; `y = 1/n`; the Black-Scholes call value given all six inputs (a script takes them and returns $907 million); the exercise-timing curve, which is just the same computation repeated for `t` = 17, 16, ... 1 and compared against the constant `S - K`. **JUDGMENT**: the underlying value `S`. Estimating it means forecasting drug revenues, market share, pricing, and margins over the product's life. Volatility `sigma^2` is also judgment. Industry-average firm variance for biotech (0.224) is a proxy choice, not a measurement of this drug. Strike `K` is judgment too, as is whether it stays constant in PV dollars for 17 years. So is the exclusivity assessment — how much of the computed value the firm can actually claim given that rivals may develop different drugs for the same disease.

**Pitfalls:**
- Double counting. If patents are valued as options, do NOT also build a high growth rate into the DCF of existing commercial products. See [[valuing-a-firm-with-patents]].
- Treating patent exclusivity as complete. A patent stops copies, not competition. Scale the option value for that.
- Quoting the $907 million as precise. The estimate is only as good as the capital budgeting behind `S`, and there is no traded underlying to discipline it.
- Holding the patent to expiry. There is an optimal exercise point (roughly 8 years remaining in the Avonex case) after which waiting destroys value.
- Applying the approach to a diversified firm with hundreds of small patents. It works best where value is concentrated in one or a few patents.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.27-31, p.37
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.27-31, p.37

**Related:** [[option-to-delay]], [[valuing-a-firm-with-patents]], [[black-scholes-model]], [[real-options-framework]], [[natural-resource-options]], [[opportunities-are-not-options]], [[simulation]]

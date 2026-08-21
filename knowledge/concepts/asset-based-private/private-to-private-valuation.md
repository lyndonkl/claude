# Valuing a private-to-private transaction end to end

**Core idea:** One individual sells a private business to another. Three things distinguish this from any public valuation. Neither side is diversified, so a model that prices only market risk badly understates the discount rate. The investment is illiquid, so the buyer must take a discount for the missing exit. And a chunk of the revenue may belong to the current owner personally rather than to the business. The six-step procedure below is Damodaran's full sequence, and the order matters — statement cleanup feeds the coverage ratio that feeds the cost of debt, and the key-person haircut has to land on operating income before growth and reinvestment are applied.

**Formulas:**
- Terminal (stable-growth) firm value: `Value = EBIT × (1 + g) × (1 − t) × (1 − RIR) / (Cost of capital − g)`
- `RIR = g / ROC` — the reinvestment rate that makes growth internally consistent.
- `FCFF next year = EBIT × (1 + g) × (1 − t) × (1 − RIR)`
- `Value of equity = Value of firm − Debt`, where debt includes capitalized operating leases.
- `Final value of equity = Value of equity × (1 − Illiquidity discount)`
- Symbols: `EBIT` = adjusted, key-person-haircut operating income; `t` = tax rate; `g` = perpetual growth rate; `ROC` = return on capital; `RIR` = reinvestment rate.

**Procedure:**
1. **Estimate the discount rate.** No market prices exist and the buyer is undiversified, so standard models fail on both counts. Take a bottom-up unlevered beta from comparables, convert to a total beta by dividing by the correlation, lever at the sector's D/E, and build the cost of capital with a synthetic-rating cost of debt. See [[total-beta]] and [[private-company-cost-of-capital]].
2. **Clean up the financial statements.** Capitalize operating leases as debt; charge a market salary for uncompensated owner labour; strip personal expenses. See [[private-company-statement-cleanup]].
3. **Assess the key person.** Haircut operating income by the share of the business that leaves with the owner. See [[key-person-discount]].
4. **Set the valuation fundamentals.** Choose a growth rate and a return on capital, then derive the reinvestment rate as `g / ROC`. Even a business that will not grow in size needs reinvestment to stay attractive (remodeling) and functional (new ovens and appliances).
5. **Complete the valuation.** Value the firm as a stable-growth perpetuity, then subtract debt to get equity.
6. **Apply the illiquidity discount.** Choose a route and apply it to the equity value. See [[illiquidity-discount]].
7. **Decide what to ask for.** The seller's value and the buyer's value are different numbers; where the price lands between them depends on bargaining power and how many bidders exist. See [[private-to-public-sale]] for the case where a diversified bidder appears.

**Reference data — the restaurant's full input set:**

| Input | Value | Source step |
|---|---|---|
| Reported operating income | $400,000 | Statements |
| Adjusted operating income (market chef salary, leases reclassified) | $370,000 | Step 2 |
| Key person share `k` | 20% | Step 3 |
| EBIT after key-person haircut | $296,000 | Step 3 |
| Tax rate | 40% | Statements |
| Perpetual growth `g` | 2% | Step 4 |
| Return on capital `ROC` | 20% | Step 4 |
| Reinvestment rate `RIR = g/ROC` | 10% | Step 4 |
| Cost of capital | 13.25% | Step 1 |
| Debt (PV of leases, 12 yrs @ 7.5%) | $928,230 | Step 2 |
| Illiquidity discount (bid-ask route) | 12.88% | Step 6 |

**Worked example — the upscale French restaurant:**
- `FCFF next year = 296,000 × 1.02 × (1 − 0.40) × (1 − 0.10) = $163,040`
- `Value of firm = 163,040 / (0.1325 − 0.02) = $1,449,220`
- `Value of equity = 1,449,220 − 928,230 = $520,990`
- `Final value of equity = 520,990 × (1 − 0.1288) = $453,880`

Trace the value destruction step by step. Reported operating income of $400,000 became $370,000 after paying a real chef, then $296,000 after the key-person haircut. The 13.25% cost of capital is nearly 50% higher than a diversified buyer's 8.76%. And the last 12.88% comes off for illiquidity. The undiversified buyer's $453,880 is less than a third of the $1,483,560 a public buyer would pay for the identical cash flows.

**Determinism:**
- DETERMINISTIC: `{EBIT, k, g, ROC, t, cost of capital, debt, illiquidity discount} → firm value → equity value → final value`. Every step is closed-form. A script can run the whole chain given the eleven inputs above.
- JUDGMENT: the comparable set and its correlation with the market; the market salary; the key-person share `k`; the growth rate and the return on capital; and the choice of illiquidity route. That judgment needs sector data, compensation benchmarks, an understanding of the customer base, and the reinvestment the business actually needs to stay competitive.

**Pitfalls:**
- Skipping a step or reordering them. The coverage ratio that sets the cost of debt uses the lease expense from step 2, and the key-person haircut in step 3 must precede the growth calculation in step 4.
- Assuming growth without reinvestment. A restaurant that never remodels and never replaces its ovens does not hold its cash flows, let alone grow them.
- Using the market beta because it is what the comparables report. For an undiversified buyer that is the wrong risk measure and it roughly doubles the value.
- Applying the illiquidity discount to firm value instead of equity value.
- Treating the resulting number as "the" value of the business. It is the value to *this* buyer.
- Forgetting to subtract the capitalized lease debt at the end after having added it in step 2.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.129-131, p.132, p.138-142, p.149, p.152-153
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.127-129, p.130, p.136-140, p.147, p.150-151

**Related:** [[private-company-valuation-framework]], [[total-beta]], [[private-company-cost-of-capital]], [[private-company-statement-cleanup]], [[key-person-discount]], [[illiquidity-discount]], [[private-to-public-sale]], [[minority-discount]], [[stable-growth-model]]

# Valuing synergy: the three-step procedure

**Core idea:** Synergy has a value, and that value can be computed. The method is a difference of two DCFs. Value each firm alone at its own cost of capital. Add them to get the combined firm with no synergy. Then rebuild the combined firm with the synergy assumptions layered onto growth, margins and cash flows. The gap is the value of synergy. A useful check falls out of the arithmetic: the no-synergy combined value must equal the sum of the two stand-alone values exactly. Merely adding two firms together creates nothing. Separately, deciding what synergy is worth is not the same as deciding what to pay for it. Paying the full synergy value as a premium hands your gains to the seller.

**Formulas:**
- `Value of synergy = Value of combined firm WITH synergy − Value of combined firm WITHOUT synergy`.
- `Value of combined firm WITHOUT synergy = V_acquirer(stand-alone) + V_target(stand-alone)`, each discounted at its own WACC.
- Combined-firm status-quo inputs are value-weighted (or revenue-weighted, for margins) composites of the two firms.
- Tax synergy from net operating losses: `Maximum tax benefit = NOL × acquirer's tax rate`, achievable only if the losses can be used immediately.
- If taxable income limits usage: `Annual tax saving = min(Taxable income, remaining NOL) × tax rate`, and `Value = PV of that stream` over the years it takes to absorb the NOL.
- `Years to absorb NOL = NOL / Annual taxable income`.

**Procedure:**
1. Value the acquirer stand-alone. Use its own cash flows, its own growth, its own cost of capital.
2. Value the target stand-alone. Use the target's own risk and debt capacity. In a control-plus-synergy deal, use the target's **restructured** value here, so control value and synergy value do not overlap.
3. Add the two. This is the combined firm without synergy. Verify it equals the sum of the parts.
4. Build the combined firm's status-quo operating inputs as weighted averages: revenues add, margins blend by revenue, betas and debt ratios blend by value.
5. Overlay the synergy assumptions from the taxonomy — a higher margin, a higher ROC, a higher reinvestment rate, a longer growth period, a lower tax rate, a higher debt ratio.
6. Re-run the DCF on the combined firm with those inputs.
7. Subtract step 3 from step 6. That difference is the value of synergy.
8. Decide separately how much of it to pay away. As a sole bidder you keep more; in a contested auction the synergy gets bid into the price.

**Reference data:**

Worked synergy case 1 — P&G acquiring Gillette ("Piglet" = combined firm), FCFE-based, $ millions:

| Input | P&G | Gillette | Piglet: No Synergy | Piglet: Synergy |
|---|---|---|---|---|
| Free cash flow to equity | $5,864.74 | $1,547.50 | $7,412.24 | $7,569.73 |
| Growth rate, first 5 years | 12% | 10% | 11.58% | 12.50% |
| Growth rate after 5 years | 4% | 4% | 4.00% | 4.00% |
| Beta | 0.90 | 0.80 | 0.88 | 0.88 |
| Cost of equity | 7.90% | 7.50% | 7.81% | 7.81% |
| Value of equity | $221,292 | $59,878 | $281,170 | $298,355 |

Synergy assumptions: annual operating expenses cut by $250 million (raising FCFE), and a slightly higher five-year growth rate.

Worked synergy case 2 — AB InBev / SABMiller, FCFF-based, $ millions:

| Item | InBev | SABMiller (restructured) | Combined (status quo) | Combined (synergy) |
|---|---|---|---|---|
| Cost of equity | 8.93% | 9.37% | 9.12% | 9.12% |
| After-tax cost of debt | 2.10% | 2.24% | 2.10% | 2.10% |
| Cost of capital | 7.33% | 8.03% | 7.51% | 7.51% |
| After-tax return on capital | 12.10% | 12.64% | 11.68% | 12.00% |
| Reinvestment rate | 50.99% | 33.29% | 43.58% | 50.00% |
| Expected growth rate | 6.17% | 4.21% | 5.09% | 6.00% |
| Operating margin | 32.28% | 19.97% | 28.27% | 30.00% |
| PV of FCFF in high growth | $28,733 | $9,806 | $38,539 | $39,151 |
| Terminal value | $260,982 | $58,736 | $319,717 | $340,175 |
| Value of operating assets | $211,953 | $50,065 | $262,018 | $276,610 |

**Worked example:** Take the P&G/Gillette numbers. The no-synergy combined equity value is $281,170M, which is exactly $221,292M + $59,878M — the sum of the parts, as required. With $250M of annual cost savings and growth raised from 11.58% to 12.50%, the combined equity is worth $298,355M. Value of synergy = `298,355 − 281,170 = $17,185 million`.

For the AB InBev case, the same subtraction on operating assets gives `276,610 − 262,018 = $14,592 million` (~$14.6B). Note the check holds there too: `211,953 + 50,065 = 262,018`.

Tax synergy example — Best Buy considering Zenith. Zenith carries $2 billion of NOLs and Best Buy's tax rate is 36%. If the losses were usable at once, the benefit is `0.36 × 2,000 = $720 million`. Suppose Best Buy has only $500M of taxable income a year. Annual saving = `500 × 0.36 = $180M`. Absorbing the NOL takes `2,000 / 500 = 4 years`. The synergy is the present value of $180M a year for four years, which is well below $720M. Zenith's market value is $800M — pay the tax benefit as a premium only if the market price does not already reflect it and no rival bidder can capture it too.

**Determinism:**
- DETERMINISTIC: the stand-alone DCFs given their inputs; the weighted-average combined inputs; the re-valued combined DCF given the synergy inputs; the subtraction; the NOL arithmetic and its present value given a usage schedule and discount rate.
- JUDGMENT: every synergy assumption. How much margin improvement, how much extra growth, how many years until it arrives, and whether it arrives at all. That judgment needs bottom-up overlap analysis, precedent-transaction sanity checks, and a named owner for delivery. Also judgment: how much of the synergy to concede in the price.

**Pitfalls:**
- Valuing synergy against the target's *status-quo* value when you are also claiming control value. That double counts the restructuring gains. Use the restructured target value in the no-synergy baseline.
- Skipping the sum-of-parts check. If the no-synergy combined value differs from the sum of the stand-alone values, an inconsistent assumption has crept in.
- Letting the combined firm inherit a lower cost of capital purely from combining. In the AB InBev case the cost of capital is 7.51% in both combined columns — the synergy runs through operations, not financing.
- Paying the whole synergy value as a premium. That guarantees you capture none of it.
- Assuming NOLs convert to cash immediately. Usage is capped by the acquirer's taxable income, and delay cuts the present value.
- Assuming the target's market price contains none of the synergy. If the benefit is obvious to you, it may be obvious to other bidders.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.100-102, p.128-129`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.100-102, p.128-129`

**Related:** [[synergy-taxonomy]], [[synergy-delivery-odds]], [[three-reasons-and-acid-test]], [[restructured-value-and-value-of-control]], [[abinbev-sabmiller-case]], [[target-discount-rate-discipline]], [[status-quo-valuation]]

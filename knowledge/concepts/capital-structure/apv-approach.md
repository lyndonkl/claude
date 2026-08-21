# The Adjusted Present Value (APV) approach to the optimal debt ratio

**Core idea:** APV decomposes firm value into three additive pieces: the value of the firm with no debt, plus the present value of the tax benefits debt creates, minus the expected cost of bankruptcy that debt causes. Vary the dollar debt level and each piece moves. Tax benefits rise linearly with debt; expected bankruptcy costs rise with the default probability implied by the deteriorating rating. The optimal debt level maximizes the sum. Unlike the cost of capital approach, APV values debt *levels* rather than *ratios*, makes the bankruptcy cost explicit rather than burying it in a default spread, and needs no assumption that the cost of capital is a smooth function of leverage.

**Formulas:**
- `Firm Value = Unlevered Firm Value + Tax Benefits of Debt − Expected Bankruptcy Cost`.
- Unlevered value, backed out of the market: `V_u = Current market value of firm − Current tax benefits of debt + Current expected bankruptcy cost` = `(E + D) − (D × t) + (p_current × BC% × (E + D))`.
- Unlevered value, computed directly: value the firm's cash flows at the cost of equity implied by the unlevered beta (for an all-equity firm that equals the cost of capital).
- `Tax Benefits(d) = $Debt(d) × t_eff(d)`, with `t_eff = t` if interest ≤ EBIT, else `t × EBIT / Interest` (perpetual-savings assumption).
- `Expected Bankruptcy Cost(d) = p_default(rating(d)) × BC% × Firm value base`. The lecture version uses the current firm value as the base; apv.xls uses `(V_u + Tax Benefits(d))`.
- `$Debt(d) = d × Current firm value` (apv.xls does **not** net out cash).
- Optimal `d* = argmax_d [V_u + Tax Benefits(d) − Expected Bankruptcy Cost(d)]`.

**Procedure:**
1. **Step 1 — unlevered firm value.** Either value the unlevered cash flows at the unlevered cost of equity, or back it out from today's market value by removing the tax benefit on existing debt and adding back the expected bankruptcy cost already embedded in the price.
2. **Step 2 — tax benefits at each debt level.** Multiply dollar debt by the effective tax rate, applying the EBIT cap once interest exceeds operating income ([[tax-benefit-of-debt]]).
3. **Step 3 — probability of bankruptcy at each debt level.** Estimate the synthetic rating from the interest coverage ratio, then map the rating to a cumulative default probability using empirical studies (Altman, updated annually).
4. **Step 4 — cost of bankruptcy.** Direct costs run 5–10% of firm value empirically. Add indirect costs, which are much harder to size: high in sectors where distress visibly damages operations (airlines), low where it does not (groceries). Damodaran's worked examples use 25% of firm value in total.
5. **Step 5 — combine and pick the maximum.** Report the dollar debt level, not just the ratio.
6. Cross-check against the cost of capital answer. They use different machinery and should land in the same neighborhood; a large divergence usually traces to the bankruptcy-cost assumption or to a non-monotonic default-probability table.

**Reference data:**

*Altman's rating-to-default-probability mapping (cumulative 10-year likelihood of default, estimated by taking bonds in each rating class ten years earlier and measuring the proportion that defaulted):*

| Rating | Likelihood of default |
|---|---|
| AAA | 0.07% |
| AA | 0.51% |
| A+ | 0.60% |
| A | 0.66% |
| A- | 2.50% |
| BBB | 7.54% |
| BB | 16.63% |
| B+ | 25.00% |
| B | 36.80% |
| B- | 45.00% |
| CCC | 59.01% |
| CC | 70.00% |
| C | 85.00% |
| D | 100.00% |

*apv.xls ratings table, "large or stable firms"* (coverage band → rating, default spread, bankruptcy probability). Note the ladder ordering in the B/BB range is non-standard in this file and the probability column is non-monotonic — reproduce it verbatim:

| Coverage > | ≤ | Rating | Spread | p(default) |
|---|---|---|---|---|
| −100000 | 0.199999 | D2/D | 18.60% | 1.00 |
| 0.20 | 0.649999 | C2/C | 13.95% | 0.85 |
| 0.65 | 0.799999 | Ca2/CC | 10.63% | 0.70 |
| 0.80 | 1.249999 | Caa/CCC | 8.64% | 0.5901 |
| 1.25 | 1.499999 | B3/B- | 4.37% | 0.45 |
| 1.50 | 1.749999 | Ba1/BB+ | 3.57% | 0.10 |
| 1.75 | 1.999999 | Ba2/BB | 2.98% | 0.1663 |
| 2.00 | 2.249999 | B1/B+ | 2.38% | 0.25 |
| 2.25 | 2.49999 | B2/B | 1.98% | 0.368 |
| 2.50 | 2.999999 | Baa2/BBB | 1.27% | 0.0754 |
| 3.00 | 4.249999 | A3/A- | 1.125% | 0.025 |
| 4.25 | 5.499999 | A2/A | 0.99% | 0.0066 |
| 5.50 | 6.499999 | A1/A+ | 0.90% | 0.006 |
| 6.50 | 8.499999 | Aa2/AA | 0.72% | 0.0051 |
| 8.50 | 100000 | Aaa/AAA | 0.54% | 0.0007 |

The "smaller and riskier firms" table uses the same ratings, spreads and probabilities with stricter coverage thresholds: D < 0.5; C 0.5–0.8; CC 0.8–1.25; CCC 1.25–1.5; B- 1.5–2; BB+ 2–2.5; BB 2.5–3; B+ 3–3.5; B 3.5–4; BBB 4–4.5; A- 4.5–6; A 6–7.5; A+ 7.5–9.5; AA 9.5–12.5; AAA > 12.5.

**Worked example (Disney, 2013):** Step 1 — current firm value = $121,878m equity + $15,961m debt = $137,839m. Tax benefit on current debt = 15,961 × 0.361 = $5,762m. Expected bankruptcy cost at the current A rating = 0.66% × (0.25 × 137,839) = $227m. So unlevered value = 137,839 − 5,762 + 227 = **$132,304m**. Steps 2–5 give:

| d | $ Debt | Tax rate | Tax benefits | Rating | p(default) | Expected bankruptcy cost | Levered firm value |
|---|---|---|---|---|---|---|---|
| 0% | $0 | 36.10% | $0 | AAA | 0.07% | $23m | $132,281m |
| 10% | $13,784m | 36.10% | $4,976m | Aaa/AAA | 0.07% | $24m | $137,256m |
| 20% | $27,568m | 36.10% | $9,952m | Aaa/AAA | 0.07% | $25m | $142,231m |
| 30% | $41,352m | 36.10% | $14,928m | Aa2/AA | 0.51% | $188m | $147,045m |
| **40%** | **$55,136m** | **36.10%** | **$19,904m** | **A2/A** | **0.66%** | **$251m** | **$151,957m** |
| 50% | $68,919m | 36.10% | $24,880m | B3/B- | 45.00% | $17,683m | $139,501m |
| 60% | $82,703m | 36.10% | $29,856m | C2/C | 59.01% | $23,923m | $138,238m |
| 70% | $96,487m | 32.64% | $31,491m | C2/C | 59.01% | $24,164m | $139,631m |
| 80% | $110,271m | 26.81% | $29,563m | Ca2/CC | 70.00% | $28,327m | $133,540m |
| 90% | $124,055m | 22.03% | $27,332m | Caa/CCC | 85.00% | $33,923m | $125,713m |

At 40%: 132,304 + 19,904 − 251 = $151,957m, the maximum. APV agrees with the cost of capital approach at 40%.

*Second worked case (Hormel, apv.xls, 2009, bankruptcy cost 25% of value, small/risky ratings table):* unlevered value $4,477.19m; levered value rises through 0.6 (5,563.77) then dips at 0.7 (5,424.09) before peaking at **0.8 (5,823.31)**. The dip-then-peak comes entirely from the non-monotonic probability column — 0.7 lands on B1/B+ with p = 0.25 while 0.8 lands on Ba1/BB+ with p = 0.10.

**Determinism:**
- DETERMINISTIC: equity value, debt, tax rate, default probability, bankruptcy-cost percentage → unlevered value; dollar debt + effective tax rate → tax benefits; rating → default probability → expected bankruptcy cost; the sum and its argmax. Fully scriptable given the tables.
- JUDGMENT: the bankruptcy cost percentage (direct costs 5–10% are empirical, indirect costs are a guess); which default-probability study and vintage to use; whether the perpetual-tax-savings assumption is reasonable; which ratings table applies.

**Pitfalls:**
- Believing the precision. The answer is driven by two soft numbers, the bankruptcy cost percentage and the default probability.
- Using a non-monotonic probability table without noticing. It can produce a higher optimum than the economics justify, as in the Hormel example.
- Mixing bases for the expected bankruptcy cost. The lecture applies the percentage to current firm value; apv.xls applies it to unlevered value plus tax benefits. Pick one and be consistent.
- Forgetting the EBIT cap on tax benefits at high debt levels.
- Netting out cash in one model and not the other when comparing APV to the cost of capital answer.
- Assuming perpetual tax savings for a firm whose debt is short-dated or whose taxable income is unreliable.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.89-94
- corpfin-capital-structure — apv.xls (Inputs, `Default Spreads and Ratios`, `Adjusted Present Value` engine, Hormel worked example)

**Related:** [[cost-of-capital-approach]], [[enhanced-cost-of-capital-approach]], [[synthetic-rating-and-cost-of-debt]], [[tax-benefit-of-debt]], [[debt-equity-tradeoff]], [[pathways-to-the-optimal-debt-ratio]]

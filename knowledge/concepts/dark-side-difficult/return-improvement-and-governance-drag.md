# The governance drag and the value of improving returns

**Core idea:** Stockholders in many Asian, Latin American and European companies have little power over managers. Insiders hold the voting shares and run the firm, so the conflict-of-interest potential is large. The usual response — bump the discount rate, or slap a "governance discount" on the value — is arbitrary and unfalsifiable. The disciplined response is to show what bad management costs in cash-flow terms. Value the firm as it is run today, then value it with returns fixed, and let the gap speak. Poorly governed firms are usually poorly run firms, and being poorly run shows up as a return on capital below the cost of capital. There are two separate return levers, and they are worth very different amounts: raising the return on **new** investments, and raising the return on **existing** assets. The second is larger, because existing assets are usually the bulk of the capital.

**Formulas:**
- Growth from new investment: `Expected growth = Reinvestment rate × Return on capital on new investments`.
- Extra growth from improving returns on existing assets, spread over `n` years:
  `Efficiency growth per year = [1 + (ROC_new − ROC_old)/ROC_old]^(1/n) − 1`.
- Total expected growth when both levers are pulled:
  `g = Reinvestment rate × ROC_new + Efficiency growth`.
- Value of better management = value with improved returns − status-quo value; multiply by the probability of change to get an expected value ([[value-of-control-and-restructuring]]).
- Excess return test: value is created only when `ROC > Cost of capital`. A firm reinvesting 60% of after-tax operating income at 9.2% while its cost of capital is 16.9% is destroying value with every rupee it retains.

**Procedure:**
1. Compute the firm's actual return on capital and compare it with its cost of capital. A large negative gap **is** the governance drag, quantified.
2. **Scenario A — status quo.** Value the firm with the existing reinvestment rate and the existing return on capital. Do not soften anything.
3. **Scenario B — better returns on new investments.** Keep the reinvestment rate, raise the return on new capital to a defensible target (peer median, or the firm's own cost of capital, or its best historical performance). Recompute growth as `RIR × ROC_new`. Existing assets keep earning their old, sub-par return.
4. **Scenario C — better returns on new *and* existing assets.** Add the efficiency-growth term for lifting the return on the existing capital base from `ROC_old` to `ROC_new` over `n` years. This adds growth on top of the reinvestment-driven growth.
5. Report all three values, plus the current price. The spread between them is the price of governance.
6. Weight the scenarios by the probability that anyone forces the change: insider ownership, voting-share structure, activist presence, takeover market, regulatory pressure.
7. Do **not** additionally discount the estimated value for the absence of stockholder power. That would count the same problem twice — once in the low returns you already modelled, once in an arbitrary haircut.

**Reference data:** Tube Investments (India, 2000) — three scenarios, identical discount rates. Rs millions. Common inputs: cost of equity = 12% + 1.17 × 9.23% = 22.80% (risk premium 9.23% = 4% mature + 5.23% country; beta 1.17 from an unlevered sector beta of 0.75 relevered at D/E 79%); after-tax cost of debt = (12% + 1.50%) × (1 − 0.30) = 9.45%; WACC = 22.8% × 0.558 + 9.45% × 0.442 = **16.90%** in all three scenarios. Current position: EBIT(1−t) 4,425; net capex 843; ΔWC 4,150; FCFF −568; current reinvestment rate 112.82%. Forward reinvestment rate 60% in every scenario. Stable phase: g = 5%, beta 1.00, debt ratio 44.2%, country premium 3%, stable cost of capital 14.78%.

| | A. Status quo | B. Higher marginal return | C. Higher average return |
|---|---|---|---|
| ROC on new investments | 9.20% | 12.20% | 12.20% |
| Return on existing assets | 9.20% (unchanged) | 9.20% (unchanged) | rises 9.2% → 12.2% over 5 years |
| Efficiency growth | — | — | 5.81% per year |
| Expected growth | 0.60 × 0.092 = **5.52%** | 0.60 × 0.122 = **7.32%** | 0.60 × 0.122 + 0.0581 = **13.13%** |
| EBIT(1−t), years 1–5 | 4,670 / 4,928 / 5,200 / 5,487 / 5,790 | 4,749 / 5,097 / 5,470 / 5,871 / 6,300 | 5,006 / 5,664 / 6,407 / 7,248 / 8,200 |
| FCFF, years 1–5 | 1,868 / 1,971 / 2,080 / 2,195 / 2,316 | 1,900 / 2,039 / 2,188 / 2,348 / 2,520 | 2,003 / 2,265 / 2,563 / 2,899 / 3,280 |
| Terminal-year FCFF | 2,775 | 3,904 | 5,081 |
| Stable ROC / stable RIR | 9.22% / 54.35% | 12.20% / 40.98% | 12.20% / 40.98% |
| Terminal value (year 5) | 2,775/(0.1478 − 0.05) = 28,378 | 3,904/(0.1478 − 0.05) = 39,921 | 5,081/(0.1478 − 0.05) = 51,956 |
| Firm value | 19,578 | 25,185 | 31,829 |
| + cash 13,653 − debt 18,073 = equity | 15,158 | 20,765 | 27,409 |
| **Value per share** | **Rs 61.57** | **Rs 84.34** | **Rs 111.30** |

Market price at the time: Rs 102. On status-quo assumptions the stock was overvalued by 66%; on the full-improvement scenario it was undervalued.

**Worked example:** The efficiency-growth term for Tube Investments, scenario C. Returns on existing assets rise from 9.2% to 12.2%, an increase of `(0.122 − 0.092)/0.092 = 32.6%` in total operating income from the same asset base. Spread over five years: `(1 + 0.326)^(1/5) − 1 = 5.81%` extra growth a year. Add the reinvestment-driven growth of `0.60 × 0.122 = 7.32%` and total expected growth is **13.13%**. That single change — fixing the existing business rather than only the next investment — moves the value from Rs 84.34 to Rs 111.30, a bigger jump than the move from Rs 61.57 to Rs 84.34.

**Determinism:** DETERMINISTIC — (reinvestment rate, ROC_old, ROC_new, improvement horizon `n`, discount-rate inputs, stable-phase inputs) → efficiency growth, total growth, cash flows, terminal value, value per share for each scenario. JUDGMENT: the target return on capital and whether it is reachable (needs peer returns, the firm's own better years, and evidence of management capability), the number of years over which existing assets improve, and the probability that the improvement happens at all. That probability needs ownership structure, voting rights, activist activity, and the local market for corporate control.

**Pitfalls:**
- Answering the governance problem with a discount-rate bump or a flat value discount. Both are unfalsifiable and neither tells you what a fix is worth.
- Modelling only the marginal-return improvement. Most of the capital is already in the ground, so the existing-asset lever is usually the bigger one.
- Applying the efficiency-growth term forever. It is a one-time level shift in returns, spread over `n` years, not a permanent growth rate.
- Presenting the improved-management value as the value of the stock when nobody can force the change.
- Forgetting that a firm reinvesting heavily at a return below its cost of capital destroys value as it grows — the higher the reinvestment rate, the worse it is.
- Changing the discount rate between scenarios. In the Tube Investments case the WACC is deliberately identical across all three, so the entire difference comes from returns.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.330-333
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.321-324

**Related:** [[value-of-control-and-restructuring]], [[country-risk-exposure]], [[cross-holdings]], [[difficult-company-taxonomy]], [[return-on-invested-capital]], [[sales-to-capital-reinvestment]], [[value-versus-price]]

# Restructured value and the value of control

**Core idea:** The value of control is not a percentage. It is the difference between a firm valued as it would be run optimally and the same firm valued as it is run today. Getting that number requires a second complete DCF, built from a specific list of policy changes. The changes come from benchmarking: compare the target's margin, return on capital, reinvestment rate and debt ratio against the acquirer and the sector, and close the gaps you believe you can close. Control has value only where there is a gap. A well-run firm offers none.

**Formulas:**
- `Value of control = Optimal (restructured) firm value − Status quo firm value`, usually computed on equity value.
- Restructuring works through the same drivers as any DCF:
  - `Expected growth = Reinvestment rate × After-tax return on capital` — raise either or both.
  - `EBIT = Revenues × Operating margin` — raise the margin.
  - `ROC = Operating margin × Capital turnover ratio` — raise either.
  - `WACC = k_e × E/(D+E) + k_d(1−t) × D/(D+E)` — move to the debt ratio that minimizes WACC.
- Optimal capital structure: the debt ratio that minimizes WACC and therefore maximizes firm value.
- Note the tension: raising the reinvestment rate lowers near-term FCFF while raising growth. Value rises only if the reinvestment earns more than the cost of capital.

**Procedure:**
1. Complete the status-quo valuation first.
2. Benchmark the target on four metrics against the acquirer and the sector: pre-tax operating margin, after-tax ROIC, reinvestment rate, and debt to capital. Add the effective tax rate.
3. For each gap, decide whether it is closeable and by how much. Sector averages are the usual anchor for a "run like everyone else" case; the acquirer's own metrics are the anchor for a "run like us" case.
4. Change investing policy: set the new ROC and the new reinvestment rate, and recompute expected growth.
5. Change financing policy: run the cost-of-capital schedule across debt ratios. At each ratio, relever the beta, infer the bond rating and interest rate, apply the tax benefit (capped when interest exceeds EBIT), and compute WACC and firm value. Pick the ratio that minimizes WACC.
6. Change dividend policy if the firm holds excess cash it will not invest well.
7. Re-run the full DCF with the new inputs to get the restructured (optimal) value.
8. Subtract the status-quo value. That is the value of control.
9. Sanity-check the direction of each change. Higher reinvestment cuts early FCFF; the value gain must come from the terminal value and must survive the delay.

**Reference data:**

Benchmarking table, SABMiller vs acquirer and sector, 2015:

| Metric | SABMiller | AB InBev | Global Alcoholic Beverage Sector |
|---|---|---|---|
| Pre-tax operating margin | 19.97% | 32.28% | 19.23% |
| Effective tax rate | 26.36% | 18.00% | 22.00% |
| Pre-tax ROIC | 14.02% | 14.76% | 17.16% |
| ROIC | 10.33% | 12.10% | 13.38% |
| Reinvestment rate | 16.02% | 50.99% | 33.29% |
| Debt to capital | 14.67% | 23.38% | 18.82% |

SABMiller status quo vs optimal, $ millions:

| Item | Status Quo | Optimal |
|---|---|---|
| Cost of equity | 9.10% | 9.37% |
| After-tax cost of debt | 2.24% | 2.24% |
| Cost of capital | 8.09% | 8.03% |
| After-tax return on capital | 10.33% | 12.64% |
| Reinvestment rate | 16.02% | 33.29% |
| Expected growth rate | 1.65% | 4.21% |
| PV of FCFF in high growth | 11,411.72 | 9,757.08 |
| Terminal value | 47,711.04 | 56,935.06 |
| Value of operating assets | 43,747.24 | 48,449.42 |
| + Cash | 1,027.00 | 1,027.00 |
| + Minority holdings | 20,819.02 | 20,819.02 |
| − Debt | 12,918.00 | 12,918.00 |
| − Minority interests | 1,183.00 | 1,183.00 |
| **Value of equity** | **51,492.26** | **56,194.44** |

SAP optimal capital structure schedule, 2005 — the financing half of restructuring:

| Debt Ratio | Beta | Cost of Equity | Bond Rating | Interest Rate | Tax Rate | After-tax Cost of Debt | WACC | Firm Value |
|---|---|---|---|---|---|---|---|---|
| 0% | 1.25 | 8.72% | AAA | 3.76% | 36.54% | 2.39% | 8.72% | $39,088 |
| 10% | 1.34 | 9.09% | AAA | 3.76% | 36.54% | 2.39% | 8.42% | $41,480 |
| 20% | 1.45 | 9.56% | A | 4.26% | 36.54% | 2.70% | 8.19% | $43,567 |
| **30%** | **1.59** | **10.16%** | **A−** | **4.41%** | **36.54%** | **2.80%** | **7.95%** | **$45,900** |
| 40% | 1.78 | 10.96% | CCC | 11.41% | 36.54% | 7.24% | 9.47% | $34,043 |
| 50% | 2.22 | 12.85% | C | 15.41% | 22.08% | 12.01% | 12.43% | $22,444 |
| 60% | 2.78 | 15.21% | C | 15.41% | 18.40% | 12.58% | 13.63% | $19,650 |
| 70% | 3.70 | 19.15% | C | 15.41% | 15.77% | 12.98% | 14.83% | $17,444 |
| 80% | 5.55 | 27.01% | C | 15.41% | 13.80% | 13.28% | 16.03% | $15,658 |
| 90% | 11.11 | 50.62% | C | 15.41% | 12.26% | 13.52% | 17.23% | $14,181 |

Note two features of the schedule. The tax rate falls above 40% debt, because interest expense exceeds EBIT and the tax shield stops being fully usable. And the rating collapses from A− to CCC between 30% and 40%, which is what makes 30% the optimum.

**Worked example — three cases:**

*SABMiller.* Benchmarking shows a firm reinvesting far too little (16.02% against a 33.29% sector rate) at a ROIC below both peers and acquirer. The restructuring raises ROC to 12.64% and the reinvestment rate to the sector's 33.29%. Growth rises from 1.65% to 4.21% (`0.3329 × 0.1264 = 4.21%`). Adding debt raises the cost of equity to 9.37% but nudges WACC down to 8.03%. Equity value rises from $51,492.26M to $56,194.44M. **Value of control = $4,702.17M**, about $4.7B. Even so, $51.5B + $4.7B falls well short of the $75B market price, so control alone cannot justify the deal.

*SAP.* Two changes: reinvest more in emerging markets (reinvestment rate from 57.42% to 70%, so growth = `0.70 × 0.1993 = 13.99%`) and move to the optimal 30% debt ratio. New cost of equity = `3.41% + 1.59 × 4.50% = 10.57%`; after-tax cost of debt = `(3.41% + 1.00%) × (1 − 0.3654) = 2.80%`; WACC = `10.57% × 0.70 + 2.80% × 0.30 = 8.24%`. Stable phase: debt ratio 30%, cost of capital 6.27%, ROC 6.27%, reinvestment 54.38%, `TV_10 = 1,898/(0.0627 − 0.0341) = 66,367`. Operating assets rise to 38,045 and equity to 40,157, giving **€126.51 per share** against €106.12 status quo. Value of control ≈ **€20.39 per share**. Note the shape: FCFF in year 1 *falls* from 671 to 484 because of heavier reinvestment, and the gain arrives later.

*Blockbuster.* Here the lever is margin, not reinvestment. Better management raises after-tax operating income from 163 to 249, lifting ROC from 4.06% to 6.20%. The same dollar reinvestment (43) now represents a reinvestment rate of only `43/249 = 17.32%`, so growth stays at `0.1732 × 0.0620 = 1.07%` — the same growth achieved far more efficiently. WACC is unchanged at 6.17%. `TV_5 = 156/(0.0676 − 0.03) = 4,145`. Operating assets 3,840 + cash 330 − debt 1,847 = equity **$2,323M**, or **$12.47 per share**, against $5.13 status quo. Value of control ≈ **$7.34 per share** — more than the entire status-quo value.

**Determinism:**
- DETERMINISTIC: the restructured DCF given the new inputs; the subtraction that yields the value of control; the whole cost-of-capital schedule given an unlevered beta, a rating-to-spread lookup, a tax rate and EBIT.
- JUDGMENT: which gaps are closeable and by how much; whether to anchor on the sector or the acquirer; how fast the changes can be implemented; the synthetic-rating assignment at each hypothetical debt ratio. This judgment needs the benchmarking table, an operating plan, and evidence that the acquirer has achieved similar improvements before.

**Pitfalls:**
- Assuming every gap closes fully and immediately. Delay reduces the present value of control, and Damodaran's own question — what if the changes take three years? — points at exactly this.
- Raising the reinvestment rate without checking that ROC exceeds the cost of capital. Reinvesting more at a sub-WACC return destroys value.
- Restructuring a firm that is already well run and calling the difference "control value."
- Moving to a debt ratio past the rating cliff. Between 30% and 40% for SAP, firm value drops from $45,900 to $34,043.
- Ignoring the tax-benefit cap. Above the point where interest exceeds EBIT, extra debt buys a smaller shield.
- Confusing the value of control with what you should pay for it. Paying the full amount gives the entire improvement to the seller.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.126-127, p.141-142, p.144`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.126-127, p.141-142, p.144`

**Related:** [[status-quo-valuation]], [[expected-value-of-control]], [[control-premium-rules-of-thumb]], [[three-reasons-and-acid-test]], [[implied-probability-of-management-change]], [[paths-to-value-creation]], [[optimal-capital-structure]], [[synthetic-rating]], [[abinbev-sabmiller-case]]

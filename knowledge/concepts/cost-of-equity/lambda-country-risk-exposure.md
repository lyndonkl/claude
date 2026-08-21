# Lambda: firm-specific exposure to country risk

**Core idea:** Revenue and production weights are crude proxies for how much country risk a company actually bears. Two other forces matter. Companies can **hedge** country risk with options, futures, and political-risk insurance. And companies in sectors deemed vital to "national interests" — where the government has an official or unofficial role — bear more country risk than their revenue mix suggests. Lambda is a single, richer measure of a firm's relative exposure to country risk, designed to absorb all of these drivers. It enters the cost of equity as a separate factor loading on the country risk premium, independent of beta.

**Formulas:**
- Cost of equity with lambda: **E(Return) = Riskfree Rate + β × (Mature ERP) + λ × (CRP)**.
  - β = market beta, loading on mature-market equity risk.
  - λ (lambda) = the firm's exposure to country risk, relative to the average firm in that market.
  - CRP = the country's additional equity risk premium.
- Revenue-based lambda: **λ = (% of revenues earned domestically by the firm) / (% of revenues earned domestically by the average firm in that market)**.
- Return-based lambda: regress the firm's stock returns on returns of the country's sovereign bond. The **slope coefficient is lambda**.
  - Return_firm = a + λ × Return_country bond.

Symbols: "domestically" means inside the risky country; the "average firm in that market" benchmark is estimated from the local market as a whole (roughly 80% domestic revenues for Indian firms in 2008-09).

**Procedure:**
1. Decide whether lambda is worth estimating. It is, when firms in the same country plainly differ in country-risk exposure — an exporter versus a domestic utility, a hedged company versus an unhedged one.
2. **Revenue-based route.** Get the firm's domestic revenue share. Get the domestic revenue share of the average firm in that market. Divide. λ = 1 means average exposure; λ < 1 means less exposed than the typical local firm; λ > 1 means more.
3. **Return-based route.** Collect the firm's stock returns and the returns on the country's US$ sovereign bond over a common window (Damodaran used Brazil's C-Bond, 2000-2003). Run an OLS regression of firm returns on bond returns. The slope is lambda. Report its standard error — this is a regression, with all the noise problems in [[regression-beta]].
4. Adjust judgmentally for drivers the mechanical measures miss: active hedging programs (which lower lambda) and government/national-interest entanglement (which raises it).
5. Plug lambda into the cost-of-equity formula as a separate term. Do **not** also scale the CRP by beta — that would double-count exposure.
6. Sanity-check the answer against the other four country-risk approaches (see [[operation-weighted-erp]]). Lambda should land between the location-CRP and operation-CRP extremes unless you have a specific reason otherwise.

**Reference data:**

Revenue-based lambdas, Indian firms 2008-09 (average Indian firm earns ~80% of revenues domestically):

| Firm | Domestic (India) revenue share | Lambda |
|---|---|---|
| Tata Motors | 91.37% | 91%/80% = 1.14 |
| Tata Consultancy Services (TCS) | 7.62% | 7.62%/80% = 0.09 |

Return-based lambdas, Brazil 2000-2003, regressed against the Brazilian C-Bond:

| Firm | Regression | Lambda |
|---|---|---|
| Embraer | Return_Embraer = 0.0195 + 0.2681 × Return_C-Bond | 0.27 |
| Embratel | Return_Embratel = −0.0308 + 2.0030 × Return_C-Bond | 2.00 |

Two firms in the same country, differing by a factor of seven in country-risk exposure.

**Worked example (Embraer, September 2004):** Inputs: US$ riskfree rate 4%, beta 1.07, mature-market ERP 5%, Brazil CRP 7.89%, lambda 0.27.

Cost of equity = 4% + 1.07 × 5% + 0.27 × 7.89% = 4% + 5.35% + 2.13% = **11.48%**.

Compare: the location-CRP approaches give 17.24% and 17.79%; the operation-CRP approaches give 9.59% and 9.60%. Lambda lands in between, which is what you want — Embraer earns only 3% of revenues in Brazil, but it is a Brazilian aerospace champion with government entanglement, so its true exposure exceeds its revenue share. Damodaran's full 2004 Embraer cost of capital uses this 11.48%-style construction with a 4.29% riskfree rate and a 4% mature premium, giving a cost of equity of 4.29% + 1.07×4% + 0.27×7.89% = **10.70%**.

**Determinism:**
- DETERMINISTIC: (firm domestic revenue %, average-firm domestic revenue %) → revenue-based lambda; (firm return series, sovereign bond return series) → regression slope = return-based lambda; (Rf, beta, mature ERP, lambda, CRP) → cost of equity.
- JUDGMENT: which lambda estimate to use; the "average firm" domestic-revenue benchmark; the regression window and the sovereign bond chosen as the country-risk proxy; how much to adjust for hedging and national-interest exposure; whether the regression lambda is statistically meaningful at all.

**Pitfalls:**
- Estimating a return-based lambda from a short or crisis-dominated window. It is a regression slope and inherits every noise problem of a beta regression.
- Using lambda **and** multiplying the CRP by beta. Pick one exposure channel.
- Assuming lambda ≈ 1 for every local firm, which collapses the method back to the blanket location-CRP approach.
- Applying the revenue-based lambda to a firm whose plants, not its customers, sit in the risky country.
- Forgetting that lambda is relative to the *average local firm*, not to a global average.
- Ignoring the parallel question on the debt side: a firm may bear only a fraction of country default risk in its cost of debt too (Embraer was assigned two-thirds of Brazil's country default spread).

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.60-63
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.60-63
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.111 (Embraer cost of equity assembly with lambda)

**Related:** [[country-risk-premium]], [[operation-weighted-erp]], [[regression-beta]], [[cost-of-equity-assembly]], [[country-risk-in-cost-of-debt]]

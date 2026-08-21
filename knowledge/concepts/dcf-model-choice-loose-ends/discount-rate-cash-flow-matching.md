# Matching the discount rate to the cash flow

**Core idea:** The discount rate must belong to the same world as the cash flow it discounts. Three dimensions have to line up. Claimholder: equity cash flows go with the cost of equity, firm cash flows with the cost of capital. Currency: the riskfree rate must be denominated in the currency of the cash flows, since a currency's riskfree rate carries its expected inflation. Inflation basis: nominal cash flows need a nominal rate, real cash flows a real rate. A mismatch on any dimension biases the value, and the bias can be large. Discounting rupee cash flows at a dollar cost of capital, for example, values away the rupee's inflation without removing it from the cash flows.

**Formulas:**
- Claimholder match: equity flows (dividends, FCFE) → `k_e`; firm flows (FCFF) → `WACC = k_e × E/(D+E) + k_d(1−t) × D/(D+E)`.
- Currency match: `k_e = Riskfree Rate(currency) + Beta × ERP`. The riskfree rate is a default-free government bond rate in that currency.
- Real-versus-nominal conversion (Fisher): `(1 + Nominal Rate) = (1 + Real Rate) × (1 + Expected Inflation)`.
- Component decomposition: `Riskfree Rate = Expected Inflation + Expected Real Interest Rate`; `Nominal GDP Growth = Expected Inflation + Expected Real Growth`.

**Reference data — the matching rules:**

| Dimension | Cash flow | Discount rate |
|---|---|---|
| Claimholder | Dividends or FCFE | Cost of equity |
| Claimholder | FCFF | Cost of capital |
| Currency | Cash flows in currency X | Riskfree rate (and hence discount rate) in currency X |
| Inflation basis | Nominal cash flows | Nominal cost of equity / capital |
| Inflation basis | Real cash flows | Real cost of equity / capital |

Inflation threshold: if expected inflation is **below 10%**, stay nominal — taxes are levied on nominal income, so nominal modeling is simpler and more accurate. If expected inflation is **above 10%**, switch to real cash flows and a real discount rate, because nominal forecasts become unstable.

Consistency corollary: the riskfree rate embeds an implicit view of nominal economic growth. A low riskfree rate implies low inflation and low real growth. Pairing high nominal growth in the cash flows with a low riskfree rate overvalues the business. Pairing low growth with a high riskfree rate undervalues it.

**Procedure:**
1. Name the cash flow you are discounting and its claimholder. Pick `k_e` or WACC accordingly.
2. Identify the reporting/forecast currency of the cash flows. Take a default-free long-term government bond rate in that currency as the riskfree rate; if the sovereign is not default-free, strip its default spread first.
3. Read expected inflation for that currency. Below 10% → build nominal cash flows and a nominal rate. Above 10% → convert both sides to real terms using the Fisher relation.
4. Check the growth-versus-riskfree consistency. Your perpetual nominal growth rate should not exceed the riskfree rate in the same currency, because the riskfree rate is a proxy for nominal GDP growth.
5. If you switch currencies mid-analysis, convert cash flows at expected exchange rates implied by the inflation differential, not at the spot rate carried forward.

**Worked example (Heineken, September 2019, in euros):** the cash flows are in euros, so the discount rate is built on the euro riskfree rate of **−0.50%**. Cost of equity = −0.50% + beta 1.20 × ERP 6.83% = **7.66%**. Pre-tax cost of debt = −0.5% + 2% default spread; after tax at 25%, `k_d = 1.13%`. With weights E = 59.9% and D = 40.1%, `WACC = 7.66%(0.599) + 1.13%(0.401) = 5.04%`. The same consistency governs the terminal growth rate: because the euro riskfree rate is −0.5%, stable growth is set at **−0.5%**, which forces a *negative* stable reinvestment rate of `g/ROC = −0.5%/5% = −10%`. Terminal value = `2,972/(0.05 − (−0.005)) = €54,034`.

**Determinism:**
- DETERMINISTIC: the claimholder/currency/inflation classification given the three facts; the Fisher conversion between real and nominal; the WACC computation given components.
- JUDGMENT: the expected inflation forecast, whether a government bond in that currency is genuinely default-free, and whether the growth path in the cash flows is consistent with the implied nominal growth in the riskfree rate. That judgment needs sovereign ratings/CDS spreads and macro forecasts.

**Pitfalls:**
- Discounting emerging-market-currency cash flows at a dollar cost of capital.
- Modeling real cash flows and then applying a nominal WACC (or the reverse) — a silent, systematic error.
- Assuming high nominal growth alongside a low riskfree rate; the value is inflated by construction.
- Forgetting that taxes are assessed on nominal income, which is the reason to stay nominal at moderate inflation.

**Sources:**
- valpacket1spr21 p.215
- valpacket1spr20 p.211
- valpacket1spr21 p.201-202 (riskfree rate, nominal GDP growth and consistency)
- valpacket1spr21 p.203 (Heineken euro valuation)

**Related:** [[dcf-model-choice-framework]], [[equity-versus-firm-valuation]], [[growth-pattern-and-stage-count]], [[riskfree-rate]], [[equity-risk-premium]], [[cost-of-capital]], [[terminal-value]]

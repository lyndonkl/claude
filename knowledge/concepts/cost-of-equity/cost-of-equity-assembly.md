# Assembling a cost of equity end to end

**Core idea:** A cost of equity is three inputs assembled under strict consistency rules. Take a riskfree rate in the currency of the cash flows. Take an equity risk premium that reflects where the company actually operates. Take a beta, preferably bottom-up, that reflects the businesses the firm is in and its own financial leverage. The discount rate must match the cash flows on three dimensions: claim type (equity cash flows go with the cost of equity, firm cash flows with the cost of capital), currency, and nominal versus real. Once you have a cost of equity in one currency, you can convert it into another using only differential inflation — currency differences in discount rates are an inflation effect, nothing more.

**Formulas:**
- **Cost of Equity = Riskfree Rate + Beta × (Equity Risk Premium).**
- With a country risk premium attached through beta: Cost of Equity = Rf + β × (Mature ERP + CRP).
- With a country risk premium attached through lambda: Cost of Equity = Rf + β × Mature ERP + λ × CRP.
- Historical-premium route for the ERP: ERP = Mature-market premium + Country risk premium, where Country risk premium = Country default spread × (σ_equity / σ_country bond).
- **Currency conversion:** Cost of Equity in currency X = (1 + Cost of Equity in $) × (1 + Expected inflation in X) / (1 + Expected inflation in $) − 1.
- Equivalent direct route: Cost of Equity in X = Riskfree rate in X + β × ERP.
- Feeding the cost of capital: Cost of Capital = Cost of Equity × E/(D+E) + Cost of Debt × (1 − t) × D/(D+E), on market-value weights.

**Procedure:**
1. **Fix the currency and nominal/real basis** of the cash flows. Everything else follows from this.
2. **Riskfree rate**: the 10-year default-free government bond rate in that currency, or the local bond rate minus the sovereign default spread if the government is not default-free ([[riskfree-rate-fundamentals]], [[currency-riskfree-rate]]). Do not normalize it in isolation ([[riskfree-rate-normalization]]).
3. **Equity risk premium**:
   a. Get the mature-market premium — the implied ERP for the S&P 500 (4.72% on 1/1/2021) ([[implied-equity-risk-premium]], [[choosing-an-equity-risk-premium]]).
   b. Get the country risk premiums for the countries the company operates in ([[country-risk-premium]]).
   c. Weight them by the company's operations, not its country of incorporation ([[operation-weighted-erp]]).
4. **Beta**: build it bottom-up from comparable firms in the company's businesses, value-weight across businesses, and relever at the firm's own market debt-to-equity ratio ([[bottom-up-beta]], [[levering-and-unlevering-beta]]). Use the regression beta only as a diagnostic ([[regression-beta]]).
5. **Adjust for the investor**. If the marginal investor is not diversified, convert to a total beta ([[total-beta]]). If the asset is not traded, build the beta from comparables and assume an industry-median D/E ([[non-traded-asset-betas]]).
6. **Combine**: Cost of Equity = Rf + β × ERP. Decide whether country risk enters through beta, additively, or through lambda ([[lambda-country-risk-exposure]]).
7. **Do it by division** where divisions differ in business risk. The right hurdle rate for a project is the cost of equity of the business it belongs to, not the company average.
8. **Convert currencies** if needed, by differential inflation, and cross-check against building the rate directly off the local riskfree rate. The two should agree closely.
9. **Check consistency** before using it: same currency as the cash flows; same nominal/real basis; equity cash flows only; no risk counted twice (country risk in both the cash flows and the premium; leverage in both the beta and the weights).

**Reference data:**

The three consistency dimensions for any discount rate:

| Dimension | Rule |
|---|---|
| Claim type | Cash flows to equity → cost of equity. Cash flows to the firm → cost of capital. |
| Currency | Currency of the cash flows must equal currency of the discount rate. |
| Nominal vs real | Nominal cash flows (with expected inflation) → nominal discount rate. Real cash flows → real rate. |

Consequences of mismatching (worked in the packet on a company whose true equity value is $1,073): discounting equity cash flows at the 9.94% cost of capital gives $1,248, overstating equity by $175. Discounting firm cash flows at the 13.625% cost of equity gives a firm value of $1,613, so equity comes out at $813, understating it by $260. Doing that and also forgetting to subtract debt gives $1,613, overstating equity by $540.

January 2021 default inputs for a US company: riskfree rate 0.93%; mature-market ERP 4.72%; expected return on the market 5.65%.

**Worked example (Embraer, 2004 — an emerging-market firm with lambda):**
- Riskfree rate (US$): 4.29%.
- Beta: 1.07 (bottom-up, unlevered 0.95 from aerospace comparables, relevered at D/E 18.95% with t = 34%).
- Mature-market premium: 4%.
- Country risk: Brazil CRP 7.89%, attached through lambda = 0.27.
- **Cost of equity = 4.29% + 1.07 × 4% + 0.27 × 7.89% = 10.70%.**
- Feeding the cost of capital: market equity 11,042m BR (84% weight), market debt 2,083m BR (16%), pre-tax cost of debt 9.29%, t = 34% → cost of capital = 10.70% × 0.84 + 9.29% × 0.66 × 0.16 = 9.97%.
- Converting to nominal Brazilian reais, route 1: with a 12% BR riskfree rate, cost of equity = 12% + 1.07 × 4% + 0.27 × 7.89% = **18.41%**.
- Converting to nominal reais, route 2 (differential inflation, applied to the cost of capital): (1.0997) × (1.08/1.02) − 1 = **16.44%**, with 8% Brazilian and 2% US inflation.

**Worked example (Vale, currency conversion of the cost of equity):** Vale's US$ cost of equity is 11.23% (bottom-up beta 1.1503, riskfree 2.75%, ERP 7.38%). With expected inflation of 9% in Brazil and 2% in the US: Cost of equity in nominal R$ = (1.1123) × (1.09/1.02) − 1 = **18.87%**. Cross-check by building it directly: 10.18% R$ riskfree rate + 1.15 × 7.38% = **18.67%**. The two agree to within 20 basis points, which is the consistency test.

**Worked example (Disney, November 2013 — a developed-market multinational):** Bottom-up levered beta 1.0013 (unlevered 0.9239 for operations, blended to 0.8978 with cash, relevered at a 13.10% market D/E); riskfree rate 2.75%; operation-weighted ERP 5.76% (not the raw US 5.50%). **Cost of equity = 2.75% + 1.0013 × 5.76% = 8.52%.** That 8.52% feeds a cost of capital of 8.52% × 0.8842 + 2.40% × 0.1158 = 7.81%. The divisional costs of equity built the same way ranged from 7.09% (Parks & Resorts) to 11.61% (Interactive), so a movie project returning 9.5% on equity clears the company average of 8.52% but fails the Studio Entertainment hurdle of 9.92% — and should be rejected.

**Determinism:**
- DETERMINISTIC: (Rf, β, ERP) → cost of equity, under any of the country-risk attachment forms; (cost of equity in one currency, two expected inflation rates) → cost of equity in another; (cost of equity, cost of debt, tax rate, market-value weights) → cost of capital; (divisional betas, divisional D/E, Rf, ERP) → divisional costs of equity.
- JUDGMENT: every input. The riskfree rate choice, the ERP method and vintage, the comparable set behind the beta, the leverage to relever at, the country-risk attachment mechanism, the inflation forecasts used in currency conversion, and whether the marginal investor is diversified.

**Pitfalls:**
- **Mismatching cash flows and discount rates.** Discounting equity cash flows at the cost of capital overstates equity value; discounting firm cash flows at the cost of equity understates it.
- Using a US$ riskfree rate with local-currency cash flows, or a nominal rate with real cash flows.
- Attaching country risk twice — once by adding the CRP and again by multiplying it through beta.
- Levering the beta on a net debt ratio while using gross debt in the cost-of-capital weights.
- Using the company-wide cost of equity for every division, which pushes capital toward the riskiest businesses.
- Mixing vintages: a 2021 riskfree rate with a 2013 country ERP table, or a 2020 beta with a 2021 leverage ratio.
- Converting currencies with realized rather than expected inflation, or with spot exchange rates rather than inflation differentials.
- Treating a cost of equity as fixed over a forecast in which leverage or the business mix will change.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.11-12, p.21-22, p.26, p.99, p.111-112
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.11-12, p.21-22, p.26, p.97, p.108-109
- corporate_finance--lecture_slides--cfpacket1spr20 p.144-146, p.173-177, p.200
- spreadsheet `wacccalc.xls` (Valuation Inputs collection): assembles riskfree rate, ERP approach, bottom-up or direct beta, and market-value weights into a cost of equity and a WACC

**Related:** [[riskfree-rate-fundamentals]], [[currency-riskfree-rate]], [[equity-risk-premium-basics]], [[implied-equity-risk-premium]], [[country-risk-premium]], [[operation-weighted-erp]], [[lambda-country-risk-exposure]], [[bottom-up-beta]], [[levering-and-unlevering-beta]], [[total-beta]], [[cost-of-capital]], [[cost-of-debt]], [[discount-rate-consistency]]

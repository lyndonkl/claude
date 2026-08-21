# Converting discount rates across currencies

**Core idea:** A discount rate estimated in one currency converts to another using only the two currencies' expected inflation rates. Currency is not a risk factor in itself; the difference between a dollar discount rate and a real discount rate is purely differential inflation. So the same business, valued in dollars and in reais, must produce the same value — but the reais version carries a much higher discount rate against much higher nominal cash flows. Two routes exist: rebuild every input with a local riskfree rate, or scale the finished dollar rate by the inflation ratio. Both should give nearly the same answer, and disagreement between them is a useful diagnostic.

**Formulas:**
- Differential-inflation conversion (the canonical form):
  Rate_LocalCurrency = (1 + Rate_US$) × (1 + Expected inflation_Local) / (1 + Expected inflation_US$) − 1
  - Applies to the cost of equity, the cost of debt, and the cost of capital alike.
  - Expected inflation rates are long-term expectations, not current-year rates.
- Direct rebuild (route 2):
  Cost of equity_Local = Local riskfree rate + Beta × ERP (+ lambda × country risk premium, if used).
  Cost of debt_Local = Local riskfree rate + Default spread.
  - This assumes the local government bond rate is a clean riskfree rate with no sovereign default risk embedded. If it is not, strip the country default spread out first.
- Real rate version: use the same formula with zero expected inflation to get a real discount rate for real cash flows.

**Procedure:**
1. Build the full cost of capital in the currency where your inputs are best — usually US dollars, where riskfree rates, betas and spreads are most reliable.
2. Decide the valuation currency. It must match the currency of the cash flows.
3. Estimate long-term expected inflation in both currencies. Sources: central bank targets, inflation-indexed bond breakevens, consensus long-run forecasts.
4. Apply the differential-inflation formula to whichever rate you need — cost of equity, cost of debt, or the assembled cost of capital.
5. Cross-check with route 2: rebuild the cost of equity from the local riskfree rate and see whether the two answers land close. A large gap usually means either the inflation assumptions are inconsistent with the local bond rate, or the local bond rate contains sovereign default risk you have not stripped.
6. Make sure the cash flows use the SAME inflation assumptions you used in the conversion. Converting the rate but not the cash flows changes the answer and is the most common error.
7. Document both inflation rates as explicit assumptions.

**Reference data:** Conversions from the packets.

| Case | Rate in source currency | Inflation (local / US) | Converted rate | Cross-check via local riskfree |
|---|---|---|---|---|
| Vale cost of equity | 11.23% (US$) | 9% / 2% | 18.87% (nominal R$) | 10.18% R$ riskfree + 1.15 × 7.38% = 18.67% |
| Vale cost of debt | 4.05% (US$) | 9% / 2% | 11.19% (nominal R$) | — |
| Vale cost of capital | 8.20% (US$) | 9% / 2% | 15.62% (nominal R$) | — |
| Embraer cost of capital | 9.97% (US$) | 8% / 2% | 16.44% (nominal BR) | — |
| Embraer cost of equity (route 2) | — | — | 18.41% with a 12% BR riskfree | 12% + 1.07 × 4% + 0.27 × 7.89% |
| Embraer cost of debt (route 2) | — | — | 13.00% with a 12% BR riskfree | 12% + 1% company spread |

Vale's divisional cost of capital in both currencies (see [[divisional-cost-of-capital]]): Metals & Mining 8.27% US$ / 15.70% R$; Iron Ore 8.13% / 15.55%; Fertilizers 9.14% / 16.63%; Logistics 7.59% / 14.97%; Vale Operations 8.20% / 15.62%.

**Worked examples:**

*Vale cost of equity, US$ to nominal reais.* Cost of equity in dollars is 11.23%. Expected inflation is 9% in Brazil and 2% in the US.
Cost of equity in R$ = 1.1123 × (1.09 / 1.02) − 1 = 1.1123 × 1.06863 − 1 = **18.87%**.
Cross-check by direct build-up: the R$ riskfree rate is 10.18%, and Vale's levered beta is 1.15 against a 7.38% ERP, giving 10.18% + 1.15 × 7.38% = 18.67%. The 20 basis point gap is small enough to accept.

*Vale cost of debt, US$ to nominal reais.* Cost of debt in dollars = 2.75% riskfree + 1.30% A− spread = 4.05%.
Cost of debt in R$ = 1.0405 × (1.09 / 1.02) − 1 = **11.19%**.

*Embraer cost of capital, US$ to nominal BR.* Dollar cost of capital 9.97%; Brazilian inflation 8%; US inflation 2%.
Cost of capital in BR = 1.0997 × (1.08 / 1.02) − 1 = **16.44%**.
Route 2 with a 12% BR riskfree rate gives a cost of equity of 12% + 1.07 × 4% + 0.27 × 7.89% = 18.41% and a cost of debt of 13%, which at 84/16 weights and a 34% tax rate produces about 16.84% — close enough to confirm the 16.44%, and the small gap reflects an inflation assumption slightly inconsistent with a 12% local riskfree rate.

**Determinism:**
- DETERMINISTIC: given a rate in one currency and two expected inflation rates, the converted rate is pure arithmetic. Route 2 is equally deterministic once the local riskfree rate, beta and premiums are set.
- JUDGMENT: the expected inflation rates. These are forecasts. The judgment needs central bank targets, the local inflation-indexed bond market if one exists, the gap between the local nominal government bond and the US bond, and long-run consensus forecasts. Small differences compound over a long forecast horizon.
- JUDGMENT: whether a local government bond rate qualifies as a riskfree rate. In many emerging markets it embeds sovereign default risk and must be adjusted before route 2 works.
- JUDGMENT: which route to prefer when the two disagree. Damodaran's practice is to build in the currency with the most reliable inputs and convert, using the direct rebuild as a check.

**Pitfalls:**
- Converting the discount rate but leaving the cash flows in the original currency's inflation terms. The two must move together.
- Using a spot exchange rate or a forecast exchange-rate path instead of the inflation differential.
- Using current-year inflation instead of long-term expected inflation.
- Treating a local government bond rate as riskfree when it carries sovereign default risk, which then double counts country risk against a country risk premium in the ERP.
- Concluding that a business is riskier because its local-currency discount rate is higher. The higher rate is inflation, not risk. Vale's iron ore business is not twice as risky in reais as in dollars.
- Applying the conversion to a real discount rate as though it were nominal.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.175, p.187, p.201
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.112
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.109
- corporate_finance--lecture_slides--cfpacket1spr20 p.186 (currency consistency requirement across cost of debt, cost of equity and cash flows)

**Related:** [[cost-of-capital-assembly]], [[divisional-cost-of-capital]], [[country-risk-in-cost-of-debt]], [[cost-of-debt-estimation-routes]], [[riskfree-rate]], [[cost-of-equity]], [[inflation-and-cash-flows]]

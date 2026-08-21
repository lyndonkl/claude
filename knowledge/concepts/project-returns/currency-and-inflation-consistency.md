# Currency and real-versus-nominal consistency

**Core idea:** Cash flows and the discount rate must be defined in the same terms. Cash flows in Brazilian reais require a discount rate denominated in reais. If the cash flows are nominal, the rate must be nominal; if real, real. Maintain that consistency and the project's NPV and accept/reject verdict are identical no matter which currency or convention you pick. Currency is a unit of measurement, not a source of value. The mechanics are purchasing power parity for the exchange rate path and the inflation differential for converting the discount rate. Currency risk itself normally earns no premium in the discount rate, because it is diversifiable for a geographically spread firm or globally diversified investors.

**Formulas:** Symbols: `i_f` = expected inflation in the foreign currency; `i_d` = expected inflation in the domestic (analysis) currency; `t` = year index.
- Expected exchange rate (purchasing power parity): `Rate_t = Spot rate × [(1 + i_f)/(1 + i_d)]^t`
- Discount rate conversion: `Cost of capital_foreign = (1 + Cost of capital_domestic) × (1 + i_f)/(1 + i_d) − 1`
- Real from nominal (Fisher): `(1 + nominal) = (1 + real) × (1 + inflation)`
- NPV invariance: `NPV in foreign currency / Spot rate = NPV in domestic currency`

**Procedure:**
1. Pick the analysis currency. Any choice works; pick the one in which forecasting is easiest, usually the currency in which most cash flows arise.
2. Pick nominal or real, and hold it. Nominal is the default because tax depreciation schedules are stated in nominal terms.
3. If converting currencies, get expected inflation for both. Build the forecast exchange rate path from purchasing power parity — depreciate the higher-inflation currency at the differential.
4. Convert the discount rate by scaling `(1 + rate)` by the inflation ratio. Do not just add the inflation difference.
5. Convert the perpetual growth rate too. Rio Disney grows at 2% in US dollars and 9% in reais, because that is the respective inflation rate in each currency.
6. Convert cash flows year by year at the corresponding forecast rate, then discount at the converted rate.
7. Verify invariance: the foreign-currency NPV divided by the *spot* rate must equal the domestic-currency NPV.
8. Decide separately whether currency risk deserves a discount-rate premium. It generally does not for a diversified firm. Non-diversifiable emerging-market political risk does, through a country risk premium in the equity risk premium.

**Reference data:** Rio Disney currency inputs (2020 packet):

| Input | Value |
|---|---|
| US expected inflation | 2% |
| Brazil expected inflation | 9% |
| Spot rate | 2.35 $R per US$ |
| US$ cost of capital (Brazil-adjusted theme parks) | 8.46% |
| $R cost of capital | (1.0846)(1.09/1.02) − 1 = 15.91% |
| Perpetual growth, US$ | 2% |
| Perpetual growth, $R | 9% |

Vale Labrador mine: costs are in Canadian dollars, revenues in US dollars. Parity (C$1 = US$1) is assumed to continue because interest and inflation rates are similar in the two currencies, so no PPP drift is modeled.

Risk-premium rules for foreign projects:

| Situation | Discount-rate treatment |
|---|---|
| Firm operates in many countries, or investors are globally diversified | No currency-risk premium |
| Project in another mature market (Germany, UK, France) | No premium |
| Diversifiable political risk | No premium |
| Emerging-market political risk that cannot be diversified and may cut expected life or cash flows | Add a country risk premium to the equity risk premium |

**Worked example:** Rio Disney redone in reais. Dollar cash flows are converted at PPP-forecast rates (2.35 rising to 4.56 by year 10), then discounted at 15.91%.

| Year | Cash flow ($) | $R/$ | Cash flow ($R) | Present value ($R) |
|---|---|---|---|---|
| 0 | −$2,000 | 2.35 | −R$ 4,700 | −R$ 4,700 |
| 1 | −$1,000 | 2.51 | −R$ 2,511 | −R$ 2,167 |
| 2 | −$859 | 2.68 | −R$ 2,305 | −R$ 1,716 |
| 3 | −$267 | 2.87 | −R$ 767 | −R$ 492 |
| 4 | $340 | 3.06 | R$ 1,043 | R$ 578 |
| 5 | $466 | 3.27 | R$ 1,527 | R$ 730 |
| 6 | $516 | 3.50 | R$ 1,807 | R$ 745 |
| 7 | $555 | 3.74 | R$ 2,076 | R$ 739 |
| 8 | $615 | 4.00 | R$ 2,458 | R$ 754 |
| 9 | $681 | 4.27 | R$ 2,910 | R$ 771 |
| 10 | $11,990 | 4.56 | R$ 54,720 | R$ 12,504 |
| **NPV** | | | | **R$ 7,745** |

Year 10 dollar flow of $11,990 = $715 annual cash flow + $11,275 terminal value. Convert the answer back at the *spot* rate: R$ 7,745 / 2.35 = **$3,296 million**, exactly the dollar NPV. Currency choice changed nothing.

The same logic answers the real-versus-nominal question. Estimating the Vale plant's cash flows in real terms and discounting at a real cost of equity gives the same NPV as the nominal analysis.

**Determinism:** DETERMINISTIC — feed a script the spot rate, two inflation rates, and a domestic discount rate. It returns the whole exchange-rate path, the converted discount rate, the converted growth rate, and the converted cash flows. The resulting foreign-currency NPV reconciles to the domestic answer at the spot rate. JUDGMENT — the inflation forecasts themselves, whether purchasing power parity is a reasonable model over the project horizon, and whether the project's political risk is diversifiable. That judgment needs country inflation forecasts, sovereign ratings or CDS spreads, and the firm's geographic footprint.

**Pitfalls:**
- Converting cash flows to a second currency but leaving the original discount rate in place. That is the single most common error, and it manufactures or destroys value out of nothing.
- Adding the inflation differential to the discount rate instead of scaling by the ratio.
- Forgetting to convert the perpetual growth rate along with the discount rate.
- Converting the final foreign-currency NPV back at a *forward* rate instead of the spot rate.
- Charging a currency-risk premium to a project in a mature market for a globally diversified firm.
- Confusing currency risk (diversifiable) with emerging-market political risk (partly not).

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.222-224
- corporate_finance--lecture_slides--cfpacket1spr20 p.250-253
- corporate_finance--lecture_slides--cfpacket1spr20 p.262
- corporate_finance--lecture_slides--cfpacket1spr20 p.271
- corporate_finance--lecture_slides--cfpacket1spr20 p.273

**Related:** [[project-hurdle-rate-selection]], [[npv-and-irr-mechanics]], [[terminal-value-and-project-life]], [[uncertainty-payback-sensitivity-simulation]], [[country-risk-premium]], [[acquisitions-as-projects]]

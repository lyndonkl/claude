# Currency invariance: value is the same in any currency

**Core idea:** Currency is a measurement unit, not a value driver. A Brazilian company can be valued in nominal reais, in US dollars, or in Swiss francs, and if the inputs are internally consistent the three answers must agree once converted at the current exchange rate. Consistency has one requirement: cash flows and discount rates must live in the same currency. A high-inflation currency raises growth rates **and** discount rates by roughly the inflation differential, and the two effects cancel. When someone tells you a company is worth more in dollars than in rupees, they have an inconsistency, not an insight.

**Formulas:**
- Riskfree rate in currency X, built from a currency with a reliable riskfree rate:
  `(1 + r_f,X) = (1 + r_f,US$) × (1 + expected inflation_X) / (1 + expected inflation_US$)`.
- Expected exchange rate under purchasing power parity:
  `E[FX_{t}] = FX_0 × [(1 + inflation_local)/(1 + inflation_foreign)]^t` — the higher-inflation currency depreciates by the inflation differential each year.
- Approximate translation of any nominal rate: `rate_X ≈ rate_Y + (inflation_X − inflation_Y)`.
- Growth cap: nominal stable growth in a currency cannot exceed that currency's riskfree rate, because the riskfree rate embeds expected inflation plus real growth. This holds when the riskfree rate is negative too.
- Real-terms alternative: value in real cash flows with a real discount rate and real growth; inflation drops out of both sides.

**Procedure:**
1. Pick the valuation currency. Anything works; pick the one your audience thinks in, or the one with the most reliable riskfree rate.
2. Build the riskfree rate for that currency. Either take a default-free government bond in that currency, or build it from a reliable riskfree rate plus the inflation differential (the formula above).
3. Set expected inflation for the valuation currency and keep it consistent everywhere: revenue growth, margins, terminal growth, and the discount rate.
4. Set the equity risk premium from the company's operating exposure, not from the currency ([[country-risk-exposure]]). The ERP is a **risk** number and does not change when you switch currency units.
5. Forecast cash flows in the chosen currency. If the underlying business earns in another currency, convert with PPP-consistent expected exchange rates, not with the spot rate held flat.
6. Cap stable growth at the currency's riskfree rate.
7. Cross-check by re-running the valuation in a second currency. If the two per-share values do not match at the current exchange rate, find the inconsistent input.

**Reference data:** Infosys valued twice — in Indian rupees (about 4% expected inflation) and in US dollars (about 1%). Every rate in the rupee column is higher by roughly the 3% inflation differential, and the value is the same.

| Input | In Indian rupees | In US$ |
|---|---|---|
| Riskfree rate | 5.00% | 2.00% |
| Expected inflation rate | 4.00% | 1.00% |
| Cost of capital — high growth | 12.50% | 9.25% |
| Cost of capital — stable growth | 10.39% | 7.21% |
| Expected growth rate — high growth | 12.01% | 8.78% |
| Expected growth rate — stable growth | 5.00% | 2.00% |
| Return on capital — high growth | 17.16% | 13.78% |
| Return on capital — stable growth | 10.39% | 7.21% |
| **Value per share** | **Rs 614** | **$12.79** (≈ Rs 614 at the current exchange rate) |

Built riskfree rates and negative riskfree rates in practice:
- Egyptian pound, December 2015: `r_f,EGP = 1.0227 × (1.097 / 1.015) − 1 = 10.53%`, from a US$ riskfree rate of 2.27%, Egyptian inflation of 9.7% and US inflation of 1.5%. That 10.53% then anchored the CIB Egypt valuation, with a cost of equity of 10.53% + 0.81 × 15.70% = 23.25%.
- Euro, September 2019: riskfree rate **−0.50%**. Heineken's stable growth was set to −0.5% to match, cost of equity = −0.50% + 1.20 × 6.83% = 7.66%, after-tax cost of debt = (−0.5% + 2%) × (1 − 0.25) = 1.13%, WACC 5.04%, terminal value = 2,972/(0.05 − (−0.005)) = €54,034m. Negative rates break nothing; they simply push nominal growth negative.
- US dollar valuations of foreign firms: Embraer valued in US$ at a 3.8% riskfree rate, then translated to R$15.72 per share ([[country-risk-exposure]]).

**Worked example:** Infosys. In rupees the stable growth rate is 5.00% and the stable cost of capital is 10.39%; in dollars they are 2.00% and 7.21%. Both differences are close to the 3% inflation gap (4% rupee inflation versus 1% dollar inflation). The stable-phase spread that actually drives the terminal value is nearly identical: 10.39% − 5.00% = 5.39% in rupees and 7.21% − 2.00% = 5.21% in dollars. Because the spread survives the currency change, so does the value: Rs 614 per share, which is $12.79 at the prevailing exchange rate.

**Determinism:** DETERMINISTIC — (US$ riskfree rate, expected inflation in both currencies) → the local riskfree rate; (spot rate, inflation differential, horizon) → expected exchange rates; and the whole valuation once the consistent input set exists. JUDGMENT: the expected inflation rates themselves (needs central bank targets, market-implied breakevens, or the local government bond yield less a default spread), whether a local government bond is genuinely default-free, and the real growth and real return assumptions that survive the currency change.

**Pitfalls:**
- Discounting local-currency cash flows at a US-dollar cost of capital. This is the classic error and it always inflates value.
- Using a local government bond yield as the riskfree rate when that government can default. Strip the default spread out first, or build the rate from the inflation differential.
- Holding the spot exchange rate flat across a ten-year forecast for a high-inflation currency.
- Letting stable growth exceed the currency's riskfree rate — an automatic value machine, and always wrong.
- Changing the equity risk premium when you change currency. The ERP tracks operating exposure, not the unit of account.
- Refusing to model a negative riskfree rate. The framework handles it; it just means negative nominal stable growth.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.328-329
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.342
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.319-320
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.333

**Related:** [[country-risk-exposure]], [[declining-firm-valuation]], [[financial-service-firm-valuation]], [[difficult-company-taxonomy]], [[riskfree-rate]], [[terminal-value]]

# Currency-Consistent Valuation and Riskfree Rates by Currency

**Core idea:** The same project or company shows very different numbers in US dollars than in, say, Indonesian Rupiah. Those gaps do not come from country risk or from anything about the business, because neither changes when you switch currencies. They come entirely from the different expected inflation rates embedded in each currency. Higher inflation in a currency raises both the interest rates you observe in it and the nominal growth rates you should forecast in it. The discipline this demands is simple to state and easy to violate: the currency of your cash flows and the currency of your discount rate must match, and the same expected inflation must sit on both sides. Get that right and value is, in principle, invariant to the currency you choose.

**Formulas:**
- The valuation identity, in one currency throughout: `Value = E(CF_1)/(1+r) + E(CF_2)/(1+r)^2 + … + E(CF_n)/(1+r)^n`. `E(CF_t)` = expected cash flow in year t stated in the chosen currency; `r` = discount rate in that same currency.
- Discount rate build-up: `r = Expected inflation in the currency + Real interest rate + Risk premium for company characteristics`.
- Cash flow build-up: `Growth in cash flows = Expected inflation in the currency + Real growth in the economy and the company`.
- Riskfree rate from a government bond: `Riskfree rate in a currency = Government bond rate in that currency − Default spread for the sovereign's rating`.
- Differential inflation, approximate: `Rate in currency X ≈ US$ rate + (Expected inflation in X − Expected inflation in US$)`.
- Differential inflation, exact: `Rate in currency X = (1 + US$ riskfree rate) × (1 + Expected inflation in X) / (1 + Expected inflation in US$) − 1`.

**Procedure:**
1. Choose the currency for the valuation and declare it. Any currency is legitimate; the only sin is mixing.
2. Get the riskfree rate in that currency. Start from the local 10-year government bond rate, then subtract the default spread implied by that sovereign's rating. A government bond rate is not a riskfree rate unless the sovereign is default-free.
3. If the local bond market is illiquid, manipulated, or missing, build the rate instead from differential inflation. Take the US dollar riskfree rate and scale it by the ratio of expected inflation in the two currencies, using the exact compounded form.
4. Cross-check the two estimates. If the bond-derived rate and the differential-inflation rate disagree sharply, the local bond market is probably distorted; prefer the differential-inflation estimate and say so.
5. Forecast cash flows in the same currency, growing them at that currency's expected inflation plus real growth. Do not take a dollar-based real growth rate and apply it to rupiah cash flows without re-inflating.
6. Build the discount rate on the same inflation assumption used in the growth rates. This is the single consistency check that catches most currency errors.
7. If you must report in a different currency, either translate the finished value at the spot rate, or convert the cash flows year by year using forecast exchange rates. Do not switch mid-model.
8. Verify invariance as a test. Value the same business in two currencies. If the answers differ materially, you have an inconsistency, not an insight.

**Reference data:** Riskfree rates by currency, July 2020 (Damodaran, Foundations of Finance Session 12; government-bond-based estimates, read from a bar chart, so treat as illustrative). Each bar is a government bond rate split into a true riskfree rate plus a rating-based default spread. Approximate total government bond rates:

| Currency band | Currencies | Approximate government bond rate |
|---|---|---|
| Negative or near zero | Euro, Swiss Franc, Japanese Yen, Danish Krone, Swedish Krona | below ~0.5% |
| Low single digits | US $, Canadian $, Australian $, Singapore $, NZ $, British Pound | ~0.5-2% |
| Mid single digits | Russian Ruble, Brazilian Real, Indian Rupee | ~6% |
| Upper single digits | Indonesian Rupiah ~7%, Pakistani Rupee ~9%, Nigerian Naira ~9%, South African Rand ~9% | 7-9% |
| Extremes | Kenyan Shilling ~12%, Turkish Lira ~12%, Zambian Kwacha ~38% (of which about 27% is the local rate before spread) | 12-38% |

The spread across roughly forty currencies is driven mainly by inflation differences, with sovereign default risk explaining the rest.

**Worked example:** Egyptian pound riskfree rate, December 2015. Inputs: US dollar riskfree rate on 12/31/15 = 2.27%; expected US inflation = 1.50%; expected Egyptian inflation = 9.70%. Exact differential-inflation form: `(1.0227) × (1.097 / 1.015) − 1 = 1.0227 × 1.08079 − 1 = 10.53%`. The additive shortcut would give `2.27% + (9.70% − 1.50%) = 10.47%`, which is close here but drifts further apart as inflation rises. A valuation of an Egyptian company run in Egyptian pounds must therefore start from a roughly 10.5% riskfree rate, and its cash flows must grow at Egyptian inflation of about 9.7% plus real growth. Run the same company in dollars and both numbers drop by roughly the inflation differential — the value should not move.

**Determinism:**
- DETERMINISTIC: `government bond rate − default spread` → riskfree rate. The differential-inflation conversion, both forms, given the US rate and the two expected inflation rates. The present-value sum once cash flows and `r` are set.
- JUDGMENT: the expected inflation rate in each currency; whether the local government bond market is trustworthy; the sovereign rating and its default spread; the real growth rate for the economy and the company; the company risk premium. Estimating expected inflation for an emerging-market currency needs the country's inflation history, its monetary regime, and any market-implied measures available.

**Pitfalls:**
- Discounting local-currency cash flows at a US dollar discount rate, or the reverse. This is the classic mismatch and it moves value by the full inflation differential each year.
- Treating a high local interest rate as evidence of country risk. Most of the gap is inflation, and country risk should enter through the risk premium, not through the currency.
- Using a government bond rate directly as the riskfree rate for a sovereign that is not default-free.
- Trusting a quoted local rate in a currency whose bond market is illiquid or state-controlled. Sanity-check it with differential inflation.
- Assuming that switching currencies should change value. If it does, the model is inconsistent.

**Sources:**
- `foundations_of_finance--exchange_rates p.2-5, p.8`

**Related:** [[exchange-rate-forecasting-with-parity]], [[fisher-equation-and-intrinsic-riskfree-rate]], [[real-vs-nominal-conversion]], [[inflation-measurement-and-causes]], [[default-risk-and-default-spreads]], [[cost-of-capital]], [[country-risk-premium]]

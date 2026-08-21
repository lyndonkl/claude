# Real versus Nominal Conversion

**Core idea:** We live in a nominal world. Wages, taxes, returns, and reported cash flows are all stated in current currency units. Inflation quietly eats what those amounts are worth, which is why Damodaran calls it "the hidden tax." A return, a growth rate, or a cash flow can be stated either in nominal terms (current dollars) or real terms (constant purchasing power), and the conversion between them runs through the inflation rate. The rule that matters in valuation is consistency: nominal cash flows must be discounted at nominal rates, and real cash flows at real rates. Over long horizons the compounding gap between the two is enormous, so getting this wrong is not a rounding error.

**Formulas:**
- Approximation: `Nominal return ≈ Real return + Inflation`. Adequate only when both terms are small.
- Exact, returns: `(1 + Nominal return) = (1 + Real return) × (1 + Inflation rate)`, so `Real return = (1 + Nominal return)/(1 + Inflation rate) − 1`.
- Growth rates, shortcut: `Real growth = Nominal growth − Inflation`.
- Growth rates, exact: `Real growth = (1 + Nominal growth)/(1 + Inflation) − 1`.
- Cash flows: `Real CF_t = Nominal CF_t / (1 + Inflation rate)^t`. `t` = number of years in the future the cash flow occurs; `Inflation rate` = expected annual inflation over that horizon.
- Symbols throughout: `Nominal` = stated in current currency; `Real` = stated in constant purchasing power of the base date; `Inflation rate` = the rate over the same period as the return or growth rate.

**Procedure:**
1. Decide which basis the valuation will run in and write it at the top of the model. Nominal is the default, because reported financials, interest rates, and tax rules are all nominal.
2. Convert every input onto that basis before using it. A real growth rate cannot be applied to a nominal base-year cash flow.
3. Use the exact multiplicative form whenever inflation exceeds roughly 3-4%, or whenever the horizon is long. The additive shortcut understates the correction, and the error compounds.
4. For a stream of cash flows, deflate each year by the *cumulative* inflation factor `(1 + i)^t`, not by a single year's inflation.
5. Keep the discount rate on the same basis. A real discount rate is built from a real riskfree rate (the TIPS rate is the market's measure) plus a risk premium.
6. Check tax treatment. Taxes are levied on nominal income, so a real-terms model must still capture the nominal tax bill. This is the most common place a real-basis model breaks.
7. Report both if the audience needs it. Real numbers answer "will I be better off?"; nominal numbers answer "how many dollars will there be?".

**Reference data:** Average annual US stock returns by decade, nominal versus real (Damodaran, Foundations of Finance Session 10; data through 2019):

| Decade | Nominal | Real |
|---|---|---|
| 1930-1939 | 4.27% | 6.23% |
| 1940-1949 | 9.64% | 4.10% |
| 1950-1959 | 20.93% | 18.59% |
| 1960-1969 | 8.60% | 6.21% |
| 1970-1979 | 6.30% | −0.14% |
| 1980-1989 | 17.95% | 11.86% |
| 1990-1999 | 18.82% | 15.42% |
| 2000-2009 | 1.16% | −1.27% |
| 2010-2019 | 14.02% | 11.99% |

Two features are worth memorizing. In the 1970s stocks earned 6.30% nominal but −0.14% real, so a decade of apparent gains bought nothing. In the 1930s the real return of 6.23% *exceeded* the nominal 4.27%, because prices were falling. The sign of the correction flips with deflation.

**Worked example:** $100 invested in US stocks at the start of 1928 and compounded through 2019 grows to $502,417.21 in nominal terms. Restated in 1928 purchasing power it is only $33,953.22 — roughly fifteen times less. The nominal wealth line explodes upward after the 1980s while the real line stays nearly flat on the same scale. That ratio is the cumulative bite of the hidden tax over 92 years. (Source: Damodaran, Foundations of Finance Session 10, US equity returns 1928-2019.)

A single-year check on the same machinery: a 14.02% nominal return with 2% inflation gives a real return of `1.1402/1.02 − 1 = 11.78%`, whereas the additive shortcut would say 12.02%. The 24-basis-point error looks trivial for one year and costs a great deal over thirty.

**Determinism:**
- DETERMINISTIC: every conversion here. Inputs `(nominal return, inflation)` → real return, exactly, and every rearrangement. Inputs `(nominal CF_t, inflation, t)` → real CF_t. Inputs `{annual nominal returns}` and `{annual inflation rates}` → compounded nominal and real wealth paths, as in the $100-in-1928 example.
- JUDGMENT: the expected inflation rate to use, especially over long horizons; which inflation index applies to these particular cash flows; whether to run the model in nominal or real terms at all. That judgment needs an inflation forecast, the currency of the cash flows, and the tax regime.

**Pitfalls:**
- Discounting nominal cash flows at a real rate, or the reverse. This is the single most common mismatch, and it always biases value in a predictable direction: nominal cash flows at a real rate massively overstate value.
- Using the additive shortcut in a high-inflation currency, where the error is large and one-directional.
- Deflating a year-t cash flow by one year of inflation instead of `(1+i)^t`.
- Forgetting that deflation reverses the sign of the adjustment, so real returns exceed nominal ones.
- Building a real-terms model and then applying nominal tax rules inconsistently.
- Presenting long-horizon nominal wealth figures without the real counterpart, which flatters performance enormously.

**Sources:**
- `foundations_of_finance--inflation p.7-11`

**Related:** [[inflation-measurement-and-causes]], [[fisher-equation-and-intrinsic-riskfree-rate]], [[currency-consistent-valuation]], [[time-value-of-money-and-discount-rates]], [[compounding-frequency-and-effective-rates]]

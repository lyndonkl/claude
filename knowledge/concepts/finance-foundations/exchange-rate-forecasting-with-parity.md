# Forecasting Exchange Rates with Parity Conditions

**Core idea:** Once you commit to currency-consistent valuation, you often need future exchange rates — to convert local-currency cash flows into a reporting currency, for instance. There are three ways to get them. You can forecast yourself, you can read market forward and futures rates, or you can apply a parity condition. Damodaran's advice is blunt on the first: do not. Exchange rate forecasting is done badly even by the best forecasters, and embedding your currency view in a project analysis means the investment decision ends up driven by that view rather than by the project. Use market forwards when a liquid quote exists for your horizon. Otherwise use interest rate parity (which turns the interest-rate gap into a forward rate) or purchasing power parity (which turns the inflation gap into an expected rate path).

**Formulas:**
- Interest rate parity, one year: `XRF($/Euro) = XR($/Euro) × (1 + r_US$) / (1 + r_Euro)`. `XR` = current spot exchange rate in dollars per euro; `r_US$` and `r_Euro` = interest rates in the two currencies for the matching horizon; `XRF` = expected future (forward) rate in dollars per euro.
- Interest rate parity, t years: `XRF_t = XR × (1 + r_US$)^t / (1 + r_Euro)^t`, using rates compounded over t years.
- Purchasing power parity, one year: `XRF($/Rs) = XR($/Rs) × (1 + i_$) / (1 + i_Rs)`. `i_$` and `i_Rs` = expected inflation in the two currencies; `XR` = spot rate in dollars per rupee.
- Purchasing power parity, t years: `XRF_t = XR × (1 + i_$)^t / (1 + i_Rs)^t`.
- Reading the direction: in a `$/foreign` quote, a *falling* number means the foreign currency is depreciating against the dollar.

**Procedure:**
1. Fix the quote convention before anything else and write it down. This note uses dollars per unit of foreign currency throughout. Inverting the quote inverts the formula.
2. Check for a market forward rate at your horizon. For widely held currencies such as the dollar and euro, forwards are cheap and available out to three, five, even ten years. Use the mid quote.
3. For emerging-market currencies, expect the forward curve to stop at one or two years, or not to exist at all. A bank will quote a customized forward, but that is a bank's price, not a market consensus.
4. Where forwards run out, switch to a parity condition for the remaining years. Use interest rate parity when you trust the interest rates in both currencies for the horizon. Use purchasing power parity when you trust the inflation forecasts more than the rates, which is the common case in emerging markets and for long horizons.
5. Match the horizon of your inputs to the horizon of your forecast. One-year rates give a one-year forward. A two-year forward needs rates compounded over two years, not one-year rates squared onto a one-year answer.
6. Build the whole path, not just the endpoint. Each year's rate equals the prior year's rate times the parity ratio, so a ten-year forecast is a ten-step compounding.
7. Apply the path to the cash flows year by year, then discount in the reporting currency. Do not translate the finished value at the spot rate if the currencies have very different inflation.
8. Keep your own currency views out of it. If you genuinely can forecast exchange rates, there are far easier ways to make money than running a business.

**Reference data:**

US dollars per Euro forward rates quoted 7/24/2020 (Damodaran, Foundations of Finance Session 12):

| Expiration | Ask | Bid | Mid |
|---|---|---|---|
| Current (spot) | 1.1662 | 1.1653 | 1.1657 |
| Six months | 1.1712 | 1.1702 | 1.1707 |
| One year | 1.1756 | 1.1745 | 1.1750 |
| Two years | 1.1858 | 1.1838 | 1.1848 |
| Three years | 1.1968 | 1.1948 | 1.1958 |
| Four years | 1.2098 | 1.2068 | 1.2083 |
| Five years | 1.2235 | 1.2206 | 1.2220 |
| Six years | 1.2393 | 1.2343 | 1.2368 |
| Seven years | 1.2546 | 1.2496 | 1.2521 |
| Ten years | 1.3025 | 1.2935 | 1.2980 |

The dollar price of the euro rises from about 1.166 spot to about 1.298 at ten years. That upward slope is exactly what interest rate parity predicts when euro rates sit below dollar rates.

Purchasing power parity ten-year paths against the US dollar, assuming 2% expected US inflation (Damodaran, Session 12). Expected local inflation: India 6.00%, Brazil 9.00%, Switzerland 0.50%.

| Year | $/Indian Rupee | $/Brazilian Real | $/Swiss Franc |
|---|---|---|---|
| Current | 0.0130 | 0.1900 | 1.0900 |
| 1 | 0.0125 | 0.1778 | 1.1063 |
| 2 | 0.0120 | 0.1664 | 1.1228 |
| 3 | 0.0116 | 0.1557 | 1.1395 |
| 4 | 0.0111 | 0.1457 | 1.1565 |
| 5 | 0.0107 | 0.1363 | 1.1738 |
| 6 | 0.0103 | 0.1276 | 1.1913 |
| 7 | 0.0099 | 0.1194 | 1.2091 |
| 8 | 0.0096 | 0.1117 | 1.2272 |
| 9 | 0.0092 | 0.1045 | 1.2455 |
| 10 | 0.0088 | 0.0978 | 1.2641 |

The rupee and the real depreciate against the dollar every year, because their inflation exceeds 2%. The Swiss franc appreciates, because 0.5% inflation sits below US inflation.

**Worked example:** Interest rate parity on the euro. Spot is $1.1662 per euro, the one-year US interest rate is 2%, and the one-year euro rate is 1%. Then `XRF = 1.1662 × 1.02 / 1.01 = $1.1777 per euro` one year forward. The euro is expected to strengthen by about 1%, exactly the interest differential.

Purchasing power parity on the rupee. Spot is $0.013 per rupee, expected Indian inflation is 10%, expected US inflation is 1%. Next year: `0.013 × 1.01/1.10 = $0.0119`. Two years out: `0.013 × 1.01²/1.10² = $0.0110`. The rupee is expected to lose roughly 9% a year against the dollar, which is the inflation gap.

**Determinism:**
- DETERMINISTIC: both parity formulas and the full multi-year path. Inputs `(spot rate, r_domestic, r_foreign, t)` → forward rate. Inputs `(spot rate, i_domestic, i_foreign, t)` → expected rate at year t. Reading a quoted forward rate off a curve.
- JUDGMENT: the expected inflation rates that feed purchasing power parity. Also whether local interest rates are trustworthy enough for interest rate parity, whether a bank-quoted emerging-market forward is fair, and which estimate wins when forwards and parity disagree. These need the country's inflation history and monetary regime, plus the liquidity of the local rate and forward markets.

**Pitfalls:**
- Embedding a personal currency view in a project valuation. The investment decision then turns on the currency call rather than on the business, which muddies the judgment you were actually trying to make.
- Inverting the quote convention halfway through, which flips the direction of the expected move.
- Mismatching horizons — using one-year interest rates to build a five-year forward.
- Assuming forward markets exist at your horizon for an emerging-market currency. They usually stop at one or two years.
- Treating a bank's customized forward quote as a market consensus forecast.
- Converting the finished valuation at today's spot rate when the two currencies have very different inflation, instead of converting the cash flows year by year.

**Sources:**
- `foundations_of_finance--exchange_rates p.6-7, p.9-13`

**Related:** [[currency-consistent-valuation]], [[fisher-equation-and-intrinsic-riskfree-rate]], [[real-vs-nominal-conversion]], [[inflation-measurement-and-causes]], [[finance-first-principles]]

# Inflation: Measurement, Biases and Causes

**Core idea:** Inflation is a general rise in the price level; deflation is a general fall. Individual prices can rise with no inflation at all, if offsets elsewhere keep the overall level flat. Those relative price moves still hurt or help whoever buys the affected goods, but they do not register as inflation. Finance cares because inflation changes how a cash flow today compares with an equal cash flow later. Any inflation number you use is an estimate built on a chosen perspective and a chosen basket of goods, produced mostly by governments that have an interest in the answer. Treat it as a measurement with error bars, not as a fact.

**Formulas:**
- Period inflation from an index: `Inflation_t = Index_t / Index_{t−1} − 1`. `Index` = the price index level (CPI, PPI, or GDP deflator) at that date.
- Compound average inflation over N years: `(Index_N / Index_0)^(1/N) − 1`.
- GDP deflator inflation: `(1 + nominal GDP growth) / (1 + real GDP growth) − 1`.

**Procedure:**
1. Pick the perspective first. Consumers or producers? That choice determines the index family before any number is looked up.
2. Pick the index. CPI tracks prices paid by consumers for a market basket of goods and services. PPI tracks prices received by producers. The GDP deflator is derived from nominal and real GDP and covers all goods and services in the economy.
3. Match the index to the cash flows you are adjusting. Use CPI for consumer-facing revenues and wages, PPI for input costs and industrial pricing, the GDP deflator for economy-wide aggregates.
4. Interrogate the basket. Ask whether the basket reflects what this business actually buys or sells. A mis-specified or stale basket makes measured inflation drift from the inflation that matters to your cash flows.
5. Check the price sources. How and when prices are observed changes the reported number.
6. Apply a skepticism discount where warranted. Most inflation rates are produced by governments or their agencies, and most governments prefer a lower reported rate. In countries with a track record of statistical manipulation, cross-check against market-implied inflation or against a differential-inflation estimate.
7. When forecasting inflation, reason from the three drivers rather than extrapolating. Large government spending it cannot fund (crises, wars) pushes inflation up. High real growth pushes prices up as spendable income outruns production. Loose monetary policy raises inflation over the long term; inflation is at root a monetary phenomenon.

**Reference data:** Average annual US inflation by measure and period, 1914-2019 (Damodaran, Foundations of Finance Session 10; data through 2019):

| Period | CPI | PPI | GDP deflator |
|---|---|---|---|
| 1914-1919 | 14.48% | 11.45% | NA |
| 1920-1939 | −2.69% | −1.39% | NA |
| 1940-1959 | 4.56% | 3.88% | 2.15% |
| 1960-1979 | 5.13% | 4.97% | 5.20% |
| 1980-1999 | 2.22% | 4.04% | 3.18% |
| 2000-2019 | 2.34% | 2.14% | 1.81% |

Shape of the history: violent swings early in the century, with spikes above +30% around WWI and the mid-1940s and drops below −20% in the early 1920s and early 1930s. A high-inflation episode ran through the 1970s, peaking around 10-20%. Rates have been much lower and more stable since the early 1980s. The three measures move together but are not interchangeable, and PPI swings the most.

**Worked example:** Suppose you are valuing a US consumer-products company and need a long-run inflation assumption. The 2000-2019 CPI average is 2.34%, PPI is 2.14%, and the GDP deflator is 1.81%. If you take the GDP deflator (1.81%) for revenue growth but the PPI (2.14%) for input costs, you have quietly assumed 33 basis points of annual margin compression for the entire forecast. That assumption should be deliberate, not a by-product of picking indices carelessly. For a single economy-wide assumption over 2000-2019, the three measures bracket a range of 1.81% to 2.34%, and the width of that range is the honest uncertainty in the input.

**Determinism:**
- DETERMINISTIC: computing inflation rates and period averages from published index levels. Inputs `{Index_t}` → annual and multi-year average inflation. Deriving deflator inflation from nominal and real GDP growth.
- JUDGMENT: which index to use; whether the official number is credible; what the basket should be for a specific business; forecasting future inflation. That judgment needs the composition of the index basket, the business's own input and output mix, the country's statistical track record, and a view on fiscal and monetary policy.

**Pitfalls:**
- Treating CPI, PPI, and the GDP deflator as one number. They differ persistently, and in 1980-1999 the CPI-PPI gap was 182 basis points a year.
- Confusing a relative price change with inflation. A rising price for one good is not inflation if other prices are falling.
- Accepting official inflation uncritically, particularly where the measuring agency answers to a government that benefits from a low print.
- Using a consumer basket to inflate industrial input costs, or the reverse.
- Assuming past inflation predicts future inflation across a regime change. The pre-1980 and post-1980 US series behave like two different worlds.

**Sources:**
- `foundations_of_finance--inflation p.2-6`

**Related:** [[real-vs-nominal-conversion]], [[fisher-equation-and-intrinsic-riskfree-rate]], [[currency-consistent-valuation]], [[exchange-rate-forecasting-with-parity]], [[time-value-of-money-and-discount-rates]]

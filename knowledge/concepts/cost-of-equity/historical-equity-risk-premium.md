# Historical equity risk premium

**Core idea:** The historical premium is what stocks actually earned over riskless securities in the past, averaged over a long window. Practitioners treat it as a fact. It is an estimate, and a noisy one. Three choices move it by several percentage points: how far back you go, whether the riskless benchmark is T.Bills or T.Bonds, and whether you average arithmetically or geometrically. Two structural problems compound this: the standard error of the estimate exceeds 2% even with 90+ years of data, and US data suffers survivorship bias because the US was one of the twentieth century's most successful equity markets.

**Formulas:**
- Historical ERP = Average annual return on a stock index over the period − Average annual return on the riskless security over the same period.
- Standard error of the premium = Annualized standard deviation of stock returns / sqrt(Number of years of data).
  Example: 20% / sqrt(90) = 2.1%.
- Arithmetic average = simple mean of annual excess returns. Geometric (compounded) average = (ending value / beginning value)^(1/n) − 1 differenced against the riskless compounded return.

Symbols: n = number of years in the estimation window; the riskless security is either 3-month T.Bills or 10-year T.Bonds, and the choice must match the riskfree rate used in the cost of equity.

**Procedure:**
1. Define the estimation period. Use the **longest** available (1928-present for the US). Short windows have huge standard errors — the 2011-2020 arithmetic stocks-over-T.Bonds premium is 9.70% with a standard error of 4.87%, which is meaningless.
2. Choose the riskless benchmark to **match** the riskfree rate you will use in the cost of equity. If you discount with a 10-year T.Bond rate, use the stocks-over-T.Bonds premium.
3. Choose the averaging method. Use the **geometric (compounded)** average. Arithmetic averages overstate long-horizon expected returns because returns are serially correlated and compounding matters over multi-year horizons.
4. Compute the standard error and report it. If the standard error is a large fraction of the premium, say so.
5. Check the survivorship-bias exposure. If your window is US-only twentieth century, consider the global cross-section (table below): the world premium of 3.20% is well below the US 4.40%.
6. Decide whether to use the historical premium at all. It is defensible only if you believe premiums revert to historical norms *and* your valuation horizon is long enough to realize those norms. Otherwise use the implied premium — see [[choosing-an-equity-risk-premium]].

**Reference data:**

US historical equity risk premiums, through 2020:

| Period | Arithmetic: Stocks − T.Bills | Arithmetic: Stocks − T.Bonds | Geometric: Stocks − T.Bills | Geometric: Stocks − T.Bonds |
|---|---|---|---|---|
| 1928-2020 | 8.28% | 6.43% | 6.47% | 4.84% |
| Std error (1928-2020) | 2.06% | 2.18% | — | — |
| 1971-2020 | 7.67% | 4.90% | 6.35% | 3.91% |
| Std error (1971-2020) | 2.38% | 2.70% | — | — |
| 2011-2020 | 13.83% | 9.70% | 13.24% | 9.35% |
| Std error (2011-2020) | 3.88% | 4.87% | — | — |

(Through 2019: 1928-2019 arithmetic 8.18% / 6.43%, geometric 6.35% / 4.83%; 1970-2019 arithmetic 7.26% / 4.50%, geometric 5.93% / 3.52%; 2010-2019 arithmetic 13.51% / 9.67%, geometric 12.93% / 9.31%.)

Global historical premiums, geometric mean of stocks over bonds, 1900-2017:

| Country | Geometric mean | Std error | Country | Geometric mean | Std error |
|---|---|---|---|---|---|
| Australia | 5.00% | 1.70% | Norway | 2.40% | 2.50% |
| Austria | 2.90% | 14.10% | Portugal | 5.30% | 2.90% |
| Belgium | 2.20% | 1.90% | South Africa | 5.30% | 1.80% |
| Canada | 3.50% | 1.70% | Spain | 1.80% | 1.90% |
| Denmark | 2.20% | 1.70% | Sweden | 3.10% | 2.00% |
| Finland | 5.20% | 2.70% | Switzerland | 2.20% | 1.60% |
| France | 3.10% | 2.10% | U.K. | 3.70% | 1.60% |
| Germany | 5.10% | 2.60% | U.S. | 4.40% | 1.90% |
| Ireland | 2.70% | 1.80% | Europe | 3.00% | 1.40% |
| Italy | 3.20% | 2.70% | World ex-U.S. | 2.80% | 1.30% |
| Japan | 5.10% | 3.00% | **World** | **3.20%** | **1.40%** |
| Netherlands | 3.30% | 2.00% | | | |
| New Zealand | 4.00% | 1.60% | | | |

**Worked example:** An analyst wants a historical US premium in January 2021 to pair with the 0.93% 10-year T.Bond rate. Matching the benchmark to T.Bonds and taking the longest window and the geometric average gives **4.84%** (1928-2020). Switching to the arithmetic stocks-over-T.Bills figure from the same window gives 8.28% — a 3.44-percentage-point swing from two formatting choices, and it would raise a beta-1 cost of equity from 5.77% to 9.21%. The implied premium on that date was 4.72%, very close to the geometric T.Bond figure, and far from the arithmetic T.Bill figure.

**Determinism:**
- DETERMINISTIC: (return series for stocks, return series for the riskless asset, period, averaging method) → historical premium; (annualized standard deviation, years of data) → standard error. A script can reproduce every cell of the table above from raw return data.
- JUDGMENT: which of the twelve cells in the table to use; whether US data is representative; whether to correct for survivorship bias and by how much; whether history is the right guide at all.

**Pitfalls:**
- Quoting a single number as "the" historical premium without stating period, benchmark, and averaging method.
- Using a short recent window because it "reflects current conditions". Short windows are pure noise (std errors of 4-5%).
- Mismatching the benchmark: using a stocks-over-T.Bills premium with a T.Bond riskfree rate double-counts the term premium.
- Preferring the arithmetic average because it is larger, or because "expected returns are arithmetic". Over multi-year valuation horizons the compounded average is the right one.
- Ignoring survivorship bias. Ex ante, an investor in 1900 could not know the US would be the winner.
- Using the arithmetic 1928-2020 T.Bill premium of 8.28% in January 2021, when the implied premium was 4.72%. Every stock you value will look overvalued.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.45-48, p.76
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.45-48, p.74
- corporate_finance--lecture_slides--cfpacket1spr20 p.114-115, p.118

**Related:** [[equity-risk-premium-basics]], [[implied-equity-risk-premium]], [[choosing-an-equity-risk-premium]], [[country-risk-premium]], [[riskfree-rate-fundamentals]]

# Step 1: Survey the landscape

**Core idea:** Before you can write a narrative you have to know the terrain. The survey covers four things: the company (its products, its management, its history), the market or markets it will grow in, the competition it faces now and will face later, and the macro environment it operates in. The output is not numbers. It is a business-model map plus a set of benchmarks that tell you what is normal in this business. Those benchmarks are what stop the later story from drifting into fantasy. In practice the survey has a numeric half too: update the base-year financials, clean them for accounting distortions, and get an honest share count.

**Formulas:**
- Trailing 12-month figure = Last 10-K figure − first X months of last year + first X months of this year. Use trailing numbers, not the stale annual report.
- Annualised recent revenue growth = (Revenues_now / Revenues_last10K)^(1 / years since last 10-K) − 1.
- Sales-to-capital ratio = Revenues / Invested capital. Invested capital = Book equity + Book debt − Cash, plus the capitalised research asset and any lease asset.
- ROIC = After-tax operating income / Invested capital.
- If you are not working in US dollars, add the inflation differential to any US-dollar industry averages before comparing.

**Procedure:**
1. **Map the business model.** Who are the suppliers and the customers? How does money move? Who sets price? What slice does the company keep? What does it have to invest in to grow? Draw it as a loop, not a list.
2. **Update the base year.** Pull trailing-12-month revenues, EBIT, interest expense, book equity, book debt and cash. Note how many years have passed since the last 10-K.
3. **Clean up the accounting.** Capitalise R&D and add the amortisation-adjusted amount back to EBIT. Convert operating lease commitments to debt and adjust EBIT accordingly. Both change invested capital, and therefore ROIC and sales-to-capital.
4. **Get a comprehensive share count.** Actual shares outstanding, plus a separate list of employee options with strike, maturity and volatility. Options are neither shares nor nothing.
5. **Benchmark against the industry.** Compare revenue growth, pre-tax operating margin, sales-to-capital, ROIC and cost of capital to US and global industry averages.
6. **Benchmark against the biggest incumbents.** For a company claiming it will become the largest player, look at what the largest players actually earn.
7. **Learn from history without being enslaved by it.** Quarterly history shows the direction of travel — use the trend to test whether the story's claimed inflection has already started.

**Reference data:** Tesla vs the auto industry, November 2021 (most recent year):

| Metric | Tesla | Industry (US) | Industry (Global) |
|---|---|---|---|
| Revenue growth in most recent year | 69.50% | 14.31% | 4.97% |
| Pre-tax operating margin | 12.06% | 3.41% | 4.79% |
| Sales to capital ratio | 1.68 | 0.87 | 1.06 |
| Return on invested capital | 17.88% | 2.89% | 4.60% |
| Standard deviation in stock prices | — | 35.02% | 33.62% |
| Cost of capital | — | 4.40% | 6.48% |

Global automakers, 2019 LTM (the scale and margin reality of the business):

| Company | Revenues 2019 LTM ($M) | CAGR 2010-19 | Operating income ($M) | Operating margin |
|---|---|---|---|---|
| Toyota Motor | 285,284.6 | 1.83% | 24,146.2 | 8.46% |
| Volkswagen | 270,296.6 | 5.72% | 22,447.9 | 8.30% |
| Daimler | 187,796.3 | 4.54% | 5,167.4 | 2.75% |
| Ford Motor | 155,900.0 | 2.13% | 574.0 | 0.37% |
| Honda Motor | 145,690.5 | 3.24% | 6,968.2 | 4.78% |
| General Motors | 137,237.0 | 0.13% | 5,481.0 | 3.99% |
| Fiat Chrysler | 117,565.2 | 16.08% | 6,174.9 | 5.25% |
| SAIC Motor | 111,839.0 | 12.03% | 2,303.1 | 2.06% |
| BMW | 108,985.9 | 3.63% | 7,459.4 | 6.84% |
| Nissan Motor | 102,176.8 | 0.11% | 1,290.5 | 1.26% |
| Hyundai Motor | 86,053.2 | 1.03% | 2,454.5 | 2.85% |
| Peugeot | 83,946.3 | 2.24% | 6,841.1 | 8.15% |
| AUDI | 64,663.2 | 5.37% | 5,034.1 | 7.79% |
| Renault | 63,168.0 | 3.61% | 3,801.8 | 6.02% |
| Kia Motors | 46,311.2 | 6.97% | 1,502.7 | 3.24% |
| Tata Motors | 40,131.4 | 4.91% | 914.6 | 2.28% |
| Suzuki Motor | 34,206.7 | 1.03% | 2,259.3 | 6.60% |
| Mazda Motor | 32,769.8 | 1.80% | 721.2 | 2.20% |
| Subaru | 30,338.5 | 5.27% | 2,165.1 | 7.14% |
| Tesla | 24,578.0 | 81.20% | 80.0 | 0.33% |

Tesla base inputs, November 2021 ($ millions):

| Item | Trailing 12M | Last 10-K |
|---|---|---|
| Revenues | 46,848 | 31,536 |
| Operating income (EBIT) | 4,586 | 1,951 |
| Interest expense | 529 | 784 |
| Book value of equity | 28,494 | 23,679 |
| Book value of debt | 10,158 | 13,337 |
| Cash and marketable securities | 16,095 | 19,384 |
| Cross holdings / non-operating assets | 0 | 0 |
| Minority interests | 0 | 0 |
| Shares outstanding (millions) | 1,123.00 | |
| Current stock price | $1,200.00 | |
| Effective tax rate | 11.99% | |
| Marginal tax rate | 25.00% | |
| Years since last 10-K | 0.75 | |
| Capitalize R&D? | Yes | |
| Operating lease commitments? | No | |

Tesla quarterly trend check: Q3 2019 to Q3 2021 revenues rose from $6,303M to $13,757M (+118.26%), gross profit from $1,191M to $3,660M (+207.30%), operating profit from $261M to $2,055M (+687.36%).

**Worked example:** Uber, June 2014, business-model map. Drivers: anyone with a car in a covered city can apply, and approved drivers get an Uber iPhone. Customers: subscribers request rides on the app and watch the car approach. Pricing and payment: Uber sets the fare, with surge pricing at peak demand, and customers pay Uber by credit card rather than paying drivers directly. Splitting the proceeds: Uber keeps about 20% of ride receipts, already cut in some cities under pressure from Lyft and Hailo; even at a 20% cut drivers earn more than before, but stronger competition will squeeze the slice. Revenues to profits: Uber pays for R&D, technology, customer acquisition rebates, marketing and per-city staff; the low-cost model should convert a large share of revenue to profit, though regulatory and legal costs will rise. Reinvest to grow: Uber owns no cars, so reinvestment is technology plus the occasional local acquisition to enter a market. Each of those six boxes becomes a driver in [[narrative-to-value-drivers]].

**Determinism:**
- DETERMINISTIC: trailing-12-month arithmetic; the R&D and lease conversions; invested capital; sales-to-capital, ROIC and annualised growth; every industry-average lookup.
- JUDGMENT: whether to capitalise R&D and over what life; how to read the competitive map; which industry is the right comparison set; whether recent history is a guide or a break from it.

**Pitfalls:**
- Valuing off the last 10-K when three quarters have passed.
- Skipping the R&D capitalisation, which understates both EBIT and invested capital and so distorts ROIC and sales-to-capital.
- Counting employee options as ordinary shares — or ignoring them.
- Extrapolating quarterly momentum as though it were the narrative.
- Benchmarking a global company against US-only industry averages, or comparing non-dollar figures without an inflation adjustment.

**Sources:**
- valpacket1spr21 p.257-258
- valpacket1spr20 p.253-254
- valuationmotleyfool p.11, p.12, p.13, p.14
- motley-fool-tesla-xlsx: `Input sheet` (base-year block, feedback block I22-I25 with industry VLOOKUPs), `R& D converter` (research asset 5,261.4; EBIT adjustment +1,064.4), `Operating lease converter` (method, inactive for Tesla), `Trailing 12 month` helper sheet

**Related:** [[story-to-numbers-process]], [[narrative-to-value-drivers]], [[tesla-motley-fool-valuation]], [[uber-narrative-valuation]], [[life-cycle-uncertainty]]

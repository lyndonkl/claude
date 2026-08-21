# Return spreads and EVA (measuring investment quality)

**Core idea:** A firm creates value only when what it earns on its investments beats what those investments cost. Part IV of the corporate finance project turns that into two spreads: ROE minus cost of equity, and ROC minus cost of capital. EVA is the capital-scaled version of the second spread — a dollar figure rather than a percentage. The same check appears in the equity valuation project as a standalone section per company. A positive spread means the firm creates value with any reinvestment; a negative spread means growth destroys value and the firm should shrink or return cash instead.

**Formulas:**
- ROE = Net income / Book value of equity.
- After-tax ROC = EBIT × (1 − t) / (Book debt + Book equity − Cash). t = marginal tax rate. Cash is subtracted because it earns a market return and is not invested capital.
- Equity spread = ROE − Cost of equity.
- Capital spread = ROC − WACC.
- EVA = (ROC − WACC) × Capital invested (book value of capital).
- Rule: ROC > WACC ⟺ EVA > 0 ⟺ the firm creates value with any reinvestment of capital.

**Procedure:**
1. Pull EBIT, net income, book debt, book equity and cash for the most recent fiscal year.
2. Compute capital invested = book debt + book equity − cash.
3. Compute ROE and after-tax ROC.
4. Bring in the hurdle rates on the *same basis*. Compare ROE to the book/net cost of equity and ROC to the book/net WACC, not to the market-value versions. See [[cost-of-capital-buildup-deliverable]].
5. Compute both spreads and EVA in currency units.
6. Read the verdict. Large positive spreads = good projects. A spread near zero or negative = the firm is not clearing its hurdle rate.
7. Benchmark, do not just compare to zero. For a distressed firm, compare EVA to the industry-average firm EVA. A firm with a terrible ROC−WACC gap on a small capital base can still have a less negative EVA than the sector average.
8. Ask the follow-up the project requires: are future projects likely to look like past projects, and why? A persistent failure to clear the hurdle can explain a strategic move such as a large acquisition.
9. Decompose invested capital when intangibles matter. Capitalized R&D belongs in invested capital.

**Reference data:** Spring 2015 food-industry return spreads (book/net basis, tax rate 35%).

| Item | SBUX | MCD | CMG | TSN |
|---|---|---|---|---|
| EBIT ($m) | 3,081 | 7,968 | 718 | 1,430 |
| Net income ($m) | 2,068 | 4,758 | 445 | 856 |
| BV of debt ($m) | 5,479 | 14,990 | 534 | 8,178 |
| BV of equity ($m) | 5,274 | 12,853 | 2,012 | 8,904 |
| Cash ($m) | 1,708 | 2,078 | 419 | 438 |
| ROE | 39.22% | 37.02% | 22.13% | 9.61% |
| Cost of equity (book, net) | 8.89% | 9.57% | 6.46% | 9.37% |
| ROE − COE | 30.32% | 27.44% | 15.67% | 0.24% |
| After-tax ROC | 22.14% | 20.10% | 21.94% | 5.58% |
| WACC (book, net) | 6.57% | 6.18% | 6.29% | 6.35% |
| ROC − WACC | 15.58% | 13.92% | 15.64% | −0.77% |
| EVA ($m) | 1,409 | 3,587 | 333 | −128 |

EVA sections from the equity valuation project (ca. 2003), showing the same computation across very different firms:

| Firm | ROC | WACC | BV capital | EVA | Reading |
|---|---|---|---|---|---|
| Affiliated Computer Services | 11.27% | 9.37% | $2,923.88m | $55.61m | Creates value with any reinvestment |
| Biosite | 10.13% | 6.69% | 119,383 (000s) | 4,103 | Flipped from historically negative after a newly approved product doubled ROC |
| Gundle Environmental | 11.73% | 6.71% | 169,193 (000s) | $8,493 | Creates value with any reinvestment |
| Infosys | 28.12% | 13.86% | 3,383 Rs crore | 482 Rs crore | Strongly positive |
| Apple | — | — | BV equity ≈ 2/3 of invested capital; capitalized research asset > $1.1bn is the other third | 58.12 | Creates value by reinvesting |
| Nextel Partners | −19.71% | 18.57% | $1,632m | −$625m | Deeply negative, but less negative than the wireless industry average firm EVA of −5,742 |

Published data sets for this part: ROE and equity EVA by sector; ROC and EVA by sector.

**Worked example:** Tyson Foods, 2015. Capital invested = 8,178 + 8,904 − 438 = $16,644m. After-tax ROC = 1,430 × 0.65 / 16,644 = 5.58%. Book/net WACC = 6.35%. Capital spread = 5.58% − 6.35% = −0.77%. EVA = −0.0077 × 16,644 ≈ −$128m. Tyson is the one firm in the set that fails to clear its cost of capital, and its ROE spread of +0.24% is effectively break-even too. The team read the shortfall as a plausible driver of the Hillshire Brands acquisition — a mature firm buying its way back onto a growth trajectory because its own projects do not clear the bar.

**Determinism:** DETERMINISTIC — EBIT, net income, tax rate, book debt, book equity, cash and the two hurdle rates produce ROE, ROC, both spreads and EVA exactly. The industry-average EVA comparison is a lookup. JUDGMENT — whether future projects will resemble past ones, what a near-zero spread means strategically, whether the accounting book capital fairly represents invested capital (leases, capitalized R&D, recent write-offs), and whether a one-year figure is representative.

**Pitfalls:**
- Comparing accounting returns to market-value hurdle rates. The mismatch can flip the sign of a spread.
- Forgetting to net cash out of invested capital. Cash inflates the denominator and depresses ROC.
- Judging a single year. Biosite's EVA flipped from negative to strongly positive in one year on a single new product approval — a good year is not a good business.
- Comparing a distressed firm's EVA only to zero. Compare to the industry average.
- Ignoring intangible capital. Apple's capitalized research asset is a third of its invested capital; leaving it out overstates ROC.

**Sources:**
- corporate_finance--project--cfproj p.7
- corporate_finance--project--food2015 p.9, p.2
- valuations--projects--valproject2 p.3, p.6, p.10, p.12, p.17, p.20

**Related:** [[cost-of-capital-buildup-deliverable]], [[two-stage-fcff-company-valuation]], [[qualitative-debt-tradeoff]], [[valuation-triangulation-and-recommendation]], [[project-executive-summary-scorecard]]

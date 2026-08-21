# Accounting returns: ROC, ROIC, ROE and EVA

**Core idea:** The accounting view of return divides an income number by a book capital number. For the whole firm or a project financed by all claimholders, that is return on capital (ROC, or ROIC when computed on invested capital). For equity investors it is return on equity (ROE). The measure earns its keep as a quick quality test of *existing* investments: a firm creating value earns ROC above its cost of capital. Economic Value Added converts the percentage spread into dollars. The measure is easy to compute and easy to distort. Every input — the earnings numerator, the book capital denominator, the averaging window — can be bent by accounting choices, write-offs, life-cycle position, and inflation. Roughly half the world's non-financial firms earn less than their cost of capital.

**Formulas:** Symbols: `EBIT` = operating income; `t` = tax rate; `BV` = book value.
- `Return on capital = EBIT(1 − t) / BV of capital`, where `BV of capital = BV of debt + BV of equity − cash`. Denominator conventionally measured at the *start* of the period (previous year's balance sheet).
- Project ROC, average-capital basis: `ROC(a)_t = After-tax operating income_t / [(BV capital at start of t + BV capital at end of t) / 2]`
- Project ROC, start-of-year basis: `ROC(b)_t = After-tax operating income_t / BV capital at start of t`
- `Return on Invested Capital = After-tax operating income / capital invested in existing assets`, where `invested capital = BV of equity + BV of debt − cash and cross holdings`
- `Return spread = ROC − cost of capital`
- `EVA = Return spread × (BV of debt + BV of equity − cash)`, denominator from the previous year
- `ROE = Net income / BV of equity`; `Equity return spread = ROE − cost of equity`

**Procedure:**
1. Pick the perspective. Returns to all capital → ROC vs cost of capital. Returns to equity → ROE vs cost of equity. See [[project-hurdle-rate-selection]].
2. Build the numerator. Use operating income for the most recent 12 months, taxed at the marginal rate for a project, or the effective rate when measuring what a firm actually earned. Add back one-time and non-recurring items. Capitalize operating leases and (optionally) R&D, restating operating income upward by (current expense − amortization on the created asset).
3. Build the denominator from the *previous* year's balance sheet: short-term debt + long-term debt + shareholder equity + minority interest, minus goodwill, minus cash. Add the debt value of capitalized leases and the R&D research asset if you capitalized them.
4. For a project, track the book capital roll-forward year by year: pre-project book value + book value of new fixed assets + book value of working capital.
5. Compute annual ROC and the simple average across the project life. Report both the average-capital and start-of-year variants; they normally differ by only a few basis points.
6. Compare to the risk-matched cost of capital. `ROC > cost of capital` → value creating. `ROC < cost of capital` → value destroying.
7. Convert to dollars: `EVA = spread × invested capital`.
8. Sanity-check against the distortions listed under Pitfalls before acting on the number.

**Reference data:**

Firm-level ROC and spreads (2020 packet; currency in millions, ¥ for Baidu, ₹ for Tata Motors):

| Company | EBIT(1−t) | BV debt | BV equity | Cash | BV capital | ROC | Cost of capital | Spread |
|---|---|---|---|---|---|---|---|---|
| Disney | $6,920 | $16,328 | $41,958 | $3,387 | $54,899 | 12.61% | 7.81% | +4.80% |
| Vale | $12,432 | $49,246 | $75,974 | $5,818 | $119,402 | 10.41% | 8.20% | +2.22% |
| Baidu | ¥9,111 | ¥13,561 | ¥27,215 | ¥10,456 | ¥30,320 | 30.05% | 12.42% | +17.63% |
| Tata Motors | ₹120,905 | ₹471,489 | ₹330,056 | ₹225,562 | ₹575,983 | 20.99% | 11.44% | +9.55% |
| Bookscape (total-beta cost of capital) | $1,775 | $12,136 | $8,250 | $1,250 | $19,136 | 9.28% | 10.30% | −1.02% |

Share of non-financial-service firms by ROIC-vs-WACC bucket, January 2020:

| Region | ROIC < WACC | ROIC ≈ WACC | ROIC > WACC |
|---|---|---|---|
| Africa and Middle East | 51.68% | 17.83% | 30.49% |
| Australia & NZ | 67.22% | 8.06% | 24.72% |
| Canada | 80.31% | 6.17% | 13.52% |
| China | 49.18% | 16.54% | 34.28% |
| EU & Environs | 47.38% | 16.21% | 36.41% |
| Eastern Europe & Russia | 50.96% | 18.73% | 30.30% |
| India | 47.66% | 14.85% | 37.49% |
| Japan | 34.24% | 23.11% | 42.65% |
| Latin America & Caribbean | 43.90% | 20.34% | 35.76% |
| Small Asia | 59.08% | 15.12% | 25.80% |
| UK | 46.54% | 13.46% | 40.00% |
| United States | 50.00% | 11.73% | 38.27% |
| **Global** | **52.05%** | **15.32%** | **32.63%** |

Standard adjustment machinery (Damodaran `returncalculator.xls`), in three steps:

1. Capitalize operating leases. Discount the commitments at the pre-tax cost of debt. Depreciation on the leased asset = lease debt / (5 + n6), where n6 = round(year-6+ lump / average of years 1–5).
2. Optionally capitalize R&D over an industry amortization period. Rule of thumb: 2 years for non-technological service and retail, 3 for tech service, 5 for light manufacturing, 10 for heavy manufacturing, patenting research, and long-gestation businesses.
3. Strip goodwill and cash from invested capital, with user-controlled partial add-backs.

Two documented quirks in that sheet. The unadjusted ROIC uses *stated* EBIT(1−t) over *unadjusted* capital. The partial-cash setting subtracts (1 − pct kept) × cash but then adds back pct × cash, leaving twice the intended cash share in capital.

**Worked example:** Rio Disney project ROC ($ millions).

| Year | After-tax operating income | BV of capital (start) | Average BV of capital | ROC(a) | ROC(b) |
|---|---|---|---|---|---|
| 1 | −$32 | $2,500 | $2,975 | −1.07% | −1.28% |
| 2 | −$96 | $3,450 | $3,863 | −2.48% | −2.78% |
| 3 | −$54 | $4,275 | $4,429 | −1.22% | −1.26% |
| 4 | $68 | $4,582 | $4,517 | 1.50% | 1.48% |
| 5 | $202 | $4,452 | $4,410 | 4.57% | 4.53% |
| 6 | $249 | $4,368 | $4,335 | 5.74% | 5.69% |
| 7 | $299 | $4,302 | $4,286 | 6.97% | 6.94% |
| 8 | $352 | $4,270 | $4,262 | 8.26% | 8.24% |
| 9 | $410 | $4,254 | $4,255 | 9.62% | 9.63% |
| 10 | $421 | $4,257 | $4,250 | 9.90% | 9.89% |
| **Average** | | | | **4.18%** | **4.11%** |

Average ROC of 4.18% is below the 8.46% Brazil-adjusted theme-park cost of capital, so the naive accounting verdict is reject. That verdict is unsafe: the parks last far longer than ten years, and the truncated window loads all the early-year losses into the average while excluding the mature high-return years. The DCF analysis, run over a perpetual life, gives NPV = +$3,296 million.

**Determinism:** DETERMINISTIC — given EBIT, tax rate, prior-year book debt/equity/cash, and the cost of capital, a script computes ROC, ROE, the spread, and EVA. The full project ROC series follows from the income and book-capital tables. The lease and R&D capitalization adjustments are deterministic once the amortization period and cost of debt are set. JUDGMENT — normalizing the numerator, which means deciding which charges are non-recurring and whether to capitalize R&D. Also judgment: correcting the denominator for write-offs, inflation-stale book values, and life-cycle position. Also: choosing the averaging window, and deciding whether the resulting number is informative at all.

**Pitfalls:**
- **Numerator distortions:** abnormally good or bad trailing-12-month earnings, misclassified leases and R&D, unusual income or expenses.
- **Life-cycle bias:** current earnings understate long-term potential for young firms and infrastructure firms.
- **Denominator distortions:** write-offs shrink invested capital and mechanically flatter ROIC; treating capital expenses (R&D) or financial expenses (leases) as operating expenses understates invested capital; inflation leaves older assets carried at stale book values.
- **Depreciation choice:** more accelerated depreciation shrinks book capital and raises ROC substantially. Two analysts with identical cash flows can report very different ROCs.
- **Allocation choice:** the overhead allocation mechanism changes operating income and therefore ROC. The Netflix Fit case shows student groups clustering at both <5% and >20% for the same project.
- **Mechanical rise over time:** book-based returns climb as assets depreciate, even with flat cash flows. Netflix Fit's ROIC runs from −2.91% in year 1 to 44.06% in year 10 on an unchanging asset.
- **Horizon truncation:** averaging over an arbitrary window on a long-lived project (Rio Disney).
- Comparing ROC to a cost of *equity*, or ROE to a cost of *capital*.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.220-221
- corporate_finance--lecture_slides--cfpacket1spr20 p.225-229
- corporate_finance--lecture_slides--cfpacket1spr20 p.261
- corporate_finance--lecture_slides--cfpacket1spr20 p.266-267
- corporate_finance--lecture_slides--cfpacket1spr20 p.284-285
- corporate_finance--case--netflixfit p.7
- corporate_finance--case--netflixfitpresentation p.7-9
- corpfin-ratings-risk (returncalculator.xls: ROIC/ROE adjustment engine, lease and R&D converters, industry amortization table)

**Related:** [[earnings-vs-cash-flows]], [[equity-side-project-analysis]], [[project-hurdle-rate-selection]], [[assessing-existing-investments]], [[npv-and-irr-mechanics]], [[netflix-fit-case]], [[cost-of-capital]], [[operating-lease-capitalization]], [[rnd-capitalization]]

# Implied equity risk premium

**Core idea:** If you know the price you paid for an asset and you can forecast its cash flows, the internal rate of return on those cash flows is your expected return. Apply that to an entire equity index. Assume stocks are correctly priced in aggregate, forecast the cash the index will return to investors, and solve for the discount rate that sets the present value equal to today's index level. That rate is the expected return on stocks; subtract the riskfree rate and you have the implied equity risk premium. It is forward-looking, it can be re-estimated as often as you like (daily, even minute by minute), and empirically it predicts future returns far better than the historical premium does.

**Formulas:**

The standard five-year-plus-terminal-value form:

Index level = CF₁/(1+r) + CF₂/(1+r)² + CF₃/(1+r)³ + CF₄/(1+r)⁴ + CF₅/(1+r)⁵ + CF₅×(1+g)/((r − g)×(1+r)⁵)

- Index level = the current level of the index (e.g. S&P 500).
- CF_t = expected cash returned to investors in year t = dividends + buybacks (the "cash yield" measure), grown from the base year.
- CF₀ (base year) = trailing 12-month dividends + trailing 12-month buybacks on the index.
- CF_t = CF₀ × (1 + g_high)^t for t = 1..5, where g_high = expected earnings growth for the next 5 years (top-down analyst consensus for the index). More refined versions grow *earnings* at g_high and apply a rising payout ratio to get cash flows.
- g = perpetual growth rate after year 5, **set equal to the riskfree rate** in that currency.
- r = the implied expected return on stocks; solve for it numerically.
- **Implied ERP = r − Riskfree rate.**

Dividend-only variant (Damodaran's `implprem.xls`): base dividends D₀ = Index level × Dividend yield; D_t = D₀(1+g_high)^t for t = 1..5; terminal value at year 5 = D₅(1+g)/(r − g); solve for r such that the sum of present values equals the index level. Implied premium = r − bond rate. Requires r > g, i.e. premium > g − riskfree rate, or the terminal value is undefined.

**Procedure:**
1. **Base cash flow.** Take trailing-12-month dividends plus buybacks on the index. Buybacks matter — they were 68.89 of the S&P 500's 127.78 total in 2020, and ignoring them roughly halves the premium.
2. **Normalize the base if it is distorted.** In crisis years the trailing figure is not a sustainable base. Damodaran normalized 2008 buybacks downward (from 40.25 to 24.11, giving 52.58 instead of 68.72 total) because Q4 2008 buybacks had dropped 41%.
3. **Growth for years 1-5.** Use the top-down consensus analyst estimate of index earnings growth. Either grow cash flows at that rate directly, or grow earnings and apply an explicit payout-ratio path.
4. **Terminal growth.** Set it equal to the current riskfree rate in the index's currency. This is the internal-consistency rule: a perpetual growth rate cannot exceed the riskfree rate.
5. **Solve for r.** The equation is a polynomial in r; use Goal Seek, Solver, or a root finder (Brent/bisection) bracketing r in (g + ε, 0.20].
6. **Subtract the riskfree rate** to get the implied ERP.
7. **Update it.** Re-run whenever the index moves materially. The premium is a live number, not an annual one.
8. To get an implied premium for a **non-US index**, run the identical procedure with that index's level, cash yield, growth, and local riskfree rate as the terminal growth rate.

**Reference data:**

S&P 500 implied ERP computations across editions:

| Date | Index level | Base cash flow (div + buyback) | 5-yr growth | Terminal growth (= Rf) | Solved r | Implied ERP |
|---|---|---|---|---|---|---|
| 1/1/2008 | 1468.36 | 59.03 (4.02% of index) | 5.00% | 4.02% | 8.39% | **4.37%** |
| 1/1/2009 | 903.25 | 52.58 (normalized) | 4.00% | 2.21% | 8.64% | **6.43%** |
| 11/1/2013 | 1756.54 | 82.35 (33.22 + 49.02) | 5.59% | 2.55% | 8.04% | **5.49%** |
| 1/1/2020 | 3230.78 | 150.50 (57.71 + 92.80) | 3.96% | 1.92% | 7.12% | **5.20%** |
| 1/1/2021 | 3756.07 | 127.78 (58.89 + 68.89) | 10.15% | 0.93% | 5.65% | **4.72%** |

January 1, 2021 cash-flow path (the current edition's mature-market premium of 4.72%):
- Expected earnings: 2019 actual 163.00; trailing 12 months 123.35; 2021 138.55; 2022 152.62; 2023 168.11; 2024 185.18; 2025 203.98; terminal year 205.88.
- Cash payout ratio: 89.76% (2019), 103.59% (TTM), then 89.09%, 90.21%, 91.33%, 92.46%, 93.58%, 93.58% (terminal).
- Expected dividends + buybacks: 123.43, 137.67, 153.54, 171.21, 190.88; terminal 192.66.
- Equation: 3756.07 = 123.43/(1+r) + 137.67/(1+r)² + 153.54/(1+r)³ + 171.21/(1+r)⁴ + 190.88/(1+r)⁵ + 190.88(1.0093)/((r − 0.0093)(1+r)⁵) → r = 5.65%, ERP = 4.72%.

S&P 500 dividends and buybacks history (used to build base cash flows):

| Year | Index | Dividends | Buybacks | Cash to equity | Total yield |
|---|---|---|---|---|---|
| 2001 | 1148.09 | 15.74 | 14.34 | 30.08 | 2.62% |
| 2002 | 879.82 | 15.96 | 13.87 | 29.83 | 3.39% |
| 2003 | 1111.91 | 17.88 | 13.70 | 31.58 | 2.84% |
| 2004 | 1211.92 | 19.01 | 21.59 | 40.60 | 3.35% |
| 2005 | 1248.29 | 22.34 | 38.82 | 61.17 | 4.90% |
| 2006 | 1418.30 | 25.04 | 48.12 | 73.16 | 5.16% |
| 2007 | 1468.36 | 28.14 | 67.22 | 95.36 | 6.49% |
| 2008 | 903.25 | 28.47 | 40.25 | 68.72 | 7.77% |
| 2008 normalized | 903.25 | 28.47 | 24.11 | 52.58 | 5.82% |

US implied ERP averages: 1960-2020 = 4.21%; 2001-2020 = 4.95%; 2011-2020 = 5.53%; end of 2020 = 4.72%. The series has ranged from about 2% (1999 dot-com peak) to about 6.5% (late 1970s and 2008).

Expected return on stocks = T.Bond rate + implied ERP: 1960-2020 average 10.06%; 2001-2020 8.01%; 2011-2020 7.68%; end of 2020 **5.65%** — the lowest in 60 years.

Crisis dynamics: 9/12/2008 implied ERP ~4.3% → peak near 8% in late November 2008 → 6.43% at year end. In 2020: 4.83% on 2/14, 7.75% at the 3/23 market bottom (6.87% on a COVID-adjusted earnings path), 5.35% by 11/1 (5.02% COVID-adjusted).

**Worked example (India's Sensex, 9/5/2007):** Index 15446; dividend yield 3.05%, so base cash flow ≈ 471; expected growth 14% per year for 5 years; terminal growth 6.76% (the Indian riskfree rate). Cash flows: 537.06, 612.25, 697.86, 795.67, 907.07. Equation: 15446 = 537.06/(1+r) + 612.25/(1+r)² + 697.86/(1+r)³ + 795.67/(1+r)⁴ + 907.07/(1+r)⁵ + 907.07(1.0676)/((r − 0.0676)(1+r)⁵). Solving gives r = 11.18%, so the implied ERP for India = 11.18% − 6.76% = **4.42%**.

**Worked example (dividend-only calculator, `implprem.xls`):** Index 1418.3, dividend yield 3.75% → D₀ = 53.186. Growth 6% for 5 years → D₅ = 71.175. Bond rate 4.7%, long-term growth 4.7%. At a trial premium of 4.91% (r = 9.61%) the model values the index at 1200.06, below the actual 1418.3, so the trial premium is too high. Solving for the premium that reproduces 1418.3 gives **4.158%**: terminal value = 71.175 × 1.047 / (0.04158) = 1792.42, and the present values sum to 1418.30.

**Determinism:**
- DETERMINISTIC: given (index level, base cash flow, 5-year growth rate, payout path, terminal growth = riskfree rate) → solve for r → implied ERP. A script can do this with a one-dimensional root find. Also deterministic: computing the base cash flow from reported dividends and buybacks, and averaging the annual series.
- JUDGMENT: the 5-year growth forecast; whether and how to normalize the base cash flow (the 2008 buyback haircut, the COVID earnings-recovery path); the payout-ratio trajectory; whether to use cash yield or dividends only; whether the "market is correctly priced in aggregate" assumption is acceptable for your purpose.

**Pitfalls:**
- Using dividends only in a market where buybacks dominate. The 2020 S&P 500 returned 68.89 in buybacks against 58.89 in dividends.
- Setting terminal growth above the riskfree rate. This inflates the terminal value and mechanically depresses the solved r.
- Using an unnormalized crisis-year base cash flow, which produces a wildly overstated premium.
- Forgetting that the solution requires r > g. If your bracket includes r ≤ g, the terminal value is negative or undefined.
- Treating the number as stable. It moved from 4.83% to 7.75% and back to 5.35% within 2020.
- Confusing the implied ERP (r − Rf) with the implied expected return on stocks (r).

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.65-73, p.78-79
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.65-71, p.76-77
- corporate_finance--lecture_slides--cfpacket1spr20 p.116-117, p.126-128
- spreadsheet `implprem.xls` (Valuation Inputs collection): dividend-discount implied-premium solver

**Related:** [[equity-risk-premium-basics]], [[historical-equity-risk-premium]], [[choosing-an-equity-risk-premium]], [[country-risk-premium]], [[riskfree-rate-normalization]], [[terminal-value]]

# Capitalizing R&D and other intangible investments

**Core idea:** By accounting first principles, spending that creates benefits over many periods is a capital expenditure. It should sit on the balance sheet and be depreciated over its life, not charged against this year's operating income. Accounting follows that principle for manufacturing firms and abandons it everywhere else. For pharmaceutical and technology companies, R&D is the ultimate capital expenditure and it is expensed. For consulting and other human-capital firms, recruiting and training are the long-term investments and they are expensed. For brand-name consumer companies, the brand-building portion of advertising is the real capital expenditure and it too is expensed. The consequence is that operating income, invested capital, the reinvestment rate and the return on capital are all wrong at exactly the firms where growth matters most. Fixing the inconsistency changes both your picture of the company and its value.

**Formulas:** With a straight-line amortizable life of `N` years and `R&D_{−k}` the R&D expense `k` years ago (`k = 0` is the current year):
- Unamortized fraction of year `−k`'s spending: `(N − k)/N`.
- Research asset (capital invested in R&D): `Research asset = Σ_{k=0..N} R&D_{−k} × (N − k)/N`.
- This year's amortization: `Amortization = Σ_{k=1..N} R&D_{−k} / N`.
- Adjustment to operating income: `ΔEBIT = Current-year R&D − Amortization` (positive means add to reported EBIT; it can be **negative** when R&D spending is shrinking).
- `Adjusted operating income = Reported EBIT + Current R&D − Amortization`.
- `Adjusted net income = Reported net income + Current R&D − Amortization`.
- `Adjusted book equity = Book equity + Research asset`; `Adjusted invested capital = Invested capital + Research asset`.
- `Adjusted ROE = Adjusted net income / Adjusted book equity`; `Adjusted pre-tax ROC = Adjusted operating income / Adjusted invested capital`.
- Tax effect of the adjustment (informational): `Tax effect = Tax rate × ΔEBIT`.
- Capital expenditure in the DCF becomes: `Cap ex = Accounting net cap ex + Acquisitions + Current-year R&D`.

**Procedure:**
1. Choose the amortizable life. It should match how long the investment takes to produce revenue. For Amgen the FDA approval process justified **10 years**. Use the lookup table below when in doubt.
2. Collect R&D expense for the current year and each of the prior `N` years. Missing years are treated as zero.
3. Compute the research asset and the current year's amortization from the two sums above.
4. Restate: add current R&D back to operating income and net income, subtract the amortization; add the research asset to book equity and to invested capital.
5. Recompute returns. Expect ROE and ROC to **fall**, not rise — capital usually goes up proportionally more than income.
6. Recompute the reinvestment rate with R&D now inside capital expenditure.
7. Run the DCF on the restated numbers. Keep the treatment consistent: if R&D is capitalized, it must be in cap ex, in invested capital, and in the ROC used to set growth.
8. Apply the same logic to recruiting and training at human-capital firms, and to the brand-building share of advertising at consumer-products firms.

**Reference data (1):** Amgen R&D capitalization, 10-year amortizable life, $ millions.

| Year | R&D expense | Unamortized fraction | Unamortized portion | Amortization this year |
|---|---|---|---|---|
| Current | 3,030.00 | 1.00 | 3,030.00 | — |
| −1 | 3,266.00 | 0.90 | 2,939.40 | 326.60 |
| −2 | 3,366.00 | 0.80 | 2,692.80 | 336.60 |
| −3 | 2,314.00 | 0.70 | 1,619.80 | 231.40 |
| −4 | 2,028.00 | 0.60 | 1,216.80 | 202.80 |
| −5 | 1,655.00 | 0.50 | 827.50 | 165.50 |
| −6 | 1,117.00 | 0.40 | 446.80 | 111.70 |
| −7 | 864.00 | 0.30 | 259.20 | 86.40 |
| −8 | 845.00 | 0.20 | 169.00 | 84.50 |
| −9 | 823.00 | 0.10 | 82.30 | 82.30 |
| −10 | 663.00 | 0.00 | 0.00 | 66.30 |
| **Total** | | | **13,283.60** | **1,694.10** |

**Reference data (2):** R&D amortizable-life rules of thumb. Non-technological service 2 years; retail and tech service 3 years; light manufacturing 5 years; heavy manufacturing 10 years; research with patenting 10 years; long gestation period 10 years.

Selected industry lives from the lookup table: Advertising 2; Aerospace/Defense 10; Air Transport 10; Apparel 3; Auto & Truck 10; Auto Parts 5; Bank 2; Beverage 3; Building Materials 5; Cable TV 10; Chemical (Basic/Diversified/Specialty) 10; Computer & Peripherals 5; Computer Software & Services 3; Drug 10; Electric Utility 10; Electrical Equipment 10; Electronics 5; Entertainment 3; Financial Services 2; Food Processing 3; Grocery 2; Healthcare Info Systems 3; Homebuilding 5; Hotel/Gaming 3; Insurance 3; Internet 3; Machinery 10; Maritime 10; Medical Services 3; Medical Supplies 5; Metal Fabricating 10; Natural Gas 10; Newspaper 3; Paper & Forest Products 10; Petroleum 5; Precision Instrument 5; Publishing 3; Railroad 5; Restaurant 2; Retail (all) 2; Securities Brokerage 2; Semiconductor 5; Shoe 3; Steel 5; Telecom Equipment 10; Telecom Services 5; Textile 5; Thrift 2; Tobacco 5; Toiletries/Cosmetics 3; Trucking 5; Water Utility 10.

**Reference data (3):** What the fix does to Amgen (May 2007).

| Metric | No R&D adjustment | With R&D adjustment |
|---|---|---|
| EBIT | $5,071m | $7,336m |
| Invested capital | $25,277m | $33,173m |
| ROIC | 14.58% | 18.26% |
| Reinvestment rate | 115.68% | 106.98% |
| Value of firm | $58,617m | $95,497m |
| Value of equity | $50,346m | $87,226m |
| **Value per share** | **$42.73** | **$74.33** |

**Worked example:** Amgen, restated. Current-year R&D of $3,030m is the capital expenditure; amortization of $1,694m is the depreciation; the unamortized $13,284m is the capital invested.
- Net income: `4,196 + 3,030 − 1,694 = $5,532m`. Book equity: `17,869 + 13,284 = $31,153m`. ROE falls from `4,196/17,869 = 23.48%` to `5,532/31,153 = 17.75%`.
- Pre-tax operating income: `5,594 + 3,030 − 1,694 = $6,930m`. Invested capital: `21,985 + 13,284 = $35,269m`. Pre-tax ROC falls from `5,594/21,985 = 25.44%` to `6,930/35,269 = 19.65%`.
- In the DCF, cap ex becomes accounting net cap ex $255m + acquisitions $3,975m + R&D $2,216m. EBIT(1−t) = 7,336 × (1 − 0.28) = $6,058m; reinvestment rate 60% at a 16% ROC gives 9.6% growth for five years, fading to 4%. Cost of equity = 4.78% + 1.73 × 4% = 11.70%; after-tax cost of debt = (4.78% + 0.85%) × (1 − 0.35) = 3.66%; WACC = 11.7% × 0.90 + 3.66% × 0.10 = 10.90%. Terminal value (year 10) = 7,300/(0.0808 − 0.04) = $179,099m. Operating assets $94,214m + cash $1,283m − debt $8,272m = equity $87,226m; − options $479m → **$74.33 per share** versus a 1 May 2007 price of $55.

A counter-example on sign: Boeing in March 2020 had current-year R&D of $3,219m and prior years of $3,269m, $3,179m, $4,626m, $3,331m, $3,047m over a 5-year life. The research asset is $10,258.2m, but amortization of $3,490.4m **exceeds** current R&D, so the adjustment to operating income is `3,219 − 3,490.4 = −$271.4m`. Capitalizing R&D lowered Boeing's reported EBIT.

**Determinism:** DETERMINISTIC — (R&D history, amortizable life) → research asset, current amortization, EBIT adjustment, tax effect, restated income, book equity, invested capital, ROE, ROC. The Amgen and Boeing numbers reproduce exactly. JUDGMENT: the amortizable life (needs the industry's development-to-revenue lag; use the lookup table), which advertising or training spend is genuinely capital rather than maintenance, and how many prior years of data are available.

**Pitfalls:**
- Expecting the fix to improve returns. Both ROE and ROC usually **fall**, because capital rises proportionally more than income.
- Adding the research asset to invested capital but forgetting to add R&D to capital expenditure. That understates reinvestment and manufactures free growth.
- Assuming the adjustment to operating income is always positive. When R&D spending is falling, amortization exceeds current spending and EBIT goes down.
- Using a single amortizable life across a diversified company. The life should track the business.
- Applying the restated ROC to set growth while leaving the reinvestment rate on the old basis. The two must move together.
- Treating the whole advertising budget as capital. Only the brand-building portion is.
- Forgetting that the same restatement changes the interest coverage ratio, and so the synthetic rating and the cost of debt.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.347-351
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.338-342
- spreadsheet model doc: special-troubled.md — normearn.xls, R&D converter sheet and the amortization-period lookup table
- spreadsheet model doc: ginzu-fcff-corona.md — R& D converter sheet

**Related:** [[normalized-earnings]], [[sales-to-capital-reinvestment]], [[difficult-company-taxonomy]], [[synthetic-rating]], [[operating-lease-capitalization]], [[return-on-invested-capital]], [[fcff-valuation]]

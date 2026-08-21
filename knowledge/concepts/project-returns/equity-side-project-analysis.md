# Equity-side project analysis

**Core idea:** The whole investment analysis can be run from the equity investors' viewpoint instead of the firm's. Everything shifts one layer down the capital structure. The accounting return becomes return on equity, net income over book equity, tested against the cost of equity. The cash flow becomes cash flow to equity, which is cash flow after interest and principal payments, discounted at the cost of equity. The two routes — firm and equity — answer the same question and normally agree. The firm route is cleaner when the financing mix is stable, because debt effects live entirely in the discount rate. The equity route is natural when the project carries its own dedicated financing with a known amortization schedule, and it is the standard route for financial service firms, where capital and cost of capital are hard to pin down.

**Formulas:** Symbols: `NI` = net income; `D&A` = depreciation and amortization; `BV` = book value.
- `ROE_t = Net income_t / Average BV of equity_t`, where `Average BV of equity_t = (BV equity_{t−1} + BV equity_t)/2` and `BV equity = BV assets + BV working capital − debt outstanding`
- `Equity return spread = ROE − cost of equity`
- `Cash flow to equity_t = NI_t + D&A_t − CapEx_t − ΔWorking capital_t − Principal repayments_t + Salvage value (final year)`
- `Equity NPV = Σ_t Cash flow to equity_t / (1 + cost of equity)^t`
- Amortizing loan: `Payment = Loan × r / (1 − 1/(1+r)^n)`; `Interest_t = Beginning debt_t × r`; `Principal repaid_t = Payment − Interest_t`

**Procedure:**
1. Confirm the perspective. Equity analysis requires a defined financing plan for the project — how much is borrowed, at what rate, on what repayment schedule.
2. Build the loan amortization schedule: beginning debt, interest expense, principal repaid, ending debt, year by year.
3. Build the income statement down to *net* income. Deduct interest expense (unlike the firm-side analysis, where interest never appears in the cash flows).
4. Tax at the marginal rate. Losses generate tax benefits at the same rate.
5. Roll forward the book value of equity: beginning assets − depreciation + capex, plus working capital, minus debt outstanding.
6. Compute annual and average ROE. Compare to the cost of equity for that business, in that currency.
7. Convert net income to cash flow to equity. Add back depreciation. Subtract capex, counting only the *equity* share of the initial investment, since the borrowed portion is not an equity outflow. Subtract working capital changes and principal repayments. Add salvage in the final year.
8. Discount at the cost of equity matched to the business, currency, and risk. Accept if equity NPV > 0 or equity IRR > cost of equity.
9. Cross-check the ROE verdict and the NPV verdict. Divergence signals a book-value distortion.

**Reference data:** Vale iron ore mine case inputs (2020 packet), the running equity-analysis example:

| Assumption | Value |
|---|---|
| Initial investment | $1,250M for 8M tons capacity |
| Depreciation | Double declining balance over 10 yrs to $250M salvage |
| Production | 4M tons yr 1, 6M yr 2, 8M yrs 3–10 |
| Iron ore price | $100/ton now, growing at 2% inflation |
| Variable cost | $45/ton, growing at 2% |
| Fixed cost | $125M in yr 1, growing at 2% |
| Working capital | 20% of revenues, invested at start of each year, fully salvaged at yr 10 |
| Tax rate | 34% |
| Exchange rate | C$1 = US$1 parity, assumed to persist |
| Debt | $500M term loan, 4.05% (A− rating), 10-yr equal installments of $61.80M |
| Hurdle rate | US$ cost of equity for Vale's **iron ore** business = 11.13% |

Vale business-level rates (US$ and Brazilian reais):

| Business | Cost of equity | After-tax cost of debt | Debt ratio | Cost of capital (US$) | Cost of capital ($R) |
|---|---|---|---|---|---|
| Metals & Mining | 11.35% | 2.67% | 35.48% | 8.27% | 15.70% |
| Iron Ore | 11.13% | 2.67% | 35.48% | 8.13% | 15.55% |
| Fertilizers | 12.70% | 2.67% | 35.48% | 9.14% | 16.63% |
| Logistics | 10.29% | 2.67% | 35.48% | 7.59% | 14.97% |
| Vale Operations | 11.23% | 2.67% | 35.48% | 8.20% | 15.62% |

Loan amortization schedule ($ millions, $500M at 4.05%, 10 years):

| Year | Beginning debt | Interest | Principal repaid | Total payment | Ending debt |
|---|---|---|---|---|---|
| 1 | $500.00 | $20.25 | $41.55 | $61.80 | $458.45 |
| 2 | $458.45 | $18.57 | $43.23 | $61.80 | $415.22 |
| 3 | $415.22 | $16.82 | $44.98 | $61.80 | $370.24 |
| 4 | $370.24 | $14.99 | $46.80 | $61.80 | $323.43 |
| 5 | $323.43 | $13.10 | $48.70 | $61.80 | $274.73 |
| 6 | $274.73 | $11.13 | $50.67 | $61.80 | $224.06 |
| 7 | $224.06 | $9.07 | $52.72 | $61.80 | $171.34 |
| 8 | $171.34 | $6.94 | $54.86 | $61.80 | $116.48 |
| 9 | $116.48 | $4.72 | $57.08 | $61.80 | $59.39 |
| 10 | $59.39 | $2.41 | $59.39 | $61.80 | $0.00 |

**Worked example:** Vale Labrador mine, full equity analysis ($ millions).

Net income and book equity:

| Item | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Revenues | $408.00 | $624.24 | $848.97 | $865.95 | $883.26 | $900.93 | $918.95 | $937.33 | $956.07 | $975.20 |
| − Variable costs | $180.00 | $275.40 | $374.54 | $382.03 | $389.68 | $397.47 | $405.42 | $413.53 | $421.80 | $430.23 |
| − Fixed costs | $125.00 | $127.50 | $130.05 | $132.65 | $135.30 | $138.01 | $140.77 | $143.59 | $146.46 | $149.39 |
| − Depreciation (DDB) | $200.00 | $160.00 | $128.00 | $102.40 | $81.92 | $65.54 | $65.54 | $65.54 | $65.54 | $65.54 |
| EBIT | −$97.00 | $61.34 | $216.37 | $248.86 | $276.37 | $299.91 | $307.22 | $314.68 | $322.28 | $330.04 |
| − Interest | $20.25 | $18.57 | $16.82 | $14.99 | $13.10 | $11.13 | $9.07 | $6.94 | $4.72 | $2.41 |
| − Taxes @34% | −$39.87 | $14.54 | $67.85 | $79.51 | $89.51 | $98.19 | $101.37 | $104.63 | $107.97 | $111.40 |
| **Net income** | **−$77.39** | **$28.23** | **$131.71** | **$154.35** | **$173.76** | **$190.60** | **$196.78** | **$203.11** | **$209.59** | **$216.24** |
| End BV of equity | $716.40 | $644.57 | $564.95 | $512.82 | $483.13 | $471.87 | $462.74 | $455.81 | $451.18 | $250.00 |
| **ROE** | **−10.00%** | **4.15%** | **21.78%** | **28.64%** | **34.89%** | **39.92%** | **42.11%** | **44.22%** | **46.22%** | **61.68%** |

Average ROE over ten years = **31.36%** versus an 11.13% cost of equity → passes the accounting-equity test.

Cash flow to equity and equity NPV:

| Item | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Net income | | ($77.39) | $28.23 | $131.71 | $154.35 | $173.76 | $190.60 | $196.78 | $203.11 | $209.59 | $216.24 |
| + D&A | | $200.00 | $160.00 | $128.00 | $102.40 | $81.92 | $65.54 | $65.54 | $65.54 | $65.54 | $65.54 |
| − Capital expenditures | $750.00 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| − Change in working capital | $81.60 | $43.25 | $44.95 | $3.40 | $3.46 | $3.53 | $3.60 | $3.68 | $3.75 | $3.82 | ($195.04) |
| − Principal repayments | | $41.55 | $43.23 | $44.98 | $46.80 | $48.70 | $50.67 | $52.72 | $54.86 | $57.08 | $59.39 |
| + Salvage value of mine | | | | | | | | | | | $250.00 |
| **Cash flow to equity** | **($831.60)** | **$37.82** | **$100.05** | **$211.33** | **$206.48** | **$203.44** | **$201.86** | **$205.91** | **$210.04** | **$214.22** | **$667.42** |
| PV @ 11.13% | ($831.60) | $34.03 | $81.02 | $153.99 | $135.40 | $120.04 | $107.18 | $98.39 | $90.31 | $82.89 | $232.38 |

**Equity NPV = $304.04 million** — positive, so the mine creates value for Vale's equity investors, confirming the ROE verdict. Note the year-0 outflow of $831.60M = $750M equity share of capex ($1,250M less the $500M borrowed) plus $81.60M of initial working capital.

The equity IRR is the discount rate at which this stream's NPV hits zero; graphically it is where the equity NPV profile crosses the axis. Accept if equity IRR > cost of equity.

**Determinism:** DETERMINISTIC — feed a script the operating assumptions, the loan terms, and the tax rate. It returns the amortization schedule, the income statement, and the book-equity roll-forward. From those it computes annual and average ROE, the cash flow to equity, the equity NPV, and the equity IRR. JUDGMENT — the financing plan (how much debt, at what rate), the operating assumptions, and the choice of a business-specific rather than company-wide cost of equity. That judgment needs the firm's credit rating and cost of debt, the segment's bottom-up beta, and the currency of the cash flows.

**Pitfalls:**
- Subtracting the *full* initial investment as an equity capex when part of it is borrowed. Only the equity share is an equity outflow.
- Forgetting to subtract principal repayments, which turns a levered project into an unlevered one halfway through.
- Discounting cash flows to equity at a cost of capital, which double counts the debt benefit.
- Using the company-wide cost of equity when the project sits in a specific business with a different beta. The Vale mine uses the iron ore rate of 11.13%, not the 11.23% company rate.
- Treating ROE's steep climb in later years as improving performance. Book equity shrinks as assets depreciate and debt is repaid.
- Running an equity analysis for a project whose financing mix will drift, where the firm-side analysis is more robust.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.261-270
- corporate_finance--lecture_slides--cfpacket1spr20 p.284

**Related:** [[accounting-returns-roc-roe-eva]], [[earnings-vs-cash-flows]], [[npv-and-irr-mechanics]], [[project-hurdle-rate-selection]], [[uncertainty-payback-sensitivity-simulation]], [[cost-of-equity]], [[bottom-up-beta]]

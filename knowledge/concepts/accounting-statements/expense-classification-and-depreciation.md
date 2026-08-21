# Expense classification and depreciation

**Core idea:** Every expense a firm incurs falls into exactly one of three classes. Operating expenses arise from running the business this period. Financing expenses arise from using non-equity funding, most often interest on debt. Capital expenses buy benefits that last many years. Where an expense lands decides which statement it hits and when. Operating and financing expenses are netted from revenues now. Capital expenses become assets on the balance sheet and are written off over the asset's life as depreciation. This split is the second reason earnings differ from cash flows. It is also the classification accounting handles worst for firms that do not make physical goods.

**Formulas:**
- `Operating Profit = Revenues − Operating Expenses` (see [[income-statement-structure]] for the full ladder).
- Straight-line accounting depreciation: `Annual Depreciation = (Cost − Salvage Value) / Useful Life`. Cost = capitalized purchase price; Salvage Value = expected residual at end of life; Useful Life = years of assumed service.
- Net book value: `Net Book Value at time t = Cost − Accumulated Depreciation through t`.
- Net carrying value of a definite-lived intangible: `Net Carrying Value = Gross Carrying Value − Accumulated Amortization`.
- Effect on earnings versus cash: `Cash Flow = Earnings + Non-cash expenses − Capital Expenditures − Change in non-cash Working Capital`.

**Reference data:** The three expense classes.

| Class | Test | Income statement effect | Balance sheet effect |
|---|---|---|---|
| Operating | Tied to operations this period, with no benefit spilling into future years | Netted from revenues to get operating profit | None directly |
| Financing | Tied to the use of non-equity funding (mainly interest) | Netted from operating profit to get taxable income | The borrowing behind it sits as debt |
| Capital | Gives benefits over many years | Only the annual depreciation/amortization charge | Recorded as an asset, written down over its life |

The three forms of depreciation.

| Form | What it measures | How it is set | Nature |
|---|---|---|---|
| Economic | The real loss in value (earning power) as an asset ages | Varies even within one asset type, by how the asset is used | Requires nuance and estimation |
| Accounting | Book write-off for financial reporting | Mostly by asset age; straight-line (even) or accelerated (faster up front) | Mechanical once method and life are chosen |
| Tax | What the tax authority allows in computing taxable income | Statutory schedules | Mechanical, set by tax code |

Coca-Cola's intangible amortization, 2019 ($ millions), as an illustration of definite-lived write-off:

| Item | Gross carrying | Accumulated amortization | Net carrying |
|---|---|---|---|
| Customer relationships | 344 | (177) | 167 |
| Bottlers' franchise rights | 341 | (94) | 247 |
| Trademarks | 177 | (99) | 78 |
| Other | 55 | (30) | 25 |
| Total | 917 | (400) | 517 |

**Procedure:**
1. List every expense line in the income statement and in the operating section of the cash flow statement.
2. For each, ask the three questions in order. Does it fund the business through non-equity capital? → financing. Does its benefit last beyond this year? → capital. Otherwise → operating.
3. Split operating expenses into COGS and other operating expenses. Directly tied to producing the revenue-generating goods → COGS. Operations-related but not directly tied → other operating (typically SG&A).
4. Identify expenses the firm treats as operating that behave like capital. R&D and brand-building are the classic cases. Accounting expenses them; economically they buy multi-year benefits. Flag them for capitalization if your analysis calls for it.
5. Find the depreciation and amortization figure. Check the income statement, the D&A add-back in the cash flow statement, and the PP&E footnote. They should agree.
6. Determine which depreciation concept you need. For book earnings use accounting depreciation. For cash taxes use tax depreciation. For economic value use economic depreciation, which you must estimate.
7. Compare accumulated depreciation with gross PP&E. A high ratio means an old, heavily written-down asset base.
8. Do not adjust the classification just because it flatters the numbers. See [[extraordinary-items-and-pro-forma-earnings]].

**Worked example:** Toyota, 31 March 2020 (¥ millions). Total PP&E at cost was 24,457,088 with accumulated depreciation of (13,855,563), giving net PP&E of 10,601,525. Accumulated depreciation is 56.7% of gross cost. That ratio marks an aging asset base: more than half the original capital expense has already run through the income statement as depreciation. Contrast Peloton in 2019, where property and equipment net of 249.7 million sits on a young, barely depreciated base built almost entirely in the prior two years.

**Determinism:**
- DETERMINISTIC: accounting depreciation given method, cost, salvage and life; tax depreciation given the statutory schedule; net book value; net carrying value of intangibles; the accumulated-to-gross ratio; the three profit subtractions once buckets are fixed.
- JUDGMENT: sorting each expense into operating, financing or capital. Economic depreciation is entirely judgment — it varies by how the asset is used and needs knowledge of the asset's real earning power. Deciding whether R&D or brand spending should be recapitalized is judgment and needs multi-year expense history plus an assumed amortizable life.

**Pitfalls:**
- Accepting the accounting classification for firms that do not make physical goods. Their capital expenses "take less solid forms" and accounting handles them poorly.
- Confusing the three depreciation concepts. Book depreciation is not economic depreciation and neither is tax depreciation.
- Treating SG&A as a clean bucket. It is a vague catch-all that can hold almost anything, which is what breaks cross-firm gross-margin comparisons.
- Missing depreciation embedded inside COGS. Some filers do not break it out on the face of the income statement.
- Shifting expenses from operating to capital to flatter earnings. That is one of the two pro-forma abuses the source singles out.

**Sources:**
- accounting__101--income_statements p.3-5
- accounting__101--income_statements p.8-9
- accounting__101--balance_sheet_illustrations p.7
- accounting__101--balance_sheet_illustrations p.8
- foundations_of_finance--cash_flows p.2

**Related:** [[income-statement-structure]], [[accrual-accounting-and-revenue-recognition]], [[extraordinary-items-and-pro-forma-earnings]], [[intangibles-and-goodwill]], [[earnings-versus-cash-flows]], [[investing-cash-flows-and-reinvestment]], [[capitalizing-rd-and-leases]]

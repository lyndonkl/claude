# Earnings versus cash flows

**Core idea:** Accounting earnings are not spendable cash. Two accounting principles create the gap. Accrual accounting records revenue when goods or services are delivered, not when cash arrives, and matches expenses to that revenue. The operating-versus-capital distinction expenses only outlays tied to current-period revenue, and spreads multi-period outlays over time as depreciation or amortization. Three adjustments bridge earnings to cash flow: add back non-cash charges such as depreciation, subtract cash outflows that were never expensed (capital expenditures), and adjust for changes in working capital. Depreciation matters only through its tax shield. Capital expenditures matter fully. Working capital ties up cash that cannot be used elsewhere.

**Formulas:** Symbols: `EBIT` = operating income; `t` = marginal tax rate; `D&A` = depreciation and amortization; `CapEx` = capital expenditures (growth plus maintenance); `ΔWC` = change in non-cash working capital.
- `After-tax operating income = EBIT × (1 − t)`
- `Cash flow to the firm = EBIT(1 − t) + D&A − CapEx − ΔWC`
- `Depreciation tax benefit = Depreciation × t`
- `Non-cash working capital = current assets excluding cash − current liabilities excluding debt`; commonly modeled as a percent of revenues
- Book value roll-forward: `BV(t) = BV(t−1) + CapEx(t) − Depreciation(t)`
- Depreciation from a percentage schedule: `Depreciation(t) = depreciation% (t) × BV of fixed assets at end of t−1`

**Procedure:**
1. Build the project income statement top-down: revenues by segment, direct operating expenses (usually a percent of revenues), depreciation and amortization, then any allocated overhead.
2. Tax operating income at the **marginal** rate, not the effective rate. Negative operating income generates a tax credit at the same rate if the firm has other income to shelter.
3. Never deduct interest expense in the project's operating cash flows. Financing effects belong in the discount rate through the after-tax cost of debt. Including them in both double counts.
4. Add back depreciation and amortization in full. Their only cash effect is the tax saving already captured in step 2.
5. Drop any non-cash charge that is not tax deductible (e.g. goodwill amortization). It has zero cash-flow effect.
6. Subtract capital expenditures, split into growth capex (creates new assets) and maintenance capex (keeps existing assets going). Maintenance needs rise with project life: a 25-year project needs far more than a 2-year project.
7. Subtract the change in non-cash working capital each year. An increase is an outflow; a decrease is an inflow. Recover (salvage) the remaining working capital at the end of project life.
8. Choose depreciation method deliberately. Straight line reports higher near-term income; accelerated produces higher near-term *cash flow* through bigger early tax shields. For value maximization prefer accelerated for tax purposes.

**Reference data:** Rio Disney assumption set (2020 packet, $ millions) — a template for how these assumptions are usually specified:

| Assumption | Value |
|---|---|
| Park direct operating expenses | 60% of park revenues |
| Resort direct operating expenses | 75% of resort revenues |
| Allocated corporate G&A | 15% of total revenues (only 1/3 variable) |
| Non-cash working capital | 5% of revenues, invested at end of each year |
| Marginal tax rate | 36.1% |
| Pre-project (sunk) investment | $500, straight line 10 yrs = $50/yr |
| Magic Kingdom capex | $2,000 at t=0, $1,000 at t=1 |
| Epcot Rio capex | $1,000 at t=2, $500 at t=3 |

Depreciation and capital maintenance schedule (Rio Disney):

| Year | Depreciation as % of book value | Capital maintenance as % of depreciation |
|---|---|---|
| 1 | 0.00% | 0% |
| 2 | 12.50% | 50% |
| 3 | 11.00% | 60% |
| 4 | 9.50% | 70% |
| 5 | 8.00% | 80% |
| 6 | 8.00% | 90% |
| 7 | 8.00% | 100% |
| 8 | 8.00% | 105% |
| 9 | 8.00% | 110% |
| 10 | 8.00% | 110% |

**Worked example:** Rio Disney, earnings then cash flow ($ millions).

Income statement:

| Item | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Total revenues | $0 | $1,250 | $1,750 | $2,500 | $3,125 | $3,438 | $3,781 | $4,159 | $4,575 | $4,667 |
| Total direct expenses | $0 | $788 | $1,103 | $1,575 | $1,969 | $2,166 | $2,382 | $2,620 | $2,882 | $2,940 |
| Depreciation & amortization | $50 | $425 | $469 | $444 | $372 | $367 | $364 | $364 | $366 | $368 |
| Allocated G&A (15% of revenue) | $0 | $188 | $263 | $375 | $469 | $516 | $567 | $624 | $686 | $700 |
| Operating income | −$50 | −$150 | −$84 | $106 | $315 | $389 | $467 | $551 | $641 | $658 |
| Taxes @36.1% | −$18 | −$54 | −$30 | $38 | $114 | $141 | $169 | $199 | $231 | $238 |
| After-tax operating income | −$32 | −$96 | −$54 | $68 | $202 | $249 | $299 | $352 | $410 | $421 |

Cash flow to the firm:

| Item | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| After-tax operating income | | −$32 | −$96 | −$54 | $68 | $202 | $249 | $299 | $352 | $410 | $421 |
| + D&A | $0 | $50 | $425 | $469 | $444 | $372 | $367 | $364 | $364 | $366 | $368 |
| − Capital expenditures | $2,500 | $1,000 | $1,188 | $752 | $276 | $258 | $285 | $314 | $330 | $347 | $350 |
| − Change in non-cash WC | | $0 | $63 | $25 | $38 | $31 | $16 | $17 | $19 | $21 | $5 |
| **Cash flow to firm** | **($2,500)** | **($982)** | **($921)** | **($361)** | **$198** | **$285** | **$314** | **$332** | **$367** | **$407** | **$434** |

Depreciation tax benefits at 36.1%: year 2 = 425 × 0.361 = $153; year 10 = 368 × 0.361 = $133.

**Determinism:** DETERMINISTIC — given revenues, expense ratios, a depreciation schedule, a capex schedule, a working-capital ratio, and a tax rate, a script computes the full income statement, the book-value roll-forward, and the cash-flow-to-firm line. JUDGMENT — the revenue forecast itself, the expense ratios, choice of depreciation method, the split between growth and maintenance capex, and the marginal tax rate. That judgment needs the firm's historical margins, the tax code's depreciation schedule, and comparable projects' maintenance requirements.

**Pitfalls:**
- Ignoring working capital entirely. It overstates cash flows and makes every project look better than it is.
- Forgetting to salvage working capital at the end of the project.
- Adding back a non-deductible non-cash charge as if it produced a tax shield.
- Deducting interest in the cash flows *and* using a WACC discount rate (double counting the debt benefit).
- Taxing project income at the effective rate. Netflix's effective rate is 10% but its marginal rate is 25%; incremental project income is taxed at the marginal rate.
- Omitting maintenance capex on a long-lived project, which silently assumes the assets never wear out.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.208
- corporate_finance--lecture_slides--cfpacket1spr20 p.212-219
- corporate_finance--lecture_slides--cfpacket1spr20 p.230-235
- corporate_finance--case--netflixfit p.2
- corporate_finance--case--netflixfitpresentation p.6
- corporate_finance--case--netflixfitpresentation p.8

**Related:** [[incremental-cash-flow-principle]], [[accounting-returns-roc-roe-eva]], [[npv-and-irr-mechanics]], [[terminal-value-and-project-life]], [[equity-side-project-analysis]], [[capital-budgeting-model]], [[marginal-vs-effective-tax-rate]]

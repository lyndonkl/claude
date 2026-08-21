# Closing the cash flows: salvage, terminal value and life assumptions

**Core idea:** Every project model stops somewhere, and how it stops drives a large share of the answer. A project with a short finite life is closed with a **salvage value**: the proceeds from selling everything at the end, usually taken as the book value of fixed assets plus recovered working capital. A project with a long or indefinite life is closed with a **terminal value**: the present value, at the end of the estimation period, of every cash flow after it, valued as a growing perpetuity. The growth rate in that perpetuity must be modest — the inflation rate is the standard conservative choice. Growth and reinvestment must be consistent: a project cannot grow forever while spending nothing on maintaining its asset base. Extending a project's assumed life is not free. It buys a terminal value at the cost of maintenance capex in every intermediate year.

**Formulas:** Symbols: `CF_{n+1}` = cash flow in the first year after the estimation period; `r` = cost of capital; `g` = perpetual growth rate; `n` = length of the estimation period.
- `Terminal value at end of year n = CF_{n+1} / (r − g)`, requires `r > g`
- `PV of terminal value = Terminal value_n / (1 + r)^n`
- `Salvage value ≈ book value of fixed assets + recovered working capital` (short finite life)
- Perpetual-growth maintenance capex: `Maintenance capex_t = Depreciation_t × (1 + inflation)` when g = inflation

**Procedure:**
1. Decide the project's life honestly. Ask how long the competitive advantage, the technology, or the license actually lasts.
2. Short finite life → estimate salvage. Default to book value of fixed assets at the end of life plus the full recovery of working capital. Adjust if the asset has a known resale market.
3. Long or indefinite life → forecast explicitly for a reasonable estimation period (10 years is the packet standard), then apply a terminal value.
4. Set the terminal-year cash flow to a **steady state** number. Strip out growth-related items that no longer apply — new-customer acquisition costs, ramp-up capex, working-capital build.
5. Cap `g` at the inflation rate unless there is a defensible reason for real growth. A perpetual growth rate above the economy's growth rate is not credible.
6. Match the reinvestment assumption to the growth assumption using the consistency table below.
7. Discount the terminal value back n years and add it to the year-n cash flow.
8. Report the terminal value's share of total NPV. If it dominates, the answer rests almost entirely on the perpetuity assumption.

**Reference data:** Growth-versus-reinvestment consistency rules:

| Life / growth assumption | Required capital expenditure assumption |
|---|---|
| Project ends at a fixed date | No (or very low) capital maintenance; let assets run down toward end of life |
| Infinite life, g = 0% | Capital maintenance = depreciation; invested capital held at base level |
| Infinite life, g = inflation | Capital maintenance > depreciation; invested capital grows at the inflation rate |
| Infinite life, g > inflation | Capital investment to increase capacity; maintenance well above depreciation; invested capital grows to reflect real growth |

**Worked example:** Two contrasting closures.

*Rio Disney, perpetual life.* Year-10 incremental cash flow to the firm = $715 million. Cash flows after year 10 grow at 2% (US inflation) forever. Cost of capital = 8.46%. Terminal value at end of year 10 = 715 × 1.02 / (0.0846 − 0.02) = **$11,275 million**. Discounted with the year-10 cash flow: (715 + 11,275)/1.0846^10 = $5,321 million, which is 161% of the project's total NPV of $3,296 million. The terminal value carries the decision.

*Netflix Fit, finite versus infinite.* The 10-year finite case assumes the business is wrapped up at the end of year 10, so it needs no meaningful maintenance capex, and it recovers a $400 million salvage value plus working capital. NPV = $106 million stand-alone. The infinite-life case requires maintenance capex exceeding depreciation by 1% (the inflation rate) in every year: $202.00 in year 1 rising to $223.13 in year 11 against $200 of depreciation. That costs roughly $168–187 million of cash flow every intermediate year. In exchange, year 11 steady-state FCFF of $244.33 million capitalizes into a terminal value of 244.33/(0.0801 − 0.01) = **$3,486 million** at end of year 10. Stand-alone NPV rises to $365 million. Note the year-11 cash flow is far below year 10's, because subscriber growth stops and the add-on subscriber economics disappear.

Year-by-year trade-off ($ millions):

| Year | Finite | Perpetual | Differential |
|---|---|---|---|
| 0 | (2,500.00) | (2,500.00) | 0.00 |
| 1 | 132.94 | (35.19) | (168.13) |
| 2 | 200.68 | 30.87 | (169.81) |
| 3 | 272.66 | 101.15 | (171.51) |
| 4 | (171.29) | (344.51) | (173.22) |
| 5 | 459.60 | 284.65 | (174.95) |
| 6 | 944.35 | 757.25 | (187.10) |
| 7 | 442.58 | 264.38 | (178.20) |
| 8 | 484.43 | 304.45 | (179.99) |
| 9 | 528.60 | 346.81 | (181.79) |
| 10 | 1,143.52 | 3,917.23 | 2,773.71 |

**Determinism:** DETERMINISTIC — given `CF_{n+1}`, `r`, and `g`, the terminal value is one division; discounting it back is one exponent. The maintenance-capex schedule implied by a chosen growth rate is a mechanical roll-forward. JUDGMENT — the project life, the perpetual growth rate, and what "steady state" means for the terminal-year cash flow. That judgment needs the durability of the competitive advantage, the technology cycle, and the long-run inflation outlook in the cash flows' currency.

**Pitfalls:**
- Capitalizing the *last forecast year's* cash flow when that year is still in growth mode, inheriting growth-phase economics into perpetuity. Netflix Fit's year 10 FCFF of $3,917 million (including TV) versus its year 11 steady-state $244 million shows the size of that error.
- Assuming perpetual growth while setting maintenance capex to zero. Growth without reinvestment is arithmetically impossible.
- Using a perpetual growth rate above the riskfree rate or the economy's nominal growth rate.
- Using a nominal growth rate with a real discount rate, or vice versa. See [[currency-and-inflation-consistency]].
- Extending the life to make a marginal project look good. Netflix Fit's NPV triples on an infinite-life assumption, but technology is a fickle advantage and the perpetual assumption may be too generous.
- Setting salvage value at original cost rather than end-of-life book value, or forgetting the working-capital recovery.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.245
- corporate_finance--lecture_slides--cfpacket1spr20 p.246
- corporate_finance--case--netflixfit p.7
- corporate_finance--case--netflixfitpresentation p.10-11
- corporate_finance--case--netflixfitpresentation p.15-21

**Related:** [[time-value-and-cash-flow-timing]], [[npv-and-irr-mechanics]], [[earnings-vs-cash-flows]], [[comparing-projects-different-lives]], [[currency-and-inflation-consistency]], [[netflix-fit-case]], [[assessing-existing-investments]]

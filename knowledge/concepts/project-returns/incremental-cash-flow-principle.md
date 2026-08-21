# Incremental cash flows: sunk and allocated costs

**Core idea:** Only cash flows that change because of the decision belong in the analysis. Two categories routinely violate that rule. **Sunk costs** are expenditures already incurred that cannot be recovered whether or not the project goes ahead — test marketing, R&D, licenses, feasibility studies. They are excluded, along with the depreciation tax shield on any capitalized portion, because that shield exists either way. **Allocated costs** are shares of a central pool (usually G&A) charged to the project on some basis such as sales or earnings. Only the genuinely variable part is incremental. The fixed part would exist regardless, so charging it to the project can kill investments that would have made the firm better off. Two routes reach the same answer: adjust total cash flows for the non-incremental pieces, or build the cash flows incrementally from the start.

**Formulas:** Symbols: `t` = marginal tax rate.
- Adjustment route: `Incremental CF = Cash flow to firm + sunk investment charged at t=0 − (sunk asset depreciation × t) + (non-incremental allocated expense × (1 − t))`
- Direct route: `Incremental CF = Incremental EBIT × (1 − t) + incremental depreciation − incremental capex − Δ incremental working capital`, where incremental depreciation excludes depreciation on sunk assets and incremental capex excludes sunk outlays.
- Fixed/variable split from a regression of G&A on revenues: `G&A = fixed + slope × Revenues`. The slope is the variable (incremental) cost per dollar of revenue.

**Procedure:**
1. Write down the counterfactual explicitly: what the firm's cash flows look like if it does *not* take the project.
2. List every outlay already made on the project. Exclude all of it. Also strip the depreciation tax shield on any capitalized sunk asset, because that shield survives rejection.
3. Identify allocated overhead charged to the project. Split it into fixed and variable components.
4. To make the split empirically, regress a time series of company G&A on company revenues. The slope is the variable rate; the intercept is the fixed pool.
5. Charge only the variable share to the project, plus any *truly new* overhead the project causes (new headcount, new systems).
6. Build the cash flows either way — adjust the total, or build directly from incremental lines. The two must reconcile up to rounding.
7. Add the side costs and side benefits that ordinary accounting misses. See [[opportunity-costs-and-side-costs]] and [[project-synergies]].
8. Ex ante, police the sunk costs before they are incurred. Build expected downstream test-marketing and R&D spending into planning-level hurdle requirements, even though each project decision correctly ignores them ex post.

**Reference data:** Fixed/variable split of G&A from a revenue regression (packet example):

| Year | Revenues | G&A costs |
|---|---|---|
| 1 | $1,000 | $250 |
| 2 | $1,200 | $270 |
| 3 | $1,500 | $300 |

G&A rises $50 per $500 of revenue, so variable cost = 10% of revenues and the fixed pool = $150.

Rio Disney: allocated G&A = 15% of revenues, of which one third (5% of revenues) is variable and incremental; two thirds is fixed.

Netflix Fit: Netflix *allocates* 4% of existing firm-wide G&A ($1.5 billion in the most recent year, growing 5%/yr for 10 years with or without the project). None of that allocation is incremental. Separately, the project causes a genuinely new $50 million of G&A in year 1, growing with the division's dollar revenues thereafter. Netflix Fit's $250 million of already-expensed fitness R&D is sunk and unrecoverable.

**Worked example:** Rio Disney, both routes ($ millions).

Adjustment route:

| Item | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Cash flow to firm (total) | ($2,500) | ($982) | ($921) | ($361) | $198 | $285 | $314 | $332 | $367 | $407 | $434 |
| + Pre-project investment (sunk) | $500 | | | | | | | | | | |
| − Pre-project depreciation × 36.1% | | $18 | $18 | $18 | $18 | $18 | $18 | $18 | $18 | $18 | $18 |
| + Non-incremental allocated G&A × (1−t) | | $0 | $80 | $112 | $160 | $200 | $220 | $242 | $266 | $292 | $298 |
| **Incremental cash flow to firm** | **($2,000)** | **($1,000)** | **($860)** | **($267)** | **$340** | **$467** | **$516** | **$555** | **$615** | **$681** | **$715** |

Direct route (incremental G&A = 5% of revenues; capex excludes the sunk $500; depreciation excludes the $50/yr on the sunk asset):

| Item | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Revenues | | $0 | $1,250 | $1,750 | $2,500 | $3,125 | $3,438 | $3,781 | $4,159 | $4,575 | $4,667 |
| Direct expenses | | $0 | $788 | $1,103 | $1,575 | $1,969 | $2,166 | $2,382 | $2,620 | $2,882 | $2,940 |
| Incremental depreciation | | $0 | $375 | $419 | $394 | $322 | $317 | $314 | $314 | $316 | $318 |
| Incremental G&A | | $0 | $63 | $88 | $125 | $156 | $172 | $189 | $208 | $229 | $233 |
| Incremental operating income | | $0 | $25 | $141 | $406 | $678 | $783 | $896 | $1,017 | $1,148 | $1,175 |
| − Taxes @36.1% | | $0 | $9 | $51 | $147 | $245 | $283 | $323 | $367 | $415 | $424 |
| Incremental after-tax operating income | | $0 | $16 | $90 | $260 | $433 | $500 | $572 | $650 | $734 | $751 |
| + Incremental depreciation | | $0 | $375 | $419 | $394 | $322 | $317 | $314 | $314 | $316 | $318 |
| − Capital expenditures | $2,000 | $1,000 | $1,188 | $752 | $276 | $258 | $285 | $314 | $330 | $347 | $350 |
| − Change in non-cash WC | | $0 | $63 | $25 | $38 | $31 | $16 | $17 | $19 | $21 | $5 |
| **Cash flow to firm** | **($2,000)** | **($1,000)** | **($859)** | **($267)** | **$340** | **$466** | **$516** | **$555** | **$615** | **$681** | **$715** |

The two routes agree to rounding ($859 vs $860 in year 2).

Sunk-cost quandary: a consumer products firm spent $100 million on test marketing. Ignoring that spend, the project's incremental cash flows create $25 million of value. Take the project — the $100 million is gone either way. But a firm whose every project carries sunk costs exceeding value added cannot survive; ex ante it destroyed $75 million. The fix is upstream discipline on the test-marketing budget, not a wrong ex-post rule.

**Determinism:** DETERMINISTIC — given total cash flows, the sunk amounts, the fixed share of allocated costs, and the tax rate, a script produces the incremental series. The fixed/variable regression is a closed-form OLS on revenues. JUDGMENT — deciding *which* outlays are truly unrecoverable, what fraction of allocated overhead is fixed, and whether new overhead is genuinely caused by the project. That judgment needs a G&A time series, the cost accounting behind the allocation, and management's plan for headcount and systems.

**Pitfalls:**
- Behavioral research shows managers find it nearly impossible to ignore sunk costs. The rule is easy; the discipline is not.
- Forgetting to remove the depreciation tax benefit on a capitalized sunk asset, which quietly leaves part of the sunk cost in the analysis.
- Letting big fixed allocations kill positive-value projects in large firms.
- Treating *all* allocated costs as non-incremental. The variable share is real and must be charged.
- Double counting when mixing the adjustment route and the direct route in the same model.
- Using the sunk-cost rule as license to spend freely on R&D and test marketing before the decision point.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.209
- corporate_finance--lecture_slides--cfpacket1spr20 p.213
- corporate_finance--lecture_slides--cfpacket1spr20 p.215
- corporate_finance--lecture_slides--cfpacket1spr20 p.236-241
- corporate_finance--case--netflixfit p.2
- corporate_finance--case--netflixfit p.4
- corporate_finance--case--netflixfitpresentation p.6
- corporate_finance--case--netflixfitpresentation p.10

**Related:** [[earnings-vs-cash-flows]], [[opportunity-costs-and-side-costs]], [[project-synergies]], [[npv-and-irr-mechanics]], [[investment-analysis-first-principles]], [[assessing-existing-investments]], [[netflix-fit-case]]

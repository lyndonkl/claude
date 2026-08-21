# Framework: The intrinsic valuation playbook

**Scope.** End-to-end orchestration of a discounted-cash-flow valuation of a company, from the
narrative and the landscape survey to a value per share, a price comparison and a feedback loop.
This document sequences the work, fixes the decision rules and thresholds at each branch, names the
consistency invariants that bind the stages together, and states which errors invalidate downstream
work. Detail lives in the concept files; this file exists only to run them in the right order with
the right couplings.

**How to read it.** Stages S0–S18 run in order. Branches B1–B10 are overlays selected at S0 and S4;
each branch names the stages it modifies and how. Section C is the cross-cutting invariant set —
every rule there binds more than one stage, which is why it is not owned by any of them. Section D
is the circularity register: four places where the pipeline is not a DAG and must be solved by
fixed-point iteration. Section E is the terminal validation gate. Section F is the double-count
register, which is the single most productive audit in this domain.

**Counting.** 19 stages (S0–S18), 10 branches (B1–B10).

---

## 0. The spine in one page

```
S0  Mandate + classification        -> currency, date, claim type, company type, route, constraints
S1  Landscape survey + base year    -> business map, TTM base financials, industry benchmarks
S2  Narrative: write, grade, screen -> prose story, claim ledger graded possible/plausible/probable
S3  Statement cleanup + normalize   -> adjusted EBIT/NI, invested capital, debt, reinvestment
S4  MODEL SELECTION (branch point)  -> {dividends|FCFE|FCFF} x {1|2|3|n stages} x {nominal|real} x currency
S5  Riskfree rate                   -> Rf in valuation currency
S6  Equity risk premium             -> ERP = mature + operation-weighted CRP
S7  Relative risk (beta)            -> bottom-up levered beta (or total beta)
S8  Cost of debt                    -> pre-tax kd, after-tax kd
S9  Cost of capital assembly        -> ke, WACC, per-division rates, per-year rate path
S10 Cash flow construction          -> FCFF / FCFE / DPS schedule definition
S11 Growth                          -> growth path (fundamental route or revenue route)
S12 Terminal value                  -> stable-phase parameter set + TV
S13 Discount -> operating assets    -> PV(CF) + PV(TV), failure adjustment
S14 Equity bridge                   -> + cash, holdings, other; - debt, claims, options
S15 Value per share + price         -> per-share value, gap, expected return
S16 Uncertainty                     -> sensitivity grid, scenario grid, simulation
S17 VALIDATION GATE                 -> the consistency and screen battery; pass/fail
S18 Feedback loop                   -> counter-narratives, break/shift/change taxonomy, re-run
```

The four hard couplings that make this a pipeline rather than a list of steps:

1. **S4 fixes S9, S10, S11 and S12 simultaneously.** Cash flow choice determines discount rate,
   growth measure, terminal-value formula and bridge structure. Choosing them independently is the
   most common structural error. `concepts/dcf-model-choice-loose-ends/dcf-model-choice-framework.md`
2. **S3 changes both the numerator and the denominator.** Capitalizing leases and R&D moves EBIT,
   invested capital, debt, the coverage ratio, the rating, the cost of debt and the cost-of-capital
   weights. Adjusting one side only corrupts ROIC and therefore growth.
3. **S11 and S12 are not free.** Growth is bought with reinvestment at a return: `g = RIR × ROC`
   forward, `RIR = g/ROC` in the terminal year. Setting growth and reinvestment independently
   silently asserts an ROIC nobody examined.
4. **S5 caps S12.** The riskfree rate is inflation plus real growth in that currency, so perpetual
   nominal growth cannot exceed it. A normalized-up riskfree rate with untouched growth assumptions
   biases every valuation downward.

---

## S0. Mandate and classification

**Purpose.** Fix the four parameters that every later stage inherits, and route the company to the
branch set that applies. Classification precedes everything: standard machinery run on a bank, a
money-loser or a cyclical at a trough produces confident nonsense.

**Inputs (external).** Company identity; filings (last 10-K/annual report plus latest interim);
market data (price, shares, sovereign rates, ratings); the analyst's purpose (investment decision,
acquisition, IPO, litigation, restructuring).

**Procedure.**
1. **Fix the valuation currency and date.** Everything downstream must match both. Record them.
2. **Fix the claim being valued.** Contractual, residual or contingent. This valuation prices a
   residual claim; contingent claims are valued separately and added once (see B9).
   `concepts/finance-foundations/finance-first-principles.md`,
   `concepts/accounting-statements/cash-flow-claim-types.md`
3. **Bias audit before opening the model.** Name who pays for the valuation, what answer they want,
   any public position already taken, and whether the market price has been seen. Do the qualitative
   work before looking at price. `concepts/narrative-numbers/valuation-misconceptions.md`
4. **Classify the company on six axes:**

   | Axis | Values | Selects |
   |---|---|---|
   | Life-cycle stage | start-up / young growth / high growth / mature growth / mature stable / decline | dominant uncertainty, stage count, driver emphasis |
   | Earnings status | profitable / marginal / negative / cyclical trough or peak | B2 (revenue route) or B7 (normalization) |
   | Sector type | non-financial / financial service / commodity-cyclical / real estate | B3 |
   | Ownership and buyer | public / private / division / IPO; diversified vs undiversified buyer | B5 |
   | Geography | incorporation vs revenue and production footprint | B4 |
   | Intangible intensity | low / moderate / high | R&D capitalization in S3 |

   Distress markers (negative equity from losses, coverage < 1, bonds at deep discounts, going-concern
   qualification) trigger B6 regardless of the other axes.
   `concepts/dark-side-difficult/difficult-company-taxonomy.md`,
   `concepts/accounting-statements/life-cycle-patterns-in-financial-statements.md`,
   `concepts/narrative-numbers/life-cycle-uncertainty.md`
5. **Identify the marginal investor.** High institutional ownership with active trading → diversified
   → beta prices only market risk. Closely-held with an undiversified owner → total beta (B5). The
   largest holder is not automatically marginal; marginality requires trading.
   `concepts/cost-of-equity/capm-cost-of-equity.md`
6. **Emit the constraint set.** Hard stops that every downstream stage must honor.

**Outputs.** `valuation_currency`, `valuation_date`, `claim_type`, classification vector, marginal
investor verdict, active branch list, constraint list.

**Constraint catalogue (hard stops).**

| Constraint | Trigger | Effect |
|---|---|---|
| `no-fcff-valuation` | financial service firm | S4 must pick dividends or FCFE/excess return |
| `no-optimal-debt-ratio` | financial service firm | regulatory capital governs, not a WACC schedule |
| `no-standard-growth-model` | negative or trough earnings | S11 must use the revenue route |
| `require-failure-probability` | young firm or distress markers | S13 must carry a failure branch |
| `require-total-beta` | private firm, undiversified buyer | S7 must scale beta by 1/sqrt(R²) |
| `require-illiquidity-discount` | private firm, non-liquid buyer | S15 applies a discount |
| `require-normalized-earnings` | cyclical/commodity at a cycle extreme | S3 normalizes before anything else |
| `no-perpetual-growth-above-riskfree` | universal | S12 caps `g ≤ Rf` in the valuation currency |

**Invalidating errors.** Wrong sector classification (running FCFF on a bank) invalidates S8–S15.
Wrong earnings status (using an earnings growth rate off a negative base) invalidates S11–S15.
Missing the undiversified-buyer case understates the discount rate and overstates value by 40–60%
(Bookscape: $13.40 vs $8.35 per dollar of perpetual cash flow).

---

## S1. Landscape survey and base-year assembly

**Purpose.** Produce the business-model map and the honest base-year numbers the narrative will be
argued against. This stage has a qualitative half and a numeric half, and both are prerequisites for
S2 — writing a story without benchmarks is how a valuation drifts into fantasy.

**Inputs.** S0 classification; filings; industry-average datasets; peer filings.

**Procedure.**
1. **Map the business model as a loop, not a list.** Suppliers, customers, who sets price, what slice
   the firm keeps, what it must invest in to grow. Six boxes is the working size.
2. **Update the base year to trailing 12 months.** `TTM = last 10-K figure − prior-year YTD + current-year YTD`,
   applied to revenues, EBIT, interest expense, R&D, taxes. Record `years_since_last_10K`. Prioritize
   the update for small, volatile or recently restructured firms.
3. **Pull the balance-sheet base:** book equity, book debt (all interest-bearing plus leases), cash and
   marketable securities, cross-holdings, minority interests.
4. **Get a comprehensive share count:** actual shares outstanding, plus a separate schedule of options
   and warrants (count, average strike, average remaining maturity), plus restricted stock already granted.
   Options are neither shares nor nothing.
5. **Benchmark against the industry and against the incumbents.** Revenue growth, pre-tax operating
   margin, sales-to-capital, ROIC, cost of capital, against US and global industry averages. For a
   company claiming it will become the largest player, look at what the largest players actually earn.
   Adjust dollar-denominated industry averages by the inflation differential before comparing to a
   non-dollar company.
6. **Read the quarterly trend** to test whether the story's claimed inflection has already started —
   as evidence, not as an extrapolation.

**Outputs.** Business-model map; base-year financial block (pre-cleanup); share and option schedule;
peer/industry benchmark table; life-cycle placement confirmation.

**Binding rules.** The base year assembled here is *pre-cleanup*. S3 rewrites EBIT, invested capital
and debt; nothing computed on the S1 numbers (margin, ROIC, sales-to-capital) may be carried past S3
without recomputation.

**Invalidating errors.** Valuing off a stale 10-K when three quarters have passed. Benchmarking a
global company against US-only industry averages. Counting employee options as ordinary shares, or
ignoring them.

**Concepts.** `concepts/narrative-numbers/landscape-survey.md`,
`concepts/accounting-statements/segment-and-geographic-reporting.md`,
`concepts/accounting-statements/life-cycle-patterns-in-financial-statements.md`,
`concepts/accounting-statements/role-of-accounting-and-three-statements.md`,
`concepts/accounting-statements/accounting-standards-gaap-ifrs.md`

---

## S2. Narrative: write it, grade it, screen it

**Purpose.** Produce a prose story and a graded ledger of its claims, so that every later input has a
sentence behind it and every claim has exactly one input. This stage is what stops S11's growth rate
from being a number pulled from a template.

**Inputs.** S1 business map and benchmarks; S0 classification.

**Procedure.**
1. **Write the narrative in prose, spreadsheet closed.** Three rules: keep it simple, keep it focused,
   stay grounded in reality. If it does not fit in a paragraph, it is not a narrative yet.
2. **Break the narrative into discrete claims.** One market, one capability, one margin path per claim.
3. **Grade each claim** on the assessability ladder and route it:

   | Grade | Definition | Where it goes | What promotes it |
   |---|---|---|---|
   | Probable | expected, with evidence (product success, financial results) | base-year numbers and expected cash flows (S10–S11) | — |
   | Plausible | reasoned argument, no tangible evidence yet | higher expected growth rate inside the DCF (S11) | product success + financial results |
   | Possible | probability cannot be assessed at all | option value added on top of the DCF (B9) | market-potential evidence + product testing |

   A claim may be routed exactly once. A market counted in revenues may not also be counted as option
   value. Record the promotion trigger for each claim so S18 has something to watch.
4. **Run the pre-model narrative screens.** These are qualitative at this stage and re-run mechanically
   at S17:
   - *Impossible:* perpetuity growth above the economy's growth rate; implied revenues above the total
     market; operating margin above 100%; depreciation above cap ex in perpetuity.
   - *Implausible:* growth without reinvestment; rising profits with no competitive response; high
     returns in a business with no risk.
   - *Improbable:* the growth/risk/reinvestment triangle — high growth with low risk, high growth with
     low reinvestment, low risk with high reinvestment. You may have a good outcome on one corner,
     sometimes two with a stated reason, never all three for free.
5. **Score the runaway-story ingredients.** Charismatic narrator + disliked status quo being disrupted
   + claimed societal benefit. Two or three yeses means write down the questions you have not asked
   and ask them, and test the core claim against first principles ("is this even possible?") rather
   than against execution risk.
6. **If the company is one of many chasing one market, run the aggregation test** before trusting any
   single-company story: impute each competitor's breakeven revenue in a common future year, multiply
   by its share of revenue from that market, sum, and compare with an independent forecast of total
   market size. `Σ implied market share ≤ 100%`.

**Outputs.** `narrative.md` (prose); claim ledger with grade, routed driver, and promotion trigger;
pre-model screen results; runaway-story score.

**Binding rules.** Every claim maps to exactly one of six drivers: total market, market share,
operating margin, reinvestment efficiency, discount rate, survival probability. A claim mapping to two
drivers is double counted; a claim mapping to none is decoration and should be deleted or moved to the
option layer.

**Invalidating errors.** Starting at the driver template and inventing a story afterwards — this
produces a rationalisation, not a valuation, and S17 cannot detect it. Skipping the grading step, so a
possible market enters the cash flows. Skipping the aggregation test in a hot sector.

**Concepts.** `concepts/narrative-numbers/story-to-numbers-process.md`,
`concepts/narrative-numbers/narrative-numbers-bridge.md`,
`concepts/narrative-numbers/possible-plausible-probable.md`,
`concepts/narrative-numbers/narrative-consistency-checks.md`,
`concepts/narrative-numbers/runaway-stories.md`,
`concepts/narrative-numbers/big-market-delusion.md`,
`concepts/narrative-numbers/bermuda-triangle-of-valuation.md`,
`concepts/narrative-numbers/three-approaches-to-valuation.md`

---

## S3. Statement cleanup and normalization

**Purpose.** Convert reported accounting into valuation inputs. Three operations in fixed order:
**update** (done at S1), **cleanse** (reclassify financial and capital expenses that accounting buried
in operating expenses, strip genuinely non-recurring items), **normalize** (if the current year is
unrepresentative). This stage produces the numerator base *and* half the denominator inputs.

**Inputs.** S1 base-year block and filings; S0 classification; a seed pre-tax cost of debt (see D1).

**Procedure, in this order.**

1. **Reconciliation ties first.** Before interpreting anything, confirm six ties: balance sheet
   balances; net income ties to the first line of the operating cash-flow section; retained-earnings
   roll-forward reconciles; D&A on the income statement ties to the cash-flow add-back; the three
   cash-flow sections plus FX tie to the change in cash; segments plus eliminations tie to consolidated
   totals. A failed tie means a transcription error or a missed mezzanine/NCI line, not an insight.

2. **Sort every expense into operating / financing / capital.** Test in order: does it fund the business
   through non-equity capital (financing)? does its benefit last beyond this year (capital)? otherwise
   operating. `concepts/accounting-statements/expense-classification-and-depreciation.md`

3. **Capitalize operating leases** (the financing-expense case). Deterministic given commitments and kd:
   - `n6 = ROUND(lump beyond year 5 / mean(C1..C5), 0)`; annual tail `A = lump / n6`.
   - `Lease debt = Σ_{t=1..5} C_t/(1+kd)^t + A·[1−(1+kd)^(−n6)]/kd · (1+kd)^(−5)`.
   - Leased asset = lease debt, by construction. Lease life `= 5 + n6`; depreciation `= lease debt / (5+n6)`.
   - `Adjusted EBIT = EBIT + current lease expense − lease depreciation` (short-cut: `EBIT + kd × lease debt`).
   - `Adjusted debt = interest-bearing debt + lease debt`. `Adjusted interest = interest + kd × lease debt`.
   - **Check: net income must be unchanged.** If it moves, the lease payment has been double counted.
   - Guards: lump = 0 → n6 = 0, lease life 5; all five commitments zero → guard the division; kd = 0 →
     use `n6 × A` undiscounted. ROUND is half-away-from-zero.
   - This is circular with the rating (see D1) whenever the cost of debt is synthetic.
   - Materiality: lease expense is ~12.5% of operating income market-wide, ~50% for furniture stores,
     ~44% apparel, ~27% restaurants. Post-2019 IFRS 16 / ASC 842 numbers are not equivalent to this
     calculation; recompute when the reported liability looks inconsistent.

4. **Capitalize R&D** (the capital-expense case) if intangible intensity is moderate or high. Choose an
   amortizable life `N` from the industry table (guideline blocks: non-technological service 2; retail
   and tech service 3; light manufacturing 5; heavy manufacturing 10; research with patenting 10; long
   gestation 10). Then:
   - `Research asset RA = Σ_{k=0..N} RD_k × (N−k)/N`; `Amortization AM = Σ_{k=1..N} RD_k / N`.
   - `Adjusted EBIT += RD_0 − AM`; `adjusted net income += RD_0 − AM`; **the add-back is not tax-effected**
     (the deduction was already taken). `Adjusted after-tax operating income = EBIT(1−t) + RD_0 − AM`.
   - `Adjusted book capital += RA`; `adjusted cap ex += RD_0`; `adjusted D&A += AM`.
   - **Check: FCFF must be unchanged.** Earnings and reinvestment rise by the same amount. What changes
     is EBIT, capital, ROIC and therefore growth.
   - Do not drop the year `−N` row: it contributes nothing to RA but does contribute to AM. If R&D is
     shrinking, `AM > RD_0` and the adjustment *lowers* operating income.
   - The same machinery capitalizes brand advertising and recruiting/training spend.

5. **Strip one-time items — with a recurrence test, not a label.** Over a window of N ≥ 5 years compute
   frequency (years the item appears / N) and variability (sd / mean absolute). Treat as extraordinary
   only when frequency is low **and** variability is high. If frequency = 1.0 the item is recurring
   whatever the firm calls it; if it recurs every k years, build `charge/k` into normalized earnings
   every year rather than excluding it. Reconcile every pro-forma add-back line by line to the audited
   statement.

6. **Screen for aggressive accounting** (six signals): income from unspecified sources; income from
   asset sales or financial transactions at a non-financial firm; sudden drops in SG&A or R&D as a
   percent of revenues; frequent restatements; accrual earnings persistently above cash earnings;
   large book-tax income gaps. Statement analysis catches aggressiveness, not fraud; the response is a
   haircut to earnings, a higher discount rate, or a failure probability — pick one.

7. **Decide the tax rate.** Effective (taxes / pre-tax income) versus marginal (statutory rate of the
   jurisdiction, or a revenue-weighted multi-country rate). Default anchor is the marginal rate; the
   standard forecast holds the effective rate for years 1–5 then ramps linearly to the marginal rate
   over years 6–10, with the marginal rate in perpetuity. If the firm has an NOL balance, carry it:
   `EBIT_t ≤ 0` → taxes 0 and `NOL_t = NOL_{t−1} + |EBIT_t|`; `0 < EBIT_t ≤ NOL_{t−1}` → taxes 0 and
   `NOL_t = NOL_{t−1} − EBIT_t`; otherwise `taxes = (EBIT_t − NOL_{t−1}) × t_marginal` and `NOL_t = 0`.
   **The same t must be used for the after-tax cost of debt in S8.** In zero-tax years the debt tax
   shield is also zero.

8. **Normalize if the base year is unrepresentative** — but only after diagnosing *why*:

   | Cause | Treatment |
   |---|---|
   | Temporary problem (one-off disruption) | Normalize |
   | Cyclicality (commodity, auto, in a recession) | Normalize |
   | Life-cycle (young firm, infrastructure build-out) | Do **not** normalize — forecast from revenues (B2) |
   | Leverage problem (healthy operations, too much debt) | Forecast from revenues, converge the debt ratio |
   | Long-term operating problem (structural cost/production) | Forecast from revenues to a sector-median margin |

   Normalization mechanics: if firm size is stable, average dollar earnings over a full cycle (5 years
   is the working default). If size has changed, use return-based normalization: `normalized EBIT(1−t)
   = average ROC × current invested capital`, `normalized NI = average ROE × current book equity`.
   Normalize the tax rate over the same window. Use the *pre-shock* cycle when a specific event
   destroyed the recent window. Be consistent: do not normalize EBIT and then feed current depressed
   coverage into the synthetic rating.

9. **Rebuild invested capital.** `Invested capital = BV equity + BV debt − cash − cross-holdings
   + research asset + leased asset`. Measure at the **start** of the period so the numerator's income
   was earned on it.

10. **Rebuild reinvestment.**
    - `Net cap ex = cap ex − depreciation`, both from the **cash-flow statement**.
    - `+ R&D − R&D amortization`; `+ normalized (multi-year average) acquisitions − their amortization`
      (acquisition amortization is usually already inside reported D&A — do not subtract it twice).
    - `Non-cash working capital = non-cash current assets − non-debt current liabilities`. Interest-bearing
      short-term borrowing and the current portion of long-term debt must be moved to the debt column
      first. Forecast NCWC as a **percent of revenues**, triangulated across the firm's own multi-year
      average and the industry average — never extrapolate the latest year's dollar change. Fade a
      large negative ratio toward zero rather than assuming it persists forever.
    - `Reinvestment = adjusted net cap ex + ΔNCWC`; `Reinvestment rate = Reinvestment / EBIT(1−t)`.
    - Hunt for reinvestment the filer classified as operating (content spend, capitalized software,
      originated receivables) and move it. Hunt for stock-funded acquisitions, which appear nowhere in
      the cash-flow statement.

11. **Compute the base ROIC and interrogate it** against six distortions before any growth rate is
    built on it: abnormal earnings; accounting misclassification (R&D, leases — now fixed); unusual
    items; life-cycle effect; write-offs that shrank the capital base; inflation-stale book values.

**Outputs.** `cleaned-financials`: adjusted EBIT and EBIT(1−t), adjusted net income, adjusted debt
(book and, after S8, market), invested capital, reinvestment and reinvestment rate, ROIC/ROE, working
capital ratio, tax rate path, NOL balance, normalization basis and window, adjustment log.

**Binding rules.**
- Every adjustment touches both statements. Lease debt without the leased asset understates capital and
  inflates ROIC. R&D add-back without the research asset does the same, more severely.
- The tax rate chosen here is the tax rate used in S8's `(1−t)`.
- Whatever was capitalized must be capitalized in **every** year of history used, or the trend is corrupted.

**Invalidating errors.** Adjusting EBIT and not invested capital (corrupts ROIC → corrupts S11 growth →
corrupts S12 terminal reinvestment). Tax-effecting the R&D add-back (the single most common porting
error). Normalizing a structural problem (values a company that no longer exists). Leaving interest-bearing
short-term debt inside working capital (double counts the borrowing). Using reported EBIT with a
lease-inclusive debt ratio in the WACC.

**Concepts.** `concepts/dcf-cashflows-growth/reported-to-actual-earnings.md`,
`concepts/dcf-cashflows-growth/operating-lease-capitalization.md`,
`concepts/dcf-cashflows-growth/rnd-capitalization.md`,
`concepts/dcf-cashflows-growth/normalizing-depressed-earnings.md`,
`concepts/dcf-cashflows-growth/tax-rate-and-nols.md`,
`concepts/dcf-cashflows-growth/net-capital-expenditures.md`,
`concepts/dcf-cashflows-growth/non-cash-working-capital.md`,
`concepts/dcf-cashflows-growth/return-on-invested-capital.md`,
`concepts/accounting-statements/extraordinary-items-and-pro-forma-earnings.md`,
`concepts/accounting-statements/liabilities-debt-and-leases.md`,
`concepts/accounting-statements/investing-cash-flows-and-reinvestment.md`,
`concepts/accounting-statements/cash-flow-from-operations-and-working-capital.md`,
`concepts/accounting-statements/earnings-versus-cash-flows.md`,
`concepts/accounting-statements/intangibles-and-goodwill.md`,
`concepts/accounting-statements/shareholders-equity-book-value.md`,
`concepts/accounting-statements/balance-sheet-views-and-asset-measurement.md`,
`concepts/accounting-statements/financial-balance-sheet.md`,
`concepts/dark-side-difficult/capitalizing-rd.md`,
`concepts/dark-side-difficult/normalized-earnings.md`

---

## S4. MODEL SELECTION — the branch point

**Purpose.** Choose the three building blocks of the DCF simultaneously: which cash flow, which
discount rate, which growth pattern. Each choice constrains the others; resolving them independently
is what produces models whose numerator and denominator describe different companies.

**Inputs.** S0 classification; S3 cleaned financials and debt ratio; five-year payout and FCFE history.

### S4.1 Claimholder: equity route or firm route

| Use **firm** valuation (FCFF at WACC) when | Use **equity** valuation (dividends/FCFE at ke) when |
|---|---|
| Leverage is too high or too low and is expected to change | Leverage is stable, whether high or low |
| Leverage information is partial (interest expense not broken out, debt schedule unreliable) | Equity — the stock — is explicitly what you are valuing |
| You want firm value (value consulting, whole-business transactions) | The firm is a financial service firm (B3), where FCFF is meaningless |

Decision rule: compute the current market debt ratio, compare with the sector average and with
management's stated target. Close and historically stable → equity route is safe. Far from target,
recapitalizing, levering for an acquisition, deleveraging out of distress → firm route. Note that the
firm route buries leverage in the WACC, where a drifting debt ratio moves the rate only gradually,
which is why it is the robust choice under change.

### S4.2 Equity cash-flow measure: dividends or FCFE

Screen over a **five-year window**, with buybacks added to dividends:
`Dividend coverage = Σ_5 (dividends + buybacks) / Σ_5 FCFE`.

| Coverage | Model | Reading |
|---|---|---|
| < 80% | FCFE | cash is accumulating inside the firm |
| 80%–110% | Dividend discount model | payout ≈ capacity |
| > 110% | FCFE | payout is funded from debt or reserves |

Exceptions that override the screen: financial service firms use dividends (cap ex, depreciation and
working capital have no clean meaning, so FCFE cannot be estimated reliably) unless the
regulatory-capital FCFE route of B3 applies; private companies and IPOs have no dividend history, so
use FCFE.

### S4.3 Growth pattern and stage count

Compare the firm's expected near-term growth `g_firm` with the economy's nominal growth `g_econ`
(proxied by the riskfree rate in the valuation currency):

| Firm characteristics | Model |
|---|---|
| Large and growing at or below `g_econ`; or regulated out of new growth markets; or already showing stable-firm traits (average risk, average reinvestment) | **Stable growth**, 1 stage |
| Large and growing moderately, `g_firm ≤ g_econ + 10%`; or a single product behind a finite-life barrier such as a patent | **Two-stage** |
| Small and growing very fast, `g_firm > g_econ + 10%`; or strong broad barriers to entry; or characteristics far from the norm | **Three-stage / n-stage** |

Overrides on structure, not on the screen: a patent with a known expiry argues two stages even at high
growth; a young firm with broad durable moats argues three. Set the **length** of the high-growth phase
from the strength and durability of the competitive advantage, never from a spreadsheet having ten
columns. Growth alone creates no value — only growth earning above the cost of capital does — so the
high-growth phase is really the period over which competition can be held off. Newly public firms'
excess revenue growth over their industry fades to roughly zero in five to six years; a decade of it
needs an argument. Note the asymmetry in mean reversion: **fade growth faster than you fade excess
returns** (median large-cap ROIC has been sustainable in an 8–12% band over decades, while real revenue
growth reliably decays toward GDP growth).

### S4.4 Inflation basis and currency

- Currency of the cash flows = currency of the discount rate. Non-negotiable.
- Expected inflation **below 10%** → model nominal (taxes are levied on nominal income, so nominal is
  both simpler and more accurate). **At or above 10%** → switch both cash flows and discount rate to
  real terms via Fisher: `(1+nominal) = (1+real)(1+inflation)`.
- Value must be invariant to the currency chosen. If it is not, there is an inconsistency, not an insight.

### S4.5 The resulting model variant

The nine canonical variants, plus the n-stage general form:

| | 1 stage | 2 stage | 3 stage |
|---|---|---|---|
| Dividends | `ddmst` | `ddm2st` | `ddm3st` |
| FCFE | `fcfest` | `fcfe2st` | `fcfe3st` |
| FCFF | `fcffst` | `fcff2st` | `fcff3st` (+ `fcffgen` for n-stage with year-specific inputs and NOL logic) |

**Outputs.** `model_variant` = {cash flow, discount rate, stage count, phase lengths, nominal/real,
currency}; the debt-ratio path (constant, or a convergence schedule to a target).

**Binding rules.** Fixing the cash flow fixes the discount rate (S9), the growth measure (S11), the
terminal-value formula (S12) and the bridge structure (S14). Once fixed, no stage may substitute a
different pairing.

**Invalidating errors.** Discounting FCFF at the cost of equity (overstates equity by roughly the value
of the debt) or FCFE at the cost of capital (understates it). Using the equity route on a firm whose
debt ratio is drifting while holding the cost of equity constant. Subtracting debt after an equity-route
valuation (already netted through the cash flows). Adding a third stage to a mature regulated utility —
that adds parameters, not accuracy.

**Concepts.** `concepts/dcf-model-choice-loose-ends/dcf-model-choice-framework.md`,
`concepts/dcf-model-choice-loose-ends/equity-versus-firm-valuation.md`,
`concepts/dcf-model-choice-loose-ends/dividends-versus-fcfe.md`,
`concepts/dcf-model-choice-loose-ends/growth-pattern-and-stage-count.md`,
`concepts/dcf-model-choice-loose-ends/discount-rate-cash-flow-matching.md`,
`concepts/dcf-model-choice-loose-ends/multistage-model-mechanics.md`,
`concepts/dcf-model-choice-loose-ends/model-choice-case-studies.md`,
`concepts/finance-foundations/equity-vs-firm-valuation.md`,
`concepts/finance-foundations/stable-growth-equity-valuation.md`,
`concepts/deliverables-worked-examples/dcf-model-selection.md`

---

## S5. Riskfree rate

**Purpose.** Fix the base of the discount rate in the valuation currency. Everything in S6–S9 and the
S12 growth cap hangs off this number.

**Inputs.** S4 currency and nominal/real basis; sovereign bond rates; sovereign local-currency ratings;
sovereign CDS spreads; hard-currency sovereign bond spreads.

**Procedure.**
1. **Match currency, horizon and inflation basis.** Convention: the **10-year** default-free government
   bond rate in the cash flows' currency. Do not use a T-bill for a going-concern valuation; do not
   default to the 30-year. Real cash flows → inflation-indexed (TIPS) yield.
2. **Is the issuing government default-free?** Aaa/AAA local-currency rating → use its 10-year rate directly.
3. **Multiple sovereigns issuing in one currency (the Euro case):** take the **minimum** 10-year rate
   across issuers (Germany), never an average and never your home sovereign. Every other issuer's excess
   is sovereign default risk and belongs in the ERP (S6), not in the riskfree rate.
4. **Not default-free:** `Rf = local 10-year government bond rate − sovereign default spread`. Estimate
   the spread by all three routes where data exists and report the range:
   (a) the sovereign's US$/EUR-denominated bond yield less the matching Treasury/German rate;
   (b) the sovereign 10-year CDS spread net of the US CDS spread;
   (c) a rating-table lookup on the **local-currency** rating.
   Pick one route and use it consistently in both S5 and S6.
5. **No trustworthy local bond rate:** choose one of —
   (a) build-up: `Rf = expected inflation + expected real rate`;
   (b) differential inflation: `Rf_C = (1+Rf_US)·(1+π_C)/(1+π_US) − 1`;
   (c) covered interest parity off forward FX;
   (d) switch to real terms (indexed bond yield, or long-run real growth as a proxy);
   (e) switch the whole valuation to US$ or EUR — legitimate, but then *every* input including growth
       and margins must be restated in that currency.
6. **Do not normalize a low or negative rate in isolation.** The intrinsic riskfree rate is
   `expected inflation + expected real GDP growth`; the residual against the market rate is the "Fed
   effect" and has historically been small. If you normalize the rate upward you must normalize
   inflation, real growth and the ERP with it, and you are then valuing a hypothetical economy. Negative
   rates are usable as-is; do not floor them at zero, and check that inflation and growth assumptions in
   that currency are correspondingly near zero or negative.

**Outputs.** `Rf` with currency, date, derivation route, and the sovereign spread used (if any).

**Binding rules.** `Rf` is simultaneously the base of ke and kd, the proxy for `g_econ` in S4.3, and the
cap on terminal growth in S12. Changing it changes all three; they may not be changed independently.

**Invalidating errors.** A US$ riskfree rate with local-currency cash flows. Adding the sovereign spread
instead of subtracting it. Stripping the spread from Rf and *also* leaving country risk in the cash
flows. Using the foreign-currency sovereign rating when the valuation is in local currency. Selective
normalization (raising Rf while leaving g and the ERP untouched) — this biases every valuation downward.

**Concepts.** `concepts/cost-of-equity/riskfree-rate-fundamentals.md`,
`concepts/cost-of-equity/currency-riskfree-rate.md`,
`concepts/cost-of-equity/riskfree-rate-normalization.md`,
`concepts/finance-foundations/fisher-equation-and-intrinsic-riskfree-rate.md`,
`concepts/finance-foundations/currency-consistent-valuation.md`,
`concepts/finance-foundations/real-vs-nominal-conversion.md`,
`concepts/dark-side-difficult/currency-consistency-and-invariance.md`

---

## S6. Equity risk premium

**Purpose.** Price market risk for the markets this company actually operates in.

**Inputs.** S5 Rf; index level and cash yield (dividends + buybacks); sovereign ratings and spreads;
the company's geographic revenue/production breakdown from S1.

**Procedure.**
1. **Mature-market premium.** Default is the **current implied ERP**, solved from the index:
   `Index = Σ_{t=1..5} CF_t/(1+r)^t + CF_5(1+g)/((r−g)(1+r)^5)`, with `CF_0` = trailing-12-month
   dividends **plus buybacks**, `g_high` = top-down consensus index earnings growth, terminal `g = Rf`,
   then `ERP = r − Rf`. Normalize the base cash flow if a crisis year distorted it. Alternatives:
   historical (use the longest window, the geometric average, and the benchmark that matches your Rf's
   maturity) or survey (not recommended: short-horizon and unconstrained).
2. **Choose deliberately, and know the bias you are creating.** If your ERP exceeds the implied ERP, your
   discount rates are too high, your values too low, and everything will look overvalued — an artifact of
   the premium choice, not a market insight. Decision rule: believe premiums revert to historical norms →
   historical; believe the market is right in aggregate or want a market-neutral valuation → current
   implied; believe the market errs but corrects over time → average implied over a long window.
3. **Cross-checks.** `ERP / (Baa spread − T.Bond)` should sit near 2 (historical median ≈ 2.02).
   `Rf + ERP` = expected return on stocks; sanity-check the level.
4. **Country risk premium.** For each non-mature country: take the **local-currency** Moody's sovereign
   rating (convert S&P equivalents; use PRS composite scores where unrated), get a default spread, and
   scale it: `CRP = sovereign default spread × relative equity market volatility`
   (σ emerging-market equity index / σ emerging-market bond index; the production multiplier was 1.10 in
   Jan 2021, 1.18 in Jan 2020, applied uniformly). `ERP_country = mature ERP + CRP`. Aaa → CRP = 0.
5. **Weight by operations, not by passport.** `Company ERP = Σ_i weight_i × ERP_i`. Choose the exposure
   measure by what actually creates the exposure: **revenues** for a consumer business, **production**
   for a natural-resource firm (Shell sells globally and pumps in Nigeria, Iraq and Oman), assets for a
   plant-heavy manufacturer. Use regional ERPs (GDP-weighted) when exposure spans dozens of countries.
   Handle reported aggregations ("Pacific", "Eurasia", "Oceania") explicitly rather than mapping them
   silently.
6. **Choose the attachment mechanism** — and use exactly one:

   | Approach | Formula | When |
   |---|---|---|
   | Constant exposure, location CRP | `Rf + β·ERP_mature + CRP_incorporation` | default banking practice; overstates cost of equity for globalized EM firms |
   | Constant exposure, operation CRP | `Rf + β·ERP_mature + Σ w_i·CRP_i` | the standard fix |
   | Beta exposure, location CRP | `Rf + β·(ERP_mature + CRP_incorporation)` | assumes beta measures country-risk exposure too |
   | Beta exposure, operation CRP | `Rf + β·(ERP_mature + Σ w_i·CRP_i)` | same assumption, operation-weighted |
   | Lambda | `Rf + β·ERP_mature + λ·CRP` | when revenue/production weights are too crude |

   Lambda estimation: revenue-based `λ = firm's domestic revenue share / average local firm's domestic
   revenue share`; or return-based, regressing the firm's stock returns on the country's sovereign bond
   returns (the slope is λ). Adjust judgmentally for hedging (lowers λ) and national-interest
   entanglement (raises λ). The Embraer spread across the five approaches is more than 8 percentage
   points on identical facts, so this choice is material and must be stated.

**Outputs.** Mature ERP with vintage and derivation; per-country CRPs; exposure weights and measure;
company ERP; attachment mechanism; λ if used.

**Binding rules.** ERP vintage must match the Rf date and the default-spread vintage used in S8. Country
risk enters exactly once — through the ERP, or through λ, or through beta, never through two channels.

**Invalidating errors.** Mixing vintages (a 2021 riskfree rate with a 2013 country ERP table). Pairing an
ERP measured over T-Bills with a T-Bond riskfree rate. Stamping the country-of-incorporation CRP on a
company earning 97% of revenues in mature markets. Estimating a local historical premium from twenty
years of emerging-market data (standard error exceeds the estimate).

**Concepts.** `concepts/cost-of-equity/equity-risk-premium-basics.md`,
`concepts/cost-of-equity/implied-equity-risk-premium.md`,
`concepts/cost-of-equity/historical-equity-risk-premium.md`,
`concepts/cost-of-equity/choosing-an-equity-risk-premium.md`,
`concepts/cost-of-equity/country-risk-premium.md`,
`concepts/cost-of-equity/operation-weighted-erp.md`,
`concepts/cost-of-equity/lambda-country-risk-exposure.md`,
`concepts/dark-side-difficult/country-risk-exposure.md`

---

## S7. Relative risk: beta

**Purpose.** Measure how much of the market's risk this business carries, at this leverage, for this
investor.

**Inputs.** S0 marginal-investor verdict; S1 business mix and segment revenues; S3 market debt ratio and
marginal tax rate; comparable-firm data (betas, D/E, tax rates, cash/firm value, R²); industry EV/Sales.

**Procedure.**
1. **Confirm the risk measure applies.** Two questions decide the family: is the marginal investor
   diversified, and do you trust price-based measures?

   | | Price-based | Not price-based |
   |---|---|---|
   | Diversified | CAPM / APM / multi-factor | accounting betas, cost-of-debt-based models |
   | Not diversified | relative volatility, proxy models, CAPM Plus, implied cost of capital | relative earnings volatility, accounting-ratio risk scores |

2. **Build the beta bottom-up.** This is the production method; a regression beta is a diagnostic only.
   - Identify the businesses the firm is in (by economics, not by the filer's segment labels).
   - For each, take the **median** (not mean — comparable sets routinely contain 500%+ D/E outliers)
     levered beta of publicly traded comparables and unlever at the sample's median D/E and tax rate:
     `β_u = β_L / (1 + (1−t)·D/E)`.
   - Cash-correct to a pure business beta: `β_business = β_u / (1 − median cash/firm value)`.
   - Value-weight across businesses: `business value = segment revenues × peer EV/Sales`.
   - Relever at the firm's own **market** D/E (debt including capitalized leases):
     `β_L = β_u × (1 + (1−t)·D/E)`.
   - `Std error of bottom-up beta = average comparable SE / sqrt(n)` — typically an order of magnitude
     tighter than any single regression.
   - Business risk travels across borders: US and European aerospace comparables are valid for a
     Brazilian aerospace firm, because beta measures exposure to the *business's* macro risk and country
     risk lives in the premium.
3. **Run the regression beta as a diagnostic only,** and record its failure modes: a high standard error
   (most US betas sit between 0.20 and 0.40); a low R²; index domination (Nokia at 94% R² was regressed
   against an index it constituted 70% of); regime change inside the window; and index shopping
   (Bombardier's beta moved 0.5 across two listings in the same period). Remember it is levered at the
   *average* D/E over the window, not today's. Extract Jensen's alpha as its second output:
   `α = intercept − Rf_period(1 − β)`, using the **average** riskfree rate over the regression window
   converted to the return interval — not today's rate, and not zero as the benchmark.
4. **Sanity-check against the business determinants.** Product discretionary-ness, operating leverage
   (`EBIT variability = avg %Δ EBIT / avg %Δ revenues`), financial leverage. A defensive staples firm
   with a beta of 2 is not plausible; a gold miner near zero is. Note the convexity of the leverage
   effect: the last 10 points of debt ratio add more beta than the first 50.
5. **Adjust for the investor.** Undiversified owner → `total beta = β_market / correlation = β_market /
   sqrt(R²)`, using the comparables' **median R²** (the firm has no R² of its own). Typical sector
   correlation ≈ 0.5, so total betas run near twice market betas. Use the market beta when the buyer is a
   diversified acquirer; the gap between the two values *is* the diversification benefit and is the
   negotiating range.
6. **Non-traded assets** (private firms, divisions, IPOs): same comparable route, but with no market D/E
   of its own assume the **industry median market D/E** to relever. Accounting betas are a last resort
   (annual data gives four or five observations per decade).
7. **Divisional betas** where divisions differ in business risk. Allocate firm debt across divisions on
   a stated key (identifiable assets is the worked default), derive each division's D/E from allocated
   debt and estimated business value, relever each unlevered beta at its own D/E.
8. **Beta path.** If the debt ratio or business mix changes over the forecast, the levered beta changes
   year by year. In the stable phase drive it toward 1.00 (empirical stable range 0.8–1.2).

**Outputs.** Unlevered business beta(s), value weights, levered beta (and its path), total beta if
required, divisional betas, standard error, regression diagnostics, Jensen's alpha.

**Binding rules.** The D/E used to relever must be the same D/E implied by the S9 cost-of-capital
weights. Gross-debt levering requires gross-debt weights; net-debt levering requires net-debt weights.
Never unlever bank betas — use median levered comparable betas directly (B3).

**Invalidating errors.** Unlevering a regression beta at today's D/E instead of the window average.
Using the mean comparable beta with an extreme-D/E outlier in the sample. Applying a total beta when the
buyer is diversified. Stacking a small-cap premium on a bottom-up beta already built from small-cap
comparables. Using the company-wide beta as the hurdle for every division.

**Concepts.** `concepts/cost-of-equity/capm-cost-of-equity.md`,
`concepts/cost-of-equity/bottom-up-beta.md`,
`concepts/cost-of-equity/levering-and-unlevering-beta.md`,
`concepts/cost-of-equity/regression-beta.md`,
`concepts/cost-of-equity/beta-determinants.md`,
`concepts/cost-of-equity/total-beta.md`,
`concepts/cost-of-equity/non-traded-asset-betas.md`,
`concepts/cost-of-equity/alternative-relative-risk-measures.md`,
`concepts/cost-of-equity/jensen-alpha.md`,
`concepts/finance-foundations/marginal-investor-and-beta.md`,
`concepts/asset-based-private/total-beta.md`

---

## S8. Cost of debt

**Purpose.** Get today's long-term borrowing rate for this firm, in the valuation currency, and its
after-tax equivalent.

**Inputs.** S3 adjusted EBIT and adjusted interest expense (lease-inclusive); S5 Rf; S3 tax rate;
ratings; traded bond data; current default-spread table with a vintage.

**Procedure.**
1. **Define what counts as debt** — the three-part test, all three required: a commitment to fixed
   future payments; those payments tax deductible; non-payment triggers default or loss of control. In:
   all interest-bearing liabilities short and long term, all leases (operating and capital), the
   straight-debt half of any convertible. Out: accounts payable, supplier credit, accruals, deferred
   taxes, minority interest. Pension underfunding and contingent liabilities are **not** debt for the
   cost of capital — they are subtracted once in the S14 bridge. Counting payables as debt to "be
   conservative" inflates the debt weight and *lowers* the WACC — the opposite of conservative.
2. **Walk the estimation-route decision tree:**

   | Situation | Route |
   |---|---|
   | Liquid long-term **straight** bond outstanding | its yield to maturity |
   | Rated, no liquid bond | **median** rating → current spread table → `Rf + spread` |
   | Unrated, recent long-term bank loan | that loan's rate (recency matters) |
   | Unrated, no recent loan; private firm; division | **synthetic rating** from interest coverage |
   | Financial service firm | actual rating; do not synthesize from ordinary coverage |
   | Local-agency rating (company risk only, e.g. CRISIL) | `Rf + sovereign spread + company spread` |

   Never use the accounting cost of debt (`interest expense / book debt`) — it reflects old borrowings at
   old rates and an old credit view. Never use a bond with embedded options.
3. **Interest coverage ratio** (the synthetic-rating input): `ICR = EBIT / interest expense`, both
   lease-adjusted: numerator `EBIT + lease expense − lease depreciation`, denominator
   `interest + kd × lease debt`. Normalize EBIT over a cycle if the current year is unrepresentative,
   but keep interest expense at the **current** year (debt service is a stock, not a cycle average). In
   a high-rate market, scale down: `ICR_adj = ICR / (local long rate / US long rate)`. Edge cases: zero
   interest with positive EBIT → top bracket; negative EBIT → bottom bracket.
4. **Synthetic rating lookup.** Classify the firm: large manufacturing (market cap above roughly $5bn),
   smaller/riskier (below, or young/volatile/private — this column demands substantially **higher**
   coverage for the same rating), or financial (long-term interest only, far lower thresholds). Look up
   `lower < ICR ≤ upper` → rating → spread.
5. **Take the spread from a table dated at the valuation date.** Coverage brackets are stable across
   vintages; **spreads are not** (a D rating has carried 12.00%, 17.44% and 20.00% across the vintages
   in the source material; Baa2 spreads went 2.02% → 5.75% between Jan-2008 and Jan-2009). Refresh, and
   match the vintage to the S6 ERP vintage.
6. **Country risk on the debt side.** A **global** agency rating already embeds country risk — add only
   the company spread. A **local-scale** rating does not — add the sovereign spread. Not every firm bears
   the full spread: `kd = Rf + λ_debt × country default spread + company spread`, with λ_debt near 1.0
   for a small domestic firm and below 1.0 for a large global exporter (Embraer used 2/3, calibrated to
   other large Brazilian issuers' traded bond spreads). Distinguish the country **default spread** (bond
   market, used here) from the country **risk premium** (default spread scaled by relative equity
   volatility, used in S6).
7. **Reconcile synthetic against actual.** Use the actual rating when one exists and is credible; use
   the synthetic as a diagnostic. Explain any material gap by one of: unnormalized current earnings;
   sector rating conventions; emerging-market sovereign drag (the most common cause); uncapitalized
   off-balance-sheet obligations; staleness after a large recent change.
8. **Subsidized debt.** Use the **fair** default-risk-based rate in the WACC and value the subsidy
   separately as `(fair rate − subsidized rate) × principal`, after tax, over the loan's remaining life,
   discounted at a rate reflecting the subsidy's certainty. Never let a subsidized rate lower the hurdle
   rate for new projects.
9. **After-tax.** `kd_after-tax = kd × (1 − marginal t)`, using the **same** t as S3. The tax shield lives
   here and only here — never also as an add-back in FCFF.

**Outputs.** Debt definition and classification log; ICR (lease-adjusted, normalized); rating (actual and
synthetic) with the reconciliation note; spread with vintage; pre-tax and after-tax kd; λ_debt if used.

**Invalidating errors.** Reading the large-firm column for a small firm (artificially good rating, too
low a cost of debt). Using a stale spread table. Double-counting country risk by using a global rating
and adding the sovereign spread again. Applying an ordinary coverage table to a bank. Not resolving the
lease/rating circularity (D1). Applying the effective tax rate here and the marginal rate in S3.

**Concepts.** `concepts/cost-of-debt-capital/what-counts-as-debt.md`,
`concepts/cost-of-debt-capital/cost-of-debt-estimation-routes.md`,
`concepts/cost-of-debt-capital/interest-coverage-ratio.md`,
`concepts/cost-of-debt-capital/synthetic-rating.md`,
`concepts/cost-of-debt-capital/synthetic-vs-actual-rating.md`,
`concepts/cost-of-debt-capital/default-spreads-over-time.md`,
`concepts/cost-of-debt-capital/country-risk-in-cost-of-debt.md`,
`concepts/cost-of-debt-capital/after-tax-cost-of-debt.md`,
`concepts/cost-of-debt-capital/operating-leases-as-debt.md`,
`concepts/cost-of-debt-capital/subsidized-debt.md`,
`concepts/dcf-model-choice-loose-ends/defining-debt-for-cost-of-capital.md`,
`concepts/finance-foundations/default-risk-and-default-spreads.md`

---

## S9. Cost of capital assembly

**Purpose.** Combine S5–S8 into the discount rate (or the discount-rate *path*) that matches the S4
cash flow, in the S4 currency, at the right level of risk.

**Inputs.** S5 Rf, S6 ERP, S7 beta, S8 kd and t; market values.

**Procedure — run in this order (the order is not arbitrary; see D1).**
1. Market value of equity = shares × price, plus the equity half of any convertible.
2. Lease capitalization at kd (done in S3) → lease debt, lease-adjusted EBIT and interest.
3. Interest coverage → synthetic rating → spread → kd. (Iterate 2–3 with kd until stable.)
4. **Market value of debt.** Treat total book debt as one coupon bond:
   `MV = interest expense × [1−(1+kd)^(−M)]/kd + book debt/(1+kd)^M`, with `M` = the weighted-average
   maturity from the debt footnote (weight each disclosed tranche by its share of the *disclosed* total,
   but use **full** book debt as the face value). Default `M = 3 years` when no schedule is disclosed.
   Add lease debt and the straight-debt half of any convertible. Market value falls below book when the
   current kd exceeds the embedded average coupon, and above book when it does not.
5. **Convertible split:** `straight debt value = coupon × [1−(1+r)^(−n)]/r + face/(1+r)^n` at the
   **straight-bond rate for that rating** (never the convertible's own below-market coupon);
   `equity portion = market value of the convertible − straight debt value`. Straight half → debt;
   option half → market capitalization.
6. **Preferred stock:** `k_ps = preferred dividend per share / preferred market price`. **No `(1−t)`** —
   preferred dividends are not deductible. If `PS / (D+E+PS) ≥ 5%`, carry it as a third component;
   below 5%, lumping with debt is acceptable (state that you did).
7. `ke = Rf + β × ERP` (with the S6 attachment mechanism). `WACC = ke·E/(D+E+PS) + kd(1−t)·D/(D+E+PS)
   + k_ps·PS/(D+E+PS)`, on **market-value weights**.
8. **Divisional rates** for a multi-business firm (B8). A single company rate lets safe divisions
   subsidize risky ones and tilts capital toward the riskiest business. Disney's divisional costs of
   capital span 5.69%–8.96% around a company 7.81%.
9. **Currency conversion** where the build-up currency differs from the valuation currency:
   `rate_local = (1 + rate_US$) × (1 + π_local)/(1 + π_US$) − 1`, applied to ke, kd or the WACC alike.
   Cross-check by rebuilding directly off the local riskfree rate; a large gap means either inconsistent
   inflation assumptions or an unstripped sovereign spread. Currency does not change risk — a higher
   local-currency rate is inflation, not danger.
10. **Build the rate path,** not just a rate. Standard convention: constant at the initial WACC for years
    1–5, then fade linearly over years 6–10 to the terminal WACC, where
    `terminal WACC = post-year-10 Rf (or Rf) + mature-market ERP`, with the beta going to 1.00, the debt
    ratio going to the mature/industry average, and any country risk premium fading. Discount with the
    **cumulative product** of year-specific rates, `CDF_t = Π_{i=1..t} 1/(1+r_i)` — never a single
    average rate raised to a power.

**Outputs.** `ke`, `kd_after-tax`, `k_ps`, market-value weights, WACC, the per-year rate path, divisional
rates, the currency and vintage of every input.

**Binding rules.**
- **Market values, never book.** Book weights typically assign more weight to debt, which lowers the WACC
  — anti-conservative, the opposite of what their defenders claim. All three arguments for book weights
  (stability, conservatism, consistency with accounting returns) are specious.
- **Gross debt throughout or net debt throughout.** Net-debt levering requires net-debt weights, and a
  net-debt valuation is already net of cash — do not add cash back in S14. Under the gross convention,
  cash is stripped from the unlevered beta separately and added back in the bridge.
- Same D/E in the beta relevering as in the weights.
- Hurdle-rate matching: returns measured to equity → cost of equity; returns measured to the firm → cost
  of capital; at the risk level of the specific business and in the currency of the thing being measured.

**Invalidating errors.** Currency mismatch anywhere in the chain. Applying `(1−t)` to the whole WACC.
Using a single average WACC when the rate path fades. Leaving capitalized leases out of the weights after
including them in debt elsewhere. A terminal WACC that does not exceed terminal growth (the terminal
value explodes or goes negative).

**Concepts.** `concepts/cost-of-debt-capital/cost-of-capital-assembly.md`,
`concepts/cost-of-debt-capital/market-value-of-debt.md`,
`concepts/cost-of-debt-capital/market-value-weights.md`,
`concepts/cost-of-debt-capital/net-debt-vs-gross-debt.md`,
`concepts/cost-of-debt-capital/preferred-stock-cost.md`,
`concepts/cost-of-debt-capital/convertible-debt-decomposition.md`,
`concepts/cost-of-debt-capital/divisional-cost-of-capital.md`,
`concepts/cost-of-debt-capital/currency-conversion-of-discount-rates.md`,
`concepts/cost-of-debt-capital/wacc-calculator-workflow.md`,
`concepts/cost-of-debt-capital/hurdle-rate-choice.md`,
`concepts/cost-of-equity/cost-of-equity-assembly.md`,
`concepts/finance-foundations/cost-of-capital.md`,
`concepts/deliverables-worked-examples/cost-of-capital-buildup-deliverable.md`

---

## S10. Cash flow construction

**Purpose.** Define the cash-flow line the model will forecast, consistent with the S4 claimholder choice
and built on S3's cleaned inputs.

**Inputs.** S3 cleaned financials; S4 model variant; S9 rate path (for the FCFF/FCFE reconciliation).

**Procedure.**

**FCFF route.** Three algebraically identical pathways — use whichever the available data supports, then
cross-check against the others:
- `FCFF = EBIT(1−t) − (cap ex − depreciation) − ΔNCWC`
- `FCFF = EBIT(1−t) − Reinvestment`
- `FCFF = EBIT(1−t) × (1 − reinvestment rate)`, and with fundamental growth, `= EBIT(1−t) × (1 − g/ROC)`
EBIT is the **adjusted** figure from S3; cap ex includes capitalized R&D and normalized acquisitions;
working capital is the non-cash definition. The interest tax shield is deliberately absent — it lives in
the `(1−t)` on kd inside the WACC. Never add interest, interest tax savings, debt issues or debt
repayments to FCFF. The present value of FCFF is the value of **operating assets**, not equity.

**FCFE route.**
- Full: `FCFE = NI − (cap ex − depreciation) − ΔNCWC − (principal repayments − new debt issued) − preferred dividends`
- Stable-leverage shortcut: `FCFE = NI − (1−DR)(cap ex − depreciation) − (1−DR)·ΔNCWC`, where DR is the
  fraction of reinvestment funded with debt (book DR for historical FCFE, market DR for forecasts).
- Equity reinvestment form: `equity reinvestment = net cap ex + ΔNCWC − Δdebt`;
  `FCFE = NI × (1 − equity reinvestment rate)`.
- From the cash-flow statement: `FCFE = CFO − cap ex − cash acquisitions − (debt repaid − debt issued)`,
  cross-checked against `dividends + buybacks − issuances + Δcash`.
- Because FCFE includes interest income from cash, the discount rate must use the **whole-company** beta
  (operating beta value-weighted with a zero-beta cash holding), not the operating-asset beta.
- Leverage raises FCFE roughly linearly but raises beta convexly. More leverage does not automatically
  raise equity value.

**Dividend route.** Expected DPS, with buybacks added when treating them as cash returned. The terminal
payout must come from fundamentals: `payout = 1 − g/ROE`, never carried over from the high-growth phase.

**Reconciliation unit tests** (run whenever both routes are available):
- *FCFF ↔ FCFE:* build the debt schedule as `Debt_t = DR × V_t` where `V_t = V_{t−1}(1+WACC) − FCFF_t`,
  charge interest on **beginning** debt, set new debt issued = the change in the balance, and use the
  **same** total reinvestment in both routes. The equity values then match exactly. A mismatch means the
  debt schedule and the WACC disagree — check, in order: identical reinvestment, debt tied to
  contemporaneous firm value, interest on beginning debt.
- *DDM ↔ FCFE:* they agree only if retained cash earns the cost of equity. Otherwise the DDM falls short
  by the present value of the shortfall: `CB_t = CB_{t−1}(1+r_cash) + (FCFE_t − Div_t)`, with `PV(CB_n)`
  added to the DDM value. Set `r_cash = ke` and the two must be identical — that is the arithmetic check.
  A cash-hoarding firm's low DDM value is trapped cash, not overvaluation.

**Outputs.** The cash-flow definition, the base-year cash flow, the reinvestment definition, the debt
schedule rule (if FCFE), and the reconciliation test result.

**Invalidating errors.** Discounting earnings as though they were potential dividends (earnings contain
non-cash items, and a firm paying out all earnings could never grow). Splitting cap ex into
"discretionary" and "non-discretionary" and subtracting only the latter — once growth is in the forecast,
the reinvestment that produces it is not discretionary. Applying the standard FCFE formula to a bank.
Forgetting preferred dividends. Using cash-inclusive earnings in EBIT and also adding cash back in S14.

**Concepts.** `concepts/dcf-cashflows-growth/fcff.md`,
`concepts/dcf-cashflows-growth/fcfe.md`,
`concepts/dcf-model-choice-loose-ends/fcff-fcfe-reconciliation.md`,
`concepts/dcf-model-choice-loose-ends/ddm-fcfe-reconciliation.md`,
`concepts/accounting-statements/potential-dividends-fcfe.md`,
`concepts/dividend-policy/fcfe-potential-dividends.md`,
`concepts/dividend-policy/dividend-decision-sequence.md`,
`concepts/dcf-cashflows-growth/dcf-case-valuations.md`

---

## S11. Growth

**Purpose.** Produce the growth path — and, inseparably, the reinvestment path that pays for it. There
are two routes, and S0's earnings-status classification chooses between them.

**Inputs.** S2 claim ledger (which claims were graded plausible and therefore enter as growth); S3 ROIC/ROE
and reinvestment rate; S4 stage count and phase lengths; industry data.

### Route A — fundamental growth (positive, stable-margin earnings)

- **Firm level:** `g_EBIT = reinvestment rate × ROC`. With a changing return, add the efficiency term:
  `g = ROC_{t+1} × RIR + (ROC_{t+1} − ROC_t)/ROC_t`, annualized over the n years the improvement takes:
  `[1 + (ROC_{t+n} − ROC_t)/ROC_t]^{1/n} − 1`. The efficiency term is a one-off spread over the
  transition, never a perpetual source, and it cannot be assumed in stable growth.
- **Equity level:** `g_EPS = retention ratio × ROE`, or the non-cash version
  `g_NI = equity reinvestment rate × non-cash ROE` (strip cash and its after-tax interest income from
  both numerator and denominator — a firm parking retained earnings in a money-market account does not
  earn ROE on them). Constraint: `g ≤ ROE`, because retention cannot exceed 100%.
- **Never mix the three matched pairs:**

  | Earnings measure | Reinvestment measure | Return measure |
  |---|---|---|
  | EPS | retention ratio = 1 − payout | ROE = NI / BV equity |
  | Net income from non-cash assets | equity reinvestment rate | non-cash ROE |
  | Operating income | reinvestment rate = (net cap ex + ΔWC)/EBIT(1−t) | ROC = EBIT(1−t)/(BV equity + BV debt − cash) |

- **Decompose the ROE** to see how much growth is manufactured by borrowing:
  `ROE = ROC + (D/E)[ROC − i(1−t)]`. Leverage raises ROE only when `ROC > i(1−t)`, and levered growth
  comes with a higher cost of equity, so the same `g` is worth less.
- **Three sources, ranked.** Historical growth is a starting point only: report both arithmetic and
  geometric averages and the standard deviation, discard the arithmetic average when the series is
  volatile (Motorola's EBIT "grew 42.45%" arithmetically while compounding at 4.31%), and refuse to
  compute growth off a negative or tiny base. Analyst estimates are an input, not an answer: they are
  **EPS** growth (embedding leverage and buybacks) and cannot be dropped into an FCFF model; the
  advantage over a time-series model is small and vanishes at five-year horizons; distrust both very
  tight consensus (herding) and very wide dispersion (noise). Fundamentals govern for long-horizon work.
- **Test whether the growth is worth anything.** Only growth at `ROIC > cost of capital` creates value;
  at `ROIC = cost of capital` growth is exactly value-neutral at any rate; below, faster growth destroys
  more value. Decompose: `value of assets in place (no growth) = EBIT(1−t)/WACC`; `value added by growth
  = model value − that`; `price the market pays for growth = market EV − that`. The ratio of the last two
  is the number to argue about, not the share price.

### Route B — top-down revenue growth (negative earnings, or changing margins)

Mandatory when earnings are negative or margins are expected to change; the fundamental equations break
because no sustainable return exists.

1. **Revenue path.** Size the total addressable market, grow it, estimate attainable market share at
   explicit milestones (year 5, year 10), convert to revenues, and back out the implied CAGR. Set the
   growth lever from an **end-state revenue level**, not from a rate — that forces you to look at
   absolute dollars. Taper the rate as the base grows; do not hold it flat and then cliff it to the
   terminal rate.
2. **Margin path.** Choose a **target margin** anchored on mature firms with the same business model
   (state which peer percentile), not on the firm's current losses. Converge linearly to it by a stated
   year: `Margin_t = Target − (Target − Base)/Y × (Y − t)` for `t ≤ Y`; or geometrically with a speed
   parameter. `EBIT_t = Revenue_t × Margin_t`.
3. **Reinvestment via sales-to-capital.** `Reinvestment_t = (Revenue_t − Revenue_{t−1}) / sales-to-capital`.
   This single ratio bundles net cap ex, acquisitions, capitalized R&D and working capital — so do **not**
   subtract ΔWC again. The ratio may vary by phase (asset-light early then heavier, or the reverse).
   Choose it against the industry average and argue any large deviation: a ratio far above the industry
   quietly assumes growth is nearly free, and the implied marginal ROIC will show it.
4. **Taxes:** carry the NOL, no tax until it burns, then ramp to the target/marginal rate.
5. **Roll invested capital and compute ROIC each year.** The ROIC path is the honesty check on whether
   the story hangs together. Deeply negative early FCFF is the correct output for a money-loser, not an
   error — it is what the equity issuance or cash burn must fund.

**Outputs.** Year-by-year growth (or revenue) path; margin path; reinvestment path; reinvestment rate;
invested-capital roll-forward; ROIC path; the source and argument for each lever.

**Binding rules.** Growth and reinvestment are one decision, not two. Every growth assumption implies a
reinvestment rate and an ROIC; if you have not stated them you have assumed them silently. In a
three-stage model every changing parameter (growth, payout, beta, debt ratio, cost of debt) steps
**linearly** across the transition and lands exactly on its stable value in the final transition year.

**Invalidating errors.** Setting net cap ex independently of growth. Extrapolating a reinvestment rate
above 100% as sustainable. Using ROC computed on end-of-year capital, or on capital excluding the
research and lease assets. Mixing the effective rate into the reinvestment rate and the marginal rate
into the ROC. Applying the efficiency term every year forever. Using an EPS growth rate as an EBIT growth
rate. Anchoring a target margin on a loss-making current margin.

**Concepts.** `concepts/dcf-cashflows-growth/fundamental-growth-operating.md`,
`concepts/dcf-cashflows-growth/fundamental-growth-equity.md`,
`concepts/dcf-cashflows-growth/historical-growth.md`,
`concepts/dcf-cashflows-growth/analyst-growth-estimates.md`,
`concepts/dcf-cashflows-growth/return-on-invested-capital.md`,
`concepts/dcf-cashflows-growth/value-of-growth.md`,
`concepts/dcf-cashflows-growth/top-down-revenue-growth.md`,
`concepts/dcf-model-choice-loose-ends/multistage-model-mechanics.md`,
`concepts/narrative-numbers/narrative-to-value-drivers.md`,
`concepts/dark-side-difficult/sales-to-capital-reinvestment.md`,
`concepts/dark-side-difficult/young-company-valuation.md`

---

## S12. Terminal value and the stable phase

**Purpose.** Close the valuation. This one number typically carries the majority of value (more than 80%
for a growth company is normal, not a defect), and it is where most valuations go wrong — not because
the perpetuity formula is hard, but because its assumptions are rarely made internally consistent.

**Inputs.** S5 Rf; S9 terminal rate; S11 terminal-year cash flow base; S4 stage count.

**Procedure — the four disciplines, all four required.**
1. **Obey the growth cap.** `g ≤ growth rate of the economy`, proxied by the **riskfree rate in the
   valuation currency**. It may be set lower (a mature firm in an economy that also contains high-growth
   firms probably grows below the aggregate). It may be **negative** — with a negative euro riskfree rate,
   Heineken's stable growth was set at −0.5%, which correctly forces a negative reinvestment rate as the
   firm disinvests. Pairing high `g` with a low Rf systematically overvalues; the reverse undervalues.
2. **Do not stretch the high-growth period.** Its length is the period over which the moat holds off
   competition, and strong durable moats are rare.
3. **Make growth earned, not free.** `Stable reinvestment rate = g / ROC` (firm) or
   `stable payout = 1 − g/ROE` (equity). The classic sleight of hand — cap ex merely offsetting
   depreciation with no working-capital needs, alongside positive real growth — is growth for free. Zero
   net reinvestment supports approximately zero real growth at best.
4. **Make every stable-phase input mature.** Beta → 1.00 (empirical band 0.8–1.2). Debt ratio → industry
   or mature-company average. Country risk premium fading. Excess returns approaching zero
   (`ROC → WACC`, `ROE → ke`) unless a moat is explicitly argued. Tax rate → marginal, no NOL shield.
   Cost of capital → mature level.

**Formulas.**
- `TV_N = CF_{N+1} / (r_stable − g)`, with `r` matched to the cash flow.
- Firm form with reinvestment built in: `TV_N = EBIT_{N+1}(1−t)(1 − g/ROC) / (WACC_stable − g)`.
- Discount TV back through the **whole** transition using the cumulative discount factor, not the
  high-growth rate.
- Terminal cap ex must be **back-solved** from the stable reinvestment rule, never grown from year N.

**Reverse consistency check (mandatory).**
`embedded reinvestment rate = 1 − FCFF_terminal/EBIT(1−t)_terminal`; `implied perpetual ROIC = g /
embedded reinvestment rate`; and, for comparison, `reinvestment rate that would make ROIC = WACC = g/WACC`.
If the implied perpetual ROIC exceeds the cost of capital, you are claiming a permanent moat — state it
or set them equal. Never ship a valuation whose implied perpetual ROIC nobody looked at.

**Alternatives, and why they are inferior.** Liquidation value is right only when assets are separable and
marketable (not a going-concern value). An **exit multiple** is easiest and converts your intrinsic
valuation into a relative valuation by importing market pricing — do not then describe the result as
intrinsic.

**Outputs.** Stable-phase parameter set (g, ROC/ROE, reinvestment/payout, beta, debt ratio, tax rate,
cost of capital); terminal cash flow; TV; PV(TV); TV as a share of total value; the implied perpetual ROIC.

**Invalidating errors.** `g > Rf` in the valuation currency. `r_stable ≤ g` (TV explodes or goes negative).
Positive real growth with zero net reinvestment. A high-growth beta, debt ratio or payout left in the
terminal year. Terminal ROC left above the terminal cost of capital by default rather than by argument.
Discounting TV at the high-growth rate.

**Concepts.** `concepts/dcf-cashflows-growth/terminal-value.md`,
`concepts/dcf-cashflows-growth/value-of-growth.md`,
`concepts/dcf-cashflows-growth/return-on-invested-capital.md`,
`concepts/dcf-model-choice-loose-ends/growth-pattern-and-stage-count.md`,
`concepts/project-returns/terminal-value-and-project-life.md`,
`concepts/finance-foundations/present-value-of-the-five-cash-flow-types.md`

---

## S13. Discounting to the value of operating assets

**Purpose.** Turn the cash-flow schedule and the rate path into the value of operating assets (firm route)
or of equity (equity route), with an explicit failure branch where survival is genuinely in doubt.

**Inputs.** S9 rate path; S10 cash-flow schedule; S12 TV; S0 distress classification.

**Procedure.**
1. Build cumulative discount factors: `CDF_t = Π_{i=1..t} 1/(1 + r_i)`. `PV(CF_t) = CF_t × CDF_t`.
   Discount TV with `CDF_N`.
2. `Going-concern value = Σ PV(CF_t) + PV(TV)`.
3. **Failure adjustment** (mandatory under `require-failure-probability`):
   `Value = going-concern value × (1 − p_failure) + distress proceeds × p_failure`.
   - `p_failure` anchors: cumulative default probabilities by rating (10-year: AAA 0.70%, BBB 3.32%,
     BB 11.78%, B 23.74%, CCC/C 50.38%), sector long-run business survival rates (all-sector average
     16.6%; range 11.5% for Information to 35.2% for Management of companies), or a bond-price inversion.
   - Distress proceeds basis: a stated percentage of book capital, or a fraction of going-concern value.
     Declare which.
   - **Do not** apply a failure probability *and* a distress-adjusted discount rate. That double counts.
4. Record the value split: PV of explicit-period cash flows versus PV of terminal value.

**Outputs.** PV table; going-concern value; failure-adjusted value of operating assets (firm route) or of
equity (equity route); TV share of value.

**Invalidating errors.** Discounting with a constant rate when the rate path fades. Treating the FCFF
present value as equity value — the bridge still has to be done. Omitting the failure branch on a young
or distressed firm (a going-concern DCF alone overstates value).

**Concepts.** `concepts/dcf-cashflows-growth/fcff-forecast-engine.md`,
`concepts/dcf-model-choice-loose-ends/multistage-model-mechanics.md`,
`concepts/dark-side-difficult/distress-and-failure-adjusted-value.md`,
`concepts/dark-side-difficult/bond-implied-distress-probability.md`,
`concepts/dark-side-difficult/truncation-and-political-risk.md`

---

## S14. The equity bridge

**Purpose.** Get from operating-asset value to the value of common stock. Most valuation disputes between
competent analysts happen here, not in the cash-flow forecast. The organizing rule for the whole stage:
**every adjustment is made exactly once.**

**Inputs.** S13 operating-asset value; S3 balance-sheet detail and footnotes; S1 option and share schedule;
S9 market value of debt.

**The ladder.**
```
  Value of operating assets            (DCF of FCFF at the cost of capital)
+ Cash and marketable securities
+ Value of cross holdings
+ Value of other non-operating assets
= Value of firm
− Market value of debt                 (not book, for a going concern)
− Other claims (pension/health-care underfunding, contingent liabilities, minority interests)
= Value of equity
− Value of equity options              (employee options, warrants, conversion options)
= Value of common stock
÷ Actual shares outstanding            (not diluted)
= Value per share
```

**Link-by-link rules.**

1. **Cash.** Keep it out of the operating valuation, then add it back. That requires two disciplines: cash
   flows measured **before** interest income from cash, and a beta of the operating assets alone. The
   alternative — folding interest income into the flows and weighting the beta down for cash — only works
   if cash stays a fixed percentage of value forever, which it rarely does. Split out **operating cash**
   (needed for day-to-day liquidity), which belongs inside working capital; only the excess is added here.
   Note that cash inflates blended multiples (cash carries a PE of `1/Rf`), which matters for the S16
   cross-check.
2. **Marginal value of cash.** Face value when `ROIC ≈ cost of capital`; below face when `ROIC < cost of
   capital` (a wasting asset — the discount is for the *risk of poor deployment*, never because cash earns
   a low rate; a riskless asset should earn a riskless return); above face when the firm earns large excess
   returns with a reinvestment runway. Market evidence for $1 of cash: ≈$0.75 at mature value-destroying
   firms, ≈$1.00 across all firms, ≈$1.25 at high-excess-return growth firms. Size a discount from the
   expected shortfall: `discount = annual underperformance / required return`. Do not apply a cash
   discount *and* lower the growth/return assumptions for the same bad management.
3. **Cross holdings.** Three accounting tiers, three different distortions:

   | Stake | In the parent's statements | Bridge treatment |
   |---|---|---|
   | Minority passive (<20%) | dividends only | add the stake's value; the DCF captured almost none of it |
   | Minority active (20–50%) | proportional equity income below operating income | add the stake's value; strip the equity income from operating earnings |
   | Majority (>50%) | full consolidation of 100% | subtract the market value of the minority interest you do not own |

   Preferred method is a three-step sum-of-the-parts: value the unconsolidated parent, value each holding
   on its own, then `parent equity = unconsolidated parent value − unconsolidated parent debt + Σ (% owned
   × holding equity value)`. Using **market** values for listed holdings inside an intrinsic valuation
   imports the market's errors. Fallback approximation: convert book minority interest and book holdings
   to market with the subsidiary's sector price-to-book. Net out taxes due on unrealized gains where a sale
   or repatriation is contemplated (Yahoo's tax line was $5,017m, over 10% of equity value).
4. **Other non-operating assets — one test.** Add an asset only if its cash flows are **not already in the
   forecast**. In: overfunded pension surplus (haircut for bargaining constraints and withdrawal taxes, and
   for the probability you can actually claim it); genuinely unutilized assets (vacant land, idle plant,
   non-core real estate) at estimated market value. Out: headquarters real estate, PP&E, brand names,
   customer lists — all already in the margins and growth. **Never** goodwill; it is an accounting residual,
   not an asset.
5. **Complexity/opacity adjustment** (optional, firm level). Score the firm (weighted scorecard, or at
   minimum 10-K page count against sector peers). If you adjust, pick exactly **one** channel — lower cash
   flows, higher discount rate, lower growth, shorter growth period, or a final percentage haircut. Never
   stack them. Prefer fixing the underlying modelling problem (do the cross-holding work, capitalize the
   leases, read the segments) over applying a blanket discount. Market cross-check: the PBV regression
   prices roughly 0.003 of price-to-book per 10-K page.
6. **Debt.** Market value for a going concern; **face** value in a liquidation frame (creditors are owed
   face). A distressed telecom with $1bn of enterprise value and $1bn face of debt trading at 50 gives
   $500m of equity as a going concern and $200m in a $1.2bn liquidation — same firm, same debt, $300m apart
   on a frame judgment.
7. **Other claims.** Pension and health-care underfunding at the amount of the underfunding, subtracted
   **once, here** — never also as debt in the WACC, and never also as a cash-flow line for funding
   contributions. Contingent liabilities at `probability × expected size`, not the plaintiff's headline
   number. Minority interests at estimated market value; book is usually far too low for a profitable
   subsidiary.
8. **Equity options — use the option-value-drag method.** Three approaches circulate; two are wrong in
   predictable directions:

   | Approach | Bias |
   |---|---|
   | Diluted share count | too low — ignores exercise proceeds |
   | Treasury stock | too high — ignores the time premium; and mishandles out-of-the-money options |
   | **Option value drag: `(equity value − option value) / actual shares`** | consistent; brackets the other two |

   Value the options with a **dilution-adjusted** Black-Scholes: `S_adj = (S·N_shares + C·N_options)/(N_shares
   + N_options)`, solved with `C` as a fixed point (see D2); `C = S_adj e^{−yT}N(d1) − K e^{−rT}N(d2)`.
   Shorten `T` from contractual to expected life for early exercise. Multiply by the probability of vesting
   if a material share is unvested. Tax-adjust only if exercise creates a deduction. Include warrants and
   the conversion option inside convertibles — they are claims on the same equity.
9. **Restricted stock and future grants — different destinations.** Restricted stock **already granted**
   goes into the share count (denominator). Grants **expected in future** are compensation and go into the
   forecast as an operating expense, as a percent of revenues declining as the firm scales. Never both for
   the same grant. Stock-based compensation is a real cost — it is not a free add-back.
10. **Divide by actual shares.** If you subtracted option value, using diluted shares double counts.
11. **Per-share discounts last,** and only when the buyer's position justifies them: illiquidity (B5),
    minority-stake discount, control premium. Check they do not overlap with a total-beta discount rate
    already applied.

**Outputs.** Each bridge line item with its basis; value of equity; value of common stock; value per share.

**Invalidating errors.** Subtracting book debt from a market-based enterprise value. Forgetting minority
interests after a consolidated DCF (credits shareholders with a subsidiary they only partly own). Adding
brand value on top of brand-driven margins. Adding goodwill. Subtracting option value **and** dividing by
diluted shares. Counting pension underfunding twice. Leaving interest income in the cash flows and adding
cash back.

**Concepts.** `concepts/dcf-model-choice-loose-ends/equity-value-bridge.md`,
`concepts/dcf-model-choice-loose-ends/cash-in-valuation.md`,
`concepts/dcf-model-choice-loose-ends/marginal-value-of-cash.md`,
`concepts/dcf-model-choice-loose-ends/cross-holdings.md`,
`concepts/dcf-model-choice-loose-ends/other-non-operating-assets.md`,
`concepts/dcf-model-choice-loose-ends/complexity-discount.md`,
`concepts/dcf-model-choice-loose-ends/debt-and-other-claims-in-the-bridge.md`,
`concepts/dcf-model-choice-loose-ends/employee-option-per-share-approaches.md`,
`concepts/dcf-model-choice-loose-ends/valuing-employee-options.md`,
`concepts/dcf-model-choice-loose-ends/restricted-stock-and-future-grants.md`,
`concepts/dark-side-difficult/dilution-and-employee-options.md`,
`concepts/dark-side-difficult/cross-holdings.md`,
`concepts/accounting-statements/non-operating-items-and-cross-holdings.md`,
`concepts/finance-foundations/black-scholes-and-put-call-parity.md`

---

## S15. Value per share, the gap, and the expected return

**Purpose.** Convert the value estimate into a statement about an investment, or state honestly that it
cannot be.

**Inputs.** S14 value per share; market price; S9 ke.

**Procedure.**
1. `Gap = value per share − price`; report also `price as % of value`. Flag thresholds: value below 50% of
   price, or above 200% of price, is a prompt to re-examine inputs — not proof of mispricing.
2. **Ask the three questions in order:** is there a gap? will it close? if so, what closes it? Name the
   mechanism — news arrival, an earnings report, an activist, an acquirer, an index event. A DCF that skips
   the third question is an academic exercise; a gap without a closing mechanism and a horizon is an opinion,
   not a trade.
3. **Convert to an expected return** if the market corrects: roll value forward at ke,
   `expected price_1 = value × (1 + ke) − expected dividend_1` (or `value × (1+g)` in the stable-growth
   form), then `expected 1-year return = (expected price_1 + dividend_1 − price)/price`.
4. **Compute the breakeven (implied) input.** Solve for the growth rate — or the margin, or the market share
   — that sets model value equal to the market price. In the stable-growth DDM the closed form is
   `g = (ke·P − DPS_0)/(P + DPS_0)`. That number is what the market is assuming, not a forecast. Then ask
   whether that assumption is **probable**, not merely possible — some scenario always justifies any price.
5. Apply per-share discounts from S14 step 11 if the buyer's position calls for them.
6. **Cross-check against pricing, and explain the gap rather than averaging it away.** Run at least one
   relative-valuation comparison (peer multiple with its companion variable, or a sector regression).
   Never average a DCF value and a multiple-based price into one number.

**Outputs.** Value per share; price; gap and ratio; expected return; breakeven input; the named catalyst;
the relative cross-check and the explanation of the difference.

**Invalidating errors.** Reverse-engineering value from price and calling it independent. Reading a large
gap as proof the market is wrong before checking your own inputs. Presenting a point estimate to the cent.
Treating value as static — intrinsic value moves too (3M's moved from $83.55 to $60.53 in five weeks in
2008 because cash flows, growth and rates all changed at once).

**Concepts.** `concepts/narrative-numbers/value-vs-price-gap.md`,
`concepts/dark-side-difficult/value-versus-price.md`,
`concepts/dcf-model-choice-loose-ends/model-choice-case-studies.md`,
`concepts/relative-valuation/pricing-vs-value.md`,
`concepts/relative-valuation/comparable-selection-and-controls.md`,
`concepts/deliverables-worked-examples/valuation-triangulation-and-recommendation.md`

---

## S16. Uncertainty: sensitivity, scenarios, simulation

**Purpose.** Convert a point estimate into a range, and locate the market price inside it. The tool depends
on the *kind* of doubt.

**Inputs.** The completed base-case model; S2 claim ledger; S0 life-cycle stage.

**Procedure.**
1. **Two-way sensitivity grid.** Pick the two inputs that move value most (usually growth and target
   margin) and tabulate value across a plausible range. This produces the Lo/Base/Hi triple. Apply a
   plausibility filter that rules cells out — a grid with impossible cells in it is not analysis.
2. **Scenario grid — when the doubt is about *which story*.** Choose two to four story dimensions (total
   market definition, market-growth effect, network effects, competitive advantage, take rate, target
   margin), define discrete **named** levels in story language, hold everything else fixed including the
   model structure, run every combination, sort by value and inspect the extremes. Report the spread
   (Uber's twelve-cell grid ran $799M to $90,457M — a 113x spread driven entirely by narrative choices).
   **Label every row possible / plausible / probable**; a range without likelihood labels is a wish list.
   State your chosen cell and the evidence for it — a range with no chosen cell is an abdication.
3. **Monte Carlo — when the doubt is about *how much*.** Distribute the three or four inputs that both
   matter and are genuinely uncertain (not everything — that manufactures a wide range with no information).
   Choose a shape per input and justify it: lognormal for a growth rate with a long right tail; triangular
   when you can state min/likeliest/max; uniform when you have a range and no view inside it;
   minimum-extreme when downside surprises dominate. **Set the correlations** — getting the sign right
   matters more than the exact number. Read median, 10th and 90th percentiles, and the share of trials at or
   below zero. Treat the 0th and 100th percentiles as tail artifacts, not a range. The simulation median is
   **not** the base case (Paytm's median sat 17% below its base-case DCF).
4. **Locate the price in the distribution.** Near the median → the market is inside your uncertainty band
   and you have no edge. Beyond the 90th percentile → you have a case.
5. **Match the tool to the life-cycle stage.** Company-specific and binary ("does the idea work at all")
   → failure probability and option value. Macro and continuous ("how big does this get") → scenarios and
   simulation.
6. **Do not double-count risk.** The discount rate already carries risk. Simulation is about the range of
   outcomes, not an extra risk premium. Likewise, do not simulate a narrative *break* — a binary end-of-story
   event needs a probability and a consequence, not a distribution over a continuing model.

**Outputs.** Sensitivity grid; scenario grid with likelihood labels and a designated base cell; simulation
percentiles with distributions and correlations documented; the price's location in the distribution.

**Concepts.** `concepts/narrative-numbers/narrative-scenario-grids.md`,
`concepts/narrative-numbers/monte-carlo-valuation-simulation.md`,
`concepts/narrative-numbers/life-cycle-uncertainty.md`,
`concepts/dark-side-difficult/scenario-analysis-and-simulation.md`,
`concepts/deliverables-worked-examples/dcf-sensitivity-analysis.md`,
`concepts/project-returns/uncertainty-payback-sensitivity-simulation.md`

---

## S17. VALIDATION GATE

**Purpose.** The battery that must pass before a value is reported. Every check here is mechanical on the
finished model plus at most one external number. This is the cheapest quality control in valuation, and it
runs *after* the model is built, on the model's own outputs.

Fail behaviour: **fix the offending input, not the output.** Then re-run from the stage that owns it.

### 17.1 The impossible screens (never allow)

| Check | Test | External input |
|---|---|---|
| Bigger than the economy | terminal `g ≤ Rf` in the valuation currency | Rf |
| Bigger than the market | year-N implied revenues / total market size `≤ 100%` | market-size estimate |
| Margin above 100% | max operating margin over the forecast `< 100%` | — |
| Depreciation without cap ex | terminal depreciation `≤` terminal cap ex | — |
| Terminal denominator | `r_stable > g_stable` strictly | — |
| Terminal reinvestment | `RIR_terminal = g/ROC` exactly (or `payout = 1 − g/ROE`) | — |

### 17.2 The implausible screens (require extraordinary justification)

Growth forever with zero reinvestment. Rising margins and share with no competitive response modelled.
High returns assumed in a business with no risk.

### 17.3 The improbable screens (the growth/risk/reinvestment triangle)

- `Marginal ROIC = Δ EBIT(1−t) over the forecast / Δ invested capital over the forecast`. If it exceeds
  what the best firms in the business earn, either reinvestment is too low or margins are too high.
- Terminal excess return: `ROC_terminal − WACC_terminal`. Positive means a perpetual moat is being claimed.
  State the moat or set them equal.
- High growth with a mature-company cost of capital; heavy reinvestment with a mature-company risk profile.
- Absolute revenues in year N, in dollars, with the question: who loses that revenue?

### 17.4 The consistency invariants (Section C, mechanically)

Each of C1–C8 below is a pass/fail check. Any failure blocks the report.

### 17.5 The double-count register (Section F, mechanically)

Each of F1–F10 below is a pass/fail check.

### 17.6 The reconciliation unit tests

- FCFF and FCFE routes agree exactly under constant market-value leverage (S10).
- DDM and FCFE agree exactly when retained cash earns ke (S10).
- Reverse ROIC check: the implied perpetual ROIC is stated and defended (S12).
- Net income unchanged by lease capitalization; FCFF unchanged by R&D capitalization (S3).
- Six accounting reconciliation ties (S3.1).

### 17.7 Diagnostics to read before shipping

Marginal ROIC; ending ROIC versus sector ROIC; average compounded WACC; TV share of value; value as a
percent of price (flag <50% or >200%); the count of model inputs with no story sentence and story claims
with no driver (both should be zero).

**Concepts.** `concepts/narrative-numbers/narrative-consistency-checks.md`,
`concepts/dcf-cashflows-growth/return-on-invested-capital.md`,
`concepts/dcf-cashflows-growth/fcff-forecast-engine.md`,
`concepts/dcf-model-choice-loose-ends/fcff-fcfe-reconciliation.md`,
`concepts/dcf-model-choice-loose-ends/ddm-fcfe-reconciliation.md`,
`concepts/narrative-numbers/narrative-numbers-bridge.md`

---

## S18. The feedback loop

**Purpose.** Keep the valuation a working hypothesis rather than a position. Two habits: value the
counter-narratives, and revise as events unfold.

**Procedure.**
1. **Solicit counter-narratives explicitly.** Ask what would have to be true for a much higher value, and
   for a much lower one. Then **value** the alternative story with the same model, changing only the drivers
   that story changes. Knowing what someone else's story is worth is more useful than knowing you disagree —
   it locates the disagreement in specific drivers (Damodaran's $5.9bn versus Gurley's $53.4bn on Uber lived
   entirely in market size, share and slice).
2. **When news arrives, classify it.** That diagnosis is the only one that matters:

   | Change | What happened | Response | Tool |
   |---|---|---|---|
   | **Break** | external (legal, political, economic) or internal (management, competitive, default) events end the story | existing estimates of cash flows, risk, growth and value stop being operative | probability of the break × consequences |
   | **Shift** | the business model improves or deteriorates — market size, share and/or profitability move | modify the driver estimates and re-run | Monte Carlo or scenario analysis (S16) |
   | **Change** | unexpected entry into or exit from a market | redo the valuation on new market potential | real options (B9) |

3. **Re-grade the claim ledger.** Promotion (possible → plausible → probable) or demotion changes which
   device applies, and therefore the value. Watch the promotion triggers written down at S2.
4. **Revise on business news, not on price moves.** Price moving against you is not information about the
   business; revising because it did is herding with extra steps.
5. **Run the unbiasedness test over time.** Count revisions in both directions; they should be roughly
   symmetric. A one-sided revision record is evidence of a biased process, not bad luck. Expect to be wrong;
   value estimates move as information arrives, and that is what risk means.
6. **Re-enter the pipeline at the owning stage**, not at the top. A margin re-estimate re-runs S11 → S17. A
   rating change re-runs S8 → S17. A currency or classification change re-runs everything from S4.

**Concepts.** `concepts/narrative-numbers/narrative-updating-feedback-loop.md`,
`concepts/narrative-numbers/story-to-numbers-process.md`,
`concepts/narrative-numbers/valuation-misconceptions.md`,
`concepts/narrative-numbers/uber-narrative-valuation.md`,
`concepts/narrative-numbers/tesla-motley-fool-valuation.md`

---

# Branches

Branches are overlays selected at S0 (and confirmed at S4). Each names the stages it modifies. Multiple
branches can be active at once (an emerging-market money-losing private firm runs B2 + B4 + B5).

## B1. Model-variant matrix (always active)

Not an overlay but the resolution of S4. The variant is the tuple
`{dividends | FCFE | FCFF} × {1 | 2 | 3 | n stages} × {nominal | real} × currency`, with the discount rate
and terminal formula determined by the first element. Canonical worked instances to pattern-match against:

| Subject | Variant | Why that cash flow | Why that growth pattern |
|---|---|---|---|
| Regulated utility (Con Ed) | stable DDM | payout ≈ 97% of FCFE; leverage stable near 70/30 for decades | regulated, service area grows ~2% |
| Large industrial (3M) | two-stage FCFF | firm level, modest stable leverage | moderate growth then stable |
| Mature firm with a moat (Disney) | three-stage FCFF | debt ratio expected to change | strong competitive advantages → 10-year growth period |
| Normalized commodity cyclical (Vale) | single-stage FCFF | debt ratio changing | already mature after normalization → **no** high-growth period |
| Emerging-market firm in local currency (Tata Motors) | two-stage FCFE | stable debt ratio | growth mostly from outside the home market → 5 years |
| Changing-margin high-growth firm (Baidu) | FCFF with a declining margin path | firm level | strong excess returns → 10 years |
| Bank (Deutsche Bank) | DDM, or regulatory-capital FCFE | FCFF meaningless; FCFE unestimable by the standard formula | — |
| Equity index (S&P 500) | two-stage DDM with buybacks | dividends + buybacks are the tangible index cash flow | near-term analyst growth above stable |

`concepts/dcf-cashflows-growth/dcf-case-valuations.md`,
`concepts/dcf-model-choice-loose-ends/model-choice-case-studies.md`

## B2. Negative or abnormal earnings — the revenue route

**Trigger:** negative operating income, or margins expected to change materially.

| Stage | What changes |
|---|---|
| S3 | Diagnose the cause first. Do **not** normalize when the cause is structural, life-cycle or leverage. |
| S11 | Route B is mandatory. Fundamental growth equations do not apply. |
| S12 | Argue the terminal ROC explicitly. The ROIC path ends far from where it started. |
| S13 | A failure probability is mandatory. |

Method: work backwards from a mature end-state. Build the revenue path from market size times share. Anchor
the target margin on mature firms with the same business model. Drive reinvestment from a sales-to-capital
ratio. Carry the NOL. Fade the cost of capital as the firm matures. Attach a probability of failure. Deeply
negative early FCFF is the correct output, not an error.
`concepts/dcf-cashflows-growth/top-down-revenue-growth.md`,
`concepts/dcf-cashflows-growth/normalizing-depressed-earnings.md`,
`concepts/dark-side-difficult/young-company-valuation.md`,
`concepts/dark-side-difficult/sales-to-capital-reinvestment.md`,
`concepts/dark-side-difficult/declining-firm-valuation.md`

## B3. Financial service firms

**Trigger:** bank, insurer, brokerage.

| Stage | What changes |
|---|---|
| S3 | Revenue is net interest income plus net fee income. Credit-loss provisions are a **recurring** operating expense, never extraordinary. |
| S4 | Constraint `no-fcff-valuation`. Value equity directly: dividends, regulatory-capital FCFE, or an equity excess-return model. |
| S7 | Do **not** unlever or relever. Use median levered comparable betas, weighted by net revenues. |
| S8 | No synthetic rating from ordinary coverage. Use the actual rating, or long-term-interest-only coverage. |
| S10 | Reinvestment is the build-up of regulatory capital. `Investment in regulatory capital_t = Tier1_t − Tier1_{t−1}`; `NI_t = book equity_t × expected ROE_t`; `FCFE_t = NI_t − investment in regulatory capital_t`. |
| S12 | Stable ROE converges to ke. Payout `= 1 − g/ROE`. |

Never apply a debt-to-capital ratio, EBITDA or enterprise value to a bank. Debt is raw material, not
financing, and thin equity-to-assets is structural rather than a warning.
`concepts/dark-side-difficult/financial-service-firm-valuation.md`,
`concepts/dark-side-difficult/bank-fcfe-and-excess-return-models.md`,
`concepts/dividend-policy/fcfe-for-banks.md`,
`concepts/accounting-statements/sector-differences-in-financial-statements.md`,
`concepts/capital-structure/financial-firm-capital-structure.md`

## B4. Emerging market / multi-currency

**Trigger:** material operations, production or incorporation outside mature markets. Or a valuation currency
with no default-free issuer.

| Stage | What changes |
|---|---|
| S5 | Strip the sovereign default spread out of the local bond rate, or build the rate up from inflation. |
| S6 | Add a country risk premium, weighted by operations. Declare the attachment mechanism, and λ if used. |
| S8 | Decide whether the rating is global (country risk already inside) or local (add the sovereign spread). Set λ_debt. |
| S9 | Convert rates by differential inflation. Cross-check by rebuilding directly off the local riskfree rate. |
| S12 | Fade the country risk premium in the stable phase. Cap terminal `g` at the **local-currency** riskfree rate. |
| S13 | Add truncation risk where nationalization or regime change is live, as a probability-weighted scenario. |
| S14 | Value cross-holdings explicitly. At a group company they are often half the total. |

Invariance test: value the same business in two currencies. The answers must agree.
`concepts/dark-side-difficult/country-risk-exposure.md`,
`concepts/dark-side-difficult/currency-consistency-and-invariance.md`,
`concepts/dark-side-difficult/truncation-and-political-risk.md`,
`concepts/cost-of-equity/operation-weighted-erp.md`,
`concepts/cost-of-debt-capital/currency-conversion-of-discount-rates.md`,
`concepts/finance-foundations/currency-consistent-valuation.md`,
`concepts/finance-foundations/exchange-rate-forecasting-with-parity.md`

## B5. Private company, division, or IPO

**Trigger:** no traded equity, or a non-diversified buyer.

| Stage | What changes |
|---|---|
| S3 | Charge a market salary for owner labour. Remove personal expenses. Capitalize leases. Treat a short history with caution. |
| S7 | Build the beta from comparables using **median** statistics. Relever at the industry median **market** D/E. Use a total beta if the marginal investor is undiversified. |
| S8 | Synthetic rating, with leases counted as interest in the coverage ratio. |
| S9 | Industry median D/E supplies the weights. |
| S14 | Apply the key-person discount to **operating income**, not to value. |
| S15 | Size the illiquidity discount from restricted-stock or bid-ask-spread evidence. A flat 20–30% is wrong. Add a minority discount for a below-50% stake. |

The transaction scenario decides the rate and the discounts. Private-to-private uses a total beta and an
illiquidity discount. Private-to-public sale and IPO use the market beta and drop the illiquidity discount,
which can multiply the value. The gap between the two is the bargaining range. An IPO adds three further
adjustments: use of proceeds, prior equity claims, and the share and option count.
`concepts/asset-based-private/private-company-valuation-framework.md`,
`concepts/asset-based-private/private-company-statement-cleanup.md`,
`concepts/asset-based-private/private-company-cost-of-capital.md`,
`concepts/asset-based-private/total-beta.md`,
`concepts/asset-based-private/key-person-discount.md`,
`concepts/asset-based-private/illiquidity-discount.md`,
`concepts/asset-based-private/minority-discount.md`,
`concepts/asset-based-private/private-to-private-valuation.md`,
`concepts/asset-based-private/ipo-valuation.md`,
`concepts/cost-of-equity/non-traded-asset-betas.md`

## B6. Distress

**Trigger:** distress markers at S0 (coverage below 1, negative equity from losses, bonds at deep discounts,
going-concern qualification).

| Stage | What changes |
|---|---|
| S13 | Blend going-concern and distress values by probability. Set distress proceeds as a percent of book or fair value. |
| S14 | Decide the frame. A going concern subtracts the market value of debt; a liquidation subtracts face value. |
| S15 | Consider valuing equity as a **call option** on firm value. Strike = face value of debt; life = weighted debt duration; variance from stock and bond volatilities. This is why bankrupt firms' stock trades above zero. |

Probability sources: invert a traded bond price for the annual and cumulative distress probability; or use
rating-based cumulative default tables; or use sector survival rates.
`concepts/dark-side-difficult/distress-and-failure-adjusted-value.md`,
`concepts/dark-side-difficult/bond-implied-distress-probability.md`,
`concepts/real-options/equity-as-call-option.md`,
`concepts/real-options/distressed-equity-time-value.md`,
`concepts/real-options/equity-option-inputs-troubled-firms.md`,
`concepts/deliverables-worked-examples/equity-as-call-option-valuation.md`

## B7. Cyclical and commodity firms

**Trigger:** earnings driven by a commodity price or the macro cycle. Classification says trough or peak.

| Stage | What changes |
|---|---|
| S3 | Normalize. Average dollar earnings over a full cycle if size is stable; apply an average return to current capital if size has changed. Normalize the tax rate over the same window. Be consistent about which numbers are normalized and which are current. |
| S4 | A normalized mature firm may deserve **no** high-growth period at all. |
| S8 | Use normalized EBIT in the coverage ratio. |
| S11 | Compute growth off the normalized base and the normalized return. |
| S16 | The commodity price is the natural scenario dimension. |

Where a usable price driver exists, separate macro from micro instead: value at today's commodity price,
regress revenues on the price, and normalize margins and ROC. Routine divestitures at commodity firms are
not extraordinary.
`concepts/dark-side-difficult/commodity-and-cyclical-valuation.md`,
`concepts/dark-side-difficult/normalized-earnings.md`,
`concepts/dcf-cashflows-growth/normalizing-depressed-earnings.md`

## B8. Multi-business firms

**Trigger:** more than one business with materially different risk. Or segment data showing divergent margins
and returns.

| Stage | What changes |
|---|---|
| S7 | Value-weight the unlevered betas across businesses. Weights come from `segment revenues × peer EV/Sales`. |
| S9 | Compute a cost of capital per division. Allocate debt on a stated key, derive each division's D/E, relever its unlevered beta, and combine with the company-wide cost of debt. |
| S11 | Forecast growth and reinvestment per division. |
| S13, S14 | Optionally run a full sum-of-the-parts: value each division separately, then run one bridge. |

Watch for allocation artefacts. A large asset base against a small business value produces an implausible
divisional D/E, and with it a divisional cost of capital low enough to let weak projects clear.
Consider running four numbers side by side: intrinsic sum-of-the-parts, relative sum-of-the-parts,
whole-company DCF, and market enterprise value. The spread is the finding.
`concepts/cost-of-debt-capital/divisional-cost-of-capital.md`,
`concepts/cost-of-equity/bottom-up-beta.md`,
`concepts/asset-based-private/sum-of-the-parts-framework.md`,
`concepts/asset-based-private/sum-of-the-parts-dcf.md`,
`concepts/asset-based-private/sum-of-the-parts-pricing.md`,
`concepts/accounting-statements/segment-and-geographic-reporting.md`

## B9. Real options overlay

**Trigger:** a claim graded **possible** at S2 (unassessable probability), or an identifiable option to delay,
expand, or abandon.
**Modifies:** S13/S14 (option value added on top of the DCF, once).
**Gate before any premium is admitted — three sequential tests:** (1) is it genuinely an option (underlying
asset with value, payoff contingent on a strike, fixed life)? (2) is access **exclusive**? Most claimed real
options fail this one. (3) can it be priced (is there a value and a variance for the underlying)?
Value the underlying first; option pricing is always an addendum, never a stand-alone approach. Prefer a
binomial engine where early exercise or jumps matter. Scale computed option value down using the barrier
ladder when exclusivity is partial.
**The double-count rule:** if you raised the DCF growth rate because of the patent or the new market, you
have already paid for it. Route each claim once — that is what the S2 grading exists to enforce.
`concepts/narrative-numbers/contingent-claim-valuation.md`,
`concepts/real-options/real-options-framework.md`,
`concepts/real-options/opportunities-are-not-options.md`,
`concepts/real-options/option-to-delay.md`,
`concepts/real-options/option-to-expand.md`,
`concepts/real-options/option-to-abandon.md`,
`concepts/real-options/patent-valuation-as-option.md`,
`concepts/real-options/natural-resource-options.md`,
`concepts/real-options/black-scholes-model.md`

## B10. Control, restructuring and acquisition overlay

**Trigger:** the valuation supports an acquisition, an activist position, or a restructuring recommendation.
**Modifies:** run the whole pipeline **twice** — once on the status quo (as currently run) and once on the
optimally-run firm — then weight.
- *Status quo value:* the standard pipeline, including sum-of-the-parts for JVs and associates.
- *Restructured value:* pull the four levers only — existing cash flows (margins, tax, working capital),
  growth from new investment (reinvestment rate × ROC), length of the growth period, cost of capital (move to
  the optimal debt ratio). ROIC > WACC is the value test.
- `Value of control = restructured value − status quo value`.
- `Expected value of control = P(management change) × value of control`. Invert a market price to read the
  probability the market is already pricing.
- *Synergy* is valued **on top of** the restructured target, in three steps, and discounted at the **target's**
  own risk and debt capacity — never at the acquirer's cheaper rate. Cost synergies land; growth synergies
  mostly do not; haircut accordingly.
- Acid test: `price paid ≤ status quo value + value of control + value of synergy`. A blanket "20% control
  premium" on top of a valuation that already includes control is double counting.
- Allocate control value across share classes (voting premium) and across private stakes (minority discount).
`concepts/acquisitions-control-enhancement/three-reasons-and-acid-test.md`,
`concepts/acquisitions-control-enhancement/status-quo-valuation.md`,
`concepts/acquisitions-control-enhancement/restructured-value-and-value-of-control.md`,
`concepts/acquisitions-control-enhancement/expected-value-of-control.md`,
`concepts/acquisitions-control-enhancement/implied-probability-of-management-change.md`,
`concepts/acquisitions-control-enhancement/valuing-synergy.md`,
`concepts/acquisitions-control-enhancement/synergy-delivery-odds.md`,
`concepts/acquisitions-control-enhancement/target-discount-rate-discipline.md`,
`concepts/acquisitions-control-enhancement/control-premium-rules-of-thumb.md`,
`concepts/acquisitions-control-enhancement/paths-to-value-creation.md`,
`concepts/dark-side-difficult/value-of-control-and-restructuring.md`,
`concepts/dark-side-difficult/return-improvement-and-governance-drag.md`,
`concepts/deliverables-worked-examples/value-of-control-and-synergy.md`

---

# C. Cross-cutting consistency invariants

These bind more than one stage, which is why no stage owns them. Every one is a mechanical pass/fail at S17.

**C1 — Claimholder match.** Equity cash flows (dividends, FCFE) go with the cost of equity and produce equity
value. Firm cash flows (FCFF) go with the cost of capital and produce the value of **operating assets**, which
still needs the bridge. Return on equity is compared to the cost of equity; return on capital to the cost of
capital. *Failure cost:* discounting FCFF at ke understates equity by roughly the debt value; discounting FCFE
at WACC overstates it.
Owners: S4, S9, S10, S13.

**C2 — Currency match.** One currency across the riskfree rate, the ERP, the cost of debt, the weights, the
cash flows and the terminal growth cap. Convert whole rates by differential inflation, never by spot exchange
rates, and convert the cash flows with the **same** inflation assumptions. Value must be invariant to the
currency chosen; if it is not, the model is inconsistent. A higher local-currency discount rate is inflation,
not risk.
Owners: S4, S5, S6, S8, S9, S11, S12.

**C3 — Inflation basis match.** Nominal cash flows with a nominal rate; real cash flows with a real rate.
Below 10% expected inflation stay nominal (taxes are levied on nominal income). At or above 10%, convert both
sides via Fisher. Deflate a year-t cash flow by `(1+i)^t`, not by one year's inflation. Use the exact
multiplicative form, not the additive shortcut, once inflation exceeds ~3–4% or the horizon is long.
Owners: S4, S5, S11, S12.

**C4 — Growth ↔ reinvestment ↔ return.** `g = reinvestment rate × return` in every explicit year;
`reinvestment rate = g/ROC` (or `payout = 1 − g/ROE`) in the terminal year. Never set growth and reinvestment
independently. Never mix the three matched pairs of (earnings measure, reinvestment measure, return measure).
The efficiency term is a one-off spread over a transition and cannot appear in stable growth.
Owners: S11, S12, S17.

**C5 — Growth ≤ riskfree rate in the valuation currency.** The riskfree rate is inflation plus real growth in
that economy, so the cap follows from the arithmetic, not from convention. Negative caps are legitimate and
force a negative terminal reinvestment rate. Selective normalization of the riskfree rate without normalizing
growth, inflation and the ERP is a systematic downward bias on every valuation.
Owners: S5, S12.

**C6 — One tax rate.** The rate used for EBIT(1−t) is the rate used for the after-tax cost of debt, in every
year. In zero-tax (NOL) years the debt tax shield is also zero. The terminal year uses the marginal rate with
no NOL shield. Marginal, not effective, for the shield.
Owners: S3, S8, S9, S10.

**C7 — One leverage convention.** Gross debt throughout or net debt throughout. Gross: strip cash from the
unlevered beta separately, weight on gross debt and full equity, value operating assets and add cash back at
the end. Net: unlever and relever on net D/E, weight on net debt, and the value is already net of cash — do
not add cash back. The same D/E must appear in the beta relevering and in the WACC weights. A negative net
debt ratio is arithmetically fine and easy to mishandle downstream.
Owners: S7, S9, S14.

**C8 — One vintage, one date.** The riskfree rate, the ERP, the country ERP table, the default-spread table,
the industry averages, the beta and the leverage ratio must all be as of the valuation date. A 2021 riskfree
rate with a 2013 country ERP table, or current spreads with a stale ERP, is an internal inconsistency that no
later stage can repair. Record the vintage of every lookup used.
Owners: S5, S6, S7, S8, S9.

---

# D. The circularity register

Four places where the pipeline is not a DAG. Each is solved by fixed-point iteration; each returns a wrong
answer silently if iteration is skipped.

**D1 — Lease debt ↔ interest coverage ↔ synthetic rating ↔ cost of debt.** Lease commitments are discounted at
the pre-tax cost of debt; the cost of debt comes from a synthetic rating; the rating comes from a
lease-adjusted coverage ratio; the lease adjustment needs the cost of debt. Seed `kd = Rf + guessed spread`,
loop `lease PV → adjusted EBIT and interest → coverage → rating → spread → kd`, and stop when the spread is
stable. Converges in a few passes. **Cap the iterations and keep the last value** — a firm sitting on a
bracket boundary can oscillate between two adjacent ratings. With no leases the loop disappears.
Order matters: leases must be capitalized *before* the rating is computed. Owners: S3, S8, S9.

**D2 — Employee option value ↔ value per share.** The dilution-adjusted Black-Scholes needs a stock price
input, and the model's own value per share is that input, which in turn nets out the option value. Guess `C`,
compute `S_adj`, recompute `C`, repeat to a fixed point. Convergence is fast. A single pass gives the wrong
option value and the wrong per-share value. Owner: S14.

**D3 — Debt schedule ↔ firm value (FCFF/FCFE reconciliation).** The identity holds only when
`Debt_t = DR × V_t` with `V_t` the *contemporaneous* firm value, `V_t = V_{t−1}(1+WACC) − FCFF_t`. Applying the
debt ratio to book capital, or charging interest on end-of-year debt, breaks the identity. Owner: S10.

**D4 — Gross-versus-net cash allocation.** Under the gross-debt convention the debt allocated to cash depends
on the firm's own debt ratio, which depends on firm value, which depends on the WACC, which depends on the
allocation. Solve iteratively; convergence is well under 50 iterations. The two conventions agree only at a 0%
tax rate, and the net-debt approach gives the lower value as the tax rate rises. Owner: S9.

---

# E. Terminal deliverable

**Minimum reportable set.** Narrative in prose at the top. Driver assumptions in the middle with a **"link to
story"** note on every row. The value bridge at the bottom. Value per share against price, with the gap and
the named catalyst. A range (sensitivity or scenario or simulation) with a designated base cell. The
validation battery result. The vintage of every lookup. The two counts that must both be zero: model inputs
with no story sentence, and story claims with no driver.

**What the report must not do.** Present a point estimate to the cent. Average a DCF value with a
multiple-based price. Present a range without a chosen cell. Describe an exit-multiple terminal value as
intrinsic. Report a restructured value as the current value.

`concepts/deliverables-worked-examples/equity-valuation-project-blueprint.md`,
`concepts/deliverables-worked-examples/two-stage-fcff-company-valuation.md`,
`concepts/deliverables-worked-examples/valuation-triangulation-and-recommendation.md`,
`concepts/deliverables-worked-examples/project-executive-summary-scorecard.md`

---

# F. The double-count register

Each of these is the same error in a different costume: charging or crediting the same thing twice. Run every
one as a check at S17.

| # | Double count | Where it hides | Fix |
|---|---|---|---|
| F1 | Interest tax shield | in the `(1−t)` on kd **and** added back in FCFF | shield lives only in the discount rate |
| F2 | Cash | interest income left in the cash flows **and** cash added back in the bridge | strip interest income, use the operating-asset beta |
| F3 | Pension underfunding | counted as debt in the WACC **and** subtracted in the bridge | bridge only, once |
| F4 | Employee options | option value subtracted **and** diluted shares used | subtract value, divide by **actual** shares |
| F5 | Brand / intangible value | embedded in margins and growth **and** added as an asset | never add; it is in the flows |
| F6 | Country risk | stripped from Rf, then re-added through both the ERP and beta; or a global rating plus a sovereign spread | one channel only, declared |
| F7 | A "possible" market | raised the DCF growth rate **and** added as option value | route each claim once (S2 grading) |
| F8 | Cross-holding | equity income left in operating earnings **and** the stake's value added | strip the income, add the stake |
| F9 | Complexity / opacity | discount rate raised **and** cash flows cut **and** a final haircut | pick exactly one channel |
| F10 | Distress | failure probability applied **and** a distress-adjusted discount rate used | probability branch only |
| F11 | Lease payment | reclassified out of operating costs **and** left in the forecast cash flows | net income must be unchanged |
| F12 | Acquisition amortization | inside reported D&A **and** subtracted again in net cap ex | check reported D&A first |
| F13 | Working capital | inside the sales-to-capital reinvestment **and** subtracted as ΔWC | the sales-to-capital route already includes it |
| F14 | Future equity grants | forecast as an expense **and** their shares added to the count | expense for future grants, share count for past ones |
| F15 | Control | value of control computed **and** a blanket 20% control premium added | the premium is the value of control |
| F16 | Undiversification | total beta used **and** an illiquidity discount applied without checking overlap | check the overlap explicitly |

---

# G. Determinism boundary

What a script computes versus what an agent judges, stage by stage. This is the line that decides what is
automated and what is argued.

| Stage | Script computes | Agent judges |
|---|---|---|
| S1 | TTM arithmetic, invested capital, ROIC, sales-to-capital, industry lookups | which industry is the comparison set; whether recent history is a guide or a break |
| S2 | the completeness counts; the aggregation test's arithmetic | the narrative; the grade of each claim; the market definition |
| S3 | lease PV, research asset, all adjusted line items, NOL waterfall, ratio pack | classification of every expense; whether a charge is one-time; whether to normalize and over what window |
| S4 | the 80/110 screen, the `g_econ + 10%` screen, the 10% inflation switch | whether leverage is "stable"; whether barriers justify a longer phase |
| S5 | rate selection, `min()` over Euro issuers, spread subtraction, differential inflation | which spread route; whether a sovereign is default-free; the inflation forecast |
| S6 | implied-ERP root find, CRP scaling, operation weighting | which premium family; which exposure measure; the attachment mechanism; λ |
| S7 | unlever/relever, value weights, total beta, standard errors, regression | the comparable set; median vs mean; whether the marginal investor is diversified |
| S8 | coverage, rating lookup, spread lookup, market value of debt, after-tax kd | firm class; which estimation route; λ_debt; whether the actual rating is stale |
| S9 | weights, WACC, currency conversion, the rate path, divisional rates | gross vs net; current vs target structure; division definitions and the debt-allocation key |
| S10 | all cash-flow definitions, the reconciliation unit tests | whether leverage is stable enough for the DR shortcut; which DR |
| S11 | the whole forecast table, growth decomposition, marginal ROIC | growth rate, target margin, sales-to-capital, convergence year, target ROC |
| S12 | TV formula, `g/ROC`, the implied-ROIC reverse check | terminal growth within the cap; terminal ROC; whether a moat persists; phase length |
| S13 | cumulative discounting, the failure blend | the failure probability and the recovery basis |
| S14 | every bridge line, dilution-adjusted Black-Scholes, the fixed point | which cash is operating; cash discount/premium; holdings values; contingent-liability probabilities |
| S15 | gap, ratio, expected return, breakeven input | whether the gap will close and what closes it |
| S16 | grids, simulation percentiles | which inputs to vary; distribution shapes; correlations; which cell is the base case |
| S17 | every screen and invariant | whether a flagged excess return is defensible |
| S18 | probability weighting, re-runs, the revision-symmetry count | break vs shift vs change |

---

# H. Stage dependency map (for loopback routing)

When a finding reopens a stage, these are the stages that must re-run with it.

```
S0  -> everything
S1  -> S2, S3, S6(weights), S7(mix), S14(shares/options)
S2  -> S11, S16, S18
S3  -> S8(coverage), S9(weights), S10, S11, S12, S14
S4  -> S9, S10, S11, S12, S13, S14
S5  -> S6, S8, S9, S12(cap), S13
S6  -> S9, S13
S7  -> S9, S13
S8  -> S9, S13
S9  -> S13, S12(terminal rate)
S10 -> S11, S13
S11 -> S12, S13
S12 -> S13
S13 -> S14
S14 -> S15
S15 -> S16, S18
S17 -> the owning stage of each failed check
S18 -> re-enter at the owning stage, never at S0 unless classification changed
```

Loopback discipline: cap re-runs at two per stage. On the third, disclose the finding in the report as an
unresolved risk rather than looping forever.

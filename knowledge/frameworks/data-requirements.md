# Data requirements map

The input contract for the analysis pipeline. Every external number the playbooks
consume, where it comes from, how stale it may be, whether a user can hand it over
directly, and what to do when it is missing.

This document is written to be executed. It drives two things:

1. **The data-collection agent** (`financial-data-collector` in `architecture/SPEC.md`)
   — what to fetch, from which source, in which order, and what to write into
   `01-data/raw-financials.json`, `01-data/market-data.json`, `01-data/sources.md`
   and `01-data/gaps.json`.
2. **The gate predicates** — `G1_data`, `G3_financials`, `G4_discount_rate`,
   `G5_forecast` are all predicates over the fields defined here.

It does **not** restate method. Every stage cites the concept files that own the
procedure; read those for how a number is used. This map says only what must be in
hand before that procedure can run, and what to substitute when it is not.

---

## 0. The contract

### 0.1 Three data classes

Every field carries exactly one class. The class determines caching, refresh policy
and blame when the number is wrong.

| Class | Code | Definition | Keyed by | Cache scope |
|---|---|---|---|---|
| Company-specific | **CO** | Comes out of this company's filings, its own market prices, or its own ownership records | ticker + fiscal period | per-company, per-period |
| Market-wide | **MK** | A price or rate observed in a market, not attributable to one firm | currency/country/index + date | global, per valuation date |
| Reference table | **RT** | A published cross-sectional or historical lookup, refreshed on a vintage cycle | table name + as_of | global, per vintage |
| Derived | **DV** | Computed by the pipeline from CO/MK/RT inputs; never fetched | — | recomputed |

The collector fetches CO, MK and RT. It never fetches DV. Where a DV field appears
below it is because a downstream stage treats it as an input and must be able to
name its provenance.

### 0.2 Field descriptor schema

Every row in every input table below has these columns:

- **Field** — canonical name used in the artifact JSON.
- **Units** — currency + scale, decimal fraction, count, years, rating symbol, or category.
  Percentages are **always decimal fractions** in artifacts (0.0472, never 4.72).
- **Source** — a source ID from §1.
- **Freq** — how often the underlying number changes; drives the refresh policy in §7.
- **User?** — whether a user can supply it directly and be believed.
  - `Y` = accept a user value as authoritative, record it as `source: "user"`.
  - `Y*` = accept, but run the stated validation before use.
  - `N` = never accept a bare user value; it is either derivable or must be traced to a source.
- **Fallback** — what to do when it cannot be obtained. `BLOCK` means the gate fails.

### 0.3 Status vocabulary for `gaps.json`

Every field the collector attempts resolves to exactly one status:

| Status | Meaning | Effect |
|---|---|---|
| `found` | Retrieved from the named source at the named vintage | none |
| `user` | Supplied by the user, validation passed | record and flag in the report |
| `derived` | Computed from other found fields via a stated identity | record the identity |
| `fallback` | Primary source unavailable, documented default applied | must appear in `sources.md` and in the report's assumption list |
| `stale` | Found, but older than the freshness limit in §7 | usable; flag; forbidden for the fields marked `vintage-critical` |
| `missing` | Not obtainable, no fallback exists | triggers the stage's BLOCK rule |

---

## 1. Source registry

Canonical source IDs. Every `Source` cell below is one of these.

### 1.1 Company filings and disclosures (CO)

| ID | Source | What it yields | Notes |
|---|---|---|---|
| `F-10K` | Annual report (10-K, 20-F, 40-F, or local annual report) | Three statements, all footnotes, segment note, MD&A | The base document. Non-US filers: IFRS/Ind-AS presentation differs — see `concepts/accounting-statements/accounting-standards-gaap-ifrs.md` |
| `F-10Q` | Latest quarterly filing | Year-to-date columns for the trailing-12-month rebuild | Required whenever the last 10-K is >1 quarter old |
| `F-DEBT` | Debt footnote | Instrument list, stated rates, maturities, currency, fixed/floating, 5-year maturity schedule | |
| `F-LEASE` | Lease footnote / commitments note | Current-year lease expense, minimum commitments years 1–5, "thereafter" lump, reported lease liability (post-2019) | |
| `F-SEG` | Segment and geographic footnote | Third-party revenue, intersegment revenue, operating income, identifiable assets, investments, cap ex, D&A per segment/region | |
| `F-OPT` | Stock-compensation footnote | Options outstanding, weighted-average exercise price, weighted-average remaining life, vesting status, restricted stock | |
| `F-INV` | Investments / equity-method footnote | Cross-holdings with ownership %, carrying value, equity income | |
| `F-TAX` | Tax footnote | Effective rate reconciliation, statutory rate, NOL carryforward balance and expiry | |
| `F-PEN` | Pension & OPEB footnote | Projected benefit obligation, plan assets, funded status | |
| `F-CONT` | Commitments & contingencies footnote | Litigation, guarantees, take-or-pay, off-balance-sheet obligations | |
| `F-PROXY` | Proxy statement (DEF 14A or local equivalent) | Board composition, tenure, independence, attendance, compensation, insider holdings, charter/bylaw provisions | |
| `F-ACQ` | Acquisitions footnote | Deal prices, goodwill created, purchase-price allocation, stock-funded deals | Stock-funded deals never appear in the cash flow statement |

### 1.2 Market data (MK)

| ID | Source | What it yields |
|---|---|---|
| `M-PX` | Equity market data feed | Current price, shares outstanding, market cap, historical price series, dividend/split-adjusted returns |
| `M-IDX` | Index data | Index level, index return series, index dividends, index buybacks |
| `M-BOND` | Corporate bond market | Traded bond prices, coupons, maturities, YTM for the subject firm |
| `M-RATE` | Government bond markets | 10-year (and other tenor) government bond yields by currency; TIPS / index-linked yields |
| `M-CDS` | CDS market | Sovereign 10-year CDS spreads; corporate CDS where traded |
| `M-RATING` | Rating agencies (Moody's / S&P / Fitch) | Corporate issuer and issue ratings; sovereign local-currency and foreign-currency ratings; local-scale agency ratings (CRISIL etc.) |
| `M-CRED` | Corporate credit spread series | Baa−T.Bond spread; spread-by-rating curve at a date |
| `M-OWN` | Ownership filings and aggregators (13F, Forms 3/4/5, local equivalents) | Institutional %, insider %, float, largest holders |
| `M-FX` | FX market | Spot rates, forward rates (for interest-rate-parity checks) |

### 1.3 Damodaran reference datasets (RT)

These are the named lookup tables. Each ships with an `as_of` field and is versioned;
see §7 for refresh rules. Paths are `cost-of-capital-toolkit/resources/data/` per SPEC §8.

| ID | Dataset | Columns used | Vintage-critical? |
|---|---|---|---|
| `D-ERP` | Implied equity risk premium for the S&P 500 (`implprem` / histimpl series) | Current implied ERP; annual history; expected return on stocks | **Yes** |
| `D-HIST` | Historical returns (`histretSP`) | Arithmetic and geometric stocks−T.Bills and stocks−T.Bonds by window; standard errors | No |
| `D-CTRY` | Country equity risk premiums | Country → Moody's local-currency rating, default spread, country risk premium, total ERP; regional GDP-weighted ERPs; PRS composite score mapping for unrated countries | **Yes** |
| `D-SOVSPR` | Sovereign rating → default spread table | Rating → typical default spread | **Yes** |
| `D-TAX` | Country corporate marginal tax rates | Country → statutory marginal rate | Yes |
| `D-RATE1` | Synthetic rating table, large/stable firms | Coverage lower bound, upper bound, rating, default spread | **Yes** (spreads move; brackets do not) |
| `D-RATE2` | Synthetic rating table, small/risky firms | Same | **Yes** |
| `D-RATE3` | Synthetic rating table, financial-service firms (long-term interest coverage only) | Same | **Yes** |
| `D-SPREAD` | Rating → default spread map (for the actual-rating route) | Rating → spread, by date | **Yes** |
| `D-INDUS` | US industry averages | Per industry: n firms, levered beta, **unlevered beta**, std dev equity, market D/E, market debt/capital, ROE, ROC, effective tax rate, pre-tax and after-tax operating margin, net margin, Cap Ex/Depreciation, **non-cash WC/revenues**, payout ratio, reinvestment rate, **sales/capital**, EV/Sales, EV/EBITDA, EV/EBIT, P/BV, trailing PE, cost of equity, cost of capital, pre-tax cost of debt | Yes |
| `D-GLOB` | Global industry averages | Same schema, global universe | Yes |
| `D-DEFPROB` | Cumulative default probability by rating | Rating → 1yr / 5yr / 10yr cumulative default rate (Altman-style) | Yes |
| `D-DISTRESS` | Indirect bankruptcy cost table | Rating → EBITDA haircut under Low / Medium / High severity | No |
| `D-RDLIFE` | R&D amortizable life by industry | Industry → amortizable life in years (2–10) | No |
| `D-CPXSEC` | Sector cap-ex ratios | Sector → Cap Ex/Depreciation, Net CapEx/Sales, Net CapEx/EBIT(1−t) | No |
| `D-MACRO` | Sector macro-sensitivity coefficients by SIC | Sector → duration, cyclicality, inflation, currency coefficients (firm-value and operating-income blocks) | No |
| `D-MULTREG` | Market-wide and regional multiple regressions | Region → fitted equations for PE, PEG, PBV, EV/EBITDA, EV/Sales, EV/IC with R² | **Yes** |
| `D-DEBTREG` | Market-wide debt-ratio regression | Coefficients on ETR, growth, institutional holdings, CVOI, EBITDA/EV | Yes |
| `D-PAYREG` | Market payout / yield regressions | Coefficients on beta, expected growth, debt-to-capital, with R² | Yes |
| `D-ILLIQ` | Illiquidity regressions | Silber restricted-stock regression; bid-ask-spread regression coefficients | No |
| `D-SURV` | Sector and startup survival tables | Years-since-founding → survival rate, by sector | No |
| `D-DISTRIB` | Multiple distribution statistics by region | Multiple → 10th/25th/median/75th/90th percentile, % of firms with a computable value | Yes |

### 1.4 Macro sources (MK)

| ID | Source | What it yields |
|---|---|---|
| `X-CB` | Central bank / statistical agency | CPI inflation, inflation targets, real GDP growth (actual and forecast) |
| `X-FRED` | FRED or equivalent macro series | DGS10 (10-yr Treasury), BAA10Y (Baa spread), CPIAUCSL, GDPC1, trade-weighted dollar index |
| `X-BREAK` | Inflation-indexed bond market | TIPS / index-linked breakeven inflation, real yields |
| `X-IMF` | IMF / World Bank / OECD | Long-run inflation and real growth forecasts by country; nominal GDP |

### 1.5 Consensus and third-party estimates (CO/MK)

| ID | Source | What it yields | Trust rule |
|---|---|---|---|
| `E-CONS` | Analyst consensus aggregator | 5-year expected EPS growth, next-year revenue and EPS, estimate dispersion, revision history | Input, not answer. Never drop an EPS growth rate into an FCFF model. `concepts/dcf-cashflows-growth/analyst-growth-estimates.md` |
| `E-IDXCONS` | Top-down index earnings consensus | Aggregate index earnings growth for the implied-ERP solve | Required for `D-ERP` recomputation |
| `E-GOV` | Governance score vendor (ISS QuickScore or equivalent) | Overall, audit, board, shareholder-rights, compensation sub-scores (1–10, 1 = best) | Read the underlying policies; never take the score at face value |
| `E-MKT` | Total addressable market research | Market size, market growth rate, market shares | Only for revenue-driven forecasts; always a judgment input |

---

## 2. Global conventions and cross-stage consistency rules

These bind every stage. A violation is a hard failure, not a warning.

### 2.1 The five matching rules

| # | Rule | Checked at | Concept |
|---|---|---|---|
| **R1 Currency** | The riskfree rate, ERP, cost of debt, cash flows, growth rate and terminal growth are all in ONE currency | G4, G5 | `concepts/cost-of-equity/cost-of-equity-assembly.md`, `concepts/cost-of-debt-capital/currency-conversion-of-discount-rates.md` |
| **R2 Claimholder** | Equity cash flows ↔ cost of equity; firm cash flows ↔ cost of capital. Return on equity ↔ cost of equity; return on capital ↔ cost of capital | G4, G6 | `concepts/cost-of-debt-capital/hurdle-rate-choice.md` |
| **R3 Nominal/real** | Nominal cash flows ↔ nominal discount rate; real ↔ real. Inflation assumption used in cash flows equals the one used in any currency conversion | G5 | `concepts/cost-of-equity/cost-of-equity-assembly.md` |
| **R4 Vintage** | All `vintage-critical` reference tables share one `as_of`, and that `as_of` is within the freshness limit of the valuation date | G1, G4 | `concepts/cost-of-debt-capital/default-spreads-over-time.md`, `concepts/cost-of-equity/country-risk-premium.md` |
| **R5 Debt convention** | Gross debt throughout, or net debt throughout. The convention used to lever beta must equal the convention used in the WACC weights and in the equity bridge | G4, G6 | `concepts/cost-of-debt-capital/net-debt-vs-gross-debt.md` |

### 2.2 The single-count rules

Each of these is the same error in different clothing. Enforce all of them.

| # | Rule |
|---|---|
| **N1** | Interest tax shield lives in the discount rate `(1−t)` only. Never also in FCFF. `concepts/cost-of-debt-capital/after-tax-cost-of-debt.md` |
| **N2** | Country risk is attached **once** — through the ERP, or through lambda, or through the cash flows. Never two of the three. If the sovereign spread was stripped out of the riskfree rate, it may not also sit inside the ERP build. `concepts/cost-of-equity/country-risk-premium.md`, `concepts/cost-of-debt-capital/country-risk-in-cost-of-debt.md` |
| **N3** | Employee option value is subtracted **or** diluted shares are used — never both. `concepts/dcf-model-choice-loose-ends/employee-option-per-share-approaches.md` |
| **N4** | Cash is inside the cash flows (with its interest income and a cash-diluted beta) **or** outside and added back. Never both. `concepts/dcf-model-choice-loose-ends/cash-in-valuation.md` |
| **N5** | Cross-holding value is added as a non-operating asset **or** its equity income sits in operating earnings. Never both. `concepts/accounting-statements/non-operating-items-and-cross-holdings.md` |
| **N6** | Failure risk enters through a probability weight **or** through a raised discount rate. Never both. `concepts/dark-side-difficult/distress-and-failure-adjusted-value.md` |
| **N7** | Downside is protected by a rating constraint **or** an EBIT haircut. Never both. `concepts/capital-structure/downside-risk-and-rating-constraints.md` |
| **N8** | A complexity/opacity adjustment is made in one place only — cash flows, discount rate, growth, or a final haircut. `concepts/dcf-model-choice-loose-ends/complexity-discount.md` |
| **N9** | Real-option premium is added only after the corresponding optimism is removed from the DCF. `concepts/real-options/real-options-framework.md` |
| **N10** | Control value is added only for a buyer who can force the change; never for a minority-stake buy/sell call. `concepts/acquisitions-control-enhancement/expected-value-of-control.md` |

### 2.3 Unit and sign conventions

- Percentages stored as decimals. Growth rates, margins, tax rates, payout ratios, debt ratios, ROE/ROC, spreads.
- Currency fields carry an explicit `{value, currency, scale}` triple. Never mix scales inside one table (Bookscape's thousands-vs-millions trap: `concepts/capital-structure/optimal-debt-ratio-by-firm-type.md`).
- Cash-flow-statement line items arrive **already signed**. Cap ex and working-capital changes from `F-10K` are added, not subtracted. `concepts/dividend-policy/fcfe-potential-dividends.md`
- A **positive** change in non-cash working capital is a cash **outflow**.
- Balance-sheet items are point-in-time; income and cash flow items cover a period. Any ratio mixing them declares whether it uses beginning-of-period or average balances. ROIC and ROE use **beginning-of-period** capital.
- Macro conventions: interest-rate and inflation-rate changes are **absolute** changes in the rate; GDP and currency changes are **percentage** changes. `concepts/capital-structure/macro-sensitivity-regressions.md`

---

# Part III — Collection stages

Eight stages. The collector runs A1 first (it determines everything else), then A2–A8;
A2–A8 are parallelisable except where a dependency is named.

---

## A1 — Mandate, identity and routing data

**Purpose:** fix the analysis frame before anything is fetched. Every later fetch is
parameterised by the outputs of this stage.

**Inputs**

| Field | Units | Source | Freq | User? | Fallback |
|---|---|---|---|---|---|
| `mode` | enum: valuation \| corporate-finance \| acquisition \| project \| ipo \| restructuring | user | per-run | Y | BLOCK |
| `company.name`, `company.ticker`, `company.exchange` | string | user / `M-PX` | static | Y | BLOCK |
| `company.country_of_incorporation` | ISO country | `F-10K` | static | Y | BLOCK |
| `company.currency` | ISO currency | user | per-run | Y | Reporting currency of `F-10K` |
| `valuation_date` | date | user | per-run | Y | Today |
| `company.fiscal_year_end` | MM-DD | `F-10K` | static | Y* | Infer from filing dates |
| `company.industry_us`, `company.industry_global` | `D-INDUS` / `D-GLOB` industry name | user / SIC mapping | static | Y* | Map from SIC/GICS; if ambiguous, list candidates in `gaps.json` |
| `company.is_public` | boolean | `M-PX` | static | Y | If no price series exists, treat as private → branch C6 |
| `company.reporting_standard` | enum: GAAP \| IFRS \| local | `F-10K` auditor's report | static | Y* | Infer from statement headings |

**Decision rules**

- **DR-A1.1 (currency).** If `company.currency` differs from the reporting currency of `F-10K`, flag every downstream stage as requiring a currency conversion, and record which of the two routes will be used (differential-inflation conversion of a completed rate, or direct rebuild from a local riskfree rate). `concepts/cost-of-debt-capital/currency-conversion-of-discount-rates.md`
- **DR-A1.2 (industry mapping).** Map by the business the firm actually operates in, not its listing classification. A multi-business firm gets a *list* of industries plus revenue weights (see A3). `concepts/relative-valuation/industry-average-multiples.md`
- **DR-A1.3 (project mode).** In `mode = project` the company-level stages A2–A4 collapse to whatever is needed for the divisional hurdle rate; the project's own cash-flow schedule is a user input.

**Outputs:** the fetch parameter set — ticker, currencies, fiscal calendar, industry keys, valuation date, as_of for reference tables.

**Concepts:** `concepts/accounting-statements/accounting-standards-gaap-ifrs.md`, `concepts/deliverables-worked-examples/project-company-selection.md`, `concepts/dark-side-difficult/difficult-company-taxonomy.md`

---

## A2 — Financial statements (multi-year)

**Purpose:** the three statements, for enough years to normalize, compute growth, and
measure volatility.

**Horizon rule:** pull **10 fiscal years** where available, minimum **5**, absolute
minimum **1** (which forces `require-normalized-earnings = false` to be impossible
and blocks several branches).

**Inputs — income statement (CO, `F-10K` + `F-10Q`)**

| Field | Units | Freq | User? | Fallback |
|---|---|---|---|---|
| `revenues` | ccy | annual + quarterly | Y* | BLOCK |
| `cogs`, `sga`, `rnd`, `other_operating_expense` | ccy | annual | Y* | If no COGS line (IFRS by-nature presentation), build a proxy from materials + inventory change + production share of employee benefits; record the assumption |
| `depreciation_amortization` | ccy | annual | Y* | Take from the cash-flow statement add-back if not on the face of the income statement |
| `ebit` (operating income, as reported) | ccy | annual + TTM | Y* | Derive: revenues − operating expenses, on **your** operating/non-operating line, not the filer's label |
| `interest_expense` (gross) | ccy | annual | Y* | If the filer nets interest, dig into `F-DEBT`; a net figure is insufficient |
| `interest_income` | ccy | annual | Y* | 0 |
| `equity_income_from_affiliates` | ccy | annual | Y* | 0 |
| `pretax_income`, `tax_provision`, `net_income` | ccy | annual + TTM | Y* | BLOCK |
| `noncontrolling_interest_income` | ccy | annual | Y* | 0 |
| `net_income_to_parent` | ccy | annual | N (derived) | net_income − NCI |
| `shares_basic`, `shares_diluted` (weighted average) | count | annual | Y* | BLOCK for per-share work |
| `special_items` (each labelled one-time / restructuring / impairment charge, per year) | ccy | annual, 5–10 yrs | Y* | Empty list; flag that the recurrence test cannot run |
| `excise_taxes` | ccy | annual | Y* | 0 — required only for commodity filers |

**Inputs — balance sheet (CO, `F-10K`)**

| Field | Units | Freq | User? | Fallback |
|---|---|---|---|---|
| `cash_and_equivalents`, `short_term_investments`, `marketable_securities` | ccy | annual (2+ yrs) | Y | BLOCK |
| `accounts_receivable`, `inventory`, `other_current_assets` | ccy | annual (2+ yrs) | Y* | BLOCK for working-capital work |
| `accounts_payable`, `accrued_liabilities`, `taxes_payable`, `other_non_debt_current_liabilities` | ccy | annual (2+ yrs) | Y* | BLOCK for working-capital work |
| `short_term_debt`, `current_portion_lt_debt`, `commercial_paper` | ccy | annual | Y* | BLOCK — these must be pulled OUT of current liabilities |
| `long_term_debt` (book) | ccy | annual | Y | BLOCK |
| `gross_ppe`, `accumulated_depreciation`, `net_ppe` | ccy | annual | Y* | Net PP&E alone; loses the asset-age ratio |
| `goodwill`, `intangibles_definite`, `intangibles_indefinite`, `accumulated_amortization` | ccy | annual | Y* | 0 |
| `equity_method_investments`, `other_non_operating_assets` | ccy | annual | Y* | 0 |
| `book_equity_parent`, `noncontrolling_interests`, `mezzanine_equity` | ccy | annual | Y* | BLOCK for ROE |
| `paid_in_capital`, `retained_earnings`, `treasury_stock`, `aoci` | ccy | annual | Y* | Composition analysis skipped |
| `preferred_stock` (book) | ccy | annual | Y | 0 |
| `total_assets`, `total_liabilities`, `total_equity` | ccy | annual | Y | BLOCK — needed for the balance check |

**Inputs — cash flow statement (CO, `F-10K`)**

| Field | Units | Freq | User? | Fallback |
|---|---|---|---|---|
| `cfo` and its build-up lines: net income, D&A, stock-based comp, deferred taxes, impairments, each working-capital change line | ccy | annual (5–10 yrs) | Y* | Section total alone is insufficient for FCFE |
| `capital_expenditures` | ccy | annual | Y | BLOCK |
| `divestitures_of_assets` | ccy | annual | Y* | 0 |
| `cash_acquisitions` | ccy | annual (5–10 yrs) | Y* | 0 — but flag: acquisitive firms without this understate reinvestment several-fold |
| `purchases_sales_of_investments` | ccy | annual | Y* | 0 |
| `debt_raised`, `debt_repaid` | ccy | annual | Y* | Net debt issued alone |
| `equity_issued`, `stock_buybacks` | ccy | annual (5–10 yrs) | Y | 0 |
| `dividends_paid_common`, `dividends_paid_preferred`, `dividends_paid_nci` | ccy | annual (5–10 yrs) | Y | 0 |
| `fx_effect_on_cash` | ccy | annual | Y* | 0 |
| `unusual_operating_classifications` (content spend, capitalized software, originated receivables sitting inside CFO) | ccy | annual | Y* | Empty; flag if the filer is a streaming, software or captive-finance business |

**Validation (runs before the stage is marked complete)**

| ID | Tie | Action on failure |
|---|---|---|
| V-A2.1 | `total_assets = total_liabilities + total_equity` (including mezzanine and NCI) | BLOCK — transcription error or a missed layer |
| V-A2.2 | Income-statement `net_income` = first line of CFO (IFRS filers may start at pre-tax profit; then tie to that line and confirm the tax-paid adjustment) | BLOCK |
| V-A2.3 | `retained_earnings_t = retained_earnings_{t−1} + net_income − dividends − buyback charges` | Residual must be explained; flag, do not block |
| V-A2.4 | Income-statement D&A = cash-flow-statement D&A add-back | Flag; check whether D&A is buried inside COGS |
| V-A2.5 | `beginning_cash + CFO + CFI + CFF + fx_effect = ending_cash` on the balance sheet | BLOCK |
| V-A2.6 | Segment third-party revenues + eliminations = consolidated revenues (when A3 is available) | Flag; a gap means a missed corporate or elimination column |

These six ties are the precondition for interpreting anything. `concepts/accounting-statements/role-of-accounting-and-three-statements.md`

**Concepts:** `concepts/accounting-statements/income-statement-structure.md`, `.../balance-sheet-views-and-asset-measurement.md`, `.../cash-flow-statement-structure.md`, `.../cash-flow-from-operations-and-working-capital.md`, `.../investing-cash-flows-and-reinvestment.md`, `.../financing-cash-flows-and-cash-returned.md`, `.../liabilities-debt-and-leases.md`, `.../shareholders-equity-book-value.md`, `.../intangibles-and-goodwill.md`, `.../extraordinary-items-and-pro-forma-earnings.md`

---

## A3 — Footnotes and structured disclosures

**Purpose:** everything the face of the statements omits. This stage is what separates
a usable valuation from a plausible-looking wrong one.

| Field | Units | Source | Freq | User? | Fallback |
|---|---|---|---|---|---|
| `lease.current_expense` | ccy | `F-LEASE` | annual | Y | 0 → lease capitalization skipped, flag |
| `lease.commitments[1..5]` | ccy per year | `F-LEASE` | annual | Y | Post-2019 filers: use the reported lease liability, but flag that the accounting number need not equal the PV of commitments |
| `lease.thereafter_lump` | ccy | `F-LEASE` | annual | Y | 0 → set n₆ = 0, lease life = 5 |
| `lease.reported_liability` (IFRS 16 / ASC 842) | ccy | `F-LEASE` | annual | Y | — |
| `debt.instruments[]` — amount, stated rate, maturity, currency, fixed/floating, straight/convertible | mixed | `F-DEBT` | annual | Y* | Blended rate only |
| `debt.maturity_schedule[1..5]` | ccy per year | `F-DEBT` | annual | Y* | **Default weighted-average maturity = 3 years** |
| `debt.weighted_avg_maturity` | years | derived from schedule | annual | Y | 3 years |
| `debt.weighted_avg_rate` | decimal | derived | annual | N | interest_expense / book debt (diagnostic only, never the cost of debt) |
| `segments[]` — name, third-party revenue, intersegment revenue, operating income, identifiable assets, investments, cap ex, D&A | ccy | `F-SEG` | annual | Y* | Single-segment assumption; blocks divisional rates and branch C7 |
| `geography[]` — region/country, third-party revenue share | decimal | `F-SEG` | annual | Y | Country of incorporation gets 100% — **strongly flagged**, this is the single most common source of a wrong ERP |
| `production_by_country[]` | decimal share | `F-10K` / operating stats | annual | Y | Revenue weights |
| `options.count_outstanding` | count | `F-OPT` | annual | Y | 0 |
| `options.weighted_avg_strike` | ccy | `F-OPT` | annual | Y | Current price (at-the-money assumption) |
| `options.weighted_avg_remaining_life` | years | `F-OPT` | annual | Y | 4 years, and shorten for early exercise |
| `options.vested_fraction` | decimal | `F-OPT` | annual | Y | 1.0 |
| `restricted_stock_outstanding` | count | `F-OPT` | annual | Y | 0 |
| `cross_holdings[]` — name, ownership %, consolidated?, carrying value, listed price if traded | mixed | `F-INV` | annual | Y* | Carrying value; flag |
| `nol_carryforward` | ccy | `F-TAX` | annual | Y | 0 |
| `effective_tax_rate` | decimal | `F-TAX` / derived | annual + TTM | Y | tax_provision / pretax_income |
| `pension_funded_status` | ccy (negative = underfunded) | `F-PEN` | annual | Y | 0 |
| `contingent_liabilities[]` — description, disclosed amount, probability language | mixed | `F-CONT` | annual | Y* | Empty; flag |
| `rnd_history[0..N]` | ccy per year, N = amortizable life | `F-10K` (N+1 years) | annual | Y | Pad missing years with zeros and **flag that the research asset is understated** |
| `acquisitions_history[]` — year, price, cash vs stock | mixed | `F-ACQ` | annual, 5+ yrs | Y* | Cash-acquisition line from A2; stock-funded deals will be missed |

**Decision rules**

- **DR-A3.1 (lease horizon).** `n₆ = ROUND(thereafter_lump / mean(commitments[1..5]))`, half-away-from-zero. Guard: mean = 0 → n₆ = 0. Lease life = 5 + n₆. `concepts/cost-of-debt-capital/operating-leases-as-debt.md`
- **DR-A3.2 (weighted-average maturity).** Weight each disclosed tranche by its share of the **disclosed** total, but apply the resulting maturity to **full book debt**, not to the disclosed subtotal. `concepts/cost-of-debt-capital/market-value-of-debt.md`
- **DR-A3.3 (geographic weights).** Use **third-party** revenue, never total revenue including intersegment. For natural-resource firms prefer production location; for manufacturers ask where the plants are. `concepts/cost-of-equity/operation-weighted-erp.md`
- **DR-A3.4 (R&D life).** `N` from `D-RDLIFE` by industry; the guideline blocks are non-technological service 2, retail/tech service 3, light manufacturing 5, heavy manufacturing 10, research-with-patenting 10, long gestation 10. `concepts/dcf-cashflows-growth/rnd-capitalization.md`
- **DR-A3.5 (hidden reinvestment).** If `unusual_operating_classifications` is non-empty, those amounts move from CFO into the investing step before FCFE is built. `concepts/accounting-statements/investing-cash-flows-and-reinvestment.md`

**Concepts:** `concepts/cost-of-debt-capital/operating-leases-as-debt.md`, `.../market-value-of-debt.md`, `.../what-counts-as-debt.md`, `concepts/dcf-cashflows-growth/rnd-capitalization.md`, `concepts/accounting-statements/segment-and-geographic-reporting.md`, `concepts/dcf-model-choice-loose-ends/valuing-employee-options.md`, `.../cross-holdings.md`, `.../debt-and-other-claims-in-the-bridge.md`

---

## A4 — Company market data

| Field | Units | Source | Freq | User? | Fallback |
|---|---|---|---|---|---|
| `price` | ccy/share | `M-PX` | daily | Y | BLOCK for public firms |
| `shares_outstanding` (actual, not weighted average) | count | `M-PX` / `F-10K` cover | quarterly | Y | BLOCK |
| `market_cap` | ccy | derived | daily | N | price × shares |
| `return_series` (stock, dividend- and split-adjusted) | decimal per interval | `M-PX` | daily→monthly | Y* | Blocks regression beta and Jensen's alpha; bottom-up beta unaffected |
| `index_return_series` | decimal per interval | `M-IDX` | daily→monthly | Y* | Same |
| `traded_bonds[]` — price, coupon, maturity, straight? liquid? | mixed | `M-BOND` | daily | Y* | Empty → cost-of-debt route falls to rating/synthetic |
| `issuer_rating` (agency, scale, date) | rating symbol + enum{global, local-scale} | `M-RATING` | event | Y* | Empty → synthetic rating |
| `issue_ratings[]` | rating symbols | `M-RATING` | event | Y* | Use the **median** when they differ |
| `implied_volatility` / `historical_volatility` (annualized) | decimal | `M-PX` / options market | daily | Y | Industry-average std dev from `D-INDUS` |
| `dividend_history` (DPS, ex-dates, 10 yrs) | ccy/share | `M-PX` | quarterly | Y | Cash-flow-statement dividends |
| `preferred.shares`, `preferred.price`, `preferred.annual_dividend` | mixed | `M-PX` / `F-10K` | quarterly | Y | 0 |
| `convertible.book_value`, `.interest_expense`, `.maturity`, `.market_value` | mixed | `F-DEBT` + `M-BOND` | annual | Y | Treat wholly as debt only if the option is deeply out of the money; otherwise flag |

**Decision rules**

- **DR-A4.1 (regression beta parameters).** Default 5 years of monthly returns. Record estimation period, return interval, and index. The beta is a **diagnostic**, not the hurdle-rate input. `concepts/cost-of-equity/regression-beta.md`
- **DR-A4.2 (index choice).** Use an index representing the marginal investor's portfolio, not the local exchange index for a globally held firm. Index choice moves betas by 0.5 on identical data.
- **DR-A4.3 (rating scale).** Tag every rating as global-agency or local-scale. A local-scale rating does **not** embed sovereign risk; a global one does. This single flag decides whether the country default spread is added or not. `concepts/cost-of-debt-capital/country-risk-in-cost-of-debt.md`
- **DR-A4.4 (bond usability).** A bond is usable for a YTM-based cost of debt only if it is **straight** (no conversion, no call/put, not floating), **long-term**, and **liquid**. Otherwise its yield is contaminated by option value.

**Concepts:** `concepts/cost-of-equity/regression-beta.md`, `.../jensen-alpha.md`, `concepts/cost-of-debt-capital/cost-of-debt-estimation-routes.md`, `.../preferred-stock-cost.md`, `.../convertible-debt-decomposition.md`

---

## A5 — Macro and currency data

Fetched per currency and per operating country, keyed to `valuation_date`.

| Field | Units | Source | Freq | User? | Fallback |
|---|---|---|---|---|---|
| `riskfree.gov_bond_10y[currency]` | decimal | `M-RATE` | daily | Y | See ladder DR-A5.1 |
| `riskfree.tips_yield[currency]` | decimal | `X-BREAK` | daily | Y | Real riskfree ≈ long-term real GDP growth |
| `sovereign.local_currency_rating[country]` | Moody's symbol | `M-RATING` | event | Y* | Convert S&P → Moody's equivalent; if unrated, PRS composite score |
| `sovereign.foreign_currency_rating[country]` | Moody's symbol | `M-RATING` | event | Y* | — (do **not** substitute for the local-currency rating) |
| `sovereign.cds_10y[country]`, `sovereign.cds_10y[US]` | decimal | `M-CDS` | daily | Y | Rating-based lookup `D-SOVSPR` |
| `sovereign.hard_currency_bond_spread[country]` | decimal | `M-BOND` | daily | Y | CDS or rating route |
| `inflation.expected_long_run[currency]` | decimal | `X-CB` / `X-BREAK` / `X-IMF` | quarterly | Y | Central bank target; else TIPS breakeven; else 5-yr trailing CPI |
| `real_gdp_growth.expected[country]` | decimal | `X-IMF` / `X-CB` | quarterly | Y | Trailing 10-yr average |
| `baa_spread` (Baa − T.Bond) | decimal | `X-FRED` / `M-CRED` | daily | Y | Used only for the ERP cross-check |
| `fx_spot[pair]`, `fx_forward[pair]` | rate | `M-FX` | daily | Y | Spot only; forward route unavailable |
| `macro_series` (10-yr rate changes, real GDP growth, CPI inflation changes, trade-weighted dollar % change) | mixed, 20+ yrs | `X-FRED` | annual | Y* | Blocks firm-level macro regressions → fall to `D-MACRO` sector coefficients |

**Decision rules**

- **DR-A5.1 (riskfree ladder).** In order:
  1. Sovereign issuing in this currency is rated **Aaa/AAA** in local currency → its 10-year bond rate **is** the riskfree rate. Stop.
  2. Multiple sovereigns issue in this currency (Euro) → take the **minimum** 10-year rate across them. Do not average, do not use the home sovereign.
  3. Sovereign is below Aaa → riskfree = local 10-yr bond rate **minus** the sovereign default spread. Three ways to get that spread: (a) the sovereign's hard-currency bond spread over the matching Treasury, (b) the sovereign CDS net of the US CDS, (c) `D-SOVSPR` on the **local-currency** rating. Prefer a market measure. Report the range across every available route.
  4. No trustworthy local bond rate → build up: expected inflation + expected real rate; **or** differential inflation from the US$ riskfree; **or** covered-interest-parity from forwards; **or** switch the whole valuation to US$/EUR (and restate every other input).
  `concepts/cost-of-equity/riskfree-rate-fundamentals.md`, `.../currency-riskfree-rate.md`
- **DR-A5.2 (no normalization).** Never substitute a "normalized" historical riskfree rate for the observed one. If a user insists, normalize riskfree rate, inflation, real growth and ERP **together**, and label the output as a valuation of a hypothetical economy. `concepts/cost-of-equity/riskfree-rate-normalization.md`
- **DR-A5.3 (negative rates).** Use negative 10-year rates as observed. Do not floor at zero. Check that growth and inflation assumptions in that currency are correspondingly near zero or negative.
- **DR-A5.4 (maturity).** 10-year is the convention for going-concern valuation. Use a short rate only for a genuinely short-horizon analysis.

**Concepts:** `concepts/cost-of-equity/riskfree-rate-fundamentals.md`, `.../currency-riskfree-rate.md`, `.../riskfree-rate-normalization.md`, `concepts/cost-of-debt-capital/currency-conversion-of-discount-rates.md`

---

## A6 — Reference-table load

**Purpose:** load every `RT` dataset at one consistent `as_of` and record the vintage.

| Load | Datasets | Keyed by | Freshness limit (§7) |
|---|---|---|---|
| Risk premiums | `D-ERP`, `D-CTRY`, `D-SOVSPR` | date; country | ERP monthly; country tables semi-annual (January and July) |
| Credit | `D-RATE1`, `D-RATE2`, `D-RATE3`, `D-SPREAD`, `D-DEFPROB` | date; coverage bracket; rating | Spreads: **at the valuation date**. Brackets: stable across vintages |
| Industry | `D-INDUS`, `D-GLOB`, `D-CPXSEC`, `D-RDLIFE`, `D-MACRO` | industry name; SIC | Annual (January snapshot) |
| Pricing | `D-MULTREG`, `D-DISTRIB` | region; multiple | Annual |
| Corporate finance | `D-TAX`, `D-DEBTREG`, `D-PAYREG`, `D-DISTRESS` | country; region | Annual |
| Special situations | `D-ILLIQ`, `D-SURV` | — | Rarely refreshed |

**Decision rules**

- **DR-A6.1 (single vintage).** All `vintage-critical` tables must share one `as_of`. Mixing a 2021 riskfree rate with a 2013 country ERP table, or a current ERP with stale spreads, is a hard failure. `concepts/cost-of-debt-capital/default-spreads-over-time.md`
- **DR-A6.2 (staleness).** If any vintage-critical table is more than one year older than `valuation_date`, the collector attempts a refresh from the publisher; on failure, the run continues with `status: stale` and the report must disclose the vintage. `architecture/SPEC.md` §8.
- **DR-A6.3 (rating-label anomalies).** Some published synthetic-rating tables have non-monotonic labels or spreads below B3/B−. Reproduce the shipped table verbatim; do not silently "fix" it, but flag it. `concepts/cost-of-debt-capital/synthetic-rating.md`, `concepts/capital-structure/apv-approach.md`

**Concepts:** `concepts/cost-of-debt-capital/default-spreads-over-time.md`, `.../synthetic-rating.md`, `concepts/cost-of-equity/country-risk-premium.md`, `concepts/relative-valuation/industry-average-multiples.md`

---

## A7 — Ownership, governance and marginal-investor data

Required for `mode = corporate-finance` and for any run where the marginal-investor
question is live (private firms, closely held firms, family groups).

| Field | Units | Source | Freq | User? | Fallback |
|---|---|---|---|---|---|
| `ownership.institutional_pct_shares` | decimal | `M-OWN` | quarterly | Y | `D-INDUS`-style institutional-holdings-by-industry average |
| `ownership.institutional_pct_float` | decimal | `M-OWN` | quarterly | Y | Same |
| `ownership.insider_pct` | decimal | `M-OWN` / `F-PROXY` | quarterly | Y | Same |
| `ownership.individual_pct` | decimal | derived | quarterly | N | 1 − institutional − insider |
| `ownership.largest_holders[]` — name, %, type (index / activist / family / strategic) | mixed | `M-OWN` | quarterly | Y* | Empty; blocks the "largest ≠ marginal" test |
| `governance.board[]` — member, employee?, shares owned, other boards, tenure, age, attendance | mixed | `F-PROXY` | annual | Y* | Blocks the board table |
| `governance.exec_comp[]` — name, total comp, performance-linked share, tenure | mixed | `F-PROXY` | annual | Y* | Blocks the risk-incentive read |
| `governance.provisions` — staggered board?, majority vote?, poison pill?, dual-class?, golden shares? | booleans | `F-PROXY` / charter | event | Y* | Flag as unknown; do not assume absent |
| `governance.quickscore` — overall + 5 sub-scores | 1–10 | `E-GOV` | quarterly | Y | Skip; the red-flag checklist still runs |
| `peer_governance_averages` | mixed | peer set (A8) `F-PROXY` | annual | Y* | Skip the benchmark column |

**Decision rules**

- **DR-A7.1 (marginal investor).** High institutional share of float + low insider % → diversified marginal investor → CAPM with a **market beta** applies. Low institutional + high insider (founder/family who does not trade) → undiversified marginal investor → **total beta** required (branch C6 machinery even for a listed firm). Mixed → state the assumption explicitly and carry it as a sensitivity. `concepts/cost-of-equity/capm-cost-of-equity.md`, `concepts/deliverables-worked-examples/stockholder-analysis-marginal-investor.md`
- **DR-A7.2 (float artifacts).** Institutional-percent-of-float above 100% is a reporting artifact, not an error. Do not clamp.
- **DR-A7.3 (nominally institutional but undiversified).** A controlling stake held through a partnership or holding company is an undiversified holder even when classified as institutional.
- **DR-A7.4 (never take the score).** `governance.quickscore` is an input to the read, not the verdict. Both overriding a bad score (real mitigants exist) and confirming one (the policies are genuinely bad) are legitimate outcomes.

**Concepts:** `concepts/deliverables-worked-examples/governance-analysis-deliverable.md`, `.../stockholder-analysis-marginal-investor.md`, `concepts/governance-objective/ownership-and-control-structure-analysis.md`, `.../modified-objective-function.md`, `concepts/cost-of-equity/capm-cost-of-equity.md`

---

## A8 — Comparable-firm and peer-set data

Two distinct peer sets are needed and they are **not** interchangeable.

**Set 1 — Beta comparables** (for the bottom-up beta), one per business the firm operates in.

| Field | Units | Source | Freq | User? | Fallback |
|---|---|---|---|---|---|
| `beta_comps[].levered_beta` | decimal | `M-PX` regressions / `D-INDUS` | annual | Y* | Use `D-INDUS`/`D-GLOB` unlevered beta directly and skip firm-level assembly |
| `beta_comps[].market_de` | decimal | `M-PX` + `F-10K` | annual | Y* | Industry median market D/E from `D-INDUS` |
| `beta_comps[].marginal_tax_rate` | decimal | `D-TAX` | annual | Y | Domicile marginal rate |
| `beta_comps[].cash_to_firm_value` | decimal | `F-10K` + `M-PX` | annual | Y* | Skip the cash correction; flag |
| `beta_comps[].r_squared` | decimal | regression | annual | Y* | **Required** for total beta (C6); else BLOCK that branch |
| `beta_comps[].se_beta` | decimal | regression | annual | Y* | Cannot report the bottom-up standard error |

**Set 2 — Pricing comparables** (for relative valuation), defined by fundamentals, not by SIC code.

| Field | Units | Source | Freq | User? | Fallback |
|---|---|---|---|---|---|
| `price_comps[].market_cap`, `.net_debt`, `.cash`, `.enterprise_value` | ccy | `M-PX` + `F-10K` | quarterly | Y* | BLOCK for EV multiples |
| `price_comps[].revenues`, `.ebitda`, `.ebit`, `.net_income`, `.book_equity`, `.invested_capital` | ccy | `F-10K` | annual | Y* | BLOCK |
| `price_comps[].roe`, `.roic`, `.operating_margin`, `.net_margin` | decimal | derived | annual | N | — |
| `price_comps[].expected_growth` | decimal | `E-CONS` | quarterly | Y* | Fundamental growth (retention × ROE, or RIR × ROC) |
| `price_comps[].payout_ratio`, `.buybacks`, `.fcfe` | mixed | `F-10K` | annual | Y* | Blocks the payout peer analysis |
| `price_comps[].beta`, `.debt_to_capital`, `.effective_tax_rate` | decimal | mixed | annual | Y* | Industry averages |
| `price_comps[].std_dev_equity` | decimal | `M-PX` | annual | Y | `D-INDUS` |

**Decision rules**

- **DR-A8.1 (median, not mean).** Beta-comparable statistics use the **median**. A single comparable with a 500%+ or 3000% D/E destroys a mean. `concepts/cost-of-equity/non-traded-asset-betas.md`
- **DR-A8.2 (sample width).** Cast the beta comparable net wide — global, with a market-cap floor — because business risk travels across borders while country risk belongs in the premium. Ten to several hundred firms is normal. Standard error falls as `avg_SE / sqrt(n)`. `concepts/cost-of-equity/bottom-up-beta.md`
- **DR-A8.3 (banks).** For financial-service firms do **not** unlever. Use median **levered** comparable betas weighted by net revenues. `concepts/cost-of-equity/bottom-up-beta.md`
- **DR-A8.4 (pricing-peer definition).** A comparable is a firm with similar risk, growth and cash-flow characteristics — not a firm in the same sector. Record the screen (sector, geography, size floor, growth band) explicitly; it is the most challengeable part of the analysis. `concepts/relative-valuation/comparable-selection-and-controls.md`
- **DR-A8.5 (sample cleaning).** Drop firms where the multiple is not computable (negative earnings for PE, negative book value for PBV, negative EBITDA for EV/EBITDA) and **record the count**. If most of the universe drops out, the surviving sample is biased and any conclusion describes profitable survivors only. `concepts/relative-valuation/multiple-distribution-statistics.md`
- **DR-A8.6 (peer FCFE ≤ 0).** Report `NA`, never zero, for cash-return-to-FCFE at a peer with non-positive FCFE, and exclude it from the group statistic. `concepts/dividend-policy/peer-group-payout-analysis.md`

**Concepts:** `concepts/cost-of-equity/bottom-up-beta.md`, `.../non-traded-asset-betas.md`, `concepts/relative-valuation/comparable-selection-and-controls.md`, `.../multiple-distribution-statistics.md`, `concepts/dividend-policy/peer-group-payout-analysis.md`, `concepts/capital-structure/relative-and-regression-analysis.md`

---

# Part IV — Analysis-stage input contracts

Ten stages. Each names the fields it consumes (from Part III or from an earlier
analysis stage), the decision rules with thresholds, the validation it must pass, and
its concept files. These are the predicates behind gates G2–G8.

---

## B1 — Classification and routing

**Consumes:** A1 (all), A2 (`revenues` 5–10 yrs, `ebit`, `net_income`, sign history),
A3 (`segments`, `geography`, `rnd_history`), A4 (`price`, `issuer_rating`),
A5 (`sovereign.*` for operating countries), A7 (`ownership.*`).

**Produces:** `02-diagnosis/classification.json` — `life_cycle_stage`, `earnings_status`,
`sector_type`, `ownership`, `geography`, `distress_markers`, `intangible_intensity`,
`primary_path`, `overlays`, `constraints`.

**Decision rules with thresholds**

| Rule | Test | Route |
|---|---|---|
| DR-B1.1 sector | SIC/GICS in banks, insurers, brokers, or revenue reported as net interest income + net fee income | `sector_type = financial-service` → **branch C1**; constraints `no-fcff-valuation`, `no-optimal-debt-ratio` |
| DR-B1.2 earnings | `ebit ≤ 0` or `net_income ≤ 0` in the trailing 12 months | `earnings_status = negative` → constraints `no-earnings-multiple`, `no-standard-growth-model`; **branch C2** |
| DR-B1.3 cyclical trough | Pre-tax operating margin range across 3–5 yrs spans a factor of ~1.5 or more, or the firm is a commodity/cyclical producer | `require-normalized-earnings` → **branch C4** |
| DR-B1.4 distress | Market D/(D+E) high **and** (negative/marginal EBIT, or interest coverage < 1, or a distressed rating, or a bond trading far below par) | `distress_markers.present = true`; `require-failure-probability` → **branch C3** |
| DR-B1.5 equity-as-option | `earnings_status = negative` **AND** market debt-to-capital **> 50%** | Add the equity-as-call valuation alongside the DCF. `concepts/deliverables-worked-examples/equity-as-call-option-valuation.md` |
| DR-B1.6 high growth | Expected revenue growth **> 25%** | Revenue-driven forecast; `primary_path = revenue-driven` |
| DR-B1.7 private | No traded price series | `ownership = private` → **branch C6**; `require-total-beta` unless the buyer is diversified; `require-illiquidity-discount` unless the buyer is public and liquid |
| DR-B1.8 emerging market | Any operating country with a non-zero country risk premium in `D-CTRY` | Overlay `emerging-market` → **branch C5** |
| DR-B1.9 multi-business | More than one segment with a materially different business risk | Overlay `multi-business` → **branch C7** |
| DR-B1.10 intangible-heavy | R&D or brand advertising is a large share of operating income (market-wide R&D runs ~10.5% of operating income; computers ~50%, pharma high) | Overlay `intangible-heavy`; R&D capitalization is **mandatory before any valuation** |
| DR-B1.11 lease-heavy | Lease expense is a large share of operating income (market ~12.5%; furniture stores ~50%, apparel ~44%, restaurants ~27%) | Lease capitalization is load-bearing; the rating/lease iteration will bind |
| DR-B1.12 captive finance | A finance subsidiary with material finance receivables | Split the finance arm out; treat it on bank logic |

**Validation:** the routing must be internally consistent — a `financial-service` firm
cannot simultaneously carry `no-fcff-valuation` and a `standard-fcff` primary path.

**Concepts:** `concepts/dark-side-difficult/difficult-company-taxonomy.md`, `concepts/accounting-statements/life-cycle-patterns-in-financial-statements.md`, `.../sector-differences-in-financial-statements.md`, `concepts/deliverables-worked-examples/project-company-selection.md`, `concepts/dcf-model-choice-loose-ends/dcf-model-choice-framework.md`

---

## B2 — Statement normalization (cleaned financials)

**Consumes:** A2 (all), A3 (`lease.*`, `rnd_history`, `special_items`, `nol_carryforward`,
`cross_holdings`, `unusual_operating_classifications`), A6 (`D-RDLIFE`),
B4 (`pre_tax_cost_of_debt` — **circular**, see DR-B2.4).

**Produces:** `04-financials/cleaned-financials.json` — adjusted EBIT, adjusted net
income, invested capital, lease debt, research asset, normalized earnings, reinvestment,
FCFF, FCFE, ratio pack.

**Ordered procedure (order is load-bearing)**

1. **Update.** Rebuild trailing-12-month figures: `TTM = last 10-K annual − prior-year YTD + current-year YTD`. Required whenever the 10-K is more than one quarter old; prioritise for small, volatile, and recently restructured firms.
2. **Reclassify debt.** Move every interest-bearing short-term borrowing out of current liabilities before computing non-cash working capital.
3. **Capitalize leases.** PV the commitment schedule at the **pre-tax cost of debt** → lease debt, leased asset, straight-line depreciation over `5 + n₆`. Restate: EBIT `+= lease_expense − lease_depreciation`; debt `+= lease_debt`; invested capital `+= lease_asset`; interest expense `+= k_d × lease_debt`.
4. **Capitalize R&D.** Research asset `RA = Σ_{k=0..N} RD_k × (N−k)/N`; amortization `AM = Σ_{k=1..N} RD_k/N`. Restate: EBIT, net income and after-tax operating income each `+= (RD_0 − AM)` **untaxed**; book capital `+= RA`; cap ex `+= RD_0`; D&A `+= AM`.
5. **Strip one-time items,** subject to the recurrence test in DR-B2.2.
6. **Normalize** if the year is unrepresentative (branch C4).
7. **Recompute everything downstream:** effective tax rate, net cap ex, invested capital, ROIC, reinvestment rate, interest coverage.

**Decision rules with thresholds**

- **DR-B2.1 (what counts as debt).** Three-part test: contractually fixed payments, tax deductible, non-payment triggers default/loss of control. Debt = all interest-bearing liabilities (short and long) + **all** lease obligations + the straight-debt half of any convertible. Excludes payables, accruals, deferred taxes, minority interest. Preferred is a separate component. `concepts/cost-of-debt-capital/what-counts-as-debt.md`
- **DR-B2.2 (recurrence test).** Over a window of N ≥ 5 years compute `Frequency = years the item appears / N` and `Variability = sd(item) / mean|item|`. Treat as extraordinary **only if** Frequency is low **and** Variability is high. `Frequency = 1.0` → recurring, whatever it is called. For recurring-but-lumpy charges, deduct the multi-year average every year rather than excluding. `concepts/accounting-statements/extraordinary-items-and-pro-forma-earnings.md`, `concepts/dcf-cashflows-growth/reported-to-actual-earnings.md`
- **DR-B2.3 (tax rate).** Default to the **marginal** rate of the domicile from `D-TAX`. If starting from the effective rate, hold it years 1–5 and ramp linearly to marginal over years 6–10; terminal year uses marginal. Run the NOL waterfall: zero tax until the balance is exhausted, then partial tax in the crossover year, then full. **The same `t` must appear in the after-tax cost of debt.** `concepts/dcf-cashflows-growth/tax-rate-and-nols.md`
- **DR-B2.4 (the lease/rating circularity).** Lease debt needs `k_d`; `k_d` needs a rating; the rating needs lease-adjusted coverage; coverage needs lease debt. Solve by fixed-point iteration seeded at `riskfree + top-rating spread`. Cap iterations; on oscillation between adjacent brackets, take the worse rating. This loop exists only when the cost-of-debt route is `synthetic` **and** the firm has leases. `concepts/cost-of-debt-capital/wacc-calculator-workflow.md`
- **DR-B2.5 (working capital).** Non-cash WC = non-cash current assets − non-debt current liabilities. Forecast as a **percent of revenues**, triangulated across the current ratio, the firm's 3–5-yr average and the `D-INDUS` non-cash-WC/revenues figure. Never extrapolate last year's dollar change. Fade a large negative ratio toward zero. `concepts/dcf-cashflows-growth/non-cash-working-capital.md`
- **DR-B2.6 (net cap ex).** `Net cap ex = cap ex − depreciation + R&D − R&D amortization + normalized acquisitions − acquisition amortization`. Acquisitions must be **multi-year normalized**, never one year's figure. Acquisition amortization is usually already inside reported D&A — do not subtract twice. `concepts/dcf-cashflows-growth/net-capital-expenditures.md`
- **DR-B2.7 (aggressive-accounting screen).** Six signals. Flag on any one.
  1. Income from unspecified or unnamed sources.
  2. Income from asset sales or financial transactions at a **non-financial** firm.
  3. A sudden change in a standard expense item, such as a big drop in SG&A or R&D as a percent of revenues.
  4. Frequent accounting restatements.
  5. Accrual earnings persistently ahead of cash earnings.
  6. A large gap between tax-book income and reported income.

  This is an aggressiveness detector, not a fraud detector. `concepts/dcf-cashflows-growth/reported-to-actual-earnings.md`

**Validation**

| ID | Check | Action |
|---|---|---|
| V-B2.1 | Lease capitalization leaves **net income unchanged** | Failure = the lease payment was double-counted; BLOCK |
| V-B2.2 | R&D capitalization leaves **FCFF unchanged** (earnings and reinvestment rise by the same amount) | Failure = the add-back was tax-effected, the classic porting error; BLOCK |
| V-B2.3 | Every capitalization that changed earnings also changed invested capital | Failure silently corrupts ROIC and fundamental growth; BLOCK |
| V-B2.4 | Quality-of-earnings ratio `CFO / net income` computed and trended over 5+ years | Persistent sub-1 at a profitable firm with rising receivables = red flag; report |
| V-B2.5 | If the sector is commodity/oil, excise taxes stripped before revenues | Flag |
| V-B2.6 | If a bank: revenue built as net interest income + net fee income + trading income; credit-loss provision left as a recurring operating expense | Flag; route to C1 |

**Gate G3 passes when:** V-A2.1–V-A2.6 pass, all applicable capitalizations are applied
with their matching balance-sheet effects, invested capital and adjusted EBIT exist.

**Concepts:** `concepts/dcf-cashflows-growth/reported-to-actual-earnings.md`, `.../operating-lease-capitalization.md`, `.../rnd-capitalization.md`, `.../tax-rate-and-nols.md`, `.../net-capital-expenditures.md`, `.../non-cash-working-capital.md`, `.../fcff.md`, `.../fcfe.md`, `concepts/accounting-statements/potential-dividends-fcfe.md`, `.../earnings-versus-cash-flows.md`

---

## B3 — Cost of equity

**Consumes:** A5 (`riskfree.*`, `sovereign.*`, `inflation.*`), A6 (`D-ERP`, `D-CTRY`,
`D-HIST`), A3 (`geography`, `production_by_country`, `segments`), A8 (Set 1),
A7 (`ownership.*`), B2 (market D/E, marginal tax rate, cash/firm value).

**Produces:** riskfree rate with derivation, ERP build-up, unlevered and levered beta
with standard error, cost of equity — plus divisional versions where C7 applies.

**Inputs and their fallback ladders**

| Field | Primary | Fallback 1 | Fallback 2 | User? |
|---|---|---|---|---|
| `riskfree_rate` | DR-A5.1 ladder | Build-up (inflation + real rate) | Differential inflation from US$ | Y |
| `mature_market_erp` | Current implied ERP from `D-ERP` | Average implied ERP over a stated window (1960–present, or 10-yr) | Historical **geometric, stocks−T.Bonds, longest window** from `D-HIST` | Y |
| `country_risk_premium[country]` | `D-CTRY` lookup on the **local-currency** Moody's rating | `sovereign_default_spread × relative_equity_volatility_multiplier` computed from `M-CDS` or hard-currency bond spread | PRS composite score → ERP mapping for unrated countries | Y |
| `operation_weights[country]` | Revenue share from `F-SEG` | Production share | Asset share | Y |
| `unlevered_beta[business]` | Median comparable levered beta / (1+(1−t)·median D/E), cash-corrected | `D-INDUS` / `D-GLOB` unlevered beta for the industry | — | Y |
| `business_value_weights` | Segment revenue × peer EV/Sales from `D-INDUS` | Segment revenue share | Segment operating income share | Y |
| `market_de` | Market debt (incl. leases) / market equity | Industry median market D/E (`D-INDUS`) — **mandatory for private firms** | — | Y |
| `lambda` (country-risk exposure) | Return regression on the sovereign bond | Firm domestic revenue % / average local firm domestic revenue % | 1.0 | Y |
| `r_squared_median` (comparables) | Beta regressions across the comparable set | `D-INDUS` implied | — | Y* |

**Decision rules with thresholds**

- **DR-B3.1 (ERP choice).** Default = **current implied ERP**. Use a historical premium only if you assert mean reversion, and if you do, use geometric, stocks-over-T.Bonds, over the longest window — never arithmetic stocks-over-T.Bills. Always compute the current implied premium anyway; the gap between it and your choice is the size and direction of the bias you are introducing. `concepts/cost-of-equity/choosing-an-equity-risk-premium.md`
- **DR-B3.2 (ERP cross-checks).** (a) `ERP / Baa spread` should sit near its long-run median of ~2.0. (b) `riskfree + ERP` = expected return on stocks; check plausibility. Large deviations require an explanation in the report.
- **DR-B3.3 (country risk attachment).** Rating **Aaa/AAA** → CRP = 0, stop. Otherwise `CRP = default_spread × relative_equity_volatility_multiplier` (a uniform multiplier in the production table; country-specific σ_equity/σ_bond in the melded method). Attach it by **operation weights**, not by country of incorporation. Choose exactly one attachment mechanism: additive (constant exposure), through beta, or through lambda. `concepts/cost-of-equity/country-risk-premium.md`, `.../operation-weighted-erp.md`, `.../lambda-country-risk-exposure.md`
- **DR-B3.4 (beta source).** Bottom-up is the production estimate. The regression beta is a **diagnostic only**. Report the regression's beta, intercept, R², standard error and t-statistic, and the derived Jensen's alpha, but do not feed the regression beta into the cost of equity by default. `concepts/cost-of-equity/bottom-up-beta.md`, `.../regression-beta.md`
- **DR-B3.5 (unlever at the right D/E).** If a regression beta must be unlevered, use the **average D/E over the regression window**, not today's.
- **DR-B3.6 (cash correction).** `business_unlevered_beta = company_unlevered_beta / (1 − cash/firm value)`. Apply when the comparable set is cash-rich. Alternatively use the net-debt convention — but then use net debt everywhere (R5).
- **DR-B3.7 (total beta trigger).** Marginal investor undiversified → `total beta = market beta / sqrt(median comparable R²)`. Sector correlation with the market runs near 0.5, so total betas run near twice market betas. Do not stack total beta with a small-cap premium or with an illiquidity discount without checking overlap. `concepts/cost-of-equity/total-beta.md`
- **DR-B3.8 (Jensen's alpha).** `alpha = intercept − Rf_period × (1 − beta)`, where `Rf_period` is the **average riskfree rate over the regression window**, converted to the return interval (÷12 monthly, ÷52 weekly). Not today's rate; not compared to zero. `concepts/cost-of-equity/jensen-alpha.md`

**Validation:** currency of `riskfree_rate` = mandate currency; ERP vintage = country-table
vintage = spread-table vintage; N2 (country risk counted once); R5 (debt convention).

**Concepts:** `concepts/cost-of-equity/cost-of-equity-assembly.md` and the full area index.

---

## B4 — Cost of debt, weights and cost of capital

**Consumes:** A3 (`debt.*`, `lease.*`), A4 (`traded_bonds`, `issuer_rating`, `preferred.*`,
`convertible.*`), A5 (`riskfree`, `sovereign`), A6 (`D-RATE1/2/3`, `D-SPREAD`, `D-TAX`),
B2 (adjusted EBIT, adjusted interest, invested capital), B3 (cost of equity).

**Produces:** `05-capital/cost-of-capital.json`.

**Cost-of-debt route ladder (DR-B4.1)**

| Priority | Condition | Route | Inputs required |
|---|---|---|---|
| 1 | Liquid, long-term, **straight** bond outstanding | YTM on that bond | bond price, coupon, maturity |
| 2 | Rated by a global agency | `riskfree + D-SPREAD[median rating]` | median issuer/issue rating, current spread table |
| 3 | Unrated, recent long-term bank borrowing | Loan rate | loan rate + date (recency matters) |
| 4 | Otherwise (private firm, division, unrated) | Synthetic rating | adjusted EBIT, adjusted interest expense, firm class, spread table |
| 5 | Local-scale agency rating only | `riskfree + λ × country_default_spread + company_spread` | local rating, sovereign spread, λ |
| — | Financial-service firm | Actual rating, or `D-RATE3` on **long-term interest expense only** | Never the ordinary coverage table |

**Decision rules with thresholds**

- **DR-B4.2 (firm class for the synthetic table).** Market cap **> ~$5 billion** and a conventional operating business → `D-RATE1` (large/stable). Below that, or young/cyclical/volatile/private → `D-RATE2` (small/risky, which demands materially higher coverage for the same rating). Banks/insurers → `D-RATE3`. The $5bn line is a guide, not a law. `concepts/cost-of-debt-capital/synthetic-rating.md`
- **DR-B4.3 (coverage clamps).** Interest = 0 with positive EBIT → coverage = +∞ → top rating. Negative EBIT → negative coverage → bottom bracket (D). Table bounds are ±100,000.
- **DR-B4.4 (emerging-market coverage scaling).** If local long-term rates far exceed US rates, divide the coverage ratio by `k = local long-term rate / US long-term rate` before the table lookup. `concepts/cost-of-debt-capital/interest-coverage-ratio.md`
- **DR-B4.5 (country risk in the cost of debt).** Global-agency rating → country risk is **already inside** it; add only the company spread. Local-scale rating → add `λ × sovereign spread` separately. λ near 1.0 for a small domestic firm; below 1.0 for a large exporter, calibrated to traded bond spreads of comparable large domestic issuers. `concepts/cost-of-debt-capital/country-risk-in-cost-of-debt.md`
- **DR-B4.6 (synthetic vs actual).** When both exist and are credible, use the **actual** rating and use the synthetic as a diagnostic. Explain the gap: normalized-vs-current earnings, sector rating conventions, country-risk drag, uncapitalized off-balance-sheet obligations. `concepts/cost-of-debt-capital/synthetic-vs-actual-rating.md`
- **DR-B4.7 (subsidized debt).** Use the **fair** rate in the cost of capital and value the subsidy separately as `(fair − subsidized) × principal`, after tax, over the remaining life. Never let a subsidized rate lower the hurdle rate for new projects. `concepts/cost-of-debt-capital/subsidized-debt.md`
- **DR-B4.8 (market value of debt).** Treat total book debt as one coupon bond: `MV = interest_expense × annuity(k_d, M) + book_debt / (1+k_d)^M`, with `M` = weighted-average maturity, **default 3 years**, and `k_d` = the **current pre-tax** cost of debt (never the historical coupon rate, which returns book by construction). Then add capitalized lease debt and the straight-debt half of any convertible. `concepts/cost-of-debt-capital/market-value-of-debt.md`
- **DR-B4.9 (convertible split).** Straight-debt value = coupon annuity + discounted face at the **straight-bond rate for that rating**, not the convertible's own low coupon. Option portion = market value − straight-debt value, and it belongs in market capitalization. Sanity check: option value must be positive. `concepts/cost-of-debt-capital/convertible-debt-decomposition.md`
- **DR-B4.10 (preferred).** `k_ps = annual dividend per share / market price per preferred share`; **no (1−t) factor**. Keep as a third component when `PS/(D+E+PS) ≥ 5%`; below that, lumping with debt is acceptable and must be stated. `concepts/cost-of-debt-capital/preferred-stock-cost.md`
- **DR-B4.11 (weights).** Market values only. Equity = shares × price (+ the convertible's option half). Debt = market debt + lease debt + convertible straight half. The D/E used to lever the beta **must equal** the D/(D+E) in the weights. `concepts/cost-of-debt-capital/market-value-weights.md`
- **DR-B4.12 (currency conversion).** `Rate_local = (1 + Rate_USD) × (1 + inflation_local) / (1 + inflation_USD) − 1`, applied to the cost of equity, cost of debt or the assembled WACC. Cross-check by rebuilding directly off the local riskfree rate; agreement within ~20 bps is the test. `concepts/cost-of-debt-capital/currency-conversion-of-discount-rates.md`

**Pipeline order (DR-B4.13, from the WACC calculator workflow)**

1. Market value of equity → 2. Lease capitalization at `k_d` → 3. Lease-adjusted EBIT and interest → 4. Coverage → 5. Synthetic rating and spread → `k_d` (**iterate 2–5 to a fixed point**) → 6. Market value of straight debt → 7. Convertible split → 8. Aggregate MV debt / MV preferred → 9. Levered beta → 10. ERP → cost of equity → 11. After-tax `k_d`, cost of preferred → 12. Total capital and weights → 13. WACC.

**Validation:** R1 (currency), R5 (gross/net), same `t` in beta relevering and after-tax
`k_d`, same D/E in beta and weights, N1 (tax shield not in FCFF), preferred and leases
present in the capital base, spread vintage = ERP vintage.

**Gate G4 passes when:** WACC exists, its `currency` field equals the mandate currency,
and all of the above validations pass.

**Concepts:** `concepts/cost-of-debt-capital/cost-of-capital-assembly.md`, `.../wacc-calculator-workflow.md`, `.../hurdle-rate-choice.md`, and the full area index.

---

## B5 — Growth and forecast drivers

**Consumes:** B2 (adjusted EBIT, invested capital, reinvestment, ROIC, tax path),
A2 (5–10 yr revenue/EBIT/net income history), A6 (`D-INDUS`, `D-CPXSEC`),
`E-CONS`, `E-MKT`, A5 (riskfree — the terminal cap), narrative drivers.

**Produces:** `06-intrinsic/forecast.json` — per-year revenue growth, operating margin,
tax rate, reinvestment (or sales-to-capital), cost of capital; plus the terminal block.

**Growth-source hierarchy (DR-B5.1), in ascending order of reliability**

| Source | Inputs | When usable | Trust |
|---|---|---|---|
| Historical | Revenue/EBIT/EPS series | Base is positive and the firm has not been scaling from a tiny base | Starting point only |
| Analyst consensus | `E-CONS` 5-yr EPS growth + dispersion | Large firms, short horizons | Input, not answer. It is **EPS** growth — never drop it into an FCFF model |
| Fundamental | Reinvestment rate × ROC (firm) or retention × ROE (equity) | Positive, stable returns | **Default** |
| Revenue-driven | Market size, market share, target margin, sales-to-capital | Negative earnings **or** changing margins | Mandatory when fundamentals break |

**Decision rules with thresholds**

- **DR-B5.2 (historical growth hygiene).** Compute arithmetic mean, geometric mean and the standard deviation of annual changes. If the standard deviation is large, discard the arithmetic mean. If the base is negative, the growth rate **cannot be estimated** — stop and switch route. Test for the scaling effect: monotonically declining year-by-year growth means the window average is an artifact. Always run the extrapolation plausibility test (compound five years forward and compare the level to the addressable market). `concepts/dcf-cashflows-growth/historical-growth.md`
- **DR-B5.3 (matched pairs).** Never mix rows: EPS ↔ retention ratio ↔ ROE; net income from non-cash assets ↔ equity reinvestment rate ↔ non-cash ROE; operating income ↔ reinvestment rate ↔ ROC. `concepts/dcf-cashflows-growth/fundamental-growth-equity.md`
- **DR-B5.4 (ROIC before growth).** Run the six-distortion checklist on ROIC — abnormal earnings, accounting misclassification (R&D/leases), unusual items, life-cycle effect, write-offs shrinking the capital base, inflation on old book values — before any growth rate built on it is trusted. Measure on **beginning-of-period** capital. `concepts/dcf-cashflows-growth/return-on-invested-capital.md`
- **DR-B5.5 (value of growth test).** Growth adds value only when ROIC on **new** investment exceeds the cost of capital. At `ROIC = WACC`, growth is value-neutral at any rate. Below, growth destroys value. Compute the no-growth benchmark `EBIT(1−t)/WACC` and the value added by growth; compare with the market's implied price of growth. `concepts/dcf-cashflows-growth/value-of-growth.md`
- **DR-B5.6 (revenue-driven inputs).** Six inputs, all required. Total addressable market size and its growth rate (`E-MKT`). Target market share at explicit milestone years. A **target operating margin** anchored on **mature firms with the same business model** — state which peer percentile. A margin convergence path: linear to a stated year, or a speed-of-convergence parameter. A **sales-to-capital ratio** from `D-INDUS`, which may vary by phase. The NOL balance. `concepts/dcf-cashflows-growth/top-down-revenue-growth.md`
- **DR-B5.7 (structural forecast conventions).** 10-year explicit forecast; growth constant years 2–5 then linear fade to terminal over 6–10; tax constant years 1–5 then five equal steps to marginal; cost of capital constant years 1–5 then linear fade to terminal. **Discount with the cumulative product of year-specific rates**, never a constant WACC. `concepts/dcf-cashflows-growth/fcff-forecast-engine.md`
- **DR-B5.8 (growth-pattern / stage count).** Growth at or below the economy's rate, or a regulated firm → **stable, single stage**. Growth ≤ `g_econ + 10%`, or a finite-life moat → **2-stage**. Growth > `g_econ + 10%`, or strong barriers to entry → **3-stage / n-stage**. `concepts/dcf-model-choice-loose-ends/growth-pattern-and-stage-count.md`
- **DR-B5.9 (model choice).** FCFE when leverage is low and **stable**; FCFF when leverage is changing or leverage information is partial. Dividends only when FCFE cannot be estimated (banks) or when the dividend passes the payout screen. `concepts/dcf-model-choice-loose-ends/equity-versus-firm-valuation.md`
- **DR-B5.10 (dividends vs FCFE screen).** Over five years, if dividends fall between **80% and 110%** of FCFE, the DDM is acceptable; outside that band use FCFE. Bank and private/IPO exceptions apply. `concepts/dcf-model-choice-loose-ends/dividends-versus-fcfe.md`

**Validation (gate G5)**

| ID | Check |
|---|---|
| V-B5.1 | `g = reinvestment rate × ROIC` holds in every explicit year, or the model uses sales-to-capital and the implied ROIC path is reported |
| V-B5.2 | Implied **marginal ROIC** over the forecast is plausible against the firm's own history and the industry average |
| V-B5.3 | Absolute revenue level in the terminal year is plausible against market size and against the largest incumbents |
| V-B5.4 | Growth rate does not exceed the addressable market's implied ceiling |
| V-B5.5 | Reinvestment and growth are not set independently anywhere in the model |
| V-B5.6 | Working capital is not double-counted alongside a sales-to-capital reinvestment |
| V-B5.7 | NOL balance is not extended into the terminal year |

**Concepts:** `concepts/dcf-cashflows-growth/fundamental-growth-operating.md`, `.../fundamental-growth-equity.md`, `.../historical-growth.md`, `.../analyst-growth-estimates.md`, `.../top-down-revenue-growth.md`, `.../value-of-growth.md`, `.../fcff-forecast-engine.md`, `concepts/dcf-model-choice-loose-ends/growth-pattern-and-stage-count.md`, `.../multistage-model-mechanics.md`

---

## B6 — Terminal value

**Consumes:** A5 (`riskfree` in the valuation currency), B3/B4 (terminal beta, debt
ratio, cost of capital), B5 (terminal growth, terminal ROC), A6 (`D-INDUS` for mature
industry norms).

| Field | Units | Source | User? | Fallback / default |
|---|---|---|---|---|
| `terminal_growth` | decimal | judgment, **capped** | Y* | Riskfree rate in the valuation currency; may be lower, may be negative |
| `terminal_roc` | decimal | judgment | Y* | **Terminal cost of capital** (makes terminal growth value-neutral by construction) |
| `terminal_beta` | decimal | convention | Y | **1.00** |
| `terminal_debt_ratio` | decimal | judgment | Y | Industry / mature-company average from `D-INDUS` |
| `terminal_cost_of_capital` | decimal | derived | N | `riskfree + mature-market ERP` |
| `terminal_reinvestment_rate` | decimal | **derived, never assumed** | N | `g / ROC` (firm) or `1 − g/ROE` payout (equity) |
| `growth_period_length N` | years | judgment | Y* | 5 for mature, 10 for growth; tie to the durability of the moat, not to a spreadsheet's column count |

**Decision rules with thresholds**

- **DR-B6.1 (hard cap).** `terminal_growth ≤ riskfree rate` in the valuation currency. Universal constraint (`no-perpetual-growth-above-riskfree`). Pairing high `g` with a low riskfree rate systematically overvalues.
- **DR-B6.2 (earned growth).** Terminal reinvestment = `g/ROC`. The "cap ex = depreciation, no working-capital needs" assumption is consistent **only with roughly zero real growth**.
- **DR-B6.3 (excess returns).** `ROC = WACC` in perpetuity is the neutral default. Allowing `ROC > WACC` forever asserts a permanent moat and must be argued in the report. Empirically, fade **growth faster than excess returns** — median ROIC persists in an 8–12% band over decades while real revenue growth declines toward GDP growth.
- **DR-B6.4 (mature on every dimension).** Beta → 1.00; debt ratio → industry norm; country risk premium fades; cost of capital → mature level.
- **DR-B6.5 (reverse check, mandatory).** `embedded reinvestment rate = 1 − FCFF_terminal/EBIT(1−t)_terminal`; `implied perpetual ROIC = g / embedded reinvestment rate`. Report it. A valuation that ships without anyone having looked at its implied perpetual ROIC is incomplete.
- **DR-B6.6 (exit multiples).** Using an exit multiple converts the intrinsic valuation into a relative valuation. Permitted only if labelled as such.

**Concepts:** `concepts/dcf-cashflows-growth/terminal-value.md`, `.../return-on-invested-capital.md`, `.../value-of-growth.md`

---

## B7 — Equity bridge and per-share value

**Consumes:** DCF operating-asset value; A2/A3 (cash, cross-holdings, non-operating
assets, pension, contingencies, NCI); A4 (`shares_outstanding`, volatility, `options.*`);
B4 (market value of debt).

| Bridge line | Field(s) | Source | User? | Default / open question |
|---|---|---|---|---|
| + Cash | `cash_and_equivalents + short_term_investments + marketable_securities` | A2 | Y | Full face value. Trapped-cash haircut: `cash − trapped × (marginal − foreign tax rate)`; operating cash belongs in working capital, only the excess is added back |
| + Cross-holdings | `cross_holdings[]` valued | A3 + `M-PX` | Y* | Market value for listed stakes; price-to-book approximation otherwise; carrying value as last resort |
| + Other non-operating assets | overfunded pension, unutilised assets | A3 | Y | 0. **Never** brand value, goodwill, or operating PP&E |
| − Debt | market value of debt incl. leases | B4 | N | **State whether the bridge uses book or market debt and make it consistent with the WACC weights** |
| − Other claims | pension underfunding, expected value of contingent liabilities, minority interests | A3 | Y* | 0, flagged |
| − Equity options | `options.*` valued | A3 + A4 | Y | Dilution-adjusted Black-Scholes; iterate the circularity |
| ÷ Shares | `shares_outstanding` (**actual**, not diluted) | A4 | Y | BLOCK |
| Per-share discounts | illiquidity, minority | branch C6 | Y* | None for a listed firm with a diversified buyer |

**Decision rules**

- **DR-B7.1 (employee option inputs).** `S` = current price adjusted for dilution (iterate `S_adj = (S·n_shares + C·n_options)/(n_shares + n_options)`); `K` = weighted-average exercise price; `T` = **expected** life, shortened from contractual to reflect early exercise; `σ` = stock volatility (or industry std dev); `y` = dividend yield; `r` = riskfree. Multiply by the vesting probability if a material share is unvested; multiply by `(1 − t)` if exercise creates a tax deduction. `concepts/dcf-model-choice-loose-ends/valuing-employee-options.md`
- **DR-B7.2 (N3 enforcement).** Subtract option value **and** divide by actual shares; or use diluted shares and subtract nothing. Never both.
- **DR-B7.3 (cash treatment).** Enforce N4: if interest income is inside the cash flows, the beta must be the cash-diluted whole-company beta and cash is **not** added back.
- **DR-B7.4 (complexity discount).** At most one channel (N8). Inputs: disclosure page count / weighted complexity score; the price-to-book regression on opacity.

**Gate G6 passes when:** every bridge line has a value or an explicit zero-with-reason,
N3/N4/N5 hold, and value per share exists.

**Concepts:** `concepts/dcf-model-choice-loose-ends/equity-value-bridge.md`, `.../cash-in-valuation.md`, `.../marginal-value-of-cash.md`, `.../cross-holdings.md`, `.../other-non-operating-assets.md`, `.../debt-and-other-claims-in-the-bridge.md`, `.../employee-option-per-share-approaches.md`, `.../valuing-employee-options.md`, `.../restricted-stock-and-future-grants.md`, `.../complexity-discount.md`

---

## B8 — Relative valuation

**Consumes:** A8 Set 2, A6 (`D-INDUS`, `D-GLOB`, `D-MULTREG`, `D-DISTRIB`), A4 (price,
shares, EV components), B2 (cleaned fundamentals), `E-CONS`.

**Per-multiple input requirements**

| Multiple | Numerator | Denominator | **Companion variable (mandatory control)** | Secondary controls |
|---|---|---|---|---|
| PE (current / trailing / forward) | market cap | earnings on the matching basis | expected growth | payout, beta |
| PEG | PE | expected EPS growth in percentage points | risk, payout, **level** of growth (regress on `ln(growth)`) | — |
| PBV | market cap | book equity | **ROE** | growth, beta |
| EV/Invested Capital | EV | book equity + book debt − cash | **ROIC** | debt ratio, growth |
| EV/EBITDA | EV | EBITDA | **reinvestment needs (CapEx/EBITDA)** | tax rate, cost of capital, debt ratio |
| EV/Sales, P/S | EV / market cap | revenues | **after-tax operating margin** / net margin | RIR, growth, WACC |

**Decision rules with thresholds**

- **DR-B8.1 (definitional tests).** Numerator and denominator must belong to the same claimholders. `Price/EBITDA` is rejected outright. Fix the timing variant (current / trailing / forward) and use it for **every** firm in the set. Fix the share-count convention. Net cash out of EV. Correct for minority interests when a partly-owned subsidiary is consolidated. `concepts/relative-valuation/multiple-definition-tests.md`
- **DR-B8.2 (distribution first).** Compute median and the 10/25/75/90 percentiles from `D-DISTRIB` or from the pulled sample. Use the **median**, never the mean — these distributions are heavily right-skewed. Record how many firms had no computable value. Fixed thresholds ("under 6x EBITDA is cheap") are forbidden without a current, regional distribution check. `concepts/relative-valuation/multiple-distribution-statistics.md`
- **DR-B8.3 (control technique by dimension count).** Zero differing dimensions → direct comparison. One → story telling or a modified multiple (and PEG does **not** neutralise growth). Several → regression. Several is the normal case. `concepts/relative-valuation/comparable-selection-and-controls.md`
- **DR-B8.4 (regression usability).** t-statistic **> 2** good, **1–2** marginal, **< 1** noise → drop the variable. R² **< ~15%** → the prediction is weak evidence; say so. Negative intercepts can produce negative predicted multiples; the through-origin refit is an imperfect fix. Check the correlation matrix — wrong-sign coefficients are usually multicollinearity, not a finding. `concepts/relative-valuation/market-wide-regressions.md`, `.../sector-regressions.md`
- **DR-B8.5 (units).** The slide-form regional regressions in `D-MULTREG` take growth, payout, ROE, ROIC, margins, tax rates and debt ratios as **decimals**. The SPSS-form US regressions take payout and growth as absolute percent. Record which form the loaded coefficients use; this is a silent factor-of-100 error otherwise. `concepts/relative-valuation/cross-market-multiple-regressions.md`
- **DR-B8.6 (young/money-losing sector).** If a regression of the multiple on its conventional companion variable produces a near-zero R² and an insignificant slope, current fundamentals are uninformative. Three replacement routes:
  1. **Survival-and-growth proxies** — regress the multiple on `ln(revenues)`, revenue growth and cash/revenues.
  2. **Forward multiple with the full haircut sequence.** Value in year N. Discount at the **risk-adjusted cost of capital**, never the riskfree rate. Subtract expected dilution from new equity. Multiply by (1 − failure probability). Adjust for debt and cash. Subtract the option overhang. Skipping any step overstates value, usually by a large factor.
  3. **Market-implied pricing metric** — correlate market cap and EV against every candidate operating metric and price on the winner.

  `concepts/relative-valuation/pricing-young-companies.md`
- **DR-B8.7 (region assignment).** Assign a multinational to a region by operations, not by listing venue.
- **DR-B8.8 (verdict language).** A relative verdict is always relative. "Cheap versus this comparable group" is never "undervalued". `concepts/relative-valuation/pricing-vs-value.md`

**Concepts:** the full `concepts/relative-valuation/` index, plus `concepts/deliverables-worked-examples/relative-valuation-comparables-regression.md`, `.../market-wide-multiple-regression.md`

---

## B9 — Capital structure optimization

Runs in `mode = corporate-finance`, `restructuring`, and wherever value-of-control is
computed. **Blocked** for financial-service firms (branch C1).

**Consumes:** B2 (lease-adjusted EBIT, EBITDA, depreciation, cap ex, ΔWC, invested capital),
B3 (unlevered beta), B4 (riskfree, ERP, marginal tax rate, market equity, market debt,
cash), A6 (`D-RATE1/2`, `D-SPREAD`, `D-DEFPROB`, `D-DISTRESS`, `D-DEBTREG`, `D-TAX`),
A2 (10-yr EBIT history for volatility).

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `unlevered_beta` | decimal | B3 | Y | `D-INDUS` |
| `ebit_lease_adjusted`, `ebitda`, `depreciation`, `capex`, `delta_wc` | ccy | B2 | Y | BLOCK |
| `total_capital` (E + D, held constant across the grid) | ccy | B4 | N | — |
| `marginal_tax_rate` | decimal | `D-TAX` | Y | Domicile statutory rate |
| `interest_deductibility_cap` | rule | tax code | Y | Post-2017 US: 30% of EBITDA through 2022, 30% of EBIT thereafter |
| `ebit_history[10y]` → `sd(%ΔEBIT)` | decimal | A2 | Y* | Industry earnings-variance table; blocks the stress test |
| `bankruptcy_cost_pct` | decimal | judgment | Y | Direct costs empirically 5–10% of firm value; worked examples use **25%** total |
| `distress_severity` | enum Low/Med/High | judgment | Y | Medium |
| `implied_growth` | decimal | derived | N | `(EV × WACC_current − FCFF) / (EV + FCFF)`, capped at the riskfree rate for the incremental method |
| `rating_constraint` | rating symbol or none | management | Y | None |

**Decision rules with thresholds**

- **DR-B9.1 (the grid).** Debt ratio from **0% to 90% in 10% steps**. 100% is undefined (D/E infinite). At each level: relever beta with the **tax rate actually used at that level**, solve the rating circularity, apply the tax cap, compute WACC and firm value. `concepts/capital-structure/cost-of-capital-approach.md`
- **DR-B9.2 (tax cap).** `t_EBIT = t` if interest ≤ EBIT else `t × EBIT/interest`; `t_cap = t` if interest ≤ 0.30 × M else `t × (0.30 × M)/interest`; `t_used = min(t_EBIT, t_cap)`. **Relever beta with `t_used`, not the headline rate** — this is why high-leverage betas rise faster than a constant-`t` calculation implies. `concepts/capital-structure/tax-benefit-of-debt.md`
- **DR-B9.3 (selection objective).** With no indirect bankruptcy costs, `argmin WACC` = `argmax value`. With the enhanced approach on (EBITDA haircut by rating), operating income varies with the debt ratio, so select on **maximum firm value only**. `concepts/capital-structure/enhanced-cost-of-capital-approach.md`
- **DR-B9.4 (value of the move).** Report **both** methods: incremental (`annual saving = EV × ΔWACC`, capitalized at `WACC_new − riskfree`) and full revaluation (`FCFF(1+g)/(WACC_new − g)` at the price-implied `g`). They can differ by a factor of two. `concepts/capital-structure/recapitalization-and-buyback-price.md`
- **DR-B9.5 (rational buyback price).** `rational price = current price + value gain/shares`. Verify the fixed point: buying back at that price must reproduce it as the post-buyback value per share.
- **DR-B9.6 (downside).** One protection only (N7). Either re-run the grid at EBIT haircuts of 10%…60% (or EBIT − 3 s.d.) and report where the optimum first moves, **or** impose a rating floor and price it as `value at unconstrained optimum − value at the constrained ratio`.
- **DR-B9.7 (benchmarks).** Compare the current ratio to the peer group average (book, market, and net versions) and to the `D-DEBTREG` predicted ratio. Neither is an optimum; a market-wide regression with R² near 8% describes typical behaviour, not value maximization. `concepts/capital-structure/relative-and-regression-analysis.md`
- **DR-B9.8 (APV cross-check).** `V = V_unlevered + Σ tax benefits − Σ expected bankruptcy costs`, with default probabilities from `D-DEFPROB`. State which base the bankruptcy cost percentage is applied to and keep it consistent. `concepts/capital-structure/apv-approach.md`
- **DR-B9.9 (use of proceeds is irrelevant).** The optimal ratio is a function of business risk and the tax rate. It does not change with whether the money funds buybacks or projects, provided the business mix and tax rate are unchanged.

**Concepts:** the full `concepts/capital-structure/` index, plus `concepts/deliverables-worked-examples/qualitative-debt-tradeoff.md`, `.../optimal-debt-ratio-wacc-schedule.md`, `.../recapitalization-value-and-stress-test.md`, `.../debt-design-deliverable.md`

**Debt-design sub-inputs (Part VII of the corporate finance deliverable)**

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `macro_regressions.firm` (ΔV and ΔOI on Δrates, %ΔGDP, Δinflation, %Δdollar) | slopes + t-stats | A2 + `X-FRED` | Y* | If t-stat < 2, **discard** and use `D-MACRO` sector coefficients weighted by business value |
| `project_duration` | years | PV-weighted project cash flows | Y | Firm-level duration from the interest-rate slope, floored at 0 |
| `currency_mix_target` | decimal shares | revenue geography (A3) | Y | Match to where revenues arise, not to the listing venue |
| `pricing_power` | qualitative | business analysis | Y* | No default; drives fixed-vs-floating and has no number attached |

---

## B10 — Payout policy

**Consumes**
- A2 — 5–10 years of net income, cap ex, depreciation, ΔWC, net debt issued, dividends, buybacks, equity issuance
- A4 — price and dividend history. B3 — cost of equity and beta. B4 — debt ratio
- A5 — annual riskfree and market returns for the CAPM required-return series
- A6 — `D-PAYREG`, `D-INDUS`. A8 — peer payout data

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `net_income[t]`, `capex[t]`, `depreciation[t]`, `delta_wc[t]`, `net_debt_issued[t]` | ccy | A2 | Y | BLOCK |
| `dividends[t]`, `buybacks[t]`, `equity_issued[t]` | ccy | A2 | Y | 0 |
| `debt_ratio` (for the target-ratio FCFE variant) | decimal | B4 | Y | Current market debt-to-capital |
| `book_equity[t]` | ccy | A2 | Y | BLOCK for ROE |
| `riskfree[t]`, `market_return[t]` (annual, over the window) | decimal | A5 / `M-IDX` | Y | Blocks Jensen's alpha; the ROE-vs-COE leg still runs |
| `beta` | decimal | B3 | Y | — |
| `peer_payout`, `peer_yield`, `peer_fcfe` | decimal / ccy | A8 | Y* | `D-INDUS` payout ratio |
| `payout_regression_coefficients` | mixed | `D-PAYREG` | Y | Skip the market benchmark |
| `expected_growth` (for the regression) | decimal | `E-CONS` | Y | Fundamental growth |

**Decision rules with thresholds**

- **DR-B10.1 (three FCFE variants, always).** Pre-debt (`NI − net cap ex − ΔWC`), actual-debt (`+ net debt issued`), and target-debt-ratio (`NI − (1−DR)(net cap ex + ΔWC)`). **Report all three.** Lead with the target-ratio variant when actual debt flows are lumpy; the verdict can flip between them. `concepts/dividend-policy/fcfe-potential-dividends.md`
- **DR-B10.2 (cash returned).** Always `dividends + buybacks`, net of equity issuance where a large stock-compensation programme exists. Dividend-only analysis mis-ranks US firms by a factor of two or more. Add buybacks on **both** sides of any FCFE comparison. `concepts/dividend-policy/cash-returned-dividends-and-buybacks.md`
- **DR-B10.3 (trust axis).** `ROE − cost of equity` (project quality) and `Jensen's alpha` (market verdict). Both positive → high trust, flexibility earned. Both negative → low trust. Mixed → weight the project measure for the payout decision and say so. `concepts/dividend-policy/cash-trust-assessment.md`
- **DR-B10.4 (matrix placement).** Cash surplus/deficit × good/poor projects. State the FCFE variant used, because it determines the column. In the deficit quadrants, sequence correctly: with poor projects, fix investment policy first; with good projects, cut payout to fund investment. `concepts/dividend-policy/dividend-matrix.md`
- **DR-B10.5 (undefined ratios).** Net income ≤ 0 → payout ratio is `NA`, never negative. FCFE ≤ 0 → cash-return-to-FCFE is `NA`.
- **DR-B10.6 (regression benchmark).** `D-PAYREG` is fitted on **dividends only** and will label a heavy repurchaser a cash hoarder. Always adjust for buybacks before acting on the gap. R² near 20–26% means the prediction is a central tendency, not a target. `concepts/dividend-policy/market-regression-payout-prediction.md`
- **DR-B10.7 (peer group sanity).** If the peer group's own average FCFE is negative, matching it is not a target worth hitting. Report both median and average; where most peers pay nothing, the divergence is the finding. `concepts/dividend-policy/peer-group-payout-analysis.md`
- **DR-B10.8 (forward capacity).** `Cash available for buybacks_t = FCFE_t − expected dividends_t`, with FCFE projected on growth rates for revenues, net income, cap ex, depreciation, a working-capital percentage of the **revenue increment**, and the debt ratio. `concepts/dividend-policy/payout-forecasting.md`
- **DR-B10.9 (change constraints).** Before recommending a change, collect: the clientele profile (`M-OWN` tax status, age/income proxies), contractual promises (preferred-share minimum payouts), regulatory mandates, and flotation costs for any equity issue used to preserve a dividend. Treat an increase as permanent and a cut as costly. `concepts/dividend-policy/managing-dividend-changes.md`

**Concepts:** the full `concepts/dividend-policy/` index, plus `concepts/deliverables-worked-examples/dividend-policy-deliverable.md`

---

# Part V — Conditional branch overlays

Nine branches. Each is switched on by a rule in B1 and adds inputs on top of the standard
stages. More than one may be active at once; the constraint sets compose.

---

## C1 — Financial-service firms

**Trigger:** DR-B1.1. **Constraints:** `no-fcff-valuation`, `no-optimal-debt-ratio`,
`no-earnings-multiple` does *not* apply (PE and PBV are the right multiples here).

**Replaces:** B2's standard cleanup, B4's synthetic rating, B9 entirely, B10's FCFE.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `net_interest_income`, `net_fee_income`, `trading_income` | ccy | `F-10K` | Y | BLOCK — there is no COGS and no gross profit |
| `credit_loss_provision` | ccy | `F-10K` | Y | **Recurring operating expense; never extraordinary** |
| `risk_weighted_assets` | ccy | regulatory disclosures | Y | Total assets × a stated risk weight |
| `tier1_capital`, `tier1_ratio` | ccy / decimal | regulatory disclosures | Y | BLOCK |
| `regulatory_minimum_ratio` | decimal | regulator | Y | Basel minimum plus a stated buffer |
| `target_tier1_ratio_path[t]` | decimal | judgment | Y | Ramp from current to target over the forecast; **the ramp is often a larger reinvestment than asset growth itself** |
| `asset_growth_path[t]` | decimal | judgment | Y | Nominal GDP growth for a mature bank |
| `roe_path[t]` | decimal | judgment | Y | Converge to the cost of equity or a normalized industry level |
| `book_equity[t]` | ccy | derived, recursive | N | `BE_{t−1} + investment in regulatory capital_t` |
| `long_term_interest_expense` | ccy | `F-DEBT` | Y* | Required if a synthetic rating is attempted at all (`D-RATE3` only) |

**Rules**
- Reinvestment = **investment in regulatory capital** = `Δ(RWA × Tier 1 ratio)`.
- `FCFE = net income − investment in regulatory capital`.
- Value equity directly, through dividends or an excess-return model. Never via FCFF.
- Do **not** unlever bank betas. Use median **levered** comparable betas, weighted by net revenues.
- Regulatory ratios are stated on **book** values. A market-value "optimal debt ratio" can therefore breach a binding constraint.

**Concepts:** `concepts/dividend-policy/fcfe-for-banks.md`, `concepts/capital-structure/financial-firm-capital-structure.md`, `concepts/dark-side-difficult/financial-service-firm-valuation.md`, `.../bank-fcfe-and-excess-return-models.md`, `concepts/accounting-statements/sector-differences-in-financial-statements.md`

---

## C2 — Young / negative-earnings firms

**Trigger:** DR-B1.2 or DR-B1.6. **Constraints:** `no-earnings-multiple`,
`no-standard-growth-model`, `require-failure-probability`.

**Adds to B5:**

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `total_addressable_market`, `market_growth_rate` | ccy / decimal | `E-MKT` | Y | BLOCK — the forecast has no anchor without it |
| `target_market_share[milestone_year]` | decimal | judgment | Y | BLOCK |
| `target_operating_margin` | decimal | mature same-business-model peers (`D-INDUS`, named comparables) | Y | Industry after-tax operating margin; state the peer percentile used |
| `margin_convergence_year` or `speed_of_convergence` | year / parameter | judgment | Y | Linear to the target by year 10 |
| `sales_to_capital[phase]` | ratio | `D-INDUS` sales/capital | Y | Industry average; may vary by phase |
| `nol_carryforward` | ccy | `F-TAX` | Y | 0 |
| `failure_probability` | decimal | `D-SURV` sector survival tables, or bond-implied (C3) | Y | Sector survival rate over the forecast horizon |
| `distress_recovery_pct` | decimal | judgment | Y | **50%** |
| `distress_proceeds_basis` | enum book \| going-concern | judgment | Y | Book (BV equity + BV debt) × recovery % |
| `dilution_from_future_equity` | ccy or share count | judgment | Y | Required for any forward-multiple valuation |

**Rules**
- Work backwards from a mature end-state.
- Taxes are 0% while NOLs persist, then ramp to the target rate.
- FCFF is deeply negative for several years. That is the correct output, not an error.
- The ROIC path is the honesty check on whether the story hangs together.
- Discount rates fade toward mature levels over the forecast.
- Sanity-check the **absolute** revenue level in the terminal year against market size and against the largest incumbents.

**Concepts:** `concepts/dark-side-difficult/young-company-valuation.md`, `.../sales-to-capital-reinvestment.md`, `concepts/dcf-cashflows-growth/top-down-revenue-growth.md`, `.../normalizing-depressed-earnings.md`, `concepts/relative-valuation/pricing-young-companies.md`

---

## C3 — Distressed firms

**Trigger:** DR-B1.4. **Constraint:** `require-failure-probability`.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `traded_bond.price`, `.coupon`, `.maturity`, `.face` | mixed | `M-BOND` | Y | Rating-based cumulative default probability from `D-DEFPROB` |
| `annual_distress_probability π` | decimal | **derived** by inverting the bond price at the riskfree rate | N | `1 − (1 − cumulative)^{1/n}` from `D-DEFPROB` |
| `cumulative_distress_probability` | decimal | `1 − (1−π)^n` | N | `D-DEFPROB` 10-yr rate for the rating |
| `distress_sale_proceeds` | ccy | judgment | Y | % of book value; the percentage **falls** in a weak economy and when peers are also distressed |
| `face_value_of_debt` | ccy | A3 | Y | Book debt |
| `equity_option_inputs` (S = firm asset value, K = face value of debt, T = weighted debt life, σ² = firm-value variance) | mixed | DCF + A3 + `D-INDUS` std devs | Y* | Industry-average stock and bond volatilities; **never the firm's own equity volatility** as the asset volatility |

**Rules:** blend, do not raise the discount rate (N6). If proceeds < face value of debt,
the distress branch value of equity is **zero**. A market-implied probability that is far
more pessimistic than the rating table is information, not an error. The equity-as-call
valuation is an **alternative** estimate of equity value, never additive to the DCF.

**Concepts:** `concepts/dark-side-difficult/distress-and-failure-adjusted-value.md`, `.../bond-implied-distress-probability.md`, `concepts/real-options/equity-as-call-option.md`, `.../equity-option-inputs-troubled-firms.md`, `concepts/deliverables-worked-examples/equity-as-call-option-valuation.md`

---

## C4 — Cyclical and commodity firms

**Trigger:** DR-B1.3. **Constraint:** `require-normalized-earnings`.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `ebit_history[N]`, `margin_history[N]`, `roc_history[N]` | mixed | A2 | Y | BLOCK — normalization needs a full cycle |
| `normalization_window` | years | judgment | Y | **5 years**; longer for deep commodity cycles; use the **pre-shock** cycle where a specific shock hit |
| `normalization_method` | enum dollar-average \| return-based | judgment | Y* | Dollar averaging if firm size is stable; **return-based** (average ROC × current invested capital) if size changed materially |
| `commodity_price_current`, `.normalized` | price | `M-*` commodity feed | Y | Value at today's price and disclose the assumption |
| `revenue_to_price_regression` | slope | derived from history | Y* | Skip; use margin normalization only |
| `normalized_effective_tax_rate` | decimal | average over the same window | Y | Marginal rate |

**Rules:** normalize **only** when the cause is transient (a temporary problem or the
cycle). Structural causes — life cycle, leverage, a long-term operating problem — require
the revenue-driven route in C2 instead. Be consistent: if EBIT is normalized, the interest
coverage feeding the synthetic rating must use the normalized figure too. A normalized,
mature firm may deserve **no high-growth period at all**.

**Concepts:** `concepts/dcf-cashflows-growth/normalizing-depressed-earnings.md`, `concepts/dark-side-difficult/normalized-earnings.md`, `.../commodity-and-cyclical-valuation.md`, `concepts/capital-structure/optimal-debt-ratio-by-firm-type.md`

---

## C5 — Emerging-market / country-risk overlay

**Trigger:** DR-B1.8.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `sovereign.local_currency_rating` | Moody's | `M-RATING` | Y | S&P → Moody's conversion; PRS composite score if unrated |
| `sovereign_default_spread` | decimal | `M-CDS` net of US CDS \| hard-currency bond spread \| `D-SOVSPR` | Y | Rating table; report the range across all three routes |
| `relative_equity_volatility_multiplier` | ratio | `D-CTRY` production value | Y | Country-specific σ_equity/σ_bond |
| `country_erp[country]` | decimal | `D-CTRY` | Y | `mature ERP + spread × multiplier` |
| `revenue_by_country`, `production_by_country`, `assets_by_country` | decimal shares | `F-SEG` / operating stats | Y | Country of incorporation = 100%, heavily flagged |
| `lambda` | decimal | return regression on the sovereign bond \| domestic revenue ratio | Y | 1.0 |
| `expected_inflation[local]`, `expected_inflation[USD]` | decimal | `X-CB` / `X-IMF` / `X-BREAK` | Y | Central bank targets |
| `truncation_scenarios[]` — nationalization/regime-change probability and payoff | decimal / ccy | judgment | Y | None; flag if the asset is politically exposed |
| `cross_holdings` (group structures) | mixed | A3 | Y* | Often half the value of a group company sits outside the DCF |

**Rules:** N2 is the dominant risk here — the sovereign spread is stripped from the riskfree
rate **or** it sits in the ERP, never both, and never also in the cash flows. Use the
**local-currency** sovereign rating for a local-currency valuation. Country risk premiums
fade toward zero in the terminal phase. Value invariance: the same business must be worth
the same in any currency once inflation is handled consistently.

**Concepts:** `concepts/cost-of-equity/country-risk-premium.md`, `.../operation-weighted-erp.md`, `.../lambda-country-risk-exposure.md`, `concepts/cost-of-debt-capital/country-risk-in-cost-of-debt.md`, `.../currency-conversion-of-discount-rates.md`, `concepts/dark-side-difficult/country-risk-exposure.md`, `.../currency-consistency-and-invariance.md`, `.../truncation-and-political-risk.md`, `.../cross-holdings.md`

---

## C6 — Private companies and non-traded assets

**Trigger:** DR-B1.7. **Constraints:** `require-total-beta` (unless the buyer is
diversified), `require-illiquidity-discount` (unless the buyer is public and liquid).

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `owner_compensation_actual`, `market_salary_for_the_role` | ccy | filings / user / market survey | Y | BLOCK the cleanup step |
| `personal_expenses_in_the_statements` | ccy | user | Y | 0, flagged |
| `comparable_median_r_squared` | decimal | A8 Set 1 regressions | Y | `D-INDUS` implied; BLOCK total beta without it |
| `assumed_market_de` | decimal | **industry median market D/E** from `D-INDUS` | Y | Never the private firm's book D/E |
| `equity_value_proxy` | ccy | comparable PE × net income, or a comparable multiple | Y | BLOCK the debt ratio |
| `buyer_type` | enum private \| public-acquirer \| PE/VC \| IPO | user | Y | BLOCK — it determines beta, tax rate and every discount |
| `stake_pct` | decimal | user | Y | 100% |
| `illiquidity_route` | enum flat \| silber \| bid-ask-regression | judgment | Y | Bid-ask regression when revenues, profitability and cash are known |
| `key_person_share_of_business` | decimal | judgment | Y | 0; applies to **operating income**, not to value |
| `revenue`, `earnings_positive?`, `cash_to_firm_value` | mixed | statements | Y | Inputs to the bid-ask illiquidity regression |

**Rules:** clean the statements **first** (market owner salary, capitalized leases as the
often-only debt, remove personal expenses) — the cleanup feeds everything downstream.
Use medians, never averages, across comparables. Total beta = market beta / correlation
(= `sqrt(median R²)`). Buyer type flips the answer: a public acquirer gets a **market**
beta and **no** illiquidity discount; a private buyer gets total beta and a discount.
Illiquidity and minority discounts are separate and are not folded together.

**Concepts:** `concepts/asset-based-private/private-company-valuation-framework.md`, `.../private-company-statement-cleanup.md`, `.../private-company-cost-of-capital.md`, `.../total-beta.md`, `.../illiquidity-discount.md`, `.../silber-restricted-stock-regression.md`, `.../bid-ask-spread-illiquidity-regression.md`, `.../minority-discount.md`, `.../key-person-discount.md`, `.../private-to-public-sale.md`, `.../ipo-valuation.md`, `.../vc-stage-varying-cost-of-equity.md`, `concepts/cost-of-equity/non-traded-asset-betas.md`, `.../total-beta.md`

---

## C7 — Multi-business firms and sum-of-the-parts

**Trigger:** DR-B1.9.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `segments[].revenues`, `.operating_income`, `.identifiable_assets`, `.investments`, `.capex`, `.dandA` | ccy | `F-SEG` | Y | BLOCK the branch |
| `segments[].industry_key` | `D-INDUS` name | mapping | Y* | BLOCK |
| `segments[].peer_ev_sales` | ratio | `D-INDUS` EV/Sales | Y | Revenue weights as a crude substitute |
| `segments[].unlevered_beta` | decimal | A8 Set 1 per business | Y | `D-INDUS` unlevered beta |
| `debt_allocation_key` | enum identifiable-assets \| sales \| ebitda \| target-ratio | judgment | Y | **Identifiable assets**; state the key, it drives divisional D/E directly |
| `capitalized_corporate_expenses` | ccy | `F-SEG` corporate column | Y | Allocate or capitalize; state which |

**Rules:** business value = segment revenues × peer EV/Sales; the firm's unlevered beta is
the **value-weighted** average of the business unlevered betas (never revenue-weighted when
margins differ). Divisional debt is allocated, divisional D/E derived, betas relevered per
division. Use divisional rates as project hurdle rates — a company-wide rate lets safe
divisions subsidise risky ones and tilts the firm toward its riskiest businesses. Watch for
implausible allocation artifacts (a 117% divisional D/E producing an absurdly low WACC).

**Concepts:** `concepts/cost-of-debt-capital/divisional-cost-of-capital.md`, `concepts/cost-of-equity/bottom-up-beta.md`, `concepts/accounting-statements/segment-and-geographic-reporting.md`, `concepts/asset-based-private/sum-of-the-parts-framework.md`, `.../sum-of-the-parts-dcf.md`, `.../sum-of-the-parts-pricing.md`

---

## C8 — Real options

**Trigger:** an explicit claim of embedded optionality that passes the three-test gate.

**Gate before any data is collected (DR-C8.1):**
1. Is there a **named underlying asset** whose value changes unpredictably, and a payoff contingent on a specified event **within a finite period**? If not — stop, no premium.
2. Does the option have **significant economic value**? The test is restriction on competition. Full exclusivity → full value; no barriers → **zero**, however volatile the underlying; partial barriers → scale by an exclusivity factor between 0 and 1.
3. Can an option pricing model price it? Score: is the underlying traded? is there a market for the option? is the exercise cost known? Trust the output in proportion to how many hold.

**Inputs (collected only after the gate passes)**

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `S` — value of the underlying (PV of project/reserve/product cash flows) | ccy | DCF | Y | BLOCK |
| `K` — strike (development cost, expansion cost, salvage value, face value of debt) | ccy | project data | Y | BLOCK |
| `T` — life of the right (patent life, lease life, debt maturity) | years | contract | Y | BLOCK |
| `σ` — variance of the underlying's value | decimal | commodity price volatility, sector firm-value volatility, simulation | Y* | Industry std dev from `D-INDUS`; this is the least reliable input |
| `y` — dividend yield analogue (net production revenue / reserve value; `1/n` cost of delay) | decimal | derived | Y | `1/n` where n = years of exclusivity remaining |
| `r` — riskfree at the option's maturity | decimal | A5 | Y | 10-yr rate |
| `exclusivity_factor` | 0–1 | judgment | Y | Barrier-ladder scaling |

**Rules:** N9 — remove the corresponding optimism from the DCF before adding any premium.
Prefer the binomial engine when early exercise or jumps matter, which is the normal case
for real assets. If test 3 fails but 1 and 2 pass, use a decision tree and treat any number
as an order of magnitude.

**Concepts:** `concepts/real-options/real-options-framework.md`, `.../black-scholes-model.md`, `.../replicating-portfolio-and-binomial-model.md`, `.../option-to-delay.md`, `.../patent-valuation-as-option.md`, `.../natural-resource-options.md`, `.../option-to-expand.md`, `.../opportunities-are-not-options.md`, `.../option-to-abandon.md`, `.../decision-trees-vs-option-pricing.md`

---

## C9 — Acquisition, control and synergy

**Trigger:** `mode = acquisition` or `mode = restructuring`, or an activist/control question.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| Target: the full A2–A8 input set | — | — | — | BLOCK |
| Acquirer: the full A2–A8 input set | — | — | — | Required for synergy; not for value-of-control alone |
| `target_optimal_policy` — optimal debt ratio, target ROC, target reinvestment | mixed | B9 + B5 run on the target | N | — |
| `probability_of_management_change` | decimal | judgment, or **inverted from the market price** | Y | Read it out of the price: `price = status quo + p × (optimal − status quo)` |
| `synergy_assumptions` — which growth rate, margin, ROC, reinvestment, tax rate or debt ratio changes, by how much, and when it takes effect | mixed | judgment | Y | BLOCK — an unnamed synergy cannot be valued |
| `combined_unlevered_beta` | decimal | **value-weighted** average of the two unlevered betas | N | — |
| `combined_debt_ratio` | decimal | deal financing plan | Y | Value-weighted current ratios |
| `nol_target` and acquirer taxable income | ccy | `F-TAX` | Y | 0 |
| `share_classes[]` — voting rights, economic rights, prices | mixed | `F-PROXY` / `M-PX` | Y* | Single class |
| `transaction_multiples[]` (precedent deals) | ratio | deal databases | Y* | Sector multiples from `D-INDUS`, flagged as pricing not valuation |

**Rules:** discount the target at the **target's own** risk and debt capacity, never the
acquirer's. Four numbers are required: status quo value, restructured (optimally managed)
value, synergy value, and the price. Value of control = restructured − status quo. Synergy
= combined-with-synergy − (standalone A + standalone B), and the no-synergy combined value
must equal the sum of the parts **exactly** as a check. Use the target's restructured value
as the synergy base so control and synergy do not overlap. No bolt-on control premium — that
double counts (N10).

**Concepts:** `concepts/acquisitions-control-enhancement/three-reasons-and-acid-test.md`, `.../status-quo-valuation.md`, `.../restructured-value-and-value-of-control.md`, `.../valuing-synergy.md`, `.../synergy-taxonomy.md`, `.../target-discount-rate-discipline.md`, `.../control-premium-rules-of-thumb.md`, `.../expected-value-of-control.md`, `.../implied-probability-of-management-change.md`, `.../voting-premium-and-minority-discount.md`, `.../transaction-and-exit-multiples.md`, `concepts/deliverables-worked-examples/value-of-control-and-synergy.md`

---

# Part VI — Minimum viable dataset and the G1 predicate

`G1_data` passes when **all** of the following hold.

### 6.1 Universal minimum (every mode)

| Requirement | Fields |
|---|---|
| Identity | `mode`, ticker/name, country of incorporation, valuation currency, valuation date, industry key |
| One full fiscal year of statements | Income statement through net income; balance sheet that balances; cash flow statement with all three sections |
| Debt boundary | Book debt (short + long + current portion) and either a lease schedule or a reported lease liability |
| Cash | Cash and marketable securities |
| Share base | Actual shares outstanding (public) or an equity-value proxy route (private, C6) |
| Riskfree rate | A 10-year rate in the valuation currency, by any rung of the DR-A5.1 ladder |
| ERP | Mature-market ERP at a stated vintage |
| Beta path | Either a comparable set (A8 Set 1) or an industry unlevered beta from `D-INDUS`/`D-GLOB` |
| Tax rate | A marginal rate for the domicile |
| Reference vintage | All vintage-critical tables loaded at one consistent `as_of` |

### 6.2 Mode-specific additions

| Mode | Additional minimum |
|---|---|
| `valuation` | 3+ years of statements (5 preferred); a growth-driver route with its inputs; terminal-value inputs |
| `corporate-finance` | 10 years of EBIT history (volatility), ownership breakdown, 5 years of dividends and buybacks, peer group, EBITDA and cap ex |
| `acquisition` | Target **and** acquirer full sets; named synergy assumptions |
| `project` | Project cash-flow schedule, project life, divisional business classification, project currency and country |
| `ipo` | C6 set plus use of proceeds, prior equity claims, post-issue share count and options |
| `restructuring` | Status-quo set plus B9's optimal-structure input set plus a target-ROC assumption |

### 6.3 Blocking rules

- Any of V-A2.1, V-A2.2, V-A2.5 failing → **BLOCK**. The statements are not internally consistent and nothing downstream is trustworthy.
- A vintage-critical table missing with no fallback → **BLOCK**.
- `require-failure-probability` active with no probability source and no `D-SURV`/`D-DEFPROB` fallback → **BLOCK**.
- `require-total-beta` active with no comparable R² → **BLOCK**.
- Geography weights defaulted to country-of-incorporation for a firm with a country risk premium above zero → **not blocking, but a mandatory disclosure** and a required sensitivity.
- Statements older than 18 months with no interim filing → **BLOCK** for `valuation`; degrade to `stale` for `corporate-finance`.

### 6.4 What the collector writes

- `01-data/raw-financials.json` — all CO fields, per period, with `source` and `as_of` on every leaf.
- `01-data/market-data.json` — all MK fields plus the loaded RT snapshots with their `as_of`.
- `01-data/sources.md` — one line per source ID actually used, with retrieval date and document reference; every `fallback` and `stale` field listed explicitly.
- `01-data/gaps.json` — one entry per attempted field with status, the fallback applied, and the downstream stage it constrains.

---

# Part VII — Refresh, vintage and freshness policy

| Data | Freshness limit relative to `valuation_date` | On breach |
|---|---|---|
| Price, shares, market cap | 1 trading day | Refetch |
| Government bond yields, CDS, Baa spread | 1 trading day | Refetch |
| Corporate rating spread table (`D-SPREAD`, `D-RATE*`) | **At the valuation date** — spreads doubled to tripled inside one year in 2008 and spiked and reverted inside 2020 | Refetch; if impossible, mark `stale` and disclose |
| Implied ERP (`D-ERP`) | 1 month; re-estimate on any material index move | Recompute from index level, base cash flow (dividends + buybacks), consensus growth, terminal growth = riskfree |
| Country ERP / default spread (`D-CTRY`, `D-SOVSPR`) | 6 months (published each January and July) | Recompute from CDS or hard-currency bond spreads |
| Industry averages (`D-INDUS`, `D-GLOB`, `D-CPXSEC`) | 12 months (January snapshot) | Mark `stale`, disclose |
| Multiple regressions (`D-MULTREG`) | 12 months — coefficients drift hard; the market price of growth ranged roughly 0.4 to 2.6 across two decades | Mark `stale`, weight the prediction down |
| Payout / debt-ratio regressions (`D-PAYREG`, `D-DEBTREG`) | 12 months | Mark `stale` |
| Tax rates (`D-TAX`) | 12 months, or immediately on a known statutory change | Refetch |
| Filings | New 10-K within 90 days of fiscal year end; new 10-Q within 45 days of quarter end | Rebuild TTM |
| Analyst consensus | 1 month | Refetch |
| Ownership (13F) | 1 quarter | Refetch |
| Governance (proxy) | 12 months | Refetch |
| Survival, illiquidity, R&D-life, distress-cost tables | No limit — structural | — |

**Vintage-matching rule (R4) restated as a predicate:** for the set
`{D-ERP, D-CTRY, D-SOVSPR, D-RATE1, D-RATE2, D-RATE3, D-SPREAD, D-MULTREG, D-DISTRIB}`,
`max(as_of) − min(as_of) ≤ 3 months` **and** `valuation_date − min(as_of) ≤ 12 months`.
Violation is a hard failure at G4.

---

# Part VIII — Validation rule catalogue (consolidated)

The full predicate set, grouped by what it protects.

**Statement integrity**
- V-A2.1 balance sheet balances
- V-A2.2 net-income tie into CFO
- V-A2.3 retained-earnings roll-forward
- V-A2.4 D&A tie
- V-A2.5 cash tie
- V-A2.6 segment reconciliation

**Adjustment integrity**
- V-B2.1 lease capitalization leaves net income unchanged
- V-B2.2 R&D capitalization leaves FCFF unchanged
- V-B2.3 every earnings adjustment has a matching capital adjustment
- V-B2.4 quality-of-earnings trend computed
- V-B2.5 excise taxes stripped for commodity filers
- V-B2.6 bank revenue built as net interest plus net fee plus trading income

**Matching**
- R1 currency
- R2 claimholder
- R3 nominal versus real
- R4 vintage
- R5 debt convention
- Same `t` in beta relevering and in the after-tax `k_d`
- Same D/E in beta relevering and in the WACC weights

**Single-count**
- N1 tax shield. N2 country risk. N3 options versus dilution. N4 cash. N5 cross-holdings.
- N6 failure risk. N7 downside protection. N8 complexity. N9 real options. N10 control value.

**Forecast consistency**
- V-B5.1 `g = RIR × ROIC` holds every year
- V-B5.2 marginal ROIC plausible
- V-B5.3 absolute revenue level plausible
- V-B5.4 within the market ceiling
- V-B5.5 growth and reinvestment never set independently
- V-B5.6 working capital not double counted
- V-B5.7 NOL not extended into perpetuity

**Terminal**
- DR-B6.1 `g ≤ riskfree`
- DR-B6.2 reinvestment = `g/ROC`
- DR-B6.5 implied perpetual ROIC computed and reported
- Terminal beta, debt ratio and country risk premium all mature

**Bridge**
- Every line valued, or explicitly zero with a reason
- Actual shares, not diluted
- Book-versus-market debt convention declared, and consistent with the WACC weights

**Statistical**
- t-statistic and R² thresholds (DR-B8.4)
- Median, not mean (DR-B8.2, DR-A8.1)
- Dropped-observation counts recorded (DR-A8.5)
- Units form recorded for every regression (DR-B8.5)

**Diagnostics that prompt re-examination rather than failure.** None of these blocks a run.
Each one means an input is probably wrong.
- Value/price ratio above 2 or below 0.5
- Marginal ROIC far above the firm's own history
- ERP divided by the Baa spread far from ~2
- A synthetic rating more than two notches from the actual rating
- A peer group whose average FCFE is negative
- A regression with R² below 15% carrying a recommendation

---

# Part IX — Fallback ladder summary

The single table a collector consults when a primary source fails. Ordered by how much the
substitution costs the analysis.

| Missing | Ladder (best first) | Cost of the last rung |
|---|---|---|
| Riskfree rate | Aaa sovereign 10-yr → min across same-currency sovereigns → local rate − sovereign spread (market, then rating) → inflation + real rate build-up → differential inflation from US$ → switch currency | Every other input must be restated in the new currency |
| Mature-market ERP | Current implied → average implied over a stated window → historical geometric stocks−T.Bonds, longest window | Historical premium is *negatively* correlated with future returns |
| Country risk premium | `D-CTRY` on the local-currency rating → CDS net of US → hard-currency bond spread → PRS composite score | PRS mapping is coarse |
| Unlevered beta | Firm-level comparable median, cash-corrected → `D-INDUS`/`D-GLOB` industry unlevered beta → regression beta unlevered at the window-average D/E | A regression beta measures a company that may no longer exist |
| Market D/E | Market equity + market debt → industry median market D/E → target ratio | Book D/E is never acceptable |
| Cost of debt | Straight-bond YTM → global rating spread → recent bank loan → synthetic rating → local rating + λ × sovereign spread | Synthetic uses one ratio where agencies use many |
| Debt maturity | Disclosed schedule weighted average → **3 years** | Biases market value of debt |
| Lease debt | PV of disclosed commitments at pre-tax `k_d` → reported IFRS 16 / ASC 842 liability → 0 | Zero understates debt, overstates ROIC, overstates the equity weight |
| Working-capital ratio | Firm 3–5 yr average → industry `D-INDUS` non-cash WC/revenues → 0 | A wrong sign here compounds every forecast year |
| Cap ex forecast | Reinvestment rate `g/ROC` → firm history → `D-CPXSEC` sector Cap Ex/Depreciation or Net CapEx/Sales → net cap ex = 0 | Net cap ex = 0 is consistent only with ~zero real growth |
| Sales-to-capital | Firm's own → `D-INDUS` sales/capital → industry median | Drives the whole reinvestment path in C2 |
| Growth rate | Fundamentals (RIR × ROC) → analyst consensus, converted → historical geometric | Historical growth off a small or negative base is meaningless |
| Terminal growth | Explicit judgment, capped → riskfree rate | Never above riskfree |
| Terminal ROC | Explicit judgment → terminal cost of capital | Neutralises growth, which is the honest default |
| Failure probability | Bond-implied → rating cumulative default (`D-DEFPROB`) → sector survival (`D-SURV`) | Rating tables are class averages, usually optimistic |
| Volatility (options, distress) | Firm's own implied/historical → `D-INDUS` std dev equity | Firm-value variance ≠ equity variance at high leverage |
| Comparable R² (total beta) | Comparable regressions → `D-INDUS` | Without it, total beta cannot be computed at all |
| Peer multiples | Screened peer set → `D-INDUS`/`D-GLOB` industry row → `D-MULTREG` regional regression | The regional regression ignores sector membership entirely |
| Governance score | `E-GOV` → the red-flag checklist alone | Loses the peer benchmark, keeps the substance |
| Macro sensitivities | Firm regressions with t > 2 → `D-MACRO` sector coefficients, value-weighted | Firm-level insignificant slopes are worse than the sector average |

---

## Appendix — What a user may supply directly

Fields marked `Y` above are accepted at face value and recorded as `source: "user"`.
Fields marked `Y*` are accepted after the stated validation. The rest are derived.

**Freely user-suppliable.** These are judgments the pipeline cannot make for itself.
- Mode, company identity, valuation currency, valuation date
- Target operating margin; market size and market-share path; sales-to-capital ratio
- Growth-period length; terminal growth and terminal ROC, subject to the cap and the reverse check
- Failure probability, recovery rate, bankruptcy-cost percentage, distress severity
- Debt-allocation key, illiquidity route, buyer type, lambda
- Synergy assumptions, rating constraints, peer-set definitions

**Never accepted bare.** Each of these must trace to a source or to a stated derivation.
- A statement line item with no filing reference
- A rate-table row with no vintage
- WACC, cost of equity or beta as a single number, without its components
- A "normalized" riskfree rate
- A control premium expressed as a bolt-on percentage
- A terminal growth rate above the riskfree rate
- A growth rate and a reinvestment rate set independently of each other

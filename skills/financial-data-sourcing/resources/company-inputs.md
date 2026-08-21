# Company inputs: identity, statements, footnotes

Stages A1 to A3. Every field is class CO unless the source column says otherwise. Column
meanings: units are always decimal fractions for percentages and an explicit
`{value, currency, scale}` triple for money. The user column reads `Y` for accept at face
value, `Y*` for accept after the stated validation, `N` for derive or trace. `BLOCK` in the
fallback column means the gate fails.

---

## A1 — Mandate, identity and routing

| Field | Units | Source | Frequency | User? | Fallback |
|---|---|---|---|---|---|
| `mode` | enum: valuation, corporate-finance, acquisition, project, ipo, restructuring | user | per run | Y | BLOCK |
| `company.name`, `.ticker`, `.exchange` | string | user or `M-PX` | static | Y | BLOCK |
| `company.country_of_incorporation` | ISO country | `F-10K` | static | Y | BLOCK |
| `company.currency` | ISO currency | user | per run | Y | The reporting currency of `F-10K` |
| `valuation_date` | date | user | per run | Y | Today |
| `company.fiscal_year_end` | MM-DD | `F-10K` | static | Y* | Infer from filing dates |
| `company.industry_us`, `.industry_global` | industry name from `D-INDUS` or `D-GLOB` | user or SIC mapping | static | Y* | Map from SIC or GICS. If ambiguous, list the candidates in `gaps.json` |
| `company.is_public` | boolean | `M-PX` | static | Y | No price series means private; route to the private branch |
| `company.reporting_standard` | enum: GAAP, IFRS, local | `F-10K` auditor's report | static | Y* | Infer from the statement headings |

**Currency.** If the valuation currency differs from the filing's reporting currency, flag
every downstream stage as needing a conversion, and record which route applies:
differential-inflation conversion of a finished rate, or a rebuild from the local riskfree
rate. See `knowledge/concepts/cost-of-debt-capital/currency-conversion-of-discount-rates.md`.

**Industry.** Map by the business the firm operates, not by its listing classification. A
multi-business firm gets a list of industries with revenue weights, filled in at A3.

**Project mode.** In `mode = project`, stages A2 to A4 collapse to whatever the divisional
hurdle rate needs. The project's own cash-flow schedule is a user input.

Concepts: `knowledge/concepts/accounting-statements/accounting-standards-gaap-ifrs.md`,
`knowledge/concepts/dark-side-difficult/difficult-company-taxonomy.md`.

---

## A2 — Financial statements

Pull ten fiscal years where available, five as the working minimum, one as the floor. Use
`F-10Q` whenever the last annual report is more than one quarter old.

### Income statement

| Field | Units | Frequency | User? | Fallback |
|---|---|---|---|---|
| `revenues` | ccy | annual + quarterly | Y* | BLOCK |
| `cogs`, `sga`, `rnd`, `other_operating_expense` | ccy | annual | Y* | With no cost-of-goods line under a by-nature presentation, build a proxy from materials, the inventory change and the production share of employee benefits. Record the assumption |
| `depreciation_amortization` | ccy | annual | Y* | Take the cash-flow-statement add-back when it is not on the face of the income statement |
| `ebit` as reported | ccy | annual + trailing twelve months | Y* | Derive it: revenues less operating expenses, on your own operating line rather than the filer's label |
| `interest_expense`, gross | ccy | annual | Y* | If the filer nets interest, go to `F-DEBT`. A net figure is not enough |
| `interest_income` | ccy | annual | Y* | 0 |
| `equity_income_from_affiliates` | ccy | annual | Y* | 0 |
| `pretax_income`, `tax_provision`, `net_income` | ccy | annual + trailing twelve months | Y* | BLOCK |
| `noncontrolling_interest_income` | ccy | annual | Y* | 0 |
| `net_income_to_parent` | ccy | annual | N | Net income less noncontrolling interest |
| `shares_basic`, `shares_diluted`, weighted average | count | annual | Y* | BLOCK for per-share work |
| `special_items`, each labelled and dated | ccy | annual, 5 to 10 years | Y* | Empty list, and flag that the recurrence test cannot run |
| `excise_taxes` | ccy | annual | Y* | 0. Needed only for commodity filers |

### Balance sheet

| Field | Units | Frequency | User? | Fallback |
|---|---|---|---|---|
| `cash_and_equivalents`, `short_term_investments`, `marketable_securities` | ccy | annual, 2+ years | Y | BLOCK |
| `accounts_receivable`, `inventory`, `other_current_assets` | ccy | annual, 2+ years | Y* | BLOCK for working-capital work |
| `accounts_payable`, `accrued_liabilities`, `taxes_payable`, `other_non_debt_current_liabilities` | ccy | annual, 2+ years | Y* | BLOCK for working-capital work |
| `short_term_debt`, `current_portion_lt_debt`, `commercial_paper` | ccy | annual | Y* | BLOCK. These must be pulled out of current liabilities before working capital is computed |
| `long_term_debt`, book | ccy | annual | Y | BLOCK |
| `gross_ppe`, `accumulated_depreciation`, `net_ppe` | ccy | annual | Y* | Net property alone, which loses the asset-age ratio |
| `goodwill`, `intangibles_definite`, `intangibles_indefinite`, `accumulated_amortization` | ccy | annual | Y* | 0 |
| `equity_method_investments`, `other_non_operating_assets` | ccy | annual | Y* | 0 |
| `book_equity_parent`, `noncontrolling_interests`, `mezzanine_equity` | ccy | annual | Y* | BLOCK for return on equity |
| `paid_in_capital`, `retained_earnings`, `treasury_stock`, `aoci` | ccy | annual | Y* | Composition analysis is skipped |
| `preferred_stock`, book | ccy | annual | Y | 0 |
| `total_assets`, `total_liabilities`, `total_equity` | ccy | annual | Y | BLOCK. The balance check needs them |

### Cash flow statement

| Field | Units | Frequency | User? | Fallback |
|---|---|---|---|---|
| `cfo` and its build-up lines: net income, depreciation, stock-based compensation, deferred taxes, impairments, each working-capital change | ccy | annual, 5 to 10 years | Y* | The section total alone cannot support a free cash flow to equity |
| `capital_expenditures` | ccy | annual | Y | BLOCK |
| `divestitures_of_assets` | ccy | annual | Y* | 0 |
| `cash_acquisitions` | ccy | annual, 5 to 10 years | Y* | 0, and flag it. An acquisitive firm without this line understates reinvestment |
| `purchases_sales_of_investments` | ccy | annual | Y* | 0 |
| `debt_raised`, `debt_repaid` | ccy | annual | Y* | Net debt issued alone |
| `equity_issued`, `stock_buybacks` | ccy | annual, 5 to 10 years | Y | 0 |
| `dividends_paid_common`, `_preferred`, `_nci` | ccy | annual, 5 to 10 years | Y | 0 |
| `fx_effect_on_cash` | ccy | annual | Y* | 0 |
| `unusual_operating_classifications`: content spend, capitalized software, originated receivables sitting inside operating cash flow | ccy | annual | Y* | Empty. Flag it for a streaming, software or captive-finance filer |

### The six ties

Run these before marking the stage complete.

| ID | Tie | On failure |
|---|---|---|
| V-A2.1 | Total assets equal total liabilities plus total equity, including mezzanine and noncontrolling interests | BLOCK. Either a transcription error or a missed layer |
| V-A2.2 | Income-statement net income equals the first line of operating cash flow. An IFRS filer may start at pre-tax profit; tie to that line and confirm the tax-paid adjustment | BLOCK |
| V-A2.3 | Retained earnings roll forward: prior balance plus net income less dividends and buyback charges | Flag. The residual must be explained |
| V-A2.4 | Income-statement depreciation equals the cash-flow add-back | Flag. Check whether depreciation is buried inside cost of goods |
| V-A2.5 | Beginning cash plus the three sections plus the currency effect equals ending cash | BLOCK |
| V-A2.6 | Segment third-party revenues plus eliminations equal consolidated revenues | Flag. A gap means a missed corporate or elimination column |

Concepts: `knowledge/concepts/accounting-statements/role-of-accounting-and-three-statements.md`,
`.../income-statement-structure.md`, `.../balance-sheet-views-and-asset-measurement.md`,
`.../cash-flow-statement-structure.md`, `.../liabilities-debt-and-leases.md`,
`.../extraordinary-items-and-pro-forma-earnings.md`.

---

## A3 — Footnotes and structured disclosures

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `lease.current_expense` | ccy | `F-LEASE` | Y | 0, which skips lease capitalization. Flag it |
| `lease.commitments[1..5]` | ccy per year | `F-LEASE` | Y | For a post-2019 filer use the reported lease liability, flagged, because the accounting number need not equal the present value of commitments |
| `lease.thereafter_lump` | ccy | `F-LEASE` | Y | 0, which sets the tail to zero and the lease life to five years |
| `lease.reported_liability` | ccy | `F-LEASE` | Y | — |
| `debt.instruments[]`: amount, stated rate, maturity, currency, fixed or floating, straight or convertible | mixed | `F-DEBT` | Y* | A blended rate only |
| `debt.maturity_schedule[1..5]` | ccy per year | `F-DEBT` | Y* | Weighted-average maturity of three years |
| `debt.weighted_avg_maturity` | years | derived from the schedule | Y | 3 years |
| `debt.weighted_avg_rate` | decimal | derived | N | Interest expense over book debt. A diagnostic only, never the cost of debt |
| `segments[]`: name, third-party revenue, intersegment revenue, operating income, identifiable assets, investments, capital expenditure, depreciation | ccy | `F-SEG` | Y* | Assume a single segment, which blocks divisional rates and sum-of-the-parts work |
| `geography[]`: region or country, third-party revenue share | decimal | `F-SEG` | Y | Country of incorporation at one hundred percent, flagged hard. This is the most common cause of a wrong equity risk premium |
| `production_by_country[]` | decimal share | `F-10K` or operating statistics | Y | Revenue weights |
| `options.count_outstanding` | count | `F-OPT` | Y | 0 |
| `options.weighted_avg_strike` | ccy | `F-OPT` | Y | The current price, an at-the-money assumption |
| `options.weighted_avg_remaining_life` | years | `F-OPT` | Y | 4 years, shortened further for early exercise |
| `options.vested_fraction` | decimal | `F-OPT` | Y | 1.0 |
| `restricted_stock_outstanding` | count | `F-OPT` | Y | 0 |
| `cross_holdings[]`: name, ownership percentage, consolidated flag, carrying value, listed price where traded | mixed | `F-INV` | Y* | Carrying value, flagged |
| `nol_carryforward` | ccy | `F-TAX` | Y | 0 |
| `effective_tax_rate` | decimal | `F-TAX` or derived | Y | Tax provision over pre-tax income |
| `pension_funded_status` | ccy, negative when underfunded | `F-PEN` | Y | 0 |
| `contingent_liabilities[]`: description, disclosed amount, probability language | mixed | `F-CONT` | Y* | Empty, flagged |
| `rnd_history[0..N]`, N being the amortizable life | ccy per year | `F-10K`, N+1 years | Y | Pad the missing years with zeros and flag that the research asset is understated |
| `acquisitions_history[]`: year, price, cash or stock | mixed | `F-ACQ` | Y* | The cash-acquisition line from A2. Stock-funded deals will be missed |

### Decision rules

**Lease tail.** The number of years beyond the fifth is the thereafter lump divided by the
mean of the first five commitments, rounded half away from zero. A mean of zero sets the
tail to zero. Lease life is five plus that tail.
See `knowledge/concepts/cost-of-debt-capital/operating-leases-as-debt.md`.

**Debt maturity.** Weight each disclosed tranche by its share of the disclosed total, then
apply the resulting maturity to full book debt rather than to the disclosed subtotal.

**Geographic weights.** Use third-party revenue, never revenue including intersegment
sales. Prefer production location for a natural-resource firm. For a manufacturer, ask
where the plants are. See `knowledge/concepts/cost-of-equity/operation-weighted-erp.md`.

**R&D life.** Take the amortizable life from `D-RDLIFE` by industry. The guideline blocks
run two years for a non-technological service, three for retail and technology services,
five for light manufacturing, and ten for heavy manufacturing, research with patenting, and
long-gestation businesses. See `knowledge/concepts/dcf-cashflows-growth/rnd-capitalization.md`.

**Hidden reinvestment.** When `unusual_operating_classifications` is non-empty, those
amounts move out of operating cash flow and into the investing step before free cash flow
to equity is built.
See `knowledge/concepts/accounting-statements/investing-cash-flows-and-reinvestment.md`.

Concepts: `knowledge/concepts/cost-of-debt-capital/market-value-of-debt.md`,
`.../what-counts-as-debt.md`,
`knowledge/concepts/accounting-statements/segment-and-geographic-reporting.md`,
`knowledge/concepts/dcf-model-choice-loose-ends/valuing-employee-options.md`,
`.../cross-holdings.md`, `.../debt-and-other-claims-in-the-bridge.md`.

# Source registry

Canonical source identifiers. Every field table in this skill names one of these. Record
the identifier, the retrieval date and the document reference in `01-data/sources.md`.

## Company filings and disclosures — class CO

| ID | Source | What it yields |
|---|---|---|
| `F-10K` | Annual report: 10-K, 20-F, 40-F or the local equivalent | Three statements, all footnotes, segment note, management discussion |
| `F-10Q` | Latest quarterly filing | Year-to-date columns for the trailing-twelve-month rebuild |
| `F-DEBT` | Debt footnote | Instrument list, stated rates, maturities, currency, fixed or floating, five-year maturity schedule |
| `F-LEASE` | Lease footnote and commitments note | Current-year lease expense, minimum commitments for years one to five, the thereafter lump, the reported lease liability |
| `F-SEG` | Segment and geographic footnote | Third-party revenue, intersegment revenue, operating income, identifiable assets, investments, capital expenditure, depreciation, per segment and region |
| `F-OPT` | Stock-compensation footnote | Options outstanding, weighted-average exercise price, weighted-average remaining life, vesting status, restricted stock |
| `F-INV` | Investments and equity-method footnote | Cross-holdings with ownership percentage, carrying value, equity income |
| `F-TAX` | Tax footnote | Effective-rate reconciliation, statutory rate, loss carryforward balance and expiry |
| `F-PEN` | Pension and other post-employment benefits footnote | Projected benefit obligation, plan assets, funded status |
| `F-CONT` | Commitments and contingencies footnote | Litigation, guarantees, take-or-pay contracts, off-balance-sheet obligations |
| `F-PROXY` | Proxy statement, DEF 14A or the local equivalent | Board composition, tenure, independence, attendance, compensation, insider holdings, charter provisions |
| `F-ACQ` | Acquisitions footnote | Deal prices, goodwill created, purchase-price allocation, stock-funded deals |

`F-10K` is the base document. A non-US filer under IFRS or Ind-AS presents differently: the
balance sheet often runs non-current assets first, and expenses are often grouped by nature
rather than by function. See `knowledge/concepts/accounting-statements/accounting-standards-gaap-ifrs.md`.

`F-ACQ` matters more than its size suggests. Stock-funded deals never appear in the cash
flow statement, so an acquisitive firm sourced only from the cash-flow line understates
reinvestment, sometimes several-fold.

## Market data — class MK

| ID | Source | What it yields |
|---|---|---|
| `M-PX` | Equity market data feed | Current price, shares outstanding, market capitalization, historical price series, dividend- and split-adjusted returns |
| `M-IDX` | Index data | Index level, index return series, index dividends, index buybacks |
| `M-BOND` | Corporate bond market | Traded bond prices, coupons, maturities, yield to maturity for the subject firm |
| `M-RATE` | Government bond markets | Ten-year and other tenor government bond yields by currency; index-linked yields |
| `M-CDS` | Credit default swap market | Sovereign ten-year spreads; corporate spreads where traded |
| `M-RATING` | Moody's, S&P, Fitch and local-scale agencies | Corporate issuer and issue ratings; sovereign local-currency and foreign-currency ratings |
| `M-CRED` | Corporate credit spread series | The Baa-over-Treasury spread; the spread-by-rating curve at a date |
| `M-OWN` | Ownership filings and aggregators: 13F, Forms 3/4/5, local equivalents | Institutional percentage, insider percentage, float, largest holders |
| `M-FX` | Foreign exchange market | Spot rates, forward rates for interest-rate-parity checks |

Tag every rating from `M-RATING` as global-agency or local-scale. A global rating already
embeds sovereign risk; a local-scale rating does not. That flag decides whether the country
default spread is added a second time.
See `knowledge/concepts/cost-of-debt-capital/country-risk-in-cost-of-debt.md`.

## Damodaran reference datasets — class RT

Listed with their columns and freshness limits in
[reference-datasets.md](reference-datasets.md). Identifiers: `D-ERP`, `D-HIST`, `D-CTRY`,
`D-SOVSPR`, `D-TAX`, `D-RATE1`, `D-RATE2`, `D-RATE3`, `D-SPREAD`, `D-INDUS`, `D-GLOB`,
`D-DEFPROB`, `D-DISTRESS`, `D-RDLIFE`, `D-CPXSEC`, `D-MACRO`, `D-MULTREG`, `D-DEBTREG`,
`D-PAYREG`, `D-ILLIQ`, `D-SURV`, `D-DISTRIB`.

## Macro sources — class MK

| ID | Source | What it yields |
|---|---|---|
| `X-CB` | Central bank or national statistical agency | Consumer price inflation, inflation targets, real GDP growth actual and forecast |
| `X-FRED` | FRED or an equivalent macro series library | Ten-year Treasury yield, the Baa spread, consumer price index, real GDP, trade-weighted dollar index |
| `X-BREAK` | Inflation-indexed bond market | Breakeven inflation and real yields from index-linked bonds |
| `X-IMF` | IMF, World Bank, OECD | Long-run inflation and real growth forecasts by country; nominal GDP |

## Consensus and third-party estimates

| ID | Source | What it yields | Trust rule |
|---|---|---|---|
| `E-CONS` | Analyst consensus aggregator | Five-year expected earnings growth, next-year revenue and earnings, dispersion, revision history | An input, not an answer. This is earnings-per-share growth. Never drop it into a firm-level cash flow model |
| `E-IDXCONS` | Top-down index earnings consensus | Aggregate index earnings growth | Needed to recompute the implied equity risk premium |
| `E-GOV` | Governance score vendor | Overall score plus audit, board, shareholder-rights and compensation sub-scores | Read the underlying policies. The score is an input to the read, never the verdict |
| `E-MKT` | Addressable-market research | Market size, market growth rate, market shares | Only for revenue-driven forecasts, and always a judgment input |

`E-CONS` growth is estimated on earnings per share. Feeding it into an operating cash flow
model mixes claimholders and breaks rule R2.
See `knowledge/concepts/dcf-cashflows-growth/analyst-growth-estimates.md`.

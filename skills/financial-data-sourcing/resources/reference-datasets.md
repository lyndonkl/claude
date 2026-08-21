# Reference datasets

Stage A6. The Damodaran lookup tables, their columns, and the freshness limit on each.
These are class RT: keyed by table name and `as_of`, cached globally per vintage, and
loaded once per run at a single consistent vintage.

The bundled snapshots live in `cost-of-capital-toolkit/resources/data/`. Each file carries
`as_of`, `source` and `refresh` fields. Read them from a path passed in, so a refreshed
table can be swapped without touching code. The published source is Damodaran's data page
at NYU Stern, updated each January, with the country and premium tables also updated in
July.

## The tables

| ID | Dataset | Columns used | Vintage-critical |
|---|---|---|---|
| `D-ERP` | Implied equity risk premium for the S&P 500 | Current implied premium; the annual history; the expected return on stocks | Yes |
| `D-HIST` | Historical returns | Arithmetic and geometric premiums over bills and over bonds, by window, with standard errors | No |
| `D-CTRY` | Country equity risk premiums | Country, Moody's local-currency rating, default spread, country risk premium, total premium; regional GDP-weighted premiums; the PRS composite score mapping for unrated countries | Yes |
| `D-SOVSPR` | Sovereign rating to default spread | Rating, typical default spread | Yes |
| `D-TAX` | Country corporate marginal tax rates | Country, statutory marginal rate | Yes |
| `D-RATE1` | Synthetic rating table, large and stable firms | Coverage lower bound, upper bound, rating, default spread | Yes for the spreads |
| `D-RATE2` | Synthetic rating table, small and risky firms | Same | Yes for the spreads |
| `D-RATE3` | Synthetic rating table, financial-service firms, on long-term interest coverage only | Same | Yes for the spreads |
| `D-SPREAD` | Rating to default spread, for the actual-rating route | Rating, spread, by date | Yes |
| `D-INDUS` | US industry averages | Firm count, levered beta, unlevered beta, standard deviation of equity, market debt-to-equity, market debt-to-capital, return on equity, return on capital, effective tax rate, pre-tax and after-tax operating margin, net margin, capital expenditure over depreciation, non-cash working capital over revenues, payout ratio, reinvestment rate, sales-to-capital, EV/Sales, EV/EBITDA, EV/EBIT, price-to-book, trailing price-earnings, cost of equity, cost of capital, pre-tax cost of debt | Yes |
| `D-GLOB` | Global industry averages | The same schema on a global universe | Yes |
| `D-DEFPROB` | Cumulative default probability by rating | Rating, one-year, five-year and ten-year cumulative default rates | Yes |
| `D-DISTRESS` | Indirect bankruptcy cost | Rating, EBITDA haircut under low, medium and high severity | No |
| `D-RDLIFE` | R&D amortizable life by industry | Industry, life in years, two to ten | No |
| `D-CPXSEC` | Sector capital-expenditure ratios | Sector, capital expenditure over depreciation, net capital expenditure over sales, net capital expenditure over after-tax EBIT | No |
| `D-MACRO` | Sector macro sensitivities by SIC | Sector, duration, cyclicality, inflation and currency coefficients, for firm value and for operating income | No |
| `D-MULTREG` | Market-wide and regional multiple regressions | Region, fitted equations for price-earnings, PEG, price-to-book, EV/EBITDA, EV/Sales, EV/Invested Capital, with R² | Yes |
| `D-DEBTREG` | Market-wide debt-ratio regression | Coefficients on the effective tax rate, growth, institutional holdings, earnings variance, EBITDA over enterprise value | Yes |
| `D-PAYREG` | Market payout and yield regressions | Coefficients on beta, expected growth, debt-to-capital, with R² | Yes |
| `D-ILLIQ` | Illiquidity regressions | The restricted-stock regression; the bid-ask-spread regression coefficients | No |
| `D-SURV` | Sector and startup survival tables | Years since founding, survival rate, by sector | No |
| `D-DISTRIB` | Multiple distribution statistics by region | Multiple, 10th, 25th, median, 75th and 90th percentiles, share of firms with a computable value | Yes |

## Load groups

| Load | Datasets | Keyed by | Freshness limit |
|---|---|---|---|
| Risk premiums | `D-ERP`, `D-CTRY`, `D-SOVSPR` | date, country | One month for the implied premium; six months for the country tables, published each January and July |
| Credit | `D-RATE1`, `D-RATE2`, `D-RATE3`, `D-SPREAD`, `D-DEFPROB` | date, coverage bracket, rating | Spreads at the valuation date. The coverage brackets themselves are stable across vintages |
| Industry | `D-INDUS`, `D-GLOB`, `D-CPXSEC`, `D-RDLIFE`, `D-MACRO` | industry name, SIC | Twelve months, on the January snapshot |
| Pricing | `D-MULTREG`, `D-DISTRIB` | region, multiple | Twelve months |
| Corporate finance | `D-TAX`, `D-DEBTREG`, `D-PAYREG`, `D-DISTRESS` | country, region | Twelve months, or immediately on a known statutory tax change |
| Special situations | `D-ILLIQ`, `D-SURV` | — | Structural. No limit |

## Rules

**One vintage.** Every vintage-critical table shares a single `as_of`. Stated as a
predicate over the set
`{D-ERP, D-CTRY, D-SOVSPR, D-RATE1, D-RATE2, D-RATE3, D-SPREAD, D-MULTREG, D-DISTRIB}`:
`max(as_of) − min(as_of) ≤ 3 months` and `valuation_date − min(as_of) ≤ 12 months`. A
violation fails at `G4_discount_rate`.

**Staleness.** When a vintage-critical table is more than a year older than the valuation
date, attempt a refresh from the publisher. On failure, continue with `status: stale` and
disclose the vintage in the report.

**Spreads move.** Default spreads roughly doubled to tripled at every rating between
January 2008 and January 2009, and spiked and reverted inside 2020. Never carry last year's
spread table. Mixing a current premium with old spreads, or the reverse, is inconsistent in
a way that survives review unnoticed.
See `knowledge/concepts/cost-of-debt-capital/default-spreads-over-time.md`.

**Reproduce anomalies.** Some published synthetic-rating tables carry non-monotonic labels
or spreads below the B3 bracket. Ship the table verbatim and flag the anomaly. A silent fix
cannot be reconciled against the source.
See `knowledge/concepts/cost-of-debt-capital/synthetic-rating.md`.

**Recomputation.** The implied equity risk premium can be rebuilt rather than looked up. It
needs the index level, the base cash flow of dividends plus buybacks, a consensus growth
path from `E-IDXCONS`, and a terminal growth rate set to the riskfree rate. Buybacks are
not optional in the base cash flow; leaving them out roughly halves the premium.
See `knowledge/concepts/cost-of-equity/implied-equity-risk-premium.md`.

**Country premiums.** The country premium is the sovereign default spread scaled by a
relative equity volatility multiplier. Use the local-currency sovereign rating, not the
foreign-currency one. A country rated Aaa carries a country premium of zero. Attach the
premium by operation weights rather than by country of incorporation.
See `knowledge/concepts/cost-of-equity/country-risk-premium.md`.

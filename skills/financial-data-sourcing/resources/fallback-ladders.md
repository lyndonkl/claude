# Fallback ladders and refresh policy

Two tables. The first is what to substitute when a primary source fails, ordered by how
much the substitution costs the analysis. The second is how stale each input may be before
it must be refetched.

## The ladder table

Walk left to right. Record the rung you stopped at, in `gaps.json` and in `sources.md`.

| Missing | Ladder, best first | Cost of the last rung |
|---|---|---|
| Riskfree rate | Aaa sovereign ten-year rate, then the minimum across same-currency sovereigns, then the local rate less the sovereign spread taken from a market measure and then a rating, then an inflation-plus-real build-up, then differential inflation from the US dollar, then a currency switch | Every other input must be restated in the new currency |
| Mature-market equity risk premium | Current implied premium, then the average implied premium over a stated window, then the historical geometric premium over bonds on the longest window | The historical premium is negatively correlated with future returns |
| Country risk premium | `D-CTRY` on the local-currency rating, then the credit default swap spread net of the US spread, then a hard-currency bond spread, then the PRS composite score | The PRS mapping is coarse |
| Unlevered beta | The comparable median, cash-corrected, then the `D-INDUS` or `D-GLOB` industry beta, then a regression beta unlevered at the window-average debt-to-equity ratio | A regression beta measures a company that may no longer exist |
| Market debt-to-equity | Market equity plus market debt, then the industry median, then a target ratio | Book debt-to-equity is never acceptable |
| Cost of debt | A straight-bond yield, then a global rating spread, then a recent bank loan rate, then a synthetic rating, then a local rating plus lambda times the sovereign spread | A synthetic rating uses one ratio where an agency uses many |
| Debt maturity | The disclosed schedule's weighted average, then three years | Biases the market value of debt |
| Lease debt | The present value of disclosed commitments at the pre-tax cost of debt, then the reported lease liability, then zero | Zero understates debt and overstates both return on capital and the equity weight |
| Working-capital ratio | The firm's three-to-five-year average, then the industry ratio of non-cash working capital to revenues, then zero | A wrong sign here compounds through every forecast year |
| Capital-expenditure forecast | The reinvestment rate implied by growth and return, then firm history, then the `D-CPXSEC` sector ratios, then net capital expenditure of zero | Zero net capital expenditure is consistent only with roughly zero real growth |
| Sales-to-capital | The firm's own ratio, then `D-INDUS`, then the industry median | It drives the whole reinvestment path in a revenue-driven forecast |
| Growth rate | Fundamentals, meaning the reinvestment rate times the return on capital, then analyst consensus converted to the right claimholder, then the historical geometric rate | Historical growth off a small or negative base is meaningless |
| Terminal growth | Explicit judgment, capped, then the riskfree rate | Never above the riskfree rate |
| Terminal return on capital | Explicit judgment, then the terminal cost of capital | It neutralises growth, which is the honest default |
| Failure probability | Bond-implied, then the rating cumulative default rate, then sector survival tables | Rating tables are class averages and usually optimistic |
| Volatility | The firm's own implied or historical volatility, then the industry standard deviation of equity | Firm-value variance is not equity variance at high leverage |
| Comparable R² | Comparable regressions, then `D-INDUS` | Without it a total beta cannot be computed at all |
| Peer multiples | The screened peer set, then the industry row, then the regional regression | The regional regression ignores sector membership entirely |
| Governance score | `E-GOV`, then the red-flag checklist alone | Loses the peer benchmark, keeps the substance |
| Macro sensitivities | Firm regressions with a t-statistic above two, then the `D-MACRO` sector coefficients, value-weighted | Firm-level insignificant slopes are worse than the sector average |

## Refresh and freshness

| Data | Limit relative to the valuation date | On breach |
|---|---|---|
| Price, shares, market capitalization | One trading day | Refetch |
| Government bond yields, credit default swaps, the Baa spread | One trading day | Refetch |
| Corporate rating spread tables | At the valuation date | Refetch. If impossible, mark stale and disclose |
| Implied equity risk premium | One month, and re-estimate on any material index move | Recompute from the index level, the base cash flow, consensus growth, and a terminal growth rate equal to the riskfree rate |
| Country premiums and sovereign spreads | Six months, published each January and July | Recompute from credit default swaps or hard-currency bond spreads |
| Industry averages | Twelve months, on the January snapshot | Mark stale and disclose |
| Multiple regressions | Twelve months. Coefficients drift hard | Mark stale and weight the prediction down |
| Payout and debt-ratio regressions | Twelve months | Mark stale |
| Tax rates | Twelve months, or immediately on a known statutory change | Refetch |
| Filings | A new annual report within ninety days of the fiscal year end; a new quarterly filing within forty-five days of the quarter end | Rebuild the trailing twelve months |
| Analyst consensus | One month | Refetch |
| Ownership filings | One quarter | Refetch |
| Proxy statement | Twelve months | Refetch |
| Survival, illiquidity, R&D-life and distress-cost tables | No limit. These are structural | — |

Spreads deserve their tight limit. They roughly doubled to tripled at every rating between
January 2008 and January 2009, and spiked and reverted inside 2020. A rating-based cost of
debt is only as current as the spread table behind it.
See `knowledge/concepts/cost-of-debt-capital/default-spreads-over-time.md`.

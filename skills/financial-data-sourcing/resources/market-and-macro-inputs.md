# Market and macro inputs

Stages A4 and A5. Class MK throughout, except where a filing is the source. User column:
`Y` accept at face value, `Y*` accept after validation, `N` derive.

---

## A4 — Company market data

| Field | Units | Source | Frequency | User? | Fallback |
|---|---|---|---|---|---|
| `price` | ccy per share | `M-PX` | daily | Y | BLOCK for a public firm |
| `shares_outstanding`, actual rather than weighted average | count | `M-PX` or the `F-10K` cover page | quarterly | Y | BLOCK |
| `market_cap` | ccy | derived | daily | N | Price times shares |
| `return_series`, dividend- and split-adjusted | decimal per interval | `M-PX` | daily to monthly | Y* | Blocks the regression beta and Jensen's alpha. The bottom-up beta is unaffected |
| `index_return_series` | decimal per interval | `M-IDX` | daily to monthly | Y* | Same |
| `traded_bonds[]`: price, coupon, maturity, straight flag, liquidity flag | mixed | `M-BOND` | daily | Y* | Empty, which sends the cost of debt to the rating or synthetic route |
| `issuer_rating`: agency, scale, date | rating symbol plus enum global or local-scale | `M-RATING` | on event | Y* | Empty, which forces a synthetic rating |
| `issue_ratings[]` | rating symbols | `M-RATING` | on event | Y* | Take the median when they differ |
| `implied_volatility` or `historical_volatility`, annualized | decimal | `M-PX` or the options market | daily | Y | The industry standard deviation of equity from `D-INDUS` |
| `dividend_history`: dividend per share and ex-dates, ten years | ccy per share | `M-PX` | quarterly | Y | Cash-flow-statement dividends |
| `preferred.shares`, `.price`, `.annual_dividend` | mixed | `M-PX` or `F-10K` | quarterly | Y | 0 |
| `convertible.book_value`, `.interest_expense`, `.maturity`, `.market_value` | mixed | `F-DEBT` plus `M-BOND` | annual | Y | Treat it wholly as debt only when the option is deeply out of the money. Otherwise flag it |

### Decision rules

**Regression parameters.** Default to five years of monthly returns. Record the estimation
period, the return interval and the index. The regression beta is a diagnostic, not the
hurdle-rate input. See `knowledge/concepts/cost-of-equity/regression-beta.md`.

**Index choice.** Use an index that represents the marginal investor's portfolio, not the
local exchange index for a globally held firm. Index choice moves betas by half a point on
identical data.

**Rating scale.** Tag every rating as global-agency or local-scale. A local-scale rating
does not embed sovereign risk; a global one does. That flag decides whether the country
default spread is added separately.
See `knowledge/concepts/cost-of-debt-capital/country-risk-in-cost-of-debt.md`.

**Bond usability.** A bond supports a yield-based cost of debt only when it is straight,
long-term and liquid. No conversion feature, no call or put, not floating. Anything else
carries option value inside its yield.

Concepts: `knowledge/concepts/cost-of-equity/regression-beta.md`, `.../jensen-alpha.md`,
`knowledge/concepts/cost-of-debt-capital/cost-of-debt-estimation-routes.md`,
`.../preferred-stock-cost.md`, `.../convertible-debt-decomposition.md`.

---

## A5 — Macro and currency data

Fetched per currency and per operating country, keyed to the valuation date.

| Field | Units | Source | Frequency | User? | Fallback |
|---|---|---|---|---|---|
| `riskfree.gov_bond_10y[currency]` | decimal | `M-RATE` | daily | Y | The ladder below |
| `riskfree.tips_yield[currency]` | decimal | `X-BREAK` | daily | Y | A real riskfree rate near long-term real GDP growth |
| `sovereign.local_currency_rating[country]` | Moody's symbol | `M-RATING` | on event | Y* | Convert the S&P rating to its Moody's equivalent. If unrated, use the PRS composite score |
| `sovereign.foreign_currency_rating[country]` | Moody's symbol | `M-RATING` | on event | Y* | None. Do not substitute it for the local-currency rating |
| `sovereign.cds_10y[country]` and `[US]` | decimal | `M-CDS` | daily | Y | The rating-based lookup `D-SOVSPR` |
| `sovereign.hard_currency_bond_spread[country]` | decimal | `M-BOND` | daily | Y | The credit default swap or rating route |
| `inflation.expected_long_run[currency]` | decimal | `X-CB`, `X-BREAK`, `X-IMF` | quarterly | Y | The central bank target, then the breakeven rate, then five-year trailing inflation |
| `real_gdp_growth.expected[country]` | decimal | `X-IMF` or `X-CB` | quarterly | Y | The trailing ten-year average |
| `baa_spread` | decimal | `X-FRED` or `M-CRED` | daily | Y | Used only for the equity risk premium cross-check |
| `fx_spot[pair]`, `fx_forward[pair]` | rate | `M-FX` | daily | Y | Spot only, which closes the forward route |
| `macro_series`: ten-year rate changes, real GDP growth, inflation changes, trade-weighted dollar change, twenty or more years | mixed | `X-FRED` | annual | Y* | Blocks firm-level macro regressions. Fall back to the `D-MACRO` sector coefficients |

### The riskfree ladder

Work down in order and record the rung you stopped at.

1. The sovereign issuing in this currency is rated Aaa in local currency. Its ten-year bond
   rate is the riskfree rate. Stop.
2. Several sovereigns issue in this currency, as with the euro. Take the minimum ten-year
   rate across them. Do not average, and do not default to the home sovereign.
3. The sovereign is below Aaa. The riskfree rate is the local ten-year rate less the
   sovereign default spread. Three routes give that spread: the sovereign's hard-currency
   bond spread over the matching Treasury, its credit default swap spread net of the US
   spread, or a `D-SOVSPR` lookup on the local-currency rating. Prefer a market measure.
   Report the range across every route available.
4. No trustworthy local bond rate exists. Build up from expected inflation plus an expected
   real rate. Or convert from the US dollar riskfree rate by the inflation differential. Or
   use covered interest parity from forward rates. Or switch the valuation currency and
   restate every other input.

### Further rules

**No normalization.** Do not substitute a normalized historical riskfree rate for the
observed one. If a user insists, normalize the riskfree rate, inflation, real growth and
the equity risk premium together, and label the output a valuation of a hypothetical
economy. See `knowledge/concepts/cost-of-equity/riskfree-rate-normalization.md`.

**Negative rates.** Use a negative ten-year rate as observed. Do not floor it at zero.
Check that the growth and inflation assumptions in that currency are near zero too.

**Maturity.** Ten years is the convention for a going-concern valuation. Use a short rate
only for a genuinely short-horizon analysis.

Concepts: `knowledge/concepts/cost-of-equity/riskfree-rate-fundamentals.md`,
`.../currency-riskfree-rate.md`,
`knowledge/concepts/cost-of-debt-capital/currency-conversion-of-discount-rates.md`.

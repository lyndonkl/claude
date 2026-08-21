# Inputs by company type

Classification adds inputs on top of the standard stages. More than one branch can be live
at once, and their input sets compose. The routing rules themselves live in
`knowledge/frameworks/special-situations-routing.md`; this file covers only what to collect.

---

## Financial-service firms

Triggered by a banking, insurance or brokerage classification, or by revenue reported as
net interest income plus net fee income. Constraints: no firm-level cash flow valuation, no
optimal debt ratio.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `net_interest_income`, `net_fee_income`, `trading_income` | ccy | `F-10K` | Y | BLOCK. There is no cost of goods and no gross profit here |
| `credit_loss_provision` | ccy | `F-10K` | Y | A recurring operating expense, never an extraordinary item |
| `risk_weighted_assets` | ccy | regulatory disclosures | Y | Total assets times a stated risk weight |
| `tier1_capital`, `tier1_ratio` | ccy, decimal | regulatory disclosures | Y | BLOCK |
| `regulatory_minimum_ratio` | decimal | the regulator | Y | The Basel minimum plus a stated buffer |
| `target_tier1_ratio_path[t]` | decimal | judgment | Y | Ramp from current to target across the forecast. The ramp is often a larger reinvestment than asset growth itself |
| `asset_growth_path[t]` | decimal | judgment | Y | Nominal GDP growth for a mature bank |
| `roe_path[t]` | decimal | judgment | Y | Converge to the cost of equity or to a normalized industry level |
| `book_equity[t]` | ccy | derived, recursive | N | Prior book equity plus the investment in regulatory capital |
| `long_term_interest_expense` | ccy | `F-DEBT` | Y* | Needed for any synthetic rating attempt, and only against `D-RATE3` |

Reinvestment here is the investment in regulatory capital, which is the change in
risk-weighted assets times the tier-one ratio. Regulatory ratios are stated on book values,
so a market-value optimal debt ratio can breach a binding constraint.
Concepts: `knowledge/concepts/dividend-policy/fcfe-for-banks.md`,
`knowledge/concepts/dark-side-difficult/bank-fcfe-and-excess-return-models.md`.

---

## Young and negative-earnings firms

Triggered by non-positive operating or net income, or by expected revenue growth above
twenty-five percent. Constraints: no earnings multiple, no standard growth model, a failure
probability is required.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `total_addressable_market`, `market_growth_rate` | ccy, decimal | `E-MKT` | Y | BLOCK. The forecast has no anchor without it |
| `target_market_share[milestone_year]` | decimal | judgment | Y | BLOCK |
| `target_operating_margin` | decimal | mature peers with the same business model | Y | The industry after-tax operating margin. State the peer percentile used |
| `margin_convergence_year` or `speed_of_convergence` | year or parameter | judgment | Y | Linear to the target by year ten |
| `sales_to_capital[phase]` | ratio | `D-INDUS` | Y | The industry average, which may vary by phase |
| `nol_carryforward` | ccy | `F-TAX` | Y | 0 |
| `failure_probability` | decimal | `D-SURV`, or bond-implied | Y | The sector survival rate over the forecast horizon |
| `distress_recovery_pct` | decimal | judgment | Y | 50 percent |
| `distress_proceeds_basis` | enum: book, going-concern | judgment | Y | Book value of equity plus debt, times the recovery rate |
| `dilution_from_future_equity` | ccy or share count | judgment | Y | Required for any forward-multiple valuation |

Concepts: `knowledge/concepts/dark-side-difficult/young-company-valuation.md`,
`knowledge/concepts/dcf-cashflows-growth/top-down-revenue-growth.md`.

---

## Distressed firms

Triggered by high market leverage combined with weak earnings, coverage below one, a
distressed rating, or a bond trading far below par.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `traded_bond.price`, `.coupon`, `.maturity`, `.face` | mixed | `M-BOND` | Y | The rating-based cumulative default probability from `D-DEFPROB` |
| `annual_distress_probability` | decimal | derived by inverting the bond price at the riskfree rate | N | Annualized from the `D-DEFPROB` cumulative rate |
| `cumulative_distress_probability` | decimal | derived | N | The ten-year rate for the rating |
| `distress_sale_proceeds` | ccy | judgment | Y | A percentage of book value. That percentage falls in a weak economy and when peers are also distressed |
| `face_value_of_debt` | ccy | A3 | Y | Book debt |
| `equity_option_inputs`: asset value, face value of debt, weighted debt life, firm-value variance | mixed | the DCF plus A3 plus `D-INDUS` | Y* | Industry-average stock and bond volatilities. Never the firm's own equity volatility as the asset volatility |

A market-implied probability far more pessimistic than the rating table is information, not
an error. Concepts: `knowledge/concepts/dark-side-difficult/bond-implied-distress-probability.md`,
`knowledge/concepts/real-options/equity-as-call-option.md`.

---

## Cyclical and commodity firms

Triggered when the operating margin range across three to five years spans a factor of
roughly one and a half or more, or when the firm is a commodity producer.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `ebit_history[N]`, `margin_history[N]`, `roc_history[N]` | mixed | A2 | Y | BLOCK. Normalization needs a full cycle |
| `normalization_window` | years | judgment | Y | Five years. Longer for a deep commodity cycle. Use the pre-shock cycle where a specific shock hit |
| `normalization_method` | enum: dollar-average, return-based | judgment | Y* | Dollar averaging when firm size is stable; the return-based method when size changed materially |
| `commodity_price_current`, `.normalized` | price | a commodity feed | Y | Value at today's price and disclose the assumption |
| `revenue_to_price_regression` | slope | derived from history | Y* | Skip it and normalize margins only |
| `normalized_effective_tax_rate` | decimal | averaged over the same window | Y | The marginal rate |

Normalize only when the cause is transient. A structural cause — life cycle, leverage, a
long-term operating problem — needs the revenue-driven route instead.

---

## Emerging-market exposure

Triggered when any operating country carries a non-zero country risk premium.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `sovereign.local_currency_rating` | Moody's symbol | `M-RATING` | Y | The S&P conversion, then the PRS composite score |
| `sovereign_default_spread` | decimal | `M-CDS` net of the US spread, a hard-currency bond spread, or `D-SOVSPR` | Y | The rating table. Report the range across all three routes |
| `relative_equity_volatility_multiplier` | ratio | `D-CTRY` | Y | The country-specific ratio of equity to bond volatility |
| `country_erp[country]` | decimal | `D-CTRY` | Y | Mature premium plus spread times the multiplier |
| `revenue_by_country`, `production_by_country`, `assets_by_country` | decimal shares | `F-SEG` or operating statistics | Y | Country of incorporation at one hundred percent, heavily flagged |
| `lambda` | decimal | a return regression on the sovereign bond, or the domestic revenue ratio | Y | 1.0 |
| `expected_inflation[local]`, `[USD]` | decimal | `X-CB`, `X-IMF`, `X-BREAK` | Y | Central bank targets |
| `truncation_scenarios[]`: nationalization or regime-change probability and payoff | decimal, ccy | judgment | Y | None. Flag a politically exposed asset |

Single-count rule N2 dominates here. The sovereign spread is stripped from the riskfree
rate, or it sits in the equity risk premium — never both, and never also in the cash flows.
Concepts: `knowledge/concepts/cost-of-equity/country-risk-premium.md`,
`knowledge/concepts/dark-side-difficult/currency-consistency-and-invariance.md`.

---

## Private companies and non-traded assets

Triggered by the absence of a traded price series. Constraints: a total beta is required
unless the buyer is diversified; an illiquidity discount is required unless the buyer is
public and liquid.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `owner_compensation_actual`, `market_salary_for_the_role` | ccy | filings, user, or a market survey | Y | BLOCK the cleanup step |
| `personal_expenses_in_the_statements` | ccy | user | Y | 0, flagged |
| `comparable_median_r_squared` | decimal | Set 1 regressions | Y | The industry implied value. Without it the total beta cannot be computed |
| `assumed_market_de` | decimal | the industry median from `D-INDUS` | Y | Never the private firm's own book debt-to-equity |
| `equity_value_proxy` | ccy | a comparable multiple times the matching fundamental | Y | BLOCK the debt ratio |
| `buyer_type` | enum: private, public acquirer, private equity or venture, IPO | user | Y | BLOCK. It sets the beta, the tax rate and every discount |
| `stake_pct` | decimal | user | Y | 100 percent |
| `illiquidity_route` | enum: flat, restricted-stock regression, bid-ask regression | judgment | Y | The bid-ask regression when revenues, profitability and cash are known |
| `key_person_share_of_business` | decimal | judgment | Y | 0. It applies to operating income, not to value |

Clean the statements first: a market salary for the owner, capitalized leases as the often
only debt, personal expenses removed. Buyer type flips the answer. A public acquirer gets a
market beta and no illiquidity discount; a private buyer gets a total beta and a discount.
Illiquidity and minority discounts stay separate.
Concepts: `knowledge/concepts/asset-based-private/private-company-valuation-framework.md`,
`.../illiquidity-discount.md`.

---

## Multi-business firms

Triggered by more than one segment with materially different business risk.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `segments[].revenues`, `.operating_income`, `.identifiable_assets`, `.investments`, `.capex`, `.depreciation` | ccy | `F-SEG` | Y | BLOCK the branch |
| `segments[].industry_key` | `D-INDUS` name | mapping | Y* | BLOCK |
| `segments[].peer_ev_sales` | ratio | `D-INDUS` | Y | Revenue weights, a crude substitute |
| `segments[].unlevered_beta` | decimal | Set 1 per business | Y | The industry unlevered beta |
| `debt_allocation_key` | enum: identifiable assets, sales, EBITDA, target ratio | judgment | Y | Identifiable assets. State the key, since it drives divisional leverage directly |
| `capitalized_corporate_expenses` | ccy | the `F-SEG` corporate column | Y | Allocate or capitalize, and state which |

Business value is segment revenue times the peer EV/Sales ratio. The firm's unlevered beta
is the value-weighted average of the business betas, never the revenue-weighted average
when margins differ. Watch for allocation artifacts, such as a divisional debt-to-equity
ratio above one hundred percent producing an implausibly low cost of capital.

---

## Real options

Collect nothing until the three-part gate passes. First, there must be a named underlying
asset whose value changes unpredictably, with a payoff contingent on a specified event
inside a finite period. Second, the option must have economic value, which turns on a
restriction on competition: full exclusivity gives full value, no barriers give zero
however volatile the underlying. Third, an option pricing model must be able to price it.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `S`, the value of the underlying | ccy | the DCF | Y | BLOCK |
| `K`, the exercise cost | ccy | project data | Y | BLOCK |
| `T`, the life of the right | years | the contract | Y | BLOCK |
| `sigma`, the variance of the underlying's value | decimal | commodity volatility, sector firm-value volatility, or simulation | Y* | The industry standard deviation. This is the least reliable input |
| `y`, the cost of delay | decimal | derived | Y | One divided by the years of exclusivity remaining |
| `r`, the riskfree rate at the option's maturity | decimal | A5 | Y | The ten-year rate |
| `exclusivity_factor` | 0 to 1 | judgment | Y | Scaled along the barrier ladder |

Concepts: `knowledge/concepts/real-options/real-options-framework.md`,
`.../opportunities-are-not-options.md`.

---

## Acquisition, control and synergy

Triggered by `mode = acquisition` or `mode = restructuring`, or by an activist question.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| The target's full A2 to A8 set | — | — | — | BLOCK |
| The acquirer's full A2 to A8 set | — | — | — | Required for synergy, not for the value of control alone |
| `target_optimal_policy`: optimal debt ratio, target return on capital, target reinvestment | mixed | run on the target | N | — |
| `probability_of_management_change` | decimal | judgment, or inverted from the market price | Y | Read it out of the price, where price equals status quo plus the probability times the gain |
| `synergy_assumptions`: which growth rate, margin, return, reinvestment, tax rate or debt ratio changes, by how much, and when | mixed | judgment | Y | BLOCK. An unnamed synergy cannot be valued |
| `combined_unlevered_beta` | decimal | value-weighted average of the two | N | — |
| `combined_debt_ratio` | decimal | the deal financing plan | Y | Value-weighted current ratios |
| `nol_target` and acquirer taxable income | ccy | `F-TAX` | Y | 0 |
| `share_classes[]`: voting rights, economic rights, prices | mixed | `F-PROXY` or `M-PX` | Y* | A single class |
| `transaction_multiples[]` from precedent deals | ratio | deal databases | Y* | Sector multiples, flagged as pricing rather than valuation |

Discount the target at the target's own risk and debt capacity, never the acquirer's. Four
numbers are required: the status quo value, the restructured value, the synergy value, and
the price. Concepts: `knowledge/concepts/acquisitions-control-enhancement/valuing-synergy.md`,
`.../target-discount-rate-discipline.md`.

# Ownership, governance and peer inputs

Stages A7 and A8.

---

## A7 — Ownership, governance and the marginal investor

Required for `mode = corporate-finance`, and for any run where the marginal-investor
question is live: private firms, closely held firms, family groups.

| Field | Units | Source | Frequency | User? | Fallback |
|---|---|---|---|---|---|
| `ownership.institutional_pct_shares` | decimal | `M-OWN` | quarterly | Y | The industry average for institutional holdings |
| `ownership.institutional_pct_float` | decimal | `M-OWN` | quarterly | Y | Same |
| `ownership.insider_pct` | decimal | `M-OWN` or `F-PROXY` | quarterly | Y | Same |
| `ownership.individual_pct` | decimal | derived | quarterly | N | One less institutional less insider |
| `ownership.largest_holders[]`: name, percentage, type — index, activist, family, strategic | mixed | `M-OWN` | quarterly | Y* | Empty, which blocks the test of whether the largest holder is the marginal one |
| `governance.board[]`: member, employee flag, shares owned, other boards, tenure, age, attendance | mixed | `F-PROXY` | annual | Y* | Blocks the board table |
| `governance.exec_comp[]`: name, total compensation, performance-linked share, tenure | mixed | `F-PROXY` | annual | Y* | Blocks the risk-incentive read |
| `governance.provisions`: staggered board, majority vote, poison pill, dual-class shares, golden shares | booleans | `F-PROXY` or the charter | on event | Y* | Flag as unknown. Do not assume absent |
| `governance.quickscore`: overall plus five sub-scores | 1 to 10, 1 best | `E-GOV` | quarterly | Y | Skip it. The red-flag checklist still runs |
| `peer_governance_averages` | mixed | peer-set `F-PROXY` | annual | Y* | Skip the benchmark column |

### Reading the ownership data

**Marginal investor.** A high institutional share of float with a low insider percentage
means a diversified marginal investor, so the standard market beta applies. Low
institutional ownership with a founder or family who does not trade means an undiversified
marginal investor, which calls for a total beta even at a listed firm. A mixed picture
requires an explicit statement of the assumption and a sensitivity around it.
See `knowledge/concepts/cost-of-equity/capm-cost-of-equity.md`.

**Float artifacts.** Institutional ownership above one hundred percent of float is a
reporting artifact rather than an error. Do not clamp it.

**Institutional but undiversified.** A controlling stake held through a partnership or a
holding company is an undiversified holder, whatever the classification says.

**Governance scores.** A vendor score is an input to the read, not the verdict. Overriding
a bad score because real mitigants exist is legitimate. So is confirming it because the
policies are genuinely bad.

Concepts: `knowledge/concepts/governance-objective/ownership-and-control-structure-analysis.md`,
`knowledge/concepts/deliverables-worked-examples/stockholder-analysis-marginal-investor.md`,
`.../governance-analysis-deliverable.md`.

---

## A8 — Comparable firms

Two peer sets. They are not interchangeable, and using one where the other belongs is a
common and invisible error.

### Set 1 — Beta comparables

One set per business the firm operates in, for the bottom-up beta.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `beta_comps[].levered_beta` | decimal | `M-PX` regressions or `D-INDUS` | Y* | Use the industry unlevered beta directly and skip the firm-level assembly |
| `beta_comps[].market_de` | decimal | `M-PX` plus `F-10K` | Y* | The industry median market debt-to-equity from `D-INDUS` |
| `beta_comps[].marginal_tax_rate` | decimal | `D-TAX` | Y | The domicile marginal rate |
| `beta_comps[].cash_to_firm_value` | decimal | `F-10K` plus `M-PX` | Y* | Skip the cash correction and flag it |
| `beta_comps[].r_squared` | decimal | regression | Y* | Required for a total beta. Without it, that route is blocked |
| `beta_comps[].se_beta` | decimal | regression | Y* | The bottom-up standard error cannot be reported |

**Median, not mean.** One comparable with a debt-to-equity ratio in the hundreds of percent
destroys an average.

**Sample width.** Cast the net wide — global, with a market-capitalization floor — because
business risk travels across borders while country risk belongs in the premium. Ten to
several hundred firms is normal. The standard error of the median falls with the square
root of the count. See `knowledge/concepts/cost-of-equity/bottom-up-beta.md`.

**Banks.** Do not unlever a bank beta. Use median levered comparable betas weighted by net
revenues.

### Set 2 — Pricing comparables

For relative valuation. Defined by fundamentals, not by sector code.

| Field | Units | Source | User? | Fallback |
|---|---|---|---|---|
| `price_comps[].market_cap`, `.net_debt`, `.cash`, `.enterprise_value` | ccy | `M-PX` plus `F-10K` | Y* | BLOCK for enterprise-value multiples |
| `price_comps[].revenues`, `.ebitda`, `.ebit`, `.net_income`, `.book_equity`, `.invested_capital` | ccy | `F-10K` | Y* | BLOCK |
| `price_comps[].roe`, `.roic`, `.operating_margin`, `.net_margin` | decimal | derived | N | — |
| `price_comps[].expected_growth` | decimal | `E-CONS` | Y* | Fundamental growth: retention times return on equity, or the reinvestment rate times return on capital |
| `price_comps[].payout_ratio`, `.buybacks`, `.fcfe` | mixed | `F-10K` | Y* | Blocks the payout peer analysis |
| `price_comps[].beta`, `.debt_to_capital`, `.effective_tax_rate` | decimal | mixed | Y* | Industry averages |
| `price_comps[].std_dev_equity` | decimal | `M-PX` | Y | `D-INDUS` |

**Screen definition.** A comparable is a firm with similar risk, growth and cash-flow
characteristics, not a firm in the same sector. Record the screen explicitly: sector,
geography, size floor, growth band. It is the most challengeable part of the analysis.
See `knowledge/concepts/relative-valuation/comparable-selection-and-controls.md`.

**Sample cleaning.** Drop a firm where the multiple is not computable — negative earnings
for a price-earnings ratio, negative book value for price-to-book, negative EBITDA for
EV/EBITDA — and record the count. When most of the universe drops out, the survivors are
profitable survivors, and any conclusion describes only them.
See `knowledge/concepts/relative-valuation/multiple-distribution-statistics.md`.

**Non-positive free cash flow to equity.** Report `NA` rather than zero for a peer's
cash-return ratio when its free cash flow to equity is not positive, and exclude it from
the group statistic. See `knowledge/concepts/dividend-policy/peer-group-payout-analysis.md`.

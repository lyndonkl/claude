# Asset-based valuation and private company valuation — concept index

Determinism flag: **D** = fully deterministic given named inputs; **M** = mixed (deterministic core, judgment inputs); **J** = judgment-led framework.

| Slug | What it covers | Flag |
|---|---|---|
| [[asset-based-valuation-overview]] | The three ways to value a business; the three motives for asset-based valuation; the three mechanics (intrinsic, relative, accounting); the separability / traceable-cash-flow / active-market feasibility test | J |
| [[liquidation-valuation]] | Piecemeal sale value; price the assets rather than value them; book value as fallback; the extra discount when liquidation is urgent | M |
| [[fair-value-accounting-fas157]] | Fair value as an exit price; the level 1/2/3 measurement hierarchy; why it tilts to relative valuation; reverse engineering | J |
| [[sum-of-the-parts-framework]] | Motive determines route — passive investor uses intrinsic, activist uses relative; the four-number comparison; the conglomerate discount | J |
| [[sum-of-the-parts-pricing]] | Pricing divisions off sector medians, then off sector regressions evaluated at each division's own fundamentals; the equity bridge (UTC, GE) | D |
| [[sum-of-the-parts-dcf]] | Divisional costs of capital, ROC and reinvestment, the zero-growth rule for divisions below cost of capital, capitalized corporate expenses, the equity bridge (UTC, GE) | M |
| [[private-company-valuation-framework]] | Same process, two structural problems (no market value, weak statements); motives; the four transaction scenarios and what each implies for beta and discounts | J |
| [[total-beta]] | Market beta ÷ correlation with the market (= sqrt of the comparables' R²); why an undiversified owner prices total risk; partial diversification | D |
| [[private-company-cost-of-capital]] | Assembling the rate: bottom-up beta → total beta → industry D/E → cost of equity; coverage ratio with leases as interest → synthetic rating → cost of debt → WACC. Includes the rating/spread table | D |
| [[private-company-statement-cleanup]] | Market salary for owner labour, capitalizing operating leases as debt, removing personal expenses, short-history caution | D |
| [[key-person-discount]] | Haircut operating income by the share of the business that leaves with the owner; why it lands on income, not on value; mitigation through deal structure | M |
| [[illiquidity-discount]] | Why the flat 20–30% rule is wrong; the company/time/buyer dimensions; the three estimation routes and the restaurant comparison; when no discount applies | M |
| [[silber-restricted-stock-regression]] | Restricted-stock and pre-IPO discount evidence; the Silber regression; the extended discount-by-revenue table; the sampling-bias critique | D |
| [[bid-ask-spread-illiquidity-regression]] | The spread regression evaluated at zero trading volume as a firm-specific illiquidity discount | D |
| [[minority-discount]] | Value of control = optimal value − status quo value; majority stakes priced off optimal, minority stakes off status quo | D |
| [[private-to-private-valuation]] | The six-step end-to-end procedure, worked fully on the restaurant from reported statements to a final $453,880 | M |
| [[private-to-public-sale]] | Diversified buyer: market beta, buyer's tax rate, no illiquidity discount; the bargaining range; the partially diversified PE/VC bidder | M |
| [[ipo-valuation]] | Market beta, no illiquidity discount; the three IPO value adjustments — use of proceeds, prior equity claims, share count and options (Twitter) | M |
| [[ipo-pricing-and-underpricing]] | The banker's pricing guarantee; underpricing evidence by deal size; the winner's curse; the offering-quantity calculus; direct listings and SPACs | M |
| [[vc-stage-varying-cost-of-equity]] | Cost of equity falls as ownership moves founder → VC → public; cumulated discount factors; why one rate misvalues; implications for private company value | D |

## How these fit together

The area splits into two halves that share one idea: **value depends on who holds the asset and why you are asking.**

The **asset-based half** starts at [[asset-based-valuation-overview]], which sorts the work by motive. A liquidation motive leads to [[liquidation-valuation]]. An accounting mandate leads to [[fair-value-accounting-fas157]]. An investment or restructuring motive leads to [[sum-of-the-parts-framework]], which routes you to [[sum-of-the-parts-pricing]] if you are an activist who will sell the pieces, or to [[sum-of-the-parts-dcf]] if you are a passive investor waiting for a correction. In practice you run both and compare four numbers — intrinsic sum of the parts, relative sum of the parts, whole-company DCF, and market enterprise value. The spread is the finding.

The **private company half** runs as a pipeline. Start at [[private-company-valuation-framework]] to fix the motive and classify the deal into one of the four scenarios. Then clean the statements ([[private-company-statement-cleanup]]) — this must come first, because the capitalized lease debt and the market owner salary feed everything downstream. Strip key-person value from operating income ([[key-person-discount]]). Build the discount rate: [[total-beta]] for the risk measure, then [[private-company-cost-of-capital]] to assemble the levered beta, the synthetic-rating cost of debt, and the weights. Value the business, subtract debt, then apply the discounts the scenario calls for — [[illiquidity-discount]], estimated via [[silber-restricted-stock-regression]] or [[bid-ask-spread-illiquidity-regression]], plus [[minority-discount]] for a below-50% stake. [[private-to-private-valuation]] runs the whole pipeline end to end on the restaurant case.

The remaining three scenarios run the same pipeline with the rate and the discounts swapped out. [[private-to-public-sale]] uses the market beta and drops the illiquidity discount. That triples the value and opens a bargaining range. [[ipo-valuation]] does the same, then adds the three IPO-specific value adjustments. [[ipo-pricing-and-underpricing]] handles a separate question: what price the banker will actually set. [[vc-stage-varying-cost-of-equity]] generalizes the whole set. The discount rate is not one number. It is a schedule that falls as ownership moves from founder to VC to public markets.

## Scope boundary

This area covers the asset-based valuation section and the entire private company valuation module: spring-2021 packet pages 103–170 and spring-2020 packet pages 101–167.

Pages 81–102 (2021) and 81–100 (2020) of the same source files cover market-wide multiple regressions and the closing propositions on relative valuation. That material belongs to the **relative-valuation** area. Two notes covering it also sit in this directory and are listed below for completeness:

| Slug | What it covers | Flag |
|---|---|---|
| [[market-multiple-regression]] | Regressing a multiple on risk, growth and payout across a whole market; using predicted vs actual multiples; the market price of growth | D |
| [[peg-ratio-regression]] | Why PEG is not growth-neutral; regressing PEG on ln(growth), beta and payout | D |

[[sum-of-the-parts-pricing]] uses the same regression machinery, applied at the sector rather than the market level.

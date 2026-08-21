# Comparable-set and pricing-route bias

Relative valuation is where a conclusion is easiest to reverse-engineer. The peer set is
chosen, the multiple is chosen, and both choices happen after the analyst knows what answer
would be convenient. A cherry-picked set of six firms can justify almost any number.

Attack it in three layers: the multiple, the sample, and the comparison.

## Layer one — is this multiple allowed here

The route decides which multiples survive the company's defects. This is not a matter of
taste. Check the branch against the forbidden list before looking at any number.

| Route condition | Allowed | Forbidden |
|---|---|---|
| Negative or trough earnings | survival and growth proxies, forward multiples, whichever operating metric the market actually prices | price-earnings, price-earnings-to-growth, EV/EBIT, EV/EBITDA |
| Financial service firm | equity multiples only: price-to-book against return on equity, price-earnings | every enterprise multiple |
| Commodity or cyclical | multiples on normalized earnings, EV/EBITDA with a reinvestment control | current-year price-earnings at a cycle extreme |
| Intangible-heavy | multiples on restated earnings and capital, EV/Sales with a margin control | raw price-to-book, raw EV/Invested Capital on unrestated capital |
| Multi-business | each division priced off its own sector, then bridged once | one company-wide multiple |
| Emerging market or non-domestic | the regional regression, with the region assigned by operations | a United States regression on a firm that operates elsewhere |
| Private company | sector multiples with the same discounts as the intrinsic route | any multiple that assumes a traded market with no discount |
| Young or high-growth | forward multiples and market-implied metrics with survival proxies | raw price-to-sales regressed on a current loss-making margin |

A multiple on the forbidden list for the route is a `high` finding. It is the same failure
as A1, arriving through the pricing door.

## Layer two — is the sample honest

Rebuild the peer statistics rather than reading them. `relative-valuation-toolkit` gives you
four subcommands that make this quick.

| Subcommand | What it exposes |
|---|---|
| `multiples` | inconsistent numerator and denominator pairings, which it refuses outright |
| `peer-stats` | median, quartiles, skew, and the count of firms dropped from the sample |
| `locate` | where a multiple sits in the current bundled distribution |
| `regress`, `predict` | whether the fitted equation is strong enough to act on, and the over- or under-valuation it implies |

Then check five things.

**The drop-out count.** Multiples are undefined for firms with negative denominators, so
those firms leave the sample. They are usually the troubled ones, which biases the survivors
upward. The number dropped belongs in the write-up.

**Medians, not means.** These distributions are always right-skewed and comparable sets
routinely carry extreme outliers. A mean levered by one firm at 500% debt-to-equity is not
a benchmark.

**A current, local distribution.** A fixed threshold flips meaning across years and across
regions. "Under 12 times earnings is cheap" is a statement about one market in one year.

**Claimholder consistency.** Enterprise numerators need operating denominators. Equity
numerators need equity denominators. The `multiples` subcommand refuses the mismatches, so
a hand-built table is where they survive.

**Sample construction order.** Ask when the peer set was assembled relative to the target
price. A set built afterwards is the verdict-first pattern in relative-valuation clothing.

## Layer three — is the comparison controlled

A multiple is only a comparison if the differences that matter are controlled for.

Run the four-step discipline. Define the multiple and check the numerator and denominator
are consistent. Describe its current distribution. Analyse what drives it — growth, risk,
payout, return on equity. Apply it with those differences controlled, statistically once
more than one fundamental differs.

Two further checks belong here.

**Regression usability.** A low R-squared says the fitted equation does not explain the
cross-section, and a prediction from it is noise dressed as precision. Report the R-squared
alongside any predicted multiple. Judgment about whether it justifies acting is the
analyst's, but an unreported one is a finding.

**Intrinsic cross-check.** The `intrinsic` subcommand derives the multiple a firm's own
fundamentals justify. Where the traded multiple and the intrinsic multiple disagree, the
gap is the analysis. Averaging them is not.

## The transaction-multiple trap

In deal work a fourth failure appears. Precedent-transaction multiples are a sample of what
other acquirers paid, and acquirers on average overpay. Matching that sample replicates the
mistake with extra steps.

The same trap wears a discounted-cash-flow costume when terminal value is set at a multiple
of earnings. That imports today's market pricing into an intrinsic valuation and assumes it
holds forever. If an exit multiple has been used, back out the growth and return on capital
it implies and test those against a stable-growth firm.

## Reporting the verdict

A relative valuation states a verdict that is relative, never absolute. "Cheap against this
peer group on this multiple, with these controls" is a finding-free statement. "Cheap" on
its own is not.

Two final failures to check. The write-up should not average a discounted cash flow value
with a multiple-based price into one number. And where the two disagree, the difference has
to be explained rather than split.

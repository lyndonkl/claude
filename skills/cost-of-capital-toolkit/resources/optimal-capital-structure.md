# Optimal capital structure: the detail

SKILL.md covers the main line — run `debt-schedule`, read the curve, stress it or constrain
it, cross-check with `apv`. This file holds the parts that did not fit.

## Why a debt ratio has an optimum at all

Debt is cheaper than equity for two reasons and more expensive for one. Interest is tax
deductible, so the government pays part of the coupon. Fixed repayment obligations impose a
discipline on managers who would otherwise spend cash on empire-building. Against that,
every dollar of debt raises the odds of default, and default is expensive.

The first two effects are roughly linear in debt. The third is not: it stays near zero
while the rating is investment grade, then rises steeply. That asymmetry is what puts a
minimum in the cost-of-capital curve rather than pushing the answer to 0% or 100%.

## The circularity inside the schedule

At each candidate debt ratio the engine has to solve a loop, not evaluate a formula:

    debt ratio → dollar debt → interest rate → interest expense
                                   ↑                    ↓
                              default spread ← rating ← coverage ratio

Guessing an interest rate gives an interest expense, which gives a coverage ratio, which
gives a rating, which gives a spread, which gives a new interest rate. `solve_cost_of_debt`
iterates this to a fixed point. It converges because a higher rate lowers coverage, which
raises the rate by a smaller step each pass.

The loop can oscillate between two adjacent rating bands when the firm sits exactly on a
threshold. The iteration cap stops it, and the reported rating is then one of the two the
loop was flipping between. A rating that flips on a small change in EBIT is a signal, not
noise: the firm is on a knife edge at that leverage. Say so rather than smoothing it over.

## The enhanced approach: indirect bankruptcy costs

The standard schedule holds operating income fixed as the rating falls. That understates
the cost of leverage for firms whose customers care about survival. Nobody buys a
thirty-year warranty from a company that might not last thirty months.

The enhanced approach makes the feedback explicit. Operating income falls as the rating
deteriorates:

    EBITDA(d) = EBITDA_base × (1 + drop(rating(d)))
    EBIT(d)   = EBITDA(d) − depreciation

Typical severity assumptions at medium severity: no haircut at A2/A and above, −10% at
Baa2/BBB, −40% at Caa/CCC. High severity roughly doubles those. The choice of severity is a
judgment about the business, not a number to be looked up: airlines and capital-goods
makers sit at the high end, groceries and utilities at the low end.

This nests a second fixed point inside the first — rating sets the drop, the drop sets
EBITDA, EBITDA sets coverage, coverage sets the rating. The effect is always to move the
optimum to a lower debt ratio and to steepen the value cliff past it.

One normalisation matters. If the firm is *already* distressed at its current rating, its
reported EBITDA is already depressed, and applying the haircut again double-counts. Gross
the base up first:

    EBITDA_base = current EBITDA / (1 + drop(current rating))

## Choosing between the two protections

| | Stress test | Rating constraint |
|---|---|---|
| Protects against | operating income falling | operating income falling |
| Answers | how far can EBIT fall before the answer changes | what does a floor rating cost |
| Best for | firms with a long EBIT history to measure | firms whose management has a stated rating policy |

They guard the same risk. Use one. Applying both leaves the firm under-levered by an amount
nobody can account for.

The stress route needs the firm's own EBIT history. Compute the standard deviation of
annual percentage changes, then compare the safety buffer against three benchmarks: one
standard deviation, the worst single year on record, and the decline in the last recession.
A buffer that clears all three is real protection.

The constraint route needs a number from management, and it needs pricing. Report both the
cost of capital given up and the firm value given up. Then separate the reasons for the
floor. Protection against downside operating income is legitimate. A genuine feedback
effect from a ratings drop is legitimate too, but it belongs in the enhanced approach
instead. Wanting to say the company is AAA-rated is not a reason.

## Moving to the optimal ratio

Finding the optimum is the easy half. Three questions decide how a firm gets there.

**How fast?** Move immediately when the firm is under-levered and a hostile bidder would
notice the unused debt capacity, or when the gap is large and cash flows are stable. Move
gradually — through retained earnings and financing choices at the margin — when the firm
has good projects to fund, when its cash flows are volatile, or when the gap is small.
Near the flat bottom of the curve, the move is nearly free either way.

**Debt or equity, and in what form?** The direction is set by the gap. The form should match
the assets being financed — currency, duration and cyclicality all matter, and a mismatch
reintroduces the default risk the whole exercise was meant to price.

**Where does the money go?** Under-levered firms borrow to buy back stock or to fund
projects. Over-levered firms issue equity, cut dividends, or sell assets.

The use of proceeds does not change the optimal ratio. Business risk and the tax rate set
the optimum, so a buyback and a new plant give the same answer, as long as the projects sit
in the same business mix at the same tax rate. Recompute only when the firm moves into
genuinely different businesses.

## Where this does not apply

**Financial service firms.** Debt is raw material for a bank, not just financing, and
regulatory capital sets the mix. The calculation returns a number; the number means
nothing.

**Firms with negative EBIT.** Coverage is undefined, the synthetic rating pins to the
bottom of the scale, and every debt ratio prices at a distressed spread. Normalise earnings
first, or accept that the answer is zero debt.

**Firms at a cyclical peak.** An optimum computed on peak EBIT is the classic route to an
implausible 70% answer. This is exactly the case the stress test exists for.

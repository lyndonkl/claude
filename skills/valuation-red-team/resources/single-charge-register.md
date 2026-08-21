# The single-charge register

One risk, one charge. One benefit, one credit. Every failure in this file is the same error
in a different costume, and each one is quietly worth real money.

Work it as two passes. The first pass covers risks that can enter through more than one
channel. The second pass covers items that get counted twice on the way from operating
assets to value per share.

## Pass one — risks with more than one channel

Build the grid. One row per risk. One column per channel. Fill it from the artifacts. Any
row with two marks is a `high` finding.

| Risk | Channel A | Channel B | Channel C | Keep |
|---|---|---|---|---|
| Failure or distress | probability weight on the value | a raised discount rate | shrunken expected cash flows | the probability weight |
| Country risk | exposure-weighted premium in the cost of equity | a nationalization or truncation scenario | a blanket emerging-market haircut | premium, or scenario, never both plus a haircut |
| Governance | low returns on capital and a low probability of change | a discount-rate bump | a flat value haircut | the cash-flow route |
| Illiquidity | a discount on equity value | a total beta already raising the rate | — | check the overlap and argue it |
| Control | restructured value minus status quo | a fixed percentage premium | a management-quality premium | the derived difference |
| Complexity or opacity | lower cash flows | a higher rate | a shorter growth period | exactly one, and prefer fixing the model |
| Aggressive accounting | an earnings haircut | a higher rate | a failure probability | exactly one |
| Dilution from money-losing years | negative early free cash flow inside the model | a separate dilution haircut | a diluted share count | the negative cash flows |

Two of these deserve extra care.

**Country risk is the usual triple charge.** A premium in the cost of equity, plus a
nationalization scenario, plus a governance discount, is three charges for overlapping
risks. Composition arithmetic allows probability-weighted branches to stack
multiplicatively, but in practice two is the ceiling, and the second needs an argument that
the events are genuinely distinct.

**Failure risk is never a discount-rate matter.** Failure is not a marginal, diversifiable
risk that a beta can carry. Raising the rate and probability-weighting both charges for the
same event. The probability weight is the correct channel, and it also lets you state the
recovery basis explicitly.

## Pass two — the double-count register

Sixteen rows. Run every one as a pass or fail on the finished model.

| # | Double count | Where it hides | The fix |
|---|---|---|---|
| F1 | interest tax shield | in the after-tax cost of debt and added back in the cash flows | the shield lives only in the discount rate |
| F2 | cash | interest income left in the flows and cash added back in the bridge | strip the interest income, use the operating-asset beta |
| F3 | pension underfunding | counted as debt in the weights and subtracted in the bridge | the bridge only, once |
| F4 | employee options | option value subtracted and diluted shares used | subtract the value, divide by actual shares |
| F5 | brand or intangible value | inside margins and growth, and added as an asset | never add it; it is already in the flows |
| F6 | country risk | stripped from the riskfree rate, then re-added through both premium and beta | one declared channel |
| F7 | a possible market | raised the growth rate and added as option value | route each claim once |
| F8 | a cross-holding | equity income left in operating earnings and the stake's value added | strip the income, add the stake |
| F9 | complexity | rate raised and cash flows cut and a final haircut applied | exactly one channel |
| F10 | distress | failure probability applied and a distress-adjusted rate used | the probability branch |
| F11 | lease payment | reclassified out of operating costs and left in the forecast flows | net income must be unchanged by the capitalization |
| F12 | acquisition amortization | inside reported depreciation and subtracted again in net capital spending | check reported depreciation first |
| F13 | working capital | inside sales-to-capital reinvestment and subtracted again as a change in working capital | the sales-to-capital route already includes it |
| F14 | future equity grants | forecast as an expense and their shares added to the count | expense the future grants, count the past ones |
| F15 | control | value of control computed and a blanket premium added | the premium is the value of control |
| F16 | undiversification | total beta used and an illiquidity discount applied with no overlap check | check and state the overlap |

## Two arithmetic checks that expose the rest

Two identities catch a whole family of these without reading the prose.

**Lease capitalization leaves net income unchanged.** The adjustment moves the lease payment
between expense lines and creates an asset and a debt. If net income moved, the payment was
counted twice, which is F11.

**Research capitalization leaves free cash flow to the firm unchanged.** Earnings and
reinvestment rise by the same amount. What changes is operating income, invested capital,
return on capital and therefore growth. If free cash flow moved, one side of the adjustment
was skipped.

A related error is not a double count but its mirror: adding the research asset to capital
while leaving research spending out of capital expenditure. That manufactures free growth.
Check both sides of every capitalization.

## How to size a finding here

A double count is only worth a `high` severity if it moves the verdict. Quantify it before
you grade it. Re-run the model with the offending charge removed, using the same engine and
the analyst's own payload, and report the change in value per share inside the `evidence`
field. A finding that says "this is worth $3.10 a share, which closes 40% of the gap" gets
fixed. A finding that says "this is double counted" gets argued about.

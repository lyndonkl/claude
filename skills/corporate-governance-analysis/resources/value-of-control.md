# Pricing control

Knowing a firm would be worth more under better management is not enough. You also need the
odds that management actually changes. The expected value of control is the product of the
two. That single product explains four things at once. It sets what a hostile bidder can
pay. It explains why market prices sit between two valuations. It explains why voting shares
trade above non-voting shares. And it explains why minority stakes in private firms sell at
a discount.

Control has value only where there is a gap. A well-run firm offers none, whatever any
survey says about typical premiums.

## The two valuations

Everything here rests on running the same model twice.

**Status quo.** The firm as it is run and financed today. Base year normalized. Growth
earned rather than asserted, so that expected growth equals the reinvestment rate times the
return on capital. Cost of capital at the current structure. Terminal value under the usual
caps. Then the equity bridge and a comparison to market capitalization.

**Restructured.** The same model with the policy changes you can name. Every change lands
on exactly one of four levers.

| Lever | What moves | Discipline |
|---|---|---|
| Cash flows from existing assets | Operating margin, divestiture of negative-earnings assets, tax rate, capital spending, working capital | Benchmark each against the sector |
| Expected growth | Reinvestment rate, return on capital (margin times capital turnover) | Only raise reinvestment when return on capital exceeds the cost of capital |
| Length of the growth period | Brand, legal protection, switching costs, cost advantage | Name the advantage or leave the period alone |
| Cost of capital | Operating leverage, product discretionary-ness, the debt ratio, debt matched to assets | Take the ratio from the schedule, not from peers |

Anything that touches none of the four does not create value. It may still move the price.

Build both cases with `dcf-valuation-engine`, running `value` twice. Take the optimal debt
ratio from `cost-of-capital-toolkit`'s `debt-schedule` subcommand, and use its output for
the restructured cost of capital. Watch the rating cliff in that schedule: a ratio one step
past the optimum can cut firm value by a quarter.

Two sanity checks on the restructured case. Raising the reinvestment rate lowers near-term
free cash flow, so the gain has to arrive later and survive discounting. And a firm already
running at sector benchmarks has almost nothing to restructure.

## The formulas

```
Value of control = restructured equity value − status quo equity value

Expected value of control = P(management change) × value of control

Market value = status quo value + P × (optimal value − status quo value)

P = (market price/share − status quo/share) / (optimal/share − status quo/share)

Adjusted control value = (optimal − status quo) / (1 + r)^k     for a k-year turnaround

Maximum premium per share = optimal value/share − current price/share
```

Reading the implied probability:

| Result | Meaning |
|---|---|
| P at or below 0 | The market prices no chance of change; the stock may be cheap without one |
| 0 < P < 1 | The normal case; compare it to your own estimate |
| P at or above 1 | Your optimal value is too low, or the market prices something outside your model |

P is a residual, so it absorbs every error in both valuations. Report it as a read on the
market's odds, not as an objective probability. Both inputs must be per share on the same
share base, including or excluding options consistently.

Use the `implied` subcommand of `dcf-valuation-engine` when you want the reverse question:
what growth or margin does the current price already assume?

## What moves the probability

Structural determinants, which set the level:

| Factor | Direction |
|---|---|
| Takeover restrictions: poison pills, staggered boards, legal barriers | More restrictions lowers it |
| Voting rules and concentrated voting control | More entrenchment lowers it |
| Access to funds to mount a challenge | Easier financing raises it |
| Size of the company | Larger lowers it |

Empirical determinants of forced turnover refine that level. Forced change is more likely
when the firm underperforms peers and expectations. It is more likely when the board is
small, outsider-dominated and separately chaired. It is more likely when insider holdings
are low, institutional holdings are high, and the firm depends on equity markets for new
capital. A competitive industry raises it further.

The probability is not stable. Governance rules change. Activists appear, and are more
visible in down markets and after scandals. A hostile bid elsewhere in the sector reminds
investors of the power they hold. Re-run the calculation around each such event, and the
change in P measures what the event was worth.

**Worked read — Blockbuster, 2005.** Status quo equity $955 million, or $5.13 per share.
Optimally managed $2,323 million, or $12.47 per share. The gap is $7.34 per share, more than
the entire status quo value. Before Carl Icahn's challenge the stock traded at $8.20, an
implied probability of 41.8 percent. After the challenge succeeded it traded at $9.50, an
implied probability of 59.5 percent. Activism moved the market's odds by about 18 points,
worth $1.30 per share.

## Allocating control value

Control value does not spread evenly. It attaches to whoever can exercise it.

**Two share classes.** Every share owns the same cash flows, so the status quo value spreads
across all shares equally. Only the expected control value attaches to the voting class.

```
Value per non-voting share = status quo value / (V + NV)
Value per voting share     = value per non-voting share + P × (optimal − status quo) / V
Voting premium %           = (voting − non-voting) / non-voting
```

Worked on Embraer: status quo equity R$12,500 million, optimal R$14,700 million, 242.5
million voting shares, 476.7 million non-voting, P of 20 percent. Non-voting is R$17.38.
Expected control value is R$440 million, or R$1.81 per voting share. Voting is R$19.19, a
10.4 percent premium. Raise P to 50 percent and the premium goes to 26 percent. The voting
premium is a direct read on how likely change looks.

These formulas assume the non-voting class is completely unprotected. Where charters, local
law or tag-along rights protect it, some control value leaks back and the premium is
smaller. And part of any observed premium is a liquidity effect, because non-voting classes
often trade thinner.

**Private stakes.** A controlling stake is priced off the optimal value, and a minority
stake off the status quo.

```
Controlling stake (above the control threshold) = ownership % × optimal value
Minority stake                                  = ownership % × status quo value
Minority discount per unit of ownership         = 1 − status quo value / optimal value
```

Worked on a private business valued at $1.6 million as run and $2.0 million under better
management: a 51 percent stake is worth $1.02 million and a 49 percent stake $784,000. Two
points of ownership are worth $236,000, because one stake carries control and the other does
not. Do not look up a standard percentage discount. It is derived from this specific gap,
and a well-run private firm has almost none.

## The rule-of-thumb trap

Deal practice quotes fixed premiums, most often 20 percent. There is no defensible lookup
table, and that is the point. Take a firm with revenues of 100, operating income of 20, tax
of 8, no debt, no growth, and a 20 percent cost of equity. Status quo value is 60. The rule
of thumb says pay 72. If you can raise the pre-tax margin from 20 to 30 percent, after-tax
operating income becomes 18 and the optimal value is 90, so control is worth 30 and the
defensible premium is 50 percent. If the firm is already perfectly run, control is worth
zero and any premium is a gift.

Two further disciplines. The maximum premium is not the right premium; paying the whole
value of control hands your entire improvement plan to the seller. And a premium for brand
or for management quality is double counting, because a properly built valuation already
holds both.

## Guarding against double counting

- Control value and synergy value do not overlap. Measure synergy off the restructured
  target, never off the status quo.
- Do not add a control premium, a brand premium and a management-quality premium on top of
  one valuation.
- Cash counted in the cash flows is not also added in the equity bridge.
- In an acquisition, discount the target at the target's own risk and the target's own debt
  capacity, not the acquirer's.
- State which capital structure each scenario uses, and use the same one throughout that
  scenario.

## Pitfalls

- Treating the probability as 1 outside a hostile takeover. A minority holder cannot force
  change.
- Ignoring the delay. A three-year turnaround is worth materially less than the
  undiscounted gap.
- Restructuring a firm that is already well run and calling the difference control value.
- Raising the reinvestment rate without first checking that the return on capital exceeds
  the cost of capital.
- Reading a rising implied probability as good news for a holder. A high probability means
  the change is already paid for.
- Reporting a probability above 100 percent as very high confidence rather than as a broken
  input.

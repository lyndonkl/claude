# The bridge, the range, and value against price

Three presentation problems recur in every mode. How to show where the value came from.
How to show how uncertain it is. How to compare it with a market price without claiming
more than the analysis supports.

## The two bridges

The word covers two different tables. Both are called bridges and both belong in a report,
but they answer different questions and never merge into one ladder.

### The equity bridge

Answers: how did the discounted cash flow become a value per share? Present it as a ladder
with one line per adjustment, each with its basis stated.

```
  Value of operating assets          discounted cash flows at the cost of capital
+ Cash and marketable securities     excess cash only; operating cash sits in working capital
+ Value of cross holdings            valued separately, not at book
+ Other non-operating assets         only if their cash flows are not already in the forecast
= Value of firm
- Market value of debt               market, not book, for a going concern
- Other claims                       pension underfunding, contingent liabilities, minorities
= Value of equity
- Value of equity options            employee options, warrants, conversion options
= Value of common stock
/ Actual shares outstanding          not diluted
= Value per share
```

The organizing rule the report should demonstrate: every adjustment is made exactly once.
Give each line a basis column, because a reader disagreeing with a bridge is almost always
disagreeing with a basis rather than with the arithmetic.

Four lines carry most of the disputes and deserve a sentence each in the report.

- **Cash.** Was it kept out of the operating valuation and added back, or folded in? If a
  marginal-value haircut was applied, state the expected underperformance that sized it.
  Do not apply a cash haircut and also lower the growth assumptions for the same bad
  management.
- **Cross holdings.** State the stake size, the accounting tier, and the treatment. A
  consolidated model that forgets to subtract minority interests credits shareholders with
  a subsidiary they only partly own.
- **Other claims.** Pension underfunding is subtracted once, here, and never also carried
  as debt in the cost of capital. Contingent liabilities enter at probability times
  expected size, not at the plaintiff's headline number.
- **Options.** Subtract the option value from the numerator and divide by actual shares.
  Doing that and also using diluted shares double counts.

### The value stack

Answers: how much of the value is available to whom? It applies in the `restructuring` and
`acquisition` modes.

```
  Status quo value        the firm as currently run
+ Value of control        restructured value less status quo value
= Optimally managed value
+ Value of synergy        combined with synergy, less acquirer plus restructured target
= Total value to this acquirer
```

Two disciplines the report must show. Control value is the difference between two runs of
the same model, never a rule-of-thumb percentage. Synergy is measured off the
**restructured** target, not the status quo, or the control gain is counted twice.

State which layer applies to the reader. A minority holder with no path to control cannot
realize the control layer, and quoting the stack total to them is misleading.

## The range

A range needs three things to be useful: a method, a label, and a chosen cell. Give all
three.

### Choosing the method

Match the tool to the kind of doubt.

| The doubt is about | Use | Report |
|---|---|---|
| how much a driver moves | a two-input sensitivity grid | low, base, high with the inputs behind each |
| which story is true | a named scenario grid | the spread, the likelihood label on each cell, and the chosen cell |
| the joint distribution | simulation | median, tenth and ninetieth percentiles, and the share of trials at or below zero |
| whether the firm survives | a failure probability | the probability, its basis, and the proceeds assumption |

### Presenting it

Pick the two inputs that actually move value. A range built by varying inputs the value is
insensitive to is falsely tight, and a reader who checks will notice.

Apply the plausibility filter and show its work. Say which cells were ruled out and on what
grounds — growth above the economy's growth rate forever, high growth held for ten years in
a competitive industry, a margin no firm in the sector has ever earned. The value of a grid
lies in what it lets you rule out, not in the cells themselves.

Label every scenario possible, plausible or probable. A range without likelihood labels is
a wish list. Then name the cell you chose and the evidence for it. A range with no chosen
cell is an abdication.

Report the spread honestly. If value varies by seventy percent across the grid, say so and
temper the recommendation. If even the most conservative cell sits above the price, say
that too — it is a stronger argument than the base case can make alone.

Where a simulation ran, note that the simulation median is not the base case. They differ,
often materially, and reporting one as the other misstates both. Treat the extreme
percentiles as tail artifacts rather than as a range.

Do not add a risk premium on top of a simulation. The discount rate already carries risk,
and the simulation describes the spread of outcomes, not an extra charge for them.

## Precision and rounding

Round to the precision the inputs justify. A share count rounded to millions cannot support
a value per share quoted to four decimals.

Two decimals on a per-share figure is conventional and usually fine. What is not fine is a
point estimate presented without its range, because that is where the false precision
actually lives. The number itself can be exact; the claim around it must not be.

State the value as a base case plus an explicit range, every time. If a reader insists on
one number to two decimals with no range, that is a warning about the reader, not a
specification to satisfy.

## Value against price

Four steps, in order, in every mode that has a market price.

**1. The gap.** Value per share, price per share, the difference, and price as a percent of
value. Below 50% or above 200% is a prompt to re-examine your own inputs before concluding
the market is wrong. Say that you re-examined them and what you found.

**2. The implied input.** Solve for the growth rate, margin or market share that makes model
value equal the market price. Report it as what the market is assuming, not as a forecast.
Then ask whether that assumption is probable rather than merely possible. Some scenario
justifies any price, so possibility is not an argument.

**3. The closing mechanism.** Name what closes the gap and over what horizon: an earnings
report, a product milestone, an activist, an acquirer, an index event, a refinancing. A gap
with no mechanism and no horizon is an opinion, not a trade. Where you cannot name one, say
so and let the recommendation carry that weight honestly.

**4. The margin of safety.** The gap net of the range. This is the number the gate asks for
and the number a decision-maker actually uses.

Optionally add the expected one-year return if the market corrects, computed by rolling
value forward at the cost of equity and adding the expected dividend. Label it as
conditional on correction, because that is exactly what it is.

## Reconciling estimates that disagree

Intrinsic value, a peer multiple, a sector regression, a market regression and an option
value rarely agree. The report shows all of them and reconciles them. It never averages
them.

Put them in one table with the current price as the first row. Discard any estimate that is
economically implausible and say why, rather than letting it drag an average. Then name the
estimate that carries the decision and defend the choice. Where comparable selection was
ambiguous, the intrinsic answer usually carries more information and the report should say
that plainly.

Where every method except one points the same way, that near-unanimity is strong evidence
and deserves a sentence. Where the methods split evenly, the honest output is a hold with
the disagreement explained, not a forced call.

Where the recommendation rests on a small gap, acknowledge it. A sell call resting on a
two percent difference is a defensible call and an indefensible silence.

## Detail

- Bridge mechanics and the link-by-link rules: `knowledge/frameworks/intrinsic-valuation-playbook.md`
  stage S14.
- The gap, expected return and the three investor questions:
  `knowledge/concepts/narrative-numbers/value-vs-price-gap.md`.
- Grid construction and the plausibility filter:
  `knowledge/concepts/deliverables-worked-examples/dcf-sensitivity-analysis.md`.
- Scenario grids and likelihood labels:
  `knowledge/concepts/narrative-numbers/narrative-scenario-grids.md`.
- Simulation reading: `knowledge/concepts/narrative-numbers/monte-carlo-valuation-simulation.md`.
- Reconciliation and the weighting rule:
  `knowledge/concepts/deliverables-worked-examples/valuation-triangulation-and-recommendation.md`.
- The value stack worked end to end:
  `knowledge/concepts/deliverables-worked-examples/value-of-control-and-synergy.md`.

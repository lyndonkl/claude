# Template: `corporate-finance` mode

The question is whether this firm's investing, financing and payout choices are right. The
terminal artifact is the ten-part assessment, opened by a one-page scorecard.

The ten parts come from the graded corporate finance project. They run strictly in order,
because each part consumes the one before it. Returns cannot be judged before hurdle
rates. The payout verdict needs the return spread. The valuation needs the recommended
capital structure. Reordering the report hides those dependencies from the reader.

## Sections in order

### 0. Executive scorecard

One page, one column per company or scenario, one row per headline number, in the order
the parts run. Every cell is pulled from its own part. The scorecard reports; it does not
compute.

| Row | Source part |
|---|---|
| Governance power score | I |
| Beta approach and levered beta | III |
| Jensen's alpha, R squared | III |
| Return on equity less cost of equity | IV |
| Return on capital less cost of capital | IV |
| Economic value added, in currency | IV |
| Current debt ratio | III |
| Optimal debt ratio | VI |
| Change in cost of capital at the optimum | VII |
| Change in firm value at the optimum | VII |
| Dividends and buybacks | VIII |
| Free cash flow to equity | IX |
| Value per share | X |
| Price per share | market |

Always carry the benchmark next to the estimate. An optimal debt ratio of 40% means
nothing without the current 12% beside it. Read the scorecard across rows to find the
outlier for each question, then down columns to build each firm's story.

Close with a short paragraph written from the pattern, not firm by firm. Flag internal
tensions: a firm with a negative return spread that is also under-levered has two
different problems, and the recommendations must not conflict.

### I. Governance and the objective

Board and executive table against peer averages. The three CalPERS tests. Ownership,
voting stake and the control wedge. Entrenchment and takeover defenses. Covenant
inventory. Counter-force scores. The archetype.

State the objective the analysis maximizes, derived from the three booleans: traded and
liquid, markets efficient for this stock, lenders protected. Then the constraint set and
the agency-cost prior.

This part gates the credibility of everything after it. A board that can ignore an
optimal-debt recommendation indefinitely changes what the recommendation is worth, and the
reader needs that before the numbers arrive.

### II. Stockholders and the marginal investor

Insider, individual and institutional breakdown. Institutional share of float. The
marginal investor — the holder most likely to trade next, not the largest holder.

State the risk measure that follows: market beta, total beta, or an alternative. This
single call determines whether the entire hurdle-rate stack is legitimate.

### III. Risk and hurdle rates

The build-up table, produced twice: on market values for every forward-looking use, and on
net book values for the return comparison in Part IV. Label which is which.

Regression diagnostics as diagnostics only: regression beta with its standard error,
Jensen's alpha measured against the riskfree benchmark, and R squared. Say plainly that
the bottom-up beta is the production number and the regression is a check on it.

Divisional rates where the businesses differ in risk, with the debt allocation key stated.

### IV. Returns on existing investments

Return on capital against cost of capital, return on equity against cost of equity, both
on matching bases. Economic value added in currency. Benchmark twice: against zero, and
against the industry-average firm.

State the verdict in one word — creates value, neutral, or destroys value — and then the
forward question. Will future projects look like past ones, and why?

This verdict is one axis of the payout matrix in Part IX and the strongest evidence for or
against the growth story in Part X. Keep it consistent across all three.

### V. Capital structure choices, qualitatively

The five forces scored: tax benefit, discipline, expected bankruptcy cost, agency cost,
flexibility. Each with its proxy and its direction.

Then the prediction: too much debt or too little, and roughly where the optimum should
sit. This prediction was made before the schedule ran, and the report should show it in
that order. A qualitative argument written after the spreadsheet is a rationalization.

### VI. Optimal capital structure

The cost-of-capital schedule from 0% to 90% in ten-point steps, with the rating, the
spread, the relevered beta and the cost of capital at each row. Mark the optimum.

Report a range and a direction, not a single ratio with false precision. The grid steps
are wide and the inputs are noisy.

Then the constrained recommendation, stated separately from the mechanical minimum. If a
rating floor binds, price it: firm value at the unconstrained optimum less firm value at
the constrained ratio. Show the stress table and say where the optimum first moves.

Where an alternate lens ran — the enhanced approach, adjusted present value, or the peer
and regression comparison — report it beside the standard answer. Where intrinsic and
peer-based answers disagree, prefer the intrinsic one and explain the gap. Do not average.

### VII. Moving to the optimum, and debt design

Speed and method, from the decision tree. Then the value of the move, reported both ways:
the full revaluation and the conservative incremental version. They can differ by a factor
of two, and the difference is entirely the growth rate assumed. Report both and say so.

The rational buyback price where a buyback is the method, with the arithmetic that
supports it.

Then debt design: target duration, currency mix, fixed against floating, and any special
features, each traced to an asset characteristic or a macro sensitivity. A regression slope
that is not statistically significant must not drive a financing recommendation, and the
report should say which slopes were and were not usable.

Close with the gap table: existing debt profile beside the recommendation, and the
instruments that close the gap.

### VIII and IX. Payout

Cash returned, meaning dividends plus buybacks, on both sides of every comparison. Payout
ratio, cash payout ratio, yield, buyback share.

Free cash flow to equity in all three variants, with the variant that drove the verdict
named. Disagreement between the variants is itself a finding and can move the firm between
quadrants.

The trust scores: the return spread from Part IV, and the alpha from Part III. Then the
quadrant, the peer comparison with both average and median, and the regression prediction
with its buyback caveat.

The recommendation: how much, in what form, at what speed, with the constraints checked —
clientele, contractual, regulatory, signaling.

### X. Valuation

The status quo discounted cash flow, then the restructured one with every recommendation
in place. Growth comes from the reinvestment rate times the return on capital in both, and
the report states that identity rather than asserting a growth rate.

The equity bridge and value per share against market price.

Then the difference between the two runs: the value of control, in total, per share, and
as a percent of the current price. Discount it for implementation delay and say how many
years you assumed.

The market-implied probability of change, compared with your own governance-based estimate
from Part I. A probability at or beyond the ends of the range means an input is wrong, not
that a discovery has been made.

Name the key driver: which single variable moves the value most, and what a hired value
enhancer would do first.

### XI. Unresolved findings, sources and vintages

See `disclosure-and-vintage.md`.

## Consistency the reader will check

- The optimal ratio in Part VI is the ratio used in Part VII's recapitalization, in Part
  IX's target-ratio cash flow, and in Part X's restructured cost of capital. If it differs
  anywhere, explain why in that section.
- The good-projects axis of the payout matrix is the same verdict as Part IV's spread, on
  the same basis.
- Every scorecard cell equals its section. A discrepancy is a validation failure.

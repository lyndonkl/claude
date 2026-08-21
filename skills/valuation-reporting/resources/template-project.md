# Template: `project` mode

The question is whether to make this investment. The terminal artifact is a net present
value verdict on the project.

This mode differs from the others in one structural way. There is no company to value and
no market price to compare against, so the discipline that replaces the value-versus-price
section is the break-even table. The decision-maker wants to know what has to be true, and
what they should watch after the money is committed.

## Sections in order

### 1. Verdict

- Accept or reject, and at what scale.
- Net present value in currency, with the hurdle rate that produced it.
- The internal rate of return against that hurdle rate.
- The range: net present value at the low and high ends of the two assumptions that decide
  it.
- The break-even level of the single most uncertain driver.
- Whether an embedded option carries the decision, stated explicitly if it does.

Report net present value as a statement of value added in currency, not as a ratio. The
reader is deciding whether to spend money, and the answer should be in money.

### 2. The project and the counterfactual

What is being built or bought, over what life, at what initial outlay. Then the
counterfactual: what happens if the firm does nothing. Every number in the report is the
difference between those two worlds.

State the perspective — firm side or equity side — and keep it throughout. Firm-side cash
flows never deduct interest.

### 3. The hurdle rate

From `05-capital/`. The rate used, and the argument that it matches this project's business
risk rather than the company average. A single company-wide rate lets safe divisions
subsidize risky ones and tilts the firm toward its riskiest businesses.

Where the project sits in a different currency or a riskier geography, show the conversion
or the added country risk premium, and confirm it is counted once.

Where the project carries subsidized financing, show the fair rate used in the hurdle rate
and the subsidy valued separately. A subsidized rate must never lower the hurdle.

### 4. The cash flows

The annual table, and above it the assumptions that generated it: revenue path, direct
costs, depreciation, the overhead treatment, the working capital ratio, the tax rate.

Then the incremental adjustments, each as its own line so a reader can argue with it:

- Sunk costs excluded, including the depreciation shield on any capitalized sunk asset.
- Allocated overhead reduced to the genuinely variable share plus new overhead, with the
  split's derivation.
- Side costs charged: owned resources at their best alternative use, excess capacity at
  the cost of bringing the next unit forward, cannibalization at the share the firm would
  otherwise have kept.
- Side benefits credited, each valued at the receiving business's cost of capital, with an
  honest adoption lag.

Report stand-alone value and synergy value separately. Blending them hides which half of
the case is doing the work.

### 5. Closing the stream

For a short finite life: salvage as end-of-life book value plus recovered working capital.

For a long or indefinite life: the terminal value, capitalized off a steady-state year and
never off a still-growing forecast year. Show the maintenance capital spending implied by
the assumed perpetual growth. Zero growth means maintenance equals depreciation; positive
growth requires more.

### 6. The tests

Net present value first, because it is the decision rule. Then the internal rate of return
with the count of sign changes noted, because more than one sign change means more than
one rate and the reader should know the number is unusable.

Where projects are being compared, name the ranking rule and why it applies: different
scale means net present value; different lives means equivalent annuities or replication;
genuine capital rationing means the profitability index.

Add the accounting cross-check: the project's return on capital against the same
risk-matched rate.

### 7. The break-even table

The section a project sponsor actually uses after approval. For each of the three or four
drivers that matter, the level at which net present value reaches zero, and the current
forecast beside it.

Say which of those levels a manager can monitor month by month. That converts the analysis
into something the firm can act on rather than a one-time verdict.

Then the range: net present value across the plausible span of the two drivers with the
largest effect. Where a simulation ran, report the mean, the median, the span and the share
of trials below zero.

State clearly that a downside probability is not by itself a rejection reason. The hurdle
rate already charges for risk, and double-charging it rejects good projects.

### 8. Embedded options

Only where an option genuinely exists. Name it, and name what makes it real.

- Delay: requires genuine exclusivity. Without exclusivity, waiting invites entry.
- Expand: name the specific follow-on investment the first project unlocks.
- Abandon: requires a real exit value, not a hope of one.

Report the option value beside the traditional net present value, and say explicitly when
the option is what carries the decision. Value them separately; do not fold the option into
the base case.

### 9. What to watch and who owns it

The forecast milestones, the break-even levels from section 7, and the named person
accountable for delivery. Then the post-mortem commitment: when actuals will be compared
with this forecast.

### 10. Unresolved findings, sources and vintages

See `disclosure-and-vintage.md`.

## What the reader will check

- Interest is absent from firm-side cash flows.
- Side costs and side benefits appear once, either inside the annual flows or as a
  lump-sum adjustment, never in both places.
- The capitalized terminal year is a steady state.
- Working capital is recovered at the end of a finite-life project.
- The hurdle rate matches the project's risk, not the corporate average.

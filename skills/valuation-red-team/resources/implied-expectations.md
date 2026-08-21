# The implied-expectations attack

This is usually the most productive thing in the review. It converts an argument about your
assumptions into a claim about the world.

"The stock is worth $31 and trades at $42" invites a fight over the discount rate. "At $42
the market assumes a 22% operating margin, which no firm in this industry has sustained" is
checkable, and either side can lose it.

The attack runs in three directions. Read the price backwards. Read the analyst's own
number backwards. Then read the sector in aggregate.

## Direction one — what the price assumes

Run the `implied` subcommand of the DCF engine with the market price as the target.

```bash
python3 <skills>/dcf-valuation-engine/resources/dcf.py implied --in solve.json
```

The payload has four parts.

| Key | Contents |
|---|---|
| `base_case` | the analyst's own driver payload, unmodified |
| `path` | a dotted path to one leaf, such as `operating_margin.end`, `terminal.growth_rate` or `revenue_growth.start` |
| `target_value_per_share` | the market price |
| `low`, `high` | the bracket to search |

Use the analyst's payload rather than one of your own. The point is to hold their story
fixed and solve for the single number the price requires under it. Changing anything else
first makes the answer yours, not theirs.

Pick the path that carries the story. For a young company that is usually the target
operating margin or the year-10 revenue level. For a mature firm it is usually terminal
growth or the terminal return on capital. For a commodity firm it is the price the revenue
model is built on.

Then locate the answer. `relative-valuation-toolkit` has two subcommands for this. Use
`peer-stats` to get the median and quartiles of the sector on that measure. Use `locate` to
place a multiple inside a bundled current distribution. The finding is not the solved
number. The finding is where that number sits in the distribution of what firms in this
business actually achieve.

## Direction two — what the analyst's own drivers assume

Run the same machinery on the model's own output rather than on the price. Four reverse
checks, all cheap.

**Implied perpetual return on capital.** Compute the embedded reinvestment rate as
`1 − terminal free cash flow / terminal after-tax operating income`, then divide terminal
growth by it. If the result sits above the terminal cost of capital, the model claims a
permanent moat. State the moat or set the two equal. Never let a valuation ship whose
implied perpetual return nobody looked at.

**Implied market share.** Divide year-N revenue by an independent estimate of the market's
size in that year. Above 100% the model is impossible. Below 100% but above what any
incumbent has ever held, it is a claim that needs an argument.

**Absolute revenue in year N.** Convert the growth path into currency and ask who loses that
revenue. Percentage growth is deceptive in a way that dollar totals are not.

**Implied marginal return on capital.** The change in after-tax operating income across the
forecast divided by the change in invested capital. Above the best firms in the business,
either reinvestment is too low or margins are too high.

## Direction three — the sector aggregation test

A single company's story can be defensible while the sector's stories are collectively
impossible. This is invisible from inside one valuation.

1. Define the market precisely. Vague definitions defeat the test.
2. List every competitor for it, listed and private, domestic and foreign. Leaving out the
   foreign names understates the total badly.
3. Impute each one's breakeven revenue in a common future year, solving its own enterprise
   value backwards.
4. Multiply by the share of that firm's revenue that comes from this market.
5. Sum, and compare against an independent forecast of total market size.
6. Implied shares across the sector cannot exceed 100%.

When the sum exceeds the market, the finding is about the sector, not the name. Say so.
Note also that using each company's own bullish margin assumptions understates the required
revenue and hides the problem.

## The restructuring variant — implied probability of change

Where the analysis produced a status-quo value and an optimally-run value, the market price
already carries an opinion about whether anyone will force the change.

```
implied probability = (price − status quo value) / (optimal value − status quo value)
```

A result outside the range zero to one is not a discovery. It means one of the two
valuations is wrong, and the finding belongs to whichever stage produced them.

Compare the implied probability against the evidence: ownership and voting structure,
takeover defences, board composition, activist presence, and firm size. A market pricing an
80% chance of change at a firm whose founder controls the votes is a finding worth writing.

## How to grade what you find

The direction decides the severity.

| Finding | Severity | Why |
|---|---|---|
| the model's own drivers imply an impossible share, revenue or return | high | the screen is arithmetic, not taste |
| the model's implied perpetual return exceeds its cost of capital with no named moat | high | a stated default is being passed off as an argument |
| the price implies something extreme and the write-up never says so | medium | the verdict rests on an unstated disagreement; the fix is a sentence |
| the price implies something merely unusual | low | note it and move on |

One warning about reading these results. Some combination of inputs justifies any price.
Finding a scenario that reaches the market price proves nothing. The question is whether
that scenario is probable, and the answer to that lives in the sector distribution rather
than in the model.

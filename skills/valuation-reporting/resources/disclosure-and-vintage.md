# Assumptions, disclosure and vintage

Three sections appear in every report regardless of mode. The pivotal assumption ledger,
the unresolved findings, and the sources and vintages. They are what let a sceptical reader
audit the answer instead of taking it on faith.

## The pivotal assumption ledger

Every valuation has dozens of inputs and two or three that decide it. The report names
those two or three in the executive summary and tabulates the rest in an appendix.

### Finding them

Do not guess. The `sensitivity` block of `dcf-result.json` already contains the answer. An
assumption is pivotal when moving it across its plausible range moves value enough to
change the recommendation. Everything else is detail.

In practice the pivotal set is drawn from a short list. It holds the revenue growth path or
its end-state level, the target operating margin, and the sales-to-capital ratio. It also
holds the length of the growth period, the terminal growth rate, the cost of capital and
the probability of failure. Damodaran's own published valuations run on roughly five
levers, and the small input count is deliberate. A reader can argue with five numbers. Nobody argues with fifty.

### Presenting them

One row per pivotal assumption, with these columns.

| Column | What goes in it |
|---|---|
| Assumption | the driver, named in the vocabulary of the model |
| Value used | the number, with unit and currency |
| Source | the peer percentile, the industry average, the narrative claim, or the management target |
| Range tested | the low and high used in the sensitivity |
| Value effect | value per share at each end |
| Flips the call at | the level at which the recommendation changes, where one exists |

Below the table, one sentence per row saying which claim in the narrative supports it. A
model input with no story sentence behind it is unsupported, and a story claim with no
input is decoration. Both counts should be zero, and the report should say so.

### The appendix table

Everything else, in one flat table: input, value, source, and the stage that owns it. No
commentary. Its purpose is reproducibility, not persuasion.

## Unresolved findings

Gate `G7_challenged` passes when every high-severity finding in `10-challenge/challenge.json`
is either resolved or explicitly disclosed. The loopback rule caps reruns at two per stage.
A finding that survives the third attempt is disclosed in the report as an unresolved risk
rather than looped on forever.

Disclosure is a named section with its own heading. It is never a footnote, an appendix
entry or a parenthesis.

### What each disclosure carries

- The finding `id` from `challenge.json`, so the reader can trace it.
- Its `severity` and `target_stage`.
- The `claim`, in the critic's own terms rather than paraphrased into something softer.
- The `evidence` the critic gave.
- What was attempted across the reruns, and why it did not resolve.
- The value effect if the critic is right: value per share under the critic's assumption,
  beside the base case.
- Whether it changes the recommendation.

That last line is the one the reader wants. A high-severity finding that does not change
the call is a very different situation from one that does, and the report should not make
the reader work that out.

### Findings that were resolved

Summarize them briefly in the same section. Two or three lines: what was challenged, what
changed, and by how much the value moved. A report that shows the analysis surviving attack
is more credible than one that never mentions the attack.

### The temptation to soften

Do not restate a finding in gentler language, bury it among minor items, or place it after
the recommendation. The one failure that destroys a reader's trust in every other number is
discovering a material objection that the report knew about and did not surface.

## Sources, gaps and vintages

### The vintage table

Every external input has a date, and mixing dates is the most common silent error in this
domain. One table, listing each input, its source, its `as_of` date, and the value used.

Cover, at minimum: the riskfree rate, the mature equity risk premium, the country risk
premium table, the default spread table, the synthetic rating table, industry averages,
the tax rates, the market price and the share count.

The reference tables bundled with `cost-of-capital-toolkit` each carry an explicit `as_of`
field. Read it from the file rather than assuming, and quote it.

### Two checks the report states

**The mandate check.** Every vintage should sit near the `valuation_date` in
`mandate.json`. Name any input that does not, and say what it would change. A current
riskfree rate paired with a country risk table from four years ago is not a small
inconsistency; it silently biases every value in the report.

**The staleness check.** Anything more than a year old is flagged, with a note on whether a
refresh was attempted. The reference tables are refreshed from the published source when
they go stale, and the vintage actually used is what the report records — not the vintage
that should have been used.

### Gaps and fallbacks

From `01-data/gaps.json`. One row per missing input: what was unavailable, why, the
fallback used, and its likely direction of error.

A gap filled with an industry average is not the same as a gap filled with a guess, and the
report should distinguish them. Where a gap sits underneath one of the pivotal assumptions,
say so explicitly — that combination is where a valuation is most fragile.

### Sources

From `01-data/sources.md`. Filings with their dates, market data with its timestamp,
reference tables with their `as_of`, and any management guidance with the date and forum in
which it was given. Where a number came from a transcript or a call, say so; it is weaker
evidence than a filing and the reader should be able to weigh it.

## The bias line

One sentence, near the top of the report. Who commissioned the work. What answer they
would prefer. Whether the market price was seen before the qualitative work was done. Any
public position already taken on this company.

Bias is not eliminated by declining to mention it. Stating it lets the reader discount in
the right direction, which is the most useful thing an honest analyst can offer.

## Detail

- The validation battery the report ships behind:
  `knowledge/frameworks/intrinsic-valuation-playbook.md` stage S17.
- Cross-stage validation rules for the corporate finance mode:
  `knowledge/frameworks/corporate-finance-playbook.md`, the consistency and validation section.
- Input inventory, sources and fallbacks: `knowledge/frameworks/data-requirements.md`.
- Precision, bias and the small-model rule:
  `knowledge/concepts/narrative-numbers/valuation-misconceptions.md`.
- Claim grading and promotion triggers:
  `knowledge/concepts/narrative-numbers/possible-plausible-probable.md`.

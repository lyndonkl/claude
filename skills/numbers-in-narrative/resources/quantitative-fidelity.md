# Quantitative Fidelity: The Frame Lock And The Refusals

Reference matter for Steps 1, 2 and 6. The structural fact this file exists to answer: in quantitative narrative, every fact can be true and the story still false. Falsity lives in the choices — unit, denominator, window, boundary, aggregation level, which measure leads — not in the figures. Fact-checking cannot see it.

## Frame Lock template

The Frame Lock is owned by `narrative-evidence-ledger`. If a ledger exists, import its lock verbatim rather than filling this in; the template below is for material that has no ledger. The owner's procedure and worked examples live in [../../narrative-evidence-ledger/resources/frame-lock.md](../../narrative-evidence-ledger/resources/frame-lock.md).

Fill this before any prose. Written down, not held in memory.

```
FRAME LOCK
UNIT:         one row is ______
  rejected:   ______ because ______
DENOMINATOR:  per ______
  rejected:   ______ because ______
WINDOW:       ______ to ______
  left edge justified by:  ______
  right edge justified by: ______
  rejected:   ______ because ______
BOUNDARY:     population is ______
  drawn by:   me / the source / a regulator / an industry body
  rejected:   ______ because ______
```

Any later change to one of the four re-opens the whole piece. It does not just adjust one chart, because the change alters which claims are sayable about the material.

**Worked lock, supply chain.**
```
UNIT:         one inbound container, at one terminal, on one calendar day
  rejected:   one booking — bookings split across containers and double-count dwell
DENOMINATOR: per container-day of dwell
  rejected:   per TEU — mixes 20ft and 40ft boxes whose handling differs
WINDOW:       Jan 2021 - Dec 2023
  left edge:   first month the terminal's new gate system was live (prior data is a different instrument)
  right edge:  last month with complete billing reconciliation
  rejected:   starting 2019 — the pre-system data is not comparable and would manufacture a jump
BOUNDARY:     the four terminals under the same operator agreement
  drawn by:   the source, in its own reporting
  rejected:   all terminals in the port — different operators report dwell differently
```

## Denominator drift: the failure fact-checking cannot detect

The pattern: the piece opens on counts, pivots to per-capita for the one comparison where per-capita favours the thesis, then returns to counts for the conclusion. Every exhibit is individually defensible. The sequence is a lie.

**Worked example, public health.**

1. Opening: "The county recorded 412 cases, the most in the state." (count)
2. Middle: "Adjusted for population, the neighbouring county is worse — 61 per hundred thousand against 44." (rate)
3. Close: "With more than four hundred cases, the county remains the state's outbreak centre." (count again)

Nothing here is false. The county is both the worst place and not the worst place, depending on which sentence you remember. The piece has already chosen for you: counts sit in the emphatic position at both ends.

**The sweep.** List every number in the finished draft, in order, with its denominator:

| # | Figure | Denominator | Position |
|---|---|---|---|
| 1 | 412 cases | none (count) | opening |
| 2 | 61 vs 44 | per 100k residents | middle |
| 3 | 400+ cases | none (count) | close |

Two switches. Each switch must be reverted, or narrated as a beat: "Counted heads, this is the worst county in the state. Counted per resident, it is fourth — and which of those matters depends on whether you are allocating vaccine or allocating blame."

**Rate vs count rule.** If entities differ in size by more than roughly 2x, rates are mandatory for comparison and raw counts are supplementary, never the headline. If the denominator is itself moving — a shrinking population, a growing user base, a changing test volume — show both series. The ratio alone hides which term moved.

**Denominator language.** "Per capita" means per person. A figure of 2.3 per 1,000 residents is not a per-capita figure. This is the most checkable error in quantitative writing and the most common.

## Precision and rounding

**Precision ceiling.** No figure in prose may exceed the precision of its source.
- Source: "roughly a third." Permitted: "about a third", "roughly one in three." Forbidden: "33.4%."
- Source: 23.7%. Permitted: "about a quarter", "23.7%." Forbidden: "23.74%."

**Rounding drift.** The compounding version is the dangerous one. The agent rounds for readability, then uses the rounded figure as the input to the next sentence's ratio or total. By the third derivation the number sits outside the source's range while still wearing the word "about".

- Held value: 1,043,200 units. Prose: "about a million."
- Next sentence derives a share: 1,000,000 / 4,180,000 = 24%. But the true share is 1,043,200 / 4,180,000 = 25%.
- Shipped: "about a quarter" would have been right. "Just under a quarter" is now wrong.

Rule: derived figures reference the held source value and its pointer, never a prose sentence. Recompute every total, share, and ratio at the end from the held values, and confirm the parts still sum to the whole after rounding.

**Circular sourcing.** Your own earlier draft, summary, or notes are never a source for a number. In a multi-step pipeline this corruption is silent: every figure has a pointer, no figure has a source, and no single step did anything wrong. Check it mechanically. It is invisible on reading.

## Percent, percentage point, relative, absolute

| Move | Bad | Good |
|---|---|---|
| Percent vs point | "Coverage rose 50%" (from 4% to 6%) | "Coverage rose two percentage points, from 4% to 6%" |
| Relative without base | "Adverse events doubled" | "Adverse events went from three to six, out of 4,000 enrolled" |
| Absolute without base | "1,200 more failures" | "1,200 more failures, on a base of 90,000 — one in seventy-five" |
| Both in one sentence | "a fifty percent rise, or two percentage points" | Pick the one the claim rests on. Put the other in the exhibit. |

A rise from 4% to 6% is simultaneously two percentage points and a fifty percent increase. Both are true. Only one belongs in a given sentence, and which one you choose is a rhetorical act — pick it deliberately and disclosably.

## Contested figures

Both values, both sources, one sentence. Never average. Never silently pick the better-sounding one.

- Bad: "Downtime ran to about an hour and a half."
- Good: "The operator put downtime at 40 minutes; the regulator's incident log records 94."

If the sources disagree on the SIGN of a change, the disagreement is its own beat and needs a paragraph, not a clause. If you believe one over the other, say which and why — that is a claim you own, and it belongs in the text rather than in a note.

## Model output must not wear the grammar of a measurement

A projection, a fit, a simulation, or an analyst estimate may not take the sentence shape of an observation.

| Forbidden | Permitted |
|---|---|
| "Throughput reaches 14,000 units in 2027." | "The capacity model puts throughput at about 14,000 units by 2027." |
| "The intervention prevents 3,100 infections." | "Under the transmission model as specified, the intervention averts roughly 3,000 infections; a second specification puts it near 1,200." |
| "Latency will settle near 40ms." | "Extrapolating the last six weeks, latency settles near 40ms — the extrapolation is marked on the chart." |
| "She earned the equivalent of $84,000." | "Converted at the 1911 exchange rate and adjusted by CPI, her salary is roughly $84,000 in today's money; other deflators give figures from $60,000 to $110,000." |

The grammar carries the epistemic status. When it does not, the reader has no way to know they are reading a model.

## The other hard refusals

- **Trend from two points.** Two observations are a difference. "Rising", "accelerating", "the trajectory", "on track to" all require more than two.
- **Qualitative quantifier to numeral.** Source says "several suppliers." You may not write "six". You may write "several", and you may go ask.
- **Ranges survive.** If the source gives a range or interval, prose carries it, or states explicitly that it is using the midpoint. Silently collapsing an interval to its centre is manufacturing precision.
- **Thin support.** Never lead on a figure resting on a handful of records or one reporting period. Rarity in real data is overwhelmingly produced by small denominators, coding errors, partial reporting periods, and newly created categories. Plot the measure's variance against denominator size. If your extremes all sit in the smallest denominators, your extremes are noise wearing a story's clothes.
- **Instrument versus world.** A sharp break in a series is a change in the world only if it survives an instrument check. Enumerate definitional revisions, coverage changes, methodology restatements, reporting-lag artifacts, entity and boundary changes. If the break coincides with one of these, either re-baseline on a consistent definition or narrate the instrument change as the story. The artifact is usually sharper than the real transition, so the false version reads better.
- **Verified.** You track provenance. You do not verify. The correct verb is "sourced".

## The omitted-number log

Refusal training makes a writer good at not adding. Nothing makes them good at not omitting. A fully sourced piece can be entirely false through subtraction alone: the disconfirming quarter, the failed arm, the region that went the other way, each cut individually defensible for length or flow.

Keep a log of every figure cut from the draft. Review it as a SET, not per cut. The question is not "was this cut defensible?" but "do these cuts share a direction?" If the remaining text implies a different frequency, magnitude, or balance than the full record, the subtraction has become deception.

## Person and system variants

| Concern | Person protagonist | System protagonist |
|---|---|---|
| Unit | one year of a life, one work, one transaction she made | one shipment, one wafer, one request, one enrolled patient |
| Denominator | per year of career, per work produced | per unit of exposure, per attempt, per dollar deployed |
| Boundary | which of her activities count as the career | which entities count as the market, and who drew that line |
| Intentionality | motive requires a stated source, at the time or recalled | "the market priced in", "the protocol decided" is an unsourced claim about collective intent — rewrite as aggregated behaviour of named actors |
| Aggregates | not applicable | a representative firm or median user may never take a name, a date, a scene, or an intent |

The intentionality row is the one that fails silently. Every "the market realized", "the industry decided", "the index knew" is either shorthand the reader will read as agency, or a hidden causal claim that never faces the sourcing discipline an explicit claim would face. Personify once, marked as a device. After that, attribute behaviour to named mechanisms and named actors.

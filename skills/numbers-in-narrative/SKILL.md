---
name: numbers-in-narrative
description: Writes quantities into prose so they land without overstating what the source supports. Applies a per-paragraph number-landing checklist (three numbers per paragraph, one per sentence, direction before magnitude, a comparison on the same screen), a unit-and-denominator lock that catches denominator drift, quantitative fidelity refusals (precision ceiling, rounding drift, percent vs percentage point, model output vs measurement), an uncertainty routing table, a declared likelihood-and-confidence ladder, and a chart-beat contract for exhibits that carry a claim. Use when drafting or editing prose that carries figures, statistics, benchmarks, forecasts or estimates, when a passage reads as a stat wall, when deciding how much precision or hedging a number can bear, or when the user mentions numbers in prose, rounding, denominator, per capita, percentage points, error bars, confidence, uncertainty, chart title, caption, or stat wall.
---

# Numbers In Narrative

## Table of Contents
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [Number-Landing Checklist](#number-landing-checklist)
- [Fidelity Refusals](#fidelity-refusals)
- [Uncertainty Routing Table](#uncertainty-routing-table)
- [Likelihood and Confidence Ladder](#likelihood-and-confidence-ladder)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

**Related skills:** Use `narrative-evidence-ledger` for the Frame Lock this skill imports, `narrative-fallacy-guard` for the likelihood lexicon, `narrative-fidelity-audit` for the pre-ship gate. Use `visual-storytelling-design` for the narrative shape around the exhibits, `cognitive-fallacies-guard` for auditing a chart's encoding, `writing-revision` for the prose pass after the numbers are settled, `readability-check` for reading-level gates.

## Core Principles

1. **A bare number is not information**: every figure that survives into prose carries a comparison on the same screen — a prior period, a peer, a denominator, or a physical referent the reader already owns.
2. **Direction before magnitude**: say which way it moved, then how far. A reader who does not know the sign cannot use the size.
3. **The frame is the claim**: unit, denominator, window, and population boundary determine which stories are sayable. Change one mid-piece and every exhibit stays defensible while the sequence becomes a lie.
4. **Precision is a property of the source, not a style choice**: round for prose, compute from the source value, never from the rounded prose figure.
5. **Uncertainty is routed, never dumped**: it rides in the annotation layer of the claim it qualifies, unless it would change the conclusion — then it is its own beat. Never all of it in a trailing methods note; never a hedge in every sentence.
6. **The exhibit travels alone**: readers recall the gist of the title, and follow it even when it disagrees with the marks (Kong et al., CHI 2018/2019). So the title must be a claim the chart's own marks can falsify.
7. **Sourced, not verified**: you track provenance. You do not verify. Never write "verified", "confirmed", or "fact-checked" about your own numbers.

## Workflow

Copy this checklist and track your progress:

```
Numbers In Narrative Progress:
- [ ] Step 1: Import the frame, or build one (unit, denominator, window, boundary)
- [ ] Step 2: Bind every number to a source and a precision
- [ ] Step 3: Land the numbers, paragraph by paragraph
- [ ] Step 4: Route the uncertainty by type
- [ ] Step 5: Contract each exhibit that carries a beat
- [ ] Step 6: Run the drift and fidelity audit
```

**Step 1: Import the frame, or build one**

Step 1.1: The Frame Lock belongs to `narrative-evidence-ledger`. If a ledger already exists for this material, import its Frame Lock verbatim: unit, denominator, window, boundary, plus the rejected alternative and reason for each. Do not restate it in your own words. A paraphrased frame drifts from the frozen one, and the drift is invisible on reading.

Step 1.2: If no Frame Lock exists, build one using that skill's procedure before drafting any prose. See [../narrative-evidence-ledger/resources/frame-lock.md](../narrative-evidence-ledger/resources/frame-lock.md). Whichever route you took, the frame is now frozen. Any later change to unit, denominator, window, or boundary re-opens the ledger. It is not a chart adjustment.

Step 1.3: Apply the rate-vs-count rule. If entities differ in size by more than roughly 2x, rates are mandatory for comparison and raw counts are supplementary, never the headline. If the denominator is itself moving, show both series — the ratio alone hides which term moved.

See [resources/quantitative-fidelity.md](resources/quantitative-fidelity.md) for the denominator-drift worked example.

**Step 2: Bind every number to a source and a precision**

Step 2.1: For each figure, record five things. The pointer: document and page, table and cell, query, row range, retrieval date. "The 10-K" is not a pointer. Then the source's own precision, OBSERVED or DERIVED, MEASURED or MODELLED, and CONTESTED or not.

Step 2.2: Hold the unrounded value. Every derived figure is computed from the held value and cites its pointer, never from a rounded sentence elsewhere in the draft.

Step 2.3: Never treat your own earlier draft, summary, or notes as a source for a number. A pointer that resolves inside your own pipeline is a hard failure and is invisible on reading.

**Step 3: Land the numbers, paragraph by paragraph**

Step 3.1: Run the [Number-Landing Checklist](#number-landing-checklist) on every data-carrying paragraph. Surplus figures go to a table, an exhibit, or a footnote — not into another sentence.

Step 3.2: Convert to human scale where a scale exists, and swap bureaucratic number-words for plain ones (see [resources/number-landing.md](resources/number-landing.md)).

Step 3.3: Where the protagonist is a system, do not let a single quantified individual stand in for a distribution without repair. If you open on one patient, one shipment, one training run, the next sentence must restore the distribution and say what that case is and is not typical of.

**Step 4: Route the uncertainty by type**

Step 4.1: For each load-bearing claim, name the DOMINANT uncertainty type — sampling, measurement, model/specification, coverage-missingness, or contested source. One type per claim; do not blend.

Step 4.2: Route it through the [Uncertainty Routing Table](#uncertainty-routing-table). Apply the momentum rule: uncertainty earns its own beat only when it would change the conclusion.

Step 4.3: Band only load-bearing judgments with the [Likelihood and Confidence Ladder](#likelihood-and-confidence-ladder), and declare the ladder's bands once, in the piece.

Step 4.4: Write the reference-model sentence: what a reader would have to assume for your signal to be absent. Omitting uncertainty does not avoid assumptions, it outsources them to a distribution in the reader's head that you cannot see.

**Step 5: Contract each exhibit that carries a beat**

Step 5.1: Write the beat sentence first, as one declarative claim, before drawing anything. Make the title that sentence, phrased so the chart's own marks can check it.

Step 5.2: Per annotation, write the falsification line privately: which specific marks would make this annotation false? Cannot answer means the annotation asserts something the chart does not show — cut it.

Step 5.3: Mark the leap-of-faith point on the exhibit wherever measurement ends and projection, model, or extrapolation begins.

Step 5.4: Run the detachment test: crop the exhibit out of the prose. Does it still carry the beat AND the caveat that qualifies it? Exhibits circulate alone.

See [resources/uncertainty-and-exhibits.md](resources/uncertainty-and-exhibits.md) for the annotation spec and density caps.

**Step 6: Run the drift and fidelity audit**

Step 6.1: DENOMINATOR SWEEP. List every number in the finished draft in order with its denominator. Any change of denominator across the sequence must either be reverted or narrated explicitly as a beat. This is the failure fact-checking cannot see: every exhibit defensible, the sequence a lie.

Step 6.2: RECOMPUTE. Recompute every total, share, and ratio from the held source values. Confirm parts still sum to the whole after rounding.

Step 6.3: Walk the [Fidelity Refusals](#fidelity-refusals). Each hit is a defect, not a preference.

Step 6.4: OMITTED-NUMBER LOG. List every figure you cut, and read the list as a set. Individually defensible cuts routinely form a pattern — the disconfirming quarter, the failed arm, the region that went the other way.

Step 6.5: HEDGE BUDGET. Count hedged sentences. Over roughly one in four in a passage means the passage is under-sourced, not over-cautious: go back to sources rather than deleting hedges. Never delete a hedge that reflects genuine evidential uncertainty.

Validate using [resources/evaluators/rubric_numbers_in_narrative.json](resources/evaluators/rubric_numbers_in_narrative.json). **Minimum standard**: average score >= 3.5.

## Number-Landing Checklist

Run per data-carrying paragraph. Caps are working defaults for narrative prose, not published thresholds. Tune them for your register, and say that you did.

| # | Check | Fix |
|---|-------|-----|
| 1 | More than three numbers in this paragraph? | Move the surplus to a table, exhibit, or footnote |
| 2 | More than one number in any sentence? | Split the sentence or cut a number |
| 3 | Can it be rounded without losing the claim? | 105% becomes doubled; 33% becomes one in three; 1.043bn becomes about a billion |
| 4 | Does the rounding erase a distinction that mattered? | Restore the digits and say in the sentence why the precision is the point |
| 5 | Does every surviving number have a comparison on the same screen? | Add a prior period, a peer, a denominator, or a physical referent |
| 6 | Is it at human scale where a scale exists? | Per person, per day, per shipment, per thousand doses, as a multiple of something owned |
| 7 | Direction before magnitude? | Say which way it moved, then how far |
| 8 | Does the paragraph open on a number with no frame? | Build the frame first, then land the number |
| 9 | Bureaucratic number-words? | expenditures to spending, utilization to use, headcount to staff, revenue to income |

**Bad (supply chain):** "Dwell time at the terminal averaged 4.7 days in Q3 against 3.2 days in Q2, with 61.4% of containers exceeding the 72-hour free window versus 44.9% prior, across 18,412 boxes."

**Good:** "Boxes started sitting longer. Containers that used to clear the terminal in three days took nearly five, and for the first time most of them — three in five, against fewer than half the quarter before — blew past the free-storage window and started billing."

**Bad (public health):** "Vaccination coverage in the district reached 62.3%, up 11.8 percentage points."

**Good:** "Coverage rose by a ninth of the district, from roughly half of children to roughly three in five. The threshold health officials use for measles herd immunity is closer to nine in ten."

## Fidelity Refusals

These are refusals, not preferences. Every hit is a defect.

- **Precision ceiling.** No figure may exceed the precision of its source. Source says "roughly a third" — you may never write 33.4%.
- **Rounding drift.** Never compute a derived figure from a rounded prose number. Compute from the held source value; recompute totals at the end.
- **Percent vs percentage point.** Never conflate. A rise from 4% to 6% is two percentage points and a fifty percent increase, and only one of those belongs in a given sentence.
- **Relative vs absolute.** Never present a relative change without the base when the base is small. "Cases doubled" from 3 to 6 is a different claim from 3,000 to 6,000.
- **Contested figures.** Both values, both sources, in the same sentence. "The operator put downtime at 40 minutes; the regulator's log records 94." Never average, never silently choose.
- **Model output in measurement grammar.** A projection, fit, simulation, or estimate may not wear the sentence shape of an observation. Not "throughput reaches 14,000 units in 2027" but "the capacity model puts throughput at about 14,000 units by 2027."
- **Trend from two points.** Two observations are a difference, not a trend. Never write "rising", "accelerating", or "the trajectory" off two data points.
- **Qualitative to numeral.** Never convert "many", "several", or "most" into a numeral the source does not contain.
- **Ranges survive.** If the source gives a range or interval, the prose carries it or states explicitly that it is using the midpoint.
- **Thin support.** Never lead on a figure resting on a handful of records or one reporting period. Extremes concentrated in the smallest denominators are sampling noise wearing a story's clothes.
- **Verified.** Never claim you verified, confirmed, or fact-checked a number. You sourced it.

## Uncertainty Routing Table

| Type | Vehicle | Placement |
|------|---------|-----------|
| Sampling | Interval, or frequency framing in words ("about one year in twenty looks like this") | Annotation layer of the exhibit it qualifies |
| Measurement | Stated range or instrument-precision note | Exhibit caption AND the sentence that first uses the number |
| Model / specification | Two or more specifications shown side by side; their disagreement is the point | Its own beat — here the disagreement outranks any point estimate |
| Coverage / missingness | Render the absence: shade the gap, count what is missing, name who is not in the denominator | In the exhibit — missingness rendered as blank space is invisible |
| Contested source | Both sources as separate series with provenance; say which you believe and why | Own beat if they disagree on sign, otherwise annotation layer |

**Momentum rule:** uncertainty earns its own beat only when it would change the conclusion. Otherwise it rides in the annotation layer. This is what preserves pace without hiding anything.

**Never** route all uncertainty to a trailing methods note. **Never** hedge every sentence — readers then fall back on the headline, which is the one unhedged artifact in the piece.

**Self-diagnostic.** Three thoughts mean you are rationalising an omission rather than editing (Hullman, IEEE TVCG 2020). "The exhibit should express a clear signal." "The analysis was rigorous, so the reader can trust it." "This would muddy the message." Catch any of the three and route the uncertainty.

## Likelihood and Confidence Ladder

Two different quantities. **Likelihood** is how probable the thing is. **Confidence** is how good your evidence is. Never combine them in one sentence: "we are highly confident this is very likely" is unparseable and hides which one is weak.

| Likelihood term | Band |
|-----------------|------|
| almost no chance / remote | 01-05% |
| very unlikely / highly improbable | 05-20% |
| unlikely / improbable | 20-45% |
| roughly even chance | 45-55% |
| likely / probable | 55-80% |
| very likely / highly probable | 80-95% |
| almost certain / nearly certain | 95-99% |

**Attribution:** these seven bands are ICD 203's published lexicon. `narrative-fallacy-guard` carries the same ladder, so a draft run through both skills gets one ladder rather than two. Declare it once in the piece, where a reader meets it before the first banded judgment, and never let a term drift off its band mid-draft. If you substitute another published standard, substitute it everywhere. A piece must never carry two ladders.

Confidence is a separate three-rung scale, and it is this skill's own: LOW (single source, or sources disagree on sign), MODERATE (multiple sources agreeing, known gaps), HIGH (direct primary evidence, replicated). Confidence is not a probability, which is why it never shares a sentence with a likelihood band.

**Banding applies only to load-bearing judgments** — the ones a reader would act on. Banding every sentence produces the hedge flooding described above and costs the same credibility as no banding at all.

## Guardrails

**Requirements:**

1. **Frame Lock in writing**: unit, denominator, window, boundary — plus one rejected alternative each — before any prose. Holding it in working memory is how drift happens.
2. **Pointer per number**: every figure resolves to an external artifact. Pointers into your own drafts are a hard failure.
3. **Denominator sweep before shipping**: an unnarrated change of denominator across the piece is the defect fact-checking cannot detect.
4. **Falsification line per annotation**: no annotation ships without the private sentence naming the marks that would falsify it.
5. **Leap-of-faith mark**: every exhibit containing projected, modelled, or extrapolated values marks where measurement ends.
6. **One uncertainty type per claim**, routed by table, placed inside the claim it qualifies.
7. **Omitted-number log reviewed as a set**, not per cut.

**Common pitfalls:**
- The stat wall: five figures and three percentages in one paragraph, packed in to demonstrate rigour, exactly where the evidence was strongest and the reader stops reading.
- Rounding away the distinction that was the whole point ("about a billion" when 1.04bn versus 1.4bn is the argument).
- Defensive over-disclosure: answering an honesty audit by adding twelve caveat exhibits and four hedging paragraphs. Volume is not integrity. The operative test is whether a disagreeing reader can find your strongest counter-number within one exhibit.
- Intentionality verbs on systems: "the market priced in", "the protocol decided", "the index knew". Each is an unsourced claim about collective intent smuggled through a verb. Rewrite as aggregated behaviour of named actors, or mark it once as shorthand.
- Deleting hedges during a style pass and silently raising a claim's confidence past its evidence.
- Letting one quantified individual — one patient, one customer, one run — stand for a distribution without the sentence that says what it is not typical of.

## Quick Reference

**Key resources:**
- **[resources/number-landing.md](resources/number-landing.md)**: the landing checklist with bad/good pairs across market history, epidemiology, ML evaluation and supply chain; rounding table; human-scale conversions; bureaucratic word swaps; opening-frame patterns
- **[resources/quantitative-fidelity.md](resources/quantitative-fidelity.md)**: Frame Lock template, denominator-drift worked example, precision and rounding rules, percent vs percentage point, contested-figure grammar, model-vs-measurement grammar, person and system variants
- **[resources/uncertainty-and-exhibits.md](resources/uncertainty-and-exhibits.md)**: expanded routing table, likelihood and confidence ladder usage, hedge budget, chart-beat contract, annotation spec and density caps, detachment and falsification tests
- **[resources/evaluators/rubric_numbers_in_narrative.json](resources/evaluators/rubric_numbers_in_narrative.json)**: quality scoring

**Inputs required:**
- The draft or passage carrying the figures
- The source values at full precision, with pointers
- Which claims are load-bearing (what a reader would act on)

**Outputs produced:**
- Frame Lock block (unit, denominator, window, boundary, plus rejected alternatives)
- Revised prose passing the number-landing checklist
- Uncertainty routing decisions, one type per load-bearing claim
- Chart-beat contract per exhibit: beat sentence, title, falsification lines, leap-of-faith mark
- Denominator sweep result, recomputation result, omitted-number log, refusal-list defects

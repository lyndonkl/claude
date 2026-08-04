# Frame Lock

Every fact in a piece can be true and the piece still be false. In quantitative and semi-quantitative material, falsity lives in the choices — unit, denominator, window, boundary, aggregation level, which measure is foregrounded — not in the facts. Fact-checking cannot detect this. Only a written, frozen frame can.

## Table of Contents
- [The four locks](#the-four-locks)
- [The rejected-alternative record](#the-rejected-alternative-record)
- [Worked frame locks, three domains](#worked-frame-locks-three-domains)
- [Rate versus count](#rate-versus-count)
- [Denominator language](#denominator-language)
- [Denominator drift](#denominator-drift)
- [The instrument check](#the-instrument-check)
- [The three vetoes](#the-three-vetoes)
- [The seven metamorphic transforms](#the-seven-metamorphic-transforms)
- [The starting-hypothesis diff](#the-starting-hypothesis-diff)
- [When the protagonist is a person](#when-the-protagonist-is-a-person)

## The four locks

Written before any material is examined. Four lines.

| Lock | The question | Fails when |
|------|-------------|-----------|
| UNIT | What is one row? One case, one person, one incident, one shipment, one training run, one episode? | The unit changes mid-analysis: incidents become incident-days become affected users |
| DENOMINATOR | Per what? Per person, per dollar, per attempt, per unit of exposure, per deploy? | Absolute counts are compared across entities of different size |
| WINDOW | From when to when, and what justifies each edge? | The start date is the one that makes the trend work |
| BOUNDARY | Which entities are in the population, and who drew that line — you, the source, or a regulator? | The boundary is inherited from a source without being noticed |

Lock all four in writing. **Any later change re-opens the ledger.** It is not a chart adjustment. A changed denominator can invalidate findings, claims, and beats simultaneously, because it changes what the numbers mean rather than what they are.

## The rejected-alternative record

For each of the four, name one alternative you rejected and give a one-sentence reason. This is the anti-cherry-picking record, and it is the artefact you produce when someone asks why the analysis starts in 2019.

Format:

```
UNIT: one confirmed incident, as classified by the on-call at declare time.
  Rejected: one customer-affecting minute. Reason: minute-level data begins
  only in 2023 and would truncate the window by four years.

DENOMINATOR: per 1,000 production deploys.
  Rejected: per engineer-month. Reason: headcount data is quarterly and the
  team boundary moved twice, so the denominator would itself be unstable.

WINDOW: 2019-01-01 to 2025-12-31.
  Rejected: starting 2017. Reason: the incident classification scheme changed
  in December 2018 and no re-baselined series exists before it.

BOUNDARY: services owned by the platform group per the 2025 service registry.
  Rejected: all services in the monorepo. Reason: that set includes 40
  experiment services with no on-call rotation, which have no incidents by
  construction and would deflate every rate.
```

Note what the last entry does. It names a boundary choice that would have moved the headline number in a specific direction, and says why it was rejected on grounds unrelated to the direction. That is the difference between a frame lock and a rationalisation.

## Worked frame locks, three domains

### Public health

```
UNIT: one laboratory-confirmed case, by specimen collection date.
  Rejected: one person-episode. Reason: reinfections cannot be linked in this
  dataset, so person-episodes would be undercounted at an unknown rate.

DENOMINATOR: per 100,000 residents, from the mid-year population estimate.
  Rejected: per 100,000 tests. Reason: test volume tracks the outbreak itself,
  so a per-test rate would suppress exactly the signal under study. Both series
  are shown; the per-test view is a supplementary beat, not the headline.

WINDOW: 2021-W01 to 2024-W52.
  Rejected: starting 2020-W10. Reason: case ascertainment before 2021 was
  limited by test availability and is not comparable.

BOUNDARY: residents of the reporting region, by residence not by treatment
site.
  Rejected: patients treated in the region. Reason: two tertiary hospitals
  draw from outside the region and would inflate counts against a resident
  denominator.
```

### Manufacturing market history

```
UNIT: one 300mm wafer start.
  Rejected: one die. Reason: die counts depend on reticle size, which changed
  twice in the window, so a die series would mix a demand signal with a
  geometry change.

DENOMINATOR: per installed tool, for utilisation; absolute starts for the
capacity beat.
  Rejected: per fab. Reason: fabs differ in size by more than 10x, so a
  per-fab rate is dominated by which fabs are in the sample.

WINDOW: 1998-Q1 to 2008-Q4.
  Rejected: ending 2010. Reason: the 2009 accounting restatement at two of the
  five reporters makes 2009-2010 non-comparable without a re-baselined series.

BOUNDARY: the five merchant foundries filing quarterly in every year of the
window.
  Rejected: all foundries. Reason: entrants and exits would make the panel
  unbalanced and the "industry" series would move with sample composition.
```

### ML evaluation writeup

```
UNIT: one evaluation run at a fixed seed and a fixed prompt template.
  Rejected: one benchmark item. Reason: items are not independent within a
  task family and per-item claims would overstate precision.

DENOMINATOR: per 1,000 evaluation items attempted, not per item scored.
  Rejected: per item scored. Reason: refusals and timeouts drop out of the
  scored set, which would silently reward a model that refuses more.

WINDOW: model releases from 2024-06 to 2026-03.
  Rejected: including pre-2024 checkpoints. Reason: the harness changed its
  tokenisation of the prompt template in May 2024; earlier scores are not
  comparable.

BOUNDARY: models with published weights or a stable API version string.
  Rejected: all models evaluated. Reason: three endpoints changed behind the
  same version string during the window, so their series measure the endpoint,
  not the model.
```

## Rate versus count

If entities differ in size by more than roughly 2x, rates are mandatory for comparison and raw counts are a supplementary beat, never the headline. (The 2x figure is a derived default.)

If the **denominator itself is changing** — a shrinking population, a growing user base, a fleet that doubled — show both series. A ratio alone conceals which term moved. A falling incident rate during a period when deploys tripled is a different finding from a falling incident rate at flat deploy volume, and the ratio cannot tell them apart.

**Small-denominator check.** Plot the measure's variance against denominator size. If the extremes all sit in the smallest decile of denominators, the extremes are sampling noise wearing a story's clothes.

This matters because any ranking built on surprise — the rarest configuration, the biggest outlier, the largest percentage change — is maximised by small denominators, coding errors, partial reporting periods, and newly created categories. An agent that picks its protagonist by novelty alone will reliably crown noise, and the resulting narrative will be structurally sound and built on a county of 400 people, a month of incomplete filings, or a benchmark with 12 examples.

## Denominator language

Get the words right. This is the most checkable error in quantitative writing.

- **"Per capita" means per person.** A figure of 2.3 per 1,000 residents is not a per-capita figure. Say "per 1,000 residents".
- **Percent versus percentage point.** A move from 4% to 6% is a 2 percentage-point rise and a 50% rise. Never conflate them.
- **Relative versus absolute change.** "Doubled" and "rose by 3" are different claims and the second requires a base.
- **Precision ceiling.** No figure in prose may exceed the precision of its source. A source saying "roughly a third" can never become "33.4%".
- **Round for prose, compute from source.** The ledger holds the unrounded value. Derived figures reference the source finding ID, never a rounded prose sentence. Rounding drift compounds: round for readability, use the rounded figure as input to the next ratio, and by the third derivation the number is outside the source's range while still wearing "about".
- **Hedge words are precision claims.** "About" implies roughly the rounding unit. "Nearly" and "more than" assert a direction and must be true. "Roughly" signals genuine estimate uncertainty. None of them are decoration.
- **Never manufacture a number from a qualitative source.** "Several" does not become "six". "Many" does not become "dozens".

## Denominator drift

The characteristic sequence-level lie. The piece opens on counts. It pivots to per-capita for the one comparison where per-capita favours the thesis. It returns to counts for the conclusion. Every individual exhibit is defensible. The sequence is false, and it survives fact-checking because no single number is wrong.

**Detection**: build a table of every figure in the piece against the denominator it uses. Any change of denominator between adjacent claims must be either (a) narrated in the text at the point of change, or (b) reverted.

Bad, from an operations writeup:

> Incidents rose from 41 to 58 last year. Our incident rate per deploy remains the lowest in the division. The 58 incidents represent our worst year on record.

Three sentences, two denominators, one unstated switch, and the switch happens exactly where it helps.

Good:

> Incidents rose from 41 to 58 last year, against a deploy volume that rose from 3,900 to 7,100. The rate per 1,000 deploys therefore fell from 10.5 to 8.2. Both the raw count and the rate matter here: the count is what on-call carried, and the rate is what the process improved.

## The instrument check

**Did the world change, or did the measurement change?**

This is the most common catastrophic failure in data narrative. A break in the data-generating process gets narrated as a break in the world. The resulting story is internally consistent, vividly told, well-sourced, and entirely spurious — and it is usually *more* confident and better structured than a correct one, because measurement artifacts produce sharper discontinuities than real transitions do.

Run on every discontinuity before it becomes a finding. Enumerate:

| Artifact type | Examples |
|--------------|----------|
| Definitional revision | Reclassification; a metric's formula changed; "active user" redefined; a diagnostic code split |
| Coverage or sampling change | New reporters added; a survey redesigned; a sensor fleet expanded; a region joined the panel |
| Methodology restatement | Accounting restatement; seasonal adjustment introduced; a benchmark's scoring changed |
| Reporting-lag artifact | The most recent periods are incomplete and look like a decline |
| Entity or boundary change | Merger, demerger, redistricting, team reorganisation, service ownership transfer |
| Collection-platform change | Reporting moved from email to a form; a logging library upgraded; an API version changed what got counted |

**Dispositions:**

1. The discontinuity coincides with a known instrument change and you can re-baseline on a consistent definition → keep the finding, cite the re-baselined series.
2. It coincides and you cannot re-baseline → the finding goes to DEAD with `killed_by: instrument check`, verdict DID-NOT-SUPPORT. **The instrument change is now the finding.** Narrate it.
3. No instrument change identified → keep, and record which artifact types you checked. "Checked and none found" is a real result and it strengthens the finding.

**Change-point forking.** Scanning many series with many methods until a break lands where the thesis wants it is a garden of forking paths. Control it by writing down which series and which methods you will scan, before scanning. Record rejected candidates and why. That list is the defence against a cherry-picked start date.

**Time-to-detect.** For surviving discontinuities, compute when a contemporary observer, with only the data then available, could have seen it. The gap between the event and its detectability is usually the most interesting thing in the material, and it is the honest source of dramatic irony.

## The three vetoes

Applied in order to any measure being considered as the piece's central quantity.

1. **DENOMINATOR VETO.** Can you defend the denominator in one sentence to a hostile reader? No → kill.
2. **THIN-SUPPORT VETO.** Does the top-ranked finding for this measure rest on fewer than about 5 underlying records, or on a single reporting period? Yes → kill. (The 5-record figure is a derived default.)
3. **IRRELEVANCE VETO.** Does the audience hold any prior belief about this measure? No prior → nothing can be surprising → kill, or spend a beat establishing the prior first.

Every veto kill goes to DEAD with the veto named. That column is the record of what the story is not.

## The seven metamorphic transforms

Applied per claim, after the ledger is built. Any transform that flips the claim kills it, or promotes the sensitivity itself to being the claim.

1. **Shuffle row order.** The conclusion must be invariant. Catches draw-order and order-dependent aggregation.
2. **Swap SUM ↔ MEAN and COUNT ↔ RATE.** If the claim flips, state which is correct and why, in the text. Catches aggregation masking.
3. **Change bin count and bin origin by ±50%.** Distribution claims must survive. Catches binning artifacts.
4. **Extend and truncate the window by one period at each end.** Trend and change-point claims must survive. Catches start-date cherry-picking.
5. **Re-aggregate spatial or categorical units at a different boundary.** Catches boundary choice manufacturing the pattern.
6. **Drop the top 1% of records.** Extreme, outlier, and mean-based claims must be re-checked. Catches thin-support extremes.
7. **Re-render at two aspect ratios.** Slope and correlation claims must survive. Catches visual slope distortion.

**Before all seven, the forgotten-population check**: who is not in this dataset who should be, and would including them change the sign?

**Also run the re-aggregation test for sign flips.** Re-run the headline at two other aggregation levels and two other filter sets. If the sign flips at any level, that is Simpson's paradox and the disaggregated view is the story, not a footnote.

Record every failure in DEAD with the transform that killed it.

**Metamorphic testing is a floor, never a certificate.** A claim can pass all seven while resting on the wrong population, the wrong denominator, or a definitional break in the source, because all three are upstream of anything the transforms touch. Reporting the transforms as a certificate is worse than not running them.

## The starting-hypothesis diff

Write the starting hypothesis down, verbatim and dated, before examining material. At handoff, diff the current reading against it and write what changed.

The ordering matters and is not stylistic. Suppose the thesis exists before the finding inventory. Then every downstream choice bends toward that sentence: the denominator, the window, the aggregation, which discontinuity gets an instrument check and which gets waved through. The agent doing the bending has no way to notice it. Inventory first, spine second, thesis third, then diff.

If nothing changed, either you were unusually right or you did not look. Say which you believe.

## When the protagonist is a person

The frame lock still applies, and it is easier to skip because personal narrative does not feel quantitative.

- **UNIT**: what is one episode in this life? A job, a year, a project, a relationship, a publication? Biographies that switch silently between these produce careers that look denser or sparser than they were.
- **DENOMINATOR**: compared with what? Peers of the same cohort, the same institution, the same starting resources? A career described without a comparison class is a career described as unique by construction.
- **WINDOW**: what justifies where the account starts and stops? Starting at the first success is the biographical equivalent of a cherry-picked start date.
- **BOUNDARY**: whose accounts are in the population of sources? An archive assembled by the subject's family is a boundary someone else drew.

**Individualization warning.** Framing a distributional finding through one quantified person is a rhetorical technique with real framing power, not a neutral choice. It raises engagement precisely because it invites the reader to reason from a single case. When the real protagonist is a system — a market, a protocol, an institution, a supply chain — an individualized opening will be the most-remembered part of the piece and the least representative. If you use it, the very next beat must restore the distribution, and the text must say explicitly what the individual is and is not typical of.

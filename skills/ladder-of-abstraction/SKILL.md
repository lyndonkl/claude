---
name: ladder-of-abstraction
description: Moves prose deliberately between the concrete and the abstract and stops it stranding in the middle rung where bureaucratic prose lives. Tags every paragraph R1 (named particulars) to R4 (meaning), enforces run rules, detects the middle-rung trap, repairs it by climbing down to a real particular rather than simplifying vocabulary, gates the top rung with a counter-sentence test, and closes with an A-frame descent. Use when a draft reads as dense, vague, or jargon-heavy, when a readability score fails, when a conclusion feels grandiose or unearned, when technical material will not land for a general reader, or when user mentions ladder of abstraction, too abstract, too vague, concrete example, middle rung, dead zone, jargon, altitude, zoom in, zoom out, and thus capitalism.
---

# Ladder Of Abstraction

## Table of Contents
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [The Four Rungs](#the-four-rungs)
- [Run Rules and Violations](#run-rules-and-violations)
- [Readability Routing](#readability-routing)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

**Related skills:** Use `readability-check` for the actual scoring pass (this skill diagnoses what a failing score means), `writing-structure-planner` for section order and shape, `hedge-detector` when repairs threaten epistemic hedges, `abstraction-concrete-examples` for building explanatory ladders from scratch rather than auditing a draft, `systemic-protagonist` for the full agency-repair ledger when the subject is a system.

## Core Principles

1. **The middle rung is a transit lane, not a parking space**: prose the reader can neither see nor understand is usually stuck halfway up, not too technical.
2. **Climb down, never simplify**: the only real fix for an abstract paragraph is one particular instance from the material. Swapping jargon for plainer jargon changes the reading score and not the comprehensibility.
3. **No particular, no paragraph**: if the material contains no instance, that is a reporting gap to log, not a detail to invent.
4. **The honest ceiling is set by the material**: if your top-rung claim could be attached to any story in the domain, it is generic. A piece is allowed to mean something small.
5. **Alternation constrains runs, not paragraphs**: rung-switching every beat produces jerky text where no idea is developed.
6. **One move per step**: R1 to R4 in a single jump is what produces the "and thus, capitalism" reading. Land on R2 or R3.
7. **The tags are planning instruments**: rung labels, altitude talk, and "as we saw above" must never appear in the delivered prose.

## Workflow

Copy this checklist and track your progress:

```
Ladder Audit Progress:
- [ ] Step 1: Declare the honest ceiling from the material
- [ ] Step 2: Tag every paragraph R1-R4
- [ ] Step 3: Run the run-rule audit and list violations
- [ ] Step 4: Repair traps by climbing down; log gaps; escalate
- [ ] Step 5: Gate the top rung and build the A-frame close
- [ ] Step 6: Route readability failures; strip structural residue
```

**Step 1: Declare the honest ceiling from the material**

Step 1.1: Before tagging anything, write one sentence naming the highest rung the material earns, and list the specific evidence under it. Do this from the source record, not from the draft.

Step 1.2: If the material contains two or three independent findings, do not force one covering abstraction. Give each its own section with its own ascent, or change the form.

Step 1.3: Record the ceiling as R2, R3, or R4. Most analytical material tops out at R3. Ending at R2 is a legitimate outcome for a status report or a mechanism explainer.

**Step 2: Tag every paragraph R1-R4**

Step 2.1: Assign exactly one rung per paragraph (or per planned beat, if working from an outline). Ambiguous is not a rung. Force a decision, then note why it was hard.

Step 2.2: For each R3 and R4 paragraph, name by pointer the R1 evidence it rests on. An R3 with no pointer is unsupported altitude.

Step 2.3: Produce the rung map as a table: paragraph number, rung, one-phrase content, R1 pointer.

See [resources/rung-tagging.md](resources/rung-tagging.md) for the full rung definitions, the person and system variants, and worked tagging examples.

**Step 3: Run the run-rule audit and list violations**

Step 3.1: Apply the six run rules in [Run Rules and Violations](#run-rules-and-violations) against the rung map. Output every violation with its paragraph range and rule number.

Step 3.2: Compute the middle share: R2 sentences as a fraction of total sentences in the passage. Above roughly 40 percent the passage is parked in the dead zone. Treat this as a tunable default, not a published figure.

Step 3.3: Do not fix anything yet. A full violation list first prevents local patching that creates a new trap two paragraphs down.

**Step 4: Repair traps by climbing down; log gaps; escalate**

Step 4.1: For each MIDDLE-RUNG TRAP, go to the source material and find one particular instance of the mechanism the paragraph describes. Replace or precede the abstract statement with it.

Step 4.2: Check the particular for representativeness. If it is the most extreme case you found rather than a typical one, either flag it as extreme in the prose or do not use it in a load-bearing position.

Step 4.3: If no particular exists in the material, write a GAP entry: what mechanism needs an instance, what kind of artifact would supply it, where you looked. Leave the paragraph as honest summary. Never fill it with a plausible specific.

Step 4.4: If a section accumulates three or more gaps, stop repairing and escalate: report that the defect is missing material, not missing prose, and that it cannot be fixed at this layer.

See [resources/rung-tagging.md](resources/rung-tagging.md) for the trap repair table and before-and-after repairs in three domains.

**Step 5: Gate the top rung and build the A-frame close**

Step 5.1: State each R4 claim out loud, then write its counter-sentence. If the counter-sentence is equally supported by the evidence, delete the R4 beat.

Step 5.2: Apply the generic test: could this abstraction be attached to any story in this domain? If yes, cut it or drop to R3.

Step 5.3: Build the A-frame close: restate the surviving abstraction through one R1 particular the reader has already met and now sees differently. The close descends; it does not summarize.

See [resources/top-rung-discipline.md](resources/top-rung-discipline.md) for the counter-sentence test, the meaning-inflation catalogue, and A-frame closes in four domains.

**Step 6: Route readability failures; strip structural residue**

Step 6.1: For any failing paragraph flagged by `readability-check`, classify it (a), (b), or (c) using [Readability Routing](#readability-routing) before editing a single word.

Step 6.2: After every repair, diff the meaning, not just the score. If the score improved and the propositional content changed, the fix failed and must be reverted.

Step 6.3: Sweep out structural residue: rung vocabulary, "zooming out", "at a high level", "as we saw above", and signposted section labels. Readers must not be able to recite the scaffolding.

Validate using [resources/evaluators/rubric_ladder_of_abstraction.json](resources/evaluators/rubric_ladder_of_abstraction.json). **Minimum standard**: average score >= 3.5.

## The Four Rungs

| Rung | Holds | Test it passes | Person protagonist | System protagonist |
|------|-------|----------------|--------------------|--------------------|
| R1 | Named particulars: a person, a date, an object, a number with a unit, a quoted line | Could be photographed, timestamped, or cited to a line in a document | "On 3 March 1988 Kilby signed the memo declining the second fab" | "At 09:41:02 the order book showed 4 lots bid at 88.25" |
| R2 | Category, mechanism, process, policy | Names a class or a how, with no instance attached | "She had authority over capital approvals" | "Fee schedules pay more for blocks confirmed inside 400ms" |
| R3 | System pattern: what the case is an instance of, across cases | Holds for more than one instance and could be falsified by a counter-case | "Founders who kept signing authority slowed their own expansion" | "Contract markets reprice slower than spot in every episode in the sample" |
| R4 | Meaning and stakes: trust, risk, obsolescence, scarcity, accountability | Survives the counter-sentence test in Step 5.1 | "Control was the thing she could not delegate" | "Latency became the price of admission" |

**Rung scheme caveat**: the ladder is Hayakawa's, operationalized for prose by Roy Peter Clark. The four-rung split used here separates pattern (R3) from meaning (R4); Hart and Clark work with three rungs. Treat R3/R4 as this skill's operational refinement, not as anyone's published taxonomy.

**System-specific R2 rule**: a system's mechanism sentence must not take an intentional verb. "The market decided", "the protocol wanted", "the model learned to hide" are causal claims wearing a sentence. Relocate agency onto the entity that has it: name the actor, the mechanism, the selection pressure, or the quoted human. Do not overcorrect into agentless passive, which obscures causation worse. Full repair table in `systemic-protagonist`.

## Run Rules and Violations

| # | Rule | Violation name | Repair |
|---|------|----------------|--------|
| 1 | No more than 2 consecutive R2 or R3 paragraphs | STALLED RUN | Insert an R1 instance, or merge the two abstractions into one |
| 2 | Every R3/R4 run must be preceded within 2 beats by an R1 | UNGROUNDED ASCENT | Move an existing R1 earlier; do not write a new one from imagination |
| 3 | Any R2 paragraph with no R1 within plus-or-minus 2 paragraphs | MIDDLE-RUNG TRAP | Climb down: supply one particular from the material (Step 4) |
| 4 | Never move R1 to R4 in one step | ALTITUDE JUMP | Land on R2 or R3 first: name the mechanism or the pattern the particular belongs to |
| 5 | The piece opens on R1; each section lands at or below its declared ceiling | FLOATING OPENER | Replace the opening abstraction with the particular that made you believe it |
| 6 | The close descends through an R1 the reader already met | MISSING A-FRAME | Build the descent (Step 5.3) |

**Sawtooth fatigue** is the counter-failure. Rules 1 through 3 are ceilings on runs, not a metronome. An R1 paragraph followed by R2, R1, R2, R1, R2 satisfies every rule and reads as a stutter where no idea is developed. If more than half the paragraphs change rung from their neighbor, the ladder is being climbed too fast; consolidate.

**Numeric caveat**: the plus-or-minus-2 window, the 2-paragraph run ceiling, and the 40 percent middle share are operational defaults derived for mechanization. Ship them as tunable config, not as figures anyone published.

## Readability Routing

A failing Flesch-Kincaid, Fog, or SMOG score is a symptom. Routing it to synonym substitution games the formula, because these scores are functions of sentence length and syllable count only. Classify first.

| Class | Symptom | Correct fix | Health signal |
|-------|---------|-------------|---------------|
| (a) | Long sentences, concrete content | Split. Safe, mechanical | A run dominated by (a) is healthy |
| (b) | Short sentences, dense abstract nouns | MIDDLE-RUNG TRAP. Supply a concrete R1 example, which may require returning to the material | A run dominated by (b) "fixed" without new material is a warning sign |
| (c) | Necessary technical terms | Do not simplify. Define once, in one clause, concretely, on first use | Never counts as a readability failure once defined |

**Forbidden fixes, in every class:**
- Replacing a precise term with a vaguer one
- Deleting a qualifier ("approximately", "in this sample", "under these assumptions", "as of [date]") to shorten a sentence
- Splitting a sentence in a way that severs a causal link
- Swapping jargon for plainer jargon: this moves the score and not the comprehensibility

## Guardrails

**Requirements:**
1. **Gap over invention**: a trap with no particular in the material produces a GAP entry, never prose. A nonzero gap count is reportable output, not a failure to hide.
2. **Ceiling declared before drafting**: the top rung is decided from the material in Step 1. A ceiling discovered while writing the last paragraph is meaning inflation.
3. **Counter-sentence on every R4**: no meaning claim ships without its opposite written down and judged less supported.
4. **Meaning-diff every readability repair**: record the class (a/b/c) of each fix and confirm the propositional content survived.
5. **Escalate rather than compensate**: when the defect is missing material or a wrong structure, report upward. Do not paper over it with prose polish.
6. **Representativeness flagged**: any R1 used in a load-bearing position that is the extreme case rather than the typical one must say so.
7. **Scaffolding invisible**: rung tags, altitude language, and roadmap sentences are stripped before delivery.

**Common pitfalls:**
- Crowning a modest finding with universal significance: a chip-supply analysis that "is really a story about human ambition". Not every worm story is about justice (Sabrina Imbler, via The Open Notebook).
- Fixing a middle-rung trap by simplifying vocabulary, which lowers the grade level and leaves the paragraph exactly as unintelligible.
- Generating the missing particular. Concrete sensory specificity is the easiest thing to fabricate and the hardest thing to detect afterward.
- Forcing one unifying abstraction onto material containing three independent findings.
- Skipping R2 and R3 entirely, so the reader gets particulars and then meaning with no visible path between them.
- Over-alternating until the piece stutters (sawtooth fatigue).
- Letting a system hold intentional verbs at R2, which smuggles in causation the analysis never established.

## Quick Reference

**Key resources:**
- **[resources/rung-tagging.md](resources/rung-tagging.md)**: rung definitions with edge cases, person and system variants, worked tagging of three passages, the trap repair table, before-and-after repairs, gap log format
- **[resources/top-rung-discipline.md](resources/top-rung-discipline.md)**: counter-sentence test, meaning-inflation catalogue, honest-ceiling decision table, A-frame closes in four domains, attribution caveats
- **[resources/evaluators/rubric_ladder_of_abstraction.json](resources/evaluators/rubric_ladder_of_abstraction.json)**: quality scoring

**Inputs required:**
- The draft or beat outline to audit
- Access to the source material (the record the particulars must come from)
- Declared audience, if a readability target applies

**Outputs produced:**
- Rung map table: paragraph, rung, content phrase, R1 pointer
- Violation list keyed to rules 1-6, with paragraph ranges
- Declared ceiling with its evidence, and the counter-sentence for every surviving R4
- Repaired passages, each labelled with the repair type
- Gap log: mechanisms lacking a particular, artifact sought, where searched
- Escalation note when the defect is material or structure rather than prose

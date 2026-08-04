---
name: prose-force-and-rhythm
description: Runs Jack Hart's Wordcraft line passes in strict order (Structure, Force, Brevity, Clarity, Rhythm, Humanity, Color, Voice, Mechanics) followed by a slop audit, one pass per edit class, with a claim-strength invariant that stops verb strengthening and hedge cutting from silently overclaiming. Enforces upward escalation instead of downward compensation, a protected-hedge list, a clarity split log the rhythm pass may not undo, and rhythm metrics reported as diagnostics rather than optimized. Use when line-editing a draft, tightening flabby prose, fixing weak verbs or monotonous sentence rhythm, de-slopping AI-sounding copy, or when user mentions line edit, force pass, punch it up, tighten this, passive voice, wordy, sentence variety, sounds like AI, burstiness, or Wordcraft.
---

# Prose Force and Rhythm

## Table of Contents
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [The Ten Passes](#the-ten-passes)
- [The Claim-Strength Invariant](#the-claim-strength-invariant)
- [List A and List B](#list-a-and-list-b)
- [Diagnostics, Not Objectives](#diagnostics-not-objectives)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

**Related skills:** Use `writing-structure-planner` for the structural layer this skill escalates to, `readability-check` for scoring reader-facing prose, `writing-revision` for a lighter three-pass cleanup when the full pipeline is overkill, `slop-detector` for the machine-register signature scan Pass 10 delegates to.

## Core Principles

1. **One pass, one edit class**: Each pass may make only edits of its own kind. Running all passes in one prompt collapses them into "improve this writing" and implements none of them.
2. **Escalate up, never compensate down**: A pass that cannot fix a defect inside its own class files an escalation record and moves on. It does not paper over a structural or reporting failure with prose polish.
3. **Claim strength is invariant under editing**: Record each sentence's epistemic strength before rewriting and assert it survived. No pass may raise a claim's strength, because no pass has new evidence.
4. **Two word lists, not one**: Cut List A on sight. Protect List B absolutely. Hart's parasite list was tuned for newspaper prose about events that happened; on technical, medical, legal, and financial material the qualifiers are the content.
5. **Metrics diagnose, they do not command**: Report sentence-length mean, standard deviation, and cut percentage alongside the prose. An agent optimizing variance inserts one-word sentences.
6. **Mechanics is last, always**: Never before Voice. Fixing commas in a paragraph that should not exist is the default LLM failure.
7. **Thresholds are config, not canon**: Every number here is an operational default derived for mechanization, not a figure Hart publishes. Label it as such wherever it is reported.

## Workflow

Copy this checklist and track your progress:

```
Prose Force and Rhythm Progress:
- [ ] Step 1: Configure the run and build the claim ledger
- [ ] Step 2: Pass 1 STRUCTURE (gate: escalate or proceed)
- [ ] Step 3: Passes 2-4 FORCE, BREVITY, CLARITY (separately)
- [ ] Step 4: Passes 5-7 RHYTHM, HUMANITY, COLOR
- [ ] Step 5: Passes 8-9 VOICE, then MECHANICS
- [ ] Step 6: Pass 10 SLOP AUDIT, then the run report
```

**Step 1: Configure the run and build the claim ledger**

Step 1.1: Declare the register (analytical, explanatory, narrative), the audience, and the domain risk class. Domain risk class HIGH (medical, legal, financial, safety, scientific) turns the claim-strength invariant and List B protection into hard blocks; class LOW (newsletters, essays, internal notes) keeps them as warnings.

Step 1.2: Write the tunable config. Copy the defaults from [resources/rhythm-diagnostics.md](resources/rhythm-diagnostics.md) and adjust for the register. Record in the config header: "thresholds are derived operational defaults, not published Hart figures."

Step 1.3: Build the claim ledger before any edit. One row per sentence that carries a claim: sentence id, S-level (S1-S5), the exact words carrying the strength, source cited. See [resources/claim-strength-ledger.md](resources/claim-strength-ledger.md).

**Step 2: Pass 1 STRUCTURE (gate)**

Step 2.1: Ask two questions only. Is each paragraph in the right place? Does each section advance the piece's central claim?

Step 2.2: Defects here are not yours to fix. File an escalation record (defect, why it is structural, target layer) and hand it to the structural planner or the human. Do not proceed on a draft with unresolved structural escalations in HIGH risk class; in LOW class, proceed but carry the escalations into the run report.

**Step 3: Passes 2-4 FORCE, BREVITY, CLARITY (separately)**

Step 3.1: FORCE. Run the verb audit on every sentence: "to be" as main verb, light verbs, nominalized actions, expletive openers, suffix clusters, abstract nouns as subjects. Convert passive only where the actor is named in the material; otherwise leave the passive and log a reporting gap. Check S-level after every rewrite.

Step 3.2: BREVITY. Cut List A. Protect List B. Attempt a 20-word version of every sentence over 30 words and accept only if no proposition is lost. Report the cut percentage.

Step 3.3: CLARITY. One-reading test per sentence. Fix by splitting or by supplying the missing concrete referent, never by vaguer wording. Every split you make goes in the **clarity split log**, which the rhythm pass may not reverse.

See [resources/pass-playbook.md](resources/pass-playbook.md) for each pass's full procedure, escalation targets, and worked before/after examples.

**Step 4: Passes 5-7 RHYTHM, HUMANITY, COLOR**

Step 4.1: RHYTHM. Compute the sentence-length series. Fix low variance by splitting one long sentence and merging two short ones inside the same paragraph, never by inserting fragments. Merges are forbidden on any pair in the clarity split log. Check terminal emphasis: is the last word of each paragraph the most consequential one?

Step 4.2: HUMANITY. Named people, concrete nouns, agentless abstractions removed as sentence subjects. When the protagonist is a system, the fix is a named operator, a dated state, or a named constraint, never a personified system.

Step 4.3: COLOR. Every sensory or specific detail must carry information and must be traceable to the material. A detail you cannot source is deleted, not softened.

**Step 5: Passes 8-9 VOICE, then MECHANICS**

Step 5.1: VOICE. Check consistency against the register declared in Step 1.1. Flag drift; do not "add personality."

Step 5.2: MECHANICS. Grammar, usage, house style. This runs last of the nine and never before Voice.

**Step 6: Pass 10 SLOP AUDIT, then the run report**

Step 6.1: Invoke `slop-detector` for signature detection. It owns the signature list and the detection rules. Do not re-derive them here. That skill is still substacker-scoped: its flattened-uncertainty signature reads a `corpus/drafts/notes/` path, so skip that one signature when you run it as the general register pass.

Step 6.2: Apply this skill's constraint to the hedge-reduction step, which `slop-detector` does not carry. That step may reduce only rhetorical hedge stacks. It may never remove a hedge reflecting genuine evidential uncertainty, and it may never touch a List B word. "It seems like it might possibly be the case that latency rose" is three rhetorical hedges on one claim; reduce it. "The estimate may understate exposure under these assumptions" is two epistemic hedges, both load-bearing; leave both.

Step 6.3: Re-run MECHANICS on every line the slop pass changed, then produce the run report: claim ledger diff, escalation records, reporting gaps, cut percentage, rhythm diagnostics, and the config used.

Validate using [resources/evaluators/rubric_prose_force_and_rhythm.json](resources/evaluators/rubric_prose_force_and_rhythm.json). **Minimum standard**: Average score >= 3.5.

## The Ten Passes

| # | Pass | May edit | May NOT touch | Escalates to |
|---|------|----------|---------------|--------------|
| 1 | Structure | Paragraph order, section boundaries | Wording | Structural planner / human |
| 2 | Force | Verbs, subjects, voice | Claim strength, hedges | Reporting (missing actor) |
| 3 | Brevity | List A words, redundancy, sentence length | List B, propositions | Reporting (claim stated twice, evidence once) |
| 4 | Clarity | Sentence splits, missing referents | Terminology precision | Ladder of abstraction / reporting |
| 5 | Rhythm | Length variance, terminal emphasis, openers | Clarity split log pairs | Pass 4 |
| 6 | Humanity | Abstract subjects, named agents | Attribution of intent to systems | Reporting (who acted?) |
| 7 | Color | Sourced detail, decoration | Unsourced sensory detail (delete it) | Reporting |
| 8 | Voice | Register drift | Content | Step 1 config |
| 9 | Mechanics | Grammar, usage, style | Everything above | None |
| 10 | Slop audit | Machine-register signatures | Epistemic hedges, load-bearing claims | Reporting (specificity sweep) |

An **escalation record** has four fields: the defect, the class it actually belongs to, why this pass cannot fix it, and the target layer. Escalations are successful outputs, not failures. A run that produces zero escalations on a thin-material draft is a run that papered over the thinness.

## The Claim-Strength Invariant

The most important rule in this skill. Hart's force rules were tuned for reporting on events that happened. Applied to analytical claims they turn "was associated with" into "drove" and "suggests" into "shows."

**The ladder:** S5 asserted fact (dated, sourced) / S4 quantified finding with stated conditions / S3 association or co-occurrence / S2 inference or suggestion / S1 possibility or disputed.

**The rule:** record S-level before the rewrite, assert it after. Any rewrite that raises S-level is reverted, even when the stronger version is probably true. Only new evidence raises a claim, and an editing pass has none.

| Rewrite | Delta | Verdict |
|---|---|---|
| "The rollout was associated with a 12% drop in errors" to "The rollout drove errors down 12%" | S3 to S5 | REVERT |
| "The rollout was associated with a 12% drop in errors" to "Errors fell 12% after the rollout" | S3 to S3 | ACCEPT (expletive killed, strength held) |
| "The assay suggests the compound binds" to "The assay shows the compound binds" | S2 to S5 | REVERT |
| "Output declined 4% in Q3" to "Output collapsed in Q3" | S4 magnitude inflation | REVERT |
| "According to the 2019 filing, reserves fell" to "Reserves fell" | attribution deleted | REVERT |

Strength also moves silently through deletions: dropped attribution, dropped scope ("in this cohort"), dropped date ("as of Q2 2023"), and dropped units. Treat every deletion of those as a strength change.

**Anti-overcorrection:** the invariant is symmetric. Do not add hedges to sourced facts. "The plant appears to have possibly closed" when the closure is in the filing is also a violation.

**System variant:** when the actor is a market, a protocol, or a pipeline, the force pass must reach for a state-change verb, not an intention verb. "The auction cleared at $4.10" is force. "The auction chose $4.10" is an unfalsifiable causal claim distributed across the sentence. Systems have states, constraints, and incentives; only people have wants.

See [resources/claim-strength-ledger.md](resources/claim-strength-ledger.md) for the full ledger format, the verb-swap danger table, and worked examples from clinical, supply-chain, and market-history drafts.

## List A and List B

| List A: cut on sight | List B: protected, never auto-cut |
|---|---|
| rather, somewhat, generally, virtually, pretty, slightly, a bit, a little, quite, very, really, actually, basically, essentially, in order to, the fact that, it should be noted, it is important to note, needless to say | approximately, estimated, roughly, may, might, appears, suggests, is consistent with, in this sample, in this cohort, under these assumptions, as of [date], reported, alleged, preliminary |

**The scope exception.** A List A word doing scope work is not a parasite. "Retail sales generally recover within two quarters" is a base-rate claim; deleting "generally" produces a universal law. The fix is neither to keep the vague word nor to cut it, but to replace it with the scope from the material: "In seven of the nine postwar recessions, retail sales recovered within two quarters." If the material does not supply the scope, keep the word and log a reporting gap.

## Diagnostics, Not Objectives

Report these alongside the prose. Never optimize them directly.

| Metric | Default | If it fails | Forbidden fix |
|---|---|---|---|
| Sentence-length mean | 15-20 words, general readership | Investigate, do not chop | Splitting sentences to hit the number |
| Sentence-length SD | >= 7, or 60-70% of mean | Split one long, merge two short in the same paragraph | Inserting fragments or one-word sentences |
| Short-sentence presence | one under 8 words per 150 | Find a claim worth landing short | "It didn't." "Nobody knew." |
| Consecutive similar lengths | no 3 within +/-2 words | Vary clause structure | Padding a sentence |
| Brevity cut | 10-20% | Under 5% means the pass did not run; over 30% means diff the propositions | Cutting hedges to hit the target |
| Readability score | set per audience in config | Route to a concrete example at the bottom of the abstraction ladder | Swapping a precise term for a vaguer one |

All numeric thresholds above are operational defaults derived for mechanization. Hart publishes no such figures, and both Wordcraft and Storycraft are lending-restricted, so they could not be verified against the primary text. Ship them as tunable config with that provenance stated.

## Guardrails

**Requirements:**

1. **Separate invocations**: Each pass runs as its own step with its own output. If you find yourself editing verbs and commas in the same reading, you are not running this skill.
2. **Ledger before edits**: No FORCE pass begins before the claim ledger exists. In HIGH risk class this is a hard block.
3. **Passive stays when the actor is unknown**: "The alert was silenced at 02:14" stays passive and produces a reporting gap. Writing "An on-call engineer silenced the alert" invents an actor.
4. **Clarity split log is binding**: The rhythm pass may not merge any pair the clarity pass split.
5. **Attribution honesty**: Cite Hart, Wordcraft, or Storycraft. Do not cite "the Oregon Method" as a codified canon; it is a retrospective label for the Oregonian coaching practice Hart ran, not a system he branded. Do not attribute the SCAM acronym to Hart; it comes from journalism pedagogy at Dynamics of Writing.
6. **Report, do not silently apply**: Every claim-strength revert, escalation, and reporting gap appears in the run report.

**Common pitfalls:**
- Running all nine passes in one prompt, producing generic polish and no escalation signal.
- Strengthening a verb past the evidence because the stronger verb reads better.
- Deleting "approximately," "in this sample," or "as of Q3" during the brevity pass.
- Maximizing sentence-length variance with fragments, which reads as LinkedIn copy in an engineering or clinical register and destroys credibility faster than monotony did.
- Merging short sentences to raise the mean, reintroducing the subordination the clarity pass removed.
- Over-correcting the slop audit into a new uniformity: banned em dashes, sprinkled fragments, performed casualness. The cure for machine register is specificity and asymmetry, not affected roughness.
- Letting the humanity pass personify a market, model, or institution to satisfy "concrete agent."
- Fixing a middle-rung abstraction trap by swapping jargon for plainer jargon instead of supplying one particular from the material.

## Quick Reference

**Key resources:**
- **[resources/pass-playbook.md](resources/pass-playbook.md)**: Per-pass procedures for Passes 1-9, escalation targets, worked before/after examples across clinical, supply-chain, ML, incident, and market-history drafts. Its Pass 10 section predates the split; `slop-detector` now owns signature detection
- **[resources/claim-strength-ledger.md](resources/claim-strength-ledger.md)**: S1-S5 ladder, ledger format, verb-swap danger table, silent strength moves, List A/B rationale
- **[resources/rhythm-diagnostics.md](resources/rhythm-diagnostics.md)**: Burstiness, 2-3-1 end-stress, right-branching, terminal emphasis, pace modulation at complexity, number landing, transitions, tunable config block
- **[resources/evaluators/rubric_prose_force_and_rhythm.json](resources/evaluators/rubric_prose_force_and_rhythm.json)**: quality scoring

**Inputs required:**
- The draft, as text or a file
- Register, audience, and domain risk class
- The source material or citation set behind the draft (required to distinguish a reporting gap from a wording problem)

**Outputs produced:**
- The edited draft
- Claim ledger with before/after S-levels and every revert
- Escalation records (defect, class, target layer)
- Reporting-gap register
- Rhythm and brevity diagnostics, plus the config used and its provenance note

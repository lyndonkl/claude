---
name: narrative-form-triage
description: Decides which narrative form a body of researched material can actually support, before any structure is imposed. Runs a six-question form-triage gate producing STORY NARRATIVE, EXPLANATORY NARRATIVE, MULTI-NODE GATHERING, or DO NOT NARRATE; runs the ABT (And/But/Therefore) spine diagnostic; selects a spine from a thirteen-structure table covering Truby arc, layer cake, pyramid/SCQA, OCAR, PR/FAQ, sparkline, Raskin five-slot, martini glass, drill-down, inverted pyramid and braided/mosaic; and writes an immutable spine contract with a boredom budget. Use before outlining or drafting any long-form nonfiction, report, post-mortem, market history, research writeup or case study, or when user mentions find the narrative, what's the story here, narrative arc, story structure, how should I structure this, does this have a story, or storytelling with data.
---

# Narrative Form Triage

## Table of Contents
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [The Six-Question Form Triage](#the-six-question-form-triage)
- [Structure Selection Table](#structure-selection-table)
- [ABT Spine Diagnostic](#abt-spine-diagnostic)
- [Boredom Budget and Nesting Rules](#boredom-budget-and-nesting-rules)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

**Related skills:** Use `narrative-arc-mapping` for building the arc once this triage returns STORY NARRATIVE, `narrative-evidence-ledger` for the full evidence ledger the Step 1 chronology table is a subset of, `mcphee-structure-derivation` for deriving the shape inside a declared form. Use `narrative-opposition-web` for warranting an opponent once a story arc is available, `writing-structure-planner` for diagramming a chosen structure, `communication-storytelling` for audience adaptation after the spine is fixed.

**Boundary with `mcphee-structure-derivation`:** this skill decides the FORM — whether the material narrates at all, and as what — while `mcphee-structure-derivation` derives the SHAPE inside a form this skill has already declared.

## Core Principles

1. **Form before craft**: the form declaration precedes outlining, which precedes drafting, which precedes line work. A defect at any stage almost always originates in the stage before it, so triage failures cannot be repaired by better prose.
2. **The refusal is a deliverable**: "DO NOT NARRATE" and "no BUT in this material" are successful, complete outputs. Deliver them with the same confidence as an arc. An agent that cannot refuse will always build an arc.
3. **Every slot is a claim needing a warrant**: each triage answer and each structural slot cites specific corpus material or is recorded EMPTY. An empty slot means the form is wrong, not that you should search harder for something to put in it.
4. **One contradiction, written first**: the BUT is load-bearing. Write it before the AND. Two BUTs that will not collapse into one means two deliverables.
5. **Thesis or theme, decided explicitly**: a falsifiable proposition is a thesis and must be stated early and plainly. A value proposition is a theme and must never be stated, only enacted. Withholding a thesis is not sophistication; asserting a theme is not clarity.
6. **The spine contract is immutable within a draft**: switching structures because a section is hard produces documents that open as a story, become a pyramid and end as a pitch. Readers register that as dishonesty. Changing spine requires a logged restart.
7. **Anti-narrative reflex is also a bias**: refusing every arc over-attributes outcomes to luck and structure. Record the strongest agency-based reading you considered and why it lost.

## Workflow

Copy this checklist and track your progress:

```
Narrative Form Triage:
- [ ] Step 1: Build the evidence table (before any form talk)
- [ ] Step 2: Run the ABT spine diagnostic (BUT first)
- [ ] Step 3: Run the six-question form triage gate
- [ ] Step 4: Select the spine and the runner-up
- [ ] Step 5: Write and freeze the spine contract
```

**Step 1: Build the evidence table**

Step 1.1: Build a chronology table before writing a single word of form or theme: DATE | EVENT | ACTOR OR NODE | SOURCE | SOURCE IS PRIMARY-CONTEMPORANEOUS OR SECONDARY-RETROSPECTIVE | TYPE (pivotal / defining / neither). Pivotal means an external, dated, verifiable state change. Defining means a participant's model of the world was falsified.

Step 1.2: Do not let a theme or a thesis be proposed before this table is complete. Theme-first material bending is the commonest quiet failure: the abstraction gets written, then evidence is selected to confirm it.

Step 1.3: Flag rows whose only support is a secondary retrospective. Those sources already had the halo, the teleology and the genre applied upstream, and you will faithfully re-derive them while passing every check.

**Step 2: Run the ABT spine diagnostic**

Step 2.1: Fill BUT first, using only claims in the table, each with a citation. Then AND, then THEREFORE. See [ABT Spine Diagnostic](#abt-spine-diagnostic).

Step 2.2: Classify: zero contradictions (AAA), exactly one (ABT), two or more that will not collapse (DHY). AAA forbids all story structures. DHY requires a split or a disclosed set-aside.

Step 2.3: If you cannot fill BUT without importing a fact not in the corpus, output "NO BUT IN MATERIAL" and stop the story branch. This is a pass, not a failure.

**Step 3: Run the six-question form triage gate**

Step 3.1: Answer each of the six questions YES-with-citation or NO. An answer with no citation is a NO. See [The Six-Question Form Triage](#the-six-question-form-triage).

Step 3.2: Score to one of four forms. Record the failing question numbers alongside the form. The declaration binds every downstream pass.

Step 3.3: For any slot the chosen form requires and the evidence cannot fill, apply the Empty Slot Protocol in [resources/form-triage-gate.md](resources/form-triage-gate.md). Never fill by inference disclosed only in back matter; never fill by invention.

**Step 4: Select the spine and the runner-up**

Step 4.1: Key the [Structure Selection Table](#structure-selection-table) on five facts: contradiction count, person or system subject, obligated or voluntary audience, outcome already known or not, audience hostile or trusting.

Step 4.2: Name the runner-up structure and why it lost. The runner-up is the fallback when a section refuses to fit, and naming it in advance is what stops mid-draft shopping.

Step 4.3: If the subject is a system, apply the system remap in [resources/structure-catalog.md](resources/structure-catalog.md) before adopting any agentic template. Unmapped templates are how prose ends up attributing intent to markets, protocols and institutions.

**Step 5: Write and freeze the spine contract**

Step 5.1: Emit the full contract using the template in [resources/form-triage-gate.md](resources/form-triage-gate.md). Eleven fields are required:

```
1. Form declaration       5. Thesis-or-theme + its sentence   9. Set-aside log
2. Failing question nums  6. Boredom budget sentence         10. Rejected agency reading
3. ABT sentence, cited    7. Nesting declaration             11. Attribution note
4. Structure + runner-up  8. Empty-slot log
```

Step 5.2: Freeze it. Downstream passes may not add, remove or reframe claims, and may not change structure. A structural defect discovered later escalates back to a logged re-run of Step 3, never a quiet substitution.

**How to know if the triage is working:**

If working: the contract fits on one page, a reader can predict which sections the draft will contain, and at least some triage runs end in DO NOT NARRATE or a demoted form.

If not working: every corpus somehow turns out to contain a story, contracts are written after drafting, or the boredom-budget line is missing (which means no structure was actually chosen).

Validate using [resources/evaluators/rubric_narrative_form_triage.json](resources/evaluators/rubric_narrative_form_triage.json). **Minimum standard**: Average score >= 3.5.

## The Six-Question Form Triage

Answer each YES-with-citation or NO. No citation means NO. These mechanize the story-versus-explanatory distinction Jack Hart draws in *Storycraft* chapters 11 to 13; the six-question form and its scoring are a derived instrument, not a gate Hart publishes. Do not cite "the Oregon Method" as a codified canon — it is a retrospective label for a newsroom practice, not a named system.

| # | Question | Fails when |
|---|----------|-----------|
| 1 | Is there a single continuous entity, person or system, whose state is tracked start to finish? | The material is a set of independent findings |
| 2 | Does that entity want something specific and reachable, documented in the record? | Motive is inferred from outcome |
| 3 | Is there a dated, sourced rupture of the status quo? | The "inciting incident" is only visible in hindsight |
| 4 | Do you hold a continuous sourced action sequence, granular enough that at least three moments could be rendered as scenes? | You have conclusions, not events |
| 5 | Is there an evidenced point of insight, a moment the entity or its participants saw the world differently? | You can name it but nobody's behavior changed after it |
| 6 | Is there a resolution: a new stable state? | The situation is ongoing |

**Scoring:**
- YES to 1-6 → **STORY NARRATIVE**. Build the arc.
- YES to 1-4, NO to 5 and/or 6 → **EXPLANATORY NARRATIVE**. You have an action line and no transformation. Use the action line as a spine to hang explanation on. Do not manufacture a climax.
- YES to 1-2 only, or the action sequence is discontinuous → **MULTI-NODE GATHERING**. 3-5 nodes, all instantiating the same causal verb.
- NO to 4 → **DO NOT NARRATE**. Write analytical prose with narrative texture (a concrete opener, specific detail) and no arc. Say so explicitly in the plan.

Question 5 has a hard evidential test: a point of insight exists only if behavior demonstrably changed after it, with a source. Otherwise record "NO POINT OF INSIGHT" and downgrade the form. Promoting the largest number in the dataset or the most recent event into a turning point is the single most common way an honest analysis becomes a false dramatic claim.

## Structure Selection Table

Key on: contradiction count (AAA/ABT/DHY), subject (person or system), audience (obligated or voluntary), outcome (known or not), audience stance (trusting or hostile). Full slot lists, system remaps and worked examples across market history, ML writeups, incident review, supply chain, biography and policy live in [resources/structure-catalog.md](resources/structure-catalog.md).

| Structure | Select when | Boredom permitted | Refuse when |
|-----------|-------------|-------------------|-------------|
| **Truby / full story arc** | ABT + person subject + documented desire + warranted opponent + documented change of state + outcome unknown to audience | Nowhere; exposition must be blended | Any of the four evidence conditions is missing |
| **Explanatory narrative (layer cake)** | ABT + system subject + a followable action line + voluntary audience + dense material | Inside a digression a preceding scene paid for, up to that scene's length | No action line exists (a traveling unit that touches 4+ nodes) |
| **Pyramid / SCQA** | Obligated audience must decide; or AAA material; or outcome already known | Below the key line only | The governing thought is not falsifiable in one sentence |
| **OCAR / LDR** | Peer or technical audience, empirical claim, authority comes from method | In Action (methods, results); O, C and R must survive alone | Deleting the Action still leaves a finding — that means there was no Challenge |
| **PR/FAQ (working backwards)** | Obligated audience, subject does not exist yet, decision is go/no-go | Nowhere in the body; density exiled to appendices | No internal-FAQ answer materially weakens the proposal |
| **Duarte sparkline** | Audience must act and feel; a change is already underway they half-believe | Nowhere; any stretch without an oscillation is a leak | The "what is" beats are one problem in several costumes |
| **Raskin five-slot** | Audience must be repositioned; the audience is the protagonist; no human protagonist in the material | Nowhere before the evidence slot | The enemy slot can only be filled by a named party whose intent is undocumented |
| **Martini glass** | Reader must understand before exploring; a dataset, model or appendix is attached | After the handoff, at the reader's discretion | The stem lacks a stated thesis and stated limitations |
| **Drill-down** | Reader arrives with their own case and wants to find themselves in the data | Everywhere outside the entry frame | The reader could reach a wrong opposite conclusion unaided |
| **Inverted pyramid** | Reader may exit at any point without penalty; outcome already known | Increasingly, top to bottom | The material's value depends on accumulation |
| **Braided / mosaic (gathering)** | 3-5 nodes, no single spanning entity, all sharing one causal verb | At node boundaries only | Node 4 proves nothing node 1 did not — then it is a list, format it as one |
| **Chronicle** | Two or more major structural slots are empty and the record is genuinely thin | Throughout, by design | You are using it to avoid taking a position you have evidence for |
| **Taxonomy** | Independent findings, no causal chain, DHY that will not collapse | Within categories | You are hiding a real contradiction behind categories |

Cross-cutting overrides:
- **Outcome already known to the audience** (quarterly results, a published finding, a shipped incident): all suspense structures are wasted. Lead with the answer.
- **Hostile or low-trust audience**: use inductive grouping, which is failure-tolerant, and put evidence before conclusion. A deductive chain hands a hostile reader one link to break.
- **Independent findings with no causal chain**: an arc here fabricates causality. That is a correctness failure, not a style choice.

## ABT Spine Diagnostic

One sentence: `___ AND ___, BUT ___, THEREFORE ___.` Randy Olson's framework; the Narrative Spectrum bands (AAA / ABT / DHY) are his.

Procedure, in this order:
1. **BUT first.** Skip AND entirely on the first pass. Ask "why has this not already been solved?" — the answer is usually the real BUT.
2. **Check the causal level.** Is the contradiction the proximate harm or the condition that permits it? Test both; keep the level at which the THEREFORE is actionable.
3. **Then AND**, with two elements: an uncontested status quo, and what is at stake stated as a number or a named consequence, never "X is important."
4. **WHAT before HOW.** Good: "the fleet lost 40% of its capacity in eleven weeks, through three unrelated failures." Bad: "three unrelated failures across eleven weeks cost the fleet 40% of its capacity." Analytical writers default to the wrong order because they were trained to show method before result.
5. **Citation per slot.** A slot with no corpus citation is empty; the material is AAA.
6. **Truth check.** The ABT is a form test, not a truth test. Olson is explicit that the form is identical on either side of a true/false divide. A well-formed ABT makes a false claim more persuasive, so structural scoring must always be paired with a claim-to-citation audit.

**Worked contrast (post-mortem):** AAA — "The service scaled AND we added regions AND latency rose." No contradiction; this is a status report, route to inverted pyramid. ABT — "The service hit its latency target every month AND the team added three regions, BUT the target measured a p99 that excluded the retry path, where 80% of user-visible delay lived, THEREFORE redefine the target before adding capacity." One contradiction, cited, actionable.

## Boredom Budget and Nesting Rules

**Boredom budget.** Name the structure, then state in one sentence where it permits the reader to be bored. If you cannot, you have not chosen a structure — you have chosen a label. Per-structure rules are in the selection table above. Then mark every consecutive run of undramatized evidence longer than three paragraphs; each must sit in a permitted zone, or be moved to an appendix, compressed to claim-plus-citation, or paid for with a scene. Measure the distance from document start to the first statement of the governing thought: more than one screen of evidence before it means the budget has already failed.

**Nesting rules.** A story scene may nest inside an explanatory spine at any depth. An explanatory spine may nest inside a story at **one level only** — the nut graf. Deeper nesting is structure-shopping wearing a disguise.
- Every nested scene must be an instance of a specific claim stated within two paragraphs of it. If the scene could be swapped for a different scene without changing any claim, it is decoration; cut it.
- Attach each digression to the moment the reader feels the lack, not where the information is logically prior, and never before tension exists.
- The nut graf arrives before the reader decides whether to continue, states stakes and claim rather than scope, and never appears in a story narrative at all.
- Label every opening anecdote's position in the corpus distribution: median, tail or unique. Do not open with a tail case unless the piece is about the tail.

## Guardrails

**Requirements:**
1. **Citation per triage answer**: six questions, six answers, each YES carrying a specific corpus reference. Uncited YES is NO.
2. **Refusal outputs are first-class**: DO NOT NARRATE, NO BUT IN MATERIAL, and NO POINT OF INSIGHT are delivered as findings with reasons, never softened into a weaker arc.
3. **Empty slots change the form**: at most one inference-filled slot per piece, never at the climax, and its disclosure lives in the body within two sentences of the inference, in the same typographic register. Endnote-only disclosure is illegal.
4. **Opponent warrant before any antagonist**: competition, awareness and directed action, each documented. Two of three makes a rival, one or zero makes environmental pressure with no verbs of intent. For system subjects the slot takes a binding constraint, a regulatory regime, a physical limit or a countervailing incentive.
5. **Set-aside log**: when DHY material is reduced to one contradiction, name the contradictions dropped and why. Distinguish evidence that merely failed to support the spine from evidence that contradicted it; the second category is always surfaced to the reader.
6. **Immutable spine**: no structural change within a draft. Escalate for a logged restart.
7. **Attribution honesty**: cite Olson for ABT, Minto for the pyramid, Schimel for OCAR, Duarte for the sparkline, Raskin for the five slots, Segel and Heer for martini glass and drill-down, Hart for the story/explanatory distinction. Do not attribute the six-question instrument, the numeric thresholds, or "the Oregon Method" to Hart.

**Common pitfalls:**
- Declaring a form and then drifting back into arc language ("the crisis reached its climax") in a piece that has no climax.
- Choosing the opening anecdote for vividness, generalizing from it in the nut graf, and letting the body's evidence describe a different distribution.
- Anthropomorphizing the subject. Systems have states, constraints and incentives; only people have wants. "The market decided" smuggles in a causal claim the analysis has not established.
- Crowning a modest finding with universal significance. A piece is allowed to mean something small.
- Treating the tests as delete rules. They are label-and-disclose devices; an agent that gates on all of them ships chronicles, and chronicles inform nobody.
- Passing every per-sentence check while misrepresenting proportion through selection and emphasis alone. Word count against evidentiary weight is the expensive check and the one that matters.
- Producing a document that scans as rigorous because the headings are parallel. Run the read-through test: strip everything but the headlines and read them in sequence.

## Quick Reference

**Key resources:**
- **[resources/form-triage-gate.md](resources/form-triage-gate.md)**: six-question gate with worked runs, ABT development card, Empty Slot Protocol, refusal catalogue, spine contract template, thesis-vs-theme adjudication
- **[resources/structure-catalog.md](resources/structure-catalog.md)**: all thirteen structures with slot lists, system remaps, boredom rules, failure signatures and cross-domain worked examples
- **[resources/evaluators/rubric_narrative_form_triage.json](resources/evaluators/rubric_narrative_form_triage.json)**: quality scoring

**Inputs required:**
- The assembled corpus, with sources
- Audience: obligated or voluntary, trusting or hostile, and what they must do (decide, understand, act)
- Whether the outcome is already known to the audience
- Medium constraints: can the reader exit early, can the reader explore afterwards

**Outputs produced:**
- Chronology table with source-type flags
- Form declaration with failing question numbers
- ABT spine sentence with a citation per slot, or an explicit NO BUT IN MATERIAL
- Spine contract: structure, runner-up and why it lost, thesis-or-theme, boredom budget, nesting declaration
- Empty-slot log, set-aside log, rejected agency reading, attribution note

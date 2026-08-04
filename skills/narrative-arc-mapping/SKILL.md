---
name: narrative-arc-mapping
description: Maps researched evidence onto Truby's twenty-two structural steps without fabricating the steps the evidence cannot fill. Runs the designing-principle discrimination test, step-fit triage (PRESENT / ABSENT / NOT APPLICABLE), per-slot warrant cards, the empty-slot decision table, the moral-argument spine, and the revelation-intensity audit, then stops at a tagged scene weave. Use when architecting a long-form nonfiction piece from a research corpus, structuring a post-mortem, market history, biography, or science writeup, or when user mentions Truby, 22 steps, designing principle, moral argument, revelation sequence, scene weave, or step-fit triage.
---

# Narrative Arc Mapping

## Table of Contents
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [Step-Fit Triage](#step-fit-triage)
- [The Empty-Slot Decision Table](#the-empty-slot-decision-table)
- [Story-Movement Shapes](#story-movement-shapes)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

**Related skills:** Use `narrative-form-triage` FIRST — do not run this skill on material that has not been declared STORY NARRATIVE. Use `research-claim-map` to assemble the claim corpus. Use `deliberation-debate-red-teaming` to generate the rival arcs in Step 3. Use `narrative-opposition-web` for opponent warranting, which it owns. Use `scene-construction-scam` to build the scenes this skill's weave only tags. Use `causal-inference-root-cause` when the question is what caused the outcome. Use `writing-structure-planner` when triage says the material has no arc.

## Core Principles

1. **Structure is discovered, not imposed**: The material decides which steps exist. You run a triage against evidence, not a fill-in-the-blanks template.
2. **An empty slot is a finding**: "ABSENT — the record does not support this step" is a first-class, correct output. All twenty-two filled is the signature of fabrication.
3. **Narrative order is permitted; narrative causation is not**: You may reorder scenes for structure. You may never imply anyone knew something before the sources show they could have.
4. **Endpoint-first, contemporaneity-gated**: Derive the starting weakness backward from the known outcome, then require a source dated *before* the outcome that says the weakness was real. Backward derivation without that gate is hindsight determinism.
5. **Theme is enacted, never narrated**: The moral argument is carried by who wins and what they became to win. Explicit moral language is allowed in exactly three positions (see [resources/slot-warrants.md](resources/slot-warrants.md)).
6. **Intensity is course change, not adjectives**: A revelation's rating is the size of the change it forces in desire, motive, or plan. "Devastatingly" rates nothing.
7. **The macro layer stops at the scene weave**: One tagged line per scene plus construction fields. If you write a paragraph of prose, you have overrun your job.

## Workflow

Copy this checklist and track your progress:

```
Narrative Arc Mapping Progress:
- [ ] Step 1: Declare subject level, corpus, and selection rule
- [ ] Step 2: Derive endpoint-first, gate every weakness on a contemporaneous source
- [ ] Step 3: Find the designing principle (four gates) and the rival arcs
- [ ] Step 4: Triage all 22 steps; warrant every PRESENT slot
- [ ] Step 5: Resolve empty slots; choose movement shape
- [ ] Step 6: Build moral spine and revelation sequence; emit tagged scene weave; STOP
```

**Step 1: Declare subject level, corpus, and selection rule**

Step 1.1: State whether the protagonist is a PERSON, a NAMED ORGANIZATION, or a SYSTEM (a market, a protocol, an institution, a codebase, a supply chain). Hold it constant. Oscillating between "the standards committee" and "the protocol" is the first symptom of agency laundering.

Step 1.2: Tag every source: PRIMARY/CONTEMPORANEOUS or SECONDARY/RETROSPECTIVE, plus its interest (promotional, adversarial, regulatory, disinterested, unknown). A dated pre-outcome source is not automatically clean; trade press and analyst notes carry an in-progress halo. Never base a documented-mechanism claim on a purely secondary retrospective account.

Step 1.3: Write the corpus selection rule in one sentence: "This corpus consists of X that survived / were written about / left logs / are still listed." If you cannot state it, you do not know what your evidence is a sample of.

**Step 2: Derive endpoint-first**

Step 2.1: Write the terminal claim: "By the end, the reader understands that ____." Split it into PSYCHOLOGICAL self-revelation (what the subject learns about what it was doing to itself) and MORAL self-revelation (what it was doing to others). If only one exists, say so; do not manufacture the other.

Step 2.2: Invert each into a starting-state weakness. Then apply the **contemporaneity gate**: every claimed starting weakness needs a citation dated before the outcome that shows the deficiency was visible then. A weakness evidenced only by post-hoc commentary is confabulation and must be marked INFERRED.

Step 2.3: State NEED (internal, hidden, unrecognised at the start), PROBLEM (the concrete opening crisis, an outgrowth of the weakness), and DESIRE (external, visible). Desire test: name the specific moment at which a reader can tell whether the goal was reached. No nameable moment means it is not a desire.

Step 2.4: Run the confusion check. If need and desire use the same verb, you have collapsed them.

See [resources/slot-warrants.md](resources/slot-warrants.md) for the hindsight-determinism procedure and the system-protagonist translation table.

**Step 3: Find the designing principle**

Step 3.1: Write the premise line (one sentence: the event that starts it, the subject, the outcome). Then draft 4-6 one-line candidate designing principles, each starting with a process verb: trace, force, use, show, follow, invert, express.

Step 3.2: Run all four gates on each candidate. A candidate must pass all four. Gate 3 (IT CUTS) requires you to **name three specific claims in the corpus the principle excludes**. A principle that excludes nothing organises nothing.

Step 3.3: Generate at least three structurally distinct rival arcs before committing (tragedy / structure-decided / contingency / convergence). Rank by fewest inconsistencies with the corpus, not most consistencies. Name the runner-up and the evidence that would have favoured it in the delivered notes.

See [resources/designing-principle.md](resources/designing-principle.md) for the four gates, worked candidates across five domains, and the rival-arc matrix.

**Step 4: Triage all 22 steps**

Step 4.1: Run every one of the twenty-two steps against the material and record PRESENT (with source) / ABSENT (material does not support) / NOT APPLICABLE (this domain or shape does not use it). Emit the table; it ships with the deliverable.

Step 4.2: Check the MANDATORY SEVEN. Any ABSENT there is a stop-work condition, not a style choice.

Step 4.3: Fill a warrant card for every PRESENT slot, including the question "name two other events a narrator working toward a different ending would have chosen for this slot." If you cannot name two, you have not searched the corpus.

Step 4.4: Declare the START TYPE (community / running / slow). If slow, report the structural risk before proceeding.

See [resources/twenty-two-steps.md](resources/twenty-two-steps.md) for all 22 with functions, system variants, and triage defaults.

**Step 5: Resolve empty slots and choose the shape**

Step 5.1: For each ABSENT slot, pick a move from [The Empty-Slot Decision Table](#the-empty-slot-decision-table). Log the slot and the move chosen.

Step 5.2: Enforce the budget: at most ONE inference-filled slot in the whole piece, never at the climax or the thesis sentence. If two or more major slots are empty, Move 3 (change the architecture) is mandatory.

Step 5.3: Choose one dominant movement shape and at most one secondary. If not linear, every strand must carry all seven mandatory steps or be cut.

**Step 6: Moral spine, revelations, scene weave, stop**

Step 6.1: Build the moral-argument spine, mapping each element to evidence and leaving unsupported elements visibly EMPTY. If the material is value-neutral (a benchmark result, a pricing mechanism, a taxonomy), return "no moral argument available; this is an explanatory piece" and run the steps in explanatory mode.

Step 6.2: Extract every revelation onto its own line. Rate intensity 1-10 strictly by size of course change. Audit for monotonic climb and accelerating pace. Information that changes nothing is exposition; relabel it.

Step 6.3: Emit the scene weave: ONE line per scene, max 200 characters, tagged with step, strand, and reveal, plus the construction fields (whose desire / opposition / plan / endpoint / twist). Re-check every reorder against source dates. Then stop. Do not write prose.

Validate using [resources/evaluators/rubric_narrative_arc_mapping.json](resources/evaluators/rubric_narrative_arc_mapping.json). **Minimum standard**: average score >= 3.5.

## Step-Fit Triage

**The mandatory seven.** Truby: a story "must have no fewer than the seven steps, because that is the least number of steps in an organic story." ABSENT on any of these means the material does not have this shape.

| Mandatory step | Person variant | System variant |
|---|---|---|
| Weakness and need | The flaw ruining their situation | Structural fragility, dependency, or unexamined assumption |
| Desire | The visible goal pursued | The goal participants collectively and verifiably pursued |
| Opponent | Who wants the same thing | Competing faction or force pursuing the same goal by incompatible means |
| Plan | How they intend to get it | The dominant strategy, standard, or consensus approach |
| Battle | The decisive confrontation | The decisive contest: one vote, one quarter, one decision |
| Self-revelation | What they learn | What the system now knows, evidenced by an observed behaviour change |
| New equilibrium | The changed steady state | The changed steady state, explicitly higher or lower than the start |

**Commonly and legitimately ABSENT in analytical domains.** Expect these to be empty and do not patch them: ghost; fake-ally opponent; attack by ally; gate / gauntlet / visit to death; opponent's self-revelation; audience revelation. Truby calls the gate/gauntlet "the most moveable of the 22 steps," and practitioners note the fake-ally opponent is "not 100% essential to all stories."

**Middle-weight check.** Count steps before the plan versus after. A front-loaded outline reproduces exactly the sagging middle the extra fifteen steps exist to prevent.

## The Empty-Slot Decision Table

| Move | When | What it looks like |
|---|---|---|
| **1. DECLARE THE ABSENCE IN THE BODY** (default) | Any empty slot | "No source records what was decided in that room." / "The commit history is silent on why the timeout was set to 30 seconds." A named absence creates tension; it does not destroy it. |
| **2. DOWNGRADE AND SUBSTITUTE** | An adjacent event exists but was not treated as pivotal at the time | "The nearest thing to a turning point in the record is the March supplier audit, though nobody then treated it as one." |
| **3. CHANGE THE ARCHITECTURE** | Two or more major slots empty | Re-run rival arcs with shapes that do not need the missing slots: chronicle, braided comparison, taxonomy, single-question investigation. |

**Illegal moves:**
- Fill by inference and disclose only in an endnote, footnote, appendix, or methods block. Readers experience the body. Any inference occupying a structural slot must be disclosed **within two sentences of the inference, in the same typographic register as the surrounding prose**, and marked non-removable.
- Fill by invention of any kind: an invented ghost, an invented betrayal, a supplier who changed terms promoted to fake-ally opponent.

**Budget:** at most one inference-filled slot per piece, never at the climax. (This cap is a derived working default for research-narrative work, not a figure published by Truby or by any of the source disciplines.)

## Story-Movement Shapes

| Shape | Select when | Typical fit |
|---|---|---|
| Linear | One subject, one intense desire, causal explanation | Biography, single-incident post-mortem, one-firm case |
| Meandering | Desire exists but is not intense; broad territory; nobody is really fighting anyone | Landscape surveys, field reviews |
| Spiral | The same event or claim re-examined at deeper levels each pass | Forensic accounting, replication analyses, root-cause retrospectives |
| Branching | Paths splitting from central points, each a complete sub-world | Supply-chain tiers, protocol ecosystems, taxonomy explainers |
| Explosive | Simultaneity itself is the argument, rendered by deliberate crosscutting | Systemic crises only |

**Explosive is the cop-out shape.** Complex interconnected research invites the agent to declare simultaneity and thereby choose no shape at all, producing a piece where nothing builds. Explosive is the hardest form and requires crosscutting between named, seven-step-complete strands. **Default to linear or spiral** unless the designing principle genuinely demands otherwise, and write down why.

## Guardrails

**Requirements:**

1. **Absence is reportable**: The triage table must ship with the deliverable. At least one of the twenty-two steps reported ABSENT with a reason is the healthy signature; all twenty-two filled fails the output gate.
2. **Contemporaneity gate on every weakness**: A starting weakness with no pre-outcome citation is marked INFERRED and cannot occupy the climax or the thesis sentence.
3. **Opponent warrant before promotion**: Opponent slots are warranted by `narrative-opposition-web`; an unwarranted opponent may not be marked PRESENT.
4. **Agency audit on every abstraction**: Flag every intentional verb attached to a system. "The market realised," "the industry learned," "the protocol wanted." Rewrite each one to named actors, or cash it out into a collective mechanism (a vote, a standard, a price) in the same sentence.
5. **Date check on every reorder**: Structural reordering that implies anyone knew something before they could have is a defect regardless of how well it reads. Evidence overrides structure. Keep a reorder log with one line per departure from chronology.
6. **Explanatory mode is legitimate**: "No moral argument available" is a permitted and sometimes correct output. Forcing one on a benchmark, a pricing mechanism, or a taxonomy produces sanctimony and a manufactured villain.
7. **Justify from the material, not from film canon**: Do not cite Truby's stock examples (The Godfather, Casablanca, Tootsie) as justification for a structural choice. They import single-protagonist, decisive-battle, terminal-revelation assumptions that do not hold in most analytical domains.
8. **Consider the agency reading**: For each major outcome, state the strongest skill-and-intent explanation you considered and why you did or did not adopt it. Over-attributing to luck and structure is also a bias.
9. **Stop at the weave**: One tagged line per scene, 200 characters max. No paragraphs, no prose, no draft.

**Common pitfalls:**
- Filling all 22 slots because empty ones look like unfinished work. This is the single highest-frequency failure of this method.
- The retrofitted weakness: a starting deficiency that exists only to make the known ending look inevitable.
- The strawman opponent: assigning the role to whoever lost and backfilling stupidity. Bad craft and bad analysis at once.
- The decorative fourth corner: padding a real two-sided conflict with generic "regulators" and "users." Delete the corner; if no argument breaks, it was decoration.
- Two-part opposition sneaking back: corners C and D appear in the setup and vanish from the drive section.
- Manufactured escalation: inflating adjectives instead of sequencing genuinely larger findings.
- The moralizing narrator: building a correct moral spine and then also stating the lesson in prose.
- The flat drive: five quarters of declining margin or five failed experiments described identically. If you can swap any two drive actions without changing the argument, they are one beat.
- Multiple apparent defeats: there is exactly one, everything else is a setback.
- Turning every check into a delete rule. These are label-and-disclose devices. An agent that gates on all of them ships a chronicle, and a chronicle informs nobody.
- Epistemic apparatus crowding out the subject. If disclosures, hedges, and contingency nodes exceed roughly one per 250 words, the material is too thin for this architecture: change the architecture rather than spending more disclosure budget.

## Quick Reference

**Key resources:**
- **[resources/twenty-two-steps.md](resources/twenty-two-steps.md)**: all 22 steps with function, system variant, triage default, and the evidence each requires; start types; multistrand rule; scene-weave output spec
- **[resources/designing-principle.md](resources/designing-principle.md)**: the four discrimination gates, worked good/bad candidates across five domains, the rival-arc matrix, genre disclosure and suppression-set reinstatement
- **[resources/slot-warrants.md](resources/slot-warrants.md)**: the structural slot warrant card, hindsight-determinism procedure, moral-argument spine, revelation audit, agency audit, system translation table, GOOD/BAD output gate
- **[resources/evaluators/rubric_narrative_arc_mapping.json](resources/evaluators/rubric_narrative_arc_mapping.json)**: quality scoring

**Inputs required:**
- **Precondition (hard):** a frozen spine contract from `narrative-form-triage` declaring the form STORY NARRATIVE. Any other declaration — EXPLANATORY NARRATIVE, MULTI-NODE GATHERING, DO NOT NARRATE — means this skill does not run. No contract means run the triage first, not this.
- A research corpus with dated, attributable sources
- The known outcome or finding (the endpoint already exists in researched material)
- Target length (sets the reveal count and step-count target)

**Outputs produced:**
- Subject-level declaration and source ledger (primary/secondary, interest tag, selection rule)
- Endpoint-first derivation with contemporaneity gate results
- One designing principle plus the three claims it excludes, and the named runner-up arc
- The 22-step triage table: PRESENT (source) / ABSENT (reason) / NOT APPLICABLE
- Warrant card per PRESENT slot; empty-slot log with the move chosen for each
- Moral-argument spine with visible EMPTY elements, or an explanatory-mode declaration
- Revelation sequence with intensity ratings justified by course change
- Tagged scene weave, one line per scene, and nothing beyond it

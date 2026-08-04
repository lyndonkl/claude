---
name: narrative-evidence-ledger
description: Builds the evidence ledger that narrative work is allowed to be built on, before any structure is chosen. Locks the frame (unit, denominator, window, population boundary), atomizes material into findings with evidence classes A-F and re-findable pointers, triages every causal claim L1 MECHANISM to L5 CONJECTURE with permitted and banned verb sets, runs one-way promotion from finding to claim to beat, and keeps a DEAD column of everything a veto killed. Use before outlining or drafting any evidence-based narrative, when auditing whether a draft's claims are actually sourced, when a piece needs a provenance layer for handoff, or when user mentions evidence ledger, claim ledger, provenance, sourcing, causal grading, denominator lock, cherry-picking, or circular citation.
---

# Narrative Evidence Ledger

## Table of Contents
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [The Ledger Columns](#the-ledger-columns)
- [Evidence Classes and Attribution Grammar](#evidence-classes-and-attribution-grammar)
- [Causal Claim Triage](#causal-claim-triage)
- [Mechanical Integrity Checks](#mechanical-integrity-checks)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

**Related skills:** Use `claim-extractor` to harvest raw assertions from a corpus before entering them here, `research-claim-map` for mapping claim-to-source webs, `narrative-opposition-web` for opponent warranting once the ledger exists, `causal-inference-root-cause` when a causal link needs actual analysis rather than grading. Three siblings consume what this skill defines: `narrative-fidelity-audit` is the pre-ship gate and imports this ledger rather than rebuilding it, `narrative-fallacy-guard` uses the L1-L5 causal grades defined here, `numbers-in-narrative` imports the frame lock built here.

**This skill owns** the A-F evidence classes, the L1-L5 causal ladder, the pointer schema, the circular-citation check, and the frame lock; siblings cite these definitions rather than restating them.

## Core Principles

1. **Provenance, not verification**: This skill tracks where a claim came from. It never establishes that a claim is true. The permitted verbs are "sourced", "class-tagged", "re-derivable". The banned verbs are "verified", "fact-checked", "confirmed", "validated". An output claiming verification is a defect, not a flourish.
2. **Ledger before architecture**: Any structure chosen before the ledger exists will generate demand for material, and unfilled demand gets filled by invention. Build order is frame lock -> findings -> claims -> beats. Never the reverse.
3. **The pointer must resolve outside the pipeline**: A pointer into your own summary, notes, or a prior draft is a hard failure, not a weak citation. Only external artefacts count.
4. **Nothing is deleted, only killed**: Findings that a veto killed move to DEAD with the veto that killed them. The DEAD column ships with the deliverable. It is the only defence against a cherry-picking charge.
5. **The verb carries the evidence grade**: Causal language is typed. A claim graded L3 SEQUENCE may not later acquire the verb of an L1 MECHANISM claim without re-grading. Silent upgrades are the most common corruption.
6. **These are label devices, not delete rules**: A ledger that gates on every test ships a chronicle, and a chronicle informs nobody. Most checks here terminate in a disclosure or a downgrade, not a deletion.
7. **A clean ledger is not a true piece**: Every per-claim check can pass while the assembled work misrepresents drift and proportion through selection alone. The omission set and proportion check are the expensive parts and they are the ones that matter.

## Workflow

Copy this checklist and track your progress:

```
Evidence Ledger Progress:
- [ ] Step 1: Lock the frame (unit, denominator, window, boundary)
- [ ] Step 2: Atomize material into findings with class + pointer
- [ ] Step 3: Triage every causal link and assign permitted verbs
- [ ] Step 4: Promote findings -> claims -> beats, one way
- [ ] Step 5: Run the mechanical integrity checks
- [ ] Step 6: Emit the handoff artefact and the gate verdict
```

**Step 1: Lock the frame**

Step 1.1: Write four lines before touching any material. UNIT: what is one row or one case? DENOMINATOR: per what? WINDOW: from when to when, and what justifies each edge? BOUNDARY: which entities are in the population, and who drew that line, you or the source?

Step 1.2: For each of the four, name one alternative you rejected and give a one-sentence reason. This is the anti-cherry-picking record and it is not optional.

Step 1.3: Record the starting hypothesis verbatim, dated, before you look. You will diff against it in Step 6.

See [resources/frame-lock.md](resources/frame-lock.md) for the rate-vs-count rule, denominator-drift detection, the instrument check, and worked frame locks from three domains.

**Step 2: Atomize material into findings**

Step 2.1: Decompose the material into atomic findings, one verifiable assertion each, with an ID. A finding has no addressee and no interpretation.

Step 2.2: Tag each with an EVIDENCE CLASS (A-F), a POINTER granular enough to re-find it, CONTESTED or UNCONTESTED, SOURCE INTEREST (who benefits from this account), and SOURCE VINTAGE (contemporaneous or retrospective, primary or secondary).

Step 2.3: Kill nothing yet. Findings that fail a veto later go to DEAD with the veto named.

See [resources/evidence-classes.md](resources/evidence-classes.md) for the class definitions, the pointer granularity test, and the register-porting table.

**Step 3: Triage every causal link**

Step 3.1: Extract every sentence or planned link containing a causal connective, plus every juxtaposition a reader would read causally. Scan headings, captions, section breaks and chart titles, not only body sentences.

Step 3.2: Assign exactly one grade: L1 MECHANISM, L2 CORRELATION, L3 SEQUENCE, L4 ADJACENCY, L5 CONJECTURE. Record the permitted verb set with the grade.

Step 3.3: For every L1, name the artefact that documents the LINK, not the two endpoints. If the only source is a retrospective secondary account, downgrade to L3 or L5.

See [resources/causal-triage.md](resources/causal-triage.md) for the full verb tables, the back-reference check, and system-intentionality grammar.

**Step 4: Promote, one way**

Step 4.1: FINDING -> CLAIM requires three things in writing: the interpretive leap, the population it generalises to, and what evidence would falsify it. A claim with no falsifier is not a claim; send it back.

Step 4.2: CLAIM -> BEAT requires two things: the prior belief it overturns, phrased as a sentence someone actually held, and the relation joining it to the preceding beat. A claim that changes nothing in the reader's model is supporting evidence, not a beat.

Step 4.3: Promotion is one-way per pass. Nothing may be promoted and then demoted inside a single revision, or the ledger stops tracking anything. Demotion is a logged event in the next pass, with a reason.

See [resources/ledger-schema.md](resources/ledger-schema.md) for the field-by-field schema, the ratio check, and DEAD-column conventions.

**Step 5: Run the mechanical integrity checks**

Step 5.1: Run all six checks in [Mechanical Integrity Checks](#mechanical-integrity-checks). Each returns pass or a defect list. Do not fix while checking; fixing and checking are separate passes.

Step 5.2: Sample 10% of findings at random and re-derive each from its pointer alone, with the draft hidden. If the pointer does not independently yield the finding, the class tag is wrong.

Step 5.3: Assemble the OMISSION SET: every corpus item that appears nowhere in the ledger. For each, write why. Any item that would weaken the emerging spine and lacks a written reason is a cherry-pick and must be reinstated.

**Step 6: Emit the handoff artefact and the gate verdict**

Step 6.1: Emit the ledger with all four columns, the frame lock, the causal grade map, the omission set, and the integrity check results.

Step 6.2: Diff the current reading against the Step 1.3 starting hypothesis and write what changed. If nothing changed, either you were unusually right or you did not look.

Step 6.3: State the gate verdict explicitly, including the required line: "This ledger records provenance. No claim in it has been verified. Human verification status: none."

Validate using [resources/evaluators/rubric_narrative_evidence_ledger.json](resources/evaluators/rubric_narrative_evidence_ledger.json). **Minimum standard**: Average score >= 3.5.

## The Ledger Columns

| Column | Definition | Entry requires |
|--------|------------|----------------|
| FINDING | A typed fact, checkable against a source. No addressee, no interpretation. | Class, pointer, contested flag, source interest, source vintage |
| CLAIM | A finding plus an interpretive commitment that can be wrong even if the finding is right. | The leap, the population, the falsifier |
| BEAT | A claim plus a change in the reader's model of the world. | The prior belief overturned, the relation to the previous beat |
| DEAD | Anything a veto, an instrument check, or a test killed. Never deleted. | The killer, the date, and DID-NOT-SUPPORT vs CONTRADICTED |

**Referential integrity**: every beat cites >= 1 claim; every claim cites >= 1 finding; every finding cites an external data location (table and row range, document and page, commit hash, transcript timestamp).

**Ratio check**: beats > claims means you are narrating without arguing. Findings vastly exceeding claims means you are reporting without interpreting. Claims exceeding findings means you are asserting.

**DEAD entries are typed.** "Did not support" (the evidence was too thin, the denominator was indefensible, the transform flipped it) is not the same as "CONTRADICTED" (a source establishes the opposite). Conflating them lets a contradicted claim re-enter later as merely unproven.

## Evidence Classes and Attribution Grammar

| Class | What it is | Default attribution level |
|-------|-----------|---------------------------|
| A | Primary artefact: filing, contract, dataset, log, transcript, commit, instrument reading | L0 if uncontested and covered by a methods note; L1 if consequential |
| B | First-person testimony about own experience | L2 epistemic verb; L3 if self-serving or contested |
| C | Second-hand testimony about someone else's experience | L3 mandatory, plus explicit distance |
| D | Secondary reporting: another account of the events | L3 mandatory, plus a flag that the underlying source was not obtained. Never L0 or L1 |
| E | Analyst or agent inference | L5-adjacent marking. Never presented as a finding |
| F | Unsourced | Cannot enter the ledger. Delete, or convert to an open research question |

Attribution levels: **L0** unmarked assertion. **L1** embedded source ("the postmortem timestamps the first alert at 02:14") - this is the workhorse and costs almost no rhythm. **L2** epistemic verb (recalled, estimated, projected). **L3** explicit attribution ("according to X"). **L4** contest marker, both values in one sentence, mandatory for every CONTESTED finding. **L5** uncertainty declaration ("the record does not establish"). **L6** methods block absorbing routine load.

**Bad** (supply-chain domain, class D wearing L0 grammar): "Congestion forced carriers to reroute through Vancouver in early 2021."
**Good**: "Carrier filings put Vancouver call volume up 34% between January and April 2021 [F-112, class A]. Two operators cited congestion in their rerouting notices [F-118, class A]; the record does not establish why the others moved [L5]."

**Budget rule (derived default, not a published figure)**: if more than roughly one sentence in four in a passage sits at L3 or above, the passage is under-reported, not over-attributed. Fix by reporting, never by deleting attributions.

**Register porting**: technical, financial and scientific registers have no "sources said" convention. Port the FUNCTION (evidentiary status visible in the sentence) into that register's own forms - inline figures with units and dates, footnote markers, named instruments, commit references. Do not import journalism's surface grammar, and do not drop the requirement because the target register lacks it.

## Causal Claim Triage

| Grade | Established | Permitted verbs | Banned |
|-------|-------------|-----------------|--------|
| L1 MECHANISM | The linking step itself is documented: memo, contract, physical process, accounting identity, code path, executed decision | caused, forced, triggered, led to, because, resulted in | - |
| L2 CORRELATION | Quantitative co-movement documented, mechanism absent | moved with, tracked, accompanied, coincided with | because, drove, forced |
| L3 SEQUENCE | Only temporal order established, both dates known | then, afterwards, in the following quarter, subsequently | every causal connective |
| L4 ADJACENCY | Co-present in time or space, no link established | (separate them in the text) or an inline disclaimer: "the two were concurrent; no link is documented" | any verb joining them |
| L5 CONJECTURE | The analyst's inference, no source | must carry an inference marker: "the most plausible reading is", "no source says why, but" | may never occupy a thesis, climax, or revelation slot |

**L1 requires a source for the LINK.** Two sourced endpoints plus a plausible story is L3. A retrospective secondary account that *asserts* a mechanism does not *document* one; it cannot support an L1 tag.

**Bad** (ML writeup): "Adding the auxiliary loss drove the 3.1-point accuracy gain."
**Good**: "Accuracy rose 3.1 points in the run that added the auxiliary loss [F-44]. Three other changes shipped in the same commit [F-45..47]; no ablation isolates the loss. L3."

**Back-reference check (the anti-upgrade guard)**: causal verbs are protected tokens carrying their grade. Any later edit that changes a causal verb must re-cite the grade in the same edit. Re-run the check after every revision pass by re-extracting the verbs and diffing against the grade map. Verb creep is silent: grades are assigned honestly at ledger time, then a line-edit turns "then" into "which forced" and the grade map no longer describes the text.

**System protagonists**: substitute INTENTIONALITY for interiority. A market, protocol, institution or codebase has no mind, so "the market realized", "the industry decided", "the protocol wanted" is either shorthand the reader will misread as agency or an unsourced claim about collective intent. Ground the system's want in one of three, and label which: documented incentives, stated strategy in a filing or roadmap or minutes, or revealed preference in prices, allocations, or spend.

## Mechanical Integrity Checks

Run all six. Each is checkable by pattern, not by judgment.

1. **Circular citation**: every pointer must resolve to an artefact outside this pipeline. Any pointer resolving into your own summaries, notes, prior drafts, or another agent's output is a HARD FAILURE. Invisible to reading; must be checked mechanically.
2. **Class F sweep**: zero findings may sit at class F when the ledger is handed off.
3. **Pointer granularity**: "the 10-K" fails; "FY2023 Form 10-K, p.47, Risk Factors" passes. "The logs" fails; "app-server.log, 2024-03-11 02:14:07Z" passes.
4. **Grade-verb match**: re-extract every causal verb and confirm it sits inside its grade's permitted set.
5. **Instrument check on every discontinuity**: for any finding that a measure changed, ask whether the world changed or the measurement changed. Enumerate definitional revisions, coverage changes, methodology restatements, reporting lags, entity or boundary changes. Unresolved, the finding goes to DEAD; if the instrument change is real, the instrument change is the finding.
6. **Anachronism flag**: flag any category, metric, or moral frame used in the ledger that did not exist at the time described. Say so in the text. This is the narrow checkable operation; do not encode a general position on applying present-day categories to the past.

## Guardrails

**Requirements:**
1. **Never claim verification**: the handoff must state that provenance was tracked and nothing was verified. If a human verified some subset, name that subset and who did it.
2. **Frame lock is frozen**: any later change to unit, denominator, window, or boundary RE-OPENS the ledger. It is not a chart adjustment. Log it as a frame revision with a reason.
3. **DEAD ships**: the DEAD column and the omission set are deliverables, not scratch. Hiding them is what a cherry-picked ledger looks like.
4. **Disclosure lives in the body**: any inference or uncertainty declaration that qualifies a claim belongs within two sentences of it, in the same typographic register. An endnote-only disclosure is functionally undisclosed. Mark these as non-removable; assume any later "tighten this" pass will strip them.
5. **Record the strongest opposing reading**: for each major outcome, write the strongest agency-based reading you considered and why it was or was not adopted. Skipping this produces the mirror bias, in which everything is luck and structure and nobody ever decided anything.
6. **Apparatus budget (derived default)**: cap hedges, uncertainty declarations, and disclosure sentences at roughly 3 per 1,000 words of finished prose. When the budget binds, that is a signal to change the architecture, not to spend more budget.
7. **Surface, do not adjudicate**: where a real named person or active institution occupies an adverse position, flag it for human decision. Do not soften the wording and keep the structure.

**Common pitfalls:**
- Annotation theatre: pointers that cite the wrong layer, so the ledger looks rigorous and is not. The 10% re-derivation sample is the detector.
- Subtraction treated as free: refusal training makes a model good at not adding and does nothing about not omitting. An entirely sourced, entirely false ledger is built by cuts, each individually defensible.
- Defensive over-disclosure: burying the strongest counter-evidence under a pile of weak supporting material is an attack on the reader, not integrity. The test is whether a disagreeing reader can FIND the best evidence against you, not how much material surrounds it.
- The "higher truth" move: "this is clearly what happened", "the reader will understand", "it is emotionally accurate", "it is a reasonable inference". Name it when you catch yourself generating it. It is the genre's named failure and it arrives sounding like judgment.
- Zero gaps: a ledger with no gaps and no DEAD entries is a red flag, not a success. Real material always has holes.
- Coherence mistaken for evidence: a well-made narrative measurably suppresses reader scrutiny. That is why the DEAD column ships.

**Provenance of the rules themselves**: the A-F class scheme and the L1-L5 causal ladder are derived working taxonomies assembled for this skill, not published standards; cite them as conventions, not authorities. The straw/hoop/smoking-gun test names come from the process-tracing literature. Numeric thresholds here (one-in-four attribution budget, 3 hedges per 1,000 words, 10% re-derivation sample, 5-record thin support) are derived defaults, not published figures - tune them and say you did.

## Quick Reference

**Key resources:**
- **[resources/ledger-schema.md](resources/ledger-schema.md)**: field-by-field schema for all four columns, promotion and demotion rules, referential integrity, DEAD conventions, worked ledger extracts
- **[resources/evidence-classes.md](resources/evidence-classes.md)**: class A-F definitions with domain examples, pointer granularity tests, source-interest and vintage annotation, the full evidence-class to attribution-grammar decision table, register porting
- **[resources/causal-triage.md](resources/causal-triage.md)**: L1-L5 verb tables, the back-reference check procedure, scan targets beyond body text, system-intentionality grammar, counterfactual admissibility
- **[resources/frame-lock.md](resources/frame-lock.md)**: unit/denominator/window/boundary procedure, rejected-alternative record, denominator drift, the instrument check, the seven metamorphic transforms
- **[resources/evaluators/rubric_narrative_evidence_ledger.json](resources/evaluators/rubric_narrative_evidence_ledger.json)**: quality scoring

**Inputs required:**
- The research corpus, with source artefacts reachable (not summaries of them)
- The intended protagonist, if known: a person, or a system such as a market, protocol, institution, codebase, or supply chain
- The starting hypothesis, written down and dated before analysis

**Outputs produced:**
- Frame lock: unit, denominator, window, boundary, each with one rejected alternative and reason
- Four-column ledger with referential integrity satisfied
- Causal grade map: every link graded L1-L5 with its permitted verb set
- DEAD column, typed DID-NOT-SUPPORT vs CONTRADICTED
- Omission set with a written reason per omitted corpus item
- Integrity check results, including the circular-citation verdict
- Hypothesis diff and the explicit no-verification statement

---
name: narrative-fidelity-audit
description: Runs the hard gate on invention in fact-based narrative — a bright-line refusal sweep, an interior-state provenance ladder ([A] said-so / [B] contemporaneous document / [C] behavioural inference / [D] unsourced, where any [D] blocks publication), an LLM-specific fabrication red-flag scan, a three-altitude "How do you know?" prosecution at sentence, paragraph and passage level, a subtraction-log set review, and a note on sources generated from the deviation log. Use before shipping any narrative built on real evidence — market history, incident post-mortem, biography, ML writeup, supply-chain reconstruction, science writing — or when the user mentions fact-check, fidelity audit, fabrication check, invented detail, sourcing pass, did I make this up, composite scene, note on sources, or is this defensible.
---

# Narrative Fidelity Audit

## Table of Contents
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [The Bright Lines](#the-bright-lines)
- [The Interiority Provenance Ladder](#the-interiority-provenance-ladder)
- [The Three Altitudes](#the-three-altitudes)
- [Gate Verdict](#gate-verdict)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

**Related skills:** Use `narrative-evidence-ledger` to build the source ledger this gate imports. It owns pointers, evidence classes, the circular-citation check and register porting at build time. Use `narrative-fallacy-guard` for passage-level proportion and omission, `numbers-in-narrative` for quantitative fidelity, `scene-construction-scam` for a candidate scene *before* drafting where this skill audits a finished draft. Use `writing-structure-planner` for architecture before drafting, `claim-extractor` and `citation-form-check` for harvesting and formatting claims, `scout-mindset-bias-check` for motivated reasoning in the analysis, `writing-pre-publish-checklist` for non-fidelity final checks.

## Core Principles

1. **The agent sources, it does not verify**: You cannot confirm a fact. You can only record where a claim came from and how far the prose sits from it. Any output saying "fact-checked", "verified", or "confirmed" is false and turns this apparatus into a trust-laundering machine. The permitted verb is **sourced**.
2. **Do not add; do not deceive**: Roy Peter Clark's two axioms. Nonfiction may legitimately distort by subtraction (selecting, cropping, condensing). It becomes fiction the moment anything enters the text that was not in the record.
3. **Vividness is not the signal; a missing pointer is**: The scan keys on claims with no source pointer, never on how good a sentence sounds. A well-sourced vivid detail survives untouched no matter how beautiful.
4. **Subtraction is the unguarded flank**: Refusal training makes you good at not adding and does nothing about not omitting. A fully sourced, entirely false piece is produced by cutting the disconfirming quarter, the failed pilot, the dissenting engineer — each cut individually defensible.
5. **Sentence-local checking is what you do well and will default to**: Every documented case of a fully-checked-but-false narrative failed at the paragraph or passage level — ordering, adjacency, proportion, omission.
6. **These are label-and-disclose devices, not delete rules**: An audit that strips every claim it cannot make bulletproof ships a chronicle. Chronicles inform nobody, which is its own accuracy failure.
7. **Disclosure is not a currency**: A note on sources describes an already-honest method. It never purchases a deviation.

## Workflow

Copy this checklist and track your progress:

```
Narrative Fidelity Audit:
- [ ] Step 1: Establish the audit basis and the vocabulary contract
- [ ] Step 2: Bright-line refusal sweep
- [ ] Step 3: Interiority provenance tagging + over-hedging counter-check
- [ ] Step 4: Fabrication red-flag scan
- [ ] Step 5: Three-altitude "How do you know?" pass
- [ ] Step 6: Subtraction-set review and note on sources
```

**Step 1: Establish the audit basis and the vocabulary contract**

**Precondition: this gate imports the ledger, it does not rebuild it.** Pointer granularity, the circular-citation check, source interest and vintage annotation, and register porting are build-time procedures owned by `narrative-evidence-ledger`. If no ledger exists, or its integrity checks were never run, stop and run that skill first — auditing prose against nothing is not an audit.

Step 1.1: Import the source ledger and confirm it carries, per claim, a pointer, an evidence class, source interest and vintage, and a clean circular-citation verdict. Any of those missing is a RETURN TO RESEARCH, not something to reconstruct here.

Step 1.2: Write the vocabulary contract into your own output header: this pass **sources**; it does not verify.

**Step 2: Bright-line refusal sweep**

Step 2.1: Read [The Bright Lines](#the-bright-lines) below. Sweep the draft for each one and record every breach with a line reference.

Step 2.2: For every breach, apply the disposition table in [resources/bright-lines.md](resources/bright-lines.md): DELETE, DOWNGRADE (rewrite to the evidence level actually held), DECLARE (write the absence into the body), or RESEARCH (emit a specific answerable request). There is no fifth disposition. "Draft it and flag it for review" is not a disposition — flagged drafted text survives review at high rates because it reads well and the reviewer is checking, not rewriting.

Step 2.3: Watch for the **higher-truth rationalization** as you go. It will be generated internally, it will arrive sounding like good judgment, and it is the named failure of the entire genre. See [resources/bright-lines.md](resources/bright-lines.md#the-higher-truth-rationalization) for the phrase catalogue.

**Step 3: Interiority provenance tagging + over-hedging counter-check**

Step 3.1: Find every sentence attributing a thought, feeling, belief, motive, worry, intention, or realization to a real person — and every sentence attributing intent to a system ("the market realized", "Intel decided", "the protocol wanted", "the codebase assumed"). Tag each [A], [B], [C], or [D] using [The Interiority Provenance Ladder](#the-interiority-provenance-ladder).

Step 3.2: **A nonzero [D] count blocks publication.** Report the count as a number. Each [D] is deleted, converted to observable behaviour, or converted to attributed speech.

Step 3.3: **Anti-overcorrection, mandatory.** Re-read every [A] and [B] sentence and verify it is *not* hedged. Say he wrote in an email that night that the number was wrong. Then "he wrote that night that the number was wrong" is correct. "He appears to have possibly thought the number may have been wrong" is a fidelity defect in the other direction. Hedging sourced thought destroys close third person and reads as evasive. A human reviewer facing hedge-saturated prose strips hedges wholesale rather than surgically, losing the true ones with the defensive ones.

Step 3.4: If more than roughly a quarter of sentences in a passage carry explicit attribution or hedging, the diagnosis is **under-reporting, not over-caution**. Send that passage back to research. Do not fix it by deleting attributions. (The one-in-four figure is a working default for calibration, not a published standard.)

**Step 4: Fabrication red-flag scan**

Step 4.1: Run the twelve LLM-specific signatures in [resources/audit-passes.md](resources/audit-passes.md#fabrication-red-flag-scan). Every hit is guilty until it produces a pointer.

Step 4.2: The five highest-yield signatures, because they trip no ordinary fact-check:
- A **quotation that lands the theme too cleanly**, or is too well-formed for speech (no disfluency, no hedge, no irrelevance).
- A **transition asserting a state change**: "by then it was clear", "the mood had shifted", "the team, now convinced". These carry no proper nouns and no numbers, so nothing catches them.
- An **ending that rhymes with the opening**, or three examples forming a suspiciously clean progression.
- A **causal verb sitting exactly at the seam** between two sourced facts: "led to", "forced", "triggered", "which is why".
- **Detail so good you would have led with it, and did not** — because it arrived in drafting rather than in reporting.

Step 4.3: Key every judgment on the missing pointer, never on the vividness. Stripping genuinely reported detail alongside the fabrications is how writers learn to switch this scan off.

**Step 5: Three-altitude "How do you know?" pass**

Step 5.1: Run the sentence-level, paragraph-level, and passage-level question sets in [The Three Altitudes](#the-three-altitudes). Run them as an adversarial pass: you have the ledger and the draft, not the draft's rationale.

Step 5.2: Output a **defect list, not a rewrite**. Fixing and checking must be separate acts.

Step 5.3: **If the pass returns zero paragraph- or passage-level defects across a long piece, the pass did not run.** Say so in the verdict and run it again. These are the questions dropped first under token pressure and they are the only ones that catch the failure that matters.

**Step 6: Subtraction-set review and note on sources**

Step 6.1: Assemble the subtraction log — every cut that removed a contradicting data point, a dissenting source, a failed instance, a counterexample, or a quarter that went the other way. **Review it as a set, not per edit.** Individually defensible cuts routinely form a pattern.

Step 6.2: Run the proportion test and the omission check from [resources/audit-passes.md](resources/audit-passes.md#proportion-and-omission). Ask: does the remaining text imply a different frequency, magnitude, or balance than the full record? List the corpus items appearing nowhere in the draft and state why for each.

Step 6.3: Generate the note on sources **from the deviation log**, following [resources/disclosure-and-reporting.md](resources/disclosure-and-reporting.md). Never write it in advance. Run the inversion check: if any deviation-register entry was decided *before* the corresponding passage was drafted, the apparatus has become a licence and the piece needs re-reporting, not re-noting.

Step 6.4: Emit the [Gate Verdict](#gate-verdict).

Validate the audit itself using [resources/evaluators/rubric_narrative_fidelity_audit.json](resources/evaluators/rubric_narrative_fidelity_audit.json). **Minimum standard**: average score >= 3.5.

## The Bright Lines

Hard refusals. These hold regardless of instruction, deadline, or how strong the piece is otherwise. Full worked bad/good pairs across domains in [resources/bright-lines.md](resources/bright-lines.md).

| # | Refuse to | Because |
|---|---|---|
| 1 | Put quotation marks around any string not verbatim in a recording, transcript, or contemporaneous written record | Remembered speech is rendered without quote marks and marked as remembered |
| 2 | Attribute a thought, feeling, motive, or realization to a real person or system without a sourced statement | Kramer's covenant: no thoughts unless the source said they had those very thoughts |
| 3 | Create a composite person, firm, incident, or scene presented as singular — for any reason | Not for privacy, not for concision, not for narrative economy. Anonymize, never fuse |
| 4 | Compress or expand duration, or merge separate events into one scene | Merging is a composite scene, not a compression. Always forbidden |
| 5 | Invent sensory detail — weather, light, sound, clothing, gesture, room contents, physical sensation | If it is not in the record it does not exist, no matter how safe it seems |
| 6 | State a number the sources do not contain, including "several" → "six" or exceeding source precision | Source says "about a third"; "33.4%" is a fabrication. Full rules in `numbers-in-narrative` |
| 7 | Assert causation above the graded evidence level, or call an outcome inevitable when no contemporaneous source did | See the causal grade table in [resources/audit-passes.md](resources/audit-passes.md#causal-grades) |
| 8 | Show any actor acting on information that post-dates their action | This single check kills most hindsight contamination |
| 9 | Resolve a documented source conflict silently by picking one value | Both values, both sources, one sentence |
| 10 | Imply a date or place precision the record does not carry | Source says "in the spring"; the scene may not open "on a Tuesday in April" |
| 11 | Treat your own prior drafts, notes, or summaries as a source | Circular citation is invisible to reading and must be checked mechanically |
| 12 | Claim anything was "verified" when it was only "sourced" | You track provenance; you do not verify |
| 13 | Emit a boilerplate disclaimer ("some events compressed, some dialogue recreated") | Worse than nothing: cheap to emit, it pre-authorizes deviations and fakes a human judgment call |
| 14 | Accept the higher-truth argument in any form | "This is clearly what happened", "the reader will understand", "it's emotionally accurate", "it's a reasonable inference" |

## The Interiority Provenance Ladder

**This skill owns the [A]/[B]/[C]/[D] interiority ladder**; siblings cite this definition rather than restating it. Tag before you write the sentence, and tag again in the audit. The labels are this skill's working convention for compressing the practitioner ladder (Kramer, Clark), not a published four-tier standard.

| Tag | Evidence | Person example | System example | Permitted grammar |
|---|---|---|---|---|
| **[A]** | Subject stated the thought — contemporaneous note, email, message, recorded remark, or later on-record recall | Diary entry that night; "she recalled thinking the number was wrong" | Stated strategy in a filing, roadmap, board minutes, RFC, design doc | Direct rendering, cited. For later recall, memory-mark it. **Do not hedge** |
| **[B]** | A contemporaneous artefact stands in for the state | The cancelled order, the 03:00 commit, the resignation letter dated that day | The price move, the allocation shift, the reverted config, the halted line | Narrate the artefact; let it carry. **Do not hedge**. Write the alternative reading first: a resignation letter proves a resignation, not a disillusionment |
| **[C]** | Behavioural inference, or an on-record third party's belief | "His deputy believed he had already decided" | Revealed preference across many actors, labelled as aggregate behaviour | Attributed inference, or marked authorial inference. Rare enough to stay visible |
| **[D]** | Nothing. The state arrived in drafting | "He felt the ground shift." "She knew, then, that it was over." | "The market realized." "The protocol wanted." "The industry decided" | **None. Refuse.** Includes dead subjects and includes when the realization is the whole point of the scene |

When the record has no [A] or [B] for a required realization beat, pick one of five substitutes:

- **Behavioural turn** — narrate the documented change in action. The strategy reversed. The hiring stopped. The parameter was halved.
- **Artefact pivot** — an object dated to the moment: the revised deck, the deleted section, the new metric in the next board pack.
- **Attributed witness** — someone on the record says they saw the change.
- **Deferred revelation** — the reader understands at the end what the subject never did. This is the strongest move for system protagonists.
- **Named absence** — "No one recorded when the decision was made. By March it had been."

Then strike every noun and verb in the beat not traceable to a pointer. See whether the beat survives. If it collapses, it was invention wearing a substitute's clothes.

## The Three Altitudes

**SENTENCE** — what you are good at and what you will default to:
1. What does this sentence assert, including what it implies but does not state?
2. Which pointers support it? None means defect.
3. Did I observe, get told, read, or conclude this — and which one does the grammar tell the reader?
4. Which single word carries more certainty, specificity, or vividness than the source supports? Name the word.
5. What is the strongest reading of the source under which this sentence is false?
6. Does this verb make a causal claim, and does its grade support it?

**PARAGRAPH** — catches what sentence checking cannot:
7. Every sentence here is supported. Is the *implicature* supported? What will the reader believe after this paragraph that no sentence in it claims?
8. Does the ordering assert a causality no source asserts? Narrative adjacency reads as cause.
9. Does any transition sentence assert a state change nobody documented?

**PASSAGE** — where the documented failures live:
10. Would each person and institution depicted recognize this as a fair account? On what specific point would they object, and is that point in the text?
11. What did I cut here, and does the remainder imply a different frequency, magnitude, or balance than the full record?
12. Is this scene typical of the period it represents, or atypical and vivid? If atypical, does the text say so?
13. Does a category, metric, or moral frame used here postdate the events described? If so, does the text say so?

## Gate Verdict

Emit these fields verbatim. No field may be omitted.

```
BRIGHT-LINE BREACHES: n   (must be 0 to clear)
INTERIORITY [D]-COUNT: n  (must be 0 to clear)
UNRESOLVED POINTERS / CIRCULAR CITATIONS: n  (must be 0 to clear)
RED-FLAG HITS WITHOUT POINTERS: n
PASSAGE-LEVEL DEFECTS FOUND: n  (0 across a long piece = pass did not run)
SUBTRACTION SET VERDICT: <pattern found | no pattern | log absent>
HEDGE LOAD: <under budget | over budget -> passage is under-reported>
NOTE ON SOURCES: <generated from deviation log | not generated>
INVERSION CHECK: <pass | fail — deviation decided before drafting>
VERDICT: BLOCKED | RETURN TO RESEARCH | CLEARED AS SOURCED
```

"CLEARED AS SOURCED" is the strongest verdict available. There is no "verified".

## Guardrails

**Requirements:**
1. **Vocabulary discipline**: Never write "verified", "fact-checked", or "confirmed" about your own output. Use "sourced", "pointer resolves", "traced to".
2. **Zero-D gate**: A nonzero [D] count blocks publication. Report it as a number, not a description.
3. **Passage-level proof of work**: A clean report with no paragraph- or passage-level defect on a long piece is evidence the pass was skipped, not evidence the piece is clean.
4. **Subtraction reviewed as a set**: Per-edit review of cuts always passes. The pattern only appears in aggregate.
5. **Disclosure in the body, near the claim**: Any inference or reconstruction occupying a structural slot is disclosed within two sentences of itself, in the same typographic register. Endnote-only disclosure is functionally undisclosed. Mark those sentences non-removable; assume any later "tighten this up" pass will strip them.
6. **Label and disclose, do not delete**: The output of an asymmetry finding is a written justification requirement, not an automatic edit.
7. **Surface, do not adjudicate**: Where a real named person or active institution occupies an adversarial role, flag it for human decision. Quietly softening the language while keeping the structure makes the problem invisible rather than solving it.

**Common pitfalls:**
- Running only the sentence-level questions and reporting a clean piece.
- Stripping vivid detail that *is* in the record, teaching the writer to disable the scan.
- Hedging [A] and [B] material until the prose reads like a compliance document, after which a human strips all hedges wholesale.
- Accepting an internally generated "this is clearly what happened" as a reason rather than recognizing it as the named rationalization.
- Writing the note on sources first, so it becomes permission rather than description.
- Letting the aggregate ("the representative fab", "the median advertiser", "a typical incident") accrete a name, a date, a room, or a decision over the length of the piece.
- Spending audit budget on epistemic apparatus when the real signal is that the evidence does not support this architecture. Over-budget hedging means change the shape, not add more caveats.
- Over-attributing outcomes to luck and structure because the red-team literature is stocked with attacks on agency. State the strongest agency-based reading you considered and why it was not adopted.

## Quick Reference

**Key resources:**
- **[resources/bright-lines.md](resources/bright-lines.md)**: the fourteen refusals with bad/good pairs across post-mortem, market history, biography, supply chain and science writing; the higher-truth phrase catalogue; the breach disposition table; composite and aggregate discipline; chronology rules
- **[resources/audit-passes.md](resources/audit-passes.md)**: fabrication red-flag scan, evidence-class to attribution-grammar decision table, causal grade table with permitted verbs, chronology audit, proportion and omission audit, subtraction log format. Quantitative fidelity is handed off to `numbers-in-narrative`
- **[resources/disclosure-and-reporting.md](resources/disclosure-and-reporting.md)**: note-on-sources generator, deviation register, inversion check, gate report template, worked examples
- **[resources/evaluators/rubric_narrative_fidelity_audit.json](resources/evaluators/rubric_narrative_fidelity_audit.json)**: quality scoring

**Inputs required:**
- The draft under audit
- The source ledger produced by `narrative-evidence-ledger`: claims with pointers granular enough to re-find, each source annotated with date *and* interest, and the circular-citation check already run
- The subtraction log, if one was kept (its absence is itself a finding)
- Register and domain, so the ledger's ported attribution forms can be checked against the prose

**Outputs produced:**
- Bright-line breach list with dispositions
- Interiority tag map with [D] count
- Red-flag hit list, each resolved to a pointer or deleted
- Three-altitude defect list, separated by altitude
- Subtraction-set verdict and omission check
- Note on sources generated from the deviation log
- Gate verdict block

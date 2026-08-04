---
name: scene-construction-scam
description: Builds scenes that are reported rather than generated, by running a four-slot SCAM qualification gate (Setting, Character, Action, Meaning) with a source required per slot, a scene floor and ceiling, the 1-of-20 telling-detail cut with a provenance veto, the RUE pass, and a scene/summary narrative-distance audit against per-form ratio targets. Every technique has a person variant and a system variant (market, protocol, institution, codebase, supply chain). Use when turning research notes into a scene, opening a section with a moment, deciding whether a passage is a scene or summary, or auditing whether a vivid paragraph is actually sourced, or when user mentions scene, SCAM, show don't tell, telling detail, scene vs summary, summary in costume, establishing shot, make this vivid, or in medias res.
---

# Scene Construction (SCAM)

## Table of Contents
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [The SCAM Gate](#the-scam-gate)
- [Scene Floor and Ceiling](#scene-floor-and-ceiling)
- [Scene or Summary: Distance Targets](#scene-or-summary-distance-targets)
- [The Scene Provenance Ledger](#the-scene-provenance-ledger)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

**Related skills:** Use `narrative-fidelity-audit` for the interiority ladder and the bright lines, `narrative-arc-mapping` for where scenes sit in the whole piece, `narrative-opposition-web` for who the scene's actors oppose, `writing-structure-planner` for sequencing, `slop-detector` for the register pass that runs last. The fidelity audit owns the ladder and runs on a finished draft; this skill runs on a candidate scene before drafting.

## Core Principles

1. **Gate 4 decides everything**: Could this passage have been written without the source material? If yes, it is generated, not reported. Kill it. No other test in this skill outranks that one.
2. **An empty slot is a result, not a problem**: any unfilled SCAM slot means the passage is not a scene. Demote it to summary. Never fill a slot by inference, and never fill it because the piece needs a scene there.
3. **Sourced, never verified**: this skill tracks provenance. It cannot check whether a source is true. Write "sourced to X"; never write "verified" or "fact-checked".
4. **CHARACTER has a system variant**: the protagonist may be a market, a protocol, an institution, or a codebase. Then CHARACTER is the system's observable state at that moment, plus one distinguishing behavior. State means a clearing price, a queue depth, a p99 latency, an inventory, a wafer yield. It is never a want, a belief, or a decision.
5. **Stop at the ceiling**: two to four concrete elements. A fifth sourced detail that changes no inference is padding, and padding in a scene reads as texture manufactured to look reported.
6. **RUE, then swap**: delete every sentence explaining what the scene means. If the meaning disappears with it, the scene was the wrong scene. Swap the scene; do not restore the annotation.
7. **Thin record means honest summary or a gap note**: never a plausible specific. Reporting back "this material supports summary, not scene" is a successful outcome of this skill, not a failure.

## Workflow

Copy this checklist and track your progress:

```
Scene Construction Progress:
- [ ] Step 1: Build the scene provenance ledger (blocks everything after it)
- [ ] Step 2: Run the SCAM gate per candidate scene
- [ ] Step 3: Build to the floor, stop at the ceiling
- [ ] Step 4: Cut twenty details to one
- [ ] Step 5: RUE pass, then the scene/summary distance audit
- [ ] Step 6: Block or ship
```

Run these steps in order and do not batch them. Step 4's provenance veto collides with Step 3's concreteness push, and Step 5 can invalidate Step 3. When a later step changes load-bearing text, re-run the earlier step on that text only.

**Step 1: Build the scene provenance ledger**

Step 1.1: List candidate scenes. For each, open a ledger row and fill every required field in [The Scene Provenance Ledger](#the-scene-provenance-ledger). Any missing field BLOCKS the build of that scene. Do not draft prose for a blocked row.

Step 1.2: Fill the drift-and-proportion field: is this moment typical of the period it stands for, or atypical and vivid? Atypical scenes may still be used, but the text must say so on the page ("the sharpest of the eleven outages that quarter"), not in a footnote.

Step 1.3: Every pointer must resolve to an external artifact: page, section, timestamp, line number, table cell, commit hash, URL with retrieval date. Your own earlier notes, summaries, or drafts are never a source.

See [resources/scene-ledger.md](resources/scene-ledger.md) for the full field list, worked ledger rows, and the composite/aggregate rules.

**Step 2: Run the SCAM gate per candidate scene**

Step 2.1: Fill the four slots and their source column using [The SCAM Gate](#the-scam-gate). Use the system row for CHARACTER when the protagonist is not a person.

Step 2.2: Apply Gates 1 through 4 in order. Gate 4 is the last and the strictest: strip the citations mentally and ask whether a competent writer with no access to your sources could have produced this paragraph. If yes, delete it.

Step 2.3: Record the disposition of every failed candidate: demoted to summary, sent back as a research request, declared as an absence in the text, or cut. There is no fifth disposition. "Draft it and flag it" is not a disposition.

See [resources/scam-gate.md](resources/scam-gate.md) for the gate applied to five domains, including two candidates that correctly fail.

**Step 3: Build to the floor, stop at the ceiling**

Step 3.1: Meet the floor: one located place, one time marker, one observable action. Below the floor the reader is standing nowhere and the passage is summary.

Step 3.2: Stop at the ceiling: two to four concrete elements. Test each addition by asking whether it changes what the reader can infer. If not, it does not go in.

Step 3.3: Enter in medias res. After a section break, do not recap. No weather, light, or mood unless a source recorded weather, light, or mood.

Step 3.4: Dialogue in quotation marks must be verbatim from a transcript, recording, or contemporaneous written record, and must occur between people inside the scene. Testimony given to a researcher is quotation, not scene; label it as such.

**Step 4: Cut twenty details to one**

Step 4.1: List 15 to 20 candidate details before writing anything. Score each against the seven tests in [resources/detail-selection.md](resources/detail-selection.md).

Step 4.2: PROVENANCE is an absolute veto. A detail that is not in the record, sourced, and datable is cut regardless of how well it scores on every other test. There is no override.

Step 4.3: Keep one, occasionally two. Do not demote survivors into a list. Attach no adjective explaining what the detail means.

Step 4.4: Record which detail was kept and which were cut, so the selection can be audited as a set. Cuts that all point the same way are a proportion defect, not nineteen independent decisions.

**Step 5: RUE pass, then the scene/summary distance audit**

Step 5.1: Delete every sentence that explains the scene's meaning. Re-read. If the meaning is no longer available, swap the scene for one that carries it; do not restore the sentence.

Step 5.2: Label every paragraph S (summary) or C (scenic). Ambiguous gets X. X is a defect, not a third mode.

Step 5.3: Resolve every X. A general practice described with sensory adjectives is summary in costume: either demote it to clean summary or promote it with a date, a place, and named actors. Compare against the ratio targets in [Scene or Summary: Distance Targets](#scene-or-summary-distance-targets).

See [resources/distance-and-rue.md](resources/distance-and-rue.md) for the audit procedure, costume-summary examples, and the alternation rule.

**Step 6: Block or ship**

Step 6.1: Run the blocking checklist in [resources/scene-ledger.md](resources/scene-ledger.md#blocking-checklist). Any red line fires means do not ship the scene.

Step 6.2: Generate the note on sources from the ledger. Never write a boilerplate disclaimer in advance; a disclosure written before the deviation pre-authorizes it.

Validate using [resources/evaluators/rubric_scene_construction_scam.json](resources/evaluators/rubric_scene_construction_scam.json). **Minimum standard**: average score >= 3.5.

## The SCAM Gate

Fill this table per candidate scene. Every filled cell needs a source pointer.

| Slot | Person protagonist | System protagonist | Empty means |
|------|--------------------|--------------------|-------------|
| **S — Setting** | Place, time, and at least two physical specifics that a source records | Place, time, and at least two recorded conditions of the venue: the exchange session, the deploy window, the dock, the fab bay | No located moment. Not a scene. |
| **C — Character** | At least one physical detail and one behavioral detail, sourced | Observable state at that moment (price, queue depth, latency, inventory, yield, error rate) plus one distinguishing behavior of the system | No subject. Not a scene. |
| **A — Action** | At least three ordered observable events, each sourced | Three ordered observable events: an order posted, a fill printed, a limit hit; a commit, a rollout, a rollback | A state of affairs is not an action sequence. Not a scene. |
| **M — Meaning** | One sentence naming what the scene demonstrates | Same, and it must map to the piece's governing claim | No reason to include it. Cut. |

**Gate 1**: any empty slot means this is not a scene. Demote to summary. Do not fill by inference.
**Gate 2**: the MEANING sentence may introduce no information absent from S, C, and A. If it does, you are interpreting; move that sentence into the following summary block, where interpretation is licensed.
**Gate 3**: overinterpretation check. Sometimes a cigar is just a cigar. Would a skeptical reader accept this meaning from these details alone?
**Gate 4**: could this passage have been written WITHOUT the source material? If yes, it is generated, not reported. Kill it.

Attribution note: SCAM is journalism-pedagogy shorthand from Dynamics of Writing. It is **not** Jack Hart's acronym, and must not be attributed to him or to Storycraft.

## Scene Floor and Ceiling

**Floor** (all three required): one located place, one time marker, one observable action.

**Ceiling**: stop at 2 to 4 concrete elements. Not a room inventory.

A "scene" that covers a period of months is summary wearing a scene's grammar, and it quietly relicenses invented specificity. One dated decision, one filing, one price print, one shipped release, one failed test, one shift, one meeting.

## Scene or Summary: Distance Targets

| Form | Scenic share | Run-length rule |
|------|--------------|-----------------|
| Story narrative (one protagonist, one arc) | 40-60% | No summary run over 3 paragraphs |
| Explanatory narrative (action line explores a subject) | 15-30% | A scenic beat at least every 6-8 paragraphs |
| Analytical report or memo | 5-15% | Scenes only at openings, section heads, and the close |

These ratios are **operational defaults derived for mechanization**, not published figures from any craft text. Tune them per project and say so.

**Summary in costume** is the defect these targets exist to catch. It is the paragraph that sounds scenic and cites nothing:

- Bad: "Across the Gulf ports that spring, dispatchers watched the backlog swell, phones ringing off the hook as one delayed vessel became six."
- Good, as summary: "Dwell time at the four Gulf container terminals rose from 3.1 to 8.7 days between March and May 2021 (PMSA monthly, table 2)."
- Good, as scene: "At Barbours Cut on 14 May, the *Ever Lissome* was logged in at 06:12 and did not begin discharge until 19:40 (terminal berth log, entry 2214)."

## The Scene Provenance Ledger

Required per scene. **Any missing field blocks the build.**

| Field | Content |
|-------|---------|
| Scene ID | Stable handle used by the draft |
| Date and place | Exact as the source carries it. Never imply finer precision than the source |
| Actors | Named real people or named systems. No composites, no unnamed thesis-voicing extras |
| Action sequence | The three-plus ordered events, each with its own pointer |
| Source pointers | External artifacts only. Not your own summaries or drafts |
| Interior-state class | Per interiority claim, tag [A] said-so, [B] document, [C] inference, [D] unsourced. Ladder defined in `narrative-fidelity-audit`, which owns it; any [D] refuses |
| Drift and proportion | Typical of the period, or atypical? If atypical, the flag text that will appear on the page |
| Subtraction log | What was cut from this moment, and whether the remainder implies a different frequency or magnitude than the record |
| Disposition | Built, demoted to summary, research request, declared absence, or cut |

Composites are prohibited regardless of framing: never merge two people, firms, incidents, shifts, or datasets into one entity presented as singular, not for privacy, not for concision, not for narrative economy. Aggregates ("the median advertiser", "a representative 200mm fab") are permitted only if labeled at first use, and they may never take a proper name, a date, a location, dialogue, intent, or sensory detail. The moment an aggregate gets a Tuesday and a phone call, it is a fabricated character. Never label an aggregate a "composite". That word is reserved for the prohibited operation, and reusing it re-licenses what this line forbids.

## Guardrails

**Requirements:**

1. **Ledger before prose**: no scene is drafted before its ledger row is complete. A slot that cannot be filled produces a gap entry, never prose.
2. **Provenance veto is absolute**: a detail with no pointer is cut at any score. The scan keys on missing pointers, never on vividness. A vivid detail that has a pointer survives no matter how good it sounds.
3. **No invented sensory material**: literary-journalism sensory technique does not transfer to unreported domains. A writer working from filings, logs, or archives was in no room. If no source observed the setting, there is no setting, and the honest output is summary.
4. **Systems get states, not wants**: no "the market realized", "the protocol decided", "the model believed". Personify at most once, explicitly, as a framing device. After that, attribute behavior to named mechanisms and named actors. An imputed institutional intent requires a filing, minute, transcript, or quoted executive.
5. **Refusal is an output**: "this material supports exposition, not narrative" is a valid, complete result. Return it rather than manufacturing the missing elements.
6. **Name the rationalization**: "this is clearly what happened", "the reader will understand", "it is emotionally true", "it is a reasonable inference" is the higher-truth argument. It is the named failure of this entire genre, and it will arrive sounding like good judgment. Refuse it in all its forms.

**Common pitfalls:**
- Establishing-shot bloat: weather, architecture, and mood written because that is what literary journalism looks like, in a domain where none of it was observed.
- Detail confetti: six details each passed the tests, so all six were kept, producing an inventory paragraph that reads as texture and carries no inference.
- The plausible bridge: a connective sentence asserting a state change ("by then the pressure was impossible to ignore") that carries no proper noun, trips no fact-check, and is pure invention. Transitions need pointers too.
- Subtraction drift: every sentence sourced, the piece false, because the failed pilot and the dissenting engineer were each cut for length. Review the subtraction log as a set.
- The scene promoted because it was vivid rather than because it was representative.
- Claiming a fact was "verified" when it was only sourced.
- Attribution errors that destroy credibility on first inspection. Do not credit SCAM to Hart. Do not cite "the Oregon Method" as a codified canon; it is a retrospective label for the Oregonian coaching practice, not a defined system. Do not present the ratio and count thresholds here as published figures.

## Quick Reference

**Key resources:**
- **[resources/scam-gate.md](resources/scam-gate.md)**: the four slots worked through five domains, including two candidates that fail, plus the demotion procedure
- **[resources/detail-selection.md](resources/detail-selection.md)**: the 1-of-20 cut, the seven tests, worked cuts, the representativeness flag
- **[resources/distance-and-rue.md](resources/distance-and-rue.md)**: the S/C/X audit, costume summary, RUE, the alternation rule, gap-note formats
- **[resources/scene-ledger.md](resources/scene-ledger.md)**: ledger schema, composite and aggregate rules, blocking checklist, note-on-sources generation
- **[resources/evaluators/rubric_scene_construction_scam.json](resources/evaluators/rubric_scene_construction_scam.json)**: quality scoring

**Inputs required:**
- A researched corpus with resolvable pointers (documents, logs, filings, transcripts, datasets)
- The form of the piece (story narrative, explanatory narrative, analytical report)
- The governing claim the scene's MEANING slot must map to
- Representativeness judgments: which cases are typical of the period, which are extreme

**Outputs produced:**
- A completed scene provenance ledger, one row per candidate
- SCAM gate results with the disposition of every failed candidate
- Built scenes at floor and ceiling, with one telling detail each
- An S/C/X paragraph map with the measured scenic share against the form's target
- A gap register: research requests, declared absences, and cuts
- A note on sources generated from the ledger

---
name: narrative-handoff-contract
description: Defines and validates the machine-readable contract that passes a narrative architecture between a structural agent and a drafting agent — architecture.json with evidence-backed slots, capped scene tags, gap dispositions, a DEAD column, and an escalation object for sending defects back upward. Ships a validator script so the rules are enforced rather than requested. Use when two agents or two sessions must hand narrative work to each other, when an architecture needs checking before drafting begins, when a draft must report a defect it cannot fix at its own layer, or when the user mentions handoff, contract, schema, validator, architecture.json, escalation, or "the outline and the draft have drifted apart".
---

# Narrative Handoff Contract

## Table of Contents

- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [The three fields that carry the weight](#the-three-fields-that-carry-the-weight)
- [The escalation object](#the-escalation-object)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

**Related skills:** Use `narrative-evidence-ledger` to build the claim set this contract points at, `narrative-arc-mapping` to fill the slots, and `narrative-fidelity-audit` to check the prose that comes back.

## Core Principles

1. **A pipeline whose interface is prose has no interface.** Two agents that hand each other paragraphs cannot enforce anything. The handoff is a file.
2. **The evidence array is the validated field, not the value.** A slot with a confident sentence and no claim ID fails here rather than reading well downstream.
3. **ABSENT is a passing state.** An architecture with every slot filled is flagged, because real material always has holes.
4. **Enforce with a cap, not a request.** "Never draft prose" decays as context fills. A length limit on scene lines does not.
5. **The channel runs both ways.** Without an escalation object the drafting layer has no way to report a structural defect, so it papers over it with polish.
6. **Pointers resolve outward.** A citation resolving into the pipeline's own earlier output is circular, invisible to reading, and a hard failure.

## Workflow

Copy this checklist and track your progress:

```
Handoff Contract Progress:
- [ ] Step 1: Emit the architecture object
- [ ] Step 2: Validate before handing off
- [ ] Step 3: Write the demand manifest
- [ ] Step 4: Receive and route escalations
```

**Step 1: Emit the architecture object**

Step 1.1: Write `architecture.json` with the fields in [resources/schema.md](resources/schema.md). Start from the worked example there rather than from an empty file.

Step 1.2: Stamp the run header — model, corpus reference, timestamp, and the list of claim IDs actually consulted. A run over a corpus too large to read linearly must record which claims it did **not** see. Silent partial coverage reported as full coverage defeats every audit downstream.

Step 1.3: Write incrementally. Append each slot as you settle it, so a run that dies partway loses one slot rather than the whole pass.

**Step 2: Validate before handing off**

Step 2.1: Run the validator. It reports every problem, not just the first:

```
python3 resources/validate_architecture.py path/to/architecture.json \
    --corpus-root path/to/corpus --output-root path/to/pipeline/output
```

Step 2.2: Fix errors. Read warnings as diagnosis rather than noise — "0 slots ABSENT" usually means slot-filling, not unusually complete material.

Step 2.3: Use `--strict` in CI, where a warning should stop the build. Leave it off while drafting.

**Step 3: Write the demand manifest**

Step 3.1: Give the drafting agent absolute paths, an explicit scope in beat IDs, an explicit out-of-scope statement, the style contract, and the required return shape.

Step 3.2: Read it back as a stranger. If it only makes sense to someone who saw the previous conversation, it will fail. The downstream agent inherits nothing else.

**Step 4: Receive and route escalations**

Step 4.1: An escalation naming layer `architecture` is a defect in the spine or the slot. An escalation naming layer `reporting` means the corpus lacks something — route it to research, not to redrafting.

Step 4.2: A spine change is legal but never local. Bump `spine_version`, invalidate the draft, and re-pass from the scene weave down. Patching one section into a different structure while the rest keeps the old one is what readers register as untrustworthy without being able to say why.

## The three fields that carry the weight

| Field | Rule | What it prevents |
|---|---|---|
| `slots[].evidence[]` | Non-empty for any slot not marked ABSENT | A fluent sentence standing in for a finding |
| `slots[].status` | `ABSENT` passes; all-filled warns | Twenty-two slots producing twenty-two inventions |
| `scenes[].tagged_line` | Hard character cap | The structural agent quietly drafting, leaving the craft agent editing text instead of executing architecture |

Two more matter almost as much. `dead_column[]` keeps every killed finding, distinguishing `did_not_support` from `CONTRADICTED` — the second always reaches the reader, and its absence is how cherry-picking becomes undetectable. And `scenes[].representativeness` is assigned upstream against the corpus, never by the drafting agent, because a vivid case in the opener is selected for energy and energy correlates with being atypical.

## The escalation object

```json
{
  "beat_id": "b14",
  "layer": "architecture",
  "defect": "No particular exists anywhere in the corpus for this beat; the ladder audit finds an R2 run with no R1 within two paragraphs.",
  "what_would_resolve_it": "Either a dated artifact from the 1998 filings, or a redesign that does not require a scene here."
}
```

`layer` is `architecture` when only the spine can resolve it, and `reporting` when the material itself is missing. Both are successful outputs. Neither is a request for permission to invent.

## Guardrails

**Requirements:**

1. **Validate before every handoff.** An unvalidated contract is a suggestion.
2. **Absolute paths only.** Relative paths across an agent boundary are a documented recurring failure.
3. **Version the contract.** A run that cannot say which contract it was written against cannot be re-derived or diffed.
4. **Every gap carries exactly one disposition** — RESEARCH, REDESIGN, DECLARE or CUT. There is no "draft and flag": flagged prose survives review at high rates because it reads well.
5. **Zero gaps is a red flag, not a success.**

**Common pitfalls:**

- Treating the markdown companion as the artifact. Generate it from the JSON; never edit it by hand and expect the JSON to follow.
- Letting the drafting agent widen its own scope because "the next section obviously follows."
- Recording coverage as the whole corpus when the agent read the first N chunks.
- Deleting killed findings to tidy the file.
- Escalating by writing a note into the prose instead of emitting the object, where nothing will route it.

## Quick Reference

**Key resources:**
- **[resources/schema.md](resources/schema.md)**: full field list, types, and a worked example for a system protagonist
- **[resources/validate_architecture.py](resources/validate_architecture.py)**: the validator; exit 0 pass, 1 violated, 2 unreadable
- **[resources/evaluators/rubric_narrative_handoff_contract.json](resources/evaluators/rubric_narrative_handoff_contract.json)**: quality scoring

**Inputs required:**
- A claim set or evidence ledger with stable claim IDs
- A chosen structure and its slots
- The output directory, for the circular-citation check

**Outputs produced:**
- `architecture.json`, validated
- A demand manifest a stranger could execute
- Escalation objects routed by layer

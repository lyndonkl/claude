---
name: hedge-detector
description: Classifies every hedge in a substacker draft as either a precision hedge (keep — "n=1 may not replicate", "I do not know") or an epistemic-weakness hedge (flag — "I think", "perhaps", "arguably", "it could be argued"). Only flags weakness hedges; suggests either a commit (remove hedge, take position) or a specific hedge (name the uncertainty). Use when a draft feels wishy-washy or when a cluster of modal verbs appears. Trigger keywords: hedging, I think, perhaps, arguably, uncertainty, weak claim, wishy-washy.
---

# Hedge Detector

## Table of Contents

- [Precision vs weakness](#precision-vs-weakness)
- [Workflow](#workflow)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by the Editor in the voice pass. Complements `voice-check` (which flags "I think" as a don't-list phrase when used as primary hedge). This skill does the finer classification.

## Precision vs weakness

**Precision hedge (KEEP)**: scope-naming, sample-size-caveat, specific-uncertainty.
- "I do not know" (full sentence) — writer's signature.
- "I am not claiming…" — explicit scope.
- "On my 3B-param run…" — sample caveat.
- "n=1 may not replicate."
- "I have only tested this on 3 teams."

**Epistemic-weakness hedge (FLAG)**: softens without adding information.
- "I think" (when followed by a claim).
- "Perhaps" (standalone).
- "Arguably" — deniability.
- "It could be argued" — auto-deniability.
- "Somewhat" — weakening adverb.
- "Seems" (when no sensing is happening).
- "It seems clear that" — worst-of-both-worlds.

## Workflow

```
For each hedge in the draft:
- [ ] Step 1: Detect hedge markers (modal verbs + phrase list above)
- [ ] Step 2: Classify as precision or weakness
- [ ] Step 3: For weakness, suggest a commit OR a specific hedge (both, as 2 rewrite options)
- [ ] Step 4: For precision, leave alone (note in the "calibrated hedges kept" count)
- [ ] Step 5: Emit the hedge audit with both lists
```

### Step 2: Classifier

A hedge is **precision** if paired with specific bounds:
- Sample size named (n=1, 3B model, last 12 weeks)
- Scope named ("in three teams I've worked with")
- Specific uncertainty named ("I have not re-derived the gradient")

Otherwise **weakness**. Default to weakness when unsure — the writer prefers over-flagging here.

### Step 3: Rewrite options

For each weakness hedge:
- **Option A (commit)**: remove hedge, take position. "I think batch size matters" → "Batch size matters."
- **Option B (specific)**: name the uncertainty. "I think batch size matters" → "On this 3-run sweep, batch size moved loss by 0.08."

Both options; writer picks.

## Worked example

**Draft sentences**:
1. "I think RAG beats fine-tuning for most teams."
2. "I do not know whether this holds at 70B — my only test was on a 3B model."
3. "Arguably the attention mask is wrong."
4. "Perhaps fine-tuning is better when you have very specific stylistic requirements."

**Classification**:

| # | Hedge | Class | Rewrites |
|---|---|---|---|
| 1 | "I think" | weakness | (a) "RAG beats fine-tuning for most teams." (b) "In the three teams I've worked with, RAG beat fine-tuning." |
| 2 | "I do not know" + scope | **precision** | Keep as-is. |
| 3 | "Arguably" | weakness | (a) "The attention mask is wrong." (b) "The attention mask looks wrong to me — I have not re-derived the gradient." |
| 4 | "Perhaps" + "very specific" | weakness | (a) "Fine-tuning wins on style." (b) "Fine-tuning wins on style; I have not tested this below 7B." |

## Guardrails

1. Never flag precision hedges. They are a voice feature.
2. Never replace "I do not know" — this is the writer's signature phrase.
3. Suggest 2 rewrite options (commit + specific), not 3+.
4. Hedge clusters (≥2 weakness hedges within 50 words) get flagged once, collectively — also surfaced to `slop-detector` signal S8.
5. Don't flag hedges in quoted text or code fences.
6. If the draft is a reflective essay openly admitting uncertainty as its subject, relax the threshold — flag only the most decorative hedges.

## Quick reference

- Input: draft.
- Output: hedge audit — weakness hedges with rewrites, precision hedges kept with a count.
- Signal downstream: cluster count goes to `slop-detector` S8.

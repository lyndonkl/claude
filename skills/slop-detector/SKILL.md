---
name: slop-detector
description: Scans a substacker draft for 10 signatures of AI-generated explainer slop — meta-framing openers ("In this post"), list-heavy argument, nominalization clusters, generic examples lacking first-person texture, prompt-residue phrases ("Let's break this down"), buzzword stuffing, outline-shaped paragraphs, hedge clusters, flattened uncertainty. Use when a draft "feels generic" even after voice-check passes. Trigger keywords: slop, AI-written, generic, template, meta-framing, zombie nouns, prompt residue, outline-shaped.
---

# Slop Detector

## Table of Contents

- [The 10 signatures](#the-10-signatures)
- [Workflow](#workflow)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by the Editor voice pass. Consumes hedge-cluster count from `hedge-detector` (S8). Emits the "Slop signatures" subsection.

## The 10 signatures

Fixed list. Each either `clean` or `flagged` with the offending span.

| # | Signature | Detection |
|---|---|---|
| S1 | Meta-framing opener | First paragraph contains `In this post`, `This article`, `We will explore`, `Let's dive into`, `Today we'll look at` |
| S2 | List-carrying-argument | Any bulleted list where the argument collapses if bullets are removed. Test: does the prose still stand without the list? |
| S3 | Zombie nouns (Sword) | >3 nominalizations per 100 words (suffixes: -ation, -ity, -ment, -ence on abstract nouns) |
| S4 | Generic examples | "a company" / "a model" / "a user" with no specific name, scale, dataset |
| S5 | No first-person | Zero `I`, `my`, `we-as-me` in a >800-word reflective essay |
| S6 | Prompt residue | `Let's break this down`, `To summarize`, `In conclusion`, `Key takeaways`, `Let me explain` |
| S7 | Outline-shaped paragraphs | >60% of paragraphs follow same syntactic shape: topic → 3 supporting sentences → transition |
| S8 | Hedge cluster | ≥2 epistemic-weakness hedges within 50 words (from `hedge-detector`) |
| S9 | Buzzword stuffing | ≥3 terms from {game-changer, paradigm shift, under the hood, delve, unpack, dive into} in a single draft |
| S10 | Flattened uncertainty | Any small-N caveat that appears in `corpus/drafts/notes/` but was removed in the submitted draft (requires notes; else skip this signature) |

## Workflow

```
Slop scan draft D:
- [ ] Step 1: For each signature, run detection rule
- [ ] Step 2: Mark each signature as clean | flagged (with quote)
- [ ] Step 3: Tier-1 signatures: S1, S2, S6 (generic framing + prompt residue)
- [ ] Step 4: Tier-2 signatures: S3, S4, S5, S7, S9
- [ ] Step 5: Emit the slop signatures subsection with each labeled clean/flagged
```

### S3 nominalization scoring

Count suffix hits (`-ation`, `-ity`, `-ment`, `-ence`, `-ness`, `-ance`) on abstract nouns per 100 words. >3 = flag. Example: "provides analysis of" → nominalized; "analyzes" → active.

### S4 generic-example rule

Flag an example if it uses only generic pronouns / nouns without a specific anchor:
- "A company might use this" → flag.
- "At Google in 2024, Chen et al. used this" → clean.

### S7 outline-shape rule

Parse paragraphs; count those with the shape:
- Sentence 1: topic statement
- Sentences 2–4: three supporting sentences
- Last sentence: transition

>60% of paragraphs following this shape → the draft reads like an AI-generated outline expanded.

## Worked example

**Draft fragment**:
> In this post, we'll explore why RAG beats fine-tuning.
>
> First, let's define RAG. It's a technique where models retrieve documents before generating. A company might use RAG for their customer service chatbot.
>
> Second, fine-tuning involves training. A team might fine-tune to adapt style.
>
> Third, RAG has benefits. Fine-tuning has drawbacks. It could be argued that hybrid works.
>
> To summarize, both approaches have merit.

**Detections**:
- S1: flagged ("In this post, we'll explore").
- S2: flagged (argument carried by "First / Second / Third" list-in-prose).
- S3: zombie-noun check — "technique", "documents", "benefits", "drawbacks" — borderline. Not flagged yet.
- S4: flagged ("A company might use RAG", "a team might fine-tune") — no specifics.
- S5: clean (has "we").
- S6: flagged ("To summarize").
- S7: flagged (each paragraph: topic + supporting + transition).
- S8: weakness hedges — "It could be argued" — cluster check: just 1, not a cluster (yet).
- S9: buzzword — "explore" is close. Not flagged yet (1 term).
- S10: skipped (no notes dir).

**Output**: 5 signatures flagged (S1, S2, S4, S6, S7). Tier-1: S1, S2, S6 = 3 tier-1 slop violations.

## Guardrails

1. Each signature has a concrete detection rule. No "feels slop."
2. Quote the offending span. Don't just say "S1 triggered" — quote the opener.
3. Signatures are additive, not exclusive. A draft can trip 8 signatures and still be revise-able; Editor's must-not #13 sets the no-go threshold.
4. S10 requires a notes dir; skip quietly if absent.
5. Don't double-count with `hedge-detector`. Hedge clusters flow from hedge-detector into S8 as an input, not a separate scan here.
6. S5 (no first-person) — reflective essays only. How-to / methodology posts may legitimately lack "I."

## Quick reference

- 10 fixed signatures, deterministic detection.
- Tier-1: S1, S2, S6. Tier-2: the rest.
- Consumes `hedge-detector` cluster count as S8 input.

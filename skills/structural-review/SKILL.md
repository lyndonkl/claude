---
name: structural-review
description: Performs pass-1 structural review of a substacker essay draft — argument flow, out-of-order moves, buried topic sentences, missing pivots, weak signposting, paragraph-logic issues. Emits the "Argument flow" and "Structural blockers" sections of the Editor artifact. Use when reviewing a draft's macro-structure before addressing voice, when a draft feels like it meanders, or when the user asks whether the argument lands. Trigger keywords: structure, argument flow, outline, signposting, meandering, pivot, macro edit, substantive edit.
---

# Structural Review

## Table of Contents

- [Workflow](#workflow)
- [Expected essay shape](#expected-essay-shape)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by the Editor as the first structural skill. Runs before voice-check, hedge-detector, slop-detector. Pairs with `paragraph-rhythm-check` (paragraph logic) and `opener-critique` / `closer-critique`.

## Workflow

```
Structural review of draft D:
- [ ] Step 1: Extract paragraphs as an array. For each: first-sentence topic + word count
- [ ] Step 2: Produce a 1-line-per-paragraph outline of the draft AS READ
- [ ] Step 3: Compare to expected essay shape (see below)
- [ ] Step 4: Flag out-of-order moves, buried topic sentences, walls, missing pivots, weak signposts
- [ ] Step 5: Per flag: tier (1 or 2), paragraph index, quote, reason, ≤2 suggested rewrites
```

## Expected essay shape

Writer's signature shape (from voice-profile signature moves + opening/closing patterns):

```
1. Confession / concrete admission (opener)
2. Reframe / thesis
3. Exposition (mechanism, data, arithmetic)
4. Pivot (usually a one-sentence paragraph)
5. Applied case / example (often the IPL/Kalshi trade or a pathology slide)
6. Bolded maxim or forward-looking close
```

Not every essay hits every beat — short reflective posts skip steps 3 and 5. Series-log posts compress 2-3 and always include a scoreboard in 6.

**Flag if**:
- Hook is news-based or generic-opener (see `opener-critique`).
- Step 3 (mechanism) appears before step 1 (confession). "In this post we'll explore" structure = tier-1.
- Step 5 is missing in a full essay (not a series-log). Writer's voice has lived texture; its absence is a signal.
- Step 6 is absent entirely (no close). Tier-1.
- Buried topic sentence: the paragraph's point is in sentence 3 or later. Flag as tier-2.
- Wall: paragraph >120 words with no internal pivot. Flag as tier-2.

## Worked example

**Draft outline (as Editor reads it)**:
- Para 1 (42 w): "In today's AI landscape, teams often wonder whether RAG or fine-tuning…"
- Para 2 (81 w): Defines RAG.
- Para 3 (68 w): Defines fine-tuning.
- Para 4 (bullets): Comparison list.
- Para 5 (55 w): "I think RAG is the right choice for most teams."
- Para 6 (37 w): "To summarize, both have merit."

**Flags (structural)**:
1. (Tier-1) Hook is generic ("In today's AI landscape…"). Expected: confession. Rewrites: (a) "I spent four months moving a RAG pipeline to a fine-tune. I was wrong about which would win." (b) "I had never shipped a fine-tune until last quarter."
2. (Tier-1) Mechanism before confession. Structural ordering violates the writer's shape. Rewrite: restructure so confession precedes exposition.
3. (Tier-1) No pivot paragraph. Suggest: insert one-sentence paragraph at ~paragraph 3.5 marking the turn.
4. (Tier-1) Argument runs through a bulleted list (para 4). Rewrite: convert to 3 short paragraphs, one mechanism each.
5. (Tier-2) Closer is "To summarize" — prompt residue + no bolded maxim. Rewrite: replace with a mechanism close (e.g., "**You're choosing where your domain knowledge lives — in weights, or in retrieval.**").

## Guardrails

1. Never flag voice issues. This skill is structural only.
2. Never propose more than 2 rewrite options per flag.
3. Flags are located by paragraph index. If the writer paginates sections, cite section + paragraph.
4. Do not rewrite the draft. Rewrites are ≤2 sentences each, bracketed.
5. Series posts (frontmatter `series: {slug}`) get a special-case: step 5 often IS the scoreboard+trade narration, not an extended applied case. Don't flag absence.
6. If the draft is a how-to / methodology post (H2 headers throughout, numbered steps), the expected shape is different (intro → sections → wrap). Detect and adapt.

## Quick reference

- Input: draft markdown.
- Output: the "Structural pass → Argument flow" + "Structural blockers" sections.
- Runs first in the Editor pipeline.

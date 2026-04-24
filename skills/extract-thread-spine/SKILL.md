---
name: extract-thread-spine
description: Extracts the 5-7 point argument backbone of a published substacker essay into a structured _spine.json working artifact that downstream platform-rewrite skills consume. Pulls verbatim sentences where possible (not paraphrases). Tags each point with evidence anchor (paper, anecdote, formula, analogy), essay section, and translatability score. Use at the start of a Distribution Translator run. Trigger keywords: spine, backbone, extract claims, thread spine, argument skeleton.
---

# Extract Thread Spine

## Workflow

```
For a published essay P:
- [ ] Step 1: Read P end-to-end
- [ ] Step 2: Identify thesis (usually opening confession + first pivot sentence)
- [ ] Step 3: Extract 5-7 load-bearing claims IN ORDER
- [ ] Step 4: Tag each claim: evidence_type (confession / claim / paper / analogy / formula / maxim), essay_section, translatability (1-5)
- [ ] Step 5: Extract closing_maxim verbatim
- [ ] Step 6: Extract 3 candidate hook sentences (from the essay itself, not paraphrases)
- [ ] Step 7: Write _spine.json
```

## Output schema

```json
{
  "thesis": "{one sentence, verbatim or lightly-compressed from the essay}",
  "claims": [
    {"text": "verbatim from essay", "evidence_type": "confession|claim|paper|analogy|formula|maxim", "essay_section": "opener|pivot|body|closer", "translatability": 1-5}
  ],
  "closing_maxim": "{verbatim from essay, usually bolded in the post}",
  "best_hook_candidates": [
    "{verbatim sentence 1}",
    "{verbatim sentence 2}",
    "{verbatim sentence 3}"
  ]
}
```

Translatability: 5 = works on any platform; 1 = needs the full essay's setup to make sense.

## Worked example

**Input** (essay *The Execution Gap*, abridged):

> I have been meaning to open a Kalshi account for months.
>
> Not casually meaning to...
>
> This is not a story about prediction markets. It is a story about the distance between learning about something and actually doing it.
>
> [methodology, Brier arithmetic...]
>
> **I have not tried this. Not once.**

**Output _spine.json**:
```json
{
  "thesis": "Learning about prediction markets is not the same as betting on them. The gap between knowing and doing is the real subject.",
  "claims": [
    {"text": "I have been meaning to open a Kalshi account for months.", "evidence_type": "confession", "essay_section": "opener", "translatability": 5},
    {"text": "This is not a story about prediction markets. It is a story about the distance between learning about something and actually doing it.", "evidence_type": "claim", "essay_section": "pivot", "translatability": 5},
    {"text": "Say you predict a team at 80% confidence. If they win, your Brier score is (0.80 - 1)^2 = 0.04. But if they lose, it's (0.80 - 0)^2 = 0.64. That's catastrophic.", "evidence_type": "formula", "essay_section": "body", "translatability": 3},
    {"text": "I have not tried this. Not once.", "evidence_type": "maxim", "essay_section": "closer", "translatability": 5}
  ],
  "closing_maxim": "I have not tried this. Not once.",
  "best_hook_candidates": [
    "I have been meaning to open a Kalshi account for months.",
    "I am one of those people who substitutes learning for doing.",
    "This is not a story about prediction markets. It is a story about the distance between learning about something and actually doing it."
  ]
}
```

## Guardrails

1. Pull verbatim sentences. Paraphrasing is the slop door — the writer's voice is in the exact phrasing.
2. Never invent a claim not in the essay.
3. Exactly 5–7 claims. Fewer under-represents; more overwhelms downstream rewrites.
4. Preserve paper attributions intact at this stage. X skill decides per-tweet trade-offs later.
5. `closing_maxim` is verbatim — it's what the writer will want bolded in the Substack Note.
6. Translatability is the writer's dial. Use it; don't inflate everything to 5.

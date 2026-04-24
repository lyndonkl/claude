---
name: tag-by-topic
description: Assigns 1-4 topic tags to a seed body from the controlled vocabulary in substacker shared-context/topic-ledger.md. Prevents tag sprawl at small-corpus scale by requiring existing-tag match or logged addition. Uses keyword + title match; logs near-miss candidates to pending-tags. Use after format normalization and before dedupe. Trigger keywords: tag, topics, categorize, classify, taxonomy, controlled vocabulary, topic ledger.
---

# Tag by Topic

## Table of Contents

- [Workflow](#workflow)
- [Controlled vocabulary rules](#controlled-vocabulary-rules)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by `ingest-inbox-item` step 2. Writes to `topic-ledger.md` pending-tags section when proposing additions. Upstream of `update-topic-ledger` (which records the finalized counts per tag).

## Workflow

```
Tag one seed:
- [ ] Step 1: Read shared-context/topic-ledger.md — collect current tag set
- [ ] Step 2: Score each existing tag against body + title (keyword + weighted title match)
- [ ] Step 3: Select top 1-4 tags above threshold
- [ ] Step 4: If top-1 score below threshold, propose new tag in kebab-case; log to pending-tags
- [ ] Step 5: Return {topics: [str], pending_tags: [str]}
```

### Step 2: Scoring

For each existing tag, compute:
- `keyword_match` = number of times tag-words appear in body (normalized by body length)
- `title_match` = 3× if tag-words appear in title, else 0
- `score = keyword_match + title_match`

Threshold for selection: `score ≥ 0.3` (tunable — start at 0.3, adjust if tagging is noisy).

### Step 3: Select top 1–4

- If 0 tags above threshold → assign `unclassified` and log this as a signal that vocabulary may need extension.
- If 1–4 tags above threshold → return them, highest-score first.
- If >4 above threshold → keep top 4 by score.

### Step 4: New-tag proposal

If the top-1 score is below threshold, the body is about something the vocabulary doesn't cover. Propose a new tag:

- Extract 2–4 candidate keywords from title + first paragraph.
- Kebab-case: lowercase, hyphen-separated, `^[a-z0-9]+(-[a-z0-9]+)*$`.
- Append to `topic-ledger.md#pending-tags`:
  ```
  - tag: {proposed-tag}
    proposed_at: YYYY-MM-DD
    seed_id: {seed-id}
    justification: "{one-line reason}"
  ```
- Still return the closest existing tag for the seed's `topics`, so the seed is not untagged.

Never silently add to canonical vocabulary. The writer reviews pending-tags and promotes.

## Controlled vocabulary rules

- Max 4 tags per seed (enforced).
- Min 1 tag (enforced; use `unclassified` if truly nothing fits).
- Tag names: `^[a-z0-9]+(-[a-z0-9]+)*$`.
- New-tag additions require logged pending entry. Never silent.
- Tags are internal taxonomy — NOT Substack tags (which are a separate platform feature).

## Worked example

**Input seed body** (dropout-as-ensemble):
> had a thought while running — dropout is secretly an ensemble method. each forward pass is a different sub-network. so at test time when you turn dropout off and scale, you're averaging predictions across exponentially many thinned networks. this is why it generalizes. not "regularization" in the L2 sense. more like bagging.

**Existing tags** (from topic-ledger.md): `regularization`, `attention-mechanism`, `rag`, `emergence`, `kalshi`, `ipl-cricket`, `pathology-ai`.

**Scoring**:
- `regularization`: keyword "regularization" in body → 0.4. Score: 0.4.
- `ensembling`: NOT in vocabulary → propose.
- `dropout`: NOT in vocabulary → propose.

**Output**:
- `topics: [regularization]` (only one existing tag scored above threshold)
- `pending_tags: [ensembling, dropout]` logged to topic-ledger with this seed-id.

The writer reviews pending and either promotes both to canonical or renames to existing synonyms.

## Guardrails

1. Maximum 4 tags — hard enforced.
2. Minimum 1 tag — `unclassified` if nothing fits.
3. New tag proposal is always logged; never silent addition.
4. Tag names must match `^[a-z0-9]+(-[a-z0-9]+)*$`. Reject any other form.
5. Do not remove existing tags from the ledger. If a tag becomes cold, that's a state change, not a removal.
6. Do not use `score-intuition-density` or `dedupe-against-corpus` logic here — this is topic-only.

## Quick reference

- Input: seed body + partial frontmatter.
- Output: `{topics: [str], pending_tags: [str]}`.
- Side effect: may append to `topic-ledger.md#pending-tags`.

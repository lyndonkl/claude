---
name: rank-by-user-fit
description: Scores and ranks substacker Trend Scout annotated candidates against voice-profile and goals, producing a top-10 keep list and an explicit drop list with reasons. Weighted-sum scoring across intuition-density fit, goal alignment, dedup penalty, source reliability, freshness. Produces the digest's keeps and drops sections. Use after cross-ref-topic-ledger. Trigger keywords: rank, fit score, user fit, keep list, drop list, signal weight.
---

# Rank by User Fit

## Workflow

```
Per candidate pool:
- [ ] Step 1: Score each on 5 dimensions (intuition_density_fit, goal_alignment, dedup_penalty, source_reliability, freshness)
- [ ] Step 2: Weighted sum → rank
- [ ] Step 3: Top items with score > threshold (default 30), max 10 → keep list
- [ ] Step 4: Remaining → drop list; per-drop one-line reason using worst-scoring dimension
- [ ] Step 5: Enforce minimum: ≥2-3 drops visible even in slow weeks (ranker transparency)
```

## Scoring rubric

| Dimension | Weight | Range |
|---|---|---|
| intuition_density_fit | 3.0 | high=10, medium=5, low=0 |
| goal_alignment | 2.0 | full-match=10, partial=5, none=2, anti-aligned=-3 |
| dedup_penalty | 2.0 | NEW=+5, OVERLAPS seed=+2, OVERLAPS draft=0, OVERLAPS published=-2 (unless reinforcement_angle strong) |
| source_reliability | 1.0 | essential=10, optional=6, aggregator=4 |
| freshness | 1.0 | in-window=10, republished=5, older=2 |

Threshold for keep: score > 30.

## Worked example

Candidate: Karpathy microgpt (teaches GPT internals in 200 lines, in window).

- intuition_density_fit: 10 × 3 = 30 (high)
- goal_alignment: 10 × 2 = 20 (matches "intuition-first" explicitly)
- dedup_penalty: +5 × 2 = 10 (NEW)
- source_reliability: 10 × 1 = 10 (essential)
- freshness: 10 × 1 = 10 (in window)
- **Total: 80 → keep, high rank**

Candidate: "OpenAI announces GPT-5.5" release post.

- intuition_density_fit: 0 × 3 = 0
- goal_alignment: 2 × 2 = 4
- dedup_penalty: +5 × 2 = 10
- source_reliability: 4 × 1 = 4
- freshness: 10 × 1 = 10
- **Total: 28 → drop. Reason: capability announcement; no mechanism taught.**

## Guardrails

1. Never let freshness outweigh intuition-density. Freshness is a tiebreaker.
2. Never keep more than 10.
3. Never drop all items from a single essential source two weeks in a row without surfacing "this source may be stale" for `update-watchlist`.
4. Never drop an item solely for source weight 4 — good content from unknown sources matters.
5. Always produce drops. Zero drops in a week with >5 candidates = ranker failure.

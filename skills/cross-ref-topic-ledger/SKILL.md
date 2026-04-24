---
name: cross-ref-topic-ledger
description: For each Trend Scout candidate item, checks substacker shared-context/topic-ledger.md and tags with NEW | OVERLAPS seed:{slug} | OVERLAPS draft:{slug} | OVERLAPS published:{slug}. Adds a reinforcement_angle note for items overlapping with published posts ("external confirmation of X"). Read-only against the ledger. Use after summarize-signal, before rank-by-user-fit. Trigger keywords: cross-ref, ledger check, overlap, reinforcement, dedup external.
---

# Cross-Ref Topic Ledger

## Workflow

```
Per candidate:
- [ ] Step 1: Parse topic-ledger.md into {slug, title, status, tags, last_touched} records
- [ ] Step 2: Extract 2-5 topic tags from the candidate's summary (reuse ledger vocabulary)
- [ ] Step 3: Match candidate to ledger entries by tag overlap (≥2 shared tags) OR semantic title similarity
- [ ] Step 4: Classify: NEW | OVERLAPS seed:{slug} | OVERLAPS draft:{slug} | OVERLAPS published:{slug}
- [ ] Step 5: If OVERLAPS published, generate reinforcement_angle (1 line)
- [ ] Step 6: Annotate candidate with dedup_status, overlap_slug, reinforcement_angle
```

## Classification rules

- **NEW**: tag overlap <2 AND title similarity <0.4.
- **OVERLAPS seed:{slug}**: writer has a seed on this; mention is context but NOT a new seed candidate.
- **OVERLAPS draft:{slug}**: writer is actively working on this; may absorb external evidence.
- **OVERLAPS published:{slug}**: writer already shipped on this; becomes reinforcement material for future posts.

### Reinforcement angle

When OVERLAPS published: generate a one-line angle the writer could use in a future post.

Example:
- Candidate: Transformer Circuits — "Attention as Soft Nearest-Neighbor Lookup"
- Overlaps: published `attention-as-kernel-regression`
- Reinforcement angle: "Anthropic's interp team came at this from circuits; I came at it from kernel regression — same answer."

## Guardrails

1. **Read-only.** Never mutate the ledger. Never propose ledger edits here.
2. If ledger is stale (>60 days since last touch), emit a warning in digest appendix.
3. Borderline matches → prefer `NEW`; false negatives (a missed overlap) are worse UX than false positives (a buried genuine thread).
4. Reinforcement angles are drafts — writer refines on use. Keep ≤1 sentence.
5. Never cross-reference with `corpus/dead/` — dead ideas should stay dead for Trend Scout's purposes.

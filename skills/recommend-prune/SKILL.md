---
name: recommend-prune
description: Recommends structural cleanups for the substacker section map — sections to retire, sections to merge, posts to reassign. Applies under-filled, stale, and overlapping heuristics. Writes proposals with reasons-to-reject (steelman counter). Does not execute. Use once per Curator run, after drift audit. Trigger keywords: prune, retire section, merge sections, reassign post, cleanup.
---

# Recommend Prune

## Three cleanup categories

1. **Retire**: section with <2 posts added in 3 months AND no new cluster signal → candidate for retirement.
2. **Merge**: two sections whose promises overlap >60% semantically OR whose post-sets have >40% cross-fit → merge candidate.
3. **Reassign**: posts from `audit-drift` flagged as genuine-drift → suggest target section or move to `unassigned`.

## Workflow

```
Per Curator run:
- [ ] Step 1: For each section, check retire conditions
- [ ] Step 2: Cross-check section promises for merge candidates
- [ ] Step 3: Collect reassignment candidates from drift audit
- [ ] Step 4: For each proposal: write reasoning + reasons-to-reject
- [ ] Step 5: Emit three lists (retire / merge / reassign)
```

## Guardrails

1. Never delete. Only retire (mark status: retired, keep in map).
2. Never merge without the merge proposal fully visible in review artifact (both original promises preserved verbatim).
3. Never recommend pruning a provisional section in its first 2 cycles — give it probation time.
4. Reasons-to-reject are mandatory for every proposal. Writer needs the counter-argument pre-built.

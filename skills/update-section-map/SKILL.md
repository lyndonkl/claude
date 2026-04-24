---
name: update-section-map
description: Writes the canonical substacker shared-context/section-map.md after writer confirmation of review-artifact proposals. Atomic write with backup snapshot. Validates schema before writing. Use as the final step of a Curator run, only after writer has accepted/modified proposals. Trigger keywords: update section map, write section map, commit sections, apply changes.
---

# Update Section Map

## Workflow

```
After writer confirms review proposals:
- [ ] Step 1: Snapshot current section-map.md to ops/curator/snapshots/YYYY-MM-DD-section-map.md
- [ ] Step 2: Apply confirmed changes: add / rename / merge / retire / reassign
- [ ] Step 3: Sort sections by `Established` date (oldest first for stable ordering)
- [ ] Step 4: Validate schema (every post in exactly one section or unassigned; every section has promise; retired sections preserved)
- [ ] Step 5: Write new section-map.md
- [ ] Step 6: Update the last_updated timestamp + changelog entry
```

## Schema validation rules

- Every post appears in exactly one section OR in `unassigned`. No double-assignment.
- Every section has: `slug`, `promise`, `fit_confidence`, `established`, `posts`.
- Retired sections stay in map under `## Retired sections` with `retired: YYYY-MM-DD` and `reason`.
- Max 5 non-retired sections. If >5, abort and flag.

## Guardrails

1. Snapshot before every write.
2. Validate schema before writing. If invalid, bubble error; don't write partial.
3. Never delete retired-section entries.
4. Changelog entry on every write (single line with YYYY-MM-DD + summary of changes).
5. Atomic: read → snapshot → validate → write. Single operation.

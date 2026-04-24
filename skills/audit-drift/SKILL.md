---
name: audit-drift
description: Checks every post currently assigned to a substacker section against that section's promise and flags posts that no longer fit. Distinguishes acceptable-stretch (minor) from borderline (surface for review) from genuine-drift (violates promise). Never reassigns automatically — only flags. Use on every Curator run where at least one section already exists. Trigger keywords: drift, drift audit, section fit, promise violation, post in wrong section.
---

# Audit Drift

## Workflow

```
Per section in section-map:
- [ ] Step 1: Load section's promise
- [ ] Step 2: For each assigned post, score fit against promise
- [ ] Step 3: Tag: acceptable-stretch | borderline | genuine-drift
- [ ] Step 4: If >2 posts in one section are "genuine-drift", also flag the section's PROMISE as a rewrite candidate
- [ ] Step 5: Emit per-post verdict list
```

## Three levels

- **Acceptable-stretch**: post stretches the promise but doesn't break it. Note only.
- **Borderline**: post is at the edge. Surface for writer review; consider reassignment.
- **Genuine-drift**: post violates the promise. Reassign candidate OR trigger section-promise rewrite.

## Guardrails

1. Never reassign automatically. Only flag.
2. When >2 posts in one section drift, prefer rewriting the section's promise over reassigning posts (usually the promise was too narrow, not the writer too drifting).
3. Fit-scoring is intuitive, not algorithmic — based on whether the reader subscribed for THIS would expect THIS post.
4. Retired sections are excluded from drift checks.

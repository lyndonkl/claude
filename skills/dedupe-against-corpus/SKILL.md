---
name: dedupe-against-corpus
description: Checks a candidate seed against the existing substacker corpus (seeds, drafts, published) for exact duplicates (sha256 fingerprint) and near-duplicates (title Jaccard, first-200-word Jaccard, shared topic cluster). Exact match exits as SKIPPED. Near-match links via related_seeds rather than creating a duplicate. Use after topic tagging and density scoring, before writing the seed. Trigger keywords: dedupe, duplicate, already thought, near-match, related seed, fingerprint.
---

# Dedupe Against Corpus

## Table of Contents

- [Three tiers of match](#three-tiers-of-match)
- [Workflow](#workflow)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by `ingest-inbox-item` step 4. Queried ad-hoc by `search-corpus`. Backlinks into matched seeds (the one place this skill writes outside new seeds).

## Three tiers of match

1. **Tier 1 — Exact fingerprint**: sha256 of body matches an existing seed's fingerprint. → `SKIPPED`.
2. **Tier 2 — Title similarity**: normalized Jaccard on title tokens ≥ 0.7. → `LINK` candidate.
3. **Tier 3 — Content similarity**: for seeds sharing ≥2 topic tags, first-200-word Jaccard ≥ 0.5. → `LINK` candidate.

Tier 2 and 3 candidates are unioned (up to 3 total LINK targets).

## Workflow

```
Dedupe one candidate seed:
- [ ] Step 1: Grep all corpus/**/*.md frontmatter for fingerprint match
- [ ] Step 2: If exact match, return SKIPPED
- [ ] Step 3: Normalized title Jaccard against all existing seeds
- [ ] Step 4: For seeds sharing ≥2 topic tags, first-200-word Jaccard
- [ ] Step 5: Union tier-2 and tier-3 candidates, cap at 3
- [ ] Step 6: If any LINK candidates, return LINK with related_seeds list; else CREATE
- [ ] Step 7: For LINK, Edit matched seeds' related_seeds to add this candidate's id
```

### Step 7: Backlink safely

The matched seeds get their `related_seeds` field extended (append, never replace) ONLY IF:
- `manual_edits: false` on the matched seed, OR
- The edit is strictly additive (appending an id to a list is always safe).

Do not touch any other field on the matched seed.

## Worked example

**Candidate**: new seed about "dropout as ensemble" with topics `[regularization, ensembling, dropout]`, first 200 words describing thinned-network averaging.

**Existing corpus**:
- `2026-03-11-l2-as-gaussian-prior` — topics `[regularization, bayesian]`. Title Jaccard = 0.1 (different). Shared tags: 1. Skip content-similarity check.
- `2026-02-08-bagging-in-deep-nets` — topics `[regularization, ensembling]`. Shared tags: 2. First-200-word Jaccard: 0.51 → LINK candidate.

**Output**: `{action: LINK, related_seeds: [2026-02-08-bagging-in-deep-nets]}`.

Side effect: `corpus/seeds/2026-02-08-bagging-in-deep-nets.md` gets its `related_seeds` appended with the new seed's id.

## Guardrails

1. Never merge, rewrite, or delete. Only link. Merging is the writer's call.
2. Never alter an existing seed's body. Only its `links.related_seeds` field.
3. Never cross-link into `corpus/dead/` — dead ideas stay dead.
4. Fingerprint is over the body only (not frontmatter). Retagging must not change fingerprint.
5. The 3-link cap prevents unbounded link chains.
6. Never propose LINK across `status: published` to `status: seed` — published posts are immutable except for typo fixes.

## Quick reference

- Returns one of: `SKIPPED`, `LINK`, `CREATE`.
- LINK can carry up to 3 related-seed ids.
- Side effect: backlinks into matched seeds (additive).

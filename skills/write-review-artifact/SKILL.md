---
name: write-review-artifact
description: Composes the final Technical Reviewer artifact at ops/technical-reviewer/YYYY-MM-DD-{slug}-review.md. Enforces frontmatter schema, section order (Summary → Blockers → Claims → Boundary-Break Suggestions → Glossary Alignment → Could-Not-Verify → Research Log), go/no-go decision rule, and never-modify-draft principle. Use exactly once per Technical Reviewer run as the last step. Trigger keywords: write review, technical review artifact, compose review, claim review output.
---

# Write Review Artifact

## Output schema

```yaml
---
agent: technical-reviewer
version: 1.0
draft_path: corpus/drafts/{slug}.md
draft_sha256: {hash}
reviewed_at: ISO8601
topic_hint: {string or null}
total_claims: N
counts:
  simplified-correct: N
  simplified-boundary: N
  wrong: N
  contested: N
  overclaim: N
blockers: N                              # count of wrong claims
glossary_alignment_notes: N
go_no_go: GO | GO-WITH-HEDGES | NO-GO
timebox_used_hours: N.N
---
```

## Body sections (exact order, no exceptions)

1. `## Summary` — one paragraph, plain English, counts + verdict.
2. `## Blockers` — every `wrong` claim, numbered, excerpt + why-wrong + primary source + suggested fix. Empty section if zero.
3. `## Claims` — full per-claim table: #, excerpt, location, classification, confidence, primary_source, action, note.
4. `## Boundary-Break Suggestions` — for every `simplified-boundary`.
5. `## Glossary Alignment` — terms where writer's glossary diverges from field. Empty if zero.
6. `## Could-Not-Verify` — claims where primary source was paywalled / unreachable / not findable.
7. `## Research Log` — queries run, sources fetched, time spent. Audit trail.

## Go/no-go rule (mechanical)

- `blockers = count(wrong)`
- If `blockers > 0` → `NO-GO`.
- Else if `contested + overclaim > 0` → `GO-WITH-HEDGES`.
- Else → `GO`.

## Guardrails

1. Never emit GO if blockers > 0.
2. Never omit Could-Not-Verify section, even empty — an empty section is the positive signal.
3. Never modify the draft. Only write to the review path.
4. `draft_sha256` recorded to detect re-runs on a changed draft.
5. Body sections in the exact order above. No interleaving.
6. Overwrite if re-run on the same date for the same slug; append `-v2` suffix if running a second time after a revision.

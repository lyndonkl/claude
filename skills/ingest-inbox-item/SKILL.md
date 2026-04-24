---
name: ingest-inbox-item
description: Ingests a single file from the substacker inbox/ into corpus/seeds/ as a normalized markdown seed with full frontmatter. Orchestrates format normalization, topic tagging, intuition-density scoring, dedupe, changelog, ledger update, and inbox-file move to .processed/. Use when the user drops raw material into inbox/ and runs /ingest, at session start, or whenever a single inbox file needs to become an indexed seed. Trigger keywords: ingest, inbox, new note, new transcript, new highlight, index this, add to corpus.
---

# Ingest Inbox Item

## Table of Contents

- [Workflow](#workflow)
- [Frontmatter schema](#frontmatter-schema)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)
- [Related skills](#related-skills)

**Related skills:** Uses `normalize-format`, `tag-by-topic`, `score-intuition-density`, `dedupe-against-corpus`, `update-topic-ledger`. Called by the Librarian agent for each file in `inbox/`.

## Workflow

Copy this checklist and track progress per file:

```
Ingest one inbox file:
- [ ] Step 0: Compute sha256 of file body; check .librarian-state.json for duplicate fingerprint
- [ ] Step 1: Invoke normalize-format → body + partial frontmatter
- [ ] Step 2: Invoke tag-by-topic → topics + pending_tags
- [ ] Step 3: Invoke score-intuition-density → score + signals
- [ ] Step 4: Invoke dedupe-against-corpus → CREATE | LINK | SKIPPED
- [ ] Step 5: If LINK, backlink matched seeds' related_seeds field
- [ ] Step 6: Write seed file with full frontmatter; status=seed; manual_edits=false
- [ ] Step 7: Append one line to corpus/seeds/.changelog.md
- [ ] Step 8: Invoke update-topic-ledger for each topic tag
- [ ] Step 9: mv inbox file → inbox/.processed/
- [ ] Step 10: Update .librarian-state.json with the fingerprint
```

**Step 0**: Hash the body (not frontmatter). If the fingerprint is in `.librarian-state.json`, exit with `SKIPPED (already ingested: <seed-id>)`. Idempotency is a feature.

**Step 1**: `normalize-format` handles all supported formats (plain markdown, `.jsonl` Claude Code sessions, `.json` Claude.ai exports, Readwise exports, transcripts with speaker labels, link captures). Returns one or more `{body, partial_frontmatter}` pairs — multi-chunk outputs possible for long transcripts.

**Step 2**: `tag-by-topic` proposes 1–4 tags from the controlled vocabulary. If none match, it logs to `topic-ledger.md#pending-tags` and still assigns the closest existing tag.

**Step 3**: `score-intuition-density` computes 0–10 from 8 explicit signals. Auditable.

**Step 4**: `dedupe-against-corpus` returns one of `SKIPPED` (exact fingerprint match — exit), `LINK` (near-match — proceed but write `related_seeds`), or `CREATE` (no match).

**Step 6**: Write the seed file. Location: `corpus/seeds/{id}.md` where `id = YYYY-MM-DD-slugified-title`. If a seed with that `id` already exists, append `-v2` rather than overwrite.

**Step 7**: Changelog format: `YYYY-MM-DDThh:mm | ADDED | {seed-id} | from {original_path} | density={N} | topics={comma-list}`

## Frontmatter schema

```yaml
---
id: 2026-04-23-dropout-as-ensemble-thinned-networks
title: "Dropout as ensemble over thinned networks"
created: 2026-04-21T09:14:00-07:00
source:
  type: inbox-note
  original_path: inbox/2026-04-21-dropout-as-ensemble.md
  ingested_at: 2026-04-23T14:32:01-07:00
  fingerprint: sha256:7c1d...
topics: [regularization, ensembling, dropout]
intuition_density:
  score: 8
  signals: [analogy_present, concrete_worked_example, counterfactual_offered, reframe_against_default, biology_to_ai]
status: seed
provenance:
  author: kushal
  confidence: owned
links:
  related_seeds: [2026-03-11-l2-as-gaussian-prior]
  parent_source: null
section_affinity: [agent-workshop]
word_count: 87
manual_edits: false
---

[body: preserved verbatim from normalize-format output]
```

## Worked example

**Input**: `inbox/2026-04-21-dropout-as-ensemble.md` (87 words, plain markdown, user's own note).

**Run**:
- Step 0: fingerprint new → proceed.
- Step 1: normalize-format → body unchanged (plain markdown); title from first line or filename.
- Step 2: tag-by-topic → `[regularization, ensembling, dropout]`; `dropout` new → logged to pending-tags.
- Step 3: score → 8; signals fired: analogy_present, concrete_worked_example, counterfactual_offered, reframe_against_default, biology_to_ai.
- Step 4: dedupe → near-match `2026-03-11-l2-as-gaussian-prior` at Jaccard 0.32 (below 0.5 threshold) → CREATE (not LINK).
- Step 6: Write `corpus/seeds/2026-04-21-dropout-as-ensemble-thinned-networks.md` with full frontmatter.
- Step 7: Changelog: `2026-04-23T14:32 | ADDED | 2026-04-21-dropout-as-ensemble-thinned-networks | from inbox/2026-04-21-dropout-as-ensemble.md | density=8 | topics=regularization,ensembling,dropout`
- Step 8: Ledger: `regularization` seeds 3→4, temperature→hot; `ensembling` 1→2; `dropout` new row added.
- Step 9: `mv inbox/2026-04-21-dropout-as-ensemble.md inbox/.processed/`
- Step 10: Append fingerprint to state.

**Output**: one seed file, one changelog line, three ledger updates, one moved file.

## Guardrails

1. If `normalize-format` fails, the inbox file stays put (not moved) and the changelog records `ERROR | <file> | <reason>`. No partial ingests.
2. If topic-tagger proposes a tag not in the controlled vocabulary that cannot map to one, log to pending-tags — never silently invent.
3. If a seed with the candidate `id` exists, append `-v2`; never overwrite.
4. Never ingest files under `inbox/.processed/` or `inbox/.trash/`.
5. Run single-threaded. Parallel ingests corrupt the ledger and changelog.
6. If `dedupe-against-corpus` returns `SKIPPED`, move the inbox file to `.processed/` with a renamed suffix `-duplicate-of-{matched-seed-id}` and exit — don't re-write the matched seed.

## Quick reference

- **Idempotent**: yes (fingerprint check in step 0).
- **Writes**: one seed file + one changelog line + ledger updates + one moved inbox file + state update.
- **Failure mode**: format error halts the pipeline for that one file; other files continue.

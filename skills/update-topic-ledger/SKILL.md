---
name: update-topic-ledger
description: Maintains substacker shared-context/topic-ledger.md as an append-and-update index of all topics in the corpus. Each topic row tracks seed/draft/published counts, last-touched date, top-3 seed ids by density, and a hot/warm/cold temperature indicator. Use after any seed is created, promoted to draft, published, or killed. Trigger keywords: ledger, topic index, update index, topic ledger, hot/cold topics.
---

# Update Topic Ledger

## Table of Contents

- [Ledger row schema](#ledger-row-schema)
- [Workflow](#workflow)
- [Temperature rules](#temperature-rules)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by `ingest-inbox-item` step 8 for each topic on a new seed. Called by any status-changing agent on promote/publish/kill events.

## Ledger row schema

Each topic gets a block in `shared-context/topic-ledger.md`:

```markdown
## {topic-slug}
- seeds: N
- drafts: N
- published: N
- last_touched: YYYY-MM-DD
- temperature: hot | warm | cold
- top_seeds:
  - {seed-id} (density={N})
  - {seed-id} (density={N})
  - {seed-id} (density={N})
```

## Workflow

```
Update ledger for one topic + event:
- [ ] Step 1: Read the ledger; find or create the row for {topic}
- [ ] Step 2: Update counts based on event (ADDED | PROMOTED | PUBLISHED | KILLED)
- [ ] Step 3: Update last_touched = today
- [ ] Step 4: Recompute temperature
- [ ] Step 5: Recompute top_seeds = top 3 by density across all statuses except dead
- [ ] Step 6: Write the updated row back
```

### Step 2: Event → count change

| Event | seeds | drafts | published | dead |
|---|---|---|---|---|
| `ADDED` (new seed) | +1 | — | — | — |
| `PROMOTED` (seed → draft) | -1 | +1 | — | — |
| `PUBLISHED` (draft → published) | — | -1 | +1 | — |
| `KILLED` (any → dead) | -1, 0, 0 (whichever bucket) | -1 | -1 | +1 |

## Temperature rules

- `hot`: `last_touched` within last 14 days.
- `warm`: `last_touched` 14–60 days ago.
- `cold`: `last_touched` >60 days ago.

Temperature is computed, not stored — recompute on every update.

## Worked example

**Event**: `{topic: regularization, event: ADDED, seed_id: 2026-04-21-dropout-as-ensemble-thinned-networks, density: 7}`

**Existing row**:
```
## regularization
- seeds: 3
- drafts: 1
- published: 1
- last_touched: 2026-03-11
- temperature: warm
- top_seeds:
  - 2026-03-11-l2-as-gaussian-prior (density=6)
  - 2025-11-14-noise-as-regularization (density=5)
  - 2025-09-22-weight-decay-intuition (density=4)
```

**Updated row**:
```
## regularization
- seeds: 4
- drafts: 1
- published: 1
- last_touched: 2026-04-21
- temperature: hot
- top_seeds:
  - 2026-04-21-dropout-as-ensemble-thinned-networks (density=7)
  - 2026-03-11-l2-as-gaussian-prior (density=6)
  - 2025-11-14-noise-as-regularization (density=5)
```

## Guardrails

1. Never remove a topic row even if count drops to 0. Mark `temperature: cold` to preserve historical signal.
2. Never promote a pending tag to canonical silently. The writer reviews `#pending-tags`; this skill only updates rows for tags already in canonical.
3. Temperature is recomputed every time, not stored. If today differs from last_touched, the temperature reflects today.
4. `top_seeds` excludes dead seeds. A seed promoted from seed → draft retains its density score.
5. Never re-order rows alphabetically in bulk — preserve whatever order the ledger is in (last-touched DESC is the current convention).
6. Single-threaded. The Librarian serializes calls so the ledger doesn't race.

## Quick reference

- Input: `{topic: str, event: str, seed_id: str, density: int}`.
- Output: updated `topic-ledger.md`.
- Side effect: single file write with diff-style edit.

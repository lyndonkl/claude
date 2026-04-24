---
name: sweep-stale-seeds
description: Identifies substacker seeds older than 30 days with status=seed and no incoming related_seeds links, flags them for writer review, and recommends keep / promote-to-draft / kill based on density score. Does NOT auto-execute any action. Emits a review list to ops/librarian/YYYY-MM-DD-stale-sweep.md. Run at session start after ingest, once per day max. Trigger keywords: stale, sweep, review, old seeds, cleanup, gardener, corpus hygiene.
---

# Sweep Stale Seeds

## Table of Contents

- [Workflow](#workflow)
- [Recommendation rules](#recommendation-rules)
- [Output format](#output-format)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by Librarian agent's pipeline step 2. Output consumed by the writer and by `curator` on its monthly-ish cycle.

## Workflow

```
Sweep the corpus for stale seeds:
- [ ] Step 1: If ops/librarian/{today}-stale-sweep.md exists, skip (daily idempotency)
- [ ] Step 2: Glob corpus/seeds/*.md
- [ ] Step 3: For each seed, parse frontmatter
- [ ] Step 4: Apply stale criteria: status=seed AND created < today-30d AND no related_seeds referencing this seed
- [ ] Step 5: For each stale seed, compute recommendation
- [ ] Step 6: Write the review list to ops/librarian/{today}-stale-sweep.md
```

### Step 4: Stale criteria

A seed is stale if ALL of:
- `status: seed` (not yet promoted to draft)
- `created` is > 30 days before today
- No other seed's `related_seeds` includes this seed's id (orphan test)
- `manual_edits: false` (writer-edited seeds are never in the sweep)

## Recommendation rules

| If... | Recommend |
|---|---|
| `density >= 7` | `promote-to-draft` (high-quality material sitting stale is the real loss) |
| `density <= 3` | `kill` (low-density AND stale = not going to improve) |
| else | `keep` (mid-density — more time to mature) |

## Output format

`ops/librarian/YYYY-MM-DD-stale-sweep.md`:

```yaml
---
agent: librarian
date: YYYY-MM-DD
total_seeds: N
stale_seeds: M
recommendations:
  promote: X
  kill: Y
  keep: Z
---

# Stale Seed Sweep — YYYY-MM-DD

## Promote to draft (X)

- `{seed-id}` | density={N} | created={date} | topics={comma-list}
  - Rationale: high density, sitting stale. Consider promoting.

## Kill (Y)

- `{seed-id}` | density={N} | created={date} | topics={comma-list}
  - Rationale: low density, stale, orphan. Safe to move to corpus/dead/.

## Keep (Z)

- `{seed-id}` | density={N} | created={date} | topics={comma-list}
  - Rationale: mid-density, give it more time.
```

## Worked example

Corpus today (2026-04-23) has 47 seeds. Globbing + filtering finds 6 stale:

```
## Promote to draft (1)
- 2026-02-18-residuals-as-a-reset-button | density=8 | created=2026-02-18 | topics=resnet, training
  - Rationale: high density, sitting stale for 2 months. Consider promoting.

## Kill (2)
- 2026-01-04-maybe-writing-about-tokenizers | density=2 | created=2026-01-04 | topics=tokenizer
  - Rationale: low density, stale, orphan. Safe to move to corpus/dead/.
- 2025-12-21-quick-thought-on-sparse-moe | density=3 | created=2025-12-21 | topics=moe
  - Rationale: low density, stale, orphan. Safe to kill.

## Keep (3)
- 2026-02-28-rope-intuition | density=5 | created=2026-02-28 | topics=attention-mechanism, rope
- 2026-03-05-grokking | density=5 | created=2026-03-05 | topics=emergence, training
- 2026-03-15-temperature-vs-top-p | density=6 | created=2026-03-15 | topics=sampling
  - Rationale: mid-density; not stale enough to act yet.
```

## Guardrails

1. Never delete. Only flag. The writer or Curator executes.
2. Never change `status`. The status field is owned by the writer / downstream agents.
3. Never include seeds with `manual_edits: true` in the kill list regardless of density.
4. One-time per day: if today's sweep file exists, skip.
5. A seed linked from another seed's `related_seeds` is never stale by this skill's criteria, even if old and low-density.
6. Never recommend `kill` for a seed with `density >= 7`; that would contradict the promote recommendation.

## Quick reference

- Runs once per session (skip if today's file exists).
- Output: one markdown report. No file deletions.
- Criteria: status=seed + >30 days + orphan + manual_edits=false.

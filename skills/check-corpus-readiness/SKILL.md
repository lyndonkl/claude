---
name: check-corpus-readiness
description: Checks whether the substacker corpus has enough material to justify a Curator run. Counts published posts, time-gates against the last review, and reports go/no-go with the specific gate that failed. Use before any Curator run, and on cold start to decide whether to propose sections yet. Trigger keywords: readiness, corpus ready, gate check, cadence gate, pre-flight.
---

# Check Corpus Readiness

## Gates

- Minimum 28 days since last Curator review (`ops/curator/YYYY-MM-DD-review.md`).
- Minimum 4 new published posts since last review.
- Cold start: `section-map.md` empty requires ≥10 posts in `corpus/published/**`.

## Output

```python
{
  "ready": bool,
  "gate_failed": str or None,          # which gate, if any
  "days_elapsed": int,
  "new_posts": int,
  "total_posts": int,
  "rationale": str
}
```

## Worked example

- Corpus has 21 posts. Last review 2026-03-10 (44 days ago). New posts since: 5. → `{ready: true, gate_failed: None, ...}`.
- Corpus has 15 posts. Last review 2026-04-05 (18 days ago). → `{ready: false, gate_failed: "28-day-floor", days_elapsed: 18, ...}`. Skip this run.
- Cold start, corpus has 9 posts. → `{ready: false, gate_failed: "cold-start-10-post-floor", ...}`. Abort.

## Guardrails

1. Abort if corpus has shrunk. Posts disappearing is not a Curator concern.
2. A user-invoked early run still reports `ready: false` with a too-recent warning in the output, but doesn't block. Writer decides.
3. First step of every Curator run. If this fails, all other skills skip.

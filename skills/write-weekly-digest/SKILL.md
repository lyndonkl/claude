---
name: write-weekly-digest
description: Renders the Trend Scout ranked keep-and-drop lists into ops/trend-scout/YYYY-WW-digest.md using the agent voice profile and including an appendix of all sources surveyed. Use once per weekly run as the terminal skill. Trigger keywords: weekly digest, write digest, Trend Scout digest, Saturday morning digest.
---

# Write Weekly Digest

## Workflow

```
Compose digest:
- [ ] Step 1: Load ranked keep list + drop list
- [ ] Step 2: Fill frontmatter
- [ ] Step 3: Render top-signals section (≤10 items)
- [ ] Step 4: Render explicit-drops section
- [ ] Step 5: Render appendix (every source surveyed + freshness state)
- [ ] Step 6: Voice-profile lint: no banned vocabulary; one-sentence paragraphs at pivots
- [ ] Step 7: Write ops/trend-scout/YYYY-WW-digest.md
```

## Output format

```markdown
---
week: YYYY-WW
generated: ISO8601
items_surveyed: N
items_kept: K (≤10)
items_dropped: D (explicit, with reasons)
---

# Week {WW} Digest — YYYY-MM-DD through YYYY-MM-DD

## Top signals ({K})

### 1. {Source} — {Title}
- URL: {full URL}
- Why this matters: {1-line teaches-X summary}
- Dedup: NEW | OVERLAPS {status}:{slug}
- Seed candidate: YES: {angle} | NO: {reason}
- Reading time: {N} min

### 2. ...

## Explicit drops ({D})
- {URL}: {1-line reason}
- ...

## Appendix: all sources surveyed
- {source}: {fresh | stale | failed} + one-line note
- ...
```

## Guardrails

1. Hard cap 10 keeps.
2. Never publish with 0 drops in a week where >5 items were fetched.
3. Appendix is mandatory — audit trail.
4. Voice-profile lint catches banned vocabulary before writing.
5. Idempotent: running twice in one week overwrites deterministically.
6. Every "Why this matters" is the `summary` from `summarize-signal`, not a rewrite.

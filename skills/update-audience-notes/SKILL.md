---
name: update-audience-notes
description: Appends one structured YAML observation block to substacker shared-context/audience-notes.md iff the week produced at least one observation with confidence ≥ medium. Includes supporting evidence (post slugs + numbers) and reviewed_by_curator flag. Never rewrites or deletes prior entries. Append-only discipline protects downstream agents' shared context. Use at the end of each weekly pipeline after write-weekly-report. Trigger keywords: audience notes, append observation, audience insight, confidence-rated.
---

# Update Audience Notes

## Workflow

```
At end of weekly pipeline:
- [ ] Step 1: Review attribution outputs for any pattern observed
- [ ] Step 2: Filter to confidence ≥ medium only (low is never appended)
- [ ] Step 3: Format as YAML block per schema
- [ ] Step 4: Append to shared-context/audience-notes.md
- [ ] Step 5: If no medium+ observation this week, log "no additions this week" to weekly report's data-caveats (not to audience-notes)
```

## YAML block schema

```yaml
- date: YYYY-MM-DD
  week: YYYY-WW
  observation: >
    {plain English, ideally testable}
  confidence: medium | high
  evidence:
    - slug: {post-slug}
      metric: {value}
      baseline: {value}
  reviewed_by_curator: false
```

## Example entries

```yaml
- date: 2026-06-01
  week: 2026-W22
  observation: >
    External restack from a larger ML account on Substack Notes is
    the strongest sub-acquisition channel observed to date —
    +49 subs from a single post vs ~+4 baseline, with 71% of the
    new cohort landing in "active" tier immediately.
  confidence: high
  evidence:
    - slug: why-your-embedding-search-melted-at-10pm
      open_rate: 0.61
      click_rate: 0.12
      baseline_open: 0.49
      baseline_click: 0.05
      new_subs: 49
      active_tier_of_new_subs: 35
      external_restacks_observed: 2
  reviewed_by_curator: false
```

## Guardrails

1. **Append-only.** Never rewrite or delete prior entries. Entries stand.
2. **Confidence floor: medium.** Low-confidence observations stay in the weekly report body; never enter shared context.
3. **Evidence required.** Every observation cites at least 2 posts (or 1 post + 1 external datum) with specific numbers.
4. **`reviewed_by_curator: false`** on append; Curator flips to `true` on its next monthly review.
5. Never append an observation identical to a prior entry. Dedupe by the `observation` field's content.
6. If >2 medium+ observations in one week, append all of them as separate blocks.
7. Individual subscriber info (email, name) never in evidence — aggregate counts only.

## Quick reference

- Append-only writes.
- Confidence floor: medium.
- Evidence: ≥2 posts / data points with numbers.
- Fires once per week at pipeline end; may write 0, 1, or 2+ blocks.

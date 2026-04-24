---
name: per-section-tracking
description: Breaks down weekly and trailing-4-week substacker performance per Substack section, keyed on section tags in corpus/published/ and section-map.md. Reports opens, clicks, subs-attributable-to-section per section with ≥3 posts. Skips if section-map has <2 sections. Feeds Curator with pruning candidates (sections with 4-week median z ≤ -1.0). Use when section-map has ≥2 live sections. Trigger keywords: per-section, section performance, section metrics, section pruning, differential engagement.
---

# Per Section Tracking

## Workflow

```
Per week (if ≥2 sections with ≥3 posts each):
- [ ] Step 1: Load section-map.md
- [ ] Step 2: Join CSV posts with corpus/published/{section}/ to map each post to section
- [ ] Step 3: Compute per-section aggregates (mean open rate, click rate, views/send, subs delta)
- [ ] Step 4: Compute trailing 4-week per-section z-score
- [ ] Step 5: Flag sections with median z ≤ -1.0 over 4 weeks → candidate for Curator prune proposal
- [ ] Step 6: Emit per-section table for the weekly report
```

## Skip rule

- If section-map has <2 sections → skip, note "sections not yet established."
- If a section has <3 posts → exclude from per-section table; show in note: "{section} has <3 posts, not enough for section-level stats."

## Output format (weekly-report subsection)

```markdown
## Per section

| Section | Posts (week / total) | Open rate (week / 4w baseline) | Click rate (week / 4w baseline) | Sub delta | 4w z |
|---|---|---|---|---|---|
| kalshi-log | 2 / 6 | 0.54 / 0.51 | 0.06 / 0.05 | +8 | +0.7 |
| agent-workshop | 0 / 7 | — | — | +2 | +0.2 |
```

Narrative: 1-2 sentences per section summarizing what the numbers say (not interpretation — that's attribute-performance's job).

## Guardrails

1. Skip entirely if section-map empty or only one section.
2. Skip any section with <3 posts.
3. Never compare across sections' absolute numbers ("agent-workshop has higher open rate than kalshi-log"). Audiences differ; compare each to its own baseline.
4. Section pruning flag is advisory — surfaces to Curator, Curator decides.
5. Per-section z-scores use same IQR-based method as global baseline.
6. Don't attribute causes in this skill (that's attribute-performance). Only describe the numbers.

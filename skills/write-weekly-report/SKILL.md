---
name: write-weekly-report
description: Composes the substacker final ops/growth-analyst/YYYY-WW-report.md from ingest + baseline + attribute + per-section + public-page outputs. Enforces 400-800 word budget, YAML frontmatter schema, seven-section body structure. Truncates weakest sections first when over budget. Injects data-caveats from any degraded-mode flags upstream. Use as the final compose step of the weekly pipeline. Trigger keywords: weekly report, compose report, growth report, Monday report.
---

# Write Weekly Report

## Workflow

```
Compose weekly report:
- [ ] Step 1: Receive outputs from all upstream skills
- [ ] Step 2: Draft YAML frontmatter (week, coverage, csv_source, subs, baselines, one_number_to_watch, confidence)
- [ ] Step 3: Draft body in 7 sections (see format)
- [ ] Step 4: Count words; if >800, truncate weakest sections first
- [ ] Step 5: Voice-check pass (no vanity phrases, no AI-slop openers)
- [ ] Step 6: Write file
```

## Output schema

```markdown
---
week: YYYY-WW
reported_on: YYYY-MM-DD
coverage: YYYY-MM-DD to YYYY-MM-DD
publication: the-thinkers-notebook
csv_source: inbox/substack-stats/substack-stats-YYYY-MM-DD.csv
subscribers_start: N
subscribers_end: N
delta_subscribers: N
open_rate_week: 0.NN
open_rate_baseline_4w: 0.NN
click_rate_week: 0.NN
click_rate_baseline_4w: 0.NN
posts_sent_this_week: N
one_number_to_watch: subscribers
confidence: high | medium | low
---

## Headline
1-2 sentences. The single thing worth knowing.

## Numbers in context
Subs, delta, open rate, click rate paired with 4-week rolling. No external comparisons.

## What worked / what didn't
Per outlier post: plain-English attribution with confidence label.

## Per section
Only if sections populated. Table + 1-2 sentence narrative per section.

## Hypothesis for next week
1-2 specific, falsifiable things to test.

## Data caveats
Missing columns, low-N warnings. Mandatory — say "no caveats" if empty.
```

## Word budget

Target 400–800 words. Hard ceiling 800.

Truncation priority (drop first if over 800):
1. Per-section narrative (keep table; drop prose)
2. Data caveats (keep 1-line summary; move detail to a linked stub)
3. Numbers in context (tighten to single table)
4. Attribution (keep outliers, drop near-baseline posts)

## Voice rules

- No "went viral" / "crushed it" / "blew up" / "massive week"
- Use "overperformed by Xσ" / "breakout post" / "high-z outlier"
- Anti-vanity framing throughout
- `confidence: high` is rare — earn it with ≥2 channels converging

## Guardrails

1. Hard cap 800 words.
2. Every section present even if empty — mandatory schema.
3. No narrative where the underlying numbers are noise. In a quiet week, "A quiet, in-baseline week — nothing moved meaningfully" is the honest story.
4. Data caveats section is always present.
5. Voice-check pass before writing.
6. Frontmatter fields required: week, subscribers_start, subscribers_end, open/click rate + baselines, one_number_to_watch, confidence.

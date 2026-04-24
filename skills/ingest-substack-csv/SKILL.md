---
name: ingest-substack-csv
description: Loads and validates a weekly Substack CSV stats export for the substacker Growth Analyst. Reconciles header against expected-columns schema, parses post rows + subscriber aggregates, moves file into corpus/stats/ on success, emits schema-warning stub on header drift. Never reads subscriber emails row-by-row — aggregates only. FALLBACK path when fetch-substack-stats (Chrome automation) is unavailable. Use when a CSV appears in inbox/substack-stats/, when Chrome is not logged in, or when the writer prefers manual export. Trigger keywords: CSV, Substack export, stats export, schema validation, subscriber data, manual export, CSV fallback.
---

# Ingest Substack CSV

## Workflow

```
Per weekly CSV:
- [ ] Step 1: Read header row; diff against .schema-expected.json
- [ ] Step 2: If load-bearing column missing, halt + emit schema-warning stub
- [ ] Step 3: Parse post rows (load-bearing: views, opens, open_rate, clicks, sent, post_date)
- [ ] Step 4: Parse subscribers aggregate (total, free/paid distribution, activity tiers) — NEVER row-by-row emails
- [ ] Step 5: Emit typed WeekExport object
- [ ] Step 6: On success, move CSV into corpus/stats/YYYY-WW.csv
```

## Expected schema

Posts CSV columns (load-bearing in bold):
**id, slug, title, post_date, views, opens, open_rate, clicks, click_through_rate, sent**, delivered, signups_within_1_day, subscriptions_within_1_day, unsubscribes_within_1_day, signups, subscribes, shares, estimated_value, engagement_rate, reaction_count, comment_count

Subscribers CSV (handled separately, never ingested row-by-row): email, created_at, subscription_type, activity_tier, email_opens_last_30_days, email_opens_last_7_days.

## Schema drift

If a load-bearing column is missing:
- Write `ops/growth-analyst/YYYY-WW-schema-warning.md` with the header diff.
- Halt the pipeline.
- Prompt the writer: "Substack may have changed its export format. Review the diff; update `.schema-expected.json` if confirmed."

New columns (additions) are accepted silently. Removals of non-load-bearing columns produce a soft note but don't halt.

## Output: WeekExport

```python
{
  "subscribers_end": int,
  "delta_subscribers": int,
  "posts": [ {slug, title, post_date, views, opens, open_rate, clicks, sent, ...} ],
  "sends_this_week": int,
  "free_subs": int,
  "paid_subs": int,
  "activity_tier_distribution": {active, at-risk, churned}
}
```

## Guardrails

1. Never read subscriber-CSV row-by-row. Aggregate reductions only.
2. Halt on load-bearing column loss; stub the warning.
3. New columns → accept silently; note in data-caveats later.
4. Subscriber CSV is deleted from `inbox/` after 7 days (privacy posture).
5. Tolerate naming variants (underscore vs hyphen vs missing date) — warn, don't hard-fail.

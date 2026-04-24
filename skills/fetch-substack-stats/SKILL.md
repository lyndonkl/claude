---
name: fetch-substack-stats
description: Pulls substacker's weekly Substack stats directly from the dashboard via Claude-in-Chrome browser automation. Navigates to substack.com/stats, parses the posts table and subscribers table, and produces the same typed WeekExport object that ingest-substack-csv produces — but without requiring a manual CSV export. The writer keeps Chrome signed in to Substack; this skill opens the dashboard in a new tab, reads the rendered stats, closes the tab. Primary data path for the Growth Analyst; ingest-substack-csv is the fallback when browser automation is unavailable. Trigger keywords: fetch stats, Substack dashboard, auto stats, Chrome stats, dashboard scrape, live stats, no CSV.
---

# Fetch Substack Stats (Chrome automation)

## Table of Contents

- [Prerequisites](#prerequisites)
- [Workflow](#workflow)
- [Output](#output)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Primary alternative to `ingest-substack-csv`. Produces the same `WeekExport` contract so downstream skills (`compute-baseline`, `attribute-performance`, `per-section-tracking`) don't care which path produced the data.

## Prerequisites

- **Chrome logged in to Substack** as the publication owner (one-time manual setup by the writer).
- **Claude-in-Chrome** MCP tools available: `tabs_context_mcp`, `tabs_create_mcp`, `navigate`, `get_page_text`, `read_page`, optionally `javascript_tool`.
- Publication URL known: `https://thethinkersnotebook.substack.com/publish/stats` (the dashboard URL shape — verify on first run).

## Workflow

```
Per weekly run (Mondays) or on-demand:
- [ ] Step 1: tabs_context_mcp — inspect existing tabs; if a Substack stats tab is already open, reuse; else tabs_create_mcp
- [ ] Step 2: navigate to https://substack.com/publish/stats (or publication-specific dashboard URL)
- [ ] Step 3: get_page_text on the rendered dashboard; parse:
    - Total subscribers (headline number)
    - Weekly delta
    - Posts table with columns: title, date, opens, open rate, clicks, CTR, views, sent
    - Activity-tier distribution (free / paid, active / at-risk / churned)
- [ ] Step 4: For each post in the last 7 days, also navigate to the individual post stats page for:
    - Referral sources breakdown
    - Post-specific engagement
- [ ] Step 5: Normalize into WeekExport object (schema matches ingest-substack-csv's output)
- [ ] Step 6: Archive the scraped stats as CSV in corpus/stats/YYYY-WW.csv (so historical baseline works identically)
- [ ] Step 7: Close the Substack tab (do NOT leave stats pages open in the user's browser)
```

### Step 4 detail — referral sources

Substack exposes referral source breakdowns only on individual post stats pages. The scraper navigates to each outlier post (|z| ≥ 1.0 candidate, determined after baseline compute — so this step may be deferred to `attribute-performance`) to pull referral data. For non-outliers, per-post referral is skipped.

## Output

Same schema as `ingest-substack-csv`:

```python
{
  "subscribers_end": int,
  "delta_subscribers": int,
  "posts": [
    {"slug", "title", "post_date", "views", "opens", "open_rate", "clicks", "sent", ...}
  ],
  "sends_this_week": int,
  "free_subs": int,
  "paid_subs": int,
  "activity_tier_distribution": {...},
  "source": "chrome-scrape",  # vs. "csv-export" from the other skill
  "scraped_at": ISO8601
}
```

Written to `corpus/stats/YYYY-WW.csv` (same archive path as CSV imports). The `source` field marks provenance so the writer can tell at a glance whether a week came from live scrape or manual export.

## Worked example

**Trigger**: Monday morning, Growth Analyst invokes `fetch-substack-stats`.

1. `tabs_context_mcp` — no existing Substack tab.
2. `tabs_create_mcp` + `navigate` → Substack dashboard stats page.
3. `get_page_text` — reads:
   - Total subscribers: **148**
   - Weekly delta: **+6**
   - Posts table (last 7 days): 1 post shown, "Attention is a routing problem", 680 views, 48% open, 5% CTR.
4. For the one post, `navigate` → post-specific stats → referral breakdown shows 60% direct, 20% Notes, 20% search.
5. Normalize: `WeekExport{subscribers_end: 148, delta_subscribers: 6, posts: [...], ...}`.
6. Write `corpus/stats/2026-W17.csv`.
7. Close the Substack tab.

Downstream pipeline (`compute-baseline`, `attribute-performance`, etc.) runs identically whether data came from CSV or scrape — the WeekExport contract is stable.

## Guardrails

1. **Idempotent within a week.** If `corpus/stats/{YYYY-WW}.csv` already exists for today's ISO week, compare — don't overwrite unless the scrape is strictly more recent and differs meaningfully.
2. **Close tabs on exit.** Do not leave stats pages open in the user's browser; they are distracting.
3. **Fallback to CSV cleanly.** If any step fails (login expired, dashboard URL changed, page structure shifted), emit `fetch-substack-stats FAILED: {reason}; falling back to ingest-substack-csv` and halt — let the writer decide whether to retry or drop a manual CSV.
4. **Never log individual subscriber emails** even though the dashboard subscriber list is visible. Aggregate counts and activity-tier distributions only. Matches the CSV path's privacy posture.
5. **Do not navigate anywhere except Substack dashboard URLs.** No side-trips.
6. **Do not auto-install or update Claude-in-Chrome.** If the MCP tools are unavailable, return a specific error ("claude-in-chrome not available; user must enable").
7. **Respect soft rate limits.** One scrape per week is the default; catch-up mode may run up to 4 if the writer missed multiple weeks, but always space them at least 30 seconds apart.
8. **Never take actions on the dashboard.** No clicking "Delete", no editing post metadata, no unsubscribing anyone. Read-only.
9. **Session state hygiene.** If login has expired, do not attempt to log in on the writer's behalf. Halt with `login-required` message; writer handles auth manually.

## Quick reference

- Browser-automation replacement for manual CSV export.
- Same WeekExport contract → downstream pipeline identical.
- Archives to `corpus/stats/YYYY-WW.csv` on success.
- Fallback: `ingest-substack-csv` if browser path fails.
- Read-only — never takes actions on the dashboard.

---
name: fetch-public-page-stats
description: Uses WebFetch to pull publicly visible subscriber count and per-post public view count from substacker's Substack archive page and individual post URLs. Supplements the CSV when subscriber-count field is stale (>24h old) or when a post has public shares not yet reflected. Rate-limited to ≤10 fetches per invocation. Use when CSV subscribers-end field may have drifted or when external-share attribution needs a public signal. Trigger keywords: public stats, Substack public page, subscriber count check, post views supplement, WebFetch.
---

# Fetch Public Page Stats

## Workflow

```
Supplement CSV with public-page data:
- [ ] Step 1: WebFetch https://thethinkersnotebook.substack.com/ → extract subscriber count
- [ ] Step 2: Compare to csv.subscribers_end; if delta > 5% OR CSV export >24h old, flag as `public > csv`
- [ ] Step 3: For each post with |z| ≥ 1.0 (outliers), WebFetch the post URL
- [ ] Step 4: Extract public "N views" counter; compare to CSV views
- [ ] Step 5: Return {subscribers_public, post_deltas: [...]}
- [ ] Step 6: Cap: ≤10 WebFetch calls per invocation
```

## Use cases

- CSV export was Monday morning; a post went viral Monday afternoon. Public page shows 1380 views; CSV shows 1240. Delta +140 in 6 hours supports external-share attribution.
- Writer forgot to export but wants an unofficial check. Public subscriber count is the best available signal.
- Attribute-performance wants a verification signal for external-share hypothesis.

## Guardrails

1. **Cap at 10 WebFetch calls.** Substack soft-throttles.
2. Never fetch more than the public homepage + outlier-post URLs. No scraping.
3. If WebFetch fails or returns stale, note in data-caveats and proceed with CSV-only.
4. Don't use this skill to replace the CSV. It supplements. CSV is primary.
5. Public view counts can differ from CSV views (CSV counts "opens" + Apple-pixel pre-fetch; public counts visits). Report both, don't pretend they're the same metric.

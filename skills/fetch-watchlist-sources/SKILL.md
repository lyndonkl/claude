---
name: fetch-watchlist-sources
description: Fetches the last 7 days of updates from every entry in the substacker Trend Scout watchlist — blogs, paper aggregators (arXiv, Hugging Face papers), social feeds. Returns normalized {title, url, author, published, excerpt, source_type} tuples. Use at the start of a weekly Trend Scout run. Trigger keywords: watchlist, fetch sources, weekly fetch, last 7 days, source normalization.
---

# Fetch Watchlist Sources

## Workflow

```
At start of weekly Trend Scout run:
- [ ] Step 1: Parse ops/trend-scout/watchlist.md; group by source_type
- [ ] Step 2: For each blog: WebFetch archive URL; extract posts from last 7 days
- [ ] Step 3: For each paper aggregator: WebFetch the listing URL; filter to last 7 days
- [ ] Step 4: For each X account / subreddit: WebFetch the public URL
- [ ] Step 5: Normalize each item
- [ ] Step 6: Deduplicate by URL
- [ ] Step 7: Write .cache/YYYY-WW-raw.jsonl
```

## Guardrails

1. Cap: 60 URLs per run. If watchlist is longer, run in two passes + flag.
2. Back off on 429s; retry each source at most twice.
3. Never use fetched content to mutate watchlist (that's `update-watchlist`'s job).
4. If a source fails 3+ consecutive weeks, surface in output for monthly removal.
5. Fetch only archive URLs, not individual posts yet — excerpt-level info is enough for ranking; full-text fetch happens later (`summarize-signal` on survivors).

## Watchlist bootstrap (35 entries seeded on activation)

Stored in `ops/trend-scout/watchlist.md` on Trend Scout's first real run. Starter set clustered by type:

- **Blogs (intuition-first)**: colah's blog, Lil'Log, Jay Alammar, Karpathy, Distill, Gwern, Sasha Rush, Chip Huyen, Neel Nanda.
- **Substack / people**: Ahead of AI (Raschka), Simon Willison, Interconnects (Lambert), Import AI (Jack Clark), The Batch.
- **Research groups**: Transformer Circuits, Anthropic research, OpenAI research, DeepMind research, BAIR, MIT CSAIL, The Gradient.
- **Paper aggregators**: arXiv cs.LG recent, arXiv cs.CL recent, Hugging Face Daily Papers, Papers with Code, DAIR.AI.
- **Domain-specific** (for user's current seams): Stanford HAI, Nature Medicine AI, Kalshi blog, Cricmetric, ESPNCricinfo features.
- **Social / aggregators**: r/MachineLearning top-of-week, AK on X, Jim Fan on X, Lex Fridman podcast notes.

~15 marked `essential: true`, ~20 `essential: false` (sampled).

## Quick reference

- 7-day window (+1 day slop for timezones).
- Cap 60 URLs per run.
- Output: `.cache/YYYY-WW-raw.jsonl`.

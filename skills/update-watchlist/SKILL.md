---
name: update-watchlist
description: Proposes adds and removes to the Trend Scout watchlist based on consecutive-failure sources, repeated-reference external authors, and user-added feedback markers. Emits a proposed diff at ops/trend-scout/watchlist-proposed-diff.md for user review. On explicit approval, applies the diff. Monthly cadence. Trigger keywords: watchlist update, add source, remove source, watchlist review, monthly review, source pruning.
---

# Update Watchlist

## Workflow

```
Monthly (first weekly run of the month):
- [ ] Step 1: Read last 4-8 weekly digests' appendices
- [ ] Step 2: Identify sources with ≥3 consecutive fetch failures (remove candidates)
- [ ] Step 3: Identify external authors/URLs referenced by watchlist sources ≥3 times in a month (add candidates)
- [ ] Step 4: Parse any user-added markers in digest bodies (<!-- scout: drop-this-source --> / <!-- scout: add {url} -->)
- [ ] Step 5: WebFetch each proposed add to validate it returns content
- [ ] Step 6: Emit ops/trend-scout/watchlist-proposed-diff.md
- [ ] Step 7: On user approval (.approved file or explicit trigger), apply diff; append changelog to watchlist.md
```

## Proposed diff format

```diff
# Watchlist changes proposed 2026-W17

+ ## people
+ - name: "Interconnects (Nathan Lambert)"
+   url: https://www.interconnects.ai/archive
+   source_type: blog
+   essential: false
+   rationale: "Referenced 6x in last 4 weeks from Raschka, Willison, Transformer Circuits."

- ## blogs
- - name: "someblog"
-   url: https://someblog.example/
-   source_type: blog
-   rationale: "4 consecutive fetch failures."
```

## Guardrails

1. Never add without WebFetch validation.
2. Never remove `essential: true` sources without explicit user approval.
3. Cap adds at 3 per month. Prevents drift.
4. Preserve clustered structure (blogs / people / research / aggregators / domain / social).
5. Changelog entry appended to watchlist.md on every apply.
6. Monthly only. Don't run weekly.

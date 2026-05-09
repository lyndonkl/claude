---
name: fetch-preprint-recent
description: Fetches preprints posted to bioRxiv or medRxiv within a given date window, then keyword-filters the results client-side. Wraps the public `api.biorxiv.org/details/{server}/{from}/{to}/{cursor}` endpoint, handles cursor pagination, normalizes records to a stable shape (doi, title, authors, abstract, date, server, version, url), and applies a keyword-OR match against title + abstract. Domain-neutral — usable for any biology / clinical preprint scan, not just one project. Use when user mentions bioRxiv, medRxiv, weekly preprint scan, fetch preprints, last-N-days preprints, or when a literature-scan agent needs structured preprint records.
---

# fetch-preprint-recent

Fetch preprints from bioRxiv or medRxiv for a date window, normalize the records, and keyword-filter them.

## Workflow

```
- [ ] Step 1: Validate inputs (server, from, to, keywords)
- [ ] Step 2: Page through the details endpoint until messages.cursor exhausted
- [ ] Step 3: Normalize each record to the canonical shape
- [ ] Step 4: Dedupe within the window (keep latest version per DOI)
- [ ] Step 5: Keyword-filter on lowercased title + abstract
- [ ] Step 6: Return matched records + a summary (total fetched, total matched, pages fetched)
```

**Step 1 — Validate inputs**

Required:
- `server`: one of `biorxiv` or `medrxiv` (the API uses these literal strings)
- `from`: `YYYY-MM-DD`, inclusive
- `to`: `YYYY-MM-DD`, inclusive, must be ≥ `from`
- `keywords`: list of strings; may include multi-word phrases; case-insensitive matching

Reject if window > 31 days (the API supports it but you almost never want to dump a month of preprints in one call without a stronger filter — flag and confirm).

**Step 2 — Page through the endpoint**

The endpoint is:

```
https://api.biorxiv.org/details/{server}/{from}/{to}/{cursor}
```

- Start with `cursor=0`.
- The response shape is:
  ```json
  {
    "messages": [{"status": "ok", "interval": "2026-05-04/2026-05-10", "cursor": "0", "count": 100, "total": 327}],
    "collection": [ { record }, { record }, ... ]
  }
  ```
- After consuming `collection`, increment `cursor` by 100 (the page size is fixed) and refetch until `cursor + count >= total`.
- Cap pages at 20 (2,000 records) as a safety; if you hit the cap, surface a "window may be over-broad" warning and return what you have.

Use WebFetch with the URL. If WebFetch returns malformed JSON or a 5xx, retry once with a 2-second backoff; on second failure, return partial results with a `fetch_errors` field listing the failed cursors.

**Step 3 — Normalize each record**

The API returns fields like `doi, title, authors, author_corresponding, author_corresponding_institution, date, version, type, license, category, jatsxml, abstract, published, server`. Reduce to:

```json
{
  "id": "10.1101/2026.05.07.123456",          // doi
  "title": "...",
  "authors": ["Smith J", "Doe A", ...],        // split the API's `authors` string on `;`
  "abstract": "...",
  "date": "2026-05-07",
  "server": "biorxiv",                          // or "medrxiv"
  "version": 1,
  "category": "neuroscience",                   // bioRxiv subject area
  "url": "https://www.biorxiv.org/content/10.1101/2026.05.07.123456v1",
  "published_doi": null                         // populated if the preprint has been published; from `published` field
}
```

URL pattern: `https://www.{server}.org/content/{doi}v{version}` (no `https://doi.org/` redirect — direct to the preprint server keeps the abstract page accessible).

**Step 4 — Dedupe within the window**

The same DOI can appear with multiple `version` values if the authors revised mid-window. Keep the highest version per DOI. Drop the rest.

**Step 5 — Keyword-filter**

For each kept record, check whether any keyword (or phrase) appears in `lowercase(title + " " + abstract)`. Match logic:

- Multi-word keyword like `"protein language model"` → must appear as a contiguous substring.
- Single-word keyword like `"crispr"` → must appear with word boundaries (don't match `"crisper"`).
- OR across all keywords (paper kept if any keyword matches).

Track which keyword(s) matched per paper — downstream `paper-relevance-filter` will use that signal.

**Step 6 — Return**

Return a payload like:

```json
{
  "server": "biorxiv",
  "window": "2026-05-04/2026-05-10",
  "fetched_total": 327,
  "matched_total": 14,
  "pages_fetched": 4,
  "fetch_errors": [],
  "records": [ {normalized record + "matched_keywords": [...]} , ... ]
}
```

Cache the raw API JSON (pre-normalization) to the agent's `.cache/` directory under `{YYYY-WW}-{server}.json` so a re-run can skip the network if the user wants to re-synthesize without re-fetching.

## Common Patterns

**Pattern A — One server, one window**: standard call. Use this in a weekly digest.

**Pattern B — Multi-week catch-up**: call once per week, never one giant 28-day window. The cursor pagination is fine but the keyword filter is more honest at weekly granularity (matches the way papers are released and discussed).

**Pattern C — Preprint-only follow-up of a known paper**: if you already have a DOI, do not use this skill. Use a direct WebFetch on `https://api.biorxiv.org/details/{server}/{doi}` instead.

## Guardrails

1. **Don't fetch without a window.** "Recent" must always resolve to specific `from`/`to` dates before the call.
2. **Don't keyword-filter server-side** — the API doesn't support it; attempting via URL params silently returns everything.
3. **Don't trust the abstract field to be present.** Some entries have empty abstracts; treat those as title-only matches and flag in the output.
4. **Don't dedupe across servers in this skill.** Cross-server dedupe (bioRxiv ↔ medRxiv ↔ PubMed) belongs to the calling agent, not here.
5. **Don't transform DOIs.** Keep them as-returned; downstream tools rely on the exact `10.1101/...` string.
6. **Don't claim "no papers" on a fetch error.** Distinguish "fetched and filtered to zero" from "fetch failed." The first is a thin week; the second is a bug.

## Quick Reference

| Field          | Source                                                        | Notes                                                           |
| -------------- | ------------------------------------------------------------- | --------------------------------------------------------------- |
| Endpoint       | `api.biorxiv.org/details/{server}/{from}/{to}/{cursor}`       | Same host serves both bioRxiv and medRxiv; only `{server}` varies |
| Auth           | None                                                          | Public API. Be polite — don't hammer.                           |
| Page size      | 100, fixed                                                    | Cursor is the offset into the window's results                  |
| Window cap     | 31 days (soft); 7 days is the typical weekly call             | Wider windows = thousands of records before keyword filter       |
| Rate limit     | Not formally documented; ~1 req/sec is safe                   | Backoff on 5xx                                                  |
| URL pattern    | `https://www.{server}.org/content/{doi}v{version}`            | Linkable to abstract page                                        |
| Server values  | `biorxiv`, `medrxiv`                                          | Case-sensitive in path                                           |

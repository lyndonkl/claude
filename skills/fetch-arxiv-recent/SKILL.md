---
name: fetch-arxiv-recent
description: Fetches arXiv papers submitted within a given date window matching a keyword set, with optional restriction to one or more arXiv categories (e.g. cs.LG, cs.CL, cs.CV, stat.ML, math.ST, q-bio.QM). Wraps the public `export.arxiv.org/api/query` endpoint, parses Atom XML, handles pagination, and normalizes records to the same canonical shape as `fetch-preprint-recent` and `fetch-pubmed-recent` so a calling agent can dedupe across sources. Domain-neutral — usable for any literature scan that crosses CS, ML, statistics, math, physics, or quantitative biology. Use when user mentions arXiv, cs.LG, ML papers, NeurIPS-adjacent preprints, weekly arXiv scan, or when a literature-scan agent needs arXiv records alongside bioRxiv / medRxiv / PubMed.
---

# fetch-arxiv-recent

Fetch arXiv papers submitted within a date window, optionally restricted to specific arXiv categories, and keyword-filter the results. Returns records in the same canonical shape as the other three literature fetchers.

## Workflow

```
- [ ] Step 1: Validate inputs (from, to, keywords, optional categories)
- [ ] Step 2: Build the search_query string with date range + categories + keywords
- [ ] Step 3: Page through the API until results exhausted or window endpoint passed
- [ ] Step 4: Parse Atom XML; normalize each entry
- [ ] Step 5: Dedupe by arXiv ID (keep latest version)
- [ ] Step 6: Return matched records + summary
```

**Step 1 — Validate inputs**

Required:
- `from`: `YYYY-MM-DD`, inclusive
- `to`: `YYYY-MM-DD`, inclusive, `to >= from`
- `keywords`: list of strings (case-insensitive substring match against title + abstract)

Optional:
- `categories`: list of arXiv category codes — e.g. `["cs.LG", "cs.CL", "stat.ML"]`. If omitted, search all of arXiv. Common groupings the caller may want to expose:
  - **CS / ML**: `cs.LG, cs.CL, cs.CV, cs.AI, cs.NE, stat.ML`
  - **Math / stats**: `math.ST, math.PR, math.OC, stat.ME, stat.AP`
  - **Quantitative biology**: `q-bio.QM, q-bio.GN, q-bio.MN, q-bio.NC`
  - **Physics-adjacent**: `physics.data-an, cond-mat.stat-mech`

  The skill itself does not hard-code these groupings; it accepts whatever categories the caller passes. The orchestrator's `source-registry.md` can document the groupings the operator cares about.

Reject if window > 31 days (same rule as `fetch-preprint-recent` — wider windows almost always indicate a misuse).

**Step 2 — Build the query string**

The arXiv search API accepts a query language with fielded search. Compose:

```
search_query = (date_clause) AND (category_clause)? AND (keyword_clause)
```

- **Date clause** (always include — without it you'll get the whole arXiv history):
  ```
  submittedDate:[YYYYMMDDHHMM TO YYYYMMDDHHMM]
  ```
  Use `from + 0000` and `to + 2359` so the window is fully inclusive of both days.

- **Category clause** (optional): join categories with OR.
  ```
  (cat:cs.LG OR cat:cs.CL OR cat:stat.ML)
  ```

- **Keyword clause**: join with OR. Use `all:` for full-record search (covers title + abstract + authors, which is what we want for a wide-net keyword scan):
  ```
  (all:"protein language model" OR all:"diffusion model" OR all:gnn)
  ```
  Multi-word phrases must be double-quoted. Single words don't need quotes.

Final assembled example:
```
submittedDate:[202605040000 TO 202605102359]
  AND (cat:cs.LG OR cat:cs.CL OR cat:stat.ML)
  AND (all:"protein language model" OR all:"diffusion model" OR all:transformer)
```

URL-encode and pass as `search_query` to:

```
http://export.arxiv.org/api/query?search_query={URL_ENCODED}&sortBy=submittedDate&sortOrder=descending&start={offset}&max_results=200
```

`sortBy=submittedDate&sortOrder=descending` is important — it lets you stop paginating as soon as the result dates fall before `from`, instead of having to walk the whole result set.

**Step 3 — Pagination**

arXiv returns 200 records per page (max). After each page:
- If response has 0 entries, stop.
- If the *last* entry's `published` date is older than `from`, stop (the rest are out of window).
- Otherwise, increment `start` by 200, request again.
- Cap at 10 pages (2,000 records). If hit, surface "window may be over-broad" and return what you have.

Rate limit: arXiv asks for **1 request every 3 seconds**. Sleep between paginated requests. Don't hammer.

**Step 4 — Parse Atom XML**

The API returns an Atom feed. Each `<entry>` has:
- `<id>`: full URL like `http://arxiv.org/abs/2605.12345v1` — the canonical paper ID is the trailing `2605.12345` (post-2007 format) or `arxiv.org/abs/cs.LG/0301001` (legacy format)
- `<title>`: paper title (may have newlines + indentation; collapse whitespace)
- `<summary>`: abstract (same whitespace caveat)
- `<author><name>`: one per author; preserve order
- `<published>`: ISO timestamp of v1 submission (use this as `date`)
- `<updated>`: ISO timestamp of latest version (different if revised)
- `<arxiv:primary_category term="cs.LG">`: primary category
- `<category term="..."/>`: list of all categories
- `<link rel="alternate" type="text/html" href="..."/>`: abstract page URL
- `<link title="pdf" rel="related" type="application/pdf" href="..."/>`: PDF URL
- `<arxiv:doi>`: optional, present once paper is published in a journal

If the Atom parser fails, retry the request once with a 5-second backoff. On second failure, log the error to `fetch_errors` and skip the page.

**Step 5 — Dedupe by arXiv ID**

The paginated results may include the same paper twice if a v2 was submitted within the window. Keep the highest version per ID.

The arXiv ID alone (e.g. `2605.12345`) is the canonical key — strip the `v1`/`v2` suffix from the URL and use that.

**Step 6 — Normalize and return**

Same canonical record shape as the other fetchers:

```json
{
  "id": "arxiv:2605.12345",                                   // arxiv-prefixed for source clarity
  "title": "...",
  "authors": ["Smith J", "Doe A", ...],
  "abstract": "...",
  "date": "2026-05-07",                                       // YYYY-MM-DD parsed from <published>
  "server": "arxiv",
  "primary_category": "cs.LG",
  "categories": ["cs.LG", "stat.ML"],
  "version": 2,
  "doi": "10.1145/...",                                       // if present, otherwise null
  "url": "https://arxiv.org/abs/2605.12345",                  // abstract page (preferred for digest links)
  "pdf_url": "https://arxiv.org/pdf/2605.12345.pdf",
  "matched_keywords": ["protein language model"]
}
```

Apply the keyword filter client-side (the API's `all:` is full-record OR but doesn't preserve the match-keyword info). For each record, check title + abstract against the keyword list, populate `matched_keywords`, and drop records that match none (the API's recall is broader than the operator's intent — the skill must filter).

Return summary:

```json
{
  "server": "arxiv",
  "window": "2026-05-04/2026-05-10",
  "categories": ["cs.LG", "cs.CL", "stat.ML"],
  "query": "(...full search_query...)",
  "fetched_total": 1240,
  "matched_total": 18,
  "pages_fetched": 7,
  "fetch_errors": [],
  "records": [ ... ]
}
```

Cache the raw Atom XML responses (one per page) to `.cache/{YYYY-WW}-arxiv-{page}.xml`.

## Common Patterns

**Pattern A — CS-only weekly scan**: `categories=["cs.LG", "cs.CL", "cs.CV", "cs.AI", "stat.ML"]`. The default for an ML/CS-leaning watchlist.

**Pattern B — Cross-disciplinary scan (CS + quant-bio)**: `categories=["cs.LG", "stat.ML", "q-bio.QM", "q-bio.GN"]`. When the operator wants computational-biology preprints from arXiv that bioRxiv may miss.

**Pattern C — All of arXiv**: `categories=None`. Maximum recall, maximum noise. Only useful when the keyword filter is very tight.

**Pattern D — Track a specific arXiv account**: outside this skill's default scope. Add `(au:"Smith, J" OR au:"Doe, A")` to the search_query as an additional AND clause.

## Guardrails

1. **Always include the date clause.** Without `submittedDate:[... TO ...]` arXiv returns the entire history of the matching query — millions of records. This is the single most common arXiv-API mistake.
2. **Sort by submittedDate descending.** Otherwise you cannot bail out of pagination early when the dates fall out of window — you'd have to walk the whole result set.
3. **Respect the 3-second rate limit.** arXiv enforces it loosely but consistent abuse triggers IP-level throttling. Sleep 3s between paginated requests.
4. **Don't trust the `<title>` and `<summary>` whitespace.** Atom feeds often contain literal `\n` plus 6 spaces of indentation. Collapse all internal whitespace runs to single spaces before storing.
5. **Don't conflate the `id` URL with the canonical ID.** `<id>http://arxiv.org/abs/2605.12345v2</id>` — the canonical ID is `2605.12345`. The `v2` is the version suffix; strip it for dedupe.
6. **Don't drop the legacy ID format silently.** Pre-2007 arXiv IDs look like `cs.LG/0301001`. The skill should accept both formats, never assert the modern one. Match `^[a-z-]+\.[A-Z]+/\d+$|^\d{4}\.\d{4,5}$` to validate.
7. **Don't dedupe across sources here.** A paper on arXiv may also be on bioRxiv (for cross-listing) or have a PubMed publication — that's the calling agent's job, not this skill's.
8. **Don't expand keywords automatically.** arXiv's full-record `all:` search is already broad; further synonym expansion silently widens the net. The watchlist is the gate.

## Quick Reference

| Field          | Source                                                       | Notes                                                         |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------- |
| Endpoint       | `http://export.arxiv.org/api/query?search_query={q}&...`     | HTTPS works too but the docs use HTTP                         |
| Auth           | None                                                         | Public API. Use a User-Agent header if WebFetch lets you set one. |
| Page size      | 200 max (`max_results=200`)                                  |                                                               |
| Rate limit     | 1 request / 3 seconds                                        | Sleep between paginated requests                              |
| Window cap     | 31 days (soft); 7 days for weekly digests                    |                                                               |
| Date format    | `YYYYMMDDHHMM` (no dashes, no colons)                        | Use `0000` for `from`, `2359` for `to`                        |
| ID format      | `2605.12345` (post-2007), `cs.LG/0301001` (legacy)           | Strip `vN` suffix from the URL; canonical ID excludes version |
| Canonical URL  | `https://arxiv.org/abs/{id}`                                 | Abstract page; preferred for digest links                     |
| PDF URL        | `https://arxiv.org/pdf/{id}.pdf`                             | Optional secondary link                                       |
| Sort           | `sortBy=submittedDate&sortOrder=descending`                  | Required for early-bail pagination                            |
| Common cats    | `cs.LG, cs.CL, cs.CV, cs.AI, stat.ML, math.ST, q-bio.QM`     | Operator decides; skill takes any list                        |

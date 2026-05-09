---
name: fetch-pubmed-recent
description: Fetches PubMed articles posted in a given date window matching a keyword set, returning normalized records (PMID, title, authors, abstract, journal, date, DOI, URL). Uses NCBI E-utilities (`esearch` + `esummary` + `efetch`) via WebFetch for portability, but prefers a PubMed MCP server's `search_articles` + `get_article_metadata` tools when one is connected (faster, paginated, parsed). Builds date-bounded queries with optional MeSH expansion. Domain-neutral - usable for any PubMed scan, not just one project. Use when user mentions PubMed, NCBI, last-N-days PubMed, weekly PubMed scan, MeSH search, or when a literature-scan agent needs structured PubMed records.
---

# fetch-pubmed-recent

Fetch PubMed records for a date window + keyword set. Normalize the output to the same shape as `fetch-preprint-recent` so a calling agent can dedupe across sources.

## Workflow

```
- [ ] Step 1: Detect transport — prefer PubMed MCP if available, else E-utilities via WebFetch
- [ ] Step 2: Build the keyword query with explicit date bounds
- [ ] Step 3: Execute search → list of PMIDs (page if > 100)
- [ ] Step 4: Fetch metadata + abstracts for each PMID batch
- [ ] Step 5: Normalize records to canonical shape
- [ ] Step 6: Return matched records + summary
```

**Step 1 — Detect transport**

At session start the runtime exposes any connected MCP servers. Check whether tools matching `mcp__*PubMed*__search_articles` and `mcp__*PubMed*__get_article_metadata` are available.

- **MCP available**: use it. The MCP wraps the same E-utilities but handles pagination and field extraction. Pass the keyword query as the search string with the date filter appended (see Step 2).
- **MCP not available**: fall back to direct E-utilities calls via WebFetch. Endpoints:
  - Search: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmode=json&retmax=200`
  - Summary: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmids_csv}&retmode=json`
  - Abstract: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmids_csv}&rettype=abstract&retmode=xml`

Both transports return the same downstream shape. The skill caller should not need to care which was used (record `transport_used` in the return summary so debugging is possible).

**Step 2 — Build the date-bounded query**

PubMed accepts boolean keyword expressions plus a date filter. The canonical date filter for "papers indexed in PubMed during this window" is:

```
("YYYY/MM/DD"[PDAT] : "YYYY/MM/DD"[PDAT])
```

`PDAT` is the publication date — the most stable choice for a weekly digest. (`EDAT` is the entry-into-PubMed date, useful if you want "newly indexed even if old"; `MHDA` is the MeSH-indexed date. Default `PDAT`.)

For each watchlist keyword, expand into a sub-query:

- Plain term: `"protein language model"[Title/Abstract]`
- Term + MeSH: `("Alzheimer Disease"[MeSH] OR "alzheimer's disease"[Title/Abstract])` — only when the keyword has a clean MeSH match the caller has confirmed; do not auto-MeSH-expand or you'll widen the net unpredictably.

Combine sub-queries with OR, then AND the date filter:

```
(("term1"[Title/Abstract]) OR ("term2"[Title/Abstract]) OR ...) AND ("2026/05/04"[PDAT] : "2026/05/10"[PDAT])
```

Watch out for special characters — escape `()` inside terms by quoting the term.

**Step 3 — Execute search**

Call the search tool. Expected output is a list of PMIDs and a count.

If `count > 200`, page: rerun the search with `retstart=200`, `retstart=400`, etc. Cap at 1,000 PMIDs (5 pages). If a 7-day window matches more than 1,000 records, the keyword set is too broad — surface this and ask the calling agent to tighten.

**Step 4 — Fetch metadata + abstracts**

Batch the PMIDs (200 per esummary call). Pull:

- PMID
- Title
- Authors (full list — keep in order; `et al.` truncation is the digest's job, not this skill's)
- Journal name (`fulljournalname`)
- Publication date (`pubdate`, `sortpubdate`)
- DOI (`articleids[].idtype == 'doi'`)
- Abstract (separate `efetch` call with `rettype=abstract` since esummary doesn't return abstracts)

Abstract fetch is the slow part. Batch 100 PMIDs at a time. If abstract fetch fails for a record, keep it but with `abstract: null` and a `warnings` flag.

**Step 5 — Normalize**

Same canonical shape as `fetch-preprint-recent`:

```json
{
  "id": "PMID:39123456",                                  // PMID-prefixed for source clarity
  "title": "...",
  "authors": ["Smith J", "Doe A", ...],
  "abstract": "...",
  "date": "2026-05-07",                                   // YYYY-MM-DD parsed from pubdate
  "server": "pubmed",
  "journal": "Nature Biotechnology",
  "doi": "10.1038/s41587-026-12345-6",                    // if present
  "url": "https://pubmed.ncbi.nlm.nih.gov/39123456/",
  "matched_keywords": ["protein language model"]
}
```

URL pattern: `https://pubmed.ncbi.nlm.nih.gov/{pmid}/` — the canonical PubMed link. Optional secondary URL via DOI: `https://doi.org/{doi}` for the publisher's page.

**Step 6 — Return**

```json
{
  "server": "pubmed",
  "transport_used": "mcp" | "eutils",
  "window": "2026-05-04/2026-05-10",
  "query": "(...full query string...)",
  "fetched_total": 47,
  "matched_total": 47,                       // PubMed filter is server-side, so fetched == matched
  "fetch_errors": [],
  "records": [ ... ]
}
```

Cache the raw search + metadata responses to `.cache/{YYYY-WW}-pubmed.json`.

## Common Patterns

**Pattern A — Standard weekly scan**: PDAT-bounded query with all watchlist keywords OR'd together. The default.

**Pattern B — Newly-indexed reach-back**: when the user wants "papers PubMed indexed this week, even if published earlier" (useful for older preprints just appearing in PubMed), swap `PDAT` for `EDAT`. Document the choice in the digest.

**Pattern C — High-precision MeSH-only search**: when keyword matching is producing too much noise, ask the user for the exact MeSH headings they care about and search `term[MeSH]` only. Higher precision, lower recall.

**Pattern D — Author-specific watch**: outside this skill's default scope but easy — add `(Smith J[Author] OR Doe A[Author])` as an additional OR clause to the keyword group.

## Guardrails

1. **Always include the date bound.** A keyword-only PubMed query returns the entire PubMed history for the term. Forgetting `PDAT` is the bug that turns a 7-paper digest into a 70,000-paper data dump.
2. **Don't auto-expand keywords to MeSH.** PubMed's automatic-term-mapping silently expands "Alzheimer" to a MeSH tree; that's the right call for a clinician but the wrong call for a curated keyword digest. Quote keywords with `[Title/Abstract]` to disable expansion unless MeSH expansion is explicitly requested.
3. **Don't trust the first abstract API call to succeed.** `efetch` with `rettype=abstract` occasionally times out for batches > 100. On failure, halve the batch and retry; only after two full halvings do you give up on a record.
4. **Don't strip the `PMID:` prefix from `id`.** It distinguishes PubMed records from preprint DOIs at a glance — important during cross-source dedupe in the caller.
5. **Don't dedupe against bioRxiv/medRxiv inside this skill.** Cross-source dedupe is the caller's job.
6. **Respect the rate limit.** NCBI allows 3 requests/second without an API key, 10/second with one. Pace accordingly. If a key is in the env (`NCBI_API_KEY`), include it as `&api_key=...`.
7. **Don't claim a record is "in PubMed" just because esearch returned its PMID.** Some PMIDs are MEDLINE-status `Publisher` (in-process, not yet fully indexed). Fine to include but note `status` if available.

## Quick Reference

| Field          | E-utilities (fallback)                                                   | MCP (preferred)                       |
| -------------- | ------------------------------------------------------------------------ | ------------------------------------- |
| Search         | `esearch.fcgi?db=pubmed&term={q}&retmode=json`                            | `search_articles(query=...)`          |
| Metadata       | `esummary.fcgi?db=pubmed&id={pmids}&retmode=json`                         | `get_article_metadata(pmids=...)`     |
| Abstract       | `efetch.fcgi?db=pubmed&id={pmids}&rettype=abstract&retmode=xml`           | included in metadata when MCP returns it |
| Date filter    | `("YYYY/MM/DD"[PDAT] : "YYYY/MM/DD"[PDAT])`                              | same — pass inside query string       |
| Page size      | 200 (search), 100-200 (summary), 100 (abstract)                          | MCP server's choice                   |
| Auth           | optional `api_key` query param (3 → 10 rps)                              | per MCP server config                 |
| Canonical URL  | `https://pubmed.ncbi.nlm.nih.gov/{pmid}/`                                |                                       |

---
name: search-corpus
description: Answers "what have I already thought about X?" by searching the substacker corpus (seeds, drafts, published) for seeds matching a topic, keyword, analogy, or author. Returns a ranked list of seeds with id, title, status, density score, and a one-line excerpt. Use when another agent (Intuition Builder, Editor) needs prior thinking before generating new material, or when the writer asks "have I written about X." Trigger keywords: search, find, what have I, already thought, prior work, precedent, have I written about.
---

# Search Corpus

## Table of Contents

- [Workflow](#workflow)
- [Query forms](#query-forms)
- [Output format](#output-format)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by `intuition-builder` (before generating framings), `editor` (before reviewing a draft to surface prior thinking), writer directly. Read-only — no writes.

## Workflow

```
Search corpus for query:
- [ ] Step 1: Parse query → topic tag, keyword, analogy term, or author
- [ ] Step 2: Grep corpus/{seeds,drafts,published}/**/*.md
- [ ] Step 3: Rank matches by signal
- [ ] Step 4: Format top 10 as a ranked list with id, status, density, excerpt
```

## Query forms

The skill accepts three query shapes:

1. **Topic tag** (e.g., `dropout`): grep frontmatter `topics:` for the tag; fallback to body keyword.
2. **Freeform keyword** (e.g., `kv cache`): grep body + title for the phrase.
3. **Structured** (e.g., `{topics: [attention-mechanism], status: published}`): direct filter.

## Ranking

Rank by:
1. Exact tag match > freeform body match.
2. Density score descending.
3. Recency (created date descending).
4. Status priority: `published > draft > seed > dead`.

Exclude `corpus/dead/` always unless query includes `include_dead: true`.

## Output format

Top 10 matches, one per line:

```
N. {id} | {status} | density={score} | "{first-sentence excerpt, ≤120 chars}"
```

If >10 results, show 10 and append: `... N more matches — narrow the query`.

If 0 results: `No matches. Candidate related searches: {suggest 2-3 alternate topic tags}`.

## Worked example

**Query**: `dropout`

**Matches**:
```
1. 2026-04-21-dropout-as-ensemble-thinned-networks | seed | density=7 | "had a thought while running — dropout is secretly an ensemble method."
2. 2026-02-08-bagging-in-deep-nets | draft | density=6 | "bagging is the thing dropout is trying to be."
3. 2025-11-14-noise-as-regularization | published | density=5 | "adding noise at training time prevents the model from memorizing."
```

**Query**: `KV cache` (freeform)

**Matches**:
```
No matches. Candidate related searches: attention-mechanism, inference, context-engineering
```

## Guardrails

1. Read-only. Never mutates seeds.
2. Never returns seeds from `corpus/dead/` unless query explicitly opts in.
3. Excerpt is verbatim from body — never a summary.
4. If >10 matches, truncate and tell the caller.
5. If 0 matches, suggest related searches; do not invent matches.
6. Respect `manual_edits: true` — do not reveal private-looking content beyond first-sentence excerpt without caller explicitly requesting full seed read.

## Quick reference

- Input: query string or structured filter.
- Output: top-10 ranked matches with id, status, density, excerpt.
- Read-only, no side effects.

---
name: update-analogy-catalog
description: Appends an entry to substacker shared-context/analogy-catalog.md when the writer PUBLISHES a post that uses a new analogy. Not invoked on seed or draft — only on publish. Records source, target, post, freshness, mapping, where-it-breaks, and why-it-worked. Prevents silent recycling in future Intuition Builder runs. Use at publish time for any post that contains a non-trivial analogy. Trigger keywords: catalog, analogy catalog, update catalog, publish, analogy archive.
---

# Update Analogy Catalog

## Table of Contents

- [When this fires](#when-this-fires)
- [Workflow](#workflow)
- [Entry schema](#entry-schema)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called at publish time after Distribution Translator runs (or on manual trigger). Reads the published post to extract used analogies; writes to `shared-context/analogy-catalog.md`. Does NOT fire on seed or draft creation.

## When this fires

- User publishes a post (moves draft to `corpus/published/{section}/`).
- User runs `update-analogy-catalog` explicitly on a published post.
- Never on seed or draft.

## Workflow

```
For a newly published post:
- [ ] Step 1: Read the published post file
- [ ] Step 2: Extract non-trivial analogies (present a source-target mapping with mechanical weight)
- [ ] Step 3: For each, determine freshness (new / reused / borrowed)
- [ ] Step 4: For each, extract where-it-breaks if named
- [ ] Step 5: Write one entry per analogy to analogy-catalog.md
- [ ] Step 6: Commit ledger-style entry with date + post reference
```

### Step 2: Non-trivial extraction

Trivial similes don't count ("fast as lightning"). An analogy is non-trivial if:
- It has a named source domain (bucket brigade, immune system, courtroom)
- It maps to a specific technical target
- The mapping does work in the post (remove it and the explanation suffers)

The writer can manually annotate `analogy: true` in a post's frontmatter to force inclusion, or `analogy: skip` to exclude.

### Step 3: Freshness

- `fresh`: the writer's own analogy, first use. Default.
- `reused`: the writer used this analogy in a prior published post. Auto-detected by cross-checking the catalog.
- `borrowed`: the analogy came from a named source (Hofstadter, a cited paper). Writer annotates.

## Entry schema

Append to `analogy-catalog.md` under the table:

```markdown
| {source} | {target} | {post-title} | {fresh|reused|borrowed} | {note} |
```

Also in the "notes" section at the bottom:

```
## {post-slug} — YYYY-MM-DD
- analogy: {source} → {target}
- freshness: fresh|reused|borrowed
- why it worked: {one-sentence note from the writer or inferred from post context}
- breaks at: {the boundary the writer named in the post, if any}
```

## Worked example

**Event**: Writer publishes "Why your embedding search melted at 10pm" on 2026-05-20. The post uses two analogies:

1. "The retrieval layer is the thermometer" — monitoring-as-sensing; maps concept "retrieval quality metric" to "thermostat reading."
2. "RAG is prosthetic memory" — borrowed from `2026-03-03-rag-as-prosthetic-memory` (already in corpus/seeds/ earlier).

**Detection**:
- Analogy 1: source `thermometer`, target `retrieval quality metric`. Not in catalog. Freshness: **fresh**.
- Analogy 2: source `prosthetic memory`, target `RAG`. Already in catalog from a prior post. Freshness: **reused**. Cross-reference to the prior entry.

**Catalog update**:

| source | target | post | freshness | note |
|---|---|---|---|---|
| thermometer | retrieval quality metric | Why your embedding search melted at 10pm | fresh | "you need to sense before you can steer" — operational framing |
| prosthetic memory (reused) | RAG | Why your embedding search melted at 10pm | reused | sibling to 2026-03-03 post; same frame, new context |

## Guardrails

1. Only fires on publish. Never on seed or draft.
2. Reused analogies are a feature, not an error. Log them as reused; let the writer decide if a future post should freshen up.
3. Trivial similes are excluded. A rule of thumb: if removing the simile changes nothing about the explanation, skip it.
4. Borrowed analogies require attribution. If the writer doesn't name the source (Hofstadter, Feynman, a paper), mark `freshness: fresh` but flag for writer review.
5. Never edit existing catalog entries. Append-only.
6. If the writer explicitly marks `analogy: skip` in post frontmatter, respect it.

## Quick reference

- Fires on publish only.
- Appends rows to the analogy-catalog table + detailed notes section.
- Reuses are flagged, not errors.

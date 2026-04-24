---
name: check-analogy-novelty
description: Cross-references each proposed analogy in a 5-framing set against substacker shared-context/analogy-catalog.md to flag reuse. Classifies each analogy as new, reused-from-catalog (and which entry), or adjacent-to-catalog (close to an existing entry but not identical). Prevents the writer from recycling "imagine a library" for the twentieth time. Use after generate-analogy-set and before presenting framings to the writer. Trigger keywords: novelty, catalog, analogy reuse, already used, imagine a library.
---

# Check Analogy Novelty

## Table of Contents

- [Workflow](#workflow)
- [Match tiers](#match-tiers)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by the Intuition Builder after `generate-analogy-set` and before presenting framings. Reads `shared-context/analogy-catalog.md`. Does NOT write to the catalog — that's `update-analogy-catalog`'s job, fired on publish.

## Workflow

```
For each of the 5 framings:
- [ ] Step 1: Extract the analogy's source domain (e.g., "library card catalog")
- [ ] Step 2: Extract the analogy's target concept (e.g., "KV cache")
- [ ] Step 3: Grep analogy-catalog.md for exact or near-exact source × target match
- [ ] Step 4: Classify: new | reused-from-catalog | adjacent-to-catalog
- [ ] Step 5: For reused/adjacent, cite the catalog entry with its post
```

## Match tiers

- **New**: neither the source nor a close variant of it appears in the catalog for this target concept.
- **Reused-from-catalog**: exact source × target match — writer already used this analogy in a published post. Flag strongly; either justify reuse or swap.
- **Adjacent-to-catalog**: source matches a nearby analogy in the catalog (e.g., "drawer" vs. "card catalog") or target is in the catalog but source differs. Flag softly — writer should see the adjacency.

"Close variant" = same source domain (library, immune system, bucket brigade) even if different specific instance.

## Worked example

**Proposed framings for KV cache**:
1. Everyday: "a library's card catalog with a fixed drawer count"
2. Physical metaphor: "a ring buffer with index"
3. Contrarian: "the cache is not the table — it's the index into what's been already paid for"
4. Historical: "before caches, every lookup was recomputation"
5. Counterfactual: "remove the cache and decode becomes quadratic"

**Catalog check**:
- Entry in catalog: *"Agents as departments reading each other's memos but never sitting in on each other's meetings"* — source: institutional. Target: multi-agent. Not related to KV cache.
- Entry: *"Bucket brigade"* — source: bucket brigade. Target: sequential multi-agent. Not related.
- No entry for `library` → KV cache, or `ring buffer`, or `index`.

**Output**:
1. Everyday: new
2. Physical metaphor: new
3. Contrarian: new
4. Historical: new
5. Counterfactual: new

**But**: if the catalog had an entry *"Library index → tokenizer vocabulary"*, framing 1's adjacency would trigger: "adjacent-to-catalog — library appears once for a different target". Flag softly.

## Guardrails

1. Read-only. Never writes to the catalog.
2. Match on both source domain and target concept. Same source for different target is an adjacency, not a reuse.
3. Flag adjacencies, don't auto-reject — the writer decides if reuse is intentional (a recurring analogy can be a feature).
4. Cite the catalog entry + post when flagging. "Reused from catalog" without pointing to the entry is useless.
5. Don't expand near-matches to other analogy directions (biology vs. organizational are different domains, never flag across).
6. If the catalog is empty (early-stage publication), all framings are `new` by definition. Note this once in the output.

## Quick reference

- Input: list of 5 framings + analogy-catalog.md.
- Output: per-framing classification `{new | reused-from-catalog | adjacent-to-catalog}` with citation.
- Side effect: none. Read-only.

---
name: glossary-alignment-check
description: For each technical term in a substacker draft's claims, checks shared-context/glossary.md for a writer-specific definition and compares to field-standard. Emits a note for terms where the two diverge (aligned / diverged-safe / diverged-risky). Feeds into classify-claim (which definition governs) and write-review-artifact's Glossary Alignment section. Use on every claim. Trigger keywords: glossary alignment, term definition, writer vs field, load-bearing term.
---

# Glossary Alignment Check

## Workflow

```
Per claim:
- [ ] Step 1: Tokenize claim for candidate terms (named concepts, TLAs, math)
- [ ] Step 2: Grep shared-context/glossary.md for each term
- [ ] Step 3: If found, pull writer's definition
- [ ] Step 4: Compare to field-standard (prior knowledge + optional WebSearch)
- [ ] Step 5: Emit: aligned | diverged-safe | diverged-risky
```

## Three outcomes

- **aligned**: writer's definition matches field-standard. No note.
- **diverged-safe**: definitions differ but the post's argument doesn't depend on the difference. Note but don't block.
- **diverged-risky**: definitions differ AND the post's argument hinges on which definition is in force. Tier-2 note for the writer.

## Worked example

**Term**: "attention"
**Writer's glossary**: "the mechanism that lets tokens exchange information, including the residual bypass."
**Field-standard**: "the weighted sum `softmax(QK^T/√d)V`, excluding the residual."

**Status**: `diverged-risky` if post asserts "attention is O(n²)" — true under field definition, false-or-unclear under the writer's.

**Output note**: "Writer's glossary includes residual in 'attention'; field-standard excludes. Post's claim 'attention is O(n²) in memory' is true under field but misleading under writer's glossary. Consider disambiguating in-post or tightening the glossary."

## Guardrails

1. Never rewrite the glossary. Only flag.
2. Never mark `aligned` without actually checking the glossary file this run.
3. If glossary is missing or empty, emit `no-glossary` and treat field definition as governing.
4. When disagreement is strictly semantic (not functional), prefer `diverged-safe` over `diverged-risky` — err toward non-blocking.
5. Diverged-risky notes appear in the Glossary Alignment section of the review artifact; don't bury in claim table.

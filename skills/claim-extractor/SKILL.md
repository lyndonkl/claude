---
name: claim-extractor
description: Extracts atomic technical claims from a substacker essay draft, converting flowing intuition-first prose into a numbered list where each item is a statement that could in principle be verified or falsified. Skips non-technical sections (personal anecdote, motivation, call-to-action). Use when the Technical Reviewer starts a per-draft review. Trigger keywords: extract claims, atomic claims, technical claim list, fact-check prep.
---

# Claim Extractor

## Workflow

```
Per draft:
- [ ] Step 1: Segment draft by heading / section
- [ ] Step 2: Within each section, split by sentence
- [ ] Step 3: Flag sentences containing technical claims:
    - Math symbols / formulas
    - Named systems, components, algorithms
    - Quantitative assertions
    - Universal quantifiers ("always", "never", "all models")
    - Named papers / results
- [ ] Step 4: Coalesce adjacent claim sentences that argue the same thing into one claim
- [ ] Step 5: Output numbered list: {id, excerpt (≤200 chars), location}
```

## Non-claim content (skip)

- Personal anecdotes without technical assertion
- Motivation / framing
- Calls to action
- Closing maxims (unless they assert a technical fact)

## Worked example

Draft paragraph:
> Attention is O(n²). This is why context windows are expensive. Each token looks at every other token, and the matrix is n-by-n.

Extraction:
1. "Attention is O(n²) in compute and memory in a naive implementation." [§2 ¶1]
2. "Context windows are expensive because of attention's complexity." [§2 ¶1]
3. "Each token attends to every other token via an n-by-n matrix." [§2 ¶1]

## Guardrails

1. Never paraphrase aggressively. Preserve the writer's hedges.
2. Excerpts ≤200 chars verbatim.
3. Coalesce adjacent claims only if they argue the same thing.
4. Respect `[contrarian]` annotations — still extract the claim, but flag it for `classify-claim` to treat specially.
5. Don't extract claims from code blocks or quoted text.

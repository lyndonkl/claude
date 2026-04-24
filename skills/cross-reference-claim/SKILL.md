---
name: cross-reference-claim
description: Finds and cites a primary source for each substacker draft claim — original arXiv paper, official documentation, RFC, canonical textbook. Source hierarchy enforced: primary > secondary > tertiary > not-a-source. Records URL, title, passage/result that settles the claim. Use after classify-claim; runs once per claim unless classification is simplified-correct with high confidence on standard undergrad material. Trigger keywords: cross-reference, primary source, citation, arXiv, RFC, paper lookup, source hierarchy.
---

# Cross-Reference Claim

## Source hierarchy (enforced)

1. **Primary**: original arXiv paper, official docs (PyTorch, CUDA, Linux), RFC, ACM/IEEE proceedings, canonical textbook (*Deep Learning* Goodfellow et al., DDIA Kleppmann, Jurafsky & Martin).
2. **Secondary**: author's own blog/slides when they are the primary authority; well-maintained official implementation source.
3. **Tertiary**: Wikipedia (orientation only, never as the cite).
4. **Not a source**: random blog posts, Medium, X threads, unreviewed tutorials, other LLM outputs.

## Workflow

```
Per claim:
- [ ] Step 1: WebSearch with claim + likely source terms
- [ ] Step 2: WebFetch top candidate; extract specific result/passage
- [ ] Step 3: If paywalled, fall back one tier; note fallback explicitly
- [ ] Step 4: If nothing authoritative within 10 min on one claim, mark could-not-verify
- [ ] Step 5: Return {url, title, passage_or_result, tier}
```

## Guardrails

1. Never cite a blog post as primary.
2. Never cite model's own recall as source.
3. Never invent a URL. `could-not-verify` with attempted-queries is better than fabrication.
4. 48h wall-clock cap is enforced at the agent level; per-claim cap is 10 minutes of research.
5. `could-not-verify` doesn't block GO. It lands in the Could-Not-Verify section of the review; the writer decides whether to ship anyway.
6. Primary source must contain the specific result/passage — not a reference to a result. Fetch the paper, not a blog that cites the paper.

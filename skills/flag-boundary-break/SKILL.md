---
name: flag-boundary-break
description: For each simplified-boundary claim, drafts a one-paragraph suggestion for how to acknowledge the boundary inside the post — usually a single sentence or "but" clause — so the break becomes a teaching moment rather than hidden fragility. Runs for exactly the claims classified as simplified-boundary. Skip for all other classifications. Use after cross-reference-claim. Trigger keywords: boundary break, fold break into post, feature not flaw, simplified-boundary.
---

# Flag Boundary Break

## Workflow

```
Per simplified-boundary claim:
- [ ] Step 1: Identify the intuition the writer was using (analogy, metaphor, concrete picture)
- [ ] Step 2: Identify precisely where the intuition breaks using primary source
- [ ] Step 3: Draft a one-sentence suggestion that names the break as a feature
- [ ] Step 4: Optionally suggest a follow-up post if break is too rich for a sentence
- [ ] Step 5: Return {intuition, break_point, fold_suggestion, optional_follow_up}
```

## Worked example

Claim: "Attention is O(n²) in memory."
Classification: `simplified-boundary`.
Primary source: Dao et al. 2022 — FlashAttention, arXiv:2205.14135. "FlashAttention uses O(N) memory rather than the O(N²) of standard attention."

**Fold suggestion**:
> "The O(n²) figure is the naive memory cost — modern production attention (FlashAttention, Dao et al. 2022) is actually O(n) in HBM by never materializing the full attention matrix. The quadratic view is still the right intuition for 'why context windows are expensive' circa 2020, but the actual frontier now is 'attention is memory-bandwidth-bound,' which is a richer story — probably a follow-up post."

**Optional follow-up**: "FlashAttention as memory-bandwidth reframe."

## Guardrails

1. Fold suggestion is a nudge, not a rewrite. Never propose more than one sentence of insertion.
2. Never fold-suggest for `wrong` claims — those get fixed, not folded.
3. Always name the break specifically. "The analogy breaks at scale" is vague; "the drawer metaphor implies physical contiguity but the cache is logically indexed" is specific.
4. Optional follow-up is optional. Offer when the break is rich enough for its own post.
5. Writer's voice preserved — fold suggestions read like the writer could say them.

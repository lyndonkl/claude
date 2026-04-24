---
name: propose-section
description: Converts one candidate cluster from cluster-corpus-by-theme into a named, promised section proposal ready for writer review. Calls write-section-promise for the one-sentence promise. Rates fit confidence (high / medium / low / provisional) and flags borderline posts. Use once per cluster that passes ≥3-post threshold. Trigger keywords: propose section, section proposal, new section candidate.
---

# Propose Section

## Workflow

```
Per qualifying cluster:
- [ ] Step 1: Name the cluster (working name from centroid codes)
- [ ] Step 2: Call write-section-promise for the one-sentence promise
- [ ] Step 3: Score each member post: tight | fair | borderline
- [ ] Step 4: Check non-overlap against existing section-map.md and other proposals this run
- [ ] Step 5: Assign fit_confidence:
    - high: ≥5 tight-fit posts + strong cohesion + unambiguous non-overlap
    - medium: 3-4 posts with mixed fit + narrowing promise
    - low: borderline throughout; defer
    - provisional: confident enough to name, uncertain enough to need probation
- [ ] Step 6: Write proposal block with reasons_to_reject (steelman the case against)
```

## Output

```yaml
proposal:
  name: "{Human name}"
  slug: {kebab-case}
  promise: "{one sentence}"
  fit_confidence: high | medium | low | provisional
  supporting_posts: [{slug, fit}]
  borderline_posts: [{slug, reason}]
  non_overlap_check: "Distinct from {other section} because..."
  reasons_to_reject: "Two of these posts also fit {other section}. If those migrate, cluster drops to 3 posts and becomes marginal."
```

## Guardrails

1. Never propose with <3 posts unless labeled PROVISIONAL + promise-testing plan.
2. Never rename an existing section inside this skill — route through user-confirmation flow.
3. Provisional sections require an explicit promotion test: "X more posts in Y weeks."
4. Reasons-to-reject is mandatory — the Curator must pre-build a devil's advocate brief.
5. Confidence is assigned from rules, not feel.

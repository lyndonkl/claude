---
name: attribute-performance
description: For each substacker post that materially over- or under-performs the rolling baseline (|z| ≥ 1.0), produces a plain-English attribution paragraph with calibrated confidence (high / medium / low / unexplained). Considers subject-line effect, topic zeitgeist, external share, day-of-week, length effect, and audience-notes signals. Labels unexplained outliers explicitly rather than fabricating a story. Use after compute-baseline when outlier posts exist. Trigger keywords: attribution, why did this post work, outlier explanation, performance analysis.
---

# Attribute Performance

## Workflow

```
For each |z| ≥ 1.0 post:
- [ ] Step 1: Check 6 attribution channels (subject line, topic zeitgeist, external share, day-of-week, length, audience-notes match)
- [ ] Step 2: Per channel, rate confidence: high / medium / low / absent
- [ ] Step 3: If no channel ≥ medium, return "unexplained — candidate hypotheses: A, B, C"
- [ ] Step 4: If ≥1 channel ≥ medium, attribute with confidence label
```

## Six attribution channels

1. **Subject-line effect**: did title-pattern match a known audience-notes signal?
2. **Topic zeitgeist**: was topic trending externally (check trend-scout digests if available)?
3. **External share**: WebFetch public post URL + Notes mentions — did a larger account restack it?
4. **Day-of-week**: send-day different from baseline?
5. **Length effect**: significantly shorter or longer than median?
6. **Audience-notes signals**: does this post fit a previously-medium-confidence pattern?

## Guardrails

1. **Never fabricate attribution.** `unexplained` is a valid output.
2. Confidence = highest single channel. Two mediums do not make a high.
3. External share = highest-confidence driver (WebFetch evidence is verifiable).
4. Day-of-week alone rarely justifies medium confidence.
5. Audience-notes match requires the post to fit the pattern's supporting evidence set, not just semantically match.
6. Keep attribution to 2–4 sentences per outlier. Full weekly report cannot exceed 800 words.

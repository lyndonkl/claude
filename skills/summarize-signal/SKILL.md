---
name: summarize-signal
description: Given a candidate item from the substacker Trend Scout fetch, WebFetches the full post or arXiv abstract and produces a one-line "teaches X" summary plus signal_type classification (mechanism / empirical / tool / opinion / announcement / benchmark). Distinguishes teaching-content from capability-announcement explicitly. Use during the weekly run, after fetching and before ranking. Trigger keywords: summarize, signal type, mechanism vs announcement, teaching content.
---

# Summarize Signal

## Workflow

```
Per candidate item:
- [ ] Step 1: WebFetch the URL; ask: "Extract the core argument in 300 words. What mechanism does this teach? Is there a diagram/analogy? Is this a capability announcement?"
- [ ] Step 2: Classify signal_type: mechanism | empirical | tool | opinion | announcement | benchmark
- [ ] Step 3: Classify intuition_density: high (diagram + analogy + worked example) | medium | low (prose-only announcement)
- [ ] Step 4: Compose one-line summary framed as "teaches that X" or "shows that Y"
- [ ] Step 5: Voice-check the summary against voice-profile don'ts
```

## Signal type taxonomy

- **mechanism**: teaches HOW something works (attention heads, routing, retrieval)
- **empirical**: reports a measurement/experiment (benchmark diff, ablation result)
- **tool**: introduces or reviews a specific tool/library
- **opinion**: position piece, no new data
- **announcement**: capability release, model drop, version bump — no mechanism
- **benchmark**: leaderboard update, SOTA claim without teaching

## Output per item

Appends to candidate record:

```json
{
  "summary": "Teaches that X",
  "signal_type": "mechanism",
  "intuition_density": "high",
  "teaches_mechanism": true,
  "full_text_excerpt_300w": "..."
}
```

## Guardrails

1. One WebFetch per item. Fetch failure → `summary: "FETCH_FAILED"` and let ranker drop.
2. Never hallucinate a mechanism. If the post doesn't teach one, say so explicitly.
3. Stay under 30 words in the summary.
4. Never use: delve, unpack, paradigm shift, moreover, furthermore, "it's worth noting."
5. If item is an announcement with no mechanism, `teaches_mechanism: false` — downstream ranker drops it.

---
name: classify-claim
description: Assigns each extracted claim to one of five buckets — simplified-correct, simplified-boundary, wrong, contested, overclaim — with low/medium/high confidence and one-sentence rationale. Classification happens before primary-source verification (which confirms, not invents). Use for every claim from claim-extractor. Trigger keywords: classify, bucket, simplified vs wrong, claim type, technical classification.
---

# Classify Claim

## Five buckets

- **simplified-correct**: strips detail; underlying claim still holds. Keep.
- **simplified-boundary**: holds in common case, breaks in edge case. Fold break into post.
- **wrong**: flat factual error. Fix.
- **contested**: field actively debating. Hedge.
- **overclaim**: true narrowly, asserted broadly. Scope.

## Examples

- "Softmax turns logits into a probability distribution" → **simplified-correct** (omits calibration caveats but the core claim holds).
- "Attention is O(n²) in memory" → **simplified-boundary** (true naive; FlashAttention is O(N)).
- "Softmax produces calibrated probabilities" → **wrong** (distribution ≠ calibrated probability).
- "LLMs exhibit emergent reasoning with scale" → **contested** (Schaeffer et al. 2023 actively disputes).
- "RAG beats fine-tuning for domain knowledge" → **overclaim** (true for tail factoid recall; false for reasoning).

## Workflow

```
Per claim:
- [ ] Step 1: Match claim to nearest bucket by definition
- [ ] Step 2: Assign confidence: low (pattern-matching, need source), medium (field knowledge suggests), high (sure)
- [ ] Step 3: Write one-sentence rationale
- [ ] Step 4: If low confidence, defer final classification until cross-reference-claim confirms
```

## Guardrails

1. Never classify `wrong` without a post-classification primary-source check (that's `cross-reference-claim`).
2. Respect `[contrarian]` regions: `wrong` downgrades to `contested` or `overclaim` inside contrarian annotations.
3. Classification is structural — goes on the claim object, not in prose.
4. If the writer's glossary defines a term differently than the field, `glossary-alignment-check` ran first and flagged it — apply the writer's definition for classification.
5. Default to the more conservative classification on ties. `simplified-boundary` beats `wrong` when the claim is right "most of the time."

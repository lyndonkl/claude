---
name: stress-test-analogy
description: Stress-tests a proposed analogy by finding the edge where the mapping breaks, then frames that break as a teaching opportunity the writer can fold into the post. Every analogy has a boundary; the writer's style treats that boundary as a feature. Use after generate-analogy-set and map-analogy-to-concept, for each framing. Trigger keywords: where does it break, stress-test, boundary, edge case, fold the break, analogy limits.
---

# Stress Test Analogy

## Table of Contents

- [Workflow](#workflow)
- [Where-it-breaks taxonomy](#where-it-breaks-taxonomy)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by the Intuition Builder per framing. Input is one framing (source + target + mapping from `map-analogy-to-concept`). Output feeds the final artifact's "Where it breaks" section for each framing and the Technical Reviewer's `flag-boundary-break` on drafts.

## Workflow

```
For one framing (source → target + mapping):
- [ ] Step 1: Identify the mapping's weakest link — which source-component-to-target-component pairs are forced?
- [ ] Step 2: Generate 2-3 edge cases where the forced pair fails
- [ ] Step 3: Write the boundary as one or two sentences — specific and named
- [ ] Step 4: Propose a "fold" — how the writer turns this break into content in the draft
- [ ] Step 5: Rate fold value: high | medium | low (high = the break is its own paragraph or sub-section)
```

### Step 3: Boundary phrasing

The boundary sentence should be specific enough that the reader could verify it. Good: "The drawer metaphor implies physical contiguity in memory, but a KV cache is logically indexed, not physically contiguous." Bad: "The analogy doesn't quite work at scale."

### Step 4: The fold

The writer's voice turns boundary-breaks into features, not hidden flaws. A good fold says: "This is where the analogy stops working — and here's what's interesting about why." Propose one sentence for the writer to edit.

## Where-it-breaks taxonomy

Analogies break in predictable ways:

- **Scale break**: works for small, fails for large (or vice versa).
- **Category break**: the two domains are structurally different (a cache is not physically a drawer).
- **Dynamics break**: static analogy, dynamic target (or vice versa).
- **Granularity break**: the analogy glosses over an important sub-mechanism.
- **Causality break**: the analogy implies the wrong causal direction.

Use these tags to classify the break type in the output.

## Worked example

**Framing**: "KV cache is a library card catalog with a fixed drawer count."

**Mapping** (from `map-analogy-to-concept`):
- library = the cache data structure
- drawer = one slot in the cache (capacity-bounded)
- card = one (key, value) projection pair
- lookup = retrieval by key
- eviction policy = what you do when drawers fill

**Stress test**:
1. **Category break**: drawers imply physical location. KV cache entries are not physically located; they're logically indexed in a tensor. *Edge*: readers familiar with memory layout will find this confusing.
2. **Dynamics break**: a library catalog is mostly static (you add cards; you rarely evict). A KV cache evicts constantly under streaming generation. *Edge*: the writer must describe eviction, which the library analogy barely touches.
3. **Granularity break**: a card catalog doesn't do attention — it's pure retrieval. But KV cache IS the state that attention reads from. *Edge*: the analogy covers "store and look up" but not "what the lookup enables."

**Boundary sentence**:
"The drawer metaphor captures capacity and lookup, but it hides two things: eviction dynamics under streaming decode (real drawers don't lose cards every turn) and the role of the cache as input to attention (a card catalog doesn't compute anything — a KV cache does)."

**Proposed fold** (for the writer):
"Say upfront that the library image is for the shape of the thing, not the motion. Then let eviction be the paragraph that breaks the image — 'real drawers don't evict a card every time you add a new one; a KV cache does, which is where the analogy starts needing a second image.' That becomes the pivot."

**Fold value**: high. This break is a whole paragraph in the draft.

## Guardrails

1. Every framing gets a boundary. If you can't find one, you haven't stress-tested enough — try harder.
2. Boundary sentence must be specific and verifiable. No "the analogy breaks at scale."
3. Classify the break with one of the 5 taxonomy tags.
4. Fold-value rating is 3 levels only: high / medium / low. Nothing is "critical" or "trivial."
5. Do not propose replacement analogies inside this skill — the writer picks from the 5 framings. Proposing a 6th contradicts the "5 framings" contract.
6. Keep the output compact: 1 boundary sentence + 1 fold sentence per framing. The writer does the rest.

## Quick reference

- Input: one framing (source + mapping).
- Output: `{boundary: str, break_type: str, fold: str, fold_value: high|medium|low}`.
- Runs once per framing (5 times per Intuition Builder invocation).

---
name: map-analogy-to-concept
description: Produces an explicit component-by-component mapping from the analogy's source domain to the target technical concept. Rejects vague analogies by forcing each source element to map to a specific target element, and flags unmapped elements as voice-breaking ("it's like a brain" is rejected because "brain" is unmapped). Use after generate-analogy-set, for each of the 5 framings. Trigger keywords: map, component mapping, source target, explicit mapping, what does the X correspond to.
---

# Map Analogy to Concept

## Table of Contents

- [Workflow](#workflow)
- [Mapping schema](#mapping-schema)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by the Intuition Builder per framing, after `generate-analogy-set` and before `stress-test-analogy`. Gentner's structure-mapping theory is the theoretical spine: good analogies map **relations**, not just objects.

## Workflow

```
For one framing (source → target):
- [ ] Step 1: Enumerate the source domain's key components (entities + relations)
- [ ] Step 2: For each source component, propose the target component it maps to
- [ ] Step 3: Check systematicity — do the relations carry across, or only objects?
- [ ] Step 4: Flag any source component that maps to nothing concrete (vague mapping = reject)
- [ ] Step 5: Return the mapping table
```

### Step 3: Systematicity check

A strong analogy preserves the **pattern of relations**, not just object-level similarity. Example:

- Weak: "a neural network is like a brain" — both have "neurons", but the relation "neurons fire" doesn't carry over in a useful way.
- Strong: "V/D/J gene recombination in B cells maps to multi-agent diversity" — the relation "small vocabulary generates exponential combinatorial space" carries.

If the framing only matches on objects (nouns), reject or downgrade.

### Step 4: Unmapped flagging

Every source component must map somewhere. "It's like a brain" fails because "brain" is unmapped to anything specific in the target (neuron? cortex? entire NS?). Flag and reject.

## Mapping schema

```yaml
source_domain: "library card catalog"
target_concept: "KV cache"
mapping:
  - source: "library"
    target: "the KV cache data structure"
    relation: "contains"
  - source: "drawer"
    target: "cache slot"
    relation: "capacity-bounded container"
  - source: "card"
    target: "(key, value) projection pair"
    relation: "indexed entry"
  - source: "lookup by drawer then card"
    target: "retrieval by position in key tensor"
    relation: "indexed retrieval"
  - source: "eviction when drawers fill"
    target: "LRU / FIFO eviction under context-length pressure"
    relation: "replacement under capacity constraint"
systematicity_score: 4/5  # how well relations carry over
unmapped_source: none
unmapped_target: "the attention operation that reads this cache"  # flagged — see stress-test
```

## Worked example

**Framing**: "Dropout is antibody diversity for weights."

**Source components**:
- immune system
- antibody population
- pathogen recognition
- diversity generation (V/D/J recombination)

**Target components**:
- neural network
- weights under dropout
- generalization to unseen examples
- implicit ensembling via sub-networks

**Mapping**:
| Source | Target | Relation |
|---|---|---|
| immune system | the trained neural network | generates patterns from a small genome/parameter set |
| antibody population | ensemble of thinned sub-networks | many variants tested in parallel |
| pathogen recognition | generalization on test data | performance on unseen inputs |
| V/D/J combinatorial generation | random dropout masks produce sub-network diversity | small seed → many variants |

**Systematicity**: 4/5 — the relation "small number of building blocks → large functional diversity" carries across. The one break: actual biological V/D/J has selection (negative selection in thymus), which dropout doesn't do. Flag.

## Guardrails

1. Every source component maps to a concrete target component. No source is left unmapped.
2. Rate systematicity on a 1–5 scale. Below 3 = the analogy is object-level, not relation-level; flag for downgrade.
3. Do not generate the analogy itself — that's `generate-analogy-set`. This skill only maps.
4. Flag unmapped target components as candidates for the stress-test boundary.
5. Mapping output is structured (table or yaml) — don't write it as prose.

## Quick reference

- Input: one framing (source + target).
- Output: structured mapping + systematicity score + unmapped flags.
- Theoretical basis: Gentner's structure-mapping; relations > objects.

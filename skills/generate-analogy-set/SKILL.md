---
name: generate-analogy-set
description: Generates exactly 5 distinct intuitive framings for a given technical topic — one everyday analogy, one physical metaphor, one contrarian take, one historical angle, one counterfactual. Each framing is a short scaffold (not prose), paired with its archetype and a one-line framing statement. Use when the writer invokes the Intuition Builder agent, as the core generation step before mapping, stress-testing, novelty checking, and voice fitness. Trigger keywords: generate framings, analogies for, give me 5, intuitive angles, framing set.
---

# Generate Analogy Set

## Table of Contents

- [The 5 archetypes](#the-5-archetypes)
- [Workflow](#workflow)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by the Intuition Builder agent as step 1. Feeds `map-analogy-to-concept`, `stress-test-analogy`, `check-analogy-novelty`, `voice-fitness-check`.

## The 5 archetypes

Each framing must match one of these archetypes:

1. **Everyday analogy** — maps the topic to something in ordinary life (cooking, traffic, weather, a household object). Accessible; surface-friendly.
2. **Physical metaphor** — maps to a physical system (fluid, gravity, spring, circuit, lens). Rigorous when the physics actually transfers; leaky when it doesn't.
3. **Contrarian take** — inverts the received framing. "People say X; actually Y." Works when the received framing has a known failure mode.
4. **Historical angle** — shows the topic through its precursor or evolution (attention before Transformer; word2vec → GloVe → BERT; consistent hashing's origin in distributed caches).
5. **Counterfactual** — "what if this weren't here?" Reveals function by subtracting. (See `propose-counterfactual` for depth.)

These 5 are fixed. If a topic resists one archetype (rare), the agent produces a weaker version rather than substituting a 6th.

## Workflow

```
Generate 5 framings for topic T:
- [ ] Step 1: Restate T in one sentence (what the writer is explaining)
- [ ] Step 2: Brainstorm 2-3 candidates per archetype
- [ ] Step 3: Pick the strongest candidate per archetype using the voice-profile analogy-direction priority (biology > organizational > sports; NEVER physics/military)
  - Exception: "physical metaphor" archetype explicitly permits physical domain, but even here prefer fluid/biological analogues over mechanical/military ones.
- [ ] Step 4: Write each as one-line framing statement (≤25 words)
- [ ] Step 5: Return the 5 with archetype labels
```

### Priority in selection

The voice-profile says biology → AI, organizational → multi-agent, sports → calibration are the writer's characteristic directions. Within each archetype, if a biology-flavored option exists AND is crisp, it wins over an equally crisp mechanical/military option. The writer almost never uses physics/military.

## Worked example

**Topic**: Attention (in Transformers).

**5 framings**:

1. **Everyday**: *A crowded table where each person glances around to find the two or three others whose words most reshape what they're about to say.*
2. **Physical metaphor**: *A weighted heat diffusion — each token's representation equilibrates against others in proportion to their pairwise affinity, smoothing toward a distribution.*
3. **Contrarian**: *Attention is not about "where the model looks" — it's about which other tokens get to edit you, and by how much. The token is the editor, not the camera.*
4. **Historical**: *Before attention, seq2seq bottlenecked through a single fixed-length hidden state — "read the whole sentence, then speak." Attention said: let the decoder re-read relevant words each step. Attention is the inversion of the bottleneck.*
5. **Counterfactual**: *Remove attention from a transformer and you have a stack of residual MLPs per token — no information ever flows between token positions within a layer. Context is gone. That absence is what attention is "doing."*

Each framing is ≤1 sentence (some are 2). The mapping, breaks, and novelty checks come from the downstream skills.

## Guardrails

1. Always produce exactly 5 — one per archetype. No substitutions.
2. Each framing is ≤25 words as a one-line statement.
3. Within an archetype, prefer biology / organizational / sports direction unless the topic is physical enough that the physical metaphor IS the right call.
4. Never use military, war, or weapons metaphors. Never combat-code.
5. Never produce prose-ready framings. These are scaffolds; the writer writes the prose.
6. If a topic is too narrow or too broad, return a single "scope-clarification-needed" message instead of forcing 5 weak framings.

## Quick reference

- Input: topic string.
- Output: 5 framings × {archetype, statement}.
- Downstream: each framing feeds through mapping, stress-test, novelty check, voice fitness.

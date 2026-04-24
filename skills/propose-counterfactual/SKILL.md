---
name: propose-counterfactual
description: Produces the counterfactual framing in an Intuition Builder 5-set — "what if this component were not here?" Reveals the function of a technical element by subtracting it and observing what breaks. Uses Pearl's causal ladder (counterfactual = level 3) as the theoretical spine. Use as the 5th archetype slot of generate-analogy-set, or invoked standalone when the writer wants to build intuition for why a specific element exists. Trigger keywords: counterfactual, what if not, remove, subtract, reveal function, why does this exist.
---

# Propose Counterfactual

## Table of Contents

- [Workflow](#workflow)
- [The 3 counterfactual moves](#the-3-counterfactual-moves)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** One of the 5 archetypes in `generate-analogy-set`. Can also be invoked standalone when the writer specifically wants the counterfactual angle without the full 5-set.

## Workflow

```
For topic T:
- [ ] Step 1: Identify the component / mechanism whose function the writer wants to illuminate
- [ ] Step 2: Propose the subtraction — what if this component were absent?
- [ ] Step 3: Describe the concrete system that results (what you'd have instead)
- [ ] Step 4: Describe what breaks — performance, correctness, expressivity, efficiency
- [ ] Step 5: Return the counterfactual framing statement
```

## The 3 counterfactual moves

Three sub-archetypes, pick whichever fits best:

1. **Ablation**: "Remove X. What remains?" Reveals X's function by showing the degraded system.
2. **Substitution**: "Replace X with its naive alternative. How does the system fail?" Reveals why X is the specific choice.
3. **Inversion**: "What if X operated the opposite way?" Reveals directionality — why X pushes one way and not the other.

## Worked example

**Topic**: Attention (in Transformers).

**Ablation**:
"Remove attention from a transformer and you have a stack of residual MLPs per token — no information ever flows between token positions within a layer. The model can still transform each token independently, but 'context' is gone. That absence is what attention is 'doing.'"

**Substitution**:
"Replace attention with fixed convolutions (the RNN/CNN alternative). You get locality — each token sees its neighbors — but the model can't arbitrarily connect token 1 to token 500. Attention's gift is not the operation, it's the arbitrary-range addressing."

**Inversion**:
"Invert attention: instead of softmax-weighted averaging, what if the model picked exactly one token to copy from? That's hard-attention, and it turns out to be worse for training — soft interpolation makes the loss surface navigable. Attention is soft by gradient-descent necessity, not by design choice."

Pick one (usually ablation for a 5-framing set). The others can become a standalone post later.

## Guardrails

1. The counterfactual must be concrete. Not "imagine attention didn't exist" — actually describe what the system looks like without it.
2. Describe the failure specifically. "Performance would suffer" is vague; "context is gone — the model processes tokens independently within a layer" is specific.
3. Counterfactual framing is ≤2 sentences for the framing statement. The details can be expanded in the writer's draft.
4. Do not confuse counterfactual with hypothetical. Counterfactual is "what if this weren't here" (revealing function). Hypothetical is "what if we tried X instead" (proposing an alternative). This skill is the former.
5. If the topic has no clear subtractable component (rare — true of "transformer" but not of "softmax"), fall back to substitution or inversion.

## Quick reference

- Input: topic + (optional) target-component-to-ablate.
- Output: one counterfactual framing statement + the concrete failure it reveals.
- Theory: Pearl's causal ladder — counterfactual reasoning illuminates causation in a way association cannot.

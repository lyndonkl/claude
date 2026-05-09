---
name: ml-primitive-decoder
description: Decomposes any ML construct (attention, layer norm, softmax, convolution, dropout, contrastive loss, diffusion step, gradient descent update, cross-entropy) into the small set of linear-algebra primitives it's built from, then explains why those primitives produce the observed behavior. Includes an ablation thought experiment that asks "what would break if you removed this piece?". Use when the user asks "why does X work?", "explain attention/conv/norm intuitively", "what's actually happening in this layer", or when reading an architecture paper and a particular block doesn't make sense yet.
---

# ML Primitive Decoder

## Table of Contents
1. [Workflow](#workflow)
2. [The Primitive Catalog](#the-primitive-catalog)
3. [Decoding Patterns](#decoding-patterns)
4. [Ablation Thought Experiment](#ablation-thought-experiment)
5. [Common Patterns](#common-patterns)
6. [Guardrails](#guardrails)
7. [Quick Reference](#quick-reference)

Most ML constructs that look opaque are actually a short stack of well-understood linear algebra primitives composed in a specific way. Attention is dot product + softmax + weighted sum. Layer norm is recenter + rescale + learnable affine. Diffusion is noise injection + denoising regression repeated. This skill names the primitives, then shows why their composition produces the behavior the construct is famous for.

The signature deliverable is: **construct = primitive₁ + primitive₂ + primitive₃, and *that's why* it does X**.

**Quick example (Attention):**

> **Construct:** Self-attention layer, output = softmax(QKᵀ/√d) · V.
>
> **Primitives:**
> 1. **Linear projections** (Q, K, V each = a different learnable linear layer applied to the same input).
> 2. **Dot product** (QKᵀ measures pairwise similarity between query and key vectors).
> 3. **Scaled softmax** (divides scores by √d to keep variance bounded, then row-normalizes into mixing weights).
> 4. **Weighted sum** (multiplying by V is a per-row weighted average over value vectors).
>
> **Why it works:** Each token learns to *advertise* (K), *ask* (Q), and *deliver* (V). The dot product matches asks to advertisements; softmax turns raw matches into selection weights; the weighted sum is the selected content. The whole layer is content-addressable memory implemented in pure linear algebra.
>
> **Ablation:**
> - Remove softmax → linear combination, no selectivity (just averaging everything).
> - Remove √d → softmax saturates as d grows, gradients vanish.
> - Tie Q = K → tokens can only ask questions about *themselves*; no cross-token information transfer.

## Workflow

Copy this checklist and track your progress:

```
Decoding Progress:
- [ ] Step 1: Identify the construct and write its formula
- [ ] Step 2: List the primitives it's composed of
- [ ] Step 3: Explain what each primitive contributes
- [ ] Step 4: Show how composition produces the famous behavior
- [ ] Step 5: Run the ablation thought experiment (what breaks if you remove each piece?)
- [ ] Step 6: Verify with a tiny worked example or invitation
```

**Step 1: Identify the construct and write its formula**

Pin down what you're decoding. Get the formula in front of you (and the user). If the user asks "why does attention work" without specifying, it's almost always self-attention — but check. Multi-head attention, cross-attention, and flash attention are different decompositions.

For a catalog of common ML constructs and their formulas, see [resources/constructs.md](resources/constructs.md).

**Step 2: List the primitives it's composed of**

The primitives are a small fixed set (see [The Primitive Catalog](#the-primitive-catalog) below). Decompose the formula into a list of these. Most constructs are 2-5 primitives.

The discipline: name only the *load-bearing* primitives. Trivial reshapes, broadcasts, and identity passes don't count. If a primitive doesn't change the *behavior* of the construct, skip it.

**Step 3: Explain what each primitive contributes**

For each primitive, write one sentence saying what it does *in this construct specifically* — not in general. "Dot product measures alignment" is too generic. "Dot product, applied to (Q, K) pairs, scores how well each token's question matches each other token's advertisement" is specific.

**Step 4: Show how composition produces the famous behavior**

This is the payoff. The construct is famous for some behavior — attention does content-addressable retrieval; layer norm stabilizes training; softmax produces a sharp-or-smooth distribution. Show how the *combination* of primitives produces that behavior. The composition is where the magic isn't.

A good Step 4 reads like: "Primitive A produces sub-effect 1. Primitive B turns sub-effect 1 into sub-effect 2. Primitive C turns sub-effect 2 into the famous behavior. Each step is mechanical; the famous behavior emerges from the chain."

**Step 5: Run the ablation thought experiment**

For each primitive, ask: "what would break if we removed this?" The answers are the highest-information part of the decoding — they tell the learner *why each piece is there*, which is much harder to forget than the formula.

See [Ablation Thought Experiment](#ablation-thought-experiment) below for the structure. For ablation tables per construct, see [resources/ablations.md](resources/ablations.md).

**Step 6: Verify with a tiny worked example or invitation**

Either compute one tiny instance of the construct end-to-end (a 3-token attention, a 2-feature layer norm) showing each primitive's intermediate output — or invite the user to do so. The worked example is what makes the decomposition feel real, not just declarative.

For tiny worked examples per construct, hand off to the `worked-example-walkthrough` skill.

## The Primitive Catalog

Almost every ML construct is built from a small set of these:

| Primitive | What it does | Famous uses |
|---|---|---|
| **Linear projection** (matrix multiply) | Maps input vector to a new space; learnable | Q/K/V projections, FFN layers, embeddings |
| **Dot product** | Measures alignment between two vectors | Attention scores, cosine similarity, score functions |
| **Outer product** | Forms a rank-1 matrix from two vectors | Hebbian updates, low-rank adaptations (LoRA) |
| **Softmax** | Normalizes scores into a probability distribution; sharpens at high contrast | Attention weights, classification heads, mixture-of-experts gating |
| **Element-wise nonlinearity** (ReLU, GELU, sigmoid, tanh) | Introduces nonlinearity, gates information | Hidden layers, gating mechanisms |
| **Weighted sum** | Combines vectors with given weights | Attention output, mixture models, EMA |
| **Centering / normalization** | Subtract mean, divide by std | LayerNorm, BatchNorm, GroupNorm |
| **Affine transform** (γx + β) | Learnable shift + scale | LayerNorm tail, BatchNorm tail |
| **Residual / skip connection** (x + f(x)) | Adds an identity path around a block | Transformers, ResNets |
| **Dropout / noise injection** | Randomly zeros or perturbs values | Regularization, diffusion forward process |
| **Convolution** | Weight-shared local linear map | CNNs |
| **Pooling** (max, mean, attention) | Aggregates many features into one | Read-out layers, set/graph reductions |
| **Embedding lookup** | Indexes into a learnable table | Token embeddings, position embeddings |
| **Loss (cross-entropy, MSE, contrastive, KL)** | Scalar measure of wrongness | Training objective |
| **Gradient descent step** | Subtract scaled gradient from parameters | Every training loop |

Whenever you decode a construct, the primitives list should come from this catalog. If you find yourself naming something that isn't here, either it's a more complex construct (decompose further) or it's a new primitive worth adding.

## Decoding Patterns

### Pattern A: The pipeline construct
The construct is a *sequence* of primitives applied in order. Decode as: input → P₁ → intermediate → P₂ → ... → output. Examples: attention block, transformer FFN, layer norm.

### Pattern B: The decorated construct
The construct is a base primitive *wrapped* with normalization, residuals, or activations. Decode as: base + decorator₁ + decorator₂. Examples: a transformer block (attention + residual + LN + FFN + residual + LN), ResNet block.

### Pattern C: The objective construct
The construct is a loss function. Decode as: similarity measure + normalization + reduction. Examples: cross-entropy (log + sum), contrastive loss (similarity + softmax + cross-entropy).

### Pattern D: The iterative construct
The construct is a single *step* repeated many times. Decode the step, then explain the dynamics of repetition. Examples: gradient descent (gradient + step), diffusion (noise + denoise step), RNN (state update step).

For one full decode per pattern, see [resources/constructs.md](resources/constructs.md).

## Ablation Thought Experiment

For every decoded construct, run an ablation table. For each primitive, answer: "what would break if you removed it (or replaced it with the simplest possible thing)?"

This is the most pedagogically valuable part of the skill. It forces the user to see *why each piece is there*.

**Format:**

| Remove | What happens | What insight it reveals |
|---|---|---|
| Primitive 1 | Concrete failure mode | What primitive 1 is contributing |
| Primitive 2 | Concrete failure mode | What primitive 2 is contributing |
| ... | ... | ... |

**Example (Attention):**

| Remove | What happens | What insight it reveals |
|---|---|---|
| Softmax | Output becomes a linear combination — every token mixed equally with every other; no selectivity | Softmax is what makes attention *attention* (not averaging) |
| √d scaling | At high d, dot products become large, softmax saturates, gradients vanish | √d controls the variance of scores so softmax stays in its useful regime |
| Separate Q vs K | Tokens can only attend based on self-similarity, not cross-similarity | Splitting Q and K is what allows asymmetric matching |
| V (use K instead) | Model can only retrieve what tokens advertise about themselves; no separate "content" channel | V is the actual payload — separate from the matching key |
| Multi-head | Single semantic relation per layer; loses ability to attend along multiple axes simultaneously | Heads are parallel attention computations on different subspaces |

For ablation tables for many constructs, see [resources/ablations.md](resources/ablations.md).

## Common Patterns

### When the user asks "why does X work?"
Always run the full workflow. The "why" is in Step 4 (composition) and Step 5 (ablation), not in Step 2 (primitive list).

### When the user asks "what is X doing?"
Steps 1-3 may be enough. Skip ablation if the user just wants a quick read.

### When the construct is opaque even to you
Don't fake it. Decode what you understand; flag what you don't. "I can decode the attention part but I'm not sure why this paper added the gating; let me look it up" is a much better response than confident-sounding nonsense.

### When the construct is novel
Decompose into the catalog of primitives anyway. Truly novel ML constructs are rare; most are reshufflings of the catalog. If something genuinely doesn't fit, name it as a new primitive and explain why.

## Guardrails

- **Don't list primitives without saying what they do *in this construct*.** Generic descriptions ("softmax produces a probability distribution") are worth less than construct-specific ones ("softmax converts the row of dot product scores into mixing weights for the value vectors").
- **Don't skip the ablation.** It's the part that builds *durable* understanding. The user who can answer "what would happen if you removed the softmax from attention?" understands attention; the user who can only recite the formula does not.
- **Don't bury the punchline.** Step 4 — "and that's why it does X" — should be loud and short. If the punchline is buried in paragraph 4, the reader missed it.
- **Don't decode further than necessary.** Linear projection is a primitive. You don't need to decode it into "matrix multiply, which is itself a sum of weighted columns…" unless the user asks. Decompose to the level the user needs and stop.
- **Don't conflate the construct with its claimed *purpose*.** Attention isn't "how transformers attend to relevant context" — that's its emergent behavior. The construct is softmax(QKᵀ/√d)V; the behavior emerges from training. Be precise about what the math forces vs. what learning produces.

## Quick Reference

| Construct | Primitives (in order) | Famous behavior emerges because… |
|---|---|---|
| Self-attention | Linear proj × 3 + dot product + scaled softmax + weighted sum | Each token learns to ask, advertise, deliver; the math implements soft database lookup |
| LayerNorm | Center + rescale + learnable affine | Standardizes per-example activations; γ, β preserve expressiveness |
| Softmax | Exp + normalize | Positivity + sum-to-1 + amplification of contrast |
| Cross-entropy | Log + weighted sum | Punishes low predicted prob on the true class |
| Conv layer | Weight-shared linear projection | Translation equivariance + parameter efficiency from sharing |
| ResNet block | f(x) + identity (residual) + nonlinearity | Identity path means gradients flow + small learned perturbations to the input |
| Dropout | Random binary mask + rescale | Forces redundancy; prevents co-adaptation |
| Diffusion (one step) | Noise injection (forward) + linear projection + nonlinearity (denoise) | Slow noise schedule lets simple regression learn complex distributions |
| SGD step | Gradient + scaled subtraction | Local descent on the loss surface |
| Adam step | Gradient + moving averages + per-coord rescale + scaled subtraction | Per-parameter adaptive learning rate from gradient statistics |
| Embedding | Index + lookup table | Discrete tokens get learnable continuous coordinates |
| Contrastive (InfoNCE) | Dot product + scaled softmax + cross-entropy | Pulls aligned pairs together, pushes others apart, all in one loss |

For the full decode of each construct, see [resources/constructs.md](resources/constructs.md).
For ablation tables for each construct, see [resources/ablations.md](resources/ablations.md).

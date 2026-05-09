---
name: worked-example-walkthrough
description: Produces step-by-step computational walkthroughs of vector and matrix operations as a sequence of numbered "frames", showing the explicit state at each step. The text-equivalent of a 3Blue1Brown animation — each frame shows what changed and why, so the learner can re-trace the operation by hand. Use when the learner needs to *see* a computation unfold (eigenvalue computation, attention with 3 tokens, gradient descent step, SVD on a 2×2, layer norm on a 3-vector, softmax of a small input), when an explanation has been given but the learner needs to ground it in a worked example, or when introducing an operation that's intimidating in symbol form but trivial in pencil-and-paper form.
---

# Worked Example Walkthrough

## Table of Contents
1. [Workflow](#workflow)
2. [Frame Anatomy](#frame-anatomy)
3. [Choosing the Right Example](#choosing-the-right-example)
4. [Common Patterns](#common-patterns)
5. [Guardrails](#guardrails)
6. [Quick Reference](#quick-reference)

A walkthrough is a sequence of numbered frames showing the state of a computation at each step. Each frame answers three questions: *what's the current state?*, *what operation produced it?*, and *what should the learner notice?*

This is the closest pure text gets to a 3Blue1Brown animation. The learner can re-trace the operation by hand, and the explicit intermediate states catch confusions that a final-result-only treatment hides.

**Quick example (Eigenvalues of a 2×2 matrix):**

> **Compute the eigenvalues of A = [[4, 1], [2, 3]].**
>
> **Frame 1.** State: A = [[4, 1], [2, 3]]. We want λ such that det(A − λI) = 0.
>
> **Frame 2.** Form A − λI:
> ```
> A - λI = [[4-λ,  1 ],
>          [ 2,  3-λ]]
> ```
>
> **Frame 3.** Compute the determinant:
> det = (4 − λ)(3 − λ) − 1·2 = (12 − 7λ + λ²) − 2 = λ² − 7λ + 10
>
> **Frame 4.** Solve λ² − 7λ + 10 = 0:
> Factor: (λ − 5)(λ − 2) = 0. So λ = 5 or λ = 2.
>
> **Frame 5.** Eigenvalues: 5 and 2. Quick sanity check: trace(A) = 4 + 3 = 7 = sum of eigenvalues ✓; det(A) = 12 − 2 = 10 = product of eigenvalues ✓.
>
> **What to notice:** The characteristic polynomial is just det(A − λI) expanded; finding eigenvalues is just root-finding. No magic.

Five frames, ~80 words. The learner can redo this on paper in under a minute.

## Workflow

Copy this checklist and track your progress:

```
Walkthrough Progress:
- [ ] Step 1: Pick the smallest possible example that exercises the concept
- [ ] Step 2: Write the goal — what we'll compute and why
- [ ] Step 3: Plan the frames (3-7 typically)
- [ ] Step 4: Write each frame: state, operation, notice
- [ ] Step 5: End with a sanity check or invitation to verify
- [ ] Step 6: Optional — invite the learner to redo with a variant
```

**Step 1: Pick the smallest possible example that exercises the concept**

The example must be *small*. 2×2 matrices, 3-vector inputs, 3-token sequences. Bigger examples obscure the structure with arithmetic.

The example must also *exercise* the concept — not just trivially demonstrate it. A diagonal matrix has trivial eigenvectors; pick a 2×2 that's not diagonal. A scalar attention is trivial; pick at least 3 tokens.

For a catalog of recommended example sizes per concept, see [resources/examples.md](resources/examples.md).

**Step 2: Write the goal — what we'll compute and why**

Single sentence. "Compute the eigenvalues of A = [[4, 1], [2, 3]]." or "Apply attention to a 3-token sequence with random Q, K, V vectors." The goal frames everything that follows.

**Step 3: Plan the frames (3-7 typically)**

Each frame is one operation. Sketch the frames before writing them out — this catches the "skipped step" problem before it hits the page.

A frame budget that works for most operations:
- 3 frames: trivial chain (one transformation)
- 5 frames: typical single-concept walkthrough (eigenvalues, softmax, single SGD step)
- 7 frames: compound walkthrough (attention with all sub-steps shown)

If you find yourself wanting >7 frames, either the example is too big (shrink) or the operation has multiple sub-operations that each deserve their own walkthrough.

**Step 4: Write each frame: state, operation, notice**

Each frame has three parts (see [Frame Anatomy](#frame-anatomy)):
- **State:** the current values, shown explicitly.
- **Operation:** what we just did to get here (or what we're about to do).
- **Notice:** one sentence pointing out something the learner might miss.

The "notice" is what distinguishes a walkthrough from a worked solution. A worked solution shows the steps; a walkthrough also says *what to look at*.

**Step 5: End with a sanity check or invitation to verify**

Every walkthrough ends with one of:
- A sanity check: "trace ✓, determinant ✓".
- A consistency check: "the result has the expected shape".
- An invitation: "try the same operation on A = [[1, 2], [3, 4]]; the answer should be λ ≈ −0.37 and λ ≈ 5.37."

The sanity check is what tells the learner the result is right. It also doubles as a *reusable verification trick* they can apply to similar problems.

**Step 6 (optional): Invite the learner to redo with a variant**

If the learner has time and the example is short, invite them to redo with a small change:
- "Same matrix, different starting vector: redo with v = (0, 1) instead of (1, 0)."
- "Same attention computation, but with one token's K replaced by zero: predict the change to the output before computing."

Variants check whether the *picture* transferred, not just the arithmetic.

## Frame Anatomy

Each frame has three parts. Keep them visually distinct.

```
**Frame N.** [Operation: short verb phrase, what we're doing.]
[State: explicit values, in a code block if needed.]
[Notice: one sentence — what to look at.]
```

### State block

Use a code block for matrices, vectors, and equations. Show actual numbers; resist the urge to leave things symbolic. The point is *concreteness*.

```
v = (3, 4)
|v| = √(3² + 4²) = √25 = 5
```

### Operation phrase

Short verb phrase: "Compute…", "Apply…", "Substitute…", "Solve…". One line.

### Notice sentence

One sentence pointing at the most important feature of this frame.
- "The cross terms cancelled — that's because A is symmetric."
- "Notice the second eigenvalue is negative — A reflects along that direction."
- "The softmax peaked on the first row — token 1's query strongly matched key 1."

If a frame doesn't earn a notice sentence, it might not need to be its own frame. Consider merging.

## Choosing the Right Example

The example you choose makes or breaks the walkthrough. Heuristics for choosing:

### Use specific small numbers, not symbols
A walkthrough with `a, b, c, d` is a *derivation*, not a walkthrough. Pick numbers like 2, 3, 1, −1 — small enough to compute by eye, varied enough to expose pattern.

### Avoid the simplest possible case
Identity matrix, zero vector, all-equal scores — these are *too* trivial; they don't exercise the operation. The walkthrough learner needs to see what happens when the operation is *non-trivially active*.

### Pick examples with verifiable properties
Symmetric matrices have real eigenvalues — easy to spot a bug. Stochastic matrices have a stationary distribution — easy to verify. Pick examples with these checkable properties so Step 5's sanity check is meaningful.

### When in doubt, use the smallest non-trivial size
- Matrices: 2×2 first; 3×3 only if 2×2 doesn't exercise the concept.
- Vectors: 2D or 3D.
- Sequences: 3 tokens minimum (so attention is interesting), 4 if you need parity.
- Networks: 1-layer, 2-input, 1-output minimum (for backprop demos).

For a recommended example per concept, see [resources/examples.md](resources/examples.md).

## Common Patterns

### Pattern A: Single computation walkthrough
Used for one-shot operations: eigenvalue compute, single SGD step, single attention forward pass, softmax of a vector.
Length: 3-5 frames.
Closing: sanity check.

### Pattern B: Iterative walkthrough
Used for processes that loop: gradient descent over multiple steps, power iteration finding eigenvectors, diffusion sampling.
Length: 5-7 frames showing 2-3 iterations explicitly, then "and so on…".
Closing: convergence comment + invitation to predict the limit.

### Pattern C: Comparative walkthrough
Used to show the *contrast* between two operations: matrix-vector mul as row-dot vs as column-combination; layer norm vs batch norm; SGD vs Adam on the same gradient.
Length: parallel frames in two columns or two passes.
Closing: bridge sentence on what makes them equivalent or different.

For one filled walkthrough per pattern, see [resources/examples.md](resources/examples.md).

## Guardrails

- **Show actual numbers, not symbols.** A walkthrough with `Av` is a derivation; a walkthrough with `[5, 11]` is a walkthrough. The learner needs to *see* the values.
- **Don't skip arithmetic the learner might be uncertain about.** "(4−λ)(3−λ) − 2 = λ² − 7λ + 10" is fine; "(4−λ)(3−λ) − 2 = (λ−5)(λ−2)" skips the expansion. Give them the polynomial first, then factor.
- **Each frame should advance the state.** A frame whose state is identical to the previous one (just rephrased) is wasted.
- **Use only one operation per frame.** Two operations in one frame is two frames.
- **Don't bury the punchline in arithmetic.** End with the result clearly stated and the sanity check explicit.
- **For long computations, consider Bash.** If the arithmetic is genuinely long (e.g., a 4×4 eigenvalue problem), use Bash to numpy the intermediate states — but still show the *operations* as frames. The Bash output is the verification, not the walkthrough.

## Quick Reference

| Operation | Recommended example | Frame count |
|---|---|---|
| Matrix-vector mul | A = [[1, 2], [3, 4]], v = (5, 6) | 3 |
| Eigenvalues | A = [[4, 1], [2, 3]] | 5 |
| Eigenvector for known λ | Same A, λ = 5 | 4 |
| SVD | A = [[3, 1], [1, 3]] (symmetric for clean SVD) | 6 |
| Softmax | x = (2, 1, -1) | 4 |
| Cross-entropy | p = (1, 0, 0), q = (0.7, 0.2, 0.1) | 3 |
| Single SGD step | Loss x², start at x = 4, η = 0.5 | 4 |
| Attention forward | 3 tokens, d = 2 | 7 |
| LayerNorm | x = (1, 5, 9) | 5 |
| Backprop on tiny net | y = w₂σ(w₁x), one input/output | 6 |
| PCA on tiny dataset | 4 points in 2D | 6 |

For full filled-in walkthroughs of each, see [resources/examples.md](resources/examples.md).

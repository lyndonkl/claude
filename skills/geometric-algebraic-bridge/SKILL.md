---
name: geometric-algebraic-bridge
description: Presents a math or ML concept simultaneously in geometric form (picture, transformation, region, surface) and algebraic form (formula, matrix, derivation), then writes the explicit one-sentence bridge that says "these are the same thing because…". The signature 3Blue1Brown move applied to any vector/matrix concept. Use when a learner has one view but not the other ("I understand the formula but not what it means" or "I see the picture but can't write it down"), when introducing a concept that genuinely needs both views to land (eigendecomposition, SVD, dot product, attention, gradient, covariance), or when the user mentions "geometric meaning", "intuition behind", "picture for", or "why does the formula look like that".
---

# Geometric-Algebraic Bridge

## Table of Contents
1. [Workflow](#workflow)
2. [The Bridge Sentence](#the-bridge-sentence)
3. [Layout Templates](#layout-templates)
4. [Common Patterns](#common-patterns)
5. [Guardrails](#guardrails)
6. [Quick Reference](#quick-reference)

A geometric picture without the algebra leaves the learner unable to compute. An algebraic formula without the picture leaves them unable to *see*. This skill produces both, side by side, with one sentence between them that says — in plain English — why they are the same thing.

The bridge sentence is the load-bearing piece. Without it, you've handed the learner two unrelated halves and made them do the joining themselves.

**Quick example (Dot product):**

> **Geometric:** Two arrows in the plane. The dot product a · b measures *how much one points along the other* — the projection of a onto b's direction, scaled by b's length.
>
> **Algebraic:** a · b = a₁b₁ + a₂b₂ + … + aₙbₙ. (Or equivalently, a · b = |a| |b| cos θ.)
>
> **Bridge:** The component-wise sum *is* the projection-times-length. You can prove it by writing a in coordinates aligned with b — the sum collapses to |a|cos θ × |b|, which is what projection-times-length says geometrically.

Three short blocks. The bridge is the last, and the only one that's not optional.

## Workflow

Copy this checklist and track your progress:

```
Bridge Progress:
- [ ] Step 1: Identify the concept and which view the learner has
- [ ] Step 2: Construct the missing view, kept short and concrete
- [ ] Step 3: Write the bridge sentence — one sentence, plain English
- [ ] Step 4: Verify the bridge with a small example
- [ ] Step 5: Invite the learner to confirm or push back
```

**Step 1: Identify the concept and which view the learner has**

Most users come with one view, not zero. Diagnose which:

- **Algebra-first learner** (most ML practitioners): "I understand the equation Av = λv but I can't see what it *means*." → Build the geometric view.
- **Geometry-first learner** (visual / physics-trained): "I get the picture of a rotation, but I don't know how to write it down." → Build the algebraic view.
- **Neither** (rarer): use the `concept-rediscovery-walk` skill instead — they need to invent the concept first.

A diagnostic question that almost always tells you which: "Can you predict what this concept does without computing? Or do you need to compute first?" Predict-without-compute = geometric; compute-first = algebraic.

**Step 2: Construct the missing view, kept short and concrete**

Build the missing view in 3-5 sentences. Length is a discipline: longer = more chance the learner loses the thread before the bridge.

- **For the geometric view:** Use a specific example (a 2×2 matrix, a small transformation, a labeled diagram). Prefer 2D unless the concept genuinely requires 3D.
- **For the algebraic view:** Show the formula, then *say what it does, term by term, in 1-2 sentences*. Don't drop the formula and walk away.

For per-concept layout templates, see [resources/templates.md](resources/templates.md). For full worked examples, see [resources/examples.md](resources/examples.md).

**Step 3: Write the bridge sentence — one sentence, plain English**

The bridge is the highest-leverage sentence in the response. It must:
- Be one sentence (two if absolutely necessary).
- Use plain English — no LaTeX, no symbols if avoidable.
- Say *why* the two views are the same thing — not just *that* they are.

Three bridge formulas that work for most concepts:

- **"X *is* Y, because…"** — direct identification. ("The dot product *is* the projection times length, because writing a in coordinates aligned with b collapses the sum to |a|cos θ × |b|.")
- **"X happens *because* Y."** — causal. ("Eigenvectors get only stretched, not rotated, because they're the directions where Av = λv — and λv is just a rescaling.")
- **"X is what Y looks like when you do Z."** — perspective shift. ("A matrix is what a linear transformation looks like once you pick a basis.")

The bridge fails when it just restates one view in symbols and the other in words without explaining the *why*. "Av = λv means v is left in place up to scaling" is not a bridge; it's a translation. The bridge is "and *that's why* it's the special direction the transformation can't rotate".

**Step 4: Verify the bridge with a small example**

After the bridge, run *one* small example end-to-end through both views:

- "Take A = [[2, 0], [0, 3]]. Geometrically, it stretches the x-axis by 2, the y-axis by 3. Algebraically, eigenvalues are 2 and 3, eigenvectors are (1, 0) and (0, 1). Same picture, same numbers — bridge confirmed."

The verification example should fit on one line if possible. Its purpose is to make the bridge *concrete* — not to teach a new concept.

**Step 5: Invite the learner to confirm or push back**

End with one of:
- "Does the bridge land? Or is there a step that still feels arbitrary?"
- "Try [small variant]. Predict the result both ways before computing."
- "What's still unclear?"

This catches the case where the bridge made sense to *you* but not to the learner. Bridges are subjective; the learner is the only judge.

## The Bridge Sentence

The bridge is a single sentence (or two) that explicitly identifies the geometric and algebraic descriptions as the same thing, with a *because*. It is the part of the explanation most often skipped, and the part most often missed by learners who say "I sort of get it but it doesn't click."

### What a good bridge does
- Names both views by their key noun. ("The eigenvector equation Av = λv corresponds to the *invariant direction* in the picture, *because* λv just rescales v without rotating it.")
- Includes the word "because" or its functional equivalent. The bridge is *causal*, not just declarative.
- Uses the most concrete language available. Prefer "stretched" over "scaled by a positive scalar"; prefer "the picture of an ellipsoid" over "a positive semidefinite quadratic form".

### What a bad bridge does
- Restates the formula. ("Av = λv means v is an eigenvector of A.") That's a definition, not a bridge.
- Hedges. ("These are essentially related…", "in some sense the same thing…") If you can't say *why*, you don't have a bridge yet.
- Skips the geometric noun. ("Eigenvectors satisfy Av = λv.") Where's the picture?

For a library of bridge sentences per concept, see [resources/templates.md](resources/templates.md).

## Layout Templates

### Template A: Bridge after both views (default)

```
**Geometric view.** [3-5 sentence picture, with one specific example.]

**Algebraic view.** [Formula, with 1-2 sentences saying what each term does.]

**Bridge.** [One sentence: X *is* Y because Z.]

**Verify on a tiny example.** [One-line check that both views give the same answer.]
```

Use when both views are roughly equal weight. This is the default.

### Template B: Lead with the missing view

```
**[The view the learner has].** You already have this — [restate in one sentence].

**[The missing view].** [3-5 sentences, ending in the formula or the picture.]

**Bridge.** [One sentence.]

**Verify.** [One line.]
```

Use when the learner has one view confidently and you don't want to belabor it.

### Template C: Three-column for compound concepts

```
| Geometric | Algebraic | Bridge |
|---|---|---|
| [Sentence] | [Formula] | [Why same] |
```

Use only for compound concepts with multiple sub-bridges (e.g., SVD = rotate, scale, rotate; attention = ask, match, mix). The table prevents the bridge from getting lost in prose.

For full filled-in templates per concept, see [resources/templates.md](resources/templates.md).

## Common Patterns

### Concepts where the bridge is the whole game
- Eigenvectors (formula ↔ invariant directions)
- Dot product (sum ↔ projection × length)
- Determinant (formula ↔ signed area scaling)
- Covariance matrix (formula ↔ ellipsoidal shape of data cloud)
- Softmax (formula ↔ point on the simplex; sharp at high contrast)
- Cross-entropy (formula ↔ surprise weighted by truth)
- Jacobian (matrix of partials ↔ local linear approximation)
- Outer product (rank-1 matrix ↔ "every row is a scaled copy of one row")

### Concepts where the picture leads
- Span / subspace
- Rank / null space (the four fundamental subspaces)
- Orthogonality
- Projection

### Concepts where the algebra leads
- Matrix multiplication (the picture is "compose two transformations" but the algebra is what you actually compute)
- Backprop (the picture is "chain rule on a graph" but the bookkeeping is algebraic)

For one filled template per concept type, see [resources/examples.md](resources/examples.md).

## Guardrails

- **One bridge sentence, not three.** If you find yourself writing a paragraph for the bridge, it's not crystallized yet. Cut.
- **Do not skip Step 4.** The verification example is what makes the bridge real. Without it, the learner has prose; with it, they have proof.
- **Do not present both views and walk away.** That's an exposition, not a bridge. The whole point is the joining.
- **Do not use the algebraic view as the bridge.** "Av = λv *is* the bridge" is a common failure. The bridge is the English sentence *connecting* Av = λv to "the direction A doesn't rotate."
- **Match formality to the learner.** A learner comfortable with proofs can take "by the inner product axioms…"; a learner who wants intuition cannot. Watch for jargon mismatch and adjust.

## Quick Reference

| Concept | Geometric noun | Algebraic form | Bridge sentence stub |
|---|---|---|---|
| Eigenvector | Direction A doesn't rotate | Av = λv | "...because λv is just a rescaling, no rotation." |
| Dot product | Projection × length | a₁b₁ + … + aₙbₙ | "...because aligning coordinates with b collapses the sum to \|a\|cos θ × \|b\|." |
| Determinant | Signed volume scale factor | det(A) formula | "...because the formula counts volume cell-by-cell with sign." |
| Covariance matrix | Shape of data cloud (ellipsoid) | Σᵢⱼ = E[(xᵢ−μᵢ)(xⱼ−μⱼ)] | "...because it stretches the unit ball into the cloud's shape." |
| Softmax | Point on the simplex | exp(xᵢ)/Σexp(xⱼ) | "...because exp ensures positivity, normalize ensures sum-to-1." |
| Jacobian | Local linear map at a point | matrix of ∂fᵢ/∂xⱼ | "...because it's the linear approximation of f near a point." |
| SVD | Rotate, scale, rotate | A = UΣVᵀ | "...because U is a rotation, Σ scales axis-aligned, Vᵀ is a rotation." |
| Outer product | Rank-1 matrix; rows are scaled v | uvᵀ | "...because each row is uᵢ times the row vector v." |

For full worked examples per concept, see [resources/examples.md](resources/examples.md). For per-concept templates with all four blocks filled in, see [resources/templates.md](resources/templates.md).

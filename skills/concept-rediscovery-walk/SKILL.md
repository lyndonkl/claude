---
name: concept-rediscovery-walk
description: Guides a learner to invent a math or ML concept themselves through a Socratic walk — a sequence of small guessable questions that ends with the learner stating the formal definition unprompted. The 3Blue1Brown signature move. Use when the learner is meeting a foundational concept (eigenvectors, gradient, attention, softmax, KL divergence) for the first time, when prior exposure produced memorization without understanding, or when the user says "explain it from scratch", "I want to really get it", "build it up for me", or "where does this come from".
---

# Concept Rediscovery Walk

## Table of Contents
1. [Workflow](#workflow)
2. [The Three Cuts](#the-three-cuts)
3. [Question Types](#question-types)
4. [Common Patterns](#common-patterns)
5. [Guardrails](#guardrails)
6. [Quick Reference](#quick-reference)

The principle is simple: a learner who *guesses* the equation `Av = λv` from "what would survive a transformation unchanged?" owns eigenvectors in a way that no exposition can match. This skill structures the walk that makes that guess possible.

**Quick example (Eigenvectors):**

> **Set the seed:** "Picture any 2D matrix as a transformation that bends the plane — most arrows get rotated and stretched. But are there special arrows that *only* get stretched, not rotated?"
>
> **Let them guess:** "What would such an arrow satisfy, if A is the matrix?"
> *Learner:* "Av is parallel to v?"
>
> **Tighten:** "Right — and 'parallel' means equal up to a scalar. So we need…?"
> *Learner:* "Av = λv for some number λ."
>
> **Name what they invented:** "You just wrote the eigenvector equation. v is an eigenvector, λ is its eigenvalue. Now we never have to introduce them — you derived them."

Ten lines. The learner did most of the talking. That is the move.

## Workflow

Copy this checklist and track your progress:

```
Rediscovery Walk Progress:
- [ ] Step 1: Identify the concept and its motivating question
- [ ] Step 2: Choose the seed observation (the door)
- [ ] Step 3: Plan the question ladder (3-5 rungs to the definition)
- [ ] Step 4: Walk the learner up the ladder, one guess at a time
- [ ] Step 5: Name what they invented; restate it cleanly
- [ ] Step 6: Verify ownership with a small unfamiliar question
```

**Step 1: Identify the concept and its motivating question**

Every concept exists because it answers a question. Before walking, pin down what the question is. Eigenvectors answer "which directions does this transformation leave alone?" Gradient answers "which way is uphill steepest?" Softmax answers "how do I turn arbitrary scores into a probability distribution?" If you cannot state the motivating question in one sentence, you have not understood the concept well enough to walk anyone to it.

For a catalog of motivating questions per concept, see [resources/examples.md](resources/examples.md).

**Step 2: Choose the seed observation (the door)**

The seed is a concrete observation or scenario that makes the motivating question feel natural. Three good seed types:

- **A specific transformation the learner can picture** ("Consider the matrix [[2, 1], [1, 2]] applied to the plane…")
- **A familiar problem with a missing piece** ("You want to combine 3 scores into a probability distribution. The scores can be negative. Adding doesn't work. What might?")
- **A phenomenon they've seen but not named** ("In any high-dim Gaussian, samples cluster near a thin shell, not at the origin. Why might that be?")

Pick the seed that requires the least background to grasp. Bad seeds open with formalism ("Let A be a square matrix over ℝ…"); good seeds open with a picture or a problem.

**Step 3: Plan the question ladder (3-5 rungs to the definition)**

Sketch the ladder *before* you start walking. Each rung is a question the learner can answer with what they already know plus the seed. The last rung's answer is the formal concept.

A good ladder has these properties:
- Each rung is *guessable* — not "deduce it" but "what would you propose?"
- No rung skips. If you find yourself thinking "and then obviously…", insert a rung.
- The ladder ends when the learner has *spoken* the definition, not when you've stated it.

For ladder templates by concept, see [resources/examples.md](resources/examples.md). For ladder design heuristics, see [resources/methodology.md](resources/methodology.md).

**Step 4: Walk the learner up the ladder, one guess at a time**

Ask the rung. Wait for the answer. If the answer is right, name it cleanly and ask the next rung. If the answer is partial, affirm what's right and probe the gap ("Yes — and what about the other direction?"). If the answer is wrong, do not correct — *probe*: "What made you think that? Let's test it on a tiny example."

The ratio matters: aim for the learner to type more than you do during this phase. If you find yourself writing paragraphs while waiting, your rung was too vague — break it smaller.

**Step 5: Name what they invented; restate it cleanly**

After the last rung, do this in two beats:

1. **Name it:** "You just wrote the eigenvector equation."
2. **Restate cleanly:** "Eigenvector: a vector v such that Av = λv. Eigenvalue: the scalar λ. Geometrically: the direction A doesn't rotate; the factor it stretches by."

This is the *only* moment the formal definition appears. It appears at the end, as a compression of what the learner already understands. Sanderson's principle, applied: definitions are the ending point, not the start.

**Step 6: Verify ownership with a small unfamiliar question**

Ownership ≠ recognition. Test with a question they haven't been walked through:

- "If A = 2I (the identity scaled by 2), what are its eigenvectors? Why does that answer feel weird?"
- "If A is a 90° rotation, what are its real eigenvectors? Why?"

Answers reveal whether the picture stuck. A learner who sees the rotation case has no real eigenvectors *because no real direction is left unrotated* has the picture. A learner who says "I'd have to compute the characteristic polynomial" has memorization, not understanding — back to Step 4 with a different angle.

## The Three Cuts

If a walk is dragging, almost always one of these cuts will fix it.

**Cut 1: Cut the setup.** If your seed needs more than two sentences to land, the seed is wrong. Pick a more concrete one.

**Cut 2: Cut the lecture.** If you find yourself explaining for more than three sentences before the next question, you've stopped walking and started telling. Break it into a question.

**Cut 3: Cut the rung count.** If you planned 7 rungs, half of them are filler. The walk usually wants 3-5. More rungs = more places for the learner to lose the thread.

## Question Types

The walk uses four kinds of questions; rotate them.

**1. Picture-prompts** (lowest friction, use early)
- "Picture a matrix as a transformation. What kinds of motion can it do?"
- "Imagine a cloud of data points. What shape might 'best fit' it?"

**2. Goal-prompts** (set up the search)
- "We want to combine these scores into a probability distribution. What's the obvious problem?"
- "We want a direction that's left alone. What equation captures 'left alone'?"

**3. Test-prompts** (force concreteness)
- "What does this matrix do to the vector (1, 0)? What about (0, 1)?"
- "If you took softmax of (10, 0, 0), what would you get? What about (1, 0, 0)?"

**4. Anomaly-prompts** (productive surprise)
- "What if we tried this transformation on a 90° rotation matrix? What goes wrong?"
- "What if all the scores were 0? Does softmax still work?"

If a learner stalls on one type, switch to another. Picture-prompts unstick most stalls.

## Common Patterns

### Pattern A: Single-concept walk
Used for: eigenvectors, gradient, dot product, softmax, cross-entropy, Jacobian.
Structure: seed → 3-5 rungs → name → verify.
Length: ~10 exchanges, ~5 minutes.

### Pattern B: Compound walk
Used for: attention (Q, K, V — 3 sub-walks fused), backprop (chain rule + reverse mode), PCA (covariance + eigenstuff).
Structure: walk to each sub-concept separately, then a final rung that fuses them.
Length: ~25 exchanges, ~15 minutes.

### Pattern C: Anomaly-first walk
Used for: high-dim phenomena (concentration of measure), counterintuitive results (KL asymmetry).
Structure: present the anomaly → "guess why" → walk through the intuition repair.
Length: ~10 exchanges.

For one full walked example per pattern, see [resources/examples.md](resources/examples.md).

## Guardrails

- **Do not skip Step 6.** A walk without verification is just performance. The whole point is the unfamiliar-question test at the end.
- **Do not do all the talking.** If the learner has not typed an answer in the last 3 turns, the walk has failed. Stop and ask them to attempt the rung explicitly.
- **Do not correct wrong guesses by stating the right answer.** Probe what produced the guess. Wrong guesses are diagnostic gold; treat them that way.
- **Do not name the concept before Step 5.** Saying "this is the eigenvector equation" mid-walk collapses the rediscovery into recognition.
- **Match speed to comfort.** A confident learner can take 2-rung jumps. A struggling learner needs 1-rung steps. Read their answers for confidence cues ("oh!" = speed up; "I think maybe…" = slow down).

## Quick Reference

| Concept | Seed | Final rung |
|---|---|---|
| Eigenvectors | "Most arrows get rotated and stretched. Are there ones that only get stretched?" | "Av = λv" |
| Gradient | "On a hilly surface, you want to climb fastest. Which way?" | "The vector of partial derivatives" |
| Dot product | "When are two vectors 'similar'?" | "a·b = \|a\|\|b\|cos θ" |
| Softmax | "Turn arbitrary scores into a probability distribution." | "exp(xᵢ)/Σexp(xⱼ)" |
| Attention Q | "Each token needs to ask the others for info. What does 'asking' look like as a vector?" | "The query vector" |
| Cross-entropy | "How do we measure how 'wrong' a predicted distribution is?" | "−Σpᵢ log qᵢ" |
| Jacobian | "Derivative is a number for f: ℝ→ℝ. What is it for f: ℝⁿ→ℝᵐ?" | "The matrix of partial derivatives" |

For full walked dialogues per concept, see [resources/examples.md](resources/examples.md).

For the deeper methodology behind seed selection and rung sizing, see [resources/methodology.md](resources/methodology.md).

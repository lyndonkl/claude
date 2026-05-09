# Bridge Examples by Learner Type

Worked examples showing how the bridge changes depending on which view the learner already has. Each pair illustrates the same concept, bridged from two starting points.

## Contents
- Eigenvectors (algebra-first vs geometry-first learner)
- Attention (algebra-first vs geometry-first learner)
- Convolution (algebra-first vs geometry-first learner)
- Layer norm (algebra-first learner — most common case)
- KL divergence (special case: bridging the asymmetry)

---

## Eigenvectors

### Algebra-first learner

> **Learner says:** "I can compute eigenvalues by solving det(A − λI) = 0 but I don't know what they *mean*."

**You already have the formula.** Av = λv, eigenvalues are roots of det(A − λI) = 0 — that part you've got.

**The picture.** A 2×2 matrix is a transformation of the plane. Pick any arrow; A bends it into a new direction *and* changes its length. Most arrows experience both. But some matrices have special arrows that A only stretches, never rotates. The eigenvectors *are* those special arrows. The eigenvalues are how much they stretch.

**Bridge.** Av = λv is the algebraic way of saying "v's direction is left alone, only its length scales by λ" — because λv is just v rescaled, with no change in direction.

**Verify.** A = [[2, 0], [0, 3]] stretches x by 2 and y by 3, no rotation. The eigenvectors are (1, 0) and (0, 1) (the special directions). The eigenvalues are 2 and 3 (the stretch factors). Same numbers as the formula gives.

### Geometry-first learner

> **Learner says:** "I get the picture — directions a transformation doesn't rotate. But how do I find them?"

**You already have the picture.** Eigenvectors are the special directions A leaves alone (up to stretching). Eigenvalues are the stretch factors.

**The formula.** "Direction left alone, only stretched" means Av is just v rescaled: Av = λv. To solve for v, rewrite as (A − λI)v = 0. For a non-zero v to satisfy this, the matrix (A − λI) must be singular, which means det(A − λI) = 0. That equation gives the eigenvalues; substituting each back into (A − λI)v = 0 gives the corresponding eigenvectors.

**Bridge.** The "no rotation" picture forces the equation Av = λv, because λv is the only way for the result to be v with just a length change.

**Verify.** A 90° rotation matrix has *no* real eigenvectors — every direction gets rotated. Algebraically: det(A − λI) = λ² + 1, which has no real roots. The picture and the algebra agree.

---

## Attention

### Algebra-first learner

> **Learner says:** "I can read softmax(QKᵀ)V but I have no intuition for what Q, K, V mean."

**You already have the formula.** Output = softmax(QKᵀ)V. Each token has three vectors: Q (query), K (key), V (value).

**The picture.** Each token in the sequence is doing three things at once:
- *Asking* the rest of the sequence a question: that's Q.
- *Advertising* what it has to offer: that's K.
- *Holding* the actual content it can deliver: that's V.

QKᵀ is the matrix of all pairwise question-meets-advertisement scores — how well does token i's question match token j's advertisement? Softmax row-normalizes those scores into mixing weights. Multiplying by V is then a weighted average over the actual content each token can deliver, with weights determined by how well their advertisements matched i's question.

**Bridge.** softmax(QKᵀ)V *is* "for each token, ask its question, get a soft match score against every other token's advertisement, then take a weighted average of their content." Q, K, V have those three roles because the math forces them to: Q meets K via dot product (the question matches the advertisement), softmax sharpens into selection weights, V is what gets selected and averaged.

**Verify.** If token i's Qᵢ aligns perfectly with token j's Kⱼ and is orthogonal to all other K's: QᵢKᵀ has one large entry (at j), softmax → ≈ 1 at j and 0 elsewhere, output ≈ Vⱼ. Token i pulls only from token j. Perfect content-based addressing.

### Geometry-first learner

> **Learner says:** "I get that attention is a soft database lookup, but how is that turned into a formula?"

**You already have the picture.** Soft database lookup: each token asks a question, finds the best-matching keys, pulls the associated values.

**The formula.** Make the question a vector — call it Q. Make each token's advertisement a vector — call it K. Make each token's actual content a vector — call it V. To measure "how well does this question match this key", use the dot product: QᵢKⱼᵀ. Stack these into a matrix QKᵀ. To turn raw scores into mixing weights, apply softmax row-wise. To pull the weighted content, multiply by V. Result: softmax(QKᵀ)V.

**Bridge.** The picture *forces* the formula, because every step of the database-lookup picture has a unique linear-algebra realization: dot products for similarity, softmax for soft selection, weighted sum for retrieval.

**Verify.** What does this look like for a 1-token "sequence"? QKᵀ is 1×1, softmax gives 1, output = V. The token attends only to itself. Matches the picture: with no neighbors, lookup returns your own content.

---

## Convolution

### Algebra-first learner

> **Learner says:** "I can implement a convolution as nested for-loops but I don't see what it *is*."

**You already have the formula.** For each output position (i, j), output[i, j] = Σ filter[k, l] · input[i+k, j+l]. The filter slides; at each position, do an element-wise multiply and sum.

**The picture.** The filter is a small pattern — say, an edge detector. At every position in the input, you're asking "how much does the local patch here look like my filter?" The output is a heatmap: bright where the local patch matches the filter, dim where it doesn't.

**Bridge.** The element-wise multiply-and-sum *is* the dot product between the filter and the local patch — and dot product measures alignment, so the output at each position is "how aligned is the patch here with the filter."

**Verify.** Use a horizontal-edge filter: [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]. At a flat region (all pixels equal), the dot product is 0 — no edge. At a horizontal edge (top row dark, bottom row bright), the dot product is large — strong response. The picture predicts what the math computes.

### Geometry-first learner

> **Learner says:** "I get that conv slides a filter and looks for matches. How is that a linear layer?"

**You already have the picture.** Filter slides; output is the alignment heatmap.

**The formula.** A convolution with a small filter is *equivalent* to a giant matrix multiplication where most of the matrix is zeros and the non-zero entries are forced to repeat (weight sharing). If the input is flattened to a vector, the convolution is a structured linear map — the matrix has a Toeplitz-like structure (constant along diagonals because the same filter is reused at every position).

**Bridge.** "Sliding filter" *is* a special pattern of weight sharing in a linear layer, because reusing the same filter at every spatial position is what produces the repeated entries in the giant matrix.

**Verify.** Count parameters. A fully-connected layer from a 28×28 input to a 28×28 output has 784² ≈ 615K parameters. A 3×3 convolution producing the same output uses just 9. The picture (sliding filter) and the math (sparse, weight-shared linear map) explain that 68000× reduction.

---

## Layer norm (algebra-first; the typical case)

> **Learner says:** "I know layer norm is (x − μ)/σ then γ·… + β. But why?"

**The picture.** Take the activations of one layer for one example as a cloud of numbers. They might be drifting — mean far from 0, variance far from 1. Layer norm grabs the cloud and:
1. Slides it to be centered at 0 (subtract the mean).
2. Squeezes it to have unit variance (divide by std).
Then learnable γ, β allow the network to *redo* any shift and scale that's actually useful for the next layer.

**Bridge.** The formula (x − μ)/σ *is* "recenter and rescale this layer's activations to a standard shape", because subtracting the mean is recentering and dividing by the std is rescaling — the simplest possible canonicalization.

**Verify.** Apply layer norm to (1, 5, 9). μ = 5, σ ≈ 3.27. Output ≈ (−1.22, 0, 1.22). Mean is 0, std is 1. Confirmed: standard shape.

---

## KL divergence — bridging the asymmetry

> **Learner says:** "Why is KL(p‖q) ≠ KL(q‖p)? Distances should be symmetric."

**The picture.** KL divergence is *not* a distance — it's an *expected log-ratio*. KL(p‖q) asks: "if I sample from p but assume q, how surprised am I on average?" KL(q‖p) asks the *opposite* question: "if I sample from q but assume p, how surprised am I on average?" These are different scenarios — different *truths* and different *assumptions* — so they give different numbers.

**The formula.** KL(p‖q) = Σ p(x) log[p(x)/q(x)]. The expectation is taken under *p*. Switch to KL(q‖p): expectation is under *q*. The asymmetry is structurally baked in.

**Bridge.** KL(p‖q) ≠ KL(q‖p) *because* the two formulas take expectations under different distributions — and since the expectation is what averages the surprise, weighting by p vs weighting by q gives different averages.

**Verify.** Take p = (0.99, 0.01), q = (0.5, 0.5).
- KL(p‖q) = 0.99·log(0.99/0.5) + 0.01·log(0.01/0.5) ≈ 0.673 + (−0.039) ≈ 0.634.
- KL(q‖p) = 0.5·log(0.5/0.99) + 0.5·log(0.5/0.01) ≈ −0.341 + 1.957 ≈ 1.616.

Very different. The intuition: under q, both outcomes are equally likely, so the rare-under-p outcome (the second one) gets full weight in the expectation. Under p, that outcome almost never happens, so its big surprise gets crushed by its low probability. *That's* the asymmetry, geometrically.

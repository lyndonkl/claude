# Worked Walks

One full walked dialogue per pattern. Use these as both examples and templates — adapt the seeds and rungs to the learner.

## Contents
- Eigenvectors (single-concept walk)
- Gradient (single-concept walk)
- Softmax (single-concept walk)
- Attention Q/K/V (compound walk)
- PCA (compound walk)
- Concentration of measure (anomaly-first walk)
- Cross-entropy (single-concept walk)
- Jacobian (single-concept walk)

---

## Eigenvectors (single-concept walk)

**Coach:** Picture any 2×2 matrix as a transformation of the plane. It takes every arrow and bends it — most arrows get *both* rotated and stretched. Quick check: if A = [[2, 0], [0, 3]], what does it do to the arrow (1, 0)?

**Learner:** Stretches it to (2, 0).

**Coach:** Right. And to (0, 1)?

**Learner:** (0, 3).

**Coach:** Notice anything special about those two arrows compared to a generic one like (1, 1)?

**Learner:** They didn't change direction, just length.

**Coach:** Exactly. Most arrows get rotated *and* stretched, but those two only got stretched. Now the question: for a *general* matrix A, are there always arrows that only get stretched? And what equation would such an arrow satisfy?

**Learner:** Hmm — Av is parallel to v?

**Coach:** Yes. And "parallel" means equal up to a scalar. So we want…?

**Learner:** Av = λv, for some number λ.

**Coach:** That's the eigenvector equation. v is an *eigenvector* of A; λ is its *eigenvalue*. Geometrically: the direction A doesn't rotate; the factor it stretches by.

**Verification rung:** If A is a 90° rotation matrix, what are its real eigenvectors?

**Learner:** ...none? Because every direction gets rotated.

**Coach:** Correct, and you just felt *why* — not from the characteristic polynomial, but from the picture. That's the test.

---

## Gradient (single-concept walk)

**Coach:** You're standing on a hilly landscape and want to climb as fast as possible. You can step in any direction — north, south, northwest, etc. How would you decide which direction to step?

**Learner:** Whichever direction goes uphill steepest.

**Coach:** Right. Now suppose the landscape's height at each (x, y) is given by a function f(x, y). What information about f tells you which direction is steepest?

**Learner:** Probably the partial derivatives — how much height changes per step in x and per step in y.

**Coach:** Good. ∂f/∂x is the slope in the x-direction, ∂f/∂y in the y-direction. But you don't have to step purely in x or purely in y. You can step in any direction. If you take a small step in some direction (a, b), how much does height change?

**Learner:** Roughly a · ∂f/∂x + b · ∂f/∂y?

**Coach:** Exactly — that's the linear approximation. Now: among all unit-length directions (a, b), which one maximizes that quantity?

**Learner:** ...the one that's parallel to (∂f/∂x, ∂f/∂y)?

**Coach:** Yes — by the dot product rule, a · u is maximized when a points the same way as u. So the direction of steepest ascent is the vector (∂f/∂x, ∂f/∂y). That vector has a name: the *gradient* of f, written ∇f.

**Verification rung:** If you wanted to descend fastest (e.g., minimize a loss), which way would you step?

**Learner:** The negative gradient.

**Coach:** That's gradient descent in one sentence.

---

## Softmax (single-concept walk)

**Coach:** Suppose your model spits out raw scores for 3 classes: (2, 1, -1). You need to turn these into a probability distribution — three numbers that are non-negative and sum to 1. What's the most obvious thing to try?

**Learner:** Just normalize? Divide by the sum?

**Coach:** Try it. What's 2 / (2 + 1 + (-1))?

**Learner:** 2 / 2 = 1. And 1 / 2 = 0.5. And -1 / 2 = -0.5.

**Coach:** That's a problem. Why?

**Learner:** Negative probability.

**Coach:** Right. So before normalizing, we need a function that turns any real number into a positive one. What's a natural choice?

**Learner:** Exponential? exp(x) is always positive.

**Coach:** Yes. So: take exp of each score, then normalize. Write that out for our (2, 1, -1).

**Learner:** (exp(2), exp(1), exp(-1)) / (exp(2) + exp(1) + exp(-1)).

**Coach:** That's softmax. The general formula: softmax(x)ᵢ = exp(xᵢ) / Σⱼ exp(xⱼ). You just derived it.

**Verification rung:** What does softmax of (10, 0, 0) look like? What about (1, 0, 0)? What's that telling you?

**Learner:** (10, 0, 0) gives almost (1, 0, 0). (1, 0, 0) gives something like (0.58, 0.21, 0.21). It's like… the bigger the gap between scores, the more confident the distribution.

**Coach:** Exactly. Softmax is a *soft* argmax — sharper at high contrast, flatter at low contrast. That's the intuition the formula encodes.

---

## Attention Q/K/V (compound walk)

This is three single-concept walks fused at the end.

**Coach:** Imagine you have a sequence of tokens, each represented by a vector. Each token needs to gather information from the others — but selectively, not uniformly. What does each token need, conceptually, to do this?

**Learner:** Some way of asking the others "do you have what I need?"

**Coach:** Right. So each token has a *question* it's asking the others. As a vector, what would we call that?

**Learner:** A query vector. Q.

**Coach:** Good. But a question only works if the others are *advertising* what they have. So each token also needs to publish a description of itself. What's that?

**Learner:** A key vector. K.

**Coach:** Right. Now: how do you measure how well one token's query matches another token's key?

**Learner:** Dot product?

**Coach:** Yes — high dot product = good match. So for each pair of tokens (i, j), we compute Qᵢ · Kⱼ. Stack these into a matrix; you get QKᵀ — every query meeting every key. Now we have a similarity score for every pair. But these scores aren't yet probabilities — what would we apply to make them mixing weights?

**Learner:** Softmax, row-wise.

**Coach:** Exactly. Now each row tells token i how much to listen to each other token. Last piece: what does token i actually pull *from* the others? Not their keys — those were just for matching.

**Learner:** ...a third vector? The actual content?

**Coach:** Yes — call it V, the value vector. Each token publishes K (what it advertises) and V (what it can deliver). So: token i's output is a weighted average of all the V vectors, weighted by the row of softmax(QKᵀ) corresponding to i. That's attention.

**Verification rung:** If token i's query Qᵢ is exactly aligned with token j's key Kⱼ and orthogonal to all the others, what's token i's output?

**Learner:** Just Vⱼ. Token i pulls only from token j.

**Coach:** Right — perfect content-based addressing. The whole mechanism is a soft, learned database lookup.

---

## PCA (compound walk)

**Coach:** You have a cloud of 2D data points and want to summarize it with one number per point. Which direction in the plane should you project onto, to lose the least information?

**Learner:** The direction the cloud is most spread out along?

**Coach:** Exactly — the long axis of the cloud. Now: what mathematical object captures the *shape* of a data cloud — its spread in different directions?

**Learner:** The covariance matrix?

**Coach:** Right. Σᵢⱼ tells you how features i and j vary together. Now think of the covariance matrix as a transformation. What does it geometrically represent?

**Learner:** ...some kind of stretch?

**Coach:** Yes — it stretches the unit ball into an ellipsoid that has the same shape as the data cloud. So now the question becomes: what are the *axes* of an ellipsoid produced by a matrix?

**Learner:** ...the eigenvectors?

**Coach:** Exactly. The eigenvectors of the covariance matrix are the principal axes of the data ellipsoid. The eigenvalues are the *spread* along each axis. So:

- Largest eigenvalue → direction of greatest variance → the first principal component.
- Second largest → direction of next-greatest variance, perpendicular to the first.
- And so on.

PCA is just: take the covariance matrix, find its eigenvectors, project onto the top k. You just derived it.

**Verification rung:** Why do we want eigenvectors of *covariance* specifically, and not some other matrix?

**Learner:** Because covariance is the matrix that captures spread, and eigenvectors give the natural axes of any matrix's stretch.

**Coach:** That's the whole story.

---

## Concentration of measure (anomaly-first walk)

**Coach:** Here's a fact that's going to feel wrong: in 1000-dimensional Gaussian, samples cluster near a *thin shell* at radius √1000, not near the origin. Even though the density is highest at the origin. Why might that be?

**Learner:** ...wait, the density is highest at the origin but samples aren't near it?

**Coach:** Right. Try this: in d dimensions, how does the volume of a thin spherical shell at radius r scale with r?

**Learner:** As r^(d-1), I think. Surface area scales that way.

**Coach:** Yes. So even though density per unit volume is highest at r = 0, the *amount of volume available* at radius r grows fast with r. In high d, that growth crushes the density falloff. Where would you expect samples to land?

**Learner:** Wherever density × volume is maximized. Not at the origin, because there's almost no volume there.

**Coach:** Exactly. Take the derivative of (density × volume) with respect to r. For Gaussian in d dimensions, the maximum is around r = √d. So samples land in a shell at √d. Almost none near the origin, almost none far outside the shell.

**Verification rung:** Your 3D intuition says "sample from a Gaussian, you mostly get points near the mean". Does that intuition extrapolate to 1000D?

**Learner:** No — in high dim, you almost never get points near the mean. They're all on the shell.

**Coach:** That's concentration of measure. Your 3D intuition is *wrong* for high dim, and now you know why.

---

## Cross-entropy (single-concept walk)

**Coach:** Your model predicts a probability distribution q over classes; the true label is some distribution p (often a one-hot vector). You need a single number that says "how wrong is q?" What properties should that number have?

**Learner:** Should be 0 if q = p. Bigger if q is far from p. ...non-negative?

**Coach:** Good. And it should especially punish q for putting low probability on the *true* class. If the true class is class 3 and q says P(class 3) = 0.001, that should hurt a lot.

**Learner:** So we want something that blows up as q(true class) → 0?

**Coach:** Right. What function blows up at 0?

**Learner:** −log? log(0) = −∞, so −log(0) = +∞.

**Coach:** Yes. So for a one-hot true label, the loss is just −log q(true class). For a general distribution p, weight each class by how true it is: −Σᵢ pᵢ log qᵢ. That's cross-entropy. You derived it from "punish low probability on truth."

**Verification rung:** If p and q are identical, what's the cross-entropy? Will it be zero?

**Learner:** ...let me check. If p = q = (0.5, 0.5), it's −0.5 log 0.5 − 0.5 log 0.5 = log 2. Not zero.

**Coach:** Right — cross-entropy of p with itself is the *entropy* of p, which is non-zero unless p is one-hot. The thing that's zero when p = q is *KL divergence*: KL(p‖q) = cross-entropy − entropy. Cross-entropy is "loss"; KL is "distance" (sort of — it's not symmetric). That asymmetry is its own walk.

---

## Jacobian (single-concept walk)

**Coach:** For a function f: ℝ → ℝ, the derivative at a point is just one number — the local slope. Now consider f: ℝⁿ → ℝᵐ. What's the derivative?

**Learner:** ...partial derivatives?

**Coach:** There are a lot of those — n inputs, m outputs, so n·m of them. But what does "the derivative at a point" *mean* geometrically, even in 1D?

**Learner:** The slope of the best-fitting line at that point.

**Coach:** Right — the *local linear approximation*. For f: ℝⁿ → ℝᵐ, what's the local linear approximation?

**Learner:** ...a linear map from ℝⁿ to ℝᵐ?

**Coach:** Exactly. And what represents a linear map from ℝⁿ to ℝᵐ?

**Learner:** A matrix. m by n.

**Coach:** That matrix is the Jacobian. Its (i, j) entry is ∂fᵢ/∂xⱼ. The Jacobian *is* the derivative for vector-valued functions — it's the matrix that linearly approximates f near a point.

**Verification rung:** For f: ℝⁿ → ℝ (scalar output), what shape is the Jacobian? And what's it usually called?

**Learner:** 1 × n. ...the gradient? Transposed?

**Coach:** Yes — the gradient is the Jacobian of a scalar-valued function. They're the same object, viewed differently. Once you see the Jacobian as "the local linear map", gradient becomes a special case.

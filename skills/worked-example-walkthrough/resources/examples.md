# Filled Walkthroughs

One full walkthrough per common operation. Each example is small enough to redo on paper in under 2 minutes. Use as templates — adapt the numbers but keep the frame structure.

## Contents
- Matrix-vector multiplication (two views)
- Eigenvalue computation (2×2)
- Finding the eigenvector for a known eigenvalue
- Softmax of a small vector
- Single SGD step
- Attention forward pass (3 tokens, d=2)
- LayerNorm on a 3-vector
- Backprop through a tiny network
- PCA on 4 points in 2D
- Power iteration (3 iterations)
- Single diffusion denoising step

---

## Matrix-vector multiplication (two views)

**Goal:** Compute Av for A = [[1, 2], [3, 4]], v = (5, 6) — once as row-dot-vector, once as weighted column combination.

**Frame 1 (row-dot view).** Multiply each row of A by v.
```
Row 0: (1, 2) · (5, 6) = 1·5 + 2·6 = 5 + 12 = 17
Row 1: (3, 4) · (5, 6) = 3·5 + 4·6 = 15 + 24 = 39
```
Result: Av = (17, 39).

**Frame 2 (column-combination view).** Treat v as weights for A's columns.
```
v[0] · A[:,0] = 5 · (1, 3) = (5, 15)
v[1] · A[:,1] = 6 · (2, 4) = (12, 24)
Sum: (5+12, 15+24) = (17, 39)
```
Same answer.

**Frame 3 (sanity).** Both views must give the same result; they did. **Notice:** the row-dot view gives one entry of Av at a time. The column-combination view gives all of Av at once. Same operation, different bookkeeping.

---

## Eigenvalue computation (2×2)

**Goal:** Find the eigenvalues of A = [[4, 1], [2, 3]].

**Frame 1.** Eigenvalues solve det(A − λI) = 0. Form A − λI:
```
A - λI = [[4-λ,  1 ],
         [ 2,  3-λ]]
```

**Frame 2.** Compute the determinant:
det = (4 − λ)(3 − λ) − 1·2 = (12 − 7λ + λ²) − 2 = λ² − 7λ + 10

**Frame 3.** Solve λ² − 7λ + 10 = 0:
Factor: (λ − 5)(λ − 2) = 0. So λ = 5 or λ = 2. **Notice:** factoring works here because the discriminant is a perfect square; in general you'd use the quadratic formula.

**Frame 4.** Sanity checks.
- trace(A) = 4 + 3 = 7 = sum of eigenvalues (5 + 2). ✓
- det(A) = 4·3 − 1·2 = 10 = product of eigenvalues (5·2). ✓

**Frame 5.** Eigenvalues: 5 and 2. Geometrically: A stretches some direction by 5 and another by 2. We don't yet know which directions — that's the next walkthrough.

---

## Finding the eigenvector for a known eigenvalue

**Goal:** Find an eigenvector of A = [[4, 1], [2, 3]] for the eigenvalue λ = 5.

**Frame 1.** Eigenvector v satisfies Av = 5v, equivalently (A − 5I)v = 0.
```
A - 5I = [[-1,  1],
         [ 2, -2]]
```

**Frame 2.** Solve (A − 5I)v = 0. The matrix is singular (rows are scalar multiples), so it has a 1-D null space. Pick the equation from row 0:
−v₀ + v₁ = 0 ⟹ v₁ = v₀.

**Frame 3.** Any vector with v₀ = v₁ works. Pick v = (1, 1). **Notice:** the choice of magnitude is arbitrary; (2, 2) and (100, 100) are also eigenvectors.

**Frame 4.** Verify: Av = [[4, 1], [2, 3]]·(1, 1) = (4 + 1, 2 + 3) = (5, 5) = 5·(1, 1) = 5v. ✓

---

## Softmax of a small vector

**Goal:** Compute softmax((2, 1, −1)).

**Frame 1.** Apply exp to each entry:
exp(2) ≈ 7.389, exp(1) ≈ 2.718, exp(−1) ≈ 0.368.

**Frame 2.** Sum: 7.389 + 2.718 + 0.368 ≈ 10.475.

**Frame 3.** Divide each entry by the sum:
softmax ≈ (7.389/10.475, 2.718/10.475, 0.368/10.475) ≈ (0.705, 0.260, 0.035).

**Frame 4.** Sanity: entries are positive, sum to 1. ✓ **Notice:** the largest input (2) got 70% of the mass, the smallest (−1) got 3.5%. Softmax is a soft argmax — sharper at higher contrast. If the input had been (10, 1, −1), the largest would have gotten ≈ 99.99%.

---

## Single SGD step

**Goal:** One SGD step on the loss f(x) = x², starting at x = 4, with learning rate η = 0.5.

**Frame 1.** Initial state: x = 4, f(x) = 16.

**Frame 2.** Gradient: f'(x) = 2x = 8. The gradient at x = 4 is 8.

**Frame 3.** Update: x ← x − η · f'(x) = 4 − 0.5 · 8 = 4 − 4 = 0.

**Frame 4.** New state: x = 0, f(x) = 0. **Notice:** with η = 0.5 on this convex quadratic, we converged in one step. Smaller η would have taken multiple steps; η > 1 would have *overshot* and bounced or diverged. Try η = 1.5 yourself: x → 4 − 1.5·8 = −8, then 8, then −8 — it bounces forever.

---

## Attention forward pass (3 tokens, d=2)

**Goal:** Compute self-attention for 3 tokens, each with a 2-D embedding. We'll use simple Q, K, V values for clarity.

**Frame 1.** Inputs. Three tokens with embeddings:
```
X = [[1, 0],   # token 0
     [0, 1],   # token 1
     [1, 1]]   # token 2
```
For simplicity: Q = K = X (no projection), V = X. d = 2.

**Frame 2.** Compute scores QKᵀ:
```
QK^T = X · X^T =
  [[1·1+0·0, 1·0+0·1, 1·1+0·1],
   [0·1+1·0, 0·0+1·1, 0·1+1·1],
   [1·1+1·0, 1·0+1·1, 1·1+1·1]]
       =
  [[1, 0, 1],
   [0, 1, 1],
   [1, 1, 2]]
```

**Frame 3.** Scale by √d = √2 ≈ 1.414:
```
scaled ≈ [[0.71, 0,    0.71],
          [0,    0.71, 0.71],
          [0.71, 0.71, 1.41]]
```

**Frame 4.** Apply softmax row-wise. For row 0: softmax([0.71, 0, 0.71]).
exp ≈ [2.03, 1.00, 2.03]; sum ≈ 5.07; softmax ≈ [0.40, 0.20, 0.40].
Same for row 1: [0.20, 0.40, 0.40].
Row 2: exp ≈ [2.03, 2.03, 4.10]; sum ≈ 8.17; softmax ≈ [0.25, 0.25, 0.50].
```
attn = [[0.40, 0.20, 0.40],
        [0.20, 0.40, 0.40],
        [0.25, 0.25, 0.50]]
```

**Frame 5.** Multiply by V (= X):
Row 0 output: 0.40·(1,0) + 0.20·(0,1) + 0.40·(1,1) = (0.40+0+0.40, 0+0.20+0.40) = (0.80, 0.60).
Row 1 output: 0.20·(1,0) + 0.40·(0,1) + 0.40·(1,1) = (0.60, 0.80).
Row 2 output: 0.25·(1,0) + 0.25·(0,1) + 0.50·(1,1) = (0.75, 0.75).

**Frame 6.** Output:
```
[[0.80, 0.60],
 [0.60, 0.80],
 [0.75, 0.75]]
```

**Frame 7.** **Notice:**
- Token 0's output (0.80, 0.60) is closer to (1, 0) than token 1's output. Each token's output reflects mostly itself (high diagonal in attn matrix), with some pull from neighbors.
- Token 2's row is symmetric (0.25, 0.25, 0.50) — it's "in the middle" geometrically, so its query matches both neighbors equally and itself the most.
- Sanity: every output row's components sum to a number ≤ max V row sum. Outputs are convex combinations of input embeddings.

---

## LayerNorm on a 3-vector

**Goal:** Apply LayerNorm to x = (1, 5, 9), with γ = 1, β = 0 (no learnable affine for clarity).

**Frame 1.** Compute mean: μ = (1 + 5 + 9)/3 = 5.

**Frame 2.** Center: x − μ = (1−5, 5−5, 9−5) = (−4, 0, 4).

**Frame 3.** Compute variance: σ² = (16 + 0 + 16)/3 ≈ 10.67. So σ ≈ 3.27.

**Frame 4.** Rescale: (x − μ)/σ ≈ (−4/3.27, 0, 4/3.27) ≈ (−1.22, 0, 1.22).

**Frame 5.** Apply γ, β: γ·result + β = result (since γ = 1, β = 0). Final: (−1.22, 0, 1.22). **Notice:** mean is 0, std is 1 (verify: variance = (1.49 + 0 + 1.49)/3 ≈ 0.99 ≈ 1, modulo rounding). With learnable γ, β the network can rescale and reshift away from this canonical shape — but starts from the standardized state.

---

## Backprop through a tiny network

**Goal:** Forward pass and backward pass through y = w₂ · σ(w₁ · x) where σ is sigmoid, x = 1, w₁ = 0.5, w₂ = 2. Loss L = ½(y − target)², target = 1.

**Frame 1.** Forward pass.
- z₁ = w₁ · x = 0.5 · 1 = 0.5.
- a₁ = σ(z₁) = σ(0.5) ≈ 0.622.
- y = w₂ · a₁ = 2 · 0.622 = 1.244.
- L = ½(1.244 − 1)² = ½ · 0.0596 ≈ 0.0298.

**Frame 2.** Backward, ∂L/∂y.
∂L/∂y = y − target = 1.244 − 1 = 0.244.

**Frame 3.** Backward, ∂L/∂w₂.
y = w₂ · a₁, so ∂y/∂w₂ = a₁ = 0.622.
∂L/∂w₂ = ∂L/∂y · ∂y/∂w₂ = 0.244 · 0.622 ≈ 0.152.

**Frame 4.** Backward, ∂L/∂a₁.
∂L/∂a₁ = ∂L/∂y · w₂ = 0.244 · 2 = 0.488.

**Frame 5.** Backward, ∂L/∂z₁.
σ'(z) = σ(z)(1 − σ(z)) = 0.622 · 0.378 ≈ 0.235.
∂L/∂z₁ = ∂L/∂a₁ · σ'(z₁) = 0.488 · 0.235 ≈ 0.115.

**Frame 6.** Backward, ∂L/∂w₁.
z₁ = w₁ · x, ∂z₁/∂w₁ = x = 1.
∂L/∂w₁ = ∂L/∂z₁ · x = 0.115. **Notice:** the chain rule is exactly what you used; backprop is just the systematic rightmost-to-leftmost application of it. Each frame is one chain rule link.

---

## PCA on 4 points in 2D

**Goal:** Find the principal components of the dataset {(0, 0), (1, 1), (2, 2), (3, 3)}.

**Frame 1.** Compute the mean: μ = ((0+1+2+3)/4, (0+1+2+3)/4) = (1.5, 1.5).

**Frame 2.** Center the data:
```
[(-1.5, -1.5), (-0.5, -0.5), (0.5, 0.5), (1.5, 1.5)]
```

**Frame 3.** Compute the covariance matrix Σ. Each off-diagonal Σ₀₁ = mean(centered_x · centered_y) = mean(2.25, 0.25, 0.25, 2.25) = 1.25. Similarly Σ₀₀ = Σ₁₁ = 1.25.
```
Σ = [[1.25, 1.25],
     [1.25, 1.25]]
```

**Frame 4.** Find eigenvalues of Σ. det(Σ − λI) = (1.25 − λ)² − 1.25² = 0 → (1.25 − λ)² = 1.5625 → 1.25 − λ = ±1.25 → λ = 0 or λ = 2.5.

**Frame 5.** Find eigenvectors.
- For λ = 2.5: solve (Σ − 2.5I)v = 0. Σ − 2.5I = [[−1.25, 1.25], [1.25, −1.25]]. Null space: v₀ = v₁. Eigenvector ∝ (1, 1).
- For λ = 0: solve Σv = 0. Null space: v₀ = −v₁. Eigenvector ∝ (1, −1).

**Frame 6.** Result. The first principal component is (1, 1) (with variance 2.5); the second is (1, −1) (with variance 0). **Notice:** the data is exactly a line along (1, 1), so all variance is along that direction and zero perpendicular to it. The eigenvectors of covariance have correctly identified the axis of the data cloud.

---

## Power iteration (3 iterations)

**Goal:** Find the dominant eigenvector of A = [[2, 1], [1, 3]] using power iteration.

**Frame 1.** Initial guess: v₀ = (1, 0). (Any vector not orthogonal to the dominant eigenvector works.)

**Frame 2.** Iterate v ← A v / ||A v||.
- A v₀ = (2·1 + 1·0, 1·1 + 3·0) = (2, 1). ||(2, 1)|| ≈ 2.236. v₁ ≈ (0.894, 0.447).

**Frame 3.** Second iteration.
- A v₁ ≈ (2·0.894 + 1·0.447, 1·0.894 + 3·0.447) = (2.236, 2.236). ||(2.236, 2.236)|| ≈ 3.162. v₂ ≈ (0.707, 0.707).

**Frame 4.** Third iteration.
- A v₂ ≈ (2·0.707 + 1·0.707, 1·0.707 + 3·0.707) = (2.121, 2.828). ||(2.121, 2.828)|| ≈ 3.535. v₃ ≈ (0.600, 0.800).

**Frame 5.** Continued iteration. v₄ ≈ (0.526, 0.851), v₅ ≈ (0.488, 0.873)... converging to the dominant eigenvector ≈ (0.526, 0.851), which is the eigenvector for λ = 3.618 (the larger eigenvalue of A).

**Frame 6.** **Notice:** each iteration multiplies by A and normalizes. Components in the direction of the dominant eigenvector grow fastest (they're scaled by the largest eigenvalue), while normalization keeps the vector at unit length. Eventually the dominant component dominates and the iteration stabilizes. This is one of the simplest and most useful algorithms in linear algebra — the foundation of PageRank, among many others.

---

## Single diffusion denoising step

**Goal:** One step of DDPM denoising. Inputs: noisy sample x_t ≈ (0.5, 1.0), predicted noise ε ≈ (0.3, 0.6), step coefficients α_t = 0.9, ᾱ_t = 0.95 (made up for clarity).

**Frame 1.** Inputs.
- x_t = (0.5, 1.0) (current noisy sample at step t)
- ε = (0.3, 0.6) (predicted noise from the network)
- α_t = 0.9, ᾱ_t = 0.95.

**Frame 2.** Compute the predicted clean sample x₀ from x_t and ε (one common formulation):
x̂₀ = (x_t − √(1 − ᾱ_t) · ε) / √ᾱ_t
   = ((0.5, 1.0) − √0.05 · (0.3, 0.6)) / √0.95
   = ((0.5, 1.0) − 0.224 · (0.3, 0.6)) / 0.975
   ≈ ((0.5, 1.0) − (0.067, 0.134)) / 0.975
   ≈ (0.433, 0.866) / 0.975 ≈ (0.444, 0.888).

**Frame 3.** Compute x_{t-1} as a combination of x̂₀ and x_t with the step's mixing coefficients (DDPM-style):
mean ≈ coefficient_a · x̂₀ + coefficient_b · x_t (specific form depends on parameterization).
Skipping detailed coefficients; result: x_{t-1} ≈ (0.46, 0.91) (approximate).

**Frame 4.** Add a bit of Gaussian noise (DDPM is stochastic): x_{t-1} ← x_{t-1} + σ_t · z, z ∼ N(0, I). Skipping for brevity.

**Frame 5.** **Notice:** each step partially de-noises by predicting where x_t came from and stepping toward it. The slow schedule (many small denoising steps) is what lets a simple regression model build up complex generative outputs. One step is small; the chain of T steps is what produces the full sample.

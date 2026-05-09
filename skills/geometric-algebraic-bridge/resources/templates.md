# Filled Templates

One filled-in template per major concept. Each shows the four blocks (geometric, algebraic, bridge, verify) ready to deliver to a learner. Adapt the wording but keep the structure.

## Contents
- Eigenvectors and eigenvalues
- Dot product
- Determinant
- Covariance matrix and PCA
- Softmax
- Jacobian
- SVD
- Outer product
- Matrix-vector multiplication
- Cross-entropy

---

## Eigenvectors and eigenvalues

**Geometric view.** A matrix A acts on the plane (or higher) as a transformation — rotating and stretching. Most arrows get bent into a new direction. But for some matrices, there are special arrows that *only* get stretched, never rotated. Those are the eigenvectors. The factor by which they stretch is the eigenvalue.

**Algebraic view.** An eigenvector v of A satisfies Av = λv, where λ is the eigenvalue. Equivalently, (A − λI)v = 0, so eigenvalues are roots of det(A − λI) = 0.

**Bridge.** The equation Av = λv is the algebraic statement of "left in place direction-wise" — because λv is just v rescaled, no rotation. The picture and the formula are the same fact written in two languages.

**Verify on a tiny example.** Take A = [[2, 0], [0, 3]]. Geometrically: stretches x-axis by 2, y-axis by 3. Algebraically: eigenvectors are (1, 0) with λ = 2, and (0, 1) with λ = 3. Same picture, same numbers.

---

## Dot product

**Geometric view.** Take two arrows a and b. The dot product measures how much one points along the other — specifically, the projection of a onto b's direction, multiplied by b's length. If they're perpendicular, the projection is 0 → dot product is 0. If parallel, projection equals |a| → dot product is |a||b|.

**Algebraic view.** a · b = a₁b₁ + a₂b₂ + … + aₙbₙ. Equivalently: a · b = |a| |b| cos θ.

**Bridge.** The component-wise sum *is* the projection-times-length, because if you rewrite a in coordinates with one axis aligned to b, all but one term vanish — and that surviving term equals |a|cos θ × |b|.

**Verify on a tiny example.** a = (3, 4), b = (1, 0). Component-wise: 3·1 + 4·0 = 3. Projection: a's component along x-axis is 3; b's length is 1; 3 × 1 = 3. Match.

---

## Determinant

**Geometric view.** A 2×2 matrix transforms the unit square into some parallelogram. The determinant is the *signed area* of that parallelogram — positive if orientation is preserved (no flip), negative if the matrix flips the plane. In 3D: signed volume of the transformed unit cube. Determinant 0 means the transformation collapses everything onto a lower-dimensional space.

**Algebraic view.** det([[a, b], [c, d]]) = ad − bc. In general, the Leibniz formula sums signed products over permutations of the indices.

**Bridge.** The formula ad − bc *is* the signed area of the unit square's image, because it counts the parallelogram's area with the right sign convention — positive when the transformation preserves orientation, negative when it flips.

**Verify on a tiny example.** A = [[2, 0], [0, 3]]. Image of unit square: a 2×3 rectangle, area 6. Formula: 2·3 − 0·0 = 6. Match.

---

## Covariance matrix and PCA

**Geometric view.** A cloud of data points in n dimensions has a *shape* — it's spread out more in some directions than others. That shape is an ellipsoid. The covariance matrix Σ encodes this ellipsoid: its eigenvectors are the ellipsoid's axes, and its eigenvalues are the spread (variance) along each axis.

**Algebraic view.** Σᵢⱼ = E[(xᵢ − μᵢ)(xⱼ − μⱼ)], the average product of centered features. Eigenvectors of Σ give orthogonal directions of variance; eigenvalues give the variance along each.

**Bridge.** The covariance matrix *is* the ellipsoid's shape because applying it to the unit ball produces an ellipsoid with the same shape as the data cloud — and the eigenvectors of any matrix are the axes of the ellipsoid it produces.

**Verify on a tiny example.** Data: points along the line y = x. Σ ≈ [[1, 1], [1, 1]]. Eigenvectors: (1, 1) with λ = 2 (the long axis), (1, −1) with λ = 0 (the perpendicular, where there's no spread). Matches: cloud is a line along (1, 1), zero spread perpendicular.

---

## Softmax

**Geometric view.** Softmax takes a vector of arbitrary real "scores" and bends it onto the *simplex* — the surface of all valid probability distributions over the same number of outcomes. At low contrast (scores close together), it lands near the center of the simplex (uniform). At high contrast (one score much bigger), it lands near a corner (concentrated on one outcome). It's a *soft* version of argmax.

**Algebraic view.** softmax(x)ᵢ = exp(xᵢ) / Σⱼ exp(xⱼ). Exponential ensures positivity; normalization ensures sum-to-1.

**Bridge.** The exp-then-normalize formula *is* the projection onto the simplex with sharpening, because exp amplifies score differences (more contrast → more extreme distribution) and the normalization places the result on the simplex.

**Verify on a tiny example.** x = (10, 0, 0). exp gives (e¹⁰, 1, 1) ≈ (22026, 1, 1). Normalize: ≈ (1.000, 0, 0). Almost a corner of the simplex. Now x = (1, 0, 0): (e, 1, 1) ≈ (2.72, 1, 1). Normalize: ≈ (0.58, 0.21, 0.21). Center-ish of the simplex. Confirms the "sharper at high contrast" picture.

---

## Jacobian

**Geometric view.** For a function f: ℝⁿ → ℝᵐ, near any point p there's a linear approximation — a linear map that best matches f's behavior in a tiny neighborhood. That linear map is the Jacobian. It's the m × n matrix that *represents* the derivative.

**Algebraic view.** J(f)ᵢⱼ = ∂fᵢ/∂xⱼ. The (i, j) entry is the partial of the i-th output with respect to the j-th input, evaluated at p.

**Bridge.** The matrix of partials *is* the local linear map because each entry tells you how a unit change in input j affects output i — which is exactly what the linear approximation needs to know.

**Verify on a tiny example.** f(x, y) = (x², xy). At (1, 1): J = [[2x, 0], [y, x]] = [[2, 0], [1, 1]]. Check: f(1.01, 1) ≈ (1.0201, 1.01). Linear approx at (1, 1) + (0.01, 0): (1, 1) + J·(0.01, 0) = (1, 1) + (0.02, 0.01) = (1.02, 1.01). Matches.

---

## SVD

**Geometric view.** Every matrix A — *every* matrix, even non-square — can be decomposed into three transformations: a rotation, an axis-aligned scaling, and another rotation. SVD is the decomposition that finds these three.

**Algebraic view.** A = U Σ Vᵀ, where U and V are orthogonal (rotations/reflections) and Σ is diagonal with non-negative entries (scalings). The diagonal entries of Σ are the *singular values* of A.

**Bridge.** Every linear transformation, no matter how complicated, *is* a rotate-scale-rotate sequence — because Vᵀ rotates the input into a frame where A acts diagonally (Σ scales each axis), and U then rotates the result into the output frame. The singular values are how much the transformation stretches each axis.

**Verify on a tiny example.** A = [[3, 0], [0, 1]]. Already diagonal. SVD: U = I, Σ = [[3, 0], [0, 1]], Vᵀ = I. Stretches x by 3, y by 1. The singular values (3, 1) are the stretch factors.

---

## Outer product

**Geometric view.** The outer product u vᵀ is a *rank-1 matrix*: every row is a scaled copy of v, and every column is a scaled copy of u. As a transformation, it projects every input onto the direction of v, then scales by u's length and points in u's direction. It collapses everything onto a single line.

**Algebraic view.** (u vᵀ)ᵢⱼ = uᵢ vⱼ. Each entry is just the product of one component of u with one component of v.

**Bridge.** The matrix u vᵀ *is* a rank-1 collapse-and-stretch, because (u vᵀ) x = u (vᵀ x) — first project x onto v (giving a scalar vᵀ x), then scale u by that scalar.

**Verify on a tiny example.** u = (1, 2), v = (3, 4). u vᵀ = [[3, 4], [6, 8]]. Apply to x = (1, 1): vᵀ x = 7, then 7 · u = (7, 14). Matrix multiplication: [[3, 4], [6, 8]] · (1, 1) = (7, 14). Match.

---

## Matrix-vector multiplication

**Geometric view.** A matrix A acts on a vector v. Two equivalent pictures:
1. **Transformation.** A bends the input space — rotates, stretches, shears. The output Av is where the input v lands after the transformation.
2. **Weighted column combination.** The output Av is a weighted sum of A's columns, with the weights being v's components. The columns of A *are* the images of the basis vectors under A.

**Algebraic view.** (Av)ᵢ = Σⱼ Aᵢⱼ vⱼ. Row of A dotted with v gives one entry of Av.

**Bridge.** "Row dot v" *is* "weighted sum of columns" written from a different angle, because both describe the same operation: the i-th component of Av is row i of A dotted with v, which equals the i-th entry of (sum of v_j times column j).

**Verify on a tiny example.** A = [[1, 2], [3, 4]], v = (5, 6). Row-dot: (1·5 + 2·6, 3·5 + 4·6) = (17, 39). Column combination: 5·(1, 3) + 6·(2, 4) = (5, 15) + (12, 24) = (17, 39). Match.

---

## Cross-entropy

**Geometric view.** You have a true distribution p (often one-hot) and a predicted distribution q. Cross-entropy measures how *surprised* you'd be on average if you assumed q but the truth was p — weighted by how much each outcome actually matters under p. It blows up when q assigns near-zero probability to something that actually happens (under p).

**Algebraic view.** H(p, q) = −Σᵢ pᵢ log qᵢ. If p is one-hot on class k, this collapses to −log qₖ.

**Bridge.** The formula −Σ pᵢ log qᵢ *is* "expected surprise under p, given prediction q", because −log qᵢ is the surprise when outcome i happens, and pᵢ weights it by how often i actually does happen.

**Verify on a tiny example.** p = (1, 0, 0) (truth: class 0), q = (0.7, 0.2, 0.1). Cross-entropy = −1·log 0.7 = 0.357. Now q = (0.1, 0.5, 0.4) (very wrong on class 0): −1·log 0.1 = 2.30. Larger when prediction is more wrong on the true class — matches the picture.

# Numpy Demonstration Scripts

Self-contained scripts that produce the actual numbers backing each high-dim phenomenon. Run via Bash; report the output to the learner.

Each script is short (under 20 lines), uses only numpy, and prints labeled output.

## Contents
- Concentration of measure (Gaussian shell radius)
- Distance concentration (min/max distance ratio)
- Angle concentration (cosine similarity of random vectors)
- Cube-corner dominance (fraction of cube samples inside ball)
- JL random projection (distance preservation)
- Multi-phenomenon combo (all five at d=1000)

---

## Concentration of measure

```python
import numpy as np
print("d  | mean radius | std radius | √d")
for d in [2, 3, 10, 100, 1000, 10000]:
    samples = np.random.randn(10000, d)
    norms = np.linalg.norm(samples, axis=1)
    print(f"{d:5} | {norms.mean():10.2f} | {norms.std():10.2f} | {np.sqrt(d):.2f}")
```

**What to highlight to the learner:**
- The mean radius matches √d almost exactly across all d.
- The std stays near 1/√2 ≈ 0.71 regardless of d, so the *relative* shell width (std/mean) shrinks like 1/√d.

---

## Distance concentration

```python
import numpy as np
print("d  | min dist | max dist | min/max ratio")
N = 1000
for d in [3, 10, 100, 1000, 10000]:
    pts = np.random.randn(N, d)
    dists = np.linalg.norm(pts - pts[0], axis=1)
    dists = dists[1:]  # exclude self
    print(f"{d:5} | {dists.min():8.2f} | {dists.max():8.2f} | {dists.min()/dists.max():.3f}")
```

**What to highlight:**
- The ratio of nearest to farthest grows toward 1.
- By d = 10000, the closest point is ~97% as far as the farthest. "Nearest" loses meaning.

---

## Angle concentration

```python
import numpy as np
print("d  | cos mean | cos std | 1/√d")
for d in [2, 3, 10, 100, 1000, 10000]:
    v = np.random.randn(10000, d)
    w = np.random.randn(10000, d)
    cos = (v * w).sum(axis=1) / (np.linalg.norm(v, axis=1) * np.linalg.norm(w, axis=1))
    print(f"{d:5} | {cos.mean():+8.4f} | {cos.std():8.4f} | {1/np.sqrt(d):.4f}")
```

**What to highlight:**
- The std of cosine matches 1/√d to high precision.
- In d = 10000, random cosines are essentially in [−0.03, +0.03] — anything above this is signal.

---

## Cube-corner dominance

```python
import numpy as np
print("d  | fraction of unit-cube samples inside unit ball")
for d in [2, 3, 5, 10, 20, 50, 100]:
    samples = np.random.uniform(-1, 1, size=(100000, d))
    in_ball = (np.linalg.norm(samples, axis=1) < 1).mean()
    print(f"{d:5} | {in_ball:.5f}")
```

**What to highlight:**
- The fraction collapses fast: 78% in 2D, 52% in 3D, 0.25% in 10D, ~0% past d = 30.
- The cube's volume is in the corners. The inscribed ball is irrelevant in high D.

---

## Johnson–Lindenstrauss random projection

```python
import numpy as np
N, d_orig = 500, 10000
print(f"Projecting {N} points from d={d_orig} to various k:")
print("k   | mean ratio | std ratio")
X = np.random.randn(N, d_orig) / np.sqrt(d_orig)
D_orig = np.linalg.norm(X[:, None] - X[None, :], axis=2)
mask = D_orig > 0
for k in [10, 50, 100, 500, 1000, 5000]:
    P = np.random.randn(d_orig, k) / np.sqrt(k)
    Y = X @ P
    D_proj = np.linalg.norm(Y[:, None] - Y[None, :], axis=2)
    ratio = (D_proj[mask] / D_orig[mask])
    print(f"{k:5} | {ratio.mean():9.3f} | {ratio.std():.3f}")
```

**What to highlight:**
- Even projecting to k = 100 dims (2 orders of magnitude smaller), distances are preserved to a few percent.
- The original d = 10000 doesn't appear in the JL bound — only k matters, and only logarithmically in N.

---

## Multi-phenomenon combo (all in one)

```python
import numpy as np
d = 1000
print(f"Demonstrating all five phenomena at d = {d}")
print("=" * 60)

# 1. Concentration of measure
samples = np.random.randn(10000, d)
print(f"1. Gaussian shell:   mean radius = {np.linalg.norm(samples, axis=1).mean():.2f}, expected √d = {np.sqrt(d):.2f}")

# 2. Distance concentration
pts = np.random.randn(1000, d)
dists = np.linalg.norm(pts - pts[0], axis=1)[1:]
print(f"2. Distance ratio:   min/max = {dists.min()/dists.max():.3f} (was 0.12 at d=3)")

# 3. Angle concentration
v = np.random.randn(10000, d); w = np.random.randn(10000, d)
cos = (v * w).sum(axis=1) / (np.linalg.norm(v, axis=1) * np.linalg.norm(w, axis=1))
print(f"3. Random cosine:    std = {cos.std():.4f}, expected 1/√d = {1/np.sqrt(d):.4f}")

# 4. Cube-corner dominance
cube = np.random.uniform(-1, 1, size=(100000, d))
in_ball = (np.linalg.norm(cube, axis=1) < 1).mean()
print(f"4. Cube samples in unit ball: {in_ball:.10f} (essentially zero)")

# 5. JL projection preservation
X = np.random.randn(500, d) / np.sqrt(d)
D_orig = np.linalg.norm(X[:, None] - X[None, :], axis=2)
P = np.random.randn(d, 100) / np.sqrt(100)
Y = X @ P
D_proj = np.linalg.norm(Y[:, None] - Y[None, :], axis=2)
mask = D_orig > 0
print(f"5. JL d=1000→k=100:  distance ratio = {(D_proj[mask]/D_orig[mask]).mean():.3f} ± {(D_proj[mask]/D_orig[mask]).std():.3f}")
```

**Use this when:** You want to demonstrate the breadth of high-dim weirdness in one shot — useful for an "intro to high-dim thinking" session.

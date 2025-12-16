# Group Theory Methodology for ML

## Core Concepts

### What is a Group?

A group (G, ·) consists of a set G with an operation · satisfying:
1. **Closure**: a·b ∈ G for all a,b ∈ G
2. **Associativity**: (a·b)·c = a·(b·c)
3. **Identity**: ∃e such that e·a = a·e = a
4. **Inverse**: ∀a, ∃a⁻¹ such that a·a⁻¹ = e

### Why Groups Matter for ML

Groups formalize symmetry mathematically. When we say data has "rotation symmetry," we mean the rotation group SO(n) acts on it. Building this into networks:
- Reduces parameters through weight sharing
- Guarantees generalization across transformations
- Improves sample efficiency

### Representations

A representation ρ: G → GL(V) maps group elements to matrices acting on a vector space V.

**Irreducible representations (irreps)**: Cannot be decomposed into smaller representations. They are the building blocks of equivariant networks.

For SO(3), irreps are labeled by l = 0, 1, 2, ... with dimension 2l+1:
- l=0: Scalars (1D)
- l=1: Vectors (3D)
- l=2: Traceless symmetric tensors (5D)

### Invariance vs Equivariance

- **Invariant**: f(g·x) = f(x) - output unchanged
- **Equivariant**: f(g·x) = g·f(x) - output transforms consistently

For ML tasks:
- Classification → Invariant output
- Segmentation/Detection → Equivariant output
- Force prediction → Equivariant (vector output)

## Advanced Topics

### Semidirect Products

SE(3) = SO(3) ⋊ ℝ³ means rotations and translations don't commute. The rotation "twists" how translations compose.

### Gauge Equivariance

For manifolds without global coordinate systems, we need gauge equivariance - invariance to choice of local frame. This generalizes standard equivariance.

### Representation Theory in Practice

In e3nn, features are typed by irreps:
```
"2x0e + 3x1o + 1x2e"
```
means: 2 even scalars, 3 odd vectors, 1 even order-2 tensor.

Tensor products combine irreps following Clebsch-Gordan rules.

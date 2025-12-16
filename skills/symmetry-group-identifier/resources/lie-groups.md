# Lie Groups Reference for Geometric Deep Learning

This reference covers continuous (Lie) groups commonly used in geometric deep learning.

## What is a Lie Group?

A **Lie group** is a group that is also a smooth manifold, where the group operations (multiplication and inversion) are smooth functions.

**Key insight**: Lie groups are continuous symmetries that can be parameterized by real numbers.

## The Lie Algebra

Every Lie group G has an associated **Lie algebra** g:
- The tangent space at the identity
- Captures infinitesimal group transformations
- Connected to the group via the exponential map: exp: g → G

## Common Lie Groups in ML

### SO(2) - 2D Rotations

**Matrix form**:
```
R(θ) = [cos(θ)  -sin(θ)]
       [sin(θ)   cos(θ)]
```

**Parameters**: 1 (the angle θ)

**Lie algebra so(2)**:
```
[0  -θ]
[θ   0]
```

**Irreducible representations**:
- Complex exponentials e^{inθ} for integer n
- In terms of real matrices: 2×2 rotation matrices

### SO(3) - 3D Rotations

**Matrix form**: 3×3 rotation matrices (RᵀR = I, det(R) = 1)

**Parameters**: 3 (axis-angle, Euler angles, or quaternion with constraint)

**Common parameterizations**:
- **Euler angles**: (φ, θ, ψ) - suffer from gimbal lock
- **Axis-angle**: (n, θ) where n is unit vector
- **Quaternions**: (w, x, y, z) with w² + x² + y² + z² = 1
- **Rotation matrix**: 9 numbers with 6 constraints

**Lie algebra so(3)**: 3×3 antisymmetric matrices
```
[0   -ω₃   ω₂]
[ω₃   0   -ω₁]
[-ω₂  ω₁   0]
```

**Irreducible representations**:
| l | Dimension | Name | Parity |
|---|-----------|------|--------|
| 0 | 1 | Scalar | Even (e) |
| 1 | 3 | Vector | Odd (o) |
| 2 | 5 | Matrix/Tensor | Even (e) |
| l | 2l+1 | Higher tensor | (-1)^l |

**Spherical harmonics** Y_l^m form a basis for irrep l.

### O(3) - 3D Rotations + Reflections

**Structure**: O(3) = SO(3) ∪ (inversion × SO(3))

**Two components**:
- det = +1: Proper rotations (SO(3))
- det = -1: Improper rotations (rotoreflections)

**Irreps**: Same dimensions as SO(3), but with parity label:
- **Even (e)**: Invariant under inversion (scalars, even-rank tensors)
- **Odd (o)**: Change sign under inversion (vectors, pseudovectors)

**e3nn notation**: "1x0e + 1x1o" means 1 even scalar + 1 odd vector

### SE(3) - 3D Rigid Motions

**Elements**: (R, t) where R ∈ SO(3), t ∈ ℝ³

**Composition**: (R₁, t₁) · (R₂, t₂) = (R₁R₂, R₁t₂ + t₁)

**Structure**: Semidirect product SE(3) = SO(3) ⋊ ℝ³

**Parameters**: 6 (3 for rotation + 3 for translation)

**Lie algebra se(3)**: 4×4 matrices
```
[ω̂   v]    where ω̂ is 3×3 antisymmetric
[0   0]
```

**Key property**: Non-compact (translations are unbounded)

### E(3) - Full Euclidean Group

**Elements**: SE(3) + reflections

**Structure**: E(3) = O(3) ⋊ ℝ³

**Components**: 2 (orientation-preserving and reversing)

**Most common in chemistry**: Molecules can be reflected without changing energy.

## Representations in Practice

### Spherical Harmonics Basis

For SO(3)/O(3), spherical harmonics provide a basis:

```
Y_l^m(θ, φ) for m ∈ {-l, ..., l}
```

**Properties**:
- Orthonormal on the sphere
- Transform as irrep l under rotations
- Real spherical harmonics often used in ML

### e3nn Irreps Notation

In e3nn, representations are specified as strings:

```
"2x0e + 3x1o + 1x2e"
```

Meaning:
- 2 even scalars (l=0, even parity)
- 3 odd vectors (l=1, odd parity)
- 1 even rank-2 tensor (l=2, even parity)

Total dimension: 2×1 + 3×3 + 1×5 = 16

### Clebsch-Gordan Coefficients

When combining two irreps, the result decomposes into a sum of irreps:

```
l₁ ⊗ l₂ = |l₁-l₂| ⊕ |l₁-l₂|+1 ⊕ ... ⊕ l₁+l₂
```

**Example**: 1 ⊗ 1 = 0 ⊕ 1 ⊕ 2

Clebsch-Gordan coefficients tell you how to do this combination.
**In e3nn**: `o3.FullyConnectedTensorProduct` handles this automatically.

## Choosing the Right Group

| Data Type | Position Matters | Orientation Matters | Handedness Matters | Group |
|-----------|-----------------|--------------------|--------------------|-------|
| Molecules (energy) | No | No | No | E(3) |
| Molecules (chiral) | No | No | Yes | SE(3) |
| Point clouds | Sometimes | No | No | SO(3) or SE(3) |
| Robotics | Yes | Yes | Yes | SE(3) |
| Physics simulation | Depends | Depends | Depends | Varies |

## Implementation Tips

### Sampling Random Rotations

**SO(3)**: Use quaternion sampling
```python
# Sample uniform random quaternion
q = np.random.randn(4)
q = q / np.linalg.norm(q)
# Convert to rotation matrix
```

**SO(2)**: Uniform angle
```python
theta = np.random.uniform(0, 2*np.pi)
```

### Numerical Stability

- **Quaternions** are more stable than Euler angles
- **Rotation matrices** have orthogonality constraints to enforce
- **Exponential map** can have numerical issues near identity

### Efficiency Considerations

| Group | Parameter Count | Computational Cost |
|-------|----------------|-------------------|
| SO(2) | 1 | Low |
| SO(3) | 3 | Medium |
| SE(3) | 6 | Medium-High |
| E(3) | 6 + parity | Medium-High |

Higher l irreps are more expensive (dimension 2l+1).

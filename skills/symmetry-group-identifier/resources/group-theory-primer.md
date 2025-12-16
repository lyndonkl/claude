# Group Theory Primer for Machine Learning

This primer covers the essential group theory concepts needed for geometric deep learning.

## What is a Group?

A **group** is a set G with a binary operation · that satisfies four axioms:

1. **Closure**: For all a, b in G, a · b is also in G
2. **Associativity**: For all a, b, c in G, (a · b) · c = a · (b · c)
3. **Identity**: There exists e in G such that e · a = a · e = a for all a
4. **Inverse**: For each a in G, there exists a⁻¹ such that a · a⁻¹ = a⁻¹ · a = e

## Key Concepts

### Subgroups

A subset H of G that is itself a group under the same operation.

**Example**: Rotations by 180° form a subgroup of all rotations.

### Group Actions

A group G **acts on** a set X if there's a function G × X → X such that:
- e · x = x (identity acts trivially)
- g · (h · x) = (gh) · x (composition works correctly)

**In ML**: Groups act on input spaces (e.g., rotations act on images).

### Representations

A **representation** is a homomorphism ρ: G → GL(V), mapping group elements to invertible matrices on vector space V.

**Why it matters**: Neural network features transform according to representations.

### Irreducible Representations (Irreps)

Representations that cannot be decomposed into smaller representations.

**Example for SO(3)**:
- l=0: Scalars (dimension 1) - invariant
- l=1: Vectors (dimension 3) - rotate like arrows
- l=2: Symmetric traceless tensors (dimension 5)

## Important Group Families

### Cyclic Groups (Cₙ)

- **Elements**: {e, r, r², ..., rⁿ⁻¹} where rⁿ = e
- **Size**: n elements
- **Structure**: Rotations by 2π/n
- **Abelian**: Yes (commutative)

### Dihedral Groups (Dₙ)

- **Elements**: n rotations + n reflections
- **Size**: 2n elements
- **Structure**: Symmetries of regular n-gon
- **Abelian**: No (reflections don't commute with rotations)

### Symmetric Groups (Sₙ)

- **Elements**: All permutations of n items
- **Size**: n! elements
- **Structure**: Reorderings
- **Abelian**: No (for n > 2)

### Special Orthogonal Groups SO(n)

- **Elements**: n×n rotation matrices (det = 1)
- **Size**: Continuous (infinite)
- **Dimension**: n(n-1)/2 parameters
- **Compact**: Yes
- **Connected**: Yes

### Orthogonal Groups O(n)

- **Elements**: n×n orthogonal matrices (including reflections)
- **Structure**: O(n) = SO(n) ∪ (reflections × SO(n))
- **Two components**: det = +1 and det = -1

### Special Euclidean Groups SE(n)

- **Elements**: Rotations + Translations
- **Structure**: SE(n) = SO(n) ⋊ ℝⁿ (semidirect product)
- **Non-compact**: Translations extend to infinity

### Euclidean Groups E(n)

- **Elements**: Rotations + Translations + Reflections
- **Structure**: E(n) = O(n) ⋊ ℝⁿ

## Group Properties Relevant to Architecture

| Property | Definition | ML Implication |
|----------|------------|----------------|
| **Compact** | Bounded and closed | Finite-dimensional representations |
| **Abelian** | All elements commute | Simpler representation theory |
| **Connected** | Cannot split into pieces | All irreps reached from identity |
| **Simple** | No normal subgroups | Cannot factor architecture |

## Product Groups

### Direct Product (G × H)

Elements are pairs (g, h). Groups act independently.

**When to use**: Symmetries don't interact (e.g., rotation × permutation).

### Semidirect Product (G ⋊ H)

One group's action depends on the other.

**Example**: SE(3) = SO(3) ⋊ ℝ³
- First rotate, then translate ≠ First translate, then rotate
- The rotation "twists" how translations work

## From Groups to Neural Networks

1. **Identify symmetry** → Determine the group G
2. **Choose representations** → How features transform under G
3. **Equivariant layers** → Layers that commute with G-action
4. **Invariant output** → Pool to remove G-dependence (if needed)

## Further Reading

- "Visual Group Theory" by Nathan Carter - Intuitive introduction
- "Group Theory in a Nutshell for Physicists" by A. Zee
- "Geometric Deep Learning" by Bronstein et al. (GDL survey paper)

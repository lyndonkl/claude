# Equivariant Architecture Design Methodology

## Design Principles

### The Equivariant Constraint

An equivariant layer satisfies:
```
f(ρ_in(g) · x) = ρ_out(g) · f(x)
```
where ρ_in and ρ_out are representations of group G on input and output spaces.

### Layer Building Blocks

**Theorem (Kondor & Trivedi)**: For compact groups, equivariant linear maps are convolutions.

This means all equivariant architectures use some form of convolution - the key is choosing the right parameterization.

## Architecture Patterns

### Pattern 1: Lift → Process → Pool

```
Input (on base space X)
  ↓ Lift to group
Features (on G × X)
  ↓ G-convolution layers
Features (on G × X)
  ↓ Pool over G
Output (invariant)
```

Used by: G-CNNs, steerable CNNs

### Pattern 2: Message Passing

```
Nodes with features
  ↓ Aggregate neighbor messages
  ↓ Update node features
  ↓ (repeat)
Global pooling or node outputs
```

Used by: GNNs, equivariant point cloud networks

### Pattern 3: Tensor Product Networks

```
Features as spherical tensors (irreps)
  ↓ Tensor product layers (Clebsch-Gordan)
  ↓ Linear combinations within irreps
  ↓ Gated nonlinearities
Output irreps
```

Used by: e3nn, NequIP, MACE

## Critical Design Decisions

### Nonlinearity Selection

**Problem**: Standard nonlinearities break equivariance.

**Solutions**:
1. **Gated**: g(||x||) · x where g is any function
2. **Norm-based**: Apply nonlinearity to ||x||
3. **S²-activation**: For SO(3), nonlinearity on sphere
4. **Tensor product**: Use ⊗ with itself

### Normalization

**BatchNorm breaks equivariance** (different statistics for rotated inputs).

**Solutions**:
- LayerNorm (per-sample)
- Instance Norm
- Equivariant BatchNorm (normalize per irrep channel)

### Pooling

For **invariant outputs** from **equivariant features**:
- Sum/mean pooling (permutation invariant)
- Max-norm pooling (rotation invariant)
- Attention pooling (weighted, learnable)

## Implementation Checklist

Before implementing:
- [ ] Identify input/output representations
- [ ] Choose basis for feature spaces (irreps for Lie groups)
- [ ] Design layer sequence with correct irrep flow
- [ ] Select equivariant nonlinearities
- [ ] Plan normalization strategy
- [ ] Design pooling for final invariance (if needed)
- [ ] Verify theoretical equivariance of design

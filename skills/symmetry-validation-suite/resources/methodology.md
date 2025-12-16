# Symmetry Validation Methodology

## Why Validate Symmetries?

Assuming wrong symmetries hurts models:
- **Over-constraining**: Too much symmetry limits expressiveness
- **Under-constraining**: Missing symmetries wastes model capacity
- **Broken symmetries**: External factors may partially break symmetry

Empirical validation catches these issues before architecture commitment.

## Validation Philosophy

### Exact vs Approximate Symmetry

**Exact symmetry**: f(T(x)) = f(x) exactly (up to numerical precision)
- Use hard equivariant constraints
- Examples: Physical laws, mathematical structures

**Approximate symmetry**: f(T(x)) ≈ f(x) within tolerance
- Consider soft constraints or augmentation
- Examples: Natural images (gravity breaks rotation), noisy measurements

### Statistical Testing Framework

For rigorous validation:
1. **Null hypothesis**: Model is NOT equivariant
2. **Test statistic**: Mean equivariance error
3. **Significance**: p-value < 0.05 indicates equivariance

Sample size recommendations:
- At least 100 data samples
- At least 50 transformations per sample
- Report confidence intervals, not just point estimates

## Test Design Principles

### Transformation Sampling

**Continuous groups** (SO(3), SE(3)):
- Sample uniformly from group (Haar measure)
- Use enough samples to cover the group well

**Discrete groups** (Cₙ, Dₙ, Sₙ):
- Test ALL elements if |G| < 1000
- Random sample if |G| is large

### Edge Cases to Test

1. **Identity**: T = e should give zero error
2. **Composition**: T₁ then T₂ vs T₁·T₂
3. **Inverse**: T then T⁻¹ should return to original
4. **Boundary**: Test near data distribution edges

## Interpreting Results

### Error Thresholds

| Relative Error | Interpretation |
|----------------|----------------|
| < 1e-6 | Numerical precision (float32) |
| 1e-6 to 1e-4 | Excellent - use hard constraints |
| 1e-4 to 1e-2 | Good - consider soft constraints |
| > 1e-2 | Questionable - investigate further |

### When Tests Fail

1. **Check data preprocessing**: Centering, normalization may break symmetry
2. **Check boundary conditions**: Padding, cropping effects
3. **Check distributional assumptions**: Symmetry may only hold for certain data subsets
4. **Consider partial symmetry**: May hold only for specific transformations

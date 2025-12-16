# Model Equivariance Auditing Methodology

A systematic approach to verifying that neural network implementations correctly respect their intended symmetries.

## Why Audit Equivariance?

Even when using equivariant libraries:
- Custom layers may break equivariance
- Incorrect configurations can violate symmetry
- Numerical issues can accumulate
- Integration bugs between components

Auditing catches these issues before they impact training and deployment.

## The Auditing Framework

### Phase 1: Specification Review

Before running tests, verify:

1. **Intended symmetry group is documented**
   - Exact group (SO(3), E(3), C4, etc.)
   - Whether output should be invariant or equivariant
   - What type of equivariance (scalars, vectors, tensors)

2. **Input/output transformations are defined**
   - How inputs transform under group action
   - How outputs should transform
   - Any constraints or special cases

3. **Architecture claims match design**
   - Each layer type documented
   - Library versions recorded
   - Known limitations noted

### Phase 2: Test Design

#### Test Types

| Test | What It Checks | When to Use |
|------|---------------|-------------|
| **End-to-end** | Full model equivariance | Always |
| **Layer-wise** | Individual component equivariance | When E2E fails |
| **Gradient** | Backward pass equivariance | For training stability |
| **Stress** | Edge cases and boundaries | For production readiness |

#### Sample Size Guidelines

| Model Complexity | Data Samples | Transforms per Sample |
|-----------------|--------------|----------------------|
| Simple (< 1M params) | 50-100 | 50 |
| Medium (1M-100M) | 100-200 | 100 |
| Complex (> 100M) | 200+ | 100-200 |

#### Transformation Sampling

For continuous groups, sample transformations uniformly:
- SO(3): Use quaternion rejection sampling or axis-angle
- SE(3): Combine rotation sampling with bounded translations
- SO(2): Uniform angle sampling

For discrete groups, test all elements if |G| < 50, otherwise sample.

### Phase 3: Test Execution

#### Standard Protocol

```
1. Set model to eval mode
2. Disable dropout, stochastic layers
3. Use float64 for precision-critical tests
4. Fix random seeds for reproducibility
5. Run tests on CPU first (more deterministic)
6. Repeat on GPU to check device-specific issues
```

#### Metrics to Compute

| Metric | Formula | Purpose |
|--------|---------|---------|
| Absolute error | \|\|f(Tx) - T'f(x)\|\| | Raw equivariance violation |
| Relative error | error / \|\|T'f(x)\|\| | Scale-independent measure |
| Max error | max over all tests | Worst-case violation |
| Error variance | std of errors | Consistency check |

### Phase 4: Failure Analysis

#### Decision Tree for Failures

```
Error > threshold?
├─ Yes: Investigate
│   ├─ Consistent across transforms?
│   │   ├─ Yes: Likely architecture bug
│   │   └─ No: Likely numerical/boundary issue
│   ├─ Grows with layer depth?
│   │   ├─ Yes: Check nonlinearities, normalizations
│   │   └─ No: Check specific failing layer
│   └─ Varies with input?
│       ├─ Yes: Check data preprocessing
│       └─ No: Check model configuration
└─ No: Pass (document threshold used)
```

#### Common Root Causes

1. **Nonlinearity breaks equivariance**
   - Symptom: Error spikes after activation layers
   - Solution: Use gated/norm-based nonlinearities

2. **Normalization statistics vary by transform**
   - Symptom: BatchNorm causes varying errors
   - Solution: Use LayerNorm or equivariant BatchNorm

3. **Incorrect representation matching**
   - Symptom: Error at layer boundaries
   - Solution: Verify irreps match between layers

4. **Numerical precision loss**
   - Symptom: Small but consistent error everywhere
   - Solution: Use higher precision, check operations

5. **Boundary/padding effects**
   - Symptom: Higher error at edges
   - Solution: Use circular padding or careful handling

### Phase 5: Documentation

#### Audit Report Structure

```
1. Model Identification
   - Model name and version
   - Date of audit
   - Auditor

2. Specification
   - Intended symmetry group
   - Input/output types
   - Architecture summary

3. Test Configuration
   - Test types run
   - Sample sizes
   - Thresholds used

4. Results Summary
   - Pass/fail for each test type
   - Key metrics
   - Any anomalies

5. Detailed Findings
   - Layer-by-layer results (if applicable)
   - Failure analysis (if applicable)
   - Root causes identified

6. Recommendations
   - Required fixes
   - Suggested improvements
   - Follow-up tests needed

7. Certification
   - Overall verdict
   - Conditions/caveats
```

## Continuous Monitoring

For production models:

1. **Pre-deployment gate**: Full audit must pass
2. **Post-update checks**: Re-audit after any change
3. **Periodic verification**: Monthly spot checks
4. **Training monitoring**: Track equivariance loss during training

## Threshold Selection

### Recommended Thresholds

| Context | Relative Error Threshold |
|---------|-------------------------|
| Research/prototype | 1e-3 |
| Production (non-critical) | 1e-4 |
| Production (critical) | 1e-5 |
| Safety-critical | 1e-6 |

### Calibrating Thresholds

1. Run tests on known-good reference implementation
2. Measure baseline numerical error
3. Set threshold at 10x baseline
4. Document reasoning

## Integration with Development

### When to Audit

- After initial implementation
- After any architecture change
- After dependency updates
- Before deployment/release
- After performance optimizations

### CI/CD Integration

```yaml
# Example CI check
equivariance_tests:
  script:
    - python -m pytest tests/test_equivariance.py
  rules:
    - changes to model/**/*
    - changes to layers/**/*
```

## References

- [Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges](https://arxiv.org/abs/2104.13478)
- e3nn documentation on testing
- escnn verification guidelines

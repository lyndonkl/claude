# Equivariance Debugging Guide

Step-by-step guide for diagnosing and fixing equivariance bugs.

## Debugging Workflow

```
1. Confirm the bug exists
   └─> Run end-to-end equivariance test

2. Localize the problem
   └─> Run layer-by-layer tests

3. Identify the root cause
   └─> Check common failure patterns

4. Apply the fix
   └─> Implement correction

5. Verify the fix
   └─> Re-run tests
```

## Step 1: Confirm the Bug

### Symptoms of Broken Equivariance

- **Training instability**: Loss oscillates or doesn't converge
- **Inconsistent predictions**: Same input rotated gives different results
- **Test failure**: Equivariance error > threshold
- **Generalization gap**: Model fails on transformed test data

### Quick Diagnostic Test

```python
def diagnose_equivariance(model, x, transform, threshold=1e-3):
    """Quick diagnostic for equivariance issues."""
    model.eval()

    y_orig = model(x)
    y_trans = model(transform(x))

    error = torch.norm(y_trans - y_orig).item()

    print(f"Equivariance error: {error:.2e}")
    print(f"Threshold: {threshold:.2e}")
    print(f"Status: {'PASS' if error < threshold else 'FAIL'}")

    return error
```

## Step 2: Localize the Problem

### Layer-by-Layer Testing

```python
def find_breaking_layer(model, x, transform):
    """Identify which layer breaks equivariance."""

    # Hook to capture intermediate outputs
    intermediates = {}

    def hook(name):
        def fn(module, input, output):
            intermediates[name] = output.clone()
        return fn

    # Register hooks
    handles = []
    for name, layer in model.named_modules():
        handles.append(layer.register_forward_hook(hook(name)))

    # Forward pass on original input
    model.eval()
    with torch.no_grad():
        model(x)
    orig_intermediates = dict(intermediates)
    intermediates.clear()

    # Forward pass on transformed input
    with torch.no_grad():
        model(transform(x))
    trans_intermediates = dict(intermediates)

    # Clean up hooks
    for h in handles:
        h.remove()

    # Compare intermediates
    print("Layer-by-layer equivariance errors:")
    print("-" * 50)

    for name in orig_intermediates:
        orig = orig_intermediates[name]
        trans = trans_intermediates[name]

        # Note: you may need to transform orig for equivariant comparison
        error = torch.norm(trans - orig).item()
        status = "OK" if error < 1e-3 else "SUSPECT"

        print(f"{name}: {error:.2e} [{status}]")

    return orig_intermediates, trans_intermediates
```

### Binary Search for Large Models

```python
def binary_search_breaking_point(model, x, transform, layers):
    """Binary search to find first breaking layer."""

    def test_up_to(n):
        """Test first n layers only."""
        partial_model = torch.nn.Sequential(*layers[:n])
        # Run equivariance test on partial model
        ...

    low, high = 0, len(layers)

    while low < high:
        mid = (low + high) // 2
        if test_up_to(mid) < threshold:
            low = mid + 1
        else:
            high = mid

    return low  # First breaking layer index
```

## Step 3: Common Failure Patterns

### Pattern 1: Non-Equivariant Nonlinearity

**Symptom**: Error increases after ReLU/activation layers

**Example of broken code**:
```python
# WRONG: ReLU on vector features breaks equivariance
h = F.relu(vector_features)  # vectors are l=1 irreps
```

**Fix**:
```python
# Option 1: Norm-based activation
norm = torch.norm(vector_features, dim=-1, keepdim=True)
h = F.relu(norm) * vector_features / (norm + 1e-8)

# Option 2: Gated activation
gate = torch.sigmoid(scalar_features)
h = gate.unsqueeze(-1) * vector_features

# Option 3: Only activate scalars
scalars = F.relu(scalar_features)  # l=0 irreps
vectors = vector_features  # l=1 irreps unchanged
```

### Pattern 2: Batch Normalization

**Symptom**: Error varies with batch composition or rotation angle

**Why it breaks**: BN computes statistics that aren't equivariant

**Fix options**:
```python
# Option 1: Layer Normalization
h = F.layer_norm(h, h.shape[-1:])

# Option 2: Instance Normalization
h = F.instance_norm(h)

# Option 3: Equivariant Batch Norm (normalize per irrep)
# In e3nn:
from e3nn.nn import BatchNorm
bn = BatchNorm(irreps)
```

### Pattern 3: Padding Issues

**Symptom**: Higher error near image/volume boundaries

**Why it breaks**: Zero padding isn't equivariant to rotations

**Fix**:
```python
# Option 1: Circular padding (for periodic data)
h = F.pad(h, padding, mode='circular')

# Option 2: Replicate padding
h = F.pad(h, padding, mode='replicate')

# Option 3: Larger valid region
# Crop outputs to avoid boundary effects
```

### Pattern 4: Incorrect Representation Matching

**Symptom**: Error at layer boundaries, especially after tensor products

**Example of broken code**:
```python
# WRONG: Mismatched irreps between layers
tp = o3.FullyConnectedTensorProduct(
    "1x0e + 1x1o",
    "1x1o",
    "1x0e + 1x1o"  # Should this be 1x1e?
)
```

**Fix**: Verify irrep parity matches expected output:
```python
# Check what tensor product actually produces
print(tp.irreps_out)  # Verify this matches expectations

# Ensure downstream layers expect the correct irreps
```

### Pattern 5: Numerical Precision

**Symptom**: Small but consistent error everywhere

**Diagnosis**:
```python
# Test in float64
model = model.double()
x = x.double()
# If error drops significantly, it's precision
```

**Fix**:
```python
# Option 1: Use float64 where precision matters
model = model.double()

# Option 2: More numerically stable operations
# Replace: torch.sqrt(x)
# With: torch.sqrt(x + eps)

# Option 3: Orthogonalize rotation matrices periodically
R = orthogonalize(R)  # Gram-Schmidt or SVD
```

### Pattern 6: Custom Layer Bug

**Symptom**: Error isolated to one specific layer

**Debugging checklist**:
```
□ Weight sharing correct?
□ Tensor contraction indices correct?
□ Correct handling of batch dimension?
□ Proper initialization?
□ All operations differentiable?
```

**Debug technique**:
```python
# Test the layer in isolation
def test_layer_isolation(layer, x, transform_in, transform_out):
    layer.eval()

    with torch.no_grad():
        # Transform then layer
        y1 = layer(transform_in(x))

        # Layer then transform
        y2 = transform_out(layer(x))

        error = torch.norm(y1 - y2)

        # Print intermediate values for inspection
        print(f"Input shape: {x.shape}")
        print(f"Output shape: {y1.shape}")
        print(f"Error: {error:.2e}")

        # Check specific values
        print(f"y1 sample: {y1[0, :5]}")
        print(f"y2 sample: {y2[0, :5]}")

    return error
```

## Step 4: Verification After Fix

### Regression Test

```python
def verify_fix(model_old, model_new, x, transform, n_tests=100):
    """Verify that fix improves equivariance."""

    errors_old = []
    errors_new = []

    for _ in range(n_tests):
        T = sample_transform()

        # Old model
        y1_old = model_old(transform(x, T))
        y2_old = transform(model_old(x), T)
        errors_old.append(torch.norm(y1_old - y2_old).item())

        # New model
        y1_new = model_new(transform(x, T))
        y2_new = transform(model_new(x), T)
        errors_new.append(torch.norm(y1_new - y2_new).item())

    print(f"Old model - max error: {max(errors_old):.2e}")
    print(f"New model - max error: {max(errors_new):.2e}")
    print(f"Improvement: {max(errors_old) / max(errors_new):.1f}x")
```

## Debugging Checklist

Before declaring the model equivariant:

```
□ End-to-end test passes
□ Layer-by-layer tests pass
□ Gradient equivariance verified
□ Multiple input samples tested
□ Full transform range tested
□ Both float32 and float64 tested
□ CPU and GPU tested
□ Different batch sizes tested
```

## Quick Reference: Layer Types and Equivariance

| Layer Type | Usually Equivariant? | Common Issues |
|------------|---------------------|---------------|
| Linear | No | Need weight sharing |
| Conv2d | Translation only | Rotation breaks it |
| G-Conv | Yes (for group G) | Implementation bugs |
| ReLU | No | Use on invariants only |
| BatchNorm | No | Use LayerNorm |
| LayerNorm | Yes | Check normalization dim |
| Dropout | Yes | Same mask for transforms |
| MaxPool | No (usually) | Depends on symmetry |
| MeanPool | Yes (for global) | OK for invariance |
| Attention | Permutation | Position encoding matters |
| TensorProduct | Yes | Check irrep matching |

## When to Ask for Help

If you've tried the above and still can't fix the issue:

1. **Minimal reproduction**: Create smallest failing example
2. **Document what you tried**: List debugging steps taken
3. **Share exact error values**: Include test output
4. **Library versions**: Note e3nn, PyTorch versions
5. **Check library issues**: Search GitHub issues for similar problems

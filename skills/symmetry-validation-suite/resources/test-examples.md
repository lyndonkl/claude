# Symmetry Validation Test Examples

Concrete examples of symmetry validation tests for common scenarios.

## Example 1: Image Rotation Invariance (C4)

### Scenario
Testing if an image classifier is invariant to 90° rotations.

### Setup
```python
import torch
import torch.nn.functional as F
import numpy as np

def rotate_image_90(img, k):
    """Rotate image by k * 90 degrees."""
    return torch.rot90(img, k, dims=[-2, -1])

def test_c4_invariance(model, images, threshold=1e-4):
    """
    Test C4 (90° rotation) invariance.

    Args:
        model: Image classifier
        images: Batch of images [B, C, H, W]
        threshold: Maximum allowed difference

    Returns:
        dict with test results
    """
    model.eval()
    results = []

    with torch.no_grad():
        # Get predictions for original images
        pred_original = model(images)

        # Test all 4 rotations
        for k in [1, 2, 3]:  # 90°, 180°, 270°
            rotated = rotate_image_90(images, k)
            pred_rotated = model(rotated)

            error = torch.abs(pred_rotated - pred_original).max().item()
            results.append({
                'rotation': k * 90,
                'max_error': error,
                'pass': error < threshold
            })

    return {
        'group': 'C4',
        'tests': results,
        'overall_pass': all(r['pass'] for r in results)
    }
```

### Expected Output
```
C4 Invariance Test Results:
- 90° rotation: max_error=2.3e-6, PASS
- 180° rotation: max_error=1.8e-6, PASS
- 270° rotation: max_error=2.1e-6, PASS
Overall: PASS
```

## Example 2: 3D Point Cloud SO(3) Equivariance

### Scenario
Testing if a point cloud network produces equivariant features under 3D rotations.

### Setup
```python
import torch
from scipy.spatial.transform import Rotation

def random_rotation_matrix():
    """Generate random SO(3) rotation matrix."""
    return torch.tensor(Rotation.random().as_matrix(), dtype=torch.float32)

def rotate_points(points, R):
    """Rotate point cloud. points: [B, N, 3]"""
    return torch.einsum('ij,bnj->bni', R, points)

def rotate_vectors(vectors, R):
    """Rotate vector features. vectors: [B, N, 3]"""
    return torch.einsum('ij,bnj->bni', R, vectors)

def test_so3_equivariance(model, points, n_tests=50, threshold=1e-3):
    """
    Test SO(3) equivariance for vector outputs.

    Args:
        model: Network that outputs [B, N, 3] vectors
        points: Input point cloud [B, N, 3]
        n_tests: Number of random rotations to test
        threshold: Error threshold for relative error
    """
    model.eval()
    errors = []

    with torch.no_grad():
        for _ in range(n_tests):
            R = random_rotation_matrix()

            # Method 1: Rotate input, then model
            points_rotated = rotate_points(points, R)
            output1 = model(points_rotated)

            # Method 2: Model, then rotate output
            output_original = model(points)
            output2 = rotate_vectors(output_original, R)

            # Compute relative error
            error = torch.norm(output1 - output2) / (torch.norm(output2) + 1e-8)
            errors.append(error.item())

    return {
        'group': 'SO(3)',
        'symmetry_type': 'equivariance',
        'n_tests': n_tests,
        'mean_relative_error': np.mean(errors),
        'max_relative_error': np.max(errors),
        'pass': np.max(errors) < threshold
    }
```

## Example 3: Graph Permutation Invariance

### Scenario
Testing if a graph neural network is invariant to node reordering.

### Setup
```python
def permute_graph(node_features, edge_index, perm):
    """
    Permute nodes in a graph.

    Args:
        node_features: [N, F] node feature matrix
        edge_index: [2, E] edge connectivity
        perm: permutation tensor [N]
    """
    # Permute node features
    new_features = node_features[perm]

    # Permute edge indices
    inv_perm = torch.argsort(perm)
    new_edge_index = inv_perm[edge_index]

    return new_features, new_edge_index

def test_permutation_invariance(model, node_features, edge_index, n_tests=100):
    """
    Test Sn (permutation) invariance for graph-level output.
    """
    model.eval()
    N = node_features.size(0)
    errors = []

    with torch.no_grad():
        # Original prediction
        pred_original = model(node_features, edge_index)

        for _ in range(n_tests):
            # Random permutation
            perm = torch.randperm(N)
            new_features, new_edges = permute_graph(
                node_features, edge_index, perm
            )

            pred_permuted = model(new_features, new_edges)
            error = torch.abs(pred_permuted - pred_original).max().item()
            errors.append(error)

    return {
        'group': f'S{N}',
        'symmetry_type': 'invariance',
        'mean_error': np.mean(errors),
        'max_error': np.max(errors),
        'pass': np.max(errors) < 1e-5
    }
```

## Example 4: E(3) Equivariance for Molecular Forces

### Scenario
Testing if a molecular model predicts forces that transform correctly under E(3).

### Setup
```python
def test_e3_force_equivariance(model, positions, atom_types, n_tests=50):
    """
    Test E(3) equivariance for force predictions.
    Forces should rotate with the molecule and be translation-invariant.
    """
    model.eval()
    results = {'rotation': [], 'translation': [], 'reflection': []}

    with torch.no_grad():
        forces_original = model(positions, atom_types)

        for _ in range(n_tests):
            # Test rotation equivariance
            R = random_rotation_matrix()
            pos_rot = rotate_points(positions, R)
            forces_rot = model(pos_rot, atom_types)
            expected = rotate_vectors(forces_original, R)
            rot_error = relative_error(forces_rot, expected)
            results['rotation'].append(rot_error)

            # Test translation invariance
            t = torch.randn(1, 1, 3) * 10
            pos_trans = positions + t
            forces_trans = model(pos_trans, atom_types)
            trans_error = relative_error(forces_trans, forces_original)
            results['translation'].append(trans_error)

            # Test reflection equivariance
            P = torch.diag(torch.tensor([1., 1., -1.]))  # Reflect z
            pos_ref = positions @ P.T
            forces_ref = model(pos_ref, atom_types)
            expected_ref = forces_original @ P.T
            ref_error = relative_error(forces_ref, expected_ref)
            results['reflection'].append(ref_error)

    return {
        'group': 'E(3)',
        'output_type': 'force vectors (equivariant)',
        'rotation_equivariance': {
            'mean': np.mean(results['rotation']),
            'max': np.max(results['rotation']),
            'pass': np.max(results['rotation']) < 1e-3
        },
        'translation_invariance': {
            'mean': np.mean(results['translation']),
            'max': np.max(results['translation']),
            'pass': np.max(results['translation']) < 1e-5
        },
        'reflection_equivariance': {
            'mean': np.mean(results['reflection']),
            'max': np.max(results['reflection']),
            'pass': np.max(results['reflection']) < 1e-3
        }
    }
```

## Example 5: Testing Group Structure

### Scenario
Verifying that transformations actually form a valid group.

### Setup
```python
def test_group_axioms(transform_fn, compose_fn, inverse_fn, identity, n_tests=100):
    """
    Test that transformations satisfy group axioms.

    Args:
        transform_fn: Function to sample random group elements
        compose_fn: Function to compose two elements (g1, g2) -> g1 * g2
        inverse_fn: Function to compute inverse
        identity: Identity element
    """
    results = {
        'closure': [],
        'associativity': [],
        'identity': [],
        'inverse': []
    }

    for _ in range(n_tests):
        g1 = transform_fn()
        g2 = transform_fn()
        g3 = transform_fn()

        # Closure: g1 * g2 should be valid group element
        g12 = compose_fn(g1, g2)
        results['closure'].append(is_valid_element(g12))

        # Associativity: (g1 * g2) * g3 = g1 * (g2 * g3)
        left = compose_fn(compose_fn(g1, g2), g3)
        right = compose_fn(g1, compose_fn(g2, g3))
        results['associativity'].append(
            np.allclose(left, right, atol=1e-6)
        )

        # Identity: g * e = e * g = g
        ge = compose_fn(g1, identity)
        eg = compose_fn(identity, g1)
        results['identity'].append(
            np.allclose(ge, g1, atol=1e-6) and
            np.allclose(eg, g1, atol=1e-6)
        )

        # Inverse: g * g^-1 = e
        g_inv = inverse_fn(g1)
        gg_inv = compose_fn(g1, g_inv)
        results['inverse'].append(
            np.allclose(gg_inv, identity, atol=1e-6)
        )

    return {
        'closure': all(results['closure']),
        'associativity': all(results['associativity']),
        'identity': all(results['identity']),
        'inverse': all(results['inverse']),
        'is_valid_group': all([
            all(results['closure']),
            all(results['associativity']),
            all(results['identity']),
            all(results['inverse'])
        ])
    }
```

## Interpreting Results

### Pass Criteria

| Test Type | Threshold | Interpretation |
|-----------|-----------|----------------|
| Exact symmetry | < 1e-6 | Built-in equivariance |
| Approximate | 1e-6 to 1e-3 | Acceptable numerical error |
| Weak | 1e-3 to 0.01 | May need investigation |
| Failed | > 0.01 | Symmetry broken |

### Common Issues

1. **High error on specific transforms**: Check boundary handling
2. **Error grows with batch size**: Batch normalization issue
3. **Error varies between runs**: Non-deterministic operations
4. **Error only at certain angles**: Interpolation artifacts

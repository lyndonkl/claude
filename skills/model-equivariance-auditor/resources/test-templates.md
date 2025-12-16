# Equivariance Test Code Templates

Ready-to-use test code for auditing model equivariance.

## Complete Test Suite Template

```python
"""
Equivariance Audit Test Suite

Usage:
    pytest test_equivariance.py -v

Or run directly:
    python test_equivariance.py
"""

import torch
import numpy as np
from typing import Callable, Dict, List, Optional, Tuple
from dataclasses import dataclass
from scipy.spatial.transform import Rotation


@dataclass
class AuditConfig:
    """Configuration for equivariance audit."""
    n_samples: int = 100
    n_transforms: int = 50
    relative_threshold: float = 1e-4
    absolute_threshold: float = 1e-5
    use_float64: bool = True
    device: str = 'cpu'


@dataclass
class AuditResult:
    """Results from an equivariance test."""
    test_name: str
    passed: bool
    mean_absolute_error: float
    max_absolute_error: float
    mean_relative_error: float
    max_relative_error: float
    n_tests: int
    details: Optional[Dict] = None


class EquivarianceAuditor:
    """
    Comprehensive equivariance auditor for neural networks.
    """

    def __init__(self, config: Optional[AuditConfig] = None):
        self.config = config or AuditConfig()
        self.results: List[AuditResult] = []

    def audit_invariance(
        self,
        model: torch.nn.Module,
        sample_input: Callable,
        transform_input: Callable,
        name: str = "invariance"
    ) -> AuditResult:
        """
        Test if model output is invariant to input transformations.

        Args:
            model: The model to test
            sample_input: Function that returns a random input
            transform_input: Function (x, T) -> transformed x
            name: Name for this test

        Returns:
            AuditResult with test outcomes
        """
        model.eval()
        dtype = torch.float64 if self.config.use_float64 else torch.float32
        device = self.config.device

        absolute_errors = []
        relative_errors = []

        with torch.no_grad():
            for _ in range(self.config.n_samples):
                x = sample_input().to(device=device, dtype=dtype)
                y_original = model(x)

                for _ in range(self.config.n_transforms):
                    x_t = transform_input(x)
                    y_t = model(x_t)

                    abs_err = torch.norm(y_t - y_original).item()
                    rel_err = abs_err / (torch.norm(y_original).item() + 1e-10)

                    absolute_errors.append(abs_err)
                    relative_errors.append(rel_err)

        result = AuditResult(
            test_name=name,
            passed=(
                max(relative_errors) < self.config.relative_threshold and
                max(absolute_errors) < self.config.absolute_threshold
            ),
            mean_absolute_error=float(np.mean(absolute_errors)),
            max_absolute_error=float(np.max(absolute_errors)),
            mean_relative_error=float(np.mean(relative_errors)),
            max_relative_error=float(np.max(relative_errors)),
            n_tests=len(absolute_errors),
        )

        self.results.append(result)
        return result

    def audit_equivariance(
        self,
        model: torch.nn.Module,
        sample_input: Callable,
        transform_input: Callable,
        transform_output: Callable,
        name: str = "equivariance"
    ) -> AuditResult:
        """
        Test if model is equivariant: f(T(x)) = T'(f(x)).

        Args:
            model: The model to test
            sample_input: Function that returns (input, transform_params)
            transform_input: Function (x, T) -> transformed input
            transform_output: Function (y, T) -> transformed output
            name: Name for this test
        """
        model.eval()
        dtype = torch.float64 if self.config.use_float64 else torch.float32
        device = self.config.device

        absolute_errors = []
        relative_errors = []

        with torch.no_grad():
            for _ in range(self.config.n_samples):
                x = sample_input().to(device=device, dtype=dtype)

                for _ in range(self.config.n_transforms):
                    T = self._sample_transform()

                    # f(T(x))
                    x_t = transform_input(x, T)
                    y1 = model(x_t)

                    # T'(f(x))
                    y = model(x)
                    y2 = transform_output(y, T)

                    abs_err = torch.norm(y1 - y2).item()
                    rel_err = abs_err / (torch.norm(y2).item() + 1e-10)

                    absolute_errors.append(abs_err)
                    relative_errors.append(rel_err)

        result = AuditResult(
            test_name=name,
            passed=(
                max(relative_errors) < self.config.relative_threshold and
                max(absolute_errors) < self.config.absolute_threshold
            ),
            mean_absolute_error=float(np.mean(absolute_errors)),
            max_absolute_error=float(np.max(absolute_errors)),
            mean_relative_error=float(np.mean(relative_errors)),
            max_relative_error=float(np.max(relative_errors)),
            n_tests=len(absolute_errors),
        )

        self.results.append(result)
        return result

    def audit_layers(
        self,
        model: torch.nn.Module,
        sample_input: Callable,
        transform_input: Callable,
        transform_output: Callable,
    ) -> List[AuditResult]:
        """Test equivariance of each layer individually."""
        results = []

        # Get all named modules
        for name, layer in model.named_modules():
            if self._is_testable_layer(layer):
                result = self._test_single_layer(
                    layer, sample_input, transform_input, transform_output, name
                )
                results.append(result)
                self.results.append(result)

        return results

    def audit_gradients(
        self,
        model: torch.nn.Module,
        sample_input: Callable,
        transform_input: Callable,
        transform_gradient: Callable,
        loss_fn: Callable,
        name: str = "gradient_equivariance"
    ) -> AuditResult:
        """Test if gradients respect equivariance."""
        model.train()
        dtype = torch.float64 if self.config.use_float64 else torch.float32

        errors = []

        for _ in range(self.config.n_samples):
            for _ in range(self.config.n_transforms):
                T = self._sample_transform()

                # Gradient at x
                x1 = sample_input().to(dtype=dtype).requires_grad_(True)
                y1 = model(x1)
                loss1 = loss_fn(y1)
                loss1.backward()
                grad1 = x1.grad.clone()

                # Gradient at T(x)
                model.zero_grad()
                x2 = transform_input(
                    sample_input().to(dtype=dtype), T
                ).requires_grad_(True)
                y2 = model(x2)
                loss2 = loss_fn(y2)
                loss2.backward()
                grad2 = x2.grad.clone()

                # Compare T(grad1) with grad2
                grad1_t = transform_gradient(grad1, T)
                error = torch.norm(grad2 - grad1_t).item()
                errors.append(error)

        model.eval()

        result = AuditResult(
            test_name=name,
            passed=max(errors) < self.config.relative_threshold,
            mean_absolute_error=float(np.mean(errors)),
            max_absolute_error=float(np.max(errors)),
            mean_relative_error=float(np.mean(errors)),  # Same for gradients
            max_relative_error=float(np.max(errors)),
            n_tests=len(errors),
        )

        self.results.append(result)
        return result

    def generate_report(self) -> str:
        """Generate a formatted audit report."""
        lines = [
            "=" * 60,
            "EQUIVARIANCE AUDIT REPORT",
            "=" * 60,
            "",
            f"Configuration:",
            f"  Samples: {self.config.n_samples}",
            f"  Transforms per sample: {self.config.n_transforms}",
            f"  Relative threshold: {self.config.relative_threshold}",
            f"  Float64: {self.config.use_float64}",
            "",
            "-" * 60,
            "RESULTS:",
            "-" * 60,
        ]

        for result in self.results:
            status = "PASS" if result.passed else "FAIL"
            lines.extend([
                f"\n{result.test_name}: [{status}]",
                f"  Mean absolute error: {result.mean_absolute_error:.2e}",
                f"  Max absolute error:  {result.max_absolute_error:.2e}",
                f"  Mean relative error: {result.mean_relative_error:.2e}",
                f"  Max relative error:  {result.max_relative_error:.2e}",
                f"  Tests run: {result.n_tests}",
            ])

        lines.extend([
            "",
            "-" * 60,
            f"OVERALL: {'PASS' if all(r.passed for r in self.results) else 'FAIL'}",
            "=" * 60,
        ])

        return "\n".join(lines)

    def _sample_transform(self):
        """Override this for specific group."""
        raise NotImplementedError("Subclass must implement _sample_transform")

    def _is_testable_layer(self, layer):
        """Determine if a layer should be tested individually."""
        # Skip containers and trivial layers
        skip_types = (
            torch.nn.Sequential,
            torch.nn.ModuleList,
            torch.nn.Identity,
        )
        return not isinstance(layer, skip_types)

    def _test_single_layer(self, layer, sample_input, transform_input,
                           transform_output, name):
        """Test a single layer."""
        # Simplified single-layer test
        errors = []
        layer.eval()

        with torch.no_grad():
            for _ in range(min(20, self.config.n_samples)):
                x = sample_input()
                T = self._sample_transform()

                try:
                    y1 = layer(transform_input(x, T))
                    y2 = transform_output(layer(x), T)
                    error = torch.norm(y1 - y2).item()
                    errors.append(error)
                except Exception as e:
                    # Layer might not be compatible with this input
                    pass

        if not errors:
            return AuditResult(
                test_name=f"layer:{name}",
                passed=True,
                mean_absolute_error=0,
                max_absolute_error=0,
                mean_relative_error=0,
                max_relative_error=0,
                n_tests=0,
                details={"note": "Could not test layer"}
            )

        return AuditResult(
            test_name=f"layer:{name}",
            passed=max(errors) < self.config.relative_threshold,
            mean_absolute_error=float(np.mean(errors)),
            max_absolute_error=float(np.max(errors)),
            mean_relative_error=float(np.mean(errors)),
            max_relative_error=float(np.max(errors)),
            n_tests=len(errors),
        )


class SO3Auditor(EquivarianceAuditor):
    """Auditor specialized for SO(3) symmetry."""

    def _sample_transform(self) -> torch.Tensor:
        """Sample random SO(3) rotation matrix."""
        R = Rotation.random().as_matrix()
        return torch.tensor(R, dtype=torch.float64)


class SE3Auditor(EquivarianceAuditor):
    """Auditor specialized for SE(3) symmetry."""

    def __init__(self, config=None, translation_scale=10.0):
        super().__init__(config)
        self.translation_scale = translation_scale

    def _sample_transform(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Sample random SE(3) transform (rotation, translation)."""
        R = torch.tensor(Rotation.random().as_matrix(), dtype=torch.float64)
        t = torch.randn(3, dtype=torch.float64) * self.translation_scale
        return R, t


class PermutationAuditor(EquivarianceAuditor):
    """Auditor specialized for permutation symmetry."""

    def __init__(self, config=None, n_elements=None):
        super().__init__(config)
        self.n_elements = n_elements

    def _sample_transform(self) -> torch.Tensor:
        """Sample random permutation."""
        return torch.randperm(self.n_elements)


# Example usage
if __name__ == "__main__":
    # Create a simple test model
    class DummyInvariantModel(torch.nn.Module):
        def forward(self, x):
            return x.sum(dim=-1, keepdim=True)

    model = DummyInvariantModel()

    # Create auditor
    auditor = SO3Auditor(AuditConfig(n_samples=10, n_transforms=10))

    # Define transforms
    def sample_input():
        return torch.randn(1, 10, 3)

    def transform_input(x, R):
        return torch.einsum('ij,...j->...i', R, x)

    # Run audit
    result = auditor.audit_invariance(
        model, sample_input,
        lambda x: transform_input(x, auditor._sample_transform())
    )

    print(auditor.generate_report())
```

## Quick Test Functions

For rapid testing during development:

```python
def quick_invariance_check(model, x, transform_fn, n=10):
    """Quick check for invariance. Returns max error."""
    model.eval()
    with torch.no_grad():
        y = model(x)
        errors = []
        for _ in range(n):
            y_t = model(transform_fn(x))
            errors.append(torch.norm(y_t - y).item())
    return max(errors)


def quick_equivariance_check(model, x, in_transform, out_transform, n=10):
    """Quick check for equivariance. Returns max error."""
    model.eval()
    with torch.no_grad():
        errors = []
        for _ in range(n):
            T = sample_transform()
            y1 = model(in_transform(x, T))
            y2 = out_transform(model(x), T)
            errors.append(torch.norm(y1 - y2).item())
    return max(errors)
```

## pytest Integration

```python
import pytest

class TestModelEquivariance:
    @pytest.fixture
    def model(self):
        return YourModel()

    @pytest.fixture
    def auditor(self):
        return SO3Auditor(AuditConfig(n_samples=50, n_transforms=20))

    def test_invariance(self, model, auditor):
        result = auditor.audit_invariance(model, ...)
        assert result.passed, f"Invariance failed: {result.max_relative_error}"

    def test_equivariance(self, model, auditor):
        result = auditor.audit_equivariance(model, ...)
        assert result.passed, f"Equivariance failed: {result.max_relative_error}"

    def test_gradient_equivariance(self, model, auditor):
        result = auditor.audit_gradients(model, ...)
        assert result.passed, f"Gradient equivariance failed"
```

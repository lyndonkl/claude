# Domain-Specific Symmetry Examples

## Image Data

### Classification Tasks

**Example: Object Recognition**
```
Data: RGB images of objects
Task: Predict object category

Symmetry Analysis:
- Translation: YES (object can be anywhere) → Translation invariance
- Rotation: PARTIAL (some objects have canonical orientation)
  - 90° rotations: Often OK
  - Arbitrary rotation: Depends on object type
- Reflection: PARTIAL (text would be mirrored, faces OK)
- Scale: YES (objects at different distances) → Scale invariance

Result: Translation invariant, approximately rotation invariant
Architecture: CNN with data augmentation, or G-CNN for strict rotation
```

**Example: Medical Imaging**
```
Data: X-ray or MRI scans
Task: Detect pathology

Symmetry Analysis:
- Translation: YES (lesion can be anywhere)
- Rotation: CAREFUL (anatomy has preferred orientation)
  - Small rotations: OK (patient positioning variance)
  - 180° flip: May swap left/right (clinically important!)
- Reflection: NO (left/right matters medically)

Result: Translation invariant, limited rotation, no reflection
Architecture: CNN with careful augmentation
```

### Detection/Segmentation Tasks

**Example: Object Detection**
```
Data: RGB images
Task: Predict bounding boxes

Symmetry Analysis:
- Translation: EQUIVARIANT (box moves with object)
- Rotation: EQUIVARIANT (box rotates with image)
- Scale: EQUIVARIANT (box scales with image)

Result: All geometric transforms are equivariant, not invariant
Architecture: Feature pyramid + equivariant heads
```

---

## 3D Point Cloud Data

### Molecular Property Prediction

**Example: Energy Prediction**
```
Data: 3D atomic coordinates + atom types
Task: Predict molecular energy (scalar)

Symmetry Analysis:
- Translation: YES (energy doesn't depend on position in space)
- Rotation: YES (energy doesn't depend on orientation)
- Reflection: YES (energy same for mirror image)
- Atom permutation: YES (identical atoms are interchangeable)

Result: Full E(3) invariance + permutation invariance
Architecture: SchNet, EGNN, or e3nn-based invariant networks
```

**Example: Force Prediction**
```
Data: 3D atomic coordinates + atom types
Task: Predict forces on each atom (vectors)

Symmetry Analysis:
- Translation: Forces unchanged (invariant)
- Rotation: Forces rotate with system (EQUIVARIANT)
- Reflection: Forces reflect with system (EQUIVARIANT)
- Atom permutation: Force assignments permute (EQUIVARIANT)

Result: Translation invariant, E(3) equivariant, permutation equivariant
Architecture: Equivariant GNN with vector outputs (PaiNN, NequIP)
```

### Robotics/Manipulation

**Example: Grasp Prediction**
```
Data: 3D point cloud of object
Task: Predict grasp poses

Symmetry Analysis:
- Translation: EQUIVARIANT (grasp moves with object)
- Rotation: EQUIVARIANT (grasp rotates with object)
- Gravity: BREAKS rotational symmetry (up is special)

Result: SE(3) equivariance conditioned on gravity direction
Architecture: SE(3)-equivariant network with gravity conditioning
```

---

## Graph Data

### Node Classification

**Example: Social Network Role Prediction**
```
Data: Social network graph
Task: Predict role/community for each node

Symmetry Analysis:
- Node permutation: Labels should permute with nodes (EQUIVARIANT)
- Edge direction: May or may not matter (domain-dependent)

Result: Permutation equivariant
Architecture: GNN (message passing)
```

### Graph Classification

**Example: Molecule Classification**
```
Data: Molecular graph (atoms as nodes, bonds as edges)
Task: Predict property category

Symmetry Analysis:
- Node permutation: Doesn't change molecule → INVARIANT
- Edge permutation: Follows node permutation → INVARIANT

Result: Permutation invariant
Architecture: GNN + global pooling (sum, mean, or attention)
```

---

## Time Series Data

### Forecasting

**Example: Stock Price Prediction**
```
Data: Historical prices over time
Task: Predict future prices

Symmetry Analysis:
- Time shift: Pattern can occur at any time → Time-translation
- Time reversal: Forward ≠ backward (markets are directional)
- Scale: Relative changes matter more than absolute → Scale equivariant

Result: Time-translation invariant, not time-reversal symmetric
Architecture: Temporal convolutions, or Transformers with positional encoding
```

### Anomaly Detection

**Example: Sensor Fault Detection**
```
Data: Sensor readings over time
Task: Detect anomalies

Symmetry Analysis:
- Time shift: Anomaly can occur anytime → Time-translation invariant
- Permutation of sensors: Sensors may be interchangeable → Check domain

Result: Time-translation invariant, possibly sensor-permutation invariant
Architecture: 1D CNN or Transformer
```

---

## Tabular Data

### Feature Analysis

**Example: Customer Churn Prediction**
```
Data: Customer features (age, tenure, usage, etc.)
Task: Predict churn probability

Symmetry Analysis:
- Feature permutation: NO (features have specific meanings)
- Row permutation: YES (customers are independent samples)

Result: No feature-level symmetry (each feature is distinct)
Architecture: Standard MLP, boosting, or tabular Transformer
```

**Example: Set-based Tabular**
```
Data: Set of items purchased
Task: Predict next purchase

Symmetry Analysis:
- Item permutation: YES (order doesn't matter for recommendation)

Result: Permutation invariant over items
Architecture: DeepSets or Set Transformer
```

---

## Physics Simulations

### Particle Systems

**Example: N-body Simulation**
```
Data: Positions and velocities of N particles
Task: Predict future state

Symmetry Analysis:
- Translation: Total momentum conserved → Translation equivariant
- Rotation: Angular momentum conserved → Rotation equivariant
- Particle permutation: Identical particles → Permutation equivariant
- Time reversal: Depends on forces (conservative = yes)

Result: SE(3) equivariant + permutation equivariant
Architecture: EGNN or SE(3)-Transformer
```

### Fluid Dynamics

**Example: Fluid Flow Prediction**
```
Data: Velocity field on grid
Task: Predict future velocity field

Symmetry Analysis:
- Translation: Depends on boundary conditions
- Rotation: Flows rotate with domain → Equivariant
- Reflection: Depends on forcing (turbulence often symmetric)

Result: Careful analysis needed based on specific setup
Architecture: Equivariant CNN or neural operator
```

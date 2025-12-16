# Symmetry Discovery Methodology

## Why Symmetry Discovery Matters

### The Core Insight

Neural networks that respect data symmetries have:
- **Reduced parameter count** through weight sharing
- **Better sample efficiency** - learn once, generalize everywhere
- **Improved generalization** - guaranteed consistent behavior under transformations
- **Faster convergence** - constrained hypothesis space

**Theorem**: For any prediction task where equivariance is correctly specified, there exists an equivariant predictor with strictly lower test risk than any non-equivariant predictor.

### The Discovery Challenge

The challenge is that symmetries are often:
- **Hidden**: Not obvious from looking at raw data
- **Approximate**: Real data has noise and imperfections
- **Domain-specific**: Require expertise to recognize
- **Task-dependent**: Same data may have different symmetries for different tasks

---

## The Systematic Discovery Process

### Phase 1: Domain Understanding

**Goal**: Understand the data's structure and the task's requirements.

**Key Questions**:
1. What physical/abstract space does the data live in?
2. What are the degrees of freedom?
3. What defines "the same" vs. "different" in this domain?
4. What domain knowledge do experts use?

**Common Domain Patterns**:

| Domain | Key Considerations |
|--------|-------------------|
| Images | Pixel grid, color channels, spatial relationships |
| Point Clouds | 3D coordinates, possibly features per point |
| Molecules | Atom types, bond connectivity, 3D geometry |
| Graphs | Node features, edge features, connectivity |
| Time Series | Temporal ordering, sampling rate, stationarity |
| Tabular | Feature semantics, categorical vs. continuous |

### Phase 2: Coordinate Analysis

**Goal**: Identify which aspects of the coordinate system are arbitrary choices.

**The Arbitrary Choice Test**:
For each coordinate system property, ask: "Would a different choice change the underlying reality?"

1. **Origin Selection**
   - Is there a natural center/zero point?
   - Would shifting everything preserve meaning?

2. **Axis Orientation**
   - Is there a natural "up" direction?
   - Is there a reference frame from physics (gravity, magnetic field)?

3. **Handedness**
   - Does left vs. right matter?
   - Are mirror images physically distinct?

4. **Scale/Units**
   - Are absolute sizes meaningful?
   - Would rescaling change the answer?

### Phase 3: Transformation Enumeration

**Goal**: Systematically test candidate transformations.

**The Transformation Catalog**:

#### Geometric Transformations
- **Translation**: Shift in space
- **Rotation**: Change orientation
- **Reflection**: Mirror across plane/axis
- **Scaling**: Uniform resize
- **Shearing**: Non-uniform stretch

#### Structural Transformations
- **Permutation**: Reorder elements
- **Subset selection**: Remove elements
- **Duplication**: Add identical elements

#### Temporal Transformations
- **Time shift**: Move in time
- **Time reversal**: Play backward
- **Time scaling**: Speed up/slow down

#### Domain-Specific Transformations
- **Color shifts** (images)
- **Gauge transformations** (physics)
- **Atom substitution** (chemistry)

### Phase 4: Output Behavior Analysis

**Goal**: Determine how outputs should transform when inputs transform.

**The Output Transformation Matrix**:

| Input Transformation | Output Behavior | Symmetry Type |
|---------------------|-----------------|---------------|
| T(x) | y unchanged | Invariance |
| T(x) | T'(y) for related T' | Equivariance |
| T(x) | Unpredictable | No symmetry |

**Examples by Task Type**:

| Task | Input Transform | Output Behavior |
|------|-----------------|-----------------|
| Image Classification | Rotation | Label unchanged (invariant) |
| Object Detection | Rotation | Boxes rotate (equivariant) |
| Molecular Energy | 3D Rotation | Energy unchanged (invariant) |
| Force Prediction | 3D Rotation | Forces rotate (equivariant) |
| Graph Classification | Node permutation | Label unchanged (invariant) |
| Node Classification | Node permutation | Labels permute (equivariant) |

---

## Handling Ambiguous Cases

### Approximate Symmetries

Real data often has **approximate** rather than exact symmetries.

**Detection Strategies**:
1. Check if augmentation with T improves validation performance
2. Measure sensitivity of model outputs to transformation T
3. Look for consistent patterns across training examples

**Design Choices**:
- **Hard constraint**: Build exact equivariance into architecture
- **Soft constraint**: Use equivariance-encouraging regularization
- **Data augmentation**: Let model learn approximate equivariance

### Broken Symmetries

Some symmetries are **broken** by external factors:

**Examples**:
- Gravity breaks rotational symmetry for falling objects
- Edge effects break translation symmetry near boundaries
- Camera orientation breaks rotation symmetry in natural images

**Strategies**:
1. Identify what breaks the symmetry
2. Condition on the symmetry-breaking factor
3. Use partial/local equivariance

### Task-Dependent Symmetries

The **same data** may have different symmetries for **different tasks**:

**Example - Molecule Data**:
- Energy prediction: Full E(3) invariance
- Force prediction: E(3) equivariance
- Chirality classification: Only SE(3), not reflection

**Strategy**: Always analyze symmetries relative to the specific task.

---

## Common Pitfalls

### Pitfall 1: Assuming Symmetries Without Verification
- **Problem**: Building equivariant model for non-existent symmetry
- **Solution**: Always validate empirically before committing

### Pitfall 2: Missing Broken Symmetries
- **Problem**: Assuming full symmetry when partial applies
- **Solution**: Consider external factors, boundary conditions

### Pitfall 3: Confusing Data Symmetry with Label Symmetry
- **Problem**: Data may be symmetric, but task may not be
- **Solution**: Always ask "how should the OUTPUT transform?"

### Pitfall 4: Over-constraining
- **Problem**: Too much symmetry limits model expressiveness
- **Solution**: Start with obvious symmetries, add cautiously

### Pitfall 5: Ignoring Approximate Symmetries
- **Problem**: Requiring exact symmetry when approximate works
- **Solution**: Consider soft equivariance or augmentation for noisy cases

---

## Integration with Other Skills

After completing symmetry discovery:

1. **Uncertain symmetries?** → Use `symmetry-validation-suite` to test
2. **Ready to formalize?** → Use `symmetry-group-identifier` to map to groups
3. **Ready to build?** → Use `equivariant-architecture-designer` for model design
4. **Model complete?** → Use `model-equivariance-auditor` to verify

# Fermi Estimation Templates

Quick-start templates for decomposition, component estimation, bounding, and sanity-checking.

## Workflow

```
Fermi Estimation Progress:
- [ ] Step 1: Clarify the question and define metric
- [ ] Step 2: Decompose into estimable components
- [ ] Step 3: Estimate components using anchors
- [ ] Step 4: Bound with upper/lower limits
- [ ] Step 5: Calculate and sanity-check
- [ ] Step 6: Triangulate with alternate path
```

**Step 1: Clarify the question and define metric**

Use [Clarification Template](#clarification-template) to restate question precisely with units, scope, timeframe, and decision context.

**Step 2: Decompose into estimable components**

Select decomposition strategy using [Decomposition Strategies](#decomposition-strategies) and build estimation tree.

**Step 3: Estimate components using anchors**

Ground each component in known quantities using [Component Estimation Template](#component-estimation-template).

**Step 4: Bound with upper/lower limits**

Calculate optimistic and pessimistic bounds using [Bounding Template](#bounding-template).

**Step 5: Calculate and sanity-check**

Compute central estimate and validate using [Sanity-Check Template](#sanity-check-template).

**Step 6: Triangulate with alternate path**

Re-estimate via different decomposition using [Triangulation Template](#triangulation-template) to validate.

---

## Clarification Template

**Original Question**: [As stated]

**Clarified Question**:
- **What exactly are we estimating?** (metric name, definition)
- **Units?** (dollars, people, tons, requests/sec, etc.)
- **Geographic scope?** (US, global, city, region)
- **Time scope?** (annual, daily, lifetime, point-in-time)
- **Exclusions?** (what are we NOT counting?)

**Decision Context**:
- **What decision depends on this estimate?**
- **What precision is needed?** (order of magnitude sufficient? need ±2x? ±10%?)
- **How will estimate be used?** (go/no-go decision, budget planning, prioritization)
- **What threshold matters?** (if >X we do Y, if <Z we don't)

**Success Criteria**:
- [ ] Question is unambiguous (two people would estimate same thing)
- [ ] Units are specified
- [ ] Scope is bounded (not infinite)
- [ ] Decision context is clear

---

## Decomposition Strategies

Choose strategy based on question structure and available knowledge.

### Top-Down Filtering

**When to use**: Estimating subset of total population (market sizing, target audience)

**Structure**: Start with total, apply filters to narrow down

**Template**:
```
Total population
× Filter 1 (% that have characteristic A)
× Filter 2 (% that have characteristic B | A)
× Filter 3 (% that have characteristic C | A,B)
= Target population
```

**Example - TAM estimation**:
```
US population (330M)
× Adults 18-65 (65% = 215M)
× Urban/suburban (80% = 172M)
× Smartphone users (90% = 155M)
× Willing to pay for app (5% = 7.75M)
× Price point ($50/year)
= TAM: ~$390M/year
```

### Bottom-Up Scaling

**When to use**: Have data on units, want to estimate total (revenue, capacity, production)

**Structure**: Start with single unit, multiply by count

**Template**:
```
Output per unit
× Number of units
× Utilization rate (% of theoretical capacity actually used)
= Total output
```

**Example - Server capacity**:
```
1 server handles 10k requests/sec
× 100 servers in cluster
× 70% utilization (peak headroom, maintenance, failures)
= Cluster capacity: 700k requests/sec
```

### Rate × Time

**When to use**: Estimating accumulation over time (customers served, miles driven, content consumed)

**Structure**: Flow rate × Duration

**Template**:
```
Rate (per time unit)
× Time duration (in same units)
= Total quantity
```

**Example - Annual customers**:
```
50 customers/day
× 250 business days/year
= 12,500 customers/year
```

### Density × Area/Volume

**When to use**: Spatial estimation (people in stadium, cars on highway, storage capacity)

**Structure**: Concentration × Space

**Template**:
```
Density (per unit area/volume)
× Total area/volume
= Total quantity
```

**Example - Stadium capacity**:
```
4 people/sq meter (seated)
× 10,000 sq meters seating area
= 40,000 capacity
```

### Analogous Scaling

**When to use**: Have data on similar system, adjusting for size difference

**Structure**: Known comparable × Scaling factor

**Template**:
```
Comparable system value
× (Our scale / Their scale)^exponent
= Our estimate

Exponent = 1 for linear scaling, <1 for economies of scale, >1 for diseconomies
```

**Example - Competitor revenue**:
```
Competitor A revenue: $100M with 500k users
Our users: 50k
Estimate: $100M × (50k/500k) = $10M
(assumes linear revenue per user)
```

---

## Component Estimation Template

For each component in decomposition:

**Component**: [Name of quantity being estimated]

**Anchor Strategy** (how will we estimate this?):
- [ ] Known data (cite source):
- [ ] Personal experience/intuition (describe basis):
- [ ] Derived from other estimates (show calculation):
- [ ] Analogous comparison (similar known quantity):

**Estimate**: [Value with units]

**Confidence**: (How certain are we?)
- [ ] High (have data or strong knowledge)
- [ ] Medium (reasonable inference)
- [ ] Low (educated guess, wide range)

**Sensitivity**: (How much does final answer depend on this?)
- [ ] High (10% change here → >5% change in final)
- [ ] Medium (10% change here → 1-5% change in final)
- [ ] Low (final answer insensitive to this component)

**Assumption stated**: [Explicit statement of what we're assuming]

---

## Bounding Template

### Optimistic Bound (Upper Limit)

**Scenario**: [What favorable conditions would maximize the estimate?]

**Assumptions**:
- Component 1: [Optimistic value]
- Component 2: [Optimistic value]
- ...

**Calculation**: [Show work]

**Result**: [Upper bound with units]

### Pessimistic Bound (Lower Limit)

**Scenario**: [What unfavorable conditions would minimize the estimate?]

**Assumptions**:
- Component 1: [Pessimistic value]
- Component 2: [Pessimistic value]
- ...

**Calculation**: [Show work]

**Result**: [Lower bound with units]

### Range Assessment

**Bounds**: [Lower] to [Upper]

**Ratio**: Upper/Lower = [X]× range

**Decision Sensitivity**:
- [ ] Decision same across entire range → Estimate good enough
- [ ] Decision changes within range → Need more precision or different approach
- [ ] Range too wide (>10× span) → Decomposition may be flawed, revisit assumptions

---

## Sanity-Check Template

### Dimensional Analysis

**Units Check**: Do units cancel correctly in calculation?
- Calculation: [Show units through formula]
- Final units: [Should match expected units]
- [ ] Units are correct

### Reality Checks

**Check 1 - Order of magnitude comparison**:
- Our estimate: [X]
- Known comparable: [Y]
- Ratio: [X/Y]
- [ ] Within factor of 10? (If not, investigate why)

**Check 2 - Extreme case testing**:
- What if assumption taken to extreme? (e.g., 100% penetration, everyone participates)
- Result: [Calculate]
- [ ] Does it violate physical/economic constraints? (population limits, GDP constraints, physics)

**Check 3 - Internal consistency**:
- Do derived metrics make sense? (profit margins, growth rates, per-capita figures)
- Derived metric: [Calculate, e.g., revenue per employee, cost per user]
- [ ] Is it in reasonable range for industry/domain?

**Check 4 - Personal intuition**:
- Does this "feel right" given your experience?
- [ ] Passes gut check
- [ ] Feels too high (revise assumptions)
- [ ] Feels too low (revise assumptions)

### Common Failure Modes to Check

- [ ] Did I double-count anything?
- [ ] Did I mix units (per day vs per year, millions vs billions)?
- [ ] Am I extrapolating linearly when should be exponential (or vice versa)?
- [ ] Did I account for utilization/efficiency factors (not everything runs at 100%)?
- [ ] Did I consider survivor bias (basing estimate on successful cases only)?

---

## Triangulation Template

### Primary Estimate (from main decomposition)

**Method**: [Top-down, bottom-up, etc.]

**Decomposition**: [Brief formula or tree]

**Result**: [Value with units]

### Alternate Estimate (different approach)

**Method**: [Different strategy than primary]

**Decomposition**: [Brief formula or tree]

**Result**: [Value with units]

### Comparison

**Primary**: [X]
**Alternate**: [Y]
**Ratio**: [X/Y] = [Z]×

**Assessment**:
- [ ] Within factor of 3 (good agreement, increase confidence)
- [ ] Factor of 3-10 (moderate agreement, average or investigate difference)
- [ ] >10× difference (investigate: one decomposition is likely flawed)

**Reconciliation** (if estimates differ):
- Why do they differ? (which assumptions differ?)
- Which approach is more reliable?
- Final estimate: [Choice or average]

---

## Complete Estimation Template

Structure for full documentation:

1. **Clarification**: Original question, clarified with units/scope, decision context
2. **Decomposition**: Strategy (top-down/bottom-up/etc), formula, estimation tree
3. **Component Estimates**: For each component - estimate, anchor, assumption, confidence
4. **Calculation**: Formula with numbers, central estimate (1-2 sig figs)
5. **Bounds**: Optimistic/pessimistic scenarios, range assessment
6. **Sanity Checks**: Units, order of magnitude comparison, extreme cases, consistency, gut check
7. **Triangulation**: Alternate approach, comparison (within factor of 3?), reconciliation
8. **Final Estimate**: Point estimate, range, confidence, key assumptions, sensitivity, recommendation
9. **Next Steps**: Data collection, assumption testing, detailed modeling if precision needed

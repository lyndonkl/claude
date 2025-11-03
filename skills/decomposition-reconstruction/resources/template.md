# Decomposition & Reconstruction Template

## Workflow

Copy this checklist and track your progress:

```
Decomposition & Reconstruction Progress:
- [ ] Step 1: System definition and scoping
- [ ] Step 2: Component decomposition
- [ ] Step 3: Relationship mapping
- [ ] Step 4: Property analysis
- [ ] Step 5: Reconstruction and recommendations
```

**Step 1: System definition and scoping** - Define system, goal, boundaries, constraints. See [System Definition](#system-definition).

**Step 2: Component decomposition** - Break into atomic parts using appropriate strategy. See [Component Decomposition](#component-decomposition).

**Step 3: Relationship mapping** - Map dependencies, data flow, control flow. See [Relationship Mapping](#relationship-mapping).

**Step 4: Property analysis** - Measure/estimate component properties, identify critical elements. See [Property Analysis](#property-analysis).

**Step 5: Reconstruction and recommendations** - Apply reconstruction pattern, deliver recommendations. See [Reconstruction & Recommendations](#reconstruction--recommendations).

---

## System Definition

### Input Questions

Ask user to clarify:

**1. System description:**
- What system are we analyzing? (Specific name, not vague category)
- What does it do? (Purpose, inputs, outputs)
- Current state vs desired state?

**2. Goal:**
- What problem needs solving? (Performance, cost, complexity, reliability, redesign)
- What would success look like? (Specific, measurable outcome)
- Primary objective: Optimize, simplify, understand, or redesign?

**3. Boundaries:**
- What's included in this system? (Components definitely in scope)
- What's excluded? (Adjacent systems, dependencies we won't decompose further)
- Why these boundaries? (Prevent scope creep)

**4. Constraints:**
- What can't change? (Legacy integrations, regulatory requirements, budget limits)
- Time horizon? (Quick analysis vs comprehensive redesign)
- Stakeholder priorities? (Speed vs cost vs reliability)

### System Definition Template

```markdown
## System Definition
**Name:** [Specific system name]
**Purpose:** [What it does]
**Problem:** [Current issue]
**Goal:** [Target improvement with success criteria]
**Scope:** In: [Components to decompose] | Out: [Excluded systems]
**Constraints:** [What can't change, timeline]
```

---

## Component Decomposition

### Choose Decomposition Strategy

Match strategy to system type:

**Functional Decomposition** (processes, workflows):
- Question: "What tasks does this system perform?"
- Break down by function or activity
- Example: User onboarding → Signup | Email verification | Profile setup | Tutorial

**Structural Decomposition** (architectures, organizations):
- Question: "What are the physical or logical parts?"
- Break down by component or module
- Example: Microservices app → Auth service | User service | Payment service | Notification service

**Data Flow Decomposition** (pipelines, ETL):
- Question: "How does data transform as it flows?"
- Break down by transformation or processing stage
- Example: Log processing → Collect | Parse | Filter | Aggregate | Store | Alert

**Temporal Decomposition** (sequences, journeys):
- Question: "What are the stages over time?"
- Break down by phase or time period
- Example: Sales funnel → Awareness | Consideration | Decision | Purchase | Retention

**Cost/Resource Decomposition** (budgets, capacity):
- Question: "How are resources allocated?"
- Break down by cost center or resource type
- Example: Team capacity → Development (60%) | Meetings (20%) | Support (15%) | Admin (5%)

### Decomposition Process

**Step 1: First-level decomposition**

Break system into 3-8 major components. If <3, system may be too simple for this analysis. If >8, group related items.

**Step 2: Determine decomposition depth**

For each component, ask: "Is further breakdown useful?"
- **Yes, decompose further if:**
  - Component is complex and opaque
  - Further breakdown reveals optimization opportunities
  - Component is the bottleneck or high-cost area
- **No, stop if:**
  - Component is atomic (can't meaningfully subdivide)
  - Further detail doesn't help achieve goal
  - Component is out of scope

**Step 3: Document decomposition hierarchy**

Use indentation or numbering to show levels.

### Component Decomposition Template

```markdown
## Component Breakdown

**Strategy:** [Functional / Structural / Data Flow / Temporal / Cost-Resource]

**Hierarchy:**
- **[Component A]:** [Description]
  - A.1: [Sub-component description]
  - A.2: [Sub-component description]
- **[Component B]:** [Description]
  - B.1: [Sub-component description]
- **[Component C]:** [Description - atomic]

**Depth Rationale:** [Why decomposed to this level]
```

---

## Relationship Mapping

### Relationship Types

Identify all applicable relationships:

**1. Dependency:** A requires B to function
- Example: Frontend depends on API, API depends on database
- Notation: A → B (A depends on B)

**2. Data flow:** A sends data to B
- Example: User input → Validation → Database
- Notation: A ⇒ B (data flows from A to B)

**3. Control flow:** A triggers or controls B
- Example: Payment success triggers fulfillment
- Notation: A ⊳ B (A triggers B)

**4. Temporal ordering:** A must happen before B
- Example: Authentication before authorization
- Notation: A < B (A before B in time)

**5. Resource sharing:** A and B both use C
- Example: Services share database connection pool
- Notation: A ← C → B (both use C)

### Mapping Process

**Step 1: Pairwise relationship check**

For each pair of components, ask:
- Does A depend on B?
- Does data flow from A to B?
- Does A trigger B?
- Must A happen before B?
- Do A and B share a resource?

**Step 2: Document relationships**

List all relationships with type and direction.

**Step 3: Identify critical paths**

Trace sequences of dependencies from input to output. Longest path = critical path.

### Relationship Mapping Template

```markdown
## Relationships

**Dependencies:** [A] → [B] → [C] (A requires B, B requires C)
**Data Flows:** [Input] ⇒ [Process] ⇒ [Output]
**Control Flows:** [Trigger] ⊳ [Action] ⊳ [Notification]
**Temporal:** [Step 1] < [Step 2] < [Step 3]
**Resource Sharing:** [A, B] share [Resource C]
**Critical Path:** [Start] → [A] → [B] → [C] → [End] (Total: [time/cost])
```

---

## Property Analysis

### Component Properties

For each component, measure or estimate:

**Performance properties:**
- Latency: Time to complete
- Throughput: Capacity (requests/sec, items/hour)
- Reliability: Uptime, failure rate
- Scalability: Can it handle growth?

**Cost properties:**
- Direct cost: $/month, $/transaction
- Indirect cost: Maintenance burden, technical debt
- Opportunity cost: What else could we build with these resources?

**Complexity properties:**
- Lines of code, number of dependencies, cyclomatic complexity
- Cognitive load: How hard to understand/change?
- Coupling: How tightly connected to other components?

**Other properties (domain-specific):**
- Security: Vulnerability surface
- Compliance: Regulatory requirements
- User experience: Friction points, satisfaction

### Analysis Techniques

**Measurement (objective):**
- Use profiling tools, logs, metrics dashboards
- Benchmark performance, measure latency, count resources
- Example: Database query takes 1.2s (measured via APM tool)

**Estimation (subjective):**
- When measurement isn't available, estimate with rationale
- Use comparative judgment (high/medium/low or 1-10 scale)
- Example: "Component A complexity: 8/10 because 500 LOC, 12 dependencies, no docs"

**Sensitivity analysis:**
- Identify which properties matter most for goal
- Focus measurement/estimation on critical properties

### Property Analysis Template

```markdown
## Component Properties

| Component | Latency | Cost | Complexity | Reliability | Notes |
|-----------|---------|------|------------|-------------|-------|
| [A] | 500ms | $200/mo | 5/10 | 99.9% | [Notes] |
| [B] | 1.2s | $50/mo | 8/10 | 95% | [Notes] |

**Data sources:** [Where metrics came from]

**Critical Components:** [List with impact on goal]
```

---

## Reconstruction & Recommendations

### Choose Reconstruction Pattern

Based on goal and analysis, select approach:

**Bottleneck Identification:**
- Goal: Find limiting factor
- Approach: Identify component with highest impact on goal metric
- Recommendation: Optimize the bottleneck first

**Simplification:**
- Goal: Reduce complexity
- Approach: Question necessity of each component, eliminate low-value parts
- Recommendation: Remove or consolidate components

**Reordering:**
- Goal: Improve efficiency through sequencing
- Approach: Identify independent components, move earlier or parallelize
- Recommendation: Change execution order

**Parallelization:**
- Goal: Increase throughput
- Approach: Find independent components, execute concurrently
- Recommendation: Run in parallel instead of serial

**Substitution:**
- Goal: Replace underperforming component
- Approach: Identify weak component, find better alternative
- Recommendation: Swap component

**Consolidation:**
- Goal: Reduce overhead
- Approach: Find redundant/overlapping components, merge
- Recommendation: Combine similar components

**Modularization:**
- Goal: Improve maintainability
- Approach: Identify tight coupling, separate concerns
- Recommendation: Extract into independent modules

### Recommendation Structure

Each recommendation should include:
1. **What:** Specific change to make
2. **Why:** Rationale based on analysis
3. **Expected impact:** Quantified or estimated benefit
4. **Implementation:** High-level approach or next steps
5. **Risks:** Potential downsides or considerations

### Reconstruction Template

```markdown
## Reconstruction

**Pattern:** [Bottleneck ID / Simplification / Reordering / Parallelization / Substitution / Consolidation / Modularization]

**Key Findings:**
- [Finding 1 with evidence]
- [Finding 2 with evidence]

## Recommendations

### Priority 1: [Title]
**What:** [Specific change]
**Why:** [Rationale from analysis]
**Impact:** [Quantified improvement, confidence level]
**Implementation:** [High-level approach, effort estimate]
**Risks:** [Key risks and mitigations]

### Priority 2: [Title]
[Same structure]

## Summary
**Current:** [System as analyzed]
**Proposed:** [After recommendations]
**Total Impact:** [Goal metric improvement]
**Next Steps:** [1. Immediate action, 2. Planning, 3. Execution]
```

---

## Quality Checklist

Before delivering, verify:

**Decomposition quality:**
- [ ] System boundary is clear and justified
- [ ] Components are at appropriate granularity (not too coarse, not too fine)
- [ ] Decomposition strategy matches system type
- [ ] All major components identified
- [ ] Decomposition depth is justified (why stopped where we did)

**Relationship mapping:**
- [ ] All critical relationships documented
- [ ] Relationship types are clear (dependency vs data flow vs control flow)
- [ ] Critical path identified
- [ ] Dependencies are accurate (verified with stakeholders if uncertain)

**Property analysis:**
- [ ] Key properties measured or estimated for each component
- [ ] Data sources documented (measurement vs estimation)
- [ ] Critical components identified (highest impact on goal)
- [ ] Analysis focuses on properties relevant to goal

**Reconstruction & recommendations:**
- [ ] Reconstruction pattern matches goal
- [ ] Recommendations are specific and actionable
- [ ] Expected impact is quantified or estimated
- [ ] Rationale ties back to component analysis
- [ ] Risks and considerations noted
- [ ] Prioritization is clear (Priority 1, 2, 3)

**Communication:**
- [ ] Decomposition is visualizable (hierarchy or diagram could be drawn)
- [ ] Analysis findings are clear and evidence-based
- [ ] Recommendations have clear expected impact
- [ ] Technical level appropriate for audience
- [ ] Assumptions and limitations stated

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| **Decomposition too shallow** (2-3 complex components) | Ask "can this be broken down further?" |
| **Decomposition too deep** (50+ atomic parts) | Group related components, focus on goal-relevant areas |
| **Inconsistent strategy** (mixing functional/structural) | Choose one primary strategy, stick to it |
| **Missing critical relationships** (hidden dependencies) | Trace data/control flow systematically, validate with stakeholders |
| **Unmeasured properties** (all guesses) | Prioritize measurement for critical components |
| **Vague recommendations** ("optimize X") | Specify WHAT, HOW, WHY with evidence from analysis |
| **Ignoring constraints** (impossible suggestions) | Check all recommendations against stated constraints |
| **No impact quantification** ("can't estimate improvement") | Estimate expected impact from component properties |

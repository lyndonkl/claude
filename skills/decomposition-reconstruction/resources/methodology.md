# Decomposition & Reconstruction: Advanced Methodology

## Workflow

Copy this checklist for complex decomposition scenarios:

```
Advanced Decomposition Progress:
- [ ] Step 1: Apply hierarchical decomposition techniques
- [ ] Step 2: Build and analyze dependency graphs
- [ ] Step 3: Perform critical path analysis
- [ ] Step 4: Use advanced property measurement
- [ ] Step 5: Apply optimization algorithms
```

**Step 1: Apply hierarchical decomposition techniques** - Multi-level decomposition with consistent abstraction levels. See [1. Hierarchical Decomposition](#1-hierarchical-decomposition).

**Step 2: Build and analyze dependency graphs** - Visualize and analyze component relationships. See [2. Dependency Graph Analysis](#2-dependency-graph-analysis).

**Step 3: Perform critical path analysis** - Identify bottlenecks using PERT/CPM. See [3. Critical Path Analysis](#3-critical-path-analysis).

**Step 4: Use advanced property measurement** - Rigorous measurement and statistical analysis. See [4. Advanced Property Measurement](#4-advanced-property-measurement).

**Step 5: Apply optimization algorithms** - Systematic reconstruction approaches. See [5. Optimization Algorithms](#5-optimization-algorithms).

---

## 1. Hierarchical Decomposition

### Multi-Level Decomposition Strategy

Break into levels: L0 (System) → L1 (3-7 subsystems) → L2 (3-7 components each) → L3+ (only if needed). Stop when component is atomic or further breakdown doesn't help goal.

**Abstraction consistency:** All components at same level should be at same abstraction type (e.g., all architectural components, not mixing "API Service" with "user login function").

**Template:**
```
System → Subsystem A → Component A.1, A.2, A.3
      → Subsystem B → Component B.1, B.2
      → Subsystem C → Component C.1 (atomic)
```

Document WHY decomposed to this level and WHY stopped.

---

## 2. Dependency Graph Analysis

### Building Dependency Graphs

**Nodes:** Components (from decomposition)
**Edges:** Relationships (dependency, data flow, control flow, etc.)
**Direction:** Arrow shows dependency direction (A → B means A depends on B)

**Example:**

```
Frontend → API Service → Database
               ↓
            Cache
               ↓
          Message Queue
```

### Graph Properties

**Strongly Connected Components (SCCs):** Circular dependencies (A → B → C → A). Problematic for isolation. Use Tarjan's algorithm.

**Topological Ordering:** Linear order where edges point forward (only if acyclic). Reveals safe build/deploy order.

**Critical Path:** Longest weighted path, determines minimum completion time. Bottleneck for optimization.

### Dependency Analysis

**Forward:** "If I change X, what breaks?" (BFS from X outgoing)
**Backward:** "What must work for X to function?" (BFS from X incoming)
**Transitive Reduction:** Remove redundant edges to simplify visualization.

---

## 3. Critical Path Analysis

### PERT/CPM (Program Evaluation and Review Technique / Critical Path Method)

**Use case:** System with sequential stages, need to identify time bottlenecks

**Inputs:**
- Components with estimated duration
- Dependencies between components

**Process:**

**Step 1: Build dependency graph with durations**

```
A (3h) → B (5h) → D (2h)
A (3h) → C (4h) → D (2h)
```

**Step 2: Calculate earliest start time (EST) for each component**

EST(node) = max(EST(predecessor) + duration(predecessor)) for all predecessors

**Example:**
- EST(A) = 0
- EST(B) = EST(A) + duration(A) = 0 + 3 = 3h
- EST(C) = EST(A) + duration(A) = 0 + 3 = 3h
- EST(D) = max(EST(B) + duration(B), EST(C) + duration(C)) = max(3+5, 3+4) = 8h

**Step 3: Calculate latest finish time (LFT) working backwards**

LFT(node) = min(LFT(successor) - duration(node)) for all successors

**Example (working backwards from D):**
- LFT(D) = project deadline (say 10h)
- LFT(B) = LFT(D) - duration(B) = 10 - 5 = 5h
- LFT(C) = LFT(D) - duration(C) = 10 - 4 = 6h
- LFT(A) = min(LFT(B) - duration(A), LFT(C) - duration(A)) = min(5-3, 6-3) = 2h

**Step 4: Calculate slack (float)**

Slack(node) = LFT(node) - EST(node) - duration(node)

**Example:**
- Slack(A) = 2 - 0 - 3 = -1h (on critical path, negative slack means delay)
- Slack(B) = 5 - 3 - 5 = -3h (critical)
- Slack(C) = 6 - 3 - 4 = -1h (has some float)
- Slack(D) = 10 - 8 - 2 = 0 (critical)

**Step 5: Identify critical path**

Components with zero (or minimum) slack form the critical path.

**Critical path:** A → B → D (total 10h)

**Optimization insight:** Only optimizing B will reduce total time. Optimizing C (non-critical) won't help.

### Handling Uncertainty (PERT Estimates)

When durations are uncertain, use three-point estimates:

- **Optimistic (O):** Best case
- **Most Likely (M):** Expected case
- **Pessimistic (P):** Worst case

**Expected duration:** E = (O + 4M + P) / 6

**Standard deviation:** σ = (P - O) / 6

**Example:**
- Component A: O=2h, M=3h, P=8h
- Expected: E = (2 + 4×3 + 8) / 6 = 3.67h
- Std dev: σ = (8 - 2) / 6 = 1h

**Use expected durations for critical path analysis, report confidence intervals**

---

## 4. Advanced Property Measurement

### Quantitative vs Qualitative Properties

**Quantitative (measurable):**
- Latency (ms), throughput (req/s), cost ($/month), lines of code, error rate (%)
- **Measurement:** Use APM tools, profilers, logs, benchmarks
- **Reporting:** Mean, median, p95, p99, min, max, std dev

**Qualitative (subjective):**
- Code readability, maintainability, user experience, team morale
- **Measurement:** Use rating scales (1-10), comparative ranking, surveys
- **Reporting:** Mode, distribution, outliers

### Statistical Rigor

**For quantitative measurements:**

**1. Multiple samples:** Don't rely on single measurement
- Run benchmark 10+ times, report distribution
- Example: Latency = 250ms ± 50ms (mean ± std dev, n=20)

**2. Control for confounds:** Isolate what you're measuring
- Example: Measure DB query time with same dataset, same load, same hardware

**3. Statistical significance:** Determine if difference is real or noise
- Use t-test or ANOVA to compare means
- Report p-value (p < 0.05 typically considered significant)

**For qualitative measurements:**

**1. Multiple raters:** Reduce individual bias
- Have 3+ people rate complexity independently, average scores

**2. Calibration:** Define rating scale clearly
- Example: Complexity 1="< 50 LOC, no dependencies", 10=">1000 LOC, 20+ dependencies"

**3. Inter-rater reliability:** Check if raters agree
- Calculate Cronbach's alpha or correlation coefficient

### Performance Profiling Techniques

**CPU Profiling:**
- Identify which components consume most CPU time
- Tools: perf, gprof, Chrome DevTools, Xcode Instruments

**Memory Profiling:**
- Identify which components allocate most memory or leak
- Tools: valgrind, heaptrack, Chrome DevTools, Instruments

**I/O Profiling:**
- Identify which components perform most disk/network I/O
- Tools: iotop, iostat, Network tab in DevTools

**Tracing:**
- Track execution flow through distributed systems
- Tools: OpenTelemetry, Jaeger, Zipkin, AWS X-Ray

**Result:** Component-level resource consumption data for bottleneck analysis

---

## 5. Optimization Algorithms

### Greedy Optimization

**Approach:** Optimize components in order of highest impact first

**Algorithm:**
1. Measure impact of optimizing each component (reduction in latency, cost, etc.)
2. Sort components by impact (descending)
3. Optimize highest-impact component
4. Re-measure, repeat until goal achieved or diminishing returns

**Example (latency optimization):**
- Components: A (100ms), B (500ms), C (50ms)
- Sort by impact: B (500ms), A (100ms), C (50ms)
- Optimize B first → Reduce to 200ms → Total latency improved by 300ms
- Re-measure, continue

**Advantage:** Fast, often gets 80% of benefit with 20% of effort
**Limitation:** May miss global optimum (e.g., removing B entirely better than optimizing B)

### Dynamic Programming Approach

**Approach:** Find optimal decomposition/reconstruction by exploring combinations

**Use case:** When multiple components interact, greedy may not find best solution

**Example (budget allocation):**
- Budget: $1000/month
- Components: A (improves UX, costs $400), B (reduces latency, costs $600), C (adds feature, costs $500)
- Constraint: Total cost ≤ $1000
- Goal: Maximize value

**Algorithm:**
1. Enumerate all feasible combinations: {A}, {B}, {C}, {A+B}, {A+C}, {B+C}
2. Calculate value and cost for each
3. Select combination with max value under budget constraint

**Result:** Optimal combination (may not be greedy choice)

### Constraint Satisfaction

**Approach:** Find reconstruction that satisfies all hard constraints

**Use case:** Multiple constraints (latency < 500ms AND cost < $500/month AND reliability > 99%)

**Formulation:**
- Variables: Component choices (use component A or B? Parallelize or serialize?)
- Domains: Possible values for each choice
- Constraints: Rules that must be satisfied

**Algorithm:** Backtracking search, constraint propagation
**Tools:** CSP solvers (Z3, MiniZinc)

### Sensitivity Analysis

**Goal:** Understand how sensitive reconstruction is to property estimates

**Process:**
1. Build reconstruction based on measured/estimated properties
2. Vary each property by ±X% (e.g., ±20%)
3. Re-run reconstruction
4. Identify which properties most affect outcome

**Example:**
- Baseline: Component A latency = 100ms → Optimize B
- Sensitivity: If A latency = 150ms → Optimize A instead
- **Conclusion:** Decision is sensitive to A's latency estimate, need better measurement

---

## 6. Advanced Reconstruction Patterns

### Caching & Memoization

**Pattern:** Add caching layer for frequently accessed components

**When:** Component is slow, accessed repeatedly, output deterministic

**Example:** Database query repeated 1000x/sec → Add Redis cache → 95% cache hit rate → 20× latency reduction

**Trade-offs:** Memory cost, cache invalidation complexity, eventual consistency

### Batch Processing

**Pattern:** Process items in batches instead of one-at-a-time

**When:** Per-item overhead is high, latency not critical

**Example:** Send 1000 individual emails (1s each, total 1000s) → Batch into groups of 100 → Send via batch API (10s per batch, total 100s)

**Trade-offs:** Increased latency for individual items, complexity in failure handling

### Asynchronous Processing

**Pattern:** Decouple components using message queues

**When:** Component is slow but result not needed immediately

**Example:** User uploads video → Process synchronously (60s wait) → User unhappy
**Reconstruction:** User uploads → Queue processing → User sees "processing" → Email when done

**Trade-offs:** Complexity (need queue infrastructure), eventual consistency, harder to debug

### Load Balancing & Sharding

**Pattern:** Distribute load across multiple instances of a component

**When:** Component is bottleneck, can be parallelized, load is high

**Example:** Single DB handles 10K req/s, saturated → Shard by user ID → 10 DBs each handle 1K req/s

**Trade-offs:** Operational complexity, cross-shard queries expensive, rebalancing cost

### Circuit Breaker

**Pattern:** Fail fast when dependent component is down

**When:** Component depends on unreliable external service

**Example:** API calls external service → Service is down → API waits 30s per request → API becomes slow
**Reconstruction:** Add circuit breaker → Detect failures → Stop calling for 60s → Fail fast (< 1ms)

**Trade-offs:** Reduced functionality during outage, tuning thresholds (false positives vs negatives)

---

## 7. Failure Mode & Effects Analysis (FMEA)

### FMEA Process

**Goal:** Identify weaknesses and single points of failure in decomposed system

**Process:**

**Step 1: List all components**

**Step 2: For each component, identify failure modes**
- How can this component fail? (crash, slow, wrong output, security breach)

**Step 3: For each failure mode, assess:**
- **Severity (S):** Impact if failure occurs (1-10, 10 = catastrophic)
- **Occurrence (O):** Likelihood of failure (1-10, 10 = very likely)
- **Detection (D):** Ability to detect before impact (1-10, 10 = undetectable)

**Step 4: Calculate Risk Priority Number (RPN)**
RPN = S × O × D

**Step 5: Prioritize failures by RPN, design mitigations**

### Example

| Component | Failure Mode | S | O | D | RPN | Mitigation |
|-----------|--------------|---|---|---|-----|------------|
| Database | Crashes | 9 | 2 | 1 | 18 | Add replica, automatic failover |
| Cache | Stale data | 5 | 6 | 8 | 240 | Reduce TTL, add invalidation |
| API | DDoS attack | 8 | 4 | 3 | 96 | Add rate limiting, WAF |

**Highest RPN = 240 (Cache stale data)** → Address this first

### Mitigation Strategies

**Redundancy:** Multiple instances, failover
**Monitoring:** Early detection, alerting
**Graceful degradation:** Degrade functionality instead of total failure
**Rate limiting:** Prevent overload
**Input validation:** Prevent bad data cascading
**Circuit breakers:** Fail fast when dependencies down

---

## 8. Case Study Approach

### Comparative Analysis

Compare reconstruction alternatives in table format (Latency, Cost, Time, Risk, Maintainability). Make recommendation with rationale based on trade-offs.

### Iterative Refinement

If initial decomposition doesn't reveal insights, refine: go deeper in critical areas, switch decomposition strategy, add missing relationships. Re-run analysis. Stop when further refinement doesn't change recommendations.

---

## 9. Tool-Assisted Decomposition

**Static analysis:** CLOC, SonarQube (dependency graphs, complexity metrics)
**Dynamic analysis:** Flame graphs, perf, Chrome DevTools (CPU/memory/I/O), Jaeger/Zipkin (distributed tracing)

**Workflow:** Static analysis → Dynamic measurement → Manual validation → Combine quantitative + qualitative

**Caution:** Tools miss runtime dependencies, overestimate coupling, produce overwhelming detail. Use as guide, not truth.

---

## 10. Communication & Visualization

**Diagrams:** Hierarchy trees, dependency graphs (color-code critical path), property heatmaps, before/after comparisons

**Stakeholder views:**
- Executives: 1-page summary, key findings, business impact
- Engineers: Detailed breakdown, technical rationale, implementation
- Product/Business: UX impact, cost-benefit, timeline

Adapt depth to audience expertise.

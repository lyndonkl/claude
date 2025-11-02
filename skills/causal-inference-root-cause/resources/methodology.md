# Causal Inference & Root Cause Analysis Methodology

## Root Cause Analysis Workflow

Copy this checklist and track your progress:

```
Root Cause Analysis Progress:
- [ ] Step 1: Generate hypotheses using structured techniques
- [ ] Step 2: Build causal model and distinguish cause types
- [ ] Step 3: Gather evidence and assess temporal sequence
- [ ] Step 4: Test causality with Bradford Hill criteria
- [ ] Step 5: Verify root cause and check coherence
```

**Step 1: Generate hypotheses using structured techniques**

Use 5 Whys, Fishbone diagrams, timeline analysis, or differential diagnosis to systematically generate potential causes. See [Hypothesis Generation Techniques](#hypothesis-generation-techniques) for detailed methods.

**Step 2: Build causal model and distinguish cause types**

Map causal chains to distinguish root causes from proximate causes, symptoms, and confounders. See [Causal Model Building](#causal-model-building) for cause type definitions and chain mapping.

**Step 3: Gather evidence and assess temporal sequence**

Collect evidence for each hypothesis and verify temporal relationships (cause must precede effect). See [Evidence Assessment Methods](#evidence-assessment-methods) for essential tests and evidence hierarchy.

**Step 4: Test causality with Bradford Hill criteria**

Score hypotheses using the 9 Bradford Hill criteria (strength, consistency, specificity, temporality, dose-response, plausibility, coherence, experiment, analogy). See [Bradford Hill Criteria](#bradford-hill-criteria) for scoring rubric.

**Step 5: Verify root cause and check coherence**

Ensure the identified root cause has strong evidence, fits with known facts, and addresses systemic issues. See [Quality Checklist](#quality-checklist) and [Worked Example](#worked-example-website-conversion-drop) for validation techniques.

---

## Hypothesis Generation Techniques

### 5 Whys (Trace Back to Root)

Start with the effect and ask "why" repeatedly until you reach the root cause.

**Process:**
```
Effect: {Observed problem}
Why? → {Proximate cause 1}
Why? → {Proximate cause 2}
Why? → {Intermediate cause}
Why? → {Deeper cause}
Why? → {Root cause}
```

**Example:**
```
Effect: Server crashed
Why? → Out of memory
Why? → Memory leak in new code
Why? → Connection pool not releasing connections
Why? → Error handling missing in new feature
Why? → Code review process didn't catch this edge case (ROOT CAUSE)
```

**When to stop**: When you reach a cause that, if fixed, would prevent recurrence.

**Pitfalls to avoid**:
- Stopping too early at proximate causes
- Following only one path (should explore multiple branches)
- Accepting vague answers ("because it broke")

---

### Fishbone Diagram (Categorize Causes)

Organize potential causes by category to ensure comprehensive coverage.

**Categories (6 Ms)**:
```
Methods         Machines        Materials
   |               |               |
   |               |               |
   └───────────────┴───────────────┴─────────→ Effect
   |               |               |
   |               |               |
Manpower      Measurement    Environment
```

**Adapted for software/product**:
- **People**: Skills, knowledge, communication, errors
- **Process**: Procedures, workflows, standards, review
- **Technology**: Tools, systems, infrastructure, dependencies
- **Environment**: External factors, timing, context

**Example (API outage)**:
- **People**: On-call engineer inexperienced with database
- **Process**: No rollback procedure documented
- **Technology**: Database connection pooling misconfigured
- **Environment**: Traffic spike coincided with deploy

---

### Timeline Analysis (What Changed?)

Map events leading up to effect to identify temporal correlations.

**Process**:
1. Establish baseline period (normal operation)
2. Mark when effect first observed
3. List all changes in days/hours leading up to effect
4. Identify changes that temporally precede effect

**Example**:
```
T-7 days: Normal operation (baseline)
T-3 days: Deployed new payment processor integration
T-2 days: Traffic increased 20%
T-1 day: First error logged (dismissed as fluke)
T-0 (14:00): Conversion rate dropped 30%
T+1 hour: Alert fired, investigation started
```

**Look for**: Changes, anomalies, or events right before effect (temporal precedence).

**Red flags**:
- Multiple changes at once (hard to isolate cause)
- Long lag between change and effect (harder to connect)
- No changes before effect (may be external factor or accumulated technical debt)

---

### Differential Diagnosis

List all conditions/causes that could produce the observed symptoms.

**Process**:
1. List all possible causes (be comprehensive)
2. For each cause, list symptoms it would produce
3. Compare predicted symptoms to observed symptoms
4. Eliminate causes that don't match

**Example (API returning 500 errors)**:

| Cause | Predicted Symptoms | Observed? |
|-------|-------------------|-----------|
| Code bug (logic error) | Specific endpoints fail, reproducible | ✓ Yes |
| Resource exhaustion (memory) | All endpoints slow, CPU/memory high | ✗ CPU normal |
| Dependency failure (database) | All database queries fail, connection errors | ✗ DB responsive |
| Configuration error | Service won't start or immediate failure | ✗ Started fine |
| DDoS attack | High traffic, distributed sources | ✗ Traffic normal |

**Conclusion**: Code bug most likely (matches symptoms, others ruled out).

---

## Causal Model Building

### Distinguish Cause Types

#### 1. Root Cause
- **Definition**: Fundamental underlying issue
- **Test**: If fixed, problem doesn't recur
- **Usually**: Structural, procedural, or systemic
- **Example**: "No code review process for infrastructure changes"

#### 2. Proximate Cause
- **Definition**: Immediate trigger
- **Test**: Directly precedes effect
- **Often**: Symptom of deeper root cause
- **Example**: "Deployed buggy config file"

#### 3. Contributing Factor
- **Definition**: Makes effect more likely or severe
- **Test**: Not sufficient alone, but amplifies
- **Often**: Context or conditions
- **Example**: "High traffic amplified impact of bug"

#### 4. Coincidence
- **Definition**: Happened around same time, no causal relationship
- **Test**: No mechanism, doesn't pass counterfactual
- **Example**: "Marketing campaign launched same day" (but unrelated to technical issue)

---

### Map Causal Chains

#### Linear Chain
```
Root Cause
    ↓ (mechanism)
Intermediate Cause
    ↓ (mechanism)
Proximate Cause
    ↓ (mechanism)
Observed Effect
```

**Example**:
```
No SSL cert renewal process (Root)
    ↓ (no automated reminders)
Cert expires unnoticed (Intermediate)
    ↓ (HTTPS handshake fails)
HTTPS connections fail (Proximate)
    ↓ (users can't connect)
Users can't access site (Effect)
```

#### Branching Chain (Multiple Paths)
```
        Root Cause
           ↙    ↘
    Path A      Path B
       ↓          ↓
    Effect A   Effect B
```

**Example**:
```
    Database migration error (Root)
           ↙              ↘
  Missing indexes    Schema mismatch
       ↓                    ↓
  Slow queries       Type errors
```

#### Common Cause (Confounding)
```
    Confounder (Z)
      ↙    ↘
Variable X   Variable Y
```
X and Y correlate because Z causes both, but X doesn't cause Y.

**Example**:
```
    Hot weather (Confounder)
      ↙              ↘
Ice cream sales   Drownings
```
Ice cream doesn't cause drownings; both caused by hot weather/summer season.

---

## Evidence Assessment Methods

### Essential Tests

#### 1. Temporal Sequence (Must Pass)
**Rule**: Cause MUST precede effect. If effect happened before "cause," it's not causal.

**How to verify**:
- Create detailed timeline
- Mark exact timestamps of cause and effect
- Calculate lag (effect should follow cause)

**Example**:
- Migration deployed: March 10, 2:00 PM
- Queries slowed: March 10, 2:15 PM
- ✓ Cause precedes effect by 15 minutes

#### 2. Counterfactual (Strong Evidence)
**Question**: "What would have happened without the cause?"

**How to test**:
- **Control group**: Compare cases with cause vs without
- **Rollback**: Remove cause, see if effect disappears
- **Baseline comparison**: Compare to period before cause
- **A/B test**: Random assignment of cause

**Example**:
- Hypothesis: New feature X causes conversion drop
- Test: A/B test with X enabled vs disabled
- Result: No conversion difference → X not the cause

#### 3. Mechanism (Plausibility Test)
**Question**: Can you explain HOW cause produces effect?

**Requirements**:
- Pathway from cause to effect
- Each step makes sense
- Supported by theory or evidence

**Example - Strong**:
- Cause: Increased checkout latency (5 sec)
- Mechanism: Users abandon slow pages
- Evidence: Industry data shows 7+ sec → 20% abandon
- ✓ Clear, plausible mechanism

**Example - Weak**:
- Cause: Moon phase (full moon)
- Mechanism: ??? (no plausible pathway)
- Effect: Website traffic increase
- ✗ No mechanism, likely spurious correlation

---

### Evidence Hierarchy

**Strongest Evidence** (Gold Standard):

1. **Randomized Controlled Trial (RCT)**
   - Random assignment eliminates confounding
   - Compare treatment vs control group
   - Example: A/B test with random user assignment

**Strong Evidence**:

2. **Quasi-Experiment / Natural Experiment**
   - Some random-like assignment (not perfect)
   - Example: Policy implemented in one region, not another
   - Control for confounders statistically

**Medium Evidence**:

3. **Longitudinal Study (Before/After)**
   - Track same subjects over time
   - Controls for individual differences
   - Example: Metric before and after change

4. **Well-Controlled Observational Study**
   - Statistical controls for confounders
   - Multiple variables measured
   - Example: Regression analysis with covariates

**Weak Evidence**:

5. **Cross-Sectional Correlation**
   - Single point in time
   - Can't establish temporal order
   - Example: Survey at one moment

6. **Anecdote / Single Case**
   - May not generalize
   - Many confounders
   - Example: One user complaint

**Recommendation**: For high-stakes decisions, aim for quasi-experiment or better.

---

### Bradford Hill Criteria

Nine factors that strengthen causal claims. Score each on 1-3 scale.

#### 1. Strength
**Question**: How strong is the association?

- **3**: Very strong correlation (r > 0.7, OR > 10)
- **2**: Moderate correlation (r = 0.3-0.7, OR = 2-10)
- **1**: Weak correlation (r < 0.3, OR < 2)

**Example**: 10x latency increase = strong association (3/3)

#### 2. Consistency
**Question**: Does relationship replicate across contexts?

- **3**: Always consistent (multiple studies, settings)
- **2**: Mostly consistent (some exceptions)
- **1**: Rarely consistent (contradictory results)

**Example**: Latency affects conversion on all pages, devices, countries = consistent (3/3)

#### 3. Specificity
**Question**: Is cause-effect relationship specific?

- **3**: Specific cause → specific effect
- **2**: Somewhat specific (some other effects)
- **1**: General/non-specific (cause has many effects)

**Example**: Missing index affects only queries on that table = specific (3/3)

#### 4. Temporality
**Question**: Does cause precede effect?

- **3**: Always (clear temporal sequence)
- **2**: Usually (mostly precedes)
- **1**: Unclear or reverse causation possible

**Example**: Migration (2:00 PM) before slow queries (2:15 PM) = always (3/3)

#### 5. Dose-Response
**Question**: Does more cause → more effect?

- **3**: Clear gradient (linear or monotonic)
- **2**: Some gradient (mostly true)
- **1**: No gradient (flat or random)

**Example**: Larger tables → slower queries = clear gradient (3/3)

#### 6. Plausibility
**Question**: Does mechanism make sense?

- **3**: Very plausible (well-established theory)
- **2**: Somewhat plausible (reasonable)
- **1**: Implausible (contradicts theory)

**Example**: Index scans faster than table scans = well-established (3/3)

#### 7. Coherence
**Question**: Fits with existing knowledge?

- **3**: Fits well (no contradictions)
- **2**: Somewhat fits (minor contradictions)
- **1**: Contradicts existing knowledge

**Example**: Aligns with database optimization theory = fits well (3/3)

#### 8. Experiment
**Question**: Does intervention change outcome?

- **3**: Strong experimental evidence (RCT)
- **2**: Some experimental evidence (quasi)
- **1**: No experimental evidence (observational only)

**Example**: Rollback restored performance = strong experiment (3/3)

#### 9. Analogy
**Question**: Similar cause-effect patterns exist?

- **3**: Strong analogies (many similar cases)
- **2**: Some analogies (a few similar)
- **1**: No analogies (unique case)

**Example**: Similar patterns in other databases = some analogies (2/3)

**Scoring**:
- **Total 18-27**: Strong causal evidence
- **Total 12-17**: Moderate evidence
- **Total < 12**: Weak evidence (need more investigation)

---

## Worked Example: Website Conversion Drop

### Problem

Website conversion rate dropped from 5% to 3% (40% relative drop) starting November 15th.

---

### 1. Effect Definition

**Effect**: Conversion rate dropped 40% (5% → 3%)

**Quantification**:
- Baseline: 5% (stable for 6 months prior)
- Current: 3% (observed for 2 weeks)
- Absolute drop: 2 percentage points
- Relative drop: 40%
- Impact: ~$100k/week revenue loss

**Timeline**:
- Last normal day: November 14th (5.1% conversion)
- First drop observed: November 15th (3.2% conversion)
- Ongoing: Yes (still at 3% as of November 29th)

**Impact**:
- 10,000 daily visitors
- 500 conversions → 300 conversions
- $200 average order value
- Loss: 200 conversions × $200 = $40k/day

---

### 2. Competing Hypotheses (Using Multiple Techniques)

#### Using 5 Whys:
```
Effect: Conversion dropped 40%
Why? → Users abandoning checkout
Why? → Checkout takes too long
Why? → Payment processor is slow
Why? → New processor has higher latency
Why? → Switched to cheaper processor (ROOT)
```

#### Using Fishbone Diagram:

**Technology**:
- New payment processor (Nov 10)
- New checkout UI (Nov 14)

**Process**:
- Lack of A/B testing
- No performance monitoring

**Environment**:
- Seasonal traffic shift (holiday season)

**People**:
- User behavior changes?

#### Using Timeline Analysis:
```
Nov 10: Switched to new payment processor
Nov 14: Deployed new checkout UI
Nov 15: Conversion drop observed (2:00 AM)
```

#### Competing Hypotheses Generated:

**Hypothesis 1: New checkout UI** (deployed Nov 14)
- Type: Proximate cause
- Evidence for: Timing matches (Nov 14 → Nov 15)
- Evidence against: A/B test showed no difference; Rollback didn't fix

**Hypothesis 2: Payment processor switch** (Nov 10)
- Type: Root cause candidate
- Evidence for: New processor slower (400ms vs 100ms); Timing precedes
- Evidence against: 5-day lag (why not immediate?)

**Hypothesis 3: Payment latency increase** (Nov 15)
- Type: Proximate cause/symptom
- Evidence for: Logs show 5-8 sec checkout (was 2-3 sec); User complaints
- Evidence against: None (strong evidence)

**Hypothesis 4: Seasonal traffic shift**
- Type: Confounder
- Evidence for: Holiday season
- Evidence against: Traffic composition unchanged

---

### 3. Causal Model

#### Causal Chain:
```
ROOT: Switched to cheaper payment processor (Nov 10)
    ↓ (mechanism: lower throughput processor)
INTERMEDIATE: Payment API latency under load
    ↓ (mechanism: slow API → page delays)
PROXIMATE: Checkout takes 5-8 seconds (Nov 15+)
    ↓ (mechanism: users abandon slow pages)
EFFECT: Conversion drops 40%
```

#### Why Nov 15 lag?
- Nov 10-14: Weekday traffic (low, processor handled it)
- Nov 15: Weekend traffic spike (2x normal)
- Processor couldn't handle weekend load → latency spike

#### Confounders Ruled Out:
- UI change: Rollback had no effect
- Seasonality: Traffic patterns unchanged
- Marketing: No changes

---

### 4. Evidence Assessment

**Temporal Sequence**: ✓ PASS (3/3)
- Processor switch (Nov 10) → Latency (Nov 15) → Drop (Nov 15)
- Clear precedence

**Counterfactual**: ✓ PASS (3/3)
- Test: Switched back to old processor
- Result: Conversion recovered to 4.8%
- Strong evidence

**Mechanism**: ✓ PASS (3/3)
- Slow processor (400ms) → High load → 5-8 sec checkout → User abandonment
- Industry data: 7+ sec = 20% abandon
- Clear, plausible mechanism

**Dose-Response**: ✓ PASS (3/3)
| Checkout Time | Conversion |
|---------------|------------|
| <3 sec | 5% |
| 3-5 sec | 4% |
| 5-7 sec | 3% |
| >7 sec | 2% |

Clear gradient

**Consistency**: ✓ PASS (3/3)
- All devices (mobile, desktop, tablet)
- All payment methods
- All countries
- Consistent pattern

**Bradford Hill Score: 24/27** (Very Strong)
1. Strength: 3 (40% drop)
2. Consistency: 3 (all segments)
3. Specificity: 2 (latency affects other things)
4. Temporality: 3 (clear sequence)
5. Dose-response: 3 (gradient)
6. Plausibility: 3 (well-known)
7. Coherence: 3 (fits theory)
8. Experiment: 3 (rollback test)
9. Analogy: 2 (some similar cases)

---

### 5. Conclusion

**Root Cause**: Switched to cheaper payment processor with insufficient throughput for weekend traffic.

**Confidence**: High (95%+)

**Why high confidence**:
- Perfect temporal sequence
- Strong counterfactual (rollback restored)
- Clear mechanism
- Dose-response present
- Consistent across contexts
- No confounders
- Bradford Hill 24/27

**Why root (not symptom)**:
- Processor switch is decision that created problem
- Latency is symptom of this decision
- Fixing latency alone treats symptom
- Reverting switch eliminates problem

---

### 6. Recommended Actions

**Immediate**:
1. ✓ Reverted to old processor (Nov 28)
2. Negotiate better rates with old processor

**If keeping new processor**:
1. Add caching layer (reduce latency <2 sec)
2. Implement async checkout
3. Load test at 3x peak

**Validation**:
- A/B test: Old processor vs new+caching
- Monitor: Latency p95, conversion rate
- Success: Conversion >4.5%, latency <2 sec

---

### 7. Limitations

**Data limitations**:
- No abandonment reason tracking
- Processor metrics limited (black box)

**Analysis limitations**:
- Didn't test all latency optimizations
- Small sample for some device types

**Generalizability**:
- Specific to our checkout flow
- May not apply to other traffic patterns

---

## Quality Checklist

Before finalizing root cause analysis, verify:

**Effect Definition**:
- [ ] Effect clearly described (not vague)
- [ ] Quantified with magnitude
- [ ] Timeline established (when started, duration)
- [ ] Baseline for comparison stated

**Hypothesis Generation**:
- [ ] Multiple hypotheses generated (3+ competing)
- [ ] Used systematic techniques (5 Whys, Fishbone, Timeline, Differential)
- [ ] Proximate vs root distinguished
- [ ] Confounders identified

**Causal Model**:
- [ ] Causal chain mapped (root → proximate → effect)
- [ ] Mechanisms explained for each link
- [ ] Confounding relationships noted
- [ ] Direct vs indirect causation clear

**Evidence Assessment**:
- [ ] Temporal sequence verified (cause before effect)
- [ ] Counterfactual tested (what if cause absent)
- [ ] Mechanism explained with supporting evidence
- [ ] Dose-response checked (more cause → more effect)
- [ ] Consistency assessed (holds across contexts)
- [ ] Confounders ruled out or controlled

**Conclusion**:
- [ ] Root cause clearly stated
- [ ] Confidence level stated with justification
- [ ] Distinguished from proximate causes/symptoms
- [ ] Alternative explanations acknowledged
- [ ] Limitations noted

**Recommendations**:
- [ ] Address root cause (not just symptoms)
- [ ] Actionable interventions proposed
- [ ] Validation tests specified
- [ ] Success metrics defined

**Minimum Standards**:
- For medium-stakes (postmortems, feature issues): Score ≥ 3.5 on rubric
- For high-stakes (infrastructure, safety): Score ≥ 4.0 on rubric
- Red flags: <3 on Temporal Sequence, Counterfactual, or Mechanism = weak causal claim

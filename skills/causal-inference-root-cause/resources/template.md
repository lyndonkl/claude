# Causal Inference & Root Cause Analysis Template

## Workflow

Copy this checklist and track your progress:

```
Root Cause Analysis Progress:
- [ ] Step 1: Define effect with quantification and timeline
- [ ] Step 2: Generate competing hypotheses systematically
- [ ] Step 3: Build causal model with mechanisms
- [ ] Step 4: Assess evidence using essential tests
- [ ] Step 5: Document conclusion with confidence level
```

**Step 1: Define effect with quantification and timeline**

Describe what happened specifically, quantify magnitude (baseline vs current, change), establish timeline (first observed, duration, context), and identify impact (who's affected, severity, business impact). Use [Quick Template](#quick-template) section 1.

**Step 2: Generate competing hypotheses systematically**

List 3-5 potential causes, classify each as root/proximate/symptom, note evidence for/against each hypothesis, and identify potential confounders (third factors causing both X and Y). Use techniques from [Section-by-Section Guidance](#section-by-section-guidance): 5 Whys, Fishbone Diagram, Timeline Analysis.

**Step 3: Build causal model with mechanisms**

Draw causal chain (Root → Intermediate → Proximate → Effect) with mechanisms explaining HOW each step leads to next, and rule out confounders (distinguish Z causing both X and Y from X causing Y). See [Causal Model](#3-causal-model) template structure.

**Step 4: Assess evidence using essential tests**

Check temporal sequence (cause before effect?), test counterfactual (what if cause absent?), explain mechanism (HOW does it work?), look for dose-response (more cause → more effect?), verify consistency (holds across contexts?), and control for confounding. See [Evidence Assessment](#4-evidence-assessment) and [Section-by-Section Guidance](#4-evidence-assessment-1).

**Step 5: Document conclusion with confidence level**

State root cause with confidence level (High/Medium/Low) and justification, explain complete causal mechanism, clarify why this is root (not symptom), note alternative explanations and why less likely, recommend interventions addressing root cause, propose validation tests, and acknowledge limitations. Use [Quality Checklist](#quality-checklist) to verify completeness.

## Quick Template

```markdown
# Root Cause Analysis: {Effect/Problem}

## 1. Effect Definition

**What happened**: {Clear description of the effect}

**Quantification**: {Magnitude, frequency, impact}
- Baseline: {Normal state}
- Current: {Observed state}
- Change: {Absolute and relative change}

**Timeline**:
- First observed: {Date/time}
- Duration: {Ongoing/resolved}
- Context: {What else was happening}

**Impact**:
- Who's affected: {Users, systems, metrics}
- Severity: {High/Medium/Low}
- Business impact: {Revenue, users, reputation}

---

## 2. Competing Hypotheses

Generate 3-5 potential causes systematically:

### Hypothesis 1: {Potential cause}
- **Type**: Root cause / Proximate cause / Symptom
- **Evidence for**: {Supporting data, observations}
- **Evidence against**: {Contradicting data}

### Hypothesis 2: {Potential cause}
- **Type**: Root cause / Proximate cause / Symptom
- **Evidence for**: {Supporting data}
- **Evidence against**: {Contradicting data}

### Hypothesis 3: {Potential cause}
- **Type**: Root cause / Proximate cause / Symptom
- **Evidence for**: {Supporting data}
- **Evidence against**: {Contradicting data}

**Potential confounders**: {Third factors that might cause both X and Y}

---

## 3. Causal Model

### Causal Chain (Root → Proximate → Effect)

```
{Root Cause}
    ↓ {mechanism: how does root cause lead to next step?}
{Intermediate Cause}
    ↓ {mechanism: how does this lead to proximate?}
{Proximate Cause}
    ↓ {mechanism: how does this produce observed effect?}
{Observed Effect}
```

**Mechanisms**: {Explain HOW each step leads to the next}

**Confounders ruled out**: {Z causes both X and Y, but X doesn't cause Y}

---

## 4. Evidence Assessment

### Temporal Sequence
- [ ] Does cause precede effect? {Yes/No}
- [ ] Timeline: {Cause at time T, effect at time T+lag}

### Counterfactual Test
- [ ] "What if cause hadn't occurred?" → {Expected outcome}
- [ ] Evidence: {Control group, rollback, baseline comparison}

### Mechanism
- [ ] Can we explain HOW cause produces effect? {Yes/No}
- [ ] Mechanism: {Detailed explanation with supporting evidence}

### Dose-Response
- [ ] More cause → more effect? {Yes/No/Unknown}
- [ ] Evidence: {Examples of gradient}

### Consistency
- [ ] Does relationship hold across contexts? {Yes/No}
- [ ] Evidence: {Different times, places, populations}

### Confounding Control
- [ ] Identified confounders: {List third variables}
- [ ] Controlled for: {How confounders were ruled out}

---

## 5. Conclusion

### Most Likely Root Cause

**Root cause**: {Identified root cause}

**Confidence level**: {High/Medium/Low}

**Justification**: {Why this confidence level based on evidence}

**Causal mechanism**: {Complete chain from root cause → effect}

**Why this is root cause (not symptom)**: {If fixed, problem wouldn't recur}

### Alternative Explanations

**Alternative 1**: {Other possible cause}
- Why less likely: {Evidence against}

**Alternative 2**: {Other possible cause}
- Why less likely: {Evidence against}

**Unresolved uncertainties**: {What we still don't know}

---

## 6. Recommended Actions

### Immediate Interventions (Address Root Cause)
1. {Action to eliminate root cause}
2. {Action to prevent recurrence}

### Tests to Validate Causal Claim
1. {Experiment to confirm causation}
2. {Observable prediction if theory is correct}

### Monitoring
- Metrics to track: {Key indicators}
- Expected change: {What should happen if intervention works}
- Timeline: {When to expect results}

---

## 7. Limitations

**Data limitations**: {Missing data, measurement issues}

**Analysis limitations**: {Confounders not controlled, temporal gaps, sample size}

**Generalizability**: {Does this apply beyond this specific case?}
```

---

## Section-by-Section Guidance

### 1. Effect Definition
**Goal**: Precisely specify what you're explaining
- Be specific (not "system slow" but "p95 latency 50ms → 500ms")
- Quantify magnitude and timeline
- Establish baseline for comparison

### 2. Competing Hypotheses
**Goal**: Generate multiple explanations (avoid confirmation bias)
- Use techniques: 5 Whys, Fishbone Diagram, Timeline Analysis (see `methodology.md`)
- Distinguish: Root cause (fundamental) vs Proximate cause (immediate trigger) vs Symptom
- Consider confounders (third variables causing both X and Y)

### 3. Causal Model
**Goal**: Map how causes lead to effect
- Show causal chains with mechanisms (not just correlation)
- Identify confounding relationships
- Distinguish direct vs indirect causation

### 4. Evidence Assessment
**Goal**: Test whether X truly causes Y (not just correlates)

**Essential tests:**
- **Temporal sequence**: Cause must precede effect
- **Counterfactual**: What happens when cause is absent?
- **Mechanism**: HOW does cause produce effect?

**Strengthening evidence:**
- **Dose-response**: More cause → more effect?
- **Consistency**: Holds across contexts?
- **Confounding control**: Ruled out third variables?

### 5. Conclusion
**Goal**: State root cause with justified confidence
- Distinguish root from proximate causes
- State confidence level (High/Medium/Low) with reasoning
- Acknowledge alternative explanations and limitations

### 6. Recommendations
**Goal**: Actionable interventions based on root cause
- Address root cause (not just symptoms)
- Propose tests to validate causal claim
- Define success metrics

### 7. Limitations
**Goal**: Acknowledge uncertainties and boundaries
- Missing data or measurement issues
- Confounders not fully controlled
- Scope of generalizability

---

## Quick Reference

**For detailed techniques**: See `methodology.md`
- 5 Whys (trace back to root)
- Fishbone Diagram (categorize causes)
- Timeline Analysis (what changed when?)
- Bradford Hill Criteria (9 factors for causation)
- Evidence hierarchy (RCT > longitudinal > cross-sectional)
- Confounding control methods

**For complete example**: See `examples/database-performance-degradation.md`
- Shows full analysis with all sections
- Demonstrates evidence assessment
- Includes Bradford Hill scoring

**Quality checklist**: Before finalizing, verify:
- [ ] Effect clearly defined with quantification
- [ ] Multiple hypotheses generated (3+ competing explanations)
- [ ] Root cause distinguished from proximate/symptoms
- [ ] Temporal sequence verified (cause before effect)
- [ ] Counterfactual tested (what if cause absent?)
- [ ] Mechanism explained (HOW, not just THAT)
- [ ] Confounders identified and controlled
- [ ] Confidence level stated with justification
- [ ] Alternative explanations noted
- [ ] Limitations acknowledged

---
name: causal-inference-root-cause
description: Use when investigating why something happened and need to distinguish correlation from causation, identify root causes vs symptoms, test competing hypotheses, control for confounding variables, or design experiments to validate causal claims. Invoke when debugging systems, analyzing failures, researching health outcomes, evaluating policy impacts, or when user mentions root cause, causal chain, confounding, spurious correlation, or asks "why did this really happen?"
---

# Causal Inference & Root Cause Analysis

## Table of Contents

- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [What is Causal Inference?](#what-is-causal-inference)
- [Workflow](#workflow)
  - [1. Define the Effect](#1--define-the-effect)
  - [2. Generate Hypotheses](#2--generate-hypotheses)
  - [3. Build Causal Model](#3--build-causal-model)
  - [4. Test Causality](#4--test-causality)
  - [5. Document & Validate](#5--document--validate)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Systematically investigate causal relationships to identify true root causes rather than mere correlations or symptoms. This skill helps distinguish genuine causation from spurious associations, test competing explanations, and design interventions that address underlying drivers.

## When to Use This Skill

- Investigating system failures or production incidents
- Debugging performance issues with multiple potential causes
- Analyzing why a metric changed (e.g., conversion rate drop)
- Researching health outcomes or treatment effects
- Evaluating policy or intervention impacts
- Distinguishing correlation from causation in data
- Identifying confounding variables in experiments
- Tracing symptom back to root cause
- Testing competing hypotheses about cause-effect relationships
- Designing experiments to validate causal claims
- Understanding why a project succeeded or failed
- Analyzing customer churn or retention drivers

**Trigger phrases:** "root cause", "why did this happen", "causal chain", "correlation vs causation", "confounding", "spurious correlation", "what really caused", "underlying driver"

## What is Causal Inference?

A systematic approach to determine whether X causes Y (not just correlates with Y):

- **Correlation**: X and Y move together (may be coincidental or due to third factor Z)
- **Causation**: Changing X directly causes change in Y (causal mechanism exists)

**Key Concepts:**

- **Root cause**: The fundamental issue that, if resolved, prevents the problem
- **Proximate cause**: Immediate trigger (may be symptom, not root)
- **Confounding variable**: Third factor that causes both X and Y, creating spurious correlation
- **Counterfactual**: "What would have happened without X?" - the key causal question
- **Causal mechanism**: The pathway or process through which X affects Y

**Quick Example:**

```markdown
# Effect: Website conversion rate dropped 30%

## Competing Hypotheses:
1. New checkout UI is confusing (proximate)
2. Payment processor latency increased (proximate)
3. We changed to a cheaper payment processor that's slower (root cause)

## Test:
- Rollback UI (no change) → UI not cause
- Check payment logs (confirm latency) → latency is cause
- Trace to processor change → processor change is root cause

## Counterfactual:
"If we hadn't switched processors, would conversion have dropped?"
→ No, conversion was fine with old processor

## Conclusion:
Root cause = processor switch
Mechanism = slow checkout → user abandonment
```

## Workflow

Follow these steps in order:

### 1. [ ] Define the Effect

Clearly specify what you're investigating:
- [ ] **Describe the effect/outcome**: What happened? (be specific)
- [ ] **Quantify if possible**: How big is the effect? (magnitude, frequency)
- [ ] **Establish timeline**: When did it start? Is it ongoing?
- [ ] **Determine baseline**: What's normal? What changed from before?
- [ ] **Identify stakeholders**: Who's impacted? Who needs answers?

**Key questions:**
- What exactly are we trying to explain?
- Is this a one-time event or recurring pattern?
- How do we measure this effect objectively?

### 2. [ ] Generate Hypotheses

Brainstorm potential causes systematically:
- [ ] **List proximate causes**: What are immediate triggers or symptoms?
- [ ] **Identify potential root causes**: What underlying factors could explain this?
- [ ] **Consider confounders**: What third factors might create spurious associations?
- [ ] **Challenge assumptions**: What if our initial theory is wrong?

**Techniques to generate hypotheses:**
- **5 Whys**: Ask "why" repeatedly to trace back to root
- **Fishbone diagram**: Categorize causes (people, process, technology, environment)
- **Timeline analysis**: What changed right before the effect?
- **Differential diagnosis**: What else could explain these symptoms?

**For simple investigations** → Use `resources/template.md` to structure analysis

**For complex causal problems** → Study `resources/methodology.md` for advanced techniques (confounding control, DAGs, Bradford Hill criteria)

### 3. [ ] Build Causal Model

Map how causes might lead to effect:
- [ ] **Draw causal chains**: A → B → C → Effect (mechanisms)
- [ ] **Identify necessary vs sufficient causes**: What must be present? What alone causes effect?
- [ ] **Map confounding relationships**: What influences both cause and effect?
- [ ] **Note temporal sequence**: Does cause precede effect? (necessary for causation)
- [ ] **Specify mechanisms**: HOW does X cause Y? (not just THAT it does)

**Causal model elements:**
- **Direct cause**: X → Y (X directly causes Y)
- **Indirect cause**: X → Z → Y (X causes Y through Z)
- **Confounding**: Z → X, Z → Y (Z causes both, X and Y merely correlate)
- **Mediating variable**: X → M → Y (M is the mechanism by which X causes Y)
- **Moderating variable**: X → Y depends on M (M changes strength of X → Y)

### 4. [ ] Test Causality

Evaluate evidence for each hypothesis:
- [ ] **Check temporal sequence**: Does cause precede effect? (if not, not causal)
- [ ] **Assess strength of association**: Strong correlation? (stronger = more likely causal)
- [ ] **Look for dose-response**: More cause → more effect? (gradient suggests causation)
- [ ] **Test counterfactual**: What happens when cause is absent/removed?
- [ ] **Search for mechanism**: Can you explain HOW cause produces effect?
- [ ] **Check consistency**: Does relationship hold across contexts/populations?
- [ ] **Rule out confounders**: Control for third variables that might explain both

**Evidence hierarchy (strongest to weakest):**
1. **Randomized controlled trial** (gold standard - removes confounding)
2. **Natural experiment** (quasi-random assignment)
3. **Longitudinal studies** (track changes over time)
4. **Case-control studies** (compare cases with controls)
5. **Cross-sectional studies** (snapshot correlations)
6. **Expert opinion / intuition** (weakest)

**Bradford Hill Criteria** (9 factors suggesting causation):
1. Strength (strong association)
2. Consistency (replicable)
3. Specificity (specific cause → specific effect)
4. Temporality (cause precedes effect)
5. Dose-response (more cause → more effect)
6. Plausibility (mechanism makes sense)
7. Coherence (fits with existing knowledge)
8. Experiment (intervention changes outcome)
9. Analogy (similar cause-effect patterns exist)

### 5. [ ] Document & Validate

Create output and validate quality:
- [ ] **Create** `causal-inference-root-cause.md` in current directory with:
  - Effect description and quantification
  - Competing hypotheses generated
  - Causal model (chains, confounders, mechanisms)
  - Evidence assessment for each hypothesis
  - Most likely root cause(s) with confidence level
  - Recommended tests or interventions
  - Limitations and alternative explanations
- [ ] **Validate quality** using `resources/evaluators/rubric_causal_inference_root_cause.json`

**Quality checks:**
- [ ] Distinguished proximate cause from root cause
- [ ] Identified and controlled for obvious confounders
- [ ] Explained causal mechanism (not just correlation)
- [ ] Assessed evidence systematically (not cherry-picked)
- [ ] Noted confidence level and uncertainty
- [ ] Recommended testable interventions
- [ ] Acknowledged limitations and alternative explanations

**Minimum standard**: Score ≥ 3.5 across all rubric criteria

If any criterion scores < 3, strengthen that aspect before delivering.

## Common Patterns

**For incident investigation (engineering):**
- Effect: System outage, performance degradation
- Hypotheses: Recent deploy, traffic spike, dependency failure, resource exhaustion
- Model: Timeline + dependency graph + recent changes
- Test: Logs, metrics, rollback experiments
- Output: Postmortem with root cause and prevention plan

**For metric changes (product/business):**
- Effect: Conversion drop, revenue change, user engagement shift
- Hypotheses: Product changes, seasonality, market shifts, measurement issues
- Model: User journey + external factors + recent experiments
- Test: Cohort analysis, A/B test data, segmentation
- Output: Causal explanation with recommended actions

**For policy evaluation (research/public policy):**
- Effect: Health outcome, economic indicator, social metric
- Hypotheses: Policy intervention, confounding factors, secular trends
- Model: DAG with confounders + mechanisms
- Test: Difference-in-differences, regression discontinuity, propensity matching
- Output: Causal effect estimate with confidence intervals

**For debugging (software):**
- Effect: Bug, unexpected behavior, test failure
- Hypotheses: Recent changes, edge cases, race conditions, dependency issues
- Model: Code paths + data flows + timing
- Test: Reproduce, isolate, binary search, git bisect
- Output: Bug report with root cause and fix

## Guardrails

**Do:**
- Distinguish correlation from causation explicitly
- Generate multiple competing hypotheses (not just confirm first theory)
- Map out confounding variables and control for them
- Specify causal mechanisms (HOW X causes Y)
- Test counterfactuals ("what if X hadn't happened?")
- State confidence levels and uncertainty
- Acknowledge alternative explanations
- Recommend testable interventions based on root cause

**Don't:**
- Confuse proximate cause with root cause
- Cherry-pick evidence that confirms initial hypothesis
- Assume correlation implies causation
- Ignore confounding variables
- Skip mechanism explanation (just stating correlation)
- Overstate confidence without strong evidence
- Stop at first plausible explanation without testing alternatives
- Propose interventions without identifying root cause

**Common Pitfalls:**
- **Post hoc ergo propter hoc**: "After this, therefore because of this" (temporal sequence ≠ causation)
- **Spurious correlation**: Two things correlate due to third factor or coincidence
- **Confounding**: Third variable causes both X and Y
- **Reverse causation**: Y causes X, not X causes Y
- **Selection bias**: Sample is not representative
- **Regression to mean**: Extreme values naturally move toward average

## Quick Reference

- **Template**: `resources/template.md` - Structured framework for root cause analysis
- **Methodology**: `resources/methodology.md` - Advanced techniques (DAGs, confounding control, Bradford Hill criteria)
- **Quality rubric**: `resources/evaluators/rubric_causal_inference_root_cause.json`
- **Output file**: `causal-inference-root-cause.md`
- **Key distinction**: Correlation (X and Y move together) vs. Causation (X → Y mechanism)
- **Gold standard test**: Randomized controlled trial (eliminates confounding)
- **Essential criteria**: Temporal sequence (cause before effect), mechanism (how it works), counterfactual (what if cause absent)

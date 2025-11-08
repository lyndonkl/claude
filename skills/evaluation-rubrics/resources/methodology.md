# Evaluation Rubrics Methodology

Comprehensive guidance on scale design, descriptor writing, calibration, bias mitigation, and advanced rubric design techniques.

## Workflow

```
Rubric Development Progress:
- [ ] Step 1: Define purpose and scope
- [ ] Step 2: Identify evaluation criteria
- [ ] Step 3: Design the scale
- [ ] Step 4: Write performance descriptors
- [ ] Step 5: Test and calibrate
- [ ] Step 6: Use and iterate
```

**Step 1: Define purpose and scope** → See [resources/template.md](template.md#purpose-definition-template)

**Step 2: Identify evaluation criteria** → See [resources/template.md](template.md#criteria-identification-template)

**Step 3: Design the scale** → See [1. Scale Design Principles](#1-scale-design-principles)

**Step 4: Write performance descriptors** → See [2. Descriptor Writing Techniques](#2-descriptor-writing-techniques)

**Step 5: Test and calibrate** → See [3. Calibration Techniques](#3-calibration-techniques)

**Step 6: Use and iterate** → See [4. Bias Mitigation](#4-bias-mitigation) and [6. Common Pitfalls](#6-common-pitfalls)

---

## 1. Scale Design Principles

### Choosing Appropriate Granularity

**The granularity dilemma**: Too few levels (1-3) miss meaningful distinctions; too many levels (1-10) create false precision and inconsistency.

| Factor | Favors Fewer Levels (1-3, 1-4) | Favors More Levels (1-5, 1-10) |
|--------|--------------------------------|--------------------------------|
| Evaluator expertise | Novice reviewers, unfamiliar domain | Expert reviewers, deep domain knowledge |
| Observable differences | Hard to distinguish subtle differences | Clear gradations exist |
| Stakes | High-stakes binary decisions (pass/fail) | Developmental feedback, rankings |
| Sample size | Small samples (< 20 items) | Large samples (100+, statistical analysis) |
| Time available | Quick screening, time pressure | Detailed assessment, ample time |
| Consistency priority | Inter-rater reliability critical | Differentiation more important |

**Scale characteristics** (See SKILL.md Quick Reference for detailed comparison):
- **1-3**: Fast, coarse, high reliability. Use for quick screening.
- **1-4**: Forces choice (no middle), avoids central tendency. Use when bias observed.
- **1-5**: Most common, allows neutral, good balance. General purpose.
- **1-10**: Fine gradations, statistical analysis. Use for large samples (100+), expert reviewers.
- **Qualitative** (Novice/Proficient/Expert): Intuitive for skills, growth-oriented. Educational contexts.

### Central Tendency and Response Biases

**Central tendency bias**: Reviewers avoid extremes, cluster around middle (most get 3/5).

**Causes**: Uncertainty, social pressure, lack of calibration.

**Mitigations**:
1. **Even-number scales** (1-4, 1-6) force choice above/below standard
2. **Anchor examples** at each level (what does 1 vs 5 look like?)
3. **Calibration sessions** where reviewers score same work, discuss discrepancies
4. **Forced distributions** (controversial): Require X% in each category. Use sparingly.

**Other response biases**:

- **Halo effect**: Overall impression biases individual criteria scores.
  - **Mitigation**: Vertical scoring (all work on Criterion 1, then Criterion 2), blind scoring.

- **Leniency/severity bias**: Reviewer consistently scores higher/lower than others.
  - **Mitigation**: Calibration sessions, normalization across reviewers.

- **Range restriction**: Reviewer uses only part of scale (always 3-4, never 1-2 or 5).
  - **Mitigation**: Anchor examples at extremes, forced distribution (cautiously).

### Numeric vs. Qualitative Scales

**Numeric** (1-5, 1-10): Easy to aggregate, quantitative comparison, ranking. Numbers feel precise but may be arbitrary.

**Qualitative** (Novice/Proficient/Expert, Below/Meets/Exceeds): Intuitive labels, less false precision. Harder to aggregate, ordinal only.

**Hybrid approach** (best of both): Numeric with labels (1=Poor, 2=Fair, 3=Adequate, 4=Good, 5=Excellent). Labels anchor meaning, numbers enable analysis.

**Unipolar vs. Bipolar**:
- **Unipolar**: 1 (None) → 5 (Maximum). Measures amount or quality. **Use for rubrics.**
- **Bipolar**: 1 (Strongly Disagree) → 5 (Strongly Agree), 3=Neutral. Measures agreement.

---

## 2. Descriptor Writing Techniques

### Observable, Measurable Language

**Core principle**: Two independent reviewers should score the same work consistently based on descriptors alone.

| ❌ Subjective (Avoid) | ✓ Observable (Use) |
|----------------------|-------------------|
| "Shows effort" | "Submitted 3 drafts, incorporated 80%+ of feedback" |
| "Creative" | "Uses 2+ techniques not taught, novel combination of concepts" |
| "Professional quality" | "Zero typos, consistent formatting, APA citations correct" |
| "Good understanding" | "Correctly applies 4/5 key concepts, explains mechanisms" |
| "Needs improvement" | "Contains 5+ bugs, missing 2 required features, <100ms target" |

**Test for observability**: Could two reviewers count/measure this? (Yes → observable). Does this require mind-reading? (Yes → subjective).

**Techniques**:
1. **Quantification**: "All 5 requirements met" vs. "Most requirements met"
2. **Explicit features**: "Includes abstract, intro, methods, results, discussion" vs. "Complete structure"
3. **Behavioral indicators**: "Asks clarifying questions, proposes alternatives" vs. "Critical thinking"
4. **Comparison to standards**: "WCAG AA compliant" vs. "Accessible"

### Parallel Structure Across Levels

**Parallel structure**: Each level addresses the same aspects, making differences clear.

**Example: Code Review, "Readability" criterion**

| Level | Variable Names | Comments/Docs | Code Complexity |
|-------|---------------|---------------|-----------------|
| **5** | Descriptive, domain-appropriate | Comprehensive docs, all functions commented | Simple, DRY, single responsibility |
| **3** | Mostly clear, some abbreviations | Key functions documented, some comments | Moderate complexity, some duplication |
| **1** | Cryptic abbreviations, unclear | No documentation, no comments | Highly complex, nested logic, duplication |

**Benefits**: Easy comparison (what changes 3→5?), diagnostic (pinpoint weakness), fair (same dimensions).

### Examples and Anchors at Each Level

**Anchor**: Concrete example of work at a specific level, calibrates reviewers.

**Types**:
1. **Exemplar work samples**: Actual submissions scored at each level (authentic, requires permission)
2. **Synthetic examples**: Crafted to demonstrate each level (controlled, no permission needed)
3. **Annotated excerpts**: Sections highlighting what merits that score (focused, may miss holistic quality)

**Best practices**:
- Anchor at extremes and middle (minimum: 1, 3, 5)
- Diversity of anchors (different ways to achieve a level)
- Update anchors as rubric evolves
- Make accessible to evaluators and evaluatees

### Avoiding Hidden Expectations

**Hidden expectation**: Quality dimension reviewers penalize but isn't in rubric.

**Example**: Rubric has "Technical Accuracy", "Clarity", "Practical Value". Reviewer scores down for "poor visual design" (not a criterion). **Problem**: Evaluatee had no way to know design mattered.

**Mitigation**:
1. **Comprehensive criteria**: If it matters, include it. If not in rubric, don't penalize.
2. **Criterion definitions**: Explicitly state what is/isn't included.
3. **Feedback constraints**: Suggestions outside rubric don't affect score.
4. **Rubric review**: Ask evaluatees what's missing, update accordingly.

---

## 3. Calibration Techniques

### Inter-Rater Reliability Measurement

**Inter-rater reliability (IRR)**: Degree to which independent reviewers give consistent scores.

**Target IRR thresholds**:
- <50%: Unreliable, major revision needed
- 50-70%: Marginal, refine descriptors, more calibration
- 70-85%: Good, acceptable for most uses
- >85%: Excellent, highly reliable

**Measurement methods**:

**1. Percent Agreement**
- **Calculation**: (# items where reviewers agree exactly) / (total items)
- **Pros**: Simple, intuitive. **Cons**: Inflated by chance agreement.
- **Variant: Within-1 agreement**: Scores within 1 point count as agree. Target: ≥80%.

**2. Cohen's Kappa (κ)**
- **Calculation**: (Observed agreement - Expected by chance) / (1 - Expected by chance)
- **Range**: -1 to 1 (0=chance, 1=perfect agreement)
- **Interpretation**: <0.20 Poor, 0.21-0.40 Fair, 0.41-0.60 Moderate, 0.61-0.80 Substantial, 0.81-1.00 Almost perfect
- **Pros**: Corrects for chance. **Cons**: Only 2 raters, affected by prevalence.

**3. Intraclass Correlation Coefficient (ICC)**
- **Use when**: More than 2 raters, continuous scores
- **Range**: 0 to 1. **Interpretation**: <0.50 Poor, 0.50-0.75 Moderate, 0.75-0.90 Good, >0.90 Excellent
- **Pros**: Handles multiple raters, gold standard. **Cons**: Requires statistical software.

**4. Krippendorff's Alpha**
- **Use when**: Multiple raters, missing data, various data types
- **Range**: 0 to 1. **Interpretation**: α≥0.80 acceptable, ≥0.67 tentatively acceptable
- **Pros**: Most flexible, robust to missing data. **Cons**: Less familiar.

### Calibration Session Design

**Pre-calibration**:
1. **Select 3-5 samples** spanning quality range (low, medium, high, edge cases)
2. **Independent scoring**: Each reviewer scores all samples alone, no discussion
3. **Calculate IRR**: Baseline reliability (percent agreement, Kappa)

**During calibration**:
4. **Discuss discrepancies** (focus on differences >1 point): "I scored Sample 1 as 4 because... What led you to 3?"
5. **Identify ambiguities**: Descriptor unclear? Criterion boundaries fuzzy? Missing cases?
6. **Refine rubric**: Clarify descriptors (add specificity, numbers, examples), add anchors, revise criteria
7. **Re-score**: Independently re-score same samples using refined rubric

**Post-calibration**:
8. **Calculate final IRR**: If ≥70%, proceed. If <70%, iterate (more refinement + re-calibration).
9. **Document**: Date, participants, samples, IRR metrics (before/after), rubric changes, scoring decisions
10. **Schedule ongoing calibration**: Monthly or quarterly check-ins (prevents rubric drift)

### Resolving Discrepancies

**When reviewers disagree**:

- **Option 1: Discussion to consensus**: Reviewers discuss, agree on final score. Ensures consistency but time-consuming.
- **Option 2: Averaged scores**: Mean of reviewers' scores. Fast but can mask disagreement (4+2=3).
- **Option 3: Third reviewer**: If A and B differ by >1, C scores as tie-breaker. Resolves impasse but requires extra reviewer.
- **Option 4: Escalation**: Discrepancies >1 escalated to lead reviewer or committee. Quality control but bottleneck.

**Recommended**: Average for small discrepancies (1 point), discussion for large (2+ points), escalate if unresolved.

---

## 4. Bias Mitigation

### Halo Effect

**Halo effect**: Overall impression biases individual criterion scores. "Excellent work" → all criteria high, or "poor work" → all low.

**Example**: Code has excellent documentation (5/5) but poor performance (should be 2/5). Halo: Reviewer scores performance 4/5 due to overall positive impression.

**Mitigation**:
1. **Vertical scoring**: Score all submissions on Criterion 1, then all on Criterion 2 (focus on one criterion at a time)
2. **Blind scoring**: Reviewers don't see previous scores when scoring new criterion
3. **Separate passes**: First pass for overall sense (don't score), second pass to score each criterion
4. **Criterion definitions**: Clear, narrow definitions reduce bleed-over

### Anchoring and Order Effects

**Anchoring**: First information biases subsequent judgments. First essay scored 5/5 → second (objectively 4/5) feels worse → scored 3/5.

**Mitigation**:
1. **Randomize order**: Review in random order, not alphabetical or submission time
2. **Calibration anchors**: Review rubric and anchors before scoring (resets mental baseline)
3. **Batch scoring**: Score all on one criterion at once (easier to compare)

**Order effects**: Position in sequence affects score (first/last reviewed scored differently).

**Mitigation**: Multiple reviewers score in different random orders (order effect averages out).

### Leniency and Severity Bias

**Leniency**: Reviewer consistently scores higher than others (generous). **Severity**: Consistently scores lower (harsh).

**Detection**: Calculate mean score per reviewer. If Reviewer A averages 4.2 and Reviewer B averages 2.8 on same work → bias present.

**Mitigation**:
1. **Calibration sessions**: Show reviewers their bias, discuss differences
2. **Normalization** (controversial): Convert to z-scores (adjust for reviewer's mean). Changes scores, may feel unfair.
3. **Multiple reviewers**: Average scores (bias cancels out)
4. **Threshold-based**: Focus on "meets standard" (yes/no) vs numeric score

---

## 5. Advanced Rubric Design

### Weighted Criteria

**Weighting approaches**:

**1. Multiplicative weights**:
- Score × weight, sum weighted scores, divide by sum of weights
- Example: Security (4×3=12), Performance (3×2=6), Style (5×1=5). Total: 23/6 = 3.83

**2. Percentage weights**:
- Assign % to each criterion (sum to 100%)
- Example: Security 4×50%=2.0, Performance 3×30%=0.9, Style 5×20%=1.0. Total: 3.9/5.0

**When to weight**: Criteria have different importance, regulatory/compliance criteria, developmental priorities.

**Cautions**: Adds complexity, can obscure deficiencies (low critical score hidden in average). Alternative: Threshold scoring.

### Threshold Scoring

**Threshold**: Minimum score required on specific criteria regardless of overall average.

**Example**:
- Overall average ≥3.0 to pass
- **AND** Security ≥4.0 (critical threshold)
- **AND** No criterion <2.0 (floor threshold)

**Benefits**: Ensures critical criteria meet standard, prevents "compensation" (high Style masking low Security), clear requirements.

**Use cases**: Safety-critical systems, compliance requirements, competency gatekeeping.

### Combination Rubrics

**Hybrid approaches**:

- **Analytic + Holistic**: Analytic for diagnostic detail, holistic for overall judgment. Use when want both.
- **Checklist + Rubric**: Checklist for must-haves (gatekeeping), rubric for quality gradations (among passing). Use for gatekeeping then ranking.
- **Self-Assessment + Peer + Instructor**: Same rubric used by student, peers, instructor. Compare scores, discuss. Use for metacognitive learning.

---

## 6. Common Pitfalls

### Overlapping Criteria

**Problem**: Criteria not distinct, same dimension scored multiple times.

**Example**: "Organization" (structure, flow, coherence) + "Clarity" (easy to understand, well-structured, logical). **Overlap**: "well-structured" in both.

**Detection**: High correlation between criteria scores. Difficulty explaining difference.

**Fix**: Define boundaries explicitly ("Organization = structure. Clarity = language."), combine overlapping criteria, or split into finer-grained distinct criteria.

### Rubric Drift

**Problem**: Over time, reviewers interpret descriptors differently, rubric meaning changes.

**Causes**: No ongoing calibration, staff turnover, system changes.

**Detection**: IRR declines (was 80%, now 60%), scores inflate/deflate (average was 3.5, now 4.2 with no quality change), inconsistency complaints.

**Prevention**:
1. **Periodic calibration**: Quarterly sessions even with experienced reviewers
2. **Anchor examples**: Maintain library, use same anchors over time
3. **Documentation**: Record scoring decisions, accessible to new reviewers
4. **Version control**: Date rubric versions, note changes, communicate updates

### False Precision

**Problem**: Numeric scores imply precision that doesn't exist. 10-point scale but difference between 7 vs 8 arbitrary.

**Fix**:
- Reduce granularity (10→5 or 3 categories)
- Add descriptors for each level
- Report confidence intervals (Score = 3.5 ± 0.5)
- Be transparent: "Scores are informed judgments, not objective measurements"

### No Consequences for Ignoring Rubric

**Problem**: Rubric exists but reviewers don't use it or override scores based on gut feeling. Rubric becomes meaningless.

**Fix**:
1. **Require justification**: Reviewers must cite rubric descriptors when scoring
2. **Audit scores**: Spot-check scores against rubric, challenge unjustified deviations
3. **Training**: Emphasize rubric as contract (if wrong, change rubric, don't ignore)
4. **Accountability**: Reviewers who consistently deviate lose review privileges

---

## Summary

**Scale design**: Choose granularity matching observable differences. Mitigate central tendency with even-number scales or anchors.

**Descriptor writing**: Use observable language, parallel structure, examples at each level. Test: Can two reviewers score consistently?

**Calibration**: Measure IRR (Kappa, ICC), conduct calibration sessions, refine rubric, prevent drift with ongoing calibration.

**Bias mitigation**: Vertical scoring for halo effect, randomize order for anchoring, normalize or average for leniency/severity.

**Advanced design**: Weight critical criteria, use thresholds to prevent compensation, combine rubric types.

**Pitfalls**: Define distinct criteria, prevent drift with documentation and re-calibration, avoid false precision, ensure rubric has teeth.

**Final principle**: Rubrics structure judgment, not replace it. Use to increase consistency and transparency, not mechanize evaluation.

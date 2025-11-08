# Evaluation Rubrics Templates

Quick-start templates for purpose definition, criteria selection, scale design, descriptor writing, and rubric formats.

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

**Step 1: Define purpose and scope**

Use [Purpose Definition Template](#purpose-definition-template) to clarify evaluation context and constraints.

**Step 2: Identify evaluation criteria**

Brainstorm and prioritize quality dimensions using [Criteria Identification Template](#criteria-identification-template).

**Step 3: Design the scale**

Select scale type and levels using [Scale Selection Template](#scale-selection-template).

**Step 4: Write performance descriptors**

Write clear, observable descriptors using [Descriptor Writing Template](#descriptor-writing-template).

**Step 5: Test and calibrate**

Conduct inter-rater reliability testing and refine rubric.

**Step 6: Use and iterate**

Apply rubric, collect feedback, revise as needed.

---

## Purpose Definition Template

**What are we evaluating?**
- Artifact type: [e.g., code pull requests, research proposals, design mockups, student essays]
- Specific context: [e.g., internal code review, grant competition, course assignment]

**Who will evaluate?**
- Number of evaluators: [Single reviewer or multiple?]
- Evaluator expertise: [Subject matter experts, peers, instructors, automated systems]
- Evaluator availability: [Time per evaluation? Total volume?]

**Who are the evaluatees?**
- Audience: [Students, employees, vendors, applicants]
- Skill level: [Novice, intermediate, expert]
- Will they see rubric before evaluation? [Yes/No - if yes, rubric serves as guide]

**What decisions depend on scores?**
- High stakes: [Pass/fail, hiring, funding, promotion, grades]
- Medium stakes: [Feedback for improvement, prioritization, awards]
- Low stakes: [Self-assessment, informal feedback]

**Success criteria for rubric:**
- [ ] Enables consistent scoring across evaluators (inter-rater reliability >70%)
- [ ] Provides actionable feedback for improvement
- [ ] Takes reasonable time to use (target: X minutes per evaluation)
- [ ] Acceptable to evaluators (not overly complex or rigid)
- [ ] Acceptable to evaluatees (perceived as fair and transparent)

---

## Criteria Identification Template

### Brainstorming Quality Dimensions

**Product criteria** (artifact itself):
- Correctness/Accuracy: [Is it right? Factually accurate? Meets requirements?]
- Completeness: [Covers all necessary elements? No major gaps?]
- Clarity: [Easy to understand? Well-organized? Clear communication?]
- Quality/Craftsmanship: [Attention to detail? Polished? Professional?]
- Originality/Creativity: [Novel approach? Innovative? Goes beyond expected?]
- Performance: [Fast? Efficient? Scalable? Meets technical specs?]

**Process criteria** (how it was made):
- Methodology: [Followed appropriate process? Research methods sound?]
- Collaboration: [Teamwork? Communication? Used feedback?]
- Iteration: [Multiple drafts? Refinement? Responsiveness to critique?]
- Time management: [Completed on time? Paced work appropriately?]

**Impact criteria** (effects/outcomes):
- Usability: [User-friendly? Accessible? Intuitive?]
- Value: [Solves problem? Addresses need? Business impact?]
- Learning demonstrated: [Shows understanding? Growth from previous work?]

**Meta criteria** (quality of quality):
- Maintainability: [Can others work with this? Documented? Modular?]
- Testability: [Can be verified? Validated? Measured?]
- Extensibility: [Can be built upon? Flexible? Adaptable?]

### Prioritization

**Rate each candidate criterion:**

| Criterion | Importance (H/M/L) | Observable (Y/N) | Distinct from others (Y/N) | Include? |
|-----------|-------------------|------------------|---------------------------|----------|
| [Criterion 1] | | | | |
| [Criterion 2] | | | | |
| [Criterion 3] | | | | |

**Selection rules:**
- Must be High or Medium importance
- Must be Observable (can two reviewers score consistently?)
- Must be Distinct (not overlapping with other criteria)
- Aim for 4-8 criteria (balance coverage vs. simplicity)

**Final criteria** (4-8 selected):
1. [Criterion]: [Brief definition]
2. [Criterion]: [Brief definition]
3. [Criterion]: [Brief definition]
4. [Criterion]: [Brief definition]

---

## Scale Selection Template

**Scale type options:**

### Numeric Scales

**1-3 scale** (Low/Medium/High)
- Use when: Quick categorization, clear tiers sufficient
- Levels: 1=Below standard, 2=Meets standard, 3=Exceeds standard

**1-4 scale** (Forced choice, no middle)
- Use when: Want to avoid central tendency, need clear differentiation
- Levels: 1=Poor, 2=Fair, 3=Good, 4=Excellent

**1-5 scale** (Most common, allows neutral)
- Use when: General purpose, familiar to evaluators
- Levels: 1=Poor, 2=Fair, 3=Adequate, 4=Good, 5=Excellent

**1-10 scale** (Fine gradations)
- Use when: Large sample, need statistical analysis, can distinguish subtle differences
- Levels: 1-2=Poor, 3-4=Fair, 5-6=Adequate, 7-8=Good, 9-10=Excellent

### Qualitative Scales

**Developmental**: Novice → Developing → Proficient → Expert
**Standards-based**: Below Standard → Approaching → Meets → Exceeds
**Competency**: Not Yet Competent → Partially Competent → Competent → Highly Competent

### Binary

**Pass/Fail, Yes/No, Present/Absent**
- Use when: Compliance checks, minimum thresholds, clear criteria

**Selected scale for this rubric**: [Choose one]
- **Type**: [Numeric 1-5, Qualitative, etc.]
- **Levels**: [List with labels]
- **Rationale**: [Why this scale fits purpose]

---

## Descriptor Writing Template

For each criterion, write descriptors at each scale level.

### Criterion: [Name]

**Definition**: [What does this criterion assess? 1-2 sentences]

**Why it matters**: [Importance to overall quality]

**Scale descriptors:**

#### Level 5 (or highest): [Label]
**Observable characteristics**:
- [Concrete, observable feature 1]
- [Concrete, observable feature 2]
- [Concrete, observable feature 3]

**Example**: [Specific instance of work at this level]

#### Level 4: [Label]
**Observable characteristics**:
- [How this differs from Level 5 - what's missing or less strong]
- [Concrete observable feature]

**Example**: [Specific instance]

#### Level 3: [Label] (Baseline/Adequate)
**Observable characteristics**:
- [Minimum acceptable performance]
- [Observable feature]

**Example**: [Specific instance]

#### Level 2: [Label]
**Observable characteristics**:
- [What's lacking compared to Level 3]
- [Observable deficiency]

**Example**: [Specific instance]

#### Level 1 (or lowest): [Label]
**Observable characteristics**:
- [Significant deficiencies]
- [Observable problems]

**Example**: [Specific instance]

---

### Descriptor Writing Guidelines

**DO:**
- Use observable, measurable language ("Contains 3+ bugs" not "poor quality")
- Provide concrete examples or anchors for each level
- Focus on what IS present at each level, not just "less than" higher level
- Use parallel structure across levels (same aspects addressed at each level)
- Specify quantities when possible ("All 5 requirements met" vs "Most requirements met")

**DON'T:**
- Use subjective terms without definition ("creative", "professional", "excellent effort")
- Rely on comparative language only ("better than", "more sophisticated")
- Make assumptions about process ("spent time", "worked hard" - unless observable)
- Penalize for things not mentioned in descriptor (hidden expectations)

---

## Analytic Rubric Template

Most common format: Multiple criteria (rows) × Multiple levels (columns)

### Rubric for: [Artifact Type]

**Purpose**: [Brief description]

**Scale**: [1-5, 1-4, etc. with labels]

| Criterion | 1 | 2 | 3 | 4 | 5 | Weight |
|-----------|---|---|---|---|---|--------|
| **[Criterion 1]** | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] | [×N or %] |
| **[Criterion 2]** | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] | [×N or %] |
| **[Criterion 3]** | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] | [×N or %] |
| **[Criterion 4]** | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] | [Descriptor] | [×N or %] |

**Scoring:**
- Calculate: (Score1 × Weight1) + (Score2 × Weight2) + ... / Total Weights
- Threshold: [e.g., Must average ≥3.0 to pass, ≥4 on critical criteria]

**Usage notes:**
- Score each criterion independently before looking at others (avoid halo effect)
- Provide brief justification for each score
- Flag areas for improvement in feedback

---

## Holistic Rubric Template

Single overall score integrating multiple criteria.

### Rubric for: [Artifact Type]

**Purpose**: [Brief description]

#### Level 5: Excellent
**Overall quality**: [Integrated description touching all important aspects]
- Criterion A: [How it manifests at this level]
- Criterion B: [How it manifests at this level]
- Criterion C: [How it manifests at this level]

**Example**: [Work that exemplifies this level]

#### Level 4: Good
**Overall quality**: [Integrated description]
- Differences from Level 5: [What's less strong]
- Key characteristics: [Observable features]

**Example**: [Work that exemplifies this level]

#### Level 3: Adequate
**Overall quality**: [Integrated description of baseline acceptable]
- Meets minimum standards: [What's required]
- May have: [Acceptable weaknesses]

**Example**: [Work that exemplifies this level]

#### Level 2: Weak
**Overall quality**: [Integrated description of below standard]
- Falls short because: [Key deficiencies]
- Problems include: [Observable issues]

**Example**: [Work that exemplifies this level]

#### Level 1: Poor
**Overall quality**: [Integrated description of unacceptable]
- Major problems: [Significant deficiencies across multiple aspects]

**Example**: [Work that exemplifies this level]

---

## Single-Point Rubric Template

Lists criteria with "meets standard" description only, space to note exceeds/below.

### Rubric for: [Artifact Type]

| Criterion | Concerns (Below Standard) | Meets Standard | Advanced (Exceeds Standard) |
|-----------|---------------------------|----------------|----------------------------|
| **[Criterion 1]** | | [Clear description of standard] | |
| **[Criterion 2]** | | [Clear description of standard] | |
| **[Criterion 3]** | | [Clear description of standard] | |
| **[Criterion 4]** | | [Clear description of standard] | |

**Usage:**
- Check if work meets standard for each criterion
- Note specific strengths in "Advanced" column (e.g., "+Exceptionally clear examples")
- Note specific areas for improvement in "Concerns" column (e.g., "-Missing citations for 3 claims")

---

## Checklist Template

Binary yes/no for must-have requirements.

### Checklist for: [Artifact Type]

#### Category 1: [e.g., Completeness]
- [ ] [Specific requirement 1]
- [ ] [Specific requirement 2]
- [ ] [Specific requirement 3]

#### Category 2: [e.g., Quality]
- [ ] [Specific requirement 4]
- [ ] [Specific requirement 5]

#### Category 3: [e.g., Compliance]
- [ ] [Specific requirement 6]
- [ ] [Specific requirement 7]

**Pass/Fail Criteria:**
- **Pass**: All items checked OR All items in critical categories + X% of others
- **Fail**: Any critical item unchecked OR <Y% total items checked

---

## Weighted Scoring Template

When criteria have different importance.

### Weighted Rubric for: [Artifact Type]

| Criterion | Score (1-5) | Weight | Weighted Score |
|-----------|-------------|--------|----------------|
| [Criterion 1] | | ×3 (Critical) | Score × 3 = |
| [Criterion 2] | | ×2 (Important) | Score × 2 = |
| [Criterion 3] | | ×2 (Important) | Score × 2 = |
| [Criterion 4] | | ×1 (Desirable) | Score × 1 = |
| **Total** | | **8** | **[Sum] / 8 =** |

**Weight categories:**
- ×3 = Critical (must be strong, threshold: ≥4 required)
- ×2 = Important (significant impact on overall quality)
- ×1 = Desirable (nice to have, less critical)

---

## Calibration Session Template

**Pre-calibration:**
1. Select 3-5 sample works spanning quality range (low, medium, high)
2. Have each reviewer independently score samples using rubric
3. Record scores without discussion

**During calibration:**
4. Compare scores across reviewers for each sample
5. For discrepancies (>1 point difference):
   - Discuss what each reviewer saw
   - Identify ambiguous descriptors
   - Clarify criterion boundaries
   - Refine rubric language
6. Re-score samples using refined rubric

**Post-calibration:**
7. Calculate inter-rater reliability (% agreement, Kappa)
8. Target: ≥70% agreement (within 1 point) or Kappa ≥0.6
9. If below target: Iterate with more refinement + calibration
10. Document calibration decisions and rubric changes

---

## Feedback Template

**For: [Evaluatee Name]**

**Overall Score**: [X.X / 5.0 or Level]

**Criterion-by-Criterion Scores:**

| Criterion | Score | Feedback |
|-----------|-------|----------|
| [Criterion 1] | X/5 | **Strengths**: [What was done well]<br>**Areas for improvement**: [Specific suggestions] |
| [Criterion 2] | X/5 | **Strengths**: [What was done well]<br>**Areas for improvement**: [Specific suggestions] |
| [Criterion 3] | X/5 | **Strengths**: [What was done well]<br>**Areas for improvement**: [Specific suggestions] |

**Summary:**
- **Greatest strengths**: [2-3 specific strengths]
- **Priority improvements**: [2-3 most important areas to address]
- **Next steps**: [Actionable recommendations]

**Overall assessment**: [Pass/Fail or qualitative judgment]

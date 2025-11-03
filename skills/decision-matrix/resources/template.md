# Decision Matrix Template

## Workflow

Copy this checklist and track your progress:

```
Decision Matrix Progress:
- [ ] Step 1: Frame the decision
- [ ] Step 2: Identify criteria and assign weights
- [ ] Step 3: Score alternatives
- [ ] Step 4: Calculate and analyze results
- [ ] Step 5: Validate and deliver
```

**Step 1: Frame the decision** - Clarify decision context, list alternatives, identify must-haves. See [Decision Framing](#decision-framing).

**Step 2: Identify criteria and assign weights** - Determine what factors matter, assign percentage weights. See [Criteria Identification](#criteria-identification) and [Weighting Techniques](#weighting-techniques).

**Step 3: Score alternatives** - Rate each option on each criterion (1-10 scale). See [Scoring Guidance](#scoring-guidance).

**Step 4: Calculate and analyze results** - Compute weighted scores, rank options, check sensitivity. See [Matrix Calculation](#matrix-calculation) and [Interpretation](#interpretation).

**Step 5: Validate and deliver** - Quality check against [Quality Checklist](#quality-checklist), deliver with recommendation.

---

## Decision Framing

### Input Questions

Ask user to clarify:

**1. Decision context:**
- What are we deciding? (Be specific: "Choose CRM platform" not "improve sales")
- Why now? (Triggering event, deadline, opportunity)
- What happens if we don't decide or choose wrong?

**2. Alternatives:**
- What are ALL the options we're considering? (Get exhaustive list)
- Include "do nothing" or status quo as an option if relevant
- Are these mutually exclusive or can we combine them?

**3. Must-have requirements (filters):**
- Are there absolute dealbreakers? (Budget cap, compliance requirement, technical constraint)
- Which options fail must-haves and can be eliminated immediately?
- Distinguish between "must have" (filter) and "nice to have" (criterion)

**4. Stakeholders:**
- Who needs to agree with this decision?
- Who will be affected by it?
- Do different stakeholders have different priorities?

### Framing Template

```markdown
## Decision Context
- **Decision:** [Specific choice to be made]
- **Timeline:** [When decision needed by]
- **Stakeholders:** [Who needs to agree]
- **Consequences of wrong choice:** [What we risk]

## Alternatives
1. [Option A name]
2. [Option B name]
3. [Option C name]
4. [Option D name - if applicable]
5. [Do nothing / Status quo - if applicable]

## Must-Have Requirements (Pass/Fail)
- [ ] [Requirement 1] - All options must meet this
- [ ] [Requirement 2] - Eliminates options that don't pass
- [ ] [Requirement 3] - Non-negotiable constraint

**Options eliminated:** [List any that fail must-haves]
**Remaining options:** [List that pass filters]
```

---

## Criteria Identification

### Process

**Step 1: Brainstorm factors**

Ask: "What makes one option better than another?"

Common categories:
- **Cost:** Upfront, ongoing, total cost of ownership
- **Performance:** Speed, quality, reliability, scalability
- **Risk:** Implementation risk, reversibility, vendor lock-in
- **Strategic:** Alignment with goals, competitive advantage, future flexibility
- **Operational:** Ease of use, maintenance, training, support
- **Stakeholder:** Team preference, customer impact, executive buy-in

**Step 2: Validate criteria**

Each criterion should be:
- [ ] **Measurable or scorable** (can assign 1-10 rating)
- [ ] **Differentiating** (options vary on this dimension)
- [ ] **Relevant** (actually matters for this decision)
- [ ] **Independent** (not redundant with other criteria)

**Remove:**
- Criteria where all options score the same (no differentiation)
- Duplicate criteria that measure same thing
- Criteria that should be must-haves (pass/fail, not scored)

**Step 3: Keep list manageable**

- **Ideal:** 4-7 criteria (enough to capture trade-offs, not overwhelming)
- **Minimum:** 3 criteria (otherwise too simplistic)
- **Maximum:** 10 criteria (beyond this, hard to weight meaningfully)

If you have >10 criteria, group related ones into categories with sub-criteria.

### Criteria Template

```markdown
## Evaluation Criteria

| # | Criterion | Definition | How We'll Measure |
|---|-----------|------------|-------------------|
| 1 | [Name] | [What this measures] | [Data source or scoring approach] |
| 2 | [Name] | [What this measures] | [Data source or scoring approach] |
| 3 | [Name] | [What this measures] | [Data source or scoring approach] |
| 4 | [Name] | [What this measures] | [Data source or scoring approach] |
| 5 | [Name] | [What this measures] | [Data source or scoring approach] |
```

---

## Weighting Techniques

### Technique 1: Direct Allocation (Fastest)
Solo decision or aligned stakeholders. Assign percentages summing to 100%. Start with most important (30-50%), avoid weights <5%, round to 5% increments.

**Example:** Cost 30%, Performance 25%, Ease of use 20%, Risk 15%, Team preference 10% = 100%

### Technique 2: Pairwise Comparison (Most Rigorous)
Difficult to weight directly or need justification. Compare each pair ("Is A more important than B?"), tally wins, convert to percentages.

**Example:** Cost vs Performance → Performance wins. After all pairs, Performance has 4 wins (40%), Cost has 2 wins (20%), etc.

### Technique 3: Stakeholder Averaging (Group Decisions)
Multiple stakeholders with different priorities. Each assigns weights independently, then average. Large variance reveals disagreement → discuss before proceeding.

**Example:** If stakeholders assign Cost weights of 40%, 20%, 30% → Average is 30%, but variance suggests need for alignment discussion.

---

## Scoring Guidance

### Scoring Scale

**Use 1-10 scale** (better granularity than 1-5):

- **10:** Exceptional, best-in-class
- **8-9:** Very good, exceeds requirements
- **6-7:** Good, meets requirements
- **4-5:** Acceptable, meets minimum
- **2-3:** Poor, below requirements
- **1:** Fails, unacceptable

**Consistency tips:**
- Define what 10 means for each criterion before scoring
- Score all options on one criterion at a time (easier to compare)
- Use half-points (7.5) if needed for precision

### Scoring Process

**For objective criteria (cost, speed, measurable metrics):**

1. Get actual data (quotes, benchmarks, measurements)
2. Convert to 1-10 scale using formula:
   - **Lower is better** (cost, time): Score = 10 × (Best value / This value)
   - **Higher is better** (performance, capacity): Score = 10 × (This value / Best value)

**Example (Cost - lower is better):**
- Option A: $50K → Score = 10 × ($30K / $50K) = 6.0
- Option B: $30K → Score = 10 × ($30K / $30K) = 10.0
- Option C: $40K → Score = 10 × ($30K / $40K) = 7.5

**For subjective criteria (ease of use, team preference):**

1. Define what 10, 7, and 4 look like for this criterion
2. Score relative to those anchors
3. Document reasoning/assumptions

**Example (Ease of Use):**
- 10 = No training needed, intuitive UI, users productive day 1
- 7 = 1-week training, moderate learning curve
- 4 = Significant training (1 month), complex UI

**Calibration questions:**
- Would I bet money on this score being accurate?
- Is this score relative to alternatives or absolute?
- What would change this score by ±2 points?

### Scoring Template

```markdown
## Scoring Matrix

| Option | Criterion 1 (Weight%) | Criterion 2 (Weight%) | Criterion 3 (Weight%) | Criterion 4 (Weight%) |
|--------|-----------------------|-----------------------|-----------------------|-----------------------|
| Option A | [Score] | [Score] | [Score] | [Score] |
| Option B | [Score] | [Score] | [Score] | [Score] |
| Option C | [Score] | [Score] | [Score] | [Score] |

**Data sources and assumptions:**
- Criterion 1: [Where scores came from, what assumptions]
- Criterion 2: [Where scores came from, what assumptions]
- Criterion 3: [Where scores came from, what assumptions]
- Criterion 4: [Where scores came from, what assumptions]
```

---

## Matrix Calculation

### Calculation Process

**For each option:**
1. Multiply criterion score by criterion weight
2. Sum all weighted scores
3. This is the option's total score

**Formula:** Total Score = Σ (Criterion Score × Criterion Weight)

**Example:**

| Option | Cost (30%) | Performance (40%) | Risk (20%) | Ease (10%) | **Total** |
|--------|-----------|------------------|-----------|-----------|---------|
| Option A | 7 × 0.30 = 2.1 | 9 × 0.40 = 3.6 | 6 × 0.20 = 1.2 | 8 × 0.10 = 0.8 | **7.7** |
| Option B | 9 × 0.30 = 2.7 | 6 × 0.40 = 2.4 | 8 × 0.20 = 1.6 | 6 × 0.10 = 0.6 | **7.3** |
| Option C | 5 × 0.30 = 1.5 | 8 × 0.40 = 3.2 | 7 × 0.20 = 1.4 | 9 × 0.10 = 0.9 | **7.0** |

**Winner: Option A (7.7)**

### Final Matrix Template

```markdown
## Decision Matrix Results

| Option | [Criterion 1] ([W1]%) | [Criterion 2] ([W2]%) | [Criterion 3] ([W3]%) | [Criterion 4] ([W4]%) | **Weighted Total** | **Rank** |
|--------|----------------------|----------------------|----------------------|----------------------|-------------------|----------|
| [Option A] | [S] ([S×W1]) | [S] ([S×W2]) | [S] ([S×W3]) | [S] ([S×W4]) | **[Total]** | [Rank] |
| [Option B] | [S] ([S×W1]) | [S] ([S×W2]) | [S] ([S×W3]) | [S] ([S×W4]) | **[Total]** | [Rank] |
| [Option C] | [S] ([S×W1]) | [S] ([S×W2]) | [S] ([S×W3]) | [S] ([S×W4]) | **[Total]** | [Rank] |

**Weights:** [Criterion 1] ([W1]%), [Criterion 2] ([W2]%), [Criterion 3] ([W3]%), [Criterion 4] ([W4]%)

**Scoring scale:** 1-10 (10 = best)
```

---

## Interpretation

### Analysis Checklist

After calculating scores, analyze:

**1. Clear winner vs close call**
- [ ] **Margin >10%:** Clear winner, decision is robust
- [ ] **Margin 5-10%:** Moderate confidence, validate assumptions
- [ ] **Margin <5%:** Toss-up, need more data or stakeholder discussion

**2. Dominant criterion check**
- [ ] Does one criterion drive entire decision? (accounts for >50% of score difference)
- [ ] Is that appropriate or is weight too high?

**3. Surprising results**
- [ ] Does the winner match gut instinct?
- [ ] If not, what does the matrix reveal? (Trade-off you hadn't considered)
- [ ] Or are weights/scores wrong?

**4. Sensitivity questions**
- [ ] If we swapped top two criterion weights, would winner change?
- [ ] If we adjusted one score by ±1 point, would winner change?
- [ ] Which scores are most uncertain? (Could they change with more data)

### Recommendation Template

```markdown
## Recommendation

**Recommended Option:** [Option name] (Score: [X.X])

**Rationale:**
- [Option] scores highest overall ([X.X] vs [Y.Y] for runner-up)
- Key strengths: [What it excels at based on criterion scores]
- Acceptable trade-offs: [Where it scores lower but weight is low enough]

**Key Trade-offs:**
- **Winner:** Strong on [Criterion A, B] ([X]% of total weight)
- **Runner-up:** Strong on [Criterion C] but weaker on [Criterion A]
- **Decision driver:** [Criterion A] matters most ([X]%), where [Winner] excels

**Confidence Level:**
- [ ] **High (>10% margin):** Decision is robust to reasonable assumption changes
- [ ] **Moderate (5-10% margin):** Sensitive to [specific assumption], recommend validating
- [ ] **Low (<5% margin):** Effectively a tie, consider [additional data needed] or [stakeholder input]

**Sensitivity:**
- [Describe any sensitivity - e.g., "If Risk weight increased from 20% to 35%, Option B would win"]

**Next Steps:**
1. [Immediate action - e.g., "Get final pricing from vendor"]
2. [Validation - e.g., "Confirm technical feasibility with engineering"]
3. [Communication - e.g., "Present to steering committee by [date]"]
```

---

## Quality Checklist

Before delivering, verify:

**Decision framing:**
- [ ] Decision is specific and well-defined
- [ ] All viable alternatives included
- [ ] Must-haves clearly separated from nice-to-haves
- [ ] Stakeholders identified

**Criteria:**
- [ ] 3-10 criteria (enough to capture trade-offs, not overwhelming)
- [ ] Each criterion is measurable/scorable
- [ ] Criteria differentiate between options (not all scored the same)
- [ ] No redundancy between criteria
- [ ] Weights sum to 100%
- [ ] Weight distribution reflects true priorities

**Scoring:**
- [ ] Scores use consistent 1-10 scale
- [ ] Objective criteria based on data (not guesses)
- [ ] Subjective criteria have clear definitions/anchors
- [ ] Assumptions and data sources documented
- [ ] Scores are defensible (could explain to stakeholder)

**Analysis:**
- [ ] Weighted scores calculated correctly
- [ ] Options ranked by total score
- [ ] Sensitivity analyzed (close calls identified)
- [ ] Recommendation includes rationale and trade-offs
- [ ] Next steps identified

**Communication:**
- [ ] Matrix table is clear and readable
- [ ] Weights shown in column headers
- [ ] Weighted scores shown (not just raw scores)
- [ ] Recommendation stands out visually
- [ ] Assumptions and limitations noted

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| **Too many criteria (>10)** | Consolidate related criteria into categories |
| **Redundant criteria** | Combine criteria that always score the same |
| **Arbitrary weights** | Use pairwise comparison or stakeholder discussion |
| **Scores are guesses** | Gather data for objective criteria, define anchors for subjective |
| **Confirmation bias** | Weight criteria BEFORE scoring options |
| **Ignoring sensitivity** | Always check if small changes flip the result |
| **False precision** | Match precision to confidence level |
| **Missing "do nothing"** | Include status quo as an option to evaluate |

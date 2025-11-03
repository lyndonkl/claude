# Decision Matrix: Advanced Methodology

## Workflow

Copy this checklist for complex decision scenarios:

```
Advanced Decision Matrix Progress:
- [ ] Step 1: Diagnose decision complexity
- [ ] Step 2: Apply advanced weighting techniques
- [ ] Step 3: Calibrate and normalize scores
- [ ] Step 4: Perform rigorous sensitivity analysis
- [ ] Step 5: Facilitate group convergence
```

**Step 1: Diagnose decision complexity** - Identify complexity factors (stakeholder disagreement, high uncertainty, strategic importance). See [1. Decision Complexity Assessment](#1-decision-complexity-assessment).

**Step 2: Apply advanced weighting techniques** - Use AHP or other rigorous methods for contentious decisions. See [2. Advanced Weighting Methods](#2-advanced-weighting-methods).

**Step 3: Calibrate and normalize scores** - Handle different scoring approaches and normalize across scorers. See [3. Score Calibration & Normalization](#3-score-calibration--normalization).

**Step 4: Perform rigorous sensitivity analysis** - Test decision robustness with Monte Carlo or scenario analysis. See [4. Advanced Sensitivity Analysis](#4-advanced-sensitivity-analysis).

**Step 5: Facilitate group convergence** - Use Delphi method or consensus-building techniques. See [5. Group Decision Facilitation](#5-group-decision-facilitation).

---

## 1. Decision Complexity Assessment

### Complexity Indicators

**Low Complexity** (use basic template):
- Clear stakeholder alignment on priorities
- Objective criteria with available data
- Low stakes (reversible decision)
- 3-5 alternatives

**Medium Complexity** (use enhanced techniques):
- Moderate stakeholder disagreement
- Mix of objective and subjective criteria
- Moderate stakes (partially reversible)
- 5-8 alternatives

**High Complexity** (use full methodology):
- Significant stakeholder disagreement on priorities
- Mostly subjective criteria or high uncertainty
- High stakes (irreversible or strategic decision)
- >8 alternatives or multi-phase decision
- Regulatory or compliance implications

### Complexity Scoring

| Factor | Low (1) | Medium (2) | High (3) |
|--------|---------|------------|----------|
| **Stakeholder alignment** | Aligned priorities | Some disagreement | Conflicting priorities |
| **Criteria objectivity** | Mostly data-driven | Mix of data & judgment | Mostly subjective |
| **Decision stakes** | Reversible, low cost | Partially reversible | Irreversible, strategic |
| **Uncertainty level** | Low uncertainty | Moderate uncertainty | High uncertainty |
| **Number of alternatives** | 3-4 options | 5-7 options | 8+ options |

**Complexity Score = Sum of factors**
- **5-7 points:** Use basic template
- **8-11 points:** Use enhanced techniques (sections 2-3)
- **12-15 points:** Use full methodology (all sections)

---

## 2. Advanced Weighting Methods

### Analytic Hierarchy Process (AHP)

**When to use:** High-stakes decisions with contentious priorities, need rigorous justification

**Process:**

1. **Create pairwise comparison matrix:** For each pair, rate 1-9 (1=equal, 3=slightly more important, 5=moderately, 7=strongly, 9=extremely)
2. **Calculate weights:** Normalize columns, average rows
3. **Check consistency:** CR < 0.10 acceptable (use online AHP calculator: bpmsg.com/ahp/ahp-calc.php)

**Example:** Comparing Cost, Performance, Risk, Ease pairwise yields weights: Performance 55%, Risk 20%, Cost 15%, Ease 10%

**Advantage:** Rigorous, forces logical consistency in pairwise judgments.

### Swing Weighting

**When to use:** Need to justify weights based on value difference, not just importance

**Process:**

1. **Baseline:** Imagine all criteria at worst level
2. **Swing:** For each criterion, ask "What value does moving from worst to best create?"
3. **Rank swings:** Which swing creates most value?
4. **Assign points:** Give highest swing 100 points, others relative to it
5. **Convert to weights:** Normalize points to percentages

**Example:**

| Criterion | Worst → Best Scenario | Value of Swing | Points | Weight |
|-----------|----------------------|----------------|--------|--------|
| Performance | 50ms → 5ms response | Huge value gain | 100 | 45% |
| Cost | $100K → $50K | Moderate value | 60 | 27% |
| Risk | High → Low risk | Significant value | 50 | 23% |
| Ease | Hard → Easy to use | Minor value | 10 | 5% |

**Total points:** 220 → **Weights:** 100/220=45%, 60/220=27%, 50/220=23%, 10/220=5%

**Advantage:** Focuses on marginal value, not abstract importance. Reveals if criteria with wide option variance should be weighted higher.

### Multi-Voting (Group Weighting)

**When to use:** Group of 5-15 stakeholders needs to converge on weights

**Process:**

1. **Round 1 - Individual allocation:** Each person assigns 100 points across criteria
2. **Reveal distribution:** Show average and variance for each criterion
3. **Discuss outliers:** Why did some assign 40% to Cost while others assigned 10%?
4. **Round 2 - Revised allocation:** Re-allocate with new information
5. **Converge:** Repeat until variance is acceptable or use average

**Example:**

| Criterion | Round 1 Avg | Round 1 Variance | Round 2 Avg | Round 2 Variance |
|-----------|-------------|------------------|-------------|------------------|
| Cost | 25% | High (±15%) | 30% | Low (±5%) |
| Performance | 40% | Medium (±10%) | 38% | Low (±4%) |
| Risk | 20% | Low (±5%) | 20% | Low (±3%) |
| Ease | 15% | High (±12%) | 12% | Low (±4%) |

**Convergence achieved** when variance <±5% for all criteria.

---

## 3. Score Calibration & Normalization

### Handling Different Scorer Tendencies

**Problem:** Some scorers are "hard graders" (6-7 range), others are "easy graders" (8-9 range). This skews results.

**Solution: Z-score normalization**

**Step 1: Calculate each scorer's mean and standard deviation**

Scorer A: Gave scores [8, 9, 7, 8] → Mean=8, SD=0.8
Scorer B: Gave scores [5, 6, 4, 6] → Mean=5.25, SD=0.8

**Step 2: Normalize each score**

Z-score = (Raw Score - Scorer Mean) / Scorer SD

**Step 3: Re-scale to 1-10**

Normalized Score = 5.5 + (Z-score × 1.5)

**Result:** Scorers are calibrated to same scale, eliminating grading bias.

### Dealing with Missing Data

**Scenario:** Some alternatives can't be scored on all criteria (e.g., vendor A won't share cost until later).

**Approach 1: Conditional matrix**

Score available criteria only, note which are missing. Once data arrives, re-run matrix.

**Approach 2: Pessimistic/Optimistic bounds**

Assign worst-case and best-case scores for missing data. Run matrix twice:
- Pessimistic scenario: Missing data gets low score (e.g., 3)
- Optimistic scenario: Missing data gets high score (e.g., 8)

If same option wins both scenarios → Decision is robust. If different winners → Missing data is decision-critical, must obtain before deciding.

### Non-Linear Scoring Curves

**Problem:** Not all criteria are linear. E.g., cost difference between $10K and $20K matters more than $110K vs $120K.

**Solution: Apply utility curves**

**Diminishing returns curve** (Cost, Time):
- Score = 10 × (1 - e^(-k × Cost Improvement))
- k = sensitivity parameter (higher k = faster diminishing returns)

**Threshold curve** (Must meet minimum):
- Score = 0 if below threshold
- Score = 1-10 linear above threshold

**Example:** Load time criterion with 2-second threshold:
- Option A: 1.5s → Score = 10 (below threshold = great)
- Option B: 3s → Score = 5 (above threshold, linear penalty)
- Option C: 5s → Score = 1 (way above threshold)

---

## 4. Advanced Sensitivity Analysis

### Monte Carlo Sensitivity

**When to use:** High uncertainty in scores, want to understand probability distribution of outcomes

**Process:**

1. **Define uncertainty ranges** for each score
   - Option A Cost score: 6 ± 2 (could be 4-8)
   - Option A Performance: 9 ± 0.5 (could be 8.5-9.5)

2. **Run simulations** (1000+ iterations):
   - Randomly sample scores within uncertainty ranges
   - Calculate weighted total for each option
   - Record winner

3. **Analyze results:**
   - Option A wins: 650/1000 = 65% probability
   - Option B wins: 300/1000 = 30% probability
   - Option C wins: 50/1000 = 5% probability

**Interpretation:**
- **>80% win rate:** High confidence in decision
- **50-80% win rate:** Moderate confidence, option is likely but not certain
- **<50% win rate:** Low confidence, gather more data or consider decision is close call

**Tools:** Excel (=RANDBETWEEN or =NORM.INV), Python (numpy.random), R (rnorm)

### Scenario Analysis

**When to use:** Future is uncertain, decisions need to be robust across scenarios

**Process:**

1. **Define scenarios** (typically 3-4):
   - Best case: Favorable market conditions
   - Base case: Expected conditions
   - Worst case: Unfavorable conditions
   - Black swan: Unlikely but high-impact event

2. **Adjust criterion weights or scores per scenario:**

| Scenario | Cost Weight | Performance Weight | Risk Weight |
|----------|-------------|--------------------|-------------|
| Best case | 20% | 50% | 30% |
| Base case | 30% | 40% | 30% |
| Worst case | 40% | 20% | 40% |

3. **Run matrix for each scenario**, identify winner

4. **Evaluate robustness:**
   - **Dominant option:** Wins in all scenarios → Robust choice
   - **Scenario-dependent:** Different winners → Need to assess scenario likelihood
   - **Mixed:** Wins in base + one other → Moderately robust

### Threshold Analysis

**Question:** At what weight does the decision flip?

**Process:**

1. **Vary one criterion weight** from 0% to 100% (keeping others proportional)
2. **Plot total scores** for all options vs. weight
3. **Identify crossover point** where lines intersect (decision flips)

**Example:**

When Performance weight < 25% → Option B wins (cost-optimized)
When Performance weight > 25% → Option A wins (performance-optimized)

**Insight:** Current weight is 40% for Performance. Decision is robust unless Performance drops below 25% importance.

**Practical use:** Communicate to stakeholders: "Even if we reduce Performance priority to 25% (vs current 40%), Option A still wins. Decision is robust."

---

## 5. Group Decision Facilitation

### Delphi Method (Asynchronous Consensus)

**When to use:** Experts geographically distributed, want to avoid groupthink, need convergence without meetings

**Process:**

**Round 1:**
- Each expert scores options independently (no discussion)
- Facilitator compiles scores, calculates median and range

**Round 2:**
- Share Round 1 results (anonymous)
- Experts see median scores and outliers
- Ask experts to re-score, especially if they were outliers (optional: provide reasoning)

**Round 3:**
- Share Round 2 results
- Experts make final adjustments
- Converge on consensus scores (median or mean)

**Convergence criteria:** Standard deviation of scores <1.5 points per criterion

**Example:**

| Option | Criterion | R1 Scores | R1 Median | R2 Scores | R2 Median | R3 Scores | R3 Median |
|--------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| A | Cost | [5, 7, 9, 6] | 6.5 | [6, 7, 8, 6] | 6.5 | [6, 7, 7, 7] | **7** |

**Advantage:** Avoids dominance by loudest voice, reduces groupthink, allows reflection time.

### Nominal Group Technique (Structured Meeting)

**When to use:** In-person or virtual meeting, need structured discussion to surface disagreements

**Process:**

1. **Silent generation (10 min):** Each person scores options independently
2. **Round-robin sharing (20 min):** Each person shares one score and rationale (no debate yet)
3. **Discussion (30 min):** Debate differences, especially outliers
4. **Re-vote (5 min):** Independent re-scoring after hearing perspectives
5. **Aggregation:** Calculate final scores (mean or median)

**Facilitation tips:**
- Enforce "no interruptions" during round-robin
- Time-box discussion to avoid analysis paralysis
- Focus debate on criteria with widest score variance

### Handling Persistent Disagreement

**Scenario:** After multiple rounds, stakeholders still disagree on weights or scores.

**Options:**

**1. Separate matrices by stakeholder group:**

Run matrix for Engineering priorities, Sales priorities, Executive priorities separately. Present all three results. Highlight where recommendations align vs. differ.

**2. Escalate to decision-maker:**

Present divergence transparently: "Engineering weights Performance at 60%, Sales weights Cost at 50%. Under Engineering weights, Option A wins. Under Sales weights, Option B wins. Recommendation: [Decision-maker] must adjudicate priority trade-off."

**3. Multi-criteria satisficing:**

Instead of optimizing weighted sum, find option that meets minimum thresholds on all criteria. This avoids weighting debate.

**Example:** Option must score ≥7 on Performance AND ≤$50K cost AND ≥6 on Ease of Use. Find options that satisfy all constraints.

---

## 6. Matrix Variations & Extensions

### Weighted Pros/Cons Matrix
Hybrid: Add "Key Pros/Cons/Dealbreakers" columns to matrix for qualitative context alongside quantitative scores.

### Multi-Phase Decision Matrix
**Phase 1:** High-level filter (simple criteria) → shortlist top 3
**Phase 2:** Deep-dive (detailed criteria) → select winner
Avoids analysis paralysis by not deep-diving on all options upfront.

### Risk-Adjusted Matrix
For uncertain scores, use expected value: (Optimistic + 4×Most Likely + Pessimistic) / 6
Accounts for score uncertainty in final weighted total.

---

## 7. Common Failure Modes & Recovery

| Failure Mode | Symptoms | Recovery |
|--------------|----------|----------|
| **Post-Rationalization** | Oddly specific weights, generous scores for preferred option | Assign weights BEFORE scoring, use third-party facilitator |
| **Analysis Paralysis** | >10 criteria, endless tweaking, winner changes repeatedly | Set deadline, time-box criteria (5 max), use satisficing rule |
| **Garbage In, Garbage Out** | Scores are guesses, no data sources, false confidence | Flag uncertainties, gather real data, acknowledge limits |
| **Criterion Soup** | Overlapping criteria, scorer confusion | Consolidate redundant criteria, define each clearly |
| **Spreadsheet Error** | Calculation mistakes, weights don't sum to 100% | Use templates with formulas, peer review calculations |

---

## 8. When to Abandon the Matrix

Despite best efforts, sometimes a decision matrix is not the right tool:

**Abandon if:**

1. **Purely emotional decision:** Choosing baby name, selecting wedding venue (no "right" answer)
   - **Use instead:** Gut feel, user preference vote

2. **Single dominant criterion:** Only cost matters, everything else is noise
   - **Use instead:** Simple cost comparison table

3. **Decision already made:** Political realities mean decision is predetermined
   - **Use instead:** Document decision rationale (not fake analysis)

4. **Future is too uncertain:** Can't meaningfully score because context will change dramatically
   - **Use instead:** Scenario planning, real options analysis, reversible pilot

5. **Stakeholders distrust process:** Matrix seen as "math washing" to impose decision
   - **Use instead:** Deliberative dialog, voting, or delegated authority

**Recognize when structured analysis adds value vs. when it's theater.** Decision matrices work best when:
- Multiple alternatives genuinely exist
- Trade-offs are real and must be balanced
- Stakeholders benefit from transparency
- Data is available or can be gathered
- Decision is reversible if matrix misleads

If these don't hold, consider alternative decision frameworks.

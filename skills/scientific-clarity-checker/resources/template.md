# Clarity Templates

This resource provides templates for scientific clarity assessment.

---

## Claims-Evidence Matrix

### Template

Use this matrix to systematically audit each claim:

| # | Claim | Location | Evidence | Evidence Type | Support Level | Issues |
|---|-------|----------|----------|---------------|---------------|--------|
| 1 | [Claim text] | p.X, §Y | [Evidence cited] | [Data/Citation/Logic] | [Strong/Mod/Weak] | [If any] |
| 2 | | | | | | |
| 3 | | | | | | |

### Evidence Types

- **Data**: Results presented in this document
- **Citation**: Reference to published work
- **Logic**: Logical inference from other claims
- **Authority**: Expert opinion or consensus
- **None**: No explicit support provided

### Support Levels

- **Strong**: Direct evidence, well-documented, replicated
- **Moderate**: Indirect evidence, reasonable inference
- **Weak**: Limited evidence, significant assumptions
- **Missing**: No evidence provided for claim

### Example Completed Matrix

| # | Claim | Location | Evidence | Evidence Type | Support Level | Issues |
|---|-------|----------|----------|---------------|---------------|--------|
| 1 | "Drug X inhibits enzyme Y" | Results, p.5 | IC50 = 10nM, n=3 | Data | Strong | None |
| 2 | "This explains disease Z" | Discussion, p.8 | None stated | Logic | Weak | Overclaiming |
| 3 | "Y is the primary target" | Discussion, p.9 | Smith et al. 2020 | Citation | Moderate | Need mechanism |

---

## Precision Checklist

### Quantification Audit

Check each category for vague vs. precise language:

**Magnitude/Size:**
- [ ] "Large" → Replace with measurement (e.g., "5-fold")
- [ ] "Small" → Replace with measurement (e.g., "15% reduction")
- [ ] "Significant" → Add statistical values (e.g., "p<0.001")

**Frequency/Rate:**
- [ ] "Often" → Replace with percentage (e.g., "in 72% of cases")
- [ ] "Rarely" → Replace with number (e.g., "in 3 of 50 patients")
- [ ] "Sometimes" → Replace with range (e.g., "in 20-30% of samples")

**Time:**
- [ ] "Long-term" → Specify duration (e.g., "6-month follow-up")
- [ ] "Rapid" → Specify timeframe (e.g., "within 2 hours")
- [ ] "Extended" → Specify period (e.g., "14-day treatment")

**Sample Size:**
- [ ] "Multiple" → Specify n (e.g., "n=6 biological replicates")
- [ ] "Several" → Specify count (e.g., "5 independent experiments")
- [ ] "Numerous" → Specify number (e.g., "47 patients")

**Comparisons:**
- [ ] "Higher than" → Add fold-change and p-value
- [ ] "Better than" → Add metric and difference
- [ ] "Similar to" → Add statistical comparison

### Precision Replacement Examples

| Vague | Precise |
|-------|---------|
| "Expression was dramatically increased" | "Expression increased 12-fold (p<0.001, n=6)" |
| "Most patients responded" | "78% of patients (32/41) achieved clinical response" |
| "The treatment was highly effective" | "Treatment reduced tumor volume by 65% (95% CI: 52-78%)" |
| "Cells were treated for an extended period" | "Cells were treated for 72 hours" |
| "A large cohort was studied" | "We analyzed data from 2,847 participants" |

---

## Logic Flow Template

### Argument Reconstruction

Use this template to reconstruct and evaluate arguments:

```markdown
## Argument: [Name/Topic]

### Conclusion (What is being argued)
[State the main claim]

### Premises (Evidence/Reasons given)
P1: [First premise/piece of evidence]
P2: [Second premise/piece of evidence]
P3: [Third premise, if any]

### Logical Structure
P1 + P2 → [Intermediate conclusion]
[Intermediate] + P3 → [Final conclusion]

### Validity Assessment
- Does conclusion follow from premises? [Yes/No/Partially]
- Are all premises true/supported? [Yes/No/Unknown]
- Are there hidden assumptions? [If so, list them]

### Issues Identified
1. [Issue 1]
2. [Issue 2]

### Suggested Fixes
1. [Fix for issue 1]
2. [Fix for issue 2]
```

### Example

```markdown
## Argument: Drug X treats Disease Y

### Conclusion
Drug X should be pursued as a treatment for Disease Y.

### Premises
P1: Protein Z is overexpressed in Disease Y (Citation: Smith 2020)
P2: Drug X inhibits Protein Z (Data: Figure 3)
P3: Inhibiting Protein Z reduces disease symptoms (Logic: inferred)

### Logical Structure
P1 + P2 → Drug X affects a disease-relevant target
[Intermediate] + P3 → Drug X should reduce disease symptoms

### Validity Assessment
- Does conclusion follow from premises? Partially
- Are all premises true/supported? P1 and P2 yes; P3 unsupported
- Hidden assumptions: Z is causal (not just correlated)

### Issues Identified
1. P3 is assumed, not demonstrated
2. Correlation (Z expression) ≠ causation
3. No in vivo or clinical data presented

### Suggested Fixes
1. Add data showing Z inhibition reduces symptoms, or hedge claim
2. Acknowledge correlation vs. causation limitation
3. Frame as "supports further investigation" not "should be pursued"
```

---

## Summary Report Template

### Clarity Assessment Report

```markdown
# Scientific Clarity Assessment

**Document:** [Title/description]
**Date:** [Date]
**Reviewer:** [Name/AI]

## Executive Summary
[2-3 sentences summarizing overall clarity and major issues]

## Claims Audit Summary
- Total claims identified: [N]
- Claims with strong support: [N]
- Claims with weak/no support: [N]
- Overclaiming instances: [N]

## Key Issues

### Critical Issues (Must Fix)
1. [Issue 1 with location]
2. [Issue 2 with location]

### Moderate Issues (Should Fix)
1. [Issue 1 with location]
2. [Issue 2 with location]

### Minor Issues (Optional)
1. [Issue 1]
2. [Issue 2]

## Detailed Findings

### Logic and Argument Structure
[Findings on logical flow]

### Claims vs. Evidence
[Findings on support levels]

### Quantitative Precision
[Findings on vague language]

### Terminology Consistency
[Findings on term usage]

### Hedging Calibration
[Findings on hedge appropriateness]

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]
```

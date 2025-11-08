# Domain Research: Health Science - Templates

## Workflow

```
Health Research Progress:
- [ ] Step 1: Formulate research question (PICOT)
- [ ] Step 2: Assess evidence hierarchy and study design
- [ ] Step 3: Evaluate study quality and bias
- [ ] Step 4: Prioritize and define outcomes
- [ ] Step 5: Synthesize evidence and grade certainty
- [ ] Step 6: Create decision-ready summary
```

**Step 1: Formulate research question (PICOT)**

Use [PICOT Framework](#picot-framework) to structure precise research question with Population, Intervention, Comparator, Outcome, and Timeframe fully specified.

**Step 2: Assess evidence hierarchy and study design**

Select appropriate study design for question type using [Common Question Types](#common-question-types) guidance (RCT for therapy, cross-sectional for diagnosis, cohort for prognosis, observational for rare harms).

**Step 3: Evaluate study quality and bias**

Apply bias assessment using [Evidence Appraisal Template](#evidence-appraisal-template) with appropriate tool (Cochrane RoB 2 for RCTs, ROBINS-I for observational, QUADAS-2 for diagnostic).

**Step 4: Prioritize and define outcomes**

Create hierarchy using [Outcome Hierarchy Template](#outcome-hierarchy-template), prioritizing patient-important outcomes (mortality, QoL) over surrogates (biomarkers), and specify MCID.

**Step 5: Synthesize evidence and grade certainty**

Rate certainty using [GRADE Evidence Profile Template](#grade-evidence-profile-template), assessing study limitations, inconsistency, indirectness, imprecision, and publication bias.

**Step 6: Create decision-ready summary**

Produce evidence summary using [Clinical Interpretation Template](#clinical-interpretation-template) with benefits/harms balance, certainty ratings, applicability, and evidence gaps identified.

---

## PICOT Framework

### Research Question Template

**Clinical scenario**: [Describe the decision problem or knowledge gap]

### PICOT Components

**P (Population)**:
- **Demographics**: [Age range, sex, race/ethnicity if relevant]
- **Condition**: [Disease, severity, stage, diagnostic criteria]
- **Setting**: [Primary care, hospital, community, country/region]
- **Inclusion criteria**: [Key eligibility requirements]
- **Exclusion criteria**: [Factors that make evidence inapplicable]

**I (Intervention)**:
- **Type**: [Drug, procedure, diagnostic test, preventive measure, exposure]
- **Specification**: [Dose, frequency, duration, route, technique details]
- **Co-interventions**: [Other treatments given alongside]
- **Timing**: [When initiated relative to disease course]

**C (Comparator)**:
- **Type**: [Placebo, standard care, alternative treatment, no intervention]
- **Specification**: [Same level of detail as intervention]
- **Rationale**: [Why this comparator?]

**O (Outcome)**:
- **Primary outcome**: [Most important endpoint - typically patient-important]
  - Measurement instrument/definition
  - Timepoint for assessment
  - Minimal clinically important difference (MCID) if known
- **Secondary outcomes**: [Additional endpoints]
- **Safety outcomes**: [Harms, adverse events]

**T (Timeframe)**:
- **Follow-up duration**: [How long? Justification for duration choice]
- **Time to outcome**: [When do you expect to see effect?]

**Structured PICOT statement**:

"In [population], does [intervention] compared to [comparator] affect [outcome] over [timeframe]?"

**Example**: "In adults >65 years with heart failure and reduced ejection fraction (HFrEF), does dapagliflozin 10mg daily compared to standard care (ACE inhibitor + beta-blocker) reduce all-cause mortality over 12 months?"

---

## Outcome Hierarchy Template

### Outcome Prioritization

Rate each outcome as:
- **Critical** (7-9): Essential for decision-making, would change recommendation
- **Important** (4-6): Informs decision but not decisive alone
- **Not important** (1-3): Interesting but doesn't influence decision

| Outcome | Rating (1-9) | Patient-important? | Surrogate? | MCID | Measurement | Timepoint |
|---------|--------------|---------------------|------------|------|-------------|-----------|
| All-cause mortality | 9 (Critical) | Yes | No | N/A | Death registry | 12 months |
| CV mortality | 8 (Critical) | Yes | No | N/A | Adjudicated cause | 12 months |
| Hospitalization (HF) | 7 (Critical) | Yes | No | 1-2 events/year | Hospital admission | 12 months |
| Quality of life (QoL) | 7 (Critical) | Yes | No | 5 points (KCCQ) | KCCQ questionnaire | 6, 12 months |
| 6-minute walk distance | 5 (Important) | Yes | No | 30 meters | 6MWT | 6, 12 months |
| NT-proBNP reduction | 4 (Important) | No | Yes (partial) | 30% reduction | Blood test | 3, 6, 12 months |
| Ejection fraction | 3 (Not important) | No | Yes (weak) | 5% absolute | Echocardiogram | 6, 12 months |

**Notes**:
- Prioritize patient-important outcomes (mortality, symptoms, function, QoL) over surrogates (biomarkers)
- Surrogates only acceptable if validated relationship to patient outcomes exists
- MCID = Minimal Clinically Important Difference (smallest change patients notice as meaningful)

---

## Evidence Appraisal Template

### Study Identification

**Citation**: [Author, Year, Journal]
**Study design**: [RCT, cohort, case-control, cross-sectional, systematic review]
**Research question type**: [Therapy, diagnosis, prognosis, harm, etiology]
**Setting**: [Country, healthcare system, single/multi-center]
**Funding**: [Government, industry, foundation - assess for conflict of interest]

### PICOT Match Assessment

| PICOT Element | Study Population | Your Population | Match? |
|---------------|------------------|-----------------|--------|
| Population | [Study's population] | [Your patient/question] | Yes/Partial/No |
| Intervention | [Study's intervention] | [Your intervention] | Yes/Partial/No |
| Comparator | [Study's comparator] | [Your comparator] | Yes/Partial/No |
| Outcome | [Study's outcomes] | [Your outcomes of interest] | Yes/Partial/No |
| Timeframe | [Study's follow-up] | [Your timeframe] | Yes/Partial/No |

**Applicability**: [Overall assessment - can you apply these results to your question/patient?]

### Risk of Bias Assessment (RCT - Cochrane RoB 2)

| Domain | Judgment | Support |
|--------|----------|---------|
| 1. Randomization process | Low / Some concerns / High | [Was allocation sequence random and concealed?] |
| 2. Deviations from intended interventions | Low / Some concerns / High | [Were participants and personnel blinded? Deviations balanced?] |
| 3. Missing outcome data | Low / Some concerns / High | [Loss to follow-up <10%? Balanced across groups? ITT analysis?] |
| 4. Measurement of outcome | Low / Some concerns / High | [Blinded outcome assessment? Validated instruments?] |
| 5. Selection of reported result | Low / Some concerns / High | [Protocol pre-specified outcomes? Selective reporting?] |

**Overall risk of bias**: Low / Some concerns / High

### Key Results

| Outcome | Intervention group | Control group | Effect estimate | 95% CI | p-value | Clinical interpretation |
|---------|-------------------|---------------|-----------------|--------|---------|-------------------------|
| Mortality | [n/N, %] | [n/N, %] | RR 0.75 | 0.68-0.83 | <0.001 | 25% relative risk reduction |
| QoL change | [Mean ± SD] | [Mean ± SD] | MD 5.2 points | 3.1-7.3 | <0.001 | Exceeds MCID (5 points) |

**Absolute effects**:
- **Risk difference**: [e.g., 5% absolute reduction in mortality]
- **Number needed to treat (NNT)**: [e.g., NNT = 20 to prevent 1 death]

---

## GRADE Evidence Profile Template

### Evidence Summary Table

**Question**: [PICOT question]
**Setting**: [Clinical context]
**Bibliography**: [Key studies included]

| Outcomes | Studies (Design) | Sample Size | Effect Estimate (95% CI) | Absolute Effect | Certainty | Importance |
|----------|------------------|-------------|--------------------------|-----------------|-----------|------------|
| Mortality (12mo) | 5 RCTs | N=15,234 | RR 0.75 (0.70-0.80) | 50 fewer per 1000 (from 60 to 40) | ⊕⊕⊕⊕ High | Critical |
| HF hospitalization | 5 RCTs | N=15,234 | RR 0.70 (0.65-0.76) | 90 fewer per 1000 (from 300 to 210) | ⊕⊕⊕○ Moderate¹ | Critical |
| QoL (KCCQ change) | 3 RCTs | N=8,500 | MD 5.2 (3.1-7.3) | 5.2 points higher (MCID=5) | ⊕⊕⊕○ Moderate² | Critical |
| Serious adverse events | 5 RCTs | N=15,234 | RR 0.95 (0.88-1.03) | 15 fewer per 1000 (from 300 to 285) | ⊕⊕⊕○ Moderate³ | Critical |

**Footnotes**:
1. Downgraded for inconsistency (I²=55%, moderate heterogeneity across studies)
2. Downgraded for indirectness (QoL instrument not validated in all subgroups)
3. Downgraded for imprecision (confidence interval includes no effect)

### GRADE Certainty Assessment

| Outcome | Study Design | Risk of Bias | Inconsistency | Indirectness | Imprecision | Publication Bias | Upgrade Factors | Final Certainty |
|---------|--------------|--------------|---------------|--------------|-------------|------------------|-----------------|-----------------|
| Mortality | RCT (High) | No serious (-0) | No serious (-0) | No serious (-0) | No serious (-0) | Undetected (-0) | None | ⊕⊕⊕⊕ High |
| HF hosp | RCT (High) | No serious (-0) | Serious (-1) | No serious (-0) | No serious (-0) | Undetected (-0) | None | ⊕⊕⊕○ Moderate |
| QoL | RCT (High) | No serious (-0) | No serious (-0) | Serious (-1) | No serious (-0) | Undetected (-0) | None | ⊕⊕⊕○ Moderate |

**Certainty definitions**:
- **High** (⊕⊕⊕⊕): Very confident true effect is close to estimate
- **Moderate** (⊕⊕⊕○): Moderately confident; true effect likely close but could differ substantially
- **Low** (⊕⊕○○): Limited confidence; true effect may be substantially different
- **Very Low** (⊕○○○): Very little confidence; true effect likely substantially different

---

## Clinical Interpretation Template

### Evidence-to-Decision

**Benefits**:
- [List benefits with certainty ratings]
- Example: Mortality reduction (RR 0.75, GRADE: High) - clear benefit

**Harms**:
- [List harms with certainty ratings]
- Example: Serious adverse events (RR 0.95, GRADE: Moderate) - no significant increase

**Balance of benefits vs harms**: [Favorable / Unfavorable / Uncertain]

**Certainty of evidence**: [Overall certainty across critical outcomes]

**Patient values and preferences**: [Are there important variations? Uncertainty?]

**Resource implications**: [Cost, accessibility, training required]

**Applicability**: [Can these results be applied to your setting/population?]
- PICO match: [Assess similarity]
- Setting differences: [Trial setting vs your setting]
- Feasibility: [Can intervention be delivered as in trial?]

**Evidence gaps**: [What remains uncertain? Need for further research?]

---

## Systematic Review Protocol Template

### Protocol Information

**Title**: [Systematic review title]
**Registration**: [PROSPERO ID if applicable]
**Review team**: [Names, roles, affiliations]
**Funding**: [Source - declare conflicts of interest]

### Research Question (PICOT)

[Use PICOT template above]

### Eligibility Criteria

**Inclusion criteria**:
- Study designs: [RCTs, cohort, etc.]
- Population: [Specific PICO elements]
- Interventions: [What will be included]
- Comparators: [What will be included]
- Outcomes: [Which outcomes required for inclusion]
- Setting/context: [Geographic, time period]
- Language: [English only? All languages?]

**Exclusion criteria**:
- [Specific exclusions]

### Search Strategy

**Databases**: [MEDLINE, Embase, Cochrane CENTRAL, CINAHL, PsycINFO, Web of Science]

**Search terms**: [Key concepts - population AND intervention AND outcome]
- Population: [MeSH terms, keywords]
- Intervention: [MeSH terms, keywords]
- Outcome: [MeSH terms, keywords]

**Other sources**: [Clinical trial registries, grey literature, reference lists, contact authors]

**Date limits**: [From XXXX to present, or all dates]

### Selection Process

- **Screening**: Two reviewers independently screen titles/abstracts, then full text
- **Disagreement resolution**: Discussion, third reviewer if needed
- **Software**: [Covidence, DistillerSR, or other]
- **PRISMA flow diagram**: Document screening at each stage

### Data Extraction

**Information to extract**:
- Study characteristics: Author, year, country, setting, sample size, funding
- Population: Demographics, condition details, inclusion/exclusion criteria
- Intervention: Specifics of intervention (dose, duration, delivery)
- Comparator: Details of comparison
- Outcomes: Results for each outcome (means, SDs, events, totals)
- Risk of bias domains: [RoB 2 or ROBINS-I elements]

**Extraction tool**: Standardized form, piloted on 5 studies

**Duplicate extraction**: Two reviewers independently, compare and resolve discrepancies

### Risk of Bias Assessment

**Tool**: [Cochrane RoB 2 for RCTs, ROBINS-I for observational studies, QUADAS-2 for diagnostic accuracy]

**Domains assessed**: [List specific domains from chosen tool]

**Process**: Two independent reviewers, disagreements resolved by discussion

### Data Synthesis

**Quantitative synthesis (meta-analysis)**: [If appropriate]
- Statistical method: [Random-effects or fixed-effect]
- Effect measure: [Risk ratio, odds ratio, mean difference, standardized mean difference]
- Software: [RevMan, R, Stata]
- Heterogeneity assessment: [I², Cochran's Q test]
- Subgroup analyses: [Pre-specified]
- Sensitivity analyses: [Exclude high risk of bias, publication bias adjustment]

**Qualitative synthesis**: [If meta-analysis not appropriate]
- Narrative summary organized by [outcome, population, intervention]

### Certainty of Evidence

**GRADE assessment**: Rate certainty (high, moderate, low, very low) for each critical outcome

**Summary of findings table**: Create evidence profile with absolute effects and certainty ratings

---

## Common Question Types

### Therapy Question

**PICOT**: Population with condition → Intervention vs Comparator → Patient-important outcomes → Follow-up
**Best study design**: RCT (if feasible); cohort if RCT not ethical/feasible
**Bias tool**: Cochrane RoB 2 (RCT), ROBINS-I (observational)
**Key outcomes**: Mortality, morbidity, quality of life, adverse events
**Statistical measure**: Risk ratio, hazard ratio, absolute risk reduction, NNT

### Diagnosis Question

**PICOT**: Population with suspected condition → Index test vs Reference standard → Diagnostic accuracy → Cross-sectional
**Best study design**: Cross-sectional with consecutive enrollment
**Bias tool**: QUADAS-2
**Key outcomes**: Sensitivity, specificity, positive/negative predictive values, likelihood ratios
**Statistical measure**: Sensitivity, specificity, diagnostic odds ratio, AUC

### Prognosis Question

**PICOT**: Population with condition/exposure → Prognostic factors → Outcomes → Long-term follow-up
**Best study design**: Prospective cohort
**Bias tool**: ROBINS-I or PROBAST (for prediction models)
**Key outcomes**: Incidence, survival, hazard ratios, risk prediction performance
**Statistical measure**: Hazard ratio, incidence rate, C-statistic, calibration

### Harm Question

**PICOT**: Population exposed to intervention → Adverse outcomes → Timeframe for rare/delayed harms
**Best study design**: RCT for common harms; observational for rare harms
**Bias tool**: Cochrane RoB 2 (RCT), ROBINS-I (observational)
**Key outcomes**: Serious adverse events, discontinuations, organ-specific toxicity
**Statistical measure**: Risk ratio, absolute risk increase, number needed to harm (NNH)

---

## Quick Reference

### Evidence Hierarchy by Question Type

**Therapy**: Systematic review of RCTs > RCT > Cohort > Case-control > Case series
**Diagnosis**: Systematic review > Cross-sectional with consecutive enrollment > Case-control (inflates accuracy)
**Prognosis**: Systematic review > Prospective cohort > Retrospective cohort > Case-control
**Harm**: Systematic review > RCT (common harms) > Observational (rare harms) > Case series

### GRADE Domains

**Downgrade certainty for**:
1. **Risk of bias** (study limitations)
2. **Inconsistency** (unexplained heterogeneity, I² > 50%)
3. **Indirectness** (PICO mismatch, surrogate outcomes)
4. **Imprecision** (wide confidence intervals, small sample)
5. **Publication bias** (funnel plot asymmetry, selective reporting)

**Upgrade certainty for** (observational studies):
1. **Large effect** (RR > 2 or < 0.5; very large RR > 5 or < 0.2)
2. **Dose-response gradient**
3. **All plausible confounders would reduce effect**

### Effect Size Interpretation

**Risk Ratio (RR)**:
- RR = 1.0: No effect
- RR = 0.75: 25% relative risk reduction
- RR = 1.25: 25% relative risk increase

**Minimal Clinically Important Difference (MCID) - Common Scales**:
- **KCCQ** (Kansas City Cardiomyopathy Questionnaire): 5 points
- **SF-36** (Short Form Health Survey): 5-10 points
- **VAS pain** (0-100): 10-15 points
- **6-minute walk test**: 30 meters
- **FEV₁** (lung function): 100-140 mL

### Sample Size Considerations

**Adequate power**: ≥80% power to detect MCID
**Typical requirements**:
- Mortality reduction (5% → 4%): ~10,000 per arm
- QoL improvement (MCID): ~200-500 per arm
- Diagnostic accuracy (sensitivity 85% → 90%): ~300-500 patients

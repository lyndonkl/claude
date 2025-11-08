# Domain Research: Health Science - Advanced Methodology

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

Define precise PICOT elements for answerable research question (see template.md for framework).

**Step 2: Assess evidence hierarchy and study design**

Match study design to question type using [1. Evidence Hierarchy](#1-evidence-hierarchy) (RCT for therapy, cohort for prognosis, cross-sectional for diagnosis).

**Step 3: Evaluate study quality and bias**

Apply systematic bias assessment using [2. Bias Assessment](#2-bias-assessment) (Cochrane RoB 2, ROBINS-I, or QUADAS-2 depending on design).

**Step 4: Prioritize and define outcomes**

Distinguish patient-important from surrogate outcomes using [6. Outcome Measurement](#6-outcome-measurement) guidance on MCID, composite outcomes, and surrogates.

**Step 5: Synthesize evidence and grade certainty**

Rate certainty using [3. GRADE Framework](#3-grade-framework) (downgrade for bias/inconsistency/indirectness/imprecision/publication bias, upgrade for large effects/dose-response). For multiple studies, apply [4. Meta-Analysis Techniques](#4-meta-analysis-techniques).

**Step 6: Create decision-ready summary**

Synthesize findings using [8. Knowledge Translation](#8-knowledge-translation) evidence-to-decision framework, assess applicability per [7. Special Populations & Contexts](#7-special-populations--contexts), and avoid [9. Common Pitfalls](#9-common-pitfalls--fixes).

---

## 1. Evidence Hierarchy

### Study Design Selection by Question Type

**Therapy/Intervention Questions**:
- **Gold standard**: RCT (randomized controlled trial)
- **When RCT not feasible**: Prospective cohort or pragmatic trial
- **Never acceptable**: Case series, expert opinion for causal claims
- **Rationale**: RCTs minimize confounding through randomization, establishing causation

**Diagnostic Accuracy Questions**:
- **Gold standard**: Cross-sectional study with consecutive enrollment
- **Critical requirement**: Compare index test to validated reference standard in same patients
- **Avoid**: Case-control design (inflates sensitivity/specificity by selecting extremes)
- **Rationale**: Cross-sectional design prevents spectrum bias; consecutive enrollment prevents selection bias

**Prognosis/Prediction Questions**:
- **Gold standard**: Prospective cohort (follow from exposure to outcome)
- **Acceptable**: Retrospective cohort with robust data (registries, databases)
- **Avoid**: Case-control (can't estimate incidence), cross-sectional (no temporal sequence)
- **Rationale**: Cohort design establishes temporal sequence, allows incidence calculation

**Harm/Safety Questions**:
- **Common harms**: RCTs (adequate power for events occurring in >1% patients)
- **Rare harms**: Large observational studies (cohort, case-control, pharmacovigilance)
- **Delayed harms**: Long-term cohort studies or registries
- **Rationale**: RCTs often lack power/duration for rare or delayed harms; observational studies provide larger samples and longer follow-up

### Hierarchy by Evidence Strength

**Level 1 (Highest)**: Systematic reviews and meta-analyses of well-designed RCTs
**Level 2**: Individual large, well-designed RCT with low risk of bias
**Level 3**: Well-designed RCTs with some limitations (quasi-randomized, not blinded)
**Level 4**: Cohort studies (prospective better than retrospective)
**Level 5**: Case-control studies
**Level 6**: Cross-sectional surveys (descriptive only, not causal)
**Level 7**: Case series or case reports
**Level 8**: Expert opinion, pathophysiologic rationale

**Important**: Hierarchy is a starting point. Study quality matters more than design alone. Well-conducted cohort > poorly conducted RCT.

---

## 2. Bias Assessment

### Cochrane Risk of Bias 2 (RoB 2) for RCTs

**Domain 1: Randomization Process**
- **Low risk**: Computer-generated sequence, central allocation, opaque envelopes
- **Some concerns**: Randomization method unclear, baseline imbalances suggesting problems
- **High risk**: Non-random sequence (alternation, date of birth), predictable allocation, post-randomization exclusions

**Domain 2: Deviations from Intended Interventions**
- **Low risk**: Double-blind, protocol deviations balanced across groups, intention-to-treat (ITT) analysis
- **Some concerns**: Open-label but objective outcomes, minor unbalanced deviations
- **High risk**: Open-label with subjective outcomes, substantial deviation (>10% cross-over), per-protocol analysis only

**Domain 3: Missing Outcome Data**
- **Low risk**: <5% loss to follow-up, balanced across groups, multiple imputation if >5%
- **Some concerns**: 5-10% loss, ITT analysis used, or reasons for missingness reported
- **High risk**: >10% loss, or imbalanced loss (>5% difference between groups), or complete-case analysis with no sensitivity

**Domain 4: Measurement of Outcome**
- **Low risk**: Blinded outcome assessors, objective outcomes (mortality, lab values)
- **Some concerns**: Unblinded assessors but objective outcomes
- **High risk**: Unblinded assessors with subjective outcomes (pain, quality of life)

**Domain 5: Selection of Reported Result**
- **Low risk**: Protocol published before enrollment, all pre-specified outcomes reported
- **Some concerns**: Protocol not available, but outcomes match methods section
- **High risk**: Outcomes in results differ from protocol/methods, selective subgroup reporting

**Overall Judgment**: If any domain is "high risk" → Overall high risk. If all domains "low risk" → Overall low risk. Otherwise → Some concerns.

### ROBINS-I for Observational Studies

**Domain 1: Confounding**
- **Low**: All important confounders measured and adjusted (multivariable regression, propensity scores, matching)
- **Moderate**: Most confounders adjusted, but some unmeasured
- **Serious**: Important confounders not adjusted (e.g., comparing treatment groups without adjusting for severity)
- **Critical**: Confounding by indication makes results uninterpretable

**Domain 2: Selection of Participants**
- **Low**: Selection into study unrelated to intervention and outcome (inception cohort, consecutive enrollment)
- **Serious**: Post-intervention selection (survivor bias, selecting on outcome)

**Domain 3: Classification of Interventions**
- **Low**: Intervention status well-defined and independently ascertained (pharmacy records, procedure logs)
- **Serious**: Intervention status based on patient recall or subjective classification

**Domain 4: Deviations from Intended Interventions**
- **Low**: Intervention/comparator groups received intended interventions, co-interventions balanced
- **Serious**: Substantial differences in co-interventions between groups

**Domain 5: Missing Data**
- **Low**: <5% missing outcome data, or multiple imputation with sensitivity analysis
- **Serious**: >10% missing, complete-case analysis with no sensitivity

**Domain 6: Measurement of Outcomes**
- **Low**: Blinded outcome assessment or objective outcomes
- **Serious**: Unblinded assessment of subjective outcomes, knowledge of intervention may bias assessment

**Domain 7: Selection of Reported Result**
- **Low**: Analysis plan pre-specified and followed
- **Serious**: Selective reporting of outcomes or subgroups

### QUADAS-2 for Diagnostic Accuracy Studies

**Domain 1: Patient Selection**
- **Low**: Consecutive or random sample, case-control design avoided, appropriate exclusions
- **High**: Case-control design (inflates accuracy), inappropriate exclusions (spectrum bias)

**Domain 2: Index Test**
- **Low**: Pre-specified threshold, blinded to reference standard
- **High**: Threshold chosen after seeing results, unblinded interpretation

**Domain 3: Reference Standard**
- **Low**: Reference standard correctly classifies condition, interpreted blind to index test
- **High**: Imperfect reference standard, differential verification (different reference for positive/negative index)

**Domain 4: Flow and Timing**
- **Low**: All patients receive same reference standard, appropriate interval between tests
- **High**: Not all patients receive reference (partial verification), long interval allowing disease status to change

---

## 3. GRADE Framework

### Starting Certainty

**RCTs**: Start at High certainty
**Observational studies**: Start at Low certainty

### Downgrade Factors (Each -1 or -2 levels)

**1. Risk of Bias (Study Limitations)**
- **Serious (-1)**: Most studies have some concerns on RoB 2, or observational studies with moderate risk on most ROBINS-I domains
- **Very serious (-2)**: Most studies high risk of bias, or observational with serious/critical risk on ROBINS-I

**2. Inconsistency (Heterogeneity)**
- **Serious (-1)**: I² = 50-75%, or point estimates vary widely, or confidence intervals show minimal overlap
- **Very serious (-2)**: I² > 75%, opposite directions of effect
- **Do not downgrade if**: Heterogeneity explained by subgroup analysis, or all studies show benefit despite variation in magnitude

**3. Indirectness (Applicability)**
- **Serious (-1)**: Indirect comparison (no head-to-head trial), surrogate outcome instead of patient-important, PICO mismatch (different population/intervention than question)
- **Very serious (-2)**: Multiple levels of indirectness (e.g., indirect comparison + surrogate outcome)

**4. Imprecision (Statistical Uncertainty)**
- **Serious (-1)**: Confidence interval crosses minimal clinically important difference (MCID) or includes both benefit and harm, or optimal information size (OIS) not met
- **Very serious (-2)**: Very wide CI, very small sample (<100 total), or very few events (<100 total)
- **Rule of thumb**: OIS = sample size required for adequately powered RCT (~400 patients for typical effect size)

**5. Publication Bias**
- **Serious (-1)**: Funnel plot asymmetry (Egger's test p<0.10), all studies industry-funded with positive results, or known unpublished negative trials
- **Note**: Requires ≥10 studies to assess funnel plot. Consider searching trial registries for unpublished studies.

### Upgrade Factors (Observational Studies Only)

**1. Large Effect**
- **Upgrade +1**: RR > 2 or < 0.5 (based on consistent evidence, no plausible confounders)
- **Upgrade +2**: RR > 5 or < 0.2 ("very large effect")
- **Example**: Smoking → lung cancer (RR ~20) upgraded from low to moderate or high

**2. Dose-Response Gradient**
- **Upgrade +1**: Increasing exposure associated with increasing risk/benefit in consistent pattern
- **Example**: More cigarettes/day → higher lung cancer risk

**3. All Plausible Confounders Would Reduce Observed Effect**
- **Upgrade +1**: Despite confounding working against finding effect, effect still observed
- **Example**: Healthy user bias would reduce observed benefit, yet benefit still seen

### Final Certainty Rating

**High** (⊕⊕⊕⊕): Very confident true effect is close to estimate. Further research very unlikely to change conclusion.

**Moderate** (⊕⊕⊕○): Moderately confident. True effect is likely close to estimate, but could be substantially different. Further research may change conclusion.

**Low** (⊕⊕○○): Limited confidence. True effect may be substantially different. Further research likely to change conclusion.

**Very Low** (⊕○○○): Very little confidence. True effect is likely substantially different. Any estimate is very uncertain.

---

## 4. Meta-Analysis Techniques

### When to Pool (Meta-Analysis)

**Pool when**:
- Studies address same PICO question
- Outcomes measured similarly (same construct, similar timepoints)
- Low to moderate heterogeneity (I² < 60%)
- At least 3 studies available

**Do not pool when**:
- Substantial heterogeneity (I² > 75%) unexplained by subgroups
- Different interventions (can't pool aspirin with warfarin for "anticoagulation")
- Different populations (adults vs children, mild vs severe disease)
- Methodologically flawed studies (high risk of bias)

### Statistical Models

**Fixed-effect model**: Assumes one true effect, differences due to sampling error only.
- **Use when**: I² < 25%, studies very similar
- **Calculation**: Inverse-variance weighting (larger studies get more weight)

**Random-effects model**: Assumes distribution of true effects, accounts for between-study variance.
- **Use when**: I² ≥ 25%, clinical heterogeneity expected
- **Calculation**: DerSimonian-Laird or REML methods
- **Note**: Gives more weight to smaller studies than fixed-effect

**Recommendation**: Use random-effects as default for clinical heterogeneity, even if I² low.

### Effect Measures

**Binary outcomes** (event yes/no):
- **Risk Ratio (RR)**: Events in intervention / Events in control. Easier to interpret than OR.
- **Odds Ratio (OR)**: Used when outcome rare (<10%) or case-control design.
- **Risk Difference (RD)**: Absolute difference. Important for clinical interpretation (NNT = 1/RD).

**Continuous outcomes** (measured on scale):
- **Mean Difference (MD)**: When outcome measured on same scale (e.g., mm Hg blood pressure)
- **Standardized Mean Difference (SMD)**: When outcome measured on different scales (different QoL questionnaires). Interpret as effect size: SMD 0.2 = small, 0.5 = moderate, 0.8 = large.

**Time-to-event outcomes**:
- **Hazard Ratio (HR)**: Accounts for censoring and time. From Cox proportional hazards models.

### Heterogeneity Assessment

**I² statistic**: % of variability due to heterogeneity rather than chance.
- **I² = 0-25%**: Low heterogeneity (might not need subgroup analysis)
- **I² = 25-50%**: Moderate heterogeneity (explore sources)
- **I² = 50-75%**: Substantial heterogeneity (subgroup analysis essential)
- **I² > 75%**: Considerable heterogeneity (consider not pooling)

**Cochran's Q test**: Tests whether heterogeneity is statistically significant (p<0.10 suggests heterogeneity).
- **Limitation**: Low power with few studies, high power with many studies (may detect clinically unimportant heterogeneity)

**Exploring heterogeneity**:
1. Visual inspection (forest plot - outliers?)
2. Subgroup analysis (by population, intervention, setting, risk of bias)
3. Meta-regression (if ≥10 studies) - test whether study-level characteristics (year, dose, age) explain heterogeneity
4. Sensitivity analysis (exclude high risk of bias, exclude outliers)

### Publication Bias Assessment

**Methods** (require ≥10 studies):
- **Funnel plot**: Plot effect size vs precision (SE). Asymmetry suggests small-study effects/publication bias.
- **Egger's test**: Statistical test for funnel plot asymmetry (p<0.10 suggests bias).
- **Trim and fill**: Impute missing studies and recalculate pooled effect.

**Limitations**: Asymmetry can be due to heterogeneity, not just publication bias. Small-study effects != publication bias.

**Search mitigation**: Search clinical trial registries (ClinicalTrials.gov, EudraCT), contact authors, grey literature.

---

## 5. Advanced Study Designs

### Pragmatic Trials

**Purpose**: Evaluate effectiveness in real-world settings (vs efficacy in ideal conditions).

**Characteristics**:
- Broad inclusion criteria (representative of clinical practice)
- Minimal exclusions (include comorbidities, elderly, diverse populations)
- Flexible interventions (allow adaptations like clinical practice)
- Clinically relevant comparators (usual care, not placebo)
- Patient-important outcomes (mortality, QoL, not just biomarkers)
- Long-term follow-up (capture real-world adherence, adverse events)

**PRECIS-2 wheel**: Rates trials from explanatory (ideal conditions) to pragmatic (real-world) on 9 domains.

**Example**: HOPE-3 trial (polypill for CVD prevention) - broad inclusion, minimal monitoring, usual care comparator, long-term follow-up.

### Non-Inferiority Trials

**Purpose**: Show new treatment is "not worse" than standard (by pre-defined margin), usually because new treatment has other advantages (cheaper, safer, easier).

**Key concepts**:
- **Non-inferiority margin** (Δ): Maximum acceptable difference. New treatment preserves ≥50% of standard's benefit over placebo.
- **One-sided test**: Test whether upper limit of 95% CI for difference < Δ.
- **Interpretation**: If upper CI < Δ, declare non-inferiority. If CI crosses Δ, inconclusive.

**Pitfalls**:
- Large non-inferiority margins (>50% of benefit) allow ineffective treatments
- Per-protocol analysis bias (favors non-inferiority); need ITT + per-protocol
- Assay sensitivity: Must show historical evidence that standard > placebo

**Example**: Enoxaparin vs unfractionated heparin for VTE treatment. Margin = 2% absolute difference in recurrent VTE.

### Cluster Randomized Trials

**Design**: Randomize groups (hospitals, clinics, communities) not individuals.

**When used**:
- Intervention delivered at group level (policy, training, quality improvement)
- Contamination risk if individuals randomized (control group adopts intervention)

**Statistical consideration**:
- **Intracluster correlation (ICC)**: Individuals within cluster more similar than across clusters
- **Design effect**: Effective sample size reduced: Deff = 1 + (m-1) × ICC, where m = cluster size
- **Analysis**: Account for clustering (GEE, mixed models, cluster-level analysis)

**Example**: COMMIT trial (smoking cessation at workplace level). Randomized worksites, analyzed accounting for clustering.

### N-of-1 Trials

**Design**: Single patient receives multiple crossovers between treatments in random order.

**When used**:
- Chronic stable conditions (asthma, arthritis, chronic pain)
- Rapid onset/offset treatments
- Substantial inter-patient variability in response
- Patient wants personalized evidence

**Requirements**:
- ≥3 treatment periods per arm (A-B-A-B-A-B)
- Washout between periods if needed
- Blind patient and assessor if possible
- Pre-specify outcome and decision rule

**Analysis**: Compare outcomes during A vs B periods within patient (paired t-test, meta-analysis across periods).

**Example**: Stimulant dose optimization for ADHD. Test 3 doses + placebo in randomized crossover, 1-week periods each.

---

## 6. Outcome Measurement

### Minimal Clinically Important Difference (MCID)

**Definition**: Smallest change in outcome that patients perceive as beneficial (and would mandate change in management).

**Determination methods**:
1. **Anchor-based**: Link change to external anchor ("How much has your pain improved?" - "A little" threshold)
2. **Distribution-based**: 0.5 SD or 1 SE as MCID (statistical, not patient-centered)
3. **Delphi consensus**: Expert panel agrees on MCID

**Examples**:
- **Pain VAS** (0-100): MCID = 10-15 points
- **6-minute walk distance**: MCID = 30 meters
- **KCCQ** (Kansas City Cardiomyopathy Questionnaire): MCID = 5 points
- **FEV₁** (lung function): MCID = 100-140 mL

**Interpretation**: Effect size must exceed MCID to be clinically meaningful. p<0.05 with effect < MCID = statistically significant but clinically trivial.

### Composite Outcomes

**Definition**: Combines ≥2 outcomes into single endpoint (e.g., "death, MI, or stroke").

**Advantages**:
- Increases event rate → reduces required sample size
- Captures multiple aspects of benefit/harm

**Disadvantages**:
- Obscures which component drives effect (mortality reduction? or non-fatal MI?)
- Components may not be equally important to patients (MI ≠ revascularization)
- If components affected differently, composite can mislead

**Guidelines**:
- Report components separately
- Verify effect is consistent across components
- Weight components by importance if possible
- Avoid composites with many low-importance components

**Example**: MACE (major adverse cardiac events) = death + MI + stroke (appropriate). But "death, MI, stroke, or revascularization" dilutes with less important outcome.

### Surrogate Outcomes

**Definition**: Biomarker/lab value used as substitute for patient-important outcome.

**Valid surrogate criteria** (Prentice criteria):
1. Surrogate associated with clinical outcome (correlation)
2. Intervention affects surrogate
3. Intervention's effect on clinical outcome is mediated through surrogate
4. Effect on surrogate fully captures effect on clinical outcome

**Problems**:
- Many surrogates fail criteria #4 (e.g., antiarrhythmics reduce PVCs but increase mortality)
- Intervention can affect surrogate without affecting clinical outcome

**Examples**:
- **Good surrogate**: Blood pressure for stroke (validated, consistent)
- **Poor surrogate**: Bone density for fracture (drugs increase density but not all reduce fracture)
- **Unvalidated**: HbA1c for microvascular complications (association exists, but lowering HbA1c doesn't always reduce complications)

**Recommendation**: Prioritize patient-important outcomes. Accept surrogates only if validated relationship exists and patient-important outcome infeasible.

---

## 7. Special Populations & Contexts

**Pediatric Evidence**: Age-appropriate outcomes (developmental milestones, parent-reported), pharmacokinetic modeling for dose prediction, extrapolation from adults if justified, expert opinion carries more weight when RCTs infeasible.

**Rare Diseases**: N-of-1 trials, registries, historical controls (with caution), Bayesian methods to reduce sample requirements. Regulatory allows lower evidence standards (orphan drugs, conditional approval).

**Health Technology Assessment**: Assesses clinical effectiveness (GRADE), safety, cost-effectiveness (cost per QALY), budget impact, organizational/ethical/social factors. Thresholds vary (£20-30k/QALY UK, $50-150k US). Requires systematic review + economic model + probabilistic sensitivity analysis.

---

## 8. Knowledge Translation

**Evidence-to-Decision Framework** (GRADE): Problem priority → Desirable/undesirable effects → Certainty → Values → Balance of benefits/harms → Resources → Equity → Acceptability → Feasibility.

**Recommendation strength**:
- **Strong** ("We recommend"): Most patients would want, few would not
- **Conditional** ("We suggest"): Substantial proportion might not want, or uncertainty high

**Guideline Development**: Scope/PICOT → Systematic review → GRADE profiles → EtD framework → Recommendation (strong vs conditional) → External review → Update plan (3-5 years). COI management critical. AGREE II assesses guideline quality.

---

## 9. Common Pitfalls & Fixes

**Surrogate outcomes**: Using unvalidated biomarkers. **Fix**: Prioritize patient-important outcomes (mortality, QoL).

**Composite outcomes**: Obscuring which component drives effect. **Fix**: Report components separately, verify consistency.

**Subgroup proliferation**: Data dredging for false positives. **Fix**: Pre-specify <5 subgroups, test interaction, require plausibility.

**Statistical vs clinical significance**: p<0.05 with effect below MCID. **Fix**: Compare to MCID, report absolute effects (NNT).

**Publication bias**: Missing null results. **Fix**: Search trial registries (ClinicalTrials.gov), contact authors, assess funnel plot.

**Poor applicability**: Extrapolating from selected trials. **Fix**: Assess PICO match, setting differences, patient values.

**Causation claims**: From observational data. **Fix**: Use causal language only for RCTs or strong obs evidence (large effect, dose-response).

**Industry bias**: Uncritical acceptance. **Fix**: Assess COI, check selective reporting, verify independent analysis.

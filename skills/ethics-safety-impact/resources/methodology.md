# Ethics, Safety & Impact Assessment Methodology

Advanced techniques for fairness metrics, privacy analysis, safety assessment, bias detection, and participatory design.

## Workflow

```
Ethics & Safety Assessment Progress:
- [ ] Step 1: Map stakeholders and identify vulnerable groups
- [ ] Step 2: Analyze potential harms and benefits
- [ ] Step 3: Assess fairness and differential impacts
- [ ] Step 4: Evaluate severity and likelihood
- [ ] Step 5: Design mitigations and safeguards
- [ ] Step 6: Define monitoring and escalation protocols
```

**Step 1: Map stakeholders and identify vulnerable groups**

Apply stakeholder analysis and vulnerability assessment frameworks.

**Step 2: Analyze potential harms and benefits**

Use harm taxonomies and benefit frameworks to systematically catalog impacts.

**Step 3: Assess fairness and differential impacts**

Apply [1. Fairness Metrics](#1-fairness-metrics) to measure group disparities.

**Step 4: Evaluate severity and likelihood**

Use [2. Safety Assessment Methods](#2-safety-assessment-methods) for safety-critical systems.

**Step 5: Design mitigations and safeguards**

Apply [3. Mitigation Strategies](#3-mitigation-strategies) and [4. Privacy-Preserving Techniques](#4-privacy-preserving-techniques).

**Step 6: Define monitoring and escalation protocols**

Implement [5. Bias Detection in Deployment](#5-bias-detection-in-deployment) and participatory oversight.

---

## 1. Fairness Metrics

Mathematical definitions of fairness for algorithmic systems.

### Group Fairness Metrics

**Demographic Parity** (Statistical Parity, Independence)
- **Definition**: Positive outcome rate equal across groups
- **Formula**: P(Ŷ=1 | A=a) = P(Ŷ=1 | A=b) for all groups a, b
- **When to use**: When equal representation in positive outcomes is goal (admissions, hiring pipelines)
- **Limitations**: Ignores base rates, may require different treatment to achieve equal outcomes
- **Example**: 40% approval rate for all racial groups

**Equalized Odds** (Error Rate Balance)
- **Definition**: False positive and false negative rates equal across groups
- **Formula**: P(Ŷ=1 | Y=y, A=a) = P(Ŷ=1 | Y=y, A=b) for all y, a, b
- **When to use**: When fairness means equal error rates (lending, criminal justice, medical diagnosis)
- **Strengths**: Accounts for true outcomes, balances burden of errors
- **Example**: 5% false positive rate and 10% false negative rate for all groups

**Equal Opportunity** (True Positive Rate Parity)
- **Definition**: True positive rate equal across groups (among qualified individuals)
- **Formula**: P(Ŷ=1 | Y=1, A=a) = P(Ŷ=1 | Y=1, A=b)
- **When to use**: When accessing benefit/opportunity is key concern (scholarships, job offers)
- **Strengths**: Ensures qualified members of all groups have equal chance
- **Example**: 80% of qualified applicants from each group receive offers

**Calibration** (Test Fairness)
- **Definition**: Predicted probabilities match observed frequencies for all groups
- **Formula**: P(Y=1 | Ŷ=p, A=a) = P(Y=1 | Ŷ=p, A=b) = p
- **When to use**: When probability scores used for decision-making (risk scores, credit scores)
- **Strengths**: Predictions are well-calibrated across groups
- **Example**: Among all applicants scored 70%, 70% actually repay loan in each group

**Disparate Impact** (80% Rule, Four-Fifths Rule)
- **Definition**: Selection rate for protected group ≥ 80% of selection rate for reference group
- **Formula**: P(Ŷ=1 | A=protected) / P(Ŷ=1 | A=reference) ≥ 0.8
- **When to use**: Legal compliance (EEOC guidelines for hiring, lending)
- **Regulatory threshold**: <0.8 triggers investigation, <0.5 strong evidence of discrimination
- **Example**: If 50% of white applicants hired, ≥40% of Black applicants should be hired

### Individual Fairness Metrics

**Similar Individuals Treated Similarly** (Lipschitz Fairness)
- **Definition**: Similar inputs receive similar outputs, regardless of protected attributes
- **Formula**: d(f(x), f(x')) ≤ L · d(x, x') where d is distance metric, L is Lipschitz constant
- **When to use**: When individual treatment should depend on relevant factors only
- **Challenge**: Defining "similarity" in a fair way (what features are relevant?)
- **Example**: Two loan applicants with same income, credit history get similar rates regardless of race

**Counterfactual Fairness**
- **Definition**: Outcome would be same if protected attribute were different (causal fairness)
- **Formula**: P(Ŷ | A=a, X=x) = P(Ŷ | A=a', X=x) for all a, a'
- **When to use**: When causal reasoning appropriate, can model interventions
- **Strengths**: Captures intuition "would outcome change if only race/gender differed?"
- **Example**: Applicant's loan decision same whether they're coded male or female

### Fairness Tradeoffs

**Impossibility results**: Cannot satisfy all fairness definitions simultaneously (except in trivial cases)

Key tradeoffs:
- **Demographic parity vs. calibration**: If base rates differ, cannot have both (Chouldechova 2017)
- **Equalized odds vs. calibration**: Generally incompatible unless perfect accuracy (Kleinberg et al. 2017)
- **Individual vs. group fairness**: Treating similar individuals similarly may still produce group disparities

**Choosing metrics**: Context-dependent
- **High-stakes binary decisions** (hire/fire, admit/reject): Equalized odds or equal opportunity
- **Scored rankings** (credit scores, risk assessments): Calibration
- **Access to benefits** (scholarships, programs): Demographic parity or equal opportunity
- **Legal compliance**: Disparate impact (80% rule)

### Fairness Auditing Process

1. **Identify protected groups**: Race, gender, age, disability, religion, national origin, etc.
2. **Collect disaggregated data**: Outcome metrics by group (requires demographic data collection with consent)
3. **Compute fairness metrics**: Calculate demographic parity, equalized odds, disparate impact across groups
4. **Test statistical significance**: Are differences statistically significant or due to chance? (Chi-square, t-tests)
5. **Investigate causes**: If unfair, why? Biased training data? Proxy features? Measurement error?
6. **Iterate on mitigation**: Debiasing techniques, fairness constraints, data augmentation, feature engineering

---

## 2. Safety Assessment Methods

Systematic techniques for identifying and mitigating safety risks.

### Failure Mode and Effects Analysis (FMEA)

**Purpose**: Identify ways system can fail and prioritize mitigation efforts

**Process**:
1. **Decompose system**: Break into components, functions
2. **Identify failure modes**: For each component, how can it fail? (hardware failure, software bug, human error, environmental condition)
3. **Analyze effects**: What happens if this fails? Local effect? System effect? End effect?
4. **Score severity** (1-10): 1 = negligible, 10 = catastrophic (injury, death)
5. **Score likelihood** (1-10): 1 = rare, 10 = very likely
6. **Score detectability** (1-10): 1 = easily detected, 10 = undetectable before harm
7. **Compute Risk Priority Number (RPN)**: RPN = Severity × Likelihood × Detectability
8. **Prioritize**: High RPN = high priority for mitigation
9. **Design mitigations**: Eliminate failure mode, reduce likelihood, improve detection, add safeguards
10. **Re-compute RPN**: Has mitigation adequately reduced risk?

**Example - Medical AI diagnosis**:
- **Failure mode**: AI misclassifies cancer as benign
- **Effect**: Patient not treated, cancer progresses, death
- **Severity**: 10 (death)
- **Likelihood**: 3 (5% false negative rate)
- **Detectability**: 8 (hard to catch without second opinion)
- **RPN**: 10×3×8 = 240 (high, requires mitigation)
- **Mitigation**: Human review of all negative diagnoses, require 2nd AI model for confirmation, patient follow-up at 3 months
- **New RPN**: 10×1×3 = 30 (acceptable)

### Fault Tree Analysis (FTA)

**Purpose**: Identify root causes that lead to hazard (top-down causal reasoning)

**Process**:
1. **Define top event** (hazard): e.g., "Patient receives wrong medication"
2. **Work backward**: What immediate causes could lead to top event?
   - Use logic gates: AND (all required), OR (any sufficient)
3. **Decompose recursively**: For each cause, what are its causes?
4. **Reach basic events**: Hardware failure, software bug, human error, environmental
5. **Compute probability**: If basic event probabilities known, compute probability of top event
6. **Find minimal cut sets**: Smallest combinations of basic events that cause top event
7. **Prioritize mitigations**: Address minimal cut sets (small changes with big safety impact)

**Example - Wrong medication**:
- Top event: Patient receives wrong medication (OR gate)
  - Path 1: Prescription error (AND gate)
    - Doctor prescribes wrong drug (human error)
    - Pharmacist doesn't catch (human error)
  - Path 2: Dispensing error (AND gate)
    - Correct prescription but wrong drug selected (human error)
    - Barcode scanner fails (equipment failure)
  - Path 3: Administration error
    - Nurse administers wrong drug (human error)
- Minimal cut sets: {Doctor error AND Pharmacist error}, {Dispensing error AND Scanner failure}, {Nurse error}
- Mitigation: Double-check systems (reduce AND probability), barcode scanning (detect errors), nurse training (reduce error rate)

### Hazard and Operability Study (HAZOP)

**Purpose**: Systematic brainstorming to find deviations from intended operation

**Process**:
1. **Divide system into nodes**: Functional components
2. **For each node, apply guide words**: NO, MORE, LESS, AS WELL AS, PART OF, REVERSE, OTHER THAN
3. **Identify deviations**: Guide word + parameter (e.g., "MORE pressure", "NO flow")
4. **Analyze causes**: What could cause this deviation?
5. **Analyze consequences**: What harm results?
6. **Propose safeguards**: Detection, prevention, mitigation

**Example - Content moderation system**:
- Node: Content moderation AI
- Deviation: "MORE false positives" (over-moderation)
  - Causes: Model too aggressive, training data skewed, threshold too low
  - Consequences: Silencing legitimate speech, especially marginalized voices
  - Safeguards: Appeals process, human review sample, error rate dashboard by demographic
- Deviation: "NO moderation" (under-moderation)
  - Causes: Model failure, overwhelming volume, adversarial evasion
  - Consequences: Harmful content remains, harassment, misinformation spreads
  - Safeguards: Redundant systems, rate limiting, user reporting, human backup

### Worst-Case Scenario Analysis

**Purpose**: Stress-test system against extreme but plausible threats

**Process**:
1. **Brainstorm worst cases**: Adversarial attacks, cascading failures, edge cases, Murphy's Law
2. **Assess plausibility**: Could this actually happen? Historical precedents?
3. **Estimate impact**: If it happened, how bad?
4. **Identify single points of failure**: What one thing, if it fails, causes catastrophe?
5. **Design resilience**: Redundancy, fail-safes, graceful degradation, circuit breakers
6. **Test**: Chaos engineering, red teaming, adversarial testing

**Examples**:
- **AI model**: Adversary crafts inputs that fool model (adversarial examples) → Test robustness, ensemble models
- **Data breach**: All user data leaked → Encrypt data, minimize collection, differential privacy
- **Bias amplification**: Feedback loop causes AI to become more biased over time → Monitor drift, periodic retraining, fairness constraints
- **Denial of service**: System overwhelmed by load → Rate limiting, auto-scaling, graceful degradation

---

## 3. Mitigation Strategies

Taxonomy of interventions to reduce harm.

### Prevention (Eliminate Harm)

**Design out the risk**:
- Don't collect sensitive data you don't need (data minimization)
- Don't build risky features (dark patterns, addictive mechanics, manipulation)
- Use less risky alternatives (aggregate statistics vs. individual data, contextual recommendations vs. behavioral targeting)

**Examples**:
- Instead of collecting browsing history, use contextual ads (keywords on current page)
- Instead of infinite scroll (addiction), paginate with clear endpoints
- Instead of storing plaintext passwords, use salted hashes (can't be leaked)

### Reduction (Decrease Likelihood or Severity)

**Technical mitigations**:
- Rate limiting (prevent abuse)
- Friction (slow down impulsive harmful actions - time delays, confirmations, warnings)
- Debiasing algorithms (pre-processing data, in-processing fairness constraints, post-processing calibration)
- Differential privacy (add noise to protect individuals while preserving aggregate statistics)

**Process mitigations**:
- Staged rollouts (limited exposure to catch problems early)
- A/B testing (measure impact before full deployment)
- Diverse teams (more perspectives catch more problems)
- External audits (independent review)

**Examples**:
- Limit posts per hour to prevent spam
- Require confirmation before deleting account or posting sensitive content
- Apply fairness constraints during model training to reduce disparate impact
- Release to 1% of users, monitor for issues, then scale

### Detection (Monitor and Alert)

**Dashboards**: Real-time metrics on harm indicators (error rates by group, complaints, safety incidents)

**Anomaly detection**: Alert when metrics deviate from baseline (spike in false positives, drop in engagement from specific group)

**User reporting**: Easy channels for reporting harms, responsive investigation

**Audit logs**: Track decisions for later investigation (who accessed what data, which users affected by algorithm)

**Examples**:
- Bias dashboard showing approval rates by race, gender, age updated daily
- Alert if moderation false positive rate >2× baseline for any language
- "Report this" button on all content with category options
- Log all loan denials with reason codes for audit

### Response (Address Harm When Found)

**Appeals**: Process for contesting decisions (human review, overturn if wrong)

**Redress**: Compensate those harmed (refunds, apologies, corrective action)

**Incident response**: Playbook for handling harms (who to notify, how to investigate, when to escalate, communication plan)

**Iterative improvement**: Learn from incidents to prevent recurrence

**Examples**:
- Allow users to appeal content moderation decisions, review within 48 hours
- Offer compensation to users affected by outage or data breach
- If bias detected, pause system, investigate, retrain model, re-audit before re-launch
- Publish transparency report on harms, mitigations, outcomes

### Safeguards (Redundancy and Fail-Safes)

**Human oversight**: Human in the loop (review all decisions) or human on the loop (review samples, alert on anomalies)

**Redundancy**: Multiple independent systems, consensus required

**Fail-safes**: If system fails, default to safe state (e.g., medical device fails → alarm, not silent failure)

**Circuit breakers**: Kill switches to shut down harmful features quickly

**Examples**:
- High-stakes decisions (loan denial, medical diagnosis, criminal sentencing) require human review
- Two independent AI models must agree before autonomous action
- If fraud detection fails, default to human review rather than approving all transactions
- CEO can halt product launch if ethics concerns raised, even at last minute

---

## 4. Privacy-Preserving Techniques

Methods to protect individual privacy while enabling data use.

### Data Minimization

- **Collect only necessary data**: Purpose limitation (collect only for stated purpose), don't collect "just in case"
- **Aggregate where possible**: Avoid individual-level data when population-level sufficient
- **Short retention**: Delete data when no longer needed, enforce retention limits

### De-identification

**Anonymization**: Remove direct identifiers (name, SSN, email)
- **Limitation**: Re-identification attacks possible (linkage to other datasets, inference from quasi-identifiers)
- **Example**: Netflix dataset de-identified, but researchers re-identified users by linking to IMDB reviews

**K-anonymity**: Each record indistinguishable from k-1 others (generalize quasi-identifiers like zip, age, gender)
- **Limitation**: Attribute disclosure (if all k records have same sensitive attribute), composition attacks
- **Example**: {Age=32, Zip=12345} → {Age=30-35, Zip=123**}

**Differential Privacy**: Add calibrated noise such that individual's presence/absence doesn't significantly change query results
- **Definition**: P(M(D) = O) / P(M(D') = O) ≤ e^ε where D, D' differ by one person, ε is privacy budget
- **Strengths**: Provable privacy guarantee, composes well, resistant to post-processing
- **Limitations**: Accuracy-privacy tradeoff (more privacy → more noise → less accuracy), privacy budget exhausted over many queries
- **Example**: Census releases aggregate statistics with differential privacy (Apple, Google use for local learning)

### Access Controls

- **Least privilege**: Users access only data needed for their role
- **Audit logs**: Track who accessed what data when, detect anomalies
- **Encryption**: At rest (storage), in transit (network), in use (processing)
- **Multi-party computation**: Compute on encrypted data without decrypting

### Consent and Control

- **Granular consent**: Opt-in for each purpose, not blanket consent
- **Transparency**: Explain what data collected, how used, who it's shared with (in plain language)
- **User controls**: Export data (GDPR right to portability), delete data (right to erasure), opt-out of processing
- **Meaningful choice**: Consent not coerced (service available without consent for non-essential features)

---

## 5. Bias Detection in Deployment

Ongoing monitoring to detect and respond to bias post-launch.

### Bias Dashboards

**Disaggregated metrics**: Track outcomes by protected groups (race, gender, age, disability)
- Approval/rejection rates
- False positive/negative rates
- Recommendation quality (precision, recall, ranking)
- User engagement (click-through, conversion, retention)

**Visualizations**:
- Bar charts showing metric by group, flag >20% disparities
- Time series to detect drift (bias increasing over time?)
- Heatmaps for intersectional analysis (race × gender)

**Alerting**: Automated alerts when disparity crosses threshold

### Drift Detection

**Distribution shift**: Has data distribution changed since training? (Covariate shift, concept drift)
- Monitor input distributions, flag anomalies
- Retrain periodically on recent data

**Performance degradation**: Is model accuracy declining? For which groups?
- A/B test new model vs. old continuously
- Track metrics by group, ensure improvements don't harm any group

**Feedback loops**: Is model changing environment in ways that amplify bias?
- Example: Predictive policing → more arrests in flagged areas → more training data from those areas → more policing (vicious cycle)
- Monitor for amplification: Are disparities increasing over time?

### Participatory Auditing

**Stakeholder involvement**: Include affected groups in oversight, not just internal teams
- Community advisory boards
- Public comment periods
- Transparency reports reviewed by civil society

**Contests**: Bug bounties for finding bias (reward researchers/users who identify fairness issues)

**External audits**: Independent third-party assessment (not self-regulation)

---

## 6. Common Pitfalls

**Fairness theater**: Performative statements without material changes. Impact assessments must change decisions, not just document them.

**Sampling bias in testing**: Testing only on employees (young, educated, English-speaking) misses how diverse users experience harm. Test with actual affected populations.

**Assuming "colorblind" = fair**: Not collecting race data doesn't eliminate bias, it makes bias invisible and impossible to audit. Collect demographic data (with consent and safeguards) to measure fairness.

**Optimization without constraints**: Maximizing engagement/revenue unconstrained leads to amplifying outrage, addiction, polarization. Set ethical boundaries as constraints, not just aspirations.

**Privacy vs. fairness tradeoff**: Can't audit bias without demographic data. Balance: Collect minimal data necessary for fairness auditing, strong access controls, differential privacy.

**One-time assessment**: Ethics is not a launch checkbox. Continuous monitoring required as systems evolve, data drifts, harms emerge over time.

**Technochauvinism**: Believing technical fixes alone solve social problems. Bias mitigation algorithms can help but can't replace addressing root causes (historical discrimination, structural inequality).

**Moving fast and apologizing later**: For safety/ethics, prevention > apology. Harms to vulnerable groups are not acceptable experiments. Staged rollouts, kill switches, continuous monitoring required.

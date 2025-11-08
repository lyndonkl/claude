# Ethics, Safety & Impact Assessment Templates

Quick-start templates for stakeholder mapping, harm/benefit analysis, fairness evaluation, risk prioritization, mitigation planning, and monitoring.

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

Use [Stakeholder Mapping Template](#stakeholder-mapping-template) to identify all affected parties and prioritize vulnerable populations.

**Step 2: Analyze potential harms and benefits**

Brainstorm harms and benefits for each stakeholder group using [Harm/Benefit Analysis Template](#harmbenefit-analysis-template).

**Step 3: Assess fairness and differential impacts**

Evaluate outcome, treatment, and access disparities using [Fairness Assessment Template](#fairness-assessment-template).

**Step 4: Evaluate severity and likelihood**

Prioritize risks using [Risk Matrix Template](#risk-matrix-template) scoring severity and likelihood.

**Step 5: Design mitigations and safeguards**

Plan interventions using [Mitigation Planning Template](#mitigation-planning-template) for high-priority harms.

**Step 6: Define monitoring and escalation protocols**

Set up ongoing oversight using [Monitoring Framework Template](#monitoring-framework-template).

---

## Stakeholder Mapping Template

### Primary Stakeholders (directly affected)

**Group 1**: [Name of stakeholder group]
- **Size/reach**: [How many people?]
- **Relationship**: [How do they interact with feature/decision?]
- **Power/voice**: [Can they advocate for themselves? High/Medium/Low]
- **Vulnerability factors**: [Age, disability, marginalization, economic precarity, etc.]
- **Priority**: [High/Medium/Low risk]

**Group 2**: [Name of stakeholder group]
- **Size/reach**:
- **Relationship**:
- **Power/voice**:
- **Vulnerability factors**:
- **Priority**:

[Add more groups as needed]

### Secondary Stakeholders (indirectly affected)

**Group**: [Name]
- **How affected**: [Indirect impact mechanism]
- **Priority**: [High/Medium/Low risk]

### Societal/Systemic Impacts

- **Norms affected**: [What behaviors/expectations might shift?]
- **Precedents set**: [What does this enable or legitimize for future?]
- **Long-term effects**: [Cumulative, feedback loops, structural changes]

### Vulnerable Groups Prioritization

Check all that apply and note specific considerations:

- [ ] **Children** (<18): Special protections needed (consent, safety, development impact)
- [ ] **Elderly** (>65): Accessibility, digital literacy, vulnerability to fraud
- [ ] **People with disabilities**: Accessibility compliance, exclusion risk, safety
- [ ] **Racial/ethnic minorities**: Historical discrimination, disparate impact, cultural sensitivity
- [ ] **Low-income**: Economic harm, access barriers, inability to absorb costs
- [ ] **LGBTQ+**: Safety in hostile contexts, privacy, outing risk
- [ ] **Non-English speakers**: Language barriers, exclusion, misunderstanding
- [ ] **Politically targeted**: Dissidents, journalists, activists (surveillance, safety)
- [ ] **Other**: [Specify]

**Highest priority groups** (most vulnerable + highest risk):
1.
2.
3.

---

## Harm/Benefit Analysis Template

For each stakeholder group, identify potential harms and benefits.

### Stakeholder Group: [Name]

#### Potential Benefits

**Benefit 1**: [Description]
- **Type**: Economic, Social, Health, Autonomy, Access, Safety, etc.
- **Magnitude**: [High/Medium/Low]
- **Distribution**: [Who gets this benefit? Everyone or subset?]
- **Timeline**: [Immediate, Short-term <1yr, Long-term >1yr]

**Benefit 2**: [Description]
- **Type**:
- **Magnitude**:
- **Distribution**:
- **Timeline**:

#### Potential Harms

**Harm 1**: [Description]
- **Type**: Physical, Psychological, Economic, Social, Autonomy, Privacy, Reputational, Epistemic, Political
- **Mechanism**: [How does harm occur?]
- **Affected subgroup**: [Everyone or specific subset within stakeholder group?]
- **Severity**: [1-5, where 5 = catastrophic]
- **Likelihood**: [1-5, where 5 = very likely]
- **Risk Score**: [Severity × Likelihood]

**Harm 2**: [Description]
- **Type**:
- **Mechanism**:
- **Affected subgroup**:
- **Severity**:
- **Likelihood**:
- **Risk Score**:

**Harm 3**: [Description]
- **Type**:
- **Mechanism**:
- **Affected subgroup**:
- **Severity**:
- **Likelihood**:
- **Risk Score**:

#### Second-Order Effects

- **Feedback loops**: [Does harm create conditions for more harm?]
- **Accumulation**: [Do small harms compound over time?]
- **Normalization**: [Does this normalize harmful practices?]
- **Precedent**: [What does this enable others to do?]

---

## Fairness Assessment Template

### Outcome Fairness (results)

**Metric being measured**: [e.g., approval rate, error rate, recommendation quality]

**By group**:

| Group | Metric Value | Difference from Average | Disparate Impact Ratio |
|-------|--------------|-------------------------|------------------------|
| Group A | | | |
| Group B | | | |
| Group C | | | |
| Overall | | - | - |

**Disparate Impact Ratio** = (Outcome rate for protected group) / (Outcome rate for reference group)
- **> 0.8**: Generally acceptable (80% rule)
- **< 0.8**: Potential disparate impact, investigate

**Questions**:
- [ ] Are outcome rates similar across groups (within 20%)?
- [ ] If not, is there a legitimate justification?
- [ ] Do error rates (false positives/negatives) differ across groups?
- [ ] Who bears the burden of errors?

### Treatment Fairness (process)

**How decisions are made**: [Algorithm, human judgment, hybrid]

**By group**:

| Group | Treatment Description | Dignity/Respect | Transparency | Recourse |
|-------|----------------------|-----------------|--------------|----------|
| Group A | | High/Med/Low | High/Med/Low | High/Med/Low |
| Group B | | High/Med/Low | High/Med/Low | High/Med/Low |

**Questions**:
- [ ] Do all groups receive same quality of service/interaction?
- [ ] Are decisions explained equally well to all groups?
- [ ] Do all groups have equal access to appeals/recourse?
- [ ] Are there cultural or language barriers affecting treatment?

### Access Fairness (opportunity)

**Barriers to access**:

| Barrier Type | Description | Affected Groups | Severity |
|--------------|-------------|-----------------|----------|
| Economic | [e.g., cost, credit required] | | High/Med/Low |
| Technical | [e.g., device, internet, literacy] | | High/Med/Low |
| Geographic | [e.g., location restrictions] | | High/Med/Low |
| Physical | [e.g., accessibility, disability] | | High/Med/Low |
| Social | [e.g., stigma, discrimination] | | High/Med/Low |
| Legal | [e.g., documentation required] | | High/Med/Low |

**Questions**:
- [ ] Can all groups access the service/benefit equally?
- [ ] Are there unnecessary barriers that could be removed?
- [ ] Do barriers disproportionately affect vulnerable groups?

### Intersectionality Check

**Combinations of identities that may face unique harms**:
- Example: Black women (face both racial and gender bias)
- Example: Elderly immigrants (language + digital literacy + age)

Groups to check:
- [ ] Intersection of race and gender
- [ ] Intersection of disability and age
- [ ] Intersection of income and language
- [ ] Other combinations: [Specify]

---

## Risk Matrix Template

Score each harm on Severity (1-5) and Likelihood (1-5). Prioritize high-risk (red/orange) harms for mitigation.

### Severity Scale

- **5 - Catastrophic**: Death, serious injury, irreversible harm, widespread impact
- **4 - Major**: Significant harm, lasting impact, affects many people
- **3 - Moderate**: Noticeable harm, temporary impact, affects some people
- **2 - Minor**: Small harm, easily reversed, affects few people
- **1 - Negligible**: Minimal harm, no lasting impact

### Likelihood Scale

- **5 - Very Likely**: >75% chance, expected to occur
- **4 - Likely**: 50-75% chance, probable
- **3 - Possible**: 25-50% chance, could happen
- **2 - Unlikely**: 5-25% chance, improbable
- **1 - Rare**: <5% chance, very unlikely

### Risk Matrix

| Harm | Stakeholder Group | Severity | Likelihood | Risk Score | Priority |
|------|------------------|----------|------------|------------|----------|
| [Harm 1 description] | [Group] | [1-5] | [1-5] | [S×L] | [Color] |
| [Harm 2 description] | [Group] | [1-5] | [1-5] | [S×L] | [Color] |
| [Harm 3 description] | [Group] | [1-5] | [1-5] | [S×L] | [Color] |

**Priority Color Coding**:
- **Red** (Risk ≥15): Critical, must address before launch
- **Orange** (Risk 9-14): High priority, address soon
- **Yellow** (Risk 5-8): Monitor, mitigate if feasible
- **Green** (Risk ≤4): Low priority, document and monitor

**Prioritized Harms** (Red + Orange):
1. [Highest risk harm]
2. [Second highest]
3. [Third highest]

---

## Mitigation Planning Template

For each high-priority harm, design interventions.

### Harm: [Description of harm being mitigated]

**Affected Group**: [Who experiences this harm]

**Risk Score**: [Severity × Likelihood = X]

#### Mitigation Strategies

**Option 1: [Mitigation name]**
- **Type**: Prevent, Reduce, Detect, Respond, Safeguard, Transparency, Empower
- **Description**: [What is the intervention?]
- **Effectiveness**: [How much does this reduce risk? High/Medium/Low]
- **Cost/effort**: [Resources required? High/Medium/Low]
- **Tradeoffs**: [What are downsides or tensions?]
- **Owner**: [Who is responsible for implementation?]
- **Timeline**: [By when?]

**Option 2: [Mitigation name]**
- **Type**:
- **Description**:
- **Effectiveness**:
- **Cost/effort**:
- **Tradeoffs**:
- **Owner**:
- **Timeline**:

**Recommended Approach**: [Which option(s) to pursue and why]

#### Residual Risk

After mitigation:
- **New severity**: [1-5]
- **New likelihood**: [1-5]
- **New risk score**: [S×L]

**Acceptable?**
- [ ] Yes, residual risk is acceptable given tradeoffs
- [ ] No, need additional mitigations
- [ ] Escalate to [ethics committee/leadership/etc.]

#### Implementation Checklist

- [ ] Design changes specified
- [ ] Testing plan includes affected groups
- [ ] Documentation updated (policies, help docs, disclosures)
- [ ] Training provided (if human review/moderation involved)
- [ ] Monitoring metrics defined (see next template)
- [ ] Review date scheduled (when to reassess)

---

## Monitoring Framework Template

### Outcome Metrics

Track actual impacts post-launch to detect harms early.

**Metric 1**: [Metric name, e.g., "Approval rate parity"]
- **Definition**: [Precisely what is measured]
- **Measurement method**: [How calculated, from what data]
- **Baseline**: [Current or expected value]
- **Target**: [Goal value]
- **Threshold for concern**: [Value that triggers action]
- **Disaggregation**: [Break down by race, gender, age, disability, etc.]
- **Frequency**: [Daily, weekly, monthly, quarterly]
- **Owner**: [Who tracks and reports this]

**Metric 2**: [Metric name]
- Definition, method, baseline, target, threshold, disaggregation, frequency, owner

**Metric 3**: [Metric name]
- Definition, method, baseline, target, threshold, disaggregation, frequency, owner

### Leading Indicators & Qualitative Monitoring

- **Indicator 1**: [e.g., "User reports spike"] - Threshold: [level]
- **Indicator 2**: [e.g., "Declining engagement Group Y"] - Threshold: [level]
- **User feedback**: Channels for reporting concerns
- **Community listening**: Forums, social media, support tickets
- **Affected group outreach**: Check-ins with vulnerable communities

### Escalation Protocol

**Yellow Alert** (early warning):
- **Trigger**: [e.g., Metric exceeds threshold by 10-20%]
- **Response**: Investigate, analyze patterns, prepare report

**Orange Alert** (concerning):
- **Trigger**: [e.g., Metric exceeds threshold by >20%, or multiple yellow alerts]
- **Response**: Escalate to product/ethics team, begin mitigation planning

**Red Alert** (critical):
- **Trigger**: [e.g., Serious harm reported, disparate impact >20%, safety incident]
- **Response**: Escalate to leadership, pause rollout or rollback, immediate remediation

**Escalation Path**:
1. First escalation: [Role/person]
2. If unresolved or critical: [Role/person]
3. Final escalation: [Ethics committee, CEO, board]

### Review Cadence

- **Daily**: Critical safety metrics (safety-critical systems only)
- **Weekly**: User complaints, support tickets
- **Monthly**: Outcome metrics, disparate impact dashboard
- **Quarterly**: Comprehensive fairness audit
- **Annually**: External audit, stakeholder consultation

### Audit & Accountability

- **Audits**: Internal (who, frequency), external (independent, when)
- **Transparency**: What disclosed, where published
- **Affected group consultation**: How vulnerable groups involved in oversight

---

## Complete Assessment Template

Full documentation structure combines all above templates:

1. **Context**: Feature/decision description, problem, alternatives
2. **Stakeholder Analysis**: Use Stakeholder Mapping Template
3. **Harm & Benefit Analysis**: Use Harm/Benefit Analysis Template for each group
4. **Fairness Assessment**: Use Fairness Assessment Template (outcome/treatment/access)
5. **Risk Prioritization**: Use Risk Matrix Template, identify critical harms
6. **Mitigation Plan**: Use Mitigation Planning Template for each critical harm
7. **Monitoring & Escalation**: Use Monitoring Framework Template
8. **Decision**: Proceed/staged rollout/delay/reject with rationale and sign-off
9. **Post-Launch Review**: 30-day, 90-day checks, ongoing monitoring, updates

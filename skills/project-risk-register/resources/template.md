# Project Risk Register Template

## Table of Contents
1. [Workflow](#workflow)
2. [Risk Register Template](#risk-register-template)
3. [Risk Response Planning Template](#risk-response-planning-template)
4. [Risk Monitoring Log Template](#risk-monitoring-log-template)
5. [Guidance for Each Section](#guidance-for-each-section)
6. [Quick Patterns](#quick-patterns)
7. [Quality Checklist](#quality-checklist)

## Workflow

Copy this checklist and track your progress:

```
Risk Register Progress:
- [ ] Step 1: Identify risks across categories
- [ ] Step 2: Assess probability and impact
- [ ] Step 3: Calculate risk scores and prioritize
- [ ] Step 4: Assign owners and define responses
- [ ] Step 5: Monitor and update regularly
```

**Step 1:** Brainstorm risks using category checklist. See [Guidance: Risk Identification](#guidance-risk-identification) for structured brainstorming.

**Step 2:** Score probability (1-5) and impact (1-5) for each risk. See [Guidance: Scoring](#guidance-scoring) for calibration.

**Step 3:** Calculate Risk Score = Prob × Impact, plot on matrix. See [Risk Register Template](#risk-register-template) for visualization.

**Step 4:** For High/Critical risks, assign owners and define responses. See [Risk Response Planning Template](#risk-response-planning-template).

**Step 5:** Review weekly (active) or monthly (longer projects), update scores. See [Risk Monitoring Log Template](#risk-monitoring-log-template).

---

## Risk Register Template

Copy this section to create your risk register:

### Project Risk Register: [Project Name]

**Project**: [Name]
**Date Created**: [YYYY-MM-DD]
**Last Updated**: [YYYY-MM-DD]
**Project Manager**: [Name]
**Review Frequency**: [Weekly / Bi-weekly / Monthly]

#### Risk Matrix Visualization

```
Impact →     1         2         3         4         5
Prob ↓    Minimal   Minor   Moderate  Major   Severe

5 High   │ Medium │ Medium │  High  │  High  │ Critical│
         │   5    │   10   │   15   │   20   │   25    │
4        │  Low   │ Medium │ Medium │  High  │  High   │
         │   4    │    8   │   12   │   16   │   20    │
3 Medium │  Low   │  Low   │ Medium │ Medium │  High   │
         │   3    │    6   │    9   │   12   │   15    │
2        │  Low   │  Low   │  Low   │ Medium │ Medium  │
         │   2    │    4   │    6   │    8   │   10    │
1 Low    │  Low   │  Low   │  Low   │  Low   │ Medium  │
         │   1    │    2   │    3   │    4   │    5    │
```

**Risk Thresholds:**
- **Critical (≥20)**: Escalate to exec, immediate mitigation required
- **High (12-19)**: Active management, weekly review, documented mitigation
- **Medium (6-11)**: Monitor closely, monthly review, contingency plan
- **Low (1-5)**: Accept or minimal mitigation, quarterly review

#### Risk Register Table

| ID | Risk Description | Category | Prob | Impact | Score | Priority | Owner | Status |
|----|------------------|----------|------|--------|-------|----------|-------|--------|
| R-001 | [Specific risk description] | [Technical/Schedule/Resource/External/Scope/Org] | [1-5] | [1-5] | [P×I] | [Critical/High/Medium/Low] | [Name] | [Open/In Mitigation/Closed] |
| R-002 | [Another risk] | [Category] | [1-5] | [1-5] | [P×I] | [Priority] | [Name] | [Status] |
| R-003 | [Another risk] | [Category] | [1-5] | [1-5] | [P×I] | [Priority] | [Name] | [Status] |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Risk Summary by Priority:**
- **Critical (≥20)**: X risks
- **High (12-19)**: X risks
- **Medium (6-11)**: X risks
- **Low (1-5)**: X risks
- **Total Active Risks**: X

**Risk Summary by Category:**
- **Technical**: X risks
- **Schedule**: X risks
- **Resource**: X risks
- **External**: X risks
- **Scope**: X risks
- **Organizational**: X risks

---

## Risk Response Planning Template

Copy this section for detailed risk response plans (High/Critical risks only):

### Risk Response Plan: [Risk ID - Risk Title]

**Risk ID**: R-XXX
**Risk Description**: [Detailed description of what could go wrong]
**Category**: [Technical / Schedule / Resource / External / Scope / Organizational]
**Risk Owner**: [Name, Title]
**Date Identified**: [YYYY-MM-DD]
**Review Date**: [YYYY-MM-DD]

#### Current Assessment

**Probability**: [1-5] - [Rare / Unlikely / Possible / Likely / Almost Certain]
**Rationale**: [Why this probability? Historical data, assumptions, conditions]

**Impact**: [1-5] - [Minimal / Minor / Moderate / Major / Severe]
**Breakdown**:
- Schedule Impact: [1-5] - [Delay estimate: X days/weeks]
- Budget Impact: [1-5] - [Cost estimate: $X or X% overrun]
- Scope/Quality Impact: [1-5] - [Features/quality affected]

**Risk Score**: [Prob × Impact] - **[Priority Level]**

#### Mitigation Plan (Reduce Probability)

**Goal**: Reduce probability from [current] to [target] by [date]
**Actions**: [Action 1 - Owner, Deadline] | [Action 2 - Owner, Deadline] | [Action 3 - Owner, Deadline]
**Investment**: [Time, budget, resources] | **Expected Reduction**: Prob [X]→[Y], Score: [new]

#### Contingency Plan (Reduce Impact If Occurs)

**Triggers**: [Trigger 1] | [Trigger 2] | [Trigger 3] (specific, measurable indicators)
**Actions**: Immediate: [Action - Owner] | Short-term: [Action - Owner] | Long-term: [Action - Owner]
**Backup Resources**: People: [Names] | Budget: [$X] | Time: [X days] | Alternatives: [Options]

#### Monitoring Plan

**Review**: [Frequency] | **Next Review**: [Date]
**Leading Indicators**: [Metric 1: Current/Threshold] | [Metric 2: Current/Threshold] | [Metric 3: Current/Threshold]
**Actions**: [Who monitors, escalation path]

#### Change Log

| Date | Change | New Prob | New Impact | New Score | Reason |
|------|--------|----------|------------|-----------|--------|
| [YYYY-MM-DD] | Initial assessment | [X] | [Y] | [X×Y] | Risk identified |
| [YYYY-MM-DD] | Updated probability | [X] | [Y] | [X×Y] | [Mitigation action completed] |
| [YYYY-MM-DD] | Risk closed | - | - | - | [Reason risk no longer relevant] |

---

## Risk Monitoring Log Template

Copy this section to track risk evolution over time:

### Risk Monitoring Log

**Reporting Period**: [Week/Month of YYYY-MM-DD]
**Project Status**: [On Track / At Risk / Off Track]
**Overall Risk Profile**: [Improving / Stable / Deteriorating]

#### New Risks Identified This Period

| ID | Risk | Category | Prob | Impact | Score | Owner |
|----|------|----------|------|--------|-------|-------|
| R-XXX | [New risk] | [Cat] | [1-5] | [1-5] | [P×I] | [Name] |

#### Risks Closed This Period

| ID | Risk | Closure Reason | Closure Date |
|----|------|----------------|--------------|
| R-XXX | [Risk description] | [Mitigated / No longer relevant / Accepted] | [YYYY-MM-DD] |

#### Risk Score Changes

| ID | Risk | Old Score | New Score | Change | Reason |
|----|------|-----------|-----------|--------|--------|
| R-XXX | [Risk] | [Old P×I] | [New P×I] | [+/- X] | [Why probability/impact changed] |

#### Critical/High Risk Updates

**R-XXX: [Risk Title]** (Score: [X], Priority: [Critical/High])
- **Status**: [In Mitigation / Monitoring / Escalated]
- **Progress This Period**: [What mitigation actions completed, what's next]
- **Probability/Impact Change**: [Why scores changed]
- **Blockers/Issues**: [Anything preventing mitigation progress]
- **Next Actions**: [What's happening next review period]

**R-XXX: [Another Critical/High Risk]** (Score: [X], Priority: [Critical/High])
- [Same structure]

#### Top 5 Risks (by Score)

1. **R-XXX** ([Score]): [Risk description] - [Status update]
2. **R-XXX** ([Score]): [Risk description] - [Status update]
3. **R-XXX** ([Score]): [Risk description] - [Status update]
4. **R-XXX** ([Score]): [Risk description] - [Status update]
5. **R-XXX** ([Score]): [Risk description] - [Status update]

#### Risk Profile Trend

| Metric | This Period | Last Period | Trend |
|--------|-------------|-------------|-------|
| Total Active Risks | [X] | [Y] | [↑/↓/→] |
| Critical Risks (≥20) | [X] | [Y] | [↑/↓/→] |
| High Risks (12-19) | [X] | [Y] | [↑/↓/→] |
| Medium Risks (6-11) | [X] | [Y] | [↑/↓/→] |
| Low Risks (1-5) | [X] | [Y] | [↑/↓/→] |
| Average Risk Score | [X.X] | [Y.Y] | [↑/↓/→] |

**Trend Analysis**: [Is risk profile improving (scores decreasing) or deteriorating (scores increasing)? Why?]

#### Actions Required

- [ ] **Action 1**: [Specific action needed] - Owner: [Name], Deadline: [Date]
- [ ] **Action 2**: [Another action] - Owner: [Name], Deadline: [Date]
- [ ] **Action 3**: [Another action] - Owner: [Name], Deadline: [Date]

#### Escalations

**[Risk ID]**: [Risk requiring executive/stakeholder escalation]
**Reason for Escalation**: [Why escalating - Critical score, budget needed, decision required]
**Action Requested**: [What we need from stakeholders]
**Escalated To**: [Name, Title]
**Escalation Date**: [YYYY-MM-DD]

---

## Guidance for Each Section

### Guidance: Risk Identification

**Structured brainstorming by category:**

**Technical**: New technology? Dependencies? Performance assumptions? Complexity? Security/compliance gaps?
**Schedule**: Dependencies? Estimate uncertainty? Scope creep? Resource unavailability? External deadlines?
**Resource**: Single points of failure (people)? Budget assumptions? Critical vendors? Equipment? Skill gaps?
**External**: Regulatory changes? Competitor actions? Economic shifts? Force majeure? Stakeholder changes?
**Scope**: Unclear requirements? Conflicting priorities? Feature expansion? Gold-plating? Wrong user assumptions?
**Organizational**: Exec support? Competing projects? Funding security? Restructuring? Political conflicts?

### Guidance: Scoring

**Probability**: Use base rates (how often?), reference class (last time?), expert input, historical data. Avoid overconfidence.
**Impact**: Schedule (% delay), Budget (% overrun), Scope (features cut). Use maximum dimension or weighted average.
**Common mistakes**: Conflating prob/impact, anchoring bias, optimism bias, availability bias.
**Calibration**: Score 3-5 reference risks as group, use as anchors for comparison.

### Guidance: Response Planning

**Mitigation** (reduce probability before): Specific, measurable, owned, deadlined, scoped actions.
**Contingency** (reduce impact if occurs): Backup plans with specific, measurable triggers.
**Priority**: Critical (≥20): Full plan + weekly review | High (12-19): Full plan + bi-weekly | Medium (6-11): Light plan + monthly | Low (1-5): Accept

---

## Quick Patterns

### By Project Phase

**Kickoff (Week 1)**:
- Focus: Identify comprehensive risk baseline (20-40 risks typical)
- Many risks at Medium score (uncertainty high, no mitigation yet)
- Action: Full risk workshop with stakeholders

**Planning (Weeks 2-4)**:
- Focus: Develop mitigation plans for High/Critical risks
- Action: Assign owners, define mitigations, schedule mitigation work into project plan

**Execution (Mid-Project)**:
- Focus: Monitor risk evolution, add new risks as discovered
- Expect: Critical risks mitigated to Medium/Low, new integration/dependency risks emerge
- Action: Weekly review of High/Critical risks, monthly full register review

**Near Completion (Final Weeks)**:
- Focus: New "last-minute surprise" risks, launch risks
- Expect: Mostly Low risks (issues resolved), few High (deployment, cutover, training)
- Action: Daily check-in on Critical risks, prepare rollback contingencies

### By Project Type

**Software Migration/Upgrade**:
- Key risks: Data corruption, downtime, rollback complexity, user adoption
- Mitigations: Pilot migration, automated testing, phased rollout, extensive rollback testing
- Contingencies: Full rollback plan, extended downtime window, manual workarounds

**New Product Launch**:
- Key risks: Market demand lower than expected, competitor launch first, supply chain delay
- Mitigations: Customer interviews, MVP testing, multiple suppliers, buffer inventory
- Contingencies: Pricing flexibility, pivoted positioning, delayed launch

**Organizational Change**:
- Key risks: Employee resistance, communication breakdown, insufficient training
- Mitigations: Change management program, stakeholder engagement, pilot groups
- Contingencies: Extended transition period, additional support resources, rollback to old process

---

## Quality Checklist

Before finalizing, verify:

**Risk Identification Quality:**
- [ ] Identified 15-30 risks (if <10, incomplete; if >50, probably too granular)
- [ ] Risks span all categories (technical, schedule, resource, external, scope, org - not just one category)
- [ ] Risks are specific (not vague like "things might not work")
- [ ] Risks describe what could go wrong, not symptoms (root cause level)

**Risk Assessment Quality:**
- [ ] All risks scored on probability (1-5) and impact (1-5)
- [ ] Risk scores differentiated (not all 6-9; use full 1-25 range)
- [ ] Scoring rationale documented for High/Critical risks
- [ ] Subject matter experts involved in scoring (not solo effort)
- [ ] Probability and impact assessed independently (not conflated)

**Risk Prioritization Quality:**
- [ ] Risk matrix plotted (visual representation of risk profile)
- [ ] Critical risks (≥20) escalated to stakeholders
- [ ] High risks (12-19) have detailed response plans
- [ ] Medium/Low risks not over-managed (accept or lightweight mitigation)

**Risk Response Quality:**
- [ ] All High/Critical risks have named owners (not "team")
- [ ] Mitigation plans are specific, measurable, owned, deadlined
- [ ] Contingency plans exist for High/Critical risks (backup if mitigation fails)
- [ ] Contingency triggers are quantifiable (not vague)
- [ ] Investment in mitigation/contingency is reasonable (cost vs risk reduction)

**Risk Monitoring Quality:**
- [ ] Review frequency defined (weekly for active, monthly for longer projects)
- [ ] Leading indicators identified for High/Critical risks (early warnings)
- [ ] Monitoring log tracks risk evolution (new risks, closed risks, score changes)
- [ ] Risk profile trend analyzed (improving/stable/deteriorating)

**Common Red Flags:**
- ❌ <10 risks identified (incomplete risk picture)
- ❌ All risks scored 6-9 (not differentiated, unclear priorities)
- ❌ No risk owners assigned (diffused accountability)
- ❌ Only mitigation, no contingencies (no backup plans)
- ❌ Contingencies with vague triggers ("when things get bad")
- ❌ Created once, never updated (stale, false confidence)
- ❌ Risk register disconnected from project plan (not actionable)

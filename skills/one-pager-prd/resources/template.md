# One-Pager PRD Template

## Quick Start

**One-Pager (1 page):** For simple features needing quick approval. Bullet points, high-level.
**PRD (1-2 pages):** For complex features needing detailed requirements. More flows, edge cases, phasing.

---

## Option A: One-Pager Template

### [Feature/Product Name]

**Date:** [YYYY-MM-DD]
**Author:** [Name]
**Stakeholders:** [PM, Eng Lead, Design Lead, etc.]
**Status:** [Draft / Review / Approved]

---

### Problem

**What user pain are we solving?**
- [Describe specific user problem with evidence]
- [Quantify the pain: how many users, how often, impact]
- [Why this matters: business/user value]

**Why now?**
- [Timing rationale: competitive pressure, strategic priority, market shift]

**Supporting Data:**
- [User research / Analytics / Support tickets / Competitive analysis]

---

### Solution

**What are we building?**
- [High-level approach in 1-3 sentences]
- [Key capabilities without over-specifying how]

**How it works (user perspective):**
1. [User action 1]
2. [System response 1]
3. [User action 2]
4. [Outcome]

---

### Users

**Who benefits?**
- **Primary:** [Persona name] ([% of users]) - [Use case]
- **Secondary:** [Persona name] ([% of users]) - [Use case]

**Key Use Cases:**
1. [Use case 1]: [Description]
2. [Use case 2]: [Description]

---

### Goals & Metrics

**Success Metrics:**
- **Primary:** [Metric name] - Baseline: [X], Target: [Y], Timeline: [Z]
- **Secondary:** [Metric name] - Baseline: [X], Target: [Y], Timeline: [Z]

**Leading Indicators:**
- [Early signal 1]: [Target]
- [Early signal 2]: [Target]

---

### Scope

**In Scope (MVP):**
- [Must-have 1]
- [Must-have 2]
- [Must-have 3]

**Out of Scope (Future):**
- [Nice-to-have 1] - Reason: [Why not now]
- [Nice-to-have 2] - Reason: [Why not now]

**Key User Flows:**
- **Happy Path:** [Flow description]
- **Edge Cases:** [How we handle X, Y, Z]

---

### Constraints

**Technical:**
- [Constraint 1]: [Impact]
- [Dependency 1]: [On what, when available]

**Business:**
- [Budget / Timeline / Resource limit]

**Assumptions:**
- [Key assumption 1]
- [Key assumption 2]

---

### Open Questions

1. **[Question 1]:** [Context] - Decision needed by: [Date]
2. **[Question 2]:** [Context] - Decision needed by: [Date]

---

### Next Steps

- [ ] [Stakeholder review]: [By when]
- [ ] [Design mockups]: [By when]
- [ ] [Technical spike]: [By when]
- [ ] [Final approval]: [By when]
- [ ] [Kickoff]: [Target date]

---

## Option B: Full PRD Template

### [Feature/Product Name]

**Document Info:**
- **Date:** [YYYY-MM-DD]
- **Author:** [Name]
- **Status:** [Draft / Review / Approved / In Development]
- **Version:** [1.0]
- **Last Updated:** [Date]

**Stakeholders:**
- **PM:** [Name]
- **Engineering:** [Name]
- **Design:** [Name]
- **Other:** [Legal, Compliance, Marketing, etc.]

---

## 1. Overview

### 1.1 Executive Summary
[2-3 sentence summary: Problem → Solution → Impact]

### 1.2 Problem Statement

**User Pain:**
[Detailed description of user problem]

**Impact:**
- [Quantified impact: time wasted, revenue lost, churn risk]
- [How many users affected]
- [Frequency of problem]

**Evidence:**
- [User interview quotes]
- [Analytics data]
- [Support ticket volume]
- [Competitive benchmarks]

**Why Now:**
[Strategic timing, competitive pressure, market opportunity]

### 1.3 Goals

**Business Goals:**
- [Revenue / Retention / Market share / Competitive parity]

**User Goals:**
- [What user wants to accomplish]

**Success Metrics:**

| Metric | Baseline | Target | Timeline | Measurement |
|--------|----------|--------|----------|-------------|
| [Primary metric] | [Current] | [Goal] | [When] | [How measured] |
| [Secondary metric] | [Current] | [Goal] | [When] | [How measured] |

**Leading Indicators:**
- [Early signal 1]: [How it predicts success]
- [Early signal 2]: [How it predicts success]

---

## 2. Users & Use Cases

### 2.1 User Personas

**Primary Persona: [Name]**
- **Profile:** [Demographics, role, technical proficiency]
- **Goals:** [What they want to achieve]
- **Pain Points:** [Current frustrations]
- **Motivation:** [Why they'd use this feature]
- **Usage:** [% of user base, frequency]

**Secondary Persona: [Name]**
[Same structure]

### 2.2 Use Cases

**Use Case 1: [Name]**
- **Actor:** [Primary persona]
- **Goal:** [What they want to do]
- **Preconditions:** [What must be true before]
- **Flow:**
  1. [User action]
  2. [System response]
  3. [User action]
  4. [Outcome]
- **Success Criteria:** [How user knows it worked]

**Use Case 2: [Name]**
[Same structure]

**Use Case 3: [Name]**
[Same structure]

---

## 3. Solution

### 3.1 Overview
[High-level description of what we're building]

### 3.2 Key User Flows

**Flow 1: [Happy Path]**
1. [User action] → [System response]
2. [User action] → [System response]
3. [Outcome]

**Flow 2: [Alternative/Error]**
[Trigger] → [Handling] → [User sees]

### 3.3 Functional Requirements

**Must-Have (MVP):**
1. [Requirement]: [Description + rationale]
2. [Requirement]: [Description + rationale]

**Post-MVP:**
1. [Requirement]: [Why v2]

**Out of Scope:**
1. [Explicitly excluded]: [Reason]

### 3.4 Non-Functional Requirements
- **Performance:** [Targets]
- **Scalability:** [Limits]
- **Security:** [Requirements]
- **Accessibility:** [WCAG level]
- **Compatibility:** [Browsers/devices]

---

## 4. Design & Experience
- **Navigation:** [Where feature lives in product]
- **Key Screens:** [Screen 1], [Screen 2], [Empty/Loading/Error states]
- **Interactions:** [Buttons, forms, modals, etc.]
- **Copy:** Feature name, onboarding, help text, error messages

---

## 5. Technical Considerations
- **Architecture:** [High-level approach]
- **Dependencies:** Internal [systems], External [vendors]
- **Data Model:** [Key entities, storage]
- **APIs:** [If exposing/integrating]
- **Migration:** [If replacing existing]
- **Constraints:** [Limits, rates]

---

## 6. Go-to-Market
- **Launch:** Beta [when], Rollout [gradual/full], Sunset [if applicable]
- **Marketing:** Positioning, target audience, channels
- **Sales:** [B2B enablement materials]
- **Support:** Help docs, training, FAQ

---

## 7. Risks & Mitigation

| Risk | Impact | Probability | Mitigation | Owner |
|------|--------|-------------|------------|-------|
| [Risk 1] | [High/Med/Low] | [High/Med/Low] | [How we reduce/handle] | [Name] |
| [Risk 2] | [High/Med/Low] | [High/Med/Low] | [How we reduce/handle] | [Name] |

---

## 8. Open Questions & Decisions

| Question | Options | Decision | Decider | Deadline |
|----------|---------|----------|---------|----------|
| [Question 1] | [Option A, B, C] | [TBD / Decided] | [Who] | [Date] |
| [Question 2] | [Option A, B] | [TBD / Decided] | [Who] | [Date] |

---

## 9. Timeline & Milestones
- **Discovery:** User research [date], mockups [date], spike [date]
- **Development:** Kickoff [date], alpha [date], beta [date]
- **Launch:** Full launch [date], review [date]
- **Dependencies:** [Blockers and when resolved]

---

## 10. Success Criteria
- **Launch Criteria:** Functional reqs met, performance benchmarks, security review, docs complete
- **Monitoring:** Week 1 [metrics], Month 1 [adoption/retention], Quarter 1 [business impact]
- **Success:** [Metric 1] reaches [target], [Metric 2] reaches [target]

---

## Appendix
- **Research:** [Links]
- **Design:** [Links]
- **Technical:** [Links]
- **Related:** [Links]

---

## Quality Checklist
- [ ] Problem: Specific, evidenced, quantified impact, "why now"
- [ ] Solution: Clear high-level, not over-specified, key flows, edge cases
- [ ] Users: Personas with %, realistic use cases
- [ ] Metrics: Measurable, baselines + targets, leading indicators
- [ ] Scope: In/out clear, MVP vs future defined
- [ ] Constraints: Technical, business, dependencies identified
- [ ] Open Questions: Surfaced with timelines and deciders
- [ ] Overall: Appropriate length (1-2 pages), scannable, jargon-free, stakeholder review

---

## Tips by Context
- **New Feature:** Fits existing flows, adoption strategy. Keep brief.
- **New Product:** Vision, market opportunity, differentiation. More detail.
- **Technical:** Performance gains, cost savings, risk reduction. Translate to user/business value.
- **Experiment:** Hypothesis, success criteria, rollback plan. Stay flexible.
- **Internal Tool:** Efficiency gains, time saved. Include end users (employees).

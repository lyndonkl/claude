# Deliberation, Debate & Red Teaming Template

## Workflow

Copy this checklist and track your progress:

```
Red Teaming Progress:
- [ ] Step 1: Proposal definition and context
- [ ] Step 2: Adversarial role assignment
- [ ] Step 3: Critique generation
- [ ] Step 4: Risk assessment and prioritization
- [ ] Step 5: Mitigation recommendations
```

**Step 1: Proposal definition** - Define what we're evaluating, stakes, constraints. See [Proposal Definition](#proposal-definition).

**Step 2: Adversarial role assignment** - Choose 3-5 critical perspectives. See [Role Assignment](#role-assignment).

**Step 3: Critique generation** - For each role, generate specific challenges. See [Critique Generation](#critique-generation).

**Step 4: Risk assessment** - Score risks by severity × likelihood. See [Risk Assessment](#risk-assessment).

**Step 5: Mitigation recommendations** - Propose fixes for critical risks. See [Mitigation Recommendations](#mitigation-recommendations).

---

## Proposal Definition

### Input Template

```markdown
## Proposal Under Review

**Title:** [Concise name of proposal]

**Description:** [1-3 sentences explaining what we're proposing to do]

**Goal:** [Why are we doing this? What problem does it solve?]

**Stakeholders:**
- **Proposer:** [Who is advocating for this]
- **Decision maker:** [Who has final authority]
- **Affected parties:** [Who will be impacted]

**Stakes:**
- **If successful:** [Upside, benefits]
- **If fails:** [Downside, worst case]
- **Reversibility:** [Can we undo this? At what cost?]

**Timeline:**
- **Decision deadline:** [When must we decide]
- **Implementation timeline:** [When would this happen]
- **Cost of delay:** [What do we lose by waiting]

**Current confidence:** [Team's current belief this is the right decision, 0-100%]

**Prior analysis:** [What vetting has been done already]
```

---

## Role Assignment

### Role Selection Guide

**Choose 3-5 adversarial roles most likely to expose blind spots for this specific proposal.**

**For product/feature launches:**
- Customer (user friction)
- Operations (reliability, maintenance)
- Competitor (market positioning)
- Legal/Privacy (compliance)

**For technical/architecture decisions:**
- Security (attack vectors)
- Operations (operability, debugging)
- Engineer (technical debt, complexity)
- Long-term Thinker (future costs)

**For strategy/business decisions:**
- Competitor (market response)
- Finance (hidden costs, ROI assumptions)
- Contrarian (challenge core assumptions)
- Long-term Thinker (second-order effects)

**For policy/process changes:**
- Affected User (workflow disruption)
- Operations (enforcement burden)
- Legal/Compliance (regulatory risk)
- Investigative Journalist (PR risk)

### Role Assignment Template

```markdown
## Adversarial Roles

**Role 1: [Role Name]** (e.g., Security / Malicious Actor)
- **Perspective:** [What are this role's incentives and concerns?]
- **Key question:** [What would this role be most worried about?]

**Role 2: [Role Name]** (e.g., Customer)
- **Perspective:** [What does this role care about?]
- **Key question:** [What friction or cost does this create for them?]

**Role 3: [Role Name]** (e.g., Operations)
- **Perspective:** [What operational burden does this create?]
- **Key question:** [What breaks at 2am?]

**Role 4: [Role Name]** (optional)
- **Perspective:**
- **Key question:**

**Role 5: [Role Name]** (optional)
- **Perspective:**
- **Key question:**
```

---

## Critique Generation

### Critique Framework

For each assigned role, answer these questions:

**1. What could go wrong?**
- Failure modes from this perspective
- Edge cases that break the proposal
- Unintended consequences

**2. What assumptions are questionable?**
- Optimistic estimates (timeline, cost, adoption)
- Unvalidated beliefs (market demand, technical feasibility)
- Hidden dependencies

**3. What are we missing?**
- Gaps in analysis
- Stakeholders not considered
- Alternative approaches not evaluated

**4. What happens under stress?**
- How does this fail under load, pressure, or adversarial conditions?
- What cascading failures could occur?

### Critique Template (Per Role)

```markdown
### Critique from [Role Name]

**What could go wrong:**
1. [Specific failure mode]
2. [Edge case that breaks this]
3. [Unintended consequence]

**Questionable assumptions:**
1. [Optimistic estimate: e.g., "assumes 80% adoption but no user testing"]
2. [Unvalidated belief: e.g., "assumes competitors won't respond"]
3. [Hidden dependency: e.g., "requires Team X to deliver by date Y"]

**What we're missing:**
1. [Gap in analysis: e.g., "no security review"]
2. [Unconsidered stakeholder: e.g., "impact on support team not assessed"]
3. [Alternative not evaluated: e.g., "could achieve same goal with lower-risk approach"]

**Stress test scenarios:**
1. [High load: e.g., "What if usage is 10x expected?"]
2. [Adversarial: e.g., "What if competitor launches similar feature first?"]
3. [Cascading failure: e.g., "What if dependency X goes down?"]

**Severity assessment:** [Critical / High / Medium / Low / Trivial]
**Likelihood assessment:** [Very Likely / Likely / Possible / Unlikely / Rare]
```

### Multi-Role Synthesis Template

```markdown
## Critique Summary (All Roles)

**Themes across roles:**
- **Security/Privacy:** [Cross-role security concerns]
- **Operations/Reliability:** [Operational risks raised by multiple roles]
- **Customer Impact:** [User friction points]
- **Financial:** [Cost or ROI concerns]
- **Legal/Compliance:** [Regulatory or liability issues]
- **Technical Feasibility:** [Implementation challenges]

**Showstopper risks** (mentioned by multiple roles or rated Critical):
1. [Risk that appeared in multiple critiques or scored ≥15]
2. [Another critical cross-cutting concern]
```

---

## Risk Assessment

### Risk Scoring Process

**For each risk identified in critiques:**

1. **Assess Severity (1-5):**
   - 5 = Critical (catastrophic failure)
   - 4 = High (major damage)
   - 3 = Medium (moderate impact)
   - 2 = Low (minor inconvenience)
   - 1 = Trivial (negligible)

2. **Assess Likelihood (1-5):**
   - 5 = Very Likely (>80%)
   - 4 = Likely (50-80%)
   - 3 = Possible (20-50%)
   - 2 = Unlikely (5-20%)
   - 1 = Rare (<5%)

3. **Calculate Risk Score:** Severity × Likelihood

4. **Categorize:**
   - ≥15: Showstopper (must fix)
   - 10-14: High Priority (should address)
   - 5-9: Monitor (accept with contingency)
   - <5: Accept (acknowledge)

### Risk Assessment Template

```markdown
## Risk Register

| # | Risk Description | Source Role | Severity | Likelihood | Score | Category | Priority |
|---|-----------------|-------------|----------|------------|-------|----------|----------|
| 1 | [Specific risk] | [Role] | [1-5] | [1-5] | [Score] | [Showstopper/High/Monitor/Accept] | [1/2/3] |
| 2 | [Specific risk] | [Role] | [1-5] | [1-5] | [Score] | [Category] | [Priority] |
| 3 | [Specific risk] | [Role] | [1-5] | [1-5] | [Score] | [Category] | [Priority] |

**Showstoppers (Score ≥ 15):**
- [List all must-fix risks]

**High Priority (Score 10-14):**
- [List should-address risks]

**Monitored (Score 5-9):**
- [List accept-with-contingency risks]

**Accepted (Score < 5):**
- [List acknowledged low-risk items]
```

---

## Mitigation Recommendations

### Mitigation Strategy Selection

For each risk, choose appropriate mitigation:

**Showstoppers:** Must be addressed before proceeding
- **Revise:** Change the proposal to eliminate risk
- **Safeguard:** Add controls to reduce likelihood
- **Reduce scope:** Limit blast radius (gradual rollout, pilot)
- **Delay:** Gather more data or wait for conditions to improve

**High Priority:** Should address or have strong plan
- **Safeguard:** Add monitoring, rollback capability
- **Contingency:** Have plan B ready
- **Reduce scope:** Phase implementation
- **Monitor:** Track closely with trigger for action

**Monitor:** Accept with contingency
- **Monitor:** Set up alerts/metrics
- **Contingency:** Have fix ready but don't implement preemptively

**Accept:** Acknowledge and move on
- **Document:** Note risk for awareness
- **No action:** Proceed as planned

### Mitigation Template

```markdown
## Mitigation Plan

### Showstopper Risks (Must Address)

**Risk 1: [Description]** (Score: [XX], S: [X], L: [X])
- **Strategy:** [Revise / Safeguard / Reduce Scope / Delay]
- **Actions:** [1. Concrete action, 2. Another action, 3. Measurement]
- **Owner:** [Who] | **Deadline:** [When] | **Success:** [How we know it's mitigated]

**Risk 2: [Description]** (Score: [XX])
[Same structure]

### High Priority Risks (Should Address)

**Risk 3: [Description]** (Score: [XX])
- **Strategy:** [Safeguard / Contingency / Reduce Scope / Monitor]
- **Actions:** [1. Action, 2. Monitoring setup]
- **Owner:** [Who] | **Deadline:** [When]

### Monitored Risks

**Risk 4: [Description]** (Score: [XX])
- **Metrics:** [Track] | **Alert:** [Threshold] | **Contingency:** [Action if manifests]

### Accepted Risks

**Risk 5: [Description]** (Score: [XX]) - [Rationale for acceptance]
```

### Revised Proposal Template

```markdown
## Revised Proposal

**Original Proposal:**
[Brief summary of what was originally proposed]

**Key Changes Based on Red Team:**
1. [Change based on showstopper risk X]
2. [Safeguard added for high-priority risk Y]
3. [Scope reduction for risk Z]

**New Implementation Plan:**
- **Phase 1:** [Revised timeline, reduced scope, or pilot approach]
- **Phase 2:** [Gradual expansion if Phase 1 succeeds]
- **Rollback Plan:** [How we undo if something goes wrong]

**Updated Risk Profile:**
- **Showstoppers remaining:** [None / X issues pending resolution]
- **High-priority risks with mitigation:** [List with brief mitigation]
- **Monitoring plan:** [Key metrics and thresholds]

**Recommendation:**
- [ ] **Proceed** - All showstoppers addressed, high-priority risks mitigated
- [ ] **Proceed with caution** - Some high-priority risks remain, monitoring required
- [ ] **Delay** - Showstoppers unresolved, gather more data
- [ ] **Cancel** - Risks too high even with mitigations, pursue alternative
```

---

## Quality Checklist

Before delivering red team analysis, verify:

**Critique quality:**
- [ ] Each role provides specific, realistic critiques (not strawman arguments)
- [ ] Critiques identify failure modes, questionable assumptions, gaps, and stress scenarios
- [ ] At least 3 roles provide independent perspectives
- [ ] Critiques are adversarial but constructive (steelman, not strawman)

**Risk assessment:**
- [ ] All identified risks have severity and likelihood ratings
- [ ] Risk scores calculated correctly (Severity × Likelihood)
- [ ] Showstoppers clearly flagged (score ≥ 15)
- [ ] Risk categories assigned (Showstopper/High/Monitor/Accept)

**Mitigation quality:**
- [ ] Every showstopper has specific mitigation plan
- [ ] High-priority risks either mitigated or explicitly accepted with rationale
- [ ] Mitigations are concrete (not vague like "be careful")
- [ ] Responsibility and deadlines assigned for showstopper mitigations

**Revised proposal:**
- [ ] Changes clearly linked to risks identified in red team
- [ ] Implementation plan updated (phasing, rollback, monitoring)
- [ ] Recommendation made (Proceed / Proceed with caution / Delay / Cancel)
- [ ] Rationale provided for recommendation

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| **Strawman critiques** (weak arguments) | Make critiques realistic. If real attacker wouldn't make this argument, don't use it. |
| **Missing critical perspectives** | Identify who has most to lose. Include those roles. |
| **No prioritization** (all risks equal) | Use severity × likelihood matrix. Not everything is showstopper. |
| **Vague mitigations** ("be careful") | Make concrete, measurable, with owners and deadlines. |
| **Red team as rubber stamp** | Genuinely seek to break proposal. If nothing found, critique wasn't adversarial enough. |
| **Defensive response** | Red team's job is to find problems. Fix or accept risk, don't dismiss. |
| **Analysis paralysis** | Time-box red team (1-2 sessions). Focus on showstoppers. |
| **Ignoring culture** | Calibrate tone. Some teams prefer "curious questions" over "aggressive challenges." |

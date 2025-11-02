# Chain Spec Risk Metrics Template

## Workflow

Copy this checklist and track your progress:

```
Chain Spec Risk Metrics Progress:
- [ ] Step 1: Gather initiative context
- [ ] Step 2: Write comprehensive specification
- [ ] Step 3: Conduct premortem and build risk register
- [ ] Step 4: Define success metrics and instrumentation
- [ ] Step 5: Validate completeness and deliver
```

**Step 1: Gather initiative context** - Collect goal, constraints, stakeholders, baseline, desired outcomes. See [Context Questions](#context-questions).

**Step 2: Write comprehensive specification** - Document scope, approach, requirements, dependencies, timeline. See [Quick Template](#quick-template) and [Specification Guidance](#specification-guidance).

**Step 3: Conduct premortem and build risk register** - Run failure imagination exercise, categorize risks, assign mitigations/owners. See [Premortem Process](#premortem-process) and [Risk Register Template](#risk-register-template).

**Step 4: Define success metrics** - Identify leading/lagging indicators, baselines, targets, counter-metrics. See [Metrics Template](#metrics-template) and [Instrumentation Guidance](#instrumentation-guidance).

**Step 5: Validate and deliver** - Self-check with rubric (≥3.5 average), ensure all components align. See [Quality Checklist](#quality-checklist).

## Quick Template

```markdown
# [Initiative Name]: Spec, Risks, Metrics

## 1. Specification

### 1.1 Executive Summary
- **Goal**: [What are you building/changing and why?]
- **Timeline**: [When does this need to be delivered?]
- **Stakeholders**: [Who cares about this initiative?]
- **Success Criteria**: [What does done look like?]

### 1.2 Current State (Baseline)
- [Describe the current state/system]
- [Key metrics/data points about current state]
- [Pain points or limitations driving this initiative]

### 1.3 Proposed Approach
- **Architecture/Design**: [High-level approach]
- **Implementation Plan**: [Phases, milestones, dependencies]
- **Technology Choices**: [Tools, frameworks, platforms with rationale]

### 1.4 Scope
- **In Scope**: [What this initiative includes]
- **Out of Scope**: [What is explicitly excluded]
- **Future Considerations**: [What might come later]

### 1.5 Requirements
**Functional Requirements:**
- [Feature/capability 1]
- [Feature/capability 2]
- [Feature/capability 3]

**Non-Functional Requirements:**
- **Performance**: [Latency, throughput, scalability targets]
- **Reliability**: [Uptime, error rates, recovery time]
- **Security**: [Authentication, authorization, data protection]
- **Compliance**: [Regulatory, policy, audit requirements]

### 1.6 Dependencies & Assumptions
- **Dependencies**: [External teams, systems, resources needed]
- **Assumptions**: [What we're assuming is true]
- **Constraints**: [Budget, time, resource, technical limitations]

### 1.7 Timeline & Milestones
| Milestone | Date | Deliverable |
|-----------|------|-------------|
| [Phase 1] | [Date] | [What's delivered] |
| [Phase 2] | [Date] | [What's delivered] |
| [Phase 3] | [Date] | [What's delivered] |

## 2. Risk Analysis

### 2.1 Premortem Summary
**Exercise Prompt**: "It's [X months] from now. This initiative failed catastrophically. What went wrong?"

**Top failure modes identified:**
1. [Failure mode 1]
2. [Failure mode 2]
3. [Failure mode 3]
4. [Failure mode 4]
5. [Failure mode 5]

### 2.2 Risk Register

| Risk ID | Risk Description | Category | Likelihood | Impact | Risk Score | Mitigation Strategy | Owner | Status |
|---------|-----------------|----------|------------|--------|-----------|---------------------|-------|--------|
| R1 | [Specific failure scenario] | Technical | High | High | 9 | [How you'll prevent/reduce] | [Name] | Open |
| R2 | [Specific failure scenario] | Operational | Medium | High | 6 | [How you'll prevent/reduce] | [Name] | Open |
| R3 | [Specific failure scenario] | Organizational | Medium | Medium | 4 | [How you'll prevent/reduce] | [Name] | Open |
| R4 | [Specific failure scenario] | External | Low | High | 3 | [How you'll prevent/reduce] | [Name] | Open |

**Risk Scoring**: Low=1, Medium=2, High=3. Risk Score = Likelihood × Impact.

**Risk Categories**:
- **Technical**: Architecture, code quality, infrastructure, performance
- **Operational**: Processes, runbooks, support, operations
- **Organizational**: Resources, skills, alignment, communication
- **External**: Market, vendors, regulation, dependencies

### 2.3 Risk Mitigation Timeline
- **Pre-Launch**: [Risks to mitigate before going live]
- **Launch Window**: [Monitoring and safeguards during launch]
- **Post-Launch**: [Ongoing monitoring and response]

## 3. Success Metrics

### 3.1 Leading Indicators (Early Signals)
| Metric | Baseline | Target | Measurement Method | Tracking Cadence | Owner |
|--------|----------|--------|-------------------|------------------|-------|
| [Predictive metric 1] | [Current value] | [Goal value] | [How measured] | [How often] | [Name] |
| [Predictive metric 2] | [Current value] | [Goal value] | [How measured] | [How often] | [Name] |
| [Predictive metric 3] | [Current value] | [Goal value] | [How measured] | [How often] | [Name] |

**Examples**: Deployment frequency, code review cycle time, test coverage, incident detection time

### 3.2 Lagging Indicators (Outcome Measures)
| Metric | Baseline | Target | Measurement Method | Tracking Cadence | Owner |
|--------|----------|--------|-------------------|------------------|-------|
| [Outcome metric 1] | [Current value] | [Goal value] | [How measured] | [How often] | [Name] |
| [Outcome metric 2] | [Current value] | [Goal value] | [How measured] | [How often] | [Name] |
| [Outcome metric 3] | [Current value] | [Goal value] | [How measured] | [How often] | [Name] |

**Examples**: Uptime, user adoption rate, revenue impact, customer satisfaction score

### 3.3 Counter-Metrics (What We Won't Sacrifice)
| Metric | Threshold | Monitoring Method | Escalation Trigger |
|--------|-----------|-------------------|-------------------|
| [Protection metric 1] | [Minimum acceptable] | [How monitored] | [When to escalate] |
| [Protection metric 2] | [Minimum acceptable] | [How monitored] | [When to escalate] |
| [Protection metric 3] | [Minimum acceptable] | [How monitored] | [When to escalate] |

**Examples**: Code quality (test coverage > 80%), team morale (happiness score > 7/10), security posture (no critical vulnerabilities), user privacy (zero data leaks)

### 3.4 Success Criteria Summary
**Must-haves (hard requirements)**:
- [Critical success criterion 1]
- [Critical success criterion 2]
- [Critical success criterion 3]

**Should-haves (target achievements)**:
- [Desired outcome 1]
- [Desired outcome 2]
- [Desired outcome 3]

**Nice-to-haves (stretch goals)**:
- [Aspirational outcome 1]
- [Aspirational outcome 2]
```

## Context Questions

**Basics**: What are you building/changing? Why now? Who are the stakeholders?

**Constraints**: When does this need to be delivered? What's the budget? What resources are available?

**Current State**: What exists today? What's the baseline? What are the pain points?

**Desired Outcomes**: What does success look like? What metrics would you track? What are you most worried about?

**Scope**: Greenfield/migration/enhancement? Single or multi-phase? Who is the primary user?

## Specification Guidance

### Scope Definition

**In Scope** should be specific and concrete:
- ✅ "Migrate user authentication service to OAuth 2.0 with PKCE"
- ❌ "Improve authentication"

**Out of Scope** prevents scope creep:
- List explicitly what won't be included in this phase
- Reference future work that might address excluded items
- Example: "Out of Scope: Social login (Google/GitHub) - deferred to Phase 2"

### Requirements Best Practices

**Functional Requirements**: What the system must do
- Use "must" for requirements, "should" for preferences
- Be specific: "System must handle 10K requests/sec" not "System should be fast"
- Include acceptance criteria: How will you verify this requirement is met?

**Non-Functional Requirements**: How well the system must perform
- **Performance**: Quantify with numbers (latency < 200ms, throughput > 1000 req/s)
- **Reliability**: Define uptime SLAs, error budgets, MTTR targets
- **Security**: Specify authentication, authorization, encryption requirements
- **Scalability**: Define growth expectations (users, data, traffic)

### Timeline & Milestones

Make milestones concrete and verifiable:
- ✅ "Milestone 1 (Mar 15): Auth service deployed to staging, 100% auth tests passing"
- ❌ "Milestone 1: Complete most of auth work"

Include buffer for unknowns:
- 80% planned work, 20% buffer for issues/tech debt
- Identify critical path and dependencies clearly

## Premortem Process

### Step 1: Set the Scene

Frame the failure scenario clearly:
> "It's [6/12/24] months from now - [Date]. We launched [initiative name] and it failed catastrophically. [Stakeholders] are upset. The team is demoralized. What went wrong?"

Choose timeframe based on initiative:
- Quick launch: 3-6 months
- Major migration: 12-24 months
- Strategic change: 24+ months

### Step 2: Brainstorm Failures (Independent)

Have each stakeholder privately write 3-5 specific failure modes:
- Be specific: "Database migration lost 10K user records" not "data issues"
- Think from your domain: Engineers focus on technical, PMs on product, Ops on operational
- No filtering: List even unlikely scenarios

### Step 3: Share and Cluster

Collect all failure modes and group similar ones:
- **Technical failures**: System design, code bugs, infrastructure
- **Operational failures**: Runbooks missing, wrong escalation, poor monitoring
- **Organizational failures**: Lack of skills, poor communication, misaligned incentives
- **External failures**: Vendor issues, market changes, regulatory changes

### Step 4: Vote and Prioritize

For each cluster, assess:
- **Likelihood**: How probable is this? (Low 10-30%, Medium 30-60%, High 60%+)
- **Impact**: How bad would it be? (Low = annoying, Medium = painful, High = catastrophic)
- **Risk Score**: Likelihood × Impact (1-9 scale)

Focus mitigation on High-risk items (score 6-9).

### Step 5: Convert to Risk Register

For each significant failure mode:
1. Reframe as a risk: "Risk that [specific scenario] happens"
2. Categorize (Technical/Operational/Organizational/External)
3. Assign owner (who monitors and responds)
4. Define mitigation (how to reduce likelihood or impact)
5. Track status (Open/Mitigated/Accepted/Closed)

## Risk Register Template

### Risk Statement Format

Good risk statements are specific and measurable:
- ✅ "Risk that database migration script fails to preserve foreign key relationships, causing data integrity errors in 15% of records"
- ❌ "Risk of data issues"

### Mitigation Strategies

**Reduce Likelihood** (prevent the risk):
- Example: "Implement dry-run migration on production snapshot; verify all FK relationships before live migration"

**Reduce Impact** (limit the damage):
- Example: "Create rollback script tested on staging; set up real-time monitoring for FK violations; keep read replica as backup"

**Accept Risk** (consciously choose not to mitigate):
- For low-impact or very-low-likelihood risks
- Document why it's acceptable: "Accept risk of 3rd-party API rate limiting during launch (low likelihood, workaround available)"

**Transfer Risk** (shift to vendor/insurance):
- Example: "Use managed database service with automated backups and point-in-time recovery (transfers operational risk to vendor)"

### Risk Owners

Each risk needs a clear owner who:
- Monitors early warning signals
- Executes mitigation plans
- Escalates if risk materializes
- Updates risk status regularly

Not necessarily the person who fixes it, but the person accountable for tracking it.

## Metrics Template

### Leading Indicators (Early Signals)

These predict future success before lagging metrics move:
- **Engineering**: Deployment frequency, build time, code review cycle time, test coverage
- **Product**: Feature adoption rate, activation rate, time-to-value, engagement trends
- **Operations**: Incident detection time, MTTD, runbook execution rate, alert accuracy

Choose 3-5 leading indicators that:
1. Predict lagging outcomes (validated correlation)
2. Can be measured frequently (daily/weekly)
3. You can act on quickly (short feedback loop)

### Lagging Indicators (Outcomes)

These measure actual success but appear later:
- **Reliability**: Uptime, error rate, MTTR, SLA compliance
- **Performance**: p50/p95/p99 latency, throughput, response time
- **Business**: Revenue, user growth, retention, NPS, cost savings
- **User**: Activation rate, feature adoption, satisfaction score

Choose 3-5 lagging indicators that:
1. Directly measure initiative goals
2. Are measurable and objective
3. Stakeholders care about

### Counter-Metrics (Guardrails)

What success does NOT mean sacrificing:
- If optimizing for speed → Counter-metric: Code quality (test coverage, bug rate)
- If optimizing for growth → Counter-metric: Costs (infrastructure spend, CAC)
- If optimizing for features → Counter-metric: Technical debt (cycle time, deployment frequency)

Choose 2-3 counter-metrics to:
1. Prevent gaming the system
2. Protect long-term sustainability
3. Maintain team/user trust

## Instrumentation Guidance

**Baseline**: Measure current state before launch (✅ "p99 latency: 500ms" ❌ "API is slow"). Without baseline, you can't measure improvement.

**Targets**: Make them specific ("reduce p99 from 500ms to 200ms"), achievable (industry benchmarks), time-bound ("by Q2 end"), meaningful (tied to outcomes).

**Measurement**: Document data source, calculation method, measurement frequency, and who can access the metrics.

**Tracking Cadence**: Real-time (system health), daily (operations), weekly (product), monthly (business).

## Quality Checklist

Before delivering, verify:

**Specification Complete:**
- [ ] Goal, stakeholders, timeline clearly stated
- [ ] Current state baseline documented with data
- [ ] Scope (in/out/future) explicitly defined
- [ ] Requirements are specific and measurable
- [ ] Dependencies and assumptions listed
- [ ] Timeline has concrete milestones

**Risks Comprehensive:**
- [ ] Premortem conducted (failure imagination exercise)
- [ ] Risks span technical, operational, organizational, external
- [ ] Each risk has likelihood, impact, score
- [ ] High-risk items (6-9 score) have detailed mitigation plans
- [ ] Every risk has an assigned owner
- [ ] Risk register is prioritized by score

**Metrics Measurable:**
- [ ] 3-5 leading indicators (early signals) defined
- [ ] 3-5 lagging indicators (outcomes) defined
- [ ] 2-3 counter-metrics (guardrails) defined
- [ ] Each metric has baseline, target, measurement method
- [ ] Metrics have clear owners and tracking cadence
- [ ] Success criteria (must/should/nice-to-have) documented

**Integration:**
- [ ] Risks map to specs (e.g., technical risks tied to architecture choices)
- [ ] Metrics validate risk mitigations (e.g., measure if mitigation worked)
- [ ] Specs enable metrics (e.g., instrumentation built into design)
- [ ] All three components tell a coherent story

**Rubric Validation:**
- [ ] Self-assessed with rubric ≥ 3.5 average across all criteria
- [ ] Stakeholders can act on this artifact
- [ ] Gaps and unknowns explicitly acknowledged

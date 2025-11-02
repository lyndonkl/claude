# Chain Spec Risk Metrics Methodology

Advanced techniques for complex multi-phase programs, novel risks, and sophisticated metric frameworks.

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

**Step 1: Gather initiative context** - Collect goal, constraints, stakeholders, baseline. Use template questions plus assess complexity using [5. Complexity Decision Matrix](#5-complexity-decision-matrix).

**Step 2: Write comprehensive specification** - For multi-phase programs use [1. Advanced Specification Techniques](#1-advanced-specification-techniques) including phased rollout strategies and requirements traceability matrix.

**Step 3: Conduct premortem and build risk register** - Apply [2. Advanced Risk Assessment](#2-advanced-risk-assessment) methods including quantitative analysis, fault tree analysis, and premortem variations for comprehensive risk identification.

**Step 4: Define success metrics** - Use [3. Advanced Metrics Frameworks](#3-advanced-metrics-frameworks) such as HEART, AARRR, North Star, or SLI/SLO depending on initiative type.

**Step 5: Validate and deliver** - Ensure integration using [4. Integration Best Practices](#4-integration-best-practices) and check for [6. Anti-Patterns](#6-anti-patterns) before delivering.

## 1. Advanced Specification Techniques

### Multi-Phase Program Decomposition

**When**: Initiative is too large to execute in one phase (>6 months, >10 people, multiple systems).

**Approach**: Break into phases with clear value delivery at each stage.

**Phase Structure**:
- **Phase 0 (Discovery)**: Research, prototyping, validate assumptions
  - Deliverable: Technical spike, proof of concept, feasibility report
  - Metrics: Prototype success rate, assumption validation rate
- **Phase 1 (Foundation)**: Core infrastructure, no user-facing features yet
  - Deliverable: Platform/APIs deployed, instrumentation in place
  - Metrics: System stability, API latency, error rates
- **Phase 2 (Alpha)**: Limited rollout to internal users or pilot customers
  - Deliverable: Feature complete for target use case, internal feedback
  - Metrics: User activation, time-to-value, critical bugs
- **Phase 3 (Beta)**: Broader rollout, feature complete, gather feedback
  - Deliverable: Production-ready with known limitations
  - Metrics: Adoption rate, support tickets, performance under load
- **Phase 4 (GA)**: General availability, full feature set, scaled operations
  - Deliverable: Fully launched, documented, supported
  - Metrics: Market penetration, revenue, NPS, operational costs

**Phase Dependencies**:
- Document what each phase depends on (previous phase completion, external dependencies)
- Define phase gates (criteria to proceed to next phase)
- Include rollback plans if a phase fails

### Phased Rollout Strategies

**Canary Deployment**:
- Roll out to 1% → 10% → 50% → 100% of traffic/users
- Monitor metrics at each stage before expanding
- Automatic rollback if error rates spike

**Ring Deployment**:
- Ring 0: Internal employees (catch obvious bugs)
- Ring 1: Pilot customers (friendly users, willing to provide feedback)
- Ring 2: Early adopters (power users, high tolerance)
- Ring 3: General availability (all users)

**Feature Flags**:
- Deploy code but keep feature disabled
- Gradually enable for user segments
- A/B test impact before full rollout

**Geographic Rollout**:
- Region 1 (smallest/lowest risk) → Region 2 → Region 3 → Global
- Allows testing localization, compliance, performance in stages

### Requirements Traceability Matrix

For complex initiatives, map requirements → design → implementation → tests → risks → metrics.

| Requirement ID | Requirement | Design Doc | Implementation | Test Cases | Related Risks | Success Metric |
|----------------|-------------|------------|----------------|------------|---------------|----------------|
| REQ-001 | Auth via OAuth 2.0 | Design-Auth.md | auth-service/ | test/auth/ | R3, R7 | Auth success rate > 99.9% |
| REQ-002 | API p99 < 200ms | Design-Perf.md | gateway/ | test/perf/ | R1, R5 | p99 latency metric |

**Benefits**:
- Ensures nothing is forgotten (every requirement has tests, metrics, risk mitigation)
- Helps with impact analysis (if a risk materializes, which requirements are affected?)
- Useful for audit/compliance (trace from business need → implementation → validation)

## 2. Advanced Risk Assessment

### Quantitative Risk Analysis

**When**: High-stakes initiatives where "Low/Medium/High" risk scoring is insufficient.

**Approach**: Assign probabilities (%) and impact ($$) to risks, calculate expected loss.

**Example**:
- **Risk**: Database migration fails, requiring full rollback
- **Probability**: 15% (based on similar past migrations)
- **Impact**: $500K (3 eng-weeks × 10 engineers × $50K/year/eng + customer churn)
- **Expected Loss**: 15% × $500K = $75K
- **Mitigation Cost**: $30K (comprehensive testing, dry-run on prod snapshot)
- **Decision**: Invest $30K to mitigate (expected savings $45K)

**Three-Point Estimation** for uncertainty:
- **Optimistic**: Best-case scenario (10th percentile)
- **Most Likely**: Expected case (50th percentile)
- **Pessimistic**: Worst-case scenario (90th percentile)
- **Expected Value**: (Optimistic + 4×Most Likely + Pessimistic) / 6

### Fault Tree Analysis

**When**: Analyzing how multiple small failures combine to cause catastrophic outcome.

**Approach**: Work backward from catastrophic failure to root causes using logic gates.

**Example**: "Customer data breach"
```
[Customer Data Breach]
       ↓ (OR gate - any path causes breach)
    ┌──┴──┐
[Auth bypass] OR [DB exposed to internet]
    ↓ (AND gate - both required)
 ┌──┴──┐
[SQL injection] AND [No input validation]
```

**Insights**:
- Identify single points of failure (only one thing has to go wrong)
- Reveal defense-in-depth opportunities (add redundant protections)
- Prioritize mitigations (block root causes that appear in multiple paths)

### Bow-Tie Risk Diagrams

**When**: Complex risks with multiple causes and multiple consequences.

**Structure**:
```
[Causes] → [Preventive Controls] → [RISK EVENT] → [Mitigative Controls] → [Consequences]
```

**Example**: Risk = "Production database unavailable"

**Left side (Causes + Prevention)**:
- Cause 1: Hardware failure → Prevention: Redundant instances, health checks
- Cause 2: Human error (bad migration) → Prevention: Dry-run on snapshot, peer review
- Cause 3: DDoS attack → Prevention: Rate limiting, WAF

**Right side (Mitigation + Consequences)**:
- Consequence 1: Users can't access app → Mitigation: Read replica for degraded mode
- Consequence 2: Revenue loss → Mitigation: SLA credits, customer communication plan
- Consequence 3: Reputational damage → Mitigation: PR plan, status page transparency

**Benefits**: Shows full lifecycle of risk (how to prevent, how to respond if it happens anyway).

### Premortem Variations

**Reverse Premortem** ("It succeeded wildly - how?"):
- Identifies what must go RIGHT for success
- Reveals critical success factors often overlooked
- Example: "We succeeded because we secured executive sponsorship early and maintained it throughout"

**Pre-Parade** (best-case scenario):
- What would make this initiative exceed expectations?
- Identifies opportunities to amplify impact
- Example: "If we also integrate with Salesforce, we could unlock enterprise market"

**Lateral Premortem** (stakeholder-specific):
- Run separate premortems for each stakeholder group
- Engineering: "It failed because of technical reasons..."
- Product: "It failed because users didn't adopt it..."
- Operations: "It failed because we couldn't support it at scale..."

## 3. Advanced Metrics Frameworks

### HEART Framework (Google)

For user-facing products, track:
- **Happiness**: User satisfaction (NPS, CSAT surveys)
- **Engagement**: Level of user involvement (DAU/MAU, sessions/user)
- **Adoption**: New users accepting product (% of target users activated)
- **Retention**: Rate users come back (7-day/30-day retention)
- **Task Success**: Efficiency completing tasks (completion rate, time on task, error rate)

**Application**:
- Leading: Adoption rate, task success rate
- Lagging: Retention, engagement over time
- Counter-metric: Happiness (don't sacrifice UX for engagement)

### AARRR Pirate Metrics

For growth-focused initiatives:
- **Acquisition**: Users discover product (traffic sources, signup rate)
- **Activation**: Users have good first experience (onboarding completion, time-to-aha)
- **Retention**: Users return (D1/D7/D30 retention)
- **Revenue**: Users pay (conversion rate, ARPU, LTV)
- **Referral**: Users bring others (viral coefficient, NPS)

**Application**:
- Identify bottleneck stage (where most users drop off)
- Focus initiative on improving that stage
- Track funnel conversion at each stage

### North Star + Supporting Metrics

**North Star Metric**: Single metric that best captures value delivered to customers.
- Examples: Weekly active users (social app), time-to-insight (analytics), API calls/week (platform)

**Supporting Metrics**: Inputs that drive the North Star.
- Example NSM: Weekly Active Users
  - Supporting: New user signups, activation rate, feature engagement, retention rate

**Application**:
- All initiatives tie back to moving North Star or supporting metrics
- Prevents metric myopia (optimizing one metric at expense of others)
- Aligns team around common goal

### SLI/SLO/SLA Framework

For reliability-focused initiatives:
- **SLI (Service Level Indicator)**: What you measure (latency, error rate, throughput)
- **SLO (Service Level Objective)**: Target for SLI (p99 latency < 200ms, error rate < 0.1%)
- **SLA (Service Level Agreement)**: Consequence if SLO not met (customer credits, escalation)

**Error Budget**:
- If SLO is 99.9% uptime, error budget is 0.1% downtime (43 minutes/month)
- Can "spend" error budget on risky deployments
- If budget exhausted, halt feature work and focus on reliability

**Application**:
- Define SLIs/SLOs for each major component
- Track burn rate (how fast you're consuming error budget)
- Use as gate for deployment (don't deploy if error budget exhausted)

### Metrics Decomposition Trees

**When**: Complex metric needs to be broken down into actionable components.

**Example**: Increase revenue
```
Revenue
├─ New Customer Revenue
│  ├─ New Customers (leads × conversion rate)
│  └─ Average Deal Size (features × pricing tier)
└─ Existing Customer Revenue
   ├─ Expansion (upsell rate × expansion ARR)
   └─ Retention (renewal rate × existing ARR)
```

**Application**:
- Identify which leaf nodes to focus on
- Each leaf becomes a metric to track
- Reveals non-obvious leverage points (e.g., increasing renewal rate might have bigger impact than new customer acquisition)

## 4. Integration Best Practices

### Specs → Risks Mapping

**Principle**: Every major specification decision should have corresponding risks identified.

**Example**:
- **Spec**: "Use MongoDB for user data storage"
- **Risks**:
  - R1: MongoDB performance degrades above 10M documents (mitigation: sharding strategy)
  - R2: Team lacks MongoDB expertise (mitigation: training, hire consultant)
  - R3: Data model changes require migration (mitigation: schema versioning)

**Implementation**:
- Review each spec section and ask "What could go wrong with this choice?"
- Ensure alternative approaches are considered with their risks
- Document why chosen approach is best despite risks

### Risks → Metrics Mapping

**Principle**: Each high-impact risk should have a metric that detects if it's materializing.

**Example**:
- **Risk**: "Database performance degrades under load"
- **Metrics**:
  - Leading: Query time p95 (early warning before user impact)
  - Lagging: User-reported latency complaints
  - Counter-metric: Don't over-optimize for read speed at expense of write consistency

**Implementation**:
- For each risk score 6-9, define early warning metric
- Set up alerts/dashboards to monitor these metrics
- Define escalation thresholds (when to invoke mitigation plan)

### Metrics → Specs Mapping

**Principle**: Specifications should include instrumentation to enable metric collection.

**Example**:
- **Metric**: "API p99 latency < 200ms"
- **Spec Requirements**:
  - Distributed tracing (OpenTelemetry) for end-to-end latency
  - Per-endpoint latency bucketing (identify slow endpoints)
  - Client-side RUM (real user monitoring) for user-perceived latency

**Implementation**:
- Review metrics and ask "What instrumentation is needed?"
- Add observability requirements to spec (logging, metrics, tracing)
- Include instrumentation in acceptance criteria

### Continuous Validation Loop

**Pattern**: Spec → Implement → Measure → Validate Risks → Update Spec

**Steps**:
1. **Initial Spec**: Document approach, risks, metrics
2. **Phase 1 Implementation**: Build and deploy
3. **Measure Reality**: Collect actual metrics vs. targets
4. **Validate Risk Mitigations**: Did mitigations work? New risks emerged?
5. **Update Spec**: Revise for next phase based on learnings

**Example**:
- **Phase 1 Spec**: Expected 10K req/s with single instance
- **Reality**: Actual 3K req/s (bottleneck in DB queries)
- **Risk Update**: Add R8: Query optimization needed for target load
- **Metric Update**: Add query execution time to dashboards
- **Phase 2 Spec**: Refactor queries, add read replicas, target 12K req/s

## 5. Complexity Decision Matrix

Use this matrix to decide when to use this skill vs. simpler approaches:

| Initiative Characteristics | Recommended Approach |
|---------------------------|----------------------|
| **Low Stakes** (< 1 eng-month, reversible, no user impact) | Lightweight spec, simple checklist, skip formal risk register |
| **Medium Stakes** (1-3 months, some teams, moderate impact) | Use template.md: Full spec + premortem + 3-5 metrics |
| **High Stakes** (3-6 months, cross-team, high impact) | Use template.md + methodology: Quantitative risk analysis, comprehensive metrics |
| **Strategic** (6+ months, company-level, existential) | Use methodology + external review: Fault tree, SLI/SLOs, continuous validation |

**Heuristics**:
- If failure would cost >$100K or 6+ eng-months, use full methodology
- If initiative affects >1000 users or >3 teams, use at least template
- If uncertainty is high, invest more in risk analysis and phased rollout
- If metrics are complex or novel, use advanced frameworks (HEART, North Star)

## 6. Anti-Patterns

**Spec Only (No Risks/Metrics)**:
- Symptom: Detailed spec but no discussion of what could go wrong or how to measure success
- Fix: Run quick premortem (15 min), define 3 must-track metrics minimum

**Risk Theater (Long List, No Mitigations)**:
- Symptom: 50+ risks identified but no prioritization or mitigation plans
- Fix: Score risks, focus on top 10, assign owners and mitigations

**Vanity Metrics (Measures Activity Not Outcomes)**:
- Symptom: Tracking "features shipped" instead of "user value delivered"
- Fix: For each metric ask "If this goes up, are users/business better off?"

**Plan and Forget (No Updates)**:
- Symptom: Beautiful spec/risk/metrics doc created then never referenced
- Fix: Schedule monthly reviews, update risks/metrics, track in team rituals

**Premature Precision (Overconfident Estimates)**:
- Symptom: "Migration will take exactly 47 days and cost $487K"
- Fix: Use ranges (30-60 days, $400-600K), state confidence levels, build in buffer

**Analysis Paralysis (Perfect Planning)**:
- Symptom: Spent 3 months planning, haven't started building
- Fix: Time-box planning (1-2 weeks for most initiatives), embrace uncertainty, learn by doing

## 7. Templates for Common Initiative Types

### Migration (System/Platform/Data)
- **Spec Focus**: Current vs. target architecture, migration path, rollback plan, validation
- **Risk Focus**: Data loss, downtime, performance regression, failed migration
- **Metrics Focus**: Migration progress %, data integrity, system performance, rollback capability

### Launch (Product/Feature)
- **Spec Focus**: User stories, UX flows, technical design, launch checklist
- **Risk Focus**: Low adoption, technical bugs, scalability issues, competitive response
- **Metrics Focus**: Activation, engagement, retention, revenue impact, support tickets

### Infrastructure Change
- **Spec Focus**: Architecture diagram, capacity planning, runbooks, disaster recovery
- **Risk Focus**: Outages, cost overruns, security vulnerabilities, operational complexity
- **Metrics Focus**: Uptime, latency, costs, incident count, MTTR

### Process Change (Organizational)
- **Spec Focus**: Current vs. new process, roles/responsibilities, training plan, timeline
- **Risk Focus**: Adoption resistance, productivity drop, key person dependency, communication gaps
- **Metrics Focus**: Process compliance, cycle time, employee satisfaction, quality metrics

For complete worked example, see [examples/microservices-migration.md](../examples/microservices-migration.md).

# ADR Methodology for Complex Decisions

## Complex ADR Workflow

Copy this checklist and track your progress:

```
ADR Progress (Complex Decisions):
- [ ] Step 1: Identify decision pattern and scope
- [ ] Step 2: Conduct detailed analysis for each concern
- [ ] Step 3: Engage stakeholders and gather input
- [ ] Step 4: Build decision tree for related choices
- [ ] Step 5: Perform quantitative analysis and create ADR
```

**Step 1: Identify decision pattern and scope**

Determine which pattern applies to your decision (cascading, competing concerns, unknown unknowns, etc.). See [Complex Decision Patterns](#complex-decision-patterns) for patterns and approaches.

**Step 2: Conduct detailed analysis for each concern**

For each competing concern (security, scalability, cost, compliance), analyze how alternatives address it. See [Extended ADR Sections](#extended-adr-sections) for analysis templates.

**Step 3: Engage stakeholders and gather input**

Identify all affected parties and gather their perspectives systematically. See [Stakeholder Management](#stakeholder-management) for mapping and engagement techniques.

**Step 4: Build decision tree for related choices**

Map out cascading or interdependent decisions. See [Decision Trees for Related Choices](#decision-trees-for-related-choices) for structuring related ADRs.

**Step 5: Perform quantitative analysis and create ADR**

Use scoring matrices, cost modeling, or load testing to support decision. See [Quantitative Analysis](#quantitative-analysis) for methods and examples.

## Complex Decision Patterns

### Pattern 1: Cascading Decisions

When one architectural choice forces or constrains subsequent decisions.

**Approach:**
1. Create primary ADR for the main architectural decision
2. Create child ADRs for cascading decisions, referencing parent
3. Use "Related ADRs" field to link the chain

**Example:**
- ADR-100: Adopt Microservices Architecture (parent)
- ADR-101: Use gRPC for Inter-Service Communication (child - follows from ADR-100)
- ADR-102: Implement Service Mesh with Istio (child - follows from ADR-101)

### Pattern 2: Competing Concerns

When decision must balance multiple competing priorities (cost vs performance, security vs usability).

**Approach:**
Add **Analysis Sections** to standard ADR:

```markdown
## Detailed Analysis

### Security Analysis
{How each alternative addresses security requirements}

### Performance Analysis
{Benchmarks, load tests, scalability projections}

### Cost Analysis
{TCO over 3 years, including hidden costs}

### Operational Complexity Analysis
{Team skill requirements, monitoring needs, on-call burden}
```

### Pattern 3: Phased Decisions

When full solution is too complex to decide at once; need to make interim decision.

**Approach:**
1. Create ADR for Phase 1 decision
2. Add "Future Decisions" section listing what's deferred
3. Set review date to revisit (e.g., "Review in 6 months")

**Example:**
```markdown
## Decision (Phase 1)
Start with managed PostgreSQL on RDS. Evaluate sharding vs Aurora vs NewSQL in 12 months.

## Future Decisions Needed
- ADR-XXX: Horizontal scaling strategy (by Q3 2025)
- ADR-XXX: Multi-region deployment approach (by Q4 2025)
```

## Extended ADR Sections

### When to Add Detailed Analysis Sections

**Security Analysis** - Add when:
- Decision affects authentication, authorization, or data protection
- Compliance requirements involved (SOC2, HIPAA, GDPR)
- Handling sensitive data

**Performance Analysis** - Add when:
- SLA commitments at stake
- Significant performance differences between alternatives
- Scalability is critical concern

**Cost Analysis** - Add when:
- Multi-year TCO differs significantly (>20%) between alternatives
- Hidden costs exist (operational overhead, training, vendor lock-in)
- Budget constraints are tight

**Operational Complexity Analysis** - Add when:
- Team skill gaps exist for some alternatives
- On-call burden varies significantly
- Monitoring/debugging complexity differs

**Migration Analysis** - Add when:
- Replacing existing system
- Need to maintain backward compatibility
- Rollback strategy is complex

### Template for Extended Sections

```markdown
## Security Analysis

### {Alternative A}
- **Threat model**: {What threats does this mitigate?}
- **Attack surface**: {What new vulnerabilities introduced?}
- **Compliance**: {How does this meet regulatory requirements?}
- **Score**: {1-5 rating}

### {Alternative B}
{Same structure}

### Security Recommendation
{Which alternative is strongest on security, and any mitigations needed}
```

## Stakeholder Management

### Identifying Stakeholders

**Technical stakeholders:**
- Engineering teams affected by the decision
- DevOps/SRE teams who will operate the solution
- Security team for compliance/security decisions
- Architecture review board (if exists)

**Business stakeholders:**
- Product managers (feature impact)
- Finance (budget implications)
- Legal/compliance (regulatory requirements)
- Executive sponsors (strategic alignment)

### Getting Input

**Pre-ADR phase:**
1. Conduct stakeholder interviews to gather requirements and constraints
2. Share draft alternatives for early feedback
3. Identify concerns and dealbreakers

**ADR draft phase:**
1. Share draft ADR with key stakeholders for review
2. Hold working session to discuss controversial points
3. Revise based on feedback

**Approval phase:**
1. Present ADR at architecture review (if applicable)
2. Get sign-off from decision-makers
3. Communicate decision to broader team

### Recording Stakeholder Positions

For controversial decisions, add:

```markdown
## Stakeholder Positions

**Backend Team (Support):**
"PostgreSQL aligns with our SQL expertise and provides ACID guarantees we need."

**DevOps Team (Concerns):**
"Concerned about operational complexity of read replicas. Request 2-week training before launch."

**Finance (Neutral):**
"Within budget. Request quarterly cost reviews to ensure no overruns."
```

## Decision Trees for Related Choices

When decision involves multiple related questions, use decision tree approach.

**Example: Cloud Provider + Database Decision**

```
Q1: Which cloud provider?
├─ AWS
│  ├─ Q2: Which database?
│  │  ├─ RDS PostgreSQL → ADR-042
│  │  ├─ Aurora → ADR-043
│  │  └─ DynamoDB → ADR-044
│
├─ GCP
│  └─ Q2: Which database?
│     ├─ Cloud SQL → ADR-045
│     └─ Spanner → ADR-046
```

**Approach:**
1. Create ADR for Q1 (cloud provider selection)
2. Create separate ADRs for Q2 based on Q1 outcome
3. Link ADRs using "Related ADRs" field

## Quantitative Analysis

### Cost-Benefit Matrix

For decisions with measurable trade-offs:

| Alternative | Setup Cost | Annual Cost | Performance (QPS) | Team Velocity Impact | Risk Score |
|-------------|-----------|-------------|-------------------|---------------------|------------|
| PostgreSQL  | $10k      | $36k        | 50k               | +10% (familiar)     | Low        |
| MongoDB     | $15k      | $84k        | 100k              | -20% (learning)     | Medium     |
| DynamoDB    | $5k       | $60k        | 200k              | -15% (new patterns) | Medium     |

### Decision Matrix with Weighted Criteria

When multiple factors matter with different importance:

```markdown
## Weighted Decision Matrix

Criteria weights:
- Performance: 30%
- Cost: 25%
- Team Expertise: 20%
- Operational Simplicity: 15%
- Ecosystem Maturity: 10%

| Alternative | Performance | Cost | Team | Ops | Ecosystem | Weighted Score |
|-------------|-------------|------|------|-----|-----------|----------------|
| PostgreSQL  | 7/10        | 9/10 | 10/10| 8/10| 10/10     | **8.35**       |
| MongoDB     | 9/10        | 6/10 | 5/10 | 7/10| 8/10      | 7.10           |
| DynamoDB    | 10/10       | 7/10 | 4/10 | 9/10| 7/10      | 7.50           |

PostgreSQL scores highest on weighted criteria.
```

### Scenario Analysis

For decisions under uncertainty, model different futures:

```markdown
## Scenario Analysis

### Scenario 1: Rapid Growth (3x projections)
- PostgreSQL: Need expensive scaling (Aurora + sharding), $150k/yr
- DynamoDB: Handles easily, $120k/yr
- **Winner**: DynamoDB

### Scenario 2: Moderate Growth (1.5x projections)
- PostgreSQL: Read replicas sufficient, $60k/yr
- DynamoDB: Overprovisioned, $90k/yr
- **Winner**: PostgreSQL

### Scenario 3: Slow Growth (0.8x projections)
- PostgreSQL: Single instance sufficient, $40k/yr
- DynamoDB: Low usage still requires min provision, $70k/yr
- **Winner**: PostgreSQL

**Assessment**: PostgreSQL wins in 2 of 3 scenarios. Given our conservative growth estimates, PostgreSQL is safer bet.
```

## Review and Update Process

### When to Review ADRs

**Scheduled reviews:**
- High-stakes decisions: Review after 6 months
- Medium-stakes: Review after 12 months
- Check if consequences matched reality

**Triggered reviews:**
- Major change in context (team size, scale, requirements)
- Significant problems attributed to decision
- New technology emerges that changes trade-offs

### How to Update ADRs

**Never edit old ADRs.** Instead:

1. Create new ADR that supersedes the old one
2. Update old ADR status to "Superseded by ADR-XXX"
3. New ADR should reference old one and explain what changed

**Example:**
```markdown
# ADR-099: Migrate from PostgreSQL to CockroachDB

**Status:** Accepted
**Date:** 2026-03-15
**Supersedes:** ADR-042 (PostgreSQL decision)

## Context
ADR-042 chose PostgreSQL in 2024 when we had 5k users. We now have 500k users across 8 regions. PostgreSQL sharding has become operationally complex...

## What Changed
- Scale increased 100x beyond projections
- Multi-region deployment now required for latency
- Team size grew from 5 to 40 engineers (distributed systems expertise available)
...
```

## Summary

For complex decisions:
- Break into multiple ADRs if needed (use cascading pattern)
- Add detailed analysis sections for critical factors
- Engage stakeholders early and document positions
- Use quantitative analysis (matrices, scenarios) to support intuition
- Plan for review and evolution over time

Remember: The best ADR is the one that helps future teammates understand "why" when reading it 2 years later.

---
name: stakeholders-org-design
description: Provides frameworks for mapping stakeholder influence networks, designing team structures aligned with system architecture (Conway's Law), defining team interface contracts (APIs, SLAs, decision rights), and assessing capability maturity (DORA, CMMC, agile models). Use when designing org structure or team topologies, mapping stakeholders for change initiatives, defining team interfaces, assessing capability maturity, planning restructures, or when user mentions org design, team structure, stakeholder map, Conway's Law, or RACI.
---

# Stakeholders & Organizational Design

## Table of Contents
1. [Workflow](#workflow)
2. [Stakeholder Mapping](#stakeholder-mapping)
3. [Team Interface Contracts](#team-interface-contracts)
4. [Capability Maturity](#capability-maturity)
5. [Common Patterns](#common-patterns)
6. [Guardrails](#guardrails)
7. [Quick Reference](#quick-reference)

## Workflow

Copy this checklist and track your progress:

```
Org Design Progress:
- [ ] Step 1: Map stakeholders and influence
- [ ] Step 2: Define team structure and boundaries
- [ ] Step 3: Specify team interfaces and contracts
- [ ] Step 4: Assess capability maturity
- [ ] Step 5: Create transition plan with governance
```

**Step 1: Map stakeholders and influence**

Identify all stakeholders, categorize by power-interest, map influence networks. See [Stakeholder Mapping](#stakeholder-mapping) for power-interest matrix and RACI frameworks.

**Step 2: Define team structure and boundaries**

Design teams aligned with architecture and strategy. For straightforward restructuring → Use [resources/template.md](resources/template.md). For complex org design with Conway's Law → Study [resources/methodology.md](resources/methodology.md).

**Step 3: Specify team interfaces and contracts**

Define APIs, SLAs, handoff protocols, decision rights between teams. See [Team Interface Contracts](#team-interface-contracts) for contract patterns.

**Step 4: Assess capability maturity**

Evaluate current state using maturity models (DORA, CMMC, custom). See [Capability Maturity](#capability-maturity) for assessment frameworks.

**Step 5: Create transition plan with governance**

Define migration path, decision rights, review cadence. Self-check using [resources/evaluators/rubric_stakeholders_org_design.json](resources/evaluators/rubric_stakeholders_org_design.json). Minimum standard: Average score ≥ 3.5.

## Stakeholder Mapping

### Power-Interest Matrix

| Quadrant | Engagement | Example |
|----------|------------|---------|
| High Power, High Interest | Manage Closely (frequent communication) | Executive sponsor, product owner |
| High Power, Low Interest | Keep Satisfied (status updates) | CFO for tech project, legal |
| Low Power, High Interest | Keep Informed (engage for feedback) | Individual contributors, early adopters |
| Low Power, Low Interest | Monitor (minimal engagement) | Peripheral teams |

### RACI Matrix

- **R - Responsible**: Does the work (can be multiple) — Example: Engineering team builds feature
- **A - Accountable**: Owns outcome (**exactly one** per decision) — Example: Product manager accountable for feature success
- **C - Consulted**: Provides input before decision (two-way) — Example: Security team consulted on auth design
- **I - Informed**: Notified after decision (one-way) — Example: Support team informed of launch

### Influence Network Mapping

**Identify**: Champions (advocates), Blockers (resistors), Bridges (connectors), Gatekeepers (control access)
**Map**: Who influences whom? Formal vs informal power, trust relationships, communication patterns

## Team Interface Contracts

### API Contracts

**Specify**: Endpoints, data format/schemas, authentication, rate limits, versioning/backward compatibility
**Example**: Service: User Auth API | Owner: Identity Team | Endpoints: /auth/login, /auth/token | SLA: 99.95% uptime, <100ms p95

### SLA (Service Level Agreements)

**Define**: Availability (99.9%, 99.99%), Performance (p50/p95/p99 latency), Support response times (critical: 1hr, high: 4hr, medium: 1 day), Capacity (requests/sec, storage)

### Handoff Protocols

**Design → Engineering**: Specs, prototype, design review sign-off | **Engineering → QA**: Feature complete, test plan, staging | **Engineering → Support**: Docs, runbook, training | **Research → Product**: Findings, recommendations, prototypes

### Decision Rights (DACI)

**D - Driver** (orchestrates), **A - Approver** (exactly one), **C - Contributors** (input), **I - Informed** (notified)
**Examples**: Architectural (Tech Lead approves, Architects contribute) | Hiring (Hiring Manager approves, Interviewers contribute) | Roadmap (PM approves, Eng/Design/Sales contribute)

## Capability Maturity

### DORA Metrics (DevOps Maturity)

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment Frequency | Multiple/day | Weekly-daily | Monthly-weekly | <Monthly |
| Lead Time | <1 hour | <1 day | 1 week-1 month | >1 month |
| MTTR | <1 hour | <1 day | 1 day-1 week | >1 week |
| Change Failure Rate | 0-15% | 16-30% | 31-45% | >45% |

### Generic Maturity Levels (CMM)

**Level 1 Initial**: Unpredictable, reactive | **Level 2 Repeatable**: Basic PM | **Level 3 Defined**: Documented, standardized | **Level 4 Measured**: Data-driven | **Level 5 Optimizing**: Continuous improvement

### Custom Capability Assessment

**Template**: Capability Name | Current Level (1-5 with evidence) | Target Level | Gap | Action Items

## Common Patterns

**Pattern 1: Functional → Product Teams (Spotify Model)**
- **Before**: Frontend team, Backend team, QA team, DevOps team
- **After**: Product Squad 1 (full-stack), Product Squad 2 (full-stack)
- **Interfaces**: Squads own end-to-end features, shared platform team for infrastructure
- **Benefit**: Faster delivery, reduced handoffs, clear ownership

**Pattern 2: Platform Team Extraction**
- **Trigger**: Multiple product teams duplicating infrastructure work
- **Design**: Create platform team providing self-service tools
- **Interface**: Platform team APIs + documentation, office hours, SLA
- **Staffing**: 10-15% of engineering (1 platform engineer per 7-10 product engineers)

**Pattern 3: Embedded vs Centralized Specialists**
- **Embedded**: Security/QA/Data engineers within product teams (close collaboration)
- **Centralized**: Specialists in separate team (consistency, expertise depth)
- **Hybrid**: Center of Excellence (set standards) + Embedded (implementation)
- **Choice Factors**: Team size, maturity, domain complexity

**Pattern 4: Conway's Law Alignment**
- **Principle**: System design mirrors communication structure
- **Application**: Design teams to match desired architecture
- **Example**: Microservices → Small autonomous teams per service
- **Anti-pattern**: Monolithic team structure → Monolithic architecture persists

**Pattern 5: Team Topologies (4 Fundamental Types)**
- **Stream-Aligned**: Product teams, aligned with flow of change
- **Platform**: Internal products enabling stream-aligned teams
- **Enabling**: Build capability in stream-aligned teams (temporary)
- **Complicated-Subsystem**: Specialists for complex areas (ML, security)

## Guardrails

**Conway's Law is inevitable:**
- Teams will produce systems mirroring their communication structure
- Design teams intentionally for desired architecture
- Reorganizing teams = reorganizing system boundaries

**Team size limits:**
- **2-pizza team**: 5-9 people (Amazon)
- **Dunbar's number**: 5-15 close working relationships
- Too small (<3): Fragile, lacks skills diversity
- Too large (>12): Communication overhead, subgroups form

**Cognitive load per team:**
- Each team has limited capacity for domains/systems
- **Simple**: 1 domain per team
- **Complicated**: 2-3 related domains
- **Complex**: Max 1 complex domain per team

**Interface ownership clarity:**
- Every interface needs one clear owner
- Shared ownership = no ownership
- Document: Owner, SLA, contact, escalation

**Avoid matrix hell:**
- Minimize dual reporting (confusing accountability)
- If matrix needed: Clear primary vs secondary manager
- Define decision rights explicitly (RACI/DACI)

**Stakeholder fatigue:**
- Don't manage all stakeholders equally
- High power/interest = frequent engagement
- Low power/interest = minimal updates
- Adjust as power/interest shifts

**Maturity assessment realism:**
- Don't grade on aspirations
- Evidence-based assessment (metrics, artifacts, observation)
- Common pitfall: Over-rating current state
- Use external benchmarks when available

## Quick Reference

**Resources:**
- **Quick org design**: [resources/template.md](resources/template.md)
- **Conway's Law & Team Topologies**: [resources/methodology.md](resources/methodology.md)
- **Quality rubric**: [resources/evaluators/rubric_stakeholders_org_design.json](resources/evaluators/rubric_stakeholders_org_design.json)

**5-Step Process**: Map Stakeholders → Define Teams → Specify Interfaces → Assess Maturity → Transition Plan

**Stakeholder Mapping**: Power-Interest Matrix (High/Low × High/Low), RACI (Responsible/Accountable/Consulted/Informed), Influence Networks

**Team Interfaces**: API contracts, SLAs (availability/performance/support), handoff protocols, decision rights (DACI/RAPID)

**Maturity Models**: DORA (deployment frequency, lead time, MTTR, change failure rate), Generic CMM (5 levels), Custom assessments

**Team Types**: Stream-Aligned (product), Platform (internal products), Enabling (capability building), Complicated-Subsystem (specialists)

**Guardrails**: Conway's Law, team size (2-pizza, Dunbar), cognitive load limits, interface ownership clarity, avoid matrix hell

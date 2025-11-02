# Platform Engineering Team Alignment Framework

## Context

**Why this matters now:**
Our platform team has grown from 3 to 15 engineers in 12 months. We're seeing inconsistent architecture decisions, unclear ownership, and technical debt accumulating. Teams are blocked waiting for platform features. We need shared principles to enable autonomous decision-making while maintaining quality and consistency.

**Who this is for:**
Platform Engineering team (15 engineers, 3 teams: Infrastructure, Developer Tools, Observability)

**Last updated:** 2024-11-15

---

## North Star

**Build infrastructure that developers trust and love to use.**

Every platform we build should make developers more productive, not add cognitive load. Systems should be so reliable that product teams never think about them.

---

## Core Values

### 1. Simplicity Over Cleverness

**What it means:**
We choose boring, proven technology over exciting new tools. We value systems that operators can debug at 3 AM over systems that are technically impressive. Every abstraction must pay for itself in reduced complexity.

**Why it matters:**
Complex systems fail in complex ways. When product teams are down, they need fixes fast, not archaeology. Our 3 AM self will curse our 3 PM clever self.

**What we optimize for:**
- Debuggability and operational simplicity
- Fewer moving parts
- Standard solutions over custom code
- Clear mental models

**What we de-prioritize:**
- Resume-driven development
- Micro-optimizations that add complexity
- Novel approaches when proven ones exist
- Being first to adopt new tech

**Examples:**
- Use managed PostgreSQL instead of building our own database cluster
- Choose nginx over a custom written load balancer
- Pick Kubernetes standard patterns over clever custom operators

### 2. Reliability Over Features

**What it means:**
Every service has SLOs and we honor them. We say no to features that compromise reliability. Reliability is a feature, not a phase. When in doubt, we prioritize preventing incidents over shipping features.

**Why it matters:**
One platform outage affects every product team. Our unreliability multiplies across the organization. Lost trust takes months to rebuild.

**What we optimize for:**
- SLO compliance (99.9%+ uptime for critical paths)
- Graceful degradation
- Observable systems
- Rollback capability

**What we de-prioritize:**
- Shipping fast at the cost of stability
- Features without monitoring
- Experimentation that risks critical path
- Tight coupling that prevents safe deploys

**Examples:**
- We run chaos engineering tests before Black Friday
- New features launch behind feature flags with gradual rollout
- We have automated rollback for all critical services

### 3. Developer Experience is Not Optional

**What it means:**
APIs should be intuitive, documentation should exist, and errors should be actionable. If developers are frustrated, we've failed. We design for the developer using our systems, not just for the system itself.

**Why it matters:**
Friction in platform tools slows every product team. 100 developers × 10min friction = 1000min lost daily. Good DX multiplies productivity; bad DX multiplies frustration.

**What we optimize for:**
- Clear, actionable error messages
- Comprehensive, up-to-date documentation
- Simple onboarding (< 1 hour to first deploy)
- Fast feedback loops

**What we de-prioritize:**
- Internal-only jargon in APIs
- Optimization for our convenience over user experience
- Tribal knowledge over documentation
- Complex configurations

**Examples:**
- All APIs have OpenAPI specs and interactive docs
- Error messages include links to runbooks
- We measure "time to first successful deploy" for new services

### 4. Ownership Means Accountability

**What it means:**
If you build it, you run it. Teams own their services end-to-end: development, deployment, monitoring, on-call. Ownership includes making your service operationally excellent, not just functionally correct.

**Why it matters:**
Throwing code over the wall creates unmaintainable systems. Operators who didn't build it can't improve it. Builders who don't operate it don't feel the pain of poor operational characteristics.

**What we optimize for:**
- End-to-end ownership
- Operational maturity (monitoring, alerting, runbooks)
- Empowered teams
- Learning from production

**What we de-prioritize:**
- Separate "ops" team for platform services
- Deploying without runbooks
- Services without clear owners
- Handoffs between teams

**Examples:**
- Infrastructure team is on-call for Kubernetes cluster
- Developer Tools team owns CI/CD pipeline end-to-end
- Each team has SLO dashboards they review weekly

---

## Decision Tenets

### When Choosing Technology

**When evaluating new tools:**
- ✓ Choose managed services (RDS, managed K8s) over self-hosted when quality is comparable
- ✓ Pick tools with strong observability out-of-the-box
- ✓ Prefer tools our team has expertise in over "better" tools we'd need to learn
- ✗ Don't adopt because it's trending or looks good on résumé
- ⚠ **Exception:** When existing tools fundamentally can't meet requirements AND we have capacity to support

**When building vs buying:**
- ✓ Build when our requirements are unique or when vendors don't exist
- ✓ Buy when it's undifferentiated heavy lifting (observability, databases)
- ✗ Don't build for the joy of building
- ⚠ **Exception:** Build when vendor lock-in risk outweighs development cost

### When Making Architecture Decisions

**When designing APIs:**
- ✓ Choose RESTful JSON APIs as default (boring, widely understood)
- ✓ Design for the developer experience, document before implementing
- ✗ Don't create bespoke protocols without strong justification
- ⚠ **Exception:** gRPC for high-performance internal services

**When choosing between perfection and shipping:**
- ✓ Ship with known minor issues if they don't affect SLOs
- ✓ Document technical debt and schedule fixes
- ✗ Don't ship if it compromises security, data integrity, or violates SLOs
- ⚠ **Exception:** Never compromise on security, payments, or PII handling

### When Prioritizing Work

**When product teams request features:**
- 🔴 **Critical:** SLO violations, security issues, data loss risks
- 🟡 **Important:** Developer friction affecting >3 teams, technical debt preventing new features
- ⚪ **Nice-to-have:** Single-team requests, optimizations, new nice-to-have features

**When allocating time:**
- 70% Product work (features product teams need)
- 20% Platform health (tech debt, improvements)
- 10% Innovation (experiments, R&D)

---

## Observable Behaviors

### In Code Reviews

- We comment on operational characteristics (What happens when this fails? How will we debug it?)
- We ask "What's the runbook?" before approving infrastructure changes
- We praise simplicity and question complexity
- We flag missing monitoring/alerting

### In Planning

- First question: "What's the simplest thing that could work?"
- We timeblock for operational work (not just features)
- We say no to work that violates SLOs or has no monitoring plan
- We ask "Who's on-call for this?"

### In Incidents

- Postmortems focus on learning, not blame
- We fix systemic issues, not just symptoms
- We update runbooks during incidents
- We celebrate good incident response (fast mitigation, clear communication)

### In Communication

- We write Architecture Decision Records (ADRs) for significant choices
- We document before we ship
- We assume future readers lack our context
- We use plain language, not jargon

### In Hiring

- We ask candidates to debug a system, not just build features
- We evaluate for operational maturity, not just coding skills
- We look for simplicity-minded engineers, not algorithm wizards
- We ask: "Tell me about a time you chose boring tech over exciting tech"

### In Daily Work

- We check SLO dashboards daily
- We improve documentation when we're confused
- We automate toil we encounter
- We share learnings in team channels

---

## Anti-Patterns

### What We Explicitly DON'T Do

✗ **Ship without monitoring** - even when deadline pressure is high
   - **Because:** Reliability > Features. Can't fix what we can't observe.

✗ **Optimize prematurely** - even when we see potential improvements
   - **Because:** Simplicity > Performance. Measure first, optimize if needed.

✗ **Build custom solutions for solved problems** - even when it seems fun
   - **Because:** Maintenance cost exceeds initial development 10x. Use managed services.

✗ **Skip documentation because "code is self-documenting"** - even when time is tight
   - **Because:** Developer Experience matters. Future us will curse present us.

✗ **Say yes to every feature request** - even when stakeholders insist
   - **Because:** Ownership includes protecting platform quality. Our job is to say no to bad ideas.

✗ **Deploy Friday afternoon** - even when it seems low-risk
   - **Because:** Reliability matters more than shipping fast. Weekend incidents aren't worth it.

---

## How to Use This

### In Decision-Making

**When stuck between two options:**
1. Check decision tenets above
2. Ask "Which choice better serves our North Star?"
3. Consider which value is most relevant
4. Document decision in ADR with rationale

### In Hiring

**Interview questions tied to values:**
- **Simplicity:** "Tell me about a time you refactored complex code to be simpler. What drove that decision?"
- **Reliability:** "How do you decide when to ship vs. when to delay for quality?"
- **Developer Experience:** "What makes a good API? Show me an API you love and why."
- **Ownership:** "How do you approach on-call? What makes a service operationally mature?"

### In Onboarding

**Week 1:** New engineers read this document and discuss in 1:1
**Week 2:** Shadow on-call to see ownership in practice
**Week 3:** Pair on feature to see values in code review
**Month 1:** Present one architectural decision using these tenets

### In Performance Reviews

We evaluate on:
- **Simplicity:** Do they choose boring solutions? Do they reduce complexity?
- **Reliability:** Do their services meet SLOs? How do they handle incidents?
- **Developer Experience:** Is their code/APIs/docs easy to use?
- **Ownership:** Do they own services end-to-end? Do they improve operations?

### When Values Conflict

**Simplicity vs Developer Experience:**
- **Winner:** Developer Experience. Simple for *us* to maintain isn't valuable if developers can't use it.

**Reliability vs Speed:**
- **Winner:** Reliability. But use feature flags to ship safely.

**Features vs Platform Health:**
- **Default:** Follow 70/20/10 allocation. But SLO violations always win.

---

## Evolution

**Review cadence:** Quarterly team retro discusses if values still serve us. Annual deep revision.

**Who can propose changes:** Anyone. Discuss in team meeting, decision by consensus.

**What stays constant:**
- North Star (unless fundamental mission changes)
- Core value themes (names might evolve, principles remain)

**Recent changes:**
- *2024-Q3*: Added "Developer Experience" value as team grew and internal customers increased
- *2024-Q2*: Refined "Simplicity" to explicitly call out managed services
- *2024-Q1*: Added 70/20/10 time allocation guideline

---

## Success Stories

### Example 1: Chose PostgreSQL RDS over Self-Hosted

**Situation:** Need database for new service. Self-hosted gives more control and learning opportunity.

**Decision:** Chose AWS RDS PostgreSQL (managed service).

**Values applied:**
- ✓ Simplicity > Cleverness: Less operational burden
- ✓ Ownership: Team doesn't have DB expertise yet
- ✓ Reliability: AWS has better uptime than we'd achieve

**Outcome:** Service launched in 2 weeks vs. estimated 6 weeks for self-hosted setup and learning. Zero database incidents in 6 months.

### Example 2: Said No to Real-Time Features

**Situation:** Product team requested real-time notifications (WebSockets) for dashboard.

**Decision:** Said no, proposed 30-second polling instead.

**Values applied:**
- ✓ Simplicity: Polling is simpler than WebSocket infrastructure
- ✓ Reliability: Don't risk stability for nice-to-have feature
- ✓ Developer Experience: Team lacks WebSocket experience

**Outcome:** Shipped in 1 week with polling. User research showed 30s delay was acceptable. Saved 6+ weeks of WebSocket infrastructure work.

### Example 3: Invested Week in Documentation

**Situation:** New API ready to ship, docs incomplete. Pressure to launch.

**Decision:** Delayed launch one week to complete docs, examples, and migration guide.

**Values applied:**
- ✓ Developer Experience: Documentation is not optional
- ✓ Ownership: We support what we ship

**Outcome:** 12 teams adopted in first month (vs estimated 4-6 with poor docs). Near-zero support requests due to clear docs.

# ADR Template - Standard Format

## When to Use This Template

Use this template for straightforward technology or process decisions where:
- Clear alternatives exist
- Trade-offs are primarily technical
- Decision scope is well-defined
- Standard ADR format is sufficient

For complex architectural decisions with multiple interdependent factors, see `methodology.md`.

## Quick Template

Copy this structure to create your ADR:

```markdown
# ADR-{NUMBER}: {Decision Title in Title Case}

**Status:** {Proposed | Accepted | Deprecated | Superseded}
**Date:** {YYYY-MM-DD}
**Deciders:** {List people/teams involved in decision}
**Related ADRs:** {Links to related ADRs, if any}

## Context

{Describe the situation, problem, or opportunity that necessitates this decision}

**Background:**
{What led to this decision being needed?}

**Requirements:**
{What functional/non-functional requirements must be met?}

**Constraints:**
{What limitations exist? Budget, timeline, skills, compliance, technical debt, etc.}

## Decision

{State clearly what you're choosing to do}

{Be specific and actionable. Include:}
- {What technology/approach/standard is being adopted}
- {What version or configuration, if relevant}
- {What scope this applies to (one service, entire system, etc.)}

## Alternatives Considered

### Option A: {Name}
**Description:** {Brief description}
**Pros:**
- {Benefit 1}
- {Benefit 2}

**Cons:**
- {Drawback 1}
- {Drawback 2}

**Why not chosen:** {Specific reason}

### Option B: {Name}
{Same structure}

### Option C: {Name}
{Same structure}

*Note: Include at least 2-3 real alternatives that were seriously considered*

## Consequences

### Benefits
- **{Benefit category}**: {Specific benefit and why it matters}
- **{Benefit category}**: {Specific benefit and why it matters}

### Drawbacks
- **{Drawback category}**: {Specific cost/limitation and mitigation if any}
- **{Drawback category}**: {Specific cost/limitation and mitigation if any}

### Risks
- **{Risk}**: {Likelihood and mitigation plan}

### Trade-offs Accepted
{What are we explicitly trading off? E.g., "Trading development speed for operational simplicity"}

## Implementation

{Optional section - include if implementation details are important}

**Rollout Plan:**
{How will this be deployed/adopted?}

**Migration Path:**
{If replacing something, how do we transition?}

**Timeline:**
{Key milestones and dates}

**Success Criteria:**
{How will we know this decision was right?}

## References

{Links to:}
- {Technical documentation}
- {Benchmarks or research}
- {Related discussions or RFCs}
- {Vendor documentation}
```

## Field-by-Field Guidance

### Title
- Format: `ADR-{NUMBER}: {Short Decision Summary}`
- Number: Sequential, usually 001, 002, etc.
- Summary: One line, actionable (e.g., "Use PostgreSQL for Primary Database", not "Database Choice")

### Status
- **Proposed**: Under discussion, not yet adopted
- **Accepted**: Decision is final and being implemented
- **Deprecated**: No longer recommended (but still in use)
- **Superseded**: Replaced by another ADR (link to it)

### Context
**Purpose**: Help future readers understand WHY this decision was necessary

**Include:**
- What problem/opportunity triggered this?
- What are the business/technical drivers?
- What requirements must be met?
- What constraints limit options?

**Don't include:**
- Solutions (those go in Decision section)
- Analysis of options (that goes in Alternatives)

**Length**: 2-4 paragraphs typically

**Example:**
> Our current monolithic application is becoming difficult to scale and deploy. Deploys take 45 minutes and require full system downtime. Teams are blocked on each other's changes. We need to support 10x traffic growth in the next year.
>
> Requirements: Independent deployment, horizontal scaling, fault isolation, team autonomy.
> Constraints: Team has limited Kubernetes experience, must complete migration in 6 months, budget allows 20% infrastructure cost increase.

### Decision
**Purpose**: State clearly and specifically what you're doing

**Include:**
- Specific technology/approach (with version if relevant)
- Configuration or implementation approach
- Scope of application

**Don't:**
- Justify (that's in Consequences)
- Compare (that's in Alternatives)
- Be vague ("use the best tool")

**Length**: 1-3 paragraphs

**Example:**
> We will adopt a microservices architecture using:
> - Kubernetes (v1.28+) for orchestration
> - gRPC for inter-service communication
> - PostgreSQL databases (one per service where needed)
> - Shared API gateway (Kong) for external traffic
>
> Scope: All new services and existing services as they require significant changes. No forced migration of stable services.

### Alternatives Considered
**Purpose**: Show other options were evaluated seriously (prevents "we should have considered X")

**Include:**
- 2-4 real alternatives that were discussed
- Honest pros/cons for each
- Specific reason not chosen

**Don't:**
- Include straw man options you never seriously considered
- Unfairly present alternatives (be honest about their merits)
- Omit major alternatives

**Format for each alternative:**
- Name/summary
- Brief description
- 2-4 key pros
- 2-4 key cons
- Why not chosen (specific, not "just worse")

**Example:**
> ### Continue with Monolith + Optimization
> **Pros:**
> - No migration cost or risk
> - Team expertise is high
> - Simpler operations
>
> **Cons:**
> - Doesn't solve team coupling problem
> - Still requires full-system deploys
> - Scaling is all-or-nothing
>
> **Why not chosen:** Doesn't address fundamental team velocity and deployment issues that are our primary pain points.

### Consequences
**Purpose**: Honest assessment of what this decision means long-term

**Include:**
- Benefits (what we gain)
- Drawbacks (what we lose or costs we incur)
- Risks (what could go wrong)
- Trade-offs (what we explicitly chose to sacrifice)

**Critical**: Be honest about downsides. Every decision has cons.

**Format:**
- Group by category (performance, cost, team, operations, etc.)
- Be specific (not "better performance" but "50% faster writes, 2x slower reads")
- Note mitigation strategies for drawbacks where applicable

**Example:**
> **Benefits:**
> - **Team velocity**: Teams can deploy independently, 10min deploys vs 45min
> - **Scalability**: Can scale hot services independently, expect 50% infrastructure cost reduction
> - **Resilience**: Service failures are isolated, no cascading failures
>
> **Drawbacks:**
> - **Operational complexity**: Managing 15+ services vs 1, need monitoring/tracing
> - **Development overhead**: Network calls vs function calls, serialization costs
> - **Data consistency**: Eventual consistency across services, need compensating transactions
>
> **Risks:**
> - **Migration risk**: If migration takes >6mo, could end up with worst of both worlds
> - **Team skill gap**: Need to train team on Kubernetes, distributed systems concepts
>
> **Trade-offs:**
> Trading development simplicity for deployment flexibility and team autonomy.

## Quality Checklist

Before finalizing, verify:

- [ ] Title is clear and specific (not generic)
- [ ] Status is set and accurate
- [ ] Context explains WHY without proposing solutions
- [ ] Decision is specific and actionable
- [ ] At least 2-3 real alternatives are documented
- [ ] Each alternative has honest pros/cons
- [ ] Consequences include both benefits AND drawbacks
- [ ] Risks are identified with mitigation where applicable
- [ ] Technical details are accurate and specific
- [ ] Future readers will understand context without asking around
- [ ] No jargon without explanation
- [ ] Trade-offs are explicitly acknowledged

## Common Patterns

### Technology Selection ADR
Focus on: capabilities vs requirements, performance characteristics, team expertise, operational complexity, ecosystem maturity

### Process/Standard ADR
Focus on: enforcement mechanisms, exceptions, onboarding/training, examples, tooling support

### Migration ADR
Focus on: rollout strategy, backward compatibility, rollback plan, success metrics, timeline

### Deprecation ADR
Set Status: Deprecated or Superseded
Include: Sunset timeline, migration path, superseding ADR link (if applicable)

## Examples

See `examples/` directory for complete examples:
- `database-selection.md` - Technology choice
- `api-versioning.md` - Standard/process decision
- `microservices-migration.md` - Large architectural change

## Anti-Patterns to Avoid

**Vague context:**
- Bad: "We need a better database"
- Good: "Current MySQL instance hitting 80% CPU during peak load (5k QPS), queries taking >500ms"

**Non-specific decision:**
- Bad: "Use microservices"
- Good: "Migrate to microservices using Kubernetes 1.28+ with gRPC, starting with user service"

**Unfair alternatives:**
- Bad: "MongoDB: bad for our use case, slow, unreliable"
- Good: "MongoDB: Excellent for flexible schemas and horizontal scaling, but lacks multi-document ACID transactions we need for payments"

**Hiding downsides:**
- Bad: "PostgreSQL will solve all our problems"
- Good: "PostgreSQL provides ACID guarantees we need, but will require read replicas at >50k QPS and is harder to shard than DynamoDB"

**Too long:**
- If ADR is >3 pages, consider splitting into multiple ADRs or creating separate design doc with ADR referencing it

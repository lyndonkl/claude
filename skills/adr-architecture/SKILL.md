---
name: adr-architecture
description: Use when documenting significant technical or architectural decisions that need context, rationale, and consequences recorded. Invoke when choosing between technology options, making infrastructure decisions, establishing standards, migrating systems, or when team needs to understand why a decision was made. Use when user mentions ADR, architecture decision, technical decision record, or decision documentation.
---

# Architecture Decision Records (ADR)

## Table of Contents

- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [What is an ADR?](#what-is-an-adr)
- [Workflow](#workflow)
  - [1. Understand the Decision](#1--understand-the-decision)
  - [2. Choose ADR Template](#2--choose-adr-template)
  - [3. Document the Decision](#3--document-the-decision)
  - [4. Validate Quality](#4--validate-quality)
  - [5. Deliver and File](#5--deliver-and-file)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Document significant architectural and technical decisions with full context, alternatives considered, trade-offs analyzed, and consequences understood. ADRs create a decision trail that helps teams understand "why" decisions were made, even years later.

## When to Use This Skill

- Recording architecture decisions (microservices, databases, frameworks)
- Documenting infrastructure choices (cloud providers, deployment strategies)
- Capturing technology selections (libraries, tools, platforms)
- Logging process decisions (branching strategy, deployment process)
- Establishing technical standards or conventions
- Migrating or sunsetting systems
- Making security or compliance choices
- Resolving technical debates with documented rationale
- Onboarding new team members who need decision history

**Trigger phrases:** "ADR", "architecture decision", "document this decision", "why did we choose", "decision record", "technical decision log"

## What is an ADR?

An Architecture Decision Record is a document capturing a single significant decision. It includes:

- **Context**: What situation necessitates this decision?
- **Decision**: What are we choosing to do?
- **Alternatives**: What other options did we consider?
- **Consequences**: What are the trade-offs and implications?
- **Status**: Proposed, accepted, deprecated, superseded?

**Quick Example:**

```markdown
# ADR-042: Use PostgreSQL for Primary Database

**Status:** Accepted
**Date:** 2024-01-15
**Deciders:** Backend team, CTO

## Context
Need to select primary database for new microservices platform.
Requirements: ACID transactions, complex queries, 10k+ QPS at launch.

## Decision
Use PostgreSQL 15+ as primary relational database.

## Alternatives Considered
- MySQL: Weaker JSON support, less robust constraint handling
- MongoDB: No ACID across documents, eventual consistency issues
- CockroachDB: Excellent but adds operational complexity we can't support yet

## Consequences
✓ Strong consistency and data integrity
✓ Excellent JSON support for semi-structured data
✓ Team has deep PostgreSQL experience
✗ Vertical scaling limits (will need read replicas at 50k+ QPS)
✗ More complex to shard than DynamoDB if we need it
```

## Workflow

Follow these steps in order:

### 1. [ ] Understand the Decision

Gather decision context:
- [ ] **What decision needs to be made?** (specific technology, approach, or standard)
- [ ] **Why now?** (what triggered this decision?)
- [ ] **Who are the deciders?** (team, role, individuals)
- [ ] **What are the constraints?** (budget, timeline, skills, compliance)
- [ ] **What are the requirements?** (functional, non-functional, business)
- [ ] **What's the scope?** (one service, entire system, organization-wide)

### 2. [ ] Choose ADR Template

Based on decision type:

- [ ] **For technology selection** → Use `resources/template.md` (standard ADR format)
  - Choosing frameworks, libraries, databases, tools
  - Clear alternatives exist
  - Trade-offs are technical

- [ ] **For complex architectural decisions** → Study `resources/methodology.md`
  - System-wide architectural patterns
  - Multiple interdependent decisions
  - Need detailed analysis sections (security, scalability, cost)

- [ ] **To see examples** → Review `resources/examples/`
  - `database-selection.md` - Technology choice with trade-offs
  - `microservices-migration.md` - Large architectural change
  - `api-versioning.md` - Process/standard decision

### 3. [ ] Document the Decision

Create the ADR following this structure:

- [ ] **Write clear title**: "ADR-{number}: {Decision in one line}"
- [ ] **Add metadata**: Status, date, deciders
- [ ] **Explain context**: Situation, requirements, constraints (why this decision is needed)
- [ ] **State decision**: What you're choosing to do (be specific and actionable)
- [ ] **List alternatives**: What else was considered (with brief pros/cons)
- [ ] **Analyze consequences**: Trade-offs, risks, benefits, long-term implications
- [ ] **Add implementation notes**: If relevant (migration path, rollout plan)
- [ ] **Include links/references**: Related ADRs, external resources

**Output file**: Create `adr-{number}-{short-title}.md` in current directory

### 4. [ ] Validate Quality

Self-check using `resources/evaluators/rubric_adr_architecture.json`:

**Quality checks:**
- [ ] Context clearly explains WHY this decision is needed
- [ ] Decision is specific and actionable (not vague)
- [ ] At least 2-3 real alternatives are documented with trade-offs
- [ ] Consequences include both benefits and drawbacks
- [ ] Technical details are accurate
- [ ] Someone unfamiliar with context can understand the decision
- [ ] Trade-offs are honest (acknowledges downsides)
- [ ] Future readers will understand "why we chose this"

**Minimum standard**: Score ≥ 3.5 across all criteria

If decision is controversial or high-impact, aim for 4.5+ average.

### 5. [ ] Deliver and File

Present to the user:
- [ ] The completed ADR file
- [ ] Highlight key trade-offs identified
- [ ] Suggest ADR numbering if not provided
- [ ] Recommend review process (if high-stakes decision)
- [ ] Note any follow-up decisions needed

**Filing convention**: Store ADRs in `docs/adr/` or `architecture/decisions/` directory with sequential numbering.

## Common Patterns

**For technology selection:**
- Focus on technical capabilities vs requirements
- Include performance benchmarks if available
- Document team expertise level
- Consider operational complexity

**For architectural changes:**
- Include migration strategy in consequences
- Document backward compatibility impact
- Consider team velocity impact during transition
- Note monitoring and rollback plans

**For standards and conventions:**
- Include examples of the standard in practice
- Document exceptions or escape hatches
- Consider enforcement mechanisms
- Note educational/onboarding implications

**For deprecations:**
- Set status to "Deprecated" or "Superseded"
- Link to superseding ADR
- Document sunset timeline
- Include migration guide

## Guardrails

**Do:**
- Be honest about trade-offs (every choice has downsides)
- Write for future readers who lack current context
- Include specific technical details (versions, configurations)
- Acknowledge uncertainty and risks
- Keep ADRs immutable (status changes, but content doesn't)
- Write one ADR per decision (focused scope)

**Don't:**
- Make decisions sound better than they are
- Omit alternatives that were seriously considered
- Use jargon without explanation
- Write vague consequences ("might improve performance")
- Revisit/edit old ADRs (write new superseding ADR instead)
- Combine multiple independent decisions in one ADR

## Quick Reference

- **Standard template**: `resources/template.md`
- **Complex decisions**: `resources/methodology.md`
- **Examples**: `resources/examples/database-selection.md`, `resources/examples/microservices-migration.md`, `resources/examples/api-versioning.md`
- **Quality rubric**: `resources/evaluators/rubric_adr_architecture.json`

**ADR Naming Convention**: `adr-{number}-{short-kebab-case-title}.md`
- Example: `adr-042-use-postgresql-for-primary-database.md`

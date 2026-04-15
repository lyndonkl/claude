---
name: chain-spec-risk-metrics
description: Chains together clear specifications, proactive risk analysis (premortem/register), and measurable success metrics into a comprehensive planning artifact for high-stakes initiatives. Use when planning migrations, launches, or strategic changes that need implementation roadmaps, risk mitigation, and instrumentation. Invoke when user mentions "plan this migration", "launch strategy", "implementation roadmap", "what could go wrong", "how do we measure success", or when high-impact decisions need comprehensive planning.
---
# Chain Spec Risk Metrics

## Table of Contents
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Overview

This skill combines three components into a comprehensive planning artifact:

1. **Specification** - Define what you're building/changing with clarity (scope, requirements, approach, timeline)
2. **Risk Analysis** - Identify what could go wrong through premortem ("imagine we failed - why?") and create risk register with mitigations
3. **Success Metrics** - Define measurable outcomes to track progress and validate success

**When NOT to use:** For specifications only, use `one-pager-prd` or `adr-architecture`. For risk analysis only, use `project-risk-register`. For metrics only, use `metrics-tree`. For brainstorming alternatives, use `brainstorm-diverge-converge`.

**Quick example:**
> **Initiative:** Migrate monolith to microservices
>
> **Spec:** Decompose into 5 services (auth, user, order, inventory, payment), API gateway, shared data patterns
>
> **Risks:**
> - Data consistency issues between services (High) → Implement saga pattern with compensation
> - Performance degradation from network hops (Medium) → Load test with production traffic patterns
>
> **Metrics:**
> - Deployment frequency (target: 10+ per week, baseline: 2 per week)
> - API p99 latency (target: < 200ms, baseline: 150ms)
> - Mean time to recovery (target: < 30min, baseline: 2 hours)

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

**Step 1: Gather initiative context**

Ask user for the initiative goal, constraints (time/budget/resources), stakeholders, current state (baseline), and desired outcomes. Clarify whether this is a greenfield build, migration, enhancement, or strategic change. See [resources/template.md](resources/template.md) for full context questions.

**Step 2: Write comprehensive specification**

Create detailed specification covering scope (what's in/out), approach (architecture/methodology), requirements (functional/non-functional), dependencies, timeline, and success criteria. For standard initiatives use [resources/template.md](resources/template.md); for complex multi-phase programs see [resources/methodology.md](resources/methodology.md) for decomposition techniques.

**Step 3: Conduct premortem and build risk register**

Run premortem exercise: "Imagine 12 months from now this initiative failed spectacularly. What went wrong?" Identify risks across technical, operational, organizational, and external dimensions. For each risk document likelihood, impact, mitigation strategy, and owner. See [Premortem Technique](#premortem-technique) and [Risk Register Structure](#risk-register-structure) sections, or [resources/methodology.md](resources/methodology.md) for advanced risk assessment methods.

**Step 4: Define success metrics and instrumentation**

Identify leading indicators (early signals), lagging indicators (outcome measures), and counter-metrics (what you're NOT willing to sacrifice). Specify current baseline, target values, measurement method, and tracking cadence for each metric. See [Metrics Framework](#metrics-framework) and use [resources/template.md](resources/template.md) for standard structure.

**Step 5: Validate completeness and deliver**

Self-check the complete artifact using [resources/evaluators/rubric_chain_spec_risk_metrics.json](resources/evaluators/rubric_chain_spec_risk_metrics.json). Ensure specification is clear and actionable, risks are comprehensive with mitigations, metrics measure actual success, and all three components reinforce each other. Minimum standard: Average score ≥ 3.5 across all criteria.

## Common Patterns

### Premortem Technique

1. **Set the scene**: "It's [6/12/24] months from now. This initiative failed catastrophically."
2. **Brainstorm failure causes**: Each stakeholder writes 3-5 reasons why it failed (independently first)
3. **Cluster and prioritize**: Group similar failures, vote on likelihood and impact
4. **Convert to risk register**: Each failure mode becomes a risk with mitigation plan

### Risk Register Structure

For each identified risk, document:
- **Risk description**: Specific failure mode (not vague "project delay")
- **Category**: Technical, operational, organizational, external
- **Likelihood**: Low/Medium/High (or probability %)
- **Impact**: Low/Medium/High (or cost estimate)
- **Mitigation strategy**: What you'll do to reduce likelihood or impact
- **Owner**: Who monitors and responds to this risk
- **Status**: Open, Mitigated, Accepted, Closed

### Metrics Framework

**Leading indicators** (predict future success):
- Deployment frequency, code review velocity, incident detection time

**Lagging indicators** (measure outcomes):
- Uptime, user adoption, revenue impact, customer satisfaction

**Counter-metrics** (what you're NOT willing to sacrifice):
- Code quality, team morale, security posture, user privacy

## Guardrails

- **Don't skip any component** - Spec without risks = blind spots; risks without metrics = unvalidated mitigations
- **Be specific in specifications** - "Improve performance" is not a spec; "Reduce p99 API latency from 500ms to 200ms" is
- **Quantify risks** - Use likelihood × impact scores to prioritize; don't treat all risks equally
- **Make metrics measurable** - "Better UX" is not measurable; "Increase checkout completion from 67% to 75%" is
- **Assign owners** - Every risk and metric needs a clear owner who monitors and acts
- **State assumptions explicitly** - Document what you're assuming about resources, timelines, dependencies
- **Include counter-metrics** - Always define what success does NOT mean sacrificing
- **Update as you learn** - This is a living document; revisit after milestones to update risks/metrics

## Quick Reference

| Component | When to Use | Resource |
|-----------|-------------|----------|
| **Template** | Standard initiatives with known patterns | [resources/template.md](resources/template.md) |
| **Methodology** | Complex multi-phase programs, novel risks | [resources/methodology.md](resources/methodology.md) |
| **Examples** | See what good looks like | [resources/examples/](resources/examples/) |
| **Rubric** | Validate before delivering | [resources/evaluators/rubric_chain_spec_risk_metrics.json](resources/evaluators/rubric_chain_spec_risk_metrics.json) |

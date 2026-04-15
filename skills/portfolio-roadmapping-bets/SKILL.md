---
name: portfolio-roadmapping-bets
description: Creates strategic portfolio roadmaps that size and sequence initiative bets across time horizons (H1/H2/H3), balance risk profiles (core/adjacent/transformational), and set clear exit/scale criteria for disciplined resource allocation. Use when managing multiple initiatives across time horizons, balancing risk vs return across portfolio, sizing and sequencing bets with dependencies, setting exit/scale criteria for experiments, allocating resources across innovation types, or when user mentions portfolio planning, roadmap horizons, betting framework, initiative prioritization, innovation portfolio, or resource allocation across horizons.
---
# Portfolio Roadmapping Bets

**When NOT to use:** Single initiative with clear priority (use one-pager-prd or project-risk-register instead), purely operational prioritization without strategic horizons (use prioritization-effort-impact), or no resource constraints or trade-offs.

## Workflow

Copy this checklist and track your progress:

```
Portfolio Roadmapping Bets Progress:
- [ ] Step 1: Define portfolio theme and constraints
- [ ] Step 2: Inventory and size all bets
- [ ] Step 3: Sequence bets across horizons
- [ ] Step 4: Set exit and scale criteria
- [ ] Step 5: Balance and validate portfolio
```

**Step 1: Define portfolio theme and constraints**

Clarify the strategic theme (north star), time horizons (H1/H2/H3 definitions), resource constraints (budget, people, time), and portfolio balance targets (e.g., 70/20/10 rule). See [Portfolio Theme & Constraints](#portfolio-theme--constraints) for guidance.

**Step 2: Inventory and size all bets**

List all candidate initiatives, size each by effort (S/M/L/XL) and impact potential (1x/3x/10x), categorize by type (core/adjacent/transformational), and identify dependencies. For simple cases use [resources/template.md](resources/template.md). For complex cases with 15+ bets or multiple themes, study [resources/methodology.md](resources/methodology.md).

**Step 3: Sequence bets across horizons**

Assign each bet to H1 (now), H2 (next), or H3 (later) based on dependencies, strategic timing, learning sequencing, and capacity constraints. See [Sequencing & Dependencies](#sequencing--dependencies) for sequencing heuristics.

**Step 4: Set exit and scale criteria**

For each bet, define what success looks like (scale criteria: double down, expand scope) and what failure looks like (exit criteria: kill, deprioritize, pivot). See [Exit & Scale Criteria](#exit--scale-criteria) for examples.

**Step 5: Balance and validate portfolio**

Check portfolio balance (are we too conservative or too aggressive?), validate resource feasibility (can we actually staff this?), and self-assess using [resources/evaluators/rubric_portfolio_roadmapping_bets.json](resources/evaluators/rubric_portfolio_roadmapping_bets.json). Minimum standard: ≥3.5 average score. See [Portfolio Balance Checks](#portfolio-balance-checks).

## Common Patterns

### By Portfolio Type

**Product Portfolio** (multiple features/products):
- H1: Ship quick wins and critical bugs
- H2: Strategic features with cross-product dependencies
- H3: Platform bets and R&D exploration
- Balance: 60% incremental, 30% substantial, 10% breakthrough

**Technology Portfolio** (platform, infrastructure, tech debt):
- H1: Stability, security, performance quick wins
- H2: Major migrations and platform upgrades
- H3: Next-gen architecture and tooling
- Balance: 50% maintain, 30% improve, 20% transform

**Innovation Portfolio** (R&D, experiments, ventures):
- H1: Validated experiments ready to scale
- H2: Active experiments with checkpoints
- H3: Early-stage exploration and research
- Balance: 70% core business, 20% adjacent, 10% transformational (McKinsey Horizons)

**Marketing Portfolio** (campaigns, channels, experiments):
- H1: Proven channels with optimization
- H2: New channel experiments and tests
- H3: Brand building and long-term positioning
- Balance: 70% performance marketing, 20% growth experiments, 10% brand

### By Bet Size

**Small Bets** (1-2 weeks, 1-2 people):
- Low effort, low-to-medium impact
- Use for quick wins, experiments, bug fixes
- Example: A/B test new pricing page (2 weeks, 1.2x conversion potential)

**Medium Bets** (1-3 months, 3-5 people):
- Moderate effort, moderate-to-high impact
- Use for features, improvements, small initiatives
- Example: Build seller dashboard (2 months, 1.8x seller retention)

**Large Bets** (3-6 months, 5-10 people):
- High effort, high impact
- Use for strategic initiatives, platform work, major features
- Example: Marketplace trust & safety system (5 months, 3x GMV via reduced fraud)

**X-Large Bets** (6-12+ months, 10+ people):
- Very high effort, transformational impact potential
- Use for platform rewrites, new business lines, moonshots
- Example: AI-powered recommendation engine (9 months, 10x engagement potential)

### By Risk Profile

**Core Bets** (Low Risk, Incremental Return):
- Optimize existing products/channels
- Proven approaches with clear ROI
- Example: Improve search relevance from 65% → 75% accuracy

**Adjacent Bets** (Medium Risk, Substantial Return):
- Extend to new use cases, segments, or capabilities
- Validated approach, new application
- Example: Launch seller analytics (proven feature, new user segment)

**Transformational Bets** (High Risk, Breakthrough Return):
- New business models, technologies, or markets
- Unproven approach, high uncertainty
- Example: Blockchain-based ownership system (unproven tech, could unlock new market)

## Portfolio Theme & Constraints

Define the strategic anchor for your portfolio:

**Theme**: The overarching goal (e.g., "Grow enterprise revenue 3x", "Achieve platform parity", "Launch in APAC")

**Time Horizons**:
- **H1 (Now)**: 0-6 months - High confidence, shipping soon
- **H2 (Next)**: 6-12 months - Medium confidence, in planning/development
- **H3 (Later)**: 12-24+ months - Lower confidence, exploration/research

**Resource Constraints**:
- Budget: $X available across all initiatives
- People: Y engineers, Z designers, etc. (capacity by function)
- Time: When must key milestones be hit? (launch date, board meeting, fiscal year)

**Portfolio Balance Targets**:
- Example: 70% core / 20% adjacent / 10% transformational (McKinsey Three Horizons)
- Example: 60% product features / 30% platform / 10% R&D
- Example: 50% H1 / 30% H2 / 20% H3 (de-risk near term while investing in future)

## Sequencing & Dependencies

**Types**: Technical (infrastructure), Learning (insights), Strategic (validation), Resource (capacity)

**Heuristics**: Dependencies first, learn before scaling, quick wins early, long bets start early, hedge portfolio

## Exit & Scale Criteria

**Exit** (kill): Time-based ("90 days"), Metric ("<5% adoption"), Cost (">$X"), Strategic ("market shifts")
**Scale** (double-down): Adoption (">20%"), Engagement (">3x baseline"), Revenue (">1.5x target"), Efficiency ("<$X CAC")

**Example**: AI chatbot bet | Exit: Deflection <30% after 60d OR sentiment <-20% | Scale: Deflection >50% AND sentiment >70%

## Portfolio Balance Checks

**Risk**: ✓ ~70% core, ~20% adjacent, ~10% transformational | ❌ >80% core (too safe) or >30% transformational (too risky)
**Horizon**: ✓ ~50-60% H1, ~25-30% H2, ~15-20% H3 | ❌ >70% H1 (no future) or >40% H3 (no near-term)
**Capacity**: Effort ≤ capacity × 0.8 (20% slack) | Example: 10 eng → 48 EM/6mo → max 38 EM in H1
**Impact**: Portfolio ladders to theme (risk-adjusted) | Example: "3x revenue" → bets sum to 4.7x potential → 50% fail = 2.35x expected → add more bets

## Guardrails

**Problem Framing**:
- ❌ Vague theme like "improve product" → ✓ Specific like "Reduce churn from 5% to 2% in 12 months"
- ❌ No constraints (infinite resources) → ✓ Explicit budget, people, time limits
- ❌ Missing portfolio balance targets → ✓ Define risk tolerance (e.g., 70/20/10)

**Bet Sizing**:
- ❌ Effort in person-days without context → ✓ Use S/M/L/XL relative sizing
- ❌ Impact as vague "high/medium/low" → ✓ Use multipliers (1x/3x/10x) or concrete metrics
- ❌ All bets are "high priority" → ✓ Force-rank or categorize by type

**Sequencing**:
- ❌ No dependencies identified → ✓ Map technical, learning, strategic dependencies
- ❌ All bets in H1 (wish list) → ✓ Realistic capacity-constrained sequencing
- ❌ No rationale for sequence → ✓ Explain why A before B (dependency, learning, quick win)

**Exit & Scale Criteria**:
- ❌ No criteria (just "we'll see") → ✓ Specific metrics and timelines for kill/scale decisions
- ❌ Only exit criteria (pessimistic) → ✓ Include scale criteria (what does wild success look like?)
- ❌ Unmeasurable criteria → ✓ Use quantifiable metrics with baselines

**Portfolio Balance**:
- ❌ All core (too safe) or all transformational (too risky) → ✓ Balanced risk distribution
- ❌ Sum of efforts exceeds capacity → ✓ Effort ≤ capacity × 0.8 (20% slack for unknowns)
- ❌ Expected impact below strategic goal → ✓ Portfolio ladders up to theme with risk adjustment

## Quick Reference

**Resources**:
- [resources/template.md](resources/template.md) - Portfolio roadmap structure and bet template
- [resources/methodology.md](resources/methodology.md) - Horizon planning, bet sizing frameworks, portfolio balancing techniques
- [resources/evaluators/rubric_portfolio_roadmapping_bets.json](resources/evaluators/rubric_portfolio_roadmapping_bets.json) - Quality criteria for portfolio roadmaps

**Success Criteria**:
- ✓ Strategic theme is clear and measurable
- ✓ All bets sized by effort (S/M/L/XL) and impact (1x/3x/10x)
- ✓ Bets sequenced across H1/H2/H3 with dependency rationale
- ✓ Exit and scale criteria defined for each bet
- ✓ Portfolio balanced across risk profiles and horizons
- ✓ Total effort ≤ team capacity (with 20% slack)
- ✓ Expected portfolio impact ≥ strategic goal (risk-adjusted)

**Common Mistakes**:
- ❌ No strategic theme → roadmap becomes random wish list
- ❌ All bets sized "Large" → no useful prioritization
- ❌ No exit criteria → sunk cost fallacy, zombie projects
- ❌ Portfolio imbalanced → all quick wins (no future) or all moonshots (no near-term value)
- ❌ Dependencies ignored → H1 bets blocked by H2 infrastructure
- ❌ Over-capacity → team burns out, quality suffers
- ❌ Under-ambitious → portfolio impact below strategic goal even if everything succeeds

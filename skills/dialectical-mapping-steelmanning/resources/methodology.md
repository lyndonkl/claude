# Dialectical Mapping & Steelmanning - Advanced Methodology

## Workflow

Copy this checklist for advanced cases:

```
Advanced Dialectical Mapping:
- [ ] Step 1: Assess complexity (multi-party, nested, empirical-normative mix)
- [ ] Step 2: Apply advanced steelmanning techniques
- [ ] Step 3: Map principle hierarchies and conflicts
- [ ] Step 4: Generate synthesis using advanced patterns
- [ ] Step 5: Validate synthesis with adversarial testing
```

**Step 1: Assess complexity**

Identify which advanced techniques apply: multi-party dialectics (>2 positions), nested dialectics (positions are themselves syntheses), principle hierarchies (multiple conflicting values), empirical-normative mix (fact vs value questions), or power dynamics (conflicts of interest). See technique selection below.

**Step 2: Apply advanced steelmanning**

Use [Toulmin Argumentation Model](#1-toulmin-argumentation-model) to strengthen steelmans, identify implicit warrants, and expose assumptions. Check for [Common Fallacies](#2-common-fallacies-in-dialectical-reasoning) that weaken arguments.

**Step 3: Map principle hierarchies**

For multi-dimensional tradeoffs, use [Principle Mapping](#3-principle-mapping-hierarchies) to structure values. Identify which principles are means vs ends, where they conflict, and potential higher-order principles.

**Step 4: Generate synthesis**

Apply advanced patterns: [Multi-Party Synthesis](#4-multi-party-dialectics), [Nested Dialectics](#5-nested-dialectics), [Empirical-Normative Separation](#6-empirical-vs-normative-questions), or [Power Dynamics Handling](#7-power-dynamics-and-conflicts-of-interest).

**Step 5: Validate synthesis**

Use [Synthesis Validation Techniques](#8-synthesis-validation-techniques) including adversarial testing, edge case analysis, and unintended consequences check.

---

## 1. Toulmin Argumentation Model

**Use when**: Steelmanning complex arguments with implicit assumptions, strengthening argument structure, or identifying weak points charitably.

### Model Structure

**Claim** (C): What position asserts
**Data** (D): Evidence supporting claim
**Warrant** (W): Logical connection between data and claim (often implicit)
**Backing** (B): Support for the warrant
**Qualifier** (Q): Degree of certainty (always, probably, unless...)
**Rebuttal** (R): Conditions under which claim doesn't hold

### Application to Steelmanning

**Standard steelman**: "Position A wants X because Y."

**Toulmin-enhanced steelman**:
- **Claim**: X is the right choice
- **Data**: Y (evidence, context, examples)
- **Warrant**: "Given Y, X follows because [logical connection]"
- **Backing**: [Why the warrant is valid—theory, principle, precedent]
- **Qualifier**: "X is right **unless** [edge cases, conditions]"
- **Rebuttal**: "X fails if [specific scenarios]"

### Example

**Topic**: Should we use microservices architecture?

**Basic steelman (weak)**: "Microservices scale better."

**Toulmin steelman (strong)**:
- **Claim**: We should use microservices
- **Data**: Our user base will grow 10x next year; different services have different scaling needs (API: 100x, admin: 2x)
- **Warrant**: When services have heterogeneous scaling requirements, independent deployability enables cost-efficient scaling (scale what needs scaling, not entire monolith)
- **Backing**: Economic principle (marginal cost optimization) + engineering precedent (Netflix, Uber scaled via microservices)
- **Qualifier**: Microservices are appropriate **if** org can handle operational complexity (monitoring, distributed tracing, service mesh)
- **Rebuttal**: Falls apart if team < 20 engineers (coordination overhead exceeds benefits) or if services are tightly coupled (defeats independence)

**Result**: Stronger steelman that acknowledges scope conditions and failure modes.

---

## 2. Common Fallacies in Dialectical Reasoning

### Strawman (The Problem Steelmanning Solves)

**Definition**: Misrepresenting opponent's position to make it easier to attack.
**Example**: "Position A wants speed, so they don't care about quality."
**Fix**: Steelman: "Position A prioritizes speed because early market entry captures compounding advantages, accepting higher initial defect risk as a calculated tradeoff."

### False Dichotomy

**Definition**: Framing as binary choice when other options exist.
**Example**: "We must choose growth OR profitability."
**Detection**: Ask: "Are these actually mutually exclusive? Can we do both sequentially, conditionally, or on different dimensions?"
**Fix**: Synthesis via temporal, conditional, or dimensional separation patterns.

### False Equivalence

**Definition**: Treating unequal positions as equally valid.
**Example**: "Both sides have good points" when one position has stronger evidence.
**Fix**: Steelman both, but acknowledge asymmetry. Synthesis can lean heavily toward stronger position while incorporating weaker position's safeguards.

### Slippery Slope

**Definition**: Assuming small step inevitably leads to extreme outcome without justification.
**Example**: "If we allow any technical debt, we'll end up with unmaintainable codebase."
**Fix**: Identify intermediate stopping points, decision criteria, compensating controls. "Technical debt is acceptable if: (1) repayment plan exists, (2) debt tracked publicly, (3) quarterly budget for paydown."

### Appeal to Extremes

**Definition**: Judging position by worst-case misuse rather than typical application.
**Example**: "Decentralization leads to chaos" (judging by anarchy rather than reasonable autonomy).
**Fix**: Steelman with realistic implementation, boundaries, guardrails. "Decentralized execution with centralized strategy and escalation paths."

### Begging the Question

**Definition**: Assuming the conclusion in the premise.
**Example**: "We should centralize because centralization works better."
**Detection**: Check if warrant is circular. Does argument provide independent evidence?
**Fix**: Identify actual evidence or principle. "Centralize when coordination costs of decentralization exceed benefits of local optimization—measurable via cycle time, error rates, duplication metrics."

---

## 3. Principle Mapping & Hierarchies

**Use when**: Multiple conflicting values (speed, quality, cost, equity, freedom), need to prioritize principles, or synthesis requires identifying higher-order principle.

### Principle Types

**Instrumental principles** (means to an end): Speed, cost-efficiency, consistency, simplicity
**Terminal principles** (ends in themselves): Human wellbeing, freedom, fairness, truth

### Mapping Process

1. **List all principles** invoked by both positions
2. **Categorize**: Instrumental vs terminal
3. **Identify conflicts**: Which principles oppose each other?
4. **Find hierarchy**: Are conflicting principles actually at different levels? Can instrumental principle be reframed to serve terminal principle better?

### Example

**Debate**: Privacy vs Security (government encryption backdoors)

**Position A (Privacy)**: No backdoors. Principles: Individual freedom, protection from overreach, right to privacy.

**Position B (Security)**: Backdoors for law enforcement. Principles: Public safety, crime prevention, national security.

**Principle mapping**:
- **Terminal principles**: Individual freedom (A), Public safety (B)
- **Conflict**: These ARE genuinely opposed (zero-sum in some cases)
- **Instrumental question**: Do backdoors actually increase security? (Empirical question—creates vulnerability for adversaries too)

**Higher-order principle**: "Maximize security for law-abiding citizens"

**Synthesis**: No backdoors (protects against authoritarian abuse and adversarial exploitation), but strong metadata analysis, international cooperation on criminal activity, investment in other investigative techniques. Accepts that some investigations are harder, rejects that backdoors materially improve security given systemic risks.

**Result**: Synthesis leans toward Privacy position but for Security reasons (backdoors undermine security). Reframes apparent conflict.

---

## 4. Multi-Party Dialectics

**Use when**: More than 2 positions (e.g., A vs B vs C vs D).

### Approach 1: Pairwise Comparison

1. Pick two dominant positions (A vs B)
2. Synthesize to C'
3. Compare C' vs remaining position C
4. Synthesize to C''
5. Repeat until all positions incorporated

**Limitation**: Order-dependent. Different pairing order may yield different synthesis.

### Approach 2: Principle Clustering

1. Map all positions to underlying principles
2. Group positions by shared principles
3. Identify principle conflicts (not position conflicts)
4. Synthesize at principle level
5. Derive concrete approach from principle synthesis

**Example**:

**Debate**: How to structure engineering team (100 engineers)?

**Position A**: Centralized platform team builds shared services, product teams consume
**Position B**: Fully autonomous product teams, each owns full stack
**Position C**: Matrix org, engineers report to tech lead (for skills) and product manager (for direction)
**Position D**: Rotate engineers across teams quarterly for knowledge sharing

**Principle mapping**:
- A values: Consistency, reuse, economies of scale (instrumental)
- B values: Autonomy, speed, end-to-end ownership (instrumental)
- C values: Skill development, career growth (instrumental)
- D values: Knowledge distribution, bus factor reduction (instrumental)

**Terminal goal (all positions)**: Maximize product delivery velocity AND quality

**Synthesis**: Hybrid model—
- Platform team for true shared infrastructure (data pipeline, auth, payments—things with network effects or compliance requirements)
- Product teams own full stack for product-specific features (autonomy where it matters)
- Guilds for skill development (engineers self-organize by discipline—frontend, backend, data)
- 6-month rotations optional for L3-L4 engineers (knowledge sharing without mandating churn)

**Result**: Incorporates elements from all four positions, structured by principle (platform for scale, autonomy for speed, guilds for growth, optional rotation for knowledge).

---

## 5. Nested Dialectics

**Use when**: One of the "positions" is itself a synthesis of sub-positions. Positions have internal contradictions.

### Structure

**Position A**: Synthesis of A1 vs A2
**Position B**: Synthesis of B1 vs B2
**Meta-synthesis**: Resolve A vs B at higher level

### Example

**Debate**: How should AI companies handle safety vs capability development?

**Position A (Safety-first)**: Is itself a synthesis of:
- A1: Pause all development until alignment solved
- A2: Develop capabilities slowly with extensive testing

**Position B (Capability-first)**: Is itself a synthesis of:
- B1: Race to AGI (winner determines future)
- B2: Develop capabilities, use them to solve alignment

**Meta-synthesis approach**:

1. **Steelman sub-positions** (A1, A2, B1, B2)
2. **Identify that A vs B is false dichotomy**: Actually four positions with different combinations of beliefs about:
   - How solvable is alignment? (A1: very hard, A2/B2: tractable, B1: solve after)
   - What are risks of delay? (A: manageable, B1: existential, B2: medium)
3. **Reframe around cruxes**: Not safety vs capability, but **beliefs about alignment difficulty and delay risks**
4. **Synthesis based on empirical assessment**: If alignment progress stalls (trigger), slow capability development (A2). If alignment progresses faster than expected (trigger), maintain pace (B2). Never pure A1 (pause is unilateral disadvantage) or B1 (race without guardrails is reckless).

**Result**: Conditional synthesis that responds to empirical evidence, not fixed binary.

---

## 6. Empirical vs Normative Questions

**Use when**: Debate mixes factual questions (what IS) with value questions (what SHOULD BE).

### Separation Strategy

1. **Decompose debate** into empirical claims vs normative claims
2. **Empirical claims**: Resolvable via evidence (in principle). Highlight these as **cruxes**—if evidence changes, does position change?
3. **Normative claims**: Value judgments. Require principle-level resolution, not evidence.
4. **Synthesize separately**: Agree on facts where possible, then resolve value conflict conditional on facts.

### Example

**Debate**: Should we implement remote-first work policy?

**Mixed arguments**:
- Position A: "Remote work hurts productivity" (empirical) + "Companies should maximize productivity" (normative)
- Position B: "Remote work improves wellbeing" (empirical) + "Employee wellbeing matters more than marginal productivity" (normative)

**Separation**:

**Empirical questions** (resolvable with data):
1. Does remote work reduce productivity? (Measure: output metrics, project completion, code quality)
2. Does remote work improve wellbeing? (Measure: retention, satisfaction scores, burnout rates)
3. Is there variance by role? (e.g., individual contributors vs managers)

**Normative questions** (value judgments):
1. How should we weight productivity vs wellbeing?
2. What about hiring advantages (global talent pool)?
3. Long-term effects on culture, mentorship, serendipity?

**Synthesis approach**:
- **Resolve empirical questions first**: Run 6-month experiment, measure metrics
- **Conditional synthesis based on data**:
  - If productivity unchanged or improves → Remote-first (preserves wellbeing, no cost)
  - If productivity declines < 10% but wellbeing/retention improves → Remote-first (accept tradeoff)
  - If productivity declines > 10% → Hybrid (2-3 days office for collaboration, 2-3 remote for focus)
- **Re-evaluate quarterly**: Track metrics, adjust policy

**Result**: Separates empirical cruxes from value questions, makes synthesis conditional on evidence.

---

## 7. Power Dynamics and Conflicts of Interest

**Use when**: Debate involves parties with different power, resources, or incentives. "Disagreement" may be conflict of interest, not idea conflict.

### Detection

**Signs of power dynamics**:
- One position benefits speaker/advocate materially (financial, status, control)
- Asymmetric stakes (one side risks much more)
- Historical power imbalance between advocates
- Debate framing obscures who benefits ("rising tide lifts all boats" when boats are different sizes)

### Approach

1. **Make power dynamics explicit**: Who benefits from each position? What are material stakes?
2. **Separate ideas from interests**: Steelman arguments independent of advocate motives
3. **Synthesis must address structural issues**: Can't resolve via "better ideas" if problem is power imbalance
4. **Compensating mechanisms**: If synthesis leans toward powerful party's position, include safeguards for less powerful

### Example

**Debate**: Should gig economy platforms classify workers as employees vs independent contractors?

**Position A (Contractor status)**: Flexibility, entrepreneurial freedom, lower costs (enables more work)
**Position B (Employee status)**: Benefits, job security, labor protections

**Power dynamic**: Platforms have massive information/resource advantage, legal teams, lobbying. Workers individually have minimal bargaining power.

**Steelman both arguments** (independent of power):
- A: Flexibility IS valuable for many workers (students, retirees, side hustlers)
- B: Protections ARE necessary for full-time gig workers (no healthcare, no unemployment insurance)

**Synthesis that addresses power**:
- **Classification by hours**: <20 hrs/week = contractor (flexibility preserved), ≥20 hrs/week = employee (protections for full-timers)
- **Portable benefits**: Industry-wide benefits fund (platforms contribute per worker-hour, workers access regardless of hours)
- **Collective bargaining**: Workers can organize without classification change (addresses power imbalance directly)

**Result**: Synthesis recognizes power dynamic, doesn't just "split difference on ideas."

---

## 8. Synthesis Validation Techniques

### Adversarial Testing

**Method**: Inhabit each original position and attack the synthesis.

**Questions to ask as Position A partisan**:
- Does synthesis abandon my core principle?
- Is this really "synthesis" or capitulation to Position B?
- What tradeoffs am I being asked to accept that Position B isn't?

**Repeat as Position B partisan.**

**Pass criteria**: Synthesis survives critique from both sides, or critiques cancel out (each side sees it as slight lean toward other, suggesting balance).

### Edge Case Analysis

**Method**: Test synthesis with extreme scenarios.

**Example**: "Move fast with guardrails" synthesis

**Edge cases**:
- High-risk domain (healthcare, finance) → Guardrails insufficient?
- Novel technology → Guardrails unknown?
- Aggressive competitor → Speed advantage evaporates?

**Evaluation**: Does synthesis break down in edge cases? If yes, refine with conditional logic ("In high-risk domains, prioritize guardrails over speed").

### Unintended Consequences

**Method**: Consider second-order effects, perverse incentives, long-term dynamics.

**Example**: "Profitable growth" synthesis (grow as fast as unit economics allow)

**Unintended consequences**:
- Focus on profitable channels may miss future market shifts (addressable market shrinks)
- Discipline to say no may calcify into risk-aversion
- LTV:CAC metric may be gamed (optimize metric, not underlying economics)

**Fix**: Add monitoring ("Review addressable market quarterly"), decision criteria ("Experiment with 10% budget in unproven channels"), and metric audits ("Validate LTV assumptions annually").

### Synthesis Stability Test

**Question**: Is synthesis stable, or does it collapse back to Position A/B under pressure?

**Example**: "Centralize strategy, decentralize execution"

**Pressure test**:
- Strategy team starts specifying execution details → Collapse to centralization
- Execution teams ignore strategy → Collapse to full autonomy
- Gray-zone decisions escalate constantly → Synthesis unworkable

**Fix**: Define clear boundaries ("Strategy sets goals and constraints, not tactics"), escalation criteria ("Escalate if execution conflicts with cross-team dependency"), and feedback loop ("Execution teams input to strategy quarterly").

---

## 9. Advanced Synthesis Patterns

### Pattern 6: Principle Inversion

**Structure**: Both positions optimize for same principle but in opposite ways. Synthesis finds third approach to principle.

**Example**: "Maximize developer productivity"
- Position A: Remove all process (friction kills productivity)
- Position B: Standardize everything (consistency enables productivity)

**Synthesis**: Identify which types of friction help vs hurt. Remove ceremony (status meetings, approval chains) that wastes time. Add structure (linters, type systems, templates) that reduces cognitive load. Not "some process," but "automate what can be automated, remove what can't."

### Pattern 7: Time-Horizon Mismatch

**Structure**: Positions optimize for different time horizons. Synthesis balances short-term and long-term.

**Example**: Technical debt
- Position A: Never take debt (compound interest kills you)
- Position B: Always optimize for shipping (future is uncertain)

**Synthesis**: Allow debt with explicit interest rate. "Accept debt if repayment cost < 2x initial cost AND payback within 6 months. Track debt-hours, allocate 20% of sprint to paydown."

### Pattern 8: Stakeholder Rotation

**Structure**: Different stakeholders have different needs. Synthesis rotates optimization target.

**Example**: Product priorities
- Customer wants features
- Engineering wants technical excellence
- Business wants revenue

**Synthesis**: Quarterly rotation. Q1: Customer (ship requested features). Q2: Engineering (refactor, test coverage, performance). Q3: Business (monetization, growth experiments). Q4: Integration (synthesize learnings). Over 12 months, all stakeholders served.

### Pattern 9: Threshold-Based Switching

**Structure**: Position A below threshold, Position B above threshold.

**Example**: Meeting culture
- Position A: Async-first (meetings are waste)
- Position B: High-bandwidth sync (Zoom for everything)

**Synthesis**: Use async for <5 people OR routine updates. Use sync for ≥5 people AND novel/contentious discussion. Threshold-based decision rule.

### Pattern 10: Modular Synthesis

**Structure**: Different parts of system optimize differently.

**Example**: Software architecture
- Core services: Optimize for reliability (test coverage, formal methods, slow deploys)
- Experimentation layer: Optimize for speed (feature flags, canary rollouts, fast iteration)
- Infrastructure: Optimize for cost (spot instances, autoscaling)

**Synthesis**: Not one-size-fits-all. Different modules, different optimization criteria, unified by interfaces and observability.

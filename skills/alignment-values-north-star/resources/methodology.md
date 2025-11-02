# Alignment Framework Methodology for Scaling Organizations

## Table of Contents

- [When to Use This Methodology](#when-to-use-this-methodology)
- [Refining Existing Values](#refining-existing-values)
- [Multi-Team Alignment Frameworks](#multi-team-alignment-frameworks)
- [Building Decision Frameworks for Autonomy](#building-decision-frameworks-for-autonomy)
- [Common Scaling Challenges](#common-scaling-challenges)
- [Case Study: Company-Wide Values Refresh](#case-study-company-wide-values-refresh)

---

## When to Use This Methodology

Use this methodology when:
- **Scaling organization** (50+ people, multiple teams)
- **Existing values need refinement** (outdated, vague, or conflicting)
- **Multiple teams need alignment** (silos forming, conflicting priorities)
- **Need decision framework** (enabling autonomy while maintaining alignment)
- **Values drift** (stated values don't match actual behavior)

For new teams starting from scratch, use `template.md`.

---

## Refining Existing Values

### Why Refine?

Common triggers:
- Values are vague ("be excellent") - no operational guidance
- Values conflict with reality (say "innovation" but punish failures)
- New priorities emerged (e.g., shift from growth to profitability)
- Multiple acquisitions brought different cultures
- Team doesn't reference values in decisions (not useful)

### Audit Current State

**Step 1: Document existing values**
- What are stated values? (website, onboarding docs, walls)
- What are *actual* values? (observed in decisions, promotions, conflicts)
- Gap analysis: Where do stated and actual diverge?

**Step 2: Interview stakeholders**

Questions to ask:
- "What do we truly value here? (not what we say we value)"
- "Tell me about a tough decision - what guided it?"
- "What behaviors get rewarded? Punished?"
- "When have our values helped you? Hindered you?"
- "What values are missing that we need?"

**Step 3: Analyze decisions**

Review past 6-12 months:
- Hiring/firing decisions - what values were applied?
- Product prioritization - what drove choices?
- Resource allocation - what got funded/cut?
- Conflict resolution - how were tradeoffs made?

Look for patterns revealing true values.

### Refinement Process

**Option A: Evolve existing values**

Keep core values but make them clearer:

Before: "Customer obsession"
After: "Customer obsession: We prioritize long-term customer success over short-term metrics. When in doubt, we ask 'what would create lasting value for customers?' and optimize for that, even if it delays revenue."

**Add:**
- Specific definition
- Why it matters
- Decision examples
- Anti-patterns

**Option B: Retire and replace**

When existing values don't serve:
1. Acknowledge what's changing and why
2. Thank the old values for their service
3. Introduce new values with context
4. Show connection (evolution, not rejection)

Example:
- Old: "Move fast and break things" (startup phase)
- New: "Move deliberately with customer trust" (scale phase)
- Context: "We used to optimize for speed because we needed product-market fit. Now we optimize for reliability because customers depend on us."

### Rollout Strategy for Refined Values

**Phase 1: Leadership alignment (Week 1-2)**
- All leaders can articulate values in their own words
- Leadership team models values in visible decisions
- Leaders prepared to answer "why change?" and "what's different?"

**Phase 2: Cascading communication (Week 3-4)**
- All-hands presentation (context, new values, Q&A)
- Team-level workshops (apply to team decisions)
- 1:1s address individual concerns

**Phase 3: Integration (Month 2-3)**
- Update hiring rubrics
- Update performance review criteria
- Reference in decision memos
- Celebrate examples of values in action

**Phase 4: Reinforcement (Ongoing)**
- Monthly: Leaders share values-driven decisions
- Quarterly: Audit if values are being used
- Annually: Refresh based on feedback

---

## Multi-Team Alignment Frameworks

### Challenge: Silos & Conflicting Priorities

As organizations scale:
- Teams optimize for local goals
- Priorities conflict (eng wants stability, product wants speed)
- Decisions require escalation (autonomy breaks down)
- Values interpreted differently across teams

### Layered Alignment Framework

**Layer 1: Company-Wide North Star & Values**

Company level (50+ people, multiple teams):
- North Star: Aspirational direction for whole company
- Values: 3-5 company-wide principles
- Decision Tenets: Company-level tradeoff guidance

Example:
```
Company North Star: "Empower every team to ship confidently"

Company Values:
1. Customer trust over growth metrics
2. Clarity over consensus
3. Leverage through platforms

Company Decision Tenets:
- When product and platform conflict, platforms enable more product value long-term
- When speed and reliability conflict, we choose reliability for critical paths
```

**Layer 2: Function-Level Values & Tenets**

Engineering, Product, Design, Sales functions each add:
- Function-specific interpretation of company values
- Function decision tenets (within company constraints)
- Function behaviors

Example (Engineering):
```
Engineering North Star: "Enable product velocity through reliable platforms"

Engineering Values (extending company):
1. Customer trust → "We treat production as sacred"
2. Clarity → "We write decisions down before coding"
3. Leverage → "We build platforms, not point solutions"

Engineering Decision Tenets:
- When feature velocity and platform health conflict, platform health wins
- When local optimization and system optimization conflict, system wins
- When urgency and testing conflict, we ship with tests (move test left)
```

**Layer 3: Team-Level Rituals & Practices**

Individual teams implement values through rituals:
- How we run standups
- How we make architectural decisions
- How we handle incidents
- How we onboard new members

Example (Platform Team):
```
Rituals embodying "Platform enables product velocity":
- Weekly: Office hours for product teams (30 min slots)
- Monthly: Platform roadmap review with product input
- Quarterly: Platform usability study with product engineers
```

### Alignment Check: Nested Frameworks

Test if layers are aligned:

| Company Value | Function Interpretation | Team Practice |
|---------------|------------------------|---------------|
| Customer trust | Engineering: Production is sacred | Platform: 99.9% SLA, postmortems within 24hr |
| Clarity | Engineering: Write before coding | Platform: RFC required for API changes |
| Leverage | Engineering: Platforms not point solutions | Platform: Reusable libraries, not feature forks |

If a team practice doesn't connect to function value → doesn't connect to company value → misaligned.

---

## Building Decision Frameworks for Autonomy

### Problem: Alignment vs Autonomy Tension

- Too much alignment → slow, needs approval for everything
- Too much autonomy → teams diverge, duplicate work, conflict

Goal: **Aligned autonomy** - teams make fast local decisions within clear constraints.

### Decision Tenet Pattern

**Format:**
```
When {situation with tradeoff}, we choose {option A} over {option B} because {rationale}.
```

**Characteristics of good tenets:**
- Specific (not "be excellent")
- Tradeoff-oriented (acknowledges what we're NOT optimizing)
- Contextual (explains why this choice for us)
- Actionable (guides concrete decisions)

**Example Tenets:**

Engineering:
```
When latency and throughput conflict, we optimize for latency (p95 < 100ms)
because our users are professionals in workflows where milliseconds matter.
```

Product:
```
When power-user features and beginner simplicity conflict, we choose beginner simplicity
because growing the user base is our current strategic priority (2024 goal: 10x users).
```

Sales:
```
When deal size and customer fit conflict, we choose customer fit
because high-churn enterprise customers damage our brand and reference-ability.
```

### Decision Authority Matrix (RACI + Values)

Map which decisions require escalation vs can be made locally:

| Decision Type | Team Authority | Escalation Trigger | Values Applied |
|---------------|----------------|-------------------|----------------|
| API design for team features | Team decides | If cross-team impact | Platform leverage |
| Production incident response | On-call decides | If customer data risk | Customer trust |
| Prioritization within quarter | PM decides | If OKR conflict | Quarterly focus |
| Hiring bar | Team + function | Never lower bar | Excellence standard |

**Escalation triggers** (when to involve leadership):
- Cross-team conflict on priorities
- Values conflict (two values in tension)
- Precedent-setting decision (will affect future teams)
- High-stakes outcome (>$X, >Y customer impact)

### Operationalizing Tenets in Decisions

**Step 1: Frame decision with tenets**

Bad decision memo:
```
We should build feature X.
```

Good decision memo:
```
Decision: Build feature X

Relevant tenets:
- "When power-users and beginners conflict, choose beginners" → Feature X is beginner-focused ✓
- "When latency and features conflict, choose latency" → Feature X adds 20ms latency ✗
- "Platform leverage over point solutions" → Feature X is platform component ✓

Recommendation: Build feature X BUT optimize latency first (refactor API)
Estimate: +2 weeks for latency optimization, worth it per tenets
```

**Step 2: Audit tenet usage**

Quarterly review:
- How many decisions referenced tenets?
- Which tenets are most/least used?
- Where did tenets conflict? (may need refinement)
- Where did teams escalate unnecessarily? (need clearer tenet)

---

## Common Scaling Challenges

### Challenge 1: Values Drift (Stated ≠ Actual)

**Symptoms:**
- Leaders say "we value X" but reward Y
- Values posters on walls, but no one references them
- Cynicism about values ("just marketing")

**Diagnosis:**
- Review promotions: Who gets promoted? What values did they embody?
- Review tough decisions: Which values were actually applied?
- Interview employees: "Do you use our values? When? How?"

**Fix:**
1. **Acknowledge drift** ("Our stated values haven't matched our actions")
2. **Choose**: Either change stated values to match reality OR change behavior to match values
3. **Leader modeling**: Leaders publicly use values in decisions
4. **Consequences**: Promotions/rewards explicitly tied to values

**Example:**
```
Stated: "We value work-life balance"
Reality: Promotions go to those who work weekends

Fix Option A (change stated): "We value high output and intense commitment"
Fix Option B (change reality): "Promotions now require sustainable pace, not just output"
```

### Challenge 2: Values Conflict (Internal Tensions)

**Symptoms:**
- Teams cite different values for same decision
- Paralysis (can't decide because values conflict)
- Escalation overload (everything needs leadership tiebreak)

**Diagnosis:**
- Map values pairwise: When do Value A and Value B conflict?
- Identify repeated conflict scenarios
- Ask: Is this values conflict or unclear priority?

**Fix: Priority tenets**

When values conflict, state priority:
```
"Speed" and "Quality" both matter, but:
- For customer-facing features: Quality > Speed (customer trust)
- For internal tools: Speed > Perfection (iterate fast)
- For platform APIs: Quality > Speed (leverage means hard to change)
```

### Challenge 3: Multi-Team Misalignment

**Symptoms:**
- Teams build conflicting solutions
- Escalation required for every cross-team decision
- "Not my priority" culture

**Diagnosis:**
- Map team goals: Do team OKRs align?
- Check incentives: What does each team get rewarded for?
- Review cross-team projects: How often do they succeed?

**Fix: Nested alignment framework (see above)**

Plus:
- **Cross-team rituals**: Monthly

 syncs on interdependencies
- **Shared metrics**: At least one metric in common across teams
- **Rotation**: Engineers rotate across team boundaries

---

## Case Study: Company-Wide Values Refresh

### Context

**Company**: SaaS product, 150 employees, 8 engineering teams
**Trigger**: Rapid growth (30 → 150 people in 18 months), old startup values not working
**Old values**: "Move fast", "Customer obsessed", "Scrappy"
**Problem**: "Move fast" causing production incidents; "Scrappy" justifying technical debt that slows product

### Process

**Month 1: Discovery**
- Interviewed 40 employees (all levels, all functions)
- Reviewed 20 major decisions (what values were actually applied?)
- Surveyed all employees: "What do we truly value? What should we value?"

**Key findings:**
- "Move fast" interpreted as "ship without testing" (not intended)
- "Customer obsessed" unclear (speed to market vs quality vs support?)
- "Scrappy" became excuse for poor tooling
- **Missing value**: Reliability/trust (now serving enterprise customers)

**Month 2: Leadership Workshop**
- All directors + exec team (2-day offsite)
- Reviewed discovery findings
- Drafted new values + tenets
- Pressure-tested against real decisions

**New values (refined):**
1. **Customer trust over growth metrics**
   - Tenet: "When feature velocity and reliability conflict, reliability wins for core workflows"
   - Evolution of "customer obsessed" (clarified: long-term trust, not short-term features)

2. **Leverage through platforms**
   - Tenet: "When team autonomy and platform standards conflict, we choose standards for leverage"
   - Evolution of "scrappy" (still efficient, but via platforms not point solutions)

3. **Clarity over consensus**
   - Tenet: "When speed and buy-in conflict, we choose fast decision with clear rationale over slow consensus"
   - New value (addresses decision paralysis)

**Month 3: Rollout**
- All-hands (CEO presented, Q&A, examples of how values applied to recent decisions)
- Team workshops (each team applied to their context)
- Updated hiring rubric (added values-based questions)
- Updated performance review (added values section)

**Month 4-6: Reinforcement**
- Weekly exec team review: "What values-driven decisions did we make?"
- Monthly all-hands: Celebrate values in action (shoutouts)
- Quarterly survey: "Are we living our values?"

### Results (6 months later)

**Wins:**
- Production incidents dropped 60% ("Customer trust" being applied)
- Engineering happiness up 25% (better tooling via "leverage through platforms")
- Decision velocity up (no more endless debates, "clarity over consensus")
- Values referenced in 80% of decision memos (actual usage)

**Challenges:**
- Some engineers missed "move fast" culture (clarified: fast decisions, deliberate execution)
- Sales initially confused ("customer trust" seemed to slow deals - clarified: long-term trust creates more deals)

**Evolution (12 months):**
- Added 4th value: "Default to transparency" (based on feedback)
- Refined "leverage" tenet (too restrictive, added exceptions for experiments)

### Lessons Learned

1. **Co-create with leadership**: Top-down values fail, need buy-in from leaders who'll model them
2. **Show the evolution**: Don't reject old values, show how they evolved (honors the past)
3. **Operationalize fast**: Values are useless without tenets + integration into decisions
4. **Celebrate examples**: Abstract values need concrete stories of values in action
5. **Iterate**: Values are living, not static - update based on feedback

---

## Quality Checklist for Scaling Organizations

Before finalizing alignment framework refresh, check:

**Discovery**:
- [ ] Interviewed stakeholders across levels/functions
- [ ] Reviewed actual decisions (not just stated values)
- [ ] Identified gap between stated and actual values
- [ ] Understood why current values aren't working

**Refinement**:
- [ ] New values address root causes (not symptoms)
- [ ] Values evolved from old (honored the past)
- [ ] Values are specific and actionable (not vague platitudes)
- [ ] Tenets operationalize values (guide concrete decisions)
- [ ] Conflicts between values explicitly resolved (priority tenets)

**Multi-Team Alignment**:
- [ ] Company-wide values clear
- [ ] Function-level interpretations add specificity
- [ ] Team practices connect to function/company values
- [ ] Decision authority matrix defined (what escalates vs local)
- [ ] Cross-team conflicts have resolution process

**Rollout**:
- [ ] Leadership aligned and can model values
- [ ] Communication plan (all-hands, team workshops, 1:1s)
- [ ] Integration into systems (hiring, perf review, decision memos)
- [ ] Examples prepared (values in action stories)
- [ ] Feedback loops established (quarterly check-ins)

**Reinforcement**:
- [ ] Regular rituals (monthly values spotlights)
- [ ] Values referenced in decisions (not just posters)
- [ ] Consequences tied to values (promotions, rewards)
- [ ] Audit usage quarterly (are values being applied?)
- [ ] Iterate based on feedback (values evolve)

**Minimum standard for scaling orgs**: All checklist items completed before rollout

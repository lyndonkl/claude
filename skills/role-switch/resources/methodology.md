# Role Switch: Advanced Methodologies

## Table of Contents
1. [Stakeholder Mapping & Selection](#1-stakeholder-mapping--selection)
2. [Cognitive Empathy Techniques](#2-cognitive-empathy-techniques)
3. [Power Dynamics & Decision Authority](#3-power-dynamics--decision-authority)
4. [Synthesis Strategies](#4-synthesis-strategies)
5. [Facilitation for Multi-Stakeholder Alignment](#5-facilitation-for-multi-stakeholder-alignment)
6. [Advanced Patterns](#6-advanced-patterns)

## 1. Stakeholder Mapping & Selection

### RACI Matrix (Responsibility Assignment)

Map stakeholders by their relationship to the decision:

- **R** (Responsible): Does the work, executes the decision
- **A** (Accountable): Has decision authority, owns outcome (only ONE per decision)
- **C** (Consulted): Provides input, must be heard before deciding
- **I** (Informed): Notified after decision, affected but not consulted

**Example (API deprecation decision):**
- **R**: Engineering (implements deprecation, migration tooling)
- **A**: VP Engineering (final call on timeline and support model)
- **C**: Product (customer impact), Finance (revenue implications), Customer Success (migration support)
- **I**: Sales (so they can communicate to prospects), Marketing (public messaging)

**Selection rule**: Always include **A** (decision authority). Include **R** if execution feasibility is uncertain. Include **C** stakeholders with veto power or critical constraints. Consider **I** stakeholders if their reaction could derail implementation.

### Power-Interest Matrix

Map stakeholders by **power** (ability to influence decision) and **interest** (how much they care):

```
High Interest, High Power → MANAGE CLOSELY (key players)
High Interest, Low Power  → KEEP INFORMED (advocates/resistors)
Low Interest, High Power  → KEEP SATISFIED (don't let them block)
Low Interest, Low Power   → MONITOR (minimal engagement)
```

**Example (pricing change):**
- **High Power, High Interest**: CFO (margin), Sales VP (quota), top customers (retention)
- **High Power, Low Interest**: CEO (busy, delegates to CFO unless escalated)
- **Low Power, High Interest**: Individual sales reps (compensation), customer success managers (renewal risk)
- **Low Power, Low Interest**: Marketing ops (just implements new pricing in systems)

**Selection for role-switch**: Focus on high-interest stakeholders (top two quadrants). Include high-power stakeholders even if low interest (they can block). Deprioritize low-power, low-interest (not decision-critical).

### Influence Mapping (Who Influences Whom)

Some stakeholders don't decide but influence deciders:

**Example (hospital EMR selection):**
- **Formal authority**: CIO (signs contract), CFO (budget approval)
- **Informal influence**: Chief of Surgery (respected voice, if she opposes no one proceeds), Head of Nursing (staff adoption critical)
- **Technical veto**: CISO (security compliance), Legal (contract terms)

**Map influence paths**: Identify who the decision authority listens to. Include those influencers in role-switch even if they lack formal authority.

## 2. Cognitive Empathy Techniques

### Perspective-Taking Protocol

**Step 1: Inhabit the role's context**
- What is this role measured on? (OKRs, KPIs, promotion criteria)
- What are they accountable for? (what gets them fired if it fails)
- What information do they have that others don't? (asymmetric context)
- What pressures are they under? (boss's expectations, quarterly reviews, competitive threats)

**Step 2: Adopt their time horizon**
- **Short-term** (this quarter): Sales (quota), Support (ticket backlog)
- **Medium-term** (this year): Product (roadmap), Engineering (technical debt)
- **Long-term** (3+ years): Leadership (strategy), Legal (precedent setting)

Conflicts often arise from mismatched time horizons (sales wants deal today, eng sees 5-year maintenance burden).

**Step 3: Understand their incentive structure**
- **Aligned incentives**: Marketing and Sales both want customer acquisition (but marketing = leads, sales = closed deals)
- **Misaligned incentives**: Sales (maximize deal size) vs Finance (minimize discounts)
- **Perverse incentives**: Support (minimize handle time) vs Customers (thorough resolution)

**Step 4: Identify their constraints**
- **Resource constraints**: Headcount, budget, tooling access
- **Time constraints**: Quarterly deadlines, regulatory timelines, market windows
- **Process constraints**: Approval chains, audit requirements, compliance gates
- **Political constraints**: Board expectations, stakeholder promises, prior commitments

### Steel-Manning Perspectives

**Steel-manning**: Construct the *strongest possible* version of a role's position (opposite of strawman).

**Process**:
1. State their position as they would state it (use their language)
2. Identify the strongest evidence/reasoning for that position
3. Articulate what they might be right about (even if you disagree)
4. Note what legitimate values or priorities drive their stance

**Example (feature prioritization conflict):**

**Strawman (weak)**: "Sales just wants to promise customers everything to close deals, they don't care about product quality"

**Steel-man (strong)**: "Sales sees customer requests as real market signals—if multiple prospects ask for the same capability, it indicates unmet need and competitive gap. Prioritizing these features captures revenue that would otherwise go to competitors and validates product-market fit. Sales fears that saying 'no' to customer requests will result in lost deals, making it harder to hit quota, and signaling to the market that we're not responsive to customer needs."

Steel-manning builds trust when you present perspectives to stakeholders ("you see I understood your position") and surfaces legitimate concerns that deserve addressing.

### Position vs Interest Negotiation

**Position**: What they say they want (surface demand)
**Interest**: Why they want it (underlying need)

**Example**:
- **Position**: "We need this feature by Q1"
- **Interest**: "We promised a key customer in the sales cycle, and if we don't deliver we risk $500K annual contract and relationship damage"

**Why this matters**: You can often satisfy the interest without meeting the position.
- Alternative to building feature by Q1: Offer workaround solution, partner integration, or professional services to satisfy customer while buying time for proper feature in Q2.

**Uncovering interests**: Ask "why" 2-3 times:
- "Why do you want this feature?" → "Customer is asking for it"
- "Why is this customer important?" → "They're our largest account and up for renewal"
- "Why does this specific feature matter for renewal?" → "Competitor has it, they're considering switching"

Now you see the interest: competitive differentiation for retention, not the feature itself.

## 3. Power Dynamics & Decision Authority

### Decision Rights Framework

**Types of decision authority:**
- **Autocratic**: One person decides, others provide input (e.g., CEO on strategic pivot)
- **Consultative**: Decision-maker seeks input, but retains final call (e.g., PM on feature prioritization)
- **Consensus**: All stakeholders must agree (e.g., co-founders on equity split)
- **Democratic**: Majority vote (e.g., board approval)
- **Delegated**: Authority holder delegates to expert (e.g., CEO → CTO on tech stack)

**Role-switch implication**: Synthesis should acknowledge decision authority. If PM has final say on roadmap, synthesis can note "Engineering recommends X but PM decides based on customer commitments." Don't pretend consensus is required when it's not.

### Veto Power Identification

Some roles can't make the decision but can block it:

**Examples:**
- **Legal**: Can veto on liability/compliance grounds (not a suggestion, a blocker)
- **Security**: Can veto on risk grounds (breach could be existential)
- **Finance**: Can veto if budget doesn't exist (hard constraint)
- **Regulatory**: External veto (FDA, FTC, etc. can block regardless of internal consensus)

**Synthesis strategy**: Address veto-holders first. If Legal says "this contract exposes us to unacceptable IP risk," that's non-negotiable. Synthesis must either fix legal issue or find alternative path. No amount of alignment among other stakeholders overrides veto.

### Navigating Hierarchy

**Peer conflicts** (same level, e.g., VP Eng vs VP Product):
- Escalate to shared manager if consensus fails
- Frame as tradeoff for leadership to decide (don't make it personal)
- Offer to run experiment/pilot to gather data (de-emotionalize)

**Vertical conflicts** (manager vs subordinate):
- Subordinate's role: Make recommendation, provide data, articulate risks
- Manager's prerogative: Override with context subordinate may lack
- Synthesis should acknowledge manager has broader context (benefit of doubt)

**Cross-functional conflicts** (different orgs):
- Identify shared OKRs or company goals to align on
- Escalate to neutral party (e.g., COO) if functions can't resolve
- Avoid "us vs them"—frame as "how do we both win?"

## 4. Synthesis Strategies

### Sequential Decision-Making

When perspectives conflict, decompose into sequence:

**Pattern**: "Do X first (satisfies role A), then Y (satisfies role B), then Z (satisfies role C)"

**Example (build vs buy):**
- **Engineering**: "Build in-house for control"
- **Product**: "Buy to launch faster"
- **Synthesis**: "Buy now to hit market window (Product wins short-term). As we scale, evaluate build for strategic capabilities (Engineering wins long-term). Set decision checkpoint at 10K users (concrete trigger)."

**Benefits**: Reduces present conflict (only deciding immediate action), creates learning period (gather data before next decision), aligns incentives over time.

### Hybrid Approaches

Combine elements from multiple perspectives:

**Example (pricing strategy):**
- **Finance**: "Charge premium to maximize margin"
- **Sales**: "Offer competitive pricing to win deals"
- **Marketing**: "Simple, transparent pricing"
- **Synthesis**: "Tiered pricing (Finance gets premium tier, Sales gets accessible entry tier, Marketing gets 3 clear tiers with public pricing)"

**Example (work policy):**
- **Leadership**: "In-office for collaboration"
- **Employees**: "Remote for flexibility"
- **Synthesis**: "Hybrid 3 days/week in-office (Leadership gets collaboration days), 2 days remote (Employees get flexibility), core hours 10am-3pm Tue-Thu (ensures overlap)"

### Pilot/Experiment to Resolve Uncertainty

When conflict stems from different predictions, run experiment:

**Example:**
- **Sales**: "Customers will pay 20% more for premium tier"
- **Product**: "Customers are price-sensitive, will churn at higher price"
- **Synthesis**: "Run 2-week pricing test with 10% of new trials. Measure conversion rate and NPS. Decision rule: If conversion drops <5%, proceed with premium pricing. If drops >10%, stay at current price."

**Benefits**: Converts opinions to data, de-risks decision, builds consensus around evidence.

### Constraints as Creative Forcing Function

Use one role's constraint to sharpen another's solution:

**Example:**
- **Finance**: "We have $100K budget, not $500K"
- **Product**: "We want features A, B, C, D, E"
- **Synthesis**: "Budget constraint forces ruthless prioritization. Which single feature drives 80% of value? (Pareto principle). Build only that feature to MVP standard in Q1, defer B-E to Q2 based on usage data from A."

Constraint (budget) forces clearer thinking about value (Product benefits from discipline).

### Risk Mitigation for Fears

Address each role's top fear with specific mitigation:

**Example (technical migration):**
- **Engineering fear**: "Migration will surface hidden dependencies and blow up timeline"
  - **Mitigation**: 2-week technical spike to map dependencies, discovery phase with 30% time buffer
- **Product fear**: "Feature freeze will let competitor gain ground"
  - **Mitigation**: Incremental migration (no freeze), maintain feature velocity on new system
- **User fear**: "Downtime will disrupt workflows"
  - **Mitigation**: Blue-green deployment, rollback plan, phased rollout starting with low-risk cohort

Naming fears explicitly and mitigating shows you took each perspective seriously.

## 5. Facilitation for Multi-Stakeholder Alignment

### Pre-Work for Alignment Meetings

**Before bringing stakeholders together:**
1. **Identify decision framing**: What exactly are we deciding? (avoid vague "alignment meeting")
2. **Pre-socialize positions**: Talk to each stakeholder 1:1 to understand their stance (no surprises in group)
3. **Find common ground**: Identify 2-3 shared goals to anchor discussion
4. **Prepare synthesis options**: Come with 2-3 proposals that address key interests (don't start from blank slate)
5. **Clarify decision authority**: Who has final say if consensus fails?

### Facilitation Techniques

**Round-robin sharing** (ensure all voices heard):
- Each stakeholder shares their perspective (2 min, uninterrupted)
- Others listen without rebutting (defer debate to later)
- Captures positions before conflict dominates

**Interest articulation** (go beneath positions):
- Facilitator asks: "What outcome would satisfy your core need?" (not "what do you want us to do")
- Reframe positions as interests: "I hear you want X because you're trying to achieve Y"

**Tradeoff matrix** (make tradeoffs explicit):
- On whiteboard, list options across top, criteria down left side
- Score each option (1-5) against each criterion
- Visually shows why no option is perfect (builds realistic expectations)

**Consensus-building ladder**:
1. **Full agreement**: Everyone enthusiastically supports
2. **Agreement with minor reservations**: Support with noted concerns
3. **Support with significant reservations**: "I disagree but won't block"
4. **Abstain**: "I have no strong opinion"
5. **Stand aside**: "I disagree but defer to group"
6. **Block**: "I cannot support this" (veto)

Most decisions don't need Level 1. Level 2-3 is sufficient. Reserve Level 6 (block) for ethical/legal/existential issues.

### Dealing with Impasse

**When stakeholders can't agree:**

**Option 1: Escalate**
- Clearly frame tradeoff for decision authority
- Example: "Engineering recommends A (technical merit), Sales recommends B (customer promise). VP Product, your call."

**Option 2: Decouple**
- Split into multiple decisions with different owners
- Example: "Engineering decides tech stack (their domain). Product decides feature scope (their domain)."

**Option 3: Time-box discussion**
- "We'll discuss for 30 min. If no consensus, we'll go with default option C and revisit in 3 months."

**Option 4: Introduce new information**
- "Let's gather customer feedback / run competitive analysis / build prototype before deciding."

## 6. Advanced Patterns

### Divergent Incentives (Sales vs Finance vs Ops)

**Scenario**: Sales wants custom contracts to close deals, Finance wants standardized pricing to forecast revenue, Operations wants limited SKUs to simplify fulfillment.

**Tension**: Each role optimizes for different metric (deal size vs predictability vs complexity).

**Synthesis**:
- **Core offering**: Standardized packages (Finance & Ops win on base case)
- **Custom tier**: Allow customization for enterprise deals >$500K with CFO approval (Sales wins on strategic accounts)
- **Operational tax**: Custom deals pay 20% premium to fund ops complexity (Ops gets resourced, Sales pays for flexibility)

**Principle**: Tiered approach where standardization is default, customization is available but priced to internalize costs.

### Temporal Conflicts (Short-Term vs Long-Term)

**Scenario**: Marketing wants aggressive growth spend (customer acquisition), Finance wants profitability (unit economics), Leadership wants sustainable growth.

**Tension**: Short-term growth (sacrifice margins) vs long-term health (profitable unit economics).

**Synthesis**:
- **Phase 1** (Year 1): Growth mode—invest in acquisition, LTV:CAC = 2:1 acceptable (Marketing wins)
- **Phase 2** (Year 2): Efficiency mode—optimize unit economics, LTV:CAC = 4:1 target (Finance wins)
- **Trigger for shift**: Hit $10M ARR or 18 months, whichever comes first (Leadership defines graduation criteria)

**Principle**: Sequence priorities over time with clear phase transitions.

### Regulatory/Ethical vs Commercial Tensions

**Scenario**: Product wants to use customer data for personalization (revenue driver), Privacy/Legal want data minimization (compliance, trust).

**Tension**: Commercial opportunity (more data = better product) vs regulatory/ethical constraint (less data = lower risk).

**Synthesis**:
- **Explicit consent**: Only use data if customer opts in (Legal satisfied—compliant)
- **Value exchange**: Show customer how data improves their experience (Product satisfied—retention driver)
- **Minimization**: Collect only what's needed for stated purpose, delete after 90 days (Privacy satisfied—limits exposure)
- **Differential privacy**: Aggregate data for analytics, never expose individual records (Security satisfied—no breach risk)

**Principle**: Regulatory constraints are non-negotiable. Find commercial model that works within those constraints (not around them).

### Cross-Cultural or Cross-Organizational Differences

**Scenario**: Acquiring company (startup culture) vs acquired company (enterprise culture) have different decision norms.

**Tension**: Fast, informal decisions (startup) vs deliberate, documented decisions (enterprise).

**Synthesis**:
- **Categorize decisions**: Reversible (fast process), irreversible (rigorous process) (Amazon "Type 1 vs Type 2")
- **Reversible examples**: UI changes, feature experiments → Startup process (bias to action)
- **Irreversible examples**: Infrastructure migrations, M&A, pricing model → Enterprise process (diligence, documentation)
- **Hybrid team norms**: Preserve startup speed for Type 2 decisions, adopt enterprise rigor for Type 1 (best of both)

**Principle**: Integrate cultural differences by creating framework that specifies when each approach applies.

---

## When to Use Methodology

**Simple decisions** (<4 stakeholders, clear authority): Use template.md
**Complex decisions** (5+ stakeholders, power dynamics, veto players): Use this methodology for:
- RACI and power-interest mapping (Section 1)
- Steel-manning and interest negotiation (Section 2)
- Decision rights and veto identification (Section 3)
- Advanced synthesis strategies (Section 4)
- Facilitation for multi-party alignment (Section 5)

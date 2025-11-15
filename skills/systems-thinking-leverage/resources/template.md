# Systems Thinking & Leverage Points Template

## Workflow

Copy this checklist and track your progress:

```
Systems Thinking Template Progress:
- [ ] Step 1: Define system boundaries and variables
- [ ] Step 2: Create causal loop diagram
- [ ] Step 3: Identify stocks, flows, and delays
- [ ] Step 4: Find leverage points
- [ ] Step 5: Validate and finalize
```

**Step 1**: Fill out [Section 1: System Definition](#1-system-definition) to clarify boundaries, stocks, flows, and problem pattern.

**Step 2**: Use [Section 2: Causal Loop Diagram](#2-causal-loop-diagram) to map feedback loops (R for reinforcing, B for balancing).

**Step 3**: Complete [Section 3: Stock-Flow Analysis](#3-stock-flow-analysis) to identify what accumulates and at what rates.

**Step 4**: Apply [Section 4: Leverage Point Ranking](#4-leverage-point-ranking) using Meadows' hierarchy to find high-leverage interventions.

**Step 5**: Verify quality using [Quality Checklist](#quality-checklist) before delivering systems-thinking-leverage.md.

---

## 1. System Definition

### System Boundary

**What's inside the system** (components you're analyzing and can influence):

[List the key components, actors, processes that are within your scope of analysis and intervention]

**What's outside the system** (external forces you can't control but affect the system):

[List external factors, constraints, or environmental conditions that influence the system but are beyond your control]

**Why this boundary?**

[Explain the pragmatic rationale for this scope - what makes this a useful boundary for analysis and intervention?]

### Key Variables

**Stocks** (things that accumulate - nouns):

| Stock Name | Current Level | Description | Measurement Unit |
|------------|---------------|-------------|------------------|
| [e.g., Employee count] | [e.g., 250] | [What it represents] | [e.g., # people] |
| [e.g., Technical debt] | [e.g., High] | [Description] | [e.g., story points, hours] |
| [Stock 3] | [Level] | [Description] | [Unit] |
| [Stock 4] | [Level] | [Description] | [Unit] |

**Flows** (rates of change - verbs):

| Flow Name | Current Rate | Affects Stock | Direction |
|-----------|--------------|---------------|-----------|
| [e.g., Hiring rate] | [e.g., 5/month] | [Employee count] | [Inflow ↑ / Outflow ↓] |
| [e.g., Attrition rate] | [e.g., 3/month] | [Employee count] | [Outflow ↓] |
| [Flow 3] | [Rate] | [Stock name] | [Direction] |
| [Flow 4] | [Rate] | [Stock name] | [Direction] |

**System Goals** (implicit or explicit):

- Primary goal: [What is the system fundamentally trying to achieve?]
- Secondary goals: [What other goals compete with or support the primary goal?]
- Whose goals? [Which stakeholders' goals drive system behavior?]

### Time Horizon

**Analysis timeframe**: [Short-term (weeks-months) / Medium-term (quarters-year) / Long-term (years)]

**Why this timeframe?** [Explain what you're trying to understand or influence within this time period]

### Problem Statement

**Symptom** (observable issue):

[What's the visible problem? Include metrics if available. e.g., "Customer churn rate is 30%/year, up from 15% last year"]

**Pattern** (recurring dynamic):

[What's the underlying pattern or behavior over time? e.g., "Each time we improve onboarding, churn drops briefly (2-3 months) then returns to previous level"]

**Hypothesis** (suspected feedback loop):

[What feedback loop might explain this pattern? e.g., "Pressure to reduce churn → Quick onboarding fixes → Users don't understand value prop → Churn returns → More pressure for quick fixes"]

---

## 2. Causal Loop Diagram

### Feedback Loops Identified

**Reinforcing Loop R1: [Name]**

```
[Variable A] → (+/-) → [Variable B] → (+/-) → [Variable C] → (+/-) → [Variable A]
```

- **Description**: [How does this loop amplify change? What does it reinforce?]
- **Polarity**: [+ means same direction, - means opposite direction]
- **Effect**: [Growth or collapse? What happens if this loop dominates?]
- **Time to complete loop**: [How long for one full cycle?]

**Example:** `Engaged Employees → (+) → Customer Satisfaction → (+) → Revenue → (+) → Investment → (+) → Engaged Employees` (virtuous growth cycle)

**Reinforcing Loop R2: [Name]** (if applicable)
[Same structure as R1]

**Balancing Loop B1: [Name]**

```
[Variable A] → (+/-) → [Variable B] → (+/-) → [Goal Gap] → (+/-) → [Corrective Action] → (+/-) → [Variable A]
```

- **Description**: [How does this loop resist change? What goal is it trying to maintain?]
- **Goal**: [Target state this loop seeks]
- **Effect**: [Stabilizes around what value?]
- **Time to complete loop**: [How long for feedback?]

**Example:** `Workload → (+) → Stress → (+) → Sick Days → (-) → Workload` (temporary relief, not solving root cause)

**Balancing Loop B2: [Name]** (if applicable) - [Same structure as B1]

### System Dynamics Map

**ASCII Causal Loop Diagram:**

```
        +
    A -----> B
    ^        |
    |        | +
    |        v
    +        C
    |        |
    |        | -
    |        v
    D <----- E

R: A → B → C → A (Reinforcing)
B: C → E → D → A (Balancing with delay [~~])
```

**Key:**
- `→` with `+` means same direction (A increases → B increases)
- `→` with `-` means opposite direction (C increases → E decreases)
- `R` marks reinforcing loops (amplify change)
- `B` marks balancing loops (resist change, goal-seeking)
- `[~~]` marks delays (time lag between cause and effect)

**Your diagram:**

```
[Draw your causal loop diagram here using ASCII art or describe the major connections]


```

---

## 3. Stock-Flow Analysis

### Stock Accumulation Dynamics

For each major stock, trace how it changes:

**Stock: [Stock Name]**

**Inflows** (what increases it):
- Flow 1: [Name] at rate [X/time period]
- Flow 2: [Name] at rate [Y/time period]

**Outflows** (what decreases it):
- Flow 1: [Name] at rate [X/time period]
- Flow 2: [Name] at rate [Y/time period]

**Current state**: [Accumulating / Depleting / Stable]

**Why?** [Are inflows > outflows (accumulating), inflows < outflows (depleting), or balanced (stable)?]

**Delays:**
- From [Flow/Action] to [Stock change]: [Time lag, e.g., "3-6 months"]
- From [Flow/Action] to [Stock change]: [Time lag]

**Implications**: [What happens if this stock continues accumulating/depleting? What's the consequence?]

**Example:** Technical Debt stock - Inflows: quick fixes (20/sprint) + shaky features (10/sprint) = 30/sprint. Outflows: refactoring (5/sprint) + root-cause fixes (3/sprint) = 8/sprint. Net: +22/sprint accumulating. Delays: 3-6 months to slowdown, 1-2 sprints for improvement. Implication: In 6 months, debt slows development 50%, reinforcing quick-fix pressure.

---

## 4. Leverage Point Ranking

### Candidate Interventions

List all possible places to intervene:

| Intervention | Description | Leverage Level (1-12) | Feasibility (High/Med/Low) | Expected Impact (High/Med/Low) |
|--------------|-------------|-----------------------|----------------------------|--------------------------------|
| [Intervention 1] | [Brief description] | [1-12, see hierarchy below] | [H/M/L] | [H/M/L] |
| [Intervention 2] | [Description] | [Level] | [Feasibility] | [Impact] |
| [Intervention 3] | [Description] | [Level] | [Feasibility] | [Impact] |
| [Intervention 4] | [Description] | [Level] | [Feasibility] | [Impact] |
| [Intervention 5] | [Description] | [Level] | [Feasibility] | [Impact] |

**Meadows' Leverage Point Hierarchy** (for classification):
- **12**: Parameters (numbers, rates) - LOW leverage
- **11**: Buffers (stock sizes vs. flows)
- **10**: Stock-flow structures (physical design)
- **9**: Delays (time lags)
- **8**: Balancing feedback loop strength
- **7**: Reinforcing feedback loop strength
- **6**: Information flows (who knows what)
- **5**: Rules (incentives, constraints)
- **4**: Self-organization (adapt/evolve capability)
- **3**: Goals (system purpose)
- **2**: Paradigms (mindset, mental models)
- **1**: Transcending paradigms (paradigm fluidity) - HIGH leverage

### High-Leverage Interventions (Priority)

**Primary Intervention: [Name]**

- **Leverage level**: [1-7, high leverage]
- **Mechanism**: [How does this intervention work? Which loop does it affect?]
- **Why high leverage?** [Explain why this is more effective than adjusting parameters]
- **Feasibility challenges**: [What makes this hard? Who will resist?]
- **Time to impact**: [How long until results visible, accounting for delays?]
- **Success metrics**: [How will you know it's working? Leading and lagging indicators]

**Supporting Intervention 1: [Name]**

- **Leverage level**: [Level]
- **How it supports primary**: [Explain complementary effect]
- **Rationale**: [Why combine these interventions?]

**Supporting Intervention 2: [Name]**

[Same structure as Supporting Intervention 1]

### Low-Leverage Interventions (Avoid or Deprioritize)

**Why avoid:**

| Intervention | Leverage Level | Why It's Low Leverage | Better Alternative |
|--------------|----------------|------------------------|---------------------|
| [e.g., Increase budget 10%] | [12 - Parameter] | [Temporary, competitors can match] | [Change hiring goal from "fill seats" to "build capability"] |
| [Intervention 2] | [Level] | [Reason] | [Alternative] |

---

## 5. Intervention Strategy

### Recommended Approach

**Primary intervention**: [Name from high-leverage section above]

**Supporting interventions**: [List 1-3 complementary interventions]

**Sequencing**: [What order? Simultaneous or phased?]

1. [First action and timing]
2. [Second action and timing]
3. [Third action and timing]

**Rationale**: [Why this sequence? What dependencies exist?]

### Predicted Outcomes

**Short-term** (1-3 months): [Immediate effects? Which loops activate? Worse before better?]

**Medium-term** (3-12 months): [Reinforcing loop momentum? Delays complete? Resistances emerge?]

**Long-term** (1+ years): [New equilibrium? New limits? System evolution?]

### Risks & Unintended Consequences

**Risk 1**: [What could go wrong?]
- **Likelihood**: [High / Medium / Low]
- **Impact if occurs**: [Severity]
- **Mitigation**: [How to prevent or reduce risk]

**Risk 2**: [Unintended consequence from intervention]
- **Mechanism**: [Which loop or delay causes this?]
- **Mitigation**: [How to monitor and adjust]

**Risk 3**: [System resistance or pushback]
- **Source**: [Who or what will resist?]
- **Mitigation**: [How to address resistance]

### Success Metrics

**Leading indicators** (early signals intervention is working):
1. [Metric to track weekly/monthly]
2. [Metric to track]
3. [Metric to track]

**Lagging indicators** (longer-term outcomes):
1. [Metric to track quarterly/annually]
2. [Metric to track]
3. [Metric to track]

**How to interpret**: [What trends indicate success vs. failure? What adjustments might be needed?]

### Monitoring & Adaptation Plan

**Check-in frequency**: [Weekly / Bi-weekly / Monthly]

**What to monitor:**
- [Key stock levels]
- [Flow rates]
- [Loop activation signs (is reinforcing loop building momentum?)]
- [Delay timers (have we waited long enough for effect to show?)]
- [Resistance signals (pushback, workarounds)]

**Adaptation triggers**: [Under what conditions do we adjust strategy?]

**Responsible party**: [Who monitors and makes adjustment calls?]

---

## Quality Checklist

Before finalizing, verify:

### System Definition
- [ ] System boundary clearly stated (what's in/out)?
- [ ] Boundary rationale pragmatic (useful scope for intervention)?
- [ ] Stocks identified (things that accumulate - nouns)?
- [ ] Flows identified (rates of change - verbs)?
- [ ] Stocks and flows connected (flows change which stocks)?
- [ ] System goals stated (implicit or explicit)?
- [ ] Time horizon appropriate for problem and intervention?

### Causal Loop Diagram
- [ ] At least one reinforcing loop (R) identified?
- [ ] At least one balancing loop (B) identified?
- [ ] Polarity marked (+ same direction, - opposite direction)?
- [ ] Loop effects described (growth/collapse for R, goal-seeking for B)?
- [ ] Delays explicitly noted where they exist?
- [ ] Diagram shows interconnections (not just isolated pairs)?

### Stock-Flow Analysis
- [ ] For each major stock: inflows and outflows listed?
- [ ] Current state assessed (accumulating/depleting/stable)?
- [ ] Delays from flows to stock changes estimated?
- [ ] Implications of accumulation/depletion stated?
- [ ] Time lags quantified (not just "delayed" but "3 months")?

### Leverage Point Analysis
- [ ] Multiple intervention points considered (not just first idea)?
- [ ] Each intervention classified by leverage level (1-12)?
- [ ] High-leverage interventions (1-7) prioritized over low-leverage (8-12)?
- [ ] Feasibility vs. leverage trade-offs acknowledged?
- [ ] Parameter-tweaking (level 12) avoided as primary strategy?

### Intervention Strategy
- [ ] Primary intervention is high-leverage (levels 1-7)?
- [ ] Supporting interventions complement primary (not duplicate)?
- [ ] Predicted outcomes based on loop dynamics (not just wishful thinking)?
- [ ] Short, medium, long-term effects distinguished?
- [ ] Delays accounted for in outcome timeline?
- [ ] Unintended consequences anticipated (second-order effects)?
- [ ] System resistance identified (who/what will push back)?
- [ ] Success metrics include leading and lagging indicators?
- [ ] Monitoring plan specified (frequency, what to track, adaptation triggers)?

### System Archetype Recognition (if applicable)
- [ ] Does system match a known archetype (fixes that fail, shifting burden, tragedy of commons, limits to growth)?
- [ ] If yes, typical failure mode acknowledged?
- [ ] Archetype-specific high-leverage intervention identified?

### Overall Quality
- [ ] Problem statement clear (symptom → pattern → hypothesis)?
- [ ] Analysis grounded in feedback loop logic (not just list of causes)?
- [ ] Interventions address structure, not just symptoms?
- [ ] Assumptions stated explicitly (what must be true for this to work)?
- [ ] Confidence appropriate (not overconfident given complexity)?
- [ ] Actionable recommendations (clear what to do, when, how to measure)?

**Minimum Standard**: If any checklist item is unchecked and relevant to your system, address it before finalizing. Use rubric (evaluators/rubric_systems_thinking_leverage.json) for detailed scoring. Average score ≥ 3.5/5.

---

## Common Mistakes to Avoid

**❌ Treating symptoms not root causes** - "Add more people" (parameter) vs. "Eliminate low-value work" (goal/rules). Fix: Ask "what feedback loop creates this symptom?"

**❌ Ignoring delays** - "Tried for 2 weeks, didn't work" (but skill development takes 3-6 months). Fix: Estimate delays, wait appropriately.

**❌ Single-loop thinking** - Only seeing growth (R loop), missing limit (B loop). Fix: Look for both R and B loops. Every R hits a limit.

**❌ Confusing stocks and flows** - "Morale is flowing" (morale = stock, recognition = flow). Fix: Stocks are nouns (accumulations), flows are verbs (rates).

**❌ Low-leverage interventions** - Tweaking parameters when structure/goals/paradigms need changing. Fix: Use hierarchy (1-12), prioritize 1-7 over 8-12.

**❌ Unintended consequences** - "Speed up releases" → Technical debt → Slower releases. Fix: Trace second-order effects through all loops.

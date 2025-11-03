# Deliberation, Debate & Red Teaming: Advanced Methodology

## Workflow

Copy this checklist for advanced red team scenarios:

```
Advanced Red Teaming Progress:
- [ ] Step 1: Select appropriate red team technique
- [ ] Step 2: Design adversarial simulation or exercise
- [ ] Step 3: Facilitate session and capture critiques
- [ ] Step 4: Synthesize findings with structured argumentation
- [ ] Step 5: Build consensus on mitigations
```

**Step 1: Select appropriate red team technique** - Match technique to proposal complexity and stakes. See [Technique Selection](#technique-selection).

**Step 2: Design adversarial simulation** - Structure attack trees, pre-mortem, wargaming, or tabletop exercise. See techniques below.

**Step 3: Facilitate session** - Manage group dynamics, overcome defensiveness, calibrate intensity. See [Facilitation Techniques](#facilitation-techniques).

**Step 4: Synthesize findings** - Use structured argumentation to evaluate critique validity. See [Argumentation Framework](#argumentation-framework).

**Step 5: Build consensus** - Align stakeholders on risk prioritization and mitigations. See [Consensus Building](#consensus-building).

---

## Technique Selection

**Match technique to proposal characteristics:**

| Proposal Type | Complexity | Stakes | Group Size | Best Technique |
|--------------|------------|--------|------------|----------------|
| Security/Architecture | High | High | 3-5 | Attack Trees |
| Strategy/Product | Medium | High | 5-10 | Pre-mortem |
| Policy/Process | Medium | Medium | 8-15 | Tabletop Exercise |
| Crisis Response | High | Critical | 4-8 | Wargaming |
| Feature/Design | Low | Medium | 3-5 | Structured Critique (template.md) |

**Time availability:**
- 1-2 hours: Structured critique (template.md), Pre-mortem
- Half-day: Tabletop exercise, Attack trees
- Full-day: Wargaming, Multi-round simulation

---

## 1. Attack Trees

### What Are Attack Trees?

Systematic enumeration of attack vectors against a system. Start with attacker goal (root), decompose into sub-goals using AND/OR logic.

**Use case:** Security architecture, product launches with abuse potential

### Building Attack Trees

**Process:**
1. Define attacker goal (root node): "Compromise user data"
2. Decompose with AND/OR gates:
   - **OR gate:** Attacker succeeds if ANY child succeeds
   - **AND gate:** Must achieve ALL children
3. Assign properties to each path: Feasibility (1-5), Cost (L/M/H), Detection (1-5)
4. Identify critical paths: High feasibility + low detection + low cost
5. Design mitigations: Prevent (remove vulnerability), Detect (monitoring), Respond (incident plan)

**Example tree:**
```
[Compromise user data]
  OR
    ├─ [Exploit API] → SQL injection / Auth bypass / Rate limit bypass
    ├─ [Social engineer] → Phish credentials AND Access admin panel
    └─ [Physical access] → Breach datacenter AND Extract disk
```

**Template:**
```markdown
## Attack Tree: [Goal]

**Attacker profile:** [Script kiddie / Insider / Nation-state]

**Attack paths:**
1. **[Attack vector]** - Feasibility: [1-5] | Cost: [L/M/H] | Detection: [1-5] | Critical: [Y/N] | Mitigation: [Defense]
2. **[Attack vector]** [Same structure]

**Critical paths:** [Feasibility ≥4, detection ≤2]
**Recommended defenses:** [Prioritized mitigations]
```

---

## 2. Pre-mortem

### What Is Pre-mortem?

Assume proposal failed in future, work backwards to identify causes. Exploits prospective hindsight (easier to imagine causes of known failure than predict unknowns).

**Use case:** Product launches, strategic decisions, high-stakes initiatives

### Pre-mortem Process (90 min total)

1. **Set the stage (5 min):** "It's [date]. Our proposal failed spectacularly. [Describe worst outcome]"
2. **Individual brainstorming (10 min):** Each person writes 5-10 failure reasons independently
3. **Round-robin sharing (20 min):** Go around room, each shares one reason until all surfaced
4. **Cluster and prioritize (15 min):** Group similar, vote (3 votes/person), identify top 5-7
5. **Risk assessment (20 min):** For each: Severity (1-5), Likelihood (1-5), Early warning signs
6. **Design mitigations (30 min):** Preventative actions for highest-risk modes

**Template:**
```markdown
## Pre-mortem: [Proposal]

**Scenario:** It's [date]. Failed. [Vivid worst outcome]

**Failure modes (by votes):**
1. **[Mode]** (Votes: [X]) - Why: [Root cause] | S: [1-5] L: [1-5] Score: [S×L] | Warnings: [Indicators] | Mitigation: [Action]
2. [Same structure]

**Showstoppers (≥15):** [Must-address]
**Revised plan:** [Changes based on pre-mortem]
```

**Facilitator tips:** Make failure vivid, encourage wild ideas, avoid blame, time-box ruthlessly

---

## 3. Wargaming

### What Is Wargaming?

Multi-party simulation where teams play adversarial roles over multiple rounds. Reveals dynamic effects (competitor responses, escalation, unintended consequences).

**Use case:** Competitive strategy, crisis response, market entry

### Wargaming Structure

**Roles:** Proposer team, Adversary team(s) (competitors, regulators), Control team (adjudicates outcomes)

**Turn sequence per round (35 min):**
1. Planning (15 min): Teams plan moves in secret
2. Execution (5 min): Reveal simultaneously
3. Adjudication (10 min): Control determines outcomes, updates game state
4. Debrief (5 min): Reflect on consequences

**Process:**
1. **Define scenario (30 min):** Scenario, victory conditions per team, constraints
2. **Brief teams (15 min):** Role sheets with incentives, capabilities, constraints
3. **Run 3-5 rounds (45 min each):** Control introduces events to stress-test
4. **Post-game debrief (45 min):** Strategies emerged, vulnerabilities exposed, contingencies needed

**Template:**
```markdown
## Wargame: [Proposal]

**Scenario:** [Environment] | **Teams:** Proposer: [Us] | Adversary 1: [Competitor] | Adversary 2: [Regulator] | Control: [Facilitator]

**Victory conditions:** Proposer: [Goal] | Adversary 1: [Goal] | Adversary 2: [Goal]

**Round 1:** Proposer: [Move] | Adv1: [Response] | Adv2: [Response] | Outcome: [New state]
**Round 2-5:** [Same structure]

**Key insights:** [Unexpected dynamics, blind spots, countermoves]
**Recommendations:** [Mitigations, contingencies]
```

---

## 4. Tabletop Exercises

### What Are Tabletop Exercises?

Structured walkthrough where participants discuss how they'd respond to scenario. Focuses on coordination, process gaps, decision-making under stress.

**Use case:** Incident response, crisis management, operational readiness

### Tabletop Process

1. **Design scenario (1 hr prep):** Realistic incident with injects (new info at intervals), decision points
2. **Brief participants (10 min):** Set scene, define roles, clarify it's simulation
3. **Run scenario (90 min):** Present 5-7 injects, discuss responses (10-15 min each)
4. **Debrief (30 min):** What went well? Gaps exposed? Changes needed?

**Example inject sequence:**
- T+0: "Alert fires: unusual DB access" → Who's notified? First action?
- T+15: "10K records accessed" → Who notify (legal, PR)? Communication?
- T+30: "CEO wants briefing, reporter called" → CEO message? PR statement?

**Template:**
```markdown
## Tabletop: [Scenario]

**Objective:** Test [plan/procedure] | **Participants:** [Roles] | **Scenario:** [Incident description]

**Injects:**
**T+0 - [Event]** | Q: [Who responsible? What action?] | Decisions: [Responses] | Gaps: [Unclear/missing]
**T+15 - [Escalation]** [Same structure]

**Debrief:** Strengths: [Worked well] | Gaps: [Process/tool/authority] | Recommendations: [Changes]
```

---

## Facilitation Techniques

### Managing Defensive Responses

| Pattern | Response | Goal |
|---------|----------|------|
| "We already thought of that" | "Great. Walk me through the analysis and mitigation?" | Verify claim, check adequacy |
| "That's not realistic" | "What makes this unlikely?" (Socratic) | Challenge without confrontation |
| "You don't understand context" | "You're right, help me. Can you explain [X]? How does that address [critique]?" | Acknowledge expertise, stay focused |
| Dismissive tone/eye-rolling | "Sensing resistance. Goal is improve, not attack. What would help?" | Reset tone, reaffirm purpose |

### Calibrating Adversarial Intensity

**Too aggressive:** Team shuts down, hostile | **Too soft:** Superficial critiques, groupthink

**Escalation approach:**
- Round 1: Curious questions ("What if X?")
- Round 2: Direct challenges ("Assumes Y, but what if false?")
- Round 3: Aggressive probing ("How does this survive Z?")

**Adjust to culture:**
- High-trust teams: Aggressive critique immediately
- Defensive teams: Start curious, frame as "helping improve"

**"Yes, and..." technique:** "Yes, solves X, AND creates Y for users Z" (acknowledges value + raises concern)

### Facilitator Tactics

- **Parking lot:** "Important but out-of-scope. Capture for later."
- **Redirect attacks:** "Critique proposal, not people. Rephrase?"
- **Balance airtime:** "Let's hear from [quiet person]."
- **Synthesize:** "Here's what I heard: [3-5 themes]. Accurate?"
- **Strategic silence:** Wait 10+ sec after tough question. Forces deeper thinking.

---

## Argumentation Framework

### Toulmin Model for Evaluating Critiques

**Use case:** Determine if critique is valid or strawman

**Components:** Claim (assertion) + Data (evidence) + Warrant (logical link) + Backing (support for warrant) + Qualifier (certainty) + Rebuttal (conditions where claim fails)

**Example:**
- **Claim:** "Feature will fail, users won't adopt"
- **Data:** "5% beta adoption"
- **Warrant:** "Beta users = target audience, beta predicts production"
- **Backing:** "Past 3 features: beta adoption r=0.89 correlation"
- **Qualifier:** "Likely"
- **Rebuttal:** "Unless we improve onboarding (not in beta)"

### Evaluating Critique Validity

**Strong:** Specific data, logical warrant, backing exists, acknowledges rebuttals
**Weak (strawman):** Vague hypotheticals, illogical warrant, no backing, ignores rebuttals

**Example evaluation:**
"API slow because complex DB queries" | Data: "5+ table joins" ✓ | Warrant: "Multi-joins slow" ✓ | Backing: "Prior 5+ joins = 2s" ✓ | Rebuttal acknowledged? No (caching, indexes) | **Verdict:** Moderate strength, address rebuttal

### Structured Rebuttal

**Proposer response:**
1. **Accept:** Valid, will address → Add to mitigation
2. **Refine:** Partially valid → Clarify conditions
3. **Reject:** Invalid → Provide counter-data + counter-warrant (substantive, not dismissive)

---

## Consensus Building

### Multi-Stakeholder Alignment (65 min)

**Challenge:** Different stakeholders prioritize different risks

**Process:**
1. **Acknowledge perspectives (15 min):** Each states top concern, facilitator captures
2. **Identify shared goals (10 min):** What do all agree on?
3. **Negotiate showstoppers (30 min):** For risks ≥15, discuss: Is this truly showstopper? Minimum mitigation? Vote if needed (stakeholder-weighted scoring)
4. **Accept disagreements (10 min):** Decision-maker breaks tie on non-showstoppers. Document dissent.

### Delphi Method (Asynchronous)

**Use case:** Distributed team, avoid group pressure

**Process:** Round 1 (independent assessments) → Round 2 (share anonymized, experts revise) → Round 3 (share aggregate, final assessments) → Convergence or decision-maker adjudicates

**Advantage:** Eliminates groupthink, HiPPO effect | **Disadvantage:** Slower (days/weeks)

---

## Advanced Critique Patterns

### Second-Order Effects

**Identify ripple effects:** "If we change this, what happens next? Then what?" (3-5 iterations)

**Example:** Launch referral → Users invite friends → Invited users lower engagement (didn't choose organically) → Churn ↑, LTV ↓ → Unit economics worsen → Budget cuts

### Inversion

**Ask "How do we guarantee failure?" then check if proposal avoids those modes**

**Example:** New market entry
- Inversion: Wrong product-market fit, underestimate competition, violate regulations, misunderstand culture
- Check: Market research? Regulatory review? Localization?

### Assumption Surfacing

**For each claim: "What must be true for this to work?"**

**Example:** "Feature increases engagement 20%"
- Assumptions: Users want it (validated?), will discover it (discoverability?), works reliably (load tested?), 20% credible (source?)
- Test each. If questionable, critique valid.

---

## Common Pitfalls & Mitigations

| Pitfall | Detection | Mitigation |
|---------|-----------|------------|
| **Analysis paralysis** | Red team drags on for weeks, no decision | Time-box exercise (half-day max). Focus on showstoppers only. |
| **Strawman arguments** | Critiques are unrealistic or extreme | Use Toulmin model to evaluate. Require data and backing. |
| **Groupthink persists** | All critiques are minor, no real challenges | Use adversarial roles explicitly. Pre-mortem or attack trees force critical thinking. |
| **Defensive shutdown** | Team rejects all critiques, hostility | Recalibrate tone. Use "Yes, and..." framing. Reaffirm red team purpose. |
| **HiPPO effect** | Highest-paid person's opinion dominates | Anonymous brainstorming (pre-mortem). Delphi method. |
| **No follow-through** | Great critiques, no mitigations implemented | Assign owners and deadlines to each mitigation. Track in project plan. |
| **Red team as rubber stamp** | Critique is superficial, confirms bias | Choose truly adversarial roles. Bring in external red team if internal team too aligned. |
| **Over-optimization of low-risk items** | Spending time on low-impact risks | Use risk matrix. Only address showstoppers and high-priority. |

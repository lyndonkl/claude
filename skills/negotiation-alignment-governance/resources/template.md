# Negotiation Alignment Governance Template

## Quick Start

**Purpose:** Create explicit stakeholder alignment through decision rights matrices (RACI/DACI/RAPID), working agreements, and conflict resolution protocols.

**When to use:** Decision authority is ambiguous, stakeholders have conflicting priorities, teams need coordination norms, or conflicts need structured resolution.

---

## Part 1: Stakeholder Mapping

**Context:** [Brief description of situation requiring alignment]

**Key Stakeholders:**

| Stakeholder | Role/Team | Primary Interest | Current Concerns | Power/Influence |
|-------------|-----------|------------------|------------------|-----------------|
| [Name] | [Role] | [What they care about] | [Worries/blockers] | High/Medium/Low |
| [Name] | [Role] | [What they care about] | [Worries/blockers] | High/Medium/Low |
| [Name] | [Role] | [What they care about] | [Worries/blockers] | High/Medium/Low |

**Stakeholder Relationships:**
- **Aligned:** [Who agrees on what]
- **Tensions:** [Who conflicts on what]
- **Dependencies:** [Who needs what from whom]

**Decision Points Needing Clarity:**
1. [Decision 1]: Currently unclear who decides
2. [Decision 2]: Multiple people believe they decide
3. [Decision 3]: Decisions blocked due to ambiguity

---

## Part 2: Decision Rights Framework

### Option A: RACI Matrix

Use for: Process mapping, task allocation, operational clarity

| Decision/Activity | R (Responsible) | A (Accountable) | C (Consulted) | I (Informed) |
|-------------------|-----------------|-----------------|---------------|--------------|
| [Decision 1] | [Who does work] | **[ONE owner]** | [Who gives input] | [Who gets notified] |
| [Decision 2] | [Who does work] | **[ONE owner]** | [Who gives input] | [Who gets notified] |
| [Decision 3] | [Who does work] | **[ONE owner]** | [Who gives input] | [Who gets notified] |

**Key:**
- **R (Responsible):** Does the work to complete the task
- **A (Accountable):** Owns the outcome (exactly ONE person—neck on the line)
- **C (Consulted):** Provides input BEFORE decision (two-way communication)
- **I (Informed):** Notified AFTER decision (one-way communication)

### Option B: DACI Matrix

Use for: Strategic decisions, product choices, high-stakes calls

| Decision | D (Driver) | A (Approver) | C (Contributors) | I (Informed) |
|----------|------------|--------------|------------------|--------------|
| [Decision 1] | [Runs process] | **[ONE decider]** | [Must consult] | [Gets notified] |
| [Decision 2] | [Runs process] | **[ONE decider]** | [Must consult] | [Gets notified] |
| [Decision 3] | [Runs process] | **[ONE decider]** | [Must consult] | [Gets notified] |

**Key:**
- **D (Driver):** Runs the decision process, gathers input, recommends
- **A (Approver):** Makes final decision (exactly ONE—thumb up/down)
- **C (Contributors):** Must be consulted for input (but Approver decides)
- **I (Informed):** Notified of outcome

### Option C: RAPID Matrix

Use for: Complex strategic decisions with compliance, legal, or technical veto requirements

| Decision | R (Recommend) | A (Agree) | P (Perform) | I (Input) | D (Decide) |
|----------|---------------|-----------|-------------|-----------|------------|
| [Decision 1] | [Proposes] | [Must agree/veto] | [Executes] | [Advises] | **[ONE decider]** |
| [Decision 2] | [Proposes] | [Must agree/veto] | [Executes] | [Advises] | **[ONE decider]** |

**Key:**
- **R (Recommend):** Proposes the decision with analysis
- **A (Agree):** Must agree (veto power for legal/compliance/technical)
- **P (Perform):** Implements the decision
- **I (Input):** Consulted for expertise
- **D (Decide):** Final authority

### Option D: Advice Process

Use for: Empowered teams, flat organizations

Anyone can decide after seeking advice from affected parties and experts. Decision-maker accountable for outcome.

**Scope:** [Which decisions use advice process]
**Guardrails:** [Minimum advisors, escalation criteria]

---

## Part 3: Working Agreements

### Communication Norms

**Sync (Meetings):** Use for brainstorming, negotiation. Agenda required 24h advance. Max [30/60 min]. Document decisions.

**Async (Docs/Slack):** Use for updates, approvals. Response times: Urgent (<2h), Normal (<24h), FYI (none).

**Documentation:** Decisions in [ADRs/log/wiki]. Meeting notes in [tool]. Source of truth: [location].

### Decision-Making Norms

**Decision Speed vs Quality:**
- **Fast/Reversible decisions:** Use consent (no strong objections)
- **Slow/Irreversible decisions:** Use explicit DACI with analysis

**Time-boxing:**
- If no consensus after [N] discussions, escalate with:
  - Options analysis
  - Recommendation
  - Decision criteria

**Decision Documentation:**
- Architecture decisions: ADRs (Architecture Decision Records)
- Product decisions: Decision log with rationale
- Process changes: Updated handbook/wiki

### Quality & Standards

**Definition of Done:**
- [Criterion 1]: [Specific requirement]
- [Criterion 2]: [Specific requirement]
- [Criterion 3]: [Specific requirement]

**Quality Bar:**
- Minimum: [Non-negotiable requirements]
- Target: [Aspirational standards]
- Trade-offs: [When quality can flex]

**Review Requirements:**
- [Type of work]: Requires [N] approvals from [roles]
- Approval SLA: [Timeframe]
- Escalation: If not reviewed in [timeframe], [action]

### Escalation Paths

**When to Escalate:**
- Decision blocked for > [N days]
- Stakeholders fundamentally disagree after structured dialogue
- Decision impacts outside agreed scope
- Risk or compliance concern

**How to Escalate:**
1. Document the issue and options considered
2. Clarify the decision needed and by when
3. Escalate to: [Manager / Committee / Executive]
4. Include joint recommendation if possible

---

## Part 4: Conflict Resolution Protocols

### Level 1: Direct Dialogue (Default)

**When:** First response to disagreement

**Process:** 1:1 conversation. Assume good intent. Focus on interests (why) not positions (what). Use data/criteria. Seek understanding. Propose solutions addressing both interests.

**Outcome:** Agreement or escalate to Level 2

### Level 2: Facilitated Mediation

**When:** Direct dialogue fails after [N] attempts

**Process:** Neutral facilitator. Each party explains interests, concerns, constraints. Facilitator clarifies agreement/disagreement, objective criteria. Brainstorm options meeting both interests. Test solutions against criteria.

**Outcome:** Agreement, compromise, or escalate to Level 3

### Level 3: Escalation & Decision

**When:** Mediation doesn't resolve within [timeframe]

**Process:** Document for decider (context, options, positions, recommendations). Decider reviews, may request more info or facilitate final discussion, then decides. Disagree-and-commit: All parties commit once decided.

**Decider:** [Role / Name per decision type]

### Conflict Resolution Principles

**Separate People from Problem:**
- Attack the problem, not the person
- Use "I feel..." not "You always..."

**Focus on Interests, Not Positions:**
- Position: "I want X"
- Interest: "I need X because Y"

**Generate Options Before Deciding:**
- Avoid false dichotomies
- Brainstorm win-win solutions

**Use Objective Criteria:**
- Data (metrics, user research, benchmarks)
- Principles (company values, best practices)
- External standards (industry norms, regulations)

---

## Part 5: Negotiation Framework (For Trade-offs)

### 1. Clarify Interests

**Party A:**
- **Wants:** [Position]
- **Because:** [Underlying interest/need]
- **Success looks like:** [Outcome]
- **Can't compromise on:** [Hard constraints]

**Party B:**
- **Wants:** [Position]
- **Because:** [Underlying interest/need]
- **Success looks like:** [Outcome]
- **Can't compromise on:** [Hard constraints]

### 2. Identify BATNA (Best Alternative To Negotiated Agreement)

**Party A's BATNA:** [What happens if no agreement]
**Party B's BATNA:** [What happens if no agreement]

**Zone of Possible Agreement (ZOPA):** [Where both parties are better off than BATNA]

### 3. Generate Options

**Option 1:** [Proposal]
- Party A gets: [Benefits]
- Party B gets: [Benefits]
- Trade-offs: [Costs]

**Option 2:** [Proposal]
- Party A gets: [Benefits]
- Party B gets: [Benefits]
- Trade-offs: [Costs]

**Option 3:** [Proposal]
- Party A gets: [Benefits]
- Party B gets: [Benefits]
- Trade-offs: [Costs]

### 4. Evaluate Against Criteria

| Option | Criterion 1 | Criterion 2 | Criterion 3 | Total Score |
|--------|-------------|-------------|-------------|-------------|
| Option 1 | [Score] | [Score] | [Score] | [Sum] |
| Option 2 | [Score] | [Score] | [Score] | [Sum] |
| Option 3 | [Score] | [Score] | [Score] | [Sum] |

**Selected:** [Option X] because [rationale]

### 5. Agreement Terms

**What:** [Specific outcome agreed]
**Who:** [Responsible parties]
**When:** [Timeline]
**How:** [Implementation]
**Review:** [When to revisit]

---

## Part 6: Governance Maintenance

### Review Cadence

**Quarterly Governance Review:**
- What's working well?
- What's not working?
- Emerging gaps or ambiguities?
- Updated decision rights matrix
- Revised working agreements

**Triggers for Ad-Hoc Review:**
- Org structure change
- New stakeholders or teams
- Recurring conflicts in same area
- Decision velocity declining

### Metrics to Track

**Decision Velocity:**
- Time from decision needed to decision made
- Number of decisions blocked > [N] days
- Escalation frequency

**Conflict Resolution:**
- Time to resolve conflicts
- Escalation rate (Level 1 → 2 → 3)
- Repeat conflicts in same area

**Agreement Adherence:**
- Working agreement violations
- Shadow governance incidents (decisions made outside framework)
- Stakeholder satisfaction with process

---

## Output Format

Create `negotiation-alignment-governance.md`:

```markdown
# [Initiative/Team]: Negotiation Alignment Governance

**Date:** [YYYY-MM-DD]
**Review Date:** [Quarterly]

## Stakeholder Map
[Table of stakeholders, interests, concerns]

## Decision Rights Matrix
[RACI / DACI / RAPID matrix for key decisions]

## Working Agreements

### Communication
- Sync vs async guidelines
- Response time expectations
- Documentation requirements

### Decision-Making
- Fast vs slow decision criteria
- Time-boxing and escalation
- Documentation standards

### Quality & Standards
- Definition of done
- Quality bar (minimum vs target)
- Review requirements

### Escalation Paths
- When to escalate
- How to escalate
- Who decides

## Conflict Resolution Protocols

### Level 1: Direct Dialogue
[Process for peer-to-peer resolution]

### Level 2: Mediation
[When and how to bring in facilitator]

### Level 3: Escalation
[Final decision authority]

## Governance Maintenance
- Review cadence: [Quarterly / Ad-hoc triggers]
- Metrics: [Decision velocity, conflict resolution, adherence]

## Key Insights
- [What alignment this creates]
- [What conflicts this prevents]
- [What enables faster decisions]
```

---

## Quality Checklist

Before finalizing:
- [ ] Decision rights: Exactly ONE Accountable/Approver per decision
- [ ] All key stakeholders covered in framework
- [ ] Working agreements are specific and observable (not vague)
- [ ] Conflict resolution has clear escalation path
- [ ] Agreements include review/update cadence
- [ ] No shadow governance (framework covers real decisions)
- [ ] Psychological safety (people can disagree without fear)
- [ ] Stakeholders have consented to framework

---

## Tips

**For RACI/DACI:**
- Start with most contentious decisions
- One Accountable/Approver only (resist pressure for multiple)
- Consulted ≠ consensus—input gathered, decider decides
- Review quarterly—roles change, decisions evolve

**For Working Agreements:**
- Make observable (not "communicate well" but "respond in 24h")
- Include positive behaviors AND boundaries
- Get explicit consent from all parties
- Revisit when violated or ineffective

**For Conflict Resolution:**
- Assume good intent (conflicts are structural, not personal)
- Make escalation safe (not punishment, but decision support)
- Document decisions to avoid re-litigating
- Disagree-and-commit once decided

**For Facilitation:**
- Stay neutral (don't take sides)
- Make implicit tensions explicit
- Use objective criteria when possible
- Don't force consensus—escalate when stuck

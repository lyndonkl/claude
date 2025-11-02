# Alignment Framework Template

## Workflow

Copy this checklist and track your progress:

```
Alignment Framework Progress:
- [ ] Step 1: Draft North Star and core values
- [ ] Step 2: Create decision tenets for common dilemmas
- [ ] Step 3: Define observable behaviors
- [ ] Step 4: Add anti-patterns and usage guidance
- [ ] Step 5: Validate with quality checklist
```

**Step 1: Draft North Star and core values**

Write 1-2 sentence North Star (where we're going and why) and 3-5 core values with specific definitions, why they matter, what we optimize FOR, and what we de-prioritize. Use [Quick Template](#quick-template) structure and [Field-by-Field Guidance](#field-by-field-guidance) for details.

**Step 2: Create decision tenets for common dilemmas**

Identify 5-10 real trade-offs your team faces and write "When X vs Y, we..." statements. See [Decision Tenets](#decision-tenets) guidance for format. Include specific reasons tied to values and acknowledge merit of alternatives.

**Step 3: Define observable behaviors**

List 10-15 specific, observable actions across contexts: meetings, code/design reviews, planning, communication, hiring, operations. See [Observable Behaviors](#observable-behaviors) for examples. Focus on what you could notice in daily work.

**Step 4: Add anti-patterns and usage guidance**

Document 3-5 behaviors you explicitly DON'T do, even when tempting, and explain which value they violate. Add practical guidance for using framework in decision-making, hiring, onboarding, performance reviews. See [Anti-Patterns](#anti-patterns) section.

**Step 5: Validate with quality checklist**

Use [Quality Checklist](#quality-checklist) to verify: North Star is memorable, values are specific with trade-offs, decision tenets address real dilemmas, behaviors are observable, usable TODAY, no contradictions, 1-2 pages total, jargon-free.

## Quick Template

Copy this structure to create your alignment framework:

```markdown
# {Team/Organization Name} Alignment Framework

## Context

**Why this matters now:**
{What triggered the need for alignment? Growth, conflict, new direction?}

**Who this is for:**
{Team, organization, function - be specific}

**Last updated:** {Date}

---

## North Star

{1-2 sentences: Where are we going and why?}

**Example formats:**
- "Build {what} that {who} {value proposition}"
- "Become the {superlative} {thing} for {audience}"
- "{Action verb} {outcome} by {approach}"

---

## Core Values

### Value 1: {Name}
**What it means:** {Specific definition in context of this team}

**Why it matters:** {What problem does honoring this value solve?}

**What we optimize for:** {Concrete outcome}

**What we de-prioritize:** {Trade-off we accept}

### Value 2: {Name}
{Same structure}

### Value 3: {Name}
{Same structure}

*Note: 3-5 values is ideal. More than 7 becomes unmemorable.*

---

## Decision Tenets

When making decisions, we:

**When choosing between {X} and {Y}:**
- ✓ We choose {X} because {specific reason tied to values}
- ✗ We don't choose {Y} even though {acknowledge Y's merit}

**When facing {common dilemma}:**
- ✓ Our default is {approach} because {value}
- ⚠ Exception: When {specific condition}, we {alternative}

**When prioritizing {work/features/initiatives}:**
- 🔴 Critical: {what always gets done}
- 🟡 Important: {what gets done when possible}
- ⚪ Nice-to-have: {what we explicitly defer}

*Include 5-10 decision tenets that address real trade-offs your team faces*

---

## Observable Behaviors

**What this looks like in practice:**

**In meetings:**
- {Specific behavior that demonstrates value}
- {Specific behavior that demonstrates value}

**In code reviews / design reviews:**
- {What comments look like}
- {What we praise / what we push back on}

**In planning / prioritization:**
- {How decisions get made}
- {What questions we ask}

**In communication:**
- {How we share information}
- {How we give feedback}

**In hiring:**
- {What we look for}
- {What's a dealbreaker}

**In operations / incidents:**
- {How we respond to problems}
- {What we optimize for under pressure}

---

## Anti-Patterns

**What we explicitly DON'T do:**

- ✗ {Behavior that violates values} - even when {tempting circumstance}
- ✗ {Common industry practice we reject} - because {conflicts with which value}
- ✗ {Shortcuts we don't take} - we value {what} over {what}

---

## How to Use This

**In decision-making:**
{Practical guide for referencing these values when stuck}

**In hiring:**
{How to interview for these values, what questions to ask}

**In onboarding:**
{How new teammates should learn these values}

**In performance reviews:**
{How values factor into evaluations}

**When values conflict:**
{Which value wins in common scenarios, or how to resolve}

---

## Evolution

**Review cadence:** {How often to revisit - typically annually}

**Who can propose changes:** {Process for updating values}

**What stays constant:** {Core elements that shouldn't change}
```

## Field-by-Field Guidance

### North Star

**Purpose**: Inspiring but specific direction

**Include:**
- Who you serve
- What value you create
- What makes you distinctive

**Don't:**
- Be generic ("be the best")
- Use corporate speak
- Make it unmemorable

**Length**: 1-2 sentences max

**Test**: Can team members recite it from memory? Does it help choose between two good options?

**Examples:**

**Good:**
- "Build developer tools that spark joy and eliminate toil"
- "Make renewable energy cheaper than fossil fuels for every market by 2030"
- "Give every student personalized learning that adapts to how they learn best"

**Bad:**
- "Achieve excellence in everything we do" (generic)
- "Leverage synergies to maximize stakeholder value" (jargon)
- "Be the world's leading provider of solutions" (unmemorable, vague)

### Core Values

**Purpose**: Principles that constrain behavior

**Include:**
- Specific definition in your context
- Why it matters (what problem it solves)
- Trade-off you accept
- 3-5 values total

**Don't:**
- List every positive quality
- Be generic (every company has "integrity")
- Ignore tensions between values
- Go beyond 7 values (unmemorable)

**Structure for each value:**
- Name (1-2 words)
- Definition (what it means HERE)
- Why it matters
- What we optimize FOR
- What we de-prioritize (trade-off)

**Examples:**

**Good - Specific:**
- **Bias to action**: We'd rather ship, learn, and iterate than plan perfectly. We accept some rework to get fast feedback. We optimize for learning velocity over getting it right the first time.

**Bad - Generic:**
- **Excellence**: We strive for excellence in everything we do and never settle for mediocrity.

**Good - Shows trade-off:**
- **User delight over enterprise features**: We prioritize magical user experiences for individuals over procurement-friendly enterprise checkboxes. We'll lose some enterprise deals to keep the product simple.

**Bad - No trade-off:**
- **Customer focus**: We care deeply about our customers and always put them first.

### Decision Tenets

**Purpose**: Actionable guidance for real decisions

**Include:**
- "When choosing between X and Y..." format
- Real dilemmas your team faces
- Specific guidance, not platitudes
- 5-10 tenets

**Don't:**
- Be abstract ("choose the best option")
- Avoid acknowledging trade-offs
- Make it too long (unmemorable)

**Format:**

```
When choosing between {specific options your team actually faces}:
- ✓ We {specific action} because {which value}
- ✗ We don't {alternative} even though {acknowledge merit}
```

**Examples:**

**Good:**
```
When choosing between shipping fast and perfect quality:
- ✓ Ship with known minor bugs if user impact is low
- ✗ Don't delay for perfection
- ⚠ Exception: Anything related to payments, security, or data loss requires high quality bar
```

**Bad:**
```
When making decisions:
- Always do what's best for the customer
```

### Observable Behaviors

**Purpose**: Concrete manifestation of values

**Include:**
- Specific, observable actions
- Examples from daily work
- Things you could notice in a meeting
- 10-15 behaviors across contexts

**Don't:**
- Be vague ("communicate well")
- Only list aspirations
- Skip the messy details

**Contexts to cover:**
- Meetings
- Code/design reviews
- Planning
- Communication
- Hiring
- Operations/crisis

**Examples:**

**Good:**
- "In code reviews, we comment on operational complexity and debuggability, not just correctness"
- "In planning, we ask 'what's the simplest thing that could work?' before discussing optimal solutions"
- "We say no to features that would compromise reliability, even when customers request them"

**Bad:**
- "We communicate effectively"
- "We make good decisions"
- "We work hard"

### Anti-Patterns

**Purpose**: Explicit boundaries

**Include:**
- Common temptations you resist
- Industry practices you reject
- Shortcuts you don't take
- 3-5 clear anti-patterns

**Format:**
```
✗ {Specific behavior} - even when {tempting situation}
  Because: {which value it violates}
```

**Examples:**

**Good:**
- "✗ We don't add features without talking to users first - even when executives request them. Because: User delight > internal opinions"
- "✗ We don't skip writing tests to ship faster - even when deadline pressure is high. Because: Reliability > shipping fast"

**Bad:**
- "✗ We don't do bad things"
- "✗ We avoid poor quality"

## Quality Checklist

Before finalizing, verify:

- [ ] North Star is memorable (could team recite it?)
- [ ] Values are specific to this team (not generic)
- [ ] Each value includes a trade-off
- [ ] Decision tenets address real dilemmas
- [ ] Behaviors are observable (not abstract)
- [ ] Someone could make a decision using this TODAY
- [ ] Anti-patterns are specific
- [ ] No contradictions between sections
- [ ] Total length is 1-2 pages (concise)
- [ ] Language is clear and jargon-free

## Common Patterns by Team Type

### Engineering Team
**Focus on:**
- Technical trade-offs (simplicity, performance, reliability)
- Operational philosophy
- Code quality standards
- On-call and incident response
- Technical debt management

**Example values:**
- Simplicity over cleverness
- Reliability over features
- Developer experience matters

### Product Team
**Focus on:**
- User/customer value
- Feature prioritization
- Quality bar
- Product-market fit assumptions
- Launch criteria

**Example values:**
- User delight over feature count
- Solving real problems over building cool tech
- Data-informed over opinion-driven

### Sales/Customer-Facing
**Focus on:**
- Customer relationships
- Deal qualification
- Success metrics
- Communication style

**Example values:**
- Long-term relationships over short-term revenue
- Customer success over sales quotas
- Honesty even when it costs a deal

### Leadership Team
**Focus on:**
- Strategic priorities
- Resource allocation
- Decision-making process
- Communication norms

**Example values:**
- Transparency by default
- Disagree and commit
- Long-term value over short-term metrics

## Rollout & Socialization

**Week 1: Draft**
- Leadership creates draft
- Test against recent real decisions
- Revise based on applicability

**Week 2-3: Feedback**
- Share with team for input
- Hold working session to discuss
- Incorporate feedback
- Ensure team authorship, not just leadership

**Week 4: Launch**
- Publish finalized version
- Present at all-hands
- Explain rationale and examples
- Share how to use in daily work

**Ongoing:**
- Reference in decision-making
- Include in onboarding
- Use in hiring interviews
- Revisit quarterly, revise annually
- Celebrate examples of values in action

## Anti-Patterns to Avoid

**Vague North Star:**
- Bad: "Be the best company"
- Good: "Build developer tools that eliminate toil"

**Generic values:**
- Bad: "Integrity, Excellence, Innovation"
- Good: "Simplicity over cleverness, User delight over feature count"

**No trade-offs:**
- Bad: "Quality is important to us"
- Good: "We optimize for reliability over shipping speed, accepting slower feature velocity"

**Unmemorable length:**
- Bad: 10 pages of values, tenets, behaviors
- Good: 1-2 pages that people can actually remember

**Top-down only:**
- Bad: Leadership writes values, announces them
- Good: Collaborative process with team input and ownership

**Set and forget:**
- Bad: Write values in 2020, never revisit
- Good: Annual review, update as team evolves

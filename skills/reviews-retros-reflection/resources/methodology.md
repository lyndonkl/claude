# Reviews, Retros & Reflection: Advanced Methodologies

## Table of Contents
1. [Advanced Retrospective Formats](#1-advanced-retrospective-formats)
2. [Facilitation Techniques](#2-facilitation-techniques)
3. [Root Cause Analysis Methods](#3-root-cause-analysis-methods)
4. [Psychological Safety Building](#4-psychological-safety-building)
5. [Action Tracking and Metrics](#5-action-tracking-and-metrics)
6. [Remote and Async Retrospectives](#6-remote-and-async-retrospectives)

## 1. Advanced Retrospective Formats

### Lean Coffee (Self-Organizing Agenda)

**Setup**:
- Participants write topics on cards
- Group similar topics
- Dot vote to prioritize
- Discuss top topics time-boxed (5-7 min each)
- Thumbs up/down/sideways to continue or move on

**When**: Diverse team needs, unclear what to discuss, want emergent agenda

**Pros**: Democratic, surfaces unexpected issues, adapts to group needs
**Cons**: Can be unfocused, requires strong time-boxing

### Perfection Game (Aspirational)

**Process**:
1. Rate period 1-10 (10 = perfect)
2. "What did you like about this period?"
3. "What would make it a 10?"
4. Convert "make it 10" suggestions into actions

**When**: Positive framing needed, team demoralized, focus on future not past

**Pros**: Forward-looking, avoids negativity spiral, actionable
**Cons**: Can avoid real problems if not pushed for honesty

### Return on Time Invested (ROTI)

**Process**:
- Each participant rates retro value: thumb up (worth time), sideways (neutral), down (waste of time)
- Anonymous or public depending on culture
- Discuss: What made it valuable/not? How to improve next time?

**When**: End of every retro to improve retro itself

**Metrics to track**: % thumbs up over time (target: >80%)

### Starfish (Five Categories)

**Categories**:
- **Keep Doing**: Works well, maintain
- **Less Of**: Doing too much, scale back
- **More Of**: Doing some, do more
- **Stop Doing**: Not working, eliminate
- **Start Doing**: Not doing, should begin

**When**: More nuance than Start/Stop/Continue, want gradation

**Pros**: Spectrum of actions, acknowledges partial successes
**Cons**: More complex, can overwhelm with options

### Speedboat with Crew (Team Dynamics Focus)

**Extended metaphor**:
- **Captain** (leadership): What's steering us?
- **Crew** (team): What's propelling us?
- **Wind** (external help): What's helping externally?
- **Anchor** (drag): What's slowing us?
- **Rocks** (risks): What dangers ahead?
- **Shore** (safety): What's our safety net?
- **Island** (goal): Where are we going?

**When**: Complex team dynamics, cross-functional alignment, strategic context needed

### Kaleidoscope (Multiple Perspectives)

**Process**:
- Divide team into small groups (3-4 people)
- Each group discusses period from different lens:
  - Customer perspective
  - Business perspective
  - Technical perspective
  - Team health perspective
- Groups share findings
- Synthesize cross-perspective insights

**When**: Cross-functional team, need multiple viewpoints, large retro (>10 people)

## 2. Facilitation Techniques

### Balancing Participation

**Silent participants**:
- Call on directly with specific question
- Use round-robin (everyone speaks once before anyone twice)
- Silent brainstorming before verbal discussion
- Anonymous input (digital tools, sticky notes)

**Dominant participants**:
- "Let's hear from folks who haven't spoken yet"
- Time limits per person
- Parking lot for off-topic deep dives
- Private conversation outside retro if pattern persists

**Conflict emergence**:
- Acknowledge tension, don't dismiss
- Reframe as system/process issue, not personal
- Focus on data/facts, not judgments
- Table if too heated, address offline with parties

### Time-Boxing Discipline

**Visible timer**: Project countdown timer, everyone sees time remaining

**Gentle warnings**: "3 minutes left on this topic"

**Hard stops**: Move on even mid-discussion (capture in parking lot if needed)

**Flex time**: Reserve 10-15 min at end for parking lot topics if time permits

### Clustering and Affinity Mapping

**Process**:
1. Gather all items (sticky notes, digital cards)
2. Read aloud without discussion
3. Ask: "Which items are about the same thing?"
4. Physically group similar items
5. Name each cluster (theme)
6. Dot vote on clusters, not individual items

**Benefit**: Reduces 30 individual items to 5-6 themes, focuses discussion

### Dot Voting Variants

**Standard**: Each person gets 3-5 votes, distribute as they wish (can multi-vote same item)

**Forced distribution**: Must place votes on different items (prevents piling)

**Weighted**: Different color dots for "must discuss" (3 pts) vs "nice to have" (1 pt)

**Quadrant voting**: Vote on impact AND effort separately, plot on 2x2 matrix

### Parking Lot Management

**Purpose**: Capture important but off-topic ideas without derailing

**Process**:
- Visible "parking lot" section (whiteboard, digital doc)
- When topic emerges: "This is important. Let's park it and return if time."
- At end: Review parking lot, decide which to address (next retro, separate meeting, async)

**Don't let parking lot become graveyard**: Follow up or explicitly discard

## 3. Root Cause Analysis Methods

### 5 Whys (Iterative Questioning)

**Process**:
1. State problem: "We missed sprint goal by 20%"
2. Why? "Too much unplanned work came in"
3. Why? "Sales committed features without engineering input"
4. Why? "No clear process for vetting customer requests"
5. Why? "We haven't defined roles in customer escalations"
6. Why? "Product/Sales alignment meetings were cancelled repeatedly"

**Root cause**: Inconsistent cross-functional communication, not just "too much work"

**Pitfalls**: Stopping too early (symptom not root), blaming people not systems

### Fishbone/Ishikawa Diagram (Categorical)

**Structure**: Problem at head, "bones" are categories of causes

**Categories (6Ms for manufacturing, adapt for software)**:
- **Methods**: Processes, workflows
- **Machines**: Tools, systems, infrastructure
- **Materials**: Code, data, resources
- **Measurements**: Metrics, monitoring
- **Mother Nature/Environment**: External factors
- **Manpower/People**: Skills, capacity, communication

**Process**:
1. Draw fishbone, problem at right
2. Brainstorm causes in each category
3. For each cause, ask "why?" to find sub-causes
4. Identify which causes have most sub-causes or highest impact
5. Select root causes to address

**When**: Complex problem with multiple contributing factors, want structured brainstorming

### Timeline Analysis (Chronological Reconstruction)

**Process**:
1. Draw timeline of period (days, weeks, sprints)
2. Plot events chronologically:
   - Decisions made
   - Incidents occurred
   - Metrics changed
   - External events (outages, launches, org changes)
3. Mark sentiment highs/lows
4. Look for patterns:
   - What preceded highs? (replicate)
   - What preceded lows? (avoid)
   - Clustering of incidents?
   - Recurring cycles?

**When**: Long period (quarter), complex project, team needs shared understanding of sequence

**Insight example**: "Every time we skip retrospective, next sprint has more bugs" (correlation)

### Systemic Root Cause (Layers of Systems)

**Go beyond immediate cause to systemic**:
- **Immediate**: "Typo caused outage"
- **Proximate**: "No code review caught it"
- **Systemic**: "Code review process not enforced on urgent fixes"
- **Cultural**: "Urgency culture prioritizes speed over safety"

**Questions to surface systemic issues**:
- "What allowed this to happen?"
- "What would prevent this in the future?"
- "Is this an isolated incident or pattern?"
- "What incentives/pressures contributed?"

## 4. Psychological Safety Building

### Pre-Retro Norms Setting

**Establish explicitly** (don't assume):
- Prime Directive: Everyone did best with what they had
- Focus on systems/processes, not people
- Listen to understand, not to judge
- Disagree respectfully
- What's said here stays here (Chatham House Rule)
- Assume positive intent

**Post visibly**: On screen share, whiteboard, meeting notes

**Reference during**: "Remember, we're focusing on the process, not individuals"

### Blameless Language

**Shift from**:
- "You broke production" → "Production broke when X was deployed"
- "Why didn't you test this?" → "What prevented testing from catching this?"
- "That was a stupid decision" → "What information led to that decision?"

**Focus on learning, not fault**: "What can we learn?" not "Who's responsible?"

### Retro Facilitator Rotation

**Why**: Prevents one person's biases from dominating, distributes facilitation skill

**How**: Rotate each retro, pair new facilitators with experienced

**Training**: Share facilitation guide, observe retros, debrief after facilitation

### Confidentiality vs Transparency

**Rule of thumb**: What's said in retro stays in retro UNLESS:
- It's an action item that needs external visibility
- Team explicitly decides to share broadly
- It's a safety/legal/ethical issue requiring escalation

**Document actions, not discussions**: Share what we'll do, not who said what

### Building Trust Over Time

**Early retros** (first 3-5): Focus on safe topics (tools, process), celebrate wins, build habit

**Mid-term** (after ~10): Team comfortable, can address harder topics (communication, decision-making)

**Mature retros**: Can discuss interpersonal issues, performance, strategic direction

**Regression**: If trust breaks (leadership change, reorganization), return to basics

## 5. Action Tracking and Metrics

### Action Completion Tracking

**Metrics**:
- **Completion rate**: % actions completed before next retro (target: >80%)
- **Cycle time**: Days from action creation to completion (target: <14 days for sprint teams)
- **Carry-over rate**: % actions moved to next retro (target: <20%)

**Dashboard** (simple spreadsheet or tool):

| Action | Owner | Due | Status | Completed | Notes |
|--------|-------|-----|--------|-----------|-------|
| Create standup template | Sarah | Nov 18 | ✓ Done | Nov 17 | |
| Fix CI pipeline timeout | James | Nov 25 | ⚠ In Progress | - | Blocked on infra |

**Review at start of every retro**: Celebrate completions, discuss blockers, decide on carry-overs

### Leading Indicators (Retro Health)

**Participation rate**: % team attending (target: 100% or explained absence)

**Engagement**: % participants contributing ideas (target: >80%)

**ROTI scores**: % thumbs up on retro value (target: >80%)

**Sentiment trend**: Are Mad/Sad decreasing, Glad increasing over time?

**Repeat issues**: Same problem >3 retros → escalate to leadership (systemic issue beyond team control)

### Lagging Indicators (Business Impact)

**Team performance**:
- Velocity trend (increasing/stable/decreasing)
- Bug rate trend (decreasing ideal)
- On-time delivery % (increasing ideal)

**Team health**:
- Turnover rate (decreasing ideal)
- Engagement scores (increasing ideal)
- Sick leave patterns (stable or decreasing ideal)

**Correlation**: Do teams with regular retros + high action completion have better metrics?

### Action Type Distribution

**Track action categories** over time:
- **Process**: 40-50% (change how we work)
- **Technical**: 20-30% (tools, infrastructure, code quality)
- **Communication**: 15-25% (meetings, documentation, alignment)
- **Team dynamics**: 5-15% (collaboration, morale, conflict)

**Red flags**:
- >60% process actions → too much overhead, simplify
- 0% technical actions → accumulating technical debt
- >30% communication actions → organizational dysfunction

## 6. Remote and Async Retrospectives

### Synchronous Remote Retros

**Tools**: Miro, Mural, Jamboard, FigJam, Retrium

**Best practices**:
- **Cameras on**: Increases engagement, reads body language
- **Silent brainstorming**: Everyone types simultaneously (prevents groupthink, balances introverts/extroverts)
- **Timers visible**: Keep time-boxing discipline
- **Breakout rooms**: For large teams, split for intimate discussion, reconvene for synthesis
- **Emoji reactions**: Quick, non-verbal feedback during shares

**Challenges**:
- Harder to read room energy → Check in explicitly: "Sensing some tension, am I reading that right?"
- Tech issues → Have backup plan (phone-in, async fallback)
- Timezone spread → Rotate times to share burden, or go async

### Async Retrospectives

**When**: Extreme timezone spread (>8 hours), team prefers written reflection

**Process** (5-day cycle):
1. **Monday**: Facilitator posts retro format, instructions, deadline (Friday)
2. **Mon-Thu**: Team adds items asynchronously
3. **Thursday**: Facilitator clusters items, posts summary, asks for votes
4. **Friday**: Team votes on priorities, facilitator summarizes top themes
5. **Friday PM**: Facilitator proposes actions based on votes/themes
6. **Monday (next week)**: Finalize actions, assign owners

**Pros**: Time to reflect deeply, written record, inclusive of all timezones
**Cons**: Less energy, harder to build on ideas, slower resolution

**Hybrid approach**: Async data gathering, sync discussion and action planning (60 min)

### Tooling Recommendations

**Simple** (small teams, <10 people):
- Google Docs/Slides: Shared doc, everyone edits simultaneously
- Jamboard: Simple, sticky-note style

**Advanced** (large teams, dedicated retros):
- **Retrium**: Purpose-built for retros, many formats, voting, action tracking
- **Miro/Mural**: Infinite canvas, rich templates, integrations
- **Parabol**: Open-source, async support, Jira integration

**Action tracking**:
- Lightweight: Spreadsheet in shared drive
- Integrated: Jira, Linear, Asana (link retro actions to work tracking)
- Dedicated: Retrium, Parabol (built-in action tracking and reminders)

---

## Workflow Integration

**When to use advanced techniques**:

**Advanced formats** → When standard formats feel stale, team wants variety
**Root cause analysis** → When recurring issues appear >3 times, need depth
**Facilitation techniques** → When participation imbalanced, conflicts emerge
**Psychological safety building** → New teams, post-conflict, low trust
**Metrics tracking** → Mature retro practice, want to measure improvement
**Remote/async** → Distributed teams, timezone challenges

**Progression**:
1. **Start simple**: Start/Stop/Continue, 30-min retros, basic facilitation
2. **Build habit**: Consistent schedule, track action completion, >80% attendance
3. **Deepen practice**: Experiment with formats, root cause techniques, track metrics
4. **Embed in culture**: Retros feel safe, honest, valuable; team requests retros proactively

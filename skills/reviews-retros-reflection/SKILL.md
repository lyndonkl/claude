---
name: reviews-retros-reflection
description: Facilitates structured team reflection through retrospectives, post-mortems, after-action reviews, and weekly/quarterly reviews, producing root cause analysis and SMART action items with psychological safety. Use when conducting sprint retrospectives, project post-mortems, weekly reviews, quarterly reflections, after-action reviews (AARs), or when user mentions "retro", "retrospective", "what went well", "lessons learned", "reflection", or "how can we improve".
---

# Reviews, Retros & Reflection

## Table of Contents
1. [Workflow](#workflow)
2. [Retrospective Formats](#retrospective-formats)
3. [Common Patterns](#common-patterns)
4. [Guardrails](#guardrails)
5. [Quick Reference](#quick-reference)

## Workflow

Copy this checklist and track your progress:

```
Retrospective Progress:
- [ ] Step 1: Set the stage (context, psychological safety)
- [ ] Step 2: Gather data (what happened)
- [ ] Step 3: Generate insights (why it happened)
- [ ] Step 4: Decide actions (what to change)
- [ ] Step 5: Close and follow up (commit, track)
```

**Step 1: Set the stage**

Define period/scope, review previous action items, establish psychological safety (Prime Directive: "everyone did best job given knowledge/skills/resources/context"). For quick reviews → Use [resources/template.md](resources/template.md). For complex team retros → Study [resources/methodology.md](resources/methodology.md).

**Step 2: Gather data**

Collect facts about period: metrics (velocity, bugs, incidents), events (launches, blockers, decisions), sentiment (team energy, morale). See [Retrospective Formats](#retrospective-formats) for collection methods.

**Step 3: Generate insights**

Identify patterns, root causes, surprises. Ask "why?" to move from symptoms to causes. Use [resources/methodology.md](resources/methodology.md) for root cause techniques (5 Whys, fishbone diagrams, timeline analysis).

**Step 4: Decide actions**

Vote on most impactful improvements (dot voting, SMART criteria). Define 1-3 SMART actions (Specific, Measurable, Assigned owner, Realistic, Time-bound). See [Common Patterns](#common-patterns) for action quality criteria.

**Step 5: Close and follow up**

Commit to actions, schedule check-in, thank participants. Track action completion rate (target: >80% completion before next retro). Self-check using `resources/evaluators/rubric_reviews_retros_reflection.json` before closing. Minimum standard: Average score ≥ 3.5.

## Retrospective Formats

**Start/Stop/Continue (Simple, Balanced):**
- **Start**: What should we begin doing?
- **Stop**: What should we stop doing?
- **Continue**: What's working well, keep doing?
- **When**: General purpose, new teams, tight on time (30 min)

**Mad/Sad/Glad (Emotion-Focused):**
- **Mad**: What frustrated or angered you?
- **Sad**: What disappointed you?
- **Glad**: What made you happy?
- **When**: Processing difficult period, improving morale, surfacing hidden issues

**4Ls (Comprehensive):**
- **Loved**: What did we love?
- **Learned**: What did we learn?
- **Lacked**: What did we lack?
- **Longed for**: What did we long for?
- **When**: End of major project, quarterly reviews, want depth

**Sailboat/Speedboat (Metaphor-Based):**
- **Wind** (helping): What's propelling us forward?
- **Anchor** (hindering): What's slowing us down?
- **Rocks** (risks): What dangers lie ahead?
- **Island** (goal): Where are we going?
- **When**: Strategic planning, visualizing progress, cross-functional teams

**Timeline (Chronological):**
- Plot events on timeline, mark highs/lows, identify patterns
- **When**: Long period (quarter), complex project, need shared understanding

## Common Patterns

**Pattern 1: Sprint Retrospective (Agile)**
- **Frequency**: Every 1-2 weeks
- **Duration**: 45-90 min (shorter sprints = shorter retros)
- **Focus**: Process improvements, team dynamics, technical practices
- **Format**: Start/Stop/Continue or Mad/Sad/Glad
- **Actions**: 1-3 process improvements, 1 technical improvement

**Pattern 2: Project Post-Mortem**
- **Frequency**: End of project/phase
- **Duration**: 90-120 min
- **Focus**: What to repeat, what to avoid, systemic issues
- **Format**: 4Ls or Timeline
- **Actions**: Documentation updates, playbook changes, skill gaps to address

**Pattern 3: Weekly Team Review**
- **Frequency**: Weekly (Fridays common)
- **Duration**: 15-30 min
- **Focus**: Wins, blockers, priorities for next week
- **Format**: Custom (Wins/Blockers/Priorities)
- **Actions**: Blocker removal, celebrate wins, align on top 3 priorities

**Pattern 4: Incident Retrospective**
- **Frequency**: After major incidents
- **Duration**: 60 min
- **Focus**: Blameless analysis, system improvements
- **Format**: Timeline + 5 Whys
- **Actions**: Incident response improvements, monitoring/alerting, prevention

## Guardrails

**Psychological safety:**
- **Prime Directive**: "Regardless of what we discover, we understand and truly believe that everyone did the best job they could, given what they knew at the time, their skills and abilities, the resources available, and the situation at hand."
- Focus on processes/systems, not people
- No blame, no judgment, no defensiveness
- Encourage dissenting opinions
- What's said in retro stays in retro (unless actionable for others)

**Quality standards:**
- **Action items are SMART**: Specific, Measurable, Assigned, Realistic, Time-bound
- **Track completion**: >80% action completion before next retro (if <80%, too many actions or not committed)
- **Rotate facilitator**: Different person each time, prevents bias
- **Time-box discussions**: Don't get stuck, move on, revisit if time
- **Vote for focus**: Use dot voting to prioritize discussion topics

**Common pitfalls to avoid:**
- **Too many actions**: >5 actions = none get done. Focus on 1-3 high-impact items.
- **Vague actions**: "Improve communication" → ❌. "Daily 15-min standup in #eng-sync by Monday" → ✓
- **No follow-up**: Actions from last retro ignored → trust erodes, retros become theater
- **Blame culture**: Pointing fingers → people stop being honest
- **Same issues every retro**: If no progress on recurring issues, escalate to leadership

## Quick Reference

**Resources:**
- **Quick retro formats**: [resources/template.md](resources/template.md)
- **Facilitation techniques**: [resources/methodology.md](resources/methodology.md)
- **Quality rubric**: `resources/evaluators/rubric_reviews_retros_reflection.json`

**5-Stage Process**: Set Stage → Gather Data → Generate Insights → Decide Actions → Close

**Top Formats**:
- **Start/Stop/Continue**: General purpose, 30 min
- **Mad/Sad/Glad**: Emotion processing, 45 min
- **4Ls**: Deep reflection, 60 min
- **Sailboat**: Visual/strategic, 60 min

**Action Quality**: SMART criteria + <5 total + >80% completion rate

**Psychological Safety**: Prime Directive + Blameless + Confidential

---
name: goal-reset-proposal
description: Drafts a proposed diff to substacker shared-context/goals.md showing which lines to add, remove, or change based on the quarter's review. Never writes to goals.md directly — writer applies manually. Used once per Growth Strategist review. Trigger keywords: goal reset, goals diff, update goals, goals proposal, rework goals.
---

# Goal Reset Proposal

## Workflow

```
After the three questions + bet + kill list are drafted:
- [ ] Step 1: Read current goals.md line by line
- [ ] Step 2: For each goal, ask:
    - Is it still true?
    - Has it been met?
    - Is it vestigial?
    - Is it inconsistent with this review's conclusions?
- [ ] Step 3: Propose changes as unified-diff block with prose justification
- [ ] Step 4: Keep goals list short — if diff adds >2 goals without removing any, reject and retry
```

## Output format

```diff
- Goal: {old line}
+ Goal: {new line}
+ Goal: {added goal}
```

Followed by one paragraph justifying the changes, explicitly naming which review conclusion drove each change.

## Worked example

```diff
- Goal: Reach 1,000 subscribers by end of 2026
+ Goal: Reach 500 subscribers by end of Q2; 1,000 by end of Q3 if applied-experiments keeps its lift
- Goal: Publish one post per week
+ Goal: Publish biweekly (7 posts per quarter is the floor); one flagship post per month
+ Goal: By end of Q2, at least 3 posts in a second named section, OR formal decision to consolidate into one section
```

**Justification**: the "1000 by EOY" is a year-end abstraction; breaking into Q2/Q3 milestones makes it actionable. The weekly cadence missed 7 of 13 weeks — biweekly is what happens, and writing it down removes the guilt tax. The second-section goal forces the emergence decision rather than letting it drift.

## Guardrails

1. Never silently rewrite goals.md. Propose diff; writer applies.
2. Keep goals list short. Max 5-7 active goals. If diff adds more than 2 without removing any, rethink.
3. Every change tied to a specific review conclusion (uncomfortable question answer, bet, kill list item).
4. Preserve goals.md's tone (short, declarative, actionable).
5. Never promote an aspirational target to a goal without evidence the writer can execute in 13 weeks.

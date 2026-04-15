---
name: communication-storytelling
description: Transforms analysis, data, and complex information into clear, persuasive narratives tailored to specific audiences — executives, customers, investors, or non-technical stakeholders. Provides story structures (Hero's Journey, Problem-Solution-Benefit, Situation-Complication-Resolution) and audience adaptation techniques. Use when presenting findings, explaining technical concepts to non-technical audiences, writing announcements, or when user mentions "write this for", "explain to", "present findings", "make this compelling", or "audience is".
---

# Communication Storytelling

## Table of Contents
- [Overview](#overview)
- [Workflow](#workflow)
- [Story Structure](#story-structure)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Overview

This skill crafts compelling stories using a structured framework: (1) Headline — single clear statement capturing the essence, (2) Key Points — 3-5 supporting ideas with logical flow, (3) Proof — evidence, data, examples that substantiate, (4) Call-to-Action — what audience should think, feel, or do.

**Quick example:**

**Bad (data dump):**
"Our Q2 revenue was $2.3M, up from $1.8M in Q1. Customer count went from 450 to 520. Churn decreased from 5% to 3.2%. NPS improved from 42 to 58. We launched 3 new features..."

**Good (storytelling):**
"We've reached product-market fit. Three signals prove it: (1) Revenue grew 28% while sales capacity stayed flat—customers are pulling product from us, not the other way around. (2) Churn dropped 36% as we focused on power users, with our top segment now at 1% monthly churn. (3) NPS jumped 16 points to 58, with customers specifically praising the three features we bet on. Recommendation: Double down on power user segment with premium tier."

## Workflow

Copy this checklist and track your progress:

```
Communication Storytelling Progress:
- [ ] Step 1: Gather inputs and clarify audience
- [ ] Step 2: Choose appropriate narrative structure
- [ ] Step 3: Craft the narrative
- [ ] Step 4: Validate quality and clarity
- [ ] Step 5: Deliver and adapt
```

**Step 1: Gather inputs and clarify audience**

Ask user for the message (analysis, data, information to communicate), audience (who will receive this), purpose (inform, persuade, inspire, build trust), context (situation, stakes, constraints), and tone (formal, casual, urgent, celebratory). Understanding audience deeply is critical—their expertise level, concerns, decision authority, and time constraints shape everything. See [resources/template.md](resources/template.md) for input questions.

**Step 2: Choose appropriate narrative structure**

For standard communications (announcements, updates, presentations) → Use [resources/template.md](resources/template.md) quick template. For complex multi-stakeholder communications requiring different versions → Study [resources/methodology.md](resources/methodology.md) for audience segmentation and narrative adaptation techniques. To see what good looks like → Review [resources/examples/](resources/examples/).

**Step 3: Craft the narrative**

Create `communication-storytelling.md` with: (1) Compelling headline that captures essence in one sentence, (2) 3-5 key points arranged in logical flow (chronological, problem-solution, importance-ranked), (3) Concrete proof for each point (data, examples, quotes, stories), (4) Clear call-to-action stating what audience should do next. Use storytelling techniques: specificity over generality, show don't tell, human stories over abstract concepts, tension/resolution arcs. See [Story Structure](#story-structure) for narrative patterns.

**Step 4: Validate quality and clarity**

Self-assess using [resources/evaluators/rubric_communication_storytelling.json](resources/evaluators/rubric_communication_storytelling.json). Check: headline is clear and compelling, key points are distinct and well-supported, proof is concrete and relevant, flow is logical, tone matches audience, jargon is appropriate for expertise level, call-to-action is clear and achievable, length matches time constraints. Read aloud to test clarity. Test with "so what?" question—does each point answer why audience should care? Minimum standard: Average score ≥ 3.5 before delivering.

**Step 5: Deliver and adapt**

Present the completed `communication-storytelling.md` file. Highlight how narrative addresses audience's key concerns. Note storytelling techniques used (data humanized, tension-resolution, specificity). If user has feedback or needs adaptations for different audiences, use [resources/methodology.md](resources/methodology.md) for multi-version strategy.

## Story Structure

### The Hero's Journey (Transformation Story)

**When to use:** Major changes, pivots, overcoming challenges

**Structure:**
1. **Status Quo** - Where we were (comfort, but problem lurking)
2. **Call to Adventure** - Why we had to change (problem emerges)
3. **Trials** - What we tried, what we learned (struggle builds credibility)
4. **Victory** - What worked (resolution)
5. **Return with Knowledge** - What we do now (new normal, lessons learned)

**Example:** "We were growing 20% YoY, but churning 10% monthly—unsustainable. Data showed we were solving the wrong problem for the wrong users. We tested 5 hypotheses over 3 months, failing at 4. The one that worked: focusing on power users willing to pay 5x more. Churn dropped to 2%, growth hit 40% YoY. Now we're betting everything on premium tier."

### Problem-Solution-Benefit (Decision Story)

**When to use:** Recommendations, proposals, project updates

**Structure:**
1. **Problem** - Clearly defined issue with stakes (what happens if unaddressed)
2. **Solution** - Your recommendation with rationale (why this, not alternatives)
3. **Benefit** - Tangible outcomes (quantified impact)

**Example:** "We lose 30% of signups at checkout—$2M ARR left on table. Root cause: we ask for credit card before users see value. Proposal: 14-day trial, no card required, with onboarding emails showing ROI. Comparable companies saw 60% conversion lift. Expected impact: +$1.2M ARR with 4-week implementation."

### Before-After-Bridge (Contrast Story)

**When to use:** Product launches, feature announcements, process improvements

**Structure:**
1. **Before** - Current painful state (audience's lived experience)
2. **After** - Improved future state (what becomes possible)
3. **Bridge** - How to get there (your solution)

**Example:** "Before: Sales team spends 10 hours/week manually exporting data, cleaning it in spreadsheets, and copy-pasting into slide decks—error-prone and soul-crushing. After: One-click report generation with live data, auto-refreshing dashboards, 30 minutes per week. Bridge: We built sales analytics v2.0, launching Monday with training sessions."

### Situation-Complication-Resolution (Executive Story)

**When to use:** Executive communications, board updates, investor relations

**Structure:**
1. **Situation** - Context and baseline (set the stage)
2. **Complication** - What changed or what's at stake (creates tension)
3. **Resolution** - Your path forward (release tension)

**Example:** "Situation: We budgeted $5M for customer acquisition in 2024. Complication: iOS 17 privacy changes killed our primary ad channel—50% drop in conversion overnight. Resolution: Shifting $2M to content marketing (3-month ROI), $1M to partnerships (immediate distribution), keeping $2M in ads for testing new channels. Risk: content takes time to scale, but partnerships derisk timeline."

## Common Patterns

**Data-Heavy Communications:**
- Lead with insight, not data
- One number per point (too many = confusion)
- Humanize data with stories: "42% churn" → "We lose 12 customers every week—that's Sarah's entire cohort from January"
- Use comparisons for context: "200ms latency" → "2x slower than competitors, 3x slower than last year"

**Technical → Non-Technical:**
- Translate jargon: "distributed consensus algorithm" → "how servers agree on truth without a central authority"
- Use analogies from audience's domain: "Kubernetes is like a airport air traffic control for containers"
- Focus on business impact, not technical implementation
- Anticipate "why does this matter?" and answer it explicitly

**Change Management:**
- Acknowledge the loss/pain (don't gloss over difficulty)
- Paint compelling future state (hope, not just fear)
- Show path from here to there (make it concrete)
- Address "what about me?" early (personal impact)

**Crisis Communications:**
- Lead with facts (what happened, when, impact)
- Take accountability (no blame-shifting or weasel words)
- State what you're doing (concrete actions with timeline)
- Commit to transparency (when they'll hear next)

## Guardrails

**Do:**
- ✅ Test headline clarity—can someone understand the essence in 10 seconds?
- ✅ Use concrete specifics over vague generalities
- ✅ Match sophistication level to audience (avoid talking up or down)
- ✅ Front-load conclusions (executives decide in first 30 seconds)
- ✅ Show your work for major claims (data sources, assumptions)
- ✅ Acknowledge limitations and risks (builds credibility)

**Don't:**
- ❌ Bury the lede (most important thing must be first)
- ❌ Use jargon your audience doesn't know (or define it)
- ❌ Make claims without proof (erodes trust)
- ❌ Assume audience cares—make them care by showing stakes
- ❌ Write walls of text (use bullets, headers, white space)
- ❌ Lie or mislead (including by omission)

**Red Flags:**
- 🚩 Your draft is mostly bullet points with no narrative arc
- 🚩 You can't summarize your message in one sentence
- 🚩 You use passive voice to avoid accountability ("mistakes were made")
- 🚩 You include data that doesn't support your points
- 🚩 Your call-to-action is vague ("be better," "work harder")

## Quick Reference

**Resources:**
- **[resources/template.md](resources/template.md)** - Quick-start template with headline, key points, proof structure
- **[resources/methodology.md](resources/methodology.md)** - Advanced techniques for multi-stakeholder communications, narrative frameworks, persuasion principles
- **[resources/examples/](resources/examples/)** - Worked examples showing different story structures and audiences
- **[resources/evaluators/rubric_communication_storytelling.json](resources/evaluators/rubric_communication_storytelling.json)** - 10-criteria quality rubric with audience-based thresholds

**When to use which resource:**
- Standard communication → Start with template.md
- Multiple audiences for same message → Study methodology.md multi-version strategy
- Complex persuasion (board pitch, investor update) → Study methodology.md persuasion frameworks
- Unsure what good looks like → Review examples/ for your scenario
- Before delivering → Validate with rubric (score ≥ 3.5 required)

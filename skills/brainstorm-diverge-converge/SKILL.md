---
name: brainstorm-diverge-converge
description: Use when you need to generate many creative options before systematically narrowing to the best choices. Invoke when exploring product ideas, solving open-ended problems, generating strategic alternatives, developing research questions, designing experiments, or when you need both breadth (many ideas) and rigor (principled selection). Use when user mentions brainstorming, ideation, divergent thinking, generating options, or evaluating alternatives.
---

# Brainstorm Diverge-Converge

## Table of Contents

- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [What is Brainstorm Diverge-Converge?](#what-is-brainstorm-diverge-converge)
- [Workflow](#workflow)
  - [1. Gather Requirements](#1--gather-requirements)
  - [2. Diverge (Generate Ideas)](#2--diverge-generate-ideas)
  - [3. Cluster (Group Themes)](#3--cluster-group-themes)
  - [4. Converge (Evaluate & Select)](#4--converge-evaluate--select)
  - [5. Document & Validate](#5--document--validate)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Apply structured divergent-convergent thinking to generate many creative options, organize them into meaningful clusters, then systematically evaluate and narrow to the strongest choices. This balances creative exploration with disciplined decision-making.

## When to Use This Skill

- Generating product or feature ideas
- Exploring solution approaches for open-ended problems
- Developing research questions or hypotheses
- Creating marketing or content strategies
- Identifying strategic initiatives or opportunities
- Designing experiments or tests
- Naming products, features, or projects
- Developing interview questions or survey items
- Exploring design alternatives (UI, architecture, process)
- Prioritizing from a large possibility space
- Overcoming creative blocks
- When you need both quantity (many options) and quality (best options)

**Trigger phrases:** "brainstorm", "generate ideas", "explore options", "what are all the ways", "divergent thinking", "ideation", "evaluate alternatives", "narrow down choices"

## What is Brainstorm Diverge-Converge?

A three-phase creative problem-solving method:

- **Diverge (Expand)**: Generate many ideas without judgment or filtering. Focus on quantity and variety. Defer evaluation.

- **Cluster (Organize)**: Group similar ideas into themes or categories. Identify patterns and connections. Create structure from chaos.

- **Converge (Select)**: Evaluate ideas against criteria. Score, rank, or prioritize. Select strongest options for action.

**Quick Example:**

```markdown
# Problem: How to improve customer onboarding?

## Diverge (30 ideas)
- In-app video tutorials
- Interactive walkthroughs
- Email drip campaign
- Live webinar onboarding
- 1-on-1 concierge calls
- ... (25 more ideas)

## Cluster (6 themes)
1. **Self-serve content** (videos, docs, tooltips)
2. **Interactive guidance** (walkthroughs, checklists)
3. **Human touch** (calls, webinars, chat)
4. **Motivation** (gamification, progress tracking)
5. **Timing** (just-in-time help, preemptive)
6. **Social** (community, peer examples)

## Converge (Top 3)
1. Interactive walkthrough (high impact, medium effort) - 8.5/10
2. Email drip campaign (medium impact, low effort) - 8.0/10
3. Just-in-time tooltips (medium impact, low effort) - 7.5/10
```

## Workflow

Follow these steps in order:

### 1. [ ] Gather Requirements

Ask the user to clarify:
- [ ] **Topic/problem**: What are you brainstorming about?
- [ ] **Goal**: What decision will this inform?
- [ ] **Constraints**: Any must-haves, no-gos, or boundaries?
- [ ] **Evaluation criteria**: What makes an idea "good"? (e.g., impact, feasibility, cost, speed)
- [ ] **Target quantity**: How many ideas to generate? (suggest 20-50 for most cases)
- [ ] **Rounds**: Single session or multiple rounds? (default: 1 round)

### 2. [ ] Diverge (Generate Ideas)

Generate many ideas without judgment:
- [ ] **Suspend criticism**: All ideas are valid during divergence
- [ ] **Aim for quantity**: More ideas = more raw material
- [ ] **Encourage variety**: Different types, scales, approaches
- [ ] **Use prompts** to stimulate creativity:
  - "What if we had unlimited resources?"
  - "What would a competitor do?"
  - "What's the simplest possible approach?"
  - "What's the most ambitious version?"
  - "What are unconventional alternatives?"
- [ ] **Target**: Generate 20-50 ideas (adjust based on complexity)
- [ ] **Output**: Numbered list of raw ideas

**For simple topics** → Generate ideas directly in SKILL.md

**For complex topics** → Study `resources/template.md` for structured prompts and techniques

### 3. [ ] Cluster (Group Themes)

Organize ideas into meaningful groups:
- [ ] **Identify patterns**: Which ideas are similar or related?
- [ ] **Create categories**: Group by approach, theme, or mechanism
- [ ] **Name clusters**: Give each cluster a clear, descriptive label
- [ ] **Check coverage**: Do clusters represent distinct approaches?
- [ ] **Target**: 4-8 clusters (fewer than 4 = not enough variety; more than 8 = too fragmented)
- [ ] **Output**: Clusters with ideas grouped under each

**Clustering approaches:**
- By mechanism (how it works)
- By target user/audience
- By timeline (short-term vs long-term)
- By resource requirements (low/medium/high effort)
- By risk level
- By strategic objective

### 4. [ ] Converge (Evaluate & Select)

Evaluate ideas systematically and select strongest:
- [ ] **Define criteria**: What makes an idea strong? (from step 1)
  - Common criteria: Impact, Feasibility, Cost, Speed, Risk, Alignment
- [ ] **Score ideas**: Rate each idea on defined criteria
  - Use simple scale (1-10 or Low/Med/High)
  - Can score individual ideas or representative ideas per cluster
- [ ] **Rank ideas**: Order by total score or weighted criteria
- [ ] **Select top options**: Identify 3-5 strongest ideas to pursue
- [ ] **Document tradeoffs**: Note why top ideas were chosen and what was deprioritized

**Evaluation patterns:**
- Impact/Effort matrix (prioritize high impact, low effort)
- Weighted scoring (multiply scores by criteria importance)
- Must-have filtering (eliminate ideas that violate constraints)
- Pairwise comparison (compare ideas head-to-head)

### 5. [ ] Document & Validate

Create output and validate quality:
- [ ] **Create** `brainstorm-diverge-converge.md` in current directory with:
  - Problem/topic statement
  - Diverge: Full list of ideas generated
  - Cluster: Ideas organized into themes
  - Converge: Scored, ranked, and selected top options
  - Next steps: Recommended actions based on selections
- [ ] **Validate quality** using `resources/evaluators/rubric_brainstorm_diverge_converge.json`

**Quality checks:**
- [ ] Diverge phase generated sufficient quantity (20+ ideas)
- [ ] Ideas show variety (not all similar)
- [ ] Clusters are distinct and well-labeled
- [ ] Evaluation criteria are explicit and relevant
- [ ] Scoring is consistent and justified
- [ ] Top selections are clearly better than alternatives
- [ ] Next steps are actionable

**Minimum standard**: Score ≥ 3.5 across all rubric criteria

If any criterion scores < 3, revise that aspect before delivering.

## Common Patterns

**For product/feature ideation:**
- Diverge: 30-50 feature ideas
- Cluster by: User need, use case, or feature type
- Converge: Impact vs. effort scoring
- Select: Top 3-5 for roadmap

**For problem-solving:**
- Diverge: 20-40 solution approaches
- Cluster by: Mechanism (how it solves problem)
- Converge: Feasibility vs. effectiveness
- Select: Top 2-3 to prototype

**For research questions:**
- Diverge: 25-40 potential questions
- Cluster by: Research method or domain
- Converge: Novelty, tractability, impact
- Select: Top 3-5 to investigate

**For strategic planning:**
- Diverge: 20-30 strategic initiatives
- Cluster by: Time horizon or strategic pillar
- Converge: Strategic value vs. resource requirements
- Select: Top 5 for quarterly planning

## Guardrails

**Do:**
- Generate at least 20 ideas in diverge phase (quantity matters)
- Suspend judgment during divergence (criticism kills creativity)
- Create distinct clusters (avoid overlap and confusion)
- Use explicit, relevant criteria for convergence (not vague "goodness")
- Score consistently across all ideas
- Document why top ideas were selected (transparency)
- Include "runner-up" ideas (for later consideration)

**Don't:**
- Filter ideas during divergence (defeats the purpose)
- Create clusters that are too similar or overlapping
- Use vague evaluation criteria ("better", "more appealing")
- Cherry-pick scores to favor pet ideas
- Select ideas without systematic evaluation
- Ignore constraints from requirements gathering
- Skip documentation of the full process

## Quick Reference

- **Template**: `resources/template.md` - Structured prompts and techniques for diverge-cluster-converge
- **Quality rubric**: `resources/evaluators/rubric_brainstorm_diverge_converge.json`
- **Output file**: `brainstorm-diverge-converge.md`
- **Typical idea count**: 20-50 ideas → 4-8 clusters → 3-5 selections
- **Common criteria**: Impact, Feasibility, Cost, Speed, Risk, Alignment

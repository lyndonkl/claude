---
name: quarterly-zoomout
description: Synthesizes 13 weeks of substacker Growth Analyst reports + the most recent Curator review + a meta-scan of the published corpus into a 400-700 word narrative that names the quarter's shape — what happened, what changed, what held steady, what surprised. Used by the Growth Strategist at the opening of every review. Trigger keywords: quarterly, zoomout, quarter narrative, rollup, what happened this quarter.
---

# Quarterly Zoomout

## Workflow

```
Per quarterly run:
- [ ] Step 1: Glob ops/growth-analyst/*.md since last Strategist review
- [ ] Step 2: Glob ops/curator/*.md — most recent
- [ ] Step 3: Meta-scan corpus/published/ (titles, dates, first paragraphs)
- [ ] Step 4: Extract top-line numbers per week (subs, delta, open rate, top post)
- [ ] Step 5: Write the narrative (400-700 words) in the writer's register
```

## Output

A markdown block for the review's executive summary + section-portfolio pages:

```markdown
{N weeks, M posts, K new subscribers}. {the headline}.
{what the Curator's map shows — which section is carrying, which drifting}.
{unusual patterns — retention, specific-post outliers, engagement baseline shifts}.
{surprises — things that changed vs last quarter}.
{open questions this synthesis raises}.
```

## Voice rules

Write in the writer's register:
- Short sentences; one metaphor max.
- No "synergy" / "trajectory" / MBA-speak without specifics.
- Specific post titles where relevant.
- "I do not know" welcome where genuinely uncertain.

## Guardrails

1. 400-700 words.
2. No absolute-number comparisons to other publications.
3. If the quarter had <4 posts, note the sparse data explicitly — the silence IS the story.
4. Never summarize the Growth Analyst weekly reports — just distill the pattern across them.
5. Reads, does not write shared-context.

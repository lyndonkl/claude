---
name: section-portfolio-assessment
description: Classifies each substacker section as healthy / drifting / candidate-for-prune based on post volume, engagement trend, and niche alignment. Produces table + 2-4 paragraph narrative. Used in every quarterly review. Trigger keywords: portfolio, section health, healthy drifting prune, section assessment, which section is carrying.
---

# Section Portfolio Assessment

## Classification rules

- **Healthy**: ≥2 posts this quarter AND engagement at or above publication baseline AND clearly inside the stated niche.
- **Drifting**: posts exist but one of: engagement below baseline, niche drift, or cadence collapse (0-1 posts).
- **Candidate for prune**: 0 posts in 2 consecutive quarters OR writer has admitted they no longer find it interesting OR its removal would make the publication more coherent.

On the boundary → "drifting" (conservative).

## Workflow

```
Per section in section-map.md:
- [ ] Step 1: Count posts this quarter + trailing 4 weeks
- [ ] Step 2: Compute engagement signal (open rate z-score vs publication baseline)
- [ ] Step 3: Check niche-fit (does the section's promise still describe what ran?)
- [ ] Step 4: Assign status: healthy | drifting | candidate-for-prune
- [ ] Step 5: Write 1-sentence "why" per section
```

## Output format

```markdown
| Section | Posts this quarter | Status | Read verdict |
|---|---|---|---|
| kalshi-log | 6 | healthy | Carrying the publication; 63% avg open; clear niche fit |
| agent-workshop | 2 | drifting | 2 posts is below cadence target; engagement on-baseline |
| book-reviews | 0 | candidate-for-prune | 0 posts in 2 consecutive quarters; unassign its 2 historical posts and retire the section |
```

Followed by 2-4 paragraphs of narrative: what the portfolio shape tells us, which section is carrying, which has gone cold.

## Guardrails

1. Label conservatively. "Drifting" beats "candidate-for-prune" on ambiguity.
2. Narrative is where the agent earns its keep. Status labels are mechanical; "why" is judgement.
3. Don't recommend pruning in this skill — that's `recommend-prune` inside Curator. Strategist flags candidates only.
4. A section can stay "healthy" on low volume if engagement is strong.

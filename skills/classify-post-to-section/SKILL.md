---
name: classify-post-to-section
description: Assigns a substacker draft or published post to the best-fitting section (or to unassigned) based on content + section promises in section-map.md. Used by the Editor on every draft review (to load the right voice overlay) and by the Curator in batch mode. Trigger keywords: classify post, section assignment, which section, route post, per-draft section.
---

# Classify Post To Section

## Workflow

```
Per post (draft or published):
- [ ] Step 1: Read post body (not just title)
- [ ] Step 2: Read section-map.md for all current section promises
- [ ] Step 3: Score post fit against each section's promise (specific, testable, voice register)
- [ ] Step 4: If top score clearly above second → assign that section
- [ ] Step 5: If ambiguous between two sections → propose both; writer picks
- [ ] Step 6: If no section scores above threshold → assign `unassigned`
- [ ] Step 7: Return: {section_slug, confidence, rationale}
```

## Scoring dimensions

For each section, compute fit on:
- **Promise match**: does this post deliver on the section's one-sentence promise?
- **Voice register**: does the post's register (confessional-operational / technical-mechanistic / epistolary) match the section's voice overlay?
- **Topic tag overlap**: does the post's internal `topics` frontmatter intersect with the section's typical topic distribution?

## Worked example

**Draft**: "KV Cache as a library card catalog" — full body on KV cache mechanics, diagram-heavy, cites Vaswani et al. and Dao et al.

**Current sections**:
- `kalshi-log`: scoreboard-required, prediction markets / IPL. Promise match: low. Score: 1/5.
- `agent-workshop`: mechanism + architecture, code-fence-welcome. Promise match: high. Score: 5/5.

**Output**: `{section_slug: agent-workshop, confidence: high, rationale: "mechanism post with explicit paper citations; matches Agent Workshop register and promise"}`.

## Guardrails

1. Never assign without scoring at least 2 candidate sections.
2. If writer has manually annotated `section: X` in frontmatter, respect it — this skill only proposes when frontmatter is missing or `unassigned`.
3. Ambiguous cases return both candidates; do not arbitrarily pick.
4. "unassigned" is a valid output. Don't force fit.
5. Read body, not just title.

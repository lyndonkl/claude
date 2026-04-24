---
name: cross-poster-blurb
description: Writes a 60-140 word third-person blurb for the Substack cross-post feature, positioned so another newsletter writer can paste it into their cross-post popup without editing. Third-person throughout ("In this piece, Kushal argues…"). No subscriber CTAs. Use as the cross-post arm of the Distribution Translator. Trigger keywords: cross-post, cross-poster, blurb, Substack cross-post, third person, positioning.
---

# Cross-Poster Blurb

## Workflow

```
Write blurb for cross-post:
- [ ] Step 1: Load spine + voice-profile + audience-notes
- [ ] Step 2: One-line positioning: "In this piece, Kushal argues…"
- [ ] Step 3: 2-3 sentences summarizing argument + one concrete anchor
- [ ] Step 4: One sentence on why a tech-adjacent audience should care
- [ ] Step 5: Sign-off minimal: "Read the full piece." or a period — no subscribe CTA
- [ ] Step 6: Enforce 60-140 words
```

## Output format

```markdown
---
source_post: {slug}.md
platform: substack-crosspost
target_length: 60-140 words
actual_length: {N}
section: {section-slug}
---

In this piece, Kushal argues {thesis}. {2-3 sentences of argument + concrete anchor}. For anyone building with {domain}, the {specific-claim} is the move that reframes the problem. Read the full piece.
```

## Worked example (Architecture, Not Prompting)

```markdown
---
source_post: architecture-not-prompting.md
platform: substack-crosspost
target_length: 60-140 words
actual_length: 98
section: agent-workshop
---

In this piece, Kushal argues that most prompt-engineering advice mistakes the unit of analysis — the lever that moves behaviour in long-running AI systems is organisational, not linguistic. Drawing on Wang et al., Anthropic (2024), which found multi-agent decompositions outperformed long-prompted single agents by roughly 40% on sustained tasks, he lays out four recurring patterns: supervisor-worker, pipeline, jury, and debate. For anyone building with agents — or watching teams ship agents that don't quite work — the reframing from "better prompt" to "better architecture" is worth the ten-minute read.
```

## Guardrails

1. Third person throughout. Never "I argue…" — the blurb will be pasted by another writer.
2. 60-140 words. Substack's cross-post popup is small; shorter reads.
3. Never say "amazing," "brilliant," "must-read" — the other writer sounds like a fan, not a curator.
4. No subscriber CTA ("subscribe to From First Principles"). Just positioning.
5. Preserve paper attributions.
6. If the essay is in a specific section, the blurb can reference the section's promise subtly — not as "Filed under."
7. Voice register: neutral-analytical. Not the writer's confessional register; the blurb represents the piece to strangers.

---
name: linkedin-post-rewrite
description: Rewrites a published substacker essay as a LinkedIn post with a hook fitting the 210-char fold, practitioner framing (less confessional than Substack), short 2-3 line paragraphs, and 0-2 niche hashtags. 900-2500 characters. Emits linkedin-post.md. Use as the LinkedIn-native arm of the Distribution Translator. Trigger keywords: LinkedIn post, LinkedIn rewrite, practitioner, professional network, niche hashtags.
---

# LinkedIn Post Rewrite

## Workflow

```
Rewrite for LinkedIn:
- [ ] Step 1: Load spine + chosen hook + voice-profile + audience-notes
- [ ] Step 2: Hook ≤210 chars (first 1-2 lines; must survive the "...see more" fold)
- [ ] Step 3: Line break, then one-sentence pivot paragraph
- [ ] Step 4: Body — 4-7 short paragraphs of 2-3 lines each (white space is structural)
- [ ] Step 5: Optional list block only if essay's spine is genuinely enumerable
- [ ] Step 6: Practitioner-takeaway closer (NOT bolded maxim — bold doesn't render well on LinkedIn)
- [ ] Step 7: Link line: `Full essay: {substack-url}`
- [ ] Step 8: 0-2 niche hashtags on final line (prefer 0-1)
- [ ] Step 9: Cap at 2500 chars total
```

## Voice shift for LinkedIn

LinkedIn reads "practitioner sharing learnings," not "writer thinking aloud." Slight voice shift allowed:

- Essay: "I do not know whether this generalizes." → LinkedIn: "I'm still figuring out if this generalizes." (same hedge, practitioner-flavored)
- Essay: "I shipped a demo in a weekend." → LinkedIn: "A team I worked with shipped a demo in a weekend." (slight depersonalization okay; full pronoun stripping not)
- Essay: Confessional opener. → LinkedIn: Confession OK but can lean "here's what broke" rather than "I was wrong."

## Output format

```markdown
---
source_post: {slug}.md
platform: linkedin
target_length: 900-2500 chars
actual_length: {N}
length_mode: short | long
hook_chars: {N}
hashtags: 0-2
section: {section-slug}
---

{hook — first 1-2 lines, ≤210 chars total}

{one-sentence pivot paragraph}

{body — 4-7 short paragraphs, 2-3 lines each}

{optional list block only if genuinely enumerable}

{practitioner takeaway — not bolded}

Full essay: {substack-url}

{#NicheHashtag1 #NicheHashtag2}  ← 0-2 only
```

## Guardrails

1. First 210 chars MUST fit the fold. Count and report in frontmatter.
2. ≤2500 chars total. LinkedIn caps at 3000 but dwell data drops above 2500.
3. 0-2 hashtags; prefer 0-1. Niche tags only (`#MultiAgentSystems`, `#LLMEngineering`). Never generic (`#AI`, `#tech`, `#innovation`, `#thoughts`, `#leadership`).
4. No bolded maxim closer — bold renders as markdown leak on LinkedIn. Use plain-text practitioner takeaway instead.
5. Paragraphs 2-3 lines max. White space is structural.
6. Use list block only if the essay's spine is genuinely enumerable. Never shoehorn.
7. Preserve paper attributions (Author, Institution, Year).
8. No emoji. No exclamation points. No custom CTA.

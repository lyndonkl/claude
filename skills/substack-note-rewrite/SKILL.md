---
name: substack-note-rewrite
description: Rewrites a published substacker essay as a Substack Note using the extracted spine and chosen hook. Closest voice to the essay. Bolded maxim closer. Single link line. 60-180 words. Emits substack-note.md in the post's distribution folder. Use as the Substack-native arm of the Distribution Translator. Trigger keywords: Substack Note, note rewrite, note post, tease, Notes feed.
---

# Substack Note Rewrite

## Workflow

```
Rewrite essay for Substack Notes:
- [ ] Step 1: Load spine + chosen hook + voice-profile + section overlay
- [ ] Step 2: Open with chosen hook (confession preferred)
- [ ] Step 3: Use 2-3 spine claims with highest translatability
- [ ] Step 4: Optional: one one-sentence pivot paragraph
- [ ] Step 5: Close with spine.closing_maxim, **bolded**
- [ ] Step 6: Add link line: `Full essay: [title]({substack-url})`
- [ ] Step 7: Voice-check pass: no don't-list, no emoji, no hashtags, no CTA
- [ ] Step 8: Enforce 60-180 word cap
```

## Output format

`ops/distribution/{date}-{slug}/substack-note.md`:

```markdown
---
source_post: {slug}.md
platform: substack-notes
target_length: 60-180 words
actual_length: {N}
hook_pattern: confession | claim | question | reframe
section: {section-slug or null}
---

{hook line}

{body — 2-5 short paragraphs, each 1-3 sentences; may use em-dash reframes and one-sentence pivots}

**{closing_maxim from spine}**

Full essay: [{title}]({substack-url})
```

## Worked example

**Input** — spine from *The Execution Gap*.

**Output `substack-note.md`** (139 words):

```markdown
I have been meaning to open a Kalshi account for months.

Not casually meaning to — the way you mean to clean the garage or read the Piketty book on the nightstand. I am one of those people who substitutes learning for doing.

Here's the experiment: $10, one IPL season, every trade logged. Brier score on every call. Real money, real scoreboard.

Say you predict a team at 80%. If they win, your Brier is (0.80 - 1)² = 0.04. If they lose, it's (0.80 - 0)² = 0.64. Overconfidence is asymmetrically punished.

I have not tried this. Not once.

**At the end of the tournament, I'll answer the question. Or I'll admit I can't.**

Full essay: [The Execution Gap](https://thethinkersnotebook.substack.com/p/the-execution-gap)
```

## Guardrails

1. Word count strictly 60–180. Under 60 = teasing; over 180 = Notes dwell-time drops.
2. No hashtags. No emoji. No exclamation points. No custom CTA.
3. Preserve paper attributions in full (Author, Institution, Year) if any appear.
4. If essay's closer is hedged ("I do not know"), Note's closer is hedged too.
5. Bolded maxim is verbatim from spine.closing_maxim. Do not edit.
6. Single link line at the end. Not mid-text.

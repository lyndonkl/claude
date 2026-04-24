---
name: platform-voice-check
description: Runs a voice-fidelity audit on each of the four substacker platform outputs (Substack Note, X thread, LinkedIn post, cross-post blurb) before reporting Distribution Translator completion. Checks for voice-don'ts (banned vocabulary, emoji, generic openers, marketing math without source), voice-do compliance (paper attribution preserved, hedges preserved, em-dash reframes present), platform-specific tonal shifts. Emits voice-check.md with pass/fail per artifact. Trigger keywords: platform voice check, voice-check, gate, distribution voice, slop-leak check.
---

# Platform Voice Check

## Workflow

```
Voice-audit the 4 platform outputs:
- [ ] Step 1: Read all 4 output files + voice-profile.md + voices/{section}.md (if applicable)
- [ ] Step 2: For each file:
    - Scan voice-don'ts (delve, unpack, paradigm shift, emoji, exclamations, I think, AI-is-transforming, custom CTA)
    - Scan voice-dos (opener classification, em-dash reframes, hedge preservation, paper attribution)
    - Platform-specific tonal shift check
- [ ] Step 3: Emit voice-check.md with pass/fail per file
- [ ] Step 4: If FAIL on any file, return the flag list to Distribution Translator for loop-back
```

## Platform-specific tonal checks

| Platform | Expected tone shift | Flag if |
|---|---|---|
| Substack Note | Closest to essay voice | Any over-polishing that reads AI-rewritten |
| X | More declarative, more quotable | Over-hedging ("Substack leak on X") |
| LinkedIn | Practitioner, slightly less confessional | Raw confession ("Substack leak on LinkedIn") |
| Cross-post | Third person | Any first-person use ("I argue…") |

## Output format

`ops/distribution/{date}-{slug}/voice-check.md`:

```markdown
---
agent: distribution-translator
date: YYYY-MM-DD
post_slug: {slug}
results:
  substack-note.md: PASS | FAIL
  x-thread.md: PASS | FAIL
  linkedin-post.md: PASS | FAIL
  cross-post-blurb.md: PASS | FAIL
---

## substack-note.md: PASS | FAIL
- (line / location) — issue — voice-profile citation

## x-thread.md: PASS | FAIL
- variant: short — line X — issue
- variant: medium — line Y — issue

## linkedin-post.md: PASS | FAIL
- ...

## cross-post-blurb.md: PASS | FAIL
- ...
```

## Loop-back

If voice-check reports FAIL on any file, Distribution Translator MUST loop back to the matching rewrite skill with the flags as input. Max 2 loops per artifact. After 2 loops:

> DESIGN-NOTE: This essay's voice may not translate cleanly to {platform}. User review recommended.

Ship best-so-far; flag for writer.

## Guardrails

1. Every flag must cite a voice-profile line. No flag without citation.
2. Advisory on first pass; blocking after 2 loops (then ship best-so-far with a design-note).
3. Do not write to the platform files directly. Emit the flag list; the rewrite skill re-runs.
4. Check banned-vocabulary regex first (fast); tonal-shift checks second (slower).
5. Paper attribution rule: if a paper is cited in the essay, check every platform file mentions Author, Institution, Year on first mention.
6. Emoji check: zero tolerance across all four files.

## Quick reference

- Runs as the final gate in the Distribution Translator pipeline.
- Advisory → loop-back → ship-best-after-2-loops.
- Output: one voice-check.md in the post's distribution folder.

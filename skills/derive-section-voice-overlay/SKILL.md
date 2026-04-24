---
name: derive-section-voice-overlay
description: Derives a draft per-section voice overlay (deltas against substacker global voice-profile) once a section reaches ≥3 published posts with shared voice tells. Writes to shared-context/voices/{slug}.md. Writer reviews and commits. Overlay expresses only the DELTA from global voice — not a full rewrite. Use when a section crosses the 3-post threshold. Trigger keywords: voice overlay, section voice, overlay delta, per-section voice.
---

# Derive Section Voice Overlay

## Workflow

```
When a section reaches ≥3 posts:
- [ ] Step 1: Read all posts in corpus/published/{section}/
- [ ] Step 2: Read global shared-context/voice-profile.md
- [ ] Step 3: Extract patterns present in this section's posts but different from global:
    - Tone shifts (confessional vs technical; register)
    - Structural shifts (scoreboard required; code fences allowed; H2 permitted)
    - Vocabulary shifts (term-of-art allowed; jargon defined on first use)
    - Register permissions (epistolary, second-person, etc.)
- [ ] Step 4: Draft the overlay as a delta (bullet list per category; NOT a full voice profile)
- [ ] Step 5: Write shared-context/voices/{slug}.md for writer review
- [ ] Step 6: Emit draft status: "awaits writer commit" in the Curator review artifact
```

## Overlay schema

```yaml
---
name: voice-overlay-{slug}
section: {slug}
type: voice-overlay
purpose: Voice deltas for {section name} against global voice-profile.
based_on: voice-profile.md (global)
maintained_by: curator (seed) + writer (refinements)
last_updated: YYYY-MM-DD
---

# {Section name} — Voice Overlay

Apply these on top of the global voice-profile. Where rules conflict, this overlay wins for posts in section `{slug}`.

## Tone shifts
- {delta bullet}

## Structural shifts
- {delta bullet}

## Vocabulary shifts
- {delta bullet}

## Register permissions
- {delta bullet}

## Carryovers (emphasized for this section)
- {global rule that matters even more here}

## Things this section does NOT do (anti-overlay)
- {negative rule — what the section explicitly does not do that the global voice might allow}

## Changelog
- YYYY-MM-DD — Initial overlay derived from N posts.
```

## Worked example

**Section**: Kalshi Log (6 posts).

**Detected patterns vs global**:
- Every post has scoreboard at close (absent from global voice).
- Register leans confessional-operational; the "what actually happened" body, not speculative essay.
- Epistolary second-person register appears in 1 of 6 posts — color, not default.
- No post ends on a universal maxim; all close with forward-looking "next match" or "let's find out."

**Overlay draft**:
```yaml
## Tone shifts
- Register leans confessional-operational, not speculative-essay.
- Closer points forward, not upward (universal maxim rare).

## Structural shifts
- Scoreboard block required at the close of every post.
- More numbers per paragraph than global voice allows.
- Short-form is default (≤1500 words).

## Register permissions
- Epistolary second-person register permitted (as in *The Letter*). Color, not default.

## Anti-overlay
- No generalizing to other sports / markets without explicit scope.
- No "lessons for life" closes.
```

## Guardrails

1. Overlay is a delta, not a full voice rewrite. Keep short.
2. Requires ≥3 published posts in the section. Below that, section uses global voice.
3. Writer reviews and commits. Don't write final overlay without writer confirmation in the Curator review artifact.
4. Flag candidate overlay rules that contradict global — those need the writer's explicit promotion.
5. Voice overlays are refined over time — first draft is a starting point, not a finished system.

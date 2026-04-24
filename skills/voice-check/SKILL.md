---
name: voice-check
description: Scans a substacker draft line-by-line against the canonical voice-profile.md don't-list and signature moves. Emits phrase-level flags with location, quoted phrase, violation type, voice-profile citation, and up-to-2 suggested rewrites per flag. Use as pass-2 skill (voice) after structural-review completes, when a draft reads competent but not in the writer's voice, or when the writer asks "does this sound like me?" Trigger keywords: voice check, delve, unpack, paradigm shift, sounds AI, does this sound like me, voice violation.
---

# Voice Check

## Table of Contents

- [Workflow](#workflow)
- [Don't-list regex bank](#dont-list-regex-bank)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by the Editor after `structural-review`. Runs alongside `hedge-detector`, `slop-detector`, `citation-form-check`. Each skill owns a specific band of voice issues; this one handles explicit don't-list phrase matches.

## Workflow

```
Voice check draft D:
- [ ] Step 1: Load voice-profile.md (global) + voices/{section}.md (if applicable)
- [ ] Step 2: Extract the don't-list as a regex bank
- [ ] Step 3: Scan draft; match each regex with word boundaries
- [ ] Step 4: For each match: record {line, quoted phrase, violation, voice-profile citation, 2 rewrite options}
- [ ] Step 5: Emit phrase-flags table
```

## Don't-list regex bank

From `voice-profile.md` §10 (Voice don'ts). Word-boundary enforced.

| Violation | Regex | Rewrite hint |
|---|---|---|
| `delve` | `\bdelve(s|d|ing)?\b` | replace with specific verb |
| `unpack` | `\bunpack(s|ed|ing)?\b` | replace with specific verb |
| `dive into` | `\bdive\s+into\b` | replace with specific verb |
| `let's explore` | `\blet'?s\s+(explore|dive)` | delete; open with confession |
| `at the end of the day` | `\bat\s+the\s+end\s+of\s+the\s+day\b` | delete clause |
| `game-changer` | `\bgame[-\s]?changer\b` | name the specific change |
| `paradigm shift` | `\bparadigm\s+shift\b` | name the shift explicitly |
| `under the hood` | `\bunder\s+the\s+hood\b` | replace with "mechanically" or delete |
| `in today's fast-paced world` | `in\s+today'?s\s+(fast[-\s]?paced\s+)?world` | delete; open with a dated concrete fact |
| `AI is transforming` | `(?i)AI\s+is\s+transforming` | delete generic framing; open with confession |
| emoji | `[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]` | delete |
| exclamation | `!` (in body, not quotes) | convert to period |
| `I think` (as hedge) | `\bI\s+think\b` (when followed by a claim, not a question) | commit OR specific hedge |
| `clearly` / `obviously` / `simply` (as persuasion) | `\b(clearly|obviously|simply)\b` | delete or name the step |
| custom CTA | `subscribe\b.*(resonated|more|stay\s+tuned)` | delete; Substack boilerplate is fine |

Section overlays can add or override entries. If `voices/kalshi-log.md` bans "generalizing to other sports", add that rule.

## Worked example

**Draft excerpt**:
> In today's rapidly evolving AI landscape, let's unpack why RAG beats fine-tuning. At the end of the day, RAG is a game-changer. Let's dive into the details!

**Flags (all tier-1)**:

| loc | quote | violation | citation | rewrites |
|---|---|---|---|---|
| P1 S1 | "In today's rapidly evolving AI landscape" | generic opener | voice-profile §10 don't #2 | (a) delete; (b) replace with a dated concrete fact |
| P1 S1 | "let's unpack" | don't-list | §10 don't #1 | (a) "Here is the mechanism" (b) delete |
| P1 S2 | "At the end of the day" | don't-list | §10 don't #1 | (a) delete clause |
| P1 S2 | "game-changer" | don't-list | §10 don't #1 | (a) "it cuts token budget by 40% on our traces" (b) "it avoids a retrain" |
| P1 S3 | "Let's dive into" | don't-list | §10 don't #1 | (a) "Here is what actually happens" (b) delete |
| P1 S3 | "!" (exclamation) | don't-list | §10 don't #8 | (a) period |

Six tier-1 flags in three sentences → triggers Editor must-not #13 (≥3 tier-1 voice violations = no-go).

## Guardrails

1. Every flag must cite a voice-profile line. No flag without citation.
2. Regex must have word boundaries; avoid false positives (e.g., "undelete" shouldn't match `delve`).
3. Section overlays extend but never override global don'ts — an overlay cannot *allow* a global don't.
4. Exclamation-point rule excludes quoted dialogue and code fences.
5. "I think" is flagged only when followed by a claim. "I think so, but I'm not sure" is a sentence of quiet agreement, not a hedge on a claim.
6. Max 2 rewrite options per flag.

## Quick reference

- Input: draft + voice-profile + optional overlay.
- Output: phrase-flags table in the voice pass.
- Complements `hedge-detector` (hedging) and `slop-detector` (structural voice).

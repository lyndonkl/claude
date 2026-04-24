---
name: hook-generator
description: Generates 3-5 candidate first-line hooks for a specific platform (Substack Note, X, LinkedIn, cross-post) from a given spine. Uses platform-appropriate hook patterns (confession / claim / question / reframe) and voice-profile constraints. Runs before each platform rewrite so the rewrite skill picks the strongest hook rather than reusing the essay's opener verbatim on every platform. Trigger keywords: hook, opening line, platform hook, first tweet, LinkedIn hook, Substack Note hook.
---

# Hook Generator

## Workflow

```
Generate hooks for platform P from spine S:
- [ ] Step 1: Pull best_hook_candidates + thesis + opening claim from spine
- [ ] Step 2: Apply platform hook rules (see below)
- [ ] Step 3: Generate 3-5 candidates
- [ ] Step 4: Score each: attention (1-5), voice-fidelity (1-5), truth-fidelity (1-5)
- [ ] Step 5: Drop any hook scoring <4 on voice-fidelity
- [ ] Step 6: Return sorted list
```

## Platform hook rules

| Platform | Length cap | Pattern | Notes |
|---|---|---|---|
| Substack Note | 1–2 sentences | confession preferred | Can use em-dash reframe; closest to essay opener |
| X (hook tweet) | ≤240 chars | confession or bold claim | No question unless genuine; no "here's what I learned" |
| LinkedIn | ≤210 chars total (first 1–2 lines) | practitioner confession | "I spent four months…" > "I had a realization…" |
| Cross-post | N/A | third-person positioning | "In this piece, Kushal argues…" |

## Worked example

**Platform: X. Spine from *The Execution Gap*.**

**Candidates**:

1. **Confession (attention 5, voice 5, truth 5)**: "I have been meaning to open a Kalshi account for months. Not casually — the way you mean to clean the garage."
2. **Reframe (attention 4, voice 5, truth 5)**: "This isn't a story about prediction markets. It's a story about the distance between learning about something and actually doing it."
3. **Bold claim (attention 4, voice 4, truth 5)**: "Most 'learning' about a domain is substitution for doing the thing."
4. **Question (attention 3, voice 3, truth 5)** — DROPPED: "Why do so many of us substitute learning for doing?" — too generic for the writer's voice.

**Return 3 candidates** (dropped the one below voice-fidelity 4).

## Guardrails

1. Never generate a hook that promises something the essay doesn't deliver.
2. Never use "AI is transforming…" / "In today's fast-paced…" / "Let's explore…" in any hook.
3. Don't start with a stat unless the stat is in the essay.
4. Don't propose a hook whose voice-fidelity score is <4 — drop it, don't include.
5. Per platform, stay within the length cap — a 300-char X hook that would fit in two tweets is not a hook, it's a thread.
6. Cross-post hook uses third person; never "I" in that variant.

---
name: x-thread-rewrite
description: Rewrites a published substacker essay as three X thread variants (short 3-5 tweets, medium 6-8, long 9-12). Each tweet ≤280 chars. Hook tweet works standalone. No numbering by default (2026 convention for tech-first-principles accounts). Final tweet is the link. If essay doesn't translate to X, emits a VERDICT line and halts rather than producing weak variants. Trigger keywords: X thread, Twitter thread, thread, tweet, threaded post, thread variants.
---

# X Thread Rewrite

## Workflow

```
Rewrite for X:
- [ ] Step 1: Load spine + chosen hook + voice-profile
- [ ] Step 2: Score translatability: if >60% of claims score ≤2, emit VERDICT: skip X, halt
- [ ] Step 3: For each of 3 variants (short 3-5, medium 6-8, long 9-12):
    - Pick spine claims by translatability (short = only 5s; medium = 4s and 5s; long = full spine)
    - Write each tweet ≤280 chars, one claim per tweet
    - Preserve paper attributions verbatim
    - End with link tweet: `Full essay: {substack-url}`
- [ ] Step 4: No hashtags, no emoji, no numbering
- [ ] Step 5: Voice-check pass
```

## Output format

`ops/distribution/{date}-{slug}/x-thread.md`:

```markdown
---
source_post: {slug}.md
platform: x
variants: [short, medium, long]
numbering: off
section: {section-slug}
---

### VARIANT: short

Tweet 1 (hook) [{N chars}]:
{text}

Tweet 2 [{N chars}]:
{text}

...

Link tweet [{N chars}]:
Full essay: {substack-url}

---

### VARIANT: medium
...

---

### VARIANT: long
...
```

## Worked example

See the Distribution Translator agent's example B in the spec archive. Each tweet has character count in brackets. No 1/n, no emoji, link only in final tweet.

## Guardrails

1. Hard cap: 12 tweets per variant. Attention cliff beyond that.
2. ≤280 characters per tweet. Include character count in brackets for writer's audit.
3. One claim per tweet. A tweet with two claims fails the "each stands alone" test.
4. Keep paper attributions intact. If `Chen et al., Google, 2024` won't fit with the claim, drop the tweet — never collapse the attribution.
5. Link ONLY in the final tweet. Links mid-thread get algorithmic depression post-March-2026.
6. If essay can't translate (>60% low translatability, or hook can't fit in 280 chars), emit `## VERDICT: this essay doesn't translate to X. Skip X for this post.` and halt. Do not produce weak variants.
7. No hashtags, no emoji, no numbering (1/n is dated for tech-first-principles accounts).
8. Hedges from essay preserved verbatim. No sharpening.

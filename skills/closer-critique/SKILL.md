---
name: closer-critique
description: Evaluates the final paragraph of a substacker draft for compression and closing form — bolded maxim, forward-looking question, or compressed mechanism statement. For series posts (frontmatter series: {slug}), verifies the running scoreboard (P&L, Brier, W-L) is present and updated. Use on every draft. Blocks publication of series posts missing the scoreboard. Trigger keywords: closer, closing, last paragraph, bolded maxim, scoreboard, CTA, wrap up, conclusion.
---

# Closer Critique

## Table of Contents

- [Closing archetypes](#closing-archetypes)
- [Scoreboard check (series posts)](#scoreboard-check-series-posts)
- [Workflow](#workflow)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by Editor in the structural pass. For series posts, enforces scoreboard non-negotiability (ties to `style-guide.md`'s scoreboard template and each section-profile's operational rules).

## Closing archetypes

| Archetype | Example | Verdict |
|---|---|---|
| **Bolded maxim** | **"You don't have an AI problem. You have an eval problem."** | PASS |
| **Forward-looking question / statement** | "Game 6 is tomorrow. The scoreboard will move." | PASS |
| **Compressed mechanism** | "The AI is not the bottleneck. The context you architect around it is." | PASS |
| **Gratitude beat** | "I'm grateful for it." (after a reader-correction post) | PASS |
| **Scoreboard + restrained disclaimer** | Running-tally block + one-paragraph financial disclaimer | PASS (and REQUIRED for series) |
| **"In summary…" or "To conclude…"** | prompt residue | **FLAG tier-2** |
| **Custom CTA** | "If this resonated, subscribe!" | **FLAG tier-1** |
| **No close / dangling** | Post ends mid-thought | **FLAG tier-1** |

## Scoreboard check (series posts)

If draft frontmatter has `series: {slug}`, the closer MUST include a scoreboard block per `style-guide.md`:

```
Running tally: P&L $NNN.NN, Brier 0.NN, W-L N-N
This week: +$N.NN or -$N.NN on {bet}.
```

Placed above the bolded maxim (if one exists).

**Missing scoreboard = automatic tier-1 blocker.** No-go on series posts until fixed.

## Workflow

```
Evaluate closer:
- [ ] Step 1: Extract last paragraph (and bolded maxim if separate)
- [ ] Step 2: Classify archetype
- [ ] Step 3: If series, check scoreboard presence + format
- [ ] Step 4: Emit verdict + flags
```

## Worked example

**Series post closer (Kalshi Log)** — missing scoreboard:
> This concludes my Fed-meeting experiment. Thanks for reading.
>
> **The decision is not the news. The explanation is.**

**Flags**:
1. (Tier-1) Scoreboard missing. Series is `kalshi-log`. Prior post ended with P&L +$127, Brier 0.18, W-L 4-3. This post must update.
2. (Tier-2) "Thanks for reading" — CTA residue. Cut.

**Rewrite** (scoreboard insertion above the maxim):
```
Running tally: P&L $134.50, Brier 0.19, W-L 5-3
This week: +$7.50 on the Fed decision not moving.

**The decision is not the news. The explanation is.**
```

**Non-series post closer** (good):
> After training for two weeks, the model held. I do not know whether it would hold on a different dataset.
>
> **The context you architect around it is.**

**Classification**: compressed mechanism + bolded maxim. PASS.

## Guardrails

1. Series posts without scoreboard = automatic tier-1. Non-negotiable.
2. Scoreboard format follows `style-guide.md` exactly. Deviations (missing W-L, missing Brier) are tier-1.
3. Custom CTA ("subscribe if this resonated!") = tier-1. Substack's platform boilerplate is fine.
4. Dangling close ("... and that's what I think about attention") = tier-1.
5. Don't flag bolded maxims that are a full paragraph of prose — bolded-for-emphasis within a paragraph is different from a one-sentence maxim close. Accept both forms.
6. The closer can be a scoreboard-only (no maxim) on series posts — acceptable if the scoreboard IS the close.

## Quick reference

- Input: last paragraph + draft frontmatter.
- Output: classification + verdict + scoreboard-check result for series posts.
- Blocks: series posts without scoreboard, custom CTAs, dangling closes.

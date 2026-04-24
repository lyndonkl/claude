---
name: paragraph-rhythm-check
description: Checks paragraph rhythm in a substacker draft — long/short mix, one-sentence paragraph at pivots, no walls, avoid monotony. Flags drafts where >3 consecutive paragraphs share the same length bucket, where the pivot lacks a one-sentence paragraph, or where any paragraph exceeds 120 words. Use in the Editor's structural pass. Trigger keywords: rhythm, paragraph length, wall of text, one-sentence paragraph, pivot, monotone.
---

# Paragraph Rhythm Check

## Table of Contents

- [Length buckets](#length-buckets)
- [Rules](#rules)
- [Workflow](#workflow)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by Editor in structural pass. Writes to "Paragraph logic" subsection.

## Length buckets

| Bucket | Word count |
|---|---|
| short | ≤25 |
| medium | 26–80 |
| long | 81–150 |
| wall | >150 |

The writer's voice signature is **long + short mix** with **one-sentence paragraphs at pivots**. Monotone = voice violation.

## Rules

1. **Wall rule**: No paragraph >120 words (wall threshold is slightly below 150 for flagging; >150 is a hard flag). Tier-2.
2. **Monotone rule**: >3 consecutive paragraphs in the same bucket = tier-2 flag.
3. **Pivot rule**: Essays >1500 words should have at least one one-sentence paragraph at a pivot. Absence = tier-2 flag.
4. **Opening short rule**: the opener paragraph is typically short (≤60 words) for punch. A 150-word opening block is a flag.

## Workflow

```
Rhythm check draft D:
- [ ] Step 1: Compute word count per paragraph
- [ ] Step 2: Assign bucket
- [ ] Step 3: Detect monotone runs (≥4 consecutive same bucket)
- [ ] Step 4: Detect walls (>120 words)
- [ ] Step 5: Detect missing pivot in essays >1500 words
- [ ] Step 6: Flag + suggest (split wall / insert pivot / tighten opener)
```

## Worked example

**Draft paragraphs (word counts)**: [62, 58, 71, 63, 68, 72, 180, 45]

**Detections**:
- Monotone: [62, 58, 71, 63, 68, 72] = 6 consecutive medium. Tier-2 flag.
- Wall: paragraph 7 at 180 words. Tier-2 flag.
- Pivot: no single-sentence paragraph in the draft. If total >1500 words → tier-2 flag.

**Suggestions**:
- Insert a one-sentence paragraph at ~paragraph 3 or 4 to mark the pivot.
- Split the 180-word paragraph at the natural semantic break (likely a contrast or a named example).
- Optionally cut one of the middle paragraphs to a single declarative sentence.

## Guardrails

1. Word counts exclude blank lines and code fences.
2. Bullet lists count as their own paragraph unit; don't flag list-adjacent rhythm separately.
3. Series-log posts are often shorter and tighter — relax the pivot rule below 1000 words.
4. If the draft uses `* * *` section breaks, count rhythm within each section separately.
5. Don't propose specific rewrites for rhythm issues — surface the issue; let the writer decide.
6. A 150-word paragraph is a wall only if it lacks internal variation (e.g., long-sentence-after-long-sentence); a 150-word paragraph with internal short sentences is less of a wall.

## Quick reference

- Buckets: short (≤25), medium (26–80), long (81–150), wall (>150).
- Hard flags: wall >120, monotone ≥4 consecutive, missing pivot in essays >1500 words.
- Output: paragraph-logic subsection of structural pass.

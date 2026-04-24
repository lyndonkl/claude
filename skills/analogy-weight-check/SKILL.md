---
name: analogy-weight-check
description: For every analogy in a substacker draft, verifies it carries mechanical weight — the analogy does real work explaining the mechanism, not merely decorates it. Cross-references analogy-catalog.md for novelty (is this analogy reused from a prior post?) and domain fit (biology > organizational > sports preferred; physics/military disfavored). Use whenever an analogy appears in the draft. Trigger keywords: analogy weight, decorative, mechanical weight, reused analogy, catalog check, metaphor check.
---

# Analogy Weight Check

## Table of Contents

- [Mechanical-weight test](#mechanical-weight-test)
- [Workflow](#workflow)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by Editor in structural pass (since analogy decisions affect paragraph structure). Reads `shared-context/analogy-catalog.md` for novelty.

## Mechanical-weight test

The test: **if you remove the analogy, does the explanation still work?**

- **Still works** → analogy is decorative. Either cut or extend so it carries weight.
- **Degrades** → analogy carries weight. Keep.

A decorative analogy is not a tier-1 issue by itself — writers may legitimately use decorative language occasionally. But:

- **If the draft has >2 decorative analogies**, flag as a pattern. Cluster of decorative = slop signal.
- **If the analogy is physics/military** AND decorative, flag tier-2 (physics/military are already disfavored directions).

## Workflow

```
For each analogy in the draft:
- [ ] Step 1: Identify the analogy (source + target)
- [ ] Step 2: Mechanical-weight test — simulate removing it; does the explanation degrade?
- [ ] Step 3: Check analogy-catalog.md for reuse
- [ ] Step 4: Check source domain against voice-profile priority (biology > organizational > sports; not physics/military)
- [ ] Step 5: Emit verdict per analogy: carries-weight | decorative | reused-from-catalog | wrong-domain
```

## Worked example

**Draft excerpt**:
> A KV cache is like a library's card catalog — it lets you find things. Under the hood, it stores key and value projections for each past token, so when a new token arrives, attention can index back without recomputing.
>
> Attention is also like a room full of people trying to hear each other.

**Analogies**:

1. **"KV cache like a library card catalog"**
   - Remove test: "A KV cache stores key and value projections for each past token, so when a new token arrives, attention can index back without recomputing." Still works and is arguably clearer.
   - Verdict: **decorative**. Catalog check: not in analogy-catalog. Domain: neutral (everyday).
   - Suggestion: either cut the simile, OR extend to carry weight ("like a card catalog with a fixed drawer count — evicting old cards to make room for new ones").

2. **"Attention is also like a room full of people trying to hear each other"**
   - Remove test: what remains? "Attention is also…" — the sentence collapses; no mechanism.
   - Verdict: **decorative** AND un-mapped (no component-to-component mapping in the draft).
   - Suggestion: cut entirely or replace with a framing that carries weight.

**Overall**: 2 decorative analogies in one excerpt. Cluster signal — flag as tier-2, note pattern.

## Guardrails

1. Don't flag an analogy as decorative if the draft immediately extends it (next sentence provides the mapping). Look at the surrounding 2-3 sentences.
2. An analogy the writer has just generated via Intuition Builder is pre-mapped; treat as carrying weight unless the draft drops the mapping.
3. Reused analogies from the catalog are not failures; they're a feature of recurring analogies the writer owns (e.g., "from first principles" is a recurring frame). Flag softly.
4. Physics/military analogies get an extra demerit but are not automatic tier-1 — writer may use them with explicit irony or override.
5. Suggested rewrites should be ≤2 sentences each. Don't propose a full paragraph.
6. A decorative analogy in isolation is tier-2. Three+ decorative analogies in a single draft = pattern flag, still tier-2 but surfaced in summary.

## Quick reference

- Per-analogy verdict: carries-weight | decorative | reused-from-catalog | wrong-domain.
- Cluster rule: >2 decorative = pattern flag.
- Reads analogy-catalog.md; does not write (that's `update-analogy-catalog`).

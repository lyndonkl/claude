---
name: voice-fitness-check
description: Ranks a proposed set of framings against the writer's voice profile, especially the analogy-direction priority — biology > organizational > sports, with physics/military as voice violations. Produces a tier rating per framing and flags any framing that would break voice. Use in the Intuition Builder pipeline after generating framings, to order them by fit with the writer's register. Trigger keywords: voice fit, analogy direction, biology to AI, organizational to multi-agent, sports to calibration.
---

# Voice Fitness Check

## Table of Contents

- [Analogy direction priority](#analogy-direction-priority)
- [Workflow](#workflow)
- [Tier ratings](#tier-ratings)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by the Intuition Builder in the pipeline (step 5). Reads `shared-context/voice-profile.md` and `shared-context/voices/{section}.md` if a target section is specified.

## Analogy direction priority

From `voice-profile.md` section 9:

1. **Biology → AI architecture and emergence** (immune system, thymus, crypts, DNA/protein, ant colony) — Tier 1.
2. **Organizational / institutional → multi-agent systems** (departments, courtroom, bucket brigade) — Tier 2.
3. **Sports → calibration / prediction / betting** (cricket phases, soccer-as-practice, scoreboard) — Tier 3.

Everything else is Tier 4 (acceptable but not a voice signature).

**Physics, military, warfare, weapons, combat** — these are voice violations. Flag strongly. Propose a replacement in Tier 1–3 direction if one is available.

## Workflow

```
For each of the 5 framings:
- [ ] Step 1: Classify the source domain
- [ ] Step 2: Assign a tier (1-4) based on the priority table
- [ ] Step 3: Flag any Tier 4 or voice-violating framings
- [ ] Step 4: Rank the 5 framings overall (tier + craft quality)
- [ ] Step 5: Recommend first choice
```

### Step 1: Domain classification

Look at the source. Is it:
- A living system, cellular process, evolution, immunology? → biology (Tier 1)
- A human organization, hierarchy, committee, courtroom, workflow? → organizational (Tier 2)
- A sport, game, match, contest, calibration of a prediction? → sports (Tier 3)
- A machine, mechanical system, fluid, physical law, vehicle? → physics (Tier 4)
- A battle, weapon, combat, tactic, strategy (in the military sense)? → voice violation

"Neural network" itself counts as biology — but only if the framing actually uses biological relations (neurons firing, learning as development), not just the name.

## Tier ratings

- **Tier 1** (biology): preferred, voice signature. Use often.
- **Tier 2** (organizational): preferred, voice signature. Use when biology doesn't fit.
- **Tier 3** (sports): acceptable for calibration/prediction content specifically. Out of register for pure ML architecture.
- **Tier 4** (other): usable if no Tier 1-3 candidate fits, but not a voice signature.
- **Violation** (physics/military): flag. Do not include without explicit writer override.

## Worked example

**Topic**: Multi-agent AI system.

**5 framings** (from generate-analogy-set):
1. Everyday: "A potluck dinner where each guest brings one dish" — Tier 4 (household).
2. Physical metaphor: "Distributed load across power-grid nodes" — Tier 4 (physics; voice-adjacent violation).
3. Contrarian: "Not a single super-agent; a parliament of specialized agents" — Tier 2 (organizational).
4. Historical: "The Sumerian scribe running grain accounting — system intelligence exceeding any individual" — Tier 2 (borrowed, attributed).
5. Counterfactual: "Remove inter-agent communication; you're back to single-agent with longer prompts" — neutral (structural, not an analogy in the usual sense).

**Ranking**:
1. Contrarian (parliament) — Tier 2, strong fit with writer's voice signature for multi-agent.
2. Historical (Sumerian scribe) — Tier 2, attributed borrow, strong.
3. Counterfactual — neutral; always welcome.
4. Everyday (potluck) — Tier 4, usable but not voice-native.
5. Physical (power grid) — Tier 4 with voice-adjacent risk. **Suggest replacement**: "An immune system's parallel T-cell response" (Tier 1, biology).

**Recommendation**: First choice is the **parliament** contrarian. Swap framing 5 for the biological alternative.

## Guardrails

1. Tier assignments are not opinions — they come directly from the voice-profile's analogy-direction table.
2. Flag voice violations (physics/military) strongly. Do not merely rank low; call them out.
3. Suggest a replacement for any violation, drawn from Tier 1-3.
4. Ranking combines tier + craft quality. A Tier-2 framing with a weak mapping ranks below a Tier-3 with strong mapping. Use judgement for ties.
5. Counterfactual framings are usually neutral — they're structural, not source-domain-based. Rate on mechanical clarity instead.
6. If the target section has its own voice overlay (`voices/{section}.md`) with different priorities, apply those on top of global.

## Quick reference

- Input: 5 framings + voice-profile.md.
- Output: per-framing tier + overall ranking + flagged violations + replacement suggestions.
- Final step before the Intuition Builder presents to the writer.

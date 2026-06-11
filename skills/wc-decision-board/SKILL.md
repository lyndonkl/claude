---
name: wc-decision-board
description: Renders the FIFA World Cup Fantasy decision board — the advisory output that surfaces 2-4 genuinely distinct, weighted options for the expert manager and ends on "your call." Takes the evolution engine's verified offspring (with fitness decomposition, genotype lineage, and specialist dissent) and formats each as an option with its concrete picks, EV/ownership-leverage/variance/progression decomposition, football reasoning, what it's betting on, the dissent, and an ownership read — then a trade-off axis, a recommended-but-overridable default tied to the rank objective, and a "what I need from you." Enforces options-not-commands, shows the working, surfaces dissent, never auto-commits. Use to present any squad/matchday/transfer/chip decision.
---

# wc-decision-board — render the advisory board

Implements `footballfantasy/context/frameworks/decision-board-format.md`. This is the system's product surface and the structural enforcement of "the agents feed me options, I decide." A board that reads like a command has failed even if its top option is right. The manager is the selection operator; this renders the choice for them.

## Inputs
- The verified offspring (post-engine, post-specialist-verify): each with fitness decomposition, genotype lineage, repair log, and the specialists' dissent/annotations.
- The rank objective θ/k, the round/phase/deadline, mini-league standing, the diversity report.

## Workflow

```
- [ ] 1. Select the 2–4 offspring to show (spanning the variance spectrum — at least one cover, one climb)
- [ ] 2. Render each as an OPTION (picks + decomposition + reasoning + bet + dissent + ownership read)
- [ ] 3. Write the TRADE-OFF axis (what actually separates them)
- [ ] 4. Write the RECOMMENDED DEFAULT (tied to θ, explicitly overridable)
- [ ] 5. Write WHAT I NEED FROM YOU (the inputs that would sharpen/change the board)
- [ ] 6. End on "your call." Write to boards/ and present. Do NOT proceed past this.
```

## The rendered shape

```
═══════════════════════════════════════════════════════════════
[DECISION] — [round id] · [phase] · lock [deadline]
Objective: θ=[protect|gain|neutral] (k=[..]) — [one line why]
Mini-league: [standing] · [rounds left]    Diversity: [wide|close]
═══════════════════════════════════════════════════════════════

CONTEXT
  [2–4 lines: where we stand, what changed (eliminations, fixture swings,
   the field's notable moves), the one tension this decision turns on.]

── OPTION A · "[handle]" ─────────────────────────────────────
  Lineage:  [A1 captain core + A4 clean-sheet stack + A2 differential pod]
  Fitness:  [n]  ·  variance [band]
  Decomp:   xEV [n] · ownership-leverage [+/−n] · progression [n]
  Picks:    [squad/XI/captain/bench/chip — the concrete plan]
  Strength: [2–3 lines, football reasoning the manager can interrogate]
  Betting on: [the key assumption that must hold]
  Dissent:  [the strongest case against — from the critic / specialist verify]
  Ownership: [template-covering | balanced | differential-leaning]

── OPTION B · "[handle]" ── [a genuinely different bet — different variance band] ──
  …

[C, D as warranted; never more than 4]

THE TRADE-OFF
  [1–3 lines naming the axis the manager is choosing on — variance vs floor,
   template vs differential, this-round xEV vs progression carry.]

RECOMMENDED DEFAULT
  "If you do nothing else, [Option X] — because [one line tied to θ].
   If you'd rather [protect/gamble] instead, [Option Y]."

WHAT I NEED FROM YOU
  • [the input(s) that would change the board — standing, appetite, non-negotiables, chip intent]
  Your call — tell me which option (or your own variant) and I'll lock it and update state.
═══════════════════════════════════════════════════════════════
```

## Rules (the contract)
1. **2–4 options, genuinely distinct**, spanning the variance spectrum (≥1 cover-leaning, ≥1 climb-leaning). Collapse near-duplicates.
2. **Always show the decomposition.** Never a bare fitness number — the manager re-weights by their own read.
3. **Football register, expert.** Reasoning the manager can interrogate, not "the model likes it."
4. **Surface the dissent** on every option. A board that only sells hides risk.
5. **Recommend, don't command.** The default is overridable and tied to θ, with the opposite-posture alternative named.
6. **Ask for what would change the board.** The "what I need from you" block is mandatory (or an explicit "no input needed").
7. **End on the manager's move, then stop.** Rendering the board is the last thing this skill does — it does not lock, update state, or proceed.

## Mini-boards
Sub-decisions (switch the armband now or bank the 7? fire the Shield or hold? transfer X or Y?) use the same shape compressed to 2 options + trade-off + default + your-call. Same contract at every scale.

## Guardrails
- If only one offspring survived verification, **do not manufacture filler options** — present the one with its dissent and explicitly say the alternatives were ruled out and why (and offer to widen the search if the manager wants more choice).
- If a load-bearing fact is unconfirmed (predicted XI, a knock), flag the affected option "confirm before lock."
- Write the board to `boards/YYYY-MM-DD-<decision>.md` and return its path; the Director presents and waits.

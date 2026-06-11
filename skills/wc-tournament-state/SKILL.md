---
name: wc-tournament-state
description: Reads and updates the FIFA World Cup Fantasy tournament state machine (footballfantasy/context/tournament-state.md) — the temporal backbone tracking phase (pre-tournament → group MD1-3 → R32 → R16 → QF → SF → final), budget ($100m group / $105m knockouts), nation cap (3 group, loosening in knockouts), chips remaining, surviving nations, each owned player's elimination-risk horizon, and deadlines. Validates state on load (count/feasibility checks), applies phase transitions, and appends to the append-only state log (never silent overwrite). Use to load state at the start of a run and to commit state changes after the manager makes a move.
---

# wc-tournament-state — the temporal state machine

Owns `footballfantasy/context/tournament-state.md`. The World Cup is a month-long state machine and tracking it correctly is a core deliverable — budget rises at the knockouts, the nation cap loosens as teams are eliminated, five chips burn down once each, and every owned player has an elimination horizon that caps his value. This skill is the single writer of that file (everyone else reads it).

## Two modes

### LOAD (start of every run)
1. Read `tournament-state.md`. Parse: current phase, round id, next deadline, budget, squad value, in-the-bank, nation cap, free transfers, chips remaining, surviving nations, owned-player exposure.
2. **Validate:**
   - squad shape: 2 GK / 5 DEF / 5 MID / 3 FWD if a squad exists; else flag "no squad — run build".
   - budget: squad value ≤ budget for the current phase.
   - nation cap: no nation over the current-phase cap.
   - formation feasibility: at least one valid XI exists.
   - chip ledger consistency: matches `tracker/chip-ledger.md`.
3. Return the parsed state + any validation flags to the caller. **Do not proceed a decision on invalid state** — surface the break.

### UPDATE (after a move / phase transition)
1. Apply the change (transfer in/out, chip used, XI/captain set, phase advance).
2. **On a phase transition** run the transition rules:
   - **group → knockout:** budget $100m → $105m; nation cap loosens (set the new cap from the game); recompute every owned player's elimination horizon against the new bracket; flag that a Wildcard rebuild may be due.
   - **each knockout round:** prune eliminated nations from "surviving"; update `p_advance`; re-flag exposure for owned players whose nations are now out (these are forced-transfer candidates).
3. Rewrite only the changed fields.
4. **Append to the State log** (append-only): `YYYY-MM-DD HH:MMZ — phase — what changed — why`. Never overwrite log history — it's how we reconstruct what was true at each decision.
5. Mirror chip changes to `tracker/chip-ledger.md` and squad changes to `context/squad.md`.

## Owned-player exposure (the clock on each asset)

For every owned player, maintain `elimination_risk_round` = the earliest round his nation could be knocked out (from `fixtures/progression-odds.md`). This is the horizon on that asset's value and the transfer-strategist's primary watch list. When a nation is eliminated, immediately flag its players as `dead — transfer out next window` and surface them to the Director.

## Workflow
```
- [ ] LOAD: parse → validate → return state + flags
- [ ] UPDATE: apply change → run transition rules if phase changed → rewrite fields →
              append state-log line → mirror to chip-ledger / squad.md
```

## Guardrails
- **Single writer.** Only this skill writes `tournament-state.md`. Prevents drift.
- **Validate on load; never decide on invalid state.** A budget or nation-cap break must halt the decision and be surfaced, not silently tolerated.
- **Append-only state log.** History is never overwritten.
- **Phase transitions are explicit events** with their own rules (budget, cap, exposure) — never let a phase change slip through as a field edit.
- Confirm the knockout nation-cap numbers against the live game at the transition (the exact loosening schedule is game-defined — `league-config.md`).

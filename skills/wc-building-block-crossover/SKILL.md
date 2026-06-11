---
name: wc-building-block-crossover
description: The recombination operator for the FIFA World Cup Fantasy evolution engine. Crosses elite candidate squads/plans at BUILDING-BLOCK boundaries (Captain Core, Clean-Sheet Spine, Mid-Engine, Differential Pod, Enabler Bench; or for matchday plans the XI/captain-ladder/bench/sub/chip blocks) — harvesting the strongest module from each parent rather than swapping individual players — then runs a feasibility REPAIR operator (budget, nation cap, formation, 15-man shape) that restores legality from the cheapest block first and never guts a value-bearing block. Records block lineage (which parent each block came from). Implements the Evolution document's central lesson that naive crossover destroys good building blocks. Use in the recombine stage after fitness selection.
---

# wc-building-block-crossover — recombine modules, then repair

Implements the recombination step of `evolution-protocol.md` against the module map in `building-blocks.md`. The discipline that defines this skill, straight from the Evolution document: **a squad is not a flat list of independent slots; it is modules with internal linkage, and crossover must operate at module boundaries or it destroys the very things that make the parents good.** "Excellent planning + Excellent memory without rediscovering both independently" — here: the best captain core and the best clean-sheet stack, fused.

## Inputs
- The elite candidate set (from fitness selection), each with its block tags and per-block quality.
- Live constraints from `tournament-state.md`: budget (group $100m / KO $105m), nation cap (3 group, current-phase cap KO), phase.

## Workflow

```
- [ ] 1. For each block slot, rank the elites by that block's quality (per-block fitness contribution)
- [ ] 2. Compose offspring by harvesting the top block from different parents (try a few combinations)
- [ ] 3. REPAIR each offspring to feasibility — cheapest block first, never gut a value block
- [ ] 4. Drop any offspring whose parents' blocks are fundamentally incompatible (repair would break a block)
- [ ] 5. Record block lineage per offspring; emit the feasible offspring
```

## Step 1–2: Cross at block boundaries

For a **squad**, the blocks are BB1 Captain Core, BB2 Clean-Sheet Spine, BB3 Mid-Engine, BB4 Differential Pod, BB5 Enabler Bench (BB6 Fixture/Timing is the constraint layer, enforced in repair). For each block, identify which elite has the best version (highest contribution to fitness for that module — best captain core, best stack, sharpest pod). Compose 2–4 candidate offspring by mixing: e.g.

```
offspring_1 = BB1(A1) + BB2(A4) + BB3(A5) + BB4(A2) + BB5(cheapest-feasible)
offspring_2 = BB1(A6) + BB2(A3) + BB3(A5) + BB4(A4) + BB5(...)
```

Harvest **whole blocks**, not players. Do not pluck one defender out of a stack — the stack's value is its correlation; take it or leave it. For a **matchday plan**, cross MB2 captain-ladder from one parent, MB3 bench-order from another, MB1 XI / MB4 sub-triggers / MB5 chip likewise — keeping each block internally intact.

## Step 3: Repair to feasibility (priority order)

Recombined blocks will usually break BB6 constraints. Repair in this order, **preserving value-bearing blocks**:

1. **Formation.** If no valid XI (1 GK; 3–5 DEF; 2–5 MID; 1–3 FWD) can be fielded from the 15, the recombination is structurally broken → re-pick the offending block from the next-best parent rather than patching individual players.
2. **Nation cap.** If a nation exceeds the cap, swap the **lowest-xEV** offender, preferring to move a BB5 enabler or BB4 differential over a BB1/BB2 value piece.
3. **Budget.** If over budget, release funds from **BB5 first** (downgrade the cheapest enabler), then BB4 (cheaper differential), and only touch BB1/BB2/BB3 if unavoidable — and if so, prefer downgrading one BB1 premium over breaking the BB2 stack (correlation is harder to rebuild than a single captain option).
4. **Matchday spread / dead-minutes bench.** Fix last; it's the cheapest lever.

## Step 4: Drop incompatible offspring

**Repair invariant:** never satisfy a constraint by *destroying* a block. If, say, the only way to afford BB1(A1)'s captain core is to break BB2(A4)'s stack, the two parents are incompatible — **drop that offspring and report it** rather than emit a mangled squad. An incompatible pairing is information (those two genotypes don't fuse this round), not something to force.

## Step 5: Lineage + emit

For each surviving offspring record:
```yaml
offspring_id: <id>
blocks:
  BB1_captain_core:   { from: A1, players: [...] }
  BB2_clean_sheet:    { from: A4, players: [...] }
  BB3_mid_engine:     { from: A5, players: [...] }
  BB4_differential:   { from: A2, players: [...] }
  BB5_enabler_bench:  { from: repair, players: [...] }
repair_log: [ "downgraded enabler X→Y for $1.5m", "swapped nation-clash bench Z" ]
feasible: true
```

Lineage feeds the board ("A1 core + A4 stack + A2 pod") and the archetype scoreboard (which genotypes' blocks keep getting chosen). Hand the offspring to mutation, then diversity.

## Guardrails
- **Whole blocks only.** No individual-player crossover — that's the failure mode this skill exists to prevent.
- **Repair never guts a block.** Cheapest-block-first; drop incompatible offspring rather than mangle.
- **Always emit lineage + repair log.** Unexplained offspring can't be presented or learned from.
- Produce a **variance-diverse** offspring set where the parents allow it (a safe fusion and a brave fusion) — the diversity skill checks this next, but don't pre-collapse it here.

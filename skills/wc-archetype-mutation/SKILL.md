---
name: wc-archetype-mutation
description: The mutation operator for the FIFA World Cup Fantasy evolution engine. Applies small, bounded, feasibility-preserving perturbations to a recombined offspring squad/plan — swap one differential for an adjacent-price alternative, reorder the bench by kickoff, shift one captain-ladder step, try one fixture-swing transfer, nudge one enabler. Mutation rate is low by default and raised on demand by the diversity governor when the population has collapsed. Each mutation stays inside budget/nation/formation feasibility. Use in the mutate stage after recombination, or when wc-population-diversity calls for more exploration.
---

# wc-archetype-mutation — bounded exploration

The mutation operator from the genetic loop (`evolution-protocol.md`). After recombination has fused the best blocks, mutation explores the *neighbourhood* of each offspring — small perturbations that might find a slightly better local arrangement or, when the diversity governor raises the rate, push an offspring away from a collapsed template. It is the explore side of the explore/exploit dial.

## Inputs
- An offspring candidate (post-crossover, feasible) with block tags.
- `mutation_rate` (default **low**, e.g. ~1 perturbation per offspring; raised by `wc-population-diversity` to ~2–3 when collapse is detected).
- Live constraints (budget, nation cap, phase) for the feasibility guard.

## Mutation moves (pick per the rate; each must keep feasibility)

| Move | What it does | When apt |
|---|---|---|
| **Differential swap** | replace one BB4 pick with an adjacent-price, similar-EV alternative of *lower ownership* | exploring the rank axis; diversity-injection toward differential |
| **Enabler nudge** | swap a BB5 enabler for an equal-price guaranteed starter with a marginally better fixture | freeing optionality without touching value blocks |
| **Captain-ladder shift** | reorder one step of MB2 (promote a different day-2 captain candidate) | matchday plans; exploring captaincy variance |
| **Bench reorder** | re-rank MB3 bench by a refined kickoff/likely-points read | improving manual-sub optionality |
| **Fixture-swing transfer** | for a transfer plan, try one alternative in→out pair targeting a steeper fixture delta | exploring A4-style edges |
| **Formation flex** | shift the XI between two valid formations (e.g. 3-4-3 ↔ 3-5-2) the same 15 supports | exploring attack/defence balance |

## Workflow

```
- [ ] 1. Read offspring + mutation_rate + constraints
- [ ] 2. Pick `rate` moves, biased by any diversity-injection target passed in (e.g. "push toward differential")
- [ ] 3. Apply each move; re-check feasibility (budget, nation cap, formation, 15-man shape)
- [ ] 4. Reject any move that breaks feasibility or destroys a building block; retry an alternative move
- [ ] 5. Emit the mutated offspring + a mutation log (what changed, why)
```

## Bounds (mutation is small by design)
- **Never a wholesale rebuild.** That's the Wildcard / a fresh strategist run, not mutation. Mutation touches ~1 (default) to ~3 (raised) elements.
- **Feasibility-preserving.** A mutation that breaks budget/nation/formation is discarded, not repaired (repair is crossover's job; mutation simply tries a different small move).
- **Block-respecting.** Mutation perturbs *within or at the edge of* a block (swap a differential, nudge an enabler) — it does not split a value block (never break the clean-sheet stack as a "mutation").
- **Directed when asked.** If `wc-population-diversity` passes an injection target ("move toward high-variance / differential"), bias move selection that way.

## Output
```yaml
mutated_offspring: <candidate>
mutation_log:
  - move: differential_swap
    change: "BB4: out [player A, 12% owned] → in [player B, 4% owned, similar xEV]"
    rationale: "diversity injection toward differential; raises ceiling variance"
  feasibility_ok: true
```

## Guardrails
- Keep the default rate **low** — over-mutation destroys the gains recombination just made (the document's "too much disruption tears apart useful structure").
- One mutated copy per offspring (don't fan out many mutants unless the diversity governor explicitly asks).
- Always log the change so lineage stays auditable.

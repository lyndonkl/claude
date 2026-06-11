---
name: wc-decision-logger
description: Appends FIFA World Cup Fantasy decisions to tracker/decisions-log.md — logging not just what the manager chose but the full OPTION SET they chose from, which option the board recommended, whether the manager overrode it, and the manager's stated reasoning. Also archives the full generation (population → offspring → board → pick) to generations/, and updates the archetype scoreboard (which genotypes' blocks were chosen/won) and the manager's revealed preferences. Append-only; never overwrites. The override rows are the system's most valuable learning signal. Use after the manager picks an option off a board.
---

# wc-decision-logger — log the choice, the option set, and the why

Implements `footballfantasy/context/frameworks/decision-log-format.md`. The key difference from a normal decision log: here we record a **choice among presented options**, including the recommendation, the override, and the manager's reasoning — because three learning loops feed on exactly that (archetype scoreboard, revealed preferences, specialist calibration). A bare "chose B" teaches nothing.

## Inputs (from the Director, after the manager picks)
- The board (option set with lineage + fitness + variance + dissent), the recommended default.
- The manager's pick, any modification, their stated reasoning, the objective θ/k in force.

## Workflow

```
- [ ] 1. Build the log entry (schema below) — capture the full option set + pick + reasoning + override flag
- [ ] 2. Append atomically to tracker/decisions-log.md (never overwrite)
- [ ] 3. Archive the generation to generations/<round>/ (population, fitnesses, offspring lineage, board, pick)
- [ ] 4. Update tracker/archetype-scoreboard.md (which genotype's blocks were chosen)
- [ ] 5. On override/modification, append a revealed-preference note to manager-profile.md
- [ ] 6. Return the decision_id
```

## Entry schema (per `decision-log-format.md`)
```markdown
### {iso8601} | {decision_type} | round {round_id}
- decision_id: {round_id}-{decision_type}-{NN}
- objective: θ={..}, k={..}
- board_options: [ A "{handle}" — lineage — fitness — variance ; B … ; C … ]
- recommended_default: {option}
- manager_pick: {A | modified A | own plan}
- manager_modification: {what they changed}
- manager_reasoning: {their stated why — verbatim/close; this is gold}
- override?: {yes/no}
- key_assumptions: {what the pick bets on}
- dissent_carried: {strongest case against the pick}
- confidence: {0–1}
- will_verify_on: {round id}
- outcome: {filled by round-review}
- outcome_recorded_on: {filled later}
- what_we_learned: {filled later}
```
`decision_type` ∈ `squad-build | matchday | transfer | captain | chip | ad-hoc`.

## Generation archive (the evolutionary trail)
Write `generations/<round>/<decision_type>.md` capturing the whole search: the population (each archetype's candidate + self-dissent), the fitness table with decompositions, the offspring with lineage + repair logs, the diversity report, the board, and the manager's pick. This is how the search is audited and how memetic learning reconstructs which genotypes produced winning blocks.

## Scoreboard + revealed-preference updates
- **Archetype scoreboard:** increment the count of "blocks chosen" for each genotype whose block appears in the picked candidate. After the round (via round-review) attach the points outcome so the scoreboard reflects which genotypes *win*, not just which get picked.
- **Revealed preferences:** when the manager overrides or modifies, append a one-line note to `manager-profile.md` describing the tilt (e.g. "took the differential captain but refused the second punt → will gamble the armband, not the whole squad"). These become soft fitness terms.

## Guardrails
- **Append-only.** Never overwrite a prior entry. Outcomes are filled in later by round-review, in place.
- **Log the option set and the reasoning, always** — not just the pick. The override rows are the highest-value training signal; capture the manager's words.
- **One entry per decision**; one generation archive per decision. Keep `decision_id`s unique and chronological.

---
name: wc-fitness-eval
description: Scores a FIFA World Cup Fantasy candidate squad/plan as risk-adjusted, rank-relative fitness under a stated rank objective (protect / gain / neutral). Sums fixture-scaled player xEV + captaincy uplift, adds clean-sheet correlation and progression-carry, applies an ownership-leverage term (cover chalk when protecting, fade it when gaining), and a variance term whose SIGN flips with the objective (penalty when protecting, reward when chasing) — the selection-pressure dial. Returns one fitness number plus the full decomposition. Use to score the population in the evolution engine, or to evaluate any single squad/plan. The objective makes the same candidate score differently for a leader vs a chaser; never returns raw expected points.
---

# wc-fitness-eval — risk-adjusted, rank-relative fitness

Implements `footballfantasy/context/frameworks/fitness-function.md`. The whole evolution engine selects on this number, so it must encode the two things that make fantasy fitness *not* raw points: **rank is relative** (ownership matters) and **the rank objective sets the variance target** (the selection-pressure dial).

## The formula

```
fitness(c | θ) =   raw_xEV(c)                    # Σ player xEV (fixture-scaled) + captaincy uplift
                 + cs_corr_bonus(c)              # within-team clean-sheet correlation (BB2 stacks)
                 + progression_carry(c, horizon) # discounted future-round value of deep-team players
                 + ownership_leverage(c | θ)     # rank term — sign/shape set by θ
                 − variance_term(c | θ)          # selection pressure — sign flips with θ
                 − feasibility_penalty(c)        # 0 after clean repair; disqualifying if infeasible
```

## Workflow

```
- [ ] 1. Read inputs: candidate (with block tags), round signals (player-ev, clean-sheet, fixture, ownership), θ and k
- [ ] 2. raw_xEV: sum per-player xEV (from wc-player-ev signals); add captaincy uplift (from wc-captain-ladder)
- [ ] 3. cs_corr_bonus: from wc-clean-sheet-model for each defensive stack
- [ ] 4. progression_carry: Σ player_xEV_future × P(team advances)^rounds, discounted; weight up in KO phases
- [ ] 5. ownership_leverage: apply θ (cover high-EO when protect; overweight low-EO ceilings when gain)
- [ ] 6. variance_term: estimate candidate variance; multiply by ±k per θ
- [ ] 7. feasibility_penalty: 0 if repair-clean; large if not
- [ ] 8. Sum → fitness; emit fitness + the full decomposition
```

## Step detail

**raw_xEV** — sum the `xEV` field from each player's `player-ev` signal (already fixture-scaled, minutes-weighted, with the 60' tier and card/concede downside). Captaincy uplift = the expected *extra* from the captain ladder (from `wc-captain-ladder`), i.e. `E[best ladder-reachable captain outcome]`, not a naive 2× of the top player. For a squad-build (no fixed matchday yet), use the round-1 captaincy estimate.

**cs_corr_bonus** — for each Clean-Sheet Spine stack (BB2), `wc-clean-sheet-model` returns the joint-distribution bonus capturing that a 3-defender + GK stack hauls *together*. Sign by θ: amplify the correlated-haul upside when `gain`; lightly discount when `protect` (they also blank together).

**progression_carry** — `Σ_player xEV_typical(player) × Σ_{r=next..horizon} P(team alive at r) × discount^r`. A steady player on a likely semi-finalist accrues several future rounds; a coin-flip nation's player accrues little. Weight ≈0 in the final, high in early knockouts (this is what makes A3 Progression Theorist competitive on fitness). Advance probabilities from `wc-fixture-progression`.

**ownership_leverage(c | θ)** — using effective ownership EO from `wc-ownership-meta`:
- `θ=protect`: `− w · Σ_{high-EO players NOT owned} EO_haul_risk` → rewards covering chalk (penalise gaps in the template).
- `θ=gain`: `+ w · Σ_{owned, low-EO, live-ceiling} (ceiling × (1−EO))` → rewards differentiation.
- `θ=neutral`: small symmetric term; mostly defer to raw_xEV.

**variance_term(c | θ)** — candidate variance from the spread of its players' point distributions + captaincy variance + stack correlation:
| θ | term |
|---|---|
| protect | `+ k · variance` (penalty) — damp swings, bank the lead |
| gain | `− k · variance` written as a *reward* (subtract a negative) — you need the swing |
| neutral | small penalty |
`k` scales with how extreme the standing is (big lead + few rounds → high k_protect; big deficit + few rounds → high k_gain).

**feasibility_penalty** — 0 if the candidate passed repair (budget, nation cap, formation, 15-man shape). Large/disqualifying otherwise (keeps infeasible candidates out of the elite set; their blocks can still be harvested in crossover before they drop).

**Revealed-preference soft terms** — add the small bonuses/penalties accrued in `manager-profile.md` (e.g. "+ minutes-secure mids", "− benching the favourite nation"). Soft: they tilt, never dominate.

## Output (the decomposition — always return it)

```yaml
fitness: <number>
decomposition:
  raw_xEV: <n>
  captaincy_uplift: <n>
  cs_corr_bonus: <n>
  progression_carry: <n>
  ownership_leverage: <+/- n>     # under θ
  variance: <n>   variance_term: <+/- n>   # under θ, with k
  feasibility_penalty: <n>
objective: { theta: protect|gain|neutral, k: <n> }
variance_band: low|medium|high
```

The decomposition is mandatory — the board explains options through it, and the engine needs `variance_band` to mandate spectrum coverage in selection.

## Goodhart / substitution guard (`system-dynamics.md` §4, `invariants.md` §6)

Fitness is **multi-term by design, and that is non-negotiable** — the systems-thinking digest's cautionary tale (held *"close before writing any agent-fitness metric"*): every "maximise X" rule produces a substitution effect at a node the rule did not name. Collapsing fitness to one dominant term is forbidden; if you ever find one term swamping the rest (one weight set so high the others are noise), that is the Goodhart failure in progress — re-balance.

Emit, alongside the decomposition, a one-line **substitution-watch** per candidate when one term is doing most of the work: name *what the candidate gave up to score there.* Examples:
- captaincy_uplift dominates → "ceiling-led; check the bench/minutes floor it traded away."
- ownership_leverage dominates → "differential-led; check how many nailed starts it sacrificed."
- raw_xEV (this round) dominates → "this-round-led; check the progression_carry it ignored."

The thing that quietly degraded is usually the node the objective didn't name. Surfacing it on the artifact lets `round-review` run the substitution-watch across rounds before it compounds.

## Guardrails
- **Never return raw points as fitness.** If θ isn't supplied, ask for it; do not default silently to neutral on a high-stakes round.
- **Never collapse to a single metric.** Multi-term always (Goodhart). The decomposition ships every time.
- **The same candidate must score differently under protect vs gain** — if it doesn't, the variance term is mis-wired.
- Confirm the point values in `scoring-rules.md` are `confirmed: true` before trusting absolute magnitudes; otherwise flag every fitness as provisional.

---
name: wc-population-diversity
description: Measures and protects diversity in the FIFA World Cup Fantasy evolution engine — the anti-inbreeding / selection-pressure governor from the Evolution document. Computes how collapsed an offspring set is (pairwise squad overlap %, captain overlap, ownership-profile spread, variance-band coverage); if the population has converged toward one template (premature convergence / local optimum), it injects an under-represented genotype's blocks and/or raises the mutation rate and signals a re-run; and it tunes selection pressure (too high collapses the gene pool, too low makes the board noise). Ensures the manager's board always offers a real choice across the variance spectrum. Use after recombination + mutation, before emitting offspring.
---

# wc-population-diversity — anti-inbreeding & selection-pressure governor

Implements the diversity-maintenance and selection-pressure ideas the Evolution document is explicit about: "plant breeders care about preserving genetic diversity; agent researchers care about maintaining behavioural diversity — same problem," and "selection pressure too high → population collapses; too low → progress is slow," and "repeatedly refining the same strategy leads to local optima" (inbreeding). In this system, diversity isn't an aesthetic — it's what guarantees the manager sees a genuine choice (a cover path *and* a climb path), not six shades of the same template.

## Inputs
- The offspring set (post-recombination, post-mutation), each with squad/plan, ownership profile, and `variance_band`.
- The objective θ/k and the elite-set history (was selection already monochrome upstream?).

## Workflow

```
- [ ] 1. Measure collapse metrics across the offspring set
- [ ] 2. Compare against diversity floors
- [ ] 3. If collapsed: inject an under-represented genotype and/or raise mutation; signal re-run of crossover+mutation
- [ ] 4. Tune selection pressure (widen/tighten the elite set)
- [ ] 5. Emit the diversity report
```

## Step 1: Collapse metrics

- **Squad overlap:** mean pairwise % of shared players across offspring. >~75% mean overlap = collapsed.
- **Captain overlap:** do all offspring captain the same player / same day? Total captain overlap = collapsed (captaincy is the highest-leverage axis; it must vary).
- **Ownership-profile spread:** the spread of offspring across the template↔differential axis (mean effective-ownership of each offspring's distinctive picks). All clustered at "template" or all at "differential" = collapsed on the rank axis.
- **Variance-band coverage:** does the set include ≥1 low-variance AND ≥1 high-variance offspring? Missing a band = collapsed on the selection-pressure axis.

## Step 2: Diversity floors (the board must clear these)

A healthy offspring set, before it reaches the manager, must satisfy:
- mean pairwise squad overlap < ~75%,
- at least 2 distinct captain choices (or captain-ladder shapes) across the set,
- variance-band coverage: ≥1 low and ≥1 high band present,
- ownership spread: at least one cover-leaning and one differential-leaning option.

These exist so `decision-board-format.md`'s "2–4 genuinely distinct options spanning the variance spectrum" is structurally guaranteed, not hoped for.

## Step 3: If collapsed — re-seed *wider*, mutate, re-run

The Evolution document's remedies plus the systems-thinking digest's broad-band respawn (`system-dynamics.md` §1–2):
- **Re-seed from a *wider* kernel, not the mean.** Identify the under-represented corner (usually high-variance / differential when selection pressure was high) and force that archetype's blocks in **wider than the current population's spread** — if everything converged to chalk, inject an A2/A4 rebuild *braver than any survivor*, not a copy of the survivors' average. Averaging toward the collapsed centre is the wrong move; widen away from it. (Migration with a wide kernel — the digest's "respawn from a distribution wider than the current std".)
- **Raise the mutation rate** for the re-run so the regenerated offspring explore further from the collapsed template.
- **Signal the engine to re-run** crossover (Phase 3) + mutation (Phase 4) for the affected offspring, then re-measure. Cap at 2 re-runs to avoid loops; if still collapsed after 2, emit what you have *with an explicit "low-diversity board" flag* so the Director can tell the manager the options are genuinely close this round (sometimes one template really is dominant — that's honest, but say so).

## Step 3.5: Protected-invariant guard + critical-numerosity probe

- **Protected-invariant guard (`invariants.md` §4, §10).** This guard is itself invariant: **no learning-loop update may weaken it, and no archetype is ever zeroed.** Before accepting any soft-prior tilt the scoreboard proposes, confirm it would not (a) drive a genotype's weight to zero, (b) let one genotype's blocks dominate every offspring, or (c) disable/soften this diversity check. If it would, **reject the tilt** and report it — the population search has started eating its own safety rail (the digest's #1 failure: premature convergence + the self-update overwriting the diversity monitor).
- **Critical-numerosity probe (`system-dynamics.md` §5).** Population size N (the archetype count) is *not* monotonic. If the same decision rerun keeps producing qualitatively different winners — high run-to-run instability in which option leads — that's the signature of sitting near a critical N. Flag it to the Director to **probe N−1 and N+1** rather than reflexively adding lanes; prefer the count that yields a stable, spectrum-spanning board. More archetypes is not automatically better.

## Step 4: Selection-pressure tuning

- **Too high** (every stage kept only the single best fitness → monochrome set): widen the elite set, force the variance spread back in. Pressure that collapses the gene pool defeats the population.
- **Too low** (offspring are noise, no quality concentration): tighten — narrow toward the higher-fitness fusions. The target is a *healthy middle*: 2–4 offspring that are distinct **and** good.
- Pressure direction also tracks θ — `protect` legitimately tilts the *recommended default* toward low-variance, but it must **not** delete the high-variance option from the board (re-weight, don't collapse — `fitness-function.md`).

## Step 5: Emit the diversity report

```yaml
diversity_report:
  mean_squad_overlap: <%>
  distinct_captains: <n>
  variance_bands_present: [low, medium, high?]
  ownership_spread: cover↔differential coverage: ok|gap
  collapsed: false|true
  actions_taken: [ "injected A2 differential pod into offspring_3", "raised mutation 0.1→0.25", "re-ran crossover ×1" ]
  board_flag: none | "low-diversity: options genuinely close this round"
```

This report goes to the Director so the manager knows whether the board is a wide-open choice or a narrow one. Transparency about diversity is part of the advisory contract.

## Guardrails
- **The board must clear the diversity floors** or carry an explicit low-diversity flag. Never present six near-identical squads as a "choice."
- **Re-weight, don't delete.** θ tilts the default; it never removes the opposite-variance option.
- **Cap re-runs at 2.** Sometimes convergence is correct — say so rather than thrash.

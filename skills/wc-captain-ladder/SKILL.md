---
name: wc-captain-ladder
description: Computes the optimal rolling-captaincy LADDER across a matchday's staggered kickoff sequence — the ordered captain candidates, the explicit bank-or-switch rules at each kickoff, and the captaincy_uplift that wc-fitness-eval folds into raw_xEV. Because the armband doubles the round's points AND can be MOVED during the round to a player who has not yet kicked off, captaincy EV is the expected value of the best outcome reachable by switching across the sequence — not a naive 2x of the top xEV player. Call from wc-matchday-tactician (to write MB2 of the matchday plan), from the strategists (to value a candidate's captaincy when building a matchday plan), and from wc-fitness-eval (which consumes captaincy_uplift). Returns the ladder, the switch thresholds, and the uplift against a stated baseline; the ladder is moot under the Maximum Captain chip (value = max of candidates).
---

# wc-captain-ladder — the rolling-captaincy edge

Implements **MB2 — Captain Ladder** from `footballfantasy/context/frameworks/building-blocks.md`, the captaincy clauses of `league-config.md` ("Captaincy — the rolling-captain edge"), and the captaincy-in-EV note in `scoring-rules.md`. It supplies the `captaincy_uplift` term that `wc-fitness-eval` adds inside `raw_xEV` (see `frameworks/fitness-function.md`).

This is the **single biggest structural difference from FPL** and the largest single lever in `wc-matchday-tactician`'s claimed ~20–40 pts/round active-management edge. In FPL the captain is locked at deadline; here the armband **doubles the round's points** and can be **moved during the round to any captain candidate who has not yet kicked off**. So the question is never "who is the highest-xEV captain?" — it is **"what is the expected value of the best armband I can realise by watching the early games and re-deciding before each later candidate kicks off?"**

That makes captaincy a **sequential decision under uncertainty**, not a point estimate. A merely-good captain who plays in the late kickoff is worth more than a marginally-better one who plays first, because the late slot lets you bank an early hauler and only ride the late man if the early games disappoint. This skill prices that optionality.

---

## Why captaincy_uplift is not 2× the best player

Define `xEV_cap(p)` as the (already fixture-scaled, minutes-weighted) expected captain *bonus* from player `p` — i.e. the **extra** points the armband adds, which equals one more copy of `p`'s round score: `xEV_cap(p) = xEV(p)`. The naive captaincy value is `max_p xEV(p)`: pin the armband on the top player and never touch it.

The ladder beats that by an **option premium**. With candidates on different days you observe the early candidate's actual return, then keep-or-switch. You capture the *maximum* of correlated-but-staggered draws rather than a single fixed draw:

```
naive   = max_p  E[score(p)]                          # one fixed bet, set at lock
ladder  = E[ max over the switching policy of the realised captain score ]   # best reachable, decided live
uplift_vs_naive = ladder − naive   ≥ 0
```

The premium is largest when (a) candidates kick off on **different days** (you actually get to see results before committing the late slot), (b) the candidates have **comparable xEV** (no runaway favourite, so the live info changes the decision), and (c) each candidate's **outcome variance is high** (boom/bust attackers — the max of two volatile draws is well above either mean). It collapses to ~0 when everyone kicks off simultaneously (no information, no switch) or when one candidate dominates so heavily that you would never move off him.

---

## Workflow

```
- [ ] 1. Inputs: the squad/XI, this round's kickoff schedule (UTC, per match), θ, and
        the player-ev signals (xEV, variance, ceiling, floor) for every captain candidate
- [ ] 2. Build the candidate set: 2–3 from BB1 Captain Core, ideally on DIFFERENT days.
        If <2 candidates, or all on one day → no ladder; flag it (see Guardrails)
- [ ] 3. Reconstruct each candidate's per-match point DISTRIBUTION from its player-ev moments
- [ ] 4. Order candidates by kickoff time (earliest first = the first decision node)
- [ ] 5. Solve the optimal switching policy by backward induction over the kickoff sequence,
        applying the BANK-OR-SWITCH thresholds, MATCHUP-CONTINGENT
- [ ] 6. Read off the ladder: lock pick + the explicit per-kickoff switch rules
- [ ] 7. captaincy_uplift = E[optimal ladder] − baseline (STATE which baseline)
- [ ] 8. Maximum-Captain override: if that chip rides this round, value = max of candidates;
        the ladder is moot — emit it flagged
- [ ] 9. Emit the captain-ladder signal (ordered ladder + switch rules + uplift + baseline)
```

---

## METHOD

### Step 1 — Candidate set (from BB1)

Take the captain candidates from the squad's **BB1 Captain Core** (the 2–3 premium FWD/attacking-MID; `building-blocks.md`). A valid ladder wants:

- **2–3 candidates** — one is no ladder (it degenerates to "captain him"); four-plus is noise (the third candidate almost never gets the armband once two strong ones have been observed).
- **On different match days/slots.** This is the linkage BB1 shares with BB6 (matchday spread). If the Captain Core is strong but all three kick off in the same slot, the ladder has **no switching value** — say so and price captaincy at the naive `max`.
- Only **genuine** candidates: a player must be in the **XI (MB1)** and start (use `start_prob`/`p60` from the player-ev signal; do not put a rotation-risk player on the ladder as a primary). A bench player can be a *contingent* late candidate only if a manual sub (MB3/MB4) would promote him into the XI before his kickoff.

### Step 2 — Per-candidate point distribution

`wc-player-ev` emits `xEV`, `variance`, `ceiling`, `floor` per player. Captaincy is driven by the **tails** (a captained 2-pointer is a disaster; a captained 15 wins the round), so do **not** reduce a candidate to its mean. Reconstruct a working distribution from the moments:

- Use a **3-point discretisation** that matches the player-ev moments — a *blank/floor* node, a *base/return* node, and a *ceiling/haul* node — with probabilities chosen to reproduce `xEV` (mean), `variance`, and to put mass at `floor` and `ceiling`:

  | node | value | typical attacker meaning |
  |---|---|---|
  | floor (blank) | `floor` (≈ appearance only, e.g. 1–2) | played, no attacking return |
  | base (return) | near `xEV` | one goal-or-assist game |
  | ceiling (haul) | `ceiling` (e.g. 13–20+) | brace / goal+assist / penalty haul |

  Solve the three node-probabilities `(p_floor, p_base, p_ceil)` from the three constraints `Σp=1`, `Σ p·v = xEV`, `Σ p·(v−xEV)² = variance`. If the player-ev signal already carries a `dist` field, use it directly and skip the reconstruction.
- These are the *captain bonus* draws (one extra copy of the round score), and they map points→keep/switch through the thresholds below.
- **Note on correlation:** candidates on the **same** team or in the **same** match are positively correlated (a team-wide good day lifts both); treat them as effectively one ladder node for switching purposes (you cannot bank one and ride the other on fresh information — they resolve together). The option premium lives in candidates whose matches are **independent and staggered**.

### Step 3 — Order by kickoff, then solve the switching policy (backward induction)

Order the candidates `c_1, c_2, …, c_n` by kickoff time, earliest first. The armband is on someone at lock; after each candidate's match finishes you may move it to any not-yet-kicked-off candidate. Solve **backwards**:

```
Let s_i = realised captain score of candidate c_i (drawn from its Step-2 distribution).

Terminal: once only the last candidate c_n remains un-played, its value is E[s_n].

Induction at node i (c_i has just finished, armband currently notionally on the
banked-best-so-far b = max realised score among c_1..c_i that the armband could hold):
    keep_value   = b                                # bank what's already realised
    switch_value = E[ max over the remaining optimal policy of s_{i+1..n} ]
    decision = SWITCH if switch_value > keep_value else KEEP
    node_value = max(keep_value, switch_value)

E[optimal ladder] = the value at the first decision node, integrated over all
early-result realisations (compute exactly over the 3^k discretised outcome grid,
or Monte-Carlo if n and node-count make the grid large).
```

Crucially the rule is **state-dependent**: you keep an early haul and switch away from an early blank. The lock pick is the candidate that maximises the *whole policy's* value (usually an early candidate so you preserve the option to bank or bail) — but if the strongest candidate is the latest kickoff, the policy is "provisionally captain the early man, bank a haul, otherwise roll to the late favourite."

### Step 4 — The BANK-OR-SWITCH thresholds (the live switch rules)

The backward induction is driven by these thresholds on the **realised captain score of the candidate who just played** — the operational rules the manager executes live, and the ones written into MB2:

| Realised captain score | Action | Rationale |
|---|---|---|
| **2–5** | **Switch** to the next candidate (if any remains un-kicked-off) | A captained ~3 is a wasted armband; almost any live candidate's mean beats banking it. |
| **6–7** | **Close call / contingent** | Bank it only if the next candidate's *matchup-adjusted* mean is **below** the banked score; otherwise switch. This band is where matchup-contingency decides. |
| **8+** | **Usually keep** | A captained 16 (8 doubled) is a strong round; only switch for a clearly superior remaining matchup (e.g. a penalty-taker vs a minnow at home, still to play). |
| **10+** | **Almost always keep** | Chasing more variance off a banked 20 is −EV against any realistic remaining candidate; never throw it away (Guardrail). |

**Matchup-contingency** shifts every threshold. Switch *more freely* (treat 6–7, even a soft 8, as switchable) when the next candidate has the **materially easier assignment** — at home, vs a weak defence (high opponent xGA, low PPDA resistance), on penalties, with their team a heavy favourite to dominate territory and pile up shot volume. Switch *less freely* (hold even a 5–6) when the only remaining candidate faces a **tough, low-block opponent** or carries **rotation/minutes risk** — a captained blank from a benched-at-half forward is worse than a banked 6.

Encode matchup as a per-candidate **switch-readiness multiplier** on its xEV when evaluating `switch_value`: scale up the easier-fixture candidate (e.g. ×1.15 for a home favourite vs a leaky defence), down the harder one (×0.85 vs an elite defence or with `rotation_risk`). Source the fixture difficulty from the `fixture` signal (`wc-fixture-progression`) and the minutes/role risk from the `scout` signal — **do not re-derive them here**.

### Step 5 — captaincy_uplift (and STATE the baseline)

`captaincy_uplift` is what `wc-fitness-eval` consumes; it must declare its baseline so two candidates are compared like-for-like:

```
captaincy_uplift = E[optimal ladder]  −  baseline
```

Emit **both** baselines and label which one fitness should use:

- **`baseline = no_captain`** → `uplift = E[optimal ladder]` (the captain bonus is one extra copy of the captained score; with no captain the XI scores its base once). This is the term that enters `raw_xEV` as the captaincy contribution. **Use this by default** for fitness's `raw_xEV` so captaincy is counted once, cleanly.
- **`baseline = static_chalk`** → `uplift = E[optimal ladder] − E[score(chalk captain held all round)]`, where the chalk captain is the highest effective-ownership captain (the field's default armband, from `wc-ownership-meta`). This is the **rank-relevant** number — what the ladder gains *over the field's set-and-forget armband* — and is the more honest figure to show on the decision board's captaincy line and to compare across the population.

State the baseline explicitly in the output; a `captaincy_uplift` without its baseline is meaningless to fitness.

**θ interaction (consistent with the fitness variance dial):** the *expected* ladder value is objective-neutral, but report the ladder's **captain variance** so fitness can sign it. When `θ=gain`, the board may prefer the *higher-ceiling* lock pick even at marginally lower mean (the switch policy already banks upside); when `θ=protect`, prefer the lock pick whose policy has the **higher floor** (more candidates that let you bail off a blank). Do not bake θ into the EV here — emit the mean *and* the variance and let `wc-fitness-eval` apply ±k·variance.

### Step 6 — Maximum Captain chip override

If the **Maximum Captain** chip rides this round (`chip-catalog.md` #3, MB5), the game retroactively captains your highest-scoring player — captain-pick risk is removed entirely. The ladder is **moot**:

```
captaincy_value(Max-Captain) = E[ max over ALL eligible players of their realised round score ]
```

This is the expectation of the maximum over the *whole XI* (not just BB1), with **no switching constraint and no kickoff ordering** — strictly ≥ the ladder. Emit it flagged `chip: maximum_captain`, with `ladder_moot: true`, and pass this value (not the ladder) to fitness for that round. (Conversely, this skill's own output is a signal of *how much the ladder is worth* — if the ladder's uplift over static chalk is already large, the Maximum Captain chip adds little and is better held; surface that for `wc-chip-strategist`.)

---

## Output (the `captain-ladder` signal)

```yaml
type: captain-ladder
round: <round id, e.g. 2026-grp-md2>
date: <YYYY-MM-DD>
emitted_by: wc-captain-ladder
confidence: <0.00–1.00>          # cap 0.35 if a candidate's start/minutes is web-unconfirmed
source_urls:
  - <kickoff schedule url>
  - <predicted-XI / minutes url per candidate>   # or manager-provided

ladder_valid: true|false          # false if <2 candidates or all same slot
no_ladder_reason: <if invalid: "single candidate" | "all candidates same kickoff slot">

lock_pick: <player>               # who wears the armband at deadline
ladder:                            # ordered by kickoff (earliest first)
  - order: 1
    player: <name>
    team: <nation>
    kickoff: <UTC>
    xEV: <n>           variance: <n>     ceiling: <n>   floor: <n>
    matchup: <one football line — opponent xGA, home/away, pen duty, fav?>
    switch_readiness: <multiplier, e.g. 1.15>   # higher = switch toward this one more freely
  - order: 2
    player: <name>
    # …same shape…
switch_rules:                      # the live, executable instructions (MB2 content)
  - "Lock the armband on <lock_pick>."
  - "After <c_1> (<kickoff>): if his captain score ≤5 → move to <c_2>; 6–7 → switch only if <c_2> faces the softer matchup; 8+ → keep."
  - "After <c_2> (<kickoff>): bank anything ≥8; below that, roll to <c_3> if <c_3>'s adjusted mean is higher."
  - "Never move off a banked 10+."

captaincy_uplift:
  ladder_ev: <E[optimal ladder]>
  vs_no_captain: <n>               # = ladder_ev; the term raw_xEV consumes (default)
  vs_static_chalk: <n>             # ladder_ev − E[chalk-captain held all round]; the board figure
  chalk_captain: <player>          # field's default armband (highest EO)
  baseline_for_fitness: no_captain # which one wc-fitness-eval should use
  ladder_variance: <n>             # captain-score variance, for fitness's ±k·variance term

chip:
  maximum_captain: <true|false>
  ladder_moot: <true|false>        # true when maximum_captain is on
  max_captain_value: <E[max over XI] — only when the chip rides>
```

(Frontmatter follows the common signal schema in `frameworks/signal-framework.md`; `wc-signal-emitter` validates and persists it.)

---

## Guardrails

- **A ladder needs candidates on different days.** If the Captain Core all kicks off in the same slot, there is **no switching value** — set `ladder_valid: false`, price captaincy at the naive `max` of the candidates, and flag it loudly so the manager (or a strategist on a squad build) knows the squad has *captaincy fragility*: BB1 and BB6 are mis-laid out. This is exactly the linkage failure `building-blocks.md` warns about ("reshuffle them onto one day and the ladder is dead").
- **Never throw away a banked 8+ chasing variance against a tough opponent.** The thresholds are asymmetric for a reason: the downside of switching off a real haul into a captained blank dwarfs the upside of a marginally higher mean. A banked 10+ is final. This guardrail holds *regardless of θ* — even a chaser does not bin a banked 20.
- **Do not put a rotation/minutes risk on the ladder as a primary candidate.** A captained early sub who is hooked at 60' for tactical reasons is a wasted armband with no switch left. Demote minutes-risky names to *contingent* late candidates only (and only if a manual sub would field them); cap confidence at 0.35 and add a "confirm start before lock" flag when `start_prob`/`p60` is web-unconfirmed.
- **Use, don't re-derive, upstream signals.** Per-player distributions come from `wc-player-ev`; fixture difficulty from `wc-fixture-progression` (the `fixture` signal); minutes/role from `wc-scout`; chalk/effective ownership from `wc-ownership-meta`. This skill *sequences and prices*; it does not re-scout players or re-rate fixtures.
- **State the baseline.** A `captaincy_uplift` is meaningless without it — `vs_no_captain` for fitness's `raw_xEV`, `vs_static_chalk` for the board and population comparison. Emit both; never a bare number.
- **Under Maximum Captain the ladder is moot.** Do not also count ladder uplift — that double-counts captaincy. Emit `max_captain_value` and `ladder_moot: true`, and let fitness use the max value for that round only.
- **Captaincy values trace to confirmed scoring.** If `scoring-rules.md` still has `confirmed: false`, mark the uplift provisional — the absolute magnitudes (especially the doubled goal/haul values) depend on the unverified point table.

---
name: wc-player-ev
description: Computes one player's expected FIFA World Cup Fantasy points for a single round (xEV) from a scout signal — folding start probability, the 60-minute appearance cliff, fixture-and-minutes-scaled npxG/xA, clean-sheet and defensive-action floors, the penalty/set-piece premium, and the card/concede downside into one number plus its full decomposition, variance, ceiling, and floor. This is the atomic EV unit the whole system samples from. Use whenever a single player's per-round point distribution is needed — called by wc-scout, every wc-strategist genotype, wc-matchday-tactician, and wc-fitness-eval (which sums these into raw_xEV). Reads the scout signal; never re-scouts. Emits a player-ev signal.
---

# wc-player-ev — the atomic expected-points unit

Implements the `xEV(player)` formula defined in `footballfantasy/context/frameworks/scoring-rules.md`. Everything in this system that talks about a player's value — a strategist weighting a pick, the captain ladder sampling a candidate's distribution, `wc-fitness-eval` summing `raw_xEV` — ultimately samples the number this skill produces. So it has one job and must do it precisely: turn a **scout signal** (minutes model, npxG/xA, set-piece duty, card/rotation/injury risk) plus the round's **fixture** and **clean-sheet** signals into a player's expected points for *this* round, with the decomposition exposed so downstream agents reason about *why*, not just *how much*.

Two properties dominate every other term and must never be smoothed over:
1. **The 60-minute cliff.** The appearance tier is a step function, not linear in minutes — 59' and 60' are one point apart, and nearly every defensive/clean-sheet return requires the 60' threshold. A nailed-on starter banks this floor; a rotation risk's whole distribution shifts down and widens. Minutes security is the single biggest EV driver after goals.
2. **The penalty / set-piece premium.** A confirmed penalty taker and primary set-piece deliverer carries a structurally higher xG/xA than open-play numbers alone imply. This premium is large, position-agnostic, and must be surfaced explicitly (it is a top-3 focus on the FIFA strategy ladder and the reason a mid-price pen-taker often out-EVs a pricier non-taker).

This skill is the **floor-and-ceiling factory**. It does not decide captaincy (that sequencing belongs to `wc-captain-ladder`, which samples the per-player distribution this skill emits), does not score rank-relative fitness (that belongs to `wc-fitness-eval`), and does not derive its own clean-sheet probability or fixture difficulty (those are upstream signals — read them, never recompute).

## When to invoke

- `wc-scout` chains into it to attach an EV to a player it has just profiled.
- Any `wc-strategist` genotype calls it per candidate player and then *re-weights* the output by genotype (A2 multiplies appeal by low-ownership leverage; A5 maximises the floor term; A4 leans on the fixture-scaled attacking terms against a weak opponent). The skill returns a neutral xEV; the archetype tilt happens in the caller.
- `wc-matchday-tactician` calls it for XI/bench ordering and to feed the captain ladder the distributions it sequences.
- `wc-fitness-eval` consumes the emitted `player-ev` signals as `raw_xEV` inputs — it must **read** them, not re-derive.

## Workflow

```
- [ ] 1. Read the scout signal for this player+round (start_prob, p60, npxg90, xa90, setpiece_share, pen_taker, rotation_risk, injury, suspension, minutes_model). DO NOT re-scout.
- [ ] 2. Read the round fixture signal (opponent strength / mismatch) and the clean-sheet signal (p_cs, expected_ga for the player's team). DO NOT recompute them.
- [ ] 3. Confirm scoring-rules.md point values: is `confirmed: true`? If not, set a provisional flag — relative ordering holds, absolute magnitudes carry a calibration caveat.
- [ ] 4. Resolve the minutes projection: expected_minutes from minutes_model; derive minutes_factor (= proj_min / 90) and the two appearance probabilities (P(plays), P(plays60+)).
- [ ] 5. Scale attacking output: xG_adj = npxg90 × minutes_factor × fixture_mult; xA_adj = xa90 × minutes_factor × fixture_mult. Add the penalty/set-piece premium into xG_adj/xA_adj where the scout confirms the duty.
- [ ] 6. Compute each EV term with the position-specific lambdas (goal weights GK10/DEF6/MID5/FWD4; cs weights GK4/DEF4/MID1/FWD0; etc.).
- [ ] 7. Sum to xEV. Build the decomposition (one line per term, signed).
- [ ] 8. Estimate variance, ceiling (P90-ish best realistic line), floor (P10-ish — usually the no-60'/blank line).
- [ ] 9. Set confidence: cap at 0.35 if minutes are unconfirmed or any load-bearing fact is web-unconfirmed; cap provisional if step 3 failed.
- [ ] 10. Emit the `player-ev` signal via wc-signal-emitter. Return its path.
```

## The method

### The formula (verbatim from scoring-rules.md, with the terms specified)

```
xEV(player) =   P(plays)        · appearance_tier_EV        # the 1–59' floor
              + P(plays 60+)     · minutes_bonus             # the 60' cliff (step, not ramp)
              + λ_goal(pos)      · xG_adj                    # fixture- & minutes-scaled npxG (+ pen/SP premium)
              + λ_assist         · xA_adj                    # fixture- & minutes-scaled xA  (+ SP-creation premium)
              + λ_cs(pos)        · P(clean sheet | fixture)  # GK/DEF/MID only — needs 60'
              + λ_save           · expected_saves            # GK only
              + λ_defact         · P(def-actions threshold)  # DEF / ball-winning MID
              + λ_setpiece       · set_piece_share           # residual premium not already in xG_adj/xA_adj
              − λ_card           · card_risk                 # yellow/red expectation
              − λ_concede(pos)   · expected_GA               # GK/DEF — the −1 per 2 conceded bracket
```

All point magnitudes (`appearance_tier_EV`, `minutes_bonus`, the `λ`s) are read from `scoring-rules.md`. The skill never hard-codes them in a way that survives a rules update — if that file says `confirmed: false`, every absolute number below is provisional.

### Position weight table (from scoring-rules.md — the part that makes positions differ)

| λ | GK | DEF | MID | FWD | note |
|---|---|---|---|---|---|
| `appearance_tier_EV` (1–59') | +1 | +1 | +1 | +1 | floor of any pick that gets on the pitch |
| `minutes_bonus` (the 60' tier, total when 60+) | +2 | +2 | +2 | +2 | the cliff — modelled as the *extra* above the 1–59' tier |
| `λ_goal` | **10** | **6** | **5** | **4** | a DEF goal pays more but fires far less often |
| `λ_assist` | 3 | 3 | 3 | 3 | position-flat |
| `λ_cs` (clean sheet, 60+) | 4 | 4 | 1 | 0 | the defensive-stack engine; MID gets a token, FWD nothing |
| `λ_save` (per 3 saves) | ~0.33/save | — | — | — | GK only; expected_saves × (1/3) |
| `λ_defact` (def-actions threshold) | — | +2 | +2 | — | CB/full-back clearances-blocks-interceptions or tackles; the hidden floor |
| `λ_concede` (per 2 conceded) | −0.5/goal | −0.5/goal | — | — | GK/DEF only; expected_GA × (1/2) |
| `λ_card` | −1 yellow / −3 red | same | same | same | position-flat |

The asymmetry the manager already knows but the math must honour: **a defender's goal is worth 6 to a forward's 4, but a centre-back's per-match npxG is a fraction of a striker's**, so on raw goal EV forwards still win — *except* a set-piece-threat CB against a weak, set-piece-vulnerable opponent, whose `xG_adj` can spike enough that `6 × xG_adj` rivals a forward's `4 × xG_adj`. That crossover is exactly what this skill exists to surface; do not pre-judge it, compute it.

### Term-by-term

**1. Minutes resolution (do this first — it gates everything).**
From the scout's `minutes_model` derive an `expected_minutes` projection. Then:
- `minutes_factor = expected_minutes / 90` (a 70-minute projection ⇒ ~0.78; this scales all open-play output linearly — a player on the pitch 78% of the match generates ~78% of a 90-minute xG/xA baseline).
- `P(plays)` = `start_prob` + (cameo probability if a likely sub). Use the scout's `start_prob`/`p60` directly; do not invent them.
- `P(plays 60+)` = `p60` from the scout. This is the gate on the appearance bonus **and** on every clean-sheet/defensive return (those require the 60' threshold).

The cliff in practice: a nailed starter with `p60 ≈ 0.92` banks the bonus tier almost every week; a 65%-to-start rotation risk with `p60 ≈ 0.5` loses roughly half the appearance bonus *and* half the clean-sheet EV *and* widens variance — model it as the probability-weighted step, never as "minutes × a rate."

**2. Fixture & minutes scaling of attacking output.**
```
fixture_mult = opponent-adjusted multiplier from wc-fixture-progression's `fixture` signal
               (a striker vs a leaky minnow > 1; vs an elite, deep-block defence < 1)
xG_adj = npxg90 · minutes_factor · fixture_mult
xA_adj = xa90   · minutes_factor · fixture_mult
```
`npxg90`/`xa90` are **non-penalty** per-90 rates from the scout (npxG strips penalties so they aren't double-counted). `fixture_mult` is read, not derived — `wc-fixture-progression` already encodes opponent defensive/attacking strength for this specific fixture, and the team's clean-sheet probability comes from `wc-clean-sheet-model`. Typical band: ~0.6 (brutal matchup) to ~1.5 (mismatch); the fixture signal supplies the exact value.

**3. The penalty / set-piece premium (fold in here, then avoid double-count).**
If the scout flags `pen_taker: true`, add the expected penalty contribution into `xG_adj`:
```
xG_adj += P(team wins a penalty this match) · P(this player takes it) · P(scores | takes)
```
A primary penalty taker on a side that draws ~0.25–0.4 penalties/match is carrying meaningful extra goal expectation that open-play npxG misses entirely — this is the premium, and it is why pen-takers are a top-3 scout focus. For primary set-piece *delivery* (corners, direct free-kicks), add the incremental created-chance expectation into `xA_adj`. Whatever portion of set-piece value you have **already** folded into `xG_adj`/`xA_adj` here must NOT be re-added by the standalone `λ_setpiece · set_piece_share` term — that residual term covers only set-piece duty value not already expressed as xG/xA (e.g. a "won penalty" the player draws but doesn't take). Keep the books clean: premium counted once.

**4. Clean-sheet term (GK/DEF, token MID).**
```
+ λ_cs(pos) · P(clean sheet | fixture, team)
```
`P(clean sheet)` is read straight from the `clean-sheet` signal (`wc-clean-sheet-model`) for the player's team in this fixture — **never recompute it here.** Note it is implicitly conditioned on the player surviving to 60'; if `p60` is low, the realised clean-sheet EV is `P(cs) · (p60 / typical_starter_p60)` — a rotation-risk defender cannot bank a clean sheet he's subbed out of. FWD: this term is zero. MID: token (×1), but it still tips marginal mid choices toward the strong-defence side.

**5. Saves (GK only).**
```
+ λ_save · expected_saves   where  expected_saves ≈ opponent_shots_on_target_estimate (from fixture signal),
                                   scored at (1/3) point per save.
```
A shot-stopper behind a mid-tier defence facing a strong attack can paradoxically out-save-EV a keeper behind a dominant side who faces three shots — the save points and the clean-sheet points pull in opposite directions, and this skill exposes both so the caller sees the trade.

**6. Defensive-actions threshold (DEF / ball-winning MID — the hidden floor).**
```
+ λ_defact · P(player hits the CBI/tackles threshold this match)
```
From the scout's per-90 defensive-action rate and the fixture (a defender vs a side that attacks a lot sees more clearance/interception volume → higher threshold-hit probability). This is the term that gives a busy attacking full-back or a destroyer-mid a floor independent of clean sheets, and it is why such players are not pure clean-sheet lottery tickets.

**7. Negative terms.**
```
− λ_card   · card_risk      (E[yellow] · 1  + E[red] · 3 ;  a booking-prone player or a derby/high-stakes ref tilts this up;
                             watch yellow-card accumulation before knockouts — a suspension-risk yellow has cost beyond the −1)
− λ_concede(pos) · expected_GA   (GK/DEF only; expected_GA from the clean-sheet signal, scored at −0.5/goal i.e. −1 per 2 conceded)
```
`expected_GA` is the same upstream `clean-sheet` signal's field — read it. A leaky defence's downside enters here; it is what makes a cheap defender on a bad side a negative-tail pick even when his clean-sheet term is non-zero.

### Worked micro-example (illustrative; magnitudes provisional until scoring-rules confirmed)

A set-piece centre-back, nailed starter (`p60 ≈ 0.9`), `npxg90 = 0.12`, on a tournament favourite vs a weak set-piece-vulnerable minnow (`fixture_mult ≈ 1.4`, `P(cs) ≈ 0.55`, `expected_GA ≈ 0.7`), not a pen-taker, hits the defensive-actions threshold ~60% of matches:
```
appearance       ≈ 0.95 · 1   + 0.90 · 2(extra→ here total 2)   ≈ ~2.8   (floor: he plays and clears 60')
goal     6 · xG_adj  = 6 · (0.12 · 1.0 · 1.4)            ≈ 6 · 0.168 ≈ 1.0
assist   3 · xA_adj  ≈ small                              ≈ 0.2
clean    4 · 0.55                                          ≈ 2.2
defact   2 · 0.60                                          ≈ 1.2
concede −0.5 · 0.7                                         ≈ −0.35
card    −1 · ~0.15                                         ≈ −0.15
xEV ≈ 7.1   ceiling ≈ 16 (header + CS),  floor ≈ 1 (no 60' / conceded 2+)
```
The point is mechanical, not the exact total: against the right opponent the `λ_goal=6` weight plus a real CS probability lifts a set-piece CB into captain-ladder-adjacent territory — and the decomposition shows the manager it's a set-piece-and-stack bet, not form.

### Variance, ceiling, floor

- **variance** — from the spread of the discrete outcome lattice: appearance tier (binary cliff), goals (0/1/2 at xG_adj), assists, the clean-sheet binary, cards. A pen-taker and a set-piece CB are *high-variance-up* (fat right tail); a no-attacking-return holding mid on a coin-flip-minutes leash is *high-variance-down*. Report a single variance number plus a `variance_band: low|medium|high`.
- **ceiling** — the realistic top line (≈P90): the player starts, plays 90, returns (goal/assist), and the team keeps a clean sheet where applicable. This is what the captain ladder cares about.
- **floor** — the realistic bottom line (≈P10): usually the *no-60'* or *blank-and-booked* outcome. For a rotation risk the floor is near zero or negative (a 20-minute cameo with a yellow). The floor is the term `wc-fitness-eval` leans on when `θ=protect`.

The ceiling/floor split is the whole reason this skill emits a distribution and not a point estimate: A5 (EV Maximizer) reads the floor, A2 (Differential Hunter) reads the ceiling, the captain ladder reads both.

## Output (the `player-ev` signal)

Emit via `wc-signal-emitter` to `signals/<round>-player-ev-<player>.md`:

```yaml
---
type: player-ev
round: <round id, e.g. 2026-grp-md2>
date: <YYYY-MM-DD>
emitted_by: wc-player-ev
confidence: <0.00–1.00>          # ≤0.35 if minutes unconfirmed or a load-bearing fact web-unconfirmed
source_urls:
  - <scout signal path or url>   # facts trace to the scout signal / fixture / clean-sheet signals, or manager-provided
provisional_scoring: <true|false>   # true if scoring-rules.md is not confirmed:true → absolute magnitudes caveated
---
player: <name>
team: <nation>
position: <GK|DEF|MID|FWD>
price: <m>
fixture: <opponent + home/away>
minutes:
  expected_minutes: <n>
  minutes_factor: <proj_min/90>
  start_prob: <0–1>            # from scout — not re-derived
  p60: <0–1>                   # from scout — the cliff gate
xEV: <number>                  # the headline
decomposition:                 # signed, sums to xEV — MANDATORY (the board/fitness explain through it)
  appearance: <n>
  minutes_60_bonus: <n>
  goal:      <n>   # λ_goal(pos) · xG_adj
  assist:    <n>   # λ_assist · xA_adj
  clean_sheet: <n> # λ_cs(pos) · P(cs)   (0 for FWD)
  saves:     <n>   # GK only
  def_actions: <n> # DEF/ball-winning MID
  set_piece_residual: <n>   # premium NOT already folded into goal/assist
  card:      <-n>
  concede:   <-n>  # GK/DEF only
scaled_inputs:
  xG_adj: <n>      # npxg90 · minutes_factor · fixture_mult (+ pen premium if taker)
  xA_adj: <n>
  fixture_mult: <n>
  pen_taker: <true|false>
  pen_premium_in_xG: <n>      # portion of xG_adj from penalties (0 if not taker)
variance: <n>
variance_band: low|medium|high
ceiling: <n>       # ~P90 realistic best line
floor: <n>         # ~P10 — usually the no-60'/blank line
flags:
  - <e.g. "penalty taker — top-3 EV premium">
  - <e.g. "rotation risk: p60 0.5, re-check XI ~24h pre-lock">
  - <e.g. "yellow-card accumulation: one booking from a knockout suspension">
recheck_before_lock: <true|false>   # true whenever minutes are projected, not confirmed
---
```

## Guardrails

- **Read the scout signal; never re-scout.** `start_prob`, `p60`, `npxg90`, `xa90`, `setpiece_share`, `pen_taker`, `rotation_risk`, `injury`, `suspension` all come from the `scout` signal. If it is missing for this player+round, return that the scout must run first — do not fabricate minutes or rates.
- **Never recompute an upstream signal.** `P(clean sheet)`, `expected_GA`, and `fixture_mult` are read from `wc-clean-sheet-model` and `wc-fixture-progression`. Re-deriving them here would desync the system and double-handle uncertainty.
- **Confirm `scoring-rules.md` is `confirmed: true` before trusting absolute magnitudes.** If it is not, set `provisional_scoring: true` and caveat the xEV — *relative ordering between players is still usable, exact point totals are not.*
- **Cap confidence at 0.35 when minutes are unconfirmed** (predicted XI not yet out, or `injury`/`suspension` unresolved) or any other load-bearing fact could not be web-confirmed, and set `recheck_before_lock: true`. Minutes are the dominant lever — an unconfirmed start makes the whole distribution speculative.
- **Honour the 60' cliff as a step, not a ramp.** Do not approximate the appearance bonus as `minutes/90 × bonus`. It is gated on `p60`. Clean-sheet and defensive returns are gated on the same threshold.
- **Count the set-piece/penalty premium exactly once.** Whatever you fold into `xG_adj`/`xA_adj` must not also appear in the `set_piece_residual` term. Report `pen_premium_in_xG` so the caller can see it.
- **xEV is neutral; archetype tilt belongs to the caller.** Do not bake ownership leverage, rank objective, or genotype weighting into xEV — that is `wc-fitness-eval`'s and the strategists' job. This skill emits the raw per-round distribution they sample.
- **Decomposition is mandatory and must sum to xEV.** The board and the fitness function explain options through it; a bare number is not a valid output.
- **Captaincy is out of scope.** Emit the per-player distribution; `wc-captain-ladder` handles the across-kickoff doubling. Do not 2× anything here.

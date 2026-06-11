---
name: wc-clean-sheet-model
description: Computes clean-sheet probability and defensive-returns EV for a team in a specific fixture from team defensive strength (xGA) against opponent attacking strength (xG), then models the STACK CORRELATION that turns a Clean-Sheet Spine (BB2) — GK + k same-team defenders — into a single correlated bet rather than k independent draws. Returns p_cs(team,fixture), a stack_corr_bonus capturing the amplified joint ceiling and shared downside (sign interacts with the rank objective θ: amplify when chasing, discount when protecting), and expected_ga with its conceding-points downside. Use when sizing a defensive stack, valuing a GK/DEF pick, scoring a candidate's BB2, or weighing the Clean Sheet Shield chip — called by wc-squad-architect, wc-matchday-tactician, wc-fitness-eval, and the strategists.
---

# wc-clean-sheet-model — clean-sheet probability + the stack correlation

Implements the clean-sheet and defensive-returns piece of `footballfantasy/context/frameworks/scoring-rules.md`, and supplies the `cs_corr_bonus` term that `fitness-function.md` adds and that the **Clean-Sheet Spine (BB2)** in `building-blocks.md` exists to capture. Defensive points are *lumpy and team-correlated*: the GK and the whole back line keep a clean sheet **together** or concede **together**. So a 3-defender-plus-GK stack from one strong defence is not four independent picks — it is **one bet with an amplified ceiling and a shared floor**. This skill is where that correlation is priced. Every defensive EV in the system traces back to the `p_cs` and `expected_ga` it emits; downstream agents read the signal, they do not re-derive it (`signal-framework.md`).

The two jobs:
1. **Per-team clean-sheet probability and expected goals against** for the specific fixture — the marginal building block of every GK/DEF/MID defensive return.
2. **The joint distribution of a same-team stack** — the correlation bonus (and its θ-dependent sign) that makes BB2 a coherent module and the Clean Sheet Shield chip a natural partner.

---

## Workflow

```
- [ ] 1. Read inputs: team, opponent, fixture; the `fixture` signal (team xGA, opp xG, difficulty, p_advance); θ and k from the spawn prompt; the stack composition if scoring a BB2
- [ ] 2. Build expected_GA = blend(team defensive xGA-against-this-opponent, opponent attacking xG) × game-state and home/neutral adjustments
- [ ] 3. p_cs = Poisson P(opponent scores 0 | expected_GA) = exp(−expected_GA), refined by defensive-quality and low-block/game-state tilt
- [ ] 4. Per-player defensive EV: λ_cs(pos)·p_cs + clean-sheet-conditional save/defact terms − λ_concede(pos)·E[concede-bracket penalty]
- [ ] 5. Stack: model the joint via a shared team-defence latent; compute P(whole stack clean) and the marginal-vs-joint gap → stack_corr_bonus
- [ ] 6. Apply θ sign: amplify stack_corr_bonus when gain, discount when protect; flag Clean Sheet Shield fit if a full 3+1 stack vs a weak attack
- [ ] 7. Emit the `clean-sheet` signal: p_cs, stack_corr_bonus, expected_ga, conceding downside, confidence
```

---

## Method

### 1. Expected goals against (the engine quantity)

Everything keys off `expected_GA(team, fixture)` — the team's expected goals conceded in *this* match. Build it from both sides of the fixture so neither a stout defence vs a great attack nor a leaky defence vs a poor attack is mispriced:

```
expected_GA =  w_def · xGA_team_vs_this_style       # how much this defence usually concedes (per-90, recent form-weighted)
             + w_att · xG_opponent_vs_this_style     # how much this attack usually creates (per-90)
             scaled by minutes-on-pitch context, then × adjustments below
```

- Read `xGA_team` and `xG_opponent` from the `fixture` signal (`wc-fixture-progression`). Do **not** re-derive fixture difficulty — consume it.
- Blend weights default `w_def = w_att = 0.5`; tilt toward the side with the larger, more reliable sample (a defence with 6 tournament matches outweighs an opponent with 1). At the World Cup, samples are tiny — lean on pre-tournament reference-class xGA/xG and cap confidence accordingly (see Guardrails).
- **Adjustments (multiplicative on expected_GA):**
  - **Opponent strength tier / mismatch:** a top seed vs a weak qualifier compresses expected_GA hard — this is the A4 Fixture Exploiter's whole edge. Use the `mismatch_list` from the fixture signal.
  - **Game state / motivation:** a dead-rubber group game where the opponent rotates or sits off → lower expected_GA. A must-win opponent chasing the game → higher. A knockout cagey-tie prior → lower (low-event games are clean-sheet-rich, per the chip catalog's KO note).
  - **Home / neutral:** 2026 is largely neutral or host-advantaged venues — apply a small host bump for USA/CAN/MEX, otherwise treat as neutral (no standard home boost). Flag if manager-provided venue info contradicts.
  - **Personnel:** a confirmed first-choice CB/keeper out (from the `scout` signal) widens expected_GA; full-strength back line tightens it. Reference the scout's `injury`/`rotation_risk`, do not re-scout.

### 2. Clean-sheet probability (first-order Poisson, refined)

Goals conceded in a match are well-approximated as Poisson with mean `expected_GA`. A clean sheet is the opponent scoring **zero**:

```
p_cs(team, fixture) = P(opponent scores 0) = exp(−expected_GA)          # first-order Poisson estimate
```

Sanity anchors (use to gut-check, not to override the model): `expected_GA = 0.7 → p_cs ≈ 0.50`; `1.0 → 0.37`; `1.3 → 0.27`; `1.6 → 0.20`; `2.0 → 0.14`. A clean sheet is a **minority outcome even for a big favourite** — never carry `p_cs` above ~0.60 without a confirmed mismatch, and treat anything above 0.65 as a flag to re-examine expected_GA.

**Refinements on the raw Poisson:**
- **Defensive-quality / low-block tilt:** elite low-block defences (and packed-in underdogs parking the bus) suppress the *tail* of goals against more than Poisson assumes — apply a small positive shrink to `p_cs` (+0.02 to +0.05) for a genuinely disciplined defensive setup, and a small negative one for a high-line side that bleeds chances even in wins. Keep the adjustment bounded; it tunes, it never dominates expected_GA.
- **60-minute rule:** the clean-sheet point requires the player on the pitch for 60+ and the sheet intact at the player's exit. For a rotation-risk defender (early-sub or in-game-management substitution likely), multiply the CS-return EV by `p60` from the scout signal — a stack's correlation is worthless on a player who comes off at the hour with the score 0-0 and concedes after.
- **Optional Poisson-difference upgrade:** when both teams' xG are reliable, model home/away goals as a Skellam (Poisson-difference) to get `P(opp = 0)` jointly with the win/draw distribution — useful when game state feeds back (a team protecting a lead drops deeper, lowering late expected_GA). Default to the simple exponential unless the fixture signal carries reliable two-sided xG.

### 3. Per-player defensive-returns EV

For a GK or DEF (and partial-credit MID per the scoring table), the clean-sheet-and-defence contribution to `xEV` (the term `wc-player-ev` consumes) is:

```
def_EV(player) =  λ_cs(pos) · p_cs · p60                         # clean-sheet point, gated on 60'+
                + λ_save · E[saves]                  (GK only)    # E[saves] rises as expected_GA rises — partial hedge vs the CS miss
                + λ_defact · P(hit defensive-actions threshold)   (DEF / ball-winning MID)
                − λ_concede(pos) · E[concede-bracket penalty]     # the downside — see below
```

- `λ_cs(pos)` from `scoring-rules.md` (provisional GK/DEF +4, MID +1, FWD 0 — confirm). The MID clean-sheet rule is a real, often-overlooked floor on a defensive-minded midfielder in a strong side; surface it.
- **The GK hedge:** higher `expected_GA` *lowers* `p_cs` but *raises* `E[saves]` — a keeper behind a busy-but-resolute defence has a partial floor even without the sheet. Estimate `E[saves] ≈ shots_on_target_faced` (scales with expected_GA and opponent xG); credit the per-3-saves point and the penalty-save tail.
- **Defensive-actions floor (DEF/MID):** attacking full-backs and ball-winning mids can hit the CBI/tackles threshold even in a leaky game — this is a *non-correlated* floor that partially offsets a stack's shared downside. Flag when a stack member carries it (it diversifies the bet from within).

### 4. The conceding-points downside (the bracket)

The mirror of the clean sheet. GK/DEF lose points per the concede bracket (provisional: −1 per 2 goals conceded). Because expected_GA is the same latent that drives both, the downside is **mechanically tied** to the upside — and for a stack it is **shared** (they all sit in the same conceding bracket together). Return it explicitly so the board can show the floor, not just the ceiling:

```
E[concede_penalty(team)] = Σ_g P(opponent scores g | expected_GA) · penalty_bracket(g)     # Poisson over goals conceded
```

For a **stack of `k` defenders + GK**, the concede penalty is incurred by *every* stacked player on the same goals-against draw — so the downside scales ~linearly with stack size on the bad draws, while the upside also scales on the good draws. That two-sidedness is the heart of the stack bonus below.

### 5. The stack correlation bonus (the value-add)

This is the term BB2 exists for and that `fitness-function.md` adds as `cs_corr_bonus`. A naive model treats `k` defenders + a GK from the same team as `k+1` independent clean-sheet draws. **They are not** — one match, one defence, one realised goals-against count. Model the shared outcome with a single team-defence latent:

```
clean-sheet indicator for the whole stack  =  1{ opponent scores 0 }          # a SINGLE Bernoulli, shared by all k+1 players
P(whole stack returns the CS point)         =  p_cs · Π p60(member)            # ~p_cs, lightly haircut for any rotation-risk member
```

The fantasy value of the stack is the **joint** distribution of its total defensive points, which has two parts a naive sum misses:

- **Amplified ceiling.** On the good draw (clean sheet), the stack pays `(k+1)` clean-sheet points *at once* — a correlated haul. A 3+1 stack vs a weak attack is a ~`p_cs` chance at `4 × λ_cs ≈ +16` from clean sheets alone, plus any set-piece CB goal or full-back attacking return riding on top. That correlated spike is exactly the ceiling a chaser wants and a naive independent-sum understates.
- **Shared floor.** On the bad draw (concede), they **all** blank the CS point and **all** take the concede-bracket penalty together — the stack has no internal diversification on the clean-sheet axis. A blank is a *team* blank.

Compute the bonus as the gap between the joint ceiling/variance the stack actually carries and the independent-draw approximation the rest of the EV pipeline would assume:

```
# correlation lift to the ceiling (what the joint buys over independent draws):
ceiling_lift   =  ρ · k · λ_cs(DEF) · p_cs · (1 − p_cs)         # ρ→1 within a team; grows with stack size k and with how live the CS is

# shared-downside term (the cost of zero internal diversification on the CS axis):
shared_floor   =  ρ · k · E[concede_penalty_per_player]          # the same bad draw hits all k+1 together

stack_corr_bonus =  sign(θ) · ceiling_lift  −  damp(θ) · shared_floor
```

where `ρ ≈ 1` for same-team back-line members (perfect within-team CS correlation is the modelling premise of BB2), decaying toward 0 as you split the stack across teams — **splitting a stack across nations destroys the bonus**, which is precisely why crossover keeps BB2 intact and repair downgrades enablers before breaking the spine (`building-blocks.md`).

**The θ sign flip (selection pressure):**

| θ | stack_corr_bonus treatment | football logic |
|---|---|---|
| `gain` (chasing) | `sign(θ) = +`, `damp(θ)` small → **amplify** the correlated ceiling | you need the swing; a 4-up clean-sheet haul the field's spread defences don't get is a rank earthquake |
| `protect` (leading) | `sign(θ) = +` but small, `damp(θ)` large → **discount** for the shared floor | a team blank that zeroes four of your players at once is exactly the variance a leader is trying to avoid; prefer spreading defenders |
| `neutral` | symmetric, modest | let the marginal `p_cs` EV lead; small bonus for coherence |

This makes the *same* 3+1 stack score as an asset for a chaser and as a liability for a leader — the selection-pressure dial of `fitness-function.md`, applied to the defensive module.

**Chip and building-block synergy (surface, do not decide):**
- **Clean Sheet Shield + full stack:** the chip protects CS returns (e.g. defenders keep the point despite a late goal — confirm exact rule in-game). On a **3+1 stack vs a weak attack** it turns a ~`p_cs` chance into a near-locked correlated haul *and* caps the shared floor — the single highest-leverage home for the chip (`chip-catalog.md` §4). Set `shield_fit: true` and report the lift to `p_cs` and the floor the shield would underwrite, so `wc-chip-strategist` can size the deployment.
- **BB2 coherence flag:** report whether the stack is a *real* same-team stack (≥3 from one back line + that GK) or a pseudo-stack split across teams (no ρ, no bonus) — the engine needs this to know whether crossover preserved the linkage.

---

## Output (the `clean-sheet` signal)

Emit via `wc-signal-emitter` to `signals/<round>-clean-sheet-<team>.md`:

```yaml
---
type: clean-sheet
round: <round id, e.g. 2026-grp-md2>
date: <YYYY-MM-DD>
emitted_by: wc-clean-sheet-model
confidence: <0.00–1.00>          # cap 0.35 if expected_GA rests on unconfirmed xGA/xG or scoring values
source_urls:
  - <url for team xGA / opponent xG / predicted back line / venue>   # or "manager-provided"
---

team: <team>
fixture: { opponent: <opp>, round: <round>, venue: neutral|host|home, kickoff_utc: <ts> }

expected_ga: <float>             # expected goals conceded this match (the engine quantity)
p_cs: <0.00–1.00>                # = exp(−expected_ga), refined; clean sheet is a minority outcome
p_cs_60: <0.00–1.00>             # p_cs × representative p60 (the actually-bankable CS prob for a starter)

defensive_ev:
  gk:  { cs_point: <n>, e_saves: <n>, save_points: <n>, concede_penalty: <-n>, def_ev: <n> }
  def: { cs_point: <n>, defact_floor: <n>, concede_penalty: <-n>, def_ev: <n> }   # per typical stacked DEF
  mid_partial_cs: <n>            # the MID clean-sheet floor, if relevant

concede_downside:
  e_concede_penalty_per_player: <-n>     # Poisson over goals-against × bracket; SHARED across a stack
  bracket_note: <"−1 per 2 conceded; provisional — confirm scoring-rules.md">

stack:
  composition: { team: <team>, defenders: <k>, gk: <bool> }   # the BB2 spine being priced
  is_real_stack: <bool>          # ≥3 same back line + that GK; false = split pseudo-stack (ρ→0, no bonus)
  rho: <0.0–1.0>                 # within-team CS correlation (~1 same team)
  p_stack_clean: <0.00–1.00>     # P(whole stack returns the CS point together)
  ceiling_correlated_haul: <n>   # points the stack pays AT ONCE on the good draw (e.g. (k+1)·λ_cs + set-piece spike)
  shared_floor: <-n>             # points all members lose together on the bad draw
  stack_corr_bonus: <+/- n>      # the fitness term, AFTER the θ sign flip
  theta_applied: { theta: protect|gain|neutral, k: <n> }

shield_fit: <bool>               # true = full 3+1 stack vs weak attack → prime Clean Sheet Shield slot
shield_note: <lift to p_cs and floor the chip would underwrite, for wc-chip-strategist>

assumptions:
  blend_weights: { w_def: <n>, w_att: <n> }
  adjustments_applied: [ mismatch, game_state, venue, personnel, low_block ]
  recheck_near_lock: <bool>      # true if predicted back line / keeper not yet confirmed
```

The decomposition is mandatory: `wc-fitness-eval` reads `stack_corr_bonus`, `wc-player-ev` reads the per-position `def_ev` and `concede_downside`, `wc-chip-strategist` reads `shield_fit`/`shield_note`, and the Director shows ceiling-vs-floor on the board so the manager sees both sides of the stack bet.

---

## Guardrails

- **A clean sheet is a minority outcome.** Do not let `p_cs` drift above ~0.60 without a confirmed mismatch (`mismatch_list`); above 0.65 is a flag to re-examine `expected_GA`. Big favourites still concede.
- **Never sum a stack as independent draws.** That is the exact error BB2 and this skill exist to prevent. A same-team GK + k defenders share **one** clean-sheet Bernoulli — report `p_stack_clean`, not `p_cs^(k+1)`.
- **The bonus is two-sided.** Always emit `shared_floor` alongside `ceiling_correlated_haul`. A correlation that lifts the ceiling lifts the floor's depth equally — hiding the downside would mislead a protecting manager into a single fragile bet.
- **Respect the θ sign.** If `θ` isn't supplied, ask — do not silently default to neutral on a stack-heavy candidate; the sign flip is the whole point of the term for fitness.
- **Gate on minutes.** Multiply CS-return EV by `p60` from the `scout` signal; a defender subbed at the hour is not a clean-sheet bank. A rotation-risk member also drags `ρ`-adjusted `p_stack_clean`.
- **Consume, don't re-derive.** Team xGA, opponent xG, fixture difficulty and `p_advance` come from the `fixture` signal; injuries/minutes from the `scout` signal. Re-deriving them violates `signal-framework.md` and risks contradicting an upstream agent.
- **Confidence discipline.** World Cup samples are tiny and the 2026 scoring values are provisional (`scoring-rules.md confirmed: false`). If `expected_GA` rests on unconfirmed xGA/xG or the clean-sheet point value is unverified, cap `confidence ≤ 0.35` and set `recheck_near_lock: true` until the back line and keeper are confirmed.

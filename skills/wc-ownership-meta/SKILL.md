---
name: wc-ownership-meta
description: Models the FIFA World Cup Fantasy field — effective ownership, the template set, the differential list, and the rank-protect-vs-gain leverage math — so the system reasons about "what will most managers do?" rather than raw points. Computes effective ownership EO = field_ownership% x (1 + captaincy_share), classifies every owned/missed player into the three regimes (own high-EO haul = hold station, MISS high-EO haul = drop hard, own low-EO haul = leap the field), builds the template set and differential list, flags where the field is over-concentrated (fade ops) and under-reacting (get-there-first), and returns the ownership_leverage contribution under the rank objective θ that wc-fitness-eval folds into fitness. Also computes mini-league rival-relative leverage. Emits an `ownership` signal. Use when called by wc-ownership-analyst, by the strategists weighting picks by leverage, and by wc-fitness-eval scoring the rank term.
---

# wc-ownership-meta — effective ownership, the field model, and the leverage math

Implements `footballfantasy/context/frameworks/game-theory-meta.md`. This game is scored against the whole field at once, not a weekly opponent, so the entire opponent collapses into one number per player: **ownership.** This skill is the engine that turns ownership into the rank-relative leverage the system runs on — the `ownership_leverage` term in `wc-fitness-eval`, the differential/cover read on the decision board, and the per-pick leverage multiplier the strategists weight by.

The one sentence that governs everything below: **rank moves on the gap between your points and the field's points, so what matters is never "did my player score?" but "did my player score relative to what the field owns?"**

`wc-ownership-analyst` calls this to build its read; the strategists call it to weight picks; `wc-fitness-eval` calls it for the rank term. Never re-derive ownership downstream — read this skill's `ownership` signal.

## Workflow

```
- [ ] 1. Gather field ownership% per relevant player (web search — public ownership trends) and captaincy share for the round
- [ ] 2. Compute EO = field_ownership% x (1 + captaincy_share) for every player in play; classify each into the 3 regimes vs our squad
- [ ] 3. Build the TEMPLATE SET (high-EO core you cannot afford to miss) and the DIFFERENTIAL LIST (live-ceiling low-ownership picks)
- [ ] 4. Run the FIELD MODEL — project "what will most managers do?" this round; flag over-concentration (fade) and under-reaction (get-there-first)
- [ ] 5. Compute ownership_leverage(c | θ) for wc-fitness-eval: cover-penalty when θ=protect, differentiate-reward when θ=gain
- [ ] 6. Overlay mini-league rival-relative leverage (block a rival you lead; match a rival's punt you trail)
- [ ] 7. Emit the `ownership` signal with field_ownership, effective_ownership, template_set, differential_list, and the flags
```

---

## Method

### 1. Effective ownership (the master signal)

Captaincy doubles a player's points, so a player the field both *owns and captains* hurts your rank far more if you miss him than one merely owned. EO folds the captaincy multiplier into ownership:

```
EO[player] = field_ownership%[player] x (1 + captaincy_share[player])
```

where `captaincy_share` = the fraction **of owners** who captain him this round (0–1), web-searched from captaincy-poll trends or estimated from the chalk-captain logic in §4.

**Worked example.** A forward owned by 50% of the field, captained by 30% of those owners:
`EO = 50 x (1 + 0.30) = 65%`. Effectively 65% of the field's *scoring exposure* sits on this player once the armband is counted. A 40%-owned mid captained by only 5% of owners: `EO = 40 x 1.05 = 42%` — heavily owned but not a captaincy threat, so missing him costs floor, not the doubled swing. A 6%-owned differential captained by 1% of its owners: `EO ≈ 6.06%` — missing him costs almost nothing to your rank; owning *and* it hauling is where rank is won.

EO is the quantity every other section consumes. It is capped conceptually at the doubling ceiling (a player 100% owned and 100% captained has EO = 200%, i.e. the field's entire doubled exposure).

### 2. The three regimes (classify every player vs our squad)

For each player, cross "do we own him?" with "is his EO high or low?" and read the rank consequence of a haul:

| Our holding | Player EO | If he HAULS | Read |
|---|---|---|---|
| **We own** | **high-EO** | We **hold station** — everyone else got it too | Necessary to not fall behind; insufficient to climb. This is the cost of staying in the race. |
| **We MISS** | **high-EO** | We **drop, hard** | The template-protection risk. The single reason a leader covers chalk. The doubled chalk captain we don't own is the classic lead-killer. |
| **We own** | **low-EO** | We **leap the field** | Where rank is won. The differential. One of these per round jumps thousands of places. |
| We own | low-EO | (he blanks) | Costs us almost nothing vs the field — the field didn't have him either. The cheap downside that makes differentials asymmetric. |

High vs low EO is relative to the round's distribution, not a fixed cutoff: treat the top decile of EO as **template-grade** (miss-risk dominates), and anything below ~10–15% EO as **differential-grade** (leap-potential dominates). The middle band is contested — own it if cheap, fade it if it crowds out a sharper differential.

The sign of the leverage flips with the rank objective (cover the high-EO regime when protecting; hunt the low-EO regime when gaining) — formalised in §5.

### 3. The template set and the differential list

These are the two lists every consumer reads off this signal.

**TEMPLATE SET** = the high-EO core you cannot afford to *miss* when protecting. Construction:
- Rank all players by EO; take everyone in the template-grade band (top-decile EO, plus any player whose `captaincy_share` alone makes him a doubled-haul threat even at moderate ownership).
- For each, record `EO`, `miss_risk` = `EO x ceiling[player]` (the rank damage if he hauls and we're not on him — ceiling from the player-ev signal), and whether **we currently cover him**.
- The template set is the protect-objective shopping list: every uncovered member is a fitness penalty under `θ=protect` (§5). The chalk captain is its most important single entry.

**DIFFERENTIAL LIST** = the live-ceiling, low-ownership picks that *gain* rank when chasing. Construction:
- Filter to differential-grade EO (sub ~10–15% EO, ideally sub-10% field ownership).
- Keep only those with a **live ceiling this round** — a real route to a haul (penalty taker, set-piece threat, nailed starter with xGI vs a weak opponent, a clean-sheet defender from a favourite vs a minnow). A low-owned player with no ceiling is not a differential, just an unowned bad pick.
- Score each on `leap_value` = `ceiling[player] x (1 − EO[player])` — the rank-gain weight, high when the ceiling is real and the field isn't there. This is exactly the weight `θ=gain` rewards in §5.
- Rank descending; this is the gain-objective shopping list.

A picked-over differential (one whose ownership is *rising* round on round — see §4 under-reaction) is annotated "closing": its leverage decays as the field arrives, so its value is highest **now**.

### 4. The field model — "what will most managers do?"

The field is predictable in aggregate. Project its likely moves each round from four regularities, then flag the two exploitable distortions.

**The four regularities:**
1. **Chalk concentrates on in-form big-nation players.** Ownership piles onto the form attackers from the largest, most-watched nations (the Brazils, Frances, Englands, Argentinas). Project ownership *up* on any such player riding a goal narrative; project it *down* on equivalent producers from smaller nations the casual field overlooks.
2. **The obvious chalk captain is the premium attacker vs the weakest opponent.** The field's captaincy concentrates on the biggest name facing the softest defence on the slate. Estimate `captaincy_share` for that player high (often 25–40%+) even before polls confirm; this is usually the single highest-EO entry in the template set.
3. **Ownership LAGS reality by ~a round.** The field is slow to react to fixture swings and rotation news — a player whose fixtures just turned, or who just won a starting role, is under-owned *this* round and will be chalk *next* round. This lag is the core exploit: **get to the fixture/rotation edge before the field does.**
4. **In knockouts ownership COMPRESSES onto survivors.** As nations are eliminated, the field's squads converge onto the 8–16 surviving favourites; ownership concentrates, differentials get scarce and precious, and EO on the surviving stars climbs toward saturation. Differential value rises in knockouts precisely because there are fewer live differentials to go around.

**The two flags (the deliverable):**
- **field_concentration_flags (FADE ops).** Where the field is *over-concentrated* — a player (especially a captain) carrying EO so high that if he blanks, simply **not owning him gains you rank** while the field stalls. A 40%-captained forward against a defence that is tougher than its reputation is the textbook fade: the field is paying full chalk price for a coin-flip. Flag the player, his EO, the reason the concentration is mispriced, and the rank gained if he blanks.
- **under_reaction_flags (GET-THERE-FIRST ops).** Where the field is *under-reacting* — a fixture swing, a rotation/role change, an injury return, a newly-confirmed penalty duty the field hasn't priced yet. These are tomorrow's chalk at today's differential ownership. Flag the player, the catalyst, current vs projected-next-round ownership, and the "buy now" window before the lag closes.

These two flags are the actionable output of the field model: fade the over-loved chalk, front-run the under-reacted edge.

### 5. ownership_leverage(c | θ) — the rank term for wc-fitness-eval

`wc-fitness-eval` calls this skill for the rank term in `fitness(c | θ)`. The sign and shape are set entirely by the rank objective θ (the protect-vs-gain dial, identical to the fitness selection-pressure dial). For a candidate `c`:

**θ = protect (leading the mini-league) — cover-penalty.** Penalise being *underweight* the template. Missing a haul the field captained drops you; owning it only holds station. So fitness rewards covering chalk:

```
ownership_leverage(c | protect) = − w_protect · Σ_{p ∈ template_set, p ∉ c} miss_risk[p]
                                = − w_protect · Σ_{uncovered template p} EO[p] · ceiling[p]
```

Every uncovered template member subtracts; the chalk captain (highest `EO·ceiling`) dominates the sum. A protect-candidate scores well by leaving no high-EO haul uncovered.

**θ = gain (chasing) — differentiate-reward.** Reward being *overweight* low-ownership pieces with live ceilings. A differential haul the field doesn't own is where rank is won:

```
ownership_leverage(c | gain) = + w_gain · Σ_{p ∈ differential_list, p ∈ c} leap_value[p]
                             = + w_gain · Σ_{owned differential p} ceiling[p] · (1 − EO[p])
```

Every owned, live-ceiling differential adds; the term is largest when the ceiling is real and EO is near zero. A gain-candidate scores well by carrying differentials the field is not on.

**θ = neutral (mid-table / early) — small symmetric term.** A light version of both, scaled down, mostly deferring to raw xEV:

```
ownership_leverage(c | neutral) = ½ · [ gain-term(c) + protect-term(c) ] · w_neutral   (w_neutral small)
```

`w_protect`, `w_gain`, `w_neutral` are the leverage weights; they scale with how extreme the standing is, mirroring fitness's `k` (a big lead with few rounds left pushes `w_protect` high; a large deficit late pushes `w_gain` high). Return the chosen weight and the per-player breakdown so `wc-fitness-eval` can show the decomposition on the board — never just a bare number.

### 6. Mini-league rival-relative leverage (the real objective)

The global field sets ownership, but the manager's prize is the **mini-league of friends** (`context/manager-profile.md`, `context/rivals/`). Against a handful of named rivals the calculus sharpens, and can *override* the global read. Using whatever we can see of rival squads (coarse — only what's visible):

- **You LEAD a rival → block, even beyond global EO.** Overweight to match the rival's high-EO pieces specifically. You cannot lose ground to a haul you both own. Mirror their captain and their template stars even if global EO alone wouldn't justify it — the goal is to deny them a swing relative to *you*, not to the global field.
- **You TRAIL a rival → match their punt.** If a rival above you owns a big differential you don't, covering the global field is not enough — you may need to *match their specific risk* to have a live path past them. Add their differential to your differential list with a rival-relative bonus, even if its global leap_value is modest, because the only points that matter are points relative to *that rival*.
- **Mini-league tight, late → pure rival-leverage.** With few rounds left and the table close, the right play can be a leverage move computed purely against the rivals' squads, not the global field. Compute a per-rival `block_set` (their high-EO pieces to mirror when ahead) and `chase_set` (their differentials to match when behind), and let these override the global template/differential lists where they conflict.

Emit the rival-relative overlay alongside the global lists so the strategists and `wc-fitness-eval` can apply whichever the standing demands. When rival squads are only partially visible, mark the overlay's confidence accordingly (§Guardrails).

---

## Output — the `ownership` signal

Emit via `wc-signal-emitter` (validated against `signal-framework.md`; type `ownership`, consumed by `wc-fitness-eval` and the strategists).

```yaml
---
type: ownership
round: <round id, e.g. 2026-grp-md2>
date: <YYYY-MM-DD>
emitted_by: wc-ownership-meta
confidence: <0.00–1.00>          # cap per Guardrails when ownership is estimated / national-only
source_urls:
  - <ownership-trend source url>   # or manager-provided
---

objective: { theta: protect|gain|neutral, leverage_weight: <w> }

field_ownership:                   # field ownership %, 0–100, web-searched
  <player>: { own_pct: <0–100>, captaincy_share: <0–1>, source: <url|estimated|manager-provided> }

effective_ownership:               # EO = own_pct x (1 + captaincy_share)
  <player>: <EO 0–200>

template_set:                      # high-EO core you cannot afford to MISS (protect shopping list)
  - player: <name>
    EO: <0–200>
    miss_risk: <EO x ceiling>
    we_cover: <true|false>
    is_chalk_captain: <true|false>

differential_list:                 # live-ceiling low-ownership picks (gain shopping list)
  - player: <name>
    EO: <0–200>
    own_pct: <0–100>
    leap_value: <ceiling x (1 − EO)>
    ceiling_basis: <pen taker | set-piece threat | CS defender vs weak attack | xGI vs soft opp>
    trend: <stable|closing>        # "closing" = ownership rising, value is highest now

field_concentration_flags:         # FADE ops — over-loved chalk; not owning gains rank if he blanks
  - player: <name>
    EO: <0–200>
    why_mispriced: <one line — fixture tougher than reputation, coin-flip captain, etc.>
    rank_gain_if_blank: <qualitative or estimated>

under_reaction_flags:              # GET-THERE-FIRST ops — field hasn't priced the catalyst yet
  - player: <name>
    catalyst: <fixture swing | role/rotation change | injury return | confirmed pen duty>
    own_now: <0–100>
    own_projected_next: <0–100>
    buy_window: <this round | before [event]>

ownership_leverage:                # the term wc-fitness-eval folds into fitness, with breakdown
  theta: protect|gain|neutral
  value: <+/- n>
  per_player: { <player>: <+/- contribution> }

rival_overlay:                     # mini-league rival-relative leverage (overrides global where it conflicts)
  - rival: <name>
    standing_vs_us: ahead|behind
    block_set: [<their high-EO pieces to mirror — when we lead>]
    chase_set: [<their differentials to match — when we trail>]
    visibility: full|partial        # how much of their squad we can actually see
```

---

## Guardrails

- **Ownership is web-searched or estimated — cite the trend.** There is no ownership API here. Every `own_pct` and `captaincy_share` traces to a public ownership-trend source URL or is marked `estimated` / `manager-provided`. An ownership table with no source is not persisted as fact.
- **National ≠ game ownership → cap confidence.** If only *national-team* popularity is available (how popular the nation is) but not actual in-game selection %, that is a proxy, not the signal. Mark those entries `estimated` and **cap the signal confidence at 0.35** with a "needs ownership confirmation before lock" flag — per the load-bearing-fact rule in `signal-framework.md`. Do not let a guessed ownership number drive a high-confidence fade.
- **EO not raw ownership for any rank read.** A player heavily owned but rarely captained is a different rank object from a heavily-captained one. Always pass EO (with the captaincy share) downstream, never bare ownership — the captaincy multiplier *is* the leverage.
- **Leverage sign must flip with θ.** Cover-penalty under protect, differentiate-reward under gain. If the same candidate's `ownership_leverage` doesn't change sign between a leader and a chaser, the term is mis-wired (the symmetric check `wc-fitness-eval` relies on).
- **A differential needs a live ceiling.** Never list a low-owned player as a differential without a concrete route to a haul this round (pen/set-piece/role/fixture). Low ownership alone is not an edge — it is just an unowned bad pick.
- **Mini-league overrides the global field when they conflict** — the prize is the friends' table, not the global percentile. But mark `rival_overlay.visibility` honestly: rival squads are only partially observable, so rival-relative leverage carries lower confidence than global EO and must say so.
- **Read, don't re-derive.** Ceilings come from the `player-ev` signal and clean-sheet probabilities from `clean-sheet`; do not recompute them here — this skill turns *ownership* into leverage, nothing else.

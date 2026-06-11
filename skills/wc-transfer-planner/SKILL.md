---
name: wc-transfer-planner
description: Plans between-round FIFA World Cup Fantasy transfers — budgets the round's free transfer(s), forces out players whose nation has been eliminated, chases fixture-swing drops, upgrades on value, and decides when a rebuild is large enough to fire the Wildcard instead of spending free transfers one at a time. Ranks candidate in/out pairs by EV gain over each player's remaining survival horizon (delta xEV weighted by progression_carry) MINUS transfer cost (a free transfer is cheap, a points hit is real, churning the squad for marginal swings is a critic flag), and tags forced/fixture/upgrade priority. Emits a `transfer-plan` signal. Use when called by wc-squad-architect (whose transfer work this skill is the engine for) and by the strategists in the populate stage when their candidate is transfer-adjacent rather than a full rebuild.
---

# wc-transfer-planner — between-round transfer optimisation

The engine behind `wc-squad-architect`'s transfer work. Given the current 15 and the round's signals, it answers four questions in priority order: **who is dead weight and must go** (eliminated nations), **where the fixtures are swinging** (chase the drop), **where value is left on the table** (upgrade), and **is the rebuild big enough that the Wildcard beats spending free transfers**. It does not pick the squad and it does not present a board — it ranks in/out pairs, budgets the free transfer(s), prices any hit, and recommends (or rejects) the Wildcard, then emits a `transfer-plan` signal for `wc-squad-architect` and the Director to act on.

The discipline that defines this skill: **a transfer is only worth making if its EV gain over the horizon the player will actually survive exceeds its cost.** Two failure modes sit on either side of that line — *under-trading* (leaving an eliminated player in the squad to rot) and *over-trading* (transfer thrash: churning the squad chasing every one-band fixture wobble, burning free transfers and paying hits for swings the field hasn't even priced). This skill exists to find the moves that clear the bar and stop at the ones that don't.

This is between-round, transfer-adjacent search. A *structural* rebuild — most of the squad re-pointed at the surviving nations at the group→knockout transition — is not a transfer plan; it is a Wildcard, and the whole candidate space reopens to the full market (`chip-catalog.md` §1). The rule for when the rebuild crosses that threshold is below.

## When to invoke

- `wc-squad-architect` is this skill's primary caller: it runs the transfer plan whenever the between-round window is open, then folds the result into its `transfer-plan` signal and the squad it carries to the board.
- A `wc-strategist` genotype calls it when its candidate is an *evolution from the current squad* (a few moves) rather than a from-scratch build — A4 (Fixture Exploiter) especially, whose whole thesis is rotating toward the steepest fixture drops via transfers. The skill returns a neutral EV-ranked pair list; the archetype tilt (how aggressively to chase variance, whether to pay a hit) happens in the caller.
- It does **not** run on a Wildcard round — when the Wildcard fires, the population is re-seeded from the full market via `wc-squad-architect` (build-squad), not evolved one transfer at a time. This skill's job on such a round is the *recommendation to fire the Wildcard*, after which it hands off.

## Workflow

```
- [ ] 1. Read state: FT count this round, whether extra transfers cost points, budget, nation cap, in-the-bank — from tournament-state.md. Read each owned player's elimination-risk horizon.
- [ ] 2. Read signals (never re-derive): the round `fixture` signal (swing_calendar, p_advance, mismatch_list, dead_rubber_flags) and the `player-ev` signals for owned players and transfer targets. Read `ownership` if differentiating.
- [ ] 3. FORCED MOVES — list every owned player whose nation is eliminated (p_advance = 0). These are dead weight: zero future xEV. Mark each a forced OUT for the next window.
- [ ] 4. SWING MOVES — from swing_calendar, list owned players hitting an easy→hard flip (sell) and market targets hitting a hard→easy flip (buy), respecting each one's elimination horizon.
- [ ] 5. UPGRADE MOVES — find in/out pairs where a target's horizon-weighted xEV beats an owned player's at affordable cost (value left on the table).
- [ ] 6. SCORE every candidate in→out pair: net_gain = ΔxEV_horizon − transfer_cost. Rank by net_gain. Tag each pair forced | fixture | upgrade.
- [ ] 7. BUDGET the free transfer(s): assign FTs to the highest-net-gain pairs first (forced moves take precedence even at equal gain). Price any pair beyond the FT count as a hit; keep it only if net_gain still clears the hit.
- [ ] 8. WILDCARD CHECK — count the moves that genuinely clear the bar. If the rebuild scope crosses the Wildcard threshold (rule below), recommend the Wildcard instead of free transfers + hits, and hand off to build-squad.
- [ ] 9. Repair: confirm the post-transfer 15 stays feasible (budget, nation cap, formation) per building-blocks.md repair order. Flag if a move breaks a building block.
- [ ] 10. Emit the `transfer-plan` signal (ordered pairs, FT usage, any hit + its justification, Wildcard recommendation) via wc-signal-emitter. Return its path.
```

## Method

### 0. Read the round's transfer budget (state first — it sets the whole cost side)

From `tournament-state.md`:
- **`free_transfers_this_round`** — how many moves are free. **Confirm the count from the live game** (`league-config.md` §Transfers leaves it to be confirmed) and whether free transfers **carry over** when unused. Before the tournament: transfers are unlimited (build freely — no plan needed). Between rounds: the granted free count is the cheap budget.
- **Does an extra transfer cost points?** This is the other load-bearing rule to confirm. Two regimes, and the plan changes shape between them:
  - **Hit regime (FPL-style):** each transfer beyond the free count costs a fixed **−points** (commonly −4). A hit is a real, paid cost — a move must out-gain it to be worth taking.
  - **Hard-cap regime:** extra transfers are simply *not allowed* (capped at the free count). Then there is no hit to price; the constraint is integer — you get exactly `free_transfers_this_round` moves and rank-and-cut to that many.
  - Until the game confirms which regime applies, **plan under both** and flag the assumption on the signal (cap confidence at 0.35 on the cost side, per `signal-framework.md`).
- **Budget and in-the-bank** — group $100.0m / knockout $105.0m (`league-config.md`); `in_the_bank = budget − squad_value`. Prices are **fixed all tournament** (no rises/falls), so there is no price-rise meta-game to race — value is captured at purchase, and a transfer's only cost is the FT/hit, never a price change.
- **Nation cap** — 3 in the group stage, loosening per round in the knockouts (confirm the per-round number in-game). Every in/out pair must keep the squad under the current cap.
- **Each owned player's elimination-risk horizon** — the round their nation could be knocked out, from the `fixture` signal's `p_advance` ladder, mirrored in `tournament-state.md`. This is the clock on every asset and the denominator of every EV-gain calculation.

### 1. The EV-gain-minus-cost model (the core ranking)

A transfer replaces an owned player `out` with a target `in`. Its worth is the extra expected points it buys **over the rounds the *new* player will actually survive to play**, minus what the move costs:

```
ΔxEV_horizon(in, out) =  Σ_{r = next .. H}  [ xEV(in, r) · P(in's nation alive at r)
                                            − xEV(out, r) · P(out's nation alive at r) ] · discount^r

net_gain(in, out)     =  ΔxEV_horizon(in, out)  −  transfer_cost
```

- **`xEV(player, r)`** is read from the player's `player-ev` signal for the immediate round and projected forward for later rounds (the same per-round distribution `wc-fitness-eval` sums). **Never re-derive it** — read the signal; if a target has no `player-ev` signal yet, `wc-scout` → `wc-player-ev` must run first.
- **`P(nation alive at r)`** is the `p_advance` survival ladder from the `fixture` signal (`p_reach(R) = Π p_win_tie`). This is the **`progression_carry` weighting** from `fitness-function.md` applied to *both sides of the trade*: the gain from a fixture-swing pickup decays if that player's nation is itself elimination-exposed, and selling a player on a likely semi-finalist forfeits several future rounds, not one. A single-round fixture edge that buys a player whose nation may be gone next week is mostly illusory — this term is what catches that.
- **`discount^r`** — mild horizon discount (uncertainty compounds; near rounds are firmer than far ones), matching the fitness function's `progression_carry` discount. Weight the near round heaviest.
- **`H`** is the horizon: in the group stage, the remaining matchdays; in the knockouts, the bracket path weighted by `p_reach`. Do not project EV gain past the round either player's nation is realistically eliminated — that is phantom value.

**`transfer_cost`:**
- A move funded by a **free transfer**: cost ≈ 0 (the FT is the cheap budget; the only "cost" is consuming one of a scarce resource that could fund a better move later — a small opportunity weight, not a points charge).
- A move that **takes a hit** (hit regime): `transfer_cost = hit_points` (e.g. 4). The move must clear it: `ΔxEV_horizon > hit_points`. A −4 hit for a +2-over-the-horizon upgrade is **−EV** and a critic flag.
- In the **hard-cap regime**: no hit exists; instead you have an integer budget of `free_transfers_this_round` and simply take the top-`k` net-gain pairs.

### 2. Priority classes — what to do, in order

Every candidate pair is tagged with exactly one class. Classes set precedence when free transfers are scarce: a **forced** move outranks a **fixture** move outranks an **upgrade** at comparable net gain, because the forced move's *out* player has collapsed to zero future value.

**(1) FORCED — eliminated-player replacement (highest priority).**
A player whose nation is **eliminated** (`p_advance = 0` in the `fixture` signal) is **dead weight**: his `xEV(out, r)` is zero for every future round — he cannot score, cannot be captained, cannot fill an XI slot. Leaving him in the squad is strictly dominated; he must be transferred **out next window**. Because `xEV(out)` over the horizon is ~0, *any* viable replacement has a large positive `ΔxEV_horizon`, so forced moves almost always clear the bar even on a hit — but spend a **free transfer** on them first, because they are the cheapest large gains available. (Distinguish *eliminated* — a hard forced move — from *elimination-risk* — a nation that *could* go out soon, which is a fixture/horizon consideration, not yet forced. Also distinguish the **dead-rubber** flag: a clinched team resting starters in a final group game is a one-round minutes problem, not an elimination — discount that fixture's xEV, but do not force the player out.)

**(2) FIXTURE-SWING — chase the difficulty drop (second priority).**
From the `fixture` signal's `swing_calendar` (built by `wc-fixture-progression`):
- **Easy→hard swing on an owned player (sell signal):** an owned attacker whose nation runs into a `fd_att` 4–5 fixture, or a defender into a `fd_def` 4–5 (shootout) game — transfer out *before* that round, into a player with a kinder draw. But check the **elimination horizon first**: do not pay to dodge a future hard fixture in a knockout nation whose own elimination-risk round arrives *before* the swing — the move is moot (coordinate with `tournament-state.md`; the swing calendar already carries an `elimination_caveat`).
- **Hard→easy swing on a market target (buy signal):** a player from a team coming *into* a `fd_att` 1–2 or `fd_def` 1–2 run — and a `mismatch_list` favourite (powerhouse-vs-minnow) is the sharpest case: its attackers become captain candidates and its defenders clean-sheet locks. The field **lags fixture turns by ~a round** (`game-theory-meta.md` §4), so move a round *early*, before ownership rises, to bank value the field hasn't priced — the swing's `plan_ahead_lead` says how early. This is the A4 Fixture Exploiter move; the EV gain is the `ΔxEV_horizon` from the better fixture.
- **The thrash guard lives here:** a swing of only **one** difficulty band, or a swing into a fixture the player's nation may not survive to, rarely clears a hit and often doesn't justify burning a scarce free transfer. Require a swing of **≥2 bands** (the `wc-fixture-progression` swing threshold) *and* a positive horizon-weighted `ΔxEV` *after* cost before chasing it.

**(3) UPGRADE ON VALUE — bank the EV left on the table (third priority).**
With forced and fixture moves placed, look for pairs where a target's horizon-weighted xEV simply beats an owned player's at an affordable price — funded by `in_the_bank` plus the price of the player sold. These are the value plays: a higher-floor pen-taker for a non-taker, a nailed starter for a rotation risk (`p60` gap), a deep-run nation's asset for a coin-flip nation's (`progression_carry` gap). They are lowest priority because the *out* player still has positive value — the gain is the **margin**, which must beat the cost. An upgrade is only worth a **hit** if `ΔxEV_horizon` over the remaining rounds comfortably exceeds the hit (a multi-round upgrade can; a one-round +1 cannot).

### 3. Budgeting the free transfer(s) and pricing hits

1. Rank all candidate pairs by `net_gain`, with the priority class as the tie-breaker (forced > fixture > upgrade at comparable gain).
2. **Assign the free transfer(s) to the top pairs** — forced moves first (cheapest large gains), then the highest-net-gain fixture/upgrade pairs, until the free count is exhausted.
3. **For each additional pair beyond the free count:**
   - *Hard-cap regime:* stop — you are out of moves. Carry the rest to next window (and note any unused FT if the game allows carry-over: an unused free transfer banked for a bigger move next round can be worth more than a marginal move now — do not spend a free transfer just because it exists).
   - *Hit regime:* take the hit **only if `ΔxEV_horizon > hit_points` with margin.** A forced move (eliminated player) is the one case that routinely justifies a hit, because the *out* side is zero. A speculative upgrade rarely is. Every hit on the plan carries an explicit justification (the horizon-weighted gain that beats it); an unjustified hit is a critic kill.
4. **Never burn a free transfer on a marginal swing.** A free transfer is a scarce, renewable-but-limited resource; spending it on a +1-over-one-round move forecloses funding a forced or value move next window. If the best available move's net gain is small and no forced move is pending, **the correct plan can be zero transfers** — bank the move.

### 4. The Wildcard threshold — when to stop transferring and rebuild

The Wildcard gives **unlimited transfers for one round** (`chip-catalog.md` §1) — a free full rebuild. Spending free transfers one at a time (and paying hits) to patch a squad that needs *many* changes is strictly worse than one Wildcard that re-points everything at once. So the decision is **scope**: how many moves does the squad genuinely need?

Recommend the **Wildcard** when the rebuild scope crosses the threshold:

- **Count `N_needed`** = the number of pairs that genuinely clear the bar this window and over the next 1–2: forced moves (eliminated players) + high-confidence fixture-swing moves + value upgrades whose horizon gain beats their cost.
- **The canonical trigger — the group→knockout transition** (`chip-catalog.md` §1, `CLAUDE.md` cadence): budget jumps to **$105m**, the nation cap **loosens**, and roughly half the nations are eliminated at once — so a large slice of the squad is simultaneously dead weight *and* the affordable market just changed. This almost always wants the Wildcard. **Do not** drip eliminated players out across the first knockout rounds at one free transfer (and a string of hits) each — re-point the whole squad in one move.
- **The mid-group trigger** — a round where a **cluster** of your players hit dead fixtures or eliminations *simultaneously* and a patch-by-patch plan can't keep up (`chip-catalog.md` §1).
- **The numeric rule of thumb:** if `N_needed ≥ ~4–5` moves (and especially if executing them with free transfers would require **paying hits** across this window and next), the Wildcard's value — `Σ net_gain of all needed moves` with **zero transfer cost** — beats free-transfers-plus-hits. Compare explicitly:
  ```
  value(Wildcard)        = Σ ΔxEV_horizon over ALL needed moves     (transfer_cost = 0, unlimited)
  value(free transfers)  = Σ ΔxEV_horizon over the moves you can afford this window
                           − Σ hits paid to exceed the free count
                           − (deferred gain lost on moves you must postpone)
  → recommend Wildcard when value(Wildcard) − value(free transfers) > 0
    AND no later round has a clearly higher-leverage Wildcard use queued (don't spend the
        one Wildcard on a 4-move group patch if the KO transition rebuild is imminent).
  ```
- **Anti-pattern (from the catalog):** burning the Wildcard early to chase **one** hot player. The Wildcard is for a **structural rebuild**, not a tweak — for a one-or-two-move need, use free transfers. And **never carry the Wildcard unused into the semi-finals** (`chip-catalog.md` golden rule): if it is still in hand late and a multi-move need appears, that is the moment.
- **Hand-off when recommending the Wildcard:** the candidate space is the **full market** again, not transfer-adjacent squads (`chip-catalog.md` §1) — the strategist population must be **re-seeded from scratch** via `wc-squad-architect` build-squad, not evolved from the current 15. This skill's output in that case is the *recommendation + the rationale (`N_needed`, the value comparison)*, and it defers the actual rebuild to build-squad. Coordinate the timing with `wc-chip-strategist` (`wc-chip-timing`) — the chip ledger owns the deployment plan; this skill proposes the fire, the chip-strategist confirms the leverage, the manager fires.

### 5. Repair — keep the post-transfer squad feasible

After applying the chosen pairs, the new 15 must still satisfy the constraint layer (BB6 in `building-blocks.md`). Run the **repair operator** in its priority order — **formation, then nation cap, then budget, then matchday spread** — preserving value-bearing blocks:
- A transfer that takes the squad over the **nation cap** (e.g. loading a third-then-fourth player from a favourite at the KO transition before the cap has loosened to allow it) must be repaired by swapping the **lowest-EV** offender, preferring to move a BB5 enabler or BB4 differential over a BB1/BB2 value piece.
- A transfer that breaks a **building block** — selling one defender out of a 3+GK Clean-Sheet Spine (BB2) and shattering the within-team clean-sheet correlation, or stripping an enabler that funds the Captain Core (BB1) — is a **repair invariant violation**: flag it. Such a move's true cost includes the block it breaks, not just the FT; usually the block should be transferred **as a unit** (sell the whole spine, rebuild a new one) or not touched. If a single transfer can only be made feasible by gutting a block, that is a signal the move is wrong — surface it rather than mangling the squad.
- Confirm at least one valid **formation** (2-5-5-3 shape yielding a legal XI) survives every pair.

## Output — the `transfer-plan` signal

Emit via `wc-signal-emitter` to `signals/<round>-transfer-plan.md`. Per the registry (`signal-framework.md`), the `transfer-plan` type is carried by `wc-squad-architect`; when this skill runs standalone it emits the same shape with `emitted_by: wc-transfer-planner`.

```yaml
---
type: transfer-plan
round: <round id, e.g. 2026-grp-md3>
date: <YYYY-MM-DD>
emitted_by: wc-squad-architect | wc-transfer-planner
confidence: <0.00-1.00>          # ≤0.35 if FT count / hit-regime / a target's minutes are web-unconfirmed
source_urls:
  - <fixture signal path>        # swing_calendar, p_advance, mismatch_list
  - <player-ev signal paths for in/out players>
  - <url confirming free-transfer count and hit rule>   # or "manager-provided"
provisional_cost_rule: <true|false>   # true until the live game confirms hit vs hard-cap regime
---

state:
  phase: <group-mdN | r32 | r16 | qf | sf | final>
  free_transfers_this_round: <n>          # confirmed from game; note carry-over if applicable
  extra_transfer_rule: hit | hard_cap | unconfirmed
  hit_points: <n | n/a>                   # e.g. 4 in the hit regime
  budget: <100.0 | 105.0>
  in_the_bank: <m>
  nation_cap: <current-phase cap>

forced_moves:                              # eliminated nations — dead weight, OUT next window
  - out: { player: <name>, nation: <nation>, reason: "nation eliminated (p_advance 0)", future_xEV: 0 }
    in:  { player: <name>, nation: <nation>, price: <m>, xEV_next: <n> }
    delta_xEV_horizon: <n>
    class: forced
    funded_by: free_transfer | hit

ranked_pairs:                              # all candidate in/out pairs, best net_gain first
  - rank: <n>
    out: { player: <name>, nation: <nation>, price: <m>, horizon_xEV: <n>, elim_risk_round: <round|none> }
    in:  { player: <name>, nation: <nation>, price: <m>, horizon_xEV: <n>, elim_risk_round: <round|none> }
    delta_xEV_horizon: <n>                 # Σ (in − out) · P(alive) · discount over H
    transfer_cost: <0 | hit_points>
    net_gain: <delta_xEV_horizon − transfer_cost>
    class: forced | fixture | upgrade
    swing_ref: <swing_calendar round + direction, if class=fixture>
    rationale: <one football-literate line — fixture drop / minutes upgrade / pen-taker / deep-run carry>

plan:                                      # the recommended moves this window
  transfers:
    - { out: <name>, in: <name>, funded_by: free_transfer, net_gain: <n> }
  free_transfers_used: <n> / <available>
  hits_taken: <n>
  hit_justification: <the horizon gain that beats each hit, or "none — no hit taken">
  no_move_recommended: <true|false>        # true when the best net_gain is marginal and no forced move pends — bank the FT
  feasible_after: { formation: <y/n>, nation_cap: <y/n>, budget: <y/n> }
  block_warnings: [ <e.g. "this pair breaks the Norway BB2 spine — sell as a unit or hold"> ]

wildcard:
  recommend: <true|false>
  N_needed: <n>                            # moves that genuinely clear the bar this window + next
  trigger: group_to_KO_transition | dead_fixture_cluster | none
  value_wildcard: <Σ ΔxEV_horizon over all needed moves, cost 0>
  value_free_transfers: <Σ affordable ΔxEV − hits − deferred gain>
  rationale: <why the rebuild does/doesn't cross the threshold>
  handoff: <"re-seed population from full market via wc-squad-architect build-squad" if recommend=true>
  defer_to: wc-chip-strategist            # chip ledger owns deployment; manager fires
---
```

Every numeric field declares its meaning so the emitter can range-check it (`signal-framework.md`). The Director routes this to `wc-squad-architect` and onto the board; the manager decides — this skill never auto-commits a transfer.

## Guardrails

- **An eliminated player is a forced move — out next window.** A player whose nation is knocked out has zero future xEV and cannot be captained, scored, or fielded. Leaving him in is strictly dominated. Spend a free transfer on him first; take a hit if no free transfer remains and the replacement clears it (it almost always does, since the out side is zero). Distinguish *eliminated* (forced) from *elimination-risk* (a horizon consideration) from *dead-rubber* (a one-round minutes discount, not a forced sale).
- **Don't burn free transfers on marginal swings (the thrash guard).** A one-band fixture wobble, or a swing into a fixture the target's nation may not survive to, rarely clears the cost of a scarce free transfer — let alone a hit. Require a **≥2-band** swing *and* a positive horizon-weighted `ΔxEV` after cost. When the best available move is marginal and no forced move pends, the right plan is **zero transfers** — bank it.
- **A hit must be out-gained over the horizon, not the round.** In the hit regime, take the hit only if `ΔxEV_horizon > hit_points` with margin — measured over the rounds the *new* player will actually survive to play, weighted by `progression_carry`. Every hit on the plan carries the explicit gain that beats it; an unjustified hit is a critic kill. A one-round +1-point upgrade never justifies a −4.
- **Prefer the Wildcard for a structural rebuild; reserve it for one.** When `N_needed ≥ ~4–5` (and especially when free transfers would force paying hits this window and next), the Wildcard's zero-cost full rebuild beats drip-feeding transfers — the group→KO transition is the canonical case (budget $105m, cap loosens, half the nations out). Conversely, **never burn the Wildcard on a one-or-two-move tweak** or to chase a single hot player; and never carry it unused into the semi-finals. On a Wildcard recommendation, hand off to `wc-squad-architect` build-squad (full-market re-seed) and defer the fire to `wc-chip-strategist` / the manager.
- **Weight every gain by the survival horizon, not one round.** `ΔxEV_horizon` uses each side's `p_advance` ladder so a fixture edge bought into an elimination-exposed nation, or a sale that forfeits a deep run, is priced correctly. Never rank a transfer on next-round xEV alone — that is how the field over-trades.
- **Read upstream signals; never re-derive them.** `xEV` comes from `player-ev` signals; `swing_calendar`, `p_advance`, `mismatch_list`, `dead_rubber_flags` come from the `fixture` signal; ownership from the `ownership` signal. If a target has no `player-ev` signal, `wc-scout` → `wc-player-ev` runs first — do not fabricate a target's minutes or EV.
- **Repair to feasibility without gutting a block.** Apply the `building-blocks.md` repair order (formation → nation cap → budget → spread) preserving value-bearing blocks. A transfer that shatters a BB2 clean-sheet spine or strips a BB1 enabler costs more than the FT — flag it; sell the block as a unit or hold. Confirm a legal XI survives every pair.
- **Confirm the transfer rules or cap confidence.** The free-transfer count, carry-over behaviour, and hit-vs-hard-cap regime are load-bearing and not yet confirmed in `league-config.md` — web-search and cite them, plan under both regimes until confirmed, set `provisional_cost_rule: true`, and cap the cost side's confidence at 0.35 with a "confirm before lock" note (`signal-framework.md`). Prices are fixed all tournament, so a transfer's only cost is the FT/hit — there is no price-rise race to model.
- **Rank pairs; never auto-commit.** This skill emits an ordered, costed plan with the Wildcard call for `wc-squad-architect` and the board. The manager executes transfers manually in the official game (`CLAUDE.md` operating rule 1) — surface the options and the recommended default, and stop.

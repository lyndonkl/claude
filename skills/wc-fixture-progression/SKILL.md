---
name: wc-fixture-progression
description: Rates fixture difficulty (separately for an attacking and a defending fantasy asset, 1-5 each way, from opponent xGA/xG), computes team progression probabilities (group qualification odds from the mini-table; round-by-round knockout survival down the bracket) by reference-class forecasting updated Bayesianly on observed form and group state, detects weak-group/mismatch fixtures (powerhouse-vs-minnow -> captain candidates and clean-sheet locks), and builds a multi-round swing calendar of where each team's difficulty flips so transfers can be planned ahead. Emits the `fixture` signal. Use when called by wc-fixture-analyst, by the strategists in the populate stage, and by wc-fitness-eval for its progression_carry term — and never re-derive these once the signal exists.
---

# wc-fixture-progression — difficulty, progression odds, mismatches, swings

The engine behind `wc-fixture-analyst` and the source of the `p_advance` figures `wc-fitness-eval` discounts in its `progression_carry` term. It does four jobs the rest of the system reads off rather than recomputing: rate each fixture's difficulty *in both directions*, put a calibrated probability on each team advancing each round, flag the lopsided fixtures where points come cheapest, and lay out a forward calendar of difficulty swings so transfers land *ahead* of the field's lag (`game-theory-meta.md` §4).

The probability work is deliberately two-stage: an **outside view first** (reference-class advance rates by seed/ranking — `reference-class-forecasting`), then a **Bayesian update** on what we actually observe (form, goal difference, group state — `bayesian-reasoning-calibration`). A favourite is never priced as a certainty; the reference class always carries an upset rate, and the dead-rubber rotation flag fires the moment a team has clinched.

## Inputs

- The round id, phase, and bracket from `tournament-state.md` (group mini-tables, who plays whom, current standings).
- Per-team attacking and defensive strength: team xG-for and xGA per match (web-searched, cited; manager-provided where a model exists). Seed/pot and world ranking at the draw for the reference class.
- Observed results to date this tournament (goals, goal difference, xG over/under-performance) for the Bayesian update.
- Confirmed kickoff order within the round (from `wc-matchday-timing` if already emitted) for the swing calendar's day-tagging — optional, fixture difficulty does not need it.

Read the round's `clean-sheet` and `scout` signals if present, but do **not** re-derive them — this skill supplies the *fixture-strength scalars* those skills consume, not the other way round.

## Workflow

```
- [ ] 1. FIXTURE DIFFICULTY — rate every fixture 1-5 for an attacker AND 1-5 for a defender (opponent xGA -> attack ease; opponent xG -> clean-sheet ease)
- [ ] 2. PROGRESSION ODDS — outside-view base rate by seed (reference class), then Bayesian update on form + group state; groups via the mini-table, knockouts round-by-round down the bracket
- [ ] 3. WEAK-GROUP / MISMATCH — flag powerhouse-vs-minnow fixtures; tag attackers as captain candidates, defenders as clean-sheet locks
- [ ] 4. FIXTURE SWINGS — find the rounds where a team's difficulty flips (easy->hard or hard->easy); build the swing calendar to plan transfers ahead
- [ ] 5. DEAD-RUBBER CHECK — flag any fixture where a team has already qualified/is already out (rotation risk on that fixture's assets)
- [ ] 6. Emit the `fixture` signal (both-direction difficulty grid, p_advance per round, weak_group_flags, mismatch_list, swing_calendar) via wc-signal-emitter
```

## Method

### 1. Fixture difficulty — two directions, never one number

A fixture is *not* equally hard for the attacker you own and the defender you own. A goalkeeper against a toothless attack and a striker against a porous defence can sit in the **same** match with opposite difficulty. So rate every fixture twice on a 1-5 scale (1 = easiest for that asset, 5 = hardest):

- **Attacking ease (`fd_att`)** — driven by the *opponent's defensive concession rate*. Read the opponent's xGA-per-match and convert to a band. The easier the defence leaks, the lower (better) the score for your forwards/attacking mids:

  | opponent xGA/match | `fd_att` | meaning for your attacker |
  |---|---|---|
  | ≥ 1.8 | 1 | shooting gallery — captain/ceiling territory |
  | 1.4 – 1.8 | 2 | soft |
  | 1.0 – 1.4 | 3 | neutral |
  | 0.7 – 1.0 | 4 | stingy |
  | < 0.7 | 5 | elite back line — fade your attackers |

- **Clean-sheet / defensive ease (`fd_def`)** — driven by the *opponent's attacking output*. Read the opponent's xG-for-per-match. The blunter their attack, the lower (better) the score for your GK/defenders:

  | opponent xG/match | `fd_def` | meaning for your defence |
  |---|---|---|
  | < 0.7 | 1 | clean-sheet lock — stack candidate |
  | 0.7 – 1.0 | 2 | strong CS odds |
  | 1.0 – 1.4 | 3 | neutral |
  | 1.4 – 1.8 | 4 | leaky game likely |
  | ≥ 1.8 | 5 | shootout — avoid the defensive stack here |

Adjust each band by ±1 for **home/away** (host or strong-home-support nations defend better and attack more freely at home — nudge `fd_def` down and `fd_att` down at home, up away) and clamp to [1,5]. These are the scalars `wc-player-ev` multiplies xG/xA by and `wc-clean-sheet-model` reads for `P(clean sheet | fixture)` — emit them, do not let those skills re-estimate opponent strength independently.

> The two directions can disagree sharply and that is the *point*: a 1/5 split (`fd_att`=1, `fd_def`=5) is a high-scoring-game signal — load attackers, avoid the back line; a 5/1 split is a low-event game — your GK is a lock, your striker is a trap. `wc-fixture-analyst` reads both columns, never an averaged "FDR".

### 2. Progression odds — reference class, then Bayes

The probability a team advances is a forecast, so build it the disciplined way: **outside view, then update.**

**(a) Outside view — the reference class (`reference-class-forecasting`).** Anchor on the historical advance rate for a team of this seed/pot/ranking *before* looking at the current team's narrative. Starting base rates (World Cup historical seed-advance frequencies; refine against the cited source, mark provisional until confirmed):

- Group stage — P(advance from group) by pot: **Pot 1 ≈ 0.80, Pot 2 ≈ 0.60, Pot 3 ≈ 0.40, Pot 4 ≈ 0.20** (these sum to ~2 per group of four, i.e. two qualifiers — sanity-check that each group's four priors total ≈ 2.0 and renormalise if not).
- Knockout single tie — P(win the tie) from the **seed gap**: roughly even (≈0.50) between peers, ≈0.62 for a one-tier favourite, ≈0.72 for a two-tier favourite, ≈0.82 for a three-tier-plus gulf. Never 1.0 — the highest a single-match World Cup favourite earns is ~0.85; the residual is the upset rate the reference class *exists* to preserve.

**(b) Bayesian update on observed reality (`bayesian-reasoning-calibration`).** Treat the base rate as the prior and update on what this tournament has actually shown:

```
prior_odds      = p_base / (1 - p_base)
posterior_odds  = prior_odds × Π_i LR_i
p_advance       = posterior_odds / (1 + posterior_odds)
```

Evidence likelihood ratios `LR_i` (multiply the ones that apply; keep each bounded so no single signal swamps the prior):

| evidence | LR direction | rough magnitude |
|---|---|---|
| won MD1 / positive goal difference | > 1 | 1.3 – 1.7 |
| lost MD1 / negative GD | < 1 | 0.6 – 0.8 |
| xG strongly out-performing (over-performing finish — regress) | slightly < 1 | 0.85 – 0.95 |
| xG strongly under-performing (unlucky — expect mean-reversion up) | slightly > 1 | 1.05 – 1.20 |
| key player injured/suspended for the decisive match (cite `scout`) | < 1 | 0.5 – 0.8 |
| favourable remaining group draw vs unfavourable | > 1 / < 1 | 0.8 – 1.25 |

Cap the total swing so a single MD1 result can't move a Pot-1 side from 0.80 to a near-certainty — calibration over reactivity. After MD2/MD3, the group **mini-table arithmetic dominates the prior**: compute qualification combinatorially.

**(c) Groups — qualification odds from the mini-table.** Once games are played, enumerate the remaining-results space rather than trusting the seed prior:
- With one round to go, list the realistic remaining scorelines, find which combinations qualify the team (including the tie-breakers in order: points → goal difference → goals scored → head-to-head per the official rule, confirm in `league-config.md`/competition rules), and weight each combination by the per-match win/draw/loss probabilities implied by the two sides' `fd`/strength. `p_advance_group = Σ P(qualifying combinations)`.
- **2026 best-thirds path (do not use top-two-only math):** the top two per group **plus the 8 best third-placed teams** (of 12) advance. So `p_advance_group = P(top two) + P(3rd) × P(3rd-place points/GD ranks in the best 8 | the cross-group thirds table)`. The cross-group comparison means a "likely 3rd" team is often **~50–70% alive, not out** — and qualification can stay undecided until other groups finish. Track the live thirds table once MD2 results land.
- Surface **clinched** (`p_advance = 1.0`, but tag dead-rubber — see step 5) and **eliminated** (`p_advance = 0.0`) explicitly; these flip the whole asset calculus.

**(d) Knockouts — round-by-round survival down the bracket.** A team's value horizon is the *product* of surviving each successive tie:
```
p_reach(round R) = Π_{r = current..R} p_win_tie(r)
```
where each `p_win_tie(r)` is the seed-gap base rate updated by form, against the *likeliest* opponent at that node (use the bracket; if the next opponent is itself unresolved, average over that opponent's own `p_reach` to this node). Emit the full ladder `p_advance[round]` for `r32, r16, qf, sf, final` — this is exactly the per-round survival curve `wc-fitness-eval` multiplies into `progression_carry` (`Σ_r P(team alive at r) × discount^r`). A team that is 0.72 to win the R16 but only 0.30 to reach the QF tells the carry term to value its assets for ~1.7 more rounds, not the whole bracket.

### 3. Weak-group / mismatch detection

Points come from mismatches (the **A4 Fixture Exploiter** thesis). Flag a fixture as a **mismatch** when the strength gulf is large enough that returns become cheap and near-deterministic:

- **Powerhouse-vs-minnow trigger:** strength delta ≥ ~2 difficulty bands *and* one of {`fd_att` ≤ 2 for the favourite's attackers, `fd_def` ≤ 2 for the favourite's defence}. Concretely: favourite's `fd_att` = 1-2 → its attackers are **captain candidates** (ceiling + safety together — the chalk-captain and differential-captain logic both start here); favourite's `fd_def` = 1-2 vs a sub-0.7-xG attack → its defenders/GK are **clean-sheet locks** and a natural BB2 stack + Clean Sheet Shield target.
- **Weak-group flag:** a whole group containing a clearly dominant side and ≥2 weak attacks — it will generate multiple cheap clean sheets and goal hauls across the group across all three matchdays; flag the group so the strategists know to mine it, not just the single fixture.
- For each mismatch, name the **direction(s)** (attack, defence, or both) and the asset type unlocked, so the board can route it: A1 captains the favourite's premium attacker, A4 stacks the favourite's defence, A2 looks for the *low-owned* member of the same mismatch (the third-choice striker who'll still feast).

Mismatches are where ownership concentrates and where the field is *quickest* to converge — so a mismatch flag is also an instruction to `wc-ownership-analyst` to expect chalk, and to the differential hunters to find the under-owned way into the same game.

### 4. Fixture swings — the forward calendar

The field is slow to react to fixture turns (ownership lags reality by ~a round). Identify, per team, the rounds where its difficulty **flips** so transfers land *before* the field moves:

- For each team build the difficulty path across the next `H` rounds (group: the remaining matchdays; knockout: the bracket path weighted by `p_reach`). A **swing** is a flip of ≥2 bands in either direction:
  - **Easy→hard swing (sell signal):** a team enjoying a 1-2 stretch hits a 4-5 fixture in round *t+k* → plan to **transfer its attackers out before round t+k**, and (if KO) note whether its elimination-risk round arrives first (don't pay a transfer to dodge a fixture in a team that may be gone anyway — coordinate with `tournament-state.md` elimination horizons).
  - **Hard→easy swing (buy signal):** a team coming off tough fixtures into a 1-2 run → **get there a round early**, before ownership rises, to bank the value the lagging field hasn't priced.
- Annotate each swing with the round id, the direction, the asset class affected (attack vs defence — a swing can be one-directional, e.g. the opponent is leaky but also dangerous: `fd_att` improves while `fd_def` worsens), and a **plan-ahead lead** (how many rounds before the swing the transfer should fire to beat the field). Feed this straight to `wc-transfer-planner`.

### 5. Dead-rubber / rotation guard

The moment a team has **clinched** (or been **eliminated** from) qualification, its final group fixture becomes a rotation risk: managers rest starters, the clean-sheet and minutes assumptions break, and an owned asset's xEV can collapse without any injury. For every such fixture:
- Tag the fixture `dead_rubber: true` and drop a `rotation_risk: high` note keyed to that team's assets, so `wc-scout` and `wc-player-ev` discount minutes and `wc-fitness-eval` doesn't carry phantom progression value on a benched starter.
- A clinched team still shows `p_advance = 1.0` for *progression*, but its **next-fixture** difficulty and minutes carry the dead-rubber caveat — keep the two separate so the carry term isn't double-penalised.
- **2026 caveat — third place is usually alive, so true dead rubbers are rarer than top-two math suggests.** A team sitting 3rd on MD3 typically still has a live best-thirds path (above), and even a *clinched* team may play its starters to win the group (a kinder R32 bracket slot) or to protect goal difference for the thirds tie-breaker its rivals need. Only tag `dead_rubber: true` when the team's qualification **and** seeding/GD incentives are both settled — otherwise tag `rotation_risk: medium` with the reason, and let `wc-scout` confirm the team-news reality near lock.

## Output — the `fixture` signal

```yaml
---
type: fixture
round: <round id, e.g. 2026-grp-md2>
date: <YYYY-MM-DD>
emitted_by: wc-fixture-progression
confidence: <0.00-1.00>          # cap at 0.35 for any load-bearing strength/odds fact web-search couldn't confirm
source_urls:
  - <url for team xG/xGA>
  - <url for results/standings>
  - <url for seeds/ranking>      # or "manager-provided"
---

fixture_difficulty:               # both directions, 1 (easy) .. 5 (hard), per team per round
  - team: <nation>
    round: <round id>
    opponent: <nation>
    home_away: H|A|N
    fd_att: <1-5>                  # from opponent xGA — ease for YOUR attackers
    fd_def: <1-5>                  # from opponent xG  — ease for YOUR defence/GK
    opp_xGA_per_match: <n>
    opp_xG_per_match: <n>
    note: <e.g. "1/5 split — high-scoring game, load attack, fade the back line">

p_advance:                        # the per-round survival ladder fitness-eval discounts
  - team: <nation>
    p_advance_this_round: <0.00-1.00>
    method: reference-class+bayes | group-mini-table | clinched | eliminated
    base_rate: <0.00-1.00>        # the outside-view prior (seed/pot/seed-gap) BEFORE update
    by_round: { r32: <p>, r16: <p>, qf: <p>, sf: <p>, final: <p> }   # p_reach = Π survival
    upset_rate: <1 - p_win_tie>   # explicit — a favourite is never 1.0
    drivers: [ "won MD1 +2 GD (LR 1.5)", "xG over-performing, regress (LR 0.9)" ]

weak_group_flags:
  - group: <id>
    dominant: <nation>
    weak_attacks: [<nation>, <nation>]
    note: "multiple cheap CS + goal hauls available across all three MDs"

mismatch_list:
  - fixture: <FAV vs MINNOW> (<round id>)
    strength_delta_bands: <n>
    favourite: <nation>
    unlocks: [ captain_candidate (attack), clean_sheet_lock (defence) ]
    differential_angle: <e.g. "FAV's 2nd-choice striker — same feast, sub-8% owned">

swing_calendar:
  - team: <nation>
    swing_round: <round id>
    direction: easy_to_hard | hard_to_easy
    axis: attack | defence | both
    delta_bands: <n>
    plan_ahead_lead: <rounds before the swing to transfer to beat the field>
    action: "sell attackers before <round>" | "buy a round early, pre-ownership-rise"
    elimination_caveat: <e.g. "team's R16 elim-risk precedes this swing — may be moot">

dead_rubber_flags:
  - team: <nation>
    fixture_round: <round id>
    status: clinched | eliminated
    rotation_risk: high|medium
    note: "discount minutes/CS for this team's assets this fixture"
```

Every numeric field declares its range so the emitter can range-check it (`signal-framework.md`). Downstream agents read these columns; they must not re-estimate opponent strength or advance odds for the same round.

## Guardrails

- **Never price a favourite as a certainty.** Every `p_advance` carries its `base_rate` and an explicit `upset_rate` from the reference class; the single-match ceiling is ~0.85. If you've written 1.0 for anything other than a *mathematically clinched* group position, the Bayesian update has over-fit to a small sample — pull it back to the reference class.
- **Reference class before narrative.** Anchor on the seed/pot/ranking base rate first (`reference-class-forecasting`), then update on form (`bayesian-reasoning-calibration`). Do not let a single MD1 scoreline or a hot-form story set the prior; bound each likelihood ratio so no one signal swamps the base rate.
- **Two directions, always.** Never collapse `fd_att` and `fd_def` into one "difficulty" number — a fixture that is easy for attackers can be hard for the defence and vice-versa, and conflating them is the most common fantasy fixture error. Emit both columns.
- **Dead-rubber rotation is a hard flag, not a footnote.** Once a team has qualified or is out, its remaining group asset minutes are unreliable — tag it so the EV and fitness skills discount it. A clinched team's *progression* is 1.0 but its *next-fixture* value is not.
- **Swings must respect the elimination clock.** Don't recommend a transfer to dodge a future hard fixture in a knockout team whose elimination-risk round arrives first (`tournament-state.md`) — coordinate the swing calendar with each asset's horizon, or the move is wasted.
- **Confirm the strength inputs or cap confidence.** Team xG/xGA, seeds, and standings are load-bearing; web-search and cite each, or mark manager-provided. Any unconfirmed load-bearing fact caps the whole signal's `confidence` at 0.35 and gets a "confirm before lock" note for the board (`signal-framework.md`).
- **Emit; don't re-derive.** If a `fixture` signal already exists for this round, read it. This skill is the single source of fixture-strength scalars and progression odds for the round — downstream skills consume it rather than recomputing opponent strength.

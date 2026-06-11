---
name: wc-matchday-timing
description: Builds the structural support for the in-round levers in FIFA World Cup Fantasy — scores how the squad's players are distributed across the round's match days (a good build spreads them, NOT stacked on one day), orders the 4 bench players by kickoff time (latest highest, so they stay promotable after early results land), and generates conditional manual-substitution triggers ("if early starter scores ≤ T and a later bench player hasn't kicked off, promote them"). Implements BB6 (matchday spread) and MB3/MB4 (bench order + sub triggers), and the manual-substitution rule in league-config.md. Returns a kickoff_spread assessment with over-stack flags, a ranked bench_order (1–4), and a sub_triggers list. Use when laying out a matchday plan or vetting a candidate squad's timing layout — called by wc-matchday-tactician and the strategists, especially A6 Matchday Mechanic.
---

# wc-matchday-timing — kickoff spread, bench order, manual-sub triggers

Implements the **BB6 matchday-spread** constraint in `footballfantasy/context/frameworks/building-blocks.md` and the **manual-substitution rule** in `context/league-config.md`. This skill owns the *structural plumbing* under the two point-winning levers: the **captain ladder** (owned by `wc-captain-ladder`) and **manual subs**. Neither lever works on a squad whose players all kick off in the same window — there is nothing to switch to, nobody left to promote. This skill measures whether the build has that material, and if so, lays out the bench and the triggers that turn it into points.

The edge is concrete: `league-config.md` states an active manager working the captain ladder + manual subs gains **~20–40 points per round** over a set-and-forget manager. That edge is only *available* when the squad is spread across the round's match days. This skill protects that availability.

**One hard fact this skill is built around:** a manual sub only works if the bench player **has not yet kicked off**. Once a match has started, that player's score is locked — promotable players are exactly the ones whose kickoff is still in the future. So bench order is primarily a **kickoff-time** problem, and only secondarily a points problem. Order by kickoff first; break ties by xEV.

## Workflow

```
- [ ] 1. Load the round's match-day calendar (which days, kickoff times UTC) — web-search, cite
- [ ] 2. Load the candidate's XI + bench, each player's nation, fixture, kickoff slot, and xEV (read player-ev signals; do NOT re-derive)
- [ ] 3. KICKOFF SPREAD — bin the XI (and squad) by day/slot; score the spread; raise over-stack flags
- [ ] 4. BENCH ORDER — rank the 4 bench by kickoff time (latest = highest), break ties by xEV; drop dead-fixture benchers to the floor
- [ ] 5. SUB TRIGGERS — for each early starter, generate a conditional promotion rule; set the threshold T by position and the bench player's own xEV
- [ ] 6. Cross-check against the captain ladder (shared kickoff sequence) — flag conflicts, don't re-solve the ladder
- [ ] 7. Emit the matchday-timing signal: kickoff_spread + over_stack_flags, bench_order[1–4], sub_triggers[]
```

---

## Method

### 1. KICKOFF SPREAD — is there material for the levers?

Bin every starter by the **match day** (and, within a packed day, by the **kickoff slot** — early / late) on which their nation plays this round. The unit of analysis is the **XI** (those are the live captain-ladder candidates and the players a sub can replace); compute the same over the full 15 to read bench promotability.

**The spread score.** A good build distributes players across days so that on any given day there are *both* players still to play (ladder/sub fodder) and results already in (information). Stacking everyone on one day collapses both. Score the spread with normalised entropy over the day-bins:

```
Let n_d = number of starters who play on day d, N = 11 (the XI).
p_d = n_d / N.
H   = − Σ_d p_d · ln(p_d)                         # Shannon entropy of the day distribution
spread_score = H / ln(D)                            # normalise by ln(#days in the round) → [0,1]
```

- `spread_score → 1.0`: players evenly across all the round's days — maximal ladder/sub material (e.g. **3 Tue / 4 Wed / 4 Thu** across a 3-day round → `H/ln3 ≈ 0.99`).
- `spread_score → 0.0`: all 11 on one day — **the levers are dead.** No captain to ladder to, no later bench to promote; you are effectively set-and-forget for the round whether you like it or not.

**Interpretation bands:**

| spread_score | read | lever availability |
|---|---|---|
| ≥ 0.85 | well spread | full ladder + sub optionality |
| 0.65–0.85 | acceptable | levers work, some days thin |
| 0.45–0.65 | concentrated | one lever likely available, the other weak |
| < 0.45 | **over-stacked** | levers largely dead this round — flag |

**Over-stack flags** (raise each that applies):
- `single_day_stack`: any one day holds **> ~55%** of the XI (`max_d p_d > 0.55`). The round's captaincy and subs are decided in one window with no recourse.
- `captain_core_same_slot`: **all** BB1 captain candidates kick off in the *same* slot (no day/slot separation). The captain ladder (MB2) has no switching room — surfaced here for `wc-captain-ladder`, which owns the fix.
- `last_day_empty_bench`: the **latest** kickoff day has **no bench player** on it. Manual subs lose their best asset — the late promotable option — because every bencher has already played by the time early results are known.
- `front_loaded`: ≥ ~70% of the XI plays on day 1 of a multi-day round. You learn nothing before most of your points are banked; the in-round levers can't act on information that arrives too late.

A flag is **advisory** — it is a property of the squad build (BB6), not a matchday error. The right consumer is usually a strategist (rebuild the timing layout) or the tactician (note that this round is a low-lever round and manage expectations). For a candidate *squad* being vetted, a persistent low `spread_score` across the next 1–2 rounds is a real BB6 weakness worth a board annotation.

### 2. BENCH ORDER — rank the 4 by kickoff, then by points

The bench is an *ordered* list (MB3). Auto-subs and manual subs both walk it in order, promoting the highest-ranked eligible bencher. The ordering rule is **lexicographic — kickoff first, xEV second:**

```
For each of the 4 bench players, compute the key (kickoff_rank, xEV):
  kickoff_rank = how LATE the player kicks off this round (latest kickoff → highest rank)
  xEV          = the player's expected points (from their player-ev signal)

Sort DESCENDING by kickoff_rank; within an equal kickoff slot, sort DESCENDING by xEV.
Bench position 1 = first to be promoted; position 4 = last.
```

**Why latest-kickoff is highest, not highest-xEV.** A bench slot's *value as an option* is the chance you can still act on it after seeing results. A high-xEV bencher who has already kicked off is no longer promotable — his number is locked; the option is spent. The latest kickoff is the one that survives longest as a live lever, so it sits at the top of the order where a manual sub can reach it. xEV only sorts players who share a kickoff window.

**Two overrides on the pure kickoff sort:**

1. **Dead-fixture demotion — to the floor, never the top.** A bench player whose match is effectively meaningless to him — confirmed benched / suspended / injured / a starter on a side that has nothing to play for and is rotating — has **near-zero live xEV regardless of kickoff time.** Demote him to bench position 4 even if he kicks off latest. *A late kickoff on a player who won't accrue points is not a promotable option — it is a dead slot.* This is the single most common bench-order error and is called out in Guardrails.
2. **Auto-sub safety floor.** Position 1 should also be a *valid* auto-sub for the most likely XI hole (formation-legal as a swap for a startable position). If the kickoff-latest player can never legally replace a plausibly-benched starter (e.g. he's the backup GK and no outfielder is at risk), keep him ranked for *manual* promotion but note that the *automatic* fallback walks to position 2. Order serves both the manual lever and the auto-sub net.

Emit the final order as `bench_order[1..4]` with each player's `(kickoff, xEV, reason)` so the tactician and the board can see *why* a lower-xEV player outranks a higher one (it's the option value).

### 3. SUB TRIGGERS — the conditional promotion rules

For each **early-kickoff starter**, generate a rule that promotes a **later, still-to-play** bench player if the starter underperforms. The canonical shape:

```
IF  [early starter S] has finished his match AND scored ≤ T(S)
AND [bench player B] has NOT yet kicked off
AND promoting B keeps the XI formation-valid
THEN promote B for S before B's kickoff.
```

**Setting the threshold T(S)** — by position, then adjusted by *B's own xEV* (you only sub down to something better):

Base threshold by the started player's position (points already banked at which it's no longer worth chasing — calibrate magnitudes against `scoring-rules.md`, which is still `confirmed: false`, so treat absolute values as provisional):

| Position of S | base T | rationale |
|---|---|---|
| FWD / attacking MID | **≤ 2** | a forward who returns only the appearance tier (no goal/assist contribution) has whiffed his entire reason for starting; a live bencher with real attacking xEV is +EV to promote |
| MID (central / two-way) | **≤ 2** | floor came from minutes + maybe a defensive-actions return; if he didn't clear it, a better-fixtured B wins |
| DEF / GK | **≤ 1** | the clean sheet is already gone (conceded → CS points lost and he's into negative concede territory); little left to bank, promote if B's fixture is live |

Then **adjust T by the gap to B**:

```
T_eff(S, B) = T_base(S) + clamp( round(xEV(B) − xEV(S)) , −1, +2 )
```

- If the promotable B is meaningfully *higher* xEV than S (a strong bencher behind a punt starter), **raise** T — you'll sub off even a mediocre return because B's ceiling/floor is better. (cap +2)
- If B is only marginally better, **lower** T — only promote when S has clearly busted, since the swing is small and the downside of guessing wrong is real. (floor −1)
- Never set `T_eff` so high you'd bench a starter who's already returned (e.g. don't generate a trigger that fires on a captain-tier 6). The trigger is for *busts*, not for chasing variance off a decent score.

**Trigger hygiene:**
- **Only generate a trigger when B is genuinely later than S.** If B kicks off *before or with* S, there is no manual-sub window — the rule can never fire. Drop it. (This is the kickoff-ordering discipline made executable.)
- **Never target a dead-fixture B.** A trigger that promotes a bench player who won't accrue points is worse than no sub (you'd swap a banked appearance tier for a likely zero). Skip B's that were demoted to the floor in step 2.
- **Chain awareness, no double-counting.** If two early starters can both trigger onto the *same* single late bencher, note it as a *priority* (promote for whichever bust is worse / whichever vacancy keeps the formation valid) — you cannot promote one B twice.
- **Respect the captain ladder.** If S is also a captain-ladder candidate, the *armband* decision (keep/switch) is `wc-captain-ladder`'s, not a sub trigger. A manual sub removes the player and his (doubled, if captained) score entirely — only trigger a sub on a captain after the ladder has already moved the armband off him. Flag any S that is both a sub-trigger subject and a live captain so the tactician sequences them correctly; do not resolve it here.

### 4. Cross-check with the captain ladder

This skill and `wc-captain-ladder` share one object: the **kickoff sequence** of the round. Read its signal if present; do not re-solve the armband. Surface conflicts only:
- a sub trigger that would promote a player *off* whom the ladder still plans to move the armband (sequence collision),
- an over-stack flag (`captain_core_same_slot`) that kills the ladder's switching room.
Hand these to the tactician; the two skills are one system (per MB2/MB3/MB4 linkage in `building-blocks.md`) but each owns its half.

---

## Output (the matchday-timing signal)

Emitted via `wc-signal-emitter`. Type `matchday-timing`. Frontmatter per `signal-framework.md` (kickoff times are load-bearing facts — cite the source URL or mark manager-provided; if a kickoff or a predicted bench can't be web-confirmed, cap `confidence` at 0.35 and flag "confirm before lock").

```yaml
type: matchday-timing
round: <round id, e.g. 2026-grp-md2>
date: <YYYY-MM-DD>
emitted_by: wc-matchday-timing
confidence: <0.00–1.00>
source_urls:
  - <kickoff-schedule url | manager-provided>

kickoff_spread:
  days: [<day/slot ids this round, e.g. Tue-early, Tue-late, Wed, Thu>]
  xi_distribution: { <day>: <count>, ... }   # e.g. {Tue: 3, Wed: 4, Thu: 4}
  spread_score: <0.00–1.00>                   # normalised entropy of the XI day distribution
  band: well-spread | acceptable | concentrated | over-stacked
  over_stack_flags:                           # [] if none
    - flag: single_day_stack | captain_core_same_slot | last_day_empty_bench | front_loaded
      detail: <one line — which day/slot, what % of the XI, what lever it kills>

bench_order:        # ordered 1 (first promoted) → 4 (last); kickoff-first, xEV-second
  - rank: 1
    player: <name>
    kickoff: <UTC time / slot>
    xEV: <n>
    reason: <e.g. "latest kickoff Thu 20:00, live fixture — most promotable">
  - rank: 2 { player: ..., kickoff: ..., xEV: ..., reason: ... }
  - rank: 3 { player: ..., kickoff: ..., xEV: ..., reason: ... }
  - rank: 4 { player: ..., kickoff: ..., xEV: ..., reason: <e.g. "dead fixture — demoted to floor"> }
  auto_sub_fallback: <position whose player is the formation-valid automatic fallback, if not 1>

sub_triggers:       # [] if the spread gives no manual-sub window
  - if_starter: <S>
    starter_kickoff: <slot>
    threshold_T: <T_eff>            # position base, adjusted by xEV(B) − xEV(S)
    promote: <B>
    promote_kickoff: <slot>         # MUST be later than starter_kickoff
    keeps_xi_valid: true
    note: <e.g. "raise T: B is +3 xEV over S; sub even on a quiet 2">
    ladder_conflict: <none | "S is live captain — move armband first">

notes: <e.g. "Low-lever round: spread_score 0.41, everyone Wednesday. Manage as set-and-forget; the captain pick is the only live decision.">
```

If `spread_score` is in the over-stacked band, say so plainly in `notes` and emit `sub_triggers: []` — be honest that there is no in-round material this round rather than inventing triggers that can never fire.

## Guardrails

- **Matchday-3 simultaneity (the anti-collusion rule): a group's final two games kick off at the same time.** Within an MD3 group pair there is **no information window** — no captain switch, no manual sub between those two games; the in-round levers exist only *across* groups playing at different hours. So for an MD3 plan: (a) score kickoff spread across *group slots*, not raw match count; (b) treat each owned player in a simultaneous pair as **set-and-forget** for trigger purposes (no trigger may target a bench player whose game starts with the starter's); (c) the captain ladder for MD3 must step *between group slots* or it's dead (`wc-captain-ladder`). Verify the actual MD3 kickoff schedule from the round calendar — the simultaneity applies within each group, while different groups still stagger through the day.
- **A manual sub only works if the bench player has NOT yet kicked off. Order by kickoff time first, xEV second** — never by xEV alone. A higher-xEV bencher who has already played is a spent option; he cannot rank above a still-to-play one.
- **Never promote (or build a trigger toward) a dead-fixture bench player.** A confirmed-benched / suspended / injured / nothing-to-play-for-and-rotating player has near-zero live xEV regardless of kickoff time — demote him to bench position 4 and skip every trigger that targets him. Promoting him swaps a banked appearance tier for a likely zero.
- **Don't generate a trigger when the bench player kicks off before or with the starter.** With no future kickoff window the rule can never fire; drop it rather than emit a dead rule.
- **This skill does not switch the armband.** Captain keep/switch is `wc-captain-ladder`'s; only flag the sequencing where a sub and the ladder touch the same player, and require the armband to move off a captain before a sub removes him.
- **Don't re-derive upstream signals.** Read player xEV from `player-ev`, kickoff times from the round calendar, predicted benchings from `scout`. Re-compute nothing already emitted this round (`signal-framework.md`).
- **Cite every kickoff and predicted bench, or cap confidence at 0.35.** Kickoff times and predicted line-ups are load-bearing and firm up only ~24h before lock; flag minutes-sensitive items "re-check near lock."
- **Absolute thresholds are provisional until `scoring-rules.md` is `confirmed: true`.** The T values encode the points structure; treat magnitudes as calibration-caveated and re-verify the 60' tier and goal/clean-sheet values before trusting them numerically.
- **A flag is advisory, not a command.** Over-stacking is a property of the build (BB6) for a strategist or the tactician to weigh — surface it on the board; never silently restructure the squad.

---
name: wc-chip-timing
description: Scores the deployment leverage of all five FIFA World Cup Fantasy boosters (Wildcard, 12th Man, Maximum Captain, Clean Sheet Shield, Qualification Booster) across the remaining tournament horizon — computing, for each chip and each candidate round, the EXTRA expected points the chip yields in that round versus an average round, then turning the leverage surface into a fire/hold call per chip this round plus a maintained earmark table (chip -> earmarked round -> trigger -> fallback). This is the math engine behind wc-chip-strategist. Reads the round's player-ev, clean-sheet, fixture/progression, ownership and captain-ladder signals plus tournament-state (chips remaining, phase, surviving nations); never re-derives them. Enforces the golden rule — never reach the semis with chips unused. Use whenever a chip decision is live (the chip-check prompt, the group->KO transition, or any round where a chip is earmarked or leverage spikes). Emits a chip-plan signal.
---

# wc-chip-timing — chip deployment leverage across the horizon

Implements the deployment logic of `footballfantasy/context/frameworks/chip-catalog.md` — the five single-use boosters and the principle that **chips pay off on leverage, not on a quiet round.** `wc-chip-strategist` owns the deployment *plan* and the verify-verdict on offspring; this skill is the **engine it reasons from**: it prices, for every chip and every upcoming round, how much *extra* the chip is worth there, and converts that surface into a fire/hold recommendation and a horizon-aware earmark table.

The one idea this skill exists to make concrete: a chip's value is **not** "what it does," it is **what it does *here* minus what it would do in an ordinary round.** Five levers, one tournament; mis-timing one (especially the Wildcard or Maximum Captain) is a top-tier mistake, and nailing one is worth more than a round of good transfers (`chip-catalog.md` opening). So the deliverable is a **leverage score per chip per round** — the marginal EV the booster adds above its baseline round — and the discipline to *spend* that leverage at its peak rather than hoard it (the golden rule).

This skill **prices and sequences chips**; it does not build squads, derive player EV, rate fixtures, model clean sheets, or solve the captain ladder. Those are upstream signals — read them, never recompute (`signal-framework.md` rule). It feeds `wc-chip-strategist`, which presents the chip line to the board and emits the verify verdict; the **manager fires** — this skill never auto-deploys.

## When to invoke

- The **`chip-check` prompt** — "fire a chip this round?" runs this skill to score every chip's this-round leverage against its earmark.
- The **`matchday-board`** whenever a chip is earmarked for this round or the Director flags that leverage may have appeared (a loaded captain slate, a full BB2 stack drawn against a weak attack, the first KO round with multiple owned favourites).
- The **group->KO transition** — the canonical Wildcard window (`chip-catalog.md` #1): budget jumps to $105m, the nation cap loosens, half the field of nations is gone, and the whole squad needs re-pointing at survivors.
- `wc-chip-strategist` calls it during the **verify** stage to test whether a recombined offspring's MB5 chip attachment sits on a genuine leverage peak or is burning a chip on a quiet round.
- Any round where the **golden-rule clock** says chips are stacking up dangerously close to the semis (see the horizon-budget guard).

## Workflow

```
- [ ] 1. Load state: chips remaining + phase + surviving nations + nation-cap-by-round + budget (tournament-state.md);
        the current rank objective θ; the manager's stated chip appetite this round.
- [ ] 2. Load the round signals — DO NOT re-derive: player-ev (xEV/variance/ceiling/floor per owned player),
        clean-sheet (p_cs, stack_corr, expected_GA), fixture (fixture_difficulty + p_advance by round),
        ownership (effective ownership), captain-ladder (ladder_ev, vs_static_chalk, ladder_variance).
- [ ] 3. Define the candidate-round horizon: this round → … → final, with each round's phase tag.
- [ ] 4. Establish the BASELINE for each chip — its value in an *average* remaining round (the bench-marking line each chip's leverage is measured against).
- [ ] 5. For each chip × each candidate round, compute VALUE(chip, round) from that chip's formula (the METHOD section).
- [ ] 6. LEVERAGE(chip, round) = VALUE(chip, round) − BASELINE(chip). Build the leverage_by_round surface.
- [ ] 7. This-round call per chip: FIRE if this round is at/above the chip's leverage peak AND its trigger condition holds AND the golden-rule clock permits holding no longer; else HOLD.
- [ ] 8. Maintain the earmark table: each chip → its peak-leverage round → the trigger that fires it → the fallback if the leverage doesn't materialise.
- [ ] 9. Note chip interactions (pairs that compound; pairs to deliberately spread for variance) and apply the horizon-budget guard (don't hoard into the semis).
- [ ] 10. Emit the chip-plan signal (leverage_by_round, this-round fire/hold per chip, earmarks, interactions). Return its path.
```

## METHOD

### Leverage is the unit — the master formula

For every chip `g` and every candidate round `r` in the remaining horizon:

```
LEVERAGE(g, r) = VALUE(g, r) − BASELINE(g)
```

- `VALUE(g, r)` = the **extra expected points the chip yields if fired in round `r`** — computed from the chip-specific formulas below, using only this round's read signals (and, for future rounds, the fixture/progression signal's forward-looking fields plus a clearly-flagged projection).
- `BASELINE(g)` = the **same chip's value in an average remaining round** — the bench-marking line. It is *not* zero; every chip does *something* every round (an extra starter always scores *something*, a Max Captain always beats a fixed pick a little). Leverage is the *surplus over that ordinary-round value*, which is what makes "hold for a peak" a real, quantified decision rather than a vibe.

Set the baseline per chip as the **horizon median** of its own `VALUE(g, r)` across the remaining rounds (or, if forward signals are thin, a typical-round estimate flagged provisional). A chip is **worth firing now** when `LEVERAGE(g, this_round)` is at or near the **maximum of its own leverage curve** over the rounds in which it can still be played — tempered by the golden-rule clock (you cannot wait for a peak that arrives after the chip must be spent).

> All absolute magnitudes inherit the calibration state of `scoring-rules.md`: if it is still `confirmed: false`, every leverage number is **provisional** — the *relative ordering of rounds* for a given chip holds, the absolute point surplus does not. Carry that flag through to the signal.

Two framing rules that hold for every chip:

1. **Leverage is round-relative, not absolute.** A 12th-Man worth +6 in every round has *zero* leverage — there is no reason to time it; fire it whenever the golden rule demands. The chips worth agonising over are the ones whose curve is **peaky** (Wildcard, Maximum Captain, Qualification Booster), not flat.
2. **The leverage surface is computed under the current θ where the chip's value is variance-shaped.** Maximum Captain and the differential-amplifying use of 12th Man add *ceiling*; a chaser (`θ=gain`) values that surplus more, a leader (`θ=protect`) less. Where a chip is purely floor/EV (Wildcard rebuild, Clean Sheet Shield), θ barely moves it. Apply the same ±k·variance sign convention as `wc-fitness-eval`, and **state θ in the output** so the board reads the leverage the way fitness did.

---

### 1. Wildcard — value = the rebuild gain when many assets go dead at once

**What it does:** unlimited free transfers for one round — re-tools 6–10 players in a single move (`chip-catalog.md` #1).

```
VALUE(Wildcard, r) = [ Σ_player  ( xEV(best_replacement | r..horizon)  −  xEV(current_player | r..horizon) ) ]_over the players a normal-FT plan could NOT reach
                   + budget_unlock_gain(r)            # extra xEV buyable from the +$5m KO budget jump
                   + nation_cap_unlock_gain(r)        # extra xEV from loosened nation cap (stack a surviving favourite)
                   − 0                                # the chip itself costs no points
```

The load-bearing term is the **first one, restricted to the players a patch-by-patch transfer plan cannot keep up with.** A Wildcard's leverage is *not* the gain over your current squad — it is the gain over **what your free transfers alone could have fixed this round.** If two free transfers would have repaired the squad, the Wildcard's leverage is small; its surplus is the value of the moves *beyond* those FTs — which spikes exactly when **many assets hit dead fixtures or eliminations simultaneously** and the FT drip can't drain the backlog.

```
LEVERAGE(Wildcard, r) ≈ Σ_{dead-or-soon-dead assets beyond reach of this round's FTs}
                          ( xEV(replacement, r..horizon) − xEV(stranded asset, r..horizon) )
                        + budget_unlock_gain(r) + nation_cap_unlock_gain(r)
```

**Peak — the group→KO transition** is canonical and almost always the maximum of the curve:
- `+$5m` budget (group $100m → KO $105m) → `budget_unlock_gain` is real and only available once.
- nation cap **loosens** → you can now legally over-stack a surviving favourite's back line (a BB2 spike that was illegal in groups) → `nation_cap_unlock_gain`.
- **survivors only** → roughly half the nations are eliminated at once, stranding a large block of your squad in a single round — the dead-asset count peaks here, and no FT plan can re-point 6–10 players in one round.
- the field's squads converge on the 8–16 survivors → differentials get scarcer (`league-config.md`), so the rebuild also re-sets your ownership posture.

Score the transition round's `VALUE` with the **KO budget and KO nation cap already applied** (read them from `tournament-state.md`), and count progression carry over the *deep* survivors (`fixture` signal `p_advance`) — that is what makes this round dominate every group-stage alternative.

**Secondary peak:** a group-stage round where a **cluster** of your players hit dead fixtures/eliminations together and the FT count can't keep pace — the same first-term spike without the budget/cap unlocks.

**Anti-pattern (forces a near-zero leverage):** burning it to chase one hot player. One transfer is a one-FT problem; the Wildcard's surplus over a single FT is tiny. Flag any this-round FIRE whose first-term reach is ≤ (FTs available + 1) as **anti-pattern — save for a structural rebuild.**

**Evolution-engine interaction:** a Wildcard round means `wc-squad-architect`'s candidate space is the *full market* again, not transfer-adjacent squads — the strategist population must be **re-seeded from scratch**, not evolved from the current squad. Surface this so the Director re-populates.

---

### 2. 12th Man — value = the expected score of your 12th-best starter that round

**What it does:** start 12 instead of 11 — the bench's best player also scores (`chip-catalog.md` #2).

```
VALUE(12th Man, r) = E[ score of the best-of-bench player who would be the 12th starter in round r ]
                   = max over the 4 bench players of  xEV(player, r)   (restricted to players who actually start their match)
```

The chip is worth **exactly the 12th-best expected score** — so its whole value is *maximise that number*, never "just use it." Leverage peaks when the **bench itself is strong**:

```
LEVERAGE(12th Man, r) = E[12th-best starter, r]  −  BASELINE(12th Man)
   peaks when:  bench is all-from-survivors with good draws (typically a KO round)
                AND/OR the slate is clean-sheet-rich across your bench defenders (broad p_cs)
```

- **Peak A — loaded bench:** a knockout round where all 15 are from surviving nations with good draws, so even the bench player is a real starter against a beatable opponent. The marginal 12th score is highest then.
- **Peak B — CS-rich slate:** broad clean-sheet potential across your bench defenders (read `p_cs` from the `clean-sheet` signal for each bench defender's fixture) — the extra starter is *likely to return* the 60'-gated clean-sheet points, not just an appearance fee.

**Anti-pattern (depresses the value directly):** promoting a **dead-fixture or rotation-risk** bench player — the 12th score is then near the appearance floor (or zero if he doesn't start). The value term already punishes this (`max over bench` collapses), but flag it explicitly: *the chip is worth the 12th-best score; if that player isn't a nailed starter against a beatable side, the leverage isn't there.*

**Pairs with Maximum Captain** in a genuinely loaded round (both want a strong slate) — but see the **spread-for-variance** guard: doubling chips into one round concentrates your tournament variance into a single result.

---

### 3. Maximum Captain — value = E[max captain candidate] − E[ladder]

**What it does:** retroactively captains your highest-scoring player of the round — removes captain-pick risk entirely (`chip-catalog.md` #3).

```
VALUE(Maximum Captain, r) = E[ max over ALL eligible XI players of realised round score, r ]   # the chip's outcome (from wc-captain-ladder's max_captain_value)
                          − E[ optimal captain ladder, r ]                                     # what you'd get WITHOUT the chip, playing the ladder well (ladder_ev)
```

This is the crux and the reason this chip is so badly mistimed in practice: its value is **not** the captain's ceiling — it is the **resolution of captain *uncertainty*** over and above what the rolling ladder already buys you. The ladder is already good: you watch the early games and switch the armband (`wc-captain-ladder`). The chip's surplus is only the gap between the *guaranteed max* and the *ladder's expected best reachable*:

```
LEVERAGE(Maximum Captain, r) = ( E[max over XI] − ladder_ev )  −  BASELINE(Maximum Captain)
   peaks when:  captaincy is a hard MULTI-CANDIDATE call (no runaway favourite)  → ladder_ev is well below E[max]
                AND the candidates have HIGH CEILING (premium attackers vs weak opponents)  → E[max] is large
                AND candidates are correlated/same-slot (the ladder can't switch on info) → ladder_ev underperforms most
```

Read both numbers straight from the `captain-ladder` signal: `max_captain_value` (the chip outcome — `wc-captain-ladder` emits it when the chip rides) and `ladder_ev` (the no-chip optimum). When the ladder signal reports `ladder_valid: false` (candidates all in one slot), the ladder degenerates to a single fixed bet and the chip's surplus is **largest** — that is precisely the captaincy-fragile round the chip rescues.

- **Peak:** several plausible captain options with high ceilings, hard to separate — the chip converts that uncertainty into a guaranteed best outcome.
- **Anti-pattern (near-zero leverage):** one obvious nailed captain. If `ladder_ev ≈ E[max]` (a runaway favourite the ladder would never move off), the chip adds almost nothing over simply captaining him — **hold it.** Flag any FIRE where `(E[max] − ladder_ev)` is below a small threshold as *anti-pattern — no captaincy uncertainty to resolve.*

**θ:** the surplus is ceiling-shaped → a chaser (`θ=gain`) values it more; still fire it on its leverage peak, but the peak round itself shifts a touch earlier for a chaser who wants the variance banked.

**Interaction:** when this chip is on, the ladder is **moot** for the round (`wc-captain-ladder` `ladder_moot: true`); fitness uses `max_captain_value`, not the ladder's switching value. Conversely, if `wc-captain-ladder` reports the ladder's own uplift over static chalk is *already large*, the chip adds little — surface that as a hold signal.

---

### 4. Clean Sheet Shield — value = the protected clean-sheet EV

**What it does:** protects clean-sheet returns in certain situations (e.g. defenders keep CS points despite a late goal — confirm the exact rule in-game, `chip-catalog.md` #4).

```
VALUE(Clean Sheet Shield, r) = Σ_{defenders+GK on the pitch in round r}  λ_cs(pos) · P(late-goal-breaks-an-otherwise-CS | fixture)
                             ≈ stack_corr_EV(r) · P(marginal CS loss the shield would reverse)
```

The chip's value is the **clean-sheet EV it rescues** — the points lost to the *late breach of an otherwise-earned clean sheet*, summed over your defensive assets on the pitch, amplified by within-team correlation (a stacked back line keeps or loses the CS *together*). Read `p_cs`, `expected_GA` and `stack_corr_bonus` from the `clean-sheet` signal; do not recompute them.

```
LEVERAGE(Clean Sheet Shield, r) = protected_CS_EV(r) − BASELINE(Clean Sheet Shield)
   peaks when:  a FULL BB2 stack (3+ defenders + GK from one strong team) is on the pitch
                AND that team faces a WEAK attack (high P(CS), low expected_GA, a stack on the cusp of locking)
                AND (knockout) low-scoring cagey games make CS both likely AND pivotal
```

- **Peak:** heavily stacked on one defence (a full BB2 at 3+1) against a weak attack — the shield turns a *probable* clean sheet into a *near-locked* one and caps the stack's correlated downside. The bigger and more correlated the stack, the more EV there is to protect (this is why the chip pairs with BB2 at full stack).
- **Anti-pattern (little to protect):** a thin or spread defence — minimal CS exposure, so `protected_CS_EV` is small regardless of the round. Flag any FIRE without a 3+1 stack on the pitch as *anti-pattern — insufficient CS exposure to shield.*

**Pairs with the Clean-Sheet Spine (BB2) at full stack** — its leverage is *defined* by having that block on the pitch, so coordinate with the MB1/MB5 plan: fire it the round the stack is both complete and drawn against the weakest available attack.

---

### 5. Qualification Booster — value = expected progression bonus

**What it does:** rewards you when your players' nations advance in the tournament (`chip-catalog.md` #5).

```
VALUE(Qualification Booster, r) = Σ_{owned players}  progression_bonus_per_advance · P(player's nation advances this round | tie)
```

The value is the **expected progression bonus** — directly the sum, over your owned players, of the per-advance bonus times each nation's probability of going through this round. Read `p_advance[round]` per nation from the `fixture` signal (`wc-fixture-progression`); never re-rate a tie.

```
LEVERAGE(Qualification Booster, r) = E[progression bonus, r] − BASELINE(Qualification Booster)
   peaks in:  a KNOCKOUT round where you own MULTIPLE players from STRONG FAVOURITES in FAVOURABLE ties
              (top seed vs weak qualifier → high, concentrated P(advance))
```

- **Peak:** a knockout round where you own several players from heavy favourites with **favourable ties** (a top seed vs a weak qualifier) — high, *concentrated* advance probability across many of your assets compounds the progression you were already banking on. The first KO round is the default earmark because the most nations are still alive and the seeding mismatches are widest.
- **Anti-pattern (mushy expectation):** a squad spread across **coin-flip ties** — the expected bonus is a smear of ~50% probabilities and the chip underdelivers. The fix is ordering: *concentrate ownership in likely-advancers first, then fire it.* Flag any FIRE whose owned-nation advance probabilities are mostly near 0.5 as *anti-pattern — concentrate on favourites before deploying.*

**Interaction:** directly amplifies the **Progression Theorist (A3)** thesis (`archetype-catalog.md`). If A3's candidates are winning the fitness race in a KO round, this chip is their natural partner — surface that the chip and the genotype want the same round.

---

### From the surface to the calls — fire/hold and the earmark table

**This-round fire/hold (per chip).** Given the leverage surface, the rule for each chip is:

```
FIRE(g) this round  ⇔  ( LEVERAGE(g, this_round) ≥ peak_band of g's leverage curve over rounds g can still be played )
                       AND ( g's trigger condition holds — the chip-specific peak conditions above )
                       AND ( anti-pattern flag NOT raised for g this round )
                       AND ( holding longer is permitted by the golden-rule clock — see guard )
else HOLD(g), carrying its earmark forward.
```

"Peak band" = at or near (within a small tolerance of) the **maximum of that chip's own leverage curve** across the rounds in which it remains legally playable. A chip whose curve still rises ahead is **held** — *unless* the golden-rule clock forces the hand. A chip whose peak is *behind* it (a passed group→KO transition for an unused Wildcard) is **overdue** — fire at the next-best round, do not chase a peak that has gone.

**The earmark table (maintained every run, mirrors `tracker/chip-ledger.md` and the table in `chip-catalog.md`):**

| Chip | Earmarked round | Trigger condition | Fallback |
|---|---|---|---|
| Wildcard | group→KO transition | budget + elimination rebuild needed (dead-asset count beyond FT reach) | next dead-fixture cluster |
| 12th Man | a loaded KO round | bench all-from-survivors with good draws + CS-rich slate | hold to a stronger-bench round; force before semis |
| Maximum Captain | TBD — a multi-candidate captain round | hard, high-ceiling captain call (`ladder_ev` ≪ `E[max]`) | hold; force before semis |
| Clean Sheet Shield | TBD — a full-stack round | 3+1 BB2 stack on the pitch vs a weak attack | hold to the next full-stack-vs-weak-attack round |
| Qualification Booster | first KO round | multi-favourite ownership in favourable ties | next KO round with concentrated favourites |

Each earmark is `(chip → peak-leverage round → trigger that fires it → fallback if the leverage doesn't appear)`. Re-derive it every run from the live surface; an earmark whose round has passed unfired escalates to **overdue** and its fallback becomes the active plan.

### Chip interactions

- **12th Man + Maximum Captain** *compound* in a genuinely loaded round (both want a strong, high-ceiling slate) — their leverage peaks can coincide. But **consider spreading them across rounds for variance** (Guardrails): two chips on one slate concentrates a large share of your tournament's chip value into a single result; a blank that round wastes two levers at once.
- **Clean Sheet Shield + BB2 full stack** are nearly inseparable — the chip's leverage is *defined* by the stack being on the pitch; coordinate firing with the MB1/MB5 plan, not independently.
- **Qualification Booster + A3 (Progression Theorist)** want the same KO round and the same owned-favourite concentration — when A3 is winning fitness in a KO round, the chip is its partner.
- **Wildcard ⟂ everything** — it changes the *squad*, so it is rarely paired with a same-round scoring chip (the rebuilt squad's MB5 is a fresh question); price it on its own rebuild-gain curve and re-seed the population.

### The golden-rule clock (horizon-budget guard)

**Never carry all five chips into the semi-finals unused** (`chip-catalog.md`). Maintain a running check:

```
chips_remaining  vs  scoring_rounds_left_before_semis   (read both from tournament-state.md)
if  chips_remaining ≥ scoring_rounds_left_before_semis :  raise FORCE flags — the lowest-leverage-cost
    chips must be spent at their best *remaining* round even if that round is below their historical peak.
```

Unused leverage is wasted leverage. The job is to **spend** chips at peak leverage, not to hoard them safe to the end. When the clock binds, this skill stops waiting for an ideal peak and recommends firing the chip whose *cost of a sub-optimal round is smallest* (typically the flat-curve chips — 12th Man before Maximum Captain) at its best remaining opportunity.

---

## Output (the `chip-plan` signal)

Emit via `wc-signal-emitter` to `signals/<round>-chip-plan.md`:

```yaml
---
type: chip-plan
round: <round id, e.g. 2026-grp-md3>
date: <YYYY-MM-DD>
emitted_by: wc-chip-timing
confidence: <0.00–1.00>          # ≤0.35 if a load-bearing leverage input (a future fixture, a stack's p_cs, a tie's p_advance) is web-unconfirmed
source_urls:
  - <fixture / progression signal path or url>     # facts trace to upstream signals or are manager-provided
  - <clean-sheet / captain-ladder / ownership signal paths>
provisional_scoring: <true|false>   # true if scoring-rules.md is not confirmed:true → absolute leverage magnitudes caveated
---
objective: { theta: protect|gain|neutral, k: <n> }   # the lens the variance-shaped chips were scored under
horizon:                                              # the candidate rounds priced, this round → final
  - { round: <id>, phase: <grp-md3|r32|r16|qf|sf|final> }
chips_remaining: [<Wildcard|12th Man|Maximum Captain|Clean Sheet Shield|Qualification Booster>, ...]
golden_rule_clock:
  scoring_rounds_left_before_semis: <n>
  chips_remaining_count: <n>
  force_flags: [<chip names the clock now forces to spend>]   # empty if slack remains

leverage_by_round:                  # the surface — per chip, VALUE and LEVERAGE for each candidate round
  - chip: Wildcard
    baseline: <n>                   # the average-remaining-round value this chip's leverage is measured against
    rounds:
      - { round: <id>, value: <n>, leverage: <n>, trigger_met: <true|false>, anti_pattern: <true|false>, note: "<one football line>" }
      # … one row per candidate round …
    peak_round: <id>                # argmax of leverage over playable rounds
  - chip: 12th Man
    baseline: <n>
    rounds: [ { round: <id>, value: <n>, leverage: <n>, trigger_met: <bool>, anti_pattern: <bool>, note: "<...>" }, ... ]
    peak_round: <id>
  - chip: Maximum Captain            # value = E[max over XI] − ladder_ev   (both read from captain-ladder signal)
    baseline: <n>
    rounds: [ ... ]
    peak_round: <id>
  - chip: Clean Sheet Shield         # value = protected CS EV over the BB2 stack on the pitch
    baseline: <n>
    rounds: [ ... ]
    peak_round: <id>
  - chip: Qualification Booster      # value = Σ owned · per-advance bonus · p_advance(tie)
    baseline: <n>
    rounds: [ ... ]
    peak_round: <id>

this_round:                         # the actionable call per chip (advisory — the manager fires)
  - { chip: Wildcard,            recommendation: fire|hold, leverage_now: <n>, peak_band: <true|false>, reason: "<football line>" }
  - { chip: 12th Man,            recommendation: fire|hold, leverage_now: <n>, peak_band: <bool>, reason: "<...>" }
  - { chip: Maximum Captain,     recommendation: fire|hold, leverage_now: <n>, peak_band: <bool>, reason: "<...>" }
  - { chip: Clean Sheet Shield,  recommendation: fire|hold, leverage_now: <n>, peak_band: <bool>, reason: "<...>" }
  - { chip: Qualification Booster, recommendation: fire|hold, leverage_now: <n>, peak_band: <bool>, reason: "<...>" }

earmarks:                           # the living horizon plan (chip → peak round → trigger → fallback)
  - { chip: Wildcard,            earmarked_round: <id>, trigger: "<condition>", fallback: "<round/condition>", status: available|earmarked|overdue|used }
  - { chip: 12th Man,            earmarked_round: <id>, trigger: "<...>", fallback: "<...>", status: <...> }
  - { chip: Maximum Captain,     earmarked_round: <id>, trigger: "<...>", fallback: "<...>", status: <...> }
  - { chip: Clean Sheet Shield,  earmarked_round: <id>, trigger: "<...>", fallback: "<...>", status: <...> }
  - { chip: Qualification Booster, earmarked_round: <id>, trigger: "<...>", fallback: "<...>", status: <...> }

interactions:
  - "<e.g. 12th Man + Maximum Captain peaks coincide at <round> — compounding; consider spreading for variance>"
  - "<e.g. Clean Sheet Shield earmark binds to BB2 full stack on the pitch at <round>>"
  - "<e.g. Qualification Booster ↔ A3 both want <KO round>>"
flags:
  - "<e.g. Wildcard overdue — group→KO transition passed unfired; fallback = next dead-fixture cluster>"
  - "<e.g. golden-rule clock binding — force 12th Man at its best remaining round before semis>"
  - "<e.g. confirm 2026 booster mechanics in-game — Clean Sheet Shield exact rule provisional (league-config §7)>"
recheck_before_lock: <true|false>   # true whenever a fire/hold call depends on a not-yet-confirmed XI, fixture, or tie
```

(Frontmatter follows the common signal schema in `frameworks/signal-framework.md`; `wc-signal-emitter` validates and persists it.)

## Guardrails

- **Read the upstream signals; never re-derive them.** Player EV (xEV/variance/ceiling/floor) is `wc-player-ev`'s; clean-sheet `p_cs`/`expected_GA`/`stack_corr` are `wc-clean-sheet-model`'s; fixture difficulty and `p_advance` are `wc-fixture-progression`'s; the ladder's `ladder_ev`/`max_captain_value`/`ladder_variance` are `wc-captain-ladder`'s; effective ownership is `wc-ownership-meta`'s. This skill **prices and times** chips; re-computing any of these would desync the system and double-handle uncertainty.
- **Leverage, never raw chip value.** A fire/hold call must be made on `VALUE − BASELINE`, not on the chip's absolute effect. A chip that does the same thing every round has zero leverage and should be timed only by the golden-rule clock.
- **Hold for leverage — but do not hoard into the semis.** The golden rule is binding: never carry all five chips into the semi-finals unused. When `chips_remaining ≥ scoring_rounds_left_before_semis`, stop waiting for an ideal peak and recommend firing the lowest-leverage-cost chip at its best *remaining* round. Unused leverage is wasted leverage; the deliverable is *spending* chips well, not preserving them.
- **Some chips pair — but consider spreading for variance.** Note compounding pairs (12th Man + Maximum Captain in a loaded round; Clean Sheet Shield + a BB2 full stack; Qualification Booster + A3 in a KO round). Where two chips' peaks coincide, surface that stacking them concentrates a large share of the tournament's chip value into a single result, and offer the spread-across-rounds alternative explicitly so the manager chooses the variance posture.
- **Each chip's anti-pattern voids a FIRE.** Do not recommend firing a chip into its catalogued anti-pattern even if the round is otherwise convenient: a Wildcard for one transfer, a 12th Man on a dead-fixture bench player, a Maximum Captain with one obvious captain, a Clean Sheet Shield on a thin defence, a Qualification Booster across coin-flip ties. Raise the `anti_pattern` flag and recommend hold.
- **Confirm the 2026 booster mechanics before trusting absolute leverage.** The booster set is provisional (`league-config.md` §7 / `chip-catalog.md` opening) and the point table is provisional until `scoring-rules.md` is `confirmed: true`. When either is unconfirmed, set `provisional_scoring: true`: the *round ordering* of a chip's leverage remains usable, the *absolute point surplus* is caveated. Cap confidence at 0.35 when a load-bearing leverage input (a future fixture, a stack's clean-sheet probability, a tie's advance probability, a not-yet-confirmed XI) could not be web-confirmed, and set `recheck_before_lock: true`.
- **Advisory only — surface the call, never fire.** This skill recommends; `wc-chip-strategist` presents the chip line to the board with its dissent; the **manager deploys** in the official game and the Director marks the chip `used` in `tournament-state.md` and `tracker/chip-ledger.md` the same turn. Never treat a FIRE recommendation as a deployment.

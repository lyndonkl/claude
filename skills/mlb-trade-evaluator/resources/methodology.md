# MLB Trade Evaluator Methodology

Detailed procedures for rest-of-season projection sourcing, per-category delta math, `cat_pressure` weighting, dollar valuation, slot-value optionality, delegation to `adverse-selection-prior`, positional flex scoring, playoff impact, and the principle-#8 verdict ladder.

## Table of Contents
- [Projection Sourcing](#projection-sourcing)
- [Counting Category Math](#counting-category-math)
- [Ratio Category Math](#ratio-category-math)
- [`cat_pressure` Weighting](#cat_pressure-weighting)
- [`trade_value_delta` — Dollar Valuation](#trade_value_delta--dollar-valuation)
- [Slot-Value Optionality](#slot-value-optionality)
- [Adverse-Selection Delegation](#adverse-selection-delegation)
- [`positional_flex_delta` Scoring](#positional_flex_delta-scoring)
- [`playoff_impact` (July+)](#playoff_impact-july)
- [Verdict Ladder — Principle #8 and the Always-Counter Rule](#verdict-ladder--principle-8-and-the-always-counter-rule)
- [Counter-Offer Construction](#counter-offer-construction)
- [Common Failure Modes](#common-failure-modes)

---

## Projection Sourcing

All rest-of-season projections come from web search. No API is available. Cite every URL.

### Primary source: FanGraphs ATC

**ATC (Average Total Cost)** is the ensemble projection that weights multiple forecasters. It is the most accurate consensus source for rest-of-season value.

- Rest-of-season projections URL: `https://www.fangraphs.com/projections.aspx?type=atcr` (the `r` suffix = ros)
- Full-season projections URL: `https://www.fangraphs.com/projections.aspx?type=atc`
- Individual player page: `https://www.fangraphs.com/players/{slug}/{id}` — has a ROS line in the projections box

**Always prefer `atcr` (rest-of-season) over `atc` (full season).** A player who has banked 20 HRs in April is worth less for the remaining 5 months than his full-season line implies.

### Fallback order

1. **FanGraphs Depth Charts** (`type=fangraphsdcr`) — hand-adjusts ATC for playing time.
2. **Razzball Player Rater** — industry-standard fantasy value.
3. **FantasyPros ECR** — consensus rank; useful when the other two disagree by more than one tier.

### What to pull per player

**Hitters:** Remaining PAs, R, HR, RBI, SB, OBP.

**Pitchers:** Remaining IP, K, ERA, WHIP, QS (direct from FanGraphs; do not heuristic), SV (with `save_role_certainty` cross-check from `mlb-closer-tracker`).

### When projections conflict

If ATC and Depth Charts disagree by more than 15% on any counting stat, note both values in the signal file and use the **more conservative** of the two for delta math.

### When a player is on the IL

ATC does not always reprice quickly after an IL stint. Cross-check RotoWire. If the projected return date will cost >4 weeks of games and ATC hasn't adjusted, manually scale: `adjusted_proj = atc_ros × (games_remaining_after_return / total_ros_games)`.

---

## Counting Category Math

Counting cats: **R, HR, RBI, SB** (hitters) and **K, QS, SV** (pitchers). Seven total.

```
raw_delta_C = Σ (projected_C of IN players) − Σ (projected_C of OUT players)
```

No scaling, no volume weighting.

### Special case: SV

Always cross-reference `save_role_certainty` from `mlb-closer-tracker`. If `save_role_certainty` < 70 for an IN or OUT RP, flag the trade as SV-volatile and reduce confidence by 0.1.

### Special case: QS

Use FanGraphs' direct QS projection. If missing: `projected_QS = projected_GS × estimated_QS_rate` where QS rate is pulled from the pitcher's trailing 50-start history.

---

## Ratio Category Math

Ratio cats: **OBP** (hitters), **ERA** and **WHIP** (pitchers). Three total.

### OBP delta

```
OBP_IN  = Σ(OBP_i × PA_i) / Σ(PA_i)   over IN hitters
OBP_OUT = Σ(OBP_j × PA_j) / Σ(PA_j)   over OUT hitters
```

Compute the team-level OBP before and after the trade (replace OUT with IN in the team pool); `delta_OBP = after − before`.

### ERA delta

```
Implied ER_i = ERA_i × IP_i / 9
ERA_IN  = 9 × Σ(ER_i) / Σ(IP_i)
ERA_OUT = 9 × Σ(ER_j) / Σ(IP_j)
```

**Sign convention:** lower ERA is better. Flip sign before summing into `trade_cat_delta`.

### WHIP delta

```
Implied baserunners_i = WHIP_i × IP_i
WHIP_IN = Σ(baserunners_i) / Σ(IP_i)
```

Same sign-flip rule.

### Converting ratio deltas to the `trade_cat_delta` scale

- **OBP**: `scaled_delta_OBP = delta_OBP × 10,000`
- **ERA**: `scaled_delta_ERA = −delta_ERA × 50`
- **WHIP**: `scaled_delta_WHIP = −delta_WHIP × 200`

---

## `cat_pressure` Weighting

Open the most recent `signals/YYYY-MM-DD-cat-state.md`. If it does not exist, **run `mlb-category-state-analyzer` first.**

```
weight_C = cat_pressure_C / 50
weighted_delta_C = raw_delta_C (or scaled ratio delta) × weight_C
trade_cat_delta = Σ weighted_delta_C
```

| `cat_pressure` | weight | Meaning |
|---|---|---|
| 0 | 0.0 | Punt category |
| 25 | 0.5 | Low importance |
| 50 | 1.0 | Neutral |
| 75 | 1.5 | High importance |
| 100 | 2.0 | Critical |

### Caveat: opponent's `cat_pressure` is not ours

Mirror table: use raw deltas, or pull the opponent's standings per-cat separately. Never apply our weights to their side.

---

## `trade_value_delta` — Dollar Valuation

### Primary source: FanGraphs Auction Calculator

- URL: `https://www.fangraphs.com/auction-calculator`
- Configure: 12-team, H2H categories, standard roster, 5x5 (OBP variant).

### Raw formula

```
trade_value_delta_raw = Σ($_ROS of IN players) − Σ($_ROS of OUT players)
```

This is the input to Step 6 (slot-value bonus) and Step 7 (adverse-selection haircut). It is NOT the final number used by the verdict ladder.

### Calibration buckets (on the FINAL `trade_value_delta_adjusted`, expressed as a percent of outgoing dollars)

| `delta_pct` | Bucket | Verdict guidance |
|---|---|---|
| ≥ +15% | Clear gain | ACCEPT (if other gates pass) |
| 0 to +15% | Modest gain | COUNTER (squeeze more) |
| −20% to 0 | Modest loss | COUNTER (specific ask) |
| ≤ −20% | Clear loss | REJECT (if adverse-selection evidence) |

### Handling IL / injured players

If a player is on IL with >4 weeks of expected recovery: `injury_discount = $value × (expected_missed_weeks / weeks_remaining)`. Apply BEFORE feeding into `trade_value_delta_raw`.

---

## Slot-Value Optionality

**Rationale (from game-theory-principles.md #9 — the 2-for-1 consolidation bonus):**

> Every open bench slot is worth ~$2–3 in optionality (streaming, IL stashes, handcuff speculation). A 2-for-1 trade that gives us the better player PLUS a freed bench slot is worth more than its raw player-value delta.

### Why bench slots have optionality value

A bench slot on a 26-man roster is a call option. You can spend it on:

1. **Streaming SPs**: a two-start week from a $0 FAAB pickup produces ~$1-2 of category value you would not otherwise capture.
2. **IL stashes**: a bench slot that parks an IL-returning player at pennies (via RotoWire's return-date tracker) converts into a mid-tier contributor.
3. **Handcuff speculation**: stashing the backup to your own (or a contested) closer insures against blow-ups at close to zero cost.
4. **Matchup rotations**: platoon the Util slot across two L/R bench bats for a lineup optimization worth ~$0.50-1.00/week of category points.

Summed over 20 weeks of regular season plus 3 playoff weeks, each bench slot conservatively returns $2-3 of category value. We use the midpoint of **$2.50** as the slot unit.

### The formula

```
N_slots_cleared_for_us   = max(0, players_OUT − players_IN)     # from our side
N_slots_cleared_for_them = max(0, players_IN  − players_OUT)    # from their side
slot_value_delta = (N_slots_cleared_for_us − N_slots_cleared_for_them) × $2.50
```

### Worked examples

| Shape | Our slots cleared | Their slots cleared | `slot_value_delta` |
|---|---|---|---|
| 1-for-1 | 0 | 0 | $0.00 |
| 2-for-1 (we send 2) | +1 | 0 | **+$2.50** |
| 1-for-2 (we send 1) | 0 | +1 | **−$2.50** |
| 3-for-2 (we send 3) | +1 | 0 | **+$2.50** |
| 3-for-1 (we send 3) | +2 | 0 | **+$5.00** |
| 2-for-3 (we send 2) | 0 | +1 | **−$2.50** |

### Symmetry is required

Always compute both sides. Do not credit yourself for a bench slot you free up while ignoring the bench slot the opponent frees on their side. The principle is explicit: the asymmetry works AGAINST us when *they* give up two.

### When `slot_value_delta` tips the verdict

The bonus is small in absolute dollars ($2.50 per cleared slot), but on a low-stakes 1-for-1 trade where `trade_value_delta_raw` is ±$3, the slot bonus can determine the sign. Do not skip it.

### Add to the pre-adjustment delta

```
trade_value_delta_pre_adj = trade_value_delta_raw + slot_value_delta
```

This is the number fed to Step 7 (adverse-selection haircut).

---

## Adverse-Selection Delegation

**Principle (from game-theory-principles.md #4):**

> If an opponent offered you this trade, they believe it's +EV for them. By Bayes: probability the offer is +EV for you is materially below 50%. The average player offered to you is worse than the average player of that name.

### Why we delegate, not recompute

The `@skills/adverse-selection-prior/` skill encapsulates the Akerlof market-for-lemons logic and is reused across:
- incoming trade offers (this skill);
- waiver drops by other teams (mlb-waiver-analyst);
- future negotiation/M&A use cases.

Centralizing keeps the Bayesian update logic single-source. The trade evaluator only prepares inputs and consumes the output contract.

### Input scoring for trade evaluations

When preparing inputs for `@skills/adverse-selection-prior/`:

#### `offer_type`

- Use `trade` for a fresh incoming offer.
- Use `counter_offer` when this is the opponent's response to a prior proposal we sent (tighter selection pressure, base prior 0.38 instead of 0.40).

#### `proposer_archetype`

Read from `context/opponents/<opponent-team>.md`, written by `mlb-opponent-profiler`. Expected values: `active`, `expert`, `dormant`, `frustrated`, `unknown`. If the file is missing or stale (>4 weeks old), use `unknown`.

#### `offer_symmetry_score` (0-100)

Derive from `trade_value_delta_pre_adj / Σ($_OUT)`:

| Ratio (pre-adj) | `offer_symmetry_score` |
|---|---|
| ≥ 0 | 72 (offer looks fair-to-favorable on our own numbers) |
| 0 to −10% | 60 (mildly asymmetric) |
| −10% to −25% | 40 (noticeably lopsided) |
| < −25% | 20 (predatory on surface — `adverse-selection-prior` will flag "too good to be true" if it's actually favorable) |
| > +20% | 85 (looks very favorable for us on surface — biggest red flag per Akerlof) |

#### `proposer_info_asymmetry` (0-100)

Start at 50. Apply these deltas:

- Add +30 if there is **recent injury/IL news** in the last 48 hours on any IN or OUT player.
- Add +20 if the opponent is classified `expert` (they likely track news faster than we do).
- Add +15 if closer roles are in flux on any affected team (cross-reference `mlb-closer-tracker`).
- Add +10 if trade is proposed within 72 hours of a `mlb-regression-flagger` signal change on an involved player.
- Subtract −10 if our own `mlb-regression-flagger` output strongly supports the trade being +EV for us (we have insight THEY may not).
- Subtract −10 if this is a repeated-game partner with >= 5 prior trades and no history of predatory offers.
- Clip to [0, 100].

### Consuming the output contract

The skill returns:
```
{
  "prior_ev_probability": float in [0.10, 0.70],
  "recommended_adjustment": float in [0.75, 1.00],
  "bayesian_rationale": string,
  "override_hints": string[]
}
```

Apply:

```
trade_value_delta_adjusted = trade_value_delta_pre_adj × recommended_adjustment
adverse_selection_adjustment_pct = (1 − recommended_adjustment) × 100   # e.g., 12%
```

Record `prior_ev_probability`, `recommended_adjustment`, and `adverse_selection_adjustment_pct` in the signal file frontmatter.

Embed `bayesian_rationale` verbatim in the verdict block's rationale section.

Add each `override_hints` entry as a `red_team_findings` item in the signal file (severity 3, likelihood 3, score 9 by default; raise if the override would flip the verdict).

### The sign-and-magnitude question

A multiplicative haircut on a positive delta shrinks it toward zero (good — it tempers our enthusiasm). A multiplicative haircut on a negative delta moves it further from zero (also correct — the prior says the actual EV is even worse than our pessimistic model).

Example:
- `trade_value_delta_pre_adj = +$10` on $50 outgoing → ratio +20%, pre-haircut looks like ACCEPT.
- `recommended_adjustment = 0.85` → `trade_value_delta_adjusted = +$8.50` → ratio +17%. Still clears +15% → ACCEPT survives.
- But if `recommended_adjustment = 0.75`: `trade_value_delta_adjusted = +$7.50` → ratio +15% on the nose. **Tie goes to COUNTER**, not ACCEPT.

---

## `positional_flex_delta` Scoring

Scored from −100 to +100. Neutral = 0.

| Move | Score |
|---|---|
| Gain a starter at a scarce position (C, SS) from a surplus position (OF, Util) | +30 |
| Lose a starter at a scarce position to a surplus position | −30 |
| Gain a starter at a moderately scarce position (2B, 3B) | +15 |
| Lose a starter at a moderately scarce position | −15 |
| Gain multi-position (2+ slots) eligibility | +15 |
| Lose multi-position eligibility | −15 |
| Consolidate 2 bench players into 1 starter (frees a bench slot) | +10 |
| Turn 1 starter into 2 bench players (fills bench) | −10 |
| Create an orphaned IL-only slot | −10 |
| Align SP count with 3 SP + 5 P (flex) starting slots | +10 to −10 depending on gap |
| Align RP count with 2 RP + 5 P (flex) starting slots | +10 to −10 |

**Roster reference**: 26 slots (1C, 1 1B, 1 2B, 1 3B, 1 SS, 3 OF, 2 Util, 3 SP, 2 RP, 5 P flex, 3 BN, 3 IL).

- **Scarce**: C, SS
- **Moderately scarce**: 2B, 3B
- **Abundant**: OF, P pool

Add contributions, clamp to [−100, +100].

**Note on interaction with `slot_value_delta`**: The flex delta captures STARTING-slot fit (scarce position gain/loss). The slot-value bonus captures BENCH-slot optionality from consolidation. They are independent axes — count both.

---

## `playoff_impact` (July+)

### Applicability

- Eval date < July 1: set `playoff_impact = 50` (neutral), note "N/A — pre-July."
- July 1 to July 14: compute, weight ×1.
- July 15 to Aug 6: compute, weight ×2 in verdict.

### Formula

```
contribution_player = playoff_games × playoff_matchup_quality
raw_playoff_delta = Σ contribution_IN − Σ contribution_OUT
playoff_impact = 50 + clamp(raw_playoff_delta / 200, −50, +50)
```

### Pitcher playoff_games = STARTS, not team games

Pull from Roster Resource probables grid.

---

## Verdict Ladder — Principle #8 and the Always-Counter Rule

**Principle (from game-theory-principles.md #8 — repeated-game reputation):**

> Over the season you will receive 15–30 trade offers from 11 distinct managers. If you reject fairly (with a counter and a brief rationale), you keep getting offers. If you reject dismissively, the pipeline dries up. This is a repeated cooperation game — cooperation breeds cooperation.

### Core insight

A fantasy league is a repeated game. The short-term gain from a pure REJECT (zero transaction cost) is wiped out by the long-term loss of trade-partner willingness. Every declined offer is also a relationship move.

**The always-counter rule**: in the middle band (`−20% < delta_pct < +15%`), we ALWAYS produce a specific counter-package. No exceptions, no pure REJECT in this band.

### The three-tier ladder

Compute `delta_pct`:

```
delta_pct = trade_value_delta_adjusted / Σ($_OUT)
```

Apply:

```
IF delta_pct >= +0.15
   AND no cat with pressure >= 80 has negative weighted delta
   AND advocate variant and critic variant agree:
   -> ACCEPT

ELIF -0.20 < delta_pct < +0.15:
   -> COUNTER (specific package required; see next section)

ELIF delta_pct <= -0.20
     AND prior_ev_probability <= 0.35:
   -> REJECT

ELSE (delta_pct <= -0.20 but prior_ev_probability > 0.35):
   -> COUNTER (with a more demanding package — the bad-value is on paper
      but adverse-selection signal is not confirming; counter to verify)
```

### Why the ACCEPT threshold is +15% and not +5%

Three reasons:

1. **Projection uncertainty.** ATC is the best available but still has ±20% error on individual counting stats. Demanding +15% ensures our signal exceeds the noise floor.
2. **The haircut is pre-applied.** `trade_value_delta_adjusted` already incorporates the adverse-selection prior. A +15% post-haircut delta corresponds to a ~+18-25% pre-haircut delta in typical cases — substantial.
3. **Asymmetric regret.** Accepting a bad trade costs a season; rejecting a good trade costs the incremental EV only. Be conservative on ACCEPT.

### Why the REJECT threshold is −20% AND adverse-selection evidence

- `delta_pct ≤ −20%` alone is not enough. A surface-bad-looking offer could be our projection model being off.
- `prior_ev_probability ≤ 0.35` means the adverse-selection skill returned strong evidence the opponent chose this offer because it is +EV for them.
- Both conditions together: clearly predatory, and refusing to even counter sends a legitimate signal.

If only one REJECT condition holds, downgrade to COUNTER with a tighter ask — this preserves the relationship signal while not capitulating on value.

### Advocate / critic variant agreement

For trades, run two variant passes:
- **Advocate**: assume the trade is good; find the steelmanned case to accept.
- **Critic**: assume the trade is predatory; find the hidden reason.

If they disagree on ACCEPT vs COUNTER, default to COUNTER. If they disagree on COUNTER vs REJECT, default to COUNTER (tie goes to counter, not reject, per the always-counter rule).

### Forced REJECT overrides (trumps delta_pct)

These still apply independent of the ladder:

- Any player IN is on IL with unknown return date → REJECT until return date is known.
- Evaluation is July 15+ and `playoff_impact` ≤ 40 → REJECT.
- Commissioner-review risk very high AND `delta_pct` ≥ +25% (commissioner likely reverses).

### Forced ACCEPT: rare

Only when `delta_pct ≥ +25%` AND `prior_ev_probability ≥ 0.45` AND all cats with pressure ≥ 80 are positive or zero. Even then, red-team why the opponent would make this offer.

---

## Counter-Offer Construction

When VERDICT = COUNTER (which is now the modal case, per always-counter rule), the output must be a **specific** counter-package.

### Procedure

**Step 1: Identify the gap.**
- Value gap: `delta_pct` below +15% by how much?
- Cat gap: which high-pressure cat has negative delta?
- Flex gap: scarce-position loss?

**Step 2: Scan the opponent's roster.** Pull their Yahoo team page. Identify players that close the gap:
- Value gap → a player worth roughly the missing dollars (after adverse-selection haircut applied in reverse)
- Cat gap → a player with strong projection in the specific cat
- Flex gap → a player at the scarce position

**Step 3: Propose the swap.** Two forms:
- **Add**: "Ask them to add [Player] to their side."
- **Swap**: "Ask them to swap [their Player X] for [their Player Y]."

**Step 4: Estimate acceptance probability.** A counter that closes half the gap is much more likely accepted than one that closes 100%. Prefer counters the opponent can rationalize.

**Step 5: Pre-commit to the fallback.**
- If middle-band COUNTER and they refuse: next counter we'd send, or REJECT on third refusal.
- If we REJECTED but are documenting the counter-we-would-have-sent (for relationship signal): include it in the signal file but note we're not sending it.

### Example: middle-band COUNTER

**Original offer:** Their Ronald Acuña Jr. for our Mookie Betts + José Ramírez.
**Pre-adj:** `trade_value_delta_pre_adj = −$6` on $52 out → ratio −11.5%.
**Haircut:** `recommended_adjustment = 0.90` → `trade_value_delta_adjusted = −$5.40`, `delta_pct = −10.4%`. Middle band.
**Gap:** value short by ~$13 to clear +15%.
**Counter:** "Ask them to add [their Juan Soto] to their side."
**Fallback:** If they refuse, send a smaller counter asking for [their Yoshinobu Yamamoto] instead. On second refusal, pre-commit to REJECT.

---

## Common Failure Modes

| Failure | Symptom | Fix |
|---|---|---|
| Skipped adverse-selection delegation | Signal file has no `prior_ev_probability` field | Invoke `@skills/adverse-selection-prior/` in Step 7; consume all four output fields |
| Applied haircut per-category | Cat deltas look suspiciously damped | Apply only to `trade_value_delta_pre_adj`, not to individual cat numbers |
| Forgot slot-value bonus | 2-for-1 trade not credited with +$2.50 | Compute in Step 6; always include both sides (symmetric) |
| Counted slot-value twice | Both in `slot_value_delta` and again in `positional_flex_delta` bench-consolidation | They are independent — bench optionality ($) vs starting-slot fit (flex score). Count both but do not reuse. |
| Pure REJECT in middle band | Verdict is REJECT despite `delta_pct > −20%` | Violates always-counter rule; downgrade to COUNTER with specific package |
| ACCEPT at `delta_pct` between +5% and +15% | Old threshold carried over | New threshold is +15%, not +5% |
| Used full-season not ROS projection | Hot-starter valued as if April repeats | Use `type=atcr` URL |
| Simple-averaged a ratio cat | OBP delta looks implausibly large or small | Volume-weight by PA |
| No `cat_pressure` applied | All cats weighted equally | Always read cat-state signal first |
| Vague counter ("ask for more") | User can't act on it | Propose specific named player from opponent's roster |
| Ignored IL status | Incoming player "worth" $30 but won't play for 6 weeks | Check RotoWire before any other step |
| Accepted a lopsided trade in our favor | Missed commissioner-review risk | Flag any `delta_pct ≥ +25%` for commissioner review |
| Ratio sign confusion | ERA/WHIP treated as "higher = better" | Flip sign before summing |
| Applied our pressures to opponent mirror table | Red-team check is garbled | Use raw deltas (or their actual pressures) on their side |
| Archetype not looked up | Inputs to adverse-selection-prior default to `unknown` when opponent file exists | Read `context/opponents/<team>.md` before Step 7 |

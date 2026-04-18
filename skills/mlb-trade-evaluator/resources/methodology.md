# MLB Trade Evaluator Methodology

Detailed procedures for rest-of-season projection sourcing, per-category delta math, `cat_pressure` weighting, dollar valuation, positional flex scoring, playoff impact, and reject-biased verdict logic.

## Table of Contents
- [Projection Sourcing](#projection-sourcing)
- [Counting Category Math](#counting-category-math)
- [Ratio Category Math](#ratio-category-math)
- [`cat_pressure` Weighting](#cat_pressure-weighting)
- [`trade_value_delta` — Dollar Valuation](#trade_value_delta--dollar-valuation)
- [`positional_flex_delta` Scoring](#positional_flex_delta-scoring)
- [`playoff_impact` (July+)](#playoff_impact-july)
- [Verdict Logic with Reject Bias](#verdict-logic-with-reject-bias)
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

**Always prefer `atcr` (rest-of-season) over `atc` (full season).** A player who has banked 20 HRs in April is worth less for the remaining 5 months than his full-season line implies. Using full-season projections systematically overvalues hot-start players.

### Fallback order

1. **FanGraphs Depth Charts** (`type=fangraphsdcr`) — hand-adjusts ATC for playing time. Use when a player's role has changed recently.
2. **Razzball Player Rater** — industry-standard fantasy value; good for sanity-checking ATC dollar values.
3. **FantasyPros ECR** — consensus rank; useful when the other two disagree by more than one tier.

### What to pull per player

**Hitters:**
- Remaining PAs (plate appearances)
- R (runs), HR, RBI, SB
- OBP (on-base percentage — the OBP-league variant is our scoring cat)

**Pitchers:**
- Remaining IP (innings pitched)
- K (strikeouts)
- ERA, WHIP
- QS (quality starts — a start with 6+ IP and ≤3 ER). FanGraphs reports QS directly on the ATC sheet. If missing, estimate as `IP / 30 × projected QS rate`.
- SV (saves) — for RPs only. Use save role certainty from `mlb-player-analyzer` to flag closers whose grip is loose.

### When projections conflict

If ATC and Depth Charts disagree by more than 15% on any counting stat, note both values in the signal file and use the **more conservative** of the two for delta math. This hews to the reject-bias: when in doubt, assume less value.

### When a player is on the IL

ATC does not always reprice quickly after an IL stint. Cross-check RotoWire injury report. If the projected return date will cost >4 weeks of games and ATC hasn't adjusted, manually scale the projection: `adjusted_proj = atc_ros × (games_remaining_after_return / total_ros_games)`.

---

## Counting Category Math

Counting cats: **R, HR, RBI, SB** (hitters) and **K, QS, SV** (pitchers). Seven total.

These are simple additive totals. The delta is:

```
raw_delta_C = Σ (projected_C of IN players) − Σ (projected_C of OUT players)
```

No scaling, no volume weighting. Just sum and subtract.

**Example — HR delta with Judge in, Witt + Strider out:**

```
IN total HR  = Judge(28) = 28
OUT total HR = Witt(20) + Strider(0) = 20
raw_delta_HR = 28 − 20 = +8
```

A positive counting-stat delta is unambiguously good; negative is bad.

### Special case: SV

Saves behave differently from other counting cats because they depend on the pitcher being in a defined closer role. A pitcher's SV projection is highly sensitive to role changes (demotions, injuries to the current closer, bullpen philosophy shifts).

- Always cross-reference `save_role_certainty` from `mlb-player-analyzer` before trusting an SV projection.
- If `save_role_certainty` < 70 for an IN or OUT RP, flag the trade as SV-volatile and reduce confidence by 0.1.

### Special case: QS

QS requires the starter to complete 6+ IP with ≤3 ER. Relief-oriented openers, bullpen-game SPs, and innings-limited rookies produce close to 0 QS regardless of K totals.

- Do not estimate QS as `Wins × 0.7` or similar heuristics. Use FanGraphs' direct QS projection.
- If missing, compute: `projected_QS = projected_GS × estimated_QS_rate` where QS rate is pulled from the pitcher's trailing 50-start history (Baseball Reference).

---

## Ratio Category Math

Ratio cats: **OBP** (hitters), **ERA** and **WHIP** (pitchers). Three total.

Ratio cats cannot be added. They must be **volume-weighted**.

### OBP delta — the correct math

A team's OBP is the PA-weighted average of its players' OBPs. The shift from a trade is:

```
Step 1. Compute volume-weighted OBP for the IN set:
        OBP_IN = Σ(OBP_i × PA_i) / Σ(PA_i)   over IN hitters

Step 2. Compute volume-weighted OBP for the OUT set:
        OBP_OUT = Σ(OBP_j × PA_j) / Σ(PA_j)  over OUT hitters

Step 3. Compute the team-level OBP before the trade:
        OBP_team_before = Σ(OBP_k × PA_k) / Σ(PA_k)  over all team hitters

Step 4. Compute the team-level OBP after the trade:
        OBP_team_after = (Σ_team_keep + Σ_IN) weighted the same way
        (i.e., replace the OUT players with the IN players in the roster sum)

Step 5. delta_OBP = OBP_team_after − OBP_team_before
        (typically a small number, e.g., +0.003 or −0.008)
```

**Why simple differences of averages are wrong:** a 250-PA .410 OBP hitter (small volume, big rate) contributes less to team OBP than a 450-PA .370 OBP hitter (big volume, moderate rate). Ignoring PAs treats them as equal — they are not.

### ERA delta — the correct math

```
Implied ER_i = ERA_i × IP_i / 9

ERA_IN = 9 × Σ(ER_i) / Σ(IP_i)  over IN pitchers
ERA_OUT = 9 × Σ(ER_j) / Σ(IP_j) over OUT pitchers

Team ERA shift computed same pattern as OBP (replace OUT with IN in team pool)

delta_ERA = ERA_team_after − ERA_team_before
```

**Sign convention for ERA:** lower is better. A negative delta is a GAIN. Record the delta with sign and flip it (multiply by −1) before summing into `trade_cat_delta` so that positive contributions to the sum mean "trade helps us."

### WHIP delta — the correct math

```
Implied baserunners_i = WHIP_i × IP_i
WHIP_IN = Σ(baserunners_i) / Σ(IP_i) over IN pitchers
```

Same sign-convention note as ERA: lower WHIP is better, flip sign before summing.

### Converting ratio deltas to the `trade_cat_delta` scale

The counting cats contribute raw integer deltas (tens or hundreds). The ratio deltas are tiny decimals (e.g., +.004 in OBP). To make them commensurable, scale:

- **OBP**: `scaled_delta_OBP = delta_OBP × 10,000` (so a .004 shift = 40 scaled points)
- **ERA**: `scaled_delta_ERA = −delta_ERA × 50` (sign flipped; 0.10 ERA improvement = +5 points)
- **WHIP**: `scaled_delta_WHIP = −delta_WHIP × 200` (sign flipped; 0.02 WHIP improvement = +4 points)

These scalings are calibrated so that one "point" of ratio-cat delta is roughly one counting-cat unit at the team level. Use them consistently; document in the signal file.

---

## `cat_pressure` Weighting

### Read the signal

Open the most recent `signals/YYYY-MM-DD-cat-state.md`. It contains `cat_pressure` (0-100) for each of the 10 cats. If it does not exist for today, **stop and run `mlb-category-state-analyzer` first.**

### Apply the weight

```
weight_C = cat_pressure_C / 50

weighted_delta_C = raw_delta_C (or scaled ratio delta) × weight_C

trade_cat_delta = Σ weighted_delta_C  over all 10 cats
```

### Interpretation of the weight

| `cat_pressure` | weight | Meaning |
|---|---|---|
| 0 | 0.0 | Punt category — this cat does not factor into the verdict at all |
| 25 | 0.5 | Low importance — we're comfortably ahead or behind; mild discounting |
| 50 | 1.0 | Neutral — normal weight |
| 75 | 1.5 | High importance — matchup hinges on this cat |
| 100 | 2.0 | Critical — losing (or winning) this cat would swing the entire week |

### Why pressure-weighting is load-bearing

A +5 HR delta means very different things:
- If we're already winning HR by 8 this week (low pressure): worth little
- If we're tied in HR and this is a cat we always compete for (high pressure): worth a lot

Flat-weighted deltas systematically mis-rank trades by ignoring this. The category-strategist already paid the thinking cost; the trade evaluator just reads its output.

### Caveat: opponent's `cat_pressure` is not ours

Do not apply our `cat_pressure` weights to the mirror-side table (the opponent's gain/loss). Their pressures are different. For the mirror table, either:
- Skip the weighting step (use raw deltas), or
- Estimate their pressures from their current standings in each cat (requires additional web search of league standings page).

The mirror table is primarily a red-team check: does the opponent get a package that "solves" a known weakness of theirs? If so, that's a signal the offer is extractive.

---

## `trade_value_delta` — Dollar Valuation

### Primary source: FanGraphs Auction Calculator

- URL: `https://www.fangraphs.com/auction-calculator`
- Set league parameters to **12-team, H2H categories, standard roster, 5x5 (OBP variant)**.
- Pull rest-of-season dollar values for each player.

### Formula

```
trade_value_delta = Σ($_ROS of IN players) − Σ($_ROS of OUT players)
```

### Calibration buckets

| Value delta | Bucket | Implication |
|---|---|---|
| ≥ +$10 | Clear gain | Strong ACCEPT signal (still check cats and flex) |
| +$5 to +$10 | Modest gain | Lean ACCEPT |
| −$5 to +$5 | Noise | Verdict driven by cats, flex, and playoff impact |
| −$10 to −$5 | Modest loss | Lean REJECT |
| ≤ −$10 | Clear loss | REJECT unless overwhelmingly positive on cats AND fixes critical positional gap |

### Fallback: Razzball Player Rater

If FanGraphs AC is unreachable, Razzball's dollar-value rater approximates well for standard leagues. Flag confidence drop to 0.6 because Razzball doesn't natively account for OBP scoring — adjust manually: +$2-$4 for high-walk hitters, −$2-$4 for free-swingers.

### Handling IL / injured players in dollar valuation

Auction calculators typically value healthy seasons. If a player is on IL with >4 weeks of expected recovery, subtract: `injury_discount = $value × (expected_missed_weeks / weeks_remaining)`.

---

## `positional_flex_delta` Scoring

Scored from −100 to +100. Neutral = 0. Measures how the trade changes roster flexibility.

### Base scoring

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

### Roster reference (from `league-config.md`)

- 26 roster slots: 1C, 1 1B, 1 2B, 1 3B, 1 SS, 3 OF, 2 Util, 3 SP, 2 RP, 5 P (flex), 3 BN, 3 IL
- **Scarce positions**: C (1 slot only), SS (1 slot, thin talent pool)
- **Moderately scarce**: 2B, 3B
- **Abundant**: OF (3 starters + Util), P (10 total pitcher slots)

### Sum and clamp

Add the individual scores, then clamp to [−100, +100]. Record each factor's contribution in the template's flex block.

---

## `playoff_impact` (July+)

### Applicability

- Evaluation date < July 1: set `playoff_impact = 50` (neutral) and note "N/A — pre-July."
- Evaluation date July 1 to July 14: compute, but weight it normally (×1 in the verdict).
- Evaluation date July 15 to August 6 (deadline): compute and **double-weight** in the verdict. Trades made this close to the deadline must clearly improve the playoff schedule.

### Formula

For each player, pull:
- `playoff_games` (int): games in weeks 21+22+23, from `mlb-playoff-scheduler` signal or FanGraphs team schedule
- `playoff_matchup_quality` (0-100): from `mlb-playoff-scheduler` signal

```
contribution_player = playoff_games × playoff_matchup_quality

raw_playoff_delta = Σ contribution_IN − Σ contribution_OUT

playoff_impact = 50 + clamp(raw_playoff_delta / normalizer, −50, +50)
where normalizer = 200   (calibrated so ±200 raw = ±50 scaled)
```

### Interpretation

| `playoff_impact` | Meaning |
|---|---|
| ≥ 60 | Trade meaningfully improves our playoff-week lineup |
| 50-60 | Slight playoff improvement |
| 45-55 | Playoff-neutral |
| 40-50 | Slight harm |
| ≤ 40 | Meaningful harm — strong REJECT signal in mid-July+ |

### Common trap: pitching playoff-impact

For SPs, `playoff_games` is actually projected *starts* in those 3 weeks, not team games. A 2-start week beats a 1-start week by a factor of 2. Pull start counts from Roster Resource probables grid, not the team schedule.

---

## Verdict Logic with Reject Bias

**Core principle: most trade offers are extractive. Default to REJECT. Require the math to clearly justify ACCEPT.**

### Decision tree

```
IF (trade_value_delta ≥ +$5)
   AND (trade_cat_delta (weighted) > +30)
   AND (positional_flex_delta ≥ 0)
   AND (no cat with pressure ≥ 80 has a negative weighted delta)
   AND (playoff_impact ≥ 50 if applicable):
   → ACCEPT

ELIF (trade_value_delta ≥ −$5)                             # within noise band
     AND (trade_cat_delta (weighted) ≥ 0)                  # non-negative overall
     AND (no cat with pressure ≥ 80 is negative):
   → COUNTER (propose specific improved package; see next section)

ELSE:
   → REJECT
```

### Why the bias toward REJECT works

Four reasons:

1. **Adverse selection.** The opponent chose us as the target. They believe this trade improves their team. If they're right, we lose by accepting.
2. **Projection uncertainty.** ATC is the best available but still has ±20% error on individual counting stats. Small positive deltas (<+$5) are indistinguishable from noise.
3. **Transaction cost is zero to refuse.** Rejecting costs nothing. Accepting a bad trade costs a full season.
4. **Counter is free insurance.** If the trade is close to fair, asking for more never harms — worst case, they refuse and we end where we started.

### Forced REJECT overrides (trumps any other math)

- Any cat with `cat_pressure ≥ 80` has negative weighted delta → REJECT.
- `trade_value_delta ≤ −$10` → REJECT.
- `positional_flex_delta ≤ −30` → REJECT.
- Evaluation is July 15+ and `playoff_impact ≤ 40` → REJECT.
- Any player IN is on IL with unknown return date → REJECT until return date is known.

### Forced ACCEPT: rare

Only when all five ACCEPT conditions are met AND `trade_value_delta ≥ +$10`. Even then, a red-team pass should sanity-check why the opponent would make this offer (maybe they know something the projections don't).

---

## Counter-Offer Construction

When VERDICT = COUNTER, the output must be a **specific** counter-package, not a general "ask for more."

### Procedure

**Step 1: Identify the gap.** What's the shortfall that pushed this from ACCEPT to COUNTER? Usually one of:
- Value is short by $X
- One high-pressure cat has a negative delta
- Positional flex is marginally negative

**Step 2: Scan the opponent's roster.** Pull the opponent's Yahoo team page. Identify players that would close the specific gap:
- Value gap → a player worth +$X
- Cat gap → a player with strong projection in that specific cat
- Flex gap → a player at the scarce position

**Step 3: Propose the swap.** Two forms:
- **Add**: "Ask them to add [Player] to their side."
- **Swap**: "Ask them to swap [their Player X] for [their Player Y]."

**Step 4: Estimate acceptance probability.** If the counter is obviously extractive from their side, it will be refused. Prefer counters that the opponent can rationalize (e.g., we're asking for a player they have on their bench, not a key starter).

**Step 5: Pre-commit to the fallback.** "If they refuse, REJECT." Never leave the counter open-ended.

### Example counter construction

**Original offer:** Their Judge for our Witt + Strider.
**Verdict math:** value −$24, cat delta −217 weighted (SB, K, QS all hammered).
**Gap:** too much pitching given up.
**Counter:** "Ask them to add [their Logan Webb] to their side. This replaces the K and QS we're giving up with Strider."
**Fallback:** REJECT if they refuse to add Webb.

---

## Common Failure Modes

| Failure | Symptom | Fix |
|---|---|---|
| Used full-season not ROS projection | Hot-starter valued as if April repeats for 5 more months | Use `type=atcr` URL on FanGraphs |
| Simple-averaged a ratio cat | OBP delta looks implausibly large or small | Volume-weight by PA per [Ratio Category Math](#ratio-category-math) |
| No `cat_pressure` applied | All cats weighted equally; trade looks good but mishandles the cats we actually need | Always read cat-state signal first |
| Vague counter ("ask for more") | User can't act on it | Propose a specific player name from the opponent's roster |
| Ignored IL status | Incoming player "worth" $30 but won't play for 6 weeks | Check RotoWire before any other step |
| Accepted a lopsided trade in our favor | Missed that the commissioner will review and reverse | Flag any trade where `trade_value_delta ≥ +$20` for commissioner-review risk |
| Ratio sign confusion | ERA and WHIP treated as "higher = better" | Flip sign (multiply by −1) before summing; lower ERA/WHIP is a gain |
| Over-valued a closer | SV projection assumed stable closer role | Check `save_role_certainty`; drop projection if < 70 |
| Applied our pressures to opponent mirror table | Red-team check is garbled | Use raw deltas (or their actual pressures) on their side |
| Missed the bias-toward-reject | Verdict is ACCEPT on a trade that's essentially fair | Re-check: did all five ACCEPT conditions hold, not just some? |

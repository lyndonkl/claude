---
name: mlb-category-state-analyzer
description: Computes the weekly category state for a Yahoo H2H Categories matchup across all 10 scoring categories (R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV). For each cat, emits cat_position (winning/tied/losing), cat_pressure (0-100 urgency), cat_reachability (0-100 flip probability), and cat_punt_score (0-100 concede sensibility). Produces an overall "push 6, punt N" recommendation that drives waiver, streaming, and lineup decisions downstream. Use when user asks about "category state", "where am I winning", "should I punt", "matchup score", "cat pressure", weekly category planning, or which cats to push vs. concede.
---
# MLB Category State Analyzer

## Table of Contents
- [Example](#example)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Example

**Scenario**: Week 3, K L's Boomers (Team 5) vs. Los Doyers. Wednesday AM (mid-week). 4 scoring days remain.

**Raw matchup scores (pulled from Yahoo matchup page)**:

| Cat | Us | Opp | Margin | Games left (us/opp) |
|---|---|---|---|---|
| R | 28 | 31 | -3 | 26 / 22 |
| HR | 9 | 7 | +2 | 26 / 22 |
| RBI | 30 | 29 | +1 | 26 / 22 |
| SB | 4 | 6 | -2 | 26 / 22 |
| OBP | .342 (82 PA) | .336 (78 PA) | +.006 | 26 / 22 GP |
| K | 42 | 38 | +4 | 9 SP starts / 7 SP starts |
| ERA | 3.80 (21 IP) | 4.12 (19 IP) | -0.32 (better) | 9 / 7 |
| WHIP | 1.18 (21 IP) | 1.25 (19 IP) | -0.07 (better) | 9 / 7 |
| QS | 2 | 1 | +1 | 9 / 7 |
| SV | 3 | 5 | -2 | ~8 RP days / ~8 RP days |

**Per-cat signals (computed — see [resources/methodology.md](resources/methodology.md))**:

| Cat | Position | Pressure | Reachability | Punt Score | Verdict |
|---|---|---|---|---|---|
| R | losing | 72 | 68 | 22 | push |
| HR | winning | 48 | 70 | 18 | maintain |
| RBI | winning (thin) | 65 | 55 | 30 | push |
| SB | losing | 55 | 40 | 58 | evaluate punt |
| OBP | winning (thin) | 70 | 60 | 25 | push (unusual cat — see below) |
| K | winning | 55 | 72 | 15 | push |
| ERA | winning | 62 | 58 | 28 | push |
| WHIP | winning | 60 | 55 | 32 | maintain |
| QS | winning | 78 | 82 | 10 | push hard (volume edge) |
| SV | losing | 38 | 32 | 72 | punt candidate |

**Overall recommendation**: **Push 6, maintain 2, punt 2.**

- **Push (6)**: R, RBI, OBP, K, ERA, QS — close or pushable with reachability ≥ 55.
- **Maintain (2)**: HR, WHIP — lead is comfortable, don't overspend roster moves here.
- **Punt (2)**: SB (low reachability, single stolen-base threat unlikely) and SV (volatile, opp closer dominance, punt score 72).

**Downstream implications for other agents**:
- Waiver analyst: prioritize SP (QS, K, ERA), OBP-heavy bats (walks), not closers or speed.
- Streaming strategist: every QS-capable SP gets a start this week; skip any 5-inning risk arms.
- Lineup optimizer: prefer high-OBP bats (walks count) over BA/power-only bats; sit SB-only specialists.

## Workflow

Copy this checklist and track progress:

```
MLB Category State Analysis Progress:
- [ ] Step 1: Pull current matchup scores from Yahoo
- [ ] Step 2: Count remaining games/PAs/IP for both rosters
- [ ] Step 3: Project remaining production per cat
- [ ] Step 4: Compute cat_position, cat_pressure, cat_reachability, cat_punt_score for all 10 cats
- [ ] Step 5: Rank cats and emit push/maintain/punt plan
- [ ] Step 6: Write signal file with YAML frontmatter
```

**Step 1: Pull current matchup scores**

Web-fetch the Yahoo matchup page: `https://baseball.fantasysports.yahoo.com/b1/23756/5/matchup?week=N`. Extract current totals for both teams in each of the 10 cats. For ratio cats (OBP, ERA, WHIP), also capture the denominator (PAs for OBP, IP for ERA/WHIP). This is **required** — you cannot compute reachability without the volume underlying the ratio.

- [ ] 5 batting cats: R, HR, RBI, SB, OBP (+ at-bats / plate-appearances)
- [ ] 5 pitching cats: K, ERA, WHIP, QS, SV (+ innings pitched)
- [ ] Source URL cited in signal file

See [resources/methodology.md](resources/methodology.md#pulling-matchup-data-from-yahoo) for scrape procedure and fallback if Yahoo is unreachable.

**Step 2: Count remaining games/PAs/IP**

For each roster, count the number of MLB games its players will play for the rest of the scoring period, and project PAs (hitters) and IP (pitchers).

- [ ] Hitter games remaining: sum of (each rostered hitter's team games × probability they start)
- [ ] Pitcher starts remaining: number of scheduled SP starts for the rest of the week per roster
- [ ] Reliever days remaining: days × eligible RPs (for SV projection)
- [ ] Volume imbalance: if one team has meaningfully more games, that matters for `cat_pressure`

Use MLB.com schedules + probable pitcher grids. See [resources/methodology.md](resources/methodology.md#projecting-remaining-games).

**Step 3: Project remaining production per cat**

For each cat, estimate expected remaining production.

- [ ] **Counting cats** (R, HR, RBI, SB, K, QS, SV): expected contribution = sum over roster of (per-game rate × games remaining)
- [ ] **Ratio cats** (OBP, ERA, WHIP): project final ratio as weighted average of (current ratio × current volume) + (projected ratio × remaining volume) / total volume
- [ ] Document per-cat projections for both rosters

**Step 4: Compute per-cat signals**

Apply the formulas in [resources/methodology.md](resources/methodology.md#signal-formulas) (these implement `context/frameworks/category-math.md`).

- [ ] `cat_position` ∈ {winning, tied, losing} — current state
- [ ] `cat_pressure` (0–100) — how much to push
- [ ] `cat_reachability` (0–100) — can we flip/hold given volume remaining
- [ ] `cat_punt_score` (0–100) — how sensible to concede

For **ratio cats** (OBP, ERA, WHIP), use best/expected/worst-case crossing logic. For **counting cats**, use deficit-vs-expected-remaining. See the worked examples for OBP, SV, and QS in the methodology file.

**Step 5: Rank and emit plan**

Rank all 10 cats by `cat_pressure × cat_reachability / 100`:

- [ ] **Top 6**: push — mark these as priority for waivers, streams, starts
- [ ] **Middle 2**: maintain — hold position, don't overspend
- [ ] **Bottom 2**: evaluate punt — if `cat_punt_score > 60`, confirm punt; otherwise hold

Goal in H2H Cats is 6-of-10. A defensible plan is "push 6, concede up to 4." See [resources/template.md](resources/template.md#per-cat-signal-table) for the output signal format.

**Step 6: Write signal file**

Write to `signals/YYYY-MM-DD-cat-state.md` with YAML frontmatter (type: `cat-state`). Validate with `mlb-signal-emitter` before persisting.

- [ ] All 10 cats present with all 4 signals each
- [ ] Confidence reflects data quality (lower if Yahoo scrape was partial)
- [ ] `source_urls` includes Yahoo matchup page + MLB.com schedule pages
- [ ] Red-team findings noted (e.g., "Opp has a two-start ace coming that could flip K + ERA + WHIP all at once")

Validate output using [resources/evaluators/rubric_mlb_category_state_analyzer.json](resources/evaluators/rubric_mlb_category_state_analyzer.json). Minimum: average score of 3.5 or above.

## Common Patterns

**Pattern 1: Balanced mid-week state**
- Typical Wednesday AM state: 3-4 cats already locked, 3-4 close, 2-3 volatile.
- Action: push the close cats hardest, coast the locked wins, ignore locked losses.

**Pattern 2: Volume-imbalanced matchup**
- We have 30 hitter games left, opp has 22. We get a free pressure-boost on every counting batting cat.
- Action: stack the lineup (fewer off-days, prefer teams playing doubleheaders), bid on streamers.

**Pattern 3: Two-start ace incoming (us or them)**
- One pitcher's two-start week can swing K, ERA, WHIP, QS simultaneously.
- If **we** have the two-start ace: pressure up on all 4 pitching ratio/counting cats, push hard.
- If **opp** has the two-start ace: reachability on K/ERA/WHIP drops sharply; consider conceding one of those three and re-allocating.

**Pattern 4: Save-category volatility**
- SVs are low-frequency, one-walkoff-blown-save can flip the category.
- If behind by 2+ with only 3-4 days left and no second closer on roster, `cat_punt_score` almost always exceeds 60 — punt and use bench slot for a streamer instead.

**Pattern 5: Ratio-cat "freeze"**
- Late in the week, if opp is far below the IP/PA minimum (e.g., has 9 IP on Friday with no more starts), their ratio cats are locked at whatever they have.
- Compute our mathematical ceiling/floor to see if we've clinched or lost those cats regardless of action.

## Guardrails

1. **Never compute OBP/ERA/WHIP from rates alone — always include volume (PA/IP).** A .400 OBP in 10 PAs is not better than .342 in 82 PAs. Reachability hinges on the weighted-average calculation, which requires the denominator.

2. **QS is the #1 category, not Wins.** This league uses Quality Starts (6+ IP, ≤3 ER). A 5-inning outing scores zero. When projecting remaining QS, multiply each SP start by its QS probability (from `mlb-player-analyzer`'s `qs_probability` signal) — don't just count scheduled starts.

3. **OBP is the #5 category, not AVG.** Walks count. When projecting OBP contribution, use players' OBP (not AVG). A high-BB, low-AVG player like Juan Soto is worth more in this league than his raw hit rate suggests.

4. **SV is volatile — trust the punt when signals agree.** Unlike counting batting cats, a 2-save deficit with 3 days left has low reachability regardless of roster. Don't fight for saves if the closer role on your roster isn't locked (check `save_role_certainty` < 70 → automatic punt candidate).

5. **Don't double-count the "close margin" boost.** The `cat_pressure` formula adds +20 for close margin and +15 for volume advantage. A single cat can have both, but the clamp to [0, 100] still applies. Sanity-check any cat with pressure > 90.

6. **Locked-in cats get pressure adjustments, not zero.** A locked-in win still has `cat_pressure ≈ 40` (it's banked). A locked-in loss still has `cat_pressure ≈ 20` (stop investing). Don't set them to zero — downstream agents use non-zero values to decide bench vs. drop.

7. **Ratio cats need the minimum-IP/PA rule.** Yahoo enforces minimums for pitcher ratio cats (usually 20 IP for the week). If either roster is tracking below the minimum late in the week, the ratio cat may auto-loss. Factor this into `cat_reachability` — if opp is at 8 IP with 2 days left and no starts scheduled, they may forfeit ERA/WHIP automatically.

8. **Never re-derive upstream signals.** `qs_probability`, `sb_opportunity`, `obp_contribution`, `save_role_certainty` come from `mlb-player-analyzer`. Read them from the signal directory; do not recompute.

## Quick Reference

**Category math (from `context/frameworks/category-math.md`):**

```
cat_pressure =
    50                                         # neutral baseline
  + 20 × (is_close_margin: deficit/lead ≤ 10% of total)
  + 15 × (opponent_volume_exhausted: we have more games left)
  - 10 × (locked_in_win)
  - 30 × (locked_in_loss)
  clamp(0, 100)

Counting cats (R, HR, RBI, SB, K, QS, SV):
  cat_reachability = 100 × P(Σ expected_remaining ≥ deficit)

Ratio cats (OBP, ERA, WHIP):
  cat_reachability = 100 × P(projected final ratio crosses opponent projected final)
  (Monte-Carlo mental: worst / expected / best)

cat_punt_score =
    (100 - cat_reachability) × 0.6
  + 30 × (cat is traditionally volatile: SV)
  + 20 × (below min-PA/IP threshold)
  - 10 × (cat has spillover: K feeds QS; OBP feeds R)
```

**League constants (from `context/league-config.md`):**

- 10 cats: **R, HR, RBI, SB, OBP, K, ERA, WHIP, QS, SV**
- OBP (not AVG) — walks matter
- QS (not W) — 6+ IP with ≤3 ER
- H2H Cats, goal = win 6+ of 10 each week
- Daily lineup lock; weekly matchup rolls Mon-Sun

**Signal file output schema (from `context/frameworks/signal-framework.md`):**

```yaml
---
type: cat-state
date: YYYY-MM-DD
emitted_by: mlb-category-state-analyzer
week: N
matchup_opponent: <team name>
scoring_days_remaining: N
synthesis_confidence: 0.0-1.0
source_urls:
  - https://baseball.fantasysports.yahoo.com/b1/23756/5/matchup?week=N
---
```

Body: per-cat table + overall push/maintain/punt recommendation + red-team findings.

**Thresholds used downstream:**

| Agent | Threshold | Effect |
|---|---|---|
| Waiver analyst | `cat_pressure ≥ 60` | Prioritize targets that fill that cat |
| Streaming strategist | `cat_pressure (ERA/WHIP) < 30` | Allow riskier streamers (we're punting) |
| Lineup optimizer | `cat_pressure (SB) < 40` | Deprioritize speed-only specialists |
| Trade analyzer | weights `trade_cat_delta` | Multiplied by `cat_pressure / 50` |

**Key resources:**

- **[resources/template.md](resources/template.md)**: Output signal file format, per-cat table, push/maintain/punt recommendation block
- **[resources/methodology.md](resources/methodology.md)**: Full signal formulas, Yahoo scrape procedure, remaining-games projection, counting vs. ratio cat math, worked examples for OBP/SV/QS
- **[resources/evaluators/rubric_mlb_category_state_analyzer.json](resources/evaluators/rubric_mlb_category_state_analyzer.json)**: 8-criterion evaluator rubric

**Inputs required:**

- Current matchup scores (10 cats, both teams, with volume for ratio cats)
- Roster IDs for both teams
- Remaining MLB schedule through Sunday
- Upstream signals: `qs_probability`, `save_role_certainty`, `obp_contribution`, `sb_opportunity`
- League config (cats list, min-IP/PA thresholds)

**Outputs produced:**

- `signals/YYYY-MM-DD-cat-state.md` — signal file with 10-cat table, overall plan, confidence, source URLs
- `cat_position`, `cat_pressure`, `cat_reachability`, `cat_punt_score` per cat
- Overall "push N, maintain M, punt P" recommendation (N + M + P = 10, target N ≥ 6)

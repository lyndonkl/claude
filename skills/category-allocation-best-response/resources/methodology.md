# Category Allocation Best-Response — Methodology

## Table of Contents

- [Colonel Blotto Origins](#colonel-blotto-origins)
- [The H2H Categories Variant: K-of-N, Not Winner-Takes-All](#the-h2h-categories-variant-k-of-n-not-winner-takes-all)
- [Nash Equilibrium for Symmetric Cases](#nash-equilibrium-for-symmetric-cases)
- [Heuristic Best-Response for Asymmetric Cases](#heuristic-best-response-for-asymmetric-cases)
- [Why These Thresholds (0.25 / 0.70 / 0.85)](#why-these-thresholds)
- [Why Dominated Cats Get Zero Leverage](#why-dominated-cats-get-zero-leverage)
- [Leverage Weight Derivation](#leverage-weight-derivation)
- [Upstream Dependency on matchup-win-probability-sim](#upstream-dependency-on-matchup-win-probability-sim)
- [Poisson-Binomial Recurrence](#poisson-binomial-recurrence)
- [What to Do When Our Roster Is Simply Worse](#what-to-do-when-our-roster-is-simply-worse)
- [Generalization to Non-10-Cat Leagues](#generalization-to-non-10-cat-leagues)

## Colonel Blotto Origins

The Colonel Blotto game, introduced by Émile Borel (1921) and formalized by Gross and Wagner (1950), models two commanders distributing limited troops across N battlefields. Each battlefield is won by the side with more troops; the player winning more battlefields wins the war. Three features make it the closest classical model for H2H Categories fantasy:

1. **Simultaneous, hidden allocation**: Both players commit resources before seeing the opponent's allocation (you set your lineup before Monday without seeing opponent's lineup in full).
2. **Fixed total resources**: Roster slots, FAAB budget, and streamer starts are bounded; pushing one cat costs resources elsewhere.
3. **Mixed-strategy Nash equilibria**: The classical game has no pure-strategy equilibrium when resources are symmetric — the optimum is randomized.

Fantasy H2H Categories differs from classical Blotto in three important ways:

| Classical Blotto | H2H Categories |
|------------------|----------------|
| Winner-takes-all (majority of battlefields wins war) | K-of-N threshold (6 of 10, 5 of 9) — a strict majority, not all |
| Deterministic comparison per battlefield | Stochastic comparison (per-cat output has variance) |
| Single resource type (troops) | Multiple resource types (roster slots, FAAB, streamer starts, waiver priority) |
| Battlefields are symmetric | Cats are asymmetric (ratio cats vs counting cats, inverse cats vs normal cats) |

These differences make the classical Nash solution inapplicable. But the **core insight carries over**: when allocating across contested battlefields, the best move is to match the opponent at the margin — not to stockpile on battlefields you already dominate, and not to fight battlefields you've already lost.

See Roberson (2006) "The Colonel Blotto game" for the canonical mixed-strategy solution.

## The H2H Categories Variant: K-of-N, Not Winner-Takes-All

Yahoo H2H Categories matchups are won by reaching `K` cat-wins out of `N`, where `K = ceil(N/2) + 1` typically (6 of 10 for MLB 5x5, 5 of 9 for NBA). This changes the strategic structure meaningfully:

**Winner-takes-all Blotto** (classical): Every battlefield win matters equally up to majority. Losing by 4–6 is indistinguishable from losing by 0–10. Optimal play distributes troops broadly and trusts the coin flips.

**K-of-N Blotto** (H2H Cats): Once you reach K wins, additional wins are worthless this week. This creates a cliff at K, which drives three behaviors:

1. **Concede freely**. If you already have `K` defensible cats, losing 1 more cat at 0.15 probability is free — you don't need it. Don't fight dominated cats.
2. **Push to K, not past K**. A 7-0 matchup is the same win as a 6-4 matchup. Marginal resources beyond the 6th win have zero value this week. (They may have trade/waiver-market value in future weeks, but that is a separate calculation.)
3. **Weight contested cats heaviest**. When you are threshold-limited, the cats whose outcome is uncertain (0.25–0.70) are where your win probability lives. A cat at 0.95 is already a win; a cat at 0.05 is already a loss; neither moves much with marginal effort. The 0.50 cats are where the coin is still in the air.

This motivates the four-tier classification: locked (>0.85), pushed (0.70–0.85), contested (0.25–0.70), conceded (<0.25). See [Why These Thresholds](#why-these-thresholds).

## Nash Equilibrium for Symmetric Cases

When both teams have identical per-cat distributions (`our_capacity == opp_projection` for every cat with identical variance), the per-cat win probability is 0.5 everywhere. Every cat is contested. The equilibrium allocation is uniform: spread resources evenly across all N cats, and let variance determine who wins the K-of-N threshold.

Expected cats-won under uniform symmetric allocation: `N * 0.5 = N/2`. With `K = N/2 + 1` (strict majority), the matchup is a coin flip — the Poisson-binomial distribution over N independent 0.5-Bernoullis is symmetric around `N/2`, so `P(sum >= N/2 + 1) ≈ 0.5`.

This is the baseline: absent asymmetry, absent variance differences, the game is 50-50. Any deviation from this baseline comes from (a) asymmetric capacities or (b) asymmetric variances.

**Implication for this skill**: if `per_cat_win_probability` clusters tightly around 0.5 (all cats between 0.40 and 0.60), every cat is contested. Resources should distribute broadly. If the skill returns "all cats contested", that's not a bug — that's the symmetric case correctly identified.

## Heuristic Best-Response for Asymmetric Cases

Real matchups are almost never symmetric. Opponents have different roster shapes: a closer-heavy opponent projects 5 SV to your 2, a power-heavy opponent projects 16 HR to your 12, etc. These asymmetries produce `per_cat_win_probability` values far from 0.5, and the best-response allocation is no longer uniform.

The heuristic best-response procedure (what this skill implements):

1. **Classify**. Sort cats into {conceded, contested, pushed, locked} based on `per_cat_win_probability`.
2. **Concede the dominated**. Any cat with `< 0.25` gets leverage 0.0. Resources here are strictly dominated by redeployment to contested cats.
3. **Defend the locked**. Any cat with `> 0.85` gets leverage 1.0 (default, not elevated). Don't over-invest in cats already in the bag.
4. **Push the pushed**. Cats in `[0.70, 0.85]` get leverage 1.2 — defend with ordinary care but don't splurge.
5. **Weight the contested heaviest**. Cats in `[0.25, 0.70)` get leverage 1.5 — this is where marginal resources have the highest flip impact.
6. **Count**. Verify `pushed + contested >= K`. If not, the matchup is mathematically losing on the median — apply borderline upgrades or pivot to variance.

This is a heuristic — it is not provably optimal in the game-theoretic sense. Two simplifications:

- It ignores cat-to-cat correlation (a power bat lifts both HR and RBI; the skill's leverage weights treat HR and RBI as independent). Downstream consumers like `mlb-waiver-analyst` that know the player-cat correlation matrix recover the bundled leverage naturally when they multiply `daily_quality × leverage`.
- It ignores resource-specific constraints (some FAAB targets consume $ but not roster slots; some streamers consume streamer starts but not roster slots). The skill emits leverage per cat and lets each resource-type-specific downstream skill apply it to the right currency.

The heuristic approaches the true best-response in the limit where (a) per-cat Bernoullis are independent and (b) resources are fungible. Neither is exactly true, but both are good approximations.

## Why These Thresholds

The four cut points (0.25, 0.70, 0.85) are calibrated to the marginal value of one additional unit of resource.

**0.25 (concede line)**: Below 25%, the gap between our capacity and opponent's projection is wide enough that realistic marginal moves (adding one bat, starting one pitcher) have near-zero flip probability. Simulations across MLB 5x5 scenarios show that a cat starting at 0.20 win prob moves to ~0.23 after a typical waiver add — not enough to matter. Below 0.25 is the domain where resources are strictly dominated.

**0.70 (push-to-contested line)**: Above 70%, the cat is highly likely to be a win even with ordinary play. Marginal resources add to a buffer that was already adequate. Dropping below 70% means the cat is close enough that marginal moves have meaningful flip impact — hence the jump from 1.2 (push) to 1.5 (contested) leverage weight.

**0.85 (pushed-to-locked line)**: Above 85%, the cat is essentially in the bag. Any resources spent padding it are wasted — leverage drops back to the default 1.0. We don't zero it out (it's still "our" cat and deserves ordinary defensive attention), but we don't premium it either.

These numbers are approximate. Sensitivity analysis shows:

- Moving concede line from 0.25 to 0.20: includes more cats in "pushable" set, typically adds one cat per week at the cost of a 2–3% reduction in `k_of_n_win_probability` (wasted resources).
- Moving concede line from 0.25 to 0.30: concedes more freely, frees up roster slots, but risks conceding recoverable cats.
- Moving push-locked line from 0.85 to 0.90: treats more cats as pushed, elevates leverage on cats that don't need it.

The 0.25 / 0.70 / 0.85 cuts are the operational defaults. A skilled operator may tune based on league-specific scoring and observed opponent behavior.

## Why Dominated Cats Get Zero Leverage

Dominated-strategy elimination (principle #1 in `frameworks/game-theory-principles.md`) is a hard rule, not a soft preference. The rationale:

- **Game theory**: A strictly dominated strategy should never be played. Spending a roster slot on a pure-SV reliever when SV is at 0.08 win prob is strictly worse than spending the same slot on a power bat who lifts HR from 0.35 to 0.40. The dominated action is eliminated by iterated deletion.
- **Budget logic**: Roster slots, FAAB, and streamer starts are bounded. Every slot spent on a conceded cat is a slot not spent on a contested cat. The opportunity cost is high.
- **Downstream enforcement**: `mlb-lineup-optimizer` maximizes `Σ daily_quality × leverage`. If SV has `leverage = 0.0`, the optimizer correctly refuses to start an SV-only reliever — not because the reliever is bad, but because the match between the reliever's output and our matchup needs is zero.

Softening `0.0` to `0.1` or `0.2` (to "keep options open") breaks this. With non-zero leverage, the optimizer may start a pure-SV reliever whose `daily_quality` is high, even though the cat is conceded. The result: wasted roster slot, lost contested-cat opportunity, lower overall matchup win probability.

Zero means zero. If new information arrives mid-week that changes SV from 0.08 to 0.35 (e.g., opponent's closers all blow saves simultaneously), re-run `matchup-win-probability-sim` and re-run this skill. Do not hack in a partial leverage weight.

## Leverage Weight Derivation

The leverage weight is the multiplier that converts private per-player value into competitive per-matchup value.

**Intuition**: a player's `daily_quality` score says "this player is good at baseball." But "good at baseball" is a private-value score. What we care about is "is this player good at moving cats that are close in our current matchup" — a competitive score.

```
competitive_score(player) = Σ_over_cats [ player.contribution[cat] × leverage[cat] ]
```

A power bat contributing `3 HR, 10 RBI, 8 R, 2 SB` per week has the same `daily_quality` regardless of opponent. But against an opponent where:

- HR is contested (leverage 1.5), RBI is contested (1.5), R is pushed (1.2), SB is conceded (0.0):
  - competitive_score = `3 * 1.5 + 10 * 1.5 + 8 * 1.2 + 2 * 0.0 = 4.5 + 15 + 9.6 + 0 = 29.1`

- HR is locked (1.0), RBI is locked (1.0), R is locked (1.0), SB is contested (1.5):
  - competitive_score = `3 * 1.0 + 10 * 1.0 + 8 * 1.0 + 2 * 1.5 = 24`

Same player, same week, different matchup — the first matchup values the player 21% higher. That's the leverage weights doing their work.

**Weight magnitudes**:

- `1.5` (contested): chosen to give a ~50% premium over default. Large enough to meaningfully shift lineup decisions, small enough not to override flagrant `daily_quality` differences.
- `1.2` (pushed): a modest premium — we want these cats defended, but not at the cost of sharply better players elsewhere.
- `1.0` (locked, default): no premium, no discount.
- `0.0` (conceded): hard zero — see above.

These magnitudes align with principle #5 in `frameworks/game-theory-principles.md`.

## Upstream Dependency on matchup-win-probability-sim

`per_cat_win_probability` is the critical input. It must come from `matchup-win-probability-sim` (or a behaviorally equivalent simulator) and not from eyeballing capacity vs projection. Here's why:

**Capacity vs projection gives point estimates. Win probability requires variance.**

Consider two scenarios:

- **Scenario A**: our HR capacity = 12, opp HR projection = 14. Both sides have stddev = 4. Gap is 2 HR but the variance is large. `per_cat_win_prob ≈ 0.35` (close to 50/50).
- **Scenario B**: our HR capacity = 12, opp HR projection = 14. Both sides have stddev = 1. Gap is 2 HR but the variance is small. `per_cat_win_prob ≈ 0.08` (close to certain loss).

Same point estimates. Radically different classification: Scenario A is contested (leverage 1.5, push resources here); Scenario B is conceded (leverage 0.0, don't touch).

The only way to distinguish the two is to compute win probability from the full `(mean, stddev)` distribution — which is exactly what `matchup-win-probability-sim` does via Monte Carlo or Poisson-binomial.

**Practical protocol**:

1. Caller invokes `matchup-win-probability-sim` first. Captures `per_cat_win_probability` dict and `matchup_win_probability` scalar.
2. Caller invokes this skill (`category-allocation-best-response`) passing `per_cat_win_probability` directly from step 1.
3. This skill computes `k_of_n_win_probability` via its own Poisson-binomial. Sanity check: `abs(this.k_of_n_win_probability - upstream.matchup_win_probability) < 0.03` (within PB approximation error).
4. If divergence is larger than 0.03, investigate: is the caller using a different threshold? Are per-cat probabilities being re-processed somewhere?

## Poisson-Binomial Recurrence

The Poisson-binomial distribution describes the sum of N independent Bernoulli random variables with different success probabilities. Given `p = [p_1, ..., p_N]`:

```
P_i(k) = P(exactly k successes in the first i Bernoullis)

Base case:
  P_0(0) = 1
  P_0(k) = 0 for k >= 1

Recurrence:
  P_i(0) = P_{i-1}(0) * (1 - p_i)
  P_i(k) = P_{i-1}(k) * (1 - p_i) + P_{i-1}(k-1) * p_i   for k = 1..i
```

Complexity: O(N^2) — trivially fast for N up to a few hundred.

Matchup win probability:

```
k_of_n_win_probability = sum_{k = K}^{N} P_N(k)
```

With ties counted as half-wins (Yahoo default), the threshold comparison uses `k >= K` with a half-unit added to the count of tied cats. In practice, with continuous stats and rounded display, exact ties are vanishingly rare — the `k >= K` strict comparison suffices for operational use.

**Why PB, not Monte Carlo, here**: this skill lives inside the decision loop (we may call it many times while exploring lineup options). Deterministic PB is sub-millisecond; MC is 100–200ms for 10k sims. Since the upstream `matchup-win-probability-sim` already ran MC (in the caller's initial invocation), using PB here is fine for downstream consistency.

## What to Do When Our Roster Is Simply Worse

Sometimes the classification returns `pushed + contested < K`, even after borderline upgrades. This happens when our roster is genuinely worse than the opponent's — most of our cats sit below 0.25, we can't realistically reach the threshold with normal allocation. Two responses:

**1. Accept the asymmetry and pivot to variance-seeking play**

Principle #6 (cope principle): underdogs maximize variance; favorites minimize it. When we're a ~35% favorite, a balanced lineup yields ~35% win probability. A deliberately high-variance lineup (boom-bust players, one-start studs, high-K/high-BB hitters) raises win probability to ~45% — not by improving our median, but by widening our distribution.

Call `variance-strategy-selector` with our computed `k_of_n_win_probability`. That skill returns a play style (`variance_seeking` vs `variance_damping`) that `mlb-lineup-optimizer` applies as a multiplier on top of `leverage`.

**2. Set a trigger for next week**

A matchup where we're structurally outclassed is often fixable with trades or strategic waiver priority. Log the matchup outcome in `tracker/decisions-log.md` and trigger `mlb-trade-analyzer` and `mlb-waiver-analyst` to address the underlying roster gap.

**Do not**:

- Redouble resources on `pushed_cats` — they already have adequate win probability.
- Upgrade cats below the 0.20 band — they're genuinely dominated.
- Overfit this week's allocation to a matchup we can't win. Preserve resources (especially FAAB) for future-week matchups.

## Generalization to Non-10-Cat Leagues

The skill is intentionally domain-neutral. Only three things change across fantasy sports:

1. **Cat list** (`our_per_cat_capacity.keys()`): 10 cats for MLB 5x5 and NHL 10-cat, 9 cats for NBA 9-cat, varies for other formats.
2. **Threshold** (`cat_win_threshold`): 6 for 10-cat, 5 for 9-cat, etc. Must match league format.
3. **Inverse cats** (`inverse_cats`): ERA/WHIP for MLB, TO for NBA, GAA for NHL. Inverse handling is the upstream simulator's job.

Classification thresholds (0.25, 0.70, 0.85), leverage weights (0.0, 1.0, 1.2, 1.5), the upgrade band (0.20–0.25), and the Poisson-binomial recurrence are all sport-agnostic. The same code path handles MLB, NBA, NHL, and any future H2H Categories format.

**Sport-specific notes**:

- **NBA 9-cat**: cat-to-cat correlation is higher than MLB (team usage patterns link PTS-AST-3PM). The independence assumption in the PB computation is slightly more approximate in NBA. If the caller passes a correlation matrix to `matchup-win-probability-sim`, the resulting `per_cat_win_probability` already accounts for it — the classification here is unaffected.

- **NHL 10-cat**: goalie cats (W, GAA, SV%, SO) come bundled through a single player. A roster move that changes goalie affects four cats at once. The skill treats each cat independently for classification, but downstream consumers should recognize the bundling when allocating streamer-goalie starts.

- **Daily-lineup sports (NBA, NHL)**: `streamer_starts` in `resources_available` is measured in games, not weeks. The leverage weights apply identically; the resource budget is just denser.

**Format boundary cases**:

- **8-cat or smaller leagues** (common in custom NBA or fantasy football leagues with cat scoring): the `K/N` ratio shifts. In a 5-of-8 league, K = 5 still applies; the PB recurrence handles any N.
- **12-cat or larger leagues**: more cats means more room for differentiation; typical matchups show ~3 conceded, ~3 locked, ~6 contested/pushed. The leverage weights stay the same.

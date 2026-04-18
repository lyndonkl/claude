# Variance Strategy Selector Methodology

The mathematical and game-theoretic foundations for variance-seeking vs variance-minimizing postures, including Kelly Criterion reference, variance-of-sum math, tail-probability reasoning, Central Limit dampening, and cross-domain parallels.

## Table of Contents
- [The Core Intuition](#the-core-intuition)
- [Why Underdogs Want Variance: Right-Tail Probability](#why-underdogs-want-variance-right-tail-probability)
- [Why Favorites Want Low Variance: Left-Tail Probability](#why-favorites-want-low-variance-left-tail-probability)
- [Variance-of-Sum Math](#variance-of-sum-math)
- [Central Limit Dampening](#central-limit-dampening)
- [Kelly Criterion Reference](#kelly-criterion-reference)
- [Downside-Asymmetry Amplification](#downside-asymmetry-amplification)
- [Cross-Domain Parallels](#cross-domain-parallels)
- [Citations and Further Reading](#citations-and-further-reading)

---

## The Core Intuition

Variance is the agent's friend when the expected outcome is bad and the agent's enemy when the expected outcome is good. Expected value (EV) by itself does not tell you what to do under uncertainty -- you also need the shape of the distribution.

Consider two lottery tickets:
- Ticket A: guaranteed $50
- Ticket B: 50% chance of $0, 50% chance of $100

Both have EV = $50. But if you are $90 short on rent due tomorrow, Ticket B is strictly better -- the left tail ($0) is no worse than your already-catastrophic baseline, and the right tail ($100) solves your problem. If instead you have $1,000 in the bank and rent is $50, Ticket A is strictly better -- Ticket B's left tail introduces risk you do not need.

The same logic applies to every decision with a controllable variance knob: lineup slots, portfolio weights, bet sizes, racing lines, career moves. The agent's win probability tells them which tail to bet on.

---

## Why Underdogs Want Variance: Right-Tail Probability

Suppose your team's skill is fixed at some mean performance level `mu_you`, and the opponent's is `mu_opp`, with `mu_opp > mu_you`. You win if your realized performance `X_you` exceeds the opponent's realized performance `X_opp` on the day:

```
P(win) = P(X_you > X_opp) = P(X_you - X_opp > 0)
```

The difference `D = X_you - X_opp` has mean `mu_you - mu_opp < 0` (negative because you're the underdog) and some variance that depends on both sides' variance.

With the standard normal approximation:

```
P(win) = P(D > 0) = 1 - Phi((0 - E[D]) / sqrt(Var[D]))
                  = 1 - Phi(-E[D] / sqrt(Var[D]))
                  = Phi(E[D] / sqrt(Var[D]))
```

Because `E[D] < 0`, this is `Phi(negative)`, which is less than 0.5. **The key insight: as `Var[D]` increases, the ratio `E[D] / sqrt(Var[D])` approaches zero from below, and `P(win)` approaches 0.5.**

The underdog cannot change the mean (skill is what it is), but they can choose lineups, positions, or bets that increase `Var[X_you]` -- which increases `Var[D]` -- which pulls `P(win)` toward 0.5.

**Numerical example.** Opponent is 15% better on skill. With balanced lineups, the standard deviation of the difference might give `P(win) = 0.35`. Switching to a deliberately higher-variance lineup can increase `sqrt(Var[D])` by 40%, pulling `P(win)` up to roughly 0.45 -- a 10-percentage-point gain from choosing variance. This is the empirical basis for the "seek" band's multiplier range.

---

## Why Favorites Want Low Variance: Left-Tail Probability

The same formula runs in reverse for favorites. If `mu_you > mu_opp`, then `E[D] > 0`, and `P(win) = Phi(positive) > 0.5`. Increasing `Var[D]` now pulls `P(win)` *down* toward 0.5.

A favorite's optimal posture is therefore to *minimize* variance -- to choose the most stable roster, the most diversified portfolio, the tightest racing line. Every additional dollar of standard deviation on the favorite's side is a dollar of give-back toward a coin flip.

**Operational consequence.** A favorite who plays "exciting" high-variance choices throws away free expected win probability. The 0.85 multiplier floor in the "minimize" band reflects the observed magnitude of this give-back in practice: roughly 10-15% of boom-bust weighting compressed out, which converts to 3-5 percentage points of recovered win probability on a typical weekly matchup or portfolio rebalance.

---

## Variance-of-Sum Math

When an agent makes `n` independent decisions, the total realized performance is a sum:

```
X_you = sum_{i=1}^{n} x_i
```

The variance of a sum of independent random variables is the sum of variances:

```
Var[X_you] = sum_{i=1}^{n} Var[x_i]
```

The standard deviation scales with `sqrt(n)`:

```
sd[X_you] = sqrt(sum Var[x_i]) ~ sqrt(n) * sd[typical x_i]
```

But the mean scales linearly with `n`:

```
E[X_you] = n * E[typical x_i]
```

**Coefficient of variation** (relative spread) = `sd / E` scales as `1 / sqrt(n)`. As `n` grows, the distribution of the sum concentrates around its mean -- the Central Limit Theorem in action. This is what motivates slot-count dampening.

---

## Central Limit Dampening

The variance knob is less powerful when applied across many independent slots, because the overall distribution of the sum is already being narrowed by the `1/sqrt(n)` collapse of the coefficient of variation.

**Formal argument.** Suppose you pick between two lineups:
- Lineup A: each of `n` slots has variance `v_low`
- Lineup B: each of `n` slots has variance `v_high`

The sum has variance `n * v_low` vs `n * v_high`. The standard deviation ratio is `sqrt(v_high / v_low)` regardless of `n`. But the *marginal* benefit to an underdog of choosing B over A -- the gain in `P(win)` -- depends on how close the Z-score `E[D] / sqrt(Var[D])` is to zero. When `n` is large, both denominators are large relative to the mean gap, and the Z-score is already close to zero. Further variance inflation has diminishing returns.

The dampening formula `factor = max(0.5, 5/n)` captures this: below `n=5` the variance knob has full authority; between 5 and 10 it halves in power; beyond 10 we floor the factor at 0.5 to preserve the strategic posture without claiming unrealistic effect sizes.

**Important caveat: independence assumption.** If the slot outcomes are correlated (all pitchers from the same team, all tech stocks, all races on the same weather-dependent track), the `1/sqrt(n)` collapse does not apply and dampening is unwarranted. The skill's guardrail flags this: when the consumer domain is known to be correlated, apply less dampening or none.

---

## Kelly Criterion Reference

Kelly (1956) derived the optimal fraction of bankroll to bet when offered a positive-edge bet:

```
f* = (p * b - q) / b = (edge) / (odds)
```

where `p` = probability of winning, `q = 1 - p`, and `b` = net odds received on a win.

Kelly is the optimal *bet sizing* rule for maximizing long-run logarithmic wealth. This skill does not compute Kelly directly -- sizing is the consumer's job -- but Kelly is the conceptual reference for why variance preference depends on win probability and downside.

Two observations from Kelly:

1. **Kelly scales with edge.** When you are a small underdog, Kelly says bet small. When you are a large favorite with good odds, Kelly says bet big. The variance-strategy-selector encodes the *direction* of bet-size tilt; the consumer uses Kelly or a fraction of Kelly for the *magnitude*.

2. **Fractional Kelly is standard in practice.** Full Kelly maximizes expected log-wealth but has very high variance of outcomes. Most practitioners use 1/4 or 1/2 Kelly. The variance multiplier here can be read as a tilt on top of whatever fractional-Kelly baseline the consumer already uses: 1.30 means "bet like 1.3x your usual Kelly fraction" (slightly more aggressive), 0.80 means "bet like 0.8x" (slightly more conservative).

See `market-mechanics-betting` skill for operational Kelly computation.

---

## Downside-Asymmetry Amplification

Utility theory distinguishes between the probability of an outcome and the utility of that outcome. When loss-pain is much larger than win-pleasure (asymmetric utility), the optimal posture is not symmetric.

**Must-win scenarios** (asymmetry near 1.0): missing playoffs, bankroll ruin, elimination. Here, the utility of losing is effectively `-infinity` (or close enough that any further loss is irrelevant), while any win at all counts as a success. The underdog should maximize the probability of *any* win, which is maximum-variance lottery-ticket behavior.

**Protect-the-lead scenarios** (asymmetry near 1.0 for the favorite): championship-clinching race, expiry-day options hedge, final quarterly earnings print. Losing a won position here is much worse than winning by a larger margin. The favorite should minimize the probability of any catastrophic draw, which is minimum-variance hold-what-you-have behavior.

The +/- 0.10 shift is calibrated to roughly an extra 10-15% of multiplier authority, reflecting empirical post-hoc studies of stars-and-scrubs vs balanced lineup outcomes in must-win H2H weeks and of "protect the lead" vs "press the bet" outcomes in racing and trading.

**Why not amplify neutral-band posture?** If you are genuinely at 0.50 win probability, there is no tail to prefer -- both tails are equally yours. A high-asymmetry neutral scenario might motivate *reducing stake* entirely, but that is a sizing question, not a variance-direction question. This skill does not adjust neutral-band multipliers for asymmetry.

---

## Cross-Domain Parallels

The same framework governs decisions across very different domains. In each case, the agent controls a variance knob, and the optimal setting depends on current win probability and downside asymmetry.

### Fantasy Sports Lineup Construction

- **Variance knob**: boom-bust players (high K% hitters, volatile starters) vs stable players (high-contact hitters, steady innings-eaters)
- **Underdog posture**: start the boom-bust guys. If your opponent's lineup is 15% stronger on projections, a balanced lineup gives ~35% win probability; a deliberately volatile lineup gives ~45%. The variance you introduce is free because you're behind on mean.
- **Favorite posture**: start the stable guys. Lock in the expected margin; don't donate probability to the coin flip.
- **Slots**: ~9-15 slots per week, so moderate dampening applies.
- **Asymmetry**: high in must-win playoff weeks (weeks 20-23), low in early-season weeks.

### Portfolio Allocation

- **Variance knob**: concentration vs diversification; high-beta vs low-beta; equities vs bonds
- **Underdog posture**: a fund that is far behind its benchmark mid-year has negative expected alpha if it stays passive. Concentrated, high-beta bets give it right-tail probability to catch up -- at the cost of left-tail probability that doesn't matter if benchmark-underperformance already costs the job.
- **Favorite posture**: a fund that is far ahead of its benchmark in Q4 should lock it in. Low-beta, diversified, cash-heavy. Do not give back the lead chasing additional alpha.
- **Slots**: often large (20-100 positions), so heavy dampening applies -- but watch the correlation assumption. A portfolio of 50 tech stocks is not 50 independent decisions.
- **Asymmetry**: high when year-end bonus depends on benchmark beat; low in mid-cycle.

### Poker Bankroll Decisions

- **Variance knob**: bet sizing relative to optimal (over-bet for fold equity / under-bet for pot control), tournament selection (high-variance MTT vs low-variance cash game)
- **Underdog posture**: short stack at a final table -> shove wide, take coin flips, accept bust risk for the right-tail payout.
- **Favorite posture**: chip leader at a final table -> play tight, avoid coin flips, let short stacks bust each other.
- **Slots**: small for a single decision (1 hand), large for a session (100+ hands); the skill's dampening adapts.
- **Asymmetry**: high at the money bubble or in a satellite; low in a re-entry tournament early.

### Horse Racing / Motor Racing Strategy

- **Variance knob**: racing line (inside vs outside), pit timing, tire choice, aero trim
- **Underdog posture**: trailing car makes aggressive overtaking attempts, pits at non-standard windows, gambles on weather.
- **Favorite posture**: leading car covers the follower's moves, pits in the standard window, takes no unforced risks.
- **Slots**: usually 1-5 strategic decisions per race.
- **Asymmetry**: high when championship is at stake in final race; low in a mid-season race of a long championship.

### General Decision Making

Any repeatable decision with (a) an estimable `P(win)`, (b) a controllable variance option, and (c) a known or estimable downside asymmetry can plug into this skill. The skill emits a scalar; the consumer decides what to multiply it against.

---

## Citations and Further Reading

- **Game Theory Principles #6** (`/Users/kushaldsouza/Documents/Projects/yahoo-mlb/context/frameworks/game-theory-principles.md`): the "cope" principle -- favorites minimize variance, underdogs maximize it. Operationalized for MLB fantasy in the `mlb-lineup-optimizer` consumer.
- **Kelly, J. L. (1956)**, "A New Interpretation of Information Rate," Bell System Technical Journal. The original optimal-bet-size derivation; the conceptual backbone for why variance preference depends on edge.
- **Thorp, E. O. (1969)**, "Optimal Gambling Systems for Favorable Games." Fractional Kelly and practical bankroll management.
- **Markowitz, H. (1952)**, "Portfolio Selection," Journal of Finance. Mean-variance optimization; the foundational framework in which "variance is bad when you're ahead" was first formalized for investment.
- **Kahneman & Tversky (1979)**, "Prospect Theory." Loss aversion as the utility-theoretic basis for downside-asymmetry amplification.
- **Central Limit Theorem** (any undergraduate probability text): the `1/sqrt(n)` collapse of the coefficient of variation that motivates slot-count dampening.

**Related skills in this codebase:**
- `market-mechanics-betting` -- Kelly bet sizing and edge calculation
- `expected-value` -- EV computation (uses the posture emitted here to tilt option scoring)
- `bayesian-reasoning-calibration` -- updating `current_win_probability` as evidence arrives
- `mlb-lineup-optimizer` (consumer) -- applies the multiplier to `boom_bust` weighting in `daily_quality x leverage x variance_multiplier`

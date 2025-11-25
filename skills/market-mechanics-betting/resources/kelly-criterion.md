# Kelly Criterion Deep Dive

Mathematical foundation for optimal bet sizing under uncertainty.

## Table of Contents

1. [Mathematical Derivation](#1-mathematical-derivation)
2. [Formula Variations](#2-formula-variations)
3. [Fractional Kelly](#3-fractional-kelly)
4. [Extensions](#4-extensions)
5. [Common Mistakes](#5-common-mistakes)
6. [Practical Implementation](#6-practical-implementation)
7. [Historical Examples](#7-historical-examples)
8. [Comparison to Other Methods](#8-comparison-to-other-methods)

---

## 1. Mathematical Derivation

### The Core Question

**Problem**: What fraction of your bankroll maximizes long-term growth?

**Why it matters**: Bet too little → Leave money on the table. Bet too much → Risk ruin, high variance.

### Logarithmic Utility Framework

**Key insight**: Maximize expected logarithm of wealth, not expected wealth.

**Why log utility?**
- Captures diminishing marginal utility ($1 matters more when you have $100 vs $1M)
- Makes repeated multiplicative bets additive: log(AB) = log(A) + log(B)
- Geometric mean emerges naturally (what matters for repeated bets)
- Prevents betting 100% (avoids ruin)

### Derivation for Binary Bet

**Setup**:
- Current bankroll: W
- Bet fraction: f
- Win probability: p, Loss probability: q = 1 - p
- Net odds: b (bet $1, win $b net)

**Outcomes**:
- Win (probability p): New wealth = W(1 + fb)
- Lose (probability q): New wealth = W(1 - f)

**Expected log utility**:
```
E[log(W_new)] = p × log(1 + fb) + q × log(1 - f) + log(W)
```

**Objective**: Maximize g(f) = p × log(1 + fb) + q × log(1 - f)

### Finding the Optimum

**Take derivative**:
```
dg/df = pb/(1 + fb) - q/(1 - f)
```

**Set equal to zero and solve**:
```
pb/(1 + fb) = q/(1 - f)
pb(1 - f) = q(1 + fb)
pb - pbf = q + qfb
pb - q = f(pb + qb) = fb(p + q) = fb

f* = (pb - q) / b = (bp - q) / b
```

**The Kelly Criterion**:
```
f* = (bp - q) / b

Where:
f* = Optimal fraction to bet
b  = Net odds received
p  = Win probability
q  = 1 - p
```

### Alternative Form

**Edge** = Expected return per dollar bet = bp - q

**Kelly formula**: f* = Edge / Odds = (bp - q) / b

**Example**: p = 60%, b = 1.0 (even money)
- Edge = 0.6 × 1 - 0.4 = 0.2
- f* = 0.2 / 1 = 20%

### Optimality

**Second derivative**: d²g/df² < 0 at f = f* → Maximum confirmed

**Growth rate**: G(f*) maximizes long-run geometric growth

**Comparison**:
- f < f*: Lower growth (too conservative)
- f > f*: Lower growth (too aggressive, variance dominates)
- f > 2f*: Negative growth (eventual ruin)

---

## 2. Formula Variations

### Converting Market Odds

**Decimal odds** (e.g., 2.50): b = Decimal - 1 = 1.50

**American odds**:
- Positive (+150): b = 150/100 = 1.50
- Negative (-150): b = 100/150 = 0.667

**Fractional odds** (3/1): b = 3.0

**Implied probability**: Market p = 1/(b + 1)

### Multi-Outcome Bet

**Horse race**: Multiple options, bet on any with positive Kelly

**Formula for outcome i**:
```
f_i* = (p_i(b_i + 1) - 1) / b_i

If f_i* > 0: Bet f_i* on outcome i
If f_i* ≤ 0: Don't bet
```

### Continuous Outcomes (Merton's Formula)

**Stock market application**:
```
f* = μ / σ²

Where:
μ = Expected return (drift)
σ² = Variance of returns
```

**Example**: μ = 8%, σ = 20% → f* = 0.08/0.04 = 2.0 (200%, use leverage)

**Reality**: Too aggressive, use fractional Kelly → 50-100% more reasonable

---

## 3. Fractional Kelly

### Why Fractional Kelly?

**Problems with full Kelly**:
1. **Extreme volatility**: Wild swings, can lose 50%+ in bad runs
2. **Model error**: If probability estimate wrong, full Kelly overbets dramatically
3. **Practical ruin**: 20% chance of 50% drawdown before doubling
4. **Non-ergodic**: Most can't bet infinitely many times

### Formula

```
Fractional Kelly = f* × Fraction

Common choices:
- Half Kelly: f*/2
- Quarter Kelly: f*/4 (recommended)
- Third Kelly: f*/3
```

### Growth vs. Variance Trade-off

| Strategy | Growth Rate | Volatility | Max Drawdown |
|----------|-------------|------------|--------------|
| Full Kelly | 100% | 100% | -50% |
| Half Kelly | ~75% | 50% | -25% |
| Quarter Kelly | ~50% | 25% | -12% |

**Key**: Half Kelly gives 75% of growth with 25% of variance → Better risk-adjusted return

### Robustness to Error

**Example**: You think p = 0.60, true p = 0.55, even money bet

**Full Kelly** (f = 20%):
- Growth rate = 0.55×log(1.20) + 0.45×log(0.80) ≈ 0 (breakeven!)

**Half Kelly** (f = 10%):
- Growth rate = 0.55×log(1.10) + 0.45×log(0.90) ≈ 0.005 (still positive)

**Lesson**: Overbetting much worse than underbetting. Fractional Kelly provides buffer.

### Recommended Fractions

| Situation | Fraction | Reasoning |
|-----------|----------|-----------|
| Professional gambler | 1/4 to 1/3 | Reduces career risk |
| High model uncertainty | 1/4 or less | Error buffer crucial |
| High confidence | 1/2 to 2/3 | Can use more aggression |
| Institutional | 1/4 to 1/3 | Drawdown = career risk |

**Default**: Quarter Kelly (1/4) for most real-world situations

---

## 4. Extensions

### Multiple Simultaneous Bets

**Matrix form** (N assets):
```
f* = Σ⁻¹ × μ

Where:
Σ = Covariance matrix
μ = Expected returns vector
```

**Key insight**: Correlated bets reduce optimal sizing

**Heuristic**: Adjusted Kelly = Individual Kelly × (1 - ρ/2), where ρ = correlation

**Example**: ρ = 0.6, Individual Kelly = 15%
- Adjusted: 15% × (1 - 0.3) = 10.5%

### Correlated Outcomes

**Common correlations**:
- Political: Presidential + Senate races
- Sports: Team championship + Player MVP
- Markets: Tech stock A + Tech stock B

**Extreme cases**:
- ρ = 1 (perfect correlation): Only bet on one
- ρ = -1 (negative correlation): Bets hedge, can bet more
- ρ = 0 (independent): No adjustment

### Dynamic Kelly

**Problem**: Probability changes over time (new information)

**Process**:
1. Start with p₀, bet f₀*
2. New information → Update to p₁ (Bayesian)
3. Recalculate f₁*
4. Rebalance (adjust bet size)

**Consideration**: Transaction costs limit rebalancing frequency

---

## 5. Common Mistakes

### Mistake 1: Full Kelly Overbet

**The error**: Using full Kelly in practice

**Why wrong**: Assumes perfect probability estimate (never true)

**Impact**: Bet 2×f* → Negative growth rate

**Fix**: Always use fractional Kelly (1/4 to 1/2)

### Mistake 2: Ignoring Model Error

**The error**: Treating probability as certain

**Adjustment**:
```
Uncertain Kelly = f* × Confidence

Example: f* = 20%, 80% confident → Bet 16%
```

**Better**: Use fractional Kelly (implicitly adjusts)

### Mistake 3: Neglecting Bankruptcy

**Reality**: Finite games + estimation error → real ruin risk

**Drawdown stats** (full Kelly, p=0.55):
- 25% chance of -40% before recovery
- 10% chance of -50% before recovery

**Practical bankruptcy**: Client fires you, forced liquidation, can't maintain discipline

**Fix**: Use fractional Kelly, set stop-loss (if down 25%, pause)

### Mistake 4: Ignoring Correlation

**Example disaster**:
- 10 bets, each Kelly 10%
- All highly correlated (same theme)
- Bet 100% total → Single adverse event → Large loss

**Fix**: Measure correlations, use portfolio Kelly, diversify themes

### Mistake 5: Misestimating Odds

**Common confusion**:
- Decimal 2.0: b = 1.0 (not 2.0)
- "3-to-1": b = 3.0 ✓
- American +200: b = 2.0 (not 200)

**Fix**: Always convert to NET payout (b = total return - 1)

### Mistake 6: Static Bankroll

**Problem**: Calculate once, never update

**Fix**: Recalculate before each bet using current bankroll

---

## 6. Practical Implementation

### Step-by-Step Process

**1. Convert odds to decimal**:
```python
# Decimal odds: b = decimal - 1
# American +150: b = 150/100 = 1.50
# American -150: b = 100/150 = 0.667
# Fractional 3/1: b = 3.0
```

**2. Determine probability**: Use forecasting process (base rates, Bayesian updating, etc.)

**3. Calculate edge**:
```python
edge = net_odds * probability - (1 - probability)
```

**4. Calculate Kelly**:
```python
kelly_fraction = edge / net_odds
```

**5. Apply fractional Kelly**:
```python
fraction = 0.25  # Quarter Kelly recommended
adjusted_kelly = kelly_fraction * fraction
```

**6. Calculate bet size**:
```python
bet_size = current_bankroll * adjusted_kelly
```

**7. Execute and track**:
- Record: Date, event, probability, odds, edge, Kelly%, bet
- Set reminder for resolution
- Note new information

### Position Tracking Template

```
Date: 2024-01-15
Event: Candidate A wins
Your probability: 65%
Market odds: 2.20 (implied 45%)
Net odds (b): 1.20
Edge: 0.43 (43%)
Full Kelly: 35.8%
Fractional (1/4): 8.9%
Bankroll: $10,000
Bet size: $890
Resolution: 2024-11-05
```

---

## 7. Historical Examples

### Ed Thorp - Blackjack (1960s)

**Application**: Card counting edge varies with count → Dynamic Kelly

**Implementation**:
- True count +1: Edge ~0.5%, bet ~0.5% of bankroll
- True count +5: Edge ~2.5%, bet ~2.5% of bankroll

**Results**: Turned $10k into $100k+, proved Kelly works in practice

**Lessons**: Used fractional Kelly (~1/2), dynamic sizing, managed "heat" (detection risk)

### Princeton-Newport Partners (1970s-1980s)

**Strategy**: Statistical arbitrage, convertible bonds

**Kelly application**: 1-3% per position, 50-100 positions (diversification)

**Results**: 19.1% annual (1969-1988), only 4 down months in 19 years, <5% max drawdown

**Lessons**: Fractional Kelly + diversification = low volatility, dominant strategy

### Renaissance Technologies / Medallion Fund

**Strategy**: Thousands of small edges, high frequency

**Kelly application**:
- Each signal: 0.1-0.5% (tiny fractional Kelly)
- Portfolio: 10,000+ positions
- Leverage: 2-4× (portfolio Kelly supports with diversification)

**Results**: 66% annual (gross) over 30+ years, never down year

**Lessons**: Kelly optimal for repeated bets with edge. Diversification enables leverage. Discipline crucial.

### Warren Buffett (Implicit Kelly)

**Concentrated bets**: American Express (40%), Coca-Cola (25%), Apple (40%)

**Why Kelly-like**: High conviction → High p → Large Kelly → Large position

**Quote**: "Diversification is protection against ignorance."

**Lessons**: Kelly justifies concentration with edge. Still uses fractional (~40% max, not 100%).

---

## 8. Comparison to Other Methods

### Fixed Fraction

**Method**: Always bet same percentage

**Pros**: Simple, prevents ruin

**Cons**: Ignores edge, suboptimal growth

**When to use**: Don't trust probability estimates, want simplicity

### Martingale (Double After Loss)

**Method**: Double bet after each loss

**Fatal flaws**:
- Requires infinite bankroll
- Exponential growth (10 losses → need $10,240)
- Negative edge → lose faster
- Betting limits prevent recovery

**Conclusion**: **NEVER use**. Mathematically certain to fail.

### Fixed Amount

**Method**: Always bet same dollar amount

**Cons**: As bankroll changes, fraction changes inappropriately

**When to use**: Very small recreational betting

### Constant Proportion

**Method**: Fixed percentage, not optimized for edge

**Difference from Kelly**: Doesn't adjust for edge/odds

**Conclusion**: Better than fixed dollar, worse than Kelly

### Risk Parity

**Method**: Allocate to equalize risk contribution

**Difference from Kelly**: Doesn't use expected returns (ignores edge)

**When better**: Don't have reliable return estimates, defensive portfolio

**When Kelly better**: Have edge estimates, goal is growth

### Summary Comparison

| Method | Growth | Ruin Risk | When to Use |
|--------|--------|-----------|-------------|
| **Kelly** | Highest | None* | Active betting with edge |
| **Fractional Kelly** | High | Very low | **Real-world (recommended)** |
| **Fixed Fraction** | Medium | Low | Simple discipline |
| **Fixed Amount** | Low | Medium | Recreational only |
| **Martingale** | Negative | Certain | **NEVER** |
| **Risk Parity** | Low-Med | Low | Defensive portfolios |

*Kelly theoretically no ruin risk, but model error creates practical risk → use fractional Kelly

**Final Recommendation**: **Quarter Kelly (f*/4)** for nearly all real-world scenarios.

---

## Return to Main Skill

[← Back to Market Mechanics & Betting](../skill.md)

**Related resources**:
- [Betting Theory Fundamentals](betting-theory.md)
- [Scoring Rules and Calibration](scoring-rules.md)

# Betting Theory Fundamentals

This resource explains the core theoretical foundations of rational betting, expected value, variance management, and market efficiency.

**Foundation for:** All betting and forecasting decisions

---

## Why Learn Betting Theory

**Core insight:** Betting theory separates decision quality from outcome quality. Make +EV decisions repeatedly and survive variance.

**Enables:**
- Think probabilistically (convert beliefs to quantifiable edges)
- Manage risk rationally (distinguish bad decisions from bad outcomes)
- Avoid costly mistakes (identify predictable failure modes)
- Optimize long-term growth (balance aggression with preservation)

**Research foundation:** Kelly (1956), Samuelson (1963), Thorp (1969), behavioral economics (Kahneman & Tversky), market efficiency (Fama).

---

## 1. Expected Value Framework

### Definition and Formula

**Expected Value (EV):** Probability-weighted average of all possible outcomes.

```
EV = Σ(Probability × Outcome)

Binary bet:
EV = (P_win × Amount_won) - (P_lose × Amount_lost)
```

**Example:**
```
Bet $100 on 60% event at even odds (+100)
EV = (0.60 × $100) - (0.40 × $100) = $20
EV% = +20% per $100 wagered
```

### Positive vs Negative EV

**Decision Framework:**
- **EV > +5%:** Strong bet (after fees/uncertainty)
- **EV = 0% to +5%:** Marginal (consider passing)
- **EV < 0%:** Never bet (unless hedging)

**Critical Rule:** Judge decisions by EV, not outcomes. Good decisions lose sometimes; bad decisions win sometimes. Process matters in small samples, results matter over 100+ trials.

### Converting Market Odds to EV

**Step 1: Implied probability**
```
Decimal odds: P = 1 / Odds
  Example: 1.67 → 60%

American (+): P = 100 / (Odds + 100)
  Example: +150 → 40%

American (-): P = |Odds| / (|Odds| + 100)
  Example: -150 → 60%
```

**Step 2: Calculate edge**
```
Your probability: 70%
Market probability: 60%
Edge = 70% - 60% = +10%
```

**Step 3: Calculate EV**
```
Bet $100 at 1.67 odds:
EV = (0.70 × $67) - (0.30 × $100) = +$16.90 = +16.9%
```

### Law of Large Numbers

**Key principle:** Observed frequency converges to true probability as sample size increases.

**Practical thresholds:**
- 10 bets: High variance, might be down despite +EV
- 100 bets: Convergence starting, likely near EV
- 1000 bets: Results tightly centered around EV

**Application:** Don't judge strategy on <30 trials. Variance dominates small samples.

---

## 2. Variance and Risk

### Standard Deviation

**Measures outcome dispersion around EV.**

**Formula:**
```
σ = √(P_win×(Win-EV)² + P_lose×(Loss-EV)²)
```

**Example ($100 bet, 60% win, even odds):**
```
EV = $20
σ = √(0.60×(100-20)² + 0.40×(-100-20)²)
σ = √9600 = $98

Coefficient of Variation: σ/EV = $98/$20 = 4.9
```

**Interpretation:** Standard deviation ($98) is 5× the EV ($20). Variance dominates signal.

### Volatility Categories

**Coefficient of Variation (CV = σ/EV):**
- CV < 1: Low volatility (10-30 trials to see EV)
- CV = 1-3: Moderate (30-50 trials)
- CV = 3-10: High (50-100 trials)
- CV > 10: Extreme (100+ trials)

**Higher CV requires:** Larger bankroll, more patience, stronger discipline.

### Risk of Ruin

**Probability of losing entire bankroll before profit.**

**Practical Guidelines:**

| Bet Size | Risk of Ruin | Assessment |
|----------|--------------|------------|
| 50% of bankroll | ~40% | Reckless |
| 25% of bankroll | ~20% | Aggressive |
| 10% of bankroll | ~5% | Moderate |
| 5% of bankroll | ~1% | Conservative |
| 2% of bankroll | ~0.1% | Very conservative |

**Kelly Criterion naturally manages risk of ruin. Never bet >10% of bankroll on single bet.**

### Managing Volatility

**1. Fractional Kelly (Primary Tool):**
- Full Kelly: 100% variance, 40%+ drawdowns
- Half Kelly: 25% variance, ~20% drawdowns
- Quarter Kelly: 6% variance, ~10% drawdowns

**2. Diversification:**
- Multiple uncorrelated +EV bets
- Requires independence (correlation < 0.3)

**3. Expected Drawdown:**
- Even optimal betting experiences 20-40% drawdowns
- Mentally prepare for temporary losses
- Don't confuse drawdown with -EV strategy

---

## 3. Bankroll Management

### Defining Your Bankroll

**Valid:** Money you can afford to lose entirely, separate from emergency fund, investment portfolio, daily expenses. **Starting:** $500-$5000 recreational, $10,000+ serious.

**NOT valid:** Money needed for bills, emergency fund, retirement, money you'd be devastated to lose.

### Separation Principle

**Why:** Prevents scared money and revenge betting. Clear accounting, tax clarity, risk containment.

**Implementation:** Separate betting account, never add money mid-downswing, withdraw profits periodically, stop if bankroll → $0.

### Growth vs Preservation

**Preservation (Default):** 1/4 to 1/2 Kelly, for most bettors and bankrolls <$5000
**Growth (Advanced):** 1/2 to full Kelly, for large bankrolls and high variance tolerance (requires 2+ years track record)

### Dynamic Sizing

Bet size scales with bankroll. Example: $1000 bankroll at 5% = $50. After wins → $1500 → bet $75. After losses → $600 → bet $30.

**Recalculate:** Daily if >20% change, weekly (active), monthly (casual).

### Withdrawal Strategy

**Recommended:** When bankroll doubles, withdraw original amount, continue with profit (break-even if lose profit).
**Conservative:** 50% profit monthly. **Aggressive:** Never withdraw (full compounding).

---

## 4. Market Efficiency

### Efficient Market Hypothesis

**Core claim:** Prices reflect all available information. **Reality:** Semi-strong efficient in liquid, mature markets.

**Market knows:** Published polls/news, historical base rates, expert commentary, obvious statistical patterns.

### Where Edges Exist

**1. Information Asymmetry:** Local knowledge, domain expertise
**2. Model Superiority:** Better statistical model, proper extremizing
**3. Lower Transaction Costs:** Market 5% fee vs your 0-1%
**4. Behavioral Biases:** Recency bias, base rate neglect, narrative following
**5. Market Immaturity:** Low liquidity, niche topics, few informed traders

**Before betting, ask:** "What information or model do I have that the market doesn't?"
- Nothing → Pass | Vague → Pass | Specific → Investigate

### Trust vs Question Market

**Trust:** Liquid, mature, objective outcome, many informed participants, low emotion
**Question:** Illiquid, new, subjective outcome, few informed participants, high emotion (politics, fandom)

---

## 5. Common Betting Mistakes

### Chasing Losses
**What:** Increasing bet size after losses. **Why:** Loss aversion, emotional arousal.
**Fix:** Never increase bet size after loss, use bankroll %, take break after 2+ losses.

### Tilt (Emotional Betting)
**Triggers:** Bad beat, streaks, external stress. **Symptoms:** No analysis, ignoring Kelly, revenge betting.
**Fix:** Pre-commit no bets when tilted. Checklist: Calm? Calculate EV? Kelly sizing? Betting for +EV not revenge?

### Overconfidence Bias
**What:** Overestimating probability accuracy (90% when true is 70%).
**Fix:** Track calibration, log predictions + outcomes, calculate curve quarterly. Do 70% predictions happen 70%?

### Ignoring Variance
**What:** Judging strategy on <30 trials. Example: "Down 15% after 20 bets, strategy sucks" (normal variance).
**Fix:** Require 50+ bets minimum, 100+ preferred, 200+ for high confidence.

### Outcome Bias
**What:** Judging by results not process. +15% EV lost = good decision (bad outcome). -10% EV won = bad decision (lucky).
**Fix:** Checklist: EV correct? Edge > threshold? Kelly fraction? Followed system? YES = good decision regardless of outcome.

### Hindsight Bias
**What:** After outcome, "I knew it would happen."
**Fix:** Pre-commit logging, write probability before event, don't revise after, accept 40% events happen 40%.

---

## 6. Integration with Kelly Criterion

### EV Drives Kelly

**Kelly derives from:** Expected value (edge), odds received, bankroll optimization (maximize log wealth).

**Key relationship:** `f* = (bp - q) / b`. Edge drives bet size: 10% edge → ~10% Kelly, 5% edge → ~5% Kelly, 0% edge → 0% bet.

### Variance Tolerance

| Fraction | Variance | Growth | Drawdown |
|----------|----------|--------|----------|
| Full (1.0) | 100% | 100% | ~40% |
| Half (0.5) | 25% | 75% | ~20% |
| Quarter (0.25) | 6% | 50% | ~10% |

### Bankruptcy Protection

Kelly never bets 100%: prevents ruin, keeps capital for next bet, scales down as bankroll shrinks. **Practical:** Stop if bankroll drops 80-90%.

---

## 7. Practical Examples for Forecasters

### Example 1: Election Prediction Market

**Scenario:** Market 55%, your forecast 65%, bankroll $2000

**Step 1: Edge**
```
Edge = 65% - 55% = +10%
Threshold: 5%
Decision: +10% > 5% → Proceed
```

**Step 2: EV**
```
Bet $100 at 1.82 odds → Win $82
EV = (0.65 × $82) - (0.35 × $100) = +$18.30 = +18.3%
```

**Step 3: Kelly**
```
Full Kelly: 22.3%
Half Kelly: 11.2%
Bet: $2000 × 11.2% = $224
```

### Example 2: Brier Score Tracking

**50 forecasts, goal: Brier < 0.15**

| Forecast | Your P | Outcome | (P-O)² |
|----------|--------|---------|--------|
| Event A | 80% | YES (1) | 0.04 |
| Event B | 30% | NO (0) | 0.09 |
| Event C | 90% | YES (1) | 0.01 |
| Event D | 60% | NO (0) | 0.36 |
| Event E | 70% | YES (1) | 0.09 |

**Brier:** 0.59 / 5 = 0.118 (Excellent)

**Analysis:** Event D large error normal (40% events happen). Don't game metric by avoiding 60% predictions.

### Example 3: Extremizing

**Forecasts:** You 72%, A 68%, B 75%, C 70%, Market 71%
**Average:** 71.2%

**Extremize:**
```
Factor: 1.3 (moderate)
Extremized = 50% + (71.2% - 50%) × 1.3 = 77.6% ≈ 78%

Edge: 78% - 71% = +7%
Half Kelly ≈ 3.5% of $5000 = $175 bet
```

### Example 4: Correlated Portfolio

**Scenario:** Democrats House (60% yours, 55% market) + Senate (55% yours, 50% market)
**Correlation:** 0.7 (high)

**Naive (WRONG):**
```
Bet A: 5% × $10k = $500
Bet B: 5% × $10k = $500
Total: $1000 (10%)
```

**Correct:**
```
Adjust for correlation: 1 - (0.7 × 0.5) = 0.65
Bet A: $500 × 0.65 = $325
Bet B: $500 × 0.65 = $325
Total: $650 (6.5%)
```

**Reasoning:** Positive correlation amplifies risk. Reduce sizing to maintain tolerance.

---

## Key Takeaways

### The 10 Commandments

1. **Expected Value is King** - Judge decisions by EV, not outcomes
2. **Variance is Inevitable** - Embrace it; don't fight it
3. **Bankroll is Sacred** - Protect it above all else
4. **Kelly is Your Guide** - But use fractional (1/4 to 1/2)
5. **Market is Usually Right** - You need edge to beat it
6. **Discipline Over Impulse** - System beats emotion
7. **Sample Size Matters** - 50+ bets before judgment
8. **Calibration is Honesty** - Track it religiously
9. **Correlations Kill** - Adjust for portfolio risk
10. **Survival Enables Profit** - Can't win if bankrupt

### Mental Models

**Betting = Business**
- Bankroll = Working capital
- EV = Profit margin
- Variance = Market volatility
- Kelly = Capital allocation

**Decision Quality ≠ Outcome Quality**
- Good decisions lose sometimes (variance)
- Bad decisions win sometimes (luck)
- Process > Results (small samples)
- Results > Process (large samples 100+)

### Integration Workflow

**Before betting:**
1. Make forecast (Bayesian, reference class)
2. Calculate edge vs market
3. Check edge > threshold (5%+)
4. Use Kelly for sizing
5. Execute and log

**After betting:**
1. Track outcome
2. Update calibration
3. Calculate Brier score
4. Don't judge single bet
5. Evaluate after 50+ bets

---

**Return to:** [Main Skill](../SKILL.md#interactive-menu)

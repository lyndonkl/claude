# Expected Value Methodology

Advanced techniques for probability estimation, payoff quantification, utility theory, decision trees, and bias mitigation.

## Workflow

```
Expected Value Analysis Progress:
- [ ] Step 1: Define decision and alternatives
- [ ] Step 2: Identify possible outcomes
- [ ] Step 3: Estimate probabilities
- [ ] Step 4: Estimate payoffs (values)
- [ ] Step 5: Calculate expected values
- [ ] Step 6: Interpret and adjust for risk preferences
```

**Step 1-2**: Define decision, identify outcomes → See [resources/template.md](template.md)

**Step 3**: Estimate probabilities → See [1. Probability Estimation Techniques](#1-probability-estimation-techniques)

**Step 4**: Estimate payoffs → See [2. Payoff Quantification](#2-payoff-quantification)

**Step 5**: Calculate EV → See [3. Decision Tree Analysis](#3-decision-tree-analysis) for sequential decisions

**Step 6**: Adjust for risk → See [4. Risk Preferences and Utility](#4-risk-preferences-and-utility)

---

## 1. Probability Estimation Techniques

### Base Rates (Outside View)

**Principle**: Use historical frequency from similar situations (reference class forecasting).

**Process**:
1. **Identify reference class**: What category of events does this belong to? (e.g., "tech startup launches", "enterprise software migrations", "clinical trials for this disease")
2. **Gather data**: How many cases in the reference class? How many succeeded vs. failed?
3. **Calculate base rate**: p(success) = # successes / # total cases
4. **Adjust for differences**: Is your case typical or atypical for the reference class? (Use inside view to adjust, but anchor on base rate.)

**Example**: Startup success rate. Reference class = "SaaS B2B startups, 2015-2020". Data: 10,000 launches, 1,500 reached $1M ARR. Base rate = 15%. Your startup: Similar profile → start with 15%, then adjust for unique factors.

**Cautions**: Reference class selection matters. Too broad (all startups) misses nuance. Too narrow (exactly like us) has no data.

### Inside View (Causal Decomposition)

**Principle**: Break outcome into necessary conditions, estimate probability of each, combine.

**Process**:
1. **Causal chain**: What needs to happen for this outcome? (A and B and C...)
2. **Estimate each link**: What's p(A)? p(B|A)? p(C|A,B)?
3. **Combine**: If independent: p(Outcome) = p(A) × p(B) × p(C). If conditional: p(Outcome) = p(A) × p(B|A) × p(C|A,B).

**Example**: Product launch success requires: (1) feature ships on time (80%), (2) marketing campaign reaches target audience (70%), (3) product-market fit (50%). If independent: p(success) = 0.8 × 0.7 × 0.5 = 28%. If dependent (late ship → poor marketing → worse fit): adjust.

**Cautions**: Overconfidence in ability to model all links. Conjunction fallacy (underestimate how probabilities multiply, 80% × 80% × 80% = 51%).

### Expert Judgment Aggregation

**Methods**:
- **Simple average**: Mean of expert estimates. Works well if experts are independent and equally calibrated.
- **Weighted average**: Weight experts by track record (past calibration score). More weight to well-calibrated forecasters.
- **Median**: Robust to outliers. Use if some experts give extreme estimates.
- **Delphi method**: Multiple rounds. Experts see others' estimates (anonymized), revise their own, converge.

**Calibration scoring**: Expert says "70% confident" → are they right 70% of the time? Track record via Brier score = Σ (p_i - outcome_i)² / N. Lower = better.

**Cautions**: Group-think if experts see each other's estimates before forming own. Anchoring on first estimate heard.

### Data-Driven Models

**Regression**: Predict outcome probability from features. Logistic regression for binary (success/fail). Linear for continuous (revenue).

**Time series**: If outcome is repeating event (monthly sales, weekly sign-ups), use time series (ARIMA, exponential smoothing) to forecast.

**Machine learning**: If rich data, use ML (random forest, gradient boosting, neural nets). Provides predicted probability + confidence intervals.

**Backtesting**: Test model on historical data. What would model have predicted vs. actual outcomes? Calibration plot: predicted 70% → actually 70%?

**Cautions**: Overfitting (model fits noise, not signal). Out-of-distribution (future may differ from past). Need enough data (small N → high variance).

### Combining Methods (Triangulation)

**Best practice**: Don't rely on single method. Estimate probability using 2-4 methods, compare.

- If estimates converge (all ~60%) → confidence high.
- If estimates diverge (base rate = 20%, inside view = 60%) → investigate why. Which assumptions differ? Truth likely in between.

**Weighted combination**: Base rate (50% weight), Inside view (30%), Expert judgment (20%) → final estimate.

**Update with new info**: Start with base rate (prior), update with inside view / expert / data (evidence) using Bayes theorem: p(A|B) = p(B|A) × p(A) / p(B).

---

## 2. Payoff Quantification

### Monetary Valuation

**Direct cash flows**: Revenue, costs, savings. Straightforward to quantify.

**Opportunity cost**: What are you giving up? (Time, resources, alternative investments). Cost = value of best alternative foregone.

**Option value**: Does this create future options? (Pilot project → if successful, can scale. Value of option > value of pilot alone.) Use real options analysis or decision tree.

**Time value of money**: $1 today ≠ $1 next year. Discount future cash flows to present value.

**NPV formula**: NPV = Σ (CF_t / (1+r)^t) where CF_t = cash flow in period t, r = discount rate (WACC, hurdle rate, or risk-free + risk premium).

**Discount rate selection**:
- Risk-free rate (US Treasury): ~3-5%
- Corporate projects: WACC (weighted average cost of capital), typically 7-12%
- Venture / high-risk: 20-40%
- Personal decisions: Opportunity cost of capital (what else could you invest in?)

**Inflation**: Use real cash flows (inflation-adjusted) or nominal cash flows with nominal discount rate. Don't mix.

### Non-Monetary Valuation

**Time**: Convert to dollars. Your hourly rate (salary / hours or freelance rate). Time saved = hours × rate. Or use opportunity cost (what else could you do with time?).

**Reputation / brand**: Harder to quantify. Approaches:
- Proxy: How much would you pay to prevent reputation damage? (e.g., PR crisis costs $X to fix → value of avoiding = $X)
- Customer lifetime value: Better reputation → higher retention → $Y in CLV
- Premium pricing: Strong brand → can charge Z% more → $W in extra revenue

**Learning / optionality**: Value of information or skills gained. Enables future opportunities. Hard to quantify exactly, but can bound:
- Conservative: $0 (ignore)
- Optimistic: Value of best future opportunity enabled × probability you pursue it
- Expected: Sum of option values across multiple future paths

**Strategic**: Competitive advantage, market position. Quantify via:
- Market share ×Average profit per point of share
- Defensive: How much would competitor pay to block this move?
- Offensive: How much extra profit from improved position?

**Utility**: Some outcomes have intrinsic value not captured by money (autonomy, impact, meaning). Use utility functions or qualitative scoring (1-10 scale).

### Handling Uncertainty in Payoffs

**Point estimate**: Single number (expected case). Simple but hides uncertainty.

**Range**: Optimistic / base / pessimistic (three-point estimate). Captures uncertainty. Can convert to distribution (triangular or PERT).

**Distribution**: Full probability distribution over payoffs (normal, lognormal, beta). Most accurate but requires assumptions. Use Monte Carlo simulation.

**Sensitivity analysis**: How much does EV change if payoff varies ±20%? Identifies which payoffs matter most.

---

## 3. Decision Tree Analysis

### Building Decision Trees

**Nodes**:
- **Decision node** (square): You make a choice. Branches = alternatives.
- **Chance node** (circle): Uncertain event. Branches = possible outcomes with probabilities.
- **Terminal node** (triangle): End of path. Payoff specified.

**Structure**:
- Start at left (initial decision), move right through chance and decision nodes, end at right (payoffs).
- Label all branches (decision choices, outcome names, probabilities).
- Assign payoffs to terminal nodes.

**Conventions**:
- Probabilities on branches from chance nodes must sum to 1.0.
- Decision branches have no probabilities (you control which to take).

### Fold-Back Induction (Solving Trees)

**Algorithm**: Work backwards from terminal nodes to find optimal strategy.

1. **At terminal nodes**: Payoff given.
2. **At chance nodes**: EV = Σ (p_i × payoff_i). Replace node with EV.
3. **At decision nodes**: Choose branch with highest EV. Replace node with max EV, note optimal choice.
4. **Repeat** until you reach initial decision node.

**Result**: Optimal strategy (which choices to make at each decision node) and overall EV of following that strategy.

**Example**:
```
Decision 1: [Invest $100k or Don't]
  If Invest → Chance: [Success 60% → $300k, Fail 40% → $0]
    EV(Invest) = 0.6 × $300k + 0.4 × $0 = $180k. Net = $180k - $100k = $80k.
  If Don't → $0
  Optimal: Invest (EV = $80k > $0)
```

### Value of Information

**Perfect information**: If you could learn outcome of uncertain event before deciding, how much would that be worth?

**EVPI** (Expected Value of Perfect Information):
- **With perfect info**: Choose optimal decision for each outcome. EV = Σ (p_i × best_payoff_i).
- **Without info**: EV of optimal strategy under uncertainty.
- **EVPI** = EV(with info) - EV(without info).

**Interpretation**: Maximum you'd pay to eliminate uncertainty. If actual cost of info < EVPI, worth buying (run experiment, hire consultant, do research).

**Partial information**: If info is imperfect (e.g., test with 80% accuracy), use Bayes theorem to update probabilities, calculate EV with updated beliefs, subtract cost of test.

### Sequential vs. Simultaneous Decisions

**Sequential**: Make choice, observe outcome, make next choice. Fold-back induction finds optimal strategy. Captures optionality (can stop, pivot, wait).

**Simultaneous**: Make all choices upfront, then outcomes resolve. Less flexible but sometimes unavoidable (commit to strategy before seeing results).

**Design for learning**: Structure decisions sequentially when possible (pilot before full launch, Phase I/II/III trials, MVP before scale). Preserves options, reduces downside.

---

## 4. Risk Preferences and Utility

### Risk Neutrality vs. Risk Aversion

**Risk-neutral**: Only care about EV, not variance. EV($100k, 50/50) = EV($50k, certain) → indifferent.

**Risk-averse**: Prefer certainty, willing to sacrifice EV to reduce variance. Prefer $50k certain over $100k gamble even though EV equal.

**Risk-seeking**: Enjoy uncertainty, prefer high-variance gambles. Rare for most people/organizations.

**When does risk matter?**
- **One-shot, high-stakes**: Can't afford to lose (bet life savings, critical product launch). Risk aversion matters.
- **Repeated, portfolio**: Many independent bets, law of large numbers. EV dominates (VCs, insurance companies, diversified portfolios).

### Utility Functions

**Utility** U(x): Subjective value of outcome x. For risk-averse agents, U is concave (diminishing marginal utility).

**Common functions**:
- **Linear**: U(x) = x. Risk-neutral (EU = EV).
- **Square root**: U(x) = √x. Moderate risk aversion.
- **Logarithmic**: U(x) = log(x). Strong risk aversion (common in economics).
- **Exponential**: U(x) = -e^(-ax). Constant absolute risk aversion (CARA), parameter a = risk aversion coefficient.

**Expected Utility**: EU = Σ (p_i × U(v_i)). Choose option with highest EU.

**Certainty Equivalent** (CE): The guaranteed amount you'd accept instead of the gamble. Solve: U(CE) = EU. For risk-averse agents, CE < EV.

**Risk Premium**: RP = EV - CE. How much you'd pay to eliminate risk.

**Example**: Gamble: 50% $100k, 50% $0. EV = $50k.
- If U(x) = √x, then EU = 0.5 × √100k + 0.5 × √0 = 0.5 × 316.2 = 158.1.
- CE: √CE = 158.1 → CE = 158.1² = $25k.
- RP = $50k - $25k = $25k. Would pay up to $25k to avoid gamble, take guaranteed $50k instead.

### Calibrating Your Utility Function

**Questions to reveal risk aversion**:
1. "Gamble: 50% $100k, 50% $0 vs. Certain $40k. Which?" → If prefer certain $40k, you're risk-averse (CE < $50k).
2. "Gamble: 50% $200k, 50% $0 vs. Certain $X. At what X are you indifferent?" → X = CE for this gamble.
3. Repeat for several gambles, fit utility curve to your choices.

**Organization risk tolerance**: Depends on reserves, ability to absorb loss, stakeholder expectations (public company vs. startup founder). Quantify via "How much can we afford to lose?" and "What's minimum acceptable return?"

### Non-Linear Utility (Prospect Theory)

**Observations** (Kahneman & Tversky):
- **Loss aversion**: Losses hurt more than equivalent gains feel good. U(loss) < -U(gain) in absolute terms. Ratio ~2:1 (losing $100 feels 2× worse than gaining $100).
- **Reference dependence**: Utility depends on change from reference point (status quo), not absolute wealth.
- **Probability weighting**: Overweight small probabilities (1% feels > 1%), underweight large probabilities (99% feels < 99%).

**Implications**: People are risk-averse for gains, risk-seeking for losses (gamble to avoid sure loss). Framing matters (80% success vs. 20% failure).

**Practical**: If stakeholders are loss-averse, emphasize downside protection (hedges, insurance, diversification) even if it reduces EV.

---

## 5. Common Biases and Pitfalls

### Overconfidence

**Problem**: Estimated probabilities too extreme (80% when should be 60%). Underestimate uncertainty.

**Detection**: Track calibration. Are your "70% confident" predictions right 70% of the time? Most people are overconfident (right 60% when say 70%).

**Fix**: Widen probability ranges. Use reference classes (base rates). Ask "How often am I this confident and wrong?"

### Anchoring

**Problem**: First number you hear (or think of) biases estimate. Adjust insufficiently from anchor.

**Example**: "Is revenue > $500k?" → even if you say no, your estimate will be anchored near $500k.

**Fix**: Generate estimate independently before seeing anchors. Use multiple methods to triangulate (outside view, inside view, experts).

### Availability Bias

**Problem**: Overweight recent or vivid events. "Startup X just failed, so all startups fail" (ignoring base rate of thousands of startups).

**Fix**: Use data / base rates, not anecdotes. Ask "How representative is this example?"

### Sunk Cost Fallacy

**Problem**: Include past costs in forward-looking EV. "We've already spent $1M, can't stop now!"

**Fix**: Sunk costs are sunk. Only future costs/benefits matter. EV = future payoff - future cost. Ignore past.

### Neglecting Tail Risk

**Problem**: Round low-probability, high-impact events to zero. "0.1% chance of -$10M? I'll call it 0%."

**Fix**: Don't ignore tail risk. 0.1% × -$10M = -$10k in EV (material). Sensitivity: What if probability is 1%?

### False Precision

**Problem**: "Probability = 67.3%, payoff = $187,432.17" when you're guessing.

**Fix**: Express uncertainty. Use ranges (55-75%, $150k-$200k). Don't pretend more precision than you have.

### Static Analysis (Ignoring Optionality)

**Problem**: Assume you make all decisions upfront, can't update or pivot. Misses value of learning.

**Fix**: Use decision trees for sequential decisions. Model optionality (stop early, wait for info, pivot). Often shifts optimal strategy.

---

## 6. Advanced Topics

### Correlation and Diversification

**Independent outcomes**: If portfolio of uncorrelated bets, variance decreases with N (Var_portfolio = Var_single / N). Diversification works.

**Correlated outcomes**: If outcomes move together (economic downturn hurts all investments), correlation reduces diversification benefit. Model dependencies (correlation coefficient, copulas).

**Portfolio EV**: Sum of individual EVs (always true). Portfolio variance: More complex, depends on correlations.

### Monte Carlo Simulation

**When to use**: Continuous distributions, many uncertain variables, complex interactions.

**Process**:
1. Define distributions for each uncertain variable (normal, lognormal, beta, etc.).
2. Sample randomly from each distribution (draw one value per variable).
3. Calculate outcome (payoff) for that sample.
4. Repeat 10,000+ times.
5. Analyze results: Mean = EV, percentiles = confidence intervals (5th-95th), plot histogram.

**Pros**: Captures full uncertainty, no need for discrete scenarios, provides distribution of outcomes.

**Cons**: Requires distributional assumptions (which may be wrong), computationally intensive, harder to communicate.

**Tools**: Excel (@RISK, Crystal Ball), Python (NumPy, SciPy), R (mc2d).

### Multi-Attribute Utility

**When**: Multiple objectives (profit, risk, strategic value, ethics) that can't all be converted to dollars.

**Approaches**:
- **Weighted scoring**: Score each option on each attribute (1-10), multiply by weight, sum. Choose highest total.
- **Utility surface**: Define utility over multiple dimensions U(x, y, z) where x=profit, y=risk, z=strategy.
- **Pareto frontier**: Identify non-dominated options (no option strictly better on all dimensions). Choose from frontier based on preferences.

**Example**: Investment A (high profit, high risk, low strategic value), Investment B (medium profit, medium risk, high strategic value). Can't say one is objectively better. Depends on weights.

### Game Theory (Strategic Interactions)

**When**: Outcome depends on competitor's choice (pricing, product launch, negotiation).

**Payoff matrix**: Rows = your choices, columns = competitor's choices, cells = your payoff given both choices.

**Nash equilibrium**: Strategy pair where neither player wants to deviate given other's strategy. May not maximize joint value.

**Expected value in games**: Estimate opponent's probabilities (mixed strategy or beliefs about their choice), calculate EV for each of your strategies, choose best response.

**Cautions**: Assumes rational opponent. Real opponents may be irrational, vindictive, or making mistakes. Model their actual behavior, not ideal.

---

## Summary

**Probability estimation**: Use multiple methods (base rates, inside view, experts, data), triangulate. Avoid overconfidence, anchoring, availability bias.

**Payoff quantification**: Include monetary (revenue, costs, NPV) and non-monetary (time, reputation, learning, strategic). Handle uncertainty with ranges or distributions.

**Decision trees**: Fold-back induction for sequential decisions. Calculate EVPI for value of information. Structure for learning (sequential > simultaneous).

**Risk preferences**: Risk-neutral → maximize EV. Risk-averse → maximize expected utility (EU). Calibrate utility function via elicitation. Account for loss aversion (Prospect Theory).

**Biases**: Overconfidence, anchoring, availability, sunk cost, tail risk neglect, false precision, static analysis. Mitigate via calibration, base rates, ranges, optionality.

**Advanced**: Correlation in portfolios, Monte Carlo for continuous distributions, multi-attribute utility for multiple objectives, game theory for strategic interactions.

**Final principle**: EV analysis structures thinking, not mechanizes decisions. Probabilities and payoffs are estimates. Sensitivity analysis reveals robustness. Combine quantitative EV with qualitative judgment (strategic fit, alignment with values, regret minimization).

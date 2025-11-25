# Outside View Principles

## Theory and Foundation

### What is the Outside View?

The **Outside View** is a forecasting method that relies on statistical baselines from similar historical cases rather than detailed analysis of the specific case at hand.

**Coined by:** Daniel Kahneman and Amos Tversky
**Alternative names:** Reference class forecasting, actuarial prediction, statistical prediction

---

## The Two Views Framework

### Inside View (The Trap)
- Focuses on unique details of the specific case
- Constructs causal narratives
- Emphasizes what makes "this time different"
- Relies on expert intuition and judgment
- Feels more satisfying and controllable

**Example:** "Our startup will succeed because we have a great team, unique technology, strong market timing, and passionate founders."

### Outside View (The Discipline)
- Focuses on statistical patterns from similar cases
- Ignores unique narratives initially
- Emphasizes what usually happens to things like this
- Relies on base rates and frequencies
- Feels cold and impersonal

**Example:** "Seed-stage B2B SaaS startups have a 10% success rate. We start at 10%."

---

## Why the Outside View Wins

### Research Evidence

**The Planning Fallacy Study (Kahneman)**
- Students asked to predict thesis completion time
- Inside view: Average prediction = 33 days
- Actual average: 55 days
- Outside view (based on past students): 48 days
- **Result:** Outside view was 7× more accurate than inside view

**Expert Predictions vs Base Rates**
- Expert forecasters using inside view: 60% accuracy
- Simple base rate models: 70% accuracy
- **Result:** Ignoring expert judgment improves predictions

**Why Experts Fail:**
1. **Overweight unique details** (availability bias)
2. **Construct plausible narratives** (hindsight bias)
3. **Underweight statistical patterns** (base rate neglect)
4. **Overconfident in causal understanding** (illusion of control)

---

## When Outside View Works Best

### High-Signal Situations
✓ Large historical datasets exist
✓ Cases are reasonably similar
✓ Outcomes are measurable
✓ No major structural changes
✓ Randomness plays a significant role

**Examples:**
- Startup success rates
- Construction project delays
- Drug approval timelines
- Movie box office performance
- Sports team performance

---

## When Outside View Fails

### Low-Signal Situations
✗ Truly novel events (no reference class)
✗ Structural regime changes (e.g., new technology disrupts all patterns)
✗ Extremely heterogeneous reference class
✗ Small sample sizes (N < 20)
✗ Deterministic physics-based systems

**Examples:**
- First moon landing (no reference class)
- Pandemic with novel pathogen (limited reference class)
- Cryptocurrency regulation (regime change)
- Your friend's personality (N = 1)

**What to do:** Use outside view as starting point, then heavily weight specific evidence

---

## Statistical Thinking vs Narrative Thinking

### Narrative Thinking (Human Default)
- Brain constructs causal stories
- Connects dots into coherent explanations
- Feels satisfying and convincing
- **Problem:** Narratives are selected for coherence, not accuracy

**Example narrative:** "Startup X will fail because the CEO is inexperienced, the market is crowded, and they're burning cash."

This might be true, but:
- Experienced CEOs also fail
- Crowded markets have winners
- Cash burn is normal for startups

The narrative cherry-picks evidence.

### Statistical Thinking (Discipline Required)
- Brain resists cold numbers
- Requires active effort to override intuition
- Feels unsatisfying and reductive
- **Benefit:** Statistics aggregate all past evidence, not just confirming cases

**Example statistical:** "80% of startups with this profile fail within 3 years. Start at 80% failure probability."

---

## The Planning Fallacy in Depth

### What It Is
Systematic tendency to underestimate time, costs, and risks while overestimating benefits.

### Why It Happens
1. **Focus on success plan:** Ignore failure modes
2. **Best-case scenario bias:** Assume things go smoothly
3. **Neglect of base rates:** "Our project is different"
4. **Anchoring on ideal conditions:** Forget reality intrudes

### The Fix: Outside View
Instead of asking "How long will our project take?" ask:
- "How long did similar projects take?"
- "What was the distribution of outcomes?"
- "What percentage ran late? By how much?"

**Rule:** Assume your project is **average** for its class until proven otherwise.

---

## Regression to the Mean

### The Phenomenon
Extreme outcomes tend to be followed by more average outcomes.

**Examples:**
- Hot hand in basketball → Returns to average
- Stellar quarterly earnings → Next quarter closer to mean
- Brilliant startup idea → Execution regresses to mean

### Implication for Forecasting
If you're predicting based on an extreme observation:
- **Adjust toward the mean** unless you have evidence the extreme is sustainable
- Extreme outcomes are often luck + skill; luck doesn't persist

**Formula:**
```
Predicted = Mean + r × (Observed - Mean)
```
Where `r` = correlation (skill component)

If 50% skill, 50% luck → r = 0.5 → Expect halfway between observed and mean

---

## Integration with Inside View

### The Proper Sequence

**Phase 1: Outside View (Base Rate)**
1. Identify reference class
2. Find base rate
3. Set starting probability = base rate

**Phase 2: Inside View (Adjustment)**
4. Identify specific evidence
5. Calculate how much evidence shifts probability
6. Apply Bayesian update

**Phase 3: Calibration**
7. Check confidence intervals
8. Stress test with premortem
9. Remove biases

**Never skip Phase 1.** Even if you plan to heavily adjust, the base rate is your anchor.

---

## Common Objections (And Rebuttals)

### "But my case really IS different!"
**Response:** Maybe. But 90% of people say this, and 90% are wrong. Prove it with evidence, not narrative.

### "Base rates are too pessimistic!"
**Response:** Optimism doesn't change reality. If the base rate is 10%, being optimistic doesn't make it 50%.

### "I have insider knowledge!"
**Response:** Great! Use Bayesian updating to adjust from the base rate. But start with the base rate.

### "This feels too mechanical!"
**Response:** Good forecasting should feel mechanical. Intuition is for generating hypotheses, not estimating probabilities.

---

## Practical Takeaways

1. **Always start with base rate** - Non-negotiable
2. **Resist narrative seduction** - Stories feel true but aren't predictive
3. **Expect regression to mean** - Extreme outcomes are temporary
4. **Use inside view as update** - Not replacement for outside view
5. **Trust frequencies over judgment** - Especially when N is large

---

**Return to:** [Main Skill](../SKILL.md#interactive-menu)

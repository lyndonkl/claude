# Common Pitfalls in Reference Class Forecasting

## The Traps That Even Experts Fall Into

---

## 1. Base Rate Neglect

### What It Is
Ignoring statistical baselines in favor of specific case details.

### Example: The Taxi Problem

**Scenario:** A taxi was involved in a hit-and-run. Witness says it was Blue.
- 85% of taxis in city are Green
- 15% of taxis are Blue
- Witness is 80% reliable in identifying colors

**Most people say:** 80% chance it was Blue (trusting the witness)

**Correct answer:**
```
P(Blue | Witness says Blue) = 41%
```

Why? The **base rate** (15% Blue taxis) dominates the witness reliability.

### In Forecasting

**The Trap:**
- Focusing on compelling story about this startup
- Ignoring that 90% of startups fail

**The Fix:**
- Start with 90% failure rate
- Then adjust based on specific evidence
- Weight base rate heavily (especially when base rate is extreme)

---

## 2. "This Time Is Different" Bias

### What It Is
Belief that current situation is unique and historical patterns don't apply.

### Classic Examples

**Financial Markets:**
- "This bubble is different" (said before every bubble burst)
- "This time housing prices won't fall"
- "This cryptocurrency is different from previous scams"

**Technology:**
- "This social network will overtake Facebook" (dozens have failed)
- "This time AI will achieve AGI" (predicted for 60 years)

**Startups:**
- "Our team is better than average" (90% of founders say this)
- "Our market timing is perfect" (survivorship bias)

### Why It Happens
1. **Narrative fallacy:** Humans construct unique stories for everything
2. **Overconfidence:** We overestimate our ability to judge uniqueness
3. **Availability bias:** Recent cases feel more salient than statistical patterns
4. **Ego:** Admitting you're "average" feels bad

### The Fix: The Reversal Test

**Question:** "If someone else claimed their case was unique for the same reasons I'm claiming, would I believe them?"

**If NO → You're applying special pleading to yourself**

### The Reality
- ~95% of cases that feel unique are actually normal
- The 5% that ARE unique still have some reference class (just more abstract)
- Uniqueness is a matter of degree, not binary

---

## 3. Overfitting to Small Samples

### What It Is
Drawing strong conclusions from limited data points.

### Example: The Hot Hand Fallacy

**Basketball:** Player makes 3 shots in a row → "Hot hand!"
**Reality:** Random sequences produce streaks. 3-in-a-row is not evidence of skill change.

### In Reference Classes

**The Trap:**
- Finding N = 5 companies similar to yours
- All 5 succeeded
- Concluding 100% success rate

**Why It's Wrong:**
- Small samples have high variance
- Sampling error dominates signal
- Regression to the mean will occur

### The Fix: Minimum Sample Size Rule

**Minimum:** N ≥ 30 for meaningful statistics
- N < 10: No statistical power
- N = 10-30: Weak signal, wide confidence intervals
- N > 30: Acceptable
- N > 100: Good
- N > 1000: Excellent

**If N < 30:**
1. Widen reference class to get more data
2. Acknowledge high uncertainty (wide CI)
3. Don't trust extreme base rates from small samples

---

## 4. Survivorship Bias

### What It Is
Only looking at cases that "survived" and ignoring failures.

### Classic Example: WW2 Bomber Armor

**Observation:** Returning bombers had bullet holes in wings and tail
**Naive conclusion:** Reinforce wings and tail
**Truth:** Planes shot in the engine didn't return (survivorship bias)
**Correct action:** Reinforce engines

### In Reference Classes

**The Trap:**
- "Reference class = Successful tech companies" (Apple, Google, Microsoft)
- Base rate = 100% success
- Ignoring all the failed companies

**Why It's Wrong:**
You're only looking at winners, which biases the base rate upward.

### The Fix: Include All Attempts

**Correct reference class:**
- "All companies that TRIED to do X"
- Not "All companies that SUCCEEDED at X"

**Example:**
- Wrong: "Companies like Facebook" → 100% success
- Right: "Social network startups 2004-2010" → 5% success

---

## 5. Regression to the Mean Neglect

### What It Is
Failing to expect extreme outcomes to return to average.

### The Sports Illustrated Jinx

**Observation:** Athletes on SI cover often perform worse after
**Naive explanation:** Curse, pressure, jinx
**Truth:** They were on cover BECAUSE of extreme (lucky) performance → Regression to mean is inevitable

### In Forecasting

**The Trap:**
- Company has amazing quarter → Predict continued amazing performance
- Ignoring: Some of that was luck, which won't repeat

**The Fix: Regression Formula**
```
Predicted = Mean + r × (Observed - Mean)
```

Where `r` = skill/(skill + luck)

**If 50% luck, 50% skill:**
```
Predicted = Halfway between observed and mean
```

### Examples

**Startup with $10M ARR in Year 1:**
- Mean for seed startups: $500K ARR
- Observed: $10M (extreme!)
- Likely some luck (viral moment, lucky timing)
- Predicted Year 2: Somewhere between $500K and $10M, not $20M

**Student who aces one test:**
- Don't predict straight A's (could have been easy test, lucky guessing)
- Predict performance closer to class average

---

## 6. Availability Bias in Class Selection

### What It Is
Choosing reference class based on what's memorable, not what's statistically valid.

### Example: Terrorism Risk

**After 9/11:**
- Availability: Terrorism is extremely salient
- Many people chose reference class: "Major terrorist attacks on US"
- Base rate felt high (because it was memorable)

**Reality:**
- Correct reference class: "Risk of death from various causes"
- Terrorism: ~0.0001% annual risk
- Car accidents: ~0.01% annual risk (100× higher)

### The Fix
1. **Don't use "what comes to mind" as reference class**
2. **Use systematic search** for historical data
3. **Weight by frequency, not memorability**

---

## 7. Confirmation Bias in Reference Class Selection

### What It Is
Choosing a reference class that supports your pre-existing belief.

### Example: Political Predictions

**If you want candidate X to win:**
- Choose reference class: "Elections where candidate had high favorability"
- Ignore reference class: "Elections in this demographic"

**If you want candidate X to lose:**
- Choose reference class: "Candidates with this scandal type"
- Ignore reference class: "Incumbents in strong economy"

### The Fix: Blind Selection

**Process:**
1. Choose reference class BEFORE you know the base rate
2. Write down selection criteria
3. Only then look up the base rate
4. Stick with it even if you don't like the answer

---

## 8. Ignoring Time Decay

### What It Is
Using old data when conditions have changed.

### Example: Newspaper Industry

**Reference class:** "Newspaper companies, 1950-2000"
**Base rate:** ~90% profitability

**Problem:** Internet fundamentally changed the industry
**Reality in 2010s:** ~10% profitability

### When Time Decay Matters

**High decay (don't use old data):**
- Technology industries (5-year half-life)
- Regulatory changes (e.g., crypto)
- Structural market shifts (e.g., remote work post-COVID)

**Low decay (old data OK):**
- Human behavior (still same evolutionary psychology)
- Physical laws (still same physics)
- Basic business economics (margins, etc.)

### The Fix
1. **Use last 5-10 years** as default
2. **Segment by era** if structural change occurred
3. **Weight recent data more heavily**

---

## 9. Causation Confusion

### What It Is
Including features in reference class that correlate but don't cause outcomes.

### Example: Ice Cream and Drowning

**Observation:** Ice cream sales correlate with drowning deaths
**Naive reference class:** "Days with high ice cream sales"
**Base rate:** Higher drowning rate

**Problem:** Ice cream doesn't cause drowning
**Confound:** Summer weather causes both

### In Forecasting

**The Trap:**
Adding irrelevant details to reference class:
- "Startups founded by left-handed CEOs"
- "Projects started on Tuesdays"
- "People born under Scorpio"

**Why It's Wrong:**
These features don't causally affect outcomes, they just add noise.

### The Fix: Causal Screening

**Ask:** "Does this feature **cause** different outcomes, or just **correlate**?"

**Include if causal:**
- Business model (causes different unit economics)
- Market size (causes different TAM)
- Technology maturity (causes different risk)

**Exclude if just correlation:**
- Founder's birthday
- Office location aesthetics
- Random demographic details

---

## 10. Narrow Framing

### What It Is
Defining the reference class too narrowly around the specific case.

### Example

**You're forecasting:** "Will this specific bill pass Congress?"

**Too narrow:** "Bills with this exact text in this specific session"
→ N = 1, no data

**Better:** "Bills of this type in similar political climate"
→ N = 50, usable data

### The Fix
If you can't find data, your reference class is too narrow. Go up one level of abstraction.

---

## 11. Extremeness Aversion

### What It Is
Reluctance to use extreme base rates (close to 0% or 100%).

### Psychological Bias

**People feel uncomfortable saying:**
- 5% chance
- 95% chance

**They retreat to:**
- 20% ("to be safe")
- 80% ("to be safe")

**This is wrong.** If the base rate is 5%, START at 5%.

### When Extreme Base Rates Are Correct

- Drug development: 5-10% reach market
- Lottery tickets: 0.0001% chance
- Sun rising tomorrow: 99.9999% chance

### The Fix
- **Trust the base rate** even if it feels extreme
- Extreme base rates are still better than gut feelings
- Use inside view to adjust, but don't automatically moderate

---

## 12. Scope Insensitivity

### What It Is
Not adjusting forecasts proportionally to scale.

### Example: Charity Donations

**Study:** People willing to pay same amount to save:
- 2,000 birds
- 20,000 birds
- 200,000 birds

**Problem:** Scope doesn't change emotional response

### In Reference Classes

**The Trap:**
- "Startup raising $1M" feels same as "Startup raising $10M"
- Reference class doesn't distinguish by scale
- Base rate is wrong

**The Fix:**
- Segment reference class by scale
- "$1M raises" have different success rate than "$10M raises"
- Make sure scope is specific

---

## Avoiding Pitfalls: Quick Checklist

Before finalizing your reference class, check:

- [ ] **Not neglecting base rate** - Started with statistics, not story
- [ ] **Not claiming uniqueness** - Passed reversal test
- [ ] **Sample size ≥ 30** - Not overfitting to small sample
- [ ] **Included failures** - No survivorship bias
- [ ] **Expected regression** - Extreme outcomes won't persist
- [ ] **Systematic selection** - Not using availability bias
- [ ] **Chose class first** - Not confirmation bias
- [ ] **Recent data** - Not ignoring time decay
- [ ] **Causal features only** - Not including random correlations
- [ ] **Right level of abstraction** - Not too narrow
- [ ] **OK with extremes** - Not moderating extreme base rates
- [ ] **Scope-specific** - Scale is accounted for

---

**Return to:** [Main Skill](../SKILL.md#interactive-menu)

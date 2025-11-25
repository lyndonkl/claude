# Debiasing Techniques

## A Practical Guide to Removing Bias from Forecasts

---

## The Systematic Debiasing Process

**The Four-Stage Framework:**
1. **Recognition** - Identify which biases are present, assess severity and direction
2. **Intervention** - Apply structured methods (not willpower), make bias mathematically impossible
3. **Validation** - Check if intervention worked, compare pre/post probabilities
4. **Institutionalization** - Build into routine process, create checklists, track effectiveness

**Key Principle:** You cannot "try harder" to avoid bias. Biases are unconscious. You need **systematic interventions**.

---

## Pre-Commitment Strategies

**Definition:** Locking in decision rules BEFORE seeing evidence, when you're still objective.

**Why it works:** Removes motivated reasoning by making updates automatic and mechanical.

### Technique 1: Pre-Registered Update Rules

**Before looking at evidence, write down:**
1. Current belief: "I believe X with Y% confidence"
2. Update rule: "If I observe Z, I will update to W%"
3. Decision criteria: "I will accept evidence Z as valid if it meets criteria Q"

**Example - Election Forecast:**
- Current: "Candidate A has 60% chance of winning"
- Update rule: "If next 3 polls show Candidate B ahead by >5%, I will update to 45%"
- Criteria: "Polls must be rated B+ or higher by 538, sample size >800, conducted in last 7 days"

**Prevents:** Cherry-picking polls, moving goalposts, asymmetric evidence standards

### Technique 2: Prediction Intervals with Triggers

**Method:** Set probability ranges that trigger re-evaluation.

**Example - Startup Valuation:**
```
If valuation announced is:
- <$50M  → Update P(success) from 40% → 25%
- $50M-$100M → Keep at 40%
- $100M-$200M → Update to 55%
- >$200M → Update to 70%
```

Lock this in before you know the actual valuation.

**Prevents:** Post-hoc rationalization, scope insensitivity, anchoring

### Technique 3: Conditional Forecasting

**Method:** Make forecasts for different scenarios in advance.

**Example - Product Launch:**
- "If launch delayed >2 months: P(success) = 30%"
- "If launch on time: P(success) = 50%"
- "If launch early: P(success) = 45%"

When scenario occurs, use pre-committed probability.

**Prevents:** Status quo bias, under-updating when conditions change

---

## External Accountability

**Why it works:** Public predictions create reputational stake. Incentive to be accurate > incentive to be "right."

### Technique 4: Forecasting Tournaments

**Platforms:** Good Judgment Open, Metaculus, Manifold Markets, PredictIt

**How to use:**
1. Make 50-100 forecasts over 6 months
2. Track your Brier score (lower = better)
3. Review what you got wrong
4. Adjust your process

**Fixes:** Overconfidence, confirmation bias, motivated reasoning

### Technique 5: Public Prediction Logging

**Method:** Post forecasts publicly (Twitter, blog, Slack, email) before outcomes known.

**Format:**
```
Forecast: [Event]
Probability: X%
Date: [Today]
Resolution date: [When we'll know]
Reasoning: [2-3 sentences]
```

**Prevents:** Hindsight bias, selective memory, probability creep

### Technique 6: Forecasting Partners

**Method:** Find a "prediction buddy" who reviews your forecasts.

**Their job:** Ask "Why this probability and not 10% higher/lower?", point out motivated reasoning, suggest alternative reference classes, track systematic biases

**Prevents:** Blind spots, soldier mindset, lazy reasoning

---

## Algorithmic Aids

**Research finding:** Simple formulas outperform expert judgment. Formulas are consistent; humans are noisy.

### Technique 7: Base Rate + Adjustment Formula

```
Final Probability = Base Rate + (Adjustment × Confidence)
```

**Example - Startup Success:**
- Base rate: 10% (seed startups reach $10M revenue)
- Specific evidence: Great team (+20%), weak market fit (-10%), strong competition (-5%) = Net +5%
- Confidence in evidence: 0.5
- Calculation: 10% + (5% × 0.5) = 12.5%

**Prevents:** Ignoring base rates, overweighting anecdotes, inconsistent weighting

### Technique 8: Bayesian Update Calculator

**Formula:** Posterior Odds = Prior Odds × Likelihood Ratio

**Example - Medical Test:**
- Prior: 1% have disease X, Test: 90% true positive, 10% false positive, You test positive
- Prior odds: 1:99, Likelihood ratio: 0.9/0.1 = 9, Posterior odds: 9:99 = 1:11
- Posterior probability: 1/12 = 8.3%

**Lesson:** Even with positive test, only 8.3% chance (low base rate dominates).

**Tool:** Use online Bayes calculator or spreadsheet template.

### Technique 9: Ensemble Forecasting

**Method:** Use multiple methods, average results.
1. Reference class forecasting → X₁%
2. Inside view analysis → X₂%
3. Extrapolation from trends → X₃%
4. Expert consensus → X₄%
5. Weighted average: 0.4×(Ref class) + 0.3×(Inside) + 0.2×(Trends) + 0.1×(Expert)

**Prevents:** Over-reliance on single method, blind spots, methodology bias

---

## Consider-the-Opposite Technique

**Core Question:** "What would have to be true for the opposite outcome to occur?"

### Technique 10: Steelman the Opposite View

**Method:**
1. State your forecast: "70% probability Event X"
2. Build STRONGEST case for opposite (don't strawman, steelman)
3. Articulate so well that someone holding that view would agree
4. Re-evaluate probability based on strength

**Example - AGI Timeline:**
- Your view: "70% chance AGI by 2030"
- Steelman: "Every previous AI timeline wrong by decades, current systems lack common sense, scaling may hit limits, regulatory slowdowns, no clear path from LLMs to reasoning, hardware constraints, reference class: major tech breakthroughs take 20-40 years"
- Re-evaluation: "Hmm, that's strong. Updating to 45%."

### Technique 11: Ideological Turing Test

**Method:** Write 200-word argument for opposite of your forecast. Show to someone who holds that view. Ask "Can you tell I don't believe this?"

**If they can tell:** You don't understand the opposing view
**If they can't tell:** You've properly steelmanned it

**Prevents:** Strawmanning, tribalism, missing legitimate counter-arguments

---

## Red Teaming and Devil's Advocate

### Technique 12: Structured Red Team Review

**Roles (60-min session):**
- **Pessimist:** "What's worst case?" (10 min)
- **Optimist:** "Are we underestimating success?" (10 min)
- **Historian:** Find historical analogies that contradict forecast (10 min)
- **Statistician:** Check the math, CI width (10 min)
- **Devil's Advocate:** Argue opposite conclusion (10 min)
- **Moderator (You):** Listen without defending, take notes, update (15 min synthesis)

**No rebuttals allowed - just listen.**

### Technique 13: Premortem + Pre-parade

**Premortem:** "It's 1 year from now, prediction was WRONG (too low). Why?"
**Pre-parade:** "It's 1 year from now, prediction was WRONG (too high). Why?"

**Method:** Assume wrong in each direction, generate 5-10 plausible reasons. If BOTH lists are plausible → confidence too high, widen range.

---

## Calibration Training

**Calibration:** When you say "70%", it happens 70% of the time.

### Technique 14: Trivia-Based Calibration

**Method:** Answer 50 trivia questions with confidence levels. Group by confidence bucket. Calculate actual accuracy in each.

**Example results:**
| Confidence | # Questions | Actual Accuracy |
|------------|-------------|-----------------|
| 60-70% | 12 | 50% (overconfident) |
| 70-80% | 15 | 60% (overconfident) |
| 80-90% | 8 | 75% (overconfident) |

**Fix:** Lower confidence levels by 15-20 points. Repeat monthly until calibrated.

**Resources:** Calibrate.app, PredictionBook.com, Good Judgment Open

### Technique 15: Confidence Interval Training

**Exercise:** Answer questions with 80% confidence intervals (population of Australia, year Eiffel Tower completed, Earth-Moon distance, etc.)

**Your 80% CIs should capture true answer 80% of time.**

**Most people:** Capture only 40-50% (too narrow = overconfident)

**Training:** Do 20 questions/week, track hit rate, widen intervals until you hit 80%

---

## Keeping a Forecasting Journal

**Problem:** Memory unreliable - we remember hits, forget misses, unconsciously revise forecasts.

**Solution:** Written record

### Technique 16: Structured Forecast Log

**Format:**
```
=== FORECAST #[Number] ===
Date: [YYYY-MM-DD]
Question: [Precise, falsifiable]
Resolution Date: [When we'll know]
Base Rate: [Reference class frequency]
My Probability: [X%]
Confidence Interval: [Lower - Upper]

REASONING:
- Reference class: [Which, why]
- Evidence for: [Bullets]
- Evidence against: [Bullets]
- Main uncertainty: [What could change]
- Biases checked: [Techniques used]

OUTCOME (fill later):
Actual: [Yes/No or value]
Brier Score: [Calculated]
What I learned: [Post-mortem]
```

### Technique 17: Monthly Calibration Review

**Process (last day of month):**
1. Review all resolved forecasts
2. Calculate: Brier score, calibration plot, trend
3. Identify patterns: Which forecast types wrong? Which biases recurring?
4. Adjust process: Add techniques, adjust confidence levels
5. Set goals: "Reduce Brier by 0.05", "Achieve 75-85% calibration on 80% forecasts"

---

## Practicing on Low-Stakes Predictions

**Problem:** High-stakes forecasts bad for learning (emotional, rare, outcome bias).

**Solution:** Practice on low-stakes, fast-resolving questions.

### Technique 18: Daily Micro-Forecasts

**Method:** Make 1-5 small predictions daily.

**Examples:** "Will it rain tomorrow?" (70%), "Email response <24h?" (80%), "Meeting on time?" (40%)

**Benefits:** Fast feedback (hours/days), low stakes, high volume (100+/month), rapid iteration

**Track in spreadsheet, calculate rolling Brier score weekly.**

### Technique 19: Sports Forecasting Practice

**Why sports:** Clear resolution, abundant data, frequent events, low stakes, good reference classes

**Method (weekly session):**
1. Pick 10 upcoming games
2. Research: team records, head-to-head, injuries, home/away splits
3. Make probability forecasts
4. Compare to Vegas odds (well-calibrated baseline)
5. Track accuracy

**Goal:** Get within 5% of Vegas odds consistently

**Skills practiced:** Reference class, Bayesian updating, regression to mean, base rate anchoring

---

## Team Forecasting Protocols

**Team problems:** Groupthink, herding (anchor on first speaker), authority bias, social desirability

### Technique 20: Independent Then Combine

**Protocol:**
1. **Independent (15 min):** Each makes forecast individually, no discussion, submit to moderator
2. **Reveal (5 min):** Show all anonymously, display range, calculate median
3. **Discussion (20 min):** Outliers speak first, others respond, no splitting difference
4. **Re-forecast (10 min):** Update independently, can stay at original
5. **Aggregate:** Median of final forecasts = team forecast (or weighted by track record, or extremize median)

**Prevents:** Anchoring on first speaker, groupthink, authority bias

### Technique 21: Delphi Method

**Protocol:** Multi-round expert elicitation
- **Round 1:** Forecast independently, provide reasoning, submit anonymously
- **Round 2:** See Round 1 summary (anonymized), read reasoning, revise if convinced
- **Round 3:** See Round 2 summary, make final forecast
- **Final:** Median of Round 3

**Prevents:** Loud voice dominance, social pressure, first-mover anchoring

**Use when:** High-stakes forecasts, diverse expert team

### Technique 22: Red Team / Blue Team Split

**Setup:**
- **Blue Team:** Argues forecast should be HIGH
- **Red Team:** Argues forecast should be LOW
- **Gray Team:** Judges and synthesizes

**Process (75 min):**
1. Preparation (20 min): Each team finds evidence for their side
2. Presentations (30 min): Blue presents (10), Red presents (10), Gray questions (10)
3. Deliberation (15 min): Gray weighs evidence, makes forecast
4. Debrief (10 min): All reconvene, discuss learning

**Prevents:** Confirmation bias, groupthink, missing arguments

---

## Quick Reference: Technique Selection Guide

**Overconfidence:** → Calibration training (#14, #15), Premortem (#13)
**Confirmation Bias:** → Consider-opposite (#10), Red teaming (#12), Steelman (#10)
**Anchoring:** → Independent-then-combine (#20), Pre-commitment (#1), Ensemble (#9)
**Base Rate Neglect:** → Base rate formula (#7), Reference class + adjustment (#7)
**Availability Bias:** → Statistical lookup, Forecasting journal (#16)
**Motivated Reasoning:** → Pre-commitment (#1, #2), Public predictions (#5), Tournaments (#4)
**Scope Insensitivity:** → Algorithmic scaling (#7), Reference class by magnitude
**Status Quo Bias:** → Pre-parade (#13), Consider-opposite (#10)
**Groupthink:** → Independent-then-combine (#20), Delphi (#21), Red/Blue teams (#22)

---

## Integration into Forecasting Workflow

**Before forecast:** Pre-commitment (#1, #2, #3), Independent (if team) (#20)
**During forecast:** Algorithmic aids (#7, #8, #9), Consider-opposite (#10, #11)
**After initial:** Red teaming (#12, #13), Calibration check (#14, #15)
**Before finalizing:** Journal entry (#16), Public logging (#5)
**After resolution:** Journal review (#17), Calibration analysis (#17)
**Ongoing practice:** Micro-forecasts (#18), Sports (#19), Tournaments (#4)

---

## The Minimum Viable Debiasing Process

**If you only do THREE things:**

**1. Pre-commit to update rules** - Write "If I see X, I'll update to Y" before evidence (prevents motivated reasoning)
**2. Keep a forecasting journal** - Log all forecasts with reasoning, review monthly (prevents hindsight bias)
**3. Practice on low-stakes predictions** - Make 5-10 micro-forecasts/week (reduces overconfidence)

---

## Summary Table

| Technique | Bias Addressed | Difficulty | Time |
|-----------|----------------|------------|------|
| Pre-registered updates (#1) | Motivated reasoning | Easy | 5 min |
| Prediction intervals (#2) | Scope insensitivity | Easy | 5 min |
| Conditional forecasting (#3) | Status quo bias | Medium | 10 min |
| Tournaments (#4) | Overconfidence | Easy | Ongoing |
| Public logging (#5) | Hindsight bias | Easy | 2 min |
| Forecasting partners (#6) | Blind spots | Medium | Ongoing |
| Base rate formula (#7) | Base rate neglect | Easy | 3 min |
| Bayesian calculator (#8) | Update errors | Medium | 5 min |
| Ensemble methods (#9) | Method bias | Medium | 15 min |
| Steelman opposite (#10) | Confirmation bias | Medium | 10 min |
| Turing test (#11) | Tribalism | Hard | 20 min |
| Red team review (#12) | Groupthink | Hard | 60 min |
| Premortem/Pre-parade (#13) | Overconfidence | Medium | 15 min |
| Trivia calibration (#14) | Overconfidence | Easy | 20 min |
| CI training (#15) | Overconfidence | Easy | 15 min |
| Forecast journal (#16) | Multiple | Easy | 5 min |
| Monthly review (#17) | Calibration drift | Medium | 30 min |
| Micro-forecasts (#18) | Overconfidence | Easy | 5 min/day |
| Sports practice (#19) | Multiple | Medium | 30 min/week |
| Independent-then-combine (#20) | Groupthink | Medium | 50 min |
| Delphi method (#21) | Authority bias | Hard | 90 min |
| Red/Blue teams (#22) | Confirmation bias | Hard | 75 min |

---

**Return to:** [Main Skill](../SKILL.md#interactive-menu)

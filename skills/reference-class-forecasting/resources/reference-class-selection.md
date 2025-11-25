# Reference Class Selection Guide

## The Art and Science of Choosing Comparison Sets

Selecting the right reference class is the most critical judgment call in forecasting. Too broad and the base rate is meaningless. Too narrow and you have no data.

---

## The Goldilocks Principle

### Too Broad
**Problem:** High variance, low signal
**Example:** "Companies" as reference class for a fintech startup
**Base rate:** ~50% fail? 90% fail? Meaningless.
**Why it fails:** Includes everything from lemonade stands to Apple

### Too Narrow
**Problem:** No data, overfitting
**Example:** "Fintech startups founded in Q2 2024 by Stanford CS grads in SF"
**Base rate:** N = 3 companies, no outcomes yet
**Why it fails:** So specific there's no statistical pattern

### Just Right
**Sweet spot:** Specific enough to be homogeneous, broad enough to have data
**Example:** "Seed-stage B2B SaaS startups in financial services"
**Base rate:** Can find N = 200+ companies with 5-year outcomes
**Why it works:** Specific enough to be meaningful, broad enough for statistics

---

## Systematic Selection Method

### Step 1: Define the Core Entity Type

**Question:** What is the fundamental category?

**Examples:**
- Company (startup, public company, nonprofit)
- Project (software, construction, research)
- Person (athlete, politician, scientist)
- Event (election, war, natural disaster)
- Product (consumer, enterprise, service)

**Output:** "This is a [TYPE]"

---

### Step 2: Add Specificity Layers

Work through these dimensions **in order of importance:**

#### Layer 1: Stage/Size
- Startups: Pre-seed, Seed, Series A, B, C, Growth
- Projects: Small (<$1M), Medium ($1-10M), Large (>$10M)
- People: Beginner, Intermediate, Expert
- Products: MVP, Version 1.0, Mature

#### Layer 2: Category/Domain
- Startups: B2B, B2C, B2B2C
- Industry: Fintech, Healthcare, SaaS, Hardware
- Projects: Software, Construction, Pharmaceutical
- People: Role (CEO, Engineer, Designer)

#### Layer 3: Geography/Market
- US, Europe, Global
- Urban, Rural, Suburban
- Developed, Emerging markets

#### Layer 4: Time Period
- Current decade (2020s)
- Previous decade (2010s)
- Historical (pre-2010)

**Output:** "This is a [Stage] [Category] [Geography] [Type] from [Time Period]"

**Example:** "This is a Seed-stage B2B SaaS startup in the US from 2020-2024"

---

### Step 3: Test for Data Availability

**Search queries:**
```
"[Reference Class] success rate"
"[Reference Class] statistics"
"[Reference Class] survival rate"
"How many [Reference Class] succeed"
```

**Data availability check:**
- ✓ Found published studies/reports → Good reference class
- ⚠ Found anecdotal data → Usable but weak
- ✗ No data found → Reference class too narrow

**If no data:** Remove least important specificity layer and retry

---

### Step 4: Validate Homogeneity

**Question:** Are members of this class similar enough that averaging makes sense?

**Test: Variance Check**
If you have outcome data, calculate variance:
- Low variance → Good reference class (outcomes cluster)
- High variance → Bad reference class (outcomes all over the place)

**Heuristic: The Substitution Test**
Pick any two members of the reference class at random.

**Ask:** "If I swapped one for the other, would the prediction change dramatically?"
- No → Good homogeneity
- Yes → Too broad, needs subdivision

**Example:**
- "Tech startups" → Swap consumer mobile app for enterprise database company → Prediction changes drastically → **Too broad**
- "Seed-stage B2B SaaS" → Swap CRM tool for analytics platform → Prediction mostly same → **Good homogeneity**

---

## Similarity Metrics

### When You Can't Find Exact Match

If no perfect reference class exists, use **similarity matching** to find nearest neighbors.

### Dimensions of Similarity

**For Startups:**
1. Business model (B2B, B2C, marketplace, SaaS)
2. Revenue model (subscription, transaction, ads)
3. Stage/funding (seed, Series A, etc.)
4. Team size
5. Market size
6. Technology complexity

**For Projects:**
1. Size (budget, team size, duration)
2. Complexity (simple, moderate, complex)
3. Technology maturity (proven, emerging, experimental)
4. Team experience
5. Dependencies (few, many)

**For People:**
1. Experience level
2. Domain expertise
3. Resources available
4. Historical track record
5. Contextual factors (support, environment)

### Similarity Scoring

**Method: Nearest Neighbors**

1. List all dimensions of similarity (5-7 dimensions)
2. For each dimension, score how similar the case is to reference class (0-10)
3. Average the scores
4. Threshold: If similarity < 7/10, the reference class may not apply

**Example:**
Comparing "AI startup in 2024" to "Software startups 2010-2020" reference class:
- Business model: 9/10 (same)
- Revenue model: 8/10 (mostly SaaS)
- Technology maturity: 4/10 (AI is newer)
- Market size: 7/10 (comparable)
- Team size: 8/10 (similar)
- Funding environment: 5/10 (tighter in 2024)

**Average: 6.8/10** → Marginal reference class; use with caution

---

## Edge Cases and Judgment Calls

### Case 1: Structural Regime Change

**Problem:** Conditions have changed fundamentally since historical data

**Examples:**
- Pre-internet vs post-internet business
- Pre-COVID vs post-COVID work patterns
- Pre-AI vs post-AI software development

**Solution:**
1. Segment data by era if possible
2. Use most recent data only
3. Adjust base rate for known structural differences
4. Increase uncertainty bounds

---

### Case 2: The N=1 Problem

**Problem:** The case is literally unique (first of its kind)

**Examples:**
- First moon landing
- First pandemic of a novel pathogen
- First AGI system

**Solution:**
1. **Widen the class** - Go up one abstraction level
   - "First moon landing" → "First major engineering projects"
   - "Novel pandemic" → "Past pandemics of any type"
2. **Component decomposition** - Break into parts that have reference classes
   - "Moon landing" → Rocket success rate × Navigation accuracy × Life support reliability
3. **Expert aggregation** - When no data, aggregate expert predictions (but with humility)

---

### Case 3: Multiple Plausible Reference Classes

**Problem:** Event could belong to multiple classes with different base rates

**Example:** "Elon Musk starting a brain-computer interface company"

Possible reference classes:
- "Startups by serial entrepreneurs" → 40% success
- "Medical device startups" → 10% success
- "Moonshot technology ventures" → 5% success
- "Companies founded by Elon Musk" → 80% success

**Solution: Ensemble Averaging**
1. Identify all plausible reference classes
2. Find base rate for each
3. Weight by relevance/similarity
4. Calculate weighted average

**Example weights:**
- Medical device (40%): 10% × 0.4 = 4%
- Moonshot tech (30%): 5% × 0.3 = 1.5%
- Serial entrepreneur (20%): 40% × 0.2 = 8%
- Elon track record (10%): 80% × 0.1 = 8%

**Weighted base rate: 21.5%**

---

## Common Selection Mistakes

### Mistake 1: Cherry-Picking Success Examples
**What it looks like:** "Reference class = Companies like Apple, Google, Facebook"
**Why it's wrong:** Survivorship bias - only looking at winners
**Fix:** Include all attempts, not just successes

### Mistake 2: Availability Bias
**What it looks like:** Reference class = Recent, memorable cases
**Why it's wrong:** Recent events are overweighted in memory
**Fix:** Use systematic data collection, not what comes to mind

### Mistake 3: Confirmation Bias
**What it looks like:** Choosing reference class that supports your prior belief
**Why it's wrong:** You're reverse-engineering the answer
**Fix:** Choose reference class BEFORE looking at base rate

### Mistake 4: Overfitting to Irrelevant Details
**What it looks like:** "Female, left-handed CEOs who went to Ivy League schools"
**Why it's wrong:** Most details don't matter; you're adding noise
**Fix:** Only include features that causally affect outcomes

### Mistake 5: Ignoring Time Decay
**What it looks like:** Using data from 1970s for 2024 prediction
**Why it's wrong:** World has changed
**Fix:** Weight recent data more heavily, or segment by era

---

## Reference Class Hierarchy

### Start Specific, Widen as Needed

**Level 1: Maximally Specific** (Try this first)
- Example: "Seed-stage B2B cybersecurity SaaS in US, 2020-2024"
- Check for data → If N > 30, use this

**Level 2: Drop One Feature** (If L1 has no data)
- Example: "Seed-stage B2B SaaS in US, 2020-2024" (removed "cybersecurity")
- Check for data → If N > 30, use this

**Level 3: Drop Two Features** (If L2 has no data)
- Example: "Seed-stage B2B SaaS, 2020-2024" (removed "US")
- Check for data → If N > 30, use this

**Level 4: Generic Category** (Last resort)
- Example: "Seed-stage startups"
- Always has data, but high variance

**Rule:** Use the most specific level that still gives you N ≥ 30 data points.

---

## Checklist: Is This a Good Reference Class?

Use this to validate your choice:

- [ ] **Sample size** ≥ 30 historical cases
- [ ] **Homogeneity**: Members are similar enough that averaging makes sense
- [ ] **Relevance**: Data is from appropriate time period (last 10 years preferred)
- [ ] **Specificity**: Class is narrow enough to be meaningful
- [ ] **Data availability**: Base rate is published or calculable
- [ ] **No survivorship bias**: Includes failures, not just successes
- [ ] **No cherry-picking**: Class chosen before looking at base rate
- [ ] **Causal relevance**: Features included actually affect outcomes

**If ≥ 6 checked:** Good reference class
**If 4-5 checked:** Acceptable, but increase uncertainty
**If < 4 checked:** Find a better reference class

---

## Advanced: Bayesian Reference Class Selection

When you have multiple plausible reference classes, you can use Bayesian reasoning:

### Step 1: Prior Distribution Over Classes
Assign probability to each reference class being the "true" one

**Example:**
- P(Class = "B2B SaaS") = 60%
- P(Class = "All SaaS") = 30%
- P(Class = "All startups") = 10%

### Step 2: Likelihood of Observed Features
How likely is this specific case under each class?

### Step 3: Posterior Distribution
Update class probabilities using Bayes' rule

### Step 4: Weighted Base Rate
Average base rates weighted by posterior probabilities

**This is advanced.** Default to the systematic selection method above unless you have strong quantitative skills.

---

## Practical Workflow

### Quick Protocol (5 minutes)

1. **Name the core type:** "This is a [X]"
2. **Add 2-3 specificity layers:** Stage, category, geography
3. **Google the base rate:** "[Reference class] success rate"
4. **Sanity check:** Does N > 30? Are members similar?
5. **Use it:** This is your starting probability

### Rigorous Protocol (30 minutes)

1. Systematic selection (Steps 1-4 above)
2. Similarity scoring for validation
3. Check for structural regime changes
4. Consider multiple reference classes
5. Weighted ensemble if multiple classes
6. Document assumptions and limitations

---

**Return to:** [Main Skill](../SKILL.md#interactive-menu)

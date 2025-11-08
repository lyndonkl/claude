# Fermi Estimation Methodology

Advanced techniques for anchoring, bounding, triangulation, and calibration.

## Workflow

```
Fermi Estimation Progress:
- [ ] Step 1: Clarify the question and define metric
- [ ] Step 2: Decompose into estimable components
- [ ] Step 3: Estimate components using anchors
- [ ] Step 4: Bound with upper/lower limits
- [ ] Step 5: Calculate and sanity-check
- [ ] Step 6: Triangulate with alternate path
```

**Step 1: Clarify the question and define metric**

Define scope, units, decision context before decomposition.

**Step 2: Decompose into estimable components**

Choose decomposition strategy based on problem structure and available knowledge.

**Step 3: Estimate components using anchors**

Apply [1. Anchoring Techniques](#1-anchoring-techniques) to ground estimates in known quantities.

**Step 4: Bound with upper/lower limits**

Use [2. Bounding Techniques](#2-bounding-techniques) to bracket answer with constraints.

**Step 5: Calculate and sanity-check**

Validate using dimensional analysis, reality checks, and [3. Calibration Methods](#3-calibration-methods).

**Step 6: Triangulate with alternate path**

Apply [4. Triangulation Approaches](#4-triangulation-approaches) to estimate via different decomposition.

---

## 1. Anchoring Techniques

Methods for grounding component estimates in known quantities.

### Common Knowledge Anchors

**Demographics**: Population figures, household counts, labor force
- US population: ~330M (2020s), grows ~0.5%/year
- US households: ~130M, avg 2.5 people/household
- US labor force: ~165M, unemployment typically 3-6%
- Global: ~8B people, ~2B households, ~55% urban

**Economic**: GDP, spending, income
- US GDP: ~$25T, per capita ~$75k
- Median household income: ~$70k
- Consumer spending: ~70% of GDP
- Federal budget: ~$6T (~24% of GDP)

**Physical constants**: Time, space, energy
- Earth: ~510M km², ~70% water, ~150M km² land
- US land: ~10M km² (~3.8M sq mi)
- Day = 24 hours, year ≈ 365 days ≈ 52 weeks
- Typical human: 70kg, 2000 kcal/day, 8hr sleep, 16hr awake

**Business benchmarks**: SaaS metrics, retail, tech
- SaaS ARR per employee: $150-300k (mature companies)
- Retail revenue per sq ft: $300-500/year (varies by category)
- Tech company valuation: 5-15× revenue (growth stage), 2-5× (mature)
- CAC payback: <12 months good, <18 acceptable

### Data Lookup Strategies

**Quick reliable sources** (use for anchoring):
- Google: Population figures, company sizes, market data
- Wikipedia: Demographics, economic stats, physical data
- Public company filings: Revenue, employees, customers (10-K, investor decks)
- Industry reports: Gartner, Forrester, McKinsey (market sizing)

**Estimation from fragments**:
- Company has "thousands of employees" → Estimate 3,000-5,000
- Market is "multi-billion dollar" → Estimate $2-9B
- "Most people" do X → Estimate 60-80%
- "Rare" occurrence → Estimate <5%

### Personal Experience Anchors

**Observation-based**: Use your own data points
- How many apps on your phone? (extrapolate to avg user)
- How often do you buy X? (extrapolate to market)
- How long does task Y take? (estimate productivity)

**Analogous reasoning**: Scale from known to unknown
- If you know NYC subway ridership, estimate SF BART by population ratio
- If you know your company's churn, estimate competitor's by industry norms
- If you know local restaurant count, estimate city-wide by neighborhood scaling

**Bracketing intuition**: Use confidence ranges
- "I'm 80% confident the answer is between X and Y"
- Then use geometric mean: √(X×Y) as central estimate
- Example: Starbucks locations - probably between 10k and 50k → ~22k (actual ~16k)

---

## 2. Bounding Techniques

Methods for calculating upper/lower limits to bracket the answer.

### Constraint-Based Bounding

**Physical constraints**: Cannot exceed laws of nature
- Maximum speed: Speed of light (for data), sound (for physical travel), human limits (for manual tasks)
- Maximum density: People per area (fire code limits, standing room), data per volume (storage media)
- Maximum efficiency: Thermodynamic limits, conversion efficiency (solar ~20-25%, combustion ~35-45%)

**Economic constraints**: Cannot exceed available resources
- Market size bounded by: GDP, consumer spending, addressable population × willingness to pay
- Company revenue bounded by: Market size × maximum possible share (~20-30% typically)
- Headcount bounded by: Budget ÷ avg salary, or revenue ÷ revenue per employee benchmark

**Time constraints**: Cannot exceed available hours
- Work output bounded by: People × hours/person × productivity
- Example: "How many customers can support team handle?" → Agents × (40 hr/week - 10hr meetings) × tickets/hr

### Scenario-Based Bounding

**Optimistic scenario** (favorable assumptions):
- High adoption (80-100% of addressable market)
- Premium pricing (top quartile of range)
- High efficiency (best-in-class productivity)
- Fast growth (aggressive but plausible)

**Pessimistic scenario** (conservative assumptions):
- Low adoption (5-20% of addressable market)
- Discount pricing (bottom quartile of range)
- Low efficiency (industry average or below)
- Slow growth (cautious, accounts for setbacks)

**Example - Market sizing**:
- Optimistic: All 500k target businesses × $100/month × 12 = $600M
- Pessimistic: 5% penetration (25k) × $30/month × 12 = $9M
- Range: $9M - $600M (67× span → likely too wide, refine assumptions)

### Sensitivity Analysis

Identify which assumptions most affect result:

**Method**: Vary each component ±50%, measure impact on final estimate

**High sensitivity components**: Small change → large impact on result
- Focus refinement effort here
- Example: If CAC varies 50% and final ROI changes 40%, CAC is high sensitivity

**Low sensitivity components**: Large change → small impact on result
- Less critical to get precise
- Example: If office rent varies 50% but total costs change 5%, rent is low sensitivity

**Rule of thumb**: 80% of uncertainty often comes from 20% of assumptions. Find and refine those critical few.

---

## 3. Calibration Methods

Techniques for improving estimation accuracy through practice and feedback.

### Calibration Exercises

**Known problems**: Practice on verifiable questions, compare estimate to actual

**Exercise set 1 - Demographics**:
1. US population in 1950? (Estimate, then check: ~150M)
2. Number of countries in UN? (Estimate, then check: ~190)
3. World's tallest building height? (Estimate, then check: ~830m Burj Khalifa)

**Exercise set 2 - Business**:
1. Starbucks annual revenue? (Estimate, then check: ~$35B)
2. Google employees worldwide? (Estimate, then check: ~150k)
3. Average Netflix subscription price? (Estimate, then check: ~$15/month)

**Exercise set 3 - Consulting classics**:
1. Piano tuners in Chicago? (Estimate, then check: ~100)
2. Gas stations in US? (Estimate, then check: ~150k)
3. Golf balls fitting in school bus? (Estimate, then check: ~500k)

**Feedback loop**:
- Track your estimate vs actual ratio
- If consistently >3× off, identify bias (underestimate? overestimate?)
- Calibrate future estimates (if you typically 2× low, mentally adjust upward)

### Confidence Intervals

Express uncertainty quantitatively:

**90% confidence interval**: "I'm 90% sure the answer is between X and Y"
- Width reflects uncertainty (narrow = confident, wide = uncertain)
- Calibration: Of 10 estimates with 90% CI, ~9 should contain true value

**Common mistakes**:
- Too narrow (overconfidence): Only 50% of your "90% CIs" contain true value
- Too wide (useless): All your CIs span 3+ orders of magnitude
- Goal: Calibrated such that X% of your X% CIs are correct

**Practice calibration**:
1. Make 20 estimates with 80% CIs
2. Check how many actually contained true value
3. If <16 (80% of 20), you're overconfident → widen future CIs
4. If >18, you're underconfident → narrow future CIs

### Bias Identification

**Anchoring bias**: Over-relying on first number you hear
- Mitigation: Generate estimate independently before seeing any numbers
- Test: Estimate revenue before someone says "Is it $10M?" vs after

**Availability bias**: Overweighting recent/memorable events
- Mitigation: Seek base rates, historical averages, not just recent headline cases
- Example: Don't estimate startup success rate from TechCrunch unicorn coverage

**Optimism bias**: Tendency to assume favorable outcomes
- Mitigation: Explicitly calculate pessimistic scenario, force consideration of downsides
- Particularly important for: Timelines, costs, adoption rates

**Unit confusion**: Mixing millions/billions, per-day/per-year
- Mitigation: Always write units, check dimensional analysis
- Example: Company earns $10M/year = ~$27k/day (sanity check: does that seem right for scale?)

---

## 4. Triangulation Approaches

Estimating the same quantity via multiple independent paths to validate.

### Supply-Side vs Demand-Side

**Supply-side**: Count producers/capacity, estimate output
- Example (Uber drivers in SF):
  - ~5,000 drivers (estimated from driver forum activity, Uber PR)
  - ~30 rides/day per driver
  - = 150,000 rides/day in SF

**Demand-side**: Count consumers/need, estimate consumption
- Example (Uber rides in SF):
  - ~900k population
  - ~5% use Uber daily (frequent users)
  - ~3 rides per user-day
  - = 135,000 rides/day in SF

**Triangulation**: 150k (supply) vs 135k (demand) → Within 10%, confidence high

### Top-Down vs Bottom-Up

**Top-down**: Start with large total, filter down
- Example (Restaurant revenue in city):
  - 1M population
  - ~$8k/person annual food spending
  - ~40% spent at restaurants
  - = $3.2B restaurant revenue

**Bottom-up**: Start with unit, scale up
- Example (Restaurant revenue in city):
  - ~1,500 restaurants
  - ~50 meals/day per restaurant
  - ~$25 average check
  - ~350 days/year
  - = ~$650M restaurant revenue

**Discrepancy**: $3.2B vs $650M → 5× difference, investigate!
- Possible explanations: Underestimated restaurants (chains, cafes, food trucks), or overestimated per-capita spending

### Multiple Decomposition Paths

**Example - Estimating AWS revenue**:

**Path 1 - Customer-based**:
- ~1M active AWS customers (public statements)
- Average spend ~$10k/year (mix of startups $1k, enterprises $100k+)
- = $10B revenue

**Path 2 - Workload-based**:
- ~5M EC2 instances running globally (estimated from public data)
- ~$500/month avg per instance (mix of small/large)
- = $30B revenue

**Path 3 - Market share**:
- Cloud infrastructure market ~$200B (2023)
- AWS market share ~30%
- = $60B revenue

**Triangulation**: $10B vs $30B vs $60B → Within same order of magnitude, actual AWS revenue ~$85B (2023)
- All paths got within 3-10× (reasonable for Fermi), but spread suggests different assumptions need refinement

### Cross-Validation with Public Data

After Fermi estimate, quickly check if public data exists:

**Public company financials**: 10-K filings, investor presentations
- Validate: Revenue, employees, customers, margins

**Industry reports**: Gartner, IDC, Forrester market sizing
- Validate: TAM, growth rates, share

**Government data**: Census, BLS, FDA, EPA
- Validate: Population, employment, health, environment figures

**Academic studies**: Research papers on adoption, behavior, impact
- Validate: Penetration rates, usage patterns, effect sizes

**Purpose**: Not to replace Fermi process, but to:
1. Calibrate (am I within 10×? If not, what's wrong?)
2. Refine (can I improve assumptions with real data?)
3. Build confidence (multiple paths + public data all agree → high confidence)

---

## 5. Advanced Decomposition Patterns

### Conversion Funnel Decomposition

For estimating outcomes in multi-step processes:

**Structure**:
```
Starting population
× Conversion 1 (% that complete step 1)
× Conversion 2 (% that complete step 2 | completed 1)
× Conversion 3 (% that complete step 3 | completed 2)
= Final outcome
```

**Example - SaaS conversions**:
```
Website visitors: 100k/month
× Trial signup: 5% = 5k trials
× Activation: 60% = 3k activated
× Paid conversion: 20% = 600 new customers/month
```

### Cohort-Based Decomposition

For estimating aggregate from groups with different characteristics:

**Example - App revenue**:
```
Cohort 1 (Power users): 10k users × $20/month = $200k
Cohort 2 (Regular users): 100k users × $5/month = $500k
Cohort 3 (Free users): 1M users × $0 = $0
Total: $700k/month
```

### Dimensional Analysis

Using units to guide decomposition:

**Example**: Estimating data center power consumption (want kW)
```
Servers (count)
× Power per server (kW/server)
+ Cooling overhead (×1.5 for PUE)
= Total power (kW)
```

Units guide you: Need kW, have servers → must find kW/server, which is estimable

---

## 6. Common Estimation Pitfalls

**Compounding errors**: Errors multiply in chains
- 3 components each ±50% uncertain → final estimate ±300% uncertain
- Mitigation: Keep decomposition shallow (3-5 levels max), validate high-sensitivity components

**False precision**: Reporting 8.372M when uncertainty is ±3×
- Mitigation: Round to 1-2 significant figures (8M not 8.372M), express as range

**Linearity assumption**: Assuming proportional scaling when it's not
- Reality: Economies of scale (costs grow sub-linearly), network effects (value grows super-linearly)
- Mitigation: Check if relationship is truly linear or if power law applies

**Survivorship bias**: Estimating from successes only
- Example: Average startup revenue based on unicorns (ignoring 90% that failed)
- Mitigation: Include full distribution, weight by probability

**Time-period confusion**: Mixing annual, monthly, daily figures
- Example: "Company earns $1M" - per year? per month? Need clarity.
- Mitigation: Always specify time units, convert to common basis

**Outdated anchors**: Using pre-pandemic data for post-pandemic estimates
- Example: Office occupancy, remote work adoption, e-commerce penetration all shifted
- Mitigation: Check anchor recency, adjust for structural changes

**Ignoring constraints**: Estimates that violate physics/economics
- Example: Market size exceeding GDP, growth rate >100%/year sustained indefinitely
- Mitigation: Sanity-check against absolute limits

**Double-counting**: Including same quantity twice
- Example: Counting both "businesses" and "employees" when businesses already includes employee count
- Mitigation: Draw clear decomposition tree, check for overlap

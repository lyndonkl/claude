# Business Narrative Builder Methodology

Deep reference for the 6-stage corporate life cycle model, narrative-to-numbers framework, narrative plausibility testing, competitive advantage assessment, and TAM sizing methodology.

## Table of Contents
- [6-Stage Corporate Life Cycle Model](#6-stage-corporate-life-cycle-model)
- [Narrative-to-Numbers Framework](#narrative-to-numbers-framework)
- [Narrative Plausibility Testing](#narrative-plausibility-testing)
- [Competitive Advantage Assessment](#competitive-advantage-assessment)
- [TAM Sizing Methodology](#tam-sizing-methodology)
- [Industry Margin Benchmarks](#industry-margin-benchmarks)
- [Common Narrative Failures](#common-narrative-failures)

---

## 6-Stage Corporate Life Cycle Model

Based on Damodaran's corporate life cycle framework. Each stage has distinct characteristics that shape the narrative and value drivers.

### Stage 1: Start-up ("The Lightbulb Moment")

| Characteristic | Description |
|---------------|-------------|
| Revenue | Minimal or zero; may be pre-revenue |
| Earnings | Deep losses; no operating income |
| Funding | Founders, angels, seed/Series A |
| Competition | Market may not exist yet |
| Key uncertainty | Does the idea have potential? |
| Risk type | Company-specific; idea and execution risk |
| Typical duration | 1-3 years |

**Narrative implications**: Story is about the idea and the founding team. Numbers are largely speculative. TAM sizing is critical because it defines the ceiling. Failure probability is high (50-80% for most start-ups). Valuation is driven by optionality and vision.

### Stage 2: Young Growth ("From Idea to Business")

| Characteristic | Description |
|---------------|-------------|
| Revenue | Growing rapidly (>30% per year) |
| Earnings | Negative or barely positive |
| Funding | Venture capital, early public markets |
| Competition | Emerging; market structure forming |
| Key uncertainty | Is there a viable business model? |
| Risk type | Company-specific shifting toward market risk |
| Typical duration | 3-7 years |

**Narrative implications**: Story is about business model validation and path to profitability. Target operating margin comes from mature industry peers (not the company's own history). Sales-to-capital ratio is critical for estimating reinvestment needs. Failure probability is meaningful (10-30%). Revenue growth is the dominant driver.

### Stage 3: High Growth ("The Bar Mitzvah")

| Characteristic | Description |
|---------------|-------------|
| Revenue | Growing at 15-30% per year |
| Earnings | Turning positive; margins expanding |
| Funding | Mix of internal cash flow and external capital |
| Competition | Multiple players; market structure solidifying |
| Key uncertainty | Will the business generate profits at scale? |
| Risk type | Mix of company-specific and macro |
| Typical duration | 5-10 years |

**Narrative implications**: Story shifts from "can it work?" to "how big can it get?" Operating margins should be converging toward industry norms. Reinvestment rate is still high but declining. Competitive advantage period (length of high growth) becomes a key narrative element.

### Stage 4: Mature Growth ("The Scaling Up Test")

| Characteristic | Description |
|---------------|-------------|
| Revenue | Growing at 5-15% per year |
| Earnings | Positive and growing |
| Funding | Primarily internal cash flow |
| Competition | Established market with clear leaders |
| Key uncertainty | Can the business be scaled further? |
| Risk type | Predominantly macro/market risk |
| Typical duration | 5-15 years |

**Narrative implications**: Story focuses on reinvestment quality and adjacent market expansion. Return on capital vs cost of capital determines whether growth creates value. Competitive advantages are durable but not permanent. Failure probability is low (<5%).

### Stage 5: Mature Stable ("The Midlife Crisis")

| Characteristic | Description |
|---------------|-------------|
| Revenue | Growing near GDP (0-5%) |
| Earnings | High and stable |
| Funding | Excess cash flow; returning capital |
| Competition | Oligopoly or stable competitive landscape |
| Key uncertainty | Can the business be defended? |
| Risk type | Macro risk; disruption risk |
| Typical duration | 10-30+ years |

**Narrative implications**: Story is about competitive moat durability and capital allocation. Revenue growth converges to risk-free rate or GDP growth. Operating margin is at or near long-term target. Focus shifts from growth investment to capital return (dividends, buybacks). The key narrative risk is disruption from new entrants or technology shifts.

### Stage 6: Decline ("The End Game")

| Characteristic | Description |
|---------------|-------------|
| Revenue | Declining |
| Earnings | Falling; margins contracting |
| Funding | Divesting assets; managing cash |
| Competition | Market shrinking or company losing share |
| Key uncertainty | Will management face reality? |
| Risk type | Company-specific; management and strategic risk |
| Typical duration | Varies; can be extended through managed decline |

**Narrative implications**: Story depends on whether management accepts reality or fights it. Two sub-narratives: (a) managed decline -- shrink gracefully, maximize cash extraction, return capital; (b) turnaround -- new management, strategic pivot, narrative reset. Both are valid; the key is evidence for which is more plausible.

### Stage Transition Signals

| Transition | Signals to Watch |
|-----------|-----------------|
| Start-up to Young Growth | First meaningful revenue; product-market fit indicators |
| Young Growth to High Growth | Operating income turns positive; unit economics proven |
| High Growth to Mature Growth | Revenue growth decelerates below 15%; market share stabilizes |
| Mature Growth to Mature Stable | Revenue growth falls below 5%; excess cash flow begins |
| Mature Stable to Decline | Revenue begins contracting; market share erodes; disruption emerges |

---

## Narrative-to-Numbers Framework

Damodaran's 5-step process for converting a business story into valuation inputs.

### Step 1: Develop a narrative for the business

Tell the story of how the business evolves over time. A good narrative addresses:

- **What market does the company operate in?** (current and potential)
- **How big can the company get?** (revenue trajectory bounded by TAM)
- **What competitive advantages does it have?** (and how long do they last?)
- **How will the company make money?** (margin trajectory and business model)
- **What can go wrong?** (risk factors and failure scenarios)

The narrative should be specific to the company, not generic. "Company X will grow revenue" is not a narrative. "Company X will expand from domestic e-commerce into international markets, leveraging its logistics infrastructure to achieve a 15% operating margin as it scales to $50B in revenue over the next decade" is a narrative.

### Step 2: Test the narrative for plausibility

Apply the three-tier plausibility test (see [Narrative Plausibility Testing](#narrative-plausibility-testing) below):
- **Possible**: Could this happen? (Is it physically and economically possible?)
- **Plausible**: Is it reasonable? (Does evidence support it?)
- **Probable**: Is it likely? (Is it the most likely outcome among alternatives?)

### Step 3: Convert the narrative into value drivers

Map each narrative element to a specific valuation input:

| Narrative Element | Value Driver | How to Quantify |
|-------------------|-------------|-----------------|
| "How big can it get?" | Revenue growth rate | TAM x target share, compute CAGR from current to target |
| "How will it make money?" | Target operating margin | Benchmark against mature industry peers (median and quartiles) |
| "How much reinvestment?" | Sales-to-capital ratio | Revenue / Invested Capital; industry benchmarks |
| "What can go wrong?" | Cost of capital | WACC from cost-of-capital-estimator; higher for riskier narratives |
| "Could it fail entirely?" | Failure probability | Cash burn analysis, industry failure rates, Altman Z-score |

Every number should be backed by a portion of the story, and every part of the story should have a place in the numbers.

### Step 4: Connect drivers to a valuation

Feed the value drivers into a discounted cash flow model:

```
Expected FCFF = Revenue x Operating Margin x (1 - Tax Rate) - Reinvestment
Value = Sum of PV(FCFF) over high-growth period + PV(Terminal Value)
```

This step is handled by the `intrinsic-valuation-dcf` skill. The narrative builder's job is to produce the inputs; the DCF skill computes the output.

### Step 5: Keep the feedback loop open

Listen to people who know the business and use their input to refine the narrative:
- Industry experts may challenge TAM assumptions
- Competitors' results provide margin benchmarks
- Macroeconomic shifts may alter the growth trajectory
- Management actions may confirm or invalidate the narrative

Work out the effects of alternative narratives on valuation. The gap between narratives represents uncertainty in the estimate.

---

## Narrative Plausibility Testing

A framework for disciplining narratives so they produce defensible valuations.

### Three Tiers of Plausibility

**Tier 1 -- Possible**: Could this happen?
- The narrative does not violate physical laws, market size constraints, or basic economic logic
- Revenue projections do not exceed TAM
- Margin assumptions are within the range observed in any industry
- Growth rates are achievable (have been achieved by some company in some market)
- Test: "Can I point to at least one historical example of something similar?"

**Tier 2 -- Plausible**: Is it reasonable given the evidence?
- The narrative is consistent with observable facts about the company and industry
- Revenue growth is supported by customer data, market trends, or management track record
- Margin trajectory matches the competitive dynamics of the industry
- The company has the resources (capital, talent, technology) to execute
- Test: "Would a knowledgeable industry participant find this credible?"

**Tier 3 -- Probable**: Is this the most likely outcome?
- The narrative is the best single prediction among alternatives
- It accounts for the most likely competitive responses
- It reflects realistic management execution (not best-case)
- Base rates for similar companies support the assumptions
- Test: "If I had to bet, would I bet on this narrative over alternatives?"

### Plausibility Red Flags

- Revenue projection implies market share above 30-40% in a fragmented, competitive market
- Operating margin target exceeds the industry leader by more than 5 percentage points without clear structural explanation
- Growth rate sustained at >20% for more than 10 years (very few companies achieve this)
- Failure probability set to 0% for any company not yet profitable
- No competitive response assumed (the company grows unopposed)
- "Everything goes right" narrative with no acknowledgment of risks

### Narrative Scoring Matrix

| Dimension | Weak (1) | Adequate (3) | Strong (5) |
|-----------|----------|-------------|------------|
| Specificity | Generic ("will grow") | Directional ("will grow 15-20%") | Precise with logic ("will grow 18% via international expansion, adding $2B in 3 years") |
| Evidence base | Assertion only | Some data cited | Multiple data points, industry comparisons, historical analogues |
| Internal consistency | Drivers contradict each other | Mostly consistent | All drivers reinforce the same story |
| Testability | Cannot be proven wrong | Partially testable | Clear milestones and metrics that confirm or refute |
| Alternatives acknowledged | Single narrative only | Bear/bull mentioned | Full alternative narratives with driver implications |

---

## Competitive Advantage Assessment

Competitive advantages determine the length of the high-growth period and the sustainability of above-market returns.

### Types of Competitive Advantage

| Advantage | Description | Durability | Examples |
|-----------|-------------|------------|----------|
| Brand | Customer recognition, loyalty, pricing power | Moderate to high (10-20 years) | Apple, Nike, Coca-Cola |
| Network effects | Value increases with user count | High (15-25 years if dominant) | Visa, Meta, Uber |
| Switching costs | Cost to customers of changing providers | Moderate to high (10-20 years) | SAP, Oracle, Bloomberg |
| Cost advantage | Structural cost leadership | Moderate (5-15 years; can be replicated) | Walmart, Costco, TSMC |
| Intellectual property | Patents, proprietary technology | Varies (patent life 15-20 years; trade secrets longer) | Pharmaceutical firms, Qualcomm |
| Regulatory barriers | Licenses, permits, legal protections | High while regulation persists | Utilities, banks, telecom |
| Scale economies | Cost advantages from size | Moderate (5-15 years) | Amazon logistics, Google infrastructure |

### Estimating the Competitive Advantage Period

The competitive advantage period (CAP) is the number of years during which the company earns returns above its cost of capital. It determines the length of the high-growth phase in the DCF.

**Framework for estimation**:

1. Identify the primary advantage (from the table above)
2. Assess its durability based on:
   - How difficult is it to replicate? (years and capital required)
   - Is the advantage strengthening or weakening? (network effects compound; patents expire)
   - What are the most credible competitive threats?
3. Set the CAP in years:
   - Weak/no advantage: 0-3 years
   - Moderate advantage: 5-10 years
   - Strong advantage: 10-15 years
   - Exceptional advantage (dominant network effects, regulatory protection): 15-25 years

---

## TAM Sizing Methodology

### Addressable vs. Obtainable

| Level | Definition | How to Estimate |
|-------|-----------|-----------------|
| TAM (Total Addressable Market) | Total revenue opportunity if the company had 100% share | Industry research, census data, global market reports |
| SAM (Serviceable Addressable Market) | Portion the company can realistically serve (geography, segment) | Filter TAM by geography, customer type, product fit |
| SOM (Serviceable Obtainable Market) | Portion the company can realistically capture | SAM x realistic market share (based on competition, execution) |

### Top-Down Methodology

1. Start with the broadest relevant market size (global industry revenue, total spending in category)
2. Apply filters to narrow to the addressable segment:
   - Geographic filter (which countries/regions can the company serve?)
   - Segment filter (which customer types are addressed?)
   - Product filter (what portion of the market does the product address?)
3. The result is TAM

**Common sources for market sizes**: Industry reports (Gartner, McKinsey, IBISWorld), government statistics, public company filings, trade associations.

### Bottom-Up Methodology

1. Count the number of potential customers or units
2. Estimate the revenue per customer per year (from pricing and usage data)
3. Multiply: TAM = potential customers x revenue per customer

**When bottom-up is better**: When the company is creating a new category (no industry report exists) or when granular customer data is available.

### Cross-Checking TAM Estimates

- Compare TAM to public company revenues in the space (TAM should be larger than the largest player's revenue)
- Compare to GDP or consumer spending in the category (TAM should not exceed total spending)
- Compare top-down and bottom-up estimates (within 3x is reasonable agreement)
- Check growth rate: if TAM is growing faster than GDP for extended periods, confirm the structural drivers

### TAM Pitfalls

- **TAM inflation**: Defining the market too broadly (e.g., "the global software market" when the product serves a niche)
- **Static TAM**: Assuming the market does not grow or shrink over the projection period
- **Ignoring substitutes**: Not accounting for adjacent products or services that compete for the same budget
- **100% share fantasy**: Assuming the company can capture more than 30-40% of a competitive market

---

## Industry Margin Benchmarks

Use these ranges as reference points for target operating margin. The company's narrative should explain where it will land within the industry range and why.

| Industry | Median Operating Margin | 75th Percentile | Notes |
|----------|----------------------|-----------------|-------|
| Software (SaaS) | 15-20% | 25-35% | High margins at scale; R&D is major cost |
| Semiconductors | 20-25% | 30-40% | Cyclical; design vs. fabrication matters |
| Pharmaceuticals | 20-25% | 30-40% | Patent-protected products drive high margins |
| Consumer electronics | 5-10% | 12-18% | Scale and brand matter; Apple is outlier |
| Auto manufacturing | 5-8% | 10-12% | Capital-intensive; Tesla targets top quartile |
| Retail (general) | 3-6% | 8-12% | Low margin, high volume; varies by format |
| Airlines | 5-10% | 12-15% | Cyclical; fuel and labor costs dominate |
| Banks / Financial services | 25-35% | 40-50% | Operating margin on net interest income |
| Telecom | 15-25% | 28-35% | Infrastructure-heavy; regulated |
| E-commerce | 2-5% | 8-15% | Low margin; logistics and fulfillment costs |

These are approximate ranges from Damodaran's industry datasets. Margins vary by geography, business model, and competitive position. Use the relevant peer set for the specific company.

---

## Common Narrative Failures

### Narrative Failure 1: The Disconnected Story

**Symptom**: The story sounds compelling but the numbers do not follow from it. Example: "Company X has amazing technology" but the revenue growth rate is set at 8% without explanation.

**Fix**: For each number in the value driver table, write one sentence explaining how it connects to the narrative. If you cannot write the sentence, the number is not linked.

### Narrative Failure 2: The Numbers-Only Valuation

**Symptom**: Historical financial data extrapolated forward without a story. Revenue grows at the trailing 3-year CAGR; margin stays at current level; no narrative for why.

**Fix**: Start with the story first. What will the company look like in 10 years? Then derive the numbers from that vision.

### Narrative Failure 3: The "Everything Goes Right" Story

**Symptom**: Only one narrative presented and it assumes optimal execution, no competitive response, and favorable market conditions.

**Fix**: Develop at least one alternative narrative (bear case or different strategic path). Identify what signals would cause you to shift from the primary to the alternative.

### Narrative Failure 4: The Impossible Narrative

**Symptom**: The implied numbers violate basic constraints. Market share exceeds 50%. Margins double the industry leader. Growth rate of 40% sustained for 20 years.

**Fix**: Apply the plausibility test. Check every driver against TAM, industry benchmarks, and historical precedent.

### Narrative Failure 5: The Stale Narrative

**Symptom**: The narrative was written once and never updated despite new evidence (earnings reports, competitive moves, industry shifts).

**Fix**: Treat the narrative as a living document. Revisit after every major piece of new information and assess whether the story still holds.

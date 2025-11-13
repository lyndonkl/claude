# Metrics Tree Methodology

**When to use this methodology:** You've used [template.md](template.md) and need advanced techniques for:
- Multi-sided marketplaces or platforms
- Complex metric interdependencies and feedback loops
- Counter-metrics and guardrail systems
- Network effects and viral growth
- Preventing metric gaming
- Seasonal adjustment and cohort aging effects
- Portfolio approach for different business stages

**If your metrics tree is straightforward:** Use [template.md](template.md) directly. This methodology is for complex metric systems.

---

## Table of Contents
1. [Multi-Sided Marketplace Metrics](#1-multi-sided-marketplace-metrics)
2. [Counter-Metrics & Guardrails](#2-counter-metrics--guardrails)
3. [Network Effects & Viral Loops](#3-network-effects--viral-loops)
4. [Preventing Metric Gaming](#4-preventing-metric-gaming)
5. [Advanced Leading Indicators](#5-advanced-leading-indicators)
6. [Metric Interdependencies](#6-metric-interdependencies)
7. [Business Stage Metrics](#7-business-stage-metrics)

---

## 1. Multi-Sided Marketplace Metrics

### Challenge
Marketplaces have supply-side and demand-side that must be balanced. Optimizing one side can hurt the other.

### Solution: Dual Tree Approach

**Step 1: Identify constraint**
- **Supply-constrained**: More demand than supply → Focus on supply-side metrics
- **Demand-constrained**: More supply than demand → Focus on demand-side metrics
- **Balanced**: Need both → Monitor ratio/balance metrics

**Step 2: Create separate trees**

**Supply-Side Tree:**
```
North Star: Active Suppliers (providing inventory)
├─ New supplier activation
├─ Retained suppliers (ongoing activity)
└─ Supplier quality/performance
```

**Demand-Side Tree:**
```
North Star: Successful Transactions
├─ New customer acquisition
├─ Repeat customer rate
└─ Customer satisfaction
```

**Step 3: Define balance metrics**
- **Liquidity ratio**: Supply utilization rate (% of inventory sold)
- **Match rate**: % of searches resulting in transaction
- **Wait time**: Time from demand signal to fulfillment

**Example (Uber):**
- Supply NS: Active drivers with >10 hours/week
- Demand NS: Completed rides
- Balance metric: Average wait time <5 minutes, driver utilization >60%

### Multi-Sided Decomposition Template

```
Marketplace GMV = (Supply × Utilization) × (Demand × Conversion) × Average Transaction

Where:
- Supply: Available inventory/capacity
- Utilization: % of supply that gets used
- Demand: Potential buyers/searches
- Conversion: % of demand that transacts
- Average Transaction: $ per transaction
```

---

## 2. Counter-Metrics & Guardrails

### Problem
Optimizing primary metrics can create negative externalities (quality drops, trust declines, user experience suffers).

### Solution: Balanced Scorecard with Guardrails

**Framework:**
1. **Primary metric** (North Star): What you're optimizing
2. **Counter-metrics**: What could be harmed
3. **Guardrail thresholds**: Minimum acceptable levels

**Example (Content Platform):**
```
Primary: Content Views (maximize)

Counter-metrics with guardrails:
- Content quality score: Must stay ≥7/10 (current: 7.8)
- User satisfaction (NPS): Must stay ≥40 (current: 52)
- Creator retention: Must stay ≥70% (current: 75%)
- Time to harmful content takedown: Must be ≤2 hours (current: 1.5h)

Rule: If any guardrail is breached, pause optimization of primary metric
```

### Common Counter-Metric Patterns

| Primary Metric | Potential Harm | Counter-Metric |
|----------------|----------------|----------------|
| Pageviews | Clickbait, low quality | Time on page, bounce rate |
| Engagement time | Addictive dark patterns | User-reported wellbeing, voluntary sessions |
| Viral growth | Spam | Unsubscribe rate, report rate |
| Conversion rate | Aggressive upsells | Customer satisfaction, refund rate |
| Speed to market | Technical debt | Bug rate, system reliability |

### How to Set Guardrails

1. **Historical baseline**: Look at metric over past 6-12 months, set floor at 10th percentile
2. **Competitive benchmark**: Set floor at industry average
3. **User feedback**: Survey users on acceptable minimum
4. **Regulatory**: Compliance thresholds

---

## 3. Network Effects & Viral Loops

### Measuring Network Effects

**Network effect**: Product value increases as more users join.

**Metrics to track:**
- **Network density**: Connections per user (higher = stronger network)
- **Cross-side interactions**: User A's action benefits User B
- **Viral coefficient (K)**: New users generated per existing user
  - K > 1: Exponential growth (viral)
  - K < 1: Sub-viral (need paid acquisition)

**Decomposition:**
```
New Users = Existing Users × Invitation Rate × Invitation Acceptance Rate

Example:
100,000 users × 2 invites/user × 50% accept = 100,000 new users (K=1.0)
```

### Viral Loop Metrics Tree

**North Star:** Viral Coefficient (K)

**Decomposition:**
```
K = (Invitations Sent / User) × (Acceptance Rate) × (Activation Rate)

Input metrics:
├─ Invitations per user
│  ├─ % users who send ≥1 invite
│  ├─ Average invites per sender
│  └─ Invitation prompts shown
├─ Invite acceptance rate
│  ├─ Invite message quality
│  ├─ Social proof (sender credibility)
│  └─ Landing page conversion
└─ New user activation rate
   ├─ Onboarding completion
   ├─ Value realization time
   └─ Early engagement actions
```

### Network Density Metrics

**Measure connectedness:**
- Average connections per user
- % of users with ≥N connections
- Clustering coefficient (friends-of-friends)
- Active daily/weekly connections

**Threshold effects:**
- Users with 7+ friends have 10x retention (identify critical mass)
- Teams with 10+ members have 5x engagement (team size threshold)

---

## 4. Preventing Metric Gaming

### Problem
Teams optimize for the letter of the metric, not the spirit, creating perverse incentives.

### Gaming Detection Framework

**Step 1: Anticipate gaming**
For each metric, ask: "How could someone game this?"

**Example metric: Time on site**
- Gaming: Auto-play videos, infinite scroll, fake engagement
- Intent: User finds value, willingly spends time

**Step 2: Add quality signals**
Distinguish genuine value from gaming:

```
Time on site (primary)
+ Quality signals (guards against gaming):
  - Active engagement (clicks, scrolls, interactions) vs passive
  - Return visits (indicates genuine interest)
  - Completion rate (finished content vs bounced)
  - User satisfaction rating
  - Organic shares (not prompted)
```

**Step 3: Test for gaming**
- Spot check: Sample user sessions, review for patterns
- Anomaly detection: Flag outliers (10x normal behavior)
- User feedback: "Was this session valuable to you?"

### Gaming Prevention Patterns

**Pattern 1: Combination metrics**
Don't measure single metric; require multiple signals:
```
❌ Single: Pageviews
✓ Combined: Pageviews + Time on page >30s + Low bounce rate
```

**Pattern 2: User-reported value**
Add subjective quality check:
```
Primary: Feature adoption rate
+ Counter: "Did this feature help you?" (must be >80% yes)
```

**Pattern 3: Long-term outcome binding**
Tie short-term to long-term:
```
Primary: New user signups
+ Bound to: 30-day retention (signups only count if user retained)
```

**Pattern 4: Peer comparison**
Normalize by cohort or segment:
```
Primary: Sales closed
+ Normalized: Sales closed / Sales qualified leads (prevents cherry-picking easy wins)
```

---

## 5. Advanced Leading Indicators

### Technique 1: Propensity Scoring

**Predict future behavior from early signals.**

**Method:**
1. Collect historical data: New users + their 30-day outcomes
2. Identify features: Day 1 behaviors (actions, time spent, features used)
3. Build model: Logistic regression or decision tree predicting 30-day retention
4. Score new users: Probability of retention based on day 1 behavior
5. Threshold: Users with >70% propensity score are "likely retained"

**Example (SaaS):**
```
30-day retention model (R² = 0.78):
Retention = 0.1 + 0.35×(invited teammate) + 0.25×(completed 3 workflows) + 0.20×(time in app >20min)

Leading indicator: % of users with propensity score >0.7
Current: 45% → Target: 60% (predicts 15% retention increase)
```

### Technique 2: Cohort Behavior Clustering

**Find archetypes that predict outcomes.**

**Method:**
1. Segment users by first-week behavior patterns
2. Measure long-term outcomes per segment
3. Identify high-value archetypes

**Example:**
```
Archetypes (first week):
- "Power user": 5+ days active, 20+ actions → 85% retain
- "Social": Invites 2+ people, comments 3+ times → 75% retain
- "Explorer": Views 10+ pages, low actions → 40% retain
- "Passive": <3 days active, <5 actions → 15% retain

Leading indicator: % of new users becoming "Power" or "Social" archetypes
Target: Move 30% → 45% into high-value archetypes
```

### Technique 3: Inflection Point Analysis

**Find tipping points where behavior changes sharply.**

**Method:**
1. Plot outcome (retention) vs candidate metric (actions taken)
2. Find where curve steepens (inflection point)
3. Set that as leading indicator threshold

**Example:**
```
Retention by messages sent (first week):
- 0-2 messages: 20% retention (slow growth)
- 3-9 messages: 45% retention (moderate growth)
- 10+ messages: 80% retention (sharp jump)

Inflection point: 10 messages
Leading indicator: % of users hitting 10+ messages in first week
```

---

## 6. Metric Interdependencies

### Problem
Metrics aren't independent; changing one affects others in complex ways.

### Solution: Causal Diagram

**Step 1: Map relationships**
Draw arrows showing how metrics affect each other:
```
[Acquisition] → [Active Users] → [Engagement] → [Retention]
     ↓                                              ↑
[Activation] ----------------------------------------
```

**Step 2: Identify feedback loops**
- **Positive loop** (reinforcing): A → B → A (exponential)
  Example: More users → more network value → more users
- **Negative loop** (balancing): A → B → ¬A (equilibrium)
  Example: More supply → lower prices → less supply

**Step 3: Predict second-order effects**
If you increase metric X by 10%:
- Direct effect: Y increases 5%
- Indirect effect: Y affects Z, which feeds back to X
- Net effect: May be amplified or dampened

**Example (Marketplace):**
```
Increase driver supply +10%:
  → Wait time decreases -15%
  → Rider satisfaction increases +8%
  → Rider demand increases +5%
  → Driver earnings decrease -3% (more competition)
  → Driver churn increases +2%
  → Net driver supply increase: +10% -2% = +8%
```

### Modeling Tradeoffs

**Technique: Regression or experiments**
```
Run A/B test increasing X
Measure all related metrics
Calculate elasticities:
  - If X increases 1%, Y changes by [elasticity]%
Build tradeoff matrix
```

**Tradeoff Matrix Example:**
| If increase by 10% | Acquisition | Activation | Retention | Revenue |
|--------------------|-------------|------------|-----------|---------|
| **Acquisition** | +10% | -2% | -1% | +6% |
| **Activation** | 0% | +10% | +5% | +12% |
| **Retention** | 0% | +3% | +10% | +15% |

**Interpretation:** Investing in retention has best ROI (15% revenue lift vs 6% from acquisition).

---

## 7. Business Stage Metrics

### Problem
Optimal metrics change as business matures. Early-stage metrics differ from growth or maturity stages.

### Stage-Specific North Stars

**Pre-Product/Market Fit (PMF):**
- **Focus**: Finding PMF, not scaling
- **North Star**: Retention (evidence of value)
- **Key metrics**:
  - Week 1 → Week 2 retention (>40% = promising)
  - NPS or "very disappointed" survey (>40% = good signal)
  - Organic usage frequency (weekly+ = habit-forming)

**Post-PMF, Pre-Scale:**
- **Focus**: Unit economics and growth
- **North Star**: New activated users per week (acquisition + activation)
- **Key metrics**:
  - LTV/CAC ratio (target >3:1)
  - Payback period (target <12 months)
  - Month-over-month growth rate (target >10%)

**Growth Stage:**
- **Focus**: Efficient scaling
- **North Star**: Revenue or gross profit
- **Key metrics**:
  - Net revenue retention (target >100%)
  - Magic number (ARR growth / S&M spend, target >0.75)
  - Burn multiple (cash burned / ARR added, target <1.5)

**Maturity Stage:**
- **Focus**: Profitability and market share
- **North Star**: Free cash flow or EBITDA
- **Key metrics**:
  - Operating margin (target >20%)
  - Market share / competitive position
  - Customer lifetime value

### Transition Triggers

**When to change North Star:**
```
PMF → Growth: When retention >40%, NPS >40, organic growth observed
Growth → Maturity: When growth rate <20% for 2+ quarters, market share >30%
```

**Migration approach:**
1. Track both old and new North Star for 2 quarters
2. Align teams on new metric
3. Deprecate old metric
4. Update dashboards and incentives

---

## Quick Decision Trees

### "Should I use counter-metrics?"

```
Is primary metric easy to game or has quality risk?
├─ YES → Add counter-metrics with guardrails
└─ NO → Is metric clearly aligned with user value?
    ├─ YES → Primary metric sufficient, monitor only
    └─ NO → Redesign metric to better capture value
```

### "Do I have network effects?"

```
Does value increase as more users join?
├─ YES → Track network density, K-factor, measure at different scales
└─ NO → Does one user's action benefit others?
    ├─ YES → Measure cross-user interactions, content creation/consumption
    └─ NO → Standard metrics tree (no network effects)
```

### "Should I segment my metrics tree?"

```
Do different user segments have different behavior patterns?
├─ YES → Do segments have different value to business?
    ├─ YES → Create separate trees per segment, track segment mix
    └─ NO → Single tree, annotate with segment breakdowns
└─ NO → Are there supply/demand sides?
    ├─ YES → Dual trees (Section 1)
    └─ NO → Single unified tree
```

---

## Summary: Advanced Technique Selector

| Scenario | Use This Technique | Section |
|----------|-------------------|---------|
| **Multi-sided marketplace** | Dual tree + balance metrics | 1 |
| **Risk of negative externalities** | Counter-metrics + guardrails | 2 |
| **Viral or network product** | K-factor + network density | 3 |
| **Metric gaming risk** | Quality signals + combination metrics | 4 |
| **Need better prediction** | Propensity scoring + archetypes | 5 |
| **Complex interdependencies** | Causal diagram + elasticities | 6 |
| **Changing business stage** | Stage-appropriate North Star | 7 |

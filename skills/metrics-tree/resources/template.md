# Metrics Tree Template

## How to Use This Template

Follow this structure to create a metrics tree for your product or business:

1. Start with North Star metric definition
2. Apply appropriate decomposition method
3. Map action metrics for each input
4. Identify leading indicators
5. Prioritize experiments using ICE framework
6. Output to `metrics-tree.md`

---

## Part 1: North Star Metric

### Define Your North Star

**North Star Metric:** [Name of metric]

**Definition:** [Precise definition including time window]
Example: "Number of unique users who complete at least one transaction per week"

**Rationale:** [Why this metric?]
- ✓ Captures value delivered to customers: [how]
- ✓ Reflects business model: [revenue connection]
- ✓ Measurable and trackable: [data source]
- ✓ Actionable by teams: [who can influence]

**Current Value:** [Number] as of [Date]

**Target:** [Goal] by [Date]

### North Star Selection Checklist

- [ ] **Customer value**: Does it measure value delivered to customers?
- [ ] **Business correlation**: Does it predict revenue/business success?
- [ ] **Actionable**: Can teams influence it through their work?
- [ ] **Measurable**: Do we have reliable data?
- [ ] **Not vanity**: Does it reflect actual usage/value, not just interest?
- [ ] **Time-bounded**: Does it have a clear time window (daily/weekly/monthly)?

---

## Part 2: Metric Decomposition

Choose the decomposition method that best fits your North Star:

### Method 1: Additive Decomposition

**Use when:** North Star is sum of independent segments

**Formula:**
```
North Star = Component A + Component B + Component C + ...
```

**Template:**
```
[North Star] =
  + [New users/customers]
  + [Retained users/customers]
  + [Resurrected users/customers]
  + [Other segment]
```

**Example (SaaS WAU):**
```
Weekly Active Users =
  + New activated users this week (30%)
  + Retained from previous week (60%)
  + Resurrected (inactive→active) (10%)
```

### Method 2: Multiplicative Decomposition

**Use when:** North Star is product of rates/factors

**Formula:**
```
North Star = Factor A × Factor B × Factor C × ...
```

**Template:**
```
[North Star] =
  [Total addressable users/visits]
  × [Conversion rate at step 1]
  × [Conversion rate at step 2]
  × [Value per conversion]
```

**Example (E-commerce Revenue):**
```
Monthly Revenue =
  Monthly site visitors
  × Purchase conversion rate (3%)
  × Average order value ($75)
```

### Method 3: Funnel Decomposition

**Use when:** North Star is end of sequential conversion process

**Formula:**
```
North Star = Top of funnel → Step 1 → Step 2 → ... → Final conversion
```

**Template:**
```
[North Star] =
  [Total entries]
  × [Step 1 conversion %]
  × [Step 2 conversion %]
  × [Final conversion %]
```

**Example (Paid SaaS Customers):**
```
New paid customers/month =
  Free signups
  × Activation rate (complete onboarding) (40%)
  × Trial start rate (25%)
  × Trial→Paid conversion rate (20%)

Math: 1000 signups × 0.4 × 0.25 × 0.2 = 20 paid customers
```

### Method 4: Cohort Decomposition

**Use when:** Retention is key driver, need to separate acquisition from retention

**Formula:**
```
North Star = Σ (Cohort Size_t × Retention Rate_t,n) for all cohorts
```

**Template:**
```
[North Star today] =
  [Users from Month 0] × [Month 0 retention rate]
  + [Users from Month 1] × [Month 1 retention rate]
  + ...
  + [Users from Month N] × [Month N retention rate]
```

**Example (Subscription Service MAU):**
```
March Active Users =
  Jan signups (500) × Month 2 retention (50%) = 250
  + Feb signups (600) × Month 1 retention (70%) = 420
  + Mar signups (700) × Month 0 retention (100%) = 700
  = 1,370 MAU
```

---

## Part 3: Input Metrics (L2)

For each component in your decomposition, define as input metric:

### Input Metric Template

**Input Metric 1:** [Name]
- **Definition:** [Precise definition]
- **Current value:** [Number]
- **Target:** [Goal]
- **Owner:** [Team/person]
- **Relationship to North Star:** [How it affects NS, with estimated coefficient]
  Example: "Increasing activation rate by 10% → 5% increase in WAU"

**Input Metric 2:** [Name]
[Repeat for 3-5 input metrics]

### Validation Questions

- [ ] Are all input metrics **mutually exclusive**? (No double-counting)
- [ ] Do they **collectively exhaust** the North Star? (Nothing missing)
- [ ] Can each be **owned by a single team**?
- [ ] Is each **measurable** with existing/planned instrumentation?
- [ ] Are they all **at same level of abstraction**?

---

## Part 4: Action Metrics (L3)

For each input metric, identify specific user behaviors that drive it:

### Action Metrics Template

**For Input Metric: [Name of L2 metric]**

**Action 1:** [Specific user behavior]
- **Measurement:** [How to track it]
- **Frequency:** [How often it happens]
- **Impact:** [Estimated effect on input metric]
- **Current rate:** [% of users doing this]

**Action 2:** [Another behavior]
[Repeat for 3-5 actions per input]

**Example (For input metric "Retained Users"):**

**Action 1:** User completes core workflow
- Measurement: Track "workflow_completed" event
- Frequency: 5x per week average for active users
- Impact: Users with 3+ completions have 80% retention vs 20% baseline
- Current rate: 45% of users complete workflow at least once

**Action 2:** User invites teammate
- Measurement: "invite_sent" event with "invite_accepted" event
- Frequency: 1.2 invites per user on average
- Impact: Users who invite have 90% retention vs 40% baseline
- Current rate: 20% of users send at least one invite

---

## Part 5: Leading Indicators

Identify early signals that predict North Star movement:

### Leading Indicator Template

**Leading Indicator 1:** [Metric name]
- **Definition:** [What it measures]
- **Timing:** [How far in advance it predicts] Example: "Predicts week 4 retention"
- **Correlation:** [Strength of relationship] Example: "r=0.75 with 30-day retention"
- **Actionability:** [How teams can move it]
- **Current value:** [Number]

**Example:**

**Leading Indicator: Day 1 Activation Rate**
- Definition: % of new users who complete 3 key actions on first day
- Timing: Predicts 7-day and 30-day retention (measured day 1, predicts weeks ahead)
- Correlation: r=0.82 with 30-day retention. Users with Day 1 activation have 70% retention vs 15% without
- Actionability: Improve onboarding flow, reduce time-to-value, send activation nudges
- Current value: 35%

### How to Find Leading Indicators

**Method 1: Cohort analysis**
- Segment users by early behavior (first day, first week)
- Measure long-term outcomes (retention, LTV)
- Find behaviors that predict positive outcomes

**Method 2: Correlation analysis**
- List all early-funnel metrics
- Calculate correlation with North Star or key inputs
- Select metrics with r > 0.6 and actionable

**Method 3: High-performer analysis**
- Identify users in top 20% for North Star metric
- Look at their first week/month behavior
- Find patterns that distinguish them from average users

---

## Part 6: Experiment Prioritization

Use ICE framework to prioritize which metrics to improve:

### ICE Scoring Template

**Impact (1-10):** How much will improving this metric affect North Star?
- 10 = Direct, large effect (e.g., 10% improvement → 8% NS increase)
- 5 = Moderate effect (e.g., 10% improvement → 3% NS increase)
- 1 = Small effect (e.g., 10% improvement → 0.5% NS increase)

**Confidence (1-10):** How certain are we about the relationship?
- 10 = Proven causal relationship with data
- 5 = Correlated, plausible causation
- 1 = Hypothesis, no data yet

**Ease (1-10):** How easy is it to move this metric?
- 10 = Simple change, 1-2 weeks
- 5 = Moderate effort, 1-2 months
- 1 = Major project, 6+ months

**ICE Score = (Impact + Confidence + Ease) / 3**

### Prioritization Table

| Metric/Experiment | Impact | Confidence | Ease | ICE Score | Rank |
|-------------------|--------|------------|------|-----------|------|
| [Experiment 1] | [1-10] | [1-10] | [1-10] | [Avg] | [#] |
| [Experiment 2] | [1-10] | [1-10] | [1-10] | [Avg] | [#] |
| [Experiment 3] | [1-10] | [1-10] | [1-10] | [Avg] | [#] |

### Top 3 Experiments

**Experiment 1:** [Name - highest ICE score]
- **Hypothesis:** [What we believe will happen]
- **Metric to move:** [Target metric]
- **Expected impact:** [Quantified prediction]
- **Timeline:** [Duration]
- **Success criteria:** [How we'll know it worked]

**Experiment 2:** [Second highest]
[Repeat structure]

**Experiment 3:** [Third highest]
[Repeat structure]

---

## Part 7: Metric Relationships Diagram

Create visual representation of your metrics tree:

### ASCII Tree Format

```
North Star: [Metric Name] = [Current Value]
│
├─ Input Metric 1: [Name] = [Value]
│  ├─ Action 1.1: [Behavior] = [Rate]
│  ├─ Action 1.2: [Behavior] = [Rate]
│  └─ Action 1.3: [Behavior] = [Rate]
│
├─ Input Metric 2: [Name] = [Value]
│  ├─ Action 2.1: [Behavior] = [Rate]
│  ├─ Action 2.2: [Behavior] = [Rate]
│  └─ Action 2.3: [Behavior] = [Rate]
│
└─ Input Metric 3: [Name] = [Value]
   ├─ Action 3.1: [Behavior] = [Rate]
   ├─ Action 3.2: [Behavior] = [Rate]
   └─ Action 3.3: [Behavior] = [Rate]

Leading Indicators:
→ [Indicator 1]: Predicts [what] by [timing]
→ [Indicator 2]: Predicts [what] by [timing]
```

### Example (Complete Tree)

```
North Star: Weekly Active Users = 10,000
│
├─ New Activated Users = 3,000/week (30%)
│  ├─ Complete onboarding: 40% of signups
│  ├─ Connect data source: 25% of signups
│  └─ Invite teammate: 20% of signups
│
├─ Retained Users = 6,000/week (60%)
│  ├─ Use core feature 3+ times: 45% of users
│  ├─ Create content: 30% of users
│  └─ Engage with team: 25% of users
│
└─ Resurrected Users = 1,000/week (10%)
   ├─ Receive reactivation email: 50% open rate
   ├─ See new feature announcement: 30% click rate
   └─ Get @mentioned by teammate: 40% return rate

Leading Indicators:
→ Day 1 activation rate (35%): Predicts 30-day retention
→ 3 key actions in first session (22%): Predicts weekly usage
```

---

## Output Format

Create `metrics-tree.md` with this structure:

```markdown
# Metrics Tree: [Product/Business Name]

**Date:** [YYYY-MM-DD]
**Owner:** [Team/Person]
**Review Frequency:** [Weekly/Monthly]

## North Star Metric

**Metric:** [Name]
**Current:** [Value] as of [Date]
**Target:** [Goal] by [Date]
**Rationale:** [Why this metric]

## Decomposition Method

[Additive/Multiplicative/Funnel/Cohort]

**Formula:**
[Mathematical relationship]

## Input Metrics (L2)

### 1. [Input Metric Name]
- **Current:** [Value]
- **Target:** [Goal]
- **Owner:** [Team]
- **Impact:** [Effect on NS]

#### Actions (L3):
1. [Action 1]: [Current rate]
2. [Action 2]: [Current rate]
3. [Action 3]: [Current rate]

[Repeat for all input metrics]

## Leading Indicators

1. **[Indicator 1]:** [Definition]
   - Timing: [When it predicts]
   - Correlation: [Strength]
   - Current: [Value]

2. **[Indicator 2]:** [Definition]
   [Repeat structure]

## Prioritized Experiments

### Experiment 1: [Name] (ICE: [Score])
- **Hypothesis:** [What we believe]
- **Metric:** [Target]
- **Expected Impact:** [Quantified]
- **Timeline:** [Duration]
- **Success Criteria:** [Threshold]

[Repeat for top 3 experiments]

## Metrics Tree Diagram

[Include ASCII or visual diagram]

## Notes

- [Assumptions made]
- [Data gaps or limitations]
- [Next review date]
```

---

## Quick Examples by Business Model

### SaaS Example (Slack-style)

**North Star:** Teams sending 100+ messages per week

**Decomposition (Additive):**
```
Active Teams = New Active Teams + Retained Active Teams + Resurrected Teams
```

**Input Metrics:**
- New active teams: Complete onboarding + hit 100 messages in week 1
- Retained active teams: Hit 100 messages this week and last week
- Resurrected teams: Hit 100 messages this week but not last 4 weeks

**Leading Indicators:**
- 10 members invited in first day (predicts team activation)
- 50 messages sent in first week (predicts long-term retention)

### E-commerce Example

**North Star:** Monthly Revenue

**Decomposition (Multiplicative):**
```
Revenue = Visitors × Purchase Rate × Average Order Value
```

**Input Metrics:**
- Monthly unique visitors (owned by Marketing)
- Purchase conversion rate (owned by Product)
- Average order value (owned by Merchandising)

**Leading Indicators:**
- Add-to-cart rate (predicts purchase)
- Product page views per session (predicts purchase intent)

### Marketplace Example (Airbnb-style)

**North Star:** Nights Booked

**Decomposition (Multi-sided):**
```
Nights Booked = (Active Listings × Availability Rate) × (Searches × Booking Rate)
```

**Input Metrics:**
- Active host supply: Listings with ≥1 available night
- Guest demand: Unique searches
- Match rate: Searches resulting in booking

**Leading Indicators:**
- Host completes first listing (predicts long-term hosting)
- Guest saves listings (predicts future booking)

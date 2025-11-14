# Project Risk Management: Advanced Methodologies

## Table of Contents
1. [Quantitative Risk Analysis](#1-quantitative-risk-analysis)
2. [Risk Aggregation and Portfolio View](#2-risk-aggregation-and-portfolio-view)
3. [Advanced Probability Estimation](#3-advanced-probability-estimation)
4. [Decision Trees and Sequential Risks](#4-decision-trees-and-sequential-risks)
5. [Earned Value Management for Risk](#5-earned-value-management-for-risk)
6. [Organizational Risk Maturity](#6-organizational-risk-maturity)

---

## 1. Quantitative Risk Analysis

### Monte Carlo Simulation

**When to use**: Estimate project timeline/budget uncertainty by simulating thousands of scenarios

**Process**:
1. For each task, estimate optimistic/most likely/pessimistic duration (PERT: (O + 4M + P) / 6)
2. Define probability distributions (triangular, normal, log-normal)
3. Run 10,000+ simulations randomizing task durations
4. Analyze outcomes: P50 (50% confidence), P80 (80% confidence), P95 (95% confidence)

**Example - 3-month project with uncertainty**:
- Deterministic estimate (ignoring risk): 90 days
- P50 (median, 50% confidence): 95 days (5 days buffer)
- P80 (80% confidence): 110 days (20 days buffer)
- P95 (95% confidence): 125 days (35 days buffer)

**Interpretation**: If you commit to 90-day deadline, 50% chance of missing it. For 80% confidence, need 20-day buffer.

**Tools**: @RISK (Excel add-in), Crystal Ball, Python (numpy.random), R

### Three-Point Estimation (PERT)

**Formula**: Expected Duration = (Optimistic + 4×Most Likely + Pessimistic) / 6

**Example**:
- Task: Database migration
- Optimistic (best case, 10% prob): 3 days
- Most Likely (50% prob): 7 days
- Pessimistic (worst case, 10% prob): 15 days
- **PERT Estimate**: (3 + 4×7 + 15) / 6 = **8 days**
- **Standard Deviation**: (15 - 3) / 6 = **2 days**
- **80% Confidence Interval**: 8 ± 1.28×2 = **5.4 to 10.6 days**

**Advantages**: Accounts for uncertainty, easy to elicit from experts
**Disadvantages**: Assumes symmetric distribution (not always true)

### Sensitivity Analysis

**Purpose**: Identify which risks have biggest impact on outcomes (tornado diagram)

**Process**:
1. Baseline scenario: Most likely value for all variables
2. Vary each variable one at a time from low to high
3. Measure impact on outcome (e.g., total project cost)
4. Rank variables by impact range (tornado shape)

**Example - Project cost sensitivity**:
| Variable | Low | High | Impact Range |
|----------|-----|------|--------------|
| Labor rate | -$50K | +$80K | **$130K** (biggest impact) |
| Equipment cost | -$30K | +$40K | **$70K** |
| Timeline delay | -$10K | +$25K | **$35K** (smallest impact) |

**Insight**: Focus mitigation on labor rate (biggest leverage), less on timeline

---

## 2. Risk Aggregation and Portfolio View

### Risk Correlation

**Problem**: Independent risks: P(both occur) = P(A) × P(B). Correlated risks: much higher.

**Example**:
- Risk A: Vendor 1 delays (Prob=30%)
- Risk B: Vendor 2 delays (Prob=30%)
- **If independent**: P(both delay) = 0.3 × 0.3 = **9%**
- **If correlated** (same root cause - chip shortage): P(both delay) = **25%+**

**Mitigation**: Identify correlated risks (shared root causes: economy, weather, supply chain), don't assume independence

### Expected Monetary Value (EMV)

**Formula**: EMV = Σ (Probability × Impact) for all risks

**Example - 3 risks**:
| Risk | Prob | Impact | EMV |
|------|------|--------|-----|
| Vendor delay | 40% | -$100K | **-$40K** |
| Quality issue | 20% | -$50K | **-$10K** |
| Early completion (opportunity) | 30% | +$30K | **+$9K** |
| **Total EMV** | | | **-$41K** |

**Interpretation**: Expected value of risk exposure is -$41K. Budget $50K contingency reserve (EMV + buffer).

**Use case**: Prioritize mitigation by EMV (biggest expected loss first), size contingency reserves

### Risk Burn-Down Chart

**Purpose**: Track risk evolution over project lifecycle (like sprint burn-down)

**Metrics**:
- Total risk exposure (sum of all risk scores or EMV)
- Number of open risks by priority (Critical/High/Medium/Low)
- Risk velocity (new risks - closed risks per week)

**Healthy pattern**:
- Risk exposure decreases over time (mitigation working)
- Critical/High risks trend to zero (resolved or mitigated to Medium/Low)
- Risk velocity neutral or negative (closing faster than opening)

**Red flag pattern**:
- Risk exposure increasing (mitigation not working, new issues emerging)
- Critical/High risks increasing (problems escalating)
- Risk velocity positive (opening faster than closing → overwhelmed)

---

## 3. Advanced Probability Estimation

### Base Rate Neglect (Avoid Overconfidence)

**Problem**: People ignore historical frequencies, overestimate unique circumstances

**Example**:
- Question: "What's probability our migration succeeds on time?"
- Naive answer: "We're confident, 90%" (overconfident, ignores history)
- **Base rate check**: "What % of similar migrations succeed on time historically?"
  - Industry data: 40% of migrations hit deadline
  - Our company: 3 of last 5 migrations were late (60% late)
- **Adjusted estimate**: Start with 40-60%, adjust up/down based on specific factors

**Process**:
1. Find reference class (similar past projects)
2. Calculate base rate (how often did X happen?)
3. Adjust for unique factors (better team? More complexity?)
4. Avoid overweighting unique factors (regression to mean)

### Calibration Training

**Goal**: Improve probability estimates by testing against reality

**Exercise**:
1. Make 20 predictions with confidence intervals (e.g., "Project will take 30-50 days, 80% confident")
2. Track outcomes (how many fell within your interval?)
3. **Well-calibrated**: If you say 80%, 16 of 20 (80%) should fall within interval
4. **Overconfident**: If only 10 of 20 (50%) fall within interval, you're underestimating uncertainty

**Debiasing**:
- If overconfident: Widen intervals, add more uncertainty
- If underconfident: Narrow intervals, trust your judgment more
- Repeat calibration exercises quarterly to maintain skills

### Decomposition for Probability

**Problem**: Hard to estimate "What's probability of successful launch?"
**Solution**: Break into sub-components with clearer probabilities

**Example**:
- P(successful launch) = P(tech ready) × P(market demand) × P(no competitor) × P(ops ready)
- P(tech ready) = 80% (prototype works, 2 minor bugs)
- P(market demand) = 60% (50 customer interviews, 60% said "definitely buy")
- P(no competitor launch first) = 70% (intel says competitor 6 months behind)
- P(ops ready) = 90% (simple deployment, done 10× before)
- **P(successful launch)** = 0.8 × 0.6 × 0.7 × 0.9 = **30%**

**Insight**: Overall probability much lower than intuition. Focus mitigation on market demand (weakest link).

---

## 4. Decision Trees and Sequential Risks

### When Risks Have Dependencies

**Example - Sequential decisions**:
```
                        ┌─ Prototype succeeds (60%) ─> Build (cost: $200K) ─┐
Start ($50K) ─> Prototype                                                    ├─> Success ($1M value)
                        └─ Prototype fails (40%) ─> Stop (cost: $50K)       ┘
```

**Expected Value**:
- EV(Prototype) = 0.6 × ($1M - $200K - $50K) + 0.4 × (-$50K) = **$430K**
- Decision: Prototype (EV = $430K) vs Don't Start (EV = $0) → **Prototype wins**

**Fold-back method**:
1. Start at end nodes (outcomes)
2. Work backwards, calculating EV at each decision node
3. Choose branch with highest EV at each decision

**Value of information**:
- If perfect test costs $20K and resolves prototype uncertainty → EV = $1M - $200K - $20K = $780K
- Value of info = $780K - $430K = **$350K** → worth paying up to $350K for perfect info

---

## 5. Earned Value Management for Risk

### Integrating Risks into EVM

**Standard EVM**:
- Planned Value (PV): Budget for work scheduled
- Earned Value (EV): Budget for work completed
- Actual Cost (AC): Actual spend
- Schedule Variance (SV) = EV - PV (negative = behind schedule)
- Cost Variance (CV) = EV - AC (negative = over budget)

**Risk-Adjusted EVM**:
- **Budget At Completion (BAC)**: $500K baseline
- **Risk Reserve**: $50K (from EMV calculation)
- **Total Budget**: $550K (BAC + Reserve)
- **Risk Burn Rate**: How fast are risks being retired vs reserve consumed?

**Metrics**:
- **Risk-Adjusted EAC** (Estimate At Completion): BAC + Remaining Risk EMV + Cost Overruns
- **Contingency Draw-Down**: % of risk reserve consumed vs % of project complete
  - Healthy: 30% reserve used, 40% project complete (consuming slower than progress)
  - Unhealthy: 60% reserve used, 30% project complete (consuming faster → may exhaust reserve)

---

## 6. Organizational Risk Maturity

### Risk Maturity Levels

**Level 1 - Ad Hoc**: No structured risk management, reactive only
- Indicators: Risks discovered after they occur, no register, fire-fighting culture
- Impact: High surprise rate, frequent crises, low stakeholder confidence

**Level 2 - Initial**: Basic risk register exists, sporadic updates
- Indicators: Kickoff risk workshop, register created but rarely reviewed, no mitigation tracking
- Impact: Some visibility, but stale data leads to false confidence

**Level 3 - Managed**: Regular risk reviews, mitigation tracked, integrated into planning
- Indicators: Weekly/monthly reviews, risk owners accountable, mitigation in project plan
- Impact: Fewer surprises, proactive culture, stakeholder confidence improving

**Level 4 - Measured**: Quantitative risk analysis, historical data tracked, continuous improvement
- Indicators: Monte Carlo simulation, calibration against actuals, lessons learned database
- Impact: Accurate forecasting, data-driven decisions, high stakeholder confidence

**Level 5 - Optimizing**: Risk management embedded in culture, predictive analytics, portfolio optimization
- Indicators: Cross-project risk aggregation, predictive models, automated monitoring
- Impact: Strategic advantage from risk management, industry-leading performance

### Building Risk Culture

**Key behaviors**:
- **Blameless**: Focus on system fixes, not individual fault (see postmortem skill)
- **Proactive**: Reward early risk identification, not just mitigation
- **Transparent**: Make risks visible (dashboards, reviews), don't hide bad news
- **Data-driven**: Track actual vs estimated probability/impact, improve calibration
- **Integrated**: Risk discussions in every planning meeting, not separate silo

**Anti-patterns**:
- ❌ Shoot the messenger (punishing bad news → risks hidden until crisis)
- ❌ Risk theater (create register for compliance, never use it)
- ❌ Optimism bias (always underestimate risks, "this time is different")
- ❌ Analysis paralysis (spend months on risk analysis, never mitigate)
- ❌ Siloed risks (project risks tracked separately from portfolio/strategic)

### Lessons Learned Database

**Structure**:
- Risk: [Description of risk that materialized]
- Project: [Which project]
- Impact: [Actual impact realized]
- Root Cause: [Why occurred despite mitigation]
- What Worked: [Effective mitigations/contingencies]
- What Didn't: [Ineffective actions]
- Recommendation: [How to handle in future]

**Usage**:
- Reference during risk identification (what risks hit similar projects?)
- Calibrate probability estimates (how often does X actually happen?)
- Improve mitigation effectiveness (what worked last time?)
- Onboard new PMs (learn from history without repeating mistakes)

**Metrics**:
- **Risk reoccurrence rate**: Are same risks hitting multiple projects? (need systemic fix)
- **Mitigation effectiveness**: % of mitigated risks that still occurred (need better techniques)
- **Surprise rate**: % of project issues NOT in risk register (need better identification)
- **Forecast accuracy**: Actual vs estimated P/I for materialized risks (calibration quality)

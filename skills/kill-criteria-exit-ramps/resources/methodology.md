# Kill Criteria & Exit Ramps: Methodology

Advanced techniques for setting kill criteria, avoiding behavioral biases, managing portfolios, and building organizational culture around disciplined stopping.

---

## 1. Sunk Cost Psychology and Behavioral Economics

### Understanding Sunk Cost Fallacy

**Definition**: Tendency to continue project based on past investment rather than future value

**Cognitive mechanisms**:
- **Loss aversion**: Losses feel 2× more painful than equivalent gains (Kahneman & Tversky)
- **Escalation of commitment**: Justifying past decisions by doubling down
- **Status quo bias**: Preference for current state over change
- **Endowment effect**: Overvaluing what we already own/built

**Common rationalizations**:
- "We've invested $2M, can't quit now" (ignoring opportunity cost)
- "Just need a little more time" (moving goalposts)
- "Too close to finishing to stop" (completion bias)
- "Team morale will suffer if we quit" (social pressure)

### Behavioral Interventions

**Pre-commitment devices**:
1. **Signed kill criteria document** before launch (removes discretion)
2. **Third-party decision maker** without sunk cost attachment
3. **Time-locked gates** with automatic NO-GO if criteria not met
4. **Financial caps** ("Will not invest more than $X total")

**Framing techniques**:
1. **Pre-mortem inversion**: "If starting today with $0, would we do this?"
2. **Opportunity cost framing**: "What else could these resources achieve?"
3. **Reverse trial**: "To CONTINUE, we need to prove X" (default = kill)
4. **Outside view**: "What would we advise another company to do?"

**Example**: Company spent $5M on enterprise sales, 3 customers in 2 years (need 50 for viability)
- **Sunk cost framing**: "We've invested $5M, can't stop now"
- **Opportunity cost framing**: "Next $5M could yield 200 SMB customers based on pilot data"
- **Pre-mortem inversion**: "If starting today, would we choose enterprise over SMB?" → No
- **Decision**: Kill enterprise sales, reallocate to SMB

### Quantifying Opportunity Cost

**Formula**: Opportunity Cost = Value of Best Alternative − Value of Current Project

**Process**:
1. Identify top 3 alternatives for resources (team, budget)
2. Estimate expected value for each: EV = Σ (Probability × Payoff)
3. Rank by EV / Resource Cost ratio
4. If current project ranks below alternatives → Kill signal

**Example**: SaaS with 3 options
- **Current project** (mobile app): EV = $2M, Cost = 5 engineers × 6 months = 30 eng-months, Ratio = $67k/eng-month
- **Alternative 1** (API platform): EV = $8M, Cost = 30 eng-months, Ratio = $267k/eng-month
- **Alternative 2** (integrations): EV = $5M, Cost = 20 eng-months, Ratio = $250k/eng-month
- **Decision**: Kill mobile app (lowest ratio), reallocate to API platform (highest ratio)

---

## 2. Portfolio Management Frameworks

### Portfolio Ranking Methodologies

**Method 1: Expected Value / Resource Cost**

Formula: `Rank Score = (Revenue × Probability of Success) / (Engineer-Months × Avg Cost)`

**Steps**:
1. Estimate revenue potential for each project (pessimistic, baseline, optimistic)
2. Assign probability of success (use reference class forecasting for calibration)
3. Calculate expected value: EV = Σ (Probability × Revenue)
4. Estimate resource cost (engineer-months, budget, opportunity cost)
5. Rank by EV/Cost ratio
6. Define kill threshold (e.g., bottom 30% of portfolio)

**Method 2: Weighted Scoring Model**

Formula: `Score = Σ (Weight_i × Rating_i)`

**Dimensions** (weights sum to 100%):
- Strategic fit (30%): Alignment with company vision
- Revenue potential (25%): Market size × conversion × pricing
- Probability of success (20%): Team capability, market readiness, technical risk
- Resource efficiency (15%): ROI, payback period, opportunity cost
- Competitive urgency (10%): Time-to-market importance

**Ratings**: 1-5 scale for each dimension

**Example**:
- **Project A**: Strategic fit (4), Revenue (5), Probability (3), Efficiency (4), Urgency (5) → Score = 0.30×4 + 0.25×5 + 0.20×3 + 0.15×4 + 0.10×5 = 4.05
- **Project B**: Strategic fit (3), Revenue (3), Probability (4), Efficiency (2), Urgency (2) → Score = 0.30×3 + 0.25×3 + 0.20×4 + 0.15×2 + 0.10×2 = 3.05
- **Ranking**: A > B

**Method 3: Real Options Analysis**

Treat projects as options (right but not obligation to continue)

**Value of option**:
- **Upside**: High if market/tech uncertainty resolves favorably
- **Downside**: Limited to incremental investment at each gate
- **Flexibility value**: Ability to pivot, expand, or abandon based on new info

**Decision rule**: Continue if `Option Value > Immediate Kill Value`

**Example**: R&D project with 3 gates
- Gate 1 ($50k): Learn if technology feasible (60% chance) → Continue if yes
- Gate 2 ($200k): Learn if market demand exists (40% chance) → Continue if yes
- Gate 3 ($1M): Full launch if both tech + market validated
- **Option value**: Flexibility to kill early if tech/market fails (limits downside)
- **Immediate kill value**: $0 but foregoes learning

**Decision**: Continue through gates (option value > kill value)

### Portfolio Rebalancing Cadence

**Quarterly portfolio review**:
1. Re-rank all projects using latest data
2. Identify projects below threshold (bottom 20-30%)
3. Evaluate kill vs. pivot for bottom performers
4. Reallocate resources from killed projects to top performers
5. Document decisions and communicate transparently

**Trigger-based review** (between quarterly reviews):
- Major market change (competitor launch, regulation, economic shift)
- Significant underperformance vs. projections (>30% variance)
- Resource constraints (hiring freeze, budget cut, key person departure)
- Strategic pivot (new company direction)

---

## 3. Decision Rights Frameworks

### RACI Matrix for Kill Decisions

**Roles**:
- **Responsible (R)**: Gathers data, monitors metrics, presents to decision-maker
- **Accountable (A)**: Makes final kill decision (single person, not committee)
- **Consulted (C)**: Provides input before decision (team, stakeholders)
- **Informed (I)**: Notified after decision (broader org, customers)

**Example**:
- **Kill Criteria Met → Kill Decision**:
  - Responsible: Product Manager (gathers data)
  - Accountable: Product VP (makes decision)
  - Consulted: Engineering Lead, Finance, CEO (input)
  - Informed: Team, customers, company (notification)

**Anti-pattern**: "Team decides" (everyone has sunk cost, leads to paralysis)

### Escalation Paths

**Standard path**:
1. **Metrics tracked** → Alert if approaching kill threshold
2. **Project owner evaluates** → Presents data + recommendation to decision authority
3. **Decision authority decides** → GO, NO-GO, or PIVOT
4. **Execute decision** → If kill, wind down within 1 month

**Override path** (use sparingly):
- **Override condition**: Decision authority wants to continue despite kill criteria met
- **Override process**: Written justification, senior approval (e.g., CEO), new kill criteria with shorter timeline
- **Override limit**: Max 1 override per project (prevents repeated goal-post moving)

**Example**: Product VP wants to override kill criteria for feature with 8% adoption (threshold: 10%)
- **Justification**: "Enterprise pilot starting next month, expect 15% adoption within 60 days"
- **New criteria**: "If <12% adoption after 60 days, kill immediately (no further overrides)"
- **CEO approval**: Required for override

### Governance Mechanisms

**Pre-launch approval**:
- Kill criteria document signed by project owner, decision authority, executive sponsor
- Changes to criteria require re-approval by all signatories

**Monitoring dashboard**:
- Real-time metrics vs. kill thresholds
- Traffic light system: Green (>20% above threshold), Yellow (within 20%), Red (below threshold)
- Automated alerts when entering Yellow or Red zones

**Postmortem requirement**:
- All killed projects require postmortem within 2 weeks
- Focus: learning, not blame
- Shared with broader org to normalize killing projects

---

## 4. Postmortem Processes and Learning Culture

### Postmortem Structure

**Timing**: Within 2 weeks of kill decision (while context fresh)

**Participants**: Project team + key stakeholders (5-10 people)

**Facilitator**: Neutral person (not project owner, avoids defensiveness)

**Duration**: 60-90 minutes

**Agenda**:
1. **Project recap** (5 min): Goals, kill criteria, timeline, outcome
2. **What went well?** (15 min): Successes, positive learnings
3. **What went wrong?** (20 min): Root causes of failure (not blame)
4. **What did we learn?** (20 min): Insights, surprises, assumptions invalidated
5. **What would we do differently?** (15 min): Specific changes for future projects
6. **Action items** (10 min): How to apply learnings (process changes, skill gaps, hiring needs)

**Output**: Written doc (2-3 pages) shared with broader team

### Blameless Postmortem Techniques

**Goal**: Learn from failure without blame culture

**Techniques**:
1. **Focus on systems, not individuals**: "Why did our process allow this?" not "Who screwed up?"
2. **Assume good intent**: Team made best decisions with info available at the time
3. **Prime Directive**: "Everyone did the best job they could, given what they knew, their skills, the resources available, and the situation at hand"
4. **"How might we" framing**: Forward-looking, solutions-focused

**Red flags** (blame culture):
- Finger-pointing ("PM should have known...")
- Defensiveness ("It wasn't my fault...")
- Punishment mindset ("Someone should be held accountable...")
- Learning avoidance ("Let's just move on...")

**Example**:
- **Blame framing**: "Why didn't PM validate market demand before building?"
- **Blameless framing**: "How might we improve our discovery process to validate demand earlier with less investment?"

### Normalizing Killing Projects

**Cultural shift**: Killing projects = good (disciplined capital allocation), not bad (failure)

**Messaging**:
- **Positive framing**: "We killed 3 projects this quarter, freeing resources for winners"
- **Celebrate discipline**: Acknowledge teams for recognizing kill criteria and executing quickly
- **Success metrics**: % of portfolio actively managed (killed or pivoted) each quarter (target: 20-30%)

**Leadership behaviors**:
- CEO/VPs publicly discuss projects they killed and why
- Reward PMs who kill projects early (before major resource drain)
- Promote "disciplined stopping" as core competency in performance reviews

**Anti-patterns**:
- Hiding killed projects (creates stigma)
- Only discussing successes (survivorship bias)
- Punishing teams for "failed" projects (discourages risk-taking)

---

## 5. Advanced Topics

### Real Options Theory

**Concept**: Treat uncertain projects as financial options

**Option types**:
1. **Option to defer**: Delay investment until uncertainty resolves
2. **Option to expand**: Scale up if initial results positive
3. **Option to contract**: Scale down if results negative
4. **Option to abandon**: Kill if results very negative
5. **Option to switch**: Pivot to alternative use

**Valuation**: Black-Scholes model adapted for projects
- **Underlying asset**: NPV of project
- **Strike price**: Investment required
- **Volatility**: Uncertainty in outcomes
- **Time to expiration**: Decision window

**Application**: Continue projects with high option value (high upside, limited downside, flexibility)

### Stage-Gate Process Design

**Optimal gate structure**:
- **3-5 gates** for major initiatives
- **Investment increases** by 3-5× at each gate (e.g., $10k → $50k → $200k → $1M)
- **Success criteria tighten** at each gate (higher bar as investment grows)

**Gate design**:
- **Gate 0 (Concept)**: $0-10k, 1-2 weeks, validate problem exists
- **Gate 1 (Discovery)**: $10-50k, 4-8 weeks, validate solution direction
- **Gate 2 (MVP)**: $50-200k, 2-3 months, validate product-market fit
- **Gate 3 (Scale)**: $200k-1M, 6-12 months, validate unit economics
- **Gate 4 (Growth)**: $1M+, ongoing, optimize and scale

**Kill rates by gate** (typical):
- Gate 0 → 1: Kill 50% (cheap to kill, many bad ideas)
- Gate 1 → 2: Kill 30% (learning reveals issues)
- Gate 2 → 3: Kill 20% (product-market fit hard)
- Gate 3 → 4: Kill 10% (unit economics don't work)

### Bayesian Updating for Kill Criteria

**Process**: Update kill probability as new data arrives

**Steps**:
1. **Prior probability** of kill: P(Kill) = initial estimate (e.g., 40% based on historical kill rate)
2. **Likelihood** of data given kill: P(Data | Kill) = how likely is this data if project should be killed?
3. **Likelihood** of data given success: P(Data | Success) = how likely is this data if project will succeed?
4. **Posterior probability** using Bayes theorem: P(Kill | Data) = P(Data | Kill) × P(Kill) / P(Data)

**Example**: SaaS feature with 10% adoption target (kill if <10% after 6 months)
- **Month 3 data**: 7% adoption
- **Prior**: P(Kill) = 40% (4 in 10 similar features killed historically)
- **Likelihood**: P(7% at month 3 | Kill) = 70% (projects that get killed typically have ~7% at halfway point)
- **Likelihood**: P(7% at month 3 | Success) = 30% (successful projects typically have ~12% at halfway point)
- **Posterior**: P(Kill | 7% adoption) = (0.70 × 0.40) / [(0.70 × 0.40) + (0.30 × 0.60)] = 0.28 / 0.46 = 61%
- **Interpretation**: 61% chance this project should be killed (up from 40% prior)
- **Action**: Evaluate closely, prepare pivot/kill plan

### Stopping Rules in Scientific Research

**Clinical trial stopping rules** (adapted for product development):

1. **Futility stopping**: Stop early if interim data shows unlikely to reach success criteria
   - **Rule**: If <10% chance of reaching target at current trajectory → Stop
   - **Application**: Monitor weekly, project trajectory, stop if trajectory misses by >30%

2. **Efficacy stopping**: Stop early if interim data shows clear success (reallocate resources)
   - **Rule**: If >95% confident success criteria will be met → Graduate early
   - **Application**: Feature with 25% adoption at month 3 (target: 15% at month 6) → Graduate to core product

3. **Safety stopping**: Stop if harmful unintended consequences detected
   - **Rule**: If churn increases >20% or NPS drops >10 points → Stop immediately
   - **Application**: New feature causing user confusion, support ticket spike → Kill

**Example**: Mobile app experiment
- **Target**: 20% weekly active users at month 6
- **Month 2 data**: 5% weekly active
- **Trajectory**: Projecting 10% at month 6 (50% below target)
- **Futility analysis**: 95% confidence interval for month 6: 8-12% (entirely below 20% target)
- **Decision**: Invoke futility stopping, kill experiment at month 2 (save 4 months)

---

## Key Principles Summary

1. **Set kill criteria before launch** (remove emotion, politics, sunk cost bias)
2. **Make criteria objective** (numbers, dates, not feelings)
3. **Assign clear decision rights** (single decision-maker, not committee)
4. **Don't move goalposts** (criteria are fixed; changes require formal process)
5. **Sunk costs are irrelevant** (only future value matters)
6. **Kill quickly** (wind down within 1 month, avoid zombie projects)
7. **Opportunity cost > sunk cost** (kill even if "almost done" if better options exist)
8. **Normalize killing** (celebrate discipline, share learnings, remove stigma)
9. **Portfolio thinking** (rank all projects, kill bottom 20-30% regularly)
10. **Learn from kills** (blameless postmortems, apply insights to future projects)

---

## Common Mistakes and Solutions

| Mistake | Symptom | Solution |
|---------|---------|----------|
| **Setting criteria after launch** | Goalposts move when results disappoint | Document criteria in PRD before launch, get sign-off |
| **Subjective criteria** | Debate over "low engagement" | Quantify: "<10% weekly active", not "poor adoption" |
| **Team consensus for kill** | Paralysis, no one wants to kill | Single decision-maker with clear authority |
| **Sunk cost justification** | "Invested $2M, can't quit" | Pre-mortem inversion: "Would we start this today?" |
| **Zombie projects** | Lingering for 6+ months | Wind down within 1 month of kill decision |
| **Stigma around killing** | Teams hide struggles, delay kill | Celebrate kills, share postmortems, normalize stopping |
| **Portfolio inertia** | Same projects year over year | Quarterly ranking + kill bottom 20-30% |
| **No postmortem** | Repeat same mistakes | Require postmortem within 2 weeks, share learnings |

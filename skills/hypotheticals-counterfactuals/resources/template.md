# Hypotheticals and Counterfactuals Templates

Quick-start templates for counterfactual analysis, scenario planning, and pre-mortem exercises.

## Focal Question Template

**What are you exploring?**

**Type**: [Counterfactual (past) / Hypothetical (future)]

**Core question**:
- Counterfactual: "What would have happened if [X] had been different?"
- Hypothetical: "What could happen if [X] occurs in the future?"

**Context**: [What decision, event, or situation are you analyzing?]

**Time frame**: [Past event date / Future time horizon (6 months, 1 year, 5 years)]

**Purpose**: [What do you hope to learn? Understand causality? Identify risks? Test assumptions?]

---

## Counterfactual Analysis Template

**Actual outcome** (what happened):
- Decision made: [What did we actually do?]
- Outcome: [What resulted?]
- Key metrics: [Quantify results]

**Counterfactual** (what if we had done differently):
- Alternative decision: "What if we had [done X instead]?"
- Hypothesized outcome: [What would have happened?]
- Reasoning: [WHY would outcome be different? Specify causal mechanism]

**Evidence for counterfactual**:
- Analogies: [Similar cases where X led to Y]
- Data: [Market data, competitor examples, historical patterns]
- Expert opinion: [What do domain experts say?]

**Causal insight**:
- What mattered: [Which factor was causal?]
- What didn't matter: [Which factors were irrelevant?]
- Lesson learned: [What should we do differently next time?]

**Example**:
- **Actual**: Launched in US first, 10k users in 6 months
- **Counterfactual**: "What if we had launched in EU first?"
- **Hypothesized outcome**: 5k users (smaller market, slower adoption)
- **Reasoning**: EU market 40% size of US, GDPR compliance slows growth
- **Insight**: US-first was right call. Market size matters more than competition.

---

## Pre-Mortem Template

**Project/Decision**: [What are you launching or deciding?]

**Future date**: "It is [6 months / 1 year] from now..."

**Assumed outcome**: "...and the [project has failed / decision was disastrous]."

**Individual brainstorm** (5 min, silent):
Each person writes 3-5 reasons why it failed.

1. [Failure reason 1]
2. [Failure reason 2]
3. [Failure reason 3]
4. [Failure reason 4]
5. [Failure reason 5]

**Consolidate** (round-robin sharing):
- [Consolidated failure cause 1]
- [Consolidated failure cause 2]
- [Consolidated failure cause 3]
- [Consolidated failure cause 4]
- [Consolidated failure cause 5]
...

**Vote on top risks** (dot voting):

| Risk | Votes | Likelihood | Impact | Priority |
|------|-------|------------|--------|----------|
| [Risk 1] | 8 | High | High | ⚠ Critical |
| [Risk 2] | 6 | Medium | High | ⚠ High |
| [Risk 3] | 4 | High | Medium | Medium |
| [Risk 4] | 2 | Low | Low | Low |

**Mitigation actions** (top 3-5 risks):

| Risk | Mitigation | Owner | Deadline |
|------|------------|-------|----------|
| [Risk 1] | [Specific action to prevent/reduce] | [Name] | [Date] |
| [Risk 2] | [Specific action] | [Name] | [Date] |
| [Risk 3] | [Specific action] | [Name] | [Date] |

---

## Scenario Generation Template

**Time horizon**: [6 months / 1 year / 3 years / 5 years]

**Key uncertainties** (2-3 factors that most shape the future):
1. [Uncertainty 1, e.g., "Market adoption rate"]
2. [Uncertainty 2, e.g., "Competitive intensity"]
3. [Uncertainty 3, e.g., "Regulatory environment"]

### Option A: Three Scenarios

**Optimistic scenario** (Probability: [%]):
- Name: "[Descriptive name]"
- Description: [1-2 paragraphs describing this future]
- Key drivers: [What makes this happen?]
- Implications: [What does this mean for us?]

**Baseline scenario** (Probability: [%]):
- Name: "[Descriptive name]"
- Description: [1-2 paragraphs]
- Key drivers: [What makes this happen?]
- Implications: [What does this mean for us?]

**Pessimistic scenario** (Probability: [%]):
- Name: "[Descriptive name]"
- Description: [1-2 paragraphs]
- Key drivers: [What makes this happen?]
- Implications: [What does this mean for us?]

### Option B: 2×2 Matrix

**Uncertainty 1**: [e.g., Market adoption] - Axes: [Slow / Fast]
**Uncertainty 2**: [e.g., Regulation] - Axes: [Strict / Loose]

|  | **Slow Adoption** | **Fast Adoption** |
|---|---|---|
| **Strict Regulation** | **Scenario 1**: "[Name]"<br>[Description] | **Scenario 2**: "[Name]"<br>[Description] |
| **Loose Regulation** | **Scenario 3**: "[Name]"<br>[Description] | **Scenario 4**: "[Name]"<br>[Description] |

---

## Scenario Development Template

**Scenario name**: "[Memorable title]"

**Time**: [Future date, e.g., "January 2026"]

**Narrative** (tell the story, make it vivid):
[2-4 paragraphs describing this world. Use present tense, concrete details, make it feel real.]

**Key assumptions**:
- [Assumption 1: what had to be true for this scenario?]
- [Assumption 2]
- [Assumption 3]

**Metrics in this world**:
- [Metric 1]: [Value, e.g., "Market size: $500M"]
- [Metric 2]: [Value, e.g., "Our market share: 15%"]
- [Metric 3]: [Value, e.g., "Churn rate: 3%/month"]

**Leading indicators** (early signals this scenario is unfolding):
- [Indicator 1]: [e.g., "If regulation bill passes Q1"]
- [Indicator 2]: [e.g., "If competitor raises >$50M"]
- [Indicator 3]: [e.g., "If adoption rate >20% MoM for 3 months"]

**Implications for our strategy**:
- What should we do in this world? [Strategic response]
- What should we avoid? [Actions that fail in this scenario]
- What capabilities do we need? [Org/tech requirements]

---

## Assumption Reversal Template

**Current assumption**: [State the belief we take for granted]

**Reversed assumption**: "What if [opposite] is true?"

**Explore the reversal**:
- Is it plausible? [Could the reversal actually be true?]
- Evidence for reversal: [What would suggest our assumption is wrong?]
- Implications if reversed: [What would we do differently?]
- New possibilities: [What doors does this open?]

**Example**:
- **Current**: "Customers want more features"
- **Reversed**: "What if customers want fewer features?"
- **Plausible?**: Yes (research shows feature bloat frustrates users)
- **Implications**: Simplify product, remove rarely-used features, focus on core workflow
- **New possibility**: "Feature-light" positioning vs. competitors

---

## Stress Test Template

**Decision being tested**: [What are we deciding?]

**Baseline assumptions**:
- [Assumption 1]: [Current expectation, e.g., "CAC = $100"]
- [Assumption 2]: [e.g., "Churn = 5%/month"]
- [Assumption 3]: [e.g., "Market size = $1B"]

**Stress scenario 1: Optimistic**
- [Assumption 1]: [Best case, e.g., "CAC = $50"]
- [Assumption 2]: [e.g., "Churn = 2%/month"]
- [Assumption 3]: [e.g., "Market size = $2B"]
- **Decision still valid?**: [Yes/No, with explanation]

**Stress scenario 2: Pessimistic**
- [Assumption 1]: [Worst case, e.g., "CAC = $200"]
- [Assumption 2]: [e.g., "Churn = 10%/month"]
- [Assumption 3]: [e.g., "Market size = $500M"]
- **Decision still valid?**: [Yes/No, with explanation]

**Stress scenario 3: Black swan**
- [Extreme event]: [e.g., "Major competitor offers product free"]
- **Decision still valid?**: [Yes/No, with explanation]

**Conclusion**:
- Decision robust? [Does it hold across scenarios?]
- Hedges needed? [What can we do to protect downside?]
- Go/no-go? [Final decision]

---

## Action Extraction Template

**Scenarios analyzed**: [List 2-4 scenarios explored]

**Common actions** (work across all scenarios):
- [Action 1]: [What should we do regardless of which future unfolds?]
- [Action 2]
- [Action 3]

**Hedges** (protect against downside scenarios):
- [Hedge 1]: [What reduces risk if pessimistic scenario happens?]
- [Hedge 2]

**Options** (prepare for upside scenarios):
- [Option 1]: [What positions us to capture value if optimistic scenario happens?]
- [Option 2]

**Monitoring** (track which scenario unfolding):
- [Indicator 1]: [What to watch, e.g., "Track regulation votes monthly"]
- [Indicator 2]: [e.g., "Monitor competitor funding rounds"]
- [Indicator 3]: [e.g., "Measure adoption rate vs. baseline"]

**Decision points** (when to adjust):
- If [indicator crosses threshold], then [action]
- If [indicator crosses threshold], then [action]

**Example**:
- **Common**: Build core product, hire team, launch beta
- **Hedge**: Keep burn low, maintain 18-month runway for slow-growth scenario
- **Option**: Prepare enterprise sales motion if early adoption strong
- **Monitor**: Track adoption rate monthly; if >15% MoM for 3 months, trigger enterprise hiring

---

## Quick Examples

### Example 1: Product Launch Pre-Mortem

**Project**: Launch new mobile app, target 50k downloads in 6 months

**Pre-mortem** (failure causes):
1. App crashes on Android (not tested thoroughly)
2. Marketing budget too small (couldn't acquire users at scale)
3. Onboarding too complex (80% drop-off after signup)
4. Competitor launched free version (undercut pricing)
5. App Store rejection (didn't follow guidelines)

**Mitigation**:
- Comprehensive Android testing before launch
- Double marketing budget or lower target
- Simplify onboarding to 3 steps max
- Monitor competitor activity, prepare pricing flex
- Review App Store guidelines, get pre-approval

### Example 2: Counterfactual Learning

**Actual**: Raised $5M Series A, 18-month runway, hired 15 people

**Outcome**: Burned through runway in 14 months, failed to reach next milestone

**Counterfactual**: "What if we had raised $3M instead?"
- **Hypothesized outcome**: 12-month runway, hired 8 people, reached profitability
- **Reasoning**: Smaller team = lower burn, forced focus on revenue, faster decisions
- **Insight**: Raising more money led to premature scaling. Constraint is good early-stage.

### Example 3: Strategic Scenarios (3 Futures)

**Time**: 2026 (2 years out)

**Optimistic ("Market Leader")**:
- 40% market share, $10M ARR, profitability
- Drivers: Product-market fit strong, viral growth, weak competition

**Baseline ("Steady Climb")**:
- 15% market share, $3M ARR, break-even
- Drivers: Expected growth, moderate competition, steady execution

**Pessimistic ("Survival Mode")**:
- 5% market share, $500k ARR, burning cash
- Drivers: Strong competitor launches, slow adoption, pivot needed

**Implications**: Build for "Steady Climb", hedge for "Survival" (low burn), prepare for "Leader" (scale infrastructure).

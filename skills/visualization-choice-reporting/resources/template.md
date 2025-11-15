# Visualization Choice & Reporting Template

Use this template to systematically choose the right chart and create a narrated report with insights and actions.

---

## Section 1: Question & Goal Clarification

**What question are you answering?**

[Be specific. Not "analyze revenue" but "How has revenue trended over the past year, and what's driving changes?"]

**Question type (check one):**
- [ ] Trend (How has X changed over time?)
- [ ] Comparison (How do categories compare?)
- [ ] Distribution (What's the spread/frequency of X?)
- [ ] Relationship (How do X and Y relate?)
- [ ] Composition (What are the parts of X?)
- [ ] Geographic (Where is X happening?)
- [ ] Hierarchical (What's the structure of X?)
- [ ] Multivariate (How do many variables interact?)

**Audience:**
- [ ] Executive (wants insights + actions, simple charts)
- [ ] Analyst (wants details, can handle complexity)
- [ ] General stakeholder (needs context, moderate detail)
- [ ] Technical (understands domain, wants precision)

**Context/Constraints:**
- Time they have: [e.g., 5 minutes to review, 30-minute presentation]
- Medium: [e.g., email, dashboard, slide deck, printed report]
- Key concern: [e.g., hitting targets, understanding root cause, making decision]

---

## Section 2: Data Profiling

**Data source:**

[Where is the data from? Database, CSV, API, manual collection?]

**Time period covered:**

[e.g., Jan-Dec 2024, Q1-Q4 2024, last 30 days]

**Granularity:**

[e.g., daily, weekly, monthly, by user, by transaction, aggregated]

**Data types (for each variable):**

| Variable | Type | Example Values | Notes |
|----------|------|----------------|-------|
| [e.g., Date] | Temporal | 2024-01-01 to 2024-12-31 | Monthly aggregates |
| [e.g., Segment] | Categorical | Enterprise, SMB | 2 categories |
| [e.g., Revenue] | Numerical | $1.5M - $2.6M | Continuous, dollar amounts |

**Dimensions:**
- [ ] 1D (single metric over time or categories)
- [ ] 2D (X vs Y, or metric by category)
- [ ] 3D+ (multiple metrics, multiple categories, time)

**Data size:**

[e.g., 24 rows (2 segments × 12 months), 10K transactions, 150 countries]

**Data quality notes:**

[Any missing data, outliers, anomalies to be aware of?]

---

## Section 3: Chart Selection

**Matched chart family (based on question type from Section 1):**

[From Chart Selection Guide in SKILL.md - e.g., "Trend → Line chart"]

**Specific chart type selected:**

[e.g., Multi-line chart, Horizontal bar chart, Scatter plot with regression]

**Rationale:**

Why this chart?
- **Question fit:** [How does this chart answer the question type?]
- **Data fit:** [How does it handle your data dimensions, size, types?]
- **Audience fit:** [Why is this appropriate for your audience's expertise/time?]

Example rationale:
> "Multi-line chart selected because:
> - Question: Trend over time (perfect for line charts)
> - Data: 2 categorical series × 12 time periods × 1 metric (line handles multiple series well)
> - Audience: Executives need to see trend at a glance; lines show rate of change clearly; annotations highlight key events"

**Alternatives considered (and why rejected):**

| Alternative Chart | Why Not Selected |
|-------------------|------------------|
| [e.g., Stacked area] | Would obscure individual segment trends; focus is on comparison not cumulative total |
| [e.g., Table] | Doesn't show trend visually; requires more cognitive effort to spot patterns |

---

## Section 4: Visualization Design

**Essential elements:**

- **Title (insight headline):** [Not "Revenue by Month" but "Revenue Up 30% YoY, Driven by Enterprise Segment"]

- **Axes:**
  - X-axis: [Label with units, e.g., "Month (2024)"]
  - Y-axis: [Label with units, e.g., "Revenue ($M)"]
  - Start Y at zero? [ ] Yes (for bar/column) [ ] No (for line, if range is narrow and zero isn't meaningful)

- **Legend/Labels:**
  - [ ] Direct labels on chart (preferred - easier to read)
  - [ ] Legend (if direct labels clutter)
  - Position: [e.g., right of chart, below chart, inline]

- **Annotations:**
  - [ ] Key event 1: [e.g., Arrow at May 2024: "Product launch"]
  - [ ] Key event 2: [e.g., Shaded region Oct-Dec: "Enterprise sales push"]
  - [ ] Threshold line: [e.g., Horizontal line at $2.25M: "2024 target"]
  - [ ] Callout: [e.g., Label on peak: "Q4 high: $2.6M"]

- **Colors:**
  - Primary palette: [e.g., Blue (Enterprise), Orange (SMB)]
  - Colorblind-safe? [ ] Yes [ ] No (if no, add patterns)
  - Purpose: [e.g., Blue/orange are distinguishable for red-green colorblindness]

- **Data source & timestamp:**
  - [e.g., "Source: Analytics DB, as of 2024-11-14"]

**Perceptual best practices applied:**

- [ ] Use position (most accurate) over angle/area where possible
- [ ] Remove chart junk (no 3D, no gradients, no heavy gridlines)
- [ ] Mute non-data ink (light gray gridlines, thin axes)
- [ ] Limit colors to 5-7 distinct hues
- [ ] Use pre-attentive attributes (color, size, position) to highlight signal

**Accessibility:**

- [ ] Alt text provided: [Describe the insight: "Line chart showing revenue grew from $2M to $2.6M (30% increase) Q1-Q4 2024, with Enterprise segment contributing 80% of growth."]
- [ ] Sufficient contrast (text readable, lines distinguishable)
- [ ] Patterns in addition to color (if critical - dashed/solid lines, hatched fills)

**Chart specification:**

[Provide detailed spec, code, or embed image]

Example spec:
- Chart type: Multi-line chart
- X-axis: Month (Jan, Feb, ..., Dec 2024)
- Y-axis: Revenue ($M), range $0-$3M, gridlines every $0.5M
- Series 1 (blue solid line): Enterprise revenue
- Series 2 (orange solid line): SMB revenue
- Annotations:
  - Arrow at May: "Product launch"
  - Shaded region Oct-Dec (light gray): "Enterprise initiative"
  - Horizontal dashed line at $2.25M (gray): "2024 target"
- Direct labels: "Enterprise" at end of blue line, "SMB" at end of orange line
- Source note: "Source: Analytics DB, as of 2024-11-14" (bottom right, small gray text)

---

## Section 5: Narrative Development

Use the **Headline → Pattern → Context → Meaning → Action** framework:

### 5.1 Headline (Insight-first one-liner)

[Not: "This chart shows monthly revenue." But: "Revenue grew 30% YoY, driven by Enterprise segment."]

**Your headline:**

[Write a single sentence that captures the key insight someone should take away from this visualization]

### 5.2 Pattern (What do you see?)

Describe the visual pattern in the data:
- Trends: [e.g., "Q1-Q2 flat at $2M/month, then steady climb to $2.6M in Q4"]
- Comparisons: [e.g., "Enterprise grew 120% while SMB declined 10%"]
- Outliers: [e.g., "August spike to $2.8M due to one-time deal"]
- Distributions: [e.g., "Most transactions $50-$200, with long tail to $10K"]

**Your pattern description:**

[2-3 sentences describing what you observe in the chart]

### 5.3 Context (Compared to what?)

Provide benchmarks, targets, historical comparison, or industry standards:
- vs Target: [e.g., "15% above $X plan"]
- vs Last period: [e.g., "Q4 2023 was $2.0M, now $2.6M"]
- vs Industry: [e.g., "Our 30% growth vs 10% industry average"]
- vs Expectation: [e.g., "Seasonality suggests Q4 boost, but this exceeded typical 15% bump"]

**Your context:**

[What makes this pattern significant? What are you comparing against?]

### 5.4 Meaning (Why does it matter?)

Interpret what the pattern + context implies:
- Implications: [e.g., "Suggests product-market fit in Enterprise"]
- Diagnosis: [e.g., "SMB churn indicates pricing mismatch"]
- Forecast: [e.g., "If sustained, Q1 2025 could hit $3M/month"]
- Risk/Opportunity: [e.g., "Enterprise now 58% of revenue, reducing diversification"]

**Your interpretation:**

[1-2 sentences explaining what this means for the business/product/team]

### 5.5 Actions (What should we do?)

Recommend specific next steps with:
- Priority actions: [What to do first, with owners/deadlines if possible]
- Investigations: [What to dig into to understand better]
- Monitoring: [What metrics to track going forward]

**Format:**
1. **Prioritize:** [Action with owner/timeline]
2. **Fix/Investigate:** [Action with owner/timeline]
3. **Monitor:** [Metrics to track]

**Your actions:**

1. **Prioritize:**

2. **Fix/Investigate:**

3. **Monitor:**

---

## Section 6: Full Narrative (Assembled)

Combine Sections 5.1-5.5 into a coherent narrative:

**Your complete narrative:**

> **Headline:** [From 5.1]
>
> **Pattern:** [From 5.2]
>
> **Context:** [From 5.3]
>
> **Meaning:** [From 5.4]
>
> **Actions:**
> 1. [From 5.5]
> 2. [From 5.5]
> 3. [From 5.5]

---

## Section 7: Validation Checklist

Before delivering, self-check with these criteria:

**Clarity**
- [ ] Chart type clearly matches question type
- [ ] Insight headline is clear and specific (not generic)
- [ ] Axes labeled with units
- [ ] Legend/labels easy to read
- [ ] Source and timestamp provided

**Accuracy**
- [ ] Y-axis scale appropriate (starts at zero for bar/column, appropriate range for line)
- [ ] No misleading visual distortions (no 3D, no truncated axes that exaggerate)
- [ ] Data source credible and cited
- [ ] Numbers in narrative match chart
- [ ] Caveats noted (if any data quality issues, assumptions, or limitations)

**Insight**
- [ ] Pattern clearly described (not just "revenue increased" but specifics)
- [ ] Context provided (vs benchmark, target, or history)
- [ ] Meaning interpreted (why it matters, what it implies)
- [ ] Insight is non-obvious (not just reading chart, but adding interpretation)

**Actionability**
- [ ] Specific next steps recommended (not vague "we should look into this")
- [ ] Actions have owners/timelines (or at least clear enough to assign)
- [ ] Actions are feasible given context
- [ ] Monitoring metrics defined

**Accessibility**
- [ ] Colorblind-safe palette (or patterns added)
- [ ] Alt text describes the insight
- [ ] Sufficient contrast
- [ ] Chart readable in black & white (test if printing)

**If any critical criteria fail (Clarity, Accuracy, Insight, Actionability < 3/5), revise before delivering.**

---

## Section 8: Delivery Package

Create `visualization-choice-reporting.md` with these sections:
1. Question (from Section 1)
2. Data Summary (source, period, granularity, dimensions, size from Section 2)
3. Visualization (chart type, rationale, design decisions, spec from Sections 3-4)
4. Narrative (complete narrative from Section 6)
5. Validation (self-check with rubric from Section 7)
6. Appendix (optional: raw data, alternatives, tests, caveats)

---

## Examples of Common Scenarios

| Scenario | Question Example | Chart Type | Narrative Focus | Design Notes |
|----------|------------------|------------|-----------------|--------------|
| **Executive Dashboard** | How has MRR trended this quarter? | Line chart | % change, context vs target, 1-2 actions | Clean, minimal annotations, insight-first title |
| **Analyst Deep-Dive** | Does marketing spend correlate with conversions? | Scatter + regression | Correlation strength, outliers, significance | R² annotated, outliers labeled, confidence interval |
| **Stakeholder Report** | Which product lines growing/declining? | Horizontal bar (ranked) | Top 3 growers/decliners, portfolio implications | Color-coded (green/red), percentages labeled |
| **Monitoring Dashboard** | How are key SaaS metrics trending? | Small multiples | Traffic light summary, items needing attention | Consistent scales, sparklines, RAG status |

---

## Common Pitfalls & Fixes

**Pitfall:** Chart doesn't answer the question (e.g., table when trend is the question)
**Fix:** Go back to Section 3, match question type to chart family

**Pitfall:** Title is descriptive not insightful ("Revenue by Month")
**Fix:** Lead with the insight ("Revenue Up 30% YoY")

**Pitfall:** No context, just absolute numbers ("Revenue is $2.6M")
**Fix:** Add benchmark ("$2.6M, 15% above $2.25M target")

**Pitfall:** Pattern without meaning ("Revenue increased")
**Fix:** Interpret ("Revenue up 30% suggests Enterprise PMF")

**Pitfall:** No actions, ends with observation
**Fix:** Recommend specific next steps (hire, investigate, monitor)

**Pitfall:** Chart is cluttered (too many colors, gridlines, decorations)
**Fix:** Remove chart junk, mute non-data ink, use white space

**Pitfall:** Misleading scale (truncated Y-axis on bar chart)
**Fix:** Start Y at zero for bar/column charts

**Pitfall:** Pie chart with 8 slices
**Fix:** Use horizontal bar chart (position more accurate than angle)

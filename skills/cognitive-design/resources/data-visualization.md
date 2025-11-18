# Data Visualization

This resource provides cognitive design principles specifically for charts, dashboards, and data-driven presentations.

**Covered topics:**
1. Chart selection via task-encoding alignment
2. Dashboard hierarchy and grouping
3. Progressive disclosure for interactive exploration
4. Narrative data visualization

---

## Why Data Visualization Needs Cognitive Design

### WHY This Matters

**Core insight:** Data visualization is cognitive communication - the goal is insight transfer from data to human understanding. Success requires matching visual encodings to human perceptual strengths.

**Common problems:**
- Wrong chart type chosen (pie when bar would be clearer)
- Dashboards overwhelming users with too many metrics
- Interactive tools causing anxiety (users fear getting lost)
- Data stories lacking clear narrative guidance

**How cognitive principles help:**
- Choose encodings that exploit perceptual accuracy (Cleveland & McGill hierarchy)
- Design dashboards within working memory limits (chunking, hierarchy)
- Structure exploration to reduce cognitive load (progressive disclosure, visible state)
- Guide interpretation through annotations and narrative flow

**Mental model:** Data visualization is a translation problem - translating abstract data into visual form that human perception can process efficiently.

---

## What You'll Learn

**Four key areas:**

1. **Chart Selection:** Match visualization type to user task and perceptual capabilities
2. **Dashboard Design:** Organize multiple visualizations for at-a-glance comprehension
3. **Interactive Exploration:** Enable data investigation without overwhelming or losing users
4. **Narrative Visualization:** Tell data stories with clear flow and guided interpretation

---

## Why Chart Selection Matters

### WHY This Matters

**Core insight:** Not all visual encodings serve all tasks equally well - position/length enable 5-10x more accurate comparison than angle/area.

**Cleveland & McGill's Perceptual Hierarchy (most to least accurate):**
1. Position along common scale
2. Position along non-aligned scales
3. Length
4. Angle/Slope
5. Area
6. Volume
7. Color hue
8. Color saturation

**Implication:** Chart type choice directly determines user accuracy in extracting insights.

**Mental model:** Different charts are tools for different jobs - bar chart is like precision calipers (accurate comparison), pie chart is like eyeballing (rough proportion sense).

---

### WHAT to Apply

#### Task-to-Chart Mapping

**User Task: Compare Values**

**Best choice:** Bar chart (horizontal or vertical)
- **Why:** Position/length encoding (top of hierarchy)
- **Enables:** Precise magnitude comparison, easy ranking
- **Example:** Comparing sales across 6 regions

**Avoid:** Pie chart
- **Why:** Angle/area encoding (lower accuracy)
- **Problem:** Difficult to judge which slice is larger when differences are subtle

**Application rule:**
```
For precise comparison → bar chart with common baseline
Sort descending for easy ranking
Add data labels for exact values (dual coding)
```

---

**User Task: Show Trend Over Time**

**Best choice:** Line chart
- **Why:** Position along time axis shows progression naturally
- **Enables:** Pattern detection (rising, falling, cyclical), slope perception
- **Example:** Monthly revenue over 2 years

**Avoid:** Bar chart for trends (acceptable but line is clearer), stacked area (hard to compare non-bottom series)

**Application rule:**
```
Time always on x-axis (left to right)
Use line for continuous data, bar for discrete periods
Limit to 5-7 lines max (more becomes tangled mess)
Annotate significant events ("Product launch Q2")
```

---

**User Task: Understand Distribution**

**Best choice:** Histogram or box plot
- **Why:** Shows shape (normal, skewed, bimodal), spread, outliers
- **Enables:** Pattern recognition (is data normally distributed?), outlier identification
- **Example:** Distribution of customer order values

**Avoid:** Pie charts (can't show distribution), bar charts of individual values (too granular)

**Application rule:**
```
Histogram: Choose appropriate bin width (too narrow = noise, too wide = hide patterns)
Box plot: Shows median, quartiles, outliers clearly
Include sample size in label for context
```

---

**User Task: Show Part-to-Whole Relationship**

**Acceptable choice:** Pie chart (BUT only if ≤5 slices and differences clear)
- **Why:** Circular metaphor intuitive for "whole"
- **Limitations:** Hard to judge angles, tiny slices unreadable

**Better choice:** Stacked bar chart or treemap
- **Why:** Position/length still more accurate than angle
- **Enables:** Easier comparison of parts

**Application rule:**
```
If using pie: ≤5 slices, sort descending, label percentages directly
Better: Stacked bar (compare lengths) or treemap (hierarchical parts)
Always ask: "Do users need precise comparison?" → If yes, avoid pie
```

---

**User Task: Find Outliers or Clusters**

**Best choice:** Scatterplot
- **Why:** 2D position enables pattern detection, outliers pop out preattentively
- **Enables:** Correlation visualization, cluster identification
- **Example:** Relationship between marketing spend and revenue by product

**Application rule:**
```
Add trend line if correlation expected
Use color/shape for categorical third variable (max 5-7 categories)
Label outliers with annotations
Consider log scale if data spans orders of magnitude
```

---

**User Task: Compare Multiple Variables**

**Best choice:** Small multiples (repeated chart structure)
- **Why:** Consistent structure enables pattern comparison across conditions
- **Enables:** Seeing how patterns change by category
- **Example:** Monthly sales trends for each product category (separate line chart per category)

**Application rule:**
```
Keep axes consistent across multiples for fair comparison
Arrange in logical order (by average, alphabetically, geographically)
Limit to 6-12 multiples (more requires pagination)
Highlight one for focus if needed
```

---

## Why Dashboard Design Matters

### WHY This Matters

**Core insight:** Dashboards combine many visualizations competing for limited attention - without clear hierarchy and grouping, users experience cognitive overload.

**Problems dashboards solve:**
- At-a-glance status monitoring
- Quick decision-making
- Pattern detection across metrics

**Cognitive challenges:**
- Information density overwhelming working memory
- No clear entry point (where to look first?)
- Related metrics not visually grouped
- Excessive scrolling breaks mental model

**Mental model:** Dashboard is like airplane cockpit - instruments grouped by system, critical alerts preattentively salient, most important gauges in pilot's direct view.

---

### WHAT to Apply

#### Visual Hierarchy for Dashboards

**Principle:** Establish clear focal point with size, position, and contrast

**Application pattern:**

**Primary KPIs (3-4 max):**
```
- Position: Top-left (F-pattern start)
- Size: Large numbers (36-48px)
- Style: Bold, high contrast
- Purpose: "What's the current status?" answered in 5 seconds
```

**Secondary Metrics (5-10):**
```
- Position: Below or right of primary KPIs
- Size: Medium (18-24px)
- Grouping: Clustered by relationship (all conversion metrics together)
- Purpose: Supporting detail for primary KPIs
```

**Tertiary/Details:**
```
- Position: Lower sections or drill-down
- Size: Smaller (12-16px)
- Access: Details on demand (click to expand)
- Purpose: Deep investigation, not monitoring
```

**Example:** E-commerce dashboard - Primary KPIs top-left (revenue, conversion, users), secondary metrics mid (channels, products), tertiary bottom (details, history).

---

#### Gestalt Grouping for Clarity

**Principle:** Use proximity, similarity, and whitespace to show relationships

**Proximity:** Related metrics close, unrelated separated by whitespace
**Similarity:** Consistent styling (same charts styled same way, color encoding consistent)
**Example:** Traffic panel (sessions, pageviews, bounce), Conversion panel (rate, revenue, AOV) separated by whitespace, red for errors throughout

---

#### Chunking for Working Memory

**Principle:** Limit concurrent visualizations to 4±1 major groups

**Application rule:** Group >15 metrics into 3-5 categories, each with 3-5 metrics max = 9-25 metrics organized into 4±1 chunks (fits working memory).

---

#### Preattentive Salience for Alerts

**Principle:** Use red color ONLY for threshold violations requiring immediate action

**Application rule:** Normal = gray, alert = red (critical only). Avoid red for all negatives (causes alert fatigue). Example: Revenue down 2% = gray, down 15% = red threshold violation.

---

#### Data-Ink Ratio Maximization

**Principle:** Remove decorative elements; maximize ink showing actual data

**Remove:** Heavy gridlines, 3D effects, gradients, excessive decimals, decorative icons, chart borders
**Keep:** Data (points/lines/bars), minimal axes, direct labels, meaningful annotations

---

## Why Progressive Disclosure Matters

### WHY This Matters

**Core insight:** Users fear getting lost in complex data exploration - progressive disclosure (overview first, zoom/filter, then details) provides safety net and reduces cognitive load.

**Shneiderman's Mantra:** "Overview first, zoom and filter, then details on demand"

**Benefits:**
- Reduces initial cognitive load (don't show everything at once)
- Provides context before detail (prevents disorientation)
- Enables personalized investigation (users drill into what they care about)
- Lowers anxiety (visible state shows "where am I", undo provides safety)

**Mental model:** Like Google Maps - start with full map view (overview), zoom to neighborhood (filter), click building for details (details on demand).

---

### WHAT to Apply

#### Overview Level

**Purpose:** Provide context and entry point

**Design principles:**
```
Show: Overall pattern, main trends, big picture
Hide: Granular details, outliers (show in drill-down)
Enable: Quick understanding of "what's the story here?"
```

**Example:**
```
Sales Dashboard Overview:
- Total sales number (aggregated)
- Trend line (last 90 days)
- Top 3 performing regions (summary)
User understands: "Sales are up 12% this quarter, West region leading"
```

---

#### Filter/Zoom Level

**Purpose:** Focus on subset of interest

**Design principles:**
```
Show: Filtered results clearly
Externalize: Active filters as visible chips/tags (recognition, not recall)
Enable: Easy modification (click chip to remove filter)
Provide: Clear "Reset all filters" option
```

**Example:**
```
User clicks "West region" from overview:
- Dashboard updates to show only West region data
- Visible chip at top: "Region: West" with X to remove
- Breadcrumb: "All Regions > West"
- "Reset" button returns to overview
User sees: "I'm viewing West region data, can easily get back"
```

---

#### Details on Demand Level

**Purpose:** Reveal specifics only when needed

**Design principles:**
```
Trigger: Hover, click, or expand action (not visible by default)
Show: Granular data, additional metrics, raw numbers
Position: Tooltip, modal, or expandable section (doesn't disrupt main view)
```

**Example:**
```
User hovers over data point on trend line:
- Tooltip appears: "June 15, 2024: $45,234 sales, 234 orders, $193 AOV"
- User moves mouse away: Tooltip disappears
- Main chart unchanged (not cluttered with all this detail by default)
```

---

#### State Visibility

**Principle:** Always show current navigation state - don't make users remember

**Critical state to externalize:**
```
✓ Active filters (as removable chips)
✓ Current zoom level or time range
✓ Drilled-down path (breadcrumbs)
✓ Sorting/grouping applied
✓ Comparison baseline (if comparing to previous period)
```

**Example implementation:**
```
Dashboard header always shows:
- Time range: "Last 30 days" (clickable to change)
- Filters: [Region: West] [Product: Widget] (each with X to remove)
- Comparison: "vs. previous 30 days" (toggle on/off)
- Breadcrumb: "Overview > West > Widget Sales"

User never wonders: "What am I looking at? How did I get here?"
```

---

## Why Narrative Visualization Matters

### WHY This Matters

**Core insight:** People naturally seek stories with cause-effect and chronology - structuring data as narrative chunks information meaningfully and aids retention.

**Benefits of narrative structure:**
- Easier to process (story arc vs heap of facts)
- Better retention (narrative = memorable)
- Guided interpretation (annotations prevent misunderstanding)
- Emotional engagement (storytelling activates empathy)

**Mental model:** Data journalism isn't a data dump - it's a guided tour where the designer leads readers to insights.

---

### WHAT to Apply

#### Narrative Structure

**Classic arc:** Context → Problem/Question → Data/Evidence → Resolution/Insight

**Application to visualization:**

**Context (What's the situation?):**
```
- Title that sets stage: "U.S. Solar Energy Adoption 2010-2024"
- Subtitle: "How policy changes drove growth"
- Brief intro text or annotation providing background
```

**Problem/Question (What are we investigating?):**
```
- Visual question posed: "Did tax incentives accelerate adoption?"
- Annotation highlighting the question point on chart
```

**Data/Evidence (What does data show?):**
```
- Chart showing trend with clear inflection point
- Annotation: "Tax credit introduced 2015" with arrow to spike
- Supporting data: % increase after policy vs before
```

**Resolution/Insight (What did we learn?):**
```
- Conclusion annotation: "Adoption rate tripled post-incentive"
- Implications: "States with stronger incentives saw faster growth"
- Call-to-action or next question (optional)
```

---

#### Annotation Strategy

**Principle:** Guide attention to key insights; prevent misinterpretation

**Types of annotations:**

**Callout boxes:**
```
Purpose: Highlight main insight
Position: Near relevant data point
Style: Contrasting color or background
Content: 1-2 sentences max ("Sales spiked 45% after campaign launch")
```

**Arrows/Lines:**
```
Purpose: Connect explanation to data
Use: Point from text to specific data element
Example: Arrow from "Product launch" text to spike in line chart
```

**Shaded regions:**
```
Purpose: Mark time periods or ranges
Use: Highlight recession periods, policy changes, events
Example: Gray shaded region "COVID-19 lockdown Mar-May 2020"
```

**Direct labels:**
```
Purpose: Replace legend lookups
Use: Label lines/bars directly instead of requiring legend
Example: Line chart with "North region" text next to the line (not legend box)
```

**Application rule:**
```
Annotate: Main insight (what users should notice)
Annotate: Unusual events (explain outliers/anomalies)
Don't annotate: Obvious patterns (if trend is clear, don't state "going up")
Test: Can user grasp message without annotations? If not, add guidance
```

---

#### Scrollytelling

**Definition:** Visualization that updates or highlights aspects as user scrolls

**Benefits:**
- Maintains context (chart stays visible while story progresses)
- Reveals complexity gradually (progressive disclosure in narrative form)
- Engaging (interactive storytelling)

**Application pattern:**

**Example progression:** Start with full context (0%) → Highlight specific periods as user scrolls (33%, 66%) → End with full picture + projection (100%). Chart stays visible, smooth transitions, user can scroll back, provide skip option.


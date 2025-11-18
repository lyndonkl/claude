# Cognitive Fallacies & Visual Misleads

This resource covers common design failures that confuse or mislead users - what NOT to do and how to avoid cognitive pitfalls.

**Covered topics:**
1. Chartjunk and data-ink ratio violations
2. Misleading visualizations (truncated axes, 3D distortion)
3. Cognitive biases in interpretation
4. Data integrity violations
5. Integrity principles and solutions

---

## Why Avoid Cognitive Fallacies

### WHY This Matters

**Core insight:** Common visualization mistakes aren't just aesthetic failures - they cause systematic cognitive misinterpretation and damage trust.

**Problems caused by fallacies:**
- **Chartjunk:** Consumes working memory without conveying data
- **Truncated axes:** Exaggerates differences, misleads comparison
- **3D effects:** Distorts perception through volume illusions
- **Cherry-picking:** Misleads by omitting contradictory context
- **Spurious correlations:** Implies false causation

**Why designers commit fallacies:**
- Aesthetic appeal prioritized over clarity
- Unaware of cognitive impacts
- Intentional manipulation (sometimes)
- Following bad examples

**Ethical obligation:** Visualizations are persuasive - designers have responsibility to communicate honestly.

---

## What You'll Learn

**Five categories of failures:**

1. **Visual Noise:** Chartjunk, low data-ink ratio, clutter
2. **Perceptual Distortions:** 3D effects, volume illusions, inappropriate chart types
3. **Cognitive Biases:** Confirmation bias, anchoring, framing effects
4. **Data Integrity Violations:** Truncated axes, cherry-picking, non-uniform scales
5. **Misleading Correlations:** Spurious correlations, false causation

---

## Why Chartjunk Impairs Comprehension

### WHY This Matters

**Definition:** Gratuitous visual decorations that obscure data without adding information (Tufte).

**Cognitive mechanism:**
- Working memory limited to 4±1 chunks
- Every visual element consumes attentional resources
- Decorative elements compete with data for attention
- Resources spent on decoration unavailable for comprehension

**Result:** Slower comprehension, higher cognitive load, missed insights

---

### WHAT to Avoid

#### Common Chartjunk

**Avoid:** Heavy backgrounds (gradients/textures), excessive gridlines, 3D effects for decoration, decorative icons replacing data, ornamental elements (borders/fancy fonts)
**Why problematic:** Reduces contrast, creates visual noise, distorts perception, competes with data
**Solution:** White/light background, minimal gray gridlines, flat 2D design, simple bars, minimal decoration

---

#### Data-Ink Ratio

**Tufte's principle:** Maximize proportion of ink showing data, minimize non-data ink

**Application:**
```
Audit every element: "Does this convey data or improve comprehension?"
If NO → remove it
If YES → keep it minimal
```

**Example optimization:**
```
Before:
- Heavy gridlines: 30% ink
- 3D effects: 20% ink
- Decorative borders: 10% ink
- Actual data: 40% ink
Data-ink ratio: 40%

After:
- Minimal axis: 5% ink
- Simple bars: 95% ink
Data-ink ratio: 95%

Result: Faster comprehension, clearer message
```

---

## Why Truncated Axes Mislead

### WHY This Matters

**Definition:** Axes that don't start at zero, cutting off the baseline

**Cognitive issue:** Viewers assume bar length is proportional to value - truncation breaks this assumption

**Effect:** Small absolute differences appear dramatically large

---

### WHAT to Avoid

#### Truncated Bar Charts

**Problem example:**
```
Sales comparison:
Company A: $80M (bar shows from $70M)
Company B: $85M (bar shows from $70M)

Visual: Company B's bar looks 5x larger than A
Reality: Only 6.25% difference ($5M on $80M base)

Mislead mechanism: Truncated y-axis starting at $70M instead of $0M
```

**Solutions:**
```
Option 1: Start y-axis at zero (honest proportional representation)
Option 2: Use line chart instead (focuses on change, zero baseline less critical)
Option 3: If truncating necessary, add clear axis break symbol and annotation
Option 4: Show absolute numbers directly on bars to provide context
```

---

#### When Truncation is Acceptable

**Line charts:**
```
✓ Showing stock price changes over time
✓ Temperature trends
✓ Focus is on pattern/trend, not absolute magnitude comparison

Requirement: Still note scale clearly, provide context
```

**Small multiples with consistent truncation:**
```
✓ Comparing trend patterns across categories
✓ All charts use same y-axis range (fair comparison)
✓ Clearly labeled

Purpose: See shape differences, not magnitude
```

---

## Why 3D Effects Distort

### WHY This Matters

**Cognitive issue:** Human visual system estimates 3D volumes and angles imprecisely

**Mechanisms:**
- **Perspective foreshortening:** Elements at front appear larger than identical elements at back
- **Volume scaling:** Doubling height and width octuples volume, but may be perceived linearly
- **Angle distortion:** 3D pie slices at different positions appear different sizes even when equal

---

### WHAT to Avoid

#### 3D Bar Charts

**Problem:**
```
3D bars with depth dimension:
- Harder to judge bar height (top surface not aligned with axis)
- Perspective makes back bars look smaller
- Depth adds no information, only distortion

Solution: Use simple 2D bars
```

---

#### 3D Pie Charts

**Problem:**
```
3D pie with perspective:
- Slices at front appear larger than equal slices at back
- Angles further distorted by tilt
- Already-poor angle perception made worse

Solution: If pie necessary, use flat 2D; better yet, use bar chart
```

---

#### Volume Illusions

**Problem:**
```
Scaling icons in multiple dimensions:
Person icon twice as tall to represent 2x data
Visual result: 4x area (height × width)
Viewer perception: May see as 2x, 4x, or even 8x (volume)

Solution: Scale only one dimension (height), or use simple bars
```

---

## Why Cognitive Biases Affect Interpretation

### WHY This Matters

**Core insight:** Viewers bring cognitive biases to data interpretation - design can either reinforce or mitigate these biases.

**Key biases:**
- **Confirmation bias:** See what confirms existing beliefs
- **Anchoring:** First number sets benchmark for all subsequent
- **Framing effects:** How data is presented influences emotional response

**Designer responsibility:** Present data neutrally, provide full context, enable exploration

---

### WHAT to Avoid

#### Reinforcing Confirmation Bias

**Problem:**
```
Dashboard highlighting data supporting desired conclusion
- Only positive metrics prominent
- Contradictory data hidden or small
- Selective time periods

Result: Viewers who want to believe conclusion find easy support
```

**Solutions:**
```
✓ Present full context, not cherry-picked subset
✓ Enable filtering/exploration (users can challenge assumptions)
✓ Show multiple viewpoints or comparisons
✓ Note data limitations and contradictions
```

---

#### Anchoring Effects

**Problem:**
```
Leading with dramatic statistic:
"Sales increased 500%!" (from $10k to $50k, absolute small)
Then: "Annual revenue $2M" (anchored to 500%, seems disappointing)

First number anchors perception of all subsequent numbers
```

**Solutions:**
```
✓ Provide baseline context upfront
✓ Show absolute and relative numbers together
✓ Be mindful of what's shown first in presentations
✓ Use neutral sorting (alphabetical, not "best first")
```

---

#### Framing Effects

**Problem:**
```
Same data, different frames:
"10% unemployment" vs "90% employed"
"1 in 10 fail" vs "90% success rate"
"50 new cases today" vs "Cumulative 5,000 cases"

Same numbers, different emotional impact
```

**Solutions:**
```
✓ Acknowledge framing choice
✓ Provide multiple views (daily AND cumulative)
✓ Show absolute AND relative (percentages + actual numbers)
✓ Consider audience and choose frame ethically
```

**Note:** Framing isn't inherently wrong, but it's powerful - use responsibly

---

## Why Data Integrity Violations Damage Trust

### WHY This Matters

**Tufte's Graphical Integrity:** Visual representation should be proportional to numerical quantities

**Components:**
- Honest axes (zero baseline or marked truncation)
- Fair comparisons (same scale)
- Complete context (full time period, baselines)
- Clear labeling (sources, methodology)

**Why it matters:** Trust is fragile - one misleading visualization damages credibility long-term

---

### WHAT to Avoid

#### Cherry-Picking Time Periods

**Problem:**
```
"Revenue grew 30% in Q4!"
...omitting that it declined 40% over full year

Mislead mechanism: Showing only favorable subset
```

**Solutions:**
```
✓ Show full relevant time period
✓ If focusing on segment, show it IN CONTEXT of whole
✓ Note data selection criteria ("Q4 only shown because...")
✓ Provide historical comparison (vs same quarter previous year)
```

---

#### Non-Uniform Scales

**Problem:**
```
X-axis intervals:
0, 10, 20, 50, 100 (not uniform increments)

Effect: Trend appears to accelerate or decelerate artificially
```

**Solutions:**
```
✓ Use uniform scale intervals
✓ If log scale needed, clearly label as such
✓ If breaks necessary, mark with axis break symbol
```

---

#### Missing Context

**Problem:**
```
"50% increase!" without denominator
50% of what? 2 to 3? 1000 to 1500?

"Highest level in 6 months!" without historical context
What was level 7 months ago? 1 year ago? Historical average?
```

**Solutions:**
```
✓ Show absolute numbers + percentages
✓ Provide historical context (historical average, benchmarks)
✓ Include comparison baselines (previous period, peer comparison)
✓ Note sample size and data source
```

---

## Why Spurious Correlations Mislead

### WHY This Matters

**Definition:** Statistical relationship between variables with no causal connection

**Classic example:** Ice cream sales vs shark attacks (both increase in summer, no causal link)

**Cognitive bias:** Correlation looks like causation when visualized together

**Designer responsibility:** Clarify when relationships are correlational vs causal

---

### WHAT to Avoid

#### Dual-Axis Manipulation

**Problem:**
```
Dual-axis chart with independent scales:
Left axis: Metric A (scaled 0-100)
Right axis: Metric B (scaled 0-10)

By adjusting scales, can make ANY two metrics appear correlated
Viewer sees: Lines moving together, assumes relationship
Reality: Scales manipulated to create visual similarity
```

**Solutions:**
```
✓ Use dual-axis only when relationship is justified (not arbitrary)
✓ Clearly label both axes
✓ Explain WHY two metrics are shown together
✓ Consider separate charts if relationship unclear
```

---

#### Implying Causation

**Problem:**
```
Chart showing two rising trends:
"Social media usage and depression rates both rising"

Visual implication: One causes the other
Reality: Could be correlation only, common cause, or coincidence
```

**Solutions:**
```
✓ Explicitly state "correlation, not proven causation"
✓ Note other possible explanations
✓ If causal claim, cite research supporting it
✓ Provide mechanism explanation if causal
```

---

## Integrity Principles

### What to Apply

**Honest Axes:**
```
✓ Start bars at zero or clearly mark truncation
✓ Use uniform scale intervals
✓ Label clearly with units
✓ If log scale, label as such
```

**Fair Comparisons:**
```
✓ Use same scale for items being compared
✓ Don't manipulate dual-axis to force visual correlation
✓ Show data for same time periods
✓ Include all relevant data points (not selective)
```

**Complete Context:**
```
✓ Show full time period or note selection
✓ Include baselines (previous year, average, benchmark)
✓ Provide denominator for percentages
✓ Note when data is projected/estimated vs actual
```

**Accurate Encoding:**
```
✓ Match visual scaling to data scaling
✓ Avoid volume illusions (icon sizing)
✓ Use 2D representations for accuracy
✓ Ensure color encoding matches meaning (red=negative convention)
```

**Transparency:**
```
✓ Note data sources
✓ Mention sample sizes
✓ State selection criteria if data is subset
✓ Acknowledge limitations
✓ Provide access to full dataset when possible
```


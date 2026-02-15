# Fallacies Catalog

A comprehensive catalog of cognitive design failures organized by category. Each entry explains WHY it's a problem (cognitive mechanism), WHAT it looks like (examples), and HOW to fix it.

---

## Section 1: Visual Noise Fallacies

### WHY This Matters

Working memory is limited to 4±1 chunks. Every visual element consumes attentional resources. Decorative elements compete with data for attention — resources spent on decoration are unavailable for comprehension.

### Chartjunk

**Definition:** Gratuitous visual decorations that obscure data without adding information (Tufte).

**What to avoid:**
- Heavy backgrounds (gradients, textures) — reduces contrast
- Excessive gridlines — creates visual noise
- 3D effects for decoration — distorts perception
- Decorative icons replacing data — competes with information
- Ornamental elements (fancy fonts, borders) — distracts

**Solution:** White/light background, minimal gray gridlines, flat 2D design, simple bars, minimal decoration.

### Data-Ink Ratio

**Tufte's principle:** Maximize proportion of ink showing data, minimize non-data ink.

```
Audit every element: "Does this convey data or improve comprehension?"
If NO → remove it
If YES → keep it minimal
```

**Example optimization:**
- Before: 40% data ink (heavy gridlines 30%, 3D effects 20%, borders 10%)
- After: 95% data ink (minimal axis 5%)
- Result: Faster comprehension, clearer message

---

## Section 2: Perceptual Distortion Fallacies

### Truncated Axes

**WHY:** Viewers assume bar length is proportional to value. Truncation breaks this assumption, making small differences appear dramatically large.

**Problem:** Bar chart with y-axis starting at $70M instead of $0M — Company B's bar looks 5x larger than Company A, but actual difference is only 6.25%.

**Solutions:**
1. Start y-axis at zero (honest proportional representation)
2. Use line chart instead (focuses on change, zero baseline less critical)
3. If truncating necessary, add clear axis break symbol and annotation
4. Show absolute numbers directly on bars

**When truncation is acceptable:**
- Line charts showing trends (stock prices, temperatures)
- Small multiples with consistent truncation for pattern comparison
- Always require clear scale labeling and context

### 3D Effects

**WHY:** Human visual system estimates 3D volumes and angles imprecisely. Perspective foreshortening makes front elements appear larger. Volume scaling is non-linear (doubling height and width octuples volume).

**3D Bar Charts:**
- Harder to judge bar height (top surface misaligned with axis)
- Perspective makes back bars look smaller
- Depth adds no information, only distortion
- **Fix:** Use simple 2D bars

**3D Pie Charts:**
- Slices at front appear larger than equal slices at back
- Angles further distorted by tilt
- **Fix:** Use flat 2D pie, or better, use bar chart

**Volume Illusions:**
- Icon twice as tall represents 2x data, but visual area is 4x and volume is 8x
- **Fix:** Scale only one dimension (height), or use simple bars

---

## Section 3: Cognitive Bias Exploitation

### WHY This Matters

Viewers bring cognitive biases to data interpretation. Design can either reinforce or mitigate these biases. Designers have a responsibility to present data neutrally and enable exploration.

### Confirmation Bias Reinforcement

**Problem:** Dashboard highlighting only data supporting desired conclusion — positive metrics prominent, contradictions hidden, selective time periods.

**Solutions:**
- ✓ Present full context, not cherry-picked subset
- ✓ Enable filtering/exploration (users can challenge assumptions)
- ✓ Show multiple viewpoints or comparisons
- ✓ Note data limitations and contradictions

### Anchoring Effects

**Problem:** Leading with dramatic statistic — "Sales increased 500%!" (from $10k to $50k, absolute small). Subsequent numbers anchored to this first impression.

**Solutions:**
- ✓ Provide baseline context upfront
- ✓ Show absolute and relative numbers together
- ✓ Be mindful of presentation order
- ✓ Use neutral sorting (alphabetical, not "best first")

### Framing Effects

**Problem:** Same data, different frames create different emotional impact:
- "10% unemployment" vs "90% employed"
- "1 in 10 fail" vs "90% success rate"

**Solutions:**
- ✓ Acknowledge framing choice
- ✓ Provide multiple views (daily AND cumulative)
- ✓ Show absolute AND relative (percentages + actual numbers)
- ✓ Consider audience and choose frame ethically

**Note:** Framing isn't inherently wrong, but it's powerful — use responsibly.

---

## Section 4: Data Integrity Violations

### WHY This Matters

Tufte's Graphical Integrity: Visual representation should be proportional to numerical quantities. Trust is fragile — one misleading visualization damages credibility long-term.

### Cherry-Picking Time Periods

**Problem:** "Revenue grew 30% in Q4!" — omitting that it declined 40% over full year.

**Solutions:**
- ✓ Show full relevant time period
- ✓ If focusing on segment, show it IN CONTEXT of whole
- ✓ Note data selection criteria
- ✓ Provide historical comparison (vs same quarter previous year)

### Non-Uniform Scales

**Problem:** X-axis intervals: 0, 10, 20, 50, 100 — trend appears to artificially accelerate.

**Solutions:**
- ✓ Use uniform scale intervals
- ✓ If log scale needed, clearly label as such
- ✓ If breaks necessary, mark with axis break symbol

### Missing Context

**Problem:** "50% increase!" without denominator — 50% of what? "Highest level in 6 months!" without historical context.

**Solutions:**
- ✓ Show absolute numbers + percentages
- ✓ Provide historical context (average, benchmarks)
- ✓ Include comparison baselines
- ✓ Note sample size and data source

---

## Section 5: Spurious Correlations

### Dual-Axis Manipulation

**WHY:** By adjusting independent scales, ANY two metrics can appear correlated. Viewers see lines moving together and assume relationship.

**Solutions:**
- ✓ Use dual-axis only when relationship is justified
- ✓ Clearly label both axes
- ✓ Explain WHY two metrics are shown together
- ✓ Consider separate charts if relationship unclear

### Implying Causation

**Problem:** "Social media usage and depression rates both rising" — visual implication of causation when only correlation exists.

**Solutions:**
- ✓ Explicitly state "correlation, not proven causation"
- ✓ Note other possible explanations
- ✓ If causal claim, cite research supporting it
- ✓ Provide mechanism explanation if causal

---

## Integrity Principles Summary

1. **Honest Axes:** Start bars at zero or mark truncation; uniform intervals; clear labels
2. **Fair Comparisons:** Same scale for compared items; no manipulated dual-axis; same time periods
3. **Complete Context:** Full time period; baselines provided; denominators shown; projected vs actual distinguished
4. **Accurate Encoding:** Visual proportional to data; no volume illusions; 2D for accuracy
5. **Transparency:** Data sources cited; sample sizes noted; selection criteria stated; limitations acknowledged

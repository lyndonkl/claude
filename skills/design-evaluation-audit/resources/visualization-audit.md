# Visualization Audit Framework

Comprehensive 4-criteria quality assessment for data visualizations. Each criterion is independent — high scores on one don't compensate for failure on another.

---

## Why This Framework

### WHY This Matters

Visualization quality requires success on ALL four criteria. Like evaluating a car — needs to be safe (integrity), functional (efficiency), easy to use (clarity), and pleasant (aesthetics). Missing any dimension makes it poor overall.

**Use when:** Evaluating charts, dashboards, infographics, or any visual data representation.

---

## Criterion 1: Clarity

**Question:** Is the visualization immediately understandable and unambiguous?

### Checklist

- [ ] Is main message obvious or clearly annotated?
- [ ] Are axes labeled with units?
- [ ] Is legend clear and necessary? (or use direct labels if possible)
- [ ] Is title descriptive? (conveys what's being shown)
- [ ] Are annotations used to guide interpretation?
- [ ] Is chart type appropriate for the message?

### Test Method

**5-Second Test:** Show for 5 seconds, ask "What's the main point?"
- **Pass:** Correctly identify main insight
- **Fail:** Confused or remember decorative elements

### Scoring

- **5:** Main message graspable in <5 seconds, perfectly labeled
- **4:** Clear with minor improvements needed (e.g., better title)
- **3:** Understandable but requires effort
- **2:** Ambiguous or missing critical labels
- **1:** Incomprehensible

---

## Criterion 2: Efficiency

**Question:** Can users extract information with minimal cognitive effort?

### Checklist

- [ ] Are encodings appropriate for task? (position/length for comparison, not angle/area)
- [ ] Is chart type matched to user task? (compare → bar, trend → line, distribution → histogram)
- [ ] Is comparison easy? (common baseline, aligned scales)
- [ ] Is cross-referencing minimized? (direct labels instead of legend lookups)
- [ ] Are cognitive shortcuts enabled? (sorting by value, highlighting key points)

### Test Method

**Encoding check:** Identify user task, check encoding against Cleveland & McGill hierarchy.
- **Pass:** Position/length used for precise comparisons
- **Fail:** Angle/area/color used when position would work better

### Scoring

- **5:** Optimal encoding, zero wasted cognitive effort
- **4:** Appropriate with minor inefficiencies
- **3:** Works but more effort than necessary
- **2:** Poor encoding choice (pie when bar would be better)
- **1:** Wrong chart type for task

---

## Criterion 3: Integrity

**Question:** Is the visualization truthful and free from misleading distortions?

### Checklist

- [ ] Do axes start at zero (or clearly note truncation)?
- [ ] Are scale intervals uniform?
- [ ] Is data complete? (not cherry-picked dates hiding context)
- [ ] Are comparisons fair? (same scale for compared items)
- [ ] Is context provided? (baselines, historical comparison, benchmarks)
- [ ] Are limitations noted? (sample size, data source, margin of error)

### Integrity Tests

1. **Axis test:** Does y-axis start at zero for bar charts? If not, is truncation noted?
2. **Completeness test:** Is full relevant time period shown?
3. **Fairness test:** Are compared items on same scale?

### Scoring

- **5:** Completely honest, full context provided
- **4:** Honest with minor context improvements possible
- **3:** Not misleading but could provide more context
- **2:** Distortions present (truncated axis, cherry-picked data)
- **1:** Actively misleading (severe distortions, no context)

**CRITICAL:** Scores below 3 on integrity are unacceptable — fix immediately.

---

## Criterion 4: Aesthetics

**Question:** Is the visualization visually pleasing and appropriate for context?

### Checklist

- [ ] Is visual design professional and polished?
- [ ] Is color palette appropriate? (not garish, suits content tone)
- [ ] Is whitespace used effectively? (not cramped, not wasteful)
- [ ] Are typography choices appropriate? (readable, professional)
- [ ] Does style match context? (serious for finance, friendly for consumer)

### Scoring

- **5:** Beautiful and appropriate, enhances engagement
- **4:** Pleasant and professional
- **3:** Acceptable, not ugly but not polished
- **2:** Amateurish or inappropriate style
- **1:** Ugly or completely inappropriate

**Trade-off note:** If forced to choose, prioritize Clarity and Integrity over Aesthetics.

---

## Using the 4-Criteria Framework

### Process

**Step 1: Evaluate each criterion independently**
- Score Clarity (1-5)
- Score Efficiency (1-5)
- Score Integrity (1-5)
- Score Aesthetics (1-5)

**Step 2: Calculate average**
- Average = (Clarity + Efficiency + Integrity + Aesthetics) / 4
- **Pass threshold:** ≥3.5 average
- **Critical failures:** Any individual score <3 requires attention

**Step 3: Identify weakest dimension** — primary improvement target

**Step 4: Prioritize fixes**
1. CRITICAL: Integrity < 3 (fix immediately)
2. HIGH: Clarity or Efficiency < 3
3. MEDIUM: Aesthetics < 3
4. LOW: Scores 3-4 (optimization)

**Step 5: Verify fixes don't harm other dimensions**

---

## Examples

### Example 1: Dashboard Review

**Context:** Team dashboard with 20 metrics, users overwhelmed

**Results:**
- ❌ Visibility: Too cluttered, 20 equal-weight metrics
- ❌ Hierarchy: Everything same size, alerts not prominent
- ❌ Chunking: 15 ungrouped metrics
- ❌ Simplicity: Chartjunk (gridlines, 3D, gradients)
- ✓ Feedback: Hover states present

**Fixes:** Reduce to 3-4 primary KPIs top-left, group others, remove chartjunk, show active filters.

### Example 2: Bar Chart Audit

**Context:** Q4 sales bar chart for presentation

**Scores:**
- Clarity: 4/5 — Clear labels, direct annotations
- Efficiency: 5/5 — Position/length encoding, sorted descending
- Integrity: 2/5 — ❌ Y-axis starts at 80 (exaggerates differences), no historical context
- Aesthetics: 4/5 — Clean, professional

**Average:** 3.75 (passes). **But** Integrity <3 = CRITICAL fix needed.

**Fixes:** Start y-axis at zero, add Q3 baseline, annotate top performer.

**After fixes:** 4.75/5 — Excellent.

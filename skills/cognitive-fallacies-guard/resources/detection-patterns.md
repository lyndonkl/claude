# Detection Patterns

Practical methodology for auditing visualizations, detecting cognitive fallacies, and documenting findings.

---

## Quick Scan Checklist

Use this 10-item checklist for a rapid first pass over any visualization.

```
Quick Scan Checklist:
- [ ] 1. Axis Origin: Do bar charts start at zero?
        FAIL: Y-axis truncated without break symbol or annotation
- [ ] 2. Scale Uniformity: Are axis intervals consistent?
        FAIL: Non-uniform spacing without log-scale label
- [ ] 3. Dimensionality: Are charts free of cosmetic 3D effects?
        FAIL: 3D bars, pies, or perspective effects adding no data value
- [ ] 4. Data-Ink Ratio: Is most visual ink devoted to data?
        FAIL: Heavy gridlines, decorative backgrounds, ornamental elements
- [ ] 5. Chart-Task Match: Does chart type match the analytical task?
        FAIL: Pie for comparison, line for categories, area for precision
- [ ] 6. Context Present: Are baselines, denominators, sources provided?
        FAIL: Percentages without base numbers, no historical comparison
- [ ] 7. Time Period Honest: Is the full relevant time period shown?
        FAIL: Favorable window without noting full-period context
- [ ] 8. Dual-Axis Justified: If dual-axis, is the relationship established?
        FAIL: Unrelated metrics with independently scaled axes
- [ ] 9. Framing Balanced: Are both positive and negative frames available?
        FAIL: Only one framing when alternative tells different story
- [ ] 10. Causation Language: Are correlations labeled as such?
         FAIL: "Causes" language without cited causal evidence
```

**Scoring:** 0-2 fails = Generally sound. 3-5 fails = Targeted fixes needed. 6+ fails = Comprehensive redesign.

---

## Detection Methodology

Work through these layers in order — integrity issues must be resolved before optimizing clarity.

### Layer 1: Integrity (Check First)

Most serious — causes viewers to draw incorrect conclusions.

```
1. Verify axes: Zero baselines for bars, uniform intervals, clear labels
2. Verify scales: Same scale for compared items, no hidden manipulation
3. Verify completeness: Full time period, all relevant data, no cherry-picking
4. Verify encoding: Visual proportions match data proportions
5. Verify attribution: Data source stated, limitations acknowledged
6. Verify correlation claims: Causal language only where evidence supports
```

### Layer 2: Clarity (Check Second)

Causes confusion and slow comprehension, but not incorrect conclusions.

```
1. Verify hierarchy: Most important data is visually prominent
2. Verify labeling: All axes, legends, annotations clear and readable
3. Verify chart type: Encoding matches perceptual task
4. Verify chunking: Information grouped into digestible segments
5. Verify color use: Meaningful, accessible, consistent
```

### Layer 3: Efficiency (Check Third)

Makes visualization slower to use, but doesn't cause confusion.

```
1. Verify data-ink ratio: Minimal non-data ink
2. Verify redundancy: No duplicated information
3. Verify density: Appropriate for audience expertise
4. Verify scanning: Layout supports natural reading patterns
```

---

## Anti-Pattern Library

Compact reference for quick lookups during audit.

```
Anti-Pattern              | Detection Signal                  | Severity | Fix
--------------------------|-----------------------------------|----------|---------------------------
Truncated bar axis        | Y-axis doesn't start at zero      | Critical | Start at zero or use line
Non-uniform scale         | Unequal axis intervals            | Critical | Uniform intervals or log
Cherry-picked period      | Favorable subset without context  | Critical | Show full period
Dual-axis false corr.     | Unrelated metrics, tuned scales   | Critical | Separate charts
Implied causation         | Causal language without evidence  | Critical | State "correlation"
3D bar chart              | Depth dimension on bars           | High     | Use 2D bars
3D pie chart              | Tilted/perspective pie            | High     | 2D pie or bar chart
Volume illusion           | Multi-dim icon scaling            | High     | Scale one dimension
Confirmation bias layout  | Only positive metrics prominent   | High     | Show balanced view
Missing denominator       | Percentages without base numbers  | High     | Show absolute + %
Missing baseline          | Values without comparison         | High     | Add baseline
Anchoring order           | Dramatic stat shown first         | Medium   | Baseline context first
One-sided framing         | Single frame, alt tells diff story| Medium   | Provide multiple frames
Excessive chartjunk       | Data-ink ratio below 50%          | Medium   | Remove non-data ink
Heavy gridlines           | Gridlines > data prominence       | Medium   | Lighten or remove
Pie with >6 slices        | Too many to compare angles        | Low      | Horizontal bar chart
Ornamental borders        | Non-functional decoration         | Low      | Remove or simplify
```

---

## Integrity Principles

### 1. Honest Axes

- [ ] Bar charts start y-axis at zero
- [ ] If truncated, axis break symbol visible and annotated
- [ ] Scale intervals are uniform (or log scale labeled)
- [ ] Both axes have clear unit labels

### 2. Fair Comparisons

- [ ] Compared items use the same scale
- [ ] Dual-axis doesn't manufacture visual correlation
- [ ] Compared data covers same time periods
- [ ] All relevant data points included

### 3. Complete Context

- [ ] Full relevant time period shown (or selection noted)
- [ ] Baselines provided (previous year, average, benchmark)
- [ ] Denominators provided for all percentages
- [ ] Projected/estimated distinguished from actual

### 4. Accurate Encoding

- [ ] Visual scaling proportional to data scaling
- [ ] No volume illusions from icon sizing
- [ ] 2D representations for accuracy
- [ ] Color encoding follows conventions

### 5. Transparency

- [ ] Data sources cited
- [ ] Methodology stated
- [ ] Selection criteria documented if subset
- [ ] Limitations acknowledged

---

## Reporting Template

```
=== FALLACY AUDIT FINDING ===
Finding #: [number]
Fallacy Type: [Visual Noise / Perceptual Distortion / Cognitive Bias / Data Integrity / Spurious Correlation]
Specific Fallacy: [name]
Severity: [Critical / High / Medium / Low]

Evidence:
  Observed: [description]
  Location: [chart name, section, slide]
  Cognitive impact: [what incorrect conclusion viewer might draw]

Recommended Fix:
  Action: [specific fix]
  Priority: [immediate / next revision / future]
  Effort: [minimal / moderate / significant]
=== END FINDING ===
```

**Audit Summary:**

```
=== FALLACY AUDIT SUMMARY ===
Artifact: [name]  |  Date: [date]  |  Auditor: [name]

Total: [count] | Critical: [n] | High: [n] | Medium: [n] | Low: [n]
Quick Scan: [X/10 passed]

Top Priority Fixes:
1. [most critical]
2. [second]
3. [third]

Assessment: [Pass / Conditional Pass / Fail]
  Pass: 0 Critical, 0-1 High, Quick Scan >= 8/10
  Conditional: 0 Critical, 2-3 High, Quick Scan >= 6/10
  Fail: Any Critical, or 4+ High, or Quick Scan < 6/10
=== END SUMMARY ===
```

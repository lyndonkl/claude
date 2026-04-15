---
name: cognitive-fallacies-guard
description: Detects and prevents visual misleads, cognitive biases, and data integrity violations in visualizations, dashboards, reports, and presentations. Audits charts for honesty, diagnoses misinterpretation causes, and provides specific fixes. Invoke when user mentions chartjunk, misleading chart, truncated axis, data integrity, visual deception, 3D chart problems, cherry-picking data, or needs to audit visualizations for accuracy. For general design evaluation, use `design-evaluation-audit`. For cognitive foundations, use `cognitive-design`.
---

# Cognitive Fallacies Guard

## Table of Contents

- [Overview](#overview)
- [Fallacy Audit Workflow](#fallacy-audit-workflow)
- [Path Selection Menu](#path-selection-menu)
  - [Path 1: Visual Misleads Scan](#path-1-visual-misleads-scan)
  - [Path 2: Cognitive Bias Check](#path-2-cognitive-bias-check)
  - [Path 3: Data Integrity Verification](#path-3-data-integrity-verification)
- [Quick Reference](#quick-reference)
- [Guardrails](#guardrails)

---

## Overview

Visualizations are persuasive — common mistakes cause systematic misinterpretation, not just aesthetic failures. This skill scans for visual misleads (chartjunk, truncated axes, 3D distortion), checks for cognitive bias exploitation (confirmation bias reinforcement, anchoring, framing manipulation), and verifies data integrity (honest axes, complete data, fair comparisons).

**Related skills:** `design-evaluation-audit` for general design evaluation, `cognitive-design` for cognitive foundations, `d3-visualization` for creating visualizations, `visual-storytelling-design` for data stories.

---

## Fallacy Audit Workflow

**Time:** 15-30 minutes

**Copy this checklist and track your progress:**

```
Fallacy Audit Progress:
- [ ] Step 1: Scan for Visual Misleads
- [ ] Step 2: Check for Cognitive Biases
- [ ] Step 3: Verify Data Integrity
```

### Step 1: Scan for Visual Misleads

Check for chartjunk, 3D effects, truncated axes, volume illusions, and inappropriate chart types. These are the most common and visible fallacies.

**Resource:** [Fallacies Catalog](resources/fallacies-catalog.md) — Sections 1-2 (Visual Noise, Perceptual Distortion)

### Step 2: Check for Cognitive Biases

Look for confirmation bias reinforcement, anchoring effects, and framing manipulation. These are subtler but can significantly influence interpretation.

**Resource:** [Fallacies Catalog](resources/fallacies-catalog.md) — Section 3 (Cognitive Bias Exploitation)

### Step 3: Verify Data Integrity

Confirm honest axes, complete data, fair comparisons, proper context, and no spurious correlations. This is the most critical layer.

**Resource:** [Detection Patterns](resources/detection-patterns.md) — Integrity Principles and Quick Scan Checklist

---

## Path Selection Menu

### Path 1: Visual Misleads Scan

**Choose this when:** Checking for chartjunk, 3D effects, truncated axes, and encoding problems.

**→ [Go to Fallacies Catalog](resources/fallacies-catalog.md) — Sections 1-2**

---

### Path 2: Cognitive Bias Check

**Choose this when:** Looking for bias reinforcement in dashboard design, presentation framing, or data selection.

**→ [Go to Fallacies Catalog](resources/fallacies-catalog.md) — Section 3**

---

### Path 3: Data Integrity Verification

**Choose this when:** Verifying completeness, honesty, and context of data presentation.

**→ [Go to Detection Patterns](resources/detection-patterns.md)**

---

## Quick Reference

### 5 Integrity Principles

1. **Honest Axes** — Bar charts start at zero; uniform scale intervals; clear labels
2. **Fair Comparisons** — Same scale for compared items; no dual-axis manipulation
3. **Complete Context** — Full time period shown; baselines provided; denominators clarified
4. **Accurate Encoding** — Visual proportional to numerical; no volume illusions; 2D design
5. **Transparency** — Data sources cited; limitations acknowledged; methodology stated

### Quick Severity Guide

- **Severity: High** — Integrity violations (truncated bars without disclosure, cherry-picked data, implied causation)
- **HIGH:** Perceptual distortions (3D effects, volume illusions, missing denominators)
- **MEDIUM:** Bias reinforcement (one-sided framing, anchoring order, confirmation bias layout)
- **LOW:** Visual noise (excessive gridlines, decorative elements, ornamental borders)

---

## Guardrails

**Scope boundaries:** This skill detects visual misleads, identifies cognitive bias exploitation, verifies data integrity, and provides specific fixes for each fallacy found. It does not create designs, evaluate general usability, teach cognitive theory, or assess aesthetic quality.

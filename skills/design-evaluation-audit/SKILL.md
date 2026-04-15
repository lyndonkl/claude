---
name: design-evaluation-audit
description: Systematically evaluates existing designs against cognitive science principles using repeatable checklists, scoring rubrics, and severity-classified fix recommendations. Use when conducting design reviews or critiques, evaluating designs for cognitive alignment, performing quality assurance before launch, diagnosing usability issues, or choosing between design alternatives with objective criteria.
---

# Design Evaluation & Audit

## Table of Contents

- [Skill Boundaries](#skill-boundaries)
- [Design Review Workflow](#design-review-workflow)
- [Path Selection Menu](#path-selection-menu)
  - [Path 1: Run Cognitive Design Checklist](#path-1-run-cognitive-design-checklist)
  - [Path 2: Run Visualization Audit](#path-2-run-visualization-audit)
  - [Path 3: Combined Review](#path-3-combined-review)
- [Quick Reference](#quick-reference)
- [Guardrails](#guardrails)

---

## Skill Boundaries

**Use instead of this skill for:**
- Creating new designs from scratch: use `cognitive-design`
- Learning cognitive theory: use `cognitive-design` Path 1
- Detecting misleading visualizations: use `cognitive-fallacies-guard`

---

## Design Review Workflow

**Time:** 30-90 minutes depending on scope

**Copy this checklist and track your progress:**

```
Design Evaluation Progress:
- [ ] Step 1: Systematic Assessment
- [ ] Step 2: Visualization Quality Audit (if applicable)
- [ ] Step 3: Severity Classification & Prioritization
- [ ] Step 4: Fix Recommendations
```

### Step 1: Systematic Assessment

Apply the Cognitive Design Checklist across all 8 dimensions: Visibility, Visual Hierarchy, Chunking, Simplicity, Memory Support, Feedback, Consistency, Scanning Patterns. Check every item. Record pass/fail for each dimension with specific evidence.

**Resource:** [Cognitive Design Checklist](resources/cognitive-checklist.md)

### Step 2: Visualization Quality Audit (if applicable)

If the design includes data visualizations, apply the 4-Criteria Visualization Audit. Score each criterion 1-5: Clarity, Efficiency, Integrity, Aesthetics. Calculate average and identify weakest dimension.

**Resource:** [Visualization Audit Framework](resources/visualization-audit.md)

### Step 3: Severity Classification & Prioritization

Classify every finding by severity:
- **CRITICAL:** Integrity violations, accessibility failures, users cannot complete core tasks. Fix immediately.
- **HIGH:** Clarity/efficiency issues preventing use, missing feedback for critical actions, working memory overload (>10 ungrouped items). Fix before launch.
- **MEDIUM:** Suboptimal patterns, aesthetic issues, minor inconsistencies. Fix in next iteration.
- **LOW:** Minor optimizations, polish items. Fix when convenient.

**Priority rule:** Fix foundation-first — perception before coherence, integrity before aesthetics, critical before high.

### Step 4: Fix Recommendations

For each finding, document:
1. **What is wrong** — specific description with evidence
2. **Why it matters** — which cognitive principle is violated
3. **How to fix** — concrete, actionable recommendation
4. **Expected outcome** — what improves after the fix
5. **Effort estimate** — quick fix (minutes), moderate (hours), significant (days)

Verify fixes don't harm other dimensions.

---

## Path Selection Menu

### Path 1: Run Cognitive Design Checklist

**Choose this when:** Evaluating any interface, layout, content page, form, or general design.

**What you'll get:** Pass/fail across 8 cognitive dimensions, test methods, common failures, severity-classified findings.

**Time:** 20-40 minutes

**→ [Go to Cognitive Design Checklist](resources/cognitive-checklist.md)**

---

### Path 2: Run Visualization Audit

**Choose this when:** Evaluating data visualizations — charts, graphs, dashboards, infographics.

**What you'll get:** 1-5 scores on Clarity, Efficiency, Integrity, Aesthetics with pass/fail threshold.

**Time:** 15-30 minutes per visualization

**→ [Go to Visualization Audit Framework](resources/visualization-audit.md)**

---

### Path 3: Combined Review

**Choose this when:** Comprehensive review covering both interface elements and data visualizations.

**Process:** Run Cognitive Checklist first, then Visualization Audit on each data component, merge findings, produce unified fix list.

**Time:** 45-90 minutes

**→ Start with [Cognitive Checklist](resources/cognitive-checklist.md), then [Visualization Audit](resources/visualization-audit.md)**

---

## Quick Reference

### 3-Question Rapid Check

**1. Attention** — "Is it obvious what to look at first?"
- If NO: hierarchy and visibility issues

**2. Memory** — "Is the user required to remember anything that could be shown?"
- If NO: memory support and chunking issues

**3. Clarity** — "Can someone unfamiliar understand in 5 seconds?"
- If NO: simplicity and comprehension issues

All YES = likely cognitively sound. Any NO = run full checklist on the failing area.

---

## Guardrails

**Out of scope:** Creating designs, teaching theory, providing domain guidance, replacing user testing, or covering full accessibility compliance.

**In scope:** Systematic evaluation against cognitive principles, severity-classified findings, prioritized fix recommendations, and visualization quality scoring.

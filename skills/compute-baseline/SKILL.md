---
name: compute-baseline
description: Computes substacker's rolling 4-week baseline for open rate, click rate, views-per-send, and weekly subscriber delta using corpus/stats/ archived CSVs. Produces per-metric z-scores of the current week against the baseline and flags cold-start windows where fewer than 4 prior weeks exist. Use after ingest-substack-csv each Monday. Trigger keywords: baseline, rolling median, z-score, cold start, per-metric comparison.
---

# Compute Baseline

## Workflow

```
Per week:
- [ ] Step 1: Load last 4 weekly CSVs from corpus/stats/
- [ ] Step 2: For each metric (open_rate, click_rate, views_per_send, weekly_sub_delta):
    - Compute 4-week median
    - Compute trimmed median (drop 1 outlier)
    - Compute IQR
- [ ] Step 3: z-score = (current - median) / IQR
- [ ] Step 4: If <4 weeks in history, return baseline: not-yet-established
- [ ] Step 5: Emit baseline object per metric with confidence flag
```

## Baseline object schema

```json
{
  "open_rate": {"current": 0.47, "median_4w": 0.49, "trimmed_median": 0.49, "iqr": 0.03, "z": -0.67, "confidence": "medium"},
  "click_rate": {...},
  "views_per_send": {...},
  "weekly_sub_delta": {...},
  "cold_start": false
}
```

Confidence: `high` if 4+ weeks and low IQR. `medium` if 4+ weeks and typical IQR. `low` if N<4.

## Guardrails

1. Only compare writer's own trajectory. Never pull external benchmarks.
2. Below N=4, return cold-start flag. Report writes "baseline not yet established" rather than noisy averages.
3. IQR-based comparisons (not σ-based) for robustness at small N.
4. Outlier handling: use trimmed median to blunt a single extreme week.
5. |z| ≥ 1.0 is the "material move" threshold used downstream by `attribute-performance`.
6. Don't recompute baselines for prior weeks. Each week's baseline is from that week's trailing 4.

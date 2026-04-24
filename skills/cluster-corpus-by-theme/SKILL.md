---
name: cluster-corpus-by-theme
description: Performs axial-coding-style thematic clustering over the substacker corpus of published posts to surface candidate sections. Uses Braun & Clarke's six-phase thematic analysis — familiarization, initial coding, searching for themes, reviewing themes, defining themes, naming. Reads full bodies, not titles. Use when re-opening the section question. Trigger keywords: cluster, theme, axial coding, thematic analysis, candidate sections.
---

# Cluster Corpus by Theme

## Workflow

```
Per Curator run:
- [ ] Step 1: Read every post in corpus/published/** end-to-end (not just titles)
- [ ] Step 2: Extract 3-5 codes per post (concepts, methods, domains)
- [ ] Step 3: Group codes across posts by semantic similarity (axial)
- [ ] Step 4: Validate clusters — split or merge where needed
- [ ] Step 5: Report candidate clusters with membership, cohesion, outliers
```

## Output

```yaml
cluster_1:
  candidate_handle: "kalshi-log"
  posts: [list of slugs]
  cohesion: high | medium | low
  centroid_codes: [top 5 codes]
  outlier_posts: [weakly-attached members]
rejected_clusters: [clusters with <3 posts]
```

## Heuristics

- Cohesion `high`: ≥5 posts, shared centroid, clear register.
- Cohesion `medium`: 3-4 posts or mixed register.
- Cohesion `low`: cluster exists but coherence is weak.
- Reject any cluster with <3 posts (below the 3-post floor for real sections).

## Guardrails

1. Read full post bodies. Titles are marketing; bodies are the beat.
2. Do not force every post into a cluster. Outliers are legitimate.
3. If >30% of corpus doesn't cluster coherently (all cohesion low), emit "corpus too heterogeneous" → Curator abandons section proposals this run.
4. Include rejected clusters in output — they feed `recommend-prune` and "watch" candidates.
5. Single-threaded. Don't race on the corpus.

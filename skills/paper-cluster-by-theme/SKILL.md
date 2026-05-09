---
name: paper-cluster-by-theme
description: Groups a set of kept papers into 2-5 thematic clusters before synthesis, using abstract semantics + matched-keyword overlap. Names each cluster with a short noun phrase that describes what the cluster argues, not just the topic. Surfaces an "outliers" bucket for single-paper themes that don't fit. Domain-neutral - usable for any literature-scan workflow. Use after relevance filtering and before writing the synthesis report. Trigger keywords - cluster papers, group by theme, thematic clusters, paper themes, organize papers.
---

# paper-cluster-by-theme

Take a list of relevance-filtered papers and produce thematic clusters that the synthesis layer can write *about* rather than *list*.

A "cluster" here is not a topic label — it's an argument. "Diffusion models for protein design" is a topic. "Diffusion models are converging on AlphaFold-comparable accuracy without MSAs" is a theme. The synthesis is much stronger when clusters describe what the papers collectively *argue*.

## Workflow

```
- [ ] Step 1: Read all kept papers' titles, abstracts, and matched keywords
- [ ] Step 2: Identify 2-5 candidate themes from the abstract content
- [ ] Step 3: Assign each paper to its best-fit theme (or to outliers)
- [ ] Step 4: Re-name each theme as an argument-shaped phrase
- [ ] Step 5: Validate clusters (no empty cluster, no over-stuffed cluster, no paper in two)
- [ ] Step 6: Return clusters + outliers + assignment rationale
```

**Step 1 — Read inputs**

The skill takes a list of records (the KEEP set from `paper-relevance-filter`). It needs `id`, `title`, `abstract`, and `matched_keywords` for each.

**Step 2 — Candidate themes**

Two signals to use, in order:

1. **Matched-keyword groupings** (cheap, mechanical): if half the kept papers all share one keyword, that's a strong candidate cluster. Group by the most common matched keyword first; this gets you 70% of the way for a focused watchlist.
2. **Abstract semantics** (qualitative): for papers grouped by the same keyword but doing different *kinds* of work (e.g., review vs benchmark vs new method), split into sub-clusters. Conversely, for papers in different keyword groups that read like the same argument (e.g., a methods paper and an application paper extending it), merge.

Aim for 2-5 clusters. Hard cap at 5 — beyond that, the synthesis layer cannot say anything coherent about each. If you have only 2-3 papers total and they don't form a theme, return one cluster called "Notable single papers" — do not force 3 clusters of 1.

**Step 3 — Assign papers**

Each paper goes to exactly one cluster (or outliers). When a paper plausibly fits two, choose the cluster where the paper's *contribution* (read from the abstract's last 1-2 sentences) is the better fit — not just where its keywords match. Note the alternative in `also_fits`.

**Outliers**: a paper with no good cluster fit. Do not exceed 3-4 outliers; if you have more, your clustering is too narrow — go back to Step 2 and split a cluster.

**Step 4 — Argument-shaped names**

Bad cluster names:
- "Protein design"
- "Single-cell papers"
- "AI in biology"

Good cluster names (argument-shaped):
- "Protein design moves from sequence-only to sequence+structure conditioning"
- "Single-cell methods converge on multi-modal embeddings as default"
- "AI-discovered targets are being re-validated with classical biology"

A good name is a one-line argument the cluster collectively makes. If you can't write that argument because the papers in the cluster disagree, that's actually fine — name it as a tension: "Disagreement on whether X requires Y."

**Step 5 — Validate**

Reject and redo if:
- Any cluster has 0 papers (delete it)
- Any cluster has > 70% of papers (split it)
- Any paper appears in two clusters (force-pick one)
- Total clusters > 5 (merge nearest two)
- Outliers > 4 (split a cluster to absorb)

**Step 6 — Return**

```json
{
  "clusters": [
    {
      "name": "Protein design moves from sequence-only to sequence+structure conditioning",
      "rationale": "Three of the kept papers (P1, P2, P5) all argue that adding structural context at training time outperforms sequence-only baselines. P5 disagrees on the magnitude.",
      "papers": ["10.1101/2026.05.07.123456", "PMID:39000001", "10.1101/2026.05.06.654321"],
      "tension": "P5 reports smaller gains than P1; worth noting in synthesis."
    },
    {
      "name": "Single-cell foundation models start releasing benchmarks, not just weights",
      "rationale": "Two papers (P3, P7) release benchmark suites alongside the model.",
      "papers": ["PMID:39000002", "10.1101/2026.05.05.111111"],
      "tension": null
    }
  ],
  "outliers": [
    {
      "id": "PMID:39111222",
      "rationale": "Single paper on cryo-EM segmentation; doesn't fit either cluster but matches watchlist."
    }
  ],
  "summary": {
    "input_papers": 17,
    "cluster_count": 3,
    "outlier_count": 2,
    "largest_cluster_size": 6,
    "smallest_cluster_size": 3
  }
}
```

## Common Patterns

**Pattern A — Focused watchlist, week with 5-15 papers**: typically 2-3 strong clusters + 1-2 outliers. The default.

**Pattern B — Broad watchlist, week with 20+ papers**: 4-5 clusters; cluster names get more specific (one keyword's worth each). Risk: cluster names become topic labels rather than arguments. Push back on yourself.

**Pattern C — Thin week (3-5 kept papers)**: skip clustering. Return one cluster "Notable single papers" with all of them. The synthesis layer will write per-paper rather than per-theme.

**Pattern D — Disagreement-heavy week**: when 2+ papers in a cluster directly contradict each other on a finding, name the cluster as the tension and call this out in `tension`. The synthesis layer treats this as a high-value 30K-ft observation.

## Guardrails

1. **Never name a cluster after a topic when you can name it after an argument.** Topic names tell the user what the papers are about; argument names tell them what to take away. The latter is the whole point of the digest.
2. **Never put a paper in two clusters.** If it fits two, the second one goes in `also_fits` as a note, not as a duplicate assignment.
3. **Never exceed 5 clusters.** The synthesis layer renders one paragraph per cluster; 6+ is unreadable.
4. **Never coerce 3 clusters when there are clearly 2.** A real "1 cluster + 4 outliers" week is honest. A faked "3 clusters of 1-2 papers each" is noise.
5. **Never cluster by source.** "All the bioRxiv papers" is not a theme. Source belongs in the per-paper line, not the cluster name.
6. **Never cluster by date within the week.** Same reason — temporal proximity is not a theme.
7. **Always cite the rationale.** Each cluster has a `rationale` field that names which papers anchor the theme and how. Without it the synthesis writer has to re-derive your reasoning.

## Quick Reference

| Cluster count | When                                               |
| ------------- | -------------------------------------------------- |
| 1             | Thin week (≤ 5 papers, no real grouping)           |
| 2-3           | Default for focused weekly digest                  |
| 4-5           | Broad watchlist or unusually busy week             |
| 6+            | Reject — merge until ≤ 5                           |

| Naming test                                                      | Pass? |
| ---------------------------------------------------------------- | ----- |
| Is the name a noun phrase that could be a topic in a textbook?   | FAIL  |
| Does the name name an argument or a tension?                     | PASS  |
| Could a reader predict the cluster's content from the name?      | PASS  |
| Could you swap two clusters' names and have it still make sense? | FAIL — names are too generic |

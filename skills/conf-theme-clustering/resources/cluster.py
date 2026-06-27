#!/usr/bin/env python3
"""
cluster.py — the embed -> reduce -> density-cluster path for conf-theme-clustering.

Reads an events.json ({meta, events:[...]}) produced by conf-program-extraction and
writes clusters.json + affinities.json matching the canonical schemas in the
conf-theme-clustering skill.

DIVISION OF LABOR (important):
  - This script does the GROUPING only: embeddings -> UMAP -> HDBSCAN -> representative
    members -> *provisional* labels (from the most common topics in each cluster) ->
    soft top-k affinities (cosine to cluster centroids).
  - It does NOT do human-quality LABELING. That is the one LLM step. The calling agent
    (conf-theme-cartographer) reads the representative members and rewrites each theme's
    `label` and `gloss`. Provisional labels here are placeholders so the file is valid.

GRACEFUL FALLBACK:
  If the embedding/clustering libraries are not installed, this script prints the exact
  pip install line and exits non-zero (code 3). The agent then falls back to the
  LLM-reasoned hierarchical method described in the skill. Missing libraries are a
  normal, expected branch — not an error to debug.

USAGE:
  python3 cluster.py --events data/01-events/events.json --out-dir data/02-clusters \\
      [--coarse-target 7] [--top-k 3] [--model all-MiniLM-L6-v2]
"""

import argparse
import json
import sys
from collections import Counter
from datetime import date

REQUIRED = ["numpy", "sentence_transformers", "umap", "hdbscan", "sklearn"]
PIP_LINE = "pip install numpy sentence-transformers umap-learn hdbscan scikit-learn"


def _check_libs():
    """Return (ok, missing[]). Import lazily so the no-deps fallback path stays clean."""
    import importlib
    missing = []
    for name in REQUIRED:
        try:
            importlib.import_module(name)
        except Exception:
            missing.append(name)
    return (len(missing) == 0, missing)


def _event_text(ev):
    """Assemble the text we embed: enriched abstract if present, else raw abstract,
    always reinforced with the title and extracted topics so short abstracts still
    carry signal."""
    parts = []
    if ev.get("title"):
        parts.append(ev["title"])
    abstract = ev.get("abstract_enriched") or ev.get("abstract_raw") or ""
    if abstract:
        parts.append(abstract)
    topics = (ev.get("axes") or {}).get("topic") or []
    if topics:
        parts.append("Topics: " + ", ".join(topics))
    return ". ".join(parts).strip() or (ev.get("title") or ev.get("id", "untitled"))


def _provisional_label(member_topics):
    """A placeholder label from the most common topics in a cluster. The LLM replaces it."""
    if not member_topics:
        return "(unlabeled cluster)"
    common = [t for t, _ in Counter(member_topics).most_common(3)]
    return " / ".join(common)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--coarse-target", type=int, default=7,
                    help="rough number of coarse themes desired (guides min_cluster_size)")
    ap.add_argument("--top-k", type=int, default=3, help="affinities kept per event")
    ap.add_argument("--model", default="all-MiniLM-L6-v2")
    args = ap.parse_args()

    ok, missing = _check_libs()
    if not ok:
        sys.stderr.write(
            "conf-theme-clustering: embedding pipeline unavailable (missing: "
            + ", ".join(missing) + ").\n"
            "Install with:\n    " + PIP_LINE + "\n"
            "Or fall back to the LLM-reasoned hierarchical method (see SKILL.md).\n")
        sys.exit(3)

    import numpy as np
    from sentence_transformers import SentenceTransformer
    import umap
    import hdbscan

    with open(args.events) as f:
        data = json.load(f)
    events = data.get("events", data if isinstance(data, list) else [])
    if not events:
        sys.stderr.write("conf-theme-clustering: no events found in input.\n")
        sys.exit(2)

    ids = [ev.get("id") or f"event-{i}" for i, ev in enumerate(events)]
    texts = [_event_text(ev) for ev in events]
    topics_by_idx = [((ev.get("axes") or {}).get("topic") or []) for ev in events]

    # --- Embed ---
    model = SentenceTransformer(args.model)
    emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    emb = np.asarray(emb, dtype="float32")

    # --- Reduce: UMAP to a low dimension where density structure is visible. ---
    n = len(events)
    n_neighbors = max(2, min(15, n - 1))
    reducer = umap.UMAP(n_neighbors=n_neighbors, n_components=min(5, max(2, n - 2)),
                        metric="cosine", random_state=42)
    reduced = reducer.fit_transform(emb)

    # --- Density-cluster: HDBSCAN. min_cluster_size scaled so we land near coarse-target. ---
    min_cluster_size = max(2, n // max(args.coarse_target, 1))
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric="euclidean")
    labels = clusterer.fit_predict(reduced)  # -1 == noise == outlier

    # --- Cluster centroids in embedding space (for soft affinities + representatives). ---
    unique = sorted(set(int(l) for l in labels if l != -1))
    centroids = {}
    for cl in unique:
        idxs = [i for i, l in enumerate(labels) if l == cl]
        centroids[cl] = emb[idxs].mean(axis=0)

    def cosine(a, b):
        denom = (np.linalg.norm(a) * np.linalg.norm(b)) or 1.0
        return float(np.dot(a, b) / denom)

    # --- Build coarse themes with representative members + provisional labels. ---
    coarse_themes = []
    theme_id_of_cluster = {}
    for rank, cl in enumerate(unique, start=1):
        tid = f"T{rank}"
        theme_id_of_cluster[cl] = tid
        idxs = [i for i, l in enumerate(labels) if l == cl]
        # representatives: members closest to the centroid
        c = centroids[cl]
        ranked = sorted(idxs, key=lambda i: -cosine(emb[i], c))
        reps = [ids[i] for i in ranked[:min(5, len(ranked))]]
        member_topics = [t for i in idxs for t in topics_by_idx[i]]
        coarse_themes.append({
            "id": tid,
            "label": _provisional_label(member_topics),     # LLM rewrites this
            "gloss": "(provisional — replace with an LLM-written one-sentence gloss)",
            "size": len(idxs),
            "representative_event_ids": reps,
            "subclusters": [],                               # optional: agent may split further
        })

    # --- Outliers: HDBSCAN noise points. Kept as a first-class bucket. ---
    outliers = []
    for i, l in enumerate(labels):
        if l == -1:
            outliers.append({"event_id": ids[i],
                             "why": "no dense topical neighborhood in this program (HDBSCAN noise)"})

    # --- Soft affinities: cosine to every theme centroid, top-k, for EVERY event. ---
    affinities = {}
    for i in range(n):
        sims = []
        for cl in unique:
            sims.append((theme_id_of_cluster[cl], cosine(emb[i], centroids[cl])))
        sims.sort(key=lambda x: -x[1])
        top = sims[:args.top_k] if sims else []
        # rescale cosine [-1,1] -> [0,1] so affinities read as memberships
        affinities[ids[i]] = [{"theme_id": t, "affinity": round((s + 1) / 2, 3)} for t, s in top]

    today = date.today().isoformat()
    clusters_doc = {
        "method": "embed-hdbscan",
        "generated_on": today,
        "stability_note": (f"embed({args.model}) -> UMAP -> HDBSCAN(min_cluster_size="
                           f"{min_cluster_size}); {len(unique)} coarse themes, "
                           f"{len(outliers)} outliers. Labels are provisional pending LLM relabel. "
                           "Re-running with the same inputs is reproducible (random_state fixed)."),
        "coarse_themes": coarse_themes,
        "outliers": outliers,
    }
    affinities_doc = {"generated_on": today, "top_k": args.top_k, "affinities": affinities}

    import os
    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "clusters.json"), "w") as f:
        json.dump(clusters_doc, f, indent=2)
    with open(os.path.join(args.out_dir, "affinities.json"), "w") as f:
        json.dump(affinities_doc, f, indent=2)

    sys.stderr.write(
        f"conf-theme-clustering: wrote {len(coarse_themes)} coarse themes + "
        f"{len(outliers)} outliers to {args.out_dir}.\n"
        "NOTE: theme labels/glosses are provisional — the conf-theme-cartographer agent "
        "must relabel them from the representative members before the map is used.\n")


if __name__ == "__main__":
    main()

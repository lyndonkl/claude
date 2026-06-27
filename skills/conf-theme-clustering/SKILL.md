---
name: conf-theme-clustering
description: Cluster a conference's event records into a small set of coarse themes with finer sub-clusters, an explicit outlier bucket, and soft (multi-membership) affinities — using the hybrid embed-then-label pipeline (embed abstracts, reduce, density-cluster, then LLM-label the clusters) when embedding libraries are available, and an LLM-reasoned hierarchical fallback when they are not. Embeddings do the grouping; the LLM only names the groups. Conference-agnostic. Use when turning structured event records into a navigable theme map for preference elicitation and scheduling, when you need 6-8 reasonable themes rather than 20 muddy ones, or when overlapping talks must belong to more than one theme. Trigger keywords - theme clustering, cluster talks, embed then label, soft membership, outlier talks, conference themes, topic map.
---

# Conference Theme Clustering

The job is to turn a few hundred event records into a map a person can actually reason over: a handful of **coarse themes**, each openable into **sub-clusters**, with the genuinely odd talks set aside in an **outlier bucket** rather than forced into a theme, and with each talk allowed to belong to **more than one theme** because real talks do. The map is the substrate everything downstream stands on — the elicitor grounds its questions in these themes, and the scheduler uses theme coverage to reward breadth.

The method that holds up is **hybrid, not pure-LLM-per-item and not the conference's own track labels**. Embeddings do the grouping because that step must be cheap and stable across runs; an LLM does only the labeling because that is the step that needs to read like a human wrote it. Running an LLM to decide every talk's cluster is costly and varies run to run; using the conference's published tracks throws away the cross-track structure that is often the most interesting thing in the program.

Four findings shape the design, and each is a guardrail later: **embeddings group / LLM labels**; **keep the outliers** (density clustering hands you an outlier set — that is a feature); **cluster coarse, then fine** (6–8 abstract themes separate far more cleanly than 20 fine-grained ones); and **soft multi-membership** (a single hard cluster mis-represents a talk like "evaluating agentic RAG" that legitimately lives in evaluation *and* agents *and* retrieval).

## The outputs (two contracts)

### Cluster map — `clusters.json`

```json
{
  "method": "embed-hdbscan | llm-reasoned",
  "generated_on": "YYYY-MM-DD",
  "stability_note": "how stable these clusters are; what would move a talk",
  "coarse_themes": [
    {
      "id": "T1",
      "label": "human-readable theme name",
      "gloss": "one sentence: what unifies this theme",
      "size": 0,
      "representative_event_ids": ["..."],
      "subclusters": [
        { "id": "T1.1", "label": "...", "gloss": "...", "event_ids": ["..."] }
      ]
    }
  ],
  "outliers": [ { "event_id": "...", "why": "why it fits no theme — often why it is interesting" } ]
}
```

### Soft affinities — `affinities.json`

```json
{
  "generated_on": "YYYY-MM-DD",
  "top_k": 3,
  "affinities": {
    "<event_id>": [ { "theme_id": "T1", "affinity": 0.0 }, { "theme_id": "T4", "affinity": 0.0 } ]
  }
}
```

Every event appears in `affinities` with its top-k theme affinities (descending). An outlier still gets affinities — its top affinity is just low, which is exactly what marks it as an outlier.

## Common Patterns

### Pattern 1: The embed → reduce → cluster → label pipeline

When embedding libraries are available (`resources/cluster.py`):

1. **Embed** each event's text (enriched abstract if present, else raw abstract + title + topics) into a vector. Text embeddings, not an LLM call per item.
2. **Reduce** dimensionality (UMAP) so density structure is visible.
3. **Density-cluster** (HDBSCAN) — it groups what is dense and **leaves the rest as noise**, which becomes the outlier bucket. It does not force every point into a cluster.
4. **Label** each resulting cluster with an LLM: read the representative members, write the `label` + `gloss`. This is the *only* LLM step in the grouping, and it touches clusters, not items.

The division of labor is the whole point: the deterministic step decides *who is grouped with whom* (stable, cheap), the language step decides *what to call the group* (fluent, human).

### Pattern 2: Coarse first, then fine

Aim for **6–8 coarse themes** — few enough to hold in your head and to ground elicitation questions in. Get the coarse layer by clustering at low resolution (or merging fine clusters up). Then, within each coarse theme, expose **sub-clusters** for the talks that share a tighter sub-topic. Do not ship 20 flat clusters: at that resolution the boundaries blur and the elicitor cannot present a clean "A vs B" contrast. Coarse-with-drill-down beats flat-and-many.

### Pattern 3: Keep the outliers as a first-class bucket

The talks that fit no dense region are not noise to be hidden — they are frequently the cross-disciplinary, against-the-grain sessions that a curious attendee most wants surfaced. Put them in `outliers` with a `why`, and make sure they survive into elicitation (the elicitor's selection-bias probes draw from exactly here). Forcing an outlier into the nearest theme both corrupts that theme and buries the talk.

### Pattern 4: Soft multi-membership, not a hard partition

A hard assignment says a talk is *only* about evaluation. Reality is fuzzier. Give every event its **top-k theme affinities** (k≈3): the cosine similarity to each theme centroid (or HDBSCAN soft-membership probabilities), normalized. Now "I'm interested in agents" and "I'm interested in evaluation" both surface the agentic-eval talk, instead of it hiding in whichever single bucket it landed. The coarse map stays clean for navigation; the affinities carry the overlap.

### Pattern 5: The LLM-reasoned fallback (no embedding libs)

When `sentence-transformers`/`umap-learn`/`hdbscan` are unavailable, or N is small enough that density clustering is unstable, cluster by reasoning over the already-extracted `axes.topic` and abstracts:

1. Group events by topic co-occurrence into ~6–8 coarse themes; name each.
2. Split each theme into sub-clusters by tighter sub-topic.
3. Mark as outliers the events whose topics match no theme well.
4. Assign top-k affinities by judged topical closeness to each theme's gloss (0–1).

Set `method: "llm-reasoned"` and a `stability_note` flagging that the grouping is reasoning-derived (less reproducible than embeddings). The fallback produces the same two output contracts — downstream stages cannot tell which method ran except by reading `method`.

### Pattern 6: Record the method and its stability

Always set `method` and write a `stability_note`: how reproducible the clusters are, and what would move a talk between themes. Clustering is a modeling choice, not ground truth; the note is what lets the elicitor and the human treat theme boundaries as provisional rather than as fact.

## Workflow

```
□ Step 1: Load events.json; assemble each event's text (enriched abstract ?? raw abstract + title + topics).
□ Step 2: Choose the method. Try resources/cluster.py (embed-hdbscan). On missing libs / tiny N, use the
          LLM-reasoned fallback. Record the choice in method.
□ Step 3: Produce the grouping — coarse clusters with a noise/outlier set.
□ Step 4: Collapse/merge to 6-8 coarse themes; expose sub-clusters inside each.
□ Step 5: LLM-label each coarse theme and sub-cluster (label + gloss) from representative members.
□ Step 6: Build the outlier bucket with a why per event.
□ Step 7: Compute top-k soft affinities for every event (including outliers).
□ Step 8: Write clusters.json + affinities.json + a human-readable clusters.md tour. Set stability_note.
```

## Guardrails

### 1. Embeddings group, the LLM only labels
**Danger**: Asking an LLM to assign every talk to a cluster — costly, and the assignment shifts run to run.
**Guardrail**: The grouping step is deterministic (embeddings/topics); the LLM names clusters, not items.
**Red flag**: A per-event LLM "which cluster?" call in the grouping loop.

### 2. Never drop the outliers
**Danger**: Forcing every talk into a theme corrupts the theme and hides the most interesting sessions.
**Guardrail**: Maintain `outliers` as a first-class bucket with a `why`; pass it forward.

### 3. Soft membership, not a hard partition
**Danger**: One-cluster-per-talk makes overlapping talks invisible to all but one interest.
**Guardrail**: Every event carries top-k affinities. The coarse map is for navigation; affinities carry the overlap.

### 4. Coarse before fine
**Danger**: 20 flat clusters blur boundaries and break clean elicitation contrasts.
**Guardrail**: 6–8 coarse themes, sub-clusters on demand.

### 5. Declare the method and its stability
**Danger**: Treating provisional clusters as ground truth.
**Guardrail**: Set `method` + `stability_note`; downstream stages treat boundaries as provisional.

### 6. Don't re-extract or schedule
**Danger**: Scope creep — re-deriving axes or making schedule picks.
**Guardrail**: Consume the EventRecords as given; output only the map + affinities.

## Quick Reference

### The pipeline at a glance

| Step | Operation | Who does it | Output |
|---|---|---|---|
| Embed | text → vector | embedding model | per-event vectors |
| Reduce | high-dim → low-dim | UMAP | reduced vectors |
| Cluster | density grouping | HDBSCAN | clusters + noise(outliers) |
| Label | name the cluster | LLM | label + gloss |
| Soft-assign | top-k affinities | cosine / soft-membership | affinities.json |

### Method choice

| Situation | Method | Note |
|---|---|---|
| Embedding libs present, N ≳ 30 | `embed-hdbscan` via `resources/cluster.py` | most stable |
| No libs, or N small | `llm-reasoned` fallback | record lower stability |
| Either | always | 6–8 coarse + sub-clusters + outliers + soft affinities |

## Related Skills

- **conf-program-extraction**: supplies the EventRecords (topics + abstracts) this skill clusters; multi-topic survival there enables soft membership here.
- **conf-preference-elicitation**: the primary consumer — it grounds choice-based questions in these coarse themes and draws selection-bias probes from the outlier bucket.
- **conf-schedule-optimization**: uses theme coverage (via affinities) to reward breadth in the objective.
- **abstraction-concrete-examples**: useful when writing theme glosses that name the abstraction yet point at concrete member talks.

## Examples in Context

### Example 1: A theme with a sub-cluster and an overlap

Coarse theme `T3` "Evaluation & Reliability" (gloss: "measuring whether agents/models actually work and keeping them working"), sub-cluster `T3.2` "Agent eval harnesses". The talk "Evaluating Agentic RAG" lands in `T3.2` by hard clustering — but its `affinities` are `[{T3,0.71},{T5_Agents,0.66},{T2_Retrieval,0.58}]`, so it also surfaces when the attendee says "I care about agents" or "I care about retrieval." The hard map stays clean; the soft affinities carry the truth.

### Example 2: A genuine outlier

"What Octopuses Teach Us About Distributed Cognition" matches no dense region. It goes to `outliers` with `why: "biology/cognition crossover; no topical neighbors in this program"`. It still gets affinities (top affinity ~0.3 to "Agents"), and the elicitor later offers it as a deliberate selection-bias probe — the kind of talk a narrowed model of the attendee would never surface on its own.

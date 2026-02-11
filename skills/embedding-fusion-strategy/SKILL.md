---
name: embedding-fusion-strategy
description: Use when designing embedding strategies that fuse semantic and structural information for knowledge graphs. Invoke when user mentions node embeddings, structural embeddings, semantic embeddings, contrastive alignment, embedding fusion, vector representations for graphs, or combining text and graph signals. Provides embedding selection, fusion design, and implementation guidance.
---

## Table of Contents
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Granularity Selection Guide](#granularity-selection-guide)
- [Fusion Approaches](#fusion-approaches)
- [Output Template](#output-template)

# Embedding Fusion Strategy

## What Is It?

This skill helps you **design embedding strategies that combine semantic (text-based) and structural (graph-based) information** at node, edge, path, and subgraph levels. Given a knowledge graph and a downstream task, it guides you through selecting the right embedding granularity, choosing complementary semantic and structural approaches, and designing a fusion strategy that captures both meaning and topology.

**The payoff**: Neither pure text embeddings nor pure graph embeddings capture complete entity meaning. Fusion bridges the symbolic and semantic worlds, enabling retrieval and reasoning that neither approach achieves alone.

## Workflow

**COPY THIS CHECKLIST** and work through each step:

```
Embedding Fusion Strategy Progress:
- [ ] Step 1: Identify available features and data sources
- [ ] Step 2: Determine task requirements and success criteria
- [ ] Step 3: Select granularity level(s)
- [ ] Step 4: Choose semantic embedding approach
- [ ] Step 5: Choose structural embedding approach
- [ ] Step 6: Design fusion strategy
- [ ] Step 7: Produce embedding strategy specification
```

**Step 1: Identify available features and data sources**

Inventory what signals exist in the knowledge graph: node text attributes (names, descriptions, types), edge labels and properties, graph topology (density, diameter, heterogeneity), any external text corpora or pre-trained models available. Understanding the raw material determines what embeddings are feasible. See [resources/methodology.md](resources/methodology.md) for the full taxonomy of embedding types.

**Step 2: Determine task requirements and success criteria**

Clarify the downstream task: entity retrieval, link prediction, question answering, node classification, recommendation, or subgraph matching. Each task favors different granularities and fusion approaches. Establish evaluation metrics (MRR, Hits@K, F1, latency budgets). See [resources/methodology.md](resources/methodology.md) for task-to-approach mapping and selection criteria.

**Step 3: Select granularity level(s)**

Choose which levels of the graph to embed using the [Granularity Selection Guide](#granularity-selection-guide). Many strategies combine multiple granularities (e.g., node embeddings for retrieval plus subgraph embeddings for re-ranking). See [resources/embedding-catalog.md](resources/embedding-catalog.md) for specific techniques at each level.

**Step 4: Choose semantic embedding approach**

Select how to capture text-based meaning: LLM encoder for rich contextual embeddings, Sentence-BERT for efficient sentence-level similarity, or text descriptions of neighborhoods for context-aware semantics. Match the approach to your computational budget and freshness requirements. See [resources/methodology.md](resources/methodology.md) for semantic approach details and trade-offs.

**Step 5: Choose structural embedding approach**

Select how to capture graph topology: Node2Vec for flexible neighborhood sampling, DeepWalk for uniform random walks, GraphSAGE for inductive learning on unseen nodes, or positional encodings for capturing graph roles. Match the approach to your graph density and update frequency. See [resources/embedding-catalog.md](resources/embedding-catalog.md) for the full structural technique catalog.

**Step 6: Design fusion strategy**

Combine semantic and structural embeddings using one of the [Fusion Approaches](#fusion-approaches). Key decisions: early vs. late fusion, alignment training, dimensionality management, and whether to maintain multiple vectors per entity. See [resources/methodology.md](resources/methodology.md) for detailed fusion design methodology, including dynamic vs. static trade-offs and storage considerations.

**Step 7: Produce embedding strategy specification**

Document the complete design using the [Output Template](#output-template). Include embedding dimensions, training procedures, indexing strategy, and update mechanisms. Self-assess using [resources/evaluators/rubric_embedding_strategy.json](resources/evaluators/rubric_embedding_strategy.json). Minimum standard: Average score >= 3.0.

## Granularity Selection Guide

| Granularity | Description | Use Cases |
|-------------|-------------|-----------|
| **Node** | Embed individual entities combining their text attributes with local structural context | Entity retrieval, node classification, entity linking, recommendation |
| **Edge** | Embed relationships including relation type, endpoint context, and edge properties | Link prediction, relation classification, triple verification |
| **Path** | Embed sequences of nodes and edges capturing multi-hop patterns and metapath semantics | Multi-hop reasoning, pathway discovery, explainable retrieval |
| **Subgraph** | Embed local neighborhoods (ego-networks, motifs) capturing community structure | Subgraph matching, anomaly detection, community-aware retrieval |
| **Community** | Embed clusters or partitions summarizing high-level graph regions | Topic modeling, coarse-grained search, hierarchical navigation |

## Fusion Approaches

### Concatenation

Combine semantic and structural vectors by concatenation: `v_fused = [v_semantic; v_structural]`. Simple and preserves all information, but doubles dimensionality and treats both signals as independent.

**When to use**: Baseline approach, fast prototyping, when downstream model can learn weighting.

### Attention-Based Fusion

Learn a weighting over semantic and structural components: `v_fused = alpha * v_semantic + (1 - alpha) * v_structural`, where alpha is learned per entity or per query. Allows the model to emphasize the most informative signal.

**When to use**: When relative importance of semantic vs. structural varies across entities or queries.

### Contrastive Alignment

Train semantic and structural embeddings to coincide for the same entity using contrastive loss (e.g., InfoNCE). Produces a shared embedding space where both views agree. Enables cross-modal retrieval.

**When to use**: When you want a single unified space, cross-modal search, or when training data for alignment is available.

### Late Fusion / Re-Ranking

Use bi-encoder (separate semantic and structural retrieval) followed by cross-encoder re-ranking that considers both signals jointly. Separates fast candidate generation from precise scoring.

**When to use**: Large-scale retrieval where full fusion at query time is too expensive; when latency budget allows two-stage pipeline.

### Multi-Vector Representation

Maintain multiple embeddings per entity (semantic facets, structural roles, contextual variants). Match queries against the most relevant facet using max-sim or attention pooling.

**When to use**: Entities with multiple roles or meanings, faceted search, when a single vector loses too much information.

## Output Template

```
EMBEDDING STRATEGY SPECIFICATION
=================================

Domain: [Knowledge graph domain and scale]
Task: [Primary downstream task(s)]
Success Metrics: [MRR, Hits@K, latency, etc.]

Granularity Level(s): [Node / Edge / Path / Subgraph / Community]

Semantic Approach:
  - Method: [LLM encoder / Sentence-BERT / Description-based / etc.]
  - Input: [What text is embedded]
  - Dimension: [embedding size]
  - Model: [specific model name/version]
  - Update frequency: [static / periodic / real-time]

Structural Approach:
  - Method: [Node2Vec / DeepWalk / GraphSAGE / Positional / etc.]
  - Parameters: [walk length, dimensions, neighborhood size, etc.]
  - Dimension: [embedding size]
  - Update frequency: [static / periodic / incremental]

Fusion Strategy:
  - Method: [Concatenation / Attention / Contrastive / Late Fusion / Multi-Vector]
  - Final dimension: [fused embedding size]
  - Alignment training: [loss function, training procedure if applicable]
  - Rationale: [why this fusion approach for this task]

Indexing & Storage:
  - Index type: [HNSW / IVF / flat / etc.]
  - Vector database: [if applicable]
  - Approximate nearest neighbor parameters: [ef, nprobe, etc.]
  - Storage estimate: [total size]

Update & Maintenance:
  - Recomputation strategy: [full retrain / incremental / streaming]
  - Staleness tolerance: [how old before recompute]
  - Incremental update mechanism: [if applicable]

NEXT STEPS:
- Implement embedding pipeline
- Train fusion/alignment if applicable
- Build ANN index and benchmark retrieval quality
- Validate end-to-end on downstream task
- Monitor embedding drift in production
```

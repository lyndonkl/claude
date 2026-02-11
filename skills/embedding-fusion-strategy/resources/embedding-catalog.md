# Embedding Technique Catalog

> This resource supports **Steps 3-5** of the [Embedding Fusion Strategy](../SKILL.md) workflow.

## WHY

Choosing the right embedding technique for each granularity level is a critical design decision that affects retrieval quality, computational cost, and system complexity. This catalog provides a quick reference for selecting specific techniques based on the granularity level, the signals you need to capture, and your operational constraints.

Without a systematic reference, practitioners often default to the most familiar technique (typically Node2Vec or a generic sentence encoder) when a different approach would be significantly more effective for their specific task and graph structure.

---

## WHAT

### 1. Node-Level Techniques

#### Node2Vec

**How it works**: Performs biased random walks on the graph, then trains Skip-gram embeddings on the walk sequences. Parameters p (return parameter) and q (in-out parameter) control the walk behavior.

- **p < 1**: Encourages backtracking, captures local structure (BFS-like)
- **q < 1**: Encourages exploring outward, captures community structure (DFS-like)

**Captures**: Local and global neighborhood structure, homophily and structural equivalence (tunable via p, q).

**Computational cost**: Moderate. Walk generation is O(num_walks * walk_length * N). Training is standard word2vec.

**Best for**: Static graphs where you want tunable structural embeddings. Good baseline for most graph embedding tasks.

**Limitations**: Transductive (cannot embed unseen nodes without retraining). No direct use of node features. Embedding quality depends on walk hyperparameters.

#### DeepWalk

**How it works**: Uniform random walks followed by Skip-gram training. Equivalent to Node2Vec with p=1, q=1.

**Captures**: Community structure via co-occurrence in random walks. Approximates a specific matrix factorization of the graph.

**Computational cost**: Moderate. Slightly faster than Node2Vec (no bias computation).

**Best for**: Simple baseline, undirected graphs, when Node2Vec hyperparameter tuning is not feasible.

**Limitations**: Same as Node2Vec (transductive, no features). Less flexible than Node2Vec due to uniform walks. May miss fine-grained structural roles.

#### GraphSAGE

**How it works**: Samples a fixed-size neighborhood for each node, aggregates neighbor features through learned aggregation functions (mean, LSTM, or pooling), and produces a node embedding. Trained with a graph-based loss (link prediction or node classification).

**Captures**: Local neighborhood features inductively. Can incorporate node text features as input.

**Computational cost**: Higher than walk-based methods (requires neural network training). Inference is fast once trained.

**Best for**: Dynamic graphs with new nodes, when node features are available, when inductive capability is needed.

**Limitations**: Sampling introduces variance. Deep aggregation (>3 hops) can cause over-smoothing. Requires feature vectors on nodes.

#### LINE (Large-scale Information Network Embedding)

**How it works**: Optimizes two objectives: first-order proximity (direct connections) and second-order proximity (shared neighbors). Concatenates both for final embedding.

**Captures**: First-order: direct link structure. Second-order: neighborhood similarity.

**Computational cost**: Low to moderate. Scales to very large graphs via edge sampling.

**Best for**: Very large-scale graphs where walk-based methods are too slow. When you want explicit control over first vs. second order signal.

**Limitations**: Only captures up to second-order proximity. No higher-order structural patterns. Transductive.

#### TransE

**How it works**: Models relations as translations in embedding space. For a triple (h, r, t), optimizes h + r approximately equals t. Learns entity and relation embeddings jointly.

**Captures**: Relational structure in knowledge graphs. Handles composition patterns.

**Computational cost**: Low. Simple scoring function enables fast training.

**Best for**: Knowledge graph completion, link prediction, simple relational patterns (one-to-one).

**Limitations**: Cannot model symmetric, reflexive, or one-to-many relations well. Limited expressiveness compared to RotatE.

#### RotatE

**How it works**: Models relations as rotations in complex vector space. For a triple (h, r, t), optimizes h * r approximately equals t (element-wise complex multiplication).

**Captures**: Symmetry, antisymmetry, inversion, and composition relation patterns. More expressive than TransE.

**Computational cost**: Low to moderate. Complex number operations add slight overhead.

**Best for**: Knowledge graph completion with diverse relation types. When the graph has symmetric and antisymmetric relations.

**Limitations**: Still limited to pairwise interactions. Does not capture complex multi-hop patterns directly.

---

### 2. Edge-Level Techniques

#### Triple Embeddings (Text-Based)

**How it works**: Linearize a triple as text ("Drug_A treats Disease_B") and encode with a language model. Each edge gets a unique text-based embedding.

**Captures**: The specific semantic meaning of the relationship in context. Disambiguates edges with the same relation type but different endpoints.

**Computational cost**: High (one LLM call per edge). Can be batched.

**Best for**: Relation classification, triple verification, semantic search over relationships.

**Limitations**: Expensive at scale. Does not capture structural context beyond the immediate triple.

#### Relation Type Embeddings

**How it works**: Embed the relation label (e.g., "treats", "authored_by") using a text encoder. All edges of the same type share the embedding.

**Captures**: The semantic meaning of the relation type. Enables relation clustering and type-aware retrieval.

**Computational cost**: Very low (one embedding per relation type, typically < 100 types).

**Best for**: Relation type classification, filtering edges by semantic type, type-aware graph traversal.

**Limitations**: Does not distinguish between specific instances of the same relation type. Misses endpoint context.

#### Contextualized Edge Embeddings

**How it works**: Combine endpoint embeddings with relation embedding: `v_edge = f(v_head, v_relation, v_tail)` where f is concatenation, addition, or a learned function.

**Captures**: The full context of the edge including both endpoints and the relation.

**Computational cost**: Moderate (depends on endpoint embedding method and combination function).

**Best for**: Link prediction, edge classification, when edge meaning depends on both endpoints.

**Limitations**: Requires pre-computed endpoint embeddings. Combination function must be designed carefully.

---

### 3. Path-Level Techniques

#### Metapath2Vec

**How it works**: Performs random walks constrained to follow a predefined metapath schema in heterogeneous graphs (e.g., Author-Paper-Venue-Paper-Author). Then trains Skip-gram on the typed walk sequences.

**Captures**: Type-level connectivity patterns. Relationships between entities connected through specific semantic paths.

**Computational cost**: Moderate. Walk generation constrained by metapath schema. Multiple metapaths may require separate training runs.

**Best for**: Heterogeneous graphs with meaningful type-level paths. Academic networks, biomedical knowledge graphs.

**Limitations**: Requires domain expertise to define meaningful metapaths. Cannot discover unexpected paths. Separate embeddings per metapath must be combined.

#### Path Linearization + LLM Encoding

**How it works**: Convert a graph path to a natural language sequence ("Drug_A inhibits Gene_B, which is expressed_in Tissue_C, which is affected_by Disease_D") and encode with a language model.

**Captures**: Multi-hop reasoning narrative. Semantic meaning of the path in natural language.

**Computational cost**: High (LLM call per path). Paths can be long, consuming context window.

**Best for**: Explainable retrieval, multi-hop question answering, when paths need to be human-interpretable.

**Limitations**: Context window limits path length. Quality depends on linearization template. Expensive at scale.

#### Path2Vec

**How it works**: Learn embeddings for paths based on their structural properties (length, node degrees along the path, relation sequence). Treats paths as first-class objects.

**Captures**: Structural path patterns independent of specific endpoints.

**Computational cost**: Low to moderate.

**Best for**: Path classification, comparing paths structurally, identifying path patterns.

**Limitations**: Does not capture semantic meaning of path endpoints. Less commonly used than node-level methods.

---

### 4. Subgraph-Level Techniques

#### Ego-Network Pooling

**How it works**: Extract the k-hop neighborhood around a target node, apply a GNN or text summarization to the subgraph, and pool node embeddings into a single subgraph vector.

**Captures**: Local community structure, neighborhood composition, entity context.

**Computational cost**: Moderate to high. Depends on k (hop radius) and neighborhood size.

**Best for**: Context-aware entity retrieval, entity disambiguation, when local structure is informative.

**Limitations**: k-hop neighborhoods can be very large in dense graphs (requires sampling). Over-smoothing with large k.

#### Community Summarization + Encoding

**How it works**: Detect communities using graph clustering (Louvain, label propagation, spectral clustering). Summarize each community (member types, key entities, internal density) as text. Encode the summary with a language model.

**Captures**: High-level thematic structure, topical regions of the graph.

**Computational cost**: Moderate (community detection + one embedding per community).

**Best for**: Hierarchical navigation, topic-level search, coarse-grained retrieval before fine-grained refinement.

**Limitations**: Community detection is non-deterministic. Summary quality depends on verbalization strategy. Misses cross-community structure.

#### GNN-Based Subgraph Embeddings

**How it works**: Apply a GNN (GIN, GAT, or GraphSAGE) to the subgraph and use graph-level readout (sum, mean, or attention pooling over node embeddings) to produce a single vector.

**Captures**: Structural patterns within the subgraph, motifs, roles.

**Computational cost**: High (full GNN forward pass per subgraph).

**Best for**: Subgraph classification, subgraph matching, chemical compound embedding, when structural motifs matter.

**Limitations**: Requires defining subgraph boundaries. Training requires labeled subgraph data or self-supervised objectives.

---

### 5. Comparison Table

| Technique | Granularity | Captures | Computational Cost | Best For | Limitations |
|-----------|-------------|----------|-------------------|----------|-------------|
| Node2Vec | Node | Local/global structure (tunable) | Moderate | Static graphs, tunable neighborhoods | Transductive, no features |
| DeepWalk | Node | Community co-occurrence | Moderate | Simple baseline | Less flexible than Node2Vec |
| GraphSAGE | Node | Neighborhood features (inductive) | Higher | Dynamic graphs, feature-rich nodes | Sampling variance, over-smoothing |
| LINE | Node | First/second order proximity | Low-Moderate | Very large graphs | Limited to second-order |
| TransE | Node + Edge | Relational translations | Low | KG completion, one-to-one relations | Limited relation patterns |
| RotatE | Node + Edge | Relational rotations | Low-Moderate | KG completion, diverse relations | Pairwise interactions only |
| Triple embedding | Edge | Specific relationship semantics | High | Relation classification, verification | Expensive at scale |
| Relation type emb. | Edge | Relation type semantics | Very Low | Type-aware filtering | No instance distinction |
| Contextualized edge | Edge | Full edge context | Moderate | Link prediction, edge classification | Requires endpoint embeddings |
| Metapath2Vec | Path | Typed connectivity patterns | Moderate | Heterogeneous graphs | Requires metapath design |
| Path linearization | Path | Multi-hop narrative | High | Explainable retrieval, QA | Context window limits, costly |
| Path2Vec | Path | Structural path patterns | Low-Moderate | Path classification | No semantic content |
| Ego-network pooling | Subgraph | Local community context | Moderate-High | Context-aware retrieval | Large neighborhoods in dense graphs |
| Community summary | Community | Thematic regions | Moderate | Hierarchical search, topic modeling | Non-deterministic clustering |
| GNN subgraph emb. | Subgraph | Structural motifs | High | Subgraph matching, motif detection | Requires labeled data or SSL |

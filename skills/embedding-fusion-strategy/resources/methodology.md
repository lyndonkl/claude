# Embedding Fusion Strategy Methodology

> This resource supports **Steps 1-6** of the [Embedding Fusion Strategy](../SKILL.md) workflow.

## WHY

Neither pure text embeddings nor pure graph embeddings capture complete entity meaning in a knowledge graph.

**Text embeddings** (semantic) capture linguistic meaning, synonymy, and contextual nuance but are blind to graph topology. Two entities with identical descriptions but completely different structural roles (hub vs. leaf, bridging node vs. cluster member) get identical embeddings.

**Graph embeddings** (structural) capture connectivity patterns, neighborhood similarity, and topological roles but ignore the rich textual attributes that distinguish otherwise structurally similar nodes. Two nodes with identical degree distributions but describing completely different concepts get similar embeddings.

**Fusion bridges the symbolic and semantic worlds.** By combining both signals, the resulting embeddings capture what an entity means (semantics) and where it sits in the knowledge structure (topology). This enables retrieval and reasoning that neither approach achieves alone: finding structurally relevant entities that are also semantically appropriate.

---

## WHAT

### 1. Embedding Types by Granularity

#### 1.1 Node Embeddings (Section 2.1)

Node embeddings combine per-entity semantic text with structural neighborhood information.

**Semantic component**: Encode the node's text attributes (name, description, type label, associated documents) using a language model. The text can range from a simple label to a rich description incorporating neighborhood context (e.g., "Drug X, which treats Disease Y and interacts with Protein Z").

**Structural component**: Capture the node's position and role in the graph using random-walk methods (Node2Vec, DeepWalk), message-passing aggregation (GraphSAGE), or positional encodings (Laplacian eigenvectors, random walk probabilities).

**Combined**: The fused node embedding should reflect both what the entity is (semantic) and how it connects (structural).

#### 1.2 Edge and Relation Embeddings (Section 2.2)

Edges carry information beyond their endpoints. Three approaches:

- **Relation type embeddings**: Embed the relation label (e.g., "treats", "inhibits", "co-authored") using a text encoder. All edges of the same type share this embedding. Useful for relation classification and type-aware retrieval.
- **Specific edge embeddings**: Embed the full triple as text ("Drug_A treats Disease_B") to capture the specific relationship instance. Each edge gets a unique embedding.
- **Triple embeddings**: Concatenate or combine head entity, relation, and tail entity embeddings. Compatible with KG embedding methods like TransE and RotatE that learn relation-specific transformations.

#### 1.3 Path and Metapath Embeddings (Section 2.3)

Paths capture multi-hop reasoning patterns that single nodes or edges miss.

- **Path encoding**: Linearize a path (node1 -> edge1 -> node2 -> edge2 -> node3) into a text sequence and encode with an LLM. Captures the narrative of how entities connect.
- **Metapath typed patterns**: Define typed path schemas (e.g., Author-Paper-Venue in academic graphs, Drug-Gene-Disease in biomedical graphs). These capture domain-specific reasoning patterns.
- **Metapath2Vec**: Random walks constrained to follow metapath schemas in heterogeneous graphs. Produces embeddings that respect type-level connectivity patterns.

#### 1.4 Subgraph and Community Embeddings (Section 2.4)

Local and global graph structure beyond individual nodes.

- **Ego-network embedding**: Extract the k-hop neighborhood around a node, summarize it (via text description or GNN pooling), and embed. Captures local community context.
- **Community embedding**: Detect communities (Louvain, label propagation) and embed each community as a unit, using member summaries or aggregated member embeddings.
- **Motif embedding**: Identify recurring subgraph patterns (triangles, stars, chains) and embed them. Captures structural roles and functional modules.

### 2. Semantic Embedding Approaches

#### 2.1 LLM Encoder

Use a large language model (GPT, LLaMA, etc.) to produce contextual embeddings of entity descriptions. Produces high-quality, nuanced representations but is computationally expensive and may require API calls.

**Best for**: Rich text attributes, entities with complex descriptions, when quality matters more than cost.

**Trade-offs**: High quality but high latency and cost. Static once computed. May not capture domain-specific terminology without fine-tuning.

#### 2.2 Sentence-BERT / Bi-Encoder Models

Use specialized sentence embedding models (all-MiniLM, BGE, GTE, E5) that produce fixed-size embeddings optimized for similarity. Efficient inference, good quality for sentence-level comparison.

**Best for**: Medium-scale systems, when embedding speed matters, when similarity search is the primary use case.

**Trade-offs**: Good balance of quality and speed. Fine-tuning on domain data significantly improves quality. Smaller models may miss subtle distinctions.

#### 2.3 Text Descriptions of Neighborhoods

Instead of embedding only the node's own text, construct a text description that incorporates neighborhood information: "Entity X is connected to Y, Z, and W via relationships R1, R2, R3." Then embed this enriched text.

**Best for**: Injecting structural information into the semantic channel. Particularly useful when the structural embedding is weak or unavailable.

**Trade-offs**: Elegant fusion of structure into text, but limited by context window size. Quality depends on how well the neighborhood can be verbalized.

### 3. Structural Embedding Approaches

#### 3.1 Random Walk Methods

**Node2Vec**: Biased random walks with parameters p (return) and q (in-out) that control exploration vs. exploitation. Setting q < 1 favors BFS-like local exploration (captures structural equivalence); setting q > 1 favors DFS-like distant exploration (captures homophily).

**DeepWalk**: Uniform random walks followed by Skip-gram training. Simpler than Node2Vec but often competitive. Good baseline.

**Parameters**: Walk length (typically 10-80), number of walks per node (10-40), embedding dimension (64-256), window size (5-10).

#### 3.2 Message-Passing / GNN-Based

**GraphSAGE**: Sample and aggregate neighborhoods inductively. Can produce embeddings for unseen nodes (critical for dynamic graphs). Learns aggregation functions (mean, LSTM, pool) over sampled neighborhoods.

**Key advantage**: Inductive -- works on new nodes without retraining the full model. Suitable for graphs with frequent additions.

**Trade-offs**: Requires feature vectors on nodes (can use text embeddings as input features). Training is more complex than random walk methods.

#### 3.3 Position-Based Encodings

**Laplacian positional encoding**: Use eigenvectors of the graph Laplacian as node features. Captures global graph structure and spectral properties.

**Random walk positional encoding**: Use landing probabilities of random walks of different lengths as features. Captures multi-scale structural context.

**Best for**: Augmenting GNN inputs, capturing global position, graph transformer architectures.

#### 3.4 Knowledge Graph Embedding Methods

**TransE**: Models relations as translations in embedding space (h + r = t). Simple, effective for one-to-one relations.

**RotatE**: Models relations as rotations in complex space. Handles symmetry, antisymmetry, inversion, and composition patterns.

**Best for**: Knowledge graph completion, link prediction, triple classification. These methods jointly learn entity and relation embeddings.

### 4. Fusion Approaches in Detail

#### 4.1 Concatenation

```
v_fused = [v_semantic; v_structural]
dim(v_fused) = dim(v_semantic) + dim(v_structural)
```

**Pros**: Simple, preserves all information, no training required.
**Cons**: Doubles dimensionality, no learned interaction between signals, downstream model must learn weighting.
**Mitigation**: Apply a learned projection layer to reduce dimensionality after concatenation.

#### 4.2 Attention-Based Fusion

```
alpha = sigmoid(W_a * [v_semantic; v_structural] + b_a)
v_fused = alpha * W_s * v_semantic + (1 - alpha) * W_t * v_structural
```

**Pros**: Learns per-entity or per-query weighting. Adapts to entities where one signal is more informative.
**Cons**: Requires training data and supervision signal. More complex pipeline.
**Variant**: Multi-head attention over different embedding facets.

#### 4.3 Contrastive Alignment (Section 2.5)

Train two encoders to produce embeddings that agree for the same entity and disagree for different entities:

```
L = -log(exp(sim(v_sem_i, v_str_i) / tau) / sum_j(exp(sim(v_sem_i, v_str_j) / tau)))
```

**Pros**: Produces a unified space. Enables cross-modal retrieval (query with text, retrieve by structure or vice versa).
**Cons**: Requires careful negative sampling. Contrastive training can be unstable. Alignment may lose modality-specific information.
**Best practice**: Use hard negatives (structurally similar but semantically different entities, and vice versa).

#### 4.4 Late Fusion / Re-Ranking (Section 2.5)

Two-stage pipeline:

1. **Stage 1 (Bi-encoder)**: Retrieve top-K candidates independently using semantic and structural embeddings. Merge candidate lists.
2. **Stage 2 (Cross-encoder)**: Re-rank merged candidates using a model that jointly considers both signals for the query-candidate pair.

**Pros**: Scalable (bi-encoder handles millions), precise (cross-encoder handles hundreds). Separates recall from precision optimization.
**Cons**: Two models to maintain. Latency from two-stage pipeline. Cross-encoder is expensive per pair.

#### 4.5 Multi-Vector Representation

Maintain N embeddings per entity, each capturing a different facet:

- Semantic embedding (what it means)
- Structural role embedding (hub, bridge, leaf)
- Contextual embedding per relation type
- Community membership embedding

**Retrieval**: Use max-sim (maximum similarity across facets) or attention-weighted aggregation at query time.

**Pros**: Captures entity polysemy and multi-faceted nature. No information loss from compression.
**Cons**: N times storage and index complexity. Query-time aggregation adds latency.

#### 4.6 Query Enrichment (Section 2.5)

Instead of fusing entity embeddings, use graph structure to expand the query before embedding:

1. Embed the query text
2. Retrieve initial candidates
3. Expand query using graph neighbors of initial candidates
4. Re-embed expanded query
5. Retrieve final results

**Pros**: No changes to entity embeddings. Graph signal injected at query time.
**Cons**: Multiple retrieval rounds. May introduce noise from irrelevant neighbors.

### 5. Selection Criteria

#### 5.1 By Task Type

| Task | Recommended Granularity | Recommended Fusion |
|------|------------------------|--------------------|
| Entity retrieval | Node | Contrastive alignment or late fusion |
| Link prediction | Edge + Node | Concatenation with learned projection |
| Multi-hop QA | Path + Node | Late fusion with path re-ranking |
| Node classification | Node | Attention-based fusion |
| Recommendation | Node + Community | Multi-vector with community facet |
| Subgraph matching | Subgraph | Contrastive alignment at subgraph level |

#### 5.2 By Graph Characteristics

| Characteristic | Implication | Recommendation |
|----------------|-------------|----------------|
| Dense graph (high avg degree) | Rich structural signal | Weight structural embedding higher |
| Sparse graph (low avg degree) | Weak structural signal | Weight semantic embedding higher, use text neighborhood descriptions |
| Heterogeneous (multiple node/edge types) | Type information matters | Use metapath embeddings, type-aware structural methods |
| Dynamic (frequent updates) | Embeddings stale quickly | Use inductive methods (GraphSAGE), incremental updates |
| Large scale (millions of nodes) | Computational budget constrained | Use efficient bi-encoders, late fusion, approximate methods |

#### 5.3 By Computational Budget

| Budget | Semantic | Structural | Fusion |
|--------|----------|-----------|--------|
| Low | Sentence-BERT (small) | Node2Vec | Concatenation |
| Medium | Sentence-BERT (large) or fine-tuned | GraphSAGE | Attention-based |
| High | LLM encoder | GNN ensemble | Contrastive alignment + late fusion |

### 6. Dynamic vs. Static Embeddings

**Static embeddings**: Computed once (or periodically) and stored. Fast retrieval but can become stale as the graph evolves.

- Suitable for: Slowly changing graphs, batch processing pipelines
- Update strategy: Periodic full recomputation (weekly/monthly)

**Dynamic / incremental embeddings**: Updated as the graph changes. More accurate but computationally expensive.

- Suitable for: Rapidly evolving graphs, real-time applications
- Update strategy: Incremental retraining (GraphSAGE), delta updates for random walk methods, streaming contrastive learning
- Trade-off: Freshness vs. stability. Frequent updates can cause embedding drift.

### 7. Storage and Indexing Considerations

#### 7.1 Vector Database Integration

Store fused embeddings in a vector database (Pinecone, Weaviate, Milvus, Qdrant, pgvector) for efficient approximate nearest neighbor (ANN) retrieval.

**Key parameters**:
- **HNSW**: ef_construction (build quality, 100-400), M (connections per node, 16-64), ef_search (query quality, 50-200)
- **IVF**: nlist (number of clusters, sqrt(N) to 4*sqrt(N)), nprobe (clusters to search, 1-20% of nlist)

#### 7.2 Storage Estimation

```
Storage = num_entities * embedding_dim * bytes_per_float * num_vectors_per_entity
Example: 1M entities * 768 dim * 4 bytes * 1 vector = ~3 GB
With multi-vector (3 facets): ~9 GB
```

#### 7.3 Index Selection

| Scale | Recommended Index | Trade-off |
|-------|-------------------|-----------|
| < 100K entities | Flat (exact) | Perfect recall, fast enough |
| 100K - 10M entities | HNSW | Good recall (>95%), fast queries |
| > 10M entities | IVF-PQ or IVF-HNSW | Compressed, fast, some recall loss |

#### 7.4 Metadata Filtering

Combine vector search with metadata filters (entity type, timestamp, properties) to narrow the search space. Most vector databases support hybrid filtering.

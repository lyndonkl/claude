# GraphRAG System Design Methodology

> This resource supports **Steps 1-4** of the [GraphRAG System Design](../SKILL.md) workflow.

## WHY: The Case for GraphRAG

Standard vector-based RAG systems treat documents as isolated chunks, losing the relational structure that connects entities, events, and concepts. This creates fundamental limitations:

- **Multi-hop reasoning fails**: A query like "What drugs interact with medications prescribed to patients with condition X?" requires traversing patient-condition-medication-interaction paths that flat retrieval cannot assemble.
- **Entity disambiguation breaks**: When "Apple" appears in retrieved chunks, vector search cannot distinguish the company from the fruit without structural context.
- **Provenance is lost**: Flat retrieval returns chunks without the relationship chains that explain why information is relevant, making it impossible to verify reasoning paths.
- **Global queries have no anchor**: Questions like "What are the major themes across this corpus?" require aggregation structure that individual chunk retrieval cannot provide.

GraphRAG addresses these limitations by adding relational structure to retrieval. The knowledge graph provides multi-hop traversal paths, entity disambiguation through typed relationships, provenance chains from source documents through extraction to graph nodes, and community structure for corpus-level summarization.

**When GraphRAG adds value over standard RAG:**
- Queries require connecting information across multiple documents or entities
- Domain has rich relational structure (medical ontologies, corporate hierarchies, citation networks)
- Explainability and provenance are requirements, not nice-to-haves
- Entity disambiguation is critical (legal entities, medical terms, technical concepts)
- Users need both precise structural queries and fuzzy semantic search

**When standard RAG may suffice:**
- Queries are primarily single-hop factual lookups
- Data is unstructured with minimal relational structure
- Latency requirements are extremely tight (sub-100ms)
- Budget and team expertise do not support graph infrastructure

## WHAT: GraphRAG Patterns and Architecture

### Pattern 1: Hybrid Symbol-Vector

The Hybrid Symbol-Vector pattern combines graph traversal for structural precision with vector search for semantic flexibility. This is the integration pattern described in Section 1.6 of the GraphRAG literature as the convergence of symbolic AI and neural approaches.

**Mechanism:**

Two primary strategies exist for combining graph and vector retrieval:

**Strategy A -- Graph-first (pre-filter then rank):**
1. Parse the query to identify entity types, constraints, and structural requirements
2. Execute a graph query to retrieve a candidate set (e.g., all drugs treating condition X)
3. Embed the query and the candidate entities
4. Rank candidates by embedding similarity to surface the most semantically relevant results
5. Expand top results via graph neighborhood to add relational context

**Strategy B -- Vector-first (broad search then expand):**
1. Embed the query and perform broad vector similarity search
2. Map retrieved chunks back to their source graph entities
3. Expand retrieved entities via graph traversal (neighbors, paths, communities)
4. Re-rank the expanded set using both semantic similarity and graph distance/centrality
5. Assemble context from the re-ranked, graph-enriched result set

**When to use which strategy:**
- Graph-first when queries have clear structural constraints ("drugs for diabetes that interact with metformin")
- Vector-first when queries are open-ended or semantically ambiguous ("recent advances in treatment")
- Both strategies can be combined with a query classifier that routes to the appropriate path

**Technology requirements:**
- Graph database with efficient traversal (Neo4j Cypher, TigerGraph GSQL)
- Vector database or graph-native vector index (Neo4j vector index, separate Pinecone/Weaviate)
- Query parser or classifier to determine routing strategy
- Embedding model aligned with domain vocabulary

### Pattern 2: Subgraph-on-Demand

The Subgraph-on-Demand pattern builds temporary, query-specific subgraphs rather than querying a single monolithic knowledge graph. This pattern reduces cost, keeps context focused, and enables real-time updates without full graph reconstruction.

**Mechanism:**
1. Receive query and identify seed entities (via NER, entity linking, or vector lookup)
2. Extract a local subgraph around seed entities (k-hop neighborhood, filtered by edge types)
3. Optionally embed the subgraph nodes and edges for within-subgraph ranking
4. Pass the focused subgraph as structured context to the LLM
5. Generate response grounded in the subgraph, with citations to specific nodes and edges

**Key design decisions:**
- **Neighborhood depth**: 1-hop for focused queries, 2-3 hops for multi-hop reasoning (beyond 3 hops, noise typically exceeds signal)
- **Edge filtering**: Not all relationship types are relevant to every query; filter by edge type to keep subgraphs focused
- **Subgraph size budget**: Define a maximum node/edge count that fits within LLM context limits
- **Caching**: Frequently requested subgraphs can be cached to reduce cold-start latency

**Advantages over monolithic retrieval:**
- Context is precisely scoped to the query, reducing noise
- Cost-effective: only the relevant portion of the graph is processed
- Updates are localized: changing one entity does not require re-indexing the entire graph
- Supports real-time graph updates since each query builds a fresh subgraph

**Technology requirements:**
- Graph database with efficient neighborhood extraction
- Entity linking service to map query terms to graph nodes
- Subgraph serialization format (JSON-LD, adjacency list, or natural language linearization)

### Pattern 3: Community-Based Global Summarization

The Community-Based Global Summarization pattern detects communities (clusters) in the knowledge graph, generates summaries for each community, and retrieves relevant communities before drilling into entity-level details. This is the core pattern behind Microsoft GraphRAG.

**Mechanism:**
1. Build the full knowledge graph from the corpus
2. Run community detection (Leiden algorithm, Louvain, or hierarchical clustering) to identify clusters of densely connected entities
3. Generate LLM-produced summaries for each community at multiple hierarchy levels
4. Embed community summaries in a vector index
5. At query time, retrieve the most relevant community summaries via vector search
6. Drill into the matched communities to retrieve specific entities and relationships
7. Generate response grounded in both community-level themes and entity-level details

**Hierarchical community structure:**
- Level 0 (finest): Small clusters of 5-20 tightly connected entities
- Level 1 (medium): Merged clusters of 50-200 entities sharing thematic coherence
- Level 2 (coarsest): Broad thematic areas spanning hundreds of entities
- Query routing: Broad queries hit higher levels; specific queries hit lower levels

**Key design decisions:**
- **Community detection algorithm**: Leiden for quality, Louvain for speed, hierarchical for multi-level
- **Summary generation**: LLM summarizes each community's entities and relationships into a coherent paragraph
- **Update strategy**: Communities must be re-detected periodically (batch process); incremental updates to summaries when entities change
- **Level selection**: Query classifier determines which hierarchy level to search

**Advantages:**
- Handles global queries ("What are the major themes?") that defeat entity-level retrieval
- Provides corpus-level understanding without processing all documents
- Hierarchical structure supports both broad exploration and focused drill-down

**Technology requirements:**
- Graph database with community detection support (Neo4j GDS library, NetworkX)
- LLM for community summary generation (batch process)
- Vector index for community summary embeddings
- Batch processing infrastructure for periodic community re-detection

### System Architecture Design Considerations

**Graph-first vs text-first pipeline decision:**

The fundamental architectural choice is whether the graph or the text corpus is the primary source of truth for retrieval.

- **Graph-first**: Queries hit the knowledge graph first; text chunks are retrieved only to provide supporting detail for graph-retrieved entities. Best when the domain has well-defined entity types and relationships.
- **Text-first**: Queries hit the vector store first; the graph provides post-retrieval enrichment and context expansion. Best when queries are primarily semantic and the graph adds supplementary structure.

**Single-system vs multi-system hybrid:**

- **Single-system** (e.g., Neo4j with native vector index): Simpler deployment, atomic transactions across graph and vector, lower operational overhead. Limited by the vector search capabilities of the graph database.
- **Multi-system** (e.g., Neo4j + Pinecone): Best-of-breed for each component, independent scaling, richer vector search features. Requires synchronization logic to keep graph and vector indices consistent.

**Custom pipeline vs framework-based:**

- **LangChain/LlamaIndex**: Rapid prototyping, pre-built graph integrations (GraphQAChain, KnowledgeGraphIndex, PropertyGraphIndex), community support. May require workarounds for advanced patterns.
- **Custom pipeline**: Maximum control over retrieval logic, query routing, and context assembly. Higher development cost but avoids framework limitations. Recommended for production systems with complex requirements.

**Real-time vs batch processing:**

- **Real-time ingestion**: New documents are extracted, graph-updated, and indexed continuously. Essential for applications where data freshness matters (news, clinical data, financial events).
- **Batch processing**: Documents are processed in scheduled batches. Simpler to implement, allows quality validation between batches. Sufficient for stable corpora (legal codes, research literature).

**Graph maintenance and update strategy:**

- **Incremental updates**: Add/modify/delete specific nodes and edges without rebuilding the full graph. Requires entity resolution to merge new extractions with existing nodes.
- **Full rebuild**: Periodically reconstruct the entire graph from source data. Simpler but expensive; necessary when extraction methods improve significantly.
- **Schema evolution**: Plan for adding new node/edge types as requirements evolve. Graph databases handle schema evolution more flexibly than relational databases.

### Integration Pipeline Stages

The end-to-end GraphRAG pipeline follows seven stages:

**1. Ingest**
- Collect raw data from sources (documents, APIs, databases, streams)
- Normalize formats (PDF to text, HTML to markdown, structured data to JSON)
- Assign document-level metadata (source, date, author, category)
- Chunk documents using domain-appropriate strategy (semantic chunking, section-based, sliding window)

**2. Extract**
- Run entity extraction (NER models, LLM-based extraction, or hybrid)
- Run relation extraction (prompt-based, dependency parsing, or co-occurrence)
- Normalize entities (synonym resolution, ontology linking, deduplication)
- Assign confidence scores to extracted triples

**3. Build Knowledge Graph**
- Map extracted entities and relations to the graph schema
- Resolve entities against existing graph nodes (entity resolution)
- Insert new nodes and edges with provenance metadata
- Enforce schema constraints (required properties, cardinality)

**4. Index**
- Build graph indices for efficient traversal (node label indices, relationship type indices, full-text indices)
- Generate embeddings for graph entities (node2vec, text embeddings of entity descriptions)
- Populate vector index with entity/chunk embeddings
- For Community-Based pattern: run community detection and generate community summaries

**5. Retrieve**
- Parse incoming query to identify intent, entities, and constraints
- Route query to appropriate retrieval strategy (graph-first, vector-first, community-level)
- Execute graph traversal and/or vector search
- Fuse results using re-ranking (reciprocal rank fusion, learned re-ranker, or graph-distance weighting)

**6. Generate**
- Assemble retrieved context into a structured prompt (entities, relationships, supporting text)
- Include graph path information for multi-hop reasoning transparency
- Call LLM with graph-grounded context
- Post-process response for format and accuracy

**7. Cite**
- Map generated claims back to source graph nodes and edges
- Construct provenance chains: claim -> graph entity -> source document -> extraction method
- Surface citations in the response for user verification
- Log retrieval paths for debugging and quality improvement

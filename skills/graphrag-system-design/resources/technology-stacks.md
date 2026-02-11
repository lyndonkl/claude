# Technology Stacks for GraphRAG

> This resource supports **Step 3** of the [GraphRAG System Design](../SKILL.md) workflow.

## WHY: Technology Choices Matter

Technology choices significantly impact development speed, performance, and maintainability of GraphRAG systems. The wrong graph database can bottleneck multi-hop traversals; the wrong vector store can limit hybrid search capabilities; the wrong orchestration framework can constrain retrieval patterns. Deliberate component selection, grounded in requirements analysis, prevents costly migrations and performance problems downstream.

Key selection criteria:
- **Query patterns**: Do you need deep traversals (favor TigerGraph), SPARQL reasoning (favor GraphDB), or rapid prototyping (favor Neo4j)?
- **Scale**: Small knowledge graphs (< 1M nodes) have different needs than enterprise-scale graphs (100M+ nodes)
- **Integration**: Does the component integrate with your existing infrastructure and chosen orchestration framework?
- **Team expertise**: A technically superior choice that nobody on the team knows is worse than a good-enough choice the team can operate
- **Budget**: Managed services reduce operational overhead but increase direct costs; open-source requires more engineering investment

## WHAT: Component-by-Component Selection

### Graph Databases

Graph databases are the structural backbone of any GraphRAG system. They store entities, relationships, and properties, and provide traversal capabilities for multi-hop reasoning.

#### Neo4j

- **Model**: Labeled Property Graph (LPG)
- **Query Language**: Cypher
- **Key Features**:
  - Native vector index support (since version 5.11) enabling single-system GraphRAG
  - Graph Data Science (GDS) library with 65+ algorithms including community detection (Leiden, Louvain), centrality, similarity, and pathfinding
  - ACID transactions for data integrity
  - Full-text search via Apache Lucene integration
  - APOC (Awesome Procedures on Cypher) extended function library
- **Strengths**: Developer-friendly, extensive documentation, largest graph database community, first-class LangChain and LlamaIndex integration, mature tooling (Neo4j Browser, Bloom)
- **Limitations**: Vertical scaling model (single-machine for writes in Community Edition), enterprise features require commercial license, vector index less mature than purpose-built vector databases
- **Best For**: Rapid GraphRAG prototyping, systems where graph and vector can share a single database, teams with Cypher experience, LangChain/LlamaIndex-based pipelines

#### TigerGraph

- **Model**: Labeled Property Graph (LPG), distributed
- **Query Language**: GSQL (SQL-like graph query language)
- **Key Features**:
  - Distributed MPP (Massively Parallel Processing) architecture for large-scale graph analytics
  - Real-time deep link analysis across billions of edges
  - Built-in graph algorithms and machine learning workbench
  - Native parallel graph computation
- **Strengths**: Superior performance for deep traversals (10+ hops) and large-scale analytics, horizontal scaling, real-time streaming ingestion
- **Limitations**: Smaller community than Neo4j, GSQL learning curve, fewer pre-built RAG integrations, higher operational complexity
- **Best For**: Enterprise-scale GraphRAG with billions of entities, deep link analysis (fraud detection, supply chain), real-time streaming graph updates

#### ArangoDB

- **Model**: Multi-model (Graph + Document + Key-Value)
- **Query Language**: AQL (ArangoDB Query Language)
- **Key Features**:
  - Single database for graph, document, and key-value workloads
  - ArangoSearch for full-text and vector search
  - SmartGraphs for distributed graph processing
  - Foxx microservice framework for custom API endpoints
- **Strengths**: Flexible multi-model approach reduces infrastructure complexity, good for systems that need both graph and document storage, AQL supports graph traversals and document queries in one language
- **Limitations**: Graph traversal performance lower than dedicated graph databases for very deep traversals, smaller graph-specific community
- **Best For**: Systems with mixed graph and document workloads, teams wanting to minimize infrastructure components, rapid prototyping with flexible data modeling

#### AWS Neptune

- **Model**: Supports both RDF (via SPARQL) and LPG (via Apache Gremlin/openCypher)
- **Query Languages**: SPARQL, Gremlin, openCypher
- **Key Features**:
  - Fully managed service with automated backups, patching, and failover
  - Neptune ML for graph-based predictions using GNNs
  - Neptune Analytics for in-memory graph analytics
  - Deep AWS ecosystem integration (S3, Lambda, SageMaker, IAM)
- **Strengths**: Zero operational overhead, automatic scaling of read replicas, strong security via IAM and VPC, supports both RDF and LPG in the same instance
- **Limitations**: AWS lock-in, limited algorithm library compared to Neo4j GDS, higher cost for small workloads, less community tooling for RAG integration
- **Best For**: AWS-native organizations, systems requiring both RDF and LPG support, teams preferring managed infrastructure, compliance-heavy environments benefiting from AWS security controls

#### GraphDB (Ontotext)

- **Model**: RDF triple store
- **Query Language**: SPARQL
- **Key Features**:
  - OWL reasoning engine for inference and semantic queries
  - Concept search combining structured and semantic retrieval
  - GraphQL and REST API access
  - Connectors for Elasticsearch and Solr for full-text search
  - RDF-star support for statement-level metadata
- **Strengths**: Best-in-class for ontology-driven domains, OWL reasoning enables inference over explicit and implicit knowledge, SPARQL federation for querying across multiple RDF sources, strong in healthcare and life sciences
- **Limitations**: RDF triple model is more verbose than LPG, steeper learning curve for teams without semantic web experience, smaller general developer community
- **Best For**: Domains with formal ontologies (healthcare with UMLS/SNOMED, life sciences), systems requiring logical inference, semantic web integration, standards-compliant knowledge graphs

### Graph Database Comparison

| Feature | Neo4j | TigerGraph | ArangoDB | Neptune | GraphDB |
|---------|-------|------------|----------|---------|---------|
| Data Model | LPG | LPG | Multi-model | RDF + LPG | RDF |
| Query Language | Cypher | GSQL | AQL | SPARQL/Gremlin | SPARQL |
| Vector Support | Native (5.11+) | Via integration | ArangoSearch | Via integration | Via Connectors |
| Scaling | Vertical (CE) / Sharded (EE) | Horizontal | Horizontal | Managed auto | Vertical + cluster |
| Community Detection | GDS Library | Built-in | Via Pregel | Neptune Analytics | Limited |
| RAG Framework Integration | Excellent | Limited | Moderate | Moderate | Limited |
| Managed Option | Aura | Cloud | Oasis | Fully managed | Ontotext Cloud |
| OWL Reasoning | No | No | No | No | Yes |
| Best Scale | 1M-1B nodes | 1B+ nodes | 1M-100M nodes | 1M-1B nodes | 1M-500M triples |

### Vector Databases

Vector databases store embeddings and enable semantic similarity search, which complements graph-based structural retrieval.

#### Pinecone

- **Type**: Managed, cloud-native
- **Key Features**:
  - Metadata filtering for hybrid structured + semantic search
  - Sparse + dense retrieval for keyword and semantic combined
  - Namespaces for multi-tenant isolation
  - Serverless and pod-based deployment options
- **Strengths**: Zero operational overhead, fast query performance, simple API, metadata filtering enables pre-filtering before semantic search
- **Limitations**: Proprietary (no self-hosted option), cost scales with vector count, limited query expressiveness compared to graph databases
- **Best For**: Teams wanting managed vector search with minimal ops, systems where metadata filtering replaces some graph functionality, rapid prototyping

#### Weaviate

- **Type**: Open source, self-hostable
- **Key Features**:
  - GraphQL API for structured queries over vector data
  - Hybrid structured + unstructured search in a single query
  - Generative modules (generative-openai, generative-cohere) for RAG-native search
  - Multi-tenancy support
  - Built-in vectorization modules (text2vec, img2vec)
- **Strengths**: Open source with commercial support, GraphQL interface bridges structured and vector queries, generative modules reduce pipeline complexity, active community
- **Limitations**: Self-hosting requires operational expertise, GraphQL schema must be defined upfront, less mature than Pinecone for pure vector workloads
- **Best For**: Teams wanting open-source with structured query capabilities, systems that benefit from built-in vectorization, GraphQL-native architectures

#### Qdrant

- **Type**: Open source, self-hostable
- **Key Features**:
  - Written in Rust for high performance
  - Rich filtering with payload (metadata) support
  - Named vectors for multiple embedding spaces per point
  - Quantization for reduced memory usage
  - gRPC and REST APIs
- **Strengths**: High performance (Rust-based), flexible filtering, multiple vectors per record (useful for multi-modal GraphRAG), efficient memory usage with quantization
- **Limitations**: Smaller community than Pinecone/Weaviate, fewer built-in integrations, requires self-hosting for full control
- **Best For**: Performance-sensitive deployments, multi-modal systems needing multiple embedding spaces, teams comfortable with self-hosting

#### PostgreSQL + pgvector

- **Type**: Extension to PostgreSQL
- **Key Features**:
  - Vector similarity search within familiar SQL
  - HNSW and IVFFlat index types
  - Integrates with existing PostgreSQL infrastructure (authentication, backup, monitoring)
  - Combined with Apache AGE extension for graph queries in same database
- **Strengths**: No new infrastructure if already using PostgreSQL, familiar SQL interface, ACID transactions across vector and relational data, pgvector + AGE enables graph+vector in a single database
- **Limitations**: Vector search performance lower than purpose-built vector databases at scale, limited vector-specific features, HNSW index build time can be slow for large datasets
- **Best For**: Teams already on PostgreSQL wanting to add vector search without new infrastructure, smaller-scale GraphRAG systems, single-database simplicity

### Vector Database Comparison

| Feature | Pinecone | Weaviate | Qdrant | pgvector |
|---------|----------|----------|--------|----------|
| Deployment | Managed only | Self-host / Cloud | Self-host / Cloud | Extension |
| API | REST | GraphQL + REST | gRPC + REST | SQL |
| Filtering | Metadata filters | Structured + vector | Payload filters | SQL WHERE |
| Hybrid Search | Sparse + dense | Built-in | Via named vectors | Manual |
| Multi-tenancy | Namespaces | Native | Collections | Schemas |
| Max Scale | Billions | Millions-Billions | Millions-Billions | Millions |
| Open Source | No | Yes | Yes | Yes |
| Graph Combo | External | External | External | AGE extension |

### Orchestration Frameworks

Orchestration frameworks manage the pipeline logic connecting graph databases, vector stores, and LLMs.

#### LangChain

- **Graph Integration**: GraphQAChain, Neo4jGraph, GraphCypherQAChain
- **Key Features**:
  - Pre-built Neo4j integration generating Cypher from natural language
  - Agent tools for graph database interaction
  - Function calling for structured graph queries
  - LCEL (LangChain Expression Language) for composable chains
  - Community-contributed graph tools and retrievers
- **Strengths**: Largest RAG framework community, most pre-built graph integrations, rapid prototyping, extensive documentation and tutorials
- **Limitations**: Abstraction overhead for complex custom logic, fast-moving API with breaking changes, performance overhead for production workloads
- **Best For**: Rapid prototyping of GraphRAG systems, Neo4j-based architectures, teams wanting pre-built graph-to-LLM chains

#### LlamaIndex

- **Graph Integration**: KnowledgeGraphIndex, PropertyGraphIndex, Neo4jPropertyGraphStore, Neo4jGraphStore
- **Key Features**:
  - KnowledgeGraphIndex for automatic KG construction from documents
  - PropertyGraphIndex with native support for property graph stores
  - KnowledgeGraphRAGRetriever combining graph and vector retrieval
  - Composable query engines for multi-source retrieval
  - Built-in evaluation framework for RAG quality
- **Strengths**: Purpose-built for RAG (vs LangChain's broader scope), strong KG construction from unstructured text, PropertyGraphIndex deeply integrates graph structure, built-in RAG evaluation
- **Limitations**: Smaller community than LangChain, fewer third-party integrations, less flexible for non-RAG use cases
- **Best For**: Systems building KGs from unstructured data, PropertyGraph-native architectures, teams wanting integrated RAG evaluation

#### LangGraph

- **Type**: Agent state management framework (built on LangChain)
- **Key Features**:
  - Stateful agents with persistent memory across turns
  - Multi-step graph interactions with branching and looping
  - Human-in-the-loop approval steps
  - Checkpoint and replay for debugging
- **Strengths**: Manages complex multi-step GraphRAG workflows (query decomposition, iterative graph exploration, result synthesis), supports conditional routing between retrieval strategies
- **Limitations**: Adds complexity for simple retrieval patterns, requires LangChain ecosystem, newer with less production track record
- **Best For**: Multi-step GraphRAG agents that decompose complex queries, systems needing human-in-the-loop validation, iterative graph exploration workflows

#### Custom Pipelines

- **Architecture**: NER -> KG Query -> Rank -> LLM, built with application code
- **Key Features**:
  - Maximum control over every pipeline stage
  - No framework abstraction overhead
  - Direct database driver usage (neo4j Python driver, gremlin-python)
  - Custom query routing and re-ranking logic
  - Domain-specific optimizations impossible in generic frameworks
- **Strengths**: Best performance (no framework overhead), complete control over retrieval logic, no dependency on framework release cycles, can implement any retrieval pattern without workarounds
- **Limitations**: Higher development cost, must build common patterns from scratch (caching, retry, error handling), no community components to leverage
- **Best For**: Production systems with complex custom retrieval patterns, performance-critical deployments, teams with strong engineering capacity

### Orchestration Comparison

| Feature | LangChain | LlamaIndex | LangGraph | Custom |
|---------|-----------|------------|-----------|--------|
| Graph Integration | GraphQAChain, Cypher | KGIndex, PropertyGraph | Via LangChain | Direct drivers |
| Learning Curve | Medium | Medium | High | Varies |
| Flexibility | Medium | Medium | High | Maximum |
| Performance | Good | Good | Good | Best |
| Prototyping Speed | Fast | Fast | Medium | Slow |
| Production Readiness | Medium | Medium | Medium | High |
| Community Size | Largest | Large | Growing | N/A |
| Multi-step Agents | Via agents | Via query engines | Native | Custom |

### Reference Architecture Combinations

**Rapid Prototyping Stack:**
- Neo4j (with native vector index) + LangChain GraphCypherQAChain + GPT-4
- Single database, minimal infrastructure, fastest time-to-demo
- Limitation: Neo4j vector index less mature than purpose-built alternatives

**Production Hybrid Stack:**
- Neo4j (graph) + Pinecone (vector) + Custom pipeline + Claude/GPT-4
- Best-of-breed for each component, independent scaling, maximum control
- Requires synchronization logic between graph and vector stores

**Open-Source Stack:**
- Neo4j Community (graph) + Qdrant (vector) + LlamaIndex + Llama/Mistral
- Fully open-source, self-hosted, no vendor lock-in
- Higher operational overhead, requires infrastructure expertise

**Enterprise AWS Stack:**
- Neptune (graph) + OpenSearch (vector) + Custom pipeline + Bedrock (LLM)
- Fully managed, AWS-native security and compliance, IAM integration
- AWS lock-in, higher direct costs, fewer community RAG integrations

**Semantic/Ontology Stack:**
- GraphDB (RDF) + Weaviate (vector) + Custom SPARQL+vector pipeline + GPT-4
- Best for domains with formal ontologies (healthcare, life sciences)
- Requires semantic web expertise, smaller community

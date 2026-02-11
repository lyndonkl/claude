# Graph Data Models for Knowledge Representation

> This resource supports **Step 2** of the [Knowledge Graph Construction](../SKILL.md) workflow.

## WHY

Choosing the wrong graph data model creates persistent friction throughout the KG lifecycle. A model that cannot natively express your domain's core patterns forces workarounds in schema design, complicates queries, and limits the reasoning capabilities available downstream. Conversely, choosing an overly complex model for a simple use case adds unnecessary overhead in tooling, training, and maintenance.

The data model decision is one of the earliest and most consequential choices in KG construction. It determines your query language, available tooling, reasoning capabilities, and integration paths with vector databases and LLM pipelines. Making this choice explicit and well-justified prevents costly migrations later.

Different data models optimize for different properties:
- **Flexibility vs. Standardization**: LPG prioritizes rapid schema evolution; RDF prioritizes interoperable standards.
- **Expressiveness vs. Tooling**: Hypergraphs can represent N-ary relations natively but lack mature query engines.
- **Reasoning vs. Performance**: RDF/OWL enables formal inference but adds computational overhead.
- **Temporal vs. Static**: Temporal graphs model knowledge evolution but require specialized storage.

Understanding these trade-offs lets you match the model to your actual requirements rather than defaulting to whatever technology is most familiar.

## WHAT

### 1. Labeled Property Graphs (LPG)

Labeled Property Graphs represent knowledge as nodes and edges, each carrying labels (types) and key-value property maps. This is the model used by Neo4j, Amazon Neptune (in property graph mode), and TigerGraph.

**Structure**

```
Nodes:  (label, {property: value, ...})
Edges:  (label, source, target, {property: value, ...})
```

Example:
```
(:Person {name: "Alice", role: "Researcher"})
  -[:PUBLISHED {year: 2024, journal: "Nature"}]->
(:Paper {title: "Graph Methods for NLP", doi: "10.1234/..."})
```

**Strengths**

- **Flexibility**: Schema-optional; add new node/edge types and properties without migration.
- **Native traversal**: Pointer-based storage enables efficient multi-hop graph traversal.
- **Vector integration**: Neo4j natively supports vector indexes for hybrid graph+vector retrieval.
- **Developer familiarity**: Cypher and Gremlin are widely adopted query languages.
- **Rapid prototyping**: Start building without a formal ontology; evolve the schema iteratively.

**Limitations**

- **No formal reasoning**: Cannot express OWL-style class hierarchies, transitivity, or inference rules natively.
- **No global standard**: Cypher (Neo4j) and Gremlin (TinkerPop) are not fully interchangeable.
- **Schema enforcement**: Must be implemented in application code or via constraints rather than declarative ontology.

**Query Language: Cypher**

```cypher
// Find all drugs that treat diseases in a specific body system
MATCH (d:Drug)-[t:TREATS]->(dis:Disease {body_system: "cardiovascular"})
WHERE t.confidence > 0.8
RETURN d.name, dis.name, t.confidence
ORDER BY t.confidence DESC
```

**Best For**: RAG pipelines, enterprise knowledge bases, rapid development, use cases where vector search integration is critical.

### 2. RDF / OWL

The Resource Description Framework (RDF) represents knowledge as subject-predicate-object triples. Combined with the Web Ontology Language (OWL), it provides formal semantics, class hierarchies, and automated reasoning.

**Structure**

```
Triples: (subject, predicate, object)
All resources identified by URIs.
```

Example:
```turtle
:Metformin rdf:type :Drug ;
           :treats :Type2Diabetes ;
           :hasClass :Biguanide .

:Type2Diabetes rdf:type :Disease ;
               :icdCode "E11" .

:Drug rdfs:subClassOf :ChemicalSubstance .
:treats rdfs:domain :Drug ;
        rdfs:range :Disease .
```

**Strengths**

- **Standardization**: W3C standards (RDF, RDFS, OWL, SPARQL) ensure interoperability.
- **Formal reasoning**: OWL-DL reasoners can infer implicit facts (transitivity, class subsumption, property chains).
- **Ontology ecosystem**: Thousands of published ontologies (UMLS, SNOMED-CT, Gene Ontology, Dublin Core) available for reuse.
- **Federated queries**: SPARQL endpoints enable querying across distributed knowledge bases.
- **Provenance standards**: RDF Reification and Named Graphs provide standardized provenance mechanisms.

**Limitations**

- **Complexity**: RDF/OWL has a steep learning curve; ontology engineering requires specialized skills.
- **Performance**: Triple stores can be slower than native graph databases for deep traversals.
- **Verbosity**: RDF serializations are more verbose than LPG representations.
- **Vector integration**: No native vector support; requires external integration.

**Query Language: SPARQL**

```sparql
# Find all drugs treating cardiovascular diseases with evidence
SELECT ?drug ?disease ?confidence WHERE {
  ?drug rdf:type :Drug ;
        :treats ?disease .
  ?disease rdf:type :Disease ;
           :bodySystem "cardiovascular" .
  ?drug :treats ?reification .
  ?reification :confidence ?confidence .
  FILTER (?confidence > 0.8)
}
ORDER BY DESC(?confidence)
```

**Best For**: Biomedical/clinical domains, interoperability across organizations, domains requiring formal reasoning, regulatory/compliance applications.

### 3. Hypergraphs

Hypergraphs generalize standard graphs by allowing a single edge (hyperedge) to connect any number of nodes. This naturally models N-ary relations without reification.

**Structure**

```
Nodes:      Standard entities
Hyperedges: Connect 2+ nodes simultaneously, with typed roles
```

Example:
```
Hyperedge: ClinicalTrial_001
  Roles:
    drug:      Remdesivir
    condition: COVID-19
    outcome:   Reduced Mortality
    sponsor:   NIH
    phase:     3
```

**Strengths**

- **Expressiveness**: N-ary relations are first-class constructs, not workarounds.
- **Natural modeling**: Events, transactions, and multi-participant relations map directly.
- **Reduced redundancy**: No need to create intermediate reification nodes.
- **Query clarity**: Queries over multi-participant events are more direct.

**Limitations**

- **Limited tooling**: No mature, widely adopted hypergraph database exists at the scale of Neo4j or Virtuoso.
- **Query language**: No standardized query language; most implementations use custom APIs.
- **Ecosystem**: Smaller community, fewer libraries, less documentation.
- **Storage**: Most implementations serialize hyperedges as sets of binary edges internally.

**Implementation Approaches**

Since pure hypergraph databases are rare, implement hypergraph semantics on existing platforms:
- **LPG reification**: Model hyperedges as nodes with role-labeled edges (the event reification pattern).
- **RDF named graphs**: Use named graphs to group triples belonging to a single hyperedge.
- **Custom storage**: Use a document store (e.g., MongoDB) for hyperedge records with graph indexes.

**Best For**: Event-centric domains (news, clinical trials, financial transactions), situations where N-ary relations dominate, research contexts where expressiveness outweighs tooling maturity.

### 4. Temporal Graphs

Temporal graphs extend standard graph models with time-indexed nodes, edges, and subgraphs. They capture how knowledge evolves, enabling queries like "what was known at time T?" and "how has entity X changed over period P?"

**Structure**

```
Time-indexed edges:  (source, relation, target, valid_from, valid_to)
Versioned nodes:     (entity, version, timestamp, {properties})
Episodic subgraphs:  Named snapshots of the graph at specific time points
```

Example:
```
(:Alice)-[:WORKS_AT {valid_from: 2020-01, valid_to: 2023-06}]->(:CompanyA)
(:Alice)-[:WORKS_AT {valid_from: 2023-07, valid_to: null}]->(:CompanyB)

// Episodic subgraph: "state of clinical knowledge as of 2024-01"
```

**Strengths**

- **Knowledge evolution**: Track how facts change over time without losing history.
- **Temporal queries**: "Who worked at Company A in 2021?" or "What drugs were approved before 2020?"
- **Time-decay ranking**: Weight recent facts more heavily in retrieval.
- **Versioned truth**: Maintain multiple versions of facts with validity periods.
- **Episodic memory**: Create named snapshots for point-in-time reasoning.

**Limitations**

- **Storage overhead**: Every temporal edge requires additional metadata.
- **Query complexity**: Temporal predicates add complexity to query language and execution.
- **Limited native support**: Few databases natively support temporal semantics; most require application-level implementation.
- **Index complexity**: Temporal indexes (B-tree on time ranges) add storage and maintenance overhead.

**Implementation Approaches**

- **Neo4j with temporal properties**: Store valid_from/valid_to as edge properties; filter in Cypher queries.
- **RDF with temporal named graphs**: Each named graph represents a time slice.
- **Dedicated temporal stores**: TerminusDB provides native temporal graph semantics.
- **Application-layer versioning**: Maintain version chains in node properties.

**Best For**: Knowledge bases where facts change over time, clinical records, news/events, financial data, any domain requiring "as of" queries or historical analysis.

### 5. Layered Architectures

Layered architectures organize a KG into distinct tiers with different trust levels, update frequencies, and governance rules. This is an architectural pattern that can be implemented on top of any data model (LPG, RDF, Hypergraph, or Temporal).

**Three-Layer Pattern**

```
Layer 3: Canonical Ontology
  - Formal class hierarchy and relation definitions
  - Maintained by domain experts
  - Changes infrequently (versioned releases)
  - Highest trust level

Layer 2: Domain Knowledge
  - Curated facts from literature, databases, expert review
  - Updated periodically as new knowledge emerges
  - Medium trust level (verified but may become outdated)

Layer 1: Instance Data
  - Extracted from user documents, case files, real-time feeds
  - Updated continuously as new data arrives
  - Lower trust level (automated extraction, not fully verified)
```

**Cross-Layer Integration**

- Layer 1 entities link to Layer 2 concepts via `INSTANCE_OF` or `RELATED_TO` edges.
- Layer 2 concepts link to Layer 3 classes via `rdf:type` or `SUBCLASS_OF` edges.
- Queries can be scoped to a single layer or span multiple layers.
- Trust scores propagate: a Layer 1 fact supported by a Layer 2 concept inherits partial trust.

**Benefits**

- **Trust differentiation**: Distinguish verified knowledge from automated extractions.
- **Independent evolution**: Update instance data without touching the ontology.
- **Governance**: Apply different access controls and review processes per layer.
- **Scalability**: Layer 3 is small and stable; Layer 1 can grow rapidly.

**Implementation**

- **LPG**: Use node labels or a `layer` property to tag nodes; use relationship properties for cross-layer links.
- **RDF**: Use named graphs, one per layer; cross-layer links are triples spanning named graphs.
- **Neo4j multi-database**: Separate layers into distinct databases with cross-database queries.

**Best For**: Enterprise knowledge management, multi-source integration, RAG systems requiring trust-aware retrieval, regulated domains requiring audit trails.

### 6. Model Comparison Summary

| Criterion | LPG | RDF/OWL | Hypergraph | Temporal |
|-----------|-----|---------|------------|----------|
| **Flexibility** | High | Medium | High | Medium |
| **Standardization** | Low (Cypher/Gremlin) | High (W3C) | Low (custom) | Low |
| **Reasoning** | Limited | Full (OWL-DL) | Limited | Time-based |
| **Vector Integration** | Native (Neo4j) | Via extensions | Custom | Via extensions |
| **Query Language** | Cypher, Gremlin | SPARQL | Custom APIs | Temporal Cypher |
| **Tooling Maturity** | High | High | Low | Medium |
| **N-ary Relations** | Via reification | Via reification/named graphs | Native | Via reification |
| **Temporal Support** | Via properties | Via named graphs | Via properties | Native |
| **Learning Curve** | Low | High | Medium | Medium |
| **Best For** | Rapid dev, RAG | Interop, reasoning | N-ary events | Evolving knowledge |

### 7. Decision Framework

Use this flowchart to select your data model:

1. **Do you need formal reasoning or OWL inference?**
   - Yes -> RDF/OWL
   - No -> Continue

2. **Do you need to interoperate with external ontologies (UMLS, SNOMED, etc.)?**
   - Yes, and reasoning is needed -> RDF/OWL
   - Yes, but only for entity linking -> LPG with ontology linking
   - No -> Continue

3. **Are N-ary relations (3+ participants) the dominant pattern?**
   - Yes, and tooling maturity is less important -> Hypergraph
   - Yes, but need mature tooling -> LPG with event reification
   - No -> Continue

4. **Does knowledge evolve significantly over time?**
   - Yes, and temporal queries are critical -> Temporal Graph
   - Yes, but only need latest state with history -> LPG with temporal properties
   - No -> Continue

5. **Default choice**: LPG (most flexible, best tooling, easiest to start).

6. **For any model**: Consider adding the layered architecture pattern for multi-source trust differentiation.

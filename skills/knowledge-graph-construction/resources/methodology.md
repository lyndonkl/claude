# Knowledge Graph Construction Methodology

> This resource supports **Steps 3-6** of the [Knowledge Graph Construction](../SKILL.md) workflow.

## WHY

Large language models generate fluent text but lack grounded, verifiable knowledge structures. When LLMs retrieve context from flat document stores, they often hallucinate connections, miss implicit relationships, and cannot perform multi-hop reasoning across disparate facts. Knowledge graphs solve this by providing an explicit, structured representation of entities, relations, and provenance that LLMs can query deterministically.

The core problem is the gap between unstructured text and structured knowledge. Bridging this gap requires systematic extraction pipelines that identify entities, resolve ambiguities, normalize representations, and enforce schema constraints. Without a principled methodology, extracted graphs are noisy, incomplete, and unreliable -- defeating the purpose of building a KG in the first place.

A well-constructed KG provides:
- **Grounded retrieval**: Every fact traces to a source document with a confidence score.
- **Multi-hop reasoning**: Traverse chains of relations that vector similarity search cannot capture.
- **Deduplication**: Canonical entity representations eliminate redundant or conflicting information.
- **Explainability**: Query paths through the graph explain why an answer was produced.
- **Composability**: Layer domain knowledge atop instance data atop canonical ontologies.

## WHAT

### 1. LLM-Assisted Entity Extraction

Entity extraction is the foundation of KG construction. Modern pipelines use LLMs to identify entities from unstructured text, augmented with structured verification.

**Core Approach: Prompt-Based Extraction**

Design extraction prompts that specify the target entity types, expected attributes, and output format. Provide the LLM with a schema definition and ask it to extract all matching entities from a text chunk.

```
System: You are an entity extraction system. Extract all entities matching
the following types from the provided text. Return structured JSON.

Entity Types:
- Person: {name, role, affiliation}
- Organization: {name, type, location}
- Drug: {name, class, mechanism}
- Disease: {name, icd_code, body_system}

Output Format: {"entities": [{"type": "...", "attributes": {...}, "span": "..."}]}
```

**Multi-Round Verification**

A single extraction pass misses entities, especially when documents are long or entity mentions are implicit. Use multi-round extraction:

1. **Round 1**: Extract entities with the primary prompt.
2. **Round 2**: Feed the extracted entities back to the LLM and ask: "Are there any entities in the text that were missed in this list? Check especially for implicit mentions, abbreviations, and co-references."
3. **Round 3** (optional): Present the entity list to a second LLM and ask it to verify each entity against the source text.

Multi-round verification typically improves entity recall by 15-30% compared to single-pass extraction.

**Ontology-Guided Extraction**

When a domain ontology exists (UMLS for biomedical, Schema.org for general, FIBO for finance), use it to constrain extraction:

- Provide the ontology's class hierarchy as context to the extraction prompt.
- Ask the LLM to map each extracted entity to the closest ontology class.
- Flag entities that do not map to any known class for manual review.

This produces entities that are already partially aligned to the target schema.

### 2. Relation Extraction

Relations connect entities into a graph structure. Three primary approaches exist, often combined.

**Prompt-Based Relation Extraction**

After entities are extracted, prompt the LLM to identify relations between them:

```
Given these entities extracted from the text:
- [Entity A]: Drug "Metformin"
- [Entity B]: Disease "Type 2 Diabetes"
- [Entity C]: Organization "FDA"

Identify all relationships between these entities. For each relationship, provide:
- Source entity
- Target entity
- Relation type (from: TREATS, APPROVED_BY, CAUSES, ASSOCIATED_WITH, ...)
- Evidence: the text span supporting this relationship
- Confidence: high / medium / low
```

**Dependency-Parsing Augmented Extraction**

For high-precision relation extraction, combine LLM extraction with dependency parsing:

1. Parse sentences containing entity co-occurrences.
2. Extract the syntactic path between entity mentions.
3. Use the dependency path as additional signal for relation classification.
4. The LLM classifies the relation type given both the raw text and the parsed structure.

This hybrid approach reduces false-positive relations caused by entities that co-occur in text but are not actually related.

**Few-Shot Examples**

Provide 3-5 annotated examples of each target relation type in the extraction prompt. Few-shot examples dramatically improve extraction consistency, especially for domain-specific relation types that the LLM may not have encountered frequently in pre-training.

```
Examples of TREATS relation:
- "Aspirin is commonly used to treat headaches" -> (Aspirin)-[TREATS]->(Headache)
- "SSRIs are first-line therapy for depression" -> (SSRI)-[TREATS]->(Depression)

Now extract relations from the following text:
```

### 3. Event Reification

Many real-world facts involve more than two participants. A clinical trial involves a drug, a disease, an outcome, and a conducting organization. A financial transaction involves a buyer, a seller, an asset, and a price. Forcing these into binary relations loses information.

**N-ary Relations as First-Class Nodes**

Model complex events as nodes with typed role edges to each participant:

```
Event Node: ClinicalTrial_NCT04280705
  -[HAS_INTERVENTION]-> Drug: Remdesivir
  -[HAS_CONDITION]->    Disease: COVID-19
  -[HAS_OUTCOME]->      Outcome: {measure: "mortality", result: "reduced"}
  -[CONDUCTED_BY]->     Org: NIH
  -[HAS_PHASE]->        Phase: 3
  -[HAS_DATE_RANGE]->   Period: {start: 2020-03, end: 2020-10}
```

**Benefits of Reification**:
- Preserves the full structure of multi-participant events.
- Enables querying by any participant role ("all trials where NIH tested a drug for COVID-19").
- Supports attaching metadata (dates, outcomes, confidence) to the event itself.
- Avoids combinatorial explosion of binary edge pairs.

**When to Reify**:
- The relation involves 3 or more participants.
- Temporal context is essential (start/end dates, sequencing).
- The relation has its own attributes (outcome, confidence, method).
- You need to query "events matching criteria" rather than just "entity pairs."

### 4. Schema Enforcement

Extraction pipelines produce noisy output. Schema enforcement ensures the graph conforms to declared types and constraints.

**Controlled Vocabularies**

Define closed sets of allowed values for key properties:
- Entity types: only allow declared node labels.
- Relation types: only allow declared edge labels.
- Categorical attributes: use enum constraints (e.g., phase must be in {1, 2, 3, 4}).

**Post-Processing Validation**

After extraction, run automated checks:

1. **Type conformance**: Every node has a declared label; every edge connects valid source/target types.
2. **Required properties**: Mandatory fields are populated (e.g., every Drug node must have a name).
3. **Cardinality constraints**: Enforce limits (e.g., a Person has at most one date_of_birth).
4. **Orphan detection**: Flag nodes with no edges (likely extraction artifacts).
5. **Duplicate detection**: Identify near-duplicate nodes by string similarity on key attributes.

**Schema Evolution**

As extraction reveals entity types not anticipated in the initial schema, evolve the schema deliberately:
- Add new types only after reviewing a sample of instances.
- Deprecate types that prove too granular or too broad.
- Version the schema and track which extraction runs used which version.

### 5. Entity Normalization

Raw extraction produces multiple surface forms for the same real-world entity. Normalization resolves these into canonical representations.

**Synonym Merging**

Group equivalent mentions into a single canonical entity:
- "IBM", "International Business Machines", "IBM Corp." -> canonical: "IBM"
- "heart attack", "myocardial infarction", "MI" -> canonical: "Myocardial Infarction"

Methods:
1. **String similarity**: Jaccard, edit distance, or character n-gram overlap.
2. **LLM-based**: Ask the LLM "Are these two mentions referring to the same entity?"
3. **Embedding similarity**: Compute embeddings and merge above a cosine threshold.
4. **Knowledge base lookup**: Check if mentions map to the same Wikidata ID or UMLS CUI.

**Ontology Linking**

Map extracted entities to external knowledge bases:
- Biomedical: Link to UMLS Concept Unique Identifiers (CUIs).
- General: Link to Wikidata QIDs.
- Financial: Link to LEI (Legal Entity Identifier) codes.

Ontology linking provides a stable identifier for each entity, enables cross-dataset integration, and inherits hierarchical relationships from the ontology.

**Deduplication Pipeline**

1. **Blocking**: Group candidate duplicates by shared tokens or n-grams (reduces pairwise comparisons).
2. **Scoring**: Compute similarity scores for each candidate pair.
3. **Clustering**: Apply transitive closure or connected components to group duplicates.
4. **Canonical selection**: Choose the most complete or most frequent form as canonical.
5. **Merge**: Redirect all edges from duplicate nodes to the canonical node; merge properties.

### 6. Multi-Round Verification

A single extraction pass followed by normalization is insufficient for production-quality graphs. Multi-round verification catches systematic errors.

**LLM Cross-Check**

After building the initial graph, sample subgraphs and ask a second LLM to verify:
- "Given this source text, are the following extracted triples correct?"
- "Are there any relations stated in the text that are missing from this subgraph?"
- "Do any of these extracted facts contradict each other?"

**Fact-Checking Against Known KGs**

Cross-reference extracted triples against established knowledge graphs:
- Check if extracted (Drug)-[TREATS]->(Disease) triples align with DrugBank or ChEMBL.
- Verify (Person)-[AFFILIATED_WITH]->(Organization) against Wikidata.
- Flag contradictions for manual review.

**Human-in-the-Loop Review**

For high-stakes domains, sample a percentage of extracted triples for human annotation:
- Compute inter-annotator agreement on a calibration set.
- Focus human review on low-confidence extractions.
- Use human corrections to fine-tune extraction prompts iteratively.

### 7. Quality Control Framework

**Graph-Level Metrics**

Monitor overall graph health:
- **Node count by type**: Are all expected types populated?
- **Edge count by type**: Are relation distributions plausible?
- **Degree distribution**: Are there hubs (very high degree) or isolates (degree 0)?
- **Connected components**: How fragmented is the graph?
- **Schema conformance rate**: What percentage of nodes/edges pass all validation checks?

**Triple-Level Metrics**

Assess individual extraction quality:
- **Precision**: Of extracted triples, what fraction is correct? (Measured by human sample.)
- **Recall**: Of triples present in source text, what fraction was extracted? (Measured by annotation.)
- **Confidence calibration**: Do high-confidence extractions actually have higher precision?

**Iterative Improvement Loop**

1. Extract from a sample of documents.
2. Validate against schema and known KGs.
3. Human-review a sample of low-confidence triples.
4. Identify systematic error patterns (missed entity types, false relation types).
5. Update extraction prompts, schema, and normalization rules.
6. Re-extract and measure improvement.
7. Repeat until quality metrics meet thresholds.

### 8. Provenance and Evidence Layering

Every triple in the graph should carry provenance metadata:

```
(Drug: Metformin)-[TREATS {
  source_doc: "pmid_12345678",
  extraction_method: "gpt-4-turbo",
  confidence: 0.92,
  evidence_span: "Metformin is first-line therapy for type 2 diabetes",
  extracted_at: "2025-03-15T10:30:00Z",
  verified_by: "human_reviewer_42",
  layer: 2
}]->(Disease: Type 2 Diabetes)
```

Provenance enables:
- **Trust scoring**: Weight high-provenance triples more heavily in retrieval.
- **Source attribution**: Explain to end users where a fact came from.
- **Conflict resolution**: When two sources disagree, compare provenance to decide which to trust.
- **Temporal tracking**: Know when facts were extracted and whether they may be outdated.
- **Audit trails**: For regulated domains, demonstrate the chain of evidence for any fact in the graph.

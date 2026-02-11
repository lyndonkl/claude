# Provenance & Citation Tracking Patterns

> This resource supports **Step 5** of the [Retrieval & Search Orchestration](../SKILL.md) workflow.

## WHY

Trust and verifiability require knowing where each piece of information comes from. In any system that generates answers from a knowledge graph, users must be able to trace a claim back to its source evidence. Without provenance, every generated statement is unverifiable, and the system cannot distinguish between well-supported facts and hallucinated content.

This is not merely a best practice. In high-stakes domains, provenance is a requirement:
- **Healthcare**: A clinician needs to know whether a drug interaction claim comes from a peer-reviewed study, an FDA label, or an LLM extraction of uncertain quality. Acting on unsourced medical information can cause patient harm.
- **Legal**: Attorneys must cite specific statutes, case law, or regulatory filings. An answer without provenance is inadmissible and professionally negligent.
- **Finance**: Regulatory compliance (SOX, Basel III, MiFID II) requires auditable trails for any data-driven decision. Untracked information introduces compliance risk.

Beyond domain requirements, provenance serves critical system functions:
- **Hallucination detection**: If a generated claim has no supporting source, it is likely hallucinated. Provenance tracking makes this detectable.
- **Conflict resolution**: When sources disagree, provenance metadata (timestamps, authority level) enables principled resolution.
- **Trust calibration**: Users can adjust their confidence based on source quality and quantity. A fact supported by three peer-reviewed papers warrants more confidence than one supported by a single blog post.
- **Debugging and maintenance**: When errors are found, provenance trails identify which source introduced the error, enabling targeted correction.

## WHAT

### 1. Source Annotation Approaches

Every node and edge in the knowledge graph should carry metadata about its origin. There are several approaches, each with different trade-offs.

#### Metadata Fields on Edges and Nodes

The simplest approach: add properties directly to graph elements.

**Required fields**:
- `source_document_id`: Unique identifier of the document from which this fact was extracted.
- `source_url`: URL or URI where the source document can be accessed.
- `extraction_timestamp`: When the fact was extracted from the source.
- `confidence_score`: Numeric score (0.0-1.0) reflecting extraction confidence.
- `extraction_method`: How the fact was extracted (e.g., "manual_curation", "llm_extraction", "rule_based", "nlp_pipeline").

**Optional fields**:
- `source_passage`: The exact text span from which the fact was derived (sentence-level provenance).
- `source_page`: Page number or section reference within the source document.
- `reviewer`: Identifier of the human reviewer who validated the extraction, if applicable.
- `last_verified`: Timestamp of the most recent verification check.

**Trade-offs**: Simple to implement and query. However, metadata fields on each edge increase storage and can complicate queries when filtering by provenance attributes.

#### Evidence Nodes

Create dedicated nodes in the graph that represent sources, linked to fact nodes via `supported_by` edges.

**Structure**:
```
(Fact: Drug A treats Disease B)
  -[SUPPORTED_BY]-> (Evidence: {doc_id: "PMC12345", passage: "...", confidence: 0.92})
  -[SUPPORTED_BY]-> (Evidence: {doc_id: "FDA_LABEL_678", passage: "...", confidence: 0.98})
```

**Advantages**:
- Multiple sources can support a single fact without duplicating the fact node.
- Evidence nodes can carry rich metadata without bloating the fact schema.
- Easy to query: "Find all evidence for fact X" is a single hop.
- Evidence nodes can be shared across facts they support.

**Trade-offs**: Increases graph size. Each fact potentially gains several evidence nodes and edges. Requires careful schema design to avoid evidence node proliferation.

#### Named Graphs (RDF)

In RDF-based systems, use named graphs to group triples by their source context.

**Structure**:
```
GRAPH <source:PMC12345> {
  drug:A treats disease:B .
  gene:X causes disease:B .
}
GRAPH <source:FDA_LABEL_678> {
  drug:A treats disease:B .
  drug:A hasContraindication drug:C .
}
```

**Advantages**:
- Native RDF mechanism for provenance.
- Queries can be scoped to specific source contexts.
- Supports SPARQL GRAPH queries for source-aware retrieval.

**Trade-offs**: Only available in RDF/SPARQL systems. Not directly applicable to property graph databases like Neo4j.

#### Reification Approaches

Attach metadata to individual triples (statements) by treating them as first-class objects.

**RDF Reification**:
```
:statement1 rdf:type rdf:Statement ;
  rdf:subject drug:A ;
  rdf:predicate :treats ;
  rdf:object disease:B ;
  :source "PMC12345" ;
  :confidence 0.92 ;
  :extractedOn "2024-03-15" .
```

**Property Graph Reification** (via intermediate nodes):
```
(drug:A)-[:TREATS]->(Statement {confidence: 0.92, source: "PMC12345"})-[:OBJECT]->(disease:B)
```

**Trade-offs**: Conceptually clean but significantly increases graph complexity. Querying reified triples requires extra join steps. Use when fine-grained per-triple metadata is essential and the query overhead is acceptable.

### 2. Confidence Scoring

Not all sources are equally reliable. Confidence scoring assigns numeric quality indicators to facts based on their provenance.

#### Source Reliability Layering

Assign reliability tiers to source types:

| Tier | Source Type | Base Confidence | Examples |
|---|---|---|---|
| 1 (Highest) | Manually curated, peer-reviewed | 0.95-1.0 | Expert-curated KBs, published studies |
| 2 | Authoritative institutional sources | 0.85-0.95 | FDA labels, WHO guidelines, legal codes |
| 3 | Automated extraction with validation | 0.70-0.85 | NLP pipelines with human spot-checking |
| 4 | LLM extraction without validation | 0.50-0.70 | GPT-extracted triples, unreviewed |
| 5 (Lowest) | Unverified or user-generated | 0.30-0.50 | Forum posts, unverified web content |

These tiers provide a baseline. Individual facts may be adjusted up or down based on additional signals.

#### Multiple Source Aggregation

When a fact is supported by multiple independent sources, confidence increases:

- **Simple counting**: `adjusted_confidence = 1 - (1 - c1)(1 - c2)...(1 - cn)` where ci is each source's confidence. This models independent confirmation.
- **Weighted aggregation**: Weight each source by its tier reliability before aggregating.
- **Diminishing returns**: After 3-4 confirming sources, additional sources add marginal confidence. Cap the maximum at 0.99 to reflect inherent uncertainty.

#### Temporal Validity

Facts have lifespans. Confidence should decay for time-sensitive information:

- **Last Updated Tracking**: Store `last_updated` timestamps. Facts not refreshed within a domain-appropriate window (e.g., 1 year for biomedical, 1 day for financial) receive reduced confidence.
- **Status Labels**: Mark facts as `Confirmed`, `Contested`, `Deprecated`, or `Unknown`. Status affects both confidence and presentation.
- **Decay Functions**: Apply exponential decay to confidence over time: `confidence_adjusted = confidence_base * exp(-lambda * age_days)`. The lambda parameter varies by domain.

### 3. Evidence Chain Construction

Beyond individual source annotations, construct chains that show how multi-hop conclusions are derived from source evidence.

#### Linking Facts to Source Passages

Sentence-level provenance connects each graph fact to the specific text span it was extracted from:

```
Fact: (Drug A)-[:TREATS]->(Disease B)
Source passage: "In a randomized controlled trial, Drug A demonstrated significant
  efficacy in treating Disease B (p < 0.001)." [PMC12345, Section 3.2, Sentence 14]
```

This enables:
- Users to verify the extraction by reading the source passage.
- Quality auditors to check extraction accuracy at scale.
- LLMs to include the original phrasing in generated citations.

#### Multi-Source Evidence Aggregation

For complex claims derived from multiple facts, construct evidence chains:

```
Claim: "Drug A may help patients with Condition C"
Evidence chain:
  1. Drug A treats Disease B (source: PMC12345, confidence: 0.92)
  2. Disease B is a subtype of Condition C (source: MeSH ontology, confidence: 0.99)
  3. Therefore, Drug A may help with Condition C (inferred, confidence: 0.91)
```

Each step in the chain carries its own provenance. The overall confidence is bounded by the weakest link (minimum confidence in the chain) or computed as the product of individual confidences.

#### Conflict Detection

When sources disagree, the system must detect and surface the conflict:

**Detection rules**:
- Same subject-predicate with different objects from different sources.
- Contradictory relationship types (e.g., "treats" vs. "contraindicated_for") between the same entity pair.
- Numeric values that differ beyond a threshold.

**Resolution strategies**:
- **Timestamp Priority**: The most recent source wins, assuming the field is one where newer information supersedes older.
- **Source Authority**: Higher-tier sources override lower-tier sources.
- **Majority Vote**: When 3+ sources exist, go with the majority.
- **Surface the Conflict**: When resolution is uncertain, present both viewpoints to the LLM and instruct it to acknowledge the disagreement in its answer.

### 4. LLM Integration for Provenance

Provenance metadata must flow from the graph through retrieval into the LLM prompt and finally into the generated answer.

#### Feeding Provenance Metadata Alongside Content

When constructing the LLM context, include provenance metadata with each retrieved fact:

```
Context for LLM:
- Drug A treats Disease B
  [Source: PMC12345, Published: 2023-06-15, Confidence: 0.92,
   Type: Randomized Controlled Trial]
- Drug A has side effect Nausea
  [Source: FDA_LABEL_678, Updated: 2024-01-10, Confidence: 0.98,
   Type: FDA Drug Label]
```

This enables the LLM to make source-aware judgments and produce citations in its answer.

#### Citation Marker Injection in Prompts

Add explicit citation instructions to the system prompt:

```
Instructions: When answering, cite your sources using [Source: ID] markers.
Only state facts that are supported by the provided context. If you are
uncertain or the evidence is weak (confidence < 0.7), explicitly note this.
Do not make claims beyond what the sources support.
```

This guides the LLM to produce verifiable, cited answers.

#### Two Approaches to Citation

**Inline Citations**: The LLM inserts citation markers directly in the generated text.

```
"Drug A has been shown to effectively treat Disease B [PMC12345] with
minimal side effects [FDA_LABEL_678], though some patients report nausea."
```

- Advantages: Citations appear exactly where the claim is made.
- Challenges: LLMs may place citations incorrectly or fabricate citation IDs.

**Post-Hoc Source Mapping**: The LLM generates the answer without citations, then a separate pass maps each claim to supporting sources.

```
Step 1 - LLM generates: "Drug A effectively treats Disease B with minimal side effects."
Step 2 - Citation mapper matches:
  "Drug A effectively treats Disease B" -> PMC12345 (similarity: 0.94)
  "minimal side effects" -> FDA_LABEL_678 (similarity: 0.87)
Step 3 - Final output with mapped citations appended.
```

- Advantages: Separation of concerns; citation accuracy is independently verifiable.
- Challenges: Requires an additional processing step; may miss nuanced attribution.

**Recommendation**: Use inline citations as the primary approach with post-hoc verification as a quality check. If the inline citations do not match the post-hoc mapping, flag the discrepancy for review.

#### Confidence-Based Phrasing

Instruct the LLM to modulate its language based on source confidence:

| Confidence Range | Suggested Phrasing |
|---|---|
| 0.90-1.0 | "X is established/confirmed by [source]" |
| 0.75-0.90 | "According to [source], X..." |
| 0.60-0.75 | "Evidence suggests X [source], though further verification is recommended" |
| 0.50-0.60 | "[Source] reports X, but this has not been independently confirmed" |
| Below 0.50 | "Unverified reports suggest X; treat with caution" |

When multiple sources agree, escalate confidence phrasing:
- Single source: "According to [source]..."
- Two agreeing sources: "Supported by [source1] and [source2]..."
- Three or more: "Strongly supported by multiple sources [source1, source2, source3]..."

When sources disagree, surface the conflict:
- "Source A reports X, while Source B reports Y. The more recent source (A, 2024) may reflect updated findings."

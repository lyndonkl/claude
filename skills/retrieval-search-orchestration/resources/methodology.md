# Retrieval & Search Orchestration Methodology

> This resource supports **Steps 1-6** of the [Retrieval & Search Orchestration](../SKILL.md) workflow.

## WHY

Different query types demand fundamentally different retrieval approaches. A broad thematic question ("What are the major risk factors discussed across all clinical trials?") requires top-down aggregation across community summaries, while an entity-specific lookup ("What drugs interact with warfarin?") needs precise seed-entity expansion through local neighborhoods. A one-size-fits-all retrieval strategy inevitably sacrifices either recall (missing relevant information) or precision (flooding the LLM context with noise).

The consequences of poor retrieval pattern selection are severe:
- **Missed information**: Using local-first retrieval for broad questions means entire topic clusters go unseen.
- **Context pollution**: Using global-first retrieval for precise lookups dilutes the answer with irrelevant summaries.
- **Hallucination risk**: When retrieval fails silently, the LLM fills gaps with fabricated content, eroding user trust.
- **Latency waste**: Applying exhaustive multi-hop traversal to simple factoid queries adds unnecessary computational cost.
- **Broken provenance**: Without deliberate tracking, generated answers become unverifiable, which is unacceptable in high-stakes domains like healthcare, law, and finance.

Matching retrieval strategy to query type, domain constraints, and graph structure is the single most impactful design decision in a GraphRAG system.

## WHAT

### 1. Global-First Retrieval (Section 3.1)

Global-first retrieval starts from the highest level of abstraction and works downward. It is best suited for questions that require corpus-level understanding rather than entity-specific detail.

**Core Mechanism**:
- Run community detection (e.g., Leiden algorithm) on the knowledge graph to identify clusters of densely connected entities.
- Generate LLM-produced summaries for each community at multiple hierarchy levels.
- At query time, search community summaries using embedding similarity to identify relevant topic clusters.
- Traverse downward from matched communities to retrieve specific entities and relationships.

**Implementation Details**:
- Build a hierarchical community index where each level contains progressively more granular summaries.
- Use map-reduce style summarization: summarize each community independently (map), then aggregate across matched communities (reduce).
- Index community summaries with vector embeddings for fast retrieval.
- Configure the traversal depth based on query specificity. Broad questions stop at higher levels; more specific questions drill down further.

**Balancing Global Retrieval with Recall**:
- Global-first retrieval can miss entities that are poorly connected or sit at community boundaries.
- Mitigate by maintaining an entity-level fallback index for low-confidence global matches.
- Use overlap between adjacent communities to catch boundary entities.
- Monitor recall metrics per community to identify underrepresented regions of the graph.

**When to Use**:
- Summarization or thematic questions across the corpus.
- Questions about trends, patterns, or aggregate statistics.
- Exploratory queries where the user does not specify particular entities.

### 2. Local-First Retrieval (Section 3.2)

Local-first retrieval begins with specific entities mentioned in the query and expands outward through the graph neighborhood. It is ideal for entity-centric questions with clear anchor points.

**Core Mechanism**:
- **Entity Linking**: Map query mentions to graph entities using exact match, fuzzy match, or embedding-based linking. Disambiguation is critical when multiple candidates exist.
- **Seed Node Identification**: The linked entities become seed nodes for graph traversal.
- **Neighborhood Expansion**: Expand 1-2 hops from seed nodes, collecting connected entities and relationships.
- **Relevance Gating**: Use embedding similarity between the query and each candidate node/edge to prune irrelevant expansions. This acts as a guided BFS (breadth-first search) that follows only the most relevant paths.

**Implementation Details**:
- Set a maximum hop count (typically 1-2 for precision, up to 3 for broader exploration).
- At each hop, compute embedding similarity between the query and candidate nodes. Only expand nodes above a configurable threshold (e.g., cosine similarity > 0.7).
- Collect both entity attributes and relationship labels along the traversal path.
- Return the subgraph as structured context for the LLM.

**Entity Disambiguation**:
- When entity linking produces multiple candidates, use graph context to disambiguate: prefer entities whose neighborhood is more relevant to the query.
- Leverage entity type constraints from the query (e.g., if the query asks about a person, filter out organization entities with the same name).
- When ambiguity cannot be resolved, retrieve for all candidates and let the LLM select the most plausible one, noting the ambiguity.

**When to Use**:
- Factoid questions about specific entities.
- Relationship queries between known entities.
- Questions where anchor entities are clearly identifiable in the query text.

### 3. U-Shaped Hybrid Retrieval (Section 3.3)

The U-Shaped pattern combines top-down (global) and bottom-up (local) retrieval in a bidirectional process. Inspired by the MedGraphRAG approach, it achieves both breadth and depth.

**Core Mechanism**:
- **Top-Down Phase**: Start with global community search to identify relevant topic areas. This provides broad context and ensures no major theme is missed.
- **Bottom-Up Phase**: Simultaneously or subsequently, perform local-first retrieval from seed entities to gather precise detail.
- **Convergence**: Merge results from both phases. The top-down phase provides the macro context; the bottom-up phase provides the micro evidence.

**Implementation Details**:
- Execute global and local retrieval in parallel when possible to reduce latency.
- Use a dual ranking system: one score from community-level relevance, one from entity-level similarity. Combine with a weighted formula tuned to the query type.
- Implement iterative refinement loops: if the global phase identifies communities but the local phase finds no supporting entities, expand the local search. If the local phase finds entities outside the globally identified communities, check those communities for additional context.
- The MedGraphRAG variant uses a three-stage process: (1) coarse-grained document retrieval, (2) fine-grained entity extraction, (3) graph-enhanced reasoning.

**Iterative Loops**:
- After initial retrieval, the LLM evaluates whether the collected evidence is sufficient.
- If gaps are detected, a second retrieval pass targets the specific missing information.
- Limit iterations (typically 2-3) to control latency and cost.

**When to Use**:
- Complex questions that need both overview and detail.
- Domains where missing either breadth or depth causes significant quality loss.
- As a default pattern when query type distribution is mixed or unknown.

### 4. Query Decomposition (Section 3.4)

For complex multi-hop questions, decompose the original query into simpler sub-queries that can be resolved independently and then aggregated.

**Core Mechanism**:
- **LLM-as-Controller**: The LLM analyzes the original query and generates a plan of sub-queries, each targeting a specific piece of information needed for the final answer.
- **Sequential Retrieval**: Sub-queries are executed in order when later queries depend on earlier results. Independent sub-queries can run in parallel.
- **Aggregation**: Results from all sub-queries are merged, deduplicated, and ranked before being presented to the LLM for final synthesis.

**Sub-Query Generation Strategies**:
- **Decomposition**: Break a complex question into atomic parts. "Which drugs treat diseases caused by gene X?" becomes (1) "What diseases are caused by gene X?" and (2) "What drugs treat [disease results]?"
- **Self-Ask**: The LLM iteratively generates follow-up questions based on what it has learned so far, retrieving after each question.
- **ReAct Pattern**: Interleave "Thought" (reasoning about what is needed), "Action" (retrieval operation), and "Observation" (retrieved results) in a loop until the answer is complete.

**Tool-Augmented Retrieval**:
- The LLM can generate formal graph queries (Cypher for property graphs, SPARQL for RDF) instead of or alongside natural language sub-queries.
- This enables precise structural queries that embedding-based retrieval cannot express (e.g., "find all paths of length exactly 3 between entity A and entity B").
- Combine tool-generated results with embedding-based results for hybrid precision-recall.

**Aggregation Methods**:
- **Union**: Combine all results (maximizes recall).
- **Intersection**: Keep only results found by multiple sub-queries (maximizes precision).
- **Ranked Merge**: Interleave results by relevance score.
- **LLM Synthesis**: Feed all sub-query results to the LLM and let it synthesize the final answer, resolving conflicts.

**When to Use**:
- Multi-hop reasoning questions (2+ relationships to traverse).
- Composite questions with multiple independent parts.
- Questions requiring both structured graph queries and semantic search.

### 5. Temporal Retrieval (Section 3.5)

Temporal retrieval handles queries that are bounded by time or require understanding of sequences and changes over time.

**Core Mechanism**:
- **Time-Slice Filtering**: Restrict retrieval to entities and relationships valid within a specified time window. Requires temporal metadata (created_at, valid_from, valid_to) on graph elements.
- **Episodic Windowing**: Group graph updates into episodes (e.g., daily snapshots, quarterly reports) and retrieve from the relevant episode.
- **Nearest-Neighbor Sequence Prediction**: For questions about trends or future states, retrieve the most similar historical sequences and use them as context for prediction.

**Implementation Details**:
- Store temporal metadata as first-class properties on nodes and edges.
- Build time-partitioned indexes for efficient time-slice queries.
- Implement time-decay ranking: more recent information receives a higher relevance boost, with the decay rate configurable per domain. For fast-changing domains (news, stock prices), use aggressive decay. For slow-changing domains (scientific knowledge), use gentle decay.
- Support temporal operators in queries: BEFORE, AFTER, DURING, BETWEEN, LATEST.

**Time-Decay Ranking**:
- Apply an exponential decay function to relevance scores: `score_adjusted = score_base * exp(-lambda * age_days)`.
- The decay parameter lambda controls how quickly old information loses relevance.
- Combine time-decay with embedding similarity for a composite ranking.

**When to Use**:
- Questions about what was true at a specific point in time.
- Trend analysis or change detection queries.
- Domains with rapidly evolving information where recency matters.

### 6. Constraint-Guided Retrieval (Section 3.6)

Constraint-guided retrieval uses explicit type, attribute, or rule-based constraints to narrow the search space before or after neural retrieval.

**Core Mechanism**:
- **Pre-Filter + Vector Search**: Apply hard constraints (entity type, attribute ranges, relationship types) to reduce the candidate set, then run embedding similarity search within that reduced set.
- **Post-Filter After Neural Retrieval**: First retrieve the top-k by embedding similarity, then filter results that violate type or attribute constraints.
- **Symbolic Query Then Neural Re-Rank**: Execute a structured query (Cypher/SPARQL) to get candidates, then re-rank by neural embedding similarity to the original query.

**Implementation Details**:
- Parse the query for explicit constraints using NER and rule-based extraction (e.g., "clinical trials after 2020" -> type=ClinicalTrial, date>2020).
- Maintain typed indexes for efficient constraint filtering.
- For the hybrid NeuSym approach: run the symbolic query first to get a candidate set, then compute embedding similarity for ranking. This combines the precision of structured queries with the semantic flexibility of neural retrieval.
- Use rule engines for complex constraint logic (e.g., "drugs approved by FDA AND with fewer than 3 known side effects").

**When to Use**:
- Queries with explicit type or attribute filters.
- Domains with well-defined schemas and typed entities.
- Compliance or regulatory queries where constraint satisfaction is mandatory.

### 7. Decision Criteria for Pattern Selection

Choose your retrieval pattern based on these factors:

| Factor | Favors Global-First | Favors Local-First | Favors Hybrid |
|---|---|---|---|
| Query specificity | Low (broad/thematic) | High (entity-centric) | Mixed |
| Entity mention in query | None/few | Clear anchor entities | Some entities + broad scope |
| Required traversal depth | Shallow (summaries) | 1-2 hops | Variable |
| Domain graph structure | Dense communities | Hub-spoke or sparse | Mixed topology |
| Latency tolerance | Moderate | Low | Higher acceptable |
| Recall requirements | High breadth | High precision | Both critical |

**Additional considerations**:
- If queries are predominantly factoid with clear entities, start with Local-First.
- If queries are predominantly exploratory or thematic, start with Global-First.
- If query types are mixed or unpredictable, use U-Shaped Hybrid as the default.
- Add Query Decomposition on top of any base pattern for multi-hop questions.
- Layer Temporal or Constraint-Guided filtering as needed based on domain requirements.

### 8. Fallback Strategies

When primary retrieval returns insufficient or no results:

**Iterative Deepening**:
- Increase the hop count by 1 and re-retrieve.
- Useful when the answer exists in the graph but is further from seed entities than expected.
- Cap at a maximum depth (e.g., 4 hops) to prevent runaway traversal.

**Query Relaxation**:
- Remove the most restrictive constraint and re-query.
- Order of relaxation: attribute value constraints first, then type constraints, then temporal constraints.
- Log each relaxation step for provenance.

**Expanding Search Scope**:
- If local retrieval fails, escalate to global retrieval.
- If a single community search fails, search adjacent communities.
- Broaden the embedding similarity threshold by a configurable step (e.g., reduce from 0.8 to 0.7).

**Parallel Exploration**:
- Run multiple retrieval patterns simultaneously and merge results.
- More expensive but useful when query type is ambiguous.
- Use result overlap as a confidence signal: information found by multiple patterns is more likely relevant.

### 9. Query Rewriting Strategies

Before executing retrieval, rewrite the query to improve match quality:

**Entity Disambiguation**:
- Resolve ambiguous mentions using graph context. "Apple" in a technology corpus resolves to the company; in a nutrition corpus, to the fruit.
- Use entity type hints from the query structure.
- Maintain an alias table mapping common variations to canonical entity names.

**Term Expansion Using Graph Context**:
- Expand query terms with synonyms and related concepts from the graph ontology.
- Example: "heart attack" expands to include "myocardial infarction", "MI", "cardiac event".
- Use the graph's hierarchical structure: if the query mentions a parent category, optionally include child entities.
- Control expansion aggressiveness to avoid topic drift. One level of synonym expansion is typically safe; two levels risks introducing noise.

**Structural Query Hints**:
- Detect implied graph patterns in natural language queries.
- "What connects A to B?" implies a path-finding query.
- "All X that have property Y" implies a filtered traversal.
- "How has Z changed?" implies temporal traversal.
- Annotate the query with these structural hints to guide pattern selection.

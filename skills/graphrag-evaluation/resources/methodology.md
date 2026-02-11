# GraphRAG Evaluation Methodology

> This resource supports **Steps 1-6** of the [GraphRAG Evaluation](../SKILL.md) workflow.

## WHY

GraphRAG systems have multiple failure points that compound through the pipeline. Errors in knowledge graph construction propagate to retrieval, which propagates to answer generation. A missing entity means a missing retrieval path, which means an incomplete or hallucinated answer. Without systematic evaluation across every dimension, teams cannot distinguish between a KG construction problem and a retrieval problem and a generation problem.

Specific failure modes that demand structured evaluation:

- **KG construction errors**: Missed entities, incorrect relations, inconsistent schemas, and duplicate nodes degrade downstream performance silently. A system can appear to work on simple queries while failing on complex ones because critical bridging entities were never extracted.
- **Retrieval misses**: Graph traversal may fail to find relevant subgraphs, especially for multi-hop queries where the path between question entities passes through intermediate nodes. Context recall measures whether the retrieval stage found everything it needed to.
- **Answer hallucinations**: LLMs generate fluent text regardless of evidence quality. Without measuring grounding rate, teams cannot tell whether answers come from retrieved KG evidence or from the LLM's parametric memory (which may be outdated or wrong).
- **Reasoning failures**: Multi-step reasoning is particularly fragile. An error in step 2 of a 4-step reasoning chain produces a confidently wrong final answer. Process-oriented evaluation catches these intermediate failures.
- **Regression risk**: System changes (new data, updated models, modified prompts) can degrade performance in non-obvious ways. Automated evaluation pipelines catch regressions before they reach users.

Systematic evaluation catches these issues early, isolates root causes to specific components, and provides the evidence needed to prioritize improvements.

## WHAT

### 1. KG Completeness Evaluation

KG completeness measures how well the knowledge graph captures the information present in source documents. An incomplete KG limits the ceiling of system performance regardless of how good retrieval and generation are.

#### Entity Coverage

Entity coverage measures what percentage of expected entities are extracted and represented in the knowledge graph.

**Measurement approach:**
- Define a gold-standard entity set from a representative document sample (manual annotation or expert review)
- Extract the entity set from the KG for the same documents
- Calculate coverage: (entities in KG that match gold standard) / (total entities in gold standard)
- Break down by entity type (person, organization, concept, event) to identify systematic gaps

**RAKG-style evaluation:** Use an LLM to extract an "ideal" knowledge graph from source documents, then compare against the actual KG. This automates gold-standard creation but requires validation of the LLM-generated ideal graph against expert annotations on a sample.

**Thresholds:**
- Below 70%: Critical gaps likely causing retrieval failures
- 70-85%: Acceptable for many use cases but multi-hop queries may suffer
- Above 85%: Strong coverage; focus evaluation effort on other dimensions

#### Relation Completeness

Relation completeness measures whether key relationships between entities are captured, not just the entities themselves.

**Measurement approach:**
- From the gold-standard annotation, extract expected relations (entity-relation-entity triples)
- Compare against actual KG triples
- Calculate: (matched triples) / (total expected triples)
- Pay special attention to bridging relations that connect different topic clusters, since these are critical for multi-hop retrieval

#### Schema Quality

Schema quality measures the consistency and normalization of the knowledge graph structure.

**Assessment criteria:**
- Type consistency: Are equivalent entities assigned the same type?
- Relation normalization: Are equivalent relationships expressed with consistent predicates?
- Duplicate detection: Are there redundant nodes representing the same real-world entity?
- Orphan nodes: Are there disconnected entities that should be linked?

**Comparison against gold-standard or expert annotations:** For high-stakes domains, have domain experts review a stratified sample of the KG (sample across entity types, relation types, and source documents) and score for accuracy and consistency.

### 2. Retrieval Quality Evaluation

Retrieval quality measures how effectively the system finds relevant KG subgraphs for a given query.

#### Context Recall (C-Rec)

Context recall measures whether the retrieval stage found all the relevant pieces of information needed to answer a query correctly.

**Definition:** C-Rec = (relevant items retrieved) / (total relevant items that exist)

**Measurement approach:**
- For each test query, define the set of KG elements (entities, relations, subgraphs) needed to construct a correct answer
- Run the retrieval pipeline and capture what was actually retrieved
- Calculate recall per query and aggregate across the test set
- Low context recall directly causes incomplete or incorrect answers

#### Context Precision

Context precision measures what fraction of retrieved items were actually relevant to the query.

**Definition:** Context Precision = (relevant items retrieved) / (total items retrieved)

**Measurement approach:**
- For each test query, annotate each retrieved KG element as relevant or irrelevant
- Calculate precision per query and aggregate
- Low precision means the LLM receives noisy context, increasing hallucination risk and token costs

#### Multi-hop Coverage

Multi-hop coverage measures whether the retrieval system finds the complete paths needed for multi-step reasoning.

**Measurement approach:**
- Design queries that require traversing 2, 3, or more hops in the KG
- For each query, identify the required path(s) through the graph
- Check whether retrieval returned all nodes and edges on the required path(s)
- Partial path retrieval is a common failure mode: the system finds the start and end but misses bridging entities

#### Latency and Throughput Benchmarks

**Key measurements:**
- Query latency: p50, p95, p99 response times for retrieval
- Throughput: queries per second under load
- Scaling behavior: how latency changes with KG size and query complexity
- Compare graph traversal latency against vector search latency to quantify the overhead of graph-based retrieval

### 3. Answer Correctness Evaluation

Answer correctness measures the quality of the final generated response.

#### Factual Accuracy

**Measurement approach:**
- Compare generated answers against ground-truth answers (human-written reference answers)
- Use both automated metrics (exact match, F1 on answer tokens, semantic similarity) and human evaluation
- For automated evaluation, LLM-as-judge can assess factual consistency between generated and reference answers
- Break down by query type to identify where factual accuracy is weakest

#### Completeness of Answer

**Measurement approach:**
- Define the key information points that a complete answer should contain
- Score what fraction of required information points appear in the generated answer
- Distinguish between partial answers (correct but incomplete) and incorrect answers (wrong information)

#### Citation Accuracy

**Measurement approach:**
- For systems that provide citations or source references, verify that each citation actually supports the claim it is attached to
- Measure: (citations that support their claims) / (total citations provided)
- Also measure citation coverage: (claims with valid citations) / (total claims in answer)
- Citation accuracy is a proxy for grounding quality

#### Human Evaluation Protocols

**Setup:**
- Use at least 2-3 independent evaluators per query
- Provide clear scoring rubrics (not just "rate quality 1-5")
- Calculate inter-annotator agreement (Cohen's kappa or Krippendorff's alpha)
- Use a stratified sample across query types and difficulty levels
- Blind evaluators to which system produced which answer when doing comparative evaluation

### 4. Hallucination Rate Evaluation

Hallucination rate measures how often the system generates claims not supported by retrieved evidence.

#### Intrinsic Hallucination

Intrinsic hallucination occurs when the generated answer contradicts the retrieved evidence.

**Measurement approach:**
- For each generated answer, identify all factual claims
- Check each claim against the retrieved context
- A claim that directly contradicts retrieved evidence is an intrinsic hallucination
- Calculate: (intrinsic hallucinations) / (total claims)

#### Extrinsic Hallucination

Extrinsic hallucination occurs when the generated answer contains claims not supported by any retrieved source, even if those claims happen to be true.

**Measurement approach:**
- For each factual claim in the answer, check whether any retrieved context supports it
- Claims with no supporting evidence in the retrieved context are extrinsic hallucinations
- Calculate: (extrinsic hallucinations) / (total claims)
- This is typically higher than intrinsic hallucination and represents the LLM relying on parametric knowledge

#### KG Grounding Rate

KG grounding rate measures what percentage of generated claims can be traced back to specific KG entities and relations.

**Measurement approach:**
- For each claim, attempt to identify the KG triple(s) that support it
- Calculate: (claims traceable to KG) / (total claims)
- Higher grounding rate indicates the system is using the KG effectively rather than falling back to parametric generation
- This is the most direct measure of whether the "graph" in GraphRAG is actually contributing

#### Comparison: With vs Without Graph Augmentation

Run identical queries through the full GraphRAG system and through a version with graph augmentation disabled (pure vector RAG or LLM-only). Compare hallucination rates to quantify the value of graph grounding.

**Expected pattern:** Graph augmentation should reduce extrinsic hallucination by providing structured evidence. If hallucination rates are similar with and without the graph, the graph component is not contributing effectively.

### 5. Reasoning Depth Evaluation

Reasoning depth measures the system's ability to perform multi-step reasoning correctly.

#### Single-hop vs Multi-hop Query Handling

**Test design:**
- Single-hop: Questions answerable from a single KG triple (e.g., "What is the capital of France?")
- Two-hop: Questions requiring one intermediate entity (e.g., "What country is the employer of [person] headquartered in?")
- Three-hop and beyond: Questions requiring multiple intermediate steps
- Measure accuracy at each hop count to identify where performance degrades

#### Correct Chain-of-Reasoning Verification

**Measurement approach:**
- For multi-hop queries, examine not just the final answer but the intermediate reasoning steps
- Verify each step against the KG: does the intermediate conclusion follow from the retrieved evidence?
- A correct final answer with an incorrect reasoning chain is a concern (the system may have gotten lucky)

#### Process-Oriented Evaluation

Process-oriented evaluation assesses whether each step in the reasoning chain is correct, not just the final answer.

**Measurement approach:**
- Decompose each multi-hop query into its constituent reasoning steps
- Evaluate each step independently for correctness
- Calculate stepwise accuracy: (correct steps) / (total steps)
- Identify common failure patterns: which types of reasoning steps fail most often?
- This catches cases where the final answer is correct by chance despite flawed intermediate reasoning

### Baseline Comparison Approaches

Baselines provide context for interpreting evaluation results. Without baselines, a 75% accuracy score is meaningless: is that good or bad?

**Required baselines:**
1. **Pure vector RAG**: Same queries, same documents, but retrieval uses vector similarity search without graph structure. This isolates the contribution of the knowledge graph.
2. **LLM only (no RAG)**: Same queries answered by the LLM without any retrieval. This measures the LLM's parametric knowledge baseline.
3. **Different graph configurations**: Vary graph construction parameters (entity types, relation extraction thresholds, graph density) to understand sensitivity.

**Ablation study design:**
- Remove or modify one component at a time
- Measure impact on all evaluation dimensions
- Use this to identify which components contribute most and where to invest improvement effort

### Statistical Significance Testing

When comparing systems, ensure differences are statistically significant rather than due to random variation in the test set.

**Approach:**
- Use paired tests (e.g., paired bootstrap, McNemar's test) since the same test queries are used for all systems
- Report confidence intervals, not just point estimates
- For human evaluation, calculate inter-annotator agreement
- A common threshold: p < 0.05, but report the actual p-value
- With small test sets (under 100 queries), be cautious about claiming significant differences
- Consider effect size (Cohen's d or similar) alongside significance: a statistically significant but tiny improvement may not be practically meaningful

**Sample size guidance:**
- Quick health check: 20-50 queries (sufficient for large effect sizes)
- Standard evaluation: 100-200 queries (sufficient for medium effect sizes)
- Comprehensive benchmark: 500+ queries with stratification across query types and difficulty levels

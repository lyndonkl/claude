# Advanced Reasoning Patterns for GraphRAG

> This resource supports **Step 4** of the [GraphRAG Evaluation](../SKILL.md) workflow.

## WHY

Complex queries require multi-step reasoning that goes far beyond simple lookup. A user asking "Which drugs approved after 2020 target proteins involved in the same pathway as gene X?" requires the system to traverse multiple relationship types, filter by temporal constraints, and aggregate evidence from different parts of the knowledge graph. Verifying that such reasoning is correct is essential for trust, especially in high-stakes domains like healthcare, finance, and legal analysis.

Standard evaluation metrics like answer accuracy only check the final output. A system can arrive at the correct answer through flawed reasoning (lucky guesses, shortcut heuristics, or compensating errors). Process-oriented evaluation of reasoning patterns catches these hidden failures before they manifest as visible errors on harder queries.

Key challenges that motivate reasoning pattern evaluation:

- **Error propagation**: In a 4-step reasoning chain, an error at step 2 produces a confidently wrong answer at step 4. The system shows no uncertainty because each subsequent step follows logically from its (incorrect) premise.
- **Reasoning shortcuts**: LLMs may skip intermediate steps and jump to answers using parametric knowledge rather than actually traversing the graph. This works until the parametric knowledge is wrong or outdated.
- **Incomplete evidence aggregation**: Multi-hop queries often require combining evidence from multiple graph paths. Systems may find one path but miss others, producing partially correct answers.
- **Temporal and causal confusion**: Without explicit reasoning about time ordering and causality, systems conflate correlation with causation or apply outdated information.

Evaluating reasoning patterns systematically reveals which types of reasoning your GraphRAG system handles well and which types need improvement.

## WHAT

### Multi-Step Chain Validation

Multi-step chain validation verifies that each link in a reasoning chain is grounded in retrieved KG evidence and that the chain as a whole produces a correct conclusion.

#### Grounding Each Reasoning Step

Every reasoning step should be traceable to specific KG triples or subgraphs. For a query like "What is the revenue of the company that acquired startup X?", the chain is:

1. **Step 1**: Identify which company acquired startup X (requires: acquisition relation in KG)
2. **Step 2**: Look up the revenue of that company (requires: financial data relation in KG)

Each step must be independently verifiable against the KG. If step 1 retrieves the wrong acquirer, step 2 will look up the wrong company's revenue and produce a confidently incorrect answer.

**Evaluation protocol:**
- Decompose multi-hop test queries into their constituent steps
- For each step, record which KG triples were used as evidence
- Verify that the evidence actually supports the intermediate conclusion
- Flag steps where the conclusion does not follow from the retrieved evidence

#### Stepwise Verification Against KG

For each intermediate conclusion in the reasoning chain, verify it against the KG independently of the other steps.

**Approach:**
- Extract the intermediate claim (e.g., "Company Y acquired startup X")
- Query the KG directly for this specific claim
- Compare the direct KG query result with what the reasoning chain produced
- Discrepancies indicate reasoning errors even if the final answer happens to be correct

#### KG-RAR Pattern: Retrieve-at-Each-Step

The KG-RAR (Knowledge Graph Retrieval-Augmented Reasoning) pattern retrieves fresh KG evidence at each step of the chain-of-thought, rather than retrieving all context upfront.

**How it works:**
1. Parse the query into reasoning steps
2. At step 1, retrieve relevant KG subgraph for the first sub-question
3. Generate intermediate answer for step 1
4. At step 2, use the intermediate answer to formulate a new retrieval query
5. Retrieve relevant KG subgraph for step 2
6. Continue until the final answer is reached

**Evaluation:**
- Compare accuracy of retrieve-once vs retrieve-at-each-step approaches
- Measure whether intermediate retrievals find more relevant evidence
- Track retrieval latency overhead of multiple retrieval rounds
- Assess whether retrieve-at-each-step reduces error propagation

#### Error Propagation Detection

Error propagation occurs when an incorrect intermediate step leads to a wrong final conclusion.

**Detection approach:**
- For queries where the final answer is wrong, trace backward through the reasoning chain
- Identify the first step where the reasoning went wrong
- Categorize the error: retrieval failure (relevant triple not found), reasoning failure (correct evidence but wrong conclusion), or grounding failure (conclusion not supported by evidence)
- Calculate error propagation rate: (queries with intermediate errors) / (total multi-hop queries)

**Common propagation patterns:**
- Entity confusion: retrieving information about the wrong entity with a similar name
- Relation misinterpretation: using the right entities but the wrong relationship
- Scope errors: applying information from one context to a different context
- Temporal errors: using outdated information when more recent data exists

### Pattern Matching

Pattern matching uses the structural properties of the knowledge graph to find relevant information and analogies.

#### Structural Pattern Matching in Graphs

Find subgraphs in the KG that match a structural pattern derived from the query.

**Example:** For "Find all drugs that interact with proteins in pathway P and have been approved by the FDA":
- Pattern: (Drug)--[interacts_with]-->(Protein)--[part_of]-->(Pathway:P), (Drug)--[approved_by]-->(Agency:FDA)
- The system must find all subgraph instances matching this pattern

**Evaluation:**
- Define a set of structural patterns with known matches in the KG
- Measure recall (what fraction of true matches were found) and precision (what fraction of returned matches are correct)
- Test with patterns of increasing complexity (2-node, 3-node, 4+ node patterns)
- Measure how pattern matching accuracy degrades with pattern complexity

#### Metapath-Guided Pattern Retrieval

Metapaths define abstract path types through the KG schema (e.g., Author-writes-Paper-cites-Paper-written_by-Author). Metapath-guided retrieval uses these schema-level patterns to guide traversal.

**Evaluation:**
- Define metapaths relevant to your domain
- For each metapath, generate queries that require traversal along that path
- Measure whether the retrieval system correctly follows the metapath
- Compare metapath-guided retrieval against unguided graph traversal

#### Analogy Detection via Subgraph Embedding Similarity

Detect analogies by finding structurally similar subgraphs in different parts of the KG.

**Example:** "Is the relationship between company A and market X similar to company B and market Y?"

**Evaluation:**
- Create analogy test sets with known analogous subgraphs
- Measure whether the system correctly identifies structural similarity
- Test with varying degrees of analogy (exact structural match, partial match, no match)
- Assess robustness to surface-level differences (different entity names but same structural pattern)

### Hypothesis Verification

Hypothesis verification uses the KG to confirm or refute claims generated by the LLM.

#### Using KG to Confirm or Refute LLM Hypotheses

When the LLM generates a hypothesis or candidate answer, the system can query the KG to check whether evidence supports or contradicts it.

**Evaluation protocol:**
- Generate a set of true and false hypotheses about entities in the KG
- For each hypothesis, run the verification pipeline
- Measure: true positive rate (correctly confirmed true hypotheses), true negative rate (correctly refuted false hypotheses), false positive rate (incorrectly confirmed false hypotheses), false negative rate (incorrectly refuted true hypotheses)
- The false positive rate is critical: incorrect confirmation of false hypotheses is a form of hallucination

#### Evidence Aggregation from Multiple Graph Paths

Complex hypotheses may require evidence from multiple independent paths in the KG.

**Evaluation:**
- Design hypotheses that require 2, 3, or more independent evidence paths
- Measure whether the system finds all relevant paths
- Assess how the system combines evidence from multiple paths (does it weight conflicting evidence appropriately?)
- Test with cases where paths provide contradictory evidence

#### Confidence Scoring Based on Evidence Strength

The system should express higher confidence when multiple independent paths support a conclusion and lower confidence when evidence is thin or contradictory.

**Evaluation:**
- Create test cases with varying evidence strength (strong support, weak support, mixed evidence, no evidence)
- Measure calibration: does stated confidence correlate with actual accuracy?
- High-confidence wrong answers are worse than low-confidence wrong answers
- Plot calibration curves: for answers where the system says it is 90% confident, is it correct approximately 90% of the time?

### Causal Reasoning

Causal reasoning goes beyond correlation to establish cause-and-effect relationships using KG structure and temporal information.

#### Temporal Causality from Event Sequences

If event A consistently precedes event B in the KG's temporal data, this suggests (but does not prove) a causal relationship.

**Evaluation:**
- Create test cases with known causal relationships represented in the KG
- Create distractor cases with temporal correlation but no causation
- Measure whether the system correctly distinguishes causation from correlation
- Assess handling of confounding variables (event C causes both A and B)

#### Causal Chain Extraction from KG Paths

Extract multi-step causal chains by following directed causal relations in the KG.

**Evaluation:**
- Define known causal chains in the KG (e.g., Drug-->inhibits-->Enzyme-->regulates-->Pathway-->affects-->Symptom)
- Test whether the system can extract and articulate complete causal chains
- Measure accuracy at each step of the chain
- Test with chains of varying length (2-step, 3-step, 4+ step)

#### Counterfactual Reasoning Using Alternative Paths

Counterfactual reasoning asks "what would happen if X were different?" by exploring alternative paths in the KG.

**Evaluation:**
- Design counterfactual queries with known answers (e.g., "If drug A had not been approved, what alternative treatments exist?")
- Measure whether the system correctly identifies alternative paths
- Assess whether the system appropriately qualifies counterfactual answers as hypothetical
- Test robustness: does changing the counterfactual premise produce appropriately different answers?

### Test Design for Reasoning Evaluation

A comprehensive reasoning evaluation requires test sets that cover different reasoning types at varying difficulty levels.

#### Single-Hop Factual Recall Tests

**Purpose:** Establish baseline performance on simple lookups.

**Design:**
- Questions answerable from a single KG triple
- Example: "What year was company X founded?"
- Expected accuracy should be very high (above 90%); lower accuracy indicates fundamental retrieval or KG problems
- Include 30-50 questions across different entity and relation types

#### Multi-Hop Bridge Entity Tests

**Purpose:** Test the ability to reason through intermediate entities.

**Design:**
- Questions requiring 2-3 hops through the KG
- The "bridge entity" is an intermediate node not mentioned in the query
- Example: "What university did the CEO of company X attend?" (requires: company-->has_CEO-->person-->attended-->university)
- Include 30-50 questions with varying numbers of hops
- Track accuracy by hop count to identify the reasoning depth ceiling

#### Constraint Satisfaction Tests

**Purpose:** Test the ability to apply filters and constraints during reasoning.

**Design:**
- Questions with explicit constraints (temporal, categorical, numerical)
- Example: "List all products launched after 2022 in the healthcare category with revenue above $10M"
- Requires combining graph traversal with filtering
- Include 20-30 questions with 1, 2, and 3 simultaneous constraints
- Measure whether the system correctly applies all constraints vs dropping some

#### Temporal Reasoning Tests

**Purpose:** Test handling of time-dependent information.

**Design:**
- Questions where the answer depends on a specific time point or period
- Example: "Who was the CEO of company X in 2019?" (when the CEO changed in 2020)
- Questions requiring temporal ordering: "Which happened first, event A or event B?"
- Include 20-30 questions covering point-in-time queries, duration queries, and ordering queries
- This is often a weak point for GraphRAG systems; use results to identify temporal modeling gaps

#### Comparative Reasoning Tests

**Purpose:** Test the ability to compare entities across multiple attributes.

**Design:**
- Questions requiring retrieval and comparison of parallel information
- Example: "Compare the market cap and employee count of company X vs company Y"
- Requires retrieving the same attributes for multiple entities and synthesizing a comparison
- Include 15-25 questions with comparisons across 2-4 entities on 2-4 attributes

#### Negative Tests (Questions With No Answer in KG)

**Purpose:** Test the system's ability to recognize when it cannot answer a question from available evidence.

**Design:**
- Questions about entities or relations not in the KG
- Questions where the KG contains partial but insufficient information
- Example: If the KG has no information about a specific topic, the system should say so rather than hallucinate
- Include 15-25 negative questions
- Measure: false answer rate (how often the system fabricates an answer when it should abstain)
- This is one of the most important test categories for hallucination prevention

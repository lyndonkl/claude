# Domain-Specific GraphRAG Patterns

> This resource supports **Step 5** of the [GraphRAG System Design](../SKILL.md) workflow.

## WHY: Domains Demand Specialization

Each domain has unique requirements for knowledge representation, compliance, retrieval patterns, and quality validation that generic GraphRAG architectures cannot address out of the box. A healthcare GraphRAG system must navigate HIPAA constraints and medical ontologies; a financial system must track temporal facts and regulatory audit trails; a legal system must model precedent networks and statutory hierarchies. Applying domain-specific patterns is the difference between a GraphRAG system that technically works and one that delivers real value to domain experts.

Domain specialization affects every layer of the architecture:
- **Schema**: Entity types and relationship types are domain-defined (patients, drugs, conditions vs. companies, transactions, regulations)
- **Ontology**: Established vocabularies provide standardized entity classification and enable interoperability
- **Retrieval**: Query patterns differ (clinical decision support vs. fraud detection vs. legal research)
- **Compliance**: Regulatory requirements constrain data access, storage, and audit capabilities
- **Validation**: Domain experts define what "correct" retrieval looks like

## WHAT: Domain Adaptations

### Healthcare

Healthcare GraphRAG systems support clinical decision-making, drug interaction analysis, patient trajectory tracking, and medical literature retrieval. The domain is characterized by rich formal ontologies, strict regulatory requirements, and life-critical accuracy demands.

**Ontologies and Vocabularies:**
- **UMLS (Unified Medical Language System)**: Meta-thesaurus linking 200+ medical vocabularies; provides concept unique identifiers (CUIs) for entity normalization across sources
- **SNOMED CT**: Comprehensive clinical terminology with hierarchical relationships; 350,000+ concepts covering clinical findings, procedures, body structures
- **MeSH (Medical Subject Headings)**: NLM's controlled vocabulary for indexing biomedical literature; essential for literature-based GraphRAG
- **DrugBank**: Comprehensive drug database with drug-drug interactions, drug-target relationships, pharmacological data; critical for medication-related queries
- **ICD-10/11**: Diagnosis coding system; bridges clinical data to administrative/billing data

**Graph Architecture Patterns:**

**Layered Patient Graph (MedGraphRAG Triple Graph Pattern):**
The MedGraphRAG approach uses a three-layer graph structure that separates concerns and enables trust-differentiated retrieval:

```
Layer 3: Medical Dictionary Layer
  - Formal ontology nodes (UMLS concepts, SNOMED terms, MeSH headings)
  - Canonical relationships from medical knowledge bases
  - Static, curated, high confidence

Layer 2: Medical Literature Layer
  - Entities and relationships extracted from published research
  - Clinical trial data, systematic reviews, practice guidelines
  - Periodically updated, medium confidence, citation-backed

Layer 1: Patient Data Layer
  - Patient-specific entities (conditions, medications, labs, procedures)
  - Temporal relationships (prescribed_on, diagnosed_at, resolved_by)
  - Real-time updates, variable confidence, source-attributed
```

Cross-layer edges connect patient data to literature evidence and literature to canonical ontology, enabling queries that traverse from a specific patient's condition through supporting literature to formal medical knowledge.

**Drug Interaction Subgraph:**
For medication safety queries, build focused subgraphs around the patient's medication list:
1. Seed with patient's current medications (graph nodes)
2. Expand to all known drug-drug interactions (DrugBank edges)
3. Include mechanism of action nodes to explain interaction pathways
4. Filter by clinical significance (major, moderate, minor)
5. Attach literature evidence from Layer 2

**Compliance and Access Control:**
- **HIPAA**: Patient data (Layer 1) requires role-based access control at the graph level; implement graph-based access control where node/edge visibility is filtered by user role
- **De-identification**: Patient identifiers must be separated from clinical data in the graph; use reference nodes with access-controlled edges
- **Audit trails**: All queries against patient data must be logged with timestamp, user, and query scope
- **Minimum necessary**: Subgraph extraction should return only the minimum data needed for the query

**Use Cases:**
- Clinical decision support: "Given this patient's conditions and medications, what are the contraindications for prescribing drug X?"
- Drug interaction checking: "What interactions exist between these 5 medications, and what is the clinical significance?"
- Patient trajectory analysis: "How has this patient's condition progressed over the past 12 months, and what treatments were effective?"
- Literature-grounded QA: "What does recent evidence say about treatment Y for condition Z in patients with comorbidity W?"

### Finance

Financial GraphRAG systems support risk analysis, fraud detection, compliance checking, and market intelligence. The domain is characterized by temporal data, complex entity networks, regulatory requirements, and real-time processing needs.

**Ontologies and Vocabularies:**
- **FIBO (Financial Industry Business Ontology)**: OMG standard ontology covering financial instruments, business entities, indices, and indicators; provides standardized entity classification for financial knowledge graphs
- **Custom corporate taxonomies**: Organization-specific entity hierarchies (product lines, business units, risk categories) that extend FIBO for internal use
- **LEI (Legal Entity Identifier)**: Global standard for uniquely identifying legal entities in financial transactions; essential for entity resolution across data sources
- **ISDA CDM (Common Domain Model)**: Standard representation for financial derivative transactions

**Graph Architecture Patterns:**

**Temporal Financial Graph:**
Financial data is inherently temporal -- prices change, positions shift, corporate structures evolve. The graph must capture time-indexed state:

```
Temporal Edges:
  (:Company)-[:HAS_PRICE {date, open, close, volume}]->(:StockPrice)
  (:Company)-[:OWNS {from_date, to_date, percentage}]->(:Subsidiary)
  (:Fund)-[:HOLDS {date, quantity, value}]->(:Security)

Temporal Queries:
  - "What was the ownership structure of Company X on date Y?"
  - "How has Fund Z's portfolio composition changed over Q3?"
  - "What positions did Entity A hold before the regulatory event?"
```

Design temporal edges with valid_from and valid_to properties. Use snapshot subgraphs for point-in-time queries.

**Transaction Network for Fraud Detection:**
Model financial transactions as a network to detect suspicious patterns:
1. Nodes: accounts, entities, addresses, devices
2. Edges: transactions with amount, timestamp, type, channel
3. Patterns: circular transactions (A->B->C->A), rapid fan-out (one source to many destinations), structuring (many transactions just below reporting threshold)
4. Graph algorithms: community detection to find clusters of suspicious accounts, centrality to identify key nodes in money laundering networks

**Compliance and Audit:**
- **Regulatory reporting**: Graph structure enables automated generation of required reports (beneficial ownership chains, counterparty exposure)
- **Audit trails**: Every fact in the graph carries provenance (source system, extraction timestamp, confidence score) for regulatory examination
- **Temporal fact tracking**: Regulators require point-in-time views of data; temporal graph enables "as of date X" queries
- **Data lineage**: Track how derived facts (risk scores, exposure calculations) were computed from base data

**Use Cases:**
- Risk analysis: "What is our total exposure to Company X, including all subsidiaries and related entities?"
- Compliance checking: "Does this transaction pattern match any known money laundering typologies?"
- Market intelligence: "What are the ownership relationships between these entities, and how have they changed in the past year?"
- Regulatory reporting: "Generate the beneficial ownership chain for Entity Y as of reporting date Z"

### Legal

Legal GraphRAG systems support legal research, contract analysis, regulatory compliance tracking, and case-based reasoning. The domain is characterized by hierarchical document structures, complex cross-references, and precedent-based reasoning.

**Graph Architecture Patterns:**

**Statute and Regulation Graph:**
Model legal codes as hierarchical graphs with cross-reference edges:
```
(:Code)-[:CONTAINS]->(:Title)-[:CONTAINS]->(:Chapter)-[:CONTAINS]->(:Section)
(:Section)-[:REFERENCES]->(:Section)  // Cross-references
(:Section)-[:AMENDED_BY {date, public_law}]->(:Amendment)
(:Section)-[:INTERPRETED_BY]->(:CaseDecision)
```

**Precedent Network:**
Build a citation network of case decisions to enable precedent-based reasoning:
1. Nodes: case decisions with metadata (court, date, jurisdiction, outcome)
2. Edges: citation relationships (cites, distinguishes, overrules, follows)
3. Centrality analysis identifies landmark cases (most cited)
4. Community detection finds clusters of related case law
5. Temporal filtering enables precedent analysis within jurisdictions and time periods

**Case-Based Reasoning Subgraph:**
For a new legal question, build a subgraph of relevant precedents:
1. Identify key legal concepts in the query (entity extraction against legal taxonomy)
2. Retrieve cases addressing those concepts (graph traversal through concept-case edges)
3. Rank by relevance: jurisdiction match, court level, recency, citation count
4. Expand to include cases that distinguish or overrule the primary results
5. Present the reasoning chain: concept -> leading case -> supporting cases -> distinguishing cases

**Use Cases:**
- Legal research: "What cases have addressed the interpretation of Section X in the context of Y?"
- Contract analysis: "Does this contract clause conflict with any regulatory requirements in jurisdiction Z?"
- Regulatory compliance: "What regulations apply to activity X, and what are the current compliance requirements?"
- Precedent analysis: "What is the current state of law on topic Y, considering recent decisions?"

### Research and Academic

Academic GraphRAG systems support literature discovery, collaboration identification, research trend analysis, and knowledge synthesis across scientific publications.

**Graph Architecture Patterns:**

**Citation Network:**
```
(:Paper {title, abstract, year, venue})-[:CITES]->(:Paper)
(:Paper)-[:AUTHORED_BY]->(:Author)
(:Author)-[:AFFILIATED_WITH {from, to}]->(:Institution)
(:Paper)-[:ADDRESSES]->(:ResearchTopic)
(:Paper)-[:USES_METHOD]->(:Method)
(:Paper)-[:USES_DATASET]->(:Dataset)
```

**Author Collaboration Graph:**
- Edges between co-authors weighted by number of joint publications
- Community detection identifies research groups and collaboration clusters
- Bridging nodes (authors connecting different communities) identify interdisciplinary researchers
- Temporal analysis reveals evolving collaboration patterns

**Concept Taxonomy:**
- Hierarchical topic graph built from venue classifications, keyword co-occurrence, and citation-based topic modeling
- Community-Based Global Summarization pattern is particularly effective: detect topic communities, generate summaries, retrieve relevant research areas for broad queries

**Use Cases:**
- Literature discovery: "What recent papers address problem X using approach Y, and who are the leading authors?"
- Collaboration finding: "Which researchers bridge the fields of A and B, and could serve as collaborators?"
- Research trend analysis: "How has the research focus on topic Z evolved over the past 5 years?"
- Knowledge synthesis: "Summarize the state of the art on topic W across all relevant subfields"

### Enterprise and General

Enterprise GraphRAG systems integrate diverse internal knowledge sources for organizational QA, knowledge management, and employee assistance.

**Graph Architecture Patterns:**

**Organizational Knowledge Graph:**
Integrate multiple enterprise data sources into a unified graph:
```
(:Employee)-[:REPORTS_TO]->(:Employee)
(:Employee)-[:MEMBER_OF]->(:Team)
(:Team)-[:OWNS]->(:Project)
(:Project)-[:PRODUCES]->(:Document)
(:Document)-[:MENTIONS]->(:Product)
(:Product)-[:USES]->(:Technology)
(:Document)-[:TAGGED_WITH]->(:Topic)
```

**Activity-Centric Knowledge Graph:**
Model organizational activity as first-class nodes connecting people, artifacts, and outcomes:
```
(:Meeting {date, decisions})-[:ATTENDED_BY]->(:Employee)
(:Meeting)-[:PRODUCED]->(:ActionItem)
(:ActionItem)-[:ASSIGNED_TO]->(:Employee)
(:ActionItem)-[:RELATES_TO]->(:Project)
(:Decision)-[:MADE_IN]->(:Meeting)
(:Decision)-[:AFFECTS]->(:Product)
```

**Multi-Source Integration Pattern:**
1. Define a common entity schema that spans all sources (Confluence, Jira, Slack, GitHub, Google Drive)
2. Build source-specific extractors that map to the common schema
3. Entity resolution across sources (same project referenced in Jira and Confluence)
4. Provenance tracking: every graph node links back to its source system and document
5. Incremental updates via source system webhooks or periodic sync

**Use Cases:**
- Internal knowledge management: "What is our team's policy on X, and where is it documented?"
- Multi-source QA: "What decisions were made about Project Y, and what is the current status of action items?"
- Employee assistance: "Who on the team has experience with Technology Z, and what projects used it?"
- Onboarding support: "What are the key systems, processes, and contacts a new engineer needs to know about?"

## Cross-Domain Design Principles

Regardless of domain, several design principles apply to all domain-specific GraphRAG systems:

1. **Start with the domain ontology**: Use established vocabularies (UMLS, FIBO, etc.) rather than inventing entity types from scratch. This enables interoperability and leverages decades of domain expertise.

2. **Layer by trust**: Separate curated knowledge from extracted knowledge from user-specific data. This enables trust-differentiated retrieval and quality scoring.

3. **Design for the query, not the data**: Schema and retrieval patterns should be driven by the queries users will ask, not by the structure of source data. Work backward from query patterns to graph design.

4. **Build compliance in, not on**: Access control, audit logging, and data governance should be part of the graph architecture from the start, not bolted on after deployment.

5. **Validate with domain experts**: The ultimate quality measure is whether domain experts find the system's retrieval and generation useful and accurate. Build evaluation loops that include expert review.

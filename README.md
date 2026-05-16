# Claude Code Skills Collection

![Skills](https://img.shields.io/badge/skills-216-blue) ![Agents](https://img.shields.io/badge/agents-43-blue) ![Status](https://img.shields.io/badge/status-active-brightgreen) [![Run in Smithery](https://smithery.ai/badge/skills/lyndonkl)](https://smithery.ai/skills?ns=lyndonkl&utm_source=github&utm_medium=badge)

A production-ready library of **216 skills** and **43 orchestrating agents** for Claude Code — covering thinking frameworks, research, writing, design, data/ML, corporate finance, game theory, fantasy baseball, household personal finance, and a 9-agent team for growing a Substack publication.

**Install in 30 seconds:**

```
/plugin marketplace add lyndonkl/claude
/plugin install thinking-frameworks-skills
```

---

## I want to…

Pick the fastest entry point for what you're trying to do. Most users start with an **agent** (which orchestrates many skills); power users invoke **skills** directly.

| I want to… | Start here |
|---|---|
| Value a company / analyze an M&A target / plan an IPO | [`company-analyst`](agents/company-analyst.md), [`acquisition-analyst`](agents/acquisition-analyst.md), [`ipo-strategist`](agents/ipo-strategist.md), [`special-situations-analyst`](agents/special-situations-analyst.md) |
| Research a thematic macro trend cluster (AI compute cycle, demographic shift, climate transition, etc.) | [`macroeconomic-analyst`](agents/macroeconomic-analyst.md) |
| Reverse-engineer a real product's vision / strategy / tactics / ML and system architecture from public material | [`product-strategist`](agents/product-strategist.md) |
| Decide how to allocate capital (debt / dividends / projects) | [`capital-allocation-strategist`](agents/capital-allocation-strategist.md) |
| Manage my Yahoo Fantasy Baseball team | [`mlb-fantasy-coach`](agents/mlb-fantasy-coach.md) + 6 MLB specialists |
| Run my household finances from PDF statements (drop in, briefing + dashboard out) | [`household-cfo`](agents/household-cfo.md) + 8 household specialists |
| Write a paper / grant / recommendation letter | [`scientific-writing-editor`](agents/scientific-writing-editor.md) |
| Improve any piece of writing (blog, memo, essay) | [`writing-assistant`](agents/writing-assistant.md) |
| Make a calibrated forecast or probability estimate | [`superforecaster`](agents/superforecaster.md) |
| Design a dashboard, viz, or UI grounded in cognition | [`cognitive-design-architect`](agents/cognitive-design-architect.md) |
| Build a GraphRAG / knowledge-graph retrieval system | [`graphrag-specialist`](agents/graphrag-specialist.md) |
| Design equivariant / symmetry-aware neural networks | [`geometric-deep-learning-architect`](agents/geometric-deep-learning-architect.md) |
| Build geometric intuition for ML math (attention, PCA, eigenvectors, high-dim spaces) | [`math-intuition-coach`](agents/math-intuition-coach.md) |
| Get a weekly digest of new bioRxiv / medRxiv / PubMed / arXiv papers (life sciences + CS / ML) against my keyword watchlist | [`literature-scan-coach`](agents/literature-scan-coach.md) → [`paper-synthesizer`](agents/paper-synthesizer.md) |
| Grow my Substack / publish intuition-first ML & systems essays | [`librarian`](agents/librarian.md), [`intuition-builder`](agents/intuition-builder.md), [`editor`](agents/editor.md) + 6 more (see `~/Documents/Thinking/substacker/`) |
| Use just one tool (no agent) | Browse the [Skills Index](#skills-index) below |

## How the pieces fit together

```mermaid
flowchart LR
    U([What do you need?]) --> D{Task}
    D -->|Analyze a company| CA[company-analyst<br/>acquisition-analyst<br/>ipo-strategist]
    D -->|Analyze a product| PS[product-strategist]
    D -->|Write something| WA[writing-assistant<br/>scientific-writing-editor]
    D -->|Forecast / decide| SF[superforecaster]
    D -->|Design / visualize| CD[cognitive-design-architect]
    D -->|Fantasy baseball| MLB[mlb-fantasy-coach<br/>+ 6 specialists]
    D -->|Household finances| HF[household-cfo<br/>+ 8 specialists]
    D -->|Knowledge retrieval| GR[graphrag-specialist]
    D -->|Symmetry-aware ML| GDL[geometric-deep-<br/>learning-architect]
    D -->|Math intuition| MI[math-intuition-<br/>coach]
    D -->|Weekly paper digest| LSC[literature-scan-coach<br/>→ paper-synthesizer]
    D -->|One-off tool| SK[Skills Index ▾]
    CA & PS & WA & SF & CD & MLB & HF & GR & GDL & MI & LSC --> S[(216 skills)]
    SK --> S
```

---

## Orchestrating Agents

Agents detect your need and route to the right skills. Each agent's page documents the skills it orchestrates and the workflow it runs.

| Agent | Domain |
|---|---|
| [**writing-assistant**](agents/writing-assistant.md) | Any writing task — structure, revision, stickiness, pre-publish gate |
| [**scientific-writing-editor**](agents/scientific-writing-editor.md) | Manuscripts, grants, letters, reviewer responses, career docs |
| [**superforecaster**](agents/superforecaster.md) | Forecasting and probability via 5-phase calibrated pipeline |
| [**cognitive-design-architect**](agents/cognitive-design-architect.md) | Cognitive design, information architecture, D3 viz, fallacy check |
| [**geometric-deep-learning-architect**](agents/geometric-deep-learning-architect.md) | Symmetry discovery → group ID → equivariant architecture |
| [**math-intuition-coach**](agents/math-intuition-coach.md) | 3Blue1Brown-style geometric intuition for any ML/data math (attention, PCA, gradients, high-dim spaces) |
| [**literature-scan-coach**](agents/literature-scan-coach.md) | Single entry point for a weekly literature-scan project; routes weekly / catch-up / on-demand / re-synthesize intents and spawns paper-synthesizer per run with the right parameters |
| [**paper-synthesizer**](agents/paper-synthesizer.md) | Worker for literature-scan-coach. One window, one digest. Fetches bioRxiv / medRxiv / PubMed / arXiv, filters, clusters by theme, writes the layered-reasoning synthesis with paper links |
| [**skill-creator**](agents/skill-creator.md) | Orchestrates Adler's six-step methodology to transform a methodology document (PDF, markdown, paper, framework guide) into a properly structured Claude Code skill — SKILL.md + resources + rubric |
| [**graphrag-specialist**](agents/graphrag-specialist.md) | Knowledge graph construction, embedding fusion, retrieval orchestration |
| [**company-analyst**](agents/company-analyst.md) | End-to-end company valuation → buy/sell/hold recommendation |
| [**special-situations-analyst**](agents/special-situations-analyst.md) | Distressed / private / high-growth / financial-firm valuation |
| [**macroeconomic-analyst**](agents/macroeconomic-analyst.md) | Deep thematic research on one trend cluster — sub-trends, value chains, beneficiary archetypes, pricing-in assessment, watch-indicators |
| [**product-strategist**](agents/product-strategist.md) | Outside-in layered analysis of a real product — vision, strategy, tactics, operational surface, system & ML architecture map, strategist synthesis |
| [**capital-allocation-strategist**](agents/capital-allocation-strategist.md) | Financing mix, dividends/buybacks, project investment |
| [**acquisition-analyst**](agents/acquisition-analyst.md) | M&A standalone + synergy + max bid |
| [**ipo-strategist**](agents/ipo-strategist.md) | Pre-IPO → post-IPO valuation and pricing range |
| [**mlb-fantasy-coach**](agents/mlb-fantasy-coach.md) | Primary Yahoo Fantasy Baseball orchestrator; morning briefs |
| [**mlb-lineup-optimizer**](agents/mlb-lineup-optimizer.md) | Daily start/sit with advocate + critic variants |
| [**mlb-waiver-analyst**](agents/mlb-waiver-analyst.md) | Weekly add/drop and FAAB bid sizing |
| [**mlb-streaming-strategist**](agents/mlb-streaming-strategist.md) | Weekly pitching plan, two-start SPs, spot starts |
| [**mlb-trade-analyzer**](agents/mlb-trade-analyzer.md) | On-demand trade offer evaluation with always-counter ladder |
| [**mlb-category-strategist**](agents/mlb-category-strategist.md) | Weekly push/punt plan across the 10 H2H categories |
| [**mlb-playoff-planner**](agents/mlb-playoff-planner.md) | July-onward positioning for weeks 21–23 playoff window |
| [**household-cfo**](agents/household-cfo.md) | Master orchestrator + synthesizer for the household finance team; runs per-drop, monthly, and ad-hoc chat |
| [**household-intake-classifier**](agents/household-intake-classifier.md) | Per-PDF document classification + manifest + account matching |
| [**household-bookkeeper**](agents/household-bookkeeper.md) | PDF → reconciled, deduplicated, categorized JSON store with append-only commit |
| [**household-spending-analyst**](agents/household-spending-analyst.md) | Category trends, recurring detection, 60-day cash-flow forecast, seasonal calendar |
| [**household-bills-vigilance**](agents/household-bills-vigilance.md) | Missed bills, duplicate / fraud / anomaly / fee scans with severity-tagged alerts |
| [**household-savings-debt**](agents/household-savings-debt.md) | Goals, emergency fund, debt strategy, mortgage prepay math, rewards optimization |
| [**household-investment-retirement**](agents/household-investment-retirement.md) | Portfolio drift, contribution optimization, TLH with wash-sale awareness, retirement projection |
| [**household-tax-compliance**](agents/household-tax-compliance.md) | Document tracking, deduction tracker, HSA receipt vault, year-end packet for CPA |
| [**household-dashboard-designer**](agents/household-dashboard-designer.md) | Weekly static HTML dashboard with cognitive-design + storytelling + fallacy guard |
| [**librarian**](agents/librarian.md) | Ingest + tag + index a Substack writer's corpus; topic ledger maintenance |
| [**intuition-builder**](agents/intuition-builder.md) | 5 distinct framings (everyday / physical / contrarian / historical / counterfactual) per technical topic |
| [**editor**](agents/editor.md) | Two-pass voice + structural review of drafts; voice gate before publish |
| [**distribution-translator**](agents/distribution-translator.md) | Turn published essays into Substack Note / X thread / LinkedIn post / cross-post blurb |
| [**growth-analyst**](agents/growth-analyst.md) | Weekly Substack CSV → rolling baseline → attribution → per-section report |
| [**trend-scout**](agents/trend-scout.md) | Weekly ML/systems signal digest from ~35 curated intuition-first sources |
| [**technical-reviewer**](agents/technical-reviewer.md) | Pre-publish claim check — simplified / wrong / contested / overclaim classification with primary sources |
| [**curator**](agents/curator.md) | Every 4-6 weeks: section map maintenance; active + reactive; handles per-section voice overlays |
| [**growth-strategist**](agents/growth-strategist.md) | Quarterly (rolling 13-week) strategic zoomout with uncomfortable questions and kill list |

---

## Skills Index

**216 skills** across 7 super-categories. Every skill's full methodology, templates, and evaluation rubric live in its `SKILL.md` — click any entry to drill in.

<details>
<summary><b>🧠 Thinking & Decisions</b> — decision-making, problem-solving, estimation, dialogue, ideation, learning (37 skills)</summary>

### Strategy & decision-making

- **[decision-matrix](skills/decision-matrix/SKILL.md)** — Compare options against weighted criteria to pick defensibly.
- **[expected-value](skills/expected-value/SKILL.md)** — Weight outcomes by probability to choose under uncertainty.
- **[bayesian-reasoning-calibration](skills/bayesian-reasoning-calibration/SKILL.md)** — Update probabilities with evidence and calibrate confidence.
- **[heuristics-and-checklists](skills/heuristics-and-checklists/SKILL.md)** — Prevent recurring errors with fast rules and 5–9 item checklists.
- **[hypotheticals-counterfactuals](skills/hypotheticals-counterfactuals/SKILL.md)** — Stress-test decisions with "what if" scenarios and premortems.
- **[kill-criteria-exit-ramps](skills/kill-criteria-exit-ramps/SKILL.md)** — Define when to stop a project before sunk cost traps you.
- **[alignment-values-north-star](skills/alignment-values-north-star/SKILL.md)** — Connect daily choices to a shared North Star and values.
- **[environmental-scanning-foresight](skills/environmental-scanning-foresight/SKILL.md)** — Spot weak signals and plan scenarios via PESTLE.
- **[portfolio-roadmapping-bets](skills/portfolio-roadmapping-bets/SKILL.md)** — Size and sequence H1/H2/H3 bets with 70-20-10 balance.
- **[prioritization-effort-impact](skills/prioritization-effort-impact/SKILL.md)** — Sort a backlog into Quick Wins, Big Bets, Time Sinks.
- **[project-risk-register](skills/project-risk-register/SKILL.md)** — Identify, score, and monitor project risks by probability × impact.
- **[prototyping-pretotyping](skills/prototyping-pretotyping/SKILL.md)** — Validate demand cheaply before building via fake doors and MVPs.
- **[postmortem](skills/postmortem/SKILL.md)** — Turn failures into learning with blameless timelines and SMART actions.
- **[strategy-and-competitive-analysis](skills/strategy-and-competitive-analysis/SKILL.md)** — Build strategy using Rumelt's kernel, Porter, Blue Ocean, Playing to Win.

### Problem-solving & analysis

- **[decomposition-reconstruction](skills/decomposition-reconstruction/SKILL.md)** — Break complex systems into parts, then recompose with insight.
- **[causal-inference-root-cause](skills/causal-inference-root-cause/SKILL.md)** — Distinguish causation from correlation; find true root causes.
- **[abstraction-concrete-examples](skills/abstraction-concrete-examples/SKILL.md)** — Move between abstract principle and concrete example to clarify.
- **[layered-reasoning](skills/layered-reasoning/SKILL.md)** — Reason consistently across strategic / tactical / operational layers.
- **[negative-contrastive-framing](skills/negative-contrastive-framing/SKILL.md)** — Define fuzzy criteria by showing what they are NOT.
- **[synthesis-and-analogy](skills/synthesis-and-analogy/SKILL.md)** — Integrate sources and transfer insights across domains.
- **[systems-thinking-leverage](skills/systems-thinking-leverage/SKILL.md)** — Find leverage points in feedback loops and system archetypes.

### Estimation & forecasting

- **[estimation-fermi](skills/estimation-fermi/SKILL.md)** — Produce order-of-magnitude estimates via decomposition and bounding.
- **[reference-class-forecasting](skills/reference-class-forecasting/SKILL.md)** — Anchor predictions in base rates from similar past events.
- **[forecast-premortem](skills/forecast-premortem/SKILL.md)** — Stress-test a forecast by assuming it failed; surface tail risks.
- **[scout-mindset-bias-check](skills/scout-mindset-bias-check/SKILL.md)** — Detect and remove bias with reversal tests and confidence audits.
- **[chain-estimation-decision-storytelling](skills/chain-estimation-decision-storytelling/SKILL.md)** — Chain Fermi estimation → EV → narrative into a recommendation.

### Dialogue & deliberation

- **[deliberation-debate-red-teaming](skills/deliberation-debate-red-teaming/SKILL.md)** — Stress-test plans via Oxford debate, fishbowl, devil's advocate.
- **[dialectical-mapping-steelmanning](skills/dialectical-mapping-steelmanning/SKILL.md)** — Steelman both sides and synthesize a principled third way.
- **[chain-roleplay-debate-synthesis](skills/chain-roleplay-debate-synthesis/SKILL.md)** — Multi-expert roleplay and debate for complex decisions.
- **[role-switch](skills/role-switch/SKILL.md)** — Analyze decisions from each stakeholder's perspective to find alignment.

### Ideation & creativity

- **[brainstorm-diverge-converge](skills/brainstorm-diverge-converge/SKILL.md)** — Generate many ideas, cluster, then narrow via dot voting.
- **[constraint-based-creativity](skills/constraint-based-creativity/SKILL.md)** — Turn limitations into creative fuel via strategic constraints.
- **[morphological-analysis-triz](skills/morphological-analysis-triz/SKILL.md)** — Systematically explore design space and resolve contradictions.

### Productivity & learning

- **[focus-timeboxing-8020](skills/focus-timeboxing-8020/SKILL.md)** — Protect attention with Pareto, Pomodoro, and deep-work blocks.
- **[memory-retrieval-learning](skills/memory-retrieval-learning/SKILL.md)** — Build durable retention via spaced repetition and retrieval practice.
- **[socratic-teaching-scaffolds](skills/socratic-teaching-scaffolds/SKILL.md)** — Teach via strategic questions and fading scaffolds.
- **[meta-prompt-engineering](skills/meta-prompt-engineering/SKILL.md)** — Turn vague prompts into reliable, structured, verifiable ones.

</details>

<details>
<summary><b>🔬 Research & Evidence</b> — research design, evidence evaluation, rubrics, ethics, reading methodology, literature scan (17 skills)</summary>

### Research design & evaluation

- **[discovery-interviews-surveys](skills/discovery-interviews-surveys/SKILL.md)** — Run unbiased JTBD interviews and surveys with thematic coding.
- **[design-of-experiments](skills/design-of-experiments/SKILL.md)** — Design rigorous factorial, RSM, and Taguchi experiments.
- **[domain-research-health-science](skills/domain-research-health-science/SKILL.md)** — Formulate PICOT questions and GRADE clinical evidence.
- **[research-claim-map](skills/research-claim-map/SKILL.md)** — Verify claims via triangulation, source grading, confidence calibration.
- **[ethics-safety-impact](skills/ethics-safety-impact/SKILL.md)** — Assess harms, fairness, and mitigations across stakeholders.
- **[evaluation-rubrics](skills/evaluation-rubrics/SKILL.md)** — Design rubrics with calibrated scales and inter-rater reliability.

### Reading methodology (Adler-style; reusable across paper extraction, skill creation, evidence triage)

- **[inspectional-reading](skills/inspectional-reading/SKILL.md)** — Level 1. First-level systematic skim — classify document type, decide whether deeper reading is worth it. Adler's "How to Read a Book" Level 1, generalized.
- **[structural-analysis](skills/structural-analysis/SKILL.md)** — Level 2. Classify content (practical vs theoretical, structure type, completeness 1-5), state unity in one sentence, enumerate parts, define problems. Adler's analytical-reading first stage.
- **[component-extraction](skills/component-extraction/SKILL.md)** — Level 3. Section-by-section extraction of terms, propositions, arguments, solutions. Reading-strategy selection (section-based / windowing / targeted) for the right document size.
- **[synthesis-application](skills/synthesis-application/SKILL.md)** — Level 4. Completeness + logic + applicability gate after component extraction; produces GO / GO_WITH_GAPS / NO_GO verdict. Adler's "Is it true? What of it?" pass.
- **[skill-construction](skills/skill-construction/SKILL.md)** — Construction step. Build SKILL.md + resources + rubric from extracted components at appropriate complexity (Level 1-3).
- **[paper-three-pass-extraction](skills/paper-three-pass-extraction/SKILL.md)** — Three-pass + Five Cs extraction methodology specifically for academic papers. Wraps inspectional-reading as Pass 1; adds Pass 2 (content grasp via structural-analysis + component-extraction) and Pass 3 (deep understanding). Powers the `paper-extractor` agent.

### Literature scan

Domain-neutral primitives for any weekly paper-digest workflow. Powers the `literature-scan-coach` + `paper-extractor` + `paper-synthesizer` pipeline.

- **[fetch-preprint-recent](skills/fetch-preprint-recent/SKILL.md)** — Fetch bioRxiv / medRxiv preprints for a date window with cursor pagination and client-side keyword filter.
- **[fetch-pubmed-recent](skills/fetch-pubmed-recent/SKILL.md)** — Fetch PubMed records for a date window via PubMed MCP when available, E-utilities fallback otherwise.
- **[fetch-arxiv-recent](skills/fetch-arxiv-recent/SKILL.md)** — Fetch arXiv papers for a date window with optional category restriction (cs.LG, cs.CL, stat.ML, q-bio.QM, etc.); Atom XML parsing.
- **[paper-relevance-filter](skills/paper-relevance-filter/SKILL.md)** — Score candidate papers KEEP / REVIEW / DROP on match strength + criteria fit + novelty against last-4-weeks history.
- **[paper-cluster-by-theme](skills/paper-cluster-by-theme/SKILL.md)** — Group filtered papers into 2-5 argument-shaped clusters before synthesis.

</details>

<details>
<summary><b>✍️ Communication & Writing</b> — writing pipeline, scientific writing, audience adaptation (13 skills)</summary>

### General writing

- **[writing-structure-planner](skills/writing-structure-planner/SKILL.md)** — Plan writing architecture via McPhee's structural diagramming.
- **[writing-revision](skills/writing-revision/SKILL.md)** — Run the three-pass revision: clutter, cognitive load, rhythm.
- **[writing-stickiness](skills/writing-stickiness/SKILL.md)** — Make messages memorable using the Heath SUCCESs framework.
- **[writing-pre-publish-checklist](skills/writing-pre-publish-checklist/SKILL.md)** — Final 6-section quality gate before publishing.
- **[communication-storytelling](skills/communication-storytelling/SKILL.md)** — Craft narratives using arcs, tension, and audience framing.
- **[translation-reframing-audience-shift](skills/translation-reframing-audience-shift/SKILL.md)** — Adapt content for a new audience without losing accuracy.
- **[one-pager-prd](skills/one-pager-prd/SKILL.md)** — Write concise one-pagers and PRDs for stakeholder alignment.

### Scientific & academic writing

- **[scientific-manuscript-review](skills/scientific-manuscript-review/SKILL.md)** — Edit IMRaD research manuscripts for clarity and rigor.
- **[grant-proposal-assistant](skills/grant-proposal-assistant/SKILL.md)** — Assist NIH / NSF grant writing with Specific Aims + Strategy.
- **[academic-letter-architect](skills/academic-letter-architect/SKILL.md)** — Craft evidence-based recommendation and nomination letters.
- **[scientific-email-polishing](skills/scientific-email-polishing/SKILL.md)** — Polish editor letters, reviewer responses, collaboration emails.
- **[scientific-clarity-checker](skills/scientific-clarity-checker/SKILL.md)** — Audit scientific claims, hedging, and terminology consistency.
- **[career-document-architect](skills/career-document-architect/SKILL.md)** — Develop research, teaching, diversity statements and CVs.

</details>

<details>
<summary><b>🏗️ Building & Shipping</b> — architecture, design, security, org, product delivery (15 skills)</summary>

### Architecture & product

- **[adr-architecture](skills/adr-architecture/SKILL.md)** — Document architecture decisions with context, options, consequences.
- **[chain-spec-risk-metrics](skills/chain-spec-risk-metrics/SKILL.md)** — Chain spec → risk → success metrics for launches.
- **[roadmap-backcast](skills/roadmap-backcast/SKILL.md)** — Plan backward from deadline to identify critical path and feasibility.
- **[metrics-tree](skills/metrics-tree/SKILL.md)** — Decompose a North Star metric into sub-metrics and leading indicators.

### Design & information architecture

- **[information-architecture](skills/information-architecture/SKILL.md)** — Organize content via card sort, taxonomy, and tree testing.
- **[cognitive-design](skills/cognitive-design/SKILL.md)** — Ground design decisions in perception, memory, and Gestalt.
- **[design-evaluation-audit](skills/design-evaluation-audit/SKILL.md)** — Audit existing designs against cognitive-alignment checklists.
- **[cognitive-fallacies-guard](skills/cognitive-fallacies-guard/SKILL.md)** — Detect chartjunk, misleading axes, and bias in visualizations.
- **[visual-storytelling-design](skills/visual-storytelling-design/SKILL.md)** — Turn data into narrative via annotation and scrollytelling.
- **[d3-visualization](skills/d3-visualization/SKILL.md)** — Build custom interactive charts, networks, and maps with D3.js.

### Security

- **[security-threat-model](skills/security-threat-model/SKILL.md)** — Apply STRIDE with trust boundaries and defense-in-depth.

### Org & facilitation

- **[facilitation-patterns](skills/facilitation-patterns/SKILL.md)** — Run productive meetings, workshops, and retros.
- **[negotiation-alignment-governance](skills/negotiation-alignment-governance/SKILL.md)** — Align stakeholders via RACI, BATNA, and conflict protocols.
- **[reviews-retros-reflection](skills/reviews-retros-reflection/SKILL.md)** — Run blameless retros with SMART actions (Start/Stop/Continue, Sailboat).
- **[stakeholders-org-design](skills/stakeholders-org-design/SKILL.md)** — Map stakeholders; design teams via Conway and Team Topologies.

</details>

<details>
<summary><b>📊 Data & ML</b> — data modeling, visualization, math intuition, GraphRAG, geometric deep learning (19 skills)</summary>

### Data modeling & visualization

- **[data-schema-knowledge-modeling](skills/data-schema-knowledge-modeling/SKILL.md)** — Model entities and relationships for DBs, graphs, ontologies.
- **[code-data-analysis-scaffolds](skills/code-data-analysis-scaffolds/SKILL.md)** — Generate code scaffolds for analysis across Python / R / SQL.
- **[visualization-choice-reporting](skills/visualization-choice-reporting/SKILL.md)** — Pick the right chart and narrate the insight to action.
- **[mapping-visualization-scaffolds](skills/mapping-visualization-scaffolds/SKILL.md)** — Map relationships with trees, networks, layers, swimlanes.

### Geometric deep learning

- **[symmetry-discovery-questionnaire](skills/symmetry-discovery-questionnaire/SKILL.md)** — Discover hidden data symmetries collaboratively.
- **[symmetry-group-identifier](skills/symmetry-group-identifier/SKILL.md)** — Map symmetries to cyclic, dihedral, SO(3), SE(3), E(3) groups.
- **[symmetry-validation-suite](skills/symmetry-validation-suite/SKILL.md)** — Empirically test invariance and equivariance claims.
- **[equivariant-architecture-designer](skills/equivariant-architecture-designer/SKILL.md)** — Design G-CNN, steerable, and e3nn architectures.
- **[model-equivariance-auditor](skills/model-equivariance-auditor/SKILL.md)** — Verify implemented models respect their intended symmetries.

### Math intuition

3Blue1Brown-style teaching moves for explaining vector / matrix / high-dim concepts geometrically. Powers the `math-intuition-coach` agent.

- **[concept-rediscovery-walk](skills/concept-rediscovery-walk/SKILL.md)** — Socratic walks that let learners invent eigenvectors, gradient, attention themselves.
- **[geometric-algebraic-bridge](skills/geometric-algebraic-bridge/SKILL.md)** — Dual-view exposition: geometric picture + algebraic formula + the one-sentence bridge.
- **[ml-primitive-decoder](skills/ml-primitive-decoder/SKILL.md)** — Decompose attention / layer norm / softmax / conv into LA primitives + ablation table.
- **[high-dim-intuition-rebuild](skills/high-dim-intuition-rebuild/SKILL.md)** — Repair misleading 3D intuition for high-dim spaces (concentration, manifold hypothesis).
- **[worked-example-walkthrough](skills/worked-example-walkthrough/SKILL.md)** — Numbered "frame" computation walkthroughs — text equivalent of a 3b1b animation.

### GraphRAG

- **[knowledge-graph-construction](skills/knowledge-graph-construction/SKILL.md)** — Design LPG / RDF knowledge graphs from unstructured data.
- **[embedding-fusion-strategy](skills/embedding-fusion-strategy/SKILL.md)** — Combine semantic and structural embeddings for retrieval.
- **[retrieval-search-orchestration](skills/retrieval-search-orchestration/SKILL.md)** — Design graph + vector retrieval pipelines with provenance.
- **[graphrag-system-design](skills/graphrag-system-design/SKILL.md)** — Architect end-to-end GraphRAG from pattern to deployment.
- **[graphrag-evaluation](skills/graphrag-evaluation/SKILL.md)** — Evaluate GraphRAG across KG quality, retrieval, hallucination.

</details>

<details>
<summary><b>💼 Domain Packs</b> — corporate finance, household finance, game theory, fantasy baseball, specialized (47 skills)</summary>

### Corporate finance & valuation (11)

Based on Damodaran's valuation curriculum.

- **[business-narrative-builder](skills/business-narrative-builder/SKILL.md)** — Link a company's story to valuation drivers.
- **[financial-statement-analyzer](skills/financial-statement-analyzer/SKILL.md)** — Normalize financials; compute FCFF, FCFE, key ratios.
- **[cost-of-capital-estimator](skills/cost-of-capital-estimator/SKILL.md)** — Compute WACC via CAPM, bottom-up beta, country risk.
- **[intrinsic-valuation-dcf](skills/intrinsic-valuation-dcf/SKILL.md)** — Run DDM / FCFE / FCFF DCF with terminal value and sensitivity.
- **[relative-valuation-multiples](skills/relative-valuation-multiples/SKILL.md)** — Value via PE, PBV, EV/EBITDA vs peers or regression.
- **[capital-structure-optimizer](skills/capital-structure-optimizer/SKILL.md)** — Find the debt ratio that minimizes WACC.
- **[project-investment-analyzer](skills/project-investment-analyzer/SKILL.md)** — Evaluate projects via NPV, IRR, EVA vs hurdle rate.
- **[dividend-buyback-analyzer](skills/dividend-buyback-analyzer/SKILL.md)** — Decide dividends vs buybacks vs retained cash.
- **[special-situations-valuation](skills/special-situations-valuation/SKILL.md)** — Value distressed, private, high-growth, and financial firms.
- **[valuation-reconciler](skills/valuation-reconciler/SKILL.md)** — Reconcile DCF and multiples into a buy / sell / hold call.
- **[financial-unit-economics](skills/financial-unit-economics/SKILL.md)** — Analyze CAC, LTV, contribution margin, cohort payback.

### Household finance (12)

PDF-driven personal-finance pipeline. Pairs with the orchestration runtime at `~/Documents/Projects/financialplanning/` (inbox, archive, canonical JSON store, prompts, weekly static HTML dashboards). Powers the `household-cfo` agent and 8 specialists.

- **[pdf-statement-parser](skills/pdf-statement-parser/SKILL.md)** — Parse a single bank / brokerage / 401k / HSA / mortgage / tax PDF into normalized JSON with confidence.
- **[transaction-categorizer](skills/transaction-categorizer/SKILL.md)** — Rules-then-LLM categorization with merchant normalization and rule learning.
- **[transaction-deduplicator](skills/transaction-deduplicator/SKILL.md)** — Composite-key dedupe across overlapping statement imports; preserves legitimate same-day repeats.
- **[recurring-charge-detector](skills/recurring-charge-detector/SKILL.md)** — Cluster same-merchant charges by cadence; promote at ≥3 occurrences; track dormant.
- **[statement-reconciler](skills/statement-reconciler/SKILL.md)** — Verify opening + Σ = closing; diagnose sign flips, missing rows, double-counts.
- **[cash-flow-forecaster](skills/cash-flow-forecaster/SKILL.md)** — 60-day daily projection per cash account with trough confidence band.
- **[category-trend-analyzer](skills/category-trend-analyzer/SKILL.md)** — Current vs 6-month rolling vs YoY vs budget; outliers ranked by dollar impact.
- **[anomaly-fraud-scanner](skills/anomaly-fraud-scanner/SKILL.md)** — 5-rule fraud / anomaly scan with severity, evidence, recommended action.
- **[portfolio-drift-rebalancer](skills/portfolio-drift-rebalancer/SKILL.md)** — Aggregate allocation across taxable + 401k + HSA; tax-efficient rebalance proposal.
- **[tax-loss-harvest-scanner](skills/tax-loss-harvest-scanner/SKILL.md)** — TLH candidates with wash-sale guard across all household accounts including spousal.
- **[hsa-receipt-vault](skills/hsa-receipt-vault/SKILL.md)** — Track HSA-qualified out-of-pocket expenses for deferred tax-free reimbursement.
- **[household-finance-dashboard-builder](skills/household-finance-dashboard-builder/SKILL.md)** — Single self-contained static HTML dashboard from the JSON store.

### Game theory & strategic competition (8)

Domain-neutral primitives — portable across fantasy sports, poker, auctions, M&A.

- **[auction-first-price-shading](skills/auction-first-price-shading/SKILL.md)** — Optimal shaded bid for sealed first-price auctions.
- **[auction-winners-curse-haircut](skills/auction-winners-curse-haircut/SKILL.md)** — Bayesian haircut for common-value auctions.
- **[adverse-selection-prior](skills/adverse-selection-prior/SKILL.md)** — Prior that an offered trade is +EV given they proposed it.
- **[variance-strategy-selector](skills/variance-strategy-selector/SKILL.md)** — Pick variance-seeking or minimizing posture by win probability.
- **[opponent-archetype-classifier](skills/opponent-archetype-classifier/SKILL.md)** — Bayesian archetype inference from observed behavior.
- **[matchup-win-probability-sim](skills/matchup-win-probability-sim/SKILL.md)** — P(win K of N cats) via Monte-Carlo or Poisson-binomial.
- **[category-allocation-best-response](skills/category-allocation-best-response/SKILL.md)** — Push / concede / contest allocation for H2H Categories.
- **[market-mechanics-betting](skills/market-mechanics-betting/SKILL.md)** — Turn beliefs into bets: Kelly sizing, Brier optimization.

### Yahoo Fantasy Baseball (14)

Baseball-specific skills for a H2H Categories league. Pairs with the companion runtime at `~/Documents/Projects/yahoo-mlb/`.

- **[mlb-league-state-reader](skills/mlb-league-state-reader/SKILL.md)** — Parse Yahoo league state via Claude-in-Chrome.
- **[mlb-player-analyzer](skills/mlb-player-analyzer/SKILL.md)** — Deep-dive a player across FanGraphs, Savant, RotoWire.
- **[mlb-matchup-analyzer](skills/mlb-matchup-analyzer/SKILL.md)** — Grade a single game for fantasy impact (park, weather, SP).
- **[mlb-category-state-analyzer](skills/mlb-category-state-analyzer/SKILL.md)** — Compute weekly cat state across all 10 categories.
- **[mlb-regression-flagger](skills/mlb-regression-flagger/SKILL.md)** — Flag buy-low / sell-high via xwOBA / FIP vs surface stats.
- **[mlb-two-start-scout](skills/mlb-two-start-scout/SKILL.md)** — Find two-start SPs and grade for QS scoring.
- **[mlb-closer-tracker](skills/mlb-closer-tracker/SKILL.md)** — Track closer roles and handcuffs across all 30 teams.
- **[mlb-faab-sizer](skills/mlb-faab-sizer/SKILL.md)** — Size FAAB bids; delegates to auction skills for shading.
- **[mlb-trade-evaluator](skills/mlb-trade-evaluator/SKILL.md)** — Score a trade across all 10 cats with adverse-selection prior.
- **[mlb-playoff-scheduler](skills/mlb-playoff-scheduler/SKILL.md)** — Count games and grade matchups for weeks 21–23.
- **[mlb-opponent-profiler](skills/mlb-opponent-profiler/SKILL.md)** — Weekly archetype refresh for the 11 league opponents.
- **[mlb-signal-emitter](skills/mlb-signal-emitter/SKILL.md)** — Validate and persist signals with schema enforcement.
- **[mlb-decision-logger](skills/mlb-decision-logger/SKILL.md)** — Append structured decision entries; run Monday calibration.
- **[mlb-beginner-translator](skills/mlb-beginner-translator/SKILL.md)** — Wrap jargon in plain English with inline translations.

### Specialized & meta (2)

- **[chef-assistant](skills/chef-assistant/SKILL.md)** — Cook via technique, food science, flavor architecture.
- **[skill-creator](skills/skill-creator/SKILL.md)** — Turn a PDF / paper / methodology into a reusable skill.

</details>

<details>
<summary><b>📰 Substack Growth</b> — 9-agent team for growing "From First Principles / The Thinker's Notebook" (68 skills)</summary>

Pairs with the working folder at `~/Documents/Thinking/substacker/` (inbox, corpus, shared-context, ops). Voice-profile, section-map, per-section visual identities, analogy catalog, topic ledger all live there.

### Librarian (8) — corpus ingest + index

- **[ingest-inbox-item](skills/ingest-inbox-item/SKILL.md)** — Orchestrate per-file ingest: normalize → tag → score → dedupe → write seed.
- **[normalize-format](skills/normalize-format/SKILL.md)** — Convert markdown / Claude exports / transcripts / Readwise into canonical seed bodies.
- **[tag-by-topic](skills/tag-by-topic/SKILL.md)** — Assign 1-4 topic tags from controlled vocabulary; log pending tags.
- **[score-intuition-density](skills/score-intuition-density/SKILL.md)** — Compute 0-10 density from 8 explicit signals (analogy, concrete example, counterfactual, etc.).
- **[dedupe-against-corpus](skills/dedupe-against-corpus/SKILL.md)** — Exact fingerprint + near-match Jaccard; link rather than merge.
- **[search-corpus](skills/search-corpus/SKILL.md)** — "What have I already thought about X?" — ranked matches with excerpts.
- **[update-topic-ledger](skills/update-topic-ledger/SKILL.md)** — Maintain counts, last_touched, hot/warm/cold, top_seeds per topic.
- **[sweep-stale-seeds](skills/sweep-stale-seeds/SKILL.md)** — Flag seeds >30d old with no links; recommend keep/promote/kill.

### Intuition Builder (7) — 5 framings per topic

- **[generate-analogy-set](skills/generate-analogy-set/SKILL.md)** — 5 framings: everyday / physical / contrarian / historical / counterfactual.
- **[check-analogy-novelty](skills/check-analogy-novelty/SKILL.md)** — Cross-check against analogy-catalog; flag reuse.
- **[stress-test-analogy](skills/stress-test-analogy/SKILL.md)** — Find the boundary where each analogy breaks; propose a fold.
- **[map-analogy-to-concept](skills/map-analogy-to-concept/SKILL.md)** — Component-by-component source → target mapping (Gentner structure-mapping).
- **[propose-counterfactual](skills/propose-counterfactual/SKILL.md)** — "What if this weren't here?" — reveal function via subtraction.
- **[update-analogy-catalog](skills/update-analogy-catalog/SKILL.md)** — Append entry on publish; track freshness.
- **[voice-fitness-check](skills/voice-fitness-check/SKILL.md)** — Rank framings by voice-profile analogy-direction priority (biology > organizational > sports).

### Editor (10) — voice + structural review gate

- **[structural-review](skills/structural-review/SKILL.md)** — Macro-structure: argument flow, pivot, signposting, outline.
- **[voice-check](skills/voice-check/SKILL.md)** — Phrase-by-phrase against voice-profile don't-list.
- **[hedge-detector](skills/hedge-detector/SKILL.md)** — Precision hedge (keep) vs epistemic-weakness (commit or specific).
- **[slop-detector](skills/slop-detector/SKILL.md)** — 10 signatures of AI-generated explainer slop.
- **[opener-critique](skills/opener-critique/SKILL.md)** — Confession / reframe / admission pass; news-hook / generic-opener fail.
- **[closer-critique](skills/closer-critique/SKILL.md)** — Bolded maxim / scoreboard check for series posts.
- **[analogy-weight-check](skills/analogy-weight-check/SKILL.md)** — Mechanical-weight test; flag decorative and wrong-domain analogies.
- **[paragraph-rhythm-check](skills/paragraph-rhythm-check/SKILL.md)** — Long/short mix, pivot paragraph, no walls.
- **[citation-form-check](skills/citation-form-check/SKILL.md)** — Papers cited with Author, Institution, Year inline.
- **[section-break-check](skills/section-break-check/SKILL.md)** — Asterisks for essays vs H2 for methodology; no mixing.

### Distribution Translator (7) — platform-native rewrites

- **[extract-thread-spine](skills/extract-thread-spine/SKILL.md)** — 5-7 point argument backbone with translatability scoring.
- **[hook-generator](skills/hook-generator/SKILL.md)** — Platform-specific first-line hook candidates.
- **[substack-note-rewrite](skills/substack-note-rewrite/SKILL.md)** — 60-180 word Note; bolded maxim closer; single link.
- **[x-thread-rewrite](skills/x-thread-rewrite/SKILL.md)** — Short / medium / long variants; ≤12 tweets; no numbering by default.
- **[linkedin-post-rewrite](skills/linkedin-post-rewrite/SKILL.md)** — 900-2500 chars; 210-char fold hook; 0-2 niche hashtags.
- **[cross-poster-blurb](skills/cross-poster-blurb/SKILL.md)** — 60-140 word third-person blurb for Substack cross-post feature.
- **[platform-voice-check](skills/platform-voice-check/SKILL.md)** — Voice audit gate with loop-back on FAIL.

### Growth Analyst (8) — weekly Substack stats

- **[fetch-substack-stats](skills/fetch-substack-stats/SKILL.md)** — **Primary path.** Pull stats from the Substack dashboard via Claude-in-Chrome browser automation.
- **[ingest-substack-csv](skills/ingest-substack-csv/SKILL.md)** — **Fallback path.** Load + validate manual CSV; halt on schema drift.
- **[compute-baseline](skills/compute-baseline/SKILL.md)** — Rolling 4-week median + trimmed median + IQR z-scores.
- **[attribute-performance](skills/attribute-performance/SKILL.md)** — Plain-English outlier attribution with calibrated confidence.
- **[per-section-tracking](skills/per-section-tracking/SKILL.md)** — Per-section aggregates + prune candidates for Curator.
- **[fetch-public-page-stats](skills/fetch-public-page-stats/SKILL.md)** — WebFetch supplement for stale CSV data.
- **[write-weekly-report](skills/write-weekly-report/SKILL.md)** — Compose 400-800 word report; hard word cap.
- **[update-audience-notes](skills/update-audience-notes/SKILL.md)** — Append confidence ≥ medium observations.

### Trend Scout (6) — weekly ML/systems signal digest

- **[fetch-watchlist-sources](skills/fetch-watchlist-sources/SKILL.md)** — Pull 7-day updates from 30-50 intuition-first sources.
- **[summarize-signal](skills/summarize-signal/SKILL.md)** — "Teaches X" summary; mechanism / empirical / tool / opinion / announcement / benchmark.
- **[cross-ref-topic-ledger](skills/cross-ref-topic-ledger/SKILL.md)** — NEW / OVERLAPS seed|draft|published; reinforcement angle.
- **[rank-by-user-fit](skills/rank-by-user-fit/SKILL.md)** — Weighted-sum scoring; top 10 keeps + explicit drops.
- **[write-weekly-digest](skills/write-weekly-digest/SKILL.md)** — Compose Friday digest; Saturday-morning readable.
- **[update-watchlist](skills/update-watchlist/SKILL.md)** — Monthly: propose adds/removes via diff; writer approves.

### Technical Reviewer (6) — pre-publish claim check

- **[claim-extractor](skills/claim-extractor/SKILL.md)** — Extract atomic technical claims from prose.
- **[classify-claim](skills/classify-claim/SKILL.md)** — simplified-correct / simplified-boundary / wrong / contested / overclaim.
- **[cross-reference-claim](skills/cross-reference-claim/SKILL.md)** — Find primary source (arXiv, RFC, textbook); never blog posts.
- **[flag-boundary-break](skills/flag-boundary-break/SKILL.md)** — Fold suggestion for simplified-boundary as teaching moment.
- **[write-review-artifact](skills/write-review-artifact/SKILL.md)** — Compose go / go-with-hedges / no-go review.
- **[glossary-alignment-check](skills/glossary-alignment-check/SKILL.md)** — Writer's definitions vs field-standard.

### Curator (9) — section-map maintainer, active + reactive

- **[check-corpus-readiness](skills/check-corpus-readiness/SKILL.md)** — 28-day + 4-post cadence gate.
- **[cluster-corpus-by-theme](skills/cluster-corpus-by-theme/SKILL.md)** — Axial coding; Braun & Clarke thematic analysis over published corpus.
- **[propose-section](skills/propose-section/SKILL.md)** — Cluster → named section proposal with fit-confidence.
- **[write-section-promise](skills/write-section-promise/SKILL.md)** — One-sentence promise; specific, testable, non-overlapping, voiced.
- **[audit-drift](skills/audit-drift/SKILL.md)** — Flag posts no longer fitting their section's promise.
- **[recommend-prune](skills/recommend-prune/SKILL.md)** — Retire / merge / reassign with reasons-to-reject.
- **[update-section-map](skills/update-section-map/SKILL.md)** — Atomic write of section-map.md with snapshot backup.
- **[classify-post-to-section](skills/classify-post-to-section/SKILL.md)** — Assign a draft or published post to the best-fitting section.
- **[derive-section-voice-overlay](skills/derive-section-voice-overlay/SKILL.md)** — Draft per-section voice delta once section has ≥3 posts.

### Growth Strategist (7) — quarterly zoomout

- **[quarterly-zoomout](skills/quarterly-zoomout/SKILL.md)** — 400-700 word narrative synthesizing 13 weeks of data.
- **[answer-uncomfortable-question](skills/answer-uncomfortable-question/SKILL.md)** — Evidence + reasoning + downside triad per question.
- **[section-portfolio-assessment](skills/section-portfolio-assessment/SKILL.md)** — Healthy / drifting / candidate-for-prune per section.
- **[product-hiding-scan](skills/product-hiding-scan/SKILL.md)** — Course / book / cohort / consulting candidates from the corpus.
- **[paid-tier-readiness-check](skills/paid-tier-readiness-check/SKILL.md)** — Four gates: scale / engagement / section candidate / writer capacity.
- **[goal-reset-proposal](skills/goal-reset-proposal/SKILL.md)** — Propose diff to goals.md; writer applies manually.
- **[identify-kill-list](skills/identify-kill-list/SKILL.md)** — Max 4 items; easiest kills first.

</details>

---

## Installation

### Option 1 — Plugin (recommended)

```
/plugin marketplace add lyndonkl/claude
/plugin install thinking-frameworks-skills
```

All 188 skills become available immediately. Claude invokes them automatically based on your request and each skill's trigger description.

<details>
<summary><b>Option 2 — Manual install</b></summary>

Clone and copy into your Claude Code skills directory:

```bash
git clone https://github.com/lyndonkl/claude.git
cd claude

# macOS / Linux
cp -r skills/* ~/.claude/skills/

# Windows
xcopy skills\* %USERPROFILE%\.claude\skills\ /E /I
```

</details>

---

## Using Skills

Skills activate automatically when you use matching trigger phrases — no manual invocation needed.

```
"Help me decide between three options..."      → decision-matrix
"I need to run user interviews..."              → discovery-interviews-surveys
"Value this company for acquisition..."         → acquisition-analyst (agent)
"What should I stream at pitcher this week?"    → mlb-streaming-strategist (agent)
"My chicken keeps coming out dry..."            → chef-assistant
```

<details>
<summary><b>Skill anatomy</b> — how each skill is structured</summary>

```
skill-name/
├── SKILL.md                          # Entry point (< 300 lines)
│   ├── YAML metadata with triggers
│   ├── When to use + guardrails
│   ├── Workflow checklist
│   └── Common patterns
└── resources/
    ├── template.md                   # Ready-to-use templates (< 400 lines)
    ├── methodology.md                # Advanced techniques (< 500 lines)
    └── evaluators/
        └── rubric_[skill].json       # 10-criterion quality rubric
```

**Progressive depth:** SKILL.md for the skim, template.md for the copy-paste, methodology.md for the edge cases, rubric for self-evaluation. Every skill ships with all four.

</details>

---

## Contributing

Fork, branch, and PR. Follow the skill structure above — `SKILL.md` under 300 lines, self-assess against the rubric (target ≥ 3.5), and include trigger phrases in the YAML description so Claude can auto-invoke.

## Resources

- [Claude Code docs](https://docs.claude.com/en/docs/claude-code/)

## License

Open source; use freely with Claude Code. Individual skills carry their own attributions.

## Acknowledgments

Skills draw on established frameworks and practitioners:

- **Thinking:** Bayesian reasoning, causal inference, dialectics, first principles
- **Research:** Jobs-to-be-done (Christensen), design of experiments (Box, Taguchi), user research (Torres, Ulwick)
- **Decision-making:** Multi-criteria analysis, expected value, risk analysis
- **Corporate finance:** Damodaran's valuation curriculum
- **Writing:** Story structure (McKee, McPhee), clarity (Zinsser, Pinker, King), SUCCESs (Heath)
- **Culinary:** Technique (Pépin, Child, López-Alt), food science (McGee, Sharma), cultural cooking (Bourdain, Chang, Ottolenghi)

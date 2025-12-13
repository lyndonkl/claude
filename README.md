# Claude Code Skills Collection

[![Run in Smithery](https://smithery.ai/badge/skills/lyndonkl)](https://smithery.ai/skills?ns=lyndonkl&utm_source=github&utm_medium=badge)


> **Claude Code Plugin Available** — Install all 69 skills instantly with `/plugin marketplace add lyndonkl/claude` then `/plugin install thinking-frameworks-skills`

A comprehensive collection of production-ready skills for Claude Code, covering thinking frameworks, decision-making tools, research methods, design patterns, and specialized domains.

## Overview

This repository contains **69 skills** designed to enhance Claude Code's capabilities across strategic thinking, product development, research, experimentation, and creative problem-solving. Each skill includes:

- **Structured workflows** with step-by-step guidance
- **Practical templates** for immediate use
- **Advanced methodologies** for complex scenarios
- **Evaluation rubrics** with quality criteria and common failure modes
- **Progressive disclosure** (SKILL.md → template.md → methodology.md)

## Table of Contents

- [Skills by Category](#skills-by-category)
  - [🧠 Strategic Thinking & Decision Making](#-strategic-thinking--decision-making)
  - [💡 Problem Solving & Analysis](#-problem-solving--analysis)
  - [🔬 Research & Discovery](#-research--discovery)
  - [🗣️ Dialogue & Deliberation](#️-dialogue--deliberation)
  - [💭 Ideation & Creativity](#-ideation--creativity)
  - [📊 Data & Modeling](#-data--modeling)
  - [🏗️ Architecture & Design](#️-architecture--design)
  - [🔒 Security & Risk](#-security--risk)
  - [📝 Communication & Documentation](#-communication--documentation)
  - [🔬 Scientific Writing](#-scientific-writing)
  - [🎯 Estimation & Forecasting](#-estimation--forecasting)
  - [💼 Business & Product Management](#-business--product-management)
  - [⏱️ Productivity & Learning](#️-productivity--learning)
  - [🏢 Organizational Design](#-organizational-design)
  - [🛡️ Ethics & Evaluation](#️-ethics--evaluation)
  - [🍳 Specialized Domains](#-specialized-domains)
  - [🛠️ Skill Development & Meta-Tools](#️-skill-development--meta-tools)
- [Installation](#installation)
- [Using Skills](#using-skills)
- [Skill Development Status](#skill-development-status)
- [Key Features](#key-features)
- [Contributing](#contributing)
- [Resources](#resources)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Skills by Category

### 🧠 Strategic Thinking & Decision Making

**decision-matrix** - Multi-criteria decision analysis with weighted scoring, sensitivity analysis, and uncertainty handling for complex choices between 3-10 options.

**bayesian-reasoning-calibration** - Probabilistic reasoning with prior/posterior updates, Bayes theorem application, and calibration techniques for reducing overconfidence.

**alignment-values-north-star** - Strategic alignment framework connecting daily decisions to core values and long-term vision using north star metrics and principle mapping.

**environmental-scanning-foresight** - Anticipate change through PESTLE analysis, weak signal detection, scenario planning (2x2 matrix), cross-impact analysis, and signposts for early warning systems.

**expected-value** - Rational decision-making under uncertainty through probability-weighted outcomes (EV = Σ p×v). Covers scenario identification, probability estimation (base rates, triangulation, calibration), payoff quantification (NPV, non-monetary factors), decision trees (fold-back induction, optionality), expected utility for risk aversion, sensitivity analysis, and bias mitigation (overconfidence, sunk costs, tail risk neglect).

**heuristics-and-checklists** - Practical decision-making through mental shortcuts (heuristics) and systematic error prevention (checklists). Design fast & frugal heuristics (recognition, take-the-best, satisficing), create effective checklists (5-9 killer items, READ-DO vs DO-CONFIRM formats), validate rules empirically (≥80% accuracy target), and mitigate cognitive biases (availability, representativeness, anchoring). Covers aviation, surgical, and software deployment checklists with proven 60-80% error reduction.

**hypotheticals-counterfactuals** - Explore alternative scenarios and test assumptions through "what if" thinking. Use counterfactual reasoning (backward-looking: "what would have happened if?") to understand causality and learn from decisions. Apply scenario planning (forward-looking: optimistic/baseline/pessimistic futures, 2×2 matrices) to prepare for uncertainty. Conduct rigorous pre-mortems (6-step process: imagine failure, identify causes, vote on risks, assign mitigations). Extract common actions, hedges, and options from scenarios. Define leading indicators with clear thresholds for monitoring which future unfolds. Covers minimal rewrite principle, causal mechanism specification, probability calibration, and stress testing decisions.

**kill-criteria-exit-ramps** - Define objective stopping rules for projects to avoid sunk cost fallacy and optimize resource allocation. Set upfront kill criteria (quantifiable metrics, time horizons, decision authority) before emotional/financial investment. Design go/no-go gates for milestone-based evaluation with increasing investment stages. Apply pivot vs. kill framework (customer pain validation, learning rate, burn rate sustainability, opportunity cost analysis). Manage project portfolios with quarterly ranking (EV/Cost ratio), systematic rebalancing, and bottom 20-30% kill threshold. Execute disciplined wind-downs (1 month max) with team reallocation, customer transition, and blameless postmortems. Use pre-mortem inversion ("would we start this today?") to overcome sunk cost bias. Normalize killing projects as capital allocation discipline. Covers behavioral economics of stopping, real options analysis, Bayesian updating for kill probability, and organizational culture change.

**portfolio-roadmapping-bets** - Strategic portfolio roadmapping across time horizons (H1/H2/H3: Now/Next/Later) with disciplined betting framework. Size bets by effort (S/M/L/XL) and impact (1x/3x/10x), sequence across horizons with dependency mapping, set exit/scale criteria for kill or double-down decisions, and balance portfolio using 70-20-10 rule (core/adjacent/transformational). Apply McKinsey Three Horizons, RICE/ICE scoring, critical path analysis, and staged funding models. Validate capacity feasibility (effort ≤ 80% capacity), ensure impact ladders to strategic theme with risk adjustment, and establish review cadence (monthly H1, quarterly H2, semi-annual H3) with kill/pivot/persevere/scale framework. Covers horizon planning, bet sizing methodologies, portfolio balancing techniques, dependency sequencing, and portfolio health metrics tracking.

**postmortem** - Blameless postmortem analysis transforming failures into learning. Document timeline with specific timestamps (detection → investigation → resolution), quantify impact across dimensions (users, revenue, SLA, reputation), conduct root cause analysis using 5 Whys or fishbone diagrams to reach systemic issues (not individual blame), define SMART corrective actions (specific, measurable, assigned, realistic, time-bound) using hierarchy of controls (eliminate, substitute, engineering controls, administrative, training). Maintain blameless tone focusing on systems/processes, conduct within 48 hours while memory fresh, track action items to >90% completion, share broadly for organizational learning. Apply to production outages, security incidents, product failures, project misses, or near-misses. Covers blameless culture principles, root cause techniques, corrective action frameworks, incident response patterns, facilitation techniques, and learning metrics.

**prioritization-effort-impact** - Transform overwhelming backlogs into actionable priorities using 2x2 effort-impact matrix (Quick Wins, Big Bets, Fill-Ins, Time Sinks). Score items on effort (1-5: time, complexity, risk, dependencies) and impact (1-5: users, business value, strategic alignment, user pain) with diverse stakeholder input (engineering estimates effort, product/sales estimate impact). Plot on matrix to identify Quick Wins (high impact, low effort - do first) vs Time Sinks (low impact, high effort - avoid). Sequence roadmap: Quick Wins first (build momentum), Big Bets second (strategic impact), Fill-Ins opportunistically, reject Time Sinks with clear rationale. Apply calibration techniques (reference examples, silent voting, forced ranking), validate with data (usage analytics, user surveys, NPS drivers), and plan capacity with 20-30% buffer. Alternative frameworks include RICE (Reach × Impact × Confidence / Effort), MoSCoW (Must/Should/Could/Won't), ICE scoring, Kano model, and cost of delay. Covers advanced scoring methodologies, stakeholder alignment techniques, roadmap optimization, dependency mapping, and common pitfalls (optimism bias, HIPPO pressure, scope creep).

**project-risk-register** - Proactively identify, assess, prioritize, and monitor project risks using structured risk register. Score risks on probability×impact (1-5 each, 5×5 matrix = 1-25 risk score) with thresholds: Critical (≥20), High (12-19), Medium (6-11), Low (1-5). For each risk: identify root cause (not symptoms), assign named owner (not "team"), define mitigation (reduce probability before) AND contingency (reduce impact if occurs), set quantifiable triggers for contingency activation. Brainstorm risks across 6 categories (technical, schedule, resource, external, scope, organizational) using structured checklists. Monitor regularly (weekly for active projects, monthly for longer) tracking new/closed risks, score changes with rationale, risk burn-down (total exposure decreasing), and leading indicators. Integrate mitigation actions into project schedule, budget contingency reserves based on Expected Monetary Value (EMV), and use Monte Carlo simulation for probabilistic forecasting (P50/P80/P95 confidence levels). Covers quantitative risk analysis (PERT estimation, sensitivity analysis, tornado diagrams), risk aggregation and correlation, advanced probability estimation (base rates, calibration training, decomposition), decision trees for sequential risks, and organizational risk maturity building.

**prototyping-pretotyping** - Test ideas cheaply before building using pretotyping (fake it: landing pages, concierge MVPs, Wizard of Oz) and prototyping (paper, clickable, coded). Choose appropriate fidelity for question: pretotype (hours, $0-100) tests demand/pricing, paper prototype (days, $0-50) tests workflow, clickable prototype (week, $500) tests UI/UX, coded prototype (month, $10K) tests feasibility, MVP (months, $100K+) tests retention. Apply fake door tests (measure clicks on "Coming Soon"), concierge MVPs (manual service before automation), Wizard of Oz (human-powered appearing automated), single-feature MVPs (one thing done well). Measure behavior over opinions: pre-commitment signals (payments strongest, then pre-orders, waitlist emails, clicks), task completion rates, error rates, retention. Set success criteria before testing (e.g., "10% conversion validates demand"), recruit real target users (n=5-10 qualitative, n=100+ quantitative), iterate quickly through fidelity ladder (start low, climb only when validated). Common pretotypes: Dropbox video (75K sign-ups before building), fake door tests, manual-first approaches. Covers experiment design principles, bias mitigation (confirmation, sampling, social desirability), statistical confidence, qualitative analysis (think-aloud protocol, thematic coding), and common failure patterns (overbuilding, no success criteria, testing wrong users, opinions over behavior).

**strategy-and-competitive-analysis** - Develop robust business strategies grounded in rigorous competitive and market analysis using proven frameworks. Apply Good Strategy kernel (Rumelt): diagnosis (identify core challenge with evidence, not symptoms), guiding policy (overall approach addressing diagnosis, creates competitive advantage), coherent actions (3-5 specific mutually reinforcing steps with owners/timelines/resources). Conduct comprehensive competitive analysis through Porter's 5 Forces (assess industry attractiveness by analyzing competitive rivalry, threat of new entrants/substitutes, buyer/supplier power with High/Medium/Low scoring), competitor profiling (SWOT per competitor, positioning maps, strategy inference, win/loss patterns), and competitive moats identification (network effects, switching costs, brand, cost advantages, regulatory barriers). Apply strategic frameworks based on question type: Blue Ocean Strategy (create uncontested market space via eliminate/reduce/raise/create framework, strategy canvas visualization), Playing to Win (where to play: markets/segments/geographies, how to win: cost leadership/differentiation/focus strategies), Value Chain Analysis (identify cost or differentiation opportunities across primary and support activities), BCG Matrix (portfolio management: Stars/Cash Cows/Question Marks/Dogs), and SWOT Analysis (internal strengths/weaknesses, external opportunities/threats). Validate strategy is evidence-based (customer data, market research, competitive intelligence, financials), assumptions explicit with validation plans, defensible against competitors (explains why strategy hard to copy, what moat it builds), realistic given constraints (resources, capabilities, time), and actionable (clear owners, timelines, success metrics baseline+targets, go/no-go decision points, review cadence). Cover market entry strategy (assess industry with 5 Forces, choose positioning, define go-to-market), competitive response planning (analyze threat, decide defend/ignore/leapfrog), annual strategic planning (current state analysis, strategic themes, OKRs/initiatives), product differentiation strategy (positioning map, differentiation axis, roadmap alignment), and strategic scenario planning (build 2x2 scenarios from critical uncertainties, identify robust actions, set trigger points). Includes competitive intelligence gathering (public sources, primary research, strategy inference from hiring/acquisitions/pricing), stress-testing strategy (game out competitive responses, identify fragile assumptions), and avoiding common pitfalls (goals≠strategy, fluff/platitudes, laundry list of unrelated actions, ignoring constraints/competition, imitating without understanding context, analysis paralysis, confusing planning with strategy). Use for startup market entry, product launches, geographic expansion, M&A strategy, turnaround/crisis, pricing strategy, business model decisions, market positioning, and annual strategic planning.

### 💡 Problem Solving & Analysis

**decomposition-reconstruction** - Break complex problems into components, analyze independently, then reconstruct with understanding of interactions and emergent properties.

**causal-inference-root-cause** - Identify true causes vs. correlations using causal diagrams, counterfactuals, and root cause analysis (5 Whys, Ishikawa diagrams).

**abstraction-concrete-examples** - Move fluidly between abstract concepts and concrete examples to clarify thinking, test understanding, and communicate effectively.

**layered-reasoning** - Structure thinking across multiple abstraction levels (30K ft strategic → 3K ft tactical → 300 ft operational). Maintain consistency: lower layers implement upper layers, upper layers constrain lower layers. Design 3-5 layer hierarchies for system architecture, strategic planning, or cross-audience communication (CEO/manager/engineer). Validate upward consistency (ops implement tactics, tactics achieve strategy), downward consistency (strategy executable with tactics), and lateral consistency (no same-layer contradictions). Propagate changes bidirectionally (strategic shifts cascade down, operational constraints escalate up). Detect emergent properties from bottom-up patterns (Conway's Law, unintended consequences). Translate appropriately for each audience's abstraction level. Covers layer design principles, formal consistency checking, emergence recognition, abstraction gap sizing (3-10 elements per layer), and explicit layer contracts.

**negative-contrastive-framing** - Define concepts and quality criteria by showing what they're NOT—use anti-goals, near-miss examples, and failure patterns to clarify fuzzy boundaries where positive definitions alone are ambiguous. Generate 3-5 anti-goals (true opposites), 5-10 instructive near-misses (examples that almost pass but fail on single dimension), and common failure patterns with detection heuristics and prevention guards. Create contrast matrices varying dimensions systematically to explore boundary space (clear pass, borderline pass, borderline fail, clear fail). Operationalize fuzzy criteria into testable decision rules through contrast insights. Apply boundary mapping to find exact pass/fail thresholds for continuous dimensions. Build failure taxonomies (by severity, type, detection difficulty) with root cause analysis and prevention strategies. Use for teaching by counterexample (revealing misconceptions through near-misses), setting design guardrails (code quality anti-patterns, UX violations), defining evaluation criteria (what disqualifies candidates), preventing common mistakes (QA checklists), and requirements clarification (disambiguating similar concepts). Covers engineering (maintainable code, test quality), design (intuitive interfaces, accessibility), communication (clear writing, audience fit), and strategy (market positioning, brand identity). Near-misses are most valuable when genuinely close calls that isolate single failing dimension.

**synthesis-and-analogy** - Synthesize information from multiple sources into coherent insights and use analogical reasoning to transfer knowledge across domains. Apply thematic synthesis (identify 3-5 recurring themes across sources with frequency counts, code similar ideas, prioritize by frequency×importance), conflict resolution synthesis (reconcile disagreements via meta-framework recognizing both perspectives valid in different contexts, scope distinctions, temporal changes, or state uncertainty when genuinely conflicting), and pattern identification (find repeated structures, causal patterns, outliers, extract meta-insights). Use structural mapping theory for deep analogies: map entities and relationships between source domain (familiar) and target domain (unfamiliar), preserve relational structure not surface attributes (A→B in source corresponds to X→Y in target with same causal pattern), test systematicity (3+ interconnected relations map), productivity (generates new predictions about target), and explicitly state scope limitations (where analogy breaks down). Advanced techniques include meta-synthesis (synthesis of syntheses for literature reviews), mixed-methods integration (combine qualitative themes with quantitative data using convergent/explanatory/exploratory approaches), temporal synthesis (trend analysis, cycle detection, phase transitions across longitudinal data), cross-cultural synthesis (universal patterns etic analysis + culture-specific manifestations emic analysis), and forced connections (systematic variation pairing target problem with random domains for creative ideation). Apply Gentner's structure-mapping for higher-order relations, pragmatic centrality (focus mapping on goal-relevant aspects), and retrieve-map-transfer process for analogical problem-solving. Avoid cherry-picking sources, single-source patterns (require 3+ for pattern claims), false synthesis (forcing consensus where conflict exists), surface analogies (attribute-based like 'both are blue'), analogy overextension (push beyond valid scope), mixing facts with interpretations, and using analogies as proof rather than illustration. Use for literature reviews, multi-stakeholder feedback integration, explaining complex concepts, cross-domain problem-solving (transfer solutions from different fields like ant colony optimization for warehouse routing), creative ideation, and making synthesized insights accessible through familiar domain analogies. Covers information synthesis, analogical reasoning, structural correspondence, cross-domain transfer, pattern recognition, and knowledge integration.

**systems-thinking-leverage** - Find high-leverage intervention points in complex systems by mapping feedback loops (reinforcing R and balancing B), identifying stocks (accumulations like technical debt, trust, employee count) and flows (rates like hiring rate, bug introduction rate), recognizing system archetypes (Fixes That Fail, Shifting the Burden, Tragedy of Commons, Limits to Growth, Escalation, Success to Successful, Eroding Goals, Growth and Underinvestment, Accidental Adversaries, Rule Beating), and applying Meadows' leverage hierarchy (12 levels from weak parameters/numbers to strong goals/paradigms/transcending paradigms). Map causal loops with polarity (+ same direction, - opposite direction), distinguish reinforcing loops (amplify change, growth or collapse) from balancing loops (resist change, goal-seeking), explicitly note time delays (perception, information, decision, physical) with quantified duration (not just 'delayed' but '3-6 months'), anticipate stock-induced oscillations and tipping points. Classify interventions by leverage level: weak (12: parameters like budget +10%, 11: buffers, 10: stock-flow structures, 9: delays), medium (8: balancing loop strength, 7: reinforcing loop strength), strong (6: information flows who sees what, 5: rules/incentives, 4: self-organization capability), very strong (3: goals/purpose, 2: paradigms/mental models, 1: transcending paradigms). Prioritize high-leverage interventions (levels 1-7) over low-leverage parameter-tweaking (levels 8-12), link each intervention to specific loops (which loop it strengthens/weakens and how), trace second-order effects through multiple loops (intervention affects Loop A which affects Loop B), anticipate unintended consequences and system resistance (compensating loops, who pushes back), set realistic timelines accounting for delays (short-term 1-3 months, medium-term 3-12 months, long-term 1+ years), distinguish leading indicators (early signals) from lagging indicators (final outcomes). Apply advanced techniques: nested loop analysis (primary loop modulated by secondary loops), loop dominance shifts (which loop drives behavior now vs. next phase), multi-loop interactions (conflicts vs. synergies), archetype combinations (Fixes That Fail + Shifting Burden creating dependency), behavior-over-time graphs (exponential growth, S-curve, overshoot and collapse, oscillation patterns), scenario planning with systems thinking (map which loops activate in each scenario), counterintuitive interventions (slow down to speed up, weaken feedback to enable change, strengthen delays strategically, reduce efficiency to increase resilience). Avoid linear cause-effect thinking (ignoring feedback), parameter-only interventions (tweaking numbers when structure needs changing), missing delays (premature abandonment before effects manifest), confusing stocks and flows (morale is stock not flow, recognition is flow), vague system boundaries (unclear scope), treating symptoms not root causes (fixing observable problem without addressing feedback loop creating it), ignoring unintended consequences (not tracing through other loops), isolated loop analysis (not showing interconnections). Use for organizational issues (employee turnover, scaling plateaus, productivity decline, innovation stalling), product/technical systems (technical debt accumulation, performance degradation, feature adoption, quality issues), social systems (polarization, misinformation spread, community trust erosion), environmental systems (climate feedback loops, resource depletion, pollution accumulation), personal systems (habit formation, burnout cycles, skill development), and anywhere simple interventions repeatedly fail while systemic patterns persist. Covers feedback loop dynamics, stock-flow structures, system archetypes, leverage point hierarchy, causal loop diagrams, time delays, tipping points, and intervention design.

### 🔬 Research & Discovery

**discovery-interviews-surveys** - Design and conduct user research using jobs-to-be-done interviews, surveys, thematic coding, and statistical analysis while avoiding bias.

**design-of-experiments** - Plan rigorous experiments using factorial designs, response surface methodology, Taguchi methods, and statistical power analysis.

**domain-research-health-science** - Formulate clinical research questions (PICOT framework), evaluate evidence quality using GRADE certainty ratings, systematic bias assessment (Cochrane RoB 2, ROBINS-I, QUADAS-2), and conduct systematic reviews with meta-analysis.

**research-claim-map** - Systematically verify claims through evidence triangulation, source credibility assessment (expertise, independence, track record, methodology), and confidence calibration. Rate evidence quality using hierarchy (primary > secondary > tertiary), actively seek contradicting evidence to avoid confirmation bias, document limitations and gaps explicitly, and calibrate numeric confidence levels (0-100%) based on evidence strength. Apply CRAAP test for source verification, GRADE system for evidence synthesis, and Bayesian updating for confidence adjustment. Covers fact-checking workflows, due diligence investigations, academic literature validation, vendor claim verification, and misinformation detection. Use for claims requiring verification before decisions, conflicting evidence evaluation, competitive intelligence, investigative journalism, or any situation demanding rigorous source triangulation and bias mitigation.

### 🗣️ Dialogue & Deliberation

**deliberation-debate-red-teaming** - Structured debate formats (Oxford, fishbowl, devil's advocate) with red teaming for stress-testing ideas and uncovering blindspots.

**dialectical-mapping-steelmanning** - Present opposing positions in strongest form (steelmanning), map principles using Toulmin model, synthesize via third-way solutions.

**chain-roleplay-debate-synthesis** - Multi-perspective roleplay with expert personas, structured debate, and synthesis across viewpoints for complex decisions.

**role-switch** - Systematically analyze decisions from multiple stakeholder perspectives (eng, PM, legal, user, finance) to uncover blind spots and build alignment. Select 3-6 roles with different goals/incentives/constraints, charitably inhabit each perspective (steel-manning with specific metrics and genuine fears), distinguish position from interest (surface demand vs underlying need), explicitly map tensions and tradeoffs (who wins/loses for each option), and synthesize concrete resolution addressing core interests (not forced consensus). Apply RACI for decision authority, power-interest mapping for stakeholder prioritization, sequential decision-making (phase X satisfies role A, phase Y satisfies role B), hybrid approaches (tiered pricing serves multiple segments), risk mitigation for each role's fears, and escalation paths when consensus fails. Covers build vs buy decisions, feature prioritization, pricing strategy, organizational change, technical migrations, regulatory compliance tradeoffs. Use for stakeholder conflict resolution, cross-functional alignment, pressure-testing proposals, navigating complex tradeoffs, and preparing for multi-party facilitation meetings.

### 💭 Ideation & Creativity

**brainstorm-diverge-converge** - Divergent ideation (generate many ideas) followed by convergent clustering and prioritization using affinity mapping and dot voting.

**constraint-based-creativity** - Generate creative solutions by systematically applying constraints (remove, combine, extreme, reverse) to force novel thinking.

**morphological-analysis-triz** - Systematic innovation through morphological analysis (parameter-option matrices) and TRIZ (Theory of Inventive Problem Solving). Build morphological boxes with 3-7 independent parameters and 2-5 options each to explore design space systematically, generating and evaluating configurations. Resolve technical contradictions (improve parameter A worsens parameter B) using 40 inventive principles and contradiction matrix: common trade-offs include speed vs precision, strength vs weight, cost vs quality, capacity vs size. Apply principles through creative adaptation (segmentation, taking out, nesting, asymmetry, dynamics, feedback, intermediary, self-service). Covers trends of technical evolution (mono-bi-poly, micro-level transition, increasing dynamism), substance-field analysis for modeling interactions, ARIZ algorithm for complex problems, combining MA+TRIZ for multi-parameter systems with contradictions, and adapting TRIZ to software/services (weight→code size, segmentation→microservices). Includes all 40 principles with detailed examples, contradiction matrix guidance, configuration evaluation frameworks, and feasibility assessment. Use for product design, engineering solutions, process optimization, and identifying patent opportunities.

### 📊 Data & Modeling

**data-schema-knowledge-modeling** - Design data schemas, knowledge graphs, and conceptual models with entity-relationship diagrams and ontology patterns.

**code-data-analysis-scaffolds** - Generate code scaffolds for data analysis, visualization, and statistical testing across Python, R, and SQL.

**visualization-choice-reporting** - Choose the right chart for your data and question, then create narrated reports with insights and recommended actions. Match 8 question types to chart families (trend→line, comparison→bar, distribution→histogram, relationship→scatter, composition→treemap, geographic→map, hierarchical→tree, multivariate→small multiples/heatmap). Apply visualization best practices (insight-first titles not generic descriptors, Y-axis zero for bar/column, annotate key patterns, colorblind-safe palettes blue-orange, remove chart junk 3D/gradients, mute non-data ink with light gray gridlines, direct labels preferred over legends, source timestamp cited). Create narrated dashboards using Headline→Pattern→Context→Meaning→Action framework (headline: 'Revenue up 30% YoY driven by Enterprise' not 'Revenue by Month', pattern: describe specifics 'Q1-Q2 flat then climb to Q4', context: vs target/history/industry, meaning: why it matters 'suggests PMF', actions: specific next steps with owners/timelines). Design dashboards with F-pattern layout (top-left most important), inverted pyramid (summary→details→deep-dive), scorecards with big numbers trend indicators, bullet charts for performance vs target, traffic light RAG status, small multiples with consistent scales. Handle advanced chart types (sparklines inline trends, horizon charts space-efficient time series, connected scatter temporal trajectory, hexbin dense scatter 1000s+ points, alluvial state flows, SPLOM scatter matrix, parallel coordinates multi-dimensional, bubble 4D with X/Y/size/color). Apply statistical overlays (regression R² annotation, confidence intervals shaded bands/error bars, distribution overlays histogram+normal curve). Use geographic patterns (choropleth filled regions sequential/diverging scales, bubble map precise locations, flow map origin-destination). Apply hierarchical visualizations (treemap nested rectangles drill-down, sunburst radial compact deep hierarchies, dendrogram clustering, network force-directed/hierarchical layout). Master color theory (sequential light→dark single metric, diverging blue→white→red meaningful midpoint, categorical distinct hues limit 5-7, accessibility 4.5:1 contrast colorblind-safe tested). Implement interactivity (filtering dropdown/multi-select/date-slider/cross-filter, drill-down with breadcrumbs, tooltip hover exact value context metadata 2-4 lines, brushing linking range selection updates other charts). Quality assurance 10 weighted criteria: Chart Selection Appropriateness 1.5x (matches question/data), Design Quality 1.4x (perceptual best practices chart-junk-free), Narrative Quality 1.5x (Headline→Pattern→Context→Meaning→Action complete), Insight Clarity 1.4x (obvious in 5 seconds), Actionability 1.3x (specific feasible next steps), Accuracy 1.5x (truthful not misleading), Context Benchmarking 1.2x (vs target/history/industry), Accessibility 1.1x (colorblind alt-text contrast patterns), Audience Appropriateness 1.2x (expertise goals time constraints), Overall Quality 1.3x (answers question drives action). Covers business analytics (revenue growth churn funnel cohort), product metrics (usage adoption retention A/B tests), marketing analytics (campaign ROI attribution CAC), financial reporting (P&L budget forecast variance waterfall), operational monitoring (uptime performance SLA percentiles), sales analytics (pipeline forecast territory quota), HR metrics (headcount turnover engagement DEI). Common failure modes avoided: wrong chart type (pie 8 slices→bar), misleading scale (truncated Y-axis bar→zero), no insight (generic title→insight-first), chart junk (3D gradients→clean 2D), no context (absolute numbers→vs benchmarks), vague actions ('monitor'→specific who/what/when), wrong audience (5-screen exec dashboard→1-screen), colorblind red-green→blue-orange+patterns, no narrative (description→Headline→Action story). Includes comprehensive template with question clarification, data profiling, chart selection rationale, design specification, narrative development, validation checklist, advanced methodology for dashboards/multivariate/interactive/domain-specific patterns, and quality rubric with context-specific guidance (executive dashboard, analyst deep-dive, stakeholder report, monitoring dashboard, presentation).

**mapping-visualization-scaffolds** - Create visual maps that make relationships, dependencies, and structures explicit through diagrams, concept maps, and architectural blueprints. Choose from 5 visualization formats (List, Tree, Network Graph, Layered Diagram, Swimlane) based on complexity. Use for system architecture diagrams, concept maps, dependency graphs, process flows, organizational charts, and knowledge taxonomies. Includes format selection guidance, node/relationship documentation templates, and 8-criteria quality rubric.

**metrics-tree** - Decompose North Star metrics into actionable sub-metrics, leading indicators, and prioritized experiments. Apply decomposition methods (additive, multiplicative, funnel, cohort) to break down business metrics (WAU, GMV, MRR, revenue) into 3-5 input metrics (L2), map to specific user behaviors (L3 action metrics), identify early signals that predict North Star movement (leading indicators with timing and correlation strength), and prioritize experiments using ICE framework (Impact × Confidence × Ease). Covers North Star selection criteria (value delivery, business model alignment, actionability), causal relationship validation, multi-sided marketplace metrics (dual trees with balance metrics), counter-metrics and guardrails (quality, gaming prevention), network effects and viral loops (K-factor, network density), and stage-appropriate metrics (pre-PMF retention focus, growth-stage efficiency). Includes comprehensive guidance by business model (SaaS, marketplace, e-commerce, social, mobile), advanced techniques (propensity scoring, cohort clustering, inflection point analysis), and production-ready output templates.

### 🏗️ Architecture & Design

**adr-architecture** - Document architecture decisions with context, options considered, consequences, and tradeoffs using Architecture Decision Records.

**chain-spec-risk-metrics** - Progressive refinement from specification → risk analysis → success metrics with cross-validation at each stage.

**information-architecture** - Organize, structure, and label content for digital products to maximize findability and usability. Conduct card sorting (open, closed, hybrid) with 15-30 users to understand mental models, create MECE taxonomies (mutually exclusive, collectively exhaustive), design faceted navigation for large content sets, and validate structure with tree testing (≥70% success rate, ≤1.5× directness). Optimize navigation depth (3-4 levels, 5-9 items per level), strengthen information scent (clear labels, trigger words, breadcrumbs), and provide multiple access paths (browse, search, filters, tags). Includes content audit templates, sitemap design, metadata schemas, and governance frameworks. Covers e-commerce, documentation, SaaS, and knowledge base IA patterns.

**cognitive-design** - Apply cognitive psychology principles to design interfaces, visualizations, and content that align with how humans perceive, attend, remember, and process information. Ground decisions in perception research (preattentive processing, visual search patterns F/Z, attention spotlight), memory constraints (working memory 4±1 chunks, recognition over recall), Gestalt principles (proximity, similarity, continuity, closure, figure-ground), visual encoding hierarchy (Cleveland & McGill: position > length > angle > area), and mental models (Jakob's Law, affordances, natural mapping). Apply three systematic frameworks: Cognitive Design Pyramid (4-tier quality assessment: perceptual efficiency → cognitive coherence → emotional engagement → behavioral alignment), Design Feedback Loop (5-stage interaction cycle: perceive → interpret → decide → act → learn), and Three-Layer Visualization Model (data quality → visual encoding → cognitive interpretation). Use evaluation checklists across 8 dimensions (visibility, hierarchy, chunking, simplicity, memory support, feedback, consistency, scanning patterns) and 4-criteria visualization audit (clarity, efficiency, integrity, aesthetics with 1-5 scoring). Covers UX/product design (forms, navigation, dashboards, mobile interfaces with standard UI patterns), data visualization (chart selection matching task to perceptual encoding, color theory for categorical/quantitative/diverging data, dashboard design), educational design (chunking lessons, multimedia learning principles, progressive disclosure, scaffolding), storytelling/journalism (narrative arc, cognitive fluency, information scent), and avoiding cognitive fallacies (chartjunk, rainbow colormaps, pie charts for comparison, truncated axes, decoration over data). All resource files under 500 lines for focused reference. Use when designing user interfaces, creating data visualizations, developing educational content, evaluating existing designs for cognitive issues, explaining design rationale with research backing, or teaching design principles.

### 🔒 Security & Risk

**security-threat-model** - Systematically identify security vulnerabilities, threats, and mitigations for systems handling sensitive data using STRIDE methodology (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege). Map system architecture with trust boundaries (User→App, App→DB, Internal→External, Public→Private), classify data by sensitivity and compliance requirements (PII/PHI/PCI, GDPR/HIPAA/PCI DSS/SOC 2), apply STRIDE to each boundary with likelihood×impact risk scoring (1-25 scale), and define defense-in-depth mitigations (preventive controls block attacks, detective controls identify attacks, corrective controls enable response/recovery). Covers web applications (SQLi, XSS, CSRF, IDOR), mobile apps (certificate pinning, reverse engineering, local data theft), cloud infrastructure (IAM misconfiguration, public S3, credential theft), APIs (BOLA, rate limiting, OAuth), IoT (firmware tampering, network segmentation), enterprise systems, and compliance-critical domains. Includes architecture diagramming, data classification tables, STRIDE analysis per boundary, attack trees for complex threats, DREAD scoring (Damage, Reproducibility, Exploitability, Affected Users, Discoverability), monitoring thresholds, incident response plans with RTO/RPO, risk prioritization matrix, and action items with owners/deadlines. Use for security reviews before launch, compliance audits (PCI, HIPAA, SOC 2), incident investigations, third-party integration assessments, or any system handling credentials, PII, PHI, or financial data.

### 📝 Communication & Documentation

**communication-storytelling** - Craft compelling narratives using story arcs, tension-resolution, concrete details, and audience-specific framing.

**translation-reframing-audience-shift** - Adapt content between audiences with different expertise, context, or goals while preserving semantic accuracy but changing presentation. Master four fidelity types: semantic (MUST preserve facts, relationships, constraints, implications), tonal (adapt formality, emotion, register), emphasis (shift what's highlighted based on audience priorities), and medium (change structure, length, format). Apply six core translation types: technical↔business (implementation details ↔ business value, "so what?" test), strategic↔tactical (vision/goals ↔ actions/tasks, "how?" test), expert↔novice (domain jargon ↔ plain language with analogy bridges), formal↔informal (professional report ↔ casual communication), long-form↔summary (comprehensive ↔ highlights via inverted pyramid), and internal↔external (company context ↔ customer-facing). Profile audiences across expertise level (expert/intermediate/novice), primary goals (decision-makers want options/trade-offs, implementers want how-to, learners want understanding, stakeholders want impact/next-steps), context constraints (time available, medium, familiarity, sensitivity), and cultural/demographic factors (language comfort, generation, industry, geography). Use advanced techniques: multi-audience translation (parallel versions for each audience, layered progressive disclosure L0 headline→L4 full detail, modular mix-and-match content blocks), fidelity trade-off framework (safety-critical preserves accuracy absolutely, high-stakes decisions preserve key caveats, educational simplifies with disclaimers, informational rounds appropriately), domain-specific patterns with translation tables (technical→business: "migrated to microservices"→"scale independently, 30% cost reduction", strategic→tactical: "become data-driven"→"Q1 instrument flows, Q2 train PMs, Q3 metrics review"), cultural code-switching (replace idioms: "home run"→"big success", adapt date formats MM/DD/YYYY→YYYY-MM-DD ISO), and back-translation testing for semantic drift detection. Apply quality frameworks: "so what?" test (every technical detail answers business value), "how?" test (every strategic goal specifies concrete actions), analogy bridge (familiar domain→unfamiliar concept with structural mapping), inverted pyramid (most important first for busy audiences), and validation via "would expert confirm accuracy?" and "can target act on it?". Avoid pitfalls: semantic drift (facts become inaccurate through simplification), jargon mismatch (too technical or too simple), wrong emphasis (highlighting source's interests vs target's needs), missing "so what?" (technical without business impact), missing "how?" (vision without tactics), lost nuance (critical caveats omitted), cultural assumptions (idioms excluding target), and talking down (condescending to novices). Covers engineering→executive summaries, medical→patient explanations, academic→blog posts, API docs→customer guides, strategy→OKRs, security→legal/compliance, board presentations→team action items, roadmaps→public updates, bug tracking→known issues, 50-page docs→1-page briefs, annual reports→social posts, US→international markets, Gen Z→Boomer messaging, and any scenario where same core message needs different presentation for different stakeholders while maintaining correctness. Includes structured template with audience characterization, translation mapping (what must change vs preserve), translation diff tables, fidelity validation checklists, and delivery package with rationale.

**writer** - Transform writing into precise, compelling prose using structured revision (Zinsser, King, Pinker), structural architecture (McPhee), and stickiness techniques (SUCCESs framework).

**one-pager-prd** - Create concise product specifications (1-2 pages) for stakeholder alignment covering problem statement (user pain with quantified impact), solution overview (high-level approach without over-specifying), user personas and use cases, SMART metrics (baselines + targets, leading/lagging indicators), scope boundaries (MVP vs future, in/out explicit), constraints and assumptions, and open questions. Apply problem framing techniques: Jobs-to-be-Done ("When I [situation], I want to [motivation], so I can [outcome]"), 5 Whys root cause analysis, problem statement formula with evidence (interviews, analytics, support tickets). Use metric trees to decompose North Star into actionable sub-metrics. Apply scope prioritization: MoSCoW (Must/Should/Could/Won't), RICE scoring (Reach × Impact × Confidence / Effort), Kano model (basic/performance/delight needs), value-effort matrix. Write for clarity using pyramid principle (lead with conclusion), active voice, concrete language, abundant examples, scannable formatting (bullets, headers, tables). Manage stakeholders by tailoring content (engineering: constraints/dependencies, design: flows/personas, business: impact/ROI, legal: compliance). Apply user story mapping to visualize journey and slice features vertically. Includes one-pager template (1 page, bullets, quick approval) and full PRD template (1-2 pages, detailed requirements, execution guide). Covers feature proposals, new products, technical initiatives, platform projects, internal tools, strategic initiatives. For B2B (emphasize ROI, security, integrations), B2C (emphasize delight, viral potential), enterprise (emphasize compliance, customization).

### 🔬 Scientific Writing

**scientific-manuscript-review** - Review and edit research manuscripts using IMRaD structure (Introduction, Methods, Results, Discussion). Provides section-specific guidance for abstracts, introductions (knowledge gap → research question → hypothesis), methods (reproducibility checklist), results (figure/table integration, statistical reporting), and discussion (interpretation, limitations, future directions). Includes clarity checking for scientific claims, evidence-claim alignment, and appropriate hedging.

**grant-proposal-assistant** - Assist with NIH/NSF grant proposals using established frameworks. Covers Specific Aims page structure (one-page with hook, gap, solution, aims), Research Strategy sections (Significance, Innovation, Approach), and reviewer perspective analysis. Includes templates for R01, R21, R03, and K-series applications with compliance checklists and common pitfall avoidance.

**academic-letter-architect** - Craft compelling academic letters including recommendations, nominations, and references. Provides framework for context gathering (relationship, duration, context), evidence collection (specific achievements with quantification), comparative statements (percentile rankings, peer comparisons), and tone calibration by letter type and career stage.

**scientific-email-polishing** - Polish professional scientific correspondence including cover letters to editors, responses to reviewers, collaboration requests, and conference communications. Covers subject line optimization, tone calibration (formal to collegial), clear ask formulation, and response-to-reviewers strategy (acknowledge, address, explain pattern).

**scientific-clarity-checker** - Cross-cutting scientific logic review for any document type. Audits claims against evidence, checks hedging appropriateness (matches evidence strength), validates terminology consistency, maps argument logic flow, and identifies gaps in mechanistic explanations. Applies to manuscripts, grants, or any scientific writing.

**career-document-architect** - Develop academic career documents including research statements, teaching statements/philosophy, diversity statements, CVs, and biosketches. Covers narrative development (vision + track record), audience analysis (search committee priorities), institutional fit demonstration, and format-specific templates (NIH biosketch, academic CV, faculty application statements).

### 🎯 Estimation & Forecasting

**chain-estimation-decision-storytelling** - Fermi estimation → decision recommendation → compelling narrative for presenting quantitative insights.

**estimation-fermi** - Order-of-magnitude estimation via decomposition (top-down, bottom-up, rate×time), bounding techniques, triangulation, and anchoring for market sizing, resource planning, and feasibility checks.

### 💼 Business & Product Management

**financial-unit-economics** - Analyze business model viability through customer profitability metrics (CAC, LTV, contribution margin). Calculate fully-loaded acquisition costs, cohort-based lifetime value, LTV/CAC ratio (target >3:1), payback period (<12 months), conduct channel-level analysis, and provide actionable recommendations on pricing, retention, and growth strategy. Covers SaaS, e-commerce, marketplace, freemium, and enterprise models.

**facilitation-patterns** - Design and run productive group sessions (meetings, workshops, brainstorms, retrospectives) using proven facilitation patterns. Select appropriate formats (divergent brainstorm, convergent decision, alignment session), design time-boxed agendas with diverge-converge flow, manage participation dynamics (round robin, silent writing, breakouts), handle difficult situations (dominators, conflict, tangents), and apply decision-making methods (consensus, consent, vote, advisory). Includes remote and hybrid facilitation techniques.

**negotiation-alignment-governance** - Create explicit stakeholder alignment through decision rights frameworks (RACI/DACI/RAPID), working agreements, and conflict resolution protocols. Map stakeholders by power-interest to plan engagement (manage closely, keep satisfied, keep informed, monitor). Apply principled negotiation (Harvard Method): separate people from problem, focus on interests not positions, generate mutual-gain options, use objective criteria. Develop BATNA (Best Alternative To Negotiated Agreement) and analyze ZOPA (Zone of Possible Agreement) for strategic positioning. Establish unambiguous decision authority (exactly one Accountable/Approver per decision), specific working agreements (observable communication norms, response times, quality standards), and 3-level conflict resolution (direct dialogue → mediation → escalation with disagree-and-commit). Use advanced governance patterns: federated (central standards + local autonomy), rotating leadership, bounded delegation, tiered decisions (fast/reversible vs slow/irreversible), dual authority (opportunity + risk checks). Apply conflict mediation techniques (active listening, interest-based problem solving, reframing, finding common ground, caucusing), facilitation patterns (structured dialogue, decision methods, timeboxing), and multi-party negotiation strategies. Covers cross-functional coordination, org restructures, partnerships, distributed teams, and product/engineering alignment. Includes stakeholder mapping templates, negotiation preparation frameworks, governance sustainability mechanisms (quarterly reviews, metrics, triggers), and coalition-building strategies.

**roadmap-backcast** - Plan backward from fixed deadline or target outcome to identify required milestones, dependencies, critical path, and assess feasibility. Work backward asking "what must be true just before?" to create 5-10 sequenced milestones from target to present. Map dependencies (sequential A→B, parallel A∥B, converging A,B→C, diverging A→B,C) and identify critical path (longest dependent chain determining minimum timeline) using CPM forward/backward pass calculations. Add risk-calibrated buffers (20-30% moderate uncertainty, 40%+ high uncertainty/regulatory), assess feasibility (required time with buffer ≤ available time), and provide options if infeasible (extend deadline, reduce scope, add resources with cost/benefit). Apply resource leveling and smoothing to resolve over-allocation, use PERT 3-point estimates (optimistic/likely/pessimistic) for Monte Carlo probability analysis (P50/P80/P95 confidence levels), implement buffer management (project buffer, feeding buffers), and establish communication plan with Go/No-Go gates at milestones. Covers product launches with hard dates, compliance deadlines (regulatory, audit), multi-year strategic transformations, event planning (conferences, releases), and cross-functional initiatives. Includes CPM mathematics, CCPM buffer techniques, fast-tracking/crashing analysis, and resource optimization methods. Use for any planning scenario with fixed deadline where working backward from target reveals feasibility constraints and critical dependencies.

### ⏱️ Productivity & Learning

**focus-timeboxing-8020** - Manage attention and maximize high-impact work through 80/20 principle (identify vital few tasks), timeboxing (Pomodoro 25min, deep work 90-120min blocks), and energy management. Design distraction-free focus blocks, batch similar tasks (email 2×/day, meeting blocks), match work intensity to energy levels (peak hours for deep work, trough for admin), and use Parkinson's Law (time constraints force decisions). Includes weekly/daily planning templates, execution discipline techniques, and progressive focus training.

**memory-retrieval-learning** - Create evidence-based learning plans for durable knowledge retention using spaced repetition (1-3-7-14-30 day intervals), retrieval practice (active recall over passive review), and interleaving. Design study schedules with realistic time estimates (1.5x buffer, 0.7 consistency factor), choose retrieval methods by material type (flashcards for facts, practice problems for procedures, mock tests for exams), track retention metrics (target ≥70%), and adjust based on performance. Covers exam prep (certifications, medical boards, bar exam), language learning, technology skill acquisition, and professional development. Includes diagnostic framework for plateaus, motivation strategies (implementation intentions, temptation bundling), and long-term maintenance schedules.

**socratic-teaching-scaffolds** - Guide learners to discover knowledge through strategic Socratic questioning and progressive scaffolding support that fades as competence grows. Diagnose current understanding and misconceptions through probing questions (clarifying, probing assumptions/evidence, exploring implications, revealing contradictions), design question ladders building from concrete examples to abstract principles (concrete foundation → pattern recognition → formalization → edge cases → transfer), provide graduated scaffolding (Level 5 full modeling → Level 4 guided practice → Level 3 coached practice → Level 2 independent feedback → Level 1 transfer/teaching others), correct deep misconceptions through prediction-observation-explanation (not assertion), and validate understanding through multi-level transfer (near/far/creative). Apply cognitive apprenticeship model (modeling → coaching → scaffolding → articulation → reflection → exploration), maintain Zone of Proximal Development (neither boredom nor frustration), use Feynman explanations (ELI5 → undergraduate → expert levels), and test with teaching simulation ("How would you teach this? What would confuse learners?"). Covers technical concepts (programming, algorithms, mathematics), scientific principles (physics, statistics, biology), professional skills (debugging, problem-solving, analysis), mentoring, onboarding, and self-directed learning material design. Includes diagnostic techniques (mental model elicitation, POE, misconception taxonomy), multi-ladder design for complex topics, adaptive questioning with branching, scaffolding fading protocols, spaced retrieval for persistent misconceptions, and transfer validation across Bloom's taxonomy levels.

**meta-prompt-engineering** - Transform vague prompts into reliable, structured prompts that produce consistent outputs through explicit roles, task decomposition, constraints, and quality checks. Apply role specification patterns (Expert/Assistant/Critic/Creator), break tasks into 3-7 clear steps with deliverables, define format/length/tone/content constraints, add self-evaluation criteria with fix instructions, and test for ≥80% consistency across runs. Use advanced patterns for complex cases: chain-of-thought with verification (5-step Understand→Plan→Execute→Verify→Present), self-consistency ensemble (3 independent solutions), least-to-most prompting (simple→complex), constitutional AI safety checks, and anti-hallucination layering. Includes iterative refinement protocol, A/B testing framework, prompt debugging taxonomy, multi-prompt workflows (sequential chaining, self-refinement loops), domain adaptation checklist, production deployment guide (versioning, monitoring, graceful degradation), and cost-quality tradeoff analysis. Covers code generation, content writing, data analysis, research synthesis, and creative tasks with domain-specific quality criteria.

**reviews-retros-reflection** - Conduct structured team retrospectives and reflection sessions using 5-stage process (Set Stage → Gather Data → Generate Insights → Decide Actions → Close). Apply multiple formats based on context: Start/Stop/Continue (action-oriented, 30 min), Mad/Sad/Glad (emotion processing, morale), 4Ls (Loved/Learned/Lacked/Longed for, comprehensive depth), Sailboat (visual/strategic with Wind/Anchor/Rocks/Island metaphor), Timeline (chronological for complex periods). Establish psychological safety through Prime Directive ("everyone did best job given knowledge/skills/resources"), blameless language (systems-focused not people-focused), and confidentiality norms. Generate 1-3 SMART actions (Specific, Measurable, Assigned owner, Realistic, Time-bound) addressing root causes not symptoms, track completion rate (target >80%), and review previous actions systematically. Apply root cause techniques (5 Whys, fishbone diagrams, timeline analysis), facilitation patterns (silent brainstorming, dot voting, round-robin sharing, time-boxing), and participation balancing (ensuring all voices heard). Track retro health metrics (action completion, ROTI scores, participation rate) and continuous improvement over time. Covers sprint retrospectives, project post-mortems, weekly team reviews, incident after-action reviews, quarterly reflections, and team health checks. Includes remote/async facilitation techniques, action tracking dashboards, and advanced formats (Lean Coffee, Perfection Game, Starfish, Kaleidoscope multi-perspective). Use for Agile teams, project-based work, leadership teams, cross-functional collaboration, and establishing continuous learning culture.

### 🏢 Organizational Design

**stakeholders-org-design** - Map stakeholders and design effective organizational structures aligned with system architecture. Apply stakeholder mapping (power-interest matrix for engagement strategy, RACI for decision rights with exactly one Accountable, influence networks identifying champions/blockers/bridges/gatekeepers), design team structures using Conway's Law alignment (reverse Conway maneuver: design teams to match desired architecture, not current org), apply Team Topologies framework (stream-aligned product teams, platform teams providing internal services, enabling teams for capability building, complicated-subsystem teams for specialists, 3 interaction modes: collaboration/X-as-a-Service/facilitating), define team interface contracts (API contracts with endpoints/SLAs/versioning, organizational handoffs for Design→Eng/Eng→QA, decision rights via DACI framework), assess capability maturity (DORA metrics: deployment frequency/lead time/MTTR/change failure rate with Elite/High/Medium/Low levels, generic CMM 1-5 levels, custom capability assessments), and create transition plans (incremental/pilot approaches, governance with steering committee/working group, success metrics baselined). Covers organizational restructuring (functional→product teams, platform team extraction, microservices alignment), stakeholder management for change initiatives, cross-functional collaboration models (product triads, embedded vs centralized specialists), Domain-Driven Design bounded context alignment, and org refactoring patterns (cell division, merging, extraction, embedding). Includes Spotify model (squads/tribes/chapters/guilds), Amazon 2-pizza teams, mature platform staffing (1 platform engineer per 7-10 product engineers), team sizing constraints (5-9 people, 2-pizza rule, Dunbar's number), cognitive load limits (1 simple domain, 2-3 related, max 1 complex per team, <10% coordination time), and coalition building for organizational change.

### 🛡️ Ethics & Evaluation

**ethics-safety-impact** - Systematic ethical assessment using stakeholder mapping, fairness metrics (demographic parity, equalized odds, calibration), harm/benefit analysis with risk scoring, privacy-preserving techniques (differential privacy, k-anonymity), and comprehensive monitoring frameworks for responsible AI and product development.

**evaluation-rubrics** - Design reliable evaluation rubrics with explicit criteria, appropriate scales (1-5, qualitative, binary), observable descriptors, inter-rater reliability measurement (Kappa ≥0.70), calibration techniques, bias mitigation (halo, central tendency), and weighted scoring for consistent quality assessment.

### 🍳 Specialized Domains

**chef-assistant** - Expert culinary guide combining technique, food science, flavor architecture (salt/acid/fat/heat), cultural context, and plating. Covers recipe creation, troubleshooting, menu planning, and cooking methods across global cuisines.

**d3-visualization** - Implement custom, interactive data visualizations using D3.js for bar/line/scatter charts, network diagrams, geographic maps, hierarchical layouts (treemap, force simulation), and data-driven animations. Covers selections, data joins, scales (12 types), shape generators, transitions, zoom/pan/drag/brush interactions, and step-by-step workflows for translating visualization designs into working D3 code.

### 🛠️ Skill Development & Meta-Tools

**skill-creator** - Transform documents containing theoretical knowledge into actionable, reusable Claude Code skills using Mortimer Adler's analytical reading methodology. Apply 6-step progressive workflow with file-based context management to prevent overflow: (1) Inspectional Reading - systematic 10-30 minute skim, classify document type (methodology/framework/tool/theory), assess skill-worthiness using 5 criteria (teachability, generalizability, recurring problem, actionability, completeness) with 1-5 scoring (threshold ≥3.5), get user approval; (2) Structural Analysis - classify content (practical vs theoretical, sequential/categorical/structured/hybrid), state unity in one sentence, enumerate major parts with relationships, define problems solved, validate with user; (3) Component Extraction - choose reading strategy (section-based for <50 pages, windowing for >50 pages, targeted for hybrid), extract 5-15 key terms (vocabulary), 5-10 propositions (principles explaining why it works), arguments (logical sequences becoming workflow steps), and solutions (examples/templates), write section-by-section to workspace file to manage context, synthesize into final extraction; (4) Synthesis & Application - evaluate completeness and logic, identify practical application scenarios across domains, transform propositions into principles, arguments into workflow steps, theory into actionable procedures, define triggers (when/how to use), validate with user; (5) Skill Construction - determine complexity (simple/moderate/complex), plan resource file structure, create SKILL.md with YAML frontmatter (description focuses on WHEN not WHAT), table of contents, "Read This First" section, workflow with explicit "COPY THIS CHECKLIST" instruction, step definitions linking to resources, create resource files with WHY (brief theory for context activation) and WHAT (specific instructions with options/tradeoffs) subsections, create JSON evaluation rubric with 8 criteria (completeness, clarity, actionability, structure, triggers, resource quality, user collaboration, file size) scored 1-5 with threshold ≥3.5, verify all files <500 lines; (6) Validation & Refinement - score skill using rubric, present scores with rationale, identify areas <3 requiring revision, make refinements based on user decision, re-validate. File-based workflow prevents context overflow: each step writes output to `step-N-output.md` and updates `global-context.md`, next step reads both. User collaboration at decision points (proceed/modify after each major step, reading strategy choice, gap handling, workflow validation, structure approval). Components map to skill: Terms → Key Concepts/glossary in resources, Propositions → WHY sections explaining importance, Arguments → WHAT sections + workflow steps, Solutions → Examples/templates/case studies. Use when user has PDF/markdown/research paper/methodology guide containing theory and wants to convert into actionable skill, mentions "create skill from this document", "turn this into a skill", "extract skill from file", or when analyzing documents with frameworks/processes/systematic approaches for skill creation. Covers methodologies, theoretical frameworks, research papers, procedural guides, and systematic approaches requiring transformation from knowledge into executable workflows.

## Installation

### Option 1: Install as Plugin (Recommended)

Install the entire skills collection as a Claude Code plugin:

1. Add the marketplace in Claude Code:
   ```
   /plugin marketplace add lyndonkl/claude
   ```

2. Install the plugin:
   ```
   /plugin install thinking-frameworks-skills
   ```

All 62 skills will be automatically available. Skills are model-invoked—Claude autonomously uses them based on your request and the skill's description.

### Option 2: Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/lyndonkl/claude.git
   cd claude
   ```

2. Copy skills to your Claude Code skills directory:
   ```bash
   # On macOS/Linux
   cp -r skills/* ~/.claude/skills/

   # On Windows
   xcopy skills\* %USERPROFILE%\.claude\skills\ /E /I
   ```

3. Skills will be automatically available in Claude Code. Use trigger phrases to activate them (see each skill's SKILL.md for trigger phrases).

### Skill Structure

Each skill follows a consistent structure:

```
skill-name/
├── SKILL.md                              # Main entry point (< 300 lines)
│   ├── YAML metadata with trigger phrases
│   ├── Purpose and when to use
│   ├── Workflow with checkboxes
│   ├── Common patterns
│   └── Guardrails and quick reference
│
├── resources/
│   ├── template.md                       # Practical templates (< 400 lines)
│   ├── methodology.md                    # Advanced techniques (< 500 lines)
│   └── evaluators/
│       └── rubric_[skill].json          # Quality criteria and evaluation
```

## Using Skills

### Activation

Skills activate automatically when you use trigger phrases in conversation:

```
"Help me make a decision between three options..." → decision-matrix
"I need to conduct user research interviews..." → discovery-interviews-surveys
"Design an experiment to test..." → design-of-experiments
"I'm cooking chicken and it's always dry..." → chef-assistant
```

### Workflow Pattern

Most skills follow a checkbox workflow:

```markdown
Skill Progress:
- [ ] Step 1: Define objective
- [ ] Step 2: Gather inputs
- [ ] Step 3: Apply framework
- [ ] Step 4: Evaluate results
- [ ] Step 5: Document findings
```

### Progressive Depth

- **SKILL.md**: Quick overview, common patterns, guardrails
- **template.md**: Ready-to-use templates and structures
- **methodology.md**: Advanced techniques and edge cases
- **rubric**: Quality criteria and self-evaluation

## Skill Development Status

**Production Ready**: 41 skills
- ✓ 33 refined skills from standard collection
- ✓ 1 original skill (writer)
- ✓ 1 custom skill (chef-assistant)
- ✓ 6 scientific writing skills (manuscript review, grants, letters, emails, clarity, career docs)

**In Development**: 23 skills remaining from standard collection

## Key Features

### Quality Standards

All skills meet rigorous quality criteria:
- ✓ File size limits (SKILL.md < 300, template.md < 400, methodology.md < 500 lines)
- ✓ Comprehensive evaluation rubrics with 1/3/5 scoring
- ✓ Guidance by type/complexity with target scores
- ✓ Common failure modes with detection and fixes
- ✓ Practical examples and templates
- ✓ Progressive disclosure architecture

### Evaluation Rubrics

Each skill includes a comprehensive rubric with:
- **10 evaluation criteria** with clear 1/3/5 scoring
- **Guidance by type** (5+ categories specific to skill domain)
- **Guidance by complexity** (Simple, Moderate, Complex with target scores)
- **Common failure modes** (8+ patterns with symptom, detection, fix)

Example criteria:
- Problem definition clarity
- Methodology rigor
- Practical applicability
- Documentation quality
- Common pitfall avoidance

## Contributing

This is a personal skills collection for Claude Code. If you'd like to suggest improvements or report issues:

1. Fork the repository
2. Create a feature branch
3. Make your changes following the skill structure guidelines
4. Submit a pull request with clear description

### Skill Guidelines

When creating or refining skills:
- Focus on WHEN to use (trigger phrases in YAML description)
- Start with workflow checklist (checkbox format)
- Provide common patterns with examples
- Include critical guardrails
- Add comprehensive troubleshooting
- Self-assess against rubric (target ≥ 3.5)

## Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/)

## License

This project is open source and available for use with Claude Code. See individual skills for specific attributions and influences.

## Acknowledgments

Skills draw from established frameworks and expert practitioners:

- **Thinking frameworks**: Bayesian reasoning, causal inference, dialectics, first principles
- **Research methods**: Jobs-to-be-done (Christensen), design of experiments (Box, Taguchi), user research (Torres, Ulwick)
- **Decision-making**: Multi-criteria analysis, expected value, risk analysis
- **Communication**: Story structure (McKee), clarity writing (Zinsser, Pinker, King), SUCCESs framework (Heath)
- **Culinary arts**: Technique (Pépin, Child, López-Alt), food science (McGee, Sharma), cultural cooking (Bourdain, Chang, Ottolenghi)

---

**Status**: 69 production-ready skills | Active development | Last updated: 2025-12-13

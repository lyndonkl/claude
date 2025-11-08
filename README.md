# Claude Code Skills Collection

A comprehensive collection of production-ready skills for Claude Code, covering thinking frameworks, decision-making tools, research methods, design patterns, and specialized domains.

## Overview

This repository contains **24 skills** designed to enhance Claude Code's capabilities across strategic thinking, product development, research, experimentation, and creative problem-solving. Each skill includes:

- **Structured workflows** with step-by-step guidance
- **Practical templates** for immediate use
- **Advanced methodologies** for complex scenarios
- **Evaluation rubrics** with quality criteria and common failure modes
- **Progressive disclosure** (SKILL.md → template.md → methodology.md)

## Skills by Category

### 🧠 Strategic Thinking & Decision Making

**decision-matrix** - Multi-criteria decision analysis with weighted scoring, sensitivity analysis, and uncertainty handling for complex choices between 3-10 options.

**bayesian-reasoning-calibration** - Probabilistic reasoning with prior/posterior updates, Bayes theorem application, and calibration techniques for reducing overconfidence.

**alignment-values-north-star** - Strategic alignment framework connecting daily decisions to core values and long-term vision using north star metrics and principle mapping.

**environmental-scanning-foresight** - Anticipate change through PESTLE analysis, weak signal detection, scenario planning (2x2 matrix), cross-impact analysis, and signposts for early warning systems.

**expected-value** *(coming soon)* - Expected value calculations for decision-making under uncertainty.

### 💡 Problem Solving & Analysis

**decomposition-reconstruction** - Break complex problems into components, analyze independently, then reconstruct with understanding of interactions and emergent properties.

**causal-inference-root-cause** - Identify true causes vs. correlations using causal diagrams, counterfactuals, and root cause analysis (5 Whys, Ishikawa diagrams).

**abstraction-concrete-examples** - Move fluidly between abstract concepts and concrete examples to clarify thinking, test understanding, and communicate effectively.

**layered-reasoning** *(coming soon)* - Multi-level reasoning across different abstraction layers.

### 🔬 Research & Discovery

**discovery-interviews-surveys** - Design and conduct user research using jobs-to-be-done interviews, surveys, thematic coding, and statistical analysis while avoiding bias.

**design-of-experiments** - Plan rigorous experiments using factorial designs, response surface methodology, Taguchi methods, and statistical power analysis.

**domain-research-health-science** - Formulate clinical research questions (PICOT framework), evaluate evidence quality using GRADE certainty ratings, systematic bias assessment (Cochrane RoB 2, ROBINS-I, QUADAS-2), and conduct systematic reviews with meta-analysis.

### 🗣️ Dialogue & Deliberation

**deliberation-debate-red-teaming** - Structured debate formats (Oxford, fishbowl, devil's advocate) with red teaming for stress-testing ideas and uncovering blindspots.

**dialectical-mapping-steelmanning** - Present opposing positions in strongest form (steelmanning), map principles using Toulmin model, synthesize via third-way solutions.

**chain-roleplay-debate-synthesis** - Multi-perspective roleplay with expert personas, structured debate, and synthesis across viewpoints for complex decisions.

### 💭 Ideation & Creativity

**brainstorm-diverge-converge** - Divergent ideation (generate many ideas) followed by convergent clustering and prioritization using affinity mapping and dot voting.

**constraint-based-creativity** - Generate creative solutions by systematically applying constraints (remove, combine, extreme, reverse) to force novel thinking.

**morphological-analysis-triz** *(coming soon)* - Systematic innovation using morphological boxes and TRIZ principles.

### 📊 Data & Modeling

**data-schema-knowledge-modeling** - Design data schemas, knowledge graphs, and conceptual models with entity-relationship diagrams and ontology patterns.

**code-data-analysis-scaffolds** - Generate code scaffolds for data analysis, visualization, and statistical testing across Python, R, and SQL.

**metrics-tree** *(coming soon)* - Decompose high-level metrics into actionable sub-metrics.

### 🏗️ Architecture & Design

**adr-architecture** - Document architecture decisions with context, options considered, consequences, and tradeoffs using Architecture Decision Records.

**chain-spec-risk-metrics** - Progressive refinement from specification → risk analysis → success metrics with cross-validation at each stage.

**information-architecture** *(coming soon)* - Organize information for findability and usability.

### 📝 Communication & Documentation

**communication-storytelling** - Craft compelling narratives using story arcs, tension-resolution, concrete details, and audience-specific framing.

**writer** - Transform writing into precise, compelling prose using structured revision (Zinsser, King, Pinker), structural architecture (McPhee), and stickiness techniques (SUCCESs framework).

**one-pager-prd** *(coming soon)* - Create concise one-pagers and product requirement documents.

### 🎯 Estimation & Forecasting

**chain-estimation-decision-storytelling** - Fermi estimation → decision recommendation → compelling narrative for presenting quantitative insights.

**estimation-fermi** - Order-of-magnitude estimation via decomposition (top-down, bottom-up, rate×time), bounding techniques, triangulation, and anchoring for market sizing, resource planning, and feasibility checks.

### 🛡️ Ethics & Evaluation

**ethics-safety-impact** - Systematic ethical assessment using stakeholder mapping, fairness metrics (demographic parity, equalized odds, calibration), harm/benefit analysis with risk scoring, privacy-preserving techniques (differential privacy, k-anonymity), and comprehensive monitoring frameworks for responsible AI and product development.

**evaluation-rubrics** - Design reliable evaluation rubrics with explicit criteria, appropriate scales (1-5, qualitative, binary), observable descriptors, inter-rater reliability measurement (Kappa ≥0.70), calibration techniques, bias mitigation (halo, central tendency), and weighted scoring for consistent quality assessment.

### 🍳 Specialized Domains

**chef-assistant** - Expert culinary guide combining technique, food science, flavor architecture (salt/acid/fat/heat), cultural context, and plating. Covers recipe creation, troubleshooting, menu planning, and cooking methods across global cuisines.

## Installation

### Using with Claude Code

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/claude-skills.git
   cd claude-skills
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

**Production Ready**: 21 skills
- ✓ 19 refined skills from standard collection
- ✓ 1 original skill (writer)
- ✓ 1 custom skill (chef-assistant)

**In Development**: 39 skills remaining from standard collection

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

**Status**: 21 production-ready skills | Active development | Last updated: 2025-11-03

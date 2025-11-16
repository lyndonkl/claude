# File-Type-Specific Extraction Strategies

## Table of Contents
- [Code Files](#code-files)
- [Documentation Files](#documentation-files)
- [Jupyter Notebooks](#jupyter-notebooks)
- [Configuration Files](#configuration-files)
- [Data Files](#data-files)

---

## Code Files

**File types:** `.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, etc.

### Skimming Strategy

```bash
# 1. Get import statements (dependencies and context)
Grep(pattern="^import |^from |^using |^require", output_mode="content")

# 2. Get class/function signatures (API surface)
Grep(pattern="^class |^def |^function |^func |^public |^private", output_mode="content")

# 3. Get documentation
Grep(pattern='""".*"""|///.*|/\*\*.*\*/', output_mode="content")

# 4. Get type definitions (if applicable)
Grep(pattern="^interface |^type |^struct ", output_mode="content")
```

**Quick interpretation:**
- **Imports:** What does this depend on? What domain?
- **Signatures:** What's the API? What are the main abstractions?
- **Docstrings:** What's the intent? What problems does it solve?
- **Types:** What are the core data structures?

### Deep Reading Focus

**Priority targets:**
1. **Main classes/functions** - Core abstractions and logic
2. **Design patterns used** - Architectural decisions (Factory, Builder, Strategy, etc.)
3. **Algorithm implementations** - Novel or complex logic
4. **Error handling patterns** - How failures are managed
5. **Integration points** - How components connect

**Read implementations selectively:**
- Deep-read novel/complex algorithms
- Skim standard CRUD operations
- Skip boilerplate and generated code

### Extract for Skills

| Code Element | Maps to Skill Element |
|--------------|----------------------|
| API patterns | Template structure (how to organize skill outputs) |
| Design decisions | Guardrails (best practices, anti-patterns) |
| Common usage patterns | Workflow steps |
| Error handling | Edge cases in skill |
| Architecture patterns | Skill organization principles |

### Example Extraction

**Source:** Python API client library

**Extract:**
- **Pattern:** "Initialize client → Authenticate → Make requests → Handle responses → Error handling"
- **Skill type:** API integration process skill
- **Workflow:** Setup → Authentication → Request patterns → Response handling → Error handling
- **Template:** API client skeleton code
- **Guardrails:** Rate limiting, retry logic, timeout handling

---

## Documentation Files

**File types:** `.md`, `.txt`, `.rst`, `.adoc`

### Skimming Strategy

```bash
# 1. Get all headers (document structure)
Grep(pattern="^#{1,3} ", output_mode="content")

# 2. Get numbered/bulleted lists (often steps or key points)
Grep(pattern="^\d+\. |^- |^\* ", output_mode="content", -A=1)

# 3. Get emphasized terms (key concepts)
Grep(pattern="\*\*[^*]+\*\*|__[^_]+__|`[^`]+`", output_mode="content")

# 4. Get code blocks (examples and templates)
Grep(pattern="^```", output_mode="content", -A=5)
```

**Quick interpretation:**
- **Headers:** What's the structure? Tutorial? Framework? Reference?
- **Lists:** Are these methodology steps? Quality criteria? Use cases?
- **Emphasized terms:** What are the key concepts and vocabulary?
- **Code blocks:** Are there templates or examples to extract?

### Deep Reading Focus

Use section priority (from [reading-strategies.md](reading-strategies.md)):

**HIGH priority sections:**
- Methodology/Process (how-to steps)
- Decision frameworks (when to do what)
- Quality criteria (what makes it good/bad)
- Templates and formats

**MEDIUM priority:**
- Examples and case studies
- Troubleshooting guides
- FAQs

**LOW/SKIP:**
- Background and history
- Related work and references
- Acknowledgments

### Extract for Skills

| Doc Element | Maps to Skill Element |
|-------------|----------------------|
| Process sections | Workflow steps |
| Decision trees | Conditional logic in workflow |
| Quality checklists | Rubric criteria |
| Templates | resources/template.md (if needed) |
| Examples | resources/examples/ |
| Best practices | Guardrails section |
- Anti-patterns | Don't section in Guardrails |
| Use cases | "When to Use" section |

### Pattern-Based Extraction

**Pattern 1: Tutorial Structure**
```
Introduction → Prerequisites → Step-by-step → Examples → Troubleshooting
↓
Skill: How-to process
Workflow: Prerequisites check → Step 1 → Step 2 → ... → Validation
```

**Pattern 2: Framework Documentation**
```
Overview → Core Concepts → Components → Application → Advanced
↓
Skill: Analysis framework
Workflow: Understand context → Apply framework → Analyze results
```

**Pattern 3: Best Practices Guide**
```
Principles → Do's → Don'ts → Examples → Checklist
↓
Skill: Evaluation/review skill
Workflow: Apply principles → Check do's → Avoid don'ts → Validate with checklist
```

---

## Jupyter Notebooks

**File type:** `.ipynb`

### Skimming Strategy

**Notebooks have two cell types: Markdown (narrative) and Code (execution)**

```bash
# Read tool handles .ipynb natively
# Skim by reading selectively:

# 1. All markdown cells (narrative/explanation)
Read(notebook_path) → Focus on markdown cells

# 2. Function definitions (not full code)
# Look for cells with def/class keywords

# 3. Final outputs (visualizations, results)
# Look at cell outputs at end of sections
```

**Quick interpretation:**
- **Markdown cells:** What's the analysis story? What's being explained?
- **Code cells:** What's the workflow? What transformations are applied?
- **Outputs:** What's the goal? What insights are revealed?

### Deep Reading Focus

**Priority targets:**
1. **Analysis workflow** - The sequence of operations (order matters!)
2. **Data transformations** - How data is cleaned, processed, aggregated
3. **Visualization choices** - What's being plotted and why
4. **Validation/testing steps** - How results are verified
5. **Key insights** - Conclusions drawn from analysis

**Read selectively:**
- Deep-read workflow logic and transformations
- Skim data loading (usually boilerplate)
- Note visualization patterns (what's being compared?)
- Skip package imports and setup

### Extract for Skills

| Notebook Element | Maps to Skill Element |
|------------------|----------------------|
| Analysis workflow order | Workflow steps (sequential) |
| Data transformation patterns | Template code snippets |
| Validation steps | Quality criteria / rubric |
| Visualization choices | Guidance on presenting results |
| Markdown narrative | Skill explanation and context |

### Example Extraction

**Source:** Data analysis notebook

**Extract:**
- **Workflow:** Load data → Clean → Explore → Transform → Analyze → Visualize → Validate → Report
- **Skill type:** Data analysis process skill
- **Template:** Analysis notebook template with standard sections
- **Rubric:** Data quality checks, statistical rigor, visualization clarity

---

## Configuration Files

**File types:** `.json`, `.yaml`, `.toml`, `.xml`, `.ini`

### Skimming Strategy

**For JSON/YAML:**
```bash
# Read first 50 lines to see structure
Read(file_path, limit=50)

# Note:
# - Top-level keys (main configuration sections)
# - Nesting depth (complexity indicator)
# - Comments (if present, explain rationale)
# - Value patterns (are there conventions?)
```

**For XML:**
```bash
# Get root element and main sections
Grep(pattern="^<[^/]", output_mode="content", limit=100)
```

**Quick interpretation:**
- **Top-level structure:** How is configuration organized?
- **Naming conventions:** Are keys descriptive? Is there a pattern?
- **Value types:** Strings? Numbers? Nested objects? Arrays?
- **Comments:** Do they explain the "why"?

### Deep Reading Focus

**Priority targets:**
1. **Configuration patterns** - How are related settings grouped?
2. **Validation rules** - What constraints apply? (min/max, allowed values)
3. **Defaults vs. overrides** - What's required vs. optional?
4. **Integration points** - How do settings affect behavior?
5. **Conventions** - Naming, organization, structure patterns

### Extract for Skills

| Config Element | Maps to Skill Element |
|----------------|----------------------|
| Organizational patterns | Skill structure principles |
| Naming conventions | Terminology standards |
| Validation rules | Quality criteria / rubric |
| Required vs. optional | Workflow decision points |
| Best practice comments | Guardrails |

### Example Extraction

**Source:** Build configuration file (e.g., `.github/workflows/ci.yml`)

**Extract:**
- **Pattern:** "Define triggers → Set environment → Install deps → Run tests → Build → Deploy"
- **Skill type:** CI/CD pipeline design skill
- **Workflow:** Define triggers → Configure environment → Add build steps → Add validation → Configure deployment
- **Guardrails:** Security best practices, caching strategies, conditional execution

---

## Data Files

**File types:** `.csv`, `.tsv`, `.jsonl`, `.parquet`

### Skimming Strategy

**For CSV/TSV:**
```bash
# Read headers + first 5 rows
Read(file_path, limit=6)

# Sample middle section
Read(file_path, offset=500, limit=5)

# Read last 5 rows
Read(file_path, offset=-5)
```

**For JSONL (JSON Lines):**
```bash
# Read first 3 records
Read(file_path, limit=3)

# Sample middle
Read(file_path, offset=100, limit=2)
```

**Quick interpretation:**
- **Columns/fields:** What dimensions does the data have?
- **Data types:** Numeric, categorical, text, dates?
- **Completeness:** Missing values? Sparse data?
- **Patterns:** Are there trends, categories, or structures?

### Deep Reading Focus

**Priority targets:**
1. **Data schema** - Column names, types, relationships
2. **Data quality patterns** - Missing data, outliers, inconsistencies
3. **Transformation needs** - What cleaning or processing is implied?
4. **Analysis opportunities** - What questions can this data answer?
5. **Sampling strategy** - How to represent the full dataset

**Don't read entire dataset** - sample strategically.

### Extract for Skills

| Data Element | Maps to Skill Element |
|--------------|----------------------|
| Schema/structure | Template for data organization |
| Quality issues found | Quality criteria for similar data |
| Transformation patterns | Workflow steps (cleaning, processing) |
| Analysis patterns | Analytical approaches to teach |

### Example Extraction

**Source:** Customer transaction CSV

**Extract:**
- **Pattern:** "Load → Validate schema → Clean → Aggregate → Analyze → Visualize"
- **Skill type:** Transactional data analysis skill
- **Workflow:** Schema validation → Data cleaning → Feature engineering → Analysis → Reporting
- **Quality criteria:** Completeness, consistency, timeliness, accuracy

---

## Quick Reference Table

| File Type | Skim Focus | Deep Read Focus | Typical Skill Type |
|-----------|------------|----------------|-------------------|
| **Code** | Imports, signatures, docstrings | Patterns, algorithms, architecture | Process, API pattern |
| **Docs** | Headers, lists, emphasized terms | Methodology sections, quality criteria | Framework, how-to |
| **Notebooks** | Markdown cells, workflow order | Transformations, validation steps | Analysis process |
| **Config** | Top-level keys, structure, comments | Patterns, validation rules, conventions | Configuration pattern, standards |
| **Data** | Schema, sample rows, data types | Quality patterns, transformation needs | Data process, quality framework |

---

## Cross-File-Type Principles

**Regardless of file type:**

1. **Skim first** - Understand before committing to deep read
2. **Look for patterns** - Repeated structures often indicate methodology
3. **Focus on "why"** - Comments and explanations reveal intent
4. **Extract transferable concepts** - Abstract from specific domain
5. **Note decision points** - "If X then Y" logic is valuable
6. **Identify quality signals** - What makes it good vs. bad?
7. **Skip boilerplate** - Generated code, standard imports, etc.

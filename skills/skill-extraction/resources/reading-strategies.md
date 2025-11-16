# Reading Strategies for Skill Extraction

## Table of Contents
- [Overview](#overview)
- [Inspectional Reading (Skimming)](#inspectional-reading-skimming)
- [Analytical Reading (Deep Reading)](#analytical-reading-deep-reading)
- [Multi-File Analysis](#multi-file-analysis)

---

## Overview

Two complementary approaches adapted from Adler's framework:

**Inspectional Reading:** Understand structure and content type WITHOUT reading everything (prevents context dilution)

**Analytical Reading:** Systematic deep reading in manageable chunks (extracts components while maintaining context efficiency)

---

## Inspectional Reading (Skimming)

### Purpose
Get maximum structural understanding with minimum token usage. Build mental model before committing to deep reading.

### Technique 1: Boundary Reading

**For all file types:**

```bash
# Read first 30-50 lines
Read(file_path, offset=0, limit=50)

# Read last 20-30 lines
Read(file_path, offset=-30)
```

**What you get:**
- **First lines:** Purpose, intro, context, imports, headers
- **Last lines:** Conclusions, summary, main takeaways, exports

**Skip the middle entirely on first pass.**

### Technique 2: Structural Extraction

**Read structure only, not content:**

#### For Code Files:
```bash
# Get import statements (dependencies)
Grep(pattern="^import |^from ", output_mode="content")

# Get class/function signatures (API surface)
Grep(pattern="^class |^def |^function ", output_mode="content")

# Get docstrings (documentation)
Grep(pattern='""".*"""', output_mode="content")
```

#### For Markdown/Docs:
```bash
# Get all headers (structure)
Grep(pattern="^#{1,3} ", output_mode="content")

# Get numbered lists (often methodology steps)
Grep(pattern="^\d+\. ", output_mode="content")

# Get bold terms (key concepts)
Grep(pattern="\*\*[^*]+\*\*", output_mode="content")
```

#### For JSON/YAML:
- Read top-level keys only (skip values initially)
- Read comments (rationale)
- Note structure depth and organization

#### For CSV/Data:
- Read headers + first 3 rows only
- Note column count and types
- Sample middle and end rows if needed

### Technique 3: Progressive Sampling

**For large files (>500 lines):**

Sample at regular intervals:
- **0%** (lines 1-30): Introduction
- **20%** (sample 30 lines): Early content
- **40%** (sample 30 lines): Mid-early content
- **60%** (sample 30 lines): Mid-late content
- **80%** (sample 30 lines): Late content
- **100%** (last 30 lines): Conclusion

**Build hypothesis:**
- What type of methodology is this?
- What are the major sections?
- What's the complexity level?
- Which sections likely contain extractable content?

### Structural Pattern Recognition

Recognize common patterns to predict content:

| Pattern | Structure | Indicates | Extraction Focus |
|---------|-----------|-----------|------------------|
| Tutorial | Intro → Concepts → Steps → Examples → Exercises | How-to methodology | Steps section |
| Framework | Theory → Components → Relationships → Application | Analysis framework | Components + Application |
| Reference | Index/TOC → Sections (organized) → Details | Lookup tool | Organizational logic |
| Research | Background → Method → Validation → Results | Research process | Method section |
| Code Library | Imports → Classes → Functions → Examples | API/Pattern | Classes + Patterns |

**Use patterns to:**
- Predict what sections contain
- Decide which to deep-read
- Anticipate final skill structure

### Output of Skimming Phase

Copy this assessment checklist and track your progress:

```
Skim Assessment:
- [ ] Identified file type and pattern
- [ ] Extracted structure (sections/classes/functions)
- [ ] Determined main theme
- [ ] Assessed skill-worthiness
- [ ] Identified sections to deep-read
```

Create temporary `skim-notes.md`:

```markdown
## File Info
- Type: [code/docs/notebook/config]
- Size: [lines]
- Pattern: [tutorial/framework/reference/etc]

## Structure
[List of main sections/classes/functions]

## Main Theme
[1-2 sentences on what this is about]

## Skill-Worthy?
- [ ] Contains reusable process (3+ steps)
- [ ] Solves recurring problem
- [ ] Generally applicable
- [ ] Distinct from existing skills

**Decision:** [Continue to deep read | Stop, not skill-worthy]

## Sections to Deep-Read
1. [Section name] - [Why]
2. [Section name] - [Why]
```

---

## Analytical Reading (Deep Reading)

### Purpose
Extract all necessary components systematically while managing context efficiently.

### Technique 1: Section-Based Chunking

Copy this section reading checklist and track your progress:

```
Section-Based Reading:
- [ ] Identify all section boundaries from skim
- [ ] Prioritize sections (HIGH/MEDIUM/LOW)
- [ ] Read HIGH priority sections
- [ ] Extract and summarize each section
- [ ] Read MEDIUM priority sections (targeted)
- [ ] Skip LOW priority sections
```

**Process:**

1. **From skim:** Identify all section boundaries
2. **Prioritize sections** (see [component-extraction.md](component-extraction.md) for priority matrix)
3. **Read each HIGH priority section:**
   - Read section content
   - Extract key components
   - Summarize in 5-10 bullets
   - Write to `extraction-notes.md`
   - **Clear section from context**
4. **Read MEDIUM priority sections** (targeted)
5. **Skip LOW priority sections**

**Example:**
```bash
# Read Section 1 (lines 50-150)
Read(file_path, offset=50, limit=100)
# Extract → Summarize → Write notes → Continue

# Read Section 2 (lines 150-280)
Read(file_path, offset=150, limit=130)
# Extract → Summarize → Write notes → Continue
```

### Technique 2: Windowing for Large Files

**For files >1000 lines:**

Copy this windowing checklist and track your progress:

```
Windowing Process:
- [ ] Determine window size (typically 200 lines)
- [ ] Read Window 1
- [ ] Extract and summarize Window 1
- [ ] Read Window 2 (with overlap)
- [ ] Extract and summarize Window 2
- [ ] Continue for all windows
- [ ] Synthesize from all window notes
```

Use overlapping windows to maintain context continuity:

```
Window size: 200 lines
Overlap: 20 lines (10%)

Window 1: Lines 1-200
Window 2: Lines 180-380 (20-line overlap with Window 1)
Window 3: Lines 360-560 (20-line overlap with Window 2)
Continue...
```

**Per-Window Process:**
1. Read window content
2. Extract: key terms, propositions, methodology steps, examples
3. Summarize in 5-10 bullets
4. Write summary to `extraction-notes.md`
5. **Clear window from active context**

**Why overlap?**
- Catches concepts that span boundaries
- Maintains logical continuity
- Prevents missing connections

**Final step:** Read compressed `extraction-notes.md` (much smaller than original) and synthesize

### Technique 3: Targeted Reading

**Most efficient approach:**

After skim phase, you know which sections matter:

```markdown
## Sections to Read (from skim)
1. Methodology (lines 200-450) - HIGH priority
2. Examples (lines 600-750) - MEDIUM priority
3. Quality criteria (lines 800-900) - HIGH priority

## Sections to Skip
- Background (lines 1-199)
- Related work (lines 900-1100)
```

**Read ONLY HIGH priority sections deeply.**

For MEDIUM priority: skim or read selectively.

For LOW priority: skip entirely.

**This focuses your tokens on extractable content.**

### Section Priority Guidelines

| Section Type | Priority | Reading Depth | Reason |
|--------------|----------|---------------|---------|
| Methodology/Process | **HIGH** | Deep, complete | Core workflow extraction |
| Implementation Details | **HIGH** | Deep, complete | Template content |
| Quality Criteria | **HIGH** | Deep, complete | Rubric creation |
| Decision Points | **HIGH** | Deep, complete | Workflow logic |
| Examples/Case Studies | **MEDIUM** | Skim, selective | Reference material |
| Troubleshooting | **MEDIUM** | Targeted read | Guardrails |
| Background/Theory | **LOW** | Skim quickly | Context only |
| Related Work/History | **LOW** | Skip entirely | Not needed |
| Appendices | **LOW** | Skip entirely | Rarely relevant |

### Output of Deep Reading Phase

`extraction-notes.md` should contain:

```markdown
## Core Components Extracted

### Purpose & Problem
[What this solves, why it's valuable]

### Methodology Steps
1. [Step 1]: [Description, inputs, outputs]
2. [Step 2]: [Description, inputs, outputs]
...

### Key Terms & Concepts
- **Term 1**: Definition + importance
- **Term 2**: Definition + importance

### Decision Points
- **Decision 1**: When to choose A vs B [conditions]

### Quality Criteria
- Good indicator 1
- Good indicator 2
- Poor indicator 1

### Use Cases
- Context 1 → Application
- Context 2 → Application

### Guardrails
**Do:** [Best practices]
**Don't:** [Anti-patterns]
```

---

## Multi-File Analysis

### When You Have Multiple Related Files

Copy this multi-file analysis checklist and track your progress:

```
Multi-File Analysis:
- [ ] Phase 1: Discover all related files
- [ ] Phase 2: Map dependencies and reading order
- [ ] Phase 3: Skim all files
- [ ] Phase 4: Deep-read core file
- [ ] Phase 5: Targeted-read supporting files
- [ ] Phase 6: Synthesize across sources
```

#### Phase 1: Discovery

```bash
# Find all related files
Glob(pattern="**/*methodology*")
Glob(pattern="**/*framework*")
Glob(pattern="**/*guide*")
Glob(pattern="**/*template*")
```

#### Phase 2: Dependency Mapping

Create `file-map.md`:

```markdown
## Files Found

1. **main-methodology.md** (800 lines)
   - Type: Core framework doc
   - Contains: Overview, main process, principles
   - Depends on: None

2. **implementation-guide.md** (400 lines)
   - Type: Supporting guide
   - Contains: Step-by-step implementation
   - Depends on: main-methodology.md

3. **examples.md** (600 lines)
   - Type: Case studies
   - Contains: Worked examples
   - Depends on: main-methodology.md

## Reading Order

1. Skim all files (understand scope)
2. Deep-read main-methodology.md (extract core framework)
3. Targeted-read implementation-guide.md (extract templates/steps)
4. Skim examples.md (identify patterns)
5. Synthesize across all sources
```

#### Phase 3: Hierarchical Reading

**Strategy:**
1. **Skim all files** → Understand full scope and relationships
2. **Identify core file** → Usually has the main methodology
3. **Deep-read core file** → Extract primary framework
4. **Targeted-read supporting files** → Extract templates, examples, details
5. **Synthesize** → Combine insights into single skill

**Key principle:** Core file drives structure; supporting files enrich it.

---

## Quick Reference

**Inspectional (Skim):**
- Boundary reading (first/last N lines)
- Structural extraction (headers/signatures only)
- Progressive sampling (for large files)
- Pattern recognition

**Analytical (Deep):**
- Section-based chunking
- Windowing (for very large files)
- Targeted reading (priority-based)

**Multi-File:**
- Discovery → Dependency mapping → Hierarchical reading

**Always:**
- Write notes externally (compress context)
- Clear raw content after summarizing
- Skip irrelevant sections entirely

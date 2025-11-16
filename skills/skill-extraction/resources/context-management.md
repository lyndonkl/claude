# Context Management for Large File Extraction

## Table of Contents
- [The Context Problem](#the-context-problem)
- [Core Strategies](#core-strategies)
- [External Notes Pattern](#external-notes-pattern)
- [Layered Summarization](#layered-summarization)
- [Progressive Refinement](#progressive-refinement)

---

## The Context Problem

**Issue:** When an LLM reads an entire large file at once:
- Important details get "diluted" in the sea of content
- Model treats all content equally (can't distinguish signal from noise)
- Context window fills with potentially irrelevant information
- Reduces space for reasoning and synthesis

**Solution:** Strategic reading and compression techniques that maintain focus while extracting comprehensively.

---

## Core Strategies

### Strategy 1: Never Read Entire Large Files

**Guideline:** If file > 500 lines, don't read it all at once.

**Instead:**
1. **Skim** using boundary reading and sampling (see [reading-strategies.md](reading-strategies.md))
2. **Identify** which sections contain extractable content
3. **Read** only those sections, one at a time
4. **Skip** irrelevant sections entirely

**Example:**
```
File: 1200 lines total

After skim:
- Lines 1-100: Introduction (LOW priority → skip)
- Lines 101-350: Methodology (HIGH priority → read)
- Lines 351-800: Examples (MEDIUM priority → skim)
- Lines 801-1000: Background (LOW priority → skip)
- Lines 1001-1200: References (LOW priority → skip)

Result: Read ~250 lines instead of 1200 (80% reduction)
```

### Strategy 2: External Notes Files

**Pattern:** Write extracted insights to external files, clear raw content from context

**Process:**
```bash
# Read Section 1 (200 lines)
Read(file_path, offset=100, limit=200)

# Extract components → Write to external notes
Write("temp/section-1-notes.md", extracted_summary)

# Clear Section 1 from active context by moving on

# Read Section 2 (150 lines)
Read(file_path, offset=300, limit=150)

# Extract components → Write to external notes
Write("temp/section-2-notes.md", extracted_summary)

# At end: Read all notes files (much smaller than original)
Read("temp/section-1-notes.md")  # ~30 lines
Read("temp/section-2-notes.md")  # ~25 lines

# Now synthesize from compressed notes
```

**Key principle:** Raw content is temporary. Compressed insights persist.

### Strategy 3: Immediate Summarization

**Rule:** After reading any chunk, summarize IMMEDIATELY before reading next chunk.

**Process:**
1. Read chunk (section, window, or targeted content)
2. Extract relevant components (see [component-extraction.md](component-extraction.md))
3. Summarize in 5-10 bullet points
4. Write summary to notes file
5. **Clear chunk from mental context** (move to next)

**Benefits:**
- Compresses 200 lines → 10 bullets
- Forces prioritization (what's truly important?)
- Maintains focus on extractable content

### Strategy 4: Progressive Disclosure in Extraction

**Principle:** Don't load all information upfront. Bring in details only when needed.

**Pattern:**
```
Phase 1: Skim → Build mental model (50-100 lines read)
Phase 2: Extract high-level structure (read TOC, headers)
Phase 3: Deep-read HIGH priority sections only (200-400 lines)
Phase 4: Targeted-read MEDIUM priority if needed (100-200 lines)
Phase 5: Synthesize from notes (~100 lines of compressed notes)

Total: ~500-800 lines read instead of entire 2000-line file
```

---

## External Notes Pattern

### Template: Section Notes

After reading each section, write to `temp/section-N-notes.md`:

```markdown
## Section: [Name]
**Location:** Lines [X-Y]
**Priority:** [HIGH/MEDIUM/LOW]

### Key Points
- [Point 1]
- [Point 2]
- [Point 3]

### Extractable Components
**Methodology Steps:**
1. [Step if found]

**Key Terms:**
- [Term]: [Definition]

**Decision Points:**
- [Decision if found]

**Quality Criteria:**
- [Criteria if found]

**Guardrails:**
- Do: [If found]
- Don't: [If found]

### Next Actions
- [ ] Deep-read subsection X (if needed)
- [ ] Skip to Section N+1
```

### Synthesis Pattern

After all sections read, create `synthesis-notes.md`:

```markdown
# Synthesis: [Skill Name]

## Compiled from:
- section-1-notes.md (Methodology)
- section-3-notes.md (Examples)
- section-5-notes.md (Quality Criteria)

## Overall Methodology
[Combined and deduplicated steps from all sections]

## Complete Component Extraction
[Merge all extractable components]

## Skill Structure Mapping
[Map to SKILL.md, resources, rubric]
```

**This synthesis file is what you use to generate the skill** (not the original file).

---

## Layered Summarization

### Technique: Multiple Compression Passes

Copy this layered summarization checklist and track your progress:

```
Layered Summarization:
- [ ] Pass 1: Extract raw components
- [ ] Pass 2: Summarize to key points
- [ ] Pass 3: Distill to essentials
- [ ] Pass 4: Map to skill structure
```

**Process:**

**Pass 1: Extract Raw Components** → 1000 lines
- Read each relevant section
- Extract all potentially useful components
- Write to `extraction-raw.md`
- Result: Comprehensive but verbose

**Pass 2: Summarize to Key Points** → 300 lines
- Review `extraction-raw.md`
- Remove redundancy and irrelevant details
- Keep only components needed for skill
- Write to `extraction-summary.md`
- Result: Concise and focused

**Pass 3: Distill to Essentials** → 100 lines
- Review `extraction-summary.md`
- Identify absolutely essential components
- Abstract from domain specifics
- Write to `extraction-essentials.md`
- Result: Minimal, actionable

**Pass 4: Map to Skill Structure** → 50 lines
- Review `extraction-essentials.md`
- Map each component to skill file location
- Create generation plan
- Result: Ready to generate skill files

**Each pass compresses further, saving tokens and maintaining focus.**

---

## Progressive Refinement

### Technique: Funnel from Broad to Narrow

**Visualization:**
```
        ╔═══════════════════════════╗
        ║   Original File (2000)    ║  All content
        ╚═══════════════════════════╝
                    ↓ Skim
        ╔═══════════════════════════╗
        ║  Relevant Sections (800)  ║  Filter irrelevant
        ╚═══════════════════════════╝
                    ↓ Deep Read
        ╔═══════════════════════════╗
        ║ Extracted Components (300)║  Extract systematically
        ╚═══════════════════════════╝
                    ↓ Summarize
        ╔═══════════════════════════╗
        ║   Key Insights (100)      ║  Remove redundancy
        ╚═══════════════════════════╝
                    ↓ Abstract
        ╔═══════════════════════════╗
        ║ Skill Components (50)     ║  Map to structure
        ╚═══════════════════════════╝
                    ↓ Generate
        ╔═══════════════════════════╗
        ║ Skill Files (SKILL.md +)  ║  Final output
        ╚═══════════════════════════╝
```

**Each stage narrows focus and compresses information.**

### Refinement Questions

**After each compression pass, ask:**

1. **Is this relevant to skill creation?**
   - If NO → Remove
   - If MAYBE → Mark for review
   - If YES → Keep

2. **Is this actionable/extractable?**
   - Can't extract → Remove
   - Can extract → Keep and structure

3. **Is this domain-specific or generalizable?**
   - Too specific → Abstract or remove
   - Already general → Keep as-is

4. **Is this redundant with existing content?**
   - Duplicate → Remove
   - Unique → Keep

---

## Windowing for Very Large Files

### When to Use

Files > 1000 lines that require comprehensive reading (can't skip large sections).

### Technique

Copy this windowing checklist and track your progress:

```
Windowing for Large Files:
- [ ] Determine window size and overlap
- [ ] Read Window 1
- [ ] Extract and write notes for Window 1
- [ ] Read Window 2 (with overlap)
- [ ] Extract and write notes for Window 2
- [ ] Continue for all windows
- [ ] Read all window notes
- [ ] Synthesize from compressed notes
```

**Overlapping windows maintain context continuity:**

```
File: 2000 lines
Window size: 200 lines
Overlap: 20 lines (10%)

Window 1: Lines 1-200
  → Extract → Summarize → Write notes (section-1.md)

Window 2: Lines 180-380 (20-line overlap with W1)
  → Extract → Summarize → Write notes (section-2.md)

Window 3: Lines 360-560 (20-line overlap with W2)
  → Extract → Summarize → Write notes (section-3.md)

Continue for 10 windows total...

Final: Read 10 note files (~300 lines combined) instead of 2000-line file
```

**Why overlap?**
- Concepts spanning boundaries aren't missed
- Maintains logical flow between windows
- Catches cross-references

**Per-window budget:**
- Read: 200 lines
- Extract: ~50 lines of components
- Summarize: ~30 lines of notes
- Clear raw window from context

**Result:** 2000 lines → 300 lines of compressed notes

---

## Context Budget Management

### Token Budget Awareness

**Typical file sizes in tokens:**
- 100 lines ≈ 400-500 tokens
- 500 lines ≈ 2,000-2,500 tokens
- 1000 lines ≈ 4,000-5,000 tokens
- 2000 lines ≈ 8,000-10,000 tokens

**Context window limits:**
- Keep active context < 20,000 tokens
- Reserve space for reasoning (5,000+ tokens)
- External notes are "off-budget" until read

### Budget Allocation Strategy

**For a 2000-line file extraction:**

| Phase | Active Context | Notes |
|-------|---------------|-------|
| Skim | 500 tokens | Boundary read + samples |
| Section 1 read | 2,000 tokens | 200-line section |
| Section 1 summarize | 500 tokens | Compressed notes |
| **Clear Section 1** | **→ 0 tokens** | Wrote to external file |
| Section 2 read | 2,000 tokens | Next section |
| Section 2 summarize | 500 tokens | Compressed notes |
| **Clear Section 2** | **→ 0 tokens** | Wrote to external file |
| Synthesis | 2,000 tokens | Read all note files |
| Generation | 3,000 tokens | Create skill files |

**Peak context: ~3,000 tokens (well within budget)**

---

## Practical Example

### Scenario: Extracting from 1500-line methodology doc

**Step 1: Skim (100 lines read)**
```bash
Read(file, limit=50)  # First 50 lines
Grep(pattern="^## ", output_mode="content")  # All headers
Read(file, offset=-30)  # Last 30 lines
```

Result:
- 10 main sections identified
- Sections 3, 5, 7 contain methodology (HIGH priority)
- Sections 2, 6 contain examples (MEDIUM priority)
- Sections 1, 4, 8, 9, 10 are background (LOW priority → skip)

**Step 2: Deep-read HIGH priority sections (400 lines total)**
```bash
# Section 3 (lines 200-350)
Read(file, offset=200, limit=150)
# Extract → Write to temp/section-3.md (20 lines)

# Section 5 (lines 500-650)
Read(file, offset=500, limit=150)
# Extract → Write to temp/section-5.md (25 lines)

# Section 7 (lines 900-1000)
Read(file, offset=900, limit=100)
# Extract → Write to temp/section-7.md (15 lines)
```

**Step 3: Targeted-read MEDIUM priority (200 lines sampled)**
```bash
# Section 2 examples (skim, sample 50 lines)
Read(file, offset=100, limit=50)
# Note patterns → Write to temp/section-2.md (10 lines)

# Section 6 examples (skim, sample 50 lines)
Read(file, offset=700, limit=50)
# Note patterns → Write to temp/section-6.md (10 lines)
```

**Step 4: Synthesize from notes (80 lines)**
```bash
Read("temp/section-3.md")
Read("temp/section-5.md")
Read("temp/section-7.md")
Read("temp/section-2.md")
Read("temp/section-6.md")
# Combine → synthesis.md (50 lines)
```

**Step 5: Generate skill from synthesis**
```bash
Read("temp/synthesis.md")
# Map to skill structure
# Create SKILL.md, resources, rubric
```

**Total lines read: ~780 lines instead of 1500 (48% reduction)**
**Peak active context: ~100 lines (synthesis phase)**

---

## Quick Reference

**Core Principles:**
1. Never read entire large files
2. Write to external notes immediately
3. Summarize before moving to next section
4. Progressive compression (multiple passes)
5. Clear raw content, keep summaries
6. Read compressed notes for synthesis

**Compression Ratios:**
- Single section: 200 lines → 20 lines (10:1)
- Multiple sections: 800 lines → 80 lines (10:1)
- Full file: 2000 lines → 100 lines final (20:1)

**Token Budget:**
- Reserve 5,000+ tokens for reasoning
- Keep active reading < 3,000 tokens per chunk
- External notes are "off-budget" until loaded

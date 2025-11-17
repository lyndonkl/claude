# Inspectional Reading

This resource supports **Step 0** and **Step 1** of the Skill Creator workflow.

**Step 0 - Input files:** None (initialization step)
**Step 0 - Output files:** `$SESSION_DIR/global-context.md` (created)

**Step 1 - Input files:** `$SESSION_DIR/global-context.md`, `$SOURCE_DOC` (skim only)
**Step 1 - Output files:** `$SESSION_DIR/step-1-output.md`, updates `global-context.md`

---

## Session Initialization

### WHY File-Based Workflow Matters

Working with documents for skill extraction can flood context with:
- Entire document content (potentially thousands of lines)
- Extracted components accumulating across steps
- Analysis and synthesis notes

**Solution:** Write outputs to files after each step, read only what's needed for current step.

**Mental model:** Each step is a pipeline stage that reads inputs, processes, and writes outputs. Next stage picks up from there.

### WHAT to Set Up

#### Create Session Directory

```bash
# Create timestamped session directory
SESSION_DIR="/tmp/skill-extraction-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$SESSION_DIR"
echo "Session workspace: $SESSION_DIR"
```

#### Initialize Global Context

```bash
# Create global context file
cat > "$SESSION_DIR/global-context.md" << 'EOF'
# Skill Extraction Global Context

**Source document:** [path will be added in step 1]
**Session started:** $(date)
**Target skill name:** [to be determined]

## Key Information Across Steps

[This file is updated by each step with critical information needed by subsequent steps]

EOF
```

#### Set Document Path

Store the source document path for reference:

```bash
# Set this to your actual document path
SOURCE_DOC="[user-provided-path]"
echo "**Source document:** $SOURCE_DOC" >> "$SESSION_DIR/global-context.md"
```

**You're now ready for Step 1.**

---

## Why Systematic Skimming

### WHY This Matters

Systematic skimming activates the right reading approach before deep engagement. Without it:
- You waste time reading documents that don't contain extractable skills
- You miss the overall structure, making later extraction harder
- You can't estimate the effort required or plan the approach
- You don't know what type of content you're dealing with

**Mental model:** Think of this as reconnaissance before a mission. You need to know the terrain before committing resources.

**Key insight from Adler:** Inspectional reading answers "Is this book worth reading carefully?" and "What kind of book is this?" - both critical before investing analytical reading effort.

### WHAT to Do

Perform the following skimming activities in order:

#### 1. Check Document Metadata & Read Title/Introduction

Get file info, note size and type. Read title, introduction/abstract completely to extract stated purpose and intended audience.

#### 2. Examine TOC/Structure

Read TOC if exists. If not, scan headers to create quick outline. Note major sections, sequence, and depth.

#### 3. Scan Key Elements & End Material

Read first paragraph of major sections, summaries, conclusion/final pages. Note diagrams/tables/callouts. **Time: 10-30 minutes total depending on document size.**

---

## Why Document Type Matters

### WHY Classification Is Essential

Document type determines:
- **Reading strategy:** Code requires different analysis than prose
- **Extraction targets:** Methodologies yield processes; frameworks yield decision structures
- **Skill structure:** Some documents map to linear workflows; others to contextual frameworks
- **Expected completeness:** Research papers have gaps; guidebooks are comprehensive

**Mental model:** You wouldn't use a roadmap the same way you use a cookbook. Different document types serve different purposes and need different extraction approaches.

### WHAT Document Types Exist

After skimming, classify the document into one of these types:

#### Type 1: Methodology / Process Guide

**Characteristics:**
- Sequential steps or phases
- Clear "first do X, then Y" structure
- Process diagrams or flowcharts
- Decision points along a path

**Examples:**
- "How to conduct user research"
- "The scientific method"
- "Agile development process"

**Extraction focus:** Steps, sequence, inputs/outputs, decision criteria

**Skill structure:** Linear workflow with numbered steps

---

#### Type 2: Framework / Mental Model

**Characteristics:**
- Dimensions, axes, or categories
- Principles or heuristics
- Matrices or quadrants
- Conceptual models

**Examples:**
- "Eisenhower decision matrix"
- "Design thinking principles"
- "SWOT analysis framework"

**Extraction focus:** Dimensions, categories, when to apply each, interpretation guide

**Skill structure:** Framework application with decision logic

---

#### Type 3: Tool / Template

**Characteristics:**
- Fill-in-the-blank sections
- Templates or formats
- Checklists
- Structured forms

**Examples:**
- "Business model canvas"
- "User story template"
- "Code review checklist"

**Extraction focus:** Template structure, what goes in each section, usage guidelines

**Skill structure:** Template with completion instructions

---

#### Type 4: Theoretical / Conceptual

**Characteristics:**
- Explains "why" more than "how"
- Research findings
- Principles without procedures
- Conceptual relationships

**Examples:**
- "Cognitive load theory"
- "Growth mindset research"
- "System dynamics principles"

**Extraction focus:** Core concepts, implications, how to apply theory in practice

**Skill structure:** Concept → Application mapping (requires synthesis step)

**Note:** This type needs extra work in Step 4 (Synthesis) to make actionable

---

#### Type 5: Reference / Catalog

**Characteristics:**
- Lists of items, patterns, or examples
- Encyclopedia-like structure
- Lookup-oriented
- No overarching process

**Examples:**
- "Design patterns catalog"
- "Cognitive biases list"
- "API reference"

**Skill-worthiness:** **Usually NOT skill-worthy** - these are references, not methodologies

**Exception:** If the document includes *when/how to choose* among options, extract that decision framework

---

#### Type 6: Hybrid

**Characteristics:**
- Combines multiple types above
- Has both framework and process
- Includes theory and application

**Approach:** Identify which parts map to which types, extract each accordingly

**Example:** "Design thinking" combines a framework (mindsets) with a process (steps) and tools (templates)

---

### WHAT to Decide

Based on document type classification, answer:

1. **Primary type:** Which category best fits this document?
2. **Secondary aspects:** Does it have elements of other types?
3. **Extraction strategy:** What should we focus on extracting?
4. **Skill structure:** What will the resulting skill look like?

**Present to user:** "I've classified this as a [TYPE] document. This means we'll focus on extracting [EXTRACTION TARGETS] and structure the skill as [SKILL STRUCTURE]. Does this match your understanding?"

---

## Why Skill-Worthiness Check

### WHY Not Everything Is Skill-Worthy

Creating a skill has overhead:
- Time to extract, structure, and validate
- Maintenance burden (keeping it updated)
- Cognitive load (another skill to remember exists)

**Only create skills for material that is:**
- Reusable across multiple contexts
- Teachable (can be articulated as steps or principles)
- Non-obvious (provides value beyond common sense)
- Complete enough to be actionable

**Anti-pattern:** Creating skills for one-time information or simple facts that don't need systematic application.

### WHAT Makes Content Skill-Worthy

Evaluate against these criteria:

#### Criterion 1: Teachability

**Question:** Can this be taught as a process, framework, or set of principles?

**Strong signals:**
- Clear steps or stages
- Decision rules or criteria
- Repeatable patterns
- Structured approach

**Weak signals:**
- Purely informational (facts without process)
- Contextual knowledge (only applies in one situation)
- Opinion without methodology
- Single example without generalization

**Decision:** If you can't articulate "Here's how to do this" or "Here's how to think about this," it's not teachable.

---

#### Criterion 2: Generalizability

**Question:** Can this be applied across multiple situations or domains?

**Strong signals:**
- Document shows examples from different domains
- Principles are abstract enough to transfer
- Method doesn't depend on specific tools/context
- Core process remains stable across use cases

**Weak signals:**
- Highly specific to one tool or platform
- Only works in one narrow context
- Requires specific resources you won't have
- Examples are all from the same narrow domain

**Decision:** If it only works in one exact scenario, it's probably not worth a skill.

---

#### Criterion 3: Recurring Problem

**Question:** Is this solving a problem that comes up repeatedly?

**Strong signals:**
- Document addresses common pain points
- You can imagine needing this multiple times
- Problem exists across projects/contexts
- It's not a one-time decision

**Weak signals:**
- One-off decision or task
- Historical information
- Situational advice for rare scenarios

**Decision:** If you'll only use it once, save it as a note instead of a skill.

---

#### Criterion 4: Actionability

**Question:** Does this provide enough detail to actually do something?

**Strong signals:**
- Concrete steps or methods
- Clear decision criteria
- Examples showing application
- Guidance on handling edge cases

**Weak signals:**
- High-level philosophy only
- Vague principles without application
- Aspirational goals without methods
- "You should do X" without explaining how

**Decision:** If the document is all theory with no application guidance, flag this - you'll need to create the application in Step 4.

---

#### Criterion 5: Completeness

**Question:** Is there enough material to create a useful skill?

**Strong signals:**
- Multiple sections or components
- Depth beyond surface level
- Covers multiple aspects (when, how, why)
- Includes examples or case studies

**Weak signals:**
- Single tip or trick
- One-paragraph advice
- Incomplete methodology
- Missing critical steps

**Decision:** If the document is too sparse, it might be better as a reference note than a full skill.

---

### WHAT to Do: Skill-Worthiness Decision

Score the document on each criterion (1-5 scale):
- **5:** Strongly meets criterion
- **4:** Meets criterion well
- **3:** Partially meets criterion
- **2:** Weakly meets criterion
- **1:** Doesn't meet criterion

**Threshold:** If average score ≥ 3.5, proceed with skill extraction

**If score < 3.5, present options to user:**

**Option A: Proceed with Modifications**
- "This document is borderline skill-worthy. We can proceed, but we'll need to supplement it with additional application guidance in Step 4. Should we continue?"

**Option B: Save as Reference**
- "This might be better saved as a reference document rather than a full skill. Would you prefer to extract key insights into a note instead?"

**Option C: Defer Until More Material Available**
- "This document alone isn't sufficient for a skill. Do you have additional related documents we could synthesize together?"

**Present to user:**
```
Skill-Worthiness Assessment:
- Teachability: [score]/5 - [brief rationale]
- Generalizability: [score]/5 - [brief rationale]
- Recurring Problem: [score]/5 - [brief rationale]
- Actionability: [score]/5 - [brief rationale]
- Completeness: [score]/5 - [brief rationale]

Average: [X.X]/5

Recommendation: [Proceed / Modify / Alternative approach]

What would you like to do?
```

---

## Write Step 1 Output

After completing inspectional reading and getting user approval, write results to file:

```bash
# Write Step 1 output
cat > "$SESSION_DIR/step-1-output.md" << 'EOF'
# Step 1: Inspectional Reading Output

## Document Classification

**Type:** [methodology/framework/tool/theory/reference/hybrid]
**Structure:** [clear sections / continuous flow / mixed]
**Page/line count:** [X]

## Document Overview

**Main topic:** [1-2 sentence summary]
**Key sections identified:**
1. [Section 1]
2. [Section 2]
3. [Section 3]
...

## Skill-Worthiness Assessment

**Scores:**
- Teachability: [X]/5 - [rationale]
- Generalizability: [X]/5 - [rationale]
- Recurring Problem: [X]/5 - [rationale]
- Actionability: [X]/5 - [rationale]
- Completeness: [X]/5 - [rationale]

**Average:** [X.X]/5
**Decision:** [Proceed / Modify / Alternative]

## User Approval

**Status:** [Approved / Rejected / Modified]
**User notes:** [Any specific guidance from user]

EOF
```

**Update global context:**

```bash
# Add key info to global context
cat >> "$SESSION_DIR/global-context.md" << 'EOF'

## Step 1 Complete

**Document type:** [type]
**Skill-worthiness:** [average score]/5
**Approved to proceed:** [Yes/No]

EOF
```

**Next step:** Proceed to Step 2 (Structural Analysis) which will read `global-context.md` + `step-1-output.md`.

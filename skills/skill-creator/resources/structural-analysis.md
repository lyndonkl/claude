# Structural Analysis

This resource supports **Step 2** of the Skill Creator workflow.

**Input files:** `$SESSION_DIR/global-context.md`, `$SESSION_DIR/step-1-output.md`, `$SOURCE_DOC` (targeted reading)
**Output files:** `$SESSION_DIR/step-2-output.md`, updates `global-context.md`

**Stage goal:** Understand what the document is about as a whole and how its parts relate.

---

## Why Classify Content

### WHY Content Classification Matters

Classification activates the right extraction patterns:
- **Methodologies** need sequential process extraction
- **Frameworks** need dimensional/categorical extraction
- **Tools** need template structure extraction
- **Theories** need concept-to-application mapping

**Mental model:** You read fiction differently than non-fiction. Similarly, you extract differently from processes vs. frameworks.

Without classification, you might force a framework into linear steps (loses nuance) or extract a process as disconnected concepts (loses flow).

### WHAT to Classify

#### Classification Question 1: Practical vs. Theoretical

**Practical content** teaches **how to do something** (action-focused, procedures, methods)
**Theoretical content** teaches **that something is the case** (understanding-focused, principles, explanations)

**Decide:** Is this primarily teaching **how** (practical) or **why/what** (theoretical)?

**If theoretical:** Flag this - you'll need extra synthesis in Step 4 to make it actionable.

---

#### Classification Question 2: Content Structure Type

**Sequential (Methodology/Process):**
- Look for: Numbered steps, phases, "before/after" language
- Extraction focus: Order, dependencies, decision points

**Categorical (Framework/Model):**
- Look for: Dimensions, types, categories, "aspects of" language
- Extraction focus: Categories, definitions, relationships

**Structured (Tool/Template):**
- Look for: Blanks to fill, sections to complete
- Extraction focus: Template structure, what goes where

**Hybrid:**
- Combines multiple types (e.g., Design Thinking has framework + process + tools)
- Extraction focus: Identify boundaries, extract each appropriately

---

#### Classification Question 3: Completeness Level

Rate completeness 1-5:
- **5 = Complete:** Covers when/how/what, includes examples
- **3-4 = Partial:** Missing some aspects, needs gap-filling
- **1-2 = Incomplete:** Sketchy outline, missing critical pieces

**If < 3:** Ask user if you should proceed and fill gaps or find additional sources.

---

### WHAT to Document

```markdown
## Content Classification

**Type:** [Practical / Theoretical / Hybrid]
**Structure:** [Sequential / Categorical / Structured / Hybrid]
**Completeness:** [X/5] - [Brief rationale]

**Implications:**
- [What this means for extraction approach]
- [What skill structure will likely be]
```

**Present to user for validation before proceeding.**

---

## Why State Unity

### WHY Unity Statement Is Critical

The unity statement is your North Star for extraction:
- Prevents scope creep (keeps focus on main theme)
- Guides component selection (only extract what relates to unity)
- Defines skill purpose (becomes core of skill description)
- Enables coherence (everything connects back to this)

**Adler's rule:** "State the unity of the whole book in a single sentence, or at most a few sentences."

Without clear unity: bloated skills, missed central points, unclear purpose.

### WHAT to Extract

Create a one-sentence (or short paragraph) unity statement:

#### Unity Formula

**For practical content:**
"This [document type] teaches how to [VERB] [OBJECT] by [METHOD] in order to [PURPOSE]."

**Example:** "This guide teaches how to conduct user interviews by asking open-ended questions following the TEDW framework in order to discover unmet needs and validate assumptions."

**For theoretical content:**
"This [document type] explains [PHENOMENON] through [FRAMEWORK] to enable [APPLICATION]."

**Example:** "This paper explains cognitive load through information processing theory to enable instructional designers to create more effective learning materials."

---

#### How to Find the Unity

**Look for:**
1. Explicit statements in abstract, introduction, or conclusion
2. "This paper/guide..." statements
3. If not explicit, infer: What question does this answer? What problem does it solve?

**Test your statement:**
- Does it cover the whole document?
- Is it specific enough to be meaningful?
- Would the author agree?

---

### WHAT to Validate

**Present to user:**
```markdown
## Unity Statement

"[Your one-sentence unity statement]"

**Rationale:** [Why this captures the main point]

Does this align with your understanding?
```

---

## Why Enumerate Parts

### WHY Structure Mapping Is Essential

Understanding how parts relate to the whole:
- Reveals organization logic (chronological, categorical, priority-based)
- Shows dependencies (which parts build on others)
- Identifies extraction units (natural boundaries for deep reading)
- Exposes gaps (missing pieces)
- Guides skill structure (major parts often become skill sections)

**Adler's rule:** "Set forth the major parts of the book, and show how these are organized into a whole."

Without structure mapping: linear reading without understanding relationships, redundant extraction, poor skill organization.

### WHAT to Extract

#### Step 1: Identify Major Parts

Look for main section headings, numbered phases, distinct topics, natural breaks.

```markdown
## Major Parts

1. [Part 1 name] - [What it covers]
2. [Part 2 name] - [What it covers]
3. [Part 3 name] - [What it covers]
```

---

#### Step 2: Understand Relationships

**Common patterns:**

**Linear:** Part 1 → Part 2 → Part 3 (sequential, each builds on previous)

**Hub-spoke:** Core concept with multiple aspects exploring different dimensions

**Layered:** Foundation → Building blocks → Advanced applications

**Modular:** Independent parts, use what you need

---

#### Step 3: Map Parts to Unity

For each part:
- How does this contribute to the overall unity?
- Is this essential or supplementary?

```markdown
## Parts → Unity Mapping

**Part 1: [Name]**
- Contribution: [How it supports main theme]
- Essentiality: [Essential / Supporting / Optional]
```

---

#### Step 4: Identify Sub-Structure

For complex documents, go one level deeper (major parts + subsections).

**Example:**
```markdown
1. Introduction
   1.1. Problem statement
   1.2. Proposed solution
2. Core Framework
   2.1. Dimension 1
   2.2. Dimension 2
   2.3. How dimensions interact
3. Application Process
   3.1. Step 1
   3.2. Step 2
```

**Note:** Don't go too deep - 2 levels is usually sufficient.

---

### WHAT to Validate

**Present to user:**
```markdown
## Document Structure

[Your hierarchical outline]

**Organizational pattern:** [Linear/Hub-spoke/Layered/Modular]

**Key relationships:** [Major dependencies]

Does this match your understanding?
```

---

## Why Define Problems

### WHY Problem Identification Matters

Understanding the problems being solved:
- Clarifies purpose (why does this methodology exist)
- Identifies use cases (when to apply this skill)
- Reveals gaps (what problems are NOT addressed)
- Frames value (what benefit this provides)
- Guides "When to Use" section (problems = triggers)

**Adler's rule:** "Define the problem or problems the author is trying to solve."

Without problem identification: skills without clear triggers, unclear value proposition, no boundary conditions.

### WHAT to Extract

#### Level 1: Main Problem

**Question:** What is the overarching problem this document addresses?

```markdown
## Main Problem

**Problem:** [One-sentence statement]
**Why it matters:** [Significance]
**Current gaps:** [What's missing in current solutions]
```

---

#### Level 2: Sub-Problems

Map problems to structure:

```markdown
## Sub-Problems by Part

**Part 1: [Name]**
- Problem: [What this part solves]
- Solution approach: [How it solves it]
```

---

#### Level 3: Out-of-Scope Problems

What does this document NOT solve?

```markdown
## Out of Scope

This does NOT solve:
- [Problem 1 not addressed]
- [Problem 2 not addressed]

**Implication:** Users will need [OTHER SKILL] for these.
```

This defines boundaries (when NOT to use).

---

#### Level 4: Problem-Solution Mapping

```markdown
| Problem | Solution Provided | Where Addressed |
|---------|------------------|----------------|
| [Problem 1] | [Solution] | [Part/Section] |
| [Problem 2] | [Solution] | [Part/Section] |
```

This becomes the foundation for "When to Use" section.

---

### WHAT to Validate

**Present to user:**
```markdown
## Problems Being Solved

**Main problem:** [Statement]

**Sub-problems:**
1. [Problem 1] → Solved by [Part/Method]
2. [Problem 2] → Solved by [Part/Method]

**Not addressed:**
- [Out of scope items]

**Implications for "When to Use":** [Draft triggers based on problems]

Is this problem framing accurate?
```

---

## Write Step 2 Output

After completing structural analysis and getting user approval, write to output file:

```bash
cat > "$SESSION_DIR/step-2-output.md" << 'EOF'
# Step 2: Structural Analysis Output

## Content Classification

**Type:** [Practical / Theoretical / Hybrid]
**Structure:** [Sequential / Categorical / Structured / Hybrid]
**Completeness:** [X/5] - [Rationale]

## Unity Statement

"[One-sentence unity statement]"

**Rationale:** [Why this captures the main point]

## Document Structure

[Hierarchical outline of major parts]

1. [Part 1] - [Description]
   1.1. [Subsection]
   1.2. [Subsection]
2. [Part 2] - [Description]
   ...

**Organizational pattern:** [Linear/Hub-spoke/Layered/Modular]

## Problems Being Solved

**Main problem:** [One-sentence statement]

**Sub-problems:**
1. [Problem 1] → Solved by [Part/Section]
2. [Problem 2] → Solved by [Part/Section]

**Out of scope:** [What this doesn't address]

## User Validation

**Status:** [Approved / Needs revision]
**User notes:** [Feedback]

EOF
```

**Update global context:**

```bash
cat >> "$SESSION_DIR/global-context.md" << 'EOF'

## Step 2 Complete

**Content type:** [type]
**Unity:** [short version]
**Major parts:** [count]
**Ready for extraction:** Yes

EOF
```

**Next step:** Step 3 (Component Extraction) will read `global-context.md` + `step-2-output.md`.

# Synthesis and Application

This resource supports **Step 4** of the Skill Creator workflow.

**Input files:** `$SESSION_DIR/global-context.md`, `$SESSION_DIR/step-3-output.md`
**Output files:** `$SESSION_DIR/step-4-output.md`, updates `global-context.md`

**Stage goal:** Transform extracted components into actionable, practical guidance.

---

## Why Evaluate Completeness

### WHY Critical Evaluation Matters

Before transforming to application, you must evaluate what you've extracted:
- **Is it logically sound?** Do the arguments make sense?
- **Is it complete?** Are there gaps or missing pieces?
- **Is it consistent?** Do parts contradict each other?
- **Is it practical?** Can this actually be applied?

**Mental model:** You're fact-checking and quality-assuring before building. Bad foundation = bad skill.

**Adler's Critical Stage:** "Is it true? What of it?" - evaluating truth and significance.

Without evaluation: you might create skills based on incomplete or flawed methodologies, perpetuate errors, build unusable workflows.

### WHAT to Evaluate

#### Completeness Check

**Ask for each major component:**

**Terms:**
- Are all key concepts defined?
- Are definitions clear and unambiguous?
- Are there terms used but not defined?

**Propositions:**
- Are claims supported with evidence or reasoning?
- Are there contradictions between propositions?
- Are assumptions stated or hidden?

**Arguments:**
- Are logical sequences complete (no missing steps)?
- Do conclusions follow from premises?
- Are decision criteria specified?

**Solutions:**
- Are examples representative or cherry-picked?
- Do solutions address the stated problems?
- Are edge cases considered?

---

#### Logic Check

**Identify logical issues:**

**Gaps:** "The document jumps from A to C without explaining B"
- **Action:** Note the gap; decide if you can fill it or need user input

**Contradictions:** "Section 2 says X, but Section 5 says not-X"
- **Action:** Flag for user; determine which is correct

**Circular reasoning:** "A is true because of B; B is true because of A"
- **Action:** Identify the actual foundation or note as limitation

**Unsupported claims:** "The author asserts X but provides no evidence"
- **Action:** Note as assumption; decide if acceptable

---

#### Practical Feasibility Check

**Can this actually be used?**

**Resource requirements:**
- Does this require tools/resources users won't have?
- Are time requirements realistic?

**Skill prerequisites:**
- Does this assume knowledge users won't have?
- Are dependencies stated?

**Context constraints:**
- Does this only work in specific contexts?
- Are limitations acknowledged?

---

### WHAT to Document

```markdown
## Completeness Evaluation

**Complete:** [What's well-covered]
**Gaps:** [What's missing]
**Contradictions:** [Any inconsistencies found]
**Assumptions:** [Unstated prerequisites]

**Logical soundness:** [Strong / Moderate / Weak] - [Rationale]
**Practical feasibility:** [High / Medium / Low] - [Rationale]

**Implications for skill creation:**
- [What needs to be added]
- [What needs clarification]
- [What needs user input]
```

**Present to user:** Share evaluation and ask for input on gaps/issues.

---

## Why Identify Applications

### WHY Application Mapping Matters

Extracted theory must connect to real-world use:
- **Triggers skill invocation:** Users need to know WHEN to use this
- **Validates usefulness:** Theory without application is just information
- **Reveals variations:** Different contexts may need different approaches
- **Informs examples:** Concrete scenarios make skills understandable

**Mental model:** A hammer is useful because you know when to use it (nails) and when not to (screws). Same with skills.

**Adler's "What of it?" question:** What does this matter in practice?

Without application mapping: skill sits unused because users don't recognize appropriate situations, unclear value proposition.

### WHAT to Identify

#### Scenario Mapping

**Generate concrete scenarios where this skill applies:**

**Format:**
```markdown
### Scenario: [Descriptive name]

**Context:** [Situation description]
**Problem:** [What needs solving]
**How skill applies:** [Which parts of methodology address this]
**Expected outcome:** [What success looks like]
**Variations:** [How application might differ in sub-contexts]
```

**Aim for:** 3-5 diverse scenarios covering different domains or contexts

---

#### Domain Transfer

**If document examples are domain-specific, identify transfer opportunities:**

**Original domain:** [Where document's examples come from]
**Transfer domains:** [Other areas where this applies]

**Example:**
- **Original:** Reading books analytically
- **Transfer:** Reading research papers, analyzing codebases, understanding documentation, evaluating business reports

**For each transfer:**
- What changes in the application?
- What stays the same?
- Are there domain-specific considerations?

---

#### Use Case Patterns

**Identify recurring patterns of when to use:**

**Pattern types:**
- **Problem-driven:** "Use when you encounter [PROBLEM]"
- **Goal-driven:** "Use when you want to achieve [GOAL]"
- **Context-driven:** "Use when you're in [CONTEXT]"
- **Trigger-driven:** "Use when [EVENT] happens"

**Example patterns:**
```markdown
**Problem-driven:** Use inspectional reading when you have limited time and need to understand a book quickly

**Goal-driven:** Use analytical reading when you want to master complex material above your current level

**Context-driven:** Use syntopical reading when researching a topic requiring multiple sources

**Trigger-driven:** Use critical reading stage after you've fully understood the author's position
```

---

### WHAT to Document

```markdown
## Application Mapping

**Scenarios:**
1. [Scenario 1 with context and application]
2. [Scenario 2]
3. [Scenario 3]

**Domain transfers:**
- Original: [Domain]
- Applicable to: [List of domains]

**Use case patterns:**
- [Pattern type]: [Trigger description]

**Boundary conditions (when NOT to use):**
- [Context where skill doesn't apply]
```

**Present to user:** "Do these scenarios match your intended use cases? Any to add or modify?"

---

## Why Transform to Actions

### WHY Actionable Steps Matter

Theory must become procedure:
- **Users need clear instructions:** "Do this, then this, then this"
- **Reduces cognitive load:** No need to interpret principles on the fly
- **Enables execution:** Can follow steps even without deep theoretical understanding
- **Allows refinement:** Clear steps can be improved iteratively

**Mental model:** Recipe vs. food science. Both are valuable, but recipes get you cooking immediately.

Without transformation to actions: skill remains theoretical, users struggle to apply, high barrier to entry.

### WHAT to Transform

#### From Propositions → Principles/Guidelines

**Propositions** (theoretical claims) become **Principles** (actionable guidance)

**Transformation pattern:**
```markdown
**Proposition:** [Theoretical claim]
↓
**Principle:** [How to apply this in practice]
```

**Example:**
```markdown
**Proposition:** Active reading improves retention more than passive reading.
↓
**Principle:** Take notes and mark important passages while reading to improve retention.
```

---

#### From Arguments → Workflow Steps

**Arguments** (logical sequences) become **Workflow Steps** (procedures)

**Transformation pattern:**
```markdown
**Argument:** [Logical sequence]
↓
**Step X:** [Action to take]
  **Input:** [What you need]
  **Action:** [What to do]
  **Output:** [What you get]
  **Decision:** [If applicable]
```

**Example:**
```markdown
**Argument:** Systematic skimming before deep reading saves time by identifying valuable books.
↓
**Step 1: Systematic Skim**
  **Input:** Book you're considering reading
  **Action:** Read title, TOC, index, first/last paragraphs
  **Output:** Understanding of book structure and main points
  **Decision:** Is this book worth deep reading? Yes → Step 2; No → Next book
```

---

#### From Solutions → Examples and Templates

**Solutions** (demonstrations) become **Examples** (illustrations) and **Templates** (structures)

**For examples:**
- Show application in specific context
- Include before/after if possible
- Highlight key decision points

**For templates:**
- Extract reusable structure
- Add placeholders
- Provide completion instructions

---

#### Handling Theoretical Content

**If source is theoretical (no inherent procedure):**

**Ask:**
1. What decisions does this theory inform?
2. What would change in practice based on this?
3. What would someone DO differently knowing this?

**Transform:**
```markdown
**Theory:** [Conceptual understanding]
↓
**Application decision framework:**
**When to use:** [Trigger]
**How to apply:** [Action steps informed by theory]
**What to consider:** [Factors from theoretical understanding]
```

---

### WHAT to Document

```markdown
## Actionable Transformation

**Principles** (from propositions):
1. [Principle 1]
2. [Principle 2]

**Workflow** (from arguments):
**Step 1:** [Action]
  - Input: [X]
  - Action: [Y]
  - Output: [Z]
**Step 2:** [Action]
  ...

**Examples** (from solutions):
- [Example 1 showing application]

**Templates** (if applicable):
- [Template structure]

**Theoretical foundations** (if source is theoretical):
- Decision framework: [How theory informs practice]
```

**Present to user:** "Does this workflow make sense? Is it actionable as written?"

---

## Why Define Triggers

### WHY When/How Clarity Matters

Users need to know:
- **WHEN:** In what situations should I invoke this skill?
- **HOW:** What's the entry point and overall approach?

**Mental model:** A fire extinguisher has clear labels for WHEN (type of fire) and HOW (pull pin, aim, squeeze). Skills need the same clarity.

Without clear triggers: skills go unused even when appropriate, users uncertain about application, poor skill adoption.

### WHAT to Define

#### When to Use (Triggers)

**Based on problem-solution mapping from Step 2 and application scenarios from earlier in Step 4:**

```markdown
## When to Use

**Use this skill when:**
- [Trigger condition 1]
- [Trigger condition 2]
- [Trigger condition 3]

**Examples of trigger situations:**
- [Concrete situation 1]
- [Concrete situation 2]

**Do NOT use when:**
- [Anti-pattern 1]
- [Anti-pattern 2]
```

**Make triggers specific:**
- ❌ Vague: "Use when you need to understand something"
- ✅ Specific: "Use when you need to extract a methodology from a document and make it reusable"

---

#### How to Use (Entry Point)

**Provide clear entry guidance:**

```markdown
## How to Use This Skill

**Prerequisites:**
- [What you need before starting]

**Typical session flow:**
1. [High-level step 1]
2. [High-level step 2]
3. [High-level step 3]

**Time investment:**
- [Estimated time for typical use]

**Expected outcome:**
- [What you'll have when done]
```

---

## Write Step 4 Output

After completing synthesis and getting user approval, write to output file:

```bash
cat > "$SESSION_DIR/step-4-output.md" << 'EOF'
# Step 4: Synthesis and Application Output

## Completeness Evaluation

**Complete:** [What's well-covered]
**Gaps:** [What's missing]
**Contradictions:** [Any inconsistencies]
**Logical soundness:** [Strong/Moderate/Weak] - [Rationale]
**Practical feasibility:** [High/Medium/Low] - [Rationale]

## Application Scenarios

1. **Scenario:** [Name]
   - Context: [Description]
   - How skill applies: [Application]
   - Expected outcome: [Result]

2. **Scenario:** [Name]
   ...

**Domain transfers:** [Original domain → Transfer domains]

## Actionable Workflow

**Principles** (from propositions):
1. [Principle 1]
2. [Principle 2]

**Workflow Steps** (from arguments):
**Step 1:** [Action]
  - Input: [X]
  - Action: [Do Y]
  - Output: [Z]
  - Decision: [If applicable]

**Step 2:** [Action]
  ...

**Examples:** [Application examples]
**Templates:** [If applicable]

## Triggers (When/How to Use)

**When to use:**
- [Trigger condition 1]
- [Trigger condition 2]

**When NOT to use:**
- [Anti-pattern 1]

**How to use:**
- Prerequisites: [What's needed]
- Time investment: [Estimate]
- Expected outcome: [What you'll have]

## User Validation

**Status:** [Approved / Needs revision]
**User notes:** [Feedback]

EOF
```

**Update global context:**

```bash
cat >> "$SESSION_DIR/global-context.md" << 'EOF'

## Step 4 Complete

**Workflow defined:** [X steps]
**Triggers identified:** Yes
**Ready for construction:** Yes

EOF
```

**Next step:** Step 5 (Skill Construction) will read `global-context.md` + `step-4-output.md`.

# Skill Construction

This resource supports **Step 5** of the Skill Creator workflow.

**Input files:** `$SESSION_DIR/global-context.md`, `$SESSION_DIR/step-4-output.md`
**Output files:** `$SESSION_DIR/step-5-output.md`, actual skill files created in target directory, updates `global-context.md`

**Stage goal:** Build the actual skill files following standard structure.

---

## Why Complexity Level

### WHY Complexity Assessment Matters

Complexity determines skill structure:
- **Simple skills:** SKILL.md only (no resources needed)
- **Moderate skills:** SKILL.md + 1-3 focused resource files
- **Complex skills:** SKILL.md + 4-8 resource files

**Mental model:** Don't build a mansion when a cottage will do. Match structure to content needs.

Over-engineering (too many files for simple content): maintenance burden, navigation difficulty
Under-engineering (too little structure for complex content): bloated files, poor organization

### WHAT Complexity Levels Exist

**Levels:**

**Level 1 - Simple:** 3-5 steps, < 300 lines total → SKILL.md + rubric only

**Level 2 - Moderate:** 5-8 steps, 300-800 lines → SKILL.md + 1-3 resource files + rubric

**Level 3 - Complex:** 8+ steps, 800+ lines → SKILL.md + 4-8 resource files + rubric

---

### WHAT to Decide

**Assess your extracted content:**

**Count:**
- Total workflow steps: [X]
- Major decision points: [X]
- Key concepts to explain: [X]
- Examples needed: [X]
- Total estimated lines: [X]

**Complexity level:** [1 / 2 / 3]

**Rationale:** [Why this level fits]

**Proposed structure:** [List of files]

**Present to user:** "Based on content volume, I recommend [LEVEL] complexity. Structure: [FILES]. Does this make sense?"

---

## Why Plan Resources

### WHY Resource Planning Matters

Resource files should be:
- **Focused:** Each file covers one cohesive topic
- **Referenced:** Linked from SKILL.md workflow steps
- **Sized appropriately:** Under 500 lines each
- **WHY/WHAT structured:** Follows standard format

**Mental model:** Resource files are like appendices - referenced when needed, not read linearly.

Poor planning: overlapping content, unclear purpose, navigation difficulty, files too large or too granular.

### WHAT to Plan

#### Grouping Principles

**Group related content into resource files based on:**

**By workflow step** (for complex skills):
- One resource per major step
- Contains WHY/WHAT for all sub-steps
- Example: `inspectional-reading.md` for Step 1

**By topic** (for moderate skills):
- Group related concepts
- Example: `key-concepts.md`, `decision-framework.md`, `examples.md`

**By type** (alternative):
- All principles in one file
- All examples in another
- All templates in another

---

#### Resource File Template

**Each resource file should include:**

```markdown
# [Resource Name]

This resource supports **Step X** of the [Skill Name] workflow.

---

## Why [First Topic]

### WHY This Matters

[Brief explanation activating context, not over-explaining]

### WHAT to Do

[Specific instructions, options with tradeoffs, user choice points]

---

## Why [Second Topic]

### WHY This Matters

...

### WHAT to Do

...
```

---

#### File Naming

**Use descriptive, kebab-case names:**
- ✅ `inspectional-reading.md`
- ✅ `component-extraction.md`
- ✅ `evaluation-rubric.json`
- ❌ `resource1.md`
- ❌ `temp_file.md`

---

### WHAT to Document

```markdown
## Resource Plan

**Complexity level:** [Level 1/2/3]

**Resource files:**

1. **[filename.md]**
   - Purpose: [What this covers]
   - Linked from: [Which SKILL.md steps]
   - Estimated lines: [X]

2. **[filename.md]**
   - Purpose: [What this covers]
   - Linked from: [Which SKILL.md steps]
   - Estimated lines: [X]

3. **evaluation-rubric.json**
   - Purpose: Quality scoring
   - Linked from: Final validation step

**Total files:** [X]
```

**Present to user:** "Here's the resource structure plan. Any changes needed?"

---

## Why SKILL.md Structure

### WHY Standard Structure Matters

SKILL.md must follow conventions:
- **YAML frontmatter:** For skill system identification and invocation
- **Table of Contents:** For navigation
- **Read This First:** For context and overview
- **Workflow with checklist:** For execution
- **Step details:** With resource links where needed

**Mental model:** SKILL.md is the "main" file - everything starts here.

Without standard structure: skill won't be invoked correctly, users confused about how to start, poor usability.

### WHAT to Include

#### 1. YAML Frontmatter

```yaml
---
name: skill-name
description: Use when [TRIGGER CONDITIONS - focus on WHEN not WHAT]. Invoke when [USER MENTIONS]. Also applies when [SCENARIOS].
---
```

**Critical:** Description focuses on WHEN to use (triggers), not WHAT it does.

**Bad:** `description: Extracts skills from documents`
**Good:** `description: Use when user has a document containing theory or methodology and wants to convert it into a reusable skill`

---

#### 2. Title and Table of Contents

Standard TOC linking to Read This First, Workflow, and each step.

#### 3. Read This First

Includes: What skill does (1-2 sentences), Process overview, Why it works, Collaborative nature.

#### 4. Workflow Section

Must have: **"COPY THIS CHECKLIST"** instruction, followed by checklist with steps and sub-tasks.

#### 5. Step Details

Format: Step heading, Goal statement, Sub-tasks with resource links or inline instructions.

---

### WHAT to Validate

**Check:**
- ✅ YAML frontmatter present and description focuses on WHEN
- ✅ Table of contents complete
- ✅ Read This First section provides context
- ✅ Workflow has explicit copy instruction
- ✅ All steps have goals and sub-tasks
- ✅ Resource links are correct and use anchors
- ✅ File is under 500 lines

---

## Why Resource Structure

### WHY WHY/WHAT Format Matters

Resource files follow standard format:
- **WHY sections:** Activate relevant context, explain importance
- **WHAT sections:** Provide specific instructions, present options

**Mental model:** WHY primes the LLM's activation space; WHAT provides execution guidance.

Without WHY: LLM may not activate relevant knowledge, shallow understanding
Without WHAT: Clear intent but unclear execution, user stuck on "now what?"

### WHAT to Include in Resources

#### WHY Section Format

Explains what this accomplishes, why it's important, how it fits in the process. Optional mental model. Keep focused - don't over-explain.

#### WHAT Section Format

Specific instructions in clear steps. If options exist, present each with: when to use, pros, cons, how. Mark user choice points.

---

### WHAT to Validate

**For each resource file, check:**
- ✅ Each major section has WHY and WHAT subsections
- ✅ WHY explains importance without over-explaining
- ✅ WHAT provides concrete, actionable guidance
- ✅ Options presented with trade-offs when applicable
- ✅ User choice points clearly marked
- ✅ File is under 500 lines

---

## Why Evaluation Rubric

### WHY Rubric Matters

The rubric enables:
- **Self-assessment:** LLM can objectively score its work
- **Quality standards:** Clear criteria for success
- **Improvement identification:** Know what needs fixing
- **User transparency:** User sees quality assessment

**Mental model:** Rubric is like a grading rubric for an assignment - objective criteria for evaluation.

Without rubric: no quality control, subjective assessment, missed improvements.

### WHAT to Include

#### JSON Structure

```json
{
  "criteria": [
    {
      "name": "[Criterion Name]",
      "description": "[What this measures]",
      "scores": {
        "1": "[Description of score 1 performance]",
        "2": "[Description of score 2 performance]",
        "3": "[Description of score 3 performance]",
        "4": "[Description of score 4 performance]",
        "5": "[Description of score 5 performance]"
      }
    }
  ],
  "threshold": 3.5,
  "passing_note": "Average score must be ≥ 3.5 for skill to be considered complete. Scores below 3 in any category require revision."
}
```

---

#### Standard Criteria

**Recommended criteria for skills:**

1. **Completeness:** Are all required components present?
2. **Clarity:** Are instructions clear and unambiguous?
3. **Actionability:** Can this be followed step-by-step?
4. **Structure:** Is organization logical and navigable?
5. **Examples:** Are sufficient examples provided?
6. **Triggers:** Is "when to use" clearly defined?

**Customize based on skill type** - add domain-specific criteria as needed.

---

#### Scoring Guidelines

**Score scale:**
- **5:** Excellent - exceeds expectations
- **4:** Good - meets all requirements well
- **3:** Adequate - meets minimum requirements
- **2:** Needs improvement - significant gaps
- **1:** Poor - major issues

**Threshold:** Average ≥ 3.5 recommended

---

### WHAT to Validate

**Check rubric:**
- ✅ 4-7 criteria (not too few or too many)
- ✅ Each criterion has clear descriptions for scores 1-5
- ✅ Criteria are measurable (not subjective)
- ✅ Threshold is specified
- ✅ JSON is valid

---

## Write Step 5 Output

After completing skill construction and verifying files, write to output file:

```bash
cat > "$SESSION_DIR/step-5-output.md" << 'EOF'
# Step 5: Skill Construction Output

## Complexity Level

**Level:** [1/2/3] - [Simple/Moderate/Complex]
**Rationale:** [Why this level]

## Resource Plan

**Files created:**
1. SKILL.md ([X] lines) - Main skill file
2. resources/[filename1].md ([X] lines) - [Purpose]
3. resources/[filename2].md ([X] lines) - [Purpose]
...
N. resources/evaluation-rubric.json - Quality scoring

**Total files:** [X]

## Skill Location

**Path:** [Full path to created skill directory]

## File Verification

**Line counts:**
- ✅ SKILL.md: [X]/500 lines
- ✅ [file1].md: [X]/500 lines
- ✅ [file2].md: [X]/500 lines
...

**Structure checks:**
- ✅ YAML frontmatter present and WHEN-focused
- ✅ Table of contents complete
- ✅ Workflow has copy instruction
- ✅ All resource links valid
- ✅ WHY/WHAT structure followed
- ✅ Rubric JSON valid

## User Validation

**Status:** [Approved / Needs revision]
**User notes:** [Feedback]

EOF
```

**Update global context:**

```bash
cat >> "$SESSION_DIR/global-context.md" << 'EOF'

## Step 5 Complete

**Skill created at:** [path]
**Files:** [count]
**All files under 500 lines:** Yes
**Ready for validation:** Yes

EOF
```

**Next step:** Step 6 (Validation) will read `global-context.md` + `step-5-output.md` + actual skill files.

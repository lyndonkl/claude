# Skill Structure Guidelines

## Table of Contents
- [YAML Frontmatter](#yaml-frontmatter)
- [SKILL.md Structure](#skillmd-structure)
- [Resources Folder Organization](#resources-folder-organization)
- [File Size Limits](#file-size-limits)
- [Progressive Disclosure Pattern](#progressive-disclosure-pattern)

---

## YAML Frontmatter

### Description Field

**CRITICAL: Focus on WHEN to use, not WHAT it does**

The description should answer: "In what situations should Claude invoke this skill?"

**Structure:**
```yaml
description: Use when [situation 1], [situation 2], [situation 3], or [situation 4]. Invoke when user mentions [trigger phrase 1], [trigger phrase 2], or [trigger phrase 3].
```

### Rules

**Do:**
- Start with "Use when" or "Invoke when"
- List specific situations, contexts, or triggers
- Include user phrases that would trigger this skill
- Be concrete about scenarios
- Max 1024 characters
- Use third person

**Don't:**
- Start with "Create/Build/Generate/Help/Guide" (that's WHAT, not WHEN)
- Describe the output or process
- Use vague triggers like "when needed" or "for better results"

### Examples

**Bad (describes WHAT):**
```yaml
description: Create abstraction ladders that move between high-level concepts and concrete examples for better communication.
```

**Good (describes WHEN):**
```yaml
description: Use when explaining concepts at different expertise levels, moving between abstract principles and concrete implementation, identifying edge cases, designing layered documentation, or bridging strategy-execution gaps. Invoke when user mentions abstraction levels, making concepts concrete, or explaining at different depths.
```

**Bad (describes WHAT):**
```yaml
description: Extract and analyze components from files to create reusable skills.
```

**Good (describes WHEN):**
```yaml
description: Use when user wants to convert a document/file into a reusable skill, has a methodology or framework in a file that should become actionable, asks to "make this into a skill" or "extract a skill from this", or when analyzing methodology documents, framework guides, or procedural content for skill creation. Invoke when user mentions creating skills from files, extracting methodologies, or converting documentation into structured workflows.
```

---

## SKILL.md Structure

### Required Sections (in order)

```markdown
---
name: skill-name
description: [WHEN-focused description]
---

# Skill Display Name

## Table of Contents
- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [What is [Concept Name]?](#what-is-concept-name)
- [Workflow](#workflow)
  - [Step 1](#1-step-name)
  - [Step 2](#2-step-name)
  - [etc...]
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose
[1-2 sentences on what this skill helps accomplish]

## When to Use This Skill
- [Trigger situation 1]
- [Trigger situation 2]
- [Trigger situation 3]

**Trigger phrases:** "[phrase 1]", "[phrase 2]", "[phrase 3]"

## What is [Concept Name]?
[Brief explanation with quick example]

## Workflow

Copy this checklist and track your progress:

```
[Skill Name] Progress:
- [ ] Step 1: [Short action name]
- [ ] Step 2: [Short action name]
- [ ] Step 3: [Short action name]
- [ ] Step 4: [Short action name]
- [ ] Step 5: [Short action name]
```

**Step 1: [Action name]**

[1-2 sentence description of what to do]. See [Section Link](#detailed-section) or [resources/specific-file.md](resources/specific-file.md) for detailed guidance.

**Step 2: [Action name]**

[1-2 sentence description]. See [Section Link](#detailed-section) or [resources/other-file.md](resources/other-file.md) for [specific technique/method].

[Continue for all steps...]

## Common Patterns
[Typical applications and usage patterns]

## Guardrails

**Do:**
- [Best practice 1]
- [Best practice 2]
- [Best practice 3]

**Don't:**
- [Anti-pattern 1]
- [Anti-pattern 2]
- [Anti-pattern 3]

## Quick Reference
- **[Resource Name]**: `resources/file-name.md`
- **[Resource Name]**: `resources/other-file.md`
- **Quality rubric**: `resources/evaluators/rubric_skillname.json`
```

### Key Principles

1. **Table of Contents First**
   - Always include after title, before content
   - Link to all major sections
   - Use markdown anchor links: `[Section Name](#section-anchor)`

2. **Progressive Disclosure**
   - Start with high-level overview (Purpose, When to Use, What Is It)
   - Workflow gives concise steps with links to details
   - Detailed sections come after workflow
   - Resources provide deepest detail

3. **Workflow Pattern**
   - Show full checklist in code block first
   - Each step is 1-2 sentences + link to details
   - Links go to sections in SKILL.md OR resources/*.md
   - Must use markdown links for navigation

4. **Link Requirements**
   - Every workflow step MUST link somewhere for details
   - Internal links: `[Section Name](#section-anchor)`
   - Resource links: `[resources/file.md](resources/file.md)`
   - Example: "See [Reading Strategies](resources/reading-strategies.md) for skim techniques"

---

## Resources Folder Organization

### Required Files

**1. Evaluator Rubric (ALWAYS required)**
```
resources/evaluators/rubric_[skillname].json
```

### Optional but Recommended

**2. Topic-Specific Resource Files**

Instead of monolithic template.md or methodology.md, create focused files:

```
resources/
├── [concept-1].md (e.g., reading-strategies.md)
├── [concept-2].md (e.g., file-type-strategies.md)
├── [concept-3].md (e.g., component-extraction.md)
└── evaluators/
    └── rubric_[skillname].json
```

**When to create topic-specific files:**
- Concept is substantial enough to warrant its own file (>50 lines)
- Concept is referenced from multiple workflow steps
- Concept would bloat SKILL.md if included inline
- Concept contains detailed tables, examples, or procedures

**3. Examples Folder (if needed)**
```
resources/examples/
├── example-1.md
├── example-2.md
└── case-study.md
```

Use when:
- Worked examples are valuable
- Examples are lengthy (>100 lines)
- Multiple example types exist

**4. Scripts Folder (if needed)**
```
resources/scripts/
├── utility-1.py
└── automation-2.sh
```

Use when:
- Skill involves executable automation
- Tooling enhances the workflow

### Organization Principles

- **Keep references one level deep** (no nested cross-references)
- **Files > 100 lines should have table of contents**
- **Use clear, descriptive filenames** (what-concept-covers.md)
- **Remove redundant or outdated files**
- **NO "When to Use" sections in resource files** (that's in SKILL.md)

---

## File Size Limits

### Hard Limits (MUST NOT EXCEED)

| File Type | Hard Limit | Ideal Target |
|-----------|-----------|--------------|
| **SKILL.md** | 300 lines | < 250 lines |
| **Resource files** | 500 lines each | < 400 lines each |
| **Rubric JSON** | No limit | ~150-200 lines |
| **Example files** | Any length | N/A (loaded on-demand) |

### Why These Limits Matter

- **Token efficiency**: Claude loads entire files when referenced
- **Progressive disclosure**: Start small (SKILL.md), go deeper only if needed
- **Context conservation**: Bloated files waste context window
- **User experience**: Smaller files are faster to scan and navigate

### If Resource File Exceeds 500 Lines

**Options:**

1. **Split into multiple topic-specific files**
   ```
   Instead of: resources/methodology.md (800 lines)
   Create: resources/reading-strategies.md (250 lines)
           resources/extraction-techniques.md (300 lines)
           resources/validation-methods.md (250 lines)
   ```

2. **Move examples to separate files**
   ```
   Move case studies to: resources/examples/case-study-*.md
   Link from resource file
   ```

3. **Condense verbose sections**
   - Use bullet lists instead of paragraphs
   - Remove redundant explanations
   - Link to examples instead of inline descriptions

### Checking During Creation

```bash
# Check line counts
wc -l skill-name/SKILL.md skill-name/resources/*.md

# Identify sections to extract if over limit
grep -n "^## " resources/large-file.md
```

**Red flags:**
- ❌ SKILL.md > 350 lines → Move details to resources
- ❌ Resource file > 600 lines → Split into topic files
- ❌ Repeating same info across files → Remove redundancy

---

## Progressive Disclosure Pattern

### The Pattern

**Level 1: SKILL.md Overview (Quick start)**
- What is this skill?
- When to use it?
- High-level workflow (5-7 steps, 1-2 sentences each)
- Links to resources for details

**Level 2: Resource Files (Deep dive on specific concepts)**
- Detailed techniques for each concept
- Tables, examples, procedures
- Referenced from SKILL.md workflow steps

**Level 3: Examples (Demonstration)**
- Full worked examples
- Case studies
- Loaded only when needed

### Workflow Linking Pattern

**In SKILL.md:**
```markdown
**Step 2: Skim the file**

Use boundary reading and structural extraction to understand file type and structure without reading everything. See [resources/reading-strategies.md](resources/reading-strategies.md) for specific skim techniques by file type.
```

**In resources/reading-strategies.md:**
```markdown
## Boundary Reading

[Detailed explanation with code examples, tables, etc.]

## Structural Extraction

[Detailed explanation specific to different file types...]
```

**Result:** User sees concise step in workflow, can dive into details if needed.

### Benefits

- **User sees full workflow at a glance** (checkbox list)
- **Each step is concise** (1-2 sentences) with link to details
- **Details are available but not forced**
- **Files remain focused and scannable**

---

## Rubric JSON Structure

### Required Format

```json
{
  "name": "[Skill Name] Quality Rubric",
  "scale": {
    "min": 1,
    "max": 5,
    "description": "1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent"
  },
  "criteria": [
    {
      "name": "[Criterion Name]",
      "description": "[What this criterion measures]",
      "scoring": {
        "1": "[Poor performance description]",
        "2": "[Fair performance description]",
        "3": "[Good performance description]",
        "4": "[Very good performance description]",
        "5": "[Excellent performance description]"
      }
    }
  ],
  "overall_assessment": {
    "thresholds": {
      "excellent": "Average score ≥ 4.5 across all criteria",
      "very_good": "Average score ≥ 4.0 across all criteria",
      "good": "Average score ≥ 3.5 across all criteria",
      "acceptable": "Average score ≥ 3.0 across all criteria",
      "needs_improvement": "Average score < 3.0"
    }
  },
  "usage_instructions": "Rate each criterion independently on 1-5 scale. Calculate average. Minimum standard: ≥ 3.5 before delivering to user. Focus revision on lowest-scoring criteria."
}
```

### Rubric Criteria Best Practices

**Good criteria:**
- Measure observable qualities
- Have clear differentiation between score levels
- Cover different aspects of output (not redundant)
- Enable actionable feedback

**Typical criteria categories:**
- **Completeness**: Are all required elements present?
- **Quality**: Do elements meet quality standards?
- **Clarity**: Is output understandable?
- **Actionability**: Can user act on the output?
- **Distinctness** (for skills): Is it unique/non-duplicate?

**Number of criteria:** 5-15 (sweet spot: 8-12)

---

## Naming Conventions

### Skill Name (folder and YAML name field)

**Format:** `lowercase-with-hyphens`

**Patterns:**
- Methodology-based: `design-thinking`, `root-cause-analysis`
- Framework-based: `decision-matrix`, `swot-analysis`
- Activity-based: `abstraction-concrete-examples`, `skill-extraction`
- Domain-specific: `adr-architecture`, `api-design-patterns`

**Rules:**
- Be specific but concise (2-4 words)
- Use action words when possible
- Avoid generic terms (don't use just "analysis" or "helper")
- Check existing skills to avoid duplicates

**Examples:**
- ✓ `skill-extraction` (clear, specific)
- ✓ `api-design-review` (specific domain)
- ✗ `helper` (too generic)
- ✗ `the-best-framework` (unprofessional)

### Resource File Names

**Format:** `concept-name.md`

**Examples:**
- `reading-strategies.md` (covers skimming and deep reading)
- `file-type-strategies.md` (covers code, docs, notebooks)
- `component-extraction.md` (covers systematic extraction)
- `context-management.md` (covers managing large files)

**Principles:**
- Descriptive of concept covered
- Singular focus (one main topic per file)
- Easy to remember and reference

---

## Quick Checklist

**Before finalizing a skill, copy this validation checklist and verify:**

```
Skill Quality Validation:
- [ ] YAML: Description focuses on WHEN (not WHAT)
- [ ] YAML: Includes situations and trigger phrases
- [ ] YAML: Under 1024 characters
- [ ] SKILL.md: Has table of contents with working links
- [ ] SKILL.md: Workflow with checkbox list + concise steps
- [ ] SKILL.md: Each workflow step links to details
- [ ] SKILL.md: Under 300 lines (ideally < 250)
- [ ] Resources: Evaluator rubric exists
- [ ] Resources: Each file under 500 lines
- [ ] Resources: No redundancy between files
- [ ] Overall: Progressive disclosure maintained
- [ ] Overall: All links work
- [ ] Overall: File size limits respected
```

**Detailed checks:**

### YAML Frontmatter
- [ ] Description focuses on WHEN (not WHAT)
- [ ] Includes specific situations and trigger phrases
- [ ] Under 1024 characters

### SKILL.md
- [ ] Has table of contents with working links
- [ ] Purpose section (1-2 sentences)
- [ ] "When to Use" section with triggers
- [ ] "What Is It" section with brief explanation
- [ ] Workflow with checkbox list + concise steps
- [ ] Each workflow step links to details
- [ ] Common Patterns section
- [ ] Guardrails (Do/Don't) section
- [ ] Quick Reference to resources
- [ ] Under 300 lines (ideally < 250)

### Resources
- [ ] Evaluator rubric exists (rubric_[name].json)
- [ ] Topic-specific resource files created as needed
- [ ] Each resource file has table of contents (if > 100 lines)
- [ ] Each resource file under 500 lines
- [ ] No redundancy between files
- [ ] Examples in separate folder (if lengthy)

### Overall
- [ ] Progressive disclosure maintained (overview → details)
- [ ] All links work (test them!)
- [ ] No redundant content across files
- [ ] File size limits respected
- [ ] Skill name follows conventions

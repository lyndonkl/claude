---
name: skill-extraction
description: Use when user wants to convert a document/file into a reusable skill, has a methodology or framework in a file that should become actionable, asks to "make this into a skill" or "extract a skill from this", or when analyzing methodology documents, framework guides, or procedural content for skill creation. Invoke when user mentions creating skills from files, extracting methodologies, or converting documentation into structured workflows.
---

# Skill Extraction Framework

## Table of Contents

- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [What is Skill Extraction?](#what-is-skill-extraction)
- [Workflow](#workflow)
- [Quick Reference](#quick-reference)

## Purpose

Extract structured, reusable skills from documents, methodologies, frameworks, or code files. Transform written knowledge into actionable Claude Code skills that others can invoke consistently.

## When to Use This Skill

- User provides a file containing a methodology or framework to extract
- User asks to "make this into a skill" or "create a skill from this document"
- Analyzing technical documentation, guides, or procedures for skill-worthiness
- Converting existing knowledge bases into executable workflows
- Extracting patterns from code, notebooks, or configuration files
- Building skills from research papers, blog posts, or educational content

**Trigger phrases:** "make this a skill", "extract skill from", "turn this into", "create skill", "methodology to skill"

## What is Skill Extraction?

A systematic process for reading files using Adler's analytical reading framework adapted for LLMs to:
1. Understand content structure and purpose without context dilution
2. Identify if it contains skill-worthy methodology
3. Extract key components systematically
4. Synthesize into properly structured Claude Code skills

**Quick Example:**
- **Input:** PDF about "Design Thinking methodology"
- **Output:** `design-thinking` skill with 5-stage workflow (empathize, define, ideate, prototype, test)

## Workflow

Copy this checklist and track your progress:

```
Skill Extraction Progress:
- [ ] Step 1: Pre-flight and skim
- [ ] Step 2: Classify and assess
- [ ] Step 3: Deep read and extract
- [ ] Step 4: Synthesize components
- [ ] Step 5: Generate skill files
- [ ] Step 6: Validate quality
```

**Step 1: Pre-flight and skim**

Gather file metadata (name, extension, size) and perform inspectional reading using boundary reading, structural extraction, and sampling techniques. Build mental model without reading everything. See [resources/reading-strategies.md](resources/reading-strategies.md) for skim techniques and [resources/file-type-strategies.md](resources/file-type-strategies.md) for file-specific approaches.

**Step 2: Classify and assess**

Determine content type (methodology/framework/tool/reference), identify main theme, and assess if skill-worthy using classification criteria. Apply "What of it?" question to identify practical capability. If multiple related files exist, use multi-file analysis strategy from [resources/reading-strategies.md](resources/reading-strategies.md#multi-file-analysis).

**Step 3: Deep read and extract**

Read file systematically using section-based chunking, windowing, or targeted reading. Extract components using structured notes template. For large files (>500 lines), apply context management strategies. See [resources/reading-strategies.md](resources/reading-strategies.md#analytical-reading-deep-reading) for deep reading techniques, [resources/component-extraction.md](resources/component-extraction.md) for extraction framework, and [resources/context-management.md](resources/context-management.md) for managing large files.

**Step 4: Synthesize components**

Review extracted components from notes and map to skill structure using component-to-skill mapping table. Abstract domain-specific language to generalizable patterns. Determine skill complexity and required resources. See [resources/component-extraction.md](resources/component-extraction.md#mapping-components-to-skill-structure) for mapping guidance and pattern abstraction techniques.

**Step 5: Generate skill files**

Create SKILL.md with workflow, topic-specific resource files as needed, and rubric JSON following skill structure guidelines. Use progressive disclosure pattern. Reference [resources/skill-structure-guidelines.md](resources/skill-structure-guidelines.md) for complete structure requirements, file size limits, naming conventions, and YAML description format.

**Step 6: Validate quality**

Self-assess using `resources/evaluators/rubric_skill_extraction.json`. Check skill-worthiness, distinctness, completeness, clarity, and actionability. Minimum standard: Average score ≥ 3.5 AND no criterion < 3.0. Revise lowest-scoring criteria before delivering.

## Quick Reference

**Reading Strategies:**
- Inspectional reading (skim): [resources/reading-strategies.md](resources/reading-strategies.md#inspectional-reading-skimming)
- Analytical reading (deep): [resources/reading-strategies.md](resources/reading-strategies.md#analytical-reading-deep-reading)
- Multi-file analysis: [resources/reading-strategies.md](resources/reading-strategies.md#multi-file-analysis)

**File-Specific Approaches:**
- Code files: [resources/file-type-strategies.md](resources/file-type-strategies.md#code-files)
- Documentation: [resources/file-type-strategies.md](resources/file-type-strategies.md#documentation-files)
- Notebooks: [resources/file-type-strategies.md](resources/file-type-strategies.md#jupyter-notebooks)
- Config files: [resources/file-type-strategies.md](resources/file-type-strategies.md#configuration-files)
- Data files: [resources/file-type-strategies.md](resources/file-type-strategies.md#data-files)

**Component Extraction:**
- Extraction template: [resources/component-extraction.md](resources/component-extraction.md#extraction-template)
- Mapping to skill structure: [resources/component-extraction.md](resources/component-extraction.md#mapping-components-to-skill-structure)
- Pattern abstraction: [resources/component-extraction.md](resources/component-extraction.md#pattern-abstraction)

**Context Management:**
- External notes pattern: [resources/context-management.md](resources/context-management.md#external-notes-pattern)
- Layered summarization: [resources/context-management.md](resources/context-management.md#layered-summarization)
- Windowing technique: [resources/context-management.md](resources/context-management.md#windowing-for-very-large-files)

**Skill Structure:**
- Complete guidelines: [resources/skill-structure-guidelines.md](resources/skill-structure-guidelines.md)
- YAML description format: [resources/skill-structure-guidelines.md](resources/skill-structure-guidelines.md#yaml-frontmatter)
- File organization: [resources/skill-structure-guidelines.md](resources/skill-structure-guidelines.md#resources-folder-organization)
- File size limits: [resources/skill-structure-guidelines.md](resources/skill-structure-guidelines.md#file-size-limits)

**Quality Validation:**
- Rubric: [resources/evaluators/rubric_skill_extraction.json](resources/evaluators/rubric_skill_extraction.json)

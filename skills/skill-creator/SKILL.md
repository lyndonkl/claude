---
name: skill-creator
description: Transforms documents containing theoretical knowledge or frameworks (PDFs, markdown, book notes, research papers, methodology guides) into actionable, reusable Claude Code skills using systematic reading methodology. Use when user mentions "create a skill from this document", "turn this into a skill", "extract a skill from this file", or when analyzing documents with methodologies, frameworks, or processes that could be made actionable.
---

# Skill Creator

## Table of Contents

- [Workflow](#workflow)
  - [Step 1: Inspectional Reading](#step-1-inspectional-reading)
  - [Step 2: Structural Analysis](#step-2-structural-analysis)
  - [Step 3: Component Extraction](#step-3-component-extraction)
  - [Step 4: Synthesis and Application](#step-4-synthesis-and-application)
  - [Step 5: Skill Construction](#step-5-skill-construction)
  - [Step 6: Validation and Refinement](#step-6-validation-and-refinement)

---

This skill applies Mortimer Adler's systematic reading methodology ("How to Read a Book") through a six-step progressive approach: inspectional reading, structural analysis, component extraction, synthesis, skill construction, and validation. The process is collaborative -- at decision points, options and trade-offs are presented for the user to choose.

**Methodology composition.** Two of the steps are now backed by domain-neutral standalone skills, reusable beyond skill creation:

- Step 1 (Inspectional Reading) — see [`inspectional-reading`](../inspectional-reading/SKILL.md). Invoke with `purpose_context=skill_extraction_from_methodology`. The local resource at `resources/inspectional-reading.md` documents the skill-creation-specific session-initialization and `$SESSION_DIR` mechanics that the generic skill does not own.
- Step 4 (Synthesis and Application) — see [`synthesis-application`](../synthesis-application/SKILL.md). Invoke with `purpose_context=skill_construction`. The local resource at `resources/synthesis-application.md` documents the skill-creation-specific completeness inventory (terms / propositions / arguments / solutions / decision-criteria / triggers) that the generic skill defers to its caller.

The remaining steps (structural analysis, component extraction, skill construction, validation) are still documented inline via local resources only — promote to standalone skills if and when other agents need them.

---

## Workflow

**COPY THIS CHECKLIST** and work through each step:

```
Skill Creation Workflow
- [ ] Step 0: Initialize session workspace
- [ ] Step 1: Inspectional Reading
- [ ] Step 2: Structural Analysis
- [ ] Step 3: Component Extraction
- [ ] Step 4: Synthesis and Application
- [ ] Step 5: Skill Construction
- [ ] Step 6: Validation and Refinement
```

**Step 0: Initialize Session Workspace**

Create working directory and global context file. See [resources/inspectional-reading.md#session-initialization](resources/inspectional-reading.md#session-initialization) for setup commands.

**Step 1: Inspectional Reading**

Skim document systematically, classify type, assess skill-worthiness. Writes to `step-1-output.md`. See [resources/inspectional-reading.md#why-systematic-skimming](resources/inspectional-reading.md#why-systematic-skimming) for skim approach, [resources/inspectional-reading.md#why-document-type-matters](resources/inspectional-reading.md#why-document-type-matters) for classification, [resources/inspectional-reading.md#why-skill-worthiness-check](resources/inspectional-reading.md#why-skill-worthiness-check) for assessment criteria.

**Step 2: Structural Analysis**

Reads `global-context.md` + `step-1-output.md`. Classify content, state unity, enumerate parts, define problems. Writes to `step-2-output.md`. See [resources/structural-analysis.md#why-classify-content](resources/structural-analysis.md#why-classify-content), [resources/structural-analysis.md#why-state-unity](resources/structural-analysis.md#why-state-unity), [resources/structural-analysis.md#why-enumerate-parts](resources/structural-analysis.md#why-enumerate-parts), [resources/structural-analysis.md#why-define-problems](resources/structural-analysis.md#why-define-problems).

**Step 3: Component Extraction**

Reads `global-context.md` + `step-2-output.md`. Choose reading strategy, extract terms/propositions/arguments/solutions section-by-section. Writes to `step-3-output.md`. See [resources/component-extraction.md#why-reading-strategy](resources/component-extraction.md#why-reading-strategy) for strategy selection, [resources/component-extraction.md#section-based-extraction](resources/component-extraction.md#section-based-extraction) for programmatic approach, [resources/component-extraction.md#why-extract-terms](resources/component-extraction.md#why-extract-terms) through [resources/component-extraction.md#why-extract-solutions](resources/component-extraction.md#why-extract-solutions) for what to extract.

**Step 4: Synthesis and Application**

Reads `global-context.md` + `step-3-output.md`. Evaluate completeness, identify applications, transform to actionable steps, define triggers. Writes to `step-4-output.md`. See [resources/synthesis-application.md#why-evaluate-completeness](resources/synthesis-application.md#why-evaluate-completeness), [resources/synthesis-application.md#why-identify-applications](resources/synthesis-application.md#why-identify-applications), [resources/synthesis-application.md#why-transform-to-actions](resources/synthesis-application.md#why-transform-to-actions), [resources/synthesis-application.md#why-define-triggers](resources/synthesis-application.md#why-define-triggers).

**Step 5: Skill Construction**

Reads `global-context.md` + `step-4-output.md`. Determine complexity, plan resources, create SKILL.md and resource files, create rubric. Writes to `step-5-output.md`. See [resources/skill-construction.md#why-complexity-level](resources/skill-construction.md#why-complexity-level), [resources/skill-construction.md#why-plan-resources](resources/skill-construction.md#why-plan-resources), [resources/skill-construction.md#why-skill-md-structure](resources/skill-construction.md#why-skill-md-structure), [resources/skill-construction.md#why-resource-structure](resources/skill-construction.md#why-resource-structure), [resources/skill-construction.md#why-evaluation-rubric](resources/skill-construction.md#why-evaluation-rubric).

**Step 6: Validation and Refinement**

Reads `global-context.md` + `step-5-output.md` + actual skill files. Score using rubric, present analysis, refine based on user decision. Writes to `step-6-output.md`. See [resources/evaluation-rubric.json](resources/evaluation-rubric.json) for criteria.

---

## Notes

- **File-Based Context:** Each step writes output files to avoid context overflow
- **Global Context:** All steps read `global-context.md` for continuity
- **Sequential Dependencies:** Each step reads previous step's output
- **User Collaboration:** Always present findings and get approval at decision points
- **Quality Standards:** Use evaluation rubric (threshold ≥ 3.5) before delivery

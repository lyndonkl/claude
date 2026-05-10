---
name: structural-analysis
description: Domain-neutral methodology for the second level of Adler-style reading - understanding what a document is about *as a whole* and how its parts relate. Classifies content (practical vs theoretical; sequential / categorical / structured / hybrid), states unity in one sentence, enumerates major parts and their organization, and defines the problems the document tries to solve. Reusable across any extraction workflow - skill creation from a methodology document, Pass-2 content grasp on an academic paper, structural review of a long-form document. Use when an agent has done inspectional reading and now needs to map structure before deeper component extraction. Trigger keywords - structural analysis, document structure, state unity, enumerate parts, Adler Level 2, content classification, define problems.
---

# structural-analysis

The second level of Adler's reading methodology. Builds on `inspectional-reading`: now that the document is classified and worth reading further, this skill maps its structure — what it's about as a whole, how the parts relate, what problems it solves.

Invoked autonomously by an agent. The agent reads the document with the structural questions in mind and produces the structured output described below.

## Workflow

```
- [ ] Step 1: Classify content (practical vs theoretical; structure type; completeness 1-5)
- [ ] Step 2: State the unity in one sentence
- [ ] Step 3: Enumerate major parts and identify organizational pattern
- [ ] Step 4: Define the problems the document tries to solve
- [ ] Step 5: Output structured findings
```

Time budget: 20-40 minutes for a typical paper / methodology document. Comes after `inspectional-reading` (Level 1), before component extraction (Level 3).

## Inputs

The calling agent passes:
- `source`: the document
- `inspectional_output`: the structured output from `inspectional-reading` (Level 1) — type classification, structural skeleton, worthiness assessment
- `purpose_context`: what this is being read for (e.g., `paper_pass_2_content_grasp`, `skill_extraction_from_methodology`)
- `domain_hint`: optional

## Output structure

```markdown
## Structural Analysis Output

### Content classification
- Type: {practical | theoretical | hybrid}
- Structure: {sequential | categorical | structured | hybrid}
- Completeness: {1-5} — {one-line rationale}
- Implications: {how this shapes downstream extraction}

### Unity statement
{one sentence using the unity formula below}

Rationale: {why this captures the main point}

### Major parts (enumeration)
1. {Part 1 name} — {what it covers} — {essential | supporting | optional}
2. {Part 2 name} — ...

Organizational pattern: {linear | hub-spoke | layered | modular}
Key relationships: {dependencies; what builds on what}

### Problems
- Main problem: {one sentence on the overarching problem}
- Sub-problems by part: {brief mapping}
- Out of scope: {what this document explicitly does NOT address}
```

## The unity formula

The unity statement is the document's single-sentence "what it is" — your North Star for downstream extraction. Use one of these forms:

**Practical content:** "This {document type} teaches how to {VERB} {OBJECT} by {METHOD} in order to {PURPOSE}."

> Example: "This guide teaches how to conduct user interviews by asking open-ended TEDW-framework questions in order to discover unmet needs and validate assumptions."

**Theoretical content:** "This {document type} explains {PHENOMENON} through {FRAMEWORK} to enable {APPLICATION}."

> Example: "This paper explains cognitive load through information-processing theory to enable instructional designers to build more effective learning materials."

Validate: does it cover the whole document? Is it specific enough to be meaningful? Would the author agree?

## Content classification — quick reference

**Practical vs theoretical:**
- Practical = teaches *how* (action-focused)
- Theoretical = teaches *why* / *what is the case* (understanding-focused)
- Theoretical content needs extra synthesis to become actionable — flag this for the calling agent

**Structure type:**
- Sequential — numbered steps, phases, "before/after" language → extract order, dependencies, decision points
- Categorical — dimensions, types, "aspects of" → extract categories, definitions, relationships
- Structured — fill-in templates, sections to complete → extract template structure
- Hybrid — combines the above → identify boundaries, extract each part by its type

**Completeness 1-5:**
- 5 = complete (covers when/how/what + examples)
- 3-4 = partial, gap-filling needed
- 1-2 = sketchy outline, critical pieces missing — flag for calling agent

## Common patterns

### Pattern A — Skill extraction (call from skill-creator agent)

`purpose_context=skill_extraction_from_methodology`. The unity statement seeds the new skill's `description` field; the parts enumeration suggests workflow steps; the problems become the skill's "when to use" triggers.

### Pattern B — Paper Pass 2 content grasp (call from paper-extractor)

`purpose_context=paper_pass_2_content_grasp`. The unity statement matches the paper's main argument; the parts map to the paper's section structure; the problems frame the Big Question. Pass 2 of `paper-three-pass-extraction` invokes this skill before answering its content-grasp questions.

### Pattern C — Long-form document review

`purpose_context=structural_review`. The agent surfaces structural issues — incoherent unity, parts that don't fit, missing problem definition — for downstream editorial work.

## Guardrails

1. **Don't skip the unity statement.** Without it, downstream extraction has no anchor. If you can't write one, the document is too incoherent for structural analysis — return that finding.
2. **Don't go more than 2 levels deep on parts.** Major parts + subsections is enough. Three levels of nesting belongs in component extraction (Level 3), not here.
3. **Classify against evidence.** If you classify "sequential" but the TOC has no numbered steps and no temporal markers, you've inferred more than the structure shows.
4. **Out-of-scope problems matter.** Documenting what the source does NOT address prevents downstream agents from over-extracting.

## Related

- [`inspectional-reading`](../inspectional-reading/SKILL.md) — Level 1, run before this. Provides the classification + structural skeleton this skill builds on.
- [`component-extraction`](../component-extraction/SKILL.md) — Level 3, run after this. Operates on the parts this skill enumerated.
- [`synthesis-application`](../synthesis-application/SKILL.md) — Level 4, evaluates the extracted components for completeness + logic.
- [`paper-three-pass-extraction`](../paper-three-pass-extraction/SKILL.md) invokes this skill in Pass 2.
- The skill-creator skill at `skills/skill-creator/SKILL.md` invokes this skill as its Step 2.

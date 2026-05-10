---
name: skill-construction
description: Methodology for building a properly structured Claude Code skill (SKILL.md + optional resources + evaluation rubric) from extracted components. Assesses complexity (Level 1 simple - SKILL.md only; Level 2 moderate - SKILL.md plus 1-3 resources; Level 3 complex - SKILL.md plus 4-8 resources), plans the resource grouping, drafts SKILL.md following Anthropic's authoring best practices (concise frontmatter with what + when triggers, body under 500 lines, progressive disclosure to resource files one level deep, workflow checklists), and constructs an evaluation rubric. Use when extracted components and a synthesis verdict are in hand and the next step is to materialize them as a skill. Trigger keywords - construct skill, build SKILL.md, skill construction, skill scaffolding, generate skill files.
---

# skill-construction

Builds a Claude Code skill (the `SKILL.md` file plus any resource files and the evaluation rubric) from a structured set of extracted components and a synthesis verdict. The penultimate step in the skill-creator workflow.

The skill is invoked by the calling agent (typically the `skill-creator` agent) once `synthesis-application` has produced a GO or GO_WITH_GAPS verdict on the extracted components. NO_GO sends the agent back upstream.

## Workflow

```
- [ ] Step 1: Assess complexity level (1-3) from extracted content volume
- [ ] Step 2: Plan resource files (or decide SKILL.md alone is enough)
- [ ] Step 3: Draft SKILL.md frontmatter (name, description, triggers)
- [ ] Step 4: Draft SKILL.md body (workflow checklist, key patterns, guardrails)
- [ ] Step 5: Draft each resource file (focused topic, < 500 lines, WHY/WHAT structure)
- [ ] Step 6: Construct an evaluation rubric (10 criteria, 1-5 scale)
- [ ] Step 7: Output the constructed skill files
```

## Inputs

- `extracted_components`: structured terms / propositions / arguments / solutions from `component-extraction`
- `synthesis_output`: the GO / GO_WITH_GAPS verdict from `synthesis-application` plus its gap-fill recommendations
- `target_dir`: where the skill should be written (typically `skills/{skill-name}/`)
- `purpose_context`: e.g., `skill_extraction_from_methodology` (the standard case)

## Complexity levels

Match structure to content volume. Don't over-engineer; don't under-engineer.

| Level | Steps in workflow | Estimated lines total | Structure                              |
| ----- | ------------------ | --------------------- | -------------------------------------- |
| 1     | 3-5                | < 300                 | SKILL.md + rubric only                 |
| 2     | 5-8                | 300-800               | SKILL.md + 1-3 resource files + rubric |
| 3     | 8+                 | 800+                  | SKILL.md + 4-8 resource files + rubric |

Decide based on:
- Total workflow steps the methodology has
- Major decision points (each typically warrants a section)
- Number of distinct concepts that need explanation
- Examples needed (more examples → more lines → likely Level 2 or 3)

## SKILL.md structure (always required)

YAML frontmatter:
- `name`: lowercase-hyphens, ≤64 chars, no XML, no reserved words ("anthropic", "claude")
- `description`: third-person, both *what the skill does* AND *when to use it*, including trigger keywords. ≤1024 chars. This is the discovery surface — Claude uses it to decide whether to invoke the skill.

Body sections (typical order):
- `# {Skill Name}` — title + one-paragraph framing
- `## Workflow` — checklist the calling agent can copy
- `## {Domain-specific sections}` — patterns, decision logic, key concepts
- `## Common patterns` — 2-4 named patterns with usage context
- `## Guardrails` — must-nots and anti-patterns
- `## Related` — pointers to adjacent skills (one level deep only)

## Resource file structure (Level 2 and 3)

Each resource file:
- Focused on one cohesive topic (don't sprawl)
- < 500 lines
- Cross-referenced from SKILL.md as a one-level-deep link
- Follows a `## Why X` then `## What to do` structure (the WHY activates context; the WHAT gives concrete instructions)

Two grouping approaches:
- **By workflow step** (best for complex skills) — one resource file per major step, named for the step
- **By topic** (best for moderate skills) — `key-concepts.md`, `decision-framework.md`, `examples.md`

## Evaluation rubric

Always include `resources/evaluators/rubric_{skill_name}.json`. 10 criteria, each scored 1-5. Common criteria:

1. Description specificity (third person, what + when, triggers)
2. Workflow completeness (all major steps captured)
3. Pattern coverage (common cases addressed)
4. Guardrail clarity (must-nots are concrete)
5. Example quality (examples are concrete, not abstract)
6. Resource organization (files focused, one-level-deep links)
7. Token efficiency (no over-explanation; assumes Claude is smart)
8. Consistency (terminology stable; format matches across sections)
9. Triggers explicit (key phrases listed in description)
10. Tested (at least one real-world test case considered)

Target average ≥ 3.5 before shipping.

## Output structure

```markdown
## Skill Construction Output

### Complexity assessment
Level: {1 | 2 | 3}
Rationale: {1-2 sentences}
Structure: {file list}

### Files created
- {target_dir}/SKILL.md ({line count} lines)
- {target_dir}/resources/{file}.md ({line count} lines) — {topic}
- ...
- {target_dir}/resources/evaluators/rubric_{name}.json (10 criteria)

### Self-evaluation against the rubric
- Average score: {X / 5}
- Below-3 criteria: {list}
- Recommended next-pass focus: {1-2 specific improvements}

### Gaps from upstream synthesis-application
{If the synthesis verdict was GO_WITH_GAPS, restate the gap list and how the construction addressed each (filled / deferred / surfaced as a TODO in the SKILL).}
```

## Anchoring against authoring best practices

Conform to Anthropic's [agent skills authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

- **Concise is key.** Only add context Claude doesn't already have. Challenge each piece: "does Claude need this explanation?"
- **Set appropriate degrees of freedom.** High freedom (text instructions) for judgment calls; low freedom (specific scripts) for fragile procedures.
- **Keep references one level deep.** SKILL.md links directly to resource files; resources don't link to other resources.
- **Workflow checklists for complex tasks.** Calling agent can copy and check off as it progresses.
- **Feedback loops.** Validator → fix errors → repeat.
- **Avoid Windows-style paths.** Forward slashes always.
- **Avoid offering too many options.** One default with an escape hatch beats five alternatives.
- **MCP tools use fully qualified names.** `ServerName:tool_name`.

## Common patterns

### Pattern A — From a methodology document (the standard skill-creation case)

The extracted components come from a methodology guide or framework doc. Workflow steps in SKILL.md mirror the methodology's steps. Resources cover decision logic, examples, and templates.

### Pattern B — From a research paper

Less common but valid. The extraction yields propositions and arguments more than steps. SKILL.md becomes a "how to apply this paper's framework to a downstream task" guide. Resources cover the paper's framework and worked examples.

### Pattern C — Refactoring an existing skill

The "extracted components" come from an existing skill that's grown too large or has overlap with another. The construction step writes a leaner version, deferring resources to focused files.

## Guardrails

1. **Don't construct without a GO verdict.** If `synthesis-application` returned NO_GO, return upstream — building a skill from incomplete components is wasted work.
2. **Don't exceed 500 lines in SKILL.md body.** Push depth into resource files.
3. **Don't skip the rubric.** Self-evaluation gates ship-readiness; without a rubric there's no objective standard.
4. **Don't over-engineer.** A 3-step methodology is Level 1 — don't build it as Level 3 because resources feel "more professional."
5. **Don't use Anthropic's reserved words in `name`.** "claude", "anthropic" — silently breaks discovery.
6. **Don't claim test coverage you don't have.** The rubric's "Tested" criterion is a real check; mark it 1 if no test scenario was considered.

## Related

- [`component-extraction`](../component-extraction/SKILL.md) — produces the input this skill consumes.
- [`synthesis-application`](../synthesis-application/SKILL.md) — runs immediately before this skill; its GO / GO_WITH_GAPS / NO_GO verdict gates this skill's invocation.
- [`evaluation-rubrics`](../evaluation-rubrics/SKILL.md) — the rubric construction in this skill's Step 6 mirrors the rubric design patterns there.
- The skill-creator skill at `skills/skill-creator/SKILL.md` invokes this skill as its Step 5.

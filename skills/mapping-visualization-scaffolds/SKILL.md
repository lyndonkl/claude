---
name: mapping-visualization-scaffolds
description: Creates visual maps that make implicit relationships, dependencies, and structures explicit through diagrams, concept maps, and architectural blueprints. Guides through identifying nodes and relationships, choosing visualization approaches, and validating completeness. Use when complex systems need visual documentation, mapping component relationships and dependencies, creating hierarchies or taxonomies, documenting process flows or decision trees, understanding system architectures, visualizing data lineage or knowledge structures, or when user mentions concept maps, system diagrams, dependency mapping, relationship visualization, or architecture blueprints.
---

# Mapping & Visualization Scaffolds

## Table of Contents
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Workflow

Copy this checklist and track your progress:

```
Mapping Visualization Progress:
- [ ] Step 1: Clarify mapping purpose
- [ ] Step 2: Identify nodes and relationships
- [ ] Step 3: Choose visualization approach
- [ ] Step 4: Create the map
- [ ] Step 5: Validate and refine
```

**Step 1: Clarify mapping purpose**

Ask user about their goal: What system/concept needs mapping? Who's the audience? What decisions will this inform? What level of detail is needed? See [Common Patterns](#common-patterns) for typical use cases.

**Step 2: Identify nodes and relationships**

List all key elements (nodes) and their connections (relationships). Identify hierarchy levels, dependency types, and grouping criteria. For simple cases (< 20 nodes), use [resources/template.md](resources/template.md). For complex systems (50+ nodes) or collaborative sessions, see [resources/methodology.md](resources/methodology.md) for advanced strategies.

**Step 3: Choose visualization approach**

Select format based on complexity: Simple lists for < 10 nodes, tree diagrams for hierarchies, network graphs for complex relationships, or layered diagrams for systems. For large-scale systems or multi-map hierarchies, consult [resources/methodology.md](resources/methodology.md) for mapping strategies and tool selection. See [Common Patterns](#common-patterns) for guidance.

**Step 4: Create the map**

Build the visualization using markdown, ASCII diagrams, or structured text. Start with high-level structure, then add details. Include legend if needed. Use [resources/template.md](resources/template.md) as your scaffold.

**Step 5: Validate and refine**

Check completeness, clarity, and accuracy using [resources/evaluators/rubric_mapping_visualization_scaffolds.json](resources/evaluators/rubric_mapping_visualization_scaffolds.json). Ensure all critical nodes and relationships are present. Minimum standard: Score ≥ 3.5 average.

## Common Patterns

**Architecture Diagrams:**
- System components as nodes
- Service calls/data flows as relationships
- Layers as groupings (frontend, backend, data)
- Use for: Technical documentation, system design reviews

**Concept Maps:**
- Concepts/ideas as nodes
- "is-a", "has-a", "leads-to" as relationships
- Themes as groupings
- Use for: Learning, knowledge organization, research synthesis

**Dependency Graphs:**
- Tasks/features/modules as nodes
- "depends-on", "blocks", "requires" as relationships
- Phases/sprints as groupings
- Use for: Project planning, risk assessment, parallel work identification

**Hierarchies & Taxonomies:**
- Categories/classes as nodes
- Parent-child relationships
- Levels as groupings (L1, L2, L3)
- Use for: Information architecture, org charts, skill trees

**Flow Diagrams:**
- Steps/states as nodes
- Transitions/decisions as relationships
- Swim lanes as groupings (roles, systems)
- Use for: Process documentation, user journeys, decision trees

## Guardrails

**Scope Management:**
- Focus on relationships that matter for the specific purpose
- Don't map everything—map what's decision-relevant
- Stop at appropriate detail level (usually 3-4 layers deep)
- For systems with > 50 nodes, create multiple focused maps

**Clarity Over Completeness:**
- Prioritize understandability over exhaustiveness
- Use consistent notation and naming
- Add legend if > 3 relationship types
- Group related nodes to reduce visual complexity

**Validation:**
- Verify accuracy with subject matter experts
- Test if someone unfamiliar can understand the map
- Check for missing critical relationships
- Ensure directionality is clear (A → B vs A ← B)

**Common Pitfalls:**
- ❌ Creating "hairball" diagrams with too many connections
- ❌ Mixing abstraction levels (strategic + implementation details)
- ❌ Using inconsistent node/relationship representations
- ❌ Forgetting to state the map's purpose and scope

## Quick Reference

**Resources:**
- `resources/template.md` - Structured scaffold for creating maps
- `resources/evaluators/rubric_mapping_visualization_scaffolds.json` - Quality criteria

**Output:**
- File: `mapping-visualization-scaffolds.md` in current directory
- Contains: Nodes, relationships, groupings, legend (if needed)
- Format: Markdown with ASCII diagrams or structured lists

**Success Criteria:**
- All critical nodes identified
- Relationships clearly labeled with directionality
- Appropriate grouping/layering applied
- Understandable by target audience without explanation
- Validated against quality rubric (score ≥ 3.5)

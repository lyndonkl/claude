# Mapping & Visualization Scaffolds Template

## Workflow

Copy this checklist and track your progress:

```
Template Progress:
- [ ] Step 1: Define map metadata
- [ ] Step 2: List all nodes
- [ ] Step 3: Define relationships
- [ ] Step 4: Choose visualization format
- [ ] Step 5: Create the visualization
- [ ] Step 6: Add legend and insights
```

**Step 1: Define map metadata**

Fill out the Map Metadata section in the Quick Template with title, purpose, audience, and scope. This ensures the map serves the right goal. See [Section Guidance - Map Metadata](#1-map-metadata) for details.

**Step 2: List all nodes**

Complete the Nodes section in the Quick Template with all key elements (components, concepts, entities). Include brief descriptions. See [Section Guidance - Nodes](#2-nodes) for what to include.

**Step 3: Define relationships**

Document the Relationships section in the Quick Template with connections between nodes. Specify type and directionality. See [Section Guidance - Relationships](#3-relationships) for relationship types.

**Step 4: Choose visualization format**

Select from [Visualization Formats](#visualization-formats): List, Tree, Graph, or Layered based on complexity and relationship patterns. See [Format Selection Guide](#format-selection-guide).

**Step 5: Create the visualization**

Build the Visualization section in the Quick Template using your chosen format. Start with high-level structure, then add details. See [Visualization Formats](#visualization-formats) for examples.

**Step 6: Add legend and insights**

Complete the Legend and Insights sections in the Quick Template if needed, documenting discoveries from mapping. See [Quality Checklist](#quality-checklist) before finalizing.

---

## Quick Template

Copy this structure to `mapping-visualization-scaffolds.md`:

```markdown
# [Map Title]

## Map Metadata

**Purpose:** [Why this map exists, what decisions it informs]
**Audience:** [Who will use this map]
**Scope:** [What's included/excluded]
**Date:** [YYYY-MM-DD]
**Author:** [Name or team]

## Nodes

List all key elements:

| Node ID | Name | Type | Description |
|---------|------|------|-------------|
| N1 | [Node name] | [Component/Concept/Person/Step] | [Brief description] |
| N2 | [Node name] | [Type] | [Brief description] |
| N3 | [Node name] | [Type] | [Brief description] |

## Relationships

Define connections between nodes:

| From | To | Relationship Type | Description |
|------|-----|-------------------|-------------|
| N1 | N2 | [depends-on/calls/contains/leads-to] | [Details about this connection] |
| N2 | N3 | [Type] | [Details] |

## Groupings/Layers

Organize nodes into logical groups:

- **[Group 1 Name]:** N1, N2
- **[Group 2 Name]:** N3, N4
- **[Group 3 Name]:** N5, N6

## Visualization

[Insert your map using chosen format - see options below]

## Legend

**Node Types:**
- [Symbol/Color] = [Type]

**Relationship Types:**
- → = [Meaning]
- ⇒ = [Meaning]
- ↔ = [Meaning]

## Insights and Observations

**Key Findings:**
- [Important discovery from mapping]
- [Unexpected dependency or pattern]
- [Critical path or bottleneck]

**Recommendations:**
- [Action based on map insights]

**Limitations:**
- [What's not captured in this map]
- [Known gaps or uncertainties]
```

---

## Visualization Formats

### Format 1: Simple List (< 10 nodes, simple relationships)

```
API Gateway
├─→ Auth Service
│   └─→ User Database
├─→ Product Service
│   ├─→ Product Database
│   └─→ Cache Layer
└─→ Payment Service
    └─→ Payment Database
```

**When to use:** Linear flows, simple hierarchies, few cross-dependencies

### Format 2: Tree Diagram (hierarchical relationships)

```
                    Application
                        |
        ┌──────────────┼──────────────┐
        |              |              |
    Frontend       Backend         Data
        |              |              |
    ┌───┴───┐      ┌───┴───┐      ┌───┴───┐
   UI  Auth     API  Logic    DB  Cache
```

**When to use:** Org charts, taxonomies, clear parent-child relationships

### Format 3: Network Graph (complex interconnections)

```
    ┌─────────┐
    │  User   │
    └────┬────┘
         │
    ┌────▼────┐     ┌──────────┐
    │  Auth   │────→│  Logs    │
    └────┬────┘     └──────────┘
         │
    ┌────▼────┐     ┌──────────┐
    │ Service │────→│ Database │
    └────┬────┘     └──────────┘
         │              ▲
         │              │
    ┌────▼────┐         │
    │  Cache  │─────────┘
    └─────────┘
```

**When to use:** Microservices, complex dependencies, bi-directional relationships

### Format 4: Layered Diagram (system architecture)

```
┌─────────────────────────────────────────────┐
│  Presentation Layer                         │
│  [Web UI]  [Mobile App]  [API Docs]        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Business Logic Layer                       │
│  [Auth] [Users] [Products] [Payments]      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Data Layer                                 │
│  [PostgreSQL]  [Redis]  [S3]               │
└─────────────────────────────────────────────┘
```

**When to use:** System architectures, layered designs, clear abstraction levels

### Format 5: Swimlane/Matrix (responsibilities, workflows)

```
| Step | Frontend | Backend | Database | External |
|------|----------|---------|----------|----------|
| 1. Request | Send login | - | - | - |
| 2. Validate | - | Check credentials | Query users | - |
| 3. Token | - | Generate JWT | - | - |
| 4. Store | Receive token | - | Update session | Log event |
| 5. Redirect | Show dashboard | - | - | - |
```

**When to use:** Process flows with multiple actors, workflow documentation

---

## Format Selection Guide

**Choose based on:**

| Characteristic | Recommended Format |
|----------------|-------------------|
| < 10 nodes, linear flow | Simple List |
| Clear hierarchy, one parent per child | Tree Diagram |
| Many cross-dependencies, cycles | Network Graph |
| Multiple abstraction layers | Layered Diagram |
| Multiple actors/systems in process | Swimlane/Matrix |
| Time-based sequence | Swimlane or Simple List |
| Spatial/geographic relationships | Custom diagram with coordinates |

**Complexity thresholds:**
- **10-20 nodes:** Use grouping and colors
- **20-50 nodes:** Create multiple focused maps or use layered approach
- **50+ nodes:** Definitely split into multiple maps

---

## Section Guidance

### 1. Map Metadata

**Purpose:** Be specific about the map's goal
- ✓ "Understand microservices dependencies to identify deployment risks"
- ✗ "Show system architecture"

**Audience:** Tailor detail level to reader
- Technical team: Include implementation details
- Executives: Focus on high-level components and costs
- New team members: Add more context and explanations

**Scope:** Explicitly state boundaries
- "Includes all production services; excludes development tools"
- "Shows user-facing journey; excludes backend processing"
- "Maps current state as of 2024-Q4; does not include planned features"

### 2. Nodes

**What to include:**
- **ID**: Short identifier (N1, N2, or descriptive like "AUTH")
- **Name**: Clear, consistent naming (same conventions throughout)
- **Type**: Component, Concept, Person, Step, System, etc.
- **Description**: Brief (< 20 words) explanation of purpose or role

**Naming conventions:**
- Use consistent casing (PascalCase, snake_case, or kebab-case)
- Be specific: "User Authentication Service" not just "Auth"
- Avoid acronyms unless universally understood

**Examples:**
```
N1 | API Gateway | Service | Routes external requests to internal services
N2 | Auth Service | Service | Validates user credentials and generates JWTs
N3 | User DB | Data Store | PostgreSQL database storing user profiles
```

### 3. Relationships

**Common relationship types:**

**Dependency relationships:**
- `depends-on` - A needs B to function
- `requires` - A cannot start without B
- `blocks` - A prevents B from proceeding
- `enables` - A makes B possible

**Data relationships:**
- `reads-from` - A consumes data from B
- `writes-to` - A modifies data in B
- `sends-to` - A transmits messages/events to B
- `receives-from` - A gets messages/events from B

**Structural relationships:**
- `contains` / `part-of` - Hierarchical containment
- `is-a` / `extends` - Type relationships
- `implements` - Interface implementation
- `uses` / `calls` - Service invocation

**Process relationships:**
- `leads-to` / `follows` - Sequential steps
- `triggers` - Event causation
- `approves` / `rejects` - Decision flows
- `escalates-to` - Authority chain

**Specify directionality:**
- Use clear arrows: A → B (A to B)
- Note bi-directional: A ↔ B
- Include cardinality if relevant: A →[1:N]→ B

### 4. Groupings/Layers

**When to group:**
- Logical subsystems (Frontend, Backend, Data)
- Organizational boundaries (Team A, Team B)
- Phases or stages (Planning, Execution, Review)
- Environments (Dev, Staging, Production)
- Abstraction levels (Strategic, Tactical, Operational)

**Grouping strategies:**
- **By function**: All authentication-related nodes
- **By owner**: All nodes maintained by Team X
- **By layer**: All presentation-layer nodes
- **By lifecycle**: All legacy vs. new nodes
- **By criticality**: Core vs. optional nodes

## Quality Checklist

Before finalizing your map, verify:

**Completeness:**
- [ ] All critical nodes identified
- [ ] All significant relationships documented
- [ ] Groupings clearly labeled
- [ ] Legend provided if > 3 relationship types

**Clarity:**
- [ ] Consistent naming conventions
- [ ] Clear directionality on relationships
- [ ] Appropriate level of detail for audience
- [ ] No overlapping or ambiguous connections

**Accuracy:**
- [ ] Relationships verified with SMEs or documentation
- [ ] Current state (not outdated)
- [ ] No missing critical dependencies
- [ ] Scope boundaries clearly stated

**Usability:**
- [ ] Can target audience understand without explanation?
- [ ] Is the visualization scannable (not a "hairball")?
- [ ] Are insights or key findings highlighted?
- [ ] Is next action or decision clear?

**Technical:**
- [ ] File saved as `mapping-visualization-scaffolds.md`
- [ ] Markdown formatting correct
- [ ] Links and references work
- [ ] Version/date included

---

## Common Patterns by Domain

**Software Architecture:**
- Nodes: Services, databases, message queues, APIs
- Relationships: Calls, reads/writes, publishes/subscribes
- Groupings: Layers (presentation, business, data)

**Knowledge/Concept Mapping:**
- Nodes: Concepts, theories, terms, examples
- Relationships: Is-a, has-a, leads-to, contradicts
- Groupings: Themes, disciplines, abstraction levels

**Project Planning:**
- Nodes: Tasks, milestones, deliverables
- Relationships: Depends-on, blocks, follows
- Groupings: Phases, sprints, teams

**Organizational:**
- Nodes: People, teams, roles, functions
- Relationships: Reports-to, collaborates-with, approves
- Groupings: Departments, locations, levels

**Process/Workflow:**
- Nodes: Steps, decisions, handoffs
- Relationships: Leads-to, triggers, approves/rejects
- Groupings: Swimlanes (actors), phases

---

## Tips for Effective Maps

**Start Simple:**
1. Begin with 5-10 most important nodes
2. Add critical relationships only
3. Expand if needed, but resist over-complication

**Use Visual Hierarchy:**
- Size: Larger nodes = more important
- Position: Top = start, Bottom = end (for flows)
- Grouping: Visual proximity = logical grouping

**Iterate:**
- Create draft, get feedback, refine
- Test understanding with someone unfamiliar
- Simplify based on confusion points

**Know When to Split:**
- If map has > 30 nodes, consider multiple maps
- Create one high-level overview + detailed sub-maps
- Link related maps together

**Common Improvements:**
- Add color coding for node types
- Use different line styles for relationship types
- Include metrics or attributes on nodes (e.g., latency, importance)
- Highlight critical paths or bottlenecks

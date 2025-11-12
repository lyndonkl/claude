# Advanced Mapping & Visualization Methodology

## Workflow

Copy this checklist and track your progress:

```
Advanced Mapping Progress:
- [ ] Step 1: Assess complexity and scope
- [ ] Step 2: Choose mapping strategy
- [ ] Step 3: Select tools and formats
- [ ] Step 4: Execute mapping process
- [ ] Step 5: Validate with stakeholders
- [ ] Step 6: Iterate and refine
```

**Step 1: Assess complexity and scope**

Evaluate system size (nodes/relationships), stakeholder diversity, and update frequency. See [1. Complexity Assessment](#1-complexity-assessment) for decision criteria on when advanced techniques are needed.

**Step 2: Choose mapping strategy**

Select from single comprehensive map, multi-map hierarchy, or modular view-based approach based on complexity. See [2. Mapping Strategies for Scale](#2-mapping-strategies-for-scale) for guidance.

**Step 3: Select tools and formats**

Choose between manual (text/markdown), semi-automated (Mermaid), or visual tools (draw.io, GraphViz) based on collaboration needs and update frequency. See [3. Tool Selection](#3-tool-selection) for criteria.

**Step 4: Execute mapping process**

Apply chosen strategy using collaborative or individual workflows. See [4. Execution Patterns](#4-execution-patterns) for facilitation techniques and [5. Advanced Layout Techniques](#5-advanced-layout-techniques) for optimization.

**Step 5: Validate with stakeholders**

Conduct structured review sessions using [6. Validation Approaches](#6-validation-approaches) to ensure accuracy and completeness.

**Step 6: Iterate and refine**

Incorporate feedback and maintain maps over time using [7. Maintenance and Evolution](#7-maintenance-and-evolution) patterns.

---

## 1. Complexity Assessment

Use this framework to determine if advanced methodology is needed:

### Simple Case (Use template.md)
- **Nodes**: < 20
- **Relationships**: Mostly one type
- **Stakeholders**: 1-2 people
- **Change frequency**: One-time or rare
- **Structure**: Clear hierarchy or simple network
→ **Action**: Follow [template.md](template.md), use Simple List or Tree format

### Moderate Case (Consider this methodology)
- **Nodes**: 20-50
- **Relationships**: 2-4 types
- **Stakeholders**: 3-8 people
- **Change frequency**: Quarterly updates
- **Structure**: Some cross-dependencies, multiple layers
→ **Action**: Use this methodology, focus on [Multi-Map Hierarchy](#multi-map-hierarchy)

### Complex Case (Definitely use this methodology)
- **Nodes**: 50-200+
- **Relationships**: 5+ types, bidirectional
- **Stakeholders**: 10+ people across teams/orgs
- **Change frequency**: Continuous evolution
- **Structure**: Dense interconnections, emergent properties
→ **Action**: Use this methodology, apply [Modular View-Based](#modular-view-based-approach) approach

### Signals You Need Advanced Techniques
- Creating "hairball" diagrams with crossing edges everywhere
- Stakeholders can't find relevant information in map
- Map becomes outdated within weeks
- Multiple teams need different views of same system
- Need to show evolution over time
- System has 100+ nodes that can't be easily decomposed

---

## 2. Mapping Strategies for Scale

### Single Comprehensive Map

**When to use:**
- 20-50 nodes maximum
- Single primary use case
- Stable system (low change rate)
- Uniform stakeholder audience

**Techniques:**
- Use aggressive grouping/layering to reduce visual complexity
- Apply color coding consistently (by type, criticality, ownership)
- Maximize whitespace between groups
- Create clear visual hierarchy (size, position, color)

**Example structure:**
```
┌─── Frontend Layer ────────────────────┐
│  UI Components (N1-N5)                │
│  State Management (N6-N8)             │
└───────────────────────────────────────┘
            ↓ API calls
┌─── Backend Layer ─────────────────────┐
│  Services (N9-N15)                    │
│  Business Logic (N16-N20)             │
└───────────────────────────────────────┘
            ↓ queries
┌─── Data Layer ────────────────────────┐
│  Databases (N21-N25)                  │
└───────────────────────────────────────┘
```

### Multi-Map Hierarchy

**When to use:**
- 50-150 nodes
- Multiple abstraction levels needed
- Different audiences need different detail
- System has natural subsystem boundaries

**Structure:**
1. **L0 Overview Map** (5-15 nodes): High-level components only
2. **L1 Subsystem Maps** (10-30 nodes each): Detail within each component
3. **L2 Detail Maps** (optional): Deep dive into complex subsystems

**Linking approach:**
- Each L0 node links to its L1 detail map
- Use consistent naming: `system-overview.md`, `system-auth-subsystem.md`, `system-payment-subsystem.md`
- Include navigation breadcrumbs in each map

**Example hierarchy:**
```
L0: E-commerce Platform Overview
├─ Frontend (5 nodes) → L1: frontend-detail.md
├─ API Gateway (3 nodes) → L1: api-gateway-detail.md
├─ Auth Service (4 nodes) → L1: auth-service-detail.md
│  └─ JWT Module → L2: auth-jwt-detail.md
├─ Product Service (8 nodes) → L1: product-service-detail.md
├─ Payment Service (6 nodes) → L1: payment-service-detail.md
└─ Data Layer (4 nodes) → L1: data-layer-detail.md
```

### Modular View-Based Approach

**When to use:**
- 100+ nodes
- Multiple stakeholder groups with different concerns
- Need to show different perspectives of same system
- High change frequency

**View types:**
- **Structural view**: What components exist and how they're organized
- **Dependency view**: What depends on what (for deployment planning)
- **Data flow view**: How data moves through system
- **Security view**: Trust boundaries, authentication flows
- **Operational view**: Monitoring, alerting, ownership

**Approach:**
1. Maintain single **master node/relationship database** (spreadsheet or JSON)
2. Generate **filtered views** for specific audiences/purposes
3. Each view shows subset of nodes/relationships relevant to that concern
4. Cross-reference between views using node IDs

**Example - same system, different views:**

**View 1: Engineering Deployment Dependencies**
```
Shows: All services, databases, external APIs
Relationships: depends-on, requires, blocks
Purpose: Determine deployment order, identify risks
```

**View 2: Product Manager Feature Map**
```
Shows: User-facing features, backend services supporting them
Relationships: enables, requires, affects
Purpose: Understand feature scope, plan releases
```

**View 3: Security Boundaries**
```
Shows: Services, trust zones, auth components
Relationships: trusts, authenticates, authorizes
Purpose: Threat modeling, compliance review
```

---

## 3. Tool Selection

### Tool Selection Guide

**Text/Markdown:** Quick docs, frequent updates, < 20 nodes, version control critical
**Mermaid:** 20-40 nodes, markdown integration, flowcharts, version control
**Draw.io:** 40+ nodes, visual quality matters, presentations, collaborative editing
**GraphViz:** Automatic layout, 100+ nodes, programmatic generation
**Specialized (Lucidchart, etc):** Enterprise collaboration, executive presentations, branded templates

---

## 4. Execution Patterns

### Solo Mapping Workflow

**5-step process for 30-50 node maps (70-120 min total):**

1. **Brain dump** (15-30 min): List all nodes without structure, aim for exhaustiveness
2. **Cluster** (10-15 min): Group related nodes, identify subsystems/themes
3. **Structure** (20-40 min): Choose format, define relationships, create layers
4. **Refine** (15-20 min): Add missing nodes, remove redundancy, clarify relationships
5. **Validate** (10-15 min): Self-check with [rubric](evaluators/rubric_mapping_visualization_scaffolds.json), test understanding

### Collaborative Mapping Workshop

**5-phase process for 2-8 participants (80 min total):**

1. **Setup** (5 min): State purpose/scope, show example, assign roles (Facilitator, Scribe, Timekeeper)
2. **Individual brainstorm** (10 min): Each person lists 15-20 nodes on sticky notes, no discussion
3. **Share and cluster** (20 min): Share nodes (2 min each), group similar, merge duplicates, name clusters
4. **Relationship mapping** (20 min): Draw key relationships, use colors for types, vote on disputed connections
5. **Structure and refine** (15 min): Choose format together, assign digital creation, document parking lot
6. **Review and validate** (10 min): Walk through map, identify gaps, assign follow-up owners

**Facilitation tips:** Round-robin participation, park tangents, enforce timeboxes, capture dissent explicitly

---

## 5. Advanced Layout Techniques

### Minimizing Edge Crossings

**Problem:** Complex graphs become "hairballs" with edges crossing everywhere.

**Solutions:**

1. **Layered approach** (works for hierarchies)
   - Assign nodes to horizontal layers (L1, L2, L3)
   - Minimize crossings between adjacent layers
   - Use dummy nodes for long-distance edges

2. **Force-directed layout** (works for networks)
   - Related nodes pull together
   - Unrelated nodes push apart
   - Let GraphViz or similar tool calculate

3. **Manual optimization**
   - Place highly-connected nodes centrally
   - Group tightly-coupled nodes
   - Use orthogonal routing (edges follow grid)

4. **Split the map**
   - If > 30 edge crossings, split into multiple maps
   - One map per subsystem
   - Create overview map showing subsystem relationships

### Handling Bidirectional Relationships

**Problem:** A ↔ B creates visual clutter with two arrows.

**Solutions:**

1. **Single line with double arrow**: `A ←→ B`
2. **Annotate relationship**: `A ←[reads/writes]→ B`
3. **Split by type**:
   - Show `A → B` for "calls"
   - Show `B → A` for "sends events"
4. **Separate views**: One for each direction

### Visual Hierarchy Patterns

**Use visual weight to show importance:**

```
Size:
  ┌────────────┐     ← Critical component (large)
  │  Database  │
  └────────────┘

  ┌────────┐         ← Standard component (medium)
  │ Service │
  └────────┘

  ┌────┐             ← Utility (small)
  │Util│
  └────┘

Color/Style:
  ██████ Core system (solid, dark)
  ▓▓▓▓▓▓ Standard (solid, medium)
  ░░░░░░ Optional (light/dotted)

Position:
  Top → High-level/strategic
  Middle → Tactical
  Bottom → Implementation details
```

---

## 6. Validation Approaches

### Structured Review Process

**Step 1: Completeness check (5-10 min)**
Ask reviewers:
- "What critical components are missing?"
- "What relationships are incorrect or missing?"
- "What groupings don't make sense?"

**Step 2: Accuracy verification (10-15 min)**
For each subsystem:
- Assign subject matter expert
- Verify node descriptions
- Validate relationship types and directionality
- Confirm groupings

**Step 3: Usability test (5 min)**
Give map to someone unfamiliar:
- Can they answer basic questions from the map?
- "Which components depend on X?"
- "What happens if Y fails?"
- "Who owns component Z?"

**Step 4: Scenario walkthrough (10-15 min)**
Pick 3-5 scenarios:
- "A user logs in" - trace through the map
- "We deploy service X" - identify impacts
- "Database Y goes down" - find affected components

### Validation Metrics

Track these across iterations:

- **Coverage**: % of known components included
- **Accuracy**: % of relationships verified by SMEs
- **Usability**: # of correct answers in usability test
- **Completeness**: # of gaps identified in reviews
- **Consensus**: % of stakeholders agreeing on structure

**Target thresholds:**
- Coverage ≥ 95% (all critical + most secondary)
- Accuracy ≥ 90% (verified by SMEs)
- Usability ≥ 70% (most questions answered correctly)

---

## 7. Maintenance and Evolution

### Update Strategies

**Reactive (as-needed):**
- Update when someone reports inaccuracy
- Quarterly review cycle
- Works for stable systems
- **Risk**: Map becomes stale, people stop trusting it

**Proactive (systematic):**
- Assign ownership to specific people/teams
- Integrate into change processes (new service → update map)
- Automated checks (compare with service registry, org chart)
- **Benefit**: Map stays current, becomes trusted resource

### Version Control Patterns

**For text-based maps (Markdown, Mermaid):**
- Store in Git alongside code
- Include map updates in PRs that change architecture
- Use conventional commits: `docs(map): add new payment service`
- Tag versions: `v1.0-system-map-2024Q4`

**For visual tools (Draw.io, Lucidchart):**
- Export to version control (XML, JSON) regularly
- Maintain changelog in separate document
- Create dated snapshots: `architecture-2024-11-12.drawio`

### Dealing with Drift

**Symptoms of map drift:**
- Stakeholders reference outdated information
- Multiple competing maps exist
- Last update > 6 months ago
- New team members don't use it

**Recovery process:**
1. **Audit current state** (1-2 days): Compare map to reality
2. **Triage errors**: Critical fix (wrong), update (outdated), remove (obsolete)
3. **Batch update session**: Fix all at once, not incrementally
4. **Re-validate**: Get stakeholder sign-off
5. **Establish maintenance**: Assign owners, set review cadence
6. **Sunset old maps**: Archive competing/outdated versions

---

## 8. Domain-Specific Patterns

### Software Architecture
**Focus:** Service boundaries, data flows, deployment dependencies, scalability bottlenecks
**Relationships:** `calls`, `publishes/subscribes`, `reads/writes`, `depends-on`
**Layers:** Presentation (web/mobile/API), Application (services/logic), Data (databases/caches/queues)

### Organizational Structure
**Focus:** Reporting relationships, communication patterns, decision authority, ownership
**Relationships:** `reports-to`, `collaborates-with`, `escalates-to`, `consults`
**Groupings:** By function, product line, or location

### Process/Workflow
**Focus:** Step sequence, decision points, handoffs, bottlenecks
**Relationships:** `leads-to`, `branches-on`, `requires-approval`, `escalates`
**Formats:** Swimlane (multiple actors), decision tree (conditionals), linear flow

---

## 9. Troubleshooting Common Issues

### Issue: Map is too cluttered

**Symptoms:** Can't see structure, edges cross everywhere, hard to scan

**Fixes:**
1. Increase grouping - combine nodes into subsystems
2. Split into multiple maps (overview + detail)
3. Remove transitive relationships (if A→B→C, remove A→C)
4. Use different views for different audiences

### Issue: Stakeholders disagree on structure

**Symptoms:** Debates about groupings, relationship directions, what's included

**Fixes:**
1. Document perspectives explicitly: "Engineering view shows X, Product view shows Y"
2. Create view-specific maps rather than one "true" map
3. Focus on agreed-upon core, mark disputed areas
4. Use validation scenarios - test both structures

### Issue: Map becomes outdated quickly

**Symptoms:** Weekly corrections needed, people stop using it

**Fixes:**
1. Reduce scope - map stable core only
2. Assign clear ownership and update process
3. Automate where possible (generate from config files)
4. Accept "directionally correct" vs "perfectly accurate"

### Issue: Can't decide on visualization format

**Symptoms:** Trying multiple formats, none feels right

**Fixes:**
1. Match format to relationship pattern:
   - Hierarchy → Tree
   - Network → Graph
   - Sequence → Swimlane/Flow
2. Create small prototype in each format (10 nodes)
3. Test with stakeholder: "Which helps you understand better?"
4. It's okay to use different formats for different subsystems

---

## 10. Success Patterns from Practice

1. **Start messy, refine clean** - Brain dump first, organize later
2. **Version with system** - Map updates = part of change process
3. **Multiple maps > mega-map** - 5 focused maps beat 1 hairball
4. **Show evolution** - Include roadmap/changelog views
5. **Make navigable** - Links between maps, collapsible sections, filters
6. **Visual conventions matter** - Document notation, consistency > perfection
7. **Involve stakeholders early** - Collaborative mapping = shared understanding + buy-in
8. **Test usability continuously** - If people can't answer questions, it's not useful

---

## When to Apply This Methodology

Use this methodology if you're:

✓ Mapping systems with 50+ nodes
✓ Managing multiple stakeholder perspectives
✓ Needing to maintain maps over time (not one-off)
✓ Creating maps for diverse audiences (technical + non-technical)
✓ Dealing with high system complexity or frequent change
✓ Facilitating group mapping sessions
✓ Generating maps programmatically from data
✓ Building a "living documentation" practice

Go back to [template.md](template.md) if you're:
✗ Mapping simple systems (< 20 nodes)
✗ Creating one-off documentation
✗ Working alone with single audience
✗ Time-constrained (need map in < 1 hour)

# Component Extraction for Skill Creation

## Table of Contents
- [Overview](#overview)
- [Core Components to Extract](#core-components-to-extract)
- [Extraction Template](#extraction-template)
- [Mapping Components to Skill Structure](#mapping-components-to-skill-structure)
- [Pattern Abstraction](#pattern-abstraction)

---

## Overview

**Goal:** Systematically extract the building blocks needed to create a complete skill.

**Method:** Use structured notes to capture all essential components during deep reading, then map them to skill file structure.

---

## Core Components to Extract

### 1. Purpose & Problem

**Questions to answer:**
- What problem does this solve?
- What capability does it provide?
- Why would someone use this?
- What value does it deliver?

**Where to find:**
- Introduction/Overview sections
- Problem statement sections
- Use cases and applications
- Conclusions and summaries

**Example extraction:**
```markdown
## Purpose & Problem
**Problem:** Developers struggle to design RESTful APIs that follow best practices consistently
**Solution:** Provides a systematic framework for API design decisions
**Value:** Ensures APIs are intuitive, consistent, and follow REST principles
```

### 2. When to Use (Triggers)

**Questions to answer:**
- In what situations would someone use this?
- What user phrases indicate this need?
- What contexts make this applicable?
- When is this NOT appropriate?

**Where to find:**
- "When to use" sections
- Use cases and scenarios
- Problem descriptions
- Scope and limitations sections

**Example extraction:**
```markdown
## When to Use
**Situations:**
- Designing new RESTful API from scratch
- Reviewing existing API for consistency
- Making design decisions about resources and endpoints
- Teaching REST principles to team

**User phrases:**
- "How should I design this API?"
- "What endpoints should I create?"
- "Is this RESTful?"
- "API design review"
```

### 3. Methodology Structure

**Questions to answer:**
- What type of process is this? (Linear, iterative, decision tree, framework)
- What are the main stages/steps?
- What are the inputs and outputs of each step?
- What are the decision points?

**Where to find:**
- Procedure/process sections
- Step-by-step guides
- Workflow diagrams
- Methodology explanations

**Example extraction:**
```markdown
## Methodology Structure
**Type:** Linear process with decision points

**Stages:**
1. **Identify Resources**
   - Purpose: Determine the core entities in the domain
   - Inputs: Domain understanding, use cases
   - Outputs: List of resources (nouns)
   - Sub-steps: Analyze use cases, identify entities, validate with stakeholders

2. **Define Resource Operations**
   - Purpose: Determine what actions can be performed on each resource
   - Inputs: Resource list
   - Outputs: HTTP method mapping (GET, POST, PUT, DELETE)
   - Decision: Is this resource nested or top-level?

[Continue for all stages...]
```

### 4. Key Concepts & Terminology

**Questions to answer:**
- What specialized terms are used?
- What concepts need definition?
- What's the core vocabulary of this domain?

**Where to find:**
- Glossary sections
- Definitions and explanations
- Emphasized or bold terms
- First usage of technical terms

**Example extraction:**
```markdown
## Key Concepts
| Term | Definition | Importance |
|------|------------|------------|
| Resource | A conceptual entity in the API (user, post, comment) | Core abstraction in REST |
| Endpoint | A specific URL path and HTTP method combination | Implementation of resource operations |
| Idempotent | Operation that produces same result when repeated | Crucial for PUT/DELETE design |
```

### 5. Decision Points

**Questions to answer:**
- Where do users need to make choices?
- What are the criteria for each choice?
- What are the alternatives and trade-offs?

**Where to find:**
- "When to choose X vs Y" sections
- Comparison tables
- Trade-off discussions
- Decision trees

**Example extraction:**
```markdown
## Decision Points

**Decision 1: Nested vs. Top-Level Resources**
- Use nested if: Resource only exists in context of parent (e.g., /posts/123/comments)
- Use top-level if: Resource has independent existence (e.g., /users)
- Criteria: Can this resource exist without parent? Will it be accessed independently?

**Decision 2: PUT vs. PATCH for Updates**
- Use PUT if: Replacing entire resource
- Use PATCH if: Partial update of specific fields
- Criteria: Are clients providing full resource representation?
```

### 6. Quality Dimensions

**Questions to answer:**
- What makes execution good vs. bad?
- What are the quality indicators?
- How do you know if you've succeeded?
- What are common mistakes?

**Where to find:**
- Quality criteria sections
- Best practices
- Anti-patterns and pitfalls
- Validation and testing sections

**Example extraction:**
```markdown
## Quality Dimensions

| Dimension | Good Indicators | Poor Indicators |
|-----------|----------------|-----------------|
| Consistency | All resources follow same URL structure, same naming conventions | Mixed naming (camelCase and snake_case), inconsistent nesting |
| Intuitiveness | Resource names are clear nouns, operations map to HTTP methods logically | Verb-based URLs (/getUser), non-standard method usage |
| Completeness | All CRUD operations available where appropriate | Missing obvious operations, asymmetric API |
```

### 7. Examples & Use Cases

**Questions to answer:**
- What are concrete applications?
- What contexts does this work in?
- What outcomes are achieved?

**Where to find:**
- Examples sections
- Case studies
- Worked demonstrations
- Use case descriptions

**Example extraction:**
```markdown
## Examples & Use Cases

**Use Case 1: E-commerce API**
- Context: Building product catalog and shopping cart API
- Application: Resources (products, cart, orders), nested reviews under products
- Outcome: RESTful API that follows conventions, easy for mobile/web clients

**Use Case 2: Social Media API**
- Context: Designing posts, comments, likes, follows
- Application: Top-level users and posts, nested comments, junction resources for follows
- Outcome: Scalable API structure that mirrors domain model
```

### 8. Templates & Formats

**Questions to answer:**
- Is there a standard structure/format?
- What are the key sections?
- What's the fill-in-the-blank template?

**Where to find:**
- Template sections
- Boilerplate code
- Example structures
- Checklists

**Example extraction:**
```markdown
## Templates & Formats

**Type:** API Design Document Template

**Key sections:**
1. Resources (list of core entities)
2. Endpoints (URL + HTTP method for each operation)
3. Request/Response formats (JSON schema)
4. Error handling (standard error responses)
5. Authentication/Authorization (security model)
```

### 9. Guardrails (Do/Don't)

**Questions to answer:**
- What best practices must be followed?
- What anti-patterns must be avoided?
- What are common pitfalls?

**Where to find:**
- Best practices sections
- Common mistakes sections
- Do/Don't lists
- Troubleshooting guides

**Example extraction:**
```markdown
## Guardrails

**Do:**
- Use plural nouns for resource names (/users not /user)
- Use HTTP methods according to semantics (GET=read, POST=create, PUT=update, DELETE=delete)
- Return appropriate status codes (200, 201, 404, 400, etc.)
- Version your API (/v1/, /v2/)
- Provide clear error messages with error codes

**Don't:**
- Use verbs in URLs (/getUser, /deletePost)
- Use GET for operations that modify state
- Return 200 OK for errors
- Break existing endpoints in updates
- Expose internal implementation details in URLs
```

### 10. Resources Needed

**Questions to answer:**
- Should this skill have a template.md?
- Should this skill have a methodology.md (or topic-specific resources)?
- What examples should be included?
- What should the rubric measure?

**Example extraction:**
```markdown
## Resources Needed

- [ ] Template needed: Yes - API design document structure
- [ ] Additional resources needed:
  - resources/endpoint-patterns.md (common URL patterns)
  - resources/status-codes.md (when to use each code)
  - resources/examples/ (sample API designs)
- [ ] Rubric dimensions:
  - Consistency
  - RESTful principles adherence
  - Intuitiveness
  - Completeness
  - Documentation quality
```

---

## Extraction Template

**Create `components.md` during deep reading:**

```markdown
# Extracted Components for [Skill Name]

## 1. Core Purpose
**Problem:** [What problem does this solve?]
**Solution:** [What capability does it provide?]
**Value:** [Why would someone use this?]

## 2. When to Use (Triggers)
**Situations:**
- [Context 1]
- [Context 2]
- [Context 3]

**User phrases:**
- "[Phrase 1]"
- "[Phrase 2]"

## 3. Methodology Structure
**Type:** [Linear process | Iterative cycle | Decision tree | Framework]

**Main Stages:**
1. **Stage 1:** [Name] - [Purpose]
   - Sub-steps: [If any]
   - Inputs: [What's needed]
   - Outputs: [What's produced]

2. **Stage 2:** [Name] - [Purpose]
   [Continue...]

## 4. Key Concepts & Terms
| Term | Definition | Importance |
|------|------------|------------|
| [Term 1] | [Def] | [Why it matters] |
| [Term 2] | [Def] | [Why it matters] |

## 5. Decision Points
**Decision 1:** [When to choose A vs B]
- Choose A if: [Condition]
- Choose B if: [Condition]

## 6. Quality Dimensions
| Dimension | Good Indicators | Poor Indicators |
|-----------|----------------|-----------------|
| [Aspect 1] | [Good] | [Poor] |
| [Aspect 2] | [Good] | [Poor] |

## 7. Examples & Use Cases
**Use Case 1:** [Context]
- Application: [How it's used]
- Outcome: [Result]

## 8. Templates & Formats
**Template type:** [Worksheet | Checklist | Document | Code]
**Key sections:** [List]

## 9. Guardrails
**Do:**
- [Best practice 1]
- [Best practice 2]

**Don't:**
- [Anti-pattern 1]
- [Anti-pattern 2]

## 10. Resources Needed
- [ ] Template: [Needed? For what?]
- [ ] Additional resources: [List topic-specific files]
- [ ] Examples: [What to include]
- [ ] Rubric dimensions: [What to measure]
```

---

## Mapping Components to Skill Structure

**Use this table to transform extracted components into skill files:**

| Extracted Component | Maps To | File Location |
|---------------------|---------|---------------|
| Problems solved + Triggers | YAML `description` | SKILL.md frontmatter |
| Purpose statement | "Purpose" section | SKILL.md |
| When to use situations | "When to Use This Skill" | SKILL.md |
| User trigger phrases | "Trigger phrases" note | SKILL.md |
| Methodology steps | "Workflow" section | SKILL.md |
| Key terms & concepts | Glossary or inline definitions | SKILL.md or resources/ |
| Decision points | Conditional steps in workflow | SKILL.md workflow |
| Examples & use cases | "Common Patterns" | SKILL.md or resources/examples/ |
| Quality dimensions | Rubric criteria | resources/evaluators/rubric_*.json |
| Templates & formats | Template file | resources/template.md (if needed) |
| Guardrails (Do/Don't) | "Guardrails" section | SKILL.md |
| Advanced techniques | Topic-specific resource files | resources/*.md |

---

## Pattern Abstraction

**Generalize from specific to reusable:**

### Why Abstract?
- Makes skill applicable beyond original domain
- Removes unnecessary specifics
- Focuses on transferable process
- Maintains actionability

### Abstraction Process

Copy this abstraction workflow and track your progress:

```
Pattern Abstraction:
- [ ] Step 1: Identify domain-specific language
- [ ] Step 2: Extract underlying pattern
- [ ] Step 3: Generalize to broader contexts
- [ ] Step 4: Validate actionability
```

**Step 1: Identify Domain-Specific Language**

Example from source:
> "To design a REST API, first identify your resources (users, posts, comments), then define operations (GET, POST, PUT, DELETE) for each resource..."

Domain-specific elements:
- REST API → [Type of design problem]
- users, posts, comments → [Domain entities]
- GET, POST, PUT, DELETE → [Available operations]

**Step 2: Extract Underlying Pattern**

Abstracted:
> "To design a [system], first identify [core entities], then define [operations] for each entity..."

**Step 3: Generalize to Broader Contexts**

Final abstraction:
```markdown
**Step 1:** Identify domain entities/components
**Step 2:** Define operations/interactions per entity
**Step 3:** Specify data formats/interfaces
**Step 4:** Design relationships/dependencies
**Step 5:** Validate against use cases
```

### Abstraction Checklist

Copy this checklist for each methodology step and verify:

```
Abstraction Quality Check:
- [ ] Remove domain jargon (or define it clearly)
- [ ] Identify underlying pattern/principle
- [ ] Test generalizability (applies to different domains?)
- [ ] Preserve actionability (specific enough to execute?)
- [ ] Maintain examples (show domain-specific application)
```

For each methodology step verify:

- [ ] **Remove domain jargon** (or define it clearly)
- [ ] **Identify underlying pattern/principle** (what's really happening?)
- [ ] **Test generalizability** (could this apply to different domains?)
- [ ] **Preserve actionability** (is it still specific enough to execute?)
- [ ] **Maintain examples** (show domain-specific application)

### Abstraction Levels

**Too Specific (Not Reusable):**
> "Use Postman to send GET request to /api/v1/users endpoint and verify 200 status code"

**Appropriately Abstracted (Reusable):**
> "Send HTTP GET request to the users endpoint and verify successful response"

**Too Abstract (Not Actionable):**
> "Perform a data retrieval operation and check the result"

**Sweet Spot:**
- Generic enough to apply across contexts
- Specific enough to be executable
- Uses domain-agnostic vocabulary (with examples)

---

## Quick Reference

**10 Components to Extract:**
1. Purpose & Problem
2. When to Use (Triggers)
3. Methodology Structure
4. Key Concepts & Terms
5. Decision Points
6. Quality Dimensions
7. Examples & Use Cases
8. Templates & Formats
9. Guardrails (Do/Don't)
10. Resources Needed

**Extraction Flow:**
1. Read section with component lens
2. Extract to structured notes
3. Abstract from domain specifics
4. Map to skill structure
5. Generate skill files

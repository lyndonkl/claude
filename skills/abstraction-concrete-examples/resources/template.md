# Quick-Start Template

## Workflow

Copy this checklist and track your progress:

```
Abstraction Ladder Progress:
- [ ] Step 1: Gather inputs (topic, purpose, audience, levels, direction)
- [ ] Step 2: Choose starting point and build levels
- [ ] Step 3: Add connections and transitions
- [ ] Step 4: Test with edge cases
- [ ] Step 5: Validate quality checklist
```

**Step 1: Gather inputs**

Define topic (what concept/system/problem?), purpose (communication/design/validation?), audience (who will use this?), levels (3-5, default 4), direction (top-down/bottom-up/middle-out), and focus areas (edge cases/communication/implementation).

**Step 2: Choose starting point and build levels**

Use [Common Starting Points](#common-starting-points) to select direction. Top-down for teaching/design, bottom-up for analysis/patterns, middle-out for bridging gaps. Build each level ensuring distinctness and logical flow.

**Step 3: Add connections and transitions**

Explain how levels flow together as coherent whole. Each level should logically derive from previous level. See [Template Structure](#template-structure) for format.

**Step 4: Test with edge cases**

Identify 2-3 boundary scenarios that test principles. For each: describe scenario, state what abstract principle suggests, note what actually happens, assess alignment (matches/conflicts/requires nuance).

**Step 5: Validate quality checklist**

Use [Quality Checklist](#quality-checklist) to verify: levels are distinct, concrete level has specifics, abstract level is universal, edge cases are meaningful, assumptions stated, serves stated purpose.

## Template Structure

Copy this structure to create your abstraction ladder:

```markdown
# Abstraction Ladder: [Your Topic]

## Overview
**Topic**: [What you're exploring]
**Purpose**: [Why you're building this ladder]
**Audience**: [Who will use this]

## Abstraction Levels

### Level 1 (Most Abstract): [Give it a label]
[Universal principle or highest-level concept]

Why this matters: [Explain the significance]

### Level 2: [Label]
[Framework, category, or general approach]

Connection to L1: [How does this derive from Level 1?]

### Level 3: [Label]
[Specific method or implementation approach]

Connection to L2: [How does this derive from Level 2?]

### Level 4 (Most Concrete): [Label]
[Exact implementation with specific details]

Connection to L3: [How does this derive from Level 3?]

*Add Level 5 if you need more granularity*

## Connections & Transitions

[Explain how the levels flow together as a coherent whole]

**Key insight**: [What becomes clear when you see all levels together?]

## Edge Cases & Boundary Testing

### Edge Case 1: [Name]
- **Scenario**: [Concrete situation]
- **Abstract principle**: [What L1/L2 suggests should happen]
- **Reality**: [What actually happens]
- **Alignment**: [✓ matches / ✗ conflicts / ~ requires nuance]

### Edge Case 2: [Name]
[Same structure]

## Applications

This ladder is useful for:
- [Use case 1]
- [Use case 2]
- [Use case 3]

## Gaps & Assumptions

**Assumptions:**
- [What are we taking for granted?]
- [What context is this specific to?]

**Gaps:**
- [What's not covered?]
- [What questions remain?]

**What would change if:**
- [Different scale? Different domain? Different constraints?]
```

## Common Starting Points

### Start Top-Down (Abstract → Concrete)

**Good for**: Teaching, designing from principles, communication to varied audiences

**Prompt to yourself**:
1. "What's the most universal statement I can make about this topic?"
2. "How would this principle manifest in practice?"
3. "What framework implements this principle?"
4. "What's a concrete example?"
5. "What are the exact, measurable details?"

**Example**:
- L1: "Communication should be clear"
- L2: "Use plain language and structure"
- L3: "Organize documents with headings, bullets, short paragraphs"
- L4: "This document uses H2 headings every 3-4 paragraphs, bullet lists for steps"

### Start Bottom-Up (Concrete → Abstract)

**Good for**: Analyzing existing work, generalizing patterns, root cause analysis

**Prompt to yourself**:
1. "What specific thing am I looking at?"
2. "What pattern does this exemplify?"
3. "What general approach does that pattern reflect?"
4. "What framework supports that approach?"
5. "What universal principle underlies this?"

**Example**:
- L5: "Button has onClick={handleSubmit} and disabled={!isValid}"
- L4: "Form button is disabled until validation passes"
- L3: "Prevent invalid form submission through UI controls"
- L2: "Use defensive programming and client-side validation"
- L1: "Systems should prevent errors, not just catch them"

### Start Middle-Out (Familiar → Both Directions)

**Good for**: Building shared understanding, bridging expertise gaps

**Prompt to yourself**:
1. "What's something everyone already understands?"
2. Go up: "What principle does this exemplify?"
3. Go down: "How exactly is this implemented?"
4. Continue in both directions

**Example** (start at L3):
- L1: ↑ "Products should be accessible to all"
- L2: ↑ "Follow WCAG guidelines"
- **L3: "Add alt text to images"** ← Start here
- L4: ↓ `<img src="logo.png" alt="Company name logo">`
- L5: ↓ Screen reader reads: "Company name logo, image"

## Quality Checklist

Before finalizing, check:

- [ ] Each level is clearly distinct from adjacent levels
- [ ] I can explain the transition between any two adjacent levels
- [ ] Most concrete level has specific, measurable details
- [ ] Most abstract level is broadly applicable beyond this context
- [ ] Edge cases test the boundaries meaningfully
- [ ] Assumptions are stated explicitly
- [ ] The ladder serves the stated purpose
- [ ] Someone unfamiliar with the topic could follow the logic

## Guardrails

**Do:**
- State what you don't know or aren't sure about
- Include edge cases that challenge the principles
- Make concrete levels truly concrete (numbers, specifics)
- Make abstract levels truly universal (apply to other domains)

**Don't:**
- Use vague language like "good," "better," "appropriate" without defining
- Make huge jumps between levels (missing middle)
- Let different levels address different aspects of the topic
- Assume expertise your audience doesn't have

## Next Steps After Creating Ladder

**For communication:**
- Share L1-L2 with executives
- Share L2-L3 with managers
- Share L3-L5 with implementers

**For design:**
- Use L1-L2 to guide decisions
- Use L3-L4 to specify requirements
- Use L5 for implementation

**For validation:**
- Test if L5 reality matches L1 principles
- Find gaps between levels
- Identify where principles break down

**For documentation:**
- Use as table of contents (each level = section depth)
- Create expandable sections (click for more detail)
- Link levels to relevant resources

## Examples to Study

See `resources/examples/` for complete examples:
- `api-design.md` - Technical example (API design principles)
- `hiring-process.md` - Process example (hiring practices)

Each example shows different techniques and applications.

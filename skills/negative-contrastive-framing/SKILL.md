---
name: negative-contrastive-framing
description: Defines concepts, quality criteria, and boundaries by showing what they are NOT -- using anti-goals, near-miss examples, and failure patterns to create crisp decision criteria where positive definitions alone are ambiguous. Use when clarifying fuzzy boundaries, defining quality criteria, teaching by counterexample, preventing common mistakes, setting design guardrails, disambiguating similar concepts, refining requirements through anti-patterns, or when user mentions near-miss examples, anti-goals, what not to do, negative examples, counterexamples, or boundary clarification.
---

# Negative Contrastive Framing

## Workflow

Copy this checklist and track your progress:

```
Negative Contrastive Framing Progress:
- [ ] Step 1: Define positive concept
- [ ] Step 2: Identify negative examples
- [ ] Step 3: Analyze contrasts
- [ ] Step 4: Validate quality
- [ ] Step 5: Deliver framework
```

**Step 1: Define positive concept**

Start with initial positive definition, identify why it's ambiguous or fuzzy (multiple interpretations, edge cases unclear), and clarify purpose (teaching, decision-making, quality control). See [Common Patterns](#common-patterns) for typical applications.

**Step 2: Identify negative examples**

For simple cases with clear anti-patterns → Use [resources/template.md](resources/template.md) to structure anti-goals, near-misses, and failure patterns. For complex cases with subtle boundaries → Study [resources/methodology.md](resources/methodology.md) for techniques like contrast matrices and boundary mapping.

**Step 3: Analyze contrasts**

Create `negative-contrastive-framing.md` with: positive definition, 3-5 anti-goals, 5-10 near-miss examples with explanations, common failure patterns, clear decision criteria ("passes if..." / "fails if..."), and boundary cases. Ensure contrasts reveal the *why* behind criteria.

**Step 4: Validate quality**

Self-assess using [resources/evaluators/rubric_negative_contrastive_framing.json](resources/evaluators/rubric_negative_contrastive_framing.json). Check: negative examples span the boundary space, near-misses are genuinely close calls, contrasts clarify criteria better than positive definition alone, failure patterns are actionable guards. Minimum standard: Average score ≥ 3.5.

**Step 5: Deliver framework**

Present completed framework with positive definition sharpened by negatives, most instructive near-misses highlighted, decision criteria operationalized as checklist, common mistakes identified for prevention.

## Common Patterns

### By Domain

**Engineering (Code Quality):**
- Positive: "Maintainable code"
- Negative: God objects, tight coupling, unclear names, magic numbers, exception swallowing
- Near-miss: Well-commented spaghetti code (documentation without structure)

**Design (UX):**
- Positive: "Intuitive interface"
- Negative: Hidden actions, inconsistent patterns, cryptic error messages
- Near-miss: Beautiful but unusable (form over function)

**Communication (Clear Writing):**
- Positive: "Clear documentation"
- Negative: Jargon-heavy, assuming context, no examples, passive voice
- Near-miss: Technically accurate but incomprehensible to target audience

**Strategy (Market Positioning):**
- Positive: "Premium brand"
- Negative: Overpriced without differentiation, luxury signaling without substance
- Near-miss: High price without service quality to match

### By Application

**Teaching:**
- Show common mistakes students make
- Provide near-miss solutions revealing misconceptions
- Identify "looks right but is wrong" patterns

**Decision Criteria:**
- Define disqualifiers (automatic rejection criteria)
- Show edge cases that almost pass
- Clarify ambiguous middle ground

**Quality Control:**
- Identify anti-patterns to avoid
- Show subtle defects that might pass inspection
- Define clear pass/fail boundaries

## Guardrails

**Near-Miss Selection:**
- Near-misses must be genuinely close to positive examples
- Should reveal specific dimension that fails (not globally bad)
- Avoid trivial failures—focus on subtle distinctions

**Contrast Quality:**
- Explain *why* each negative example fails
- Show what dimension violates criteria
- Make contrasts instructive, not just lists

**Completeness:**
- Cover failure modes across key dimensions
- Don't cherry-pick—include hard-to-classify cases
- Show spectrum from clear pass to clear fail

**Actionability:**
- Translate insights into decision rules
- Provide guards/checks to prevent failures
- Make criteria operationally testable

**Avoid:**
- Strawman negatives (unrealistically bad examples)
- Negatives without explanation (show what's wrong and why)
- Missing the "close call" zone (all examples clearly pass or fail)

## Quick Reference

**Resources:**
- `resources/template.md` - Structured format for anti-goals, near-misses, failure patterns
- `resources/methodology.md` - Advanced techniques (contrast matrices, boundary mapping, failure taxonomies)
- `resources/evaluators/rubric_negative_contrastive_framing.json` - Quality criteria

**Output:** `negative-contrastive-framing.md` with positive definition, anti-goals, near-misses with analysis, failure patterns, decision criteria

**Success Criteria:**
- Negative examples span boundary space (not just extremes)
- Near-misses are instructive close calls
- Contrasts clarify ambiguous criteria
- Failure patterns are actionable guards
- Decision criteria operationalized
- Score ≥ 3.5 on rubric

**Quick Decisions:**
- **Clear anti-patterns?** → Template only
- **Subtle boundaries?** → Use methodology for contrast matrices
- **Teaching application?** → Emphasize near-misses revealing misconceptions
- **Quality control?** → Focus on failure pattern taxonomy

**Common Mistakes:**
1. Only showing extreme negatives (not instructive near-misses)
2. Lists without analysis (not explaining why examples fail)
3. Cherry-picking easy cases (avoiding hard boundary calls)
4. Strawman negatives (unrealistically bad)
5. No operationalization (criteria remain fuzzy despite contrasts)

**Key Insight:**
Negative examples are most valuable when they're *almost* positive—close calls that force articulation of subtle criteria invisible in positive definition alone.

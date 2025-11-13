# Negative Contrastive Framing Template

## Quick Start

**Purpose:** Define concepts by showing what they're NOT—use anti-goals, near-misses, and failure patterns to clarify fuzzy boundaries.

**When to use:** Positive definition exists but edges are unclear, multiple interpretations cause confusion, or need to distinguish similar concepts.

---

## Part 1: Positive Definition

**Concept/Goal:** [What you're trying to define]

**Initial Positive Definition:**
[Your current definition using positive attributes]

**Why It's Ambiguous:**
- [Interpretation 1 vs Interpretation 2]
- [Edge cases unclear]
- [Confusion point]

**Purpose:**
- [ ] Teaching/training
- [ ] Decision criteria
- [ ] Quality control
- [ ] Requirements clarification
- [ ] Other: [Specify]

---

## Part 2: Anti-Goals

**What This is NOT:** (Opposite of desired outcome)

**Anti-Goal 1:** [Opposite extreme]
- **Description:** [What it looks like]
- **Why it fails:** [Violates which criterion]
- **Example:** [Concrete instance]

**Anti-Goal 2:** [Another opposite]
- **Description:**
- **Why it fails:**
- **Example:**

**Anti-Goal 3:** [Third opposite]
- **Description:**
- **Why it fails:**
- **Example:**

[Add 2-5 anti-goals total]

---

## Part 3: Near-Miss Examples

**Close Calls That FAIL:** (Examples that almost qualify but fail on key dimension)

**Near-Miss 1:** [Example]
- **What it gets right:** [Positive aspects]
- **Where it fails:** [Specific dimension that disqualifies]
- **Why it's instructive:** [What it reveals about criteria]
- **Boundary lesson:** [Insight about where line is drawn]

**Near-Miss 2:** [Example]
- **What it gets right:**
- **Where it fails:**
- **Why it's instructive:**
- **Boundary lesson:**

**Near-Miss 3:** [Example]
- **What it gets right:**
- **Where it fails:**
- **Why it's instructive:**
- **Boundary lesson:**

[Continue for 5-10 near-misses—these are most valuable]

---

## Part 4: Common Failure Patterns

**Failure Pattern 1:** [Pattern name]
- **Description:** [What the pattern looks like]
- **Why it fails:** [Criterion violated]
- **How to spot:** [Detection heuristic]
- **How to avoid:** [Prevention guard]
- **Example:** [Instance]

**Failure Pattern 2:** [Pattern name]
- **Description:**
- **Why it fails:**
- **How to spot:**
- **How to avoid:**
- **Example:**

**Failure Pattern 3:** [Pattern name]
- **Description:**
- **Why it fails:**
- **How to spot:**
- **How to avoid:**
- **Example:**

[List 3-7 common failure patterns]

---

## Part 5: Contrast Matrix

| Example | Dimension 1 | Dimension 2 | Dimension 3 | Passes? | Why/Why Not |
|---------|-------------|-------------|-------------|---------|-------------|
| [Positive example] | ✓ | ✓ | ✓ | ✓ PASS | All criteria met |
| [Near-miss 1] | ✓ | ✓ | ✗ | ✗ FAIL | Fails Dimension 3 |
| [Near-miss 2] | ✓ | ✗ | ✓ | ✗ FAIL | Fails Dimension 2 |
| [Negative example] | ✗ | ✗ | ✗ | ✗ FAIL | Fails all dimensions |

**Key Dimensions:**
- **Dimension 1:** [Name] - [What it measures]
- **Dimension 2:** [Name] - [What it measures]
- **Dimension 3:** [Name] - [What it measures]

---

## Part 6: Sharpened Definition

**Revised Positive Definition:**
[Updated definition informed by negative contrasts]

**Decision Criteria:**

✓ **Passes if:**
- [ ] [Criterion 1 operationalized]
- [ ] [Criterion 2 operationalized]
- [ ] [Criterion 3 operationalized]

✗ **Fails if ANY of:**
- [ ] [Disqualifier 1]
- [ ] [Disqualifier 2]
- [ ] [Disqualifier 3]

⚠️ **Ambiguous middle ground:**
- [Case 1]: Consider context [X]
- [Case 2]: Requires judgment call on [Y]

---

## Part 7: Actionable Guards

**Prevention Checklist:**
- [ ] [Guard against failure pattern 1]
- [ ] [Guard against failure pattern 2]
- [ ] [Guard against failure pattern 3]
- [ ] [Check for near-miss condition 1]
- [ ] [Check for near-miss condition 2]

**Detection Heuristics:**
1. **Red flag:** [Signal that example might fail]
   - **Check:** [What to verify]
2. **Yellow flag:** [Warning sign]
   - **Check:** [What to verify]
3. **Green light:** [Positive signal]
   - **Confirm:** [What to validate]

---

## Part 8: Examples Across Spectrum

**Clear PASS:** [Unambiguous positive example]
- [Why it clearly meets all criteria]

**Borderline PASS:** [Barely qualifies]
- [Why it passes despite weakness in dimension X]

**Borderline FAIL:** [Almost qualifies]
- [Why it fails despite strength in dimensions Y and Z]

**Clear FAIL:** [Unambiguous negative example]
- [Why it clearly violates criteria]

---

## Output Format

Create `negative-contrastive-framing.md`:

```markdown
# [Concept]: Negative Contrastive Framing

**Date:** [YYYY-MM-DD]

## Positive Definition
[Sharpened definition]

## Anti-Goals
1. [Anti-goal] - [Why it's opposite]
2. [Anti-goal] - [Why it's opposite]

## Near-Miss Examples (Most Instructive)
1. **[Example]**: Almost passes but fails because [key dimension]
2. **[Example]**: Gets [X] right but fails on [Y]
3. **[Example]**: Looks like success but is actually [failure mode]

## Common Failure Patterns
1. **[Pattern]**: [Description] - Guard: [Prevention]
2. **[Pattern]**: [Description] - Guard: [Prevention]

## Decision Criteria

✓ **Passes if:**
- [Operationalized criterion 1]
- [Operationalized criterion 2]

✗ **Fails if:**
- [Disqualifier 1]
- [Disqualifier 2]

## Contrast Matrix
[Table showing examples across key dimensions]

## Key Insights
- [What negative examples revealed about boundaries]
- [Subtle criteria made explicit through near-misses]
- [Actionable guards to prevent common failures]
```

---

## Quality Checklist

Before finalizing:
- [ ] Anti-goals represent true opposites (not just bad versions)
- [ ] Near-misses are genuinely close calls (not obviously bad)
- [ ] Each failure has clear explanation of *why* it fails
- [ ] Failure patterns are common/realistic (not strawmen)
- [ ] Decision criteria are operationalized (testable)
- [ ] Guards are actionable (can be implemented)
- [ ] Covers spectrum from clear pass to clear fail
- [ ] Ambiguous cases acknowledged and addressed
- [ ] Insights reveal something not obvious from positive definition alone

---

## Common Applications

**Code Review:**
- Anti-goal: Unreadable code
- Near-miss: Well-commented but poorly structured code
- Pattern: "Documentation hides design problems"

**UX Design:**
- Anti-goal: Unusable interface
- Near-miss: Beautiful but non-intuitive design
- Pattern: "Form over function"

**Hiring:**
- Anti-goal: Wrong culture fit
- Near-miss: Strong skills but misaligned values
- Pattern: "Optimizing for résumé over team dynamics"

**Product Strategy:**
- Anti-goal: Feature bloat
- Near-miss: Useful feature that distracts from core value
- Pattern: "Saying yes to everything"

**Communication:**
- Anti-goal: Incomprehensible writing
- Near-miss: Technically accurate but inaccessible
- Pattern: "Correctness without clarity"

---

## Tips

**For Near-Misses:**
- Look for examples that fool initial judgment
- Find cases where single dimension tips the balance
- Use real examples from experience

**For Failure Patterns:**
- Name patterns memorably
- Make detection criteria specific
- Provide concrete prevention guards

**For Decision Criteria:**
- Test against edge cases
- Make falsifiable/testable
- Handle ambiguous middle ground explicitly

**For Teaching:**
- Start with near-misses (most engaging)
- Build pattern recognition through repetition
- Have learners generate their own negative examples

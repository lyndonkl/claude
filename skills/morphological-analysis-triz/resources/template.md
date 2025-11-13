# Morphological Analysis & TRIZ Template

## Quick Start

**For Morphological Analysis:**
1. Define 3-7 parameters → 2-5 options each → Build matrix → Evaluate combinations

**For TRIZ:**
1. State contradiction (improve A worsens B) → Look up in matrix → Apply 3-4 recommended principles

**For Both:**
Use morphological analysis to explore space, TRIZ to resolve contradictions in configurations.

---

## Part 1: Problem Definition

**Problem Statement:** [Clear, specific description]

**Objectives:**
1. [Primary objective - measurable]
2. [Secondary objective]
3. [Tertiary objective]

**Constraints:**
- Cost: [Budget limit]
- Size/Weight: [Physical limitations]
- Time: [Timeline]
- Materials: [Allowed/prohibited]
- Performance: [Minimum requirements]

**Success Criteria:**
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

---

## Part 2: Morphological Analysis

### Step 1: Identify 3-7 Independent Parameters

**Parameter 1:** [Name] - [Why essential]
**Parameter 2:** [Name] - [Why essential]
**Parameter 3:** [Name] - [Why essential]
[Continue for 3-7 parameters]

**Independence check:** Can I change Parameter 1 without forcing changes in Parameter 2? (Yes = independent)

### Step 2: List 2-5 Options Per Parameter

**Parameter 1: [Name]**
- Option A: [Description]
- Option B: [Description]
- Option C: [Description]
[2-5 mutually exclusive options]

[Repeat for all parameters]

### Step 3: Build Morphological Matrix

```
| Parameter      | Opt 1 | Opt 2 | Opt 3 | Opt 4 | Opt 5 |
|----------------|-------|-------|-------|-------|-------|
| [Param 1]      | [A]   | [B]   | [C]   | [D]   | -     |
| [Param 2]      | [A]   | [B]   | [C]   | -     | -     |
| [Param 3]      | [A]   | [B]   | [C]   | [D]   | [E]   |

Total: [N1 × N2 × N3...] = [Total configs]
```

### Step 4: Generate 5-10 Promising Configurations

**Config 1: [Name]**
- Parameter 1: [Selected option]
- Parameter 2: [Selected option]
- Parameter 3: [Selected option]
- **Rationale:** [Why promising]
- **Pros:** [Advantages]
- **Cons:** [Disadvantages]

[Repeat for 5-10 configurations]

### Step 5: Score and Rank

| Config | Obj 1 | Obj 2 | Obj 3 | Cost | Feasibility | Total | Rank |
|--------|-------|-------|-------|------|-------------|-------|------|
| Config 1 | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | [Sum] | [#] |
| Config 2 | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] | [Sum] | [#] |

**Selected:** [Top-ranked configuration]

---

## Part 3: TRIZ Contradiction Resolution

### Step 1: State Contradiction

**Improving Parameter:** [What we want to increase]
- Current: [Value]
- Desired: [Target]

**Worsening Parameter:** [What degrades when we improve first]
- Acceptable degradation: [Threshold]

**Contradiction Statement:** "To improve [X], we must worsen [Y], which is unacceptable because [reason]."

### Step 2: Map to TRIZ 39 Parameters

**TRIZ 39 Parameters (Quick Reference):**
1. Weight of moving object
2. Weight of stationary object
3-4. Length (moving/stationary)
5-6. Area (moving/stationary)
7-8. Volume (moving/stationary)
9. Speed
10. Force
11. Stress/pressure
12. Shape
13. Stability of composition
14. Strength
15-16. Duration of action
17. Temperature
18. Illumination
19-20. Energy use
21. Power
22-26. Loss of (energy, substance, info, time, quantity)
27. Reliability
28-29. Measurement/manufacturing accuracy
30-31. Harmful factors (external/internal)
32-34. Ease of (manufacture, operation, repair)
35. Adaptability
36. Device complexity
37. Difficulty of detecting/measuring
38. Automation
39. Productivity

**Map your contradiction:**
- Improving: [Map to one of 39]
- Worsening: [Map to one of 39]

### Step 3: Lookup Recommended Principles

**From TRIZ Contradiction Matrix:** [Lookup improving × worsening]

**Recommended Principles:** [#N, #M, #P, #Q]

**40 Inventive Principles (Brief):**
1. Segmentation - Divide into parts
2. Taking Out - Remove disturbing element
3. Local Quality - Different parts, different functions
4. Asymmetry - Use asymmetric forms
5. Merging - Combine similar objects
6. Universality - Multi-function
7. Nesting - Matryoshka dolls
8. Anti-Weight - Counterbalance
9. Preliminary Anti-Action - Pre-stress
10. Preliminary Action - Prepare in advance
11. Beforehand Cushioning - Emergency measures
12. Equipotentiality - Eliminate lifting/lowering
13. The Other Way - Invert
14. Spheroidality - Use curves
15. Dynamics - Make adaptable
16. Partial/Excessive - Go over/under optimal
17. Another Dimension - Use 3D, layers
18. Mechanical Vibration - Use oscillation
19. Periodic Action - Pulsed vs continuous
20. Continuity - Eliminate idle time
21. Rushing Through - High speed reduces harm
22. Blessing in Disguise - Use harm for benefit
23. Feedback - Introduce adjustment
24. Intermediary - Use intermediate object
25. Self-Service - Object services itself
26. Copying - Use cheap copy
27. Cheap Short-Living - Replace expensive with many cheap
28. Mechanics Substitution - Use fields instead
29. Pneumatics/Hydraulics - Use gas/liquid
30. Flexible Shells - Use membranes
31. Porous Materials - Make porous
32. Color Changes - Change color/transparency
33. Homogeneity - Same material
34. Discarding/Recovering - Discard after use
35. Parameter Changes - Change physical state
36. Phase Transitions - Use phenomena during transition
37. Thermal Expansion - Use expansion/contraction
38. Strong Oxidants - Enrich atmosphere
39. Inert Atmosphere - Use inert environment
40. Composite Materials - Change to composite

**For detailed principle examples, see [methodology.md](methodology.md).**

### Step 4: Apply Principles

**Principle #[N]: [Name]**
- **How to apply:** [Specific adaptation to problem]
- **Resolves contradiction:** [Explain how]
- **Feasibility:** [High/Medium/Low]

[Repeat for 3-4 principles]

### Step 5: Combine Principles (Optional)

**Combined Solution:**
- **Principles:** [#N + #M]
- **Synergy:** [How they work together]
- **Result:** [Concrete design concept]

---

## Part 4: Output Format

Create `morphological-analysis-triz.md`:

```markdown
# [Problem Name]: Systematic Innovation

**Date:** [YYYY-MM-DD]

## Problem
[Problem statement, objectives, constraints]

## Morphological Analysis (if used)

### Matrix
[Parameter-option table]

### Top Configurations
1. [Config name]: [Parameters] - Rationale: [Why] - Score: [X]
2. [Config name]: [Parameters] - Rationale: [Why] - Score: [Y]

## TRIZ Analysis (if used)

### Contradiction
Improve [X] → Worsens [Y]

### Applied Principles
- Principle #[N] ([Name]): [Application] → [Result]
- Principle #[M] ([Name]): [Application] → [Result]

### Solution Concepts
1. **[Concept name]:** [Description] - Pros: [X] - Cons: [Y]
2. **[Concept name]:** [Description] - Pros: [X] - Cons: [Y]

## Recommendation
**Primary Solution:** [Name]
- Description: [What it is]
- Why: [Rationale]
- Next Steps: [Actions]

**Alternative:** [Name] (if primary fails/too risky)
```

---

## Quick Examples

**Morphological Analysis (Lamp Design):**
```
Parameters: Power (battery/wall/solar), Light (LED/halogen), Control (switch/app/voice), Size (desk/floor/wall)
Total: 3 × 2 × 3 × 3 = 54 configurations
Promising: Battery + LED + App + Desk (portable smart lamp)
```

**TRIZ (Electric Vehicle):**
```
Contradiction: Increase range → worsens cost (large battery expensive)
Principles: #6 (Universality - battery is structure), #35 (Parameter change - different chemistry)
Solution: Structural battery pack with high energy density cells
```

**Combined MA + TRIZ:**
```
1. Build morphological box → Find promising configurations
2. Identify contradictions in top configs
3. Apply TRIZ to eliminate trade-offs
4. Re-evaluate configs with contradictions resolved
```

---

## Notes

**Morphological Analysis:**
- Keep 3-7 parameters (too many = explosion)
- Ensure independence (changing one doesn't force another)
- Don't enumerate all combinations (focus on promising clusters)

**TRIZ:**
- Verify real contradiction (not just budget constraint)
- Adapt principles creatively (metaphorical, not literal)
- Combine multiple principles for stronger solutions
- Check for new contradictions introduced by solution

**For advanced techniques:**
- Trends of evolution → See methodology.md Section 1
- Substance-field analysis → See methodology.md Section 2
- ARIZ algorithm → See methodology.md Section 3
- Detailed principle examples → See methodology.md Section 4

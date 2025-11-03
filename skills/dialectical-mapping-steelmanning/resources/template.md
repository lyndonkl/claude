# Dialectical Mapping & Steelmanning - Template

## Workflow

Copy this checklist and track your progress:

```
Dialectical Mapping Progress:
- [ ] Step 1: Frame the debate and clarify binary
- [ ] Step 2: Steelman Position A
- [ ] Step 3: Steelman Position B
- [ ] Step 4: Create tradeoff matrix
- [ ] Step 5: Synthesize third way
- [ ] Step 6: Finalize document
```

**Step 1: Frame the debate**

Identify topic, two positions, and why it's framed as binary. See [Debate Framing](#debate-framing) for structure.

**Step 2: Steelman Position A**

Present Position A in strongest form using [Steelmanning Template](#steelmanning-template). Include principle, best arguments, evidence, and legitimate tradeoffs.

**Step 3: Steelman Position B**

Present Position B with same rigor. Use [Steelmanning Template](#steelmanning-template). Ensure symmetry.

**Step 4: Create tradeoff matrix**

Map what each position optimizes for vs sacrifices. Use [Tradeoff Matrix Template](#tradeoff-matrix-template).

**Step 5: Synthesize third way**

Find higher-order principle or hybrid approach. Use [Synthesis Template](#synthesis-template) and [Synthesis Patterns](#synthesis-patterns).

**Step 6: Finalize document**

Create `dialectical-mapping-steelmanning.md` using [Document Structure](#document-structure). Self-check with [Quality Checklist](#quality-checklist).

---

## Document Structure

Use this structure for the final `dialectical-mapping-steelmanning.md` file:

```markdown
# Dialectical Mapping: [Topic]

## 1. Debate Framing

**Topic**: [What decision or question is being debated?]

**Position A (Thesis)**: [Brief statement of first position]

**Position B (Antithesis)**: [Brief statement of opposing position]

**Why Binary**: [Why is this framed as "pick one or the other"? What makes it feel like a forced choice?]

**Context & Stakes**: [What's the impact of this decision? Who's affected? What constraints exist?]

## 2. Steelman Position A (Thesis)

**Underlying Principle**: [What core value does Position A optimize for? Speed? Safety? Freedom? Equity? Efficiency?]

**Best Arguments**:
1. [Strongest argument for Position A]
2. [Second strongest argument]
3. [Supporting evidence or examples]

**What It Optimizes For**:
- [Primary value maximized]
- [Secondary benefits]

**What It Sacrifices**:
- [Primary costs or risks accepted]
- [Secondary tradeoffs]

**Steelman Summary**: [1-2 sentence charitable interpretation that adherents would recognize as fair]

## 3. Steelman Position B (Antithesis)

**Underlying Principle**: [What core value does Position B optimize for?]

**Best Arguments**:
1. [Strongest argument for Position B]
2. [Second strongest argument]
3. [Supporting evidence or examples]

**What It Optimizes For**:
- [Primary value maximized]
- [Secondary benefits]

**What It Sacrifices**:
- [Primary costs or risks accepted]
- [Secondary tradeoffs]

**Steelman Summary**: [1-2 sentence charitable interpretation that adherents would recognize as fair]

## 4. Tradeoff Matrix

| Dimension | Position A | Position B | Synthesis |
|-----------|------------|------------|-----------|
| **[Principle 1]** | [A's stance] | [B's stance] | [Synthesis approach] |
| **[Principle 2]** | [A's stance] | [B's stance] | [Synthesis approach] |
| **[Principle 3]** | [A's stance] | [B's stance] | [Synthesis approach] |
| **Primary Risk** | [A's risk] | [B's risk] | [Synthesis risk] |
| **Best Case** | [A's upside] | [B's upside] | [Synthesis upside] |
| **Worst Case** | [A's downside] | [B's downside] | [Synthesis downside] |

**Key Insight**: [What does the tradeoff matrix reveal about the tension? Are principles actually opposed, or is there a false dichotomy?]

## 5. Synthesis (Third Way)

**Higher-Order Principle**: [What meta-principle transcends the binary? What do both positions ultimately want?]

**Synthesis Approach**: [Describe the third way. How does it honor both positions' core values? What's the new structure/strategy?]

**Why This Transcends the Binary**:
- [How it preserves Position A's core value]
- [How it preserves Position B's core value]
- [Why it's not just a compromise or split-the-difference]

**New Tradeoffs** (What Synthesis Sacrifices):
- [Primary cost of synthesis vs pure Position A]
- [Primary cost of synthesis vs pure Position B]
- [New risks or challenges introduced]

**Decision Criteria**: [When would you choose synthesis vs pure Position A/B? What conditions make synthesis appropriate?]

## 6. Recommendation

**Recommended Approach**: [Synthesis | Position A | Position B | Conditional (A if X, B if Y)]

**Rationale**: [1-2 paragraphs explaining why this is the best path given context, constraints, and stakeholder values]

**Implementation**: [High-level steps to execute this approach]
1. [First action]
2. [Second action]
3. [Third action]

**Success Criteria**: [How will you know this is working? What metrics or signals indicate the right choice?]

**Reassessment Triggers**: [What would make you revisit this decision? When should you switch approaches?]
```

---

## Debate Framing

**Template**:

- **Topic**: [What's being debated? Be specific about the decision or question]
- **Position A**: [Concise statement of first position—what they advocate]
- **Position B**: [Concise statement of opposing position]
- **Why Binary**: Common reasons include:
  - Resource constraint (budget for A or B, not both)
  - Timing (must decide now, can't defer)
  - Architecture (choosing A locks out B)
  - Culture (A and B represent competing values)
  - Zero-sum framing (gain in A = loss in B)
- **Context**: Who's involved, what's at stake, constraints, deadline

**Example**:

- **Topic**: Should we build our CRM in-house or buy Salesforce?
- **Position A (Build)**: Custom-build CRM tailored to our unique workflow
- **Position B (Buy)**: Purchase Salesforce and customize with config/integrations
- **Why Binary**: Budget constraints (license fees vs eng salaries), time pressure (need CRM in 6 months), and perceived all-or-nothing choice
- **Context**: 50-person startup, complex sales process, engineering team prefers building, ops team wants standard tool

---

## Steelmanning Template

**For Position A / Position B** (use once for each):

### Underlying Principle

What core value does this position optimize for? Examples:
- **Speed**: Get to market fast, iterate quickly, fail fast
- **Quality**: Reliability, correctness, robustness, polish
- **Freedom**: Autonomy, flexibility, optionality, choice
- **Safety**: Risk mitigation, compliance, security, stability
- **Equity**: Fairness, access, inclusion, leveling playing field
- **Efficiency**: Resource optimization, cost reduction, ROI maximization
- **Innovation**: Novelty, differentiation, creative destruction
- **Simplicity**: Ease of use, maintainability, reduced cognitive load
- **Power**: Capability, expressiveness, advanced use cases

### Best Arguments

List 3-5 strongest arguments for this position:
1. **[Argument headline]**: [1-2 sentences explaining the argument. Include evidence, examples, or logic.]
2. **[Second argument]**: [Description]
3. **[Third argument]**: [Description]

Ask: "Are these arguments presented in their strongest form? Would a proponent of this view agree?"

### What It Optimizes For

Primary and secondary benefits:
- **Primary**: [Main value maximized]
- **Secondary**: [Additional benefits, positive externalities]

### What It Sacrifices

Legitimate tradeoffs this position accepts:
- **Primary cost**: [What's given up for the primary value]
- **Secondary costs**: [Other downsides or risks]

**Critical**: Don't hide or minimize costs. Steelmanning requires acknowledging tradeoffs honestly.

### Steelman Summary

Write 1-2 sentence charitable interpretation. Test: "Would someone who holds this position recognize this as a fair representation?"

**Good example**: "Position A prioritizes speed to market because in winner-take-most markets, early movers capture network effects that compound indefinitely, making later entry economically unviable. While this accepts higher risk of early failure, the potential upside of market leadership justifies the gamble."

**Bad example** (strawman): "Position A wants to move fast because they're impatient and don't care about quality."

---

## Tradeoff Matrix Template

Create a table comparing positions across multiple dimensions:

| Dimension | Position A | Position B | Synthesis |
|-----------|------------|------------|-----------|
| **[Principle 1]** | [A's approach] | [B's approach] | [How synthesis handles this] |
| **[Principle 2]** | [A's approach] | [B's approach] | [Synthesis approach] |
| **Speed** | [Fast/Slow/Medium] | [Fast/Slow/Medium] | [Synthesis speed] |
| **Quality** | [High/Medium/Low] | [High/Medium/Low] | [Synthesis quality] |
| **Cost** | [$X upfront + $Y recurring] | [$X upfront + $Y recurring] | [Synthesis cost] |
| **Flexibility** | [High/Medium/Low] | [High/Medium/Low] | [Synthesis flexibility] |
| **Risk** | [Primary risk type] | [Primary risk type] | [Synthesis risks] |
| **Best Case** | [If everything goes right] | [If everything goes right] | [Synthesis upside] |
| **Worst Case** | [If things go wrong] | [If things go wrong] | [Synthesis downside] |

**Fill in synthesis column after developing synthesis approach.**

**Example (Build vs Buy CRM)**:

| Dimension | Build In-House | Buy Salesforce | Synthesis (Buy + Custom) |
|-----------|----------------|----------------|--------------------------|
| **Control** | Full control over features/roadmap | Limited to SFDC roadmap | Core on SFDC, custom extensions for differentiators |
| **Speed to Launch** | 12-18 months (from scratch) | 2-3 months (config + training) | 4-6 months (SFDC + custom integrations) |
| **Cost (3 years)** | $1.5M (eng salaries, no licenses) | $500K (licenses, minimal dev) | $800K (licenses + targeted eng) |
| **Flexibility** | Any feature possible | Constrained by SFDC platform | Moderate—use SFDC for 80%, build 20% |
| **Maintenance Burden** | High (own all code) | Low (SFDC handles platform) | Moderate (own integrations only) |
| **Best Case** | Perfect fit, competitive moat from unique CRM | Fast deployment, proven platform | Fast start + differentiation where it matters |
| **Worst Case** | 18 months, still not done, team burnt out | Locked into ill-fitting platform, workarounds everywhere | Integration complexity, stuck between two worlds |

---

## Synthesis Template

### Higher-Order Principle

What meta-goal do both positions serve? Examples:
- **Maximize customer value**
- **Minimize risk-adjusted time to outcome**
- **Optimize for learning velocity**
- **Balance exploration and exploitation**
- **Achieve sustainable competitive advantage**

### Synthesis Approach

Describe the third way in 2-3 paragraphs:

1. **Structure**: What's the new approach? How does it work?
2. **A's Core Value**: How does synthesis preserve what Position A cares most about?
3. **B's Core Value**: How does synthesis preserve what Position B cares most about?
4. **Why Not Compromise**: Explain why this transcends the binary rather than splitting difference.

### New Tradeoffs

Be explicit about costs:
- **vs Position A**: [What does synthesis sacrifice compared to pure A?]
- **vs Position B**: [What does synthesis sacrifice compared to pure B?]
- **New challenges**: [What new problems does synthesis introduce?]

### Decision Criteria

When is synthesis appropriate vs pure positions?

**Choose Synthesis if**:
- [Condition 1]
- [Condition 2]

**Choose Position A if**:
- [Condition where A is better]

**Choose Position B if**:
- [Condition where B is better]

---

## Synthesis Patterns

### Pattern 1: Temporal Synthesis (Sequence Over Time)

**Structure**: Do A first, then transition to B. Or: A in early phases, B in later phases.

**Example**: Speed vs Quality → Move fast during exploration, tighten quality before launch.

**Template**:
- **Phase 1 (Time X to Y)**: Apply Position A because [reason]
- **Transition**: Shift when [trigger condition]
- **Phase 2 (Time Y to Z)**: Apply Position B because [reason]

### Pattern 2: Conditional Synthesis (Context-Dependent)

**Structure**: Use A in situations X, B in situations Y. Define clear decision criteria.

**Example**: Centralized vs Decentralized → Centralize strategy, decentralize execution.

**Template**:
- **Use Position A when**: [Condition 1], [Condition 2]
- **Use Position B when**: [Condition 3], [Condition 4]
- **Decision criteria**: [How to determine which context you're in]

### Pattern 3: Dimensional Separation (Orthogonal Axes)

**Structure**: Optimize A on one dimension, B on orthogonal dimension.

**Example**: Simple vs Powerful → Simple by default, power user mode available.

**Template**:
- **Dimension 1 (e.g., default UX)**: Optimize for Position A
- **Dimension 2 (e.g., advanced mode)**: Optimize for Position B
- **Rationale**: Dimensions are independent—can achieve both simultaneously.

### Pattern 4: Higher-Order Principle (Reframe Goal)

**Structure**: A and B are tactics. Find better tactic for shared goal.

**Example**: Build vs Buy → Neither—rent/SaaS. Or: Build differentiator, buy commodity.

**Template**:
- **Shared goal**: [What do both A and B ultimately want?]
- **A's limitation**: [Why A is suboptimal for goal]
- **B's limitation**: [Why B is suboptimal for goal]
- **Alternative C**: [New approach that serves goal better]

### Pattern 5: Compensating Controls (Lean + Safeguard)

**Structure**: Lean toward A (primary goal), add B's protections as guardrails.

**Example**: Move Fast vs Prevent Errors → Move fast + automated tests + staged rollouts + quick rollback.

**Template**:
- **Primary approach**: Position A (optimizes for [value])
- **Compensating controls from B**: [Safeguard 1], [Safeguard 2]
- **Result**: A's benefits with B's risk mitigation

---

## Quality Checklist

Before finalizing, verify:

**Debate Framing**:
- [ ] Topic clearly stated
- [ ] Both positions defined concisely
- [ ] Binary framing explained (why it feels like forced choice)
- [ ] Context and stakes documented

**Steelmanning**:
- [ ] Position A presented in strongest form
- [ ] Position B presented in strongest form
- [ ] Symmetry: both positions get equal charitable treatment
- [ ] Underlying principles identified (not just surface preferences)
- [ ] Best arguments for each position articulated
- [ ] Tradeoffs explicitly acknowledged for both
- [ ] Steelman test: "Would proponent of each view recognize this as fair?"

**Tradeoff Matrix**:
- [ ] Multiple dimensions compared (not just binary)
- [ ] Quantitative where possible (cost, time, metrics)
- [ ] Best case and worst case for each position
- [ ] Primary risks identified

**Synthesis**:
- [ ] Higher-order principle articulated
- [ ] Synthesis approach described in detail
- [ ] Explanation of how it preserves A's core value
- [ ] Explanation of how it preserves B's core value
- [ ] Why it transcends binary (not just compromise) explained
- [ ] New tradeoffs explicitly stated
- [ ] Decision criteria provided (when to use synthesis vs pure positions)

**Overall**:
- [ ] Analysis avoids strawman arguments
- [ ] No false equivalence (if one position clearly stronger, noted)
- [ ] False dichotomy checked (is binary real or manufactured?)
- [ ] Recommendation includes implementation steps
- [ ] Success criteria and reassessment triggers defined

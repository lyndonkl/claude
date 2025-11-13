# Meta Prompt Engineering Template

## Workflow

```
Prompt Engineering Progress:
- [ ] Step 1: Analyze baseline prompt
- [ ] Step 2: Define role and objective
- [ ] Step 3: Structure task steps
- [ ] Step 4: Add constraints and format
- [ ] Step 5: Include quality checks
- [ ] Step 6: Test and refine
```

**Step 1: Analyze baseline prompt**
Document current prompt and its failure modes. See [Failure Mode Analysis](#failure-mode-analysis).

**Step 2: Define role and objective**
Complete [Role & Objective](#role--objective-section) section. See [Role Selection Guide](#role-selection-guide).

**Step 3: Structure task steps**
Break down [Task](#task-section) into numbered steps. See [Task Decomposition](#task-decomposition-guide).

**Step 4: Add constraints and format**
Specify [Constraints](#constraints-section) and [Output Format](#output-format-section). See [Constraint Patterns](#common-constraint-patterns).

**Step 5: Include quality checks**
Add [Quality Checks](#quality-checks-section) for self-evaluation. See [Check Design](#quality-check-design).

**Step 6: Test and refine**
Run 5-10 times, measure consistency. See [Testing Protocol](#testing-protocol).

---

## Quick Template

Copy this structure to `meta-prompt-engineering.md`:

```markdown
# Engineered Prompt: [Name]

## Role & Objective

**Role:** You are a [specific role] with expertise in [domain/skills].

**Objective:** Your goal is to [specific, measurable outcome] for [target audience].

**Priorities:** You should prioritize [values/principles in order].

## Task

Complete the following steps in order:

1. **[Step 1 name]:** [Clear instruction with deliverable]
   - [Sub-requirement if needed]
   - [Expected output format for this step]

2. **[Step 2 name]:** [Clear instruction building on step 1]
   - [Sub-requirement]
   - [Expected output]

3. **[Step 3 name]:** [Synthesis or final step]
   - [Requirements]
   - [Final deliverable]

## Constraints

**Format:**
- Output must be [structure: JSON/markdown/sections]
- Use [specific formatting rules]

**Length:**
- [Section/total]: [min]-[max] [words/characters/tokens]
- [Other length specifications]

**Tone & Style:**
- [Tone]: [Professional/casual/technical/etc.]
- [Reading level]: [Target audience literacy]
- [Vocabulary]: [Domain-specific/accessible/etc.]

**Content:**
- **Must include:** [Required elements, citations, data]
- **Must avoid:** [Prohibited content, stereotypes, speculation]
- **Accuracy:** [Fact-checking requirements, uncertainty handling]

## Output Format

```
[Show exact structure expected, e.g.:]

## Section 1: [Name]
[Description of what goes here]

## Section 2: [Name]
[Description]

...
```

## Quality Checks

Before finalizing your response, verify:

- [ ] **[Criterion 1]:** [Specific, measurable check]
  - Test: [How to verify this criterion]
  - Fix: [What to do if it fails]

- [ ] **[Criterion 2]:** [Specific check]
  - Test: [Verification method]
  - Fix: [Correction approach]

- [ ] **[Criterion 3]:** [Specific check]
  - Test: [How to verify]
  - Fix: [How to correct]

**If any check fails, revise before responding.**

## Examples (Optional)

### Example 1: [Scenario]
**Input:** [Example input]
**Expected Output:**
```
[Show desired output format and content]
```

### Example 2: [Different scenario]
**Input:** [Example input]
**Expected Output:**
```
[Show desired output]
```

---

## Notes
- [Any additional context, edge cases, or clarifications]
- [Known limitations or assumptions]
```

---

## Role Selection Guide

**Choose role based on desired expertise and tone:**

**Expert Roles** (authoritative, specific knowledge):
- "Senior software architect" → technical design decisions
- "Medical researcher" → scientific accuracy, citations
- "Financial analyst" → quantitative rigor, risk assessment
- "Legal counsel" → compliance, liability considerations

**Assistant Roles** (helpful, collaborative):
- "Technical writing assistant" → documentation, clarity
- "Research assistant" → information gathering, synthesis
- "Data analyst assistant" → analysis support, visualization

**Critic/Reviewer Roles** (evaluative, quality-focused):
- "Code reviewer" → find bugs, suggest improvements
- "Editor" → prose quality, clarity, consistency
- "Security auditor" → vulnerability identification

**Creator Roles** (generative, imaginative):
- "Content strategist" → engaging narratives, messaging
- "Product designer" → user experience, interaction
- "Marketing copywriter" → persuasive, benefit-focused

**Key Principle:** More specific role = more consistent, domain-appropriate outputs

---

## Task Decomposition Guide

**Break complex tasks into 3-7 clear steps:**

**Pattern 1: Sequential (each step builds on previous)**
```
1. Gather/analyze [input]
2. Identify [patterns/issues]
3. Generate [solutions/options]
4. Evaluate [against criteria]
5. Recommend [best option with rationale]
```
Use for: Analysis → synthesis → recommendation workflows

**Pattern 2: Parallel (independent subtasks)**
```
1. Address [dimension A]
2. Address [dimension B]
3. Address [dimension C]
4. Synthesize [combine A, B, C]
```
Use for: Multi-faceted problems with separate concerns

**Pattern 3: Iterative (refine through cycles)**
```
1. Create initial [draft/solution]
2. Self-critique against [criteria]
3. Revise based on critique
4. Final check and polish
```
Use for: Quality-critical outputs, creative work

**Each step should specify:**
- Clear action verb (Analyze, Generate, Evaluate, etc.)
- Expected deliverable (list, table, paragraph, code)
- Success criteria (what "done" looks like)

---

## Common Constraint Patterns

### Length Constraints
```
**Total:** 500-750 words
**Sections:**
- Introduction: 100-150 words
- Body: 300-450 words (3 paragraphs, 100-150 each)
- Conclusion: 100-150 words
```

### Format Constraints
```
**Structure:** JSON with keys: "summary", "analysis", "recommendations"
**Markdown:** Use ## for main sections, ### for subsections, code blocks for examples
**Lists:** Use bullet points for features, numbered lists for steps
```

### Tone Constraints
```
**Professional:** Formal language, avoid contractions, third person
**Conversational:** Friendly, use "you", contractions OK, second person
**Technical:** Domain terminology, assume expert audience, precision over accessibility
**Accessible:** Explain jargon, analogies, assume novice audience
```

### Content Constraints
```
**Must Include:**
- At least 3 specific examples
- Citations for any claims (Author, Year)
- Quantitative data where available
- Actionable takeaways (3-5 items)

**Must Avoid:**
- Speculation without labeling ("I speculate..." or "This is uncertain")
- Personal information (PII)
- Copyrighted material without attribution
- Stereotypes or biased framing
```

---

## Quality Check Design

**Effective quality checks are:**
- **Specific:** Not "Is it good?" but "Does it include 3 examples?"
- **Measurable:** Can be objectively verified (count, check presence, test condition)
- **Actionable:** Clear what to do if check fails
- **Necessary:** Prevents known failure modes

**Examples of good quality checks:**

```
- [ ] **Completeness:** All required sections present (Introduction, Body, Conclusion)
  - Test: Count sections, check headings
  - Fix: Add missing sections with placeholder content

- [ ] **Citation accuracy:** All claims have sources in (Author, Year) format
  - Test: Search for factual claims, verify each has citation
  - Fix: Add citations or remove/hedge unsupported claims

- [ ] **Length compliance:** Total word count 500-750
  - Test: Count words
  - Fix: If under 500, expand examples/explanations. If over 750, condense or remove tangents

- [ ] **No hallucination:** All facts can be verified or are hedged with uncertainty
  - Test: Identify factual claims, ask "Am I certain of this?"
  - Fix: Add "likely", "according to X", or "I don't have current data on this"

- [ ] **Format consistency:** All code examples use ```language syntax```
  - Test: Find code blocks, check for language tags
  - Fix: Add language tags to all code blocks
```

---

## Failure Mode Analysis

**Common prompt problems and diagnoses:**

**Problem: Inconsistent outputs**
- Diagnosis: Underspecified format or structure
- Fix: Add explicit output template, numbered steps, format examples

**Problem: Too short/long**
- Diagnosis: No length constraints
- Fix: Add min-max word/character counts per section

**Problem: Wrong tone**
- Diagnosis: Audience not specified
- Fix: Define target audience, reading level, formality expectations

**Problem: Hallucination**
- Diagnosis: No uncertainty expression required
- Fix: Add "If uncertain, say so" + fact-checking requirements

**Problem: Missing key information**
- Diagnosis: Required elements not explicit
- Fix: List "Must include: [element 1], [element 2]..."

**Problem: Unsafe/biased content**
- Diagnosis: No content restrictions
- Fix: Explicitly prohibit problematic content types, add bias check

**Problem: Poor reasoning**
- Diagnosis: No intermediate steps required
- Fix: Require chain-of-thought, show work, numbered reasoning

---

## Testing Protocol

**1. Baseline test (3 runs):**
- Run prompt 3 times with same input
- Measure: Are outputs similar in structure, length, quality?
- Target: >80% consistency

**2. Variation test (5 runs with input variations):**
- Slightly different inputs (edge cases, different domains)
- Measure: Does prompt generalize or break?
- Target: Consistent quality across variations

**3. Failure mode test:**
- Intentionally trigger known issues
- Examples: very short input, ambiguous request, edge case
- Measure: Does prompt handle gracefully?
- Target: No crashes, reasonable fallback behavior

**4. Consistency metrics:**
- Length: Standard deviation < 20% of mean
- Structure: Same sections/format in >90% of outputs
- Quality: Human rating variance < 1 point on 5-point scale

**5. Refinement cycle:**
- Identify most common failure (appears in >30% of runs)
- Add specific constraint or check to address it
- Retest
- Repeat until quality threshold met

---

## Advanced Patterns

### Chain-of-Thought Prompting
```
Before providing your final answer:
1. Reason through the problem step-by-step
2. Show your thinking process
3. Consider alternative approaches
4. Only then provide your final recommendation

Format:
**Reasoning:**
[Your step-by-step thought process]

**Final Answer:**
[Your conclusion]
```

### Self-Consistency Checking
```
Generate 3 independent solutions to this problem.
Compare them for consistency.
If they differ significantly, identify why and converge on the most robust answer.
Present your final unified solution.
```

### Constitutional AI Pattern (safety)
```
After generating your response:
1. Review for potential harms (bias, stereotypes, unsafe advice)
2. If found, revise to be more balanced/safe
3. If uncertainty remains, state "This may not be appropriate because..."
4. Only then provide final output
```

### Few-Shot with Explanation
```
Here are examples with annotations:

Example 1:
Input: [X]
Output: [Y]
Why this is good: [Annotation explaining quality]

Example 2:
Input: [A]
Output: [B]
Why this is good: [Annotation]

Now apply the same principles to: [actual input]
```

---

## Domain-Specific Templates

### Code Generation
```
Role: Senior [language] developer
Task:
1. Understand requirements
2. Design solution (explain approach)
3. Implement with error handling
4. Add tests (>80% coverage)
5. Document with examples

Constraints:
- Follow [style guide]
- Handle edge cases: [list]
- Security: No [vulnerabilities]
Quality Checks:
- Compiles/runs without errors
- Tests pass
- Handles all edge cases listed
```

### Content Writing
```
Role: [Type] writer for [audience]
Task:
1. Hook: Engaging opening
2. Body: 3-5 main points with examples
3. Conclusion: Actionable takeaways

Constraints:
- [Length]
- [Reading level]
- [Tone]
- SEO: Include "[keyword]" naturally

Quality Checks:
- Hook grabs attention in first 2 sentences
- Each main point has concrete example
- Takeaways are actionable (verb-driven)
```

### Data Analysis
```
Role: Data analyst
Task:
1. Describe data (shape, types, missingness)
2. Explore distributions and relationships
3. Test hypotheses with appropriate statistics
4. Visualize key findings
5. Summarize actionable insights

Constraints:
- Use [tools/libraries]
- Statistical significance: p<0.05
- Visualizations: Clear labels, legends

Quality Checks:
- All analyses justified methodologically
- Visualizations self-explanatory
- Insights tied to business/research questions
```

---

## Quality Checklist

Before finalizing your engineered prompt:

**Structural:**
- [ ] Role clearly defined with relevant expertise
- [ ] Objective is specific and measurable
- [ ] Task broken into 3-7 numbered steps
- [ ] Each step has clear deliverable

**Constraints:**
- [ ] Output format explicitly specified
- [ ] Length requirements stated (if relevant)
- [ ] Tone/style defined for target audience
- [ ] Content requirements listed (must include/avoid)

**Quality:**
- [ ] 3-5 quality checks included
- [ ] Checks are specific and measurable
- [ ] Known failure modes addressed
- [ ] Self-correction instruction included

**Testing:**
- [ ] Tested 3-5 times for consistency
- [ ] Consistency >80% across runs
- [ ] Edge cases handled appropriately
- [ ] Refined based on failure patterns

**Documentation:**
- [ ] Examples provided (if format is complex)
- [ ] Assumptions stated explicitly
- [ ] Limitations noted
- [ ] File saved as `meta-prompt-engineering.md`

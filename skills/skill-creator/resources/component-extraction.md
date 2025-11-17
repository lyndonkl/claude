# Component Extraction

This resource supports **Step 3** of the Skill Creator workflow.

**Input files:** `$SESSION_DIR/global-context.md`, `$SESSION_DIR/step-2-output.md`, `$SOURCE_DOC` (section-by-section reading)
**Output files:** `$SESSION_DIR/step-3-output.md`, `$SESSION_DIR/step-3-extraction-workspace.md` (intermediate), updates `global-context.md`

**Stage goal:** Extract all actionable components systematically using the interpretive reading approach.

---

## Why Reading Strategy

### WHY Strategy Selection Matters

Different document sizes and structures need different reading approaches:
- **Too large to read at once:** Context overflow, can't hold everything in memory
- **Too structured for linear reading:** Miss relationships between non-adjacent sections
- **Too dense for single pass:** Need multiple focused extractions

**Mental model:** You wouldn't read a 500-page book the same way you read a 10-page article. Match your reading strategy to the document characteristics.

Without a deliberate strategy: context overflow, missed content, inefficient extraction, fatigue.

### WHAT Strategies Exist

Choose based on document characteristics identified in Steps 1-2:

**Three strategies:**

1. **Section-Based:** Document has clear sections < 50 pages. Read one section, extract, write notes, clear, repeat.
2. **Windowing:** Long document > 50 pages without clear breaks. Read 200-line chunks with 20-line overlap.
3. **Targeted:** Hybrid content. Based on Step 2, read only high-value sections identified.

---

### WHAT to Decide

**Present options to user:**
```markdown
## Reading Strategy Options

Based on document analysis:
- Size: [X pages/lines]
- Structure: [Clear sections / Continuous flow]
- Relevant parts: [All / Specific sections]

**Recommended strategy:** [Section-based / Windowing / Targeted]

**Rationale:** [Why this strategy fits]

**Alternative approach:** [If applicable]

Which approach would you like to use?
```

---

## Section-Based Extraction

### WHY Programmatic Approach

Reading entire document into context:
- Floods context with potentially thousands of lines
- Makes it hard to focus on one section at a time
- Risk of losing extracted content before writing it down

**Solution:** Read one section, extract components, write to intermediate file, clear from context, repeat.

### WHAT to Do

#### Step 1: Read Global Context and Previous Output

```bash
# Read what we know so far
Read("$SESSION_DIR/global-context.md")
Read("$SESSION_DIR/step-2-output.md")
```

From step-2-output, you'll have the list of major parts/sections.

#### Step 2: Initialize Extraction File

```bash
# Create extraction workspace
cat > "$SESSION_DIR/step-3-extraction-workspace.md" << 'EOF'
# Component Extraction Workspace

## Sections Processed

[Mark sections as you complete them]

## Extracted Components

[Append after each section]

EOF
```

#### Step 3: Process Each Section

**For each section from step-2-output:**

```bash
# Example for Section 1
# Read just that section from source document
Read("$SOURCE_DOC", offset=[start_line], limit=[section_length])

# Extract components from this section following the guides below:
# - Extract Terms (see Why Extract Terms section)
# - Extract Propositions (see Why Extract Propositions section)
# - Extract Arguments (see Why Extract Arguments section)
# - Extract Solutions (see Why Extract Solutions section)

# Write extraction notes to workspace
cat >> "$SESSION_DIR/step-3-extraction-workspace.md" << 'EOF'

### Section [X]: [Section Name]

**Terms extracted:**
- [Term 1]: [Definition]
- [Term 2]: [Definition]

**Propositions extracted:**
- [Proposition 1]
- [Proposition 2]

**Arguments extracted:**
- [Argument 1]

**Solutions/Examples:**
- [Example 1]

EOF

# Mark section as complete
echo "- [x] Section [X]: [Name]" >> "$SESSION_DIR/step-3-extraction-workspace.md"

# Clear this section from context (it's now in the file)
# Move to next section
```

**Repeat for all sections.**

#### Step 4: Synthesize Extraction Notes

After all sections processed:

```bash
# Read the extraction workspace
Read("$SESSION_DIR/step-3-extraction-workspace.md")

# Synthesize into final step-3-output
# Combine all terms, remove duplicates
# Combine all propositions, identify core ones
# Combine all arguments, identify workflow sequences
# Combine all solutions/examples
```

**Write final output:** (see end of this file for output template)

---

## Why Extract Terms

### WHY Key Terms Matter

Terms are the building blocks of understanding:
- They're the **specialized vocabulary** of the methodology
- Define the conceptual framework
- Must be understood to apply the skill
- Become the "Key Concepts" section of your skill

**Adler's rule:** "Come to terms with the author by interpreting key words."

**Mental model:** Terms are like the variables in an equation. You can't solve the equation without knowing what the variables mean.

Without term extraction: users misunderstand the skill, can't apply it correctly, confusion about core concepts.

### WHAT to Extract

**Look for:** Defined terms, repeated concepts, technical vocabulary, emphasized terms. **Skip:** Common words, one-off mentions.

**Format per term:** Name, Definition, Context (why it matters), Usage (how used in practice).

**How many:** 5-15 terms. Test: Would users be confused without this term?

---

## Why Extract Propositions

### WHY Propositions Matter

Propositions are the **key assertions** or principles:
- They're the "truths" the author claims
- Form the theoretical foundation
- Often become guidelines or principles in your skill
- Different from process steps (those come from arguments)

**Adler's rule:** "Grasp the author's leading propositions by dealing with important sentences."

**Mental model:** Propositions are like theorems in mathematics - fundamental truths that everything else builds on.

Without proposition extraction: shallow skill that misses underlying principles, can't explain WHY the method works.

### WHAT to Extract

**Look for:** Declarative/principle/causal statements. Signal phrases: "key insight", "research shows", "fundamental principle".

**Format per proposition:** Short title, Statement (one sentence), Evidence (why true), Implication (for practice).

**How many:** 5-10 core propositions that explain why methodology works.

---

## Why Extract Arguments

### WHY Arguments Matter

Arguments are the **logical sequences** that connect premises to conclusions:
- They explain HOW the methodology works
- Often become the step-by-step workflow
- Show dependencies and order
- Reveal decision points

**Adler's rule:** "Know the author's arguments by finding them in sequences of sentences."

**Mental model:** Arguments are like algorithms - step-by-step logic from inputs to outputs.

Without argument extraction: missing the procedural flow, unclear how to apply the methodology, no decision logic.

### WHAT to Extract

**Look for:** If-then sequences, step sequences, causal chains, decision trees. Signal phrases: "the process is", "follow these steps", "this leads to".

**Format per argument:** Name, Premise, Sequence (numbered steps), Conclusion, Decision points.

**Map to workflow:** Sequential → linear steps; Decision-tree → branching; Parallel → optional/modular.

---

## Why Extract Solutions

### WHY Solutions Matter

Solutions are the **practical applications** and outcomes:
- They show what success looks like
- Often become examples in your skill
- Reveal edge cases and variations
- Demonstrate application in different contexts

**Adler's rule:** "Determine which of the problems the author has solved, and which they have not."

**Mental model:** Solutions are the "proof" that the methodology works - concrete instances of application.

Without solution extraction: theoretical skill without practical grounding, unclear what success looks like, no examples.

### WHAT to Extract

**Look for:** Examples, case studies, templates, before/after, success criteria. Types: worked examples, templates, checklists, success indicators.

**Format per solution:** Name, Problem, Application (how methodology applied), Outcome, Key factors, Transferability.

**For templates:** Name, Purpose, Structure outline, How to use (steps), Example if available.

---

## Write Step 3 Output

After completing extraction from all sections and getting user validation, write to output file:

```bash
cat > "$SESSION_DIR/step-3-output.md" << 'EOF'
# Step 3: Component Extraction Output

## Key Terms (5-15)

### [Term 1]
**Definition:** [Clear definition]
**Context:** [Why it matters]

### [Term 2]
...

## Core Propositions (5-10)

1. **[Proposition title]:** [Statement]
   - Evidence: [Support]
   - Implication: [For practice]

2. **[Proposition 2]:** ...

## Arguments & Sequences

### Argument 1: [Name]
**Premise:** [Starting condition]
**Sequence:**
1. [Step 1]
2. [Step 2]
**Conclusion:** [Result]
**Decision points:** [Choices]

### Argument 2: ...

## Solutions & Examples

### Example 1: [Name]
**Problem:** [Context]
**Application:** [How applied]
**Outcome:** [Result]

### Example 2: ...

## Gaps Identified

- [Gap 1 to address in synthesis]
- [Gap 2]

## User Validation

**Status:** [Approved / Needs revision]
**User notes:** [Feedback]

EOF
```

**Update global context:**

```bash
cat >> "$SESSION_DIR/global-context.md" << 'EOF'

## Step 3 Complete

**Components extracted:** [X terms, Y propositions, Z arguments, W examples]
**Gaps identified:** [List if any]

EOF
```

**Next step:** Step 4 (Synthesis) will read `global-context.md` + `step-3-output.md`.

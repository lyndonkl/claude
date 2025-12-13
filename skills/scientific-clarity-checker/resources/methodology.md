# Clarity Methodology

This resource supports the Scientific Clarity Checker skill with detailed analysis methods.

---

## Claim Identification

### What Counts as a Claim

A claim is any statement the author wants readers to accept as true. Types include:

**Factual claims:** "X is true" / "Y causes Z"
**Interpretive claims:** "This means..." / "This suggests..."
**Evaluative claims:** "This is significant because..."
**Methodological claims:** "This approach is valid because..."

### How to Extract Claims

1. **Read for conclusions**: Look for conclusion language ("therefore", "thus", "we conclude", "these results demonstrate")

2. **Check section endings**: Claims often appear at the end of sections

3. **Look at figures/tables**: Captions often contain claims

4. **Examine the abstract**: Usually a concentrated list of claims

5. **Review the discussion**: Where interpretation happens

### Claim Extraction Template

```
CLAIM 1:
- Statement: [Exact quote or paraphrase]
- Location: [Page, section, line]
- Type: [Factual/Interpretive/Evaluative/Methodological]
- Strength: [How strongly stated - definitively/tentatively]

CLAIM 2:
[Continue...]
```

---

## Argument Mapping

### Basic Structure

Every argument has:
- **Premises**: Starting points (facts, assumptions, prior results)
- **Inference**: Logical steps from premises to conclusion
- **Conclusion**: What the argument claims to establish

### Mapping Process

1. **Identify the conclusion** first (what is being argued for?)
2. **Find supporting premises** (what evidence/reasons are given?)
3. **Trace the inference** (how does evidence lead to conclusion?)
4. **Check validity** (does the conclusion follow?)

### Common Argument Patterns

**Deductive (if premises true, conclusion must be true):**
```
Premise: All proteins with domain X bind ligand Y
Premise: Protein Z has domain X
Conclusion: Protein Z binds ligand Y
→ Valid if premises are true
```

**Inductive (premises make conclusion probable):**
```
Premise: In 10 experiments, treatment A reduced disease B
Premise: Our experiment shows treatment A reduces disease B
Conclusion: Treatment A generally reduces disease B
→ Strength depends on sample size, consistency
```

**Abductive (inference to best explanation):**
```
Observation: Cells die when gene X is knocked out
Observation: Gene X encodes a protein involved in survival pathway
Conclusion: Gene X is required for cell survival
→ Plausible but alternatives may exist
```

### Identifying Logic Problems

| Problem | Pattern | Fix |
|---------|---------|-----|
| Missing premise | Conclusion needs unstated assumption | Make assumption explicit |
| Non-sequitur | Conclusion doesn't follow from premises | Revise argument or conclusion |
| False dichotomy | Presents only two options when more exist | Acknowledge alternatives |
| Circular reasoning | Conclusion assumed in premise | Identify independent support |
| Hasty generalization | Broad conclusion from limited data | Limit scope of claim |

---

## Terminology Audit

### Process

1. **Create term inventory**: List all technical terms and abbreviations
2. **Check first use**: Is each term defined on first use?
3. **Check consistency**: Is the same term used throughout for same concept?
4. **Check synonyms**: Are different words used for same thing?
5. **Check audience fit**: Are terms appropriate for intended readers?

### Term Inventory Template

| Term | First Use (page) | Defined? | Consistent? | Issues |
|------|------------------|----------|-------------|--------|
| [Term 1] | p.X | Y/N | Y/N | [Notes] |
| [Term 2] | p.X | Y/N | Y/N | [Notes] |

### Common Terminology Issues

**Undefined abbreviations:**
- ❌ "We used CRISPR to edit the gene"
- ✅ "We used CRISPR (Clustered Regularly Interspaced Short Palindromic Repeats) to edit the gene" [on first use only]

**Inconsistent terms:**
- ❌ Alternating "subjects" / "participants" / "patients"
- ✅ Pick one and use consistently

**Ambiguous terms:**
- ❌ "Cells were treated with high concentrations"
- ✅ "Cells were treated with 10 µM compound"

**Jargon for wrong audience:**
- ❌ Heavy jargon in paper for general audience
- ✅ Define or replace with accessible language

---

## Hedging Guide

### Why Hedging Matters

Hedging language (may, might, suggests, indicates) calibrates certainty. Appropriate hedging:
- Protects credibility (don't overclaim)
- Signals confidence level to readers
- Distinguishes speculation from evidence
- Avoids reviewer criticism

### Hedge Calibration Matrix

| Evidence Type | Example | Appropriate Hedge |
|---------------|---------|-------------------|
| Direct mechanistic proof | Biochemical demonstration of binding | "demonstrates", "establishes" |
| Strong correlational, replicated | Multiple cohorts, consistent finding | "shows", "indicates" |
| Moderate correlational | Single study, moderate effect | "suggests", "supports" |
| Preliminary or limited | Pilot data, small n | "may", "appears to" |
| Speculation beyond data | Extrapolation to new context | "could potentially", "we speculate" |

### Hedge Words by Strength

**Strong (use with strong evidence):**
- demonstrates, proves, establishes, shows, confirms

**Moderate (use with good evidence):**
- indicates, reveals, supports, suggests

**Weak (use with limited evidence):**
- may, might, could, appears to, seems to

**Speculative (use beyond data):**
- potentially, conceivably, possibly, we hypothesize, we speculate

### Detecting Miscalibration

**Overclaiming (hedge too strong for evidence):**
- "Our data demonstrate..." (but only correlation)
- "This proves..." (but n=3)
- "We have established..." (but no mechanism)

**Underclaiming (hedge too weak for evidence):**
- "This may suggest..." (but strong direct evidence)
- "could potentially be involved..." (but clearly shown)

**Mixed signals:**
- "strongly suggests" (contradictory)
- "clearly appears to" (contradictory)

### Hedging Checklist

For each major claim:
- [ ] What is the evidence type?
- [ ] What hedge language is used?
- [ ] Does hedge strength match evidence strength?
- [ ] If speculation, is it clearly labeled?

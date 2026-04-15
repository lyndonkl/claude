---
name: research-claim-map
description: Systematically evaluates claims by triangulating sources, rating evidence quality (primary/secondary/tertiary), assessing source credibility, and reaching confidence-rated conclusions to prevent confirmation bias and reliance on unreliable sources. Use when verifying claims before decisions, fact-checking statements, conducting due diligence, evaluating conflicting evidence, or when user mentions "fact-check", "verify this", "is this true", "evaluate sources", "conflicting evidence", or "due diligence".
---

# Research Claim Map

## Table of Contents
1. [Workflow](#workflow)
2. [Evidence Quality Framework](#evidence-quality-framework)
3. [Source Credibility Assessment](#source-credibility-assessment)
4. [Common Patterns](#common-patterns)
5. [Guardrails](#guardrails)
6. [Quick Reference](#quick-reference)

## Workflow

Copy this checklist and track your progress:

```
Research Claim Map Progress:
- [ ] Step 1: Define the claim precisely
- [ ] Step 2: Gather and categorize evidence
- [ ] Step 3: Rate evidence quality and source credibility
- [ ] Step 4: Identify limitations and gaps
- [ ] Step 5: Draw evidence-based conclusion
```

**Step 1: Define the claim precisely**

Restate the claim as a specific, testable assertion. Avoid vague language - use numbers, dates, and clear terms. See [Common Patterns](#common-patterns) for claim reformulation examples.

**Step 2: Gather and categorize evidence**

Collect sources supporting and contradicting the claim. Organize into "Evidence For" and "Evidence Against". For straightforward verification → Use [resources/template.md](resources/template.md). For complex multi-source investigations → Study [resources/methodology.md](resources/methodology.md).

**Step 3: Rate evidence quality and source credibility**

Apply [Evidence Quality Framework](#evidence-quality-framework) to rate each source (primary/secondary/tertiary). Apply [Source Credibility Assessment](#source-credibility-assessment) to evaluate expertise, bias, and track record.

**Step 4: Identify limitations and gaps**

Document what's unknown, what assumptions were made, and where evidence is weak or missing. See [resources/methodology.md](resources/methodology.md) for gap analysis techniques.

**Step 5: Draw evidence-based conclusion**

Synthesize findings into confidence level (0-100%) and actionable recommendation (believe/skeptical/reject claim). Self-check using `resources/evaluators/rubric_research_claim_map.json` before delivering. Minimum standard: Average score ≥ 3.5.

## Evidence Quality Framework

**Rating scale:**

**Primary Evidence (Strongest):**
- Direct observation or measurement
- Original data or records
- First-hand accounts from participants
- Raw datasets, transaction logs
- Example: Sales database showing 10,000 customer IDs

**Secondary Evidence (Medium):**
- Analysis or interpretation of primary sources
- Expert synthesis of multiple primary sources
- Peer-reviewed research papers
- Verified news reporting with primary source citations
- Example: Industry analyst report analyzing public filings

**Tertiary Evidence (Weakest):**
- Summaries of secondary sources
- Textbooks, encyclopedias, Wikipedia
- Press releases, marketing materials
- Anecdotal reports without verification
- Example: Company blog post claiming customer count

**Non-Evidence (Unreliable):**
- Unverified social media posts
- Anonymous claims
- "Experts say" without attribution
- Circular references (A cites B, B cites A)
- Example: Viral tweet with no source

## Source Credibility Assessment

**Evaluate each source on:**

**Expertise (Does source have relevant knowledge?):**
- High: Domain expert with credentials, track record
- Medium: Knowledgeable but not specialist
- Low: No demonstrated expertise

**Independence (Is source biased or conflicted?):**
- High: Independent, no financial/personal stake
- Medium: Some potential bias, disclosed
- Low: Direct financial interest, undisclosed conflicts

**Track Record (Has source been accurate before?):**
- High: Consistent accuracy, corrections when wrong
- Medium: Mixed record or unknown history
- Low: History of errors, retractions, unreliability

**Methodology (How did source obtain information?):**
- High: Transparent, replicable, rigorous
- Medium: Some methodology disclosed
- Low: Opaque, unverifiable, cherry-picked

## Common Patterns

**Pattern 1: Vendor Claim Verification**
- **Claim type**: Product performance, customer count, ROI
- **Approach**: Seek independent verification (analysts, customers), test claims yourself
- **Red flags**: Only vendor sources, vague metrics, "up to X%" ranges

**Pattern 2: Academic Literature Review**
- **Claim type**: Research findings, causal claims
- **Approach**: Check for replication studies, meta-analyses, competing explanations
- **Red flags**: Single study, small sample, conflicts of interest, p-hacking

**Pattern 3: News Fact-Checking**
- **Claim type**: Events, statistics, quotes
- **Approach**: Trace to primary source, check multiple outlets, verify context
- **Red flags**: Anonymous sources, circular reporting, sensational framing

**Pattern 4: Statistical Claims**
- **Claim type**: Percentages, trends, correlations
- **Approach**: Check methodology, sample size, base rates, confidence intervals
- **Red flags**: Cherry-picked timeframes, denominator unclear, correlation ≠ causation

## Guardrails

**Avoid common biases:**
- **Confirmation bias**: Actively seek evidence against your hypothesis
- **Authority bias**: Don't accept claims just because source is prestigious
- **Recency bias**: Older evidence can be more reliable than latest claims
- **Availability bias**: Vivid anecdotes ≠ representative data

**Quality standards:**
- Rate confidence numerically (0-100%), not vague terms ("probably", "likely")
- Document all assumptions explicitly
- Distinguish "no evidence found" from "evidence of absence"
- Update conclusions as new evidence emerges
- Flag when evidence quality is insufficient for confident conclusion

**Ethical considerations:**
- Respect source privacy and attribution
- Avoid cherry-picking evidence to support desired conclusion
- Acknowledge limitations and uncertainties
- Correct errors promptly when found

## Quick Reference

**Resources:**
- **Quick verification**: [resources/template.md](resources/template.md)
- **Complex investigations**: [resources/methodology.md](resources/methodology.md)
- **Quality rubric**: `resources/evaluators/rubric_research_claim_map.json`

**Evidence hierarchy**: Primary > Secondary > Tertiary

**Credibility factors**: Expertise + Independence + Track Record + Methodology

**Confidence calibration**:
- 90-100%: Near certain, multiple primary sources, high credibility
- 70-89%: Confident, strong secondary sources, some limitations
- 50-69%: Uncertain, conflicting evidence or weak sources
- 30-49%: Skeptical, more evidence against than for
- 0-29%: Likely false, strong evidence against

---
name: component-extraction
description: Domain-neutral methodology for the third level of Adler-style reading - extracting structured components (terms, propositions, arguments, solutions) from a document section by section. Selects a reading strategy appropriate to document size and structure (section-based for documents under 50 pages with clear sections; windowing for long documents without breaks; targeted for hybrid content where only specific sections matter). Writes per-section extraction notes that downstream synthesis can consume. Reusable across any extraction workflow - skill creation from a methodology document, Pass-2 content grasp on a paper's full text, evidence-mining from a long-form report. Use when an agent has done structural analysis and now needs to extract the actual atomic content. Trigger keywords - component extraction, section-by-section extraction, extract terms, extract propositions, extract arguments, Adler Level 3, interpretive reading.
---

# component-extraction

The third level of Adler's reading methodology. Builds on `structural-analysis`: now that the document's unity, parts, and problems are mapped, this skill extracts atomic components — terms, propositions, arguments, solutions — section by section.

The extraction is the substrate the downstream synthesis works on. Quality here determines downstream artifact quality.

## Workflow

```
- [ ] Step 1: Choose a reading strategy based on document size and structure
- [ ] Step 2: Initialize a per-section extraction workspace
- [ ] Step 3: For each section in turn — read it, extract terms / propositions / arguments / solutions, write to workspace, clear from context
- [ ] Step 4: Cross-reference (terms used across sections, contradictions across sections)
- [ ] Step 5: Output the consolidated extraction
```

## Inputs

The calling agent passes:
- `source`: the document
- `structural_output`: from `structural-analysis` — gives the parts list and unity statement
- `purpose_context`: e.g., `paper_pass_2_content_grasp`, `skill_extraction_from_methodology`, `evidence_mining`
- `domain_hint`: optional

## Reading strategies

Match strategy to document characteristics from `structural-analysis`. Don't read everything at once — that's how context windows fill and quality drops.

### Strategy 1 — Section-based

**When:** clear sections, document under ~50 pages.

**How:** read one section, extract components for it, write to workspace, clear context, repeat. Each section is a unit of focused attention.

This is the default strategy. Most well-structured documents fit it.

### Strategy 2 — Windowing

**When:** long document over ~50 pages with no clear section breaks (long-form essays, transcripts).

**How:** read 200-line chunks with ~20-line overlap (so context spans the boundary), extract per chunk, dedupe across chunks at the end.

### Strategy 3 — Targeted

**When:** hybrid content where only specific sections from `structural-analysis` are high-value for the calling purpose.

**How:** read only the high-value sections (skip the rest with a note), extract intensively per relevant section.

The calling agent's `purpose_context` determines which sections are high-value.

## What to extract per section

For each section, extract these four component types. Each gets a structured entry.

### Terms (definitions; key concepts)

Words or short phrases the document defines, uses repeatedly, or relies on as load-bearing concepts. Capture:
- The term as written
- Definition (quoted from source, or "definition implicit; inferred from use" if not stated)
- Section reference

Distinguish terms-of-art (specific to this document or field) from generic terms (where the document uses an ordinary word in a normal sense — those don't need extraction).

### Propositions (claims; assertions)

Statements the document makes — claims it wants the reader to accept. Capture:
- Claim text
- Supporting evidence cited (quoted or summarized) or "no support cited"
- Hedging if any (preserve the source's hedge — never promote "suggests" to "shows")

### Arguments (logical sequences from premise to conclusion)

How does the document get from premise A to conclusion C? Capture:
- The premise(s)
- The conclusion
- The reasoning steps (numbered)
- Gaps where present ("step from X to Y is asserted, not derived")

### Solutions (concrete examples; templates; procedures)

Anything the document provides as a model of execution — examples worked through, templates to fill, scripts to run, procedures to follow. Capture:
- The example or template (referenced, not copied wholesale)
- The context it's offered for
- What variation is allowed vs prescribed

## Output structure

A consolidated extraction that the synthesis level (`synthesis-application`) can evaluate.

```markdown
## Component Extraction Output

### Reading strategy used
{section-based | windowing | targeted}
Rationale: {why}

### Per-section extractions

#### Section 1: {name}
**Terms:**
- {term} — {definition} — {section ref}
- ...

**Propositions:**
- {claim} — {evidence or "no support"} — {hedge if any}
- ...

**Arguments:**
- Premises: {list}
  Conclusion: {claim}
  Reasoning: {steps}
  Gaps: {if any}

**Solutions:**
- {example or template} — {context} — {what's variable}

#### Section 2: {name}
... (same structure)

### Cross-section observations
- Terms used across sections (consolidated definitions)
- Contradictions: where section X says A and section Y says not-A
- Reused arguments: where the same logical move appears multiple times
```

## Common patterns

### Pattern A — Skill extraction (call from skill-creator)

`purpose_context=skill_extraction_from_methodology`. Each extracted component becomes a candidate for the SKILL.md being built — terms become the skill's vocabulary, propositions become its claims, arguments become its decision logic, solutions become its examples and templates.

### Pattern B — Paper Pass 2 (call from paper-extractor)

`purpose_context=paper_pass_2_content_grasp`. Per-section extraction maps cleanly to the paper's section structure (intro / methods / results / discussion). The output feeds Pass 2's content-grasp questions: terms become unfamiliar-terms-to-gloss, propositions become the main argument, arguments become the hypothesis-evidence chain, solutions become the figure-by-figure analysis.

### Pattern C — Evidence mining (call from a research-claim-map workflow)

`purpose_context=evidence_mining`. Propositions are the centerpiece — extract every claim with its evidence and hedge, prepare for downstream triangulation across documents.

## Guardrails

1. **Read one section at a time.** Don't load the whole document and try to extract everything at once — context overflow degrades quality.
2. **Quote when capturing.** When extracting a definition or a claim, quote the source phrasing (or note "paraphrased"). Paraphrasing silently introduces drift.
3. **Preserve hedging.** If a proposition says "suggests" or "is consistent with," the extraction says the same. Never promote.
4. **Don't extract what isn't there.** If a section has no extractable terms or solutions, write `{none}`. Don't pad to fit the template.
5. **Flag missing support.** If a proposition has no cited evidence, mark it explicitly. The downstream synthesis-application gate uses this signal.

## Related

- [`structural-analysis`](../structural-analysis/SKILL.md) — Level 2, run before this. Provides the parts list this skill iterates over.
- [`synthesis-application`](../synthesis-application/SKILL.md) — Level 4, run after this. Evaluates the components this skill produced for completeness + logic + applicability.
- [`research-claim-map`](../research-claim-map/SKILL.md) — pairs naturally with the `evidence_mining` purpose; consumes propositions and triangulates.
- The skill-creator skill at `skills/skill-creator/SKILL.md` invokes this skill as its Step 3.
- [`paper-three-pass-extraction`](../paper-three-pass-extraction/SKILL.md) invokes this skill in Pass 2 to produce the structured per-section content used by the synthesizer.

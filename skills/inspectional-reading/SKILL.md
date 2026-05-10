---
name: inspectional-reading
description: Domain-neutral methodology for the first level of Adler-style reading - systematic skimming to determine what kind of document this is, what it's about as a whole, and whether deeper engagement is worth the time investment. Read title, metadata, table of contents or section headings, abstract or introduction, conclusion, and end-material at a glance. Classify document type (methodology, framework, tool, theoretical, reference, or hybrid). Decide whether to escalate to deeper reading. Reusable across any artifact-from-document workflow - paper extraction, skill creation from a methodology document, literature triage, reading-list pruning. Use when an agent needs to convert "I have a document, what is it" into structured downstream-actionable input. Trigger keywords - inspectional reading, systematic skimming, document classification, Adler reading, skim before reading, skill-worthiness check, paper triage, reading triage.
---

# inspectional-reading

The first level of Adler's "How to Read a Book" methodology, applied as a reusable skill. Answers two questions before any deeper reading happens: **What kind of document is this?** and **Is it worth reading carefully?**

The skill is invoked autonomously by an agent — it reads the document and produces structured output. It does not host a dialogue with the operator.

## Workflow

```
- [ ] Step 1: Read the metadata (title, authors, date, source, length)
- [ ] Step 2: Read the abstract / introduction completely
- [ ] Step 3: Examine table of contents or section headings
- [ ] Step 4: Skim the conclusion and any end-material at a glance
- [ ] Step 5: Classify the document type
- [ ] Step 6: Assess worthiness for the calling agent's purpose
- [ ] Step 7: Output structured findings
```

Time budget: 10-15 minutes for a typical paper / chapter / methodology document. If a document needs more, you've drifted into the next level of reading — stop and produce the inspectional output you have.

## Inputs

The calling agent passes:
- `source`: the document to read (path or URL or text)
- `purpose_context`: a short string describing what this document is being read *for*. The classification and worthiness check both depend on this — reading a paper for synthesis vs reading a methodology document for skill extraction yield different worthiness criteria. Examples:
  - `purpose=paper_extraction_for_weekly_digest` — caller is paper-synthesizer's pipeline
  - `purpose=skill_extraction_from_methodology` — caller is the skill-creator agent
  - `purpose=reading_list_triage` — caller wants to rank a backlog
- `domain_hint`: optional. The field the document is in (life sciences, ML, philosophy, etc.) — improves classification.

## Output structure

```markdown
## Inspectional Reading Output

### Metadata
- Source: {path or URL}
- Title: {title}
- Authors / origin: {names or affiliation}
- Length: {pages, sections, or word count}
- Date / version: {date}

### Document type
Primary: {methodology | framework | tool/template | theoretical | reference/catalog | hybrid}
Secondary aspects (if hybrid): {list}

### Stated purpose and audience
{1-2 sentences from the abstract / intro}

### Structural skeleton
{TOC or section headings, in order, as a bullet list}

### Worthiness assessment (for purpose={purpose_context})
- Reusable across multiple contexts: {yes|no|partial} — {one-line rationale}
- Teachable as steps or principles: {yes|no|partial} — {rationale}
- Non-obvious (provides value beyond common sense): {yes|no} — {rationale}
- Complete enough to be actionable: {yes|no|partial} — {rationale}
Recommendation: {ESCALATE to deeper reading | STOP — not worth it | PROCEED with caveats}

### One-line summary
{single sentence, ≤30 words, what this document is}
```

## Document types — quick reference

The classification drives what the calling agent does next. Use the most specific applicable label.

| Type                | Characteristics                                        | Extraction focus                                          | Skill-worthy default                |
| ------------------- | ------------------------------------------------------ | --------------------------------------------------------- | ----------------------------------- |
| Methodology / process | Sequential steps or phases; "first do X, then Y"      | Steps, sequence, inputs/outputs, decision criteria         | Yes — linear workflow              |
| Framework / model   | Dimensions, axes, principles, matrices                 | Dimensions, categories, when-to-apply, interpretation       | Yes — framework with decision logic |
| Tool / template     | Fill-in-the-blank, templates, checklists               | Template structure, what goes where, usage guidelines      | Yes — template with completion docs |
| Theoretical / concept | Explains "why", research findings, principles        | Core concepts, implications, application mappings           | Needs synthesis to be actionable    |
| Reference / catalog | Lists, encyclopedia-like, lookup-oriented              | Usually skip — but extract decision-frameworks if present | Usually NOT skill-worthy            |
| Hybrid              | Combines multiple types                                | Identify boundaries; extract each part by its type         | Yes — partitioned                  |

## Common patterns

### Pattern A — Paper extraction (call from a paper-reading workflow)

`purpose=paper_extraction_for_weekly_digest`. The caller wants to know enough to decide whether to invest deeper-reading compute. Worthiness criteria emphasize: relevance to the watchlist, novelty vs prior weeks, whether the abstract claims something specific or vague. Paper papers fall mostly into "theoretical / empirical study" — apply the next level of reading (content grasp) only when the worthiness check passes.

### Pattern B — Skill extraction (call from skill-creator)

`purpose=skill_extraction_from_methodology`. The caller wants to know whether this document is worth extracting into a SKILL.md. Worthiness criteria emphasize: is the methodology *actionable* (can it be turned into steps a different agent could follow), is it *non-obvious* (does it teach something the model doesn't already know), is it *complete enough* (or are there gaps that would need filling). Reference/catalog documents almost always fail; methodology / framework documents almost always pass.

### Pattern C — Reading-list triage

`purpose=reading_list_triage`. The caller has a backlog of N documents and wants to rank them. Output focuses on the worthiness assessment + one-line summary; classification is secondary.

## Guardrails

1. **Never read past the inspectional level.** If you find yourself reading the methods section in detail, you've drifted into the next reading level — stop.
2. **Always classify against the specific purpose_context.** A document that's gold for paper extraction may fail for skill extraction (or vice versa). The caller's purpose is the lens.
3. **Worthiness has gradations.** ESCALATE / STOP / PROCEED-WITH-CAVEATS — do not collapse to a binary unless the caller explicitly asks for one.
4. **Don't claim a type you can't justify from the structure.** If the TOC has both numbered steps AND framework dimensions, classify hybrid — not "methodology" with hand-waving.
5. **Don't fabricate metadata.** If date or authors aren't visible at the inspectional level, write `(not visible at this level)` rather than guessing.

## Related

- [`paper-three-pass-extraction`](../paper-three-pass-extraction/SKILL.md) — wraps this skill as Pass 1 plus the paper-specific Five Cs framework, then escalates to Pass 2 / Pass 3 for content grasp + deep reading.
- [`structural-analysis`](../structural-analysis/SKILL.md) — the *next* level of reading; called by `paper-three-pass-extraction` Pass 2 and by `skill-creator` Step 2 when this skill recommends ESCALATE.
- [`synthesis-application`](../synthesis-application/SKILL.md) — the completeness-and-logic check that runs in deeper reading levels after this one.
- The skill-creator skill at `skills/skill-creator/SKILL.md` invokes this skill as its Step 1.

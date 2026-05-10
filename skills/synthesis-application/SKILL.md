---
name: synthesis-application
description: Domain-neutral methodology for evaluating completeness and logical soundness of an extracted set of components, then transforming them into actionable guidance. Runs the "is it true / is it complete / what of it" critical evaluation pass before any final artifact is built. Checks for completeness gaps, logical consistency, contradictions, and practical applicability. Reusable across any extraction workflow - skill creation (evaluating extracted components before building SKILL.md), paper extraction (evaluating Pass 2 extraction notes before deep reading), report writing (evaluating gathered evidence before synthesis). Use when an agent has extracted structured components from a source and needs to gate-check before downstream commitment. Trigger keywords - synthesis evaluation, completeness check, logic check, critical evaluation, fact-check before synthesis, gap analysis, what is not said.
---

# synthesis-application

Critical-evaluation gate that runs after component extraction and before final artifact construction. Asks Adler's third-level questions: **"Is it true? What of it?"** Catches logical gaps, missing pieces, contradictions, and practical-applicability issues before they propagate into a downstream artifact.

The skill is invoked autonomously by an agent on a structured set of extracted components. It does not host a dialogue with the operator.

## Workflow

```
- [ ] Step 1: Completeness check — are all major component types present?
- [ ] Step 2: Logic check — do the parts cohere? Any contradictions?
- [ ] Step 3: Applicability check — can this actually be applied?
- [ ] Step 4: Gap-fill recommendations — what would the calling agent need to fill?
- [ ] Step 5: Output structured findings + a single GO / GO-WITH-GAPS / NO-GO verdict
```

## Inputs

The calling agent passes:
- `extracted_components`: a structured payload of what was extracted (terms, propositions, arguments, solutions, hypotheses, etc.). Format depends on caller.
- `purpose_context`: what this is being extracted *for*. The completeness criteria depend on it. Examples:
  - `purpose=skill_construction` — caller is about to build a SKILL.md from these components
  - `purpose=paper_pass_3_input` — caller is about to do a Pass 3 deep read on these components
  - `purpose=evidence_synthesis` — caller is about to write a report from these components
- `domain_hint`: optional, the field the source is in.

## Output structure

```markdown
## Synthesis-and-Application Output

### Completeness check
For each major component type expected for purpose={purpose_context}:
- {Component type}: {present | partial | missing} — {one-line rationale}
- ...

### Logic check
- Gaps: {list of "the artifact jumps from A to C without explaining B" issues, or "none found"}
- Contradictions: {list of "section X contradicts section Y" issues, or "none found"}
- Hidden assumptions: {assumptions stated implicitly that should be made explicit, or "none flagged"}
- Unsupported claims: {claims without evidence or reasoning, or "none flagged"}

### Applicability check
- Concrete enough to act on: {yes | partial | no} — {rationale}
- Decision criteria specified where needed: {yes | partial | no} — {rationale}
- Edge cases covered: {yes | partial | no} — {which edges are unaddressed}

### Gap-fill recommendations
- {Specific item the caller should add or seek before downstream commitment}
- ...

### Verdict
{GO | GO_WITH_GAPS | NO_GO}

Rationale: {2-3 sentences}
```

## Component types by purpose_context

Different downstream artifacts need different inventories of components. The completeness check uses the relevant inventory.

### purpose = skill_construction

A SKILL.md needs:
- **Terms**: key concepts defined unambiguously
- **Propositions**: claims supported by evidence or reasoning
- **Arguments**: complete logical sequences from premise to conclusion
- **Solutions**: concrete examples or templates that demonstrate application
- **Decision criteria**: how to choose between alternatives where the methodology branches
- **Triggers**: when this skill should be invoked

### purpose = paper_pass_3_input

A deep-read needs:
- **Main argument**: the through-line, in 3-5 sentences
- **Big Question**: the field-level problem
- **Hypotheses**: specific claims being tested
- **Evidence inventory**: figures, tables, references that carry the argument
- **Confusions**: what didn't land in Pass 2 — the agenda for Pass 3

### purpose = evidence_synthesis

A report needs:
- **Claims**: structured propositions
- **Sources**: provenance for each claim
- **Source quality**: assessment per source
- **Conflicting evidence**: where sources disagree
- **Confidence ratings**: per-claim

For other `purpose_context` values, the calling agent should specify expected component types in the input — this skill does not silently extend the inventory.

## Logic checks — what to look for

**Gaps** — premises missing between conclusions:
- "The document jumps from A to C without explaining B."
- "Step 5 references something Step 4 doesn't establish."

**Contradictions** — internal conflicts:
- "Proposition 2 says X, but Proposition 7 says not-X."
- "The framework's Dimension 1 and Dimension 3 overlap in unstated ways."

**Hidden assumptions** — load-bearing premises that aren't surfaced:
- "The methodology assumes the user has access to PHI without saying so."
- "The framework only works at scale > 10K users — never stated."

**Unsupported claims** — assertions without backing:
- "Claims X works 80% of the time but cites no source."

The output is the list. The skill does not fix gaps — it surfaces them and recommends action.

## Applicability checks — what to look for

- **Concrete enough to act on**: an extracted "principle" like "always be data-driven" is too vague. Concrete would be "before each sprint, pull last month's metric trend and identify one delta to investigate."
- **Decision criteria specified**: when the methodology branches ("if X, do A; if Y, do B"), is X-vs-Y specified clearly enough that a different agent could follow it?
- **Edge cases covered**: what happens at the boundaries — empty input, conflicting input, error states? If silent on edges, flag.

## Common patterns

### Pattern A — Skill creation gate

`purpose=skill_construction`. Run after Step 3 (component extraction) and before Step 5 (skill construction) in a skill-creation workflow. The verdict gates whether the agent proceeds to build SKILL.md or returns to the source for more extraction.

### Pattern B — Paper Pass 3 readiness

`purpose=paper_pass_3_input`. Run after Pass 2 (content grasp) on a paper extraction. The verdict gates whether Pass 3 is worth running or whether the paper needs re-reading at Pass 2 first.

### Pattern C — Pre-synthesis evidence audit

`purpose=evidence_synthesis`. Run on a research-claim-map output before writing the synthesis report. Catches "the gathered evidence doesn't actually support the conclusion you're about to write."

## Guardrails

1. **Don't fix gaps; surface them.** This skill produces a structured list of issues and a verdict. It does not modify the extracted components. The calling agent decides what to do.
2. **Don't lower the bar on completeness when components are sparse.** GO_WITH_GAPS means "you can proceed but here's what's missing" — not "this is fine because we don't have more."
3. **Verdict matters — don't soften it.** GO / GO_WITH_GAPS / NO_GO is a discrete signal. If you mean NO_GO, write NO_GO. The calling agent's pipeline depends on it.
4. **Don't import information from outside the source.** Completeness is judged against what was extracted, not what the model knows about the topic.

## Related

- [`inspectional-reading`](../inspectional-reading/SKILL.md) — the first reading level, run before extraction begins.
- [`structural-analysis`](../structural-analysis/SKILL.md) — the second level, runs between inspectional and component extraction.
- [`research-claim-map`](../research-claim-map/SKILL.md) — for the evidence-synthesis purpose, the upstream skill that produces the structured claim-source-quality payload this skill evaluates.
- [`negative-contrastive-framing`](../negative-contrastive-framing/SKILL.md) — pairs naturally with the "what is not said" portion of the logic check.
- The skill-creator skill at `skills/skill-creator/SKILL.md` invokes this skill as its Step 4.
- [`paper-three-pass-extraction`](../paper-three-pass-extraction/SKILL.md) invokes this skill before Pass 3 to gate whether a deep read is worth it.

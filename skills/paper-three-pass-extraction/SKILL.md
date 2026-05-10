---
name: paper-three-pass-extraction
description: Domain-neutral methodology for autonomously extracting structured notes from a single academic paper via three escalating passes. Pass 1 (inspectional, ~10-15 min) reads title, abstract, intro, section headings, conclusion, references at a glance, then applies the Five Cs framework (Category, Context, Correctness, Contributions, Clarity). Pass 2 (content grasp, ~30-60 min) reads the full paper skipping proofs, answers main-argument / Big-Question / hypotheses / figure-by-figure / references / confusions. Pass 3 (deep understanding, ~1-4 hours, reserved for important papers) virtually re-implements, challenges every assumption, identifies what is NOT said, asks the falsifiability question. The methodology is internal to the agent applying it - questions are answered against the paper's content, never asked of the operator. Inspired by Keshav 2007 ("How to Read a Paper") and Adler-style inspectional reading. Use when an extraction agent needs to convert dense academic prose into structured machine-and-human-readable notes - bio papers, CS papers, ML papers, statistics, math, any field.
---

# paper-three-pass-extraction

Three-pass methodology for extracting structured notes from a single academic paper. Each pass escalates from cheap-and-shallow to expensive-and-deep; downstream agents trigger Pass 2 only for relevant papers and Pass 3 only on explicit operator request.

The **central principle**: every question in this methodology is answered *by the agent reading the paper*, against the paper's content. Never ask the operator the questions. Never have a Socratic dialogue. The questions are an internal extraction checklist whose purpose is to produce structured output — not user-facing prompts.

## Workflow

```
- [ ] Pass 1: Inspectional reading (always run)
       - Read title, abstract, intro paragraphs, section headings, conclusion, references at a glance
       - Apply the Five Cs framework
       - Produce Pass 1 extraction output
- [ ] Pass 2: Content grasp (run when escalated, e.g., paper passed relevance filter)
       - Acquire full text (PDF or HTML); flag if unavailable
       - Read linearly, skipping proofs and heavy derivations
       - Answer the Pass 2 question set
       - Append Pass 2 extraction output
- [ ] Pass 3: Deep understanding (run only on operator request)
       - Re-read methods + proofs that Pass 2 skipped
       - Virtually re-implement the core idea
       - Answer the Pass 3 question set
       - Append Pass 3 extraction output
```

## Pass 1 — Inspectional Reading

Operates on title, abstract, intro paragraphs, section headings, conclusion, and references at a glance. Never blocks on a missing PDF — abstract-only Pass 1 is acceptable.

### The Five Cs (the agent answers each — not the operator)

1. **Category** — What type of paper is this? Pick the most specific applicable label: empirical study, theoretical analysis, system / architecture description, benchmark, survey / review, meta-analysis, position / perspective, replication, ablation study, dataset release, methods paper, case report. If the paper fits two, pick the dominant frame from the abstract; note the secondary in parentheses.

2. **Context** — What prior work does it build on? What field or debate does it sit within? Look for: explicit citations in the abstract, "extends [X]" / "improves on [X]" phrasing, the institutional / lab pattern in the author list, key references repeated. Output: 1-2 sentences naming the closest prior work and the active debate.

3. **Correctness (first-glance)** — Do the assumptions seem reasonable at first glance? This is *not* a deep critique — Pass 1 hasn't read the methods. Flag obvious issues: claims that contradict well-known results, conclusions that overreach the evidence cited in the abstract, missing comparisons. If nothing obvious, write "no first-glance concerns."

4. **Contributions** — What does the paper claim to add? Quote or paraphrase the abstract's contribution claim. Distinguish: new method / new result / new dataset / new framing / negative result / replication. **Preserve hedging**: if the abstract says "suggests" or "is consistent with," the extraction says the same. Never promote a "suggests" to a "shows."

5. **Clarity** — Is the abstract / structure well-written? Does the title match the abstract? Are claims specific or vague? Output: short signal — `clear`, `dense-but-clear`, `vague`, `mismatched-title`, `acronym-soup`. This guides whether Pass 2 will be easy or painful.

### Pass 1 also produces a `one_line` summary

A single-sentence compression of "what the paper does." Used by upstream callers for quick reporting. Shouldn't exceed ~30 words.

## Pass 2 — Content Grasp

Runs when the caller escalates (typical trigger: paper passed a relevance filter as KEEP). Reads the full paper, skipping proofs and heavy derivations. Needs the full-text source.

### Pass 2 question set (the agent answers — not the operator)

1. **Main argument and supporting evidence — 3 to 5 sentences.** What does the paper argue, and what does it adduce as support? Resist re-stating the abstract; this should reflect the actual structure of the paper as you read it.

2. **The Big Question.** Not what the paper is about — what *problem* the field is trying to solve, of which this paper is one move. Often inferable from the introduction's framing of related work.

3. **Specific hypotheses tested.** List them. If the paper is a systems / engineering paper without explicit hypotheses, list the design claims being defended instead.

4. **Unfamiliar terms / concepts requiring gloss for a non-specialist reader.** These will become candidates for inline glossing in any downstream summary.

5. **Figure-by-figure analysis.** For each figure or table that carries the argument: what is being shown, what's the takeaway, are axes / error bars / sample sizes clean. Skip ornamental figures.

6. **References worth follow-up.** Distinguish *load-bearing* references (the result depends on them) from background citations.

7. **Confusions or unresolved points.** What did not land for you on this read? Mark them — Pass 3 (if escalated) will return to them.

### Pass 2 acquisition order

When fetching full text, try in this order:
1. The paper record's PDF URL (arXiv records always carry one).
2. The paper's URL content (some preprint sites serve full HTML).
3. PMC OA service for PubMed records (only when a free PMC id exists).
4. If none of the above, mark `full_text_available=false` and apply Pass 2 to the abstract + intro you have, with reduced confidence. Do not skip Pass 2 — degraded Pass 2 still beats no Pass 2 for downstream synthesis.

## Pass 3 — Deep Understanding

Runs only on explicit operator request. Time investment: 1-4 hours of agent compute equivalent. Reserved for high-priority papers. **Never auto-trigger.**

### Pass 3 question set

1. **Reconstruct the structure and argument from memory.** Force a from-memory write: the structure of the paper, the argument's flow, the key results, in your own organization. If you cannot reconstruct, you don't yet understand it — return to Pass 2.

2. **Strongest points; weakest points.** Be specific. "The benchmark is standard" is weak praise; "the multi-seed protocol with seeds disclosed in the appendix is unusually rigorous" is real. Same for weaknesses.

3. **Falsifiability — what would have to be true for the conclusions to be wrong?** This is the highest-value question in deep reading. Surface the load-bearing assumptions whose failure would invalidate the result.

4. **What is *not* said?** Hidden assumptions, missing comparisons, citations that should appear but don't, methodological choices that aren't justified.

5. **Future work this opens up.** Concrete next experiments or follow-up questions, not vague "more research needed."

## Common patterns

### Pattern A — Weekly batch literature scan

Pass 1 on every fetched paper (cheap; runs in parallel as subagent batch). Apply the relevance filter on the Pass 1 outputs (richer signal than abstracts alone — the Five Cs answers improve criteria-fit scoring). Pass 2 on the KEEPs. Pass 3 only when the operator points at a specific paper from the digest.

### Pattern B — Single-paper deep read

Operator drops a paper into a focused-review workflow. Run all three passes sequentially, returning each pass's output. Pass 3 is on the table because there's only one paper to invest in.

### Pattern C — Reading-list triage

Operator has 50 papers in a backlog. Pass 1 on all 50 (fast); rank by Pass 1 signals (Category fit, hedging strength, Clarity); recommend top-N for Pass 2.

### Pattern D — Replication / disagreement check

Two papers claim contradictory results. Pass 2 on both with explicit attention to: methodology differences in question 1, hypothesis-testing protocol in question 3, figure protocol differences in question 5. Pass 3 on whichever is the higher-priority claim.

## Guardrails

1. **Never ask the operator any of the methodology questions.** Five Cs, Pass 2 questions, Pass 3 questions — all are answered by the agent against the paper. The questions are an internal extraction checklist, not a dialogue.
2. **Never skip Pass 1 for an unfamiliar paper, even when the caller asked for Pass 2 or Pass 3 directly.** Always run prior passes first; Pass 1's structured frame anchors what follows.
3. **Always preserve hedging.** If a paper says "suggests" or "is consistent with," the extraction says the same. Never promote.
4. **Never invent results not in the paper.** If a number, citation, or figure isn't in the source, don't include it. Write `(not stated)` when uncertain — that's high-information.
5. **Never auto-trigger Pass 3.** Pass 3 is operator-driven. Pass 2 may auto-escalate based on filter results; Pass 3 must not.
6. **Pass 2 without full text is degraded, not skipped.** Mark the file as such and reduce downstream confidence; don't refuse the pass.
7. **Pass 1 stays cheap.** If you're reading the methods section in Pass 1, you've drifted into Pass 2. Stop.

## Quick reference

| Pass | Time      | Trigger                                | Input                                    | Output                                          |
| ---- | --------- | -------------------------------------- | ---------------------------------------- | ----------------------------------------------- |
| 1    | ~10-15min | Always (every paper)                   | Title, abstract, intro, headings, conclusion | Five Cs answers + one_line summary              |
| 2    | ~30-60min | Caller escalates (filter KEEP)         | Full paper text (PDF or HTML), skip proofs | Pass 2 question-set answers, figure analysis    |
| 3    | ~1-4h     | Operator request only — never auto      | Full paper including methods + proofs    | Reconstruction, strongest/weakest, falsifiability, what-is-not-said, future work |

## Related skills

- [`layered-reasoning`](../layered-reasoning/SKILL.md) — the three passes are themselves a layered structure (inspectional / content / deep). Apply layered-reasoning's consistency checks across passes.
- [`scientific-clarity-checker`](../scientific-clarity-checker/SKILL.md) — directly applicable to Pass 1's Clarity assessment and Pass 2's main-argument-vs-evidence check.
- [`research-claim-map`](../research-claim-map/SKILL.md) — applicable to Pass 2's reference triage (load-bearing vs background) and Pass 3's source grading.
- [`hypotheticals-counterfactuals`](../hypotheticals-counterfactuals/SKILL.md) — drives Pass 3's falsifiability question.
- [`negative-contrastive-framing`](../negative-contrastive-framing/SKILL.md) — drives Pass 3's "what is *not* said."
- [`skill-creator/resources/inspectional-reading.md`](../skill-creator/resources/inspectional-reading.md) — the kindred-spirit predecessor scoped to skill creation; same Adler-style reading discipline applied to a different artifact (source documents for skill extraction rather than research papers).
- [`skill-creator/resources/synthesis-application.md`](../skill-creator/resources/synthesis-application.md) — same lineage; provides the completeness-and-logic check pattern that Pass 3's "what is not said" extends.

## Inputs required

- A paper record (id, title, authors, abstract, date, source URL, optional DOI, optional PDF URL)
- The pass to run (1, 2, or 3) — caller's escalation choice
- An output location for the extraction file (path-agnostic; caller decides)

## Outputs produced

A structured markdown file accumulating each pass's output. Multiple passes append; never overwrite a prior pass section. The file is the artifact downstream agents (synthesizer, archiver, search) consume.

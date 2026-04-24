---
name: citation-form-check
description: Verifies every paper or named research result cited in a substacker draft uses the inline "Author(s), Institution, Year" form per style-guide, not a bare hyperlink or title-alone reference. Flags bare-hyperlink citations and missing-institution attributions. Use whenever the draft references external research. Trigger keywords: citation, paper citation, bare hyperlink, authors, institution, reference format.
---

# Citation Form Check

## Table of Contents

- [Correct form](#correct-form)
- [Workflow](#workflow)
- [Worked example](#worked-example)
- [Guardrails](#guardrails)

**Related skills:** Called by Editor in voice pass. Reads `shared-context/style-guide.md` for the citation template.

## Correct form

From `style-guide.md`:

> Papers cited in prose: `Author(s), Institution, Year — Title` on first mention. Not a bare hyperlink, not a title alone.

Examples of correct:
- "Chen et al., Google, 2024 showed that retrieval beats parametric recall at the tail."
- "Vaswani et al. (Google Brain, 2017) introduced the Transformer architecture."
- "Dao et al., 2022, on FlashAttention demonstrated that memory is O(N), not O(N²)."

Examples to flag:
- "[this paper](https://arxiv.org/abs/...)" — bare hyperlink without author + institution.
- "A Google paper said…" — no authors.
- "*Attention Is All You Need*" (title only) — no authors, no year.
- "Recent research shows…" — no citation at all.

## Workflow

```
Citation check draft D:
- [ ] Step 1: Detect paper references (arXiv patterns, italicized titles, hyperlinks to paper sites, "a paper")
- [ ] Step 2: For each reference, parse surrounding sentence for author + institution
- [ ] Step 3: If author OR institution missing, flag tier-2 (unless it's the second+ mention of a paper already correctly cited once)
- [ ] Step 4: Suggest the correct form
```

### Detection patterns

- arXiv URLs: `arxiv.org/abs/\d{4}\.\d{4,5}`
- DOIs: `10\.\d+/\S+`
- Italicized titles: `\*[A-Z][^*]+\*` of length ≥3 words (filters out italicized phrases)
- Hyperlinks to paper sites: `(arxiv|openreview|papers\.nips|proceedings)`
- Generic "a paper" / "recent research" / "a Google paper"

### Exemption

If a paper is correctly cited in full on first mention, subsequent mentions can use a short form ("Chen et al. also noted…"). Only first-mention requires full `Author, Institution, Year`.

## Worked example

**Draft**:
> RAG (as shown in [this paper](https://arxiv.org/abs/2005.11401)) beats fine-tuning for recall.
>
> A Google paper found that retrieval dominates for rare facts.
>
> *Attention Is All You Need* is the foundational work.
>
> Chen et al., Google, 2024 — "Fine-Tuning or Retrieval?" — compared both approaches; Chen et al. concluded fine-tuning loses on tail knowledge.

**Flags**:
1. (Tier-2) "[this paper](https://arxiv.org/abs/2005.11401)" — bare hyperlink. Rewrite: "Lewis et al., FAIR, 2020 — *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*."
2. (Tier-2) "A Google paper" — no authors. Rewrite: insert authors, year, title.
3. (Tier-2) "*Attention Is All You Need*" — title only. Rewrite: "Vaswani et al., Google Brain, 2017 — *Attention Is All You Need*."
4. (PASS) Chen et al. citation is correct on first mention; second mention (short form) is acceptable.

## Guardrails

1. Citation form is tier-2. The writer can publish with a bare hyperlink; it's a craft miss, not a voice violation.
2. Don't flag mentions of blogs, tools, or GitHub projects — only formal research citations.
3. First mention rule: full form required. Subsequent mentions can be short.
4. If the writer uses a different citation template (e.g., footnote-based), respect the style-guide.
5. Never rewrite a citation without the writer's confirmation — suggest only.
6. Don't flag citations the writer explicitly annotates `[short]` in their draft (convention for intentional short-form on first mention).

## Quick reference

- Input: draft + style-guide.md.
- Output: citation flags with tier-2 severity.
- First mention = full form; subsequent mentions = short form.

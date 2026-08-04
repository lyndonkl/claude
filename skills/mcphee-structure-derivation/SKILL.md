---
name: mcphee-structure-derivation
description: Derives a document's structure out of its own corpus instead of picking one off a menu, using John McPhee's coding-and-sorting procedure - cold read, short topic codes one per card, a strict chronology sort run against a strict theme sort, a logged list of every disagreement resolved toward chronology, candidate juxtapositions gated by a state-and-footnote test, a named shape, and an invisibility test. Use when you hold researched material and have no structure yet, when a draft has turned into concept-named sections full of time-scrambled evidence, when deciding whether a flashback is earned, or when user mentions McPhee, coding pass, index cards, deriving structure, chronology versus theme, structure from material, or "what shape is this piece".
---

# McPhee Structure Derivation

## Table of Contents
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [The Dual Sort and Its Resolution](#the-dual-sort-and-its-resolution)
- [Shape Catalog](#shape-catalog)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

**Related skills:** Use `narrative-form-triage` before this skill - it decides the FORM the corpus can support and owns the DO NOT NARRATE refusal, while this one derives the SHAPE once a narrative form has been declared. Use `writing-structure-planner` once components exist - that skill SELECTS among eight known shapes and diagrams the choice; this one DERIVES a shape from raw material and hands the named shape plus the card piles over to it. Use `writing-revision` on the prose after components are drafted, `writing-pre-publish-checklist` for the final gate.

## Core Principles

1. **Derive, do not select**: The shape is an output of sorting cards, not an input chosen before reading. If you named the shape before you coded the corpus, you imposed it.
2. **Chronology wins by default**: McPhee's rule is that tension between chronology and theme is near-universal and chronology usually wins. Theme-sorting is the cheapest operation a language model performs, which is exactly why it must be the one that has to argue for itself.
3. **One code per card, provenance on every card**: The sortable unit is a chunk of researched material with a source, not a heading you invented. A card with no source is not a card.
4. **White space is a claim**: An inference produced by placing two cards side by side escapes citation discipline. Only juxtapose to imply something you would state outright and footnote.
5. **Name the shape or keep sorting**: "Partly chronological, partly thematic, with some flashbacks" is not a name. If it cannot be named, the sort is unfinished.
6. **Invisible bones**: Structure should be about as visible as someone's skeleton. If a reader can recite it after one read, you over-signposted.
7. **Refusal is a result**: "This corpus has no derivable narrative shape; it is a set of independent findings" is a successful terminal output, not a failure.

## Workflow

Copy this checklist and track your progress:

```
McPhee Structure Derivation Progress:
- [ ] Step 1: Cold read, then code the corpus onto cards
- [ ] Step 2: Sort twice and log every disagreement
- [ ] Step 3: Resolve each disagreement toward chronology
- [ ] Step 4: Test candidate juxtapositions against the footnote gate
- [ ] Step 5: Name the shape, then run the invisibility test
- [ ] Step 6: Write component by component, lede last, then hand off
```

**Step 1: Cold read, then code the corpus onto cards**

Step 1.1: Read the entire corpus once, marking nothing, annotating nothing, writing nothing. The purpose is to let patterns surface before your first classification freezes them. Record only the fact that you did it.

Step 1.2: Read again. Assign every chunk a short topic code in airport-code style - `SMELTER-Q3`, `RETRY-STORM`, `LAB-MOVE-32`, `TARIFF-88`. Codes name what the chunk is about. Codes that name a document part (`BACKGROUND`, `ANALYSIS`, `CONTEXT`, `DISCUSSION`) are not topic codes and will silently reproduce a generic essay outline.

Step 1.3: One code per card. Each card carries: code, one-line content, the date or date range the material belongs to, source reference, and a typicality label (median / tail / unique) against the corpus. Cards with an unknown date go to a dated-unknown pile, not to a guessed slot.

See [resources/coding-pass.md](resources/coding-pass.md) for the card schema, the code-quality tests, a worked corpus, and the discarded-card log format.

**Step 2: Sort twice and log every disagreement**

Step 2.1: Sort A - strict chronology. Order every card by its date. No thematic grouping allowed, even where it obviously helps. Write the resulting sequence of codes down.

Step 2.2: Sort B - strict theme. Group every card by topic, ignoring dates entirely. Write that sequence down too.

Step 2.3: Produce the disagreement log: every place the two sorts put the same card in a materially different position. This log is a required artifact. A derivation that reports no disagreements did not run both sorts.

**Step 3: Resolve each disagreement toward chronology**

Step 3.1: Walk the log row by row using [The Dual Sort and Its Resolution](#the-dual-sort-and-its-resolution). Default resolution is chronology.

Step 3.2: Break chronology only where a theme is strong enough to justify a flashback, and only by naming the explicit re-entry point - the dated card the narrative returns to. A flashback with no named re-entry point is a rejected resolution.

Step 3.3: Maintain the discarded-card log with two separate columns: cards that did not support the emerging shape, and cards that contradicted it. The first column may be pruned. The second column must appear in the body of the finished piece.

**Step 4: Test candidate juxtapositions against the footnote gate**

Step 4.1: Identify candidates: which two non-adjacent cards, placed side by side, generate an inference you currently have to assert in a sentence?

Step 4.2: For each candidate, write the inference out as a margin note. Then answer one question: would you state this inference in the text and footnote it with the evidence you hold? If no, discard the juxtaposition. Do not keep it because it is elegant.

Step 4.3: Order surviving pairs so the second card REVISES the first rather than echoing it, and cap them at roughly one per major section (a derived working default, not a published figure).

See [resources/juxtaposition-discipline.md](resources/juxtaposition-discipline.md) for the gate, worked passes and failures, and the adjacency-as-causation cases.

**Step 5: Name the shape, then run the invisibility test**

Step 5.1: Draw the resolved sequence and NAME it from the [Shape Catalog](#shape-catalog). If nothing fits, keep sorting - do not invent a hybrid label to end the step.

Step 5.2: Invisibility test. Ask whether a reader could recite the structure after one read. If yes, delete roadmap sentences ("This piece has three parts", "Having examined X, we now turn to Y") until they cannot.

Step 5.3: Write the shape contract: shape name, runner-up shape, why the runner-up lost, the flashbacks and their re-entry points, the surviving juxtapositions, and the contradicting-card list. The contract is immutable inside a draft. Changing shapes mid-draft requires an explicit logged restart.

**Step 6: Write component by component, lede last, then hand off**

Step 6.1: Write one component at a time, from that component's card pile only. No reaching into other piles for a better line. This is the point of the cards.

Step 6.2: Write the lede last, after the shape is fixed and the components exist.

Step 6.3: Hand the named shape, the component piles, and the shape contract to `writing-structure-planner` for diagramming, gold-coin placement and pacing.

Validate using [resources/evaluators/rubric_mcphee_structure_derivation.json](resources/evaluators/rubric_mcphee_structure_derivation.json). **Minimum standard**: Average score >= 3.5.

## The Dual Sort and Its Resolution

Work the disagreement log with this table. Chronology is the default; every other resolution owes an artifact.

| Disagreement pattern | Concrete instance | Resolve to | Required artifact |
|---|---|---|---|
| A theme collects events months or years apart with no causal dependency between them | Three port strikes in 1971, 1978 and 1984 that a theme sort files together as "labor disruption" | Chronology | None. Cards stay in date order. |
| A later card is unintelligible without an earlier one that chronology puts far behind it | A 1994 retry-storm outage that only makes sense given a 1989 client-library default | Chronology, with the earlier card promoted as a short dated inset inside the later section | One sentence naming the inset and its date |
| The meaning of a theme lives in a comparison across eras, not in either era alone | The same enzyme assay performed in 1957 and in 2003 with opposite conclusions | Theme, but only as a dual or triple profile on an explicitly named common denominator | The denominator, written as one noun phrase |
| The origin material precedes the reader's live interest by years | A protocol's 1996 design meetings versus the 2011 adoption fight the piece is actually about | Chronology beginning late, with one flashback | The named dated re-entry point |
| Two independent contradictions each demand their own spine | A supply chain that is both cost-fragile and politically exposed, with separate evidence bases | Neither - braid or split into two deliverables | A written note of which contradiction was set aside and why |
| Cards are independent findings with no causal chain at all | Six unrelated audit findings sharing only a fiscal year | Neither sort yields narrative | Terminal output: "no derivable narrative shape." Hand to `narrative-form-triage`, which owns the DO NOT NARRATE verdict and picks taxonomy versus chronicle, then to `writing-structure-planner` to diagram the grouped form |

**Failure signature to watch for (theme-sort capture):** five sections named after concepts, each holding evidence from scrambled years, with no accumulating tension anywhere. If your draft looks like that, Sort B captured the derivation and Step 3 was skipped.

**Opposite failure:** slavish chronology laid over material whose meaning genuinely is comparative, producing an undifferentiated timeline. Both failures are detectable from the disagreement log, which is why the log is required.

## Shape Catalog

Name the resolved sequence as one of these. Full descriptions, diagrams and emergence tests live in [resources/shape-catalog.md](resources/shape-catalog.md).

| Shape | Emerges when the sorts show | Person protagonist | System protagonist |
|---|---|---|---|
| Linear | Chronology and theme mostly agree | A career told forward | A standard's revisions in release order |
| Circular | One card is both the strongest entry and the natural close | Open and close on the same hospital shift | Open and close on the same dated shutdown |
| Spiral | The same window revisited at widening radius | One decision, then the family, then the town | One plant, then the firm, then the industry |
| Dual profile | Two card sets on one denominator, meaning in the contrast | Two chemists, one problem | Two ports, one shipping lane |
| Triple profile | Three sets on one common denominator | Three surgeons, one procedure | Three outages, one dependency |
| Geographic traverse | Cards order naturally along a route or physical path | A walk along a fault line | Ore to smelter to cell to pack |
| Braided | Two or three timelines advancing in parallel, cross-cutting | Two rivals, interleaved years | Regulation and market price, interleaved |

Caveat on provenance: McPhee described and drew several of these shapes, but this seven-row list is a working taxonomy assembled by commentators on his 2013 essay, not a canon he codified. Treat the names as vocabulary for the naming step, not as an authoritative set.

Caveat on tooling: McPhee mechanised this sort with purpose-built software - Structur, then Alpha, then a program he called Mac - which slotted coded chunks into their piles automatically. That matters because it tells you the procedure is mechanical by design. It is a filing operation, not an act of taste, and it should feel like one.

## Guardrails

**Requirements:**

1. **Cold read first**: The first pass produces no codes, no notes, no marks. Record that it happened before coding.
2. **Both sorts, written down**: Sort A and Sort B must both exist as written sequences, and the disagreement log must be produced. Skipping Sort A and calling the theme sort "the structure" is the dominant failure this skill exists to prevent.
3. **No card without provenance**: Every card cites a source. Never create a card to fill a hole in an emerging shape. A hole means the shape is wrong, not that you need one more fact.
4. **Footnote gate on every juxtaposition**: The implied inference is written out, and kept only if you would state and cite it. Adjacency is not evidence of causation.
5. **Contradicting cards surface in the body**: The discarded-card log separates "did not support" from "contradicted". The second category is never pruned silently.
6. **Named shape or explicit refusal**: End with a shape name from the catalog, or with the finding that the corpus has none.
7. **Immutable shape contract**: Once named, the shape does not change mid-draft. Structure shopping produces a document that opens as one thing and ends as another, which readers register as untrustworthiness.
8. **Dated events, not periods disguised as moments**: For a system protagonist, a card's "moment" must be a dated filing, price print, release, incident or failed test. "Through the late 1990s" is a summary card, and label it as one.

**Common pitfalls:**
- Coding chunks with document-part labels (`BACKGROUND`, `IMPLICATIONS`) rather than topic codes, which reproduces a generic outline under a McPhee-shaped process.
- Declaring a flashback without naming the re-entry point, so the piece leaves the timeline and never returns.
- Keeping a juxtaposition because it is elegant after it failed the footnote test.
- Flattening genuinely multi-causal material into one shape because a single mechanism is tidier, without logging what was set aside.
- Writing the lede early, which quietly fixes the shape before the sorts are resolved.
- Reaching outside a component's card pile while drafting it, which dissolves the piles back into an undifferentiated corpus.
- Letting personifying verbs ("the market decided", "the protocol wanted") carry causal claims the cards do not support.

## Quick Reference

**Key resources:**
- **[resources/coding-pass.md](resources/coding-pass.md)**: card schema, code-quality tests, a fully worked corpus from cold read to named shape, disagreement log and discarded-card log formats
- **[resources/shape-catalog.md](resources/shape-catalog.md)**: seven shapes with emergence tests, diagrams, person and system variants, and each shape's failure signature
- **[resources/juxtaposition-discipline.md](resources/juxtaposition-discipline.md)**: the state-and-footnote gate, passing and failing worked pairs, revision-versus-echo ordering, adjacency-as-causation cases
- **[resources/evaluators/rubric_mcphee_structure_derivation.json](resources/evaluators/rubric_mcphee_structure_derivation.json)**: quality scoring

**Inputs required:**
- A researched corpus with sources attached (notes, transcripts, documents, logs, datasets, extracted claims)
- Dates or date ranges for as much of the material as the record supports
- Any known audience constraint (obligated reader, voluntary reader, length limit)

**Outputs produced:**
- A coded card set with provenance and typicality labels
- Sort A (chronology), Sort B (theme), and the disagreement log
- Resolutions, with re-entry points named for every flashback
- Surviving juxtapositions with their written-out inferences
- A named shape and a shape contract, or an explicit "no derivable shape" finding
- Component card piles ready for `writing-structure-planner`

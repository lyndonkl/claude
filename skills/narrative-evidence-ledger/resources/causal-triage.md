# Causal Claim Triage

Every causal link in a narrative is a claim requiring a warrant. Grading is not hedging. Grading is typing: the grade fixes which verbs the sentence may use, and the back-reference check stops the grade and the sentence drifting apart later.

The L1-L5 ladder is a working taxonomy assembled for this skill, not a published standard. The straw / hoop / smoking-gun / doubly-decisive test names come from the process-tracing literature in political science.

## Table of Contents
- [The five grades](#the-five-grades)
- [What L1 actually requires](#what-l1-actually-requires)
- [Scan targets](#scan-targets)
- [The back-reference check](#the-back-reference-check)
- [System intentionality grammar](#system-intentionality-grammar)
- [Hindsight fences](#hindsight-fences)
- [Process-tracing test assignment](#process-tracing-test-assignment)
- [Counterfactual admissibility](#counterfactual-admissibility)
- [Worked triage, three domains](#worked-triage-three-domains)

## The five grades

| Grade | What is established | Permitted verbs | Banned |
|-------|--------------------|-----------------|--------|
| L1 MECHANISM | The linking step itself is documented: a decision memo, a contract term, a physical process, an accounting identity, a code path, a stated and executed decision | caused, forced, triggered, led to, because, resulted in, drove | — |
| L2 CORRELATION | Quantitative co-movement is documented; the mechanism is not | moved with, tracked, accompanied, coincided with, rose alongside | because, drove, forced, caused |
| L3 SEQUENCE | Only temporal order, with both dates known | then, afterwards, subsequently, in the following quarter, by which point | every causal connective |
| L4 ADJACENCY | Co-present in time or space; no link established | none. Either separate the two events in the text so no link can be read, or carry an inline disclaimer: "the two were concurrent; no link is documented" | any verb joining them |
| L5 CONJECTURE | The analyst's inference; no source for the link | must carry an explicit inference marker: "the most plausible reading is", "no source says why, but", "I infer" | may never occupy a thesis, climax, or revelation slot |

**L2 additionally requires**, in the ledger: the actual series, the window, and a statement of what else moved the same way in that window. A correlation with no listed co-movers is an unexamined correlation.

**Downgrade rules that fire automatically:**

- The only source for the link is `retrospective-secondary` → maximum L3.
- The source *asserts* a mechanism rather than *documenting* one → maximum L3. An analyst writing "the tariff caused the shift" is class D testimony about causation, not documentation of a mechanism.
- A live alternative explanation exists that you cannot rule out → downgrade L1 to L3, or L2 to L4.
- The link rests on stated intent alone (an actor said they did X because of Y) → this is a claim about *stated reasons*, which may be false. Permitted verbs narrow to "in response to", "citing", "after which".

## What L1 actually requires

**A source for the LINK, not for the two endpoints.**

Two sourced facts plus a plausible connecting story is L3. This is the single most common tag inflation in practice, and it is invisible unless the ledger records *what document establishes the link* as a separate field from the documents establishing the endpoints.

| Endpoints sourced | Link sourced | Grade |
|-------------------|-------------|-------|
| Tariff announced 4 March (class A); imports fell in April (class A) | nothing | L3 |
| Same | Importer's board minutes, 6 March, resolving to halt orders pending tariff review (class A) | L1 |
| Same | Trade-press article stating the tariff caused the drop (class D) | L3 |
| Same | Importer's CEO in a later interview saying the tariff was why (class B, retrospective-primary) | L2, with the stated-intent verb set |

## Scan targets

Causal claims migrate away from anywhere you check. When body sentences get constrained, the claim moves to where the tagger is not looking. Scan all of these:

- Body sentences containing: because, so, led to, drove, forced, triggered, as a result, which is why, meant that, hence, thus, consequently
- **Section headings and chapter titles** — "How the tariff broke the supply chain" is an L1 claim
- **Chart titles and figure captions** — the title is what readers remember; a causal title is a causal claim
- **Chart annotations** — an arrow labelled "policy change" pointing at an inflection is an L1 claim drawn rather than written
- **Pull quotes** — a quoted source asserting causation on your behalf is still your claim about what the piece establishes
- **Paragraph breaks and scene cuts between two events** — structural juxtaposition is a causal claim made without words
- **Metaphor** — "the dam broke", "the floor gave way", "the fuse was lit" are causal claims wearing figurative clothes
- **Ordering itself** — if B now precedes A in the text but followed A in reality, readers will invert the causality

The adjacency-by-layout check: scan for L3 and L4 pairs separated only by a paragraph break, a scene cut, or a section heading. Treat each as if the connective were present.

## The back-reference check

Grades are assigned honestly at ledger time. Then a line-edit turns "then" into "which forced", because "which forced" reads better, and the grade map silently stops describing the text.

**Procedure, run after every revision pass:**

1. Re-extract every causal verb and every juxtaposition from the current text, using the scan targets above.
2. Join against the grade map by claim ID.
3. Report three sets: verbs outside their grade's permitted set; graded links whose text no longer contains any marker; new causal constructions with no claim ID at all.
4. For each mismatch, either restore the permitted verb or re-grade the link with a written reason. Never re-grade silently to license a verb that has already been written.
5. Treat causal verbs as protected tokens. A downstream editing pass may reword around them but may not change them without re-citing the grade.

**The third set is the important one.** New causal constructions with no claim ID are usually fabricated connectives rather than fabricated facts: "By then the pressure had become impossible to ignore." "The team, now convinced, moved on." These assert state changes, carry no proper nouns or numbers, trip no fact-check, and are pure invention. Transition and summary sentences carry claim IDs like every other sentence.

## System intentionality grammar

When the protagonist is a market, a protocol, an institution, a codebase, or a supply chain, the ethics load shifts but does not lighten. A system has no interiority, so every "the market realized" sentence is either shorthand a reader will misread as agency, or a hidden causal claim about collective intent.

**Substitute intentionality for interiority.** A system's "want" must be grounded in one of three, and the ledger must record which:

| Grounding | What it is | Example |
|-----------|-----------|---------|
| Documented incentive | A payoff structure that exists on paper | "Reimbursement rules paid per procedure, not per outcome." |
| Stated strategy | A filing, roadmap, standard, charter, minutes, RFC | "The 2021 roadmap named latency as the primary target." |
| Revealed preference | Behaviour visible in prices, allocations, spend, traffic, merges | "Ninety percent of new capacity went to the 300mm line." |

**Banned constructions**, unless cashed out into the mechanism in the same sentence:

- "the market realized" / "the market decided" / "the market wanted"
- "the industry moved to" (as an intentional act)
- "the protocol wanted" / "the algorithm decided"
- "physics fought back"
- "the codebase resisted"

Rewrite as an aggregate of documented actor behaviour, or mark it explicitly as shorthand at first use.

Bad: "By 2018 the market had realized that the 200mm line was a dead end."

Good: "Between 2016 and 2018 the four largest buyers each announced 300mm-only qualification programmes [F-220..223]. No public statement from any of them names the 200mm line as obsolete."

**Opponents in a system narrative are usually constraints**, not villains: physics, capital cost, regulation, latency, yield, thermal budget, contract term. Resist casting a firm or a person as antagonist merely because the narrative has an antagonist slot. An agent that only checks facts and never checks intentionality verbs will pass a piece that is wrong in its every load-bearing sentence.

## Hindsight fences

Four checks that kill most retrospective contamination. All are label-and-disclose devices, not delete rules.

**1. Contemporaneous-knowledge fence.** No actor may be shown acting on information that postdates their action. This single check catches more hindsight contamination than the other three combined.

**2. Inevitability ban.** Delete every "was always going to", "inevitably", "the writing was on the wall", "in hindsight it was obvious" that is not attributed to a contemporaneous source. The outcome may not be foreshadowed as certain.

**3. Retrospective-only tag.** For each event carrying a structural role, record four dates: the event date; the date of the earliest source treating it as significant; the outcome date; the date of the source you actually cited. If the earliest source treating it as significant postdates the outcome, tag the link RETROSPECTIVE-ONLY. A RETROSPECTIVE-ONLY link may not carry unhedged causal language. Either downgrade the verb, or add one sentence **in the body** stating that the significance is visible only in hindsight.

Do not mechanically demote every RETROSPECTIVE-ONLY link. Some genuinely causal processes are invisible to everyone present: a slow demographic shift, accumulating technical debt, a gradual change in yield. An agent that demotes all of them will refuse to name real structural causes and will over-weight whatever happened to be loud at the time. That is salience bias wearing the costume of rigor.

**4. Substitution test.** For each retrospective-only link, name two other events in the same window that a narrator with a different ending would have selected instead. If you cannot name two, you have not searched the corpus.

## Process-tracing test assignment

Optional but high-value for load-bearing links. Assign each piece of evidence a test type by asking two yes/no questions: is passing NECESSARY for affirming the hypothesis? is passing SUFFICIENT?

| | Not sufficient | Sufficient |
|-|----------------|-----------|
| **Not necessary** | STRAW-IN-THE-WIND: passing slightly weakens rivals; failing slightly weakens H | SMOKING-GUN: passing confirms H; failing does not eliminate it |
| **Necessary** | HOOP: failing ELIMINATES H; passing only affirms relevance | DOUBLY DECISIVE: rare; passing confirms H and eliminates rivals |

Rules that make this more than a labelling ritual:

- Write at least two rival hypotheses **before** assigning any test. Without a named rival, everything looks like a smoking gun, because there is nothing for it to discriminate against.
- Name the rival each test eliminates, in the same breath as the test name.
- Run at least one hoop test whose failure would kill your spine, and record the result whichever way it goes. Running only hoop tests your favoured hypothesis will pass is hoop-test theatre.
- Record which tests were run, which passed, and which were not attempted. An unattempted hoop test is an open hole and gets disclosed as one.
- Placement rule: a link supported only by straws-in-the-wind may appear, but may not occupy the thesis, climax, or revelation slot.

## Counterfactual admissibility

If the piece uses a "what if" node, all six gates must pass or the node is rejected.

| Gate | Requirement | Fails |
|------|-------------|-------|
| CLARITY | Antecedent and consequent both specified concretely | "if things had gone differently" |
| COTENABILITY | You can enumerate the connecting principles — everything else that would also have to be true | Cannot list them → reject |
| MINIMAL REWRITE | Exactly one thing changes | Requires altering a second independent fact → you are describing a different world |
| HISTORICAL CONSISTENCY | The antecedent was physically, technically, and institutionally possible at that date, and someone at the time proposed or considered it | Anachronistic option |
| THEORETICAL CONSISTENCY | The link from antecedent to consequent uses a mechanism already established in the piece at L1 or L2 | Novel mechanism invented for the counterfactual |
| STATISTICAL CONSISTENCY | Where base rates exist, the counterfactual outcome falls inside them | Outcome outside any observed range |

Rendering rules: admitted nodes appear as bounded elements — a bracketed passage, a sidebar, a distinctly styled paragraph. Never as a dramatised scene with sensory detail; a dramatised counterfactual acquires the same vividness as documented events and readers will not retain the distinction. Cap density at roughly one node per major section (derived default).

The characteristic failure is the counterfactual as consolation: a "what if" so implausible that the actual path looks overdetermined by comparison, which strengthens the sense of inevitability the node was supposed to weaken.

## Worked triage, three domains

### Epidemiology

Text: "The vaccination campaign drove case counts down 40% over the following quarter."

- Endpoints: campaign start date (class A, health ministry release); case counts (class A, surveillance series).
- Link source: none.
- Co-movers in window: a seasonal decline of similar magnitude in each of the three prior years; a testing-eligibility change on 12 May.
- **Grade: L2 at best, and the testing change triggers an instrument check.** Permitted: "Case counts fell 40% over the quarter following the campaign, alongside the seasonal decline seen in each of the prior three years. Testing eligibility narrowed on 12 May [F-88]."

### Codebase

Text: "The refactor caused the p99 regression."

- Endpoints: merge commit (class A, `8f31ac2`); p99 series (class A, metrics store).
- Link source: **yes** — the commit changes the backoff calculation, and the code path is inspectable and produces the observed shape.
- **Grade: L1.** Permitted: "caused". The link is documented in the code path itself, which is exactly what an L1 tag is for. Record the artefact establishing the link as `scheduler/backoff.go` lines 55-71, separately from the endpoint pointers.

### Institutional history

Text: "The 1994 reorganisation was what allowed the division to survive the downturn."

- Endpoints: reorganisation date (class A, board minutes); division survived (class A, later filings).
- Link source: a 2011 management book (class D, retrospective-secondary).
- Retrospective-only: the earliest source treating the reorganisation as consequential is dated 2011, well after the outcome.
- Substitution test: name two other 1994 events a different narrator would have chosen. If you cannot, search again.
- **Grade: L5 at best, marked, and barred from the climax.** Permitted: "No contemporaneous source treats the 1994 reorganisation as decisive. Reading backward from the division's survival, it is the most plausible candidate; the record does not establish it."

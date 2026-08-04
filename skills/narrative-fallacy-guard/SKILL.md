---
name: narrative-fallacy-guard
description: Stops a true set of facts from being assembled into a false story. Runs the retrospective slot audit, the outcome-blind rewrite (flip test, separation test), the inevitability audit with its overshoot check, the survivorship graveyard pass, the counterfactual admissibility gate, and the expensive proportion and omission audits. Every check labels and discloses; none deletes. Use when drafting or reviewing history, post-mortems, biography, market or protocol narratives, research writeups, or any account written after the outcome was known, or when user mentions hindsight bias, narrative fallacy, survivorship bias, inevitability, halo effect, outcome bias, just-so story, teleology, or Whig history.
---

# Narrative Fallacy Guard

## Table of Contents
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [What Each Failed Check Produces](#what-each-failed-check-produces)
- [Banned Constructions and Their Licences](#banned-constructions-and-their-licences)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

**Related skills:** Use `writing-structure-planner` for choosing the architecture before this guard tests it, `narrative-opposition-web` for warranting an antagonist. Use `narrative-evidence-ledger` for the causal ladder and the omission set this skill leans on, `causal-inference-root-cause` for building the causal case this skill audits. Use `narrative-fidelity-audit` for the proportion, representativeness, and anachronism questions asked at draft time, `cognitive-fallacies-guard` for chart-level and visual misleads.

## Core Principles

1. **Label, never delete**: every check terminates in a disclosure sentence, a rewrite, or a tag. None of them terminates in a cut claim. A guard used as a delete rule deletes every interesting explanation and ships a chronicle, and chronicles inform nobody.
2. **The ending is the contaminant**: any structural slot, evaluative adjective, or causal verb selected after the outcome was known is suspect by construction, not by evidence of error.
3. **The cheap checks are the dangerous ones**: per-sentence passes can all pass while the piece lies through proportion and omission alone. Work that carries citations and reads as audited is more dangerous than unchecked work.
4. **Disclosure lives in the body**: within two sentences of the claim it qualifies, in the same typographic register. Anything in an endnote, appendix, or methods block is functionally undisclosed.
5. **Anti-narrative bias is also a bias**: the red-team literature is asymmetrically stocked with attacks on agency. State, for each major outcome, the strongest agency reading you considered and why you did or did not adopt it.
6. **A date is not a clean standard**: contemporaneous sources are interested parties, selected by survival, and often already carrying an in-progress halo. Annotate date, interest, and primary-vs-secondary together.
7. **A binding hedge budget is an architecture signal**: when the disclosures crowd the subject out, change the shape of the piece. Do not spend more budget.

## Workflow

Copy this checklist and track your progress:

```
Narrative Fallacy Guard Progress:
- [ ] Step 1: Build the source ledger (date + interest + primary/secondary)
- [ ] Step 2: Audit the structural slots against the outcome date
- [ ] Step 3: Run the per-sentence passes (outcome-blind rewrite, inevitability audit, overshoot check)
- [ ] Step 4: Run the expensive passes (graveyard, counterfactual gate, proportion, omission)
- [ ] Step 5: State the agency reading, place the disclosures, check the budget, ship the log
```

**Step 1: Build the source ledger**

Step 1.1: For every source, record three fields, not one.
- DATE: the published date, plus the date of the events it describes.
- INTEREST: who paid, who benefits, what the author was selling or defending.
- CLASS: primary and contemporaneous, or secondary and retrospective.

Step 1.2: Apply the hard rule, using the causal grades as defined in `narrative-evidence-ledger`. No causal claim may be tagged L1 MECHANISM on the strength of a purely secondary retrospective account. A later book asserting that a memo caused a decision is evidence about the book. Downgrade to L3 SEQUENCE or L5 CONJECTURE until the memo itself is in hand.

Step 1.3: Write down the SELECTION RULE that produced the corpus, literally: "this corpus consists of firms that survived / papers that were published / systems that still have logs / people who agreed to be interviewed." Carry this sentence into Step 4.

See [resources/audit-procedures.md](resources/audit-procedures.md) for the ledger fields and the primary-vs-secondary downgrade table.

**Step 2: Audit the structural slots**

Step 2.1: List every structural slot the piece uses (inciting incident, each turning point, revelation, climax, resolution) and the event you have placed in each.

Step 2.2: For each slot record four dates: the event date, the date of the EARLIEST source that treats the event as significant, the outcome date, and the date of the source you actually cited. If the earliest-significance date falls after the outcome date, tag the slot RETROSPECTIVE-ONLY.

Step 2.3: For every RETROSPECTIVE-ONLY slot, run the substitution test: name two other events in the same window that a narrator with a different ending would have chosen instead. Cannot name two? You have not searched the corpus; go back.

Step 2.4: Apply the rule. A RETROSPECTIVE-ONLY slot may not carry unhedged causal language. Either downgrade the verb or add one body sentence stating that the significance is visible only in hindsight. Do not demote the slot merely for being retrospective: slow demographic shifts, accumulating technical debt, and gradual definitional drift are real causes that nobody present could see.

Step 2.5: If the subject is quantitative, run the INSTRUMENT CHECK on every candidate inciting incident before accepting it. A definitional revision, a coverage change, a re-classification, a merger that changed the reporting entity, or a logging change produces a sharper, better-timed discontinuity than any real transition.

**Step 3: Run the per-sentence passes**

Step 3.1: OUTCOME-BLIND REWRITE. Extract every evaluative adjective and dispositional noun applied to any actor: visionary, reckless, disciplined, prescient, complacent, bloated, naive. Require a dated source predating the outcome for each, attributed in line with its date; otherwise replace the adjective with the action taken, the information set available at that date, and the alternatives visibly on the table. Then run the FLIP TEST and the SEPARATION TEST. Apply the identical pass to system protagonists: "an efficient market", "a rational consolidation", "an inevitable standardisation" are outcome-derived characterisations of a prior state.

Step 3.2: INEVITABILITY AUDIT. Extract every causal sentence. For each, cite what the actors at the time expected, and name one live alternative someone in the material was actually pursuing. Enforce the banned-without-licence list. Insert at least one forecast-vs-outcome beat: a documented prediction from inside the material that turned out wrong, with the reasoning that made it reasonable at the time.

Step 3.3: OVERSHOOT CHECK. Does the draft contain at least one confidently asserted "X caused Y"? If not, the brake has become hedge fog, which is abdication rather than honesty. The target is a small number of confident causal claims each carrying its counterfactual, not a large number of hedged ones.

Step 3.4: ANACHRONISM FLAG. Where a category, a metric, or a moral frame used in the text did not exist at the time described, say so in the body. Flag the anachronism; do not adjudicate whether present-day categories may be applied. That larger dispute is contested and is not this skill's business.

See [resources/audit-procedures.md](resources/audit-procedures.md) for worked bad-and-good rewrites of each pass across five domains.

**Step 4: Run the expensive passes**

These are the ones that catch the failure the cheap passes cannot see. Under schedule pressure they are the ones that get dropped. Do not drop them: see the warning in [Guardrails](#guardrails).

Step 4.1: GRAVEYARD PASS. For every success attribution, search for at least two entities that took the same action and did not get the same outcome. Three results are legal, and each one appears in the text. Counterexamples found: weaken the claim. Counterexamples searched for and not found: state the search and state the finding. Population is n=1 or unobservable: write "the base rate for this action is unknown" in the body. That third result is first-class and non-embarrassing. Manufacturing a weak analogy to avoid it is a fresh distortion dressed as a correction.

Step 4.2: COUNTERFACTUAL GATE. Any road-not-taken must pass all six admissibility tests (clarity, cotenability, minimal rewrite, historical consistency, theoretical consistency, statistical consistency) and must render as a bounded element: a bracketed passage, a sidebar, a differently-styled paragraph. Never as a dramatised scene. A dramatised counterfactual acquires the vividness of the documented events and readers will not retain the distinction.

Step 4.3: PROPORTION AUDIT. Tabulate words spent against evidence tier and against causal weight. Flag both asymmetries. First: the vivid anecdote that is top quintile by words and bottom quintile by evidence. Second: the well-evidenced driver that is top quintile by causal weight and bottom quintile by words. Each flag needs a written justification, not an automatic rebalance. Fill the causal-weight column BEFORE the arc is chosen. Filled after, it inherits the halo it is meant to catch.

Step 4.4: OMISSION CHECK. List every corpus item appearing nowhere in the draft and state why for each. Any item that would weaken the spine and was omitted without a stated reason is a cherry-pick and must be reinstated.

See [resources/audit-procedures.md](resources/audit-procedures.md) for the six-test counterfactual gate with admitted and rejected examples, and the proportion table format.

**Step 5: State the agency reading, place the disclosures, ship the log**

Step 5.1: Write the AGENCY READING for each major outcome: the strongest reading in which skill, intent, and decision explain the result, and the specific reason you did or did not adopt it. "The lens disfavours agency" is not a reason; it is the bias this step exists to catch.

Step 5.2: Move every disclosure into the body, within two sentences of the claim it qualifies, in the same typographic register. Mark each NON-REMOVABLE. Assume any later "tighten this up" pass will strip them.

Step 5.3: Count hedges, contingency nodes, and disclosure sentences per thousand words against the budget in [resources/disclosure-and-budget.md](resources/disclosure-and-budget.md). Over budget means the architecture is wrong for this evidence, not that the piece needs more caveats. Switch to a shape that does not require the missing slots: chronicle, braided comparison, taxonomy, single-question investigation.

Step 5.4: Ship the audit log with the deliverable: the slot table with its four dates, the flip-test casualties, the graveyard result, the omission list with reasons, the agency reading, and the hedge count.

Validate using [resources/evaluators/rubric_narrative_fallacy_guard.json](resources/evaluators/rubric_narrative_fallacy_guard.json). **Minimum standard**: average score >= 3.5, and no score below 3 on "Expensive Checks Actually Run".

## What Each Failed Check Produces

Every row ends in a label, a rewrite, or a disclosure. No row ends in a deletion.

| Check | Failure looks like | Required output on failure |
|---|---|---|
| Retrospective slot audit | Earliest significance date is after the outcome date | Body sentence: "nobody at the time treated this as a turning point", plus a downgraded verb |
| Substitution test | Cannot name two rival slot-fillers | Return to the corpus; the search was not done |
| Outcome-blind rewrite | Adjective has no dated pre-outcome source | Replace with action + information set + alternatives, written as vivid specifics |
| Flip test | Sentence would not have been written that way under the opposite outcome | Rewrite so the evidence, not the ending, supplies the judgment |
| Separation test | One sentence carries both decision quality and outcome quality | Split into two sentences; the outcome sentence may not supply the decision adjective |
| Inevitability audit | Banned construction with no live alternative named | Replace with contingency language, or state the binding constraint that made it overdetermined |
| Overshoot check | Zero confident causal claims in the piece | Restore the best-evidenced causal claim and give it its counterfactual |
| Graveyard pass | No comparison entities found | State the search and the finding, or state "base rate unknown" in the body |
| Counterfactual gate | Fails any of the six tests | Reject the node, or narrow the antecedent until it passes |
| Proportion audit | Words and evidence tier are inverted | Written justification, or rebalance; never a mechanical word quota |
| Omission check | Corpus item absent with no stated reason | Reinstate it |
| Source ledger | L1 MECHANISM sourced from a secondary retrospective | Downgrade the tag to L3 or L5 |
| Hedge budget | Over budget per thousand words | Change the architecture; do not add caveats |
| Agency reading | Absent, or waved away | Write it, name the evidence for it, and give the reason for rejecting it |

## Banned Constructions and Their Licences

These are banned without a licence earned in Step 3.2:

- "inevitably", "was always going to", "was bound to"
- "the writing was on the wall", "in retrospect it is obvious"
- "set the stage for", "paved the way", "the seeds of its own destruction"
- "primitive", "advanced", "matured into"

The licence is a named live alternative that someone in the material was actually advocating or pursuing at that moment, or a stated binding constraint (physical, accounting, contractual, thermodynamic) that made the path overdetermined. Overdetermination must be stated, never implied.

Replacements that carry the same information without the teleology: "happened to", "persisted given", "survived the conditions of", "nobody on the shift expected", "of the paths then on the table, this was the one funded".

Worked contrast, three domains:

- Outage post-mortem. Bad: "The undersized connection pool inevitably led to the cascade." Good: "The pool was sized for the 2021 traffic profile and never revisited. Two engineers had filed tickets to raise it; both were closed as low priority against the migration deadline. When the retry storm arrived, the pool saturated in ninety seconds."
- Protocol history. Bad: "The format matured into the industry standard." Good: "Three formats had working implementations in 1997. Two lost their sponsoring vendors within four years; the survivor was the one whose reference implementation shipped inside a widely deployed operating system, which is distribution rather than design."
- Lab science. Bad: "The 2014 assay result contained the seeds of the eventual retraction." Good: "The 2014 assay produced a result the lab could not replicate on the first attempt. The notebook records it as instrument drift, which was the standard reading for that machine at the time. Nothing in the record shows anyone treating it as a warning until 2019."

## Guardrails

**Requirements:**

1. **No check is a gate that deletes**: the Kahneman predictability test deletes essentially every rich historical explanation, the slot audit flags every structural cause invisible to contemporaries, and the graveyard pass has no valid output at n=1. Each is a label-and-disclose device. An agent that gates on them ships a chronicle, which is its own accuracy failure.
2. **The expensive checks are mandatory, not optional**: implementing only the cheap per-sentence checks produces work MORE dangerous than unchecked work, because it carries verifiable citations and reads as audited while misrepresenting drift and proportion through selection alone. If Step 4 is skipped, the deliverable must say on its face that it was skipped.
3. **Disclosure placement is load-bearing**: body text, within two sentences, same register, marked non-removable. Back matter does not count. Readers experience the body.
4. **Source interest travels with source date**: a dated pre-outcome source produced by a promoter or a defendant has moved the bias one step upstream, not removed it. Say whose interest it served, and whether it is representative of a range you actually sampled or a single cherry-picked booster.
5. **The agency reading is a required output field**: not optional prose. Missing it fails the rubric regardless of the rest.
6. **Genre disclosure is not a licence**: naming the shape of your account buys credibility that must be spent on reinstating what the shape suppressed. Any documented mechanism dropped to make the arc work goes back in, even where it damages the arc.

**Common pitfalls:**
- Neutrality collapse: stripping every adjective and shipping unreadable, unloving prose. The substitution must be vivid specifics ("two quarters of cash and one letter of intent"), never a bureaucratic placeholder.
- Applying the flip test to sentences about facts. It is valid only for sentences about decisions; elsewhere it produces nonsense.
- Luck nihilism: attributing everything to path and noise. The cumulative-advantage evidence licenses only the weak claim, that extremes are predictable and the middle is not. The check must produce an apportionment, not a shrug.
- Contemporaneity fetish: mechanically demoting every retrospective slot, which over-weights whatever happened to be loud at the time. That is salience bias wearing the costume of rigor.
- Manufacturing comparison cases to satisfy the graveyard pass in an n=1 domain.
- Defensive over-disclosure: answering an audit with twelve caveats. Volume is not integrity. The operative test is whether a reader who disagrees can find the strongest counter-evidence inside the piece.
- Dramatising a counterfactual until it reads like a documented scene.
- Letting a later editing pass strip the disclosures. Mark them; re-count them after every revision.

**Attribution caveats to carry into any output:**
- The process-tracing test names (straw-in-the-wind, hoop, smoking-gun, doubly decisive) come from Van Evera and Bennett, as presented by Collier.
- The six-part counterfactual gate is Tetlock and Belkin's. The seven-band likelihood ladder with its numeric ranges is ICD 203's published lexicon.
- "Graveyard pass", "overshoot check", and "substitution test" are this skill's own labels. They name procedures assembled from several literatures. Do not cite them as canonical terms.
- Every numeric threshold in [resources/disclosure-and-budget.md](resources/disclosure-and-budget.md) is a derived default for this skill, not a published figure.

## Quick Reference

**Key resources:**
- **[resources/audit-procedures.md](resources/audit-procedures.md)**: the six audits in full, with slot tables, the flip and separation tests, the counterfactual gate, the proportion table, and bad-and-good rewrites across post-mortems, biography, supply chain, protocol history, and research writeups
- **[resources/disclosure-and-budget.md](resources/disclosure-and-budget.md)**: disclosure placement rules, hedge budget arithmetic, the likelihood and confidence lexicon, source ledger fields, the agency-reading template, and the ship log format
- **[resources/evaluators/rubric_narrative_fallacy_guard.json](resources/evaluators/rubric_narrative_fallacy_guard.json)**: quality scoring

**Inputs required:**
- The draft or the planned structure, with its structural slots identified
- The corpus, with source dates and provenance available
- The outcome date (the date after which everything in the piece is written with hindsight)

**Outputs produced:**
- Slot table with four dates per slot and its retrospectivity tag
- Rewritten evaluative sentences with the flip and separation tests applied
- Inevitability audit results, including the forecast-vs-outcome beat and the overshoot verdict
- Graveyard result, counterfactual nodes admitted and rejected, proportion table, omission list with reasons
- The agency reading for each major outcome
- Hedge budget count and, if binding, an architecture recommendation
- The audit log, shipped with the deliverable

# Audit Passes

The scans and question sets. Run them in this order: red flags, then the three altitudes, then proportion and omission. Cheap checks first, but never stop at the cheap checks — that is the documented way a rigorous-looking narrative lies.

## Table of Contents
- [Fabrication Red-Flag Scan](#fabrication-red-flag-scan)
- [The Three Altitudes in full](#the-three-altitudes-in-full)
- [Evidence Class to Attribution Grammar](#evidence-class-to-attribution-grammar)
- [Causal Grades](#causal-grades)
- [Numbers in Narrative](#numbers-in-narrative)
- [Chronology Audit](#chronology-audit)
- [Proportion and Omission](#proportion-and-omission)
- [Subtraction Log Format](#subtraction-log-format)

## Fabrication Red-Flag Scan

Twelve signatures, tuned to how a language model fabricates rather than how a human does. **Every hit is guilty until it produces a pointer.** A hit that produces a pointer survives untouched, however good it sounds.

| # | Signature | Why it is a signature | Domain example |
|---|---|---|---|
| 1 | Quotation that lands the theme too cleanly, or is too well-formed for speech — no disfluency, no hedge, no irrelevance | Real speech is messy. Generated speech is on-topic | "We were solving yesterday's problem with tomorrow's budget," the former VP said |
| 2 | Sensory or physical detail doing thematic work | The record almost never contains it; the scene wants it | "The fab floor was silent for the first time in nine years" |
| 3 | Transition or summary sentence asserting a state change | No proper nouns, no numbers, trips no fact-check, pure invention | "By then it was clear the architecture would not scale" |
| 4 | Ending that rhymes with the opening; an arc that completes; three examples in clean progression | Symmetry arrives in drafting, not in reporting | Closing image mirroring the lede |
| 5 | Absolutes and superlatives | Cheapest sentences to write, most expensive to defend | "the first", "the only", "the largest", "never before" |
| 6 | Unnamed minor character voicing the thesis | Exists because the argument needed a mouth | "One engineer put it simply:" |
| 7 | Causal verb at the seam between two sourced facts | Both facts check out; the join is invented | "which triggered", "led to", "forced", "which is why" |
| 8 | A number more precise than its neighbours, or suspiciously round | Precision that did not come from a source | "roughly 40%" next to "38.62%" |
| 9 | A date or time more precise than the surrounding chronology | The scene wanted a clock | "at 4:15 that afternoon" in a piece dated only by month |
| 10 | Interior-state verb attached to a real person | The single most common fabrication | "realized", "knew", "felt", "understood", "feared", "wanted" |
| 11 | Intentional verb attached to a market, protocol, institution, or codebase | Hidden causal claim about collective intent | "the market decided", "the protocol wanted", "the industry accepted" |
| 12 | Detail so good you would have led with it, and did not | It arrived in drafting rather than in reporting. This is the sharpest single tell | Any of the above that you like best |

**Anti-overcorrection.** Key every judgment on the missing pointer, never on the vividness. If the scan strips genuinely reported detail — the detail that makes the piece worth reading and that *is* in the record — the writer learns to switch the scan off, and you have made things worse. Report the sourced-and-kept count alongside the deleted count so the scan's precision is visible.

## The Three Altitudes in full

Run as an adversarial pass. You hold the ledger and the draft. You do not hold the draft's rationale, and you do not accept "I remember sourcing that."

Output a **defect list, not a rewrite**. Fixing and checking must be separate acts.

### Sentence level

1. What does this sentence assert, including everything it implies but does not state?
2. Which pointers support it? If none, why does it exist?
3. Did I observe this, get told this, read this, or conclude this? Which one does the grammar tell the reader?
4. Is the attribution level correct for the evidence class, or is inference wearing the grammar of observation?
5. Which single word carries more certainty, specificity, or vividness than the source supports? Name the word.
6. What is the strongest reading of the source under which this sentence is false?
7. If a hostile, well-informed reader challenged this sentence, what exactly would I show them, and would it settle it?
8. Does the verb make a causal claim? At what grade? Does the grade support the verb?

### Paragraph level

9. Every sentence here is supported. Is the *implicature* supported? What will the reader believe after this paragraph that no sentence in it claims?
10. Does the ordering assert a causality no source asserts? Narrative adjacency reads as cause.
11. Does any transition sentence assert a state change nobody documented?
12. Does the paragraph's shape (setup, turn, payoff) come from the evidence or from the shape?

### Passage level

13. Would each person and institution depicted recognize this as a fair account of what happened? On what specific point would they object, and is that point in the text?
14. What did I cut here, and does the remainder imply a different frequency, magnitude, or balance than the full record?
15. Is this scene typical of the period it represents, or atypical and vivid? If atypical, does the text say so?
16. Does a category, metric, or moral frame used here postdate the events described? If so, does the text say so? (Encode only this narrow, checkable operation. Do not encode a general position on presentism, which is contested territory.)
17. Name two entities that took the same actions as the protagonist and did not get the same outcome. Are they in the text?
18. What is the strongest agency-based reading of this material, and why was it not adopted? If the answer is "the structural reading is more fashionable", that is anti-narrative bias, not rigor.

**The proof-of-work rule.** Sentence-local checking is what a language model does well and what it will default to. Every documented case of a fully-checked-but-false narrative failed at the paragraph or passage level. If this pass returns only sentence-level defects across a long piece, it did not run questions 9 to 18. Report that as a finding about the audit, not as a clean bill for the draft.

## Evidence Class to Attribution Grammar

Evidence classes: **(A)** primary artefact — document, filing, transcript, dataset, log, recording. **(B)** direct first-person testimony about own experience. **(C)** second-hand testimony. **(D)** secondary reporting. **(E)** analyst or agent inference. **(F)** unsourced.

Attribution levels, weakest signal to strongest:

| Level | Form | Example |
|---|---|---|
| L0 | Unmarked assertion | "Revenue fell 18% that quarter." |
| L1 | Embedded source — the source is a grammatical constituent, not an appendage | "The filing put revenue down 18%." "The postmortem timestamps the first alert at 02:14." |
| L2 | Epistemic verb naming the act | "reported", "recalled", "estimated", "projected", "claimed" |
| L3 | Explicit attribution | "according to X" |
| L4 | Contest marker, both values in one sentence | "The company put the figure at 40%; the regulator's audit found 27%." |
| L5 | Uncertainty declaration | "The record does not establish…", "no source could say…" |
| L6 | Methods block or note on sources | Absorbs the routine load so L0 and L1 can carry the prose |

**Mapping:**

| Evidence | Required level |
|---|---|
| (A) uncontested, covered by methods block | L0 |
| (A) consequential, or the document's identity matters | L1 |
| (B) present-tense recall | L2 |
| (B) self-serving or contested | L3 |
| (C) second-hand | L3 mandatory, plus explicit distance: "his deputy said he had been told…" |
| (D) secondary reporting | L3 mandatory, plus a flag that the underlying source was not obtained. Never L0 or L1 |
| (E) inference | L5-adjacent marking. "The record does not establish X; the sequence is consistent with…" Never presented as finding |
| Contested, any class | L4. Both values, both sources, one sentence |
| Gap | L5 in the body. Not silence, not a bridge sentence |

**Rules.**
- L1 is the workhorse. Prefer it to "according to". It costs no rhythm and carries full provenance.
- L3 scarcity is what makes it a signal. Spend it deliberately on contested, self-serving, or consequential claims.
- The opening sentence of a reconstructed scene carries its sourcing. The remainder may run unmarked under that cover.
- A methods block licenses L0 only for claims it actually covers. It is not a blanket. Symptom of abuse: a methods block describing the reporting in general terms rather than mapping to specific passages.
- **Budget (working default, not a published figure):** if more than about one sentence in four in a passage sits at L3 or above, the passage is under-reported. Fix by reporting. Never fix by deleting attributions.

**Register porting.** Technical, financial and ML domains have no "sources said" convention. Their prose norm is bare assertion backed by a bibliography. Port the function, not the grammar:

| Journalism form | Financial or technical equivalent |
|---|---|
| "according to the filing" | "(10-K FY23, p.47)" or "the FY23 10-K reports" |
| "sources said" | "three of five interviewed operators reported" |
| "he recalled" | "the postmortem author's own account records" |
| Methods block | Data and methods section, with per-figure definitions |

An agent tuned on journalism and pointed at a technical writeup will drop attribution entirely because the target register does not use it. That is the silent failure to watch for.

## Causal Grades

Grade every link in the narrative spine. Force the prose verb to match the grade.

| Grade | Evidence | Permitted verbs | Forbidden |
|---|---|---|---|
| **G1** | Mechanism documented — contract terms, physical process, code path, stated and executed decision | "caused", "triggered", "forced" | — |
| **G2** | Stated intent plus execution — an actor said they would do X because of Y, and did | "in response to", "citing", "after which" | Presenting the stated reason as the real reason |
| **G3** | Correlation plus argued mechanism. You are reasoning | "appears to have", "is consistent with", "plausibly" | Any G1 verb. Must be marked as the author's argument |
| **G4** | Temporal sequence only | "then", "subsequently", "by which point" | Anything causal |
| **G5** | Post-hoc pattern, visible only in retrospect and only to the analyst | Must be labelled as retrospective reading | Presenting as contemporaneous insight |

**Counterweights, all mandatory:**
- **Counterfactual log.** For every G1/G2 link on the spine, record what else could have produced the outcome. If the alternative is live, downgrade to G3.
- **Survivorship check.** Does the narrative follow only the cases that reached the ending? Name the comparable cases that did not, or state that the comparison was not made.
- **Inevitability ban.** The outcome may not be foreshadowed as certain.
- **Contemporaneous-knowledge fence.** No actor acts on information post-dating their action.

**Verb creep is the failure.** Grades get assigned honestly at outline stage, then a line-editing pass upgrades the verbs for punch: G4's "then" becomes "which forced", G3's "appears to have" becomes "did". The structural document still says G3/G4 and no longer describes the text. Treat causal verbs as protected tokens carrying their grade. Any line edit changing a causal verb must re-cite the grade.

**Secondary-source guard.** A G1 mechanism tag may not come from a purely secondary retrospective account. If the material is books, articles, and retrospectives, the halo and the teleology were already applied upstream, and you will faithfully re-derive them while passing every other check. Record per source: primary/contemporaneous or secondary/retrospective.

## Numbers in Narrative

Quantitative fidelity is owned by `numbers-in-narrative` — precision ceiling, rounding drift, hedge words as precision claims, denominators, percent versus percentage point, contested figures, ranges, and model output versus measurement all live in its Fidelity Refusals. Run that skill on any passage carrying figures; do not restate its rules here.

## Chronology Audit

Run on the diff between the master timeline and the narrative order.

- Is there a master timeline, held separately from the narrative order, with explicit date-precision tags (exact / day / week / month / quarter / year / "before X" / unknown)?
- Every reordering: does the text give a date anchor at the seam?
- Any compression of duration? Forbidden in analytic and journalistic registers. Disclosure-only in memoir register. Never silent.
- Any two events merged into one scene? Always forbidden. That is a composite scene, not a compression.
- Any event placed at a time the record does not support?
- Does any sentence imply finer date precision than the timeline records?
- After reordering, does narrative adjacency imply a causality that reality's order does not?
- Did any temporal anchor get deleted during line editing?
- Does any actor act on information that post-dates their action?
- Does the piece foreshadow the outcome as inevitable using knowledge unavailable at that point in the timeline?

## Proportion and Omission

The expensive checks. They are the ones that matter, and they are the ones that get dropped under schedule pressure. Implementing only the cheap per-sentence checks produces work that is *more* dangerous than unchecked work, because it carries verifiable citations and reads as audited.

**Proportion audit:**

1. Build a table: for each claim in the piece, WORDS SPENT, EVIDENCE TIER, and CAUSAL WEIGHT (your estimate of contribution to the outcome).
2. Fill the causal-weight column **before** the arc was chosen where possible. Weight estimated afterwards is contaminated by the same halo the audit exists to catch.
3. Flag every claim in the top quintile by words and the bottom quintile by evidence tier. These are the colourful anecdotes carrying the reader's belief.
4. Flag the inverse: top quintile by causal weight, bottom quintile by words. These are the boring drivers the arc suppressed. Usually a price change, a regulatory filing, a base rate, a demographic trend, a compiler flag, a staffing level.
5. Require a written justification for each flagged asymmetry. "This account gets 800 words because it is the only surviving first-hand record of the mechanism" is legitimate. No justification means rebalance.
6. **Do not equalise mechanically.** The output is a justification requirement, not a word-count quota. Redistributing word count produces prose with the rhythm of a spreadsheet, and readability collapse is itself an accuracy failure, because unread accurate work informs nobody.

**Omission check:** list every item in the corpus appearing nowhere in the draft. For each, state why. Any item that would weaken the spine and was omitted without justification is a cherry-pick and must be reinstated.

## Subtraction Log Format

Refusal training makes you good at not adding. Nothing makes you good at not omitting. A perfectly constrained agent produces an entirely sourced, entirely false piece by cutting the disconfirming quarter, the failed pilot, and the dissenting source — each cut individually defensible for length or flow.

Log every cut that removes a contradicting data point, a dissenting source, a failed instance, a counterexample, or a period that went the other way.

```
| ID | What was cut | Which way it cut | Stated reason | Direction relative to the spine |
```

**Review the log as a SET, not per edit.** Per-edit review always passes; that is the entire problem. Two questions:

1. Do the cuts share a direction? If every removal happens to weaken the counter-case, the reason "length" is not the real reason.
2. Does the remaining text imply a different frequency, magnitude, or balance than the full record? If yes, the subtraction has become deception and must be reversed or offset.

**The absence of a subtraction log is itself a finding.** Report it as such: a piece assembled without one cannot pass this step, and the correct verdict is RETURN TO RESEARCH.

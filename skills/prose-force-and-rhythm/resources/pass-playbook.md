# Pass Playbook

Full procedure for each of the ten passes, with escalation targets and worked examples. Examples are drawn from clinical research, semiconductor and supply-chain reporting, ML writeups, incident post-mortems, market history, and biography, so that no single domain is assumed.

Hart's diagnostic principle is what makes the order load-bearing: problems at any writing stage typically stem from the immediately preceding stage. That is why a pass that cannot fix a defect inside its own class reports upward instead of compensating downward.

---

## Pass 1: STRUCTURE

**Class of edit:** paragraph placement, section boundaries, order of argument. Nothing smaller.

**Procedure:**
1. Number every paragraph. For each, write the one claim it advances.
2. Mark any paragraph whose claim duplicates an earlier one, or whose claim does not serve the piece's central assertion.
3. Mark any section whose paragraphs could be shuffled without loss. That section has no internal logic.
4. Move or cut. Do not rewrite sentences to make a misplaced paragraph fit.

**Escalates to:** the structural planner or the human. A draft whose problem is that it has three findings and one strained thesis cannot be fixed here.

**Worked example (post-mortem):** a draft opens with three paragraphs of system background, then the outage timeline, then the root cause. The structure pass moves the timeline first and cuts background to the two facts the timeline needs. It does not touch a single verb. If the timeline turns out to have a four-hour hole, that is an escalation, not an edit.

---

## Pass 2: FORCE (the verb audit)

**Class of edit:** the main verb and the grammatical subject.

**Procedure, per sentence:**
1. Identify the main verb. Flag it if it is a form of "to be"; "has/have" as main verb; a light verb ("make a decision", "conduct an analysis", "give consideration to"); or a verb whose real action sits in a nominalization beside it.
2. Flag passive constructions. **Do not auto-convert.** Ask: is the actor named in the material? If yes, convert with the real actor as subject. If no, the passive is correct, keep it, and log a reporting gap.
3. Flag expletive openers: "There is/are/was/were", "It is/was ... that". Promote the real subject.
4. Flag suffix clusters: two or more words per sentence ending in -tion, -ment, -ance, -ity, -ness. Convert one to a verb.
5. Flag abstract-noun subjects. If the grammatical subject cannot physically act ("the increase", "the situation", "the framework", "the deterioration"), find the entity that can.
6. **Claim-strength lock.** Record the S-level before the rewrite. Verify it after. Revert on any raise.

**Escalates to:** reporting, whenever step 2 or step 5 cannot find a named actor.

**Worked examples:**

| Defect | Bad fix | Good fix | Why |
|---|---|---|---|
| "There was a sharp increase in wafer scrap at the Hsinchu fab in March." | "Wafer scrap at Hsinchu exploded in March." | "Wafer scrap at Hsinchu rose 40% in March." | Expletive killed either way; the bad fix invents a magnitude the material does not state. |
| "The alert was silenced at 02:14." (actor not in the incident log) | "An on-call engineer silenced the alert at 02:14." | Leave as written. Gap entry: "who silenced the 02:14 alert? Not in the log or the pager history." | Passive-voice elimination that invents an actor is the second failure mode of this pass. |
| "The implementation of the new screening protocol resulted in a reduction in referral times." | "The new protocol slashed referral times." | "After the clinic adopted the screening protocol, median referral time fell from 19 days to 11." | Bad fix strengthens S3 to S5 and adds unstated magnitude. Good fix names the actor, kills two nominalizations, and holds the temporal claim. |
| "The order book was characterized by significant fragmentation across venues." | "The order book fractured across venues." | "Between 2007 and 2012, trading in the name spread across nine venues from two." | Abstract subject replaced with a dated, countable fact. |
| "It is believed by the team that the regression stems from the tokenizer change." | "The regression stems from the tokenizer change." | "The team believes the tokenizer change caused the regression; the ablation is not yet run." | Bad fix deletes the belief-holder and promotes S2 to S5. |

**System variant.** When the actor is a market, protocol, institution, or pipeline, use a state-change verb, never an intention verb.

- Bad: "The market decided the risk was overpriced." / "The scheduler wants to keep queues short." / "The protocol believes the block is final."
- Good: "Spreads narrowed by 30 basis points over the week." / "The scheduler evicts jobs once queue depth passes 400." / "The protocol treats a block as final after six confirmations."

Once a market decides or a model believes, the prose asserts intent, and therefore causation the analysis has not established. Sweep for: decided, wanted, chose, believed, feared, intended, tried to, aimed to, sought.

---

## Pass 3: BREVITY

**Class of edit:** deletion and compression. No reordering, no verb changes.

**Procedure:**
1. Cut List A globally (see SKILL.md and claim-strength-ledger.md).
2. For every List B instance, verify it is doing epistemic work, then leave it.
3. Apply the scope exception: a List A word carrying scope gets replaced with the scope from the material, or kept plus a gap entry.
4. For each sentence over 30 words, attempt a version at 20 or fewer that loses no proposition. Accept only if nothing is lost. List the propositions before and after when the sentence carries a claim.
5. Redundancy sweep. Any claim stated twice keeps the instance closer to its evidence.
6. Measure and report the cut. Under 5% means the pass did not run. Over 30% means something substantive probably went with it; diff the propositions.

**Escalates to:** reporting, when a claim appears three times and the evidence appears once.

**Worked examples:**

- Bad: "The model generally outperformed the baseline, with approximately a 3-point gain in F1." to "The model outperformed the baseline with a 3-point gain in F1." Two violations: "generally" was scope (it did not win every run) and "approximately" was List B.
- Good: "The model beat the baseline in 8 of 10 seeds, by about 3 F1 points."
- Bad: "Deaths in the treatment arm fell by roughly a third in this cohort." to "Deaths fell a third." Scope and estimate both deleted; the sentence now claims a general result.
- Good: "In this cohort, deaths in the treatment arm fell by roughly a third."

---

## Pass 4: CLARITY

**Class of edit:** splitting sentences, supplying missing concrete referents.

**Procedure:**
1. One-reading test on every sentence. Flag anything that needed a second pass.
2. Classify each flag: (a) long sentence, simple content, safe to split; (b) short sentence, dense abstract nouns, a middle-rung abstraction trap; (c) necessary technical term.
3. Fix (a) by splitting. Fix (b) by supplying one particular instance from the material. Fix (c) by defining once, concretely, at first use.
4. **Forbidden fixes:** replacing a precise term with a vaguer one; deleting a qualifier to shorten a sentence; splitting in a way that severs a causal link.
5. **Maintain the clarity split log.** Record every split as a pair of sentence ids. Pass 5 may not merge any logged pair.
6. If a (b) flag has no particular available in the material, that is a reporting gap, not a wording problem. Escalate.

**Worked example (type b):** "Instructional unit throughput remained below the district's projected utilization envelope." No amount of rewording fixes this, because there is no particular in it. The fix requires material: "Sixteen of the district's 22 middle schools ran classes below 20 students; the budget had assumed 28."

A run dominated by type (a) fixes is healthy. A run dominated by type (b) fixes that were made without new material is a warning sign, and the report must say so.

---

## Pass 5: RHYTHM

**Class of edit:** sentence length distribution, terminal position, paragraph openers. See [rhythm-diagnostics.md](rhythm-diagnostics.md) for the full treatment.

**Procedure:**
1. Compute the sentence-length series per paragraph and for the piece. Report mean and SD.
2. Fix low variance by splitting one long sentence **and** merging two short ones inside the same paragraph. Never by shortening everything, which produces a staccato tic.
3. Merges are forbidden on any pair in the clarity split log. Rhythm must not undo clarity.
4. Terminal emphasis: for each paragraph's last sentence, check that the last word is the most consequential one. Move prepositional tails, attributions, and dates off the end unless the date is the point.
5. Paragraph openers: if more than a third open with the same construction, diversify one.
6. Flag any sentence with four or more stacked prepositional phrases.

**Worked example:** "Deaths in the treatment arm fell by a third, according to the 2019 trial report." to "According to the 2019 trial report, deaths in the treatment arm fell by a third." Same words, attribution moved off the terminal slot, and the claim lands last.

**Anti-pattern:** "The fab went dark. Fast. Nobody knew." Variance achieved through typographic drama. In an engineering, clinical, or financial register this reads as unserious and costs more credibility than the monotony it replaced. Variance must come from clause structure and information density.

---

## Pass 6: HUMANITY

**Class of edit:** sentence subjects and the presence of named agents.

**Procedure:**
1. List every sentence whose subject is an agentless abstraction. Replace with the entity that acted, where the material names one.
2. Where the protagonist is a system, the replacement is a named operator, a dated state, or a named constraint. It is never a personified system.
3. Use named people where the material names them. "A senior planner at the Tualatin plant" beats "stakeholders."
4. Re-run the anthropomorphism sweep from Pass 2 on anything you rewrote here, because this pass creates the pressure that causes it.

---

## Pass 7: COLOR

**Class of edit:** concrete and sensory detail.

**Procedure:**
1. Every detail must carry information, not decorate.
2. Every detail must be traceable to the material. A detail you cannot source is deleted, not softened.
3. Sensory instruction is gated on whether sensory observation exists in the source. A writeup built from filings, logs, and papers has no observed senses to report. Do not supply them.
4. Test: could this passage have been written without the source material? If yes, it was generated rather than reported. Cut it.

**Worked example:** "The trading floor fell quiet as the print crossed the tape" is fabrication unless someone on that floor said so, on the record, about that moment. The honest version is either the sourced quote or the state change: "Volume in the front contract dropped by two thirds in the four minutes after the print."

---

## Pass 8: VOICE

Consistency against the register declared at run setup. Flag drift between sections. Do not add personality; do not level a deliberate register shift that the piece uses on purpose. Constant temperature across a long piece is itself a machine signature, so a single deliberate shift is a feature to preserve, not a defect to smooth.

---

## Pass 9: MECHANICS

Grammar, usage, house style, numerals, citation format. Last of the nine. Never before Voice. If you catch yourself here early, you are polishing a paragraph that may not survive Pass 1.

---

## Pass 10: SLOP AUDIT

Run in this internal order. Steps interact, and order matters.

1. **Lexical sweep.** Remove: delve, underscore, showcase, pivotal, intricate, meticulous, realm, tapestry, landscape (as metaphor), mosaic, ecosystem (as metaphor), beacon, cornerstone, bedrock, testament to, robust, seamless, vibrant, holistic, multifaceted, nuanced, transformative, groundbreaking, leverage, harness, streamline, facilitate, foster, navigate, illuminate, unlock, embrace. Domain exception: keep "robust" in a statistics paper where it is a technical term, keep "ecosystem" in ecology.
2. **Signpost filler.** Delete: "It's important to note", "It's worth noting", "That said", "At its core", "Let's break this down", "In conclusion", "Ultimately", "In today's fast-paced world".
3. **Negated contrast.** Find every "not just X, it's Y" / "isn't X, it's Y". Allow one per piece maximum. Rewrite the rest as direct affirmations.
4. **Tricolon.** Find three parallel phrases of near-equal length. Break at least one; introduce asymmetry in length or structure.
5. **Participial tail.** Find clauses ending "...marking a", "...underscoring the", "...highlighting the", "...reflecting a". They restate the main clause. Delete them.
6. **Hedge stack.** Find sentences with two or more hedges. Reduce to one, or convert the uncertainty to a quantity. **Carve-out: this step may remove only rhetorical hedges. It may never remove a hedge reflecting genuine evidential uncertainty.** "It seems like it might possibly be the case that latency rose" has three rhetorical hedges and one claim; reduce it. "The estimate may understate exposure under these assumptions" has two epistemic hedges, both load-bearing; leave both.
7. **List shape.** Bulleted lists whose items are full parallel-stem sentences: if the idea is not list-shaped, convert to paragraphs.
8. **Specificity sweep.** Replace every general noun with a named one: a date, an organization, a figure, a person, a version number. If you cannot, you lack the reporting. Say so explicitly rather than gesturing. This step must not invent the specific it wants.
9. **Burstiness.** Run the sentence-length variance check as a diagnostic. Fix by clause structure, never by inserting fragments.
10. **Affect.** Does the register shift anywhere across the piece? Constant temperature is a tell.
11. **Closure ritual.** Does any paragraph end on a pull-quote-shaped generalization? Cut it.
12. **Formatting.** Gratuitous bold on list stems, emoji in headings, heading density disproportionate to length, unnecessary title case.
13. **Re-check.** Did steps 1-8 change any load-bearing claim's meaning or confidence level? Revert that edit. Then re-run Pass 9 on every line the audit touched.

**The anti-slop tic.** Do not overcorrect into a second uniformity: categorically banning em dashes, sprinkling fragments, mandating register shifts, or performing casualness to prove humanity. That produces a recognizable second-order artificiality. The cure for machine register is specificity and structural asymmetry.

---

## Escalation record format

```
ESCALATION
  defect:      the 02:14 alert has no named actor
  found in:    Pass 2 (Force), sentence 41
  real class:  reporting
  why not me:  converting to active requires an actor the material does not name
  target:      source corpus / the incident owner
  status:      open
```

Escalations and reporting gaps are successful outputs. A run over thin material that produces none did not run the passes; it smoothed the prose over the holes.

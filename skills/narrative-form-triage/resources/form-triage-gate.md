# Form Triage Gate: Full Procedure

Reference matter for `narrative-form-triage`. The SKILL.md body holds the gate and the selection table. This file holds the worked runs, the protocols, and the contract template.

## Contents
- [Attribution notes](#attribution-notes)
- [The six questions, with evidence tests](#the-six-questions-with-evidence-tests)
- [Three worked triage runs](#three-worked-triage-runs)
- [ABT development card](#abt-development-card)
- [Handling DHY material](#handling-dhy-material)
- [Thesis vs theme adjudication](#thesis-vs-theme-adjudication)
- [Opponent warrant tiers](#opponent-warrant-tiers)
- [Empty Slot Protocol](#empty-slot-protocol)
- [The refusal catalogue](#the-refusal-catalogue)
- [Spine contract template](#spine-contract-template)
- [Pre-ship gate](#pre-ship-gate)

## Attribution notes

Carry these into any output that names a source.

- **Hart.** *Storycraft* separates story narrative (ch. 11), explanatory narrative (ch. 12) and other narratives (ch. 13). Hart's warning is that writers force explanatory material into "a full-blown story narrative, with a narrative arc and a climax and a denouement." Hart also writes that explanatory narrative "seldom" produces a point of insight and that "not every narrative has a resolution." The six-question instrument here mechanizes those distinctions. Hart does not publish it. Cite the books, not a gate.
- **"The Oregon Method" is not a codified canon.** It is a retrospective label for the newsroom coaching practice Hart ran. Citing named rules to it is fabricating a source. What is real and citable: story-conference-first, theme statement before drafting, editor as structural partner, structural revision before line revision.
- **SCAM (Setting, Character, Action, Meaning) is not Hart's acronym.** It comes from journalism pedagogy at Dynamics of Writing. It is compatible with Hart's scene chapter. Do not attribute it to him.
- **Numeric thresholds here are derived defaults.** Three scenes minimum at question 4, three paragraphs of undramatized evidence, five or six paragraphs to the nut graf, 3-5 nodes in a gathering, one screen to the governing thought. These are tunable operating defaults for mechanization. They are not published figures from any of the named authors.
- **ABT and the Narrative Spectrum** are Randy Olson's. **Pyramid and SCQA** are Barbara Minto's. **OCAR, LDR and ABDCE** are Joshua Schimel's. **The sparkline** is Nancy Duarte's. **The five-slot strategic narrative** is Andy Raskin's. **Martini glass, interactive slideshow and drill-down** are Segel and Heer's. **PR/FAQ** is Amazon's, documented by Bryar and Carr.

## The six questions, with evidence tests

Each question takes YES-with-citation or NO. An uncited YES is a NO.

**Q1. A single continuous entity whose state is tracked start to finish?**
Person or system both qualify. The system version is a traveling unit: one container of potatoes, one packet, one dollar of a fee, one patient sample, one training batch, one purchase order, one wafer. Test: does it appear in the record at both ends of the period the piece covers?

**Q2. Does the entity want something specific and reachable, documented?**
The failure is reading the want backward from the outcome. Ask: what dated source, written before the outcome, states the goal? A strategy memo, a filing, a design doc, a commit message, an interview given at the time. For a system subject, "want" is remapped to a design objective or an equilibrium, and it still needs a source.

**Q3. A dated, sourced rupture of the status quo?**
Run the inciting-incident test. Record four dates: the event; the earliest source treating the event as significant; the outcome; the source you cited. If the earliest source treating it as significant postdates the outcome, tag the slot RETROSPECTIVE-ONLY. Then name two other events in the same window that a narrator with a different ending would have chosen instead. If you cannot name two, you have not searched.

A RETROSPECTIVE-ONLY tag is a disclosure requirement, not a deletion rule. Genuinely causal events are often invisible to everyone present: a demographic shift, an accumulating design compromise, a slow change in a cost curve. The rule is that no RETROSPECTIVE-ONLY slot may carry unhedged causal language. Either downgrade the verbs, or add one sentence in the body saying the significance is visible only in hindsight.

**Q4. A continuous sourced action sequence, at least three renderable moments?**
Renderable means: a place, a time, named participants, and documented actions. Not "the team debated the tradeoff" but a meeting with a date, attendees and a recorded outcome. Three is the derived floor. Below it, the alternation that carries explanatory narrative has nothing to alternate with.

Most document-corpus work fails here, and that is the expected result. Hart writes for people who can go stand on the corner and ask the source what they were thinking. An agent working from filings, papers and post-hoc write-ups usually finds the scenic and interior material simply is not there. The correct response is to shift form, not to lower the evidentiary bar to keep the form.

**Q5. An evidenced point of insight?**
Hard test: name the behavior that changed after it, and the source showing the change. A realization with no behavioral consequence in the record is not a point of insight. Two specific failure shapes:
- *Promotion.* The largest number in the dataset, or the most recent event, gets nominated because the template has a slot.
- *Wrong subject.* The insight belongs to the analyst reading the corpus, not to anyone inside the material. Hart's point of insight is inside the story.

If no row qualifies, record NO POINT OF INSIGHT and downgrade to explanatory narrative.

**Q6. A resolution: a new stable state?**
If the situation is ongoing, say so in the piece rather than inventing closure. An unresolved ending is a legitimate ending. A manufactured one is a false claim about the world.

## Three worked triage runs

**Run A — a market history (semiconductor capacity, 2019-2024).**
Q1 YES: a single fab's capacity, tracked quarterly, sourced to filings. Q2 NO: the fab operator's "want" appears only in retrospective analyst commentary; contemporaneous filings state capital plans, not goals. Q3 YES: an export-control rule with a date and a text. Q4 YES: eleven dated events, four with named participants and recorded actions. Q5 NO: no source shows any participant's model being falsified and their behavior changing. Q6 NO: ongoing.
→ **EXPLANATORY NARRATIVE**, failing 2, 5, 6. Action line is the wafer. Structure: layer cake. Runner-up: pyramid, which lost because the audience is voluntary and the material rewards accumulation.

**Run B — an ML research writeup.**
Q1 YES: one model family across six training runs. Q2 YES: the project's stated objective is in the original proposal, dated before results. Q3 YES: run 4 diverged, logged. Q4 NO: two renderable moments, not three; the rest is metrics without participants.
→ **DO NOT NARRATE**, failing 4. Deliverable is OCAR mapped to IMRaD, opened with the one strong concrete moment as texture. No arc language anywhere. The team wanted "the story of how we found it"; the honest output is that the record supports a finding, not a story.

**Run C — a supply-chain incident review.**
Q1 YES. Q2 YES. Q3 YES. Q4 YES: six renderable moments across four sites. Q5 YES: the shift supervisor's own incident note records that she stopped trusting the sensor reading, and the log shows her procedure changed that night. Q6 YES: a new stable state, the revised procedure, in force since.
→ **STORY NARRATIVE**, all six pass. Now run the opponent warrant before writing anything: the "opponent" here is a calibration drift, so it is environmental pressure, not an adversary. Verbs restricted accordingly.

## ABT development card

Fill in this order. Every slot cites the corpus.

| Slot | Contents | Test |
|------|----------|------|
| BUT (first) | The single contradiction | Is there exactly one? Two that will not collapse = DHY |
| BUT, level check | Proximate harm, or the condition that permits it? | Pick the level where the THEREFORE is actionable |
| BUT, blocker check | Why has this not already been solved? | The answer is usually the real BUT |
| AND, ordinary world | Uncontested status quo | Could the reader have written this sentence? |
| AND, stakes | A number, a dollar figure, or a named consequence | Never "X is important" |
| THEREFORE | The consequence that follows from BUT | Does it follow from the BUT, or from what you wanted to recommend anyway? |

Then two whole-sentence checks:
- **WHAT before HOW.** Right: "the reserve is now severely degraded, after fifty years of clearing, pollution and parcel sales." Wrong: "over fifty years, trees were cleared, pollution rose and parcels were sold, leaving the reserve degraded."
- **Dobzhansky check.** "Nothing in [domain] makes sense except in the light of [one mechanism]." If blank two needs an "and," you have two narratives. Also state one thing blank two does *not* explain, and name the second-best lens you rejected. The test rewards a single lens, so it will over-fit genuinely multi-causal material and produce a confident, elegant, wrong explanation.

**AAA output template:** "This material contains no contradiction. It is [n] independent findings with no causal chain between them. A narrative arc would fabricate the chain. Recommended form: pyramid, inductive grouping, key line of [n] items."

## Handling DHY material

Two or more simultaneous contradictions read as confusing. The standard advice is to reduce to one. That advice is right for communication and dangerous for analysis: genuinely multi-causal findings get flattened into one elegant mechanism.

Choose one:
1. **Split into separate deliverables.** Preferred when both contradictions have full evidence.
2. **Elect one spine, demote the rest to an appendix**, with a named set-aside note in the body: "A second contradiction runs through this material — [X]. It is set aside here because [reason], and treated in [location]."
3. **Switch to taxonomy**, which does not require a single spine.

Never reduce silently. The set-aside log is a required contract field.

## Thesis vs theme adjudication

Write the organizing idea as one sentence, then apply the falsifiability test.

- **Falsifiable → thesis.** Route to pyramid, OCAR, PR/FAQ or SCQA. State it early and plainly. Defend it with evidence that is mutually exclusive and collectively exhaustive. Cap at three take-home messages, each one sentence.
- **A claim about meaning or value → theme.** Examples: "institutions defend their own metabolism," "action creates identity." Route to a story structure, and then *do not state it*. It is carried by outcome. The reader may reject it and still be moved.
- **Both present → nest.** Thesis goes in the nut graf or the governing thought, stated. Theme stays implicit in the scenes and in what the ending chooses to end on.

Two mirror-image failures:
- **Theme asserted as thesis** produces moralizing. "This shows that greed always wins" converts a resonant piece into an argument the reader will fight.
- **Thesis left as theme** produces analytic mush. The reader finishes unable to say what was claimed. This one is far more common in model output, because withholding feels sophisticated.

Theme statement form, when you use one: `[NOUN] [TRANSITIVE VERB] [NOUN]`. Reject intransitive verbs and any form of "to be." Reject proper nouns. Build the chronology table before the theme statement is allowed, or the theme will bend the material.

## Opponent warrant tiers

Require three independent kinds of evidence for any antagonist.

| Evidence | What it looks like |
|----------|-------------------|
| Competition | Both parties sought the same scarce object at overlapping times, documented |
| Awareness | Each party knew of the other: a memo, filing, earnings call, commit message, interview |
| Directed action | At least one action by A that the record shows was taken *because of* B, sourced |

- **3 of 3 = opponent.** Permitted verbs: target, counter, retaliate, undercut.
- **2 of 3 = rival.** Permitted verbs: compete with, gain share against.
- **1 or 0 = environmental pressure.** Permitted verbs: coincide with, constrain, be present during. No transitive verbs of intent.

For a system subject, the opponent slot takes a named force with a documented mechanism: a binding constraint, a regulatory regime, a physical limit, a countervailing incentive. Ban "the market wanted," "the industry decided," "physics fought back" unless the sentence immediately cashes the phrase out into the mechanism.

If nothing reaches 2 of 3, leave the slot empty and say so: "No adversary appears in the record; the binding constraint was X."

## Empty Slot Protocol

A slot with zero evidence and no candidate event. Choose in this order.

**MOVE 1 (default) — declare the absence in the body.** "No source records what was decided in that room." "The record is silent on why the threshold was set at 40%." A named absence is a legitimate narrative beat. It creates tension rather than destroying it.

**MOVE 2 — downgrade and substitute.** Use the best-documented adjacent event and reduce its structural weight in the same sentence: "the nearest thing to a turning point in the record is X, though nobody at the time treated it as one."

**MOVE 3 — change the architecture.** Two or more major slots empty means the material does not have this shape. Re-run selection over structures that do not require the missing slots: chronicle, braided comparison, taxonomy, single-question investigation.

**ILLEGAL — fill by inference, disclosed only in an endnote, appendix or methods block.** Readers experience the body, not the back matter.

**ILLEGAL — fill by invention of any kind**, including invented but "representative" detail, and including detail flagged as illustrative.

**BUDGET** — at most one inference-filled slot per piece, never at the climax. **LOG** — record every empty slot and the move chosen; the log ships with the deliverable.

Disclosure placement is load-bearing and will degrade silently. Any later "tighten this up" pass strips disclosure sentences first. Mark them non-removable and keep them within two sentences of the claim, in the same typographic register as the surrounding prose.

## The refusal catalogue

Each of these is a complete, successful output.

1. Refuse a story arc when the corpus contains no documented desire for the proposed protagonist. Report the absence. Do not infer motive.
2. Refuse a story arc when the proposed opponent is a real named party whose intent is not documented. Substitute a constraint, an incentive or a status quo.
3. Refuse to fill an empty template slot from outside the corpus.
4. Refuse to state a theme. If it must be stated, it is a thesis and the structure must change.
5. Refuse to withhold a thesis. Withholding a falsifiable claim for suspense in analytical material is a defect.
6. Refuse to reduce multi-causal material to one mechanism without disclosing what was set aside.
7. Refuse to open with an anecdote whose position in the distribution is unknown.
8. Refuse to change spine mid-draft. Escalate for an explicit restart with a logged reason.
9. Refuse to declare the plan finished when the read-through test fails, regardless of prose quality.
10. Refuse to discard contradicting evidence silently. Evidence that merely fails to support may be pruned. Evidence that contradicts must be surfaced.

**The counter-rule.** Refusing is also a bias. The red-team literature is stocked asymmetrically with attacks on agency-based explanation, so an agent steeped in it will over-attribute outcomes to luck, structure and path dependence. Every refusal output must name the strongest agency-based reading it considered and say why it was not adopted. "The lens disfavours agency" is not a reason.

## Spine contract template

```
SPINE CONTRACT — [deliverable name] — [date] — FROZEN

FORM:              [STORY NARRATIVE | EXPLANATORY NARRATIVE | MULTI-NODE GATHERING | DO NOT NARRATE]
FAILING QUESTIONS: [numbers, or "none"]
ABT:               "___ AND ___, BUT ___, THEREFORE ___"
                   AND cite: [ref]  BUT cite: [ref]  THEREFORE cite: [ref]
                   [or: NO BUT IN MATERIAL — spectrum band AAA]
STRUCTURE:         [name]
RUNNER-UP:         [name] — lost because [reason]
THESIS OR THEME:   [thesis | theme] — "[the sentence]" — [stated early | never stated]
BOREDOM BUDGET:    The reader is permitted to be bored in [zone] and nowhere else.
NESTING:           [scenes nested inside explanatory spine at depth n | one nut graf, at para n | none]
OPENING CASE:      [what] — distribution position: [median | tail | unique]
EMPTY SLOTS:       [slot] → [MOVE 1 | MOVE 2 | MOVE 3]
SET ASIDE:         [contradiction or evidence dropped] — because [reason] — [contradicting | not-supporting]
AGENCY READING:    Strongest agency-based account considered: [___]. Not adopted because [___].
ATTRIBUTION:       [named sources used, with the caveats from this file]
```

## Pre-ship gate

Run before the contract leaves triage. Assume a specialist has already published a demolition; what did they find?

- Would this explanation have made the outcome predictable in advance? If not, is the piece labelled description rather than explanation?
- What selection rule produced this corpus? Is it survival? Is that said in the text?
- Name two entities that took the same actions and did not get the same outcome. Are they in the plan?
- Which corpus items appear nowhere in the plan, and why? An omission that would weaken the spine, with no justification, is a cherry-pick.
- Which claim gets the most words relative to its evidence? Which best-evidenced driver gets the fewest? Was it suppressed by the arc?
- Name the linchpin assumption whose failure collapses the spine. Is it stated in the body, with its implications if wrong?
- Does every opponent have 3-of-3 or 2-of-3 warrant, and do the verbs match the tier?
- Does any real person think, feel, believe, worry or intend anything without a sourced statement that they did?
- Are all disclosures in the body, within two sentences of the claim, in the same register?
- Count hedges, contingency notes and disclosure sentences per thousand words. Over budget is a signal to change architecture, not to spend more budget.
- Read only the headlines in sequence. Do they alone tell a complete argument? Headings that are labels ("Background," "Analysis," "Findings") mean the grouping failed.

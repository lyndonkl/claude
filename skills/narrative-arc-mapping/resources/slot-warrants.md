# Slot Warrants, Absence Handling, and the Output Gate

Every structural slot is a claim that a moment mattered. This file holds the cards and audits that decide whether a slot may be filled, what to do when it may not, and how to tell finished architecture from a fabricated shape.

## The structural slot warrant card

Run this per PRESENT slot. It is a deliverable, not scratch.

```
SLOT: [step number and name]
EVENT PLACED HERE: 
(a) event date:
(b) date of the EARLIEST source treating this event as significant:
(c) outcome date:
(d) date of the source actually cited:
SOURCE TYPE: primary/contemporaneous | secondary/retrospective
SOURCE INTEREST: promotional | adversarial | regulatory | disinterested | unknown

TAG:
  if (b) > (c)                        -> RETROSPECTIVE-ONLY
  if (b) between event and outcome    -> CONTEMPORANEOUS-PARTIAL
  if (b) at or before the event       -> CONTEMPORANEOUS

SUBSTITUTION TEST (mandatory for RETROSPECTIVE-ONLY):
  Name two other events in the same window that a narrator working toward a
  DIFFERENT ending would have selected for this slot.
  1.
  2.
  (Cannot name two? You have not searched the corpus. Go back.)

CAUSAL TIER: L1 mechanism | L2 correlation | L3 sequence | L4 adjacency | L5 conjecture
DISCLOSURE REQUIRED IN BODY? yes/no  |  DISCLOSURE SENTENCE:
```

**Hard rule:** no slot may be tagged RETROSPECTIVE-ONLY *and* carry unhedged causal language. Either downgrade the language, or add one sentence in the body text (never a footnote) saying the significance is visible only in hindsight.

**This is a disclosure requirement, not a deletion rule.** Some genuinely causal events are invisible to everyone present: a slow demographic shift, an accumulating maintenance deferral, a mutation. An agent that mechanically demotes every RETROSPECTIVE-ONLY slot refuses to name real structural causes and over-weights whatever happened to be loud at the time. That is salience bias wearing the costume of rigor.

## The causal tier ladder and permitted verbs

Apply to every causal assertion and to every juxtaposition a reader would read causally.

| Tier | Definition | Permitted verbs |
|---|---|---|
| L1 MECHANISM | The linking step itself is documented: a decision memo, a physical process, an accounting identity, a signed contract, a commit that changed the behaviour | any causal verb |
| L2 CORRELATION | Quantitative co-movement documented, mechanism not | moved with, tracked, accompanied |
| L3 SEQUENCE | Only temporal order documented | then, afterwards, in the following quarter |
| L4 ADJACENCY | Co-present, no link established | rewrite so the two events do not touch, or state "the two were concurrent; no link is documented" |
| L5 CONJECTURE | Your inference, no source | must carry an explicit inference marker, and may never occupy a climax, revelation, or thesis slot |

**Because-laundering** is what happens when a tagger constrains connectives: the causal claim moves where the tagger cannot see it. Into a metaphor ("the dam broke"), into a section break, into a chart annotation, into a chapter title, into a quoted source who asserts the causality on your behalf. Scan headings, captions, pull-quotes, and section transitions, not just body sentences.

**Adjacency-by-layout check:** scan for L3/L4 event pairs separated only by a paragraph break, a scene cut, or a heading. Structural juxtaposition is a causal claim made without words.

**Tag inflation:** an L3 claim does not become L1 because a source *asserts* a mechanism. L1 requires a source that *documents* one.

## Hindsight determinism: the specific disease of endpoint-first derivation

Deriving the weakness backward from a known ending manufactures a starting deficiency chosen to make the ending look inevitable.

| Domain | The confabulated weakness | What the record actually showed |
|---|---|---|
| Market history | "The incumbent was always complacent" | Contemporaneous filings show three funded internal programs targeting the same shift |
| ML research | "The field had been ignoring long-context evaluation" | The field had been actively debating it; two workshops predate the paper |
| Institutional post-mortem | "Safety culture had eroded for years" | Erosion is asserted only in the post-incident inquiry; pre-incident audits found the opposite |

**Procedure:**
1. List every claimed starting weakness.
2. For each, find a source dated before the outcome asserting the deficiency.
3. Found and the source is disinterested: keep the weakness, attribute inline with the date. "Auditors flagged the single-supplier dependency in 2017."
4. Found but the source is interested (a competitor, a plaintiff, a promoter): keep it, and say whose view it was.
5. Not found: mark the weakness INFERRED. It may appear in the piece. It may not occupy the climax or the thesis sentence, and it must carry an inference marker within two sentences.

**Flip test on every evaluative sentence about a decision:** rewrite it assuming the opposite outcome occurred. If it obviously would not have been written that way, the outcome is doing the work, not the evidence. (Valid only for sentences about decisions. Applied to sentences about facts it produces nonsense.)

**Decision/outcome separation:** state decision quality and outcome quality in separate sentences. "The bet had roughly even odds on the information then available. It failed." Not "the reckless bet failed."

**Systems get halos too.** "An efficient market," "a rational consolidation," "an inevitable standardisation" are all outcome-derived characterisations of a prior state.

## Opponent warrant

Truby's opponent must want the same thing the protagonist wants. Real evidence frequently contains competitors, constraints, and coincidences but no opponent.

The warrant evidence test, the verb tier table, and the four-corner opposition worksheet are owned by `narrative-opposition-web` — see [../../narrative-opposition-web/resources/opponent-warrant.md](../../narrative-opposition-web/resources/opponent-warrant.md) and [../../narrative-opposition-web/resources/four-corner-worksheet.md](../../narrative-opposition-web/resources/four-corner-worksheet.md). An opponent that skill has not warranted may not be marked PRESENT here.

If no candidate clears that test, leave the slot EMPTY and say so in the body: "No adversary appears in the record; the binding constraint was the single-certified-supplier clause."

**When the protagonist is a system**, the opponent slot must be filled by a named force with a documented mechanism: a binding constraint, a regulatory regime, a physical limit, a countervailing incentive. Ban "the market wanted," "the industry decided," "physics fought back" unless cashed out into the mechanism in the same sentence.

**No opponent at all?** Substitute a MYSTERY at the same structural position. Truby's detective-story rule: the audience needs something to replace the ongoing conflict. Do not proceed with neither. In scientific findings and supply-chain analysis the mystery substitution is usually the honest answer.

**The strawman test.** Write the opponent's justification in their own voice: a paragraph making a strong, coherent, wrong-but-defensible case. Read it and ask whether a smart person holding that position would recognise themselves. If not, rewrite until they would. Assigning the opponent role to whoever lost and backfilling stupidity is simultaneously worse craft and false analysis. It is the most reputationally damaging failure this skill can commit.

**Manufactured conflict** is the companion failure: inventing a same-goal rivalry between parties who were simply operating in different markets. Check that both actually contested the same scarce thing.

## Moral argument spine

Map each element to evidence. Leave unsupported elements visibly EMPTY. An empty element is a finding about the material, not a prompt to invent.

```
Theme line (one sentence, a claim about how to act):
Starting beliefs and values:
Moral weakness (hurting others from weakness or ignorance, not evil):
Moral need:
First immoral action:
Desire:
Drive:
Early compromises made out of desperation while losing:
Criticism by others:
Justification by the subject:
Attack by ally:
Obsessive drive after the second revelation:
Intensified compromises:
Intensified criticism / intensified justification:
Battle (which values are shown superior, regardless of who wins):
Final action against the opponent:
Moral self-revelation (never stated to the reader):
Moral decision (a choice between TWO POSITIVES, as late as possible):
Thematic revelation (the insight that reaches beyond these particular subjects):
```

**THE THEME IS ENACTED, NEVER STATED IN NARRATOR VOICE.** Explicit moral language is permitted in exactly three positions:

1. An ally criticising the protagonist.
2. Direct protagonist-opponent conflict at the battle.
3. The opponent's justification.

Everywhere else, structure carries it. Detection: search the draft for the theme line's key nouns in narrator voice. Each hit is a candidate deletion. Building a correct spine and then also stating the lesson destroys the argument.

**BALANCE CHECK:** count moral beats against event beats. Preachiness comes from too little plot to carry the argument. If moral beats outnumber events, cut moral beats or add events. Do not soften the language.

**EXPLANATORY MODE.** Some material genuinely has no moral argument: a benchmark result, a pricing mechanism, a taxonomy, a measurement method. Forcing one manufactures a villain and produces sanctimony. "No moral argument available; this is an explanatory piece" is a legitimate output. In explanatory mode, run the seven mandatory steps with the moral spine marked NOT APPLICABLE and the thematic revelation replaced by a transferable mechanism.

**DOUBLE REVERSAL.** Where the opponent also has a need, give them a self-revelation too, and connect the two: each must learn something from the other. State the synthesis in the working notes only: "the best of what both learned is ____." A genuine double reversal produces a THIRD position neither party held at the start, stateable in one sentence and defensible on the evidence. If the synthesis is the midpoint of the two starting positions, no reversal occurred and you have written "both sides had a point," which is a refusal to argue. Sentimental redemption is the second failure: check for a post-battle behavioural change in the record before granting the opponent a revelation.

## Revelation sequence audit

A revelation is information whose arrival forces a change in desire, motive, or plan. Information that arrives and changes nothing is exposition. Relabel it.

Per revelation record: WHO learns it (subject / reader / both), WHAT changes (desire, motive, or plan), INTENSITY 1-10, SOURCE.

Checks:
- **Order is logical**: the order the subject would plausibly have learned things. For researched material this is usually the order evidence became available. Check dates.
- **Intensity climbs monotonically.** Any dip is moved, merged, or cut.
- **Intensity is rated by the SIZE OF THE COURSE CHANGE**, never by the language used to describe it. A reveal that changes nothing cannot be an 8 no matter how it is written. "And then, devastatingly, the margin compressed further" is not escalation; it is an adjective. Manufactured escalation satisfies the audit on paper and the reader feels the padding.
- **Pace accelerates**: word-gaps between reveals are shorter in the last third than the first.
- **Bend, not break**: each changed desire adjusts the original rather than replacing it. A wholly new goal resets the reader's investment to zero.
- **Three decision points carry all four elements together**: revelation, decision, changed desire, changed motive. Missing one deflates the moment.
- **Count target met** for the length. Never the two or three a three-act template implies.
- **Chronology check on every reorder.** Reordering for escalation that implies impossible foreknowledge is a defect, not a style choice.

Intensity worked example, from a database incident corpus:

| Reveal | Course change forced | Rating |
|---|---|---|
| Replica lag alert was real, not a flap | On-call escalates instead of silencing | 4 |
| The failover target shared the same power domain | The entire recovery plan is invalid; a new one must be written mid-incident | 9 |
| A second team had already filed this risk in 2021 | Nothing changes during the incident; changes the post-incident scope | 3 (during) / 7 (as audience revelation) |

Note the third row: rating depends on whose course changes and when. That is what "size of course change" means in practice.

## Agency audit and the system translation table

Fill and keep as an auditable artifact whenever the protagonist is a system.

```
Subject level declared and held constant:
WEAKNESS -> structural fragility/dependency/assumption, CONTEMPORANEOUS source:
NEED -> what the system must resolve to keep functioning, unrecognised at the start:
GHOST -> prior event still constraining behaviour:
DESIRE -> visible collective goal + the moment success becomes verifiable:
OPPONENT -> competing force pursuing THE SAME goal by incompatible means:
PLAN -> dominant strategy, standard, or consensus approach:
ALLY / ATTACK BY ALLY -> internal dissent (ABSENT if the record shows none):
REVELATIONS -> disclosures, crashes, benchmark results, failed audits:
BATTLE -> decisive contest, smallest possible space:
SELF-REVELATION -> what it now knows, evidenced by observed behaviour change:
NEW EQUILIBRIUM -> changed steady state, explicitly higher or lower:
DELEGATION -> the named human or institution who demonstrably held the desire:
ARCHETYPES -> not translated. Confirm none applied to institutions.
```

**AGENCY AUDIT.** List every intentional verb attached to an abstraction in the output. For each, either rewrite to named actors or cite the collective mechanism that justifies it.

| Laundered | Repaired |
|---|---|
| "The market realised the dependency was fragile" | "Three of the five largest buyers added second-source clauses in the same quarter" |
| "The standards body wanted backward compatibility" | "The compatibility requirement passed 11-4; the four dissents are in the minutes" |
| "The codebase resisted the refactor" | "Every attempt touched the shared session object, and the four prior attempts were reverted within a week" |

**Prefer personification by delegation.** Give the system's desire a named carrier who demonstrably held it, and let that carrier's actions stand for the system's. That keeps the discipline honest and the narrative concrete.

## Proportion and omission audit

Per-sentence checks can all pass while the piece as a whole misrepresents the drift and proportion of events through selection and emphasis alone. This is the expensive audit and it is the one that matters.

1. Two columns per claim: WORDS SPENT, and EVIDENCE TIER (from the causal ladder), plus CAUSAL WEIGHT. Fill the weight column **before** the arc is chosen, or it is contaminated by the same halo the audit exists to catch.
2. Flag claims in the top quintile by words and the bottom quintile by evidence tier. These are the colourful anecdotes carrying the reader's belief.
3. Flag the inverse: top quintile by causal weight, bottom by words. These are the boring drivers the arc suppressed. Usually a price change, a filing, a base rate, a demographic trend, a compiler flag.
4. Require a written justification per flagged asymmetry. "This gets 800 words because it is the only first-hand account of the mechanism" is legitimate. No justification means rebalance.
5. **Omission check:** list corpus items appearing nowhere in the draft and state why for each. An item that would weaken the spine, omitted without justification, is a cherry-pick and must be reinstated.
6. The output is a justification requirement, not a word-count quota. Mechanical equalisation produces the rhythm of a spreadsheet, and unread accurate work informs nobody.

## Two further disclosure operations

**Anachronism flag.** When a category, a metric, or a moral frame used in the text did not exist at the time described, say so. That operation is checkable. The larger dispute about applying present-day categories to past actors is contested territory and is deliberately not encoded here as a rule.

**Silent evidence.** For every success-attribution claim, search for at least two entities that took the same action and did not get the outcome. There are three legal results, and all three appear in the text. Counterexamples found: state them and weaken the claim. Searched for and not found: state the search, which strengthens the claim. Population is n=1 or unobservable: state "the base rate for this action is unknown." The third result is first-class and non-embarrassing. Without it, agents fabricate weak analogies and present them as base rates.

**Consider the agency reading.** For each major outcome, state the strongest skill-and-intent explanation you considered and why you did or did not adopt it. Over-attributing outcomes to luck, structure, and path dependence is also a bias, and the literature that warns against narrative is asymmetrically stocked with attacks on agency-based explanation.

## GOOD / BAD output gate

Run this before handing off. A single BAD in the first three rows is a stop.

| GOOD | BAD |
|---|---|
| **At least one of the 22 steps is reported ABSENT with a reason** | **All 22 filled** |
| The designing principle excluded material; three excluded claims are named | Everything researched appears somewhere |
| Every structural reorder survives a date check | Reordering for escalation that implies impossible foreknowledge |
| The opponent's justification would be recognised by someone who holds that position | The opponent is whoever lost |
| Exactly one apparent defeat; the rest demoted to setbacks explicitly | Three or four low points of similar weight |
| Drive actions differ in kind; swapping any two would break the argument | Five interchangeable instances of the same beat |
| Reveal count matches the length target; intensity climbs by course-change size | Two or three reveals, or escalation carried by adjectives |
| The theme line appears nowhere in narrator voice | The lesson is stated, then also dramatised |
| Every corner of the web appears in the drive section | The web collapses to two parties after the opening |
| A double reversal producing a THIRD position neither party held | "Both sides had a point" |
| The moral decision is a choice between two positives, held late | A choice between an obvious good and an obvious bad |
| The step-to-evidence table can be handed to a fact-checker | The architecture exists only inside the narrative |
| Output stops at the tagged scene weave | The macro layer has written prose |
| Disclosures sit in the body within two sentences of the claim | Disclosures live in endnotes, footnotes, or a methods block |

**Density budget.** Cap disclosure sentences, hedges, and contingency notes at roughly one per 250 words. When the budget binds, that is the signal to change the architecture (Empty-Slot Move 3), not to spend more budget. A piece that is 60% epistemic apparatus and 40% subject is unreadable and misleading in a new way: it makes your uncertainty the story. (This cap is a working default for this skill, not a published figure.)

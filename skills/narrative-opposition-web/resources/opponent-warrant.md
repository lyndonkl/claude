# Opponent Warrant, the Seven-Gate Audit, and the Empty Slot

Everything here answers one question: has this entity earned the opponent slot, or is it just the party that lost?

## Table of Contents
- [The warrant evidence test](#the-warrant-evidence-test)
- [Verb constraints by tier](#verb-constraints-by-tier)
- [The seven-gate best-possible-opponent audit](#the-seven-gate-best-possible-opponent-audit)
- [Writing the justification paragraph](#writing-the-justification-paragraph)
- [The double reversal and the third position](#the-double-reversal-and-the-third-position)
- [The system constraint inventory](#the-system-constraint-inventory)
- [The mystery substitute](#the-mystery-substitute)
- [Exposure escalation](#exposure-escalation)

## The warrant evidence test

Real evidence frequently contains competitors, constraints, and coincidences but no opponent. An agent that needs an opponent to complete a shape will find one, and the cheapest one available is an inferred intention.

For each candidate, gather three independent evidence types.

**COMPETITION.** Documentary evidence that both parties sought the same scarce object at overlapping times. Not "both were in the same business." The same object: a contract, a standard, a customer, a frequency allocation, a merge right, a budget line, a seat on a committee.

**AWARENESS.** Evidence that each party knew of the other. A memo, a filing, an earnings call, a commit message, a court exhibit, an interview, a footnote.

**DIRECTED ACTION.** At least one action by A that the record shows was taken *because of* B, with a dated source for the "because." This is the type most often missing and most often assumed.

Scoring: 3/3 opponent, 2/3 rival, 0-1/3 environmental pressure.

The tell of a fabricated warrant is a transitive verb with no dated source for the because. Grep your own draft for "in response to," "to counter," "aimed at," "in order to block." Each hit must resolve to a document.

The mirror failure is over-application. A thin archive that lacks awareness evidence does not turn a documented rivalry into weather. Two of three plus an explicit note naming the missing type is honest and usable.

Worked scoring, three domains:

| Case | Competition | Awareness | Directed action | Tier |
|---|---|---|---|---|
| Two standards bodies balloting incompatible specs for the same interface | Yes: same ballot, same interface | Yes: each spec cites the other | Yes: chair's minutes record the schedule change "given the parallel effort" | OPPONENT |
| A generic manufacturer and the originator whose patent expired | Yes: same molecule, same market | Yes: litigation record | Missing: no dated evidence the originator's pricing move was aimed at this entrant specifically | RIVAL |
| A drought and a water utility's expansion plan | No shared object | Not applicable | Not applicable | ENVIRONMENT |
| A new labour statute and a haulier's route network | No shared object; the statute predates the network | Haulier's filings cite the statute | Statute was not written about the haulier | ENVIRONMENT (binding constraint) |

## Verb constraints by tier

Assign verbs at warrant time, in the notes, before prose exists. Verbs are where the claim actually lives, and they leak.

| Tier | May use | May never use |
|---|---|---|
| OPPONENT | targeted, countered, retaliated against, undercut, moved to block, matched, pre-empted | — |
| RIVAL | competed with, gained share against, bid against, arrived at the same time, offered a cheaper equivalent | any verb implying the act was aimed at the other party |
| ENVIRONMENT | coincided with, constrained, bound, set the ceiling on, was present during, narrowed | every transitive verb of intent: wanted, decided, chose, sought, punished, refused, fought back |

Worked repairs:

- Environment written as opponent: "The new emissions limit went after the older fleet." → "The limit bound at 2.4 grams. Every vehicle in the older fleet was certified above it, and none could be recertified without a new head design."
- Rival written as opponent: "The upstart moved to strangle the incumbent's flagship line." → "The upstart priced its equivalent 30 percent below the flagship. Nothing in its board minutes mentions the flagship."
- System written as agent: "The grid decided to shed the industrial load." → "The under-frequency relay is set to trip at 49.5 hertz. Frequency reached 49.4 at 03:12 and the relay tripped, dropping the industrial feeders."

**Do not over-correct.** Stripping intentional verbs into agentless passives ("share was observed to shift," "the load was shed") is worse, because passive voice obscures causation rather than clarifying it. The goal is to relocate agency onto the entity that actually has it. Post-pass check: count agentless passives before and after. If they went up, the pass failed.

One deliberate, flagged personification per major section is acceptable when you can state in one line what mechanism it stands in for. Purism buys nothing and costs readability.

## The seven-gate best-possible-opponent audit

Run in order on corner B. A gate that fails sends you back to candidate selection, not forward with a weaker opponent.

**1. SAME GOAL.** State in one sentence the single thing both parties are fighting to control or possess. Push to the deepest level of the conflict. If the honest answer is that they wanted different things, this is a competitor, not an opponent. Go deeper or replace the candidate.

- Fails: "The archive wanted to preserve the collection; the developer wanted to build on the site." Different goals; both could have won.
- Passes: "Both were fighting for the same thing: who decides what the block is for. The archive's claim ran through the landmark listing, the developer's through the zoning variance, and only one instrument could govern."

**2. NECESSITY.** Name the exact mechanism by which THIS opponent attacks THIS protagonist's specific weakness. Not "they compete." If the opponent would be equally dangerous to any protagonist, they are generic, and the piece will feel arbitrary.

**3. RELENTLESSNESS.** Does the opponent attack that weakness repeatedly across the span of the piece, or once? Count the documented instances. One instance is an event, not an opposition.

**4. VALUE CONFLICT.** Three to five values per side, stated as goods, each cited. Verify they conflict directly rather than merely differ. "One valued speed, the other valued documentation" is a difference. "One held that a released artifact is a promise, the other that a released artifact is a draft" is a conflict, because both cannot govern the same repository.

**5. THE DOUBLE.** Name what the opponent shares with the protagonist. In what way is each the other's mirror? Two parties with nothing in common are strangers. The shared thing is usually a value neither will state aloud, or a weakness both have.

> **System variant.** A constraint has no mirror. Name instead the constraint or incentive **both** A and B are subject to, with a citation. A yield ceiling that binds only one side is asymmetric pressure, not a double.

**6. POWER PARITY.** Does the opponent have real power, status, and ability? An opponent weaker than the protagonist produces no story and, in analytical work, usually signals hagiography. If your opponent is outmatched, you are probably writing a defence of the protagonist and should say so.

> **System variant.** A constraint has no status. Ask instead whether it actually **binds inside the window**, with the evidence that it did. A constraint that never binds is environment, not corner B — route it to the constraint inventory.

**7. JUSTIFICATION.** See the next section. Mandatory artifact.

> **System variant.** A constraint cannot speak. Write the justification in the voice of the documented human or institutional **carrier** — the person or body that acted to preserve the constraint, or acted under it and defended doing so. If no carrier is documented, this gate returns **N/A**, the corner is not an opponent, and it routes to the constraint inventory.

## Writing the justification paragraph

A paragraph in which the opponent makes a strong, coherent, defensible case for what they did, in their own voice, first person, present tense of their own moment. Not a confession. Not a concession. Not a villain speech.

Rules:

- No self-incrimination. Nobody narrates their own guilt. "We knew the risk and shipped anyway" is a writer's sentence, not an opponent's.
- No hedging on their own behalf. They believe this.
- Every factual assertion in it must be one the opponent actually made or could have made from what they knew at the time.
- It must be a good argument. If yours is easy to refute, you have not found the real one.

**RECOGNITION TEST.** Would a competent person holding this position read it and say "yes, that is why I did it"? If not, rewrite until they would. If you cannot, you do not yet understand the opposition and should return to the material.

**FALSIFICATION PASS.** If B's justification is more persuasive than A's position, you have assigned the roles backwards. Swap and re-derive. Do not weaken B.

### Strawman versus steelman, three domains

**Public-health logistics, corner B is the ministry directorate.**

- Strawman: "Head office cared about its numbers, not about children. Wastage looked bad on the dashboard, so the boxes went where they would be safest, not where they were needed."
- Steelman: "Every dose that spoils in a district was taken from a district that would have used it. I am not allocating vaccine, I am allocating the consequences of a cold chain that cannot reach everywhere at once, and the only defensible rule is the one I can apply the same way in all fifty-one districts. Her villages are hard to reach. So are four hundred others, and every officer who reaches them by accepting spoilage is asking me to fund that spoilage from someone else's allocation. I would rather be accused of a spreadsheet than of choosing favourites."

**Open-source governance, corner B is the commercial vendor.**

- Strawman: "The vendor saw a free library it could take over and took it, because that is what companies do."
- Steelman: "Ten thousand businesses depend on two volunteers who have never promised anyone anything, and everyone has agreed to call this a healthy ecosystem. We offered to fund it and were told no, which is their right. So we hired one of them and forked the rest. Our customers now have a support window with a number on it. I am aware this looks like capture. The alternative was continuing to ship a dependency whose maintenance plan is that two people stay interested."

**Scientific controversy, corner C is the journal editors.**

- Strawman: "The editors protected their prestige by refusing to print corrections."
- Steelman: "A journal is not a court and I am not a judge. If I start deciding which of two competent teams is right, I have replaced peer review with editorial taste, and the next editor will use that power for something worse. My job is to publish work that meets the standard and let the field adjudicate. Yes, that leaves the original claim standing longer than the critics would like. It also leaves it standing when the critics are wrong, which has happened in this journal three times that I can name."

Note what the steelman versions share: they concede the appearance, they name the cost, and they still conclude. That is what a real position sounds like.

## The double reversal and the third position

Advanced move, and the structural form of intellectual honesty in analytical work: grant a self-revelation to the opponent as well as the protagonist. The reader receives two insights rather than one verdict.

Procedure:

1. Both A and B must have a weakness and a need. An opponent with no need is a force, not a corner, and cannot reverse.
2. Establish that B is capable of changing position. For an institution, show it revising its position at least once, with a document.
3. Write B's revelation alongside A's, at or after the decisive contest.
4. CONNECT them. A must learn something from B and B something from A. Two independent lessons are two arcs, not a reversal.
5. State the synthesis in your working notes, never in the prose: "the best of what both learned is ____."

**THIRD-POSITION TEST.** A genuine double reversal produces a position neither party held at the start, stateable in one sentence and defensible on the evidence. If your synthesis is the midpoint of the two starting positions, no reversal occurred and you have written false balance. "Both sides had a point" is a refusal to argue, not a richer argument.

**SENTIMENTAL REDEMPTION CHECK.** B's revelation must be supported by something B actually said or did afterward. Check the record for a post-contest behavioural change. Absent that, B did not learn anything and you should say so.

## The system constraint inventory

When the protagonist is a market, a protocol, an institution, a codebase, a supply chain, or an ecosystem, the opponent slot is usually filled by a constraint. Resist filling it with a party merely because the slot exists.

For each constraint, record:

```
CONSTRAINT: ____
TYPE: physical / capital / regulatory / informational / latency / yield / contractual / headcount
MECHANISM: the specific pathway by which it binds, with units where units exist
WHEN IT BINDS: the conditions under which it starts setting the outcome
                (a constraint that never binds is background, not opposition)
CARRIER (optional): the named human or institution that speaks for it and can be quoted
EVIDENCE: source
```

Common types by domain, as a prompt list rather than a taxonomy:

- Physical: thermal limits, tolerance windows, half-life, road time, port draft, bandwidth-distance product
- Capital: minimum efficient scale, the cost of the next unit of capacity, working-capital cycle
- Regulatory: a certification clock, a disclosure deadline, a licence condition, an ownership cap
- Informational: what the system does not measure and therefore cannot respond to
- Latency: settlement time, review time, procurement time, the delay in a feedback loop
- Yield: the fraction of attempts that survive to output, and how it scales

A constraint acquires narrative force through **binding**, not through motive. The dramatic moment is the first time it sets the outcome, staged at a specific timestamp, in a specific place, with a specific number, witnessed by a specific named person.

**Responsibility check, run in both directions.** For every systemic attribution, ask whether a specific named actor had the authority and the information to do otherwise. If yes, name them. "The system failed" is often a sentence written to avoid naming a person, and a constraint-based opponent slot makes that evasion easy to write and hard to see. Systemic explanation is additive to individual accountability, never a substitute for it. The reverse also holds: naming a person where a binding constraint did the work is the original error this skill exists to prevent.

**Do not let the frame become the finding.** The stance that institutions are the larger forces is powerful because it is a stance. Adopted as a default, it concludes that every system is unreformable, which is inevitability with the sign flipped. Include at least one documented partial success, or state explicitly the conditions under which this system has changed before.

## The mystery substitute

Some material genuinely has no opponent. Scientific findings, supply-chain descriptions, benchmark results, and process explanations often contain no party who opposed any other. Do not proceed with neither an opponent nor a substitute; the reader needs something to replace the ongoing conflict.

Introduce a MYSTERY at the same structural position the opponent would have occupied: early, before the drive, alongside the protagonist's plan.

A usable mystery has four properties:

1. **A specific unanswered question**, not a topic. "Why did the yields differ between the two lines when the recipes were identical?" not "the mystery of manufacturing variance."
2. **A reason the answer was not available at the time.** The reader must believe the question was genuinely open.
3. **A partial answer arriving in pieces**, at an accelerating pace, more of them near the end.
4. **A resolution the material actually supports.** If the record never answered it, say so. An unresolved mystery honestly labelled beats a resolved one you supplied.

Worked: an epidemiological cluster with no antagonist. The mystery is "why did the cases follow the bus route and not the water main?" Pieces arrive as the case map, the negative water samples, the driver's shift log, the ventilation schematic. Resolution: the shared enclosed air. No opponent anywhere, and the piece has a spine.

Alternative substitutes when no mystery exists either:

- **A deadline**: a fixed date after which the protagonist's options close, documented.
- **A binding constraint approaching**: a buffer draining toward zero, with the number and the rate.
- **A verification question**: will the claim hold when someone finally checks it?

If none of these is available, the honest output is: "This material supports explanation, not opposition." That is a complete answer. Report it.

## Exposure escalation

Where a real named living person or an active institution occupies an adversarial slot, surface it for human decision. Do not adjudicate it yourself. Adverse inference about a living party creates legal exposure that is not the writer's to resolve, and a subject who consented to an interview consented to an interview, not to a structural role in someone's argument.

Emit this block, one per exposed party, alongside the web:

```
EXPOSURE FLAG
PARTY: name, and whether living person / active institution / both
SLOT: which corner, and the warrant tier assigned
ADVERSE INFERENCE BEING MADE: state it plainly, in the words a reader would take away
EVIDENCE BEHIND IT: the citations, by type (competition / awareness / directed action)
WHAT IS NOT EVIDENCED: the part of the inference the record does not reach
CONSENT STATUS: did this party speak to the project, and if so, to what did they agree?
WHO DECLINED OR IS ABSENT: and does their absence flatter anyone in the piece?
DECISION REQUIRED FROM: human reviewer
```

Two rules that make this real rather than ceremonial:

- **Disclosure is not a currency.** Flagging an inference does not authorise it. "We noted the uncertainty, so we can print it" is the reasoning to refuse. The flag routes a decision; it does not pre-approve one.
- **Source-availability bias is part of the exposure.** A cast selected by who agreed to talk systematically flatters cooperative parties and indicts silent ones. List who is missing from the web and why, in the flag and in the piece.

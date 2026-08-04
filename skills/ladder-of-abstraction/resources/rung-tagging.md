# Rung Tagging: Definitions, Variants, and Repairs

Reference matter for Steps 2 through 4 of the ladder audit.

## Table of Contents
- [Rung Definitions with Edge Cases](#rung-definitions-with-edge-cases)
- [Person Variant and System Variant](#person-variant-and-system-variant)
- [Worked Tagging: Three Passages](#worked-tagging-three-passages)
- [The Trap Repair Table](#the-trap-repair-table)
- [Before and After: Climbing Down](#before-and-after-climbing-down)
- [The Gap Log](#the-gap-log)
- [Sawtooth Fatigue: A Worked Counter-Example](#sawtooth-fatigue-a-worked-counter-example)

## Rung Definitions with Edge Cases

**R1 — named particulars.** A person with a name, a date, a physical object, a number carrying a unit, a quoted sentence, a document with an identifier. The test: could this be photographed, timestamped, or cited to a specific line in a specific source?

Edge cases that are NOT R1:
- A number with no unit and no comparison. "Volume rose 40 percent" without a base, a period, or a denominator is R2 wearing a number.
- A generic person. "A warehouse worker would typically arrive around six" is R2. "Marisol Reyes clocked in at 05:48 on 14 January" is R1.
- Sensory adjectives attached to a general practice. "The floor was tense and loud during earnings weeks" is summary in costume: it has sensory words, no date, no named actor, no source.
- A composite or representative example constructed by you. That is invention with an R1 shape.

**R2 — category, mechanism, process, policy.** Names a class of thing or explains how something works, with no instance attached. "Liquidity providers", "inference latency", "instructional units", "capacity constraints", "the escalation policy", "second-line antibiotics".

R2 is not a defect. It is where the explanation lives. It becomes a defect when it has no R1 nearby to stand on.

**R3 — system pattern.** A statement that holds across more than one instance and could be falsified by a counter-case. "Contract prices lag spot prices at every regime change in this sample." "Models trained past the compute-optimal point degrade first on the rarest tokens." "Every one of the four recalls began with a supplier substitution that skipped requalification."

If it cannot be falsified by a counter-case, it is not R3; it is R4 or it is nothing.

**R4 — meaning and stakes.** Trust, risk, obsolescence, scarcity, accountability, control, dependence. R4 is where the piece says what the pattern is worth. It is also where meaning inflation lives. See [top-rung-discipline.md](top-rung-discipline.md).

## Person Variant and System Variant

Everything in this skill works when the protagonist is a market, a protocol, an institution, a codebase, or a supply chain. The rungs change what they contain, not how they behave.

| Rung | Person protagonist | System protagonist |
|------|--------------------|--------------------|
| R1 | A named person doing one observable thing at one time in one place | A dated price print, a single transaction ID, one wafer lot number, a log line with a timestamp, an instrument reading with units, one filing |
| R2 | The role, the authority, the routine, the incentive the person operated under | The mechanism: the fee schedule, the queueing discipline, the retry policy, the requalification procedure |
| R3 | The pattern across people in that role or that period | The pattern across episodes, nodes, or regimes |
| R4 | What it cost, what it meant, what was at stake | Same |

**Finding R1 when the protagonist is a system.** Systems have no faces, but they have first-detection events: the first measurement outside tolerance, the first customer complaint, the first failed settlement, the first line in a log, the first empty shelf. Choose the detection event with the best combination of a precise timestamp, a named human present, a number attached, and a documented reaction. Write it at instrument resolution: what the screen actually showed, in what units, what the normal range was, what the observer did next.

Then climb exactly one rung: say what the reading was a reading OF, at system scale. Do not climb two.

**The intentional-verb rule at R2.** When the subject of a sentence is a system, market, institution, model, or abstraction, classify the main verb:

- MECHANICAL — rose, cleared, propagated, saturated, reallocated, timed out. Allowed.
- INTENTIONAL — wanted, decided, chose, sought, punished, learned, refused. Repair.
- EVALUATIVE-TELEOLOGICAL — matured, advanced, evolved toward, progressed, naturally moved to. Repair.

Four repairs, in preference order:
1. **Name the actor.** "The market punished the issuer" becomes "three of the four largest holders sold into the bid on 12 May".
2. **Name the mechanism.** "The protocol wanted lower latency" becomes "the fee schedule paid more for blocks confirmed inside 400ms".
3. **Name the selection pressure.** "The industry evolved toward containerization" becomes "carriers that did not containerize lost margin on the transpacific lane and exited; the survivors all had".
4. **Quote the human.** "The company decided" becomes the person, the meeting, the memo.

If none of the four can be made from the material, that is a research gap, not a style problem. Log it.

**Do not overcorrect.** A hard ban on agency produces "prices were observed to decline", which obscures causation worse than the anthropomorphism did. Count agentless passives after the pass; if they rose, the pass failed. The rule is a claim filter, not a purity filter. Repair intentional verbs that assert false causation. Tolerate the ones that are transparently figurative and locally unambiguous. Permit at most one flagged personification per major section, and only where you can name in one line the mechanism it stands in for.

## Worked Tagging: Three Passages

### Passage A — supply chain (before)

> [P1] Global logistics networks in the period were subject to increasing capacity constraints. [P2] Utilization across major container routes approached theoretical maxima, and the resulting congestion propagated through downstream distribution channels. [P3] Stakeholders across the ecosystem faced significant operational challenges. [P4] Ultimately, this reveals something fundamental about the fragility of interconnected systems.

Tags: P1 = R2. P2 = R2. P3 = R2. P4 = R4.

Violations: Rule 1 (three consecutive R2, STALLED RUN). Rule 3 (P1, P2, P3 all MIDDLE-RUNG TRAP, no R1 within plus-or-minus 2). Rule 4 (P3 to P4 is an ALTITUDE JUMP from the middle straight to meaning). Rule 5 (FLOATING OPENER). P4 also fails the generic test: "the fragility of interconnected systems" attaches to any supply chain story ever written.

Note the trap here is not vocabulary. Replacing "theoretical maxima" with "the most they could handle" lowers the Fog score by two points and leaves the paragraph exactly as unintelligible, because the reader still cannot see anything.

### Passage A — after climbing down

> [P1] The *Ever Given* wedged across the Suez Canal on 23 March 2021 and stayed there six days. Behind it, 369 ships queued. [P2] A container route is a fixed-slot system: berth windows are booked months out, and a ship that misses its window does not get the next one, it gets the one after that. [P3] By the time the canal cleared, Felixstowe was turning away trucks because its yard was full of boxes whose onward trains had already run. [P4] Congestion in a fixed-slot network does not dissipate; it queues, and the queue outlives the blockage that caused it.

Tags: P1 = R1. P2 = R2. P3 = R1. P4 = R3.

Every rule satisfied. Note the ceiling dropped from R4 to R3, and the paragraph got *more* specific rather than simpler. That is climbing down.

### Passage B — ML writeup (before)

> Model performance degradation manifested across evaluation suites as training progressed beyond the optimal compute allocation. The underlying mechanism relates to distributional shift in gradient contributions. This illustrates the fundamental tension between scale and generalization in modern machine learning.

Tags: sentence 1 = R2, sentence 2 = R2, sentence 3 = R4. Middle share 67 percent. ALTITUDE JUMP at the close, and the R4 is generic: "the fundamental tension between scale and generalization" could close any scaling paper.

### Passage B — after

> At 41,000 steps the model still answered "what is the capital of France" correctly and had started answering "what is the capital of Burkina Faso" with "Ouagadougou is a city in Burkina Faso." Accuracy on the common half of the eval set was flat. On the rarest decile it had fallen 11 points. Past the compute-optimal point, the losses do not spread evenly: they land first on the examples the model saw least.

Tags: R1, R1, R2, R3. Ceiling held at R3, which is what the ablation actually supports.

### Passage C — biography (before)

> Throughout her tenure she maintained tight control over organizational decision-making processes. Delegation of authority was limited, and approval workflows routed through the executive office. Her leadership style ultimately reflects the eternal struggle between vision and trust.

Tags: R2, R2, R4. Same shape as A and B in a completely different domain: two middle-rung paragraphs and a jump to a universal.

### Passage C — after

> On 3 March 1988 she declined the second fab in a two-line memo: "Not yet. Bring it back in the spring." She had already declined it in November. [R1] Every capital request above $50,000 crossed her desk, in a company of 1,900 people. [R1, number with unit and denominator] It is the same signature on the 1991 expansion she later said she wished she had approved a year earlier. [R1] Control was the thing she could not delegate, and it cost her the year. [R4]

The R4 survives here because it is small and specific. "Control was the thing she could not delegate" is about this person, not about leadership. Its counter-sentence would be "she delegated freely and the delay came from elsewhere", and the two memos contradict it. That is an earned top rung.

## The Trap Repair Table

| Trap type | Symptom in the draft | Repair | Explicitly forbidden |
|-----------|----------------------|--------|----------------------|
| MIDDLE-RUNG TRAP | R2 paragraph with no R1 within plus-or-minus 2 | Find one particular instance of the mechanism in the material and place it adjacent | Replacing jargon with plainer jargon; adding an analogy in place of an instance |
| STALLED RUN | 3+ consecutive R2/R3 | Insert an R1 instance between them, or merge two abstractions into one | Padding with a transitional paragraph |
| UNGROUNDED ASCENT | R3/R4 run with no R1 in the prior 2 beats | Move an existing R1 earlier in the section | Writing a new illustrative example from imagination |
| ALTITUDE JUMP | R1 immediately followed by R4 | Insert the R2 mechanism or R3 pattern the particular belongs to | Softening the R4 with a hedge and leaving the jump |
| FLOATING OPENER | Piece or section opens at R2/R3/R4 | Open with the particular that made you believe the claim | Adding a scene-setting paragraph not in the record |
| COSTUME R1 | Sensory adjectives on a general practice | Demote to clean R2 summary, or promote with a date, a place, and named actors from the record | Keeping it because it reads well |
| MISSING A-FRAME | Piece ends at R3/R4 | Descend to an R1 the reader already met | Ending on a summary of the argument |

## The Gap Log

When a trap has no repair in the material, the output is a log entry, not prose. Format:

```
GAP-04
  Paragraph: 12
  Mechanism needing an instance: how requalification was skipped
  Artifact that would supply it: a supplier change order, a QA sign-off sheet,
    or an email approving the substitution
  Where searched: supplier correspondence 2019-2021, QA archive index, recall filing exhibits
  Interim treatment: paragraph left as honest summary, no particular asserted
  Escalation: no — one gap in this section
```

Rules for the log:
- A gap entry is a successful outcome, not a failure. It is what prevents fabrication.
- Three or more gaps in one section triggers escalation: report that the defect is missing material, and that it cannot be fixed at the prose layer.
- Never resolve a gap with a composite, a typical case, or a reconstruction. A plausible specific is worse than an admitted absence, because it is undetectable downstream.
- If the gap cannot be filled and the section still needs to exist, shift the form: more summary distance, more explicit mechanism, fewer implied scenes.

## Sawtooth Fatigue: A Worked Counter-Example

The run rules are ceilings, not a rhythm. This passage satisfies every rule and is unreadable:

> On 14 January a pallet of resin arrived at the Newark cross-dock. Cross-docks hold inventory for under 24 hours by design. The pallet left at 22:10. Transfer times determine whether a route is a dock or a warehouse. Two days later it was in Charlotte. Regional distribution operates on a hub-and-spoke topology.

Tags: R1, R2, R1, R2, R1, R2. Zero violations. Six paragraphs, no idea developed, and the reader cannot say what the passage argued.

Diagnostic: if more than half the paragraphs change rung from their neighbor, consolidate. Merge the R2 sentences into one explanation that carries all three particulars, and let the R1s run consecutively as a sequence.

Repaired:

> On 14 January a pallet of resin arrived at the Newark cross-dock, left at 22:10, and was in Charlotte two days later. It never entered a warehouse. That is the design: a cross-dock is defined by holding nothing longer than a day, and the entire regional network is built around the assumption that transfers clear in hours.

Tags: R1, R1, R2. Same information, one idea developed.

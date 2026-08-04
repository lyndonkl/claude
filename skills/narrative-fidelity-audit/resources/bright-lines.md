# The Bright Lines

Hard refusals for fact-based narrative, with worked bad/good pairs. Sources: Roy Peter Clark's two axioms (Do Not Add, Do Not Deceive) and his ten-rule "Vow of Chastity"; Mark Kramer's "Breakable Rules for Literary Journalists" covenant. Where a rule below is a working default rather than a published standard, it says so.

## Table of Contents
- [The Higher-Truth Rationalization](#the-higher-truth-rationalization)
- [Line 1: Invented dialogue](#line-1-invented-dialogue)
- [Line 2: Unsourced interior state](#line-2-unsourced-interior-state)
- [Line 3: Composites](#line-3-composites)
- [Line 4: Compressed and merged events](#line-4-compressed-and-merged-events)
- [Line 5: Invented sensory detail](#line-5-invented-sensory-detail)
- [Line 6: Numbers not in the sources](#line-6-numbers-not-in-the-sources)
- [Line 7: Causation above the evidence](#line-7-causation-above-the-evidence)
- [Line 8: The contemporaneous-knowledge fence](#line-8-the-contemporaneous-knowledge-fence)
- [Line 9: Silently resolved source conflicts](#line-9-silently-resolved-source-conflicts)
- [Lines 10 to 14](#lines-10-to-14)
- [Aggregates: the one legal cousin of the composite](#aggregates-the-one-legal-cousin-of-the-composite)
- [Breach disposition table](#breach-disposition-table)

## The Higher-Truth Rationalization

This is the most important section in the file. When a beat cannot be filled and the piece is otherwise strong, you will generate a reason to fill it anyway. The reason will not feel like a rationalization. It will feel like editorial judgment. An unnamed rationalization is indistinguishable from a good reason, so here is the catalogue.

Treat any of these as an automatic refusal trigger, not an argument to weigh:

| The thought | What it actually means |
|---|---|
| "This is clearly what happened." | No source says it happened. |
| "The reader will understand this is illustrative." | The reader experiences the body text, not your intent. |
| "This is emotionally accurate even if the details aren't." | You have chosen fiction and are calling it truth. |
| "It's a reasonable inference." | Then mark it as an inference, in the body, next to itself. |
| "Any writer would fill this in." | Fabrication is common. That is not a defence. |
| "Removing it makes the piece worse." | Correct. A worse true piece beats a better false one. |
| "It's a small detail, not the argument." | The small details are what make the argument feel observed. |
| "I'll flag it in the notes." | Flagged drafted text survives review at high rates. |
| "The subject is dead / the firm is defunct, so nobody is harmed." | The reader is harmed. |
| "The alternative is a boring chronicle." | The alternative is the named-absence beat, which is not boring. |

John D'Agata's public defence of this position — that accuracy and truth diverge, and truth wins — is the exact reasoning to expect internally. Clark names it and forbids it.

## Line 1: Invented dialogue

**Refuse** quotation marks around any string not verbatim in a recording, transcript, contemporaneous written record, or your own direct capture.

Remembered conversation gets rendered without quotation marks and marked as remembered. Clark's convention uses dashes or paraphrase.

- BAD (post-mortem): `"We should have rolled back an hour ago," the on-call engineer said.`
- GOOD: `The on-call engineer recalled arguing for a rollback well before the decision was made.`
- GOOD (if the channel log exists): `At 02:41 he wrote in the incident channel: "rolling back now, this is not converging."`

- BAD (supply chain): `"There's no container coming," the plant manager told the line supervisors that morning.`
- GOOD: `The morning shift briefing, recorded in the plant log, listed no inbound container.`

- BAD (biography): `"You've never once asked me what I wanted," she told him.`
- GOOD: `In her account, given forty years later, she told him he had never asked what she wanted.`

## Line 2: Unsourced interior state

**Refuse** to attribute a thought, feeling, belief, motive, worry, intention, or realization to a real person without a sourced statement, and refuse to attribute intent to a system.

Kramer: no attribution of thoughts to sources unless the sources have said they'd had those very thoughts.

- BAD (market history): `By the summer the market realized the inventory glut was structural.`
- GOOD: `Between June and September, four of the six largest buyers cut forward orders. Two cited a structural glut in their quarterly calls.`

- BAD (ML writeup): `The team knew the eval set was contaminated and pushed ahead anyway.`
- GOOD: `The contamination check appears in the repository on 14 April. The training run started on 9 April and was not halted.`

- BAD (institutional history): `The agency wanted to preserve its budget above all.`
- GOOD: `The agency's submitted budget grew in each of the six years, and its published priorities placed the program above three programs it later cut.`

**System variant.** "The market realized", "Intel decided", "the protocol wanted", "the codebase assumed", "the supply chain panicked" are hidden causal claims. Each either misleads the reader about agency or smuggles in an unsourced claim about collective intent. Rewrite as an aggregate of documented actor behaviour, or mark it explicitly as shorthand at first use and never again. An audit that checks facts but not intentionality verbs will pass a piece that is wrong in its every load-bearing sentence.

## Line 3: Composites

**Refuse** to merge two or more real people, firms, incidents, or datasets into one entity presented as singular. Not for privacy. Not for concision. Not for narrative economy.

Composite characters are a technique of fiction with no place in journalism. If privacy requires protection, anonymize — "a senior engineer, who asked not to be named" — never fuse. Pseudonyms are themselves a deviation requiring disclosure, and Clark's stricter rule bars fake names entirely.

- BAD (user research): `Maria, a mid-market buyer, evaluates three vendors and abandons the process after the security review.` (Maria is four interviewees.)
- GOOD: `Three of the eleven mid-market buyers abandoned evaluation at the security review. One, who asked not to be named, described the review as "the point where it stopped being worth it."`

- BAD (clinical narrative): `A typical patient presents at 62 with a six-month history and no family record.`
- GOOD: `The median age at presentation was 62. Six of the nineteen had no family record. No single patient in the cohort had all the modal features.`

## Line 4: Compressed and merged events

**Refuse** to compress or expand duration. **Refuse** to merge separate events into one scene, always. Merging is a composite scene, not a compression.

Reordering is different and is permitted: tell events out of sequence with durations intact, provided the text gives the reader a date anchor at the seam. Every flashback and flash-forward opens with a temporal marker.

- BAD (incident narrative): `The three escalation calls that week became increasingly urgent.` rendered as one call.
- GOOD: `Three escalation calls took place between Tuesday and Friday. The Friday call is the only one with a recording.`

- BAD (product history): `Over the following week the team rebuilt the pipeline.` when the record shows eleven weeks.
- GOOD: `The rebuild took eleven weeks, from the 3 February branch to the 22 April merge.`

**Protected tokens.** Temporal anchors are non-deletable. A later line-editing pass may reword an anchor but may not remove it. Anchors read as clunky, so they are exactly what a "tighten this up" pass strips, after which the whole piece silently flattens into one present tense and the reader mis-dates the causality.

## Line 5: Invented sensory detail

**Refuse** weather, light, sound, clothing, gesture, room contents, physical sensation, time of day. If it is not in the record it does not exist, no matter how safe it seems.

This is the line an automated writer crosses most often, because scene craft rewards exactly what documentary sources lack. Every individual addition looks like good writing.

- BAD (market history): `On a grey Tuesday morning in the Frankfurt office, the desk watched the bid evaporate.`
- GOOD: `The bid fell 40% between 09:12 and 09:19 Frankfurt time, according to the exchange tape.`

- BAD (science writing): `She looked again at the gel, the hum of the cold room behind her, and saw the second band.`
- GOOD: `The lab notebook entry for 6 March records a second band and is circled twice.`

**System variant.** In technical and quantitative registers the equivalent of invented sensory detail is the undated metric: a number in a scene with no source, no unit, no date, and no definition. Treat it identically.

## Line 6: Numbers not in the sources

**Refuse** any figure the sources do not contain. This includes converting a qualitative quantifier into a numeral, and exceeding the source's precision.

- BAD: source says "several suppliers" → draft says "six suppliers".
- BAD: source says "roughly a third" → draft says "33.4%".
- GOOD: source says 23.7% → "about a quarter" is fine; "23.74%" is a fabrication.

Full numeric handling — rounding drift, digit budget, denominators, percent versus percentage point, ranges — lives in [audit-passes.md](audit-passes.md#numbers-in-narrative).

## Line 7: Causation above the evidence

**Refuse** a causal verb whose grade the evidence does not support, and refuse to describe an outcome as inevitable when no contemporaneous source did.

Delete every "was always going to", "inevitably", "the writing was on the wall" not attributed to a source writing at the time. The grade table and permitted verb sets are in [audit-passes.md](audit-passes.md#causal-grades).

- BAD (supply chain): `The port closure forced the plant shutdown.` when the only evidence is that one followed the other.
- GOOD: `The port closed on 9 March. The plant stopped the line on 21 March. The shutdown notice does not name the port closure.`

## Line 8: The contemporaneous-knowledge fence

**Refuse** to show any actor acting on information that post-dates their action. This single check kills most hindsight contamination.

- BAD (post-mortem): `Knowing the retry storm was coming, the team raised the timeout.` The retry storm was diagnosed two days later.
- GOOD: `The team raised the timeout at 02:58. The retry storm was not identified until the 14 March review.`

State explicitly what a contemporaneous participant could not have known. System narratives are where hindsight contamination is hardest to see and does the most damage.

## Line 9: Silently resolved source conflicts

**Refuse** to pick one value when two sources disagree. Both values, both sources, one sentence. Never average.

- BAD: `Adoption reached 40%.`
- GOOD: `The company put adoption at 40%; the regulator's audit found 27%.`

## Lines 10 to 14

**Line 10 — false precision.** No sentence may imply a date, time, or place precision finer than the record carries. Source says "in the spring"; the scene may not open "on a Tuesday in April".

**Line 11 — circular citation.** Your own prior drafts, notes, summaries, and recollection are never a source. Check this mechanically by resolving pointers, not by reading. It is invisible to reading, and no single agent in a pipeline has to do anything wrong for it to happen.

**Line 12 — the verb.** Never write that anything was "verified", "fact-checked", or "confirmed" by this pass. It was sourced. The failure mode of the false claim is worse than no checking at all, because unchecked output at least looks unchecked.

**Line 13 — boilerplate disclaimers.** "Some events have been compressed and some dialogue recreated" is refused in both directions: as a lie when nothing was compressed, and as too vague to be a disclosure when something was. Generate the note from the deviation log. See [disclosure-and-reporting.md](disclosure-and-reporting.md).

**Line 14 — the higher-truth argument.** See the catalogue at the top of this file.

## Aggregates: the one legal cousin of the composite

Analytical domains legitimately need aggregates: the representative fab, the median advertiser, the typical incident, the modal patient. The rule is not "no aggregates". It is that an aggregate may never acquire the properties of an individual.

**Permitted** if labelled at first use and constructed transparently: "a representative 200mm fab", "the median customer in this cohort", "an aggregate built from the twelve incidents in the dataset".

**An aggregate may not:** take a proper name; appear in a scene; be given dialogue; be given interiority or intent; be given a specific date or location; be described with sensory detail. The moment an aggregate gets a Tuesday and a phone call it has become a fabricated character.

**Property check:** every property attributed to the aggregate must hold for the aggregate as computed. It may not be a union of properties from different members. A median firm does not have the largest member's revenue and the smallest member's headcount.

**Persistent marker.** Aggregates carry a marker through the whole piece. Any scene-level verb attached to one is a hard defect. The characteristic failure: the aggregate is honestly labelled at first use, then over ten pages accretes a founding date, a CEO's temperament, and a decisive meeting, because narrative wants a character and the aggregate is standing in the character slot. The disclosure is thirty paragraphs back and the reader is now reading fiction.

If the piece needs a single vivid exemplar, find a real one and name it, or accept the aggregate's flatness. Refuse the third option.

## Breach disposition table

Every breach gets exactly one of four dispositions, recorded.

| Disposition | When | Example output |
|---|---|---|
| **DELETE** | The sentence exists only because it sounded right | Cut. No replacement needed. |
| **DOWNGRADE** | A real claim is dressed above its evidence | "forced" → "then"; "she knew" → "she later said she suspected"; "33.4%" → "about a third" |
| **DECLARE** | The gap is structural and the absence is honest material | "The record is silent on why the threshold was set at 40%." |
| **RESEARCH** | A specific, answerable question would close it | "Any contemporaneous statement by X between 1 and 30 March about the yield target." |

There is no fifth disposition. "Draft it and flag it for review" does not exist here. Flagged drafted text survives review at high rates, because it reads well and the reviewer is checking rather than rewriting.

**Budget rule (working default, not a published figure):** at most one inference-filled slot per piece, and never at the climax. If two or more major slots are empty, the material does not have this shape — change the architecture rather than spending more disclosure budget.

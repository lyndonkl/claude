# Narrative Distance Audit and the RUE Pass

Two passes that run after the scene is built. Order matters: RUE first, then the distance audit, because RUE can delete or swap a scene and change the audit's inputs.

## The RUE pass (Resist the Urge to Explain)

1. Mark every sentence in and around the scene that explains what the scene means.
2. Delete all of them.
3. Re-read the scene cold.
4. If the meaning is still available to a reader who has not seen your notes, keep the deletions permanently.
5. If the meaning is gone, **the scene is the wrong scene**. Swap it for one that carries the meaning. Do not restore the explanation.

Step 5 is the whole point and the step that gets skipped. Restoring the sentence produces a scene that is decorative plus an assertion that is unsupported. Two defects, not one.

**Worked example, supply chain.**

- Before: "The *Ever Lissome* logged in at 06:12 and did not begin discharge until 19:40. This thirteen-hour delay shows how badly the terminal's labor constraints had begun to bind, and illustrates the broader crisis in West Gulf capacity that spring."
- After RUE: "The *Ever Lissome* logged in at 06:12 and did not begin discharge until 19:40."
- Test: does a reader get "the ship waited on people, not cranes"? Only if the surrounding text has established that the cranes were idle. If it has not, the fix is a different scene or an added sourced fact, not the restored sentence.

**Worked example, post-mortem.**

- Before: "The page went to a rotation retired in March, revealing a deeper truth about how ownership erodes in fast-moving organizations."
- After RUE: "The page went to a rotation retired in March."
- The generalization was not just unnecessary. It was a claim about organizations in general, made with evidence about one rotation.

## The S / C / X audit

1. Label every paragraph **S** (summary) or **C** (scenic).
2. Anything you cannot label confidently is **X**. X is a defect, not a third mode.
3. Compute the scenic share and the longest run of each mode.
4. Compare against the form's targets.
5. Resolve every X before shipping.

| Form | Scenic share | Run-length rule |
|------|--------------|-----------------|
| Story narrative | 40-60% | No summary run over 3 paragraphs |
| Explanatory narrative | 15-30% | A scenic beat at least every 6-8 paragraphs |
| Analytical report or memo | 5-15% | Scenes at openings, section heads, and the close only |

These ratios are operational defaults derived for mechanization. They are not published figures from any craft text. Ship them as tunable config and say which values you used.

**What S and C actually differ on:** summary is abstract, reaches across time and space, organizes by topic, and conveys outcome. Scene is concrete, sits in one location in real time, organizes by sequence, and reproduces process. Emotion comes from proximity; understanding comes from the bird's-eye view. Neither is better.

## Summary in costume

The X paragraph is almost always the same defect: a general practice described with sensory adjectives. It has sensory words, no date, no named actor, and no source. It feels scenic and cites nothing, which makes it the most common fabrication vector in machine-written narrative nonfiction.

**Diagnostic markers:**
- Habitual verb forms: "would gather", "used to run", "each morning the team would".
- Plural unnamed actors: "traders", "engineers", "dispatchers", "the committee members".
- A time span instead of a time stamp: "that spring", "through the summer", "in those months".
- Sensory adjectives with no observer: "thick with tension", "the hum of the floor", "the smell of solder".

**Resolution, one of two.** Demote it, or promote it. Never leave it.

| Costume summary | Demote to clean summary | Promote to a real scene |
|---|---|---|
| "Traders would gather around the terminals each morning, the room thick with tension as the auction results printed." | "Auction results printed at 13:00; dealers had 30 minutes to reallocate before the cash close." | "At 13:02 on 15 May the results printed: the dealer take was 34.1%, against a 12-month average of 17.8%." |
| "Through the summer, engineers grew used to the nightly alerts and stopped acting on them." | "Between June and August, 812 alerts fired on this service; 14 produced a ticket." | "On 4 August the 03:12 page went to a rotation retired in March, and no one acknowledged it for 41 minutes." |
| "In those months she spent her evenings buried in the departmental correspondence." | "Her letters that spring refer repeatedly to departmental correspondence she was reading at home." | Only if a dated source exists. Otherwise there is no scene here, and the demotion is the answer. |

Promotion requires a date, a place, and named actors, each with a pointer. If you cannot supply all three, promotion is not available and demotion is the only legal move.

## The alternation rule

Scene and summary must earn their adjacency:

- After a scenic run, the next summary block must **explain something the scene made the reader want to know**.
- After a summary run, the next scene must **instantiate the claim just made**.

If neither holds, the alternation is decorative and one of the two blocks should be cut. A piece that alternates on a fixed rhythm regardless of content has implemented the shape of narrative and none of its function.

**Closing move:** endings usually pull back one notch in distance from the piece's dominant mode. A scene-heavy piece closes at summary distance; a summary-heavy piece closes on one concrete instance.

## Gap notes: the honest output when the record is thin

Literary-journalism sensory technique does not transfer to unreported domains. A writer working from filings, commit logs, berth records, or archives was in no room, saw no light, and heard no hum. Any instruction to engage the senses is gated on whether sensory observation exists in the source. Absent that gate, the output is atmospheric fiction attached to real claims, which is worse than dry prose.

When the record is thin, use one of these forms rather than a plausible specific:

- **Declared absence:** "What the committee discussed between 3 and 17 March is not recorded."
- **Bounded knowledge:** "The berth log gives arrival and discharge times. It does not record why the gap ran thirteen hours."
- **Source conflict left open:** "The RCA puts the exit at 09:47:11; the vendor's timeline puts it at 09:49. Both are in the record and they are not reconciled." Never resolve a documented conflict silently by picking the better-sounding value.
- **Refusal:** "This material supports an explanatory account with summary distance throughout. It does not support scenes: no dated moment in the corpus has a sourced setting, a sourced actor, and three ordered observable events."

The refusal is a successful outcome of this skill. Micro craft cannot repair absent reporting, and an agent that tries will manufacture the missing elements.

## Keeping systems out of the viewpoint chair

The audit is also where anthropomorphic drift gets caught, because drift accumulates across paragraphs rather than inside single sentences.

Count the intentional verbs attached to non-people: realized, decided, wanted, believed, chose, feared, learned, understood. Cap them. Personification is a legitimate framing device used once, explicitly. Used continuously it becomes an unfalsifiable causal claim distributed across every verb in the piece, and the causal claim never faces the citation discipline that an explicit claim would face.

| Drifted | Repaired |
|---|---|
| "The market realized the supply would not arrive." | "Front-month futures repriced 9% over two sessions after the port notice." |
| "The protocol wanted lower latency." | "The spec's stated design goal was sub-100ms confirmation (RFC draft s1.2)." |
| "The codebase resisted the change." | "The change touched 214 files across four services; three of them had no test coverage." |
| "The institution decided to look away." | "The board minutes for that quarter contain no reference to the audit finding." |

An imputed institutional intent is permitted only when a filing, a minute, a transcript, or a quoted executive supplies it. Systems have states, constraints, and incentives. Only people have wants.

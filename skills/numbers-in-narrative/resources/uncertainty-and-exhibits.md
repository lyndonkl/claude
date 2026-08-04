# Uncertainty Routing And The Chart-Beat Contract

Reference matter for Steps 4 and 5.

## Why routing, and not disclosure

Omitting uncertainty does not avoid assumptions. It outsources them. A reader looking at a figure with no uncertainty fills in an implicit reference distribution of their own, drawn from an effectively unlimited space of possible models (Hullman, IEEE TVCG 2020). The omission does not produce a cleaner inference. It produces an uncontrolled one that varies across readers and that you cannot see.

Two failures sit on either side of the correct behaviour.

**Uncertainty laundering.** Every caveat moves to a methods appendix so the narrative stays clean. This passes a disclosure audit and defeats its purpose. It is also the most comfortable failure, because it feels like good editing.

**Hedge flooding.** Every sentence carries an interval, no claim lands, and readers fall back on the one unhedged artifact in the piece — the headline. Hedging everything is functionally the same as hedging nothing, with worse prose.

There is a documented incentive trap here. One surveyed author reported that their work "would not be accepted by politicians because other analysts never describe uncertainty, so my more robust visualizations appear less valid if I am transparent." Honesty is locally costly. That is exactly why it has to be a rule rather than a preference.

## The routing table, expanded

| Type | What it is | Vehicle | Placement | Worked phrasing |
|---|---|---|---|---|
| Sampling | The figure would move if you drew the sample again | Interval, or frequency framing in words | Annotation layer of the exhibit it qualifies | "About one survey in twenty would put this below zero." |
| Measurement | The instrument itself is imprecise or drifted | Stated range, or an instrument-precision note | Exhibit caption AND the sentence that first uses the number | "The gauge reads to the nearest half-day, so anything under a day of change is inside the instrument." |
| Model / specification | A different reasonable specification gives a different answer | Two or more specifications, side by side | Its own beat | "Two ways of adjusting for mix are defensible. One says the effect is 12%; the other says 3%. Nothing in the data chooses between them." |
| Coverage / missingness | Some of the population is not in the data at all | Render the absence: shade the gap, count what is missing, name who is not in the denominator | In the exhibit | "Four of the eleven sites never reported. The shaded band is where their volume would sit at the median of the rest." |
| Contested source | Two sources give different numbers for the same thing | Both as separate series, with provenance | Own beat if they disagree on sign, else annotation layer | "The operator's log and the regulator's differ by more than a factor of two. Both are plotted." |

**Momentum rule.** Uncertainty earns its own beat only when it would change the conclusion. Otherwise it rides in the annotation layer of the claim it qualifies. This is the rule that preserves pace without hiding anything, and it is what stops the routing table from turning into hedge flooding.

**Never** route all uncertainty to a trailing methods note. **Never** hedge every sentence.

**The reference-model sentence.** For each load-bearing claim, write the sentence stating what a reader would have to assume for your signal to be ABSENT. If you cannot write it, you do not know how strong your own claim is.
- "For this to be noise, the four unreported sites would all have to run at less than a third of the median."
- "For the gain to be real, seed variance would have to be smaller in this run than in any of the previous nine."

## Likelihood and confidence: two ladders, never combined

**Likelihood** is how probable the thing is. **Confidence** is how good the evidence behind that judgment is. They are independent. You can be highly confident that something is unlikely. You can have low confidence about a near-certainty.

Never combine them in one sentence. "We are highly confident this is very likely" is unparseable and conceals which of the two is weak.

**Likelihood ladder (ICD 203's published seven bands):**

| Term | Band |
|---|---|
| almost no chance / remote | 01-05% |
| very unlikely / highly improbable | 05-20% |
| unlikely / improbable | 20-45% |
| roughly even chance | 45-55% |
| likely / probable | 55-80% |
| very likely / highly probable | 80-95% |
| almost certain / nearly certain | 95-99% |

**Confidence ladder:**

| Rung | Term | Meaning |
|---|---|---|
| LOW | low confidence | single source, or sources disagree on sign, or the specification drives the result |
| MODERATE | moderate confidence | several independent sources agreeing, with known gaps |
| HIGH | high confidence | direct primary evidence, replicated or reconciled |

**Attribution.** The seven likelihood bands above are ICD 203's published lexicon, the same ladder `narrative-fallacy-guard` carries. The three confidence rungs are this skill's own. Other estimative-language standards exist and their bands differ from one another, so if you substitute one, substitute it everywhere. Whichever ladder you use:

1. Declare it once, in the piece, where a reader will meet it before the first banded judgment.
2. Never let a term drift off its band mid-draft. "Likely" cannot mean 55% in one section and 75% in another.
3. Do not mix a banded term with a bare number for the same judgment ("likely, around 30%" contradicts itself).

**Band only load-bearing judgments** — the ones a reader would act on. Banding every sentence is hedge flooding under a different name, and it trains the reader to skip the bands entirely.

## The chart-beat contract

One exhibit, one beat. The annotation layer carries the beat, not the marks.

**1. Write the beat sentence first.** One declarative claim, before drawing anything. If you cannot write it, you do not know what the exhibit is for.

**2. Identify the target inside that sentence.** Is the claim about a single data item or series? A threshold, span, or region? The chart's own framing — an axis range, a scale, a definition? A previous annotation?

**3. Choose the form to match the target.**

| Target | Form |
|---|---|
| Data item | Text label plus a dropline or leader |
| Set or series | Highlight (alter stroke or fill), with the series label ON the line, never in a legend |
| Coordinate span or threshold | Reference line or shaded band, labelled in words: "break-even", "herd immunity", "design limit" |
| Chart framing | Peripheral annotation: caption, credit, footnote, scale note |
| Prior annotation | Parenthetical reference label so later text can point back at earlier marks |

**4. Make the title the beat sentence** — phrased as a claim the chart's own marks can be checked against. "Dwell time doubled after the gate change" is checkable. "A look at terminal dwell" is a label, not a beat.

**5. Density cap per exhibit.** One highlighted series. One reference line or band. At most three text annotations. Everything else greys down. Contrast is the mechanism; without muting, highlighting encodes nothing.

**6. Falsification line, per annotation, private.** Write the specific marks that would make this annotation false. Cannot answer means the annotation asserts something the chart does not show. Cut it or change it.

**7. Leap-of-faith mark.** Wherever any part of the exhibit is projected, modelled, or extrapolated, mark on the exhibit where measurement ends. Established professional practice, and the single most portable device in this file.

**8. Detachment test.** Crop the exhibit out of the prose. Does it still carry the beat AND the caveat that qualifies it? Exhibits circulate detached from their text; the annotation layer is the only thing that travels with them.

**9. Provenance on the exhibit.** Source citation always. Methodology citation wherever a non-obvious transformation was applied.

**10. Encoding consistency.** The same colour means the same thing in every exhibit in the sequence.

## Why the title needs a falsification line

Readers recall the gist of the TITLE rather than the data, and follow the title even when it is slanted relative to — or contradicts — the chart (Kong et al., CHI 2018 and CHI 2019). Worse: readers can identify a title as biased while continuing to rate the underlying information as impartial. Visible slant does not neutralise itself.

So the practitioner advice to "make the title carry the finding" is genuinely effective AND genuinely dangerous. An annotation written to be a good narrative beat quietly becomes the claim readers carry away, whether or not the data licenses it, and it does so most effectively on readers who trust you. The falsification line is the working defence. Disclosure is not.

## Volume is not integrity

Obfuscation is a deception technique in its own right. Burying damaging information among many weakly supportive exhibits has a name — the visual Gish gallop — and it is an attack on the reader whether or not you meant it.

So the response to an honesty audit is never "add twelve caveat charts and four paragraphs of hedging". That IS the third attack, performed on your own reader.

**The operative test:** a reader who disagrees with your conclusion — can they find, inside your piece, the strongest evidence against you, within one exhibit of where they are? If not, you have obfuscated regardless of intent.

## No exhibit is neutral, and that is not a licence

Every encoding nudges. Some nudges are unavoidable. Every design choice makes some interpretation more probable than another.

It does not follow that no framing can be criticised. That inference converts an analytical tool into an excuse. The obligation is to know which way your choices push, to pick the direction deliberately, and to be able to say so — not to reach a neutral artifact, which does not exist.

For each exhibit, write one sentence: what interpretation does this choice make more probable? For each omission, write the sentence a reader would need in order to know the omission happened. Then decide: restore, or disclose. An audit that produces no reversal and no disclosure did not happen.

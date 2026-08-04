# Rhythm Diagnostics

Sentence-length variance, end-stress, pace, and number handling. Everything in this file is a **diagnostic**: something you measure and report next to the prose. None of it is an objective to optimize. An agent that maximizes sentence-length variance inserts one-word sentences; an agent that applies 2-3-1 to every sentence produces prose made entirely of landings.

---

## Provenance of the numbers

**Every numeric threshold in this file is an operational default derived for mechanization. Hart publishes no such figures.** Both *Wordcraft* and *Storycraft* are lending-restricted, so the thresholds could not be verified against the primary text. Treat them as tunable config, state that provenance wherever the numbers are reported, and never write "Hart says the standard deviation should be at least 7."

The two things that are genuinely attributable: Hart's rhythm attribute is about cadence and sound pattern, and Gary Provost's five-word demonstration is the canonical illustration of why uniform sentence length deadens prose. The measurement scheme built on top of them is ours.

---

## Config block

Copy into the run header and adjust for register.

```yaml
# derived operational defaults, not published Hart figures
register: analytical            # analytical | explanatory | narrative
risk_class: HIGH                # HIGH blocks on claim-strength violations
sentence_length_mean: [15, 20]  # words; raise for academic, lower for general
sentence_length_sd_min: 7       # or 0.6 * mean, whichever is lower
short_sentence_per_words: 150   # at least one sentence under 8 words per N words
long_sentence_ceiling: 45       # words, without a structural reason
consecutive_similar_max: 2      # sentences within +/-2 words of each other
brevity_cut_target: [0.10, 0.20]
brevity_cut_alarm_low: 0.05     # below this, the pass did not run
brevity_cut_alarm_high: 0.30    # above this, diff the propositions
numbers_per_sentence_max: 1     # narrative passages
numbers_per_paragraph_max: 3
readability_target: null        # set explicitly per audience; no silent default
```

---

## Burstiness

**What it is.** Human prose alternates between short and long. Machine prose flatlines near a 14 to 22 word median with low variance, and that flatness is one of the most reliable machine signatures after vocabulary.

**Measure:** word count per sentence across the passage. Report mean and standard deviation, per paragraph and for the piece.

**Read the diagnostic, then act at the clause level:**
- Low SD with a high mean: the draft is all subordination. Split the longest sentence in each affected paragraph at its main clause boundary.
- Low SD with a low mean: the draft is all simple declaratives. Merge two adjacent short sentences that share a subject, unless the pair is in the clarity split log.
- Uniform paragraph lengths (every paragraph three sentences, 30 to 50 words) are a tell in their own right. Vary paragraph size as well.
- Three consecutive sentences beginning with the same construction (participle, prepositional phrase, "The X of Y", a name) is a defect regardless of length variance. Rewrite one.

**Failure mode: fragment cosplay.** Chasing variance produces "Everything changed." "Fast." "Nobody knew." In analytical, technical, clinical, and financial registers this reads as LinkedIn copy and costs more credibility than the monotony it replaced. Variance must come from clause structure and information density, not typographic drama.

**Second failure mode:** hitting the variance target while leaving every sentence the same *shape* (subject, verb, object, trailing prepositional phrase). The ear detects shape even when the metric is satisfied. Check shapes, not just lengths.

---

## End-stress: the 2-3-1 order

Roy Peter Clark's emphasis architecture. The most emphatic element goes at the end, the second most emphatic at the beginning, the least emphatic in the middle.

**Procedure, for claim-bearing sentences only:**
1. List the sentence's components. Rank them 1 (most emphatic), 2, 3.
2. Rebuild in the order 2, 3, 1.
3. Never end on a hedge, an attribution, or a date, unless the date is the point.
4. Apply at paragraph and section scale too. The last line of a section is the loudest position in the piece after the opening.

**Example (incident report).** Before: "Latency rose to 4.2 seconds at the p99 during the migration window, based on the Grafana export." After: "Based on the Grafana export, p99 latency during the migration window rose to 4.2 seconds." The attribution moves off the terminal slot; the number lands last.

**Example (biography).** Before: "She resigned on 12 June, according to the letter in the college archive." After: "The letter in the college archive is dated 12 June. She resigned that day."

**Failure mode: emphasis everywhere.** Applied to every sentence, 2-3-1 turns the prose into a sequence of punchlines and the reader stops registering any of them. Landings exist only against flat ground. Reserve the move for claim-bearing sentences and let connective sentences be deliberately unemphatic. Secondary failure: contorting syntax to force a word into the terminal slot, which produces the periodic sentence as mannerism.

---

## Right-branching default

Begin sentences with subject and verb. Make meaning early. Let qualification branch to the right.

- Left-branching (harder): "Because the 2019 revision changed how the deductible was indexed, and because indexation lagged inflation by two quarters, out-of-pocket costs rose."
- Right-branching (default): "Out-of-pocket costs rose, because the 2019 revision indexed the deductible to a lag that trailed inflation by two quarters."

Exception: use left-branching deliberately when the condition genuinely governs whether the claim holds at all, and the reader must not encounter the claim unconditioned. In HIGH risk class this exception is common and legitimate.

---

## Terminal emphasis check, per paragraph

For each paragraph's final sentence, ask whether the final word is the most consequential one available. Move prepositional tails, attributions, dates, and citation parentheticals off the end. Then ask the harder question: does this paragraph end on a fact or an image, or on a pull-quote-shaped generalization? The second is a closure ritual and gets cut.

---

## Pace modulation at the point of complexity

Clark's counterintuitive rule, and the one an LLM most reliably inverts.

1. Mark the two or three hardest passages: where a new mechanism, a counterintuitive result, or a chain of inference is introduced.
2. At each, cut average sentence length by roughly half. Break paragraphs more often. Replace every technical term you can with a plain one, and define the ones you cannot, once, at first use.
3. One new idea per sentence in these passages. If a sentence carries two, split it.
4. Immediately after the hard passage, place a concrete instance of the thing just explained, so the reader can check their own comprehension.
5. Over familiar ground, lengthen and compress. Speed is the reward for a reader who already knows.
6. Do not place a reward, a striking fact, or a set-piece image inside the hardest passage. Competition for attention destroys both.

**Failure mode: the elaboration reflex.** Sensing reader difficulty, the agent adds more, longer, and more qualified sentences, which compounds the load. Recognizable by paragraphs that grow longest exactly where the argument is hardest. Secondary failure: over-simplifying into falsity. Pace modulation licenses shorter sentences, never weaker claims.

---

## Making numbers land

Run per data-carrying paragraph.

1. **Budget:** one number per sentence, at most three per paragraph, in prose passages. Everything else goes to a table, a chart, or a footnote.
2. **Round hard in prose:** 105% becomes "doubled"; 33% becomes "one in three"; $1.043bn becomes "about a billion." Keep exact figures only where the precision is the claim.
3. **Check each rounding against the claim.** "About a billion" is an error when the difference between $1.04bn and $1.4bn is the whole argument. Rounding away a material distinction trades a stall for a falsehood.
4. **Comparison on the same screen:** an earlier year, another place, a competitor, or a physical referent the reader already owns.
5. **Human scale where possible:** per person, per day, per household, as a multiple of something familiar.
6. **Direction before magnitude:** say it doubled, then say from what.
7. **Never open a paragraph on a number the reader has no frame for.** Build the frame, then land the number.
8. **Strip bureaucratic number-words:** revenue to income, expenditures to spending, utilization to use, headcount to staff, where the plain word is accurate.

**Failure mode: the stat wall.** In data-rich domains the agent packs five figures and three percentages into one paragraph to demonstrate rigor. The eye slides off, and the argument is lost exactly where the evidence was strongest.

**Interaction with the claim-strength invariant:** rounding is a strength edit. "Roughly 40%" surviving as "40%" is a violation. Log every rounding in the ledger.

---

## Transitions: chain or cut, do not signpost

Two legitimate mechanisms.

1. **Hard cut.** End a unit on its strongest element; begin the next in a new place or time with a concrete anchor. No bridge sentence.
2. **Chaining.** Repeat a key word, image, or number from the end of the previous unit near the start of the next, in a *changed* sense. The repetition is the bridge; the change of sense is the argument. Repeating without changing sense produces echo, not movement.

**Banned mush layer:** "Meanwhile", "It is also worth considering", "Turning now to", "With that in mind", "Building on this", "First... Second... Finally..." as a roadmap.

**Allowed and useful:** time and place markers that carry information. "Three months later." "By the following spring." "Back at the Tualatin plant."

**Deletion test:** strip every transition sentence, re-read, restore only those whose absence caused real disorientation. Typically fewer than a third survive. Do not summarize the previous section after a break.

**Failure mode: the roadmap.** Telegraphing the outline ("First we examine supply, then demand, then pricing") makes the structure fully visible, and once readers can see the skeleton they navigate instead of reading.

---

## Reporting the diagnostics

The run report carries the numbers, the config, and the provenance note. Format:

```
RHYTHM DIAGNOSTICS (derived defaults, not published Hart figures)
  sentences: 214
  mean length: 21.4 words   (config target 15-20)
  sd: 6.1                   (config min 7)
  sentences < 8 words: 3    (config: >= 1 per 150 words, i.e. >= 12 expected)
  sentences > 45 words: 4   (2 have a stated structural reason)
  paragraph-opener repetition: 41% open with a subordinate clause
  READ AS: the draft subordinates heavily and lands rarely.
  ACTION TAKEN: split 9 long sentences at main-clause boundaries; merged 2 pairs
                (neither in the clarity split log). No fragments added.
```

Report the reading, the action, and what you declined to do. A diagnostics block with no "declined" line usually means the metric drove the prose.

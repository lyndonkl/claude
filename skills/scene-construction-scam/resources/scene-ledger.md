# The Scene Provenance Ledger

Build the ledger before any prose. The ledger, not the corpus, is what a scene is allowed to be built on. A scene slot that cannot be filled from the ledger produces a gap entry, never prose.

**Any missing required field BLOCKS the build of that scene.** Blocking is the normal case, not an exception. Real material always has holes; a run with zero blocked candidates is a red flag.

## Schema

| Field | Required | Content | Common defect |
|-------|----------|---------|---------------|
| `scene_id` | yes | Stable handle the draft cites | — |
| `date_place` | yes | Exact as the source carries it | Implying finer precision than the source. A source that says "March 1978" does not license "early March" |
| `actors` | yes | Named real people, or named systems | Composites; the unnamed engineer/trader/customer who exists to voice the thesis |
| `setting_specifics` | yes | Two or more recorded physical or observable conditions of the place | Weather, light, and mood written because that is what scenes look like |
| `system_state` | if protagonist is a system | Observable state at that moment: price, queue depth, latency, inventory, yield, error rate | A want, a belief, or a decision in this field |
| `action_sequence` | yes | Three or more ordered observable events, each with its own pointer | A state of affairs recorded as an action |
| `pointers` | yes | External artifacts only: page, section, timestamp, line number, table cell, commit hash, URL with retrieval date | "The 10-K" is not a pointer. "10-K FY2023 p.47, risk factors" is |
| `interior_states` | yes if any appear | Per claim, a class: A / B / C / D (see below) | Class D present |
| `drift_proportion` | yes | Typical of the period, or atypical? Plus the flag text that will appear on the page | Scene chosen because it was vivid, unflagged |
| `subtraction_log` | yes | What was cut from this moment; whether the remainder implies a different frequency or magnitude than the record | Cuts reviewed one at a time instead of as a set |
| `contested` | yes | Any conflicting source values, both retained | Silent resolution to the better-sounding value |
| `disposition` | yes | built / demoted / research request / declared absence / cut | "Drafted and flagged", which is not a disposition |

## Interior-state classes

Applies to any claim about a thought, feeling, intention, belief, expectation, or motive.

| Class | Basis | License in prose |
|-------|-------|------------------|
| **A** | The person stated this about that moment | Render as close third. No in-line hedge. Source in notes |
| **B** | Contemporaneous document: email, memo, log, diary, filing, transcript | Render as close third. The document should be visible somewhere nearby in the text |
| **C** | Behavioral inference from an observed or recorded action | Render the action only, or mark the inference in the prose: "which suggests", "he later described it as" |
| **D** | No basis | **Refuse.** Delete, or convert to the action |

A nonzero D-count blocks the build. There is a matching over-correction rule: class A and B material must **not** be hedged. Hedging every sourced thought destroys close third and makes the piece read as evasive. The hedge belongs to class C alone.

For systems, the equivalent of interior state is imputed institutional intent. Same gate: a firm "expected" something only if a filing, minute, transcript, or quoted executive says so.

## Composites and aggregates

**Composites are prohibited, categorically.** Never merge two or more real people, firms, incidents, shifts, or datasets into one entity presented as singular. Not for privacy. Not for concision. Not for narrative economy. Not because the section needs one clean example.

If privacy requires it, anonymize ("a senior engineer, who asked not to be named"). Never fuse. Pseudonyms are themselves a deviation requiring disclosure.

**Aggregates are permitted, under constraint.** Analytical domains legitimately need the representative firm, the median user, the typical trade. The rule is not "no aggregates". The rule is that an aggregate may never acquire the properties of an individual.

An aggregate must be labeled at first use and constructed transparently: "a representative 200mm fab", "the median advertiser in this cohort", "an aggregate computed across the twelve incidents in the dataset".

**Never call an aggregate a "composite."** That word is reserved for the prohibited operation — fusing several real entities into one presented as singular. Reusing it for a permitted aggregate re-licenses the thing the bright line forbids, and the drafting agent will take the licence.

An aggregate may **not**:
- take a proper name
- appear in a scene
- be given dialogue
- be given interiority or intent
- be given a specific date or location
- be described with sensory detail

Every property attributed to the aggregate must hold for the aggregate as computed, not be a union of properties drawn from different members. A median firm does not have the largest member's revenue and the smallest member's headcount.

The failure mode has a shape. The aggregate is honestly labeled at first use. Then over ten pages it accretes a founding date, a temperament, a decisive meeting. Narrative wants a character, and the aggregate is standing in the character slot. By then the disclosure is thirty paragraphs back and the reader is reading fiction. Carry a persistent marker on aggregates and treat any scene-level verb attached to one as a hard defect.

If the piece needs a single vivid exemplar, find a real one and name it, or accept the aggregate's flatness. Refuse the third option.

## Blocking checklist

Run last. Any line that fires blocks the scene.

- [ ] Every required ledger field is filled for this scene.
- [ ] Every pointer resolves to an external artifact. No pointer resolves into this pipeline's own notes, summaries, or earlier drafts.
- [ ] No SCAM slot was filled by inference.
- [ ] Gate 4 passed: this passage could not have been written without the source material.
- [ ] Interior-state D-count is zero. Class A and B material is unhedged; class C is marked in the prose.
- [ ] No dialogue in quotation marks that is not verbatim from a recording, transcript, or contemporaneous written record. Remembered speech is paraphrased and marked as remembered.
- [ ] No invented sensory material: weather, light, sound, clothing, gesture, room contents, physical sensation.
- [ ] No number the sources do not contain, including a qualitative quantifier converted to a numeral ("several" to "six") and any figure exceeding the source's precision.
- [ ] No composite person, firm, incident, or scene presented as singular. No aggregate carrying a name, a scene, dialogue, intent, a date, or sensory detail.
- [ ] No duration compressed or expanded; no separate events merged into one moment.
- [ ] No actor shown acting on information that post-dates their action.
- [ ] Documented source conflicts are both in the text, not silently resolved.
- [ ] The drift-and-proportion flag is on the page for any atypical scene.
- [ ] The subtraction log was reviewed as a set, and the remainder does not imply a different frequency, magnitude, or balance than the full record.
- [ ] No system holds a want, a belief, or a decision. Personification appears at most once, explicitly.
- [ ] Transition and summary sentences carry pointers too. No unsourced abstract-state assertion ("by then the pressure was impossible to ignore").
- [ ] The word "verified" appears nowhere. Facts were sourced, not checked.
- [ ] The higher-truth rationalization was not used. "This is clearly what happened", "the reader will understand", "it is emotionally true", "it is a reasonable inference" are all the same move under different wording.

## Generating the note on sources

Generate the disclosure **from** the deviation log after the fact. Never write it in advance.

Boilerplate ("some events have been compressed, some dialogue recreated") is worse than nothing in an automated pipeline. It is cheap to emit, it pre-authorizes the deviations, and it makes the reader believe a human weighed a trade-off that no one weighed. Disclosure is not a currency that buys deviations.

A generated note names specifics:

> Scenes are built from the berth logs, gate transaction files, and PMSA monthly tables cited in the endnotes. Times are as logged and are not adjusted for time zone drift in the 2021 records. No dialogue appears; no participant was interviewed. The 22-day dwell in section 3 is the longest in the sample, not a typical case. Discharge records for 11-13 May are missing from the terminal file and no substitute was found.

Every clause in that note traces to a ledger field. If a clause cannot be traced to one, it does not belong in the note.

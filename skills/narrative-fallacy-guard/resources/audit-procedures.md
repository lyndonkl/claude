# Audit Procedures

The six audits in full, with the tables they produce and worked bad-and-good rewrites. Domains used throughout: incident and outage post-mortems, biography, supply chain, protocol and standards history, lab science, and machine-learning research writeups.

Every audit here ends in a label, a rewrite, or a disclosure sentence. None of them ends in a deletion. That rule is not a softening of the audits. It is what keeps them usable: a delete rule applied to the predictability test removes every rich explanation ever written, and the result is a chronicle that informs nobody.

## Table of contents

- [1. Source ledger and the primary/secondary downgrade](#1-source-ledger-and-the-primarysecondary-downgrade)
- [2. Retrospective slot audit](#2-retrospective-slot-audit)
- [3. Outcome-blind rewrite](#3-outcome-blind-rewrite)
- [4. Inevitability audit and the overshoot check](#4-inevitability-audit-and-the-overshoot-check)
- [5. Graveyard pass](#5-graveyard-pass)
- [6. Counterfactual admissibility gate](#6-counterfactual-admissibility-gate)
- [7. Proportion audit and omission check](#7-proportion-audit-and-omission-check)
- [8. Causal tier tags and their permitted verbs](#8-causal-tier-tags-and-their-permitted-verbs)
- [9. Domain-dominant failure modes](#9-domain-dominant-failure-modes)

---

## 1. Source ledger and the primary/secondary downgrade

A date alone is not a clean standard. Contemporaneous sources are produced by interested parties. They survive selectively. In business and technology material they are dominated by promotional copy and by analyst commentary already carrying an in-progress halo. An agent that treats any dated pre-outcome source as clean evidence has moved the bias one step upstream rather than removing it.

Ledger fields, one row per source:

| Field | What goes in it |
|---|---|
| ID | Short handle used in the slot table and the tag map |
| PUB DATE | When the source was published or written |
| EVENT DATE | The period it describes |
| CLASS | PRIMARY (contemporaneous record, artifact, log, memo, filing) or SECONDARY (later account) |
| INTEREST | Who paid, who benefits, what is being sold or defended |
| SAMPLED | Whether this view is representative of a range you actually read, or a single voice you picked |

Downgrade rules:

- No claim may be tagged L1 MECHANISM on the strength of a secondary retrospective account alone. A later book asserting that a memo caused a decision is evidence about the book. Downgrade to L3 SEQUENCE or L5 CONJECTURE until the memo is in hand.
- A single quoted booster or a single quoted critic does not discharge the outcome-blind rewrite. Say whether the retained characterisation is representative of a sampled range.
- If the corpus is entirely secondary, say so in the body, once, early. The halo, the teleology, and the shape have already been applied upstream. You will otherwise re-derive them faithfully while passing every check.

Selection rule sentence. Write it literally, before anything else:

- "This corpus consists of the incident reviews that were written up, which is the subset where someone had time after the fact."
- "This corpus consists of the suppliers still trading in 2024, which excludes everyone the same shock removed."
- "This corpus consists of the researchers who agreed to be interviewed."

That sentence feeds the graveyard pass in section 5. If you cannot write it, you do not know what your evidence is a sample of.

---

## 2. Retrospective slot audit

A structural slot is a claim that a moment mattered. The audit separates "mattered to the people in it" from "matters because we know the ending".

Produce this table. It ships with the deliverable; it is not scratch.

| Slot | Event | (a) event date | (b) earliest source treating it as significant | (c) outcome date | (d) source cited | Tag |
|---|---|---|---|---|---|---|
| Inciting incident | ... | ... | ... | ... | ... | RETROSPECTIVE-ONLY / CONTEMPORANEOUS-PARTIAL / CONTEMPORANEOUS |

Tag rule: if (b) is after (c), the slot is RETROSPECTIVE-ONLY. If (b) sits between the event and the outcome, it is CONTEMPORANEOUS-PARTIAL. If a source dated at or before the event names it as consequential, it is CONTEMPORANEOUS.

Substitution test, run on every RETROSPECTIVE-ONLY slot: name two other events in the same window that a narrator with a different ending would have picked. If you cannot name two, you have not searched the corpus.

Worked example, supply chain. The piece opens on a 2019 decision to single-source a component, because a 2022 shortage made that decision famous. Earliest source treating the 2019 decision as significant: a 2022 trade-press retrospective. That is after the outcome date. Tag RETROSPECTIVE-ONLY. Substitution test produces two rivals: the 2018 qualification of a second supplier that was then never ordered from, and the 2020 decision to cut safety stock by a third. A narrator whose story ended in a successful cost programme would have opened on either.

Required output once tagged: either downgrade the verb, or add one body sentence. "Nothing in the 2019 record treats the single-source decision as a risk event; the first document that does is dated three months after the shortage began."

The failure mode to avoid is contemporaneity fetish. Some genuinely causal events are invisible to everyone present: a slow demographic shift, accumulating technical debt, a definitional drift in a metric, a mutation. Mechanically demoting every RETROSPECTIVE-ONLY slot over-weights whatever happened to be loud at the time. That is salience bias wearing the costume of rigor. The tag is a disclosure requirement.

### Instrument check for quantitative slots

When the inciting incident is a discontinuity in a series, ask one question before accepting it: did the world change, or did the instrument change?

Enumerate the instrument candidates: definitional revisions, coverage or sampling changes, methodology restatements, reporting-lag artifacts, entity or boundary changes (mergers, re-classification, redistricting), and collection-platform changes.

Reject any candidate whose date coincides with a known instrument change, unless the effect survives re-baselining on a consistent definition. If you cannot re-baseline, the instrument change is the story and must be narrated as such.

Bad: "Defect reports tripled in Q3, and the team never recovered." Good: "Defect reports tripled in Q3. The intake form changed on 1 July, and the new form auto-filed a ticket for every crash the old one had batched. On a consistent definition the underlying rate rose by about a fifth."

Record the rejected candidates and the reason. That list is the defence against the charge of cherry-picking a start date.

---

## 3. Outcome-blind rewrite

Reconstruct every characterisation using only the information set available at the decision date. This is the direct countermeasure to the halo effect and to outcome bias, which replicates at large effect sizes even in subjects who state that outcomes should not affect their evaluation of decisions.

Procedure:

1. Extract every evaluative adjective and dispositional noun applied to any actor: visionary, reckless, disciplined, arrogant, prescient, complacent, focused, bloated, brilliant, naive.
2. For each, look for a dated source predating the outcome that used that characterisation. Found: keep it and attribute it inline with its date. Not found: delete the adjective and replace it with three specifics. The ACTION taken. The INFORMATION SET available at that date. The ALTERNATIVES visibly on the table.
3. FLIP TEST. Rewrite the sentence assuming the opposite outcome occurred. If you would obviously not have written it that way, the outcome is supplying the judgment, not the evidence.
4. SEPARATION TEST. State decision quality and outcome quality in different sentences. The outcome sentence may not supply the adjective for the decision sentence.
5. QUOTE-LAUNDERING CHECK. Is the surviving dated characterisation representative of a range you sampled, or one cherry-picked voice? Say which.
6. SYSTEM PASS. Apply all of the above to non-person protagonists.

Worked rewrites:

- Biography. Bad: "Her reckless 1998 expansion drained the reserves." Good: "In 1998 she committed the reserves to a second site. The company had two quarters of cash, one signed anchor tenant, and a competing proposal to lease rather than build. The site did not fill for four years." (Separation test satisfied: the decision sentence and the outcome sentence are distinct, and the outcome does not supply the adjective.)
- Post-mortem. Bad: "The on-call engineer complacently ignored the alert." Good: "The alert fired at 02:14 alongside eleven others from the same dependency. The runbook for that alert had been marked 'known noisy' in March. She acknowledged it and continued on the incident she was already working."
- ML writeup. Bad: "The team made the prescient choice of a larger context window." Good: "The team chose a 4k context against a 2k baseline. Two of the three benchmarks they were tracking were insensitive to context length at the time, and the compute cost was roughly double. The internal design note gives the reason as headroom for a planned retrieval feature that was later cancelled."
- System halo. Bad: "An efficient market consolidated around two clearing venues." Good: "Two clearing venues held ninety per cent of volume by 2011. Four others had exited; three of the four cited the same capital rule. Whether the surviving two were the lowest-cost providers is not established by the record."

The failure mode is neutrality collapse. Strip every adjective and you produce prose nobody finishes, and unread accurate work informs nobody. The substitution must be vivid specifics ("two quarters of cash and one signed anchor tenant"), never a bureaucratic placeholder ("the decision was taken in a constrained information environment"). Placeholders fail the pass as surely as adjectives do.

Second failure: the flip test is valid only for sentences about decisions. Applied to sentences about facts it produces nonsense.

---

## 4. Inevitability audit and the overshoot check

Run over every causal sentence in the draft. A causal sentence is any sentence containing: because, so, led to, drove, forced, triggered, resulted in, as a result, which is why, meant that, set the stage for, inevitably, was bound to, the seeds of, paved the way.

Also scan the places the causal claim hides when the connectives are policed: figure captions, chart annotations, section headings, pull-quotes, chapter titles, scene cuts, and paragraph breaks between two events. A juxtaposition is a causal claim made without words.

For each causal sentence:

1. What did the actors at the time believe would happen? Cite a contemporaneous forecast, plan, budget, or projection.
2. Name one live alternative that was genuinely available, and that someone in the material was advocating or pursuing at that moment.
3. If no live alternative exists, the outcome may genuinely have been overdetermined. Say so explicitly and give the binding reason: a physical limit, an accounting identity, a contractual obligation, a regulatory deadline. Do not leave overdetermination implied.
4. Enforce the banned list. Replace with contingency language: "happened to", "persisted given", "survived the conditions of", "nobody on the shift expected", "of the paths then on the table, this was the one funded".

Then insert the FORECAST-VS-OUTCOME BEAT. Find one documented prediction from inside the material that turned out wrong, and give the reasoning that made it reasonable at the time. One such beat does more anti-inevitability work than any quantity of hedging, because it lets the reader feel the uncertainty rather than being told about it.

Examples of the beat:

- Protocol history: the 1996 working-group minutes in which three of five participants expect the competing encoding to win, and the throughput numbers they were looking at.
- Lab science: the grant renewal that budgeted two years for a result that took nine, and the pilot data that made two years look generous.
- Supply chain: the demand plan that assumed a 4% decline, signed by people with the order book in front of them.

### The overshoot check

Does the draft contain at least one confidently asserted "X caused Y"? If not, the brake has become hedge fog, which is abdication rather than honesty.

The correct output of this audit is a small number of confidently asserted causal claims, each carrying its counterfactual, and not a large number of hedged ones. Count them. Zero is a failure of this audit, not a success of it.

### Anachronism flag

Where a category, a metric, or a moral frame used in the text did not exist at the time described, say so in the body. "The 1974 filings contain no figure comparable to what is now reported as scope-2 emissions; the estimate below is reconstructed and is not what anyone measured then."

Flag the anachronism. Do not adjudicate whether present-day categories may be applied to past actors. That dispute is live and politically contested, and it is not this skill's business. The narrow operation is checkable; the larger argument is not.

---

## 5. Graveyard pass

Every "X did A and won" claim implies a population. The pass forces a search for the non-survivors who also did A, or a declaration that the base rate is unknown.

1. State the selection rule from section 1.
2. For every success attribution, search for at least two entities that took the same action and did not get the same outcome.
3. Report one of three results in the body text.
   - Counterexamples found: name them and weaken the claim.
   - Counterexamples searched for and not found: state the search and the finding. This strengthens the claim, and is worth saying for that reason.
   - Population is n=1 or unobservable: write "the base rate for this action is unknown".
4. Inversion, for any "the lesson is" inference: what would the record look like if the decisive factor were present only in the cases that did not survive, and therefore are not in your corpus?
5. Never let an implied prescription stand on a corpus whose selection rule is survival.

Worked example, ML writeup. Claim: "the win came from curriculum ordering of the training data." Graveyard search finds two contemporaneous groups that used the same ordering scheme and reported no gain, and one that reported a loss. Required text: "Two other groups applied the same ordering and reported no improvement; a third reported a small regression. Whatever the ordering contributed here, it is not sufficient on its own."

Worked example, biography. The subject's habit of writing to strangers is credited with the career break. The graveyard is unobservable: nobody records the letters that were never answered. Required text: "the base rate for this is unknown, and the people whose letters went unanswered did not leave archives."

Failure mode: false symmetry. Some events genuinely have no comparison class. An agent required to produce counterexamples will manufacture weak analogies and present them as base rates, which is a fresh distortion dressed as a correction. Result three must be a first-class, non-embarrassing output.

### Cumulative-advantage apportionment

Where the outcome involves observable prior adoption influencing later adoption (market share, standards, citations, downloads, funding, hiring, platform effects), add an apportionment sentence.

The experimental evidence licenses only the weak claim: the best rarely does badly and the worst rarely does well, and between those bounds many results are possible. So establish the quality bounds the record supports. Was the winner top-tier on the merits, or merely not bottom-tier? Name at least one near-peer that was comparable and did not win, and say what differed. If the difference is timing, an early endorsement, a distribution accident, or a rival's unrelated stumble, that is path, not property.

Apportionment sentence: "On the merits it was among several credible options; its win owed materially to shipping inside a widely installed runtime."

Ban the retro-justification form: any sentence of the shape "X won because it was [attribute]" where the same attribute was present in a loser.

Failure mode: luck nihilism. Applied everywhere, this concludes that nothing is explicable and produces a piece that shrugs. The check must produce an apportionment, not a dismissal. It is also simply wrong in domains without social feedback: a materials failure analysis, a contract dispute, a compiler bug.

---

## 6. Counterfactual admissibility gate

A contingency node marks a decision point where the outcome was genuinely open. All six tests must pass, or the node is rejected.

| Test | Passes | Fails |
|---|---|---|
| CLARITY | "If the second supplier had been qualified before the Q3 order" | "If things had gone differently" |
| COTENABILITY | You can list what else would have to be true: the tooling, the audit, the lead time | You cannot enumerate the connecting principles |
| MINIMAL REWRITE | Exactly one thing changes | Requires altering a second independent fact, which describes a different world |
| HISTORICAL CONSISTENCY | The antecedent was physically, technically, and institutionally possible at that date, and someone proposed it | The antecedent needs a capability that did not exist |
| THEORETICAL CONSISTENCY | The link uses a mechanism already established in the piece with L1 or L2 evidence | The link is asserted only here |
| STATISTICAL CONSISTENCY | Where base rates exist, the counterfactual outcome falls inside them | The counterfactual outcome is an outlier nobody achieved |

Rendering rules:

- Bounded element only: a bracketed passage, a sidebar, a marginal note, a differently-styled paragraph. Never a dramatised scene with sensory detail. A dramatised counterfactual acquires the vividness of the documented events, and readers will not retain which was which.
- Density cap: at most one contingency node per major structural section. Contingency nodes are punctuation, not texture.
- Inevitability disclaimer at the node: state what the actors at that moment believed the odds to be, if the record says.

Failure modes. First, the counterfactual as consolation: a decorative "what if" so implausible that the actual path looks overdetermined by comparison, which strengthens the inevitability it was meant to break. Second, unbounded cotenability: "if the firm had shipped a competing product in 1988" silently requires a different firm, at which point the counterfactual is about a fictional company. Minimal rewrite is the load-bearing constraint and the one most often violated.

Admitted example, outage post-mortem: "[Two config lines: the pool size and the retry backoff. Both were in a pending change request opened eight days earlier and unreviewed. With either merged, the saturation curve stays under the ceiling for the observed traffic. The reviewer queue was six deep that week.]"

Rejected example: "Had the platform team adopted a service mesh in 2019, the cascade could not have propagated." Fails minimal rewrite (a mesh adoption implies a different platform team, budget, and migration), and fails historical consistency unless someone actually proposed it at that date.

---

## 7. Proportion audit and omission check

These are the expensive checks. They are the ones schedule pressure removes. They are also the only checks that catch the failure where every sentence is true and the piece as a whole misrepresents the drift and proportion of events.

Implementing only the cheap per-sentence checks produces work more dangerous than unchecked work, because it carries verifiable citations and reads as audited.

### Proportion table

| Claim | Words spent | Evidence tier (L1-L5) | Causal weight (filled BEFORE the arc was chosen) | Flag | Justification |
|---|---|---|---|---|---|

Flag both asymmetries:

- Top quintile by words, bottom quintile by evidence tier. These are the colourful anecdotes carrying the reader's belief.
- Top quintile by causal weight, bottom quintile by words. These are the boring drivers the arc suppressed. Usually a price change, a regulatory filing, a base rate, a demographic trend, a compiler flag, a contract renewal date.

Every flag needs a written justification. "This anecdote gets 800 words because it is the only surviving first-hand account of the mechanism" is legitimate. No justification means rebalance.

Do not equalise mechanically. Redistributing word count produces something with the rhythm of a spreadsheet, and readability collapse is itself an accuracy failure. The audit terminates in a justification, not in an automatic edit.

Fill the causal-weight column before the arc is chosen. Filled afterwards, it inherits the same halo the audit exists to catch.

### Omission check

List every corpus item that appears nowhere in the draft. For each, state why. Any item that would weaken the spine and was omitted without a stated reason is a cherry-pick, and it goes back in.

Add the forgotten-population question for quantitative material: who is not in this dataset who should be, and would including them change the sign?

Final gate for both checks: a reader who disagrees with your conclusion, can they find the strongest evidence against you inside your piece? If not, you have obfuscated, whatever you intended.

The mirror failure is defensive over-disclosure. Answering an audit with twelve caveats and four hedging paragraphs buries the damaging material among weak supportive material, which is itself a recognised deception pattern. Volume is not integrity.

---

## 8. Causal tier tags and their permitted verbs

Tag every causal assertion before writing the sentence. The tag governs the verb.

| Tag | What it means | Permitted verbs | Banned |
|---|---|---|---|
| L1 MECHANISM | The linking step itself is documented: a memo, a contract, a physical process, an accounting identity, a commit, a transcript | caused, forced, triggered, led to, because, resulted in | — |
| L2 CORRELATION | Quantitative co-movement documented, mechanism absent | moved with, tracked, coincided with, accompanied | because, drove, forced |
| L3 SEQUENCE | Only temporal order established | then, afterwards, in the following quarter, subsequently | every causal connective |
| L4 ADJACENCY | Co-present, no link established | must be separated in the text, or carry the inline disclaimer "the two were concurrent; no link is documented" | all |
| L5 CONJECTURE | The author's inference | must carry an explicit marker: "the most plausible reading is", "no source says why, but" | may never occupy a climax, revelation, or thesis sentence |

Requirements per tier: an L1 tag needs a source for the LINK, not merely for the two endpoints. An L2 claim must name at least one other thing that moved the same way. An L3 claim needs both dates. For any L1 claim, state the DELAY: causes and effects separated by months read as unrelated, and effects that arrive instantly are usually not caused by the thing that just happened.

Two failures to watch:

- Because-laundering. When the connectives are policed, the causal claim moves where the check cannot see it. It hides in a metaphor ("the dam broke"), in a scene cut, in a chapter title, in a chart annotation, or in a quoted source who asserts the causality on the author's behalf.
- Type laundering. A correlation is introduced with hedges early, then referred back to later as established mechanism: "as we saw, the fee change drove the migration." Check every back-reference against the type of the original claim. A back-reference may not upgrade the tier. This is fully mechanical to detect and it is the most common integrity failure in long analytical pieces.

Rendering: L1 and L4/L5 must be distinguishable to the reader without opening the notes. A glyph, a class, a colour, an inline parenthetical. If the reader cannot see the difference, the tagging did nothing.

---

## 9. Domain-dominant failure modes

One uniform checklist misses the locally dominant error. Run all the audits; weight these.

| Domain | Dominant failure | Weight these audits |
|---|---|---|
| Market, industry, and technology history | Retrospective inevitability; winner's attributes explaining a draw from a distribution | Slot audit, inevitability audit, cumulative-advantage apportionment |
| Product and incident post-mortems | Hindsight plus individual blame | Outcome-blind rewrite, counterfactual gate, source ledger |
| Biography | Systemic framing used to excuse the subject, or halo applied to everything before the outcome | Outcome-blind rewrite, agency reading, graveyard pass |
| Supply chain and operations | A cherry-picked traversing unit presented as typical | Proportion audit, omission check, instrument check |
| Lab and field science | Omitted failed experiments; the retrospective coherence of a messy search | Omission check, forecast-vs-outcome beat, proportion audit |
| ML research writeups | Correlation laundered into mechanism; intentional verbs applied to models | Causal tier tags, graveyard pass, type-laundering back-reference check |
| Standards and protocol history | "Matured into"; the survivor's design credited for the survivor's distribution | Inevitability audit, apportionment sentence, graveyard pass |
| Policy and regulatory chronologies | Law-office history: facts selected so the past resolves into the present's shape | Slot audit, omission check, anachronism flag |

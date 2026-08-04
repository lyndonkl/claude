# The Claim-Strength Ledger

The guard that keeps the force and brevity passes from becoming an overclaiming machine.

Hart's force rules were written for newspaper prose about events that happened, where a stronger verb is almost always a truer verb because the reporter watched the thing happen. Analytical prose is different. Its verbs carry epistemic weight, and "energy" and "calibration" pull in opposite directions. An unsupervised force pass trades the second for the first every time.

---

## The strength ladder

| Level | Name | Markers | Example |
|---|---|---|---|
| S5 | Asserted fact | dated, sourced, no modal | "Fab 14 shut on 4 March 2021." |
| S4 | Quantified finding, conditions stated | a number plus a scope | "In this cohort, 30-day mortality fell 8 points." |
| S3 | Association or co-occurrence | associated with, coincided with, followed, correlates with | "The tariff coincided with a 15% fall in imports." |
| S2 | Inference or suggestion | suggests, is consistent with, indicates, appears | "The ablation suggests the tokenizer caused the regression." |
| S1 | Possibility or dispute | may, might, could, some argue, alleged, preliminary | "Reserves may be understated." |

S-level is a property of the **evidence**, not of the sentence. The sentence's job is to report it. Editing changes sentences; it never changes evidence; therefore editing may never change S-level.

---

## Ledger format

Build it before Pass 2. One row per claim-carrying sentence.

| id | sentence (before) | S | strength markers | source | pass | S after | verdict |
|---|---|---|---|---|---|---|---|
| 12 | The rollout was associated with a 12% drop in checkout errors. | S3 | "was associated with" | dashboard export 2024-05 | Force | S3 | PRESERVED |
| 19 | The assay suggests the compound binds ACE2. | S2 | "suggests" | Fig 3, internal report | Force | S5 | **VIOLATION, reverted** |
| 27 | In this sample, churn rose roughly 4 points. | S4 | "in this sample", "roughly" | cohort file | Brevity | S5 | **VIOLATION, reverted** |

The ledger diff goes in the run report. Reverts are reported, not hidden. In HIGH risk class (medical, legal, financial, safety, scientific), an unresolved violation blocks delivery.

---

## Verb-swap danger table

The left column is what a force pass reaches for. The right column is what it costs.

| From | To | Delta | Allowed? |
|---|---|---|---|
| was associated with | drove, caused, produced | S3 to S5 | No |
| coincided with | triggered, set off | S3 to S5 | No |
| suggests, indicates | shows, proves, demonstrates, confirms | S2 to S5 | No |
| may, might | will, does | S1 to S5 | No |
| contributed to | caused | S3 to S5 | No |
| correlates with | predicts | S3 to S4 causal | No |
| declined 4% | collapsed, cratered, plunged | magnitude inflation inside S4 | No |
| rose 3 points | surged, exploded | magnitude inflation | No |
| one model estimates | the data show | S2 to S5 | No |
| reported that X | X | attribution deleted | No |
| was silenced (actor unknown) | an engineer silenced | actor invented | No |
| was reduced by the team | the team reduced | passive to active, actor named in material | **Yes** |
| there was a decline of 12% in errors | errors fell 12% | expletive killed, strength held | **Yes** |
| conducted an analysis of the logs | analyzed the logs | nominalization killed | **Yes** |
| the implementation resulted in a reduction | after the clinic adopted it, median time fell from 19 days to 11 | abstract subject replaced with sourced particular | **Yes** |

---

## Silent strength moves

Strength changes without any verb changing. Treat each of these deletions as a strength edit requiring a ledger check.

1. **Attribution dropped.** "According to the 2019 filing, reserves fell" to "Reserves fell."
2. **Scope dropped.** "In this cohort", "in this sample", "among firms with revenue over $50m", "in the 2018-2022 window."
3. **Date dropped.** "As of Q2 2023" removed from a claim about a moving quantity.
4. **Estimate marker dropped.** "approximately", "roughly", "estimated" removed from a number that was modeled, not measured.
5. **Units or basis dropped.** "12% year over year" to "12%."
6. **Plural evidence collapsed to a singular claim.** "Three of the five studies found" to "Studies found."
7. **Hedge moved from clause to nothing during a slop-audit hedge-stack reduction.**
8. **A range narrowed to its midpoint.** "$1.0bn to $1.4bn" to "about $1.2bn."

---

## Anti-overcorrection

The invariant is symmetric. Adding hedges to sourced facts is also a violation, and it is the failure mode of an agent that has been burned once.

- Bad: "The plant appears to have possibly closed in March" when the closure notice is in the filing.
- Good: "The plant closed in March."
- Bad: "Sources suggest she may have resigned on 12 June" when the resignation letter is dated 12 June.
- Good: "She resigned on 12 June."

Hedging sourced material reads as evasive and, in narrative passages, destroys close third-person rendering.

---

## Why List A and List B are different lists

Hart's parasite list is correct for literary journalism, where "somewhat" and "virtually" genuinely dilute. It is catastrophic on technical, medical, legal, and financial writing, where "approximately", "in this cohort", "under these assumptions", and "as of [date]" are the difference between a defensible and an indefensible claim. Applying one list to both kinds of prose is the single most common way this method damages analytical work.

**List A: cut on sight**
rather, somewhat, generally, virtually, pretty, slightly, a bit, a little, quite, very, really, actually, basically, essentially, in order to, the fact that, it should be noted, it is important to note, needless to say

**List B: protected, never auto-cut**
approximately, estimated, roughly, may, might, appears, suggests, is consistent with, in this sample, in this cohort, under these assumptions, as of [date], reported, alleged, preliminary

**The scope exception in detail.** Some List A words do real work in analytical prose by naming a base rate or a coverage fraction. Three moves are available, in order of preference:

1. Replace with the scope from the material. "Retail sales generally recover within two quarters" to "In seven of the nine postwar recessions, retail sales recovered within two quarters."
2. If the material does not supply the scope, keep the word and log a reporting gap.
3. Never simply delete, which converts a base-rate claim into a universal law.

The same applies to "typically", "in most cases", "tends to", and "on average" when they are the only thing standing between the sentence and a false universal.

---

## Worked ledger examples

**Clinical.** Before: "It was found in the trial that the intervention was associated with a reduction in 30-day readmissions of approximately 18%." S3, markers "was associated with", "approximately."
Force rewrite: "In the trial, 30-day readmissions fell about 18% in the intervention arm." Expletive gone, nominalization gone, "was found" gone. Association preserved by keeping the arm-scoped framing rather than making the intervention the grammatical subject of a transitive verb. S3, PRESERVED.
Rejected rewrite: "The intervention cut 30-day readmissions 18%." S5, causal, and the estimate marker is gone. Two violations in eight words.

**Supply chain.** Before: "There has been a significant deterioration in on-time delivery performance across the tier-two supplier base since the port closure." S3, marker "since."
Force rewrite: "On-time delivery from tier-two suppliers has fallen since the port closed, from 91% to 74%." S3 preserved, expletive killed, two nominalizations killed, and the number came from the material, not from the rewrite.
Rejected rewrite: "The port closure gutted tier-two delivery performance." Causal claim, unstated magnitude, and a verb that asserts an agent.

**Market history.** Before: "The 1907 panic is generally understood to have been arrested by Morgan's intervention." S2, markers "generally understood", "is ... to have been."
Force rewrite: "Historians credit Morgan's intervention with arresting the 1907 panic." S2 preserved, actor named, passive gone, and the belief-holder is now visible instead of implied.
Rejected rewrite: "Morgan's intervention arrested the 1907 panic." A live historiographical dispute rendered as settled fact.

**ML writeup, system protagonist.** Before: "The scheduler wants to keep queue depth low, so it decided to evict the long-running jobs." Personification asserting intent.
Rewrite: "The scheduler evicts jobs once queue depth passes 400. On 14 April it evicted the four longest-running jobs." State and rule, dated instance, no intent claimed.

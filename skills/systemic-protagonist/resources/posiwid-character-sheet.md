# The POSIWID Character Sheet

The system gets a character sheet the way a novelist gives one to a person. The fields are different: objective function, constraints, feedback loops, blind spots, and behaviour under stress.

Attribution note. POSIWID — "the purpose of a system is what it does" — is Stafford Beer's formulation. The working phrasing used here, that purposes are deduced by an observer from behaviour rather than from rhetoric or stated goals, is Donella Meadows in *Thinking in Systems*. Do not attribute the acronym to Meadows, and do not present either as a quoted rule you have not checked.

## Table of Contents
- [The eight fields, in order](#the-eight-fields-in-order)
- [The two-regime test](#the-two-regime-test)
- [Functionalist overfit and the residual field](#functionalist-overfit-and-the-residual-field)
- [Three filled examples](#three-filled-examples)
- [The reform-attempt ledger](#the-reform-attempt-ledger)
- [Character dimensioning: the system translation](#character-dimensioning-the-system-translation)
- [The stated-vs-revealed billboard](#the-stated-vs-revealed-billboard)

## The eight fields, in order

**Field 1 — Outcomes.** List every outcome the system reliably produced over the period covered. Outcomes, not intentions. Each carries a citation and a date. Five is the working minimum; fewer usually means the window is too short.

Do not list events. List outcomes that recurred. "The exchange halted on 6 May 2010" is an event. "Retail orders routed through the exchange were filled at worse prices than institutional orders in 11 of 12 quarters" is an outcome.

**Field 2 — The character sentence.** Ask what a designer would have had to be optimising for to produce exactly this outcome set. Write it as one sentence:

> This system reliably converts ___ into ___.

Examples across domains:
- A municipal permitting office: "converts applicant persistence into approvals, and applicant inexperience into indefinite delay."
- A package registry: "converts download counts into maintainer obligation, without converting either into maintainer income."
- A regional grid operator: "converts winter peak demand into fuel-cost pass-through, and converts transmission scarcity into siting decisions nobody voted on."

The sentence is the character. Everything downstream is evidence for it or against it.

**Field 3 — Constraints.** Physical, legal, capital, information, latency, headcount. Per constraint: what it is, what it binds, and where it is documented. An undocumented constraint is a hypothesis, and must be labelled as one.

**Field 4 — Feedback loops.** Per loop record three things: reinforcing or balancing, the quantity that closes the loop, and the delay. Delay is the field most often skipped and the one that most often explains why a piece feels wrong. Systems stories go wrong at the timescale: causes and effects separated by months read as unrelated, and effects that arrive instantly are usually not caused by the thing that just happened.

**Field 5 — Blind spots.** What does the system not measure, and therefore not respond to? This field is where the surprises in your piece live. A hospital that measures length of stay but not readmission. A CI pipeline that measures test pass rate but not flake rate. A port that measures container throughput but not dwell time on the chassis.

**Field 6 — Stated purpose.** Quoted verbatim from a real document: charter, prospectus, mission statement, README, standards RFC, launch post, enabling legislation. Paraphrase fails this field. You need the exact words because sentence 2 of the billboard quotes them.

**Field 7 — The gap.** One sentence naming the difference between Field 6 and Field 2. This is the dramatic engine.

If there is no gap — if the system does roughly what it says it does — emit `NO DRAMATIC ENGINE` with the evidence. That is a legitimate and under-written finding. The options are: choose a different subject, widen the time window until a regime change appears, or write it as explanation rather than narrative. Do not manufacture a gap by reading the stated purpose uncharitably.

**Field 8 — The residual.** Which outcomes does the revealed objective function FAIL to explain? At least one entry is mandatory. See below.

## The two-regime test

A revealed objective function inferred from a single episode is a description of that episode wearing a character trait's clothes.

Require behaviour in at least two distinct regimes:

| Domain | Regime A | Regime B |
|--------|----------|----------|
| Market or exchange | Rising liquidity | Stress or halt |
| Public agency | Funded, staffed | Budget cut, hiring freeze |
| Open-source project | Corporate sponsorship active | Sponsorship withdrawn |
| Supply chain | Slack capacity | Capacity binding |
| Hospital or clinic | Normal census | Surge |
| Codebase | Feature growth | Freeze or migration |

Procedure: state the character sentence, then show that it predicts observed behaviour in both regimes. If the system converts A into B during expansion but converts A into C under stress, you have two characters and must either narrow the period or make the regime switch itself the subject.

Result codes: `TWO-REGIME CONFIRMED` (cite both), `SINGLE REGIME — UNSUPPORTED` (go back to the material), `REGIME SPLIT` (the switch is your story).

## Functionalist overfit and the residual field

The sheet asks what a designer would have optimised for. That question quietly invites you to read every outcome as intended. A system that was merely incompetent, path-dependent, or unlucky then gets written as a coherent malign optimiser — which is a more satisfying story and a worse account.

Detection: if the character sentence explains 100% of the outcome list with zero residual, it is fitted noise.

Countermeasure, mandatory: Field 8 carries at least one outcome the objective function does not explain, and that outcome must appear in the finished piece. Name which of the three it is:

- **Incompetence** — the outcome served nobody, including the system's own beneficiaries
- **Path dependence** — the outcome follows from a decision made under conditions that no longer obtain
- **Noise** — the outcome did not recur, and the record shows no mechanism

Worked example. A national vaccine registry converts local reporting effort into national coverage statistics. Residual: between 2016 and 2019 it also produced duplicate records at a rate of roughly 4%, serving nobody, traceable to two counties that had merged their case-management systems and never reconciled the identifiers. That is path dependence, not design, and saying so is what keeps the character sentence honest.

## Three filled examples

### Example A — A container port (supply chain)

| Field | Entry |
|-------|-------|
| Outcomes | Berth productivity rose 18% 2015–2021; truck turn times rose from 41 to 96 minutes; chassis dwell doubled; three drayage firms of nine exited |
| Character sentence | Converts vessel-side efficiency into landside queueing, and converts drayage-firm working capital into terminal buffer |
| Constraints | Berth count (physical, port authority filings); labour agreement crane-hours (legal, contract text); gate hours (regulatory) |
| Loops | Reinforcing: faster discharge → more boxes on yard → longer truck turn → more boxes on yard. Quantity: yard utilisation. Delay: 2–5 days |
| Blind spots | Does not measure driver wait time; measures moves per crane hour |
| Stated purpose | Port authority charter: "to promote the efficient movement of commerce through the harbor" |
| Gap | The charter's "commerce" stops at the fence line; the measured objective function stops at the crane |
| Residual | The 2019 chassis shortage was national and hit ports with the opposite yard policy equally. Not explained by this objective function |

### Example B — A hospital sepsis protocol (health system)

| Field | Entry |
|-------|-------|
| Outcomes | Time-to-antibiotic fell 31%; ICU transfers unchanged; alert volume rose 6x; nurse override rate reached 71% by month 14 |
| Character sentence | Converts documented alert compliance into audit-passing records, and converts clinician attention into override clicks |
| Constraints | EHR vendor alert framework (technical); reporting requirement (regulatory); night-shift staffing ratio (headcount) |
| Loops | Balancing: alert fires → override → threshold unchanged → alert fires. Quantity: override rate. Delay: minutes |
| Blind spots | Does not measure whether the override was correct |
| Stated purpose | Quality committee minutes: "to ensure every patient meeting sepsis criteria receives antibiotics within one hour" |
| Gap | The protocol optimised the documented hour, not the patient selection |
| Residual | Two units achieved both faster antibiotics and lower ICU transfer. The objective function does not explain them. Both had a dedicated response nurse, which the protocol never specified |

### Example C — A programming-language package registry (software)

| Field | Entry |
|-------|-------|
| Outcomes | Package count grew 9x in six years; median time-to-patch for critical CVEs stayed near 19 days; four of the top-50 packages had a single maintainer for the whole period; two typosquat incidents |
| Character sentence | Converts download counts into maintainer obligation, without converting either into maintainer income |
| Constraints | Storage and bandwidth cost (capital); namespace immutability (design, documented in RFC); one paid staff member (headcount) |
| Loops | Reinforcing: popularity → dependents → issue load → maintainer burnout → transfer or abandonment → supply-chain surface |
| Blind spots | Does not measure maintainer count per package or bus factor |
| Stated purpose | Launch post: "a place to share and reuse code, freely, forever" |
| Gap | "Freely" was priced for consumers and not for producers |
| Residual | The two typosquat incidents were both caught within 48 hours by unpaid volunteers with no formal role. The objective function predicts nobody would look |

## The reform-attempt ledger

Systemic subjects are dramatized by people who push against them and reveal the shape of the wall. Extract every reform attempt in the material — failed, partial, and successful.

Per attempt record:
1. What they tried to change
2. Which constraint or feedback loop they were actually pushing against (name the field number)
3. What the system did in response
4. How long the change persisted
5. What would have had to be different — which loop, which constraint, which measurement — for it to hold

Select two or three attempts that push against DIFFERENT constraints. These become probe arcs. Write each to end at the constraint, not at a moral verdict. The payload is the shape of the wall, not the character's virtue.

**Balance requirement, mandatory.** At least one attempt that partially worked, or an explicit statement of the conditions under which this system has changed historically.

Why this is not optional: the institutions-as-Olympian-gods frame is powerful precisely because it is a stance, not a discovery. Adopted as a default it concludes that every system is unreformable — which is the same error as the inevitable march of progress, with the sign flipped. Outcome treated as foreordained is teleology either way. If every probe arc in your piece fails, the frame has become the argument rather than the finding.

Refuse the redemption default too. Do not grant a person a transformation the record does not show.

## Character dimensioning: the system translation

A longer reporting instrument, adapted from Hart's character checklist. Roughly 90% never appears in the prose; it exists so the 10% that does appear is chosen rather than defaulted. Fill from material only. Empty slots stay empty and go to the gap register.

| Person slot | System translation |
|-------------|--------------------|
| Physical distinguishing traits | Observable signatures: a characteristic latency, a fee structure, a seasonal shape, a recurring failure mode |
| Education and work history | Origin and design lineage: what it was built from, and what it was built against |
| Enemies, and why | Competing systems, substitutes, regulators, adversaries — with the why |
| Present problem | The binding constraint right now |
| Greatest fear | The failure the system is architected to avoid |
| How the problem gets worse | The trend that breaks the current equilibrium |
| Strongest / weakest trait | What it does better than any alternative / its structural fragility |
| Sees self as vs. seen as | Stated purpose vs. revealed function. The richest slot; often generates the whole piece |
| Speech tags and idioms | The system's characteristic vocabulary and its euphemisms |
| Description of home | The physical and institutional environment, and the feel of it |

Warning: this is a REPORTING instrument, not a generation template. A fluent model will invent a "greatest fear" for a payments network from priors. If the record does not answer the slot, the slot stays blank.

## The stated-vs-revealed billboard

The systemic nut graf. Five sentences, in this order, placed after the opening concrete scene:

1. Name the system and its boundary in time and scope.
2. Its stated purpose, quoted from a real document.
3. Its revealed objective function, from Field 2.
4. The consequence of the gap, with one number.
5. The basis of the account — what evidence the reader is about to be shown, and its limits.

**Contract rule.** Every later section must be traceable to one of the five sentences. Sections that are not traceable are cut, or the billboard is wrong.

**Anti-tease rule.** The billboard states the finding. Withholding it to build suspense is a fiction move that damages analytical credibility.

**Anti-false-balance rule.** Refuse "the truth is complicated." If the material does not support a gap, the honest billboard says the system did roughly what it claimed.

**Drift check (last step before delivery).** Re-derive the billboard from the finished draft's evidence. Diff it against the version written in Step 5. Any change must be surfaced to the human explicitly, because it usually means the research changed the finding and nobody noticed. Report as:

```
BILLBOARD DRIFT
  Sentence 3 (revealed objective function)
  Written:  converts applicant persistence into approvals
  Derived:  converts applicant legal representation into approvals
  Cause:    fields 1 and 5 updated after the 2019 case file was added
  Action:   REQUIRES HUMAN DECISION — the thesis changed
```

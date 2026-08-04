# Ledger Schema

The ledger is four columns, not three. FINDING, CLAIM, BEAT are the promotion path. DEAD is the parallel record of everything that was killed. All four ship with the deliverable.

## Table of Contents
- [Why four columns](#why-four-columns)
- [FINDING schema](#finding-schema)
- [CLAIM schema](#claim-schema)
- [BEAT schema](#beat-schema)
- [DEAD schema](#dead-schema)
- [Promotion rules](#promotion-rules)
- [Referential integrity](#referential-integrity)
- [The ratio check](#the-ratio-check)
- [The omission set](#the-omission-set)
- [Worked ledger extracts](#worked-ledger-extracts)
- [Handoff artefact](#handoff-artefact)

## Why four columns

A finding is checkable against a source. A claim is an interpretive commitment that can be wrong even when the finding is right. A beat is a claim that changes the reader's model of the world. Collapsing these is how a narrative acquires the authority of data it does not have.

The two failure modes are symmetrical:

- **Beat inflation**: under pressure to produce narrative, findings get promoted straight to beats and the claim column is skipped. The output reads as a sequence of dramatic reveals with no argument between them, and because the claim column was skipped, no falsification condition was ever written, so nothing in the piece can be checked.
- **Claim hoarding**: every finding acquires a hedge-laden claim, nothing is ever promoted to a beat, and the result is a competent report nobody finishes. Unread accurate work informs nobody, which is its own accuracy failure.

## FINDING schema

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | Stable, e.g. `F-112`. Never reused after a kill. |
| `statement` | yes | One verifiable assertion. No addressee, no interpretation, no so-what. |
| `evidence_class` | yes | A-F. See [evidence-classes.md](evidence-classes.md). |
| `pointer` | yes | Granular enough to re-find without the draft in hand. |
| `contested` | yes | If two sources conflict, keep BOTH values. Do not resolve by picking the better-sounding one. |
| `source_interest` | yes | Who benefits from this account being believed? "None identified" is an answer; blank is not. |
| `source_vintage` | yes | `contemporaneous-primary` / `contemporaneous-secondary` / `retrospective-primary` / `retrospective-secondary`. |
| `support_n` | when quantitative | How many underlying records, respondents, runs, or incidents. Thin support is a veto trigger. |
| `derived` | when quantitative | Observed vs computed. A fitted slope and a raw reading are not the same object. |
| `precision` | when quantitative or dated | The precision the source actually carries. "In the spring" is not "on a Tuesday in April". |
| `anachronism_flag` | when applicable | The statement uses a category, metric, or moral frame that did not exist at the time described. |

`source_vintage` is doing more work than it looks. Secondary retrospective material includes books, post-hoc analyses, and incident write-ups authored after the outcome. In all of these, the halo and the teleology were applied upstream, before you arrived. A ledger built on them will re-derive those distortions faithfully while passing every check. So a `retrospective-secondary` finding can never support an L1 MECHANISM causal grade.

`source_interest` matters because "contemporaneous" is not a clean standard either. Contemporaneous sources are produced by interested parties, are themselves selected by survival, and in business and technology domains are dominated by promotional material already contaminated by an in-progress halo. Date annotation without interest annotation moves the bias one step upstream instead of removing it.

## CLAIM schema

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | e.g. `C-14`. |
| `statement` | yes | The interpretive commitment. |
| `findings` | yes | >= 1 finding ID. |
| `leap` | yes | The interpretive step being taken, stated as a step. "From: three fabs reported X. To: the cohort as a whole did X." |
| `population` | yes | Named precisely. Not "companies" — "the eleven firms in the 2019 cohort that filed in both years". |
| `falsifier` | yes | What evidence would make this false. A claim with no falsifier is not a claim; send it back to FINDING or delete it. |
| `causal_grade` | when the claim asserts a link | L1-L5. See [causal-triage.md](causal-triage.md). |
| `agency_alternative` | for outcome claims | The strongest reading that attributes the outcome to skill, intent, or decision, and why it was or was not adopted. |

The `agency_alternative` field exists because a ledger discipline built on the red-team literature will systematically over-attribute outcomes to luck, structure, and path dependence — the critical literature is asymmetrically stocked with attacks on agency-based explanation. Anti-narrative bias is a real bias. Requiring the strongest agency reading in writing is the correction.

## BEAT schema

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | e.g. `B-3`. |
| `claims` | yes | >= 1 claim ID. |
| `prior_overturned` | yes | The belief this beat changes, phrased as a sentence someone actually held. "Readers assume outages cluster around deploys." |
| `relation_to_previous` | yes | One of: similarity, elaboration (shrink the scope), generalization (enlarge the scope), contrast, temporal, cause-effect. |
| `mechanism_argument` | when relation is cause-effect | A separate paragraph resting on something other than the data: an institutional fact, a physical constraint, a documented decision. No mechanism, no cause-effect label. |

**Cause-effect is rare in practice and over-produced by models.** In a labelled corpus of 4,186 story pieces from 230 professional data videos, the six relations occurred at roughly: elaboration 34%, similarity 32%, generalization 12%, contrast 10%, temporal 8%, cause-effect 5%. Cause-effect is the rarest and the most attractive, because causal prose reads as the most satisfying and the most confident. Cap it near the observed baseline and audit the mix. The failure is invisible to fact-checking: every individual finding is true and the sequence is false.

**Recontextualisation test**: for each beat, write one sentence stating what the reader believed after the previous beat that this one changes. If that sentence is empty, this is supporting evidence attached to an existing beat, not a beat of its own.

## DEAD schema

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | The original finding or claim ID, preserved. |
| `killed_by` | yes | The specific veto, check, or transform. "Thin-support veto, support_n = 3" not "weak". |
| `date` | yes | When. Order matters when reconstructing why the piece looks as it does. |
| `verdict` | yes | `DID-NOT-SUPPORT` or `CONTRADICTED`. |
| `original_pointer` | yes | Preserved so the kill is itself re-derivable. |

**The two verdicts are not interchangeable.** DID-NOT-SUPPORT means the evidence was insufficient: thin support, indefensible denominator, an unresolved instrument change, a transform that flipped the sign. CONTRADICTED means a source establishes the opposite. Conflating them lets a contradicted claim re-enter a later pass as merely unproven, which is how killed material comes back to life.

The DEAD column is also the only real defence against subtraction. Refusal training makes a model good at not adding and does nothing about not omitting. A perfectly constrained agent will produce an entirely sourced, entirely false piece by cutting the disconfirming quarter, the failed pilot, the dissenting source — each cut individually defensible on length or flow. The DEAD column plus the omission set, reviewed as a SET rather than per-item, is what catches the pattern.

## Promotion rules

1. Nothing moves right without an explicit promotion step and a written justification.
2. Promotion is one-way per pass. Nothing may be promoted and then demoted inside a single revision, or the ledger stops tracking anything. Demotion happens in the next pass, logged, with a reason.
3. A claim with no falsifier goes back to FINDING or is deleted.
4. A beat that overturns nothing becomes supporting evidence under an existing beat.
5. A kill is not a demotion. Killed items go to DEAD, not backward along the promotion path.

## Referential integrity

- Every beat cites >= 1 claim.
- Every claim cites >= 1 finding.
- Every finding cites an external data location: table and row range, document and page, commit hash, transcript timestamp, instrument log line, URL plus retrieval date.
- No pointer resolves into this pipeline's own outputs. See the circular-citation check in the main skill.

Check this mechanically by walking the graph. A dangling reference is a defect regardless of how good the sentence reads.

## The ratio check

| Observation | Diagnosis |
|-------------|-----------|
| Beats > claims | Narrating without arguing |
| Findings vastly exceed claims | Reporting without interpreting |
| Claims exceed findings | Asserting |
| Zero DEAD entries | The vetoes were not run, or were run and ignored |
| Zero omissions | The corpus was not larger than the piece, which for real material is implausible |

## The omission set

After the ledger is built, list every corpus item that appears nowhere in it. For each, write one sentence saying why. Then apply the rule: any item that would weaken the emerging spine and lacks a written reason is a cherry-pick and must be reinstated.

This is the expensive check and it is the one that matters. Every per-finding check in this skill can pass while the assembled work misrepresents the drift and proportion of events through selection alone. A ledger that is clean per-item and silent about what it left out is more dangerous than an unchecked draft, because it carries citations and reads as audited.

## Worked ledger extracts

### Post-mortem domain

```
F-208  statement: The first alert fired at 02:14:07Z on 2024-03-11.
       class: A  pointer: app-server.log line 88214, retrieved 2024-03-14
       contested: no  source_interest: none identified
       source_vintage: contemporaneous-primary  precision: second

F-209  statement: The on-call engineer acknowledged the page at 02:31Z.
       class: A  pointer: PagerDuty incident 44192, ack event
       source_vintage: contemporaneous-primary

F-210  statement: The retro document states the delay was caused by a
       misconfigured escalation policy.
       class: D  pointer: retro-2024-03-11.md, "Root cause", authored 2024-03-19
       source_vintage: retrospective-secondary
       NOTE: cannot support an L1 grade for the escalation link.

C-31   statement: Acknowledgement latency in this incident exceeded the
       team's own 5-minute target.
       findings: F-208, F-209
       leap: from two timestamps to a comparison against a stated target
       population: this incident only; no claim about the incident population
       falsifier: a target document dated before 2024-03-11 specifying a
       different threshold
       causal_grade: n/a (no link asserted)

DEAD   C-33  statement: Escalation misconfiguration caused the delay.
       killed_by: L1 downgrade — only source is F-210, retrospective-secondary
       verdict: DID-NOT-SUPPORT
       note: re-enters as an L3 SEQUENCE claim, or as an L5 marked inference.
```

### Market-history domain

```
F-401  statement: Reported industry shipments fell 22% between Q2 and Q3 1997.
       class: A  pointer: association annual report 1998, table 4, p.31
       support_n: 14 reporting members  derived: observed
       source_interest: the association's members set the reporting standard
       source_vintage: contemporaneous-primary

F-402  statement: The association changed its member reporting definition in
       Q3 1997 to exclude re-exports.
       class: A  pointer: association annual report 1998, methodology note, p.62
       source_vintage: contemporaneous-primary

DEAD   C-77  statement: Industry demand collapsed in Q3 1997.
       killed_by: instrument check — F-402 establishes a definitional revision
       coincident with the discontinuity; no re-baselined series available
       verdict: DID-NOT-SUPPORT
       note: the definitional change is itself the finding. Narrate the
       instrument change, or obtain a consistent series.
```

### Biography domain

```
F-115  statement: She wrote in a letter dated 12 June 1953 that she expected
       the appointment to be refused.
       class: A  pointer: papers, box 4, folder 9, letter to her sister
       source_vintage: contemporaneous-primary

C-08   statement: She anticipated the refusal before it arrived.
       findings: F-115
       leap: from one written statement to a mental state at that date
       population: this individual, June 1953
       falsifier: a contemporaneous document showing she made commitments
       inconsistent with expecting refusal
       causal_grade: n/a

DEAD   C-09  statement: The refusal was the turning point of her career.
       killed_by: retrospective-only — the earliest source treating this event
       as consequential postdates the outcome by 22 years
       verdict: DID-NOT-SUPPORT
       note: may return as an L5 marked inference, never in a climax slot.
```

## Handoff artefact

The artefact both macro and micro narrative agents consume contains, in this order:

1. **Frame lock**: unit, denominator, window, boundary; one rejected alternative and reason for each.
2. **Starting hypothesis**, dated, plus the diff against the current reading.
3. **Ledger**: FINDING, CLAIM, BEAT columns with referential integrity satisfied.
4. **Causal grade map**: every link, its grade, its permitted verb set.
5. **DEAD column**, typed.
6. **Omission set** with a reason per item.
7. **Integrity check results**, including the circular-citation verdict.
8. **The no-verification statement**, verbatim: "This ledger records provenance. No claim in it has been verified. Human verification status: none."

If a human did verify a subset, name the subset and the person. Never state verification generically. The correct verb for what this skill does is "sourced". Saying "verified" induces misplaced trust in a reviewer, and unchecked output is safer than output that falsely advertises checking.

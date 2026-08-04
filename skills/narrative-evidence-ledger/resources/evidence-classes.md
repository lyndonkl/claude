# Evidence Classes and Attribution Grammar

The A-F class scheme and the L0-L6 attribution ladder are working conventions assembled for this skill. They are not published standards. Cite them as house conventions, tune the boundaries for your domain, and say that you tuned them.

## Table of Contents
- [The six classes](#the-six-classes)
- [Pointer granularity](#pointer-granularity)
- [Source interest and source vintage](#source-interest-and-source-vintage)
- [The attribution ladder](#the-attribution-ladder)
- [Decision table: class to grammar](#decision-table-class-to-grammar)
- [Register porting](#register-porting)
- [The attribution budget](#the-attribution-budget)
- [Bad and good, four domains](#bad-and-good-four-domains)
- [Class F and the open-question conversion](#class-f-and-the-open-question-conversion)

## The six classes

| Class | Definition | Examples by domain |
|-------|-----------|--------------------|
| A | Primary artefact. A document, dataset, log, transcript, recording, or instrument reading that itself constitutes the evidence. | 10-K page; signed supply contract; app-server log line; git commit; assay output; meeting minutes; a letter in an archive |
| B | Direct first-person testimony about the speaker's own experience or action. | "I set the threshold at 40%"; an engineer describing what they did; a founder on their own decision |
| C | Second-hand testimony. A witness reporting someone else's experience, action, or state. | "My deputy told me he had already decided"; a colleague describing a meeting they heard about |
| D | Secondary reporting. Someone else's account of the events, where you did not obtain the underlying source. | A trade-press article; a textbook; a retrospective blog post; an analyst note summarising a filing you did not read |
| E | Analyst or agent inference. The reasoning is yours. | "The sequence is consistent with a capacity constraint" |
| F | Unsourced. You believe it and cannot point at anything. | Any statement whose pointer field is empty |

Class D is the one that quietly corrupts a ledger. A secondary account that cites nothing, or cites a primary source you never obtained, is still class D. If you can reach the underlying artefact, reach it and re-class to A. If you cannot, D stays D and the attribution must say the underlying source was not obtained.

## Pointer granularity

The test: **can a second person, with only the pointer and no access to your draft, independently produce this finding?**

| Fails | Passes |
|-------|--------|
| "the 10-K" | "FY2023 Form 10-K, p.47, Risk Factors — Supply" |
| "the logs" | "app-server.log, 2024-03-11 02:14:07Z, line 88214" |
| "the interview" | "interview with R. Okonjo, 2025-11-02, 00:41:15" |
| "the dataset" | "shipments.parquet, rows 4,102-4,388, column `net_units`, snapshot 2026-01-09" |
| "their blog" | "engineering blog, 'Scaling the write path', 2023-06-14, para 9, retrieved 2026-02-11" |
| "the repo" | "commit 8f31ac2, `scheduler/backoff.go`, lines 55-71" |

**The 10% re-derivation sample.** Draw 10% of findings at random. Hide the draft. Re-derive each finding from its pointer alone. If the pointer does not independently yield the finding, the class tag is wrong, not merely imprecise.

This detects the characteristic failure, which is annotation theatre: the ledger fills with citations that point at the wrong layer. At your own research summary. At a secondary article that itself cited nothing. At a document that mentions the topic without establishing the claim. The page looks rigorously sourced and is not.

## Source interest and source vintage

Two fields that most ledgers omit and that change the reading of everything above them.

**Source interest.** Who benefits from this account being believed? A supplier's capacity statement, a regulator's incident count, a vendor's benchmark, a departing executive's version of a decision, a lab's own replication — each has a party with a stake. "None identified" is a legitimate answer. Blank is not.

**Source vintage.** Four values:

| Value | Meaning | Constraint |
|-------|---------|-----------|
| `contemporaneous-primary` | Produced at the time, is itself the evidence | Can support any grade |
| `contemporaneous-secondary` | Produced at the time, reporting on something else | Cannot support L1 alone |
| `retrospective-primary` | Produced later by a participant about their own action | Memory-marked attribution mandatory |
| `retrospective-secondary` | Produced later by a non-participant | Cannot support L1 MECHANISM under any circumstance |

"Contemporaneous" is not a clean standard. Contemporaneous sources are produced by interested parties, are selected by survival, and in business and technology domains skew heavily toward promotional material and commentary already coloured by an in-progress halo. Dating a source without annotating its interest moves the bias one step upstream instead of removing it.

## The attribution ladder

| Level | Form | Example |
|-------|------|---------|
| L0 | Unmarked assertion | "Revenue fell 18% that quarter." |
| L1 | Embedded source: the source is a grammatical constituent, not an appendage | "The filing put revenue down 18%." / "The postmortem timestamps the first alert at 02:14." |
| L2 | Epistemic verb naming the epistemic act | "She recalled thinking the number was wrong." / "The model projected 4.1%." |
| L3 | Explicit attribution | "According to the former CFO..." |
| L4 | Contest marker: both values, both sources, one sentence | "The company put the figure at 40%; the regulator's audit found 27%." |
| L5 | Uncertainty declaration | "The record does not establish why the threshold was set there." |
| L6 | Methods block or note on sources | Absorbs routine load so L0 and L1 can carry the prose |

**L1 is the workhorse.** It carries full provenance and costs almost no rhythm. Prefer it to "according to" everywhere the source's identity matters but the claim is not contested. Most drafts that read as over-hedged are drafts that skipped L1 and reached for L3.

**L3 is a budget item.** Its scarcity is what makes it a signal. Spend it on contested, self-serving, or consequential claims.

**L4 is mandatory, not optional.** Every CONTESTED finding gets both values in the text. Never average two conflicting figures. Never silently pick the better-sounding one.

**L6 licenses L0 only for what it actually covers.** A methods block is not a blanket. The characteristic abuse is attribution laundering: the agent pushes everything to L0 and justifies it with a methods block the reader will never open. Every sentence is individually "covered"; functionally the piece asserts inference as observation. The symptom is a methods block that describes the reporting in general terms rather than mapping to specific passages. The guard is mechanical: every L0 sentence must trace to a class A finding ID.

## Decision table: class to grammar

| Situation | Required level |
|-----------|----------------|
| Class A, uncontested, covered by the methods block | L0 |
| Class A, consequential, or where the document's identity matters | L1 |
| Class B, first-person recall, not contested | L2 |
| Class B, self-serving or contested | L3 |
| Class C, any | L3 mandatory, plus explicit distance: "his deputy said he had been told..." |
| Class D, any | L3 mandatory, plus a flag that the underlying source was not obtained. Never L0 or L1 |
| Class E, any | L5-adjacent marking. "The record does not establish X; the sequence is consistent with..." Never presented as a finding |
| CONTESTED, any class | L4. Both values, both sources, one sentence |
| Gap: the structure wanted a fact and none exists | L5 in the text. Not silence, not a bridge sentence |
| Reconstructed scene or passage | The opening sentence carries the sourcing; the remainder may run unmarked under that cover |

## Register porting

Journalism has a "sources said" convention. Technical, financial, ML, and scientific registers do not — their prose norm is bare assertion backed by a bibliography. An agent tuned on journalistic forms and pointed at a chip-market analysis or a training-run writeup will drop attribution entirely, because the target register does not use it.

Port the **function** — evidentiary status visible in the sentence — into the target register's own forms. Do not import journalism's surface grammar. Do not drop the requirement.

| Register | L1 form | L2 form | L3 form | L5 form |
|----------|---------|---------|---------|---------|
| Journalism / narrative nonfiction | "The filing put revenue down 18%." | "He recalled thinking..." | "According to X..." | "No source could say..." |
| Financial / market analysis | "FY23 filings show revenue down 18%." | "Management guided to 4%." | "The sell-side consensus, per [note], was..." | "The disclosure does not break this out." |
| ML / systems writeup | "Table 3 reports 3.1 points." | "The authors estimate the gain at..." | "Per the model card, training used..." | "No ablation isolates this component." |
| Post-mortem / incident | "PagerDuty logs the ack at 02:31Z." | "The on-call reported believing the alert was a duplicate." | "The vendor's RCA attributes it to..." | "Telemetry for the 02:14-02:31 window was not retained." |
| Science writing | "The 2019 cohort study measured a 12% difference." | "The authors interpret this as..." | "A subsequent replication reported..." | "The effect has not been tested outside this population." |
| Supply chain / operations | "Customs records show 4,200 units cleared in March." | "The carrier's notice cites port congestion." | "According to the freight forwarder..." | "Transit times for the remaining lanes are not recorded." |
| Biography / archival | "The 12 June letter says she expected refusal." | "She later described the meeting as..." | "Her secretary's memoir places the call in..." | "The archive contains nothing from that fortnight." |

## The attribution budget

**Derived default, not a published figure.** If more than roughly one sentence in four in a passage sits at L3 or above, the passage is under-reported, not over-attributed.

The correct fix is more reporting, never fewer attributions. The failure mode here is operational, not aesthetic. Prose that reads like a compliance document — "according to" every third sentence, "appears to have" everywhere — gets its hedges stripped wholesale rather than surgically. The reviewer loses the true hedges along with the defensive ones. An over-hedged draft gets the whole apparatus switched off.

Diagnostic sequence when a passage feels hedge-saturated:

1. Count sentences at L3+. Over one in four? Go to 2. Under? The problem is prose rhythm, not attribution — rewrite the L3s as L1s.
2. Which findings under this passage are class C, D, or E? Those are what forced the L3s.
3. Can any of them be re-classed to A or B by obtaining the underlying artefact? Do that.
4. If not, the passage is asserting more than the corpus supports. Cut the passage's ambition, not its attributions.

## Bad and good, four domains

**Supply chain — class D wearing L0 grammar**

Bad: "Congestion forced carriers to reroute through Vancouver in early 2021."

Good: "Carrier filings put Vancouver call volume up 34% between January and April 2021 [F-112, class A]. Two operators cited congestion in their rerouting notices [F-118, class A]; the record does not establish why the others moved."

The bad version asserts a mechanism from a trade-press summary, at L0, with an L1-grade causal verb. Three errors in nine words.

**ML writeup — class E wearing the grammar of a finding**

Bad: "The auxiliary loss is what makes the architecture work at scale."

Good: "Accuracy rose 3.1 points in the run that added the auxiliary loss [F-44]. Three other changes shipped in the same commit [F-45..47]; no ablation isolates the loss. The most plausible reading is that the loss contributes, but the run does not establish it."

**Market history — silent resolution of a contested figure**

Bad: "Industry shipments fell 22% in the third quarter."

Good: "The association's members reported shipments down 22%; the customs series for the same period shows a 9% decline [F-401, F-403]. The association changed its reporting definition that quarter to exclude re-exports [F-402]."

The bad version picked the more dramatic of two conflicting figures and hid the instrument change that probably produced the gap.

**Biography — inference in the grammar of observation**

Bad: "She knew, then, that the appointment would be refused."

Good: "She wrote to her sister on 12 June that she expected the refusal [F-115]." Or, where only the sequence is documented: "The record does not say what she expected. She had already drafted the resignation letter."

## Class F and the open-question conversion

No finding may sit at class F when the ledger is handed off. Class F findings have exactly two dispositions:

1. **Delete.** The statement leaves the ledger and goes nowhere.
2. **Convert to an open research question.** Write the question in a form someone could actually answer: "Is there any contemporaneous statement by X, between 4 March and 30 April, about the threshold decision?" Not "find out more about the threshold."

There is no third disposition. "Draft it and flag it for review" is not a disposition — flagged drafted text survives review at high rates, because it reads well and the reviewer is checking rather than rewriting.

A ledger that reaches handoff with zero open questions is a red flag rather than a success. Real material always has holes.

# Disclosure and Reporting

How the note on sources gets generated, where disclosures must sit, and what the gate report looks like.

## Table of Contents
- [The core rule](#the-core-rule)
- [Note-on-sources generator](#note-on-sources-generator)
- [Worked example: a clean piece](#worked-example-a-clean-piece)
- [Worked example: a piece with deviations](#worked-example-a-piece-with-deviations)
- [Placement rules](#placement-rules)
- [The inversion check](#the-inversion-check)
- [Gate report template](#gate-report-template)

## The core rule

**Generate the disclosure FROM the deviation log. Never write it in advance.**

Disclosure describes an already-honest method. It does not purchase deviations. The apparatus must never become negotiable — "we'll note that dialogue was recreated, so we can recreate dialogue" is the inversion, and once it happens the whole system is a laundering machine.

Boilerplate disclaimers are worse than nothing in an automated pipeline. They are cheap to emit, they pre-authorize the deviations, and they make the reader believe a human weighed a trade-off that nobody weighed.

## Note-on-sources generator

Produce the six sections in this order. Each is generated from a log, not composed.

**1. SCOPE OF EVIDENCE** — what the account is built from. Document types, counts, date ranges, datasets, interviews, direct observation. Specific, not gestural.

- BAD: "This account draws on extensive research including public filings and interviews."
- GOOD: "This account draws on 14 quarterly filings (FY19–FY23) and the incident timeline kept by the on-call rota. It also uses 31,000 rows of shipment data from the customs feed (Jan 2021–Mar 2024), plus recorded interviews with six of the eleven people named."

**2. RECONSTRUCTION STATEMENT** — which passages are reconstructed rather than observed, and from exactly what.

- GOOD: "The account of the March review is reconstructed from the minutes, two participants' contemporaneous notes, and interviews with three attendees. No recording exists."

**3. DEVIATION REGISTER** — one line per deviation, generated from the chronology, composite, and empty-slot logs. **If the register is empty, say so affirmatively.** G. Wayne Miller's model sentence is the positive template: "This is entirely a work of nonfiction; it contains no composite characters or scenes, and no names have been changed. Nothing has been invented."

**4. UNCERTAINTY REGISTER** — what the account could not establish; where sources conflicted and how that was handled; what a contemporaneous observer could not have known.

**5. INTERESTS AND ACCESS** — funding, access arrangements, prior relationships, anything given in exchange, editorial control conceded. For analytical and financial domains: positions held, client relationships, and any data supplied by an interested party.

**6. AI DISCLOSURE** — state that drafting was machine-assisted. State that provenance was human-checked **only if it actually was**. Do not write that anything was verified. The apparatus tracks provenance; it does not verify.

## Worked example: a clean piece

Deviation log empty. Post-mortem of a systems incident.

> **On sources.** This account is built from the incident channel transcript (02:04–07:52 UTC, 11 March), the service's own alert log, and the two deploy records covering the window. It also draws on recorded interviews with four of the six responders, conducted 18–22 March.
>
> Nothing here is invented. There are no composite people, no composite scenes, and no names have been changed. Every quoted string appears verbatim in the transcript or in a recorded interview; where a responder described their reasoning at the time, the text says so rather than narrating it directly.
>
> Three things the account could not establish. Who first proposed the rollback: the channel shows the decision, not the proposal. Whether the 02:41 config change was applied before or after the failover: the two logs disagree by roughly ninety seconds, and both timestamps appear in the text. And what the on-call engineer's escalation path was: the rota document for that week was not retained.
>
> Drafting was machine-assisted. Source pointers were checked by a human against the original artefacts.

Note what this does: the deviation register is *affirmatively empty*, the uncertainty register is specific, and the conflicting timestamps are named rather than resolved.

## Worked example: a piece with deviations

Market history where one anonymization was needed.

> **On sources.** [Scope paragraph.]
>
> Two departures from standard practice. One source is identified only as "a former desk head at one of the three clearing banks", at their request; the description is accurate and no details have been altered to obscure them further. And the sequence in the second section is told out of chronological order — the 2019 filing is discussed before the 2017 acquisition that produced it. Both dates are given at the seam and no duration has been compressed.
>
> There are no composite entities in this piece. No dialogue has been recreated.

Note what this does *not* do: it does not say "some events have been compressed and some dialogue recreated". It names exactly two deviations, both of which happened, and affirmatively denies the categories that did not occur.

## Placement rules

**Anything that changes how the reader should read the text goes at the FRONT.** Routine sourcing detail may go at the back.

**Any inference, conjecture, reconstruction, or empty-slot fill occupying a structural slot must be disclosed within two sentences of itself, in the body, in the same typographic register as the surrounding prose.** Disclosure confined to endnotes, footnotes, an appendix, or a methods block is functionally undisclosed. Readers experience the body.

This is the disclosure that degrades. Under a "tighten this up" or "make it flow" instruction, the disclosure sentence is the first thing an editing pass removes, or it drifts to the back matter — restoring exactly the false impression the protocol existed to prevent. Mark those sentences non-removable, or carry them as annotations the renderer is required to emit. Assume any later pass will strip them unless they are structurally protected.

**Budget.** Cap the total hedges, contingency nodes, and disclosure sentences per thousand words. When the budget binds, that is a signal to change the architecture, not to spend more budget. A piece that is sixty percent epistemic apparatus and forty percent subject is unreadable and misleading in a new way: it makes the analyst's uncertainty the story. (The specific cap is a project decision; there is no published figure.)

## The inversion check

Run this last, and run it honestly.

**Was any entry in the deviation register decided BEFORE the corresponding passage was drafted?**

If yes, the apparatus has inverted. The note stopped describing the method and started licensing it. The piece needs re-reporting, not re-noting. Report `INVERSION CHECK: fail` and block.

Symptoms:
- The note on sources exists in the working directory before the draft does.
- A deviation register entry is phrased in the future or conditional ("dialogue may be reconstructed where transcripts are unavailable").
- The register uses category language rather than instance language. Real entries name the specific passage and the specific deviation.

## Gate report template

Emit verbatim. Every field, every run.

```
NARRATIVE FIDELITY AUDIT — <piece title>
This pass SOURCED the draft against the ledger. It did not verify anything.

BASIS
  Ledger claims:                 n
  Pointers unresolved:           n
  Pointers resolving into this pipeline (circular): n
  Sources annotated with interest as well as date:  n of n
  Sources that are secondary retrospectives:        n

BRIGHT LINES
  Breaches:                      n     [must be 0 to clear]
  By line: 1:n 2:n 3:n 4:n 5:n 6:n 7:n 8:n 9:n 10:n 11:n 12:n 13:n 14:n
  Dispositions applied:          DELETE n / DOWNGRADE n / DECLARE n / RESEARCH n

INTERIORITY
  [A] n   [B] n   [C] n   [D] n     [D must be 0 to clear]
  Sourced-but-hedged defects (over-correction): n
  Intentionality verbs on systems: n

RED FLAGS
  Hits: n     Resolved to a pointer and kept: n     Deleted: n
  (If deleted >> kept, the scan is keying on vividness rather than pointers.)

THREE ALTITUDES
  Sentence-level defects:  n
  Paragraph-level defects: n
  Passage-level defects:   n     [0 across a long piece = pass did not run]

SUBTRACTION
  Log present:             yes / no        [no = RETURN TO RESEARCH]
  Cuts logged:             n
  Set verdict:             pattern found / no pattern
  Omission check items unjustified: n
  Proportion asymmetries unjustified: n

HEDGE LOAD
  Sentences at L3+:        n of n  (n%)
  Verdict:                 under budget / over budget -> passage under-reported

DISCLOSURE
  Note on sources:         generated from deviation log / not generated
  Deviation register:      n entries / affirmatively empty
  In-body disclosures within two sentences of their claim: n of n
  Inversion check:         pass / fail

SURFACED FOR HUMAN DECISION (not resolved here)
  - <real named party in an adversarial structural role, and on what evidence class>
  - <right-of-reply gaps: adverse specific claims about living people or active institutions>

VERDICT: BLOCKED | RETURN TO RESEARCH | CLEARED AS SOURCED
```

**Verdict definitions:**

- **BLOCKED** — a bright-line breach, a nonzero [D] count, a circular citation, or a failed inversion check. Not shippable in this form.
- **RETURN TO RESEARCH** — no bright-line breach, but the evidence does not support the piece: hedge load over budget, subtraction log absent, unjustified omissions, or two or more empty structural slots. The fix is reporting, not editing.
- **CLEARED AS SOURCED** — every claim traces to a pointer outside this pipeline, the three altitudes ran and produced defects at all three, and the note on sources was generated from the deviation log. This is the strongest verdict available. There is no "verified".

**What this pass does not adjudicate.** Where a real named person or an active institution occupies an adversarial structural role, surface it and stop. Adverse inference about a living person creates real exposure, and a subject who consented to an interview did not consent to a structural role. Quietly softening the language while keeping the structure makes the problem invisible rather than solving it. The same applies to right-of-reply gaps: note them in the report and let a human decide.

# The Four-Corner Worksheet

Truby's four-corner opposition, rebuilt as an evidence-bearing worksheet. The four corners are his; the numeric defaults, the tests, and the audit procedures below are operational choices made for auditability, not published thresholds.

## Table of Contents
- [The shared field](#the-shared-field)
- [Per-corner fields](#per-corner-fields)
- [The four tests](#the-four-tests)
- [The drive collapse audit](#the-drive-collapse-audit)
- [Worked web 1: open-source project governance](#worked-web-1-open-source-project-governance)
- [Worked web 2: public-health cold chain](#worked-web-2-public-health-cold-chain)
- [Worked web 3: a replication controversy](#worked-web-3-a-replication-controversy)
- [Three-corner and two-corner fallbacks](#three-corner-and-two-corner-fallbacks)

## The shared field

Fill this once. It belongs to the whole web, not to any corner.

**CENTRAL MORAL PROBLEM (one question):** ____

Requirements:

- It is a question, not a verdict. "Who was responsible for the outage?" invites one answer and produces a prosecution. "How much reliability do you owe a customer who is not paying for it?" invites four.
- Every corner must answer it differently, and each answer must be defensible by someone who is not a fool.
- It must be answerable from the material. If you cannot point at a document per corner where that corner states or enacts its answer, you are writing your own debate and casting real people in it.

Bad central problems and why:

| Bad question | Failure | Repair |
|---|---|---|
| "Was the vendor negligent?" | Yes/no; one defensible answer | "When does a maintainer's right to stop become someone else's emergency?" |
| "How did the market evolve?" | Not moral, not contested; a process question | "Who should bear the cost of a standard that only pays off after everyone adopts it?" |
| "Why do institutions fail?" | Too abstract to be answered by these four parties from this material | "What does an agency owe the users of a service it has already decided to shut down?" |

## Per-corner fields

Fill for all four. Every field carries a citation or the marker `[INFERRED]`.

```
CORNER: A / B / C / D
ROLE: protagonist / main opponent / secondary opponent 1 / secondary opponent 2
WARRANT TIER: opponent (3/3) / rival (2/3) / environment (0-1/3)   [from resources/opponent-warrant.md]
IDENTITY: who or what, precisely, with its boundary in time

WEAKNESS: the structural fragility or personal deficiency, with a CONTEMPORANEOUS source
          predating the outcome

DESIRE: the visible goal. For opponent corners this must be the SAME scarce object as A's.
        Name the moment at which success or failure becomes externally verifiable.

VALUES (3-5, stated as goods this corner believes in, each with a citation):
  1. ____
  2. ____
  3. ____

POWER / STATUS / ABILITY: what this corner can actually do, in resources and authority

ROUTE OF ATTACK on A's weakness: the exact mechanism. Must differ from every other
        corner's route. "They compete with A" is not a route.

ANSWER TO THE CENTRAL MORAL PROBLEM: one sentence, in this corner's terms

JUSTIFICATION: how this corner defends what it does, in its own voice (mandatory in full
        for corner B; one sentence is acceptable for C and D)

CONFLICTS WITH WHICH OTHER CORNERS, AND OVER WHAT:
  vs B: ____   vs C: ____   vs D: ____
  (A corner that only conflicts with A is a satellite, not a corner.)

APPEARANCES IN DRIVE SECTION (fill during the collapse check): ____
```

### The value-label rule

Every value must be traceable to something the corner said or did. This is where webs quietly become fiction.

- Weak: "The regulator valued institutional control." That is your inference about a motive.
- Strong: "The agency's 2019 supervisory guidance states its first priority as preventing depositor loss, ahead of preserving the number of independent institutions." That is the corner's stated good, in its words, dated.
- Acceptable with a label: "`[INFERRED]` The agency behaved as if consolidation were preferable to failure: it approved four of five acquisitions and blocked none."

Values written as evils are always inference and always wrong. "They valued profit over safety" is your verdict. The corner's version is "a service nobody can afford to run is a service nobody gets." Write theirs.

### The route-of-attack rule

Corners C and D exist to attack the protagonist's weakness by a route B does not use. Route means mechanism, not opinion. If B and C both "pressure A publicly," they are one corner.

Distinct routes, from a fictional-but-typical municipal utility case where A's weakness is a deferred-maintenance backlog nobody has costed:

| Corner | Route |
|---|---|
| B, the state auditor | Publishes the backlog number, converting a private liability into a public one |
| C, the bond insurer | Reprices the debt, converting the backlog into a cash-flow problem next quarter |
| D, the union local | Refuses overtime on unmaintained equipment, converting the backlog into a service outage this week |

Same weakness, three mechanisms, three timescales. That is a working web. Three corners that all "criticise the utility" is one corner with three names.

## The four tests

Run all four. Record the result of each; a web delivered without test results is unaudited.

**1. PUSH CHECK.** For each of the six pairs (AB, AC, AD, BC, BD, CD), name the sharpest difference between their value clusters. Any value appearing in two corners forces a change: either sharpen one corner's value into something the other would reject, or cut the corner. Maximum differentiation is the entire point of the exercise.

**2. CONFLICT CHECK.** For each of the six pairs, state what they fight over and cite it. Pairs that never touch are the tell. A web where BC, BD, and CD are all blank is a two-part opposition with extra labels.

**3. DELETE TEST.** Remove corner D entirely. Re-read the argument of the piece. Does anything break?

- Something breaks: D is load-bearing. Keep it.
- Nothing breaks: D was decoration. Two options, both honest. Give D a genuine competing value cluster the material supports, or drop to three corners and say in your notes that the material supported three.

Repeat for C. It is common and fine to end with three corners. It is not fine to keep four and pretend.

**4. RECOGNITION TEST.** Read corner B's justification paragraph aloud. Would a competent person holding that position recognise themselves in it? See [resources/opponent-warrant.md](resources/opponent-warrant.md) for the full procedure and the strawman-versus-steelman contrasts.

## The drive collapse audit

Run this on the finished draft, not on the plan. Even after building a real four-corner web, writers collapse to protagonist-versus-opponent in the prose, because binary conflict is easier to narrate. The worksheet cannot detect this. Only the draft can.

Procedure:

1. Mark the DRIVE section of the draft: everything after the protagonist's plan is established and before the resolution begins. Roughly the middle. If your piece has no such section, that is a separate structural problem — go to `writing-structure-planner`.
2. Inside the drive only, count appearances per corner. An appearance means the corner acts, speaks, or its position is represented as a live force. A mention in a subordinate clause is not an appearance.
3. Apply the default target: at least three appearances per corner in the drive, and at least one appearance in the final third of the drive. This threshold is a derived default chosen so that a corner cannot survive on a single cameo; adjust it for very short pieces and say that you did.
4. Any corner below target has one of three dispositions, and you must pick one explicitly:
   - **PROMOTE**: find the corner's real drive-section action in the material and write it in.
   - **CUT**: remove the corner from the web and from the setup. A corner introduced and abandoned leaves the reader holding an unresolved obligation.
   - **DEMOTE**: reclassify it as environment or context and strip its intentional verbs.
5. Report the counts. The collapse-check report is a deliverable, not a private step.

Failure signature to look for in the prose itself: corners C and D appear in a single setup paragraph that lists all the parties, then never again. That paragraph is the tell. It reads like completeness and functions as an alibi.

## Worked web 1: open-source project governance

Protagonist is a system-with-carriers: a volunteer-maintained library that a large number of products depend on.

**Central moral problem:** When software everyone depends on is maintained by volunteers, who owes what to whom?

**A — the maintainer team (protagonist).** Weakness: no succession plan; two people hold all merge rights, documented in the project's own 2021 governance thread. Values: correctness over convenience; the right to say no; a small dependency surface. Answer to the problem: nothing is owed; the licence says so, and the licence is the contract.

**B — the downstream commercial vendor (opponent, 3/3).** Same goal: control of the release cadence. Competition: both publish releases of the same library. Awareness: vendor's engineering blog names the project. Directed action: vendor funded a fork and hired one of the two maintainers, dated. Values: predictable support windows; customers should never see breakage; paying for outcomes is legitimate. Route: buys the succession the project never built, attacking the weakness directly. Answer: obligations follow from dependence, and dependence can be bought out.

**C — the distribution packagers (rival, 2/3).** Same goal: control of the release cadence. Values: reproducibility; long-term stability; every patch must be backportable. Route: freezes an old version and backports security patches, draining relevance from upstream rather than buying it. Conflicts with B: B ships fast features, C freezes interfaces, and both cannot be satisfied by one release. Answer: obligations run to users of the whole system, not to any one project.

**D — the coordinated-disclosure process (opponent, 3/3, and it is a process rather than a party).** Same goal: control of the release cadence, at the moment of a vulnerability. Values: disclosure deadlines are non-negotiable; users deserve to know; unmaintained code is a public hazard. Route: publishes with a fixed clock, forcing the maintainers to ship on someone else's schedule. Conflicts with C over backport-versus-upgrade advice, and with B over embargo handling. Answer: obligation is to the public, and it overrides both the licence and the contract.

Why this passes the delete test: remove D and the piece loses the only force that binds all three others to a calendar. The argument about volunteer obligation loses its hard edge.

## Worked web 2: public-health cold chain

Protagonist is a person: a district immunisation officer.

**Central moral problem:** How much of a scarce good do you let spoil in order to reach the people hardest to reach?

**A — the district officer.** Weakness: has never reported a wastage figure above the tolerated ceiling, documented in three years of her own returns filed before the events. Values: presence in every village; a clinic that has never had vaccine is worse than one that spoils some; trust is built by showing up.

**B — the ministry logistics directorate (rival, 2/3).** Same goal: control of the last forty cold boxes. Values: waste is theft from the next district; coverage must be measurable; centralised allocation is the only fair allocation. Route: reallocates boxes on a wastage metric, attacking A's weakness by making her honest reporting the reason she loses supply.

**C — the donor's monitoring team (rival, 2/3).** Same goal: control of the same forty boxes. Values: dose-level traceability; conditionality is what makes aid work; unverifiable delivery is indistinguishable from no delivery. Route: withholds the next tranche pending an audit, attacking the same weakness by a slower mechanism with a longer reach. Conflicts with B: B wants the boxes moved this week, C wants them stationary until counted.

**D — the local clinic committees (rival, 2/3).** Same goal: the same boxes. Values: the village that has waited longest goes first; local knowledge beats a spreadsheet; a promise made in person is binding. Route: publicly commits A to a delivery she has no supply for. Conflicts with B over who allocates and with C over whether counting is respect or suspicion.

**Not a corner — the constraint.** The vaccine's two-to-eight-degree tolerance and the four-hour road. It has no values, no awareness, and no directed action. It sets the ceiling on every corner's plan and belongs in the constraint inventory. Writing "the cold chain fought back" would be the exact error this skill exists to prevent. Write instead: "no route from the depot reaches the three northern clinics inside the tolerance, and none of the four positions above changes that."

## Worked web 3: a replication controversy

Protagonist is a system: a research subfield.

**Central moral problem:** What do you owe a body of work that has been useful and may not be true?

**A — the subfield's established programme.** Weakness: an effect size that was never estimated from a pre-registered design, visible in the 2013 methods reviews written before the failed replications. Values: cumulative evidence over single studies; theory should guide measurement; a literature is not overturned by one null.

**B — the replication team (opponent, 3/3).** Same goal: control of what the subfield's textbooks say the effect is. Competition, awareness, and directed action all documented in the exchange of published comments. Values: a claim you cannot reproduce is not a claim; methods sections are the real paper; publishing the null is the service. Route: reruns the canonical study at high power, attacking A's weakness at its origin.

**C — the journal editors (rival, 2/3).** Same goal: control of the textbook claim, exercised through what gets printed. Values: novelty is what a journal is for; adjudication is the field's job and not the editor's; the record is corrected by publication, not by retraction. Route: slows both sides by controlling the venue, which attacks A's weakness by leaving the original claim standing and uncontested in print. Conflicts with B over whether nulls are publishable.

**D — the funders (rival, 2/3).** Same goal: control of the claim, exercised through what gets studied next. Values: money should follow translatable results; replication is not new knowledge; a portfolio should be judged in aggregate. Route: keeps funding extensions of the original effect, attacking A's weakness by ensuring nobody re-estimates it. Conflicts with B over what counts as a contribution and with C over what counts as impact.

Note the double: A and B share a value neither will state, that the published record ought to be the field's memory. That shared value is what makes them opponents rather than strangers. Record it in the DOUBLE field of the opponent audit.

## Three-corner and two-corner fallbacks

Not every body of material supports four corners. The failure is padding, not honesty.

**Three corners.** Legitimate and common. Run all the same tests on the three pairs. State in your notes: "The material supported three corners; the fourth candidate (____) failed the delete test because ____."

**Two corners.** A genuine two-part opposition is a simple argument, and simple arguments are sometimes true. But check first: two corners plus a strong constraint is usually a three-corner web where you have not yet given the constraint a carrier. And check second: a two-part opposition is where good-versus-evil lives. If you are down to two, the recognition test on B's justification becomes the whole quality gate.

**Zero corners.** No party in the record opposed any other. Go to the mystery substitute in [resources/opponent-warrant.md](resources/opponent-warrant.md). Do not proceed with a web.

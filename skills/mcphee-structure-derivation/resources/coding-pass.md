# The Coding Pass

Reference matter for Steps 1-3: the card schema, code-quality tests, log formats, and two worked derivations - one with a system protagonist, one with a person.

> The corpora below are **synthetic illustrations**, invented to show the mechanics of sorting. They are labelled as such deliberately. In real use, every card must trace to a real source, and this skill's central prohibition is against creating a card to fill a hole in an emerging shape.

## Table of contents

- [Why the cold read comes first](#why-the-cold-read-comes-first)
- [Card schema](#card-schema)
- [Code-quality tests](#code-quality-tests)
- [Log formats](#log-formats)
- [Worked derivation A: a system protagonist](#worked-derivation-a-a-system-protagonist)
- [Worked derivation B: a person protagonist](#worked-derivation-b-a-person-protagonist)
- [When the derivation should refuse](#when-the-derivation-should-refuse)

## Why the cold read comes first

The first read produces nothing. No codes, no highlights, no notes. This is not ceremony. The moment you begin classifying, your first three classifications become the categories that the rest of the corpus is forced into, and everything that does not fit one of them becomes invisible. McPhee's account is that he read his notes until patterns emerged - the patterns arrive from the whole, not from the first ten pages.

For an agent the failure is sharper than for a human. An agent that codes on the first pass will produce codes that mirror the order the material was fetched in, so the "derived" structure ends up being the retrieval order with topic names painted on it.

Record the cold read as a completed step. If the corpus is too large to read whole, read a stratified sample whole, and say in the shape contract that you did.

## Card schema

One code per card. Each card carries six fields:

| Field | Content | Rule |
|---|---|---|
| `code` | Short topic code, airport-code style | Names the topic, never the document part |
| `content` | One line: what the chunk says | If it takes three lines, it is two cards |
| `date` | Date or date range the material belongs to | Unknown goes to a dated-unknown pile, never to a guessed slot |
| `source` | Document, page, transcript timestamp, table row, commit hash | No source, no card |
| `typicality` | `median` / `tail` / `unique` against the corpus | Required before a card can hold a load-bearing position |
| `kind` | `event` / `state` / `claim` / `figure` / `quote` | `state` cards cannot be treated as moments |

Example cards:

```
code: SMELTER-Q3        date: 2019-08-14   kind: event   typicality: tail
content: Refinery halts three of five lines after a grid fault; 11-day stoppage.
source: Operator incident notice 2019-08-14, p.2

code: RETRY-STORM       date: 1994-03-02   kind: event   typicality: median
content: Client retries amplify a 40-second backend blip into a 6-hour outage.
source: Post-incident review PIR-114, timeline section

code: ASSAY-DRIFT       date: 1957-1961    kind: state   typicality: median
content: Published enzyme activity figures drift 12% across four labs, unexplained.
source: Reanalysis table 3, Hollins 2004
```

The `kind` field is what stops "through the late 1990s" from being written as a scene. A `state` card describes a condition holding over a span; it can open a section but it cannot be a moment. For a system protagonist this distinction does most of the work, because systems tempt you to narrate a decade as if it were an afternoon.

## Code-quality tests

Run each proposed code through these four. A code failing any of them gets rewritten before sorting.

1. **Topic, not part.** `BACKGROUND`, `CONTEXT`, `ANALYSIS`, `IMPLICATIONS`, `DISCUSSION`, `KEY-FINDINGS` are document parts. They will reassemble themselves into a generic essay outline and the derivation will look like it worked. Rewrite as the thing the chunk is actually about.

   Bad: `BACKGROUND` / `CONTEXT-2` / `ANALYSIS-MAIN`
   Good: `PORT-STRIKE-71` / `GRID-FAULT` / `LICENSE-DENIAL`

2. **Would sort two ways.** A good code has both a date and a topic, so it can appear in Sort A and Sort B at different positions. A code that can only be placed thematically (`THEORY`) or only chronologically (`TIMELINE-3`) is not sortable and is therefore useless to this procedure.

3. **Under five words, no sentence.** Codes are handles. `THE-SHIFT-TOWARD-DISTRIBUTED-PROCUREMENT` is a thesis wearing a code's clothes and it will smuggle a conclusion into the sorting stage.

4. **Repeatable.** If the same code is assigned to eight chunks, either it is a legitimate recurring thread (fine - it will braid) or it is too coarse (split it). Eight chunks under `POLICY` is too coarse. Eight chunks under `WAFER-YIELD` spanning four years is a thread.

## Log formats

### Disagreement log

Required output of Step 2. One row per card that the two sorts place materially differently.

| Card | Sort A position (chronological) | Sort B position (thematic) | Nature of the disagreement | Resolution | Artifact |
|---|---|---|---|---|---|
| `LICENSE-DENIAL` | 4th, between two 2011 cards | 11th, grouped with regulation | Theme pulls it forward by seven years | Chronology | none |
| `DESIGN-MTG-96` | 1st | 6th, grouped with architecture | Origin material precedes reader interest | Chronology starting late + one flashback | Re-entry: `ADOPTION-VOTE` (2011-06-09) |

A derivation reporting zero disagreements did not run both sorts. Near-total agreement is possible only when the corpus is a single unbroken process; say so explicitly if you claim it.

### Discarded-card log

Two columns, always separate. This separation is the guard against the quiet failure where structural discipline eats disconfirming evidence, since evidence that contradicts the emerging shape is by definition evidence that does not serve it.

| Card | Reason | Category |
|---|---|---|
| `TRADE-SHOW-04` | Interesting, no bearing on the spine | did-not-support |
| `YIELD-RECOVERY-05` | Yield recovered a year before the fix shipped, against the causal reading | **contradicted** |

Rule: `did-not-support` cards may be pruned without mention. `contradicted` cards must appear in the body of the finished piece, not in an endnote and not stacked in a qualifications paragraph at the end.

## Worked derivation A: a system protagonist

**Synthetic corpus:** a regional battery-materials supply chain, twenty-two documents.

**Step 1 - cold read.** Whole corpus read, nothing marked.

**Step 2 - codes.** Fourteen cards emerge:

`MINE-EXPAND` (2016), `OFFTAKE-A` (2017-03), `OFFTAKE-B` (2017-03), `RAIL-CLOSURE` (2018-05), `SMELTER-Q3` (2019-08), `SPOT-SPIKE` (2019-09), `RECYCLE-PILOT` (2019-11), `EXPORT-RULE` (2020-02), `CELL-DERATE` (2020-06), `PACK-RECALL` (2020-09), `SECOND-SOURCE` (2021-01), `PRICE-FLOOR` (2021-04), `MINE-IDLE` (2022-07), `AUDIT-FINDING` (2022-11).

**Sort A (chronology):** MINE-EXPAND, OFFTAKE-A, OFFTAKE-B, RAIL-CLOSURE, SMELTER-Q3, SPOT-SPIKE, RECYCLE-PILOT, EXPORT-RULE, CELL-DERATE, PACK-RECALL, SECOND-SOURCE, PRICE-FLOOR, MINE-IDLE, AUDIT-FINDING.

**Sort B (theme):** *Contracts* (OFFTAKE-A, OFFTAKE-B, PRICE-FLOOR, SECOND-SOURCE); *Physical disruption* (RAIL-CLOSURE, SMELTER-Q3, MINE-IDLE); *Prices* (SPOT-SPIKE, CELL-DERATE); *Policy* (EXPORT-RULE, AUDIT-FINDING); *Alternatives* (RECYCLE-PILOT, MINE-EXPAND, PACK-RECALL).

**Disagreement log, abridged:**

| Card | A | B | Nature | Resolution |
|---|---|---|---|---|
| `PRICE-FLOOR` | 12th | 3rd, with contracts | Theme pulls a 2021 instrument next to 2017 offtakes | Chronology |
| `MINE-EXPAND` | 1st | 13th, with alternatives | Theme reads a 2016 expansion as an alternative-supply story | Chronology |
| `AUDIT-FINDING` | 14th | 10th, with policy | Theme groups it with the 2020 export rule | Chronology |
| `RECYCLE-PILOT` | 7th | 14th | Theme treats it as an epilogue | Chronology |

Every row resolves to chronology. No theme here is strong enough to buy a flashback. That is the ordinary outcome, and it is the point of the default. Adopting Sort B would have given the piece four concept-named sections: Contracts, Disruption, Prices, Policy. Each would hold evidence from 2016 through 2022 in scrambled order. No tension would accumulate anywhere.

**Step 4 - juxtapositions.** One candidate survives the footnote gate: `OFFTAKE-A` (the contract language guaranteeing volume irrespective of route availability) beside `RAIL-CLOSURE` (the route closing fourteen months later). The implied inference - the contract priced volume risk and ignored route risk - is one you would state and cite to both documents. A rejected candidate: `EXPORT-RULE` beside `SPOT-SPIKE`, which would imply the rule moved the price when the spike preceded it by five months. That is adjacency-as-causation and it fails the gate on the dates alone.

**Step 5 - shape.** Linear, with one white-space argument in the third section. Runner-up: geographic traverse (mine to smelter to cell to pack), rejected because the corpus's disruptions are dated events rather than located stages, so a traverse would have forced date-scrambling to hold the route order.

**Contract:** shape = linear; runner-up = geographic traverse; flashbacks = none; juxtapositions = 1 (`OFFTAKE-A` | `RAIL-CLOSURE`); contradicted cards to surface in body = `YIELD-RECOVERY-05`.

## Worked derivation B: a person protagonist

**Synthetic corpus:** the papers of a crystallographer, 1938-1979.

**Codes:** `LAB-MOVE-38`, `WARTIME-GAP`, `FIRST-STRUCTURE-49`, `PRIORITY-DISPUTE-52`, `TEACHING-LOAD`, `METHOD-PAPER-58`, `INSTRUMENT-BUILD-61`, `REFUSAL-64` (declines a directorship), `SECOND-STRUCTURE-71`, `ARCHIVE-INTERVIEW-79`.

**The one disagreement that mattered:** Sort B groups `LAB-MOVE-38` with `INSTRUMENT-BUILD-61` under *apparatus*, twenty-three years apart. Sort A keeps them at opposite ends. Here the theme has a real claim on the material - the same physical problem, solved twice, with opposite institutional support - and the comparison is the meaning.

**Resolution:** dual profile on a named common denominator: *building your own instrument*. The denominator is written down as that noun phrase, which is what licences the break from chronology. Inside each half of the dual profile, chronology is restored strictly.

**Not licensed:** `PRIORITY-DISPUTE-52` and `REFUSAL-64` also cluster thematically (both are about credit), but the cluster produces no comparison the reader could not make from the timeline. It stays chronological. A theme earns a break when the comparison is the finding, not when it is merely tidy.

**Flashback:** one, from `METHOD-PAPER-58` back to `WARTIME-GAP`. Re-entry point named: `INSTRUMENT-BUILD-61`.

**Shape:** dual profile on a common denominator, with an interior linear chronology in each panel.

## When the derivation should refuse

Refusal is a legitimate output and must be reported as a finding, not worked around.

- **No causal chain.** Cards are independent findings sharing only a period or a subject. No sort produces accumulating tension. Output: "no derivable narrative shape; use a grouped form" and hand to `writing-structure-planner`.
- **No dates.** More than roughly half the cards land in the dated-unknown pile. Sort A cannot run, so the procedure cannot run. Say what dating the corpus would need.
- **Two independent spines.** Two contradictions with separate evidence bases, neither subordinate. Braid or split into two deliverables, and log which was set aside and why. Do not flatten to one mechanism because one mechanism is more elegant.
- **A hole in the shape.** The emerging shape requires a card the corpus does not contain. The shape is wrong. Never write the missing card.

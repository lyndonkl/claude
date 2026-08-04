# The SCAM Gate, Worked

SCAM (Setting, Character, Action, Meaning) is a four-slot test for whether a candidate passage is a genuine scene. It is journalism-pedagogy shorthand from Dynamics of Writing. It is **not** Jack Hart's acronym. Do not attribute it to him or to Storycraft.

## How to run it

Build a 4x3 table per candidate: slot, filled content, source pointer. Then apply the four gates.

```
Scene ID: INC-0412
Slot | Content                                      | Pointer
S    | ...                                          | ...
C    | ...                                          | ...
A    | ...                                          | ...
M    | ...                                          | ...
Gate 1 (no empty slot):        pass / fail
Gate 2 (M adds nothing new):   pass / fail
Gate 3 (skeptical reader):     pass / fail
Gate 4 (unwritable w/o source):pass / fail
Disposition: built | demoted to summary | research request | declared absence | cut
```

## Gate 4 in practice

Gate 4 is the load-bearing one and the one an agent will skip, because the other three can all be passed by a fluent invention. Run it like this: hide the pointer column. Read the passage. Ask whether a competent writer with no access to the corpus, holding only the topic and the date range, could have produced this paragraph from priors. If yes, the passage is generated, not reported, and it goes.

The tell is that the details are *category-typical* rather than *instance-specific*. Anyone knows a data center hums. Nobody knows without a log that the 03:12 page went to the wrong rotation.

## Worked candidate 1 — engineering post-mortem (PASSES)

| Slot | Content | Pointer |
|------|---------|---------|
| S | The 12 April on-call rotation, US-East control plane; the deploy freeze had lifted 40 minutes earlier | change-calendar entry CH-8841; freeze notice, #ops-announce 09:20 |
| C (system) | Control-plane API error rate at 0.02% at 09:41, 31% at 09:47; the service had never before failed closed on a config parse error | Grafana panel export, api-5xx, 09:30-10:00; RCA doc s3.2 |
| A | 1. Config v412 merged at 09:44. 2. Rollout reached the third cell at 09:46. 3. The parser rejected the new key and the process exited at 09:47:11 | commit 7f2a9c1; rollout log lines 118-140; crash trace, node-31 |
| M | The freeze was the only thing that had been catching this class of change | maps to the piece's claim about process substituting for tests |

Gate 4: could this have been written without the corpus? No. The 09:47:11 exit and the "never before failed closed" behavior are instance-specific and both resolve to artifacts.

## Worked candidate 2 — market history (PASSES, system CHARACTER)

| Slot | Content | Pointer |
|------|---------|---------|
| S | The Tuesday afternoon Treasury auction, 15 May, at the 13:00 bidding deadline | auction results release, CUSIP 912810XX, p.1 |
| C (system) | The 10-year cleared at 2 basis points above the when-issued yield; primary dealers took 34.1% of the issue against a 12-month average of 17.8% | results release, tables 1 and 3 |
| A | 1. Indirect bids came in at 41.6%, the lowest of the eight auctions that year. 2. The auction tailed. 3. The when-issued market repriced 4bp within the hour | results release; TRACE prints 13:00-14:00 |
| M | The dealer take is what the auction leaves behind when the buyers it was designed for do not show | maps to the claim about who absorbs supply |

Note what the CHARACTER slot is here: a state (a clearing price, a share of issue) and a behavior (the tail). It is not "the market grew nervous". No intent verb appears anywhere in the row.

## Worked candidate 3 — supply chain (PASSES)

| Slot | Content | Pointer |
|------|---------|---------|
| S | Berth 6, Barbours Cut, 14 May 2021 | terminal berth log, entry 2214 |
| C (system) | Yard utilization at 94% of TEU capacity; the terminal had been running single-shift gate hours since 2 May | PMSA monthly table 2; gate notice 21-14 |
| A | 1. *Ever Lissome* logged in at 06:12. 2. Discharge began 19:40. 3. First container cleared the gate the following morning | berth log 2214; gate transaction file, 15 May |
| M | Capacity had stopped being about cranes | maps to the claim about labor hours, not equipment |

## Worked candidate 4 — biography (FAILS Gate 1, then Gate 4)

| Slot | Content | Pointer |
|------|---------|---------|
| S | Her office in the spring of 1978, papers everywhere, late afternoon light | **none** |
| C | She was known to be exacting | **none** for the physical detail |
| A | She read the memo and set it aside | letter to her brother, 3 June 1978, mentions "the memo I ignored in March" |
| M | She already knew the department would not back her | inference |

Gate 1 fails: SETTING has no pointer and CHARACTER has no sourced physical detail. Gate 4 also fails: the papers, the light, and the exacting temperament are category-typical and could have been written by anyone. The A slot has one sourced event, not three ordered ones.

**Correct disposition**: demote to summary. "In a letter that June she referred to a memo she had ignored in March; the departmental file for that spring does not survive." That sentence is honest, carries the same fact, and invents nothing. The gap ("the departmental file does not survive") is legitimate narrative material and often the most useful beat available.

## Worked candidate 5 — ML writeup (FAILS Gate 2, salvageable)

| Slot | Content | Pointer |
|------|---------|---------|
| S | Run 42, the 14:00 restart after the checkpoint at step 118k | run manifest; W&B run id 3ka9 |
| C (system) | Loss at 2.31, flat for 6k steps; gradient norm spiking every 400 steps | W&B panels, loss and grad_norm |
| A | 1. LR warm restart applied at step 118k. 2. Loss fell to 2.09 over 3k steps. 3. Grad-norm spikes stopped | run config diff; W&B panels |
| M | The team had been chasing a data problem for two weeks and it was an optimizer problem, which is why the eval suite never caught it | **introduces the two weeks and the eval-suite claim, neither of which is in S/C/A** |

Gate 2 fails: the MEANING sentence smuggles in new facts. This one is fixable without swapping the scene. Cut M back to what S/C/A support: "the instability was in the schedule, not the data." Move the two-week hunt and the eval-suite point into the summary paragraph that follows. Interpretation is licensed there, and it can carry its own pointers.

## The demotion procedure

When a candidate fails any gate, it does not become worse prose. It becomes a different unit. Pick one:

1. **Demote to summary.** Write the sourced facts at summary distance, with no sensory grammar. This is the default and it is not a defeat.
2. **Research request.** Emit a specific, answerable question: "Is there a berth log for 15 May?" Preferred when the corpus can still grow.
3. **Declare the absence in the text.** "What the committee discussed between 3 and 17 March is not recorded." Absences are legitimate narrative material.
4. **Cut.**

There is no fifth disposition. "Draft it and flag it for review" is not a disposition: flagged drafted text survives review at high rates, because it reads well and the reviewer is checking rather than rewriting.

## What the gate cannot do

The gate checks that a claim points somewhere. It cannot check that the source is right. Write "sourced to the berth log"; never write "verified". An agent that reports verification it did not perform is worse than an agent that reports nothing, because unchecked output at least looks unchecked.

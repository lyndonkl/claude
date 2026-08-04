# Number Landing: Making Quantities Land In Prose

Reference matter for Step 3 of the workflow. The governing idea is old newsroom practice: a number alone has almost no meaning. Meaning comes from relative value.

## The caps, and where they come from

| Cap | Value | Status |
|-----|-------|--------|
| Numbers per narrative paragraph | 3 | Working default for narrative prose. Not a published figure. |
| Numbers per sentence | 1 | Working default. |
| Numerals per paragraph, reference matter | ~8 | Published newsroom guidance (KSJ Science Editing Handbook). A ceiling, not a target. |

Treat the caps as a trigger for a decision, not a law. Over cap, you choose: move to a table, move to an exhibit, move to a footnote, or cut. You never choose "spread them across two sentences".

## Rounding table

| Source value | Prose | Why |
|---|---|---|
| 105% increase | doubled | The reader holds "doubled". They do not hold 105%. |
| 33.2% | one in three | Ratio beats percentage at low precision. |
| 49.6% | about half | "About" is a precision claim: plus or minus the rounding unit. |
| $1.043bn | about a billion | Unless the difference from $1.4bn is the argument. |
| 4.7 days vs 3.2 days | nearly five days, up from three | Direction and human units. |
| 0.9994 AUC vs 0.9989 | five ten-thousandths apart, inside seed noise | Here the digits ARE the claim and must survive. |

**Hedge words are precision claims, not softeners.**
- "about" means plus or minus the rounding unit.
- "nearly" and "more than" assert a direction. They must be true in that direction.
- "roughly" signals genuine estimate uncertainty, not a rounded exact figure.

Never use them decoratively. "Roughly 47.3%" is a contradiction on its face.

## Human-scale conversions

Pick the denominator the reader already owns.

| Domain | Raw | Human scale |
|---|---|---|
| Public health | 44,000 deaths a year | a town the size of Wilkes-Barre, emptied, every year |
| Supply chain | 18,412 containers dwelling over 72 hours | three in five boxes on the terminal |
| ML evaluation | 3.2e22 training FLOPs | about eight times the compute of the previous release |
| Market history | $47bn of new issuance | more paper in one quarter than the prior three years combined |
| SRE | 99.92% availability | about seven hours down a year, or one bad afternoon a quarter |
| Biography | 1,100 letters over 31 years | a letter every ten days for three decades |

The conversion must not become a claim of its own. "A town emptied every year" is a scale device. It is not an assertion that the deaths were concentrated, simultaneous, or in one place. If a reader could take the device literally and be wrong, add the clause that stops them.

## Direction before magnitude

The sign is the information. The size is the qualifier.

- Bad: "Median time to detect was 41 minutes in the second half, against 26 minutes in the first."
- Good: "Detection got slower. It took about forty minutes to notice an incident by year end, up from under half an hour."

Bad forces the reader to do the subtraction and then infer the sign. Good gives the sign in three words and spends the rest on scale.

## Never open cold on a number

A paragraph that opens on a figure the reader has no frame for is wasted. Build the frame in one clause, then land it.

- Cold: "Yield at the new node ran at 61%."
- Framed: "A new process node is considered economic somewhere above eighty percent yield. This one ran at sixty."

The frame can be a threshold, a prior period, a peer, or a stated expectation. It cannot be a definition of the metric — that is a glossary, not a frame.

## Bureaucratic number-words

| Bureaucratic | Plain |
|---|---|
| expenditures | spending |
| utilization | use |
| headcount | staff, people |
| revenue (in plain-audience prose) | income, sales |
| remuneration | pay |
| throughput degradation | slowdown |
| attrition | people leaving |
| capital expenditure | building and equipment |
| adverse events | harms, side effects |
| non-performing exposures | loans not being repaid |

Keep the technical term when the audience uses it as a term of art, or when a defined accounting or clinical meaning is load-bearing. Swapping "revenue" for "income" inside a financial statement discussion introduces an error. Swapping it in a general-audience paragraph removes a barrier.

## Worked pairs, four domains

**Market history.**
Bad: "Trading volume in the contract reached 412,000 lots in March 1998, a 187% increase over the 143,600 lots recorded in March 1997, while open interest grew 62.4% to 88,900."
Good: "Volume in the contract nearly tripled in a year, to just over four hundred thousand lots a month. Open interest — the money actually left on the table overnight — grew far more slowly, which tells you most of the new activity went home flat."

**ML evaluation.**
Bad: "The model achieved 87.4% on the benchmark, up from 84.1%, with a variance across seeds of 1.2 points."
Good: "The model gained about three points on the benchmark. Seeds move it more than a point on their own, so a third of the gain could be noise. Two of the three runs that ended above the old score also ended above it before fine-tuning."

**Post-mortem.**
Bad: "The incident lasted 4h12m, affecting 2.3% of requests, with p99 latency reaching 8,412ms against a baseline of 312ms."
Good: "The outage ran most of an afternoon. One request in forty failed outright. For the slowest one percent of users the service went from a third of a second to more than eight seconds, which is past the point where people reload."

**Biography.**
Bad: "Between 1911 and 1918 she published 47 articles, 12 in journals with circulation above 10,000."
Good: "She published something every other month for seven years. A quarter of it reached the large-circulation journals, which at the time was the only route to a paying readership."

## The stat wall, and its mirror

The stat wall packs figures in to demonstrate rigour. The eye slides off exactly where the evidence is strongest.

The mirror failure is worse. Rounding away a distinction that materially mattered trades a stall for an error. "About a billion" is a defect when the difference between $1.04bn and $1.4bn is the argument. Test each rounding against the specific claim the sentence makes, not against a general readability preference.

## Person and system variants

| Move | Person protagonist | System protagonist |
|---|---|---|
| Human scale | per week of her life, per year of practice | per shipment, per wafer, per request, per enrolled patient |
| Comparison | against her own earlier period, against a named peer | against the prior regime, a peer market, a design threshold |
| Frame before the number | what she or her contemporaries expected | the stated threshold, the design spec, the regulatory limit |
| Single case | her own figure IS the population — no repair needed | one case is a sample of one — the next sentence restores the distribution |

The last row is the one that goes wrong. Framing a distributional finding through one quantified individual raises engagement precisely because it invites the reader to reason from a single case. When the real protagonist is a market, a protocol, or a cohort, the individualized opening is the most-remembered part of the piece and the least representative. If you use it, the next beat must restore the distribution and state what the case is and is not typical of.

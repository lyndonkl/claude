# Shape Catalog

Reference matter for Step 5. Each shape has an emergence test (what the two sorts must show before you may name it), a diagram, a person variant, a system variant, and a failure signature.

> **Provenance caveat.** McPhee drew and described several of these shapes, most famously in his 2013 essay on structure. This seven-row list is a working taxonomy assembled from that essay and from commentary on it - not a canon McPhee codified, and not a closed set. Use the names as vocabulary for the naming step. If your resolved sequence genuinely fits none of them, describe it in one sentence that a reader could redraw from, and treat that sentence as the name.

## The naming rule

You may name a shape only when you can state its emergence test in one sentence about your own cards. "It felt chronological with some themes" is not a name and not a test. If nothing fits, keep sorting. The pressure to end the sorting step by inventing a hybrid label is the main reason derivations stop one pass too early.

---

## Linear

**Emergence test:** Sort A and Sort B mostly agree, or every disagreement resolved to chronology.

```
[1]--[2]--[3]--[4]--[5]--[6]
```

**Person:** A career told forward. A trial told day by day.
**System:** A standard's revisions in release order. A supply chain's disruptions in date order. A codebase's migrations.

**Failure signature:** an undifferentiated timeline. Everything is equally weighted, nothing accumulates. The fix is not to switch shapes - it is to check whether the corpus contains a contradiction at all. Linear material with no contradiction is a chronicle, and a chronicle should be told as one rather than dressed as a narrative.

**Guard:** linear is the default and therefore the least examined. Confirm you actually ran Sort B, rather than defaulting to time because it required no decisions.

---

## Circular

**Emergence test:** one card is both the strongest available entry point and the natural close, and the material between them explains how the first reading of that card was incomplete.

```
      [A]
     /   \
  [4]     [1]
    \     /
     [3]-[2]
```

**Person:** open on a surgeon mid-shift; close on the same shift, now legible.
**System:** open on the dated shutdown; close on the same shutdown after the reader knows what the operators knew.

**Failure signature:** the return is a restatement rather than a revision. If the closing pass on card A adds nothing the reader did not have at the top, the circle is decoration. Cut to linear.

**Guard:** the returning card must be the *same* card, not a similar one. Two different shutdowns is a braid, not a circle.

---

## Spiral

**Emergence test:** the same window of time supports three passes at widening radius, each pass containing cards the previous pass could not have used.

```
[narrow]--> [wider]--> [widest]
   |___________|___________|
        same window
```

**Person:** one decision, then the family it moved through, then the town.
**System:** one plant, then the firm, then the industry. One failed request, then the service, then the platform.

**Failure signature:** the passes repeat rather than widen. Each pass must add a scale of evidence, not a rephrasing. If pass two contains the same cards as pass one with more adjectives, you have a linear piece with redundancy.

**Guard:** name the radius of each pass explicitly in the shape contract - "plant / firm / industry" - so the widening is checkable.

---

## Dual profile

**Emergence test:** two card sets sit on one denominator you can write as a single noun phrase, and the meaning of the material lives in the contrast rather than in either set alone.

```
[ A1 A2 A3 ]  ||  [ B1 B2 B3 ]
      \_____denominator_____/
```

**Person:** two chemists working the same problem in different institutions.
**System:** two ports on one shipping lane. Two teams running the same migration. Two jurisdictions applying one rule.

**Failure signature:** the denominator is vague ("innovation", "leadership", "risk"). A vague denominator lets any two sets sit together and produces a comparison with no finding in it. If you cannot write the denominator as a concrete noun phrase - *building your own instrument*, *the same assay*, *one shipping lane* - the shape is not earned.

**Guard:** inside each panel, restore strict chronology. Dual profile buys you one break from time, at the top level only.

---

## Triple profile on a common denominator

**Emergence test:** as above, with three sets, and the third genuinely adds a dimension rather than a third data point. Three sets that only confirm each other are a list, not a profile.

```
[ A ]   [ B ]   [ C ]
  \_______|_______/
      denominator
```

**Person:** three surgeons performing one procedure across three decades.
**System:** three outages traced to one shared dependency. Three adoptions of one protocol under three regulators.

**Failure signature:** the third panel is thin. If set C has four cards against A's fourteen, either promote a subordinate theme into C or drop to dual profile. An underweight panel reads as an afterthought and readers discount all three.

---

## Geographic traverse

**Emergence test:** the cards order naturally along a route or physical path, *and* that ordering does not require scrambling dates to hold.

```
[origin]--[stage]--[stage]--[terminus]
```

**Person:** a walk along a fault line. A journey up a river, told in the order of the miles.
**System:** ore to smelter to cell to pack. Request to edge to service to datastore. Field to elevator to port to mill.

**Failure signature:** the route wins and the dates scramble. Physical order is a form of thematic order, so it competes with chronology and must survive the same test. If holding the traverse forces 2016 evidence after 2022 evidence with no flashback discipline, chronology wins and you use linear.

**Guard:** traverse works best when the corpus's events *are* located stages. It works badly when the events are dated shocks that happen to occur at places.

---

## Braided

**Emergence test:** two or three timelines advance in parallel, they cross-cut at datable moments, and neither can be told to completion before the other without the reader losing the connection.

```
A1----A2--------A3-----A4
   B1------B2-------B3
   ^cross  ^cross    ^cross
```

**Person:** two rivals, years interleaved.
**System:** regulation and market price. A research programme and the instrument it needed. A migration and the incident load it caused.

**Failure signature:** the strands never touch. If A and B only alternate without crossing, you have two pieces stapled together. Mark the cross-cut cards explicitly; three or more crossings is the working minimum for calling it a braid (a derived default, not a published figure).

**Guard:** braiding is the honest home for DHY material - two independent contradictions that both matter. Preferring braid over flattening to one mechanism is the anti-flattening move. But the alternative of splitting into two deliverables is often better, and the contract must say why you chose to braid.

---

## Shape does not exist

**Emergence test:** the cards are independent findings with no causal chain, or more than half the corpus is undated, or two spines are genuinely independent and neither subordinate.

Output the finding. "This corpus has no derivable narrative shape; it is six audit findings sharing a fiscal year" is a successful result. Hand to `writing-structure-planner` for a grouped or pyramid form, where the organizing logic is category and importance rather than time.

The pressure to avoid this outcome is strong, because a named shape feels like a deliverable and a refusal feels like failure. It is the opposite: a shape named over material that does not support one will manufacture causality, and manufactured causality is a correctness defect rather than a style choice.

---

## The invisibility test

Once named, run it. Could a reader recite your structure after one read?

**Over-signposted (fails):**

> This piece has three parts. First we examine the contracts, then the disruptions, then the policy response. Having examined the contracts, we now turn to the disruptions. As we saw above, the offtake agreements had priced volume risk. In the next section we will see what happened when the route closed.

**Invisible (passes):**

> [section break]
>
> The rail line closed on 14 May 2018.

The second version carries the same transition. The date does the work the roadmap sentence was doing, and the section break does the rest. Delete roadmap sentences until the reader can follow the piece without being able to draw it.

Two exceptions worth naming. A genuinely obligated reader who must be able to navigate - a regulator, a reviewer, an on-call engineer reading a post-mortem at 3am - may need a signposted contents block at the top. That is navigation furniture, not structure narration, and it belongs outside the prose. And a braid may need one sentence establishing that two timelines are running, because the reader cannot infer a second strand from its first card alone.

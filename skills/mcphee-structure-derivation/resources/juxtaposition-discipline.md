# Juxtaposition Discipline

Reference matter for Step 4. Juxtaposition is McPhee's most portable move and the most dangerous one this skill carries, so it gets its own gate.

## What the move is

Two units of researched material placed side by side, with a hard section break between them and no bridging sentence, produce an inference the writer never states. McPhee's account of the effect, describing a pair of sections in *Encounters with the Archdruid*: in the white space between those two sections there is a great deal he does not have to say.

The mechanism is deletion. You write both units, you write the sentence stating what they jointly mean, and then you delete that sentence. What remains is an argument the reader assembles.

## Why it needs a gate

An inference in white space escapes citation discipline. A stated claim gets a footnote, a hedge, a confidence level, and a reviewer who can dispute it. An implied claim gets none of those, and it lands just as hard - harder, because readers trust conclusions they believe they reached themselves.

In evidence-bound domains this inverts the usual advice. In a memoir an unstated implication is craft. In a post-mortem, a regulatory history, a research writeup or a financial analysis, an unstated implication is an uncited claim, and the fact that it is deniable is the problem rather than the defence.

So: **only juxtapose to imply a relation you would state outright and defend with a footnote.**

## The gate

Run this on every candidate pair. All five must pass.

1. **Write the inference down.** In the margin, as a full sentence, in the plainest form. If you cannot write it, the pair does not carry one and the adjacency is decoration.
2. **Footnote test.** Would you state this sentence in the body and attach the evidence you hold to it? If no - if the honest answer is "I would have to hedge it so heavily it would lose its force" - discard the pair. Do not keep the juxtaposition because the hedged version is weaker. That weakness is the evidence telling you something.
3. **Revision, not echo.** Does the second unit revise the first, or restate it? Echo is decoration. Revision is argument. Order the pair so the second card changes what the first meant.
4. **Naive-reader test.** Would a reader with no prior context state the inference unprompted? If not, the units are wrong. Change the units. Do not restore the deleted sentence and call it a juxtaposition.
5. **Budget.** Roughly one white-space argument per major section (a derived working default, not a published figure). The device works by contrast with ordinary prose. Made the default rhythm, it stops working, and every section break starts reading as an insinuation.

## Passing pairs, across domains

| Domain | Card 1 | Card 2 | Inference (written, then deleted) | Why it passes |
|---|---|---|---|---|
| Incident analysis | The escalation runbook, v4, as written | The on-call transcript for the night in question | The runbook was not followed | Both documents are in the record; you would state and cite this |
| Institutional history | The charter's stated admissions criterion | Ten years of admitted-cohort composition | The stated criterion did not govern | Both are documentary; the claim is about a gap, not a motive |
| Supply chain | Contract language guaranteeing volume regardless of route | The route closing fourteen months later | The contract priced volume risk and ignored route risk | A claim about what the document covers, defensible from the document |
| Biography | A public statement declining credit | A private letter claiming priority | The public modesty was positional | Both texts exist; the inference is about inconsistency, not psychology |
| Science writeup | The registered analysis plan | The published analysis | The analysis changed after data collection | Two dated documents; this is exactly the kind of claim one footnotes |

Note what all five have in common: the inference is about a **gap between two records**, and both records are in hand. That is the safe class.

## Failing pairs

| Domain | Card 1 | Card 2 | Implied inference | Why it fails |
|---|---|---|---|---|
| Market history | A policy decision in July | A price move in August | The decision moved the price | Adjacency-as-causation. You would not state this without an identification strategy, so you may not imply it |
| Incident analysis | A team reorganisation in Q1 | An outage in Q3 | The reorg caused the outage | Same failure, and it assigns blame to named people through arrangement alone |
| Supply chain | An export rule in February | A price spike the previous September | The rule moved the price | Fails on dates alone; the effect precedes the cause |
| Research programme | A funder's stated priority | A lab's subsequent topic shift | The lab chased money | Attributes motive. Motive is not in the record |
| Biography | A childhood incident | An adult decision forty years later | The incident explains the decision | Psychological causation, unfalsifiable, and the white space hides that it is unfalsifiable |

The pattern in the failures: the inference is about **causation or intent**, not about a gap between records. Causal and motive claims need to be stated, so they need the citations that stating requires.

## The system-protagonist trap

Juxtaposition's failure mode has a distributed cousin. When the protagonist is a market, a protocol, an institution or a codebase, causal claims can also enter through verbs - "the market decided", "the protocol wanted", "the algorithm chose". Each one is a miniature white-space argument: an assertion of intent that never faces the citation discipline an explicit claim would face.

Rule: personify at most once, as an openly flagged framing device. After that, attribute behaviour to named mechanisms and named actors. Count the personifying verbs in a draft and cap them. This is the same discipline as the footnote gate, applied at sentence scale.

For a system protagonist, the safe juxtaposition class is narrower and clearer than for a person: **the stated rule beside the observed behaviour**. Charter beside conduct, runbook beside transcript, spec beside implementation, public messaging beside shipped product, registered plan beside published result. All of these compare two records. None of them requires you to know what anything wanted.

## Recording the survivors

The shape contract lists every surviving juxtaposition in this form:

```
JUX-1  cards: RUNBOOK-V4 | PAGER-LOG-0217
       inference: the documented escalation path was not used
       would state and cite: yes - runbook p.3, pager log 02:17-02:44
       order: RUNBOOK-V4 first (LOG revises it)
       section: 3
```

Recording the inference in the contract is what makes it auditable later. It also keeps the deleted sentence recoverable. If a reviewer says the white space is doing too much work, paste the sentence back in with its footnote. That was always the fallback, and taking it is never a failure.

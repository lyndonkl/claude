# The Agency Ledger

A mechanical pass that finds sentences where a non-agentive subject takes an intentional verb, and forces a substitution that names the actual mechanism.

The grounding claim: teleology enters through grammar. Subject-verb-object carries connotations of intent even in prose that is explicitly arguing against intent. So "the market wanted higher yields" is not a bad sentence. It is a false causal claim wearing a sentence.

## Table of Contents
- [What this pass is and is not](#what-this-pass-is-and-is-not)
- [Verb classification](#verb-classification)
- [The four repairs](#the-four-repairs)
- [Banned without a named mechanism](#banned-without-a-named-mechanism)
- [The post-pass check](#the-post-pass-check)
- [The personification budget](#the-personification-budget)
- [Causal claim typing](#causal-claim-typing)
- [The responsibility-laundering reverse check](#the-responsibility-laundering-reverse-check)
- [The inevitability audit](#the-inevitability-audit)

## What this pass is and is not

It is a CLAIM filter. It is not a purity filter.

An agent told simply "don't anthropomorphise" overshoots into agentless passive prose, which is worse — passive voice obscures causation rather than clarifying it. Empirical work on anthropomorphism in science writing for non-experts found no measurable comprehension penalty and no significant misconception effect from anthropomorphic text, only that it was evocative and occasionally distracting.

So the rule is not "remove agency." The rule is:

> Relocate agency onto the entity that actually has it. Repair intentional verbs that assert false causation. Tolerate ones that are transparently figurative and locally unambiguous.

## Verb classification

Extract every sentence whose grammatical subject is a system, market, technology, institution, disease, algorithm, protocol, codebase, or abstraction. Classify the main verb.

**(a) MECHANICAL — allowed.** rose, fell, cleared, settled, propagated, saturated, reallocated, queued, blocked, expanded, contracted, spread, accumulated, drained, routed.

**(b) INTENTIONAL — must be repaired.** wanted, decided, chose, sought, aimed, tried, punished, rewarded, learned, realised, understood, refused, allowed, ignored, preferred, remembered, believed, knew.

**(c) EVALUATIVE-TELEOLOGICAL — must be repaired.** matured, advanced, evolved toward, progressed, developed into, naturally moved to, grew up, came of age, found its footing, corrected itself.

Class (c) is the sneakier one. It smuggles a value judgment and a direction of travel at the same time. "The standard matured" asserts that later is better and that the change was internally driven.

## The four repairs

Apply in preference order. The first that the material supports wins.

### Repair 1 — NAME THE ACTOR

Use when specific parties took specific actions.

| Bad | Good |
|-----|------|
| "The market punished the sector." | "Three of the four largest holders sold into the bid across two sessions." |
| "The board wanted a faster exit." | "Two directors, both from the 2019 preferred round, voted against the extension." |
| "Regulators cracked down." | "The state banking department issued 14 consent orders in nine months, all naming the same disclosure clause." |

### Repair 2 — NAME THE MECHANISM

Use when a rule, price, schedule, or physical pathway did the work.

| Bad | Good |
|-----|------|
| "The protocol wanted lower latency." | "The fee schedule paid 0.4 bps more on blocks confirmed inside 400 ms." |
| "The scheduler prioritised long jobs." | "Jobs above 4 GB requested memory skipped the preemption queue, so they ran to completion while short jobs were evicted." |
| "The disease targeted the lungs." | "The receptor the virus binds is densest in alveolar epithelium, so viral load concentrated there." |

### Repair 3 — NAME THE SELECTION PRESSURE

Use when the population shifted and nobody decided. Selection claims must never be written in intentional grammar. "The industry moved to X" is a selection claim disguised as a decision.

| Bad | Good |
|-----|------|
| "The industry evolved toward outsourced fabrication." | "Firms that kept fabrication in-house lost 12 points of margin and exited by 1998; every survivor had outsourced." |
| "Newsrooms learned to chase traffic." | "Sections whose pages fell below the traffic floor lost their staff line in the next budget; the sections that remained were the ones already above it." |
| "The codebase converged on the async API." | "Modules still using the blocking API broke on every release after 4.2 and were rewritten or deleted; nobody wrote a migration policy." |

### Repair 4 — QUOTE THE HUMAN

Use when a person decided and the record names them. Name the person, the meeting, the date, and the document.

| Bad | Good |
|-----|------|
| "The company decided to ship." | "Vargas approved the release at the 3 October go/no-go, over the objection recorded by the reliability lead in the same minutes." |
| "The project decided to deprecate the plugin loader." | "Okonkwo closed the RFC on 12 March with 'we cannot support two loaders'; neither other committer with merge rights objected." |
| "The agency chose not to inspect." | "The regional administrator's 2017 memo reassigned all four inspectors to permitting, citing the hiring freeze." |

### When no repair is possible

If none of the four can be made from the material, that is a RESEARCH GAP, not a style problem. Emit it as a gap entry:

```
AGENCY GAP
  Sentence: "the exchange tightened margin requirements"
  Needed:   who set the requirement, under what rule, on what date
  Searched: rulebook amendments, board minutes, member notices
  Status:   UNRESOLVED — do not draft this sentence
```

Do not substitute a metaphor for a missing mechanism. A metaphor in this slot reads as an explanation and is not one.

## Banned without a named mechanism

- "the market wanted / expected / demanded"
- "the economy needed"
- "the technology sought"
- "incentives conspired"
- "the system decided"
- "nature designed"
- "the model wants / knows / believes / learned to deceive"
- "the algorithm figured out"
- "the institution remembered"
- "capital flowed to where it was treated best" (a metaphor doing the work of an argument)

The ML case deserves separate emphasis because it is the most common live instance. "The model learned to X" is defensible only where X is a measured behaviour on a stated eval and the sentence says so. "The model wanted to X" is never defensible.

## The post-pass check

Mandatory. Count agentless passive constructions before and after the pass.

Agentless passive means a passive with no by-phrase and no recoverable actor: "prices were observed to decline", "a decision was reached", "the threshold was lowered", "concerns were raised".

If the count rose, the pass FAILED. You removed agency instead of relocating it. Go back and apply Repair 1 or Repair 4 to the sentences you passivised.

Report as:

```
AGENCY LEDGER RESULT
  Flagged intentional/teleological subjects: 34
  Repaired by actor: 11  mechanism: 14  selection: 6  quote: 2
  Unresolved research gaps: 1
  Agentless passives before: 9   after: 7   VERDICT: PASS
```

## The personification budget

At most one deliberate, flagged personification per major section. Two conditions:

1. It is transparently figurative — no reader will mistake it for a causal claim.
2. You can state in one line what mechanism it stands in for.

An admissible one, in a piece about a legacy mainframe: "The batch window is the building's heartbeat." Stands in for: every downstream SLA is defined relative to the 02:00–05:30 job, per the operations runbook.

Example of an inadmissible one: "The market lost patience with the sector" — stands in for nothing specific, and asserts a cause.

The budget number is an operational default derived for mechanisation, not a published figure. Tune it.

## Causal claim typing

Type every causal claim before writing the sentence, and write the sentence in the grammar of its type.

| Type | Definition | Grammar requirement |
|------|-----------|---------------------|
| **MECHANISM** | A described physical, contractual, or computational pathway from X to Y | Must state the DELAY |
| **INCENTIVE** | X changed a payoff and named actors responded as documented | Must name the actors and cite the response |
| **SELECTION** | Entities doing X survived, entities not doing X exited; the population shifted with nobody deciding | Never intentional grammar |
| **CORRELATION** | X and Y moved together, pathway unknown | Sentence contains its own uncertainty and names at least one alternative explanation |
| **ATTRIBUTION** | A named participant SAYS X caused Y | Narrated as a fact about the participant, never as mechanism |

**Back-reference check.** No later reference may upgrade a claim's type. "As we saw, the fee change drove the migration" is illegitimate when the original claim was a correlation. This is the single most common integrity failure in long analytical narrative, and it is fully mechanical to detect: list every back-reference, find the original, compare types.

**Aggregate check.** Count claim types. A systems piece dominated by ATTRIBUTION claims is a piece about what people believe about the system, not about the system. Retitle it or return to the material.

## The responsibility-laundering reverse check

"The system failed" is often a sentence written to avoid naming a person who made a decision. Personifying the pathogen as an invisible enemy let governments off the hook; the same move works on boards, agencies, and engineering orgs.

Run this on every systemic attribution in the draft:

1. Quote the systemic sentence.
2. Ask: did a specific named actor have the AUTHORITY to do otherwise?
3. Ask: did that actor have the INFORMATION to know it mattered, at the time, evidenced by a document dated at or before the decision?
4. If both are yes, name them in the text. The systemic account stays; the name is added to it.
5. If authority yes and information no, say that explicitly — it is a different and more interesting finding.
6. If authority no, the systemic attribution stands, and you should say what the constraint was.

Worked example:

> Draft: "The warehouse management system had no way to flag expired lots, so expired product shipped for eleven months."
>
> Check: The 2018 vendor scoping document lists lot-expiry flagging as a deferred module, signed by the VP of operations. Authority: yes. Information: yes, the same document notes the compliance risk.
>
> Repaired: "The warehouse management system had no way to flag expired lots. The module that would have done it was scoped in 2018 and deferred by the VP of operations, whose sign-off page notes the compliance risk in one line. Expired product shipped for eleven months."

Systemic explanation must be ADDITIVE to individual accountability, not a substitute for it. The reverse also holds: naming a person does not discharge the obligation to describe the constraint that made their decision the locally rational one.

## The inevitability audit

Run over every causal sentence. Systemic narrative and hindsight are natural allies, because in retrospect we situate an action against what actually followed, while the people at the time were projecting different futures.

1. Extract every sentence containing: because, led to, resulted in, set the stage for, inevitably, was bound to, the seeds of, paved the way.
2. For each: what did the actors AT THE TIME believe would happen? Cite a contemporaneous forecast, plan, budget, or projection.
3. For each: name one live alternative genuinely available and being advocated by someone in the material.
4. If no live alternative exists, say so explicitly and give the binding reason — a physical or accounting constraint. Do not leave overdetermination implied.
5. Banned without a licence from step 3: "inevitably", "was always going to", "the writing was on the wall", "in retrospect it is obvious", "primitive", "advanced", "matured into", "the seeds of its own destruction".
6. Replace with: "happened to", "persisted given", "survived the conditions of", "no one on the desk expected".
7. Insert at least one FORECAST-VS-OUTCOME beat: a documented prediction from inside the material that turned out wrong, with the reasoning that made it reasonable at the time. This single move does more anti-inevitability work than any amount of hedging.

**Overshoot check.** Does the piece contain at least one confidently asserted "X caused Y"? If not, the brake has become hedge fog. That is not honesty, it is abdication. The correct output is a small number of confidently asserted causal claims each with its counterfactual stated, not a large number of hedged ones.

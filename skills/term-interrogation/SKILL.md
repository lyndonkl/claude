---
name: term-interrogation
description: Walks a finished document line by line, finds every word and phrase standing in for a concept, and breaks each one down until a reader with no background can follow it. Targets the assumed-knowledge phrase, the kind that sounds ordinary while hiding everything that matters ("moat", "flywheel", "product-market fit", "at scale"), not merely the rare word. Explains each term where it is used, then re-reads its own explanation and unpacks any new term that explanation introduced, repeating until every word bottoms out in ordinary language. Produces a term ledger recording what was flagged, how it was handled, where each explanation came from, and how many passes it took. Use after drafting any report, explainer or analysis for a non-expert audience, or when asked to explain something from first principles, assume the reader knows nothing, cross-question the jargon, define every term, or make a document readable by a beginner.
---

# Term interrogation

A reader who nods along and learns nothing has been failed by the writing, not by their own
attention. The words that cause it are rarely the difficult ones. Difficult words announce
themselves and get looked up. The dangerous words are the ordinary-sounding ones that carry
a whole concept quietly inside them.

"The company built a moat around its core workflow." Every word there is common English.
The sentence is still unreadable, because "moat" is standing in for an argument about why
competitors cannot take these customers away, and that argument was never made.

This skill finds those words and makes them explain themselves.

## What this skill is for, and what it is not

It runs **after** a draft exists. It is an audit and repair pass over finished prose, not a
drafting style.

It is the recursive layer above `reader-first-prose`. That skill introduces a term before
leaning on it, once. This one keeps going: it reads its own replacement text and asks
whether that text introduced something new the reader also cannot follow.

Hand off rather than duplicate:

- `reader-first-prose` for the surrounding sentence work, metaphor grounding, and the
  honesty rules.
- `ladder-of-abstraction` when a passage is abstract all the way through. That is an
  altitude problem, not a vocabulary problem. See also the density case below, which looks
  similar and is not.
- `readability-check` for scoring afterwards.

## Keep or cut: the decision that governs everything

Two moves are available for any term, and picking the wrong one is the most common way this
work goes bad.

**Keep the term and teach it** when it is real vocabulary in the field the reader is
entering. The reader will meet "moat", "gross margin", "latency" and "cohort" again the
moment they read anything else about the subject. Removing the word leaves them unable to
look it up or use it in a conversation. Teach it once and they own it.

**Cut the term and say the thing** when it is the writer's shorthand rather than the field's
vocabulary, and the reader will never need it again. "At scale", "best-in-class",
"leverage", "seamless", "robust" and "table stakes" are not concepts the reader must carry
forward. They are compression the writer chose.

The test: **will this reader meet this word again, outside this document?** If yes, keep and
teach. If no, cut and state the thing plainly.

One tiebreaker, for the boundary cases. Keep a term only if it has a **settled definition**
the reader can carry away. A live metaphor that every writer bends to their own meaning
fails this even when it recurs constantly. "Wedge" is the clearest example: readers meet it
everywhere, and teaching it would mean teaching your definition as the field's. Cut those and
say what you mean.

Never replace a precise word with a vaguer one. Swapping "amortization" for "spreading out"
scores better and teaches nothing.

```
Before:  Revenue is recognized ratably over the contract term.
Wrong:   Revenue is counted bit by bit over time.
Right:   Revenue is recognized ratably over the contract term, meaning the company counts
         an equal slice of a yearly contract in each month rather than all of it on the
         day the customer signs.
```

## The four moves

Work the document top to bottom. One pass is usually enough; the density case below is the
exception and says so.

### 1. Detect

Read every line and flag five kinds of term.

| Kind | What it looks like | Example |
|---|---|---|
| **Assumed-knowledge phrase** | Ordinary words carrying a hidden concept. The most common and most damaging | moat, flywheel, land and expand, product-market fit, network effects |
| **Domain term** | A word that plainly belongs to a field | ratably, cohort, latency, gross margin, churn |
| **Acronym or short form** | Any initialism, including ones that feel universal | ARR, NDR, TAM, SDK, DX |
| **Named entity with a role** | A company, product, standard or person whose relevance the reader cannot infer | "the Bloomberg terminal", "Section 174", "a CRDT" |
| **Vague booster** | A word that sounds like a claim and asserts nothing measurable | best-in-class, seamless, robust, optimize, leverage, at scale |

The test that finds the assumed-knowledge phrase: **can a reader outside the field restate
what this phrase asserts, or only recognise it?** A reader recognises "moat" and cannot
restate it. That gap is the tell.

Do not use "could I delete this and still make the claim" as the test. That flags every
content-bearing noun in the language, including "revenue", and tells you nothing about
whether meaning is hidden.

### 2. Interrogate

For each flagged term, answer three questions in your working notes.

1. **What does it mean here?** Not the dictionary meaning. The meaning in this sentence,
   about this subject. "Scale" means something different in a warehouse and in a database.
2. **What would the reader need to already know?** Name the prior knowledge the sentence
   assumes. That prior knowledge is what you owe them.
3. **Keep or cut?** Apply the test above.

### 3. Explain in place

Explain the term where the reader meets it, on first use only. Four ways.

**Appositive.** Shortest and least disruptive. Best for a term with a clean definition.

> ...its net dollar retention, the share of last year's revenue that this year's customers
> still spend, sits above 120%.

**Setup sentence.** For a term that needs a full sentence before it can be used.

> A cohort is a group of customers who all started in the same month, tracked together so
> their behaviour can be compared with other months. Their cohorts show...

**Concrete instance.** For a term that is genuinely abstract. Do not paraphrase it. Show one.

> ...network effects, meaning each new user makes the product better for the ones already
> there. A phone is worthless if nobody else owns one and valuable when everyone does.

Showing a particular narrows a general claim, so keep both. "The framework itself, Next.js"
preserves the general claim and grounds it; "Next.js" alone quietly shrinks what the writer
asserted.

**Cut and restate.** For shorthand the reader will not meet again.

> Before: The platform delivers best-in-class performance at scale.
> After:  The platform stays fast as a customer grows, and no competitor is measurably
>         faster.

Note what "land and expand" is doing in the Detect table above: it is listed as an
assumed-knowledge phrase, and it passes the keep test, so it gets taught rather than cut.
Being on the Detect list means "explain me", not "delete me".

**Acronyms that arrive late.** When the spelled-out form appears early and the short form
appears several sentences later, the reader's problem is connecting them, not decoding
either. Bind them at first mention: "developer experience, usually shortened to DX".

**Compound terms.** Explain the whole compound first, then any part that still does work on
its own. "Edge network economics" gets explained as a unit; "edge network" earns its own
treatment only because it appears elsewhere alone.

### 4. Recurse

This is the step every other skill skips, and it is the reason this one exists.

Read the explanation you just wrote **as though you knew nothing**. Did it introduce a new
term the reader also cannot follow? Very often it did, because the natural way to explain a
domain term is with another domain term.

```
Pass 1:  write   "a durable competitive advantage"
         read back -> "competitive advantage" is itself an assumed-knowledge phrase.

Pass 2:  write   "a reason customers keep buying from this company rather than switching
                  to a rival, that a rival cannot easily copy"
         read back -> every word is ordinary. Stop.

Two passes. "moat" is recorded in the ledger with a count of 2.
```

**Counting passes.** One pass is one write-then-read-back cycle on that term. The final
read-back that changes nothing is still a pass, because reading back is the work. A cut with
no read-back is one pass.

**Nested terms get their own row.** When explaining term A forces you to explain term B, B
becomes its own ledger entry with its own count. Term A's count stops when A's own wording
settles. Do not roll B's passes into A, or two people auditing the same document produce
ledgers that cannot be compared.

**Row it, or rewrite around it?** Run the new term through the keep test. If it passes, give
it its own row and teach it. If it fails, do not row it: rewrite your gloss to avoid it and
count another pass. "Competitive advantage" fails the test, so the moat trace above rewrites
rather than rowing it.

**Ordinary language has a floor, so name it.** Decide what this reader is assumed to know
before you start, and write it at the top of the ledger. "Code", "server" and "price" are
ordinary for most audiences; for some they are not. Without a stated floor, two auditors
produce different pass counts on the same document and neither is wrong.

**Stop when both are true:**

- Every word in the explanation is ordinary language, or has itself been explained earlier
  in the document.
- A reader who knows nothing could restate the claim in their own words.

The second condition is the one that matters. Every word can be ordinary while the mechanism
is still missing. "Cost per visitor falls" uses only common words and does not say why.

Do not keep going past that. Explaining "customer" or "price" insults the reader.

**When you pass four or five passes on one term, stop and diagnose.** Two different failures
look alike here:

- *Abstract all the way down.* Nothing concrete anywhere. Hand to `ladder-of-abstraction`
  and get a real particular. Mark the term `handed off` in the ledger and leave the best
  gloss you have rather than deleting it.
- *Too dense.* Every term is fine alone, but they arrive faster than a reader can absorb
  them. See below. This is not an altitude problem and `ladder-of-abstraction` will not fix
  it.

## When the passage is too dense to gloss in place

Explaining every term where it appears works up to roughly one flaggable term per sentence.
Past that,
the appositives pile up, the rhythm collapses, and a 95-word paragraph becomes 500 words of
interruptions.

When you notice that happening, stop glossing and **write a short orienting paragraph
first**: what this thing is, who buys it, and how it makes money, in plain words and no
jargon. Then run the pass again. Half the glosses become unnecessary, because the reader now
has somewhere to put the terms.

Length is a real constraint. A document nobody finishes has not been made readable.

**The budget covers everything the reader reads**, orienting paragraph included. Aim to stay
under about two and a half times the original. Past that, in order:

1. Write the orienting paragraph, if you have not. It is the largest single saving.
2. Move the most-repeated glosses out of the prose and into the glossary, leaving only the
   shortest appositive inline.
3. When the passage runs beyond roughly three flaggable terms per sentence, stop repairing it
   term by term. Rewrite the passage from the underlying claim, then run this pass on the
   result. Term-by-term repair assumes the sentences are worth saving, and at that density
   they usually are not.

Never buy length by weakening a kept term. If the choice is a vaguer word or a longer
document, take the longer document.

## The term ledger

Emit this alongside the revised document so the work is checkable.

```markdown
## Term ledger

Assumed reader floor: <what this reader is taken to already know, e.g. "ordinary business
English; not software, not finance">

| Term | Kind | Where | How it was handled | Source | Status | Passes |
|---|---|---|---|---|---|---|
| orienting paragraph | authored | before §1 | Added to carry what the company sells and how it earns | imported | done | 1 |
| moat | assumed-knowledge | §2, first use | Kept. Appositive: reason customers do not switch, that rivals cannot copy | document | done | 2 |
| edge network | domain | §3 | Kept. Appositive naming the machines and where they sit | mixed | done | 3 |
| at scale | vague booster | §4 | Cut. Restated as "the bigger the company, the more of it there is" | document | done | 1 |
| aggregation theory | assumed-knowledge | §5 | Best gloss kept; passage is abstract throughout | document | handed off | 5 |
| synergy | assumed-knowledge | §3 | Could not say what it means here | document | unresolved | 2 |
```

`Where` takes any locator the document supports: a section, a heading, or a sentence number.
Text you authored yourself, such as the orienting paragraph, is located relative to the
document ("before §1").

`Source` is `document` when the explanation came from the text you were given, `imported`
when you supplied the fact, and `mixed` when both. It is not optional. See the guardrail on
imported facts below.

`Status` is `done`, `handed off` (abstract throughout, passed to `ladder-of-abstraction`,
best available gloss left in place), or `unresolved` (you could not say what the term means
here, and said so).

**The orienting paragraph gets its own row.** It is the single largest importer of outside
facts in this method, since it states what the thing is and how it earns, and a jargon-dense
document usually says neither. List the facts it brought in underneath the ledger so a
reader can check them.

Also emit a **plain-language glossary**: every kept term, alphabetical, with the explanation
that survived the recursion. Include a named product or company only when the reader needs to
carry it forward; a name used once to ground a single sentence stays in the prose. The
glossary repeats the inline explanation rather than replacing it. A reader should never have
to leave the sentence to understand the sentence.

## Worked example

Before:

> Figma's moat is its multiplayer canvas. The flywheel is strong: more collaborators drive
> more seats, and the file format creates lock-in that raises switching costs at scale.

Every word is common English. A reader learns almost nothing.

After:

> Figma's **moat**, meaning the reason its customers do not switch to a rival and a rival
> cannot easily copy, is that many people can work on the same design at the same time and
> watch each other's cursors move. That advantage feeds itself, a loop often called a
> **flywheel**. A designer who invites a colleague to open a file has effectively recruited
> them, and Figma charges per person, so invitations turn into revenue. It also raises
> **switching costs**, the work a customer must do to leave. Once a company's designs sit in
> Figma's own file format, moving to a competitor means converting or rebuilding them, and
> the bigger the company, the more there is to move.

What changed, and why:

- "moat" and "flywheel" were **kept and taught**. Both are real vocabulary in this field and
  the reader will meet them again. Cutting them would leave the reader unable to follow the
  next article they read.
- "switching costs" was **kept and taught**. It is standard vocabulary in this field with a
  settled meaning, so the reader gains something they can reuse.
- "lock-in" was **cut**. It says the same thing as "switching costs" and the passage does not
  need both. When two terms name one idea, teach the one with the settled definition.
- "at scale" was **cut**. It is a vague booster hiding a real claim, which is now visible and
  arguable.
- The claim did not get weaker. It got checkable, which is what a reader needs in order to
  disagree.

## Guardrails

- **Mark every fact you import.** Explaining a term often needs a detail the document never
  stated. "Figma charges per person" and "cursors move" are true and are not in the Before.
  Adding them is allowed and often necessary. Recording them is mandatory: mark the ledger
  row `imported`. When you cannot personally vouch for the detail, fall back to a
  non-specific gloss rather than inventing a confident one. Smooth recursion on invented
  facts is more dangerous than recursion that stalls, because nothing signals the error.
- **Preserve every number, name and citation exactly.** This pass changes how a claim reads,
  never what it asserts.
- **Do not weaken a claim while simplifying it.** If the original says a company dominates a
  market, the revision says so too, in plainer words. Demote "best-in-class" to "as good as
  anyone's", not to "good".
- **Do not delete a hedge that carries real uncertainty.** "Appears to" and "on the available
  evidence" are load-bearing when the evidence is thin.
- **Explain at first use, once.** Re-explaining on every mention is condescending and makes
  the document longer without making it clearer.
- **A term you cannot explain is a term you do not understand.** When the recursion stalls
  because you cannot say what a phrase means in this context, mark it `unresolved` in the
  ledger and say so in your response. Do not write an explanation that sounds right and means
  nothing.

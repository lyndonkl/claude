# Strategist voice: annotated examples

Concrete rewrites that follow the house rules in SKILL.md. Use as reference when drafting the consolidated report. All examples are original prose; none reproduce material from the source blogs.

## Contents

- 1. Opening paragraphs
- 2. Opinion signaling
- 3. Sentence variation
- 4. The banned negation cascade
- 5. Citation form
- 6. Synthesis statements
- 7. Architecture section prose
- 8. Defining or avoiding strategy jargon
- 9. Replacing X-shaped abstractions

## 1. Opening paragraphs

### Bad: AI-default opening

> Figma is a newly-public collaborative design platform whose stated mission is to eliminate the gap between imagination and reality.

The sentence defines the company. It is also the sentence every model produces on the topic. It buys nothing.

### Good: counterintuitive frame

> Figma is now a different company than the one Adobe tried to buy. The failed acquisition handed it a billion dollars in cash, a public-market mandate, and a permission slip to attack every adjacent surface it had previously left alone. The strategist question is whether the new attack surface is worth the cost of holding the old one.

### Good: historical comparison

> Every category-winning software company eventually faces the moment when the foundation it built becomes the cage it grows inside. The browser-native multiplayer canvas that gave Figma its monopoly over UI design is now also the constraint shaping how it can respond to AI-generated product creation.

### Good: data-point hook

> Net dollar retention on Figma's enterprise customers reached 136% in Q4 2025, a ten-quarter high. The number says more about the platform thesis than any AI feature shipped that year.[^7]

## 2. Opinion signaling

### Bad: AI-prefix

> Strategist inference: Buzz is a weak product because it competes with Canva and Adobe Express on a surface where Figma has no organizational network advantage.

### Good: phrasing-signaled opinion

> Buzz is the weakest of the Config 2025 launches. The competitive set is brutal: Canva, Adobe Express, ChatGPT, Midjourney. Figma has no organizational network advantage on the marketing-asset surface and no obvious wedge into it. The more interesting question is why it shipped at all.

Note the opinion-signaling phrase ("the more interesting question is") and the absence of any prefix or hedge. The opinion is earned by the prior sentences.

## 3. Sentence variation

### Bad: identical sentence shapes

> Figma has multiple strategic bets. These bets are described in this section. The bets include canvas as source of truth, AI as substrate, and platform expansion. Each bet carries different risks.

Every sentence is subject-verb-object. Every sentence is the same length. The paragraph reads as machine output.

### Good: varied sentences with topic-forward opening

> Figma is making five bets. Two are old. Three are post-IPO, and at least one is already failing in plain view. The risk is not in any single bet; the risk is that all five are being executed simultaneously while frontier model labs ship a sixth bet against Figma's wedge.

Topic sentence first. Then a two-word sentence. Then a longer one. Then the analytical close. Rhythm.

## 4. The banned negation cascade

### Banned construction

> The canvas is the source of truth for product creation — not the codebase, not a doc, not a slide — which is operationalized through multiplayer ubiquity and aggressive enterprise expansion.

Three problems: two em dashes, the "not X, not Y, not Z" cascade, and a sentence that buries its real claim inside parentheticals.

### Acceptable rewrite (positive declarative)

> The canvas, in Figma's strategic frame, is the source of truth for product creation. Multiplayer ubiquity is how that claim becomes operational. Aggressive enterprise expansion is how it becomes revenue.

### Acceptable rewrite (one specific contrast, no cascade)

> The canvas, more than the codebase, is what Figma is betting the AI workflow flows through. Multiplayer ubiquity is how that bet is operationalized.

## 5. Citation form

### Bad: inline parenthetical interruption

> Figma's Q4 2025 revenue was $303.8M, up 40% year on year [Source: Figma IR — https://investor.figma.com/news-events/news/news-details/2026/Figma-Announces-Fourth-Quarter-and-Fiscal-Year-2025-Financial-Results/default.aspx].

The URL hijacks the paragraph. The reader's eye runs aground on the brackets.

### Good: footnoted

In the body:

> Figma's Q4 2025 revenue reached $303.8M, up 40% year on year.[^7]

In the bibliography at the report's end:

```
**Primary company material**
[^7]: Figma Investor Relations — Q4 2025 and FY 2025 results — https://investor.figma.com/...
```

## 6. Synthesis statements

### Bad: hedged-to-death

> It could be argued, perhaps, that maybe Figma's MCP server is more important than Figma Make, although both have value and the situation is complex.

This is what synthesis looks like when an agent is afraid of being wrong. The reader gains nothing.

### Good: opinion earned

> MCP, not Make, is Figma's most important AI bet. Make sits on top of frontier models that are now shipping their own design canvases. MCP occupies the protocol position the labs structurally cannot replicate without rebuilding Figma's data model. Anthropic's April 2026 response targeted Make's surface, not MCP's, which is itself the cleanest signal of where the durable moat actually lies.

The first sentence states the take in one line. The next three sentences earn it. The last sentence ties the take to a specific observable event. No hedges, no prefixes.

## 7. Architecture section prose

### Bad: technical-list prose that reads as machine-generated

> The multiplayer system uses CRDTs. It also uses Rust processes. There is one Rust process per document. The system uses DynamoDB. The system handles 2.2 billion changes per day. The system uses LiveGraph for non-canvas data.

### Good: architecture prose with analyst opinion threaded in

> Figma's multiplayer is not a true CRDT. The choice was deliberate. Server authority plus property-level last-writer-wins gives the same offline-tolerant behavior at a fraction of the operational complexity, and the company has been explicit about that tradeoff in its engineering writeups.[^3] The actual architectural moat is one layer below the protocol choice: one Rust process per active document, with a DynamoDB write-ahead journal absorbing roughly 2.2 billion property changes a day, and a separate Go service called LiveGraph that handles every non-canvas update by tailing the Postgres WAL.[^7] None of that is the sort of system a model lab could reproduce from a standing start.

Note the structure: claim, justification, the technical material, and a final sentence of analyst opinion that connects the architecture back to the competitive position. The footnotes carry the URLs.

## 8. Defining or avoiding strategy jargon

### Bad: undefined term assumed twice

> The risk of this stage is classic: companies that try to platform-expand before fully consolidating the wedge get punished when the wedge gets attacked.

A generalist reader does not know what *the wedge* is. The term carries the load-bearing claim of the sentence, and the reader has no anchor. The sentence treats the reader as already inside the conversation.

### Good: define inline on first use

> A company's *wedge* is the narrow product or customer segment it used to enter the market: in Figma's case, the lone product designer or small design team doing UI work in the browser. Companies that move on to adjacent surfaces before that wedge is unassailable tend to get punished the moment something attacks it.

The first sentence does the defining. The second sentence uses the term once it has been earned. Note that *the* is not capitalized and the definition is folded into a normal sentence.

### Even better: avoid the term entirely

> Figma is most vulnerable on its original product, the browser-native UI design canvas, not on its newer products. That original surface is what every other Figma bet rests on. It is also what Anthropic's Claude Design is targeting most directly.

The jargon is gone. The argument is the same. The reader did not have to learn a new term to follow the analysis.

## 9. Replacing X-shaped abstractions

### Bad: abstract labels doing analytical work

> The credible vision for this stage is platform-shaped and ecosystem-shaped, not feature-shaped. Figma's MCP server and Payload acquisition match that, while Buzz and Slides do not.

*Platform-shaped*, *ecosystem-shaped*, *feature-shaped* sound like they mean something. They do not. They are placeholders for a description the writer did not commit to.

### Good: concrete description

> At this stage, a credible vision looks like a base layer that other companies build on, not a single new feature. The MCP server and the Payload acquisition fit that pattern: MCP is a protocol other AI agents read from, and Payload is the backend layer underneath Figma Sites. Buzz and Slides do not fit the pattern. They are individual products competing on their own merits against Canva and Google Slides.

The concrete description ("a base layer that other companies build on") replaces three -shaped labels and tells the reader exactly what is meant. The follow-up sentences earn the categorization by showing the mechanism in each case.

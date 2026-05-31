---
name: zettel-note
description: The note-writing discipline for this vault's evergreen knowledge graph, modeled on a Zettelkasten reading companion and governed by the vault conventions. Enforces declarative-claim titles, one claim per note (atomicity), own-words prose with no block quotes, the piped [[slug|Title]] link form, the labeled link-relationship vocabulary (Confirms/Contradicts/Extends/Context/Prerequisite/Builds-on/Applies/Example-of/Contrasts-with), 3-6 links per note, and search-before-create deduplication. Use when capturing a claim as an evergreen note, refactoring a sprawling note into atomic ones, or wiring a new claim into the graph. Trigger keywords: evergreen note, zettel, atomic note, declarative title, link relationships, search before create, route the claim.
---

# Zettel note

A note in this vault is not a summary of a source — it is one claim you can defend, written in your own words, and wired to its neighbors so the graph thinks for you later. The companion model is reading-with-a-Zettelkasten: you read, you understand, you close the book, and you write the idea as if explaining it to yourself. If you cannot write it without looking, you have not understood it yet.

All mechanics here are fixed by [[conventions|Vault Conventions]] (§3 linking, §4 relationship vocabulary, §5 naming, §6 frontmatter, §7 internal structure). This skill is the *discipline* that makes a note worth linking. It is the routing target for claims drawn out in [[experiential-kolb-teaching]]: when a learner reconstructs a mechanism, it becomes an evergreen note written this way.

## The five rules

### 1. The title is a declarative claim
The title states something true that the note then defends. Not a topic, not a question, not a noun phrase — a sentence with a verb and a stance.

| Bad title (topic) | Good title (claim) |
|---|---|
| Heritability | `Heritability is a property of a population in an environment, not of a trait` |
| BLUP | `BLUP shrinks each estimate toward the population mean in proportion to how little data supports it` |
| Marker density | `Adding markers beyond linkage-disequilibrium saturation adds noise, not predictive signal` |

The slug is the title slugified: lowercased, spaces to hyphens, apostrophes and punctuation stripped, sentence structure kept (§3, §5). Long slugs are expected and fine. The title matches the note's `# H1` and its `aliases`.

### 2. One claim per note (atomicity)
A note holds exactly one idea. The tell is the word *and* in a title joining two stances, or a second paragraph that introduces a new claim instead of developing the first. When you catch it, split into two notes and link them — usually `Builds-on` or `Contrasts-with`.

> Drafting `additive-variance-drives-selection-response-and-dominance-variance-does-not`? That's two claims. Split: `selection-response-is-driven-by-additive-genetic-variance` and `dominance-variance-does-not-contribute-to-the-breeders-equation-response`, linked `Contrasts-with`.

Atomic notes are reusable: a single claim can be cited by many posts and many other claims. A compound note can be cited by none cleanly.

### 3. Own words, no block quotes
Write the claim as you would explain it out loud. No copied passages, no block quotes from the source (§7). If a phrase from the source is doing real work, paraphrase it and cite the source — the source lives in the YAML `source:` field *and* as a `Source: [[slug|Title]]` link directly under the H1 (the YAML field is invisible to the graph; the body link is what the graph sees — §3). Two to four paragraphs that develop the single claim. An optional `**Open questions:**` list is where honest edges go.

### 4. Link 3-6 times, every link labeled by relationship
Every internal link uses the piped form `[[slug|Display Title]]` — never bare `[[Title]]`, which breaks because the file on disk is the slug (§3). In the `## Links` section, label each link with its relationship from the controlled vocabulary (§4):

| Label | Means | Example use |
|---|---|---|
| Confirms | same claim, independent source | a second paper finding the same accuracy ceiling |
| Contradicts | opposing claim, productive tension | a result that says more markers *did* help |
| Extends | builds on / deepens / applies | from heritability to the breeder's equation |
| Context | background, framing | what additive variance is, for a note about response |
| Prerequisite | must hold this claim first | linkage disequilibrium, before genomic prediction |
| Builds-on | this claim assumes and develops that one | GEBV builds on the kinship matrix |
| Applies | this claim is put to work in a project/method | heritability applied in a simulation lab |
| Example-of | a concrete instance of a general claim | a maize case as an example of G×E |
| Contrasts-with | related but importantly different | narrow- vs broad-sense heritability |

Target 3-6 outbound links (§4). Fewer than three usually means the claim is orphaned or you haven't searched; more than six usually means the note is not atomic. Pick the relationship that is most *true*, not the most generic — `Context` is the lazy default; reach for `Prerequisite`, `Builds-on`, or `Contrasts-with` when they fit.

### 5. Search before you create
Before writing a new note, search the vault for the claim. The graph rots fast with near-duplicates. Run search-corpus / dedupe-against-corpus (or a plain grep over `evergreen/`) on the key terms and the claim's verb.

- If an identical claim exists: don't create. Add your new source as a `Confirms` link on the existing note, or sharpen its prose.
- If a *near* claim exists: decide whether yours is genuinely distinct. If it's a refinement, link `Extends`/`Builds-on` and make the boundary explicit. If it's the same claim said differently, merge.
- If nothing exists: create, and wire it into the closest existing notes immediately — an unlinked note is invisible.

## Worked example: routing one claim

A Kolb session lands the claim that prediction accuracy stops improving past a marker-density threshold. Write it:

```markdown
# Adding markers beyond linkage-disequilibrium saturation adds noise, not predictive signal

Source: [[wientjes-2016-marker-density-thread|Wientjes et al. — Marker Density and GS Accuracy]]

Once marker density is high enough that every causal locus is in tight linkage
disequilibrium with at least one marker, the genome is effectively "covered."
Past that point, extra markers cannot tag any new causal variation — there is none
left untagged. What they do add is estimation burden: each new column is another
effect to estimate from the same finite training set, so the model spends data
fitting noise. Accuracy plateaus, then sags.

This is why my prediction model got *worse* after I doubled the marker panel: I was
past saturation and bought only variance.

**Open questions:**
- Does the saturation point move with effective population size? (It should — Ne sets LD decay.)

## Links
- Prerequisite: [[linkage-disequilibrium-decays-with-recombination-distance|LD decays with recombination distance]]
- Builds-on: [[genomic-prediction-borrows-information-across-relatives-via-marker-tagged-ld|Genomic prediction borrows information via marker-tagged LD]]
- Contradicts: [[denser-panels-improve-accuracy-in-low-ld-populations|Denser panels help in low-LD populations]]
- Context: [[the-bias-variance-tradeoff-governs-predictive-model-error|The bias-variance tradeoff governs predictive error]]
```

Four labeled links, one atomic claim, own words, a source link under the H1, an honest open question. That note can now be cited by a post via [[experiential-kolb-teaching]]'s routing step, and surfaced for spaced review. The graph got smarter.

## Common defects to catch

- **Topic title** ("Genomic selection") -> rewrite as a claim or it can never be confirmed/contradicted.
- **Bare link** `[[Genomic prediction borrows information…]]` -> breaks; use the slug-piped form.
- **`Context` everywhere** -> you skipped the harder, truer relationship label.
- **Block quote smuggled in** -> paraphrase; the note must be yours.
- **Two claims, one note** -> split and link.
- **Created without searching** -> likely a duplicate; merge or link instead.

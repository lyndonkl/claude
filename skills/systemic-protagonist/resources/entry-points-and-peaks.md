# Entry Points and Peaks

How a reader gets into a system, and how a system that has no battle gets a climax.

## Table of Contents
- [Gateway proxies](#gateway-proxies)
- [The traveling object](#the-traveling-object)
- [The instrumented threshold scene](#the-instrumented-threshold-scene)
- [Climax by constraint violation](#climax-by-constraint-violation)
- [Institutional sense of place](#institutional-sense-of-place)
- [Node braid: when there is no single line](#node-braid-when-there-is-no-single-line)

## Gateway proxies

A human character is the reader's point of entry and emotional anchor. The subject remains the system. What makes a non-human subject relatable is a human gateway who cares about it and understands it.

This is the most useful and most dangerous technique in the set. It is the engine of the best long-form systems journalism, and it fails exactly where it is most seductive: a hero's arc replacing a structural account, with a cast selected by who agreed to talk.

### Admission test

Run per candidate. Every question must be answered before the person gets a scene.

1. **Which single line of the character sheet does this person evidence?** No line, no scene. One person, one line — a gateway assigned to three lines is a narrator, and narrators become protagonists.
2. **PROXIMITY.** Were they physically or organisationally at the point where the system's behaviour was visible? A person who heard about it is a source, not a gateway.
3. **MISCALIBRATION.** Did they start wrong and update? A gateway who was right from the start cannot dramatize learning. They can only be vindicated, which is a different and much weaker shape.
4. **DOCUMENTATION.** Is their sequence of belief states recoverable from documents created at the time — notebooks, emails, commit messages, depositions, memos, order tickets? Recovered from a later interview, a belief sequence is a memory of a belief sequence, and memory reorders toward the outcome.
5. **NON-REPRESENTATIVENESS RISK.** Would treating them as typical mislead? If yes, you must state the respect in which they are atypical.
6. **The wrongness paragraph.** Have you written the paragraph stating what this person got wrong or could not see? This is the anti-hero-arc valve and it is mandatory.
7. **Selection disclosure.** Have you stated in the text how they came to be in the story — volunteered, deposed, published, subpoenaed?

### The arc is epistemic, not moral

Write the gateway as: what they believed at t0 → what evidence hit them → what they believed at t1. The payload is the change in the model, not the change in the person.

Bad: "Chen had always known something was wrong with the settlement window, and by that spring she could no longer stay silent."

Good: "In January, Chen's own reconciliation memo attributes the breaks to a vendor timestamp bug. She reran the same query in April with the counterparty's file and found the breaks clustered on the two days a month the netting batch slipped past 16:00. Her May memo abandons the vendor theory in the first paragraph."

### Capture tests, run on the draft

**DELETION TEST.** Remove the gateway entirely. Does the systemic claim still stand on cited evidence? If not, the gateway is load-bearing and you have a character study, not a systems piece. Relabel it or go back to the material.

**RATIO TEST.** Count paragraphs of gateway interiority against paragraphs of mechanism. If interiority wins in a piece titled as a systems piece, capture has occurred.

**ABSENCE TEST.** List who declined to speak, refused, was unreachable, or was legally barred. Then check whether their absence flatters anyone. People who kept their mouths shut end up looking a lot better than their colleagues, purely because the writer's cast was assembled from volunteers. State this in the text. It is not a disclosure footnote, it is a finding about the evidence.

Sample disclosure line: "Four of the six people on the desk that quarter spoke to us. The two who did not are the two named in the consent order; nothing here should be read as evidence that the four who talked were more responsible than the two who did not."

### Borrowing a speaker

Where the subject cannot speak, borrow a speaker and attribute the interpretation by name. Some person usually has to serve the function of speaking for the phenomenon — for the aquifer, for the protocol, for the failing subsystem. Attribute it; do not let their interpretation float as narration.

Bad: "The aquifer had perhaps thirty years left."
Good: "Ruiz, who has logged the district's wells since 1994, put it at thirty years at current draw, and said the number assumes no new permits."

## The traveling object

Instead of organising by chronology or by actor, follow a single unit as it traverses the system. The system is revealed by the sequence of places the unit passes through. Movement between stations supplies the transitions for free, which is the whole reason the technique works.

The canonical newspaper instance is Rich Read's "The French Fry Connection", edited by Jack Hart, which explained the Asian financial crisis by following one load of Northwest potatoes from a Columbia Basin farm to Indonesia.

### Choosing the unit

Candidates: one container, one packet, one dollar of a fee, one blood sample, one wafer, one purchase order, one training batch, one building permit, one insurance claim, one bug report, one kilowatt-hour.

Prefer units that are (a) countable, (b) traceable in the records, (c) transformed rather than merely relocated. Choose the one whose path crosses the most boundaries between subsystems. Boundaries are where the interesting behaviour is.

### The four constraints

1. It touches at least four distinct nodes of the system.
2. At each node there is a NAMED human whose documented actions touch it.
3. Its journey spans the time period the piece needs.
4. Its representativeness is stateable with a distributional fact.

Constraint 4 is the guard against path cherry-picking. Following one atypical unit and presenting its path as the system's typical behaviour is a quiet lie of enormous leverage. Required sentence form: "Roughly 70% of orders take this path; the exceptions are covered in section 4." If you cannot state the distribution, say that you cannot.

### Station list

Map the full path as a station list. Per station record: the transformation, the price or state change, the named humans, and the LOCAL objective function of that station (which is usually not the system's).

Worked fragment, one blood sample through a diagnostic pipeline:

| Station | Transformation | Local objective function |
|---------|---------------|--------------------------|
| Draw station | Whole blood into two labelled tubes | Patients per hour |
| Courier | Tubes into a cooled tote, 40 min transit | On-time pickup rate |
| Accessioning | Tube into a record with an ID | Accessioning error rate |
| Analyser | Sample into a number | Instrument uptime |
| Result release | Number into a flagged/unflagged result | Turnaround time |
| Clinician inbox | Result into an action or no action | Inbox volume |

The system's behaviour is legible in the mismatch between the six local objective functions and the sheet's global one.

Completeness rule: follow the unit through to the point where it really matters. Do not stop at the boundary of your comfort or your sourcing. Name the last station you could verify and say why you stopped.

### The unit is a camera, not an agent

Do not give the unit intentions. "The container sought the cheapest port" reintroduces exactly the error the whole lens exists to prevent, through the back door of the device meant to avoid it. Its "point of view" means the sequence of environments it passes through, not desires. Run the agency ledger specifically over every sentence whose subject is the unit.

### GIMMICK TEST

Cut every traveling-object passage. If the explanation still stands complete, the device was decoration. Integrate it or remove it. A frame the piece returns to for atmosphere while the actual explanation happens elsewhere is worse than no frame, because it spends the reader's attention on nothing.

## The instrumented threshold scene

Abstract, slow, or diffuse forces become visible at the exact moment and place where a person or an instrument first registered them. The scene is built around the reading, the alarm, the anomalous number, the empty shelf, the first case — not around the force itself.

### Procedure

1. Search the material for FIRST-DETECTION events: the first measurement outside tolerance, the first customer complaint, the first failed settlement, the first sequenced sample, the first line in a log.
2. Choose the one with the best combination of: precise timestamp, named human present, an attached NUMBER, a documented reaction.
3. Write at instrument resolution. What did the screen, dial, spreadsheet, or shelf actually show? What were the units? What was the normal range? What did the observer do in the next ten minutes?
4. State the THRESHOLD explicitly — the value at which the reading stopped being noise. If no threshold exists in the material, say so. Do not invent one.
5. State whether the threshold is a property of the SYSTEM or of the MEASUREMENT.
6. Climb exactly ONE rung: state what the reading was a reading OF, at system scale. Then stop. Do not climb two rungs at once.

### The two failure modes

**MANUFACTURED EPIPHANY.** Wanting a scene, a writer promotes an ordinary reading into a revelation and implies the observer understood the whole system at that moment. This retro-fits later knowledge into an earlier mind. Guard: the scene may contain only what the observer could know at that timestamp, and you must be able to cite a document created at or before that timestamp showing their actual interpretation.

Bad: "At 03:12 Okafor saw the p99 spike to 4,200 ms and knew the retry storm had begun."
Good: "At 03:12 the dashboard showed p99 at 4,200 ms against a band that had not left 240–310 ms in six weeks. Okafor's first message in the incident channel, at 03:14, says 'probably the flaky node again.' The retry loop was not named until 06:40."

**THRESHOLD FETISH.** Treating one crossing as the moment the system changed, when the underlying process was continuous and the threshold was an artefact of the instrument's sensitivity. Required line, stated plainly: is this a property of the system or of the measurement? A grid frequency limit is a property of the system. A CVE severity cutoff of 7.0 is a property of the measurement.

### When the material will not support a scene

Emit `INSUFFICIENT GROUND-LEVEL MATERIAL` and downgrade to explanatory exposition. This technique requires artefacts. If the corpus is entirely secondary and abstract, attempting the scene induces invention — the model will generate plausible sensory detail fluently and verify none of it. Never generate sensory detail that is not in the source material.

## Climax by constraint violation

### The form gate comes first

Before choosing a climax, ask: does the material contain a continuous sequence of actions by a consistent set of actors with a resolution?

- **Yes** → story narrative is available.
- **No** — which is the usual case for systemic subjects → choose EXPLANATORY NARRATIVE: a narrative line with frequent digressions into abstract context. Do not force an arc.

Writers routinely have material that would be great for an explanatory narrative and try to turn it into a full-blown story narrative with an arc, a climax, and a denouement. They turn a potential silk purse into a sow's ear: great material, wrong structure. Returning "this material does not support an arc" is a successful outcome.

### The five legitimate types

| Type | Signature | Domain examples |
|------|-----------|-----------------|
| **LOOP FLIP** | A balancing loop becomes reinforcing, or vice versa | Contributor onboarding that had replaced departures starts consuming the reviewer time that made onboarding possible |
| **BUFFER EXHAUSTION** | A slack resource reaches zero | Ward beds, spare transformers, chassis pool, maintainer hours, deferred-maintenance budget |
| **CONSTRAINT BINDING** | A limit that never mattered starts setting the outcome | Interconnection queue length replaces land cost as the thing that decides where generation gets built |
| **IRREVERSIBILITY** | An option is destroyed | A plant closes, a signing key is lost, a format locks in, a seed bank burns, the last person who understood the batch job retires |
| **LEGIBILITY** | The stated/revealed gap becomes undeniable to insiders, evidenced by a document | The internal deck that states the real objective function in plain language |

Whichever type you pick, stage it as an instrumented threshold scene: specific timestamp, specific place, specific number, specific named witness.

### The tests

**TRANSFER-FUNCTION TEST.** After the climax, do the same inputs produce different outputs? If no, it is a scene, not a climax, and the piece should be explanatory rather than dramatic. State the before and after transfer function explicitly in your working notes:

```
Before: a 200-basis-point rate move produced 3-5 days of elevated settlement fails
After:  the same move produces 12-20 days, because the two dealers who absorbed
        the imbalance in 2019 no longer make markets in the instrument
```

**ARC-FORCING CHECK.** The most common manufacture is promoting a person's dramatic moment into the system's turning point. That produces hero/villain flattening of a diffuse process. Ask: did the system's behaviour change, or did one person's day change?

**FAMOUS-DATE CHECK.** Are you using a well-known date because it is well known? Check whether the state transition actually happened earlier and less visibly. The famous date is usually the day the transition became public, which is a fact about disclosure, not about the system.

### Denouement

Do not resolve. Re-state the new steady state: what is the objective function now, and what does the system now do to the same inputs?

Refuse the prescriptive ending. Closing checklists of solutions are usually self-contradictory and usually not in the material. If the material genuinely contains a remedy that was tried and held, that is a finding and belongs in the reform-attempt ledger, not in a closing sermon.

## Institutional sense of place

Abstract power is rendered by describing, at physical resolution, the rooms and objects and geographies where it operated.

1. For each key decision or state change, locate the PHYSICAL SITE: the room, the floor, the terminal, the exchange, the plant, the server hall.
2. Interrogate the material with the literal extraction prompt — WHAT WOULD I SEE? — against transcripts, depositions, memoirs, photographs, floor plans, filings. Extract: light, sound, who sat where, what was on the walls, what the paperwork physically looked like, how long the walk was, what was on the screens.
3. Render the site BEFORE the decision, so the reader occupies the space in which it was made.
4. Show power through the powerless. Find the person at the far end of the system's output and let them testify in their own words at ground level.
5. For a number too large to feel, give it a FORM — a list, a catalogue, a physical comparison — not an adjective.

**LOAD-BEARING TEST.** For each descriptive passage, name the character-sheet line it evidences or the comprehension problem it solves. Neither, cut. Otherwise you get set dressing: novelistic padding around a thin analysis.

**SYNECDOCHE GUARD.** Pair every ground-level testimony with the distributional fact. One vivid case standing for a heterogeneous distribution is a real distortion, and it is undetectable to the reader. "Of the roughly 250,000 displaced, this block's experience was typical in X and atypical in Y."

Never let the place description carry an argument the evidence does not support. The site's job is to make the reader present, not to imply guilt by décor.

## Node braid: when there is no single line

For a system with no single storyline, compose the piece from viewpoint nodes — people, places, instruments, documents, transactions — braided rather than sequenced.

1. **Centrepiece first.** The single most consequential moment or state of the system. Everything else is positioned relative to it.
2. **Inventory nodes.** Per node: which character-sheet line it evidences, its time coordinate, its scale (individual / firm / market / era), its viewpoint holder.
3. **Reject** any node duplicating an admitted node's character-sheet line without adding a new scale or a new time.
4. **Group into three or four strands**, each with a stated job. Usual set: MECHANISM, HUMAN CONSEQUENCE, CHRONOLOGY, and optionally COUNTER-EVIDENCE. Fewer than three collapses into a linear report; more than four exceeds reader tracking.
5. **Question pairs at every cut.** Write, before drafting, the question the previous strand raised and the question the new one opens. No cut without a question pair.
6. **Re-orientation clause** in the first sentence of every strand switch: time, place, strand.
7. **Name the convergence beat** in advance. If you cannot name the beat where all strands meet, they are parallel, not braided, and the piece will read as three articles stapled together.

**ORPHAN CHECK.** Any strand appearing fewer than three times, or absent from the final third, is orphaned. Promote it or cut it entirely.

**ADJACENCY CHECK.** For any two adjacent nodes from different causal domains, state explicitly whether a causal link is being claimed. Unstated adjacency will be read as causation. Placing a node about a layoff next to a node about a stock buyback claims something whether you meant it or not.

**NO SCAFFOLDING IN THE PROSE.** Strand labels, node IDs, and "as we saw above" are planning instruments. They must not appear in the finished text. Readers are not supposed to notice the structure; a piece that shows its braid reads as an outline that learned to talk.

The strand counts and appearance minimums here are operational defaults derived for mechanisation, not published figures.

# Knowledge base — corporate finance and valuation

This is the source material the finance agents and skills were built from, and the record of
how the design decisions were reached. Nothing here loads at runtime. The agents and skills
carry their own instructions; this exists so a reader can check where a rule came from.

It was distilled from Aswath Damodaran's NYU Stern courses: the corporate finance and
valuation lecture packets, the accounting and foundations-of-finance sessions, the graded
student projects, and his public spreadsheet models.

## The four layers

Each layer compresses the one below it. Read top-down to understand the system; read
bottom-up to audit a claim back to the page it came from.

| Layer | Directory | Contents |
|---|---|---|
| Playbooks | `frameworks/` | 6 documents. The operating procedures the agents follow. |
| Concepts | `concepts/` | 362 notes in 17 areas. One idea each, with formula, procedure and worked example. |
| Model docs | `spreadsheets/` | 23 documents covering 51 of Damodaran's spreadsheets, reverse-engineered to their formulas and reference tables. |
| Page notes | `pages/` | 84 files covering all 2,424 pages of 37 lecture PDFs. Every page has a note. |

`architecture/SPEC.md` is the binding specification for the agent system: the analysis
modes, the workspace layout, the gates, the artifact contracts, and the agent roster.

`tools/` holds the scripts that built and verified the extraction, including the coverage
checker that confirms every page is accounted for.

## The playbooks

| File | What it governs |
|---|---|
| `special-situations-routing.md` | The routing tree. Classifies a company, picks the engine, and compiles the 28 hard constraints that bind every later stage. |
| `intrinsic-valuation-playbook.md` | The end-to-end discounted cash flow pipeline, with its consistency rules and circularity register. |
| `corporate-finance-playbook.md` | Governance, returns on investment, financing mix, payout policy, and how each changes value. |
| `pricing-playbook.md` | Relative valuation against peers and the market, plus asset-based approaches. |
| `data-requirements.md` | Every external input an analysis needs, where it comes from, and the fallback when it is missing. |
| `deterministic-inventory.md` | 84 computation modules with their dependencies. This is what decided which capabilities became Python scripts. |

## How a concept note is structured

Every note carries the same fields, and one of them drove the whole architecture:

- **Core idea** — what it is and why it matters
- **Formulas** — with every symbol defined
- **Procedure** — numbered steps for applying it to a real company
- **Reference data** — the lookup tables needed
- **Worked example** — real numbers from the source
- **Determinism** — which parts a script can compute, and which need judgment
- **Pitfalls** — the mistakes the source warns about
- **Sources** — the exact pages the note came from

The **Determinism** field is the one that mattered most. Sorting every concept into
"a script could do this" against "this needs a person to reason" is what produced the split
between the computation skills and the agents. The routing playbook states the finding
plainly: the arithmetic is almost always mechanical; the inputs almost never are.

## Provenance

Page notes cite their source as `<document-slug> p.<N>`, where the page number is the
physical page of the PDF. Concept notes list every page that fed them. So any rule in a
playbook can be traced down through the concept that carries it to the lecture pages
behind it.

Three PDFs in the source folder were byte-identical duplicates of others and were excluded,
which is why the page count is 2,424 rather than the raw total.

## Vintage

The lecture material is from the Spring 2020 and Spring 2021 courses. Where the two
editions teach the same concept with different data years, the notes merge them and prefer
the 2021 figures.

Reference tables extracted into the skills — rating spreads, country risk premiums,
industry averages — carry their own `as_of` dates and should be refreshed annually from
Damodaran's site rather than trusted indefinitely.

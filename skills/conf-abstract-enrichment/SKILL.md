---
name: conf-abstract-enrichment
description: Thicken a thin or missing conference-session abstract through targeted web research so short, noisy text becomes classifiable — pulling the speaker's recent work, the linked repo or paper, and the company/product to add signal. Every enriched claim carries provenance (source URL + retrieval date) and a confidence, the enriched text is stored separately from the original (never overwriting it), and enrichment is gated so already-rich abstracts are left alone. Conference-agnostic. Use when an event record has been flagged thin by program extraction, when a session lacks enough text to classify, or when a key axis (depth, topic) is low-confidence. Trigger keywords - abstract enrichment, thicken abstract, enrich session, speaker research, thin abstract, runtime web search for talks.
---

# Conference Abstract Enrichment

Most of what a scheduler needs to know about a talk is not in its abstract, because the abstract is short, sometimes missing, and written to attract an audience rather than to be classified. This is the one stage in the pipeline where **runtime web search earns its keep**: a one-line blurb plus the speaker's recent work, the linked GitHub repo, and the sponsoring company is often enough to recover the topic, depth, and stakes that the program left out.

Enrichment is powerful and therefore dangerous. Unconstrained, it invents plausible detail, over-enriches talks that were already fine, and launders a guess into the record as if it were sourced. This skill keeps it honest with four rails: a **gate** (only enrich what is actually thin), a **source-priority ladder** (search the most reliable signal first), **mandatory provenance** (every claim names where it came from), and **separation** (enriched text never overwrites the original — it lives beside it so the source of truth survives).

The output is an **enrichment record** written to the side; the ingestor merges it back into the event. Enrichment never edits the program's own words and never reclassifies on its own — it supplies *better text and clearer axis signals* with sources, and lets extraction/clustering do the classifying.

## The enrichment record (output contract)

One JSON file per event, written to `enrichment/{event_id}.json`. Canonical — reproduce these field names.

```json
{
  "event_id": "matches the EventRecord id",
  "gated_out": false,
  "abstract_enriched": "string | null",
  "axis_updates": {
    "topic": ["string"],
    "depth": { "value": "intro | intermediate | advanced | unknown", "confidence": 0.0, "basis": "string" },
    "prerequisites": { "value": ["string"], "confidence": 0.0, "basis": "string" }
  },
  "sources": [ { "url": "string", "claim": "what this source supports", "retrieved_on": "YYYY-MM-DD" } ],
  "confidence": 0.0,
  "searches_used": 0,
  "searches_cap": 4,
  "capped": false,
  "notes": "string"
}
```

When the gate rejects an event (already-rich abstract), write `gated_out: true`, leave `abstract_enriched: null` and `axis_updates: {}`, and stop — the record still exists so the merge step and any audit can see the decision was made deliberately, not skipped silently.

## Common Patterns

### Pattern 1: Gate first — only enrich what is thin

Before any search, check whether enrichment is warranted. Enrich when **any** of:
- the abstract is `null`, "TBA", or below the thinness threshold (~25 words / no concrete nouns), **or**
- a load-bearing axis (`depth`, `topic`) is below ~0.4 confidence and the talk is a plausible schedule candidate.

Otherwise `gated_out: true`. Enriching a rich abstract burns searches and invites a substitution effect — the model "improves" text that was already the best signal, drifting it toward whatever the web says about the speaker rather than what *this* talk is about. The cheapest correct enrichment is the one you correctly decline to do.

### Pattern 2: Search the source-priority ladder, in order

Spend the search budget on the most reliable signal first, and stop as soon as you have enough to classify:

1. **Linked artifact** — a repo, paper, slides, or product page referenced in the title/abstract. Most reliable: it is the talk's actual subject matter.
2. **Speaker's recent work** — their last talk, blog post, or paper on the same theme. Strong signal for depth and angle.
3. **Company / product** — what the org builds, when the talk is a vendor/sponsor session. Recovers the domain.
4. **Track context** — the track's theme as a weak prior, only to disambiguate.

Each rung is a fallback for the rung above, not an additive sweep. If rung 1 fully resolves the talk, do not run rungs 2–4.

### Pattern 3: Capture provenance for every claim

Every sentence of `abstract_enriched` and every `axis_update` must trace to a `sources[]` entry: the URL, the specific claim it supports, and the retrieval date. A claim you cannot source does not go in the record. Provenance is what makes enrichment auditable and what lets a later stage discount it appropriately — an inferred-from-the-web `advanced` is not the same as one stated in the program, and the record must show the difference.

### Pattern 4: Distinguish "enriched from a source" from "inferred"

Two different operations, two different confidences:
- **Sourced**: a page states the fact ("the repo README says this is a hands-on workshop assuming PyTorch"). Confidence `0.6–0.85`.
- **Inferred**: you reason from sourced facts to a new claim the sources do not state. Confidence `0.3–0.5`, basis names the inference.

Never promote an inference to a sourced claim. When sources conflict or are silent, return the **lower** confidence rather than picking a side — uncertainty is information the scheduler can use; a confident wrong answer is not.

### Pattern 5: Cap searches and log the cap

Set a per-event search budget (default 4) and stop when it is spent, even if more could be found. Record `searches_used`, `searches_cap`, and `capped: true` when you hit the ceiling. This is the no-silent-truncation rule: a talk that was under-researched because the budget ran out must say so, so the pipeline does not mistake "capped" for "nothing more to find."

## Workflow

```
□ Step 1: Apply the gate. If the abstract is already rich and axes are confident, write
          gated_out: true and stop.
□ Step 2: Identify candidate sources from the title/abstract (linked artifact, speaker, company).
□ Step 3: Walk the source-priority ladder, newest-and-most-specific first, within the search cap.
□ Step 4: Draft abstract_enriched — only sentences each backed by a sources[] entry.
□ Step 5: Derive axis_updates (topic/depth/prerequisites) with confidence + basis; mark
          sourced vs inferred.
□ Step 6: Set the record confidence (the weakest link of the claims you are asserting).
□ Step 7: Record searches_used / capped; write enrichment/{event_id}.json. Return the path.
```

## Guardrails

### 1. Don't over-enrich
**Danger**: Improving an already-good abstract drifts it toward the speaker's general reputation and away from this talk.
**Guardrail**: The gate is mandatory. Default to `gated_out` when in doubt.
**Red flag**: An enrichment record for a talk whose original abstract was three solid sentences.

### 2. Provenance is non-negotiable
**Danger**: A sourceless claim is indistinguishable from a hallucination.
**Guardrail**: No claim without a `sources[]` entry. If you cannot cite it, it does not go in.
**Red flag**: `abstract_enriched` longer than what the `sources` actually support.

### 3. Never overwrite the original
**Danger**: Losing `abstract_raw` makes the enrichment unauditable and irreversible.
**Guardrail**: Write to the side (`abstract_enriched`); the ingestor merges without touching `abstract_raw`.

### 4. Sourced ≠ inferred
**Danger**: Inferences laundered as facts inflate downstream confidence.
**Guardrail**: Tag each claim; inferred claims cap at ~0.5. Conflicting/absent sources ⇒ return lower confidence, not a coin flip.

### 5. Respect and log the cap
**Danger**: Silent truncation reads as completeness.
**Guardrail**: Stop at the budget; set `capped: true`. A capped record is honest about being partial.

### 6. Don't reclassify or schedule
**Danger**: Scope creep into clustering/scheduling.
**Guardrail**: Supply better text + axis *signals* with sources; let `conf-program-extraction`/`conf-theme-clustering` own the classification and `conf-schedule-optimization` own the picks.

## Quick Reference

### Source-priority ladder

| Rung | Source | Recovers | Reliability |
|---|---|---|---|
| 1 | Linked repo / paper / slides | exact subject, depth, prereqs | highest |
| 2 | Speaker's recent work | angle, depth, recurring themes | high |
| 3 | Company / product | domain, vendor context | medium |
| 4 | Track theme | coarse topic prior | low (disambiguation only) |

### Confidence rubric

| Claim type | Confidence | Rule |
|---|---|---|
| Stated by a primary source | 0.6–0.85 | URL + claim recorded |
| Inferred from sourced facts | 0.3–0.5 | basis names the inference |
| Conflicting / absent sources | ≤ 0.3 | return low, do not pick a side |
| Gated out (already rich) | n/a | `gated_out: true`, no claims |

## Related Skills

- **conf-program-extraction**: produces the thin-abstract flags and low axis confidences that gate this skill in; defines the EventRecord whose fields the merge updates.
- **scout-mindset-bias-check**: guards against confirming the topic/depth you expected to find rather than the one the sources support.
- **reference-class-forecasting**: for axis claims better made from a base rate (e.g., "vendor lightning talks are usually intro") than from this one listing.
- **conf-theme-clustering**: the immediate consumer of richer abstracts and recovered topics.

## Examples in Context

### Example 1: Missing abstract, linked repo

Event: "Claude Managed Agents Workshop (Part 1) — Priyanka Phatak, Gabriel Cemaj"; abstract: "Build an agent with Claude Managed Agents" (thin). Gate: **enrich**.
- Rung 1: the workshop's linked repo README states it is a hands-on lab assuming familiarity with the Agents SDK and Python.
- `abstract_enriched`: two sentences, each cited to the README.
- `axis_updates.depth`: `{value:"intermediate", confidence:0.7, basis:"README states 'assumes Agents SDK familiarity'"}` (sourced).
- `axis_updates.prerequisites`: `{value:["Agents SDK basics","Python"], confidence:0.7, basis:"README prerequisites section"}`.
- `confidence`: 0.7; `searches_used`: 1; `capped`: false. Resolved on rung 1 — ladder stops.

### Example 2: Sources silent — stay uncertain

Event: "Sponsor Lightning — TBA" (expo). Gate: enrich (no abstract). Rungs 1–3 find only a generic company landing page; nothing about *this* talk.
- `abstract_enriched`: null (nothing sourceable about the session itself).
- `axis_updates.topic`: `["unknown"]` left as-is; `notes`: "company page found, no session-specific content".
- `confidence`: 0.2; `searches_used`: 3. The record correctly reports that enrichment was attempted and came back thin — better than a confident fabrication about a lightning talk that has no published content.

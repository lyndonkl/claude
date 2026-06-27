---
name: conf-program-extraction
description: Parse a heterogeneous conference program (markdown, HTML, PDF-derived text, or JSON) into normalized event records with per-field confidence scores and independent classification axes (topic, depth, format, prerequisites, recorded, capacity). Detects the program's format before extracting, treats every inferred field as uncertain (present vs inferred vs missing), and flags thin or missing abstracts so downstream enrichment can target them. Conference-agnostic. Use when ingesting a conference or event schedule into a structured store, normalizing a talk/session list, or extracting per-session metadata with calibrated confidence. Trigger keywords - program ingestion, parse schedule, session extraction, event records, conference program, talk metadata, per-field confidence.
---

# Conference Program Extraction

A conference program is the noisiest structured document you will routinely parse. Formats differ between conferences and often between *days* of the same conference; abstracts are short, frequently missing, and written to sell rather than to classify; and the fields a downstream scheduler needs most — how advanced a talk is, whether it is recorded, whether it has a capacity cap — are almost never stated outright. They have to be *inferred*, and an inference you cannot tell apart from a fact is a liability.

This skill turns raw program text into **normalized event records** in which every field carries a **calibrated confidence** and a one-line **basis**, and in which the classification signal is split into **independent axes** rather than crushed into a single blob. The governing principle is honest uncertainty: a record should make it obvious to the next stage which fields are solid, which are guessed, and which are simply absent.

It does three jobs and stops: **detect the format**, **extract into the schema**, **score the confidence**. It does not enrich thin abstracts (that is `conf-abstract-enrichment`), cluster (that is `conf-theme-clustering`), or schedule. It only flags what is thin so the next agent knows where to spend effort.

## The event record (output contract)

The output is a single JSON file with a `meta` block (so an orchestrator can verify the stage gate without parsing every record) and an `events` array. This schema is canonical — reproduce it exactly; downstream skills read these field names.

```json
{
  "meta": {
    "conference_id": "string",
    "source_ref": "path or url of the parsed program",
    "generated_on": "YYYY-MM-DD",
    "counts": { "total": 0, "talk": 0, "workshop": 0, "keynote": 0, "panel": 0, "other": 0 },
    "confidence_rollup": {
      "mean_field_confidence": 0.0,
      "low_confidence_field_fraction": 0.0,
      "events_with_thin_abstract": 0
    },
    "status": "done | partial",
    "format_detected": "short description of the delimiter/heading pattern used"
  },
  "events": [
    {
      "id": "kebab slug, day+time+speaker+title-stub, e.g. d2-0900-laurie-voss-vibes-to-production",
      "title": "string",
      "speakers": [ { "name": "string", "affiliation": "string | null", "affiliation_confidence": 0.0 } ],
      "session_type": "talk | workshop | keynote | panel | sponsor | expo | unknown",
      "track": "string | null",
      "room": "string | null",
      "day": "YYYY-MM-DD | null",
      "start": "HH:MM | null",
      "end": "HH:MM | null",
      "abstract_raw": "string | null",
      "abstract_enriched": null,
      "axes": {
        "topic": ["string"],
        "depth":      { "value": "intro | intermediate | advanced | unknown", "confidence": 0.0, "basis": "string" },
        "format":     { "value": "talk | workshop | keynote | panel | unknown", "confidence": 0.0, "basis": "string" },
        "prerequisites": { "value": ["string"], "confidence": 0.0, "basis": "string" },
        "recorded":   { "value": true, "confidence": 0.0, "basis": "string" },
        "capacity_constrained": { "value": true, "confidence": 0.0, "basis": "string" }
      },
      "enrichment": null,
      "field_confidence": {
        "title": 1.0, "speakers": 0.0, "track": 0.0, "room": 0.0, "time": 0.0, "abstract": 0.0
      },
      "source_ref": "the raw heading or line range this record came from"
    }
  ]
}
```

`abstract_enriched` and `enrichment` are written as `null` here and left for `conf-abstract-enrichment` to fill. `recorded` and `capacity_constrained` use `null` for the `value` when there is genuinely no signal either way (and confidence `0.0`).

## Common Patterns

### Pattern 1: Detect the format before you extract

**Never assume a fixed format.** Read a representative slice first and identify the *recurring shape*: the heading level that delimits a session, the field order, the inline metadata convention, the grouping (by day, by track, by time). Write what you found into `meta.format_detected`. Only then extract.

A typical session line looks like one of:

```
#### 9:00am-11:00am: From Vibes to Production — Laurie Voss
(sponsor) [Track 1] | Track: Track 1 | Status: tentative
<abstract paragraph or "TBA">
```

The reusable move: derive a small set of regexes/anchors from the *detected* pattern (time anchor, title/speaker split on the em dash, the `(type) [room] | Track: x` metadata line), not from a format you remember from another conference. When a later day breaks the pattern, re-detect rather than forcing the old anchors.

### Pattern 2: Extract independent axes, not one blob

A talk is not a single label. Separate the signal into axes that vary independently, because the scheduler and the elicitor will query them independently:

- **topic** (`["evaluation","agents","rag"]`) — what it is about. Multi-valued by default.
- **depth** (`intro|intermediate|advanced`) — how much prior knowledge it assumes.
- **format** (`talk|workshop|keynote|panel`) — how it is delivered.
- **prerequisites** — concrete things the attendee should already know/have.
- **recorded** — whether they can catch it later (changes its scheduling priority).
- **capacity_constrained** — whether a seat is guaranteed (workshops usually are not).

The point of separation: "advanced workshop on RAG eval, recorded, capacity-capped" is four orthogonal facts, each with its own confidence. A blob throws away the ability to say "I'm confident it's a workshop but only guessing it's advanced."

### Pattern 3: Confidence is present vs inferred vs missing

Every field lands in one of three states, and the confidence number must reflect which:

- **Present** — stated verbatim in the program (the title, the time, an explicit "Advanced" tag). Confidence `0.9–1.0`.
- **Inferred** — derived from a real signal but not stated. "Workshop" ⇒ `format=workshop` (strong, `~0.85`); "required prerequisites" in the abstract ⇒ `depth=advanced` (moderate, `~0.6`); session in a "101" track ⇒ `depth=intro` (moderate). Confidence `0.3–0.8` with the **basis** naming the signal.
- **Missing** — no signal at all. `value: null`/`unknown`, confidence `0.0`, basis `"absent"`.

The basis string is not decoration; it is what lets a human or the elicitor audit a low-confidence schedule decision later ("depth: advanced (0.6, inferred from 'assumes familiarity with embeddings')").

### Pattern 4: Flag thin or missing abstracts — but do not fill them

Mark an abstract **thin** when it is absent, "TBA", or too short/generic to classify from (a rough rule: under ~25 words, or no concrete nouns a topic could attach to). Record this in two places: a low `field_confidence.abstract`, and the `meta.confidence_rollup.events_with_thin_abstract` count. Do **not** web-search or invent text — that is `conf-abstract-enrichment`'s job, and keeping the boundary clean is what lets enrichment carry its own provenance and confidence.

### Pattern 5: Handle parallel tracks and ambiguous times

Conferences run many rooms at once, so the same start time appears repeatedly across the program. That is expected — do **not** dedupe by time. Each `(time, room)` pair is a distinct event. Capture `room` whenever present (it is what the scheduler turns into travel-time and overlap constraints). When a time is a range, fill both `start` and `end`; when only a start is given, leave `end: null` rather than guessing a duration.

## Workflow

```
□ Step 1: Read a representative slice of the program; identify the recurring session shape.
□ Step 2: Record the detected format in meta.format_detected; derive extraction anchors from it.
□ Step 3: Walk the program in document order, emitting one EventRecord per session.
□ Step 4: For each record, fill the present fields verbatim with high confidence + source_ref.
□ Step 5: Infer the axes (depth/format/prereqs/recorded/capacity/topic) from real signals;
          attach confidence + a one-line basis to each; use null/unknown + 0.0 where absent.
□ Step 6: Score field_confidence per field; mark thin/missing abstracts.
□ Step 7: Mint a stable, collision-resistant id (day+time+speaker+title-stub, kebab-case).
□ Step 8: Compute meta.counts and meta.confidence_rollup; set status (done | partial).
□ Step 9: Write the {meta, events} JSON; write a human-readable index.md alongside it.
```

## Guardrails

### 1. Never fabricate a field
**Danger**: A null abstract or unknown room becomes a plausible-sounding guess that the scheduler then trusts.
**Guardrail**: Missing ⇒ `null`/`unknown` + confidence `0.0` + basis `"absent"`. The only text in `abstract_raw` is text that was in the program.
**Red flag**: You wrote a sentence no source contained.

### 2. Calibrate confidence honestly
**Danger**: Everything gets `0.9`, so the confidence signal carries no information and the elicitor/scheduler cannot tell solid from guessed.
**Guardrail**: Verbatim ⇒ `0.9–1.0`; strong inference ⇒ `0.6–0.85`; weak inference ⇒ `0.3–0.55`; absent ⇒ `0.0`. If you cannot name the basis, the confidence is low.
**Red flag**: A field marked `0.9` whose basis is "seemed right".

### 3. Inferred is not Present is not Missing
**Danger**: Collapsing the three states loses exactly the information downstream stages need.
**Guardrail**: Keep them distinct in both the value and the confidence. An inferred `advanced` and a stated `Advanced` must not look identical in the record.

### 4. Preserve the source reference
**Danger**: A wrong extraction is unauditable.
**Guardrail**: Every record keeps `source_ref` (the raw heading or line range). A human can always trace a record back to the program.

### 5. Don't collapse multi-topic talks
**Danger**: "Evaluating agentic RAG" filed under one topic disappears from two of the three interests it actually serves.
**Guardrail**: `axes.topic` is a list; populate all genuine topics. (Soft cross-theme membership is `conf-theme-clustering`'s job, but it can only do it if the topics survive extraction.)

### 6. Don't dedupe parallel sessions
**Danger**: Treating repeated start times as duplicates deletes real concurrent talks.
**Guardrail**: One record per `(time, room)`. Same time, different room = two events.

## Quick Reference

### Axis extraction table

| Axis | Values | Typical basis (when not stated) | Usual confidence |
|---|---|---|---|
| topic | list of strings | title + abstract nouns | 0.5–0.9 |
| depth | intro / intermediate / advanced / unknown | "101"/"intro" wording, stated prereqs, jargon density | 0.3–0.7 |
| format | talk / workshop / keynote / panel | session_type tag, "workshop"/"lab" in title, duration | 0.7–0.95 |
| prerequisites | list of strings | explicit "prerequisites"/"assumes" phrasing | 0.3–0.8 |
| recorded | true / false / null | conference-wide policy (from config), "not recorded" notes | 0.0–0.6 |
| capacity_constrained | true / false / null | workshop/lab ⇒ likely true; main-stage talk ⇒ false | 0.3–0.8 |

### Confidence rubric

| State | Definition | Confidence | Example |
|---|---|---|---|
| Present | Stated verbatim | 0.9–1.0 | Title; "Advanced" tag; explicit time |
| Strong inference | One clear signal | 0.6–0.85 | `(workshop)` ⇒ format=workshop |
| Weak inference | Indirect signal | 0.3–0.55 | dense jargon ⇒ depth=advanced |
| Absent | No signal | 0.0 | room not listed ⇒ room=null |

## Related Skills

- **conf-abstract-enrichment**: thickens the thin abstracts this skill flags, with its own provenance and confidence. The handoff is the `events_with_thin_abstract` flag plus low `field_confidence.abstract`.
- **conf-theme-clustering**: consumes `axes.topic` and abstracts to build the theme map; relies on multi-topic survival.
- **scout-mindset-bias-check**: a discipline check against motivated extraction (seeing the depth/topic you expect rather than the one the text supports).
- **reference-class-forecasting**: useful when inferring `capacity_constrained`/`recorded` from a base rate for the session type rather than this specific listing.

## Examples in Context

### Example 1: A rich session line

Input:
```
#### 9:00am-11:00am: From Vibes to Production: Evaluating and Shipping AI Agents That Work 101 — Laurie Voss
(sponsor) [Track 1] | Track: Track 1
Building an AI demo is easy. Knowing whether it works in production — and keeping it working — is the hard part. Hands-on: build an eval harness...
```

Record (abbreviated):
- `title`: "From Vibes to Production: Evaluating and Shipping AI Agents That Work 101" — confidence 1.0
- `speakers`: `[{name:"Laurie Voss", affiliation:null, affiliation_confidence:0.0}]`
- `session_type`: "sponsor"; `room`: "Track 1"; `track`: "Track 1"; `start`:"09:00", `end`:"11:00" — all Present
- `axes.depth`: `{value:"intro", confidence:0.6, basis:"'101' in title"}`
- `axes.format`: `{value:"workshop", confidence:0.75, basis:"'Hands-on: build...' + 2h block"}`
- `axes.topic`: `["evaluation","agents","production","observability"]`
- `field_confidence.abstract`: 0.9 (rich); not flagged thin.

### Example 2: A sparse expo session

Input:
```
#### 2:30pm: Sponsor Lightning — TBA
(expo) [Expo Stage NE]
```

Record:
- `title`: "Sponsor Lightning" — 1.0; `speakers`: `[]`; `session_type`:"expo"; `room`:"Expo Stage NE"; `start`:"14:30", `end`:null
- `abstract_raw`: null; `field_confidence.abstract`: 0.0 — **flagged thin** (counts toward `events_with_thin_abstract`)
- `axes.depth`: `{value:"unknown", confidence:0.0, basis:"absent"}`
- `axes.capacity_constrained`: `{value:false, confidence:0.5, basis:"expo stage, open seating"}`
- Everything unsupported stays `null`/`unknown` at confidence `0.0` — the record advertises its own thinness rather than hiding it.

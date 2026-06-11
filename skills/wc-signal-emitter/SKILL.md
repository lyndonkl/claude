---
name: wc-signal-emitter
description: Validates and persists FIFA World Cup Fantasy signal files to signals/YYYY-MM-DD-<type>.md. Checks the required frontmatter (type, round, date, emitted_by, confidence, source_urls), range-checks declared numeric signals, confirms every factual claim carries a source URL or "manager-provided", rejects unknown signal types, and refuses to persist a signal that fails validation (logging the failure instead). Keeps the inter-agent signal layer auditable so downstream agents can trust what they read and never re-derive it. Use whenever an agent or skill writes a signal.
---

# wc-signal-emitter — validate + persist signals

Implements the persistence side of `footballfantasy/context/frameworks/signal-framework.md`. Agents communicate through structured signal files; this skill is the gate that keeps those files trustworthy, so downstream agents can read rather than recompute.

## Workflow
```
- [ ] 1. Receive the signal (frontmatter + body) and its declared type
- [ ] 2. Validate frontmatter, type, numeric ranges, source citations
- [ ] 3. If valid → write to signals/YYYY-MM-DD-<type>[-<scope>].md and return the path
- [ ] 4. If invalid → do NOT persist; return the validation errors so the caller can fix and retry
```

## Validation checklist
- **Frontmatter present:** `type`, `round`, `date`, `emitted_by`, `confidence` (0–1), `source_urls`.
- **Type known:** one of the registry in `signal-framework.md` (`scout`, `player-ev`, `clean-sheet`, `fixture`, `ownership`, `candidate`, `fitness`, `offspring`, `verify`, `chip-plan`, `transfer-plan`, `board`). Reject unknown types.
- **Numeric ranges:** any signal that declares a range is checked against it (probabilities ∈ [0,1]; ownership ∈ [0,100]; xEV ≥ 0; confidence ∈ [0,1]). Out-of-range → reject.
- **Citations:** every factual claim in the body traces to a `source_urls` entry or is explicitly `manager-provided`. A signal asserting a predicted XI / injury / price / ownership with no URL → reject (or force `confidence ≤ 0.35` and a "needs confirmation" flag if the caller insists it's a best-effort estimate).
- **Confidence sanity:** confidence matches the framework bands (unconfirmed load-bearing fact ⇒ ≤0.35).

## On failure
Do **not** write the file. Return the specific errors. Optionally append a one-line note to `tracker/calibration-review.md` if a signal repeatedly fails validation (a sign an upstream agent is mis-formatting). The caller fixes and retries.

## Naming
`signals/YYYY-MM-DD-<type>.md`, or `signals/YYYY-MM-DD-<type>-<scope>.md` for per-entity signals (e.g. `-scout-musiala`, `-candidate-A2`). Round id goes in frontmatter.

## Guardrails
- **No silent persistence of unvalidated signals.** A bad signal poisons every downstream reader; reject it.
- **Cite or cap.** Uncited factual claims either don't persist or persist at `confidence ≤ 0.35` with a flag — never as confident fact.
- **One signal, one file.** Don't append unrelated signals into one file; downstream readers glob by type+round.

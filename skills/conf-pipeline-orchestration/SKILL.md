---
name: conf-pipeline-orchestration
description: The multi-agent communication and orchestration discipline for a staged pipeline whose stages each carry calibrated uncertainty. Agents talk through files with defined schemas and status fields (never free text); the orchestrator passes input paths plus an explicit output path plus a return contract, verifies each artifact's confidence before advancing a stage gate, holds and integrates worker outputs rather than passing them through, freezes its protected control logic against a checksum, maintains a diversity floor, hardens the fragile handoffs not the resilient hubs, and names the substitution effect every optimized score produces. Conference-agnostic; preloaded by a pipeline orchestrator. Use when coordinating a staged agent pipeline, designing the orchestrator-worker contract, or deciding when to advance, reconcile, or escalate. Trigger keywords - pipeline orchestration, stage gates, structured agent communication, invariant guard, confidence propagation, conflict surfacing.
---

# Conference Pipeline Orchestration

This skill is the operating discipline for an orchestrator that runs a staged pipeline of specialist agents — for a conference scheduler that is ingest → cluster → elicit → schedule, but the discipline is general. Its single organizing idea is **explicit uncertainty management at every layer**: each stage produces *calibrated confidence, not commitments*, and the orchestrator's whole job is to move that uncertainty forward honestly, integrate it, decide when it is small enough to act on, and refuse to let its own safety machinery be optimized away.

The discipline is drawn from how collectives of interacting agents actually fail. The leverage is not in the loudest stage; it is in the **shape of the communication** between stages and in a few **feedback loops on safety-critical asymmetries**. So the rules below are mostly about the *edges* of the pipeline (how stages talk) and about a small set of *invariants* (what the orchestrator must never let drift), not about making any single stage cleverer.

## Common Patterns

### Pattern 1: Confidence propagates — every stage emits it, the next stage reads it

Each stage attaches calibrated confidence to its output and the orchestrator carries it forward: extraction tags low-confidence fields, clustering exposes multi-membership and an outlier bucket, elicitation tracks a preference *region* (uncertainty bands), scheduling exposes a weighted objective and surfaced conflicts. The orchestrator does not collapse this into a single "done" — it reads the confidence at each gate and lets it govern whether to advance, reconcile, or escalate. A pipeline that throws away per-stage confidence cannot make an honest final recommendation.

**Orchestrator action**: at each gate, read the artifact's `meta`/status block (e.g., `confidence_rollup`, `region_tightness`, `unresolved_conflicts`) and branch on it.

### Pattern 2: Structured communication contract — files and status fields, never free text

Agents communicate **through artifacts with defined schemas**, not through prose summaries. The orchestrator spawns a worker with: the **input paths** to read, the **parameters** (ids, output dir), an **explicit output path** to write, and a **return contract** ("return just the path"). The worker writes the schema-shaped artifact and returns the path; the orchestrator **verifies the artifact's status fields** before advancing. This is what makes the pipeline auditable and resumable — the canonical state lives in files, and any agent (or human) can read exactly what was passed and produced. Free-text handoffs are where pipelines silently corrupt.

**Orchestrator action**: never hand a worker a paraphrase of upstream output; hand it the path. Never trust a worker's prose claim of success; read its artifact's status.

### Pattern 3: The orchestrator is an aggregator with internal recurrence, not a pass-through

A good orchestrator is not a sum that forwards whatever a worker returned. It **holds and integrates**: reconciles conflicts between stage outputs, checks the gate, decides whether the artifact is good enough, and only then issues the next command. The integration step is load-bearing — it is where confidence is weighed and where a low-confidence upstream artifact gets caught before it poisons everything downstream. If the orchestrator forwards outputs the instant they arrive, the integration that should have caught the problem never happened.

**Orchestrator action**: between stages, pause to reconcile (use `dialectical-mapping-steelmanning` when two outputs conflict, `deliberation-debate-red-teaming` before a high-stakes advance) rather than chaining blindly.

### Pattern 4: Invariant-guard — freeze the safety logic and checksum against it

The highest-leverage failure mode in multi-agent systems is an in-place agent update that **deletes the very mechanism that would have caught the failure** — the stuck-detector, the kill-switch, the escalation threshold. Defend against it by **freezing the orchestrator's protected control logic** in an invariants lock and **checksumming behavior against it each cycle**: refuse any self-modification or worker instruction that would weaken an invariant. Separate the *protected* logic (which never changes mid-run) from the *updatable* logic (the per-stage plan).

**Orchestrator action**: load `state/invariants.lock.json` at start; each cycle, confirm the stuck-detector, kill-switch, and escalation thresholds are intact; reject anything that would relax them; honor the kill-switch and persist partial state.

### Pattern 5: Diversity floor — fight the quiet convergence on a narrowed model

Sparse interaction makes a pipeline prone to **selection bias**: it converges on a narrower model of the user (or the data) than is true, because it only ever looks at the central, popular cases. Maintain a **diversity floor** — a hard minimum of exploration that cannot be optimized away. In this pipeline that is the elicitor's mandatory outlier probes; more generally it is any rule that forces the system to keep sampling the tails. The orchestrator enforces the floor as a gate condition, not a suggestion.

**Orchestrator action**: do not accept the preference profile as `stable` unless `outlier_probes_done ≥ 1`; do not let a "we already know enough" heuristic short-circuit the exploration minimum.

### Pattern 6: Concentrated hardening — protect the fragile handoffs, not the resilient hubs

Resilience does not come from hardening everything uniformly; it comes from hardening the **fragile medium-load nodes** — the handoffs where a failure cascades — while leaving the robust hubs alone. In this pipeline the fragile nodes are the **elicit → schedule handoff** (a thin, high-stakes profile drives the whole schedule) and the **enrichment fan-out** (many parallel web searches, easy to partially fail). Put the retries, the verification, and the extra confidence checks there; do not spend the budget re-checking the parts that rarely break.

**Orchestrator action**: verify the profile especially carefully before scheduling (weights present, region tight, outlier floor met); on the enrichment fan-out, check each sub-worker's artifact and retry only the failures.

### Pattern 7: Conflict-surfacing is the natural output of honest uncertainty

A system that tracks its own confidence will routinely reach a point where it knows two options both score high and that its model cannot break the tie. The correct move is to **surface that conflict to the human**, not to silently pick. Surfacing is not a failure of the pipeline; it is the pipeline being honest about the limit of what it can decide alone. The orchestrator collects these (the scheduler's `unresolved_conflicts`, any low-confidence gate) and presents them as decisions.

**Orchestrator action**: never auto-resolve a flagged conflict; route it to the human with both sides and why the model could not settle it.

### Pattern 8: Goodhart caution — any optimized score produces an unnamed substitution

Every fitness/score the pipeline optimizes will produce a substitution effect at some node the score did not name (optimize interest, lose breaks; reduce one thing, and the system substitutes toward whatever the rule did not measure). Two defenses: keep the optimization **weights user-owned** (so the system is not silently choosing what to sacrifice), and **name the trade-off** in the output. Never let the orchestrator quietly maximize a proxy and present it as the goal.

**Orchestrator action**: confirm the scheduler used the user's weights and reported a `tradeoffs_note`; if a stage optimized something, ask what it traded away.

### Pattern 9: No silent truncation

Any cap the pipeline applies — top-N events, sampled enrichment, a search budget — must be **logged, not hidden**. A silently truncated result reads as "covered everything" when it did not. The orchestrator treats an unlogged cap as a defect.

**Orchestrator action**: ensure every stage that bounded its work said so (counts, `capped` flags); surface the bound in the final summary.

## Workflow

The stage-gate loop the orchestrator runs:

```
□ Step 1: GROUND — load config, pipeline-state.json, invariants.lock.json. Confirm invariants intact.
□ Step 2: For each stage in order:
    a. SPAWN the worker with input paths + params + explicit output path + return contract.
    b. VERIFY — read the returned artifact's status/confidence fields (not the worker's prose).
       If missing/low-confidence/failed, retry the fragile node or escalate; do not advance.
    c. INTEGRATE — reconcile against prior stages; hold, don't pass through. Check the gate condition
       (including the diversity floor where it applies).
    d. CHECK INVARIANTS — confirm nothing weakened the stuck-detector/kill-switch/thresholds.
    e. ADVANCE or ESCALATE — advance only when the gate passes; otherwise surface to the human.
□ Step 3: At the interactive stage, hand off to the human-facing agent in the main conversation;
          a background worker cannot ask questions.
□ Step 4: SYNTHESIZE — present the result plus surfaced conflicts plus the trade-off note as
          decisions; never auto-commit.
```

## Guardrails

### 1. Invariant-guard is absolute
**Danger**: A self-update or worker instruction deletes the stuck-detector; the pipeline then locks up invisibly.
**Guardrail**: Freeze protected logic; checksum each cycle; reject anything that weakens it; honor the kill-switch.

### 2. Talk through files, verify by artifact
**Danger**: Free-text handoffs and trusting a worker's "done" claim corrupt the pipeline silently.
**Guardrail**: Pass paths + return contracts; verify the artifact's status fields yourself.

### 3. Hold and integrate; don't pass through
**Danger**: Forwarding outputs the instant they arrive skips the reconciliation that catches bad upstream data.
**Guardrail**: Between stages, reconcile and gate before issuing the next command.

### 4. Enforce the diversity floor
**Danger**: The pipeline quietly converges on a narrowed model.
**Guardrail**: Exploration minimums (outlier probes) are gate conditions, not suggestions.

### 5. Harden the fragile handoffs
**Danger**: Uniform hardening wastes budget and leaves the cascade-prone node exposed.
**Guardrail**: Concentrate verification/retries at the elicit→schedule handoff and the enrichment fan-out.

### 6. Surface conflicts; name trade-offs; log caps
**Danger**: Silent picks, silent proxy-maximization, and silent truncation all read as confident completeness.
**Guardrail**: Route ties to the human; keep weights user-owned and report the substitution; log every cap.

## Quick Reference

### Principle → orchestrator action

| Principle | Action at runtime |
|---|---|
| Confidence propagates | Branch on each artifact's status/confidence at the gate |
| Structured contract | Pass paths + return contract; verify artifact, not prose |
| Aggregator with recurrence | Reconcile + gate before advancing |
| Invariant-guard | Checksum protected logic each cycle; reject weakening |
| Diversity floor | Outlier-probe minimum is a gate condition |
| Concentrated hardening | Extra checks on elicit→schedule + enrichment fan-out |
| Conflict-surfacing | Route ties to the human with both sides |
| Goodhart caution | User-owned weights + named trade-off |
| No silent truncation | Every cap logged and surfaced |

### Failure mode → early warning → loop (the safety loop to build first)

| Failure mode | Early-warning signal | Closing loop |
|---|---|---|
| Stuck-detector overwritten + premature convergence | invariant checksum mismatch; `outlier_probes_done = 0` | Reject the self-update; refuse to accept the profile as stable; re-run elicitation's exploration |
| Low-confidence upstream poisons schedule | high `low_confidence_field_fraction` at a gate | Don't advance; surface, or harden the fragile handoff with a retry |
| Silent proxy-maximization | scheduler ran without user weights / no `tradeoffs_note` | Halt the advance; require user-owned weights and the trade-off note |

## Related Skills

- **systems-thinking-leverage**: the leverage-point and Goodhart/substitution lens behind these rules.
- **deliberation-debate-red-teaming**: the stress-test the orchestrator runs before a high-stakes advance.
- **dialectical-mapping-steelmanning**: how to reconcile two conflicting stage outputs without papering over the conflict.
- **bayesian-reasoning-calibration**: the calibration discipline behind per-stage confidence.

## Examples in Context

### Example 1: Catching a poisoned gate

Ingestion returns `confidence_rollup.low_confidence_field_fraction: 0.55` — more than half the fields are guesses. The orchestrator does **not** advance to clustering on it. It surfaces: "Over half the program's fields are low-confidence (sparse abstracts). I can run enrichment harder on the thin sessions, or proceed and flag the clusters as provisional — your call." The gate's confidence branch turned a silent corruption into a visible decision.

### Example 2: Refusing to optimize away the safety rail

A proposed mid-run adjustment would let the elicitor skip outlier probes "to save the user time." The orchestrator checks the invariants lock: the diversity floor is protected. It refuses the change and keeps the outlier-probe minimum, because the most common multi-agent failure is exactly this — the system removing the exploration that would have surfaced the user's hidden interest, and then quietly converging on a narrower model of them.

---
name: conf-schedule-optimization
description: Build a personal conference schedule as a constraint-optimization problem — hard constraints (no time overlap, room-to-room travel time, capacity/registration, the attendee's own must-attends and blackouts) plus a user-owned weighted objective trading interest against breadth, pacing (maximize contiguous free time), and serendipity. Surfaces unbreakable conflicts (two high-value overlapping talks the model cannot rank) as decisions for the human rather than silently picking, and reports what each choice traded away. Conference-agnostic. Use to turn a preference profile plus a theme map into a day-by-day plan, to resolve overlapping sessions, or to balance a packed vs paced schedule. Trigger keywords - schedule optimization, conference schedule, constraint optimization, overlapping talks, contiguous free time, conflict surfacing, packed vs paced.
---

# Conference Schedule Optimization

Choosing what to attend is a constrained optimization problem, and treating it as one is what separates a real schedule from a wishlist. Events are variables; time slots are their domain; **hard constraints** (you cannot be in two rooms at once, you need minutes to walk between them, a capped workshop may be full, you said you must catch the opening keynote) define what is *feasible*; and a **weighted objective** over the feasible plans defines what is *good*. The output is the best feasible plan **plus** an honest account of what it could not decide and what it gave up to score well.

The objective is genuinely multi-term and the terms are in real conflict: maximizing **interest** fights **breadth** (seeing across themes), both fight **pacing** (a day of six back-to-back talks with fifteen-minute gaps is worse than five with a real break), and all three fight **serendipity** (deliberately leaving room for the unplanned good thing). You do not resolve this by pretending one term dominates. You jointly optimize a weighted sum whose **weights are the attendee's** — handed over from the preference profile, never invented here.

Two disciplines keep it honest. **Conflict-surfacing**: when two talks overlap and both score high and the profile cannot break the tie, the system *flags it for the person* rather than quietly choosing — that flag is the natural output of a model that tracks its own uncertainty. And the **Goodhart caution**: any score you optimize produces a substitution effect somewhere the score did not name (optimize raw interest and you quietly sacrifice breaks; optimize breadth and you skip the one talk they cared about most). So the weights stay user-owned, the conflicts get surfaced, and the schedule reports what it traded away.

## The output (schedule contract)

```json
{
  "generated_on": "YYYY-MM-DD",
  "method": "greedy-local-search | ilp",
  "selections": [
    {
      "day": "YYYY-MM-DD", "start": "HH:MM", "end": "HH:MM",
      "event_id": "...", "room": "...",
      "score": 0.0, "why": "why this won its slot",
      "alternatives": [ { "event_id": "...", "score": 0.0, "why_not": "why it lost / is recorded / lower affinity" } ]
    }
  ],
  "free_blocks": [ { "day": "YYYY-MM-DD", "start": "HH:MM", "end": "HH:MM", "purpose": "break | buffer | travel | meal" } ],
  "objective_breakdown": {
    "interest": 0.0, "breadth": 0.0, "pacing": 0.0, "serendipity": 0.0,
    "total": 0.0, "weights": { "interest": 0.0, "breadth": 0.0, "pacing": 0.0, "serendipity": 0.0 }
  },
  "unresolved_conflicts": [
    {
      "day": "YYYY-MM-DD", "slot": "HH:MM-HH:MM",
      "candidates": ["event_id_a", "event_id_b"],
      "why_unbreakable": "both score within epsilon; profile does not rank them",
      "needs": "your decision"
    }
  ],
  "constraints_applied": { "travel_time": "...", "capacity": "...", "hard_constraints": ["..."] },
  "tradeoffs_note": "what the chosen weighting sacrificed (the Goodhart honesty line)"
}
```

## Common Patterns

### Pattern 1: Formulate it as a COP — hard vs soft

Separate the two kinds of rule cleanly:

- **Hard constraints** (feasibility — never violated): no two selections overlap in time; consecutive selections in different rooms are separated by at least the room-to-room **travel time** (from config); a `capacity_constrained` session counts only if the attendee can realistically get a seat; and the attendee's own **hard_constraints** from the profile (must-attends are forced in; blackouts/kept-free blocks are forced out).
- **Soft objective** (quality — maximized): the weighted sum below.

A plan that violates a hard constraint is not a worse plan, it is not a plan. Filter first, optimize second.

### Pattern 2: The weighted objective — four terms in tension

Score a candidate plan as `w_interest·Interest + w_breadth·Breadth + w_pacing·Pacing + w_serendipity·Serendipity`, with the `w`s from the profile:

- **Interest** — sum of the attendee's interest (via theme affinities × region) over selected talks. The "see what I care about" term.
- **Breadth** — coverage across distinct themes (diminishing returns on the 4th talk in one theme). The "don't tunnel" term.
- **Pacing** — rewards **contiguous free time** and penalizes fragmentation: a plan with one real 90-minute break beats one with six scattered 15-minute gaps, even at equal talk count. Also penalizes variance from preferred times and excess travel.
- **Serendipity** — rewards deliberately leaving slack and including the occasional outlier/exploration pick, so the plan is not a maximally-packed interest machine.

### Pattern 3: Maximize contiguous free time, not just minimize gaps

Anti-fragmentation deserves its own emphasis because it is the easiest thing to get wrong. Six non-adjacent talks with fifteen-minute gaps is a worse day than the same six clustered with a genuine break — the human needs contiguous recovery, hallway conversations, and food. Model free time as **blocks**, reward the *longest contiguous* block, and treat a real break as a first-class good in the objective, not as leftover space.

### Pattern 4: Surface unbreakable conflicts — do not silently pick

When two (or more) talks overlap, both score within an epsilon of each other, and the profile gives no basis to rank them, **flag it** in `unresolved_conflicts` with both candidates and why the model cannot break the tie. Do not flip a coin and hide it. This is the honest output of a system that knows both talks score high and that its model of the person cannot settle it alone — exactly the moment to hand the decision back. (When the profile *does* break the tie, pick, and record the loser in `alternatives` with a `why_not`.)

### Pattern 5: Solve with greedy + local search by default, ILP when available

- **Default (no solver deps)**: greedy seed (best feasible pick per slot, chronologically) then **local search** — swap/insert/remove moves that improve the weighted objective while staying feasible. Fast, transparent, good enough for a few-hundred-event program. This is what `resources/schedule.py` implements with numpy/pandas/networkx only.
- **Exact (optional)**: formulate as an ILP and solve with `pulp`/`ortools` when installed and an optimum is wanted. Document the upgrade; do not require it.

Record which ran in `method`.

### Pattern 6: Report the trade-off (Goodhart honesty)

Whatever the weights, the plan sacrificed something the weights under-counted. State it in `tradeoffs_note`: "Weighted toward interest, so day 2 is dense and breaks are short" or "Paced/breadth weighting means your single highest-interest talk was dropped for coverage." Naming the substitution is the antidote to optimizing a proxy and pretending it was the goal.

## Workflow

```
□ Step 1: Load events.json, affinities.json, profile.json; load rooms + travel matrix + day bounds from config.
□ Step 2: Force in the profile's must-attends; force out blackouts/kept-free blocks.
□ Step 3: Build feasibility: per slot, the set of events that do not overlap, respect travel time,
          and are seatable (capacity).
□ Step 4: Score each event for the attendee (affinity × region interest, depth/format fit).
□ Step 5: Greedy-seed a feasible plan; run local search to maximize the user-weighted objective.
□ Step 6: Detect overlaps where top candidates tie within epsilon and the profile can't rank them ->
          unresolved_conflicts (do not auto-pick).
□ Step 7: Compute free_blocks (reward the longest contiguous block) and objective_breakdown.
□ Step 8: Write schedule.json + schedule.md (day-by-day) + conflicts.md (decisions) + rationale.md
          (picks, objective_breakdown, tradeoffs_note). Return the schedule.json path.
```

## Guardrails

### 1. The weights are the user's
**Danger**: A hard-coded weighting silently sets the schedule's whole character.
**Guardrail**: Read `objective_weights` from the profile. Never invent or override them.
**Red flag**: A default weight vector compiled into the optimizer.

### 2. Surface conflicts, don't hide them
**Danger**: A silent coin-flip on two high-value talks looks like a confident decision it isn't.
**Guardrail**: Tie within epsilon + profile can't rank ⇒ `unresolved_conflicts`, not a pick.

### 3. Protect contiguous free time
**Danger**: A maximally-packed day reads as "optimal" and burns the human out.
**Guardrail**: Reward the longest contiguous free block; treat a real break as a first-class objective term.

### 4. Goodhart — report the substitution
**Danger**: Optimizing one proxy quietly sacrifices an unnamed good.
**Guardrail**: State what the weighting traded away in `tradeoffs_note`.

### 5. Hard constraints are inviolable
**Danger**: A high-scoring plan that double-books a room or skips a must-attend.
**Guardrail**: Filter to feasible before optimizing; force must-attends in, blackouts out.

### 6. No silent truncation; don't re-elicit or execute
**Danger**: Capping candidates or writing to a calendar without saying so.
**Guardrail**: Log any caps. Do not change the profile. Calendar export only on explicit instruction.

## Quick Reference

### Hard constraints

| Constraint | Source | Effect |
|---|---|---|
| No time overlap | event times | one selection per instant |
| Travel time | config room matrix | min gap between different-room picks |
| Capacity / registration | `axes.capacity_constrained` | a capped session may be infeasible |
| Must-attend / blackout | profile `hard_constraints` | forced in / forced out |

### Soft objective terms

| Term | Rewards | Typical signal |
|---|---|---|
| interest | talks the attendee cares about | affinity × region interest |
| breadth | coverage across themes | distinct themes (diminishing returns) |
| pacing | contiguous free time, low fragmentation, preferred times | longest free block; gap penalty |
| serendipity | slack + occasional outlier pick | deliberate unscheduled space |

### Method choice

| Situation | Method |
|---|---|
| No solver deps (default) | greedy + local search (`resources/schedule.py`) |
| `pulp`/`ortools` present and an optimum wanted | ILP |

## Related Skills

- **conf-preference-elicitation**: supplies the region, axis preferences, weights, and hard constraints that parameterize this optimization.
- **conf-theme-clustering**: supplies the affinities used for the interest and breadth terms.
- **decision-matrix**: a structured way to present a surfaced conflict's candidates to the human.
- **expected-value**: for weighing a capacity-risky workshop (might be full) against a guaranteed alternative.
- **systems-thinking-leverage**: the Goodhart/substitution lens that motivates `tradeoffs_note`.

## Examples in Context

### Example 1: A surfaced conflict

Day 2, 11:10–11:30 has two talks scoring 0.81 and 0.79 — one on Agents, one on Retrieval, both close to the attendee's interests, and the profile does not rank Agents over Retrieval. The optimizer does **not** pick. It writes an `unresolved_conflicts` entry naming both and "both within epsilon; profile does not rank these themes," `needs: your decision`. The person settles it in one line; the schedule never pretended it had.

### Example 2: Paced beats packed at equal interest

Two feasible plans tie on interest. Plan A: six talks, gaps of 15–20 minutes all afternoon. Plan B: five talks plus one contiguous 80-minute afternoon block. With the attendee's `pacing`-leaning weights, Plan B scores higher — the long break is a modeled good, not wasted space — and `tradeoffs_note` records that one lower-interest talk was dropped to buy the break, which is exactly the trade the person asked for.

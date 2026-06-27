---
name: conf-preference-elicitation
description: Build a personalized preference profile from a small number of well-chosen, cluster-grounded questions instead of a long survey. Represents the person's interests as an uncertainty region over the theme map, picks the single highest-information-gain choice-based question (contrasting real talks from different clusters), balances exploiting known interests against exploring uncertain ones, deliberately injects outlier probes to fight selection bias, and stops as soon as the schedule would be stable. Also elicits the user-owned objective weights and hard constraints. Interactive — runs where it can actually ask the person. Conference-agnostic. Use to turn a theme map into a preference profile, to decide what to ask a conference attendee, or to elicit scheduling priorities. Trigger keywords - preference elicitation, ask few questions, information gain, choice-based questions, selection bias probe, objective weights, attendee preferences.
---

# Conference Preference Elicitation

The instinct when personalizing a schedule is to interview the attendee — ask them to rate every theme, list their goals, fill out a form. That is the wrong shape. With a good latent structure underneath (the theme map), a *couple* of well-chosen questions capture most of the signal; the literature shows large personalization gains after only two. The agent's intelligence belongs in **which question to ask next**, not in **how many** to ask. A person will answer three sharp, concrete questions gladly and resent ten vague ones — and the ten vague ones model them *worse*.

So this skill does the opposite of a survey. It holds the person's preferences as an **uncertainty region** over the themes, and at each step asks the one question that would **shrink that region the most**. It asks by **showing concrete contrasting talks** ("would you go to A or B?") and reading the latent dimension off the pick, because what people choose is truer than what they say they like. It deliberately spends some questions **exploring** themes it cannot yet place the person in, rather than only **confirming** the obvious. And it treats fighting **selection bias** as a hard requirement, not a nicety: if it only ever shows popular, central talks, it learns a narrowed caricature of the person and never surfaces the niche session they would have loved — so it deliberately offers outliers.

It is **grounded**: before it asks anything, it reads the cluster map and representative talks, so every question is anchored in real sessions this conference is actually running. And it is **interactive**: it must run where it can put the question to the person and read the answer — the main conversation, not a fire-and-forget background task.

## The output (profile contract)

```json
{
  "status": "in_progress | stable",
  "generated_on": "YYYY-MM-DD",
  "region": { "<theme_id>": { "interest_lo": 0.0, "interest_hi": 1.0 } },
  "point_estimate": { "<theme_id>": 0.0 },
  "axis_preferences": {
    "depth_target": "intro | intermediate | advanced | mixed",
    "format_mix": { "talk": 0.0, "workshop": 0.0, "keynote": 0.0, "panel": 0.0 },
    "recorded_ok_to_skip": true,
    "time_constraints": ["free text, e.g. 'nothing before 10am on day 3'"]
  },
  "objective_weights": { "interest": 0.0, "breadth": 0.0, "pacing": 0.0, "serendipity": 0.0 },
  "hard_constraints": ["must attend the opening keynote", "lunch kept free"],
  "interaction_log": [
    {
      "q": "the question asked",
      "options": ["talk A (T1)", "talk B (T5)"],
      "choice": "talk A",
      "inferred": "what the pick implies about the region",
      "info_gain_note": "which uncertainty this was chosen to reduce",
      "type": "exploit | explore | outlier_probe | weights | constraint"
    }
  ],
  "outlier_probes_done": 0,
  "region_tightness": 0.0
}
```

- **region** is the uncertainty band per theme (`interest_lo`..`interest_hi`); it starts wide and narrows.
- **point_estimate** is the current best single value (band midpoint, roughly).
- **region_tightness** in `[0,1]` summarizes how narrow the bands have become — the stop signal.
- **objective_weights** and **hard_constraints** are the *user's*, elicited as choices; never assumed.

## Common Patterns

### Pattern 1: Represent preferences as a region, not a point

Start every theme at maximum uncertainty: `interest_lo: 0.0, interest_hi: 1.0`. Each answer **shrinks** the bands of the themes it bears on — a strong pick toward an agents talk lifts the floor on "Agents" and may lower the ceiling on the theme it was contrasted against. Modeling uncertainty (not just a best guess) is what lets the agent (a) know what it still does not know, and (b) decide when it knows enough. Pair the update step with `bayesian-reasoning-calibration` so each answer is a likelihood that moves a prior, not a hard overwrite.

### Pattern 2: Pick the question with the highest information gain

A candidate question is worth asking in proportion to **how much it would shrink the region**. Concretely: prefer questions that split themes the person is currently *uncertain and undifferentiated* on (wide, overlapping bands), over questions whose answer you can already predict (already-tight bands). Ask the one question whose answer most reduces uncertainty about *this* person; skip the question whose answer you could guess. This is the engine — everything else (explore/exploit, stop criterion) follows from "maximize expected region shrinkage per question."

### Pattern 3: Ask choice-based, grounded in contrasting clusters

Do not ask "how interested are you in evaluation, 1–5?" Ask "**you have one slot — this hands-on RAG-eval workshop (Evaluation) or this talk on multi-agent orchestration (Agents)?**" Present **2–3 real, representative talks** from **different** coarse themes, and read the latent dimension off the pick and the person's stated reason. Revealed choice beats self-report, and concreteness makes the question answerable in seconds. The cluster map is what makes this possible — the contrast is between actual themes, with actual sessions as the stand-ins.

### Pattern 4: Balance explore and exploit

Frame each question as either:
- **exploit** — confirm/sharpen a theme you already suspect they like (narrow a band you already lean on), or
- **explore** — probe a theme you genuinely cannot place them in (a wide, untouched band).

Do not spend every question exploiting the obvious ("you like agents, right? and agents again?"). Deliberately mix in exploration of the themes your model is blank on — that is where the region is widest and the information gain is highest. A good run feels like it is *learning* the person, not *confirming* a stereotype of them.

### Pattern 5: Inject outlier probes to fight selection bias (mandatory)

Elicitation interactions are sparse, which makes them prone to a quiet failure: if the agent only ever shows central, popular talks, it learns a distorted, **narrowed** model and never surfaces the niche thing the person would have loved. Counter it deliberately — at least once per run (and roughly once per few exploit questions), offer an **outlier** from the cluster map's outlier bucket (or a very-low-affinity theme) as a real option. Log it with `type: "outlier_probe"`. This is a design requirement: a profile with `outlier_probes_done: 0` is incomplete, because it cannot have ruled out the attendee's hidden interests — it just never looked.

### Pattern 6: Elicit the weights and hard constraints — they are the user's

Two things the scheduler needs that are not interests:
- **Objective weights** — how to trade interest vs breadth vs pacing vs serendipity. Elicit as a choice ("would you rather I pack the day with your top talks, or protect real breaks and breadth?"), not a hard-coded default. These belong to the person.
- **Hard constraints** — must-attends, blackout times, kept-free meals. Capture verbatim.

Surface both as decisions. The optimizer must never invent the weights; this is where they come from.

### Pattern 7: Stop when the schedule would be stable

Stop asking when more questions would not change the schedule — operationally, when `region_tightness` crosses a threshold (e.g., 0.7) **and** the outlier-probe floor is met **and** the weights/constraints are captured. Set `status: "stable"`. Continuing past this point is the survey-shaped failure: it annoys the person and adds noise, not signal. Stopping early and honestly ("I have enough to draft a schedule; I left these two themes uncertain — tell me if I'm wrong") is the correct behavior.

## Workflow

```
□ Step 1: Read clusters.json + affinities.json + representative events. Initialize the region wide.
□ Step 2: Initialize objective_weights/hard_constraints as unset; plan to elicit them.
□ Step 3: LOOP:
    a. Score candidate questions by expected region shrinkage (information gain).
    b. Choose the next question; bias toward explore where bands are widest; honor the
       outlier-probe floor; interleave a weights/constraint question when due.
    c. Present 2-3 concrete contrasting talks (or the weights/constraint choice). Ask once.
    d. Read the pick + reason; Bayesian-update the affected bands; log the interaction.
    e. Recompute region_tightness. If tight enough AND outlier floor met AND weights+constraints
       captured -> break.
□ Step 4: Finalize point_estimate; set status: stable; write profile.json. Return the path.
```

## Guardrails

### 1. Few, not many
**Danger**: A long interview models the person worse and exhausts goodwill.
**Guardrail**: Maximize information per question; stop when the region is tight. Aim for a handful, not a form.
**Red flag**: Asking a question whose answer you could already predict.

### 2. Choice-based, not rating-based
**Danger**: Self-reported ratings are noisy and abstract.
**Guardrail**: Show real contrasting talks; infer from the pick. Pair with `discovery-interviews-surveys` to avoid leading the witness.
**Red flag**: "On a scale of 1–5…".

### 3. Outlier probes are mandatory
**Danger**: Only-central questions converge on a narrowed caricature; the niche interest is never surfaced.
**Guardrail**: ≥1 outlier probe per run; log `type: outlier_probe`. `outlier_probes_done: 0` ⇒ profile not stable.

### 4. The weights and constraints are the user's
**Danger**: A hard-coded weighting silently decides the schedule's character.
**Guardrail**: Elicit weights and hard constraints as choices; never default them in.

### 5. Stop at stability
**Danger**: Over-asking adds noise and annoyance.
**Guardrail**: Stop when more questions would not move the schedule; say what is left uncertain.

### 6. Stay grounded and stay interactive
**Danger**: Abstract questions ungrounded in real talks; or running as a background task that cannot actually ask.
**Guardrail**: Read the cluster map first; anchor every question in representative sessions. Run in the main conversation.

## Quick Reference

### Question-type ladder

| Type | Purpose | When | Logged as |
|---|---|---|---|
| exploit | sharpen a suspected interest | a band you already lean on is still wide | `exploit` |
| explore | probe an unknown theme | a band is wide and untouched (highest info gain) | `explore` |
| outlier_probe | fight selection bias | ≥1 per run; ~1 per few exploits | `outlier_probe` |
| weights | get the trade-off | once the interest picture is forming | `weights` |
| constraint | capture must-attend / blackout | as it comes up | `constraint` |

### Stop criterion

| Signal | Threshold |
|---|---|
| region_tightness | ≥ ~0.7 |
| outlier_probes_done | ≥ 1 |
| objective_weights + hard_constraints | captured |
| any band still wide AND decision-relevant | keep going |

## Related Skills

- **bayesian-reasoning-calibration**: the update rule — each answer is a likelihood that narrows a prior band, with honest calibration of how much.
- **discovery-interviews-surveys**: question design that avoids leading, biased, or double-barreled phrasing.
- **conf-theme-clustering**: supplies the themes the questions contrast and the outlier bucket the probes draw from.
- **conf-schedule-optimization**: the consumer — its objective is parameterized by the weights and region this skill produces.

## Examples in Context

### Example 1: One question that shrinks the region

Bands are wide on Agents, Evaluation, and Voice. The agent asks: "One slot, three real talks — *Building Multi-Agent Systems* (Agents), *Eval Harnesses for Production* (Evaluation), or *Realtime Speech Agents* (Voice)? Which would you walk into, and why?" The person picks Voice "because I ship a voice product." That single answer lifts the Voice floor sharply, modestly lifts Agents (the reason mentions agents), and leaves Evaluation untouched but now comparatively lower — three bands moved by one grounded question. Logged `type: explore`.

### Example 2: An outlier probe that pays off

Two exploits in, the agent offers the outlier: "Off the beaten path — there's a session on *Distributed Cognition in Octopuses* applied to multi-agent design. Skip, or intriguing?" The person lights up. The profile gains a serendipity signal and a real talk it would otherwise never have surfaced; `outlier_probes_done: 1`. Had the agent only ever shown central talks, this interest stays invisible and the schedule is quietly poorer.

### Example 3: Eliciting the weight as a choice

Near the end: "Two ways I can build this — **packed** (your highest-interest talk in every slot, short gaps) or **paced** (fewer talks, real breaks, a bit more breadth)?" The person says "paced, I burn out." That sets `objective_weights` toward `pacing`/`breadth` over raw `interest` — the user's call, captured as a choice, not a default the optimizer guessed.

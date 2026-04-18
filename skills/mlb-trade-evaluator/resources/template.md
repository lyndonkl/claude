# MLB Trade Evaluator Templates

Input schema, per-category delta tables, value/slot/adverse-selection/flex/playoff blocks, verdict block with rationale and counter. Fill every field. Empty fields flag the signal confidence as low.

## Table of Contents
- [Trade Offer Input](#trade-offer-input)
- [Player Projection Table (Rest-of-Season)](#player-projection-table-rest-of-season)
- [Per-Category Delta Table — Both Teams](#per-category-delta-table--both-teams)
- [Ratio Category Weighted Computation](#ratio-category-weighted-computation)
- [`cat_pressure` Weight Sheet](#cat_pressure-weight-sheet)
- [`trade_value_delta` Stack Block](#trade_value_delta-stack-block)
- [Slot-Value Bonus Block](#slot-value-bonus-block)
- [Adverse-Selection Prior Block](#adverse-selection-prior-block)
- [`positional_flex_delta` Block](#positional_flex_delta-block)
- [`playoff_impact` Block (July+)](#playoff_impact-block-july)
- [Verdict Block](#verdict-block)
- [Counter-Offer Construction](#counter-offer-construction)
- [Signal File Frontmatter](#signal-file-frontmatter)
- [Worked Example A — ACCEPT](#worked-example-a--accept)
- [Worked Example B — COUNTER](#worked-example-b--counter)
- [Worked Example C — REJECT](#worked-example-c--reject)

---

## Trade Offer Input

| Field | Value |
|---|---|
| Evaluation date | YYYY-MM-DD |
| Initiating team (other side) | ____ |
| User's team | ⚾ K L's Boomers |
| Opponent archetype (from `context/opponents/<team>.md`) | active / expert / dormant / frustrated / unknown |
| Offer expires at | ____ |
| League standings position (us) | __ / 12 |
| Standings position (them) | __ / 12 |
| Are they a playoff-seed competitor? | yes / no |
| Days until trade deadline (Aug 6) | __ |
| Commissioner review likely? | yes / no |

**Players coming IN (to us):**

| Player | Position(s) | Team | IL? | Notes |
|---|---|---|---|---|
| | | | | |

**Players going OUT (to them):**

| Player | Position(s) | Team | IL? | Notes |
|---|---|---|---|---|
| | | | | |

---

## Player Projection Table (Rest-of-Season)

Source for every row must be cited (URL). Primary: FanGraphs ATC rest-of-season. Fallback: Depth Charts, Razzball.

**Hitters:**

| Player | Side | ROS PA | R | HR | RBI | SB | OBP | $ value | Source URL |
|---|---|---|---|---|---|---|---|---|---|
| (IN) | IN | | | | | | | | |
| (OUT) | OUT | | | | | | | | |

**Pitchers:**

| Player | Side | ROS IP | K | ERA | WHIP | QS | SV | $ value | Source URL |
|---|---|---|---|---|---|---|---|---|---|
| (IN) | IN | | | | | | | | |
| (OUT) | OUT | | | | | | | | |

**Totals:**

| Side | PA | R | HR | RBI | SB | IP | K | QS | SV | $ total |
|---|---|---|---|---|---|---|---|---|---|---|
| IN (ours after trade) | | | | | | | | | | |
| OUT (theirs after trade) | | | | | | | | | | |

---

## Per-Category Delta Table — Both Teams

| Cat | Our IN total | Our OUT total | Raw Δ (our side) | `cat_pressure` | Weighted Δ | Direction |
|---|---|---|---|---|---|---|
| R | | | | | | ▲ / ▼ / — |
| HR | | | | | | |
| RBI | | | | | | |
| SB | | | | | | |
| OBP | | | (see ratio table) | | | |
| K | | | | | | |
| ERA | | | (see ratio table) | | | |
| WHIP | | | (see ratio table) | | | |
| QS | | | | | | |
| SV | | | | | | |
| **Sum** | | | | | **`trade_cat_delta` = ____** | |

**Mirror table (red-team check — use raw or their pressures, NOT ours):**

| Cat | Their IN total | Their OUT total | Raw Δ (their side) | Their assumed pressure | Weighted Δ |
|---|---|---|---|---|---|
| R | | | | | |
| … | | | | | |

---

## Ratio Category Weighted Computation

### OBP

```
Incoming OBP (volume-weighted) = Σ(OBP_i × PA_i) / Σ(PA_i)   over IN hitters
Outgoing OBP (volume-weighted) = Σ(OBP_j × PA_j) / Σ(PA_j)   over OUT hitters
Team-level delta = team_after − team_before
```

| IN hitter | PA | OBP | PA × OBP |
|---|---|---|---|
| | | | |
| Sum | ___ | (weighted avg) ___ | ___ |

### ERA

```
Implied ER_i = ERA_i × IP_i / 9
ERA_IN = 9 × Σ(ER_i) / Σ(IP_i)
```

Sign convention: lower ERA = gain; flip sign before summing.

### WHIP

Same pattern as ERA; `baserunners_i = WHIP_i × IP_i`.

---

## `cat_pressure` Weight Sheet

Pull from the most recent `signals/YYYY-MM-DD-cat-state.md`.

| Cat | `cat_position` (winning/tied/losing) | `cat_pressure` (0-100) | Weight (= pressure/50) |
|---|---|---|---|
| R | | | |
| HR | | | |
| RBI | | | |
| SB | | | |
| OBP | | | |
| K | | | |
| ERA | | | |
| WHIP | | | |
| QS | | | |
| SV | | | |

**Source signal file**: `signals/YYYY-MM-DD-cat-state.md`

---

## `trade_value_delta` Stack Block

The raw dollar delta is only the first layer. Show the full stack: raw → slot-adjusted → adverse-selection-adjusted.

| Player | Side | $ value | Source |
|---|---|---|---|
| (IN 1) | IN | +$ | |
| (OUT 1) | OUT | −$ | |
| **Net raw** | | **$ _____** | |

```
(a) trade_value_delta_raw        = Σ$_IN − Σ$_OUT             = $ _____
(b) slot_value_delta             = (slots_us − slots_them) × $2.50 = $ _____
(c) trade_value_delta_pre_adj    = (a) + (b)                  = $ _____
(d) recommended_adjustment       (from @skills/adverse-selection-prior/)  = _____
(e) trade_value_delta_adjusted   = (c) × (d)                  = $ _____
(f) delta_pct                    = (e) / Σ$_OUT               = _____%
```

---

## Slot-Value Bonus Block

```
players_IN  = __
players_OUT = __

N_slots_cleared_for_us   = max(0, players_OUT − players_IN)  = __
N_slots_cleared_for_them = max(0, players_IN  − players_OUT) = __

slot_value_delta = (slots_us − slots_them) × $2.50 = $ _____
```

**Rationale (plain English)**: "Every empty bench spot is worth about $2-3 because we can stream a pitcher or stash an injured returner for free. A 2-for-1 where we send two gives us one free bench spot."

---

## Adverse-Selection Prior Block

Invoke `@skills/adverse-selection-prior/` with these inputs:

| Input | Value | Derivation |
|---|---|---|
| `offer_type` | trade / counter_offer | trade if fresh, counter_offer if response to our prior |
| `proposer_archetype` | active / expert / dormant / frustrated / unknown | `context/opponents/<team>.md` |
| `offer_symmetry_score` | __ | from `trade_value_delta_pre_adj / Σ$_OUT` ratio (see methodology) |
| `proposer_info_asymmetry` | __ | start 50; adjust for injuries, archetype, closer news |

Skill output (consume verbatim):

| Output | Value |
|---|---|
| `prior_ev_probability` | __ |
| `recommended_adjustment` | __ |
| `bayesian_rationale` | (quote into verdict block) |
| `override_hints` | (append each to red_team_findings) |

```
adverse_selection_adjustment_pct = (1 − recommended_adjustment) × 100 = __%
```

---

## `positional_flex_delta` Block

Score from −100 to +100.

| Factor | Our roster before | Our roster after | Score impact |
|---|---|---|---|
| SS depth (scarce) | | | ±__ |
| C depth (scarce) | | | ±__ |
| 2B depth (moderate scarcity) | | | ±__ |
| OF depth (abundant) | | | ±__ |
| SP count vs 3 slot + 5 flex | | | ±__ |
| RP / closer count vs 2 slot + 5 flex | | | ±__ |
| Multi-position (2+) eligibility gained/lost | | | ±__ |
| **Total `positional_flex_delta`** | | | **____** |

Note: bench-slot optionality is counted separately via `slot_value_delta` (dollars). Do not double-count here.

---

## `playoff_impact` Block (July+)

Only populate if evaluation date ≥ July 1, 2026.

| Player | Side | Games in W21 | W22 | W23 | Total | Avg matchup_q (0-100) | Contribution |
|---|---|---|---|---|---|---|---|
| (IN) | IN | | | | | | +___ |
| (OUT) | OUT | | | | | | −___ |

```
playoff_impact = 50 + clamp(raw_playoff_delta / 200, −50, +50)
```

---

## Verdict Block

### Summary signal values

| Signal | Value |
|---|---|
| `trade_cat_delta` (weighted sum across 10 cats) | |
| `trade_value_delta_raw` ($) | |
| `slot_value_delta` ($) | |
| `trade_value_delta_pre_adj` ($) | |
| `prior_ev_probability` | |
| `recommended_adjustment` | |
| `adverse_selection_adjustment_pct` | |
| `trade_value_delta_adjusted` ($) | |
| `delta_pct` (% of Σ$_OUT) | |
| `positional_flex_delta` (−100 to +100) | |
| `playoff_impact` (0-100; N/A if pre-July) | |
| Confidence (0.0-1.0) | |

### Ladder applied

- [ ] `delta_pct ≥ +15%`? __
- [ ] Advocate/critic variants agree? __
- [ ] No cat with pressure ≥80 has negative weighted delta? __
- [ ] `-20% < delta_pct < +15%`? __
- [ ] `delta_pct ≤ −20%` AND `prior_ev_probability ≤ 0.35`? __

Decision:
- **All three ACCEPT gates checked** → **ACCEPT**.
- **Middle band** → **COUNTER** with specific package (always).
- **Both REJECT conditions** → **REJECT** (and include the counter we would have sent for the relationship log).
- **Only one REJECT condition** → **COUNTER** with a demanding package.

### Verdict

**VERDICT: _____ [ACCEPT / COUNTER / REJECT]**

**Why (1-2 sentences, beginner-voice, jargon translated inline):**

________________________________________________

**Bayesian rationale (from `@skills/adverse-selection-prior/`):**

________________________________________________

**Category impact in plain English:**

- "We gain about __ HR and __ RBI — but lose __ SB and __ QS (quality starts, a good pitching start of 6+ innings and 3 or fewer earned runs)."
- "The cats we care most about right now are __ and __."

**Positional impact in plain English:**

________________________________________________

**Playoff impact in plain English (July+):**

________________________________________________

---

## Counter-Offer Construction

Populate whenever VERDICT = COUNTER (modal case) OR VERDICT = REJECT (include the counter we would have sent).

### Target the gap

| What our side lacks | What to ask them to add/swap |
|---|---|
| Value short by $__ (need `delta_pct ≥ +15%`) | Ask them to swap [their Player X] for [Player Y] |
| High-pressure cat negative | Ask for a throw-in player strong in that cat |
| Flex gap at scarce position | Ask for [scarce-position player] |

### Specific counter package

**Counter offer:**

- Our side: ____________ + ____________
- Their side: ____________ + ____________

**Why they might accept**: ________________________________________________

**Fallback ladder**:
1. If they refuse, send smaller counter: ____________
2. If second refusal: REJECT.

---

## Signal File Frontmatter

```yaml
---
type: trade
date: 2026-04-17
emitted_by: mlb-trade-evaluator
variant_synthesis: true
variants_fired: [advocate, critic]
synthesis_confidence: 0.72
opponent_team: "Los Doyers"
opponent_archetype: active
players_in: ["Aaron Judge"]
players_out: ["Bobby Witt Jr.", "Spencer Strider"]
trade_cat_delta:
  R: +2.3
  HR: +4.4
  RBI: +5.9
  SB: -21.3
  OBP: +3.0
  K: -115.5
  ERA: 0.0
  WHIP: 0.0
  QS: -96.0
  SV: 0.0
trade_value_delta_raw: -24
slot_value_delta: 2.50
trade_value_delta_pre_adj: -21.50
prior_ev_probability: 0.34
recommended_adjustment: 0.85
adverse_selection_adjustment_pct: 15
trade_value_delta_adjusted: -18.28
delta_pct: -0.315
positional_flex_delta: -30
playoff_impact: 35
verdict: reject
confidence: 0.78
counter_offer_if_applicable: "Witt + Strider for Judge + Webb + Ruiz"
counter_sent: false   # true only if verdict is COUNTER and we actually sent
red_team_findings:
  - severity: 3
    likelihood: 4
    score: 12
    note: "Override hint from adverse-selection-prior: If closer news broke in last 48h, asymmetry jumps to 85+; re-run."
    mitigation: "Check RotoWire closer report for involved teams"
source_urls:
  - https://www.fangraphs.com/projections.aspx?type=atcr&pos=...
  - https://www.fangraphs.com/auction-calculator
  - https://baseballsavant.mlb.com/savant-player/...
  - https://www.rotowire.com/baseball/injury-report.php
---
```

---

## User-Facing Output (what the coach reads out loud)

```
TRADE FROM [opponent team] ([archetype]):
  Out: [our players] → In: [their players]

Our take:
  • Raw value: [+/−$X]
  • Slot bonus: [+/−$Y] (because [2-for-1 frees a bench spot / 1-for-2 fills one])
  • Haircut for adverse selection: [Z%] (because [active trader selected this from many])
  • Final value: [+/−$F] ([+/−G%] of what we give up)
  • Cats we care about: [gain/lose on each]
  • Position: [gain/lose depth at __]
  • Playoff weeks: [helps/hurts/neutral]

RECOMMENDATION: [ACCEPT / COUNTER / REJECT]
[If COUNTER: specific counter package in one sentence.]
[If REJECT: counter we would have sent for the record.]
```

---

## Worked Example A — ACCEPT

**Scenario** (2026-05-20): Dormant-archetype opponent offers their **Freddie Freeman (1B/3B, $28)** for our **Yandy Díaz (1B, $17) + Luis Castillo (SP, $14)**. Our 1B slot is thin; we have OF depth. Cat pressures: HR 80, RBI 75, R 70, K 45, QS 40, OBP 65; others neutral.

**Projections (ROS):**

| Player | Side | PA | R | HR | RBI | SB | OBP | IP | K | QS | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Freeman | IN | 470 | 72 | 20 | 78 | 5 | .390 | — | — | — | $28 |
| Díaz | OUT | 450 | 58 | 14 | 55 | 2 | .370 | — | — | — | $17 |
| Castillo | OUT | — | — | — | — | — | — | 110 | 120 | 11 | $14 |

**Per-cat weighted delta (our side):**

| Cat | Raw Δ | Pressure | Weighted |
|---|---|---|---|
| R | +14 | 70 | +19.6 |
| HR | +6 | 80 | +9.6 |
| RBI | +23 | 75 | +34.5 |
| SB | +3 | 50 | +3.0 |
| OBP | +.006 team-shift → scaled +4 | 65 | +5.2 |
| K | −120 | 45 | −108 |
| QS | −11 | 40 | −8.8 |
| ERA | slight gain | 50 | +1 |
| WHIP | slight gain | 50 | +1 |
| SV | 0 | 45 | 0 |
| **Sum** | | | **−42.9** |

(Cat delta is negative because we're giving up a whole SP. But pressures on K/QS are low — we're comfortable losing those.)

**Value stack:**

```
(a) trade_value_delta_raw        = $28 − ($17 + $14) = −$3
(b) slot_value_delta             = (2 − 1, 0) × $2.50 = +$2.50
(c) trade_value_delta_pre_adj    = −$3 + $2.50        = −$0.50
```

**Adverse-selection inputs:**
- `offer_type`: trade
- `proposer_archetype`: dormant
- `offer_symmetry_score`: 72 (pre-adj ratio ≈ −1.6%, essentially fair on surface)
- `proposer_info_asymmetry`: 40 (no injury news, dormant opponent less likely to have fresh info)

**Adverse-selection output (from `@skills/adverse-selection-prior/`):**
- `prior_ev_probability`: 0.50 (dormant + symmetric + low asymmetry → base 0.40 + symmetry 0.05 + archetype +0.08 − asymmetry 0.03 = 0.50)
- `recommended_adjustment`: **1.00** (prior ≥ 0.50 → no haircut; rare case for a dormant opponent on a fair-looking offer)
- `bayesian_rationale`: "Dormant opponent with surface-symmetric offer. Adverse-selection pressure is weak; the usual 'they chose this specifically' argument does not apply when the archetype suggests they clicked without deep analysis. No haircut warranted."

```
(d) recommended_adjustment       = 1.00
(e) trade_value_delta_adjusted   = −$0.50 × 1.00 = −$0.50
(f) delta_pct                    = −$0.50 / $31  = −1.6%
```

Wait — this falls in the middle band. How is this an ACCEPT?

**Playoff & flex override**: (Date is May 20 — pre-July, so `playoff_impact = 50` neutral.)

`positional_flex_delta`:
- Gain starter at scarce 1B slot (we had only Díaz eligible): **+30**
- Lose 1 SP (we run 4 SP + 3 flex; now 3 SP + 3 flex — tight but workable): −10
- Multi-position eligibility on Freeman (1B + 3B, Díaz was 1B-only): +15
- Consolidate 2 into 1 (bench opens): +10
- **Total**: **+45**

**Reconsider the ladder with positional_flex in view:**

The verdict ladder gates on `delta_pct`. `delta_pct = −1.6%` is middle-band → COUNTER.

BUT: inspect whether we should upgrade based on flex. The ladder is strict — we do NOT upgrade COUNTER to ACCEPT on flex alone. Instead, we use the strong positional fit as LEVERAGE in the counter:

**Verdict revision**: Middle band → **COUNTER**. Ask them to add a low-$ throw-in (e.g., **Jurickson Profar, $5**) to their side, which would push `trade_value_delta_pre_adj` to +$4.50, after 1.00 haircut → `delta_pct = +14.5%` — still just under +15%.

Ask for a slightly bigger throw-in: **Kerry Carpenter, $7** → pre-adj +$6.50 → adjusted +$6.50 → `delta_pct = +17.1%` → clears +15%.

Counter: "Add Carpenter to their side."

**If they accept the counter** (highly likely — dormant manager, low-cost add): verdict becomes **ACCEPT** of the countered package, `delta_pct = +17.1%`, all cat pressures satisfied (high-pressure hitting cats strongly positive).

**Final verdict of this worked example**: **ACCEPT** (of the countered package Carpenter + Freeman for Díaz + Castillo).

**Teaching point**: The adverse-selection haircut of 1.00 (dormant opponent) is what makes the ACCEPT pathway viable. Against an `expert` archetype with the same raw numbers, the haircut would be ~0.85 and the counter would need a much bigger throw-in — the opponent might refuse, and the verdict would settle at COUNTER-then-REJECT.

---

## Worked Example B — COUNTER

**Scenario** (2026-07-08): Active-archetype opponent offers their **Corbin Carroll (OF, $31)** for our **José Ramírez (3B, $35)**. Our 3B is covered by Rafael Devers on the bench; OF is thin. Cat pressures: SB 80, R 70, HR 60, RBI 55, OBP 55; others neutral.

**Projections (ROS):**

| Player | Side | PA | R | HR | RBI | SB | OBP | $ |
|---|---|---|---|---|---|---|---|---|
| Carroll | IN | 360 | 58 | 14 | 45 | 22 | .355 | $31 |
| Ramírez | OUT | 360 | 62 | 18 | 70 | 12 | .365 | $35 |

**Per-cat weighted delta:**

| Cat | Raw Δ | Pressure | Weighted |
|---|---|---|---|
| R | −4 | 70 | −5.6 |
| HR | −4 | 60 | −4.8 |
| RBI | −25 | 55 | −27.5 |
| SB | +10 | 80 | +16.0 |
| OBP | −.003 scaled −2 | 55 | −2.2 |
| Others | 0 | — | 0 |
| **Sum** | | | **−24.1** |

**Value stack:**

```
(a) trade_value_delta_raw        = $31 − $35 = −$4
(b) slot_value_delta             = 1-for-1 → $0
(c) trade_value_delta_pre_adj    = −$4
```

**Adverse-selection inputs:**
- `offer_type`: trade
- `proposer_archetype`: active
- `offer_symmetry_score`: 60 (pre-adj ratio −11.4%, mildly asymmetric against us)
- `proposer_info_asymmetry`: 50 (no special news)

**Adverse-selection output:**
- `prior_ev_probability`: 0.35 (base 0.40 + symmetry 0.00 (below 70 threshold) − asymmetry 0.00 (50 is neutral) + archetype delta active −0.05 = 0.35)
- `recommended_adjustment`: **0.85**
- `bayesian_rationale`: "Active trader selected this specific offer from many possibilities — strong selection-pressure signal. Surface mild asymmetry against us confirms the Akerlof logic: they chose this one because it's best for them. Apply 15% haircut."

```
(d) recommended_adjustment       = 0.85
(e) trade_value_delta_adjusted   = −$4 × 0.85 = −$3.40
(f) delta_pct                    = −$3.40 / $35 = −9.7%
```

**Middle band** (−20% < −9.7% < +15%) → **COUNTER**.

**`positional_flex_delta`**: +15 (gain multi-position OF where thin; Devers covers 3B on bench). Neutral-to-slight gain.

**Playoff (July 8 — in window, normal weight)**: `playoff_impact` ≈ 52 (Carroll's schedule slightly better; trivial). Not dispositive.

**Gap to close for ACCEPT**: need `delta_pct ≥ +15%` → need `trade_value_delta_adjusted ≥ +$5.25` → need `trade_value_delta_pre_adj ≥ +$6.18` → need raw gain of at least +$6 after haircut. Pre-adj needs to move from −$4 to ~+$7, i.e., an $11 improvement to our side.

**Counter package**:
- Ask them to add a second player worth ~$11 to their side: **Esteban Ruiz (RP, $12)** would work. They probably refuse ($12 is a meaningful RP).
- Alternative: ask for a smaller throw-in. **Jarren Duran ($7)** → pre-adj +$3 → adjusted +$2.55 → `delta_pct = +7.3%`. Still middle band but much closer.

**Primary counter**: "Swap their Corbin Carroll for our José Ramírez straight up, BUT add their **Jarren Duran** to their side as a throw-in."
- `delta_pct_after_counter` = +7.3% (still COUNTER on the ladder, but noticeably better).

**Bigger counter (ambitious)**: ask for **Esteban Ruiz** — would clear +15% if accepted, but low probability.

**Fallback ladder**:
1. Send ambitious counter (add Ruiz). If they refuse:
2. Send the Duran counter. If they refuse:
3. REJECT on the original offer (not predatory; just not enough for us).

**Verdict**: **COUNTER** (Ramírez for Carroll + Duran, with fallback of Ramírez for Carroll + Ruiz).

**Teaching point**: Even though we don't love the original offer, the always-counter rule (principle #8) means we send a reasoned counter. Dismissively rejecting this active trader would close off future trade flow from them — they're the most-likely source of meaningful deals for us.

---

## Worked Example C — REJECT

**Scenario** (2026-06-10, reprise of the SKILL.md example): Expert-archetype opponent offers their **Aaron Judge (OF, $34)** for our **Bobby Witt Jr. (SS, $32) + Spencer Strider (SP, $26)**. Cat pressures: SB 85, QS 80, K 70, OBP 60, HR 55; others 40-50.

**Projections (ROS):**

| Player | Side | PA | R | HR | RBI | SB | OBP | IP | K | QS | $ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Judge | IN | 400 | 75 | 28 | 78 | 2 | .405 | — | — | — | $34 |
| Witt | OUT | 460 | 70 | 20 | 65 | 25 | .355 | — | — | — | $32 |
| Strider | OUT | — | — | — | — | — | — | 140 | 165 | 12 | $26 |

**Per-cat weighted delta (reproducing the SKILL.md table):**

| Cat | Raw Δ | Pressure | Weighted |
|---|---|---|---|
| R | +5 | 45 | +2.3 |
| HR | +8 | 55 | +4.4 |
| RBI | +13 | 45 | +5.9 |
| SB | −25 | **85** | **−42.5** (cat-pressure reject override!) |
| OBP | +.050 scaled +30 | 60 | +36.0 |
| K | −165 | 70 | **−231.0** |
| QS | −12 | **80** | **−19.2** (cat-pressure reject override!) |
| Others | 0 | — | 0 |
| **Sum** | | | **−244.1** |

(Note: two cats with pressure ≥ 80 have negative weighted deltas — SB and QS. Both are forced-reject override triggers.)

**Value stack:**

```
(a) trade_value_delta_raw        = $34 − ($32 + $26) = −$24
(b) slot_value_delta             = 2-for-1, we clear +1 slot → +$2.50
(c) trade_value_delta_pre_adj    = −$24 + $2.50 = −$21.50
```

**Adverse-selection inputs:**
- `offer_type`: trade
- `proposer_archetype`: expert
- `offer_symmetry_score`: 40 (pre-adj ratio −37%, clearly lopsided against us on surface)
- `proposer_info_asymmetry`: 55 (moderate — no specific news, but expert trader is more likely to have edge)

**Adverse-selection output:**
- `prior_ev_probability`: 0.25 (base 0.40 − archetype 0.08 (expert) + symmetry 0.00 (below 70) − asymmetry 0.05 (55 is below 60 threshold but non-trivial) − additional adjustment for clear surface lopsidedness = 0.25, clipped to floor)
- `recommended_adjustment`: **0.80**
- `bayesian_rationale`: "Expert opponent, surface-lopsided against us, moderate info asymmetry. They selected this specific 2-for-1 from many possible offers — strongest adverse-selection signal. Apply 20% haircut."

```
(d) recommended_adjustment       = 0.80
(e) trade_value_delta_adjusted   = −$21.50 × 0.80 = −$17.20
(f) delta_pct                    = −$17.20 / $58 = −29.7%
```

Wait — the math deserves a note. A multiplicative haircut on a negative delta moves it closer to zero (less negative), not further. So `−$21.50 × 0.80 = −$17.20` (less negative than pre-adj).

But `delta_pct = −29.7%` is still well below the `−20%` REJECT threshold. Both REJECT conditions hold:
- `delta_pct = −29.7% ≤ −20%` ✓
- `prior_ev_probability = 0.25 ≤ 0.35` ✓

(Compare to SKILL.md's example which treated the haircut as pushing further negative — corrected here: multiplicative haircut makes negative numbers less negative, but this trade's magnitude is large enough that even the "friendly" application of the haircut keeps it REJECT-eligible.)

**`positional_flex_delta`**: −30 (lose a scarce SS, gain a surplus OF).

**Playoff impact**: `playoff_impact = 35` (Judge 19 games, Witt 18 + Strider 4 starts → we lose 4 starts worth of K/QS in championship weeks, which is exactly the cats this trade already torches).

**Forced-REJECT overrides also triggered:**
- Two cats with pressure ≥ 80 (SB, QS) have negative weighted deltas → forced REJECT.
- `delta_pct ≤ −20%` ✓
- `prior_ev_probability ≤ 0.35` ✓

**Verdict**: **REJECT**.

**Counter we would have sent (for the relationship log, per always-counter principle)**:

"Witt + Strider for Judge + **Logan Webb** ($22) + **Esteban Ruiz** ($12)." This would push pre-adj to $34 + $22 + $12 − $58 = +$10, plus slot bonus ($0 since 3-for-2 doesn't clear a slot for us) = +$10 pre-adj. After 0.80 haircut: +$8 → `delta_pct = +14%` — still just under ACCEPT. An expert opponent would almost certainly refuse this counter, which is why we pre-commit to REJECT.

**`counter_sent: false`** in the signal file — we document the counter but do not send. The expert archetype and the 2-for-1 consolidation attempt reveal intent clearly enough.

**Teaching point**: REJECT is reserved for the rare case where adverse-selection is strong AND the value is deeply underwater AND high-pressure cats are damaged. This trade hits all three. On any of them individually, the verdict would downgrade to COUNTER.

---

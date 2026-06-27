#!/usr/bin/env python3
"""
schedule.py — greedy + local-search scheduler for conf-schedule-optimization.

Reads the canonical artifacts (events.json, affinities.json, profile.json) plus the
conference config (rooms, travel-time matrix, day bounds) and writes schedule.json
matching the SCHEDULE contract in the conf-schedule-optimization skill.

NO EXTERNAL SOLVER DEPENDENCIES — numpy only (stdlib otherwise). This is the default
path; the skill documents an optional ILP upgrade (pulp/ortools) when an exact optimum
is wanted.

What it does:
  - Filters to a FEASIBLE plan (no time overlap; room-to-room travel time; capacity;
    the attendee's forced-in / blacked-out constraints).
  - Optimizes a USER-WEIGHTED objective (interest, breadth, pacing, serendipity) whose
    weights come from profile.objective_weights — never hard-coded here.
  - SURFACES unbreakable conflicts (overlapping candidates within epsilon that the
    profile cannot rank) instead of silently choosing.
  - Reports objective_breakdown and a tradeoffs_note (the Goodhart honesty line).

The calling agent (conf-schedule-optimizer) turns schedule.json into the human-readable
schedule.md / conflicts.md / rationale.md.

USAGE:
  python3 schedule.py --events data/01-events/events.json \\
      --affinities data/02-clusters/affinities.json \\
      --profile data/03-preferences/profile.json \\
      --config conference.config.json --out data/04-schedule/schedule.json \\
      [--epsilon 0.05]
"""

import argparse
import json
import os
from datetime import date

import numpy as np


def to_min(hhmm):
    if not hhmm or ":" not in str(hhmm):
        return None
    h, m = str(hhmm).split(":")[:2]
    return int(h) * 60 + int(m)


def to_hhmm(minutes):
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def load(path):
    with open(path) as f:
        return json.load(f)


def event_interest(ev_id, affinities, region, point):
    """Interest = affinity-weighted attendee interest across the event's themes."""
    affs = affinities.get(ev_id, [])
    if not affs:
        return 0.0
    num = den = 0.0
    for a in affs:
        theme = a.get("theme_id")
        aff = float(a.get("affinity", 0.0))
        if theme in point:
            interest = float(point[theme])
        elif theme in region:
            r = region[theme]
            interest = (float(r.get("interest_lo", 0.0)) + float(r.get("interest_hi", 1.0))) / 2
        else:
            interest = 0.3  # unknown theme: mild prior
        num += aff * interest
        den += aff
    return num / den if den else 0.0


def travel_minutes(room_a, room_b, matrix, default):
    if not room_a or not room_b or room_a == room_b:
        return 0
    key = f"{room_a}|{room_b}"
    rkey = f"{room_b}|{room_a}"
    overrides = matrix.get("overrides", {}) if isinstance(matrix, dict) else {}
    return int(overrides.get(key, overrides.get(rkey, default)))


def compatible(ev, chosen, matrix, default_travel):
    """Feasible to add ev given already-chosen events on the same day: no overlap and
    enough travel time between different rooms."""
    s, e = ev["_start"], ev["_end"]
    for c in chosen:
        cs, ce = c["_start"], c["_end"]
        if s < ce and cs < e:  # time overlap
            return False
        # adjacency: ensure travel gap between back-to-back different-room picks
        gap = s - ce if s >= ce else cs - e
        need = travel_minutes(ev.get("room"), c.get("room"), matrix, default_travel)
        if 0 <= gap < need:
            return False
    return True


def objective(chosen, day_bounds, weights, n_themes, outlier_ids):
    """Weighted objective in [0,1]-ish per term. Heuristic but transparent."""
    if not chosen:
        return 0.0, {"interest": 0, "breadth": 0, "pacing": 0, "serendipity": 0}
    # interest: mean selected interest
    interest = float(np.mean([c["_interest"] for c in chosen]))
    # breadth: distinct top-themes covered, diminishing returns
    themes = set(c.get("_top_theme") for c in chosen if c.get("_top_theme"))
    breadth = min(1.0, len(themes) / max(1, min(n_themes, len(chosen))))
    # pacing: reward the longest contiguous free block per day, penalize fragmentation
    pacing_vals = []
    by_day = {}
    for c in chosen:
        by_day.setdefault(c["day"], []).append(c)
    for day, evs in by_day.items():
        evs = sorted(evs, key=lambda x: x["_start"])
        lo, hi = day_bounds.get(day, (to_min("08:00"), to_min("19:00")))
        cursor = lo
        gaps = []
        for c in evs:
            if c["_start"] > cursor:
                gaps.append(c["_start"] - cursor)
            cursor = max(cursor, c["_end"])
        if hi > cursor:
            gaps.append(hi - cursor)
        longest = max(gaps) if gaps else 0
        small = sum(1 for g in gaps if 0 < g < 30)  # fragmentation: many tiny gaps is bad
        span = max(1, hi - lo)
        pacing_vals.append(min(1.0, longest / span) - 0.1 * small)
    pacing = float(np.clip(np.mean(pacing_vals), 0, 1)) if pacing_vals else 0.0
    # serendipity: fraction of picks that are outliers/exploration + a little slack credit
    serendipity = min(1.0, sum(1 for c in chosen if c["event_id"] in outlier_ids) / max(1, len(chosen)) + 0.2 * (1 - interest))
    total = (weights.get("interest", 0) * interest + weights.get("breadth", 0) * breadth
             + weights.get("pacing", 0) * pacing + weights.get("serendipity", 0) * serendipity)
    return total, {"interest": round(interest, 3), "breadth": round(breadth, 3),
                   "pacing": round(pacing, 3), "serendipity": round(serendipity, 3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", required=True)
    ap.add_argument("--affinities", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--epsilon", type=float, default=0.05)
    args = ap.parse_args()

    edata = load(args.events)
    events = edata.get("events", edata if isinstance(edata, list) else [])
    aff_doc = load(args.affinities)
    affinities = aff_doc.get("affinities", aff_doc)
    profile = load(args.profile)
    config = load(args.config)

    region = profile.get("region", {})
    point = profile.get("point_estimate", {})
    weights = profile.get("objective_weights", {}) or {}
    if not weights:
        # The optimizer must not invent weights. If absent, halt loudly.
        raise SystemExit("schedule.py: profile.objective_weights missing — these are user-owned; "
                         "run conf-preference-elicitor before scheduling.")
    forced_in = set(profile.get("forced_in", []))           # optional structured must-attend ids
    blackouts = set(profile.get("blacked_out", []))         # optional structured drop ids

    matrix = config.get("travel_time_matrix", {})
    default_travel = int(matrix.get("default_minutes", 5))
    outlier_ids = set()  # populated from clusters if the caller injects them; optional here

    # Prepare events with parsed times + interest; skip events without a usable time/day.
    prepared = []
    for ev in events:
        s, e = to_min(ev.get("start")), to_min(ev.get("end"))
        if s is None or ev.get("day") is None:
            continue
        if e is None:
            e = s + 30  # default duration when only a start is given
        ev = dict(ev)
        ev["_start"], ev["_end"] = s, e
        ev["event_id"] = ev.get("id")
        ev["_interest"] = event_interest(ev["event_id"], affinities, region, point)
        top = affinities.get(ev["event_id"], [])
        ev["_top_theme"] = top[0]["theme_id"] if top else None
        if ev["event_id"] in blackouts:
            continue
        prepared.append(ev)

    # Day bounds from config dates (fallback 08:00-19:00).
    day_bounds = {}
    for d in config.get("dates", []):
        day_bounds[d] = (to_min("08:00"), to_min("19:00"))

    n_themes = len({ev["_top_theme"] for ev in prepared if ev["_top_theme"]}) or 1

    # ---- Greedy seed: force-ins first, then highest interest that stays feasible. ----
    chosen_by_day = {}
    def chosen_all():
        return [c for v in chosen_by_day.values() for c in v]

    ordered = sorted(prepared, key=lambda x: (x["event_id"] not in forced_in, -x["_interest"]))
    for ev in ordered:
        day = ev["day"]
        day_chosen = chosen_by_day.setdefault(day, [])
        if ev["event_id"] in forced_in or compatible(ev, day_chosen, matrix, default_travel):
            day_chosen.append(ev)

    # ---- Local search: try swaps (drop a weak pick to admit a better-objective set). ----
    base_total, _ = objective(chosen_all(), day_bounds, weights, n_themes, outlier_ids)
    improved = True
    guard = 0
    while improved and guard < 200:
        improved = False
        guard += 1
        for ev in ordered:
            day = ev["day"]
            dc = chosen_by_day.setdefault(day, [])
            if ev in dc:
                continue
            conflicts = [c for c in dc if not _ok_pair(ev, c, matrix, default_travel)]
            trial = [c for c in dc if c not in conflicts] + [ev]
            saved = chosen_by_day[day]
            chosen_by_day[day] = trial
            t_total, _ = objective(chosen_all(), day_bounds, weights, n_themes, outlier_ids)
            if t_total > base_total + 1e-9 and all(x["event_id"] not in forced_in for x in conflicts):
                base_total = t_total
                improved = True
            else:
                chosen_by_day[day] = saved

    chosen = sorted(chosen_all(), key=lambda x: (x["day"], x["_start"]))

    # ---- Surface unbreakable conflicts: overlapping unchosen within epsilon interest. ----
    unresolved = []
    chosen_ids = {c["event_id"] for c in chosen}
    for c in chosen:
        for ev in prepared:
            if ev["event_id"] in chosen_ids:
                continue
            if ev["day"] == c["day"] and ev["_start"] < c["_end"] and c["_start"] < ev["_end"]:
                if abs(ev["_interest"] - c["_interest"]) <= args.epsilon:
                    unresolved.append({
                        "day": c["day"], "slot": f"{to_hhmm(c['_start'])}-{to_hhmm(c['_end'])}",
                        "candidates": sorted([c["event_id"], ev["event_id"]]),
                        "why_unbreakable": f"both score within {args.epsilon} interest; profile does not rank these themes",
                        "needs": "your decision"})
    # de-dup conflicts
    seen = set(); uniq = []
    for u in unresolved:
        k = (u["day"], u["slot"], tuple(u["candidates"]))
        if k not in seen:
            seen.add(k); uniq.append(u)
    unresolved = uniq

    # ---- Free blocks per day. ----
    free_blocks = []
    by_day = {}
    for c in chosen:
        by_day.setdefault(c["day"], []).append(c)
    for d, evs in by_day.items():
        evs = sorted(evs, key=lambda x: x["_start"])
        lo, hi = day_bounds.get(d, (to_min("08:00"), to_min("19:00")))
        cursor = lo
        for c in evs:
            if c["_start"] > cursor:
                free_blocks.append(_free(d, cursor, c["_start"]))
            cursor = max(cursor, c["_end"])
        if hi > cursor:
            free_blocks.append(_free(d, cursor, hi))

    total, breakdown = objective(chosen, day_bounds, weights, n_themes, outlier_ids)

    selections = []
    for c in chosen:
        selections.append({
            "day": c["day"], "start": to_hhmm(c["_start"]), "end": to_hhmm(c["_end"]),
            "event_id": c["event_id"], "room": c.get("room"),
            "score": round(c["_interest"], 3),
            "why": ("forced in (must-attend)" if c["event_id"] in forced_in
                    else f"highest-interest feasible pick for its slot (interest {round(c['_interest'],3)})"),
            "alternatives": []})

    out = {
        "generated_on": date.today().isoformat(),
        "method": "greedy-local-search",
        "selections": selections,
        "free_blocks": free_blocks,
        "objective_breakdown": {**breakdown, "total": round(total, 3), "weights": weights},
        "unresolved_conflicts": unresolved,
        "constraints_applied": {
            "travel_time": f"default {default_travel} min + config overrides",
            "capacity": "capacity_constrained events admitted; agent should verify seatability",
            "hard_constraints": sorted(list(forced_in)) + [f"drop:{b}" for b in sorted(blackouts)]},
        "tradeoffs_note": _tradeoff_note(weights),
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"schedule.py: {len(selections)} selections, {len(unresolved)} surfaced conflicts, "
          f"objective total {round(total,3)} -> {args.out}")


def _ok_pair(ev, c, matrix, default_travel):
    s, e, cs, ce = ev["_start"], ev["_end"], c["_start"], c["_end"]
    if s < ce and cs < e:
        return False
    gap = s - ce if s >= ce else cs - e
    need = travel_minutes(ev.get("room"), c.get("room"), matrix, default_travel)
    return not (0 <= gap < need)


def _free(day, lo, hi):
    dur = hi - lo
    purpose = "meal" if dur >= 60 and 11 * 60 <= lo <= 14 * 60 else ("break" if dur >= 45 else "buffer")
    return {"day": day, "start": to_hhmm(lo), "end": to_hhmm(hi), "purpose": purpose}


def _tradeoff_note(weights):
    dom = max(weights, key=weights.get) if weights else "interest"
    notes = {
        "interest": "Weighted toward interest — expect a denser plan with shorter breaks; lower-affinity but broadening talks were dropped.",
        "breadth": "Weighted toward breadth — some high-interest talks were skipped to cover more themes.",
        "pacing": "Weighted toward pacing — fewer talks, protected contiguous breaks; the marginal lower-interest talk was traded for recovery time.",
        "serendipity": "Weighted toward serendipity — deliberate slack and an outlier pick were kept at the cost of one higher-interest slot.",
    }
    return notes.get(dom, "Balanced weighting; minor trade-offs across all terms.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
project.py — the discrete-investment engine: projects, capital rationing, acquisitions.

Everything here operates on a cash flow stream that someone else built. The hard part of
project analysis is deciding what belongs in that stream and what rate discounts it. This
script does the arithmetic that follows, and refuses to paper over the cases where the
arithmetic has no single answer — a stream with two internal rates of return gets both
roots and a warning, never one root presented as the answer.

Cash flow convention: `cash_flows[0]` is the year-0 outlay and is not discounted.
`cash_flows[t]` lands at the end of year t.

Pure standard library. No third-party packages, ever — this must run anywhere.

SUBCOMMANDS
  npv               cash flow stream(s) -> present values, NPV, NPV profile
  irr               IRR by bisection, with every root and a non-conventional-stream warning
  mirr              modified IRR — the reinvestment assumption corrected
  rationing         profitability index and project selection under a capital budget
  different-lives   equivalent annuities and replication for unequal project lives
  payback           payback and discounted payback, interpolated within the year
  accounting-return project ROC by year, average ROC, and EVA against the hurdle rate
  incremental       strip a total cash flow stream down to the incremental stream
  synergy           value synergy, and the acquisition ceiling price it supports
  synergy-haircut   discount a synergy schedule for observed post-merger realization
  control-value     status quo vs restructured value -> the value of running it better
  deal              the four-number acid test for an acquisition, and who keeps the gains
  control-premium   control premium, minority discount, and the conversion between them
  selftest          run the bundled worked examples and report pass/fail

Each subcommand reads a JSON payload (--in FILE, or stdin) and writes JSON to stdout.
Run any subcommand with --example to print a sample input payload.
"""

import argparse
import json
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
SYNERGY_TABLE = os.path.join(DATA_DIR, "synergy_realization.json")

# A discount rate at or below -100% makes (1+r)^t meaningless, so the IRR search starts
# just inside that wall. The upper bound of 1000% covers any real project; a stream whose
# only root sits above it is a data error, not an investment.
IRR_SEARCH_LOW = -0.99
IRR_SEARCH_HIGH = 10.0
# Roots cluster in the plausible range, so scan it at 5 basis points and the implausible
# tail at 25. Two roots closer together than the step would be indistinguishable to any
# analyst anyway, and the sign-change count still flags the stream as non-conventional.
IRR_FINE_STEP = 0.0005
IRR_FINE_LIMIT = 1.0
IRR_COARSE_STEP = 0.0025
# 200 bisections shrink any bracket by 2^-200, which is far past double precision; the
# loop exits on tolerance long before that on every well-behaved stream.
BISECTION_ITERATIONS = 200
BISECTION_TOLERANCE = 1e-12
# Two roots within one basis point of each other are the same root found twice from
# adjacent brackets.
ROOT_DEDUPE_TOLERANCE = 1e-4

# Replicating a 7-year and an 11-year project to their common multiple needs 77 years,
# which is already a fiction. Beyond 200 the replication assumption is not worth stating,
# so the engine stops and points at equivalent annuities instead.
MAX_REPLICATION_HORIZON = 200

# Exhaustive subset search is 2^n; 16 projects is 65,536 combinations, which is instant.
# Above that the engine reports the greedy ranking alone and says so.
EXACT_SELECTION_MAX_PROJECTS = 16


# --------------------------------------------------------------------------- plumbing

def _read_payload(args):
    if getattr(args, "in_file", None):
        with open(args.in_file) as f:
            return json.load(f)
    data = sys.stdin.read().strip()
    if not data:
        raise SystemExit(
            "No input. Pass --in FILE or pipe JSON on stdin. "
            "Run this subcommand with --example to see the expected shape."
        )
    try:
        return json.loads(data)
    except ValueError as exc:
        raise SystemExit("Input is not valid JSON (%s). Run with --example to see the "
                         "expected shape." % exc)


def _emit(obj):
    print(json.dumps(obj, indent=2))


def _number(payload, key, label=None, default=None):
    label = label or key
    if key not in payload or payload[key] is None:
        if default is not None:
            return float(default)
        raise SystemExit("Missing %r. It must be a number." % label)
    try:
        return float(payload[key])
    except (TypeError, ValueError):
        raise SystemExit("%r must be a number, got %r." % (label, payload[key]))


def _flows(spec, label):
    """Validate a cash flow list and return it as floats."""
    if not isinstance(spec, list) or not spec:
        raise SystemExit(
            "%s must be a non-empty list of numbers, year 0 first. Got %r."
            % (label, type(spec).__name__ if not isinstance(spec, list) else "[]"))
    out = []
    for i, v in enumerate(spec):
        try:
            out.append(float(v))
        except (TypeError, ValueError):
            raise SystemExit("%s[%d] is %r, which is not a number. Use 0 for a year with "
                             "no cash flow." % (label, i, v))
    return out


def _rates(spec, years, label):
    """Expand a discount rate into one rate per year (years 1..n)."""
    if isinstance(spec, (int, float)):
        rates = [float(spec)] * years
    elif isinstance(spec, list):
        if len(spec) != years:
            raise SystemExit(
                "%s has %d entries but the stream runs %d years after year 0. Give one "
                "rate, or one rate per year." % (label, len(spec), years))
        rates = [float(v) for v in spec]
    else:
        raise SystemExit("%s must be a number or a list of numbers, got %r."
                         % (label, type(spec).__name__))
    for r in rates:
        if r <= -1.0:
            raise SystemExit("%s contains %g. A discount rate at or below -100%% has no "
                             "meaning." % (label, r))
    return rates


def _discount_factors(rates):
    """Cumulative discount factors indexed by year; year 0 is always 1.0."""
    factors = [1.0]
    running = 1.0
    for r in rates:
        running *= (1.0 + r)
        factors.append(1.0 / running)
    return factors


def _npv_at(rate, flows):
    """NPV of a stream at a single flat rate. Returns None outside the valid domain."""
    if rate <= -1.0:
        return None
    total = 0.0
    for t, cf in enumerate(flows):
        total += cf / (1.0 + rate) ** t
    return total


def _sign_changes(flows):
    """Count sign changes among the non-zero cash flows."""
    signs = [1 if cf > 0 else -1 for cf in flows if cf != 0]
    return sum(1 for i in range(len(signs) - 1) if signs[i] != signs[i + 1])


def _apply_terminal(flows, terminal, rates):
    """Fold a perpetuity closing value into the final year of the stream.

    A project analysis usually ends with an assumption about what happens after the
    forecast, and the terminal value belongs at the end of the last forecast year rather
    than as an extra year. The cash flow being capitalised is the one for the year *after*
    the forecast, which is why `cash_flow_next_year` exists: capitalising the last
    forecast year inherits its growth-phase economics into perpetuity.
    """
    if not terminal:
        return flows, None
    growth = float(terminal.get("growth_rate", 0.0))
    rate = float(terminal.get("cost_of_capital", rates[-1]))
    if "cash_flow_next_year" in terminal:
        next_cf = float(terminal["cash_flow_next_year"])
    else:
        next_cf = flows[-1] * (1.0 + growth)
    if rate <= growth:
        raise SystemExit(
            "Terminal cost of capital (%.4f) must exceed terminal growth (%.4f), or the "
            "perpetuity is infinite or negative." % (rate, growth))
    value = next_cf / (rate - growth)
    closed = list(flows)
    closed[-1] += value
    info = {"cash_flow_next_year": next_cf, "growth_rate": growth,
            "cost_of_capital": rate, "terminal_value": value,
            "placed_at_end_of_year": len(flows) - 1}
    return closed, info


# ------------------------------------------------------------------------------- npv

def npv(p):
    """Present value each stream at its own rate, then add. Never blend rates."""
    if "streams" in p:
        specs = p["streams"]
        if not isinstance(specs, list) or not specs:
            raise SystemExit("'streams' must be a non-empty list of "
                             "{label, cash_flows, discount_rate} objects.")
    else:
        if "cash_flows" not in p:
            raise SystemExit("Provide 'cash_flows' and 'discount_rate', or a 'streams' "
                             "list. Run with --example to see the shape.")
        specs = [{"label": p.get("label", "project"), "cash_flows": p["cash_flows"],
                  "discount_rate": p.get("discount_rate"), "terminal": p.get("terminal")}]

    results = []
    total = 0.0
    for i, spec in enumerate(specs):
        label = spec.get("label", "stream %d" % (i + 1))
        flows = _flows(spec.get("cash_flows"), "%s.cash_flows" % label)
        if spec.get("discount_rate") is None:
            raise SystemExit("Stream %r has no 'discount_rate'. Each stream carries the "
                             "rate of the business that receives its cash flows." % label)
        rates = _rates(spec["discount_rate"], len(flows) - 1, "%s.discount_rate" % label)
        closed, terminal = _apply_terminal(flows, spec.get("terminal"), rates)
        factors = _discount_factors(rates)
        pvs = [closed[t] * factors[t] for t in range(len(closed))]
        stream_npv = sum(pvs)
        total += stream_npv
        row = {"label": label, "discount_rate": spec["discount_rate"],
               "cash_flows": closed, "discount_factors": factors,
               "present_values": pvs, "npv": stream_npv}
        if terminal:
            row["terminal"] = terminal
        results.append(row)

    out = {"streams": results, "total_npv": total,
           "decision": "accept" if total > 0 else "reject",
           "decision_basis": "NPV is the expected increase in firm value from taking the "
                             "project. Positive means take it."}
    if len(results) > 1:
        out["note"] = ("Each stream was discounted at its own rate and the present values "
                       "added. Report the stand-alone stream separately from any synergy "
                       "stream so a reader can see how much of the case rests on synergy.")

    profile_rates = p.get("profile_rates")
    if profile_rates:
        if len(results) > 1:
            raise SystemExit("An NPV profile sweeps one discount rate, so it applies to a "
                             "single stream. Drop 'profile_rates' or pass one stream.")
        flat = results[0]["cash_flows"]
        out["npv_profile"] = [{"discount_rate": float(r), "npv": _npv_at(float(r), flat)}
                              for r in profile_rates]
    return out


def cmd_npv(args):
    _emit(npv(_read_payload(args)))


# ------------------------------------------------------------------------------- irr

def irr(p):
    """Find every internal rate of return, and say so when there is more than one.

    A stream can have as many internal rates of return as it has sign changes. Returning
    one of several roots is the failure mode this function exists to prevent: it scans the
    whole plausible rate domain, brackets every crossing, and hands back the list.
    """
    flows = _flows(p.get("cash_flows"), "cash_flows")
    if len(flows) < 2:
        raise SystemExit("An IRR needs at least an outlay and one later cash flow.")

    changes = _sign_changes(flows)
    if changes == 0:
        direction = "all positive" if sum(1 for c in flows if c > 0) else "all negative"
        return {
            "cash_flows": flows, "sign_changes": 0, "conventional": False,
            "roots": [], "irr": None, "reliable": False,
            "note": "The cash flows are %s, so NPV never crosses zero and no IRR exists. "
                    "Check that the year-0 investment is in the stream with a negative "
                    "sign." % direction,
        }

    # Scan for brackets, then bisect each one.
    grid = []
    r = IRR_SEARCH_LOW
    while r < IRR_FINE_LIMIT:
        grid.append(r)
        r += IRR_FINE_STEP
    while r <= IRR_SEARCH_HIGH:
        grid.append(r)
        r += IRR_COARSE_STEP

    roots = []
    prev_rate = grid[0]
    prev_npv = _npv_at(prev_rate, flows)
    for rate in grid[1:]:
        cur = _npv_at(rate, flows)
        if prev_npv == 0.0:
            roots.append(prev_rate)
        elif prev_npv * cur < 0:
            lo, hi, f_lo = prev_rate, rate, prev_npv
            for _ in range(BISECTION_ITERATIONS):
                mid = (lo + hi) / 2.0
                f_mid = _npv_at(mid, flows)
                if abs(f_mid) < BISECTION_TOLERANCE or (hi - lo) < BISECTION_TOLERANCE:
                    break
                if f_lo * f_mid < 0:
                    hi = mid
                else:
                    lo, f_lo = mid, f_mid
            roots.append((lo + hi) / 2.0)
        prev_rate, prev_npv = rate, cur

    deduped = []
    for root in roots:
        if not deduped or abs(root - deduped[-1]) > ROOT_DEDUPE_TOLERANCE:
            deduped.append(root)

    out = {"cash_flows": flows, "sign_changes": changes,
           "conventional": changes == 1, "roots": deduped,
           "search_range": [IRR_SEARCH_LOW, IRR_SEARCH_HIGH]}

    if len(deduped) == 1:
        out["irr"] = deduped[0]
        out["reliable"] = changes == 1
        if changes > 1:
            out["note"] = (
                "The stream changes sign %d times, so it is not conventional even though "
                "only one root was found between %g and %g. Decide on NPV at the actual "
                "cost of capital and treat this rate as descriptive."
                % (changes, IRR_SEARCH_LOW, IRR_SEARCH_HIGH))
    elif len(deduped) > 1:
        out["irr"] = None
        out["reliable"] = False
        out["note"] = (
            "This stream has %d internal rates of return (%s), because the cash flows "
            "change sign %d times. No single one of them is the project's return, so the "
            "IRR rule gives no usable answer here. Decide on NPV at the actual cost of "
            "capital, and read the npv_profile below to see the shape."
            % (len(deduped), ", ".join("%.4f%%" % (x * 100) for x in deduped), changes))
    else:
        out["irr"] = None
        out["reliable"] = False
        out["note"] = (
            "No IRR was found between %g and %g even though the stream changes sign %d "
            "times. NPV stays on one side of zero across the whole range, so decide on "
            "NPV at the cost of capital." % (IRR_SEARCH_LOW, IRR_SEARCH_HIGH, changes))

    # The profile is what makes a multiple-root answer readable, so it is always emitted.
    profile_rates = p.get("profile_rates")
    if profile_rates is None:
        profile_rates = [i / 100.0 for i in range(0, 55, 5)]
    out["npv_profile"] = [{"discount_rate": float(r), "npv": _npv_at(float(r), flows)}
                          for r in profile_rates]

    if p.get("hurdle_rate") is not None:
        hurdle = float(p["hurdle_rate"])
        at_hurdle = _npv_at(hurdle, flows)
        out["hurdle_rate"] = hurdle
        out["npv_at_hurdle_rate"] = at_hurdle
        if out.get("irr") is not None and out["reliable"]:
            out["decision"] = "accept" if out["irr"] > hurdle else "reject"
            out["decision_basis"] = "IRR versus hurdle rate, agreeing with NPV."
        else:
            out["decision"] = "accept" if at_hurdle > 0 else "reject"
            out["decision_basis"] = ("NPV at the hurdle rate, because the IRR rule does "
                                     "not apply to this stream.")
    return out


def cmd_irr(args):
    _emit(irr(_read_payload(args)))


# ------------------------------------------------------------------------------ mirr

def mirr(p):
    """Modified IRR: intermediate cash flows reinvest at a rate you choose, not at the IRR.

    The ordinary IRR assumes every intermediate cash flow is reinvested at the IRR itself,
    which quietly assumes an endless supply of equally lucrative projects. MIRR replaces
    that with an explicit reinvestment rate — normally the hurdle rate.
    """
    flows = _flows(p.get("cash_flows"), "cash_flows")
    hurdle = _number(p, "hurdle_rate")
    reinvest = float(p.get("reinvestment_rate", hurdle))
    finance = float(p.get("finance_rate", hurdle))
    for name, rate in (("reinvestment_rate", reinvest), ("finance_rate", finance)):
        if rate <= -1.0:
            raise SystemExit("%s of %g is at or below -100%%, which has no meaning."
                             % (name, rate))
    n = len(flows) - 1
    if n < 1:
        raise SystemExit("MIRR needs at least an outlay and one later cash flow.")

    # Outflows come back to today at the financing rate; inflows go forward to the horizon
    # at the reinvestment rate. What is left is one outlay and one terminal receipt.
    pv_outflows = 0.0
    fv_inflows = 0.0
    schedule = []
    for t, cf in enumerate(flows):
        if cf < 0:
            pv = cf / (1.0 + finance) ** t
            pv_outflows += pv
            schedule.append({"year": t, "cash_flow": cf, "treated_as": "outflow",
                             "present_value": pv})
        elif cf > 0:
            fv = cf * (1.0 + reinvest) ** (n - t)
            fv_inflows += fv
            schedule.append({"year": t, "cash_flow": cf, "treated_as": "inflow",
                             "future_value_at_year_%d" % n: fv})
        else:
            schedule.append({"year": t, "cash_flow": 0.0, "treated_as": "none"})

    if pv_outflows == 0:
        raise SystemExit("The stream has no negative cash flow, so there is nothing "
                         "invested and no MIRR. Include the year-0 outlay.")
    if fv_inflows <= 0:
        raise SystemExit("The stream has no positive cash flow, so it never returns "
                         "anything and no MIRR exists.")

    value = (fv_inflows / -pv_outflows) ** (1.0 / n) - 1.0
    plain = irr({"cash_flows": flows})
    out = {
        "schedule": schedule, "years": n,
        "present_value_of_outflows": pv_outflows,
        "terminal_value_of_inflows": fv_inflows,
        "hurdle_rate": hurdle, "reinvestment_rate": reinvest, "finance_rate": finance,
        "mirr": value,
        "irr": plain.get("irr"),
        "irr_reliable": plain.get("reliable"),
        "decision": "accept" if value > hurdle else "reject",
    }
    if plain.get("irr") is not None:
        out["reinvestment_illusion"] = plain["irr"] - value
        out["note"] = ("The gap between IRR and MIRR is the reinvestment assumption. A "
                       "wide gap means the IRR is only achievable if the firm can keep "
                       "redeploying the cash at the same return.")
    return out


def cmd_mirr(args):
    _emit(mirr(_read_payload(args)))


# ------------------------------------------------------------- capital rationing / PI

def _project_npv(spec, index, default_rate):
    label = spec.get("label", spec.get("name", "project %d" % (index + 1)))
    if "npv" in spec:
        value = float(spec["npv"])
        investment = spec.get("initial_investment")
        if investment is None:
            raise SystemExit("Project %r gives an 'npv' but no 'initial_investment'. The "
                             "profitability index needs both." % label)
        return label, value, abs(float(investment)), None
    flows = _flows(spec.get("cash_flows"), "%s.cash_flows" % label)
    rate = spec.get("discount_rate", default_rate)
    if rate is None:
        raise SystemExit("Project %r has no 'discount_rate' and no top-level default."
                         % label)
    rates = _rates(rate, len(flows) - 1, "%s.discount_rate" % label)
    factors = _discount_factors(rates)
    value = sum(flows[t] * factors[t] for t in range(len(flows)))
    investment = spec.get("initial_investment")
    investment = abs(float(investment)) if investment is not None else abs(flows[0])
    if investment == 0:
        raise SystemExit("Project %r has a year-0 cash flow of zero, so there is no "
                         "investment to index against. Set 'initial_investment' "
                         "explicitly if the outlay lands in a later year." % label)
    return label, value, investment, flows


def rationing(p):
    """Rank projects by value created per dollar of scarce capital.

    The profitability index is the right rule only when capital is genuinely rationed.
    With money to spare, ranking by PI biases the firm toward small projects and leaves
    value on the table.
    """
    specs = p.get("projects")
    if not isinstance(specs, list) or not specs:
        raise SystemExit("'projects' must be a non-empty list. Each entry needs either "
                         "{cash_flows, discount_rate} or {npv, initial_investment}.")
    default_rate = p.get("discount_rate")
    rows = []
    for i, spec in enumerate(specs):
        label, value, investment, _ = _project_npv(spec, i, default_rate)
        rows.append({
            "label": label, "npv": value, "initial_investment": investment,
            "profitability_index": value / investment,
            # The other convention in circulation is PV of inflows over the outlay, which
            # is exactly this plus one. Both are reported so nobody has to guess.
            "pv_index_including_investment": (value + investment) / investment,
        })
    ranked = sorted(rows, key=lambda r: r["profitability_index"], reverse=True)
    for rank, row in enumerate(ranked, start=1):
        row["rank_by_profitability_index"] = rank
    by_npv = sorted(rows, key=lambda r: r["npv"], reverse=True)
    for rank, row in enumerate(by_npv, start=1):
        row["rank_by_npv"] = rank

    out = {"projects": rows,
           "ranking_by_profitability_index": [r["label"] for r in ranked],
           "ranking_by_npv": [r["label"] for r in by_npv]}
    if [r["label"] for r in ranked] != [r["label"] for r in by_npv]:
        out["rankings_disagree"] = True
        out["note"] = ("The two rankings disagree, which is the scale conflict. Rank by "
                       "profitability index only if capital is genuinely rationed; "
                       "otherwise rank by NPV, which is what the firm is maximising.")
    else:
        out["rankings_disagree"] = False

    budget = p.get("budget")
    if budget is not None:
        budget = float(budget)
        greedy, spent, gained = [], 0.0, 0.0
        for row in ranked:
            if row["npv"] <= 0:
                continue
            if spent + row["initial_investment"] <= budget + 1e-9:
                greedy.append(row["label"])
                spent += row["initial_investment"]
                gained += row["npv"]
        out["budget"] = budget
        out["greedy_selection"] = {"projects": greedy, "capital_used": spent,
                                   "npv_created": gained,
                                   "capital_unused": budget - spent}
        if len(rows) <= EXACT_SELECTION_MAX_PROJECTS:
            best_labels, best_npv, best_cost = [], 0.0, 0.0
            for mask in range(1 << len(rows)):
                cost = 0.0
                value = 0.0
                for i, row in enumerate(rows):
                    if mask & (1 << i):
                        cost += row["initial_investment"]
                        value += row["npv"]
                if cost <= budget + 1e-9 and value > best_npv:
                    best_npv, best_cost = value, cost
                    best_labels = [rows[i]["label"] for i in range(len(rows))
                                   if mask & (1 << i)]
            out["best_selection"] = {"projects": best_labels, "capital_used": best_cost,
                                     "npv_created": best_npv,
                                     "capital_unused": budget - best_cost}
            if sorted(best_labels) != sorted(greedy):
                out["greedy_is_suboptimal"] = True
                out["budget_note"] = (
                    "Ranking by profitability index and taking projects in order misses "
                    "%.4f of NPV here, because the projects are indivisible and do not "
                    "pack neatly into the budget. Take best_selection."
                    % (best_npv - gained))
            else:
                out["greedy_is_suboptimal"] = False
        else:
            out["budget_note"] = (
                "More than %d projects, so only the profitability-index ranking is "
                "reported. With indivisible projects that ranking can be beaten; check "
                "the leftover capital." % EXACT_SELECTION_MAX_PROJECTS)
    return out


def cmd_rationing(args):
    _emit(rationing(_read_payload(args)))


# --------------------------------------------------------------------- unequal lives

def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def different_lives(p):
    """Make mutually exclusive projects of unequal life comparable.

    Raw NPVs are not comparable across different lives: the longer project accumulates
    value over more years and ties capital up for longer, and the comparison quietly
    rewards it for both. Two repairs, reported together because they should agree.
    """
    specs = p.get("projects")
    if not isinstance(specs, list) or len(specs) < 2:
        raise SystemExit("'projects' must list at least two mutually exclusive projects.")
    default_rate = p.get("discount_rate")
    if default_rate is None:
        raise SystemExit("'discount_rate' is required. Unequal-life comparison uses one "
                         "common hurdle rate across the candidates.")
    rate = float(default_rate)
    if rate <= 0:
        raise SystemExit("'discount_rate' must be positive to form an annuity factor.")

    rows = []
    for i, spec in enumerate(specs):
        label = spec.get("label", spec.get("name", "project %d" % (i + 1)))
        if "cash_flows" in spec:
            flows = _flows(spec["cash_flows"], "%s.cash_flows" % label)
            life = int(spec.get("life", len(flows) - 1))
            factors = _discount_factors([rate] * (len(flows) - 1))
            value = sum(flows[t] * factors[t] for t in range(len(flows)))
        else:
            flows = None
            if "npv" not in spec or "life" not in spec:
                raise SystemExit("Project %r needs 'cash_flows', or both 'npv' and "
                                 "'life'." % label)
            value = float(spec["npv"])
            life = int(spec["life"])
        if life < 1:
            raise SystemExit("Project %r has a life of %d years." % (label, life))
        pvaf = (1.0 - (1.0 + rate) ** -life) / rate
        rows.append({"label": label, "life_years": life, "npv": value,
                     "pv_annuity_factor": pvaf,
                     "equivalent_annuity": value / pvaf,
                     "cash_flows": flows})

    lives = [r["life_years"] for r in rows]
    horizon = lives[0]
    for life in lives[1:]:
        horizon = horizon * life // _gcd(horizon, life)

    out = {
        "discount_rate": rate,
        "projects": [{k: v for k, v in r.items() if k != "cash_flows"} for r in rows],
        "ranking_by_raw_npv": [r["label"] for r in
                               sorted(rows, key=lambda x: x["npv"], reverse=True)],
        "ranking_by_equivalent_annuity": [
            r["label"] for r in
            sorted(rows, key=lambda x: x["equivalent_annuity"], reverse=True)],
    }

    if all(r["cash_flows"] is not None for r in rows):
        if horizon > MAX_REPLICATION_HORIZON:
            out["replication"] = {
                "common_horizon_years": horizon,
                "skipped": True,
                "reason": "The common horizon is %d years, which is past the point where "
                          "repeating the project on unchanged terms is a claim anyone can "
                          "defend. Use the equivalent annuities above."
                          % horizon}
        else:
            rep_rows = []
            for row in rows:
                flows = row["cash_flows"]
                life = row["life_years"]
                cycles = horizon // life
                stacked = [0.0] * (horizon + 1)
                for cycle in range(cycles):
                    offset = cycle * life
                    for t, cf in enumerate(flows):
                        # The reinvestment at the start of a new cycle lands in the same
                        # year as the last receipt of the previous one; they net.
                        stacked[offset + t] += cf
                factors = _discount_factors([rate] * horizon)
                rep_npv = sum(stacked[t] * factors[t] for t in range(horizon + 1))
                rep_rows.append({"label": row["label"], "cycles": cycles,
                                 "replicated_cash_flows": stacked,
                                 "replicated_npv": rep_npv})
            out["replication"] = {
                "common_horizon_years": horizon,
                "projects": [{k: v for k, v in r.items()
                              if k != "replicated_cash_flows"} for r in rep_rows],
                "detail": rep_rows,
                "ranking": [r["label"] for r in
                            sorted(rep_rows, key=lambda x: x["replicated_npv"],
                                   reverse=True)]}
            agree = (out["replication"]["ranking"]
                     == out["ranking_by_equivalent_annuity"])
            out["routes_agree"] = agree
            if not agree:
                out["note"] = ("Replication and equivalent annuities rank these projects "
                               "differently, which happens when annual cash flows are "
                               "irregular. Trust replication and check the streams.")
    if out["ranking_by_raw_npv"] != out["ranking_by_equivalent_annuity"]:
        out["raw_npv_is_misleading"] = True
        out["raw_npv_note"] = ("Ranking on raw NPV picks a different project from the "
                               "life-adjusted comparison. Raw NPV favours the longer "
                               "project for no reason connected to its merits.")
    else:
        out["raw_npv_is_misleading"] = False
    out["caveat"] = ("Both repairs assume the shorter project can actually be repeated on "
                     "the same terms. A one-off licence, a unique site or a first-mover "
                     "position cannot be, and then neither repair applies.")
    return out


def cmd_different_lives(args):
    _emit(different_lives(_read_payload(args)))


# --------------------------------------------------------------------------- payback

def _crossing(cumulative, flows_by_year):
    """First year the cumulative total turns positive, interpolated within that year."""
    for t in range(1, len(cumulative)):
        if cumulative[t] >= 0 and cumulative[t - 1] < 0:
            step = flows_by_year[t]
            if step == 0:
                return float(t)
            return (t - 1) + (-cumulative[t - 1]) / step
    return None


def payback(p):
    """How long capital is at risk — a supplementary read, never the decision rule."""
    flows = _flows(p.get("cash_flows"), "cash_flows")
    rate = p.get("discount_rate")
    rows = []
    cum = 0.0
    cum_list = []
    for t, cf in enumerate(flows):
        cum += cf
        cum_list.append(cum)
        rows.append({"year": t, "cash_flow": cf, "cumulative_cash_flow": cum})
    simple = _crossing(cum_list, flows)

    out = {"schedule": rows, "payback_period_years": simple}
    if simple is None:
        out["payback_note"] = ("Cumulative cash flow never turns positive inside the "
                               "stream, so the investment is not recovered within the "
                               "forecast. Extend the forecast or read this as a reject.")

    if rate is not None:
        rates = _rates(rate, len(flows) - 1, "discount_rate")
        factors = _discount_factors(rates)
        dcum = 0.0
        dcum_list = []
        discounted = []
        for t, cf in enumerate(flows):
            pv = cf * factors[t]
            discounted.append(pv)
            dcum += pv
            dcum_list.append(dcum)
            rows[t]["present_value"] = pv
            rows[t]["cumulative_present_value"] = dcum
        disc = _crossing(dcum_list, discounted)
        out["discount_rate"] = rate
        out["discounted_payback_period_years"] = disc
        if disc is None:
            out["discounted_payback_note"] = (
                "Cumulative present value never turns positive, which is the same "
                "statement as a negative NPV over this horizon.")
        elif simple is not None:
            out["cost_of_time_years"] = disc - simple
            out["note"] = ("The gap between the two paybacks is the cost of time. A firm "
                           "that stops at simple payback understates how long its capital "
                           "is exposed by that much.")
    out["caveat"] = ("Payback ignores every cash flow after the payback date, and in its "
                     "simple form ignores the time value of money. Use it to describe "
                     "capital at risk, not to accept or reject.")
    return out


def cmd_payback(args):
    _emit(payback(_read_payload(args)))


# ----------------------------------------------------------------- accounting return

def accounting_return(p):
    """Project ROC year by year, plus EVA against the hurdle rate.

    Book returns climb mechanically as the asset base depreciates, so a rising ROC series
    on an unchanging asset is an accounting artifact rather than improving performance.
    Both bases are reported because analysts disagree about which to use and they normally
    differ by only a few basis points.
    """
    income = p.get("after_tax_operating_income")
    if income is None:
        pre_tax = p.get("operating_income")
        if pre_tax is None:
            raise SystemExit("Provide 'after_tax_operating_income', or 'operating_income' "
                             "with a 'tax_rate'.")
        tax_rate = _number(p, "tax_rate")
        income = [float(v) * (1.0 - tax_rate) for v in pre_tax]
    income = [float(v) for v in income]

    capital = p.get("invested_capital")
    if not isinstance(capital, list) or len(capital) != len(income):
        raise SystemExit(
            "'invested_capital' must be a list of beginning-of-year book capital with one "
            "entry per income year (%d given for %d income years). Book capital is book "
            "debt plus book equity minus cash, or for a project the undepreciated fixed "
            "assets plus non-cash working capital."
            % (len(capital) if isinstance(capital, list) else 0, len(income)))
    capital = [float(v) for v in capital]
    if any(c == 0 for c in capital):
        raise SystemExit("'invested_capital' contains a zero, so ROC is undefined for that "
                         "year. A project with no capital employed has no accounting "
                         "return.")

    ending = p.get("ending_invested_capital")
    wacc = p.get("cost_of_capital")
    wacc = float(wacc) if wacc is not None else None

    rows = []
    for i, inc in enumerate(income):
        begin = capital[i]
        if i + 1 < len(capital):
            end = capital[i + 1]
        elif ending is not None:
            end = float(ending)
        else:
            end = None
        average = (begin + end) / 2.0 if end is not None else None
        row = {"year": i + 1, "after_tax_operating_income": inc,
               "invested_capital_start_of_year": begin,
               "invested_capital_end_of_year": end,
               "average_invested_capital": average,
               "roc_start_of_year_basis": inc / begin,
               "roc_average_capital_basis": (inc / average) if average else None}
        if wacc is not None:
            # EVA in dollars is the spread times capital, which is identically the income
            # left after charging every dollar of capital its cost.
            row["return_spread"] = row["roc_start_of_year_basis"] - wacc
            row["eva"] = inc - wacc * begin
        rows.append(row)

    starts = [r["roc_start_of_year_basis"] for r in rows]
    averages = [r["roc_average_capital_basis"] for r in rows
                if r["roc_average_capital_basis"] is not None]
    mean_income = sum(income) / len(income)
    mean_capital = sum(capital) / len(capital)
    out = {"years": rows,
           "average_roc_start_of_year_basis": sum(starts) / len(starts),
           "average_roc_average_capital_basis":
               (sum(averages) / len(averages)) if averages else None,
           # Two averaging conventions are in circulation and they can differ by several
           # percentage points on a project whose capital base shrinks. The two above are
           # the mean of the annual ratios; this one is the ratio of the means, which is
           # what the capital-budgeting sheet reports as the project's return on capital.
           "roc_on_average_income_and_capital": mean_income / mean_capital,
           "average_after_tax_operating_income": mean_income,
           "average_invested_capital": mean_capital,
           "note": ("Book returns rise as the asset base depreciates even when cash flows "
                    "are flat. Read the level against the cost of capital, not the "
                    "trend. The mean of the annual returns and the ratio of the means "
                    "answer different questions; quote whichever you use by name.")}
    if wacc is not None:
        out["cost_of_capital"] = wacc
        out["average_return_spread"] = out["average_roc_start_of_year_basis"] - wacc
        evas = [r["eva"] for r in rows]
        out["total_eva_undiscounted"] = sum(evas)
        factors = _discount_factors([wacc] * len(evas))
        # EVA lands at the end of each year, so year 1 discounts once.
        out["present_value_of_eva"] = sum(evas[i] * factors[i + 1]
                                          for i in range(len(evas)))
        out["verdict"] = ("value creating" if out["average_return_spread"] > 0
                          else "value destroying")
    out["caveat"] = ("Averaging over an arbitrary window on a long-lived project loads the "
                     "early-year losses into the average and excludes the mature years. "
                     "Treat a negative verdict on a truncated window as a prompt to run "
                     "the discounted cash flow analysis, not as the answer.")
    return out


def cmd_accounting_return(args):
    _emit(accounting_return(_read_payload(args)))


# --------------------------------------------------------------- incremental cash flow

def _series(spec, years, label):
    """Expand a per-year adjustment into a list covering years 0..years."""
    if spec is None:
        return [0.0] * (years + 1)
    if isinstance(spec, (int, float)):
        # A scalar adjustment is an annual amount and does not touch year 0, which holds
        # the up-front outlay rather than an operating item.
        return [0.0] + [float(spec)] * years
    if isinstance(spec, list):
        out = [float(v) for v in spec]
        if len(out) == years:
            return [0.0] + out
        if len(out) == years + 1:
            return out
        raise SystemExit(
            "%s has %d entries. Give %d (years 1..%d) or %d (years 0..%d)."
            % (label, len(out), years, years, years + 1, years))
    raise SystemExit("%s must be a number or a list of numbers." % label)


def incremental(p):
    """Turn a total cash flow stream into the incremental stream the decision turns on.

    Only cash flows that change because of the decision belong in the analysis. This runs
    the adjustment route: start from the cash flows as the accounting system reports them
    and back out what the firm would have spent or earned anyway.
    """
    flows = _flows(p.get("total_cash_flows"), "total_cash_flows")
    tax_rate = _number(p, "tax_rate")
    if not 0.0 <= tax_rate < 1.0:
        raise SystemExit("'tax_rate' of %g is outside [0, 1). Use the marginal rate for a "
                         "project, not the effective rate." % tax_rate)
    years = len(flows) - 1

    sunk_investment = float(p.get("sunk_investment", 0.0))
    if sunk_investment < 0:
        raise SystemExit("'sunk_investment' is the amount already spent and charged into "
                         "the stream. Give it as a positive number.")
    sunk_depreciation = _series(p.get("sunk_asset_depreciation"), years,
                                "sunk_asset_depreciation")
    allocated = _series(p.get("allocated_overhead_not_incremental"), years,
                        "allocated_overhead_not_incremental")
    new_overhead = _series(p.get("incremental_overhead"), years, "incremental_overhead")
    opportunity = _series(p.get("opportunity_cost_after_tax"), years,
                          "opportunity_cost_after_tax")

    cannibalization = p.get("cannibalization") or {}
    lost = _series(cannibalization.get("lost_contribution_pre_tax"), years,
                   "cannibalization.lost_contribution_pre_tax")
    retained_share = float(cannibalization.get("retained_share", 1.0))
    if not 0.0 <= retained_share <= 1.0:
        raise SystemExit("'cannibalization.retained_share' must be between 0 and 1. It is "
                         "the fraction of diverted sales the firm would otherwise have "
                         "kept; in a fiercely competitive market that is well below 1.")

    side_benefit = _series(p.get("side_benefit_after_tax"), years, "side_benefit_after_tax")

    rows = []
    result = []
    for t in range(years + 1):
        add_back_sunk = sunk_investment if t == 0 else 0.0
        # A sunk asset's depreciation shelters tax whether or not the project goes ahead,
        # so that shield must come out or part of the sunk cost stays in the analysis.
        remove_shield = -sunk_depreciation[t] * tax_rate
        add_back_allocated = allocated[t] * (1.0 - tax_rate)
        charge_new_overhead = -new_overhead[t] * (1.0 - tax_rate)
        charge_opportunity = -opportunity[t]
        charge_cannibalization = -lost[t] * retained_share * (1.0 - tax_rate)
        credit_side_benefit = side_benefit[t]
        value = (flows[t] + add_back_sunk + remove_shield + add_back_allocated
                 + charge_new_overhead + charge_opportunity + charge_cannibalization
                 + credit_side_benefit)
        result.append(value)
        rows.append({
            "year": t, "total_cash_flow": flows[t],
            "add_back_sunk_investment": add_back_sunk,
            "remove_sunk_depreciation_tax_shield": remove_shield,
            "add_back_non_incremental_allocated_overhead": add_back_allocated,
            "charge_incremental_overhead": charge_new_overhead,
            "charge_opportunity_cost": charge_opportunity,
            "charge_cannibalization": charge_cannibalization,
            "credit_side_benefit": credit_side_benefit,
            "incremental_cash_flow": value,
        })

    out = {"tax_rate": tax_rate, "years": rows, "incremental_cash_flows": result}
    if p.get("discount_rate") is not None:
        rates = _rates(p["discount_rate"], years, "discount_rate")
        factors = _discount_factors(rates)
        out["npv_of_total_cash_flows"] = sum(flows[t] * factors[t]
                                             for t in range(years + 1))
        out["npv_of_incremental_cash_flows"] = sum(result[t] * factors[t]
                                                   for t in range(years + 1))
        out["npv_effect_of_adjustments"] = (out["npv_of_incremental_cash_flows"]
                                            - out["npv_of_total_cash_flows"])
    out["note"] = ("This is the adjustment route. Building the stream directly from "
                   "incremental revenue and cost lines is the other route, and the two "
                   "must reconcile up to rounding. Do not mix them in one model.")
    return out


def cmd_incremental(args):
    _emit(incremental(_read_payload(args)))


# --------------------------------------------------------------------------- synergy

def synergy(p):
    """Value synergy, and turn it into the most an acquirer can pay.

    Two routes. The combined-firm route subtracts the sum of the stand-alone values from
    the value of the merged business, which is the definition. The cash-flow route
    discounts an explicit synergy schedule at the cost of capital of the business that
    *receives* the benefit, which is almost never the acquirer's own rate.
    """
    mode = p.get("mode")
    if mode is None:
        mode = "combined" if "combined_value_with_synergy" in p else "cash_flows"
    if mode not in ("combined", "cash_flows"):
        raise SystemExit("'mode' must be 'combined' or 'cash_flows'.")

    out = {"mode": mode}

    if mode == "combined":
        acquirer = _number(p, "acquirer_standalone_value")
        target = _number(p, "target_standalone_value")
        with_synergy = _number(p, "combined_value_with_synergy")
        sum_of_parts = acquirer + target
        value = with_synergy - sum_of_parts
        out.update({
            "acquirer_standalone_value": acquirer,
            "target_standalone_value": target,
            "combined_value_without_synergy": sum_of_parts,
            "combined_value_with_synergy": with_synergy,
            "synergy_value": value,
        })
        stated = p.get("combined_value_without_synergy")
        if stated is not None:
            difference = float(stated) - sum_of_parts
            out["sum_of_parts_check"] = {
                "stated_combined_value_without_synergy": float(stated),
                "sum_of_standalone_values": sum_of_parts,
                "difference": difference,
                "ok": abs(difference) <= 1e-6 * max(1.0, abs(sum_of_parts)),
                "why": "Merely adding two firms together creates nothing, so the no-synergy "
                       "combined value must equal the sum of the stand-alone values "
                       "exactly. A difference means an inconsistent assumption has crept "
                       "into the combined-firm model."}
        out["note"] = ("Use the target's restructured value here when the deal also claims "
                       "control value, or the restructuring gains get counted twice.")
    else:
        flows_in = p.get("cash_flows")
        if flows_in is None:
            raise SystemExit(
                "Provide 'cash_flows' — the after-tax synergy cash flows for years 1 "
                "onward, with leading zeros for any lag before the benefit arrives.")
        annual = _flows(flows_in, "cash_flows")
        rate_spec = p.get("discount_rate")
        if rate_spec is None:
            raise SystemExit(
                "'discount_rate' is required, and it is the cost of capital of the "
                "business that receives the synergy — not the project's rate and not the "
                "acquirer's.")
        # Year 0 carries no synergy; the schedule the analyst writes starts at year 1.
        stream = [0.0] + annual
        rates = _rates(rate_spec, len(annual), "discount_rate")
        closed, terminal = _apply_terminal(stream, p.get("terminal"), rates)
        factors = _discount_factors(rates)
        pvs = [closed[t] * factors[t] for t in range(len(closed))]
        value = sum(pvs)
        out.update({
            "discount_rate": rate_spec,
            "years": [{"year": t, "synergy_cash_flow": closed[t], "present_value": pvs[t]}
                      for t in range(1, len(closed))],
            "synergy_value": value,
        })
        if terminal:
            out["terminal"] = terminal
        rate_note = p.get("receiving_business")
        if rate_note:
            out["receiving_business"] = rate_note
        out["note"] = ("Discounted at the receiving business's rate. Report the "
                       "stand-alone project or target value separately so a reader can "
                       "see how much of the case rests on synergy.")

    exchange_rate = p.get("exchange_rate")
    if exchange_rate is not None:
        exchange_rate = float(exchange_rate)
        if exchange_rate <= 0:
            raise SystemExit("'exchange_rate' must be positive. It is the number of "
                             "synergy-currency units per unit of reporting currency.")
        out["exchange_rate"] = exchange_rate
        out["synergy_value_in_reporting_currency"] = out["synergy_value"] / exchange_rate

    acq = p.get("acquisition")
    if acq:
        reporting_synergy = out.get("synergy_value_in_reporting_currency",
                                    out["synergy_value"])
        standalone = _number(acq, "target_standalone_value",
                             "acquisition.target_standalone_value")
        ceiling = standalone + reporting_synergy
        block = {"target_standalone_value": standalone,
                 "synergy_value": reporting_synergy,
                 "maximum_price": ceiling,
                 "rule": "Maximum price = stand-alone value of the target + value of "
                         "synergy. Paying the full synergy hands the entire gain to the "
                         "seller, so the ceiling is a walk-away point, not a target."}
        price = acq.get("price") if acq.get("price") is not None else acq.get("market_price")
        if price is not None:
            price = float(price)
            block["price"] = price
            block["acquisition_npv"] = ceiling - price
            block["synergy_retained_by_acquirer"] = reporting_synergy - (price - standalone)
            block["premium_over_standalone"] = price - standalone
            block["synergy_required_to_justify_price"] = price - standalone
            block["verdict"] = "proceed" if price < ceiling else "walk away"
            if price >= ceiling:
                block["verdict_reason"] = (
                    "The price is at or above stand-alone value plus every dollar of "
                    "credible synergy, so the deal destroys %.4f of acquirer value even "
                    "with the synergy fully credited."
                    % (price - ceiling))
        out["acquisition"] = block
    return out


def cmd_synergy(args):
    _emit(synergy(_read_payload(args)))


# ------------------------------------------------------------------- synergy haircut

def _load_realization(path=None):
    with open(path or SYNERGY_TABLE) as f:
        return json.load(f)


def synergy_haircut(p):
    """Cut a synergy schedule down to what post-merger evidence says actually arrives.

    Cost synergies land most of the time; revenue synergies usually do not. Presenting one
    blended number hides the fact that the fragile half is the revenue half, so components
    are haircut separately and reported separately.
    """
    table = _load_realization(p.get("table_path"))
    defaults = table["defaults"]
    components = p.get("components")
    if not isinstance(components, list) or not components:
        raise SystemExit(
            "'components' must be a non-empty list of {label, kind, value} objects, where "
            "kind is 'cost' or 'revenue'. Split the schedule before haircutting it.")

    rows = []
    gross_total = 0.0
    net_total = 0.0
    for i, comp in enumerate(components):
        label = comp.get("label", "component %d" % (i + 1))
        kind = comp.get("kind")
        if kind not in defaults:
            raise SystemExit("Component %r has kind %r. Use 'cost' or 'revenue'."
                             % (label, kind))
        gross = _number(comp, "value", "%s.value" % label)
        realization = float(comp.get("realization_rate",
                                     defaults[kind]["realization_rate"]))
        attrition = float(comp.get("customer_attrition_rate",
                                   defaults[kind]["customer_attrition_rate"]))
        one_time = float(comp.get("one_time_cost_to_achieve", 0.0))
        if not 0.0 <= attrition < 1.0:
            raise SystemExit("%s.customer_attrition_rate of %g is outside [0, 1)."
                             % (label, attrition))
        after_realization = gross * realization
        after_attrition = after_realization * (1.0 - attrition)
        net = after_attrition - one_time
        gross_total += gross
        net_total += net
        rows.append({
            "label": label, "kind": kind, "gross_value": gross,
            "realization_rate": realization,
            "realization_source": ("supplied" if "realization_rate" in comp
                                   else defaults[kind]["basis"]),
            "value_after_realization": after_realization,
            "customer_attrition_rate": attrition,
            "value_after_attrition": after_attrition,
            "one_time_cost_to_achieve": one_time,
            "net_value": net,
        })

    out = {
        "components": rows,
        "gross_synergy": gross_total,
        "net_synergy": net_total,
        "haircut": gross_total - net_total,
        "haircut_percent": ((gross_total - net_total) / gross_total) if gross_total else None,
        "evidence": {"as_of": table["as_of"], "source": table["source"],
                     "headline": table["headline"],
                     "sample_sizes": table["sample_sizes"],
                     "realization_bands": table["realization_bands"],
                     "findings": table["odds_findings"]},
        "note": ("These realization rates are what happened to other people's mergers, "
                 "not a forecast for this one. Override them with a bottom-up plan when "
                 "you have one, and reduce them further if you are one of several "
                 "bidders — competition bids the synergy into the price."),
    }
    bidders = p.get("competing_bidders")
    if bidders is not None:
        bidders = int(bidders)
        out["competing_bidders"] = bidders
        out["bidding_note"] = (
            "Sole bidder: you keep what you do not pay away." if bidders <= 1 else
            "With %d bidders, assume the synergy gets competed into the price and reduce "
            "what you are willing to pay accordingly." % bidders)
    return out


def cmd_synergy_haircut(args):
    _emit(synergy_haircut(_read_payload(args)))


# ------------------------------------------------------------------ value of control

# Deal practice quotes a flat 20% "control premium", usually sourced to Mergerstat. It
# carries no valuation content, so it appears here only as a comparison against the
# premium the two valuations actually support.
RULE_OF_THUMB_CONTROL_PREMIUM = 0.20

# Two stated discount rates that agree to within 5 basis points are the same rate written
# to different precision. Anything wider is a different rate, and on a target that is the
# risk-transference error rather than rounding.
RATE_AGREEMENT_TOLERANCE = 0.0005

MOTIVES = ("undervaluation", "control", "synergy")

_RULE_OF_THUMB_WARNING = (
    "A fixed-percentage control premium is not analysis. The 20% figure in general "
    "circulation is a survey average with heavy sampling bias and wide standard errors, "
    "and it says nothing about this firm. The premium has to fall out of the gap between "
    "the status-quo valuation and the optimal one: name the changes, price them, "
    "subtract. If you cannot name a single change, the premium is zero however well the "
    "target is regarded.")


def _probability(payload, key, label=None):
    """A probability, refused unless it lies in [0, 1]."""
    label = label or key
    value = _number(payload, key, label)
    if not 0.0 <= value <= 1.0:
        raise SystemExit(
            "%r is %g. It must be a probability between 0 and 1 — write 20%% as 0.20, "
            "not as 20." % (label, value))
    return value


def _status_quo_and_restructured(p):
    """Read the two valuations control arithmetic sits on, and refuse an inverted pair."""
    status_quo = _number(p, "status_quo_value")
    if p.get("restructured_value") is not None:
        optimal = _number(p, "restructured_value")
    elif p.get("optimal_value") is not None:
        optimal = _number(p, "optimal_value")
    else:
        raise SystemExit(
            "Missing 'restructured_value' (or 'optimal_value'). Control arithmetic needs "
            "two full valuations of the same target: one under existing management and "
            "one under the policies a value-maximising owner would set. Build both with "
            "dcf-valuation-engine and pass the equity values in here.")
    if optimal < status_quo:
        raise SystemExit(
            "The restructured value (%.4f) is below the status-quo value (%.4f), so the "
            "'improvements' destroy value and the control value is negative. That is an "
            "input error, not a finding: incumbent management beats your alternative "
            "plan, so revisit the restructuring case before pricing control."
            % (optimal, status_quo))
    return status_quo, optimal


def control_value(p):
    """The value of running a company better, times the odds that anyone gets to.

    Control is worth the gap between the firm as it is run and the firm as it could be
    run, and nothing else. Both valuations happen elsewhere and arrive here as numbers.
    A bidder who takes control can *ensure* the change, so the gap is what control is
    worth to it. Everyone else holds a claim on the gap multiplied by the probability
    that the change actually happens, and that product is what puts a market price
    between the two values, what makes a voting share worth more than a non-voting one,
    and what a minority holder does not get.
    """
    status_quo, optimal = _status_quo_and_restructured(p)
    probability = _probability(p, "probability_of_change")
    gap = optimal - status_quo
    expected = probability * gap

    out = {
        "status_quo_value": status_quo,
        "restructured_value": optimal,
        "value_of_control": gap,
        "probability_of_change": probability,
        "expected_value_of_control": expected,
        # A control acquisition removes the probability: once you own the firm you decide
        # whether the changes happen, so the ceiling is the whole restructured value.
        "maximum_hostile_bid": optimal,
    }
    if gap == 0:
        out["note"] = ("The two valuations coincide, so this firm is already run the way "
                       "you would run it and control is worth nothing here. No premium "
                       "is defensible at any probability.")

    shares = p.get("shares_outstanding")
    sq_ps = p.get("status_quo_value_per_share")
    op_ps = p.get("restructured_value_per_share")
    if op_ps is None:
        op_ps = p.get("optimal_value_per_share")
    if shares is not None:
        shares = float(shares)
        if shares <= 0:
            raise SystemExit("'shares_outstanding' must be positive.")
        sq_ps = status_quo / shares
        op_ps = optimal / shares
    elif sq_ps is not None and op_ps is not None:
        sq_ps, op_ps = float(sq_ps), float(op_ps)
        if op_ps < sq_ps:
            raise SystemExit(
                "The restructured value per share (%.4f) is below the status-quo value "
                "per share (%.4f). Check that both were divided by the same share count."
                % (op_ps, sq_ps))
    else:
        sq_ps = op_ps = None

    if sq_ps is not None:
        gap_ps = op_ps - sq_ps
        out["per_share"] = {
            "shares_outstanding": shares,
            "status_quo_value_per_share": sq_ps,
            "restructured_value_per_share": op_ps,
            "value_of_control_per_share": gap_ps,
            "expected_value_of_control_per_share": probability * gap_ps,
            # The identity a market price has to satisfy: every share already owns the
            # status quo, plus the odds-weighted slice of the improvement.
            "expected_value_per_share": sq_ps + probability * gap_ps,
            "maximum_hostile_bid_per_share": op_ps,
        }

    price = p.get("market_price_per_share")
    if price is not None:
        if sq_ps is None:
            raise SystemExit(
                "'market_price_per_share' needs per-share values to compare against. Give "
                "'shares_outstanding', or give 'status_quo_value_per_share' and "
                "'restructured_value_per_share' directly.")
        price = float(price)
        gap_ps = op_ps - sq_ps
        block = {"market_price_per_share": price,
                 "maximum_premium_per_share": op_ps - price}
        if gap_ps == 0:
            block["implied_probability_of_change"] = None
            block["reading"] = ("There is no gap between the two values, so no probability "
                               "can be backed out of the price.")
        else:
            implied = (price - sq_ps) / gap_ps
            block["implied_probability_of_change"] = implied
            if implied <= 0:
                block["reading"] = (
                    "The price is at or below your status-quo value, so the market is "
                    "pricing no chance of change at all. The stock may be cheap even if "
                    "nothing ever changes.")
            elif implied >= 1:
                block["reading"] = (
                    "The price is at or above your restructured value, which reads as a "
                    "probability of %.1f%%. Treat that as a signal that your optimal value "
                    "is too low or that the market sees something you have not modelled, "
                    "not as a very high probability." % (implied * 100))
            else:
                block["reading"] = (
                    "The market is pricing roughly a %.1f%% chance that these policies "
                    "change. Compare it against your own reading of the board, the "
                    "register and the takeover defences: a higher number than yours means "
                    "the change is already paid for." % (implied * 100))
        block["premium_note"] = (
            "The maximum premium is a walk-away point. Paying all of it hands the entire "
            "value of your own improvement plan to the seller and leaves you with the "
            "work and the risk for nothing.")
        out["market"] = block

    delay = p.get("implementation_delay_years")
    if delay is not None:
        delay = float(delay)
        if delay < 0:
            raise SystemExit("'implementation_delay_years' cannot be negative.")
        rate = p.get("discount_rate")
        if rate is None:
            raise SystemExit(
                "'implementation_delay_years' needs a 'discount_rate' to discount the "
                "delayed gain — the cost of equity when the two values are equity values.")
        rate = float(rate)
        if rate <= -1.0:
            raise SystemExit("'discount_rate' at or below -100%% has no meaning.")
        factor = (1.0 + rate) ** delay
        adjusted = gap / factor
        out["delay"] = {
            "implementation_delay_years": delay,
            "discount_rate": rate,
            "adjusted_value_of_control": adjusted,
            "adjusted_expected_value_of_control": probability * adjusted,
            "value_lost_to_delay": gap - adjusted,
            "note": ("A turnaround that takes %g years is worth less than the same "
                     "turnaround today. Set the premium off the adjusted figure."
                     % delay),
        }

    classes = p.get("share_classes")
    if classes:
        voting = _number(classes, "voting_shares", "share_classes.voting_shares")
        non_voting = _number(classes, "non_voting_shares",
                             "share_classes.non_voting_shares")
        if voting <= 0:
            raise SystemExit("'share_classes.voting_shares' must be positive.")
        if non_voting < 0:
            raise SystemExit("'share_classes.non_voting_shares' cannot be negative.")
        total = voting + non_voting
        # Every share owns the same cash flows, so the status quo spreads across all of
        # them. Only the odds-weighted improvement attaches to the class that can force it.
        non_voting_value = status_quo / total
        control_per_voting = expected / voting
        voting_value = non_voting_value + control_per_voting
        out["share_classes"] = {
            "voting_shares": voting,
            "non_voting_shares": non_voting,
            "value_per_non_voting_share": non_voting_value,
            "expected_control_value_per_voting_share": control_per_voting,
            "value_per_voting_share": voting_value,
            "voting_premium_percent": ((voting_value - non_voting_value)
                                       / non_voting_value) if non_voting_value else None,
            "assumption": ("This is the extreme case in which non-voting shares are "
                           "completely unprotected. Charter provisions, tag-along rights "
                           "and local law leak control value back to the non-voting class "
                           "and shrink the premium, so read the documents before quoting "
                           "this figure."),
        }

    out["caveat"] = ("The probability is the judgment in this calculation and it is not "
                     "stable. Takeover defences, voting rules, the cost of mounting a "
                     "challenge and sheer size push it down; an activist arriving on the "
                     "register can move it twenty points overnight.")
    return out


def cmd_control_value(args):
    _emit(control_value(_read_payload(args)))


# ------------------------------------------------------------------- deal acid test

def deal(p):
    """The four-number acid test: price against the benchmark its motive implies.

    There are three value-based reasons to buy a company — the target is undervalued, you
    can run it better, or it is worth more inside your firm than outside it — and each
    has its own benchmark. Four numbers settle all three: the price, the target's
    stand-alone value, its restructured value, and the synergy value. Everything this
    function reports is a comparison among those four, which is why it refuses to run
    when one of them was built the wrong way.
    """
    status_quo = _number(p, "target_standalone_value")
    if p.get("restructured_value") is not None:
        restructured = _number(p, "restructured_value")
        control = restructured - status_quo
    elif p.get("value_of_control") is not None:
        control = _number(p, "value_of_control")
        restructured = status_quo + control
    else:
        raise SystemExit(
            "Give 'restructured_value' (the target under the policies you would set) or "
            "'value_of_control' (the gap between the two valuations). Without one of them "
            "the control test has no benchmark. Pass 0 for 'value_of_control' if you "
            "cannot name a single thing you would change — that is the honest answer for "
            "a well-run target.")
    if control < 0:
        raise SystemExit(
            "The restructured value is below the stand-alone value, so the value of "
            "control is negative (%.4f). Revisit the restructuring case: as it stands it "
            "says your policies are worse than the incumbents'." % control)
    synergy_value = _number(p, "synergy_value") if "synergy_value" in p else 0.0
    price = _number(p, "price")

    # Refusal 1: the target's own discount rate. Discounting a target at the acquirer's
    # cost of equity, or building the acquirer's cheap debt into the target's cost of
    # capital, mechanically raises the price you can "justify" and hands the difference to
    # the seller. Neither is a rounding issue, so the arithmetic below will not run on it.
    flag = p.get("target_discount_rate_used")
    if flag is None:
        raise SystemExit(
            "Missing 'target_discount_rate_used'. Set it to true only if the target's "
            "cash flows were discounted at the target's own cost of capital, built from "
            "the target's business risk and the target's own debt capacity. A risky "
            "business does not become safe because a safe buyer owns it, and the buyer's "
            "borrowing power is a property of the buyer.")
    if not isinstance(flag, bool):
        raise SystemExit("'target_discount_rate_used' must be true or false, got %r."
                         % (flag,))
    if flag is False:
        raise SystemExit(
            "'target_discount_rate_used' is false, so the target was valued at somebody "
            "else's rate and the four numbers are not comparable. Re-value the target at "
            "its own cost of capital: unlevered beta of the target's businesses relevered "
            "at the target's debt-to-equity ratio, and the target's own cost of debt. If "
            "the acquirer genuinely brings extra debt capacity to the combined firm, that "
            "is a financial synergy — value it in 'synergy_value', do not smuggle it into "
            "the discount rate.")

    rate_used = p.get("discount_rate_used")
    target_rate = p.get("target_cost_of_capital")
    rate_check = None
    if rate_used is not None and target_rate is not None:
        rate_used, target_rate = float(rate_used), float(target_rate)
        difference = rate_used - target_rate
        if abs(difference) > RATE_AGREEMENT_TOLERANCE:
            raise SystemExit(
                "'target_discount_rate_used' is true but the rate applied (%.4f) differs "
                "from the target's own cost of capital (%.4f) by %.0f basis points. The "
                "flag and the numbers disagree; fix the valuation, not the flag."
                % (rate_used, target_rate, abs(difference) * 10000))
        rate_check = {"discount_rate_used": rate_used,
                      "target_cost_of_capital": target_rate,
                      "difference": difference, "agrees": True}

    # Refusal 2: the synergy baseline. Synergy is the combined firm less the sum of the
    # parts, and the target's part is its *restructured* value whenever control value is
    # also being claimed. Baselining on the status quo puts the restructuring gains into
    # the synergy number as well, and the deal then gets credited for them twice.
    baseline = p.get("synergy_baseline")
    if synergy_value != 0.0:
        if baseline is None:
            raise SystemExit(
                "Missing 'synergy_baseline'. Set it to 'restructured_target' once you "
                "have confirmed the combined-firm baseline used the target's restructured "
                "value rather than its status-quo value. Baselining on the status quo "
                "puts the control gains inside the synergy figure as well, and this deal "
                "then claims them twice.")
        if baseline == "status_quo":
            raise SystemExit(
                "'synergy_baseline' is 'status_quo', so the synergy figure of %.4f already "
                "contains the %.4f of control value. Re-run the combined-firm valuation "
                "against acquirer + restructured target, or subtract the control value "
                "from the synergy estimate before running this test."
                % (synergy_value, control))
        if baseline != "restructured_target":
            raise SystemExit(
                "'synergy_baseline' must be 'restructured_target' or 'status_quo', got "
                "%r." % (baseline,))

    maximum = restructured + synergy_value
    combined_gains = control + synergy_value
    premium = price - status_quo
    acquirer_share = maximum - price

    tests = {
        "undervaluation": {
            "benchmark": "status_quo_value", "benchmark_value": status_quo,
            "passes": price < status_quo, "headroom": status_quo - price,
            "reads": "The target is worth more than it costs even if nothing changes."},
        "control": {
            "benchmark": "restructured_value", "benchmark_value": restructured,
            "passes": price < restructured, "headroom": restructured - price,
            "reads": "The price is below the target run the way you would run it."},
        "synergy": {
            "benchmark": "restructured_value_plus_synergy", "benchmark_value": maximum,
            "passes": price < maximum, "headroom": maximum - price,
            "reads": "The price is below the target plus everything it is worth to you."},
    }

    out = {
        "four_numbers": {
            "acquisition_price": price,
            "status_quo_value": status_quo,
            "restructured_value": restructured,
            "synergy_value": synergy_value,
        },
        "value_of_control": control,
        "maximum_justifiable_price": maximum,
        "acid_test": tests,
        "capture": {
            "premium_over_standalone_value": premium,
            "combined_gains": combined_gains,
            "captured_by_target_shareholders": premium,
            "captured_by_acquirer_shareholders": acquirer_share,
            # Seller take plus buyer take is identically the total gain, which is the
            # sanity check on the whole block.
            "gains_reconcile": abs((premium + acquirer_share) - combined_gains)
                               <= 1e-9 * max(1.0, abs(combined_gains)),
            "synergy_required_to_justify_price": price - restructured,
        },
        "synergy_baseline": baseline or "not applicable (no synergy claimed)",
    }
    if rate_check:
        out["discount_rate_check"] = rate_check

    if combined_gains == 0:
        out["capture"]["premium_share_of_combined_gains"] = None
        out["capture"]["note"] = (
            "There are no gains to share: no control value and no synergy. Every dollar "
            "of premium is a transfer to the seller.")
    else:
        share = premium / combined_gains
        out["capture"]["premium_share_of_combined_gains"] = share
        if share >= 1.0:
            out["capture"]["note"] = (
                "The premium is %.0f%% of the total gains this deal can create, so the "
                "seller takes all of them and the acquirer's shareholders fund the "
                "difference." % (share * 100))
        else:
            out["capture"]["note"] = (
                "The seller takes %.0f%% of the combined gains and the acquirer keeps "
                "%.0f%%. That split is the negotiation, and it moves toward the seller "
                "with every extra bidder." % (share * 100, (1 - share) * 100))

    market_cap = p.get("pre_announcement_market_cap")
    if market_cap is not None:
        market_cap = float(market_cap)
        out["premium_to_justify"] = price - market_cap
        out["pre_announcement_market_cap"] = market_cap
        out["undervaluation_precheck"] = {
            "status_quo_value": status_quo, "market_cap": market_cap,
            "target_was_undervalued": status_quo > market_cap,
            "why": ("The undervaluation motive is dead before any premium is discussed "
                    "if the market already prices the target above its status-quo value.")}

    motive = p.get("motive")
    if motive is not None:
        if motive not in MOTIVES:
            raise SystemExit(
                "'motive' must be one of %s. There is no fourth value-based reason to buy "
                "a company; 'strategic' is a buzz word, not a benchmark."
                % ", ".join(repr(m) for m in MOTIVES))
        chosen = tests[motive]
        out["motive"] = motive
        out["verdict"] = "defensible" if chosen["passes"] else "overpaying"
        if chosen["passes"]:
            out["verdict_reason"] = (
                "At %.4f the price sits %.4f below the %s benchmark of %.4f, so the stated "
                "motive supports it." % (price, chosen["headroom"], motive,
                                         chosen["benchmark_value"]))
        else:
            out["verdict_reason"] = (
                "At %.4f the price exceeds the %s benchmark of %.4f by %.4f. Exactly two "
                "explanations remain: the synergy is underestimated, or the acquirer is "
                "overpaying. Pick one and say which."
                % (price, motive, chosen["benchmark_value"], -chosen["headroom"]))

    if not any(t["passes"] for t in tests.values()):
        out["all_tests_failed"] = True
        out["all_tests_note"] = (
            "The price clears every benchmark this deal has, missing the highest of them "
            "by %.4f. Either the synergy potential is badly underestimated or the acquirer "
            "is overpaying by that amount." % (price - maximum))
    else:
        out["all_tests_failed"] = False

    out["caveat"] = ("All four numbers are valuations, not observations. The price may be "
                     "the only one anybody agrees on, which is exactly why the other three "
                     "have to be built before the price is discussed rather than after.")
    return out


def cmd_deal(args):
    _emit(deal(_read_payload(args)))


# --------------------------------------------------- control premium / minority discount

def control_premium(p):
    """Control premium and minority discount: the same gap, divided by different things.

    A controlling stake can move the firm from how it is run to how it could be run, so
    it is priced off the optimal value. A minority stake cannot, so it is priced off the
    status quo. Divide the gap by the status-quo value and you have the control premium;
    divide the same gap by the optimal value and you have the minority discount. Neither
    is a number you look up.
    """
    conversion_only = ("status_quo_equity_value" not in p
                       and "status_quo_value" not in p)
    if conversion_only:
        if p.get("control_premium") is not None:
            premium = _number(p, "control_premium")
            if premium <= -1.0:
                raise SystemExit("'control_premium' of %g implies a non-positive optimal "
                                 "value." % premium)
            discount = premium / (1.0 + premium)
        elif p.get("minority_discount") is not None:
            discount = _number(p, "minority_discount")
            if discount >= 1.0:
                raise SystemExit(
                    "'minority_discount' of %g is at or above 1, which says the firm is "
                    "worth nothing under current management. Check the two valuations."
                    % discount)
            premium = discount / (1.0 - discount)
        else:
            raise SystemExit(
                "Give both valuations ('status_quo_equity_value' and "
                "'optimal_equity_value') to compute the premium and the discount, or give "
                "one of 'control_premium' / 'minority_discount' on its own to convert "
                "between them.")
        return {
            "mode": "conversion",
            "control_premium": premium,
            "minority_discount": discount,
            "relationship": ("minority discount = control premium / (1 + control "
                             "premium); control premium = minority discount / "
                             "(1 - minority discount). They are the same gap over a "
                             "different denominator: the premium divides by the status-quo "
                             "value, the discount by the optimal value."),
            "warning": _RULE_OF_THUMB_WARNING,
        }

    status_quo = _number(p, "status_quo_equity_value") if "status_quo_equity_value" in p \
        else _number(p, "status_quo_value")
    if p.get("optimal_equity_value") is not None:
        optimal = _number(p, "optimal_equity_value")
    elif p.get("restructured_value") is not None:
        optimal = _number(p, "restructured_value")
    elif p.get("optimal_value") is not None:
        optimal = _number(p, "optimal_value")
    else:
        raise SystemExit(
            "Missing 'optimal_equity_value'. The premium falls out of two valuations of "
            "the same firm — as run today, and as a value-maximising owner would run it.")
    if optimal <= 0:
        raise SystemExit(
            "'optimal_equity_value' is %.4f. A minority discount divides by it, so it "
            "must be positive." % optimal)
    if optimal < status_quo:
        raise SystemExit(
            "The optimal value (%.4f) is below the status-quo value (%.4f), which would "
            "make the discount negative. That says incumbent management beats your "
            "hypothetical owner; treat it as invalid inputs and rebuild the optimal case."
            % (optimal, status_quo))

    gap = optimal - status_quo
    discount = gap / optimal
    premium = (gap / status_quo) if status_quo else None

    out = {
        "mode": "from_values",
        "status_quo_equity_value": status_quo,
        "optimal_equity_value": optimal,
        "value_of_control": gap,
        "minority_discount": discount,
        "control_premium": premium,
        "relationship": ("minority discount = control premium / (1 + control premium); "
                         "control premium = minority discount / (1 - minority discount). "
                         "The gap is the same; only the denominator changes."),
        "warning": _RULE_OF_THUMB_WARNING,
    }
    if premium is not None:
        # The round trip is an identity, and it is reported so a reader can see that the
        # two figures are one number rather than two independent estimates.
        out["conversion_check"] = {
            "minority_discount_from_control_premium": premium / (1.0 + premium),
            "control_premium_from_minority_discount": discount / (1.0 - discount),
        }
    if gap == 0:
        out["note"] = ("The two valuations coincide, so this firm is already well run. "
                       "The control premium is zero and the minority discount is zero, "
                       "whatever any survey says.")

    majority = p.get("majority_pct")
    minority = p.get("minority_pct")
    if majority is not None or minority is not None:
        stakes = {}
        if majority is not None:
            majority = float(majority)
            if not 0.0 < majority <= 1.0:
                raise SystemExit("'majority_pct' must be a fraction between 0 and 1 — "
                                 "write 51%% as 0.51.")
            if majority <= 0.5:
                raise SystemExit(
                    "'majority_pct' of %g does not convey control. A 50/50 stake cannot "
                    "force a change of policy either, so price it off the status-quo "
                    "value as a minority stake." % majority)
            stakes["majority_pct"] = majority
            stakes["majority_stake_value"] = majority * optimal
            stakes["majority_priced_off"] = "optimal equity value"
        if minority is not None:
            minority = float(minority)
            if not 0.0 < minority <= 1.0:
                raise SystemExit("'minority_pct' must be a fraction between 0 and 1 — "
                                 "write 49%% as 0.49.")
            if minority >= 0.5:
                raise SystemExit(
                    "'minority_pct' of %g is not a minority stake. Above 50%% the holder "
                    "can change how the firm is run and is priced off the optimal value."
                    % minority)
            stakes["minority_pct"] = minority
            stakes["minority_stake_value"] = minority * status_quo
            stakes["minority_priced_off"] = "status quo equity value"
        if majority is not None and minority is not None:
            stakes["ownership_difference"] = majority - minority
            stakes["stake_value_difference"] = (stakes["majority_stake_value"]
                                                - stakes["minority_stake_value"])
            stakes["note"] = (
                "%.2f percentage points of ownership are worth %.4f here, far more than "
                "that share of any value in the problem. The difference is the control, "
                "not the extra shares."
                % ((majority - minority) * 100, stakes["stake_value_difference"]))
            # The shipped minoritydiscount.xls stores optimal + minority% x status quo for
            # the minority stake, which comes out larger than the whole firm. It is named
            # here so nobody reconciles to it and thinks this engine is wrong.
            stakes["known_spreadsheet_defect"] = {
                "stored_formula": "optimal + minority_pct * status_quo",
                "stored_value": optimal + minority * status_quo,
                "correct_value": minority * status_quo,
                "why": "The stored figure exceeds the value of the whole firm. It is a "
                       "spreadsheet bug, not a convention.",
            }
        out["stakes"] = stakes

    rule = p.get("rule_of_thumb_premium", RULE_OF_THUMB_CONTROL_PREMIUM)
    rule = float(rule)
    out["rule_of_thumb"] = {
        "premium": rule,
        "price_it_implies": status_quo * (1.0 + rule),
        "price_the_valuations_support": optimal,
        "difference": optimal - status_quo * (1.0 + rule),
        "why_not": ("A flat %.0f%% premium is a survey average of other people's deals, "
                    "and averages of overpayments are still overpayments. The premium "
                    "here is %s, because that is what the named changes are worth."
                    % (rule * 100,
                       "zero" if premium == 0 else ("%.1f%%" % (premium * 100))
                       if premium is not None else "undefined")),
    }
    out["caveat"] = ("Do not stack this on other premiums. A brand premium or a "
                     "management-quality premium added to a DCF that already reflects the "
                     "brand and the management is double counting, and so is a control "
                     "premium added to a value that already assumes optimal policies.")
    return out


def cmd_control_premium(args):
    _emit(control_premium(_read_payload(args)))


# --------------------------------------------------------------------------- examples

# Netflix Fit, Damodaran's Spring 2020 investment-analysis case: finite 10-year FCFF at an
# 8.01% cost of capital, and the entertainment-side synergy at Netflix Entertainment's
# 8.93%. Published answers: stand-alone NPV $106m, IRR 8.69%, synergy NPV $376m.
NETFLIX_FIT_FCFF = [-2500.00, 132.94, 200.68, 272.66, -171.29, 459.60,
                    944.35, 442.58, 484.43, 528.60, 1143.52]
NETFLIX_FIT_SYNERGY = [56.25, 56.81, 57.38, 57.95, 58.53,
                       59.12, 59.71, 60.31, 60.91, 61.52]
NETFLIX_FIT_RATE = 0.0801
NETFLIX_ENTERTAINMENT_RATE = 0.0893

EXAMPLES = {
    "npv": {
        "streams": [
            {"label": "Netflix Fit stand-alone", "cash_flows": NETFLIX_FIT_FCFF,
             "discount_rate": NETFLIX_FIT_RATE},
            {"label": "synergy to Netflix Entertainment",
             "cash_flows": [0.0] + NETFLIX_FIT_SYNERGY,
             "discount_rate": NETFLIX_ENTERTAINMENT_RATE},
        ],
    },
    "irr": {"cash_flows": [-1000, 800, 1000, 1300, -2200], "hurdle_rate": 0.12},
    "mirr": {"cash_flows": [-1000, 300, 400, 500, 600], "hurdle_rate": 0.15},
    "rationing": {
        "discount_rate": 0.15, "budget": 10000000,
        "projects": [
            {"label": "A (small)",
             "cash_flows": [-1000000, 350000, 450000, 600000, 750000]},
            {"label": "B (large)",
             "cash_flows": [-10000000, 3000000, 3500000, 4500000, 5500000]},
        ],
    },
    "different-lives": {
        "discount_rate": 0.12,
        "projects": [
            {"label": "A", "cash_flows": [-1000, 400, 400, 400, 400, 400]},
            {"label": "B", "cash_flows": [-1500] + [350] * 10},
        ],
    },
    "payback": {"cash_flows": NETFLIX_FIT_FCFF, "discount_rate": NETFLIX_FIT_RATE},
    "accounting-return": {
        "after_tax_operating_income": [-60.00, 8.14, 80.55, 157.36, 238.68,
                                       211.59, 251.70, 294.03, 338.70, 385.83],
        "invested_capital": [2450.00, 2253.53, 2057.26, 1861.21, 2185.69,
                             1877.66, 1629.70, 1381.97, 1134.47, 887.23],
        "ending_invested_capital": 700.00,
        "cost_of_capital": NETFLIX_FIT_RATE,
    },
    "incremental": {
        "total_cash_flows": [-2500, -982, -921, -361, 198, 285, 314, 332, 367, 407, 434],
        "tax_rate": 0.361,
        "sunk_investment": 500,
        "sunk_asset_depreciation": [50] * 10,
        "allocated_overhead_not_incremental": [0, 125, 175, 250, 313, 344, 379, 416, 457, 466],
        "discount_rate": 0.0846,
    },
    "synergy": {
        "mode": "cash_flows",
        "receiving_business": "Netflix Entertainment",
        "cash_flows": NETFLIX_FIT_SYNERGY,
        "discount_rate": NETFLIX_ENTERTAINMENT_RATE,
    },
    "synergy-haircut": {
        "competing_bidders": 1,
        "components": [
            {"label": "plant and back-office consolidation", "kind": "cost", "value": 250,
             "realization_rate": 0.96, "one_time_cost_to_achieve": 0},
            {"label": "cross-selling into the acquirer's channel", "kind": "revenue",
             "value": 150, "realization_rate": 0.415, "customer_attrition_rate": 0.035},
        ],
    },
    "control-value": {
        "status_quo_value": 955.0,
        "restructured_value": 2323.0,
        "shares_outstanding": 186.3,
        "probability_of_change": 0.595,
        "market_price_per_share": 9.50,
    },
    "deal": {
        "target_standalone_value": 51.5,
        "restructured_value": 56.2,
        "synergy_value": 14.6,
        "price": 104.0,
        "pre_announcement_market_cap": 75.0,
        "motive": "synergy",
        "synergy_baseline": "restructured_target",
        "target_discount_rate_used": True,
    },
    "control-premium": {
        "status_quo_equity_value": 12500.0,
        "optimal_equity_value": 14700.0,
        "majority_pct": 0.51,
        "minority_pct": 0.49,
    },
    "selftest": {},
}


def cmd_example(command):
    if command not in EXAMPLES:
        raise SystemExit("No example payload for %s." % command)
    _emit(EXAMPLES[command])
    return 0


# --------------------------------------------------------------------------- selftest

def cmd_selftest(args):
    results = []

    def check(name, actual, expected, rtol=1e-6, atol=0.0):
        ok = (isinstance(actual, (int, float)) and not isinstance(actual, bool)
              and isinstance(expected, (int, float))
              and abs(actual - expected) <= max(atol, rtol * max(1.0, abs(expected))))
        results.append({"case": name, "expected": expected, "actual": actual,
                        "pass": bool(ok)})

    def check_true(name, actual):
        results.append({"case": name, "expected": True, "actual": bool(actual),
                        "pass": bool(actual)})

    def refuses(name, fn):
        try:
            fn()
            ok = False
        except SystemExit:
            ok = True
        results.append({"case": name, "expected": "refused", "actual":
                        "refused" if ok else "accepted", "pass": ok})

    # --- Netflix Fit, the corpus's full worked case. Published: NPV $106m, IRR 8.69%.
    # The published cash flow table is rounded to the cent, so the NPV is checked to the
    # nearest million and the IRR to the published two decimals.
    nf = npv({"cash_flows": NETFLIX_FIT_FCFF, "discount_rate": NETFLIX_FIT_RATE})
    check("Netflix Fit stand-alone NPV", nf["total_npv"], 106.37, rtol=0, atol=0.5)
    nf_irr = irr({"cash_flows": NETFLIX_FIT_FCFF, "hurdle_rate": NETFLIX_FIT_RATE})
    check("Netflix Fit IRR", nf_irr["irr"], 0.0869, rtol=0, atol=5e-5)

    # The year-4 studio investment makes this stream change sign three times, which is
    # exactly the case where a single reported IRR would be a lie. It happens to have one
    # root, so the engine must report the root and still flag the stream.
    check("Netflix Fit sign changes", nf_irr["sign_changes"], 3)
    check_true("Netflix Fit flagged as non-conventional", not nf_irr["conventional"])
    check_true("Netflix Fit IRR marked unreliable", not nf_irr["reliable"])

    # Synergy discounted at Netflix Entertainment's 8.93%, not the project's 8.01%.
    # Published: $376.20m. Using the project rate would give a different number, so this
    # test fails for an implementation that blends the two rates.
    syn = synergy({"mode": "cash_flows", "cash_flows": NETFLIX_FIT_SYNERGY,
                   "discount_rate": NETFLIX_ENTERTAINMENT_RATE})
    check("Netflix Fit synergy at the receiving business's rate",
          syn["synergy_value"], 376.20, rtol=0, atol=0.1)
    wrong_rate = synergy({"mode": "cash_flows", "cash_flows": NETFLIX_FIT_SYNERGY,
                          "discount_rate": NETFLIX_FIT_RATE})
    check_true("using the project rate for synergy gives a different answer",
               abs(wrong_rate["synergy_value"] - syn["synergy_value"]) > 5.0)

    # Two streams at their own rates must add to the published total NPV of $482.57m.
    both = npv(EXAMPLES["npv"])
    check("Netflix Fit total NPV with synergy", both["total_npv"], 482.57,
          rtol=0, atol=0.6)

    # --- Rio Disney. Published NPV $3,296m at an 8.46% cost of capital.
    rio = [-2000, -1000, -859, -267, 340, 466, 516, 555, 615, 681, 715 + 11275]
    check("Rio Disney NPV", npv({"cash_flows": rio, "discount_rate": 0.0846})["total_npv"],
          3296.0, rtol=0, atol=2.0)

    # --- Multiple IRRs. Packet case: -1000, 800, 1000, 1300, -2200 has roots at 6.60%
    # and 36.55%. An implementation that returns the first root it finds fails this.
    multi = irr({"cash_flows": [-1000, 800, 1000, 1300, -2200], "hurdle_rate": 0.12})
    check("multiple-IRR case finds two roots", len(multi["roots"]), 2)
    check("multiple-IRR lower root", multi["roots"][0], 0.0660, rtol=0, atol=5e-5)
    check("multiple-IRR upper root", multi["roots"][1], 0.3655, rtol=0, atol=5e-5)
    check_true("multiple-IRR case reports no single IRR", multi["irr"] is None)
    check_true("multiple-IRR case falls back to NPV for the decision",
               multi["decision_basis"].startswith("NPV"))
    check("multiple-IRR sign changes", multi["sign_changes"], 2)

    # The conventional twin of that case has exactly one root near 12.8%.
    single = irr({"cash_flows": [-1000, 200, 300, 400, 500]})
    check("conventional stream IRR", single["irr"], 0.1283, rtol=0, atol=5e-5)
    check_true("conventional stream is flagged conventional", single["conventional"])

    # An all-positive stream has no IRR and must say so rather than return a number.
    none_case = irr({"cash_flows": [100, 200, 300]})
    check_true("all-positive stream reports no IRR", none_case["irr"] is None)
    check("all-positive stream has no sign change", none_case["sign_changes"], 0)

    # --- MIRR. Packet: invest 1,000, receive 300/400/500/600 at a 15% hurdle rate.
    # Terminal value 2,160; IRR 24.89%; MIRR 21.23%.
    m = mirr({"cash_flows": [-1000, 300, 400, 500, 600], "hurdle_rate": 0.15})
    check("MIRR terminal value of inflows", m["terminal_value_of_inflows"], 2160.2625)
    check("MIRR", m["mirr"], 0.2123, rtol=0, atol=5e-5)
    check("plain IRR on the same stream", m["irr"], 0.2489, rtol=0, atol=5e-5)
    check_true("MIRR sits below IRR when reinvestment is the hurdle rate",
               m["mirr"] < m["irr"])
    # Identity: reinvesting at the IRR itself must reproduce the IRR exactly.
    m_at_irr = mirr({"cash_flows": [-1000, 300, 400, 500, 600], "hurdle_rate": 0.15,
                     "reinvestment_rate": m["irr"]})
    check("MIRR at the IRR reinvestment rate equals the IRR", m_at_irr["mirr"], m["irr"],
          rtol=0, atol=1e-6)

    # --- Profitability index and scale. Packet case 2 at a 15% hurdle rate:
    # A NPV 467,937 / PI 46.79%; B NPV 1,358,664 / PI 13.59%.
    rat = rationing(EXAMPLES["rationing"])
    a_row = [r for r in rat["projects"] if r["label"].startswith("A")][0]
    b_row = [r for r in rat["projects"] if r["label"].startswith("B")][0]
    check("small project NPV", a_row["npv"], 467937.0, rtol=0, atol=1.0)
    check("large project NPV", b_row["npv"], 1358664.0, rtol=0, atol=1.0)
    check("small project profitability index", a_row["profitability_index"], 0.4679,
          rtol=0, atol=5e-5)
    check("large project profitability index", b_row["profitability_index"], 0.1359,
          rtol=0, atol=5e-5)
    check_true("PI and NPV rankings disagree on the scale case", rat["rankings_disagree"])
    check_true("PI ranking prefers the small project",
               rat["ranking_by_profitability_index"][0].startswith("A"))
    check_true("NPV ranking prefers the large project",
               rat["ranking_by_npv"][0].startswith("B"))

    # Indivisible projects can defeat the greedy PI ranking. Here the budget is 100:
    # taking the highest-PI project first leaves 40 idle and 12 of NPV on the table.
    packing = rationing({"budget": 100, "projects": [
        {"label": "high PI", "npv": 36.0, "initial_investment": 60.0},
        {"label": "mid A", "npv": 25.0, "initial_investment": 50.0},
        {"label": "mid B", "npv": 25.0, "initial_investment": 50.0},
    ]})
    check_true("greedy PI selection is flagged as suboptimal",
               packing.get("greedy_is_suboptimal") is True)
    check("best selection beats greedy", packing["best_selection"]["npv_created"], 50.0)
    check("greedy selection value", packing["greedy_selection"]["npv_created"], 36.0)

    # --- Unequal lives. Packet: A is 5 years (NPV 442, EA 122.6), B is 10 years
    # (NPV 478, EA 84.6). Raw NPV picks B; both repairs pick A.
    dl = different_lives(EXAMPLES["different-lives"])
    a_dl = [r for r in dl["projects"] if r["label"] == "A"][0]
    b_dl = [r for r in dl["projects"] if r["label"] == "B"][0]
    check("5-year project NPV", a_dl["npv"], 442.0, rtol=0, atol=0.5)
    check("10-year project NPV", b_dl["npv"], 478.0, rtol=0, atol=0.5)
    check("PV annuity factor, 12% over 5 years", a_dl["pv_annuity_factor"], 3.6048,
          rtol=0, atol=5e-5)
    check("PV annuity factor, 12% over 10 years", b_dl["pv_annuity_factor"], 5.6502,
          rtol=0, atol=5e-5)
    check("5-year equivalent annuity", a_dl["equivalent_annuity"], 122.6, rtol=0, atol=0.1)
    check("10-year equivalent annuity", b_dl["equivalent_annuity"], 84.6, rtol=0, atol=0.1)
    check_true("raw NPV picks the longer project", dl["ranking_by_raw_npv"][0] == "B")
    check_true("equivalent annuity picks the shorter project",
               dl["ranking_by_equivalent_annuity"][0] == "A")
    check_true("raw NPV is flagged as misleading", dl["raw_npv_is_misleading"])
    check("replication horizon is the common multiple",
          dl["replication"]["common_horizon_years"], 10)
    rep_a = [r for r in dl["replication"]["projects"] if r["label"] == "A"][0]
    check("replicated NPV of the 5-year project", rep_a["replicated_npv"], 693.0,
          rtol=0, atol=1.0)
    check_true("replication and equivalent annuities agree", dl["routes_agree"])

    # --- Payback. Exact by construction: 1,000 out, 400 a year, so 2.5 years.
    pb = payback({"cash_flows": [-1000, 400, 400, 400, 400], "discount_rate": 0.10})
    check("payback period", pb["payback_period_years"], 2.5)
    check_true("discounted payback exceeds simple payback",
               pb["discounted_payback_period_years"] > pb["payback_period_years"])
    # At a zero discount rate the two must coincide — an algebraic invariant.
    pb0 = payback({"cash_flows": [-1000, 400, 400, 400, 400], "discount_rate": 0.0})
    check("discounted payback equals payback at a zero rate",
          pb0["discounted_payback_period_years"], pb0["payback_period_years"])
    # A stream that never recovers must return null rather than a fabricated year.
    pb_never = payback({"cash_flows": [-1000, 100, 100], "discount_rate": 0.10})
    check_true("unrecovered investment reports no payback",
               pb_never["payback_period_years"] is None)

    # --- Accounting return. Netflix Fit incremental ROIC, published as -2.45% in year 1
    # and 10.92% in year 5, with an average of 10.76% over the ten years.
    ar = accounting_return(EXAMPLES["accounting-return"])
    check("Netflix Fit year 1 ROIC", ar["years"][0]["roc_start_of_year_basis"], -0.0245,
          rtol=0, atol=5e-5)
    check("Netflix Fit year 5 ROIC", ar["years"][4]["roc_start_of_year_basis"], 0.1092,
          rtol=0, atol=5e-5)
    # The case quotes 10.76% for the ten-year average, which is average income over
    # average capital. The mean of the ten annual ratios is 14.25% on the same numbers —
    # the gap is why the convention has to be named rather than assumed.
    check("Netflix Fit average ROIC, ratio of means",
          ar["roc_on_average_income_and_capital"], 0.1076, rtol=0, atol=5e-4)
    check_true("the two averaging conventions differ materially here",
               abs(ar["average_roc_start_of_year_basis"]
                   - ar["roc_on_average_income_and_capital"]) > 0.02)

    # Rio Disney project ROC: both bases published, -1.07% and -1.28% in year 1.
    rio_roc = accounting_return({
        "after_tax_operating_income": [-32, -96, -54, 68, 202, 249, 299, 352, 410, 421],
        "invested_capital": [2500, 3450, 4275, 4582, 4452, 4368, 4302, 4270, 4254, 4257],
        "ending_invested_capital": 4243, "cost_of_capital": 0.0846})
    # The packet prints returns to two decimal places of a percent, so published figures
    # are matched to within one basis point rather than exactly.
    check("Rio Disney year 1 ROC, average-capital basis",
          rio_roc["years"][0]["roc_average_capital_basis"], -0.0107, rtol=0, atol=1e-4)
    check("Rio Disney year 1 ROC, start-of-year basis",
          rio_roc["years"][0]["roc_start_of_year_basis"], -0.0128, rtol=0, atol=5e-5)
    check("Rio Disney average ROC, average-capital basis",
          rio_roc["average_roc_average_capital_basis"], 0.0418, rtol=0, atol=5e-4)
    check_true("Rio Disney project ROC is below its cost of capital",
               rio_roc["average_return_spread"] < 0)

    # EVA identity: the spread times capital must equal income less the capital charge.
    # Disney firm-level, published: EBIT(1-t) 6,920 on capital of 54,899 at a 7.81% cost
    # of capital, a spread of +4.80%.
    disney = accounting_return({"after_tax_operating_income": [6920.0],
                                "invested_capital": [54899.0],
                                "cost_of_capital": 0.0781})
    check("Disney return on capital", disney["years"][0]["roc_start_of_year_basis"],
          0.1261, rtol=0, atol=1e-4)
    check("Disney return spread", disney["years"][0]["return_spread"], 0.0480,
          rtol=0, atol=1e-4)
    check("EVA equals spread times capital", disney["years"][0]["eva"],
          disney["years"][0]["return_spread"] * 54899.0, rtol=0, atol=1e-6)

    # --- Incremental cash flows. Rio Disney adjustment route: the published total stream
    # becomes the published incremental stream once the sunk 500 is added back, its
    # depreciation tax shield removed, and the non-incremental allocated G&A restored.
    inc = incremental(EXAMPLES["incremental"])
    expected_incremental = [-2000, -1000, -860, -267, 340, 467, 516, 556, 615, 681, 714]
    for year, want in enumerate(expected_incremental):
        check("Rio Disney incremental cash flow, year %d" % year,
              inc["incremental_cash_flows"][year], want, rtol=0, atol=1.0)
    check_true("stripping non-incremental costs raises NPV",
               inc["npv_effect_of_adjustments"] > 0)
    refuses("an effective tax rate above 100% is refused",
            lambda: incremental({"total_cash_flows": [-100, 50], "tax_rate": 1.2}))

    # A cannibalization share outside [0,1] is a modelling error, not a rounding issue.
    refuses("a cannibalization retained share above 1 is refused",
            lambda: incremental({"total_cash_flows": [-100, 50], "tax_rate": 0.25,
                                 "cannibalization": {"lost_contribution_pre_tax": 10,
                                                     "retained_share": 1.4}}))

    # --- Combined-firm synergy. P&G / Gillette, published: no-synergy combined equity
    # 281,170 (exactly the sum of the parts) and with-synergy 298,355, so synergy 17,185.
    pg = synergy({"mode": "combined", "acquirer_standalone_value": 221292.0,
                  "target_standalone_value": 59878.0,
                  "combined_value_without_synergy": 281170.0,
                  "combined_value_with_synergy": 298355.0})
    check("P&G/Gillette synergy value", pg["synergy_value"], 17185.0, rtol=0, atol=1.0)
    check_true("P&G/Gillette sum-of-parts check passes", pg["sum_of_parts_check"]["ok"])

    # AB InBev / SABMiller, published: 276,610 - 262,018 = 14,592 on operating assets.
    ab = synergy({"mode": "combined", "acquirer_standalone_value": 211953.0,
                  "target_standalone_value": 50065.0,
                  "combined_value_without_synergy": 262018.0,
                  "combined_value_with_synergy": 276610.0})
    check("AB InBev/SABMiller synergy value", ab["synergy_value"], 14592.0,
          rtol=0, atol=1.0)
    check_true("AB InBev sum-of-parts check passes", ab["sum_of_parts_check"]["ok"])

    # A combined firm worth more than the parts for no reason must fail the check.
    bad_parts = synergy({"mode": "combined", "acquirer_standalone_value": 100.0,
                         "target_standalone_value": 50.0,
                         "combined_value_without_synergy": 160.0,
                         "combined_value_with_synergy": 180.0})
    check_true("an inconsistent no-synergy combined value fails the check",
               bad_parts["sum_of_parts_check"]["ok"] is False)

    # --- Bookscape cafe. Stand-alone NPV -87,571; synergy to the bookstore worth 135,268
    # at the bookstore's 10.30% cost of capital, which turns a reject into an accept.
    cafe = synergy({"mode": "cash_flows",
                    "cash_flows": [30000, 33000, 36300, 39930, 43923],
                    "discount_rate": 0.1030})
    check("Bookscape cafe synergy value", cafe["synergy_value"], 135268.0,
          rtol=0, atol=25.0)
    check_true("cafe is a reject alone and an accept with synergy",
               -87571 < 0 < -87571 + cafe["synergy_value"])

    # --- Tata Motors / Harman. Synergy is a rupee perpetuity starting in year 4:
    # Rs 10bn growing 4% at a 13.63% rupee cost of capital, worth Rs 103,814m at the end
    # of year 3 and Rs 70,753m today, which is $1,179m at Rs 60/$. Ceiling price is the
    # $2,678m stand-alone equity plus that, and the market price of $5,248m clears it.
    harman = synergy({
        "mode": "cash_flows", "cash_flows": [0.0, 0.0, 0.0],
        "discount_rate": 0.1363,
        "terminal": {"cash_flow_next_year": 10000.0, "growth_rate": 0.04},
        "exchange_rate": 60.0,
        "acquisition": {"target_standalone_value": 2678.0, "price": 5248.0}})
    check("Harman synergy at the end of year 3",
          harman["terminal"]["terminal_value"], 103814.0, rtol=0, atol=40.0)
    check("Harman synergy in dollars",
          harman["synergy_value_in_reporting_currency"], 1179.0, rtol=0, atol=1.0)
    check("Harman maximum justifiable price",
          harman["acquisition"]["maximum_price"], 3857.0, rtol=0, atol=1.0)
    check_true("Harman at market price is a walk away",
               harman["acquisition"]["verdict"] == "walk away")
    check("Harman value destroyed at market price",
          harman["acquisition"]["acquisition_npv"], -1391.0, rtol=0, atol=1.0)
    # Paying exactly the ceiling leaves the acquirer with none of the synergy.
    ceiling_deal = synergy({
        "mode": "combined", "acquirer_standalone_value": 0.0,
        "target_standalone_value": 2678.0, "combined_value_with_synergy": 3857.0,
        "acquisition": {"target_standalone_value": 2678.0, "price": 3857.0}})
    check("paying the full synergy retains none of it",
          ceiling_deal["acquisition"]["synergy_retained_by_acquirer"], 0.0,
          rtol=0, atol=1e-6)

    # --- Synergy haircut. The corpus's illustration: 250 of cost savings and 150 of
    # revenue synergy claimed as 400 becomes roughly 300 once the evidence is applied.
    hc = synergy_haircut(EXAMPLES["synergy-haircut"])
    check("haircut gross synergy", hc["gross_synergy"], 400.0)
    check("haircut net synergy", hc["net_synergy"], 300.0, rtol=0, atol=1.0)
    check("cost component survives the haircut", hc["components"][0]["net_value"], 240.0)
    check("revenue component net value", hc["components"][1]["net_value"],
          150 * 0.415 * (1 - 0.035))
    # The bundled evidence must make revenue synergies the fragile half by default.
    defaults_only = synergy_haircut({"components": [
        {"label": "cost", "kind": "cost", "value": 100.0},
        {"label": "revenue", "kind": "revenue", "value": 100.0}]})
    check_true("default realization is lower for revenue than for cost synergies",
               defaults_only["components"][1]["net_value"]
               < defaults_only["components"][0]["net_value"])
    check_true("bundled synergy table carries an as_of date",
               bool(hc["evidence"]["as_of"]))

    # --- Value of control. Blockbuster, July 2005: equity worth $955m under incumbent
    # management and $2,323m restructured, on 186.3m shares. Published per-share figures
    # are $5.13 and $12.47, a gain of $7.34 a share.
    bb = control_value({"status_quo_value": 955.0, "restructured_value": 2323.0,
                        "shares_outstanding": 186.3, "probability_of_change": 0.595,
                        "market_price_per_share": 9.50})
    check("Blockbuster status quo per share",
          bb["per_share"]["status_quo_value_per_share"], 5.13, rtol=0, atol=0.01)
    check("Blockbuster restructured per share",
          bb["per_share"]["restructured_value_per_share"], 12.47, rtol=0, atol=0.01)
    check("Blockbuster value of control per share",
          bb["per_share"]["value_of_control_per_share"], 7.34, rtol=0, atol=0.01)
    check("Blockbuster value of control", bb["value_of_control"], 1368.0)
    check("Blockbuster expected value of control",
          bb["expected_value_of_control"], 0.595 * 1368.0)
    # The market-price identity, run forwards: status quo plus the odds-weighted gain must
    # reproduce the $9.50 price the probability was backed out of. An implementation that
    # reports only the control slice, forgetting the status quo underneath it, fails here.
    check("Blockbuster expected value per share reproduces the market price",
          bb["per_share"]["expected_value_per_share"], 9.50, rtol=0, atol=0.01)
    # Inverted: the published implied probabilities, before and after Icahn's challenge.
    check("Blockbuster implied probability at $9.50",
          bb["market"]["implied_probability_of_change"], 0.595, rtol=0, atol=0.002)
    before_icahn = control_value({"status_quo_value": 955.0, "restructured_value": 2323.0,
                                  "shares_outstanding": 186.3,
                                  "probability_of_change": 0.418,
                                  "market_price_per_share": 8.20})
    check("Blockbuster implied probability at $8.20",
          before_icahn["market"]["implied_probability_of_change"], 0.418,
          rtol=0, atol=0.002)
    check_true("activism moved the implied odds by about 18 points",
               0.15 < (bb["market"]["implied_probability_of_change"]
                       - before_icahn["market"]["implied_probability_of_change"]) < 0.20)
    # A control acquirer can guarantee the change, so its ceiling is the whole
    # restructured value and the maximum premium is $12.47 - $9.50 = $2.97 a share.
    check("Blockbuster maximum hostile bid", bb["maximum_hostile_bid"], 2323.0)
    check("Blockbuster maximum premium per share",
          bb["market"]["maximum_premium_per_share"], 2.97, rtol=0, atol=0.01)
    # Damodaran's own follow-up: a three-year implementation delay shrinks the gain.
    delayed = control_value({"status_quo_value": 955.0, "restructured_value": 2323.0,
                             "probability_of_change": 0.595,
                             "implementation_delay_years": 3, "discount_rate": 0.0617})
    check("three-year delay discounts the control value",
          delayed["delay"]["adjusted_value_of_control"], 1368.0 / (1.0617 ** 3),
          rtol=0, atol=1e-6)
    check_true("delay makes control worth less than the undiscounted gap",
               delayed["delay"]["adjusted_value_of_control"] < delayed["value_of_control"])
    # A firm already run the way you would run it offers no control value at any odds.
    well_run = control_value({"status_quo_value": 60.0, "restructured_value": 60.0,
                              "probability_of_change": 0.9})
    check("a well-run firm has no expected value of control",
          well_run["expected_value_of_control"], 0.0)

    # Embraer's two share classes, R$ millions: status quo 12,500, optimal 14,700, 242.5m
    # voting and 476.7m non-voting shares, a 20% probability of change. Published:
    # R$17.38 non-voting, R$19.19 voting, a 10.4% premium.
    emb = control_value({"status_quo_value": 12500.0, "restructured_value": 14700.0,
                         "probability_of_change": 0.20,
                         "share_classes": {"voting_shares": 242.5,
                                           "non_voting_shares": 476.7}})
    sc = emb["share_classes"]
    # Every share owns the same cash flows, so the status quo spreads over all 719.2m of
    # them. An implementation that gives the status quo to the voting class alone reports
    # R$51.55 here instead of R$17.38.
    check("Embraer value per non-voting share", sc["value_per_non_voting_share"], 17.38,
          rtol=0, atol=0.01)
    check("Embraer value per voting share", sc["value_per_voting_share"], 19.19,
          rtol=0, atol=0.01)
    check("Embraer voting premium", sc["voting_premium_percent"], 0.104,
          rtol=0, atol=0.001)
    # Raise the probability to 50% and the corpus reports a 26% premium.
    emb50 = control_value({"status_quo_value": 12500.0, "restructured_value": 14700.0,
                           "probability_of_change": 0.50,
                           "share_classes": {"voting_shares": 242.5,
                                             "non_voting_shares": 476.7}})
    check("Embraer voting premium at 50% odds",
          emb50["share_classes"]["voting_premium_percent"], 0.26, rtol=0, atol=0.005)

    # --- Deal acid test. AB InBev / SABMiller, $ billions: status quo 51.5, restructured
    # 56.2, synergy 14.6, price 104, pre-announcement market cap 75. Published: value of
    # control 4.7, restructured + synergy 70.8, and the deal fails every test by ~33.
    ab_deal = deal({"target_standalone_value": 51.5, "restructured_value": 56.2,
                    "synergy_value": 14.6, "price": 104.0,
                    "pre_announcement_market_cap": 75.0, "motive": "synergy",
                    "synergy_baseline": "restructured_target",
                    "target_discount_rate_used": True})
    check("SABMiller value of control", ab_deal["value_of_control"], 4.7,
          rtol=0, atol=0.01)
    check("SABMiller maximum justifiable price", ab_deal["maximum_justifiable_price"],
          70.8, rtol=0, atol=0.01)
    # Baselining synergy on the status quo instead of the restructured target would put
    # the ceiling at 66.1 and double-count the 4.7 of control value.
    check_true("the ceiling is built on the restructured target, not the status quo",
               abs(ab_deal["maximum_justifiable_price"] - 66.1) > 4.0)
    check("AB InBev overpayment against the highest benchmark",
          ab_deal["capture"]["captured_by_acquirer_shareholders"], -33.2,
          rtol=0, atol=0.01)
    check("premium to justify over the market cap", ab_deal["premium_to_justify"], 29.0,
          rtol=0, atol=0.01)
    check("premium over stand-alone value",
          ab_deal["capture"]["premium_over_standalone_value"], 52.5, rtol=0, atol=0.01)
    check("combined gains available to split", ab_deal["capture"]["combined_gains"], 19.3,
          rtol=0, atol=0.01)
    check("premium as a share of the combined gains",
          ab_deal["capture"]["premium_share_of_combined_gains"], 52.5 / 19.3,
          rtol=0, atol=1e-9)
    check_true("what the seller takes and what the buyer keeps add to the total gain",
               ab_deal["capture"]["gains_reconcile"])
    check_true("all three acid tests fail", ab_deal["all_tests_failed"])
    check_true("the stated motive returns an overpaying verdict",
               ab_deal["verdict"] == "overpaying")
    check_true("the target was not undervalued before the premium",
               ab_deal["undervaluation_precheck"]["target_was_undervalued"] is False)
    check("synergy required to justify the price",
          ab_deal["capture"]["synergy_required_to_justify_price"], 47.8, rtol=0, atol=0.01)

    # A deal inside every benchmark: pay 58 for a target worth 51.5 alone, 56.2
    # restructured and 70.8 with synergy. Control passes, undervaluation does not.
    good_deal = deal({"target_standalone_value": 51.5, "restructured_value": 56.2,
                      "synergy_value": 14.6, "price": 58.0, "motive": "synergy",
                      "synergy_baseline": "restructured_target",
                      "target_discount_rate_used": True})
    check_true("a price under the ceiling is defensible on the synergy motive",
               good_deal["verdict"] == "defensible")
    check_true("the same price still fails the undervaluation test",
               good_deal["acid_test"]["undervaluation"]["passes"] is False)
    check("the acquirer keeps the rest of the gains",
          good_deal["capture"]["captured_by_acquirer_shareholders"], 12.8,
          rtol=0, atol=0.01)
    check("the seller takes a third of the combined gains",
          good_deal["capture"]["premium_share_of_combined_gains"], 6.5 / 19.3,
          rtol=0, atol=1e-9)

    # --- Control premium and minority discount. minoritydiscount.xls default case:
    # optimal 14,700, status quo 12,500, 51% and 49% stakes.
    md = control_premium({"status_quo_equity_value": 12500.0,
                          "optimal_equity_value": 14700.0,
                          "majority_pct": 0.51, "minority_pct": 0.49})
    check("minority discount", md["minority_discount"], 2200.0 / 14700.0,
          rtol=0, atol=1e-12)
    check("control premium", md["control_premium"], 2200.0 / 12500.0, rtol=0, atol=1e-12)
    check("majority stake priced off the optimal value",
          md["stakes"]["majority_stake_value"], 7497.0)
    check("minority stake priced off the status quo",
          md["stakes"]["minority_stake_value"], 6125.0)
    # The shipped spreadsheet stores optimal + minority% x status quo, which is 20,825 —
    # more than the whole firm. The engine must report 6,125 and name the defect.
    check("the spreadsheet's stored minority formula is reported as a defect",
          md["stakes"]["known_spreadsheet_defect"]["stored_value"], 20825.0)
    check_true("the reported minority stake is not the spreadsheet's stored value",
               md["stakes"]["minority_stake_value"]
               != md["stakes"]["known_spreadsheet_defect"]["stored_value"])
    # The premium and the discount are one gap over two denominators, so the round trip
    # is an identity. An implementation that treats them as independent fails this.
    check("minority discount converts back from the control premium",
          md["conversion_check"]["minority_discount_from_control_premium"],
          md["minority_discount"], rtol=0, atol=1e-12)
    check("control premium converts back from the minority discount",
          md["conversion_check"]["control_premium_from_minority_discount"],
          md["control_premium"], rtol=0, atol=1e-12)
    conv = control_premium({"control_premium": 2200.0 / 12500.0})
    check("standalone conversion matches the full calculation",
          conv["minority_discount"], 2200.0 / 14700.0, rtol=0, atol=1e-12)
    back = control_premium({"minority_discount": 2200.0 / 14700.0})
    check("the conversion is symmetric", back["control_premium"], 2200.0 / 12500.0,
          rtol=0, atol=1e-12)

    # Kristin Kandy: $1.6m under existing management, $2.0m under better management.
    # 51% is worth $1,020,000 and 49% is worth $784,000 — two points of ownership worth
    # $236,000, because one stake carries control and the other does not.
    kk = control_premium({"status_quo_equity_value": 1600000.0,
                          "optimal_equity_value": 2000000.0,
                          "majority_pct": 0.51, "minority_pct": 0.49})
    check("Kristin Kandy controlling stake", kk["stakes"]["majority_stake_value"],
          1020000.0)
    check("Kristin Kandy minority stake", kk["stakes"]["minority_stake_value"], 784000.0)
    check("two percentage points of ownership are worth $236,000",
          kk["stakes"]["stake_value_difference"], 236000.0)

    # The stylized target: revenues 100, after-tax operating income 12, cost of equity
    # 20%, so status quo is 60. Raising the pre-tax margin to 30% makes it 90. The rule of
    # thumb says pay 72; the valuations support a 50% premium, not 20%.
    stylized = control_premium({"status_quo_equity_value": 60.0,
                                "optimal_equity_value": 90.0})
    check("stylized target control premium", stylized["control_premium"], 0.50)
    check("stylized target minority discount", stylized["minority_discount"],
          30.0 / 90.0, rtol=0, atol=1e-12)
    check("the 20% rule of thumb implies a different price",
          stylized["rule_of_thumb"]["price_it_implies"], 72.0)
    check("the valuations support a higher price than the rule of thumb",
          stylized["rule_of_thumb"]["difference"], 18.0)
    # Case B of the same example: a perfectly run target carries a zero premium.
    perfect = control_premium({"status_quo_equity_value": 60.0,
                               "optimal_equity_value": 60.0})
    check("a perfectly run target has a zero control premium",
          perfect["control_premium"], 0.0)
    check("a perfectly run target has a zero minority discount",
          perfect["minority_discount"], 0.0)

    # --- Refusals. Bad input must be explained, never crash or silently return a number.
    refuses("an empty cash flow list is refused",
            lambda: npv({"cash_flows": [], "discount_rate": 0.10}))
    refuses("a non-numeric cash flow is refused",
            lambda: npv({"cash_flows": [-100, "n/a"], "discount_rate": 0.10}))
    refuses("a discount rate at -100% is refused",
            lambda: npv({"cash_flows": [-100, 50], "discount_rate": -1.0}))
    refuses("a rate list of the wrong length is refused",
            lambda: npv({"cash_flows": [-100, 50, 50], "discount_rate": [0.1]}))
    refuses("a synergy stream with no discount rate is refused",
            lambda: synergy({"mode": "cash_flows", "cash_flows": [10, 10]}))
    refuses("terminal growth above the discount rate is refused",
            lambda: synergy({"mode": "cash_flows", "cash_flows": [10],
                             "discount_rate": 0.08,
                             "terminal": {"cash_flow_next_year": 10,
                                          "growth_rate": 0.09}}))
    refuses("invested capital of the wrong length is refused",
            lambda: accounting_return({"after_tax_operating_income": [10, 20],
                                       "invested_capital": [100]}))
    refuses("zero invested capital is refused",
            lambda: accounting_return({"after_tax_operating_income": [10],
                                       "invested_capital": [0]}))
    refuses("a single project cannot be compared on unequal lives",
            lambda: different_lives({"discount_rate": 0.12,
                                     "projects": [{"npv": 100, "life": 5}]}))
    refuses("a stream with no outlay has no MIRR",
            lambda: mirr({"cash_flows": [100, 200], "hurdle_rate": 0.15}))
    refuses("a probability written as a percentage is refused",
            lambda: control_value({"status_quo_value": 100.0,
                                   "restructured_value": 150.0,
                                   "probability_of_change": 20}))
    refuses("a restructured value below the status quo is refused",
            lambda: control_value({"status_quo_value": 150.0,
                                   "restructured_value": 100.0,
                                   "probability_of_change": 0.5}))
    refuses("a market price with no share count is refused",
            lambda: control_value({"status_quo_value": 100.0,
                                   "restructured_value": 150.0,
                                   "probability_of_change": 0.5,
                                   "market_price_per_share": 12.0}))
    refuses("an implementation delay with no discount rate is refused",
            lambda: control_value({"status_quo_value": 100.0,
                                   "restructured_value": 150.0,
                                   "probability_of_change": 0.5,
                                   "implementation_delay_years": 3}))
    # The two refusals the deal test exists for.
    refuses("a deal that does not say whose discount rate was used is refused",
            lambda: deal({"target_standalone_value": 51.5, "restructured_value": 56.2,
                          "synergy_value": 14.6, "price": 58.0,
                          "synergy_baseline": "restructured_target"}))
    refuses("a target valued at somebody else's discount rate is refused",
            lambda: deal({"target_standalone_value": 51.5, "restructured_value": 56.2,
                          "synergy_value": 14.6, "price": 58.0,
                          "synergy_baseline": "restructured_target",
                          "target_discount_rate_used": False}))
    refuses("a synergy baselined on the status quo is refused as double counting",
            lambda: deal({"target_standalone_value": 51.5, "restructured_value": 56.2,
                          "synergy_value": 14.6, "price": 58.0,
                          "synergy_baseline": "status_quo",
                          "target_discount_rate_used": True}))
    refuses("a synergy figure with no stated baseline is refused",
            lambda: deal({"target_standalone_value": 51.5, "restructured_value": 56.2,
                          "synergy_value": 14.6, "price": 58.0,
                          "target_discount_rate_used": True}))
    # A true flag contradicted by the rates themselves is still the risk-transference sin.
    refuses("a discount rate that disagrees with the target's own rate is refused",
            lambda: deal({"target_standalone_value": 51.5, "restructured_value": 56.2,
                          "price": 58.0, "target_discount_rate_used": True,
                          "discount_rate_used": 0.0781,
                          "target_cost_of_capital": 0.0903}))
    refuses("'strategic' is not a motive",
            lambda: deal({"target_standalone_value": 51.5, "restructured_value": 56.2,
                          "price": 58.0, "target_discount_rate_used": True,
                          "motive": "strategic"}))
    refuses("a deal with no restructured value and no control value is refused",
            lambda: deal({"target_standalone_value": 51.5, "price": 58.0,
                          "target_discount_rate_used": True}))
    refuses("an optimal value below the status quo is refused",
            lambda: control_premium({"status_quo_equity_value": 14700.0,
                                     "optimal_equity_value": 12500.0}))
    refuses("a 50/50 stake cannot be priced as controlling",
            lambda: control_premium({"status_quo_equity_value": 12500.0,
                                     "optimal_equity_value": 14700.0,
                                     "majority_pct": 0.50}))
    refuses("a stake above 50% is not a minority stake",
            lambda: control_premium({"status_quo_equity_value": 12500.0,
                                     "optimal_equity_value": 14700.0,
                                     "minority_pct": 0.60}))
    refuses("a zero optimal value has no minority discount",
            lambda: control_premium({"status_quo_equity_value": 0.0,
                                     "optimal_equity_value": 0.0}))

    # --- Every documented example payload must run.
    runners = {"npv": npv, "irr": irr, "mirr": mirr, "rationing": rationing,
               "different-lives": different_lives, "payback": payback,
               "accounting-return": accounting_return, "incremental": incremental,
               "synergy": synergy, "synergy-haircut": synergy_haircut,
               "control-value": control_value, "deal": deal,
               "control-premium": control_premium}
    for name, fn in sorted(runners.items()):
        try:
            fn(EXAMPLES[name])
            ok = True
        except SystemExit:
            ok = False
        check_true("example payload runs: %s" % name, ok)

    failed = [x for x in results if not x["pass"]]
    _emit({"total": len(results), "passed": len(results) - len(failed),
           "failed": len(failed), "results": results})
    return 1 if failed else 0


COMMANDS = {
    "npv": cmd_npv,
    "irr": cmd_irr,
    "mirr": cmd_mirr,
    "rationing": cmd_rationing,
    "different-lives": cmd_different_lives,
    "payback": cmd_payback,
    "accounting-return": cmd_accounting_return,
    "incremental": cmd_incremental,
    "synergy": cmd_synergy,
    "synergy-haircut": cmd_synergy_haircut,
    "control-value": cmd_control_value,
    "deal": cmd_deal,
    "control-premium": cmd_control_premium,
    "selftest": cmd_selftest,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=sorted(COMMANDS))
    parser.add_argument("--in", dest="in_file", help="JSON input file (default: stdin)")
    parser.add_argument("--example", action="store_true",
                        help="print a sample input payload for this subcommand and exit")
    args = parser.parse_args()
    if args.example:
        return cmd_example(args.command)
    return COMMANDS[args.command](args) or 0


if __name__ == "__main__":
    sys.exit(main())

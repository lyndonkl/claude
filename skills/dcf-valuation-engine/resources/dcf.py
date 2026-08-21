#!/usr/bin/env python3
"""
dcf.py — the discounted cash flow engine.

Given a set of value drivers, this builds the year-by-year forecast, closes it with a
terminal value, adjusts for failure risk, walks the bridge from operating assets to
equity, and divides by shares. It also runs the arithmetic backwards: given a market
price, what growth or margin does that price already assume.

The engine computes. It never invents a driver. Revenue growth, target margin,
sales-to-capital and terminal growth are the analyst's judgments and arrive as inputs.

Pure standard library. No third-party packages, ever — this must run anywhere.

SUBCOMMANDS
  value          drivers -> full forecast, terminal value, equity bridge, value per share
  sensitivity    re-run `value` across a grid of two drivers
  implied        solve for the driver value that makes the DCF equal the market price
  selftest       run the bundled worked examples and report pass/fail

Each subcommand reads a JSON payload (--in FILE, or stdin) and writes JSON to stdout.
Run any subcommand with --example to print a sample input payload.
"""

import argparse
import copy
import json
import sys

# Bisection on a single driver converges to well past input precision in ~60 passes;
# 200 is a ceiling that still returns promptly on a pathological, non-monotonic input.
MAX_SOLVER_ITERATIONS = 200
SOLVER_TOLERANCE = 1e-9


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
    return json.loads(data)


def _emit(obj):
    print(json.dumps(obj, indent=2))


# ------------------------------------------------------------------ driver expansion

def _expand(spec, years, label):
    """Turn a driver spec into a per-year list.

    Accepts three shapes:
      - a number: constant across every year
      - a list: used as given (must be exactly `years` long)
      - {"start": x, "end": y, "converge_by": n}: linear glide from x to y by year n,
        then flat at y. This is how growth, margin and cost of capital fade toward
        their stable-period values.
    """
    if isinstance(spec, (int, float)):
        return [float(spec)] * years
    if isinstance(spec, list):
        if len(spec) != years:
            raise SystemExit(
                "%s has %d entries but the forecast is %d years." % (label, len(spec), years))
        return [float(v) for v in spec]
    if isinstance(spec, dict):
        start = float(spec["start"])
        end = float(spec["end"])
        converge_by = int(spec.get("converge_by", years))
        if converge_by < 1:
            raise SystemExit("%s.converge_by must be at least 1." % label)
        out = []
        for year in range(1, years + 1):
            if year >= converge_by:
                out.append(end)
            else:
                out.append(start + (end - start) * (year / converge_by))
        return out
    raise SystemExit("%s must be a number, a list, or a {start,end,converge_by} object." % label)


# ------------------------------------------------------------------------ core engine

def value(p):
    years = int(p.get("forecast_years", 10))
    base_revenue = float(p["base_revenue"])
    base_ebit = float(p.get("base_ebit", 0.0))
    invested_capital = float(p.get("base_invested_capital", 0.0))

    growth = _expand(p["revenue_growth"], years, "revenue_growth")
    margin = _expand(p["operating_margin"], years, "operating_margin")
    sales_to_capital = _expand(p.get("sales_to_capital", 2.0), years, "sales_to_capital")
    tax_rate = _expand(p.get("tax_rate", 0.25), years, "tax_rate")
    discount = _expand(p["cost_of_capital"], years, "cost_of_capital")

    terminal = p["terminal"]
    g_terminal = float(terminal["growth_rate"])
    wacc_terminal = float(terminal["cost_of_capital"])
    tax_terminal = float(terminal.get("tax_rate", tax_rate[-1]))
    if wacc_terminal <= g_terminal:
        raise SystemExit(
            "Terminal cost of capital (%.4f) must exceed terminal growth (%.4f); "
            "otherwise the terminal value is infinite or negative."
            % (wacc_terminal, g_terminal))

    nol = float(p.get("net_operating_loss_carryforward", 0.0))

    rows = []
    revenue = base_revenue
    capital = invested_capital
    cumulative_discount = 1.0
    for i in range(years):
        prior_revenue = revenue
        revenue = revenue * (1 + growth[i])
        ebit = revenue * margin[i]

        # Losses shelter later profits: the carryforward absorbs income before tax applies.
        if ebit <= 0:
            taxes = 0.0
            nol += -ebit
        elif ebit <= nol:
            taxes = 0.0
            nol -= ebit
        else:
            taxable = ebit - nol
            taxes = taxable * tax_rate[i]
            nol = 0.0
        ebit_after_tax = ebit - taxes

        # Growth has to be bought. Reinvestment is the new revenue divided by the
        # efficiency with which this business converts capital into sales.
        delta_revenue = revenue - prior_revenue
        if sales_to_capital[i] <= 0:
            raise SystemExit("sales_to_capital must be positive in year %d." % (i + 1))
        reinvestment = delta_revenue / sales_to_capital[i]
        if i == 0 and reinvestment < 0:
            # A first-year revenue decline does not hand cash back; later years may.
            reinvestment = 0.0

        fcff = ebit_after_tax - reinvestment
        capital += reinvestment
        cumulative_discount *= (1 + discount[i])
        rows.append({
            "year": i + 1,
            "revenue_growth": growth[i], "revenue": revenue,
            "operating_margin": margin[i], "ebit": ebit,
            "tax_rate": tax_rate[i], "taxes": taxes, "ebit_after_tax": ebit_after_tax,
            "sales_to_capital": sales_to_capital[i], "reinvestment": reinvestment,
            "fcff": fcff, "invested_capital": capital,
            "roic": (ebit_after_tax / capital) if capital else None,
            "cost_of_capital": discount[i],
            "cumulative_discount_factor": 1 / cumulative_discount,
            "present_value": fcff / cumulative_discount,
        })

    # Terminal year: one more year of growth, then a perpetuity.
    terminal_revenue = rows[-1]["revenue"] * (1 + g_terminal)
    terminal_margin = float(terminal.get("operating_margin", margin[-1]))
    terminal_ebit = terminal_revenue * terminal_margin
    terminal_ebit_after_tax = terminal_ebit * (1 - tax_terminal)
    terminal_roic = float(terminal.get("return_on_capital", wacc_terminal))

    # Growth in perpetuity must be paid for at the terminal return on capital.
    if g_terminal > 0:
        if terminal_roic <= 0:
            raise SystemExit("terminal.return_on_capital must be positive when terminal growth is positive.")
        terminal_reinvestment_rate = g_terminal / terminal_roic
        if terminal_reinvestment_rate > 1:
            raise SystemExit(
                "Terminal growth of %.4f at a return on capital of %.4f implies reinvesting "
                "%.0f%% of income, which is impossible. Lower the growth rate or raise the return."
                % (g_terminal, terminal_roic, terminal_reinvestment_rate * 100))
    else:
        terminal_reinvestment_rate = 0.0
    terminal_reinvestment = terminal_ebit_after_tax * terminal_reinvestment_rate
    terminal_fcff = terminal_ebit_after_tax - terminal_reinvestment
    terminal_value = terminal_fcff / (wacc_terminal - g_terminal)
    pv_terminal = terminal_value * rows[-1]["cumulative_discount_factor"]

    pv_explicit = sum(r["present_value"] for r in rows)
    going_concern_value = pv_explicit + pv_terminal

    # Failure branch: a going-concern DCF alone assumes the firm survives to collect it.
    failure = p.get("failure", {}) or {}
    prob_failure = float(failure.get("probability", 0.0))
    if prob_failure:
        basis = failure.get("proceeds_basis", "going_concern")
        pct = float(failure.get("proceeds_percent", 0.5))
        if basis == "book_value":
            distress_proceeds = float(failure["book_value_of_capital"]) * pct
        else:
            distress_proceeds = going_concern_value * pct
    else:
        distress_proceeds = 0.0
    operating_assets = going_concern_value * (1 - prob_failure) + distress_proceeds * prob_failure

    # Bridge from the operating business to what a share is worth.
    bridge = p.get("bridge", {}) or {}
    debt = float(bridge.get("debt", 0.0))
    minority = float(bridge.get("minority_interests", 0.0))
    cash = float(bridge.get("cash", 0.0))
    non_operating = float(bridge.get("non_operating_assets", 0.0))
    options_value = float(bridge.get("employee_options_value", 0.0))
    shares = float(bridge.get("shares_outstanding", 0.0))

    equity_value = operating_assets - debt - minority + cash + non_operating
    equity_in_common = equity_value - options_value
    value_per_share = (equity_in_common / shares) if shares else None

    out = {
        "forecast": rows,
        "terminal": {
            "growth_rate": g_terminal, "cost_of_capital": wacc_terminal,
            "revenue": terminal_revenue, "operating_margin": terminal_margin,
            "ebit": terminal_ebit, "ebit_after_tax": terminal_ebit_after_tax,
            "return_on_capital": terminal_roic,
            "reinvestment_rate": terminal_reinvestment_rate,
            "reinvestment": terminal_reinvestment, "fcff": terminal_fcff,
            "terminal_value": terminal_value, "present_value": pv_terminal,
        },
        "present_value_of_explicit_forecast": pv_explicit,
        "present_value_of_terminal_value": pv_terminal,
        "terminal_value_share_of_total": (pv_terminal / going_concern_value) if going_concern_value else None,
        "going_concern_value": going_concern_value,
        "failure": {"probability": prob_failure, "distress_proceeds": distress_proceeds},
        "value_of_operating_assets": operating_assets,
        "bridge": {
            "value_of_operating_assets": operating_assets, "less_debt": debt,
            "less_minority_interests": minority, "plus_cash": cash,
            "plus_non_operating_assets": non_operating,
            "equity_value": equity_value,
            "less_employee_options": options_value,
            "equity_in_common_stock": equity_in_common,
            "shares_outstanding": shares,
        },
        "value_per_share": value_per_share,
    }
    price = bridge.get("current_price")
    if price and value_per_share:
        out["price_check"] = {
            "current_price": price, "value_per_share": value_per_share,
            "price_as_percent_of_value": price / value_per_share,
            "upside": value_per_share / price - 1,
            "verdict_hint": "undervalued" if value_per_share > price else "overvalued",
        }
    if p.get("currency"):
        out["currency"] = p["currency"]
    return out


def cmd_value(args):
    _emit(value(_read_payload(args)))


# ------------------------------------------------------------------------ sensitivity

def _set_path(payload, path, new_value):
    """Set a dotted path such as `terminal.growth_rate` or `revenue_growth.start`."""
    parts = path.split(".")
    node = payload
    for key in parts[:-1]:
        if key not in node or not isinstance(node[key], dict):
            raise SystemExit("Cannot set %r: %r is not an object in the payload." % (path, key))
        node = node[key]
    leaf = parts[-1]
    if isinstance(node.get(leaf), (dict, list)) and not isinstance(new_value, (dict, list)):
        raise SystemExit(
            "Cannot set %r to a scalar: it currently holds a %s. Point at a leaf such as "
            "'revenue_growth.start' instead." % (path, type(node[leaf]).__name__))
    node[leaf] = new_value


def sensitivity(p):
    base = p["base_case"]
    axes = p["axes"]
    if not 1 <= len(axes) <= 2:
        raise SystemExit("Provide one or two axes.")
    grid = []
    if len(axes) == 1:
        for v in axes[0]["values"]:
            trial = copy.deepcopy(base)
            _set_path(trial, axes[0]["path"], v)
            r = value(trial)
            grid.append({axes[0]["path"]: v, "value_per_share": r["value_per_share"],
                         "value_of_operating_assets": r["value_of_operating_assets"]})
    else:
        for v1 in axes[0]["values"]:
            row = []
            for v2 in axes[1]["values"]:
                trial = copy.deepcopy(base)
                _set_path(trial, axes[0]["path"], v1)
                _set_path(trial, axes[1]["path"], v2)
                r = value(trial)
                row.append({axes[1]["path"]: v2, "value_per_share": r["value_per_share"]})
            grid.append({axes[0]["path"]: v1, "results": row})
    out = {"axes": [a["path"] for a in axes], "grid": grid}
    values = ([g["value_per_share"] for g in grid] if len(axes) == 1
              else [c["value_per_share"] for g in grid for c in g["results"]])
    values = [v for v in values if v is not None]
    if values:
        out["range"] = {"min": min(values), "max": max(values),
                        "base": value(base)["value_per_share"]}
    return out


def cmd_sensitivity(args):
    _emit(sensitivity(_read_payload(args)))


# ------------------------------------------------------- implied expectations (solver)

def implied(p):
    """Solve for the driver value at which the DCF reproduces the market price.

    This is the reverse-engineering move: rather than asking what the company is worth,
    it asks what the market must already believe. Bisection needs the value per share to
    move monotonically in the driver, which holds for growth, margin and cost of capital
    over any sensible range.
    """
    base = p["base_case"]
    path = p["path"]
    target = float(p["target_value_per_share"])
    lo = float(p.get("low", 0.0))
    hi = float(p.get("high", 0.5))

    def value_at(x):
        trial = copy.deepcopy(base)
        _set_path(trial, path, x)
        try:
            return value(trial)["value_per_share"]
        except SystemExit:
            # An infeasible driver (terminal growth above the discount rate, say) is a
            # hard boundary for the search, not a crash.
            return None

    v_lo, v_hi = value_at(lo), value_at(hi)
    if v_lo is None or v_hi is None:
        raise SystemExit(
            "The search bounds [%g, %g] contain infeasible assumptions for %s. "
            "Narrow them and retry." % (lo, hi, path))
    if (v_lo - target) * (v_hi - target) > 0:
        raise SystemExit(
            "Target %.4f is outside the achievable range over %s in [%g, %g] "
            "(value spans %.4f to %.4f). Widen the bounds or change the driver."
            % (target, path, lo, hi, min(v_lo, v_hi), max(v_lo, v_hi)))

    increasing = v_hi > v_lo
    for _ in range(MAX_SOLVER_ITERATIONS):
        mid = (lo + hi) / 2
        v_mid = value_at(mid)
        if v_mid is None:
            hi = mid
            continue
        if abs(v_mid - target) < SOLVER_TOLERANCE:
            break
        if (v_mid < target) == increasing:
            lo = mid
        else:
            hi = mid
    solution = (lo + hi) / 2
    return {"path": path, "target_value_per_share": target, "implied_value": solution,
            "achieved_value_per_share": value_at(solution),
            "base_value_per_share": value(base)["value_per_share"]}


def cmd_implied(args):
    _emit(implied(_read_payload(args)))


# ---------------------------------------------------------------------------- selftest

_SIMPLE = {
    "base_revenue": 1000.0, "base_ebit": 100.0, "base_invested_capital": 500.0,
    "forecast_years": 5,
    "revenue_growth": 0.10, "operating_margin": 0.10, "sales_to_capital": 2.0,
    "tax_rate": 0.25, "cost_of_capital": 0.10,
    "terminal": {"growth_rate": 0.02, "cost_of_capital": 0.08, "return_on_capital": 0.12},
    "bridge": {"debt": 200.0, "cash": 100.0, "shares_outstanding": 100.0},
}

EXAMPLES = {
    "value": _SIMPLE,
    "sensitivity": {"base_case": _SIMPLE,
                    "axes": [{"path": "terminal.growth_rate", "values": [0.01, 0.02, 0.03]},
                             {"path": "operating_margin", "values": [0.08, 0.10, 0.12]}]},
    "implied": {"base_case": _SIMPLE, "path": "operating_margin",
                "target_value_per_share": 12.0, "low": 0.01, "high": 0.30},
}


def cmd_selftest(args):
    results = []

    def check(name, actual, expected, tol=1e-6):
        ok = (expected is True and actual is True) or (
            isinstance(actual, (int, float)) and isinstance(expected, (int, float))
            and abs(actual - expected) <= tol * max(1.0, abs(expected)))
        results.append({"case": name, "expected": expected, "actual": actual, "pass": bool(ok)})

    r = value(_SIMPLE)

    # Revenue compounds at the stated growth rate.
    check("year 5 revenue compounds", r["forecast"][4]["revenue"], 1000 * 1.1 ** 5)
    # Reinvestment is the revenue change divided by sales-to-capital.
    y1 = r["forecast"][0]
    check("year 1 reinvestment", y1["reinvestment"], 100.0 / 2.0)
    check("year 1 after-tax EBIT", y1["ebit_after_tax"], 1100 * 0.10 * 0.75)
    check("year 1 FCFF", y1["fcff"], 1100 * 0.10 * 0.75 - 50.0)
    check("year 1 discount factor", y1["cumulative_discount_factor"], 1 / 1.10)

    # Terminal reinvestment rate is growth over return on capital.
    check("terminal reinvestment rate", r["terminal"]["reinvestment_rate"], 0.02 / 0.12)
    tv = r["terminal"]["fcff"] / (0.08 - 0.02)
    check("terminal value formula", r["terminal"]["terminal_value"], tv)

    # The bridge arithmetic must tie out.
    b = r["bridge"]
    check("equity value bridge",
          b["equity_value"], r["value_of_operating_assets"] - 200.0 + 100.0)
    check("value per share", r["value_per_share"], b["equity_in_common_stock"] / 100.0)

    # With no failure probability, operating assets equal the going-concern value.
    check("no failure adjustment by default",
          r["value_of_operating_assets"], r["going_concern_value"])

    # A failure branch must reduce value.
    risky = copy.deepcopy(_SIMPLE)
    risky["failure"] = {"probability": 0.3, "proceeds_basis": "going_concern",
                        "proceeds_percent": 0.5}
    r2 = value(risky)
    results.append({"case": "failure probability lowers value", "expected": True,
                    "actual": r2["value_per_share"] < r["value_per_share"],
                    "pass": r2["value_per_share"] < r["value_per_share"]})
    check("failure adjustment is a probability weighting",
          r2["value_of_operating_assets"],
          r["going_concern_value"] * 0.7 + r["going_concern_value"] * 0.5 * 0.3)

    # Losses carried forward shelter later income.
    loss = copy.deepcopy(_SIMPLE)
    loss["net_operating_loss_carryforward"] = 1000.0
    rl = value(loss)
    check("NOL shelters year 1 taxes", rl["forecast"][0]["taxes"], 0.0)
    results.append({"case": "NOL raises value", "expected": True,
                    "actual": rl["value_per_share"] > r["value_per_share"],
                    "pass": rl["value_per_share"] > r["value_per_share"]})

    # A glide path must start and end where it is told to.
    glide = _expand({"start": 0.20, "end": 0.02, "converge_by": 5}, 5, "t")
    check("glide path reaches its end value", glide[4], 0.02)
    results.append({"case": "glide path descends monotonically", "expected": True,
                    "actual": True,
                    "pass": all(glide[i] >= glide[i + 1] for i in range(4))})

    # Terminal growth above the discount rate must be refused, not silently valued.
    bad = copy.deepcopy(_SIMPLE)
    bad["terminal"] = {"growth_rate": 0.09, "cost_of_capital": 0.08, "return_on_capital": 0.12}
    try:
        value(bad)
        refused = False
    except SystemExit:
        refused = True
    results.append({"case": "terminal growth above discount rate is refused",
                    "expected": True, "actual": refused, "pass": refused})

    # Impossible terminal reinvestment must be refused too.
    bad2 = copy.deepcopy(_SIMPLE)
    bad2["terminal"] = {"growth_rate": 0.06, "cost_of_capital": 0.08, "return_on_capital": 0.04}
    try:
        value(bad2)
        refused2 = False
    except SystemExit:
        refused2 = True
    results.append({"case": "terminal reinvestment above 100% is refused",
                    "expected": True, "actual": refused2, "pass": refused2})

    # The implied solver must invert the engine.
    target = r["value_per_share"]
    inv = implied({"base_case": _SIMPLE, "path": "operating_margin",
                   "target_value_per_share": target, "low": 0.01, "high": 0.30})
    check("implied solver recovers the base margin", inv["implied_value"], 0.10, 1e-4)

    # Sensitivity must bracket the base case.
    s = sensitivity(EXAMPLES["sensitivity"])
    results.append({"case": "sensitivity brackets the base case", "expected": True,
                    "actual": True,
                    "pass": s["range"]["min"] <= s["range"]["base"] <= s["range"]["max"]})

    failed = [x for x in results if not x["pass"]]
    _emit({"total": len(results), "passed": len(results) - len(failed),
           "failed": len(failed), "results": results})
    return 1 if failed else 0


COMMANDS = {"value": cmd_value, "sensitivity": cmd_sensitivity, "implied": cmd_implied,
            "selftest": cmd_selftest}


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=sorted(COMMANDS))
    parser.add_argument("--in", dest="in_file", help="JSON input file (default: stdin)")
    parser.add_argument("--example", action="store_true",
                        help="print a sample input payload for this subcommand and exit")
    args = parser.parse_args()
    if args.example:
        if args.command not in EXAMPLES:
            raise SystemExit("No example payload for %s." % args.command)
        _emit(EXAMPLES[args.command])
        return 0
    return COMMANDS[args.command](args) or 0


if __name__ == "__main__":
    sys.exit(main())

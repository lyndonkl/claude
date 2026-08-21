#!/usr/bin/env python3
"""
multiples.py — the relative valuation (pricing) engine.

Relative valuation prices an asset off what the market pays for similar assets. This
script runs the arithmetic of that process: building multiples that pass the
claimholder-consistency test, describing their distribution across a peer set,
deriving the intrinsic multiple a DCF implies, and controlling for fundamental
differences with an ordinary-least-squares regression fitted here in pure Python.

The script computes. It never picks the comparable set, never decides whether a
residual is mispricing, and never converts a relative verdict into an absolute one.

Pure standard library. No third-party packages, ever — this must run anywhere.

SUBCOMMANDS
  multiples    financials -> traded multiples, with inconsistent pairings refused
  peer-stats   a column of peer multiples -> median, quartiles, skew, drop-out count
  locate       one multiple -> where it sits in a bundled market distribution
  intrinsic    DCF fundamentals -> the justified (intrinsic) multiple
  regress      a sector or market sample -> OLS coefficients, R-squared, SEs, t-stats
  predict      a fitted or published equation -> predicted multiple and over/under
  sum-of-parts divisions and their multiples -> per-division values, total, gap to market
  cross-holdings stakes in other firms -> what to add, what to subtract, and at what value
  selftest     run the bundled worked examples and report pass/fail

Each subcommand reads a JSON payload (--in FILE, or stdin) and writes JSON to stdout.
Run any subcommand with --example to print a sample input payload.
"""

import argparse
import json
import math
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Damodaran's reading of a regression t-statistic: above 2 the variable is doing real
# work, 1 to 2 is marginal, below 1 is noise and the variable should be dropped.
T_SIGNIFICANT = 2.0
T_MARGINAL = 1.0

# A sector sample of 15-30 firms cannot support many predictors. Ten observations per
# estimated coefficient is the working floor below which the fit is over-determined.
MIN_OBS_PER_COEFFICIENT = 10

# Below this many observations the coefficients are fragile enough that the source
# treats the regression as illustrative rather than usable on its own.
SMALL_SAMPLE_N = 30

# Pairwise predictor correlation above this makes individual coefficients unreliable
# and is the usual explanation for a wrong-sign coefficient. Growth and risk, and
# growth and payout, routinely breach it.
COLLINEARITY_THRESHOLD = 0.5

# An R-squared under about 15% means the sample is not priced on the stated
# fundamentals; the prediction is weak evidence rather than an estimate.
WEAK_FIT_R2 = 0.15

# Gaussian elimination pivots are rejected below this magnitude. A pivot this small
# means the design matrix is effectively singular (a duplicated or constant column),
# which is a data problem the caller has to fix.
SINGULAR_PIVOT = 1e-12


# --------------------------------------------------------------------------- helpers

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


def _load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(
            "Bundled reference file %s is missing from %s. Reinstall the skill or pass "
            "your own table with the 'path' field." % (filename, DATA_DIR)
        )


def _percentile(sorted_values, pct):
    """Linear-interpolation percentile on an already-sorted list.

    Uses the inclusive convention (the same one behind Excel's PERCENTILE and numpy's
    default): rank = pct * (n - 1), interpolating between the two neighbouring order
    statistics. Stated explicitly because percentile conventions differ by a fraction
    of an observation and multiple distributions are steep in the tails.
    """
    if not sorted_values:
        return None
    if len(sorted_values) == 1:
        return sorted_values[0]
    rank = pct * (len(sorted_values) - 1)
    low = int(math.floor(rank))
    high = int(math.ceil(rank))
    if low == high:
        return sorted_values[low]
    return sorted_values[low] + (rank - low) * (sorted_values[high] - sorted_values[low])


def _number(payload, key):
    v = payload.get(key)
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        raise SystemExit(
            "Field %r must be a number, got %r. Remove the field rather than passing "
            "a placeholder string." % (key, v)
        )


# ============================================================ STEP 1: DEFINITIONAL

# Every denominator is classified by the claimholders it belongs to. `equity` measures
# are after debt service; `operating` measures belong to all capital providers. The
# consistency rule is that the numerator's claimholders must match the denominator's.
DENOMINATORS = {
    "net_income": {"claim": "equity", "label": "Net income"},
    "eps": {"claim": "equity", "label": "Earnings per share"},
    "book_equity": {"claim": "equity", "label": "Book value of equity"},
    "book_value_per_share": {"claim": "equity", "label": "Book value per share"},
    "dividends": {"claim": "equity", "label": "Dividends"},
    "fcfe": {"claim": "equity", "label": "Free cash flow to equity"},
    "ebitda": {"claim": "operating", "label": "EBITDA"},
    "ebit": {"claim": "operating", "label": "EBIT"},
    "after_tax_ebit": {"claim": "operating", "label": "After-tax EBIT"},
    "fcff": {"claim": "operating", "label": "Free cash flow to the firm"},
    "invested_capital": {"claim": "operating", "label": "Invested capital"},
    # Revenue is generated by the operating assets, but pairing it with a price
    # numerator is long-established practice. It is tolerated on the condition that the
    # companion variable switches from the operating margin to the net margin.
    "revenue": {"claim": "either", "label": "Revenue"},
}

NUMERATORS = {
    "equity": "Market value of equity",
    "firm": "Market value of equity + market value of debt",
    "enterprise": "Market value of equity + market value of debt - cash + minority interests",
}

MULTIPLE_SPECS = {
    "PE": {"num": "equity", "den": "net_income", "per_share": ("price_per_share", "eps"),
           "companion": "expected growth in EPS (with payout and cost of equity as controls)"},
    "PBV": {"num": "equity", "den": "book_equity",
            "per_share": ("price_per_share", "book_value_per_share"),
            "companion": "return on equity"},
    "P/S": {"num": "equity", "den": "revenue", "per_share": None,
            "companion": "net margin"},
    "EV/EBITDA": {"num": "enterprise", "den": "ebitda", "per_share": None,
                  "companion": "reinvestment needs (CapEx/EBITDA), tax rate, cost of capital"},
    "EV/EBIT": {"num": "enterprise", "den": "ebit", "per_share": None,
                "companion": "reinvestment rate and tax rate"},
    "EV/Sales": {"num": "enterprise", "den": "revenue", "per_share": None,
                 "companion": "after-tax operating margin"},
    "EV/IC": {"num": "enterprise", "den": "invested_capital", "per_share": None,
              "companion": "return on invested capital"},
    "EV/FCFF": {"num": "enterprise", "den": "fcff", "per_share": None,
                "companion": "cost of capital and growth"},
}

# Aliases the caller is likely to type, including the pairings that fail the
# consistency test. Naming them explicitly lets the refusal say what is wrong instead
# of reporting an unknown multiple.
ALIASES = {
    "P/E": "PE", "PRICE/EARNINGS": "PE", "TRAILING PE": "PE", "FORWARD PE": "PE",
    "P/BV": "PBV", "PRICE/BOOK": "PBV", "PRICE TO BOOK": "PBV",
    "PS": "P/S", "PRICE/SALES": "P/S", "PRICE TO SALES": "P/S",
    "EV/REVENUE": "EV/Sales", "EV/REVENUES": "EV/Sales",
    "EV/INVESTED CAPITAL": "EV/IC", "EV/BOOK CAPITAL": "EV/IC",
    "TEV/EBITDA": "EV/EBITDA",
}


def _canonical(name):
    if name in MULTIPLE_SPECS:
        return name
    return ALIASES.get(name.strip().upper(), name)


def check_consistency(numerator_class, denominator_key):
    """Apply Damodaran's Proposition 1: the numerator and denominator must belong to
    the same claimholders.

    Returns (ok, explanation). An equity numerator over an operating denominator is the
    classic error (Price/EBITDA); an enterprise numerator over an equity denominator is
    the same error inverted (EV/Net Income).
    """
    if denominator_key not in DENOMINATORS:
        return False, ("%r is not a recognised denominator. Known denominators: %s."
                       % (denominator_key, ", ".join(sorted(DENOMINATORS))))
    claim = DENOMINATORS[denominator_key]["claim"]
    label = DENOMINATORS[denominator_key]["label"]
    if claim == "either":
        return True, ("%s sits above the capital structure, so it pairs with either "
                      "numerator. Match the companion margin to the numerator: net "
                      "margin with a price numerator, operating margin with an "
                      "enterprise numerator." % label)
    if numerator_class == "equity" and claim == "equity":
        return True, "Equity numerator with an equity denominator."
    if numerator_class in ("firm", "enterprise") and claim == "operating":
        return True, "Firm-level numerator with an operating denominator."
    if numerator_class == "equity" and claim == "operating":
        return False, (
            "%s belongs to all capital providers, but the numerator is only the equity "
            "claim. The multiple would divide part of the value by all of the income. "
            "Use an enterprise numerator with %s, or switch the denominator to net "
            "income or book equity." % (label, label))
    return False, (
        "%s belongs to equity holders only, but the numerator includes debt. The "
        "multiple would divide all of the value by part of the income. Use a market "
        "value of equity numerator with %s, or switch the denominator to EBITDA, EBIT, "
        "revenue or invested capital." % (label, label))


def build_numerators(p):
    """Market value of equity, firm value and enterprise value from the payload."""
    equity = _number(p, "market_cap")
    if equity is None:
        price = _number(p, "price_per_share")
        shares = _number(p, "shares_outstanding")
        if price is not None and shares is not None:
            equity = price * shares
    debt = _number(p, "debt") or 0.0
    cash = _number(p, "cash") or 0.0
    # Consolidating a partly-owned subsidiary puts all of its EBITDA in the denominator
    # while the parent owns only part of the equity. Adding minority interests to the
    # numerator restores the match.
    minority = _number(p, "minority_interests") or 0.0
    out = {"market_value_of_equity": equity, "debt": debt, "cash": cash,
           "minority_interests": minority}
    if equity is not None:
        out["firm_value"] = equity + debt
        # Cash comes out because interest income on it appears in neither EBITDA nor
        # EBIT; leaving it in the numerator prices an asset whose income is excluded.
        out["enterprise_value"] = equity + debt - cash + minority
    return out


def compute_multiples(p):
    nums = build_numerators(p)
    equity = nums.get("market_value_of_equity")
    if equity is None:
        raise SystemExit(
            "No equity value. Pass market_cap, or price_per_share together with "
            "shares_outstanding."
        )
    numerator_values = {"equity": equity, "firm": nums.get("firm_value"),
                        "enterprise": nums.get("enterprise_value")}

    requested = p.get("multiples") or list(MULTIPLE_SPECS)
    results = []
    for raw in requested:
        results.append(_one_multiple(_canonical(raw), raw, p, numerator_values))

    for custom in p.get("custom") or []:
        results.append(_custom_multiple(custom, p, numerator_values))

    computed = [r for r in results if r["status"] == "computed"]
    refused = [r for r in results if r["status"] != "computed"]
    return {
        "name": p.get("name"),
        "numerators": nums,
        "results": results,
        "computed_count": len(computed),
        "refused_count": len(refused),
        "note": ("A refused multiple is not a failure of the script. It records that the "
                 "firm drops out of that multiple's sample, which biases any peer "
                 "statistic computed without it."),
    }


def _one_multiple(key, requested_as, p, numerator_values):
    spec = MULTIPLE_SPECS.get(key)
    if spec is None:
        return {"multiple": requested_as, "status": "unknown",
                "reason": ("Not a recognised multiple. Known: %s. For an arbitrary "
                           "pairing use the 'custom' field."
                           % ", ".join(sorted(MULTIPLE_SPECS)))}
    ok, why = check_consistency(spec["num"], spec["den"])
    if not ok:
        return {"multiple": key, "status": "refused", "reason": why}

    numerator = numerator_values.get(spec["num"])
    denominator = _number(p, spec["den"])
    num_label = NUMERATORS[spec["num"]]
    den_label = DENOMINATORS[spec["den"]]["label"]
    basis = "aggregate"

    if denominator is None and spec["per_share"]:
        pn, pd = spec["per_share"]
        numerator = _number(p, pn)
        denominator = _number(p, pd)
        num_label, den_label, basis = "Price per share", DENOMINATORS[pd]["label"], "per share"

    if numerator is None or denominator is None:
        missing = spec["den"] if denominator is None else spec["num"]
        return {"multiple": key, "status": "missing_input",
                "reason": "Needs %s; it was not supplied." % missing}

    refusal = _reject_bad_ratio(key, numerator, denominator, num_label, den_label)
    if refusal:
        return refusal

    return {"multiple": key, "status": "computed", "value": numerator / denominator,
            "numerator": num_label, "numerator_value": numerator,
            "denominator": den_label, "denominator_value": denominator,
            "claimholder_class": spec["num"], "basis": basis,
            "companion_variable": spec["companion"], "consistency": why}


def _reject_bad_ratio(key, numerator, denominator, num_label, den_label):
    """Refuse ratios whose sign makes them meaningless rather than returning them."""
    if denominator <= 0:
        return {"multiple": key, "status": "refused",
                "reason": ("%s is %.4g. A multiple with a non-positive denominator is "
                           "not a small number or a large one — it carries no ordering "
                           "at all, so it cannot be ranked against peers. The firm drops "
                           "out of this multiple's sample. Price it on a denominator "
                           "that stays positive (revenue, or invested capital), on a "
                           "forward year in which the denominator turns positive, or on "
                           "a sector-specific driver."
                           % (den_label, denominator))}
    if numerator <= 0:
        return {"multiple": key, "status": "refused",
                "reason": ("%s is %.4g. A non-positive numerator usually means cash "
                           "exceeds the market value of equity plus debt, so the market "
                           "prices the operating assets at less than nothing. Check the "
                           "cash and debt figures before using any enterprise multiple "
                           "for this firm." % (num_label, numerator))}
    return None


def _custom_multiple(custom, p, numerator_values):
    num_class = custom.get("numerator")
    den_key = custom.get("denominator")
    label = custom.get("name") or "%s/%s" % (num_class, den_key)
    if num_class not in NUMERATORS:
        return {"multiple": label, "status": "unknown",
                "reason": "numerator must be one of: %s." % ", ".join(sorted(NUMERATORS))}
    ok, why = check_consistency(num_class, den_key)
    if not ok:
        return {"multiple": label, "status": "refused", "reason": why}
    numerator = numerator_values.get(num_class)
    denominator = _number(p, den_key)
    if numerator is None or denominator is None:
        return {"multiple": label, "status": "missing_input",
                "reason": "Needs both the numerator inputs and %s." % den_key}
    refusal = _reject_bad_ratio(label, numerator, denominator,
                                NUMERATORS[num_class], DENOMINATORS[den_key]["label"])
    if refusal:
        return refusal
    return {"multiple": label, "status": "computed", "value": numerator / denominator,
            "numerator": NUMERATORS[num_class], "numerator_value": numerator,
            "denominator": DENOMINATORS[den_key]["label"], "denominator_value": denominator,
            "claimholder_class": num_class, "consistency": why}


def cmd_multiples(args):
    _emit(compute_multiples(_read_payload(args)))


# ============================================================= STEP 2: DESCRIPTIVE

def peer_statistics(p):
    """Summary statistics for one multiple across a peer set.

    Firms whose multiple is missing or non-positive are counted separately rather than
    silently dropped, because that drop-out is itself the finding: a PE sample only
    contains firms that made money.
    """
    firms = p.get("firms")
    if firms is None:
        values_in = p.get("values")
        if values_in is None:
            raise SystemExit(
                "Pass either 'firms' (a list of {name, multiple, ...} objects) or "
                "'values' (a plain list of numbers)."
            )
        firms = [{"name": None, "multiple": v} for v in values_in]

    usable, dropped = [], []
    for f in firms:
        v = f.get("multiple")
        if v is None or (isinstance(v, str) and v.strip().upper() in ("NA", "N/A", "")):
            dropped.append({"name": f.get("name"), "reason": "multiple not reported"})
            continue
        v = float(v)
        if v <= 0:
            dropped.append({"name": f.get("name"),
                            "reason": "multiple is non-positive, so the denominator was "
                                      "negative and the firm has no usable multiple"})
            continue
        usable.append({"name": f.get("name"), "multiple": v,
                       "companion": f.get("companion"), "risk": f.get("risk")})

    if not usable:
        raise SystemExit(
            "No firm in the sample has a usable %s. Every denominator was missing or "
            "non-positive. Switch to a multiple whose denominator stays positive."
            % (p.get("multiple") or "multiple")
        )

    vals = sorted(x["multiple"] for x in usable)
    n = len(vals)
    mean = sum(vals) / n
    median = _percentile(vals, 0.50)
    universe = int(p.get("universe_size") or len(firms))
    stats = {
        "multiple": p.get("multiple"),
        "universe_size": universe,
        "firms_with_a_usable_multiple": n,
        "firms_dropped": len(dropped),
        "share_of_universe_priced": n / universe if universe else None,
        "mean": mean, "median": median,
        "p10": _percentile(vals, 0.10), "p25": _percentile(vals, 0.25),
        "p75": _percentile(vals, 0.75), "p90": _percentile(vals, 0.90),
        "minimum": vals[0], "maximum": vals[-1],
        "mean_over_median": mean / median if median else None,
        "dropped_firms": dropped,
    }
    stats["skew_note"] = _skew_note(stats["mean_over_median"])
    stats["use"] = ("Use the median or a percentile band as 'typical'. The mean of a "
                    "multiple is bounded below at zero and unbounded above, so a handful "
                    "of firms on the right tail drag it away from anything typical.")
    if stats["share_of_universe_priced"] is not None and stats["share_of_universe_priced"] < 1:
        stats["truncation_note"] = (
            "%d of %d firms have no usable multiple. Conclusions drawn from this sample "
            "describe the surviving subsample, not the universe."
            % (len(dropped), universe))

    subject = p.get("subject")
    if subject:
        stats["median_test"] = _median_test(subject, usable, stats)
    return stats


def _skew_note(ratio):
    if ratio is None:
        return None
    if ratio >= 1.5:
        return ("Mean is %.2fx the median. The distribution is heavily right-skewed; the "
                "mean is not a usable comparison point." % ratio)
    if ratio >= 1.15:
        return ("Mean is %.2fx the median. Visible right skew — prefer the median." % ratio)
    return ("Mean and median are within %.0f%% of each other, which is unusual for a "
            "multiple. Check that outliers were not already trimmed out; one-sided "
            "trimming biases the typical multiple downward." % (abs(ratio - 1) * 100))


def _median_test(subject, usable, stats):
    """The quick screen: cheap needs a low multiple with a high companion variable and
    below-median risk. It treats each variable independently, so it runs out as soon as
    firms differ on more than one dimension.
    """
    companions = sorted(x["companion"] for x in usable if x.get("companion") is not None)
    risks = sorted(x["risk"] for x in usable if x.get("risk") is not None)
    med_companion = _percentile(companions, 0.50) if companions else None
    med_risk = _percentile(risks, 0.50) if risks else None
    m, c, r = subject.get("multiple"), subject.get("companion"), subject.get("risk")
    out = {"subject": subject.get("name"), "sector_median_multiple": stats["median"],
           "sector_median_companion": med_companion, "sector_median_risk": med_risk}
    if m is None or c is None or med_companion is None:
        out["verdict"] = "inconclusive"
        out["reason"] = "Needs the subject's multiple and companion variable, and a " \
                        "companion variable for the peers."
        return out
    cheap = m < stats["median"] and c > med_companion and (
        med_risk is None or r is None or r < med_risk)
    expensive = m > stats["median"] and c < med_companion
    out["verdict"] = "undervalued screen" if cheap else (
        "overvalued screen" if expensive else "screen does not fire")
    out["caution"] = ("A screen, not a verdict. It ignores the size of each gap and the "
                      "correlation between the variables. Escalate to a regression once "
                      "more than one fundamental differs.")
    return out


def cmd_peer_stats(args):
    _emit(peer_statistics(_read_payload(args)))


def locate(p):
    """Place one multiple inside a bundled cross-sectional distribution."""
    tables = _load_data("multiple_distributions.json")
    key = p.get("table")
    if key not in tables["tables"]:
        raise SystemExit(
            "Unknown table %r. Available: %s." % (key, ", ".join(sorted(tables["tables"]))))
    table = tables["tables"][key]
    value = _number(p, "value")
    if value is None:
        raise SystemExit("Pass the multiple to locate as 'value'.")

    out = {"table": key, "description": table["description"], "as_of": tables["as_of"],
           "value": value, "source": tables["source"], "refresh": tables["refresh"]}

    if table["kind"] == "percentiles":
        points = table["points"]
        out["distribution"] = points
        out["placement"] = _bracket(value, points)
        if table.get("share_with_positive_multiple") is not None:
            out["share_with_positive_multiple"] = table["share_with_positive_multiple"]
            out["truncation_note"] = table.get("truncation_note")
    else:
        groups = table["groups"]
        rows = []
        for name in sorted(groups):
            med = groups[name]
            rows.append({"group": name, "median": med, "value_over_median": value / med,
                         "reading": "below the median" if value < med else "at or above the median"})
        out["comparison"] = rows
        out["cross_market_warning"] = tables["cross_market_warning"]

    out["threshold_warning"] = tables["threshold_warning"]
    return out


def _bracket(value, points):
    """Report which published percentile band the value falls in.

    Deliberately reports a band rather than an interpolated percentile. The bundled
    tables carry five points; interpolating between them would invent precision the
    source does not have.
    """
    labels = sorted(points, key=lambda k: points[k])
    below = [k for k in labels if points[k] <= value]
    above = [k for k in labels if points[k] > value]
    if not below:
        return "below the %s (%.2f)" % (labels[0], points[labels[0]])
    if not above:
        return "at or above the %s (%.2f)" % (below[-1], points[below[-1]])
    return "between the %s (%.2f) and the %s (%.2f)" % (
        below[-1], points[below[-1]], above[0], points[above[0]])


def cmd_locate(args):
    _emit(locate(_read_payload(args)))


# ============================================================== STEP 3: ANALYTICAL

def _require_spread(rate, growth, rate_label, growth_label):
    if rate <= growth:
        raise SystemExit(
            "%s (%.4f) must exceed %s (%.4f). A stable-growth multiple with a "
            "non-positive spread is infinite or negative, which means the growth rate "
            "is not a stable-growth rate. Cap growth at the riskfree rate."
            % (rate_label, rate, growth_label, growth))


def intrinsic_pe_stable(payout, growth, cost_of_equity, basis="trailing"):
    """PE = payout x (1 + g)/(r - g) on trailing earnings, payout/(r - g) on forward."""
    _require_spread(cost_of_equity, growth, "cost of equity", "stable growth")
    if basis == "forward":
        return payout / (cost_of_equity - growth)
    return payout * (1 + growth) / (cost_of_equity - growth)


def intrinsic_pe_two_stage(payout, growth, years, cost_of_equity, stable_payout,
                           stable_growth):
    """Two-stage intrinsic PE.

    The high-growth term's denominator (r - g) is negative whenever growth exceeds the
    cost of equity, and so is the bracket above it. The term stays positive. That is the
    formula working, not an error, so no spread check applies to the first stage.
    """
    _require_spread(cost_of_equity, stable_growth, "cost of equity", "stable growth")
    ratio = ((1 + growth) ** years) / ((1 + cost_of_equity) ** years)
    if abs(cost_of_equity - growth) < SINGULAR_PIVOT:
        # r == g makes the closed form 0/0; the limit is n discount-adjusted periods.
        high = payout * (1 + growth) * years / (1 + cost_of_equity)
    else:
        high = payout * (1 + growth) * (1 - ratio) / (cost_of_equity - growth)
    terminal = (stable_payout * ((1 + growth) ** years) * (1 + stable_growth)
                / ((cost_of_equity - stable_growth) * (1 + cost_of_equity) ** years))
    return {"intrinsic_pe": high + terminal, "high_growth_term": high,
            "terminal_term": terminal}


def intrinsic_pbv(roe, growth, cost_of_equity, payout=None, basis="forward"):
    """PBV from ROE, growth and the cost of equity.

    Two forms are returned. The long form uses the payout ratio directly. The short form
    (ROE - g)/(r - g) substitutes the sustainable growth relation g = (1 - payout) x ROE.
    On the forward basis the two are algebraically identical when growth is sustainable;
    a gap between them means the inputs are internally inconsistent, which is the
    routine trap this calculation exposes.
    """
    _require_spread(cost_of_equity, growth, "cost of equity", "stable growth")
    out = {"short_form_pbv": (roe - growth) / (cost_of_equity - growth)}
    if payout is not None:
        long_form = (roe * payout / (cost_of_equity - growth) if basis == "forward"
                     else roe * payout * (1 + growth) / (cost_of_equity - growth))
        out["long_form_pbv"] = long_form
        out["basis"] = basis
        sustainable = (1 - payout) * roe
        out["sustainable_growth"] = sustainable
        out["growth_is_consistent"] = abs(sustainable - growth) < 1e-9
        if not out["growth_is_consistent"]:
            out["consistency_warning"] = (
                "Payout %.4f and ROE %.4f imply sustainable growth of %.4f, but growth "
                "was set to %.4f. The two forms will disagree. Reconcile payout, ROE and "
                "growth before quoting either number."
                % (payout, roe, sustainable, growth))
    return out


def intrinsic_ev_ic(roic, growth, wacc):
    """EV/Invested Capital = (ROIC - g)/(WACC - g), the enterprise twin of PBV."""
    _require_spread(wacc, growth, "cost of capital", "stable growth")
    reinvestment_rate = growth / roic if roic else None
    return {"intrinsic_ev_ic": (roic - growth) / (wacc - growth),
            "implied_reinvestment_rate": reinvestment_rate}


def intrinsic_ev_sales(after_tax_operating_margin, reinvestment_rate, growth, wacc):
    """EV/Sales = after-tax operating margin x (1 - RIR)/(WACC - g)."""
    _require_spread(wacc, growth, "cost of capital", "stable growth")
    return {"intrinsic_ev_sales": (after_tax_operating_margin * (1 - reinvestment_rate)
                                   / (wacc - growth))}


def intrinsic_ev_ebit(tax_rate, reinvestment_rate, growth, wacc, after_tax=False):
    """EV/EBIT = (1 - t)(1 - RIR)/(WACC - g); drop the (1 - t) for after-tax EBIT."""
    _require_spread(wacc, growth, "cost of capital", "stable growth")
    base = (1 - reinvestment_rate) / (wacc - growth)
    return {"intrinsic_ev_ebit": base if after_tax else (1 - tax_rate) * base,
            "denominator": "after-tax EBIT" if after_tax else "EBIT"}


def intrinsic_ev_ebitda(tax_rate, depreciation_over_ebitda, capex_over_ebitda,
                        wc_change_over_ebitda, wacc, growth):
    """EV/EBITDA broken into its four terms.

    EBITDA is cash flow before the capital spending that keeps the assets running, so
    the reinvestment term is what separates a cheap multiple from a deserved one.
    """
    _require_spread(wacc, growth, "cost of capital", "stable growth")
    spread = wacc - growth
    after_tax = (1 - tax_rate) / spread
    shield = (depreciation_over_ebitda * tax_rate) / spread
    capex = capex_over_ebitda / spread
    wc = wc_change_over_ebitda / spread
    total = after_tax + shield - capex - wc
    out = {"intrinsic_ev_ebitda": total,
           "terms": {"after_tax_operating_cash_flow": after_tax,
                     "depreciation_tax_shield": shield,
                     "capital_expenditure": -capex,
                     "working_capital": -wc}}
    if total <= 0:
        out["warning"] = ("Reinvestment needs exhaust the cash flow, so the fundamentals "
                          "justify no positive multiple. Check whether current CapEx is "
                          "representative of steady-state needs before reporting this.")
    return out


def intrinsic_ps(net_margin, payout, growth, cost_of_equity, basis="forward"):
    """Price/Sales = net margin x payout/(ke - g) on next year's sales."""
    _require_spread(cost_of_equity, growth, "cost of equity", "stable growth")
    factor = payout if basis == "forward" else payout * (1 + growth)
    return {"intrinsic_ps": net_margin * factor / (cost_of_equity - growth)}


COMPANION_MAP = {
    "PE": "expected growth", "PEG": "risk, payout and the level of growth",
    "PBV": "return on equity", "P/S": "net margin",
    "EV/EBITDA": "reinvestment needs, tax rate", "EV/EBIT": "reinvestment rate, tax rate",
    "EV/Sales": "after-tax operating margin", "EV/IC": "return on invested capital",
}


def intrinsic(p):
    key = _canonical(p.get("multiple", "PE"))
    model = p.get("model", "stable")
    out = {"multiple": key, "model": model, "companion_variable": COMPANION_MAP.get(key)}

    if key == "PE":
        if model == "two_stage":
            r = intrinsic_pe_two_stage(
                p["payout"], p["growth"], int(p["years"]), p["cost_of_equity"],
                p.get("stable_payout", p["payout"]), p["stable_growth"])
            out.update(r)
        else:
            out["intrinsic_pe"] = intrinsic_pe_stable(
                p["payout"], p["growth"], p["cost_of_equity"], p.get("basis", "trailing"))
            out["basis"] = p.get("basis", "trailing")
    elif key == "PEG":
        if model == "two_stage":
            r = intrinsic_pe_two_stage(
                p["payout"], p["growth"], int(p["years"]), p["cost_of_equity"],
                p.get("stable_payout", p["payout"]), p["stable_growth"])
            pe = r["intrinsic_pe"]
        else:
            pe = intrinsic_pe_stable(p["payout"], p["growth"], p["cost_of_equity"],
                                     p.get("basis", "trailing"))
        if p["growth"] <= 0:
            raise SystemExit(
                "PEG needs a positive expected growth rate. With zero or negative growth "
                "the ratio is undefined or negative, and PEG is the wrong multiple.")
        # By convention PEG divides by growth in percentage points, so 25% growth
        # divides by 25 rather than by 0.25.
        out["intrinsic_pe"] = pe
        out["intrinsic_peg"] = pe / (p["growth"] * 100.0)
        out["caution"] = ("PEG does not neutralise growth. It falls with risk and with the "
                          "level of growth, so a low PEG often marks the riskiest or the "
                          "fastest-growing firm rather than the cheapest.")
    elif key == "PBV":
        out.update(intrinsic_pbv(p["roe"], p["growth"], p["cost_of_equity"],
                                 p.get("payout"), p.get("basis", "forward")))
    elif key == "EV/IC":
        out.update(intrinsic_ev_ic(p["roic"], p["growth"], p["wacc"]))
    elif key == "EV/Sales":
        out.update(intrinsic_ev_sales(p["after_tax_operating_margin"],
                                      p["reinvestment_rate"], p["growth"], p["wacc"]))
    elif key == "EV/EBIT":
        out.update(intrinsic_ev_ebit(p["tax_rate"], p["reinvestment_rate"], p["growth"],
                                     p["wacc"], p.get("after_tax", False)))
    elif key == "EV/EBITDA":
        out.update(intrinsic_ev_ebitda(
            p["tax_rate"], p.get("depreciation_over_ebitda", 0.0),
            p.get("capex_over_ebitda", 0.0), p.get("wc_change_over_ebitda", 0.0),
            p["wacc"], p["growth"]))
    elif key == "P/S":
        out.update(intrinsic_ps(p["net_margin"], p["payout"], p["growth"],
                                p["cost_of_equity"], p.get("basis", "forward")))
    else:
        raise SystemExit(
            "No intrinsic form for %r. Supported: PE, PEG, PBV, P/S, EV/EBITDA, EV/EBIT, "
            "EV/Sales, EV/IC." % key)

    actual = p.get("actual_multiple")
    if actual is not None:
        justified = next((out[k] for k in ("intrinsic_peg", "intrinsic_pe", "short_form_pbv",
                                           "intrinsic_ev_ic", "intrinsic_ev_sales",
                                           "intrinsic_ev_ebit", "intrinsic_ev_ebitda",
                                           "intrinsic_ps") if k in out), None)
        if justified and justified > 0:
            out["actual_multiple"] = actual
            out["actual_over_intrinsic"] = actual / justified - 1
            out["reading"] = ("trades below the multiple its own fundamentals justify"
                              if actual < justified else
                              "trades above the multiple its own fundamentals justify")
    return out


def cmd_intrinsic(args):
    _emit(intrinsic(_read_payload(args)))


# ============================================================= STEP 4: APPLICATION

def _solve_and_invert(a):
    """Gauss-Jordan elimination with partial pivoting.

    Returns (solution, inverse) for the augmented system [A | b | I]. The inverse is
    needed because the standard errors are the square roots of the diagonal of
    sigma-squared times (X'X) inverse; there is no shortcut that avoids it.
    """
    k = len(a)
    m = [row[:] for row in a]
    for col in range(k):
        pivot_row = max(range(col, k), key=lambda r: abs(m[r][col]))
        if abs(m[pivot_row][col]) < SINGULAR_PIVOT:
            raise SystemExit(
                "The predictor matrix is singular: two columns are identical, one is "
                "constant, or there are fewer observations than coefficients. Drop the "
                "duplicated predictor and re-run."
            )
        m[col], m[pivot_row] = m[pivot_row], m[col]
        pivot = m[col][col]
        m[col] = [v / pivot for v in m[col]]
        for r in range(k):
            if r != col and m[r][col] != 0.0:
                factor = m[r][col]
                m[r] = [m[r][j] - factor * m[col][j] for j in range(len(m[r]))]
    solution = [m[i][k] for i in range(k)]
    inverse = [[m[i][k + 1 + j] for j in range(k)] for i in range(k)]
    return solution, inverse


def ols(rows, y, names, has_intercept):
    """Ordinary least squares by the normal equations, X'X b = X'y.

    Fine for the sample sizes relative valuation deals with (tens to thousands of firms
    and a handful of predictors). The normal equations lose precision when predictors
    are on wildly different scales, which is one more reason to enter growth, payout,
    margins and returns as decimals.
    """
    n = len(rows)
    k = len(rows[0])
    if n <= k:
        raise SystemExit(
            "%d observations cannot support %d coefficients. Add firms or drop "
            "predictors." % (n, k))
    xtx = [[sum(rows[i][a] * rows[i][b] for i in range(n)) for b in range(k)]
           for a in range(k)]
    xty = [sum(rows[i][a] * y[i] for i in range(n)) for a in range(k)]
    augmented = [xtx[a] + [xty[a]] + [1.0 if j == a else 0.0 for j in range(k)]
                 for a in range(k)]
    beta, inverse = _solve_and_invert(augmented)

    fitted = [sum(beta[a] * rows[i][a] for a in range(k)) for i in range(n)]
    residuals = [y[i] - fitted[i] for i in range(n)]
    sse = sum(e * e for e in residuals)
    y_mean = sum(y) / n
    # Without an intercept the residuals need not sum to zero, so R-squared is measured
    # against zero rather than the mean. Reporting the mean-centred version there would
    # overstate the fit, sometimes making it negative.
    sst = sum((v - y_mean) ** 2 for v in y) if has_intercept else sum(v * v for v in y)
    r_squared = 1 - sse / sst if sst > 0 else None
    dof = n - k
    sigma_squared = sse / dof
    std_errors = [math.sqrt(sigma_squared * inverse[a][a]) for a in range(k)]
    t_stats = [beta[a] / std_errors[a] if std_errors[a] > 0 else None for a in range(k)]
    adjusted = (1 - (sse / dof) / (sst / (n - 1 if has_intercept else n))
                if sst > 0 else None)
    return {
        "n": n, "coefficient_count": k, "degrees_of_freedom": dof,
        "coefficients": [
            {"name": names[a], "coefficient": beta[a], "std_error": std_errors[a],
             "t_statistic": t_stats[a], "reading": _t_reading(t_stats[a])}
            for a in range(k)],
        "r_squared": r_squared, "adjusted_r_squared": adjusted,
        "standard_error_of_regression": math.sqrt(sigma_squared),
        "fitted": fitted, "residuals": residuals,
        "sum_of_residuals": sum(residuals),
    }


def _t_reading(t):
    if t is None:
        return "undefined"
    a = abs(t)
    if a > T_SIGNIFICANT:
        return "significant"
    if a >= T_MARGINAL:
        return "marginal"
    return "noise — drop this predictor and re-run"


def _correlation(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0 or syy <= 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def _design(observations, dependent, predictors, log_predictors, has_intercept):
    """Build the design matrix, dropping observations that cannot be used."""
    rows, y, kept, skipped = [], [], [], []
    for obs in observations:
        dep = obs.get(dependent)
        if dep is None:
            skipped.append({"name": obs.get("name"),
                            "reason": "no %s reported" % dependent})
            continue
        row = [1.0] if has_intercept else []
        bad = None
        for name in predictors:
            v = obs.get(name)
            if v is None:
                bad = "no %s reported" % name
                break
            v = float(v)
            if name in log_predictors:
                if v <= 0:
                    bad = ("%s is %.4g; its natural log is undefined. Firms with "
                           "non-positive %s cannot enter a log specification."
                           % (name, v, name))
                    break
                v = math.log(v)
            row.append(v)
        if bad:
            skipped.append({"name": obs.get("name"), "reason": bad})
            continue
        rows.append(row)
        y.append(float(dep))
        kept.append(obs.get("name"))
    return rows, y, kept, skipped


def regress(p):
    dependent = p.get("dependent")
    predictors = p.get("predictors")
    observations = p.get("observations")
    if not dependent or not predictors or not observations:
        raise SystemExit(
            "regress needs 'dependent' (the multiple's field name), 'predictors' (a list "
            "of field names) and 'observations' (a list of objects carrying both)."
        )
    has_intercept = bool(p.get("intercept", True))
    log_predictors = set(p.get("log_predictors") or [])
    scope = p.get("scope", "sector")

    rows, y, kept, skipped = _design(observations, dependent, predictors,
                                     log_predictors, has_intercept)
    if not rows:
        raise SystemExit(
            "No observation carried every field. Check that %r and %s are present and "
            "spelled the same way in every object."
            % (dependent, ", ".join(repr(x) for x in predictors)))

    names = (["intercept"] if has_intercept else []) + [
        "ln(%s)" % x if x in log_predictors else x for x in predictors]
    fit = ols(rows, y, names, has_intercept)
    fit["dependent"] = dependent
    fit["scope"] = scope
    fit["firms_used"] = kept
    fit["firms_skipped"] = skipped
    fit["equation"] = _equation_string(dependent, fit["coefficients"])
    fit["equation_coefficients"] = {c["name"]: c["coefficient"] for c in fit["coefficients"]}

    offset = 1 if has_intercept else 0
    pairs = []
    for i in range(len(predictors)):
        for j in range(i + 1, len(predictors)):
            col_i = [r[offset + i] for r in rows]
            col_j = [r[offset + j] for r in rows]
            pairs.append({"pair": [names[offset + i], names[offset + j]],
                          "correlation": _correlation(col_i, col_j)})
    fit["predictor_correlations"] = pairs
    regions = sorted({o["region"] for o in observations if o.get("region")})
    if len(regions) > 1:
        fit["regions_pooled"] = regions
    fit["warnings"] = _regression_warnings(fit, pairs, scope, len(skipped), regions)
    return fit


def _equation_string(dependent, coefficients):
    parts = []
    for c in coefficients:
        if c["name"] == "intercept":
            parts.append("%.4f" % c["coefficient"])
        else:
            sign = "-" if c["coefficient"] < 0 else "+"
            parts.append("%s %.4f x %s" % (sign, abs(c["coefficient"]), c["name"]))
    body = " ".join(parts)
    if body.startswith("+ "):
        body = body[2:]
    return "%s = %s" % (dependent, body)


def _regression_warnings(fit, pairs, scope, skipped_count, regions):
    warnings = []
    intercept = next((c for c in fit["coefficients"] if c["name"] == "intercept"), None)
    if intercept and intercept["coefficient"] < 0:
        warnings.append(
            "The intercept is %.4f. A negative intercept lets the equation return a "
            "negative predicted multiple for a firm with low fundamentals, which is "
            "meaningless. Re-run with \"intercept\": false to fit through the origin, "
            "and treat that as an imperfect fix rather than a repair."
            % intercept["coefficient"])
    for c in fit["coefficients"]:
        if c["name"] != "intercept" and c["reading"] == "noise — drop this predictor and re-run":
            warnings.append(
                "%s has t = %.2f. In pricing the market decides what matters, so drop it "
                "and re-run. Explanatory power rarely suffers."
                % (c["name"], c["t_statistic"]))
    for pair in pairs:
        r = pair["correlation"]
        if r is not None and abs(r) > COLLINEARITY_THRESHOLD:
            warnings.append(
                "%s and %s correlate at %.2f. Multicollinearity makes the individual "
                "coefficients unstable and can flip their signs; a wrong-sign coefficient "
                "here is an artefact, not a finding."
                % (pair["pair"][0], pair["pair"][1], r))
    if fit["n"] < MIN_OBS_PER_COEFFICIENT * fit["coefficient_count"]:
        warnings.append(
            "%d observations for %d coefficients is below the %d-per-coefficient floor. "
            "Cut the specification or widen the sample."
            % (fit["n"], fit["coefficient_count"], MIN_OBS_PER_COEFFICIENT))
    if fit["n"] < SMALL_SAMPLE_N:
        warnings.append(
            "Small sample (%d firms). Coefficients from a sector this size move sharply "
            "year to year; re-estimate every period rather than reusing this fit."
            % fit["n"])
    if fit["r_squared"] is not None and fit["r_squared"] < WEAK_FIT_R2:
        warnings.append(
            "R-squared is %.3f. The sample is not priced on these fundamentals, so the "
            "predicted multiple is weak evidence. Say so rather than pushing it."
            % fit["r_squared"])
    if skipped_count:
        warnings.append(
            "%d observation(s) were dropped for missing or non-positive fields. The fit "
            "describes the firms that survived that filter." % skipped_count)
    if scope == "market":
        warnings.append(
            "A market-wide fit prices the firm against the whole market rather than a "
            "peer group. The two can disagree, because the peer group may itself be "
            "mispriced against the market. State which benchmark the verdict uses.")
    if len(regions) > 1:
        warnings.append(
            "The sample pools %d markets (%s). Interest rates, real growth and country "
            "risk differ across them, so a single fitted line attributes those "
            "differences to the firm-level predictors. Add region dummies, or fit each "
            "market separately." % (len(regions), ", ".join(regions)))
    return warnings


def cmd_regress(args):
    _emit(regress(_read_payload(args)))


def _published(key):
    library = _load_data("published_regressions.json")
    if key not in library["regressions"]:
        raise SystemExit(
            "Unknown published regression %r. Available: %s."
            % (key, ", ".join(sorted(library["regressions"]))))
    entry = dict(library["regressions"][key])
    entry["as_of"] = library["as_of"]
    entry["source"] = library["source"]
    entry["refresh"] = library["refresh"]
    return entry


def _evaluate(equation, subject, log_predictors):
    """Evaluate a linear equation for one firm and name any missing input."""
    total = float(equation.get("intercept", 0.0))
    used = {"intercept": float(equation.get("intercept", 0.0))}
    for name, coefficient in equation.items():
        if name == "intercept":
            continue
        raw = subject.get(name)
        if raw is None:
            raise SystemExit(
                "The equation needs %r but the subject does not carry it. Supply every "
                "predictor the equation names: %s."
                % (name, ", ".join(k for k in equation if k != "intercept")))
        v = float(raw)
        if name in log_predictors:
            if v <= 0:
                raise SystemExit(
                    "%s is %.4g, so ln(%s) is undefined. This firm cannot be priced by a "
                    "log specification." % (name, v, name))
            v = math.log(v)
        used[name] = v
        total += coefficient * v
    return total, used


def predict(p):
    log_predictors = set(p.get("log_predictors") or [])
    fitted = None
    if p.get("library"):
        entry = _published(p["library"])
        equation = entry["coefficients"]
        log_predictors |= set(entry.get("log_predictors") or [])
        source = {"library": p["library"], "as_of": entry["as_of"],
                  "r_squared": entry.get("r_squared"), "units": entry["units"],
                  "definition": entry["definition"], "refresh": entry["refresh"]}
    elif p.get("equation"):
        equation = p["equation"]
        source = {"library": None, "note": "caller-supplied coefficients"}
    elif p.get("observations"):
        fitted = regress(p)
        equation = fitted["equation_coefficients"]
        log_predictors |= set(p.get("log_predictors") or [])
        # A fitted equation names its log columns as "ln(x)"; the subject carries the
        # raw field, so map the coefficient names back before evaluating.
        equation = {(k[3:-1] if k.startswith("ln(") else k): v for k, v in equation.items()}
        source = {"library": None, "note": "fitted from the observations in this payload",
                  "r_squared": fitted["r_squared"], "equation": fitted["equation"]}
    else:
        raise SystemExit(
            "predict needs one of: 'library' (a bundled published regression), "
            "'equation' (your own coefficients keyed by predictor name), or "
            "'observations' (a sample to fit first)."
        )

    subjects = p.get("subjects")
    if subjects is None:
        subject = p.get("subject")
        if subject is None:
            if fitted is None:
                raise SystemExit("Pass 'subject' (one firm) or 'subjects' (several).")
            subjects = p["observations"]
        else:
            subjects = [subject]

    rows = []
    for s in subjects:
        predicted, inputs = _evaluate(equation, s, log_predictors)
        row = {"name": s.get("name"), "predicted_multiple": predicted, "inputs": inputs}
        actual = s.get("actual") if s.get("actual") is not None else s.get(
            p.get("dependent") or "actual")
        if predicted <= 0:
            row["status"] = "refused"
            row["reason"] = (
                "The equation predicts a non-positive multiple (%.4f). That is the "
                "negative-intercept problem, not a valuation. Re-fit through the origin, "
                "or price this firm on a multiple whose regression has a positive "
                "intercept." % predicted)
        elif actual is not None:
            row["status"] = "computed"
            row["actual_multiple"] = float(actual)
            row["over_under_valuation"] = float(actual) / predicted - 1
            row["reading"] = ("below the predicted multiple — relatively cheap"
                              if float(actual) < predicted else
                              "above the predicted multiple — relatively expensive")
        else:
            row["status"] = "computed"
            row["note"] = "No actual multiple supplied, so no over/under comparison."
        rows.append(row)

    out = {"source": source, "predictions": rows,
           "verdict_scope": ("Relative to the sample the equation was fitted on. A firm "
                             "can be cheap against this benchmark and still overpriced in "
                             "absolute terms.")}
    if fitted is not None:
        out["fit"] = {k: fitted[k] for k in
                      ("coefficients", "r_squared", "adjusted_r_squared", "n",
                       "predictor_correlations", "warnings", "equation")}
    elif p.get("library"):
        entry = _published(p["library"])
        out["cautions"] = entry.get("cautions", [])
    return out


def cmd_predict(args):
    _emit(predict(_read_payload(args)))


# ====================================================== STEP 5: MULTI-BUSINESS FIRMS

# The packet's default high-growth period for a division that out-earns its cost of
# capital. A division that does not earn its cost of capital gets zero years, not a
# shorter five: growth there destroys value, so there is nothing to extend.
DEFAULT_HIGH_GROWTH_YEARS = 5

# A gap between the sum of the parts and the market's enterprise value smaller than this
# is inside the noise of a peer-multiple exercise. It changes the wording of the reading
# and nothing else — no number here is ever discounted for it.
MATERIAL_GAP_TO_MARKET = 0.10

# The scalar a division is priced on, mapped onto the denominator keys the claimholder
# consistency test already knows. The multiple gets multiplied by the scalar, so an
# EV/Capital multiple applied to EBITDA is the same error as an inconsistent multiple.
DIVISION_SCALARS = {
    "ebitda": "ebitda", "ebit": "ebit",
    "revenue": "revenue", "revenues": "revenue",
    "capital": "invested_capital", "invested_capital": "invested_capital",
    "net_income": "net_income", "book_equity": "book_equity",
}


def _require_objects(value, field, hint):
    """A list of objects, or an explanation of what was expected instead."""
    if not value:
        raise SystemExit("Pass %r: a list of objects, %s" % (field, hint))
    if not isinstance(value, list) or not all(isinstance(x, dict) for x in value):
        raise SystemExit(
            "%r must be a list of objects (got %s), %s"
            % (field, type(value).__name__, hint))
    return value


def capitalized_corporate_expense(expense, tax_rate, company_cost_of_capital, growth):
    """Unallocated corporate overhead capitalized as an after-tax growing perpetuity.

    Segment operating income is normally reported before corporate G&A, so the divisional
    values add up to more than the firm is worth. The overhead is a real and permanent
    cash drain. It has to be either allocated across the divisions before they are priced,
    or capitalized here and subtracted from the sum. Leaving it out is not a third option.
    """
    _require_spread(company_cost_of_capital, growth, "company cost of capital",
                    "stable growth")
    return expense * (1 - tax_rate) * (1 + growth) / (company_cost_of_capital - growth)


def _division_scalar(d, scalar_name):
    """The value the multiple multiplies, with the EBITDA reconstruction if needed."""
    value = _number(d, "scalar_value")
    if value is not None:
        return value, None
    if scalar_name == "ebitda":
        # Segment disclosures often stop at operating income. EBITDA = EBIT + D&A, using
        # the normalised EBIT when the latest year is a trough or a peak.
        ebit = _number(d, "normalized_ebit")
        note = "EBITDA built as normalised EBIT + D&A"
        if ebit is None:
            ebit = _number(d, "ebit")
            note = "EBITDA built as reported EBIT + D&A; normalise a cyclical segment first"
        da = _number(d, "d_and_a")
        if ebit is not None and da is not None:
            return ebit + da, note
    return None, None


def _division_multiple(d, name):
    """Resolve one division's multiple. Explicit beats regression beats sector median."""
    if d.get("multiple") is not None:
        return _number(d, "multiple"), "own multiple", None
    if d.get("regression"):
        fundamentals = d.get("fundamentals") or {}
        try:
            value, used = _evaluate(d["regression"], fundamentals,
                                    set(d.get("log_predictors") or []))
        except SystemExit as exc:
            raise SystemExit("Division %r: %s" % (name, exc))
        return value, "sector regression at the division's own fundamentals", used
    if d.get("peer_multiple") is not None:
        return _number(d, "peer_multiple"), "sector median peer multiple", None
    return None, None, None


def _division_growth(d, tax_rate):
    """ROC, reinvestment rate and the growth those two earn, with the zero-growth rule.

    A division whose return on capital sits at or below its cost of capital gets no
    high-growth period. Growth there destroys value, so extending it adds nothing.
    """
    roc = _number(d, "roc")
    ebit = _number(d, "ebit")
    capital = _number(d, "capital_invested")
    rate = _number(d, "tax_rate")
    if rate is None:
        rate = tax_rate
    after_tax_ebit = None
    if ebit is not None and rate is not None:
        after_tax_ebit = ebit * (1 - rate)
    if roc is None and after_tax_ebit is not None and capital:
        roc = after_tax_ebit / capital
    cost_of_capital = _number(d, "cost_of_capital")
    if roc is None:
        return None
    out = {"return_on_capital": roc, "cost_of_capital": cost_of_capital}

    reinvestment = _number(d, "allocated_reinvestment")
    rir = _number(d, "reinvestment_rate")
    if rir is None and reinvestment is not None and after_tax_ebit:
        rir = reinvestment / after_tax_ebit
    if rir is not None:
        out["reinvestment_rate"] = rir
        out["growth_earned"] = rir * roc

    if cost_of_capital is None:
        out["high_growth_years_allowed"] = None
        out["growth_note"] = ("No cost of capital supplied for this division, so the "
                              "zero-growth rule cannot be applied. Supply "
                              "'cost_of_capital' per division.")
        return out
    if roc > cost_of_capital:
        out["earns_its_cost_of_capital"] = True
        out["high_growth_years_allowed"] = int(d.get("high_growth_years")
                                               or DEFAULT_HIGH_GROWTH_YEARS)
        return out
    out["earns_its_cost_of_capital"] = False
    out["high_growth_years_allowed"] = 0
    if "growth_earned" in out:
        out["growth_for_valuation"] = 0.0
    out["growth_note"] = (
        "Return on capital of %.2f%% is at or below the cost of capital of %.2f%%, so this "
        "division gets a zero-year high-growth period and its whole value is terminal. A "
        "sector peer multiple carries the sector's growth with it, so applying one here "
        "prices in growth this division has not earned."
        % (roc * 100, cost_of_capital * 100))
    return out


def _value_division(d, index, tax_rate):
    name = d.get("name") or "division %d" % (index + 1)
    row = {"division": name, "sector": d.get("sector")}

    raw = (d.get("scalar") or "").strip().lower()
    if raw not in DIVISION_SCALARS:
        row.update(status="refused",
                   reason=("scalar %r is not recognised. Use one of: %s, and match it to "
                           "the multiple — an EV/Capital multiple applied to EBITDA is a "
                           "category error, not a valuation."
                           % (d.get("scalar"), ", ".join(sorted(DIVISION_SCALARS)))))
        return row
    den_key = DIVISION_SCALARS[raw]
    claim = (d.get("multiple_class") or "enterprise").strip().lower()

    if claim == "equity":
        row.update(status="refused",
                   reason=("%s is priced on an equity multiple. Every part of a sum of the "
                           "parts has to be valued before debt, because the bridge "
                           "subtracts debt once at the corporate level; an equity-level "
                           "part subtracts that division's debt a second time. Price it on "
                           "an enterprise multiple, or value it as a stake with the "
                           "cross-holdings subcommand." % name))
        return row
    if claim not in NUMERATORS:
        row.update(status="refused",
                   reason=("multiple_class %r is not recognised. Use 'enterprise' (the "
                           "default) or 'firm'." % d.get("multiple_class")))
        return row
    ok, why = check_consistency(claim, den_key)
    if not ok:
        row.update(status="refused", reason=why)
        return row

    scalar_value, scalar_note = _division_scalar(d, raw)
    if scalar_value is None:
        row.update(status="refused",
                   reason=("no scalar value. Pass 'scalar_value', or (for an EBITDA "
                           "scalar) 'ebit' — or 'normalized_ebit' — together with "
                           "'d_and_a'."))
        return row
    if scalar_value <= 0:
        row.update(status="refused",
                   reason=("%s is %.4g. A multiple times a non-positive scalar is a "
                           "negative division value, which is not what a peer multiple "
                           "means. Normalise the segment's earnings, or price this "
                           "division on revenues or capital invested."
                           % (DENOMINATORS[den_key]["label"], scalar_value)))
        return row

    multiple, route, inputs = _division_multiple(d, name)
    if multiple is None:
        row.update(status="refused",
                   reason=("no multiple. Give the division its own 'multiple', a "
                           "'peer_multiple' (the sector median, the crude route), or a "
                           "'regression' with 'fundamentals' (the refined route)."))
        return row
    if multiple <= 0:
        row.update(status="refused",
                   reason=("the multiple works out at %.4f. A non-positive multiple is the "
                           "negative-intercept problem in the sector regression, not a "
                           "price. Re-fit that sector through the origin or use its median "
                           "multiple instead." % multiple))
        return row

    row.update(status="priced", scalar=raw, scalar_value=scalar_value,
               multiple=multiple, route=route, claimholder_class=claim,
               consistency=why, value=multiple * scalar_value)
    if scalar_note:
        row["scalar_note"] = scalar_note
    if inputs:
        row["regression_inputs"] = inputs
    growth = _division_growth(d, tax_rate)
    if growth:
        row["fundamentals"] = growth
    return row


def _corporate_items(p):
    """Read the corporate block, refusing the two shapes that hide a real number."""
    corp = p.get("corporate") or {}
    if not isinstance(corp, dict):
        raise SystemExit("'corporate' must be an object of corporate-level items.")

    debt = _number(corp, "debt")
    cash = _number(corp, "cash")
    net_debt = _number(corp, "net_debt")
    notes = []
    if net_debt is not None and (debt is not None or cash is not None):
        raise SystemExit(
            "Pass either 'net_debt' or 'debt' and 'cash', not both. Netting them yourself "
            "and passing the gross figures as well subtracts the cash twice.")
    if net_debt is not None:
        debt, cash = net_debt, 0.0
        notes.append("Net debt was supplied, so cash is inside the debt figure. Use the "
                     "market value of debt, not book, in a going-concern frame.")

    expense = _number(corp, "corporate_expenses")
    allocated = bool(corp.get("corporate_costs_already_allocated"))
    if expense is None and not allocated:
        raise SystemExit(
            "No treatment for unallocated corporate overhead. Segment operating income is "
            "normally reported before corporate G&A, so the divisions add up to more than "
            "the firm. Pass 'corporate.corporate_expenses' (the annual pre-tax figure, "
            "which is capitalized after tax and subtracted), or set "
            "'corporate.corporate_costs_already_allocated' to true if the divisional "
            "scalars are already net of the allocation. Leaving the field out to mean zero "
            "is the one thing that silently overstates the total.")
    if expense is not None and allocated:
        raise SystemExit(
            "'corporate_expenses' and 'corporate_costs_already_allocated' are alternatives. "
            "Allocate the overhead across the divisions or capitalize it here, not both — "
            "doing both charges it twice.")

    return {
        "corporate_expenses": expense, "corporate_costs_already_allocated": allocated,
        "cash": cash or 0.0, "debt": debt or 0.0,
        "financing_arm_debt": _number(corp, "financing_arm_debt") or 0.0,
        "minority_interests": _number(corp, "minority_interests") or 0.0,
        "cross_holdings": _number(corp, "cross_holdings") or 0.0,
        "other_non_operating_assets": _number(corp, "other_non_operating_assets") or 0.0,
        "other_claims": _number(corp, "other_claims") or 0.0,
        "option_value": _number(corp, "option_value") or 0.0,
        "shares_outstanding": _number(corp, "shares_outstanding"),
        "notes": notes,
    }


def sum_of_parts(p):
    """Price a multi-business firm division by division and bridge to equity."""
    for banned in ("conglomerate_discount", "holding_company_discount"):
        if banned in p:
            raise SystemExit(
                "%r is not an input. A conglomerate discount is observed in prices, not "
                "derived from the parts. Pass 'market_enterprise_value' instead and the "
                "output reports the gap between the sum of the parts and what the market "
                "pays for the whole. Subtracting a discount you chose yourself makes the "
                "sum of the parts agree with the market by construction, which is the one "
                "thing this calculation must never do." % banned)

    divisions = _require_objects(
        p.get("divisions"), "divisions",
        "each with a 'scalar' ('ebitda', 'revenues', 'capital', ...), a 'scalar_value', "
        "and either a 'multiple', a 'peer_multiple' or a 'regression' plus "
        "'fundamentals'.")

    tax_rate = _number(p, "tax_rate")
    corp = _corporate_items(p)
    rows = [_value_division(d, i, tax_rate) for i, d in enumerate(divisions)]
    priced = [r for r in rows if r["status"] == "priced"]
    refused = [r for r in rows if r["status"] != "priced"]
    if not priced:
        raise SystemExit(
            "No division could be priced. First refusal: %s — %s"
            % (rows[0]["division"], rows[0]["reason"]))

    total_parts = sum(r["value"] for r in priced)
    for r in priced:
        # The contribution share is measured against the gross sum of the divisions,
        # before the corporate drag and the bridge, so the shares add to exactly 1.
        r["share_of_sum_of_parts"] = r["value"] / total_parts

    drag = 0.0
    if corp["corporate_expenses"]:
        wacc = _number(p, "company_cost_of_capital")
        growth = _number(p, "stable_growth")
        if tax_rate is None or wacc is None or growth is None:
            raise SystemExit(
                "Capitalizing corporate overhead needs 'tax_rate', "
                "'company_cost_of_capital' and 'stable_growth' at the top level. The "
                "overhead is discounted at the company-wide cost of capital, not at any "
                "one division's.")
        drag = capitalized_corporate_expense(corp["corporate_expenses"], tax_rate, wacc,
                                             growth)

    operating_assets = total_parts - drag
    firm_value = (operating_assets + corp["cash"] + corp["cross_holdings"]
                  + corp["other_non_operating_assets"])
    equity_value = (firm_value - corp["debt"] - corp["financing_arm_debt"]
                    - corp["minority_interests"] - corp["other_claims"])
    common_stock = equity_value - corp["option_value"]

    out = {
        "name": p.get("name"),
        "divisions": rows,
        "divisions_priced": len(priced),
        "divisions_refused": len(refused),
        "sum_of_division_values": total_parts,
        "capitalized_corporate_expense_drag": drag,
        "value_of_operating_assets": operating_assets,
        "bridge": {
            "value_of_operating_assets": operating_assets,
            "cash": corp["cash"], "cross_holdings": corp["cross_holdings"],
            "other_non_operating_assets": corp["other_non_operating_assets"],
            "value_of_firm": firm_value,
            "debt": corp["debt"], "financing_arm_debt": corp["financing_arm_debt"],
            "minority_interests": corp["minority_interests"],
            "other_claims": corp["other_claims"],
            "value_of_equity": equity_value,
            "option_value": corp["option_value"],
            "value_of_common_stock": common_stock,
        },
        "verdict_scope": ("A price, not a value. Each division inherits whatever its own "
                          "peer group is worth today, including that group's mispricing."),
    }

    shares = corp["shares_outstanding"]
    if shares:
        out["value_per_share"] = common_stock / shares
        out["shares_outstanding"] = shares

    market_ev = _number(p, "market_enterprise_value")
    if market_ev is not None:
        out["market_enterprise_value"] = market_ev
        gap = 1 - market_ev / operating_assets if operating_assets else None
        out["gap_to_market_enterprise_value"] = gap
        out["gap_reading"] = _gap_reading(gap)

    out["warnings"] = _sum_of_parts_warnings(rows, priced, refused, corp, drag)
    return out


def _gap_reading(gap):
    if gap is None:
        return None
    if gap > MATERIAL_GAP_TO_MARKET:
        return ("The market pays %.1f%% less for the whole than the parts price at. That "
                "gap is the conglomerate discount as observed, and nothing above has been "
                "reduced for it. It is only money if somebody actually buys the pieces at "
                "peer multiples, and it may instead be the market's price for bad capital "
                "allocation, cross-subsidy or entrenchment." % (gap * 100))
    if gap < -MATERIAL_GAP_TO_MARKET:
        return ("The market pays %.1f%% more for the whole than the parts price at. Either "
                "the peer groups are cheap relative to this firm, real synergies make the "
                "pieces worth more together, or the segment scalars are understated."
                % (-gap * 100))
    return ("The sum of the parts and the market's enterprise value are within %.1f%% of "
            "each other, which is inside the noise of a peer-multiple exercise. There is "
            "no conglomerate discount to report here." % abs(gap * 100))


def _sum_of_parts_warnings(rows, priced, refused, corp, drag):
    warnings = []
    if corp["corporate_costs_already_allocated"]:
        warnings.append(
            "Corporate overhead was declared already allocated across the divisions, so "
            "nothing was capitalized or subtracted. Check that the divisional scalars are "
            "genuinely net of corporate G&A; segment disclosures usually are not.")
    elif drag:
        warnings.append(
            "Unallocated corporate overhead is capitalized at %.2f and subtracted. How the "
            "overhead is treated moves divisional returns on capital materially, so state "
            "the treatment alongside the total." % drag)
    for r in priced:
        f = r.get("fundamentals") or {}
        if f.get("growth_note"):
            warnings.append("%s: %s" % (r["division"], f["growth_note"]))
    crude = [r["division"] for r in priced if r["route"] == "sector median peer multiple"]
    if crude:
        warnings.append(
            "%s priced at the raw sector median. A division is not the median firm in its "
            "sector; controlling for its own returns and margins moved United Technologies "
            "from $61.7bn to $74.2bn. Fit or look up the sector regression where you can."
            % ", ".join(crude))
    multiples = {round(r["multiple"], 10) for r in priced}
    if len(priced) > 1 and len(multiples) == 1:
        warnings.append(
            "Every division carries the same multiple. One company-wide multiple across "
            "businesses with different risk and returns is the single most common error in "
            "a sum of the parts, and it moves the answer a lot.")
    if refused:
        warnings.append(
            "%d division(s) were refused, so the total below covers only the rest of the "
            "firm. Fix the refusals rather than reading the partial sum: %s."
            % (len(refused), "; ".join("%s (%s)" % (r["division"], r["reason"])
                                       for r in refused)))
    if not corp["shares_outstanding"]:
        warnings.append(
            "No share count, so the output stops at the value of common stock. Divide by "
            "actual shares plus granted restricted shares, never by a diluted count when "
            "option value has already been subtracted.")
    if corp["financing_arm_debt"] == 0 and corp["debt"]:
        warnings.append(
            "No financing-arm debt was supplied. A captive finance arm's debt is separate "
            "from industrial debt and is missed routinely; GE's bridge subtracts $51.0bn "
            "of GE Capital debt on top of $83.6bn of industrial debt.")
    warnings.extend(corp["notes"])
    return warnings


def cmd_sum_of_parts(args):
    _emit(sum_of_parts(_read_payload(args)))


def _value_holding(h, index):
    """Value one stake in another firm, and decide whether it is added or subtracted."""
    name = h.get("name") or "holding %d" % (index + 1)
    row = {"holding": name}

    ownership = _number(h, "ownership")
    if ownership is None:
        row.update(status="refused",
                   reason="no 'ownership'. Enter the stake as a decimal fraction (0.60 "
                          "for 60%).")
        return row
    if ownership <= 0 or ownership > 1:
        row.update(status="refused",
                   reason=("ownership is %.4g. Enter it as a decimal fraction between 0 "
                           "and 1 (0.60 for 60%%), not as a percentage." % ownership))
        return row
    row["ownership"] = ownership

    consolidated = h.get("consolidated")
    if consolidated is None:
        # Above 50% the parent consolidates, so the operating value already carries 100%
        # of the subsidiary. Control can attach below 50%, which is why this is only a
        # default and the payload can say otherwise.
        consolidated = ownership > 0.50
        row["consolidation_inferred"] = True
    row["consolidated"] = bool(consolidated)

    if consolidated:
        return _value_majority_stake(h, row, name, ownership)
    return _value_minority_stake(h, row, name, ownership)


def _value_majority_stake(h, row, name, ownership):
    """A consolidated stake is already inside the operating value; only what the parent
    does not own comes back out, and it comes out at market, not at book."""
    row["treatment"] = "subtract the minority interest"
    row["why"] = ("The parent consolidates 100%% of %s's revenues, earnings and assets, "
                  "but owns %.1f%% of it. The %.1f%% it does not own is a claim on the "
                  "consolidated value and has to be subtracted."
                  % (name, ownership * 100, (1 - ownership) * 100))

    subsidiary = _number(h, "subsidiary_equity_value")
    book = _number(h, "minority_interest_book")
    pb = _number(h, "sector_price_to_book")

    if subsidiary is not None:
        value = (1 - ownership) * subsidiary
        row["value_basis"] = "the subsidiary's own equity value times the stake not owned"
    elif book is not None and pb is not None:
        value = book * pb
        row["value_basis"] = ("book minority interest times the subsidiary sector's "
                              "price-to-book ratio")
        if pb == 1.0:
            row["basis_note"] = ("A price-to-book of 1.0 makes book and market equal by "
                                 "assumption. State that assumption rather than letting it "
                                 "pass as an estimate.")
    elif book is not None:
        row.update(status="refused",
                   reason=("only the book minority interest (%.4g) was supplied. Book is "
                           "the wrong measure here and is usually far too low for a "
                           "profitable subsidiary. Pass 'sector_price_to_book' to convert "
                           "it, or pass 'subsidiary_equity_value' and let the stake not "
                           "owned come out of that." % book))
        return row
    else:
        row.update(status="refused",
                   reason=("no value for the minority interest. Pass "
                           "'subsidiary_equity_value' (preferred), or "
                           "'minority_interest_book' together with "
                           "'sector_price_to_book'."))
        return row

    row.update(status="valued", minority_interest_value=value, signed_contribution=-value)
    return row


def _value_minority_stake(h, row, name, ownership):
    """An unconsolidated stake is in none of the operating numbers, so it is added."""
    row["treatment"] = "add the stake"
    row["why"] = ("%s is not consolidated, so the parent's operating value contains none "
                  "of it beyond the dividends or equity income it books. The stake is "
                  "added on top." % name)

    market_stake = _number(h, "market_value_of_stake")
    subsidiary = _number(h, "subsidiary_equity_value")
    book = _number(h, "book_equity")
    pb = _number(h, "sector_price_to_book")

    if market_stake is not None:
        value = market_stake
        row["value_basis"] = "the traded value of the stake itself"
    elif subsidiary is not None:
        value = ownership * subsidiary
        row["value_basis"] = ("%s of the subsidiary's equity value"
                              % ("%.4g%%" % (ownership * 100)))
    elif book is not None and pb is not None:
        value = ownership * book * pb
        row["value_basis"] = ("estimated: the stake's book equity times the subsidiary "
                              "sector's price-to-book ratio")
        row["basis_note"] = ("An estimate, not a price. It is the fallback for a holding "
                             "that does not trade and has no valuation of its own.")
    else:
        row.update(status="refused",
                   reason=("no value for the stake. Pass 'market_value_of_stake' where it "
                           "trades, 'subsidiary_equity_value' where you have valued it, or "
                           "'book_equity' with 'sector_price_to_book' where you have "
                           "neither."))
        return row

    row.update(status="valued", stake_value=value, signed_contribution=value)
    if h.get("equity_income_in_operating_income"):
        row["double_count_warning"] = (
            "This holding's equity income is still inside the parent's operating income. "
            "Strip it out, or the stake is counted once in the flows and once again here.")
    return row


def cross_holdings(p):
    """Value stakes in other firms and net them into the parent's equity."""
    holdings = _require_objects(
        p.get("holdings"), "holdings",
        "each with 'ownership' (a decimal fraction) and a value — "
        "'market_value_of_stake', 'subsidiary_equity_value', or 'book_equity' with "
        "'sector_price_to_book'.")

    frame = (p.get("frame") or "intrinsic").strip().lower()
    if frame not in ("intrinsic", "pricing"):
        raise SystemExit("'frame' must be 'intrinsic' or 'pricing'.")

    rows = [_value_holding(h, i) for i, h in enumerate(holdings)]
    valued = [r for r in rows if r["status"] == "valued"]
    refused = [r for r in rows if r["status"] != "valued"]

    added = sum(r["signed_contribution"] for r in valued if r["signed_contribution"] > 0)
    subtracted = sum(-r["signed_contribution"] for r in valued
                     if r["signed_contribution"] < 0)
    net = added - subtracted

    parent_value = _number(p, "parent_value") or 0.0
    parent_debt = _number(p, "parent_debt") or 0.0
    cash = _number(p, "cash") or 0.0
    taxes_due = _number(p, "taxes_due") or 0.0
    option_value = _number(p, "option_value") or 0.0

    equity_value = parent_value - parent_debt + cash + net - taxes_due
    common_stock = equity_value - option_value

    out = {
        "name": p.get("name"), "frame": frame, "holdings": rows,
        "holdings_valued": len(valued), "holdings_refused": len(refused),
        "value_of_minority_holdings": added,
        "market_value_of_minority_interest": subtracted,
        "net_cross_holding_adjustment": net,
        "parent_value": parent_value, "parent_debt": parent_debt, "cash": cash,
        "taxes_due": taxes_due,
        "value_of_equity": equity_value,
        "option_value": option_value,
        "value_of_common_stock": common_stock,
    }

    shares = _number(p, "shares_outstanding")
    if shares:
        out["shares_outstanding"] = shares
        out["value_per_share"] = common_stock / shares

    base = parent_value + added + cash
    if base > 0:
        # The composition check from the source: the three sources of value have to
        # account for the whole firm, so these shares add to 1 by construction.
        out["composition_percentages"] = {
            "operating_assets": parent_value / base,
            "cross_holdings": added / base,
            "cash": cash / base,
        }

    out["warnings"] = _cross_holding_warnings(rows, valued, refused, frame, parent_value,
                                              taxes_due)
    return out


def _cross_holding_warnings(rows, valued, refused, frame, parent_value, taxes_due):
    warnings = []
    if not parent_value:
        warnings.append(
            "No 'parent_value', so the equity figure is the holdings alone. Either add the "
            "parent as a 100%-owned holding, or pass its un-consolidated firm value as "
            "'parent_value' with its debt as 'parent_debt'.")
    for r in valued:
        if r.get("double_count_warning"):
            warnings.append("%s: %s" % (r["holding"], r["double_count_warning"]))
        if r.get("consolidation_inferred"):
            warnings.append(
                "%s was treated as %s purely from the %.1f%% stake. Read the notes to the "
                "accounts: control, and therefore consolidation, can attach below 50%%."
                % (r["holding"],
                   "consolidated" if r["consolidated"] else "unconsolidated",
                   r["ownership"] * 100))
        if frame == "intrinsic" and r.get("value_basis", "").startswith("the traded"):
            warnings.append(
                "%s is carried at its traded value inside an intrinsic valuation. That "
                "imports the market's pricing error into your answer, which is the thing "
                "the valuation was meant to test. Value it yourself, or say the number is "
                "a hybrid." % r["holding"])
        if r.get("basis_note"):
            warnings.append("%s: %s" % (r["holding"], r["basis_note"]))
    if not taxes_due and any(r["signed_contribution"] > 0 for r in valued):
        warnings.append(
            "No taxes were netted against the holdings. A sale or a repatriation triggers "
            "tax on the unrealised gain; it came to $5,017m on Yahoo's stakes, over 10% of "
            "its equity value.")
    if refused:
        warnings.append(
            "%d holding(s) were refused, so the adjustment is incomplete: %s."
            % (len(refused), "; ".join("%s (%s)" % (r["holding"], r["reason"])
                                       for r in refused)))
    return warnings


def cmd_cross_holdings(args):
    _emit(cross_holdings(_read_payload(args)))


# ---------------------------------------------------------------------------- selftest

TRUCKING = [
    {"name": "KLLM Trans. Svcs.", "multiple": 2.34},
    {"name": "Ryder System", "multiple": 2.81},
    {"name": "Rollins Truck Leasing", "multiple": 3.06},
    {"name": "Hunt (J.B.)", "multiple": 3.17},
    {"name": "Yellow Corp.", "multiple": 3.18},
    {"name": "Werner Enterprises", "multiple": 4.30},
    {"name": "AMERCO", "multiple": 4.72},
    {"name": "USFreightways", "multiple": 4.95},
    {"name": "Arkansas Best", "multiple": 5.40},
    {"name": "Amer. Freightways", "multiple": 5.92},
    {"name": "Swift Transportation", "multiple": 6.89},
    {"name": "CNF Transportation", "multiple": 7.36},
    {"name": "Caliber System", "multiple": 7.55},
    {"name": "Knight Transportation", "multiple": 9.54},
    {"name": "Heartland Express", "multiple": 11.26},
    {"name": "Mark VII", "multiple": 12.38},
    {"name": "Coach USA", "multiple": 13.11},
    # EBITDA of -0.17 against a value of 5.60, so the ratio comes out at -32.94. The
    # source reports it as NA; either form has to leave the sample.
    {"name": "US 1 Inds.", "multiple": -32.94},
]

# European banks, the 2010 lecture sample. PBV, ROE and standard deviation in stock
# prices, with ROE and the standard deviation as decimals.
EUROPEAN_BANKS = [
    {"name": "Bayerische Hypo-und Vereinsbank", "PBV": 0.80, "ROE": -0.0166, "stdev": 0.4906},
    {"name": "Commerzbank", "PBV": 1.09, "ROE": -0.0672, "stdev": 0.3621},
    {"name": "Deutsche Bank", "PBV": 1.23, "ROE": 0.0132, "stdev": 0.3579},
    {"name": "Banca Intesa", "PBV": 1.66, "ROE": 0.0156, "stdev": 0.3414},
    {"name": "BNP Paribas", "PBV": 1.72, "ROE": 0.1246, "stdev": 0.3103},
    {"name": "Banco Santander", "PBV": 1.86, "ROE": 0.1106, "stdev": 0.2836},
    {"name": "Sanpaolo IMI", "PBV": 1.96, "ROE": 0.0855, "stdev": 0.2664},
    {"name": "BBVA", "PBV": 1.98, "ROE": 0.1117, "stdev": 0.1862},
    {"name": "Societe Generale", "PBV": 2.04, "ROE": 0.0971, "stdev": 0.2255},
    {"name": "Royal Bank of Scotland", "PBV": 2.09, "ROE": 0.2022, "stdev": 0.1835},
    {"name": "HBOS", "PBV": 2.15, "ROE": 0.2245, "stdev": 0.2195},
    {"name": "Barclays", "PBV": 2.23, "ROE": 0.2116, "stdev": 0.2073},
    {"name": "Unicredito Italiano", "PBV": 2.30, "ROE": 0.1486, "stdev": 0.1379},
    {"name": "Kredietbank Luxembourgeoise", "PBV": 2.46, "ROE": 0.1774, "stdev": 0.1238},
    {"name": "Erste Bank", "PBV": 2.53, "ROE": 0.1028, "stdev": 0.2191},
    {"name": "Standard Chartered", "PBV": 2.59, "ROE": 0.2018, "stdev": 0.1993},
    {"name": "HSBC", "PBV": 2.94, "ROE": 0.1850, "stdev": 0.1966},
    {"name": "Lloyds TSB", "PBV": 3.33, "ROE": 0.3284, "stdev": 0.1866},
]

# United Technologies, 2009 ($ millions). Each division is priced off its own sector's
# regression, evaluated at its own fundamentals — the refined route. The costs of capital
# come from the parallel DCF route and are carried here only so the zero-growth rule can
# be applied: UTC Fire & Security earns 6.03% against a 6.78% cost of capital.
UTC_DIVISIONS = [
    {"name": "Carrier", "sector": "Refrigeration systems", "scalar": "ebitda",
     "scalar_value": 1510.0, "roc": 0.1357, "cost_of_capital": 0.0784,
     "regression": {"intercept": 5.35, "tax_rate": -3.55, "roc": 14.17},
     "fundamentals": {"tax_rate": 0.38, "roc": 0.1357}},
    {"name": "Pratt & Whitney", "sector": "Defense", "scalar": "revenues",
     "scalar_value": 12965.0, "roc": 0.2451, "cost_of_capital": 0.0772,
     "regression": {"intercept": 0.85, "pretax_operating_margin": 7.32},
     "fundamentals": {"pretax_operating_margin": 0.1637}},
    {"name": "Otis", "sector": "Construction", "scalar": "ebitda", "scalar_value": 2680.0,
     "roc": 0.3571, "cost_of_capital": 0.0994,
     "regression": {"intercept": 3.17, "tax_rate": -2.87, "roc": 14.66},
     "fundamentals": {"tax_rate": 0.38, "roc": 0.3571}},
    {"name": "UTC Fire & Security", "sector": "Security", "scalar": "capital",
     "scalar_value": 5575.0, "roc": 0.0603, "cost_of_capital": 0.0678,
     "regression": {"intercept": 0.55, "roc": 8.22}, "fundamentals": {"roc": 0.0603}},
    {"name": "Hamilton Sundstrand", "sector": "Industrial products", "scalar": "revenues",
     "scalar_value": 6207.0, "roc": 0.1416, "cost_of_capital": 0.0906,
     "regression": {"intercept": 0.51, "pretax_operating_margin": 6.13},
     "fundamentals": {"pretax_operating_margin": 0.1771}},
    {"name": "Sikorsky", "sector": "Aircraft", "scalar": "capital", "scalar_value": 2217.0,
     "roc": 0.1337, "cost_of_capital": 0.0982,
     "regression": {"intercept": 0.65, "roc": 6.98}, "fundamentals": {"roc": 0.1337}},
]

# GE's 2018 analysis of 2017 data ($ millions), the crude route: each segment's EBITDA is
# its normalised EBIT (the 2013-17 average margin on 2017 revenues) plus 2017 D&A, priced
# at the peer group's median EV/EBITDA. The two disclosed segments are carried here with
# the balance of the businesses as a single already-valued aggregate, so the bridge can be
# reproduced against the source's per-share figure.
GE_SEGMENTS = [
    {"name": "Power", "sector": "Power", "scalar": "ebitda", "normalized_ebit": 4061.80,
     "d_and_a": 1358.00, "peer_multiple": 10.55},
    {"name": "Aviation", "sector": "Aviation", "scalar": "ebitda",
     "normalized_ebit": 5209.28, "d_and_a": 979.00, "peer_multiple": 6.56},
    {"name": "All other segments including GE Capital", "sector": "Mixed",
     "scalar": "ebitda", "scalar_value": 114253.44, "multiple": 1.0},
]

EXAMPLES = {
    "multiples": {
        "name": "Example Co",
        "price_per_share": 42.0, "shares_outstanding": 500.0,
        "debt": 3000.0, "cash": 1200.0, "minority_interests": 0.0,
        "net_income": 900.0, "book_equity": 6000.0, "revenue": 12000.0,
        "ebitda": 2400.0, "ebit": 1700.0, "invested_capital": 7800.0,
        "multiples": ["PE", "PBV", "EV/EBITDA", "EV/Sales", "EV/EBIT", "EV/IC"],
        "custom": [{"name": "EV/Net Income", "numerator": "enterprise",
                    "denominator": "net_income"}],
    },
    "peer-stats": {
        "multiple": "PBV", "universe_size": 18,
        "firms": [{"name": b["name"], "multiple": b["PBV"], "companion": b["ROE"],
                   "risk": b["stdev"]} for b in EUROPEAN_BANKS],
        "subject": {"name": "Unicredito Italiano", "multiple": 2.30, "companion": 0.1486,
                    "risk": 0.1379},
    },
    "locate": {"table": "us_trailing_pe_2021", "value": 14.2},
    "intrinsic": {"multiple": "PE", "model": "two_stage", "payout": 0.20, "growth": 0.25,
                  "years": 5, "cost_of_equity": 0.115, "stable_payout": 0.50,
                  "stable_growth": 0.08, "actual_multiple": 35.0},
    "regress": {"scope": "sector", "dependent": "PBV", "predictors": ["ROE", "stdev"],
                "observations": EUROPEAN_BANKS},
    "predict": {"library": "us_pe_jan2021", "subject": {"name": "Disney", "payout": 0.20,
                                                        "growth": 0.15, "actual": 35.0}},
    "sum-of-parts": {
        "name": "United Technologies (2009)",
        "tax_rate": 0.38, "company_cost_of_capital": 0.0868, "stable_growth": 0.03,
        "market_enterprise_value": 52261.0,
        "divisions": UTC_DIVISIONS,
        "corporate": {"corporate_expenses": 408.0, "cash": 0.0, "debt": 0.0,
                      "financing_arm_debt": 0.0, "minority_interests": 0.0,
                      "cross_holdings": 0.0, "option_value": 0.0,
                      "shares_outstanding": None},
    },
    "cross-holdings": {
        "name": "Company A", "frame": "intrinsic",
        "parent_value": 1000.0, "parent_debt": 200.0,
        "holdings": [
            {"name": "Company B", "ownership": 0.10, "consolidated": False,
             "subsidiary_equity_value": 250.0},
            {"name": "Company C", "ownership": 0.60, "consolidated": True,
             "subsidiary_equity_value": 250.0},
        ],
    },
    "selftest": {},
}


def _close(actual, expected, tol=1e-6):
    return abs(actual - expected) <= tol * max(1.0, abs(expected))


def cmd_selftest(args):
    """Worked examples from the Damodaran corpus, plus algebraic invariants that a
    wrong implementation cannot satisfy by accident."""
    results = []

    def check(name, actual, expected, tol=1e-6):
        results.append({"case": name, "expected": expected, "actual": actual,
                        "pass": isinstance(actual, (int, float))
                                and _close(actual, expected, tol)})

    def assert_true(name, condition, detail=None):
        results.append({"case": name, "expected": True, "actual": bool(condition),
                        "pass": bool(condition), "detail": detail})

    def refuses(name, thunk, needle):
        """Bad input must come back as an explanation, never as a traceback."""
        try:
            thunk()
        except SystemExit as exc:
            results.append({"case": name, "expected": "refusal mentioning %r" % needle,
                            "actual": str(exc), "pass": needle in str(exc)})
            return
        results.append({"case": name, "expected": "a refusal", "actual": "no refusal",
                        "pass": False})

    # --- Definitional tests -------------------------------------------------------
    ok, _ = check_consistency("enterprise", "net_income")
    assert_true("EV/Net Income is refused as inconsistent", not ok)
    ok, _ = check_consistency("equity", "ebitda")
    assert_true("Price/EBITDA is refused as inconsistent", not ok)
    ok, _ = check_consistency("enterprise", "ebitda")
    assert_true("EV/EBITDA is accepted", ok)
    ok, _ = check_consistency("equity", "book_equity")
    assert_true("PBV is accepted", ok)

    # Enterprise value nets cash out and adds minority interests back.
    nums = build_numerators({"market_cap": 21000.0, "debt": 3000.0, "cash": 1200.0,
                             "minority_interests": 400.0})
    check("enterprise value nets cash and adds minority interests",
          nums["enterprise_value"], 21000.0 + 3000.0 - 1200.0 + 400.0)

    # A loss-making firm must be refused a PE, not handed a negative one.
    loss = compute_multiples({"market_cap": 5000.0, "net_income": -250.0,
                              "revenue": 4000.0, "multiples": ["PE", "P/S"]})
    pe_row = next(r for r in loss["results"] if r["multiple"] == "PE")
    assert_true("negative net income refuses PE rather than returning a negative",
                pe_row["status"] == "refused" and "value" not in pe_row)
    ps_row = next(r for r in loss["results"] if r["multiple"] == "P/S")
    assert_true("the same firm still gets a price-to-sales multiple",
                ps_row["status"] == "computed")
    check("price-to-sales for the loss-making firm", ps_row["value"], 5000.0 / 4000.0)

    # --- Descriptive tests --------------------------------------------------------
    stats = peer_statistics({"multiple": "EV/EBITDA", "universe_size": 18,
                             "firms": TRUCKING})
    check("trucking sample: 17 of 18 firms have a usable EV/EBITDA",
          stats["firms_with_a_usable_multiple"], 17)
    assert_true("the negative-EBITDA firm is recorded as dropped, not ignored",
                stats["firms_dropped"] == 1
                and stats["dropped_firms"][0]["name"] == "US 1 Inds.")
    # 17 values, so the median is the 9th order statistic, Arkansas Best at 5.40.
    check("trucking median EV/EBITDA", stats["median"], 5.40)
    assert_true("mean exceeds median on the right-skewed sample",
                stats["mean"] > stats["median"])
    # Percentile convention: p25 sits at rank 0.25 x 16 = 4, the 5th value (3.18).
    check("trucking 25th percentile", stats["p25"], 3.18)
    check("trucking 75th percentile", stats["p75"], 7.55)

    # Ryder at 2.81 is far below the sector median, which is exactly the trap: its
    # reinvestment needs, not mispricing, explain the low multiple.
    assert_true("Ryder sits below the sector median", 2.81 < stats["median"])

    # European bank medians, against the values the source quotes for the same sample.
    bank_stats = peer_statistics(EXAMPLES["peer-stats"])
    check("bank sector median PBV", bank_stats["median"], 2.07, 5e-3)
    check("bank sector median ROE",
          bank_stats["median_test"]["sector_median_companion"], 0.1182, 5e-3)
    check("bank sector median standard deviation",
          bank_stats["median_test"]["sector_median_risk"], 0.2193, 5e-3)
    # Unicredito has above-median ROE and below-median risk but an above-median PBV, so
    # the screen cannot fire either way. That is where the median test runs out and a
    # regression has to take over.
    assert_true("median test declines to fire on Unicredito Italiano",
                bank_stats["median_test"]["verdict"] == "screen does not fire")

    # --- Analytical tests ---------------------------------------------------------
    # Lecture case: 25% growth for 5 years at 20% payout, then 8% growth at 50% payout,
    # beta 1.0, riskfree 6%, ERP 5.5%, so the cost of equity is 11.5%.
    two_stage = intrinsic_pe_two_stage(0.20, 0.25, 5, 0.115, 0.50, 0.08)
    check("two-stage intrinsic PE (lecture case)", two_stage["intrinsic_pe"], 28.75, 1e-4)
    assert_true("high-growth term stays positive when growth exceeds the cost of equity",
                two_stage["high_growth_term"] > 0)
    peg = intrinsic({"multiple": "PEG", "model": "two_stage", "payout": 0.20,
                     "growth": 0.25, "years": 5, "cost_of_equity": 0.115,
                     "stable_payout": 0.50, "stable_growth": 0.08})
    check("intrinsic PEG for the same firm", peg["intrinsic_peg"], 1.15, 1e-3)

    # Bank PBV: ROE 20.22%, cost of equity 9%, stable growth 4%.
    check("justified PBV from (ROE - g)/(r - g)",
          intrinsic_pbv(0.2022, 0.04, 0.09)["short_form_pbv"], 3.244, 1e-3)

    # Identity: on a forward basis the long form collapses to the short form exactly
    # when growth is the sustainable rate. A wrong PBV formula breaks this.
    roe, payout, ke = 0.18, 0.70, 0.10
    g = (1 - payout) * roe
    both = intrinsic_pbv(roe, g, ke, payout, basis="forward")
    check("PBV long form equals short form at sustainable growth",
          both["long_form_pbv"], both["short_form_pbv"], 1e-12)
    assert_true("sustainable-growth check passes on consistent inputs",
                both["growth_is_consistent"])

    # The corpus's routine trap: ROE 15%, payout 40%, r 9%, g 4% are inconsistent.
    trap = intrinsic_pbv(0.15, 0.04, 0.09, 0.40, basis="trailing")
    check("inconsistent inputs give the long-form PBV of 1.248",
          trap["long_form_pbv"], 1.248, 1e-3)
    check("and the short form of 2.20", trap["short_form_pbv"], 2.20, 1e-3)
    assert_true("the inconsistency is flagged rather than averaged away",
                not trap["growth_is_consistent"] and "consistency_warning" in trap)

    # Identity: EV/IC from the margin route equals (ROIC - g)/(WACC - g) when the
    # reinvestment rate is g/ROIC.
    roic, wacc, gn = 0.14, 0.09, 0.03
    direct = intrinsic_ev_ic(roic, gn, wacc)["intrinsic_ev_ic"]
    via_margin = intrinsic_ev_sales(roic * 1.0, gn / roic, gn, wacc)["intrinsic_ev_sales"]
    check("EV/IC identity holds through the reinvestment-rate route", via_margin, direct,
          1e-12)

    # EV/EBITDA lecture case: tax 36%, CapEx/EBITDA 30%, Depreciation/EBITDA 20%,
    # WACC 10%, growth 5%, no working capital needs.
    ebitda_case = intrinsic_ev_ebitda(0.36, 0.20, 0.30, 0.0, 0.10, 0.05)
    check("intrinsic EV/EBITDA (lecture case)", ebitda_case["intrinsic_ev_ebitda"], 8.24,
          1e-4)
    heavier = intrinsic_ev_ebitda(0.36, 0.20, 0.50, 0.0, 0.10, 0.05)
    check("raising CapEx/EBITDA to 50% halves the justified multiple",
          heavier["intrinsic_ev_ebitda"], 4.24, 1e-4)

    # --- Application tests: regression --------------------------------------------
    # A regression fitted on data generated from a known equation must recover it.
    synthetic = [{"name": str(i), "y": 3.0 + 2.0 * i - 0.5 * (i % 4), "a": float(i),
                  "b": float(i % 4)} for i in range(20)]
    exact = regress({"dependent": "y", "predictors": ["a", "b"],
                     "observations": synthetic})
    coefficients = {c["name"]: c["coefficient"] for c in exact["coefficients"]}
    check("exact-fit round trip recovers the intercept", coefficients["intercept"], 3.0,
          1e-8)
    check("exact-fit round trip recovers the first slope", coefficients["a"], 2.0, 1e-8)
    check("exact-fit round trip recovers the second slope", coefficients["b"], -0.5, 1e-8)
    check("exact fit gives R-squared of 1", exact["r_squared"], 1.0, 1e-9)

    # European bank PBV regression, reproduced from the 18-firm sample. The corpus
    # reports PBV = 2.27 + 3.63 ROE - 2.68 Std dev with t-statistics 5.56, 3.32 and
    # 2.33, and an adjusted R-squared of 79%. Only a correct normal-equations solve
    # with a correct standard-error formula lands on all six numbers.
    banks = regress({"scope": "sector", "dependent": "PBV",
                     "predictors": ["ROE", "stdev"], "observations": EUROPEAN_BANKS})
    bank_coefficients = {c["name"]: c for c in banks["coefficients"]}
    check("bank regression intercept", bank_coefficients["intercept"]["coefficient"],
          2.27, 5e-3)
    check("bank regression ROE coefficient", bank_coefficients["ROE"]["coefficient"],
          3.63, 5e-3)
    check("bank regression risk coefficient", bank_coefficients["stdev"]["coefficient"],
          -2.68, 5e-3)
    # The corpus quotes t-statistics to two decimals from its own statistics package, so
    # these are checked at 1% rather than the 0.5% used for the coefficients themselves.
    check("bank regression t-statistic on the constant",
          bank_coefficients["intercept"]["t_statistic"], 5.56, 1e-2)
    check("bank regression t-statistic on ROE",
          bank_coefficients["ROE"]["t_statistic"], 3.32, 1e-2)
    check("bank regression t-statistic on risk",
          bank_coefficients["stdev"]["t_statistic"], -2.33, 1e-2)
    check("bank regression adjusted R-squared", banks["adjusted_r_squared"], 0.79, 5e-3)
    assert_true("residuals sum to zero when an intercept is fitted",
                abs(banks["sum_of_residuals"]) < 1e-9)

    # Predicted values and the over/under table from the same sample.
    bank_predictions = predict({"dependent": "PBV", "predictors": ["ROE", "stdev"],
                                "observations": EUROPEAN_BANKS, "scope": "sector"})
    by_name = {r["name"]: r for r in bank_predictions["predictions"]}
    check("Royal Bank of Scotland predicted PBV",
          by_name["Royal Bank of Scotland"]["predicted_multiple"], 2.51, 5e-3)
    check("Royal Bank of Scotland is 16.65% below its predicted PBV",
          by_name["Royal Bank of Scotland"]["over_under_valuation"], -0.1665, 2e-3)
    check("HSBC is 21.91% above its predicted PBV",
          by_name["HSBC"]["over_under_valuation"], 0.2191, 2e-3)

    # Telebras: the lowest-PE name in global telecom is still slightly expensive once
    # growth and emerging-market risk are controlled for.
    telebras = predict({
        "equation": {"intercept": 13.1151, "growth": 121.223, "emerging_market": -13.8531},
        "subject": {"name": "Telebras ADR", "growth": 0.075, "emerging_market": 1,
                    "actual": 8.9}})
    row = telebras["predictions"][0]
    check("Telebras predicted PE", row["predicted_multiple"], 8.35, 1e-3)
    check("Telebras trades 6.6% above its predicted PE",
          row["over_under_valuation"], 0.066, 1e-3)
    assert_true("a low multiple is not the same as cheap",
                row["over_under_valuation"] > 0 and row["actual_multiple"] < 12.5)

    # Market-wide pricing: Disney against the January 2021 US PE regression.
    disney = predict({"library": "us_pe_jan2021",
                      "subject": {"name": "Disney", "payout": 0.20, "growth": 0.15,
                                  "actual": 35.0}})
    check("Disney predicted PE from the market-wide regression",
          disney["predictions"][0]["predicted_multiple"], 43.59, 1e-3)
    assert_true("Disney reads as cheap against the whole US market",
                disney["predictions"][0]["over_under_valuation"] < 0)

    # The log specification: the PEG regression worked example.
    peg_pred = predict({"library": "us_peg_jan2021",
                        "subject": {"name": "Test firm", "payout": 25.0, "growth": 20.0,
                                    "beta": 1.2, "actual": 1.5}})
    check("PEG regression predicted value", peg_pred["predictions"][0]["predicted_multiple"],
          2.383, 1e-3)

    # Cross-market: the European EV/IC worked example.
    euro = predict({"library": "europe_ev_ic_jan2021",
                    "subject": {"name": "European industrial", "debt_ratio": 0.25,
                                "revenue_growth": 0.04, "roic": 0.14}})
    check("European EV/IC predicted multiple",
          euro["predictions"][0]["predicted_multiple"], 3.745, 1e-3)

    # Country pricing: Venezuela looked cheap on the headline number and was not.
    venezuela = predict({"library": "country_pe_2000",
                         "subject": {"name": "Venezuela", "interest_rate": 0.15,
                                     "real_gdp_growth": 0.035, "country_risk": 45,
                                     "actual": 20.0}})
    vrow = venezuela["predictions"][0]
    check("Venezuela predicted market PE", vrow["predicted_multiple"], 15.35, 1e-3)
    assert_true("Venezuela is expensive despite a mid-pack headline PE",
                vrow["over_under_valuation"] > 0.29)

    # A negative predicted multiple is refused rather than reported.
    negative = predict({"equation": {"intercept": -2.0, "growth": 1.0},
                        "subject": {"name": "Low-growth firm", "growth": 0.5,
                                    "actual": 12.0}})
    assert_true("a negative predicted multiple is refused, not reported",
                negative["predictions"][0]["status"] == "refused"
                and "over_under_valuation" not in negative["predictions"][0])

    # Warnings the analyst is meant to see.
    assert_true("small-sample warning fires on the 18-firm bank regression",
                any("Small sample" in w for w in banks["warnings"]))
    collinear = regress({"dependent": "y", "predictors": ["a", "b"],
                         "observations": [
                             {"y": 1.0 + 0.01 * i, "a": float(i), "b": float(i) + 0.001 * (i % 3)}
                             for i in range(40)]})
    assert_true("multicollinearity warning fires on near-duplicate predictors",
                any("Multicollinearity" in w for w in collinear["warnings"]))
    negative_intercept = regress({"dependent": "y", "predictors": ["a"],
                                  "observations": [{"y": 2.0 * i - 5.0, "a": float(i)}
                                                   for i in range(1, 41)]})
    assert_true("negative-intercept warning fires",
                any("negative intercept" in w for w in negative_intercept["warnings"]))

    # Cross-market comparison: 6x EBITDA reads differently by region.
    six_times = locate({"table": "regional_ev_ebitda_median_2021", "value": 6.0})
    us = next(r for r in six_times["comparison"] if r["group"] == "United States")
    japan = next(r for r in six_times["comparison"] if r["group"] == "Japan")
    assert_true("6x EBITDA is far below the US median but close to Japan's",
                us["value_over_median"] < 0.4 and japan["value_over_median"] > 0.65)

    # --- Multi-business tests: sum of the parts -----------------------------------
    # United Technologies, 2009, priced division by division off each sector's own
    # regression. Segment EBIT here is already net of corporate G&A in the packet's
    # pricing table, so nothing is capitalized in this run.
    utc = sum_of_parts({
        "name": "United Technologies", "tax_rate": 0.38,
        "market_enterprise_value": 52261.0, "divisions": UTC_DIVISIONS,
        "corporate": {"corporate_costs_already_allocated": True}})
    by_division = {r["division"]: r for r in utc["divisions"]}
    check("Carrier's predicted EV/EBITDA from the refrigeration regression",
          by_division["Carrier"]["multiple"], 5.92, 1e-3)
    check("Carrier's value", by_division["Carrier"]["value"], 8944.47, 1e-3)
    check("Pratt & Whitney's value on EV/Revenues",
          by_division["Pratt & Whitney"]["value"], 26553.29, 1e-3)
    check("Otis's value", by_division["Otis"]["value"], 19601.70, 1e-3)
    check("UTC Fire & Security's value on EV/Capital",
          by_division["UTC Fire & Security"]["value"], 5828.76, 1e-3)
    check("Hamilton Sundstrand's value", by_division["Hamilton Sundstrand"]["value"],
          9902.44, 1e-3)
    check("Sikorsky's value", by_division["Sikorsky"]["value"], 3509.61, 1e-3)
    # The packet's own per-division figures sum to a shade more than its stated total, so
    # the sum is checked at 0.2% rather than at the 0.1% used on each division.
    check("UTC sum of the parts on the pricing route", utc["sum_of_division_values"],
          74230.37, 2e-3)
    check("division contributions sum to exactly 1",
          sum(r["share_of_sum_of_parts"] for r in utc["divisions"]), 1.0, 1e-12)

    # The zero-growth rule. Fire & Security earns 6.03% against a 6.78% cost of capital,
    # so it gets no high-growth period; Carrier earns 13.57% against 7.84% and gets five.
    assert_true("a division earning below its cost of capital gets no high-growth period",
                by_division["UTC Fire & Security"]["fundamentals"]
                ["high_growth_years_allowed"] == 0)
    assert_true("and that division is named in the warnings",
                any("UTC Fire & Security" in w and "zero-year" in w
                    for w in utc["warnings"]))
    assert_true("a division that out-earns its cost of capital keeps its growth period",
                by_division["Carrier"]["fundamentals"]["high_growth_years_allowed"] == 5)

    # The conglomerate discount is reported as an observed gap, never applied.
    check("UTC's gap to the market's enterprise value",
          utc["gap_to_market_enterprise_value"], 0.2960, 1e-2)
    assert_true("nothing is discounted for the gap",
                utc["value_of_operating_assets"] == utc["sum_of_division_values"])
    refuses("a caller-supplied conglomerate discount is refused",
            lambda: sum_of_parts({"conglomerate_discount": 0.30,
                                  "divisions": UTC_DIVISIONS,
                                  "corporate": {"corporate_costs_already_allocated": True}}),
            "observed in prices")

    # Unallocated corporate overhead: UTC's $408M at a 38% tax rate, an 8.68% company cost
    # of capital and 3% stable growth. A wrong implementation that drops the (1 - t) or the
    # (1 + g) lands hundreds of millions away.
    drag = capitalized_corporate_expense(408.0, 0.38, 0.0868, 0.03)
    check("capitalized value of UTC's unallocated corporate expenses", drag, 4587.0, 1e-3)
    check("UTC's DCF sum of the parts is net of that drag", 80250.0 - drag, 75663.0, 1e-3)
    utc_net = sum_of_parts({
        "tax_rate": 0.38, "company_cost_of_capital": 0.0868, "stable_growth": 0.03,
        "divisions": UTC_DIVISIONS,
        "corporate": {"corporate_expenses": 408.0}})
    check("the pipeline subtracts the same drag from the sum",
          utc_net["value_of_operating_assets"],
          utc["sum_of_division_values"] - drag, 1e-12)
    refuses("overhead that is neither allocated nor capitalized is refused",
            lambda: sum_of_parts({"divisions": UTC_DIVISIONS, "corporate": {}}),
            "silently overstates the total")
    refuses("allocating and capitalizing the same overhead is refused",
            lambda: sum_of_parts({"divisions": UTC_DIVISIONS,
                                  "corporate": {"corporate_expenses": 408.0,
                                                "corporate_costs_already_allocated": True}}),
            "charges it twice")

    # GE, 2018 analysis of 2017 data. Segment EBITDA is built from normalised EBIT plus
    # D&A, and the bridge carries the finance arm's debt separately from industrial debt.
    ge = sum_of_parts({
        "name": "GE", "divisions": GE_SEGMENTS,
        "corporate": {"corporate_costs_already_allocated": True,
                      "cash": 43299.0, "debt": 83568.0, "financing_arm_debt": 51023.0,
                      "minority_interests": 17723.0, "option_value": 218.94,
                      # Implied by the packet's per-share figure.
                      "shares_outstanding": 8681.88}})
    ge_by_division = {r["division"]: r for r in ge["divisions"]}
    check("GE Power's EBITDA is normalised EBIT plus D&A",
          ge_by_division["Power"]["scalar_value"], 5419.80)
    check("GE Power priced at the peer group's EV/EBITDA",
          ge_by_division["Power"]["value"], 57179.0, 1e-3)
    check("GE Aviation priced at its own, much lower, peer multiple",
          ge_by_division["Aviation"]["value"], 40595.0, 1e-3)
    # The source's segment values are quoted to the nearest dollar, so the bridge is
    # checked against its printed totals at that precision rather than to the cent.
    check("GE equity after the bridge", ge["bridge"]["value_of_equity"], 103012.44, 1e-6)
    check("GE common stock after employee options",
          ge["bridge"]["value_of_common_stock"], 102793.50, 1e-6)
    # Options are subtracted before the division, not after. Dividing the equity value
    # instead gives $11.87, which is what this test is here to catch.
    check("GE value per share", ge["value_per_share"], 11.84, 1e-3)

    # An equity multiple cannot be mixed into an enterprise-level sum.
    mixed = sum_of_parts({
        "divisions": [{"name": "Finance arm", "scalar": "net_income", "scalar_value": 500.0,
                       "multiple": 12.0, "multiple_class": "equity"},
                      {"name": "Industrial", "scalar": "ebitda", "scalar_value": 1000.0,
                       "multiple": 8.0}],
        "corporate": {"corporate_costs_already_allocated": True}})
    equity_row = next(r for r in mixed["divisions"] if r["division"] == "Finance arm")
    assert_true("an equity-level part is refused rather than added to the sum",
                equity_row["status"] == "refused" and "value" not in equity_row)
    assert_true("and the partial total says so",
                any("were refused" in w for w in mixed["warnings"]))
    # A loss-making segment gets no value from a positive multiple, and an unrecognised
    # scalar is named rather than silently skipped.
    loss_segment = _value_division({"name": "Oil & Gas", "scalar": "ebitda",
                                    "scalar_value": -310.0, "peer_multiple": 12.15}, 0, 0.38)
    assert_true("a negative segment scalar is refused, not multiplied",
                loss_segment["status"] == "refused" and "value" not in loss_segment)
    unknown_scalar = _value_division({"name": "X", "scalar": "gross profit",
                                      "scalar_value": 100.0, "multiple": 8.0}, 0, 0.38)
    assert_true("an unrecognised scalar is refused with the list of usable ones",
                unknown_scalar["status"] == "refused"
                and "invested_capital" in unknown_scalar["reason"])

    # --- Multi-business tests: cross holdings -------------------------------------
    # The three-part exercise. Company A is worth $1,000m on consolidated financials with
    # $200m of debt, owns 10% of B (market cap $500m) and 60% of C (minority interest
    # booked at $40m).
    shortcut = cross_holdings({
        "name": "Company A", "frame": "pricing", "parent_value": 1000.0,
        "parent_debt": 200.0,
        "holdings": [
            {"name": "Company B", "ownership": 0.10, "consolidated": False,
             "market_value_of_stake": 50.0},
            {"name": "Company C", "ownership": 0.60, "consolidated": True,
             "minority_interest_book": 40.0, "sector_price_to_book": 1.0}]})
    check("book/market shortcut gives equity of 810", shortcut["value_of_equity"], 810.0)
    check("the 10% stake is added at market",
          shortcut["value_of_minority_holdings"], 50.0)
    check("the 60% stake takes out the minority interest",
          shortcut["market_value_of_minority_interest"], 40.0)

    # The same firm with intrinsic values for both subsidiaries: B's equity at $250m
    # (half the market's $500m) and C's at $250m.
    intrinsic_route = cross_holdings({
        "name": "Company A", "parent_value": 1000.0, "parent_debt": 200.0,
        "holdings": [
            {"name": "Company B", "ownership": 0.10, "consolidated": False,
             "subsidiary_equity_value": 250.0},
            {"name": "Company C", "ownership": 0.60, "consolidated": True,
             "subsidiary_equity_value": 250.0}]})
    check("intrinsic treatment gives equity of 725",
          intrinsic_route["value_of_equity"], 725.0)
    assert_true("the intrinsic answer is $85m below the shortcut",
                abs((shortcut["value_of_equity"] - intrinsic_route["value_of_equity"])
                    - 85.0) < 1e-9)

    # The sign is the whole point: a consolidated stake reduces value, an unconsolidated
    # one raises it. An implementation that adds both lands on $925m instead of $725m.
    c_row = next(r for r in intrinsic_route["holdings"] if r["holding"] == "Company C")
    b_row = next(r for r in intrinsic_route["holdings"] if r["holding"] == "Company B")
    assert_true("the majority stake is subtracted and the minority stake added",
                c_row["signed_contribution"] < 0 < b_row["signed_contribution"])
    check("the minority interest is 40% of C's equity value",
          c_row["minority_interest_value"], 100.0)
    check("composition percentages account for the whole firm",
          sum(intrinsic_route["composition_percentages"].values()), 1.0, 1e-12)

    # Yahoo as the sum of its intrinsic pieces ($ millions), including the tax due on the
    # unrealised gains and the value of Yahoo's own options.
    yahoo = cross_holdings({
        "name": "Yahoo!", "taxes_due": 5017.0, "option_value": 298.0,
        "holdings": [
            {"name": "Yahoo! US", "ownership": 1.0, "consolidated": False,
             "subsidiary_equity_value": 7363.0},
            {"name": "Yahoo! Japan", "ownership": 0.35, "consolidated": False,
             "subsidiary_equity_value": 20997.0},
            {"name": "Alibaba", "ownership": 0.221, "consolidated": False,
             "subsidiary_equity_value": 145587.0}]})
    check("Yahoo's holdings before tax and options",
          yahoo["value_of_minority_holdings"], 7363.0 + 0.35 * 20997.0 + 0.221 * 145587.0,
          1e-12)
    check("Yahoo's equity value after tax on the stakes",
          yahoo["value_of_equity"], yahoo["value_of_minority_holdings"] - 5017.0, 1e-12)
    # The source prints $41,571m and $41.19 per share; the arithmetic lands 68 cents above
    # its rounded total, which is why this one is checked at four figures.
    check("Yahoo's common stock after its own options",
          yahoo["value_of_common_stock"], 41571.0, 1e-4)

    # The Ginzu cross-holdings sheet: one traded minority stake and one unlisted holding
    # carried at book times its sector's price-to-book.
    ginzu = cross_holdings({
        "holdings": [
            {"name": "Traded minority stake", "ownership": 0.176, "consolidated": False,
             "subsidiary_equity_value": 4806.0},
            {"name": "Unlisted holding", "ownership": 1.0, "consolidated": False,
             "book_equity": 329.8, "sector_price_to_book": 1.1}]})
    ginzu_rows = {r["holding"]: r for r in ginzu["holdings"]}
    check("traded minority stake at 17.6% of the subsidiary's equity value",
          ginzu_rows["Traded minority stake"]["stake_value"], 845.856, 1e-9)
    check("unlisted holding at book times the sector price-to-book",
          ginzu_rows["Unlisted holding"]["stake_value"], 362.78, 1e-9)

    # Book minority interest is not market value, and the engine will not pretend it is.
    book_only = cross_holdings({
        "holdings": [{"name": "Sub", "ownership": 0.60, "consolidated": True,
                      "minority_interest_book": 40.0}]})
    assert_true("book minority interest with no price-to-book is refused",
                book_only["holdings"][0]["status"] == "refused"
                and "far too low" in book_only["holdings"][0]["reason"])
    percent_stake = cross_holdings({
        "holdings": [{"name": "Sub", "ownership": 60, "consolidated": True,
                      "subsidiary_equity_value": 250.0}]})
    assert_true("an ownership stake entered as a percentage is refused",
                percent_stake["holdings"][0]["status"] == "refused")
    refuses("cross-holdings with no holdings explains what to pass",
            lambda: cross_holdings({"holdings": []}), "decimal fraction")

    failed = [r for r in results if not r["pass"]]
    _emit({"total": len(results), "passed": len(results) - len(failed),
           "failed": len(failed), "results": results})
    return 1 if failed else 0


# ------------------------------------------------------------------------------- main

COMMANDS = {
    "multiples": cmd_multiples,
    "peer-stats": cmd_peer_stats,
    "locate": cmd_locate,
    "intrinsic": cmd_intrinsic,
    "regress": cmd_regress,
    "predict": cmd_predict,
    "sum-of-parts": cmd_sum_of_parts,
    "cross-holdings": cmd_cross_holdings,
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
        _emit(EXAMPLES[args.command])
        return 0
    return COMMANDS[args.command](args) or 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except json.JSONDecodeError as exc:
        raise SystemExit("Input is not valid JSON (%s). Run the subcommand with "
                         "--example to see the expected shape." % exc)
    except KeyError as exc:
        raise SystemExit("Required field %s is missing from the payload. Run the "
                         "subcommand with --example to see the expected shape." % exc)

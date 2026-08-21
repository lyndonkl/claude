#!/usr/bin/env python3
"""
payout.py — the payout policy engine.

Answers three questions in sequence. How much cash did the firm return? How much could
it have returned? And does the record justify letting management keep the difference?
The first two are arithmetic. The third is scored here and judged by the analyst.

Every function is a pure numeric transform. The window, the debt ratio, the growth
assumptions and the peer group are the analyst's calls and arrive as inputs.

Pure standard library. No third-party packages, ever — this must run anywhere.

SUBCOMMANDS
  fcfe-history    a history of statements -> FCFE (3 variants) against cash returned
  trust           ROE, CAPM required return and Jensen's alpha -> the trust verdict
  matrix          cash verdict + quality verdict -> the dividend matrix quadrant
  sustainability  base year and growth rates -> projected FCFE, dividends, buyback capacity
  peers           a peer group -> yield, payout and cash-return percentiles
  market-norms    beta, growth and leverage -> the payout and yield the market predicts
  bank-fcfe       regulatory capital projections -> FCFE for a bank or insurer
  selftest        run the bundled worked examples and report pass/fail

Each subcommand reads a JSON payload (--in FILE, or stdin) and writes JSON to stdout.
Run any subcommand with --example to print a sample input payload.
"""

import argparse
import json
import os
import statistics
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DEFAULT_BENCHMARKS = os.path.join(DATA_DIR, "payout_benchmarks.json")
DEFAULT_REGRESSIONS = os.path.join(DATA_DIR, "payout_regressions.json")

# Damodaran's dividends.xls accepts 1 to 10 years of history. One year is dominated by
# lumpy cap ex and debt issuance; past ten the business has usually changed identity.
MIN_WINDOW_YEARS = 1
MAX_WINDOW_YEARS = 10

# The forward model in the same workbook runs five years. Longer horizons turn a capacity
# bound into a valuation, which this script deliberately does not do.
DEFAULT_FORECAST_YEARS = 5

# Bisection on the sustainable dividend growth rate: the gap function is monotonic in the
# growth rate, so ~80 passes exhaust double precision. 200 is a ceiling that still returns
# promptly on a pathological input.
MAX_SOLVER_ITERATIONS = 200
SOLVER_TOLERANCE = 1e-12
# A dividend shrinking faster than 90% a year is not a policy anyone would recommend, and
# growth above 100% a year cannot be sustained by any firm; these bound the search.
GROWTH_SEARCH_LOW = -0.90
GROWTH_SEARCH_HIGH = 1.00


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
        raise SystemExit("Input is not valid JSON (%s). Check for trailing commas or "
                         "unquoted keys, or run with --example to see the shape." % exc)


def _emit(obj):
    print(json.dumps(obj, indent=2))


def _num(payload, key, where, default=None):
    """Fetch a numeric field, or explain precisely which one is missing or malformed."""
    if key not in payload or payload[key] is None:
        if default is not None:
            return float(default)
        raise SystemExit(
            "%s is missing the field %r. Run this subcommand with --example to see every "
            "field it expects." % (where, key))
    try:
        return float(payload[key])
    except (TypeError, ValueError):
        raise SystemExit("%s: %r must be a number, got %r." % (where, key, payload[key]))


def _load_json(path, default_path, label):
    try:
        with open(path or default_path) as f:
            return json.load(f)
    except IOError:
        raise SystemExit("Could not read the %s file at %r." % (label, path or default_path))


def _safe_ratio(numerator, denominator, reason_when_undefined):
    """Ratios in this domain go meaningless, not merely large, when the base turns.

    A payout ratio on negative earnings and a cash-to-FCFE ratio on negative FCFE are both
    reported as null with a stated reason, never as a negative number that reads like a
    result.
    """
    if denominator is None or denominator <= 0:
        return None, reason_when_undefined
    return numerator / denominator, None


def _mean(values):
    return sum(values) / len(values) if values else None


def _median(values):
    return statistics.median(values) if values else None


def _check_debt_ratio(dr, where):
    if not 0.0 <= dr < 1.0:
        raise SystemExit(
            "%s: debt_ratio is %.4f. It is debt as a fraction of capital, "
            "Debt / (Debt + Equity), so it belongs in [0, 1). A ratio of 1 leaves no "
            "equity to fund reinvestment." % (where, dr))
    return dr


# ------------------------------------------------------------------- FCFE over history

def fcfe_year(net_income, depreciation, capex, change_in_wc, net_debt_issued,
              debt_ratio, preferred_dividends=0.0):
    """The three FCFE variants for one year.

    They differ only in how reinvestment is assumed to be financed. Pre-debt ignores debt
    cash flows; actual-debt uses what the firm really borrowed; target-debt-ratio assumes a
    constant fraction of reinvestment came from debt. The three routinely disagree, and the
    disagreement is itself the finding.
    """
    net_capex = capex - depreciation
    reinvestment = net_capex + change_in_wc
    predebt = net_income - reinvestment - preferred_dividends
    return {
        "net_capex": net_capex,
        "reinvestment": reinvestment,
        "fcfe_predebt": predebt,
        "fcfe_actual_debt": predebt + net_debt_issued,
        "fcfe_target_debt_ratio": net_income - preferred_dividends
                                  - reinvestment * (1.0 - debt_ratio),
        # The equity reinvestment view of the same arithmetic: what shareholders funded.
        "equity_reinvestment": reinvestment - net_debt_issued,
    }


def fcfe_history(payload):
    years = payload.get("years")
    if not isinstance(years, list) or not years:
        raise SystemExit(
            "fcfe-history needs a non-empty 'years' array, most recent year first. "
            "Run with --example to see one year's shape.")
    if not MIN_WINDOW_YEARS <= len(years) <= MAX_WINDOW_YEARS:
        raise SystemExit(
            "fcfe-history was given %d years. Use between %d and %d. A single year is "
            "dominated by lumpy cap ex and borrowing; beyond ten the business has usually "
            "changed identity." % (len(years), MIN_WINDOW_YEARS, MAX_WINDOW_YEARS))

    dr = _check_debt_ratio(_num(payload, "debt_ratio", "fcfe-history"), "fcfe-history")
    rows = []
    for i, y in enumerate(years):
        where = "fcfe-history year %s" % (y.get("label") or i + 1)
        ni = _num(y, "net_income", where)
        pref = _num(y, "preferred_dividends", where, 0.0) if "preferred_dividends" in y else 0.0
        row = fcfe_year(
            ni,
            _num(y, "depreciation", where, 0.0) if "depreciation" in y else 0.0,
            _num(y, "capex", where),
            _num(y, "change_in_noncash_wc", where, 0.0) if "change_in_noncash_wc" in y else 0.0,
            _num(y, "net_debt_issued", where, 0.0) if "net_debt_issued" in y else 0.0,
            dr, pref)
        dividends = _num(y, "dividends", where, 0.0) if "dividends" in y else 0.0
        buybacks = _num(y, "buybacks", where, 0.0) if "buybacks" in y else 0.0
        cash = dividends + buybacks
        payout, payout_na = _safe_ratio(dividends, ni, "net income is not positive")
        cash_pct, cash_na = _safe_ratio(cash, row["fcfe_actual_debt"],
                                        "actual-debt FCFE is not positive")
        reinv_rate, reinv_na = _safe_ratio(row["equity_reinvestment"], ni,
                                           "net income is not positive")
        rows.append({
            "label": y.get("label") or "year %d" % (i + 1),
            "net_income": ni, "dividends": dividends, "buybacks": buybacks,
            "cash_returned": cash,
            **row,
            "equity_reinvestment_rate": reinv_rate,
            "equity_reinvestment_rate_note": reinv_na,
            "dividend_payout_ratio": payout, "dividend_payout_ratio_note": payout_na,
            "cash_pct_of_actual_fcfe": cash_pct, "cash_pct_of_actual_fcfe_note": cash_na,
        })

    def total(key):
        return sum(r[key] for r in rows)

    n = len(rows)
    agg = {k: total(k) for k in ("net_income", "dividends", "buybacks", "cash_returned",
                                 "reinvestment", "equity_reinvestment", "fcfe_predebt",
                                 "fcfe_actual_debt", "fcfe_target_debt_ratio")}
    averages = {k: v / n for k, v in agg.items()}

    comparison = {}
    for variant in ("fcfe_predebt", "fcfe_actual_debt", "fcfe_target_debt_ratio"):
        pct, na = _safe_ratio(agg["cash_returned"], agg[variant],
                              "aggregate %s is not positive, so the ratio is meaningless; "
                              "read the surplus in currency instead" % variant)
        comparison[variant] = {
            "aggregate_fcfe": agg[variant],
            "surplus_or_deficit": agg[variant] - agg["cash_returned"],
            "cash_returned_pct_of_fcfe": pct,
            "note": na,
            # A cash accumulator has positive FCFE and returns less than it; everything
            # else — including any payout on negative FCFE — is a cash overpayer.
            "classification": ("accumulator"
                               if agg[variant] > 0 and agg["cash_returned"] <= agg[variant]
                               else "overpayer"),
        }

    div_payout_agg, div_na = _safe_ratio(agg["dividends"], agg["net_income"],
                                         "aggregate net income is not positive")
    cash_payout_agg, cash_na = _safe_ratio(agg["cash_returned"], agg["net_income"],
                                           "aggregate net income is not positive")
    annual_payouts = [r["dividend_payout_ratio"] for r in rows
                      if r["dividend_payout_ratio"] is not None]
    buyback_share, bb_na = _safe_ratio(agg["buybacks"], agg["cash_returned"],
                                       "no cash was returned")
    equity_reinv_rate, er_na = _safe_ratio(agg["equity_reinvestment"], agg["net_income"],
                                           "aggregate net income is not positive")

    classes = {comparison[v]["classification"] for v in comparison}
    return {
        "currency": payload.get("currency"),
        "debt_ratio": dr,
        "debt_ratio_basis": payload.get("debt_ratio_basis", "unstated — say whether this is "
                                        "the current market debt-to-capital ratio or a target"),
        "years_used": n,
        "annual": rows,
        "aggregate": agg,
        "average_per_year": averages,
        "dividend_payout_ratio_aggregate": div_payout_agg,
        "dividend_payout_ratio_aggregate_note": div_na,
        "dividend_payout_ratio_mean_of_annual": _mean(annual_payouts),
        "cash_payout_ratio_aggregate": cash_payout_agg,
        "cash_payout_ratio_aggregate_note": cash_na,
        "buyback_share_of_cash_returned": buyback_share,
        "buyback_share_note": bb_na,
        "equity_reinvestment_rate_aggregate": equity_reinv_rate,
        "equity_reinvestment_rate_note": er_na,
        "comparison": comparison,
        "default_variant": "fcfe_target_debt_ratio",
        "default_variant_reason": "Target-debt-ratio FCFE is the sustainable measure. "
                                  "Actual-debt FCFE counts one-off borrowing as payout "
                                  "capacity, which flatters an acquisitive, debt-funded firm.",
        "variants_agree": len(classes) == 1,
        "variants_disagree_warning": None if len(classes) == 1 else
            "The three FCFE variants do not agree on whether this firm is an accumulator or "
            "an overpayer. State which variant your conclusion rests on and why.",
    }


def cmd_fcfe_history(args):
    _emit(fcfe_history(_read_payload(args)))


# ---------------------------------------------------------------------- trust in mgmt

def trust(payload):
    """Score whether management earned the right to hold back cash.

    Two independent measures. The project measure (ROE against the CAPM required return)
    says whether the investments earned their cost of equity. The market measure (Jensen's
    alpha) says whether the stock beat that same required return. They disagree often
    enough that reporting only one is a mistake.
    """
    years = payload.get("years")
    if not isinstance(years, list) or not years:
        raise SystemExit(
            "trust needs a non-empty 'years' array, most recent year first, each with "
            "net_income, book_equity, stock_return, riskfree_rate and market_return.")
    beta = _num(payload, "beta", "trust")

    rows = []
    for i, y in enumerate(years):
        where = "trust year %s" % (y.get("label") or i + 1)
        ni = _num(y, "net_income", where)
        bv = _num(y, "book_equity", where)
        rf = _num(y, "riskfree_rate", where)
        rm = _num(y, "market_return", where)
        required = rf + beta * (rm - rf)
        roe, roe_na = _safe_ratio(ni, bv, "book equity is not positive, so ROE is meaningless")
        stock_return = (_num(y, "stock_return", where)
                        if "stock_return" in y and y["stock_return"] is not None else None)
        rows.append({
            "label": y.get("label") or "year %d" % (i + 1),
            "net_income": ni, "book_equity": bv,
            "roe": roe, "roe_note": roe_na,
            "required_return": required,
            "excess_roe": None if roe is None else roe - required,
            "stock_return": stock_return,
            "jensens_alpha": None if stock_return is None else stock_return - required,
        })

    n = len(rows)
    sum_ni = sum(r["net_income"] for r in rows)
    sum_bv = sum(r["book_equity"] for r in rows)
    roe_ratio_of_sums, ros_na = _safe_ratio(sum_ni, sum_bv,
                                            "aggregate book equity is not positive")
    annual_roes = [r["roe"] for r in rows if r["roe"] is not None]
    alphas = [r["jensens_alpha"] for r in rows if r["jensens_alpha"] is not None]
    stock_returns = [r["stock_return"] for r in rows if r["stock_return"] is not None]
    avg_required = _mean([r["required_return"] for r in rows])

    method = payload.get("roe_average_method", "ratio_of_sums")
    if method not in ("ratio_of_sums", "mean_of_annual"):
        raise SystemExit("roe_average_method must be 'ratio_of_sums' or 'mean_of_annual'.")
    average_roe = roe_ratio_of_sums if method == "ratio_of_sums" else _mean(annual_roes)

    out = {
        "beta": beta,
        "years_used": n,
        "annual": rows,
        "average_roe": average_roe,
        "average_roe_method": method,
        "average_roe_ratio_of_sums": roe_ratio_of_sums,
        "average_roe_ratio_of_sums_note": ros_na,
        "average_roe_mean_of_annual": _mean(annual_roes),
        "average_required_return": avg_required,
        "average_stock_return": _mean(stock_returns),
        "average_jensens_alpha": _mean(alphas),
    }

    # Damodaran's dividends.xls sums net income and book equity over all ten input rows when
    # it averages ROE, ignoring the selected window, while every other statistic respects it.
    # Supplying the rows outside the window reproduces that figure so a port can be compared
    # against the sheet; the corrected number above is the one to report.
    extra = payload.get("extra_years_for_legacy_roe")
    if extra:
        legacy_ni = sum_ni + sum(_num(e, "net_income", "legacy ROE row") for e in extra)
        legacy_bv = sum_bv + sum(_num(e, "book_equity", "legacy ROE row") for e in extra)
        legacy, legacy_na = _safe_ratio(legacy_ni, legacy_bv,
                                        "aggregate book equity is not positive")
        out["legacy_average_roe_all_input_rows"] = legacy
        out["legacy_average_roe_note"] = legacy_na or (
            "Reproduces the dividends.xls quirk of averaging ROE over all input rows rather "
            "than the selected window. Report average_roe, not this.")

    excess = None if average_roe is None else average_roe - avg_required
    alpha = out["average_jensens_alpha"]
    out["roe_minus_required_return"] = excess
    out["stock_return_minus_required_return"] = alpha

    if excess is None:
        verdict, note = "undetermined", "ROE could not be computed; supply positive book equity."
    elif excess > 0 and (alpha is None or alpha > 0):
        verdict = "good_projects"
        note = ("Management earned more than the cost of equity and the stock kept up. "
                "The record supports leaving the payout decision to management.")
    elif excess <= 0 and (alpha is not None and alpha <= 0):
        verdict = "poor_projects"
        note = ("Both measures are negative. Expect and support pressure to return the cash; "
                "management has not earned the right to hold it.")
    else:
        verdict = "mixed"
        note = ("The two measures disagree. Weight the project measure for the payout "
                "decision — the stock measure includes market-wide revaluation management "
                "did not create — and say which one you relied on.")
    out["project_quality_verdict"] = verdict
    out["verdict_note"] = note
    out["caution"] = ("Book equity is distorted by buybacks, write-offs and acquisition "
                      "accounting, so a low ROE at an acquisitive firm may be an accounting "
                      "artifact rather than a verdict on the investments.")
    return out


def cmd_trust(args):
    _emit(trust(_read_payload(args)))


# ------------------------------------------------------------------- the dividend matrix

# Row = cash axis, column = project-quality axis. Prescriptions are Damodaran's.
MATRIX = {
    ("surplus", "poor"): (
        "pay_out_more",
        "Heavy pressure to pay out more, as dividends or buybacks.",
        "Management has not earned the right to hold the cash. Support stockholder pressure "
        "to return it, and expect activists if the balance is large."),
    ("surplus", "good"): (
        "maximum_flexibility",
        "Maximum flexibility in setting payout policy.",
        "A firm earning excess returns has earned the freedom to hold cash, raise the "
        "dividend, or buy back stock as it sees fit."),
    ("deficit", "poor"): (
        "cut_payout_and_fix_investment",
        "Cut or end the cash return — but the real problem is investment policy.",
        "Sequence matters: fix the investment policy first, then cut. A cut on its own "
        "leaves the value destruction untouched."),
    ("deficit", "good"): (
        "reduce_payout_to_fund_projects",
        "Reduce the cash payout so the firm can fund its investments internally.",
        "The projects are worth funding; the payout is what has to give. Cutting lets the "
        "firm avoid issuing equity at a flotation cost."),
}


def matrix(payload):
    fcfe = _num(payload, "fcfe", "matrix")
    cash = _num(payload, "cash_returned", "matrix")
    ke = _num(payload, "cost_of_equity", "matrix")
    roe = payload.get("roe")
    if roe is None:
        raise SystemExit(
            "matrix needs 'roe' — the average return on equity over the same window as the "
            "FCFE figure. Get it from the trust subcommand's average_roe, or from "
            "financial-statement-normalization's ratios subcommand.")
    roe = float(roe)

    cash_axis = "surplus" if cash < fcfe else "deficit"
    excess_roe = roe - ke
    quality_signals = {"roe_minus_cost_of_equity": excess_roe}
    good = excess_roe > 0

    roc = payload.get("roc")
    kc = payload.get("cost_of_capital")
    if roc is not None and kc is not None:
        excess_roc = float(roc) - float(kc)
        quality_signals["roc_minus_cost_of_capital"] = excess_roc
        # Damodaran's rule is ROE above the cost of equity and/or ROC above the cost of
        # capital; either clearing the bar counts as good projects.
        good = good or excess_roc > 0
    alpha = payload.get("jensens_alpha")
    if alpha is not None:
        quality_signals["jensens_alpha"] = float(alpha)

    quality_axis = "good" if good else "poor"
    key, prescription, sequencing = MATRIX[(cash_axis, quality_axis)]
    pct, pct_na = _safe_ratio(cash, fcfe,
                              "FCFE is not positive, so cash paid as a percentage of FCFE "
                              "is meaningless; the firm returned cash it did not generate")

    disagreement = None
    signs = [v > 0 for k, v in quality_signals.items() if v is not None]
    if len(set(signs)) > 1:
        disagreement = ("The project-quality signals disagree. The accounting measures (ROE, "
                        "ROC) speak to the investments; Jensen's alpha includes market-wide "
                        "revaluation. Lead with the project measure and state the conflict.")

    return {
        "currency": payload.get("currency"),
        "fcfe": fcfe,
        "fcfe_variant": payload.get("fcfe_variant", "unstated — name the variant, because the "
                                    "quadrant can change with it"),
        "cash_returned": cash,
        "surplus_or_deficit": fcfe - cash,
        "cash_returned_pct_of_fcfe": pct,
        "cash_returned_pct_of_fcfe_note": pct_na,
        "cash_axis": cash_axis,
        "quality_axis": quality_axis,
        "quality_signals": quality_signals,
        "quality_signals_disagree": disagreement,
        "quadrant": "%s / %s projects" % (cash_axis, quality_axis),
        "verdict": key,
        "prescription": prescription,
        "sequencing": sequencing,
        "magnitude_note": ("Cash paid as a percentage of FCFE far from 100% in either "
                           "direction is what makes the fix urgent. Near 100% the "
                           "quadrant label matters less than it looks."),
        "re_run_note": "Firms move between quadrants. Re-run annually.",
    }


def cmd_matrix(args):
    _emit(matrix(_read_payload(args)))


# ------------------------------------------------------------------------ sustainability

def _forecast_rows(p, dividend_growth):
    """Project FCFE and dividends forward under constant growth rates."""
    years = int(p.get("forecast_years", DEFAULT_FORECAST_YEARS))
    dr = p["_debt_ratio"]
    rows = []
    prev_revenue = p["revenues"]
    for t in range(1, years + 1):
        revenue = p["revenues"] * (1 + p["growth_revenues"]) ** t
        ni = p["net_income"] * (1 + p["growth_net_income"]) ** t
        capex = p["capex"] * (1 + p["growth_capex"]) ** t
        depreciation = p["depreciation"] * (1 + p["growth_depreciation"]) ** t
        # Working capital reinvestment is driven by the revenue *increment*, not the level.
        # Multiplying the level by the percentage gives the balance and overstates
        # reinvestment by an order of magnitude.
        delta_wc = p["wc_pct_revenues"] * (revenue - prev_revenue)
        net_capex_equity = (capex - depreciation) * (1 - dr)
        wc_equity = delta_wc * (1 - dr)
        fcfe = ni - net_capex_equity - wc_equity
        dividends = p["dividends"] * (1 + dividend_growth) ** t
        rows.append({
            "year": t, "revenues": revenue, "net_income": ni,
            "capex": capex, "depreciation": depreciation,
            "change_in_noncash_wc": delta_wc,
            "net_capex_funded_by_equity": net_capex_equity,
            "wc_funded_by_equity": wc_equity,
            "fcfe": fcfe, "expected_dividends": dividends,
            "cash_available_for_buybacks": fcfe - dividends,
        })
        prev_revenue = revenue
    return rows


def sustainability(payload):
    p = {}
    for key in ("revenues", "net_income", "capex", "depreciation", "dividends"):
        p[key] = _num(payload, key, "sustainability")
    for key in ("growth_revenues", "growth_net_income", "growth_capex",
                "growth_depreciation", "growth_dividends"):
        p[key] = _num(payload, key, "sustainability")
    p["wc_pct_revenues"] = _num(payload, "wc_pct_revenues", "sustainability")
    p["forecast_years"] = int(payload.get("forecast_years", DEFAULT_FORECAST_YEARS))
    if p["forecast_years"] < 1:
        raise SystemExit("forecast_years must be at least 1.")
    p["_debt_ratio"] = _check_debt_ratio(_num(payload, "debt_ratio", "sustainability"),
                                         "sustainability")
    for key in ("growth_revenues", "growth_net_income", "growth_capex",
                "growth_depreciation", "growth_dividends", "wc_pct_revenues"):
        if abs(p[key]) > 1.0:
            raise SystemExit(
                "%s is %.4f. These are decimals, not percentages — 5%% is 0.05, not 5."
                % (key, p[key]))

    rows = _forecast_rows(p, p["growth_dividends"])
    gaps = [r["cash_available_for_buybacks"] for r in rows]
    first_shortfall = next((r["year"] for r in rows
                            if r["cash_available_for_buybacks"] < 0), None)
    coverage = []
    for r in rows:
        ratio, _ = _safe_ratio(r["fcfe"], r["expected_dividends"], "no dividend projected")
        coverage.append(ratio)

    def min_gap(g):
        return min(r["cash_available_for_buybacks"] for r in _forecast_rows(p, g))

    # Dividends are monotonically increasing in the growth rate and FCFE does not depend on
    # it, so the minimum gap falls monotonically in g and bisection is exact.
    max_growth = None
    max_growth_note = None
    if min_gap(GROWTH_SEARCH_HIGH) >= 0:
        max_growth_note = ("Projected FCFE covers the dividend even at %.0f%% annual growth; "
                           "the constraint is not binding in this horizon."
                           % (GROWTH_SEARCH_HIGH * 100))
    elif min_gap(GROWTH_SEARCH_LOW) < 0:
        max_growth_note = ("Projected FCFE cannot cover the dividend at any growth rate down "
                           "to %.0f%%, so the current dividend level itself is unaffordable. "
                           "The question is how deep the cut has to be, not how fast the "
                           "dividend can grow." % (GROWTH_SEARCH_LOW * 100))
    else:
        lo, hi = GROWTH_SEARCH_LOW, GROWTH_SEARCH_HIGH
        for _ in range(MAX_SOLVER_ITERATIONS):
            mid = (lo + hi) / 2.0
            if min_gap(mid) >= 0:
                lo = mid
            else:
                hi = mid
            if hi - lo < SOLVER_TOLERANCE:
                break
        max_growth = lo

    sustainable = first_shortfall is None
    return {
        "currency": payload.get("currency"),
        "debt_ratio": p["_debt_ratio"],
        "forecast_years": p["forecast_years"],
        "annual": rows,
        "dividend_coverage_ratio": coverage,
        "total_buyback_capacity": sum(gaps),
        "minimum_annual_buyback_capacity": min(gaps),
        "first_shortfall_year": first_shortfall,
        "dividend_sustainable": sustainable,
        "verdict": ("Projected FCFE covers the dividend in every forecast year; the surplus "
                    "is repurchase capacity."
                    if sustainable else
                    "Projected FCFE falls short of the projected dividend from year %d. The "
                    "shortfall has to come from cash reserves, new debt or new equity."
                    % first_shortfall),
        "max_sustainable_dividend_growth": max_growth,
        "max_sustainable_dividend_growth_note": max_growth_note or (
            "The fastest dividend growth this FCFE path covers in every forecast year. "
            "Above it the firm funds the dividend externally."),
        "reading_note": ("This is a capacity bound under simple growth assumptions, not a "
                         "valuation. A base year with unusual cap ex or working capital "
                         "propagates through every forecast year."),
    }


def cmd_sustainability(args):
    _emit(sustainability(_read_payload(args)))


# ------------------------------------------------------------------------- peer analysis

def _company_ratios(c, where):
    market_cap = _num(c, "market_cap", where)
    net_income = _num(c, "net_income", where)
    dividends = _num(c, "dividends", where, 0.0) if "dividends" in c else 0.0
    buybacks = _num(c, "buybacks", where, 0.0) if "buybacks" in c else 0.0
    fcfe = _num(c, "fcfe", where) if c.get("fcfe") is not None else None
    cash = dividends + buybacks
    yield_, yield_na = _safe_ratio(dividends, market_cap, "market cap is not positive")
    payout, payout_na = _safe_ratio(dividends, net_income, "net income is not positive")
    cash_payout, cp_na = _safe_ratio(cash, net_income, "net income is not positive")
    cash_pct, cash_na = _safe_ratio(cash, fcfe, "FCFE is not positive")
    return {
        "name": c.get("name", where),
        "market_cap": market_cap, "dividends": dividends, "buybacks": buybacks,
        "cash_returned": cash, "net_income": net_income, "fcfe": fcfe,
        "dividend_yield": yield_, "dividend_yield_note": yield_na,
        "dividend_payout": payout, "dividend_payout_note": payout_na,
        "cash_payout_ratio": cash_payout, "cash_payout_ratio_note": cp_na,
        "cash_return_pct_of_fcfe": cash_pct, "cash_return_pct_of_fcfe_note": cash_na,
    }


PEER_METRICS = ("market_cap", "dividends", "buybacks", "cash_returned", "net_income",
                "fcfe", "dividend_yield", "dividend_payout", "cash_payout_ratio",
                "cash_return_pct_of_fcfe")


def peers(payload):
    """Position a firm against comparables on yield, payout and cash-return capacity.

    Averages and medians are taken over the companies where the metric is defined. Treating
    a not-applicable entry as zero — a payout ratio on a loss-maker, a cash-return ratio on
    negative FCFE — drags both statistics toward zero and is the standard way this table
    gets misread.
    """
    firm_in = payload.get("firm")
    if not isinstance(firm_in, dict):
        raise SystemExit("peers needs a 'firm' object with market_cap, dividends, buybacks, "
                         "net_income and fcfe.")
    peer_list = payload.get("peers")
    if not isinstance(peer_list, list) or not peer_list:
        raise SystemExit("peers needs a non-empty 'peers' array. Say in your write-up which "
                         "sector, geography and size filter defined the group — the choice "
                         "drives the answer.")

    firm = _company_ratios(firm_in, "firm")
    rows = [_company_ratios(c, "peer %d" % (i + 1)) for i, c in enumerate(peer_list)]
    # Damodaran's peer tables include the subject firm in the group statistics; excluding it
    # is defensible at a firm large enough to move the average, so it is a switch.
    include_firm = payload.get("include_firm_in_group", True)
    group = ([firm] + rows) if include_firm else rows

    stats = {}
    for metric in PEER_METRICS:
        values = [g[metric] for g in group if g[metric] is not None]
        stats[metric] = {
            "count": len(values),
            "excluded_as_not_applicable": len(group) - len(values),
            "average": _mean(values),
            "median": _median(values),
        }

    position = {}
    for metric in ("dividend_yield", "dividend_payout", "cash_payout_ratio",
                   "cash_return_pct_of_fcfe"):
        if firm[metric] is None:
            position[metric] = {"firm": None, "note": firm[metric + "_note"]}
            continue
        values = [g[metric] for g in group if g[metric] is not None]
        below = sum(1 for v in values if v < firm[metric])
        position[metric] = {
            "firm": firm[metric],
            "group_average": stats[metric]["average"],
            "group_median": stats[metric]["median"],
            "gap_to_average": firm[metric] - stats[metric]["average"],
            "gap_to_median": firm[metric] - stats[metric]["median"],
            "percentile_in_group": below / len(values) if values else None,
        }

    warnings = []
    if stats["fcfe"]["average"] is not None and stats["fcfe"]["average"] <= 0:
        warnings.append("The group's average FCFE is not positive: these firms collectively "
                        "cannot afford any payout. Matching this group is not a target worth "
                        "hitting.")
    if stats["dividend_payout"]["median"] == 0:
        warnings.append("The median peer pays no dividend, so the group average is driven by "
                        "a handful of large payers. Read the median, not the average.")
    if stats["buybacks"]["average"] and stats["dividends"]["average"] and \
            stats["buybacks"]["average"] > stats["dividends"]["average"]:
        warnings.append("The group returns more through buybacks than dividends. A "
                        "dividend-only comparison understates payout across the table.")
    if firm["cash_return_pct_of_fcfe"] is None:
        warnings.append("The firm's own FCFE is not positive, so its cash-return ratio is "
                        "not defined. Read the surplus in currency from fcfe-history.")

    return {
        "group_label": payload.get("group_label", "unstated — name the sector, geography and "
                                   "size filter that defined this group"),
        "firm": firm,
        "peers": rows,
        "group_includes_firm": include_firm,
        "group_size": len(group),
        "group_statistics": stats,
        "firm_position": position,
        "warnings": warnings,
        "reading_note": ("Peer comparison is a cross-check, never a substitute for the "
                         "FCFE analysis. Where the two disagree, the FCFE analysis wins — "
                         "peer matching propagates whatever error the sector shares."),
    }


def cmd_peers(args):
    _emit(peers(_read_payload(args)))


# ------------------------------------------------------------------- market regression

def market_norms(payload):
    reg = _load_json(payload.get("regressions_path"), DEFAULT_REGRESSIONS,
                     "payout regression")
    beta = _num(payload, "beta", "market-norms")
    egr = _num(payload, "expected_growth", "market-norms")
    dcap = _num(payload, "debt_to_capital", "market-norms")
    for name, value in (("expected_growth", egr), ("debt_to_capital", dcap)):
        if abs(value) > 1.0:
            raise SystemExit(
                "%s is %.4f. The regressions take decimals: 14.73%% is 0.1473, not 14.73. "
                "Percentages produce absurd predictions." % (name, value))

    predicted = {}
    for name, eq in reg["equations"].items():
        c = eq["coefficients"]
        value = (eq["intercept"] + c["BETA"] * beta + c["EGR"] * egr + c["DCAP"] * dcap)
        predicted[name] = {"predicted": value, "r_squared": eq["r_squared"]}

    actual_payout = payload.get("actual_payout")
    actual_yield = payload.get("actual_yield")
    if actual_payout is not None:
        predicted["payout"]["actual"] = float(actual_payout)
        predicted["payout"]["gap"] = float(actual_payout) - predicted["payout"]["predicted"]
    if actual_yield is not None:
        predicted["yield"]["actual"] = float(actual_yield)
        predicted["yield"]["gap"] = float(actual_yield) - predicted["yield"]["predicted"]

    overlay = None
    dividends = payload.get("dividends")
    buybacks = payload.get("buybacks")
    net_income = payload.get("net_income")
    market_cap = payload.get("market_cap")
    if dividends is not None and buybacks is not None:
        cash = float(dividends) + float(buybacks)
        cash_payout, cp_na = _safe_ratio(cash, net_income, "net income is not positive") \
            if net_income is not None else (None, "net_income not supplied")
        total_yield, ty_na = _safe_ratio(cash, market_cap, "market cap is not positive") \
            if market_cap is not None else (None, "market_cap not supplied")
        overlay = {
            "cash_returned": cash,
            "cash_payout_ratio": cash_payout, "cash_payout_ratio_note": cp_na,
            "total_yield_including_buybacks": total_yield, "total_yield_note": ty_na,
            "note": ("The regressions are fitted on dividends alone. Compare these "
                     "buyback-inclusive figures with the predictions before concluding the "
                     "firm pays too little."),
        }

    benchmarks = None
    region = payload.get("region")
    if region:
        bench = _load_json(payload.get("benchmarks_path"), DEFAULT_BENCHMARKS, "benchmark")
        table = bench["regional_cash_return"]
        if region not in table["rows"]:
            raise SystemExit("Unknown region %r. Available: %s"
                             % (region, ", ".join(sorted(table["rows"]))))
        benchmarks = {
            "region": region,
            "as_of": bench["as_of"],
            "values": dict(zip(table["columns"], table["rows"][region])),
            "refresh": bench["refresh"],
        }

    return {
        "as_of": reg["as_of"],
        "market": reg["market"],
        "inputs": {"BETA": beta, "EGR": egr, "DCAP": dcap},
        "predictions": predicted,
        "buyback_overlay": overlay,
        "regional_benchmark": benchmarks,
        "caveat": reg["caveat"],
        "precision_note": ("R-squared runs 20-26%, so most of the cross-sectional variation "
                           "is unexplained. Treat the prediction as a central tendency; a gap "
                           "of a few percentage points is noise."),
        "vintage_note": reg["refresh"],
    }


def cmd_market_norms(args):
    _emit(market_norms(_read_payload(args)))


# ---------------------------------------------------------------------------- bank FCFE

def _ramp(start, end, years):
    """Linear path from a starting value to a target over `years` steps.

    Regulators force capital ratios up over a period rather than in one year, and a
    troubled bank's ROE recovers gradually. Both are ramps, not step changes.
    """
    step = (end - start) / years
    return [start + step * t for t in range(1, years + 1)]


def bank_fcfe(payload):
    """FCFE for a bank: net income less the investment in regulatory capital.

    Cap ex and non-cash working capital are meaningless at a firm whose raw material is
    capital, and debt is part of the product rather than a financing choice. What a bank
    cannot pay out is the equity it must retain to support a larger balance sheet.
    """
    if payload.get("mode") == "simple" or "new_loans" in payload:
        net_income = _num(payload, "net_income", "bank-fcfe (simple)")
        old_loans = _num(payload, "old_loans", "bank-fcfe (simple)")
        new_loans = _num(payload, "new_loans", "bank-fcfe (simple)")
        ratio = _num(payload, "capital_ratio", "bank-fcfe (simple)")
        investment = (new_loans - old_loans) * ratio
        return {
            "mode": "simple",
            "currency": payload.get("currency"),
            "net_income": net_income,
            "loan_growth": new_loans - old_loans,
            "capital_ratio": ratio,
            "investment_in_regulatory_capital": investment,
            "fcfe": net_income - investment,
            "note": ("Use this when only a capital ratio and loan growth are known. The "
                     "projection mode below is the one to use when a Tier 1 ratio is being "
                     "ramped up, because the ramp is often a larger reinvestment than the "
                     "asset growth itself."),
        }

    years = int(payload.get("forecast_years", DEFAULT_FORECAST_YEARS))
    if years < 1:
        raise SystemExit("forecast_years must be at least 1.")
    rwa0 = _num(payload, "risk_adjusted_assets", "bank-fcfe")
    tier1_0 = _num(payload, "tier1_capital", "bank-fcfe")
    equity0 = _num(payload, "book_equity", "bank-fcfe")
    growth = _num(payload, "asset_growth", "bank-fcfe")
    if rwa0 <= 0:
        raise SystemExit("risk_adjusted_assets must be positive.")

    ratio0 = tier1_0 / rwa0
    ratio_path = payload.get("tier1_ratio_path")
    if ratio_path is None:
        ratio_path = _ramp(ratio0, _num(payload, "tier1_ratio_target", "bank-fcfe"), years)
    if len(ratio_path) != years:
        raise SystemExit("tier1_ratio_path has %d entries but the forecast is %d years."
                         % (len(ratio_path), years))

    roe0 = _num(payload, "roe_current", "bank-fcfe")
    roe_path = payload.get("roe_path")
    if roe_path is None:
        roe_path = _ramp(roe0, _num(payload, "roe_target", "bank-fcfe"), years)
    if len(roe_path) != years:
        raise SystemExit("roe_path has %d entries but the forecast is %d years."
                         % (len(roe_path), years))

    rows = []
    rwa, tier1, equity = rwa0, tier1_0, equity0
    for t in range(1, years + 1):
        rwa = rwa * (1 + growth)
        new_tier1 = rwa * ratio_path[t - 1]
        investment = new_tier1 - tier1
        # Book equity grows by the capital retained, and that larger base drives next
        # year's net income through ROE. The table is recursive.
        equity = equity + investment
        net_income = equity * roe_path[t - 1]
        rows.append({
            "year": t,
            "risk_adjusted_assets": rwa,
            "tier1_ratio": ratio_path[t - 1],
            "tier1_capital": new_tier1,
            "investment_in_regulatory_capital": investment,
            "book_equity": equity,
            "roe": roe_path[t - 1],
            "net_income": net_income,
            "fcfe": net_income - investment,
        })
        tier1 = new_tier1

    first_positive = next((r["year"] for r in rows if r["fcfe"] > 0), None)
    return {
        "mode": "projection",
        "currency": payload.get("currency"),
        "tier1_ratio_current": ratio0,
        "asset_growth": growth,
        "annual": rows,
        "aggregate_fcfe": sum(r["fcfe"] for r in rows),
        "first_year_with_positive_fcfe": first_positive,
        "verdict": ("The bank generates payout capacity from year %d onward." % first_positive
                    if first_positive else
                    "FCFE is negative in every forecast year: the capital build exceeds "
                    "earnings throughout, and any dividend paid runs down the capital "
                    "cushion or relies on external issuance."),
        "judgment_note": ("The ratio ramp and the ROE recovery path dominate the answer and "
                          "are both estimates. State them and defend them; for a troubled "
                          "bank the ROE path decides everything."),
        "dividend_note": ("Do not trust a bank's reported dividend as evidence of capacity. "
                          "Banks paid dividends with negative FCFE widely before 2008."),
    }


def cmd_bank_fcfe(args):
    _emit(bank_fcfe(_read_payload(args)))


# --------------------------------------------------------------------------- examples

# Disney FY2013 back to FY2009, the default case in Damodaran's dividends.xls ($ millions).
DISNEY_YEARS = [
    {"label": "2013", "net_income": 6136, "depreciation": 2192, "capex": 2796,
     "change_in_noncash_wc": -133, "net_debt_issued": 1881, "dividends": 1324,
     "buybacks": 4087},
    {"label": "2012", "net_income": 5682, "depreciation": 1987, "capex": 3784,
     "change_in_noncash_wc": 940, "net_debt_issued": 4246, "dividends": 1076,
     "buybacks": 3015},
    {"label": "2011", "net_income": 4807, "depreciation": 1841, "capex": 3559,
     "change_in_noncash_wc": 950, "net_debt_issued": 2743, "dividends": 756,
     "buybacks": 4993},
    {"label": "2010", "net_income": 3963, "depreciation": 1713, "capex": 2110,
     "change_in_noncash_wc": 308, "net_debt_issued": 1190, "dividends": 653,
     "buybacks": 2669},
    {"label": "2009", "net_income": 3307, "depreciation": 1631, "capex": 1753,
     "change_in_noncash_wc": -109, "net_debt_issued": -235, "dividends": 648,
     "buybacks": 648},
]

DISNEY_TRUST_YEARS = [
    {"label": "2013", "net_income": 6136, "book_equity": 380078, "stock_return": 0.3533,
     "riskfree_rate": 0.0155, "market_return": 0.312236472},
    {"label": "2012", "net_income": 5682, "book_equity": 330056, "stock_return": 0.1065,
     "riskfree_rate": 0.019391667, "market_return": -0.042268693},
    {"label": "2011", "net_income": 4807, "book_equity": 194181, "stock_return": -0.0515,
     "riskfree_rate": 0.009308333, "market_return": 0.216054814},
    {"label": "2010", "net_income": 3963, "book_equity": 84200, "stock_return": 0.1622,
     "riskfree_rate": 0.003175, "market_return": 0.117730809},
    {"label": "2009", "net_income": 3307, "book_equity": 63437, "stock_return": 0.3117,
     "riskfree_rate": 0.000525, "market_return": 0.013788916},
]

# US Entertainment, 2013 ($ millions). Disney itself is supplied as `firm`.
ENTERTAINMENT_PEERS = [
    {"name": "Twenty-First Century Fox", "market_cap": 79796, "dividends": 415,
     "buybacks": 2062, "net_income": 7097, "fcfe": 2408},
    {"name": "Time Warner Inc", "market_cap": 63077, "dividends": 1060, "buybacks": 3879,
     "net_income": 3019, "fcfe": -4729},
    {"name": "Viacom, Inc.", "market_cap": 38974, "dividends": 555, "buybacks": 4664,
     "net_income": 2395, "fcfe": -2219},
    {"name": "The Madison Square Garden Co.", "market_cap": 4426, "dividends": 0,
     "buybacks": 0, "net_income": 142, "fcfe": -119},
    {"name": "Lions Gate Entertainment Corp", "market_cap": 4367, "dividends": 0,
     "buybacks": 0, "net_income": 232, "fcfe": -697},
    {"name": "Live Nation Entertainment", "market_cap": 3894, "dividends": 0, "buybacks": 0,
     "net_income": -163, "fcfe": 288},
    {"name": "Cinemark Holdings Inc", "market_cap": 3844, "dividends": 101, "buybacks": 0,
     "net_income": 169, "fcfe": -180},
    {"name": "MGM Holdings Inc", "market_cap": 3673, "dividends": 0, "buybacks": 59,
     "net_income": 129, "fcfe": 536},
    {"name": "Regal Entertainment Group", "market_cap": 3013, "dividends": 132,
     "buybacks": 0, "net_income": 145, "fcfe": -18},
    {"name": "DreamWorks Animation SKG", "market_cap": 2975, "dividends": 0, "buybacks": 34,
     "net_income": -36, "fcfe": -572},
    {"name": "AMC Entertainment Holdings", "market_cap": 2001, "dividends": 0,
     "buybacks": 0, "net_income": 63, "fcfe": -52},
    {"name": "World Wrestling Entertainment", "market_cap": 1245, "dividends": 36,
     "buybacks": 0, "net_income": 31, "fcfe": -27},
    {"name": "SFX Entertainment Inc.", "market_cap": 1047, "dividends": 0, "buybacks": 0,
     "net_income": -16, "fcfe": -137},
    {"name": "Carmike Cinemas Inc.", "market_cap": 642, "dividends": 0, "buybacks": 0,
     "net_income": 96, "fcfe": 64},
    {"name": "Rentrak Corporation", "market_cap": 454, "dividends": 0, "buybacks": 0,
     "net_income": -23, "fcfe": -13},
    {"name": "Reading International, Inc.", "market_cap": 177, "dividends": 0,
     "buybacks": 0, "net_income": -1, "fcfe": 15},
]

EXAMPLES = {
    "fcfe-history": {
        "currency": "USD millions",
        "debt_ratio": 0.11579296585803885,
        "debt_ratio_basis": "current market debt-to-capital ratio",
        "years": DISNEY_YEARS,
    },
    "trust": {
        "beta": 0.9011,
        "roe_average_method": "ratio_of_sums",
        "years": DISNEY_TRUST_YEARS,
    },
    "matrix": {
        "currency": "USD millions",
        "fcfe": 18064.53881686791,
        "fcfe_variant": "target debt ratio, 5 years to FY2013",
        "cash_returned": 19869.0,
        "roe": 0.0301615056118339,
        "cost_of_equity": 0.11224093867256421,
        "jensens_alpha": 0.06419906132743577,
    },
    "sustainability": {
        "currency": "USD millions",
        "revenues": 42278.0, "net_income": 6136.0, "capex": 2796.0,
        "depreciation": 2192.0, "dividends": 1324.0,
        "growth_revenues": 0.05, "growth_net_income": 0.05, "growth_capex": 0.05,
        "growth_depreciation": 0.05, "growth_dividends": 0.05,
        "wc_pct_revenues": 0.06, "debt_ratio": 0.11579296585803885,
        "forecast_years": 5,
    },
    "peers": {
        "group_label": "US Entertainment, 2013, all listed firms",
        "firm": {"name": "The Walt Disney Company", "market_cap": 134256, "dividends": 1324,
                 "buybacks": 4087, "net_income": 6136, "fcfe": 1503},
        "peers": ENTERTAINMENT_PEERS,
        "include_firm_in_group": True,
    },
    "market-norms": {
        "beta": 1.00, "expected_growth": 0.1473, "debt_to_capital": 0.1158,
        "actual_payout": 0.2158, "actual_yield": 0.0109,
        "dividends": 1324, "buybacks": 4087, "net_income": 6136, "market_cap": 134256,
        "region": "United States",
    },
    "bank-fcfe": {
        "currency": "EUR millions",
        "risk_adjusted_assets": 439851.0,
        "tier1_capital": 66561.0,
        "book_equity": 76829.0,
        "asset_growth": 0.03,
        "tier1_ratio_target": 0.18,
        "roe_current": -0.010757200462281816,
        "roe_target": 0.08,
        "forecast_years": 5,
    },
}


# ---------------------------------------------------------------------------- selftest

def _close(actual, expected, tol=1e-6):
    if actual is None or expected is None:
        return actual is expected
    return abs(actual - expected) <= tol * max(1.0, abs(expected))


def cmd_selftest(args):
    """Worked examples from Damodaran's dividends.xls and lecture packet, plus invariants."""
    results = []

    def check(name, actual, expected, tol=1e-6):
        results.append({"case": name, "expected": expected, "actual": actual,
                        "pass": _close(actual, expected, tol)})

    def assert_true(name, condition, detail=None):
        results.append({"case": name, "expected": True, "actual": detail if detail is not None
                        else bool(condition), "pass": bool(condition)})

    # --- Disney, 5 years to FY2013 (dividends.xls default case) --------------------
    hist = fcfe_history(EXAMPLES["fcfe-history"])
    y1 = hist["annual"][0]
    check("Disney 2013 pre-debt FCFE", y1["fcfe_predebt"], 5665.0)
    check("Disney 2013 actual-debt FCFE", y1["fcfe_actual_debt"], 7546.0)
    check("Disney 2013 target-ratio FCFE", y1["fcfe_target_debt_ratio"], 5719.5385, 1e-6)
    check("Disney 2013 cash returned", y1["cash_returned"], 5411.0)
    check("Disney 2013 cash as % of actual FCFE", y1["cash_pct_of_actual_fcfe"],
          5411.0 / 7546.0)

    check("Disney aggregate pre-debt FCFE", hist["aggregate"]["fcfe_predebt"], 17301.0)
    check("Disney aggregate actual-debt FCFE", hist["aggregate"]["fcfe_actual_debt"], 27126.0)
    check("Disney aggregate target-ratio FCFE", hist["aggregate"]["fcfe_target_debt_ratio"],
          18064.53881686791)
    check("Disney aggregate cash returned", hist["aggregate"]["cash_returned"], 19869.0)
    check("Disney cash as % of pre-debt FCFE",
          hist["comparison"]["fcfe_predebt"]["cash_returned_pct_of_fcfe"], 1.1484307265475984)
    check("Disney cash as % of actual-debt FCFE",
          hist["comparison"]["fcfe_actual_debt"]["cash_returned_pct_of_fcfe"],
          0.732470692324707)
    check("Disney cash as % of target-ratio FCFE",
          hist["comparison"]["fcfe_target_debt_ratio"]["cash_returned_pct_of_fcfe"],
          1.0998896900399782)
    check("Disney dividend payout, ratio of sums",
          hist["dividend_payout_ratio_aggregate"], 0.18652437748482947)
    check("Disney dividend payout, mean of annual ratios",
          hist["dividend_payout_ratio_mean_of_annual"], 0.1846276973824568)
    check("Disney cash payout ratio", hist["cash_payout_ratio_aggregate"],
          0.8315128688010044)
    check("Disney buyback share of cash returned",
          hist["buyback_share_of_cash_returned"], 15412.0 / 19869.0)
    # The verdict genuinely flips with the variant, which is the point of reporting three.
    assert_true("Disney: accumulator on actual debt, overpayer on target ratio",
                hist["comparison"]["fcfe_actual_debt"]["classification"] == "accumulator"
                and hist["comparison"]["fcfe_target_debt_ratio"]["classification"]
                == "overpayer")
    assert_true("Disney: disagreement between variants is flagged",
                hist["variants_agree"] is False
                and hist["variants_disagree_warning"] is not None)

    # --- Tata Motors: the case that separates the FCFE variants ---------------------
    # Aggregates from the lecture packet (₹ millions). Acquisitions make pre-debt FCFE
    # negative, debt funding makes actual-debt FCFE huge, and only the target-ratio
    # measure shows the payout at 157% of capacity.
    tata_year = fcfe_year(net_income=98926.0, depreciation=75648.0, capex=187570.0,
                          change_in_wc=680.0, net_debt_issued=32970.0, debt_ratio=0.0)
    check("Tata Motors 2012-13 equity reinvestment", tata_year["equity_reinvestment"],
          79632.0)
    check("Tata Motors 2012-13 FCFE after equity reinvestment",
          98926.0 - tata_year["equity_reinvestment"], 19294.0)

    # --- Trust scoring, same firm and window ---------------------------------------
    tr = trust({**EXAMPLES["trust"],
                "extra_years_for_legacy_roe": [
                    {"net_income": 4427, "book_equity": 91658},
                    {"net_income": 4687, "book_equity": 79717},
                    {"net_income": 3374, "book_equity": 63054},
                    {"net_income": 2533, "book_equity": 44602},
                    {"net_income": 2345, "book_equity": 37019}]})
    check("Disney 2013 required return", tr["annual"][0]["required_return"], 0.282889, 1e-5)
    check("Disney 2013 Jensen's alpha", tr["annual"][0]["jensens_alpha"], 0.070411, 1e-4)
    check("Disney 2013 ROE", tr["annual"][0]["roe"], 6136.0 / 380078.0)
    check("Disney average required return", tr["average_required_return"],
          0.11224093867256421)
    check("Disney average stock return", tr["average_stock_return"], 0.17644)
    check("Disney average Jensen's alpha", tr["average_jensens_alpha"], 0.06419906132743577)
    check("Disney mean-of-annual ROE", tr["average_roe_mean_of_annual"], 0.0314623, 1e-5)
    check("dividends.xls ten-row average ROE quirk reproduced",
          tr["legacy_average_roe_all_input_rows"], 0.0301615056118339)
    assert_true("Disney trust verdict is mixed, not a single label",
                tr["project_quality_verdict"] == "mixed", tr["project_quality_verdict"])

    # --- The four quadrants ---------------------------------------------------------
    # Disney 2013 on target-ratio FCFE: paid slightly more than capacity, good projects.
    m_disney = matrix(EXAMPLES["matrix"])
    check("Disney cash paid as % of target FCFE", m_disney["cash_returned_pct_of_fcfe"],
          1.0998896900399782)
    # BP 1982-91: 262% of FCFE with ROE 1.67% below the required return — the worst quadrant.
    bp = matrix({"fcfe": 571.10, "cash_returned": 1496.30, "roe": 0.10, "cost_of_equity":
                 0.11670, "currency": "USD millions"})
    check("BP cash paid as % of FCFE", bp["cash_returned_pct_of_fcfe"], 2.6200, 1e-3)
    assert_true("BP lands in deficit / poor projects",
                bp["verdict"] == "cut_payout_and_fix_investment", bp["verdict"])
    # The Limited 1983-92: negative FCFE, positive dividends, good projects. An 18.59%
    # payout ratio looks conservative and hides a deficit entirely.
    limited = matrix({"fcfe": -34.20, "cash_returned": 40.87, "roe": 0.20,
                      "cost_of_equity": 0.18310})
    assert_true("The Limited lands in deficit / good projects",
                limited["verdict"] == "reduce_payout_to_fund_projects", limited["verdict"])
    assert_true("negative FCFE makes cash-as-%-of-FCFE not applicable",
                limited["cash_returned_pct_of_fcfe"] is None
                and limited["cash_returned_pct_of_fcfe_note"] is not None)
    # Disney 2003: surplus with poor projects; Baidu 2013: surplus with good projects.
    d2003 = matrix({"fcfe": 969.0, "cash_returned": 639.0, "roe": 0.09,
                    "cost_of_equity": 0.11, "jensens_alpha": -0.03})
    assert_true("Disney 2003 lands in surplus / poor projects",
                d2003["verdict"] == "pay_out_more", d2003["verdict"])
    baidu = matrix({"fcfe": 1000.0, "cash_returned": 0.0, "roe": 0.30,
                    "cost_of_equity": 0.12})
    assert_true("Baidu lands in surplus / good projects",
                baidu["verdict"] == "maximum_flexibility", baidu["verdict"])
    # A poor ROE rescued by a good ROC still counts as good projects under the and/or rule.
    mixed_axis = matrix({"fcfe": 100.0, "cash_returned": 50.0, "roe": 0.05,
                         "cost_of_equity": 0.10, "roc": 0.14, "cost_of_capital": 0.09})
    assert_true("ROC above cost of capital rescues the quality axis",
                mixed_axis["quality_axis"] == "good"
                and mixed_axis["quality_signals_disagree"] is not None)

    # --- Forward projection ---------------------------------------------------------
    fc = sustainability(EXAMPLES["sustainability"])
    r1 = fc["annual"][0]
    check("Disney forecast year 1 revenues", r1["revenues"], 44391.9)
    check("Disney forecast year 1 net income", r1["net_income"], 6442.8)
    check("Disney forecast year 1 change in working capital",
          r1["change_in_noncash_wc"], 126.834)
    check("Disney forecast year 1 net cap ex funded by equity",
          r1["net_capex_funded_by_equity"], 560.7641, 1e-5)
    check("Disney forecast year 1 FCFE", r1["fcfe"], 5769.888383978806)
    check("Disney forecast year 1 expected dividends", r1["expected_dividends"], 1390.2)
    check("Disney forecast year 1 buyback capacity",
          r1["cash_available_for_buybacks"], 4379.688383978806)
    check("Disney forecast year 5 buyback capacity",
          fc["annual"][4]["cash_available_for_buybacks"], 5323.54, 1e-4)
    assert_true("Disney dividend is sustainable on these assumptions",
                fc["dividend_sustainable"] is True)

    # The solved growth ceiling must sit exactly on the boundary: at that rate the tightest
    # year's buyback capacity is zero, and a hair above it the dividend is unfunded.
    tight = {**EXAMPLES["sustainability"], "dividends": 4000.0, "growth_dividends": 0.30}
    solved = sustainability(tight)
    g = solved["max_sustainable_dividend_growth"]
    assert_true("a 30% dividend growth path is flagged unsustainable",
                solved["dividend_sustainable"] is False)
    at_ceiling = sustainability({**tight, "growth_dividends": g})
    just_above = sustainability({**tight, "growth_dividends": g + 1e-6})
    check("at the solved ceiling the tightest year's capacity is zero",
          at_ceiling["minimum_annual_buyback_capacity"], 0.0, 1e-3)
    assert_true("a hair above the ceiling the dividend is no longer covered",
                just_above["dividend_sustainable"] is False)

    # --- Peer group -----------------------------------------------------------------
    pg = peers(EXAMPLES["peers"])
    stats = pg["group_statistics"]
    check("US Entertainment average FCFE", stats["fcfe"]["average"], -232.29, 1e-3)
    check("US Entertainment median FCFE", stats["fcfe"]["median"], -27.0)
    check("US Entertainment average dividend yield", stats["dividend_yield"]["average"],
          0.00854, 1e-3)
    check("US Entertainment median dividend yield", stats["dividend_yield"]["median"], 0.0)
    check("Disney cash return as % of its own FCFE",
          pg["firm"]["cash_return_pct_of_fcfe"], 3.6001, 1e-4)
    check("Twenty-First Century Fox cash return as % of FCFE",
          pg["peers"][0]["cash_return_pct_of_fcfe"], 1.0287, 1e-4)
    # The packet's printed payout column, and its cash-return entry for Carmike, do not
    # reconcile with the net income and FCFE columns printed beside them (the payout column
    # was taken from per-share trailing figures). These two statistics are therefore checked
    # against the recomputation from the raw columns, which is what this engine does.
    check("US Entertainment average dividend payout, recomputed from net income",
          stats["dividend_payout"]["average"], 0.293863488, 1e-6)
    check("US Entertainment median dividend payout, recomputed from net income",
          stats["dividend_payout"]["median"], 0.137125581, 1e-6)
    check("US Entertainment average cash return as % of FCFE",
          stats["cash_return_pct_of_fcfe"]["average"], 0.789811, 1e-5)
    check("US Entertainment median cash return as % of FCFE",
          stats["cash_return_pct_of_fcfe"]["median"], 0.055037, 1e-4)
    # Five loss-makers have no payout ratio and eleven firms have no cash-return ratio.
    # Counting those as zero is the standard misreading, so the exclusions are asserted.
    check("five loss-makers excluded from the payout average",
          stats["dividend_payout"]["excluded_as_not_applicable"], 5)
    check("eleven firms with non-positive FCFE excluded from the cash-return average",
          stats["cash_return_pct_of_fcfe"]["excluded_as_not_applicable"], 11)
    # Counting the excluded rows as zero would drag the cash-return average from 79% to
    # 28%, which is exactly how this table gets misread.
    naive = sum(g["cash_return_pct_of_fcfe"] or 0.0
                for g in [pg["firm"]] + pg["peers"]) / (len(pg["peers"]) + 1)
    assert_true("treating not-applicable rows as zero would change the answer materially",
                abs(naive - stats["cash_return_pct_of_fcfe"]["average"]) > 0.4,
                {"naive": naive, "correct": stats["cash_return_pct_of_fcfe"]["average"]})
    assert_true("negative group FCFE is flagged as an unusable benchmark",
                any("cannot afford any payout" in w for w in pg["warnings"]))

    # --- Market regression ----------------------------------------------------------
    mn = market_norms(EXAMPLES["market-norms"])
    check("Disney predicted payout, January 2014 US regression",
          mn["predictions"]["payout"]["predicted"], 0.2695, 1e-3)
    check("Disney predicted yield, January 2014 US regression",
          mn["predictions"]["yield"]["predicted"], 0.0140, 1e-3)
    assert_true("actual payout below prediction produces a negative gap",
                mn["predictions"]["payout"]["gap"] < 0)
    # The overlay is the point: a firm returning 88% of earnings looks stingy on dividends.
    check("Disney cash payout ratio including buybacks",
          mn["buyback_overlay"]["cash_payout_ratio"], 5411.0 / 6136.0)
    check("US regional benchmark buyback share, January 2020",
          mn["regional_benchmark"]["values"]["buyback_share"], 0.6013)

    # --- Bank FCFE ------------------------------------------------------------------
    simple = bank_fcfe({"mode": "simple", "net_income": 150.0, "old_loans": 10000.0,
                        "new_loans": 11000.0, "capital_ratio": 0.075})
    check("bank simple case: investment in regulatory capital",
          simple["investment_in_regulatory_capital"], 75.0)
    check("bank simple case: FCFE", simple["fcfe"], 75.0)

    db = bank_fcfe(EXAMPLES["bank-fcfe"])
    check("Deutsche Bank 2013 year 1 Tier 1 capital",
          db["annual"][0]["tier1_capital"], 71156.0, 1e-4)
    check("Deutsche Bank 2013 year 1 investment in regulatory capital",
          db["annual"][0]["investment_in_regulatory_capital"], 4595.0, 1e-3)
    check("Deutsche Bank 2013 year 1 book equity", db["annual"][0]["book_equity"],
          81424.0, 1e-4)
    check("Deutsche Bank 2013 year 1 net income", db["annual"][0]["net_income"],
          602.0, 1e-3)
    check("Deutsche Bank 2013 year 1 FCFE", db["annual"][0]["fcfe"], -3993.0, 1e-3)
    check("Deutsche Bank 2013 year 5 net income", db["annual"][4]["net_income"],
          8164.0, 1e-4)
    check("Deutsche Bank 2013 year 5 FCFE", db["annual"][4]["fcfe"], 2652.0, 1e-3)
    check("Deutsche Bank 2013 year 5 Tier 1 ratio reaches the target",
          db["annual"][4]["tier1_ratio"], 0.18)
    check("Deutsche Bank FCFE turns positive in year 4",
          db["first_year_with_positive_fcfe"], 4)

    # --- Algebraic invariants -------------------------------------------------------
    # The three variants differ only in how reinvestment is financed, so at a zero debt
    # ratio the target-ratio variant collapses onto the pre-debt one.
    zero_dr = fcfe_history({**EXAMPLES["fcfe-history"], "debt_ratio": 0.0})
    check("at a zero debt ratio, target-ratio FCFE equals pre-debt FCFE",
          zero_dr["aggregate"]["fcfe_target_debt_ratio"],
          zero_dr["aggregate"]["fcfe_predebt"])
    # Net income less equity reinvestment is the same thing as actual-debt FCFE.
    assert_true("net income less equity reinvestment reproduces actual-debt FCFE",
                all(_close(r["net_income"] - r["equity_reinvestment"],
                           r["fcfe_actual_debt"]) for r in hist["annual"]))
    # Cash returned equals FCFE plus the change in the cash pile, by construction.
    surplus = (hist["aggregate"]["fcfe_target_debt_ratio"]
               - hist["aggregate"]["cash_returned"])
    check("surplus reconciles the target-ratio comparison",
          hist["comparison"]["fcfe_target_debt_ratio"]["surplus_or_deficit"], surplus)

    # --- Input guards ---------------------------------------------------------------
    for label, fn, payload in (
            ("debt ratio of 1 is rejected", fcfe_history,
             {**EXAMPLES["fcfe-history"], "debt_ratio": 1.0}),
            ("growth entered as a percentage is rejected", sustainability,
             {**EXAMPLES["sustainability"], "growth_revenues": 5.0}),
            ("expected growth entered as a percentage is rejected", market_norms,
             {**EXAMPLES["market-norms"], "expected_growth": 14.73}),
            ("empty peer group is rejected", peers,
             {**EXAMPLES["peers"], "peers": []}),
            ("missing net income is named in the error", fcfe_history,
             {"debt_ratio": 0.1, "years": [{"label": "2013", "capex": 100}]})):
        try:
            fn(payload)
            assert_true(label, False, "no error raised")
        except SystemExit as exc:
            assert_true(label, True, str(exc)[:90])

    failed = [r for r in results if not r["pass"]]
    _emit({"total": len(results), "passed": len(results) - len(failed),
           "failed": len(failed), "results": results})
    return 1 if failed else 0


# ------------------------------------------------------------------------------- main

COMMANDS = {
    "fcfe-history": cmd_fcfe_history,
    "trust": cmd_trust,
    "matrix": cmd_matrix,
    "sustainability": cmd_sustainability,
    "peers": cmd_peers,
    "market-norms": cmd_market_norms,
    "bank-fcfe": cmd_bank_fcfe,
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
        if args.command not in EXAMPLES:
            raise SystemExit("No example payload for %s." % args.command)
        _emit(EXAMPLES[args.command])
        return 0
    return COMMANDS[args.command](args) or 0


if __name__ == "__main__":
    sys.exit(main())

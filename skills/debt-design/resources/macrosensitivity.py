#!/usr/bin/env python3
"""
macrosensitivity.py — the macro exposure engine behind debt design.

The optimal debt ratio says how much to borrow. This says what to borrow. It runs the
firm's own history against four macro variables, reads each slope as a debt-design
parameter, and computes the present-value-weighted life of a project when no usable
history exists.

The script computes. It never picks the estimation window, never decides that a business
mix is stable enough to regress, and never converts a noisy slope into a confident
recommendation. Where the source method calls a number a judgment, the output says so.

Pure standard library. No third-party packages, ever — this must run anywhere.

SUBCOMMANDS
  regress       firm history + one macro series -> slope, SE, t-stat, R-squared, duration
  duration      project cash flows + a discount rate -> PV-weighted average time in years
  debt-profile  four regression results -> maturity, currency mix, fixed/floating, features
  selftest      run the bundled worked examples and report pass/fail

Each subcommand reads a JSON payload (--in FILE, or stdin) and writes JSON to stdout.
Run any subcommand with --example to print a sample input payload.
"""

import argparse
import json
import math
import sys

# Damodaran's reading of a regression t-statistic: above 2 the variable is doing real
# work, 1 to 2 is marginal, below 1 is noise. The design rule in the source material is
# blunter still — a slope with |t| below 2 must not drive a financing decision on its own.
T_SIGNIFICANT = 2.0
T_MARGINAL = 1.0

# Fewer than four change observations cannot support an intercept and a slope with any
# residual degrees of freedom left over. The source model's own floor is 4 input periods,
# which is 3 change rows; this script insists on 4 change rows so a standard error exists.
MIN_OBSERVATIONS = 4

# Below about ten annual observations the standard errors are wide enough to swamp any
# slope, so the source says to skip the historical route entirely. A slope estimated on
# eight years is graded a hint here no matter how large its t-statistic looks.
RELIABLE_ANNUAL_OBSERVATIONS = 10

# Gaussian elimination pivots are rejected below this magnitude. A pivot this small means
# the macro column is constant or duplicated, which is a data problem the caller must fix.
SINGULAR_PIVOT = 1e-12

# A GDP slope above 1.0 means firm value or operating income moves more than one-for-one
# with the economy — an amplified cycle rather than a merely positive correlation. It is
# the natural break point for calling a firm cyclical rather than an estimated threshold.
AMPLIFIED_CYCLE_SLOPE = 1.0

# The source material treats revenue growth at or above 15% a year as the "high growth"
# band where current cash flows are small next to the value of what is being built. That
# combination, not cyclicality on its own, is what argues for convertible rather than
# straight debt.
HIGH_GROWTH_RATE = 0.15

# Reporting bands for the floating-rate share. The source method sets this share by
# judgment and gives no formula, so these are a banding convention of this script used to
# turn a count of pro-floating signals into a number the caller can argue with.
FLOATING_SHARE_BANDS = {
    "significant": 0.40,
    "moderate": 0.25,
    "modest": 0.10,
    "predominantly fixed": 0.0,
}

MACRO_VARIABLES = {
    "interest_rate": {
        "series": "10-year government bond rate (FRED DGS10 or the local sovereign yield)",
        "change_convention": "absolute change in the rate",
        "read_from": "firm_value",
        "reading": "asset duration from firm value; fixed versus floating from operating income",
    },
    "gdp_growth": {
        "series": "real GDP (FRED GDPC1 or the local equivalent)",
        "change_convention": "percentage change",
        "read_from": "firm_value",
        "reading": "cyclicality",
    },
    "inflation": {
        "series": "CPI inflation rate (FRED CPIAUCSL_PC1 or the local equivalent)",
        "change_convention": "absolute change in the rate",
        "read_from": "operating_income",
        "reading": "pricing power, which sets the floating-rate share",
    },
    "exchange_rate": {
        "series": "trade-weighted index of the home currency",
        "change_convention": "percentage change",
        "read_from": "operating_income",
        "reading": "foreign-currency share of debt",
    },
}

DEPENDENTS = ("firm_value", "operating_income")


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
    try:
        return json.loads(data)
    except ValueError as exc:
        raise SystemExit("Input is not valid JSON (%s). Check for a trailing comma or an "
                         "unquoted key." % exc)


def _emit(obj):
    print(json.dumps(obj, indent=2))


def _numbers(payload, key, minimum=None):
    """Pull a list of numbers, refusing the shapes that silently produce nonsense."""
    raw = payload.get(key)
    if raw is None:
        return None
    if not isinstance(raw, list):
        raise SystemExit("%r must be a list of numbers, got %s."
                         % (key, type(raw).__name__))
    out = []
    for i, v in enumerate(raw):
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise SystemExit(
                "%r entry %d is %r. Every entry must be a number; drop the period "
                "entirely rather than passing a placeholder." % (key, i, v))
        out.append(float(v))
    if minimum is not None and len(out) < minimum:
        raise SystemExit("%r has %d entries; at least %d are needed."
                         % (key, len(out), minimum))
    return out


# ------------------------------------------------------------------- change conventions

def percent_changes(series, label):
    """Period-over-period percent change for a most-recent-first series.

    The source model lists period 1 as the most recent, so the change for period i
    compares it against period i+1, the period before it. Reversing that flips the sign
    of every slope while leaving the fit statistics untouched, which is why it is a
    silent error rather than an obvious one.
    """
    out = []
    for i in range(len(series) - 1):
        prior = series[i + 1]
        if prior == 0:
            raise SystemExit(
                "%s is zero in period %d, so the percent change into period %d is "
                "undefined. Drop both periods or use a shorter window."
                % (label, i + 2, i + 1))
        out.append(series[i] / prior - 1.0)
    return out


def firm_value_changes(market_cap, total_debt):
    """Change in firm value, which is market capitalisation plus total debt.

    Using market capitalisation alone measures the change in equity value, not firm
    value, and understates duration for any levered firm.
    """
    if len(market_cap) != len(total_debt):
        raise SystemExit(
            "market_cap has %d periods and total_debt has %d. They must line up "
            "period for period." % (len(market_cap), len(total_debt)))
    totals = [market_cap[i] + total_debt[i] for i in range(len(market_cap))]
    return percent_changes(totals, "market_cap + total_debt")


def _check_operating_income(series):
    """Refuse a history whose percent changes carry no information.

    A percent change off a near-zero or negative base is meaningless and, being large,
    dominates the fit. The source method drops those periods before regressing.
    """
    bad = [i + 1 for i, v in enumerate(series) if v <= 0]
    if bad:
        raise SystemExit(
            "Operating income is zero or negative in period(s) %s (period 1 is the most "
            "recent). Percent changes off that base are meaningless and will dominate the "
            "fit. Drop those periods and re-run, or use firm value as the dependent."
            % ", ".join(str(b) for b in bad))


# ------------------------------------------------------------------------- OLS by hand

def _solve_and_invert(a):
    """Gauss-Jordan elimination with partial pivoting on the augmented [A | b | I].

    The inverse comes back alongside the solution because the standard errors are the
    square roots of the diagonal of sigma-squared times (X'X) inverse, and there is no
    shortcut that avoids forming it.
    """
    k = len(a)
    m = [row[:] for row in a]
    for col in range(k):
        pivot_row = max(range(col, k), key=lambda r: abs(m[r][col]))
        if abs(m[pivot_row][col]) < SINGULAR_PIVOT:
            raise SystemExit(
                "The macro series has no variation across the sample, so no slope can be "
                "estimated. Check that the change convention is right: interest-rate and "
                "inflation changes are absolute, GDP and currency changes are percentages."
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


def ols_univariate(x, y):
    """Fit y = a + b*x by the normal equations X'X b = X'y, solved by elimination.

    One predictor, always. The source method runs four separate simple regressions per
    dependent variable rather than one multiple regression on all four macro variables;
    a multiple regression gives different coefficients and does not reproduce it.
    """
    n = len(x)
    if n != len(y):
        raise SystemExit("The dependent series has %d observations and the macro series "
                         "has %d. They must line up." % (len(y), n))
    # Two coefficients (intercept and slope) plus at least two residual degrees of
    # freedom is the floor at which a standard error means anything.
    if n < MIN_OBSERVATIONS:
        raise SystemExit(
            "%d change observations cannot support a slope and its standard error. "
            "At least %d are needed, which means at least %d periods of history."
            % (n, MIN_OBSERVATIONS, MIN_OBSERVATIONS + 1))

    rows = [[1.0, x[i]] for i in range(n)]
    k = 2
    xtx = [[sum(rows[i][a] * rows[i][b] for i in range(n)) for b in range(k)]
           for a in range(k)]
    xty = [sum(rows[i][a] * y[i] for i in range(n)) for a in range(k)]
    augmented = [xtx[a] + [xty[a]] + [1.0 if j == a else 0.0 for j in range(k)]
                 for a in range(k)]
    beta, inverse = _solve_and_invert(augmented)

    fitted = [beta[0] + beta[1] * x[i] for i in range(n)]
    residuals = [y[i] - fitted[i] for i in range(n)]
    sse = sum(e * e for e in residuals)
    y_mean = sum(y) / n
    sst = sum((v - y_mean) ** 2 for v in y)
    dof = n - k
    sigma_squared = sse / dof
    std_error = math.sqrt(sigma_squared * inverse[1][1])
    return {
        "observations": n,
        "intercept": beta[0],
        "slope": beta[1],
        "standard_error_of_slope": std_error,
        "t_statistic": (beta[1] / std_error) if std_error > 0 else None,
        "r_squared": (1 - sse / sst) if sst > 0 else None,
        "standard_error_of_regression": math.sqrt(sigma_squared),
        "degrees_of_freedom": dof,
    }


# ------------------------------------------------------------------- honest grading

def evidence_grade(t_statistic, observations):
    """Grade a slope as a finding, a hint, or noise — and never overstate it.

    Two gates, not one. A short sample caps the grade at a hint however large the
    t-statistic looks, because with eight annual observations the sampling distribution
    is wide and the point estimate is fragile. A long sample still needs |t| above 2
    before the slope is allowed to carry a financing decision.
    """
    if t_statistic is None:
        return "undefined"
    magnitude = abs(t_statistic)
    if observations < RELIABLE_ANNUAL_OBSERVATIONS:
        return "hint" if magnitude >= T_MARGINAL else "noise"
    if magnitude > T_SIGNIFICANT:
        return "finding"
    if magnitude >= T_MARGINAL:
        return "hint"
    return "noise"


def _grade_note(grade, t_statistic, observations):
    if grade == "finding":
        return ("|t| = %.2f on %d observations. This slope can carry a financing decision."
                % (abs(t_statistic), observations))
    if grade == "hint":
        if observations < RELIABLE_ANNUAL_OBSERVATIONS:
            return (
                "Only %d change observations. Fewer than %d annual periods leaves the "
                "standard error wide enough to swamp the slope, so this is a hint about "
                "direction, not a finding. Cross-check it against sector coefficients "
                "value-weighted across the firm's businesses." % (
                    observations, RELIABLE_ANNUAL_OBSERVATIONS))
        return ("|t| = %.2f is below %.1f. Treat the direction as suggestive and do not "
                "let this slope alone set a debt characteristic."
                % (abs(t_statistic), T_SIGNIFICANT))
    if grade == "noise":
        return ("|t| = %.2f. The slope is indistinguishable from zero. Switch to the "
                "bottom-up route: value-weight sector coefficients across the firm's "
                "businesses." % abs(t_statistic))
    return "The macro series has no variation, so no t-statistic exists."


def implied_duration(slope):
    """Asset duration read off the interest-rate slope, floored at zero.

    Firm value falls when rates rise, so the slope is normally negative and the duration
    is its magnitude. A positive slope does not mean negative duration; it means the
    regression carries no information about maturity, which is why the source model
    floors it at zero rather than reporting a negative number.
    """
    return max(0.0, -slope)


# ------------------------------------------------------------------------- regress

def regress(p):
    dependent = p.get("dependent")
    if dependent not in DEPENDENTS:
        raise SystemExit("dependent must be one of: %s." % ", ".join(DEPENDENTS))
    macro_variable = p.get("macro_variable")
    if macro_variable not in MACRO_VARIABLES:
        raise SystemExit(
            "macro_variable must be one of: %s. Each carries its own change convention: "
            "interest-rate and inflation changes are absolute changes in the rate, GDP "
            "and exchange-rate changes are percentage changes. Mixing them silently "
            "inverts signs." % ", ".join(sorted(MACRO_VARIABLES)))
    spec = MACRO_VARIABLES[macro_variable]

    macro_changes = _numbers(p, "macro_changes")
    if macro_changes is None:
        raise SystemExit(
            "macro_changes is required: one change per period, most recent first, "
            "expressed as %s of the %s." % (spec["change_convention"], spec["series"]))

    warnings = []
    history = p.get("history") or {}
    if not isinstance(history, dict):
        raise SystemExit(
            "history must be an object holding the named series, such as "
            "{\"market_cap\": [...], \"total_debt\": [...]}, not a bare list.")
    dependent_changes = _numbers(p, "dependent_changes")
    if dependent_changes is None:
        if dependent == "firm_value":
            market_cap = _numbers(history, "market_cap")
            total_debt = _numbers(history, "total_debt")
            if market_cap is None or total_debt is None:
                raise SystemExit(
                    "Pass either dependent_changes, or history.market_cap together with "
                    "history.total_debt, most recent period first. Firm value is market "
                    "capitalisation plus total debt, not market capitalisation alone.")
            dependent_changes = firm_value_changes(market_cap, total_debt)
        else:
            operating_income = _numbers(history, "operating_income")
            if operating_income is None:
                raise SystemExit(
                    "Pass either dependent_changes, or history.operating_income, most "
                    "recent period first.")
            _check_operating_income(operating_income)
            dependent_changes = percent_changes(operating_income, "Operating income")

    if len(dependent_changes) != len(macro_changes):
        raise SystemExit(
            "There are %d dependent-variable changes and %d macro changes. A history of "
            "N periods produces N-1 change rows, so pass %d macro changes covering the "
            "same fiscal years, most recent first."
            % (len(dependent_changes), len(macro_changes), len(dependent_changes)))

    fit = ols_univariate(macro_changes, dependent_changes)
    grade = evidence_grade(fit["t_statistic"], fit["observations"])

    if dependent != spec["read_from"]:
        warnings.append(
            "The source method reads %s off the %s regression, not the %s regression. "
            "The fit below is valid; check that you meant to read it this way."
            % (spec["reading"].split(";")[0].strip(), spec["read_from"], dependent))
    if fit["observations"] < RELIABLE_ANNUAL_OBSERVATIONS:
        warnings.append(
            "%d change observations is below the working floor of %d. The source method "
            "sends short histories to the bottom-up sector route instead."
            % (fit["observations"], RELIABLE_ANNUAL_OBSERVATIONS))

    out = {
        "dependent": dependent,
        "macro_variable": macro_variable,
        "series": spec["series"],
        "change_convention": spec["change_convention"],
        "specification": "univariate OLS, one macro variable at a time",
        "observations": fit["observations"],
        "intercept": fit["intercept"],
        "slope": fit["slope"],
        "standard_error_of_slope": fit["standard_error_of_slope"],
        "t_statistic": fit["t_statistic"],
        "r_squared": fit["r_squared"],
        "degrees_of_freedom": fit["degrees_of_freedom"],
        "standard_error_of_regression": fit["standard_error_of_regression"],
        "evidence": grade,
        "evidence_note": _grade_note(grade, fit["t_statistic"], fit["observations"]),
        "reading": spec["reading"],
        "warnings": warnings,
    }
    if macro_variable == "interest_rate":
        duration = implied_duration(fit["slope"])
        out["implied_duration_years"] = duration
        if fit["slope"] > 0:
            out["duration_note"] = (
                "The interest-rate coefficient is a duration: duration = max(0, -slope). "
                "The slope here is positive (%.6f), so the duration floors at zero. That "
                "is not a zero-duration firm; it means this regression carries no "
                "information about debt maturity. Use project duration or value-weighted "
                "sector coefficients instead." % fit["slope"])
        else:
            out["duration_note"] = (
                "The interest-rate coefficient is a duration: duration = max(0, -slope) "
                "= %.6f years. That is the duration the firm's debt should have, subject "
                "to the evidence grade above. Debt maturity must exceed it, because "
                "maturity always exceeds duration for a coupon-paying instrument."
                % duration)
    if p.get("period_labels"):
        out["period_labels"] = p["period_labels"][:fit["observations"]]
    out["dependent_changes"] = dependent_changes
    return out


def cmd_regress(args):
    _emit(regress(_read_payload(args)))


# ------------------------------------------------------------------------- duration

def duration(p):
    """Present-value-weighted average time at which a project's cash flows arrive.

        duration = sum over t of [ t * PV(CF_t) ] / sum over t of PV(CF_t)

    This is the direct route to duration when the firm has no usable history: no
    regression, no standard error, just the cash flows and the discount rate. It is the
    same arithmetic as a bond's Macaulay duration, so a bond can be passed as its coupon
    stream with the face value added to the final year.
    """
    rate = p.get("discount_rate")
    if not isinstance(rate, (int, float)) or isinstance(rate, bool):
        raise SystemExit("discount_rate is required and must be a number, as a decimal "
                         "(0.0846, not 8.46).")
    if rate <= -1:
        raise SystemExit("discount_rate must be above -1; a rate of -100% makes every "
                         "discount factor infinite.")
    cash_flows = _numbers(p, "cash_flows")
    if not cash_flows:
        raise SystemExit("cash_flows is required: one entry per year, starting at year "
                         "%d." % int(p.get("first_year", 0)))
    first_year = int(p.get("first_year", 0))
    flows = list(cash_flows)

    warnings = []
    terminal_value = p.get("terminal_value")
    if terminal_value is None:
        warnings.append(
            "No terminal_value was passed. If the project outlives the cash flows above, "
            "omitting the terminal value is the single most common error here and it can "
            "halve the answer. Pass terminal_value, or fold it into the final cash flow "
            "and ignore this note.")
    else:
        if isinstance(terminal_value, bool) or not isinstance(terminal_value, (int, float)):
            raise SystemExit("terminal_value must be a number.")
        flows[-1] += float(terminal_value)

    rows = []
    pv_total = 0.0
    weighted_total = 0.0
    for i, cf in enumerate(flows):
        year = first_year + i
        pv = cf / (1.0 + rate) ** year
        rows.append({"year": year, "cash_flow": cf, "present_value": pv,
                     "present_value_times_year": pv * year})
        pv_total += pv
        weighted_total += pv * year

    if pv_total <= 0:
        raise SystemExit(
            "The present values sum to %.4f, which is not positive, so there is no "
            "present-value-weighted average time to report. A project worth nothing "
            "today has no duration; check the discount rate and the terminal value."
            % pv_total)

    years = weighted_total / pv_total
    out = {
        "discount_rate": rate,
        "schedule": rows,
        "sum_of_present_values": pv_total,
        "sum_of_present_value_times_year": weighted_total,
        "duration_years": years,
        "terminal_value": terminal_value,
        "terminal_value_share_of_weighted_sum": (
            (rows[-1]["present_value_times_year"] / weighted_total)
            if weighted_total else None),
        "note": ("Set the debt's duration to %.2f years. Its maturity must be longer, "
                 "because maturity exceeds duration for any coupon-paying instrument."
                 % years),
        "warnings": warnings,
    }
    coupon_rate = p.get("coupon_rate")
    if coupon_rate is not None:
        out["matching_par_bond"] = par_bond_maturity(years, float(coupon_rate))
    return out


def par_bond_maturity(target_duration, coupon_rate):
    """Maturity of an annual-pay par bond whose Macaulay duration hits a target.

    For a bond priced at par the coupon equals the yield, and the duration collapses to
    D = (1+r)/r * (1 - (1+r)^-N). Inverting it gives the maturity to ask for when the
    design calls for a duration. This is the bridge between "duration 4.3 years" and an
    instrument someone can actually issue.
    """
    if coupon_rate <= 0:
        # A zero-coupon bond's duration is its maturity, with nothing to solve.
        return {"coupon_rate": coupon_rate, "maturity_years": target_duration,
                "note": "A zero-coupon instrument has duration equal to its maturity."}
    ceiling = (1.0 + coupon_rate) / coupon_rate
    if target_duration >= ceiling:
        return {
            "coupon_rate": coupon_rate, "maturity_years": None,
            "note": ("A par bond at a %.2f%% coupon cannot reach a duration of %.2f years "
                     "at any maturity; its duration approaches %.2f years as maturity goes "
                     "to infinity. Lower the coupon or accept a shorter duration."
                     % (coupon_rate * 100, target_duration, ceiling)),
        }
    maturity = -math.log(1.0 - target_duration * coupon_rate / (1.0 + coupon_rate)) \
        / math.log(1.0 + coupon_rate)
    return {
        "coupon_rate": coupon_rate, "maturity_years": maturity,
        "note": ("An annual-pay par bond with a %.2f%% coupon and a %.2f-year maturity has "
                 "a duration of %.2f years." % (coupon_rate * 100, maturity, target_duration)),
    }


def cmd_duration(args):
    _emit(duration(_read_payload(args)))


# ---------------------------------------------------------------------- debt profile

def _regression_input(payload, key, default_dependent=None):
    """Normalise one regression result, whether it came from `regress` or by hand."""
    block = payload.get(key)
    if block is None:
        raise SystemExit(
            "%r is missing. debt-profile needs all four regression results: %s. Pass each "
            "as {\"slope\": ..., \"t_statistic\": ..., \"observations\": ..., "
            "\"dependent\": ...} — the output of `regress` can be handed straight in."
            % (key, ", ".join(sorted(MACRO_VARIABLES))))
    if not isinstance(block, dict):
        raise SystemExit("%r must be an object, got %s." % (key, type(block).__name__))
    slope = block.get("slope")
    if isinstance(slope, bool) or not isinstance(slope, (int, float)):
        raise SystemExit("%r needs a numeric 'slope'." % key)
    t_statistic = block.get("t_statistic")
    if t_statistic is not None and (isinstance(t_statistic, bool)
                                    or not isinstance(t_statistic, (int, float))):
        raise SystemExit("%r has a non-numeric 't_statistic'." % key)
    observations = block.get("observations")
    if observations is None:
        # No count supplied means the caller cannot vouch for the sample, so the grader
        # is told to assume a short one rather than quietly assuming a long one.
        observations = 0
    dependent = block.get("dependent",
                          default_dependent or MACRO_VARIABLES[key]["read_from"])
    grade = evidence_grade(t_statistic, observations)
    return {
        "macro_variable": key, "slope": float(slope),
        "t_statistic": (float(t_statistic) if t_statistic is not None else None),
        "observations": int(observations), "dependent": dependent,
        "evidence": grade,
        "usable_for_design": grade == "finding",
    }


def debt_profile(p):
    """Turn four macro slopes into the debt the firm should actually issue."""
    results = {k: _regression_input(p, k) for k in MACRO_VARIABLES}
    convention_warnings = []
    for key, res in results.items():
        expected = MACRO_VARIABLES[key]["read_from"]
        if res["dependent"] != expected:
            convention_warnings.append(
                "The %s slope was taken from the %s regression; the source method reads "
                "it off the %s regression." % (key, res["dependent"], expected))

    rates = results["interest_rate"]
    gdp = results["gdp_growth"]
    inflation = results["inflation"]
    currency = results["exchange_rate"]

    # ---- maturity, from the duration
    target_duration = implied_duration(rates["slope"])
    if rates["slope"] > 0:
        maturity_note = (
            "The interest-rate slope is positive (%.4f), so duration floors at zero and "
            "this regression says nothing about maturity. Fall back to project duration "
            "or value-weighted sector coefficients before setting a maturity."
            % rates["slope"])
    else:
        maturity_note = (
            "Target a debt duration of %.2f years. Weighted-average maturity must be "
            "longer than that, because maturity exceeds duration for any coupon-paying "
            "instrument; matching maturity to duration overshoots." % target_duration)
    if rates["evidence"] != "finding":
        maturity_note = (
            "This duration is graded %s, so it cannot set a maturity on its own. %s "
            "Re-estimate it from project cash flows, or from sector coefficients "
            "value-weighted across the firm's businesses, before issuing anything."
            % (rates["evidence"], maturity_note))
    maturity_block = {
        "target_duration_years": target_duration,
        "evidence": rates["evidence"],
        "evidence_note": _grade_note(rates["evidence"], rates["t_statistic"],
                                     rates["observations"]),
        "note": maturity_note,
    }
    coupon_rate = p.get("coupon_rate")
    if coupon_rate is not None and target_duration > 0:
        maturity_block["matching_par_bond"] = par_bond_maturity(
            target_duration, float(coupon_rate))

    # ---- currency mix, from the exchange-rate sensitivity
    revenue_mix = p.get("revenue_by_currency")
    home_currency = p.get("home_currency", "home currency")
    if currency["slope"] < 0:
        currency_direction = (
            "Value or income falls when the %s strengthens, so part of the debt belongs "
            "in the currencies where revenues are earned." % home_currency)
        borrow_foreign = True
    elif currency["slope"] > 0:
        currency_direction = (
            "Value or income rises when the %s strengthens, which argues for keeping the "
            "debt in the %s. A significant slope with this sign is more often a data "
            "problem than a discovery — check it before acting on it."
            % (home_currency, home_currency))
        borrow_foreign = False
    else:
        currency_direction = "The exchange-rate slope is zero; no currency signal."
        borrow_foreign = False

    currency_block = {
        "slope": currency["slope"], "evidence": currency["evidence"],
        "evidence_note": _grade_note(currency["evidence"], currency["t_statistic"],
                                     currency["observations"]),
        "borrow_in_foreign_currency": borrow_foreign,
        "direction": currency_direction,
    }
    if revenue_mix:
        if not isinstance(revenue_mix, list):
            raise SystemExit("revenue_by_currency must be a list of "
                             "{\"currency\": ..., \"share\": ...} objects.")
        total = 0.0
        mix = []
        for row in revenue_mix:
            if not isinstance(row, dict):
                raise SystemExit(
                    "Each revenue_by_currency entry must be an object such as "
                    "{\"currency\": \"EUR\", \"share\": 0.18}, got %r." % (row,))
            share = row.get("share")
            if isinstance(share, bool) or not isinstance(share, (int, float)):
                raise SystemExit("Every revenue_by_currency row needs a numeric 'share'.")
            total += float(share)
            mix.append({"currency": row.get("currency", "?"), "share": float(share)})
        if total <= 0:
            raise SystemExit("revenue_by_currency shares must sum to something positive.")
        for row in mix:
            row["share"] = row["share"] / total
        currency_block["currency_mix"] = mix
        foreign = sum(r["share"] for r in mix if r["currency"] != home_currency)
        currency_block["foreign_currency_share"] = foreign
        currency_block["note"] = (
            "The slope gives direction and rough size, not the target share. The share "
            "above comes from revenue geography, which is the source method's rule; the "
            "regression sign %s it. Where home-currency revenue is itself exposed to "
            "currency moves, the foreign share should sit above the raw revenue split."
            % ("agrees with" if borrow_foreign else "disagrees with"))
    else:
        currency_block["note"] = (
            "Pass revenue_by_currency to size the split. The regression sets direction; "
            "revenue geography sets the share.")

    # ---- fixed against floating, from the inflation and interest-rate sensitivities
    #
    # The source method reads this pair off the operating-income regressions: what decides
    # fixed against floating is whether the cash flows that service the debt move with the
    # variable, not whether the firm's market value does. The interest-rate block above is
    # the firm-value one, so an operating-income version is taken when supplied.
    rate_signal = rates
    rate_signal_source = "the interest_rate block"
    if p.get("operating_income_on_interest_rate") is not None:
        rate_signal = _regression_input(p, "operating_income_on_interest_rate",
                                        default_dependent="operating_income")
        rate_signal["macro_variable"] = "interest_rate"
        rate_signal_source = "the operating_income_on_interest_rate block"
    elif rates["dependent"] != "operating_income":
        convention_warnings.append(
            "Fixed versus floating fell back to the firm-value interest-rate slope. Pass "
            "operating_income_on_interest_rate to use the regression the source method "
            "actually reads this off.")

    signals = []
    pro_floating = 0
    for res, why in ((inflation, "operating income rises with inflation, which is pricing "
                                 "power: floating payments rise when cash flows rise"),
                     (rate_signal, "operating income rises with interest rates, so "
                                   "floating payments and cash flows move together")):
        if res["slope"] > 0:
            significant = res["evidence"] == "finding"
            if significant:
                pro_floating += 1
            signals.append({"macro_variable": res["macro_variable"], "slope": res["slope"],
                            "evidence": res["evidence"], "direction": "favours floating",
                            "why": why})
        elif res["slope"] < 0:
            signals.append({"macro_variable": res["macro_variable"], "slope": res["slope"],
                            "evidence": res["evidence"], "direction": "favours fixed",
                            "why": "cash flows fall when this variable rises, so floating "
                                   "payments would rise exactly when the firm can least "
                                   "afford them"})
    weak_positive = any(s["direction"] == "favours floating" and s["evidence"] != "finding"
                        for s in signals)
    if pro_floating >= 2:
        band = "significant"
    elif pro_floating == 1:
        band = "moderate"
    elif weak_positive:
        band = "modest"
    else:
        band = "predominantly fixed"
    floating_share = FLOATING_SHARE_BANDS[band]
    fixed_floating = {
        "band": band,
        "floating_share": floating_share,
        "fixed_share": 1.0 - floating_share,
        "signals": signals,
        "interest_rate_signal_from": rate_signal_source,
        "note": ("The source method sets this share by judgment and gives no formula. The "
                 "share above is a reporting band of this script, driven by how many of "
                 "the two pro-floating signals cleared |t| > %.1f. Argue with the number; "
                 "do not cite it as an estimate." % T_SIGNIFICANT),
    }

    # ---- straight against convertible, from growth
    expected_growth = p.get("expected_revenue_growth")
    current_cash_flow_positive = p.get("current_cash_flow_positive", True)
    cyclical = gdp["slope"] > AMPLIFIED_CYCLE_SLOPE
    if expected_growth is not None:
        high_growth = float(expected_growth) >= HIGH_GROWTH_RATE
        convertible = bool(high_growth and not current_cash_flow_positive)
        if convertible:
            convertible_note = (
                "Expected growth of %.1f%% against current cash flows that are not "
                "positive: the value is in what has not been built yet, so lenders price "
                "straight debt off assets that do not exist. Convertible debt lets them "
                "share the upside instead, which is what brings the coupon down."
                % (float(expected_growth) * 100))
        elif high_growth:
            convertible_note = (
                "Expected growth of %.1f%% is high, but current cash flows are positive "
                "and can service straight debt. Straight debt, with the growth argument "
                "revisited if cash flows turn."  % (float(expected_growth) * 100))
        else:
            convertible_note = (
                "Expected growth of %.1f%% is below the %.0f%% high-growth band and "
                "current cash flows service the debt. Straight debt."
                % (float(expected_growth) * 100, HIGH_GROWTH_RATE * 100))
    else:
        # With no growth input the GDP slope is the only growth signal available, and it
        # measures cyclicality rather than expected growth. It is a weak proxy and the
        # output says so rather than pretending otherwise.
        convertible = False
        convertible_note = (
            "No expected_revenue_growth was passed, so the only growth signal available "
            "is the GDP slope of %.4f, which measures cyclicality rather than expected "
            "growth. Defaulting to straight debt. Pass expected_revenue_growth and "
            "current_cash_flow_positive to make this call properly." % gdp["slope"])

    special_features = []
    if cyclical and gdp["evidence"] == "finding":
        special_features.append(
            "Tie debt service to output. A GDP slope of %.2f means income swings more "
            "than one-for-one with the economy, so flat payments will default the firm in "
            "a downturn it would otherwise survive. Failing that, borrow less."
            % gdp["slope"])
    elif cyclical:
        special_features.append(
            "The GDP slope of %.2f suggests an amplified cycle, but it is graded %s. "
            "Treat cyclicality as a reason to hold debt back, not as a sized adjustment."
            % (gdp["slope"], gdp["evidence"]))
    if borrow_foreign and currency["evidence"] == "finding":
        special_features.append(
            "Issue in the revenue currencies rather than swapping later where the market "
            "allows it; the swap is the cheaper fix for debt already outstanding.")

    usable = [k for k, r in results.items() if r["usable_for_design"]]
    unusable = [k for k, r in results.items() if not r["usable_for_design"]]
    if not usable:
        headline = (
            "None of the four slopes clears the bar for a financing decision. This design "
            "rests on nothing. Switch to the bottom-up route — value-weight published "
            "sector coefficients across the firm's businesses — and treat the numbers "
            "below as the shape of an answer rather than the answer.")
    elif unusable:
        headline = (
            "%d of 4 slopes carry evidence (%s). The rest (%s) are hints or noise; the "
            "characteristics they drive should be set from sector coefficients or from "
            "the intuitive business-by-business route."
            % (len(usable), ", ".join(sorted(usable)), ", ".join(sorted(unusable))))
    else:
        headline = "All four slopes clear |t| > %.1f on an adequate sample." % T_SIGNIFICANT

    return {
        "regressions": [results[k] for k in sorted(results)],
        "evidence_summary": {
            "usable_for_design": sorted(usable),
            "not_usable_for_design": sorted(unusable),
            "headline": headline,
        },
        "debt_design": {
            "maturity": maturity_block,
            "currency": currency_block,
            "fixed_versus_floating": fixed_floating,
            "convertible": {
                "convertible_yes_no": convertible,
                "recommendation": "convertible" if convertible else "straight",
                "cyclicality_slope": gdp["slope"],
                "cyclical": cyclical,
                "note": convertible_note,
            },
            "special_features": special_features,
        },
        "convention_warnings": convention_warnings,
    }


def cmd_debt_profile(args):
    _emit(debt_profile(_read_payload(args)))


# ---------------------------------------------------------------------------- selftest

# macrodur.xls, `Inputs for top down`: eleven annual periods, period 1 most recent.
MACRODUR_OPERATING_INCOME = [27801.0, 26558.0, 25542.0, 24002.0, 22798.0, 21952.0,
                             20497.0, 18713.0, 17091.0, 12673.0, 11334.0]
MACRODUR_MARKET_CAP = [231814.0, 209728.0, 197142.0, 202286.0, 184946.0, 201590.0,
                       197007.0, 192048.0, 221861.0, 232147.0, 210081.0]
MACRODUR_TOTAL_DEBT = [54136.0, 53427.0, 49864.0, 41320.0, 42218.0, 44671.0, 39018.0,
                       38729.0, 31052.0, 26466.0, 25388.0]

# The Brazilian theme park, discounted at Disney's 8.46% cost of capital ($ millions).
PARK_CASH_FLOWS = [-2000.0, -1000.0, -859.0, -267.0, 340.0, 466.0, 516.0, 555.0, 615.0,
                   681.0, 715.0]
PARK_TERMINAL_VALUE = 11275.0
PARK_DISCOUNT_RATE = 0.0846

# Disney's own regressions, 1985-2013, exactly as the lecture reports them. Five of the
# eight slopes are insignificant, which is the base rate for this method rather than a
# bad draw, so this is the honest payload to ship as the example.
DISNEY_REGRESSIONS = {
    "interest_rate": {"slope": -2.3251, "t_statistic": 0.39, "observations": 28,
                      "dependent": "firm_value"},
    "gdp_growth": {"slope": 6.7000, "t_statistic": 2.03, "observations": 28,
                   "dependent": "firm_value"},
    "inflation": {"slope": 8.1867, "t_statistic": 2.76, "observations": 28,
                  "dependent": "operating_income"},
    "exchange_rate": {"slope": -1.6773, "t_statistic": 2.13, "observations": 28,
                      "dependent": "operating_income"},
    "operating_income_on_interest_rate": {
        "slope": -7.9339, "t_statistic": 1.40, "observations": 28,
        "dependent": "operating_income"},
}

# The same firm read bottom-up instead: sector coefficients value-weighted across its five
# businesses. This is the route the lecture actually designs the debt from, because the
# firm-level duration slope above is noise.
DISNEY_BOTTOM_UP = {
    "interest_rate": {"slope": -4.34, "t_statistic": 2.20, "observations": 28,
                      "dependent": "firm_value"},
    "gdp_growth": {"slope": 0.55, "t_statistic": 2.03, "observations": 28,
                   "dependent": "firm_value"},
    "inflation": {"slope": 8.1867, "t_statistic": 2.76, "observations": 28,
                  "dependent": "operating_income"},
    "exchange_rate": {"slope": -1.67, "t_statistic": 2.13, "observations": 28,
                      "dependent": "operating_income"},
}

EXAMPLES = {
    "regress": {
        "comment": ("The firm history is the eleven annual periods from the source model, "
                    "most recent first. The macro column is illustrative — replace it with "
                    "the published series for the same fiscal years, entered as an "
                    "absolute change in the rate."),
        "dependent": "firm_value",
        "macro_variable": "interest_rate",
        "history": {"market_cap": MACRODUR_MARKET_CAP, "total_debt": MACRODUR_TOTAL_DEBT},
        "macro_changes": [0.00273411, -0.00546, 0.00329, -0.00415, 0.00512, -0.00187,
                          -0.00301, 0.00104, 0.00268, -0.00394],
        "period_labels": ["2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011",
                          "2010", "2009"],
    },
    "duration": {
        "comment": "A proposed theme park, in millions, with the terminal value in year 10.",
        "discount_rate": PARK_DISCOUNT_RATE,
        "cash_flows": PARK_CASH_FLOWS,
        "terminal_value": PARK_TERMINAL_VALUE,
        "coupon_rate": 0.05,
    },
    "debt-profile": dict(
        DISNEY_REGRESSIONS,
        comment=("Firm-level regressions, 1985-2013. The duration slope is noise (t = "
                 "0.39), which is what sends this design to the bottom-up route."),
        home_currency="USD",
        revenue_by_currency=[{"currency": "USD", "share": 0.82},
                             {"currency": "EUR", "share": 0.12},
                             {"currency": "OTHER", "share": 0.06}],
        expected_revenue_growth=0.06,
        current_cash_flow_positive=True,
        coupon_rate=0.05,
    ),
}


def _close(actual, expected, tol=1e-6):
    return (isinstance(actual, (int, float)) and not isinstance(actual, bool)
            and abs(actual - expected) <= tol * max(1.0, abs(expected)))


def cmd_selftest(args):
    """Worked examples from the source models, so a port can be verified."""
    results = []

    def check(name, actual, expected, tol=1e-6):
        results.append({"case": name, "expected": expected, "actual": actual,
                        "pass": _close(actual, expected, tol)})

    def assert_true(name, condition, actual=None):
        results.append({"case": name, "expected": True,
                        "actual": condition if actual is None else actual,
                        "pass": bool(condition)})

    def refuses(name, fn):
        try:
            fn()
            refused = False
        except SystemExit:
            refused = True
        results.append({"case": name, "expected": True, "actual": refused,
                        "pass": refused})

    # --- change conventions, straight from macrodur.xls -------------------------------
    oi_changes = percent_changes(MACRODUR_OPERATING_INCOME, "Operating income")
    fv_changes = firm_value_changes(MACRODUR_MARKET_CAP, MACRODUR_TOTAL_DEBT)
    # 27801/26558 - 1. Period 1 is the most recent, so the change looks *backwards*.
    check("macrodur change in operating income, period 1", oi_changes[0], 0.0468032231342721)
    # (231814+54136)/(209728+53427) - 1. Firm value is market cap PLUS debt: using market
    # cap alone gives 0.105311 here, which is a different number and a different slope.
    check("macrodur change in firm value, period 1", fv_changes[0], 0.08662195284148133)
    assert_true("firm value is not equity value",
                not _close(fv_changes[0], MACRODUR_MARKET_CAP[0] / MACRODUR_MARKET_CAP[1] - 1))
    check("eleven periods give ten change rows", len(fv_changes), 10)

    # --- OLS mechanics, hand-checkable to the last digit ------------------------------
    # x = 1..5, y = 2,4,5,4,5. Sxy = 6, Sxx = 10, so slope = 0.6 and intercept = 2.2.
    # SSE = 2.4, SST = 6, so R-squared = 0.6. sigma^2 = SSE/(n-2) = 0.8, so the slope's
    # standard error is sqrt(0.8/10). Dividing by n instead of n-2 would give 0.2190 and
    # a t-statistic of 2.739 — the classic wrong answer this case is here to catch.
    fit = ols_univariate([1.0, 2.0, 3.0, 4.0, 5.0], [2.0, 4.0, 5.0, 4.0, 5.0])
    check("OLS slope", fit["slope"], 0.6)
    check("OLS intercept", fit["intercept"], 2.2)
    check("OLS R-squared", fit["r_squared"], 0.6)
    check("OLS standard error uses n-2", fit["standard_error_of_slope"], 0.08 ** 0.5)
    check("OLS t-statistic", fit["t_statistic"], 0.6 / 0.08 ** 0.5)
    check("OLS degrees of freedom", fit["degrees_of_freedom"], 3)

    # A perfect fit must come back exactly, with R-squared of one and no residual spread.
    perfect = ols_univariate([0.0, 1.0, 2.0, 3.0], [1.0, 3.0, 5.0, 7.0])
    check("perfect fit recovers the slope", perfect["slope"], 2.0)
    check("perfect fit recovers the intercept", perfect["intercept"], 1.0)
    check("perfect fit has R-squared of one", perfect["r_squared"], 1.0)

    # Scaling the regressor scales the slope inversely and leaves the fit alone. This is
    # what makes a mixed change convention silent: absolute rate changes entered as
    # percentages move the coefficient by a factor of a hundred and nothing else.
    scaled = ols_univariate([100.0, 200.0, 300.0, 400.0, 500.0], [2.0, 4.0, 5.0, 4.0, 5.0])
    check("scaling the regressor scales the slope", scaled["slope"], 0.006)
    check("scaling the regressor leaves R-squared alone", scaled["r_squared"], 0.6)

    # --- duration read off the interest-rate slope ------------------------------------
    # macrodur.xls: the firm-value slope is +6.081218, so the duration floors at zero;
    # the operating-income slope is -1.462709, so its duration is +1.462709.
    check("positive interest-rate slope floors duration at zero",
          implied_duration(6.081218), 0.0)
    check("negative interest-rate slope becomes a positive duration",
          implied_duration(-1.462709), 1.462709)
    check("Disney bottom-up duration", implied_duration(-4.34), 4.34)

    # --- project duration: the Brazilian theme park ------------------------------------
    park = duration({"discount_rate": PARK_DISCOUNT_RATE, "cash_flows": PARK_CASH_FLOWS,
                     "terminal_value": PARK_TERMINAL_VALUE})
    # The lecture case reports a PV sum of $3,296M, a PV-times-year sum of $62,355M and a
    # duration of 18.92 years, all rounded off intermediate values.
    check("theme park sum of present values", park["sum_of_present_values"], 3296.0, 1e-3)
    check("theme park PV-weighted sum", park["sum_of_present_value_times_year"],
          62355.0, 1e-3)
    check("theme park duration", park["duration_years"], 18.92, 1e-3)
    # Year 1's present value is -922 in the published table.
    check("theme park year 1 present value", park["schedule"][1]["present_value"],
          -922.0, 1e-3)
    # Omitting the terminal value is the classic error: it dominates the weighted sum.
    assert_true("terminal value dominates the weighted sum",
                park["terminal_value_share_of_weighted_sum"] > 0.8)
    refuses("the park's operating flows alone have no positive present value",
            lambda: duration({"discount_rate": PARK_DISCOUNT_RATE,
                              "cash_flows": PARK_CASH_FLOWS}))
    # A five-year annuity closed with a terminal value against the same annuity alone.
    annuity = [0.0, 30.0, 30.0, 30.0, 30.0, 30.0]
    with_tv = duration({"discount_rate": 0.10, "cash_flows": annuity,
                        "terminal_value": 500.0})
    without_tv = duration({"discount_rate": 0.10, "cash_flows": annuity})
    assert_true("dropping the terminal value shortens the duration",
                without_tv["duration_years"] < with_tv["duration_years"])
    assert_true("a missing terminal value is called out", bool(without_tv["warnings"]))
    assert_true("a supplied terminal value raises no warning", not with_tv["warnings"])

    # A zero-coupon bond's duration is its maturity — the sharpest check on the weighting.
    zero_coupon = duration({"discount_rate": 0.05,
                            "cash_flows": [0.0] * 7 + [100.0]})
    check("zero-coupon duration equals maturity", zero_coupon["duration_years"], 7.0)
    # And a coupon bond's duration is strictly shorter than its maturity.
    coupon_bond = duration({"discount_rate": 0.05,
                            "cash_flows": [0.0] + [5.0] * 6 + [105.0]})
    assert_true("coupon bond duration is shorter than its maturity",
                coupon_bond["duration_years"] < 7.0)
    # A 10-year 5% par bond has a Macaulay duration of (1.05/0.05)*(1-1.05^-10) = 8.1078.
    par_ten = duration({"discount_rate": 0.05, "cash_flows": [0.0] + [5.0] * 9 + [105.0]})
    check("ten-year par bond duration", par_ten["duration_years"],
          (1.05 / 0.05) * (1 - 1.05 ** -10))
    # The inverse must land back on the same maturity.
    check("par bond maturity inverts the duration formula",
          par_bond_maturity(par_ten["duration_years"], 0.05)["maturity_years"], 10.0)
    assert_true("an unreachable duration is refused, not approximated",
                par_bond_maturity(50.0, 0.05)["maturity_years"] is None)

    # --- honest grading ----------------------------------------------------------------
    assert_true("a long sample with a big t is a finding",
                evidence_grade(2.76, 28) == "finding", evidence_grade(2.76, 28))
    # The headline case: eight annual observations is a hint however large the t looks.
    assert_true("eight observations cap the grade at a hint",
                evidence_grade(9.0, 8) == "hint", evidence_grade(9.0, 8))
    assert_true("Disney's 0.39 duration t-statistic is noise",
                evidence_grade(0.39, 28) == "noise", evidence_grade(0.39, 28))
    assert_true("a marginal t on a long sample is a hint",
                evidence_grade(1.40, 28) == "hint", evidence_grade(1.40, 28))
    assert_true("sign does not change the grade",
                evidence_grade(-2.76, 28) == "finding")

    # --- regress end to end -------------------------------------------------------------
    fitted = regress({
        "dependent": "operating_income",
        "macro_variable": "interest_rate",
        "history": {"operating_income": MACRODUR_OPERATING_INCOME},
        "macro_changes": EXAMPLES["regress"]["macro_changes"],
    })
    check("regress computes ten observations from eleven periods",
          fitted["observations"], 10)
    assert_true("regress reports the change convention",
                fitted["change_convention"] == "absolute change in the rate")
    assert_true("regress reads the rate coefficient as a duration",
                "implied_duration_years" in fitted and "duration" in fitted["duration_note"])
    assert_true("regress flags reading a duration off operating income",
                any("firm_value" in w for w in fitted["warnings"]))
    check("regress duration is the sign-flipped slope, floored",
          fitted["implied_duration_years"], max(0.0, -fitted["slope"]))

    fv_fit = regress({
        "dependent": "firm_value", "macro_variable": "gdp_growth",
        "history": {"market_cap": MACRODUR_MARKET_CAP, "total_debt": MACRODUR_TOTAL_DEBT},
        "macro_changes": [0.0290, 0.0233, 0.0171, 0.0291, 0.0253, 0.0184, 0.0225, 0.0155,
                          0.0256, -0.0254],
    })
    check("firm-value regression uses the market cap plus debt series",
          fv_fit["dependent_changes"][0], 0.08662195284148133)
    # Eleven periods give exactly ten change rows, which is the working floor, so no
    # short-sample warning fires. One period fewer and it must.
    assert_true("ten observations clears the working floor", not fv_fit["warnings"])
    nine = regress({
        "dependent": "firm_value", "macro_variable": "gdp_growth",
        "history": {"market_cap": MACRODUR_MARKET_CAP[:10],
                    "total_debt": MACRODUR_TOTAL_DEBT[:10]},
        "macro_changes": [0.0290, 0.0233, 0.0171, 0.0291, 0.0253, 0.0184, 0.0225, 0.0155,
                          0.0256],
    })
    assert_true("nine observations is flagged as short",
                any("floor" in w for w in nine["warnings"]))
    assert_true("a short sample is graded a hint at best",
                nine["evidence"] in ("hint", "noise"), nine["evidence"])

    # Bad input is explained, not crashed.
    refuses("operating income of zero is refused", lambda: regress({
        "dependent": "operating_income", "macro_variable": "inflation",
        "history": {"operating_income": [100.0, 0.0, 90.0, 80.0, 70.0]},
        "macro_changes": [0.01, 0.02, 0.03, 0.04]}))
    refuses("a mismatched macro series is refused", lambda: regress({
        "dependent": "firm_value", "macro_variable": "gdp_growth",
        "history": {"market_cap": [10.0, 9.0, 8.0, 7.0, 6.0],
                    "total_debt": [1.0, 1.0, 1.0, 1.0, 1.0]},
        "macro_changes": [0.01, 0.02]}))
    refuses("an unknown macro variable is refused", lambda: regress({
        "dependent": "firm_value", "macro_variable": "oil_price",
        "dependent_changes": [0.1, 0.2, 0.3, 0.4], "macro_changes": [0.01, 0.02, 0.03, 0.04]}))
    refuses("too few observations is refused", lambda: regress({
        "dependent": "firm_value", "macro_variable": "inflation",
        "dependent_changes": [0.1, 0.2, 0.3], "macro_changes": [0.01, 0.02, 0.03]}))
    refuses("a constant macro column is refused", lambda: regress({
        "dependent": "firm_value", "macro_variable": "inflation",
        "dependent_changes": [0.1, 0.2, 0.3, 0.4],
        "macro_changes": [0.02, 0.02, 0.02, 0.02]}))
    refuses("a text placeholder in a series is refused", lambda: regress({
        "dependent": "firm_value", "macro_variable": "inflation",
        "dependent_changes": [0.1, "n/a", 0.3, 0.4],
        "macro_changes": [0.01, 0.02, 0.03, 0.04]}))
    refuses("duration without a discount rate is refused",
            lambda: duration({"cash_flows": [-100.0, 50.0, 60.0]}))
    refuses("a project with no positive present value has no duration",
            lambda: duration({"discount_rate": 0.10, "cash_flows": [-100.0, 10.0, 10.0]}))

    # --- debt-profile: Disney's own regressions ----------------------------------------
    disney = debt_profile(EXAMPLES["debt-profile"])
    design = disney["debt_design"]
    # The firm-value slope on rates is -2.3251, so duration reads 2.3251 years...
    check("Disney firm-level duration", design["maturity"]["target_duration_years"], 2.3251)
    # ...but its t-statistic is 0.39, so the design must refuse to lean on it.
    assert_true("Disney's duration slope is not usable for design",
                "interest_rate" in disney["evidence_summary"]["not_usable_for_design"])
    assert_true("a noisy duration is not dressed up as a maturity target",
                "cannot set a maturity on its own" in design["maturity"]["note"])
    assert_true("three of the four Disney slopes carry evidence",
                len(disney["evidence_summary"]["usable_for_design"]) == 3,
                disney["evidence_summary"]["usable_for_design"])
    # Operating income falls when rates rise (-7.9339) but rises with inflation (+8.1867,
    # t = 2.76). One significant pro-floating signal, so a moderate floating share.
    assert_true("pricing power raises the floating share",
                design["fixed_versus_floating"]["floating_share"] > 0)
    assert_true("floating and fixed shares sum to one",
                _close(design["fixed_versus_floating"]["floating_share"]
                       + design["fixed_versus_floating"]["fixed_share"], 1.0))
    assert_true("the rate signal for fixed-versus-floating comes from operating income",
                "operating_income" in design["fixed_versus_floating"]
                ["interest_rate_signal_from"])
    assert_true("a negative rate slope on income is read as favouring fixed",
                any(s["macro_variable"] == "interest_rate"
                    and s["direction"] == "favours fixed"
                    for s in design["fixed_versus_floating"]["signals"]))
    # A stronger dollar hurts income (-1.6773, t = 2.13), so part of the debt goes abroad,
    # and the share comes from revenue geography: 18% non-dollar in the 2013 case.
    assert_true("a negative currency slope sends debt abroad",
                design["currency"]["borrow_in_foreign_currency"])
    check("foreign-currency share follows revenue geography",
          design["currency"]["foreign_currency_share"], 0.18)
    # Cyclical (GDP slope 6.70) but mature and cash-generative, so the design is straight
    # debt with a cash-flow-linked feature. Keying convertible off cyclicality alone would
    # get this backwards, which is the point of the case.
    assert_true("a cyclical but cash-generative firm gets straight debt",
                design["convertible"]["convertible_yes_no"] is False)
    assert_true("cyclicality still produces a cash-flow-linked feature",
                any("output" in f for f in design["special_features"]))

    # Read bottom-up instead, the route the lecture designs from: duration 4.34 years.
    bottom_up = debt_profile(dict(DISNEY_BOTTOM_UP, home_currency="USD", coupon_rate=0.05))
    check("Disney bottom-up target duration",
          bottom_up["debt_design"]["maturity"]["target_duration_years"], 4.34)
    # Maturity must come out longer than the duration it is built from.
    assert_true("matching par bond matures after the duration",
                bottom_up["debt_design"]["maturity"]["matching_par_bond"]["maturity_years"]
                > 4.34)
    # Bottom-up cyclicality of 0.55 is below one-for-one, so no output-linked feature.
    assert_true("mild cyclicality raises no output-linked feature",
                not bottom_up["debt_design"]["convertible"]["cyclical"])

    # A young, high-growth firm with no current cash flow gets convertible debt instead.
    young = dict(EXAMPLES["debt-profile"])
    young["expected_revenue_growth"] = 0.35
    young["current_cash_flow_positive"] = False
    assert_true("high growth without current cash flow gets convertible debt",
                debt_profile(young)["debt_design"]["convertible"]["convertible_yes_no"])

    # Slopes that do not clear the bar must not produce a confident design.
    noisy = {k: dict(v) for k, v in DISNEY_REGRESSIONS.items()}
    for block in noisy.values():
        block["t_statistic"] = 0.39
    noisy["home_currency"] = "USD"
    weak = debt_profile(noisy)
    check("no usable slopes", len(weak["evidence_summary"]["usable_for_design"]), 0)
    assert_true("a design resting on noise says so",
                "rests on nothing" in weak["evidence_summary"]["headline"])
    assert_true("noisy inflation and rate slopes do not buy a big floating share",
                weak["debt_design"]["fixed_versus_floating"]["floating_share"]
                < design["fixed_versus_floating"]["floating_share"])

    # A short sample cannot buy significance either, however large the t-statistic.
    short = {k: dict(v, t_statistic=9.0, observations=8)
             for k, v in DISNEY_REGRESSIONS.items()}
    assert_true("eight observations block every slope from driving the design",
                len(debt_profile(short)["evidence_summary"]["usable_for_design"]) == 0)

    # Reading a coefficient off the wrong dependent variable is flagged, not silently used.
    swapped = {k: dict(v) for k, v in DISNEY_REGRESSIONS.items()}
    swapped["inflation"] = dict(swapped["inflation"], dependent="firm_value")
    assert_true("reading inflation off firm value is flagged",
                bool(debt_profile(swapped)["convention_warnings"]))
    # And omitting the operating-income rate regression is flagged rather than assumed.
    fallback = {k: dict(v) for k, v in DISNEY_REGRESSIONS.items()
                if k != "operating_income_on_interest_rate"}
    assert_true("falling back to the firm-value rate slope is flagged",
                any("fell back" in w
                    for w in debt_profile(fallback)["convention_warnings"]))

    refuses("debt-profile without all four regressions is refused",
            lambda: debt_profile({"interest_rate": {"slope": -4.0}}))
    refuses("a non-numeric slope is refused", lambda: debt_profile(
        {k: {"slope": "big"} for k in MACRO_VARIABLES}))
    refuses("a bare list passed as history is refused", lambda: regress({
        "dependent": "firm_value", "macro_variable": "inflation",
        "history": [1.0, 2.0, 3.0, 4.0, 5.0],
        "macro_changes": [0.01, 0.02, 0.03, 0.04]}))
    refuses("a malformed revenue_by_currency row is refused", lambda: debt_profile(
        dict(DISNEY_REGRESSIONS, revenue_by_currency=["USD"])))

    failed = [r for r in results if not r["pass"]]
    _emit({"total": len(results), "passed": len(results) - len(failed),
           "failed": len(failed), "results": results})
    return 1 if failed else 0


# ------------------------------------------------------------------------------- main

COMMANDS = {
    "regress": cmd_regress,
    "duration": cmd_duration,
    "debt-profile": cmd_debt_profile,
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
    try:
        return COMMANDS[args.command](args) or 0
    except FileNotFoundError:
        raise SystemExit("Input file not found: %s" % args.in_file)


if __name__ == "__main__":
    sys.exit(main())

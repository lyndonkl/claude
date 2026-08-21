#!/usr/bin/env python3
"""
costofcapital.py — the discount-rate engine.

Every function here is a pure numeric transform: the same inputs always give the same
outputs. Choosing the inputs (which comparables, which equity risk premium estimator,
gross or net debt) is the analyst's job and happens outside this script.

Pure standard library. No third-party packages, ever — this must run anywhere.

SUBCOMMANDS
  rating            interest coverage -> synthetic rating, spread, pre-tax cost of debt
  beta              unlever / relever / bottom-up beta from comparables
  mv-debt           book debt + interest expense -> market value of debt
  wacc              assemble the full cost of capital
  debt-schedule     cost of capital across every debt ratio -> the optimal
  implied-erp       index level + expected cash flows -> the equity risk premium priced in
  apv               unlevered value + tax shield - bankruptcy cost, at every debt ratio
  stress            re-run the debt schedule under weaker EBIT, and price a rating floor
  convert-rate      restate a discount rate in another currency
  selftest          run the bundled worked examples and report pass/fail

Each subcommand reads a JSON payload (--in FILE, or stdin) and writes JSON to stdout.
Run any subcommand with --example to print a sample input payload.
"""

import argparse
import json
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DEFAULT_RATINGS = os.path.join(DATA_DIR, "synthetic_ratings.json")
DEFAULT_DEFAULT_PROBS = os.path.join(DATA_DIR, "default_probabilities.json")

# A coverage ratio this negative is the sentinel Damodaran's sheets use to force the
# bottom (default) rating row when EBIT is negative or interest is zero.
NEGATIVE_EBIT_SENTINEL = -100000.0

# Fixed-point loops below converge in a handful of passes; 100 is a generous ceiling that
# still terminates promptly if a pathological input oscillates.
MAX_ITERATIONS = 100
# Rates are compared at 1e-10 because they are decimals near 0.05 — far tighter than any
# input precision, so convergence is limited by the data, not the tolerance.
TOLERANCE = 1e-10

# Bisection halves the bracket each pass, so 200 passes drive a 20-point rate bracket down
# to about 1e-61 — far past the point where floating point can still tell the ends apart.
MAX_SOLVER_ITERATIONS = 200
# The implied-return search starts just above the terminal growth rate. Exactly at it the
# terminal value divides by zero, so the bracket opens one nano-point above.
GROWTH_EPSILON = 1e-9
# Damodaran's implied-premium sheets bracket the expected return within 20 points of the
# terminal growth rate. A premium outside that is a data problem, not a solver problem.
DEFAULT_MAX_PREMIUM = 0.20
# The number of explicit high-growth years in the standard implied-premium form.
DEFAULT_HIGH_GROWTH_YEARS = 5


# --------------------------------------------------------------------------- helpers

def _load_ratings(path=None):
    with open(path or DEFAULT_RATINGS) as f:
        return json.load(f)


def _load_default_probabilities(path=None):
    with open(path or DEFAULT_DEFAULT_PROBS) as f:
        return json.load(f)


def _require(payload, key, hint):
    """Fetch a mandatory input, or say what is missing and what it is for."""
    value = payload.get(key)
    if value is None:
        raise SystemExit(
            "Missing required input %r. %s Run this subcommand with --example to see the "
            "expected shape." % (key, hint)
        )
    return value


def _number(value, label):
    """Coerce an input to float, or name the field that is not a number."""
    try:
        return float(value)
    except (TypeError, ValueError):
        raise SystemExit(
            "%s must be a number, got %r. Check the payload for a quoted number, a null, "
            "or a list where a single value belongs." % (label, value)
        )


def _rating_ladder(ratings_path=None):
    """Ratings ordered best to worst.

    The order is derived from the default spreads rather than hard-coded, because a lower
    spread *is* what a better rating means. Deriving it means a refreshed spread file
    carries its own ladder with it, and there is no second list to keep in step.
    """
    spreads = _load_ratings(ratings_path)["rating_to_spread"]
    # The map carries a prose "comment" key alongside the ratings; drop anything whose
    # value is not a number before sorting.
    numeric = {k: v for k, v in spreads.items() if isinstance(v, (int, float))}
    return sorted(numeric, key=lambda k: numeric[k])


def _rating_rank(rating, ladder):
    """Position on the ladder, 0 being the best rating. Lower rank is safer.

    Never compare rating strings directly: alphabetically "B1/B+" sorts before
    "Baa2/BBB", which inverts an investment-grade rating against a junk one.
    """
    if rating not in ladder:
        raise SystemExit(
            "Unknown rating %r. Use one of: %s" % (rating, ", ".join(ladder))
        )
    return ladder.index(rating)


def _default_probability(rating, table):
    """Cumulative default probability for a rating, accepting agency-style aliases."""
    probs = table["probabilities"]
    if rating in probs:
        return probs[rating]
    alias = table.get("aliases", {}).get(rating)
    if alias in probs:
        return probs[alias]
    raise SystemExit(
        "No default probability for rating %r. The bundled table (as of %s) covers: %s"
        % (rating, table.get("as_of", "?"), ", ".join(probs))
    )


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


# ----------------------------------------------------------------------- rating logic

def synthetic_rating(interest_coverage, table_name="large_manufacturing", ratings_path=None):
    """Map an interest coverage ratio to a synthetic rating and default spread.

    Selects the last band whose lower bound the coverage ratio reaches, which is what the
    approximate-match VLOOKUP in the source spreadsheets does. Only `icr_low` participates;
    `icr_high` is carried in the data for readability. Matching on both bounds would leave
    coverage ratios in the gaps between bands (8.4999995, say) unmatched.

    On a band edge the higher rating wins: coverage of exactly 8.5 reads as Aaa/AAA.
    """
    tables = _load_ratings(ratings_path)
    if table_name not in tables["tables"]:
        raise SystemExit(
            "Unknown rating table %r. Available: %s"
            % (table_name, ", ".join(sorted(tables["tables"])))
        )
    rows = tables["tables"][table_name]["rows"]
    match = rows[0]
    for row in rows:
        if interest_coverage >= row["icr_low"]:
            match = row
        else:
            break
    return {"rating": match["rating"], "spread": match["spread"],
            "table": table_name, "as_of": tables["as_of"]}


def interest_coverage(ebit, interest_expense):
    """Interest coverage with the degenerate cases handled the way the source models do."""
    if interest_expense is None or interest_expense == 0:
        # No debt service: coverage is effectively infinite, so return the top of the scale.
        return 100000.0 if (ebit is None or ebit >= 0) else NEGATIVE_EBIT_SENTINEL
    if ebit is not None and ebit < 0:
        return NEGATIVE_EBIT_SENTINEL
    return ebit / interest_expense


def cost_of_debt(riskfree_rate, company_spread, country_spread=0.0, marginal_tax_rate=0.0):
    pre_tax = riskfree_rate + company_spread + country_spread
    return {
        "pre_tax_cost_of_debt": pre_tax,
        "after_tax_cost_of_debt": pre_tax * (1 - marginal_tax_rate),
        "components": {"riskfree_rate": riskfree_rate, "company_default_spread": company_spread,
                       "country_default_spread": country_spread},
    }


def cmd_rating(args):
    p = _read_payload(args)
    ebit = p.get("ebit")
    interest = p.get("interest_expense")
    icr = p.get("interest_coverage_ratio")
    if icr is None:
        icr = interest_coverage(ebit, interest)
    r = synthetic_rating(icr, p.get("table", "large_manufacturing"), p.get("ratings_path"))
    cd = cost_of_debt(p["riskfree_rate"], r["spread"], p.get("country_default_spread", 0.0),
                      p.get("marginal_tax_rate", 0.0))
    _emit({"interest_coverage_ratio": icr, **r, **cd})


# ------------------------------------------------------------------------- beta logic

def unlever_beta(levered_beta, marginal_tax_rate, debt_equity_ratio, cash_percent=0.0):
    """Strip financial leverage (and optionally cash) out of an observed levered beta."""
    unlevered = levered_beta / (1 + (1 - marginal_tax_rate) * debt_equity_ratio)
    out = {"unlevered_beta": unlevered}
    if cash_percent:
        # Cash carries a beta of zero, so it drags the observed beta down; correcting for it
        # gives the beta of the operating business alone.
        out["unlevered_beta_corrected_for_cash"] = unlevered / (1 - cash_percent)
    return out


def relever_beta(unlevered_beta, marginal_tax_rate, debt_equity_ratio):
    return {"levered_beta": unlevered_beta * (1 + (1 - marginal_tax_rate) * debt_equity_ratio)}


def bottom_up_beta(businesses, marginal_tax_rate=None, debt_equity_ratio=None):
    """Value-weight comparable unlevered betas across a firm's businesses.

    Each business needs `unlevered_beta` and a weight basis: either an explicit
    `estimated_value`, or `revenue` together with `ev_to_sales` (the route the source
    models take when segment values are not disclosed).
    """
    rows = []
    for b in businesses:
        value = b.get("estimated_value")
        if value is None:
            if b.get("revenue") is None or b.get("ev_to_sales") is None:
                raise SystemExit(
                    "Business %r needs either estimated_value, or revenue and ev_to_sales."
                    % b.get("name", "?")
                )
            value = b["revenue"] * b["ev_to_sales"]
        rows.append({"name": b.get("name"), "unlevered_beta": b["unlevered_beta"],
                     "estimated_value": value})
    total = sum(r["estimated_value"] for r in rows)
    if total <= 0:
        raise SystemExit("Total estimated business value must be positive to weight betas.")
    for r in rows:
        r["weight"] = r["estimated_value"] / total
    blended = sum(r["unlevered_beta"] * r["weight"] for r in rows)
    out = {"businesses": rows, "total_value": total, "unlevered_beta": blended}
    if marginal_tax_rate is not None and debt_equity_ratio is not None:
        out.update(relever_beta(blended, marginal_tax_rate, debt_equity_ratio))
    return out


def total_beta(market_beta, r_squared=None, correlation=None):
    """Beta for an undiversified owner: market beta scaled up by 1/correlation.

    R-squared from the beta regression is the squared correlation with the market, so
    correlation = sqrt(R-squared).
    """
    if correlation is None:
        if r_squared is None:
            raise SystemExit("total beta needs either r_squared or correlation.")
        if not 0 < r_squared <= 1:
            raise SystemExit("r_squared must be between 0 and 1.")
        correlation = r_squared ** 0.5
    if not 0 < correlation <= 1:
        raise SystemExit("correlation must be between 0 and 1.")
    return {"market_beta": market_beta, "correlation": correlation,
            "total_beta": market_beta / correlation}


def cmd_beta(args):
    p = _read_payload(args)
    op = p.get("operation", "bottom-up")
    if op == "unlever":
        _emit(unlever_beta(p["levered_beta"], p["marginal_tax_rate"],
                           p["debt_equity_ratio"], p.get("cash_percent", 0.0)))
    elif op == "relever":
        _emit(relever_beta(p["unlevered_beta"], p["marginal_tax_rate"], p["debt_equity_ratio"]))
    elif op == "total":
        _emit(total_beta(p["market_beta"], p.get("r_squared"), p.get("correlation")))
    elif op == "bottom-up":
        _emit(bottom_up_beta(p["businesses"], p.get("marginal_tax_rate"),
                             p.get("debt_equity_ratio")))
    else:
        raise SystemExit("operation must be one of: unlever, relever, total, bottom-up")


# --------------------------------------------------------------- market value of debt

def market_value_of_debt(book_debt, interest_expense, pre_tax_cost_of_debt,
                         average_maturity, lease_debt=0.0):
    """Value all interest-bearing debt as one coupon bond.

    Interest expense is the coupon, book debt the face value, average maturity the term,
    and the pre-tax cost of debt the discount rate. Capitalized leases are already a
    present value, so they are added after, not discounted again.
    """
    r = pre_tax_cost_of_debt
    n = average_maturity
    if r <= 0:
        # A zero or negative discount rate makes the annuity formula blow up; with no
        # time value the market value is simply the undiscounted sum.
        mv = interest_expense * n + book_debt
    else:
        annuity = interest_expense * (1 - (1 + r) ** -n) / r
        mv = annuity + book_debt / (1 + r) ** n
    return {"market_value_of_debt": mv + lease_debt,
            "market_value_excluding_leases": mv,
            "lease_debt": lease_debt,
            "book_debt": book_debt}


def cmd_mv_debt(args):
    p = _read_payload(args)
    _emit(market_value_of_debt(p["book_debt"], p["interest_expense"],
                               p["pre_tax_cost_of_debt"], p["average_maturity"],
                               p.get("lease_debt", 0.0)))


# ------------------------------------------------------------------------------ wacc

def effective_tax_rate_for_interest(ebit, interest_expense, marginal_tax_rate):
    """Interest only shelters income that exists.

    Once interest exceeds EBIT the excess earns no current tax benefit, so the tax rate
    applied to the cost of debt is scaled down by the share of interest actually shielded.
    """
    if interest_expense <= 0 or marginal_tax_rate <= 0:
        return marginal_tax_rate
    if ebit is None:
        return marginal_tax_rate
    if ebit <= 0:
        return 0.0
    if interest_expense <= ebit:
        return marginal_tax_rate
    return marginal_tax_rate * (ebit / interest_expense)


def wacc(cost_of_equity, pre_tax_cost_of_debt, tax_rate, equity_value, debt_value,
         preferred_value=0.0, cost_of_preferred=0.0):
    total = equity_value + debt_value + preferred_value
    if total <= 0:
        raise SystemExit("Total capital must be positive.")
    we, wd, wp = equity_value / total, debt_value / total, preferred_value / total
    after_tax_kd = pre_tax_cost_of_debt * (1 - tax_rate)
    return {
        "wacc": we * cost_of_equity + wd * after_tax_kd + wp * cost_of_preferred,
        "weights": {"equity": we, "debt": wd, "preferred": wp},
        "cost_of_equity": cost_of_equity,
        "after_tax_cost_of_debt": after_tax_kd,
        "pre_tax_cost_of_debt": pre_tax_cost_of_debt,
        "tax_rate_applied": tax_rate,
        "total_capital": total,
    }


def cmd_wacc(args):
    p = _read_payload(args)
    ke = p.get("cost_of_equity")
    if ke is None:
        ke = p["riskfree_rate"] + p["levered_beta"] * p["equity_risk_premium"]
    tax = p.get("tax_rate")
    if tax is None:
        tax = effective_tax_rate_for_interest(
            p.get("ebit"), p.get("interest_expense", 0.0), p.get("marginal_tax_rate", 0.0))
    out = wacc(ke, p["pre_tax_cost_of_debt"], tax, p["equity_value"], p["debt_value"],
               p.get("preferred_value", 0.0), p.get("cost_of_preferred", 0.0))
    if p.get("currency"):
        out["currency"] = p["currency"]
    _emit(out)


# -------------------------------------------------------------- optimal debt schedule

def solve_cost_of_debt(dollar_debt, ebit, riskfree_rate, table="large_manufacturing",
                       ratings_path=None, country_spread=0.0):
    """Fixed point on the interest rate for one dollar debt level.

    The rate sets interest expense, interest expense sets the coverage ratio, and the
    coverage ratio sets the rate. It converges because a higher rate lowers coverage,
    which raises the rate by less on each pass.
    """
    # Seeded a point above the riskfree rate — roughly an investment-grade spread, so the
    # first pass starts inside the plausible range instead of at zero credit risk.
    kd = riskfree_rate + 0.01
    rating = spread = icr = None
    for _ in range(MAX_ITERATIONS):
        interest = dollar_debt * kd
        icr = interest_coverage(ebit, interest)
        r = synthetic_rating(icr, table, ratings_path)
        new_kd = riskfree_rate + r["spread"] + country_spread
        rating, spread = r["rating"], r["spread"]
        if abs(new_kd - kd) < TOLERANCE:
            kd = new_kd
            break
        kd = new_kd
    return {"pre_tax_cost_of_debt": kd, "interest_expense": dollar_debt * kd,
            "interest_coverage_ratio": icr, "rating": rating, "default_spread": spread}


def debt_ratio_schedule(payload):
    """Cost of capital at every debt ratio, and the ratio that minimizes it.

    At each candidate debt ratio the engine relevers the beta, sizes the debt, and then
    solves a fixed point: the interest rate sets interest expense, interest expense sets
    the coverage ratio, and the coverage ratio sets the interest rate. It converges
    because a higher rate lowers coverage, which raises the rate by less each pass.
    """
    unlevered = payload["unlevered_beta"]
    rf = payload["riskfree_rate"]
    erp = payload["equity_risk_premium"]
    ebit = payload["ebit"]
    marginal_tax = payload["marginal_tax_rate"]
    firm_value = payload["firm_value"]
    table = payload.get("table", "large_manufacturing")
    ratings_path = payload.get("ratings_path")
    country_spread = payload.get("country_default_spread", 0.0)
    ratios = payload.get("debt_ratios") or [i / 10.0 for i in range(0, 10)]
    shares = payload.get("shares_outstanding")

    rows = []
    for d in ratios:
        e = 1.0 - d
        if e <= 0:
            # A 100% debt firm has no equity to lever; the source schedules stop at 90%.
            continue
        de = d / e
        levered = unlevered * (1 + (1 - marginal_tax) * de)
        ke = rf + levered * erp
        dollar_debt = d * firm_value

        priced = solve_cost_of_debt(dollar_debt, ebit, rf, table, ratings_path, country_spread)
        kd = priced["pre_tax_cost_of_debt"]
        interest = priced["interest_expense"]
        icr = priced["interest_coverage_ratio"]
        rating, spread = priced["rating"], priced["default_spread"]
        tax_applied = effective_tax_rate_for_interest(ebit, interest, marginal_tax)
        after_tax_kd = kd * (1 - tax_applied)
        cost_of_capital = e * ke + d * after_tax_kd
        rows.append({
            "debt_ratio": d, "debt_equity_ratio": de, "levered_beta": levered,
            "cost_of_equity": ke, "dollar_debt": dollar_debt, "interest_expense": interest,
            "interest_coverage_ratio": icr, "rating": rating, "default_spread": spread,
            "pre_tax_cost_of_debt": kd, "tax_rate_applied": tax_applied,
            "after_tax_cost_of_debt": after_tax_kd, "cost_of_capital": cost_of_capital,
        })

    best = min(rows, key=lambda r: r["cost_of_capital"])
    current = payload.get("current_debt_ratio")
    out = {"schedule": rows, "optimal": best}

    if current is not None:
        cur = min(rows, key=lambda r: abs(r["debt_ratio"] - current))
        out["current"] = cur
        # Value the move as a perpetuity: the same cash flow discounted at a lower rate.
        # Growth defaults to zero, the conservative reading the source models use for the
        # incremental approach.
        g = payload.get("stable_growth_rate", 0.0)
        wacc_now, wacc_opt = cur["cost_of_capital"], best["cost_of_capital"]
        if wacc_now > g and wacc_opt > g:
            fcff = payload.get("fcff")
            if fcff is None:
                fcff = firm_value * (wacc_now - g)
            v_now = fcff / (wacc_now - g)
            v_opt = fcff / (wacc_opt - g)
            out["value_effect"] = {
                "firm_value_at_current": v_now,
                "firm_value_at_optimal": v_opt,
                "value_created": v_opt - v_now,
                "assumed_fcff": fcff,
                "stable_growth_rate": g,
            }
            if shares:
                out["value_effect"]["value_created_per_share"] = (v_opt - v_now) / shares
    return out


def cmd_debt_schedule(args):
    _emit(debt_ratio_schedule(_read_payload(args)))


# ---------------------------------------------------------------- implied equity risk

def index_present_value(expected_return, cash_flows, terminal_growth):
    """Present value of an index's cash flows: explicit years, then a perpetuity.

    The cash flows are dividends plus buybacks — everything the index returns to its
    investors. Using dividends alone roughly halves the answer in a market where buybacks
    dominate, which is every recent year in the United States.
    """
    pv = 0.0
    for t, cf in enumerate(cash_flows, 1):
        pv += cf / (1 + expected_return) ** t
    n = len(cash_flows)
    terminal_value = (cash_flows[-1] * (1 + terminal_growth)
                      / (expected_return - terminal_growth))
    return {"present_value": pv + terminal_value / (1 + expected_return) ** n,
            "present_value_explicit_years": pv,
            "terminal_value": terminal_value,
            "present_value_of_terminal_value": terminal_value / (1 + expected_return) ** n}


def _implied_erp_cash_flows(payload, index_level):
    """Build the explicit-year cash flow path from whichever inputs were supplied."""
    if payload.get("cash_flows") is not None:
        flows = payload["cash_flows"]
        if not flows:
            raise SystemExit("cash_flows is empty. Supply at least one explicit year.")
        return [_number(cf, "cash_flows entry") for cf in flows]

    if payload.get("earnings") is not None:
        earnings = payload["earnings"]
        payout = _require(payload, "payout_ratios",
                          "Supply payout_ratios alongside earnings, one per year.")
        if len(earnings) != len(payout):
            raise SystemExit(
                "earnings has %d entries but payout_ratios has %d. They must line up "
                "year for year." % (len(earnings), len(payout)))
        return [_number(e, "earnings entry") * _number(p, "payout_ratios entry")
                for e, p in zip(earnings, payout)]

    base = payload.get("base_cash_flow")
    if base is None:
        yield_ = payload.get("cash_yield", payload.get("dividend_yield"))
        if yield_ is None:
            raise SystemExit(
                "No cash flows. Supply one of: cash_flows (a list of expected dividends "
                "plus buybacks), earnings with payout_ratios, base_cash_flow with "
                "growth_rate, or dividend_yield with growth_rate.")
        base = index_level * _number(yield_, "dividend_yield")
    base = _number(base, "base_cash_flow")
    growth = _number(_require(payload, "growth_rate",
                              "It is the expected growth in index cash flows over the "
                              "explicit years."), "growth_rate")
    years = int(payload.get("high_growth_years", DEFAULT_HIGH_GROWTH_YEARS))
    if years < 1:
        raise SystemExit("high_growth_years must be at least 1.")
    return [base * (1 + growth) ** t for t in range(1, years + 1)]


def implied_erp(payload):
    """Solve for the expected return the index level already prices in.

    The historical premium is an average with a standard error wide enough to swamp it —
    roughly two points on a five-point estimate over ninety years of data. This estimator
    has no standard error at all. It asks a different question: given what you pay for the
    index today and what you expect it to pay you, what return are you earning? Subtract
    the riskfree rate and that is the premium the market is charging right now.
    """
    index_level = _number(_require(payload, "index_level",
                                   "It is the current level of the index."), "index_level")
    riskfree = _number(_require(payload, "riskfree_rate",
                                "It anchors the premium and caps terminal growth."),
                       "riskfree_rate")
    if index_level <= 0:
        raise SystemExit("index_level must be positive.")

    flows = _implied_erp_cash_flows(payload, index_level)
    if flows[-1] <= 0:
        raise SystemExit(
            "The final expected cash flow is %g. With no cash returned to investors the "
            "index is worth nothing at every discount rate, so no premium is implied. "
            "Normalise the base cash flow to a sustainable level first." % flows[-1])

    # A perpetual growth rate above the riskfree rate makes the terminal value grow faster
    # than the economy forever. Damodaran's convention is to set the two equal; anything
    # higher inflates the terminal value and mechanically depresses the solved return.
    requested_g = payload.get("terminal_growth_rate")
    requested_g = riskfree if requested_g is None else _number(requested_g,
                                                              "terminal_growth_rate")
    g = min(requested_g, riskfree)

    max_premium = _number(payload.get("max_premium", DEFAULT_MAX_PREMIUM), "max_premium")
    lo, hi = g + GROWTH_EPSILON, g + max_premium

    def pv(r):
        return index_present_value(r, flows, g)["present_value"]

    # The present value falls monotonically in the discount rate, so if even the top of
    # the bracket still values the index above its price, the premium is off the scale.
    if pv(hi) > index_level:
        raise SystemExit(
            "At an expected return of %.2f%% the cash flows are still worth %.2f against "
            "an index level of %.2f, so the implied premium exceeds max_premium (%.2f). "
            "Either the cash flows are overstated or the index is in a crisis; raise "
            "max_premium to search further." % (hi * 100, pv(hi), index_level, max_premium))

    for _ in range(MAX_SOLVER_ITERATIONS):
        mid = (lo + hi) / 2
        if pv(mid) > index_level:
            lo = mid
        else:
            hi = mid
    r = (lo + hi) / 2

    parts = index_present_value(r, flows, g)
    return {
        "index_level": index_level,
        "expected_cash_flows": flows,
        "high_growth_years": len(flows),
        "terminal_growth_rate": g,
        "terminal_growth_rate_requested": requested_g,
        "terminal_growth_capped_at_riskfree": g < requested_g,
        "riskfree_rate": riskfree,
        "implied_expected_return": r,
        "implied_erp": r - riskfree,
        "terminal_value": parts["terminal_value"],
        "reconstructed_index_level": parts["present_value"],
        "present_value_of_explicit_years": parts["present_value_explicit_years"],
        "present_value_of_terminal_value": parts["present_value_of_terminal_value"],
    }


def cmd_implied_erp(args):
    _emit(implied_erp(_read_payload(args)))


# ----------------------------------------------------------- adjusted present value

def apv(payload):
    """Value the firm additively: unlevered, plus the tax shield, minus expected distress.

    The cost of capital approach buries the cost of debt's risk inside a default spread.
    APV drags it into the open: how much is the tax shield worth, and what is the expected
    cost of the bankruptcy that borrowing makes more likely. The two soft numbers — the
    bankruptcy cost percentage and the default probability — drive the answer, so treat
    the optimum as a region, not a point.
    """
    equity = _number(_require(payload, "equity_value",
                              "It is the market value of equity."), "equity_value")
    debt = _number(_require(payload, "debt_value",
                            "It is the market value of interest-bearing debt."), "debt_value")
    lease_debt = _number(payload.get("lease_debt", 0.0), "lease_debt")
    tax = _number(_require(payload, "marginal_tax_rate",
                           "It sets the size of the tax shield."), "marginal_tax_rate")
    bc_pct = _number(_require(payload, "bankruptcy_cost_pct",
                              "It is total bankruptcy cost as a fraction of firm value: "
                              "direct costs run 5-10%, and Damodaran's worked examples "
                              "use 0.25 once indirect costs are included."),
                     "bankruptcy_cost_pct")
    table_name = payload.get("table", "large_manufacturing")
    ratings_path = payload.get("ratings_path")
    probs = _load_default_probabilities(payload.get("probabilities_path"))
    ladder = _rating_ladder(ratings_path)

    # Cash is deliberately not netted out. The debt ratios below are ratios of this same
    # gross figure, so netting here without netting there would mismatch the two.
    firm_value = equity + debt + lease_debt
    if firm_value <= 0:
        raise SystemExit("Firm value (equity + debt + leases) must be positive.")
    total_debt = debt + lease_debt

    ebit = payload.get("ebit")
    riskfree = payload.get("riskfree_rate")
    ratios = payload.get("debt_ratios") or [i / 10.0 for i in range(0, 10)]
    explicit = payload.get("ratings")
    if explicit is not None and len(explicit) != len(ratios):
        raise SystemExit(
            "ratings has %d entries but debt_ratios has %d. Supply one rating per debt "
            "ratio, or drop ratings and supply ebit and riskfree_rate so the synthetic "
            "rating can be solved for." % (len(explicit), len(ratios)))
    if explicit is None and (ebit is None or riskfree is None):
        raise SystemExit(
            "Rating at each debt ratio is unknown. Either supply ebit and riskfree_rate "
            "so the coverage-based synthetic rating can be solved for, or supply a "
            "ratings list with one entry per debt ratio.")

    # Back the unlevered value out of today's price: strip out the tax benefit the market
    # already pays for, and add back the expected bankruptcy cost it already charges for.
    country_spread = payload.get("country_default_spread", 0.0)
    current_rating = payload.get("current_rating")
    if current_rating is None:
        current_rating = solve_cost_of_debt(
            total_debt, ebit, _number(riskfree, "riskfree_rate"), table_name,
            ratings_path, country_spread)["rating"]
    current_p = _default_probability(current_rating, probs)
    current_tax_benefit = total_debt * tax
    current_bankruptcy_cost = current_p * bc_pct * firm_value
    unlevered_value = firm_value - current_tax_benefit + current_bankruptcy_cost

    rows = []
    for i, d in enumerate(ratios):
        d = _number(d, "debt_ratios entry")
        dollar_debt = d * firm_value
        interest = None
        kd = None
        icr = None
        if explicit is not None:
            rating = explicit[i]
            _rating_rank(rating, ladder)  # reject a typo here rather than mispricing it
            if riskfree is not None:
                kd = _number(riskfree, "riskfree_rate") + \
                    _load_ratings(ratings_path)["rating_to_spread"][rating]
                interest = dollar_debt * kd
        else:
            priced = solve_cost_of_debt(
                dollar_debt, ebit, _number(riskfree, "riskfree_rate"), table_name,
                ratings_path, country_spread)
            rating, kd = priced["rating"], priced["pre_tax_cost_of_debt"]
            interest, icr = priced["interest_expense"], priced["interest_coverage_ratio"]

        # The shield is worth the marginal rate only on interest that has income to
        # shelter. Past that point the excess interest earns nothing.
        if interest is None or ebit is None:
            tax_applied = tax
        else:
            tax_applied = effective_tax_rate_for_interest(ebit, interest, tax)
        tax_benefit = dollar_debt * tax_applied

        p_default = _default_probability(rating, probs)
        # apv.xls charges the bankruptcy percentage against the value that would be at
        # risk at this debt level — unlevered value plus the shield — not against today's
        # market value. The lecture version uses current firm value; the two differ by
        # little and the choice must be stated, not drifted between.
        expected_bankruptcy_cost = p_default * bc_pct * (unlevered_value + tax_benefit)
        levered_value = unlevered_value + tax_benefit - expected_bankruptcy_cost
        rows.append({
            "debt_ratio": d, "dollar_debt": dollar_debt, "rating": rating,
            "pre_tax_cost_of_debt": kd, "interest_expense": interest,
            "interest_coverage_ratio": icr, "tax_rate_applied": tax_applied,
            "tax_benefit": tax_benefit, "probability_of_default": p_default,
            "expected_bankruptcy_cost": expected_bankruptcy_cost,
            "levered_firm_value": levered_value,
        })

    best = max(rows, key=lambda r: r["levered_firm_value"])
    return {
        "current": {
            "firm_value": firm_value, "total_debt": total_debt,
            "current_debt_ratio": total_debt / firm_value, "rating": current_rating,
            "probability_of_default": current_p, "tax_benefit": current_tax_benefit,
            "expected_bankruptcy_cost": current_bankruptcy_cost,
        },
        "unlevered_value": unlevered_value,
        "bankruptcy_cost_pct": bc_pct,
        "schedule": rows,
        "optimal": best,
        "max_levered_firm_value": best["levered_firm_value"],
        "value_gain_at_optimal": best["levered_firm_value"] - firm_value,
        "default_probabilities_as_of": probs.get("as_of"),
    }


def cmd_apv(args):
    _emit(apv(_read_payload(args)))


# ------------------------------------------------------- downside stress and constraints

def stdev_of_percent_change(series):
    """Sample standard deviation of year-over-year percentage changes.

    Sample, not population: an EBIT history is a draw from the firm's possible outcomes,
    not the whole population of them.
    """
    if len(series) < 3:
        raise SystemExit(
            "ebit_history needs at least three years to give two changes and a standard "
            "deviation. Supply a longer history or set the haircuts directly.")
    changes = []
    for prev, cur in zip(series, series[1:]):
        prev = _number(prev, "ebit_history entry")
        if prev == 0:
            raise SystemExit(
                "ebit_history contains a zero, so a percentage change from it is "
                "undefined. Use absolute recession_ebit levels instead.")
        changes.append(_number(cur, "ebit_history entry") / prev - 1)
    mean = sum(changes) / len(changes)
    variance = sum((c - mean) ** 2 for c in changes) / (len(changes) - 1)
    return {"percent_changes": changes, "mean_percent_change": mean,
            "stdev_of_percent_change_in_ebit": variance ** 0.5}


def _schedule_at_ebit(payload, ebit):
    """Re-run the standard schedule with operating income replaced. Nothing else moves."""
    trial = dict(payload)
    trial["ebit"] = ebit
    # Only the cost-of-capital columns are wanted here, so drop the inputs that would make
    # debt_ratio_schedule value the move as well.
    trial.pop("current_debt_ratio", None)
    return debt_ratio_schedule(trial)


def _summarise(row):
    return {"debt_ratio": row["debt_ratio"], "rating": row["rating"],
            "cost_of_capital": row["cost_of_capital"],
            "cost_of_equity": row["cost_of_equity"],
            "pre_tax_cost_of_debt": row["pre_tax_cost_of_debt"]}


def stress(payload):
    """Stress the optimal debt ratio against weaker earnings, and price a rating floor.

    The optimum comes out of one number held fixed: operating income. Real operating
    income moves, so there are two protections. Haircut EBIT and watch how far the answer
    holds — that gap is the safety buffer. Or impose a minimum rating and pay for it.

    Use one or the other. They guard the same risk, so applying both leaves the firm
    arbitrarily under-levered for reasons nobody wrote down.
    """
    base_ebit = _number(_require(payload, "ebit",
                                 "It is the operating income the base schedule runs on."),
                        "ebit")
    base = debt_ratio_schedule(payload)
    base_optimal = base["optimal"]
    out = {"base": {"ebit": base_ebit, "optimal": _summarise(base_optimal)},
           "schedule": base["schedule"]}

    scenarios = []

    haircuts = payload.get("haircuts")
    if haircuts is None and payload.get("recession_ebit") is None \
            and payload.get("ebit_history") is None:
        # The lecture default: 10% steps down to a 60% collapse, which spans the worst
        # single year most non-financial firms have on record.
        haircuts = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    for h in haircuts or []:
        h = _number(h, "haircuts entry")
        ebit_h = base_ebit * (1 - h)
        row = _schedule_at_ebit(payload, ebit_h)["optimal"]
        scenarios.append({"scenario": "ebit down %.0f%%" % (h * 100), "haircut": h,
                          "ebit": ebit_h, "optimal": _summarise(row)})

    if payload.get("recession_ebit") is not None:
        rec = _number(payload["recession_ebit"], "recession_ebit")
        row = _schedule_at_ebit(payload, rec)["optimal"]
        scenarios.append({"scenario": "stated recession level",
                          "haircut": 1 - rec / base_ebit if base_ebit else None,
                          "ebit": rec, "optimal": _summarise(row)})

    if payload.get("ebit_history") is not None:
        vol = stdev_of_percent_change(payload["ebit_history"])
        # Three standard deviations is the deliverable's convention: a decline that deep
        # is rare enough that surviving it is a fair definition of financial safety.
        n_sigma = _number(payload.get("n_sigma", 3), "n_sigma")
        sigma = vol["stdev_of_percent_change_in_ebit"]
        stressed = base_ebit * (1 - n_sigma * sigma)
        vol["n_sigma"] = n_sigma
        vol["stressed_ebit"] = stressed
        if stressed > 0:
            vol["optimal"] = _summarise(_schedule_at_ebit(payload, stressed)["optimal"])
            scenarios.append({"scenario": "%g sigma decline" % n_sigma,
                              "haircut": n_sigma * sigma, "ebit": stressed,
                              "optimal": vol["optimal"]})
        else:
            vol["note"] = ("A %g sigma decline wipes out operating income entirely, so "
                           "there is no schedule to run. The firm's EBIT history is too "
                           "volatile for this test to say anything." % n_sigma)
        out["ebit_volatility"] = vol

    out["scenarios"] = scenarios
    if scenarios:
        # The safety buffer is how far EBIT can fall before the answer changes. Scenarios
        # with no haircut figure (an absolute recession level on zero base EBIT) sit out.
        held = [s["haircut"] for s in scenarios
                if s["haircut"] is not None
                and s["optimal"]["debt_ratio"] >= base_optimal["debt_ratio"]]
        out["safety_buffer"] = {
            "largest_decline_the_optimum_survives": max(held) if held else 0.0,
            "base_optimal_debt_ratio": base_optimal["debt_ratio"],
            "reading": ("Compare this against the firm's worst recorded annual decline. "
                        "More buffer than history has ever required means a rating "
                        "constraint would be paying for protection already in hand."),
        }

    required = payload.get("required_rating")
    if required is not None:
        out["rating_constraint"] = rating_constraint(base, required,
                                                     payload.get("ratings_path"))
    return out


def rating_constraint(schedule_output, required_rating, ratings_path=None):
    """The highest debt ratio that still earns a floor rating, and what it costs.

    Priced two ways. The cost of capital given up is the honest number and always
    available. The firm value given up needs a cash flow and a growth rate, and is the
    number to put in front of a board, because "sixteen basis points" does not land the
    way "five billion dollars" does.
    """
    ladder = _rating_ladder(ratings_path)
    floor = _rating_rank(required_rating, ladder)
    rows = schedule_output["schedule"]
    qualifying = [r for r in rows if _rating_rank(r["rating"], ladder) <= floor]
    if not qualifying:
        raise SystemExit(
            "No debt ratio in the schedule earns a rating of %s or better — not even zero "
            "debt, which rates %s. The floor is unreachable at this level of operating "
            "income." % (required_rating, rows[0]["rating"]))

    constrained = max(qualifying, key=lambda r: r["debt_ratio"])
    unconstrained = schedule_output["optimal"]
    given_up = constrained["cost_of_capital"] - unconstrained["cost_of_capital"]
    out = {
        "required_rating": required_rating,
        "constrained_optimal": _summarise(constrained),
        "unconstrained_optimal": _summarise(unconstrained),
        "cost_of_capital_given_up": given_up,
        "binds": constrained["debt_ratio"] < unconstrained["debt_ratio"],
    }
    effect = schedule_output.get("value_effect")
    if effect:
        g = effect["stable_growth_rate"]
        fcff = effect["assumed_fcff"]
        wacc_c, wacc_u = constrained["cost_of_capital"], unconstrained["cost_of_capital"]
        if wacc_c > g and wacc_u > g:
            v_c, v_u = fcff / (wacc_c - g), fcff / (wacc_u - g)
            out["firm_value_at_constrained"] = v_c
            out["firm_value_at_unconstrained"] = v_u
            out["value_given_up"] = v_u - v_c
    return out


def cmd_stress(args):
    _emit(stress(_read_payload(args)))


# ------------------------------------------------------------------- currency of rate

def convert_rate(rate, inflation_target_currency, inflation_base_currency):
    """Restate a discount rate from one currency into another via expected inflation.

    Uses the exact differential-inflation form, not the additive approximation.
    """
    converted = (1 + rate) * (1 + inflation_target_currency) / (1 + inflation_base_currency) - 1
    return {"input_rate": rate, "converted_rate": converted,
            "inflation_target_currency": inflation_target_currency,
            "inflation_base_currency": inflation_base_currency}


def cmd_convert_rate(args):
    p = _read_payload(args)
    _emit(convert_rate(p["rate"], p["inflation_target_currency"], p["inflation_base_currency"]))


# ---------------------------------------------------------------------------- selftest

EXAMPLES = {
    "rating": {"ebit": 2000.0, "interest_expense": 250.0, "riskfree_rate": 0.0169,
               "marginal_tax_rate": 0.25, "table": "large_manufacturing"},
    "beta": {"operation": "bottom-up", "marginal_tax_rate": 0.25, "debt_equity_ratio": 0.7069,
             "businesses": [{"name": "Software", "revenue": 32357.0, "ev_to_sales": 4.0,
                             "unlevered_beta": 1.14}]},
    "mv-debt": {"book_debt": 16715192.0, "interest_expense": 351778.0,
                "pre_tax_cost_of_debt": 0.03281066, "average_maturity": 3.0},
    "wacc": {"riskfree_rate": 0.0169, "levered_beta": 1.74919699,
             "equity_risk_premium": 0.05174663, "pre_tax_cost_of_debt": 0.03281066,
             "tax_rate": 0.25, "equity_value": 22864600.0, "debt_value": 16161914.12,
             "currency": "KRW"},
    "debt-schedule": {"unlevered_beta": 0.9, "riskfree_rate": 0.04, "equity_risk_premium": 0.05,
                      "ebit": 1000.0, "marginal_tax_rate": 0.25, "firm_value": 12000.0,
                      "current_debt_ratio": 0.1},
    "implied-erp": {"index_level": 3756.07,
                    "cash_flows": [123.43, 137.67, 153.54, 171.21, 190.88],
                    "riskfree_rate": 0.0093, "terminal_growth_rate": 0.0093},
    "apv": {"equity_value": 121878.0, "debt_value": 15961.0, "marginal_tax_rate": 0.361,
            "bankruptcy_cost_pct": 0.25, "current_rating": "A2/A",
            "debt_ratios": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
            "ratings": ["Aaa/AAA", "Aaa/AAA", "Aaa/AAA", "Aa2/AA", "A2/A", "B3/B-"]},
    "stress": {"unlevered_beta": 0.9, "riskfree_rate": 0.04, "equity_risk_premium": 0.05,
               "ebit": 1000.0, "marginal_tax_rate": 0.25, "firm_value": 12000.0,
               "current_debt_ratio": 0.1, "haircuts": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
               "required_rating": "A2/A"},
    "convert-rate": {"rate": 0.08, "inflation_target_currency": 0.06,
                     "inflation_base_currency": 0.02},
}

# January 2021 S&P 500, the current edition's mature-market premium. Earnings and cash
# payout ratios as published; the product is the dividends-plus-buybacks path.
_SP500_JAN_2021 = {
    "index_level": 3756.07,
    "earnings": [138.55, 152.62, 168.11, 185.18, 203.98],
    "payout_ratios": [0.8909, 0.9021, 0.9133, 0.9246, 0.9358],
    "riskfree_rate": 0.0093,
}

# Hormel, apv.xls (2009), on the small-or-risky ratings table with bankruptcy costs at
# 25% of value. The optimum lands at 80% rather than 70% purely because the default
# probability column is non-monotonic across the BB/B range.
_HORMEL_APV = {
    "equity_value": 4181.0675, "debt_value": 492.1725, "marginal_tax_rate": 0.4,
    "bankruptcy_cost_pct": 0.25, "current_rating": "Aaa/AAA",
    "debt_ratios": [0.7, 0.8], "ratings": ["B1/B+", "Ba1/BB+"],
}

# Disney, 2013 (cfpacket2spr20). Equity 121,878 and debt 15,961 at a 36.1% marginal rate,
# bankruptcy costs 25% of value. Ratings are the published ones, so the test exercises the
# APV arithmetic rather than re-deriving a 2013 spread table. Interest stays below EBIT
# across this range, so the effective tax rate is the marginal rate throughout.
_DISNEY_APV = {
    "equity_value": 121878.0, "debt_value": 15961.0, "marginal_tax_rate": 0.361,
    "bankruptcy_cost_pct": 0.25, "current_rating": "A2/A",
    "debt_ratios": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
    "ratings": ["Aaa/AAA", "Aaa/AAA", "Aaa/AAA", "Aa2/AA", "A2/A", "B3/B-"],
}

# Disney's operating income 1987-2013 ($m), the history behind the published 19.17%
# standard deviation of annual percentage changes.
_DISNEY_EBIT_HISTORY = [
    756, 848, 1177, 1368, 1124, 1287, 1560, 1804, 2262, 3024, 3945, 3843, 3580, 2525,
    2832, 2384, 2713, 4048, 4107, 5355, 6829, 7404, 5697, 6726, 7781, 8863, 9450,
]


def _close(actual, expected, tol=1e-6):
    return abs(actual - expected) <= tol * max(1.0, abs(expected))


def cmd_selftest(args):
    """Worked examples taken from the source models, so a port can be verified."""
    results = []

    def check(name, actual, expected, tol=1e-6):
        ok = _close(actual, expected, tol)
        results.append({"case": name, "expected": expected, "actual": actual, "pass": ok})

    # SK Innovation (fcffsimpleginzu.xlsx). Negative EBIT drives the sentinel and a D rating.
    icr = interest_coverage(-250829.0, 351778.0)
    check("negative EBIT -> sentinel coverage", icr, NEGATIVE_EBIT_SENTINEL)
    check("sentinel coverage -> D spread",
          synthetic_rating(icr, "large_manufacturing")["spread"], 0.1744)

    # Band edges resolve upward, and the gaps between bands stay covered.
    check("coverage 8.4 -> AA spread",
          synthetic_rating(8.4, "large_manufacturing")["spread"], 0.0085)
    check("coverage exactly 8.5 -> AAA spread",
          synthetic_rating(8.5, "large_manufacturing")["spread"], 0.0069)
    check("coverage in the gap between bands still resolves",
          synthetic_rating(8.4999995, "large_manufacturing")["spread"], 0.0085)

    # SK Innovation levered beta: unlevered 1.14316151, tax 25%, D/E = 16161914.12/22864600.
    de = 16161914.12 / 22864600.0
    check("relever to SK Innovation levered beta",
          relever_beta(1.14316151, 0.25, de)["levered_beta"], 1.74919699, 1e-6)

    # Cost of equity and WACC from the same sheet.
    ke = 0.0169 + 1.74919699 * 0.05174663
    check("SK Innovation cost of equity", ke, 0.10741506, 1e-6)
    w = wacc(ke, 0.03281066, 0.25, 22864600.0, 16161914.12)
    check("SK Innovation WACC", w["wacc"], 0.07312245558, 1e-6)
    check("SK Innovation after-tax cost of debt", w["after_tax_cost_of_debt"], 0.02460799, 1e-6)
    check("SK Innovation equity weight", w["weights"]["equity"], 0.58587349, 1e-6)

    # Market value of debt for the same firm, at its 3-year weighted-average maturity.
    mv = market_value_of_debt(16715192.0, 351778.0, 0.03281066, 3.0)
    check("SK Innovation market value of debt", mv["market_value_of_debt"], 16161914.12, 1e-6)
    # Below-market coupon must price at a discount to face.
    results.append({"case": "discount bond prices below book", "expected": True, "actual": True,
                    "pass": mv["market_value_of_debt"] < 16715192.0})

    # Unlever then relever must round-trip.
    rt = unlever_beta(relever_beta(0.8, 0.3, 0.5)["levered_beta"], 0.3, 0.5)["unlevered_beta"]
    check("unlever/relever round trip", rt, 0.8)

    # Total beta: market beta over the correlation implied by R-squared.
    check("total beta from R-squared", total_beta(0.8, r_squared=0.16)["total_beta"], 2.0)

    # Interest that exceeds EBIT only shelters the part that exists.
    check("tax benefit capped by EBIT",
          effective_tax_rate_for_interest(100.0, 200.0, 0.4), 0.2)
    check("no tax benefit when EBIT negative",
          effective_tax_rate_for_interest(-50.0, 200.0, 0.4), 0.0)

    # Currency conversion: 8% USD at 6% vs 2% inflation.
    check("currency conversion of a discount rate",
          convert_rate(0.08, 0.06, 0.02)["converted_rate"], 1.08 * 1.06 / 1.02 - 1)

    # The debt schedule must be internally coherent.
    sched = debt_ratio_schedule(EXAMPLES["debt-schedule"])
    opt = sched["optimal"]
    results.append({"case": "debt schedule returns 10 rows",
                    "expected": 10, "actual": len(sched["schedule"]),
                    "pass": len(sched["schedule"]) == 10})
    results.append({"case": "optimal minimizes cost of capital", "expected": True,
                    "actual": True,
                    "pass": all(r["cost_of_capital"] >= opt["cost_of_capital"] - 1e-12
                                for r in sched["schedule"])})
    zero = sched["schedule"][0]
    results.append({"case": "zero debt gives unlevered cost of equity", "expected": True,
                    "actual": zero["cost_of_equity"],
                    "pass": _close(zero["cost_of_equity"], 0.04 + 0.9 * 0.05)})

    # --- Implied equity risk premium (M25) ------------------------------------------
    # January 1, 2021 S&P 500: index 3756.07 against expected dividends plus buybacks of
    # 123.43, 137.67, 153.54, 171.21, 190.88, growing at the 0.93% bond rate thereafter.
    sp = implied_erp(_SP500_JAN_2021)
    check("Jan-2021 S&P 500 implied expected return", sp["implied_expected_return"],
          0.0565, 2e-3)
    check("Jan-2021 S&P 500 implied ERP", sp["implied_erp"], 0.0472, 2e-3)
    check("implied ERP reconstructs the index level",
          sp["reconstructed_index_level"], 3756.07, 1e-9)
    # The earnings-times-payout route must reproduce the published cash flow path.
    check("earnings x payout gives the published year-1 cash flow",
          sp["expected_cash_flows"][0], 123.43, 1e-3)

    # implprem.xls, the dividend-only calculator: index 1418.3 at a 3.75% dividend yield,
    # 6% growth for five years, a 4.7% bond rate used as terminal growth.
    ip = implied_erp({"index_level": 1418.3, "dividend_yield": 0.0375, "growth_rate": 0.06,
                      "riskfree_rate": 0.047})
    check("implprem.xls implied premium", ip["implied_erp"], 0.04157534555252903, 1e-6)
    check("implprem.xls year-5 dividend", ip["expected_cash_flows"][-1], 71.17520013, 1e-6)

    # Sensex, 9/5/2007: a non-US index run through the identical procedure.
    sx = implied_erp({"index_level": 15446.0, "dividend_yield": 0.0305, "growth_rate": 0.14,
                      "riskfree_rate": 0.0676})
    check("Sensex 2007 implied expected return", sx["implied_expected_return"], 0.1118, 1e-3)
    check("Sensex 2007 implied ERP", sx["implied_erp"], 0.0442, 1e-3)

    # Terminal growth above the riskfree rate is capped, not honoured. A wrong
    # implementation that honours it reports a materially lower premium.
    capped = implied_erp(dict(_SP500_JAN_2021, terminal_growth_rate=0.04))
    results.append({"case": "terminal growth capped at the riskfree rate",
                    "expected": 0.0093, "actual": capped["terminal_growth_rate"],
                    "pass": capped["terminal_growth_rate"] == 0.0093
                    and capped["terminal_growth_capped_at_riskfree"]})
    check("capping restores the uncapped premium", capped["implied_erp"], sp["implied_erp"],
          1e-9)

    # --- Adjusted present value (M54) -----------------------------------------------
    # Hormel (apv.xls): firm value 4,673.240, tax benefit 196.869, expected bankruptcy
    # cost 0.81782 at its AAA rating.
    hormel = apv(_HORMEL_APV)
    check("Hormel current firm value", hormel["current"]["firm_value"], 4673.240, 1e-9)
    check("Hormel current tax benefit", hormel["current"]["tax_benefit"], 196.869, 1e-9)
    check("Hormel current expected bankruptcy cost",
          hormel["current"]["expected_bankruptcy_cost"], 0.81782, 1e-4)
    check("Hormel unlevered value", hormel["unlevered_value"], 4477.189, 1e-6)
    check("Hormel levered value at 70% debt",
          hormel["schedule"][0]["levered_firm_value"], 5424.09, 1e-6)
    check("Hormel levered value at 80% debt",
          hormel["schedule"][1]["levered_firm_value"], 5823.31, 1e-6)
    # The whole point of the Hormel case: 80% beats 70% only because the probability
    # column falls from 0.25 at B1/B+ to 0.10 at Ba1/BB+. An implementation that
    # "corrects" the table into a monotonic one picks 70% and gets this wrong.
    results.append({"case": "non-monotonic default table puts the optimum at 80%",
                    "expected": 0.8, "actual": hormel["optimal"]["debt_ratio"],
                    "pass": hormel["optimal"]["debt_ratio"] == 0.8})
    check("Ba1/BB+ default probability sits below Ba2/BB",
          hormel["schedule"][1]["probability_of_default"], 0.10, 1e-12)

    # Disney 2013: unlevered value 132,304 and an optimum at 40% worth 151,957.
    disney = apv(_DISNEY_APV)
    check("Disney unlevered value", disney["unlevered_value"], 132304.0, 1e-5)
    check("Disney expected bankruptcy cost at 40% debt",
          disney["schedule"][4]["expected_bankruptcy_cost"], 251.14, 1e-3)
    check("Disney levered value at 40% debt",
          disney["schedule"][4]["levered_firm_value"], 151957.0, 1e-5)
    check("Disney levered value at 50% debt",
          disney["schedule"][5]["levered_firm_value"], 139501.0, 1e-5)
    results.append({"case": "Disney APV optimum at 40% debt", "expected": 0.4,
                    "actual": disney["optimal"]["debt_ratio"],
                    "pass": disney["optimal"]["debt_ratio"] == 0.4})

    # --- Stress and rating constraints (M53/M56) ------------------------------------
    # Disney's EBIT history 1987-2013 gives a published 19.17% standard deviation of
    # annual percentage changes. Sample standard deviation, not population: using the
    # population divisor returns 18.79% and fails this.
    vol = stdev_of_percent_change(_DISNEY_EBIT_HISTORY)
    check("Disney stdev of % change in EBIT",
          vol["stdev_of_percent_change_in_ebit"], 0.1917, 1e-3)

    st = stress(EXAMPLES["stress"])
    # The safety-buffer shape from the source: the optimum steps down as EBIT falls and
    # never steps back up.
    ratios = [s["optimal"]["debt_ratio"] for s in st["scenarios"]]
    results.append({"case": "optimum falls monotonically with the EBIT haircut",
                    "expected": "non-increasing", "actual": ratios,
                    "pass": all(a >= b for a, b in zip(ratios, ratios[1:]))})
    results.append({"case": "the base optimum is at least the most stressed optimum",
                    "expected": True, "actual": st["base"]["optimal"]["debt_ratio"],
                    "pass": st["base"]["optimal"]["debt_ratio"] >= ratios[-1]})
    check("stress leaves the base schedule untouched",
          st["base"]["optimal"]["cost_of_capital"], sched["optimal"]["cost_of_capital"])

    # A rating floor one notch above the unconstrained optimum's rating must bind, cost
    # something, and land on a debt ratio that actually earns the floor.
    rc = st["rating_constraint"]
    results.append({"case": "rating floor binds below the unconstrained optimum",
                    "expected": True, "actual": rc["constrained_optimal"]["debt_ratio"],
                    "pass": rc["binds"] and rc["constrained_optimal"]["debt_ratio"]
                    < rc["unconstrained_optimal"]["debt_ratio"]})
    results.append({"case": "constrained ratio actually earns the required rating",
                    "expected": "A2/A or better",
                    "actual": rc["constrained_optimal"]["rating"],
                    "pass": rc["constrained_optimal"]["rating"] in ("A2/A", "A1/A+", "Aa2/AA",
                                                                    "Aaa/AAA")})
    results.append({"case": "a binding constraint costs cost of capital and value",
                    "expected": True,
                    "actual": rc["cost_of_capital_given_up"],
                    "pass": rc["cost_of_capital_given_up"] > 0
                    and rc["value_given_up"] > 0})

    # The ladder must rank by credit quality, not alphabetically: "B1/B+" sorts before
    # "Baa2/BBB" as a string, which would rate a junk bond above an investment-grade one.
    ladder = _rating_ladder()
    results.append({"case": "rating ladder ranks BBB above B+ despite the alphabet",
                    "expected": True, "actual": ladder,
                    "pass": _rating_rank("Baa2/BBB", ladder) < _rating_rank("B1/B+", ladder)
                    and _rating_rank("Aaa/AAA", ladder) == 0
                    and _rating_rank("D2/D", ladder) == len(ladder) - 1})

    failed = [r for r in results if not r["pass"]]
    _emit({"total": len(results), "passed": len(results) - len(failed),
           "failed": len(failed), "results": results})
    return 1 if failed else 0


# ------------------------------------------------------------------------------- main

COMMANDS = {
    "rating": cmd_rating, "beta": cmd_beta, "mv-debt": cmd_mv_debt, "wacc": cmd_wacc,
    "debt-schedule": cmd_debt_schedule, "implied-erp": cmd_implied_erp, "apv": cmd_apv,
    "stress": cmd_stress, "convert-rate": cmd_convert_rate, "selftest": cmd_selftest,
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
    except json.JSONDecodeError as e:
        raise SystemExit(
            "The input is not valid JSON (%s). Check for a trailing comma, a single-quoted "
            "string, or shell quoting that swallowed part of the payload." % e)
    except FileNotFoundError as e:
        raise SystemExit("Cannot open %s. Check the path." % e.filename)
    except KeyError as e:
        raise SystemExit(
            "The payload for %s is missing the field %s. Run "
            "`%s %s --example` to see the expected shape."
            % (args.command, e, os.path.basename(__file__), args.command))
    except (TypeError, ValueError) as e:
        raise SystemExit(
            "A value in the payload for %s has the wrong type or is out of range (%s). "
            "Rates belong in decimals, not percent; lists belong where lists are asked "
            "for. Run `%s %s --example` to see the expected shape."
            % (args.command, e, os.path.basename(__file__), args.command))
    except ZeroDivisionError:
        raise SystemExit(
            "A division by zero occurred in %s. The usual cause is a zero firm value, a "
            "zero share count, or a discount rate equal to the growth rate."
            % args.command)


if __name__ == "__main__":
    sys.exit(main())

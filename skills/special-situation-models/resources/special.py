#!/usr/bin/env python3
"""
special.py — valuation models for companies the standard DCF cannot handle.

Five branches for the five kinds of company, plus the private-to-public step for a firm on
its way to an offering. Which branch applies is a routing decision the analyst makes before
running anything; the script does not guess. Each branch either produces a finished number
(a probability, a discount, a per-share equity value) or the driver payload that
`dcf-valuation-engine/resources/dcf.py value` consumes.

The engine computes. The end-state margin, the sustainable return on equity, the
probability of failure and the recovery percentage are judgments and arrive as inputs.

Pure standard library. No third-party packages, ever — this must run anywhere.

SUBCOMMANDS
  distress        bond price or rating -> probability of failure; blend the two branches
  excess-return   bank equity value = book equity + PV of returns above the cost of equity
  private         total beta for an undiversified owner; two illiquidity discounts
  ipo             the bridge from a private owner's value to an offer price, line by line
  cyclical        mid-cycle earnings; revenues at today's commodity price
  young-company   revenue-target and margin path -> a dcf.py payload plus survival odds
  selftest        run the bundled worked examples and report pass/fail

Each subcommand reads a JSON payload (--in FILE, or stdin) and writes JSON to stdout.
Run any subcommand with --example to print a sample input payload.
"""

import argparse
import json
import math
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DISTRESS_REFERENCE = os.path.join(DATA_DIR, "distress_reference.json")
ILLIQUIDITY_REFERENCE = os.path.join(DATA_DIR, "illiquidity_reference.json")

# Bisection on [0, 1] halves the bracket each pass, so 200 passes is far past double
# precision; the loop exits on the width test long before reaching the ceiling.
MAX_BISECTION = 200
# The bracket is a probability or a growth rate, both order 1, so 1e-15 is the tightest
# width a double can express without the midpoint ceasing to move.
BRACKET_TOLERANCE = 1e-15

# Face value convention in Damodaran's distress.xls and in US corporate bond quoting:
# prices are quoted per 1,000 of face.
DEFAULT_FACE_VALUE = 1000.0

# The Silber (1991) restricted-stock regression, ln(RPRS) on offering characteristics.
# RPRS is the price of the restricted block relative to the traded stock.
SILBER_INTERCEPT = 4.33
SILBER_LN_REVENUE = 0.036
SILBER_LN_BLOCK = -0.142
SILBER_POSITIVE_EARNINGS = 0.174
# liqdisc.xls hard-codes the anchor firm at $10 million of revenue and positive earnings.
# Only the base discount attached to that anchor is user-settable.
SILBER_ANCHOR_REVENUE_MILLIONS = 10.0
SILBER_BASE_DISCOUNT = 0.25

# Damodaran's cross-sectional regression of bid-ask spread (as a percent of price) on
# firm characteristics, estimated on end-of-2000 data. Trading volume is set to zero for
# a private firm, which is the whole point of the route.
SPREAD_INTERCEPT = 0.145
SPREAD_LN_REVENUE = -0.0022
SPREAD_POSITIVE_EARNINGS = -0.015
SPREAD_CASH_TO_VALUE = -0.016
SPREAD_VOLUME_TO_VALUE = -0.11

# Margin convergence that halves the remaining gap each year, the shape the Amazon
# January 2000 valuation uses. Exposed as a default so `decay` can be overridden.
DEFAULT_MARGIN_DECAY = 0.5


# --------------------------------------------------------------------------- plumbing

def _parse_json(text, origin):
    try:
        payload = json.loads(text)
    except ValueError as exc:
        raise SystemExit(
            "%s is not valid JSON (%s). Run this subcommand with --example to see a "
            "payload that parses." % (origin, exc))
    if not isinstance(payload, dict):
        raise SystemExit(
            "%s parsed as %s; every subcommand expects a JSON object at the top level."
            % (origin, type(payload).__name__))
    return payload


def _read_payload(args):
    if getattr(args, "in_file", None):
        try:
            with open(args.in_file) as f:
                return _parse_json(f.read(), args.in_file)
        except (FileNotFoundError, IsADirectoryError, PermissionError) as exc:
            raise SystemExit("Cannot read %r: %s." % (args.in_file, exc.strerror))
    data = sys.stdin.read().strip()
    if not data:
        raise SystemExit(
            "No input. Pass --in FILE or pipe JSON on stdin. "
            "Run this subcommand with --example to see the expected shape."
        )
    return _parse_json(data, "stdin")


def _emit(obj):
    print(json.dumps(obj, indent=2))


def _load_reference(default_path, override=None):
    path = override or default_path
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise SystemExit(
            "Reference file %r not found. Point `reference_path` at a copy of the bundled "
            "table, or drop the field to use the one shipped with this skill." % path)


def _require(payload, key, where):
    if key not in payload or payload[key] is None:
        raise SystemExit(
            "%s needs %r. Run this subcommand with --example to see a complete payload."
            % (where, key))
    return payload[key]


def _positive(value, name, where):
    v = float(value)
    if v <= 0:
        raise SystemExit(
            "%s: %s must be greater than zero (got %g)." % (where, name, v))
    return v


def _fraction(value, name, where, upper=1.0, allow_zero=True):
    v = float(value)
    low = 0.0 if allow_zero else 1e-12
    if not low <= v <= upper:
        raise SystemExit(
            "%s: %s must be a decimal fraction between %g and %g (got %g). "
            "A percentage such as 25 should be entered as 0.25."
            % (where, name, low, upper, v))
    return v


def _expand(spec, years, label):
    """Turn a driver spec into a per-year list.

    Three shapes, matching dcf.py so a payload reads the same in both engines:
      - a number: constant across every year
      - a list: used as given, and it must be exactly `years` long
      - {"start": x, "end": y, "converge_by": n}: linear glide to y by year n, then flat
    """
    if isinstance(spec, bool):
        raise SystemExit("%s must be a number, a list, or a glide object, not a boolean." % label)
    if isinstance(spec, (int, float)):
        return [float(spec)] * years
    if isinstance(spec, list):
        if len(spec) != years:
            raise SystemExit(
                "%s has %d entries but the forecast is %d years long. Supply one entry per "
                "year, or use a {start, end, converge_by} glide."
                % (label, len(spec), years))
        return [float(v) for v in spec]
    if isinstance(spec, dict):
        start = float(_require(spec, "start", label))
        end = float(_require(spec, "end", label))
        converge_by = int(spec.get("converge_by", years))
        if converge_by < 1:
            raise SystemExit("%s.converge_by must be at least 1." % label)
        return [end if y >= converge_by else start + (end - start) * (y / converge_by)
                for y in range(1, years + 1)]
    raise SystemExit(
        "%s must be a number, a list of %d values, or a {start, end, converge_by} object."
        % (label, years))


def _second_half_fade(high, stable, years, hold_through=None):
    """Hold the high-growth value, then move linearly to the stable value by the last year.

    This is the fade Damodaran's spreadsheets apply to return on equity, payout and the
    cost of equity: constant through the first half of the forecast, then a straight line
    into the stable value. `hold_through` defaults to half the horizon, rounded down.
    """
    if years < 1:
        return []
    hold = years // 2 if hold_through is None else int(hold_through)
    hold = max(0, min(hold, years))
    steps = years - hold
    out = []
    for t in range(1, years + 1):
        if t <= hold or steps == 0:
            out.append(float(high))
        else:
            out.append(float(high) + (float(stable) - float(high)) * (t - hold) / steps)
    return out


def _ols(x, y):
    """Least-squares fit of y on a single x, returned with R-squared.

    Written out rather than imported because the script must run on a bare Python.
    """
    n = len(x)
    if n != len(y):
        raise SystemExit("The commodity price and revenue histories must be the same length.")
    if n < 3:
        raise SystemExit(
            "A revenue-on-price regression needs at least three observations; got %d. "
            "Supply `intercept` and `slope` directly if you fitted it elsewhere." % n)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    sxx = sum((xi - mean_x) ** 2 for xi in x)
    if sxx == 0:
        raise SystemExit(
            "Every commodity price in the history is identical, so revenues cannot be "
            "regressed on price. Use a longer history that spans a cycle.")
    sxy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    syy = sum((yi - mean_y) ** 2 for yi in y)
    slope = sxy / sxx
    return {"intercept": mean_y - slope * mean_x, "slope": slope,
            "r_squared": (sxy * sxy) / (sxx * syy) if syy > 0 else None,
            "observations": n}


# ------------------------------------------------------- branch 1: distress adjustment

def bond_implied_distress(coupon_rate, maturity_years, riskfree_rate, market_price,
                          face_value=DEFAULT_FACE_VALUE):
    """Invert a traded bond price for the annual probability of distress.

    The promised coupons and principal are weighted by the probability the firm survives
    to pay them and discounted at the riskfree rate, so all the credit risk sits in the
    survival weights. Discounting at the bond's own yield instead would count it twice.
    Recovery in distress is assumed to be zero, which is a modelling choice: assuming a
    positive recovery would lower the implied probability for the same price.
    """
    maturity = int(maturity_years)
    if maturity < 1:
        raise SystemExit("bond.maturity_years must be a whole number of years, at least 1.")
    face = _positive(face_value, "bond.face_value", "distress")
    price = _positive(market_price, "bond.market_price", "distress")
    if riskfree_rate <= -1:
        raise SystemExit("distress: bond.riskfree_rate must be above -100%.")
    coupon = float(coupon_rate) * face

    def model_price(p):
        total = 0.0
        survival = 1.0
        discount = 1.0
        for t in range(1, maturity + 1):
            survival *= (1.0 - p)
            discount *= (1.0 + riskfree_rate)
            cash_flow = coupon + (face if t == maturity else 0.0)
            total += cash_flow * survival / discount
        return total

    default_free = model_price(0.0)
    if price >= default_free:
        return {
            "annual_probability": 0.0,
            "model_price": default_free,
            "default_free_price": default_free,
            "note": ("The bond trades at or above the riskfree-discounted value of its "
                     "promised payments (%.2f), so the market is pricing in no distress. "
                     "Reported as zero rather than solved." % default_free),
        }

    # model_price falls monotonically from default_free at p=0 to 0 at p=1, so the root
    # is unique and bisection cannot land on the wrong branch.
    lo, hi = 0.0, 1.0
    for _ in range(MAX_BISECTION):
        if hi - lo <= BRACKET_TOLERANCE:
            break
        mid = (lo + hi) / 2
        if model_price(mid) > price:
            lo = mid
        else:
            hi = mid
    probability = (lo + hi) / 2
    return {"annual_probability": probability, "model_price": model_price(probability),
            "default_free_price": default_free}


def cumulative_probability(annual, years):
    return 1.0 - (1.0 - annual) ** years


def annual_from_cumulative(cumulative, years):
    if cumulative >= 1.0:
        return 1.0
    return 1.0 - (1.0 - cumulative) ** (1.0 / years)


def _resolve_distress_probability(p):
    horizon = int(p.get("horizon_years", 10))
    if horizon < 1:
        raise SystemExit("distress: horizon_years must be at least 1.")

    if p.get("bond"):
        bond = p["bond"]
        solved = bond_implied_distress(
            _require(bond, "coupon_rate", "distress.bond"),
            _require(bond, "maturity_years", "distress.bond"),
            _require(bond, "riskfree_rate", "distress.bond"),
            _require(bond, "market_price", "distress.bond"),
            bond.get("face_value", DEFAULT_FACE_VALUE))
        annual = solved["annual_probability"]
        out = {"source": "traded bond price", "annual_probability": annual,
               "cumulative_probability": cumulative_probability(annual, horizon),
               "bond_model_price": solved["model_price"],
               "bond_default_free_price": solved["default_free_price"]}
        if solved.get("note"):
            out["note"] = solved["note"]
        out["horizon_years"] = horizon
        return out

    if p.get("annual_probability") is not None:
        annual = _fraction(p["annual_probability"], "annual_probability", "distress")
        return {"source": "stated annual probability", "annual_probability": annual,
                "cumulative_probability": cumulative_probability(annual, horizon),
                "horizon_years": horizon}

    if p.get("cumulative_probability") is not None:
        cum = _fraction(p["cumulative_probability"], "cumulative_probability", "distress")
        return {"source": "stated cumulative probability", "cumulative_probability": cum,
                "annual_probability": annual_from_cumulative(cum, horizon),
                "horizon_years": horizon}

    if p.get("rating"):
        ref = _load_reference(DISTRESS_REFERENCE, p.get("reference_path"))
        table = ref["rating_cumulative_default_10y"]["rates"]
        rating = str(p["rating"]).upper()
        if rating not in table:
            raise SystemExit(
                "Unknown rating %r. The bundled table covers: %s. Supply "
                "`cumulative_probability` directly if your rating scale differs."
                % (p["rating"], ", ".join(table)))
        cum10 = table[rating]
        # The table is stated over ten years; restate it to the requested horizon through
        # the implied constant annual rate rather than using a ten-year number as if it
        # were a five-year one.
        annual = annual_from_cumulative(cum10, 10)
        return {"source": "rating table (%s, as of %s)" % (rating, ref["as_of"]),
                "rating": rating, "cumulative_probability_10y": cum10,
                "annual_probability": annual,
                "cumulative_probability": cumulative_probability(annual, horizon),
                "horizon_years": horizon}

    if p.get("sector_survival"):
        ref = _load_reference(DISTRESS_REFERENCE, p.get("reference_path"))
        table = ref["sector_long_run_survival"]["rates"]
        sector = p["sector_survival"]
        if sector not in table:
            raise SystemExit(
                "Unknown sector %r. The bundled survival table covers: %s."
                % (sector, ", ".join(table)))
        cum = 1.0 - table[sector]
        return {"source": "sector long-run survival (%s, as of %s)" % (sector, ref["as_of"]),
                "cumulative_probability": cum,
                "annual_probability": annual_from_cumulative(cum, horizon),
                "horizon_years": horizon}

    raise SystemExit(
        "distress: give the probability one of five ways — `bond` (solve it from a traded "
        "price), `annual_probability`, `cumulative_probability`, `rating`, or "
        "`sector_survival`.")


def _resolve_distress_value(p, going_concern_value):
    spec = p.get("distress") or {}
    basis = spec.get("basis", "book" if spec.get("book_equity") is not None else "explicit")
    recovery = float(spec.get("recovery_percent", 0.5))

    if basis == "explicit":
        if spec.get("proceeds") is None:
            return {"basis": "explicit", "proceeds": 0.0, "distress_value": 0.0,
                    "note": "No distress branch supplied, so the distressed outcome is "
                            "valued at zero. State `distress.proceeds` if it is not."}
        proceeds = float(spec["proceeds"])
    elif basis == "book":
        book_equity = float(_require(spec, "book_equity", "distress.distress"))
        book_debt = float(_require(spec, "book_debt", "distress.distress"))
        proceeds = (book_equity + book_debt) * recovery
    elif basis in ("going_concern", "fair_value"):
        if going_concern_value is None:
            raise SystemExit(
                "distress: a going-concern recovery basis needs `going_concern_value`.")
        proceeds = going_concern_value * recovery
    else:
        raise SystemExit(
            "distress.distress.basis must be one of: book, going_concern, explicit "
            "(got %r)." % basis)

    out = {"basis": basis, "recovery_percent": recovery, "proceeds": proceeds}
    face = spec.get("debt_face_value")
    if face is not None:
        # Equity in the distress branch is a residual. If the sale proceeds fall short of
        # what the lenders are owed, shareholders receive nothing.
        residual = proceeds - float(face)
        out["debt_face_value"] = float(face)
        out["distress_value"] = max(0.0, residual)
        if residual <= 0:
            out["note"] = ("Expected proceeds of %.2f fall short of the %.2f face value of "
                           "debt, so equity is worth zero in the distress branch."
                           % (proceeds, float(face)))
    else:
        out["distress_value"] = proceeds
    return out


def distress(p):
    probability = _resolve_distress_probability(p)
    cum = probability["cumulative_probability"]
    out = {"probability": probability}

    going_concern = p.get("going_concern_value")
    if going_concern is None:
        out["next_step"] = ("Supply `going_concern_value` to blend the two branches, or "
                            "pass cumulative_probability into dcf.py's `failure` block.")
        return out
    going_concern = float(going_concern)

    loss_fraction = p.get("equity_loss_fraction")
    if loss_fraction is not None:
        # Partial wipeout: the firm survives but equity is diluted or expropriated, as in
        # a bailout. One probability, one loss fraction, applied as a single haircut.
        loss = _fraction(loss_fraction, "equity_loss_fraction", "distress")
        adjusted = going_concern * (1.0 - cum * loss)
        out["blend"] = {
            "mode": "partial wipeout",
            "going_concern_value": going_concern,
            "probability_of_failure": cum,
            "equity_loss_fraction": loss,
            "deduction": going_concern - adjusted,
            "expected_value": adjusted,
        }
    else:
        branch = _resolve_distress_value(p, going_concern)
        expected = going_concern * (1.0 - cum) + branch["distress_value"] * cum
        out["distress_branch"] = branch
        out["blend"] = {
            "mode": "two-branch blend",
            "going_concern_value": going_concern,
            "distress_value": branch["distress_value"],
            "probability_of_failure": cum,
            "expected_value": expected,
            "value_given_up": going_concern - expected,
        }

    shares = p.get("shares_outstanding")
    if shares:
        out["blend"]["expected_value_per_share"] = out["blend"]["expected_value"] / float(shares)
    return out


def cmd_distress(args):
    _emit(distress(_read_payload(args)))


# --------------------------------------- branch 2: financial service excess return model

def _is_path_spec(value):
    """True when a driver was given as a per-year list or a glide rather than one number."""
    return isinstance(value, (list, dict))


def _bank_paths(p, years, mode="retention"):
    """Return-on-equity, payout and cost-of-equity paths for the excess return model.

    Each driver accepts either a single high-growth number, which then fades to its stable
    value over the second half of the horizon, or an explicit list / glide object when the
    recovery path is not a straight line.
    """
    stable = p.get("stable") or {}
    roe_stable = float(_require(stable, "return_on_equity", "excess-return.stable"))
    g_stable = float(_require(stable, "growth_rate", "excess-return.stable"))

    riskfree = p.get("riskfree_rate")
    erp = p.get("equity_risk_premium")

    def scalar_cost_of_equity(source, allow_missing=False):
        if source.get("cost_of_equity") is not None:
            return float(source["cost_of_equity"])
        beta = source.get("beta")
        if beta is None:
            if allow_missing:
                return None
            raise SystemExit(
                "excess-return: give either a cost of equity directly (`cost_of_equity`, "
                "`stable.cost_of_equity`) or a beta with `riskfree_rate` and "
                "`equity_risk_premium`.")
        if riskfree is None:
            raise SystemExit("excess-return: a beta needs `riskfree_rate` alongside it.")
        premium = source.get("equity_risk_premium", erp)
        if premium is None:
            raise SystemExit("excess-return: `equity_risk_premium` is missing.")
        return float(riskfree) + float(beta) * float(premium)

    ke_spec = p.get("cost_of_equity")
    ke_high = None if _is_path_spec(ke_spec) else scalar_cost_of_equity(p)
    ke_stable = scalar_cost_of_equity(stable, allow_missing=True)
    if ke_stable is None:
        ke_stable = ke_high if ke_high is not None else _expand(ke_spec, years,
                                                               "cost_of_equity")[-1]

    if ke_stable <= g_stable:
        raise SystemExit(
            "excess-return: the stable cost of equity (%.4f) must exceed stable growth "
            "(%.4f), or the terminal value is infinite or negative." % (ke_stable, g_stable))

    if roe_stable == 0:
        raise SystemExit(
            "excess-return: stable.return_on_equity cannot be zero — the stable payout "
            "ratio 1 - g/ROE is undefined.")
    payout_stable = stable.get("payout_ratio")
    if payout_stable is None:
        payout_stable = 1.0 - g_stable / roe_stable
    payout_stable = float(payout_stable)
    if payout_stable < 0:
        raise SystemExit(
            "excess-return: stable growth of %.4f at a stable return on equity of %.4f "
            "implies retaining more than all earnings (payout %.4f). Lower the growth "
            "rate or raise the return." % (g_stable, roe_stable, payout_stable))

    fade = bool(p.get("fade_second_half", True))
    hold = p.get("hold_through")

    def build(spec, stable_value, label):
        if _is_path_spec(spec):
            return _expand(spec, years, label)
        value = float(spec)
        return (_second_half_fade(value, stable_value, years, hold) if fade
                else [value] * years)

    roe = build(_require(p, "return_on_equity", "excess-return"), roe_stable,
                "return_on_equity")
    ke = (_expand(ke_spec, years, "cost_of_equity") if _is_path_spec(ke_spec)
          else build(ke_high, ke_stable, "cost_of_equity"))

    payout_spec = p.get("payout_ratio")
    if payout_spec is None and p.get("retention_ratio") is not None:
        retention = p["retention_ratio"]
        payout_spec = (1.0 - float(retention) if not _is_path_spec(retention)
                       else [1.0 - r for r in _expand(retention, years, "retention_ratio")])
    if payout_spec is None:
        if mode != "regulatory_capital":
            raise SystemExit(
                "excess-return: give `retention_ratio` or `payout_ratio` for the "
                "high-growth phase.")
        # Under regulatory-capital reinvestment the payout is a residual — whatever is
        # left after funding the required capital — so it is not an input at all.
        payout_spec = payout_stable
    payout = build(payout_spec, payout_stable, "payout_ratio")

    return {"roe": roe, "payout": payout, "cost_of_equity": ke,
            "roe_stable": roe_stable, "growth_stable": g_stable,
            "payout_stable": payout_stable, "cost_of_equity_stable": ke_stable}


def _regulatory_book_equity_path(p, years):
    """Book equity a bank must hold each year, from risk-adjusted assets and the ratio.

    A bank reinvests by adding to book equity, and the regulator sets the floor. The
    year-on-year increase in required capital is the reinvestment, and it comes straight
    out of free cash flow to equity.
    """
    reg = p["regulatory_capital"]
    if reg.get("required_book_equity") is not None:
        # A bank's book equity often sits above its regulatory minimum, so the capital
        # ratio alone does not pin the book equity path down. When the path is disclosed,
        # take it as given rather than backing it out of the ratio.
        required = _expand(reg["required_book_equity"], years,
                           "regulatory_capital.required_book_equity")
        return {"risk_adjusted_assets": None, "capital_ratio": None,
                "required_book_equity": required}
    base_assets = _positive(_require(reg, "risk_adjusted_assets", "excess-return.regulatory_capital"),
                            "risk_adjusted_assets", "excess-return")
    asset_growth = _expand(reg.get("asset_growth", 0.0), years, "regulatory_capital.asset_growth")
    ratio = _expand(_require(reg, "capital_ratio", "excess-return.regulatory_capital"),
                    years, "regulatory_capital.capital_ratio")

    assets = []
    running = base_assets
    for g in asset_growth:
        running *= (1.0 + g)
        assets.append(running)
    return {"risk_adjusted_assets": assets, "capital_ratio": ratio,
            "required_book_equity": [a * r for a, r in zip(assets, ratio)]}


def excess_return(p):
    years = int(p.get("forecast_years", 10))
    if years < 0:
        raise SystemExit("excess-return: forecast_years cannot be negative.")

    book_equity = float(_require(p, "book_equity", "excess-return"))
    one_off_hit = float(p.get("one_off_capital_hit", 0.0))
    opening_equity = book_equity - one_off_hit

    mode = p.get("reinvestment", "retention")
    if mode not in ("retention", "regulatory_capital"):
        raise SystemExit(
            "excess-return: reinvestment must be 'retention' (book equity grows by retained "
            "earnings) or 'regulatory_capital' (book equity is set by the required capital "
            "ratio).")

    paths = _bank_paths(p, years, mode)
    roe, payout, ke = paths["roe"], paths["payout"], paths["cost_of_equity"]
    g_stable = paths["growth_stable"]
    ke_stable = paths["cost_of_equity_stable"]
    roe_stable = paths["roe_stable"]

    required = None
    if mode == "regulatory_capital":
        if not p.get("regulatory_capital"):
            raise SystemExit(
                "excess-return: reinvestment='regulatory_capital' needs a "
                "`regulatory_capital` block with risk_adjusted_assets and capital_ratio, "
                "or with required_book_equity stated year by year.")
        reg = _regulatory_book_equity_path(p, years)
        required = reg["required_book_equity"]

    rows = []
    equity = opening_equity
    cumulative_discount = 1.0
    for i in range(years):
        opening = equity
        net_income = roe[i] * opening
        equity_charge = ke[i] * opening
        excess = net_income - equity_charge

        if mode == "regulatory_capital":
            closing = required[i]
            investment = closing - opening
            dividends = net_income - investment
        else:
            dividends = net_income * payout[i]
            investment = net_income - dividends
            closing = opening + investment

        # Free cash flow to equity is what is left after the bank funds the book equity it
        # must hold. It is deeply negative for a bank rebuilding capital.
        fcfe = net_income - investment
        cumulative_discount *= (1.0 + ke[i])
        rows.append({
            "year": i + 1,
            "beginning_book_equity": opening,
            "return_on_equity": roe[i],
            "net_income": net_income,
            "cost_of_equity": ke[i],
            "equity_charge": equity_charge,
            "excess_equity_return": excess,
            "payout_ratio": payout[i] if mode == "retention" else (
                dividends / net_income if net_income else None),
            "dividends_or_fcfe": dividends,
            "investment_in_book_equity": investment,
            "fcfe": fcfe,
            "ending_book_equity": closing,
            "cumulative_discount_factor": 1.0 / cumulative_discount,
            "pv_excess_return": excess / cumulative_discount,
            "pv_fcfe": fcfe / cumulative_discount,
        })
        equity = closing

    closing_equity = equity
    final_discount_factor = rows[-1]["cumulative_discount_factor"] if rows else 1.0

    # Terminal year. Book equity grows at the stable rate, which is exactly what retaining
    # (1 - payout_stable) of a return of roe_stable delivers.
    terminal_net_income = roe_stable * closing_equity
    terminal_charge = ke_stable * closing_equity
    terminal_excess = terminal_net_income - terminal_charge
    terminal_investment = closing_equity * g_stable
    terminal_fcfe = terminal_net_income - terminal_investment
    tv_excess = terminal_excess / (ke_stable - g_stable)
    tv_fcfe = terminal_fcfe / (ke_stable - g_stable)

    pv_excess = sum(r["pv_excess_return"] for r in rows) + tv_excess * final_discount_factor
    equity_value = opening_equity + pv_excess
    # The same value through the cash-flow route. Residual income and discounted FCFE are
    # algebraically the same model, so a gap between them means the paths disagree.
    equity_value_fcfe = (sum(r["pv_fcfe"] for r in rows) + tv_fcfe * final_discount_factor)

    out = {
        "mode": mode,
        "opening_book_equity": opening_equity,
        "one_off_capital_hit": one_off_hit,
        "forecast": rows,
        "terminal": {
            "beginning_book_equity": closing_equity,
            "return_on_equity": roe_stable,
            "growth_rate": g_stable,
            "cost_of_equity": ke_stable,
            "payout_ratio": paths["payout_stable"],
            "net_income": terminal_net_income,
            "equity_charge": terminal_charge,
            "excess_equity_return": terminal_excess,
            "fcfe": terminal_fcfe,
            "terminal_value_of_excess_returns": tv_excess,
            "terminal_value_of_equity": tv_fcfe,
        },
        "present_value_of_excess_returns": pv_excess,
        "value_of_equity": equity_value,
        "value_of_equity_via_fcfe": equity_value_fcfe,
        "route_difference": equity_value - equity_value_fcfe,
    }

    shares = p.get("shares_outstanding")
    if shares:
        out["value_per_share"] = equity_value / float(shares)

    wipeout = p.get("probability_of_equity_wipeout")
    if wipeout:
        w = _fraction(wipeout, "probability_of_equity_wipeout", "excess-return")
        out["equity_wipeout"] = {
            "probability": w,
            "value_of_equity": equity_value * (1.0 - w),
        }
        if shares:
            out["equity_wipeout"]["value_per_share"] = out["value_per_share"] * (1.0 - w)

    if p.get("currency"):
        out["currency"] = p["currency"]
    return out


def normalize_net_income(spec, book_equity):
    """Replace an unrepresentative year's net income before computing a fundamental ROE."""
    approach = int(spec.get("approach", 1))
    if approach == 1:
        history = _require(spec, "net_income_history", "normalize")
        if not history:
            raise SystemExit("normalize: net_income_history is empty.")
        return {"approach": 1, "normalized_net_income": sum(history) / len(history),
                "basis": "average net income over %d years" % len(history)}
    if approach == 2:
        roe = float(_require(spec, "normalized_return_on_equity", "normalize"))
        return {"approach": 2, "normalized_net_income": roe * book_equity,
                "basis": "normalized return on equity applied to current book equity"}
    raise SystemExit("normalize.approach must be 1 (average net income) or 2 (normalized ROE).")


def cmd_excess_return(args):
    p = _read_payload(args)
    out = {}
    if p.get("normalize"):
        norm = normalize_net_income(p["normalize"], float(_require(p, "book_equity", "excess-return")))
        out["normalization"] = norm
        prior = p.get("prior_year_book_equity")
        if prior:
            # The fundamental return on equity convention is net income over PRIOR-year
            # book equity, while the valuation rolls forward from current book equity.
            norm["fundamental_return_on_equity"] = norm["normalized_net_income"] / float(prior)
        if p.get("return_on_equity") is None and "fundamental_return_on_equity" in norm:
            p["return_on_equity"] = norm["fundamental_return_on_equity"]
    elif p.get("return_on_equity") is None and p.get("net_income") is not None \
            and p.get("prior_year_book_equity"):
        p["return_on_equity"] = float(p["net_income"]) / float(p["prior_year_book_equity"])
        out["fundamental_return_on_equity"] = p["return_on_equity"]
    if p.get("retention_ratio") is None and p.get("payout_ratio") is None \
            and p.get("earnings_per_share") and p.get("dividends_per_share") is not None:
        p["retention_ratio"] = 1.0 - float(p["dividends_per_share"]) / float(p["earnings_per_share"])
        out["fundamental_retention_ratio"] = p["retention_ratio"]
    out.update(excess_return(p))
    _emit(out)


# ------------------------------------------------ branch 3: private company adjustments

def total_beta(market_beta, r_squared=None, correlation=None):
    """Scale a market beta up for an owner who holds nothing else.

    Betas are built from standard deviations, so the share of total risk that is market
    risk is the correlation with the market — the square root of the regression R-squared,
    not R-squared itself. Dividing by R-squared would roughly double the beta again.
    """
    if correlation is None:
        if r_squared is None:
            raise SystemExit(
                "private.total_beta needs either `r_squared` (the average R-squared of the "
                "comparables' beta regressions) or `correlation` directly.")
        r2 = float(r_squared)
        if not 0 < r2 <= 1:
            raise SystemExit("private.total_beta: r_squared must be between 0 and 1 (got %g)." % r2)
        correlation = math.sqrt(r2)
    rho = float(correlation)
    if not 0 < rho <= 1:
        raise SystemExit(
            "private.total_beta: correlation must be above 0 and at most 1 (got %g). A "
            "correlation of zero would make the total beta infinite." % rho)
    return {"correlation": rho, "market_beta": float(market_beta),
            "total_beta": float(market_beta) / rho}


def _debt_equity_from(spec, where):
    if spec.get("debt_equity_ratio") is not None:
        return float(spec["debt_equity_ratio"])
    if spec.get("debt_to_capital") is not None:
        dc = float(spec["debt_to_capital"])
        if dc >= 1:
            raise SystemExit("%s: debt_to_capital must be below 1." % where)
        return dc / (1.0 - dc)
    return 0.0


def private_cost_of_equity(spec):
    """Total beta, levered, and the cost of equity for both buyer types."""
    unlevered = float(_require(spec, "unlevered_market_beta", "private.cost_of_equity"))
    tb = total_beta(unlevered, spec.get("r_squared"), spec.get("correlation"))
    de = _debt_equity_from(spec, "private.cost_of_equity")
    tax = float(spec.get("tax_rate", 0.0))
    lever = 1.0 + (1.0 - tax) * de

    riskfree = float(_require(spec, "riskfree_rate", "private.cost_of_equity"))
    erp = float(_require(spec, "equity_risk_premium", "private.cost_of_equity"))

    levered_total = tb["total_beta"] * lever
    levered_market = unlevered * lever
    return {
        "unlevered_market_beta": unlevered,
        "correlation": tb["correlation"],
        "total_unlevered_beta": tb["total_beta"],
        "debt_equity_ratio": de,
        "tax_rate": tax,
        "levered_total_beta": levered_total,
        "levered_market_beta": levered_market,
        "cost_of_equity_undiversified_buyer": riskfree + levered_total * erp,
        "cost_of_equity_diversified_buyer": riskfree + levered_market * erp,
        "note": ("Assemble the cost of capital in cost-of-capital-toolkit: `wacc` takes "
                 "this cost of equity plus a synthetic cost of debt from `rating`."),
    }


def silber_discount(revenues_millions, positive_earnings, block_fraction=1.0,
                    base_discount=SILBER_BASE_DISCOUNT):
    """Restricted-stock illiquidity discount, the Silber-refined form used in liqdisc.xls.

    The regression predicts a discount for the subject firm and for a $10 million-revenue
    profitable anchor, and the base discount attached to the anchor is shifted by the gap.
    The block term is identical in both predictions and therefore cancels exactly; that is
    the spreadsheet's behaviour, reproduced deliberately, and it is why block size does
    not move the answer.
    """
    rev = _positive(revenues_millions, "revenues_millions", "private.illiquidity")
    block = _positive(block_fraction, "block_fraction", "private.illiquidity")
    block_percent = block * 100.0

    def score(revenue, dern):
        return (SILBER_INTERCEPT
                + SILBER_LN_REVENUE * math.log(revenue)
                + SILBER_LN_BLOCK * math.log(block_percent)
                + SILBER_POSITIVE_EARNINGS * dern)

    def predicted(revenue, dern):
        return (100.0 - math.exp(score(revenue, dern))) / 100.0

    dern = 1.0 if positive_earnings else 0.0
    anchor = predicted(SILBER_ANCHOR_REVENUE_MILLIONS, 1.0)
    firm = predicted(rev, dern)
    return {
        "method": "Silber-refined restricted stock",
        "base_discount": float(base_discount),
        "anchor_predicted_discount": anchor,
        "firm_predicted_discount": firm,
        "discount": float(base_discount) - (anchor - firm),
        "block_fraction": block,
        "block_note": ("Block size cancels between the anchor and firm terms, so it does "
                       "not change the discount."),
    }


def bid_ask_discount(revenues_millions, positive_earnings, cash_to_firm_value=0.0,
                     trading_volume_to_firm_value=0.0):
    """Illiquidity discount from the bid-ask spread regression.

    The spread is the observable cost of illiquidity for a public firm. Setting trading
    volume to zero evaluates it for a firm with no market at all. Every term subtracts
    from the intercept, so larger, profitable, cash-rich firms get smaller discounts.
    """
    rev = _positive(revenues_millions, "revenues_millions", "private.illiquidity")
    spread = (SPREAD_INTERCEPT
              + SPREAD_LN_REVENUE * math.log(rev)
              + SPREAD_POSITIVE_EARNINGS * (1.0 if positive_earnings else 0.0)
              + SPREAD_CASH_TO_VALUE * float(cash_to_firm_value)
              + SPREAD_VOLUME_TO_VALUE * float(trading_volume_to_firm_value))
    out = {"method": "bid-ask spread regression", "predicted_spread": spread,
           "discount": max(0.0, spread)}
    if spread < 0:
        out["note"] = ("The regression predicted a negative spread, which has no meaning "
                       "as a discount; clamped to zero. Check that revenues are in "
                       "millions and that trading volume is a fraction, not a dollar sum.")
    if trading_volume_to_firm_value:
        out["warning"] = ("Trading volume is non-zero. For a private firm it should be 0 — "
                          "it carries the largest coefficient and will collapse the discount.")
    return out


def private(p):
    out = {}
    if p.get("cost_of_equity"):
        out["cost_of_equity"] = private_cost_of_equity(p["cost_of_equity"])

    spec = p.get("illiquidity")
    if spec:
        rev = _require(spec, "revenues_millions", "private.illiquidity")
        profitable = bool(spec.get("positive_earnings", True))
        silber = silber_discount(rev, profitable, spec.get("block_fraction", 1.0),
                                 spec.get("base_discount", SILBER_BASE_DISCOUNT))
        spread = bid_ask_discount(rev, profitable, spec.get("cash_to_firm_value", 0.0),
                                  spec.get("trading_volume_to_firm_value", 0.0))
        flat = float(spec.get("flat_discount", SILBER_BASE_DISCOUNT))
        routes = {"flat": {"method": "flat rule of thumb", "discount": flat},
                  "silber": silber, "bid_ask": spread}

        buyer = p.get("buyer", "private")
        if buyer not in ("private", "public", "ipo"):
            raise SystemExit(
                "private.buyer must be 'private' (no liquid exit, discount applies), "
                "'public' (a listed acquirer whose own investors can sell), or 'ipo'.")
        applies = buyer == "private"

        out["illiquidity"] = {
            "buyer": buyer,
            "discount_applies": applies,
            "routes": routes,
            "spread_between_routes": max(r["discount"] for r in routes.values())
                                     - min(r["discount"] for r in routes.values()),
        }
        if not applies:
            out["illiquidity"]["note"] = (
                "A %s buyer has a liquid exit, so no illiquidity discount applies. The "
                "routes are reported for reference only." % buyer)

        equity_value = p.get("equity_value")
        if equity_value is not None:
            ev = float(equity_value)
            out["illiquidity"]["equity_value_before_discount"] = ev
            out["illiquidity"]["equity_value_after_discount"] = {
                name: ev * (1.0 - (r["discount"] if applies else 0.0))
                for name, r in routes.items()
            }
    if not out:
        raise SystemExit(
            "private: supply a `cost_of_equity` block, an `illiquidity` block, or both. "
            "Run with --example to see the shape.")
    return out


def cmd_private(args):
    _emit(private(_read_payload(args)))


# ------------------------------------------- branch 4: cyclical / commodity normalization

def normalized_ebit(spec):
    """Mid-cycle operating income by the three normalization approaches.

    Approach 3 uses the AGGREGATE margin (sum of EBIT over sum of revenues), not the
    average of the yearly margins. The two differ, and the aggregate is the one the
    source model uses.
    """
    revenues = spec.get("revenue_history") or []
    ebits = spec.get("ebit_history") or []
    history = None
    if revenues and ebits:
        if len(revenues) != len(ebits):
            raise SystemExit(
                "cyclical: revenue_history and ebit_history must be the same length "
                "(got %d and %d)." % (len(revenues), len(ebits)))
        total_revenue = sum(revenues)
        if total_revenue <= 0:
            raise SystemExit("cyclical: the revenue history sums to zero or less.")
        history = {
            "years": len(revenues),
            "total_revenue": total_revenue,
            "total_ebit": sum(ebits),
            "yearly_margins": [e / r if r else None for e, r in zip(ebits, revenues)],
            "aggregate_margin": sum(ebits) / total_revenue,
            "average_of_yearly_margins": sum(
                e / r for e, r in zip(ebits, revenues) if r) / len(revenues),
            "average_ebit": sum(ebits) / len(ebits),
        }

    approach = int(spec.get("approach", 3))
    results = {}

    if history:
        results["1_average_ebit"] = history["average_ebit"]
    if spec.get("average_ebit") is not None:
        results["1_average_ebit"] = float(spec["average_ebit"])

    if spec.get("average_pretax_return_on_capital") is not None:
        book_capital = (float(spec.get("book_value_of_debt", 0.0))
                        + float(spec.get("book_value_of_equity", 0.0)))
        results["2_return_on_capital"] = (
            float(spec["average_pretax_return_on_capital"]) * book_capital)

    current_revenues = spec.get("current_revenues")
    margin = spec.get("sector_operating_margin")
    if margin is None and history:
        margin = history["aggregate_margin"]
    if current_revenues is not None and margin is not None:
        results["3_sector_margin"] = float(current_revenues) * float(margin)

    key = {1: "1_average_ebit", 2: "2_return_on_capital", 3: "3_sector_margin"}.get(approach)
    if key is None:
        raise SystemExit(
            "cyclical.normalization.approach must be 1 (average EBIT), 2 (average return "
            "on capital times book capital) or 3 (sector margin times current revenues).")
    if key not in results:
        raise SystemExit(
            "cyclical: approach %d needs inputs that are missing. Approach 1 needs "
            "`average_ebit` or an `ebit_history`; approach 2 needs "
            "`average_pretax_return_on_capital` with book debt and equity; approach 3 "
            "needs `current_revenues` plus `sector_operating_margin` or a history."
            % approach)

    out = {"approach": approach, "approaches": results, "normalized_ebit": results[key],
           "margin_used": margin}
    if history:
        out["history"] = history
    if current_revenues:
        out["normalized_operating_margin"] = results[key] / float(current_revenues)
    return out


def commodity_revenues(spec):
    """Revenues at today's commodity price, from a fitted or supplied linear link."""
    fit = None
    if spec.get("history"):
        hist = spec["history"]
        fit = _ols([float(v) for v in _require(hist, "price", "cyclical.commodity.history")],
                   [float(v) for v in _require(hist, "revenue", "cyclical.commodity.history")])
        intercept, slope = fit["intercept"], fit["slope"]
    else:
        intercept = float(_require(spec, "intercept", "cyclical.commodity"))
        slope = float(_require(spec, "slope", "cyclical.commodity"))

    price = float(_require(spec, "price", "cyclical.commodity"))
    revenue = intercept + slope * price
    if revenue <= 0:
        raise SystemExit(
            "cyclical: the fitted relationship gives revenues of %.2f at a price of %.2f, "
            "which is not usable. Check the units of the price series." % (revenue, price))

    out = {"intercept": intercept, "slope": slope, "price": price, "revenue": revenue}
    if fit:
        out["regression"] = fit
        if fit["r_squared"] is not None and fit["r_squared"] < 0.5:
            out["warning"] = (
                "R-squared of %.4f means the commodity price explains less than half the "
                "variation in revenues. The price link is weak; normalize earnings instead."
                % fit["r_squared"])
    ladder = spec.get("price_ladder")
    if ladder:
        out["price_ladder"] = [{"price": float(x), "revenue": intercept + slope * float(x)}
                               for x in ladder]
    return out


def cyclical(p):
    out = {}
    if p.get("normalization"):
        out["normalization"] = normalized_ebit(p["normalization"])
    if p.get("commodity"):
        out["commodity"] = commodity_revenues(p["commodity"])
        out["price_neutrality"] = (
            "Report this as a value at a commodity price of %g, not as a view on the "
            "commodity. State any macro disagreement as a separate claim and rerun the "
            "ladder rather than burying it in the discount rate."
            % out["commodity"]["price"])
    if not out:
        raise SystemExit(
            "cyclical: supply a `normalization` block, a `commodity` block, or both. "
            "Run with --example to see the shape.")

    # Drivers for dcf.py, so the normalized base and the mid-cycle margin do not have to
    # be re-keyed by hand.
    base_revenue = None
    if "commodity" in out:
        base_revenue = out["commodity"]["revenue"]
    elif p.get("normalization", {}).get("current_revenues"):
        base_revenue = float(p["normalization"]["current_revenues"])

    target_margin = p.get("target_operating_margin")
    if target_margin is None and "normalization" in out:
        target_margin = out["normalization"].get("margin_used")
    base_margin = p.get("base_operating_margin")
    if base_margin is None and base_revenue and p.get("base_ebit") is not None:
        base_margin = float(p["base_ebit"]) / base_revenue

    if base_revenue and target_margin is not None:
        converge_by = int(p.get("margin_convergence_year", 5))
        out["dcf_drivers"] = {
            "base_revenue": base_revenue,
            "operating_margin": ({"start": base_margin, "end": float(target_margin),
                                  "converge_by": converge_by}
                                 if base_margin is not None else float(target_margin)),
            "note": ("Paste into a dcf-valuation-engine `value` payload. Growth, "
                     "sales-to-capital, tax rate, cost of capital, terminal block and "
                     "bridge are still yours to set; the terminal return on capital for a "
                     "cyclical should be its own long-run average, not a trough number."),
        }
    return out


def cmd_cyclical(args):
    _emit(cyclical(_read_payload(args)))


# --------------------------------------------- branch 5: young / negative-earnings build

def _fade_growth(high_rates, stable_growth, years):
    """Hold the stated high-growth rates, then fade linearly to stable growth by year n."""
    h = len(high_rates)
    if h > years:
        raise SystemExit(
            "young-company: %d high-growth rates were given but the forecast is only %d "
            "years long." % (h, years))
    out = [float(g) for g in high_rates]
    last = out[-1] if out else float(stable_growth)
    steps = years - h
    for k in range(1, steps + 1):
        out.append(last - (last - float(stable_growth)) * k / steps)
    return out


def _solve_high_growth(base_revenue, target_revenue, target_year, hold_through,
                       stable_growth, years):
    """Find the high-growth rate that lands revenue on its target in the target year.

    Revenue is monotonically increasing in the high-growth rate over any sensible range,
    so bisection on [stable_growth, 10] is safe. The upper bound of 1,000% a year is far
    above anything defensible and exists only to bracket the root.
    """
    if target_year > years:
        raise SystemExit(
            "young-company: target_year (%d) is beyond the forecast horizon (%d)."
            % (target_year, years))

    def revenue_at(g):
        path = _fade_growth([g] * hold_through, stable_growth, years)
        revenue = base_revenue
        for i in range(target_year):
            revenue *= (1.0 + path[i])
        return revenue

    lo, hi = float(stable_growth), 10.0
    if revenue_at(hi) < target_revenue:
        raise SystemExit(
            "young-company: even 1,000%% annual growth does not reach a target of %.2f "
            "from a base of %.2f by year %d. Check the units."
            % (target_revenue, base_revenue, target_year))
    if revenue_at(lo) > target_revenue:
        raise SystemExit(
            "young-company: the revenue target of %.2f is below what stable growth alone "
            "delivers by year %d. The target is not a growth story."
            % (target_revenue, target_year))
    for _ in range(MAX_BISECTION):
        if hi - lo <= BRACKET_TOLERANCE:
            break
        mid = (lo + hi) / 2
        if revenue_at(mid) < target_revenue:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _margin_path(base_margin, year1_margin, target_margin, years, style, convergence_year,
                 decay):
    """Ramp the operating margin from its current level to the mature target."""
    if style == "halving":
        # Each year closes a fixed fraction of the remaining gap to the target. This is
        # the shape the Amazon January 2000 valuation uses.
        out = []
        gap = float(target_margin) - float(base_margin)
        for _ in range(years):
            gap *= decay
            out.append(float(target_margin) - gap)
        return out
    if style == "linear":
        # The Ginzu convention: a straight line from the year-1 margin to the target by the
        # convergence year, flat at the target afterwards.
        tc = int(convergence_year)
        if tc < 1:
            raise SystemExit("young-company: margin convergence_year must be at least 1.")
        m1 = float(year1_margin if year1_margin is not None else base_margin)
        target = float(target_margin)
        return [target if t > tc else target - ((target - m1) / tc) * (tc - t)
                for t in range(1, years + 1)]
    raise SystemExit(
        "young-company: margin style must be 'halving' (close a fixed share of the gap "
        "each year) or 'linear' (straight line to a convergence year).")


def _survival(spec, reference_path=None):
    if spec.get("probability_of_failure") is not None:
        return {"source": "stated", "probability_of_failure":
                _fraction(spec["probability_of_failure"], "probability_of_failure",
                          "young-company.survival")}
    ref = _load_reference(DISTRESS_REFERENCE, reference_path)
    if spec.get("sector"):
        table = ref["sector_long_run_survival"]["rates"]
        if spec["sector"] not in table:
            raise SystemExit(
                "Unknown sector %r. The bundled long-run survival table covers: %s."
                % (spec["sector"], ", ".join(table)))
        rate = table[spec["sector"]]
        return {"source": "sector long-run survival (as of %s)" % ref["as_of"],
                "sector": spec["sector"], "survival_rate": rate,
                "probability_of_failure": 1.0 - rate}
    if spec.get("years_since_founding") is not None:
        table = ref["startup_survival_by_year"]["rates"]
        key = str(int(spec["years_since_founding"]))
        if key not in table:
            raise SystemExit(
                "The startup survival table covers years %s. Use `sector` for a longer "
                "horizon, or state `probability_of_failure` directly."
                % ", ".join(sorted(table, key=int)))
        rate = table[key]
        return {"source": "startup survival by year (as of %s)" % ref["as_of"],
                "years_since_founding": int(spec["years_since_founding"]),
                "survival_rate": rate, "probability_of_failure": 1.0 - rate}
    raise SystemExit(
        "young-company.survival needs `probability_of_failure`, `sector`, or "
        "`years_since_founding`. A young company with no failure branch is worth more "
        "than any young company has ever been worth.")


def young_company(p):
    years = int(p.get("forecast_years", 10))
    if years < 2:
        raise SystemExit("young-company: forecast_years must be at least 2.")
    base_revenue = _positive(_require(p, "base_revenue", "young-company"),
                             "base_revenue", "young-company")

    terminal = p.get("terminal") or {}
    stable_growth = float(_require(terminal, "growth_rate", "young-company.terminal"))
    riskfree = p.get("riskfree_rate")
    if riskfree is not None and stable_growth > float(riskfree) + 1e-12:
        raise SystemExit(
            "young-company: terminal growth of %.4f exceeds the riskfree rate of %.4f. A "
            "company growing faster than the economy forever becomes the economy; the "
            "riskfree rate is the practical ceiling."
            % (stable_growth, float(riskfree)))

    spec = p.get("revenue_path") or {}
    mode = spec.get("mode", "explicit")
    if mode == "explicit":
        high = [float(g) for g in _require(spec, "high_growth_rates", "young-company.revenue_path")]
        growth = _fade_growth(high, stable_growth, years)
        solved = None
    elif mode == "target_revenue":
        target_revenue = _positive(_require(spec, "target_revenue", "young-company.revenue_path"),
                                   "target_revenue", "young-company")
        target_year = int(spec.get("target_year", years))
        hold = int(spec.get("hold_through", years // 2))
        if hold < 1:
            raise SystemExit("young-company: revenue_path.hold_through must be at least 1.")
        solved = _solve_high_growth(base_revenue, target_revenue, target_year, hold,
                                    stable_growth, years)
        growth = _fade_growth([solved] * hold, stable_growth, years)
    else:
        raise SystemExit(
            "young-company.revenue_path.mode must be 'explicit' (you state the high-growth "
            "rates) or 'target_revenue' (state the revenue you expect in a given year and "
            "the engine solves for the growth rate that reaches it).")

    revenues = []
    revenue = base_revenue
    for g in growth:
        revenue *= (1.0 + g)
        revenues.append(revenue)

    margin_spec = p.get("margin") or {}
    target_margin = float(_require(margin_spec, "target_margin", "young-company.margin"))
    base_margin = margin_spec.get("base_margin")
    if base_margin is None:
        if p.get("base_ebit") is None:
            raise SystemExit(
                "young-company: give `margin.base_margin`, or `base_ebit` so the base "
                "margin can be computed from it.")
        base_margin = float(p["base_ebit"]) / base_revenue
    margins = _margin_path(float(base_margin), margin_spec.get("year1_margin"),
                           target_margin, years,
                           margin_spec.get("style", "halving"),
                           margin_spec.get("convergence_year", 5),
                           float(margin_spec.get("decay", DEFAULT_MARGIN_DECAY)))

    sales_to_capital = _expand(p.get("sales_to_capital", 3.0), years, "sales_to_capital")
    reinvestment = []
    prior = base_revenue
    for i, rev in enumerate(revenues):
        if sales_to_capital[i] <= 0:
            raise SystemExit("young-company: sales_to_capital must be positive in year %d." % (i + 1))
        step = (rev - prior) / sales_to_capital[i]
        if i == 0 and step < 0:
            step = 0.0
        reinvestment.append(step)
        prior = rev

    survival = _survival(p.get("survival") or {}, p.get("reference_path"))

    payload = {
        "base_revenue": base_revenue,
        "forecast_years": years,
        "revenue_growth": growth,
        "operating_margin": margins,
        "sales_to_capital": sales_to_capital,
        "tax_rate": p.get("tax_rate", 0.25),
        "cost_of_capital": p.get("cost_of_capital", 0.10),
        "terminal": {
            "growth_rate": stable_growth,
            "cost_of_capital": float(_require(terminal, "cost_of_capital",
                                              "young-company.terminal")),
            "return_on_capital": terminal.get(
                "return_on_capital", float(terminal.get("cost_of_capital", 0.10))),
        },
    }
    if p.get("base_ebit") is not None:
        payload["base_ebit"] = float(p["base_ebit"])
    if p.get("base_invested_capital") is not None:
        payload["base_invested_capital"] = float(p["base_invested_capital"])
    if terminal.get("operating_margin") is not None:
        payload["terminal"]["operating_margin"] = float(terminal["operating_margin"])
    else:
        payload["terminal"]["operating_margin"] = target_margin
    if terminal.get("tax_rate") is not None:
        payload["terminal"]["tax_rate"] = float(terminal["tax_rate"])
    if p.get("net_operating_loss_carryforward"):
        payload["net_operating_loss_carryforward"] = float(p["net_operating_loss_carryforward"])
    if survival["probability_of_failure"]:
        failure = {"probability": survival["probability_of_failure"]}
        distress_spec = p.get("distress") or {}
        failure["proceeds_basis"] = distress_spec.get("proceeds_basis", "book_value")
        failure["proceeds_percent"] = float(distress_spec.get("proceeds_percent", 0.5))
        if failure["proceeds_basis"] == "book_value":
            failure["book_value_of_capital"] = float(distress_spec.get(
                "book_value_of_capital", p.get("base_invested_capital", 0.0)))
        payload["failure"] = failure
    if p.get("bridge"):
        payload["bridge"] = p["bridge"]
    if p.get("currency"):
        payload["currency"] = p["currency"]

    out = {
        "revenue_path": [{"year": i + 1, "revenue_growth": growth[i], "revenue": revenues[i],
                          "operating_margin": margins[i], "ebit": revenues[i] * margins[i],
                          "reinvestment": reinvestment[i]}
                         for i in range(years)],
        "cumulative_reinvestment": sum(reinvestment),
        "survival": survival,
        "dcf_payload": payload,
        "handoff": ("python3 ../../dcf-valuation-engine/resources/dcf.py value "
                    "--in payload.json"),
    }

    tam = p.get("total_addressable_market")
    if tam:
        share = revenues[-1] / float(tam)
        out["market_share_check"] = {
            "total_addressable_market": float(tam),
            "year_%d_revenue" % years: revenues[-1],
            "implied_market_share": share,
            "verdict": ("Implausible without naming who loses this share."
                        if share > 0.25 else "Within a defensible range."),
        }
    if not payload.get("bridge"):
        out["missing_from_payload"] = [
            "bridge.debt", "bridge.cash", "bridge.shares_outstanding",
            "bridge.employee_options_value (value them in option-valuation-toolkit)",
        ]
    return out


def cmd_young_company(args):
    _emit(young_company(_read_payload(args)))


# ------------------------------------------- branch 6: the private-to-public step (IPO)

# The working range for average first-day underpricing in the source packet. It is quoted
# back to the caller when no offering discount is stated; it is never applied silently.
CUSTOMARY_OFFERING_DISCOUNT_RANGE = (0.10, 0.15)

# Each pass of the preferred waterfall flips at least one round from cash to conversion or
# back, and a repeated state ends the loop, so this ceiling is never the binding exit for a
# real cap table. It only stops a pathological oscillation.
MAX_PREFERRED_PASSES = 64


def _wacc_at(cost_of_equity, pre_tax_cost_of_debt, tax_rate, debt_equity_ratio):
    """Cost of capital at a stated debt-to-equity ratio.

    The full assembly — synthetic ratings, market value of debt, preferred stock — lives in
    cost-of-capital-toolkit. This is the two-component form the private-to-public comparison
    needs, so that the only thing changing between the two columns is the beta.
    """
    de = float(debt_equity_ratio)
    if de < 0:
        raise SystemExit("ipo: the debt-to-equity ratio cannot be negative (got %g)." % de)
    debt_weight = de / (1.0 + de)
    return (float(cost_of_equity) * (1.0 - debt_weight)
            + float(pre_tax_cost_of_debt) * (1.0 - float(tax_rate)) * debt_weight)


def _per_share(value, shares):
    return value / shares if shares else None


def offering_proceeds(spec):
    """Split the money raised into the three buckets and value each one.

    Only cash that reaches the business is worth anything to a buyer of the shares. Money
    the existing owners take out is a transfer between shareholders, so it adds nothing.
    Cash retained adds dollar for dollar; cash used to repay debt shortens the bridge by the
    same amount, so both lift equity value by the amount raised.
    """
    where = "ipo.proceeds"
    if not spec:
        return {"gross_proceeds": 0.0, "retained": 0.0, "to_owners": 0.0,
                "pay_down_debt": 0.0, "value_added": 0.0,
                "note": "No offering proceeds supplied, so nothing is added to equity."}
    gross = float(_require(spec, "gross_proceeds", where))
    if gross < 0:
        raise SystemExit("%s: gross_proceeds cannot be negative (got %g)." % (where, gross))

    buckets = {"retained": 0.0, "to_owners": 0.0, "pay_down_debt": 0.0}
    use = spec.get("use")
    if use is not None:
        if use not in buckets:
            raise SystemExit(
                "%s.use must be 'retained' (the cash stays in the firm for future "
                "reinvestment), 'to_owners' (existing owners cash out) or 'pay_down_debt' "
                "(got %r). For a mixed offering, name the three buckets in dollars instead "
                "of using `use`." % (where, use))
        buckets[use] = gross
    else:
        for name in buckets:
            buckets[name] = float(spec.get(name, 0.0))
        total = sum(buckets.values())
        if abs(total - gross) > 1e-6 * max(1.0, gross):
            raise SystemExit(
                "%s: retained + to_owners + pay_down_debt is %.4f but gross_proceeds is "
                "%.4f. The three buckets must account for every dollar raised."
                % (where, total, gross))

    out = dict(buckets)
    out["gross_proceeds"] = gross
    out["value_added"] = buckets["retained"] + buckets["pay_down_debt"]
    if buckets["to_owners"]:
        out["note"] = ("%.4f of the proceeds is being taken out by existing owners and adds "
                       "nothing to value. Those are secondary shares, already in the count, "
                       "so `shares.new_primary_shares` should not include them."
                       % buckets["to_owners"])
    if buckets["pay_down_debt"]:
        out["warning"] = (
            "%.4f of the proceeds repays debt. This bridge lowers the debt subtracted, but "
            "repaying debt also changes the debt ratio, so the cost of capital and the "
            "value of the operating assets should be recomputed at the new ratio and the "
            "run repeated." % buckets["pay_down_debt"])
    return out


def preferred_waterfall(rounds, equity_available, common_shares):
    """Split equity between preferred rounds and common when preferences are in play.

    A convertible preferred round holds two mutually exclusive rights: take the stated
    liquidation preference in cash, or convert into common and share in the upside. It takes
    whichever is worth more, and that choice moves the per-share value the other rounds are
    choosing against — so `auto` iterates to a fixed point rather than deciding each round in
    isolation. At an IPO priced well above the last round, every round converts, which is the
    customary case and the one the Twitter offering shows.
    """
    parsed = []
    for i, spec in enumerate(rounds):
        where = "ipo.convertible_preferred[%d]" % i
        if not isinstance(spec, dict):
            raise SystemExit(
                "%s must be an object with `as_converted_shares` and "
                "`liquidation_preference`." % where)
        shares = float(spec.get("as_converted_shares", 0.0))
        preference = float(spec.get("liquidation_preference", 0.0))
        if shares < 0 or preference < 0:
            raise SystemExit(
                "%s: as_converted_shares and liquidation_preference cannot be negative."
                % where)
        converts = spec.get("converts", "auto")
        if converts not in (True, False, "auto"):
            raise SystemExit(
                "%s.converts must be true (the round converts to common at the offering), "
                "false (it takes its liquidation preference in cash instead) or \"auto\" "
                "(take whichever is worth more)." % where)
        if converts is not False and shares <= 0:
            raise SystemExit(
                "%s: a round that can convert needs `as_converted_shares`; without them "
                "there is nothing to convert into." % where)
        parsed.append({"name": spec.get("name", "round %d" % (i + 1)),
                       "as_converted_shares": shares,
                       "liquidation_preference": preference,
                       "converts_input": converts})

    def evaluate(state):
        preference_paid = sum(r["liquidation_preference"]
                              for r, c in zip(parsed, state) if not c)
        converting_shares = sum(r["as_converted_shares"]
                                for r, c in zip(parsed, state) if c)
        shares = common_shares + converting_shares
        if shares <= 0:
            raise SystemExit(
                "ipo: the post-offering share count is zero. Give `shares.common_shares`, "
                "and the as-converted share count of every round that converts.")
        residual = equity_available - preference_paid
        return preference_paid, converting_shares, shares, residual, max(0.0, residual) / shares

    state = [r["converts_input"] is not False for r in parsed]
    seen = set()
    for _ in range(MAX_PREFERRED_PASSES):
        if tuple(state) in seen:
            break
        seen.add(tuple(state))
        per_share = evaluate(state)[4]
        proposed = [c if r["converts_input"] != "auto"
                    else (r["as_converted_shares"] * per_share >= r["liquidation_preference"])
                    for r, c in zip(parsed, state)]
        if proposed == state:
            break
        state = proposed

    preference_paid, converting_shares, shares, residual, per_share = evaluate(state)
    shortfall = max(0.0, preference_paid - max(0.0, equity_available))
    # Preferences rank ahead of common but not ahead of each other, so a shortfall is shared
    # pro rata among the rounds taking cash and common is left with nothing.
    scale = 1.0 if preference_paid <= 0 or shortfall <= 0 else (
        max(0.0, equity_available) / preference_paid)

    detail = []
    for r, converted in zip(parsed, state):
        paid = 0.0 if converted else r["liquidation_preference"] * scale
        detail.append({
            "name": r["name"],
            "converts": bool(converted),
            "as_converted_shares": r["as_converted_shares"],
            "liquidation_preference": r["liquidation_preference"],
            "value_to_this_round": (r["as_converted_shares"] * per_share if converted
                                    else paid),
        })

    out = {"rounds": detail,
           "converting_shares": converting_shares,
           "liquidation_preferences_paid": preference_paid * scale,
           "equity_left_for_common_and_converting_preferred": max(0.0, residual)}
    if shortfall > 0:
        out["note"] = (
            "The liquidation preferences of the rounds taking cash total %.4f against %.4f "
            "of equity, so common is wiped out and the preferences are paid pro rata. An "
            "offering at this value would not clear the preference stack."
            % (preference_paid, max(0.0, equity_available)))
    return out


def post_offering_shares(spec, converting_preferred_shares, option_shares):
    """Count every claim that becomes common, and keep options out of the count.

    Options are handled by subtracting their value from the numerator. Counting them in the
    denominator as well charges for them twice, and that is the standard error in an IPO
    bridge.
    """
    where = "ipo.shares"
    common = float(_require(spec, "common_shares", where))
    if common < 0:
        raise SystemExit("%s.common_shares cannot be negative." % where)
    parts = {
        "common_shares": common,
        "restricted_stock_units": float(spec.get("restricted_stock_units", 0.0)),
        "shares_owed_under_acquisitions": float(
            spec.get("shares_owed_under_acquisitions", 0.0)),
        "other_convertible_claims": float(spec.get("other_convertible_claims", 0.0)),
        "new_primary_shares": float(spec.get("new_primary_shares", 0.0)),
        "converting_preferred_shares": float(converting_preferred_shares),
    }
    total = sum(parts.values())
    if total <= 0:
        raise SystemExit(
            "%s: the post-offering share count came to zero. Every claim that converts to "
            "common belongs here." % where)
    out = dict(parts)
    out["post_offering_shares"] = total
    out["excluded_option_shares"] = float(option_shares)
    out["exclusion_note"] = (
        "Options and warrants are excluded from the count on purpose; their value is "
        "subtracted from equity instead. Doing both charges for them twice.")
    return out


def ipo(p):
    """Walk the bridge from a private owner's value to an IPO offer price, line by line."""
    out = {}
    steps = []

    rates = None
    if p.get("cost_of_equity"):
        spec = p["cost_of_equity"]
        rates = private_cost_of_equity(spec)
        kd = spec.get("pre_tax_cost_of_debt")
        if kd is not None:
            de, tax = rates["debt_equity_ratio"], rates["tax_rate"]
            rates["cost_of_capital_private"] = _wacc_at(
                rates["cost_of_equity_undiversified_buyer"], kd, tax, de)
            rates["cost_of_capital_public"] = _wacc_at(
                rates["cost_of_equity_diversified_buyer"], kd, tax, de)
        rates["note"] = (
            "The private owner holds one asset and prices total risk; the buyers of a "
            "listed share are diversified and price only market risk. Nothing about the "
            "cash flows changes between the two columns — only the beta.")
        out["cost_of_equity"] = rates

    cash = float(p.get("cash", 0.0))
    debt = float(p.get("debt", 0.0))
    proceeds = offering_proceeds(p.get("proceeds"))
    out["proceeds"] = proceeds

    reval = p.get("revaluation")
    stated_assets = p.get("value_of_operating_assets")
    if reval:
        g = float(_require(reval, "stable_growth", "ipo.revaluation"))
        fcff = float(_require(reval, "next_year_fcff", "ipo.revaluation"))
        pair = {}
        for label, key in (("private", "cost_of_capital_private"),
                           ("public", "cost_of_capital_public")):
            rate = reval.get(key, rates.get(key) if rates else None)
            if rate is None:
                raise SystemExit(
                    "ipo.revaluation needs %s. Give it directly, or give a `cost_of_equity` "
                    "block with `pre_tax_cost_of_debt` so both costs of capital can be "
                    "assembled from the total beta and the market beta." % key)
            rate = float(rate)
            if rate <= g:
                raise SystemExit(
                    "ipo.revaluation: the %s cost of capital (%.4f) must exceed stable "
                    "growth (%.4f), or the business is worth an infinite or negative "
                    "amount." % (label, rate, g))
            pair[label] = rate
        assets_private = fcff / (pair["private"] - g)
        assets_public = fcff / (pair["public"] - g)
        out["operating_assets"] = {
            "next_year_fcff": fcff, "stable_growth": g,
            "cost_of_capital_private": pair["private"],
            "cost_of_capital_public": pair["public"],
            "value_at_the_total_beta": assets_private,
            "value_at_the_market_beta": assets_public,
            "value_created_by_diversification": assets_public - assets_private,
        }
    elif stated_assets is not None:
        assets_private = assets_public = float(stated_assets)
        out["operating_assets"] = {
            "value_at_the_market_beta": assets_public,
            "note": ("`value_of_operating_assets` is taken as already computed on a market "
                     "beta with no illiquidity discount, which is what an IPO valuation "
                     "requires. Supply a `revaluation` block instead to see what the shift "
                     "off the total beta is worth."),
        }
    else:
        raise SystemExit(
            "ipo: give `value_of_operating_assets` (the DCF value of the business, already "
            "on a market beta), or a `revaluation` block with `next_year_fcff` and "
            "`stable_growth` so the business can be valued at both discount rates.")

    pre_shares = p.get("pre_ipo_shares")
    pre_shares = float(pre_shares) if pre_shares else None

    equity_private = assets_private + cash - debt
    discount = _fraction(p.get("illiquidity_discount", 0.0), "illiquidity_discount", "ipo")
    current = equity_private * (1.0 - discount)
    current_shares = pre_shares
    start = {"step": "private value of equity",
             "equity_value_after": current,
             "shares_after": current_shares,
             "per_share_after": _per_share(current, current_shares),
             "note": ("The owner's own value: the business at the total-beta cost of "
                      "capital, less debt, less an illiquidity discount of %.4f." % discount)}
    steps.append(start)

    def step(name, value, shares, note=None):
        row = {"step": name,
               "equity_value_before": current, "equity_value_after": value,
               "change_in_value": value - current,
               "shares_before": current_shares, "shares_after": shares,
               "per_share_before": _per_share(current, current_shares),
               "per_share_after": _per_share(value, shares)}
        if row["per_share_before"] is not None and row["per_share_after"] is not None:
            row["change_per_share"] = row["per_share_after"] - row["per_share_before"]
        if note:
            row["note"] = note
        steps.append(row)
        return value, shares

    if discount:
        current, current_shares = step(
            "remove the illiquidity discount", equity_private, current_shares,
            "The shares will trade, so the discount that priced the absence of a market "
            "comes off in full.")

    if reval:
        equity_public = assets_public + cash - debt
        current, current_shares = step(
            "revalue at the market beta", equity_public, current_shares,
            "Cost of capital falls from %.4f to %.4f because the buyers are diversified."
            % (out["operating_assets"]["cost_of_capital_private"],
               out["operating_assets"]["cost_of_capital_public"]))
    else:
        equity_public = equity_private

    if proceeds["gross_proceeds"]:
        current, current_shares = step(
            "add the offering proceeds that stay in the firm",
            equity_public + proceeds["value_added"], current_shares,
            "Raised %.4f, of which %.4f reaches the business and %.4f goes to selling "
            "owners." % (proceeds["gross_proceeds"], proceeds["value_added"],
                         proceeds["to_owners"]))
    else:
        current = equity_public

    out["value_of_equity"] = current

    claims = p.get("claims") or {}
    option_value = float(claims.get("options_and_warrants_value", 0.0))
    option_shares = float(claims.get("option_shares", 0.0))
    if option_value:
        current, current_shares = step(
            "subtract options, warrants and special claims",
            current - option_value, current_shares,
            "Valued with an option-pricing model, not counted in the denominator. IPO "
            "convention sets the expected life at half the stated life.")

    rounds = p.get("convertible_preferred") or []
    common_before_preferred = post_offering_shares(
        p.get("shares") or {}, 0.0, option_shares)["post_offering_shares"]
    if rounds:
        waterfall = preferred_waterfall(rounds, current, common_before_preferred)
        out["convertible_preferred"] = waterfall
        if waterfall["liquidation_preferences_paid"]:
            current, current_shares = step(
                "pay the liquidation preferences of rounds that do not convert",
                current - waterfall["liquidation_preferences_paid"], current_shares,
                "A preference ranks ahead of common. A round only takes it when the cash is "
                "worth more than converting.")
        converting = waterfall["converting_shares"]
    else:
        converting = 0.0

    count = post_offering_shares(p.get("shares") or {}, converting, option_shares)
    out["share_count"] = count
    out["value_of_equity_in_common_stock"] = current
    current, current_shares = step(
        "restate on the post-offering share count", current, count["post_offering_shares"],
        "Every claim that becomes common is in the denominator: converting preferred, "
        "restricted stock units, shares owed under acquisition agreements and the new "
        "shares issued at the offering.")
    value_per_share = _per_share(current, current_shares)
    out["value_per_share"] = value_per_share

    offering_discount = p.get("offering_discount")
    if offering_discount is not None:
        d = _fraction(offering_discount, "offering_discount", "ipo")
        current, current_shares = step(
            "apply the offering discount", current * (1.0 - d), current_shares,
            "The bank guarantees the offer price and carries the placement risk, so it "
            "prices below value. This is a pricing decision, not a change in value.")
        out["offer_price"] = _per_share(current, current_shares)
    else:
        out["offering_discount_note"] = (
            "No `offering_discount` supplied, so the ladder stops at value per share. The "
            "packet's working range for average first-day underpricing is %.0f%% to %.0f%%, "
            "larger for smaller deals."
            % (CUSTOMARY_OFFERING_DISCOUNT_RANGE[0] * 100,
               CUSTOMARY_OFFERING_DISCOUNT_RANGE[1] * 100))

    out["bridge"] = steps

    under = p.get("underpricing")
    if under:
        percent = _fraction(_require(under, "percent", "ipo.underpricing"), "percent",
                            "ipo.underpricing")
        fraction_offered = _fraction(
            _require(under, "fraction_offered", "ipo.underpricing"), "fraction_offered",
            "ipo.underpricing")
        total_value = under.get("total_value")
        total_value = (float(total_value) if total_value is not None
                       else out["value_of_equity_in_common_stock"])
        # The loss falls only on the shares actually sold at the offering, which is why an
        # owner floating a tenth of the company loses a tenth of what a full float loses.
        result = {"percent": percent, "fraction_offered": fraction_offered,
                  "total_value": total_value,
                  "value_of_the_stake_sold": fraction_offered * total_value,
                  "cost_of_underpricing": percent * fraction_offered * total_value}
        offer = under.get("offer_price")
        close = under.get("first_day_close")
        if offer is not None and close is not None:
            offer = _positive(offer, "offer_price", "ipo.underpricing")
            result["first_day_return"] = (float(close) - offer) / offer
        out["underpricing"] = result

    return out


def cmd_ipo(args):
    _emit(ipo(_read_payload(args)))


# ---------------------------------------------------------------------------- examples

EXAMPLES = {
    "distress": {
        "bond": {"coupon_rate": 0.06375, "maturity_years": 7, "riskfree_rate": 0.03,
                 "market_price": 529.0, "face_value": 1000.0},
        "horizon_years": 10,
        "going_concern_value": 8.12,
        "distress": {"basis": "explicit", "proceeds": 2769.0, "debt_face_value": 11000.0},
    },
    "excess-return": {
        "book_equity": 17997.0, "prior_year_book_equity": 15518.0,
        "net_income": 4791.0, "earnings_per_share": 4.75, "dividends_per_share": 0.92,
        "shares_outstanding": 1120.713,
        "beta": 1.15, "riskfree_rate": 0.05, "equity_risk_premium": 0.04,
        "forecast_years": 10, "reinvestment": "retention",
        "return_on_equity": 0.25, "retention_ratio": 0.8063157894736842,
        "fade_second_half": True,
        "stable": {"return_on_equity": 0.15, "growth_rate": 0.05, "beta": 1.10,
                   "equity_risk_premium": 0.04},
    },
    "private": {
        "buyer": "private",
        "cost_of_equity": {"unlevered_market_beta": 1.18, "r_squared": 0.25,
                           "debt_equity_ratio": 0.1433, "tax_rate": 0.40,
                           "riskfree_rate": 0.0425, "equity_risk_premium": 0.04},
        "illiquidity": {"revenues_millions": 1.2, "positive_earnings": True,
                        "block_fraction": 1.0, "base_discount": 0.25,
                        "cash_to_firm_value": 0.05, "trading_volume_to_firm_value": 0.0},
        "equity_value": 520990.0,
    },
    "cyclical": {
        "normalization": {
            "approach": 3,
            "revenue_history": [2032.0, 2376.0, 2779.0, 3155.0, 3248.0],
            "ebit_history": [186.0, 454.0, 529.0, 448.0, 383.0],
            "current_revenues": 12154.0,
            "book_value_of_debt": 0.0, "book_value_of_equity": 11722.0,
            "average_pretax_return_on_capital": 0.22, "average_ebit": 3500.0,
        },
        "commodity": {"intercept": 39992.77, "slope": 4039.40, "price": 40.0,
                      "price_ladder": [30.0, 40.0, 50.0, 60.0, 80.0]},
        "base_operating_margin": 0.0301, "target_operating_margin": 0.0935,
        "margin_convergence_year": 5,
    },
    "young-company": {
        "base_revenue": 1117.0, "base_ebit": -410.0, "base_invested_capital": 487.0,
        "forecast_years": 10, "riskfree_rate": 0.065,
        "revenue_path": {"mode": "explicit",
                         "high_growth_rates": [1.50, 1.00, 0.75, 0.50, 0.30]},
        "margin": {"style": "halving", "base_margin": -0.3671, "target_margin": 0.10,
                   "decay": 0.5},
        "sales_to_capital": 3.0,
        "tax_rate": 0.35,
        "net_operating_loss_carryforward": 500.0,
        "cost_of_capital": {"start": 0.1284, "end": 0.0961, "converge_by": 10},
        "terminal": {"growth_rate": 0.06, "cost_of_capital": 0.0961,
                     "return_on_capital": 0.20},
        "survival": {"probability_of_failure": 0.0},
        "bridge": {"debt": 349.0, "cash": 26.0, "employee_options_value": 2892.0,
                   "shares_outstanding": 340.79},
        "total_addressable_market": 400000.0,
    },
    "ipo": {
        "value_of_operating_assets": 9611.0,
        "cash": 375.0,
        "debt": 207.0,
        "proceeds": {"gross_proceeds": 1000.0, "use": "retained"},
        "claims": {"options_and_warrants_value": 805.0, "option_shares": 44.16},
        "pre_ipo_shares": 472.61,
        "shares": {"common_shares": 472.61, "restricted_stock_units": 86.0,
                   "shares_owed_under_acquisitions": 14.791,
                   "new_primary_shares": 0.0},
        "underpricing": {"percent": 0.15, "fraction_offered": 0.10,
                         "total_value": 20000.0},
    },
}


# ---------------------------------------------------------------------------- selftest

def cmd_selftest(args):
    """Worked examples from the source models, plus identities a wrong port would break."""
    results = []

    def check(name, actual, expected, tol=1e-6):
        ok = (isinstance(actual, (int, float)) and isinstance(expected, (int, float))
              and abs(actual - expected) <= tol * max(1.0, abs(expected)))
        results.append({"case": name, "expected": expected, "actual": actual, "pass": bool(ok)})

    def assert_true(name, condition, detail=None):
        results.append({"case": name, "expected": True, "actual": bool(condition),
                        "pass": bool(condition), "detail": detail})

    def refuses(name, fn):
        try:
            fn()
            ok = False
        except SystemExit:
            ok = True
        results.append({"case": name, "expected": True, "actual": ok, "pass": ok})

    # ---- branch 1: distress.xls stored case, 12% coupon, 8 years, rf 5%, price 653.
    bond = bond_implied_distress(0.12, 8, 0.05, 653.0)
    check("distress.xls annual probability", bond["annual_probability"],
          0.13531709403063646, 1e-9)
    check("distress.xls bond reprices to the market price", bond["model_price"], 653.0, 1e-9)
    check("distress.xls 5-year cumulative",
          cumulative_probability(bond["annual_probability"], 5), 0.5166247973245933, 1e-9)
    check("distress.xls 10-year cumulative",
          cumulative_probability(bond["annual_probability"], 10), 0.7663484134385095, 1e-9)

    # Las Vegas Sands, February 2009: 6.375% coupon, 7 years, rf 3%, price 529.
    lvs = bond_implied_distress(0.06375, 7, 0.03, 529.0)
    check("Las Vegas Sands annual probability", lvs["annual_probability"], 0.1354, 5e-4)
    check("Las Vegas Sands 10-year cumulative",
          cumulative_probability(lvs["annual_probability"], 10), 0.7666, 1e-3)

    # A bond priced above the riskfree-discounted promised payments has no root; the
    # engine must report zero rather than solving into nonsense.
    rich = bond_implied_distress(0.12, 8, 0.05, 5000.0)
    check("bond above its default-free value implies no distress",
          rich["annual_probability"], 0.0)

    # JC Penney: the blend at the operating-asset level.
    jcp = distress({"cumulative_probability": 0.20, "going_concern_value": 4841.0,
                    "distress": {"basis": "book", "book_equity": 4842.0,
                                 "book_debt": 0.0, "recovery_percent": 0.5}})
    check("JC Penney distress proceeds", jcp["distress_branch"]["proceeds"], 2421.0)
    check("JC Penney blended operating assets", jcp["blend"]["expected_value"], 4357.0)

    # Boeing, March 2020: the firm survives, equity does not. 20% failure with a 50% loss
    # to equity is a 10% haircut, not a 20% one.
    boeing = distress({"cumulative_probability": 0.20, "going_concern_value": 107883.0,
                       "equity_loss_fraction": 0.50})
    check("Boeing failure deduction", boeing["blend"]["deduction"], 10788.3)
    check("Boeing adjusted operating assets", boeing["blend"]["expected_value"], 97094.7)

    # Equity is a residual: proceeds below the face value of debt leave shareholders zero.
    wiped = _resolve_distress_value(
        {"distress": {"basis": "explicit", "proceeds": 2769.0, "debt_face_value": 11000.0}},
        None)
    check("equity is worth zero when proceeds fall short of debt", wiped["distress_value"], 0.0)

    refuses("distress with no probability source is refused",
            lambda: distress({"going_concern_value": 100.0}))

    # ---- branch 2: eqexret.xls stored case.
    bank = excess_return(EXAMPLES["excess-return"])
    check("eqexret year 1 net income", bank["forecast"][0]["net_income"], 4499.25, 1e-6)
    check("eqexret year 1 excess return", bank["forecast"][0]["excess_equity_return"],
          2771.54, 1e-5)
    check("eqexret year 10 cost of equity", bank["forecast"][9]["cost_of_equity"], 0.094, 1e-9)
    check("eqexret year 10 return on equity", bank["forecast"][9]["return_on_equity"],
          0.15, 1e-9)
    check("eqexret year 7 payout", bank["forecast"][6]["payout_ratio"], 0.382877, 1e-5)
    check("eqexret terminal book equity", bank["terminal"]["beginning_book_equity"],
          73370.15, 1e-6)
    check("eqexret terminal excess return", bank["terminal"]["excess_equity_return"],
          4108.73, 1e-5)
    check("eqexret terminal value of excess returns",
          bank["terminal"]["terminal_value_of_excess_returns"], 93380.20, 1e-6)
    check("eqexret present value of excess returns",
          bank["present_value_of_excess_returns"], 65993.76, 1e-6)
    check("eqexret value of equity", bank["value_of_equity"], 83990.76, 1e-6)
    check("eqexret value per share", bank["value_per_share"], 74.944, 1e-4)

    # The residual-income route and the discounted-FCFE route are the same model written
    # two ways. A gap between them means the book-equity rollforward is inconsistent with
    # the cash flows, which is the classic bank-model error.
    assert_true("excess-return and FCFE routes agree",
                abs(bank["route_difference"]) < 1e-6 * abs(bank["value_of_equity"]),
                bank["route_difference"])

    # If a bank earns exactly its cost of equity forever, it is worth its book equity and
    # not a cent more. A wrong discounting or rollforward breaks this immediately.
    flat = {"book_equity": 1000.0, "forecast_years": 10, "reinvestment": "retention",
            "cost_of_equity": 0.10, "return_on_equity": 0.10, "retention_ratio": 0.30,
            "fade_second_half": False,
            "stable": {"return_on_equity": 0.10, "growth_rate": 0.03,
                       "cost_of_equity": 0.10}}
    flat_out = excess_return(flat)
    check("no excess return means equity is worth book value",
          flat_out["value_of_equity"], 1000.0, 1e-9)

    # Regulatory-capital reinvestment: a rising ratio is not free, and the identity must
    # still hold when book equity is set by the regulator rather than by retention.
    reg = {"book_equity": 64609.0, "forecast_years": 10,
           "reinvestment": "regulatory_capital",
           "regulatory_capital": {"risk_adjusted_assets": 445570.0, "asset_growth": 0.01,
                                  "capital_ratio": {"start": 0.1241, "end": 0.1567,
                                                    "converge_by": 10}},
           "return_on_equity": {"start": -0.1370, "end": 0.0944, "converge_by": 10},
           "cost_of_equity": 0.1020, "retention_ratio": 1.0,
           "stable": {"return_on_equity": 0.0944, "growth_rate": 0.01,
                      "cost_of_equity": 0.0944}}
    reg_out = excess_return(reg)
    assert_true("regulatory routes agree",
                abs(reg_out["route_difference"]) < 1e-6 * abs(reg_out["value_of_equity"]),
                reg_out["route_difference"])
    assert_true("rebuilding capital makes early FCFE negative",
                reg_out["forecast"][0]["fcfe"] < 0, reg_out["forecast"][0]["fcfe"])
    check("required capital is assets times the ratio",
          reg_out["forecast"][9]["ending_book_equity"],
          445570.0 * 1.01 ** 10 * 0.1567, 1e-9)

    # A disclosed book equity path must be used verbatim rather than backed out of a ratio,
    # and the one-off capital hit must come out before the forecast starts.
    disclosed = excess_return({
        "book_equity": 1000.0, "one_off_capital_hit": 100.0, "forecast_years": 4,
        "reinvestment": "regulatory_capital",
        "regulatory_capital": {"required_book_equity": [950.0, 1000.0, 1050.0, 1100.0]},
        "return_on_equity": 0.08, "cost_of_equity": 0.09, "fade_second_half": False,
        "stable": {"return_on_equity": 0.08, "growth_rate": 0.02, "cost_of_equity": 0.09}})
    check("one-off capital hit reduces opening book equity",
          disclosed["opening_book_equity"], 900.0, 1e-12)
    check("disclosed capital path is used verbatim",
          disclosed["forecast"][0]["ending_book_equity"], 950.0, 1e-12)
    check("investment is the change in required capital",
          disclosed["forecast"][0]["investment_in_book_equity"], 50.0, 1e-12)
    assert_true("disclosed-path routes agree",
                abs(disclosed["route_difference"]) < 1e-6 * abs(disclosed["value_of_equity"]),
                disclosed["route_difference"])

    refuses("stable cost of equity below stable growth is refused",
            lambda: excess_return({"book_equity": 100.0, "forecast_years": 5,
                                   "cost_of_equity": 0.08, "return_on_equity": 0.10,
                                   "retention_ratio": 0.4,
                                   "stable": {"return_on_equity": 0.10,
                                              "growth_rate": 0.09,
                                              "cost_of_equity": 0.08}}))

    # ---- branch 3: the restaurant and the pvtdiscrate.xls default case.
    rest = private_cost_of_equity(EXAMPLES["private"]["cost_of_equity"])
    check("restaurant correlation from R-squared", rest["correlation"], 0.50, 1e-12)
    check("restaurant total unlevered beta", rest["total_unlevered_beta"], 2.36, 1e-9)
    check("restaurant levered total beta", rest["levered_total_beta"], 2.56, 2e-3)
    check("restaurant cost of equity, undiversified buyer",
          rest["cost_of_equity_undiversified_buyer"], 0.1450, 1e-3)
    check("restaurant cost of equity, diversified buyer",
          rest["cost_of_equity_diversified_buyer"], 0.0938, 1e-3)

    pvt = private_cost_of_equity({"unlevered_market_beta": 1.02, "correlation": 0.45,
                                  "debt_to_capital": 0.15, "tax_rate": 0.40,
                                  "riskfree_rate": 0.06, "equity_risk_premium": 0.055})
    check("pvtdiscrate levered total beta", pvt["levered_total_beta"], 2.506666666666667, 1e-9)
    check("pvtdiscrate cost of equity", pvt["cost_of_equity_undiversified_buyer"],
          0.19786666666666666, 1e-9)

    # Dividing by R-squared instead of by the correlation is the classic total-beta error;
    # this identity catches it.
    check("total beta divides by the correlation, not R-squared",
          total_beta(0.8, r_squared=0.16)["total_beta"], 2.0, 1e-12)
    refuses("a correlation of zero is refused",
            lambda: total_beta(1.0, correlation=0.0))

    check("restaurant Silber discount",
          silber_discount(1.2, True)["discount"], 0.28757, 1e-4)
    check("liqdisc.xls Silber discount",
          silber_discount(209.0, True)["discount"], 0.19095516638888976, 1e-9)
    check("restaurant bid-ask discount",
          bid_ask_discount(1.2, True, 0.05, 0.0)["discount"], 0.12880, 1e-4)
    check("liqdisc.xls bid-ask discount",
          bid_ask_discount(209.0, True, 0.03, 0.0)["discount"], 0.1177668646456774, 1e-9)

    # Every row of the bundled pre-computed table must fall out of the formula.
    table = _load_reference(ILLIQUIDITY_REFERENCE)["silber_precomputed_discounts"]["rows"]
    worst = 0.0
    for revenue, profitable, unprofitable in table:
        worst = max(worst,
                    abs(silber_discount(revenue, True)["discount"] - profitable),
                    abs(silber_discount(revenue, False)["discount"] - unprofitable))
    assert_true("bundled Silber table reproduces from the formula", worst < 5e-5, worst)

    # A listed acquirer's own investors can sell, so no illiquidity discount applies.
    public_buyer = private({**EXAMPLES["private"], "buyer": "public"})
    assert_true("a public buyer gets no illiquidity discount",
                public_buyer["illiquidity"]["equity_value_after_discount"]["silber"]
                == 520990.0)

    # ---- branch 6: Twitter's pre-IPO bridge, October 2013 ($ millions).
    tw = ipo(EXAMPLES["ipo"])
    check("Twitter value of equity", tw["value_of_equity"], 10779.0, 1e-9)
    check("Twitter value of equity in common stock",
          tw["value_of_equity_in_common_stock"], 9974.0, 1e-9)
    check("Twitter share count with RSUs and acquisition shares",
          tw["share_count"]["post_offering_shares"], 573.401, 1e-9)

    # The packet's own count is 574.44 million, about a million above the three classes it
    # enumerates, and $17.36 is the number it prints. Pin that number too, so a change in
    # the bridge cannot drift away from the published answer.
    packet = ipo({**EXAMPLES["ipo"], "shares": {"common_shares": 574.44}})
    check("Twitter value per share on the packet's share count",
          packet["value_per_share"], 17.36, 1e-3)

    # Counting options in the denominator as well as subtracting their value is the standard
    # IPO error. The 44.16 million option shares must stay out of the count.
    assert_true("option shares stay out of the share count",
                abs(tw["share_count"]["post_offering_shares"]
                    - (472.61 + 86.0 + 14.791)) < 1e-9
                and tw["share_count"]["excluded_option_shares"] == 44.16)

    # Proceeds the owners take out never reach the business, so they are worth exactly
    # nothing per share. The gap between the two runs must be the whole raise divided by the
    # share count — no more, no less.
    cashed_out = ipo({**EXAMPLES["ipo"],
                      "proceeds": {"gross_proceeds": 1000.0, "use": "to_owners"}})
    check("proceeds taken out by the owners cost exactly the raise per share",
          tw["value_per_share"] - cashed_out["value_per_share"],
          1000.0 / tw["share_count"]["post_offering_shares"], 1e-9)

    check("cost of underpricing falls only on the stake sold",
          tw["underpricing"]["cost_of_underpricing"], 300.0, 1e-9)
    first_day = ipo({**EXAMPLES["ipo"],
                     "underpricing": {"percent": 0.15, "fraction_offered": 0.10,
                                      "total_value": 20000.0, "offer_price": 20.0,
                                      "first_day_close": 23.0}})
    check("first-day return", first_day["underpricing"]["first_day_return"], 0.15, 1e-12)

    # ---- branch 6: the restaurant, sold private versus taken public.
    restaurant = {
        "cost_of_equity": {**EXAMPLES["private"]["cost_of_equity"],
                           "pre_tax_cost_of_debt": 0.075},
        "revaluation": {"next_year_fcff": 163.04, "stable_growth": 0.02,
                        "cost_of_capital_private": 0.1325,
                        "cost_of_capital_public": 0.0876},
        "debt": 928.23,
        "illiquidity_discount": 0.1288,
        "pre_ipo_shares": 1.0,
        "shares": {"common_shares": 1.0},
        "offering_discount": 0.15,
    }
    rest_ipo = ipo(restaurant)
    check("restaurant cost of capital to a private owner",
          rest_ipo["cost_of_equity"]["cost_of_capital_private"], 0.1325, 1e-4)
    check("restaurant cost of capital to public investors",
          rest_ipo["cost_of_equity"]["cost_of_capital_public"], 0.0876, 1e-4)
    check("restaurant equity to its owner, after the illiquidity discount",
          rest_ipo["bridge"][0]["equity_value_after"], 453.88, 1e-3)
    check("restaurant equity once the illiquidity discount comes off",
          rest_ipo["bridge"][1]["equity_value_after"], 520.99, 1e-3)
    check("restaurant equity at the market beta",
          rest_ipo["bridge"][2]["equity_value_after"], 1483.56, 1e-3)
    check("offer price is the value less the offering discount",
          rest_ipo["offer_price"], rest_ipo["value_per_share"] * 0.85, 1e-12)

    # ---- branch 6: the preferred waterfall. Same cap table, two offering values.
    preferred_case = {"cash": 0.0, "debt": 0.0, "shares": {"common_shares": 100.0},
                      "convertible_preferred": [
                          {"name": "Series A", "as_converted_shares": 50.0,
                           "liquidation_preference": 100.0, "converts": "auto"}]}
    rich_round = ipo({**preferred_case, "value_of_operating_assets": 1000.0})
    check("preferred converts when the as-converted stake beats the preference",
          rich_round["value_per_share"], 1000.0 / 150.0, 1e-12)
    assert_true("the converting round joins the share count",
                rich_round["share_count"]["post_offering_shares"] == 150.0)

    poor_round = ipo({**preferred_case, "value_of_operating_assets": 120.0})
    assert_true("preferred takes the cash when converting is worth less",
                poor_round["convertible_preferred"]["rounds"][0]["converts"] is False)
    check("common gets what is left after the preference",
          poor_round["value_per_share"], 0.20, 1e-12)
    assert_true("a round taking its preference stays out of the share count",
                poor_round["share_count"]["post_offering_shares"] == 100.0)

    wiped_out = ipo({**preferred_case, "value_of_operating_assets": 120.0,
                     "convertible_preferred": [
                         {"name": "Series A", "as_converted_shares": 50.0,
                          "liquidation_preference": 200.0, "converts": "auto"}]})
    check("a preference stack above the offering value leaves common nothing",
          wiped_out["value_per_share"], 0.0, 1e-12)

    refuses("proceeds buckets that do not sum to the raise are refused",
            lambda: ipo({**EXAMPLES["ipo"],
                         "proceeds": {"gross_proceeds": 1000.0, "retained": 400.0,
                                      "to_owners": 100.0}}))
    refuses("a cost of capital below stable growth is refused",
            lambda: ipo({**restaurant,
                         "revaluation": {**restaurant["revaluation"],
                                         "cost_of_capital_public": 0.01}}))
    refuses("an IPO with no operating asset value is refused",
            lambda: ipo({"cash": 10.0, "shares": {"common_shares": 1.0}}))

    # ---- branch 4: normearn.xls and the Shell oil-price regression.
    norm = normalized_ebit(EXAMPLES["cyclical"]["normalization"])
    check("normearn aggregate margin", norm["history"]["aggregate_margin"],
          0.14716703458425312, 1e-12)
    check("normearn approach 3 normalized EBIT", norm["normalized_ebit"],
          1788.6681383370124, 1e-9)
    check("normearn approach 2 normalized EBIT", norm["approaches"]["2_return_on_capital"],
          2578.84, 1e-9)
    check("normearn approach 1 normalized EBIT", norm["approaches"]["1_average_ebit"],
          3500.0, 1e-12)
    # The aggregate margin is not the average of the yearly margins; using the average
    # would change the answer, so the two must not be interchangeable.
    assert_true("aggregate margin differs from the average of yearly margins",
                abs(norm["history"]["aggregate_margin"]
                    - norm["history"]["average_of_yearly_margins"]) > 1e-4)

    shell = commodity_revenues(EXAMPLES["cyclical"]["commodity"])
    check("Shell revenues at $40 oil", shell["revenue"], 201568.77, 1e-9)
    check("Shell base operating margin at $40 oil", 6065.0 / shell["revenue"], 0.0301, 1e-3)

    # The regression must recover coefficients it was generated from.
    prices = [20.0, 30.0, 45.0, 60.0, 80.0, 100.0]
    fitted = _ols(prices, [39992.77 + 4039.40 * x for x in prices])
    check("regression recovers the slope", fitted["slope"], 4039.40, 1e-9)
    check("regression recovers the intercept", fitted["intercept"], 39992.77, 1e-9)
    check("an exact fit has R-squared of one", fitted["r_squared"], 1.0, 1e-12)

    # ---- branch 5: the Amazon January 2000 path.
    amzn = young_company(EXAMPLES["young-company"])
    path = amzn["revenue_path"]
    check("Amazon year 1 revenue", path[0]["revenue"], 2793.0, 3e-4)
    check("Amazon year 5 revenue", path[4]["revenue"], 19059.0, 3e-4)
    check("Amazon year 10 revenue", path[9]["revenue"], 39006.0, 3e-4)
    check("Amazon year 6 growth fades to 25.2%", path[5]["revenue_growth"], 0.252, 1e-9)
    check("Amazon year 10 growth reaches stable", path[9]["revenue_growth"], 0.06, 1e-12)
    check("Amazon year 1 margin", path[0]["operating_margin"], -0.1335, 1e-3)
    check("Amazon year 3 margin", path[2]["operating_margin"], 0.0416, 1e-3)
    check("Amazon year 10 margin", path[9]["operating_margin"], 0.0995, 1e-3)
    check("Amazon year 1 reinvestment", path[0]["reinvestment"], 559.0, 2e-3)
    check("Amazon year 4 reinvestment", path[3]["reinvestment"], 1629.0, 2e-3)

    # The revenue-target mode must invert the growth path it builds.
    target = young_company({
        **EXAMPLES["young-company"],
        "revenue_path": {"mode": "target_revenue", "target_revenue": 39006.0,
                         "target_year": 10, "hold_through": 5},
    })
    check("solved growth path hits the revenue target",
          target["revenue_path"][9]["revenue"], 39006.0, 1e-9)

    # The payload must carry every field dcf.py requires.
    payload = amzn["dcf_payload"]
    required = ["base_revenue", "forecast_years", "revenue_growth", "operating_margin",
                "sales_to_capital", "tax_rate", "cost_of_capital", "terminal"]
    missing = [k for k in required if k not in payload]
    assert_true("dcf payload carries every required driver", not missing, missing)
    assert_true("driver lists are one entry per forecast year",
                len(payload["revenue_growth"]) == payload["forecast_years"]
                and len(payload["operating_margin"]) == payload["forecast_years"])

    # Terminal growth above the riskfree rate is a real error, not an inconvenience.
    refuses("terminal growth above the riskfree rate is refused",
            lambda: young_company({**EXAMPLES["young-company"], "riskfree_rate": 0.03}))
    refuses("a young company with no survival input is refused",
            lambda: young_company({**EXAMPLES["young-company"], "survival": {}}))

    # A sector survival rate must reach the payload as a failure probability.
    risky = young_company({**EXAMPLES["young-company"],
                           "survival": {"sector": "Information"}})
    check("Information sector failure probability",
          risky["dcf_payload"]["failure"]["probability"], 1.0 - 0.115, 1e-12)

    # ---- integration: the payload must actually run through the DCF engine.
    engine = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "..", "dcf-valuation-engine", "resources", "dcf.py")
    if os.path.exists(engine):
        import importlib.util
        spec_ = importlib.util.spec_from_file_location("dcf_engine", engine)
        module = importlib.util.module_from_spec(spec_)
        spec_.loader.exec_module(module)
        valued = module.value(payload)
        assert_true("dcf engine values the emitted payload",
                    valued["value_per_share"] is not None, valued["value_per_share"])
        check("dcf engine sees the same year 1 revenue",
              valued["forecast"][0]["revenue"], path[0]["revenue"], 1e-12)
    else:
        results.append({"case": "dcf engine values the emitted payload", "expected": True,
                        "actual": "skipped", "pass": True,
                        "detail": "dcf-valuation-engine not found alongside this skill."})

    failed = [r for r in results if not r["pass"]]
    _emit({"total": len(results), "passed": len(results) - len(failed),
           "failed": len(failed), "results": results})
    return 1 if failed else 0


# ------------------------------------------------------------------------------- main

COMMANDS = {
    "distress": cmd_distress,
    "excess-return": cmd_excess_return,
    "private": cmd_private,
    "ipo": cmd_ipo,
    "cyclical": cmd_cyclical,
    "young-company": cmd_young_company,
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
    except (TypeError, ValueError, KeyError, IndexError, ZeroDivisionError) as exc:
        # A payload with the right keys but the wrong types lands here. Name the field
        # shape the caller should check rather than printing an interpreter traceback.
        raise SystemExit(
            "%s could not run on this payload: %s. Check that every rate is a decimal "
            "number, every list has one entry per forecast year, and nested blocks such "
            "as `terminal` and `stable` are objects. Run with --example to compare."
            % (args.command, exc))


if __name__ == "__main__":
    sys.exit(main())

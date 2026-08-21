#!/usr/bin/env python3
"""
options.py — option pricing for valuation work.

Four jobs come up repeatedly. Employee options must be valued and subtracted before
dividing equity value by shares. Equity in a deeply indebted firm behaves like a call
option on the firm's assets, which is why a company can be worth something when a DCF
says it is worth nothing. Real options — a patent, an undeveloped reserve, the right to
expand — carry value a static DCF misses. And sometimes a binomial tree is the honest
model because exercise happens early.

Pure standard library: the normal distribution comes from `math.erf`, so there are no
third-party packages, ever — this must run anywhere.

SUBCOMMANDS
  black-scholes     European call/put, with a continuous dividend or cost-of-delay yield
  employee-options  dilution-adjusted employee option value (solved iteratively)
  equity-as-option  equity of a levered firm valued as a call on firm value
  binomial          binomial tree, supporting early exercise
  implied-vol       back out volatility from an observed option price
  selftest          run the bundled worked examples and report pass/fail

Each subcommand reads a JSON payload (--in FILE, or stdin) and writes JSON to stdout.
Run any subcommand with --example to print a sample input payload.
"""

import argparse
import json
import math
import sys

# The dilution fixed point and the implied-volatility search both converge quickly;
# these ceilings simply guarantee termination on pathological inputs.
MAX_ITERATIONS = 200
TOLERANCE = 1e-10


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


def norm_cdf(x):
    """Standard normal CDF, built on the error function in the standard library."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


# ------------------------------------------------------------------------ Black-Scholes

def black_scholes(spot, strike, time_to_expiry, volatility, riskfree_rate,
                  dividend_yield=0.0, option_type="call"):
    """European option value.

    `dividend_yield` is the continuous leakage of value out of the underlying while the
    option is alive — a dividend on a stock, or the cash flow given up by not yet
    exercising a real option.
    """
    s, k, t, sigma, r, q = (float(spot), float(strike), float(time_to_expiry),
                            float(volatility), float(riskfree_rate), float(dividend_yield))
    if s <= 0 or k <= 0:
        raise SystemExit("spot and strike must be positive.")
    if t <= 0 or sigma <= 0:
        # With no time or no volatility left there is no optionality, only intrinsic value.
        intrinsic = max(0.0, s - k) if option_type == "call" else max(0.0, k - s)
        return {"value": intrinsic, "d1": None, "d2": None, "n_d1": None, "n_d2": None,
                "note": "No time value: expiry has arrived or volatility is zero."}

    d1 = (math.log(s / k) + (r - q + 0.5 * sigma ** 2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    if option_type == "call":
        value = s * math.exp(-q * t) * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d2)
    elif option_type == "put":
        value = k * math.exp(-r * t) * norm_cdf(-d2) - s * math.exp(-q * t) * norm_cdf(-d1)
    else:
        raise SystemExit("option_type must be 'call' or 'put'.")
    return {"value": value, "d1": d1, "d2": d2,
            "n_d1": norm_cdf(d1), "n_d2": norm_cdf(d2),
            "intrinsic_value": max(0.0, s - k) if option_type == "call" else max(0.0, k - s),
            "time_value": value - (max(0.0, s - k) if option_type == "call" else max(0.0, k - s))}


def cmd_black_scholes(args):
    p = _read_payload(args)
    _emit(black_scholes(p["spot"], p["strike"], p["time_to_expiry"], p["volatility"],
                        p["riskfree_rate"], p.get("dividend_yield", 0.0),
                        p.get("option_type", "call")))


# --------------------------------------------------------------------- employee options

def employee_options(p):
    """Value outstanding employee options, adjusting for the dilution they cause.

    Exercise creates new shares, which lowers the value of every share, which lowers the
    option's own payoff. The adjusted underlying blends existing share value with the
    option value being solved for, so the calculation is circular and is settled by
    iteration rather than algebra.

    Subtract the result from equity value before dividing by the ordinary share count.
    Counting options this way is more accurate than either inflating the share count or
    using the treasury-stock shortcut.
    """
    equity_value = float(p["equity_value"])
    shares = float(p["shares_outstanding"])
    n_options = float(p["options_outstanding"])
    strike = float(p["average_strike_price"])
    t = float(p["average_time_to_expiry"])
    sigma = float(p["volatility"])
    r = float(p["riskfree_rate"])
    q = float(p.get("dividend_yield", 0.0))

    if shares <= 0:
        raise SystemExit("shares_outstanding must be positive.")
    if n_options <= 0:
        return {"total_option_value": 0.0, "value_per_option": 0.0,
                "adjusted_value_per_share": equity_value / shares, "iterations": 0,
                "note": "No options outstanding."}

    total_option_value = 0.0
    per_option = 0.0
    iterations = 0
    for i in range(MAX_ITERATIONS):
        iterations = i + 1
        # Spread equity value plus the options' own value across all potential shares.
        adjusted_spot = (equity_value + total_option_value) / (shares + n_options)
        res = black_scholes(adjusted_spot, strike, t, sigma, r, q, "call")
        per_option = res["value"]
        new_total = per_option * n_options
        if abs(new_total - total_option_value) < TOLERANCE * max(1.0, abs(new_total)):
            total_option_value = new_total
            break
        total_option_value = new_total

    equity_in_common = equity_value - total_option_value
    return {
        "total_option_value": total_option_value,
        "value_per_option": per_option,
        "equity_value": equity_value,
        "equity_in_common_stock": equity_in_common,
        "shares_outstanding": shares,
        "value_per_share": equity_in_common / shares,
        "dilution_adjusted_spot": (equity_value + total_option_value) / (shares + n_options),
        "iterations": iterations,
        "converged": iterations < MAX_ITERATIONS,
    }


def cmd_employee_options(args):
    _emit(employee_options(_read_payload(args)))


# --------------------------------------------------------------------- equity as option

def equity_as_option(p):
    """Value the equity of a levered firm as a call option on its assets.

    Shareholders own the residual: if firm value ends above what is owed they keep the
    difference, and if it ends below, limited liability caps their loss at zero. So equity
    is a call struck at the face value of debt, expiring at the debt's maturity. This is
    the model that explains why the stock of a distressed company still trades above zero.
    """
    firm_value = float(p["firm_value"])
    face_value_debt = float(p["face_value_of_debt"])
    t = float(p["debt_maturity"])
    sigma = float(p["firm_value_volatility"])
    r = float(p["riskfree_rate"])
    # Cash paid out to any claimholder is value leaking away before the option matures.
    payout = float(p.get("payout_ratio", 0.0))

    res = black_scholes(firm_value, face_value_debt, t, sigma, r, payout, "call")
    equity = res["value"]
    debt_value = firm_value - equity
    out = {
        "firm_value": firm_value, "face_value_of_debt": face_value_debt,
        "equity_value": equity, "implied_debt_value": debt_value,
        "d1": res["d1"], "d2": res["d2"],
        # N(d2) is the risk-neutral probability the option finishes in the money, so its
        # complement is the probability the firm cannot repay.
        "probability_of_default": (1 - res["n_d2"]) if res["n_d2"] is not None else None,
        "note": ("Equity keeps value even when firm value is below the debt owed, because "
                 "limited liability caps the downside and time leaves room for recovery."),
    }
    if p.get("shares_outstanding"):
        out["value_per_share"] = equity / float(p["shares_outstanding"])
    if debt_value > 0 and t > 0:
        # The yield lenders are implicitly demanding, given what the debt is worth.
        out["implied_interest_rate_on_debt"] = (face_value_debt / debt_value) ** (1 / t) - 1
    return out


def cmd_equity_as_option(args):
    _emit(equity_as_option(_read_payload(args)))


# ------------------------------------------------------------------------------ binomial

def binomial(p):
    """Binomial tree valuation, with optional early exercise.

    Use this rather than Black-Scholes when exercise before expiry is genuinely on the
    table — an American put, or a real option that would be taken as soon as it pays.
    """
    s = float(p["spot"])
    k = float(p["strike"])
    t = float(p["time_to_expiry"])
    sigma = float(p["volatility"])
    r = float(p["riskfree_rate"])
    q = float(p.get("dividend_yield", 0.0))
    steps = int(p.get("steps", 100))
    option_type = p.get("option_type", "call")
    american = bool(p.get("american", False))

    if steps < 1:
        raise SystemExit("steps must be at least 1.")
    dt = t / steps
    # Cox-Ross-Rubinstein: up and down moves sized so the tree's variance matches sigma.
    u = math.exp(sigma * math.sqrt(dt))
    d = 1.0 / u
    disc = math.exp(-r * dt)
    prob_up = (math.exp((r - q) * dt) - d) / (u - d)
    if not 0 <= prob_up <= 1:
        raise SystemExit(
            "The tree is inconsistent (risk-neutral probability %.4f is outside [0,1]). "
            "Volatility is too low for the given rates, or the step count is too small."
            % prob_up)

    def payoff(price):
        return max(0.0, price - k) if option_type == "call" else max(0.0, k - price)

    # Terminal payoffs, then fold back.
    values = [payoff(s * (u ** (steps - i)) * (d ** i)) for i in range(steps + 1)]
    for step in range(steps - 1, -1, -1):
        for i in range(step + 1):
            hold = disc * (prob_up * values[i] + (1 - prob_up) * values[i + 1])
            if american:
                price = s * (u ** (step - i)) * (d ** i)
                hold = max(hold, payoff(price))
            values[i] = hold
    return {"value": values[0], "steps": steps, "up_factor": u, "down_factor": d,
            "risk_neutral_probability_up": prob_up, "american": american}


def cmd_binomial(args):
    _emit(binomial(_read_payload(args)))


# --------------------------------------------------------------------------- implied vol

def implied_volatility(p):
    """Back out the volatility consistent with an observed option price.

    Option value rises monotonically with volatility, so bisection is reliable here.
    """
    target = float(p["option_price"])
    lo, hi = 1e-6, 5.0

    def price_at(sig):
        return black_scholes(p["spot"], p["strike"], p["time_to_expiry"], sig,
                             p["riskfree_rate"], p.get("dividend_yield", 0.0),
                             p.get("option_type", "call"))["value"]

    if target < price_at(lo) or target > price_at(hi):
        raise SystemExit(
            "An option price of %.4f is not reachable for volatilities between %g and %g "
            "(prices span %.4f to %.4f). Check the inputs."
            % (target, lo, hi, price_at(lo), price_at(hi)))
    for _ in range(MAX_ITERATIONS):
        mid = (lo + hi) / 2
        if price_at(mid) < target:
            lo = mid
        else:
            hi = mid
        if hi - lo < TOLERANCE:
            break
    sigma = (lo + hi) / 2
    return {"implied_volatility": sigma, "option_price": target,
            "recomputed_price": price_at(sigma)}


def cmd_implied_vol(args):
    _emit(implied_volatility(_read_payload(args)))


# ---------------------------------------------------------------------------- selftest

EXAMPLES = {
    "black-scholes": {"spot": 100.0, "strike": 100.0, "time_to_expiry": 1.0,
                      "volatility": 0.3, "riskfree_rate": 0.05, "dividend_yield": 0.0,
                      "option_type": "call"},
    "employee-options": {"equity_value": 10000.0, "shares_outstanding": 1000.0,
                         "options_outstanding": 100.0, "average_strike_price": 8.0,
                         "average_time_to_expiry": 4.0, "volatility": 0.4,
                         "riskfree_rate": 0.03},
    "equity-as-option": {"firm_value": 800.0, "face_value_of_debt": 1000.0,
                         "debt_maturity": 5.0, "firm_value_volatility": 0.4,
                         "riskfree_rate": 0.05},
    "binomial": {"spot": 100.0, "strike": 100.0, "time_to_expiry": 1.0, "volatility": 0.3,
                 "riskfree_rate": 0.05, "steps": 200, "option_type": "put",
                 "american": True},
    "implied-vol": {"spot": 100.0, "strike": 100.0, "time_to_expiry": 1.0,
                    "riskfree_rate": 0.05, "option_price": 14.23, "option_type": "call"},
}


def cmd_selftest(args):
    results = []

    def check(name, actual, expected, tol=1e-6):
        ok = (expected is True and actual is True) or (
            isinstance(actual, (int, float)) and isinstance(expected, (int, float))
            and abs(actual - expected) <= tol * max(1.0, abs(expected)))
        results.append({"case": name, "expected": expected, "actual": actual, "pass": bool(ok)})

    # Normal CDF anchors.
    check("normal CDF at 0", norm_cdf(0.0), 0.5)
    check("normal CDF at 1.96", norm_cdf(1.96), 0.975, 1e-3)
    check("normal CDF symmetry", norm_cdf(-1.0) + norm_cdf(1.0), 1.0)

    # Black-Scholes against a standard textbook case: S=K=100, T=1, sigma=30%, r=5%.
    bs = black_scholes(100, 100, 1.0, 0.3, 0.05)
    check("at-the-money call", bs["value"], 14.231254, 1e-4)

    # Put-call parity must hold: C - P = S*e^(-qT) - K*e^(-rT).
    call = black_scholes(100, 95, 1.0, 0.25, 0.04, 0.02, "call")["value"]
    put = black_scholes(100, 95, 1.0, 0.25, 0.04, 0.02, "put")["value"]
    parity = 100 * math.exp(-0.02) - 95 * math.exp(-0.04)
    check("put-call parity", call - put, parity, 1e-9)

    # A deep in-the-money call approaches its discounted intrinsic value.
    deep = black_scholes(1000, 1.0, 1.0, 0.3, 0.05)["value"]
    check("deep in-the-money call", deep, 1000 - math.exp(-0.05), 1e-4)

    # No volatility means no time value.
    check("zero volatility leaves intrinsic value only",
          black_scholes(120, 100, 1.0, 0.0, 0.05)["value"], 20.0)

    # A binomial tree with many steps must converge to Black-Scholes for a European option.
    eur = binomial({"spot": 100, "strike": 100, "time_to_expiry": 1.0, "volatility": 0.3,
                    "riskfree_rate": 0.05, "steps": 500, "option_type": "call",
                    "american": False})
    check("binomial converges to Black-Scholes", eur["value"], bs["value"], 2e-3)

    # An American put must be worth at least its European twin.
    am = binomial({"spot": 100, "strike": 110, "time_to_expiry": 1.0, "volatility": 0.3,
                   "riskfree_rate": 0.05, "steps": 300, "option_type": "put",
                   "american": True})["value"]
    eu = binomial({"spot": 100, "strike": 110, "time_to_expiry": 1.0, "volatility": 0.3,
                   "riskfree_rate": 0.05, "steps": 300, "option_type": "put",
                   "american": False})["value"]
    results.append({"case": "American put is worth at least the European put",
                    "expected": True, "actual": am >= eu - 1e-12, "pass": am >= eu - 1e-12})

    # Equity as a call: an insolvent firm still has positive equity value.
    eq = equity_as_option(EXAMPLES["equity-as-option"])
    results.append({"case": "insolvent firm still has positive equity value",
                    "expected": True, "actual": eq["equity_value"] > 0,
                    "pass": eq["equity_value"] > 0})
    results.append({"case": "equity plus debt equals firm value", "expected": True,
                    "actual": True,
                    "pass": abs(eq["equity_value"] + eq["implied_debt_value"] - 800.0) < 1e-9})
    results.append({"case": "default probability is a probability", "expected": True,
                    "actual": eq["probability_of_default"],
                    "pass": 0.0 <= eq["probability_of_default"] <= 1.0})

    # More volatility helps shareholders of a distressed firm at lenders' expense —
    # the risk-shifting result.
    risky = equity_as_option(dict(EXAMPLES["equity-as-option"], firm_value_volatility=0.8))
    results.append({"case": "higher volatility raises distressed equity value",
                    "expected": True,
                    "actual": risky["equity_value"] > eq["equity_value"],
                    "pass": risky["equity_value"] > eq["equity_value"]})

    # Employee options: the dilution loop must converge and cost shareholders value.
    eo = employee_options(EXAMPLES["employee-options"])
    results.append({"case": "employee option loop converges", "expected": True,
                    "actual": eo["converged"], "pass": eo["converged"]})
    results.append({"case": "options reduce value per share", "expected": True,
                    "actual": True, "pass": eo["value_per_share"] < 10000.0 / 1000.0})
    check("equity in common stock nets out option value",
          eo["equity_in_common_stock"], 10000.0 - eo["total_option_value"])
    # With no options the answer is just equity over shares.
    none = employee_options(dict(EXAMPLES["employee-options"], options_outstanding=0))
    check("no options leaves value per share untouched",
          none["adjusted_value_per_share"], 10.0)

    # Implied volatility must invert the pricer.
    iv = implied_volatility({"spot": 100.0, "strike": 100.0, "time_to_expiry": 1.0,
                             "riskfree_rate": 0.05, "option_price": bs["value"]})
    check("implied volatility recovers the input", iv["implied_volatility"], 0.3, 1e-5)

    failed = [x for x in results if not x["pass"]]
    _emit({"total": len(results), "passed": len(results) - len(failed),
           "failed": len(failed), "results": results})
    return 1 if failed else 0


COMMANDS = {
    "black-scholes": cmd_black_scholes, "employee-options": cmd_employee_options,
    "equity-as-option": cmd_equity_as_option, "binomial": cmd_binomial,
    "implied-vol": cmd_implied_vol, "selftest": cmd_selftest,
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

#!/usr/bin/env python3
"""
validate.py — the consistency gate for a valuation.

Most bad valuations are not wrong in any single number. They are internally inconsistent:
cash flows in one currency discounted at a rate built in another, growth that nobody pays
for, a terminal growth rate above the economy's, or a method the company's own type rules
out. Each piece looks defensible alone, so only a cross-artifact check catches it.

This script is that check. It reads the artifacts a valuation produces and reports
violations. Run it before accepting a valuation, fix what it flags, and run it again.

Exit code 0 when nothing is at ERROR severity, 1 otherwise, so it can gate a pipeline.

Pure standard library. No third-party packages, ever — this must run anywhere.

USAGE
  validate.py --classification C.json --capital K.json --forecast F.json \
              --dcf D.json [--mandate M.json] [--relative R.json] [--json]

Any subset of files may be given; checks whose inputs are absent are skipped and
reported as such, so this is useful part-way through an analysis too.
"""

import argparse
import json
import sys

ERROR, WARN, INFO = "ERROR", "WARN", "INFO"

# A terminal value much above this share of total value means the answer rests almost
# entirely on assumptions past the forecast horizon rather than on anything forecast.
TERMINAL_VALUE_SHARE_WARN = 0.90
# Betas outside this band are possible but rare enough to be worth a second look.
BETA_LOW, BETA_HIGH = 0.3, 3.0
# Tolerance for arithmetic that should tie out exactly but passes through JSON rounding.
ARITHMETIC_TOLERANCE = 1e-6
# Growth implied by reinvestment rarely matches the forecast to the decimal; flag only
# gaps wide enough to signal that growth is not being paid for.
GROWTH_RECONCILIATION_TOLERANCE = 0.02


def load(path):
    if not path:
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        raise SystemExit("%s is not valid JSON: %s" % (path, e))


class Report:
    def __init__(self):
        self.findings = []
        self.skipped = []

    def add(self, severity, check, message, detail=None):
        self.findings.append({"severity": severity, "check": check,
                              "message": message, "detail": detail})

    def skip(self, check, why):
        self.skipped.append({"check": check, "reason": why})

    @property
    def errors(self):
        return [f for f in self.findings if f["severity"] == ERROR]


def _get(d, *path, default=None):
    """Fetch a nested key, tolerating missing intermediate levels."""
    node = d
    for key in path:
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    return node


# ------------------------------------------------------------------------------ checks

def check_currency(rep, mandate, capital, forecast, dcf):
    """Cash flows and the rate that discounts them must be in the same currency."""
    currencies = {}
    if mandate and mandate.get("currency"):
        currencies["mandate"] = mandate["currency"]
    if capital and capital.get("currency"):
        currencies["cost_of_capital"] = capital["currency"]
    if forecast and forecast.get("currency"):
        currencies["forecast"] = forecast["currency"]
    if dcf and dcf.get("currency"):
        currencies["dcf"] = dcf["currency"]

    if len(currencies) < 2:
        rep.skip("currency", "fewer than two artifacts declare a currency")
        return
    distinct = set(currencies.values())
    if len(distinct) > 1:
        rep.add(ERROR, "currency",
                "Artifacts disagree on currency, so cash flows are being discounted at a "
                "rate built for a different currency.", currencies)
    else:
        rep.add(INFO, "currency", "All artifacts agree on %s." % distinct.pop(), currencies)


def check_terminal_growth(rep, capital, dcf):
    """No company outgrows its economy forever, and the riskfree rate is that ceiling."""
    g = _get(dcf, "terminal", "growth_rate")
    if g is None:
        rep.skip("terminal_growth", "no terminal growth rate in the DCF result")
        return
    rf = _get(capital, "riskfree_rate")
    if rf is None:
        rf = _get(capital, "cost_of_equity", "riskfree_rate")
    if rf is None:
        rep.skip("terminal_growth", "no riskfree rate in the cost of capital artifact")
    elif g > rf + ARITHMETIC_TOLERANCE:
        rep.add(ERROR, "terminal_growth",
                "Terminal growth of %.2f%% exceeds the riskfree rate of %.2f%%. In a "
                "consistent valuation the riskfree rate is the ceiling on perpetual "
                "nominal growth, because it already embeds expected inflation and real "
                "growth for the economy." % (g * 100, rf * 100),
                {"terminal_growth": g, "riskfree_rate": rf})
    else:
        rep.add(INFO, "terminal_growth",
                "Terminal growth %.2f%% is within the riskfree ceiling %.2f%%."
                % (g * 100, rf * 100))

    wacc_t = _get(dcf, "terminal", "cost_of_capital")
    if wacc_t is not None and g is not None and wacc_t <= g:
        rep.add(ERROR, "terminal_discount_rate",
                "Terminal cost of capital (%.2f%%) is not above terminal growth (%.2f%%), "
                "so the terminal value is not a finite number."
                % (wacc_t * 100, g * 100))


def check_terminal_reinvestment(rep, dcf):
    """Growth has to be bought: the reinvestment rate must equal growth over return."""
    g = _get(dcf, "terminal", "growth_rate")
    roc = _get(dcf, "terminal", "return_on_capital")
    rate = _get(dcf, "terminal", "reinvestment_rate")
    if g is None or roc is None or rate is None:
        rep.skip("terminal_reinvestment", "terminal growth, return, or reinvestment missing")
        return
    if g <= 0:
        rep.add(INFO, "terminal_reinvestment",
                "Terminal growth is not positive, so no reinvestment is required.")
        return
    expected = g / roc
    if abs(rate - expected) > ARITHMETIC_TOLERANCE:
        rep.add(ERROR, "terminal_reinvestment",
                "Terminal reinvestment rate is %.4f but growth of %.2f%% at a %.2f%% "
                "return on capital requires %.4f. Growth is being received without being "
                "paid for." % (rate, g * 100, roc * 100, expected),
                {"stated": rate, "required": expected})
    elif rate > 1:
        rep.add(ERROR, "terminal_reinvestment",
                "Terminal reinvestment rate above 100%% means the firm must raise capital "
                "forever to stand still.")
    else:
        rep.add(INFO, "terminal_reinvestment",
                "Terminal reinvestment of %.1f%% of income is consistent with %.2f%% "
                "growth at a %.2f%% return." % (rate * 100, g * 100, roc * 100))


def check_excess_returns(rep, dcf):
    """A return above the cost of capital in perpetuity is a claim about competition."""
    roc = _get(dcf, "terminal", "return_on_capital")
    wacc = _get(dcf, "terminal", "cost_of_capital")
    if roc is None or wacc is None:
        rep.skip("terminal_excess_return", "terminal return or cost of capital missing")
        return
    spread = roc - wacc
    if spread > 0.02:
        rep.add(WARN, "terminal_excess_return",
                "The terminal period assumes a return on capital %.2f percentage points "
                "above the cost of capital, forever. That is a claim that competitors "
                "never arrive; it needs a named barrier to entry to be credible."
                % (spread * 100), {"terminal_roc": roc, "terminal_wacc": wacc})
    elif spread < -0.02:
        rep.add(WARN, "terminal_excess_return",
                "The terminal period destroys value (%.2f points below the cost of "
                "capital). If that is intended, growth should be zero or negative."
                % (-spread * 100))
    else:
        rep.add(INFO, "terminal_excess_return",
                "Terminal return sits near the cost of capital, the competitive default.")


def check_terminal_share(rep, dcf):
    share = _get(dcf, "terminal_value_share_of_total")
    if share is None:
        rep.skip("terminal_value_share", "terminal value share not reported")
        return
    if share > TERMINAL_VALUE_SHARE_WARN:
        rep.add(WARN, "terminal_value_share",
                "%.0f%% of the value sits in the terminal value, so the answer is driven "
                "almost entirely by assumptions beyond the forecast horizon. Consider a "
                "longer explicit forecast." % (share * 100), {"share": share})
    else:
        rep.add(INFO, "terminal_value_share",
                "Terminal value is %.0f%% of total value." % (share * 100))


def check_weights(rep, capital):
    w = _get(capital, "weights")
    if not isinstance(w, dict):
        rep.skip("capital_weights", "no weights block in the cost of capital artifact")
        return
    total = sum(v for v in w.values() if isinstance(v, (int, float)))
    if abs(total - 1.0) > 1e-4:
        rep.add(ERROR, "capital_weights",
                "Capital weights sum to %.4f rather than 1." % total, w)
    else:
        rep.add(INFO, "capital_weights", "Capital weights sum to 1.")


def check_beta(rep, capital):
    beta = _get(capital, "levered_beta") or _get(capital, "beta", "levered")
    if beta is None:
        rep.skip("beta_range", "no levered beta in the cost of capital artifact")
        return
    if beta <= 0:
        rep.add(ERROR, "beta_range",
                "A levered beta of %.2f is not usable; equity risk cannot be zero or "
                "negative for an operating company." % beta)
    elif not BETA_LOW <= beta <= BETA_HIGH:
        rep.add(WARN, "beta_range",
                "Levered beta of %.2f sits outside the usual %.1f-%.1f band. That can be "
                "right for a very safe or very leveraged firm, but check the comparables "
                "and the debt-to-equity ratio used to relever."
                % (beta, BETA_LOW, BETA_HIGH))
    else:
        rep.add(INFO, "beta_range", "Levered beta of %.2f is in the usual range." % beta)


def check_growth_reconciliation(rep, dcf):
    """Forecast growth should roughly equal reinvestment rate times return on capital."""
    rows = _get(dcf, "forecast")
    if not isinstance(rows, list) or not rows:
        rep.skip("growth_reconciliation", "no forecast rows in the DCF result")
        return
    worst = None
    for r in rows:
        after_tax = r.get("ebit_after_tax")
        reinvestment = r.get("reinvestment")
        capital = r.get("invested_capital")
        growth = r.get("revenue_growth")
        if not all(isinstance(x, (int, float)) for x in (after_tax, reinvestment, capital, growth)):
            continue
        if after_tax <= 0 or not capital:
            continue
        implied = (reinvestment / after_tax) * (after_tax / capital)
        gap = abs(implied - growth)
        if worst is None or gap > worst[1]:
            worst = (r.get("year"), gap, implied, growth)
    if worst is None:
        rep.skip("growth_reconciliation", "no profitable forecast years to reconcile")
        return
    year, gap, implied, growth = worst
    if gap > GROWTH_RECONCILIATION_TOLERANCE:
        rep.add(WARN, "growth_reconciliation",
                "In year %s the forecast grows revenue %.1f%% while the reinvestment and "
                "return assumed there support about %.1f%%. A persistent gap means growth "
                "is arriving without capital behind it, or capital is being spent without "
                "growth to show for it." % (year, growth * 100, implied * 100),
                {"year": year, "forecast_growth": growth, "implied_growth": implied})
    else:
        rep.add(INFO, "growth_reconciliation",
                "Forecast growth and reinvestment reconcile within %.0f basis points."
                % (gap * 10000))


def check_bridge(rep, dcf):
    """The walk from operating assets to equity must add up."""
    b = _get(dcf, "bridge")
    if not isinstance(b, dict):
        rep.skip("equity_bridge", "no bridge block in the DCF result")
        return
    ops = b.get("value_of_operating_assets")
    equity = b.get("equity_value")
    if ops is None or equity is None:
        rep.skip("equity_bridge", "bridge is missing operating asset or equity value")
        return
    # `less_*` fields are stored as positive magnitudes, so subtract them.
    expected = (ops - abs(b.get("less_debt", 0)) - abs(b.get("less_minority_interests", 0))
                + b.get("plus_cash", 0) + b.get("plus_non_operating_assets", 0))
    if abs(expected - equity) > ARITHMETIC_TOLERANCE * max(1.0, abs(equity)):
        rep.add(ERROR, "equity_bridge",
                "The equity bridge does not add up: %.2f expected from the line items "
                "against %.2f reported." % (expected, equity), b)
    else:
        rep.add(INFO, "equity_bridge", "The equity bridge adds up.")

    shares = b.get("shares_outstanding")
    vps = _get(dcf, "value_per_share")
    common = b.get("equity_in_common_stock", equity)
    if shares and vps is not None:
        if abs(common / shares - vps) > ARITHMETIC_TOLERANCE * max(1.0, abs(vps)):
            rep.add(ERROR, "value_per_share",
                    "Value per share does not equal equity in common stock divided by "
                    "shares outstanding.")
        else:
            rep.add(INFO, "value_per_share", "Value per share ties to the share count.")


def check_constraints(rep, classification, dcf, relative):
    """Honour the hard stops the company's type imposes."""
    if not classification:
        rep.skip("constraints", "no classification artifact")
        return
    constraints = classification.get("constraints") or []
    names = {c.get("rule") if isinstance(c, dict) else c for c in constraints}
    if not names:
        rep.add(INFO, "constraints", "No hard constraints were recorded.")
        return

    method = (_get(dcf, "method") or _get(dcf, "model") or "").lower()
    if "no-fcff-valuation" in names and "fcff" in method:
        rep.add(ERROR, "constraints",
                "Classification forbids an FCFF valuation for this company, but the DCF "
                "used one. For a financial service firm debt is raw material rather than "
                "financing, so there is no meaningful cost of capital to discount at; "
                "value equity directly with dividends or an excess return model.")

    if "require-failure-probability" in names:
        p = _get(dcf, "failure", "probability")
        if not p:
            rep.add(ERROR, "constraints",
                    "Classification requires an explicit probability of failure, but the "
                    "DCF carries none. A going-concern DCF alone prices only the branch "
                    "where the company survives.")

    if "no-earnings-multiple" in names and relative:
        used = [m.get("multiple") for m in (relative.get("multiples") or [])
                if isinstance(m, dict)]
        banned = [m for m in used if m and any(
            tag in str(m).upper() for tag in ("PE", "P/E", "EV/EBIT"))]
        if banned:
            rep.add(ERROR, "constraints",
                    "Earnings multiples (%s) were used although earnings are negative or "
                    "at a cycle trough, which makes them meaningless."
                    % ", ".join(str(b) for b in banned))

    rep.add(INFO, "constraints", "Checked %d recorded constraint(s)." % len(names),
            sorted(str(n) for n in names))


def check_tax_rates(rep, dcf):
    rows = _get(dcf, "forecast") or []
    bad = [r.get("year") for r in rows
           if isinstance(r.get("tax_rate"), (int, float))
           and not 0 <= r["tax_rate"] <= 1]
    if bad:
        rep.add(ERROR, "tax_rate", "Tax rate outside 0-100%% in year(s) %s." % bad)
    elif rows:
        rep.add(INFO, "tax_rate", "All forecast tax rates are between 0 and 100%.")
    else:
        rep.skip("tax_rate", "no forecast rows")


# -------------------------------------------------------------------------------- main

def run(paths):
    mandate = load(paths.get("mandate"))
    classification = load(paths.get("classification"))
    capital = load(paths.get("capital"))
    forecast = load(paths.get("forecast"))
    dcf = load(paths.get("dcf"))
    relative = load(paths.get("relative"))

    rep = Report()
    check_currency(rep, mandate, capital, forecast, dcf)
    check_terminal_growth(rep, capital, dcf)
    check_terminal_reinvestment(rep, dcf)
    check_excess_returns(rep, dcf)
    check_terminal_share(rep, dcf)
    check_weights(rep, capital)
    check_beta(rep, capital)
    check_growth_reconciliation(rep, dcf)
    check_bridge(rep, dcf)
    check_tax_rates(rep, dcf)
    check_constraints(rep, classification, dcf, relative)
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    for name in ("mandate", "classification", "capital", "forecast", "dcf", "relative"):
        ap.add_argument("--" + name, help="path to the %s artifact" % name)
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    ap.add_argument("--quiet", action="store_true", help="show only warnings and errors")
    args = ap.parse_args()

    paths = {n: getattr(args, n) for n in
             ("mandate", "classification", "capital", "forecast", "dcf", "relative")}
    if not any(paths.values()):
        raise SystemExit("Nothing to validate. Pass at least one artifact path; "
                         "run with --help to see the options.")
    rep = run(paths)

    if args.json:
        print(json.dumps({"findings": rep.findings, "skipped": rep.skipped,
                          "error_count": len(rep.errors),
                          "passed": not rep.errors}, indent=2))
    else:
        order = {ERROR: 0, WARN: 1, INFO: 2}
        for f in sorted(rep.findings, key=lambda x: order[x["severity"]]):
            if args.quiet and f["severity"] == INFO:
                continue
            print("[%-5s] %-24s %s" % (f["severity"], f["check"], f["message"]))
        for s in rep.skipped:
            if not args.quiet:
                print("[SKIP ] %-24s %s" % (s["check"], s["reason"]))
        print("\n%d error(s), %d warning(s)."
              % (len(rep.errors),
                 len([f for f in rep.findings if f["severity"] == WARN])))
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())

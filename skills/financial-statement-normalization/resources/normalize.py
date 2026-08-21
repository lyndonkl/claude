#!/usr/bin/env python3
"""
normalize.py — turn reported financial statements into the numbers a valuation needs.

Accounting statements are not built for valuation. Research spending is expensed when it
is really an investment, leases were long kept off the balance sheet when they are really
debt, and one-off items sit inside operating income. This script applies the standard
corrections and then derives the cash flows, capital base and returns that follow.

Every function is a pure numeric transform. Deciding *which* items are non-recurring, or
what amortizable life research spending has, is the analyst's call and arrives as input.

Pure standard library. No third-party packages, ever — this must run anywhere.

SUBCOMMANDS
  capitalize-rd     R&D history -> research asset, amortization, adjusted operating income
  capitalize-leases lease commitments -> lease debt, adjusted operating income
  cashflow          FCFF and FCFE from the corrected statements
  invested-capital  the capital base and the returns earned on it
  normalize-earnings cyclical/trough earnings -> mid-cycle earnings
  ratios            the diagnostic ratio pack
  full              run the whole chain in dependency order
  selftest          run the bundled worked examples and report pass/fail

Each subcommand reads a JSON payload (--in FILE, or stdin) and writes JSON to stdout.
Run any subcommand with --example to print a sample input payload.
"""

import argparse
import json
import sys


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


# ------------------------------------------------------------------ R&D capitalization

def capitalize_rd(current_rd, past_rd, amortizable_life):
    """Treat research spending as the capital investment it is.

    `past_rd` runs backwards: index 0 is last year, index 1 the year before, and so on.
    Spending from `amortizable_life` years ago is fully written off and contributes
    nothing. The current year's spend is entirely unamortized.
    """
    life = int(amortizable_life)
    if life < 1:
        raise SystemExit("amortizable_life must be at least 1 year.")

    rows = [{"year_offset": 0, "expense": float(current_rd),
             "unamortized_fraction": 1.0, "unamortized_value": float(current_rd),
             "amortization_this_year": 0.0}]
    amortization = 0.0
    for i, spend in enumerate(past_rd[:life]):
        years_ago = i + 1
        spend = float(spend)
        fraction = max(0.0, (life - years_ago) / life)
        # Each past year contributes one year's worth of write-off to this year's charge.
        charge = spend / life
        amortization += charge
        rows.append({"year_offset": -years_ago, "expense": spend,
                     "unamortized_fraction": fraction,
                     "unamortized_value": spend * fraction,
                     "amortization_this_year": charge})

    research_asset = sum(r["unamortized_value"] for r in rows)
    return {
        "amortizable_life": life,
        "detail": rows,
        "research_asset": research_asset,
        "amortization_this_year": amortization,
        "adjustment_to_operating_income": float(current_rd) - amortization,
        "note": ("Add adjustment_to_operating_income to reported EBIT and research_asset "
                 "to invested capital. Both must move together or returns are overstated."),
    }


def cmd_capitalize_rd(args):
    p = _read_payload(args)
    _emit(capitalize_rd(p["current_rd"], p.get("past_rd", []), p["amortizable_life"]))


# ---------------------------------------------------------------- lease capitalization

def capitalize_leases(commitments, lump_sum_beyond, pre_tax_cost_of_debt,
                      current_lease_expense=0.0):
    """Convert operating lease commitments into debt.

    `commitments` is the next few years of contracted payments in order. `lump_sum_beyond`
    is the single figure companies disclose for everything after that; the number of years
    it covers is inferred by dividing it by the average of the itemized years, which is
    the convention the source models use.
    """
    r = float(pre_tax_cost_of_debt)
    if r <= 0:
        raise SystemExit("pre_tax_cost_of_debt must be positive to discount lease commitments.")
    commitments = [float(c) for c in commitments]
    n = len(commitments)

    detail = []
    pv = 0.0
    for i, c in enumerate(commitments):
        t = i + 1
        discounted = c / (1 + r) ** t
        pv += discounted
        detail.append({"year": t, "commitment": c, "present_value": discounted})

    embedded_years = 0
    if lump_sum_beyond and n:
        average = sum(commitments) / n
        embedded_years = int(round(lump_sum_beyond / average)) if average > 0 else 0
    if embedded_years > 0:
        annual = lump_sum_beyond / embedded_years
        # An annuity running `embedded_years` long, starting after the itemized years.
        annuity_pv = annual * (1 - (1 + r) ** -embedded_years) / r
        discounted = annuity_pv / (1 + r) ** n
        pv += discounted
        detail.append({"year": "%d-%d" % (n + 1, n + embedded_years),
                       "commitment": lump_sum_beyond, "annual_equivalent": annual,
                       "present_value": discounted})
    elif lump_sum_beyond:
        discounted = lump_sum_beyond / (1 + r) ** (n + 1)
        pv += discounted
        detail.append({"year": n + 1, "commitment": lump_sum_beyond,
                       "present_value": discounted})

    total_life = n + embedded_years
    depreciation = pv / total_life if total_life else 0.0
    return {
        "detail": detail,
        "lease_debt": pv,
        "implied_lease_life_years": total_life,
        "depreciation_on_lease_asset": depreciation,
        "adjustment_to_operating_income": float(current_lease_expense) - depreciation,
        "imputed_lease_interest": pv * r,
        "note": ("Add lease_debt to debt and to invested capital, and add "
                 "adjustment_to_operating_income to EBIT. Note the circularity: the "
                 "discount rate is the pre-tax cost of debt, which a synthetic rating "
                 "derives from interest coverage, which imputed lease interest changes. "
                 "Iterate until the rate stops moving."),
    }


def cmd_capitalize_leases(args):
    p = _read_payload(args)
    _emit(capitalize_leases(p["commitments"], p.get("lump_sum_beyond", 0.0),
                            p["pre_tax_cost_of_debt"], p.get("current_lease_expense", 0.0)))


# ------------------------------------------------------------------------- cash flows

def free_cash_flows(p):
    """FCFF and FCFE from corrected statements.

    FCFF is what the whole business generates before any financing. FCFE is what is left
    for shareholders after lenders are paid and net borrowing is counted.
    """
    ebit = float(p["ebit"])
    tax_rate = float(p.get("tax_rate", 0.0))
    capex = float(p.get("capital_expenditures", 0.0))
    depreciation = float(p.get("depreciation", 0.0))
    delta_wc = float(p.get("change_in_noncash_working_capital", 0.0))
    acquisitions = float(p.get("acquisitions", 0.0))
    rd_adjustment = float(p.get("rd_capitalized_this_year", 0.0))

    ebit_after_tax = ebit * (1 - tax_rate) if ebit > 0 else ebit
    # Capitalized research and cash acquisitions are capital spending in substance even
    # when the statements put them elsewhere.
    net_capex = capex + acquisitions + rd_adjustment - depreciation
    reinvestment = net_capex + delta_wc
    fcff = ebit_after_tax - reinvestment

    out = {
        "ebit": ebit, "tax_rate": tax_rate, "ebit_after_tax": ebit_after_tax,
        "net_capital_expenditures": net_capex,
        "change_in_noncash_working_capital": delta_wc,
        "reinvestment": reinvestment,
        "reinvestment_rate": (reinvestment / ebit_after_tax) if ebit_after_tax > 0 else None,
        "fcff": fcff,
    }

    net_income = p.get("net_income")
    if net_income is not None:
        net_income = float(net_income)
        debt_ratio = p.get("debt_ratio")
        if debt_ratio is not None:
            # Stable-leverage shortcut: shareholders fund only the equity share of
            # reinvestment because debt funds the rest in constant proportion.
            d = float(debt_ratio)
            fcfe = net_income - (net_capex + delta_wc) * (1 - d)
            out["fcfe_method"] = "stable leverage"
            out["equity_funded_share_of_reinvestment"] = 1 - d
        else:
            new_debt = float(p.get("new_debt_issued", 0.0))
            debt_repaid = float(p.get("debt_repaid", 0.0))
            fcfe = net_income - net_capex - delta_wc + (new_debt - debt_repaid)
            out["fcfe_method"] = "explicit debt cash flows"
            out["net_debt_issued"] = new_debt - debt_repaid
        out["net_income"] = net_income
        out["fcfe"] = fcfe
    return out


def cmd_cashflow(args):
    _emit(free_cash_flows(_read_payload(args)))


# ------------------------------------------------------------------- capital and returns

def invested_capital(p):
    """The capital base, and the return the business earns on it.

    Cash is excluded because it earns a financial return, not an operating one; leaving it
    in understates the return on the operating business.
    """
    bv_equity = float(p["book_value_of_equity"])
    bv_debt = float(p["book_value_of_debt"])
    cash = float(p.get("cash", 0.0))
    lease_debt = float(p.get("lease_debt", 0.0))
    research_asset = float(p.get("research_asset", 0.0))

    capital = bv_equity + bv_debt - cash + lease_debt + research_asset
    out = {
        "components": {"book_value_of_equity": bv_equity, "book_value_of_debt": bv_debt,
                       "less_cash": -cash, "plus_lease_debt": lease_debt,
                       "plus_research_asset": research_asset},
        "invested_capital": capital,
    }
    ebit_after_tax = p.get("ebit_after_tax")
    if ebit_after_tax is not None and capital:
        roic = float(ebit_after_tax) / capital
        out["roic"] = roic
        wacc = p.get("cost_of_capital")
        if wacc is not None:
            out["cost_of_capital"] = float(wacc)
            out["return_spread"] = roic - float(wacc)
            out["economic_value_added"] = (roic - float(wacc)) * capital
            out["creates_value"] = roic > float(wacc)
    net_income = p.get("net_income")
    if net_income is not None and bv_equity:
        out["roe"] = float(net_income) / bv_equity
    return out


def cmd_invested_capital(args):
    _emit(invested_capital(_read_payload(args)))


# ------------------------------------------------------------------ normalized earnings

def normalize_earnings(p):
    """Mid-cycle earnings for a company caught at a peak or a trough.

    Two routes. Averaging the margin over a full cycle and applying it to current revenue
    keeps the company's current scale. Averaging the return on capital and applying it to
    current capital keeps its current asset base.
    """
    method = p.get("method", "average_margin")
    if method == "average_margin":
        margins = [float(m) for m in p["historical_margins"]]
        if not margins:
            raise SystemExit("historical_margins must not be empty.")
        avg = sum(margins) / len(margins)
        revenue = float(p["current_revenue"])
        return {"method": method, "average_margin": avg, "current_revenue": revenue,
                "normalized_ebit": avg * revenue, "years_averaged": len(margins),
                "reported_ebit": p.get("reported_ebit")}
    if method == "average_roc":
        rocs = [float(x) for x in p["historical_roc"]]
        if not rocs:
            raise SystemExit("historical_roc must not be empty.")
        avg = sum(rocs) / len(rocs)
        capital = float(p["current_invested_capital"])
        return {"method": method, "average_roc": avg, "current_invested_capital": capital,
                "normalized_ebit_after_tax": avg * capital, "years_averaged": len(rocs),
                "reported_ebit": p.get("reported_ebit")}
    if method == "average_earnings":
        earnings = [float(x) for x in p["historical_earnings"]]
        if not earnings:
            raise SystemExit("historical_earnings must not be empty.")
        avg = sum(earnings) / len(earnings)
        return {"method": method, "normalized_earnings": avg, "years_averaged": len(earnings),
                "reported_ebit": p.get("reported_ebit"),
                "caveat": ("Averaging raw earnings ignores growth in scale over the cycle. "
                           "Prefer average_margin or average_roc when the company has grown.")}
    raise SystemExit("method must be average_margin, average_roc, or average_earnings.")


def cmd_normalize_earnings(args):
    _emit(normalize_earnings(_read_payload(args)))


# ----------------------------------------------------------------------------- ratios

def ratios(p):
    """The diagnostic pack: margins, turnover, leverage, coverage, liquidity."""
    def div(a, b):
        a, b = (None if a is None else float(a)), (None if b is None else float(b))
        return None if (a is None or not b) else a / b

    revenue = p.get("revenue")
    out = {
        "margins": {
            "gross_margin": div(p.get("gross_profit"), revenue),
            "operating_margin": div(p.get("ebit"), revenue),
            "net_margin": div(p.get("net_income"), revenue),
            "ebitda_margin": div(p.get("ebitda"), revenue),
        },
        "efficiency": {
            "sales_to_capital": div(revenue, p.get("invested_capital")),
            "asset_turnover": div(revenue, p.get("total_assets")),
            "noncash_wc_as_percent_of_revenue": div(
                p.get("noncash_working_capital"), revenue),
        },
        "leverage": {
            "debt_to_capital": div(p.get("debt"),
                                   (p.get("debt") or 0) + (p.get("equity") or 0) or None),
            "debt_to_equity": div(p.get("debt"), p.get("equity")),
            "interest_coverage": div(p.get("ebit"), p.get("interest_expense")),
            "net_debt_to_ebitda": div(
                (p.get("debt") or 0) - (p.get("cash") or 0) if p.get("debt") is not None else None,
                p.get("ebitda")),
        },
        "liquidity": {
            "current_ratio": div(p.get("current_assets"), p.get("current_liabilities")),
            "quick_ratio": div(
                (p.get("current_assets") or 0) - (p.get("inventory") or 0)
                if p.get("current_assets") is not None else None,
                p.get("current_liabilities")),
        },
    }
    roic = div(p.get("ebit_after_tax"), p.get("invested_capital"))
    if roic is not None:
        out["returns"] = {"roic": roic, "roe": div(p.get("net_income"), p.get("equity"))}
        wacc = p.get("cost_of_capital")
        if wacc is not None:
            out["returns"]["return_spread"] = roic - float(wacc)
    return out


def cmd_ratios(args):
    _emit(ratios(_read_payload(args)))


# -------------------------------------------------------------------------------- full

def full(p):
    """Run the corrections in dependency order and hand back one consolidated view."""
    out = {}
    ebit = float(p["reported_ebit"])
    adjustments = []

    if p.get("research"):
        rd = capitalize_rd(p["research"]["current_rd"], p["research"].get("past_rd", []),
                           p["research"]["amortizable_life"])
        out["research_and_development"] = rd
        ebit += rd["adjustment_to_operating_income"]
        adjustments.append({"item": "R&D capitalization",
                            "ebit_effect": rd["adjustment_to_operating_income"],
                            "capital_effect": rd["research_asset"]})

    if p.get("leases"):
        lz = capitalize_leases(
            p["leases"]["commitments"], p["leases"].get("lump_sum_beyond", 0.0),
            p["leases"]["pre_tax_cost_of_debt"],
            p["leases"].get("current_lease_expense", 0.0))
        out["operating_leases"] = lz
        ebit += lz["adjustment_to_operating_income"]
        adjustments.append({"item": "Lease capitalization",
                            "ebit_effect": lz["adjustment_to_operating_income"],
                            "capital_effect": lz["lease_debt"]})

    for item in p.get("one_time_items", []):
        # Non-recurring charges are added back; non-recurring gains are removed.
        ebit += float(item["ebit_effect"])
        adjustments.append({"item": item.get("description", "one-time item"),
                            "ebit_effect": float(item["ebit_effect"]), "capital_effect": 0.0})

    out["adjustments"] = adjustments
    out["reported_ebit"] = float(p["reported_ebit"])
    out["adjusted_ebit"] = ebit

    cap_payload = dict(p.get("capital", {}))
    cap_payload.setdefault("book_value_of_equity", 0.0)
    cap_payload.setdefault("book_value_of_debt", 0.0)
    if "research_and_development" in out:
        cap_payload["research_asset"] = out["research_and_development"]["research_asset"]
    if "operating_leases" in out:
        cap_payload["lease_debt"] = out["operating_leases"]["lease_debt"]
    tax_rate = float(p.get("tax_rate", 0.0))
    cap_payload["ebit_after_tax"] = ebit * (1 - tax_rate) if ebit > 0 else ebit
    cap_payload.setdefault("cost_of_capital", p.get("cost_of_capital"))
    out["capital"] = invested_capital(cap_payload)

    if p.get("cash_flow"):
        cf = dict(p["cash_flow"])
        cf["ebit"] = ebit
        cf.setdefault("tax_rate", tax_rate)
        if "research_and_development" in out:
            cf["rd_capitalized_this_year"] = out["research_and_development"]["detail"][0]["expense"]
        out["cash_flows"] = free_cash_flows(cf)
    return out


def cmd_full(args):
    _emit(full(_read_payload(args)))


# ---------------------------------------------------------------------------- selftest

EXAMPLES = {
    "capitalize-rd": {"current_rd": 100.0, "past_rd": [90.0, 80.0, 70.0, 60.0, 50.0],
                      "amortizable_life": 5},
    "capitalize-leases": {"commitments": [100.0, 100.0, 100.0, 100.0, 100.0],
                          "lump_sum_beyond": 300.0, "pre_tax_cost_of_debt": 0.05,
                          "current_lease_expense": 110.0},
    "cashflow": {"ebit": 1000.0, "tax_rate": 0.25, "capital_expenditures": 300.0,
                 "depreciation": 200.0, "change_in_noncash_working_capital": 50.0,
                 "net_income": 600.0, "debt_ratio": 0.3},
    "invested-capital": {"book_value_of_equity": 5000.0, "book_value_of_debt": 3000.0,
                         "cash": 1000.0, "ebit_after_tax": 750.0, "cost_of_capital": 0.08},
    "normalize-earnings": {"method": "average_margin",
                           "historical_margins": [0.12, 0.08, -0.02, 0.05, 0.11],
                           "current_revenue": 10000.0, "reported_ebit": -200.0},
    "ratios": {"revenue": 10000.0, "ebit": 1200.0, "ebitda": 1600.0, "net_income": 700.0,
               "debt": 3000.0, "equity": 5000.0, "cash": 1000.0, "interest_expense": 150.0,
               "invested_capital": 7000.0, "ebit_after_tax": 900.0, "cost_of_capital": 0.08},
    "full": {"reported_ebit": 1000.0, "tax_rate": 0.25, "cost_of_capital": 0.08,
             "research": {"current_rd": 100.0, "past_rd": [90.0, 80.0, 70.0, 60.0],
                          "amortizable_life": 5},
             "capital": {"book_value_of_equity": 5000.0, "book_value_of_debt": 3000.0,
                         "cash": 1000.0},
             "cash_flow": {"capital_expenditures": 300.0, "depreciation": 200.0,
                           "change_in_noncash_working_capital": 50.0}},
}


def cmd_selftest(args):
    results = []

    def check(name, actual, expected, tol=1e-6):
        ok = (expected is True and actual is True) or (
            isinstance(actual, (int, float)) and isinstance(expected, (int, float))
            and abs(actual - expected) <= tol * max(1.0, abs(expected)))
        results.append({"case": name, "expected": expected, "actual": actual, "pass": bool(ok)})

    # R&D over a 5-year life: fractions run 1, 4/5, 3/5, 2/5, 1/5.
    rd = capitalize_rd(100.0, [90.0, 80.0, 70.0, 60.0, 50.0], 5)
    expected_asset = 100 + 90 * 0.8 + 80 * 0.6 + 70 * 0.4 + 60 * 0.2 + 50 * 0.0
    check("research asset", rd["research_asset"], expected_asset)
    check("R&D amortization", rd["amortization_this_year"], (90 + 80 + 70 + 60 + 50) / 5)
    check("R&D operating income adjustment", rd["adjustment_to_operating_income"],
          100.0 - (90 + 80 + 70 + 60 + 50) / 5)
    # Spending exactly one life ago is fully written off.
    check("oldest R&D year is fully amortized", rd["detail"][5]["unamortized_value"], 0.0)

    # Flat R&D forever: the adjustment washes out, which is the sanity check that the
    # correction only matters when research spending is changing.
    flat = capitalize_rd(100.0, [100.0] * 5, 5)
    check("flat R&D leaves operating income unchanged",
          flat["adjustment_to_operating_income"], 0.0)

    # Leases: 5 years of 100 plus a 300 lump implies 3 more years of 100.
    lz = capitalize_leases([100.0] * 5, 300.0, 0.05, 110.0)
    check("implied lease life", lz["implied_lease_life_years"], 8)
    manual = sum(100 / 1.05 ** t for t in range(1, 6))
    manual += (100 * (1 - 1.05 ** -3) / 0.05) / 1.05 ** 5
    check("lease debt", lz["lease_debt"], manual)
    check("lease depreciation", lz["depreciation_on_lease_asset"], manual / 8)
    check("imputed lease interest", lz["imputed_lease_interest"], manual * 0.05)

    # FCFF and the stable-leverage FCFE shortcut.
    cf = free_cash_flows(EXAMPLES["cashflow"])
    check("net capital expenditures", cf["net_capital_expenditures"], 100.0)
    check("FCFF", cf["fcff"], 1000 * 0.75 - 100 - 50)
    check("FCFE at stable leverage", cf["fcfe"], 600 - (100 + 50) * 0.7)

    # Explicit debt flows route.
    cf2 = free_cash_flows({"ebit": 1000.0, "tax_rate": 0.25, "capital_expenditures": 300.0,
                           "depreciation": 200.0, "change_in_noncash_working_capital": 50.0,
                           "net_income": 600.0, "new_debt_issued": 200.0,
                           "debt_repaid": 50.0})
    check("FCFE with explicit debt flows", cf2["fcfe"], 600 - 100 - 50 + 150)

    # Invested capital excludes cash and picks up the corrections.
    ic = invested_capital({"book_value_of_equity": 5000.0, "book_value_of_debt": 3000.0,
                           "cash": 1000.0, "lease_debt": 500.0, "research_asset": 250.0,
                           "ebit_after_tax": 750.0, "cost_of_capital": 0.08})
    check("invested capital", ic["invested_capital"], 5000 + 3000 - 1000 + 500 + 250)
    check("ROIC", ic["roic"], 750 / 7750)
    check("EVA", ic["economic_value_added"], (750 / 7750 - 0.08) * 7750)

    # Normalizing a trough year lifts earnings back to mid-cycle.
    ne = normalize_earnings(EXAMPLES["normalize-earnings"])
    check("normalized EBIT", ne["normalized_ebit"], (0.12 + 0.08 - 0.02 + 0.05 + 0.11) / 5 * 10000)
    results.append({"case": "normalization lifts a trough year", "expected": True,
                    "actual": True, "pass": ne["normalized_ebit"] > -200.0})

    # Negative EBIT must not be taxed.
    loss = free_cash_flows({"ebit": -500.0, "tax_rate": 0.25})
    check("losses are not taxed", loss["ebit_after_tax"], -500.0)

    # The full chain must thread R&D through EBIT and capital together.
    fl = full(EXAMPLES["full"])
    rd2 = capitalize_rd(100.0, [90.0, 80.0, 70.0, 60.0], 5)
    check("full chain adjusted EBIT", fl["adjusted_ebit"],
          1000.0 + rd2["adjustment_to_operating_income"])
    check("full chain capital includes research asset",
          fl["capital"]["invested_capital"],
          5000 + 3000 - 1000 + rd2["research_asset"])

    # Ratios.
    rt = ratios(EXAMPLES["ratios"])
    check("operating margin", rt["margins"]["operating_margin"], 0.12)
    check("interest coverage", rt["leverage"]["interest_coverage"], 8.0)
    check("sales to capital", rt["efficiency"]["sales_to_capital"], 10000 / 7000)
    check("debt to capital", rt["leverage"]["debt_to_capital"], 3000 / 8000)

    # Missing inputs must yield null, not a crash.
    sparse = ratios({"revenue": 100.0})
    results.append({"case": "missing inputs return null rather than failing",
                    "expected": True, "actual": True,
                    "pass": sparse["margins"]["net_margin"] is None})

    failed = [x for x in results if not x["pass"]]
    _emit({"total": len(results), "passed": len(results) - len(failed),
           "failed": len(failed), "results": results})
    return 1 if failed else 0


COMMANDS = {
    "capitalize-rd": cmd_capitalize_rd, "capitalize-leases": cmd_capitalize_leases,
    "cashflow": cmd_cashflow, "invested-capital": cmd_invested_capital,
    "normalize-earnings": cmd_normalize_earnings, "ratios": cmd_ratios,
    "full": cmd_full, "selftest": cmd_selftest,
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

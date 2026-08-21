#!/usr/bin/env python3
"""
reference_data.py — the bundled reference tables, served from one place.

Industry averages and country risk premiums are inputs to almost every other engine in
this suite: bottom-up betas read unlevered beta and EV/Sales, the earnings normaliser
reads sector margins, the cost of equity reads country premiums. Hardcoding those numbers
in each engine is how a valuation ends up mixing a 2020 beta with a 2022 country premium.
This script is the single reader, and every answer it returns carries its vintage.

It looks things up and weights them. It does not estimate anything. Which industry is
comparable, which countries a company is really exposed to, and whether revenue is the
right exposure measure are the analyst's judgments and arrive as inputs.

Pure standard library. No third-party packages, ever — this must run anywhere.

SUBCOMMANDS
  lookup              industry, country or region name -> the full reference row
  erp-for-operations  revenue shares by country -> the revenue-weighted equity risk premium
  vintage             the as_of date of every bundled table, checked against a valuation date
  selftest            run the bundled worked examples and report pass/fail

Each subcommand reads a JSON payload (--in FILE, or stdin) and writes JSON to stdout.
Run any subcommand with --example to print a sample input payload.
"""

import argparse
import datetime
import difflib
import json
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Which bundled file backs each lookup table, and the key its rows live under.
TABLES = {
    "industry": {"file": "industry_averages.json", "rows_key": "rows", "name_key": "industry"},
    "country": {"file": "country_risk.json", "rows_key": "countries", "name_key": "country"},
    "region": {"file": "country_risk.json", "rows_key": "regions", "name_key": "region"},
}

# Where each bundled file keeps its rows, for the vintage report's row counts. Files
# absent from this map are still reported; they simply report no counts. The report walks
# the data directory rather than a fixed list, so a table added later cannot go unchecked.
ROW_COLLECTIONS = {
    "industry_averages.json": {"industries": "rows"},
    "country_risk.json": {"countries": "countries", "regions": "regions"},
}

# Damodaran reposts these tables every January. A valuation dated more than twelve months
# after a table's as_of is therefore running on a vintage that has already been superseded.
STALE_AFTER_DAYS = 365

# Days per year including the leap-day quarter, so "years stale" reads the way a human
# would count it rather than drifting a day every four years.
DAYS_PER_YEAR = 365.25

# difflib similarity below this produces suggestions too loose to be useful — "Steel" would
# start matching "Shoe". 0.6 is the point where suggestions stay recognisable.
SUGGESTION_CUTOFF = 0.6
MAX_SUGGESTIONS = 6


# --------------------------------------------------------------------------- helpers

def _read_payload(args):
    if getattr(args, "in_file", None):
        try:
            with open(args.in_file) as f:
                raw = f.read()
        except OSError as e:
            raise SystemExit("Could not read --in file %r: %s" % (args.in_file, e.strerror))
    else:
        raw = sys.stdin.read()
    raw = raw.strip()
    if not raw:
        raise SystemExit(
            "No input. Pass --in FILE or pipe JSON on stdin. "
            "Run this subcommand with --example to see the expected shape."
        )
    try:
        payload = json.loads(raw)
    except ValueError as e:
        raise SystemExit(
            "Input is not valid JSON (%s). Check for a trailing comma, a single quote where "
            "a double quote belongs, or shell text mixed into the pipe. Run this subcommand "
            "with --example to see the expected shape." % e
        )
    if not isinstance(payload, dict):
        raise SystemExit(
            "Input must be a JSON object, got %s. Run this subcommand with --example to see "
            "the expected shape." % type(payload).__name__
        )
    return payload


def _emit(obj):
    print(json.dumps(obj, indent=2))


def _load(filename):
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path) as f:
            return json.load(f)
    except OSError:
        raise SystemExit(
            "Bundled table %s is missing from %s. Reinstall the skill, or pass your own copy "
            "with data_dir." % (filename, DATA_DIR)
        )


def _normalize(name):
    """Fold case and collapse whitespace, so ' aerospace/defense ' finds Aerospace/Defense.

    Nothing else is folded. Punctuation carries meaning in these keys: the sheet ships
    truncated labels such as 'Insurance (Prop/Cas.)' and they are the actual keys.
    """
    return " ".join(str(name).split()).lower()


def _table(kind, data_dir=None):
    """Return (document, rows, name_key) for one lookup table."""
    spec = TABLES[kind]
    if data_dir:
        path = os.path.join(data_dir, spec["file"])
        try:
            with open(path) as f:
                doc = json.load(f)
        except OSError:
            raise SystemExit("No %s in data_dir %r." % (spec["file"], data_dir))
    else:
        doc = _load(spec["file"])
    return doc, doc[spec["rows_key"]], spec["name_key"]


def _suggest(query, names):
    """Near matches for a name that did not resolve, best first.

    Two passes, because they fail on different mistakes: difflib catches typos and wrong
    endings, substring containment catches a caller who typed a fragment of a long label.
    """
    q = _normalize(query)
    ranked = difflib.get_close_matches(q, [_normalize(n) for n in names],
                                       n=MAX_SUGGESTIONS, cutoff=SUGGESTION_CUTOFF)
    by_norm = {}
    for n in names:
        by_norm.setdefault(_normalize(n), n)
    out = [by_norm[r] for r in ranked]
    if q:
        for n in names:
            if n not in out and q in _normalize(n):
                out.append(n)
    return out[:MAX_SUGGESTIONS]


def find_row(kind, name, data_dir=None):
    """Fetch one reference row by name, forgiving case and surrounding whitespace.

    A miss raises with the near matches rather than returning nothing, because the caller
    almost always has the right row in mind under a slightly different label.
    """
    doc, rows, name_key = _table(kind, data_dir)
    if not isinstance(name, str) or not name.strip():
        raise SystemExit(
            "%s name must be a non-empty string, got %r. Example: "
            '{"%s": "%s"}' % (kind.capitalize(), name, kind, rows[0][name_key])
        )
    wanted = _normalize(name)
    for row in rows:
        if _normalize(row[name_key]) == wanted:
            return doc, row
    names = [r[name_key] for r in rows]
    near = _suggest(name, names)
    hint = ("Closest matches: %s." % ", ".join(repr(n) for n in near)) if near else (
        "No name in the table resembles it.")
    # The industry sheet ships labels truncated mid-word, and those truncations are the
    # real keys, so an industry miss gets that warning; a country miss has no such trap.
    quirk = (" The sheet ships some labels truncated mid-word, such as "
             "'Insurance (Prop/Cas.)', and those truncations are the real keys."
             if kind == "industry" else "")
    raise SystemExit(
        "Unknown %s %r in the %s vintage. %s All %d keys are listed in %s.%s"
        % (kind, name, doc.get("vintage", "bundled"), hint, len(rows),
           os.path.join(DATA_DIR, TABLES[kind]["file"]), quirk)
    )


def _check_vintage(doc, requested, kind):
    if requested is not None and requested != doc.get("vintage"):
        raise SystemExit(
            "The bundled %s table is vintage %r, not the requested %r. Mixing vintages inside "
            "one valuation is the error this check exists to catch. Either drop the vintage "
            "field to accept what is bundled, or point data_dir at the vintage you want."
            % (kind, doc.get("vintage"), requested)
        )


# ---------------------------------------------------------------------------- lookup

def lookup(payload):
    kinds = [k for k in ("industry", "country", "region") if k in payload]
    kind = payload.get("table")
    if kind is not None and kind not in TABLES:
        raise SystemExit(
            "table must be one of: %s. Got %r." % (", ".join(sorted(TABLES)), kind))
    if kind is not None:
        name = payload.get("name")
        if name is None:
            raise SystemExit(
                'With "table" you must also pass "name". Example: '
                '{"table": "country", "name": "Brazil"}')
    elif len(kinds) == 1:
        kind, name = kinds[0], payload[kinds[0]]
    elif len(kinds) > 1:
        raise SystemExit(
            "Pass exactly one of industry, country or region, got %s. Look them up one at a "
            "time so the answer carries one table's vintage." % ", ".join(kinds))
    else:
        raise SystemExit(
            'Nothing to look up. Pass one of {"industry": ...}, {"country": ...}, '
            '{"region": ...}, or {"table": ..., "name": ...}. '
            "Run lookup --example to see the expected shape.")

    doc, row = find_row(kind, name, payload.get("data_dir"))
    _check_vintage(doc, payload.get("vintage"), kind)

    name_key = TABLES[kind]["name_key"]
    fields = payload.get("fields")
    if fields:
        if not isinstance(fields, list):
            raise SystemExit('fields must be a list of column names, for example '
                             '["unlevered_beta", "ev_sales"].')
        unknown = [f for f in fields if f not in row]
        if unknown:
            raise SystemExit(
                "Unknown field(s) %s on a %s row. Available: %s."
                % (", ".join(repr(f) for f in unknown), kind,
                   ", ".join(k for k in row if k != name_key)))
        body = {name_key: row[name_key]}
        body.update({f: row[f] for f in fields})
    else:
        body = dict(row)

    out = {
        "table": kind,
        "query": name,
        "matched_name": row[name_key],
        "exact_match": row[name_key] == name,
        "as_of": doc["as_of"],
        "vintage": doc["vintage"],
        "source": doc["source"],
        "row": body,
    }
    if any(v is None for v in body.values()):
        out["null_fields_note"] = doc["na_means"]
    return out


def cmd_lookup(args):
    _emit(lookup(_read_payload(args)))


# ---------------------------------------------------------- operation-weighted premium

# Keys accepted as the exposure measure, in the order they are preferred. Revenue is the
# usual weight, but the method is indifferent: production location suits a resource
# company and asset location suits a manufacturer, so both go in under `exposure`.
WEIGHT_KEYS = ("weight", "revenue", "exposure")


def erp_for_operations(payload):
    """Revenue-weight country equity risk premiums into one company premium.

    Company ERP = sum(weight_i * ERP_i), weights being that geography's share of the
    exposure measure. The company CRP is that weighted premium less the mature-market
    premium, which is what gets attached to a cost of equity.

    Each row names a `country` or a `region` in the bundled table, or supplies its own
    `erp` under any `name` — the free row every version of this sheet keeps for a
    "rest of world" bucket that maps to nothing clean.
    """
    rows_in = payload.get("operations") or payload.get("rows")
    if not rows_in:
        raise SystemExit(
            'Pass "operations": a list of geographies with an exposure weight, for example '
            '[{"country": "Brazil", "revenue": 130}, {"country": "Canada", "revenue": 23}]. '
            "Run erp-for-operations --example to see the expected shape.")
    if not isinstance(rows_in, list):
        raise SystemExit('"operations" must be a list of objects, got %s.'
                         % type(rows_in).__name__)

    data_dir = payload.get("data_dir")
    doc = None
    detail = []
    for i, r in enumerate(rows_in):
        if not isinstance(r, dict):
            raise SystemExit(
                'operations[%d] must be an object such as {"country": "Brazil", '
                '"revenue": 130}, got %s.' % (i, type(r).__name__))
        weight = None
        for k in WEIGHT_KEYS:
            if r.get(k) is not None:
                weight = r[k]
                break
        if weight is None:
            raise SystemExit(
                "operations[%d] (%s) has no exposure measure. Give it one of: %s — revenues, "
                "production or assets, whichever measures where the risk actually sits."
                % (i, r.get("country") or r.get("region") or r.get("name") or "unnamed",
                   ", ".join(WEIGHT_KEYS)))
        if not isinstance(weight, (int, float)) or isinstance(weight, bool):
            raise SystemExit("operations[%d] exposure must be a number, got %r." % (i, weight))
        if weight < 0:
            raise SystemExit(
                "operations[%d] exposure is negative (%s). Exposure shares cannot be negative; "
                "if a segment lost money, weight it by revenue rather than operating income."
                % (i, weight))

        named = [k for k in ("country", "region") if r.get(k)]
        if len(named) > 1:
            raise SystemExit(
                "operations[%d] names both a country and a region. Pick one level and use it "
                "for every row, so the weights sit on one table." % i)
        if named:
            kind = named[0]
            d, row = find_row(kind, r[kind], data_dir)
            doc = doc or d
            _check_vintage(d, payload.get("vintage"), kind)
            entry = {"name": row[TABLES[kind]["name_key"]], "source": kind,
                     "erp": row["erp"], "crp": row["crp"]}
        elif r.get("erp") is not None:
            if not isinstance(r["erp"], (int, float)) or isinstance(r["erp"], bool):
                raise SystemExit("operations[%d] erp must be a number, got %r." % (i, r["erp"]))
            entry = {"name": r.get("name", "supplied"), "source": "supplied",
                     "erp": float(r["erp"]), "crp": None}
        else:
            raise SystemExit(
                'operations[%d] names no geography. Give it a "country", a "region", or an '
                'explicit "erp" for a rest-of-world bucket that maps to no table row.' % i)
        entry["exposure"] = float(weight)
        detail.append(entry)

    total = sum(e["exposure"] for e in detail)
    if total <= 0:
        raise SystemExit(
            "Total exposure across the operations is %s. It must be positive — the weights "
            "are shares of it." % total)

    doc = doc or _load("country_risk.json")
    mature = payload.get("mature_market_erp", doc["mature_market_erp"])
    for e in detail:
        e["weight"] = e["exposure"] / total
        if e["crp"] is None:
            # A supplied rest-of-world premium carries no table CRP, so back it out of the
            # mature premium the same way the country rows already have it backed out.
            e["crp"] = e["erp"] - mature
        e["weighted_erp"] = e["erp"] * e["weight"]

    company_erp = sum(e["weighted_erp"] for e in detail)
    out = {
        "equity_risk_premium": company_erp,
        "country_risk_premium": company_erp - mature,
        "mature_market_erp": mature,
        "total_exposure": total,
        "as_of": doc["as_of"],
        "vintage": doc["vintage"],
        "operations": detail,
    }

    rf = payload.get("riskfree_rate")
    beta = payload.get("beta")
    if rf is not None and beta is not None:
        # The two operation-weighted attachments. They differ in whether beta is taken to
        # measure country-risk exposure on top of everything else; it usually is not
        # established that it does, so both are reported rather than one chosen.
        out["cost_of_equity"] = {
            "constant_exposure": rf + beta * mature + (company_erp - mature),
            "beta_exposure": rf + beta * company_erp,
            "riskfree_rate": rf,
            "beta": beta,
        }
    elif rf is not None or beta is not None:
        out["cost_of_equity_note"] = (
            "Both riskfree_rate and beta are needed to turn this premium into a cost of "
            "equity; only one was supplied, so the premium is returned on its own.")
    return out


def cmd_erp_for_operations(args):
    _emit(erp_for_operations(_read_payload(args)))


# --------------------------------------------------------------------------- vintage

def _parse_as_of(text, label):
    """Accept YYYY, YYYY-MM or YYYY-MM-DD. A year or a month resolves to its first day.

    A bare year is a real vintage in this data — the default-probability study is dated
    only to the year it was published — and resolving it to January 1 makes it the oldest
    reading of that year, which is the conservative way for a staleness check to read it.
    """
    parts = str(text).split("-")
    try:
        if len(parts) == 1:
            return datetime.date(int(parts[0]), 1, 1)
        if len(parts) == 2:
            return datetime.date(int(parts[0]), int(parts[1]), 1)
        if len(parts) == 3:
            return datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        pass
    raise SystemExit(
        "%s %r is not a date this script can read. Use YYYY-MM-DD, YYYY-MM or YYYY, for "
        'example "2024-06-30".' % (label, text))


def bundled_files():
    """Every JSON table in the data directory, in a stable order.

    Walked rather than listed, so a table dropped in later is checked for staleness like
    the rest instead of quietly ageing out of sight.
    """
    try:
        names = sorted(f for f in os.listdir(DATA_DIR) if f.endswith(".json"))
    except OSError:
        raise SystemExit(
            "The bundled data directory %s is missing. Reinstall the skill." % DATA_DIR)
    if not names:
        raise SystemExit("No reference tables found in %s. Reinstall the skill." % DATA_DIR)
    return names


def vintage(payload):
    """Report every bundled table's as_of, and flag the ones a valuation has outrun."""
    valuation_date = payload.get("valuation_date")
    as_of_date = None
    if valuation_date is not None:
        as_of_date = _parse_as_of(valuation_date, "valuation_date")

    tables, warnings = [], []
    for filename in bundled_files():
        doc = _load(filename)
        name = filename[:-len(".json")]
        entry = {
            "table": name,
            "file": os.path.join("data", filename),
            "as_of": doc.get("as_of"),
            "vintage": doc.get("vintage"),
            "source": doc.get("source"),
        }
        counts = {label: len(doc[key])
                  for label, key in ROW_COLLECTIONS.get(filename, {}).items() if key in doc}
        if counts:
            entry["row_counts"] = counts
        if doc.get("as_of_note"):
            entry["as_of_note"] = doc["as_of_note"]

        if entry["as_of"] is None:
            entry["warning"] = (
                "%s carries no as_of date, so its age cannot be checked. Add one before "
                "relying on it." % name)
            warnings.append(entry["warning"])
        elif as_of_date is not None:
            table_date = _parse_as_of(doc["as_of"], "%s as_of" % name)
            age_days = (as_of_date - table_date).days
            entry["age_days"] = age_days
            entry["age_years"] = age_days / DAYS_PER_YEAR
            entry["stale"] = age_days > STALE_AFTER_DAYS
            if entry["stale"]:
                warning = (
                    "%s is %.1f years older than the valuation date. Refresh it before "
                    "relying on it: %s"
                    % (name, entry["age_years"], doc.get("refresh", "no refresh source recorded")))
                entry["warning"] = warning
                warnings.append(warning)
            elif age_days < 0:
                # A table dated after the valuation embeds information the valuation could
                # not have had. Harmless for a teaching case, wrong for a dated appraisal.
                entry["warning"] = (
                    "%s is dated after the valuation date, so it carries information that was "
                    "not available then. Fine for a study, wrong for a dated appraisal." % name)
                warnings.append(entry["warning"])
        tables.append(entry)

    out = {"tables": tables, "stale_after_days": STALE_AFTER_DAYS, "warnings": warnings}
    if as_of_date is not None:
        out["valuation_date"] = valuation_date
        out["any_stale"] = any(t.get("stale") for t in tables)
    else:
        out["note"] = ('Pass {"valuation_date": "YYYY-MM-DD"} to have each table checked '
                       "against the date of the valuation.")
    return out


def cmd_vintage(args):
    _emit(vintage(_read_payload(args)))


# --------------------------------------------------------------------------- selftest

EXAMPLES = {
    "lookup": {"industry": "Aerospace/Defense"},
    "erp-for-operations": {
        "operations": [
            {"country": "China", "revenue": 800},
            {"country": "United States", "revenue": 1200},
        ],
        "riskfree_rate": 0.02,
        "beta": 0.95,
    },
    "vintage": {"valuation_date": "2024-06-30"},
}


def _close(actual, expected, tol=1e-6):
    return abs(actual - expected) <= tol * max(1.0, abs(expected))


def cmd_selftest(args):
    """Worked examples taken from the source models, so a port can be verified."""
    results = []

    def check(name, actual, expected, tol=1e-6):
        results.append({"case": name, "expected": expected, "actual": actual,
                        "pass": _close(actual, expected, tol)})

    def assert_true(name, ok, actual=True):
        results.append({"case": name, "expected": True, "actual": actual, "pass": bool(ok)})

    def refuses(name, fn):
        try:
            fn()
            assert_true(name, False, "no error raised")
        except SystemExit:
            assert_true(name, True)

    industry = _load("industry_averages.json")
    countries = _load("country_risk.json")

    # --- the tables arrived intact -------------------------------------------------
    assert_true("industry table carries 94 industries plus the two market totals",
                len(industry["rows"]) == 96, len(industry["rows"]))
    assert_true("industry rows keep all 26 statistics",
                all(len(r) == 27 for r in industry["rows"]),
                min(len(r) for r in industry["rows"]))
    assert_true("country table carries every sovereign in the sheet",
                len(countries["countries"]) == 186, len(countries["countries"]))
    assert_true("regional aggregates carry the nine regions plus Global",
                len(countries["regions"]) == 10, len(countries["regions"]))

    # --- M07 lookups (divginzu US industry averages) -------------------------------
    aero = lookup({"industry": "Aerospace/Defense"})["row"]
    check("Aerospace/Defense unlevered beta", aero["unlevered_beta"], 1.07852)
    check("Aerospace/Defense EV/Sales", aero["ev_sales"], 2.26617)
    check("Aerospace/Defense sales-to-capital", aero["sales_to_capital"], 3.1505)

    # NA must survive as null. Read as 0 it would say a money-center bank trades at zero
    # times EBITDA, and any average taken over the column would be wrong.
    bank = lookup({"industry": "Bank (Money Center)"})["row"]
    assert_true("bank EV/EBITDA is null, not zero", bank["ev_ebitda"] is None, bank["ev_ebitda"])
    assert_true("bank reinvestment rate is null, not zero",
                bank["reinvestment_rate"] is None, bank["reinvestment_rate"])
    check("bank price-to-book survives alongside the nulls", bank["price_to_book"], 1.27092)

    # A degenerate row is data, not a typo: Environmental & Waste Services really does
    # carry a trailing PE of 735 in this vintage. Keep it verbatim.
    check("degenerate trailing PE kept verbatim",
          lookup({"industry": "Environmental & Waste Services"})["row"]["trailing_pe"], 735.049)

    # --- M06 lookups (divginzu Country ERP) ----------------------------------------
    chile = lookup({"country": "Chile"})["row"]
    check("Chile adjusted default spread", chile["adj_default_spread"], 0.00588343)
    check("Chile total ERP", chile["erp"], 0.06384)
    check("Chile ERP is the mature premium plus its CRP", chile["erp"],
          countries["mature_market_erp"] + chile["crp"])
    check("Chile CRP is the spread scaled by relative equity volatility", chile["crp"],
          chile["adj_default_spread"] * countries["relative_equity_volatility_multiplier"], 1e-5)

    # The sheet's own country VLOOKUP range stops short of the last alphabetical rows and
    # returns 0.0133509 for the United States (inventory defect Q3). An exact match over
    # the full table must return zero, so this test fails on the sheet's implementation.
    us = lookup({"country": "United States"})["row"]
    check("United States default spread is zero, not the sheet's truncated-range answer",
          us["adj_default_spread"], 0.0)
    check("United States ERP equals the mature-market premium", us["erp"], 0.0569)

    # Unrated sovereigns keep a populated spread and a null rating.
    algeria = lookup({"country": "Algeria"})["row"]
    assert_true("unrated sovereign has a null rating",
                algeria["moodys_rating"] is None, algeria["moodys_rating"])
    check("unrated sovereign still carries a spread", algeria["adj_default_spread"], 0.054384)

    # --- forgiving names, unforgiving misses ---------------------------------------
    check("case and whitespace are forgiven",
          lookup({"country": "  united KINGDOM \n"})["row"]["erp"], 0.0617936)
    assert_true("a forgiven match is reported as inexact",
                lookup({"industry": " aerospace/defense "})["exact_match"] is False)
    assert_true("a near miss suggests the real key",
                "Aerospace/Defense" in _suggest("Aerospace Defense",
                                                [r["industry"] for r in industry["rows"]]))
    assert_true("a fragment suggests the truncated label it belongs to",
                "Insurance (Prop/Cas.)" in _suggest("Prop/Cas",
                                                    [r["industry"] for r in industry["rows"]]))
    refuses("an unknown industry is refused, not returned empty",
            lambda: lookup({"industry": "Blockchain"}))
    refuses("an unknown country is refused", lambda: lookup({"country": "Wakanda"}))
    refuses("looking up two tables at once is refused",
            lambda: lookup({"industry": "Steel", "country": "Brazil"}))
    refuses("an empty lookup payload is refused", lambda: lookup({}))
    refuses("a mismatched vintage is refused",
            lambda: lookup({"country": "Brazil", "vintage": "jan-2022"}))

    # --- M06/M24 operation-weighted ERP --------------------------------------------
    # divginzu 'ERP calculator', country table: China 800, US 1200 -> cell E15 = 0.059676.
    # This is the whole chain — bundled lookup, weights, weighted average — so an engine
    # that reads the wrong column or normalises weights wrongly cannot reach it.
    r = erp_for_operations({"operations": [{"country": "China", "revenue": 800},
                                           {"country": "United States", "revenue": 1200}]})
    check("divginzu ERP calculator, country table", r["equity_risk_premium"], 0.059676, 1e-6)
    check("weights are shares of total exposure", r["operations"][0]["weight"], 0.4)

    # Same sheet, region table: cell E29 = 0.069524.
    r = erp_for_operations({"operations": [
        {"region": "Caribbean", "revenue": 10}, {"region": "Middle East", "revenue": 30},
        {"region": "North America", "revenue": 35}, {"region": "Western Europe", "revenue": 15}]})
    check("divginzu ERP calculator, region table", r["equity_risk_premium"], 0.069524, 1e-6)

    # Embraer, September 2004 (operation-weighted-erp concept note): beta 1.07, US$ riskfree
    # 4%, mature ERP 5%, 3% of revenues in Brazil at a 12.89% total ERP.
    emb = erp_for_operations({
        "mature_market_erp": 0.05, "riskfree_rate": 0.04, "beta": 1.07,
        "operations": [{"name": "US and other mature markets", "erp": 0.05, "revenue": 97},
                       {"name": "Brazil", "erp": 0.1289, "revenue": 3}]})
    check("Embraer operation-weighted ERP", emb["equity_risk_premium"], 0.0524, 1e-3)
    check("Embraer CRP is the weighted premium less the mature premium",
          emb["country_risk_premium"], 0.03 * 0.0789, 1e-6)
    check("Embraer cost of equity, constant exposure",
          emb["cost_of_equity"]["constant_exposure"], 0.0959, 1e-3)
    check("Embraer cost of equity, beta exposure",
          emb["cost_of_equity"]["beta_exposure"], 0.0960, 1e-3)
    assert_true("attaching country risk through beta costs more than adding it",
                emb["cost_of_equity"]["beta_exposure"]
                > emb["cost_of_equity"]["constant_exposure"])

    # Ambev, 2011: eight countries weighted by revenue, company ERP 9.11%.
    ambev = erp_for_operations({"mature_market_erp": 0.06, "operations": [
        {"name": "Argentina", "erp": 0.15, "revenue": 19},
        {"name": "Bolivia", "erp": 0.1088, "revenue": 4},
        {"name": "Brazil", "erp": 0.0863, "revenue": 130},
        {"name": "Canada", "erp": 0.06, "revenue": 23},
        {"name": "Chile", "erp": 0.0705, "revenue": 7},
        {"name": "Ecuador", "erp": 0.1275, "revenue": 6},
        {"name": "Paraguay", "erp": 0.12, "revenue": 3},
        {"name": "Peru", "erp": 0.09, "revenue": 12}]})
    check("Ambev operation-weighted ERP", ambev["equity_risk_premium"], 0.0911, 1e-3)
    check("Ambev operation-weighted CRP", ambev["country_risk_premium"], 0.0311, 1e-3)

    # A single-country company gets that country's premium unchanged, whatever the weight.
    solo = erp_for_operations({"operations": [{"country": "Brazil", "revenue": 42}]})
    check("one country returns that country's premium", solo["equity_risk_premium"],
          lookup({"country": "Brazil"})["row"]["erp"])

    # An all-mature-market company must land exactly on the mature premium, with no CRP.
    mature = erp_for_operations({"operations": [{"country": "United States", "revenue": 3},
                                                {"country": "Germany", "revenue": 1}]})
    check("mature markets only leaves no country risk", mature["country_risk_premium"], 0.0)

    refuses("a geography with no exposure measure is refused",
            lambda: erp_for_operations({"operations": [{"country": "Brazil"}]}))
    refuses("zero total exposure is refused",
            lambda: erp_for_operations({"operations": [{"country": "Brazil", "revenue": 0}]}))
    refuses("a negative exposure share is refused",
            lambda: erp_for_operations({"operations": [{"country": "Brazil", "revenue": -5}]}))
    refuses("a row naming no geography at all is refused",
            lambda: erp_for_operations({"operations": [{"name": "elsewhere", "revenue": 10}]}))
    refuses("an empty operations list is refused", lambda: erp_for_operations({}))

    # --- vintage --------------------------------------------------------------------
    v = vintage({})
    reported = [t["table"] for t in v["tables"]]
    assert_true("vintage reports every JSON table in the data directory",
                len(v["tables"]) == len(bundled_files()), reported)
    assert_true("the two tables this script serves are both reported",
                {"industry_averages", "country_risk"} <= set(reported), reported)
    assert_true("every bundled table carries an as_of, or says why it cannot be checked",
                all(t.get("as_of") or t.get("warning") for t in v["tables"]))
    assert_true("country_risk reports both of its row collections",
                [t for t in v["tables"] if t["table"] == "country_risk"][0]["row_counts"]
                == {"countries": 186, "regions": 10})

    v = vintage({"valuation_date": "2024-06-30"})
    assert_true("a 2024 valuation on 2020 tables is flagged stale", v["any_stale"] is True)
    ind = [t for t in v["tables"] if t["table"] == "industry_averages"][0]
    assert_true("the stale warning names where to refresh the table",
                "stern.nyu.edu" in ind["warning"], ind.get("warning"))
    # 2020-01-01 to 2024-06-30 is 1642 days.
    check("age in years from as_of to the valuation date", ind["age_years"], 1642 / 365.25, 1e-9)

    # A bare year is a real vintage in this data and must read as that year's January 1.
    check("a bare-year as_of reads as January 1",
          (_parse_as_of("2013", "t") - datetime.date(2013, 1, 1)).days, 0)

    # Inside a year of its as_of a table is not flagged; a day past the year mark, it is.
    ind = [t for t in vintage({"valuation_date": "2020-12-31"})["tables"]
           if t["table"] == "industry_averages"][0]
    assert_true("a table under a year old is not flagged", ind["stale"] is False)
    ind = [t for t in vintage({"valuation_date": "2021-01-02"})["tables"]
           if t["table"] == "industry_averages"][0]
    assert_true("a table one day past a year old is flagged", ind["stale"] is True)

    # A valuation dated before the table is a different mistake, and gets a different warning.
    v = vintage({"valuation_date": "2019-06-30"})
    ind = [t for t in v["tables"] if t["table"] == "industry_averages"][0]
    assert_true("a table dated after the valuation is flagged as hindsight",
                "hindsight" in ind.get("warning", "").lower()
                or "not available then" in ind.get("warning", ""), ind.get("warning"))
    refuses("an unreadable valuation date is refused",
            lambda: vintage({"valuation_date": "June 2024"}))

    failed = [r for r in results if not r["pass"]]
    _emit({"total": len(results), "passed": len(results) - len(failed),
           "failed": len(failed), "results": results})
    return 1 if failed else 0


# ------------------------------------------------------------------------------- main

COMMANDS = {
    "lookup": cmd_lookup,
    "erp-for-operations": cmd_erp_for_operations,
    "vintage": cmd_vintage,
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

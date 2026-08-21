#!/usr/bin/env python3
"""
simulate.py — turn a point-estimate valuation into a distribution.

The base-case DCF is unchanged. This script replaces the two or three drivers you are
least sure about with probability distributions, runs the same engine thousands of times,
and reports the distribution of the answer: percentiles, mean, standard deviation, the
probability the value clears the market price, and the share of draws the engine refused
as infeasible.

The valuation itself is not reimplemented here. Every trial calls the DCF engine in
../../dcf-valuation-engine/resources/dcf.py, so the simulated model and the base-case
model are literally the same code.

A seed is required, not optional. A valuation that cannot be re-run to the same number
cannot be audited, and "I ran a simulation and got 42" is not a reproducible claim.

The output is a distribution of your assumptions, not a distribution of reality. Someone
chose every shape and every parameter in the input.

Pure standard library. No third-party packages, ever — this must run anywhere.

SUBCOMMANDS
  simulate     base case + driver distributions -> the value distribution
  sample       draw one or more distributions on their own, without the DCF
  scenarios    named discrete scenarios with probabilities -> probability-weighted value
  percentiles  a list of values, or a published percentile table -> stats and price position
  selftest     run the bundled worked examples and report pass/fail

Each subcommand reads a JSON payload (--in FILE, or stdin) and writes JSON to stdout.
Run any subcommand with --example to print a sample input payload.
"""

import argparse
import copy
import importlib.util
import json
import math
import os
import random
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
# The sibling skill directory layout is fixed: skills/<name>/resources/<script>.py
DEFAULT_DCF_PATH = os.path.join(
    os.path.dirname(os.path.dirname(HERE)),
    "dcf-valuation-engine", "resources", "dcf.py")
CASES_PATH = os.path.join(DATA_DIR, "simulation_cases.json")

# Monte Carlo error shrinks with the square root of the trial count, so the middle of the
# distribution settles long before the tails do. 10,000 trials pins the median of a
# well-behaved valuation to well inside its input precision; Damodaran's published Paytm
# run used 100,000, which is what the 5th and 95th percentiles need to stop moving.
DEFAULT_TRIALS = 10000

# Percentiles reported by default. The 0th and 100th are deliberately excluded from this
# list: they are single draws, they move every run, and quoting them as "the range" is the
# most common way a simulation gets misread. They are still reported, labelled as extremes.
REPORTED_PERCENTILES = (5, 10, 25, 50, 75, 90, 95)

# random.random() can return exactly 0.0, which has no finite normal quantile. Clamping at
# 1e-12 caps any single draw at about 7 standard deviations — beyond any input precision a
# valuation driver carries, and far enough out that the clamp never binds in practice.
UNIFORM_EPSILON = 1e-12

# Probabilities in a discrete scenario set are checked against 1 at this tolerance, which
# is loose enough for figures typed to four decimals and tight enough to catch a real slip.
PROBABILITY_TOLERANCE = 1e-6

# Above this share of refused trials the surviving distribution is no longer a fair
# picture of the input distributions, because the refusals are concentrated in one tail.
REFUSAL_WARNING_SHARE = 0.05

SUPPORTED_DISTRIBUTIONS = ("normal", "lognormal", "triangular", "uniform", "discrete")


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
    except json.JSONDecodeError as exc:
        raise SystemExit("The input is not valid JSON (%s). Check for a trailing comma "
                         "or an unquoted key." % exc)


def _emit(obj):
    print(json.dumps(obj, indent=2))


def _require(payload, key, subcommand):
    if key not in payload:
        raise SystemExit(
            "Missing %r. The %s payload needs it. Run `%s --example` to see the shape."
            % (key, subcommand, subcommand))
    return payload[key]


def _seed_of(payload):
    """A seed is mandatory. Reproducibility is the difference between a valuation and a
    number someone once saw on a screen."""
    if "seed" not in payload:
        raise SystemExit(
            "Missing 'seed'. A seed is required so the run can be reproduced and audited. "
            "Pick any integer, record it alongside the result, and reuse it to re-run.")
    seed = payload["seed"]
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise SystemExit("'seed' must be an integer, not %s." % type(seed).__name__)
    return seed


def _trials_of(payload):
    trials = payload.get("trials", DEFAULT_TRIALS)
    if isinstance(trials, bool) or not isinstance(trials, int) or trials < 2:
        raise SystemExit("'trials' must be an integer of at least 2 (default %d)."
                         % DEFAULT_TRIALS)
    return trials


_DCF_MODULE = None


def _load_dcf(path=None):
    """Import the DCF engine from the sibling skill and hold onto it.

    Imported rather than shelled out to: a hundred thousand subprocess launches would
    dominate the run time, and an in-process import lets an infeasible draw surface as a
    catchable SystemExit rather than an exit code and a string.
    """
    global _DCF_MODULE
    if _DCF_MODULE is not None and path is None:
        return _DCF_MODULE
    target = path or DEFAULT_DCF_PATH
    if not os.path.exists(target):
        raise SystemExit(
            "Cannot find the DCF engine at %s. It ships with the dcf-valuation-engine "
            "skill. Set 'dcf_path' in the payload to point at it." % target)
    spec = importlib.util.spec_from_file_location("dcf_engine", target)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "value"):
        raise SystemExit("%s does not expose a value() function; it is not the DCF engine."
                         % target)
    if path is None:
        _DCF_MODULE = module
    return module


def _set_path(payload, path, new_value, label):
    """Write a scalar at a dotted path such as `terminal.growth_rate`."""
    parts = path.split(".")
    node = payload
    for key in parts[:-1]:
        if not isinstance(node, dict) or key not in node:
            raise SystemExit(
                "Driver %r points at %r, but %r is not an object in the base case. "
                "Check the path against the base-case payload." % (label, path, key))
        node = node[key]
    leaf = parts[-1]
    if not isinstance(node, dict):
        raise SystemExit("Driver %r points at %r, which is not a settable field."
                         % (label, path))
    if isinstance(node.get(leaf), (dict, list)):
        raise SystemExit(
            "Driver %r points at %r, which holds a %s rather than a number. Point at a "
            "leaf such as '%s.start' or '%s.end' instead."
            % (label, path, type(node[leaf]).__name__, path, path))
    node[leaf] = new_value


def _get_path(obj, path, what):
    node = obj
    for key in path.split("."):
        if not isinstance(node, dict) or key not in node:
            raise SystemExit(
                "The DCF result has no field %r (looking for %s). Pick a field the engine "
                "returns, such as 'value_per_share' or 'value_of_operating_assets'."
                % (path, what))
        node = node[key]
    if node is None:
        raise SystemExit(
            "The DCF returned null for %r. If you are reading 'value_per_share', set "
            "bridge.shares_outstanding in the base case." % path)
    if not isinstance(node, (int, float)) or isinstance(node, bool):
        raise SystemExit("The DCF field %r is not a number, so it cannot be simulated."
                         % path)
    return float(node)


# ------------------------------------------------------------- normal distribution maths

def _norm_cdf(z):
    # The error function gives the standard normal CDF exactly: Phi(z) = (1 + erf(z/root2))/2.
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


# Peter Acklam's rational approximation to the inverse standard normal CDF. The published
# coefficient set below is accurate to about 1.15e-9 in absolute value across the whole
# range; the Halley refinement in _norm_ppf then takes it to machine precision. The
# constants have no individual meaning — they are the fitted coefficients of the two
# rational functions, and the break points 0.02425 and 1 - 0.02425 separate the tail
# branches from the central branch.
_ACKLAM_A = (-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
             1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00)
_ACKLAM_B = (-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
             6.680131188771972e+01, -1.328068155288572e+01)
_ACKLAM_C = (-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
             -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00)
_ACKLAM_D = (7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
             3.754408661907416e+00)
_ACKLAM_BREAK = 0.02425


def _norm_ppf(u):
    """Inverse standard normal CDF: the z with Phi(z) = u."""
    u = min(max(float(u), UNIFORM_EPSILON), 1.0 - UNIFORM_EPSILON)
    if u < _ACKLAM_BREAK:
        q = math.sqrt(-2 * math.log(u))
        z = ((((((_ACKLAM_C[0] * q + _ACKLAM_C[1]) * q + _ACKLAM_C[2]) * q + _ACKLAM_C[3])
               * q + _ACKLAM_C[4]) * q + _ACKLAM_C[5])
             / ((((_ACKLAM_D[0] * q + _ACKLAM_D[1]) * q + _ACKLAM_D[2]) * q
                 + _ACKLAM_D[3]) * q + 1))
    elif u > 1 - _ACKLAM_BREAK:
        q = math.sqrt(-2 * math.log(1 - u))
        z = -((((((_ACKLAM_C[0] * q + _ACKLAM_C[1]) * q + _ACKLAM_C[2]) * q + _ACKLAM_C[3])
                * q + _ACKLAM_C[4]) * q + _ACKLAM_C[5])
              / ((((_ACKLAM_D[0] * q + _ACKLAM_D[1]) * q + _ACKLAM_D[2]) * q
                  + _ACKLAM_D[3]) * q + 1))
    else:
        q = u - 0.5
        r = q * q
        z = ((((((_ACKLAM_A[0] * r + _ACKLAM_A[1]) * r + _ACKLAM_A[2]) * r + _ACKLAM_A[3])
               * r + _ACKLAM_A[4]) * r + _ACKLAM_A[5]) * q
             / (((((_ACKLAM_B[0] * r + _ACKLAM_B[1]) * r + _ACKLAM_B[2]) * r
                  + _ACKLAM_B[3]) * r + _ACKLAM_B[4]) * r + 1))
    # One Halley step against the exact CDF. Cheap, and it removes the approximation error
    # so that _norm_ppf(_norm_cdf(x)) round-trips to full precision.
    err = _norm_cdf(z) - u
    slope = math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    if slope > 0:
        z = z - err / slope / (1 + z * err / slope / 2)
    return z


# ------------------------------------------------------------------- driver distributions

def _number(spec, key, label, required=True, default=None):
    if key not in spec:
        if required:
            raise SystemExit("Distribution for %r (type %s) needs %r."
                             % (label, spec.get("type"), key))
        return default
    v = spec[key]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise SystemExit("Distribution for %r: %r must be a number, not %s."
                         % (label, key, type(v).__name__))
    return float(v)


def _validate_distribution(spec, label):
    """Check a distribution spec once, before any trial runs.

    Every failure here is a specification error the analyst has to fix, so it is worth
    catching before ten thousand trials produce ten thousand identical complaints.
    """
    if not isinstance(spec, dict):
        raise SystemExit("The distribution for %r must be an object with a 'type'." % label)
    kind = spec.get("type")
    if kind not in SUPPORTED_DISTRIBUTIONS:
        raise SystemExit(
            "Unknown distribution type %r for %r. Supported types: %s."
            % (kind, label, ", ".join(SUPPORTED_DISTRIBUTIONS)))

    if kind == "normal":
        sd = _number(spec, "sd", label)
        _number(spec, "mean", label)
        if sd < 0:
            raise SystemExit("Distribution for %r: 'sd' cannot be negative." % label)

    elif kind == "lognormal":
        shift = _number(spec, "shift", label, required=False, default=0.0)
        if "median" in spec:
            median = _number(spec, "median", label)
            log_sd = _number(spec, "log_sd", label)
            if median <= 0:
                raise SystemExit("Distribution for %r: 'median' must be positive; the "
                                 "lognormal body lives above 'shift'." % label)
            if log_sd < 0:
                raise SystemExit("Distribution for %r: 'log_sd' cannot be negative." % label)
        else:
            mean = _number(spec, "mean", label)
            sd = _number(spec, "sd", label)
            if mean - shift <= 0:
                raise SystemExit(
                    "Distribution for %r: a lognormal 'mean' (%g) must sit above 'shift' "
                    "(%g), because the variable cannot fall below the shift."
                    % (label, mean, shift))
            if sd < 0:
                raise SystemExit("Distribution for %r: 'sd' cannot be negative." % label)

    elif kind == "triangular":
        lo = _number(spec, "min", label)
        hi = _number(spec, "max", label)
        mode = _number(spec, "likeliest", label)
        if not lo <= mode <= hi:
            raise SystemExit(
                "Distribution for %r: 'likeliest' (%g) must sit between 'min' (%g) and "
                "'max' (%g)." % (label, mode, lo, hi))
        if hi <= lo:
            raise SystemExit("Distribution for %r: 'max' must exceed 'min'." % label)

    elif kind == "uniform":
        lo = _number(spec, "min", label)
        hi = _number(spec, "max", label)
        if hi < lo:
            raise SystemExit("Distribution for %r: 'max' cannot be below 'min'." % label)

    elif kind == "discrete":
        outcomes = spec.get("outcomes")
        if not isinstance(outcomes, list) or not outcomes:
            raise SystemExit(
                "Distribution for %r: 'outcomes' must be a non-empty list of "
                "{\"value\": x, \"probability\": p}." % label)
        total = 0.0
        for i, item in enumerate(outcomes):
            if not isinstance(item, dict) or "value" not in item or "probability" not in item:
                raise SystemExit("Distribution for %r: outcome %d needs 'value' and "
                                 "'probability'." % (label, i + 1))
            p = float(item["probability"])
            if p < 0:
                raise SystemExit("Distribution for %r: probabilities cannot be negative."
                                 % label)
            total += p
        if abs(total - 1.0) > PROBABILITY_TOLERANCE:
            raise SystemExit(
                "Distribution for %r: the outcome probabilities sum to %.6f, not 1. "
                "Rescale them." % (label, total))


def _quantile(spec, u):
    """Map a uniform draw u in (0,1) to the distribution's value at that probability.

    Everything is sampled through its inverse CDF rather than by a shape-specific
    generator. That is what makes the correlation model work: the same uniform can be
    pushed through any shape, so a common factor can drive a triangular take rate and a
    lognormal growth rate together.
    """
    u = min(max(u, UNIFORM_EPSILON), 1.0 - UNIFORM_EPSILON)
    kind = spec["type"]

    if kind == "normal":
        return spec["mean"] + spec["sd"] * _norm_ppf(u)

    if kind == "lognormal":
        shift = float(spec.get("shift", 0.0))
        if "median" in spec:
            median = float(spec["median"])
            log_sd = float(spec["log_sd"])
        else:
            # Convert an arithmetic mean and standard deviation into the log-space
            # parameters. Skipping this conversion is the classic lognormal error: it
            # silently produces a distribution whose mean is far below the one requested.
            mean = float(spec["mean"]) - shift
            sd = float(spec["sd"])
            log_sd = math.sqrt(math.log(1.0 + (sd / mean) ** 2))
            median = mean * math.exp(-log_sd * log_sd / 2.0)
        return shift + median * math.exp(log_sd * _norm_ppf(u))

    if kind == "triangular":
        lo, hi, mode = float(spec["min"]), float(spec["max"]), float(spec["likeliest"])
        # The CDF reaches this height at the mode; below it the left arm applies.
        split = (mode - lo) / (hi - lo)
        if u < split:
            return lo + math.sqrt(u * (hi - lo) * (mode - lo))
        return hi - math.sqrt((1.0 - u) * (hi - lo) * (hi - mode))

    if kind == "uniform":
        lo, hi = float(spec["min"]), float(spec["max"])
        return lo + u * (hi - lo)

    if kind == "discrete":
        cumulative = 0.0
        outcomes = spec["outcomes"]
        for item in outcomes:
            cumulative += float(item["probability"])
            if u <= cumulative:
                return float(item["value"])
        # Only reachable through floating-point drift in the cumulative sum.
        return float(outcomes[-1]["value"])

    raise SystemExit("Unknown distribution type %r." % kind)


def _prepare_drivers(raw, require_path):
    """Normalize and validate the driver list before any sampling happens."""
    if not isinstance(raw, list) or not raw:
        raise SystemExit("Provide a non-empty list of drivers, each with a name and a "
                         "distribution.")
    prepared = []
    seen = set()
    for i, d in enumerate(raw):
        if not isinstance(d, dict):
            raise SystemExit("Driver %d must be an object." % (i + 1))
        name = d.get("name") or d.get("path") or "driver_%d" % (i + 1)
        if name in seen:
            raise SystemExit("Two drivers are both called %r. Names must be unique so the "
                             "correlation report can be read." % name)
        seen.add(name)

        paths = d.get("paths", d.get("path"))
        if require_path:
            if not paths:
                raise SystemExit("Driver %r needs a 'path' into the base case, such as "
                                 "'operating_margin.end'." % name)
            if isinstance(paths, str):
                paths = [paths]
            if not all(isinstance(p, str) for p in paths):
                raise SystemExit("Driver %r: 'paths' must be a list of dotted strings."
                                 % name)
        else:
            paths = []

        spec = d.get("distribution")
        if spec is None:
            raise SystemExit("Driver %r has no 'distribution'." % name)
        _validate_distribution(spec, name)

        loading = d.get("loading", 0.0)
        if isinstance(loading, bool) or not isinstance(loading, (int, float)):
            raise SystemExit("Driver %r: 'loading' must be a number between -1 and 1."
                             % name)
        loading = float(loading)
        if not -1.0 <= loading <= 1.0:
            raise SystemExit(
                "Driver %r: 'loading' is %g. It is a correlation with the common factor, "
                "so it must lie between -1 and 1." % (name, loading))

        # A linear map turns a sampled macro variable into the driver the model wants.
        # Shell's revenues, for example, are a fitted line on the oil price.
        lmap = d.get("linear_map") or {}
        if not isinstance(lmap, dict):
            raise SystemExit("Driver %r: 'linear_map' must be an object with 'intercept' "
                             "and 'slope'." % name)
        for key in ("intercept", "slope"):
            if key in lmap and (isinstance(lmap[key], bool)
                                or not isinstance(lmap[key], (int, float))):
                raise SystemExit("Driver %r: linear_map.%s must be a number." % (name, key))
        intercept = float(lmap.get("intercept", 0.0))
        slope = float(lmap.get("slope", 1.0))
        if slope == 0:
            raise SystemExit(
                "Driver %r has a linear_map slope of 0, which throws the draw away and "
                "writes a constant. Set a non-zero slope, or drop the driver." % name)

        prepared.append({
            "name": name, "paths": paths, "distribution": spec,
            "factor": d.get("factor", "common"), "loading": loading,
            "intercept": intercept, "slope": slope,
        })
    return prepared


def _iter_draws(drivers, trials, seed):
    """Yield one dict of sampled driver values per trial.

    Correlation is imposed with a single shared common factor. Each driver's latent
    standard normal is

        z_i = loading_i * Z_factor + sqrt(1 - loading_i^2) * e_i

    so two drivers loaded on the same factor carry a latent correlation of
    loading_i * loading_j, and a negative loading anti-correlates with a positive one.
    The latent normal is then pushed through the target distribution's inverse CDF, which
    preserves the rank correlation exactly and the linear correlation approximately.

    Draw order is fixed — factors in sorted name order, then drivers in payload order —
    so the same seed reproduces the same run.
    """
    rng = random.Random(seed)
    factors = sorted({d["factor"] for d in drivers if d["loading"]})
    for _ in range(trials):
        z_factor = {f: _norm_ppf(rng.random()) for f in factors}
        row = {}
        for d in drivers:
            # One uniform per driver per trial, always, whether or not it is correlated.
            # Keeping the draw count fixed means adding a loading changes the correlation
            # without reshuffling every other driver's stream.
            own = _norm_ppf(rng.random())
            loading = d["loading"]
            if loading:
                z = loading * z_factor[d["factor"]] + math.sqrt(1 - loading ** 2) * own
            else:
                z = own
            x = _quantile(d["distribution"], _norm_cdf(z))
            row[d["name"]] = d["intercept"] + d["slope"] * x
        yield row


# ------------------------------------------------------------------------- order statistics

def _percentile(sorted_values, pct):
    """Linear-interpolated percentile, the convention R and numpy call type 7."""
    if not sorted_values:
        raise SystemExit("No values to take a percentile of.")
    if len(sorted_values) == 1:
        return sorted_values[0]
    rank = (len(sorted_values) - 1) * (pct / 100.0)
    lower = int(math.floor(rank))
    upper = min(lower + 1, len(sorted_values) - 1)
    frac = rank - lower
    return sorted_values[lower] + (sorted_values[upper] - sorted_values[lower]) * frac


def _share_below(sorted_values, threshold):
    """Empirical CDF: the share of draws strictly below the threshold."""
    count = 0
    for v in sorted_values:
        if v < threshold:
            count += 1
        else:
            break
    return count / len(sorted_values)


def _describe(values, price=None, extra_percentiles=()):
    ordered = sorted(values)
    pcts = {}
    for p in list(REPORTED_PERCENTILES) + list(extra_percentiles):
        pcts[str(p)] = _percentile(ordered, p)
    out = {
        "count": len(ordered),
        "mean": statistics.fmean(ordered),
        "standard_deviation": statistics.stdev(ordered) if len(ordered) > 1 else 0.0,
        "median": _percentile(ordered, 50),
        "percentiles": pcts,
        "extremes": {
            "minimum": ordered[0], "maximum": ordered[-1],
            "note": "Single draws. Quote the 10th and 90th percentiles as the working "
                    "range, not these.",
        },
        "range_10_to_90": [_percentile(ordered, 10), _percentile(ordered, 90)],
    }
    if price is not None:
        below = _share_below(ordered, price)
        out["versus_price"] = {
            "current_price": price,
            "probability_value_exceeds_price": 1.0 - below,
            "percentile_of_price": below * 100.0,
            "median_over_price": out["median"] / price if price else None,
        }
    return out


def _correlation(xs, ys):
    """Pearson correlation, returned as None when either series has no variation."""
    n = len(xs)
    mx, my = statistics.fmean(xs), statistics.fmean(ys)
    sxy = sxx = syy = 0.0
    for i in range(n):
        dx, dy = xs[i] - mx, ys[i] - my
        sxy += dx * dy
        sxx += dx * dx
        syy += dy * dy
    if sxx <= 0 or syy <= 0:
        return None
    return sxy / math.sqrt(sxx * syy)


# ------------------------------------------------------------------------------ simulate

def simulate(p):
    seed = _seed_of(p)
    trials = _trials_of(p)
    base_case = _require(p, "base_case", "simulate")
    drivers = _prepare_drivers(_require(p, "drivers", "simulate"), require_path=True)
    output_path = p.get("output", "value_per_share")
    dcf = _load_dcf(p.get("dcf_path"))

    refused_value = p.get("refused_value")
    if refused_value is not None and (isinstance(refused_value, bool)
                                      or not isinstance(refused_value, (int, float))):
        raise SystemExit("'refused_value' must be a number, or omitted to drop refused "
                         "trials from the distribution.")

    # Run the base case once, before sampling. If it is infeasible the simulation cannot
    # mean anything, and the error the analyst needs is the base case's own error.
    try:
        base_result = dcf.value(copy.deepcopy(base_case))
    except SystemExit as exc:
        raise SystemExit("The base case itself is infeasible: %s Fix the base case before "
                         "simulating it." % exc)
    base_value = _get_path(base_result, output_path, "the simulated output")

    price = base_case.get("bridge", {}).get("current_price")
    if p.get("current_price") is not None:
        price = p["current_price"]
    if price is not None:
        price = float(price)

    # The engine treats its payload as read-only and every sampled leaf is rewritten on
    # every trial, so one deep copy is enough. Copying per trial would dominate run time.
    working = copy.deepcopy(base_case)

    values = []
    driver_series = {d["name"]: [] for d in drivers}
    refusals = {}
    for row in _iter_draws(drivers, trials, seed):
        for d in drivers:
            x = row[d["name"]]
            driver_series[d["name"]].append(x)
            for path in d["paths"]:
                _set_path(working, path, x, d["name"])
        try:
            result = dcf.value(working)
        except SystemExit as exc:
            # An infeasible combination is information, not a crash. Terminal growth above
            # the discount rate, or reinvestment above 100%, means the draw described a
            # company that cannot exist.
            reason = str(exc).strip()
            refusals[reason] = refusals.get(reason, 0) + 1
            if refused_value is not None:
                values.append(float(refused_value))
            continue
        value_at = result.get(output_path) if "." not in output_path else None
        if value_at is None:
            value_at = _get_path(result, output_path, "the simulated output")
        values.append(float(value_at))

    refused = sum(refusals.values())
    completed = trials - refused
    if completed == 0:
        top = sorted(refusals.items(), key=lambda kv: -kv[1])[:3]
        raise SystemExit(
            "Every one of the %d trials was refused as infeasible. Most common reason: %s "
            "Narrow the distributions so the draws describe possible companies."
            % (trials, top[0][0] if top else "unknown."))
    if not values:
        raise SystemExit("No trials produced a value.")

    out = {
        "seed": seed,
        "trials": trials,
        "completed": completed,
        "refused": refused,
        "refused_share": refused / trials,
        "refusals": [
            {"reason": reason, "count": count, "share": count / trials}
            for reason, count in sorted(refusals.items(), key=lambda kv: -kv[1])
        ],
        "refused_trials_treatment": (
            "assigned the value %g" % refused_value if refused_value is not None
            else "dropped from the distribution"),
        "output_metric": output_path,
        "base_case_value": base_value,
        "distribution": _describe(values, price,
                                  extra_percentiles=p.get("extra_percentiles", ())),
    }
    ordered = sorted(values)
    out["probability_value_at_or_below_zero"] = _share_below(ordered, 0.0) + (
        sum(1 for v in ordered if v == 0.0) / len(ordered))
    out["probability_value_exceeds_base_case"] = 1.0 - _share_below(ordered, base_value)

    out["drivers"] = []
    for d in drivers:
        series = driver_series[d["name"]]
        ordered_series = sorted(series)
        row = {
            "name": d["name"], "paths": d["paths"],
            "distribution": d["distribution"]["type"],
            "factor": d["factor"] if d["loading"] else None,
            "loading": d["loading"],
            "realized_mean": statistics.fmean(series),
            "realized_sd": statistics.stdev(series) if len(series) > 1 else 0.0,
            "realized_p10": _percentile(ordered_series, 10),
            "realized_p50": _percentile(ordered_series, 50),
            "realized_p90": _percentile(ordered_series, 90),
        }
        if d["slope"] != 1.0 or d["intercept"] != 0.0:
            # The statistics above describe what the model received. When a linear map is
            # in play that is not what was sampled, so report the raw draw as well —
            # inverting the map costs nothing and it is the number the analyst reasons in.
            row["linear_map"] = {"intercept": d["intercept"], "slope": d["slope"]}
            row["before_map"] = {
                "mean": (row["realized_mean"] - d["intercept"]) / d["slope"],
                "p10": (_percentile(ordered_series, 10 if d["slope"] > 0 else 90)
                        - d["intercept"]) / d["slope"],
                "p50": (row["realized_p50"] - d["intercept"]) / d["slope"],
                "p90": (_percentile(ordered_series, 90 if d["slope"] > 0 else 10)
                        - d["intercept"]) / d["slope"],
            }
        out["drivers"].append(row)

    pairs = []
    for i in range(len(drivers)):
        for j in range(i + 1, len(drivers)):
            a, b = drivers[i], drivers[j]
            implied = (a["loading"] * b["loading"]
                       if a["factor"] == b["factor"] and a["loading"] and b["loading"]
                       else 0.0)
            pairs.append({
                "a": a["name"], "b": b["name"],
                "implied_latent_correlation": implied,
                "realized_correlation": _correlation(driver_series[a["name"]],
                                                     driver_series[b["name"]]),
            })
    if pairs:
        out["correlations"] = pairs

    warnings = []
    if not any(d["loading"] for d in drivers) and len(drivers) > 1:
        warnings.append(
            "Every driver was sampled independently. If any of them move together in "
            "reality, this run understates both tails and produces combinations that "
            "cannot happen. Set a 'loading' on the drivers that share a cause.")
    if refused / trials > REFUSAL_WARNING_SHARE:
        warnings.append(
            "%.1f%% of trials were refused as infeasible, and refusals cluster in one "
            "tail, so the surviving distribution is not a fair picture of the inputs. "
            "Tighten the distributions rather than reading around it."
            % (refused / trials * 100))
    median = out["distribution"]["median"]
    if base_value and abs(median - base_value) / abs(base_value) > 0.05:
        warnings.append(
            "The simulated median (%.4f) differs from the base case (%.4f) by more than "
            "5%%. That is normal when an input is skewed; it is also the number to quote, "
            "because the base case is one draw." % (median, base_value))
    if trials < 1000:
        warnings.append(
            "%d trials is enough to see the shape but not to trust the 5th and 95th "
            "percentiles. Raise 'trials' before quoting the tails." % trials)
    if warnings:
        out["warnings"] = warnings
    return out


def cmd_simulate(args):
    _emit(simulate(_read_payload(args)))


# -------------------------------------------------------------------------------- sample

def sample(p):
    """Draw the distributions on their own, with no valuation attached.

    Use it to check that a shape does what you meant before wiring it into the model —
    a lognormal specified by its arithmetic mean, for instance, has a median well below
    that mean, and it is better to find that out here.
    """
    seed = _seed_of(p)
    trials = _trials_of(p)
    drivers = _prepare_drivers(_require(p, "distributions", "sample"), require_path=False)

    series = {d["name"]: [] for d in drivers}
    for row in _iter_draws(drivers, trials, seed):
        for name, x in row.items():
            series[name].append(x)

    out = {"seed": seed, "trials": trials, "distributions": []}
    for d in drivers:
        described = _describe(series[d["name"]])
        described["name"] = d["name"]
        described["type"] = d["distribution"]["type"]
        described["loading"] = d["loading"]
        out["distributions"].append(described)

    pairs = []
    for i in range(len(drivers)):
        for j in range(i + 1, len(drivers)):
            a, b = drivers[i], drivers[j]
            implied = (a["loading"] * b["loading"]
                       if a["factor"] == b["factor"] and a["loading"] and b["loading"]
                       else 0.0)
            pairs.append({"a": a["name"], "b": b["name"],
                          "implied_latent_correlation": implied,
                          "realized_correlation": _correlation(series[a["name"]],
                                                               series[b["name"]])})
    if pairs:
        out["correlations"] = pairs
    return out


def cmd_sample(args):
    _emit(sample(_read_payload(args)))


# ----------------------------------------------------------------------------- scenarios

def scenarios(p):
    """Discrete named stories with probabilities, rather than continuous distributions.

    This is the right tool when the doubt is about *which* story is true, not about how
    much of a driver there is. A narrative break — the business stops being the business
    you modelled — is a probability and a consequence, not a wider distribution.
    """
    base_case = _require(p, "base_case", "scenarios")
    rows = _require(p, "scenarios", "scenarios")
    if not isinstance(rows, list) or not rows:
        raise SystemExit("'scenarios' must be a non-empty list of named scenarios.")
    output_path = p.get("output", "value_per_share")
    dcf = _load_dcf(p.get("dcf_path"))

    total = 0.0
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or "probability" not in row:
            raise SystemExit("Scenario %d needs a 'probability'." % (i + 1))
        total += float(row["probability"])
    if abs(total - 1.0) > PROBABILITY_TOLERANCE:
        raise SystemExit(
            "The scenario probabilities sum to %.6f, not 1. A scenario set has to be "
            "exhaustive: add a residual scenario or rescale." % total)

    results = []
    expected = 0.0
    for i, row in enumerate(rows):
        name = row.get("name", "scenario_%d" % (i + 1))
        trial = copy.deepcopy(base_case)
        for path, v in (row.get("overrides") or {}).items():
            _set_path(trial, path, v, name)
        try:
            result = dcf.value(trial)
        except SystemExit as exc:
            raise SystemExit(
                "Scenario %r is infeasible: %s A named scenario is a story you are "
                "putting weight on, so fix it rather than dropping it." % (name, exc))
        v = _get_path(result, output_path, "the scenario output")
        prob = float(row["probability"])
        expected += prob * v
        results.append({"name": name, "probability": prob, "value": v,
                        "overrides": row.get("overrides") or {}})

    values = [r["value"] for r in results]
    out = {
        "output_metric": output_path,
        "scenarios": sorted(results, key=lambda r: -r["value"]),
        "expected_value": expected,
        "spread": {
            "min": min(values), "max": max(values),
            "ratio": (max(values) / min(values)) if min(values) > 0 else None,
        },
    }
    price = p.get("current_price", base_case.get("bridge", {}).get("current_price"))
    if price is not None:
        price = float(price)
        out["versus_price"] = {
            "current_price": price,
            "probability_value_exceeds_price": sum(
                r["probability"] for r in results if r["value"] > price),
            "cheapest_scenario_above_price": min(
                (r for r in results if r["value"] > price),
                key=lambda r: r["value"], default=None),
        }
    return out


def cmd_scenarios(args):
    _emit(scenarios(_read_payload(args)))


# --------------------------------------------------------------------------- percentiles

def percentiles(p):
    """Read a distribution that already exists.

    Two inputs are accepted. A list of raw values, from a prior run or another tool. Or a
    published percentile table, which is how simulation results are usually reported —
    this is what locates a market price inside Damodaran's own published runs.
    """
    price = p.get("current_price")
    if price is not None:
        price = float(price)

    if "values" in p:
        values = p["values"]
        if not isinstance(values, list) or len(values) < 2:
            raise SystemExit("'values' must be a list of at least two numbers.")
        for v in values:
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise SystemExit("'values' must contain only numbers.")
        return {"source": "values",
                "distribution": _describe([float(v) for v in values], price,
                                          extra_percentiles=p.get("extra_percentiles", ()))}

    if "percentile_table" in p:
        table = p["percentile_table"]
        if not isinstance(table, list) or len(table) < 2:
            raise SystemExit(
                "'percentile_table' must be a list of {\"percentile\": q, \"value\": v} "
                "entries, at least two of them.")
        points = []
        for row in table:
            if not isinstance(row, dict) or "percentile" not in row or "value" not in row:
                raise SystemExit("Each percentile_table entry needs 'percentile' and "
                                 "'value'.")
            points.append((float(row["percentile"]), float(row["value"])))
        points.sort()
        if any(points[i][1] > points[i + 1][1] for i in range(len(points) - 1)):
            raise SystemExit("The percentile table is not increasing in value. A percentile "
                             "table has to be sorted by percentile with rising values.")
        out = {"source": "percentile_table",
               "table": [{"percentile": q, "value": v} for q, v in points]}
        if price is None:
            return out
        out["versus_price"] = _locate_in_table(points, price)
        return out

    raise SystemExit("Provide either 'values' (a list of numbers) or 'percentile_table' "
                     "(a published table). Run `percentiles --example` for the shape.")


def _locate_in_table(points, price):
    """Linear interpolation of the percentile a price sits at within a published table."""
    lo_q, lo_v = points[0]
    hi_q, hi_v = points[-1]
    if price <= lo_v:
        return {"current_price": price, "percentile_of_price": lo_q,
                "note": "The price is at or below the bottom of the table, so the "
                        "percentile is a floor, not an estimate."}
    if price >= hi_v:
        return {"current_price": price, "percentile_of_price": hi_q,
                "note": "The price is at or above the top of the table, so the percentile "
                        "is a ceiling, not an estimate."}
    for i in range(len(points) - 1):
        q0, v0 = points[i]
        q1, v1 = points[i + 1]
        if v0 <= price <= v1:
            frac = 0.0 if v1 == v0 else (price - v0) / (v1 - v0)
            q = q0 + (q1 - q0) * frac
            return {
                "current_price": price,
                "percentile_of_price": q,
                "bracket": {"lower_percentile": q0, "lower_value": v0,
                            "upper_percentile": q1, "upper_value": v1},
                "probability_value_exceeds_price": 1.0 - q / 100.0,
            }
    raise SystemExit("Could not locate the price in the table.")


def cmd_percentiles(args):
    _emit(percentiles(_read_payload(args)))


# ---------------------------------------------------------------------------- examples

# A deliberately small base case: five forecast years so the examples run in well under a
# second, and the same driver shapes a real valuation would use.
_BASE = {
    "base_revenue": 1000.0, "base_ebit": 100.0, "base_invested_capital": 500.0,
    "forecast_years": 5,
    "revenue_growth": {"start": 0.20, "end": 0.03, "converge_by": 5},
    "operating_margin": {"start": 0.10, "end": 0.14, "converge_by": 5},
    "sales_to_capital": 2.0, "tax_rate": 0.25, "cost_of_capital": 0.09,
    "terminal": {"growth_rate": 0.02, "cost_of_capital": 0.08, "return_on_capital": 0.12},
    "bridge": {"debt": 200.0, "cash": 100.0, "shares_outstanding": 100.0,
               "current_price": 14.00},
    "currency": "USD",
}

EXAMPLES = {
    "simulate": {
        "seed": 20240101,
        "trials": 5000,
        "base_case": _BASE,
        "output": "value_per_share",
        "drivers": [
            {"name": "revenue growth", "path": "revenue_growth.start",
             "distribution": {"type": "lognormal", "mean": 0.20, "sd": 0.06},
             "factor": "demand", "loading": 0.7},
            {"name": "target margin", "path": "operating_margin.end",
             "distribution": {"type": "triangular", "min": 0.08, "likeliest": 0.14,
                              "max": 0.20},
             "factor": "demand", "loading": 0.5},
            {"name": "sales to capital", "path": "sales_to_capital",
             "distribution": {"type": "uniform", "min": 1.5, "max": 2.5}},
            {"name": "cost of capital", "path": "cost_of_capital",
             "distribution": {"type": "normal", "mean": 0.09, "sd": 0.008}},
        ],
    },
    "sample": {
        "seed": 7,
        "trials": 20000,
        "distributions": [
            {"name": "oil price", "distribution": {"type": "lognormal", "mean": 40.0,
                                                   "sd": 12.0},
             "factor": "macro", "loading": 0.8},
            {"name": "target margin",
             "distribution": {"type": "triangular", "min": 0.05, "likeliest": 0.0935,
                              "max": 0.13},
             "factor": "macro", "loading": 0.6},
            {"name": "regime",
             "distribution": {"type": "discrete",
                              "outcomes": [{"value": 1.0, "probability": 0.7},
                                           {"value": 0.0, "probability": 0.3}]}},
        ],
    },
    "scenarios": {
        "base_case": _BASE,
        "output": "value_per_share",
        "current_price": 14.00,
        "scenarios": [
            {"name": "Category leader", "probability": 0.25,
             "overrides": {"operating_margin.end": 0.18, "revenue_growth.start": 0.30}},
            {"name": "Base case", "probability": 0.50, "overrides": {}},
            {"name": "Competition arrives", "probability": 0.25,
             "overrides": {"operating_margin.end": 0.09, "revenue_growth.start": 0.10}},
        ],
    },
    "percentiles": {
        "current_price": 3270.0,
        "percentile_table": [
            {"percentile": 0, "value": 2203.59}, {"percentile": 10, "value": 2817.08},
            {"percentile": 20, "value": 2906.30}, {"percentile": 30, "value": 2973.67},
            {"percentile": 40, "value": 3033.43}, {"percentile": 50, "value": 3091.51},
            {"percentile": 60, "value": 3150.60}, {"percentile": 70, "value": 3217.16},
            {"percentile": 80, "value": 3299.18}, {"percentile": 90, "value": 3415.91},
            {"percentile": 100, "value": 4495.29}
        ],
    },
}


# ---------------------------------------------------------------------------- selftest

def _load_cases():
    if not os.path.exists(CASES_PATH):
        raise SystemExit("Missing reference data at %s." % CASES_PATH)
    with open(CASES_PATH) as f:
        return json.load(f)


def cmd_selftest(args):
    results = []

    def check(name, actual, expected, tol=1e-6):
        ok = (isinstance(actual, (int, float)) and isinstance(expected, (int, float))
              and not isinstance(actual, bool)
              and abs(actual - expected) <= tol * max(1.0, abs(expected)))
        results.append({"case": name, "expected": expected, "actual": actual,
                        "pass": bool(ok)})

    def check_true(name, actual, detail=None):
        row = {"case": name, "expected": True, "actual": bool(actual),
               "pass": bool(actual)}
        if detail is not None:
            row["detail"] = detail
        results.append(row)

    def check_between(name, actual, lo, hi):
        ok = isinstance(actual, (int, float)) and lo <= actual <= hi
        results.append({"case": name, "expected": "in [%g, %g]" % (lo, hi),
                        "actual": actual, "pass": bool(ok)})

    def refuses(fn, payload):
        """True when the call is refused with an explanation rather than a stack trace."""
        try:
            fn(payload)
            return False
        except SystemExit as exc:
            return bool(str(exc).strip())

    cases = _load_cases()["cases"]

    # ---- 1. The normal machinery, against published values ----------------------------
    # 1.959963985 is the standard normal 97.5th percentile, the z behind every 95%
    # confidence interval, so a broken inverse CDF cannot hide behind it.
    check("inverse normal CDF at 97.5%", _norm_ppf(0.975), 1.959963984540054, 1e-9)
    check("inverse normal CDF at 50%", _norm_ppf(0.5), 0.0, 1e-12)
    check_true("normal CDF and its inverse round-trip",
               all(abs(_norm_ppf(_norm_cdf(x)) - x) < 1e-9
                   for x in (-3.5, -1.0, -0.25, 0.0, 0.25, 1.0, 3.5)))

    # ---- 2. Inverse CDFs at algebraic identities ---------------------------------------
    # At the mode the triangular CDF equals (mode-min)/(max-min) exactly. Getting the two
    # arms of that inverse the wrong way round is the classic triangular bug, and it
    # survives every "does it return a number" test.
    tri = {"type": "triangular", "min": 3.95, "likeliest": 5.95, "max": 7.95}
    check("triangular quantile at the mode returns the mode",
          _quantile(tri, (5.95 - 3.95) / (7.95 - 3.95)), 5.95, 1e-12)
    check("triangular quantile at 0 returns the minimum", _quantile(tri, 0.0), 3.95, 1e-5)
    check("triangular quantile at 1 returns the maximum", _quantile(tri, 1.0), 7.95, 1e-5)
    check("uniform quantile at the midpoint",
          _quantile({"type": "uniform", "min": 0.05, "max": 0.25}, 0.5), 0.15, 1e-12)
    check("normal quantile at the mean",
          _quantile({"type": "normal", "mean": 0.125, "sd": 0.02}, 0.5), 0.125, 1e-12)
    # A lognormal specified by its arithmetic mean must have its median strictly below the
    # mean. An implementation that treats mean and sd as log-space parameters fails here.
    logn = {"type": "lognormal", "mean": 0.20, "sd": 0.06}
    log_sd = math.sqrt(math.log(1 + (0.06 / 0.20) ** 2))
    check("lognormal median sits below its arithmetic mean",
          _quantile(logn, 0.5), 0.20 * math.exp(-log_sd * log_sd / 2), 1e-12)
    check_true("lognormal median is strictly below the mean", _quantile(logn, 0.5) < 0.20)
    # A shift moves the whole distribution without changing its mean.
    shifted = {"type": "lognormal", "mean": 0.0797, "sd": 0.008, "shift": 0.05}
    check_true("shifted lognormal stays above its shift", _quantile(shifted, 1e-9) > 0.05)
    check("discrete quantile picks the first outcome below its cumulative probability",
          _quantile({"type": "discrete",
                     "outcomes": [{"value": 10.0, "probability": 0.3},
                                  {"value": 20.0, "probability": 0.7}]}, 0.29),
          10.0, 1e-12)
    check("discrete quantile crosses to the second outcome above it",
          _quantile({"type": "discrete",
                     "outcomes": [{"value": 10.0, "probability": 0.3},
                                  {"value": 20.0, "probability": 0.7}]}, 0.31),
          20.0, 1e-12)

    # ---- 3. Percentile convention ------------------------------------------------------
    # With ten values 1..10 the type-7 median is 5.5 and the 25th percentile is 3.25.
    ten = [float(i) for i in range(1, 11)]
    check("percentile of 1..10 at 50", _percentile(ten, 50), 5.5, 1e-12)
    check("percentile of 1..10 at 25", _percentile(ten, 25), 3.25, 1e-12)
    check("percentile of 1..10 at 0", _percentile(ten, 0), 1.0, 1e-12)

    # ---- 4. Sampled moments match the specification ------------------------------------
    drawn = sample({"seed": 11, "trials": 40000, "distributions": [
        {"name": "u", "distribution": {"type": "uniform", "min": 0.05, "max": 0.25}},
        {"name": "t", "distribution": tri},
        {"name": "n", "distribution": {"type": "normal", "mean": 0.125, "sd": 0.02}},
        {"name": "l", "distribution": logn},
        {"name": "d", "distribution": {"type": "discrete", "outcomes": [
            {"value": 100.0, "probability": 0.2}, {"value": 50.0, "probability": 0.5},
            {"value": 0.0, "probability": 0.3}]}},
    ]})
    stats = {row["name"]: row for row in drawn["distributions"]}
    # Uniform: mean is the midpoint, sd is the range over the square root of twelve.
    check("uniform sample mean", stats["u"]["mean"], 0.15, 5e-3)
    check("uniform sample sd", stats["u"]["standard_deviation"],
          0.20 / math.sqrt(12), 2e-2)
    # Triangular: the mean of a triangular is the average of its three parameters.
    check("triangular sample mean", stats["t"]["mean"], (3.95 + 5.95 + 7.95) / 3, 5e-3)
    check("normal sample mean", stats["n"]["mean"], 0.125, 5e-3)
    check("normal sample sd", stats["n"]["standard_deviation"], 0.02, 2e-2)
    # Lognormal specified by arithmetic moments must reproduce those moments.
    check("lognormal sample mean matches the requested mean", stats["l"]["mean"], 0.20, 1e-2)
    check("lognormal sample sd matches the requested sd",
          stats["l"]["standard_deviation"], 0.06, 5e-2)
    check_true("lognormal sample is right-skewed",
               stats["l"]["mean"] > stats["l"]["median"])
    # Discrete: the sample mean is the probability-weighted expectation.
    check("discrete sample mean", stats["d"]["mean"],
          100 * 0.2 + 50 * 0.5 + 0 * 0.3, 2e-2)

    # ---- 5. Correlation through the common factor --------------------------------------
    # Two drivers loaded on the same factor carry a latent correlation of the product of
    # their loadings. Independent sampling would score near zero here.
    corr = sample({"seed": 99, "trials": 40000, "distributions": [
        {"name": "a", "distribution": {"type": "normal", "mean": 0.0, "sd": 1.0},
         "factor": "macro", "loading": 0.8},
        {"name": "b", "distribution": {"type": "normal", "mean": 0.0, "sd": 1.0},
         "factor": "macro", "loading": 0.8},
        {"name": "c", "distribution": {"type": "normal", "mean": 0.0, "sd": 1.0},
         "factor": "macro", "loading": -0.5},
        {"name": "d", "distribution": {"type": "normal", "mean": 0.0, "sd": 1.0}},
    ]})
    realized = {(row["a"], row["b"]): row["realized_correlation"]
                for row in corr["correlations"]}
    check("positive loadings give the product as the correlation",
          realized[("a", "b")], 0.64, 3e-2)
    check("an opposite-signed loading anti-correlates",
          realized[("a", "c")], -0.40, 5e-2)
    check_between("an unloaded driver stays independent", realized[("a", "d")],
                  -0.02, 0.02)

    # ---- 6. Degenerate distributions must reproduce the base case exactly ---------------
    # This is the round trip that catches a mis-set path, a mis-read output field or a
    # sampler that ignores its parameters: with no dispersion the simulation is the DCF.
    dcf = _load_dcf()
    base_value = dcf.value(copy.deepcopy(_BASE))["value_per_share"]
    flat = simulate({
        "seed": 1, "trials": 200, "base_case": _BASE,
        "drivers": [
            {"name": "margin", "path": "operating_margin.end",
             "distribution": {"type": "uniform", "min": 0.14, "max": 0.14}},
            {"name": "growth", "path": "revenue_growth.start",
             "distribution": {"type": "normal", "mean": 0.20, "sd": 0.0}},
        ]})
    check("a zero-width simulation returns the base case",
          flat["distribution"]["median"], base_value, 1e-12)
    check("a zero-width simulation has no dispersion",
          flat["distribution"]["standard_deviation"], 0.0, 1e-12)
    check("a zero-width simulation refuses nothing", flat["refused"], 0)
    check("base case value is reported", flat["base_case_value"], base_value, 1e-12)

    # ---- 7. Reproducibility -------------------------------------------------------------
    spec = copy.deepcopy(EXAMPLES["simulate"])
    spec["trials"] = 400
    run_a = simulate(copy.deepcopy(spec))
    run_b = simulate(copy.deepcopy(spec))
    check("the same seed reproduces the median exactly",
          run_b["distribution"]["median"], run_a["distribution"]["median"], 0.0)
    check("the same seed reproduces the 95th percentile exactly",
          run_b["distribution"]["percentiles"]["95"],
          run_a["distribution"]["percentiles"]["95"], 0.0)
    other = copy.deepcopy(spec)
    other["seed"] = spec["seed"] + 1
    run_c = simulate(other)
    check_true("a different seed gives a different run",
               run_c["distribution"]["median"] != run_a["distribution"]["median"])
    check_true("percentiles are ordered",
               all(run_a["distribution"]["percentiles"][str(lo)]
                   <= run_a["distribution"]["percentiles"][str(hi)]
                   for lo, hi in zip(REPORTED_PERCENTILES[:-1], REPORTED_PERCENTILES[1:])))

    # ---- 8. Correlation widens the tails ------------------------------------------------
    # The honest claim in the documentation, tested: sampling correlated drivers as if they
    # were independent understates the spread. Both drivers raise value, so loading them on
    # one factor must widen the 5th-to-95th range.
    wide_spec = {
        "seed": 4242, "trials": 3000, "base_case": _BASE,
        "drivers": [
            {"name": "growth", "path": "revenue_growth.start",
             "distribution": {"type": "normal", "mean": 0.20, "sd": 0.05},
             "factor": "demand", "loading": 0.9},
            {"name": "margin", "path": "operating_margin.end",
             "distribution": {"type": "normal", "mean": 0.14, "sd": 0.02},
             "factor": "demand", "loading": 0.9},
        ]}
    independent_spec = copy.deepcopy(wide_spec)
    for d in independent_spec["drivers"]:
        d["loading"] = 0.0
    corr_run = simulate(copy.deepcopy(wide_spec))
    ind_run = simulate(independent_spec)

    def spread(run):
        pc = run["distribution"]["percentiles"]
        return pc["95"] - pc["5"]

    check_true("independent sampling of correlated drivers understates the spread",
               spread(corr_run) > spread(ind_run) * 1.1,
               {"correlated": spread(corr_run), "independent": spread(ind_run)})
    check_true("independent sampling warns about it",
               any("independently" in w for w in ind_run.get("warnings", [])))

    # ---- 9. Infeasible draws are counted, not swallowed ---------------------------------
    # Terminal growth drawn above the terminal cost of capital describes a company that
    # grows faster than its discount rate forever. The engine refuses; the share of
    # refusals is the output.
    refusing = simulate({
        "seed": 5, "trials": 500, "base_case": _BASE,
        "drivers": [{"name": "terminal growth", "path": "terminal.growth_rate",
                     "distribution": {"type": "uniform", "min": 0.00, "max": 0.12}}]})
    check_true("infeasible draws are refused and counted", refusing["refused"] > 0)
    check("completed plus refused equals trials",
          refusing["completed"] + refusing["refused"], refusing["trials"])
    check_true("the refusal reason is reported",
               any("terminal" in r["reason"].lower() for r in refusing["refusals"]))
    check_true("a heavy refusal share is warned about",
               any("infeasible" in w for w in refusing.get("warnings", [])))
    # Roughly a third of a uniform 0% to 12% draw sits above the 8% terminal cost of
    # capital, and the reinvestment ceiling refuses more of what is left.
    check_between("refused share is plausible for these bounds",
                  refusing["refused_share"], 0.25, 0.75)

    # ---- 10. Price statistics --------------------------------------------------------
    priced = simulate({
        "seed": 8, "trials": 1500, "base_case": _BASE, "current_price": 14.0,
        "drivers": [{"name": "margin", "path": "operating_margin.end",
                     "distribution": {"type": "triangular", "min": 0.08,
                                      "likeliest": 0.14, "max": 0.20}}]})
    vp = priced["distribution"]["versus_price"]
    check("probability above price and percentile of price are complements",
          vp["probability_value_exceeds_price"] + vp["percentile_of_price"] / 100.0, 1.0,
          1e-12)
    check_between("probability the value exceeds the price is a probability",
                  vp["probability_value_exceeds_price"], 0.0, 1.0)

    # ---- 11. The linear map, against Shell's fitted revenue line -----------------------
    # Damodaran's Shell regression: revenues = 39,992.77 + 4,039.40 x oil price, R-squared
    # 96.44% over 1989-2015. At the March 2016 spot price of $40 that is $201,569m.
    shell = cases["shell_2016"]
    fit = shell["revenue_regression"]
    mapped = simulate({
        "seed": 3, "trials": 50, "base_case": _BASE,
        "drivers": [{"name": "oil price", "path": "base_revenue",
                     "distribution": {"type": "uniform",
                                      "min": fit["oil_price_used"],
                                      "max": fit["oil_price_used"]},
                     "linear_map": {"intercept": fit["intercept"],
                                    "slope": fit["slope"]}}]})
    check("Shell's fitted revenue at the price used in the source",
          mapped["drivers"][0]["realized_p50"], fit["revenue_at_price_used"], 1e-9)
    check("Shell's fitted revenue matches the published rounding",
          round(mapped["drivers"][0]["realized_p50"]), 201569, 1e-9)
    # Inverting the map has to hand back the price that was drawn.
    check("the raw draw is recoverable from the mapped value",
          mapped["drivers"][0]["before_map"]["p50"], fit["oil_price_used"], 1e-9)
    check_true("a linear_map slope of zero is refused",
               refuses(simulate, {"seed": 1, "base_case": _BASE, "drivers": [
                   {"name": "oil", "path": "base_revenue",
                    "distribution": {"type": "uniform", "min": 30.0, "max": 50.0},
                    "linear_map": {"intercept": 39992.77, "slope": 0.0}}]}))

    # ---- 12. Locating a market price in a published percentile table -------------------
    # The S&P 500 on 1 November 2020 traded at 3,270 against Damodaran's simulated index
    # distribution. The source says it sat between the 70th and 80th percentiles.
    sp = cases["sp500_2020"]
    located = percentiles({"percentile_table": sp["percentile_table"],
                           "current_price": sp["market_price"]})["versus_price"]
    check_between("the S&P 500 price sits between the 70th and 80th percentiles",
                  located["percentile_of_price"], 70.0, 80.0)
    check("the interpolated percentile is exact",
          located["percentile_of_price"],
          70.0 + 10.0 * (3270.0 - 3217.16) / (3299.18 - 3217.16), 1e-9)

    # Amazon, September 2018: a $1,970 price against a simulated distribution whose median
    # was $1,241.97. The source places the price around the 85th to 90th percentile.
    amzn = cases["amazon_2018"]
    amzn_loc = percentiles({"percentile_table": amzn["percentile_table"],
                            "current_price": amzn["market_price"]})["versus_price"]
    check_between("the Amazon price sits in the top fifth of the distribution",
                  amzn_loc["percentile_of_price"], 80.0, 90.0)
    check("probability the value exceeds the Amazon price",
          amzn_loc["probability_value_exceeds_price"],
          1.0 - amzn_loc["percentile_of_price"] / 100.0, 1e-12)
    # The published mean sits above the published median, which is what a right-skewed
    # input distribution does to the output.
    check_true("Amazon's simulated mean exceeds its median",
               amzn["simulated_mean"] > amzn["simulated_median"])

    # Paytm, September 2021: the simulated median came in below the base-case DCF, which is
    # the finding the source draws out. A simulation median is not the base case.
    paytm = cases["paytm_2021"]
    paytm_table = percentiles({"percentile_table": paytm["percentile_table"]})["table"]
    median_row = [r for r in paytm_table if r["percentile"] == 50][0]
    check_true("Paytm's simulated median is below its base case",
               median_row["value"] < paytm["base_case_value"])
    check("Paytm's simulated median matches the source", median_row["value"],
          1246824.0, 1e-9)

    # ---- 13. Discrete scenarios ---------------------------------------------------------
    sc = scenarios(copy.deepcopy(EXAMPLES["scenarios"]))
    manual = sum(r["probability"] * r["value"] for r in sc["scenarios"])
    check("expected value is the probability weighting of the scenarios",
          sc["expected_value"], manual, 1e-12)
    check_true("scenarios are ordered by value",
               all(sc["scenarios"][i]["value"] >= sc["scenarios"][i + 1]["value"]
                   for i in range(len(sc["scenarios"]) - 1)))
    bad_scenarios = copy.deepcopy(EXAMPLES["scenarios"])
    bad_scenarios["scenarios"][0]["probability"] = 0.9
    try:
        scenarios(bad_scenarios)
        refused_sum = False
    except SystemExit:
        refused_sum = True
    check_true("scenario probabilities that do not sum to 1 are refused", refused_sum)

    # ---- 14. Bad input is explained, not crashed ----------------------------------------
    check_true("a missing seed is refused with an explanation",
               refuses(simulate, {"base_case": _BASE, "drivers": [
                   {"name": "m", "path": "operating_margin.end",
                    "distribution": {"type": "uniform", "min": 0.1, "max": 0.2}}]}))
    check_true("an unknown distribution type is refused",
               refuses(simulate, {"seed": 1, "base_case": _BASE, "drivers": [
                   {"name": "m", "path": "operating_margin.end",
                    "distribution": {"type": "beta", "a": 2, "b": 5}}]}))
    check_true("a loading outside -1 to 1 is refused",
               refuses(simulate, {"seed": 1, "base_case": _BASE, "drivers": [
                   {"name": "m", "path": "operating_margin.end", "loading": 1.4,
                    "distribution": {"type": "uniform", "min": 0.1, "max": 0.2}}]}))
    check_true("a path that does not exist in the base case is refused",
               refuses(simulate, {"seed": 1, "base_case": _BASE, "drivers": [
                   {"name": "m", "path": "nonexistent.field",
                    "distribution": {"type": "uniform", "min": 0.1, "max": 0.2}}]}))
    check_true("a path pointing at an object rather than a number is refused",
               refuses(simulate, {"seed": 1, "base_case": _BASE, "drivers": [
                   {"name": "m", "path": "operating_margin",
                    "distribution": {"type": "uniform", "min": 0.1, "max": 0.2}}]}))
    check_true("discrete probabilities that do not sum to 1 are refused",
               refuses(simulate, {"seed": 1, "base_case": _BASE, "drivers": [
                   {"name": "m", "path": "operating_margin.end",
                    "distribution": {"type": "discrete", "outcomes": [
                        {"value": 0.1, "probability": 0.4},
                        {"value": 0.2, "probability": 0.4}]}}]}))
    check_true("a triangular whose likeliest sits outside its range is refused",
               refuses(simulate, {"seed": 1, "base_case": _BASE, "drivers": [
                   {"name": "m", "path": "operating_margin.end",
                    "distribution": {"type": "triangular", "min": 0.1,
                                     "likeliest": 0.25, "max": 0.2}}]}))
    infeasible_base = copy.deepcopy(_BASE)
    infeasible_base["terminal"] = {"growth_rate": 0.09, "cost_of_capital": 0.08,
                                   "return_on_capital": 0.12}
    check_true("an infeasible base case is refused before sampling",
               refuses(simulate, {"seed": 1, "base_case": infeasible_base, "drivers": [
                   {"name": "m", "path": "operating_margin.end",
                    "distribution": {"type": "uniform", "min": 0.1, "max": 0.2}}]}))
    check_true("an output field the engine does not return is refused",
               refuses(simulate, {"seed": 1, "base_case": _BASE, "output": "ebitda",
                                  "drivers": [
                                      {"name": "m", "path": "operating_margin.end",
                                       "distribution": {"type": "uniform", "min": 0.1,
                                                        "max": 0.2}}]}))
    check_true("a percentiles payload with neither input is refused",
               refuses(percentiles, {"current_price": 10.0}))

    failed = [x for x in results if not x["pass"]]
    _emit({"total": len(results), "passed": len(results) - len(failed),
           "failed": len(failed), "results": results})
    return 1 if failed else 0


COMMANDS = {
    "simulate": cmd_simulate, "sample": cmd_sample, "scenarios": cmd_scenarios,
    "percentiles": cmd_percentiles, "selftest": cmd_selftest,
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
            raise SystemExit("No example payload for %s; it takes no input." % args.command)
        _emit(EXAMPLES[args.command])
        return 0
    return COMMANDS[args.command](args) or 0


if __name__ == "__main__":
    sys.exit(main())

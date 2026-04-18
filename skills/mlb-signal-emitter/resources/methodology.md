# Signal Validation Methodology

This document specifies the exact rules the `mlb-signal-emitter` skill applies to every signal file before persisting it. These rules are the operational expression of `~/Documents/Projects/yahoo-mlb/context/frameworks/signal-framework.md`.

## Table of Contents
- [Required Frontmatter Fields](#required-frontmatter-fields)
- [Range Check Rules](#range-check-rules)
- [Variant Synthesis Rules](#variant-synthesis-rules)
- [File Path Conventions](#file-path-conventions)
- [Source URL Rules](#source-url-rules)
- [Handling Validation Failures](#handling-validation-failures)
- [Full Validation Pseudocode](#full-validation-pseudocode)

---

## Required Frontmatter Fields

Every signal file MUST carry the following YAML frontmatter keys. Missing any of these is an immediate validation failure.

| Field | Type | Constraint |
|---|---|---|
| `type` | string (enum) | Exactly one of: `lineup`, `waivers`, `streaming`, `trade`, `category-plan`, `playoff-push`, `player`, `matchup`, `regression`, `two-start`, `closer`, `faab`, `cat-state` |
| `date` | string | Parses as `YYYY-MM-DD` (ISO local date) |
| `emitted_by` | string | Non-empty; names the skill or agent that produced the signal. Intermediate variants append `/advocate` or `/critic` |
| `confidence` | float | `0.0 <= x <= 1.0`. Missing field is a failure. Value outside range is a failure. |
| `source_urls` | list of strings | Non-empty. Each entry must parse as a URL (scheme + host). An empty list is a failure. |

### Conditional requirements

The following are required only when the signal is a synthesized (final) signal:

| Condition | Additional required fields |
|---|---|
| `variant_synthesis: true` | `variants_fired` (list, length >= 1), `synthesis_confidence` (float in [0.0, 1.0]) |
| `variant_synthesis: false` | None additional; however, the filename MUST include a variant suffix (e.g., `-advocate` or `-critic`) |
| `variant_synthesis` absent | Treated as `false` -- intermediate variant dump -- filename must carry a variant suffix |

### Type validation details

- `type` comparison is case-sensitive. `Player`, `PLAYER`, `player_analyzer` are all rejected.
- If a new signal type needs to be introduced, the process is: (1) update `context/frameworks/signal-framework.md`, (2) update the enum in this document and in SKILL.md, (3) then start emitting.

---

## Range Check Rules

Every numeric signal in the body must fall inside its declared range. The skill parses the body (markdown) for `signal_name: value` entries or `| signal_name | value |` table cells and checks each against the table below. Values outside the declared range are a hard failure -- the skill does NOT clamp.

### Unipolar signals (0-100)

A score of 50 is "neutral / league average."

| Signal | Range | Emitted by |
|---|---|---|
| `form_score` | 0-100 | mlb-player-analyzer |
| `matchup_score` | 0-100 | mlb-player-analyzer |
| `opportunity_score` | 0-100 | mlb-player-analyzer |
| `daily_quality` | 0-100 | mlb-player-analyzer |
| `obp_contribution` | 0-100 | mlb-player-analyzer |
| `sb_opportunity` | 0-100 | mlb-player-analyzer |
| `role_certainty` | 0-100 | mlb-player-analyzer, mlb-waiver-analyst |
| `qs_probability` | 0-100 | mlb-player-analyzer (pitchers) |
| `k_ceiling` | 0-100 | mlb-player-analyzer (pitchers) |
| `era_whip_risk` | 0-100 | mlb-player-analyzer (pitchers) |
| `streamability_score` | 0-100 | mlb-streaming-strategist |
| `save_role_certainty` | 0-100 | mlb-closer-tracker |
| `cat_pressure` | 0-100 | mlb-category-state-analyzer |
| `cat_reachability` | 0-100 | mlb-category-state-analyzer |
| `cat_punt_score` | 0-100 | mlb-category-state-analyzer |
| `positional_need_fit` | 0-100 | mlb-waiver-analyst |
| `opp_sp_quality` | 0-100 | mlb-matchup-analyzer |
| `park_hitter_factor` | 0-100 | mlb-matchup-analyzer |
| `park_pitcher_factor` | 0-100 | mlb-matchup-analyzer |
| `weather_risk` | 0-100 | mlb-matchup-analyzer |
| `bullpen_state` | 0-100 | mlb-matchup-analyzer |
| `playoff_matchup_quality` | 0-100 | mlb-playoff-planner |
| `holding_value` | 0-100 | mlb-playoff-planner |
| `playoff_impact` | 0-100 | mlb-trade-evaluator |

### Bipolar signals (-100 to +100)

A score of 0 is neutral.

| Signal | Range | Emitted by |
|---|---|---|
| `regression_index` | -100 to +100 | mlb-regression-flagger |
| `positional_flex_delta` | -100 to +100 | mlb-trade-evaluator |

### Dollar signals (>= 0)

Expressed in whole dollars.

| Signal | Range | Emitted by |
|---|---|---|
| `acquisition_value` | >= 0 | mlb-faab-sizer |
| `faab_max_bid` | >= 0 | mlb-faab-sizer |
| `faab_rec_bid` | >= 0 | mlb-faab-sizer |
| `trade_value_delta` | any integer (can be negative) | mlb-trade-evaluator |

Additional constraint: `faab_rec_bid <= faab_max_bid`.

### Integer signals (>= 0)

| Signal | Range | Emitted by |
|---|---|---|
| `playoff_games` | >= 0, typically 0-21 | mlb-playoff-planner |

### Boolean signals

| Signal | Allowed | Emitted by |
|---|---|---|
| `two_start_bonus` | `true` or `false` | mlb-two-start-scout |

### Enum signals

| Signal | Allowed values | Emitted by |
|---|---|---|
| `cat_position` | `winning`, `tied`, `losing` | mlb-category-state-analyzer |
| `verdict` | `accept`, `counter`, `reject` | mlb-trade-evaluator |

### Composite signals

| Signal | Structure | Constraint |
|---|---|---|
| `trade_cat_delta` | Map of 10 categories -> integer | Each of the 10 cats must be present; each value can be negative |

---

## Variant Synthesis Rules

Per CLAUDE.md rule 3 ("Run both variants, every time"), every user-facing decision is backed by a synthesized signal. Synthesis metadata must tell an honest story about what fired.

### Rule set

1. **If `variant_synthesis: true`:**
   - `variants_fired` MUST be a list with length >= 1. Empty list is a failure.
   - `variants_fired` entries should name the variants from `context/frameworks/variant-catalog.md` (typically `advocate`, `critic`).
   - `synthesis_confidence` MUST be present and in `[0.0, 1.0]`.
   - The body SHOULD include a "variant summary" section naming each variant's position and the synthesis reasoning.

2. **If `variant_synthesis: false` or absent:**
   - The file is treated as an intermediate variant dump.
   - The filename MUST include a variant suffix: `YYYY-MM-DD-<type>-<variant>.md` where `<variant>` is one of the variants from the catalog.
   - `emitted_by` SHOULD use the `<agent>/<variant>` form (e.g., `mlb-lineup-optimizer/advocate`).

3. **If `variant_synthesis: true` but `variants_fired: []`:**
   - Hard failure. A synthesis with zero variants is a lie about process.

4. **`red_team_findings` structure (when present):**
   - List of objects, each with: `severity` (int 1-5), `likelihood` (int 1-5), `score` (product; redundant but kept for readability), `note` (string), `mitigation` (string).
   - Missing any of these inner fields on any entry is a failure.

---

## File Path Conventions

The canonical signals directory is `~/Documents/Projects/yahoo-mlb/signals/`.

### Naming rules

| Signal kind | Path pattern | Example |
|---|---|---|
| Final synthesized signal | `signals/YYYY-MM-DD-<type>.md` | `signals/2026-04-17-lineup.md` |
| Final synthesized with identifier | `signals/YYYY-MM-DD-<type>-<id>.md` | `signals/2026-04-17-player-caminero.md` |
| Intermediate variant dump | `signals/YYYY-MM-DD-<type>-<variant>.md` | `signals/2026-04-17-lineup-advocate.md` |

### Identifier rules

- `<id>` (player key, matchup key, waiver target, etc.): lowercase, kebab-case, ASCII. Derived from last name for players (`caminero`), from team abbreviations for matchups (`tb-bos`).
- `<variant>`: one of the values listed in `context/frameworks/variant-catalog.md`. Most commonly `advocate` or `critic`.

### Path validation

1. The skill computes the path from frontmatter `date` + `type` (+ optional identifier the caller passes).
2. Rejects paths that do not start with the resolved `~/Documents/Projects/yahoo-mlb/signals/` prefix (prevents directory-escape bugs).
3. Ensures the `signals/` directory exists; creates it if missing.
4. If the target path already exists:
   - Default: refuse to overwrite. Log a failure with reason `target exists, overwrite not requested`.
   - If the caller passed `overwrite: true`: proceed.

### Date consistency

The `date` in frontmatter MUST match the date in the filename. A file called `2026-04-17-lineup.md` with frontmatter `date: 2026-04-16` is a failure.

---

## Source URL Rules

Per CLAUDE.md rule 1 ("Web-search everything"), every signal must carry grounding URLs.

1. `source_urls` is a required list.
2. The list must have at least one entry.
3. Each entry must parse as a URL: must contain a scheme (`http://` or `https://`) and a host.
4. Empty strings inside the list are a failure.
5. `source_urls` is NOT range-checked or domain-whitelisted -- the validator does not judge which sources are "good." That is the job of the upstream skill and the red-team pass.

Note: `confidence: low` signals are legitimate when a web search fails. The skill does NOT reject low-confidence signals. It DOES reject signals with zero source URLs.

---

## Handling Validation Failures

When any check fails, the skill performs these steps in order:

1. **Do NOT write the signal file.** The file system must never contain a signal that failed validation.
2. **Build a structured failure entry:**
   ```yaml
   kind: signal_validation_failure
   timestamp: <ISO 8601 UTC>
   emitter: <value of emitted_by, or "unknown" if missing>
   signal_type: <value of type, or "unknown">
   attempted_path: <computed path>
   reason: <short machine-readable reason code>
   field: <field that failed, if applicable>
   expected: <what the validator wanted>
   actual: <what it got>
   caller_context: <any extra info the caller passed>
   ```
3. **Call `mlb-decision-logger`** with the failure entry. This appends a structured section to `~/Documents/Projects/yahoo-mlb/tracker/decisions-log.md`. The decisions log is append-only per CLAUDE.md rule 4.
4. **Return an error object to the caller** so the upstream skill/agent knows the emission failed. Shape:
   ```yaml
   status: error
   code: <reason code>
   message: <human-readable message>
   failed_field: <field>
   logged_to: tracker/decisions-log.md
   ```

### Reason codes

| Code | Meaning |
|---|---|
| `missing_required_field` | A required frontmatter field is absent |
| `invalid_type_enum` | `type` is not one of the 13 allowed values |
| `invalid_date_format` | `date` does not parse as `YYYY-MM-DD` |
| `confidence_out_of_range` | `confidence` is not in `[0.0, 1.0]` |
| `empty_source_urls` | `source_urls` is empty or missing |
| `malformed_url` | A URL in `source_urls` does not parse |
| `signal_value_out_of_range` | A numeric signal in the body is outside its declared range |
| `unknown_signal_name` | The body contains a signal whose name is not in the catalog |
| `variants_fired_empty` | `variant_synthesis: true` but `variants_fired` is empty |
| `synthesis_confidence_missing` | `variant_synthesis: true` but `synthesis_confidence` absent |
| `variant_filename_missing` | `variant_synthesis: false` but filename lacks variant suffix |
| `date_filename_mismatch` | Frontmatter `date` differs from filename date |
| `target_exists_no_overwrite` | File already exists and `overwrite: true` was not passed |
| `path_escape` | Computed path escapes the `signals/` directory |
| `faab_bid_ordering` | `faab_rec_bid > faab_max_bid` |
| `red_team_finding_incomplete` | A `red_team_findings` entry is missing one of `severity`/`likelihood`/`score`/`note`/`mitigation` |

---

## Full Validation Pseudocode

```
function emit_signal(frontmatter, body, overwrite=false):
    # --- Phase 1: frontmatter presence + types ---
    for field in [type, date, emitted_by, confidence, source_urls]:
        if field missing from frontmatter:
            return fail("missing_required_field", field=field)

    if frontmatter.type not in TYPE_ENUM:
        return fail("invalid_type_enum", actual=frontmatter.type)

    if not matches_yyyy_mm_dd(frontmatter.date):
        return fail("invalid_date_format", actual=frontmatter.date)

    if not (0.0 <= frontmatter.confidence <= 1.0):
        return fail("confidence_out_of_range", actual=frontmatter.confidence)

    if len(frontmatter.source_urls) == 0:
        return fail("empty_source_urls")

    for url in frontmatter.source_urls:
        if not parses_as_url(url):
            return fail("malformed_url", actual=url)

    # --- Phase 2: variant synthesis ---
    vs = frontmatter.get("variant_synthesis", false)
    if vs == true:
        if "variants_fired" not in frontmatter or len(frontmatter.variants_fired) < 1:
            return fail("variants_fired_empty")
        if "synthesis_confidence" not in frontmatter:
            return fail("synthesis_confidence_missing")
        if not (0.0 <= frontmatter.synthesis_confidence <= 1.0):
            return fail("confidence_out_of_range", field="synthesis_confidence")

    # --- Phase 3: red-team findings shape ---
    for finding in frontmatter.get("red_team_findings", []):
        for k in [severity, likelihood, score, note, mitigation]:
            if k not in finding:
                return fail("red_team_finding_incomplete", field=k)

    # --- Phase 4: body signal ranges ---
    for (name, value) in parse_signals_from_body(body):
        if name not in SIGNAL_RANGE_TABLE:
            return fail("unknown_signal_name", actual=name)
        if not SIGNAL_RANGE_TABLE[name].contains(value):
            return fail("signal_value_out_of_range", field=name, actual=value,
                        expected=SIGNAL_RANGE_TABLE[name])

    # Extra: FAAB bid ordering
    if has(faab_rec_bid) and has(faab_max_bid):
        if faab_rec_bid > faab_max_bid:
            return fail("faab_bid_ordering")

    # --- Phase 5: filename + path ---
    path = compute_path(frontmatter.date, frontmatter.type, caller_identifier, vs, caller_variant)
    if not path.startswith(SIGNALS_DIR):
        return fail("path_escape", actual=path)

    if date_in_filename(path) != frontmatter.date:
        return fail("date_filename_mismatch")

    if vs == false and not filename_has_variant_suffix(path):
        return fail("variant_filename_missing")

    if file_exists(path) and not overwrite:
        return fail("target_exists_no_overwrite", actual=path)

    # --- Phase 6: write ---
    ensure_dir(SIGNALS_DIR)
    write_file(path, rebuild_markdown(frontmatter, body))
    return success(path)


function fail(code, field=null, actual=null, expected=null):
    entry = build_failure_entry(code, field, actual, expected, caller_context)
    call mlb_decision_logger(entry)   # appends to tracker/decisions-log.md
    return {status: "error", code: code, logged_to: "tracker/decisions-log.md"}
```

Every skill that emits a signal calls this function. No skill writes directly to `signals/`.

#!/usr/bin/env python3
"""Validate a narrative architecture against the handoff contract.

The contract exists because a two-agent pipeline whose interface is prose has no
interface at all. This script is the mechanism behind three rules that are otherwise
just good intentions:

  1. The evidence array, not the value, is the validated field. A slot carrying a
     confident sentence and no claim ID fails here rather than reading well downstream.
  2. ABSENT is a passing state. An architecture with every slot filled is flagged,
     because real material always has holes.
  3. The macro layer must not draft. A length cap on scene lines enforces that
     mechanically; a prose prohibition in a system prompt decays as context fills.

Usage:
    python3 validate_architecture.py ARCHITECTURE_JSON [--corpus-root DIR]
                                     [--output-root DIR] [--strict]

Exit codes:
    0  contract satisfied (warnings may still be printed)
    1  contract violated
    2  file missing, unreadable, or not valid JSON

--strict promotes warnings to errors. Use it in CI; leave it off while drafting.
"""

import argparse
import json
import os
import re
import sys

# --- Tunable limits -----------------------------------------------------------------
# Each has a stated reason. None of these is a magic number.

# A scene line is a tag, not a draft. 200 characters is roughly two sentences of
# summary — enough to identify the beat and its construction, too short to be prose.
MAX_TAGGED_LINE_CHARS = 200

# Truby licenses fewer than 22 steps and treats only seven as mandatory. An
# architecture in which nothing is ABSENT has almost certainly been slot-filled.
MIN_ABSENT_SLOTS = 1

# A designing principle that excludes nothing organises nothing. Three is the
# smallest number that demonstrates the principle is actually cutting.
MIN_CLAIMS_EXCLUDED = 3

# At most one slot may be filled by inference, and never the climax. More than one
# and the architecture is carrying the argument rather than the evidence.
MAX_INFERRED_SLOTS = 1

VALID_STATUS = {"FILLED", "ABSENT", "INFERRED"}
VALID_TIERS = {"L1", "L2", "L3", "L4", "L5"}
VALID_DISPOSITIONS = {"RESEARCH", "REDESIGN", "DECLARE", "CUT"}
VALID_DEAD_REASONS = {"did_not_support", "CONTRADICTED"}
VALID_REPRESENTATIVENESS = {"median", "tail", "unique"}
VALID_PROTAGONIST_TYPES = {"person", "composite", "system"}
LOAD_BEARING = {"opener", "climax", "closer"}

# Verbs each causal tier licenses. L1 is the only tier permitted to assert causation.
TIER_BANNED_VERBS = {
    "L2": r"\b(because|drove|forced|caused|triggered|led to|resulted in)\b",
    "L3": r"\b(because|drove|forced|caused|triggered|led to|resulted in|coincided with)\b",
    "L4": r"\b(because|drove|forced|caused|triggered|led to|resulted in)\b",
    "L5": r"\b(because|drove|forced|caused|triggered|led to|resulted in)\b",
}

SUPPORTED_CONTRACT_VERSIONS = {"1.0"}


class Report:
    """Collects findings so the caller sees every problem, not just the first."""

    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, message):
        self.errors.append((where, message))

    def warn(self, where, message):
        self.warnings.append((where, message))

    def emit(self, strict):
        for where, message in self.errors:
            print(f"ERROR  {where}: {message}")
        for where, message in self.warnings:
            label = "ERROR " if strict else "WARN  "
            print(f"{label} {where}: {message}")
        failed = bool(self.errors) or (strict and bool(self.warnings))
        counts = f"{len(self.errors)} error(s), {len(self.warnings)} warning(s)"
        print(f"\n{'REFUSED' if failed else 'CONTRACT SATISFIED'} — {counts}")
        return 1 if failed else 0


def require(report, obj, key, where):
    """Return obj[key], recording an error when it is missing or empty."""
    value = obj.get(key)
    if value is None or value == "" or value == []:
        report.error(where, f"required field '{key}' is missing or empty")
        return None
    return value


def check_header(doc, report):
    version = doc.get("contract_version")
    if version not in SUPPORTED_CONTRACT_VERSIONS:
        report.error(
            "contract_version",
            f"got {version!r}, expected one of {sorted(SUPPORTED_CONTRACT_VERSIONS)}",
        )

    header = doc.get("run_header") or {}
    if not header:
        report.error("run_header", "missing — a run with no provenance cannot be reproduced")
        return
    for key in ("model", "corpus_ref", "timestamp", "claim_ids_consulted"):
        require(report, header, key, "run_header")

    consulted = header.get("claim_ids_consulted")
    if isinstance(consulted, list) and not consulted:
        report.error(
            "run_header.claim_ids_consulted",
            "empty — an architecture built from no claims is not an architecture",
        )


def check_frame_and_principle(doc, report):
    frame = doc.get("frame_lock") or {}
    for key in ("unit", "denominator", "window", "population"):
        require(report, frame, key, "frame_lock")
    rejected = frame.get("rejected_alternatives") or []
    if not rejected:
        report.warn(
            "frame_lock.rejected_alternatives",
            "empty — a frame chosen without a named alternative was not chosen, it was assumed",
        )

    principle = doc.get("designing_principle") or {}
    require(report, principle, "statement", "designing_principle")
    excluded = principle.get("claims_excluded") or []
    if len(excluded) < MIN_CLAIMS_EXCLUDED:
        report.error(
            "designing_principle.claims_excluded",
            f"{len(excluded)} claim(s) excluded, need at least {MIN_CLAIMS_EXCLUDED}. "
            "A principle that excludes nothing organises nothing.",
        )


def check_protagonist(doc, report):
    prot = doc.get("protagonist") or {}
    ptype = prot.get("type")
    if ptype not in VALID_PROTAGONIST_TYPES:
        report.error("protagonist.type", f"got {ptype!r}, expected one of {sorted(VALID_PROTAGONIST_TYPES)}")
    if ptype != "system":
        return

    # A system protagonist carries extra obligations, because the character is inferred
    # from behaviour rather than stated by a person.
    for key in ("stated_purpose", "revealed_function", "gap"):
        require(report, prot, key, "protagonist")

    regimes = prot.get("regimes_evidenced") or []
    if len(regimes) < 2:
        report.error(
            "protagonist.regimes_evidenced",
            f"{len(regimes)} regime(s). A revealed objective function derived from one "
            "episode is a description of that episode dressed as a character trait.",
        )

    unexplained = prot.get("outcomes_unexplained") or []
    if not unexplained:
        report.error(
            "protagonist.outcomes_unexplained",
            "empty — every inferred objective function fails to explain something, and "
            "that list must reach the reader",
        )


def check_slots(doc, report):
    slots = doc.get("slots") or []
    if not slots:
        report.error("slots", "empty — there is no architecture here")
        return

    absent = inferred = 0
    seen_ids = set()

    for slot in slots:
        sid = slot.get("id", "<no id>")
        where = f"slot[{sid}]"

        if sid in seen_ids:
            report.error(where, "duplicate slot id")
        seen_ids.add(sid)

        status = slot.get("status")
        if status not in VALID_STATUS:
            report.error(where, f"status {status!r} not one of {sorted(VALID_STATUS)}")
            continue

        if status == "ABSENT":
            absent += 1
            if not slot.get("empty_slot_move"):
                report.error(
                    where,
                    "ABSENT with no empty_slot_move. Choose DECLARE, DOWNGRADE or REDESIGN — "
                    "an unhandled absence becomes an invention downstream.",
                )
            continue

        if status == "INFERRED":
            inferred += 1
            if str(slot.get("name", "")).lower() == "climax":
                report.error(where, "the climax may never be filled by inference")

        # This is the rule the whole contract exists for.
        evidence = slot.get("evidence") or []
        if not evidence:
            report.error(
                where,
                f"status {status} with no evidence[]. The evidence array is the validated "
                "field, not the value. A confident sentence with no claim ID is not a slot.",
            )

        tier = slot.get("causal_tier")
        if tier is not None and tier not in VALID_TIERS:
            report.error(where, f"causal_tier {tier!r} not one of {sorted(VALID_TIERS)}")
        elif tier in TIER_BANNED_VERBS:
            warrant = str(slot.get("warrant") or "")
            hit = re.search(TIER_BANNED_VERBS[tier], warrant, re.IGNORECASE)
            if hit:
                report.error(
                    where,
                    f"tier {tier} warrant uses causal verb '{hit.group(0)}'. Only L1 "
                    "(documented mechanism) may assert causation.",
                )

    if absent < MIN_ABSENT_SLOTS:
        report.warn(
            "slots",
            f"{absent} slot(s) ABSENT. Every slot filled is a defect, not a triumph — "
            "real material always has holes.",
        )
    if inferred > MAX_INFERRED_SLOTS:
        report.error(
            "slots",
            f"{inferred} slots filled by inference, budget is {MAX_INFERRED_SLOTS}",
        )


def check_scenes(doc, report):
    slot_ids = {s.get("id") for s in (doc.get("slots") or [])}
    for scene in doc.get("scenes") or []:
        sid = scene.get("id", "<no id>")
        where = f"scene[{sid}]"

        if scene.get("slot_id") not in slot_ids:
            report.error(where, f"slot_id {scene.get('slot_id')!r} does not match any slot")

        line = str(scene.get("tagged_line") or "")
        if not line:
            report.error(where, "tagged_line is empty")
        elif len(line) > MAX_TAGGED_LINE_CHARS:
            report.error(
                where,
                f"tagged_line is {len(line)} chars, cap is {MAX_TAGGED_LINE_CHARS}. "
                "The macro layer tags scenes; it does not draft them.",
            )

        if not (scene.get("provenance") or []):
            report.error(where, "no provenance[] — every scene traces to claims or it is invented")

        rep = scene.get("representativeness")
        position = str(scene.get("position") or "").lower()
        if rep is not None and rep not in VALID_REPRESENTATIVENESS:
            report.error(where, f"representativeness {rep!r} not one of {sorted(VALID_REPRESENTATIVENESS)}")
        if position in LOAD_BEARING and not rep:
            report.error(
                where,
                f"in load-bearing position '{position}' with no representativeness label. "
                "An unlabelled case in the opener, climax or closer is the anecdote-"
                "distribution failure.",
            )


def check_gaps_and_dead(doc, report):
    for gap in doc.get("gaps") or []:
        disposition = gap.get("disposition")
        if disposition not in VALID_DISPOSITIONS:
            report.error(
                f"gap[{gap.get('slot_id', '?')}]",
                f"disposition {disposition!r} not one of {sorted(VALID_DISPOSITIONS)}. "
                "'draft and flag' is not a disposition — flagged prose survives review.",
            )

    dead = doc.get("dead_column")
    if dead is None:
        report.error(
            "dead_column",
            "missing. Killed findings are kept, never deleted — this is the record of "
            "what the story is not, and the only defence against a cherry-picking claim.",
        )
        return
    for entry in dead:
        reason = entry.get("reason")
        if reason not in VALID_DEAD_REASONS:
            report.error(
                f"dead_column[{entry.get('claim_id', '?')}]",
                f"reason {reason!r} not one of {sorted(VALID_DEAD_REASONS)}",
            )


def check_circular_citation(doc, report, corpus_root, output_root):
    """A pointer resolving into the pipeline's own outputs is a hard failure.

    Agent A summarises, agent B structures from the summary, agent C cites A's summary
    as a source. Every claim has a pointer, nothing has a source, and no single agent
    did anything wrong. This is invisible to reading, so it must be checked here.
    """
    if not output_root:
        return
    output_root = os.path.abspath(output_root)

    def flag(where, pointer):
        resolved = os.path.abspath(os.path.join(corpus_root or ".", str(pointer)))
        if resolved.startswith(output_root + os.sep):
            report.error(
                where,
                f"provenance pointer {pointer!r} resolves inside the pipeline's own output "
                "directory. Pointers must resolve to external artifacts.",
            )

    for slot in doc.get("slots") or []:
        for pointer in slot.get("evidence") or []:
            flag(f"slot[{slot.get('id', '?')}].evidence", pointer)
    for scene in doc.get("scenes") or []:
        for pointer in scene.get("provenance") or []:
            flag(f"scene[{scene.get('id', '?')}].provenance", pointer)


def check_spine_and_diff(doc, report):
    spine = doc.get("spine") or {}
    for key in ("abt", "structure", "spine_version"):
        require(report, spine, key, "spine")
    if not spine.get("runner_up"):
        report.warn(
            "spine.runner_up",
            "no runner-up structure named. A structure chosen without a rejected "
            "alternative was not chosen.",
        )
    if not spine.get("boredom_permitted"):
        report.warn(
            "spine.boredom_permitted",
            "unstated. If you cannot say where this structure lets the reader be bored, "
            "you have not chosen a structure.",
        )

    if not doc.get("hypothesis_diff"):
        report.warn(
            "hypothesis_diff",
            "missing. The diff between the starting hypothesis and the derived spine is "
            "how you show the evidence did its job.",
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("architecture", help="path to architecture.json")
    parser.add_argument("--corpus-root", default=None, help="root that provenance pointers resolve against")
    parser.add_argument("--output-root", default=None, help="pipeline output dir, for the circular-citation check")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = parser.parse_args()

    try:
        with open(args.architecture, "r", encoding="utf-8") as handle:
            doc = json.load(handle)
    except FileNotFoundError:
        print(f"ERROR  {args.architecture}: file not found")
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR  {args.architecture}: not valid JSON — {exc}")
        return 2
    except OSError as exc:
        print(f"ERROR  {args.architecture}: could not be read — {exc}")
        return 2

    if not isinstance(doc, dict):
        print(f"ERROR  {args.architecture}: top level must be an object, got {type(doc).__name__}")
        return 2

    report = Report()
    check_header(doc, report)
    check_frame_and_principle(doc, report)
    check_protagonist(doc, report)
    check_spine_and_diff(doc, report)
    check_slots(doc, report)
    check_scenes(doc, report)
    check_gaps_and_dead(doc, report)
    check_circular_citation(doc, report, args.corpus_root, args.output_root)
    return report.emit(args.strict)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
readability_hook.py — Claude Code hook that scores long prose and reports what to fix.

Handles two hook events from one command; it branches on hook_event_name in the payload:

  Stop          scores Claude's final message when it is long enough to be worth checking
  PostToolUse   scores a document Claude just wrote or edited (Write / Edit matcher)

FAILS OPEN, ALWAYS
  A hook that crashes takes the session with it. Every failure path here exits 0 and stays
  quiet: missing textstat, unreadable file, malformed payload, unexpected exception. The
  worst case is that a check silently does not happen, never that a session breaks.

ADVISORY BY DEFAULT
  Default mode reports through additionalContext, so Claude sees the finding on its next
  turn and can act on it. Blocking mode (exit 2) is opt-in, because a Stop hook that blocks
  on every failing draft can loop: Claude rewrites, the rewrite still fails, the hook blocks
  again. Blocking mode therefore fires at most once per turn, tracked by a marker file.

OFF BY DEFAULT
  This ships wired into the plugin's hooks/hooks.json, so it is registered the moment the
  plugin installs. It does nothing until READABILITY_HOOK_ENABLED is set. Installing a
  plugin should not silently change how someone's sessions behave; enabling is one line.

INSTALL
  See hooks/README.md for both paths: plugin install (already wired) and manual
  settings.json configuration for people not using the plugin.

ENVIRONMENT
  READABILITY_HOOK_ENABLED     1 | true | yes to turn it on    (default: off)
  READABILITY_HOOK_PROFILE     technical | general | public    (default: general)
  READABILITY_HOOK_MIN_WORDS   skip anything shorter           (default: 300)
  READABILITY_HOOK_MODE        advisory | block                (default: advisory)
  READABILITY_HOOK_EXTENSIONS  comma-separated, for PostToolUse (default: .md,.txt,.mdx)
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

# The user asked for a 300-word floor: below that, formulas are unstable and the advice is
# noise. Everything else is a plain default the operator can override.
DEFAULT_MIN_WORDS = 300
DEFAULT_PROFILE = "general"
DEFAULT_EXTENSIONS = ".md,.txt,.mdx"

# How many failing sentences to quote back. More than three buries the signal.
MAX_QUOTED_SENTENCES = 3


def quiet_exit() -> None:
    """Every unexpected path ends here. A hook must not break the session."""
    sys.exit(0)


def load_scorer():
    """Import readability.py as a sibling module. Returns None if unavailable."""
    path = Path(__file__).resolve().parent.parent / "resources" / "readability.py"
    if not path.exists():
        return None
    try:
        spec = importlib.util.spec_from_file_location("_readability", path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        # dataclasses resolves field types through sys.modules[cls.__module__], so the
        # module must be registered before exec_module or the @dataclass calls fail.
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    except SystemExit:
        # readability.py exits 3 when textstat is missing. That is not our problem to
        # report: the operator sees it the first time they run the skill directly.
        return None
    except Exception:
        return None


def already_blocked_this_turn(session_id: str, prompt_id: str) -> bool:
    """Loop guard: blocking mode fires at most once per turn."""
    key = hashlib.sha256(f"{session_id}:{prompt_id}".encode()).hexdigest()[:16]
    marker = Path(tempfile.gettempdir()) / f"readability-hook-{key}"
    if marker.exists():
        return True
    try:
        marker.touch()
    except OSError:
        # If we cannot write the marker we cannot guarantee loop safety, so report that
        # we already blocked and fall through to advisory.
        return True
    return False


def build_report(result, profile: str) -> str:
    lines = [
        f"Readability check ({profile} profile) — this draft does not pass.",
        f"Reads at: {result.consensus_band}. "
        f"Flesch Reading Ease {result.flesch_reading_ease}, "
        f"Flesch-Kincaid {result.flesch_kincaid_grade}, "
        f"Gunning Fog {result.gunning_fog}, "
        f"Dale-Chall {result.dale_chall}"
        + (f", SMOG {result.smog_index}" if result.smog_index is not None else ""),
    ]
    for f in result.failures:
        lines.append(f"  - {f}")
    if result.long_sentences:
        lines.append("Rewrite these sentences first:")
        for o in result.long_sentences[:MAX_QUOTED_SENTENCES]:
            text = o.text if len(o.text) <= 200 else o.text[:197] + "..."
            lines.append(f'  [{o.words} words] "{text}"')
    lines.append(
        "Split at conjunctions, cut throat-clearing openers, and un-nominalize. "
        "Keep technical terms exactly as they are."
    )
    return "\n".join(lines)


# hookSpecificOutput is validated against a per-event schema, and hookEventName is
# required inside it. Omitting it makes the harness reject the whole payload and surface
# a validation error to the user, which is exactly the disruption this hook exists to avoid.
def emit_advisory(report: str, event: str) -> None:
    print(json.dumps({
        "systemMessage": "Readability check failed on this draft.",
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": report,
        },
    }))
    sys.exit(0)


# Blocking uses the JSON decision form rather than exit 2. Both block, but the docs prefer
# JSON: it is structured, and the reason reaches the model as feedback rather than as an
# error string on stderr.
def emit_block(report: str) -> None:
    print(json.dumps({"decision": "block", "reason": report}))
    sys.exit(0)


def text_for_event(payload: dict, extensions: list[str]) -> str | None:
    event = payload.get("hook_event_name")

    # Stop covers the main session; SubagentStop is a separate event with the same payload
    # shape. Accept both so the hook still works if an operator wires it to either.
    if event in ("Stop", "SubagentStop"):
        return payload.get("last_assistant_message") or None

    if event == "PostToolUse":
        if payload.get("tool_name") not in ("Write", "Edit"):
            return None
        raw_path = (payload.get("tool_input") or {}).get("file_path")
        if not raw_path:
            return None
        path = Path(raw_path)
        if path.suffix.lower() not in extensions:
            return None
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None

    return None


ENABLED_VALUES = {"1", "true", "yes", "on"}


def main() -> None:
    # Opt-in gate. The plugin registers this hook on install, so it must stay inert until
    # the operator asks for it. Checked before anything else, including reading stdin.
    if os.environ.get("READABILITY_HOOK_ENABLED", "").strip().lower() not in ENABLED_VALUES:
        quiet_exit()

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        quiet_exit()

    profile = os.environ.get("READABILITY_HOOK_PROFILE", DEFAULT_PROFILE)
    mode = os.environ.get("READABILITY_HOOK_MODE", "advisory")
    extensions = [
        e.strip().lower() if e.strip().startswith(".") else "." + e.strip().lower()
        for e in os.environ.get("READABILITY_HOOK_EXTENSIONS", DEFAULT_EXTENSIONS).split(",")
        if e.strip()
    ]
    try:
        min_words = int(os.environ.get("READABILITY_HOOK_MIN_WORDS", DEFAULT_MIN_WORDS))
    except ValueError:
        min_words = DEFAULT_MIN_WORDS

    scorer = load_scorer()
    if scorer is None or profile not in scorer.PROFILES:
        quiet_exit()

    raw = text_for_event(payload, extensions)
    if not raw:
        quiet_exit()

    try:
        prose = scorer.markdown_to_prose(raw)
        if scorer.word_count(prose) < min_words:
            quiet_exit()
        result = scorer.score(prose, payload.get("hook_event_name", "draft"), profile)
    except Exception:
        quiet_exit()

    if not result.scored or result.passed:
        quiet_exit()

    report = build_report(result, profile)

    if mode == "block" and not already_blocked_this_turn(
        str(payload.get("session_id", "")), str(payload.get("prompt_id", ""))
    ):
        emit_block(report)

    emit_advisory(report, payload.get("hook_event_name", "Stop"))


if __name__ == "__main__":
    main()

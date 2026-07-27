#!/usr/bin/env python3
"""
readability.py — score prose on five readability formulas and name the sentences to fix.

Scores Flesch Reading Ease, Flesch-Kincaid Grade, SMOG, Gunning Fog, and Dale-Chall (v1),
then reports the specific sentences dragging the score down. The per-sentence offender
list is the actionable part; the aggregate scores only tell you whether to act.

CONSISTENT GRADE BANDS
  The five formulas use different scales, which makes them hard to read side by side.
  Every score is therefore also reported on one shared band scale — elementary, middle
  school, high school, college, college graduate — so a single glance shows whether the
  formulas agree. Raw scores are always printed alongside the band.

MARKDOWN-AWARE BY DEFAULT
  Readability formulas are only valid on continuous prose. Markdown tables, code fences,
  headings, and link URLs are not sentences, and scoring them produces noise. This script
  strips them before scoring. Use --include-tables to score table cell text as well.

GRACEFUL FALLBACK
  If textstat is missing, prints the exact pip install line and exits 3. A missing
  dependency is a normal branch, not a crash to debug.

USAGE
  python3 readability.py FILE [FILE ...]          # score files
  python3 readability.py --stdin                  # score piped text (for draft output)
  python3 readability.py FILE --profile public    # stricter target
  python3 readability.py FILE --json              # machine-readable
  python3 readability.py DIR --recursive          # all .md under DIR

EXIT CODES
  0  all inputs pass the profile
  1  at least one input fails
  3  textstat not installed
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    import textstat
except ImportError:
    print(
        "readability.py needs textstat.\n"
        "Install it with:\n"
        "    python3 -m pip install --user textstat",
        file=sys.stderr,
    )
    sys.exit(3)


# --- Thresholds -------------------------------------------------------------
#
# Each profile sets a floor on Flesch Reading Ease (higher = easier) and ceilings on the
# three grade-level formulas (lower = easier). Values are anchored to what each formula
# means, not picked for roundness.
#
#   technical  Dense engineering or scientific prose whose terminology is load-bearing.
#              Grade ~14 is upper-undergraduate, which is where accurate technical writing
#              lands once unavoidable terms are counted as complex. Below FRE 40 the prose
#              is doing more work than the subject requires.
#   general    Default for explanatory writing aimed at a competent non-specialist.
#              Grade ~12 is the widely used ceiling for professional communication.
#   public     Public-facing copy. Grade ~9 is the standard target for material intended
#              to be read by the general population without effort.
#
# max_sentence_words is the single most actionable lever: sentence length dominates every
# formula here, and over-long sentences are what make prose feel incoherent. The limits are
# set where a reader must re-read to hold the clause structure.

PROFILES = {
    "technical": {
        "flesch_reading_ease_min": 40.0,
        "flesch_kincaid_grade_max": 14.0,
        "gunning_fog_max": 16.0,
        "smog_index_max": 14.0,
        "dale_chall_max": 12.9,  # top of the college band; 13.0+ is college graduate
        "max_sentence_words": 40,
    },
    "general": {
        "flesch_reading_ease_min": 50.0,
        "flesch_kincaid_grade_max": 12.0,
        "gunning_fog_max": 14.0,
        "smog_index_max": 12.0,
        "dale_chall_max": 8.9,  # top of the high-school band
        "max_sentence_words": 35,
    },
    "public": {
        "flesch_reading_ease_min": 60.0,
        "flesch_kincaid_grade_max": 9.0,
        "gunning_fog_max": 11.0,
        "smog_index_max": 10.0,
        "dale_chall_max": 6.9,  # top of the middle-school band
        "max_sentence_words": 25,
    },
}

# --- Shared grade bands -----------------------------------------------------
#
# The five formulas are on incompatible scales: Flesch Reading Ease runs 0-100 and rises
# as text gets easier, Flesch-Kincaid / SMOG / Gunning Fog emit US grade numbers directly,
# and Dale-Chall emits a raw score read off a lookup table. Reporting all five on one band
# scale makes disagreement between them visible at a glance.

BANDS = (
    (6.0, "elementary"),
    (9.0, "middle school"),
    (13.0, "high school"),
    (16.0, "college"),
    (float("inf"), "college graduate"),
)

# Dale-Chall (v1, the original 1948 formula) raw score -> representative US grade.
#
# Banding note: this maps 9.0-12.9 to college and reserves "college graduate" for 13.0+.
# That is deliberately wider than the Chall & Dale 1995 table, which calls everything at
# 10.0+ college-graduate. The v1 formula runs hotter than the 1995 revision on technical
# prose, because every term outside its ~3,000-word familiar list counts as difficult, so
# the 1995 cutoffs push ordinary professional writing into the top band and stop
# discriminating. Widening the college band keeps the scale useful where real documents
# actually land. methodology.md records the alternative for anyone who wants it.
DALE_CHALL_TABLE = (
    (4.9, 4.0),    # grade 4 and below
    (6.9, 7.0),    # middle school
    (8.9, 11.0),   # high school
    (12.9, 14.0),  # college
    (float("inf"), 16.0),  # college graduate
)

# Flesch Reading Ease -> representative US grade, per Flesch's own interpretation table.
# Entries are (lower bound inclusive, representative grade), highest ease first.
FLESCH_EASE_TABLE = (
    (90.0, 5.0),
    (80.0, 6.0),
    (70.0, 7.0),
    (60.0, 8.5),
    (50.0, 11.0),
    (30.0, 14.0),
    (float("-inf"), 16.0),
)


def band_for_grade(grade: float) -> str:
    for ceiling, label in BANDS:
        if grade < ceiling:
            return label
    return BANDS[-1][1]


def dale_chall_grade(raw: float) -> float:
    for ceiling, grade in DALE_CHALL_TABLE:
        if raw <= ceiling:
            return grade
    return DALE_CHALL_TABLE[-1][1]


def flesch_ease_grade(raw: float) -> float:
    for floor, grade in FLESCH_EASE_TABLE:
        if raw >= floor:
            return grade
    return FLESCH_EASE_TABLE[-1][1]

# SMOG is defined over a 30-sentence sample. Below that it is not meaningful and textstat
# returns a value anyway, so we suppress it rather than report a number that means nothing.
SMOG_MIN_SENTENCES = 30

# Below this many words there is not enough text for any formula to be stable.
MIN_WORDS_FOR_SCORING = 40


# --- Markdown to prose ------------------------------------------------------

FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s")
HR = re.compile(r"^\s{0,3}([-*_])\s*(\1\s*){2,}$")
TABLE_ROW = re.compile(r"^\s*\|")
LIST_MARKER = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
QUOTE_MARKER = re.compile(r"^\s*>+\s?")

IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
INLINE_CODE = re.compile(r"`[^`]*`")
HTML_TAG = re.compile(r"<[^>]+>")
BARE_URL = re.compile(r"https?://\S+")
EMPHASIS = re.compile(r"(\*\*|\*|__|_|~~)")
FOOTNOTE = re.compile(r"\[\^[^\]]+\]")


def markdown_to_prose(text: str, include_tables: bool = False) -> str:
    """Reduce markdown to the continuous prose a readability formula can validly score."""
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    in_frontmatter = False

    for i, raw in enumerate(lines):
        if i == 0 and raw.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if raw.strip() == "---":
                in_frontmatter = False
            continue

        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if HEADING.match(raw) or HR.match(raw):
            continue

        if TABLE_ROW.match(raw):
            if not include_tables:
                continue
            # Keep cell text only; the pipes and alignment row are not prose.
            cells = [c.strip() for c in raw.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            raw = ". ".join(c for c in cells if c)

        line = QUOTE_MARKER.sub("", raw)
        was_list_item = bool(LIST_MARKER.match(line))
        line = LIST_MARKER.sub("", line)

        # A bullet is a sentence even when it is not punctuated as one. Without a
        # terminator, sentence splitting runs consecutive bullets together into one
        # artificially long "sentence" and reports a false over-length failure.
        if was_list_item:
            stripped = line.rstrip()
            if stripped and stripped[-1] not in ".!?:;":
                line = stripped + "."
            # Emit each bullet as its own paragraph. Sentence splitting keys on a capital
            # letter after the terminator, and a bullet often starts lowercase (a filename,
            # a code term), so punctuation alone would not separate consecutive bullets.
            out.append(line)
            out.append("")
            continue

        out.append(line)

    prose = "\n".join(out)

    prose = IMAGE.sub("", prose)
    prose = LINK.sub(r"\1", prose)
    prose = FOOTNOTE.sub("", prose)
    prose = INLINE_CODE.sub("", prose)
    prose = HTML_TAG.sub("", prose)
    prose = BARE_URL.sub("", prose)
    prose = EMPHASIS.sub("", prose)

    # Collapse the blank lines left behind so sentence splitting stays clean.
    prose = re.sub(r"[ \t]+", " ", prose)
    prose = re.sub(r"\n{2,}", "\n\n", prose)
    return prose.strip()


# --- Sentence handling ------------------------------------------------------

# Split on sentence-ending punctuation followed by whitespace and a capital or digit.
# Abbreviations ("e.g.", "Dr.") will occasionally split early; that costs a little
# precision in the offender list and does not affect the aggregate scores, which
# textstat computes independently.
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])[\"'”)\]]*\s+(?=[\"'“(\[]*[A-Z0-9])")


def split_sentences(prose: str) -> list[str]:
    """Split on paragraph boundaries first, then on sentence punctuation within each.

    Paragraphs are hard boundaries: a blank line always ends a sentence, whatever the
    punctuation. Inside a paragraph, wrapped lines are joined before splitting, so a
    hard-wrapped sentence is not cut at the line break.
    """
    sentences: list[str] = []
    for para in re.split(r"\n\s*\n", prose):
        flat = re.sub(r"\s*\n\s*", " ", para).strip()
        if not flat:
            continue
        sentences.extend(s.strip() for s in SENTENCE_SPLIT.split(flat) if s.strip())
    return sentences


def word_count(s: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", s))


# --- Scoring ----------------------------------------------------------------


@dataclass
class Offender:
    words: int
    text: str


@dataclass
class Result:
    source: str
    words: int
    sentences: int
    flesch_reading_ease: float | None
    flesch_kincaid_grade: float | None
    smog_index: float | None
    gunning_fog: float | None
    dale_chall: float | None
    bands: dict[str, str]
    consensus_band: str | None
    failures: list[str]
    long_sentences: list[Offender]
    scored: bool
    note: str = ""

    @property
    def passed(self) -> bool:
        return self.scored and not self.failures


def score(prose: str, source: str, profile: str) -> Result:
    limits = PROFILES[profile]
    sentences = split_sentences(prose)
    words = word_count(prose)

    if words < MIN_WORDS_FOR_SCORING:
        return Result(
            source=source,
            words=words,
            sentences=len(sentences),
            flesch_reading_ease=None,
            flesch_kincaid_grade=None,
            smog_index=None,
            gunning_fog=None,
            dale_chall=None,
            bands={},
            consensus_band=None,
            failures=[],
            long_sentences=[],
            scored=False,
            note=f"only {words} words of prose; too short to score reliably",
        )

    fre = round(textstat.flesch_reading_ease(prose), 1)
    fkg = round(textstat.flesch_kincaid_grade(prose), 1)
    fog = round(textstat.gunning_fog(prose), 1)
    dc = round(textstat.dale_chall_readability_score(prose), 1)
    smog = round(textstat.smog_index(prose), 1) if len(sentences) >= SMOG_MIN_SENTENCES else None

    bands = {
        "flesch_reading_ease": band_for_grade(flesch_ease_grade(fre)),
        "flesch_kincaid_grade": band_for_grade(fkg),
        "gunning_fog": band_for_grade(fog),
        "dale_chall": band_for_grade(dale_chall_grade(dc)),
    }
    if smog is not None:
        bands["smog_index"] = band_for_grade(smog)

    # The consensus is the band the most formulas agree on. Ties resolve to the harder
    # band, since under-stating difficulty is the more costly error for a reader.
    order = [label for _, label in BANDS]
    counts = {b: list(bands.values()).count(b) for b in set(bands.values())}
    top = max(counts.values())
    consensus_band = max((b for b, c in counts.items() if c == top), key=order.index)

    failures = []
    if fre < limits["flesch_reading_ease_min"]:
        failures.append(f"Flesch Reading Ease {fre} < {limits['flesch_reading_ease_min']}")
    if fkg > limits["flesch_kincaid_grade_max"]:
        failures.append(f"Flesch-Kincaid Grade {fkg} > {limits['flesch_kincaid_grade_max']}")
    if fog > limits["gunning_fog_max"]:
        failures.append(f"Gunning Fog {fog} > {limits['gunning_fog_max']}")
    if dc > limits["dale_chall_max"]:
        failures.append(f"Dale-Chall {dc} > {limits['dale_chall_max']}")
    if smog is not None and smog > limits["smog_index_max"]:
        failures.append(f"SMOG {smog} > {limits['smog_index_max']}")

    cap = limits["max_sentence_words"]
    long_sentences = sorted(
        (Offender(words=word_count(s), text=s) for s in sentences if word_count(s) > cap),
        key=lambda o: o.words,
        reverse=True,
    )
    if long_sentences:
        failures.append(f"{len(long_sentences)} sentence(s) over {cap} words")

    note = "" if smog is not None else f"SMOG omitted (needs {SMOG_MIN_SENTENCES}+ sentences)"

    return Result(
        source=source,
        words=words,
        sentences=len(sentences),
        flesch_reading_ease=fre,
        flesch_kincaid_grade=fkg,
        smog_index=smog,
        gunning_fog=fog,
        dale_chall=dc,
        bands=bands,
        consensus_band=consensus_band,
        failures=failures,
        long_sentences=long_sentences,
        scored=True,
        note=note,
    )


# --- Reporting --------------------------------------------------------------


def render(result: Result, offenders: int) -> str:
    if not result.scored:
        return f"— {result.source}: {result.note}"

    mark = "PASS" if result.passed else "FAIL"
    smog = f"{result.smog_index}" if result.smog_index is not None else "n/a"
    lines = [
        f"{mark}  {result.source}",
        f"      {result.words} words / {result.sentences} sentences of prose"
        f"   →  reads at: {result.consensus_band}",
        f"      Flesch Reading Ease {result.flesch_reading_ease} ({result.bands['flesch_reading_ease']})",
        f"      Flesch-Kincaid      {result.flesch_kincaid_grade} ({result.bands['flesch_kincaid_grade']})",
        f"      Gunning Fog         {result.gunning_fog} ({result.bands['gunning_fog']})",
        f"      Dale-Chall          {result.dale_chall} ({result.bands['dale_chall']})",
        f"      SMOG                {smog}"
        + (f" ({result.bands['smog_index']})" if result.smog_index is not None else ""),
    ]
    if result.note:
        lines.append(f"      ({result.note})")
    for f in result.failures:
        lines.append(f"      ✗ {f}")
    if result.long_sentences and offenders:
        lines.append(f"      Longest sentences — rewrite these first:")
        for o in result.long_sentences[:offenders]:
            snippet = o.text if len(o.text) <= 220 else o.text[:217] + "..."
            lines.append(f"        [{o.words}w] {snippet}")
    return "\n".join(lines)


def collect_paths(inputs: list[str], recursive: bool) -> list[Path]:
    paths: list[Path] = []
    for raw in inputs:
        p = Path(raw)
        if p.is_dir():
            pattern = "**/*.md" if recursive else "*.md"
            paths.extend(sorted(p.glob(pattern)))
        elif p.exists():
            paths.append(p)
        else:
            print(f"warning: {raw} not found, skipping", file=sys.stderr)
    return paths


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Score prose readability and name the sentences to fix.",
    )
    ap.add_argument("inputs", nargs="*", help="files or directories")
    ap.add_argument("--stdin", action="store_true", help="score text piped on stdin")
    ap.add_argument("--profile", choices=sorted(PROFILES), default="general")
    ap.add_argument("--recursive", action="store_true", help="recurse into directories")
    ap.add_argument("--include-tables", action="store_true", help="also score table cell text")
    ap.add_argument("--offenders", type=int, default=3, help="long sentences to show (0 to hide)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    if not args.stdin and not args.inputs:
        ap.error("give at least one file or directory, or use --stdin")

    results: list[Result] = []

    if args.stdin:
        raw = sys.stdin.read()
        prose = markdown_to_prose(raw, args.include_tables)
        results.append(score(prose, "<stdin>", args.profile))

    for path in collect_paths(args.inputs, args.recursive):
        try:
            raw = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            print(f"warning: cannot read {path} ({e}), skipping", file=sys.stderr)
            continue
        prose = markdown_to_prose(raw, args.include_tables)
        results.append(score(prose, str(path), args.profile))

    if not results:
        print("nothing to score", file=sys.stderr)
        return 0

    if args.json:
        print(json.dumps(
            {"profile": args.profile, "results": [asdict(r) for r in results]},
            indent=2,
        ))
    else:
        print(f"profile: {args.profile}\n")
        for r in results:
            print(render(r, args.offenders))
            print()
        scored = [r for r in results if r.scored]
        failed = [r for r in scored if not r.passed]
        print(f"{len(scored) - len(failed)}/{len(scored)} passed")
        if failed:
            print("failing: " + ", ".join(r.source for r in failed))

    return 1 if any(r.scored and not r.passed for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())

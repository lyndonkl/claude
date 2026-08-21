#!/usr/bin/env python3
"""Remove stale concept files left behind by a re-run.

A resumed synthesis run re-created each area's concepts under slightly different slugs,
so directories hold two generations. The `_index.md` written by the surviving run lists
the canonical slugs; anything else in the directory is an orphan from the earlier pass.

Dry run by default. Pass --apply to delete.
"""
import os, re, sys, argparse

KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONCEPTS = os.path.join(KB, "concepts")


def referenced_slugs(index_path):
    """Slugs named anywhere in the index — table rows, wiki links, or bare mentions."""
    text = open(index_path).read()
    slugs = set(re.findall(r"\[\[([a-z0-9][a-z0-9-]*)\]\]", text))
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        m = re.fullmatch(r"\[\[([a-z0-9][a-z0-9-]*)\]\]", first) or \
            re.fullmatch(r"`?([a-z0-9][a-z0-9-]*)`?", first)
        if m and m.group(1) not in {"slug", "covers", "determinism"}:
            slugs.add(m.group(1))
    return slugs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually delete the orphans")
    args = ap.parse_args()

    total_keep = total_drop = 0
    for area in sorted(os.listdir(CONCEPTS)):
        d = os.path.join(CONCEPTS, area)
        idx = os.path.join(d, "_index.md")
        if not os.path.isdir(d):
            continue
        files = {f[:-3] for f in os.listdir(d) if f.endswith(".md") and f != "_index.md"}
        if not os.path.exists(idx):
            print("%-34s NO INDEX — keeping all %d files" % (area, len(files)))
            total_keep += len(files)
            continue
        keep = referenced_slugs(idx) & files
        drop = files - keep
        if not keep:
            print("%-34s index names none of the files — keeping all %d" % (area, len(files)))
            total_keep += len(files)
            continue
        total_keep += len(keep)
        total_drop += len(drop)
        print("%-34s keep %2d  drop %2d" % (area, len(keep), len(drop)))
        for slug in sorted(drop):
            path = os.path.join(d, slug + ".md")
            if args.apply:
                os.remove(path)
            else:
                print("      would remove", os.path.relpath(path, KB))
    print("\n%s: keep %d, drop %d" % ("APPLIED" if args.apply else "DRY RUN",
                                      total_keep, total_drop))


if __name__ == "__main__":
    main()

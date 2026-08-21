#!/usr/bin/env python3
"""Verify page-level extraction coverage: every expected chunk file exists and
contains a `## p.<N>` section for every page in its range. Exit 1 on gaps."""
import json, os, re, sys

KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
w = json.load(open(os.path.join(KB, "worklist.json")))

missing_files, missing_pages, ok_pages = [], [], 0
for it in w["pdf"]:
    path = os.path.join(KB, "pages", it["slug"], f"p{it['start']:04d}-p{it['end']:04d}.md")
    if not os.path.exists(path):
        missing_files.append(path)
        continue
    text = open(path).read()
    found = set(int(m) for m in re.findall(r"^## p\.(\d+)", text, re.M))
    for n in range(it["start"], it["end"] + 1):
        if n in found:
            ok_pages += 1
        else:
            missing_pages.append((it["slug"], n, path))

xls_missing = []
for it in w["xls"]:
    path = os.path.join(KB, "spreadsheets", f"{it['slug']}.md")
    if not os.path.exists(path):
        xls_missing.append(path)

print(f"pages covered: {ok_pages}/{w['total_unique_pages']}")
if missing_files:
    print(f"\nMISSING CHUNK FILES ({len(missing_files)}):")
    for p in missing_files:
        print(" ", p)
if missing_pages:
    print(f"\nMISSING PAGE SECTIONS ({len(missing_pages)}):")
    for slug, n, path in missing_pages:
        print(f"  {slug} p.{n}  ({os.path.basename(path)})")
if xls_missing:
    print(f"\nMISSING SPREADSHEET DOCS ({len(xls_missing)}):")
    for p in xls_missing:
        print(" ", p)
if not (missing_files or missing_pages or xls_missing):
    print("COMPLETE: all pages and spreadsheet groups covered.")
    sys.exit(0)
sys.exit(1)

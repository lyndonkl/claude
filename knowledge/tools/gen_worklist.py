#!/usr/bin/env python3
"""Generate the extraction work-list: PDF page-range chunks + spreadsheet groups."""
import json, os, sys
from pypdf import PdfReader

ROOT = "/Users/kushaldsouza/Downloads/2020"
CHUNK = 40  # pages per extraction agent

# Byte-identical duplicates to skip (md5-verified), keeping the canonical copy.
SKIP_PDF = {
    os.path.join(ROOT, "Valuations 2021/valpacket1spr21.pdf"),
    os.path.join(ROOT, "Valuations 2021/valpacket2spr21.pdf"),
    os.path.join(ROOT, "Valuations 2021/valpacket3spr21.pdf"),
}

def slugify(path):
    rel = os.path.relpath(path, ROOT)
    return (
        rel.replace(".pdf", "")
        .replace("/", "--")
        .replace(" ", "_")
        .replace("&", "and")
        .lower()
    )

pdf_items = []
total_pages = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in sorted(filenames):
        if not fn.lower().endswith(".pdf"):
            continue
        path = os.path.join(dirpath, fn)
        if path in SKIP_PDF:
            continue
        n = len(PdfReader(path).pages)
        total_pages += n
        slug = slugify(path)
        start = 1
        while start <= n:
            end = min(start + CHUNK - 1, n)
            pdf_items.append({
                "kind": "pdf",
                "path": path,
                "slug": slug,
                "start": start,
                "end": end,
                "total": n,
            })
            start = end + 1

# Spreadsheet groups: unique files only (md5-verified dupes collapsed),
# grouped so each agent gets one model family or a small related set.
S = os.path.join(ROOT, "Spreadsheets")
groups = {
    "ginzu-fcff-simple": [os.path.join(S, "Big Picture Valuation Spreadsheets/fcffsimpleginzu.xlsx")],
    "ginzu-fcff-full": [os.path.join(S, "Big Picture Valuation Spreadsheets/fcffginzu.xlsx")],
    "ginzu-fcff-lambda": [os.path.join(S, "Big Picture Valuation Spreadsheets/fcffginzulambda.xls")],
    "ginzu-fcfe": [os.path.join(S, "Big Picture Valuation Spreadsheets/fcfeginzu.xls")],
    "ginzu-dividend": [os.path.join(S, "Big Picture Valuation Spreadsheets/divginzu.xls")],
    "ginzu-fcff-corona": [os.path.join(S, "Big Picture Valuation Spreadsheets/fcffsimpleginzuCorona.xlsx")],
    "growth-models": [
        os.path.join(S, "Big Picture Valuation Spreadsheets/growthbreakdown.xls"),
        os.path.join(S, "Big Picture Valuation Spreadsheets/higrowth.xls"),
        os.path.join(S, "Big Picture Valuation Spreadsheets/model.xls"),
        os.path.join(S, "Young and High Growth Firms/revgrowth.xls"),
    ],
    "corpfin-capital-structure": [
        os.path.join(S, "Corporate Finance Spreadsheets/capstru.xlsx"),
        os.path.join(S, "Corporate Finance Spreadsheets/apv.xls"),
        os.path.join(S, "Corporate Finance Spreadsheets/levbeta.xls"),
        os.path.join(S, "Corporate Finance Spreadsheets/macrodur.xls"),
    ],
    "corpfin-ratings-risk": [
        os.path.join(S, "Corporate Finance Spreadsheets/ratings.xls"),
        os.path.join(S, "Corporate Finance Spreadsheets/risk.xls"),
        os.path.join(S, "Corporate Finance Spreadsheets/riskchecker.xls"),
        os.path.join(S, "Corporate Finance Spreadsheets/returncalculator.xls"),
    ],
    "corpfin-payout-projects": [
        os.path.join(S, "Corporate Finance Spreadsheets/dividends.xls"),
        os.path.join(S, "Corporate Finance Spreadsheets/buybacks.xls"),
        os.path.join(S, "Corporate Finance Spreadsheets/capbudg.xls"),
        os.path.join(S, "Corporate Finance Spreadsheets/oplease.xls"),
    ],
    "focussed-ddm": [
        os.path.join(S, "Focussed Valuation Model Spreadsheet/ddmst.xls"),
        os.path.join(S, "Focussed Valuation Model Spreadsheet/ddm2st.xls"),
        os.path.join(S, "Focussed Valuation Model Spreadsheet/ddm3st.xls"),
    ],
    "focussed-fcfe": [
        os.path.join(S, "Focussed Valuation Model Spreadsheet/fcfest.xls"),
        os.path.join(S, "Focussed Valuation Model Spreadsheet/fcfe2st.xls"),
        os.path.join(S, "Focussed Valuation Model Spreadsheet/fcfe3st.xls"),
    ],
    "focussed-fcff": [
        os.path.join(S, "Focussed Valuation Model Spreadsheet/fcffst.xls"),
        os.path.join(S, "Focussed Valuation Model Spreadsheet/fcff2st.xls"),
        os.path.join(S, "Focussed Valuation Model Spreadsheet/fcff3st.xls"),
        os.path.join(S, "Focussed Valuation Model Spreadsheet/fcffgen.xls"),
    ],
    "valuation-inputs-1": [
        os.path.join(S, "Valuation Inputs Spreadsheet/wacccalc.xls"),
        os.path.join(S, "Valuation Inputs Spreadsheet/implprem.xls"),
        os.path.join(S, "Valuation Inputs Spreadsheet/ImpliedROCROE.xls"),
    ],
    "valuation-inputs-2": [
        os.path.join(S, "Valuation Inputs Spreadsheet/R&DConv.xls"),
        os.path.join(S, "Valuation Inputs Spreadsheet/cpxest.xls"),
        os.path.join(S, "Valuation Inputs Spreadsheet/readme1s.xls"),
    ],
    "special-private": [
        os.path.join(S, "Private Companies/liqdisc.xls"),
        os.path.join(S, "Private Companies/minoritydiscount.xls"),
        os.path.join(S, "Private Companies/pvtdiscrate.xls"),
    ],
    "special-troubled": [
        os.path.join(S, "Troubled Firms/distress.xls"),
        os.path.join(S, "Troubled Firms/fcffneg.xls"),
        os.path.join(S, "Troubled Firms/normearn.xls"),
    ],
    "reconciliation": [
        os.path.join(S, "Valuation Model Reconciliation/fcfevsddm.xls"),
        os.path.join(S, "Valuation Model Reconciliation/fcffvsfcfe.xls"),
        os.path.join(S, "Valuation Model Reconciliation/fcffeva.xls"),
        os.path.join(S, "Valuation Model Reconciliation/GrossvsNet.xls"),
    ],
    "focussed-eva-finsvc": [
        os.path.join(S, "Focussed Valuation Model Spreadsheet/evavaln.xls"),
        os.path.join(S, "Financial Service Firms/eqexret.xls"),
    ],
    "motley-fool-tesla": [
        os.path.join(ROOT, "Motley Fool Presentation/TeslaNov2021DIY.xlsx"),
    ],
}

xls_items = []
for name, files in groups.items():
    missing = [f for f in files if not os.path.exists(f)]
    if missing:
        print("MISSING:", missing, file=sys.stderr)
        sys.exit(1)
    xls_items.append({"kind": "xls", "slug": name, "files": files})

out = {"pdf": pdf_items, "xls": xls_items, "total_unique_pages": total_pages}
print(json.dumps(out, indent=1))
print(f"PDF chunks: {len(pdf_items)}  XLS groups: {len(xls_items)}  unique pages: {total_pages}", file=sys.stderr)

import xlrd
wb = xlrd.open_workbook("/Users/kushaldsouza/Downloads/2020/Spreadsheets/Big Picture Valuation Spreadsheets/divginzu.xls")

def fmt(v):
    if isinstance(v, float):
        if v == int(v) and abs(v) < 1e15:
            return str(int(v))
        return f"{v:.6g}"
    return str(v).replace("|", "\\|")

out = []

# US Industry averages
sh = wb.sheet_by_name("US Industry averages")
hdr = [fmt(sh.cell_value(0, c)) for c in range(sh.ncols)]
out.append("| " + " | ".join(hdr) + " |")
out.append("|" + "---|" * len(hdr))
for r in range(1, sh.nrows):
    row = [fmt(sh.cell_value(r, c)) for c in range(sh.ncols)]
    if any(x.strip() for x in row):
        out.append("| " + " | ".join(row) + " |")
out.append("")
out.append("===SPLIT===")

# Country ERP: countries rows 5-190 (idx 4-189)
sh = wb.sheet_by_name("Country ERP")
out.append("| Country | Moody's rating | Adj. Default Spread | Equity Risk Premium | Country Risk Premium | Corporate Tax Rate |")
out.append("|---|---|---|---|---|---|")
for r in range(4, 190):
    row = [fmt(sh.cell_value(r, c)) for c in range(6)]
    if row[0].strip():
        out.append("| " + " | ".join(row) + " |")
out.append("")
out.append("===SPLIT===")
# Regions rows 194-202 (idx 193-201) + Global 204 (idx 203)
out.append("| Region | ERP | Default Spread | Tax rate | CRP |")
out.append("|---|---|---|---|---|")
for r in list(range(193, 202)) + [203]:
    row = [fmt(sh.cell_value(r, c)) for c in range(5)]
    if row[0].strip():
        out.append("| " + " | ".join(row) + " |")

with open("/private/tmp/claude-501/-Users-kushaldsouza-Documents-Projects-claude/1600ea90-8623-468a-b744-aa9639cab216/scratchpad/kb/spreadsheets/tables.md", "w") as f:
    f.write("\n".join(out))
print("wrote tables.md")

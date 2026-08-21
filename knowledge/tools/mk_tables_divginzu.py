import xlrd, sys

path = "/Users/kushaldsouza/Downloads/2020/Spreadsheets/Big Picture Valuation Spreadsheets/divginzu.xls"
book = xlrd.open_workbook(path)

def fmt(v):
    if v == '' or v is None: return ''
    if isinstance(v, float):
        if v == int(v) and abs(v) < 1e10: return str(int(v))
        return f"{round(v,6):.6g}"
    return str(v).strip()

def table(sheet, r0, r1, c0, c1):
    sh = book.sheet_by_name(sheet)
    lines = []
    for r in range(r0, min(r1, sh.nrows)):
        cells = [fmt(sh.cell_value(r,c)) if c < sh.ncols else '' for c in range(c0,c1)]
        if not any(cells): continue
        lines.append("| " + " | ".join(cells) + " |")
        if r == r0:
            lines.append("|" + "---|"*(c1-c0))
    return "\n".join(lines)

out = []
out.append("US_INDUSTRY\n" + table("US Industry averages", 0, 200, 0, 27))
out.append("\nCOUNTRY_ERP\n" + table("Country ERP", 3, 300, 0, 6))
sh = book.sheet_by_name("Country ERP")
print("Country ERP nrows:", sh.nrows)
open("/private/tmp/claude-501/-Users-kushaldsouza-Documents-Projects-claude/1600ea90-8623-468a-b744-aa9639cab216/scratchpad/kb/tools/divginzu_tables.md","w").write("\n".join(out))

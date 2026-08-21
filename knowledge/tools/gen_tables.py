import openpyxl, sys, warnings
warnings.filterwarnings("ignore")

F = "/Users/kushaldsouza/Downloads/2020/Spreadsheets/Big Picture Valuation Spreadsheets/fcffsimpleginzu.xlsx"
OUT = sys.argv[1]

wb = openpyxl.load_workbook(F, data_only=True)

def fmt(v):
    if v is None:
        return ""
    if isinstance(v, float):
        return repr(v)
    return str(v)

def md_table(ws, rows, cols, header=None):
    lines = []
    it = list(rows)
    for i, r in enumerate(it):
        vals = [fmt(ws.cell(row=r, column=c).value) for c in cols]
        lines.append("| " + " | ".join(vals) + " |")
        if i == 0:
            lines.append("|" + "---|" * len(cols))
    return "\n".join(lines)

with open(OUT, "w") as f:
    # Country ERP table
    ws = wb["Country equity risk premiums"]
    f.write("#### Country table (rows 5-181)\n\n")
    f.write(md_table(ws, range(4, 182), range(1, 7)))
    f.write("\n\n#### Region table (rows 185-194)\n\n")
    f.write(md_table(ws, range(184, 195), range(1, 6)))
    f.write("\n\n")

    # Industry sheets, all 27 columns
    for sheet, tag in [("Industry Averages(US)", "US"), ("Industry Average Beta (Global)", "GLOBAL")]:
        ws = wb[sheet]
        f.write(f"#### INDUSTRY TABLE {tag} (rows 2-95, columns A-AA)\n\n")
        f.write(md_table(ws, range(1, 96), range(1, 28)))
        f.write("\n\n")
print("done")

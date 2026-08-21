import xlrd
path = "/Users/kushaldsouza/Downloads/2020/Spreadsheets/Big Picture Valuation Spreadsheets/fcfeginzu.xls"
wb = xlrd.open_workbook(path)

def fmt(v):
    if isinstance(v, float):
        if v == int(v) and abs(v) < 1e12:
            return str(int(v))
        return f"{v:.6g}"
    return str(v).replace("|","\\|")

def table(sheetname, r0, r1, cols, out):
    sh = wb.sheet_by_name(sheetname)
    with open(out,"w") as f:
        for r in range(r0, min(r1, sh.nrows)):
            vals=[]
            for c in cols:
                try: v=sh.cell_value(r,c)
                except IndexError: v=""
                vals.append(fmt(v) if v!="" else "")
            if any(vals):
                f.write("| "+" | ".join(vals)+" |\n")
            if r==r0:
                f.write("|"+"---|"*len(cols)+"\n")

# Industry averages: rows 0..96, cols 0..26
table("Industry averages", 0, 97, list(range(27)), "/private/tmp/claude-501/-Users-kushaldsouza-Documents-Projects-claude/1600ea90-8623-468a-b744-aa9639cab216/scratchpad/kb/spreadsheets/_ind.md")
# Country ERP: rows 3..195, cols 0..5
table("Country ERP", 3, 195, list(range(6)), "/private/tmp/claude-501/-Users-kushaldsouza-Documents-Projects-claude/1600ea90-8623-468a-b744-aa9639cab216/scratchpad/kb/spreadsheets/_cty.md")
sh = wb.sheet_by_name("Country ERP")
print("nrows", sh.nrows)
for r in range(150, sh.nrows):
    print(r+1, [sh.cell_value(r,c) for c in range(6)])

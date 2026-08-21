# R&D capitalization (building the research asset)

**Core idea:** R&D is spending undertaken to create future growth, which makes it a capital expenditure in economic substance. Accounting requires it to be expensed, which understates operating income, understates book capital, and makes R&D-intensive firms look like they reinvest nothing. The fix is to pick an amortizable life, treat each of the last N years of R&D as an investment being amortized straight-line over that life, sum the unamortized balances into a **research asset**, add current R&D back to operating income and subtract this year's amortization instead, and add the research asset to book equity and book capital. The adjustment is material: R&D is ~50% of operating income for computer firms and ~30% for petroleum, versus ~10.5% for the market. Crucially, **FCFF is unchanged** by the adjustment — earnings and reinvestment both rise by the same amount — but earnings, capital, and return on capital all change, and those drive growth.

**Formulas:**
Let `N` = amortizable life in years, `RD_0` = current-year R&D, `RD_k` = R&D expense k years ago.
- Unamortized fraction of `RD_k` = `max(0, (N − k)/N)` (so `RD_0` counts fully at 1.0, and `RD_N` contributes 0).
- **Research asset** `RA = SUM over k = 0..N of RD_k × (N − k)/N`.
- **Amortization this year** `AM = SUM over k = 1..N of RD_k / N` (current-year R&D is *not* amortized in the current year).
- Adjustment to operating income = `RD_0 − AM` (positive for a growing R&D spender, negative for a shrinking one).
- Adjusted EBIT = EBIT + `RD_0` − `AM`.
- Adjusted after-tax operating income = `EBIT × (1 − t) + RD_0 − AM`. **The add-back is NOT tax-effected** — the firm already took the tax deduction on the full expensed R&D. Equivalently: adjusted EBIT(1−t) = EBIT(1−t) + (ignored tax benefit), where the ignored tax benefit = `(RD_0 − AM) × t`.
- Adjusted net income = Net income + `RD_0` − `AM`.
- Adjusted book value of capital (and of equity) = Book value + `RA`.
- Adjusted capital expenditures = Cap ex + `RD_0`; Adjusted depreciation & amortization = D&A + `AM`.
- Adjusted net cap ex = Net cap ex + `RD_0` − `AM`.
- Adjusted return on capital = Adjusted after-tax operating income / (Adjusted book capital).

**Procedure:**
1. Choose the amortizable life `N` (2–10 years) from how long research takes to pay off in this business. Use the industry lookup table below; the guideline blocks are: non-technological service 2, retail/tech service 3, light manufacturing 5, heavy manufacturing 10, research-with-patenting 10, long gestation 10.
2. Collect R&D expense for the current year and each of the previous `N` years from the income statements. If fewer than `N` years of history exist, pad with zeros — and flag it, because this understates the research asset.
3. For each year k = 0..N compute the unamortized fraction `(N−k)/N` and the unamortized amount `RD_k × (N−k)/N`. Sum -> **research asset `RA`**.
4. Compute `AM` = sum of `RD_k / N` over k = 1..N. Note the year `−N` row contributes nothing to `RA` but does contribute `RD_N/N` to amortization — do not drop it.
5. Adjust the income statement: EBIT += `RD_0 − AM`; net income += `RD_0 − AM`; after-tax operating income += `RD_0 − AM` (untaxed add-back).
6. Adjust the balance sheet: book equity += `RA`; book capital += `RA`.
7. Adjust reinvestment: cap ex += `RD_0`; depreciation += `AM`; therefore net cap ex += `RD_0 − AM`.
8. Verify FCFF is unchanged: the rise in after-tax operating income exactly offsets the rise in net cap ex.
9. Recompute return on capital, reinvestment rate and hence fundamental growth on the adjusted numbers.
10. The identical machinery capitalizes other intangible spending: brand advertising, employee training/human capital. Same steps, different `N`.

**Reference data — amortizable life by industry (Value Line industry names):**

Guideline categories: Non-technological service **2**; Retail, tech service **3**; Light manufacturing **5**; Heavy manufacturing **10**; Research with patenting **10**; Long gestation period **10**.

| Industry | N | Industry | N | Industry | N |
|---|---|---|---|---|---|
| Advertising | 2 | Electronics | 5 | Newspaper | 3 |
| Aerospace/Defense | 10 | Entertainment | 3 | Office Equip & Supplies | 5 |
| Air Transport | 10 | Environmental | 5 | Oilfield Services/Equip. | 5 |
| Aluminum | 5 | Financial Services | 2 | Packaging & Container | 5 |
| Apparel | 3 | Food Processing | 3 | Paper & Forest Products | 10 |
| Auto & Truck | 10 | Food Wholesalers | 3 | Petroleum (Integrated) | 5 |
| Auto Parts (OEM) | 5 | Foreign Electron/Entertn | 5 | Petroleum (Producing) | 5 |
| Auto Parts (Replacement) | 5 | Foreign Telecom. | 10 | Precision Instrument | 5 |
| Bank (all variants) | 2 | Furn./Home Furnishings | 3 | Publishing | 3 |
| Beverage (Alcoholic) | 3 | Gold/Silver Mining | 5 | R.E.I.T. | 3 |
| Beverage (Soft Drink) | 3 | Grocery | 2 | Railroad | 5 |
| Building Materials | 5 | Healthcare Info Systems | 3 | Recreation | 5 |
| Cable TV | 10 | Home Appliance | 5 | Restaurant | 2 |
| Canadian Energy | 10 | Homebuilding | 5 | Retail (Special Lines) | 2 |
| Cement & Aggregates | 10 | Hotel/Gaming | 3 | Retail Building Supply | 2 |
| Chemical (Basic) | 10 | Household Products | 3 | Retail Store | 2 |
| Chemical (Diversified) | 10 | Industrial Services | 3 | Securities Brokerage | 2 |
| Chemical (Specialty) | 10 | Insurance (all variants) | 3 | Semiconductor | 5 |
| Coal/Alternate Energy | 5 | Internet | 3 | Semiconductor Cap Equip | 5 |
| Computer & Peripherals | 5 | Investment Co. (all) | 3 | Shoe | 3 |
| Computer Software & Svcs | 3 | Machinery | 10 | Steel (General/Integrated) | 5 |
| Copper | 5 | Manuf. Housing/Rec Veh | 5 | Telecom. Equipment | 10 |
| Diversified Co. | 5 | Maritime | 10 | Telecom. Services | 5 |
| Drug | 10 | Medical Services | 3 | Textile | 5 |
| Drugstore | 3 | Medical Supplies | 5 | Thrift | 2 |
| Educational Services | 3 | Metal Fabricating | 10 | Tire & Rubber | 5 |
| Electric Utility (all) | 10 | Metals & Mining (Div.) | 5 | Tobacco | 5 |
| Electrical Equipment | 10 | Natural Gas (Distrib./Div.) | 10 | Toiletries/Cosmetics | 3 |
| | | | | Trucking/Transp. Leasing | 5 |
| | | | | Utility (Foreign) / Water Utility | 10 |

**Worked example — SAP, 5-year life (EUR millions):**

| Year | R&D | Unamortized fraction | Unamortized amount | Amortization this year |
|---|---|---|---|---|
| Current | 1,020.02 | 1.00 | 1,020.02 | — |
| −1 | 993.99 | 0.80 | 795.19 | 198.80 |
| −2 | 909.39 | 0.60 | 545.63 | 181.88 |
| −3 | 898.25 | 0.40 | 359.30 | 179.65 |
| −4 | 969.38 | 0.20 | 193.88 | 193.88 |
| −5 | 744.67 | 0.00 | 0.00 | 148.93 |
| **Total** | | | **RA = 2,914** | **AM = 903** |

Effect (tax rate 36.54%, book debt 530, book equity 3,768):
- Increase in operating income = 1,020 − 903 = **+117**. EBIT: 2,025 -> 2,142.
- EBIT(1−t): 1,285 -> 1,359, plus the ignored tax benefit (1,020 − 903) × 0.3654 = 43, so adjusted EBIT(1−t) = **1,402** (also +117).
- Book equity: 3,768 + 2,914 = **6,782**.
- Net cap ex: 2 + 1,020 − 903 = **119** (was 2).
- FCFF: 1,285 − 2 = 1,283 conventional; 1,402 − 119 = **1,283** adjusted — **unchanged**.
- Return on capital: 1,285/(3,768+530) = 29.9% conventional; 1,402/(6,782+530) = **19.2%** adjusted.

Second worked example (the R&DConv.xls template, 5-year life, $m): R&D 1,594 / 1,026 / 698 / 399 / 211 / 89 for years 0..−5 gives `RA = 3,035.4` and `AM = 484.6`. With EBIT 3,195, tax 40%, net income 1,025, book capital 5,256, cap ex 655, D&A 525: adjusted EBIT = 4,304.4; adjusted after-tax operating income = 3,195×0.6 + 1,594 − 484.6 = 3,026.4; adjusted net income = 2,134.4; adjusted book capital = 8,291.4; adjusted cap ex = 2,249; adjusted D&A = 1,009.6; ROC 36.47% -> 36.50%.

**Determinism:**
- DETERMINISTIC: given `N`, `RD_0` and the `N` prior years of R&D -> research asset, amortization, EBIT / net income / after-tax operating income adjustments, adjusted book capital, adjusted cap ex and depreciation, adjusted ROC. Fully scriptable.
- JUDGMENT: choosing `N` (the industry table is a default, not a fact — how long does *this* firm's research take to pay off?); handling missing history; deciding whether to also capitalize advertising or training spend; whether the current year's R&D is representative.

**Pitfalls:**
- **Tax-effecting the add-back.** Adjusted after-tax operating income = EBIT(1−t) + (R&D − amortization), not EBIT(1−t) + (R&D − amortization)×(1−t). The tax deduction was already taken. This is the single most common porting error.
- Adjusting earnings but not book capital — ROC then looks spectacular and drives an inflated fundamental growth rate.
- Expecting FCFF to change. It does not; only earnings, capital, and growth do.
- Dropping the year `−N` row because it adds nothing to the asset — it still contributes to amortization.
- Padding missing years with zeros and forgetting that the research asset is now understated.
- Assuming the adjustment always raises income: if R&D is shrinking, `AM > RD_0` and operating income falls.

**Sources:**
- valpacket1spr21 p.123, p.129-132, p.141
- valpacket1spr20 p.120, p.126-129, p.138
- spreadsheet:R&DConv.xls — Inputs / `R&D capitalizer` / `Amortizable Lives Look-up Table` sheets (full formula set and the industry table)
- spreadsheet:fcffsimpleginzu.xlsx — `R& D converter` sheet and its feed into adjusted base EBIT and invested capital
- spreadsheet:higrowth.xls — `R&D` sheet (identical converter; also reproduces the industry amortization-life table)

**Related:** [[reported-to-actual-earnings]], [[operating-lease-capitalization]], [[net-capital-expenditures]], [[return-on-invested-capital]], [[fcff]], [[fundamental-growth-operating]], [[intangible-assets]]

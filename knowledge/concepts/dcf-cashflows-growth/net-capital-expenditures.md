# Net capital expenditures (including R&D and acquisitions)

**Core idea:** Net cap ex is capital expenditures minus depreciation — the part of investment that is not already paid for by the depreciation cash flow. It is the larger half of reinvestment for most firms, and it can never be assumed independently of growth: a firm growing fast must spend more than it depreciates, and a firm assuming high growth with zero net cap ex is assuming free growth. Reported cap ex is also systematically incomplete: two big categories of investment are hidden elsewhere. R&D is expensed on the income statement, and acquisitions are buried in the investing section of the cash-flow statement (and, under old pooling accounting, did not appear as spending at all). Adding both back can multiply true reinvestment several-fold.

**Formulas:**
- Net Capital Expenditures = Capital Expenditures − Depreciation.
- Adjusted for R&D: `Adjusted net cap ex = Net cap ex + Current-year R&D expense − Amortization of the research asset`.
- Adjusted for acquisitions: `Adjusted net cap ex = Net cap ex + Acquisitions of other firms − Amortization of those acquisitions`.
- Combined: `Adjusted net cap ex = (Cap ex − Depreciation) + R&D − R&D amortization + Acquisitions − Acquisition amortization`.
- Reinvestment (firm level) = Adjusted net cap ex + Change in non-cash working capital.
- Reinvestment rate = Reinvestment / EBIT(1−t); and by the fundamental growth identity, `Reinvestment rate = g / ROC` — see [[fundamental-growth-operating]].
- Stable-growth net cap ex + change in WC = `(g / ROC) × EBIT(1−t)` in the stable year.
- Sector-ratio estimator (when you cannot forecast cap ex directly): `Cap ex = (sector Cap Ex/Depreciation ratio) × Depreciation`, or `Net cap ex = (sector Net CapEx/Sales) × Sales`, or `Net cap ex = (sector Net CapEx/EBIT(1−t)) × EBIT(1−t)`.
- Sales-to-capital estimator (the young/changing-margin firm route): `Reinvestment_t = (Revenue_t − Revenue_(t−1)) / (Sales-to-capital ratio)` — see [[top-down-revenue-growth]].

**Procedure:**
1. Take cap ex and depreciation **from the statement of cash flows**, not the income statement footnotes; net them.
2. Find acquisitions in the investing section of the cash-flow statement, usually under "other investing activities". Add them to cap ex. Because most firms do not acquire every year, use a **normalized (multi-year average) acquisition figure**, not one year's.
3. If you capitalized R&D ([[rnd-capitalization]]), add current R&D to cap ex and the research-asset amortization to depreciation. Note: amortization of acquisition goodwill is usually already inside reported depreciation & amortization — do not add it twice.
4. Check whether the resulting net cap ex is consistent with your growth assumption. Compute the implied reinvestment rate and the implied ROC (`g = reinvestment rate × ROC`). If the implied ROC is implausible for the sector, the net cap ex assumption is wrong, not the growth.
5. Choose the forecasting method:
   - Mature, stable-margin firm: reinvestment rate × EBIT(1−t), with the reinvestment rate anchored on history and on `g/ROC`.
   - Firm with changing margins or negative income: sales-to-capital ratio on the revenue change.
   - No firm-specific basis: sector Cap Ex/Depreciation or Net CapEx/Sales ratios.
6. In the stable-growth phase, set net cap ex + change in WC = `(g/ROC) × EBIT(1−t)`. The classic "cap ex = depreciation, no working capital needs" assumption is only internally consistent with **zero real growth** — see [[terminal-value]].

**Reference data:**

Stable-growth cap ex, three documented approaches (in the order Damodaran ranks them):
1. **Net cap ex = 0** (cap ex = 100% of depreciation). Most common in stable growth and the most dangerous when paired with positive growth; defensible only when stable growth is approximately zero.
2. **Industry-average ratios** — set the firm's Cap Ex/Depreciation (or Net CapEx/Sales, or Net CapEx/EBIT(1−t)) to the sector average.
3. **Fundamental** — reinvestment rate = `g / ROC`. This is the only one that is internally consistent by construction.

Selected sector Cap Ex/Depreciation ratios (Value Line sector averages; late-1990s vintage — treat as illustrative defaults and refresh from current data):
| Sector | Cap Ex/Deprec'n | Net CapEx/Sales | Net CapEx/EBIT(1−t) |
|---|---|---|---|
| Advertising | 0.79 | −0.009 | −0.098 |
| Aerospace/Defense | 0.89 | −0.004 | −0.039 |
| Air Transport | 1.47 | 0.024 | 0.248 |
| Auto & Truck | 1.12 | 0.008 | 0.073 |
| Cable TV | 1.30 | 0.056 | 0.212 |
| Computer & Peripherals | 1.30 | 0.012 | 0.111 |
| Computer Software & Svcs | 1.15 | 0.011 | 0.062 |
| Drug | 1.08 | 0.005 | 0.020 |
| Electric Utility (East) | 0.90 | −0.010 | −0.049 |
| Grocery | 1.78 | 0.015 | 0.369 |
| Hotel/Gaming | 3.12 | 0.099 | 0.766 |
| Petroleum (Integrated) | 1.55 | 0.029 | 0.254 |
| Railroad | 2.08 | 0.084 | 0.480 |
| Restaurant | 2.72 | 0.086 | 0.638 |
| Retail Building Supply | 3.96 | 0.039 | 0.711 |
| Retail Store | 1.57 | 0.011 | 0.200 |
| Semiconductor | 1.86 | 0.073 | 0.381 |
| Steel (General) | 2.40 | 0.048 | 0.637 |
| Telecom. Services | 1.44 | 0.052 | 0.206 |
| Water Utility | 2.40 | 0.166 | 0.662 |

(Negative Net CapEx ratios occur where sector cap ex is below depreciation — shrinking or asset-light sectors.)

**Worked example — Cisco, fiscal 1999 ($ millions):**

Cisco's 1999 acquisitions, from the cash-flow statement:
| Acquired | Method | Price |
|---|---|---|
| GeoTel | Pooling | 1,344 |
| Fibex | Pooling | 318 |
| Sentient | Pooling | 103 |
| American Internet | Purchase | 58 |
| Summa Four | Purchase | 129 |
| Clarity Wireless | Purchase | 153 |
| Selsius Systems | Purchase | 134 |
| PipeLinks | Purchase | 118 |
| Amteva Tech | Purchase | 159 |
| **Total** | | **2,516** |

Building adjusted net cap ex:
```
Capital expenditures (statement of cash flows)      584
− Depreciation (statement of cash flows)            486
= Net cap ex                                         98
+ R&D expense                                     1,594
− Amortization of the research asset                485
+ Acquisitions                                    2,516
= Adjusted net capital expenditures               3,723
```
Reported net cap ex of $98m understates true reinvestment by roughly **38x**. (Amortization of the acquisitions was already inside the reported depreciation figure.)

Second example — Disney FY2013 ($ millions): cap ex including acquisitions 5,239 − D&A 2,192 = net cap ex 3,629; plus change in non-cash working capital 103 = reinvestment 3,732; against after-tax operating income of 10,032 × (1 − 0.3102) = 6,920, giving a **reinvestment rate of 53.93%**.

**Determinism:**
- DETERMINISTIC: net cap ex from cap ex and depreciation; all three adjustment formulas given R&D, R&D amortization and acquisitions; the reinvestment rate; the stable-period `g/ROC` reinvestment; any sector-ratio estimate once the ratio is chosen.
- JUDGMENT: how many years to average acquisitions over (and whether this firm will keep acquiring at all); whether stock-funded acquisitions belong in cap ex; whether reported depreciation already contains acquisition amortization; which of the three stable-growth approaches is defensible; the sales-to-capital ratio for a young firm; whether the historical reinvestment rate is representative (Disney's was checked against prior years for outliers).

**Pitfalls:**
- Setting net cap ex independently of the growth rate. The two are joined at the hip by `g = reinvestment rate × ROC`.
- Using one year's acquisitions as a run-rate — most firms do not acquire every year.
- Missing acquisitions entirely because pooling-accounted deals never appear as cash spending.
- Double-counting acquisition amortization (once in reported depreciation, once again as an explicit subtraction).
- Assuming cap ex = depreciation in the terminal year while assuming positive real growth. That is growth for free.
- Taking cap ex from the income statement/footnote rather than the cash-flow statement.

**Sources:**
- valpacket1spr21 p.140-143
- valpacket1spr20 p.137-140
- cfpacket2spr20 p.236 (Disney FY2013 net cap ex and reinvestment rate), p.247 (reinvestment rate x ROC)
- spreadsheet:cpxest.xls — three stable-growth cap-ex approaches; `reinvestment rate = g/ROC` cell; Table 1 sector Cap Ex/Depreciation, Net CapEx/Sales and Net CapEx/EBIT(1−t) ratios
- spreadsheet:R&DConv.xls — adjusted cap ex = cap ex + current R&D; adjusted D&A = D&A + amortization
- spreadsheet:fcffsimpleginzu.xlsx — reinvestment row driven by the sales-to-capital ratio

**Related:** [[rnd-capitalization]], [[operating-lease-capitalization]], [[non-cash-working-capital]], [[fcff]], [[fundamental-growth-operating]], [[top-down-revenue-growth]], [[terminal-value]], [[return-on-invested-capital]]

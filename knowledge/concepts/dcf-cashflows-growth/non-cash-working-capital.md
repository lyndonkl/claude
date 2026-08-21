# Non-cash working capital as reinvestment

**Core idea:** The second half of reinvestment is the cash tied up in working capital as a firm grows. The accounting definition (current assets minus current liabilities) is the wrong one for valuation, because it includes cash (which is valued separately and is not an operating asset) and short-term debt (which is a financing item). The valuation definition is **non-cash working capital**: non-cash current assets minus non-debt current liabilities. Year-to-year changes in this number are extremely volatile, so it should be forecast as a **percent of revenues**, benchmarked against the industry, rather than extrapolated from the most recent year's change. In some sectors — retail, distribution, manufacturing — working-capital investment is the larger part of reinvestment.

**Formulas:**
- Accounting working capital = Current assets − Current liabilities.
- **Non-cash working capital (NCWC)** = (Non-cash current assets) − (Non-debt current liabilities) = (Inventory + Accounts receivable + other non-cash current assets) − (Accounts payable + other non-debt current liabilities).
  - Excluded from assets: cash and marketable securities. Excluded from liabilities: short-term debt and the current portion of long-term debt.
- Working capital ratio `w = NCWC / Revenues`.
- Forecast investment in working capital in year t = `w × (Revenue_t − Revenue_(t−1))`.
- Actual change (historical) = `NCWC_t − NCWC_(t−1)`; a positive change is a cash **outflow** (reinvestment).
- Contribution to reinvestment: Reinvestment = Net cap ex + Change in non-cash working capital.
- Combined-with-cap-ex shortcut for young firms: `Reinvestment_t = (Revenue_t − Revenue_(t−1)) / Sales-to-capital ratio` folds working capital and cap ex into one number — see [[top-down-revenue-growth]].

**Procedure:**
1. Build NCWC from the balance sheet for the last several years: strip cash out of current assets, strip all interest-bearing debt out of current liabilities.
2. Express NCWC as a percent of revenues for each year. Compute the 3-year (or 5-year) average and the industry average.
3. **Do not** forecast off the most recent year's dollar change — it is noise. Pick a forward `w` by triangulating the current ratio, the firm's own multi-year average, and the industry average. Damodaran's practice is to move an outlier firm partway toward the industry.
4. Apply `w` to each year's revenue change to get the working-capital investment for that year.
5. Handle negative working capital deliberately. A firm with negative NCWC (payables exceed receivables + inventory, e.g. an early-stage e-tailer or a subscription business) generates cash as it grows, and the faster it grows the more cash it generates. Assuming that persists forever is a strong assumption; the usual response is to fade it toward zero or a small positive number.
6. Do not decompose into inventory / receivables / payables / deferred taxes unless you have firm-specific information that lets you actually forecast the pieces. Detail without information adds no accuracy.
7. Cross-check the resulting reinvestment against the growth rate you are assuming (`g = reinvestment rate × ROC`).

**Reference data:**

Worked judgment calls on the working-capital ratio (Damodaran's own forecasts):
| Item | Amazon | Cisco | Motorola |
|---|---|---|---|
| Revenues ($m) | 1,640 | 12,154 | 30,931 |
| Non-cash WC ($m) | −419 | −404 | 2,547 |
| NCWC as % of revenues | −25.53% | −3.32% | 8.23% |
| Change from last year ($m) | (309) | (700) | (829) |
| Average, last 3 years | −15.16% | −3.16% | 8.91% |
| Industry average | 8.71% | −2.71% | 7.04% |
| **Forecast w** | **3.00%** | **0.00%** | **8.23%** |

Reasoning behind each: Amazon's −25.5% is rejected as unsustainable and pulled most of the way toward the industry's +8.71%, landing at a modest +3%. Cisco is set at 0% — between its own slightly negative history and the industry's −2.71%. Motorola's current 8.23% is close to both its 3-year average and the industry, so it is kept unchanged.

Industry NCWC-as-percent-of-revenues figures are published in Damodaran's industry-average datasets (the same tables that carry unlevered betas, sales-to-capital and cost of capital), with a whole-market figure of roughly 7% in the vintage used by the high-growth model and roughly 0–2% in later vintages.

**Worked example:** Take Motorola with `w = 8.23%` and a forecast revenue increase from $30,931m to $34,024m (+10%). Investment in working capital next year = `0.0823 × (34,024 − 30,931)` = `0.0823 × 3,093` = **$254.5m** of reinvestment. If that firm's net cap ex is $700m, total reinvestment is $954.5m; against after-tax operating income of, say, $2,000m, the reinvestment rate is 47.7%.

Contrast: Cisco at `w = 0%` invests nothing in working capital regardless of how fast revenues grow, so all of its reinvestment is net cap ex (which for Cisco 1999 was overwhelmingly R&D and acquisitions — see [[net-capital-expenditures]]).

**Determinism:**
- DETERMINISTIC: NCWC from balance-sheet line items; NCWC as a percent of revenues; historical changes; the multi-year and industry averages; the forecast investment `w × ΔRevenue` once `w` is chosen.
- JUDGMENT: choosing `w`. This requires the firm's own multi-year ratio history, the industry average, and a view on whether the business model (negative working capital, extended payables, inventory-light) is durable. Also judgment: whether to decompose the components at all, and how fast to fade a negative ratio toward zero.

**Pitfalls:**
- Using accounting working capital (leaving cash and short-term debt in). This makes working-capital "investment" swing with the cash balance and with debt maturity, neither of which is operating.
- Extrapolating the latest year's dollar change. The Amazon/Cisco/Motorola table exists precisely to show how erratic those changes are (−309, −700, −829).
- Locking a large negative NCWC ratio in forever, so that growth becomes a perpetual cash source that grows with growth.
- Decomposing into inventory, receivables, deferred taxes etc. without any information to forecast them separately.
- Double-counting working capital when you are also using a sales-to-capital ratio — the sales-to-capital reinvestment already includes it.
- Forgetting that a *positive* change in NCWC is a cash outflow.

**Sources:**
- valpacket1spr21 p.144-146
- valpacket1spr20 p.141-143
- valpacket1spr21 p.117-119 / valpacket1spr20 p.114-116 (working capital as a component of reinvestment in FCFF/FCFE)
- spreadsheet:higrowth.xls — `Input Sheet(assumtion)` working-capital-as-%-of-revenues override and the ΔWC row in `DCFValuation`
- spreadsheet:fcffsimpleginzu.xlsx — working capital folded into reinvestment via the sales-to-capital ratio; `Industry Averages(US)` carries "Non-cash WC as % of Revenues"

**Related:** [[net-capital-expenditures]], [[fcff]], [[fcfe]], [[top-down-revenue-growth]], [[fundamental-growth-operating]], [[terminal-value]], [[return-on-invested-capital]]

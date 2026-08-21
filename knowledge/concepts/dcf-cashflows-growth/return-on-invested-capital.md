# Return on invested capital (ROIC) and its measurement limits

**Core idea:** ROIC is the single number a DCF leans on hardest. It is the proxy for the return the firm earns on its existing assets and, by extension, on the assets it is about to build: it drives fundamental growth (`g = reinvestment rate x ROIC`), it decides whether growth creates or destroys value (`ROIC vs cost of capital`), and it fixes the reinvestment rate in the terminal year (`g/ROIC`). It is also an accounting ratio built from two badly measured numbers, and there are six specific ways it can mislead. Anyone using ROIC as an economic return needs to know which of the six apply to the company in front of them.

**Formulas:**
- `ROIC = After-tax operating income / Capital invested in existing assets`
- `After-tax operating income = Trailing-12-month operating income × (1 − effective tax rate paid over those 12 months)`, computed on **adjusted** operating income (leases and R&D capitalized, one-time items removed).
- `Invested capital = Book value of equity + Book value of debt − Cash & cross holdings`, plus the research asset and the leased asset when those adjustments are made. Measure at the **start** of the period so that the numerator's income was actually earned on it.
- Equity analogue: `ROE = Net income / Book value of equity`; `Non-cash ROE = Non-cash net income / (BV equity − cash)`.
- Leverage decomposition: `ROE = ROC + (D/E) × [ROC − i(1 − t)]`.
- Marginal (incremental) ROIC over a forecast: `Marginal ROIC = Δ EBIT(1−t) over n years / Δ Invested capital over n years` — a useful diagnostic on whether the forecast's implied returns are plausible.
- Implied ROIC from a cash-flow forecast (terminal-value consistency check):
  - `Reinvestment rate embedded = 1 − FCFF_terminal / EBIT(1−t)_terminal`
  - `Implied perpetual ROIC = g / Reinvestment rate embedded`
  - `Reinvestment rate that would make ROIC = cost of capital = g / Cost of capital`

**Procedure:**
1. Build the numerator from adjusted, trailing-12-month operating income net of the effective tax rate actually paid.
2. Build the denominator as beginning-of-period book equity plus book debt minus cash and cross holdings, adding back the research asset and lease asset if you capitalized them.
3. Run the six-distortion checklist (Reference data). For each one that applies, decide whether to correct the number or to discount your confidence in it.
4. Compare the computed ROIC to the firm's own multi-year history and to the industry average. A ROIC far above the industry that you cannot explain by a durable competitive advantage is a signal to fade it, not to extrapolate it.
5. Feed it into growth (`g = reinvestment rate × ROIC`), into the value test (`ROIC vs cost of capital`), and into the terminal reinvestment rate (`g/ROIC`).
6. After building the forecast, run the reverse check: take the terminal-year FCFF and EBIT(1−t), back out the embedded reinvestment rate and the implied perpetual ROIC, and ask whether that return is defensible forever.
7. Compute the marginal ROIC across the whole explicit forecast. If it implies returns on *new* capital far above the firm's historical returns, your growth and reinvestment assumptions disagree with each other.

**Reference data:**

The six ways ROIC misleads:
| # | Distortion | Which side | Effect |
|---|---|---|---|
| 1 | **Abnormal earnings** — the last 12 months were unusually good or bad | Numerator | ROIC is a snapshot of a cycle position, not a return |
| 2 | **Accounting misclassification** — R&D expensed, leases treated as operating | Both | Understates income *and* understates invested capital |
| 3 | **Unusual items** — one-time gains/charges in operating income | Numerator | Random noise in the return |
| 4 | **Life-cycle effect** — young firms and infrastructure firms have not yet earned on their investment | Both | Current earnings say nothing about long-run potential |
| 5 | **Accounting write-offs** — writing off past mistakes shrinks the capital base | Denominator | Flatters ROIC; the worse the past, the better the ratio looks |
| 6 | **Inflation** — book values of old assets are unadjusted | Denominator | Understates capital invested; overstates ROIC for asset-heavy, long-lived-asset firms |

Empirical anchor on persistence: tracking the median ROIC of the 500 largest US public companies by revenue in cohorts formed in 1965, 1975, 1985 and 1995 and followed through 2004, ROIC is **sustainable over long periods** (roughly stable in an 8–12% band), while real revenue growth inevitably declines toward GDP growth. Implication: **fade growth faster than you fade excess returns.**

Industry-average ROC / ROIC is published in Damodaran's industry-average datasets alongside unlevered betas, sales-to-capital ratios and costs of capital, and is the natural benchmark. Whole-market after-tax ROC in the vintages used here runs roughly 12%.

**Worked example — the terminal-value consistency check:** A valuation produces terminal-year `EBIT(1−t) = 1,035` and terminal-year `FCFF = 750`, with perpetual growth of **4%** and a perpetual cost of capital of **9.35%**.
```
Embedded reinvestment rate = 1 − 750/1,035        = 27.54%
Implied perpetual ROIC     = 0.04 / 0.2754        = 14.53%
Reinvestment rate if ROIC = cost of capital
                           = 0.04 / 0.0935        = 42.78%
```
The forecast quietly assumes the firm earns **14.53% on capital forever** against a 9.35% cost of capital — value-creating excess returns in perpetuity. That may be defensible for a firm with a durable moat; it is not defensible by default. Forcing ROIC to the cost of capital would require reinvesting 42.78% of after-tax operating income, cutting terminal FCFF from 750 to `1,035 × (1 − 0.4278) = 592`.

Second example — Disney FY2013 ($ millions): `ROC = 10,032 × (1 − 0.361) / (41,958 + 16,328 − 3,387) = 12.61%` against a cost of capital of 7.81%. In the terminal phase the ROC is dropped to **10%** (still above the 7.29% stable cost of capital, on the argument that Disney's brand advantages will not have fully dissipated by year 10), which forces a stable reinvestment rate of `2.5%/10% = 25%`.

Third example — SAP with and without R&D capitalized (EUR m): `1,285/(3,768 + 530) = 29.9%` conventional versus `1,402/(6,782 + 530) = 19.2%` with the research asset on the books. Distortion #2 in one line.

**Determinism:**
- DETERMINISTIC: ROIC from adjusted after-tax operating income and invested capital; ROE and the leverage decomposition; the marginal ROIC over a forecast; the embedded reinvestment rate and implied perpetual ROIC from a terminal-year FCFF; the ROIC-neutral reinvestment rate `g/cost of capital`.
- JUDGMENT: whether the trailing 12 months are representative; how much of the six distortions to correct and how; whether a high ROIC reflects a moat that will persist or an accounting artifact that will not; the fade path from current ROIC to terminal ROIC; whether to allow excess returns in perpetuity at all.

**Pitfalls:**
- Using ROIC as an economic return without checking the six distortions.
- Beginning-vs-end-of-year capital mismatch, which mechanically biases the ratio for a growing firm.
- Leaving cash in invested capital (the numerator excludes interest income, so the denominator must exclude the cash that produced it).
- Rewarding a serial write-off firm: every write-off makes next year's ROIC look better.
- Reading a very high ROIC in an asset-heavy firm with old assets as a real advantage; it may just be unindexed book values.
- Assuming ROIC must equal the cost of capital in perpetuity — the empirical evidence is that excess returns persist longer than growth does. Assuming it *always* exceeds the cost of capital is the opposite error.
- Never running the reverse check, and so shipping a valuation with an implied perpetual ROIC nobody looked at.

**Sources:**
- valpacket1spr21 p.188, p.191, p.206-208, p.210
- valpacket1spr20 p.185, p.188, p.202-206
- valpacket1spr21 p.132 / valpacket1spr20 p.129 (ROC before and after R&D capitalization)
- valpacket1spr21 p.127 / valpacket1spr20 p.124 (ROC before and after lease capitalization)
- cfpacket2spr20 p.247, p.253-254, p.262-263 (Disney and Vale ROC; stable-period ROC choice)
- spreadsheet:ImpliedROCROE.xls — embedded reinvestment rate, implied perpetual ROC/ROE, ROC-neutral reinvestment rate
- spreadsheet:fcffsimpleginzu.xlsx — ROIC row, `Diagnostics` marginal-ROIC calculation, terminal ROC defaulting to the terminal cost of capital

**Related:** [[fundamental-growth-operating]], [[fundamental-growth-equity]], [[value-of-growth]], [[terminal-value]], [[rnd-capitalization]], [[operating-lease-capitalization]], [[net-capital-expenditures]], [[fcff-forecast-engine]], [[cost-of-capital]]

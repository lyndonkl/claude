# Top-down growth: revenues, target margin, sales-to-capital

**Core idea:** The fundamental growth equations (`g = reinvestment rate x return`) assume a sustainable return exists. They break down completely for a firm with negative operating income (no meaningful return) or with margins that are expected to change (today's return is not tomorrow's). For those firms — young companies, turnarounds, disruptors, money-losers — you forecast the income statement from the top instead: project **revenues**, project a **path of operating margins** converging on a target, and convert growth into **reinvestment** with a sales-to-capital ratio. Everything else (EBIT, taxes, FCFF, invested capital, ROIC) falls out of those three choices.

**Formulas:**
- `Revenue_t = Revenue_(t−1) × (1 + g_t)`
- Margin convergence, linear to a target by a chosen convergence year `Y`:
  `Margin_t = Target − (Target − Margin_start) / Y × (Y − t)`, and `Margin_t = Target` once `t >= Y`.
- Margin convergence, geometric "speed of convergence" form (closing a fraction `s/(1+s)` of the remaining gap each year):
  `Margin_t = Target − (Target − Margin_(t−1)) / (1 + 1/s)`. With `s = 1.5` the gap shrinks by 60% a year.
- `EBIT_t = Revenue_t × Margin_t`
- `Reinvestment_t = (Revenue_t − Revenue_(t−1)) / Sales-to-capital ratio`
  - The sales-to-capital ratio is dollars of revenue generated per dollar of invested capital. It bundles net cap ex, acquisitions, capitalized R&D and the change in working capital into one number.
- `Invested capital_t = Invested capital_(t−1) + Reinvestment_t`
- `ROIC_t = EBIT_t × (1 − t) / Invested capital_t`
- `FCFF_t = EBIT_t × (1 − t) − Reinvestment_t`
- Market-share sizing of revenues: `Revenue at year T = Market size today × (1 + g_market)^T × Target market share at year T`; the implied CAGR between two milestones = `(Rev_b / Rev_a)^(1/(b−a)) − 1`.

**Procedure:**
1. **Step 1 — revenue growth.**
   a. Size the total addressable market for the business model, and grow it at a market growth rate.
   b. Estimate the market share the firm can attain, at explicit milestones (e.g. year 5 and year 10). Convert to revenues and back out the implied CAGR.
   c. Taper the growth rate as the firm gets larger — high percentage growth off a large base is arithmetically implausible.
   d. Sanity-check the **absolute** revenue level in the final year against the market size and against comparable mature companies. "Would this company be as big as X?" is the test.
2. **Step 2 — operating margins.**
   a. Choose a **target margin** the firm converges to, anchored on mature firms with the same business model (not on the firm's own losses today). Use a percentile of the peer distribution, and say which.
   b. Choose a convergence path: linear to the target by a stated year, or a geometric speed-of-convergence.
   c. Multiply revenue by margin to get EBIT each year.
3. **Step 3 — reinvestment.**
   a. Choose a sales-to-capital ratio from the firm's own capital efficiency and the industry average (industry sales-to-capital figures are published in Damodaran's industry datasets). It may vary by phase — asset-light early growth then heavier build-out, or the reverse.
   b. `Reinvestment = change in revenues / sales-to-capital`. This is the only capital number you need.
4. **Taxes.** Carry losses forward; no tax until the NOL is exhausted, then ramp to the target/marginal rate ([[tax-rate-and-nols]]).
5. **FCFF and diagnostics.** `FCFF = EBIT(1−t) − reinvestment` — deeply negative in the early years for a money-loser, and that is the point. Accumulate invested capital and compute ROIC each year; the ROIC path is the honesty check on whether the story hangs together.
6. **Close it.** Fade the growth rate to the terminal rate, fade the cost of capital toward a mature level, and set the terminal reinvestment rate to `g/ROC` ([[terminal-value]]).

**Reference data:**

The three-step framework in one line: **(1) revenue growth -> (2) target operating margin and a path to it -> (3) capital needed, via a sales-to-capital ratio.** Use it whenever operating income is negative *or* margins are expected to change.

Sales-to-capital ratios used in the course cases: Tesla 1.55 (2015); Baidu 2.64 (2013); Airbnb 2.00 (2020, base year 1.92); a specialty retailer in the high-growth template 3.02; SK Innovation 10 in year 1, 5 in years 2–5, 1.5 in years 6–10 (the ratio can and often should vary by phase). Industry-average sales-to-capital ratios span roughly 0.1 (REITs, financial services) to 5–7 (human resources, food wholesalers, retail/wholesale food).

Anchoring a target margin: Airbnb's 25% target was anchored on Booking.com's pre-COVID operating margin of 35.48% for the same intermediary business model; Tesla's 12% target was the **75th percentile** of high-end auto companies; Baidu's 35% target was a *decline* from its current 48.72% as competition arrived.

**Worked example — Airbnb, November 2020 ($ thousands), sales-to-capital 2.00, target tax rate 25%:**

| Year | Revenue growth | Revenues | Operating margin | EBIT | EBIT(1−t) | Reinvestment | FCFF | Invested capital | ROIC |
|---|---|---|---|---|---|---|---|---|---|
| Base | — | 3,625,731 | −13.69% | (496,542) | (496,542) | — | — | 1,370,158 | −36.24% |
| 1 | 40.00% | 4,691,698 | −10.00% | (469,170) | (469,170) | 532,984 | (1,002,153) | 1,903,142 | −24.65% |
| 2 | 25.00% | 5,989,797 | −3.00% | (179,694) | (179,694) | 649,049 | (828,743) | 2,552,191 | −7.04% |
| 3 | 25.00% | 7,565,479 | 0.50% | 37,827 | 37,827 | 787,841 | (750,014) | 3,340,033 | 1.13% |
| 4 | 25.00% | 9,554,641 | 4.00% | 382,186 | 382,186 | 994,581 | (612,395) | 4,334,613 | 8.82% |
| 5 | 25.00% | 12,065,542 | 7.50% | 904,916 | 777,799 | 1,255,450 | (477,651) | 5,590,064 | 13.91% |
| 6 | 20.40% | 14,674,089 | 9.52% | 1,397,269 | 1,047,952 | 1,304,274 | (256,322) | 6,894,337 | 15.20% |
| 7 | 15.80% | 17,163,026 | 13.39% | 2,298,389 | 1,723,792 | 1,244,469 | 479,323 | 8,138,806 | 21.18% |
| 8 | 11.20% | 19,274,804 | 17.26% | 3,327,026 | 2,495,269 | 1,055,889 | 1,439,380 | 9,194,695 | 27.14% |
| 9 | 6.60% | 20,748,969 | 21.13% | 4,384,362 | 3,288,271 | 737,082 | 2,551,189 | 9,931,777 | 33.11% |
| 10 | 2.00% | 21,370,016 | 25.00% | 5,342,504 | 4,006,878 | 310,524 | 3,696,354 | 10,242,301 | 39.12% |
| Terminal | 2.00% | 21,797,416 | 25.00% | — | — | — | — | — | — |

Note the structure: growth starts at 40%, plateaus at 25% for four years, then tapers linearly to 2% (the economy rate) by year 10; the margin walks from −10% to the 25% target; reinvestment is always `ΔRevenue/2.00`; losses are carried forward so the first tax appears in year 5; FCFF is negative for six years and then turns.

Second example — Tesla, July 2015 ($ millions), sales-to-capital 1.55: revenues grow 65% a year for five years then taper to 2.75%, reaching **$79.5 billion** by year 10 — explicitly benchmarked as "the revenues of a successful high-end auto company (Volvo, Audi, BMW)". Margins go from −1.08% to the 12% target (75th percentile of high-end autos). Reinvestment = ΔRevenue/1.55, so year 5 reinvestment is 9,700.65/1.55 = 6,258.48 and FCFF is −5,384.81. ROIC climbs from −2.09% to 12.15%; the cost of capital declines from 8.74% to 8.00% as the firm matures.

Third example — market-share sizing: a firm with revenue 100 in a market of 100,000 growing 3% a year, targeting **2.5% share by year 5** and **6% by year 10**. Year-5 revenue = `100,000 × 1.03^5 × 0.025 = 2,898`; year-10 revenue = `100,000 × 1.03^10 × 0.06 = 8,063`. Implied CAGRs: **96.1%** for years 1–5, **22.7%** for years 6–10, **55.1%** over the decade. Stating the share assumptions is far more honest than asserting a 55% growth rate.

**Determinism:**
- DETERMINISTIC: given the growth path, the margin path (linear or speed-of-convergence), the sales-to-capital ratio and the tax rule, the entire table — revenues, EBIT, taxes, EBIT(1−t), reinvestment, FCFF, invested capital and ROIC — is mechanical. So is the market-share revenue sizing and its implied CAGRs.
- JUDGMENT: the total market size and its growth; the attainable market share; the taper schedule; the target margin and which peer percentile justifies it; how fast margins converge; the sales-to-capital ratio (and whether it changes by phase); the target tax rate.

**Pitfalls:**
- Forecasting a percentage growth rate without ever checking the absolute revenue level it implies against the size of the market.
- Anchoring the target margin on the firm's current (loss-making) margin instead of on mature firms with the same business model.
- Holding the growth rate flat and then dropping it in a cliff to the terminal rate — taper it.
- Forgetting the NOL, and taxing a firm that has years of accumulated losses.
- Double-counting working capital: the sales-to-capital reinvestment already includes it, so do not subtract ΔWC again.
- Choosing a sales-to-capital ratio so high that the firm grows to tens of billions of revenue on almost no capital, then reporting a triumphant ROIC.
- Being surprised by deeply negative FCFF in the early years. That is the correct output; it is what the equity issuance or cash burn has to fund.
- Ignoring the ROIC path. If ROIC ends at 39% and the sector earns 12%, the story needs a moat that justifies it.

**Sources:**
- valpacket1spr21 p.192-196
- valpacket1spr20 p.189-193
- cfpacket2spr20 p.248-249 (three-step approach; Baidu 10-year FCFF forecast at sales-to-capital 2.64), p.261
- spreadsheet:revgrowth.xls — market-share approach to sizing revenues and implied CAGRs
- spreadsheet:higrowth.xls — revenue path, speed-of-convergence margin path, sales-to-capital reinvestment, NOLs, converging beta/debt ratio
- spreadsheet:fcffsimpleginzu.xlsx — the same machinery in its current form (see [[fcff-forecast-engine]])

**Related:** [[fcff-forecast-engine]], [[normalizing-depressed-earnings]], [[fundamental-growth-operating]], [[tax-rate-and-nols]], [[net-capital-expenditures]], [[non-cash-working-capital]], [[terminal-value]], [[return-on-invested-capital]], [[historical-growth]], [[young-company-valuation]]

# Reinvestment from the sales-to-capital ratio

**Core idea:** Growth is never free. When a company has no meaningful capex or depreciation history — a young firm, a firm in transition, a firm whose accounting hides its real investment — you cannot forecast reinvestment line by line. Instead you assume every extra dollar of revenue needs a fixed amount of capital, so reinvestment falls out of the revenue forecast. The ratio that links them is the sales-to-capital ratio. Rolling reinvestment into an invested-capital balance also gives you a free consistency check: the implied return on capital each year. If that implied return drifts to an absurd level, your growth and reinvestment assumptions contradict each other.

**Formulas:**
- `Reinvestment_t = (Revenue_t − Revenue_{t−1}) / (Sales/Capital ratio)`.
- `Invested capital_t = Invested capital_{t−1} + Reinvestment_t`.
- `Imputed ROC_t = EBIT(1−t)_t / Invested capital_{t−1}` (beginning-of-year capital).
- Base invested capital = `Book equity + Book debt − Cash`, plus the research asset if R&D is capitalized, plus the lease-debt asset if leases are capitalized.
- Marginal ROIC on the forecast = `(EBIT(1−t)_10 − EBIT(1−t)_base) / Σ_{t=1..10} Reinvestment_t`.
- Terminal-year reinvestment from fundamentals: `Reinvestment_TY = EBIT(1−t)_TY × (g_stable / ROC_stable)`; equivalently the stable reinvestment rate is `RIR = g/ROC`.
- Inverted form used when you set the reinvestment rate instead: `Expected growth in EBIT(1−t) = Reinvestment rate × Return on capital`.

**Procedure:**
1. Pick the sales-to-capital ratio. Sources, in order of preference: the company's own current ratio (`Revenues / Invested capital`), its own multi-year average, the industry average (US or global), or a blend. Boeing (Mar 2020) used 3.79–3.80, its own current ratio. Amazon 2000 used 3.00; Amazon 2019 used 5.95; Amazon 2020 used 1.95.
2. Compute reinvestment each year from the revenue change. If revenues **fall**, the formula releases capital (negative reinvestment) — correct for a shrinking firm; see [[declining-firm-valuation]]. Damodaran's Ginzu model floors year-1 reinvestment at zero when revenues decline, but allows negative reinvestment in years 2–10.
3. Roll invested capital forward and compute the imputed ROC each year.
4. Sanity-test the imputed ROC path against (a) the sector's return on capital and (b) the terminal ROC you assumed. If year-10 imputed ROC is wildly above the sector's, either the margin is too high, the sales-to-capital ratio is too generous, or the growth is unfinanced.
5. Report the marginal ROIC on the whole forecast. A marginal ROIC of 89% (Amazon 2019) or 75% (Boeing 2020) is a claim that new capital earns extraordinary returns — defend it or lower the sales-to-capital ratio.
6. In the terminal year, switch to fundamentals: `RIR = g/ROC`. Set terminal ROC equal to the terminal cost of capital unless you argue a durable competitive advantage. If `g ≤ 0`, terminal reinvestment is set to zero in the Ginzu model.

**Reference data:** Amazon January 2000 — reinvestment, capital and imputed ROC with a sales-to-capital ratio of 3.00 and starting invested capital of $487m.

| Year | Revenues | Δ Revenue | Sales/Cap | Reinvestment | Invested capital | EBIT(1−t) | Imputed ROC |
|---|---|---|---|---|---|---|---|
| Tr 12 mths | $1,117 | — | — | — | $487 | −$410 | — |
| 1 | $2,793 | $1,676 | 3.00 | $559 | $1,045 | −$373 | −76.62% |
| 2 | $5,585 | $2,793 | 3.00 | $931 | $1,976 | −$94 | −8.96% |
| 3 | $9,774 | $4,189 | 3.00 | $1,396 | $3,372 | $407 | 20.59% |
| 4 | $14,661 | $4,887 | 3.00 | $1,629 | $5,001 | $871 | 25.82% |
| 5 | $19,059 | $4,398 | 3.00 | $1,466 | $6,467 | $1,058 | 21.16% |
| 6 | $23,862 | $4,803 | 3.00 | $1,601 | $8,068 | $1,438 | 22.23% |
| 7 | $28,729 | $4,868 | 3.00 | $1,623 | $9,691 | $1,799 | 22.30% |
| 8 | $33,211 | $4,482 | 3.00 | $1,494 | $11,185 | $2,119 | 21.87% |
| 9 | $36,798 | $3,587 | 3.00 | $1,196 | $12,380 | $2,370 | 21.19% |
| 10 | $39,006 | $2,208 | 3.00 | $736 | $13,116 | $2,524 | 20.39% |
| TY | $41,346 | $2,340 | — | $807 | — | $2,688 | 20.00% (assumed) |

Sales-to-capital ratios used across the packet's cases: Amazon 2000 = 3.00; Amazon 2019 = 5.95; Amazon 2020 = 1.95; Boeing March 2020 = 3.79 (marginal ROIC 74.72%).

Reinvestment-rate form (used when ROC is the anchor rather than revenue growth): Hormel status quo RIR 19.14% × ROC 14.34% = 2.75% growth; Hormel restructured RIR 40% × ROC 14.00% = 5.60%; Amgen RIR 60% × ROC 16% = 9.6%; Tata Chemicals RIR 56.5% × ROC 10.35% = 5.85%; TCS RIR 56.73% × ROC 40.63% = 23.05%.

**Worked example:** Amazon year 4 (Jan 2000 valuation). Revenues rise from $9,774m to $14,661m, so ΔRevenue = $4,887m. Reinvestment = 4,887/3.00 = $1,629m. Invested capital goes from $3,372m to $5,001m. EBIT(1−t) of $871m against beginning capital of $3,372m gives an imputed ROC of 25.82% — high but not absurd for a retailer, and it settles back to about 20% by year 10, matching the assumed terminal ROC of 20%. FCFF that year = 871 − 1,629 = −$758m; that negative number is the equity the company must raise, and its present value is the dilution.

**Determinism:** DETERMINISTIC — (revenue path, sales-to-capital ratio, starting invested capital, EBIT(1−t) path) → reinvestment, invested capital, imputed ROC, marginal ROIC; and (g_stable, ROC_stable, terminal EBIT(1−t)) → terminal reinvestment. JUDGMENT: the choice of the sales-to-capital ratio itself (needs the company's own ratio, its history, and industry averages), the terminal ROC, and the verdict on whether an imputed ROC path is plausible.

**Pitfalls:**
- Forecasting revenue growth without any reinvestment — value appears from nowhere.
- Using a sales-to-capital ratio so high that the implied marginal ROIC is absurd; the ratio and the margin jointly determine returns.
- Forgetting that invested capital must include the research asset once R&D is capitalized ([[capitalizing-rd]]) and the lease asset once leases are capitalized — otherwise ROC is overstated.
- Computing imputed ROC on end-of-year rather than beginning-of-year capital and then comparing it with sector ROC computed the other way.
- Blocking negative reinvestment for a shrinking firm. A declining company genuinely releases working capital and real estate.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.303
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.299
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.311-312
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.325
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.294
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.290
- spreadsheet model doc: ginzu-fcff-corona.md — rows 8, 38–40 of the Valuation output sheet

**Related:** [[young-company-valuation]], [[declining-firm-valuation]], [[capitalizing-rd]], [[value-of-control-and-restructuring]], [[terminal-value]], [[return-on-invested-capital]], [[fcff-valuation]]

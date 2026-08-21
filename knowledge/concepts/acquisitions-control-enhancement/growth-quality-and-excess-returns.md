# Growth quality: when growing less is the answer

**Core idea:** Growth is not automatically good. It creates value only when the return on invested capital exceeds the cost of capital. For roughly half of all firms in the world it does not, and for those firms every extra dollar reinvested destroys value. Growth also differs sharply by *mode*. New-product market development creates far more value per dollar than expanding an existing market, and both beat fighting for share in a stable market. Acquisitions sit at the bottom of the ranking, typically destroying value. The practical consequence is uncomfortable: for many firms the value-maximizing plan is to shrink, return capital, and stop reinvesting.

**Formulas:**
- `Excess return = ROIC − WACC`. Value is created only when this is positive.
- `Expected growth = Reinvestment rate × ROIC`. If `ROIC < WACC`, raising the reinvestment rate raises growth *and* lowers value.
- Value created per dollar of growth varies by growth mode — see the reference table.
- Break-even: at `ROIC = WACC`, growth is value-neutral. It adds earnings but adds no value.

**Procedure:**
1. Measure the firm's ROIC: `EBIT(1−t) / Invested capital`, using a defensible measure of invested capital.
2. Measure its WACC.
3. Compute the excess return. Classify the firm into one of three buckets: `ROIC < WACC`, `ROIC ≈ WACC` (within a few percentage points), or `ROIC > WACC`.
4. If `ROIC < WACC`, do not model growth as a value driver. The value-enhancing actions are to cut reinvestment, divest sub-WACC assets, and return cash to shareholders.
5. If `ROIC ≈ WACC`, growth is roughly value-neutral. The firm should focus on levers 1 and 4 — cash flows from existing assets, and the cost of capital.
6. If `ROIC > WACC`, growth creates value, and the question becomes what *kind* of growth.
7. Rank the growth options by value created per incremental dollar, using the reference table. Prefer new-product market development. Treat acquisitions as the last resort.
8. Check the scale required. The table's second column shows how much revenue growth or acquisition size it takes to double a typical company's share price — the differences are enormous.
9. Feed the conclusion into the restructuring case. A low-ROIC firm's control value often comes from *reducing* reinvestment, not increasing it.

**Reference data:**

Value created by growth mode, consumer goods industry (McKinsey-style evidence):

| Category of growth | Shareholder value created per incremental $1M of growth | Revenue growth / acquisition size to double a typical company's share price ($B) |
|---|---|---|
| New-product market development | $1.75–2.00 | 5–6 |
| Expanding an existing market | $0.30–0.75 | 13–33 |
| Maintaining/growing share in a growing market | $0.10–0.50 | 20–100 |
| Competing for share in a stable market | −$0.25 to −$0.40 (negative) | n/m–25 |
| Acquisition (25th to 75th percentile) | −$0.50 to −$0.20 (negative) | n/m–50 |

Excess returns on capital (ROIC − WACC), non-financial-service firms, January 2020, percent of firms by region:

| Region | ROIC < WACC | ROIC close to WACC | ROIC > WACC |
|---|---|---|---|
| Africa and Middle East | 51.68% | 17.83% | 30.49% |
| Australia & NZ | 67.22% | 8.06% | 24.72% |
| Canada | 80.31% | 6.17% | 13.52% |
| China | 49.18% | 16.54% | 34.28% |
| EU & Environs | 47.38% | 16.21% | 36.41% |
| Eastern Europe & Russia | 50.96% | 18.73% | 30.30% |
| India | 47.66% | 14.85% | 37.49% |
| Japan | 34.24% | 23.11% | 42.65% |
| Latin America & Caribbean | 43.90% | 20.34% | 35.76% |
| Small Asia | 59.08% | 15.12% | 25.80% |
| UK | 46.54% | 13.46% | 40.00% |
| United States | 50.00% | 11.73% | 38.27% |
| **Global** | **52.05%** | **15.32%** | **32.63%** |

Read the global row carefully. A majority of firms worldwide earn less than their cost of capital. For them, the growth story in the pitch deck is a value-destruction story.

**Worked example:** Blockbuster in 2005 had an after-tax ROIC of 4.06% against a WACC of 6.17%. Excess return = `4.06% − 6.17% = −2.11%`. It belongs in the "ROIC < WACC" bucket that holds 50% of US firms.

The consequence shows in the restructuring. Damodaran does *not* fix Blockbuster by making it grow faster. He raises after-tax operating income from 163 to 249, which lifts ROIC to 6.20% — just above the 6.17% WACC. The same dollar reinvestment of 43 now represents a reinvestment rate of `43/249 = 17.32%` instead of 26.46%. Growth stays at 1.07% in both cases. Value per share still more than doubles, from $5.13 to $12.47, because the firm now converts far more of its earnings into free cash flow.

The lesson generalizes. When ROIC is below WACC, the fix is efficiency and less reinvestment, not more growth.

**Determinism:**
- DETERMINISTIC: ROIC, WACC and the excess return given financials; bucket classification against the thresholds; the value impact of any stated change in reinvestment rate or ROIC.
- JUDGMENT: how to measure invested capital. Leases, R&D capitalization and goodwill treatment all change ROIC materially. Whether the current ROIC is representative or depressed by a cyclical trough. Which growth mode a proposed initiative really is. Whether a sub-WACC business can be fixed or should be exited.

**Pitfalls:**
- Reading growth in earnings or revenues as value creation. Only excess-return growth creates value.
- Using a naive book invested capital without adjustments, which can make ROIC meaningless.
- Assuming the firm is in the top third. The global data says two-thirds of firms are not.
- Classifying an acquisition-driven plan as "growth" without noting that acquisitions occupy the bottom row of the value-per-dollar table.
- Failing to consider shrinking as a strategy. For a sub-WACC firm, returning capital is a value-enhancing action.
- Comparing ROIC to the cost of *debt* or to an accounting hurdle rate instead of WACC.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.136-137`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.136-137`

**Related:** [[paths-to-value-creation]], [[eva-and-dcf-equivalence]], [[restructured-value-and-value-of-control]], [[acquisition-strategy-design]], [[status-quo-valuation]], [[return-on-invested-capital]]

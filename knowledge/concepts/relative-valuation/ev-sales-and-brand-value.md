# EV/Sales, price-to-sales, and valuing a brand name

**Core idea:** Revenue multiples work where earnings multiples break. Revenues are always positive and less distorted by accounting choices than earnings or book value. The price of that robustness is a strong companion variable: the margin. EV/Sales is driven by the after-tax operating margin; price-to-sales is driven by the net margin. Two firms with the same sales are worth very different amounts if one converts 20% of revenue into operating profit and the other 3%. The margin link also gives a clean way to value a brand. A brand lets a firm charge more for the same product, so it shows up as a higher margin and a higher value-to-sales ratio. Value the firm twice — once with its own margin, once with a generic competitor's — and the difference is the brand.

**Formulas:**
- `Free Cash Flow to the Firm = EBIT(1 − t)(1 − Reinvestment Rate)`
- Stable growth: `EV/Sales = ATOM × (1 − RIR)/(WACC − g)`
- Two-stage:
```
Value/Sales₀ = After-tax Operating Margin ×
  { [(1 − RIR_growth)(1+g)(1 − (1+g)^n/(1+WACC)^n)]/(WACC − g)
  + [(1 − RIR_stable)(1+g)^n (1+gn)]/[(WACC − gn)(1+WACC)^n] }
```
- Equity analogue: `P/Sales₁ = Net Margin × Payout/(ke − g)`
- Brand value: `Value of brand name = [(V/S)_b − (V/S)_g] × Sales`

Symbols:
- ATOM = after-tax operating margin = EBIT(1−t)/Sales.
- RIR = reinvestment rate; RIR_growth and RIR_stable are the high-growth and stable-phase rates.
- g = growth in after-tax operating income for n years; gn = stable growth after year n.
- WACC = cost of capital; n = length of the high-growth period; t = tax rate.
- (V/S)_b = value-to-sales ratio with the brand; (V/S)_g = value-to-sales ratio of a generic-product firm.
- ke = cost of equity; Payout = dividends/net income.

**Procedure:**
1. Match the multiple to the margin. Enterprise value goes with the operating margin; equity value (price) goes with the net margin. Never mix.
2. Compute the after-tax operating margin, reinvestment rate, growth rate and cost of capital for the firm.
3. Compute the intrinsic EV/Sales from the formula and compare with the traded multiple.
4. Across a sector, plot the revenue multiple against margin and fit a line. Points far above the band are expensive for their margin; points below are cheap.
5. Check whether the current margin is the right one. If margins are depressed, in transition, or negative, the current-margin regression will mislead. Use expected margins or survival proxies instead ([[pricing-young-companies]]).
6. To value a brand: build a full DCF of the firm with its own margin. Rebuild the identical DCF with the after-tax operating margin of a credible generic producer, holding revenues, capital turnover, cost of capital, growth period and stable-phase assumptions fixed. Let the ROC and growth adjust as the margin changes, since ROC = margin × sales/capital and g = RIR × ROC.
7. Take the difference in firm values as the brand value.

**Reference data:**

Regional EV/Sales regressions (slide labelled January 2020, carried into the 2021 packet):

| Region | Regression | R² |
|---|---|---|
| United States | EV/Sales = 4.35 − 5.40 Tax Rate − 1.00 DFR + 7.80 g + 6.50 Op. Margin | 31.2% |
| Europe | EV/Sales = 1.69 + 1.70 Tax Rate + 2.20 DFR + 3.20 g + 6.70 Op. Margin | 13.2% |
| Japan | EV/Sales = 2.10 − 0.80 Tax Rate − 2.00 DFR + 9.30 g + 6.60 Op. Margin | 23.5% |
| Emerging Markets | EV/Sales = 3.48 − 2.20 Tax Rate − 1.00 DFR + 3.20 g + 5.40 Op. Margin | 14.6% |
| Australia, NZ & Canada | EV/Sales = 2.16 − 2.80 Tax Rate + 2.60 DFR + 5.70 g + 7.90 Op. Margin | 31.8% |
| Global | EV/Sales = 3.37 − 2.30 Tax Rate − 0.10 DFR + 5.20 g + 6.30 Op. Margin | 18.1% |

Definitions: g = expected revenue growth, near term (2 or 5 years); DFR = debt ratio; Operating Margin = Operating Income/Sales; Tax Rate = effective tax rate in the most recent year.

The operating-margin coefficient sits between 5.4 and 7.9 in every region. Margin is the dominant companion variable everywhere.

US grocery-store sector regressions of price-to-sales on net margin (see [[sector-regressions]] for the Whole Foods application): 2007 `PS = 0.07 + 10.49 × Net Margin` (R² 0.595); 2010 `PS = 0.06 + 11.43 × Net Margin` (R² 0.638); 2015 `PS = 0.557 + 8.50 × Net Margin` (R² 0.291).

Current sector anchors: the January-2022 US industry-averages dataset gives EV/Sales alongside the pre-tax operating margin and sales/capital ratio for every industry ([[industry-average-multiples]]).

**Worked example — Coca-Cola's brand (lecture case):** Value Coca-Cola twice, changing only the after-tax operating margin to that of Cott, a generic cola producer. All figures in $ millions.

| Input | Coca-Cola | With Cott margins |
|---|---|---|
| Current revenues | 21,962.00 | 21,962.00 |
| Length of high-growth period | 10 | 10 |
| Reinvestment rate | 50% | 50% |
| Operating margin (after-tax) | 15.57% | 5.28% |
| Sales/Capital (turnover) | 1.34 | 1.34 |
| Return on capital (after-tax) | 20.84% | 7.06% |
| Growth rate during period | 10.42% | 3.53% |
| Cost of capital during period | 7.65% | 7.65% |
| Stable growth rate | 4.00% | 4.00% |
| Stable return on capital | 7.65% | 7.65% |
| Stable reinvestment rate | 52.28% | 52.28% |
| Stable cost of capital | 7.65% | 7.65% |
| **Value of firm** | **79,611.25** | **15,371.24** |

Value of brand name = 79,611 − 15,371 = **$64,240 million**. Note the mechanics: ROC = margin × sales/capital (0.1557 × 1.34 = 20.84%), and growth = reinvestment rate × ROC (0.50 × 20.84% = 10.42%). Changing the margin therefore changes both the level of cash flow and the growth rate, which is why the value gap is so large.

**Determinism:** DETERMINISTIC — the intrinsic EV/Sales from margin, RIR, WACC, g, gn and n; both DCF values in the brand calculation once the input table is fixed; predicted values from the regional or sector regressions. JUDGMENT — choosing the generic comparable and its margin, deciding whether the current margin is sustainable, and setting the high-growth period.

**Pitfalls:**
- Pairing an enterprise-value numerator with a net margin, or a price numerator with an operating margin.
- Using revenue multiples as if they were margin-free. A low EV/Sales with a low margin is deserved.
- Regressing price-to-sales on *current* margins for firms whose value rests on *expected* margins. For internet stocks in early 2000 that regression produced R² of 0.04.
- Picking a "generic" comparable whose business model differs in more than branding; the whole margin gap then gets attributed to the brand.
- Forgetting that a margin change flows through to ROC and growth in a consistent DCF.

**Sources:**
- valpacket2spr21 p.48-50, p.98
- valpacket2spr20 p.48-50, p.96
- tables (Jan-2022 US industry averages: EV/Sales, pre-tax operating margin, sales/capital)

**Related:** [[intrinsic-multiple-derivation]], [[sector-regressions]], [[pricing-young-companies]], [[ev-ebitda-multiple]], [[cross-market-multiple-regressions]], [[industry-average-multiples]], [[dcf-valuation]], [[operating-margin-normalization]]

# Fundamental growth in operating income

**Core idea:** Operating income grows for exactly two reasons: the firm invests new capital and earns a return on it, and/or it earns a better return on the capital it already has. That gives `g = Reinvestment rate x ROC + efficiency growth`. This is the growth equation that belongs in an FCFF valuation, because it uses pre-debt earnings and total capital, so leverage cannot manufacture it. Its most useful implication is a discipline: reinvestment and growth are not independent assumptions. For any target growth rate, the required reinvestment is inversely proportional to the quality of the firm's investments — a high-ROC firm buys the same growth with far less capital.

**Formulas:**
- `Reinvestment rate = (Net capital expenditures + Change in non-cash working capital) / [EBIT × (1 − t)]`, where net cap ex includes capitalized R&D and normalized acquisitions.
- `ROC (ROIC) = EBIT × (1 − t) / (BV of equity + BV of debt − Cash)`, with capital measured at the **start** of the period.
- **Stable-return case:** `g_EBIT = Reinvestment rate × ROC`.
- **Changing-return case:** `g_EBIT = ROC_(t+1) × Reinvestment rate + (ROC_(t+1) − ROC_t) / ROC_t`.
  - Spread the efficiency term over the years the change takes: over n years, annualized efficiency growth = `[1 + (ROC_(t+n) − ROC_t)/ROC_t]^(1/n) − 1`.
- Inverted for planning: `Reinvestment rate = g / ROC`. This is the form used in the terminal year.
- General derivation: `Current earnings = Existing investment × Current ROI`; `Next period's earnings = Existing investment × Next ROI + New investment × ROI on new projects`; therefore `Change in earnings = Existing investment × (Change in ROI) + New investment × ROI on new projects`, and dividing by current earnings gives the growth equation.

**Procedure:**
1. Build adjusted EBIT (leases and R&D capitalized, one-time items removed) and adjusted invested capital (research asset and lease asset added, cash subtracted).
2. Compute the reinvestment rate: net cap ex (including R&D and normalized acquisitions) plus the change in non-cash working capital, over after-tax operating income. Check the last several years — a single year's reinvestment rate can be an outlier (this check is explicitly done in the Disney valuation).
3. Compute ROC on beginning-of-year invested capital. Interrogate it against the six ROIC distortions ([[return-on-invested-capital]]) before trusting it.
4. If you expect both to persist, `g = reinvestment rate × ROC`. Use this for the explicit forecast years.
5. If you expect the return to change — a turnaround, margin expansion, or fade toward the industry — add the efficiency term, annualized over the number of years the improvement takes. State the implicit assumption: new investments earn the *new* ROC immediately, while existing assets improve gradually.
6. Stress the result. Ask: is the ROC overstated by accounting? Is the reinvestment mostly acquisitions (goodwill that may not repeat at the same return)? Is the firm getting large enough that scale caps growth? Is the growth already in the price?
7. In the stable phase, invert: pick `g` and a perpetual `ROC`, and let `reinvestment rate = g/ROC` follow. Never set both independently.

**Reference data:**

Growth decision tree — operating income branch:
| Situation | Formula |
|---|---|
| Stable ROC | `g = ROC × Reinvestment rate` |
| Changing ROC | `g = ROC_(t+1) × Reinvestment rate + (ROC_(t+1) − ROC_t)/ROC_t` |
| Negative operating income or changing margins | Fundamentals break down -> use revenue growth, target margin, sales-to-capital ([[top-down-revenue-growth]]) |

Four standing worries about an extrapolated fundamental growth rate: (1) the ROC may be overstated by accounting; (2) the reinvestment may be mostly acquisitions, which may not repeat at the same return; (3) the firm is getting bigger, and scale makes percentage growth harder; (4) the firm is a market darling, so the growth is already in the price.

**Worked examples:**

*Cisco vs Motorola (stable-ROC version):*
| | Reinvestment rate | ROC | Expected EBIT growth |
|---|---|---|---|
| Cisco | 106.81% | 34.07% | `1.0681 × 0.3407` = **36.39%** |
| Motorola | 52.99% | 12.18% | `0.5299 × 0.1218` = **6.45%** |

Cisco's number is arithmetically correct and practically suspect on all four worries at once: its ROC was inflated by expensing R&D, its reinvestment was overwhelmingly acquisitions (see [[net-capital-expenditures]]), it was already very large, and it was the market's favourite stock.

*Motorola (changing-ROC version):* current ROC 12.18%, reinvestment rate 52.99%, ROC expected to rise to **17.22%** over 5 years (halfway to the industry average).
```
Growth from new investments = 0.1722 × 0.5299                       = 9.12%
Efficiency growth = [1 + (0.1722 − 0.1218)/0.1218]^(1/5) − 1        = 7.17%
Total expected growth                                                = 16.29%
```
versus only 6.45% on the stable-ROC assumption. Note what has been assumed: new investments earn 17.22% immediately, while existing assets improve gradually over five years.

*Disney FY2013 ($ millions):*
```
Reinvestment rate = (net cap ex 3,629 + ΔWC 103) / [10,032 × (1 − 0.3102)] = 53.93%
ROC = 10,032 × (1 − 0.361) / (BV equity 41,958 + BV debt 16,328 − cash 3,387) = 12.61%
Expected EBIT growth = 0.5393 × 0.1261 = 6.8% per year
```
(Note the source's own inconsistency: the reinvestment rate uses the 31.02% effective rate while the ROC uses the 36.1% marginal rate. Prefer one rate throughout.)

*Baseline arithmetic:* existing investment $1,000 earning 12% -> current earnings $120. Add $100 of new investment at 12% with no change in the existing return: next period's earnings = 1,000×0.12 + 100×0.12 = $132; change = $12; reinvestment rate = 100/120 = 83.33%; `g = 0.8333 × 0.12 = 10%` = 12/120. If instead the return on the existing base rises from 12% to 13%: `[1,000 × (0.13 − 0.12) + 100 × 0.13] / [1,000 × 0.12] = 23/120 = 19.17%`.

**Determinism:**
- DETERMINISTIC: the reinvestment rate, ROC, both growth formulas, the efficiency term and its annualization, and the decomposition into new-investment growth vs efficiency growth — all from the accounting inputs plus a target ROC and a horizon.
- JUDGMENT: whether the ROC is a true economic return or an accounting artifact; whether this year's reinvestment rate is representative (needs the multi-year history); the target ROC and how many years it takes to get there (Motorola's "halfway to the industry average over 5 years" is a judgment, not a calculation); whether the growth is sustainable at the firm's scale.

**Pitfalls:**
- Setting growth and reinvestment independently. Every growth assumption implies a reinvestment rate and an ROC; if you do not state them, you have assumed them silently.
- Extrapolating a reinvestment rate above 100% (Cisco's 106.81%) as if it were sustainable.
- Using ROC computed on end-of-year capital, or on capital that excludes the research asset and lease asset.
- Mixing the effective tax rate into the reinvestment rate and the marginal rate into the ROC.
- Applying the efficiency term every year forever. It is a one-off improvement spread over the transition, not a perpetual source of growth — and in stable growth you cannot count on it at all.
- Using this equation when operating income is negative or margins are changing. Both returns are meaningless there.
- Assuming acquisition-driven reinvestment earns the same ROC as organic investment.

**Sources:**
- valpacket1spr21 p.159-160, p.174-177, p.186-187, p.189-191, p.196
- valpacket1spr20 p.156-157, p.171-174, p.183-184, p.186-188, p.193
- cfpacket2spr20 p.242, p.247 (Disney EBIT growth), p.262-264 (three-phase growth from ROC x reinvestment rate)
- spreadsheet:cpxest.xls — reinvestment rate = g/ROC as the fundamental cap-ex estimator
- spreadsheet:growthbreakdown.xls — high-growth reinvestment rate = g/ROIC on growth; stable reinvestment rate = g_stable/ROC_stable
- spreadsheet:ImpliedROCROE.xls — inverting the identity to read the ROC implied by a cash-flow forecast

**Related:** [[fundamental-growth-equity]], [[return-on-invested-capital]], [[value-of-growth]], [[net-capital-expenditures]], [[non-cash-working-capital]], [[fcff]], [[terminal-value]], [[top-down-revenue-growth]], [[historical-growth]]

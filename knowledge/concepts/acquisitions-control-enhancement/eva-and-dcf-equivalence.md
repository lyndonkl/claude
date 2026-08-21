# EVA, CFROI and their equivalence to DCF

**Core idea:** Firms often manage to a proxy for value rather than to value itself. The proxies come in four families: accounting variables (earnings, return on investment), marketing variables (market share), cash-flow variables (CFROI), and risk-adjusted cash-flow variables (EVA). EVA is the most rigorous of them. It measures the surplus earned over the cost of the capital employed. The key result is that EVA is not a different model of value — it *is* the DCF, rearranged. Firm value equals capital invested plus the present value of all future EVA, and that equals the present value of FCFF. If the two disagree, an assumption is inconsistent somewhere. The metric itself cannot create or destroy value.

**Formulas:**
- `EVA = (Return on Capital − Cost of Capital) × Capital Invested`, where capital invested is measured at the **beginning** of the period.
- Equivalently `EVA_t = EBIT(1−t)_t − WACC_t × Capital invested at start of t`.
- `CFROI = IRR of the cash flows on the capital, computed against the base value of capital invested`.
- Firm value, EVA route: `Firm value = Capital invested + PV of EVA from assets in place + Σ PV of EVA from new investments`.
- EVA from assets in place, as a perpetuity: `(ROC − WACC) × Capital / WACC`.
- Firm value, DCF route: `Firm value = Σ FCFF_t / (1+WACC)^t + PV(Terminal value)`, with `Terminal value_n = FCFF_{n+1} / (WACC − g)`.
- `MVA (Market Value Added) = Market value of firm − Capital invested`, and MVA equals the present value of expected EVA over time.
- Stable-phase consistency: `Reinvestment rate = g / ROC`.
- Terminal-capital reconciliation (needed in multi-stage models): `Adjusted terminal capital = EBIT(1−t)_terminal / ROC_terminal`, with `ROC_terminal = g_stable / Terminal reinvestment rate`. Add `PV of (Adjusted terminal capital − Ending capital in the final explicit year)` to the EVA bridge.

**Procedure:**
1. Measure capital invested at the start of each period. Roll it forward: `Capital_end = Capital_begin + Net capital expenditures + Change in working capital`, with `Net cap ex = Cap ex − Depreciation`.
2. Compute `EBIT(1−t)` for each year.
3. Compute the capital charge for each year: `WACC_t × Capital_begin,t`. Use the beginning-of-year capital, not the average or the ending balance.
4. Subtract to get EVA for each year.
5. Discount each year's EVA at the cumulative cost of capital: `Cum_t = Π_{s=1..t} (1 + WACC_s)`. Use cumulative products when WACC varies by year, not a single constant rate.
6. Handle the terminal year. Compute the terminal reinvestment rate implied by the DCF, back out the terminal ROC from `g = ROC × reinvestment rate`, and set `Adjusted terminal capital = EBIT(1−t)_terminal / ROC_terminal`.
7. Capitalize terminal EVA: `EVA_terminal / (WACC_stable − g_stable)`, and discount it back.
8. Bridge to firm value: `PV of EVA + Capital invested + PV of terminal-capital adjustment`.
9. Run the FCFF DCF on the same assumptions and confirm the two match. If they do not, look for the inconsistency — usually the terminal capital adjustment, the beginning-versus-ending capital convention, or a reinvestment rate that does not equal `g/ROC`.
10. Report MVA as market value minus capital invested, and check it equals the PV of expected EVA.

**Reference data:**

Simple illustration (the teaching example): a firm has book capital of $100 million earning 15% return on capital in perpetuity, with a 10% cost of capital. It invests an additional $10 million at the beginning of each of the next 5 years, each also earning 15% in perpetuity. After year 5, earnings grow 5% a year forever, the firm keeps reinvesting, but the return on capital on new investments equals the cost of capital (10%).

EVA route:

| Component | Calculation | Value |
|---|---|---|
| Capital invested | given | $100.00 |
| EVA from assets in place | (0.15 − 0.10) × 100 / 0.10 | $50.00 |
| EVA, year 1 investment | [(0.15−0.10) × 10 / 0.10] / 1.1^0 | $5.00 |
| EVA, year 2 investment | ÷ 1.1^1 | $4.55 |
| EVA, year 3 investment | ÷ 1.1^2 | $4.13 |
| EVA, year 4 investment | ÷ 1.1^3 | $3.76 |
| EVA, year 5 investment | ÷ 1.1^4 | $3.42 |
| **Firm value** | sum | **$170.85** |

Post-year-5 investments earn ROC = WACC, so they add zero EVA. Composition: $100 of capital invested plus $70.85 of PV of excess returns. MVA = `170.85 − 100 = $70.85`.

DCF route, same firm — FCFF build ($):

| Item | Base | Yr 1 | Yr 2 | Yr 3 | Yr 4 | Yr 5 | Term Yr |
|---|---|---|---|---|---|---|---|
| EBIT(1−t): assets in place | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | |
| EBIT(1−t): Yr 1 investment | | 1.50 | 1.50 | 1.50 | 1.50 | 1.50 | |
| EBIT(1−t): Yr 2 investment | | | 1.50 | 1.50 | 1.50 | 1.50 | |
| EBIT(1−t): Yr 3 investment | | | | 1.50 | 1.50 | 1.50 | |
| EBIT(1−t): Yr 4 investment | | | | | 1.50 | 1.50 | |
| EBIT(1−t): Yr 5 investment | | | | | | 1.50 | |
| **Total EBIT(1−t)** | 15.00 | 16.50 | 18.00 | 19.50 | 21.00 | 22.50 | 23.63 |
| − Net capital expenditures | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 11.25 | 11.81 |
| **FCFF** | | 6.50 | 8.00 | 9.50 | 11.00 | 11.25 | 11.81 |

After year 5 the reinvestment rate is `g/ROC = 5%/10% = 50%`, which is why net cap ex jumps to 11.25 in year 5.

Present values:

| Year | 0 | 1 | 2 | 3 | 4 | 5 | Term Yr |
|---|---|---|---|---|---|---|---|
| FCFF | | 6.50 | 8.00 | 9.50 | 11.00 | 11.25 | 11.81 |
| PV of FCFF | (10) | 5.91 | 6.61 | 7.14 | 7.51 | 6.99 | |
| Terminal value | | | | | | 236.25 | |
| PV of terminal value | | | | | | 146.69 | |
| **Value of firm** | **170.85** | | | | | | |

`TV_5 = 11.81 / (0.10 − 0.05) = 236.25`, and `−10 + 5.91 + 6.61 + 7.14 + 7.51 + 6.99 + 146.69 = $170.85`. Identical to the EVA answer.

**Model spreadsheets that mechanize this** (`fcffeva.xls` and `evavaln.xls`, the "Focussed Valuation Model" workbooks). Both run a 10-year model — 5 high-growth years, a 5-year linear transition, then stable perpetuity — and value the same firm both ways. Example inputs, base year: revenues 12,406; capital invested 20,000; depreciation 233; cap ex 298; ΔWC 115; debt 0; 1,500 shares.

| Input | High growth (yrs 1–5) | Stable (yr 10 on) |
|---|---|---|
| Revenue growth | 25% | 6% |
| Operating expenses as % of revenues | 70% | 75% |
| Cap ex / depreciation growth | 25% | cap ex = 2.0× depreciation |
| Working capital as % of revenues | 7.5% | 7.5% |
| Tax rate | 36% | 36% |
| Beta | 1.25 | 1.1 |
| Risk-free rate | 6.5% | 6.5% |
| Equity risk premium | 5.5% | 5.5% |
| Pre-tax cost of debt | 8.5% | 7.5% |
| Debt ratio | 0% | 5% |

Results, both routes:

| Route | Bridge | Value |
|---|---|---|
| FCFF DCF | Σ PV(FCFF) incl. terminal value 167,812.58 | **80,367.50** |
| EVA | PV of EVA 60,463.43 + capital invested 20,000 + terminal-capital adjustment (−95.93) | **80,367.50** |

Value per share = `80,367.50 / 1,500 = $53.58`.

Transition-year schedules used by both sheets (linear interpolation over years 6–10):

| Year | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|
| Revenue & depreciation growth | 0.212 | 0.174 | 0.136 | 0.098 | 0.060 |
| Operating expenses % of revenue | 0.71 | 0.72 | 0.73 | 0.74 | 0.75 |
| Cost of equity | 0.1321 | 0.13045 | 0.1288 | 0.12715 | 0.1255 |
| Debt proportion | 0.01 | 0.02 | 0.03 | 0.04 | 0.05 |
| After-tax cost of debt | 0.05312 | 0.05184 | 0.05056 | 0.04928 | 0.048 |
| WACC | 0.1313102 | 0.1288778 | 0.1264528 | 0.1240352 | 0.121625 |

Terminal reconciliation in those workbooks: terminal reinvestment rate 0.14392, terminal ROC = `0.06 / 0.14392 = 0.41691`, adjusted terminal capital = `12,079.945 / 0.41691 = 28,974.90` against ending year-10 capital of 29,300.83. The PV of that −325.93 gap is −95.93, and without it the two routes do **not** reconcile.

**Worked example:** Use the simple illustration above. The EVA route gives $170.85 by adding $100 of capital to $70.85 of discounted excess returns. The DCF route gives $170.85 by discounting the FCFF stream and its terminal value. Same inputs, same answer, two arrangements of the same arithmetic.

The decomposition is the payoff. It tells you that $100 of the value is simply the money already invested, and $70.85 is the value of earning 5 percentage points above the cost of capital. Note also what contributes nothing: the 5% perpetual growth after year 5 adds zero, because those investments earn exactly the cost of capital.

**Determinism:**
- DETERMINISTIC: everything above, given the inputs. Capital rollforward, EVA per year, cumulative WACC discounting, terminal ROC, adjusted terminal capital, the reconciliation term, both firm values, MVA, and the assertion that the two routes match. CFROI is a deterministic IRR given a capital base and a cash-flow stream.
- JUDGMENT: how to measure capital invested. The workbooks use naive book debt plus book equity, which needs adjustment for leases, R&D and goodwill in practice. Also judgment: the growth, margin and transition assumptions; the stable-period ROC; and whether the accounting ROC is a fair proxy for a true cash-flow return.

**Pitfalls:**
- Skipping the terminal-capital adjustment. Without it, the EVA and DCF values differ, and analysts often blame "the method" rather than the missing reconciliation term.
- Using ending or average capital in the capital charge instead of beginning capital.
- Discounting at a constant WACC when the WACC ramps through a transition period. Use cumulative products.
- Rebuilding terminal FCFF from components. Grow the whole FCFF at the stable rate instead.
- Believing EVA is a superior valuation model. It is the same model. If it gives a different answer, an assumption is inconsistent.
- Using naive book capital as the capital base without adjustment, which corrupts ROC and therefore every EVA figure.
- Setting a stable-phase reinvestment rate inconsistent with `g/ROC`.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.154-161`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.154-161`
- `spreadsheets/reconciliation — fcffeva.xls (sheets "FCFF Valuation", "EVA Valuation")`
- `spreadsheets/focussed-eva-finsvc — evavaln.xls (sheets "FCFF Valuation", "EVA Valuation")`

**Related:** [[gaming-eva]], [[paths-to-value-creation]], [[growth-quality-and-excess-returns]], [[status-quo-valuation]], [[terminal-value]], [[fcff]], [[return-on-invested-capital]], [[excess-return-models]]

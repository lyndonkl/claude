# Model choice in practice: three worked cases and the breakeven cross-check

**Core idea:** The model-choice rules are easiest to learn from cases where the subject dictates the answer. A regulated utility with a decades-stable capital structure and a 97% payout gets a one-stage dividend discount model. A large industrial with moderate growth and modest leverage gets a two-stage FCFF model. An entire equity index, whose earnings must eventually grow with the economy, gets a two-stage dividend discount model. In each case the three building blocks are justified before any number is computed. Once the model produces a value, one cross-check costs nothing: solve for the growth rate that would make the model value equal the market price. That breakeven growth turns a valuation into a statement about what the market believes.

**Formulas:**
- Gordon growth: `Value per share = DPS₁/(k_e − g)`, `DPS₁ = DPS₀(1 + g)`.
- Breakeven (implied) growth: solve `DPS₀(1+g)/(k_e − g) = Market Price` for g. Closed form: `g = (k_e × P − DPS₀)/(P + DPS₀)`.
- Target price one year out, assuming the market corrects: `Expected Price₁ = Value today × (1 + g)`.
- Expected one-year return: `(Expected Price₁ + Expected DPS₁ − Purchase Price)/Purchase Price`.
- Fundamental growth for equity: `g = Retention Ratio × ROE`.
- Two-stage FCFF: `Value = Σ_t FCFF_t/(1+WACC)^t + TV_n/(1+WACC)^n`, `TV_n = FCFF_{n+1}/(WACC_stable − g)`.

**Reference data — the three cases and why each model was chosen:**

| Subject | Model | Why that cash flow | Why that growth pattern |
|---|---|---|---|
| Con Ed, Aug 2008 | Stable-growth DDM | Payout ≈ 97% of FCFE; leverage stable at ~70/30 for decades | Regulated utility; NY service area grows ~2% |
| 3M, Sept 2008 | Two-stage FCFF | Firm-level valuation with modest, roughly stable leverage (8% debt) | Moderate growth (7.5%) for 5 years, then 3% forever |
| S&P 500, Jan 2020 | Two-stage DDM | Dividends are the tangible cash flow at index level | Near-term analyst growth (3.96%) exceeds stable growth |

**Procedure:**
1. Run the three model-choice tests before modeling. Payout versus FCFE; leverage stability; growth versus the economy.
2. Add the consistency tests Damodaran applies to a stable-growth candidate: is the payout high, like a mature firm's; does `retention × ROE` reproduce the g you assumed; is the beta inside the 0.8–1.2 stable range?
3. Build the model and compute the value.
4. Sweep the perpetual growth rate across a range and plot value against g.
5. Solve for the breakeven g where model value equals market price. Compare it with your fundamental estimate.
6. If you conclude the stock is mispriced, compute the target price and the expected one-year return that a correction would produce.
7. Re-run the model when conditions change materially. Intrinsic value is not a constant.

**Worked example A — Con Ed, August 2008 (stable-growth DDM and its breakeven):**
Inputs: DPS $2.32, EPS $3.17 (payout 73%), riskfree 4.10%, beta 0.80, ERP 4.5%. `k_e = 4.1% + 0.8(4.5%) = 7.70%`. `g = 27% × 7.7% = 2.1%`. `Value = 2.32(1.021)/(0.077 − 0.021) = **$42.30**` versus a price of $40.76 on 12 August 2008.
The sensitivity sweep (all other inputs fixed):

| Expected growth rate | Value per share |
|---|---|
| 4.10% | ≈ $67 |
| 3.10% | ≈ $52 |
| 2.10% | $42.30 |
| 1.10% | ≈ $35 |
| 0.10% | ≈ $30 |
| −0.90% | ≈ $27 |
| −1.90% | ≈ $24 |
| −2.90% | ≈ $21 |
| −3.90% | ≈ $19 |

The breakeven sits just below 2.10%. The market is implicitly assuming a perpetual growth rate only slightly under the fundamental estimate, so the disagreement is small. Buying the stock is a bet that Con Ed grows at least at roughly that implied rate. If $42.30 is right, the target price a year out is `42.30 × 1.021 ≈ $43.19`, and the one-year return from $40.76 (plus the $2.37 dividend) exceeds the 7.70% cost of equity, precisely because the entry price is below fair value.

**Worked example B — 3M, before and after the crisis (two-stage FCFF):**

| | 12 Sept 2008 | 16 Oct 2008 |
|---|---|---|
| Base EBIT(1−t) | 5,344 × 0.65 = 3,474 | lowered 10%: 4,810 × 0.65 = 3,180 |
| Reinvestment rate / ROC | 29.97% / 25.19% | 33% / 23.06% |
| Growth, years 1–5 | 0.30 × 0.25 = 7.5% | 0.25 × 0.20 = 5% |
| Cost of equity | 3.72% + 1.15(4%) = 8.32% | 3.96% + 1.15(6%) = 10.86% |
| After-tax cost of debt | (3.72% + 0.75%)(0.65) = 2.91% | (3.96% + 1.5%)(0.65) = 3.55% |
| Cost of capital | 7.88% | 10.27% |
| Stable phase | g 3%, WACC 6.76%, RR = 3/6.76 = 44% | g 3%, WACC 7.55%, RR = 3/7.55 = 40% |
| Terminal value | 2,645/(0.0676 − 0.03) = 70,409 | 2,434/(0.0755 − 0.03) = 53,481 |
| Operating assets + cash − debt = equity | 60,607 + 3,253 − 4,920 = 58,400 | 43,975 + 3,253 − 4,920 = 42,308 |
| **Value per share** | **$83.55** (price $70) | **$60.53** (price $57) |

The lesson: intrinsic value itself moved from $83.55 to $60.53 in five weeks, because cash flows, growth and discount rates all changed. A DCF is not a fixed anchor the market eventually returns to.

**Worked example C — the S&P 500, 1 January 2020 (two-stage DDM at market level):**
Trailing-12-month index dividends are 58.80. They grow 3.96% for five years (61.13, 63.55, 66.06, 68.67, 71.39), then at the riskfree rate of 1.92% forever. Cost of equity: `k_e = 1.92% + 1.00 × 5.00% = 6.92%`. Beta is 1.00 because the index *is* the market. The 5% ERP sits slightly above the 20-year average implied premium. `Terminal value = 71.39 × 1.0192/(0.0692 − 0.0192) = 1,455.21`. Index value = PV of five dividends + PV of terminal value = **1,311.87**, against an index level of 3,230.78. The gap is a warning about the cash-flow choice, not proof of a 60% overvaluation: dividends alone understate cash returned when buybacks are large.

**Determinism:**
- DETERMINISTIC: every valuation above given its inputs; the growth sweep; the closed-form breakeven growth; the target price and expected return.
- JUDGMENT: which model the subject warrants; the stable growth rate, beta and ERP; whether to add buybacks to dividends at index level; how far to cut base earnings in a crisis. The 2008 3M pair shows how much of the answer these judgments carry.

**Pitfalls:**
- Reading a low DDM value as overvaluation when the payout measure is incomplete (buybacks at index level, retained cash at firm level).
- Treating intrinsic value as static. Crisis conditions move both the cash flows and the discount rate.
- Sweeping the growth rate while holding the cost of equity fixed, then forgetting that a much higher g would also imply a higher riskfree rate.
- Computing a breakeven growth rate and calling it a forecast. It is what the market is assuming, not what will happen.

**Sources:**
- valpacket1spr21 p.279-280
- valpacket1spr20 p.275-280
- valpacket1spr21 p.276-278 (equity risk premiums used in these case valuations; case-study set-up)
- valpacket1spr20 p.272-274 (same)

**Related:** [[dcf-model-choice-framework]], [[dividends-versus-fcfe]], [[equity-versus-firm-valuation]], [[growth-pattern-and-stage-count]], [[multistage-model-mechanics]], [[equity-value-bridge]], [[equity-risk-premium]], [[implied-equity-risk-premium]], [[terminal-value]]

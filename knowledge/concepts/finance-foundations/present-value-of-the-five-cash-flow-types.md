# Present Value of the Five Cash Flow Types

**Core idea:** Every asset's cash flows can be broken into five building blocks. These are the simple cash flow, the annuity, the growing annuity, the perpetuity, and the growing perpetuity. Each block has a closed-form present value, so you never have to discount cash flows one by one. Most real assets are combinations. A conventional bond is an annuity (the coupons) plus a simple cash flow (the face value at maturity). A stock is often modeled as a growing annuity (the high-growth years) plus a growing perpetuity (the terminal value). Learning to decompose an asset into these blocks is most of the work in valuing it.

**Formulas:**
- Simple cash flow, PV: `PV = CF_t / (1 + r)^t`. `CF_t` = the single cash flow at time t; `r` = discount rate per period; `t` = number of periods until it arrives.
- Simple cash flow, FV: `FV = CF_0 × (1 + r)^t`. `CF_0` = cash flow today.
- Annuity, PV: `PV(A, r, n) = A × [1 − 1/(1+r)^n] / r`. `A` = the constant cash flow received at the end of each period; `n` = number of periods. This is an ordinary (end-of-period) annuity: nothing at time 0, `A` at periods 1 through n.
- Growing annuity, PV: `PV(A, r, g, n) = A(1+g) × [1 − (1+g)^n/(1+r)^n] / (r − g)`. `A` = the current (time-0) cash flow; `g` = constant expected growth rate. The first payment is `A(1+g)` at period 1, and the last is `A(1+g)^n` at period n.
- Growing annuity special case: if `g = r`, the formula divides by zero. Use `PV = n × A(1+g) / (1+r)`, which is simply the nominal sum of the payments discounted without any net growth effect.
- Perpetuity, PV: `PV = A / r`. `A` = the constant cash flow received forever, starting one period from now.
- Growing perpetuity, PV: `PV = CF_1 / (r − g)`. `CF_1` = the expected cash flow *next* period; requires `r > g` strictly.

**Procedure:**
1. Lay the asset's cash flows on a time line, with today as time 0.
2. Decompose. Look for a constant stream (annuity), a constant-growth stream over a fixed horizon (growing annuity), a one-off lump (simple cash flow), and any never-ending stream (perpetuity or growing perpetuity).
3. Check the end date of each block. Annuity and growing-annuity formulas assume the first payment is one period from now and the last is at period n. If the stream starts later, value it as of one period before its first payment, then discount that value back as a simple cash flow.
4. Apply the matching closed form for each block using the same per-period discount rate.
5. Guard the special cases before computing. For a growing annuity, test `g = r` and switch to the nominal-sum form. For a growing perpetuity, test `r > g`; if `g ≥ r` the value is infinite and the growth assumption is wrong, not the formula.
6. Sum the blocks. All blocks must now be stated as of the same date (time 0) before you add them.

**Reference data:**

| Cash flow type | Shape | PV formula | Guard condition |
|---|---|---|---|
| Simple cash flow | One payment at t | `CF_t/(1+r)^t` | none |
| Annuity | `A` at periods 1..n | `A[1 − 1/(1+r)^n]/r` | `r > 0` |
| Growing annuity | `A(1+g)^k` at periods k = 1..n | `A(1+g)[1 − (1+g)^n/(1+r)^n]/(r−g)` | `g ≠ r` |
| Perpetuity | `A` at periods 1..∞ | `A/r` | `r > 0` |
| Growing perpetuity | `CF_1(1+g)^{k−1}` at periods k = 1..∞ | `CF_1/(r−g)` | `r > g` |

| Composite asset | Decomposition |
|---|---|
| Conventional fixed-rate bond | Annuity (coupons) + simple cash flow (face value) |
| Stock in a DCF | Growing annuity (high-growth years) + growing perpetuity (terminal value), the latter discounted back as a simple cash flow |

**Worked example:** Value $1,000 a year for five years at a 10% discount rate. Using the annuity formula: `PV = 1000 × [1 − 1/(1.10)^5] / 0.10 = 1000 × [1 − 0.62092] / 0.10 = 1000 × 3.7908 = $3,791`. Check it the long way: 909.09 + 826.45 + 751.31 + 683.01 + 620.92 = $3,790.78. The closed form matches the term-by-term sum, which is the point. (Source: Damodaran, Foundations of Finance Session 6.)

**Determinism:**
- DETERMINISTIC: every formula here. A script takes `(A or CF, r, g, n)` and returns the exact PV, including the `g = r` branch and the `r > g` guard. Decomposing a bond into "annuity plus face value" is mechanical once the coupon, face value, and maturity are known.
- JUDGMENT: which decomposition fits the asset; how long the growing-annuity (high-growth) stage should run; the values of `g` and `r`. Estimating `g` for a growing perpetuity requires a view on long-run economic growth and the firm's competitive position, and it is bounded by the riskfree rate in that currency.

**Pitfalls:**
- Applying the growing-annuity formula when `g = r` and getting a division-by-zero error, instead of switching to the nominal-sum form.
- Using a growing perpetuity with `g ≥ r`, which yields a negative or infinite value. That is a signal the growth assumption is impossible, not a formula failure.
- Feeding the *current* cash flow into `CF_1/(r−g)`. The numerator of a growing perpetuity is next period's expected cash flow, so it must already be grown one period.
- Mixing up the annuity timing convention (end-of-period versus beginning-of-period) and being off by one full period's discounting.
- Adding block values that are stated as of different dates.

**Sources:**
- `foundations_of_finance--time_value_of_money p.5-7, p.10-15`

**Related:** [[time-value-of-money-and-discount-rates]], [[compounding-frequency-and-effective-rates]], [[bond-valuation-and-yield-to-maturity]], [[stable-growth-equity-valuation]], [[equity-vs-firm-valuation]], [[terminal-value]]

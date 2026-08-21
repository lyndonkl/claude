# Compounding Frequency and Effective Annual Rates

**Core idea:** A quoted (stated, or nominal) annual interest rate is not the rate you actually earn or pay unless it compounds once a year. The more often interest compounds within the year, the larger the true annual rate. A 10% rate compounded semiannually really earns 10.25%; compounded daily it earns 10.5156%; compounded continuously it earns 10.5171%. The gap widens as the stated rate rises, which is why credit-card and payday-lending quotes understate the true cost. Before comparing two rates, or before discounting cash flows that arrive more often than annually, you must put everything on one compounding basis.

**Formulas:**
- Effective annual rate with discrete compounding: `EAR = (1 + r/m)^m − 1`. `r` = stated (nominal) annual rate; `m` = number of compounding periods per year.
- Effective annual rate with continuous compounding: `EAR = e^r − 1`. `r` = stated annual rate; `e` ≈ 2.71828.
- Per-period rate for discounting sub-annual cash flows: `r_period = r/m`, applied over `n × m` periods for an n-year horizon.
- Converting an EAR back to a stated rate at frequency m: `r = m × [(1 + EAR)^(1/m) − 1]`.

**Procedure:**
1. Read the quote carefully. Identify the stated annual rate `r` and the compounding frequency `m` (annual = 1, semiannual = 2, quarterly = 4, monthly = 12, daily = 365, continuous = ∞).
2. Convert every rate you intend to compare into an effective annual rate using `(1 + r/m)^m − 1`, or `e^r − 1` if compounding is continuous. Only then compare them.
3. For discounting, match the period of the cash flows to the period of the rate. Monthly cash flows are discounted at `r/12` over `12n` periods, not at `r` over `n` periods.
4. If the cash flows are annual but the rate is quoted at a sub-annual frequency, convert the rate to an EAR first and discount annually.
5. State the basis explicitly in your output, since "10%" is ambiguous without it.

**Reference data:** Effective annual rates for a 10% stated annual rate:

| Frequency | Stated rate | m | Formula | Effective annual rate |
|---|---|---|---|---|
| Annual | 10% | 1 | `r` | 10.0000% |
| Semi-annual | 10% | 2 | `(1+r/2)^2 − 1` | 10.2500% |
| Monthly | 10% | 12 | `(1+r/12)^12 − 1` | 10.4713% |
| Daily | 10% | 365 | `(1+r/365)^365 − 1` | 10.5156% |
| Continuous | 10% | — | `e^r − 1` | 10.5171% |

Note the shape of the table: nearly all the gain from more frequent compounding is captured by the time you reach monthly. Going from daily to continuous adds only 0.0015%.

**Worked example:** A bank quotes 10% annual interest compounded semiannually. You earn 5% in the first half-year, and in the second half-year you earn 5% on the original principal *and* on the first half-year's interest. `EAR = (1 + 0.10/2)^2 − 1 = 1.05^2 − 1 = 1.1025 − 1 = 10.25%`. On $10,000 that is $1,025 of interest for the year rather than $1,000. (Source: Damodaran, Foundations of Finance Session 6.)

**Determinism:**
- DETERMINISTIC: the whole concept. Inputs `(r, m)` → `EAR`, exactly. Inputs `(EAR, m)` → stated rate, exactly. A script can also verify that a discounting scheme is internally consistent by checking that the per-period rate and period count match the quoted basis.
- JUDGMENT: essentially none in the arithmetic. The only judgment is reading an ambiguous quote correctly, which requires the contract or the market convention for that instrument (US Treasuries quote semiannual, most loans quote monthly).

**Pitfalls:**
- Comparing a monthly-compounded quote against an annually-compounded quote at face value. The higher-frequency quote always understates its true cost.
- Discounting monthly cash flows at the full annual rate, which overstates their present value.
- Assuming continuous compounding is a large step up from daily. It is not; the difference is a rounding error at ordinary rates.
- Forgetting the basis when a valuation mixes annual cash flows with a bond yield quoted on a semiannual basis.

**Sources:**
- `foundations_of_finance--time_value_of_money p.9`

**Related:** [[time-value-of-money-and-discount-rates]], [[present-value-of-the-five-cash-flow-types]], [[bond-valuation-and-yield-to-maturity]], [[black-scholes-and-put-call-parity]]

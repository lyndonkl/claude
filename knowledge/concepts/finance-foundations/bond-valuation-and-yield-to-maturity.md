# Bond Valuation and Yield to Maturity

**Core idea:** A contractual claim is a cash flow set when the contract is written, with the promisor committed to deliver it on schedule. The contracted amount is either constant (a fixed-rate coupon bond) or tied to an observable index (a floating-rate bond). Valuing a fixed-rate bond is the cleanest application of present value in finance: discount the coupons, which form an annuity, and the face value, which is a simple cash flow. Run the calculation in reverse and you get the yield to maturity — the single discount rate that makes the promised cash flows worth exactly the market price. Yield to maturity is an internal rate of return, not a guaranteed return, and it is not the same thing as the current yield.

**Formulas:**
- Price of a fixed-rate bond: `Price = C × PV(A, n, r) + F / (1+r)^n`. `C` = annual coupon in currency units (coupon rate × face value); `n` = years to maturity; `r` = discount rate per year; `F` = face value (par, conventionally $1,000).
- Annuity factor: `PV(A, n, r) = [1 − (1+r)^(−n)] / r`. This is the present value of $1 received at the end of each year for n years.
- Yield to maturity: solve `Price = C × PV(A, n, YTM) + F/(1+YTM)^n` for `YTM`. There is no closed form; it is found by root-finding (IRR).
- Current yield (the "bond yield"): `Bond yield = Coupon / Price of bond`. A simpler and much less informative number.
- Par relationship: `market rate < coupon rate` → bond trades above par. `market rate > coupon rate` → below par. `market rate = coupon rate` → at par.

**Procedure:**
1. Confirm the claim is contractual and write down the promised cash flows: coupon amount, payment dates, face value, maturity.
2. Assess default risk before choosing a discount rate. Only governments that control the printing of their own currency can possibly be default-free, and even then not all of them are. If there is default risk, use the default-spread machinery instead of a bare riskfree rate.
3. For a default-free bond, take the government riskfree rate for the bond's maturity in that currency.
4. Compute the annuity factor for the coupons and discount the face value separately. Add them.
5. Sanity-check against par. Compare the market rate with the coupon rate and confirm the price lands on the right side of face value. If a bond with a 3% coupon prices below par at a 2% market rate, you have made an arithmetic error.
6. To get yield to maturity, invert. Take the observed market price and solve for the rate that equates the promised cash flows to it. Use an IRR routine.
7. Report yield to maturity, not current yield, when comparing bonds. Current yield ignores the pull to par and the timing of the principal repayment entirely.
8. For a floating-rate bond, do not run the fixed-rate machinery. A bond whose coupon resets to the market rate each period should trade at par. Even an imperfect reset keeps the price much closer to par than an otherwise identical fixed-rate bond.

**Reference data:** No lookup table is needed for a default-free bond beyond the government yield curve in the relevant currency. For orientation, US Treasury rates at the start of 2018 ran from 1.29% at one month to 2.81% at thirty years, and the 10-year sat at 2.46%.

| Convention | Value |
|---|---|
| Face value (par), US corporate and Treasury bonds | $1,000 |
| Coupon on a "3% coupon bond" with $1,000 face | $30 per year |
| Below investment grade threshold | Rated below BBB |

**Worked example:** A 3% coupon, 10-year US Treasury bond with $1,000 face value, when the 10-year US dollar riskfree rate is 2%.

`PV(A, 10, 2%) = [1 − 1.02^(−10)] / 0.02 = [1 − 0.82035] / 0.02 = 8.9826`
`Price = 30 × 8.9826 + 1000 / 1.02^10 = 269.48 + 820.35 = $1,089.83`

It trades above par because the market rate of 2% is below the 3% coupon rate. Now invert. Suppose the same bond is quoted at $1,043.76 instead. Solving `1043.76 = 30 × PV(A, 10, r) + 1000/(1+r)^10` gives `YTM = 2.50%`. The current yield on that price is `30 / 1043.76 = 2.87%`, which is a different and misleading number — it ignores the $43.76 of premium that will erode to zero by maturity. (Source: Damodaran, Foundations of Finance Session 7.)

**Determinism:**
- DETERMINISTIC: the price, given coupon rate, face value, maturity, and discount rate. The yield to maturity, given price, coupon, face value, and maturity, via root-finding. The current yield. The par-side check.
- JUDGMENT: whether the issuer is genuinely default-free. Which maturity point on the yield curve to use. Whether the quoted price is a clean or dirty price. For floating-rate bonds, how imperfect the reset is and how far from par that pushes the price.

**Pitfalls:**
- Assuming all government bonds are riskless. Only currency-issuing sovereigns can be default-free, and not all of them are.
- Quoting current yield as if it were the return. It ignores the pull to par and the principal timing.
- Treating yield to maturity as a promised return. It is the IRR of promised cash flows and is realized only if every coupon is reinvested at that same rate and the issuer never defaults.
- Discounting the promised cash flows of a risky bond at the riskfree rate, which overvalues it by the entire default spread.
- Running fixed-rate valuation machinery on a floating-rate bond.
- Mixing an annual discount rate with a semiannual coupon schedule.

**Sources:**
- `foundations_of_finance--vauing_bonds p.2-5, p.13`

**Related:** [[interest-rate-risk-and-bond-propositions]], [[default-risk-and-default-spreads]], [[present-value-of-the-five-cash-flow-types]], [[yield-curve-and-growth-signals]], [[compounding-frequency-and-effective-rates]], [[finance-first-principles]]

# Project duration and project-specific financing

**Core idea:** Duration is the present-value-weighted average time at which a cash flow stream arrives, and it measures how much a value changes when interest rates change. Compute it for a project and you know the maturity the project's debt should have. Compute it for a bond and you can compare the two directly. Duration is the quantitative core of maturity matching. Project-specific financing takes matching to its logical end: design the debt around the individual project. That makes sense when a firm has a few large, independent projects. It becomes impractical and costly when the firm runs a portfolio of projects with interdependent cash flows — then you match at the firm level instead ([[macro-sensitivity-regressions]]).

**Formulas:**
- Duration of a project: `Duration = Σ_t [ t × PV(CF_t) ] / Σ_t PV(CF_t)`, where `PV(CF_t) = CF_t / (1+r)^t`, CF_t = the cash flow in year t (the final year includes the terminal value), and r = the discount rate (cost of capital).
- Duration of a straight bond or loan: `Duration = (dP/P)/(dr/r) = Numerator / Denominator`, with
  `Numerator = Σ_{t=1..N} [t × Coupon_t/(1+r)^t] + N × Face Value/(1+r)^N`
  `Denominator = Σ_{t=1..N} [Coupon_t/(1+r)^t] + Face Value/(1+r)^N`
  P = bond price, r = yield, N = maturity in periods, Coupon_t = interest payment in period t, Face Value = principal repaid at maturity.
- Duration rises with maturity and falls as the coupon rate rises.
- Empirical alternative (regression duration): the slope of `Change in firm value` on `Change in interest rates`, sign-flipped — see [[macro-sensitivity-regressions]].

**Procedure:**
1. Lay out the project's expected cash flows by year, including the terminal value in the final year.
2. Discount each at the project's cost of capital.
3. Multiply each present value by its year index t and sum.
4. Divide by the sum of the present values. That is the project duration in years.
5. Set the debt maturity/duration to match. Note that a bond's *maturity* exceeds its *duration*, so matching maturity to duration overshoots slightly; compare like with like.
6. Set the currency mix to the currency of the project's revenues, and add features that link debt service to the project's cash flow driver where possible.
7. Decide whether to finance at the project level at all. Use project-specific financing when the projects are few, large and independent. Avoid it when the firm holds a portfolio of interdependent projects.
8. If choosing between duration methods, check the assumptions. Traditional duration assumes cash flows are unaffected by interest rate changes and that rate changes are small. Regression duration assumes past project cash flows resemble future ones, that the link between cash flows and rates is stable, and that changes in market value reflect changes in firm value.

**Reference data:** None beyond the project's own cash flows and the firm's discount rate.

**Worked example:** Duration of a proposed Disney theme park in Brazil, discounted at 8.46% ($ millions):

| Year | Annual cash flow | Terminal value | PV @ 8.46% | PV × t |
|---|---|---|---|---|
| 0 | −2,000 | | −2,000 | 0 |
| 1 | −1,000 | | −922 | −922 |
| 2 | −859 | | −730 | −1,460 |
| 3 | −267 | | −210 | −629 |
| 4 | 340 | | 246 | 983 |
| 5 | 466 | | 311 | 1,553 |
| 6 | 516 | | 317 | 1,903 |
| 7 | 555 | | 314 | 2,200 |
| 8 | 615 | | 321 | 2,568 |
| 9 | 681 | | 328 | 2,952 |
| 10 | 715 | 11,275 | 5,321 | 53,206 |
| **Sum** | | | **3,296** | **62,355** |

Duration = 62,355 / 3,296 = **18.92 years**. The ideal debt for this park would therefore have a duration of roughly 19 years, be denominated in a mix of Latin American currencies reflecting where visitors come from, and — if it can be structured — carry interest payments tied to the number of visitors at the park.

**Determinism:**
- DETERMINISTIC: cash flows by year plus a discount rate → present values, PV×t, and duration. Same for bond duration given coupons, face value, maturity and yield. Fully scriptable.
- JUDGMENT: forecasting the project cash flows and the terminal value; choosing the discount rate; deciding the currency mix; deciding whether project-specific financing is worth its cost; judging whether the traditional or regression duration estimate is more trustworthy.

**Pitfalls:**
- Omitting the terminal value. It dominates the calculation — 53,206 of Disney's 62,355 PV×t total comes from year 10.
- Confusing maturity with duration. Disney's debt had a 7.92-year weighted average maturity against a firm-level duration estimate of about 4.3 years; maturity always exceeds duration for a coupon-paying instrument.
- Using project-specific financing for a portfolio of small, interdependent projects.
- Ignoring that traditional duration assumes cash flows are independent of interest rates, which fails for interest-rate-sensitive businesses.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.121
- corporate_finance--lecture_slides--cfpacket2spr20 p.124-126
- corporate_finance--lecture_slides--cfpacket2spr20 p.132-133

**Related:** [[debt-design-framework]], [[macro-sensitivity-regressions]], [[cost-of-capital-approach]], [[terminal-value]]

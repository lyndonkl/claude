# Duration: the quantitative core of maturity matching

Duration is the present-value-weighted average time at which a cash flow stream arrives.
It is also the sensitivity of a value to interest rates. Those two readings are the same
number, which is why it links assets to debt.

## Project duration

    PV(CF_t)  = CF_t ÷ (1 + r)^t
    duration  = Σ [ t × PV(CF_t) ] ÷ Σ PV(CF_t)

`CF_t` is the cash flow in year t, with the terminal value folded into the final year.
`r` is the project's cost of capital, in the currency of the cash flows.

Both sums run over every year including year 0, and both include negative present values.
The denominator therefore equals the project's NPV.

### Procedure

1. Lay out expected cash flows by year, with the terminal value in the final year.
2. Discount each at the project's cost of capital.
3. Multiply each present value by its year index and sum.
4. Divide by the sum of the present values.
5. Compare against the debt instrument's duration, not its maturity.

Steps 2 to 4 come out of the engine:

```bash
python3 <skills>/debt-design/resources/macrosensitivity.py duration --in project.json
```

The response carries the year-by-year present values, the weighted sum, `duration_years`,
and `terminal_value_share_of_weighted_sum`. Check that last figure first: the worked
example below puts 85% of the weighted sum in the final year.

### Worked example: a theme park in Brazil

Discounted at 8.46%, in millions of dollars.

| Year | Cash flow | Terminal value | PV at 8.46% | PV × t |
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

Duration = 62,355 ÷ 3,296 = **18.92 years**.

Note where the answer comes from. Of the 62,355 total, 53,206 arrives in year 10, almost
all of it from the terminal value. Drop the terminal value and the duration collapses.
That is not a rounding difference, it is a different recommendation.

The design that follows: debt with a duration near 19 years, denominated in a mix of Latin
American currencies reflecting where visitors come from, and if it can be structured, with
interest payments tied to attendance.

## Bond duration, for the comparison

    numerator   = Σ_{t=1..N} [ t × Coupon_t ÷ (1+r)^t ] + N × Face ÷ (1+r)^N
    denominator = Σ_{t=1..N} [ Coupon_t ÷ (1+r)^t ] + Face ÷ (1+r)^N
    duration    = numerator ÷ denominator

`r` is the yield, `N` the maturity in periods. Duration rises with maturity and falls as
the coupon rate rises, because a larger coupon moves weight toward the early years.

Compute it the same way as project duration: build the coupon-plus-face stream, run `npv`
at the yield, and take the PV-weighted average year.

**Maturity exceeds duration for any coupon-paying instrument.** Setting a bond's maturity
equal to the asset duration therefore overshoots. The gap is small at short maturities and
grows with the term. Compare duration to duration.

One firm reviewed in the source material carried debt with a face-value weighted average
maturity of 7.92 years against an estimated asset duration of about 4.3 years. Part of that
gap is the maturity-versus-duration wedge, and part of it is a genuine mismatch. Separate
the two before calling it a finding.

## Two ways to estimate duration, and what each assumes

| Method | Assumes |
|---|---|
| Traditional (PV-weighted) | Cash flows are unaffected by interest-rate changes, and rate changes are small |
| Regression (slope of Δvalue on Δrates) | Past project cash flows resemble future ones, the cash-flow-to-rate link is stable, and market value changes track firm value changes |

The traditional method fails for a business whose cash flows are themselves
interest-rate sensitive, because the first assumption is exactly what is violated. The
regression method fails when the business has changed. Neither is the default; pick the
one whose assumption survives.

## Should the firm finance project by project?

Project-specific financing takes matching to its logical end: design the debt around the
individual asset.

Use it when projects are **few, large and independent**. A mine, a toll road, a power plant
and a resort all qualify. The debt can then carry the exact duration, currency and linkage
of the asset it funds.

Avoid it when the firm runs a **portfolio of numerous, interdependent projects**. The
transaction costs multiply, the covenants conflict, and the interdependence means no single
project's cash flows are separable anyway. Match at the firm level instead, using the macro
regressions.

The middle case is common: a firm with one large lumpy asset and a long tail of small ones.
Finance the large asset specifically and match the remainder at the firm level.

# Time value and cash flow timing

**Core idea:** Incremental cash flows in earlier years are worth more than the same cash flows later. Cash flows at different dates cannot simply be added. They must first be moved to a common point in time. Moving future cash flows back to today is *discounting*. Moving today's cash flows forward is *compounding*. Five standard patterns cover almost every project cash flow: the simple cash flow, the annuity, the growing annuity, the perpetuity, and the growing perpetuity. Alongside the math sits a timing convention. Real cash flows accrue continuously through the year, and some (taxes, debt payments) arrive at discrete quarterly or monthly dates. Present-value models instead place each year's cash flow at a single point: start of year = Time 0, end of year = Time 1. Accounting records the same flows over fiscal years. A model must state which convention it uses and apply it consistently.

**Formulas:** Symbols: `CF_n` = cash flow at end of period n; `CF_0` = cash flow today; `r` = discount rate per period; `n` = number of periods; `A` = level cash flow per period; `g` = constant growth rate.
- Simple cash flow, discounting: `PV = CF_n / (1+r)^n`
- Simple cash flow, compounding: `FV = CF_0 × (1+r)^n`
- Annuity, PV: `PV = A × [1 − 1/(1+r)^n] / r`
- Annuity, FV: `FV = A × [((1+r)^n − 1) / r]`
- Growing annuity, PV: `PV = A(1+g) × [1 − (1+g)^n/(1+r)^n] / (r − g)`, valid for `r ≠ g`; A = the cash flow that just occurred
- Perpetuity: `PV = A / r`
- Growing perpetuity: `PV = (expected cash flow next year) / (r − g)`, requires `r > g`
- Amortizing loan payment: `Payment = Loan × r / (1 − 1/(1+r)^n)`
- PV annuity factor (used to build equivalent annuities): `PVAF(r, n) = (1 − (1+r)^(−n)) / r`

**Procedure:**
1. Fix the period (almost always one year in capital budgeting) and the convention: Time 0 = today, cash flow of year t placed at end of year t.
2. Place any up-front expenditure at Time 0. The case convention: "right now" = Time 0; "next year" = Year 1; "most recent year" = the year just ended.
3. Place investments that occur at the *start* of a year at the end of the previous year. Working capital needed to support year-t sales is therefore invested at end of year t−1.
4. Classify each stream by pattern (simple, annuity, growing annuity, perpetuity, growing perpetuity) and apply the matching formula.
5. Value a growing perpetuity one period *before* its first cash flow, then discount that value back to Time 0 over the remaining periods.
6. Check that the discount rate's period matches the cash flow's period, and that its currency and nominal/real basis match too. See [[currency-and-inflation-consistency]].

**Reference data:** Timing conventions used in the Damodaran capital-budgeting cases:

| Item | Placement |
|---|---|
| Up-front investment ("right now") | Time 0 |
| First operating year ("next year") | Year 1 |
| Working capital supporting year t revenue | End of year t−1 (start of year t) |
| Capital investment made at start of year t | End of year t−1 |
| Salvage / working capital recovery | Final year of project life |
| Terminal value (growing perpetuity of year n+1 flow) | End of year n |

**Worked example:** Rio Disney terminal value. Year-10 incremental cash flow to the firm = $715 million; perpetual growth = 2% (inflation); cost of capital = 8.46%. Terminal value at end of year 10 = 715 × 1.02 / (0.0846 − 0.02) = $11,275 million. That value sits at year 10 and is discounted back ten years alongside the year-10 cash flow: PV = (715 + 11,275)/1.0846^10 = $5,321 million.

**Determinism:** DETERMINISTIC — given a cash flow stream, a rate, a growth rate, and a horizon, every PV/FV/annuity/perpetuity number and the amortization split of a loan payment is a closed-form computation. JUDGMENT — choosing the period convention (annual vs quarterly), deciding whether mid-year discounting is warranted, and picking the growth rate `g` for a perpetuity.

**Pitfalls:**
- Adding cash flows from different years without discounting.
- Using the growing-perpetuity formula with `g ≥ r`, which produces a negative or infinite value.
- Applying the growing-perpetuity formula to the *current* year's cash flow instead of next year's.
- Booking start-of-year investments at the end of that year, understating the up-front outlay by a full year of discounting.
- Mixing an annual discount rate with quarterly or monthly cash flows.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.242-243
- corporate_finance--lecture_slides--cfpacket1spr20 p.245
- corporate_finance--lecture_slides--cfpacket1spr20 p.263
- corporate_finance--case--netflixfit p.1
- corporate_finance--case--netflixfit p.5
- corporate_finance--case--netflixfitpresentation p.2
- corporate_finance--case--netflixfitpresentation p.10

**Related:** [[npv-and-irr-mechanics]], [[terminal-value-and-project-life]], [[comparing-projects-different-lives]], [[currency-and-inflation-consistency]], [[incremental-cash-flow-principle]]

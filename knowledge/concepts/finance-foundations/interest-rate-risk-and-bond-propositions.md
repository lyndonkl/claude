# Interest Rate Risk: Convexity and the Two Bond Propositions

**Core idea:** A bond's price moves when market interest rates move, but not symmetrically and not by the same amount for every bond. Three regularities govern this. Convexity: for an equal-sized rate move up and down, the price gain from the fall exceeds the price loss from the rise. Proposition 1: the longer the maturity, the more sensitive the price. Proposition 2: the lower the coupon rate, the more sensitive the price. Together these tell you which bonds carry the most interest rate risk without any new machinery. You just reprice the same bond at shifted rates and compare.

**Formulas:**
- Repricing is all that is needed: `Price = C × PV(A, n, r) + F/(1+r)^n`, with `PV(A, n, r) = [1 − (1+r)^(−n)]/r`. `C` = annual coupon; `n` = years to maturity; `r` = market rate; `F` = face value.
- Percentage price change: `%Δ = (Price at new rate − Price at old rate) / Price at old rate`.
- Convexity condition: `%Δ from a rate fall of x > |%Δ from a rate rise of x|`, for every straight bond.
- Interest rate sensitivity ranking: sensitivity rises with `n` and falls with the coupon rate. A zero-coupon bond is the most sensitive bond at any given maturity.

**Procedure:**
1. Price the bond at the current market rate. This is the base.
2. Choose a symmetric rate shock, conventionally ±1%.
3. Reprice at `r + shock` and at `r − shock` using the same formula.
4. Express both results as percentage changes from the base price.
5. Compare the magnitudes. The upside from the rate fall will exceed the downside from the rate rise. That asymmetry is convexity, and it works in the bondholder's favor.
6. To rank bonds by interest rate risk, repeat for each candidate and sort. Expect the longest-maturity, lowest-coupon bond to sit at the top.
7. Use the ranking in the direction of your rate view. If you expect rates to fall, long-maturity zero-coupon bonds capture the most price gain. If you fear rate rises, shorten maturity or raise the coupon.
8. If the reset is contractual rather than a rate view, remember the floating-rate escape. A bond whose coupon resets to the market rate has almost no interest rate risk and trades near par.

**Reference data:**

Proposition 1 — percentage price change by maturity. Base case: 3% coupon bond priced at a 2.5% market rate; rate moved to 3.5% and to 1.5% (Damodaran, Foundations of Finance Session 7; values read from the chart):

| Maturity | Rate rises to 3.5% | Rate falls to 1.5% |
|---|---|---|
| 1 year | about −1% | about +1% |
| 5 years | about −5% | about +5% |
| 10 years | −8.18% | +9.06% |
| 30 years | about −18% | about +23% |

Proposition 2 — percentage price change by coupon rate. Base case: 10-year bonds priced at a 2.5% market rate; rate moved to 3.5% and to 1.5%:

| Coupon rate | Rate rises to 3.5% | Rate falls to 1.5% |
|---|---|---|
| 0% | about −9.3% | about +10.3% |
| 1% | between the endpoints | between the endpoints |
| 2% | between the endpoints | between the endpoints |
| 3% | −8.18% | +9.06% |
| 4% | between the endpoints | between the endpoints |
| 5% | about −7.8% | about +8.4% |

Note the relative magnitudes. Maturity is the far stronger lever: going from 1 year to 30 years multiplies sensitivity roughly twentyfold, while going from a 5% coupon to a zero coupon changes it by under two percentage points.

**Worked example:** A 3% coupon, 10-year bond with $1,000 face, currently priced at a 2.5% market rate.

Base: `Price = 30 × PV(A, 10, 2.5%) + 1000/1.025^10 = $1,043.76`
Rate rises to 3.5%: `Price = 30 × PV(A, 10, 3.5%) + 1000/1.035^10 = $958.41`, a change of `(958.41 − 1043.76)/1043.76 = −8.18%`
Rate falls to 1.5%: `Price = 30 × PV(A, 10, 1.5%) + 1000/1.015^10 = $1,138.33`, a change of `(1138.33 − 1043.76)/1043.76 = +9.06%`

The gain of 9.06% beats the loss of 8.18% for the identical 1% move. That 88-basis-point asymmetry is convexity. (Source: Damodaran, Foundations of Finance Session 7.)

**Determinism:**
- DETERMINISTIC: everything here. Inputs `(coupon rate, face value, maturity, base rate, rate shock)` → prices at all three rates and both percentage changes. A script can rebuild both proposition charts by looping over maturities or coupon rates.
- JUDGMENT: the size of the rate shock to test. Whether the rate move is parallel across the curve or concentrated at one maturity. Whether the issuer's default spread will move at the same time, which it usually does in a rate shock. Those judgments need the shape of the yield curve and the credit cycle.

**Pitfalls:**
- Assuming symmetric price responses to symmetric rate moves. Convexity means they never are.
- Using maturity as a proxy for interest rate risk while ignoring the coupon. A 30-year 8% coupon bond is less sensitive than a 30-year zero.
- Testing only a rate rise. The convexity benefit shows up only when you also test the fall.
- Shocking market rates while holding the default spread fixed, when in practice a rate move and a credit move often arrive together.
- Applying these propositions to a floating-rate bond, which is largely insulated by design.

**Sources:**
- `foundations_of_finance--vauing_bonds p.6-8, p.13`

**Related:** [[bond-valuation-and-yield-to-maturity]], [[default-risk-and-default-spreads]], [[yield-curve-and-growth-signals]], [[present-value-of-the-five-cash-flow-types]]

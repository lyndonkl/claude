# Finance First Principles (The Building Blocks)

**Core idea:** Finance is not one business function among many. It is the measuring rod for all of business, because every decision eventually shows up in earnings and cash flows. The discipline rests on six building blocks. A business is forward-looking, not backward-looking. Cash flows matter, and earnings are only a stopping point on the way to them. Risk is neither good nor bad; it is part of business, and it must be defined, attributed to someone's perspective, and measured. A dollar today is worth more than a dollar in the future. The value of any asset is the present value of its expected cash flows. And markets have no free lunches, because trading costs and taxes are everywhere. The most useful practical consequence is the cash-flow taxonomy: cash flows are contractual, residual, or contingent, and each type gets a different valuation machinery.

**Formulas:**
- Generic valuation identity: `Value = Σ_{t=1..n} E(CF_t) / (1 + r)^t` where `E(CF_t)` = expected cash flow in period t, `r` = risk-adjusted discount rate per period expressed in the same currency and same (nominal/real) terms as the cash flows, `n` = life of the asset (n = ∞ for a going concern).
- Financing identity: `Total capital = Debt + Equity`. There is no third funding category in finance; every hybrid is decomposed into a debt component and an equity component.

**Procedure:**
1. Classify the claim you are valuing by cash-flow type. Is the cash flow fixed by contract with a promisor (a bond, a lease, a loan)? Is it a residual left over after all other claimants are paid (common equity, a partnership interest)? Or is it contingent on a specified event inside a finite period (a warrant, a patent, an undeveloped reserve, equity in a distressed firm)?
2. Match the machinery to the type. Contractual → discount the *promised* cash flows at a rate adjusted for default risk (riskfree rate + default spread). Residual → discount the *expected* cash flows at a rate reflecting the risk that the marginal investor perceives. Contingent → use an option pricing model; do not use a straight DCF, which will systematically undervalue it.
3. Decompose hybrids. A convertible bond is a straight bond (contractual) plus a conversion option (contingent). An operating lease is contractual. Preferred stock is contractual in form but residual in enforcement.
4. Value assets on expected future earnings and cash flows, never on historical cost or what was invested in them. If you catch yourself justifying a value with book value or with the price paid, you have switched from finance to accounting.
5. Sanity-check any claimed arbitrage against the two frictions. Ask what the round-trip trading cost is and what the after-tax return is. An "arbitrage" that dies once bid-ask spreads, price impact, and taxes are subtracted was never an arbitrage.

**Reference data:**

| Building block | Damodaran's one-line theme |
|---|---|
| Concept and structure of a business | Forward looking, not backward looking |
| Measurement and importance of cash flows | Earnings are only a stopping point, not the destination |
| Definition and measurement of risk | Risk is neither good nor bad — it is part of business |
| Time value of money | A dollar today is worth more than a dollar in the future |
| Basics of valuation | The value of an asset is the present value of its cash flows |
| Trading fundamentals | No free lunches; the world is full of frictions |

| Cash-flow type | Example | Valuation machinery | Discount rate |
|---|---|---|---|
| Contractually set | Fixed-rate bond coupon, lease payment | PV of promised cash flows | Riskfree rate + default spread |
| Residual | Common equity dividends / FCFE | PV of expected cash flows | Cost of equity (risk perceived by marginal investor) |
| Contingent claim | Warrant, patent, distressed equity | Option pricing model | Riskfree rate (risk-neutral / replication) |

**Worked example:** Take a conventional 10-year, 3% coupon US Treasury bond with $1,000 face value. It is a contractual claim (coupons are promised, not expected), from an issuer that controls the printing of its own currency, so there is no default spread. The valuation machinery is therefore "PV of promised cash flows at the riskfree rate": at a 10-year US$ riskfree rate of 2%, price = $30 × PV(annuity, 10 yrs, 2%) + $1,000/1.02^10 = $1,089.83. Now contrast a share of Consolidated Edison, a residual claim. Its $4.00 dividend is not promised, so you discount an *expected* growing stream at an 8% cost of equity: $4.00 × 1.02 / (0.08 − 0.02) = $68.00 per share. Same present-value arithmetic; different cash-flow type, different discount rate, different inputs.

**Determinism:**
- DETERMINISTIC: once the cash flows and the discount rate are fixed, the present-value sum is pure arithmetic (inputs: `{CF_t}`, `r`, `n` → `Value`). The financing split into debt and equity from a given capital structure is deterministic.
- JUDGMENT: classifying the cash-flow type (a claim can be contractual in form and residual in substance); forecasting expected cash flows; setting the risk-adjusted discount rate; deciding whether a claimed arbitrage survives trading costs and taxes. Judgment here needs the contract terms, the issuer's ability to pay, and the market context.

**Pitfalls:**
- Valuing assets at what was invested in them (historical cost) rather than what they will generate. Finance is forward-looking; accounting is backward-looking.
- Stopping at earnings. Earnings are a way-station; cash flows are the destination, and they can differ materially.
- Treating risk as purely a negative to be minimized. Risk is two-sided; a business that eliminates risk eliminates return.
- Using DCF on a contingent claim, or an option model on a straight residual claim.
- Believing you have found arbitrage. Many claimed arbitrages are compensation for trading costs, taxes, or an unmodeled risk.

**Sources:**
- `foundations_of_finance--introduction p.2-9`

**Related:** [[time-value-of-money-and-discount-rates]], [[present-value-of-the-five-cash-flow-types]], [[risk-definition-and-risk-aversion]], [[equity-vs-firm-valuation]], [[bond-valuation-and-yield-to-maturity]], [[option-payoffs-and-value-determinants]], [[cost-of-capital]]

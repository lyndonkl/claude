# Types of cash flow claims

**Core idea:** Every claim on a business's cash flows falls into one of three types, and the type decides how you value it. A contractual claim is fixed when the contract begins — sometimes a constant amount, sometimes tied to a scalar both sides agree on. A residual claim is whatever is left after the contractual claims have been met. A contingent claim pays only if a stated event happens. Debt is the archetypal contractual claim, equity the archetypal residual claim, and options and guarantees are contingent. Knowing the type tells you which valuation machinery applies: discounting a known schedule, discounting an uncertain residual, or probability-weighting and option pricing.

**Formulas:**
- Residual cash flow to equity: `Residual cash flow = Cash from operations − Taxes − Capital investments − Debt payments`. Cash from operations = operating cash made in the period. Debt payments = interest and principal owed under the debt contract. The result may be negative when contractual claims exceed the cash operations generate.
- Contractual constant claim: `Payment_t = Coupon or fixed interest`, with principal repaid over the loan's life (term bank loan) or at the end (balloon payment).
- Contractual variable claim: `Payment_t = f(observable scalar_t)`. In a floating-rate loan the scalar is a market rate such as LIBOR or the T-Bond rate. In a commodity loan it is a commodity price.
- Contingent claim, expected-value form: `Expected contingent cash flow = Probability of event × Cash flow if the event occurs`.
- Contingent claim, option form: when many events' odds must be judged at once, use an option pricing model instead of a probability-weighted expected value.

**Reference data:** The three claim types.

| Type | Definition | Test | Archetype |
|---|---|---|---|
| Contractual | Fixed when the contract begins; a constant amount or tied to an agreed scalar | Fixed by contract | Bank loan, corporate bond, lease |
| Residual | What is left over after contract claims are met | Leftover after claims are paid | Common equity |
| Contingent | Occurs only if a stated event happens | Depends on an event | Options, warrants, guarantees, litigation payoffs |

Contractual claim sub-types:

| Sub-type | Payment set by | Examples |
|---|---|---|
| Constant | Interest or coupon fixed up front | Fixed-rate bank loan; corporate bond |
| Variable | Terms set up front, amount moves with a named observable variable | Floating-rate loan tied to LIBOR or the T-Bond rate; commodity loan tied to a commodity price |

Principal repayment structures:

| Structure | Repayment |
|---|---|
| Term bank loan | Principal repaid over the life of the loan |
| Balloon payment | Principal repaid at the end of the loan's life |

**Procedure:**
1. Inventory every claim on the firm's cash flows: debt issues, leases, preferred stock, common equity, options, guarantees, pending litigation.
2. Classify each with the three tests. Fixed by contract → contractual. Leftover after claims are paid → residual. Depends on an event → contingent.
3. For contractual claims, extract the payment schedule from the debt footnote: rate, maturity, fixed versus floating, straight versus convertible, and the principal repayment structure.
4. For variable-rate contractual claims, identify the observable scalar and its current level. The payment schedule is only as certain as that scalar.
5. For the residual claim, build the cash flow after taxes, capital investments and debt payments. Accept that it may be negative; that is the definition, not an error.
6. For contingent claims, put a probability on the trigger event and take the expected value.
7. Switch to an option pricing model when you would have to judge the odds for many events at once. That is the signal that expected-value arithmetic will not hold up.
8. Check that the claims exhaust the cash flows. Anything unassigned means you have missed a commitment.

**Worked example:** Coca-Cola at end-2019 ($ millions). Start with the contractual claims. The debt footnote lists total debt of 31,769 across US dollar notes, debentures, zero coupon notes, Australian dollar notes, Euro notes and Swiss franc notes. The blended rate is 1.9%, maturities run to 2098, and the five-year schedule is 4,253 / 3,767 / 3,788 / 4,097 / 1,974. These are constant contractual claims with known payment dates. The residual claim is what remains after those payments, taxes and capital investment. Operating cash 10,471 less capex 2,054 less acquisitions 5,542 less net debt repayment 1,841 leaves 1,034 available to equity. That residual is smaller than the 7,948 actually paid out. Contingent claims sit in the options and litigation footnotes and never appear on the face of the statements. The three types together exhaust the firm's cash.

**Determinism:**
- DETERMINISTIC: the residual cash flow calculation given operating cash, taxes, capital investments and debt payments; payment amounts on a contractual loan given the contract terms; the expected-value product once a probability is supplied.
- JUDGMENT: classifying hybrid claims such as convertible debt and preferred stock, which are contractual in part and contingent in part. Judging the probability of a trigger event is judgment and needs the litigation disclosure, the option terms and the business context. Deciding to switch from expected value to option pricing is a judgment about how many uncertain events interact.

**Pitfalls:**
- Treating a floating-rate loan as if its payments were known. Terms are set up front, but the amount moves with the scalar.
- Assuming a residual claim cannot be negative. It can, whenever contract claims exceed the cash operations generate.
- Probability-weighting a contingent claim whose payoff depends on many interacting events. Use option pricing instead.
- Ignoring contingent claims because they are not on the balance sheet. They still consume value that would otherwise reach equity.
- Confusing the residual claim with what shareholders actually receive. In a public company managers decide the payout.

**Sources:**
- foundations_of_finance--cash_flows p.4-7

**Related:** [[financial-balance-sheet]], [[potential-dividends-fcfe]], [[liabilities-debt-and-leases]], [[financing-cash-flows-and-cash-returned]], [[option-pricing-applications]], [[valuing-equity-as-an-option]]

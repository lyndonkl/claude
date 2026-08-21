# Subsidized debt

**Core idea:** Sometimes a firm borrows below the market rate its default risk would justify — a government development loan, an export-credit facility, a tax-exempt municipal bond, a supplier's concessionary financing. The question is which rate belongs in the cost of capital: the subsidized rate the firm actually pays, or the fair rate its risk implies. Damodaran's framework says use the FAIR, default-risk-based cost of debt to value the operating business, and value the subsidy separately as its own asset. The reason is that the subsidy is a gift from a third party, not a property of the business's investments. Projects should be required to cover what the capital is really worth; otherwise a firm with cheap political money will accept projects that destroy value the moment the subsidy stops.

**Formulas:**
- Fair pre-tax cost of debt = Riskfree rate + Default spread (from the firm's actual or synthetic rating).
- Subsidy value (per year, pre-tax) = (Fair rate − Subsidized rate) × Face amount of subsidized debt.
- Present value of the subsidy = sum over the loan's remaining life of the annual after-tax saving, discounted at a rate reflecting the certainty of the subsidy continuing.
- Total value = Value of operations discounted at the fair-rate cost of capital + PV of subsidy.

**Procedure:**
1. Identify subsidized borrowings and their terms: face amount, stated rate, remaining maturity, conditions attached, and whether the subsidy travels with the asset or with the firm.
2. Estimate the fair cost of debt for the firm ignoring the subsidy — actual rating, or synthetic rating from interest coverage.
3. Build the cost of capital using the fair rate. Value the operating business with it.
4. Value the subsidy separately: the rate differential times the subsidized principal, after tax, over the remaining life, discounted.
5. Add the subsidy's present value to the value of operations if the subsidy is genuinely attached to the firm's future.
6. Do not let a subsidized rate lower the hurdle rate for NEW projects. New projects should earn the fair cost of capital. Otherwise the firm accepts projects that only work because of the subsidy, and it will be exposed when the subsidy lapses or is competed away.
7. Disclose the treatment. This is a stated assumption; the alternative treatments give visibly different answers.

**Reference data:** The teaching case. The Brazilian government lends to Embraer at a subsidized dollar rate of 6%, while Embraer's fair market cost of debt (riskfree 4.29% + two-thirds of Brazil's country default spread + a 1% company spread) is about 9.25-9.29%. The slide poses three options:

| Option | Rate used | Argument for | Argument against |
|---|---|---|---|
| (a) Subsidized rate | 6% | It is what the company actually pays | Understates the true cost of capital; makes bad projects look good; disappears if the subsidy ends |
| (b) Fair cost of debt | 9.25% | It is what the company's projects should be required to cover | Ignores a real cash benefit the firm receives |
| (c) A rate in between | 6-9.25% | Splits the difference | Arbitrary; no economic content |

Damodaran's resolution: use (b) for the cost of capital, and capture the (a)-vs-(b) difference as a separately valued subsidy.

**Worked example:** Embraer, 2004. Subsidized dollar debt at 6%; fair pre-tax cost of debt 9.29%; marginal tax rate 34%. Suppose 1,000 million BR of subsidized principal with 5 years to run. Annual pre-tax saving = (9.29% − 6.00%) × 1,000 = 32.9m BR; after tax at 34% = 21.7m BR. Discounted over 5 years at the fair 9.29% pre-tax rate, that is roughly 84m BR of subsidy value — added to the value of operations, which is itself computed with a cost of capital built on 9.29%, not 6%.

**Determinism:**
- DETERMINISTIC: the rate differential, the annual saving, and the present value of the subsidy given a discount rate and a horizon.
- JUDGMENT: whether the subsidy persists, for how long, and how certain it is. That judgment needs the political and contractual terms of the loan, its renewal history, whether it is conditional on employment or exports, and whether the firm could be forced to repay it.
- JUDGMENT: the discount rate for the subsidy stream. A government-guaranteed saving is more certain than the firm's operating cash flows; a politically contingent one is less certain.
- JUDGMENT: whether the subsidy is a one-off or a structural feature of the business model (a regulated utility with permanent access to tax-exempt debt is different from a one-time development loan).

**Pitfalls:**
- Building the cost of capital on the subsidized rate and then also treating the subsidy as an asset. That double counts.
- Using the subsidized rate as the hurdle rate for new projects, which lets marginal projects clear a rate that does not reflect their risk.
- Assuming a political subsidy is permanent.
- Assuming a subsidized rate signals lower default risk. It signals a policy preference, not creditworthiness.
- Averaging a subsidized rate with a market rate to get a "blended" cost of debt without a stated rationale.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.109
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.106
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.104 (Embraer's fair cost of debt build-up used as the comparison)

**Related:** [[cost-of-debt-estimation-routes]], [[country-risk-in-cost-of-debt]], [[cost-of-capital-assembly]], [[after-tax-cost-of-debt]], [[hurdle-rate-choice]]

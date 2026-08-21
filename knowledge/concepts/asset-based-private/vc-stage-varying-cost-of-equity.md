# Private to VC to public: stage-varying costs of equity

**Core idea:** The cost of equity for a business depends on who owns it, and ownership changes as the company matures. A nascent business is owned entirely by an undiversified founder, who perceives total risk. Then a specialized venture capitalist buys in, holding several investments in the same sector — partially diversified. Then the company goes public and diversified investors set the price. The beta that applies at each stage is the market beta divided by that owner's correlation with the market. So the discount rate falls in steps as the company moves down the ownership chain. Cash flows must be discounted at the rate applicable in the year they arrive, using cumulated (compounded) discount factors. A single constant rate is wrong in both directions: the founder's rate applied forever undervalues the firm, and the public rate applied from day one overvalues it.

**Formulas:**
- `Perceived beta_stage = Market beta / ρ_stage`, where `ρ_stage` = correlation of the owner's portfolio with the market at that stage.
- `Cost of equity_t = Riskfree rate + Perceived beta_t × ERP`
- `Cumulated COE_t = Π_{s=1..t} (1 + Cost of equity_s)` — the compounded discount factor, not `(1 + r)^t` with a single `r`.
- `PV of CF_t = CF_t / Cumulated COE_t`
- `Terminal value at the transition year n = CF_{n+1} / (Post-transition cost of equity − g)`
- `Value of firm = Σ_t [CF_t / Cumulated COE_t] + Terminal value_n / Cumulated COE_n`
- Symbols: `ERP` = equity risk premium; `g` = stable growth rate; `n` = the year the firm goes public or is sold to a public buyer.

**Procedure:**
1. Get a market beta for the sector from publicly traded comparables.
2. Map out the ownership timeline. Who holds the equity in each year? Founder alone, founder plus VC, or public markets?
3. Assign a correlation to each stage:
   - Fully invested private owner → the sector's average firm-market correlation (0.25 in the packet's example).
   - Specialized VC holding several investments in one sector → roughly double that (0.5).
   - Public markets → 1.0, so the perceived beta collapses to the market beta.
4. Compute the perceived beta and cost of equity for each year.
5. Build the cumulated cost of equity year by year as a running product. Do **not** raise a single rate to a power.
6. Discount each year's cash flow by its own cumulated factor.
7. Compute the terminal value at the transition year using the **post-transition** (lowest) cost of equity and the stable growth rate. Discount it back at the cumulated factor for that year.
8. Sum. Compare against the single-rate alternatives to see how much the staging is worth.

**Reference data — the packet's staged setup.** Sector market beta = 1, average firm-market correlation = 0.25, riskfree rate = 4%, ERP = 5%.

| Stage | Owner | ρ | Perceived beta | Cost of equity |
|---|---|---|---|---|
| 1. Nascent business | Fully invested private owner | 0.25 | 4 | 4% + 4(5%) = 24% |
| 2. Angel/VC financing | Specialized VC with several tech holdings | 0.50 | 2 | 4% + 2(5%) = 14% |
| 3. Public offering | Diversified retail and institutional investors | 1.00 | 1 | 4% + 1(5%) = 9% |

**Worked example — the full valuation.** The owner holds the business for years 1–2, a technology VC funds it from the start of year 3 through year 5, and it goes public (or is sold to a public firm) at the end of year 5. Growth is 2% forever after year 5.

| | Yr 1 | Yr 2 | Yr 3 | Yr 4 | Yr 5 | Terminal year |
|---|---|---|---|---|---|---|
| E(Cash flow) | $100 | $125 | $150 | $165 | $170 | $175 |
| Market beta | 1 | 1 | 1 | 1 | 1 | 1 |
| Correlation | 0.25 | 0.25 | 0.5 | 0.5 | 0.5 | 1 |
| Beta used | 4 | 4 | 2 | 2 | 2 | 1 |
| Cost of equity | 24.00% | 24.00% | 14.00% | 14.00% | 14.00% | 9.00% |
| Terminal value | | | | | $2,500 | |
| Cumulated COE | 1.2400 | 1.5376 | 1.7529 | 1.9983 | 2.2780 | 2.4830 |
| PV | $80.65 | $81.30 | $85.57 | $82.57 | $1,172.07 | |

- `Terminal value = 175 / (0.09 − 0.02) = $2,500`, computed at the *public* cost of equity because the firm is public by then.
- Year 5 PV = `(170 + 2,500) / 2.2780 = $1,172.07`.
- **Value of firm with changing costs of equity = $1,502** (correct).
- Using 24% forever = **$1,221** — undervalues by 19%.
- Using 9% forever = **$2,165** — overvalues by 44%.

**Reference data — the implications for private company value:**

| Proposition | Consequence |
|---|---|
| A private business expected to become publicly traded is worth more than an identical one that will not | Later cash flows are discounted at the diversified investor's lower rate |
| Corollary: sector heat | Private businesses in sectors that are "hot" for going public (social media in 2014) are worth more than ones in less fashionable sectors |
| Corollary: IPO cycle | As IPOs boom, private company valuations rise; as IPOs bust, they fall |
| Corollary: market access | Private businesses in countries with easy access to public markets are worth more than those without |
| A private business that expects to go public *sooner* is worth more than one that will take longer | Fewer years discounted at the high early rates; private businesses gain when firms can list earlier in the life cycle |

**Determinism:**
- DETERMINISTIC: `{market beta, ρ per stage, riskfree, ERP} → perceived beta and cost of equity per stage`. `{yearly cash flows, per-year costs of equity, terminal growth, transition year} → cumulated factors → PVs → terminal value → firm value`. Fully scriptable.
- JUDGMENT: the ownership timeline and when each transition happens; the correlation assigned to each stage, especially the VC's portfolio correlation; the probability that the transition happens at all; and the cash-flow forecast. That judgment needs the financing plan, the state of the IPO market in the sector, and the VC's actual portfolio composition.

**Pitfalls:**
- Using one cost of equity for the whole life of the company. The packet's example misvalues by −19% or +44% depending on which rate you pick.
- Compounding a single rate to a power instead of building a running product of the yearly rates. `(1.24)^5` is not the right factor when years 3–5 discount at 14%.
- Computing the terminal value at the pre-transition cost of equity. The terminal cash flows belong to public investors and get the 9% rate.
- Assuming the transition will happen. If the IPO market closes, the low late-stage rates never arrive and the value falls back toward the single-owner case.
- Treating a VC as fully diversified. A specialized technology VC holds correlated bets; its correlation is between the founder's and the market's.
- Forgetting the flip side of Proposition 1. When IPO markets shut, private valuations should fall even if nothing about the business changed.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.128, p.153, p.167-169
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.126, p.151, p.164-166

**Related:** [[total-beta]], [[ipo-valuation]], [[ipo-pricing-and-underpricing]], [[private-to-public-sale]], [[private-company-valuation-framework]], [[private-company-cost-of-capital]], [[venture-capital-valuation]], [[young-company-valuation]]

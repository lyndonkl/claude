# Private company valuation: the framework

**Core idea:** Valuing a private company follows the same three steps as valuing a public one. Estimate the cash flows, attach a discount rate that reflects their risk, and take the present value — either of the whole business (FCFF at the cost of capital) or of the equity (FCFE at the cost of equity). Two problems make it different. There is no market value for the debt or the equity, which removes the inputs (debt ratios, betas, ratings) and the reasonableness check that public valuations rely on. And the financial statements go back fewer years, carry less detail, and have more holes. On top of that, the *answer depends on who is asking*: a private business does not have one value, it has a value per buyer and per purpose.

**Formulas:**
- `Value of business = Σ_t FCFF_t / (1 + Cost of capital)^t`, or `Value of equity = Σ_t FCFE_t / (1 + Cost of equity)^t`.
- `Cost of equity = Riskfree rate + Beta_relevant × ERP`, where `Beta_relevant` is the **total** beta for an undiversified buyer and the **market** beta for a diversified one. See [[total-beta]].
- `Final equity value = Equity value from DCF × (1 − Illiquidity discount) × (1 − Minority discount if applicable)`.

**Procedure:**
1. **Establish the motive.** It changes the assumptions and therefore the number.
   - *"Show" valuations*: curiosity ("what is my business worth?"), or legal purposes — estate tax, divorce court.
   - *Transaction valuations*: sale to another individual or private entity; sale of one partner's interest to another; sale to a publicly traded firm.
   - *Prelude to an IPO offering price.*
   - *Valuing a division of a public firm*: as a prelude to a spin-off, for sale to another entity, or inside a sum-of-the-parts test of whether the firm is worth more broken up.
2. **Classify the transaction into one of the four scenarios.** This determines the discount rate and the discounts:

   | Scenario | Buyer | Beta to use | Illiquidity discount |
   |---|---|---|---|
   | I. Private to private | Undiversified individual | Total beta | Yes |
   | II. Private to public | Diversified public company | Market beta | No |
   | III. Private to IPO | Diversified public investors | Market beta | No |
   | IV. Private to VC to public | Changes by stage | Stage-varying total beta | Fades out |

3. **Clean up the statements** before forecasting anything. See [[private-company-statement-cleanup]].
4. **Strip out key-person value** if the current owner is part of the product. See [[key-person-discount]].
5. **Build the discount rate** from bottom-up betas, adjusted for the buyer's diversification. See [[private-company-cost-of-capital]].
6. **Value the business**, then subtract debt (including capitalized leases) to get equity.
7. **Apply the discounts** the scenario calls for: illiquidity ([[illiquidity-discount]]) and, for a below-50% stake, lack of control ([[minority-discount]]).
8. **Sanity-check against the public alternative.** The owner of a private business can always put the money into publicly traded stocks instead. Whatever those can earn anchors the return demanded on the private business.

**Reference data:** The two structural problems and what they cost you:

| Problem | Specific consequences |
|---|---|
| No market value | No market D/E for levering betas or weighting the cost of capital; no market price to value employee options and warrants; no market price as a reasonableness check on your answer; no regression beta and no bond rating |
| Cash flow estimation | Shorter history, so less data; looser accounting standards than public firms face; personal expenses reported as business expenses; no clean line between "salaries" and "dividends" because both end up with the owner |

**Worked example:** The packet's running case is an upscale French restaurant, for sale by its owner, who is also the chef. The buyer is a former investment banker who will put his entire savings into it — completely undiversified. Last year: revenues $1.2 million, pre-tax operating profit $400,000, no conventional debt, a lease commitment of $120,000 a year for 12 more years. Three years of statements exist. Every structural problem shows up. There is no beta, no rating, no D/E, no owner salary, and a lease that is really debt. Working through the full procedure gives an equity value of $453,880 to the private buyer and $1,483,560 to a public buyer — the same business, more than three times the value. See [[private-to-private-valuation]] and [[private-to-public-sale]].

**Determinism:**
- DETERMINISTIC: the valuation arithmetic once the inputs are fixed, and the scenario-to-treatment mapping in step 2.
- JUDGMENT: the motive; who the likely buyer is; every statement-cleanup adjustment; the comparable set for betas; and the size of the discounts. Legal-purpose valuations are explicitly advocacy-driven — the assumptions and the value depend on which side of the divide you sit on.

**Pitfalls:**
- Treating a private business as having one value. It does not. Value is buyer-specific and motive-specific.
- Carrying a public-company valuation template across unchanged, keeping market beta and skipping the illiquidity discount for a private buyer.
- Accepting the reported statements. They mix personal and business expenses and usually understate the true labour cost of the owner.
- Forgetting that there is no market price to check your answer against, so an arithmetic or assumption error has nothing to bump into.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket2spr21 p.123-128, p.130, p.170
- valuations--lecture_notes--spring_2020--valpacket2spr20 p.121-126, p.128, p.167

**Related:** [[private-company-statement-cleanup]], [[private-company-cost-of-capital]], [[total-beta]], [[key-person-discount]], [[illiquidity-discount]], [[minority-discount]], [[private-to-private-valuation]], [[private-to-public-sale]], [[ipo-valuation]], [[vc-stage-varying-cost-of-equity]], [[sum-of-the-parts-framework]]

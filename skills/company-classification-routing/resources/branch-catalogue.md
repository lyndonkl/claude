# Branch catalogue B1–B16

One entry per branch. Each states the trigger, what breaks and why, what replaces it, the
extra inputs it needs, and the hard constraints it emits. Engines are B1 through B7 plus
B13 and B14. Overlays are B8, B9, B11, B12 and B16. B10 is a decomposition. B15 wraps an
engine.

Full detail, including the concept notes behind every claim, is in
`knowledge/frameworks/special-situations-routing.md` Part II.

---

## B1 · Young company, negative or trivial earnings

**Trigger.** `revenue_status == pre-revenue`, or `earnings_status ==
negative-structural`, or a start-up / young-growth firm that is not profitable. It also
fires for any firm whose losses come from the life cycle rather than a transient shock.

**What breaks.** Current earnings are meaningless, so every earnings multiple is
undefined. Growth from fundamentals breaks, because `g = RIR × ROC` needs a sustainable
return and ROC is negative. Historical growth is unusable off a tiny or negative base.
Regression betas are noise — Amazon in January 2000 showed a raw beta of 2.23 against an
R² of 0.17. Comparables often do not exist, because the business itself is young. And a
going-concern DCF overstates value, because failure is a live outcome.

**What replaces it.** Work backwards from a mature end-state.

1. Fix the base year: trailing revenues, adjusted EBIT, NOL balance, cash, debt, shares,
   options.
2. Choose the end-state first. Target pre-tax operating margin equals the mature sector's
   margin. Terminal growth stays at or below the riskfree rate. Terminal ROC equals the
   terminal cost of capital unless a moat is argued.
3. Set the revenue path backwards to that end-state and fade excess growth. Post-IPO
   excess growth over the industry decays to roughly zero by years five or six.
4. Ramp the margin to target by a stated convergence year.
5. Run the NOL engine: no tax while losses are absorbed, no refund in loss years, then
   effective rate rising to marginal.
6. Charge for growth through the sales-to-capital ratio. Roll invested capital forward and
   check imputed ROC each year.
7. Use a bottom-up sector beta fading toward 1.0, with the cost of capital falling as the
   firm matures.
8. Close the equity bridge. Value employee options with dilution-adjusted Black-Scholes
   and divide by the undiluted share count.
9. Apply the B4 failure adjustment outside the DCF.

**Extra inputs.** Mature-sector margin distribution; total addressable market, to test the
implied share; sector sales-to-capital; sector unlevered beta; NOL carryforward; the option
pool with count, average strike, average maturity and volatility; a sector survival table.

**Constraints.** `no-earnings-multiple`, `no-standard-growth-model`,
`require-failure-probability`, `no-normalization`. Also:

- No regression beta.
- No failure risk in the discount rate.
- No constant cost of capital across ten years, when the whole story is maturation.
- No separate dilution haircut on top of a DCF whose early FCFF is negative. Those
  negative flows *are* the dilution.
- No adding back stock-based compensation as a non-cash charge.

**Skill.** `special-situation-models young-company`, then `dcf-valuation-engine`.

---

## B2 · Mature firm in transition — status quo versus optimally run

**Trigger.** A mature firm with any of: `ROIC < WACC`; reinvestment far off the sector
norm; a debt ratio far from the sector optimum; an activist on the register; a control
contest; a restructuring mandate. It is the default engine for `mode == restructuring` and
the middle of the B15 chain.

**What breaks.** History is rich, but it describes policies that are about to be abandoned.
One DCF on current policy values a company that may not exist next year. One DCF on optimal
policy values a company that does not exist yet.

**What replaces it.** Value the same company twice, then weight.

1. Status quo: actual reinvestment rate, actual ROC, actual debt ratio.
2. Diagnose the three failures — invests too little or too much, earns below its cost of
   capital, wrong financing mix.
3. Operating restructuring: raise the reinvestment rate and the return on **new** capital,
   giving a new `g = RIR × ROC`. Then the larger lever, the return on **existing** assets,
   entered as an efficiency-growth term `[1 + (ROC_new − ROC_old)/ROC_old]^(1/n) − 1` spread
   over `n` years and not applied in perpetuity.
4. Financial restructuring: run the cost-of-capital schedule from 0% to 90% debt in
   ten-point steps, relevering beta and resetting the synthetic rating at each step. Cap
   the tax benefit where interest exceeds EBIT. Take the minimum-WACC ratio.
5. Value of control is optimal minus status quo. Expected value is
   `status quo × (1 − p) + optimal × p`.
6. Set `P(change)` from ownership and voting structure, takeover defenses, board
   composition, activist presence, access to challenge funding, firm size, and the
   empirical turnover determinants.
7. Read the market's own odds: `P_implied = (Price − StatusQuo)/(Optimal − StatusQuo)`. A
   value at or outside `[0, 1]` means an input is wrong, not that you found something.

**Constraints.** `no-governance-discount`. Also:

- Never quote the optimally-run value as *the* value without a probability.
- Never use a fixed control-premium percentage. A perfectly run firm has a control premium
  of zero.
- Never change the discount rate between the two scenarios, except through the deliberate
  capital-structure change.
- Never assume margin improvement without evidence of management commitment.
- Never raise the reinvestment rate while `ROC < WACC`. That accelerates value destruction.
  For a sub-WACC firm the value-creating move is usually to shrink and return capital.
- Discount the value gain for implementation delay.

**Skill.** `dcf-valuation-engine` twice, plus `cost-of-capital-toolkit debt-schedule`.

---

## B3 · Declining firm

**Trigger.** Multi-year declining revenue and `life_cycle_stage == decline`. Usually thin
margins and a material share of capital earning below the cost of capital.

**What breaks.** The long history describes a shrinking business, so extrapolation is worse
than useless. Standard templates assume positive growth and positive reinvestment. Both
signs are wrong here.

**What replaces it.** A negative revenue growth path with an explicit moderation schedule
toward zero. Margin recovery to the sector median rather than to the firm's own better
past. Negative reinvestment, since `Reinvestment = ΔRevenue / (Sales/Capital)` goes
negative automatically as revenues fall. FCFF can exceed EBIT(1−t), and that is arithmetic
rather than an error. Tax rate rises toward marginal as shields run out. Stable-phase
`RIR = g/ROC` is negative when `g < 0`. Hand off to B4 whenever survival is in doubt.

**Extra inputs.** Sector median margin; asset-disposal schedule and expected proceeds;
pension underfunding, litigation claims, liquidation preferences; bond prices or rating.

**Constraints.** `require-failure-probability` where leverage is material,
`no-normalization`. Also:

- Never force positive growth because the template assumes it.
- Never floor reinvestment at zero beyond year one. That discards the real cash released.
- Never anchor the terminal margin on the firm's own peak.
- Include the equity-side claims that decline exposes: pension shortfalls, litigation,
  liquidation preferences.

---

## B4 · Distress and failure adjustment

**Trigger.** Any distress marker from S6. Applies as an outer wrapper to whatever engine
ran.

**What breaks.** The DCF assumes survival to stable growth. If the firm may die first and
its assets would fetch less than the present value of expected cash flows, the DCF
overstates value. Raising the discount rate does not fix this, and doing both counts the
risk twice.

**What replaces it.**

- `Value = Going-concern × (1 − p) + Distress proceeds × p`, at firm or equity level.
- Partial-wipeout form when the firm survives but equity is diluted or expropriated:
  `V × (1 − p × loss_fraction)`.
- Proceeds basis: a percentage of book, or of going-concern value. Default 50%, cut
  further when the whole sector is selling the same assets at once.
- Equity is a residual. If proceeds fall short of the face value of debt, distress-branch
  equity is zero.
- Probability sourcing, in ascending information content: sector survival table, then the
  rating-implied cumulative default rate, then a statistical model, then an inverted traded
  bond price. To invert, price the promised coupons and principal, weight by `(1−π)^t`,
  discount at the **riskfree** rate, and solve for π. Convert to a cumulative probability
  over the forecast horizon.
- Cross-check with the option lens when `market D/(D+E) > 50%` and earnings are negative.
  Equity is a call on firm value struck at the face value of debt, with a life equal to the
  face-value-weighted duration of the debt.

**Constraints.** `require-failure-probability`, `single-charge-per-risk`. Also:

- Never raise the discount rate for failure and also probability-weight.
- Never shrink expected cash flows for failure and also probability-weight.
- Never report an annual probability where the model needs a cumulative one.
- Never assume generous recovery in an economy-wide downturn.
- Never assume equity retains value when expected proceeds fall short of debt face value.
- Keep firm failure and equity wipeout distinct.
- The option cross-check is an alternative equity estimate. It is never additive to the DCF
  equity value.

**Skill.** `special-situation-models distress`; `option-valuation-toolkit equity-as-call`
for the cross-check.

---

## B5 · Financial service firms

**Trigger.** `sector_type == financial-service`. Highest precedence in S2. Also fires for
any division that is a bank or a captive finance arm inside a B10 decomposition.

**What breaks.**

- Debt is raw material rather than financing. Deposits, repos and short-term funding are
  inputs to the business. Operating and financing decisions cannot be separated, so FCFF
  and the cost of capital are meaningless and there is no meaningful firm value.
- Reinvestment is undefined in the ordinary sense. Capital expenditure and working capital
  have no clean meaning.
- Statements do not fit the template. Revenue is reported net, interest expense is an
  operating cost, credit-loss provisions are recurring operating expenses, and property and
  equipment is negligible.
- Manufacturing rating tables mis-price them. Financial firms run at far thinner coverage,
  so the standard coverage-to-spread mapping assigns absurd ratings.
- Breaching a regulatory capital ratio, computed on **book** equity, can shut the firm down
  regardless of earnings. Nothing else in the catalogue has that property.

**What replaces it.** Value equity directly, by one of three routes.

1. **Dividend discount model**, the default. Growth equals retention times *sustainable*
   ROE. Sustainable ROE adjusts trailing ROE for any required increase in the capital base,
   `ROE_sustainable = ROE_trailing / (1 + required capital increase)`, and for leverage the
   regulator will no longer permit. Fade payout up toward `1 − g/ROE` as ROE falls.
   Terminal ROE equals the cost of equity unless a durable franchise is argued.
2. **FCFE to regulatory capital**, when payout no longer reflects capacity, in a crisis, or
   when capital ratios are moving. Reinvestment is the addition to regulatory equity:
   `Investment = ratio_t × RWA_t − ratio_{t−1} × RWA_{t−1}`, and
   `FCFE = Net income − that investment`. Expect deeply negative early FCFE while capital
   is rebuilt. Anchor the target ratio on the peer percentile distribution.
3. **Equity excess-return model**:
   `Value = current book equity + PV of (Net income − cost of equity × beginning book
   equity)`. Book equity is meaningful here because assets are marked to market.

Add an equity-wipeout probability for a bank in genuine crisis. A rescued bank's equity is
often worth nothing.

**Extra inputs.** The risk-weighted assets path. Current and target Tier 1 or CET1 ratios,
with the peer percentile that anchors the target. An ROE recovery path, also anchored on
peer percentiles. One-off capital hits such as fines and settlements. Preferred stock,
which is a real claim ahead of common. The bank-sector beta.

**Constraints.** `no-fcff-valuation`, `no-optimal-debt-ratio`, `no-enterprise-multiple`.
Also:

- Never apply debt-to-capital ratios, EBITDA, or manufacturing rating tables.
- Never treat the loan-loss provision as extraordinary.
- Never use trailing ROE as terminal ROE, or when the regulator is about to demand more
  capital.
- Never leave the payout ratio at its high-growth level while ROE falls. The relation
  `payout = 1 − g/ROE` links them.
- Never model dividends or buybacks while FCFE after regulatory-capital investment is
  negative.
- Never mix a hard-currency cost of equity with local-currency earnings.
- Downstream, the `capital-structure` and `payout` stages are suppressed. Only the
  regulatory-capital equity plan runs.

**Skill.** `special-situation-models excess-return`.

---

## B5b · REIT and mandated-payout vehicles

**Trigger.** `sector_type == real-estate/REIT`.

Mandated payout and tax status make optimal-debt-ratio work and retention-based growth
analysis meaningless. Value on dividends or FFO. Exclude the firm from any
corporate-finance financing recommendation. All other routing proceeds normally.

**Constraints.** `no-optimal-debt-ratio`, `no-enterprise-multiple`.

---

## B6 · Commodity companies

**Trigger.** A macro price driver exists and explains revenues. Regress revenues on the
commodity price over as long a history as available and report the R².

**What breaks.** Value depends on a price nobody forecasts reliably. Embed your own price
view and the answer becomes a blend of two opinions, with no way for a reader to tell which
is doing the work. Trough or peak margins mistake a point in the cycle for the business.
Reserves cap growth permanently.

**What replaces it.** Separate macro from micro.

1. Establish the revenue-price link empirically and report the R².
2. Set base revenue from today's market price or the futures strip. Never from your own
   forecast.
3. Normalize the margin toward the long-run average, and the terminal ROC to the long-run
   average return.
4. Grow revenues at the firm's own historical compounded rate unless there is a reason to
   differ.
5. State the answer as "worth X at today's commodity price".
6. State the macro view separately, then quantify it. Rerun at other prices, or draw the
   price from a right-skewed distribution and simulate.
7. Undeveloped reserves are a call option, routed to B12. Developed reserves are the DCF.
8. Run the optimal-debt schedule on both current and normalized EBIT, and report both
   optima.

**Constraints.** `require-normalized-earnings`. Also:

- Never embed a proprietary commodity forecast in the base valuation.
- Never use trough or peak margins as forecast margins.
- Never treat reserve life as irrelevant.
- Never value producing reserves as options, or undeveloped reserves as an annuity.
- Never present a single point estimate when the driver is a volatile price. The simulation
  costs almost nothing.
- Never recommend a large debt increase off peak-cycle earnings.

**Skill.** `special-situation-models cyclical`; `option-valuation-toolkit` for reserves.

---

## B7 · Cyclical or temporarily troubled firm — normalization

**Trigger.** `earnings_status` in {negative-transient, cyclical-trough, cyclical-peak} and
the cause is temporary. Evidence for temporary: a known sector downturn, peers showing the
same pattern, years of normal margins, and a balance sheet that survives until recovery.
Evidence against: falling market share, a structural demand shift, leverage forcing asset
sales.

**What breaks.** The base year is not representative. Growth off a depressed base is
meaningless. Ratings computed off trough EBIT are wrong, which makes the cost of debt
wrong.

**What replaces it.** One of three normalization approaches, chosen by the data available.

1. **Average earnings** over a full cycle, typically five years. Only when firm size has
   not changed much.
2. **Average return on capital times current book capital.** Use when the firm has grown,
   so old dollar earnings understate today's business.
3. **Sector or own aggregate historical operating margin times current revenues.** The
   default when revenues are meaningful and margins collapsed. Use the aggregate margin
   `ΣEBIT / ΣRevenues`, not an average of yearly ratios.

Then recompute everything derived: coverage, synthetic rating, cost of debt, lease
capitalization, restated EBIT. Iterate to a fixed point. If recovery takes time, ramp
toward the normalized level rather than jumping to it in year one. A normalized mature firm
may deserve no high-growth period at all.

**Constraints.** `require-normalized-earnings`, `no-earnings-multiple` on the un-normalized
year. Also:

- Never normalize a permanently broken business. Route it to B1 or B4 instead.
- Never dollar-average across a period in which the firm changed size materially.
- Never average ratios where the model wants the aggregate.
- Never choose a window that runs from trough to peak.
- Never normalize earnings *and* assume a separate recovery.
- Never leave a depressed coverage ratio in the rating while using normalized EBIT in the
  cash flows, or the reverse.

**Skill.** `financial-statement-normalization normalized-earnings`.

---

## B8 · Intangible-heavy firms (overlay, applied in S3)

**Trigger.** Material R&D at pharma, technology or biotech firms; material recruiting and
training at human-capital firms; material brand-building advertising at consumer-products
firms. Screen on `R&D / revenues` and `R&D / (R&D + net capex)`.

**What breaks.** Accounting expenses what is economically a capital expenditure. So
operating income is understated, invested capital is understated, reinvestment is
invisible, and ROIC, ROE, the reinvestment rate, the sales-to-capital ratio and the
interest coverage ratio are all wrong — at exactly the firms where growth matters most.

**What replaces it.** Capitalize before any valuation.

- Choose the amortizable life from the industry lookup: two years for retail and services,
  three for software and consumer brands, five for light manufacturing and semiconductors,
  ten for pharma, aerospace and heavy manufacturing.
- `Research asset = Σ_k R&D_{−k} × (N−k)/N`; `Amortization = Σ_{k≥1} R&D_{−k}/N`;
  `ΔEBIT = current R&D − amortization`. That last term can be negative when R&D spending
  is shrinking.
- Add the research asset to book equity and invested capital. Add current-year R&D to
  capital expenditure.
- Recompute ROE and ROC. They usually fall, because capital rises proportionally more than
  income.
- Recompute coverage, and therefore the synthetic rating and the cost of debt.

**Constraints.** `require-rd-capitalization`. Also:

- Never expect the fix to improve returns.
- Never add the research asset to capital while leaving R&D out of capital expenditure.
  That manufactures free growth.
- Never assume the EBIT adjustment is positive.
- Never use a single amortizable life across a diversified company.
- Never apply the restated ROC to set growth while leaving the reinvestment rate on the old
  basis.
- Never treat the whole advertising budget as capital.
- Propagate the restatement into coverage, rating and cost of debt.
- Brand value computed separately is not added on top of a valuation that already carries
  the brand-driven margin.

**Skill.** `financial-statement-normalization capitalize-rd`.

---

## B9 · Emerging-market and country risk (overlay)

**Trigger.** Material revenue, production or asset exposure to markets with sovereign risk.
Assigned by exposure, not by passport. A Brazilian exporter carries less Brazil risk than a
Brazilian retailer. Coca-Cola and Heineken carry plenty of emerging-market risk while
incorporated in developed markets.

**What breaks.** All four questions bend at once. Inflation and rate shifts plus weak
accounting distort the earnings history. Growth is tied to the country. Country risk moves
and a domestic beta does not capture it. Crises, nationalization and regime change can end
the story. Equity value is distorted by cross-holdings. The usual fixes — a discount-rate
bump, a flat emerging-market discount, a governance haircut — are unfalsifiable and often
triple-count.

**What replaces it — a four-part stack on top of an ordinary DCF.**

1. **Currency first.** Value in any currency; the answer must be invariant. Build the
   riskfree rate from a genuinely default-free bond in that currency, or from a reliable
   riskfree rate plus the inflation differential:
   `(1+r_X) = (1+r_US) × (1+i_X)/(1+i_US)`. Strip the sovereign default spread out of a
   local government bond before using it. Use PPP-consistent expected exchange rates rather
   than a flat spot rate across ten years. Cross-check by re-running in a second currency.
2. **Country risk by exposure.** `CRP = country default spread × relative equity market
   volatility`, and `ERP_country = mature ERP + CRP`. Attach it as a revenue-weighted ERP,
   `ERP_company = Σ w_i × ERP_i`, when a geographic revenue split exists. Use a lambda,
   `k_e = r_f + β × mature ERP + λ × CRP`, when exposure differs from the revenue split
   because of production location, sourcing, hedging or demand sensitivity. A lambda of 1
   is average domestic exposure; exporters sit well below it. Add the country default
   spread to the cost of debt as well.
3. **Cross-holdings**, routed to B11.
4. **Truncation** sub-branch: nationalization, regime change, war, uninsurable catastrophe.
   These do not reduce cash flows, they end them. Build the branch as its own DCF wherever
   possible, since partial expropriation and harsher fiscal terms are far more common than
   total loss. Assign a probability and blend. State that probability prominently; it is
   the only genuinely subjective input.

**Constraints.** `require-exposure-weighted-risk`, `no-blanket-country-discount`,
`no-governance-discount`. Also:

- Never assign country risk by country of incorporation.
- Never apply a country premium *and* a blanket emerging-market value discount.
- Never stack a country premium, a nationalization scenario and a governance discount.
  That is three charges for overlapping risks.
- Never put a country premium in the cost of equity while forgetting the country spread in
  the cost of debt.
- Never hold the country premium at its current level in perpetuity without saying so.
- Never discount local-currency cash flows at a hard-currency cost of capital.
- Never let stable growth exceed the currency's own riskfree rate.
- Never change the ERP because the currency changed. The ERP tracks operating exposure.
- Never set the truncated branch to zero by reflex.
- Never use a lambda you cannot justify. Fall back to revenue weighting and say so.

**Skill.** `cost-of-capital-toolkit` for the riskfree derivation, ERP build-up and currency
conversion.

---

## B10 · Multi-business firms and sum-of-the-parts

**Trigger.** `business_count > 1` with distinct economics and separable cash flows; or a
division being valued for a spin-off or sale; or a mandate asking whether the firm is worth
more broken up.

**Feasibility test first.** Separability, traceable cash flows, and an active market in
similar assets. The more of the three that fail, the less defensible the result. Brand name
is the canonical failure: it cuts across every asset and cannot be carved out.

**Motive determines the route.**

| Who is asking | Route |
|---|---|
| Passive investor betting on a mispricing | Intrinsic sum-of-the-parts, divisional DCFs |
| Activist, acquirer or board considering a break-up | Relative sum-of-the-parts, each division priced off its sector |
| Liquidator | Price assets off comparable transactions; add an urgency discount if forced |
| Accountant under a fair-value mandate | Exit price: level 1 quotes, then level 2 observable inputs, then level 3 model — report which level |
| Firm preparing a spin-off | Relative for the transaction price, intrinsic for the reservation price |

**What breaks.** One company-wide cost of capital and one company-wide multiple across
divisions of different risk is the most common error here, and it moves the answer a lot.
Segment EBIT is often reported before corporate G&A, so divisional values double-count the
missing overhead. A captive finance arm follows bank logic.

**What replaces it.** A per-division cost of capital, from that division's sector unlevered
beta levered at the parent's D/E unless the division would carry different debt standalone.
Per-division fundamentals: `ROC = after-tax EBIT / invested capital`, `RIR = allocated
reinvestment / after-tax EBIT`, `g = RIR × ROC`. Capitalize unallocated corporate expenses
as an after-tax growing perpetuity at the company-wide cost of capital and subtract them.
Bridge once, at the end. Then compare four numbers: intrinsic SOTP, relative SOTP,
whole-company DCF, and market enterprise value. The spread is the finding.

**Constraints.** `require-divisional-rates`, `zero-growth-below-cost-of-capital`. Also:

- Never apply one cost of capital or one multiple across divisions.
- Never drop unallocated corporate expenses.
- Never mismatch a multiple and its scalar.
- Never forget a captive finance arm's debt in the bridge.
- Never value a bank division on FCFF. Apply B5 to it and add it as an equity block.
- Never read a conglomerate discount as automatic free money. The pieces may also be worth
  less apart, where real synergies exist.
- Never add back going-concern items such as brand or assembled workforce in a liquidation
  frame.

---

## B11 · Cross-holdings and group structures (overlay, applied in the bridge)

**Trigger.** Any consolidated subsidiary that is less than wholly owned; any minority stake
in another firm; pyramid or circular group ownership; a material `holdings_share`.

**What breaks.** In many group companies the real work starts after the DCF, because half
the value sits in stakes in other companies valued with very little information. A perfect
operating DCF can still be half a valuation.

**What replaces it.** List every holding with its ownership percentage and accounting
treatment. For a majority consolidated stake, the subsidiary is already inside operating
income, so subtract the minority interest at estimated **market** value. For a minority
unconsolidated stake, it is not in operating income, so add `ownership % × value of
subsidiary equity`. Value that properly if listed. If opaque, apply a sector price-to-book
or earnings multiple to its book equity and disclose the approximation. Report the value
composition and flag prominently when holdings exceed roughly a third, because the error
bars then live in the holdings rather than the DCF.

**Constraints.** `require-market-value-minorities`. Also:

- Never mark holdings at book value.
- Never subtract book minority interest.
- Never add a stake's value while its earnings remain in operating income.
- Never flip majority and minority treatment. The sign of the adjustment reverses.
- Never consolidate a joint venture's operating assets and also carry its equity value as a
  holding.

---

## B12 · Real options (overlay; gated, and most candidates fail)

**Trigger.** Any item on `option_candidates`: product patents, undeveloped reserves,
exclusive licences or development rights, contractual abandonment rights, expansion rights,
excess debt capacity, and equity in a deeply levered loss-making firm.

**The gate — three sequential tests. All three pass before any premium is admissible.**

1. **Option test.** Name a clearly defined underlying asset whose value changes
   unpredictably, and a payoff contingent on a specified event within a finite period. If
   you cannot name both, there is no option.
2. **Exclusivity test.** In a perfectly competitive product market no contingency generates
   positive NPV, however volatile the underlying, because competitors compete the excess
   return away. Score the barrier: first-mover advantage is weakest, then a technological
   edge, then brand name, then licences, then pharmaceutical patents. Apply the three
   sliding scales — is the first investment a prerequisite for the second, is there a
   competitive advantage on the second, will the second earn excess returns. Any scale at
   zero makes the option worth zero, whatever the model returns.
3. **Pricing test.** Is the underlying traded, with an observable price and volatility? Is
   the option itself traded? Is the exercise cost knowable? Trust the output in proportion
   to how many hold.

**Routing after the gate.**

| Candidate | Structure |
|---|---|
| Product patent | Call. `S` = PV of cash flows from launching now, `K` = development cost, `t` = patent life, `y = 1/n`. Compute the optimal exercise date where option value crosses `S − K`. |
| Undeveloped reserves | Call. `S = reserves × (price − production cost) / (1+y)^lag`, `K = reserves × development cost`, `t` = relinquishment life. The development lag and the net-production-revenue yield are both mandatory. |
| Expansion into a new market | Call on the expansion's PV struck at entry cost. The noisiest application; scale hard by the exclusivity factor. |
| Abandonment right | Put. `S` = PV of remaining flows, `K` = salvage, `t` = life of the exit right, not of the project. Requires a counterparty obliged to buy. |
| Financing flexibility | Call on reinvestment needs, scaled by `excess return / WACC`, compared against the cost `current WACC − optimal WACC`. Zero excess returns make flexibility worth zero. |
| Equity in a distressed levered firm | Call on firm value struck at debt face value, life equal to face-value-weighted duration. An alternative equity estimate, never additive. |

**Engine choice.** Prefer a binomial tree when early exercise matters or values jump, which
is the normal case for real assets. Use Black-Scholes only for continuous processes without
jumps, and always in its dividend-adjusted form. When the pricing test fails but tests one
and two pass, use a decision tree instead.

**Constraints.** `require-exclusivity-scaling`, `no-option-premium-without-gate`. Also:

- Never add a premium without running the exclusivity test. Most real options are worth
  nothing precisely because anyone can exercise them.
- Never use volatility to rescue a case with no barriers. High variance multiplies zero.
- Never double count. Remove the patent's or the reserve's growth from the DCF once it is
  valued as an option.
- Never build a decision tree *and* add an option premium. They represent the same
  optionality.
- Never omit the cost-of-delay yield, or the development lag on a resource option.
- Never value producing reserves as options.
- Never use equity volatility where the model needs firm-value variance.
- Never quote a real-option value to the dollar.

**Skill.** `option-valuation-toolkit`.

---

## B13 · Private companies

**Trigger.** `ownership == private` and the mandate is not an IPO.

**What breaks — two structural problems.** First, no market value: no market D/E for
levering betas or weighting a WACC, no regression beta, no bond rating, no market price for
employee options, and no market price to bump into when you make an error. Second, weak
statements: short history, looser accounting, personal expenses run through the business,
and no clean line between salaries and dividends when both reach the same person.

**Mandatory pre-steps, in order.** The order matters, because the coverage ratio that sets
the cost of debt uses the lease expense from step one, and the key-person haircut precedes
the growth calculation.

1. **Statement cleanup.** Capitalize operating leases as debt at the pre-tax cost of debt.
   Charge a market salary for the owner's actual role. Strip genuinely personal expenses.
   Note whether the business is at full capacity, since revenue growth then requires
   capital expenditure.
2. **Key-person haircut.** Haircut operating income by the fraction `k` of the business
   that walks out with the owner. Judge `k` from customer concentration, personal
   referrals, and whether reputation attaches to the person or the establishment. It is
   applied to income, so it flows through cash flows, reinvestment and terminal value
   together. Transition terms, non-competes and earn-outs shrink it.
3. **Discount rate.** Bottom-up unlevered beta from comparables chosen on business
   economics rather than industry label. Convert to a total beta, `market beta / ρ` with
   `ρ = sqrt(average comparable R²)`, if the buyer is undiversified. Lever at the
   industry-average market D/E, because using your own estimated values is circular.

**The four sub-scenarios.**

| # | Scenario | Beta | Illiquidity discount |
|---|---|---|---|
| B13-I | Private to private, undiversified individual buyer | Total beta | Yes |
| B13-II | Private to public company | Market beta | No |
| B13-III | Private to IPO | Market beta | No — routes to B14 |
| B13-IV | Private to VC to public | Stage-varying perceived beta | Fades out |

A partially diversified buyer, such as a PE or VC fund, sits between I and II. Use that
fund's own portfolio correlation with the market. In B13-IV, discount each year's cash flow
by a cumulated product of that year's rate, never by a single rate raised to a power, and
use the post-transition rate for terminal value.

**Stake size.** Above 50%, price off the optimal value. At or below 50%, price off the
status quo value. `Minority discount = (Optimal − Status quo)/Optimal`, derived from two
valuations rather than from a convention. Illiquidity and lack of control are different
frictions; applying both to one stake needs a reason.

**Illiquidity routes.** Pick one and say which. The bid-ask spread regression evaluated at
zero trading volume is the most firm-specific:
`0.145 − 0.0022·ln(Revenues $m) − 0.015·DERN − 0.016·(Cash/Firm value) − 0.11·(Volume/Firm
value)`. Alternatively a Silber-refined base, shifting a 25% base by the gap between the
predicted discount for the subject firm and for a $10m-revenue profitable anchor. A flat
20–30% is a sanity check only.

**Constraints.** `require-total-beta` for an undiversified buyer,
`require-illiquidity-discount` unless the buyer is public and liquid,
`require-key-person-haircut-on-income`. Also:

- Divide by the correlation `ρ = sqrt(R²)`, not by R².
- Never apply a full total beta to a partially diversified fund.
- Lever the beta and weight the WACC at the same D/E. Keep `D/E` distinct from `D/(D+E)`.
- Apply the illiquidity discount to equity value, not to firm value.
- Never apply the key-person haircut to final value.
- Never double-count the owner salary adjustment with the key-person haircut. The first
  prices the owner's work, the second the owner's pull.
- Never skip the capitalized lease debt in the final bridge after adding it to the capital
  structure.
- Never read three good years as a trend.
- Never quote one number to both sides of a negotiation. Both valuations are correct, and
  they answer different questions.

**Skill.** `special-situation-models private`.

---

## B14 · IPO

**Trigger.** `transaction_motive == ipo`, or a private company being valued as a prelude to
an offering price.

**What breaks.** Two things change with the listing: control, since the firm becomes
subject to monitoring by investors, analysts and the market; and disclosure. The buyers are
diversified, so the private-company risk identity no longer applies. Three IPO-specific
adjustments then sit between a correct business valuation and a correct per-share number.

**What replaces it.**

1. Value the business as an ordinary DCF, with market betas and no illiquidity discount.
   Let the cost of capital decline over the forecast as risk falls. If the firm is young
   and loss-making, the engine is still B1.
2. **Use of proceeds**, read from the prospectus. Taken out by existing owners adds
   nothing. Used to pay down debt changes the debt ratio, so recompute the cost of capital
   and revalue. Retained for future reinvestment adds dollar for dollar. Split uses add
   only the retained portion.
3. **Prior equity claims.** Enumerate founder shares, every round of convertible preferred,
   restricted stock units, employee options, and shares owed under acquisition agreements.
4. **Share count.** Everything that is or becomes common goes in the denominator. Options
   stay out of the denominator and their value comes out of the numerator. Use an expected
   option life, not the stated life.
5. **Pricing is a separate question from value.** The banker sets the offer price under a
   pricing guarantee that pushes it below fair value. Expect underpricing, largest for the
   smallest deals, with 10–15% a working assumption. The cost to the owner is
   `underpricing % × value of the shares actually sold`, which is why small initial floats
   are common.

**Constraints.** `no-illiquidity-discount`. Also:

- Never use a total beta.
- Never add proceeds the existing owners are withdrawing.
- Never count options in the denominator *and* subtract their value.
- Never omit convertible preferred, RSUs, or shares owed under acquisition agreements.
- Never hold the cost of capital constant for a young company.
- Never present the offer price as the valuation, nor peer-multiple pricing as a value.
- Never price off a metric the market has stopped paying for.

---

## B15 · Acquisition analysis

**Trigger.** `transaction_motive == acquisition`. Wraps whichever engine the target's own
classification selected.

**The prior.** Acquirers usually destroy value, and the failure is structural. Target
shareholders capture nearly all the announcement gain. Bidders capture roughly nothing and
drift negative. The burden of proof belongs on the deal, not on the skeptic.

**Only three value reasons exist:** undervaluation, control, synergy. Anything else is not
a value reason. All four numbers get produced.

| # | Number | Source |
|---|---|---|
| 1 | Acquisition price | Negotiated; for a public target, a premium over pre-announcement market cap |
| 2 | Status quo value | Full DCF of the target as currently run, B2 step 1 |
| 3 | Restructured value | DCF with changed investing, financing and payout policy, B2 |
| 4 | Synergy value | `Combined with synergy − [Acquirer standalone + Restructured target]` |

**The acid test.** Undervaluation requires `Price < Status quo`. Control requires
`Price < Restructured`. Synergy requires `Price < Restructured + Synergy`. If price exceeds
the benchmark, exactly two explanations survive: the synergy was underestimated, or the
acquirer is overpaying. Decide which and say so.

**Seven disciplines, run before commitment.** Discount the target at the target's own cost
of equity. Use the target's own debt capacity and cost of debt, since added capacity in the
combined firm is a financial synergy valued separately. Derive the control premium as
restructured minus status quo. Map every claimed synergy to exactly one valuation input,
splitting cost synergies from revenue synergies, because cost synergies land and revenue
synergies mostly do not. Treat precedent-transaction multiples as a sample of
overpayments. Reconstruct the chronology to catch a valuation dated after the price. Name
the individual whose compensation depends on the promised benefits arriving.

**Constraints.** `require-target-own-discount-rate`, `synergy-baseline-is-restructured-target`,
`no-exit-multiple-terminal-value`. Also:

- Never use a fixed control-premium percentage.
- Never let the combined firm inherit a lower cost of capital purely from combining.
- Never report accretion or dilution as a deal test. EPS accretion is guaranteed whenever
  `PE_acquirer > PE_target`, and it carries no information.
- Never pay the full value of control or the full synergy value. That hands the entire gain
  to the seller.
- Verify the identity: the no-synergy combined value equals the sum of the standalone
  values exactly. If it does not, an assumption is inconsistent.

**Skill.** `project-investment-analysis synergy`.

---

## B16 · Macro shock and market-level revaluation (overlay)

**Trigger.** A material move in the macro inputs between the last valuation and the
valuation date — riskfree rate, equity risk premium, default spreads, base earnings, tax
regime — or an explicit mandate to value an index.

**What breaks.** Intrinsic value is not a fixed anchor the market wanders around. It is
built from macro inputs, and those move violently in a crisis. Treating a fall in your own
value estimate during a crisis as a mistake is itself the mistake.

**What replaces it.** Index valuation takes six inputs.

- Base aggregate earnings.
- Augmented cash returned, meaning dividends plus buybacks. Buybacks are now as large as
  dividends, and total payout regularly exceeds 100% of earnings in stress years.
- An earnings path split into transitory and permanent damage, with a stated recovery
  fraction and year.
- A payout path that falls and then recovers.
- A required return of `riskfree + ERP`, anchored on the historical average of the implied
  premium over a stated window.
- Perpetual growth capped at the riskfree rate.

Company revaluation in a shock changes four things. Base earnings. Growth inputs, usually a
lower reinvestment rate or a lower ROC. The ERP and the default spread, which both spike.
And the capital-structure path, if the firm can no longer move to target. Attribute the
change in value to each input separately, so the story is auditable.

**Constraints.** Never value an index off dividends alone. Never combine analyst growth
with an unadjusted payout ratio, since `payout = 1 − g/ROE` links them. Never assume the
crisis riskfree rate and the crisis ERP both persist forever, because they usually revert
in opposite directions and the terminal value is where that matters. Never change several
macro inputs without attributing the value change to each.

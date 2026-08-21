# Template: `valuation` mode

The question is what the company is worth and whether to buy, sell or hold. The terminal
artifacts are `11-verdict/verdict.json` and `11-verdict/REPORT.md`.

The structure below is derived from the graded equity valuation project: narrative, then
intrinsic value, then two independent pricing benchmarks, then reconciliation into one
call. The sequence is a triangulation. No single method is trusted alone, and the reader
is shown the disagreements rather than an average that hides them.

## Sections in order

### 1. Verdict

One screen. Nothing below it is required to act on the call.

- The recommendation: buy, sell or hold, with a horizon.
- Value per share, price per share, the gap, price as a percent of value.
- The range: low, base, high, with the label of what produced it.
- Margin of safety: the gap net of the range.
- The two or three assumptions the answer turns on, one line each.
- The named catalyst and the named risk.
- Confidence, with the reason.
- A flag if any high-severity finding is unresolved.

### 2. Mandate and basis

From `00-mandate/mandate.json`. Company, ticker, mandate currency, valuation date, share
count basis, and whether this is a going-concern or liquidation frame. State the bias
exposure in one line: who asked, what answer they want, whether price was seen before the
qualitative work.

### 3. The narrative

From `03-narrative/narrative.md` and `drivers.json`. The story in one paragraph, in prose.
Then the claim ledger: each claim graded probable, plausible or possible, and the single
driver it was routed to. A claim routed twice is double counted; a claim routed nowhere is
decoration.

Say which claims a reader would have to reject to reject the valuation.

### 4. Classification and route

From `02-diagnosis/classification.json`. Life-cycle stage, earnings status, sector type,
ownership, intangible intensity, distress markers. The `primary_path` chosen and the
`overlays` applied.

List the `constraints` the classification imposed and confirm each was honored. A reader
who knows this is a bank, a cyclical at a trough or a money-loser needs to see that the
standard machinery was not run on it. Carry the `confidence` field and the `unresolved`
list — what would change the routing.

### 5. What was restated

From `04-financials/adjustments.md`. Not the full adjustment log — the material ones, with
their effect on the numbers a reader will meet later.

- Operating leases capitalized: lease debt, restated EBIT, restated interest, invested
  capital. Note that net income is unchanged.
- Research and development capitalized: research asset, amortization, restated operating
  income and capital. Note that free cash flow to the firm is unchanged.
- One-time items stripped, with the recurrence test that justified each.
- The tax rate chosen, effective against marginal, and any loss carryforward balance.
- Normalization: whether the base year was normalized, on what basis, over what window,
  and why the cause called for it.

State the base return on invested capital after restatement. That number governs how much
the growth story can claim.

### 6. The discount rate

From `05-capital/cost-of-capital.md`. The build-up as a table. It carries the riskfree
rate with its derivation, the mature equity risk premium, and the country risk premium
with its exposure weights and attachment mechanism. Then the bottom-up beta with its
business weights, the cost of debt with its rating route, the market-value weights, the
cost of equity and the cost of capital.

Confirm the currency matches the mandate currency. That is what gate `G4_discount_rate`
checks, and a currency mismatch invalidates everything downstream.

Show the rate path if it fades, not just the opening rate.

### 7. The forecast

From `06-intrinsic/forecast.json`. Do not print ten years of every line. Print the drivers
and the shape.

- Revenue growth path, or the revenue level at years 5 and 10 in absolute currency.
- Operating margin path and the target margin, with the peer anchor for the target.
- Reinvestment: the sales-to-capital ratio or the reinvestment rate, against the industry.
- The implied return on invested capital each year, and the marginal return over the
  forecast.
- The tax path.
- The terminal block: growth, return on capital, cost of capital, reinvestment rate.

Show the growth, reinvestment and return triple together. Growth is bought with
reinvestment at a return, and a reader must be able to see all three at once.

Then the terminal disciplines, stated as facts: terminal growth is at or below the
riskfree rate in the mandate currency; the terminal reinvestment rate equals growth
divided by return on capital; the terminal beta is at its mature level. State the implied
perpetual return on capital and whether it exceeds the terminal cost of capital. If it
does, name the moat. If you cannot, set them equal and rerun.

### 8. The value bridge

From `06-intrinsic/dcf-result.json`. The ladder from operating assets to value per share,
line by line, each with its basis. Layout and the link-by-link rules are in
`value-bridge-and-range.md`.

Report the share of value carried by the terminal value. Above 80% is normal for a growth
company and is not a defect, but it is a fact the reader is entitled to.

### 9. The range

From the `sensitivity` block of `dcf-result.json`, plus any scenario grid or simulation.

Give the low, base and high with the inputs that produced each. Say which cells were ruled
out and why. If the conservative cell still sits above the price, say so — that argument
carries more weight than the base case. If the range is very wide, say that too, and
temper the recommendation accordingly.

Locate the market price inside the range. A price near the median of your own distribution
means you have no edge, and saying so is more useful than manufacturing one.

### 10. The pricing cross-check

From `07-relative/relative.md`. The peer set and the criteria that defined it, the multiple
chosen and its companion variable, the peer statistic, and the sector or market regression
where it is usable.

Report the implied price from each. Discard any estimate that is economically implausible
and say why rather than letting it drag an average. Then explain the difference between the
intrinsic and relative answers. That explanation is the analysis. Averaging them is not.

### 11. Value against price

The four steps from the main skill: the gap, the implied input the market is assuming, the
closing mechanism with a horizon, and the margin of safety. Add the expected one-year
return if the market corrects, and say plainly that it is conditional on correction.

Where the option overlay applies — a loss-making firm levered above half its capital at
market values — report the equity-as-call value here as a second independent estimate,
from `09-options/real-options.md`.

### 12. Challenge and unresolved findings

From `10-challenge/challenge.md` and `challenge.json`. What the critic attacked, what was
fixed, and what remains open. Format and content rules are in `disclosure-and-vintage.md`.

### 13. Recommendation

The call restated, now with everything behind it.

- The estimate the call rests on, and why that one carries the weight.
- The catalysts, each with a horizon and a mechanism.
- The risks, each with the value effect if it lands.
- What would change the call: the specific observation that would flip it.
- What to watch: the promotion trigger for each plausible claim in the ledger, so the
  narrative can be updated rather than rebuilt.

### 14. Sources, vintages and gaps

From `01-data/sources.md` and `gaps.json`, plus the `as_of` of every reference table. See
`disclosure-and-vintage.md`.

## Length

The verdict is one screen. Sections 3 to 11 run one to two screens each. Appendices carry
the full forecast table, the full adjustment log, the peer table and the full assumption
list. A reader who wants the audit trail should find it; a reader who wants the answer
should not have to walk past it.

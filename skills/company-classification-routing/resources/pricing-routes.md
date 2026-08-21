# Pricing routes by branch

Every branch also gets a *pricing* route, because a relative check runs in every mode. The
question is not which multiple you like. It is which multiple survives this company's
defects.

The forbidden column is not advice. It is the constraint set the critic enforces under rule
V9. Using PE on a firm carrying `no-earnings-multiple` fails the run.

## The routing table

| Branch condition | Pricing route | Forbidden |
|---|---|---|
| Negative or trough earnings (B1, B4, B7 pre-normalization) | A survival or growth-proxy regression. A forward multiple with the full haircut sequence. Or let the market pick the metric — the operating metric whose correlation with value is highest. | PE, PEG, EV/EBIT, EV/EBITDA |
| Financial service (B5, B5b) | Equity multiples only: PBV against ROE, and PE. | EV/EBITDA, EV/Sales, EV/IC, any enterprise multiple |
| Commodity or cyclical (B6, B7) | Multiples on **normalized** earnings. EV/EBITDA with a reinvestment control. | Current-year PE at a cycle extreme |
| Intangible-heavy (B8) | Multiples on **restated**, R&D-capitalized earnings and capital. EV/Sales with a margin control. | Raw PBV or raw EV/IC on unrestated capital |
| Multi-business (B10) | Price each division off its own sector's regression, evaluated at that division's fundamentals. Then bridge once. | One company-wide multiple |
| Emerging market or non-US (B9) | The regional regression. Assign region by operations, not by listing. | The US market regression applied to a non-US firm with no ADR |
| Private (B13) | Sector multiples carrying the same discounts as the DCF path. Regression evaluated at the firm's own fundamentals. | Any multiple that assumes a traded market, with no discount |
| Young or high-growth (B1) | Forward multiples and market-implied metrics, with survival proxies. | Raw price-to-sales regressed on current margin |

## Universal pricing rules

These hold on every branch.

**Run the four steps before trusting any multiple.** Define it, describe it, analyze it,
apply it. Most multiple errors are definition errors: an equity numerator against an
enterprise denominator, or a numerator and denominator measured at different dates.

**Use medians, never means.** Multiples are bounded below at zero and unbounded above, so
the mean is dragged by a few extreme values.

**Locate the multiple in the current, local distribution.** A fixed threshold flips meaning
across years and regions. "A PE of 15 is cheap" is a claim about a distribution, and the
distribution moves.

**Control statistically once more than one fundamental differs.** Eyeballing a peer table
handles one difference. Two or more needs a regression.

**Record the count of firms dropped from the sample.** Dropping every firm with negative
earnings is exactly the selection that makes a sector look profitable.

**State the verdict as relative.** A multiple says the company is cheap or expensive
*against this peer set*. It never says the company is worth more or less than the DCF says.

## Where the pricing route sits in the pipeline

Step 9, price comparison, after the engine and the bridge. The pricing route does not feed
the DCF and does not adjust it. The two are independent estimates, and the spread between
them is a finding worth reporting.

For B10 the ordering differs. Divisional pricing runs alongside divisional DCFs, and the
four numbers — intrinsic sum-of-the-parts, relative sum-of-the-parts, whole-company DCF,
and market enterprise value — get compared at the end.

## Detail

The mechanics live in `relative-valuation-toolkit`, which computes multiples, peer
statistics, sector and market regressions, and intrinsic multiples. The concept notes
behind each rule are listed under S9 in
`knowledge/frameworks/special-situations-routing.md`.

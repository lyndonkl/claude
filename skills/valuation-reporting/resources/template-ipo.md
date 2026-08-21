# Template: `ipo` mode

The question is what this private company is worth going public. The terminal artifact is
an offer price range.

Two numbers live in this report and they must never be merged. **Value** is what the
business is worth, from the discounted cash flow. **Price** is what the offering will
clear at, from the banker's process and the comparable set. The report gives both, keeps
them apart, and says which one the recommendation rests on.

Three adjustments sit between a correct business valuation and a correct value per share.
Get any of them wrong and the per-share number is wrong even when the business valuation is
right. They are the use of proceeds, the prior equity claims, and the share count.

## Sections in order

### 1. Verdict

- The recommended offer price range per share.
- The estimated value per share, with its own range.
- The gap between them, and the reason for it — expected underpricing, float size, or a
  deliberate discount to build a book.
- The proceeds to the company and the proceeds to selling holders, separately.
- The two or three assumptions the value turns on.

### 2. Mandate and basis

Company, currency, valuation date, the offering structure, and the intended float as a
percentage of post-offering shares. Note whether this is an intermediated offering, a
direct listing or a combination.

### 3. Business valuation

An ordinary discounted cash flow, with two differences from a private-company valuation
that the report must state.

- The beta is a market beta. The buyers after listing are diversified, so the private-firm
  risk identity no longer applies.
- No illiquidity discount is applied. The shares will have a market.

Let the cost of capital decline across the forecast toward its stable-growth level as risk
falls, and show the path. Holding it constant for a young company overstates the discount
in the later years, where most of the value sits.

Where the company is young and loss-making, the engine is the revenue-driven build with a
failure branch, and the report should say so rather than presenting a standard forecast.

Show the bridge from operating assets to equity value, per `value-bridge-and-range.md`.

### 4. Use of proceeds

Read the prospectus language and classify every currency unit raised. One table, four rows.

| Use | Effect on value |
|---|---|
| Taken out by existing owners | add nothing |
| Used to pay down debt | change the debt ratio, recompute the cost of capital, revalue |
| Retained for future reinvestment | add currency for currency |
| Split uses | add only the retained portion |

Adding proceeds the existing owners are withdrawing is a common and expensive error. The
table exists to make it visible.

### 5. Prior equity claims and the share count

Enumerate everything that is or becomes common stock: founder shares, each round of
convertible preferred with its conversion terms, restricted stock units already granted,
shares owed under acquisition agreements, and the new shares being issued.

Employee options and warrants stay out of the denominator. Their value comes out of the
numerator instead. Counting them in the share count and also subtracting their value is a
double count in the wrong direction.

Value the options with an expected life, not the stated contractual life.

Present the count as a reconciliation from the current cap table to the post-offering
share count, line by line. This table is where per-share errors are caught.

### 6. Value per share

Equity value from section 3, adjusted for the retained proceeds from section 4, less the
option value from section 5, divided by the post-offering share count.

Then the range around it, from the sensitivity on the two drivers that decide it.

### 7. Pricing the offering

A separate exercise from the valuation, and labelled as one.

The comparable set with the metric it prices on, and a note on whether the market is still
paying for that metric. Peer multiples applied to this company's forecast. The implied
price range from the peer work, beside the value range from section 6.

Then the underpricing allowance. First-day returns have been positive in every size
bucket and largest for the smallest deals; a low double-digit working assumption is
reasonable, stated as an assumption with its source. The cost to existing owners is the
underpricing percentage times the value of the shares actually sold, not of the whole
company. That arithmetic is why small initial floats are common, and the report should show
it rather than asserting it.

Note that the average underpricing cannot be harvested by an investor, because allocations
are rationed when a deal is hot.

### 8. Float, staging and the alternatives

The proposed float, the lock-up terms, and any staged follow-on. Then a short read on the
alternatives — direct listing or a blank-check structure — and why the chosen route fits
this company.

### 9. Unresolved findings, sources and vintages

See `disclosure-and-vintage.md`. Prospectus figures are unaudited in places and often
recent, so record the filing date beside the financial data.

### 10. Recommendation

The offer price range, the reason it sits where it does relative to value, and the
conditions under which you would move it. Name what would raise the range and what would
lower it before pricing day.

## What the reader will check

- No total beta and no illiquidity discount anywhere in the model.
- Proceeds withdrawn by owners add nothing.
- Options are out of the denominator and their value is out of the numerator, once each.
- Convertible preferred, restricted stock units and shares owed under acquisition
  agreements all appear in the share count.
- The cost of capital moves over the forecast for a young company.
- The offer price is never presented as the value, and the peer-multiple pricing is never
  presented as a valuation.

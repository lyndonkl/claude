# Acquisition price build-up, goodwill and the write-off post-mortem

**Core idea:** An acquisition price can be decomposed into layers, and the decomposition tells you who added what. Start at the target's pre-deal book equity. Accountants add revalued intangibles to get adjusted book equity. The market adds a premium over that to get pre-deal market equity. The acquirer then adds its own premium over market to get the price paid. Goodwill is the residual: price minus adjusted book equity. That residual is the acquirer's claim about value it will create, recorded as an asset. When the value does not arrive, the write-off decomposes the same way, and each layer has a culprit.

**Formulas:**
- `Post-deal adjusted book equity = Pre-deal book equity + Intangibles added by accountants`.
- `Pre-deal market equity = Post-deal adjusted book equity + Market premium over adjusted book`.
- `Acquisition price = Pre-deal market equity + Acquirer's premium over market`.
- `Goodwill recorded = Acquisition price − Post-deal adjusted book equity`.
- `Acquirer's premium % = (Acquisition price − Pre-deal market equity) / Pre-deal market equity`.
- Write-off attribution: `Total write-off = Premium for non-existent synergy + Effect of accounting impropriety + Post-deal deterioration`, with `Residual value = Acquisition price − Total write-off`.

**Procedure:**
1. Pull the target's pre-deal book equity from its last balance sheet before the deal.
2. Add the purchase-accounting intangibles the acquirer's accountants recognize. This is a revaluation exercise, not value creation.
3. Record the target's pre-deal market capitalization on the day before the first news story.
4. Compute the acquirer's premium over market. This is the number that has to be justified by control plus synergy.
5. Compute goodwill as price minus adjusted book equity. Read it as the acquirer's own estimate of value it must now deliver.
6. Test the premium against the acid test: is it below restructured value plus synergy value, both computed independently?
7. If the deal later fails, decompose the write-off into the three buckets — synergy that never existed, target misreporting, and post-deal deterioration — and assign a primary and secondary culprit to each.

**Reference data:**

HP / Autonomy price build-up, $ millions:

| Layer | Amount | Cumulative |
|---|---|---|
| Pre-deal book equity | 2,067 | 2,067 |
| + Intangible assets added by accountants | 2,533 | 4,600 (post-deal adjusted book equity) |
| + Market premium over adjusted book equity | 1,300 | 5,900 (pre-deal market equity) |
| + HP's premium over market value | 5,200 | 11,100 (acquisition price) |
| **Goodwill recorded** | | **6,500** (= 11,100 − 4,600) |

The market premium over *pre-deal* book equity was $3,833M. HP's premium over market was $5,200M on a $5,900M market value — roughly 88%.

HP / Autonomy write-off decomposition a year later, $ millions:

| Component | Amount | Primary culprit | Secondary culprit |
|---|---|---|---|
| Premium paid for non-existent synergy | 4,451 | Leo Apotheker, HP's old CEO | HP's deal bankers |
| Accounting impropriety — effect on claimed synergy | 749 | Autonomy's managers | Deloitte |
| Accounting impropriety — effect on pre-deal market value | 1,700 | Autonomy's managers | Deloitte |
| Post-deal deterioration and/or comparison game playing | 1,900 | HP's current management | HP's auditors |
| **Residual value remaining** | **2,300** | | |

**Worked example:** Read the HP/Autonomy tables together. HP paid $11,100M for a business whose book equity was $2,067M and whose market value was $5,900M. Of the $8.8B eventually written off, over half — $4,451M — was a premium for synergy that did not exist. Fraud at the target explains $2,449M across two layers. Post-deal decline explains $1,900M. Only $2,300M of value survived.

The lesson runs backwards from the goodwill line. Goodwill of $6,500M was, on day one, a public promise that HP would create $6.5B of value it did not yet own. No restructuring plan or bottom-up synergy schedule supported it. The write-off simply retired the promise.

**Determinism:**
- DETERMINISTIC: every line of both tables. Given the layer amounts, all cumulative values, the goodwill figure, the premium percentage and the residual are arithmetic. A script can compute goodwill from price and adjusted book equity, and the premium from price and market cap.
- JUDGMENT: the attribution of blame across layers; whether the intangibles recognized in purchase accounting are real; whether a given write-off reflects genuine deterioration or "comparison game playing" (choosing a benchmark that makes current management look better).

**Pitfalls:**
- Reading purchase-accounting intangibles as value creation. Revaluing the balance sheet moves numbers between lines; it does not change cash flows.
- Treating goodwill as an asset in a valuation. In an intrinsic valuation it is a residual, not a source of cash.
- Justifying a premium over market by pointing to the premium over *book*. Book equity is not a value benchmark.
- Waiting for the write-off to do the decomposition. The same layers are visible on announcement day and should be tested then.
- Diffusing blame across so many parties that no one is accountable — the seventh sin.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.109, p.111`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.109, p.111`

**Related:** [[deal-bias-and-ego]], [[seven-sins-of-acquisitions]], [[synergy-delivery-odds]], [[three-reasons-and-acid-test]], [[valuing-synergy]], [[accounting-for-acquisitions]]

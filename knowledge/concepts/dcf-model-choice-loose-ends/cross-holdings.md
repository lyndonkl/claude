# Cross holdings: valuing stakes in other companies

**Core idea:** When a company owns pieces of other companies, its financial statements misreport what its own shareholders own. Accounting handles the three ownership tiers differently, and each distorts the valuation in a different direction. A minority passive stake shows up only as dividends, so the DCF misses the holding almost entirely. A minority active stake contributes a share of equity income. A majority stake is fully consolidated: 100% of the subsidiary's revenues, earnings and assets flow into the parent's statements, even though the parent may own only 60%. The right fix is a sum-of-the-parts: value the parent on unconsolidated numbers, value each holding on its own, then add back only the parent's proportional share.

**Formulas:**
- Three-step method:
  `Value of equity in parent = Value of un-consolidated parent − Debt of un-consolidated parent + Σ_{j=1..N} (% owned of Company j) × (Value of Company j − Debt of Company j)`.
- Consolidated shortcut (majority holdings): `Parent equity = Consolidated firm value − Debt − Market value of minority interest`.
- Book-to-market approximation: `Estimated market value of minority interest = Minority interest on balance sheet × Price-to-Book ratio of the subsidiary's sector`.
- Same for minority holdings: `Market value of holdings = Book value of holdings on balance sheet × sector Price-to-Book ratio`, added to the value of operating assets.

**Reference data — accounting categories:**

| Category | Typical stake | What appears in the parent's statements | Valuation consequence |
|---|---|---|---|
| Minority passive | < 20% | Dividends received only; holding carried on the balance sheet | Add the stake's value; the DCF captures almost none of it |
| Minority active | 20–50% | Proportional share of the subsidiary's equity income | Add the stake's value; strip the equity income from operating earnings |
| Majority active | > 50% | Full consolidation of 100% of the subsidiary, with a minority-interest offset | Subtract the value of the minority interest you do not own |

**Procedure:**
1. Read the notes to the accounts and list every holding, its ownership percentage, and its accounting treatment.
2. **Step 1 — value the parent alone.** Use unconsolidated financial statements. If only consolidated statements exist, note that your firm value already includes 100% of the subsidiaries.
3. **Step 2 — value each holding individually.** Do a DCF of each. Using the market value of a listed holding imports the market's pricing errors into your intrinsic valuation, which defeats the purpose.
4. **Step 3 — combine.** Parent equity = unconsolidated parent value − unconsolidated parent debt + Σ (% owned × holding equity value).
5. If you had to start from consolidated statements, subtract the minority interest at *your* estimate of its value, not at book.
6. If full sum-of-the-parts is impossible, fall back to the price-to-book approximation. Convert book minority interest and book holdings to market using the subsidiary's sector P/BV, subtracting the former and adding the latter.
7. Do not forget taxes due on the holdings if a sale or repatriation is contemplated; net them out in the bridge.

**Worked example A — the three-part exercise:**
1. Company A is valued from consolidated financials at $1,000m (FCFF discounted at the cost of capital), with $200m of debt → equity $800m. That value already includes 100% of its consolidated subsidiary.
2. A owns 10% of Company B, a passive holding; B's market cap is $500m. Add 10% × 500 = $50m → equity $850m.
3. A owns 60% of Company C, fully consolidated, with minority interest booked at $40m. Subtract the minority interest → equity ≈ **$810m**. That $40m is a book-value approximation of the 40% of C the parent does not own.
4. Now redo it with intrinsic values. You value B's equity at $250m (half the market's $500m) and C's equity at $250m. Then: 1,000 − 200 + 10% × 250 − 40% × 250 = 1,000 − 200 + 25 − 100 = **$725m**. The intrinsic treatment is $85m below the book/market shortcut, on a firm worth under a billion.

**Worked example B — Yahoo as the sum of its intrinsic pieces ($ millions):**

| Piece | Operating assets | + Cash | − Debt | = Equity | Stake | Value to Yahoo |
|---|---|---|---|---|---|---|
| Yahoo! US | 4,383 | 4,571 | 1,591 | 7,363 | 100% | 7,363 |
| Yahoo! Japan | 17,884 | 3,113 | 0 | 20,997 | 35% | 7,349 |
| Alibaba | 127,484 | 27,963 | 6,670 | 145,587 | 22.1% | 32,175 |
| Less taxes due | | | | | | (5,017) |
| Less Yahoo options | | | | | | (298) |
| **Total equity value** | | | | | | **41,571** |

Per share: **$41.19**. The same structure can be run with pricing multiples instead of DCFs. Apply EV/Sales of 0.63, 7.91 and 12.18 to sales of 4,672, 3,929 and 7,911 for Yahoo US, Yahoo Japan and Alibaba. That route gives equity of **$39,580m**, or **$39.19 per share**. The two routes land close together here, but they need not.

**Determinism:**
- DETERMINISTIC: the aggregation formula; the exercise arithmetic; the Yahoo sum-of-parts given each piece's value, stake, taxes and option value; the P/BV approximation given book values and sector ratios.
- JUDGMENT: the DCF of each holding (especially a private one), the choice between intrinsic and market values for listed holdings, the sector P/BV to use in the approximation, and the tax rate on repatriating or selling stakes. This needs segment disclosures, subsidiary filings where available, and sector multiple data.

**Pitfalls:**
- Valuing a consolidated parent and forgetting to remove minority interests. You credit shareholders with a subsidiary they only partly own.
- Using book minority interest as if it were market value. Book is usually far too low for a profitable subsidiary.
- Using market values for listed holdings inside an intrinsic valuation, which smuggles the market's errors into your answer.
- Leaving the equity income of a minority active holding inside operating income *and* adding the stake's value.
- Ignoring taxes due on unrealized gains in large stakes — $5,017m on Yahoo's holdings, over 10% of its equity value.

**Sources:**
- valpacket1spr21 p.226-232
- valpacket1spr20 p.222-228

**Related:** [[equity-value-bridge]], [[complexity-discount]], [[other-non-operating-assets]], [[debt-and-other-claims-in-the-bridge]], [[sum-of-the-parts-valuation]], [[relative-valuation-multiples]]

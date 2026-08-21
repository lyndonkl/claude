# The discount for complexity and opacity

**Core idea:** Take two firms with identical value drivers — same operating income, tax rate, return on capital, growth and cost of capital. One runs a single business with simple holdings and transparent accounting. The other spans multiple businesses, complex holdings and opaque accounting. They should not be worth the same. Investors who cannot verify the fundamentals either assume the worst or demand compensation for the uncertainty, and the market data show they do exactly that. Complexity is measurable — crudely by disclosure volume, more carefully by a weighted scorecard — and it can be priced, either inside the DCF or as a haircut on the final value.

**Formulas:**
- Complexity score: `Score = Σ over factors (factor answer × weighting factor)`, aggregated across operating income, tax rate, cap ex, working capital, expected growth, cost of capital, non-operating assets, firm-to-equity items and per-share items. Higher = more complex.
- Market price of complexity (regression across the 100 largest market-cap firms):
  `PBV = 0.65 + 15.31 × ROE − 0.55 × Beta + 3.04 × Expected growth rate − 0.003 × (number of pages in the 10K)`
  where PBV = price-to-book ratio, ROE = return on equity, Beta = market beta. Each additional 10K page costs about 0.003 of price-to-book.

**Reference data:**

The experiment (two firms, identical drivers):

| | Company A | Company B |
|---|---|---|
| Operating income | $1 billion | $1 billion |
| Tax rate | 40% | 40% |
| ROIC | 10% | 10% |
| Expected growth | 5% | 5% |
| Cost of capital | 8% | 8% |
| Business mix | Single | Multiple |
| Holdings | Simple | Complex |
| Accounting | Transparent | Opaque |

Crude complexity proxy — pages of financial disclosure:

| Company | Pages in last 10Q | Pages in last 10K |
|---|---|---|
| General Electric | 65 | 410 |
| Microsoft | 63 | 218 |
| Wal-mart | 38 | 244 |
| Exxon Mobil | 86 | 332 |
| Pfizer | 171 | 460 |
| Citigroup | 252 | 1,026 |
| Intel | 69 | 215 |
| AIG | 164 | 720 |
| Johnson & Johnson | 63 | 218 |
| IBM | 85 | 353 |

The complexity scorecard, illustrated for Hyundai Heavy (total score **49.75**):

| Area | Factor | Answer | Weight | Score |
|---|---|---|---|---|
| Operating income | Businesses with >10% of revenues | 3 | 2.00 | 6.00 |
| Operating income | One-time income/expenses (% of op income) | 5% | 10.00 | 0.50 |
| Operating income | Income from unspecified sources (% of op income) | 15% | 10.00 | 1.50 |
| Operating income | Volatile income-statement items (% of op income) | 20% | 5.00 | 1.00 |
| Tax rate | Non-domestic revenues (%) | 75% | 3.00 | 2.25 |
| Tax rate | Different tax and reporting books | No | Yes=3 | 0 |
| Tax rate | Headquarters in tax havens | No | Yes=3 | 0 |
| Tax rate | Volatile effective tax rate | Yes | Yes=2 | 2.00 |
| Capital expenditures | Volatile capital expenditures | Yes | Yes=2 | 2.00 |
| Capital expenditures | Frequent and large acquisitions | No | Yes=4 | 0 |
| Capital expenditures | Stock payment for acquisitions | No | Yes=4 | 0 |
| Working capital | Unspecified current assets/liabilities | Yes | Yes=3 | 3.00 |
| Working capital | Volatile working capital items | Yes | Yes=2 | 2.00 |
| Expected growth | Off-balance-sheet items (operating leases, R&D) | No | Yes=3 | 0 |
| Expected growth | Substantial stock buybacks | No | Yes=3 | 0 |
| Expected growth | Changing/volatile return on capital | Yes | Yes=5 | 5.00 |
| Expected growth | ROC far above industry average | Yes | Yes=5 | 5.00 |
| Cost of capital | Businesses with >10% of revenues | 3 | 1.00 | 3.00 |
| Cost of capital | Emerging-market operations (% of revenues) | 50% | 5.00 | 2.50 |
| Cost of capital | Is the debt market traded? | No | No=2 | 2.00 |
| Cost of capital | Does the company have a rating? | No | No=2 | 2.00 |
| Cost of capital | Off-balance-sheet debt | No | Yes=5 | 0 |
| Non-operating assets | Minority holdings as % of book assets | 30% | 20.00 | 6.00 |
| Firm to equity value | Minority interest as % of book equity | 20% | 20.00 | 4.00 |
| Per share value | Shares with different voting rights | No | Yes=10 | 0 |
| Per share value | Options outstanding as % of shares | 0% | 10.00 | 0 |
| **Total** | | | | **49.75** |

**Procedure:**
1. Score the firm on the scorecard above, or at minimum count 10K/10Q pages against sector peers.
2. Choose a stance. The aggressive analyst trusts what the company says about its value. The conservative analyst refuses to value what cannot be seen. The compromise adjusts for complexity explicitly.
3. If you adjust, pick exactly **one** channel: lower the cash flows, raise the discount rate, cut the growth rate or shorten the growth period, or apply a final percentage discount to the computed value.
4. For a market-based cross-check, run the PBV regression with the firm's ROE, beta, expected growth and 10K page count, and compare the predicted PBV with the firm's actual PBV.
5. Re-examine the complexity items that are also modeling problems. Unspecified income, off-balance-sheet debt and unconsolidated holdings are better fixed in the model than papered over with a discount.

**Worked example:** Hyundai Heavy scores 49.75 on the scorecard. The four largest contributors are minority holdings at 30% of book assets (6.00), multiple businesses (6.00), volatile and unsustainably high return on capital (5.00 + 5.00), and minority interest at 20% of book equity (4.00). Two of those four are cross-holding problems, which points to the fix: do the sum-of-the-parts work in [[cross-holdings]] before reaching for a blanket discount. Separately, the PBV regression says a firm filing a 1,026-page 10K (Citigroup) carries about 3.1 points less price-to-book than an otherwise identical firm filing nothing — `0.003 × 1,026 ≈ 3.08`.

**Determinism:**
- DETERMINISTIC: the complexity score given the questionnaire answers and weights; the PBV regression prediction given ROE, beta, growth and page count; page counts themselves.
- JUDGMENT: answering the scorecard questions; whether complexity deserves a value adjustment at all; which channel to use and how large the adjustment should be. This needs the filings, the segment notes, and a view on management's disclosure incentives.

**Pitfalls:**
- Stacking adjustments: a higher discount rate *and* lower cash flows *and* a final haircut for the same opacity.
- Applying a complexity discount instead of doing the work — the cross-holding valuation, the lease capitalization, the segment analysis.
- Treating page count as complexity itself. Financial firms file long documents partly because regulators require it.
- Ignoring complexity because the company is large and well known. Citigroup, AIG and GE sit at the top of the disclosure-volume table.
- Using the PBV regression as a valuation model. It is a market-pricing cross-check, estimated on the 100 largest market-cap firms.

**Sources:**
- valpacket1spr21 p.235-238
- valpacket1spr20 p.231-234

**Related:** [[equity-value-bridge]], [[cross-holdings]], [[other-non-operating-assets]], [[marginal-value-of-cash]], [[relative-valuation-multiples]], [[corporate-governance-discount]]

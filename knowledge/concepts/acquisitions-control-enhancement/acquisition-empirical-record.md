# The empirical record on acquisitions

**Core idea:** Acquisitions are the largest, most visible, and most reliably value-destructive decisions firms make. Event studies show target shareholders capture almost all the gain at announcement while acquirer shareholders capture roughly nothing (and drift slightly negative). Long-horizon studies — McKinsey, KPMG, divestiture tracking, cross-border samples — confirm that the announcement-day disappointment is not a market-myopia artifact: most acquisition programs fail their own value tests, and a large fraction of deals are unwound within a decade. The purpose of this evidence is not fatalism but priors: when you value an acquisition, the base rate says the acquirer overpays, so the burden of proof belongs on the deal, not on the skeptic.

**Formulas:**
- Cumulative abnormal return (event study): `CAR(t1,t2) = Σ_{t=t1..t2} (R_t − E[R_t])`, where `R_t` = the firm's actual return on day/month t, `E[R_t]` = the expected (market-model or market-adjusted) return, and the window is measured relative to announcement date t = 0.
- Acquirer's value test 1 (McKinsey): `ROC on capital invested in acquisitions > Cost of capital`.
- Acquirer's value test 2 (McKinsey): parent's return `>` competitor/peer-group return over the same horizon.

**Procedure:**
1. Before valuing any deal, write down the base rate: assume the acquirer is more likely than not to destroy value, and require the deal's specific value case to overcome that.
2. Identify which side of the announcement you are on. If you own the target, the evidence says the announcement is where your gain is realized (~+17% to +19% CAR); if you own the acquirer, expect ~0% to −2%.
3. For an acquisition *program* (a serial acquirer), apply the two McKinsey tests: (a) did the capital deployed into acquisitions earn more than the cost of capital, and (b) did the parent beat its peer group? Failing either is a red flag; failing both means the program should be stopped.
4. Check the reversal rate: how many of the acquirer's past deals were divested, and how fast? A divestiture inside 3–5 years is an admission the deal failed.
5. Do not accept "the market cannot see the long-term benefits" as a defense — the long-horizon evidence (10+ year divestiture rates, multi-year CARs) rejects it.
6. Treat non-US and emerging-market acquirers as subject to the same pattern, not exempt from it.

**Reference data:**

Announcement-period cumulative abnormal returns, public acquisitions (chart values, approximate):

| Window (trading days around announcement) | Target CAR | Bidder CAR |
|---|---|---|
| day −20 | ~0% | ~0% to +1% |
| day −1 | ~+5% | ~+1% |
| day 0 | ~+17% | ~0% |
| day +20 | ~+19% | ~−1.5% |

Long-horizon evidence:

| Study | Finding |
|---|---|
| McKinsey (acquisition programs) | 50% of programs failed at least one of the two value tests; 25% failed both |
| KPMG (global acquisitions) | >80% of mergers "fail" — merged company underperforms its peer group |
| Divestiture tracking | ~20% of 1982–86 acquisitions divested by 1988; ~50% divested over 10+ years |

Indian acquirers of US targets, 1999–2005 — monthly CAR around takeover month 0:

| Month | CAR |
|---|---|
| 0 | ~+2.4% |
| +2 to +3 | ~+3.6% to +3.7% (peak) |
| +12 to +13 | ~0% |
| +14 | turns negative |
| +18 to +20 | ~−3.2% |

**Worked example:** An investor holds shares in a serial acquirer. Over the last decade the firm deployed $20B into acquisitions. The after-tax return on that invested capital is 6.5% against a cost of capital of 8.2%, so it fails McKinsey test 1. Its total shareholder return trailed its peer index, so it fails test 2. Three of eleven deals have already been divested — a 27% reversal rate, in line with the 20%-by-1988 benchmark. Verdict: the acquisition program is a value-destroying habit. Price the next deal off that prior, not off management's synergy deck. (Framework and statistics from Damodaran's "Acquirers Anonymous" module; source studies McKinsey, KPMG.)

**Determinism:**
- DETERMINISTIC: CAR computation given return series and a benchmark/market model; ROC on acquisition capital given invested capital and after-tax operating income; divestiture rate given a deal list and divestiture dates; peer-group comparison given return series.
- JUDGMENT: choosing the estimation window and the benchmark model. Deciding whether a divestiture is an admission of failure or a portfolio reshuffle. Deciding how much of the base rate to apply to *this* acquirer — a disciplined serial acquirer with a narrow, proven strategy is not the average acquirer.

**Pitfalls:**
- Reading positive target returns as evidence that "the deal creates value" — it only shows value transferred to the target.
- Accepting the "markets are short-sighted" defense; long-horizon evidence contradicts it.
- Assuming your firm, sector, or country is exempt — the Indian-acquirer sample shows the same decay pattern.
- Ignoring that there is almost no learning in the process: the same firms, with the same advisors, repeat the same mistakes, so a firm's past deal record is genuinely predictive.

**Sources:**
- `valuations--lecture_notes--spring_2021--valpacket3spr21 p.85-88`
- `valuations--lecture_notes--spring_2020--valpacket3spr20 p.85-88`

**Related:** [[seven-sins-of-acquisitions]], [[acquisition-strategy-design]], [[three-reasons-and-acid-test]], [[deal-bias-and-ego]], [[growth-quality-and-excess-returns]]

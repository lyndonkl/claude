# Historical growth: estimation and its pitfalls

**Core idea:** Past earnings growth is the natural first place to look for a growth rate, and it is usually a reasonable starting point — but it is far less informative than it looks. The number you get depends on the averaging method (arithmetic vs geometric), the estimation model (simple average vs regression), the start and end points of the window, and the metric you measure (revenues vs EBITDA vs EBIT vs EPS). Two structural problems make it worse: growth rates computed off a negative base are meaningless no matter how you compute them, and growth rates computed while a firm was scaling up from a tiny base will vastly overstate what is sustainable.

**Formulas:**
- Arithmetic average growth = simple mean of the yearly percentage changes.
- Geometric average growth = `(Ending value / Beginning value)^(1/n) − 1`, where `n` = number of years of growth (one less than the number of observations).
- Regression estimate: fit `Earnings_t = a + b × t` over the window; growth proxy = `b / (average earnings over the window)`.
- Relationship: arithmetic ≥ geometric always, and the gap widens with the volatility (standard deviation) of the series. For a volatile earnings series the arithmetic average is close to useless.
- Negative-base workarounds (all three are arithmetic tricks, none of them fix the underlying problem):
  1. Divide the change by the **higher** of the two earnings numbers.
  2. Divide the change by the **absolute value** of the starting earnings.
  3. Regression: slope coefficient / average earnings.

**Procedure:**
1. Pick the metric that matches your cash flow: revenues and EBIT for firm valuation, net income and EPS for equity valuation. Growth rates differ enormously across metrics for the same firm.
2. Pick the window deliberately and disclose it. Avoid windows that start at a trough or end at a peak. Check whether an acquisition, divestiture or accounting change breaks comparability mid-window.
3. Compute both the arithmetic and geometric averages **and the standard deviation** of the yearly changes. If the standard deviation is large, discard the arithmetic average and use the geometric.
4. If the base-period earnings are negative, stop. Report that the growth rate cannot be meaningfully estimated and switch to the revenue-and-margin route ([[top-down-revenue-growth]]) or normalize the earnings ([[normalizing-depressed-earnings]]).
5. Test for scaling. Plot the year-by-year growth rates. If they decline monotonically as the base grows, the average over the window is not a forecast — it is an artifact of starting small.
6. Sanity-check by extrapolating: compound the historical rate forward five years and ask whether the resulting revenue or income level is physically plausible for the industry and the total market. If not, the rate is wrong.
7. Treat the result as one input among three (history, analysts, fundamentals) — see [[analyst-growth-estimates]] and [[fundamental-growth-operating]].

**Reference data:**

Arithmetic vs geometric across metrics — Motorola, 1994–1999 ($ millions):
| Year | Revenues | % change | EBITDA | % change | EBIT | % change |
|---|---|---|---|---|---|---|
| 1994 | 22,245 | — | 4,151 | — | 2,604 | — |
| 1995 | 27,037 | 21.54% | 4,850 | 16.84% | 2,931 | 12.56% |
| 1996 | 27,973 | 3.46% | 4,268 | −12.00% | 1,960 | −33.13% |
| 1997 | 29,794 | 6.51% | 4,276 | 0.19% | 1,947 | −0.66% |
| 1998 | 29,398 | −1.33% | 3,019 | −29.40% | 822 | −57.78% |
| 1999 | 30,931 | 5.21% | 5,398 | 78.80% | 3,216 | 291.24% |
| **Arithmetic avg** | | **7.08%** | | **10.89%** | | **42.45%** |
| **Geometric avg** | | **6.82%** | | **5.39%** | | **4.31%** |
| **Std deviation** | | 8.61% | | 41.56% | | 141.78% |

For smooth revenues the two averages nearly agree (7.08% vs 6.82%). For volatile EBIT the arithmetic average (42.45%) is ten times the geometric (4.31%). Same company, same window — the "growth rate" ranges from 4.31% to 42.45% depending on choices that look purely technical.

The scaling effect — Callaway Golf net profit ($ millions):
| Year | 1990 | 1991 | 1992 | 1993 | 1994 | 1995 | 1996 |
|---|---|---|---|---|---|---|---|
| Net profit | 1.80 | 6.40 | 19.30 | 41.20 | 78.00 | 97.70 | 122.30 |
| Growth | — | 255.56% | 201.56% | 113.47% | 89.32% | 25.26% | 25.18% |

Geometric average 1990–1996 = `(122.30/1.80)^(1/6) − 1` ≈ **102%** — while the most recent years are running at 25%. Extrapolating the 102% average five years forward gives 1997: $247m, 1998: $499m, 1999: $1,008m, 2000: $2,036m, **2001: $4,113m** — a $4.1 billion net income for a golf-club maker. That is the reductio.

**Worked example — the negative base:** Time Warner's EPS was **−$0.05** in 1996 and expected to be **+$0.25** in 1997. The change is $0.30.
- Naive: `0.30 / (−0.05) = −600%` — an improvement reported as a 600% *decline*. Nonsense.
- Workaround 1 (higher of the two): `0.30 / 0.25 = +120%`.
- Workaround 2 (absolute value of the base): `0.30 / 0.05 = +600%`.
Three defensible methods, three answers spanning 720 percentage points. The honest answer to "what is the growth rate?" is **it cannot be estimated**; move to revenues and margins instead.

**Determinism:**
- DETERMINISTIC: given an earnings series, the yearly percentage changes, arithmetic mean, geometric mean, standard deviation, regression slope, and all three negative-base workarounds. Also the forward extrapolation.
- JUDGMENT: choosing the metric, the window endpoints, and the averaging method; recognizing that a scaling-up average is not a forecast; deciding that a growth number computed off a negative or tiny base should be discarded rather than used; judging comparability across an acquisition or restructuring.

**Pitfalls:**
- Quoting the arithmetic average of a volatile earnings series. Motorola's EBIT "grew 42.45%" a year while actually compounding at 4.31%.
- Reporting a growth rate off a negative base — the sign alone is meaningless.
- Averaging over a scale-up period and projecting it forward.
- Cherry-picking endpoints (start-at-trough, end-at-peak) without saying so.
- Comparing a revenue growth rate to an EPS growth rate as if they measured the same thing.
- Using historical growth in earnings for a firm whose margins are about to change — the past growth embeds the old margin path.
- Failing the plausibility test: never adopt a growth rate whose five-year extrapolation implies revenues or profits larger than the addressable market.

**Sources:**
- valpacket1spr21 p.158, p.160-167
- valpacket1spr20 p.155, p.157-164
- valpacket1spr21 p.196 / valpacket1spr20 p.193 (historical growth as one branch of the growth decision tree)

**Related:** [[analyst-growth-estimates]], [[fundamental-growth-equity]], [[fundamental-growth-operating]], [[top-down-revenue-growth]], [[normalizing-depressed-earnings]], [[value-of-growth]]

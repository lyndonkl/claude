# Normalizing negative or abnormally low earnings

**Core idea:** A DCF built off a loss year or a trough year will produce nonsense: growth rates off a negative base are meaningless, and reinvestment-times-return equations require a sustainable return. The right response depends entirely on **why** earnings are depressed. If the cause is transient (a temporary problem or the cycle), normalize the earnings and value the firm off the normalized number. If the cause is structural — the life cycle, too much leverage, or a genuine long-term operating problem — do not normalize; instead build a detailed forecast starting from revenues in which the problem is reduced or eliminated over time toward an explicit target.

**Formulas:**
- Dollar averaging (use when firm size has not changed much): Normalized net income = average net income over the cycle; Normalized EBIT = average EBIT over the cycle. Choose net income for equity valuation, EBIT for firm valuation.
- Return-based normalization (use when firm size has changed): 
  - Normalized net income = Average ROE × **current** book value of equity.
  - Normalized EBIT(1−t) = Average ROC × **current** book value of invested capital, where invested capital = BV equity + BV debt − cash.
- Growth off a normalized base then uses the normalized return: see [[fundamental-growth-equity]] and [[fundamental-growth-operating]].
- For the structural cases, the forecast engine is Revenue growth -> Target operating margin -> Reinvestment via sales-to-capital; see [[top-down-revenue-growth]].

**Procedure:**
1. **Diagnose the cause.** There are five, and they split into two treatment paths:
   | Cause | Example | Treatment |
   |---|---|---|
   | Temporary problem | one-off disruption, plant fire, a bad quarter | Normalize |
   | Cyclicality | auto or commodity firm in a recession | Normalize |
   | Life-cycle | young firm, infrastructure firm still building out | Forecast from revenues |
   | Leverage problem | healthy operations, too much debt | Forecast from revenues |
   | Long-term operating problem | structural production or cost problems | Forecast from revenues |
2. **Normalization path (temporary / cyclical).**
   a. Decide whether the firm's *size* has changed materially over the averaging window.
   b. If size is stable: average the dollar earnings over a full cycle (typically 5 years; longer for deep commodity cycles). Average net income for equity, average EBIT for the firm.
   c. If size has changed: compute average ROE (or ROC) over the cycle, and apply it to today's book equity (or book capital). This scales the normalized earnings to the firm's current size.
   d. Also normalize the tax rate over the same window if the effective rate swings with the cycle.
3. **Forecast path (life-cycle / leverage / operating).** Start from revenues and set an explicit endpoint for the problem:
   - Structural problem -> target the operating margins of *stable firms in the sector*.
   - Leverage problem -> target a debt ratio the firm can live with by the end of the forecast (its own optimal, or the industry average), and move the cost of capital with it.
   - Operating problem -> target the *industry-average* operating margin.
   Then let margins/leverage converge to the target over the forecast period, and reinvest using a sales-to-capital ratio.
4. Carry the fix through: normalized EBIT changes interest coverage (and hence the synthetic rating and cost of debt), the reinvestment rate, and the return on capital that drives growth.
5. If the base year is negative and you are on the forecast path, remember taxes: losses become NOL carryforwards -> [[tax-rate-and-nols]].

**Reference data:**
- The averaging window Damodaran uses in practice is 5 years (e.g. Vale normalized over 2009–2013; Deutsche Bank over 2003–2007). For a firm hit by a specific shock, use the *pre-shock* cycle: Embraer's interest coverage for its synthetic rating was computed from average EBIT 2001–2003 because 9/11 crushed 2002–2003 aircraft demand.
- Model-selection convention (from Damodaran's model-choice table): negative earnings that are *cyclical* -> normalized EPS model (stable leverage) or normalized FCFF model (unstable leverage); negative and *troubled* -> FCFF model if a turnaround is expected, option-pricing model if bankruptcy is likely; negative and *start-up* -> FCFF model if multiple business lines, option model if a single line.

**Worked example — Vale, November 2013 (normalizing a commodity cyclical, $ millions):**

| Year | Operating income | Effective tax rate | Invested capital | Return on capital |
|---|---|---|---|---|
| 2009 | 6,057 | 27.79% | 48,085 | 9.10% |
| 2010 | 23,033 | 18.67% | 72,339 | 25.90% |
| 2011 | 30,206 | 18.54% | 87,831 | 28.01% |
| 2012 | 13,346 | 18.96% | 98,299 | 11.00% |
| 2013 (TTM) | 15,487 | 20.65% | 100,352 | 12.25% |
| **Normalized** | **17,626** | **20.92%** | — | **17.25%** |

Because iron-ore earnings swing violently with commodity prices, Vale was valued off normalized EBIT of $17,626m and a normalized ROC of 17.25% rather than the trailing $15,487m — and, because the normalized firm was already mature, with **no high-growth period at all** (stable growth of 2% forever, reinvestment rate = g/ROC = 2%/17.25% = 11.59%).

Second example — Deutsche Bank, January 2008 (normalizing a peak year): 2007 net income was EUR 6,510m on beginning book equity of EUR 33,475m, an ROE of 19.45%, which with a 67.03% retention ratio implied 13.04% growth. Substituting **average 2003–07 net income of EUR 3,954m** gives normalized ROE = 3,954/33,475 = 11.81% and a normalized retention ratio of 1 − 2,146/3,954 = 45.72%, so normalized growth = 0.4572 × 0.1181 = **5.40%** — less than half the unnormalized figure.

**Determinism:**
- DETERMINISTIC: once the window and the metric are fixed, averaging dollar earnings, averaging ROE/ROC, and applying the average return to current book value are pure arithmetic. So is the downstream re-derivation of coverage, reinvestment rate and growth.
- JUDGMENT: (1) diagnosing *why* earnings are depressed — needs sector context, the firm's leverage, its life-cycle stage, and management commentary; (2) choosing the averaging window (how long is the cycle?); (3) deciding whether firm size has changed enough to switch from dollar averaging to return-based normalization; (4) picking the target margin/debt ratio for the forecast path (needs peer-group margin distributions).

**Pitfalls:**
- Normalizing a firm whose problems are structural — you value a company that no longer exists.
- Dollar-averaging earnings across a period in which the firm doubled or halved in size.
- Averaging over a window that does not span a full cycle, or that is chosen to flatter (start at the trough, end at the peak).
- Normalizing earnings but leaving the *current* depressed interest coverage in the synthetic rating, or vice versa — be consistent about which numbers are normalized.
- Computing a growth rate off the negative base before normalizing (see [[historical-growth]]).
- Forgetting that a normalized, mature firm may deserve **no** high-growth period.

**Sources:**
- valpacket1spr21 p.121, p.135
- valpacket1spr20 p.118, p.132
- cfpacket2spr20 p.243 (Deutsche Bank normalized ROE and growth), p.253 (Vale normalization table and stable-growth valuation)
- valpacket1spr21 p.102 / valpacket1spr20 p.100 (Embraer: normalized EBIT for interest coverage)
- spreadsheet:readme1s.xls — model-choice table routing negative/abnormal earnings to normalized-EPS, normalized-FCFF or option models
- spreadsheet:model.xls — the same routing as a questionnaire (earnings sign, normalcy, growth, leverage)

**Related:** [[reported-to-actual-earnings]], [[historical-growth]], [[top-down-revenue-growth]], [[tax-rate-and-nols]], [[fundamental-growth-operating]], [[dcf-model-choice-framework]], [[dcf-case-valuations]], [[distressed-firm-valuation]]

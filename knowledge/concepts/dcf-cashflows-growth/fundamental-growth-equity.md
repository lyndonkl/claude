# Fundamental growth in equity earnings (EPS and net income)

**Core idea:** Earnings growth is not a free-standing assumption; it is what you get when a firm reinvests and earns a return on what it reinvests. For equity earnings this means: growth = (fraction of earnings retained) x (return earned on equity). Two versions exist. The simple EPS version uses the retention ratio and ROE and implicitly assumes retained earnings are reinvested at the ROE. The more careful version strips cash out of both income and equity and uses the firm's actual equity reinvestment in real assets, because a firm that piles retained earnings into a cash account is not earning ROE on them. A key structural fact falls out immediately: **long-term expected earnings growth cannot exceed the return on equity**, because the retention ratio cannot exceed 100%.

**Formulas:**

*Version I — EPS growth (stable ROE):*
- `Retention ratio b = Retained earnings / Net income = 1 − Payout ratio`
- `ROE = Net income / Book value of equity (at the start of the year)`
- `g_EPS = b × ROE`
- Constraint: `g_EPS <= ROE`.

*Version I' — EPS growth when ROE is changing:*
- `g = ROE_(t+1) × b + (ROE_(t+1) − ROE_t) / ROE_t`
- The second term is efficiency growth from re-earning a higher return on the *existing* equity base. If the ROE change is spread over n years, annualize it: `[1 + (ROE_(t+n) − ROE_t)/ROE_t]^(1/n) − 1`.

*Version II — growth in net income from non-cash assets:*
- `Net income from non-cash assets = Net income − Interest income from cash × (1 − t)`
- `Equity reinvestment = (Cap ex − Depreciation) + Change in non-cash working capital − Change in debt`, or equivalently `(Net cap ex + ΔWC) × (1 − Debt ratio)`
- `Equity reinvestment rate = Equity reinvestment / Net income from non-cash assets`
- `Non-cash ROE = Net income from non-cash assets / (Book value of equity − Cash)`
- `g_NI = Equity reinvestment rate × Non-cash ROE`
- Changing-return version: `g = ROE_(t+1) × Equity reinvestment rate + (ROE_(t+1) − ROE_t)/ROE_t`

*Decomposing ROE (where the return comes from):*
- `ROE = ROC + (D/E) × [ROC − i × (1 − t)]`
  - `ROC = EBIT_t × (1 − tax rate) / Book value of capital_(t−1)`
  - `Book value of capital = BV debt + BV equity − cash`
  - `D/E` = book debt / book equity; `i` = interest expense / book value of debt; `t` = tax rate on ordinary income
- Leverage raises ROE **if and only if** `ROC > i(1 − t)`; the boost per unit of D/E is exactly the spread.
- Regulatory shock: `New ROE = Old ROE / (1 + % increase in required book equity)`.

**Procedure:**
1. Decide which earnings measure you are growing: EPS (dividend/DDM work) or aggregate net income (FCFE work). Pair each with its own matched reinvestment and return measures — never mix rows of the table below.
2. Compute the return measure on **beginning-of-year** book equity, and check it against the firm's own history and the industry. A single peak or trough year gives a wrong growth rate; normalize if needed ([[normalizing-depressed-earnings]]).
3. Compute the reinvestment measure. For EPS use the retention ratio. For net income use actual equity reinvestment (net cap ex + ΔWC net of debt funding), because a cash-hoarding firm has a retention ratio far above its real reinvestment rate.
4. If the firm holds material cash, strip cash and its after-tax interest income out of both numerator and denominator.
5. Multiply. If you expect the return to change over the forecast, add the efficiency term and spread it over the years in which the change happens.
6. Decompose the ROE into ROC plus the leverage spread. Ask how much of the "growth" is manufactured by borrowing. Growth bought with leverage comes with a higher cost of equity, so it does not automatically add value.
7. Check the constraint `g <= ROE`, and check that the implied ROE is one the firm can plausibly sustain.

**Reference data:**

The three matched pairs (never mix across rows):
| Earnings measure | Reinvestment measure | Return measure |
|---|---|---|
| Earnings per share | Retention ratio = 1 − payout ratio | ROE = Net income / BV of equity |
| Net income from non-cash assets | Equity reinvestment rate = (Net cap ex + ΔWC − Δdebt)/Net income | Non-cash ROE = Non-cash net income / (BV equity − cash) |
| Operating income | Reinvestment rate = (Net cap ex + ΔWC)/EBIT(1−t) | ROC = EBIT(1−t) / (BV equity + BV debt − cash) — see [[fundamental-growth-operating]] |

Decision tree for equity-earnings growth:
| Measure | Return stable | Return changing |
|---|---|---|
| EPS | `g = ROE × Retention ratio` | `g = ROE_(t+1) × Retention ratio + (ROE_(t+1) − ROE_t)/ROE_t` |
| Net income | `g = ROE × Equity reinvestment ratio` | `g = ROE_(t+1) × Equity reinvestment ratio + (ROE_(t+1) − ROE_t)/ROE_t` |

**Worked examples:**

*Wells Fargo 2008 (EPS version):* ROE 17.56%, retention ratio 45.37%. `g = 0.4537 × 0.1756 = 7.97%`.
Regulatory follow-through: if the crisis forces banks to hold **30% more book equity** for the same business, then with net income unchanged the new ROE = 17.56%/1.30 = **13.51%**, and the same retention ratio gives `g = 0.4537 × 0.1351 = 6.13%`. Higher capital requirements mechanically cut sustainable EPS growth.

*Coca-Cola 2010 (non-cash net income version, $ millions):* Net income 11,809; book equity at end-2009 25,346; cash at end-2009 7,021 which earned 105 of income in 2010; cap ex 2,215; depreciation 1,443; increase in working capital 335; total debt up 150.
```
Equity reinvestment  = 2,215 − 1,443 + 335 − 150   = 957
Non-cash net income  = 11,809 − 105                = 11,704
Non-cash book equity = 25,346 − 7,021              = 18,325
Equity reinvestment rate = 957 / 11,704            = 8.18%
Non-cash ROE             = 11,704 / 18,325         = 63.87%
Expected growth = 0.0818 × 0.6387                  = 5.22%
```

*ROE decomposition — Brahma (Brazil) 1998:* ROC 19.91%, D/E 77%, after-tax cost of debt 5.61%. `ROE = 0.1991 + 0.77 × (0.1991 − 0.0561) = 30.92%`. Borrowing at 5.61% to earn 19.91% turns a good ROC into a spectacular ROE — and a spectacular fundamental growth rate. The downside is entirely in the risk, not the arithmetic.

*ROE decomposition — Titan Watches (India) 2000:* ROC 9.54%, D/E 191% (book), after-tax cost of debt 10.125%. `ROE = 0.0954 + 1.91 × (0.0954 − 0.10125) = 8.42%`. Leverage drags ROE **below** ROC because the spread is negative.

*Quiz form:* ROC 15%, after-tax cost of debt 5%, book D/E 100% -> `ROE = 0.15 + 1.0 × (0.15 − 0.05) = 25%`. An unlevered firm in the same sector with the same ROE and payout would show the *same* EPS growth (mechanically, since `g = b × ROE`) but would **not** be worth the same — the levered firm's growth is manufactured by debt, so it is riskier and gets a higher cost of equity.

*Tata Motors 2008–2013 (Rs millions):* aggregate equity reinvestment rate 87.70% and aggregate ROE 43.34% give `g = 38.01%`; using 2013 alone (reinvestment rate 80.50%, ROE 29.97%) gives `g = 24.13%`. Year-by-year values swing from −248.63% to +80.5% on reinvestment and from −27.33% to +110.14% on ROE — which is exactly why aggregation over the window is used.

*Deutsche Bank 2007:* ROE = 6,510/33,475 = 19.45%, retention = 1 − 2,146/6,510 = 67.03%, `g = 13.04%`. Normalized on average 2003–07 income of 3,954: ROE 11.81%, retention 45.72%, `g = 5.40%`.

**Determinism:**
- DETERMINISTIC: all of the arithmetic — retention ratio, ROE, non-cash ROE, equity reinvestment and its rate, `g = reinvestment × return`, the efficiency term and its annualization, and the ROE = ROC + spread decomposition — given the accounting inputs.
- JUDGMENT: choosing which version to use; whether the current-year ROE and retention ratio are sustainable (normalize a peak year or aggregate over a window?); the target ROE if you expect the return to change and how many years the change takes; whether the leverage that manufactures the ROE is itself sustainable; whether book equity is a meaningful denominator after big write-offs.

**Pitfalls:**
- Mixing rows: retention ratio times non-cash ROE, or equity reinvestment rate times plain ROE.
- Using the EPS version for a cash-rich firm. Retained earnings sitting in a money-market account do not earn the ROE, and the growth forecast will be far too high.
- Reading a peak-year ROE as sustainable (Deutsche Bank 2007: 13.04% unnormalized vs 5.40% normalized).
- Forgetting that `g <= ROE` — a payout-paying firm cannot grow at its ROE.
- Treating leverage-manufactured growth as equivalent to operating growth. Same `g`, higher cost of equity, different value.
- Using end-of-year book equity in the ROE denominator when the numerator is the whole year's income.
- Applying this framework at all when earnings are negative — the returns are meaningless; go to [[top-down-revenue-growth]].

**Sources:**
- valpacket1spr21 p.174-185, p.196
- valpacket1spr20 p.171-182, p.193
- cfpacket2spr20 p.242-246 (fundamental growth framework; Deutsche Bank normalized growth; Tata Motors equity reinvestment and ROE; ROE-and-leverage decomposition and quiz), p.256 (Deutsche Bank DDM growth)
- spreadsheet:fcffsimpleginzu.xlsx / spreadsheet:growthbreakdown.xls — ROE and ROIC diagnostics computed on beginning-of-year book values

**Related:** [[fundamental-growth-operating]], [[return-on-invested-capital]], [[value-of-growth]], [[fcfe]], [[historical-growth]], [[analyst-growth-estimates]], [[normalizing-depressed-earnings]], [[terminal-value]], [[dividend-discount-model]], [[bank-valuation]]

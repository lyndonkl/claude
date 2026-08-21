# Empirical facts about dividend policy

**Core idea:** Before prescribing what a firm *should* pay out, you need to know how firms actually behave, because real dividend policy is driven far more by inertia and imitation than by any residual-cash logic. Four empirical regularities hold up. Dividends are sticky: most firms change nothing in a given year, and almost none cut. Dividends follow earnings, but with a lag and far less volatility. Dividend behavior responds to tax law changes. And US firms increasingly return cash through buybacks rather than dividends. Two behavioral forces explain the stickiness: **inertia** (companies hate to let go of their past dividend behavior) and **me-too-ism** (companies want to look like their peer group). These facts set the practical constraints on any dividend recommendation: raising a dividend is a near-permanent commitment, and cutting one is treated by the market as a confession of failure.

**Formulas:**
- Payout ratio = Dividends / Net Income (undefined/meaningless when Net Income ≤ 0).
- Cash returned = Dividends + Stock Buybacks.
- % of cash from buybacks = Buybacks / (Dividends + Buybacks).
- Cash return / Net income = (Dividends + Buybacks) / Net Income. Values above 100% mean the aggregate group returned more than it earned.

**Procedure:**
1. Pull the firm's dividends per share for the last 10 years. Count the years of increases, no-changes, and decreases. Expect the modal outcome to be "no change"; a firm that has raised its dividend every year for a decade has effectively made a fixed commitment.
2. Plot dividends against net income over the same period. Confirm the smoothing: the standard deviation of the dividend series should be far below that of earnings. Compute the payout ratio each year; spikes in payout usually mean an earnings collapse, not a dividend increase.
3. Add buybacks to the picture. If buybacks are a large or volatile share of cash returned, any analysis using dividends alone (peer comparisons, regression predictions, yield screens) will understate the firm's payout — flag this before drawing conclusions.
4. Check the tax regime. If dividend taxes are about to rise, expect (and do not over-interpret) special dividends and accelerated payouts, especially at firms with concentrated insider ownership (above ~20% insider holdings is the threshold Damodaran highlights).
5. Diagnose the driver of current policy. Ask: is this dividend the residue of a genuine cash-flow calculation, or is it (a) last year's dividend plus a token increase (inertia) or (b) matched to sector norms (me-too-ism)? Almost always it is (a) or (b) — which means the dividend is a legacy constraint, not evidence that the firm can afford it.
6. Translate stickiness into an asymmetry rule for recommendations: treat a dividend increase as permanent (you must be able to fund it in a bad year), and treat a dividend cut as costly (roughly −5% to −8% announcement returns; see [[dividend-signaling]]).

**Reference data:**

*Fact 1 — Dividend stickiness, US companies 1988–2019 (share of firms per year):* no change ≈ 55–73%; increases ≈ 20–40%; decreases ≈ 3–12%. Cutting is rare in every single year of the sample.

*Fact 1 tested — S&P 500 dividend actions by quarter through the 2008 crisis (number of companies):*

| Quarter | Increase | Initiated | Decrease | Suspension |
|---|---|---|---|---|
| Q1 2007 | 102 | 1 | 1 | 1 |
| Q2 2007 | 63 | 1 | 1 | 5 |
| Q3 2007 | 59 | 2 | 2 | 0 |
| Q4 2007 | 63 | 7 | 4 | 2 |
| Q1 2008 | 93 | 3 | 7 | 4 |
| Q2 2008 | 65 | 0 | 9 | 0 |
| Q3 2008 | 45 | 2 | 6 | 8 |
| Q4 2008 | 32 | 0 | 17 | 10 |

Even in the worst quarter of the worst financial crisis in 70 years, only 27 of 500 firms cut or suspended.

*Fact 2 — Dividends follow earnings (S&P 500, 1960–2019):* dividends rise with earnings but far more smoothly. Aggregate payout ratio drifted from above 60% in the early 1960s to roughly 30–45% in the 2010s, spiking whenever earnings collapsed (e.g. 2008).

*Fact 3 — Taxes move dividends:* In 2003, when the US cut dividend tax rates to parity with capital gains, 21 S&P 500 companies initiated dividends, 247 increased, 11 decreased and 5 stopped. In Q4 2012, with tax rates expected to revert to pre-2003 levels, 233 companies paid out $31 billion in dividends; 101 of them had insider holdings above 20% of shares outstanding.

*Fact 4 — Buybacks displace dividends (S&P 500, 1988–2019):* buybacks were ~1/3 of cash returned in 1988 and dipped below 20% around 1991. From the late 1990s onward they exceeded dividends. Through the 2000s–2010s they ran at roughly 60–72% of cash returned, dipping to ~45% in 2009. By 2019: buybacks ≈ $770bn vs dividends ≈ $480bn (~60% from buybacks).

*Fact 4 globally — cash returned by sub-region (January 2020, $ millions):*

| Sub Region | # firms | Net Income | Dividends | Buybacks | % Cash from Buybacks | Payout Ratio | Cash Return/NI |
|---|---|---|---|---|---|---|---|
| Africa and Middle East | 2,217 | 238,788 | 145,871 | 8,415 | 5.45% | 61.09% | 64.61% |
| Australia & NZ | 1,676 | 68,690 | 49,964 | 12,800 | 20.39% | 72.74% | 91.37% |
| Canada | 2,707 | 99,281 | 57,484 | 53,501 | 48.21% | 57.90% | 111.79% |
| China | 6,199 | 750,166 | 383,121 | 21,854 | 5.40% | 51.07% | 53.98% |
| EU & Environs | 5,537 | 693,958 | 352,810 | 140,637 | 28.50% | 50.84% | 71.11% |
| Eastern Europe & Russia | 515 | 86,133 | 33,809 | 5,899 | 14.86% | 39.25% | 46.10% |
| India | 3,589 | 64,561 | 28,009 | 6,761 | 19.44% | 43.38% | 53.86% |
| Japan | 3,854 | 396,037 | 128,485 | 77,562 | 37.64% | 32.44% | 52.03% |
| Latin America & Caribbean | 928 | 89,883 | 48,011 | 7,885 | 14.11% | 53.42% | 62.19% |
| Small Asia | 8,876 | 328,942 | 141,139 | 15,160 | 9.70% | 42.91% | 47.52% |
| UK | 1,243 | 147,586 | 95,403 | 39,341 | 29.20% | 64.64% | 91.30% |
| United States | 7,053 | 1,282,385 | 570,044 | 859,748 | 60.13% | 44.45% | 111.49% |

Read: the US and Canada are the buyback outliers and both returned more than 100% of net income; Asia, Africa and Latin America still return cash almost entirely as dividends.

**Worked example:** United States, January 2020. Net income $1,282,385M, dividends $570,044M, buybacks $859,748M. Payout ratio = 570,044 / 1,282,385 = 44.45%. Cash returned = 570,044 + 859,748 = $1,429,792M. % from buybacks = 859,748 / 1,429,792 = 60.13%. Cash return / net income = 1,429,792 / 1,282,385 = 111.49%. An analyst who looked only at the 44.45% payout ratio would conclude US firms were retaining most of their earnings; adding buybacks shows they returned more than they earned.

**Determinism:**
- DETERMINISTIC: payout ratio, dividend yield, cash returned, % from buybacks, cash return/net income, and the counts of increases/no-changes/decreases — all computed from dividends, buybacks, net income and share prices. Classifying a year as increase/no-change/decrease from a dividends-per-share series is a script.
- JUDGMENT: deciding whether the observed policy is driven by inertia, peer imitation, or genuine cash-flow logic; deciding how much of a tax-driven special dividend is repeatable; forecasting whether the buyback share will persist.

**Pitfalls:**
- Comparing firms or regions on dividend yield or payout ratio alone when buybacks are material. In the US this understates cash returned by more than half.
- Treating an aggregate payout ratio above 100% as an error — it is common (about 15% of dividend-paying firms globally pay out more than they earn) and is a signal, not a typo.
- Computing a payout ratio on negative net income. The number is meaningless; report NA.
- Reading a dividend increase as a pure signal of confidence when it may just be inertia plus a token bump, or a tax-timing response.
- Assuming stickiness means safety. Stickiness means firms delay cuts, so an unaffordable dividend can persist for years before a brutal, forced cut (see the BP case under [[dividend-matrix]]).

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.151-157

**Related:** [[dividend-payout-and-yield-measures]], [[dividend-life-cycle]], [[dividend-signaling]], [[cash-returned-dividends-and-buybacks]], [[three-schools-of-dividend-thought]], [[cash-trust-assessment]]

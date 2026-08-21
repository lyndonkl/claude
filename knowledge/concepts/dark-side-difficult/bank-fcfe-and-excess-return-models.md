# Bank reinvestment: regulatory capital, FCFE and equity excess returns

**Core idea:** Book value is close to irrelevant for an industrial company. It is a historical number, and more than a thousand listed US firms have negative book equity. For a bank it is the opposite. Assets are marked to market, so book equity is a reasonable statement of what the bank owns right now, and regulatory capital ratios are computed **on** book equity, so a bank with negative or even low book equity gets shut down. That gives banks something industrial firms lack: a hard definition of reinvestment. A bank reinvests by adding to its book equity, and it must add enough to support both its growth ambitions and its safety requirements. Two models follow. Free cash flow to equity is net income minus that required addition. The equity excess-return model says the value of a bank equals the book equity it already has plus the present value of everything it earns above its cost of equity.

**Formulas:**
- Reinvestment for a bank: `Investment in regulatory capital_t = Required book equity_t − Book equity_{t−1}`.
- `FCFE_t = Net income_t − Investment in regulatory capital_t`.
- Required capital from the ratio: `Tier 1 capital_t = Risk-adjusted assets_t × Tier 1 ratio_t`, with book/common equity moving in step.
- `Net income_t = Book equity_{t−1} × Expected ROE_t`.
- Value of equity (FCFE route): `Σ FCFE_t / (1 + k_e)^t + Terminal value of equity / (1 + k_e)^n`.
- Excess-return route: `Value of equity = Current book equity + PV of expected excess equity returns`, where
  `Excess equity return_t = Net income_t − (Cost of equity_t × Beginning book equity_t)`.
- Book-equity rollforward inside the excess-return model: `NI_t = ROE_t × BV_t`; `Dividends_t = NI_t × payout_t`; `Retained_t = NI_t − Dividends_t`; `BV_{t+1} = BV_t + Retained_t`.
- Terminal value of excess returns: `TV = Excess return_{n+1} / (k_e,stable − g_stable)`.
- Discounting uses the cumulated cost of equity: `Cum_t = Π_{s≤t} (1 + k_e,s)`; `PV_t = Excess return_t / Cum_t`.
- Wipeout overlay: `Adjusted value per share = DCF value per share × (1 − P(equity wipeout))`.

**Procedure (FCFE-to-regulatory-capital, for a bank in transition or crisis):**
1. Project risk-adjusted assets. A bank not growing in real terms grows them at the inflation rate.
2. Set the path of the Tier 1 (or CET1) ratio from where the bank is today to where the regulator and the market will require it to be. Anchor the target on the peer distribution — Deutsche Bank's target of 15.67% was the 75th percentile of all banks.
3. Required capital each year = risk-adjusted assets × the ratio for that year. The year-on-year increase is the reinvestment.
4. Subtract any one-off hits to capital today (Deutsche Bank: an expected $10 billion Department of Justice fine).
5. Project ROE from its current level to a sustainable one, again anchored on the peer distribution. Set the terminal ROE equal to the cost of equity unless a franchise justifies more.
6. Net income = beginning book equity × ROE. FCFE = net income − investment in regulatory capital. Expect FCFE to be deeply negative early when the bank must rebuild capital.
7. Discount at a cost of equity that starts high (crisis) and falls to the sector median.
8. Add a terminal value of equity, divide by shares, then apply any probability of a catastrophic wipeout.

**Procedure (equity excess-return model, eqexret.xls):**
1. Enter current net income, current book equity, prior-year book equity, EPS, DPS and share count. Fundamental ROE = `net income / prior-year book equity`; fundamental retention = `1 − DPS/EPS`.
2. Normalize net income if the current year is unrepresentative — either the average of the last five years, or a normalized ROE applied to book equity.
3. Set the high-growth ROE and retention (override the fundamentals if the current ROE is unsustainable), the length of the high-growth period, and the stable-period ROE and growth.
4. Stable payout defaults to `1 − g_stable / ROE_stable`.
5. Choose whether inputs fade over the second half of the high-growth period. With fading on, ROE, payout and cost of equity all move linearly to their stable values over the last half of the horizon.
6. Roll book equity forward year by year, computing net income, the equity cost, the excess return, dividends and retained earnings.
7. Terminal excess return divided by `(k_e,stable − g_stable)` gives the terminal value; discount everything at the cumulated cost of equity.
8. `Value of equity = current book equity + PV of excess returns`. Divide by shares.

**Reference data (1):** Deutsche Bank, October 2016 — an FCFE-to-regulatory-capital valuation in crisis.

| Item | Current | Year 10 |
|---|---|---|
| Risk-adjusted assets | $445,570m | $492,186m (growing at 1% inflation) |
| Tier 1 ratio | 12.41% | 15.67% (75th percentile of banks) |
| Tier 1 capital | $55,282m | — |
| Book equity | $64,609m | $86,453m |
| ROE | −13.70% | 9.440% (= cost of equity, bank median) |
| Net income | −$8,851m | $8,161m |
| Cost of equity | 10.20% (75th percentile) | 9.44% |
| FCFE | −$11,663m (year 1) | $6,352m |

ROE path: −13.70% now, then −7.18%, −2.84%, 0.06%, 1.99%, 5.85% (25th percentile of banks, year 5), 6.568%, 7.286%, 8.004%, 8.722%, 9.440%. Terminal value of equity $87,317m. Value of equity today $31,838.7m over 1,386m shares = **$22.97 per share**; after a 10% probability of complete equity wipeout, **$20.67** against a price of $13.33 on 3 October 2016.

**Reference data (2):** eqexret.xls fade schedule for a 10-year horizon with second-half fading switched on. High-growth ROE 25%, retention 80.6316%, cost of equity 9.6%; stable ROE 15%, stable growth 5%, stable beta 1.1, so stable cost of equity = 5% + 1.1 × 4% = 9.4% and stable payout = 1 − 5/15 = 66.6667%.

| Year | 1–5 | 6 | 7 | 8 | 9 | 10 | Terminal |
|---|---|---|---|---|---|---|---|
| ROE | 0.25 | 0.23 | 0.21 | 0.19 | 0.17 | 0.15 | 0.15 |
| Dividend payout | 0.193684 | 0.288281 | 0.382877 | 0.477474 | 0.572070 | 0.666667 | 0.666667 |
| Cost of equity | 0.0960 | 0.0956 | 0.0952 | 0.0948 | 0.0944 | 0.0940 | 0.0940 |

**Worked example:** The equity excess-return model, end to end (eqexret.xls stored case). Current book equity 17,997; prior-year book equity 15,518; net income 4,791; EPS 4.75; DPS 0.92; 1,120.713 shares; beta 1.15, riskfree 5%, premium 4% → cost of equity 9.6%. High-growth ROE is overridden to 25% (the fundamental 30.87% is not sustainable), retention 80.6316%, so expected growth = 20.16%.

Year 1: `NI = 0.25 × 17,997 = 4,499.25`; equity cost = `0.096 × 17,997 = 1,727.71`; excess return = **2,771.54**; PV = 2,771.54/1.096 = 2,528.78. Dividends = 4,499.25 × 0.193684 = 871.43, retained 3,627.82, so book equity rises to 21,624.82.

Year 10: book equity 69,876.34, ROE 15%, net income 10,481.45, excess return 3,913.07. Terminal year: book equity 73,370.15, net income 11,005.52, equity cost 6,896.79, excess return 4,108.73. Terminal value = 4,108.73/(0.094 − 0.05) = 93,380.20; PV of year 10 = (3,913.07 + 93,380.20)/2.48729 = 39,116.18. Sum of present values = 65,993.76. Value of equity = 17,997 + 65,993.76 = **83,990.76**; ÷ 1,120.713 shares = **74.94 per share**.

**Determinism:** DETERMINISTIC — (risk-adjusted assets path, Tier 1 ratio path, ROE path, cost-of-equity path, share count, wipeout probability) → required capital, net income, FCFE, value per share; and (book equity, ROE path, payout path, cost-of-equity path, growth, horizon) → excess returns, terminal value, equity value, value per share. Both examples above are exactly reproducible. JUDGMENT: the target capital ratio and how fast the bank must get there (needs the regulatory regime and the peer percentile distribution), the ROE recovery path, the sustainable ROE, one-off capital hits such as fines, the probability of an equity wipeout, and whether to normalize earnings at all.

**Pitfalls:**
- Treating a rising capital ratio as free. Every increase is reinvestment, and it comes straight out of FCFE.
- Growing book equity by retained earnings alone while assuming the capital ratio also improves. Both cannot happen unless net income is large enough; the model must reconcile them.
- Using the current, crisis-depressed ROE as the terminal ROE. Terminal ROE should equal the cost of equity unless there is a franchise.
- Ignoring the terminal-value sensitivity: with a stable cost of equity of 9.4% and stable growth of 5%, the denominator is 4.4%, so a 50 basis-point error in either input moves value by more than 10%.
- Setting stable ROE below stable growth in the excess-return model. Then `payout = 1 − g/ROE` goes negative, which means retention above 100%; the spreadsheet carries it mechanically and produces nonsense.
- Forgetting the fundamental ROE convention: it is computed on **prior-year** book equity, while the valuation rolls forward from **current** book equity. Keep both numbers.
- Skipping the wipeout probability for a bank in genuine crisis. The equity of a rescued bank is often worth nothing even when the bank survives.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.345-346
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.336-337
- spreadsheet model doc: focussed-eva-finsvc.md — eqexret.xls (financial-service equity excess return model)

**Related:** [[financial-service-firm-valuation]], [[distress-and-failure-adjusted-value]], [[normalized-earnings]], [[difficult-company-taxonomy]], [[excess-return-models]], [[cost-of-equity]], [[book-value-of-equity]]

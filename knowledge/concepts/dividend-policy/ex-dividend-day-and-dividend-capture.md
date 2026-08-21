# Ex-dividend day price drop, implied taxes and dividend capture

**Core idea:** On the ex-dividend day a stock's price falls, but not necessarily by the full dividend. The size of the drop relative to the dividend reveals the tax rates of the marginal investor in that stock. The logic is an indifference condition: an investor deciding whether to sell just before or just after the stock goes ex-dividend must be equally well off after tax either way. Solve that condition and the price drop divided by the dividend equals the ratio of the after-tax "keep rates" on ordinary income and capital gains. When the drop is less than the dividend, a tax-exempt investor can capture the difference — the dividend capture trade.

**Formulas:**

Notation:
- P = price at which the investor originally bought the stock
- P_b = price just before the stock goes ex-dividend (cum-dividend price)
- P_a = price just after the stock goes ex-dividend
- D = dividend per share declared
- t_o = tax rate paid on ordinary income (dividends)
- t_cg = tax rate paid on capital gains

Cash flow from selling **before** the ex-dividend day: P_b − (P_b − P) × t_cg
Cash flow from selling **after** the ex-dividend day: P_a − (P_a − P) × t_cg + D × (1 − t_o)

Indifference condition:
P_b − (P_b − P) × t_cg = P_a − (P_a − P) × t_cg + D × (1 − t_o)

Solving gives the central result:

**(P_b − P_a) / D = (1 − t_o) / (1 − t_cg)**

Dividend capture profit for a tax-exempt investor, where the observed drop ratio is k = (P_b − P_a)/D:
Profit per share = D − (P_b − P_a) = D × (1 − k)
Total profit = N × D × (1 − k), where N = number of shares traded (before transaction costs).

**Procedure:**
1. Collect the closing price the day before the ex-dividend date (P_b), the opening/closing price on the ex-dividend date (P_a), and the dividend per share (D). Adjust for any market-wide move on the day, otherwise the drop is contaminated by market noise.
2. Compute the observed ratio k = (P_b − P_a) / D. Average k over many dividend events for the stock or the market; a single event is far too noisy.
3. Read the marginal investor's tax position from k using the rules below.
4. Invert the formula for an implied tax differential: if you assume t_cg, then t_o = 1 − k × (1 − t_cg). Example: k = 0.90 with t_cg = 0.28 implies t_o = 1 − 0.90 × 0.72 = 0.352.
5. If k < 1 and you are tax-exempt, evaluate the dividend capture trade: buy cum-dividend, sell ex-dividend, collect D. Expected gross profit per share = D × (1 − k). Test it against round-trip transaction costs and the price risk over the holding period before acting.
6. Use the result as a clientele diagnostic, not just an arbitrage screen. A k well below 1 says the marginal holder is taxed heavily on dividends, which supports a low-payout policy for that firm (see [[clientele-effect]]).

**Decision rules (relative tax rates → ex-dividend behavior):**

| Tax situation | Predicted ex-dividend behavior |
|---|---|
| Dividends and capital gains taxed equally (t_o = t_cg) | Price change = Dividend (k = 1) |
| Dividends taxed at a higher rate (t_o > t_cg) | Price change < Dividend (k < 1) |
| Dividends taxed at a lower rate (t_o < t_cg) | Price change > Dividend (k > 1) |

**Reference data — US empirical evidence by tax regime:**

| Period | Ordinary tax rate t_o | Capital gains rate t_cg | Predicted k = (1−t_o)/(1−t_cg) | Observed price change as % of dividend |
|---|---|---|---|---|
| 1966–1969 | 70% | 28% | 0.417 | 78% |
| 1981–1985 | 50% | 20% | 0.625 | 85% |
| 1986–1990 | 28% | 28% | 1.000 | 90% |

The direction matches the theory — as the tax gap narrowed, the drop ratio rose toward 100%. The observed ratios sit above the naive prediction because the marginal investor is a blend of taxable, tax-exempt and institutional holders, not the top-bracket individual.

**Worked example — dividend capture (XYZ Corporation):** XYZ trades at $50 at the close of May 3 and goes ex-dividend on May 4 with a $1 dividend. Historically the price drop on this stock has been only 90% of the dividend (k = 0.90). A tax-exempt US pension fund:
1. Buys 1 million shares cum-dividend at $50.00 → outflow $50.000 million.
2. Sells ex-dividend at $49.10 = $50 − ($1 × 0.90) → inflow $49.100 million.
3. Collects the dividend, $1.00 per share, tax free → inflow $1.000 million.
Net profit = −50.000 + 49.100 + 1.000 = **$0.100 million** (= 1,000,000 × $1 × (1 − 0.90)). That is a 0.2% return on $50 million, earned in one day, before transaction costs.

**Determinism:**
- DETERMINISTIC: k from P_b, P_a and D. The predicted ratio from t_o and t_cg. The implied t_o from an observed k and an assumed t_cg. The dividend-capture profit from D, k and share count.
- JUDGMENT: identifying the marginal investor and whether the observed k reflects taxes rather than microstructure (bid-ask bounce, tick size, market moves on the day). Deciding whether the arbitrage survives transaction costs, price risk and the risk of the price not dropping as expected. Choosing the estimation window.

**Pitfalls:**
- Using a single ex-dividend event. Daily price noise dwarfs a typical dividend, so k must be averaged over many events.
- Failing to strip out the market return on the ex-dividend day.
- Treating dividend capture as riskless. The investor holds equity price risk overnight, pays two sets of transaction costs, and the historical drop ratio is an average, not a guarantee.
- Concluding from k < 1 that "dividends destroy value". The relationship is about *who* holds the stock and how they are taxed, not about the firm's value.
- Ignoring that since 2003 US dividends and capital gains are taxed alike, so the classic tax-arbitrage motivation is much weaker than the historical tables imply (see [[three-schools-of-dividend-thought]]).
- Using the ex-dividend drop as a rebuttal to the bird-in-the-hand argument without saying why: the point is that the dividend is not extra money, it comes out of the price (see [[bad-reasons-for-paying-dividends]]).

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.167-173

**Related:** [[three-schools-of-dividend-thought]], [[clientele-effect]], [[bad-reasons-for-paying-dividends]], [[dividend-payout-and-yield-measures]]

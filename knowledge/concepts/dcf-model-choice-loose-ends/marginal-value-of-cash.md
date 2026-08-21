# The marginal value of cash (discount, par, or premium)

**Core idea:** A dollar of cash on a balance sheet is not always worth a dollar to a shareholder. What it is worth depends on what management will do with it. If the firm earns its cost of capital, cash is a neutral asset held at face value. If the firm earns less than its cost of capital, the cash is a wasting asset — it will be spent on value-destroying projects, so it is worth less than face. If the firm earns large excess returns, cash is a call option on future value creation and can be worth more than face. Note the reason carefully: cash is *not* discounted because it earns a low return. A riskless asset should earn a riskless rate. Cash is discounted for the risk that managers do something stupid with it.

**Formulas:**
- Neutrality test: compare `ROIC` with the `cost of capital`. Cash is neutral when they are equal.
- Value of a perpetually underperforming pool of assets: `Value/NAV = Expected Return on assets / Required Return`; `Discount = 1 − (Required Return − Underperformance)/Required Return = Underperformance / Required Return`.
- Cash at face value: `Value of cash = Cash Earnings / Riskfree Rate` when it earns a fair riskless return.

**Reference data:**

Classification test:

| ROIC versus cost of capital | Cash is | Worth |
|---|---|---|
| ROIC ≈ cost of capital | Neutral asset | Face value |
| ROIC < cost of capital | Wasting asset | Less than face value |
| ROIC > cost of capital | Potential value creator | More than face value |

Empirical evidence — regressions of enterprise value against cash balances estimate the market value of $1 of cash:

| Firm group | Market value of $1 of cash |
|---|---|
| Mature firms with negative excess returns | ≈ $0.75 (2020 edition: ≈ $0.72) |
| All firms | ≈ $1.00 |
| High-growth firms with high excess returns | ≈ $1.25 |

Closed-end funds as the pure case: a November 2011 histogram of closed-end fund premiums and discounts to net asset value shows most funds at discounts of 0–12%, with tails beyond ±21%.

Berkshire Hathaway, the most famous closed-end fund analogue — its price-to-book "Buffett premium" has eroded:

| Date | Berkshire P/BV | US general insurance sector P/BV |
|---|---|---|
| December 2009 | 1.54 | 1.10 |
| December 2019 | 1.27 | 1.47 |

The 2020 edition gives the fuller series: 1.84 (1993), peak 2.62 (1997), trough 1.07 (2008), about 1.30 by 2015. Berkshire went from a premium to a discount relative to peers.

**Procedure:**
1. Estimate the firm's return on invested capital on its non-cash operations, and its cost of capital.
2. Classify the cash using the table above.
3. If ROIC is below the cost of capital, ask *why* you would discount. The right reason is the risk of poor deployment: a record of overpriced acquisitions, pie-in-the-sky projects, or entrenched management with no payout discipline.
4. Size the discount from the expected shortfall, not from the low interest rate on the cash. The closed-end fund formula gives a defensible anchor: `discount = annual underperformance / required return`.
5. Cross-check against the market evidence: $0.75 on the dollar is roughly what the market applies to mature, value-destroying firms; $1.25 to high-return growth firms.
6. Sanity-check the governance angle. Better governance, a credible payout policy, or an activist on the register all argue for holding cash closer to face value.

**Worked example (the three-company exercise):** Three firms each have enterprise value $1,000 and cash $100.

| | Company A | Company B | Company C |
|---|---|---|---|
| Enterprise value | $1,000.0 | $1,000.0 | $1,000.0 |
| Cash | $100.0 | $100.0 | $100.0 |
| Return on invested capital | 10% | 5% | 22% |
| Cost of capital | 10% | 10% | 12% |
| Trades in | US | US | Argentina |

Company A's cash is a neutral asset worth $100. Company B's is a wasting asset: management earns 5% against a 10% cost of capital, so the cash will probably be destroyed and is worth less than $100. Company C's is a potential value creator: at a 10-point excess return, cash handed to this management is worth more than face.

**Closed-end fund arithmetic:** a fund holds average-risk stocks. The market is expected to return 11.5% a year long term. The fund underperforms by 0.50% annually, so it earns 11.0%. Value per $1 of NAV = 0.11/0.115 = $0.9565, a discount of about **4.3%**. The same logic prices perpetual management underperformance in any asset pool.

**Determinism:**
- DETERMINISTIC: the ROIC-versus-cost-of-capital comparison; the closed-end fund discount formula given required return and underperformance.
- JUDGMENT: whether the firm's historical excess return will persist, and how likely management is to waste the cash. That needs the acquisition track record, governance structure, ownership concentration, and stated capital-allocation policy. The empirical $0.75/$1.00/$1.25 figures are evidence, not a formula to apply mechanically.

**Pitfalls:**
- Discounting cash because it earns 1% while the business earns 15%. Riskless assets earn riskless returns; that is not value destruction.
- Applying a cash discount and *also* lowering the growth or return assumptions for bad management — the same sin charged twice.
- Assuming a premium on cash for any growth company. The premium requires demonstrated excess returns and a reinvestment runway.
- Treating a long-standing price-to-book premium as permanent. Berkshire's faded as the firm grew.

**Sources:**
- valpacket1spr21 p.221-225
- valpacket1spr20 p.217-221

**Related:** [[cash-in-valuation]], [[equity-value-bridge]], [[ddm-fcfe-reconciliation]], [[excess-returns]], [[corporate-governance-discount]], [[complexity-discount]]

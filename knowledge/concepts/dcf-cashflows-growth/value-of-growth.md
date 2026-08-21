# The value of growth (growth can be good, bad or neutral)

**Core idea:** Growth is not automatically good. It has a good side — revenues and operating income rise — and a bad side — cash must be set aside as reinvestment to produce that rise. Whether growth adds value depends entirely on whether the return earned on the new capital exceeds the cost of that capital. Growth at `ROIC > cost of capital` creates value; growth at `ROIC = cost of capital` is exactly value-neutral no matter how fast; growth at `ROIC < cost of capital` destroys value, and the faster the firm grows the more it destroys. Growth that comes from earning a better return on *existing* assets (efficiency growth) requires no new capital and is therefore the cheapest growth there is.

**Formulas:**
- `Expected growth = Growth from new investments + Efficiency growth = Reinvestment rate × ROIC + (ROIC_t − ROIC_(t−1)) / ROIC_(t−1)`
- Value with growth, stable-growth form: `Value = EBIT(1−t)_(n+1) × (1 − g/ROC) / (Cost of capital − g)`
  - When `ROC = cost of capital`, this collapses to `EBIT(1−t)_(n+1) / Cost of capital` for **any** `g` — growth is value-neutral.
  - When `ROC > cost of capital`, value rises with `g`. When `ROC < cost of capital`, value falls with `g`.
- Value of assets in place (no-growth benchmark) = `EBIT(1−t) / Cost of capital`.
- Value added by growth = (Value of the firm with its growth forecast) − (Value of assets in place).
- Price the market is paying for growth = (Market enterprise value) − (Value of assets in place).
- Price-to-value of growth = `Price paid for growth / Value added by growth`. Greater than 1 means the market is paying more for growth than the growth is worth on your assumptions.

**Procedure:**
1. Decompose the firm's expected growth into the two sources: reinvestment-driven growth (`reinvestment rate × ROIC on new investment`) and efficiency growth (improvement in the return on existing capital).
2. For the reinvestment-driven part, compare the ROIC on **new** investment to the cost of capital. That spread, not the growth rate, decides value.
3. For the efficiency part, note that it adds value with no capital outlay — but it is finite (a firm cannot keep improving its return forever) and it cannot be assumed in stable growth.
4. Compute the no-growth benchmark value: capitalize current after-tax operating income at the cost of capital with zero reinvestment.
5. Compute the value with your growth forecast (year-by-year FCFF plus terminal value). The difference is the value of growth on your assumptions.
6. Compare against what the market is paying: `market enterprise value − no-growth value` is the market's price for growth. The ratio of the two tells you how far apart you and the market are on the growth story.
7. Optionally invert: use a root-find (Excel's Goal Seek) on the growth rate that makes your value-of-growth equal the market's price-of-growth. That is the market-implied growth rate — a cleaner statement of what you would have to believe.
8. Carry the rule into the terminal value: extending a high-growth period only adds value if the firm keeps earning excess returns through it ([[terminal-value]]).

**Reference data:**

Five firms, all growing at exactly 10%, with a 10% cost of capital:
| | Firm 1 | Firm 2 | Firm 3 | Firm 4 | Firm 5 |
|---|---|---|---|---|---|
| Reinvestment rate | 20.00% | 100.00% | 200.00% | 20.00% | 0.00% |
| ROIC on new investment | 50.00% | 10.00% | 5.00% | 10.00% | 10.00% |
| ROIC on existing investments, before | 10.00% | 10.00% | 10.00% | 10.00% | 10.00% |
| ROIC on existing investments, after | 10.00% | 10.00% | 10.00% | 10.80% | 11.00% |
| **Expected growth rate** | **10.00%** | **10.00%** | **10.00%** | **10.00%** | **10.00%** |

Ranking by the value of that growth: **Firm 1** (all growth from new investment at 50% versus a 10% cost of capital) and **Firm 5** (all growth from efficiency, no capital consumed) create the most value. **Firm 4** creates some value from its efficiency component. **Firm 2** creates none from new investment (ROIC = cost of capital). **Firm 3** destroys value — it reinvests 200% of its earnings at 5% to buy the same 10% growth.

Terminal value sensitivity to ROC versus g. After-tax operating income in year n+1 = $100m; cost of capital 10%; each cell = `100 × (1 − g/ROC) / (0.10 − g)`:
| g forever \ ROC | 6% | 8% | 10% | 12% | 14% |
|---|---|---|---|---|---|
| 0.0% | $1,000 | $1,000 | $1,000 | $1,000 | $1,000 |
| 0.5% | $965 | $987 | $1,000 | $1,009 | $1,015 |
| 1.0% | $926 | $972 | $1,000 | $1,019 | $1,032 |
| 1.5% | $882 | $956 | $1,000 | $1,029 | $1,050 |
| 2.0% | $833 | $938 | $1,000 | $1,042 | $1,071 |
| 2.5% | $778 | $917 | $1,000 | $1,056 | $1,095 |
| 3.0% | $714 | $893 | $1,000 | $1,071 | $1,122 |

Read the middle column: at ROC = cost of capital the terminal value is $1,000 regardless of growth. Read the left columns: at ROC below the cost of capital, more growth means less value.

**Worked example — decomposing price into assets-in-place and growth ($ millions):** A firm with EBIT 1,695, effective tax rate 40%, invested capital 3,694 at the start of the year, cost of capital 11.42%, riskfree rate 2%, market capitalization 70,000, debt 1,215, cash 1,512.
```
After-tax operating income          = 1,695 × 0.60             = 1,017
ROIC                                = 1,017 / 3,694            = 27.53%
Value of assets in place (no growth)= 1,017 / 0.1142           = 8,905
Growth-scenario value (10 years at 11.42% growth, reinvestment
   rate g/ROIC = 41.48%, then stable at g = rf = 2% with
   ROC = cost of capital)                                      = 14,857
Value added by future growth        = 14,857 − 8,905           = 5,951
Market enterprise value             = 70,000 + 1,215 − 1,512   = 69,703
Price the market pays for growth    = 69,703 − 8,905           = 60,798
Price of growth / value of growth   = 60,798 / 5,951           = 10.2x
```
The market is paying **ten times** what the growth is worth on these assumptions. That is the number to argue about, rather than arguing about the share price.

**Determinism:**
- DETERMINISTIC: the growth decomposition; the no-growth benchmark; the growth-scenario value given the assumption set; the value-of-growth and price-of-growth arithmetic and their ratio; every cell of the ROC-vs-g sensitivity table; the implied-growth root-find.
- JUDGMENT: the ROIC on **new** investment (not the same as the historical ROIC on existing assets); how much efficiency improvement is available and over how long; the length of the growth period; and, above all, whether a spread between ROIC and the cost of capital can survive competition.

**Pitfalls:**
- Treating a higher growth rate as automatically higher value. Firm 3 grows at 10% and destroys value doing it.
- Applying the firm's historical ROIC to new investment. Competition usually means the marginal return is below the average return.
- Counting efficiency growth as a permanent source. It is a one-off improvement spread over a transition and cannot be assumed in stable growth ([[terminal-value]]).
- Extending the high-growth period without asking whether excess returns survive it — growth without excess returns adds nothing, so a longer period of it adds nothing.
- Comparing your value of growth to the market's price of growth while using two different definitions of enterprise value.
- Ignoring the mechanical consequence: at ROC = cost of capital, the entire growth debate is irrelevant to value.

**Sources:**
- valpacket1spr21 p.159, p.191, p.205, p.207
- valpacket1spr20 p.156, p.188, p.201, p.203
- cfpacket2spr20 p.265 (the four levers of value: existing cash flows, growth from new investment, efficiency growth, length of the growth period, cost of capital)
- spreadsheet:growthbreakdown.xls — assets-in-place vs value-added-by-growth decomposition, market price of growth, price/value of growth ratio, Goal-Seek for the market-implied growth rate

**Related:** [[fundamental-growth-operating]], [[return-on-invested-capital]], [[terminal-value]], [[fcff]], [[historical-growth]], [[dcf-case-valuations]], [[cost-of-capital]], [[competitive-advantage]]

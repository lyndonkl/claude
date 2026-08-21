# Bad reasons for paying dividends

**Core idea:** Two arguments for paying dividends are made constantly and are both wrong. The **bird-in-the-hand fallacy** claims that a dividend today is more certain than a capital gain tomorrow, so dividend payers deserve higher valuations. It fails because the correct comparison is a dividend today against price appreciation today — the stock price drops on the ex-dividend day, so the dividend is not extra money. The **"we have excess cash this year"** argument says the firm has a cash surplus and no projects, so it should pay a dividend. It fails on two counts: a buyback is the better vehicle for one-time cash, and a dividend once raised is sticky, while re-raising the cash later through an equity issue is very expensive. Recognizing both fallacies matters because they are the usual justification for the sticky, inertia-driven policies that get firms into trouble.

**Formulas:**
- Why the bird-in-the-hand argument fails. Total return to a stockholder = Dividend Yield + Price Appreciation. Paying a dividend of D converts price into cash: on the ex-dividend day the price falls by roughly D (exactly D when dividends and capital gains are taxed alike; see [[ex-dividend-day-and-dividend-capture]]). The dividend is a transfer from the price to the pocket, not an addition to wealth.
- Cost of paying out and re-raising. Net cost of returning $X now and re-raising it later ≈ X × f, where f = flotation cost as a fraction of funds raised. Use the table below for f.
- The stickiness cost of a dividend versus a buyback. A dividend increase of ΔD per year is effectively a perpetual commitment with present value ≈ ΔD / (k_e − g), where k_e = cost of equity and g = expected growth in the dividend. A one-time buyback of the same amount commits nothing.

**Procedure:**
1. When a firm justifies a dividend by pointing to certainty of income, test the claim by measuring the ex-dividend price drop for that stock. If the price drops by roughly the dividend, the "certain income" is coming out of the shareholder's own capital.
2. When a firm justifies a dividend by pointing to a cash surplus, first classify the surplus: is it recurring (structural FCFE > 0, see [[fcfe-potential-dividends]]) or one-time (asset sale, cyclical peak, one large settlement)?
3. If the surplus is recurring and the firm is mature, a dividend increase is defensible.
4. If the surplus is one-time, recommend a buyback or a **special** dividend, never a permanent increase in the regular dividend. A buyback is a one-shot return of cash with no expectation of repetition.
5. Quantify the cost of getting it wrong. Estimate the firm's likely equity issuance need over the next 3–5 years, look up the flotation cost for that issue size from the table, and multiply. For a small firm needing $2M, paying out cash today and re-raising it costs roughly 12.5% of the amount.
6. Present the alternative explicitly. "Why not buy back stock instead?" is Damodaran's standard rebuttal to the excess-cash argument, and the answer must be about stockholder preferences (see [[clientele-effect]]), not convenience.

**Reference data — cost of raising capital as a % of funds raised (Figure 10.12, approximate):**

| Size of issue | Cost of issuing bonds | Cost of issuing common stock |
|---|---|---|
| Under $1 mil | ~14% | ~22% |
| $1.0–1.9 mil | ~11% | ~17% |
| $2.0–4.9 mil | ~4% | ~12.5% |
| $5.0–9.9 mil | ~2.3% | ~8% |
| $10–19.9 mil | ~1.2% | ~6% |
| $20–49.9 mil | ~1.0% | ~4.6% |
| $50 mil and over | ~0.9% | ~3.5% |

Two rules from the table: equity flotation costs exceed bond flotation costs at every issue size, and costs fall steeply as issue size rises. Small firms pay a punitive price to re-raise equity, so they should be the most reluctant to pay out cash they may need.

**Worked example:** A small firm with a $2 million one-time cash windfall and no projects this year. It expects to need $2 million of external equity in two years for an expansion. Option A: pay a $2 million special dividend now and issue $2 million of stock in two years. Flotation cost on a $2.0–4.9 million equity issue ≈ 12.5%, so the firm must issue about $2.29 million of stock to net $2 million, costing shareholders roughly $286,000 — about 14% of the cash returned. Option B: hold the cash, or return it via a buyback only if the expansion does not materialize. The bird-in-the-hand argument would favor Option A on "certainty" grounds; the price-drop logic says the shareholders' $2 million dividend simply reduced the value of their shares by $2 million, and then cost them another $286,000 in flotation fees.

**Determinism:**
- DETERMINISTIC: the flotation cost lookup by issue size and security type. The present value of a permanent dividend increase, given ΔD, k_e and g. The ex-dividend drop ratio from market data.
- JUDGMENT: whether a cash surplus is one-time or recurring. Whether the firm will need external equity in the foreseeable future, and how much. Whether the investor base would accept a buyback in place of a dividend.

**Pitfalls:**
- Accepting "our investors want income" as a reason without checking whether the ex-dividend drop or the clientele evidence supports it.
- Turning a one-time surplus into a permanent dividend. Stickiness means the firm will keep paying it in the years when it cannot afford to (see [[dividend-empirical-facts]]).
- Comparing "dividends today" with "capital gains in five years". The right comparison is with price appreciation today.
- Ignoring flotation costs when recommending a payout at a small or capital-hungry firm. The cost table shows these can exceed 20% of funds raised.
- Assuming buybacks and dividends are equivalent. They are equivalent in cash terms and very different in commitment terms — that difference is the whole point of the excess-cash rebuttal.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.174-176

**Related:** [[ex-dividend-day-and-dividend-capture]], [[clientele-effect]], [[dividend-signaling]], [[cash-returned-dividends-and-buybacks]], [[dividend-empirical-facts]], [[three-schools-of-dividend-thought]]

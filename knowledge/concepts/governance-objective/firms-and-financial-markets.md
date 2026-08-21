# Firms and Financial Markets: Information, Efficiency and Short-Termism

**Core idea:** Stock price maximization needs two things from the information link. Managers must tell markets the truth, promptly. And markets must price that truth well. Both are contested. Managers suppress and delay bad news, spin what they do release, and in some cases commit outright fraud. Markets, critics say, are irrational, overreact or underreact, are manipulated by insiders, and are short-sighted. Damodaran takes the critiques seriously but answers the short-termism charge with hard counter-evidence. Markets pay high prices for young firms with no near-term earnings, they overvalue future growth relative to current earnings, and they reward R&D and capital-spending announcements. An analyst uses this concept to decide whether a given stock's price is a usable proxy for value.

**Formulas:** No arithmetic. The consequences of the efficiency assumption, and what breaks them:

```
IF markets are efficient AND managers inform honestly, THEN
  (a) a company investing in good LONG-TERM projects is rewarded
  (b) short-term accounting gimmicks do NOT increase market value
  (c) stock price performance IS a good measure of company performance

Failure mode A - Information management: negative information is
  suppressed or delayed while managers wait for a better moment.
  Released information is "spun" or "framed" to flatter the firm.
Failure mode B - Outright fraud: intentionally misleading information
  about current conditions and future prospects.
Failure mode C - Investor irrationality: prices move for no reason,
  and are far more volatile than fundamentals justify. Earnings and
  dividends are much less volatile than stock prices.
```

**Procedure:** Judging whether a stock price is a usable objective:
1. Check disclosure quality. Look for restatements, late filings, auditor changes, SEC enforcement actions, and material weaknesses.
2. Check bad-news timing. Tabulate the weekday and hour of the firm's negative announcements. Clustering on Friday afternoons is the classic tell.
3. Check the gap between GAAP earnings and cash flow, and between "adjusted" and reported earnings. A widening gap signals framing.
4. Check market quality for this stock: trading volume, bid-ask spread, analyst coverage, options market depth, free float.
5. Weigh the three irrationality critiques against the counter-evidence below.
6. Decide. If disclosure is poor or the market for the stock is thin, do not use stock price as the objective. Step back to stockholder wealth (see [[modified-objective-function]]).

**Reference data:**

*Do managers delay bad news? Average % change in EPS and DPS announced by weekday (approximate, read from chart):*

| Weekday | %Chg (EPS) | %Chg (DPS) |
|---|---|---|
| Monday | +3.5 | +6.5 |
| Tuesday | +1.7 | +7.3 |
| Wednesday | +3.5 | +7.0 |
| Thursday | +1.2 | +5.9 |
| **Friday** | **-4.8** | **-1.2** |

Announcements are positive Monday through Thursday and negative on Friday. Managers time bad news for Friday, when market attention is lowest.

*The three critiques of market efficiency:*
1. **Reaction to news.** Some believe investors overreact to news, good and bad. Others believe investors sometimes underreact to big news stories.
2. **An insider conspiracy.** Markets are manipulated by insiders, and prices bear no relation to value.
3. **Short-termism.** Investors are short-sighted and ignore the long-term implications of firm actions.

*Counter-evidence against short-termism (not conclusive, but pointing the other way):*
1. **Value of young firms.** Hundreds of start-ups and small firms with no earnings expected in the near future raise money on financial markets. A myopic market that cared only about short-term earnings would not attach high prices to them.
2. **Current earnings vs. future growth.** If anything, markets do not value current earnings and cash flows *enough*, and value future earnings and cash flows *too much*. Studies suggest low-PE stocks are underpriced relative to high-PE stocks.
3. **Market reaction to investments.** The market response to R&D and investment expenditures is generally positive.

*Market reaction to investment announcements — abnormal returns (approximate):*

| Announcement type | Announcement day | Announcement month |
|---|---|---|
| Joint venture formations | ~+0.4% | ~+1.5% |
| R&D expenditures | ~+0.2% | ~+1.5% |
| Product strategies | ~-0.1% | ~+0.3% |
| Capital expenditures | ~+0.2% | ~+1.4% |
| All announcements | ~+0.2% | ~+1.0% |

Day reactions are small but mostly positive. Month reactions are strongly positive for every category. On average, markets *reward* firms that announce long-term investments. That is the opposite of what a short-sighted market would do.

*The short-termism debate, as three propositions to argue over (no answer given in the source):*
1. Focusing on market prices will lead companies toward short-term decisions at the expense of long-term value.
2. Allowing managers to make decisions without worrying about the effect on market prices will lead to better long-term decisions.
3. Neither managers nor markets are trustworthy, so regulations and laws should force firms to make long-term decisions.

*Do market crises disprove markets?* Critics cite the September-December 2008 turmoil as proof that free markets are the problem. Two counters. First, 2008 showed how much we depend on functioning, liquid markets with risk-taking investors. No government, no bank, not even Buffett was big enough to step in and save the day. Second, the firms that caused the collapse — banks and investment banks — were among the most regulated businesses anywhere. Their failures trace to exploiting regulatory loopholes: badly designed insurance programs, and capital measurements that missed risky assets, especially derivatives.

*The market's counter-response to information games:*
- Analysts still issue more buy than sell recommendations. But the payoff to uncovering negative news is large enough that such news is eagerly sought and quickly revealed, at least to a limited group of investors.
- As investor access to information improves, firms find it much harder to control when and how information reaches markets.
- Option trading has become more common, so it is much easier to trade on bad news. In the process, the news is revealed to the rest of the market.
- When firms mislead markets, the punishment is not only quick but savage.

**Worked example:** Applying the Friday test. Suppose a firm made 12 negative pre-announcements over three years, and 9 of them landed after 4pm on a Friday. The base rate for a random weekday distribution would be about 2-3 of 12. That concentration is direct evidence of information management, and it should lower your confidence that the current stock price reflects everything management knows. Combine it with the aggregate evidence: EPS changes announced on Fridays average -4.8% versus +1.2% to +3.5% on other weekdays.

**Determinism:**
- DETERMINISTIC: tabulating announcement weekday/hour and comparing to a base rate (announcement dates -> Friday concentration); counting restatements and late filings; measuring bid-ask spread, volume, float and analyst coverage; the reference-table lookups above.
- JUDGMENT: whether markets are "efficient enough" for this stock — the source gives no threshold; whether a given disclosure was spin or reasonable framing; how much weight to give the short-termism critique versus the counter-evidence; whether an abnormal return reflects the announcement or something else.

**Pitfalls:**
- Treating market efficiency as all-or-nothing. The practical question is whether the price is a usable proxy, not whether it is perfect.
- Accepting short-termism as established. The source's counter-evidence points the other way, and the counter-evidence is explicitly labeled as not conclusive too.
- Using a crisis as proof that markets do not work. The 2008 failures came from the most regulated firms in the economy, exploiting regulatory loopholes.
- Assuming poor disclosure is punished slowly. When firms mislead markets, the punishment is quick and savage.
- Confusing volatility with inefficiency. Excess volatility is one critique, but it is a critique, not a proof.

**Sources:**
- corporate_finance--lecture_slides--cfpacket1spr20 p.35-40
- corporate_finance--lecture_slides--cfpacket1spr20 p.41-42
- corporate_finance--lecture_slides--cfpacket1spr20 p.70

**Related:** [[classical-objective-function-assumptions]], [[modified-objective-function]], [[self-correction-and-counter-forces]], [[governance-legislation-and-payoff]], [[market-efficiency]], [[pe-ratios]]

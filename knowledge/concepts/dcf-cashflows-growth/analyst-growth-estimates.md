# Analyst growth estimates: how much to trust them

**Core idea:** The second source of a growth rate is what sell-side analysts forecast. Their forecasts do beat naive time-series models — but only by small margins, and the advantage shrinks exactly where you need it most: at long horizons, for small companies, and at the company (rather than industry) level. The reason is structural: analysts spend nearly all their forecasting effort on the *next* earnings report, and the long-term (5-year) growth numbers are produced with far less analysis. Most of their private information comes from the company itself, which biases the forecasts optimistic and makes them highly correlated with each other. Consensus growth is a legitimate input, but it is one input, not an answer.

**Formulas:**
- No formula. The usable quantities are: consensus 5-year expected EPS growth; the dispersion (standard deviation) of individual estimates around the consensus; and the revision trend.
- Diagnostic rule of thumb: trust the consensus **least** when dispersion is either extremely low (herding — the estimates carry one piece of information, not many) or extremely high (the underlying information is too noisy to be useful).

**Procedure:**
1. Pull consensus long-term EPS growth from a service that aggregates them (Zacks, IBES/Refinitiv; coverage is good for US firms, patchier elsewhere).
2. Discount it by horizon. Analyst advantage over a time-series model is large for the next quarter and small-to-nil at five years.
3. Discount it by size and level. The advantage is greater for large firms than small ones, and greater at the industry level than at the company level. An industry-level analyst growth estimate is more useful than a single-company one.
4. Look at dispersion, not just the mean. Very tight agreement is a herding signal; very wide disagreement means the estimates carry no usable information.
5. Note that analyst growth is a growth rate in **EPS**, which embeds the firm's leverage and buyback policy. It is not a growth rate in operating income and cannot be dropped into an FCFF model.
6. Cross-check the consensus against fundamentals: does the implied `g = retention ratio × ROE` (or `reinvestment rate × ROC`) reproduce it? If the analyst number requires an ROE the firm has never earned, discard it.
7. Use it as one of three inputs alongside history and fundamentals, weighting fundamentals most heavily for long-horizon DCF work.

**Reference data:**

Analyst forecast error vs a time-series model (published studies):
| Study | Group tested | Analyst error | Time-series model error |
|---|---|---|---|
| Collins & Hopwood | Value Line forecasts | 31.7% | 34.1% |
| Brown & Rozeff | Value Line forecasts | 28.4% | 32.2% |
| Fried & Givoly | Earnings Forecaster | 16.4% | 19.8% |

Are star analysts better? Evidence on **All-America Analysts** (selected by *Institutional Investor*):
- No evidence they were chosen for forecasting skill: median forecast error in the quarter **before** selection was 30%, versus 28% for other analysts.
- In the calendar year **after** selection they do become slightly better — median error about 2% lower than other analysts.
- Their earnings revisions move stock prices much more than other analysts' revisions.
- Their recommendations move prices more (about 3% on buys, 4.7% on sells) and the moves continue in the following period (a further 2.4% for buys, 13.8% for sells).
- Interpretation: star status confers influence and better company access, rather than reflecting superior prior skill.

Three propositions about analyst growth rates:
1. Analyst forecasts contain far less private information and far more public information than is generally claimed.
2. The biggest source of private information is **the company itself** — which explains why buy recommendations outnumber sells (information bias plus the need to preserve access), why forecasts and revisions are highly correlated across analysts, and why All-America analysts improve *after* being chosen.
3. There is value in knowing the consensus, but danger both when analysts agree too much and when they agree too little.

The five behavioral failings to watch for in analyst output:
| Failing | What it looks like |
|---|---|
| Tunnel vision | So focused on the sector and within-sector comparisons that the bigger picture is lost |
| Lemmingitis | Urge to revise estimates and recommendations when other analysts do |
| Stockholm syndrome | Identifying with the managers of the firms covered |
| Factophobia | Basing recommendations on a story while refusing to face the facts |
| Dr. Jekyll / Mr. Hyde | Seeing the primary job as bringing in investment-banking business |

**Worked example:** A US large-cap with a consensus 5-year EPS growth estimate of 14.73% (this is the number used for Disney in the dividend regressions). Before using it: (a) it is EPS growth, so it embeds leverage and buybacks — it cannot be used as EBIT growth in an FCFF model; (b) check it against fundamentals — Disney's operating fundamentals implied `reinvestment rate 53.93% × ROC 12.61% = 6.8%` EBIT growth, less than half the analyst EPS number; (c) the gap is partly buybacks and leverage and partly optimism. In the Disney DCF, the **6.8% fundamental number** was used for the cash flows, not the 14.73% consensus.

**Determinism:**
- DETERMINISTIC: retrieving the consensus and computing its dispersion, revision history, and the gap versus a fundamentals-implied growth rate.
- JUDGMENT: essentially all of the use. How much weight to put on the consensus given horizon, firm size, dispersion and the analyst incentive structure; whether to convert an EPS growth forecast into an operating-income forecast; whether the consensus is anchored on company guidance.

**Pitfalls:**
- Dropping an analyst **EPS** growth rate into an operating-income (FCFF) model.
- Treating a 5-year consensus with the same confidence as a next-quarter estimate; the analytical effort behind them is not comparable.
- Reading tight consensus as confirmation. It usually means herding.
- Ignoring the source-preservation bias that skews recommendations toward buys.
- Assuming award-winning analysts are better forecasters — the evidence says they were not better before selection.
- Using analyst growth for long-horizon terminal-value work, where fundamentals must govern.

**Sources:**
- valpacket1spr21 p.160, p.168-173
- valpacket1spr20 p.157, p.165-170
- valpacket1spr21 p.196 / valpacket1spr20 p.193 (analyst estimates as a branch of the growth decision tree)
- cfpacket2spr20 p.223 (analyst 5-year EPS growth used as an input; contrast with p.247 fundamental growth)

**Related:** [[historical-growth]], [[fundamental-growth-equity]], [[fundamental-growth-operating]], [[value-of-growth]], [[dcf-model-choice-framework]], [[market-efficiency]]

# Difficult-company taxonomy (the four questions and where they break)

**Core idea:** Every valuation, easy or hard, answers exactly four questions: (1) What are the cash flows from existing assets? (2) What value is added by growth assets? (3) How risky are those cash flows? (4) When does the firm become mature, and what roadblocks stand in the way? Valuing a stable, profitable company with clean accounts, a long history and many comparables is easy because all four answers can be read off the data. A company is "difficult" — the dark side of valuation — exactly when one or more of those answers is missing, unstable, or mis-measured by accounting. Diagnosing *which* question breaks tells you which repair to apply, so this taxonomy is the routing table for every other concept in this area.

**Formulas:**
- The four questions, in equity form and firm form:
  - Q1 cash flows: equity = cash flows **after** debt payments (FCFE/dividends); firm = cash flows **before** debt payments (FCFF).
  - Q2 growth: equity = growth in equity earnings/cash flows; firm = growth in operating earnings/cash flows.
  - Q3 risk: equity = risk in the equity of the company (cost of equity); firm = risk in the firm's operations (cost of capital).
  - Q4 maturity: length of the excess-return/high-growth period and the roadblocks (failure, default, nationalization, regulatory shutdown) that can end it.
- Generic intrinsic value: Value = Σ_{t=1..n} CF_t / (1+r)^t + TV_n /(1+r)^n, with TV_n = CF_{n+1}/(r_stable − g_stable), r = cost of equity (equity view) or cost of capital (firm view).

**Procedure:**
1. Ask Q1–Q4 of the company and mark each answer as *available*, *unstable*, or *mis-measured*.
2. Classify the company along three axes:
   - **Life cycle** — young growth firm / mature firm in transition / declining-or-distressed firm.
   - **Market** — developed / emerging (structure, country-risk exposure, weak governance).
   - **Sector** — financial service / commodity-cyclical / intangible-heavy / ordinary.
   A firm can sit in several buckets at once (Boeing in March 2020 was mature + cyclical + distressed; Tata Steel is emerging + cyclical + cross-holding heavy).
3. Apply the repair that matches the broken question (table below). Never repair a cash-flow problem in the discount rate.
4. Check the three information sources a normal valuation leans on — current financial statements, the firm's own financial history, and industry/comparable-firm data. Young companies in young businesses have **none** of the three; that is the point of maximum temptation toward the dark side.
5. If two or more sources are missing, force yourself to state the mature end-state explicitly (target margin, terminal ROC, stable growth) and work backwards; see [[young-company-valuation]].

**Reference data:** Difficulty map and the repair each bucket needs.

| Bucket | Symptom in the four questions | Repair |
|---|---|---|
| Young growth firm | Q1 non-existent/negative cash flows; Q2 no history to base growth on; Q3 no usable market prices/betas; Q4 high failure propensity | Work backwards from a mature end-state; bottom-up beta; explicit failure probability — [[young-company-valuation]], [[distress-and-failure-adjusted-value]] |
| Mature firm in transition | Q1/Q2 rich history but policies may be "consistent, stable and bad"; Q3 leverage can change | Value status quo and optimally-run, weight by P(change) — [[value-of-control-and-restructuring]] |
| Declining / distressed | Q1 flat-to-falling revenues, sub-WACC returns; Q2 negative growth as assets are shed; Q4 real chance of not surviving | Negative growth and negative reinvestment; distress-weighted value — [[declining-firm-valuation]], [[distress-and-failure-adjusted-value]] |
| Emerging-market firm | Q1 inflation/interest-rate shifts and weak accounting distort earnings history; Q2 growth tied to the country; Q3 country risk moves; Q4 crises and nationalization; equity value distorted by cross holdings | Exposure-weighted country risk, currency consistency, value the holdings — [[country-risk-exposure]], [[currency-consistency-and-invariance]], [[cross-holdings]], [[truncation-and-political-risk]] |
| Financial service firm | Q1 assets are loans/financial assets, marked to market, earnings hide risk; Q2 capex and working capital undefinable, growth regulated; Q3 debt is raw material, not capital; Q4 regulatory capital ratios can force shutdown | Value equity directly: dividends, FCFE-to-regulatory-capital, or excess returns on book equity — [[financial-service-firm-valuation]], [[bank-fcfe-and-excess-return-models]] |
| Commodity / cyclical | Q1 volatile history; Q2 growth comes from the cycle or the commodity price, not from the firm; Q3 dormant macro risk; Q4 finite reserves or the next recession | Normalize, or drive revenues off the current market price, then simulate — [[normalized-earnings]], [[commodity-and-cyclical-valuation]], [[scenario-analysis-and-simulation]] |
| Intangible-heavy | Q1 capex miscoded as operating expense so earnings and capital invested are both wrong; Q2 reinvestment invisible; Q3 hard to borrow against intangibles; Q4 brand can last decades or vanish overnight | Capitalize R&D / recruiting / brand-building advertising — [[capitalizing-rd]] |

**Worked example:** Classification of the packet's own case studies. Amazon (Jan 2000): young + young business + intangible-ish → work backwards, target 10% retail margin, value per share $35.08 vs price $84. Hormel (2008): mature in transition → status quo $31.91 vs optimally run $37.80. JC Penney: declining + distressed → DCF $4,841m blended at 20% failure to $4,357m. Las Vegas Sands (Feb 2009): mature + distressed → $8.12 going concern, $1.92 after a 76.66% bond-implied distress probability. Tube Investments (2000): emerging + poorly governed → Rs 61.57 status quo vs Rs 111.3 with returns fixed. Deutsche Bank (Oct 2016): financial service + crisis → $22.97, $20.67 after a 10% wipeout probability. Amgen (May 2007): intangible-heavy → $42.73 unadjusted vs $74.33 with R&D capitalized. Shell (Mar 2016): commodity → $39.31 at a $40 oil price, simulated median $36.99.

**Determinism:** Everything here is JUDGMENT — the classification, and the decision about which question is broken. The only deterministic element is the generic present-value arithmetic once cash flows, growth and discount rates exist. The judgment needs: the company's filings and history, the sector's mature economics (margins, ROC, betas, sales-to-capital), the country's risk profile, and evidence about survival/regulatory constraints.

**Pitfalls:**
- Declaring a "paradigm shift", inventing new metrics, or letting the story run without numbers — the classic tells of a dark-side valuation when information runs out.
- Putting a cash-flow problem (failure risk, governance, distress) into the discount rate instead of into expected cash flows or into probability-weighted scenarios.
- Assuming that because a mature firm's policies are stable they are also good; stability can mask persistent over- or under-investment and the wrong financing mix.
- Treating one bucket at a time when a company sits in several — a distressed emerging-market bank needs three sets of repairs, not one.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.293-296
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.297-298
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.313-314
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.319
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.326
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.341
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.347
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.352
- valuations--lecture_notes--spring_2021--valpacket1spr21 p.362
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.284-287
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.288-289
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.304-305
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.310
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.316
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.332
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.338
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.343
- valuations--lecture_notes--spring_2020--valpacket1spr20 p.353

**Related:** [[young-company-valuation]], [[value-of-control-and-restructuring]], [[declining-firm-valuation]], [[distress-and-failure-adjusted-value]], [[country-risk-exposure]], [[financial-service-firm-valuation]], [[capitalizing-rd]], [[commodity-and-cyclical-valuation]], [[value-versus-price]], [[fcff-valuation]], [[terminal-value]], [[bottom-up-beta]]

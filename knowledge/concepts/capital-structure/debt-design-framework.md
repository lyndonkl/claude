# Designing debt: matching debt cash flows to asset cash flows

**Core idea:** The right *kind* of debt is the debt whose cash flows move with the cash flows of the assets being financed. Matching reduces default risk at any given debt level, which raises debt capacity, which raises firm value. A firm whose value swings cyclically while its debt payments stay flat will dip below the value of its debt in downturns and default for purely structural reasons. Match the debt — same duration, same currency, same sensitivity to inflation and to the business cycle — and the value of the debt moves with the firm, so the firm never becomes technically insolvent in a downturn. Damodaran's design pipeline runs in six stages: profile the asset cash flows, set the debt characteristics, overlay tax preferences, consider ratings agency and analyst concerns, factor in bondholder agency conflicts, and finally allow for information asymmetry.

**Formulas:** No single equation. The quantitative inputs come from [[project-duration-and-project-financing]] (duration of assets) and [[macro-sensitivity-regressions]] (interest rate, GDP, currency and inflation sensitivities).

**Procedure (the six stages):**
1. **Start with the cash flows on assets/projects.** Characterize duration, currency, effect of inflation, uncertainty about the future, growth patterns, cyclicality, and any other systematic driver. Three ways to do it: (I) the intuitive approach — ask whether projects are long or short term, what the cash flow pattern is, how much growth potential exists relative to current projects, how cyclical cash flows are, and what specific factors drive them; (II) the project cash flow approach — estimate expected cash flows on a typical project, then run scenario analyses under different macro scenarios; (III) the historical data approach — infer the traits from the firm's own history of operating cash flows and firm value.
2. **Define debt characteristics.** Duration of assets → maturity of debt. Currency of cash flows → currency mix of debt. Cash flows that move with inflation, or high uncertainty about the future → more floating rate debt. Low current cash flows with high expected growth → convertible rather than straight debt. Special exposures → special features that make debt cash flows track asset cash flows (commodity bonds, catastrophe notes).
3. **Overlay tax preferences.** All the matching work is wasted if the security does not actually deliver the tax deduction. Check deductibility under the relevant code and exploit differences in tax rates across locales. If the tax advantage is large enough it can override the matching design (example instrument: zero coupon bonds).
4. **Keep analysts, ratings agencies and regulators applauding.** Analysts care about the EPS effect and value relative to comparables, and dislike equity issues that dilute EPS. Ratings agencies care about ratio effects and prefer equity. Regulators care about the (usually book-value) measures they use. A security that satisfies all three is "nirvana" (examples: operating leases, MIPs, surplus notes).
5. **Soothe bondholder fears.** Some firms face bondholder skepticism — a history of defaults or other actions against bondholders, or simply being small with no borrowing history. Such firms pay much higher rates. Consider: how observable are the firm's cash flows to lenders (less observable → more conflict), what kind of assets are being financed (tangible and liquid assets create fewer agency problems), and what existing covenants restrict. If agency problems are substantial, issue convertible bonds (or puttable bonds, rating-sensitive notes, LYONs).
6. **Consider information asymmetries.** With more uncertainty about future cash flows, short-term debt may be better. Firms with credibility problems will issue more short-term debt.
7. **Do not lock in market mistakes.** If the stock is under-priced, issuing equity or equity-linked products transfers wealth from existing to new stockholders. If the firm is under-rated, issuing long-term debt locks in a rate far above its true default risk. When you must finance while mispriced, use short-term or delayed structures until the mistake corrects.
8. **Compare design to actual.** Tabulate the firm's existing debt on the same dimensions (maturity, currency mix, fixed vs floating, convertible or not) and identify the gaps.
9. **Close the gap.** Swap existing fixed-rate domestic debt into the recommended structure, and issue new debt in the recommended form. Even if new debt mismatches the specific new investment, firm-level matching improves.

**Reference data:** The intuitive approach applied to Disney's five businesses:

| Business | Project cash flow characteristics | Type of financing |
|---|---|---|
| Studio entertainment | Movie projects short-term; outflows mostly in dollars but inflows have a large foreign-currency component; net cash flows driven by whether the movie is a hit, which is hard to predict | Short-term, mixed-currency debt reflecting audience make-up, if possible tied to the success of movies |
| Media networks | Short-term projects; primarily dollars though the foreign component is growing (especially ESPN); driven by advertising revenue and ratings | Short-term, primarily dollar debt, if possible linked to network ratings |
| Park resorts | Very long-term projects; currency depends on the region where the park sits; affected by the studio and media businesses | Long-term, mix of currencies based on the tourist make-up at the park |
| Consumer products | Short- to medium-term, linked to the movie division since offerings and licensing derive from film | Medium-term dollar debt |
| Interactive | Short-term, high growth potential, significant risk; cash flows initially in US dollars with the mix shifting as the business ages | Short-term, convertible, US dollar debt |

Trust preferred, as a design curiosity: it carries a fixed dividend set at issue, that payment is tax deductible like interest, and failure to pay can give holders voting rights. When first created, ratings agencies counted it as equity — a tax deduction plus equity credit. Agencies have since become more savvy and now grant only partial equity credit. The firm that gains most from such quasi-equity is an *under-levered firm with a rating constraint* that moving to its optimal would violate: it captures debt-like tax benefits while preserving the rating.

**Worked example:** Disney's debt versus its recommended design (2013). Recommended: duration about 4.3 years, a significant floating rate component (Disney has pricing power and its operating income rises with interest rates), and roughly 18% of debt in foreign currencies based on where revenues are earned. Actual: $14.3 billion of interest-bearing debt with a face-value weighted average maturity of 7.92 years, only 5.49% in non-dollar currencies (Indian rupees and Hong Kong dollars, no euro debt), 5.67% floating rate, and no convertible debt. Verdict: maturity slightly too long (maturity exceeds duration, but not by much), too little foreign currency debt (euro debt should rise to about 12%), and too little floating rate debt given Disney's pricing power. The 2013 mix may reflect a desire to lock in low long-term rates. Fixes: swap fixed-rate dollar debt into floating-rate foreign-currency debt (easy given Disney's market standing), and use floating-rate foreign-currency debt for new issues.

Three more applications:
- *Bookscape*: revenues depend on a single New York bookstore. Recommendation: long-term, dollar-denominated, fixed rate debt. Actual: a long-term operating lease on the store — a good match.
- *Vale*: mines worldwide with very long lives and large up-front investments; 37% of revenues from China; costs in local currencies, revenues in US dollars. Recommendation: long-term dollar debt, hedge local-currency cost exposure, and if possible tie payments to commodity prices. Actual: 65.48% US dollar debt, average maturity 14.70 years, all fixed rate, no commodity-linked debt.
- *Tata Motors*: manufacturer with about 24% of revenues each from India and China, the rest across developed markets. Recommendation: medium- to long-term fixed rate debt in a currency mix reflecting operations. Actual: about 71% rupee and 29% euro debt, average maturity 5.33 years, almost entirely fixed rate.
- *Baidu*: young technology company with little debt. Recommendation: convertible, Chinese yuan debt. Actual: about 82% of debt in US dollars and euros, average maturity 5.80 years, a small floating portion, very little convertible — a poor match on every dimension.

**Determinism:**
- DETERMINISTIC: computing the firm's existing debt profile (weighted average maturity, currency shares, fixed/floating split, convertible share); the duration and sensitivity inputs that feed the design.
- JUDGMENT: essentially the whole design. Mapping asset characteristics to debt features, deciding when a tax advantage should override matching, judging how analysts and agencies will react, sizing agency conflicts with bondholders, and deciding whether the firm's securities are currently mispriced.

**Pitfalls:**
- Designing perfectly matched debt that is not tax-deductible, which throws away the main benefit of borrowing.
- Locking in a market mistake — issuing long-term debt while under-rated, or equity while under-priced.
- Financing project by project when projects are numerous and interdependent ([[project-duration-and-project-financing]]).
- Chasing analyst-friendly structures that ratings agencies will see through. Agencies now give trust preferred only partial equity credit.
- Treating the design question as secondary to the mix question. Matching raises debt capacity, so it feeds back into the optimal ratio.
- Assuming an operating lease is not debt just because it sits off the balance sheet.

**Sources:**
- corporate_finance--lecture_slides--cfpacket2spr20 p.110-120
- corporate_finance--lecture_slides--cfpacket2spr20 p.121-123
- corporate_finance--lecture_slides--cfpacket2spr20 p.143-147

**Related:** [[project-duration-and-project-financing]], [[macro-sensitivity-regressions]], [[debt-vs-equity-choices]], [[cost-of-capital-approach]], [[moving-to-the-optimal]], [[downside-risk-and-rating-constraints]], [[financial-firm-capital-structure]]

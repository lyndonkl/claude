# Auction Winner's-Curse Haircut Methodology

Experimental basis, formal Bayesian derivation, and classification heuristics for the `auction-winners-curse-haircut` skill.

## Table of Contents
- [Intuition](#intuition)
- [Experimental Evidence -- Kagel and Levin](#experimental-evidence--kagel-and-levin)
- [Formal Bayesian Derivation](#formal-bayesian-derivation)
- [Haircut Formula Derivation](#haircut-formula-derivation)
- [Why Private-Value Gets Zero Haircut](#why-private-value-gets-zero-haircut)
- [Classifying Value Type in Fantasy Contexts](#classifying-value-type-in-fantasy-contexts)
- [Relationship to First-Price Bid Shading](#relationship-to-first-price-bid-shading)
- [Limitations and Open Issues](#limitations-and-open-issues)
- [References](#references)

---

## Intuition

In a common-value auction, the item being auctioned has the same true value V for every bidder, but each bidder i observes a noisy signal s_i = V + epsilon_i of that true value. Bidders translate signals into bids.

Consider a naive bidder who bids their signal: `bid_i = s_i`. The auction is won by the bidder with the highest signal. But the expected value of the highest signal among N draws is above the mean of the signal distribution. So **conditional on winning, the winner's signal was probably above V**, which means their bid was probably above V, which means they will lose money in expectation.

This is the **winner's curse**: winning is itself Bayesian evidence that you over-estimated. A rational bidder must *pre-emptively shade down* their valuation to account for the information they will receive only at the moment of winning.

Three drivers determine how severe the adverse selection is:
1. **N, the number of informed bidders** -- more competitors means the highest signal is further above the mean (order-statistic effect).
2. **Signal dispersion** -- wider spread of signals means the gap between the max and the mean is larger in absolute terms.
3. **Private vs common value** -- if the target's true value is private (different for each bidder), the order-statistic logic does not apply: winning does not tell you anything about their signals because their signals were about different objects.

---

## Experimental Evidence -- Kagel and Levin

The winner's-curse phenomenon has been extensively documented in laboratory auction experiments, most systematically by John Kagel and Dan Levin.

**Key findings from the Kagel-Levin literature:**

1. **Common-value auctions consistently produce losses for naive bidders.** Across many experimental treatments, naive bidders who bid their signal pay roughly 15-30% above true value and earn negative expected profits.
2. **Severity grows with N.** Experimental treatments with 3-4 bidders show modest over-bidding; treatments with 6-10 bidders show severe over-bidding.
3. **Experienced bidders shade, but imperfectly.** Even experienced subjects typically under-correct by about 5-10 percentage points relative to Nash-equilibrium predictions.
4. **Private-value treatments do NOT produce the same pattern.** When the experimental design uses private values (each subject's value is drawn independently), the winner's curse disappears, as theory predicts.

**The 15-30% empirical range** used in this skill's haircut formula is drawn from the consistent headline finding across these studies: naive bidders over-pay by 15-30% in common-value settings. The skill's formula is calibrated to land in this range for typical inputs (N in [3, 10], dispersion in [20, 60]).

See [References](#references) for primary citations.

---

## Formal Bayesian Derivation

Sketch of the posterior on V given both the bidder's own signal and the event "I won."

**Setup**:
- True value V (unknown).
- Bidder i observes signal s_i = V + epsilon_i, where epsilon_i is mean-zero noise with variance sigma^2.
- There are N informed bidders total.
- Auction awards the item to the highest bidder.

**Prior and likelihood**:

Treat V with a non-informative prior (or a wide Gaussian centered at bidder's signal). The likelihood of bidder i observing s_i given V is N(V, sigma^2).

**Unconditional posterior (your signal only)**:

E[V | s_i] = s_i (under non-informative prior).

**Conditional on winning**:

Let W be the event "my bid was highest." Under symmetric bidding strategies, winning is (approximately) the event "my signal was the max of N draws from N(V, sigma^2)."

The expected value of the maximum of N i.i.d. draws from a standard normal is approximately:
```
E[max of N] ~ sigma * sqrt(2 * log(N))    (for large N)
```

So:
```
E[s_i | s_i = max of N, V]  ~  V + sigma * sqrt(2 * log(N))
```

Inverting for the posterior on V:
```
E[V | s_i, winning]  ~  s_i - sigma * sqrt(2 * log(N))
```

**The haircut** (as a fraction of s_i) is therefore approximately:
```
haircut_fraction  ~  sigma * sqrt(2 * log(N)) / s_i
                 =  (sigma / s_i) * sqrt(2 * log(N))
```

- `sigma / s_i` is the coefficient of variation of the signal -- a normalized dispersion.
- `sqrt(2 * log(N))` is the order-statistic factor, growing (slowly) with N.

This is the formal motivation for using **log(N)** and a **dispersion term** as the two drivers in the practical formula.

---

## Haircut Formula Derivation

The skill's formula is a piecewise-linear approximation of the Bayesian result, calibrated to the Kagel-Levin empirical range:

```
haircut_pct = min(35, 10 + log(N) x 5 + signal_dispersion x 0.2)
```

**Term-by-term justification**:

| Term | Value at default | Role |
|------|------------------|------|
| `10` (intercept) | 10 | Baseline adverse-selection discount even at N=1 and dispersion=0. Reflects residual uncertainty even in thin-information auctions. Calibrated so N=2, dispersion=0 yields ~13.5%, matching low-end Kagel-Levin observations. |
| `log(N) x 5` | 0-12 for N in [1, 12] | Order-statistic effect. `log(N)` grows slowly, mimicking the `sqrt(2 log N)` Bayesian term in a form that is easier to reason about. Coefficient 5 calibrates the high end: at N=10, this term contributes ~11.5 percentage points. |
| `signal_dispersion x 0.2` | 0-20 for dispersion in [0, 100] | Scales the haircut with how much bidder estimates actually disagree. When dispersion is low, bidders have similar info and the winner's curse is mild; when high, it is severe. Coefficient 0.2 keeps the term bounded by 20. |
| `min(35, ...)` | Caps at 35 | Prevents the formula from exceeding empirically observed discounts even at extreme inputs. Empirical upper bound is ~30%; 35% provides a small margin. |

**Calibration anchors** (common-value, for sanity-checking):

- N=1, dispersion=0 -> 10% (minimum)
- N=6, dispersion=40 -> ~27% (center of empirical range)
- N=12, dispersion=100 -> 35% (hard cap)

---

## Why Private-Value Gets Zero Haircut

The short-circuit `haircut_pct = 0` when `value_type == "private_value"` is not a pragmatic approximation -- it is the mathematically correct answer.

**Argument**: In a pure private-value auction, each bidder i has a value V_i drawn independently from some distribution. Winning the auction means `bid_i > bid_j for all j != i`. Under equilibrium bidding, this is equivalent to `V_i > V_j for all j != i`. But this does not update your belief about your own V_i -- you knew V_i directly. The information revealed by winning is about the other bidders' valuations, which are irrelevant to your own value.

**Contrast with common value**: In common-value auctions, all bidders' valuations are estimates of the *same* underlying quantity V. Winning reveals information about the *other bidders' estimates of V*, which updates your estimate of V. That is the mechanism the haircut corrects for.

**Operational implication**: If the caller can defend a private-value claim -- "no other bidder values this target the way I do, because of [structural reason]" -- then the winner's curse logic does not apply and no haircut is warranted. This is why the skill requires an explicit classification and short-circuits aggressively when private-value is asserted.

**Watch for misclassification**: Bidders sometimes rationalize a common-value target as private-value ("I need this position!") to avoid the haircut. The test is whether the private component is *structural* (others really do not value the target similarly) or *motivational* (you want it more, but others would also value it similarly). Only structural private-value justifies zero haircut.

---

## Classifying Value Type in Fantasy Contexts

Concrete heuristics for the FAAB use case, since that was the originating context.

### COMMON_VALUE indicators

- Target is named and widely reported (headline call-up, beat-writer-confirmed closer change, top-100 prospect).
- Public projection systems (ATC, Steamer, THE BAT) are within ~15% of each other on rest-of-season value.
- League-wide positional need is broad (e.g., every team can use a closer for SV).
- Bid history in the league shows similar recent targets going for similar dollar amounts.

### PRIVATE_VALUE indicators

- Target's value depends on a roster feature only this team has (handcuff to a reliever you own, platoon fit for a specific lineup slot).
- Target helps a punted category or specific strategic orientation that is asymmetrically valuable to you.
- Other teams' bid history shows no interest in similar complementary pieces.
- Positional need: only 1-2 teams realistically have space and fit.

### MIXED indicators

- Public projection base is shared (common core) but this team has a specific short-term need (category urgency, matchup-week demand).
- Late-season claim on a previously-owned player -- ROS projections similar, but contending teams have extra private-value from the playoff window.
- Keeper-league targets where everyone agrees on the base but some teams have specific roster construction needs.

**Fantasy-specific rules of thumb**:

- FAAB closer-chase claims: almost always `common_value` (and often N=6-8).
- Handcuff closer without current role: almost always `private_value`.
- Streaming SP for a specific two-start week: usually `mixed` with ~60% common (the pitcher has a common ROS value) and ~40% private (the two-start matchup and your category state).
- DL-return hitter: `common_value` (public information that they are back).
- Mid-season power-reliever ownership grab in a punt-SV build: `private_value` for the punt-SV bidder; `common_value` for everyone else.

### Cross-domain notes

- **Prediction markets**: Almost always `common_value`. The outcome is shared by definition.
- **M&A bids**: Typically `mixed`. The target's cash flows are a common-value core; strategic fit is the private increment. Weight depends on how much the acquirer expects from synergies.
- **Ad-auction keywords**: Usually `mixed`. The keyword's common conversion-rate base is shared; bidder-specific funnel quality is private.
- **Real estate**: Usually `mixed`. Market-comp common base plus buyer-specific use (adjacency, tenant in place).

---

## Relationship to First-Price Bid Shading

The winner's-curse haircut is **distinct from** the first-price bid-shading adjustment that appears in sibling skills like `auction-first-price-shading`.

| Correction | Phenomenon | When to apply |
|------------|-----------|---------------|
| Winner's-curse haircut | Bayesian update: winning reveals I over-estimated | Applied to *valuation*, before bidding |
| First-price bid shading | Strategic: bidding true value yields zero surplus in first-price auction | Applied to *bid*, after valuation |

Both should be applied in sequence when both apply:
1. Start with `raw_valuation`.
2. Apply winner's-curse haircut -> `adjusted_valuation`.
3. Apply strategic shading (e.g., `(N-1)/N`) -> `final_bid`.

Never apply either correction twice. In particular, some frameworks fold the winner's curse into the shading factor; if you use such a framework, do not additionally apply this haircut.

---

## Limitations and Open Issues

1. **Formula is a calibrated approximation, not a closed-form Bayesian posterior.** The exact posterior depends on the prior distribution on V, the noise distribution, and the bidding strategies of other participants. The skill's formula is a practical proxy that lands in the right empirical range.

2. **Signal dispersion is rarely directly observable.** Callers estimate it from indirect evidence (spread across projection systems, public bid history, market depth). Document the basis.

3. **N is the number of *informed* bidders.** Uninformed bidders (flat priors, random bids) do not contribute to adverse selection. Counting total auction participants overestimates N.

4. **Mixed-value interpolation is linear.** The 60/40 default is a pragmatic choice and can be overridden. There is no theoretical result saying the true mixed haircut is a linear combination of pure common and pure private -- but it is a reasonable first-order approximation and avoids the need for more complex modeling.

5. **Dynamic auctions (English, Dutch) differ.** The Kagel-Levin estimates cited are primarily from sealed-bid first-price and second-price settings. Applying this haircut to open-outcry auctions requires additional care because bidders update in real time from observed competing bids.

---

## References

**Primary experimental work:**

- Kagel, John H., and Dan Levin. *Common Value Auctions and the Winner's Curse*. Princeton University Press, 2002. Comprehensive book-length treatment of the experimental literature; the 15-30% over-payment range is a central finding.
- Kagel, John H., and Dan Levin. "The Winner's Curse and Public Information in Common Value Auctions." *American Economic Review* 76, no. 5 (1986): 894-920. Foundational experimental paper.
- Kagel, John H., Ronald M. Harstad, and Dan Levin. "Information Impact and Allocation Rules in Auctions with Affiliated Private Values: A Laboratory Study." *Econometrica* 55, no. 6 (1987): 1275-1304.

**Theoretical foundations:**

- Wilson, Robert B. "A Bidding Model of Perfect Competition." *Review of Economic Studies* 44, no. 3 (1977): 511-518. Early formal treatment of common-value bidding.
- Milgrom, Paul R., and Robert J. Weber. "A Theory of Auctions and Competitive Bidding." *Econometrica* 50, no. 5 (1982): 1089-1122. General framework linking common-value and private-value auctions.
- Klemperer, Paul. "Auction Theory: A Guide to the Literature." *Journal of Economic Surveys* 13, no. 3 (1999): 227-286. Accessible survey including winner's-curse treatment.

**Field applications:**

- Capen, Edward C., Robert V. Clapp, and William M. Campbell. "Competitive Bidding in High-Risk Situations." *Journal of Petroleum Technology* 23, no. 6 (1971): 641-653. The original coinage of "winner's curse" in the context of oil-lease auctions.
- Thaler, Richard H. "Anomalies: The Winner's Curse." *Journal of Economic Perspectives* 2, no. 1 (1988): 191-202. Readable survey of winner's-curse evidence across domains (oil leases, book rights, corporate takeovers, free-agent baseball).

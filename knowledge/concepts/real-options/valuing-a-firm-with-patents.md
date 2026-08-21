# Valuing a firm with patents (sum of the parts)

**Core idea:** A firm holding a substantial number of patents cannot be valued with a single DCF, because much of its value sits in products it has not yet developed. Damodaran decomposes it into three parts: commercial products already selling (DCF), existing patents not yet developed (option pricing), and the excess value the firm's future R&D will create. The third term measures how efficiently the firm converts research dollars into commercial products. If the firm merely earns its cost of capital on research, that term is zero. The decomposition is also a discipline against double counting: value the patents as options *or* build their growth into the DCF, never both.

**Formulas:**
- `Value of Firm = Value of commercial products (DCF) + Value of existing patents (option pricing) + (Value of new patents to be obtained in the future - Cost of obtaining these patents)`
- Third term, year by year over a competitive-advantage window of `N` years:
  - `R&D_t = R&D_0 x (1 + g)^t`
  - `Patent value created_t = m x R&D_t`, where `m` = dollars of patent value created per dollar of R&D
  - `Excess value_t = Patent value_t - R&D_t = (m - 1) x R&D_t`
  - `PV of future R&D value = sum over t = 1..N of [Excess value_t / (1 + k)^t]`
- Symbols: `R&D_0` = current annual R&D spend; `g` = R&D growth rate during the window; `m` = value-creation multiple; `k` = cost of capital for the R&D component; `N` = years of competitive advantage. After year `N`, `m = 1.0` (research breaks even) and the term contributes nothing.
- Annuity PV for contractually guaranteed cash flows: `PV = CF x (1 - (1 + r)^(-n)) / r`.
- `Value per share = Equity value / shares outstanding`. With no debt, equity value = firm value.

**Procedure:**
1. Separate the firm's assets into three buckets: commercial products in market; patents granted but not yet developed; and the R&D engine that will produce future patents.
2. Value commercial products with a DCF. Match the discount rate to the risk of those specific cash flows. Contractually guaranteed cash flows (licence fees from creditworthy counterparties) are discounted at the **guarantor's pre-tax cost of debt**, not the firm's cost of capital.
3. Value each existing undeveloped patent as a call option using [[patent-valuation-as-option]]. Sum them.
4. Value future R&D. Set the current R&D spend, its growth rate, the number of years the firm can sustain a value-creation multiple above 1.0, the size of that multiple, and a discount rate reflecting the riskiness of research.
5. Compute excess value per year as `(m - 1) x R&D_t` and discount at `k`. Stop at the end of the competitive-advantage window — beyond it, assume `m = 1.0` and add nothing.
6. Sum the three components to get firm value. Subtract debt to get equity, then divide by shares.
7. Audit for double counting. If a patent is valued as an option in bucket 2, its future product revenues must not appear as growth in bucket 1's DCF.

**Reference data:**

Biogen future-R&D schedule. Base R&D $100 million, growing 20% per year, value multiple `m` = 1.25, discount rate 15%, 10-year window. All figures in $ millions.

| Yr | Value of Patents | R&D Cost | Excess Value | PV (at 15%) |
|---|---|---|---|---|
| 1 | 150.00 | 120.00 | 30.00 | 26.09 |
| 2 | 180.00 | 144.00 | 36.00 | 27.22 |
| 3 | 216.00 | 172.80 | 43.20 | 28.40 |
| 4 | 259.20 | 207.36 | 51.84 | 29.64 |
| 5 | 311.04 | 248.83 | 62.21 | 30.93 |
| 6 | 373.25 | 298.60 | 74.65 | 32.27 |
| 7 | 447.90 | 358.32 | 89.58 | 33.68 |
| 8 | 537.48 | 429.98 | 107.50 | 35.14 |
| 9 | 644.97 | 515.98 | 128.99 | 36.67 |
| 10 | 773.97 | 619.17 | 154.79 | 38.26 |
| **Total** | | | | **318.30** |

**Worked example:** Biogen, valued as the sum of three parts.

*Bucket 1 — existing commercial products.* Two products (a Hepatitis B drug and Intron) licensed to other pharmaceutical firms, generating $50 million after-tax per year for 12 years. Because the licence fees were contractually guaranteed, they were discounted at the guarantors' pre-tax cost of debt of 7%, not at a risky cost of capital.
`PV = 50 x (1 - 1.07^(-12)) / 0.07 = $397.13 million`.

*Bucket 2 — existing patents.* The Avonex patent, valued as a dividend-adjusted call: **$907 million**. See [[patent-valuation-as-option]].

*Bucket 3 — future R&D.* Biogen spent about $100 million a year on R&D, expected to grow 20% per year for 10 years and 5% thereafter. Assumption: for the next 10 years every dollar invested in research creates $1.25 of patent value. After year 10 research breaks even at $1 of patent value per $1 of R&D, so no excess value. Discount rate 15%, reflecting the riskiness of this component. Sum of PVs = **$318.30 million**.

*Total.* `397.13 + 907 + 318.30 = $1,622.43 million`. Biogen had no debt, so equity value equals firm value. With 35.50 million shares: `1,622.43 / 35.5 = $45.70 per share`.

**Determinism:** **DETERMINISTIC**: the annuity PV ($397.13 million from `CF` = 50, `r` = 7%, `n` = 12); the entire future-R&D table (given `R&D_0` = 100, `g` = 20%, `m` = 1.25, `k` = 15%, `N` = 10, a script returns $318.30 million); the three-way summation; the per-share division. **JUDGMENT**: the value-creation multiple `m` = 1.25 — this is a claim about how good the firm's research is, and it drives the whole third bucket. The length of the competitive-advantage window (10 years) and the assumption that research breaks even after it. The R&D growth rate. The 15% discount rate for the research component. Which cash flows qualify as contractually guaranteed and therefore earn the guarantor's cost of debt. And the bucket boundaries themselves — deciding what belongs in the DCF versus the option bucket is the double-counting judgment.

**Pitfalls:**
- Double counting. This is the warning Damodaran attaches directly to the formula. Valuing patents as options while also assuming a high growth rate in the DCF of existing products counts the same product twice.
- Letting the future-R&D term run forever. If the firm earns exactly its cost of capital on research, `m` = 1.0 and the term is zero. Excess value requires a sustainable competitive advantage, and it should be truncated when that advantage ends.
- Discounting contractually guaranteed licence fees at the firm's cost of capital. That understates their value; use the guarantor's pre-tax cost of debt.
- Applying the same discount rate to all three buckets. Existing licence income (7%), patent options (riskless rate inside the option model), and future R&D (15%) carry very different risks.
- Forgetting to subtract debt before dividing by shares. Biogen happened to have none.

**Sources:**
- valuations--lecture_notes--spring_2021--valpacket3spr21 p.32-36
- valuations--lecture_notes--spring_2020--valpacket3spr20 p.32-36

**Related:** [[patent-valuation-as-option]], [[option-to-delay]], [[real-options-framework]], [[natural-resource-options]], [[dcf-valuation]], [[excess-returns-and-value-creation]], [[value-per-share]]

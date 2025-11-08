# Financial Unit Economics Templates

Quick-start templates for calculating CAC, LTV, contribution margin, and cohort analysis.

## Unit Definition Template

**Business model**: [Subscription / Transactional / Marketplace / Freemium / Enterprise]

**Unit of analysis**: [What are you measuring?]
- Customer (entire relationship)
- Subscription (per subscription period)
- Transaction (per purchase)
- Product SKU (per product sold)
- User (active user)

**Time period**: [Monthly / Quarterly / Annual cohorts]

**Segments** (if analyzing by segment):
- [ ] Acquisition channel (paid search, organic, referral, etc.)
- [ ] Customer type (B2B vs B2C, SMB vs Enterprise)
- [ ] Geography (US, EU, APAC)
- [ ] Product tier (Free, Pro, Enterprise)

---

## CAC Calculation Template

**Customer Acquisition Cost (CAC)** = Total acquisition costs ÷ New customers acquired

### Fully-Loaded CAC

**Sales & Marketing Costs** (period: [Month/Quarter/Year])

| Cost Category | Amount | Notes |
|---------------|--------|-------|
| **Marketing spend** | $[X] | Paid ads, content marketing, events, tools |
| **Sales team salaries** | $[X] | Base + commission + benefits |
| **Sales tools & software** | $[X] | CRM, sales engagement, analytics |
| **Marketing team salaries** | $[X] | Marketers, designers, contractors |
| **Overhead allocation** | $[X] | % of office, admin costs attributable to S&M |
| **Other** | $[X] | [Specify] |
| **Total S&M Cost** | **$[X]** | Sum of above |

**New customers acquired** (same period): [N]

**CAC = $[Total Cost] ÷ [N customers] = $[CAC per customer]**

### CAC by Channel

Break down CAC by acquisition channel to identify most/least efficient channels.

| Channel | S&M Spend | New Customers | CAC | Notes |
|---------|-----------|---------------|-----|-------|
| Paid Search | $[X] | [N] | $[X/N] | [Google Ads, Bing] |
| Paid Social | $[X] | [N] | $[X/N] | [Facebook, LinkedIn, etc.] |
| Content/SEO | $[X] | [N] | $[X/N] | [Organic, blog, SEO tools] |
| Referral | $[X] | [N] | $[X/N] | [Referral program costs] |
| Direct | $[X] | [N] | $[X/N] | [Type-in, brand awareness] |
| Other | $[X] | [N] | $[X/N] | [Specify] |
| **Total** | **$[X]** | **[N]** | **$[Blended CAC]** | Fully-loaded blended CAC |

**Insight**: [Which channels are most/least efficient? Where to increase/decrease spend?]

---

## LTV Calculation Template

**Lifetime Value (LTV)** = Revenue over customer lifetime × Gross margin %

Choose calculation method based on business model:

### LTV (Subscription Model)

```
LTV = ARPU × Gross Margin % ÷ Monthly Churn Rate
```

**Inputs**:
- **ARPU** (Average Revenue Per User): $[X]/month
- **Gross Margin %**: [X]% (Revenue - COGS) ÷ Revenue
- **Monthly Churn Rate**: [X]% (customers lost ÷ starting customers)

**Calculation**:
- **Customer Lifetime** = 1 ÷ Churn Rate = 1 ÷ [X]% = [Y] months
- **LTV** = $[ARPU] × [Y months] × [Gross Margin %] = **$[LTV]**

### LTV (Transactional Model)

```
LTV = AOV × Purchase Frequency × Gross Margin % × Customer Lifetime (years)
```

**Inputs**:
- **AOV** (Average Order Value): $[X] per transaction
- **Purchase Frequency**: [Y] purchases/year
- **Gross Margin %**: [Z]%
- **Customer Lifetime**: [N] years

**Calculation**:
- **Annual Revenue per Customer** = $[AOV] × [Frequency] = $[X]/year
- **LTV** = $[Annual Revenue] × [Lifetime years] × [Gross Margin %] = **$[LTV]**

### LTV (Marketplace / Platform)

```
LTV = GMV per user × Take Rate × Gross Margin % ÷ Churn Rate
```

**Inputs**:
- **GMV per user** (monthly): $[X]
- **Take Rate**: [Y]% (platform's % of GMV)
- **Gross Margin %**: [Z]% (after variable costs)
- **Monthly Churn Rate**: [C]%

**Calculation**:
- **Monthly Revenue per User** = $[GMV] × [Take Rate] = $[X]/month
- **Customer Lifetime** = 1 ÷ [Churn] = [Y] months
- **LTV** = $[Monthly Rev] × [Lifetime] × [Gross Margin %] = **$[LTV]**

### LTV by Cohort (Observed Retention)

More accurate: Use actual retention data from cohorts.

**Example Cohort Retention Table** (% of customers remaining):

| Month | Cohort Jan | Cohort Feb | Cohort Mar | Average |
|-------|------------|------------|------------|---------|
| 0 | 100% | 100% | 100% | 100% |
| 1 | 95% | 94% | 96% | 95% |
| 2 | 88% | 86% | 89% | 88% |
| 3 | 80% | 78% | 82% | 80% |
| 6 | 65% | 62% | - | 64% |
| 12 | 45% | - | - | 45% |

**LTV Calculation**:
- Sum: Month 0 revenue + (Month 1 retention × revenue) + (Month 2 retention × revenue) + ...
- **LTV** = ARPU × Gross Margin × Σ(retention %) = **$[X]**

---

## Contribution Margin Template

**Contribution Margin %** = (Revenue - Variable Costs) ÷ Revenue

### Revenue & Variable Costs

| Item | Per Unit | Notes |
|------|----------|-------|
| **Revenue** | $[X] | Subscription fee / Sale price / Transaction value |
| **Variable Costs:** | | (costs that scale with each unit) |
| - COGS | $[X] | Product cost, manufacturing |
| - Hosting / Infrastructure | $[X] | Per-user server costs |
| - Payment processing | $[X] | Stripe/PayPal fees (~2-3%) |
| - Support | $[X] | Per-customer support time |
| - Shipping | $[X] | Fulfillment, delivery |
| - Other variable | $[X] | [Specify] |
| **Total Variable Costs** | **$[Y]** | Sum |
| **Contribution Margin** | **$[X - Y]** | Revenue - Variable Costs |
| **Contribution Margin %** | **[(X-Y)/X]%** | Margin as % |

**Interpretation**:
- **High margin (>60%)**: Strong unit economics, room for high CAC
- **Medium margin (40-60%)**: Acceptable, need disciplined CAC management
- **Low margin (<40%)**: Challenging, requires very efficient acquisition or high LTV

**Levers to improve margin**:
- [ ] Increase pricing (improve revenue per unit)
- [ ] Reduce COGS (negotiate supplier costs, economies of scale)
- [ ] Optimize infrastructure (reduce hosting costs per user)
- [ ] Automate support (reduce manual support time)
- [ ] Negotiate payment fees (lower processing costs)

---

## Cohort Analysis Template

Track retention, LTV, and payback by customer acquisition cohort (month, channel, segment).

### Retention Cohort Table

| Cohort (Month Acquired) | M0 | M1 | M2 | M3 | M6 | M12 | LTV | CAC | LTV/CAC | Payback (months) |
|-------------------------|----|----|----|----|----|----|-----|-----|---------|------------------|
| Jan 2024 | 100% | 92% | 84% | 78% | 62% | 42% | $1,200 | $300 | 4.0 | 4.5 |
| Feb 2024 | 100% | 90% | 81% | 75% | 60% | - | $1,150 | $320 | 3.6 | 5.0 |
| Mar 2024 | 100% | 93% | 86% | 80% | 65% | - | $1,300 | $280 | 4.6 | 4.0 |
| Apr 2024 | 100% | 91% | 83% | 77% | - | - | $1,100 | $350 | 3.1 | 5.5 |
| **Average** | **100%** | **91.5%** | **83.5%** | **77.5%** | **62.3%** | **42%** | **$1,188** | **$313** | **3.8** | **4.8** |

**Insights**:
- [Are newer cohorts performing better or worse than older cohorts?]
- [Which cohorts have best/worst retention?]
- [Is LTV improving over time?]
- [Is CAC increasing or decreasing?]

### Cohort by Channel

| Channel | # Customers | Avg LTV | Avg CAC | LTV/CAC | 12M Retention | Payback (months) |
|---------|-------------|---------|---------|---------|---------------|------------------|
| Paid Search | 500 | $800 | $250 | 3.2 | 35% | 6.0 |
| Organic | 300 | $1,500 | $150 | 10.0 | 55% | 3.0 |
| Referral | 200 | $1,800 | $100 | 18.0 | 60% | 2.5 |
| Paid Social | 400 | $700 | $300 | 2.3 | 30% | 7.0 |
| **Total** | **1,400** | **$1,050** | **$225** | **4.7** | **42%** | **5.0** |

**Insights**:
- [Best channels: Referral (high LTV, low CAC, fast payback, high retention)]
- [Worst channels: Paid Social (low LTV, high CAC, slow payback, low retention)]
- [Action: Increase referral investment, reduce or pause paid social]

---

## Interpretation Template

### LTV/CAC Ratio Analysis

**Your LTV/CAC**: [X:1]

| Range | Assessment | Action |
|-------|------------|--------|
| <1:1 | **Unsustainable**: Losing money on every customer | Stop growth, fix model or pivot |
| 1:1 - 2:1 | **Marginal**: Barely profitable | Don't scale yet, improve retention or reduce CAC |
| 2:1 - 3:1 | **Acceptable**: Unit economics work | Optimize before scaling |
| 3:1 - 5:1 | **Good**: Can profitably grow | Scale marketing spend |
| >5:1 | **Excellent**: Strong economics | Aggressive scale, raise capital |

**Your assessment**: [Based on ratio above]

### Payback Period Analysis

**Your Payback Period**: [X] months

| Range | Assessment | Cash Impact |
|-------|------------|-------------|
| <6 months | **Excellent**: Fast capital recovery | Can reinvest quickly, fuel growth |
| 6-12 months | **Good**: Reasonable payback | Manageable cash needs |
| 12-18 months | **Acceptable**: Slower recovery | Need patient capital |
| >18 months | **Challenging**: Long payback | High cash burn, risky |

**Your assessment**: [Based on payback above]

### Combined Decision Framework

| Your Metrics | Recommendation |
|--------------|----------------|
| LTV/CAC: [X:1] | [Assessment from table above] |
| Payback: [Y] months | [Assessment from table above] |
| Gross Margin: [Z]% | [Good ≥60% (SaaS) / ≥40% (ecommerce), or needs improvement] |
| **Overall** | **[Stop / Optimize / Scale / Aggressive Scale]** |

### Recommendations

**Pricing**:
- [ ] [Increase price to improve margin and LTV]
- [ ] [Add premium tier for upsell]
- [ ] [Reduce price to increase conversion]
- [ ] [No change needed]

**Channels**:
- [ ] [Increase spend on: [channels with best LTV/CAC]]
- [ ] [Reduce or pause spend on: [channels with poor LTV/CAC]]
- [ ] [Test new channels: [suggestions]]

**Retention**:
- [ ] [Improve onboarding to reduce early churn]
- [ ] [Add features to increase engagement]
- [ ] [Customer success program for high-value customers]
- [ ] [Loyalty/referral program to increase repeat]

**Growth**:
- [ ] [Scale aggressively: Economics support growth]
- [ ] [Optimize first: Improve metrics before scaling]
- [ ] [Pause growth: Fix unit economics]

**Cash & Fundraising**:
- [ ] [Raise funding to fuel growth (if LTV/CAC >3:1 and payback <12 months)]
- [ ] [Focus on profitability (if LTV/CAC 2-3:1 and payback 12-18 months)]
- [ ] [Reduce burn (if LTV/CAC <2:1)]

---

## Quick Example: SaaS Startup

**Unit**: Customer (subscription)

**CAC**: $20k marketing, 100 customers → **$200 CAC**

**LTV**:
- ARPU: $100/month
- Gross Margin: 80%
- Monthly Churn: 5% → Lifetime = 1/0.05 = 20 months
- **LTV** = $100 × 20 × 80% = **$1,600**

**Metrics**:
- **LTV/CAC**: $1,600 / $200 = **8:1** ✓ Excellent
- **Payback**: $200 ÷ ($100 × 80%) = **2.5 months** ✓ Excellent
- **Gross Margin**: **80%** ✓ Strong

**Recommendation**: **Aggressive scale**. Economics are excellent (8:1 LTV/CAC, 2.5 month payback). Raise capital, increase marketing spend 2-3×, hire sales team, expand to new channels.

---

## Common Mistakes to Avoid

1. **Not using cohort data**: Don't average retention across all time periods. Recent cohorts may behave differently.
2. **Excluding costs**: Don't forget sales salaries, support, payment fees, refunds.
3. **Vanity LTV**: Don't project 5-year LTV with 1 month of data. Use observed retention only.
4. **Ignoring channels**: Don't blend CAC across all channels. Analyze each separately.
5. **Fixed vs variable costs**: Don't include fixed costs (engineering, rent) in contribution margin. Only variable costs that scale with units.
6. **Not updating**: Re-calculate quarterly. Unit economics change as you scale, market shifts, competition intensifies.

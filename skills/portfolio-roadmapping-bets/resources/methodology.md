# Portfolio Roadmapping Bets Methodology

## Table of Contents
1. [Horizon Planning Frameworks](#1-horizon-planning-frameworks)
2. [Bet Sizing Methodologies](#2-bet-sizing-methodologies)
3. [Portfolio Balancing Techniques](#3-portfolio-balancing-techniques)
4. [Dependency Mapping](#4-dependency-mapping)
5. [Exit & Scale Criteria](#5-exit--scale-criteria)
6. [Portfolio Review](#6-portfolio-review)
7. [Anti-Patterns & Fixes](#7-anti-patterns--fixes)

---

## 1. Horizon Planning Frameworks

### McKinsey Three Horizons

**H1: Extend & Defend Core** (70%)
- Timeline: 0-12mo | Risk: Low | Return: 10-30% | Examples: Feature improvements, optimizations

**H2: Build Emerging Businesses** (20%)
- Timeline: 6-24mo | Risk: Medium | Return: 2-5x | Examples: New product lines, geographies

**H3: Create Transformational Options** (10%)
- Timeline: 12-36+mo | Risk: High | Return: 10x+ | Examples: Moonshots, new business models

**Adjustments**: Startup (50/30/20), Enterprise (80/15/5), Scale-up (70/20/10)

### Now-Next-Later

**Now** (Shipping this quarter): >80% confidence, clear reqs, in development
**Next** (Starting 1-2 quarters): ~60% confidence, mostly clear, in planning
**Later** (Future quarters): ~40% confidence, unclear, in research

Use when: Teams uncomfortable with 6-12-24mo planning

### Dual-Track Agile

**Discovery** (Learn): User research, prototypes, experiments → Decide what to build
**Delivery** (Ship): Build, ship, monitor, iterate

**Application**: H1 = delivery, H2 = mix, H3 = discovery. Discovery runs 1-2 sprints ahead.

---

## 2. Bet Sizing Methodologies

### RICE Scoring

**Formula**: (Reach × Impact × Confidence) / Effort

- **Reach**: Users affected per quarter
- **Impact**: 0.25 (minimal) to 3 (massive)
- **Confidence**: 50% (low) to 100% (high)
- **Effort**: Person-months

**Example**: (5000 × 2 × 80%) / 4 = 2000 score

### ICE Scoring

**Formula**: (Impact + Confidence + Ease) / 3 or Impact × Confidence × Ease

- **Impact**: 1-10 scale
- **Confidence**: 1-10 scale
- **Ease**: 1-10 scale (inverse of effort)

Use when: Quick prioritization without reach data

### Effort/Impact Matrix

**Quadrants**:
- High Impact, Low Effort → Quick wins (do first)
- High Impact, High Effort → Strategic (plan carefully, H2/H3)
- Low Impact, Low Effort → Fill-ins (if spare capacity)
- Low Impact, High Effort → Avoid

### Kano Model

**Basic Needs**: Must-have (if missing, dissatisfied) → H1
**Performance Needs**: Linear satisfaction (more is better) → H1/H2
**Delight Needs**: Unexpected wow factors → H2/H3

---

## 3. Portfolio Balancing Techniques

### 70-20-10 Rule

- **70% Core**: Optimize existing (low risk, predictable return)
- **20% Adjacent**: Extend to new (medium risk, substantial return)
- **10% Transformational**: Create new (high risk, breakthrough potential)

**Measure by**: Bet count or effort. **Red flags**: >80% core (too safe), >30% transformational (too risky)

### Risk-Return Diversification

**Low Risk, Low Return** (Core): 80-90% win rate, 1.2-1.5x return
**Medium Risk, Medium Return** (Adjacent): 50-60% win rate, 2-3x return
**High Risk, High Return** (Transformational): 10-30% win rate, 10x+ return

**Portfolio construction**: Combine to achieve desired risk/return profile

### Barbell Strategy

**Structure**: 80-90% very safe + 10-20% very risky, 0% medium
**Rationale**: Safe bets sustain, risky bets create upside, avoid "meh" middle

### Pacing by Cycle Time

**Fast** (days-weeks): A/B tests, experiments → 50%
**Medium** (months): Features, initiatives → 30%
**Slow** (quarters-years): Platform, R&D → 20%

---

## 4. Dependency Mapping

### Critical Path Method

1. List all bets and dependencies
2. Map dependencies (A → B → C)
3. Calculate duration for each path
4. Identify critical path (longest)
5. Accelerate critical path

**Example**: Path A (3mo) → C (4mo) = 7mo ← Critical. Path B (2mo) → C (4mo) = 6mo (1mo slack)

### Dependency Types

- **Technical**: Infrastructure, APIs, data pipelines
- **Learning**: Insights from experiments
- **Strategic**: Prior bet must validate market
- **Resource**: Team availability

### Learning-Based Sequencing

**Pattern**: Small experiment (H1) → Validate → Large bet (H2) → Scale

**Example**: H1: 2-week prototype ($5K) | Exit if CTR <5% | Scale: H2: Full build ($500K) if CTR >10%

---

## 5. Exit & Scale Criteria

### North Star Metric Thresholds

**Example**: North Star = WAU
- Exit: If WAU lift <5% after 60 days, kill
- Scale: If WAU lift >15%, expand to all users

### Staged Funding

**Stage 1** (Seed): $50K → Prototype, 100 users, 20% engagement
- Exit if <20%, fund $200K for alpha if ≥20%

**Stage 2** (Series A): $200K → Alpha, 1000 users, 10% conversion
- Exit if <10%, fund $1M for full build if ≥10%

### Kill Criteria Examples

- **Time**: "If not validated in 90 days, kill"
- **Metric**: "If adoption <5%, kill"
- **Cost**: "If CAC >$100, kill"
- **Strategic**: "If competitor launches first, reassess"

### Scale Criteria Examples

- **Adoption**: "If >20% adopt in 30 days, expand"
- **Engagement**: "If usage >3x baseline, add features"
- **Revenue**: "If ARR >$100K, hire team"
- **Efficiency**: "If LTV/CAC >5, increase budget 3x"

---

## 6. Portfolio Review

### Review Cadence

- **H1**: Monthly (check progress, blockers, kill/pivot/scale)
- **H2**: Quarterly (ready to start? dependencies? promote to H1 or push to H3?)
- **H3**: Semi-annually (still strategic? market shifts? add/kill)

### Kill / Pivot / Persevere / Scale

**For each bet**:
- **Kill**: Criteria not met, no path to success
- **Pivot**: Partially working, adjust approach
- **Persevere**: On track, continue
- **Scale**: Exceeding expectations, double-down

### Portfolio Health Metrics

**Velocity**: Bets shipped/quarter (target: 5-10)
**Win Rate**: % meeting scale criteria (target: 20-40%), % exited (target: 10-30%)
**Impact**: Portfolio contribution to North Star, ROI (target: >3x)
**Balance**: Risk 70/20/10, Horizon 50/30/20

**Red flags**: Win <10% (too risky), Win >80% (too conservative), Exit <5% (not killing), Exit >50% (too risky)

---

## 7. Anti-Patterns & Fixes

### #1: Everything High Priority

**Symptom**: All must-have, no trade-offs
**Fix**: Force-rank (only top 3 high), MoSCoW (20% must, 30% should, 30% could, 20% won't), capacity-constrain

### #2: No Exit Criteria

**Symptom**: Bets continue indefinitely, zombie projects
**Fix**: Set criteria upfront, review monthly, celebrate killing

### #3: All Bets in H1

**Symptom**: Wish list, unrealistic
**Fix**: Capacity-constrain H1, move excess to H2/H3, set expectations

### #4: No H3 Pipeline

**Symptom**: Only H1/H2, no future exploration
**Fix**: Reserve 10-20% for H3, run experiments, refresh quarterly

### #5: All Core, No Transformational

**Symptom**: 100% incremental
**Fix**: Mandate 10% transformational, innovation sprints, measure % revenue from <3yr products (target 20%+)

### #6: Dependencies Ignored

**Symptom**: H2 depends on H1 infrastructure not prioritized
**Fix**: Map dependencies, prioritize blockers, review critical path

### #7: No Review Discipline

**Symptom**: Roadmap created once, never updated
**Fix**: Monthly H1, quarterly portfolio review, version control

### #8: Metrics-Free Bets

**Symptom**: No success metrics, unclear if worked
**Fix**: Require metrics per bet, instrument before ship, review post-launch

### #9: Over-Optimistic Impact

**Symptom**: Every bet "10x potential"
**Fix**: Use baselines, benchmark, risk-adjust (assume 50% success)

### #10: No Portfolio Balance

**Symptom**: All small (busy work) or all large (nothing ships)
**Fix**: Mix sizes (50% S, 30% M, 15% L, 5% XL), cycles (fast/medium/slow), risk (70/20/10)

---

## Quick Reference

### When to Use Each Framework

**Horizon Planning**: McKinsey (classic), Now-Next-Later (adaptive), Dual-Track (continuous)
**Bet Sizing**: RICE (quantitative), ICE (quick), Effort/Impact (visual), Kano (user satisfaction)
**Balancing**: 70-20-10 (risk), Risk-Return (diversification), Barbell (extremes), Pacing (cycles)
**Sequencing**: CPM (critical path), Dependency Matrix (complex), Learning-Based (de-risk)
**Criteria**: North Star (aligned), Staged Funding (VC model), Time/Metric/Cost/Strategic (varied)
**Review**: Monthly/Quarterly/Semi-annual (by horizon), Kill/Pivot/Persevere/Scale (framework)

### Common Patterns

**Product**: H1: Quick wins + strategic features | H2: Major features + platform | H3: Exploratory | 60% incremental, 30% substantial, 10% breakthrough

**Tech**: H1: Stability + migration start | H2: Complete migration + improvements | H3: Next-gen research | 50% maintain, 30% improve, 20% transform

**Innovation**: H1: Scale validated + new tests | H2: Strategic bets + experiments | H3: Moonshots | 70% core, 20% adjacent, 10% transformational

**Marketing**: H1: Optimize proven + test new | H2: Scale winners + brand | H3: Positioning + market entry | 70% performance, 20% growth, 10% brand

### Success Criteria

✓ Strategic theme clear & measurable
✓ Bets sized (S/M/L/XL) & impact quantified (1x/3x/10x)
✓ Sequenced across H1/H2/H3 with dependencies mapped
✓ Exit & scale criteria defined per bet
✓ Portfolio balanced (risk, horizon, size)
✓ Capacity feasible (effort ≤ capacity × 0.8)
✓ Impact ladders to theme (risk-adjusted)
✓ Review cadence established

### Red Flags

❌ No theme → wish list
❌ All "Large" → no prioritization
❌ No exit criteria → zombies
❌ Imbalanced (all core or all moonshots)
❌ Dependencies ignored → blocking
❌ Overcommitted (>80% capacity)
❌ Impact below goal
❌ No review → stale roadmap

---
name: paid-tier-readiness-check
description: Evaluates whether substacker has the four preconditions for launching a paid tier — enough subs, healthy engagement, a clear candidate section, writer capacity. Produces readiness score (not-ready / close / ready) with named gaps. Used when the "should we launch paid?" question is selected or at writer's explicit request. Trigger keywords: paid tier, paid readiness, monetization, Substack paid, launch paid, 1000 subscribers.
---

# Paid Tier Readiness Check

## Four gates

All four must pass for "ready":

1. **Scale**: ≥1,000 free subs OR explicit request to evaluate sub-1,000. At sub-500, refuse with reason: 2-5% conversion × 500 = 10-25 paid, below the threshold where paid changes behaviour.
2. **Engagement**: median open rate ≥40% across last 3 months (or documented reason low-rate is acceptable).
3. **Section candidate**: at least one section has ≥5 posts AND shows differential engagement vs publication baseline. This is the section paid subs would pay for.
4. **Writer capacity**: published at least once every 3 weeks for the last quarter. Launching paid adds pressure; irregular base breaks the writer.

## Workflow

```
Per check:
- [ ] Step 1: Load Growth Analyst most recent report (for subs, open rate)
- [ ] Step 2: Load section-map.md
- [ ] Step 3: Check each of the 4 gates
- [ ] Step 4: Assign score: not-ready | close | ready
- [ ] Step 5: Name the specific gap(s)
- [ ] Step 6: One-line recommendation
```

## Output

```markdown
**Scale**: pass | fail — {N} free subs ({threshold})
**Engagement**: pass | fail — median {N}% ({threshold})
**Section candidate**: pass | fail — {section} is candidate | no section qualifies yet
**Writer capacity**: pass | fail — {N} posts in last 12 weeks

**Score**: not-ready | close (gate {X} fails) | ready

**Recommendation**: {don't launch | revisit in Q+N after X | launch with offer}
```

## Worked example (at 847 subs, Q2)

- Scale: fail. 847 < 1000.
- Engagement: pass. Median 54% over last 12 weeks.
- Section candidate: pass. `agent-workshop` shows 62% avg open vs 54% baseline.
- Writer capacity: pass. 14 posts in 12 weeks.
- **Score**: close (scale gate fails).
- **Recommendation**: Don't launch. Revisit at Q3 when scale crosses 1000.

## Guardrails

1. Never recommend launching if scale <500 unless explicitly asked.
2. Engagement threshold is 40% median — well below Substack's 45-50% benchmark for well-engaged publications. Paid works below 45% with a strong candidate section.
3. Section candidate is not just "has a section" — must show differential engagement.
4. Writer capacity is about steady state, not spikes. Once-every-3-weeks is the floor.
5. "Ready" requires all 4 gates. "Close" means 3 of 4. "Not-ready" means 2 or fewer.

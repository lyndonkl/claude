# Meta Prompt Engineering Methodology

**When to use this methodology:** You've read [template.md](template.md) and need advanced techniques for:
- Diagnosing and fixing failing prompts systematically
- Optimizing prompts for production use (cost, latency, quality)
- Building multi-prompt workflows and self-refinement loops
- Adapting prompts across domains or use cases
- Debugging complex failure modes that basic fixes don't resolve

**If your prompt is simple:** Use [template.md](template.md) directly. This methodology is for complex, high-stakes, or production prompts.

---

## Table of Contents
1. [Diagnostic Framework](#1-diagnostic-framework)
2. [Advanced Patterns](#2-advanced-patterns)
3. [Optimization Techniques](#3-optimization-techniques)
4. [Prompt Debugging](#4-prompt-debugging)
5. [Multi-Prompt Workflows](#5-multi-prompt-workflows)
6. [Domain Adaptation](#6-domain-adaptation)
7. [Production Deployment](#7-production-deployment)

---

## 1. Diagnostic Framework

### When Simple Template Is Enough
**Indicators:** One-off task, low-stakes, subjective quality, single user
**Action:** Use [template.md](template.md), iterate once or twice, done.

### When You Need This Methodology
**Indicators:** Prompt fails >30% of runs, high-stakes, multi-user, complex reasoning, production deployment
**Action:** Use this methodology systematically.

### Failure Mode Diagnostic Tree

```
Is output inconsistent?
├─ YES → Format/constraints missing? → Add template and constraints
│        Role unclear? → Add specific role with expertise
│        Still failing? → Run optimization (Section 3)
└─ NO, but quality poor?
    ├─ Too short/long → Add length constraints per section
    ├─ Wrong tone → Define audience + formality level
    ├─ Hallucination → Add uncertainty expression (Section 4.2)
    ├─ Missing info → List required elements explicitly
    └─ Poor reasoning → Add chain-of-thought (Section 2.1)
```

---

## 2. Advanced Patterns

### 2.1 Chain-of-Thought (CoT) - Deep Dive

**When to use:** Complex reasoning, math/logic, multi-step inference, debugging.

**Advanced CoT with Verification:**
```
Solve this problem using the following process:

Step 1: Understand - Restate problem, identify givens vs unknowns, note constraints
Step 2: Plan - List 2+ approaches, evaluate feasibility, choose best with rationale
Step 3: Execute - Solve step-by-step showing work, check each step, backtrack if wrong
Step 4: Verify - Sanity check, test edge cases, try alternative method to cross-check
Step 5: Present - Summarize reasoning, state final answer, note assumptions/limitations
```

**Use advanced CoT when:** 50%+ attempts fail without verification, or errors compound (math, code, logic).

### 2.2 Self-Consistency (Ensemble CoT)

**Pattern:**
```
Generate 3 independent solutions:
Solution 1: [First principles]
Solution 2: [Alternative method]
Solution 3: [Focus on edge cases]

Compare: Where agree? (high confidence) Where differ? (investigate) Most robust? (why?)
Final answer: [Synthesize, note confidence]
```

**Cost: 3x inference.** Use when correctness > cost (medical, financial, legal) or need confidence calibration.

### 2.3 Least-to-Most Prompting

**For complex problems overwhelming context:**
```
Stage 1: Simplest case (e.g., n=1) → Solve
Stage 2: Add one complexity (e.g., n=2) → Solve building on Stage 1
Stage 3: Full complexity → Solve using insights from 1-2
```

**Use cases:** Math proofs, recursive algorithms, scaling strategies, learning complex topics.

### 2.4 Constitutional AI (Safety-First)

**Pattern for high-risk domains:**
```
[Complete task]

Critique your response:
1. Potential harms? (physical, financial, reputational, psychological)
2. Bias check? (unfairly favor/disfavor any group)
3. Accuracy? (claims verifiable? flag speculation)
4. Completeness? (missing caveats/warnings)

Revise: Fix issues, add warnings, hedge uncertain claims
If fundamental safety concerns remain: "Cannot provide due to [concern]"
```

**Required for:** Medical, legal, financial advice, safety-critical engineering, advice affecting vulnerable populations.

---

## 3. Optimization Techniques

### 3.1 Iterative Refinement Protocol

**Cycle:**
1. Baseline: Run 10x, measure consistency, quality, time
2. Identify: Most common failure (≥3/10 runs)
3. Hypothesize: Why? (missing constraint, ambiguous step, wrong role)
4. Intervene: Add specific fix
5. Test: Run 10x, compare to baseline
6. Iterate: Until quality threshold met or diminishing returns

**Metrics:**
- Consistency: % meeting requirements (target ≥80%)
- Length variance: σ/μ word count (target <20%)
- Format compliance: % matching structure (target ≥90%)
- Quality rating: Human 1-5 scale (target ≥4.0 avg, σ<1.0)

### 3.2 A/B Testing Prompts

**Setup:** Variant A (current), Variant B (modification), 20 runs (10 each), define success metric
**Analyze:** Compare distributions, statistical test (t-test, F-test), review failures
**Decide:** If B significantly better (p<0.05) and meaningfully better (>10%), adopt B

### 3.3 Prompt Compression

**Remove redundancy:**
- Before: "You must include citations. Citations should be in (Author, Year) format. Every factual claim needs a citation."
- After: "Cite all factual claims in (Author, Year) format."

**Use examples instead of rules:** Instead of 10 formatting rules, show 2 examples
**External knowledge:** "Follow Python PEP 8" instead of embedding rules
**Tradeoff:** Compression can reduce clarity. Test thoroughly.

---

## 4. Prompt Debugging

### 4.1 Failure Taxonomy

| Failure Type | Symptom | Fix |
|--------------|---------|-----|
| **Format error** | Wrong structure | Add explicit template with example |
| **Length error** | Too short/long | Add min-max per section |
| **Tone error** | Wrong formality | Define target audience + formality |
| **Content omission** | Missing required elements | List "Must include: [X, Y, Z]" |
| **Hallucination** | False facts | Add "If unsure, say 'I don't know'" |
| **Reasoning error** | Logical jumps | Add chain-of-thought |
| **Bias** | Stereotypes | Add "Consider multiple viewpoints" |
| **Inconsistency** | Different outputs for same input | Add constraints, examples |

### 4.2 Anti-Hallucination Techniques (Layered Defense)

**Layer 1:** "If you don't know, say 'I don't know.' Do not guess."
**Layer 2:** Format with confidence: `[Claim] - Source: [Citation or "speculation"] - Confidence: High/Medium/Low`
**Layer 3:** Self-check: "Review each claim: Verifiable? Or speculation (labeled as such)?"
**Layer 4:** Example: "Good: 'Paris is France's capital (High)' Bad: 'Lyon is France's capital' (incorrect as fact)"

### 4.3 Debugging Process

1. **Reproduce:** Run 5x, confirm failure rate, save outputs
2. **Minimal failing example:** Simplify input, remove unrelated sections, isolate failing instruction
3. **Hypothesis:** What's missing/ambiguous/wrong?
4. **Targeted fix:** Change one thing, test minimal example, then test full prompt
5. **Regression test:** Ensure fix didn't break other cases, test edge cases

---

## 5. Multi-Prompt Workflows

### 5.1 Sequential Chaining

**Pattern:** Prompt 1 (generate ideas) → Prompt 2 (evaluate/filter) → Prompt 3 (develop top 3)
**When:** Complex tasks in stages, early steps inform later, different roles needed (creator→critic→developer)
**Example:** Outline → Draft → Edit for content writing

### 5.2 Self-Refinement Loop

**Pattern:** Generator (create) → Critic (identify flaws) → Refiner (revise) → Repeat until approval or max 3 iterations
**Cost:** 2-4x inference. Use for high-stakes outputs (user-facing content, production code).

### 5.3 Ensemble Methods

**Majority vote:** Run 5x, take majority answer at each decision point (classification, multiple-choice, binary)
**Ranker fusion:** Prompt A (top 10) + Prompt B (top 10 different framing) → Prompt C ranks A∪B → Output top 5
**Use case:** Recommendation systems, content curation, prioritization.

---

## 6. Domain Adaptation

### 6.1 Transferring Prompts Across Domains

**Challenge:** Prompt for Domain A fails in Domain B.

**Adaptation checklist:**
- [ ] Update role to domain expert
- [ ] Replace examples with domain-appropriate ones
- [ ] Add domain-specific constraints (citation format, regulatory compliance)
- [ ] Update quality checks for domain risks (medical: patient safety, legal: liability)
- [ ] Adjust terminology ("user"→"patient", "feature"→"intervention")

### 6.2 Domain-Specific Quality Criteria

**Software:** Security (no SQL injection, XSS), testing (≥80% coverage), style (linting, naming)
**Medical:** Evidence (peer-reviewed), safety (risks/contraindications), scope ("consult a doctor" disclaimer)
**Legal:** Jurisdiction, disclaimer (not legal advice), citations (case law, statutes)
**Finance:** Disclaimer (not financial advice), risk (uncertainties, worst-case), data (recent, note dates)

---

## 7. Production Deployment

### 7.1 Versioning

**Track changes:**
```
# v1.0 (2024-01-15): Initial. Hallucination ~20%
# v1.1 (2024-01-20): Added anti-hallucination. Hallucination ~8%
# v1.2 (2024-01-25): Added format template. Consistency 72%→89%
```

**Rollback plan:** Keep previous version. If v1.2 fails in production, revert to v1.1.

### 7.2 Monitoring

**Automated:** Length (track tokens, flag outliers >2σ), format (regex check), keywords (flag missing required terms)
**Human review:** Sample 5-10 daily, rate on rubric, report trends
**Alerting:** If failure rate >20%, alert. If latency >2x baseline, check prompt length creep.

### 7.3 Graceful Degradation

```
Try: Primary prompt (detailed, high-quality)
↓ If fails (timeout, error, format issue)
Try: Secondary prompt (simplified, faster)
↓ If fails
Return: Error message + human escalation
```

### 7.4 Cost-Quality Tradeoffs

**Shorter prompts (30-50% cost reduction, 10-20% quality drop):**
- When: High volume, low-stakes, latency-sensitive
- How: Remove examples, compress constraints, use implicit knowledge

**Longer prompts (50-100% cost increase, 15-30% quality/consistency improvement):**
- When: High-stakes, complex reasoning, consistency > cost
- How: Add examples, chain-of-thought, verification steps, domain knowledge

**Temperature tuning:**
- 0: Deterministic, high consistency (production, low creativity)
- 0.3-0.5: Balanced (good default)
- 0.7-1.0: High variability, creative (brainstorming, diverse outputs, less consistent)

**Recommendation:** Start at 0.3, test 10 runs, adjust.

---

## Quick Decision Trees

### "Should I optimize further?"

```
Meeting requirements >80% of time?
├─ YES → Stop (diminishing returns)
└─ NO → Optimization effort <1 hour?
    ├─ YES → Optimize (Section 3)
    └─ NO → Production use case?
        ├─ YES → Worth it, optimize
        └─ NO → Accept quality or simplify task
```

### "Should I use multi-prompt workflow?"

```
Task achievable in one prompt with acceptable quality?
├─ YES → Use single prompt (simpler)
└─ NO → Task naturally decomposes into stages?
    ├─ YES → Sequential chaining (Section 5.1)
    └─ NO → Quality insufficient with single prompt?
        ├─ YES → Self-refinement (Section 5.2)
        └─ NO → Accept single prompt or reframe
```

---

## Summary: When to Use What

| Technique | Use When | Cost | Complexity |
|-----------|----------|------|------------|
| **Basic template** | Simple, one-off | 1x | Low |
| **Chain-of-thought** | Complex reasoning | 1.5x | Medium |
| **Self-consistency** | Correctness critical | 3x | Medium |
| **Self-refinement** | High-stakes, iterative | 2-4x | High |
| **Sequential chaining** | Natural stages | 1.5-2x | Medium |
| **A/B testing** | Production optimization | 2x (one-time) | Medium |
| **Full methodology** | Production, high-stakes | Varies | High |

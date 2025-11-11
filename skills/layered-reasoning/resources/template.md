# Layered Reasoning Templates

Quick-start templates for structuring multi-level reasoning, checking consistency across layers, and translating between abstraction levels.

---

## Template 1: 3-Layer Reasoning Document

**When to use**: Designing systems, planning strategy, explaining concepts at multiple depths

### Layered Reasoning Template

**Topic/System**: [Name of what you're analyzing]

**Purpose**: [Why this layering matters]

**Date**: [Date]

---

### Layer 1: Strategic (30,000 ft) — WHY

**Core Principles/Invariants**:
1. [Principle 1, e.g., "Customer privacy is non-negotiable"]
2. [Principle 2, e.g., "System must scale to 10× current load"]
3. [Principle 3, e.g., "Developer productivity is paramount"]

**Strategic Constraints**:
- [Constraint 1, e.g., "Must comply with GDPR"]
- [Constraint 2, e.g., "Cannot exceed $X budget"]
- [Constraint 3, e.g., "Launch within 6 months"]

**Assumptions**:
- [Assumption 1, e.g., "Market remains competitive"]
- [Assumption 2, e.g., "Cloud infrastructure available"]

**Success Criteria (Strategic)**:
- [Metric 1, e.g., "Market leader in trust ratings"]
- [Metric 2, e.g., "Support 100M users"]

---

### Layer 2: Tactical (3,000 ft) — WHAT

**Approaches/Architectures** (that satisfy strategic layer):

**Approach 1**: [Name, e.g., "Microservices Architecture"]
- **Satisfies**: [Which strategic principles, e.g., "Scales to 10×, enables team independence"]
- **Tactics**:
  - [Tactic 1, e.g., "Service mesh for inter-service communication"]
  - [Tactic 2, e.g., "Event-driven architecture for async operations"]
  - [Tactic 3, e.g., "API gateway for external requests"]
- **Tradeoffs**: [What's sacrificed, e.g., "Increased operational complexity"]

**Approach 2**: [Name, e.g., "Zero-Trust Security Model"]
- **Satisfies**: [Which strategic principles, e.g., "Customer privacy, GDPR compliance"]
- **Tactics**:
  - [Tactic 1, e.g., "End-to-end encryption for all data"]
  - [Tactic 2, e.g., "Identity-based access control"]
  - [Tactic 3, e.g., "Continuous verification, no implicit trust"]
- **Tradeoffs**: [What's sacrificed, e.g., "Slight performance overhead"]

**Success Criteria (Tactical)**:
- [Metric 1, e.g., "99.9% uptime"]
- [Metric 2, e.g., "API response time <100ms p95"]

---

### Layer 3: Operational (300 ft) — HOW

**Implementation Details** (that realize tactical layer):

**Implementation 1**: [Tactic being implemented, e.g., "Service Mesh"]
- **Technology**: [Specific tools, e.g., "Istio on Kubernetes"]
- **Procedures**:
  - [Step 1, e.g., "Deploy sidecar proxies to each pod"]
  - [Step 2, e.g., "Configure mutual TLS between services"]
  - [Step 3, e.g., "Set up traffic routing rules"]
- **Timeline**: [When, e.g., "Sprint 1-2"]
- **Owner**: [Who, e.g., "Platform team"]

**Implementation 2**: [Tactic being implemented, e.g., "End-to-End Encryption"]
- **Technology**: [Specific tools, e.g., "AWS KMS for key management, AES-256 encryption"]
- **Procedures**:
  - [Step 1, e.g., "Generate master key in KMS"]
  - [Step 2, e.g., "Encrypt data at rest using KMS data keys"]
  - [Step 3, e.g., "Use TLS 1.3 for data in transit"]
- **Timeline**: [When, e.g., "Sprint 3"]
- **Owner**: [Who, e.g., "Security team"]

**Success Criteria (Operational)**:
- [Metric 1, e.g., "100% services behind Istio"]
- [Metric 2, e.g., "All PHI encrypted, verified in audit"]

---

### Consistency Validation

**Upward Consistency** (Do operations implement tactics? Do tactics achieve strategy?):
- ☐ [Check 1]: Does Istio implementation enable microservices architecture? → [Yes/No + Evidence]
- ☐ [Check 2]: Does microservices architecture support 10× scale? → [Yes/No + Evidence]
- ☐ [Check 3]: Does encryption implementation satisfy privacy principle? → [Yes/No + Evidence]

**Downward Consistency** (Can strategy be executed with tactics? Can tactics be implemented?):
- ☐ [Check 1]: Can we achieve GDPR compliance with chosen tactics? → [Yes/No + Gaps]
- ☐ [Check 2]: Can we implement Istio within budget/timeline? → [Yes/No + Constraints]

**Lateral Consistency** (Do parallel choices contradict?):
- ☐ [Check 1]: Does encryption overhead conflict with <100ms latency goal? → [Yes/No + Mitigation]
- ☐ [Check 2]: Do microservices complexity conflict with 6-month timeline? → [Yes/No + Adjustment]

**Emergent Properties Observed**:
- [Emergence 1, e.g., "Microservices increased cross-team coordination overhead → slowed feature delivery"]
- [Implication, e.g., "Adjust strategy: 'Scale' includes team coordination, not just technical scale"]

---

### Change Propagation Plan

**If Strategic Layer Changes**:
- [Change scenario, e.g., "New regulation requires data residency"] →
- [Tactical impact, e.g., "Need multi-region deployment with geo-replication"] →
- [Operational impact, e.g., "Deploy regional clusters, implement data sovereignty"]

**If Operational Constraint Discovered**:
- [Constraint, e.g., "Istio adds 50ms latency, exceeds <100ms goal"] →
- [Tactical adjustment, e.g., "Switch to Linkerd (lighter sidecar) or optimize routes"] →
- [Strategic clarification, e.g., "Refine: <100ms for critical paths, <200ms for others"]

---

## Template 2: Cross-Layer Communication Plan

**When to use**: Presenting to stakeholders at different levels (board, management, engineers)

### Communication Template

**Core Message**: [Single sentence summarizing what you're communicating]

---

### For Executive Audience (30K ft - Strategic)

**Slide 1: WHY** (Problem/Opportunity)
- **Context**: [Strategic context, e.g., "Market shifting to privacy-first products"]
- **Impact**: [Business impact, e.g., "Losing 20% customers to competitors on trust"]
- **Outcome**: [Desired end state, e.g., "Become market leader in data privacy"]

**Slide 2: WHAT** (Approach)
- **Strategy**: [High-level approach, e.g., "Zero-trust architecture, end-to-end encryption, transparent security"]
- **Investment**: [Resources required, e.g., "$2M, 6 months, 10 engineers"]
- **Risk**: [Key risks, e.g., "Performance impact, timeline risk if encryption complex"]

**Slide 3: OUTCOMES** (Success Metrics)
- **Revenue impact**: [e.g., "$5M ARR from enterprise customers requiring compliance"]
- **Market position**: [e.g., "SOC 2 Type II + GDPR certified within 6 months"]
- **Risk mitigation**: [e.g., "Avoid $XM penalty for non-compliance"]

**Language**: Business outcomes, revenue, market share, strategic risk. Avoid technical details.

---

### For Management Audience (3K ft - Tactical)

**Roadmap Overview**:
- **Q1**: [Tactical milestone, e.g., "Implement encryption at rest + TLS 1.3"]
- **Q2**: [Tactical milestone, e.g., "Deploy zero-trust access controls + audit logging"]
- **Q3**: [Tactical milestone, e.g., "SOC 2 audit + penetration testing"]

**Team & Resources**:
- **Security Team** (5 engineers): Encryption, access control, audit systems
- **Platform Team** (3 engineers): Infrastructure, key management, monitoring
- **Product Team** (2 engineers): User-facing privacy controls

**Dependencies & Risks**:
- **Dependency 1**: [e.g., "Requires AWS KMS setup (1 week)"]
- **Risk 1**: [e.g., "Encryption may slow API response; plan optimization sprint"]

**Success Metrics**:
- [Metric 1, e.g., "100% data encrypted by end Q1"]
- [Metric 2, e.g., "Pass SOC 2 audit Q3"]

**Language**: Roadmaps, team velocity, dependencies, milestones. Some technical detail but focus on execution.

---

### For Engineering Audience (300 ft - Operational)

**Technical Design**:
- **Architecture**: [e.g., "Client → API Gateway (TLS 1.3) → Service Mesh (mTLS) → Encrypted DB"]
- **Components**:
  - [Component 1, e.g., "AWS KMS for key management"]
  - [Component 2, e.g., "AES-256-GCM for data at rest"]
  - [Component 3, e.g., "Istio sidecar proxies for service-to-service encryption"]

**Implementation Steps**:
1. [Step 1, e.g., "Set up AWS KMS, create customer master key"]
2. [Step 2, e.g., "Implement encryption layer in data access library"]
3. [Step 3, e.g., "Deploy Istio with mTLS strict mode"]
4. [Step 4, e.g., "Migrate existing data: encrypt in background job"]
5. [Step 5, e.g., "Update monitoring: track encryption overhead"]

**Code Example** (if relevant):
```python
# Encrypt data before storing
def store_user_data(user_id, data):
    encrypted_data = kms.encrypt(data, key_id='customer-master-key')
    db.insert(user_id, encrypted_data)
```

**Testing Plan**:
- [Test 1, e.g., "Unit tests for encryption/decryption"]
- [Test 2, e.g., "Integration tests for end-to-end encrypted flow"]
- [Test 3, e.g., "Performance tests: measure latency impact"]

**Language**: Code, architecture diagrams, APIs, specific technologies, testing. Detailed and technical.

---

## Template 3: Consistency Check Matrix

**When to use**: Validating alignment across layers before finalizing decisions

### Consistency Check Template

**System/Decision**: [What you're validating]

---

| Layer Pair | Consistency Question | Status | Evidence/Gaps | Action Required |
|------------|----------------------|--------|---------------|-----------------|
| **Ops → Tactical** | Do operational procedures implement tactical approaches? | ☐ Pass ☐ Fail | [e.g., "Istio implements service mesh as planned"] | [e.g., "None" or "Fix X"] |
| **Tactical → Strategic** | Do tactical approaches achieve strategic principles? | ☐ Pass ☐ Fail | [e.g., "Zero-trust satisfies privacy principle"] | [e.g., "None" or "Adjust Y"] |
| **Strategic → Tactical** | Can strategic goals be achieved with chosen tactics? | ☐ Pass ☐ Fail | [e.g., "Tactics support GDPR compliance"] | [e.g., "None" or "Add Z tactic"] |
| **Tactical → Ops** | Can tactical approaches be implemented operationally? | ☐ Pass ☐ Fail | [e.g., "Team has Istio expertise"] | [e.g., "Hire or train"] |
| **Ops A ↔ Ops B** | Do parallel operational choices conflict? | ☐ Pass ☐ Fail | [e.g., "Encryption + caching compatible"] | [e.g., "Optimize cache encryption"] |
| **Tactical A ↔ Tactical B** | Do parallel tactical approaches contradict? | ☐ Pass ☐ Fail | [e.g., "Microservices + monorepo: no conflict"] | [e.g., "None" or "Choose one"] |

---

**Overall Consistency**: ☐ **Aligned** (all pass) ☐ **Minor Issues** (1-2 fails, fixable) ☐ **Major Issues** (3+ fails, rethink)

**Summary of Gaps**:
1. [Gap 1, e.g., "Encryption overhead conflicts with latency SLA → Need optimization"]
2. [Gap 2, e.g., "No plan for key rotation → Add operational procedure"]

**Remediation Plan**:
1. [Action 1, e.g., "Benchmark encryption overhead, optimize hot paths"]
2. [Action 2, e.g., "Define 90-day key rotation policy, automate in KMS"]

---

## Template 4: Layer Transition Analysis

**When to use**: When changing strategies, discovering operational constraints, or refactoring systems

### Transition Template

**Transition Type**: ☐ **Top-Down** (Strategy changed) ☐ **Bottom-Up** (Operational constraint discovered)

---

### If Top-Down (Strategy Change)

**Strategic Change**: [What changed at strategic layer, e.g., "New regulation requires data residency in EU"]

**Tactical Implications**:
- **Current Tactics**: [e.g., "Single US region deployment"]
- **Required Tactics**: [e.g., "Multi-region deployment with EU data sovereignty"]
- **New Tactics**: [e.g., "Deploy EU cluster, implement regional routing, data replication"]

**Operational Implications**:
- **Current Operations**: [e.g., "Single AWS us-east-1 region"]
- **Required Operations**: [e.g., "AWS eu-west-1 cluster, regional databases, GDPR-compliant data handling"]
- **Migration Plan**: [Timeline and steps, e.g., "Q1: Deploy EU infra, Q2: Migrate EU customers"]

**Cost/Impact**:
- **Resources**: [e.g., "$500K infrastructure, 3 engineers for 3 months"]
- **Risk**: [e.g., "Data sync latency, potential data loss during migration"]

---

### If Bottom-Up (Operational Constraint)

**Operational Constraint**: [What was discovered, e.g., "Istio sidecar adds 50ms latency, exceeds 100ms SLA"]

**Tactical Re-Evaluation**:
- **Current Tactic**: [e.g., "Istio service mesh for microservices"]
- **Options**:
  1. **Option A**: [e.g., "Switch to Linkerd (lighter, ~10ms overhead)"]
  2. **Option B**: [e.g., "Optimize Istio config, remove unnecessary features"]
  3. **Option C**: [e.g., "Selective mesh: only for services needing mTLS"]
- **Recommendation**: [Which option and why]

**Strategic Clarification** (if needed):
- **Original Strategy**: [e.g., "<100ms latency for all APIs"]
- **Refined Strategy**: [e.g., "<100ms for critical paths (user-facing), <200ms for internal APIs"]
- **Rationale**: [e.g., "Security (mTLS) worth 50ms for internal, but optimize user-facing"]

**Decision**: ☐ **Keep Strategy, Adjust Tactics** ☐ **Refine Strategy, Keep Tactics** ☐ **Both Change**

---

## Quick Reference: When to Use Each Template

| Template | Use Case | Output |
|----------|----------|--------|
| **3-Layer Reasoning Document** | Designing systems, planning strategy | Structured doc with strategic/tactical/operational layers + consistency checks |
| **Cross-Layer Communication** | Presenting to different stakeholders | Tailored messaging for exec/management/engineers |
| **Consistency Check Matrix** | Validating alignment before finalizing | Gap analysis with remediation plan |
| **Layer Transition Analysis** | Strategy changes or operational constraints | Impact analysis + migration/adjustment plan |

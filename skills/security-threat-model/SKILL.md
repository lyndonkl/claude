---
name: security-threat-model
description: Systematically identifies vulnerabilities, threats, and mitigations for systems handling sensitive data using STRIDE methodology, trust boundary mapping, and defense-in-depth principles. Use when designing or reviewing systems with PII/PHI/financial/auth data, building security-sensitive features (auth, payments, file uploads, APIs), preparing for audits or compliance (PCI, HIPAA, SOC 2), investigating incidents, or integrating third-party services. Use when user mentions threat model, STRIDE, trust boundaries, attack surface, or security review.
---

# Security Threat Model

## Table of Contents
1. [Workflow](#workflow)
2. [STRIDE Framework](#stride-framework)
3. [Trust Boundary Mapping](#trust-boundary-mapping)
4. [Common Patterns](#common-patterns)
5. [Guardrails](#guardrails)
6. [Quick Reference](#quick-reference)

## Workflow

Copy this checklist and track your progress:

```
Security Threat Model Progress:
- [ ] Step 1: Map system architecture and data flows
- [ ] Step 2: Identify trust boundaries
- [ ] Step 3: Classify data and compliance requirements
- [ ] Step 4: Apply STRIDE to identify threats
- [ ] Step 5: Define mitigations, monitoring, and prioritize risks
```

**Step 1: Map system architecture and data flows**

Document components, external services, users, data stores, and communication paths. See [Common Patterns](#common-patterns) for architecture examples. For straightforward systems → Use [resources/template.md](resources/template.md).

**Step 2: Identify trust boundaries**

Mark where data crosses security domains (user → server, server → database, internal → third-party). See [Trust Boundary Mapping](#trust-boundary-mapping) for boundary types.

**Step 3: Classify data and compliance requirements**

Rate data sensitivity (public, internal, confidential, restricted), identify PII/PHI/PCI, document compliance obligations (GDPR, HIPAA, PCI DSS). See [resources/template.md](resources/template.md) for classification tables.

**Step 4: Apply STRIDE to identify threats**

For each trust boundary and data flow, systematically check all six STRIDE threat categories. See [STRIDE Framework](#stride-framework) for threat identification. For complex systems with multiple attack surfaces → Study [resources/methodology.md](resources/methodology.md) for advanced attack tree analysis and DREAD scoring.

**Step 5: Define mitigations, monitoring, and prioritize risks**

Propose preventive/detective/corrective controls, establish monitoring and alerting, prioritize by risk score (likelihood × impact). Self-check using [resources/evaluators/rubric_security_threat_model.json](resources/evaluators/rubric_security_threat_model.json). Minimum standard: Average score ≥ 3.5.

## STRIDE Framework

**S - Spoofing Identity**
- **Threat**: Attacker impersonates legitimate user or system
- **Examples**: Stolen credentials, session hijacking, caller ID spoofing, email spoofing
- **Mitigations**: Multi-factor authentication, certificate validation, cryptographic signatures, mutual TLS

**T - Tampering with Data**
- **Threat**: Unauthorized modification of data in transit or at rest
- **Examples**: Man-in-the-middle attacks, SQL injection, file modification, message replay
- **Mitigations**: HTTPS/TLS, input validation, parameterized queries, digital signatures, checksums, immutable storage

**R - Repudiation**
- **Threat**: User denies performing action, no proof of activity
- **Examples**: Deleted logs, unsigned transactions, missing audit trails
- **Mitigations**: Comprehensive audit logging, digital signatures on transactions, tamper-proof logs, third-party timestamping

**I - Information Disclosure**
- **Threat**: Exposure of sensitive information to unauthorized parties
- **Examples**: Database dumps, verbose error messages, unencrypted backups, API over-fetching
- **Mitigations**: Encryption at rest/in transit, access control, data minimization, secure deletion, redaction in logs

**D - Denial of Service**
- **Threat**: System becomes unavailable or degraded
- **Examples**: Resource exhaustion, distributed attacks, algorithmic complexity exploits, storage filling
- **Mitigations**: Rate limiting, auto-scaling, circuit breakers, input size limits, CDN/DDoS protection

**E - Elevation of Privilege**
- **Threat**: Attacker gains unauthorized access or permissions
- **Examples**: SQL injection to admin, IDOR to other user data, path traversal, privilege escalation bugs
- **Mitigations**: Principle of least privilege, input validation, authorization checks on every request, role-based access control

## Trust Boundary Mapping

**Trust boundary**: Where data crosses security domains with different trust levels.

**Common boundaries:**
- **User → Application**: Untrusted input enters system (validate, sanitize, rate limit)
- **Application → Database**: Application credentials vs. user permissions (parameterized queries, connection pooling)
- **Internal → External Service**: Data leaves your control (encryption, audit logging, contract terms)
- **Public → Private Network**: Internet to internal systems (firewall, VPN, API gateway)
- **Client-side → Server-side**: JavaScript to backend (never trust client, re-validate server-side)
- **Privileged → Unprivileged Code**: Admin functions vs. user code (isolation, separate processes, security boundaries)

**Boundary analysis questions:**
- What data crosses this boundary? (classify sensitivity)
- Who/what is on each side? (authentication, authorization)
- What could go wrong at this crossing? (apply STRIDE)
- What controls protect this boundary? (authentication, encryption, validation, rate limiting)

## Common Patterns

**Pattern 1: Web Application with Database**
- **Boundaries**: User ↔ Web Server ↔ Database
- **Critical threats**: SQLi (Tampering), XSS (Spoofing), CSRF (Spoofing), session hijacking (Spoofing), IDOR (Elevation of Privilege)
- **Key mitigations**: Parameterized queries, CSP headers, CSRF tokens, HttpOnly/Secure cookies, authorization checks

**Pattern 2: API with Third-Party OAuth**
- **Boundaries**: User ↔ Frontend ↔ API Server ↔ OAuth Provider ↔ Third-Party API
- **Critical threats**: Token theft (Spoofing), scope creep (Elevation of Privilege), authorization code interception, redirect URI manipulation
- **Key mitigations**: PKCE for public clients, state parameter validation, token rotation, minimal scopes, HTTPS only

**Pattern 3: Microservices Architecture**
- **Boundaries**: API Gateway ↔ Service A ↔ Service B ↔ Message Queue ↔ Database
- **Critical threats**: Service impersonation (Spoofing), lateral movement (Elevation of Privilege), message tampering (Tampering), service enumeration (Information Disclosure)
- **Key mitigations**: mTLS between services, service mesh, API authentication per service, network policies, least privilege IAM

**Pattern 4: File Upload Service**
- **Boundaries**: User ↔ Upload Handler ↔ Virus Scanner ↔ Object Storage
- **Critical threats**: Malware upload (Tampering), path traversal (Information Disclosure), file overwrite (Tampering), storage exhaustion (DoS)
- **Key mitigations**: File type validation (magic bytes not extension), size limits, virus scanning, unique file naming, separate storage domain

**Pattern 5: Mobile App with Backend API**
- **Boundaries**: Mobile App ↔ API Gateway ↔ Backend Services
- **Critical threats**: API key extraction (Information Disclosure), certificate pinning bypass (Tampering), local data theft (Information Disclosure), reverse engineering
- **Key mitigations**: Certificate pinning, ProGuard/R8 obfuscation, biometric auth, local encryption (Keychain/Keystore), root/jailbreak detection

## Guardrails

**Assume breach mindset:**
- Don't ask "can attacker get in?" but "when attacker gets in, what damage can they do?"
- Defense in depth: Multiple overlapping controls, no single point of failure
- Least privilege: Minimal permissions by default, explicit grants only

**Prioritize realistically:**
- Focus on high-value assets (customer data, credentials, financial data) first
- Address compliance-critical threats (PCI, HIPAA) before nice-to-haves
- Balance security cost vs. risk (don't over-engineer low-risk systems)

**Avoid security theater:**
- **Security theater**: Controls that feel secure but don't meaningfully reduce risk (e.g., password complexity without rate limiting = still vulnerable to credential stuffing)
- **Effective security**: Address actual threat vectors with measurable risk reduction

**Document assumptions:**
- "Assumes database is not publicly accessible" (validate with network config)
- "Assumes TLS 1.2+ enforced" (verify in load balancer settings)
- "Assumes environment variables protected" (confirm secrets management)

**Update threat model:**
- Threat models decay (new features, new attack techniques, infrastructure changes)
- Review quarterly or when architecture changes significantly
- Incorporate lessons from incidents and security research

## Quick Reference

**Resources:**
- **Quick threat model**: [resources/template.md](resources/template.md)
- **Advanced techniques**: [resources/methodology.md](resources/methodology.md) (attack trees, DREAD scoring, abuse cases)
- **Quality rubric**: [resources/evaluators/rubric_security_threat_model.json](resources/evaluators/rubric_security_threat_model.json)

**5-Step Process**: Map Architecture → Identify Boundaries → Classify Data → Apply STRIDE → Mitigate & Monitor

**STRIDE**: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege

**Trust Boundaries**: User→App, App→DB, Internal→External, Public→Private, Client→Server, Privileged→Unprivileged

**Mitigation Types**: Preventive (block attacks), Detective (identify attacks), Corrective (respond to attacks)

**Prioritization**: High-value assets first, compliance-critical threats, realistic risk vs. cost balance

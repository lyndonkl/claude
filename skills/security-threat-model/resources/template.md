# Security Threat Model Template

## Workflow

Copy this checklist and track your progress:

```
Security Threat Model Progress:
- [ ] Step 1: Map system architecture and data flows
- [ ] Step 2: Identify trust boundaries
- [ ] Step 3: Classify data and compliance
- [ ] Step 4: Apply STRIDE to each boundary
- [ ] Step 5: Define mitigations and monitoring
```

**Step 1: Map system architecture**

Complete the [System Architecture](#system-architecture) section. Document all components and data flows.

**Step 2: Identify trust boundaries**

Mark boundaries in the [Trust Boundaries](#trust-boundaries) section. Identify where data crosses security domains.

**Step 3: Classify data**

Complete [Data Classification](#data-classification). Rate sensitivity and identify compliance requirements.

**Step 4: Apply STRIDE**

For each boundary, complete [STRIDE Analysis](#stride-analysis). Systematically check all six threat categories.

**Step 5: Define mitigations**

Document controls in [Mitigations & Monitoring](#mitigations--monitoring). Prioritize by risk score.

---

## Security Threat Model

### System Overview

**System Name**: [Name of system being threat modeled]

**Purpose**: [What this system does, business value, users served]

**Scope**: [What's included in this threat model, what's out of scope]

**Date**: [Date of analysis]

**Analyst(s)**: [Who conducted this threat model]

**Review Date**: [When this should be reviewed next, e.g., quarterly, after major changes]

---

### System Architecture

**Component Diagram**:

```
[User/Browser] ─── HTTPS ───> [Load Balancer] ─── HTTP ───> [Web Server]
                                                                   │
                                                                   │ JDBC
                                                                   ▼
                                                             [Database]
                                                                   │
                                                                   │
                                                                   ▼
                                                           [Backup Storage]
```

**Components**:

| Component | Technology | Purpose | Network Zone | Authentication Method |
|-----------|------------|---------|--------------|---------------------|
| [User/Browser] | Chrome/Safari/Firefox | End user interface | Public Internet | Session cookie |
| [Load Balancer] | AWS ALB | Traffic distribution, TLS termination | DMZ | N/A (no auth) |
| [Web Server] | Node.js/Express | Business logic, API endpoints | Private VPC | API key from LB |
| [Database] | PostgreSQL RDS | Persistent storage | Private subnet | DB credentials |
| [Backup Storage] | S3 bucket | Encrypted backups | AWS Region | IAM role |
| [Third-party service] | Stripe API | Payment processing | External | API secret key |

**Data Flows**:

1. **User Login**:  User → LB → Web Server → Database (credentials check) → Web Server → User (session token)
2. **Data Retrieval**: User → LB → Web Server → Database (query) → Web Server → User (JSON response)
3. **Payment**: User → LB → Web Server → Stripe API (payment token) → Webhook → Web Server → Database (order confirmation)
4. **Backup**: Database → S3 (nightly encrypted snapshot)

**External Dependencies**:

| Service | Purpose | Data Shared | Authentication | SLA/Criticality |
|---------|---------|-------------|----------------|-----------------|
| [Stripe] | Payment processing | Card tokens, customer IDs | API secret key | Critical (payment failures = revenue loss) |
| [SendGrid] | Email delivery | Email addresses, message content | API key | High (notifications) |
| [Datadog] | Monitoring/logging | Logs, metrics (may contain PII) | API key | Medium (observability) |

---

### Trust Boundaries

**Boundary 1: Public Internet → Load Balancer**
- **Data crossing**: HTTP requests (headers, body, query params)
- **Trust change**: Untrusted (anyone on Internet) → Trusted infrastructure
- **Controls**: TLS 1.2+, DDoS protection, rate limiting, Web Application Firewall (WAF)
- **Risk**: High (direct exposure to attackers)

**Boundary 2: Load Balancer → Web Server**
- **Data crossing**: HTTP requests (forwarded), source IP, X-Forwarded-For headers
- **Trust change**: DMZ → Private VPC
- **Controls**: Security groups (whitelist LB IPs), API key validation, input validation
- **Risk**: Medium (internal but accepts untrusted input)

**Boundary 3: Web Server → Database**
- **Data crossing**: SQL queries, query parameters
- **Trust change**: Application layer → Data layer
- **Controls**: Parameterized queries, connection pooling, DB credentials in secrets manager, least privilege grants
- **Risk**: High (SQL injection = full data compromise)

**Boundary 4: Web Server → Third-Party API (Stripe)**
- **Data crossing**: Payment tokens, customer data, order details
- **Trust change**: Internal → External (Stripe's control)
- **Controls**: HTTPS, API key rotation, minimal data sharing, audit logging of requests
- **Risk**: Medium (data leaves our control, reputational risk)

**Boundary 5: Database → Backup Storage (S3)**
- **Data crossing**: Encrypted database snapshots
- **Trust change**: Live database → Long-term storage
- **Controls**: AES-256 encryption at rest, bucket policies (private), versioning, lifecycle policies, cross-region replication
- **Risk**: Medium (exposure if misconfigured, compliance requirement)

**Boundary 6: Client-side (JavaScript) → Server-side (API)**
- **Data crossing**: User inputs, client-side state
- **Trust change**: User-controlled code → Server validation
- **Controls**: Server-side validation (never trust client), CSRF tokens, CSP headers, HttpOnly cookies
- **Risk**: High (client fully controlled by attacker)

---

### Data Classification

**Data Inventory**:

| Data Element | Classification | Compliance | Storage Location | Encryption | Retention |
|--------------|---------------|------------|------------------|------------|-----------|
| User passwords | Restricted | GDPR | Database | bcrypt hash (cost 12) | Until account deletion |
| Credit card numbers | Restricted (PCI) | PCI DSS Level 1 | Stripe (tokenized) | Stripe manages | Stripe retention policy |
| Email addresses | Confidential (PII) | GDPR, CAN-SPAM | Database, SendGrid | At rest: AES-256 | 7 years post-deletion |
| Order history | Confidential | GDPR | Database | At rest: AES-256 | 7 years (tax law) |
| Session tokens | Confidential | - | Redis, cookies | In transit: TLS | 24 hours |
| Audit logs | Internal | SOC 2 | Datadog, S3 | At rest: AES-256 | 1 year |
| API keys (3rd party) | Restricted | - | AWS Secrets Manager | Encrypted by SM | Rotated quarterly |
| User IP addresses | Internal (PII) | GDPR | Logs, analytics | At rest: AES-256 | 90 days |

**Classification Levels**:
- **Public**: Can be freely shared (marketing content, public documentation)
- **Internal**: For internal use, no external sharing (business metrics, roadmaps)
- **Confidential**: Sensitive, access controlled (PII, customer data)
- **Restricted**: Highly sensitive, strict access (credentials, PCI data, PHI)

**Compliance Requirements**:
- **GDPR**: Data minimization, consent management, right to deletion, breach notification (72 hours)
- **PCI DSS Level 1**: No storage of CVV, tokenization, quarterly ASV scans, annual audit
- **SOC 2 Type II**: Access controls, audit logging, change management, annual audit

---

### STRIDE Analysis

For each trust boundary, systematically apply all six STRIDE threat categories:

#### Boundary: Public Internet → Load Balancer

**S - Spoofing**
- **Threat**: Attacker spoofs user identity using stolen session cookies
- **Likelihood**: Medium (session cookies in browser storage vulnerable to XSS)
- **Impact**: High (full account access)
- **Mitigation**: HttpOnly + Secure + SameSite=Strict cookies, short session timeout (1 hour), IP binding, device fingerprinting
- **Status**: ✓ Implemented
- **Monitoring**: Alert on geo-impossible travel (login from US then China in 1 hour)

**T - Tampering**
- **Threat**: Man-in-the-middle attack modifies requests/responses
- **Likelihood**: Low (TLS widely enforced)
- **Impact**: High (data corruption, command injection)
- **Mitigation**: TLS 1.2+ enforced, HSTS header, certificate pinning (mobile), integrity checks on critical operations
- **Status**: ✓ Implemented
- **Monitoring**: Monitor TLS version usage, alert on downgrade attempts

**R - Repudiation**
- **Threat**: User denies making purchase, no audit trail
- **Likelihood**: Low (audit logging in place)
- **Impact**: Medium (dispute resolution, fraud)
- **Mitigation**: Comprehensive audit logging (user ID, timestamp, action, IP, user agent), immutable logs (S3 with object lock), digital signatures on transactions
- **Status**: ✓ Implemented
- **Monitoring**: Alert on log tampering, regular log integrity checks

**I - Information Disclosure**
- **Threat**: Verbose error messages reveal stack traces, database schema
- **Likelihood**: Medium (development errors in production)
- **Impact**: Medium (aids attacker reconnaissance)
- **Mitigation**: Generic error messages to users, detailed errors logged server-side only, security headers (X-Content-Type-Options, X-Frame-Options), no PII in URLs/logs
- **Status**: ⚠ Partial (need to audit error messages)
- **Monitoring**: Log analysis for stack traces in responses, alert on 500 errors

**D - Denial of Service**
- **Threat**: DDoS attack exhausts resources, site becomes unavailable
- **Likelihood**: Medium (e-commerce sites are targets)
- **Impact**: High (revenue loss, reputation)
- **Mitigation**: CloudFront CDN, AWS Shield Standard, WAF rate limiting (100 req/min per IP), auto-scaling, circuit breakers, resource quotas
- **Status**: ✓ Implemented
- **Monitoring**: Alert on traffic spikes (>10x baseline), track error rates, auto-scaling metrics

**E - Elevation of Privilege**
- **Threat**: Regular user gains admin access via authorization bypass
- **Likelihood**: Low (authorization checks in place)
- **Impact**: High (full system compromise)
- **Mitigation**: Role-based access control (RBAC), authorization check on every request, principle of least privilege, admin actions require re-authentication
- **Status**: ✓ Implemented
- **Monitoring**: Alert on privilege escalation attempts, admin action audit log

**Risk Score** (Likelihood × Impact):
- Spoofing: 2 × 3 = 6 (Medium)
- Tampering: 1 × 3 = 3 (Low)
- Repudiation: 1 × 2 = 2 (Low)
- Information Disclosure: 2 × 2 = 4 (Medium)
- Denial of Service: 2 × 3 = 6 (Medium)
- Elevation of Privilege: 1 × 3 = 3 (Low)

**Top Risks for This Boundary**: Session hijacking (Spoofing), DDoS (DoS), Information disclosure via errors

---

#### Boundary: Web Server → Database

**S - Spoofing**
- **Threat**: Attacker connects to database impersonating web server
- **Likelihood**: Very Low (internal network, firewall rules)
- **Impact**: High (full data access)
- **Mitigation**: Database credentials in AWS Secrets Manager (rotated), security groups (whitelist web server IPs only), IAM database authentication
- **Status**: ✓ Implemented
- **Monitoring**: Alert on new database connections from unexpected IPs, failed auth attempts

**T - Tampering**
- **Threat**: SQL injection modifies data, drops tables
- **Likelihood**: Medium (common vulnerability)
- **Impact**: Critical (data loss, corruption, exfiltration)
- **Mitigation**: Parameterized queries (ORM), input validation, least privilege DB user (no DROP/ALTER), read-only replicas for reporting, database backups
- **Status**: ⚠ Partial (manual code review needed for all SQL)
- **Monitoring**: Database audit log for DDL statements, unexpected UPDATE/DELETE volumes

**R - Repudiation**
- **Threat**: Database changes cannot be attributed to specific user
- **Likelihood**: Low (application logging in place)
- **Impact**: Low (audit, compliance)
- **Mitigation**: Application-level audit logging (user ID + action + timestamp), database query log (CloudWatch), immutable logs
- **Status**: ✓ Implemented
- **Monitoring**: Daily audit log integrity check

**I - Information Disclosure**
- **Threat**: Database dump exposed through misconfiguration, backup left public
- **Likelihood**: Medium (S3 misconfigurations common)
- **Impact**: Critical (full data breach)
- **Mitigation**: Encryption at rest (AES-256), encrypted backups, S3 bucket policies (private), no public snapshots, VPC endpoint for S3, data masking in non-prod
- **Status**: ✓ Implemented
- **Monitoring**: AWS Config rules for public S3 buckets, daily snapshot encryption check

**D - Denial of Service**
- **Threat**: Expensive queries exhaust database CPU/memory
- **Likelihood**: Medium (missing query optimization)
- **Impact**: High (site unavailable)
- **Mitigation**: Query timeouts (5s), connection pooling, read replicas, CloudWatch alarms on CPU (>80%), slow query log, query plan analysis
- **Status**: ✓ Implemented
- **Monitoring**: Alert on database CPU/memory, slow query log review weekly

**E - Elevation of Privilege**
- **Threat**: Web server DB user escalates to DBA privileges
- **Likelihood**: Very Low (IAM policies enforced)
- **Impact**: High (full database control)
- **Mitigation**: Least privilege DB grants (SELECT/INSERT/UPDATE only, no ALTER/DROP/GRANT), separate admin credentials, MFA for DB admin access
- **Status**: ✓ Implemented
- **Monitoring**: Alert on privilege grant operations, regular IAM policy audit

**Risk Score**:
- Tampering (SQL injection): 2 × 4 = 8 (High - Priority 1)
- Information Disclosure (backup exposure): 2 × 4 = 8 (High - Priority 1)
- Denial of Service (query exhaustion): 2 × 3 = 6 (Medium)
- Spoofing: 1 × 3 = 3 (Low)
- Repudiation: 1 × 1 = 1 (Low)
- Elevation of Privilege: 1 × 3 = 3 (Low)

**Top Risks for This Boundary**: SQL injection (Tampering), Backup exposure (Information Disclosure)

---

[Repeat STRIDE analysis for each trust boundary identified above]

---

### Mitigations & Monitoring

**Preventive Controls** (block attacks before they succeed):

| Control | Threats Mitigated | Implementation | Owner | Status |
|---------|-------------------|----------------|-------|--------|
| TLS 1.2+ enforcement | Tampering (MITM) | ALB listener policy | DevOps | ✓ Done |
| Parameterized queries | Tampering (SQLi) | ORM (Sequelize) | Engineering | ⚠ Partial |
| Input validation | Tampering, Injection | Joi schema validation | Engineering | ✓ Done |
| Rate limiting | DoS | WAF rules (100 req/min/IP) | DevOps | ✓ Done |
| CSRF tokens | Spoofing (CSRF) | csurf middleware | Engineering | ✓ Done |
| HttpOnly cookies | Spoofing (XSS → session theft) | Express cookie settings | Engineering | ✓ Done |
| Least privilege IAM | Elevation of Privilege | IAM policies | DevOps | ✓ Done |
| MFA for admin | Spoofing (credential theft) | AWS IAM MFA | DevOps | ✓ Done |
| Encryption at rest | Information Disclosure | RDS encryption, S3 default encryption | DevOps | ✓ Done |
| WAF (OWASP Top 10) | Multiple (SQLi, XSS, etc.) | AWS WAF managed rules | DevOps | ✓ Done |

**Detective Controls** (identify attacks in progress or after):

| Control | Detection Method | Alert Threshold | Incident Response | Owner | Status |
|---------|-----------------|----------------|-------------------|-------|--------|
| Failed login monitoring | CloudWatch Logs Insights | >5 failures in 5 min from same IP | Auto-block IP (24h), notify security team | DevOps | ✓ Done |
| SQL injection attempts | WAF logs + application logs | Any blocked SQLi pattern | Security review of attempted payload | Security | ✓ Done |
| Unusual data access | Database audit log | User accessing >1000 records in 1 min | Throttle user, security review | Engineering | ⚠ Partial |
| Privilege escalation attempts | Application audit log | Non-admin accessing admin endpoints | Block user, security review | Engineering | ✓ Done |
| Geo-impossible travel | Session activity log | Login from US then Asia <2 hours | Force re-auth, notify user | Engineering | ⚠ TODO |
| DDoS detection | CloudWatch metrics | Traffic >10x baseline | Engage AWS Shield Response Team | DevOps | ✓ Done |
| Backup integrity | S3 lifecycle checks | Missing daily backup | Page on-call, investigate | DevOps | ✓ Done |
| Secret rotation overdue | Secrets Manager | >90 days since rotation | Automated rotation, alert if fails | DevOps | ✓ Done |

**Corrective Controls** (respond to and recover from attacks):

| Scenario | Response Plan | Recovery Time Objective (RTO) | Recovery Point Objective (RPO) | Owner | Tested? |
|----------|--------------|-------------------------------|-------------------------------|-------|---------|
| Database compromise | Restore from backup, rotate credentials, forensic analysis | <4 hours | <24 hours (daily backups) | DevOps | ⚠ Last tested 6 months ago |
| DDoS attack | Enable AWS Shield Advanced, adjust WAF rules, failover to static site | <15 minutes | N/A | DevOps | ✓ Tested quarterly |
| Credential leak | Rotate all secrets, force password resets, revoke sessions, notify users | <1 hour | N/A | Security | ⚠ Runbook exists, not tested |
| Data breach | Incident response plan, legal notification, forensic preservation, public disclosure | <72 hours (GDPR) | N/A | Legal + Security | ⚠ Tabletop exercise needed |

---

### Risk Prioritization

**Risk Matrix** (Likelihood × Impact):

| Threat | Likelihood (1-5) | Impact (1-5) | Risk Score | Priority | Mitigation Status | Residual Risk |
|--------|------------------|--------------|------------|----------|-------------------|---------------|
| SQL injection | 3 (Medium) | 5 (Critical) | 15 | P0 (Critical) | Partial (manual review needed) | Medium |
| Backup exposure | 2 (Low) | 5 (Critical) | 10 | P1 (High) | Implemented | Low |
| Session hijacking | 3 (Medium) | 4 (High) | 12 | P1 (High) | Implemented | Medium |
| DDoS | 3 (Medium) | 4 (High) | 12 | P1 (High) | Implemented | Low |
| Info disclosure (errors) | 3 (Medium) | 2 (Medium) | 6 | P2 (Medium) | Partial | Medium |
| Credential stuffing | 2 (Low) | 4 (High) | 8 | P2 (Medium) | Implemented (rate limiting) | Low |
| CSRF | 2 (Low) | 3 (Medium) | 6 | P2 (Medium) | Implemented | Low |
| Query DoS | 2 (Low) | 3 (Medium) | 6 | P2 (Medium) | Implemented | Low |

**Top 3 Priorities**:
1. **SQL Injection (P0)**: Complete manual code review of all SQL queries, add automated SQLi detection in CI/CD
2. **Session Hijacking (P1)**: Implement geo-impossible travel detection, add device fingerprinting
3. **DDoS Protection (P1)**: Test Shield Advanced failover, document runbook

**Accepted Risks**:
- **CSRF on read-only endpoints**: Low impact (no state change), cost of tokens on every GET outweighs risk
- **Verbose logging in development**: Acceptable in dev/staging (not in production), aids debugging

---

### Action Items

| Action | Owner | Deadline | Priority | Status |
|--------|-------|----------|----------|--------|
| [Manual SQL code review for parameterized queries] | Engineering | 2 weeks | P0 | 🔴 Not Started |
| [Implement geo-impossible travel detection] | Engineering | 1 month | P1 | 🔴 Not Started |
| [Audit all error messages for information disclosure] | Engineering | 2 weeks | P2 | 🔴 Not Started |
| [Test database restore procedure] | DevOps | 1 week | P1 | 🟡 In Progress |
| [Tabletop exercise for data breach response] | Security + Legal | 1 month | P1 | 🔴 Not Started |
| [Document DDoS runbook and test] | DevOps | 2 weeks | P1 | 🟡 In Progress |
| [Rotate all API keys] | DevOps | Immediately | P0 | ✅ Done |

---

## Guidance for Each Section

**System Architecture**: Include visual diagram, technology stack (specific versions), network zones (DMZ/VPC/Internet), external dependencies (SaaS, APIs). Avoid vague descriptions.

**Data Classification**: Classify every element (public/internal/confidential/restricted), consult legal/compliance for PII/PHI/PCI, document retention and encryption. Don't forget data in logs/analytics/backups.

**STRIDE Application**: Apply all 6 categories to each boundary. Start with high-risk boundaries (user input, external integrations). Likelihood: 1=sophisticated attacker, 3=script kiddie, 5=trivial. Impact: 1=nuisance, 3=significant exposure, 5=complete compromise.

**Mitigation Status**: ✓ Implemented, ⚠ Partial, 🔴 TODO, ✅ Done

**Quality Checklist**: All components diagrammed | All boundaries analyzed | STRIDE on each boundary | All data classified | Mitigations mapped | Monitoring defined | Risks prioritized | Action items assigned | Assumptions documented | Review date set

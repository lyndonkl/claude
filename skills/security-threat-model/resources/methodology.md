# Security Threat Model: Advanced Methodologies

## Table of Contents
1. [Attack Trees & Attack Graphs](#1-attack-trees--attack-graphs)
2. [DREAD Risk Scoring](#2-dread-risk-scoring)
3. [Abuse Cases & Misuse Stories](#3-abuse-cases--misuse-stories)
4. [Data Flow Diagrams (DFD) for Threat Modeling](#4-data-flow-diagrams-dfd-for-threat-modeling)
5. [Threat Intelligence Integration](#5-threat-intelligence-integration)
6. [Advanced STRIDE Patterns](#6-advanced-stride-patterns)

## 1. Attack Trees & Attack Graphs

### Attack Tree Construction

**Attack tree**: Hierarchical diagram showing how security goals can be defeated through combinations of attacks.

**Structure**:
- **Root** (top): Attacker's goal (e.g., "Steal customer credit card data")
- **Nodes**: Sub-goals or attack steps
- **Leaves** (bottom): Atomic attacks (individual exploits)
- **AND nodes**: All child attacks must succeed (serial gates)
- **OR nodes**: Any child attack succeeds (parallel gates)

**Example (Steal Credit Card Data)**:
```
[Steal CC Data] (ROOT - OR)
├── [Compromise Database] (AND)
│   ├── [Gain network access] (OR)
│   │   ├── Phish employee for VPN creds
│   │   └── Exploit public-facing vulnerability
│   └── [Escalate privileges to DBA] (OR)
│       ├── SQL injection → shell → lateral movement
│       └── Steal DB credentials from secrets file
├── [Intercept in Transit] (AND)
│   ├── [MITM between user and server] (OR)
│   │   ├── Compromise WiFi router
│   │   └── BGP hijacking (sophisticated)
│   └── [Decrypt TLS] (OR)
│       ├── Steal server private key
│       └── Downgrade to weak cipher (if supported)
└── [Social Engineering] (OR)
    ├── Phish customer directly for CC
    └── Compromise customer support → access CC vault
```

**Leaf Attack Attributes**:
- **Difficulty**: Low (script kiddie), Medium (skilled attacker), High (APT)
- **Cost**: $0-100, $100-10K, $10K+ (attacker resources)
- **Detection Likelihood**: Low (0-30%), Medium (30-70%), High (70-100%)
- **Impact**: If this leaf succeeds, what's compromised?

**Analysis**:
- **Most likely path**: Lowest combined difficulty + cost
- **Stealthiest path**: Lowest combined detection likelihood
- **Critical leaves**: Appear in multiple paths (defend these first)

**Mitigation Strategy**:
- **Prune OR nodes**: Block at least one child (breaks that path)
- **Strengthen AND nodes**: Make any one child infeasible (breaks entire branch)
- **Monitor leaves**: Add detection at leaf level (early warning)

### Attack Graph Analysis

**Attack graph**: Network-level visualization showing how attacker moves laterally.

**Components**:
- **Nodes**: Network hosts (web server, DB, workstation)
- **Edges**: Exploits that allow movement between nodes
- **Entry points**: Internet-facing hosts (start nodes)
- **Crown jewels**: High-value targets (end nodes)

**Example**:
```
[Internet] → [Web Server] (SQLi) → [App Server] (lateral via shared subnet)
                                         ↓
                            [Database] (DB creds in config file)
```

**Path Analysis**:
- **Shortest path**: Fewest hops to crown jewels
- **Easiest path**: Lowest aggregate difficulty
- **Most likely path**: Attacker's expected route (probability-weighted)

**Mitigations**:
- **Network segmentation**: Break edges (VLANs, security groups, air gaps)
- **Least privilege**: Reduce accessible edges from each node
- **Defense in depth**: Require multiple successful exploits per path

## 2. DREAD Risk Scoring

**DREAD**: Microsoft's risk scoring model for prioritizing threats.

### Scoring Criteria (1-10 scale)

**D - Damage Potential**
- 1-3: Minor impact (single user affected, limited data)
- 4-7: Significant impact (many users, sensitive data)
- 8-10: Catastrophic (all users, regulated data breach, life-safety)

**R - Reproducibility**
- 1-3: Hard to reproduce (race condition, specific timing)
- 4-7: Moderate (requires specific configuration, some skill)
- 8-10: Trivial (works every time, no special conditions)

**E - Exploitability**
- 1-3: Very difficult (requires custom exploit, deep expertise)
- 4-7: Moderate (exploit code available, requires adaptation)
- 8-10: Trivial (point-and-click tool, no skill needed)

**A - Affected Users**
- 1-3: Minimal (single user, admin only, specific config)
- 4-7: Moderate (some users, default install, optional feature)
- 8-10: All users (default config, core functionality)

**D - Discoverability**
- 1-3: Obscure (requires source code audit, specific knowledge)
- 4-7: Moderate (found through scanning, disclosed vulnerability)
- 8-10: Obvious (visible in UI, publicly documented, automated scanners find it)

### Calculating DREAD Score

**Formula**: (Damage + Reproducibility + Exploitability + Affected Users + Discoverability) / 5

**Example (SQL Injection in Login Form)**:
- **Damage**: 10 (full database access, PII breach)
- **Reproducibility**: 10 (always works with same payload)
- **Exploitability**: 8 (SQLMap automates it, some skill needed)
- **Affected Users**: 10 (all users, login is core functionality)
- **Discoverability**: 9 (login forms are obvious attack surface, scanners find it)
- **DREAD Score**: (10+10+8+10+9)/5 = **9.4** (Critical)

**Example (Admin API without rate limiting)**:
- **Damage**: 7 (can enumerate accounts, some PII)
- **Reproducibility**: 10 (always works)
- **Exploitability**: 10 (trivial, just send requests)
- **Affected Users**: 6 (admin API, limited exposure)
- **Discoverability**: 5 (requires knowledge of API endpoint, not in public docs)
- **DREAD Score**: (7+10+10+6+5)/5 = **7.6** (High)

### Using DREAD for Prioritization

**Thresholds**:
- **9.0-10.0**: Critical (P0, fix immediately)
- **7.0-8.9**: High (P1, fix this sprint)
- **5.0-6.9**: Medium (P2, backlog priority)
- **3.0-4.9**: Low (P3, monitor, accept risk)
- **1.0-2.9**: Minimal (P4, informational)

**Advantages**:
- Quantitative scoring aids prioritization
- Granular (1-10 scale) vs. coarse (Low/Med/High)
- Factors in exploitability and discoverability (not just impact)

**Limitations**:
- Subjective (scorers may disagree)
- Doesn't account for existing mitigations (score pre-mitigation threat)
- "Discoverability" less relevant in post-disclosure world (assume all vulns are known)

## 3. Abuse Cases & Misuse Stories

### Abuse Cases

**Abuse case**: Scenario where functionality is misused for malicious purposes (not a bug, feature used as weapon).

**Structure**:
- **Actor**: Who abuses (insider, competitor, attacker)
- **Goal**: What they want (exfiltrate data, disrupt service, frame someone)
- **Preconditions**: What they need (account, network access, knowledge)
- **Steps**: How they abuse the feature
- **Result**: What damage occurs
- **Mitigation**: How to detect or prevent

**Example (Bulk Data Export Feature)**:

**Abuse Case**: Insider data exfiltration
- **Actor**: Disgruntled employee with valid credentials
- **Goal**: Steal entire customer database before leaving company
- **Preconditions**: Login access, export feature available to all users
- **Steps**:
  1. Log in with legitimate credentials
  2. Navigate to export page
  3. Select "All customers" (no pagination limit)
  4. Click "Export to CSV"
  5. Download 10M customer records
  6. Upload to competitor or dark web
- **Result**: Massive data breach, GDPR violation, competitive damage
- **Mitigation**:
  - **Detective**: Audit log for large exports, alert on exports >1000 records
  - **Preventive**: Require manager approval for exports >100 records
  - **Corrective**: Watermark exports with user ID (attribution), DLP to prevent upload

### Misuse Stories (Agile Format)

**Misuse story**: Agile user story from attacker's perspective.

**Format**: "As a [attacker type], I want to [malicious action], so that I can [attacker goal]"

**Example**:
- "As a **script kiddie**, I want to **enumerate valid usernames through password reset**, so that I can **target credential stuffing attacks**"
  - **Mitigation**: Generic error messages ("If that email exists, we sent a reset link"), rate limiting
- "As a **competitor**, I want to **scrape all product prices and descriptions**, so that I can **undercut pricing**"
  - **Mitigation**: Rate limiting, CAPTCHA, robots.txt, legal terms of service, API authentication
- "As a **disgruntled ex-employee**, I want to **use my old credentials that weren't revoked**, so that I can **delete critical data for revenge**"
  - **Mitigation**: Offboarding checklist (revoke all access day 1), audit logs, backups, immutable delete (soft delete with retention)

### Misuse Case Matrix

| Feature | Legitimate Use | Misuse | Mitigation |
|---------|----------------|--------|-----------|
| Search | Find products | Enumerate database, injection testing | Rate limiting, parameterized queries, no PII in results |
| File upload | Share documents | Malware upload, path traversal, storage DoS | File type validation (magic bytes), size limits, virus scan, separate domain |
| Admin panel | Manage system | Privilege escalation, mass data modification | Strong auth (MFA), audit logs, confirmation dialogs, IP whitelisting |
| API | Integrate systems | Credential theft, rate limit bypass, cost attacks | API key rotation, quota limits, cost caps, monitoring |
| Commenting | User feedback | Spam, XSS, phishing links, hate speech | Content filtering, CAPTCHA, XSS prevention (CSP), moderation queue |

## 4. Data Flow Diagrams (DFD) for Threat Modeling

### DFD Levels

**Level 0 (Context Diagram)**:
- High-level: System as single process, external entities only
- Use for: Executive overview, scope definition

**Level 1 (Major Components)**:
- Shows: Main processes, data stores, external entities, trust boundaries
- Use for: STRIDE analysis at component level

**Level 2+ (Detailed)**:
- Decomposes: Level 1 processes into sub-processes
- Use for: Deep dive on critical components (auth, payment, data handling)

### DFD Elements

**Symbols**:
- **External Entity** (rectangle): User, third-party service, external system
- **Process** (circle): Component that transforms data (web server, API, background job)
- **Data Store** (parallel lines): Database, file system, cache, queue
- **Data Flow** (arrow): Data moving between elements (HTTP request, DB query, file read)
- **Trust Boundary** (dotted line box): Security domain boundary

**Example (Login Flow - Level 1)**:
```
[User] ---(email, password)---> [Web Server] ---(credentials)---> [Database]
                                       |                              |
                                       |<--(user record, hashed pw)---|
                                       |
                                       |---(session token)---> [Redis Cache]
```

**Trust boundaries**:
- User ↔ Web Server (untrusted → trusted, validate all input)
- Web Server ↔ Database (application → data layer, parameterized queries)

### Applying STRIDE to DFD

**For each element type, ask specific STRIDE questions**:

**External Entity**:
- **Spoofing**: Can attacker impersonate this entity? (auth required?)
- **Repudiation**: Can entity deny actions? (audit logging?)

**Process**:
- **Tampering**: Can attacker modify process logic? (code signing, integrity checks?)
- **Information Disclosure**: Does process leak sensitive data in logs/errors?
- **Denial of Service**: Can attacker crash/exhaust this process?
- **Elevation of Privilege**: Can attacker gain higher permissions through this process?

**Data Store**:
- **Tampering**: Can attacker modify stored data? (access control, integrity checks?)
- **Information Disclosure**: Can attacker read sensitive data? (encryption at rest, access control?)
- **Denial of Service**: Can attacker fill/corrupt data store?

**Data Flow**:
- **Tampering**: Can attacker modify data in transit? (TLS, message signing?)
- **Information Disclosure**: Can attacker eavesdrop? (encryption in transit?)
- **Denial of Service**: Can attacker block/flood this flow?

### DFD-Based Threat Enumeration

**Systematic approach**:
1. Draw DFD with trust boundaries
2. Number each data flow (DF1, DF2, ...)
3. For each flow crossing trust boundary, apply STRIDE
4. For each process, apply STRIDE
5. For each data store with sensitive data, apply Tampering + Information Disclosure
6. Document threats in spreadsheet (DFD element, STRIDE category, threat description, mitigation)

**Example**:

| DFD Element | Trust Boundary | STRIDE | Threat | Likelihood | Impact | Mitigation |
|-------------|----------------|--------|--------|------------|--------|-----------|
| DF1: User → Web Server | Yes (external → internal) | Spoofing | CSRF attack using stolen session cookie | Medium | High | CSRF tokens, SameSite cookies |
| DF1: User → Web Server | Yes | Tampering | MITM modifies login request | Low | High | HTTPS, HSTS |
| P1: Web Server | No | Elevation of Privilege | SQLi escalates to admin via DB access | Medium | Critical | Parameterized queries, least privilege DB user |
| DS1: Database | No | Information Disclosure | Backup left public on S3 | Low | Critical | S3 bucket policy (private), encryption |

## 5. Threat Intelligence Integration

### MITRE ATT&CK Mapping

**MITRE ATT&CK**: Knowledge base of adversary tactics and techniques observed in real-world attacks.

**Tactics** (why): Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Exfiltration, Impact

**Example Mapping**:

| System Feature | ATT&CK Technique | Mitigation |
|----------------|------------------|-----------|
| Web application login | T1078 (Valid Accounts) | MFA, account lockout, monitoring |
| API with OAuth | T1550 (Use Alternate Authentication Material - token theft) | Short-lived tokens, token rotation, secure storage |
| File upload | T1105 (Ingress Tool Transfer - upload malware) | File type validation, virus scanning |
| Admin panel | T1078.003 (Valid Accounts: Local Accounts) | Principle of least privilege, MFA, audit logs |
| Database backups | T1530 (Data from Cloud Storage Object) | Encryption, private buckets, access logging |

**Using ATT&CK**:
- **Threat modeling input**: Browse ATT&CK for tactics relevant to your system (e.g., "Initial Access" for Internet-facing apps)
- **Red teaming**: Use ATT&CK techniques to simulate attacks during testing
- **Detection engineering**: Map ATT&CK techniques to monitoring rules (e.g., T1078 → alert on failed login spike)

### CVE/CWE Mapping

**CWE (Common Weakness Enumeration)**: Catalog of software weaknesses.

**Top CWEs** (CWE Top 25):
- CWE-79: Cross-Site Scripting (XSS)
- CWE-89: SQL Injection
- CWE-20: Improper Input Validation
- CWE-78: OS Command Injection
- CWE-190: Integer Overflow
- CWE-352: CSRF
- CWE-22: Path Traversal
- CWE-798: Hard-coded Credentials

**CVE (Common Vulnerabilities and Exposures)**: Specific vulnerabilities in specific products.

**Integration**:
- **Dependency scanning**: Identify CVEs in third-party libraries (npm audit, Snyk, Dependabot)
- **Patch management**: Prioritize CVEs with public exploits (CVSS ≥7.0, exploited in wild)
- **Threat model coverage**: Ensure threat model addresses CWE Top 25 for your language/framework

## 6. Advanced STRIDE Patterns

### STRIDE for Cloud Infrastructure

**Cloud-specific threats**:

**Spoofing**:
- **IAM role assumption**: Attacker assumes role with excessive permissions
- **Instance metadata service (IMDS)**: Attacker fetches IAM credentials from EC2 metadata
- **Mitigation**: Least privilege IAM, IMDSv2 (session-based), instance profile credential rotation

**Tampering**:
- **S3 bucket policy override**: Attacker modifies bucket to public
- **Security group modification**: Attacker opens firewall rules
- **Mitigation**: AWS Config rules (detect policy changes), SCPs (deny public access), CloudTrail alerts

**Information Disclosure**:
- **Public snapshot**: EBS/RDS snapshot left world-readable
- **CloudWatch Logs exposure**: Logs contain secrets, accessible to over-permissioned roles
- **Mitigation**: Automated snapshot encryption, secrets redaction in logs, least privilege CloudWatch access

**Denial of Service**:
- **Cost attack**: Attacker triggers expensive operations (Lambda invocations, data transfer)
- **Resource exhaustion**: Attacker fills S3 bucket, exhausts RDS connections
- **Mitigation**: Cost alarms, resource quotas, rate limiting

**Elevation of Privilege**:
- **Privilege escalation via misconfigured IAM**: Attacker modifies own permissions
- **Container escape**: Attacker breaks out of container to host
- **Mitigation**: IAM permission boundaries, pod security policies, AppArmor/SELinux

### STRIDE for APIs

**API-specific threats**:

**Spoofing**:
- **API key theft**: Hardcoded in client, extracted from mobile app
- **JWT forgery**: Weak secret, algorithm confusion (RS256 → HS256)
- **Mitigation**: API key rotation, secure storage (Keychain), strong JWT secrets (256-bit), algorithm whitelisting

**Tampering**:
- **Parameter tampering**: Modify user_id in request to access other user's data (IDOR)
- **Mass assignment**: Send unexpected fields to create admin users
- **Mitigation**: Authorization checks (verify user_id matches authenticated user), allowlist input fields

**Repudiation**:
- **No audit trail**: API calls not logged, can't prove who did what
- **Mitigation**: Comprehensive API logging (request ID, user ID, timestamp, endpoint, status)

**Information Disclosure**:
- **Over-fetching**: GraphQL query returns entire user object including PII
- **Verbose errors**: Stack traces reveal internal structure
- **Mitigation**: Field-level authorization (GraphQL), generic error messages to client

**Denial of Service**:
- **Query depth attack**: GraphQL query with 50 nested levels exhausts CPU
- **Rate limit bypass**: Distributed requests from many IPs
- **Mitigation**: Query depth limiting, query cost analysis, distributed rate limiting (Redis), CAPTCHA

**Elevation of Privilege**:
- **OAuth scope creep**: App requests excessive scopes, user approves without reading
- **Broken Object Level Authorization (BOLA)**: API doesn't check if user can access resource
- **Mitigation**: Minimal scopes (principle of least privilege), authorization middleware on every endpoint

### STRIDE for Mobile Apps

**Mobile-specific threats**:

**Spoofing**:
- **Jailbreak/root detection bypass**: Attacker modifies app to skip security checks
- **Certificate pinning bypass**: Attacker uses Frida to disable pinning, installs proxy cert
- **Mitigation**: Multiple anti-tamper checks, runtime integrity verification, server-side device attestation

**Tampering**:
- **Reverse engineering**: Attacker decompiles APK/IPA, finds hardcoded secrets
- **Mitigation**: ProGuard/R8 obfuscation (Android), app encryption (iOS), no secrets in client code (fetch from server)

**Information Disclosure**:
- **Insecure local storage**: SQLite DB unencrypted, accessible via device backup
- **Logging sensitive data**: Passwords/tokens in Logcat (Android) or Console (iOS)
- **Mitigation**: Keychain (iOS) / Keystore (Android), encrypted databases (SQLCipher), disable logging in production

**Denial of Service**:
- **Battery drain attack**: Malicious app or ad SDK consumes CPU/network
- **Mitigation**: Background task limits, network efficiency monitoring

**Elevation of Privilege**:
- **Permission escalation**: App tricks user into granting dangerous permissions
- **Mitigation**: Request permissions at time of use (just-in-time), explain why needed

---

## When to Use Advanced Methodologies

**Attack Trees**: Complex systems with many attack paths, need to prioritize defenses, red team planning

**DREAD Scoring**: Quantitative risk prioritization, limited security budget, need to justify spending to leadership

**Abuse Cases**: Feature-rich applications, insider threat modeling, compliance requirements (SOX, HIPAA audit trails)

**DFD-based STRIDE**: New system design (pre-implementation), comprehensive threat coverage, training junior security engineers

**Threat Intelligence (ATT&CK/CVE)**: Mature security programs, red team exercises, detection engineering, patch prioritization

**Cloud/API/Mobile STRIDE**: Specialized systems requiring domain-specific threat patterns

**Start simple** (basic STRIDE on trust boundaries), **add complexity as needed** (attack trees for critical paths, DREAD for prioritization).

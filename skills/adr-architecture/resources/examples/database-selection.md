# ADR-042: Use PostgreSQL for Primary Application Database

**Status:** Accepted
**Date:** 2024-01-15
**Deciders:** Backend team (Sarah, James, Alex), CTO (Michael), DevOps lead (Christine)
**Related ADRs:** ADR-015 (Data Model Design), ADR-051 (Read Replica Strategy - pending)

## Context

### Background
Our new SaaS platform for project management is scheduled to launch Q2 2024. We need to select a primary database that will store user data, projects, tasks, and collaboration information for the next 3-5 years.

Current situation:
- Prototype uses SQLite (clearly insufficient for production)
- Expected launch: 500 organizations, ~5,000 users
- Growth projection: 10,000 organizations, ~100,000 users within 18 months
- Data model is relational with complex queries (projects → tasks → subtasks → comments → attachments)

### Requirements

**Functional:**
- Support for complex relational queries with JOINs across 4-6 tables
- ACID transactions (critical for billing and permissions)
- Full-text search across project content
- JSON support for flexible metadata fields
- Row-level security for multi-tenant isolation

**Non-Functional:**
- Handle 10,000 QPS at launch (mostly reads)
- < 100ms p95 latency for queries
- 99.9% uptime SLA
- Support for read replicas (anticipated need at 50k+ QPS)
- Point-in-time recovery for disaster recovery

### Constraints
- Budget: $5,000/month maximum for database infrastructure
- Team expertise: Strong SQL experience, limited NoSQL experience
- Timeline: Must finalize in 2 weeks to stay on schedule
- Compliance: SOC 2 Type II required (data encryption at rest/transit)
- Existing stack: Node.js backend, React frontend, deploying on AWS

## Decision

We will use **PostgreSQL 15+** as our primary application database, hosted on AWS RDS with the following configuration:

**Infrastructure:**
- AWS RDS PostgreSQL 15.x
- Initially: db.r6g.xlarge instance (4 vCPU, 32GB RAM)
- Multi-AZ deployment for high availability
- Automated daily backups with 7-day retention
- Point-in-time recovery enabled

**Architecture:**
- Single primary database initially
- Prepared for read replicas when QPS exceeds 40k (anticipated 12-18 months)
- Connection pooling via PgBouncer (deployed on application servers)
- Row-Level Security (RLS) policies for multi-tenancy

**Scope:**
- All application data (users, organizations, projects, tasks)
- Session storage (using pgSession)
- Background job queue (using pg-boss)
- Excludes: Analytics data (separate data warehouse), file metadata (DynamoDB)

## Alternatives Considered

### MySQL 8.0
**Description:** Popular open-source relational database, strong AWS RDS support

**Pros:**
- Team has some MySQL experience
- Excellent AWS RDS integration
- Strong replication support
- Lower cost than commercial databases

**Cons:**
- Weaker JSON support compared to PostgreSQL (JSON functions less mature)
- Less robust constraint enforcement (e.g., CHECK constraints)
- Full-text search less powerful than PostgreSQL's
- InnoDB row-level locking can be problematic under high concurrency

**Why not chosen:** PostgreSQL's superior JSON support is critical for our flexible metadata requirements. Our data model has complex constraints that PostgreSQL handles more elegantly.

### MongoDB Atlas
**Description:** Managed NoSQL document database with flexible schema

**Pros:**
- Excellent horizontal scalability
- Flexible schema for evolving data model
- Strong JSON/document support
- Good full-text search

**Cons:**
- No multi-document ACID transactions (critical for our billing logic)
- Team has limited NoSQL experience (learning curve risk)
- Eventual consistency model incompatible with our requirements
- JOIN-like operations ($lookup) are slow and cumbersome
- More expensive at our scale (~$7k/month vs $3k for PostgreSQL)

**Why not chosen:** Lack of ACID transactions across documents is a dealbreaker for billing and permission changes. Our relational data model doesn't fit document paradigm well.

### Amazon Aurora PostgreSQL
**Description:** AWS's PostgreSQL-compatible database with performance enhancements

**Pros:**
- PostgreSQL compatibility with AWS optimizations
- Better read scaling (15 read replicas vs 5)
- Faster failover (< 30s vs 60-120s)
- Continuous backup to S3

**Cons:**
- 20-30% more expensive than RDS PostgreSQL
- Some PostgreSQL extensions not supported
- Vendor lock-in to AWS (harder to migrate to other clouds)
- Adds complexity we don't need yet

**Why not chosen:** Premium cost not justified at our current scale. Standard RDS PostgreSQL meets our needs. We can migrate to Aurora later if needed (minimal code changes).

### CockroachDB
**Description:** Distributed SQL database with PostgreSQL compatibility

**Pros:**
- Horizontal scalability built-in
- Multi-region support for global deployment
- PostgreSQL wire protocol compatibility
- Strong consistency guarantees

**Cons:**
- Significantly more complex to operate (distributed systems expertise needed)
- Higher latency for single-region workloads (consensus overhead)
- Limited ecosystem compared to PostgreSQL
- Team has zero distributed database experience
- More expensive (~2-3x cost of RDS PostgreSQL)

**Why not chosen:** Operational complexity far exceeds our current needs. We're a single-region deployment for the foreseeable future. Can revisit if we expand globally.

## Consequences

### Benefits

**Strong Data Integrity:**
- ACID transactions ensure billing accuracy and permission consistency
- Robust constraint enforcement catches data errors at write-time
- Foreign keys prevent orphaned records

**Excellent Query Capabilities:**
- Complex JOINs perform well with proper indexing
- Window functions enable sophisticated analytics
- CTEs (Common Table Expressions) simplify complex query logic
- Full-text search with GIN indexes for project content search

**JSON Flexibility:**
- JSONB type allows flexible metadata without schema migrations
- JSON operators enable querying nested structures efficiently
- Balances schema enforcement (relations) with flexibility (JSON)

**Team Productivity:**
- Team's SQL expertise means fast development velocity
- Mature ORM support (Sequelize, TypeORM) accelerates development
- Extensive community resources and documentation
- Familiar debugging and optimization tools

**Operational Maturity:**
- AWS RDS handles backups, patching, monitoring automatically
- Point-in-time recovery provides disaster recovery
- Multi-AZ deployment ensures high availability
- Well-understood scaling path (read replicas, connection pooling)

**Cost Efficiency:**
- Estimated $3,000/month at launch scale (db.r6g.xlarge + storage)
- Scales to ~$8,000/month with read replicas (at 100k users)
- Well within $5k/month budget initially

### Drawbacks

**Vertical Scaling Limits:**
- Single primary database limits write throughput to one instance
- At ~50-60k QPS, will need read replicas (adds operational complexity)
- Ultimate write limit around 100k QPS even with largest instance
- Mitigation: Implement caching (Redis) for read-heavy workloads

**Sharding Complexity:**
- Horizontal partitioning (sharding) is manual and complex
- If we exceed single-instance limits, migration to sharded setup is expensive
- Not as straightforward as DynamoDB or Cassandra for horizontal scaling
- Mitigation: Monitor growth carefully; consider Aurora or CockroachDB if needed

**Replication Lag:**
- Read replicas have eventual consistency (typically 10-100ms lag)
- Application must handle stale reads if using replicas
- Some queries must route to primary for consistency
- Mitigation: Use replicas only for analytics and non-critical reads

**Backup Window:**
- Automated backups cause brief I/O pause (usually < 5s)
- Scheduled during low-traffic window (3-4 AM PST)
- Multi-AZ deployment minimizes impact
- Mitigation: Accept brief latency spike during backup window

### Risks

**Performance Bottleneck:**
- **Risk:** Single database becomes bottleneck before we implement read replicas
- **Likelihood:** Medium (depends on growth rate)
- **Mitigation:** Implement aggressive caching (Redis) for frequently accessed data; monitor QPS weekly; prepare read replica configuration in advance

**Data Migration Challenges:**
- **Risk:** If we need to migrate to different database, data size makes migration slow
- **Likelihood:** Low (PostgreSQL should serve us for 3-5 years)
- **Mitigation:** Regularly test backup/restore procedures; maintain clear data export processes

**Team Scaling:**
- **Risk:** As team grows, need to train new hires on PostgreSQL specifics (RLS, JSONB)
- **Likelihood:** High (we plan to grow team)
- **Mitigation:** Document database patterns; create onboarding materials; conduct code reviews

### Trade-offs Accepted

**Trading horizontal scalability for operational simplicity:** We're choosing a database that's simple to operate now but harder to scale horizontally later, accepting that we may need to re-architect in 3-5 years if we grow beyond single-instance limits.

**Trading NoSQL flexibility for data integrity:** We're prioritizing ACID guarantees and relational integrity over schema flexibility, accepting that schema migrations will be required for data model changes.

**Trading vendor portability for convenience:** AWS RDS lock-in is acceptable given the operational benefits. We could migrate to other managed PostgreSQL services (Google Cloud SQL, Azure) if needed, though with effort.

## Implementation

### Rollout Plan

**Phase 1: Setup (Week 1-2)**
- Provision AWS RDS PostgreSQL instance
- Configure VPC security groups and IAM roles
- Set up automated backups and monitoring
- Configure PgBouncer connection pooling

**Phase 2: Migration (Week 3-4)**
- Migrate schema from SQLite prototype
- Load seed data and test data
- Performance test with simulated load
- Configure monitoring alerts (CloudWatch, Datadog)

**Phase 3: Launch (Q2 2024)**
- Deploy to production
- Monitor query performance and optimize slow queries
- Weekly capacity review for first 3 months

### Success Criteria

**Technical:**
- p95 query latency < 100ms (measured via APM)
- Zero data integrity issues in first 6 months
- 99.9% uptime achieved

**Operational:**
- Team can confidently make schema changes
- Backup/restore tested and verified monthly
- On-call incidents < 2 per month related to database

**Business:**
- Database costs remain under $5k/month through 10k users
- Support 100k users without re-architecture

### Future Considerations

**Short-term (3-6 months):**
- Implement Redis caching for hot data paths
- Tune connection pool settings based on actual load
- Create read-only database user for analytics

**Medium-term (6-18 months):**
- Add read replicas when QPS exceeds 40k
- Implement query result caching
- Consider Aurora migration if cost-benefit justifies

**Long-term (18+ months):**
- Evaluate sharding strategy if approaching single-instance limits
- Consider multi-region deployment for global users
- Explore specialized databases for specific workloads (e.g., time-series data)

## References

- [PostgreSQL 15 Release Notes](https://www.postgresql.org/docs/15/release-15.html)
- [AWS RDS PostgreSQL Best Practices](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html)
- [Internal: Database Performance Requirements Doc](https://docs.internal/db-requirements)
- [Internal: Load Testing Results](https://docs.internal/load-test-2024-01)
- [Benchmark: PostgreSQL vs MySQL JSON Performance](https://www.enterprisedb.com/postgres-tutorials/postgresql-vs-mysql-json-performance)

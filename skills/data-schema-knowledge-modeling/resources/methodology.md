# Data Schema & Knowledge Modeling: Advanced Methodology

## Workflow

```
Advanced Schema Modeling:
- [ ] Step 1: Analyze complex domain patterns
- [ ] Step 2: Design advanced relationship structures
- [ ] Step 3: Apply normalization or strategic denormalization
- [ ] Step 4: Model temporal/historical aspects
- [ ] Step 5: Plan schema evolution strategy
```

**Steps:** (1) Identify patterns in [Advanced Relationships](#1-advanced-relationship-patterns), (2) Apply [Hierarchy](#2-hierarchy-modeling) and [Polymorphic](#3-polymorphic-associations) patterns, (3) Use [Normalization](#4-normalization-levels) then [Denormalization](#5-strategic-denormalization), (4) Add [Temporal](#6-temporal--historical-modeling) if needed, (5) Plan [Evolution](#7-schema-evolution).

---

## 1. Advanced Relationship Patterns

### Self-Referential

Entity relates to itself (org charts, categories, social networks).

```sql
CREATE TABLE Employee (
  id BIGINT PRIMARY KEY,
  managerId BIGINT NULL REFERENCES Employee(id),
  CONSTRAINT no_self_ref CHECK (id != managerId)
);
```

Query with recursive CTE for full hierarchy.

### Conditional

Relationship exists only under conditions.

```sql
CREATE TABLE Order (
  id BIGINT PRIMARY KEY,
  status VARCHAR(20),
  paymentId BIGINT NULL REFERENCES Payment(id),
  CONSTRAINT payment_when_paid CHECK (
    (status IN ('paid','completed') AND paymentId IS NOT NULL) OR
    (status NOT IN ('paid','completed'))
  )
);
```

### Multi-Parent

Entity has multiple parents (document in folders).

```sql
CREATE TABLE DocumentFolder (
  documentId BIGINT REFERENCES Document(id),
  folderId BIGINT REFERENCES Folder(id),
  PRIMARY KEY (documentId, folderId)
);
```

---

## 2. Hierarchy Modeling

Four approaches with trade-offs:

| Approach | Implementation | Read | Write | Best For |
|----------|---------------|------|-------|----------|
| **Adjacency List** | `parentId` column | Slow (recursive) | Fast | Shallow trees, frequent updates |
| **Path Enumeration** | `path VARCHAR` ('/1/5/12/') | Fast | Medium | Read-heavy, moderate depth |
| **Nested Sets** | `lft, rgt INT` | Fastest | Slow | Read-heavy, rare writes |
| **Closure Table** | Separate ancestor/descendant table | Fastest | Medium | Complex queries, any depth |

**Adjacency List:**
```sql
CREATE TABLE Category (
  id BIGINT PRIMARY KEY,
  parentId BIGINT NULL REFERENCES Category(id)
);
```

**Closure Table:**
```sql
CREATE TABLE CategoryClosure (
  ancestor BIGINT,
  descendant BIGINT,
  depth INT,  -- 0=self, 1=child, 2+=deeper
  PRIMARY KEY (ancestor, descendant)
);
```

**Recommendation:** Adjacency for < 5 levels, Closure for complex queries.

---

## 3. Polymorphic Associations

Entity relates to multiple types (Comment on Post/Photo/Video).

### Approach 1: Separate FKs (Recommended for SQL)

```sql
CREATE TABLE Comment (
  id BIGINT PRIMARY KEY,
  postId BIGINT NULL REFERENCES Post(id),
  photoId BIGINT NULL REFERENCES Photo(id),
  videoId BIGINT NULL REFERENCES Video(id),
  CONSTRAINT one_parent CHECK (
    (postId IS NOT NULL)::int +
    (photoId IS NOT NULL)::int +
    (videoId IS NOT NULL)::int = 1
  )
);
```

**Pros:** Type-safe, referential integrity
**Cons:** Schema grows with types

### Approach 2: Supertype/Subtype

```sql
CREATE TABLE Commentable (id BIGINT PRIMARY KEY, type VARCHAR(50));
CREATE TABLE Post (id BIGINT PRIMARY KEY REFERENCES Commentable(id), ...);
CREATE TABLE Photo (id BIGINT PRIMARY KEY REFERENCES Commentable(id), ...);
CREATE TABLE Comment (commentableId BIGINT REFERENCES Commentable(id));
```

**Use when:** Shared attributes across types.

---

## 4. Graph & Ontology Design

### Property Graph

**Nodes** = entities, **Edges** = relationships, both have properties.

```cypher
CREATE (u:User {id: 1, name: 'Alice'})
CREATE (p:Product {id: 100, name: 'Widget'})
CREATE (u)-[:PURCHASED {date: '2024-01-15', quantity: 2}]->(p)
```

**Schema:**
```
Nodes: User, Product, Category
Edges: PURCHASED (User→Product, {date, quantity})
       REVIEWED (User→Product, {rating, comment})
       BELONGS_TO (Product→Category)
```

**Design principles:**
- Nodes for entities with identity
- Edges for relationships
- Properties on edges for context
- Avoid deep traversals (< 3 hops)

### RDF Triples (Semantic Web)

Subject-Predicate-Object:
```turtle
ex:Alice rdf:type ex:User .
ex:Alice ex:purchased ex:Widget .
```

**Use RDF when:** Standards compliance, semantic reasoning, linked data
**Use Property Graph when:** Performance, complex traversals

---

## 5. Normalization Levels

### 1NF: Atomic Values

**Violation:** Multiple phones in one column
**Fix:** Separate UserPhone table

### 2NF: No Partial Dependencies

**Violation:** In OrderItem(orderId, productId, productName), productName depends only on productId
**Fix:** productName lives in Product table

### 3NF: No Transitive Dependencies

**Violation:** In Address(id, zipCode, city, state), city/state depend on zipCode
**Fix:** Separate ZipCode table

**When to normalize to 3NF:** OLTP, frequent updates, consistency required

---

## 6. Strategic Denormalization

**Only after profiling shows bottleneck.**

### Pattern 1: Computed Aggregates

Store `Order.total` instead of summing OrderItems on every query.

**Trade-off:** Faster reads, slower writes, consistency risk (use triggers/app logic)

### Pattern 2: Frequent Joins

Embed address fields in User table to avoid join.

**Trade-off:** No join, but updates must maintain both

### Pattern 3: Historical Snapshots

```sql
CREATE TABLE OrderSnapshot (
  orderId BIGINT,
  snapshotDate DATE,
  userName VARCHAR(255),  -- denormalized from User
  userEmail VARCHAR(255),
  PRIMARY KEY (orderId, snapshotDate)
);
```

**Use when:** Need point-in-time data (e.g., user's name at time of order)

---

## 7. Temporal & Historical Modeling

### Pattern 1: Effective Dating

```sql
CREATE TABLE Price (
  productId BIGINT,
  price DECIMAL(10,2),
  effectiveFrom DATE NOT NULL,
  effectiveTo DATE NULL,  -- NULL = current
  PRIMARY KEY (productId, effectiveFrom)
);
```

**Query current:** WHERE effectiveFrom <= TODAY AND (effectiveTo IS NULL OR effectiveTo > TODAY)

### Pattern 2: History Table

```sql
CREATE TABLE UserHistory (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  userId BIGINT,
  email VARCHAR(255),
  name VARCHAR(255),
  validFrom TIMESTAMP DEFAULT NOW(),
  validTo TIMESTAMP NULL,
  changeType VARCHAR(20)  -- 'INSERT', 'UPDATE', 'DELETE'
);
```

Trigger on User table inserts into UserHistory on changes.

### Pattern 3: Event Sourcing

```sql
CREATE TABLE OrderEvent (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  orderId BIGINT,
  eventType VARCHAR(50),  -- 'CREATED', 'ITEM_ADDED', 'SHIPPED'
  eventData JSON,
  occurredAt TIMESTAMP DEFAULT NOW()
);
```

Reconstruct state by replaying events.

**Trade-offs:**
**Pros:** Complete audit, time travel
**Cons:** Query complexity, storage

---

## 8. Schema Evolution

### Strategy 1: Backward-Compatible

Safe changes (no app changes):
- Add nullable column
- Add table (not referenced)
- Add index
- Widen column (VARCHAR(100) → VARCHAR(255))

```sql
ALTER TABLE User ADD COLUMN phoneNumber VARCHAR(20) NULL;
```

### Strategy 2: Expand-Contract

For breaking changes:

1. **Expand:** Add new alongside old
   ```sql
   ALTER TABLE User ADD COLUMN newEmail VARCHAR(255) NULL;
   ```

2. **Migrate:** Copy data
   ```sql
   UPDATE User SET newEmail = email WHERE newEmail IS NULL;
   ```

3. **Contract:** Remove old
   ```sql
   ALTER TABLE User DROP COLUMN email;
   ALTER TABLE User RENAME COLUMN newEmail TO email;
   ```

### Strategy 3: Versioned Schemas (NoSQL)

```json
{"_schemaVersion": "2.0", "email": "alice@example.com"}
```

App handles multiple versions.

### Strategy 4: Blue-Green

Run old and new schemas simultaneously, dual-write, migrate, switch reads, remove old.

**Best for:** Major redesigns, zero downtime

---

## 9. Multi-Tenancy

### Pattern 1: Separate Databases

```
tenant1_db, tenant2_db, tenant3_db
```

**Pros:** Strong isolation
**Cons:** High overhead

### Pattern 2: Separate Schemas

```sql
CREATE SCHEMA tenant1;
CREATE TABLE tenant1.User (...);
```

**Pros:** Better than separate DBs
**Cons:** Still some overhead

### Pattern 3: Shared Schema + Tenant ID

```sql
CREATE TABLE User (
  id BIGINT PRIMARY KEY,
  tenantId BIGINT NOT NULL,
  email VARCHAR(255),
  UNIQUE (tenantId, email)
);
```

**Pros:** Most efficient
**Cons:** Must filter ALL queries by tenantId

**Recommendation:** Pattern 3 for SaaS, Pattern 1 for regulated industries

---

## 10. Performance

### Indexes

**Covering index** (includes all query columns):
```sql
CREATE INDEX idx_user_status ON User(status) INCLUDE (name, email);
```

**Composite index** (order matters):
```sql
-- Good for: WHERE tenantId = X AND createdAt > Y
CREATE INDEX idx_tenant_date ON Order(tenantId, createdAt);
```

**Partial index** (reduce size):
```sql
CREATE INDEX idx_active ON User(email) WHERE deletedAt IS NULL;
```

### Partitioning

**Horizontal (sharding):**
```sql
CREATE TABLE Order (...) PARTITION BY RANGE (createdAt);
CREATE TABLE Order_2024_Q1 PARTITION OF Order
  FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
```

**Vertical:** Split hot/cold data into separate tables.

---

## 11. Common Advanced Patterns

### Soft Deletes

```sql
ALTER TABLE User ADD COLUMN deletedAt TIMESTAMP NULL;
-- Query: WHERE deletedAt IS NULL
```

### Audit Columns

```sql
createdAt TIMESTAMP DEFAULT NOW()
updatedAt TIMESTAMP DEFAULT NOW() ON UPDATE NOW()
createdBy BIGINT REFERENCES User(id)
updatedBy BIGINT REFERENCES User(id)
```

### State Machines

```sql
CREATE TABLE OrderState (
  orderId BIGINT REFERENCES Order(id),
  state VARCHAR(20),
  transitionedAt TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (orderId, transitionedAt)
);
-- Track: draft → pending → confirmed → shipped → delivered
```

### Idempotency Keys

```sql
CREATE TABLE Request (
  idempotencyKey UUID PRIMARY KEY,
  payload JSON,
  result JSON,
  processedAt TIMESTAMP
);
-- Prevents duplicate processing
```

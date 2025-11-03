# Data Schema & Knowledge Modeling Template

## Workflow

Copy this checklist and track your progress:

```
Data Schema & Knowledge Modeling Progress:
- [ ] Step 1: Gather domain requirements and scope
- [ ] Step 2: Identify entities and attributes systematically
- [ ] Step 3: Define relationships and cardinality
- [ ] Step 4: Specify constraints and invariants
- [ ] Step 5: Validate against use cases and document
```

**Step 1: Gather domain requirements and scope**

Ask user for domain description, core use cases, existing data sources, scale requirements, and technology stack. Use [Input Questions](#input-questions).

**Step 2: Identify entities and attributes systematically**

Extract entities from requirements using [Entity Identification](#entity-identification). Define attributes with types and nullability using [Attribute Guide](#attribute-guide).

**Step 3: Define relationships and cardinality**

Map entity connections using [Relationship Mapping](#relationship-mapping). Specify cardinality (1:1, 1:N, M:N) and optionality.

**Step 4: Specify constraints and invariants**

Define business rules and constraints using [Constraint Specification](#constraint-specification). Document domain invariants.

**Step 5: Validate against use cases and document**

Create `data-schema-knowledge-modeling.md` using [Template](#schema-documentation-template). Verify using [Validation Checklist](#validation-checklist).

---

## Input Questions

**Domain & Scope:**
- What domain? (e-commerce, healthcare, social network)
- Boundaries? In/out of scope?
- Existing schemas to integrate/migrate from?

**Core Use Cases:**
- Primary operations? (CRUD for which entities?)
- Required queries/reports?
- Access patterns? (read-heavy, write-heavy, mixed)

**Scale & Performance:**
- Data volume? (rows per table, storage)
- Growth rate? (daily/monthly)
- Performance SLAs?

**Technology:**
- Database? (PostgreSQL, MongoDB, Neo4j, etc.)
- Compliance? (GDPR, HIPAA, SOC2)
- Evolution needs? (schema versioning, migrations)

---

## Entity Identification

**Step 1: Extract nouns**

List nouns from requirements = candidate entities.

**Step 2: Validate**

For each, check:
- [ ] Distinct identity? (can point to "this specific X")
- [ ] Independent lifecycle?
- [ ] Multiple attributes beyond name?
- [ ] Track multiple instances?

**Keep** if yes to most. **Reject** if just an attribute.

**Step 3: Entity vs Value Object**

- **Entity**: Has ID, mutable (User, Order)
- **Value Object**: No ID, immutable (Address, Money)

**Step 4: Document**

```markdown
### Entity: [Name]
**Purpose:** [What it represents]
**Examples:** [2-3 concrete cases]
**Lifecycle:** [Creation → deletion]
**Invariants:** [Rules that must hold]
```

---

## Attribute Guide

**Template:**
```
attributeName: DataType [NULL|NOT NULL] [DEFAULT value]
  - Description: [What it represents]
  - Validation: [Constraints]
  - Examples: [Sample values]
```

**Standard attributes:**
- `id`: Primary key (UUID/BIGINT)
- `createdAt`: TIMESTAMP NOT NULL
- `updatedAt`: TIMESTAMP NOT NULL
- `deletedAt`: TIMESTAMP NULL (soft deletes)

**Data types:**

| Data | SQL | NoSQL | Notes |
|------|-----|-------|-------|
| Short text | VARCHAR(N) | String | Specify max |
| Long text | TEXT | String | No limit |
| Integer | INT/BIGINT | Number | Choose size |
| Decimal | DECIMAL(P,S) | Number | Fixed precision |
| Money | DECIMAL(19,4) | {amount,currency} | Never FLOAT |
| Boolean | BOOLEAN | Boolean | Not nullable |
| Date/Time | TIMESTAMP | ISODate | With timezone |
| UUID | UUID/CHAR(36) | String | Distributed IDs |
| JSON | JSON/JSONB | Object | Flexible |
| Enum | ENUM/VARCHAR | String | Fixed values |

**Nullability:**
- NOT NULL if required
- NULL if optional/unknown at creation
- Avoid NULL for booleans

---

## Relationship Mapping

**Cardinality:**

**1:1** - User has one Profile
- SQL: `Profile.userId UNIQUE NOT NULL REFERENCES User(id)`

**1:N** - User has many Orders
- SQL: `Order.userId NOT NULL REFERENCES User(id)`

**M:N** - Order contains Products
- Junction table:
  ```sql
  OrderItem (
    orderId REFERENCES Order(id),
    productId REFERENCES Product(id),
    quantity INT NOT NULL,
    PRIMARY KEY (orderId, productId)
  )
  ```

**Optionality:**
- Required: NOT NULL
- Optional: NULL

**Naming:**
Use verbs: User **owns** Order, Product **belongs to** Category

---

## Constraint Specification

**Primary Keys:**
```sql
id BIGINT PRIMARY KEY AUTO_INCREMENT
-- or --
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
```

**Unique:**
```sql
email VARCHAR(255) UNIQUE NOT NULL
UNIQUE (userId, productId)  -- composite
```

**Foreign Keys:**
```sql
userId BIGINT NOT NULL REFERENCES User(id) ON DELETE CASCADE
-- Options: CASCADE, SET NULL, RESTRICT
```

**Check Constraints:**
```sql
price DECIMAL(10,2) CHECK (price >= 0)
status VARCHAR(20) CHECK (status IN ('draft','pending','completed'))
```

**Domain Invariants:**

Document business rules:
```markdown
### Invariant: Order total = sum of items
Order.total = SUM(OrderItem.quantity * OrderItem.price)

### Invariant: Unique email
No duplicate emails (case-insensitive)
```

Enforce via: DB constraints (preferred), application logic, or triggers.

---

## Schema Documentation Template

Create: `data-schema-knowledge-modeling.md`

**Required sections:**

1. **Domain Overview** - Purpose, scope, technology
2. **Use Cases** - Primary operations, query patterns
3. **Entity Definitions** - For each entity:
   - Purpose, examples, lifecycle
   - Attributes table (name, type, null, default, constraints, description)
   - Relationships (cardinality, FK, optionality)
   - Invariants
4. **ERD** - Visual/text diagram showing relationships
5. **Constraints** - DB constraints, domain invariants
6. **Normalization** - Level, denormalization decisions
7. **Implementation** - SQL DDL / JSON Schema / Graph schema as appropriate
8. **Validation** - Check each use case is supported
9. **Open Questions** - Unresolved decisions

**Example entity definition:**

```markdown
### Entity: Order

**Purpose:** Represents customer purchase transaction
**Examples:** Amazon order #123, Shopify order #456
**Lifecycle:** Created on checkout → Updated during fulfillment → Completed on delivery

#### Attributes

| Attribute | Type | Null? | Default | Constraints | Description |
|---|---|---|---|---|---|
| id | BIGINT | NO | auto | PK | Unique identifier |
| userId | BIGINT | NO | - | FK→User | Customer who placed order |
| status | VARCHAR(20) | NO | 'pending' | CHECK IN(...) | Order status |
| total | DECIMAL(10,2) | NO | - | CHECK >= 0 | Order total |

#### Relationships
- **belongs to:** 1:N with User (Order.userId → User.id)
- **contains:** 1:N with OrderItem junction table

#### Invariants
- total = SUM(OrderItem.quantity * OrderItem.price)
- status transitions: pending → confirmed → shipped → delivered
```

---

## Validation Checklist

**Completeness:**
- [ ] All entities identified
- [ ] All attributes defined (types, nullability)
- [ ] All relationships mapped (cardinality)
- [ ] All constraints specified
- [ ] All invariants documented

**Correctness:**
- [ ] Each entity distinct purpose
- [ ] No redundant entities
- [ ] Attributes in correct entities
- [ ] Cardinality reflects reality
- [ ] Constraints enforce rules

**Use Case Coverage:**
- [ ] Supports all CRUD operations
- [ ] All queries answerable
- [ ] Indexes planned
- [ ] No missing joins

**Normalization:**
- [ ] No partial dependencies (2NF)
- [ ] No transitive dependencies (3NF)
- [ ] Denormalization documented
- [ ] No update anomalies

**Technical Quality:**
- [ ] Consistent naming
- [ ] Appropriate data types
- [ ] Primary keys defined
- [ ] Foreign keys maintain integrity
- [ ] Soft delete strategy (if needed)
- [ ] Audit fields (if needed)

**Future-Proofing:**
- [ ] Schema extensible
- [ ] Migration path (if applicable)
- [ ] Versioning strategy
- [ ] No technical debt

---

## Common Pitfalls

**1. Modeling implementation, not domain**
- Symptom: Entities like "UserSession", "Cache"
- Fix: Model real-world concepts only

**2. God entities**
- Symptom: User with 50+ attributes
- Fix: Extract to separate entities

**3. Missing junction tables**
- Symptom: M:N with FKs
- Fix: Always use junction table

**4. Nullable FKs without reason**
- Symptom: All relationships optional
- Fix: NOT NULL unless truly optional

**5. Not enforcing invariants**
- Symptom: Rules in docs only
- Fix: CHECK constraints, triggers, app validation

**6. Premature denormalization**
- Symptom: Duplicating without measurement
- Fix: Normalize first, denormalize after profiling

**7. Wrong data types**
- Symptom: Money as VARCHAR
- Fix: DECIMAL for money, proper types for all

**8. No migration strategy**
- Symptom: Can't change schema
- Fix: Versioning, backward-compat changes

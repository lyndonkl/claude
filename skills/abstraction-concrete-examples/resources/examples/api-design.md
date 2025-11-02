# Abstraction Ladder Example: API Design

## Topic: RESTful API Design

## Overview
This ladder shows how abstract API design principles translate into concrete implementation decisions for a user management endpoint.

## Abstraction Levels

### Level 1 (Most Abstract): Universal Principle
**"Interfaces should be intuitive, consistent, and predictable"**

This applies to all interfaces: APIs, UI, command-line tools, hardware controls. Users should be able to predict behavior based on consistent patterns.

### Level 2: Framework & Standards
**"Follow REST architectural constraints and HTTP semantics"**

RESTful design provides standardized patterns:
- Resources identified by URIs
- Stateless communication
- Standard HTTP methods (GET, POST, PUT, DELETE)
- Appropriate status codes
- HATEOAS (where applicable)

### Level 3: Approach & Patterns
**"Design resource-oriented endpoints with predictable CRUD operations"**

Concrete patterns:
- Use nouns for resources, not verbs
- Plural resource names
- Nested resources show relationships
- Query parameters for filtering/pagination
- Consistent error response format

### Level 4: Specific Implementation
**"User management API with standard CRUD endpoints"**

```
GET    /api/v1/users          # List all users
GET    /api/v1/users/:id      # Get specific user
POST   /api/v1/users          # Create user
PUT    /api/v1/users/:id      # Update user (full)
PATCH  /api/v1/users/:id      # Update user (partial)
DELETE /api/v1/users/:id      # Delete user
```

Authentication: Bearer token in Authorization header
Content-Type: application/json

### Level 5 (Most Concrete): Precise Details
**Exact endpoint specification:**

```http
GET /api/v1/users/12345
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Accept: application/json

Response: 200 OK
{
  "id": 12345,
  "email": "user@example.com",
  "firstName": "Jane",
  "lastName": "Doe",
  "createdAt": "2024-01-15T10:30:00Z",
  "role": "standard"
}

Edge cases:
- User not found: 404 Not Found
- Invalid token: 401 Unauthorized
- Insufficient permissions: 403 Forbidden
- Invalid ID format: 400 Bad Request
- Server error: 500 Internal Server Error
```

Rate limit: 1000 requests/hour per token
Pagination: max 100 items per page, default 20

## Connections & Transitions

**L1 → L2**: REST provides a proven framework for creating predictable interfaces through standard conventions.

**L2 → L3**: Resource-oriented design is how REST constraints manifest in practical API design.

**L3 → L4**: User management is a concrete application of CRUD patterns to a specific domain resource.

**L4 → L5**: Exact HTTP requests/responses and error handling show how design patterns become actual code.

## Edge Cases & Boundary Testing

### Case 1: Deleting a non-existent user
- **Abstract principle (L1)**: Interface should provide clear feedback
- **Expected (L3)**: Return error for invalid operations
- **Actual (L5)**: `DELETE /users/99999` returns `404 Not Found` with body `{"error": "User not found"}`
- **Alignment**: ✓ Concrete implementation matches principle

### Case 2: Updating with partial data
- **Abstract principle (L1)**: Interface should be predictable
- **Expected (L3)**: PATCH for partial updates, PUT for full replacement
- **Actual (L5)**: `PATCH /users/123` with `{"firstName": "John"}` updates only firstName, leaves other fields unchanged
- **Alignment**: ✓ Follows REST semantics

### Case 3: Bulk operations
- **Abstract principle (L1)**: Interfaces should be consistent
- **Question**: How to delete multiple users?
- **Options**:
  - POST /users/bulk-delete (violates resource-oriented design)
  - DELETE /users with query params (non-standard)
  - Multiple DELETE requests (chatty but consistent)
- **Gap**: Pure REST doesn't handle bulk operations elegantly
- **Resolution**: Accept trade-off; use `POST /users/actions/bulk-delete` with clear documentation

## Applications

This ladder is useful for:
- **Onboarding new developers**: Show how design principles inform specific code
- **API review**: Check if implementation aligns with stated principles
- **Documentation**: Explain "why" behind specific endpoint designs
- **Consistency checking**: Ensure new endpoints follow same patterns
- **Client SDK design**: Derive SDK structure from abstraction levels

## Gaps & Assumptions

**Assumptions:**
- Using JSON (could be XML, Protocol Buffers, etc.)
- Token-based auth (could be OAuth, API keys, etc.)
- Synchronous operations (could be async/webhooks)

**Gaps:**
- Real-time updates not covered (WebSockets?)
- File uploads not addressed (multipart/form-data?)
- Versioning strategy mentioned but not detailed
- Caching strategy not specified
- Bulk operations awkward in pure REST

**Questions for deeper exploration:**
- How do GraphQL or gRPC change this ladder?
- What happens at massive scale (millions of requests/sec)?
- How does distributed/microservices architecture affect this?

# Week 3 Exercise: Adding Tags Filtering and Sorting

## 🎯 Exercise Overview

In this exercise, you will extend the basic Thoughts API to add tag filtering and sorting capabilities. The current implementation only supports basic pagination with a `limit` parameter. Your task is to add support for filtering by tags and implementing flexible sorting options.

## 📚 Learning Objectives

By completing this exercise, you will:

1. **Understand Query Parameter Processing**: Learn how to parse and validate query parameters
2. **Implement Tag-Based Filtering**: Build tag search functionality using SQL ILIKE patterns
3. **Create Dynamic Sorting**: Implement secure sorting with field validation
4. **Apply Repository Pattern**: Extend the repository pattern to handle filtering and sorting
5. **Handle Input Validation**: Implement proper validation and error handling for user input

## 🚀 Prerequisites

Before starting this exercise:

1. Complete the Week 3 tutorial (`tutorial/raw-db-connector/` or `tutorial/ORM/`)
2. Understand the Repository pattern implementation
3. Be familiar with SQL WHERE clauses and ORDER BY statements (for raw SQL) or SQLAlchemy queries (for ORM)
4. Have the database running: `docker-compose up db -d`

## 📋 Current Implementation

The current API only supports basic functionality:

```bash
# Current working endpoint
GET /api/v1/thoughts?limit=5

# Returns:
{
  "status": "success",
  "data": {
    "thoughts": [...],
    "total_count": 10,
    "limit": 5,
    "filters_applied": {}
  }
}
```

## 📋 Exercise Tasks

### Task 1: Implement Tag Filtering

**Objective**: Add the ability to filter thoughts by tags using query parameters.

#### Requirements:
- Accept a `tags` query parameter with comma-separated values
- Support multiple tags (OR logic): return thoughts containing ANY of the specified tags
- Implement case-insensitive tag matching using SQL `ILIKE` or SQLAlchemy `ilike()`
- Handle empty/invalid tag values gracefully

#### Expected API Behavior:
```bash
# Filter by single tag
GET /api/v1/thoughts?tags=work

# Filter by multiple tags (OR logic)
GET /api/v1/thoughts?tags=work,important,learning

# Case insensitive matching
GET /api/v1/thoughts?tags=WORK,Important

# Combined with limit
GET /api/v1/thoughts?tags=work&limit=3
```

#### Implementation Hints:
1. **In `app.py`**: Parse the `tags` parameter and split by commas
2. **In `repository.py`**: Extend the `get_all()` method to handle tag filtering
3. **SQL Pattern**: Use `ILIKE` for case-insensitive text search
4. **Validation**: Sanitize tag input to prevent SQL injection

### Task 2: Implement Sorting

**Objective**: Add sorting capabilities with field and direction validation.

#### Requirements:
- Accept `sort` parameter for field selection (default: `created_at`)
- Accept `order` parameter for sort direction (only `asc` or `desc` allowed)
- Support sorting by: `id`, `text`, `category`, `importance`, `created_at`, `updated_at`
- Validate sort fields against a whitelist to prevent SQL injection
- Reject invalid order values and return appropriate error messages (400 status)
- Default to sorting by `created_at` in descending order when no parameters provided

#### Expected API Behavior:
```bash
# Sort by importance (ascending)
GET /api/v1/thoughts?sort=importance&order=asc

# Sort by category (descending) - default order when sort provided
GET /api/v1/thoughts?sort=category&order=desc

# Default sorting (created_at DESC)
GET /api/v1/thoughts

# Invalid sort field should fallback to default
GET /api/v1/thoughts?sort=invalid_field

# Invalid order value should return 400 error
GET /api/v1/thoughts?sort=importance&order=invalid
```

#### Implementation Hints:
1. **Field Validation**: Use a whitelist of allowed sort fields
2. **Order Validation**: Only accept `asc` or `desc`, return error for invalid values
3. **SQL Security**: Never directly interpolate user input into SQL
4. **Default Handling**: Provide sensible defaults for missing parameters
5. **Case Handling**: Normalize `order` parameter to lowercase for comparison

### Task 3: Combine Filtering and Sorting

**Objective**: Make tag filtering and sorting work together seamlessly.

#### Requirements:
- Support using both filtering and sorting in the same request
- Ensure proper SQL query construction with WHERE and ORDER BY clauses
- Handle limit parameter correctly with filtered and sorted results
- Validate all parameters (tags, sort fields, and order values) consistently
- Return appropriate errors for invalid parameters

#### Expected API Behavior:
```bash
# Filter by tags and sort by importance
GET /api/v1/thoughts?tags=work,learning&sort=importance&order=desc

# Filter with sorting and limit
GET /api/v1/thoughts?tags=work&sort=created_at&order=asc&limit=5

# Multiple tags with custom sorting
GET /api/v1/thoughts?tags=important,learning&sort=importance&order=desc&limit=3
```

## 🧪 Testing Your Implementation

### Test Data Setup
First, create some test data:

```bash
# Create thoughts with different categories and content
curl -X POST http://localhost:5001/api/v1/thoughts \
  -H "Content-Type: application/json" \
  -d '{"thoughts":[
    {"text":"Learning SQL is important for backend development","category":"work","importance":9},
    {"text":"Remember to work on the important project deadline","category":"work","importance":8},
    {"text":"Personal learning goals for this quarter","category":"personal","importance":7},
    {"text":"Important meeting notes from today","category":"work","importance":6},
    {"text":"Random thought about learning new technologies","category":"random","importance":5}
  ]}'
```

### Test Cases

#### 1. Tag Filtering Tests
```bash
# Test single tag
curl "http://localhost:5001/api/v1/thoughts?tags=important"

# Test multiple tags
curl "http://localhost:5001/api/v1/thoughts?tags=work,learning"

# Test case insensitive
curl "http://localhost:5001/api/v1/thoughts?tags=IMPORTANT,Learning"

# Test empty tags (should return all)
curl "http://localhost:5001/api/v1/thoughts?tags="
```

#### 2. Sorting Tests
```bash
# Test sort by importance (ascending)
curl "http://localhost:5001/api/v1/thoughts?sort=importance&order=asc"

# Test sort by category (descending)
curl "http://localhost:5001/api/v1/thoughts?sort=category&order=desc"

# Test default sorting
curl "http://localhost:5001/api/v1/thoughts"

# Test invalid sort field (should use default)
curl "http://localhost:5001/api/v1/thoughts?sort=invalid_field"

# Test invalid order (should return error)
curl "http://localhost:5001/api/v1/thoughts?sort=importance&order=invalid"
```

#### 3. Combined Tests
```bash
# Filter by tags and sort
curl "http://localhost:5001/api/v1/thoughts?tags=work&sort=importance&order=desc"

# All filters with sorting
curl "http://localhost:5001/api/v1/thoughts?tags=important&category=work&importance_min=7&sort=created_at&order=asc"

# Pagination with filters
curl "http://localhost:5001/api/v1/thoughts?tags=learning&sort=importance&page=1&limit=3"
```

## 🔧 Implementation Guide

### Step 1: Modify the API Endpoint (`app.py`)

The current `get_thoughts()` function has TODO comments showing where to add the new functionality:

#### Current Implementation:
```python
@app.route("/api/v1/thoughts", methods=['GET'])
def get_thoughts():
    """
    Get thoughts with basic pagination
    
    Query Parameters:
    - limit: Items per page (default 10, max 100)
    
    TODO (Exercise): Add support for:
    - tags: Comma-separated list of tags to filter by
    - sort: Sort field (id, text, category, importance, created_at)
    - order: Sort order (asc, desc) - default: desc
    """
    try:
        # Parse query parameters (only limit for now)
        limit = min(request.args.get('limit', 10, type=int), 100)
        
        # TODO (Exercise): Parse additional parameters
        # tags_param = request.args.get('tags')
        # sort_field = request.args.get('sort', 'created_at')
        # sort_order = request.args.get('order', 'desc').upper()
```

#### Your Task:
1. **Uncomment and implement the TODO sections**
2. **Add parameter validation**
3. **Build the filters dictionary**
4. **Pass parameters to repository**

### Step 2: Extend the Repository (`repository.py`)

The repository has TODO comments showing where to add filtering and sorting logic:

#### Raw SQL Version (`raw-db-connector/repository.py`):
```python
def get_all(self, filters: Dict = None, sort_field: str = 'created_at', 
            sort_order: str = 'DESC', limit: int = 10, offset: int = 0) -> List[Dict]:
    """Get thoughts with basic filtering and sorting"""
    
    # Build base query
    query = "SELECT * FROM thoughts"
    params = []
    
    # Add filters (basic implementation)
    where_conditions = []
    if filters:
        # TODO (Exercise): Add tag filtering
        # if filters.get('tags'):
        #     tag_conditions = []
        #     for tag in filters['tags']:
        #         clean_tag = self._sanitize_search_term(tag)
        #         if clean_tag:
        #             tag_conditions.append("text ILIKE %s")
        #             params.append(f"%{clean_tag}%")
        #     
        #     if tag_conditions:
        #         where_conditions.append(f"({' OR '.join(tag_conditions)})")
        pass
```

#### ORM Version (`ORM/repository.py`):
```python
def get_all(self, filters: Dict = None, sort_field: str = 'created_at', 
            sort_order: str = 'DESC', limit: int = 10, offset: int = 0) -> List[Dict]:
    with self.db_manager.get_session() as session:
        # Start with base query
        query = session.query(Thought)
        
        # Apply filters (basic implementation)
        if filters:
            # TODO (Exercise): Add tag filtering
            # query = self._apply_filters(query, filters)
            pass
```

#### Your Task:
1. **Uncomment the TODO sections**
2. **Implement tag filtering logic**
3. **Add sorting validation**
4. **Handle the _sanitize_search_term method** (for raw SQL version)

### Step 3: Add Input Sanitization

Implement the `_sanitize_search_term()` method:

```python
def _sanitize_search_term(self, term: str) -> str:
    """Sanitize search terms to prevent SQL injection"""
    if not term or not isinstance(term, str):
        return ""
    
    # TODO: Remove potentially dangerous characters
    # Keep only alphanumeric, spaces, and common punctuation
    import re
    sanitized = re.sub(r'[^\w\s\-_]', '', term.strip())
    return sanitized[:50]  # Limit length
```

## ✅ Success Criteria

Your implementation is complete when:

1. **Tag Filtering Works**: API correctly filters thoughts containing specified tags
2. **Case Insensitive**: Tag matching works regardless of case (using ILIKE or ilike())
3. **Multiple Tags**: OR logic works for multiple tags
4. **Sorting Functions**: All valid sort fields work in both directions (asc/desc)
5. **Order Validation**: Invalid order values return 400 error with proper message
6. **Sort Field Validation**: Invalid sort fields fallback to default (created_at)
7. **Combined Operations**: Filtering and sorting work together with limit
8. **Security**: No SQL injection vulnerabilities (parameterized queries)
9. **Error Handling**: Proper error responses for invalid requests

### Test Commands That Should Work:
```bash
# Basic functionality
curl "http://localhost:5001/api/v1/thoughts?limit=5"

# Tag filtering
curl "http://localhost:5001/api/v1/thoughts?tags=work"
curl "http://localhost:5001/api/v1/thoughts?tags=work,important"

# Sorting
curl "http://localhost:5001/api/v1/thoughts?sort=importance&order=asc"
curl "http://localhost:5001/api/v1/thoughts?sort=category&order=desc"

# Combined
curl "http://localhost:5001/api/v1/thoughts?tags=work&sort=importance&order=desc&limit=3"

# Error cases (should return 400)
curl "http://localhost:5001/api/v1/thoughts?sort=importance&order=invalid"
```

## 🎓 Extension Challenges

Once you complete the basic requirements, try these advanced features:

1. **AND Logic for Tags**: Implement `tags_mode=all` to require ALL tags
2. **Partial Text Search**: Add `search` parameter for full-text search
3. **Date Range Filtering**: Add `created_after` and `created_before` parameters
4. **Multiple Sort Fields**: Support sorting by multiple fields
5. **Search Highlighting**: Return matched text with highlights

## 🔍 Common Pitfalls

Watch out for these common issues:

1. **SQL Injection**: Never directly interpolate user input into SQL queries
2. **Case Sensitivity**: Remember to use `ILIKE` for case-insensitive matching
3. **Empty Parameters**: Handle empty or whitespace-only parameters
4. **Invalid Sort Fields**: Always validate against a whitelist
5. **Parameter Parsing**: Handle malformed comma-separated values
6. **Performance**: Consider indexing for frequently searched fields

## 📖 Additional Resources

- [PostgreSQL ILIKE Documentation](https://www.postgresql.org/docs/current/functions-matching.html)
- [SQL Injection Prevention](https://owasp.org/www-community/attacks/SQL_Injection)
- [Flask Request Object](https://flask.palletsprojects.com/en/2.0.x/api/#flask.Request)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)

---

**Ready to implement advanced filtering and sorting?** Start with Task 1 and work your way through each requirement! 🚀

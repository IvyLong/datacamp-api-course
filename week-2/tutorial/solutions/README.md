# Week 2 Tutorial - Complete Exercise Solutions

This directory contains complete solutions to all exercises from the Flask API tutorial steps 1-8.

## 🎯 Solutions Overview

| Step | Topic | Solution File | Key Exercises Solved |
|------|-------|---------------|---------------------|
| 1 | Hello World | `step-1-solution.py` | Add status route, about route, test 404 handling |
| 2 | JSON Responses | `step-2-solution.py` | Product endpoints, Content-Type headers |
| 3 | Multiple Routes | `step-3-solution.py` | Tags endpoint, search functionality, API versioning |
| 4 | URL Parameters | `step-4-solution.py` | Text-only endpoint, user profiles, nested routes |
| 5 | Query Parameters | `step-5-solution.py` | Sorting, filtering, min_tags parameter |
| 6 | POST Requests | `step-6-solution.py` | Create thoughts, error handling, status codes |
| 7 | Validation | `step-7-solution.py` | Input validation, duplicate checks, error responses |
| 8 | Full CRUD | `step-8-solution.py` | Complete lifecycle, bulk operations |

## 🚀 How to Run Solutions

### Option A: Using Docker (Recommended)
```bash
# From the project root
./auto/run python week-2/tutorial/solutions/step-1-solution.py
./auto/run python week-2/tutorial/solutions/step-2-solution.py
# ... etc
```

### Option B: Direct Python
```bash
cd week-2/tutorial/solutions
python step-1-solution.py
```

**Important:** With Docker, use port **5001** in URLs (http://localhost:5001)

## 📝 Exercise Solutions Summary

### Step 1: Hello World
- ✅ Added `/api/status` endpoint
- ✅ Added `/about` endpoint with student info
- ✅ Tested all routes and 404 behavior
- ✅ Explained Flask's automatic 404 handling

### Step 2: JSON Responses
- ✅ Created `/api/product` with id, name, price, in_stock, categories
- ✅ Created `/api/products` returning list of 3 products
- ✅ Tested with browser, curl, and Python requests
- ✅ Verified `Content-Type: application/json` header

### Step 3: Multiple Routes
- ✅ Added `/api/v1/tags` returning all unique tags with counts
- ✅ Added `/api/v1/search` for finding thoughts containing "learning"
- ✅ Explained API versioning benefits (/api/v1/ pattern)
- ✅ Verified all endpoints return 200 status codes

### Step 4: URL Parameters
- ✅ Added `/api/v1/thoughts/<id>/text` for text-only responses
- ✅ Tested non-integer IDs (Flask auto-404s)
- ✅ Added `/api/v1/users/<username>` with profile URLs
- ✅ Created `/api/v1/users/<username>/thoughts/<id>` (two parameters)

### Step 5: Query Parameters
- ✅ Added `sort` parameter (author, id) to `/api/v1/thoughts`
- ✅ Added `min_tags` filter for minimum tag count
- ✅ Tested complex combinations: `?tag=python&author=Alice&limit=5`
- ✅ Explained path vs query parameter usage patterns

### Step 6: POST Requests
- ✅ Tested POST operations with curl and Python requests
- ✅ Verified error handling for missing fields
- ✅ Tested empty body scenarios
- ✅ Confirmed 201 Created status vs 200 OK for different operations

### Step 7: Validation
- ✅ Tested all validation rules (text length, tag limits, etc.)
- ✅ Added duplicate tag validation
- ✅ Added alphanumeric-only tag validation
- ✅ Explained 400 (client error) vs 500 (server error) usage

### Step 8: Full CRUD
- ✅ Tested complete CRUD lifecycle (Create→Read→Update→Delete)
- ✅ Demonstrated PUT vs PATCH differences
- ✅ Added bulk delete endpoint (`DELETE /api/v1/thoughts?tag=flask`)
- ✅ Added clear all thoughts endpoint (`DELETE /api/v1/thoughts`)

## 🧪 Testing Commands

### Step 1 Testing
```bash
curl http://localhost:5001/api/status
curl http://localhost:5001/about
curl http://localhost:5001/nonexistent  # Should return 404
```

### Step 2 Testing
```bash
curl http://localhost:5001/api/product
curl http://localhost:5001/api/products
curl -i http://localhost:5001/api/products  # See headers
```

### Step 6 POST Testing
```bash
curl -X POST http://localhost:5001/api/v1/thoughts \
  -H "Content-Type: application/json" \
  -d '{"text": "My new thought!", "tags": ["learning"]}'
```

### Step 8 CRUD Testing
```bash
# Create
curl -X POST http://localhost:5001/api/v1/thoughts \
  -H "Content-Type: application/json" \
  -d '{"text": "Test thought", "tags": ["test"]}'

# Read
curl http://localhost:5001/api/v1/thoughts/1

# Update (partial)
curl -X PATCH http://localhost:5001/api/v1/thoughts/1 \
  -H "Content-Type: application/json" \
  -d '{"text": "Updated text"}'

# Delete
curl -X DELETE http://localhost:5001/api/v1/thoughts/1
```

## 💡 Key Learning Points

### API Design Patterns
- **RESTful URLs**: Use nouns, not verbs (`/thoughts` not `/getThoughts`)
- **HTTP Methods**: GET (read), POST (create), PUT/PATCH (update), DELETE (remove)
- **Status Codes**: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found)
- **Versioning**: Use `/api/v1/` for future compatibility

### Flask Best Practices
- Use `jsonify()` for JSON responses (sets correct Content-Type)
- Validate input data before processing
- Return meaningful error messages
- Use type hints in route parameters (`<int:id>`)
- Handle exceptions gracefully

### Testing Approaches
- **Browser**: Good for GET requests and visual inspection
- **Curl**: Perfect for testing all HTTP methods and headers
- **Python requests**: Best for automated testing and integration
- **Tools**: Postman, Insomnia for complex API testing

## 🎓 Next Steps

1. **Compare with Production**: Look at `week-2/solutions/app.py` for production patterns
2. **Add Features**: Try adding authentication, pagination, or file uploads
3. **Database Integration**: Replace in-memory storage with SQLite or PostgreSQL
4. **API Documentation**: Add OpenAPI/Swagger documentation
5. **Testing**: Write unit tests for all endpoints

## 🔗 Related Files

- Original tutorial steps: `week-2/tutorial/step-*.py`
- Production solution: `week-2/solutions/app.py`
- Docker setup: `auto/run` script
- API documentation: `week-2/tutorial/README.md`

---

**Happy Learning!** 🚀 Each solution file contains detailed comments explaining the implementation and additional bonus features.
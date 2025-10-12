# Instructor Guide - Flask API Tutorial

This guide helps you teach the Flask API course using the progressive exercises.

## 📚 Course Structure

The tutorial follows a **progressive learning approach** where each step builds on the previous one:

### Step 1: Hello World (15 mins)
**Concepts:** Basic Flask app, routes, decorators
- Students create their first Flask server
- Understand the request-response cycle
- Learn about routes and view functions

**Teaching Tips:**
- Start with the absolute basics
- Show how to run the server
- Demonstrate testing in browser
- Explain what `debug=True` does

### Step 2: JSON Responses (20 mins)
**Concepts:** JSON serialization, Content-Type headers, data structures
- Introduction to `jsonify()`
- Difference between JSON objects and arrays
- When to use JSON vs plain text

**Teaching Tips:**
- Show browser DevTools to inspect responses
- Compare plain text vs JSON responses
- Explain why APIs use JSON

### Step 3: Multiple Routes (20 mins)
**Concepts:** RESTful naming, API organization, status codes
- RESTful URL patterns
- Version prefixes (`/api/v1/`)
- Health check endpoints

**Teaching Tips:**
- Discuss API versioning strategies
- Explain why we use plural nouns for resources
- Show importance of consistent URL structure

### Step 4: URL Parameters (25 mins)
**Concepts:** Path parameters, dynamic routes, 404 handling
- `<int:id>` syntax
- Type conversion in routes
- Handling missing resources

**Teaching Tips:**
- Show the difference between `/users/1` and `/users/abc`
- Explain when to use path params vs query params
- Demonstrate nested resources

### Step 5: Query Parameters (30 mins)
**Concepts:** Filtering, search, optional parameters
- `request.args.get()`
- Multiple filter combinations
- Pagination considerations

**Teaching Tips:**
- Build filters incrementally
- Show how query params are optional
- Discuss performance with large datasets
- Preview pagination needs

### Step 6: POST Requests (30 mins)
**Concepts:** HTTP methods, request body, resource creation
- Different HTTP methods (GET vs POST)
- Parsing JSON body
- 201 Created status code

**Teaching Tips:**
- Use `curl` and Python `requests` for testing
- Explain Content-Type header importance
- Discuss idempotency
- Show POST in Postman/Insomnia

### Step 7: Validation (35 mins)
**Concepts:** Input validation, error handling, security
- Comprehensive input validation
- Meaningful error messages
- Security considerations

**Teaching Tips:**
- Emphasize "never trust user input"
- Show real-world validation rules
- Discuss security implications
- Test edge cases together

### Step 8: Full CRUD (40 mins)
**Concepts:** Complete REST API, PUT vs PATCH, DELETE
- All CRUD operations
- PUT (full update) vs PATCH (partial)
- DELETE operation
- Complete API lifecycle

**Teaching Tips:**
- Walk through full lifecycle of a resource
- Explain idempotency of PUT and DELETE
- Discuss when to use PUT vs PATCH
- Compare with the solution in `week-2/solution/app.py`

## 🎯 Teaching Strategies

### Live Coding
- Code along with students for Steps 1-3
- Let students try Steps 4-5 first, then review
- Students work independently on Steps 6-8 with guidance

### Common Mistakes to Watch For
1. **Forgetting to return values** from route functions
2. **Not checking for None** when using `request.args.get()`
3. **Hardcoding port 5000** when using Docker (should access via 5001)
4. **Not handling errors** gracefully
5. **Forgetting Content-Type header** in POST requests
6. **Confusing path params with query params**

### Testing Tips for Students
```bash
# Using curl
curl http://localhost:5001/api/v1/thoughts
curl -i http://localhost:5001/api/v1/thoughts  # show headers
curl -X POST http://localhost:5001/api/v1/thoughts \
  -H "Content-Type: application/json" \
  -d '{"text": "Test", "tags": ["test"]}'

# Using Python
import requests
response = requests.get("http://localhost:5001/api/v1/thoughts")
print(response.json())
```

## 🏃 Running the Exercises

### For Students (Using Docker)
```bash
# From project root
./auto/run python week-2/tutorial/step-1-hello-world.py
```
Access at: `http://localhost:5001`

### For Instructor (Local Python)
```bash
cd week-2/tutorial
python step-1-hello-world.py
```
Access at: `http://localhost:5000`

## 📝 Suggested Timeline

### 3-Hour Workshop
- Introduction & Setup: 15 mins
- Steps 1-2: 35 mins
- Break: 10 mins
- Steps 3-4: 45 mins
- Break: 10 mins
- Steps 5-6: 60 mins
- Wrap-up & Q&A: 5 mins

### 6-Hour Course (2 sessions)
**Session 1: Fundamentals**
- Steps 1-4 with exercises
- Extended practice time
- Q&A

**Session 2: Advanced**
- Steps 5-8 with exercises
- Compare with full solution
- Build a mini project

## 🎓 Learning Objectives Checklist

By the end, students should be able to:
- [ ] Create a Flask application from scratch
- [ ] Define routes with different HTTP methods
- [ ] Return JSON responses
- [ ] Use path parameters for resource identification
- [ ] Use query parameters for filtering
- [ ] Handle POST requests with JSON body
- [ ] Validate user input
- [ ] Return appropriate HTTP status codes
- [ ] Implement complete CRUD operations
- [ ] Understand REST API best practices

## 🔧 Troubleshooting

### "Connection refused"
- Check if server is running
- Verify correct port (5001 with Docker, 5000 local)

### "ModuleNotFoundError: No module named 'flask'"
- Using Docker: rebuild image after updating requirements.txt
- Local: `pip install Flask`

### "Address already in use"
- Another server is running on that port
- Use `lsof -i :5000` to find and kill the process

### Docker issues
- Ensure Docker is running
- Try rebuilding: `docker build -t thought-tagger-workshop .`

## 📚 Additional Resources

- Flask documentation: https://flask.palletsprojects.com/
- REST API best practices
- HTTP status codes reference
- Postman/Insomnia for API testing

## 💡 Extension Ideas

After completing all steps, advanced students can:
1. Add a SQLite database instead of in-memory storage
2. Add authentication with API keys
3. Implement rate limiting
4. Add pagination to list endpoints
5. Create OpenAPI/Swagger documentation
6. Add unit tests with pytest
7. Deploy to a cloud platform

---

**Good luck with your course! 🚀**


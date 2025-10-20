#!/usr/bin/env python3
"""
Step 4 Solution: URL Parameters - Exercise Solutions

This file contains the solutions to the exercises from step-4-url-parameters.py

EXERCISES COMPLETED:
1. ✅ Add a route "/api/v1/thoughts/<int:id>/text" that returns only the text
2. ✅ Test what happens with non-integer ID (Flask returns 404 automatically)
3. ✅ Add a route "/api/v1/users/<username>" that returns user profile
4. ✅ Create a route with two path parameters
"""

from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
thoughts_storage = [
    {"id": 1, "text": "Flask is awesome!", "tags": ["flask", "python"]},
    {"id": 2, "text": "REST APIs are everywhere", "tags": ["api-design"]},
    {"id": 3, "text": "Learning by doing works", "tags": ["learning", "growth"]}
]

# Sample users data for exercises
users_data = {
    "alice": {"username": "alice", "name": "Alice Johnson", "role": "developer"},
    "bob": {"username": "bob", "name": "Bob Smith", "role": "designer"},
    "charlie": {"username": "charlie", "name": "Charlie Brown", "role": "manager"}
}


@app.route("/")
def home():
    """API documentation"""
    return jsonify({
        "api": "Thought of the Day API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/v1/thoughts": "Get all thoughts",
            "GET /api/v1/thoughts/<id>": "Get a specific thought by ID",
            "GET /api/v1/thoughts/<id>/text": "Get only the text (Exercise 1)",
            "GET /api/v1/users/<username>": "Get user profile (Exercise 3)",
            "GET /api/v1/users/<username>/thoughts/<id>": "Two parameters (Exercise 4)"
        }
    })


@app.route("/api/v1/thoughts")
def get_all_thoughts():
    """GET /api/v1/thoughts - Returns all thoughts"""
    return jsonify(thoughts_storage), 200


@app.route("/api/v1/thoughts/<int:thought_id>")
def get_thought_by_id(thought_id):
    """GET /api/v1/thoughts/{id} - Returns a single thought by its ID"""
    for thought in thoughts_storage:
        if thought["id"] == thought_id:
            return jsonify(thought), 200
    
    return jsonify({
        "error": "Not Found",
        "message": f"Thought with ID {thought_id} does not exist"
    }), 404


@app.route("/api/v1/thoughts/<int:thought_id>/tags")
def get_thought_tags(thought_id):
    """GET /api/v1/thoughts/{id}/tags - Returns only the tags for a specific thought"""
    for thought in thoughts_storage:
        if thought["id"] == thought_id:
            return jsonify({
                "thought_id": thought_id,
                "tags": thought["tags"]
            }), 200
    
    return jsonify({
        "error": "Not Found",
        "message": f"Thought with ID {thought_id} does not exist"
    }), 404


@app.route("/api/v1/tags/<tag_name>")
def get_thoughts_by_tag(tag_name):
    """GET /api/v1/tags/{tag_name} - Returns all thoughts that have this tag"""
    matching_thoughts = []
    
    for thought in thoughts_storage:
        if tag_name in thought["tags"]:
            matching_thoughts.append(thought)
    
    return jsonify({
        "tag": tag_name,
        "count": len(matching_thoughts),
        "thoughts": matching_thoughts
    }), 200


# ==========================================
# EXERCISE SOLUTIONS
# ==========================================

@app.route("/api/v1/thoughts/<int:thought_id>/text")
def get_thought_text(thought_id):
    """
    EXERCISE 1 SOLUTION:
    Add a route "/api/v1/thoughts/<int:id>/text" that returns
    only the text of a specific thought
    """
    for thought in thoughts_storage:
        if thought["id"] == thought_id:
            return jsonify({
                "thought_id": thought_id,
                "text": thought["text"]
            }), 200
    
    return jsonify({
        "error": "Not Found",
        "message": f"Thought with ID {thought_id} does not exist"
    }), 404


@app.route("/api/v1/users/<username>")
def get_user_profile(username):
    """
    EXERCISE 3 SOLUTION:
    Add a route "/api/v1/users/<username>" that returns:
    {"username": "alice", "profile_url": "/api/v1/users/alice"}
    """
    # Check if user exists in our sample data
    if username in users_data:
        user = users_data[username].copy()
        user["profile_url"] = f"/api/v1/users/{username}"
        return jsonify(user), 200
    else:
        # Create a basic profile for any username
        return jsonify({
            "username": username,
            "profile_url": f"/api/v1/users/{username}",
            "status": "guest_user",
            "message": f"Profile for {username}"
        }), 200


@app.route("/api/v1/users/<username>/thoughts/<int:thought_id>")
def get_user_thought(username, thought_id):
    """
    EXERCISE 4 SOLUTION:
    Create a route that accepts two path parameters:
    "/api/v1/users/<username>/thoughts/<int:thought_id>"
    
    This demonstrates how to use multiple path parameters in a single route
    """
    # Find the thought
    thought = None
    for t in thoughts_storage:
        if t["id"] == thought_id:
            thought = t
            break
    
    if not thought:
        return jsonify({
            "error": "Not Found",
            "message": f"Thought with ID {thought_id} does not exist"
        }), 404
    
    # Simulate user-specific access to thought
    return jsonify({
        "user": username,
        "thought_id": thought_id,
        "thought": thought,
        "user_profile_url": f"/api/v1/users/{username}",
        "access_timestamp": "2025-10-20T10:30:00Z"
    }), 200


# Bonus endpoints for additional practice
@app.route("/api/v1/thoughts/<int:thought_id>/details")
def get_thought_details(thought_id):
    """Bonus: Get extended details about a thought"""
    for thought in thoughts_storage:
        if thought["id"] == thought_id:
            return jsonify({
                "thought": thought,
                "details": {
                    "character_count": len(thought["text"]),
                    "word_count": len(thought["text"].split()),
                    "tag_count": len(thought["tags"]),
                    "contains_python": "python" in thought["tags"],
                    "text_length_category": "short" if len(thought["text"]) < 20 else "medium" if len(thought["text"]) < 50 else "long"
                }
            }), 200
    
    return jsonify({
        "error": "Not Found",
        "message": f"Thought with ID {thought_id} does not exist"
    }), 404


@app.route("/api/v1/users/<username>/stats")
def get_user_stats(username):
    """Bonus: Get statistics about a user's interaction with thoughts"""
    # This is simulated data since we don't track actual user interactions
    return jsonify({
        "username": username,
        "stats": {
            "thoughts_viewed": 12,
            "favorite_tags": ["python", "learning"],
            "last_activity": "2025-10-20T09:15:00Z",
            "join_date": "2025-09-01T00:00:00Z"
        }
    }), 200


if __name__ == "__main__":
    print("🚀 Starting Thought of the Day API server with Step 4 Solutions...")
    print("")
    print("📖 Original endpoints:")
    print("   GET  http://localhost:5001/api/v1/thoughts/1")
    print("   GET  http://localhost:5001/api/v1/thoughts/2")
    print("   GET  http://localhost:5001/api/v1/thoughts/1/tags")
    print("   GET  http://localhost:5001/api/v1/tags/flask")
    print("")
    print("📖 Exercise solution endpoints:")
    print("   GET  http://localhost:5001/api/v1/thoughts/1/text    - ✅ Exercise 1")
    print("   GET  http://localhost:5001/api/v1/users/alice        - ✅ Exercise 3")
    print("   GET  http://localhost:5001/api/v1/users/alice/thoughts/1 - ✅ Exercise 4")
    print("")
    print("📖 Test Exercise 2 (non-integer ID):")
    print("   GET  http://localhost:5001/api/v1/thoughts/abc       - 🔍 Should return 404")
    print("")
    print("📖 Bonus endpoints:")
    print("   GET  http://localhost:5001/api/v1/thoughts/1/details - 🎁 Extended details")
    print("   GET  http://localhost:5001/api/v1/users/alice/stats  - 🎁 User statistics")
    print("")
    
    app.run(debug=True, host="0.0.0.0", port=5000)


# ==========================================
# 📝 EXERCISE ANSWERS:
# ==========================================

"""
EXERCISE 2: Test what happens when you visit /api/v1/thoughts/abc
✅ Flask automatically returns 404 Not Found

When you use <int:thought_id> in your route, Flask:
1. Tries to convert the URL parameter to an integer
2. If conversion fails (like with "abc"), Flask doesn't match the route
3. Since no route matches, Flask returns 404 automatically
4. This is Flask's built-in type conversion and validation

Try these URLs to see the behavior:
- /api/v1/thoughts/1   → ✅ Works (integer)
- /api/v1/thoughts/99  → ❌ 404 (integer but thought doesn't exist)
- /api/v1/thoughts/abc → ❌ 404 (not an integer, route doesn't match)

EXERCISE 4: Path vs Query Parameters - When to use each?

PATH PARAMETERS (/api/v1/thoughts/{id}):
✅ Use for: Identifying specific resources
✅ Required for the request to be valid
✅ Part of the resource hierarchy
✅ Examples: user ID, thought ID, file name

QUERY PARAMETERS (/api/v1/thoughts?tag=flask&limit=10):
✅ Use for: Optional filtering, sorting, pagination
✅ Not required for basic functionality
✅ Modify how data is returned
✅ Examples: filters, search terms, page size
"""
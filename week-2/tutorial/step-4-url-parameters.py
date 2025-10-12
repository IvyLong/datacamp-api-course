#!/usr/bin/env python3
"""
Step 4: URL Parameters - Dynamic Routes

Learning Objectives:
- Use path parameters in URLs
- Convert parameter types (int, string)
- Handle missing resources (404 errors)
- Create dynamic routes

Concepts Introduced:
- <parameter_name> syntax in routes
- <int:parameter_name> for type conversion
- 404 Not Found responses
- Dynamic URL matching
"""

from flask import Flask, jsonify

app = Flask(__name__)

# Sample data
thoughts_storage = [
    {"id": 1, "text": "Flask is awesome!", "tags": ["flask", "python"]},
    {"id": 2, "text": "REST APIs are everywhere", "tags": ["api-design"]},
    {"id": 3, "text": "Learning by doing works", "tags": ["learning", "growth"]}
]


@app.route("/")
def home():
    """API documentation"""
    return jsonify({
        "api": "Thought of the Day API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/v1/thoughts": "Get all thoughts",
            "GET /api/v1/thoughts/<id>": "Get a specific thought by ID"
        }
    })


@app.route("/api/v1/thoughts")
def get_all_thoughts():
    """
    GET /api/v1/thoughts
    Returns all thoughts
    """
    return jsonify(thoughts_storage), 200


@app.route("/api/v1/thoughts/<int:thought_id>")
def get_thought_by_id(thought_id):
    """
    GET /api/v1/thoughts/{id}
    
    Path parameter: thought_id (automatically converted to int)
    Returns a single thought by its ID
    
    Examples:
    - /api/v1/thoughts/1 → returns thought with id=1
    - /api/v1/thoughts/99 → returns 404 if not found
    """
    # Search for the thought with matching ID
    for thought in thoughts_storage:
        if thought["id"] == thought_id:
            return jsonify(thought), 200
    
    # If not found, return 404 error
    return jsonify({
        "error": "Not Found",
        "message": f"Thought with ID {thought_id} does not exist"
    }), 404


@app.route("/api/v1/thoughts/<int:thought_id>/tags")
def get_thought_tags(thought_id):
    """
    GET /api/v1/thoughts/{id}/tags
    
    Returns only the tags for a specific thought
    This demonstrates nested resource access
    """
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
    """
    GET /api/v1/tags/{tag_name}
    
    Path parameter: tag_name (string)
    Returns all thoughts that have this tag
    
    Examples:
    - /api/v1/tags/flask → returns thoughts tagged with "flask"
    - /api/v1/tags/learning → returns thoughts tagged with "learning"
    """
    matching_thoughts = []
    
    for thought in thoughts_storage:
        if tag_name in thought["tags"]:
            matching_thoughts.append(thought)
    
    return jsonify({
        "tag": tag_name,
        "count": len(matching_thoughts),
        "thoughts": matching_thoughts
    }), 200


if __name__ == "__main__":
    print("🚀 Starting Thought of the Day API server...")
    print("")
    print("📖 Try these endpoints with path parameters:")
    print("   GET  http://localhost:5001/api/v1/thoughts/1")
    print("   GET  http://localhost:5001/api/v1/thoughts/2")
    print("   GET  http://localhost:5001/api/v1/thoughts/99   (404 Not Found)")
    print("   GET  http://localhost:5001/api/v1/thoughts/1/tags")
    print("   GET  http://localhost:5001/api/v1/tags/flask")
    print("   GET  http://localhost:5001/api/v1/tags/learning")
    print("")
    
    app.run(debug=True, host="0.0.0.0", port=5000)


# ==========================================
# 🎯 EXERCISES:
# ==========================================
# 1. Add a route "/api/v1/thoughts/<int:id>/text" that returns
#    only the text of a specific thought
#
# 2. Test what happens when you visit /api/v1/thoughts/abc
#    (a non-integer ID) - Flask should return 404 automatically
#
# 3. Add a route "/api/v1/users/<username>" that returns:
#    {"username": "alice", "profile_url": "/api/v1/users/alice"}
#
# 4. Create a route that accepts two path parameters:
#    "/api/v1/users/<username>/thoughts/<int:thought_id>"


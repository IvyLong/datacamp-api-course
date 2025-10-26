#!/usr/bin/env python3
"""
Step 6: POST Requests - Accepting Data

Learning Objectives:
- Handle POST requests
- Parse JSON request body
- Create new resources
- Return 201 Created status
- Understand HTTP methods

Concepts Introduced:
- methods=["GET", "POST"] in routes
- request.get_json() for parsing body
- 201 Created status code
- CRUD operations (Create, Read)
"""

from flask import Flask, jsonify, request
from datetime import datetime, timezone

app = Flask(__name__)

# In-memory storage
thoughts_storage = [
    {"id": 1, "text": "Flask is awesome!", "tags": ["flask", "python"], "timestamp": "2025-10-12T10:00:00Z"},
    {"id": 2, "text": "REST APIs are everywhere", "tags": ["api-design"], "timestamp": "2025-10-12T11:00:00Z"}
]
next_id = 3


@app.route("/")
def home():
    """API documentation"""
    return jsonify({
        "api": "Thought of the Day API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/v1/thoughts": "Get all thoughts",
            "POST /api/v1/thoughts": "Create a new thought",
            "GET /api/v1/thoughts/<id>": "Get specific thought"
        }
    })


@app.route("/api/v1/thoughts", methods=["GET", "POST"])
def thoughts_endpoint():
    """
    Handle both GET and POST for /api/v1/thoughts
    
    GET: Returns all thoughts
    POST: Creates a new thought
    """
    
    if request.method == "GET":
        # Handle GET request - return all thoughts
        tag_filter = request.args.get("tag")
        
        if tag_filter:
            results = [t for t in thoughts_storage if tag_filter in t["tags"]]
        else:
            results = thoughts_storage
        
        return jsonify(results), 200
    
    elif request.method == "POST":
        # Handle POST request - create new thought
        global next_id
        
        # Get JSON data from request body
        data = request.get_json()
        
        # Check if data was provided
        if not data:
            return jsonify({
                "error": "Bad Request",
                "message": "Request body is required"
            }), 400
        
        # Check for required fields
        if "text" not in data:
            return jsonify({
                "error": "Bad Request",
                "message": "Field 'text' is required"
            }), 400
        
        if "tags" not in data:
            return jsonify({
                "error": "Bad Request",
                "message": "Field 'tags' is required"
            }), 400
        
        # Create new thought
        new_thought = {
            "id": next_id,
            "text": data["text"],
            "tags": data["tags"],
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }
        
        # Add to storage and increment ID
        thoughts_storage.append(new_thought)
        next_id += 1
        
        # Return created resource with 201 status
        return jsonify(new_thought), 201


@app.route("/api/v1/thoughts/<int:thought_id>", methods=["GET"])
def get_thought(thought_id):
    """GET a specific thought by ID"""
    for thought in thoughts_storage:
        if thought["id"] == thought_id:
            return jsonify(thought), 200
    
    return jsonify({
        "error": "Not Found",
        "message": f"Thought with ID {thought_id} not found"
    }), 404


@app.route("/api/v1/stats", methods=["GET"])
def get_stats():
    """GET statistics about stored thoughts"""
    all_tags = []
    for thought in thoughts_storage:
        all_tags.extend(thought["tags"])
    
    return jsonify({
        "total_thoughts": len(thoughts_storage),
        "total_tags": len(all_tags),
        "unique_tags": len(set(all_tags))
    }), 200


if __name__ == "__main__":
    print("🚀 Starting Thought of the Day API server...")
    print("")
    print("📖 Available endpoints:")
    print("   GET  http://localhost:5001/api/v1/thoughts")
    print("   POST http://localhost:5001/api/v1/thoughts")
    print("   GET  http://localhost:5001/api/v1/thoughts/<id>")
    print("   GET  http://localhost:5001/api/v1/stats")
    print("")
    print("💡 Test POST request with curl:")
    print('   curl -X POST http://localhost:5001/api/v1/thoughts \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"text": "My new thought!", "tags": ["learning"]}\'')
    print("")
    print("💡 Test POST request with Python:")
    print('   import requests')
    print('   data = {"text": "My thought", "tags": ["python"]}')
    print('   response = requests.post("http://localhost:5001/api/v1/thoughts", json=data)')
    print('   print(response.json())')
    print("")
    
    app.run(debug=True, host="0.0.0.0", port=5001)


# ==========================================
# 🎯 EXERCISES:
# ==========================================
# 1. Use curl or Python requests to POST a new thought
#    Verify it appears in GET /api/v1/thoughts
#
# 2. Try POSTing without "text" field - observe the error
#
# 3. Try POSTing with an empty body - what happens?
#
# 4. POST 3 new thoughts, then GET /api/v1/stats to see updated counts
#
# 5. What HTTP status code is returned for successful POST?
#    Why is it different from GET's 200?


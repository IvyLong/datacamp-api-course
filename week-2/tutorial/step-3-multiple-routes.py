#!/usr/bin/env python3
"""
Step 3: Multiple Routes - Organizing Your API

Learning Objectives:
- Organize routes into logical groups
- Understand RESTful URL patterns
- Return appropriate status codes
- Use tuple returns for status codes

Concepts Introduced:
- RESTful resource naming (plural nouns)
- Status codes: 200 (OK), 201 (Created), 404 (Not Found)
- Returning (response, status_code) tuples
- Organizing related endpoints
"""

from flask import Flask, jsonify

app = Flask(__name__)

# In-memory storage for our thoughts
thoughts_storage = [
    {"id": 1, "text": "Flask is awesome!", "tags": ["flask", "python"]},
    {"id": 2, "text": "REST APIs are everywhere", "tags": ["api-design"]},
    {"id": 3, "text": "Learning by doing works", "tags": ["learning", "growth"]}
]

next_id = 4  # Track the next available ID


@app.route("/")
def home():
    """API documentation landing page"""
    return jsonify({
        "api": "Thought of the Day API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/v1/thoughts": "Get all thoughts",
            "GET /api/v1/health": "Check API health"
        }
    })


# Health check endpoint (common in production APIs)
@app.route("/api/v1/health")
def health_check():
    """
    Health check endpoint
    Returns 200 status if the API is running
    """
    return jsonify({
        "status": "healthy",
        "message": "API is running"
    }), 200


# List all thoughts
@app.route("/api/v1/thoughts")
def get_thoughts():
    """
    GET /api/v1/thoughts
    Returns all thoughts with 200 OK status
    """
    return jsonify(thoughts_storage), 200


# Get statistics
@app.route("/api/v1/stats")
def get_stats():
    """
    GET /api/v1/stats
    Returns statistics about the stored thoughts
    """
    total_thoughts = len(thoughts_storage)
    all_tags = []
    for thought in thoughts_storage:
        all_tags.extend(thought["tags"])
    
    unique_tags = len(set(all_tags))
    
    return jsonify({
        "total_thoughts": total_thoughts,
        "unique_tags": unique_tags,
        "total_tags": len(all_tags)
    }), 200


# About the API
@app.route("/api/v1/about")
def about():
    """
    GET /api/v1/about
    Information about this API
    """
    return jsonify({
        "name": "Thought of the Day API",
        "description": "A REST API for storing and retrieving daily thoughts with tags",
        "author": "API Course Student",
        "version": "1.0.0",
        "features": [
            "Store thoughts with tags",
            "Retrieve all thoughts",
            "View statistics"
        ]
    }), 200


if __name__ == "__main__":
    print("🚀 Starting Thought of the Day API server...")
    print("")
    print("📖 Available endpoints:")
    print("   GET  http://localhost:5001/")
    print("   GET  http://localhost:5001/api/v1/health")
    print("   GET  http://localhost:5001/api/v1/thoughts")
    print("   GET  http://localhost:5001/api/v1/stats")
    print("   GET  http://localhost:5001/api/v1/about")
    print("")
    
    app.run(debug=True, host="0.0.0.0", port=5001)


# ==========================================
# 🎯 EXERCISES:
# ==========================================
# 1. Add a route "/api/v1/tags" that returns a list of all unique tags
#
# 2. Add a route "/api/v1/search" that returns information about
#    how many thoughts contain the word "learning"
#
# 3. Why do we use "/api/v1/" in our URLs?
#    (Hint: Think about future versions)
#
# 4. Test all endpoints and verify they return status code 200
#    Use: curl -i http://localhost:5001/api/v1/thoughts
#    (The -i flag shows headers including status code)


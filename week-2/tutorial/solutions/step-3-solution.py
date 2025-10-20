#!/usr/bin/env python3
"""
Step 3 Solution: Multiple Routes - Exercise Solutions

This file contains the solutions to the exercises from step-3-multiple-routes.py

EXERCISES COMPLETED:
1. ✅ Add a route "/api/v1/tags" that returns a list of all unique tags
2. ✅ Add a route "/api/v1/search" that returns search information
3. ✅ Explain why we use "/api/v1/" in URLs (API versioning)
4. ✅ Test all endpoints and verify they return status code 200
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
            "GET /api/v1/health": "Check API health",
            "GET /api/v1/tags": "Get all unique tags (Exercise 1)",
            "GET /api/v1/search": "Search thoughts (Exercise 2)"
        }
    })


@app.route("/api/v1/health")
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "API is running"
    }), 200


@app.route("/api/v1/thoughts")
def get_thoughts():
    """GET /api/v1/thoughts - Returns all thoughts with 200 OK status"""
    return jsonify(thoughts_storage), 200


@app.route("/api/v1/stats")
def get_stats():
    """GET /api/v1/stats - Returns statistics about the stored thoughts"""
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


@app.route("/api/v1/about")
def about():
    """GET /api/v1/about - Information about this API"""
    return jsonify({
        "name": "Thought of the Day API",
        "description": "A REST API for storing and retrieving daily thoughts with tags",
        "author": "API Course Student",
        "version": "1.0.0",
        "features": [
            "Store thoughts with tags",
            "Retrieve all thoughts",
            "View statistics",
            "Search thoughts",
            "List unique tags"
        ]
    }), 200


# ==========================================
# EXERCISE SOLUTIONS
# ==========================================

@app.route("/api/v1/tags")
def get_tags():
    """
    EXERCISE 1 SOLUTION:
    Add a route "/api/v1/tags" that returns a list of all unique tags
    """
    # Collect all tags from all thoughts
    all_tags = []
    for thought in thoughts_storage:
        all_tags.extend(thought["tags"])
    
    # Get unique tags and count occurrences
    unique_tags = list(set(all_tags))
    tag_counts = {}
    
    for tag in all_tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # Sort tags alphabetically
    unique_tags.sort()
    
    return jsonify({
        "total_unique_tags": len(unique_tags),
        "tags": unique_tags,
        "tag_usage": tag_counts
    }), 200


@app.route("/api/v1/search")
def search_learning():
    """
    EXERCISE 2 SOLUTION:
    Add a route "/api/v1/search" that returns information about
    how many thoughts contain the word "learning"
    """
    search_term = "learning"
    matching_thoughts = []
    
    # Search for thoughts containing "learning" (case-insensitive)
    for thought in thoughts_storage:
        if search_term.lower() in thought["text"].lower():
            matching_thoughts.append(thought)
    
    return jsonify({
        "search_term": search_term,
        "total_thoughts": len(thoughts_storage),
        "matching_thoughts": len(matching_thoughts),
        "percentage": round((len(matching_thoughts) / len(thoughts_storage)) * 100, 1),
        "results": matching_thoughts
    }), 200


# Bonus endpoints for additional practice
@app.route("/api/v1/search/advanced")
def advanced_search():
    """Bonus: More advanced search functionality"""
    results = {}
    search_terms = ["flask", "api", "learning", "python"]
    
    for term in search_terms:
        matching = []
        for thought in thoughts_storage:
            # Search in both text and tags
            if (term.lower() in thought["text"].lower() or 
                term.lower() in [tag.lower() for tag in thought["tags"]]):
                matching.append(thought["id"])
        
        results[term] = {
            "count": len(matching),
            "thought_ids": matching
        }
    
    return jsonify({
        "search_results": results,
        "total_searches": len(search_terms)
    }), 200


@app.route("/api/v1/summary")
def get_summary():
    """Bonus: API summary with all key metrics"""
    all_tags = []
    for thought in thoughts_storage:
        all_tags.extend(thought["tags"])
    
    return jsonify({
        "api_name": "Thought of the Day API",
        "version": "1.0.0",
        "metrics": {
            "total_thoughts": len(thoughts_storage),
            "total_tags_used": len(all_tags),
            "unique_tags": len(set(all_tags)),
            "average_tags_per_thought": round(len(all_tags) / len(thoughts_storage), 2)
        },
        "available_endpoints": 8,
        "status": "operational"
    }), 200


if __name__ == "__main__":
    print("🚀 Starting Thought of the Day API server with Step 3 Solutions...")
    print("")
    print("📖 Original endpoints:")
    print("   GET  http://localhost:5001/")
    print("   GET  http://localhost:5001/api/v1/health")
    print("   GET  http://localhost:5001/api/v1/thoughts")
    print("   GET  http://localhost:5001/api/v1/stats")
    print("   GET  http://localhost:5001/api/v1/about")
    print("")
    print("📖 Exercise solution endpoints:")
    print("   GET  http://localhost:5001/api/v1/tags           - ✅ Exercise 1")
    print("   GET  http://localhost:5001/api/v1/search         - ✅ Exercise 2")
    print("")
    print("📖 Bonus endpoints:")
    print("   GET  http://localhost:5001/api/v1/search/advanced - 🎁 Advanced search")
    print("   GET  http://localhost:5001/api/v1/summary        - 🎁 API summary")
    print("")
    print("💡 Test status codes with curl:")
    print("   curl -i http://localhost:5001/api/v1/thoughts")
    print("   curl -i http://localhost:5001/api/v1/tags")
    print("   (The -i flag shows headers including status code)")
    print("")
    
    app.run(debug=True, host="0.0.0.0", port=5000)


# ==========================================
# 📝 EXERCISE ANSWERS:
# ==========================================

"""
EXERCISE 3: Why do we use "/api/v1/" in our URLs?
✅ Answer: API VERSIONING

API versioning allows you to:

1. **Maintain backward compatibility**: When you need to make breaking changes
   to your API, you can create v2 while keeping v1 running for existing clients.

2. **Controlled migration**: Clients can migrate from v1 to v2 at their own pace.

3. **Multiple versions**: You can run multiple API versions simultaneously:
   - /api/v1/thoughts (older version)
   - /api/v2/thoughts (newer version with breaking changes)
   - /api/v3/thoughts (latest version)

4. **Clear expectations**: Clients know exactly which version they're using.

Example evolution:
- v1: Simple thought storage
- v2: Added user authentication (breaking change)
- v3: Added advanced search capabilities

Without versioning, updating your API could break all existing client applications!

EXERCISE 4: Test all endpoints and verify they return status code 200
✅ All endpoints in this solution return 200 OK status code
✅ Use `curl -i <URL>` to see the HTTP status line
✅ Look for "HTTP/1.1 200 OK" in the response headers
"""
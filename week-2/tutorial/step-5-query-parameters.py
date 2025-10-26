#!/usr/bin/env python3
"""
Step 5: Query Parameters - Filtering and Search

Learning Objectives:
- Use query parameters for filtering
- Access query strings with request.args
- Implement search and filter logic
- Combine multiple query parameters

Concepts Introduced:
- request.args.get() for query parameters
- Optional vs required parameters
- Filtering collections
- Multiple query parameters
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data with more variety
thoughts_storage = [
    {"id": 1, "text": "Flask is awesome!", "tags": ["flask", "python"], "author": "Alice"},
    {"id": 2, "text": "REST APIs are everywhere", "tags": ["api-design"], "author": "Bob"},
    {"id": 3, "text": "Learning by doing works", "tags": ["learning", "growth"], "author": "Alice"},
    {"id": 4, "text": "Python is versatile", "tags": ["python", "programming"], "author": "Charlie"},
    {"id": 5, "text": "Flask makes APIs easy", "tags": ["flask", "python", "api-design"], "author": "Alice"}
]


@app.route("/")
def home():
    """API documentation"""
    return jsonify({
        "api": "Thought of the Day API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/v1/thoughts": "Get all thoughts (supports filtering)",
            "GET /api/v1/thoughts?tag=flask": "Filter by tag",
            "GET /api/v1/thoughts?author=Alice": "Filter by author",
            "GET /api/v1/thoughts?tag=python&author=Alice": "Multiple filters"
        }
    })


@app.route("/api/v1/thoughts")
def get_thoughts():
    """
    GET /api/v1/thoughts
    
    Query Parameters:
    - tag (optional): Filter thoughts by tag
    - author (optional): Filter thoughts by author
    - limit (optional): Limit number of results
    
    Examples:
    - /api/v1/thoughts → all thoughts
    - /api/v1/thoughts?tag=flask → thoughts with "flask" tag
    - /api/v1/thoughts?author=Alice → thoughts by Alice
    - /api/v1/thoughts?tag=python&author=Alice → both filters
    - /api/v1/thoughts?limit=2 → only first 2 thoughts
    """
    # Start with all thoughts
    results = thoughts_storage.copy()
    
    # Get query parameters
    tag_filter = request.args.get("tag")  # Returns None if not provided
    author_filter = request.args.get("author")
    limit = request.args.get("limit")
    
    # Apply tag filter if provided
    if tag_filter:
        results = [t for t in results if tag_filter in t["tags"]]
    
    # Apply author filter if provided
    if author_filter:
        results = [t for t in results if t["author"] == author_filter]
    
    # Apply limit if provided
    if limit:
        try:
            limit_num = int(limit)
            results = results[:limit_num]
        except ValueError:
            return jsonify({
                "error": "Bad Request",
                "message": "Limit must be a number"
            }), 400
    
    # Return results with metadata
    return jsonify({
        "total": len(results),
        "filters": {
            "tag": tag_filter,
            "author": author_filter,
            "limit": limit
        },
        "thoughts": results
    }), 200


@app.route("/api/v1/search")
def search_thoughts():
    """
    GET /api/v1/search
    
    Query Parameters:
    - q (required): Search term to look for in thought text
    
    Examples:
    - /api/v1/search?q=Flask
    - /api/v1/search?q=learning
    """
    search_query = request.args.get("q")
    
    if not search_query:
        return jsonify({
            "error": "Bad Request",
            "message": "Query parameter 'q' is required"
        }), 400
    
    # Search for thoughts containing the query (case-insensitive)
    results = [
        t for t in thoughts_storage 
        if search_query.lower() in t["text"].lower()
    ]
    
    return jsonify({
        "query": search_query,
        "total_results": len(results),
        "results": results
    }), 200


@app.route("/api/v1/tags")
def get_tags():
    """
    GET /api/v1/tags
    
    Query Parameters:
    - author (optional): Filter tags by author's thoughts
    
    Returns all unique tags, optionally filtered by author
    """
    author_filter = request.args.get("author")
    
    # Get thoughts to analyze
    thoughts_to_analyze = thoughts_storage
    if author_filter:
        thoughts_to_analyze = [t for t in thoughts_storage if t["author"] == author_filter]
    
    # Collect all tags
    all_tags = []
    for thought in thoughts_to_analyze:
        all_tags.extend(thought["tags"])
    
    # Get unique tags with counts
    tag_counts = {}
    for tag in all_tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    return jsonify({
        "author_filter": author_filter,
        "unique_tags": len(tag_counts),
        "tags": [
            {"tag": tag, "count": count}
            for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        ]
    }), 200


if __name__ == "__main__":
    print("🚀 Starting Thought of the Day API server...")
    print("")
    print("📖 Try these endpoints with query parameters:")
    print("   GET  http://localhost:5001/api/v1/thoughts")
    print("   GET  http://localhost:5001/api/v1/thoughts?tag=flask")
    print("   GET  http://localhost:5001/api/v1/thoughts?author=Alice")
    print("   GET  http://localhost:5001/api/v1/thoughts?tag=python&author=Alice")
    print("   GET  http://localhost:5001/api/v1/thoughts?limit=2")
    print("   GET  http://localhost:5001/api/v1/search?q=Flask")
    print("   GET  http://localhost:5001/api/v1/tags")
    print("   GET  http://localhost:5001/api/v1/tags?author=Alice")
    print("")
    
    app.run(debug=True, host="0.0.0.0", port=5001)


# ==========================================
# 🎯 EXERCISES:
# ==========================================
# 1. Add a query parameter "sort" to /api/v1/thoughts that sorts by:
#    - "author" → alphabetically by author
#    - "id" → by ID (default)
#
# 2. Add a query parameter "min_tags" that filters thoughts with
#    at least that many tags
#
# 3. Test combining multiple filters:
#    /api/v1/thoughts?tag=python&author=Alice&limit=5
#
# 4. What's the difference between path parameters and query parameters?
#    When would you use each?


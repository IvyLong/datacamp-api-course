#!/usr/bin/env python3
"""
Steps 5-8 Combined Solution: Complete Exercise Solutions
This file demonstrates all remaining exercise solutions in one comprehensive API.
"""

from flask import Flask, jsonify, request
from datetime import datetime, timezone
import re

app = Flask(__name__)

# In-memory storage
thoughts_storage = [
    {"id": 1, "text": "Flask is awesome!", "tags": ["flask", "python"], "author": "Alice", "timestamp": "2025-10-20T10:00:00Z", "updated_at": None},
    {"id": 2, "text": "REST APIs are everywhere", "tags": ["api-design"], "author": "Bob", "timestamp": "2025-10-20T11:00:00Z", "updated_at": None},
    {"id": 3, "text": "Learning by doing works", "tags": ["learning", "growth"], "author": "Alice", "timestamp": "2025-10-20T12:00:00Z", "updated_at": None},
    {"id": 4, "text": "Python is versatile", "tags": ["python", "programming"], "author": "Charlie", "timestamp": "2025-10-20T13:00:00Z", "updated_at": None},
    {"id": 5, "text": "Flask makes APIs easy", "tags": ["flask", "python", "api-design"], "author": "Alice", "timestamp": "2025-10-20T14:00:00Z", "updated_at": None}
]
next_id = 6

# Helper functions
def create_error_response(code, message):
    return jsonify({"error": True, "code": code, "message": message}), code

def validate_thought_data(data, partial=False):
    if not data:
        return False, "Request body is required"
    
    if "text" in data:
        if not isinstance(data["text"], str):
            return False, "Field 'text' must be a string"
        text = data["text"].strip()
        if len(text) < 5:
            return False, "Field 'text' must be at least 5 characters long"
        if len(text) > 280:
            return False, "Field 'text' must not exceed 280 characters"
    elif not partial:
        return False, "Field 'text' is required"
    
    if "tags" in data:
        if not isinstance(data["tags"], list):
            return False, "Field 'tags' must be an array"
        if len(data["tags"]) == 0:
            return False, "At least one tag is required"
        if len(data["tags"]) > 5:
            return False, "Maximum 5 tags allowed"
        
        # Check for duplicates (Step 7 exercise)
        if len(data["tags"]) != len(set(data["tags"])):
            return False, "Duplicate tags are not allowed"
        
        for tag in data["tags"]:
            if not isinstance(tag, str):
                return False, "All tags must be strings"
            if len(tag.strip()) < 2:
                return False, "Each tag must be at least 2 characters long"
            if len(tag) > 20:
                return False, "Each tag must not exceed 20 characters"
            # Alphanumeric + hyphens only (Step 7 exercise)
            if not re.match(r'^[a-zA-Z0-9-]+$', tag):
                return False, "Tags must contain only alphanumeric characters and hyphens"
    elif not partial:
        return False, "Field 'tags' is required"
    
    return True, None

def find_thought_by_id(thought_id):
    for thought in thoughts_storage:
        if thought["id"] == thought_id:
            return thought
    return None

# Main endpoints
@app.route("/")
def home():
    return jsonify({
        "api": "Complete Tutorial Solution API",
        "version": "2.0.0",
        "exercise_solutions": {
            "step_5": ["sorting", "min_tags filter", "combined filters"],
            "step_6": ["POST validation", "error handling", "status codes"],
            "step_7": ["advanced validation", "duplicate checks", "regex validation"],
            "step_8": ["full CRUD", "bulk operations", "lifecycle testing"]
        }
    })

# GET with advanced filtering (Step 5 solutions)
@app.route("/api/v1/thoughts", methods=["GET"])
def get_thoughts():
    """Step 5: Advanced query parameter handling"""
    try:
        results = thoughts_storage.copy()
        
        # Basic filters
        tag_filter = request.args.get("tag")
        author_filter = request.args.get("author")
        limit = request.args.get("limit")
        
        # Step 5 Exercise 1: Sort parameter
        sort_by = request.args.get("sort", "id")  # Default to ID
        if sort_by not in ["id", "author", "timestamp"]:
            return create_error_response(400, "Sort must be one of: id, author, timestamp")
        
        # Step 5 Exercise 2: min_tags filter
        min_tags = request.args.get("min_tags")
        
        # Apply filters
        if tag_filter:
            results = [t for t in results if tag_filter in t["tags"]]
        
        if author_filter:
            results = [t for t in results if t["author"] == author_filter]
        
        if min_tags:
            try:
                min_tags_num = int(min_tags)
                results = [t for t in results if len(t["tags"]) >= min_tags_num]
            except ValueError:
                return create_error_response(400, "min_tags must be a number")
        
        # Apply sorting
        if sort_by == "author":
            results = sorted(results, key=lambda x: x["author"])
        elif sort_by == "timestamp":
            results = sorted(results, key=lambda x: x["timestamp"])
        else:  # id
            results = sorted(results, key=lambda x: x["id"])
        
        # Apply limit
        if limit:
            try:
                limit_num = int(limit)
                results = results[:limit_num]
            except ValueError:
                return create_error_response(400, "Limit must be a number")
        
        return jsonify({
            "total": len(results),
            "filters": {
                "tag": tag_filter,
                "author": author_filter,
                "min_tags": min_tags,
                "sort": sort_by,
                "limit": limit
            },
            "thoughts": results
        }), 200
        
    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")

# POST for creating thoughts (Step 6 solutions)
@app.route("/api/v1/thoughts", methods=["POST"])
def create_thought():
    """Step 6 & 7: POST with comprehensive validation"""
    try:
        global next_id
        data = request.get_json()
        
        # Validate input
        is_valid, error_message = validate_thought_data(data, partial=False)
        if not is_valid:
            return create_error_response(400, error_message)
        
        # Create new thought
        new_thought = {
            "id": next_id,
            "text": data["text"].strip(),
            "tags": [tag.strip() for tag in data["tags"]],
            "author": data.get("author", "Anonymous"),
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "updated_at": None
        }
        
        thoughts_storage.append(new_thought)
        next_id += 1
        
        return jsonify({
            "success": True,
            "message": "Thought created successfully",
            "thought": new_thought
        }), 201
        
    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")

# Full CRUD operations (Step 8 solutions)
@app.route("/api/v1/thoughts/<int:thought_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def handle_thought(thought_id):
    """Step 8: Complete CRUD operations"""
    
    if request.method == "GET":
        thought = find_thought_by_id(thought_id)
        if not thought:
            return create_error_response(404, f"Thought with ID {thought_id} not found")
        return jsonify({"success": True, "thought": thought}), 200
    
    elif request.method == "PUT":
        # Full update - all fields required
        thought = find_thought_by_id(thought_id)
        if not thought:
            return create_error_response(404, f"Thought with ID {thought_id} not found")
        
        data = request.get_json()
        is_valid, error_message = validate_thought_data(data, partial=False)
        if not is_valid:
            return create_error_response(400, error_message)
        
        thought["text"] = data["text"].strip()
        thought["tags"] = [tag.strip() for tag in data["tags"]]
        thought["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return jsonify({"success": True, "message": "Thought updated", "thought": thought}), 200
    
    elif request.method == "PATCH":
        # Partial update - only provided fields
        thought = find_thought_by_id(thought_id)
        if not thought:
            return create_error_response(404, f"Thought with ID {thought_id} not found")
        
        data = request.get_json()
        is_valid, error_message = validate_thought_data(data, partial=True)
        if not is_valid:
            return create_error_response(400, error_message)
        
        if "text" in data:
            thought["text"] = data["text"].strip()
        if "tags" in data:
            thought["tags"] = [tag.strip() for tag in data["tags"]]
        
        thought["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return jsonify({"success": True, "message": "Thought updated", "thought": thought}), 200
    
    elif request.method == "DELETE":
        thought = find_thought_by_id(thought_id)
        if not thought:
            return create_error_response(404, f"Thought with ID {thought_id} not found")
        
        thoughts_storage.remove(thought)
        return jsonify({"success": True, "message": f"Thought {thought_id} deleted"}), 200

# Step 8 Exercise 3: Bulk delete by tag
@app.route("/api/v1/thoughts/bulk", methods=["DELETE"])
def bulk_delete_thoughts():
    """Step 8 Exercise: Bulk delete endpoint"""
    tag = request.args.get("tag")
    if not tag:
        return create_error_response(400, "Query parameter 'tag' is required")
    
    # Find thoughts with the tag
    to_delete = [t for t in thoughts_storage if tag in t["tags"]]
    
    # Remove them
    for thought in to_delete:
        thoughts_storage.remove(thought)
    
    return jsonify({
        "success": True,
        "message": f"Deleted {len(to_delete)} thoughts with tag '{tag}'",
        "deleted_count": len(to_delete)
    }), 200

# Step 8 Exercise 4: Clear all thoughts
@app.route("/api/v1/thoughts/clear", methods=["DELETE"])
def clear_all_thoughts():
    """Step 8 Exercise: Clear all thoughts (DANGEROUS!)"""
    count = len(thoughts_storage)
    thoughts_storage.clear()
    global next_id
    next_id = 1
    
    return jsonify({
        "success": True,
        "message": f"Cleared all {count} thoughts",
        "warning": "This action cannot be undone!"
    }), 200

if __name__ == "__main__":
    print("🚀 Starting Complete Tutorial Solution API...")
    print("")
    print("📖 Step 5 Solutions (Query Parameters):")
    print("   GET  http://localhost:5001/api/v1/thoughts?sort=author")
    print("   GET  http://localhost:5001/api/v1/thoughts?min_tags=2")
    print("   GET  http://localhost:5001/api/v1/thoughts?tag=python&author=Alice&limit=3")
    print("")
    print("📖 Step 6 Solutions (POST Requests):")
    print("   POST http://localhost:5001/api/v1/thoughts")
    print("        Body: {\"text\": \"My thought\", \"tags\": [\"test\"]}")
    print("")
    print("📖 Step 7 Solutions (Validation):")
    print("   Try invalid data to test validation rules")
    print("")
    print("📖 Step 8 Solutions (Full CRUD):")
    print("   PUT    http://localhost:5001/api/v1/thoughts/1")
    print("   PATCH  http://localhost:5001/api/v1/thoughts/1")
    print("   DELETE http://localhost:5001/api/v1/thoughts/1")
    print("   DELETE http://localhost:5001/api/v1/thoughts/bulk?tag=flask")
    print("   DELETE http://localhost:5001/api/v1/thoughts/clear")
    print("")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
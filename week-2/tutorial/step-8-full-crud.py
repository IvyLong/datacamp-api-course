#!/usr/bin/env python3
"""
Step 8: Full CRUD API - Complete Implementation

Learning Objectives:
- Implement all CRUD operations (Create, Read, Update, Delete)
- Handle PUT/PATCH for updates
- Handle DELETE requests
- Understand idempotency
- Build a production-ready API

Concepts Introduced:
- PUT vs PATCH methods
- DELETE method
- Complete CRUD operations
- Resource lifecycle management
- RESTful API best practices
"""

from flask import Flask, jsonify, request
from datetime import datetime, timezone

app = Flask(__name__)

# In-memory storage
thoughts_storage = []
next_id = 1


def create_error_response(code, message):
    """Helper function to create standardized error responses"""
    return jsonify({
        "error": True,
        "code": code,
        "message": message
    }), code


def validate_thought_data(data, partial=False):
    """
    Validate thought input data
    Args:
        data: The data to validate
        partial: If True, allows missing fields (for PATCH)
    Returns: (is_valid, error_message)
    """
    if not data:
        return False, "Request body is required"
    
    # Validate 'text' field (if present or required)
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
    
    # Validate 'tags' field (if present or required)
    if "tags" in data:
        if not isinstance(data["tags"], list):
            return False, "Field 'tags' must be an array"
        if len(data["tags"]) == 0:
            return False, "At least one tag is required"
        if len(data["tags"]) > 5:
            return False, "Maximum 5 tags allowed"
        
        for tag in data["tags"]:
            if not isinstance(tag, str):
                return False, "All tags must be strings"
            if len(tag.strip()) < 2:
                return False, "Each tag must be at least 2 characters long"
            if len(tag) > 20:
                return False, "Each tag must not exceed 20 characters"
    elif not partial:
        return False, "Field 'tags' is required"
    
    return True, None


def find_thought_by_id(thought_id):
    """Helper function to find a thought by ID"""
    for thought in thoughts_storage:
        if thought["id"] == thought_id:
            return thought
    return None


@app.route("/")
def home():
    """API documentation"""
    return jsonify({
        "api": "Thought of the Day API - Full CRUD",
        "version": "2.0.0",
        "endpoints": {
            "GET /api/v1/thoughts": "List all thoughts",
            "POST /api/v1/thoughts": "Create a new thought",
            "GET /api/v1/thoughts/<id>": "Get a specific thought",
            "PUT /api/v1/thoughts/<id>": "Replace a thought (full update)",
            "PATCH /api/v1/thoughts/<id>": "Update a thought (partial update)",
            "DELETE /api/v1/thoughts/<id>": "Delete a thought"
        }
    })


# ============================================
# READ OPERATIONS
# ============================================

@app.route("/api/v1/thoughts", methods=["GET"])
def get_thoughts():
    """
    GET /api/v1/thoughts
    List all thoughts with optional filtering
    """
    try:
        tag_filter = request.args.get("tag")
        
        if tag_filter:
            results = [t for t in thoughts_storage if tag_filter in t["tags"]]
        else:
            results = thoughts_storage
        
        return jsonify({
            "success": True,
            "total": len(results),
            "thoughts": results
        }), 200
    
    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")


@app.route("/api/v1/thoughts/<int:thought_id>", methods=["GET"])
def get_thought(thought_id):
    """
    GET /api/v1/thoughts/{id}
    Get a specific thought by ID
    """
    try:
        thought = find_thought_by_id(thought_id)
        
        if not thought:
            return create_error_response(404, f"Thought with ID {thought_id} not found")
        
        return jsonify({
            "success": True,
            "thought": thought
        }), 200
    
    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")


# ============================================
# CREATE OPERATION
# ============================================

@app.route("/api/v1/thoughts", methods=["POST"])
def create_thought():
    """
    POST /api/v1/thoughts
    Create a new thought
    """
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


# ============================================
# UPDATE OPERATIONS
# ============================================

@app.route("/api/v1/thoughts/<int:thought_id>", methods=["PUT"])
def update_thought_full(thought_id):
    """
    PUT /api/v1/thoughts/{id}
    Replace a thought entirely (full update)
    All fields must be provided
    """
    try:
        data = request.get_json()
        
        # Find existing thought
        thought = find_thought_by_id(thought_id)
        if not thought:
            return create_error_response(404, f"Thought with ID {thought_id} not found")
        
        # Validate input (all fields required for PUT)
        is_valid, error_message = validate_thought_data(data, partial=False)
        if not is_valid:
            return create_error_response(400, error_message)
        
        # Replace the thought (keep id and timestamp)
        thought["text"] = data["text"].strip()
        thought["tags"] = [tag.strip() for tag in data["tags"]]
        thought["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return jsonify({
            "success": True,
            "message": "Thought updated successfully",
            "thought": thought
        }), 200
    
    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")


@app.route("/api/v1/thoughts/<int:thought_id>", methods=["PATCH"])
def update_thought_partial(thought_id):
    """
    PATCH /api/v1/thoughts/{id}
    Partially update a thought
    Only provided fields will be updated
    """
    try:
        data = request.get_json()
        
        # Find existing thought
        thought = find_thought_by_id(thought_id)
        if not thought:
            return create_error_response(404, f"Thought with ID {thought_id} not found")
        
        # Validate input (partial validation)
        is_valid, error_message = validate_thought_data(data, partial=True)
        if not is_valid:
            return create_error_response(400, error_message)
        
        # Update only provided fields
        if "text" in data:
            thought["text"] = data["text"].strip()
        
        if "tags" in data:
            thought["tags"] = [tag.strip() for tag in data["tags"]]
        
        thought["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return jsonify({
            "success": True,
            "message": "Thought updated successfully",
            "thought": thought
        }), 200
    
    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")


# ============================================
# DELETE OPERATION
# ============================================

@app.route("/api/v1/thoughts/<int:thought_id>", methods=["DELETE"])
def delete_thought(thought_id):
    """
    DELETE /api/v1/thoughts/{id}
    Delete a thought by ID
    """
    try:
        thought = find_thought_by_id(thought_id)
        
        if not thought:
            return create_error_response(404, f"Thought with ID {thought_id} not found")
        
        # Remove from storage
        thoughts_storage.remove(thought)
        
        return jsonify({
            "success": True,
            "message": f"Thought with ID {thought_id} deleted successfully"
        }), 200
    
    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")


# ============================================
# UTILITY ENDPOINTS
# ============================================

@app.route("/api/v1/stats", methods=["GET"])
def get_stats():
    """GET statistics about the API"""
    all_tags = []
    for thought in thoughts_storage:
        all_tags.extend(thought["tags"])
    
    return jsonify({
        "total_thoughts": len(thoughts_storage),
        "total_tags": len(all_tags),
        "unique_tags": len(set(all_tags))
    }), 200


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return create_error_response(404, "The requested resource was not found")


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return create_error_response(405, "Method not allowed for this endpoint")


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return create_error_response(500, "Internal server error occurred")


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    # Add some sample data
    thoughts_storage.append({
        "id": 1,
        "text": "Flask makes building APIs fun!",
        "tags": ["flask", "python"],
        "timestamp": "2025-10-12T10:00:00Z",
        "updated_at": None
    })
    next_id = 2
    
    print("🚀 Starting Full CRUD API server...")
    print("")
    print("📖 Complete CRUD Operations:")
    print("")
    print("CREATE:")
    print('  POST http://localhost:5001/api/v1/thoughts')
    print('  Body: {"text": "My thought", "tags": ["tag1"]}')
    print("")
    print("READ:")
    print('  GET  http://localhost:5001/api/v1/thoughts')
    print('  GET  http://localhost:5001/api/v1/thoughts/1')
    print("")
    print("UPDATE (full):")
    print('  PUT  http://localhost:5001/api/v1/thoughts/1')
    print('  Body: {"text": "Updated thought", "tags": ["new"]}')
    print("")
    print("UPDATE (partial):")
    print('  PATCH http://localhost:5001/api/v1/thoughts/1')
    print('  Body: {"text": "Only update text"}')
    print("")
    print("DELETE:")
    print('  DELETE http://localhost:5001/api/v1/thoughts/1')
    print("")
    
    app.run(debug=True, host="0.0.0.0", port=5001)


# ==========================================
# 🎯 EXERCISES:
# ==========================================
# 1. Test the complete CRUD lifecycle:
#    a. POST a new thought
#    b. GET it by ID
#    c. PATCH to update just the text
#    d. PUT to replace it entirely
#    e. DELETE it
#    f. Try to GET it again (should be 404)
#
# 2. What's the difference between PUT and PATCH?
#    Try updating with PUT without providing all fields.
#
# 3. Add a bulk delete endpoint:
#    DELETE /api/v1/thoughts?tag=flask
#    (deletes all thoughts with that tag)
#
# 4. Add an endpoint to clear all thoughts:
#    DELETE /api/v1/thoughts
#    (Be careful with this in production!)
#
# 5. Compare this implementation with the solution in
#    week-2/solution/app.py - what are the differences?


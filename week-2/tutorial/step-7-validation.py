#!/usr/bin/env python3
"""
Step 7: Validation and Error Handling

Learning Objectives:
- Validate input data thoroughly
- Return meaningful error messages
- Handle different error scenarios
- Use proper HTTP status codes
- Create reusable validation functions

Concepts Introduced:
- Input validation patterns
- 400 Bad Request for validation errors
- 500 Internal Server Error for exceptions
- Validation helper functions
- Error response standardization
"""

from flask import Flask, jsonify, request
from datetime import datetime, timezone

app = Flask(__name__)

# In-memory storage
thoughts_storage = []
next_id = 1


def create_error_response(code, message):
    """
    Helper function to create standardized error responses
    """
    return jsonify({
        "error": True,
        "code": code,
        "message": message
    }), code


def validate_thought_data(data):
    """
    Validate thought input data
    Returns: (is_valid, error_message)
    """
    # Check if data exists
    if not data:
        return False, "Request body is required"
    
    # Validate 'text' field
    if "text" not in data:
        return False, "Field 'text' is required"
    
    if not isinstance(data["text"], str):
        return False, "Field 'text' must be a string"
    
    text = data["text"].strip()
    
    if len(text) < 5:
        return False, "Field 'text' must be at least 5 characters long"
    
    if len(text) > 280:
        return False, "Field 'text' must not exceed 280 characters"
    
    # Validate 'tags' field
    if "tags" not in data:
        return False, "Field 'tags' is required"
    
    if not isinstance(data["tags"], list):
        return False, "Field 'tags' must be an array"
    
    if len(data["tags"]) == 0:
        return False, "At least one tag is required"
    
    if len(data["tags"]) > 5:
        return False, "Maximum 5 tags allowed"
    
    # Validate each tag
    for tag in data["tags"]:
        if not isinstance(tag, str):
            return False, "All tags must be strings"
        
        if len(tag.strip()) < 2:
            return False, "Each tag must be at least 2 characters long"
        
        if len(tag) > 20:
            return False, "Each tag must not exceed 20 characters"
    
    # All validation passed
    return True, None


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
        },
        "validation_rules": {
            "text": "Required, 5-280 characters",
            "tags": "Required array, 1-5 tags, each 2-20 characters"
        }
    })


@app.route("/api/v1/thoughts", methods=["GET"])
def get_thoughts():
    """GET all thoughts with optional filtering"""
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


@app.route("/api/v1/thoughts", methods=["POST"])
def create_thought():
    """POST a new thought with validation"""
    try:
        # Get and parse JSON data
        data = request.get_json()
        
        # Validate input
        is_valid, error_message = validate_thought_data(data)
        if not is_valid:
            return create_error_response(400, error_message)
        
        # Create new thought
        global next_id
        new_thought = {
            "id": next_id,
            "text": data["text"].strip(),
            "tags": [tag.strip() for tag in data["tags"]],
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
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


@app.route("/api/v1/thoughts/<int:thought_id>", methods=["GET"])
def get_thought(thought_id):
    """GET a specific thought by ID"""
    try:
        for thought in thoughts_storage:
            if thought["id"] == thought_id:
                return jsonify({
                    "success": True,
                    "thought": thought
                }), 200
        
        return create_error_response(404, f"Thought with ID {thought_id} not found")
    
    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")


# Global error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors for undefined routes"""
    return create_error_response(404, "The requested resource was not found")


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors for unsupported methods"""
    return create_error_response(405, "Method not allowed for this endpoint")


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 internal server errors"""
    return create_error_response(500, "Internal server error occurred")


if __name__ == "__main__":
    print("🚀 Starting Thought of the Day API server...")
    print("")
    print("📖 Test validation with these examples:")
    print("")
    print("✅ Valid POST:")
    print('   curl -X POST http://localhost:5001/api/v1/thoughts \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"text": "This is a valid thought!", "tags": ["valid", "test"]}\'')
    print("")
    print("❌ Invalid - text too short:")
    print('   curl -X POST http://localhost:5001/api/v1/thoughts \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"text": "Hi", "tags": ["test"]}\'')
    print("")
    print("❌ Invalid - no tags:")
    print('   curl -X POST http://localhost:5001/api/v1/thoughts \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"text": "Valid text but no tags", "tags": []}\'')
    print("")
    
    app.run(debug=True, host="0.0.0.0", port=5000)


# ==========================================
# 🎯 EXERCISES:
# ==========================================
# 1. Test each validation rule:
#    - Empty text
#    - Text too short (< 5 chars)
#    - Text too long (> 280 chars)
#    - Missing tags
#    - Too many tags (> 5)
#    - Tag too short (< 2 chars)
#
# 2. Add validation to ensure no duplicate tags in a single thought
#
# 3. Add validation to check that tags only contain alphanumeric 
#    characters and hyphens (no special characters)
#
# 4. What's the difference between 400 and 500 errors?
#    When should you use each?


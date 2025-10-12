#!/usr/bin/env python3
"""
Thought of the Day API - Flask Implementation

A Flask-based REST API for storing, retrieving, and filtering user-submitted 'thoughts' by tags.
Implements the OpenAPI 3.0.0 specification defined in api-design-thought-of-the-day.yaml.

Author: API Course
Version: 1.3.0
"""

from flask import Flask, request, jsonify
from datetime import datetime, timezone
import re

app = Flask(__name__)

# In-memory storage for thoughts (will be reset when server restarts)
thoughts_storage = []
next_id = 1


class Thought:
    """Data model for a thought object."""

    def __init__(self, text, tags):
        global next_id
        self.id = next_id
        next_id += 1
        self.text = text
        self.timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        self.tags = tags if isinstance(tags, list) else []

    def to_dict(self):
        """Convert thought object to dictionary for JSON response."""
        return {
            "id": self.id,
            "text": self.text,
            "timestamp": self.timestamp,
            "tags": self.tags,
        }


def create_error_response(code, message):
    """Create standardized error response matching OpenAPI spec."""
    return jsonify({"code": code, "message": message}), code


def validate_thought_input(data):
    """Validate input data for creating a new thought."""
    errors = []

    if not data:
        return ["Request body is required"]

    if "text" not in data:
        errors.append("The 'text' field is required")
    elif not isinstance(data["text"], str):
        errors.append("The 'text' field must be a string")
    elif len(data["text"].strip()) < 5:
        errors.append("The 'text' field must be at least 5 characters long")
    elif len(data["text"]) > 280:
        errors.append("The 'text' field must not exceed 280 characters")

    if "tags" not in data:
        errors.append("The 'tags' field is required")
    elif not isinstance(data["tags"], list):
        errors.append("The 'tags' field must be an array")
    elif not all(isinstance(tag, str) for tag in data["tags"]):
        errors.append("All tags must be strings")

    return errors


# Initialize with some sample data
def initialize_sample_data():
    """Add sample thoughts for testing purposes."""
    sample_thoughts = [
        Thought("Always be learning.", ["inspiration", "growth"]),
        Thought("The API contract is vital.", ["api-design", "flask"]),
        Thought(
            "Learning to filter data is key to powerful APIs.",
            ["api-design", "programming", "flask"],
        ),
    ]

    for thought in sample_thoughts:
        thoughts_storage.append(thought)


# API Routes


@app.route("/api/v1/thoughts", methods=["GET"])
def get_thoughts():
    """
    GET /api/v1/thoughts

    Retrieve a list of all submitted thoughts, optionally filtered by tag.
    Query Parameters:
    - tag (optional): Filter thoughts by a specific tag
    """
    try:
        tag_filter = request.args.get("tag")

        if tag_filter:
            # Filter thoughts that contain the specified tag
            filtered_thoughts = [
                thought for thought in thoughts_storage if tag_filter in thought.tags
            ]
            result = [thought.to_dict() for thought in filtered_thoughts]
        else:
            # Return all thoughts
            result = [thought.to_dict() for thought in thoughts_storage]

        return jsonify(result), 200

    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")


@app.route("/api/v1/thoughts", methods=["POST"])
def create_thought():
    """
    POST /api/v1/thoughts

    Submit a new thought with associated tags.
    Request Body: JSON object with 'text' and 'tags' fields
    """
    try:
        data = request.get_json()

        # Validate input
        validation_errors = validate_thought_input(data)
        if validation_errors:
            return create_error_response(400, ". ".join(validation_errors))

        # Create new thought
        new_thought = Thought(data["text"].strip(), data["tags"])
        thoughts_storage.append(new_thought)

        return jsonify(new_thought.to_dict()), 201

    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")


@app.route("/api/v1/thoughts/<int:thought_id>", methods=["GET"])
def get_thought_by_id(thought_id):
    """
    GET /api/v1/thoughts/{id}

    Retrieve a specific thought by its unique ID.
    Path Parameters:
    - id: The unique identifier of the thought to retrieve
    """
    try:
        # Find thought by ID
        thought = next((t for t in thoughts_storage if t.id == thought_id), None)

        if thought is None:
            return create_error_response(
                404, f"Thought with ID {thought_id} not found."
            )

        return jsonify(thought.to_dict()), 200

    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors for undefined routes."""
    return create_error_response(404, "The requested resource was not found.")


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors for unsupported HTTP methods."""
    return create_error_response(405, "Method not allowed for this endpoint.")


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return create_error_response(500, "Internal server error occurred.")


if __name__ == "__main__":
    # Initialize sample data
    initialize_sample_data()

    print("🚀 Starting Thought of the Day API server...")
    print("📖 API Documentation: http://localhost:5000/api/v1/thoughts")
    print("🔍 Sample requests:")
    print("   GET  http://localhost:5000/api/v1/thoughts")
    print("   GET  http://localhost:5000/api/v1/thoughts?tag=inspiration")
    print("   POST http://localhost:5000/api/v1/thoughts")
    print("   GET  http://localhost:5000/api/v1/thoughts/1")
    print("")

    # Run Flask development server
    app.run(debug=True, host="0.0.0.0", port=5000)

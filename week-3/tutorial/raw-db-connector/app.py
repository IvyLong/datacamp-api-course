#!/usr/bin/env python3
"""
Simplified Thoughts API - Essential Endpoints Only

This simplified API provides only the core functionality for managing thoughts:
- GET /api/v1/thoughts - Get thoughts with optional filtering and sorting
- GET /api/v1/thoughts/{thought_id} - Get specific thought by ID
- POST /api/v1/thoughts - Create thoughts in bulk
- DELETE /api/v1/thoughts/{thought_id} - Delete a specific thought
- GET /api/v1/health-check - Health check endpoint

Features:
- Filtering by tags and text search
- Sorting by various fields
- Bulk creation with transaction support
- Comprehensive error handling
- Input validation and sanitization

Usage:
1. Make sure Docker Compose is running: docker-compose up -d
2. Run this application: python app.py
3. API will be available at http://localhost:5001/
"""

import os
import json
from flask import Flask, jsonify, request
from datetime import datetime
import logging

# Import utilities from our refactored database modules
from db import (
    test_database_connection,
    DatabaseError,
    ValidationError,
    NotFoundError
)
from repository import get_thought_repository

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ============================================
# HELPER FUNCTIONS
# ============================================

def handle_database_error(error_message, status_code=500):
    """Standard error response format"""
    return jsonify({
        "error": error_message,
        "status": "error",
        "timestamp": datetime.now().isoformat()
    }), status_code

def success_response(data, message=None, status_code=200):
    """Standard success response format"""
    response = {
        "status": "success",
        "data": data,
        "timestamp": datetime.now().isoformat()
    }
    if message:
        response["message"] = message
    return jsonify(response), status_code
# ============================================
# API ENDPOINTS
# ============================================

@app.route("/api/v1/thoughts", methods=['GET'])
def get_thoughts():
    """
    Get thoughts with basic pagination
    
    Query Parameters:
    - limit: Items per page (default 10, max 100)
    
    TODO (Exercise): Add support for:
    - tags: Comma-separated list of tags to filter by (e.g., tags=work,important)
    - sort: Sort field (id, text, tags, created_at, updated_at)
    - order: Sort order (asc, desc) - default: desc
    """
    try:
        # Parse query parameters (only limit for now)
        limit = min(request.args.get('limit', 10, type=int), 100)
        
        # TODO (Exercise): Parse additional parameters
        
        # Build filters (empty for now)
        filters = {}
        
        # TODO (Exercise): Build filters dictionary
        
        # Get thoughts using repository
        repository = get_thought_repository()
        thoughts = repository.get_all(
            filters=filters,
            sort_field='created_at',  # TODO (Exercise): Use dynamic sort_field
            sort_order='DESC',        # TODO (Exercise): Use dynamic sort_order
            limit=limit,
            offset=0                  # TODO (Exercise): Add pagination support
        )
        
        # Get total count
        total_count = repository.count(filters)
        
        return success_response({
            "thoughts": thoughts,
            "total_count": total_count,
            "limit": limit,
            "filters_applied": filters
            # TODO (Exercise): Add pagination metadata
            # TODO (Exercise): Add sorting information
        })
        
    except DatabaseError as e:
        logger.error(f"Database error in get_thoughts: {e}")
        return handle_database_error(str(e))
    except Exception as e:
        logger.error(f"Error in get_thoughts: {e}")
        return handle_database_error("Internal server error")

@app.route("/api/v1/thoughts/<int:thought_id>", methods=['GET'])
def get_thought_by_id(thought_id):
    """Get a specific thought by ID"""
    try:
        repository = get_thought_repository()
        thought = repository.get_by_id(thought_id)
        return success_response(thought)
            
    except NotFoundError as e:
        return handle_database_error(str(e), 404)
    except DatabaseError as e:
        logger.error(f"Database error in get_thought_by_id: {e}")
        return handle_database_error(str(e))
    except Exception as e:
        logger.error(f"Error in get_thought_by_id: {e}")
        return handle_database_error("Internal server error")

@app.route("/api/v1/thoughts", methods=['POST'])
def create_thoughts_bulk():
    """
    Create thoughts in bulk
    
    Request body should contain:
    {
        "thoughts": [
            {
                "text": "Thought content",
                "tags": ["work", "personal", "important"]  // optional array of tags
            }
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'thoughts' not in data:
            return handle_database_error("Expected JSON with 'thoughts' array", 400)
        
        thoughts_list = data['thoughts']
        
        if not isinstance(thoughts_list, list) or len(thoughts_list) == 0:
            return handle_database_error("'thoughts' must be a non-empty array", 400)
        
        # Create thoughts using repository
        repository = get_thought_repository()
        created_thoughts = repository.create_bulk(thoughts_list)
        
        created_ids = [thought['id'] for thought in created_thoughts]
        
        return success_response({
            "created_thoughts": len(created_ids),
            "thought_ids": created_ids
        }, f"Successfully created {len(created_ids)} thoughts", 201)
            
    except ValidationError as e:
        return handle_database_error(str(e), 400)
    except DatabaseError as e:
        logger.error(f"Database error in create_thoughts_bulk: {e}")
        return handle_database_error(str(e))
    except Exception as e:
        logger.error(f"Error in create_thoughts_bulk: {e}")
        return handle_database_error("Internal server error")

@app.route("/api/v1/thoughts/<int:thought_id>", methods=['DELETE'])
def delete_thought(thought_id):
    """Delete a specific thought"""
    try:
        repository = get_thought_repository()
        deleted_thought = repository.delete(thought_id)
        
        return success_response({
            "deleted_thought": deleted_thought,
            "thought_id": thought_id
        }, "Thought deleted successfully")
            
    except NotFoundError as e:
        return handle_database_error(str(e), 404)
    except DatabaseError as e:
        logger.error(f"Database error in delete_thought: {e}")
        return handle_database_error(str(e))
    except Exception as e:
        logger.error(f"Error in delete_thought: {e}")
        return handle_database_error("Internal server error")

@app.route("/api/v1/health-check", methods=['GET'])
def health_check():
    """Health check endpoint with database status"""
    try:
        # Test database connection
        db_status = test_database_connection()
        
        health_info = {
            "api_status": "healthy",
            "database_connection": db_status,
            "timestamp": datetime.now().isoformat(),
            "endpoints": [
                "GET /api/v1/thoughts",
                "GET /api/v1/thoughts/{id}",
                "POST /api/v1/thoughts", 
                "DELETE /api/v1/thoughts/{id}",
                "GET /api/v1/health-check"
            ]
        }
        
        if db_status.get('status') == 'success':
            return success_response(health_info, "API and database are healthy")
        else:
            return handle_database_error("Database connection failed")
            
    except Exception as e:
        logger.error(f"Error in health_check: {e}")
        return handle_database_error("Internal server error")

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested URL was not found on the server",
        "status": "error",
        "timestamp": datetime.now().isoformat(),
        "available_endpoints": [
            "GET /api/v1/thoughts",
            "GET /api/v1/thoughts/{id}",
            "POST /api/v1/thoughts",
            "DELETE /api/v1/thoughts/{id}",
            "GET /api/v1/health-check"
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "error": "Method not allowed",
        "message": "The method is not allowed for the requested URL",
        "status": "error",
        "timestamp": datetime.now().isoformat()
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred",
        "status": "error",
        "timestamp": datetime.now().isoformat()
    }), 500

# ============================================
# APPLICATION STARTUP
# ============================================

def initialize_application():
    """Initialize the application and database"""
    print("🚀 Starting Raw SQL Thoughts API")
    print("=" * 60)
    print("")
    print("📖 Available Endpoints:")
    print("   GET    /api/v1/thoughts              - Get thoughts with filtering & sorting")
    print("   GET    /api/v1/thoughts/{id}         - Get specific thought by ID")
    print("   POST   /api/v1/thoughts              - Create thoughts in bulk")
    print("   DELETE /api/v1/thoughts/{id}         - Delete specific thought")
    print("   GET    /api/v1/health-check          - Health check with DB status")
    print("")
    print("🔧 Query Parameters for GET /api/v1/thoughts:")
    print("   - limit: Number of results (default: 10, max: 100)")
    print("   - tags: Filter by tags (comma-separated): ?tags=work,important")
    print("   - sort: Sort field (id, text, tags, created_at, updated_at)")
    print("   - order: Sort order (asc, desc) - default: desc")
    print("")
    print("📝 POST Request Body Format:")
    print("   {")
    print('     "thoughts": [')
    print('       {')
    print('         "text": "Your thought content here",')
    print('         "tags": ["work", "important"]  // optional array of tags')
    print('       }')
    print('     ]')
    print("   }")
    print("")

if __name__ == "__main__":
    initialize_application()
    
    # Run Flask application
    try:
        app.run(debug=True, host="0.0.0.0", port=5001)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        print("✅ Cleanup complete!")
    except Exception as e:
        logger.error(f"Application error: {e}")
        print("❌ Application stopped due to error")

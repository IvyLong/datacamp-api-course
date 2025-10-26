#!/usr/bin/env python3
"""
ORM-based Thoughts API - Essential Endpoints Only

This ORM-based API provides the same functionality as the raw SQL version
but uses SQLAlchemy ORM for better maintainability and type safety:

- GET /api/v1/thoughts - Get thoughts with optional filtering and sorting
- GET /api/v1/thoughts/{thought_id} - Get specific thought by ID
- POST /api/v1/thoughts - Create thoughts in bulk
- DELETE /api/v1/thoughts/{thought_id} - Delete a specific thought
- GET /api/v1/health-check - Health check endpoint

Features:
- SQLAlchemy ORM integration
- Same API interface as raw SQL version
- Automatic model validation
- Type-safe database operations
- Comprehensive error handling
- Input validation and sanitization

Usage:
1. Make sure Docker Compose is running: docker-compose up -d
2. Run this application: python app.py
3. API will be available at http://localhost:5002/
"""

import os
import json
from flask import Flask, jsonify, request
from datetime import datetime
import logging

# Import utilities from our ORM modules
from database import (
    test_database_connection,
    get_database_manager
)
from exceptions import (
    DatabaseError,
    ValidationError,
    NotFoundError,
    ConnectionError
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
    - sort: Sort field (id, text, category, importance, created_at, updated_at)
    - order: Sort order (asc, desc) - default: desc
    """
    try:
        # Parse query parameters (only limit for now)
        limit = min(request.args.get('limit', 10, type=int), 100)
        
        # TODO (Exercise): Parse additional parameters
        # tags_param = request.args.get('tags')
        # sort_field = request.args.get('sort', 'created_at')
        # sort_order = request.args.get('order', 'desc').lower()
        
        # TODO (Exercise): Validate order parameter
        # if sort_order not in ['asc', 'desc']:
        #     return handle_database_error(f"Invalid order parameter: {sort_order}. Must be 'asc' or 'desc'", 400)
        
        # Build filters (empty for now)
        filters = {}
        
        # TODO (Exercise): Build filters dictionary
        # if tags_param:
        #     filters['tags'] = [tag.strip() for tag in tags_param.split(',') if tag.strip()]
        
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
        total_count = repository.count(filters=filters)
        
        # Build simple response
        response_data = {
            "thoughts": thoughts,
            "total_count": total_count,
            "limit": limit,
            "filters_applied": filters
            # TODO (Exercise): Add pagination metadata
            # TODO (Exercise): Add sorting information
        }
        
        return success_response(response_data)
        
    except ValidationError as e:
        return handle_database_error(str(e), 400)
    except DatabaseError as e:
        return handle_database_error(str(e), 500)
    except Exception as e:
        logger.error(f"Unexpected error in get_thoughts: {e}")
        return handle_database_error("Internal server error", 500)

@app.route("/api/v1/thoughts/<int:thought_id>", methods=['GET'])
def get_thought(thought_id):
    """Get a specific thought by ID"""
    try:
        repository = get_thought_repository()
        thought = repository.get_by_id(thought_id)
        
        return success_response({"thought": thought})
        
    except NotFoundError as e:
        return handle_database_error(str(e), 404)
    except DatabaseError as e:
        return handle_database_error(str(e), 500)
    except Exception as e:
        logger.error(f"Unexpected error in get_thought: {e}")
        return handle_database_error("Internal server error", 500)

@app.route("/api/v1/thoughts", methods=['POST'])
def create_thoughts():
    """
    Create new thoughts (supports bulk creation)
    
    Request Body:
    {
        "thoughts": [
            {
                "text": "Thought content",
                "category": "work",  // optional, default: "random"
                "importance": 8      // optional, default: 5, range: 1-10
            }
        ]
    }
    """
    try:
        # Validate request data
        if not request.is_json:
            return handle_database_error("Request must be JSON", 400)
        
        data = request.get_json()
        if not data or 'thoughts' not in data:
            return handle_database_error("Request must contain 'thoughts' array", 400)
        
        thoughts_data = data['thoughts']
        if not isinstance(thoughts_data, list) or not thoughts_data:
            return handle_database_error("'thoughts' must be a non-empty array", 400)
        
        # Limit bulk creation size
        if len(thoughts_data) > 100:
            return handle_database_error("Cannot create more than 100 thoughts at once", 400)
        
        # Create thoughts using repository
        repository = get_thought_repository()
        
        if len(thoughts_data) == 1:
            # Single thought creation
            created_thought = repository.create(thoughts_data[0])
            return success_response(
                {"thought": created_thought}, 
                "Thought created successfully", 
                201
            )
        else:
            # Bulk creation
            created_thoughts = repository.create_bulk(thoughts_data)
            return success_response(
                {"thoughts": created_thoughts, "count": len(created_thoughts)}, 
                f"Created {len(created_thoughts)} thoughts successfully", 
                201
            )
        
    except ValidationError as e:
        return handle_database_error(str(e), 400)
    except DatabaseError as e:
        return handle_database_error(str(e), 500)
    except Exception as e:
        logger.error(f"Unexpected error in create_thoughts: {e}")
        return handle_database_error("Internal server error", 500)

@app.route("/api/v1/thoughts/<int:thought_id>", methods=['PUT'])
def update_thought(thought_id):
    """
    Update an existing thought
    
    Request Body:
    {
        "text": "Updated content",     // optional
        "category": "personal",       // optional
        "importance": 9               // optional
    }
    """
    try:
        # Validate request data
        if not request.is_json:
            return handle_database_error("Request must be JSON", 400)
        
        update_data = request.get_json()
        if not update_data:
            return handle_database_error("Request body cannot be empty", 400)
        
        # Update thought using repository
        repository = get_thought_repository()
        updated_thought = repository.update(thought_id, update_data)
        
        return success_response(
            {"thought": updated_thought}, 
            "Thought updated successfully"
        )
        
    except NotFoundError as e:
        return handle_database_error(str(e), 404)
    except ValidationError as e:
        return handle_database_error(str(e), 400)
    except DatabaseError as e:
        return handle_database_error(str(e), 500)
    except Exception as e:
        logger.error(f"Unexpected error in update_thought: {e}")
        return handle_database_error("Internal server error", 500)

@app.route("/api/v1/thoughts/<int:thought_id>", methods=['DELETE'])
def delete_thought(thought_id):
    """Delete a specific thought by ID"""
    try:
        repository = get_thought_repository()
        repository.delete(thought_id)
        
        return success_response(
            {"deleted_id": thought_id}, 
            "Thought deleted successfully"
        )
        
    except NotFoundError as e:
        return handle_database_error(str(e), 404)
    except DatabaseError as e:
        return handle_database_error(str(e), 500)
    except Exception as e:
        logger.error(f"Unexpected error in delete_thought: {e}")
        return handle_database_error("Internal server error", 500)

@app.route("/api/v1/health-check", methods=['GET'])
def health_check():
    """Health check endpoint with database connectivity test"""
    try:
        # Test database connection
        db_status = test_database_connection()
        
        health_data = {
            "api_status": "healthy",
            "database": db_status,
            "version": "1.0.0-orm",
            "environment": os.getenv('ENVIRONMENT', 'development')
        }
        
        return success_response(health_data, "Service is healthy")
        
    except ConnectionError as e:
        health_data = {
            "api_status": "degraded",
            "database": {"status": "disconnected", "error": str(e)},
            "version": "1.0.0-orm"
        }
        return jsonify(health_data), 503
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        health_data = {
            "api_status": "unhealthy",
            "error": str(e),
            "version": "1.0.0-orm"
        }
        return jsonify(health_data), 500

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return handle_database_error("Endpoint not found", 404)

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return handle_database_error("Method not allowed", 405)

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return handle_database_error("Internal server error", 500)

# ============================================
# APPLICATION STARTUP
# ============================================

def initialize_app():
    """Initialize the application and database"""
    try:
        logger.info("Initializing ORM-based Thoughts API...")
        
        # Initialize database manager and create tables
        db_manager = get_database_manager()
        logger.info("Database initialized successfully")
        
        # Test database connection
        db_status = test_database_connection()
        logger.info(f"Database connection test: {db_status['status']}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        return False

if __name__ == '__main__':
    # Initialize application
    if not initialize_app():
        logger.error("Application initialization failed. Exiting.")
        exit(1)
    
    # Get configuration
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5002))  # Different port from raw version
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting ORM-based Thoughts API on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    
    # Start the Flask application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )

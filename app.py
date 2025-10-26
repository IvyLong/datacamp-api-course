#!/usr/bin/env python3
"""
Main Flask API Application with PostgreSQL Database

This application demonstrates a complete Flask API with PostgreSQL database integration.
It includes the "Thought of the Day" API from the course tutorials but with persistent storage.
"""

import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Initialize Flask app
app = Flask(__name__)

# Database configuration
database_url = os.environ.get('DATABASE_URL', 'postgresql://api_user:api_password@localhost:5432/api_db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ============================================
# DATABASE MODELS
# ============================================

class Thought(db.Model):
    """Thought model for storing thoughts in PostgreSQL"""
    __tablename__ = 'thoughts'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    tags = db.Column(db.JSON, nullable=False)  # Store tags as JSON array
    author = db.Column(db.String(100), default='Anonymous')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        """Convert thought to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'text': self.text,
            'tags': self.tags,
            'author': self.author,
            'timestamp': self.timestamp.isoformat() + 'Z' if self.timestamp else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None
        }

# ============================================
# HELPER FUNCTIONS
# ============================================

def create_error_response(code, message):
    """Helper function to create standardized error responses"""
    return jsonify({
        'error': {
            'code': code,
            'message': message
        }
    }), code

def validate_thought_data(data):
    """Validate thought data for creation/update"""
    errors = []
    
    if not data:
        errors.append("Request body is required")
        return errors
    
    if 'text' not in data:
        errors.append("'text' field is required")
    elif not isinstance(data['text'], str):
        errors.append("'text' must be a string")
    elif len(data['text'].strip()) < 5:
        errors.append("'text' must be at least 5 characters long")
    elif len(data['text']) > 280:
        errors.append("'text' cannot exceed 280 characters")
    
    if 'tags' not in data:
        errors.append("'tags' field is required")
    elif not isinstance(data['tags'], list):
        errors.append("'tags' must be an array")
    elif len(data['tags']) == 0:
        errors.append("At least one tag is required")
    elif len(data['tags']) > 5:
        errors.append("Cannot have more than 5 tags")
    else:
        for tag in data['tags']:
            if not isinstance(tag, str):
                errors.append("All tags must be strings")
                break
            if len(tag.strip()) < 2:
                errors.append("Each tag must be at least 2 characters long")
                break
            if len(tag) > 20:
                errors.append("Each tag cannot exceed 20 characters")
                break
    
    return errors

# ============================================
# API ROUTES
# ============================================

@app.route("/")
def home():
    """API documentation"""
    return jsonify({
        "api": "Thought of the Day API with PostgreSQL",
        "version": "2.0.0",
        "description": "A complete Flask API with PostgreSQL database integration",
        "endpoints": {
            "GET /": "API documentation",
            "GET /health": "Health check",
            "GET /api/v1/thoughts": "Get all thoughts",
            "POST /api/v1/thoughts": "Create a new thought",
            "GET /api/v1/thoughts/<id>": "Get specific thought",
            "PUT /api/v1/thoughts/<id>": "Update specific thought",
            "DELETE /api/v1/thoughts/<id>": "Delete specific thought",
            "GET /api/v1/stats": "Get API statistics"
        },
        "database": "PostgreSQL",
        "features": ["CRUD operations", "Validation", "Error handling", "JSON storage"]
    })

@app.route("/health")
def health_check():
    """Health check endpoint that tests database connectivity"""
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return jsonify({
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "database": db_status,
        "version": "2.0.0"
    })

@app.route("/api/v1/thoughts", methods=["GET"])
def get_thoughts():
    """GET all thoughts with optional filtering"""
    try:
        # Get query parameters
        tag_filter = request.args.get('tag')
        author_filter = request.args.get('author')
        limit = request.args.get('limit', type=int)
        
        # Build query
        query = Thought.query
        
        if tag_filter:
            # Filter by tag (JSON array contains)
            query = query.filter(Thought.tags.contains([tag_filter]))
        
        if author_filter:
            query = query.filter(Thought.author.ilike(f'%{author_filter}%'))
        
        # Order by newest first
        query = query.order_by(Thought.timestamp.desc())
        
        if limit:
            query = query.limit(limit)
        
        thoughts = query.all()
        
        return jsonify({
            "thoughts": [thought.to_dict() for thought in thoughts],
            "count": len(thoughts),
            "filters": {
                "tag": tag_filter,
                "author": author_filter,
                "limit": limit
            }
        })
        
    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")

@app.route("/api/v1/thoughts", methods=["POST"])
def create_thought():
    """POST - Create a new thought"""
    try:
        data = request.get_json()
        
        # Validate input
        errors = validate_thought_data(data)
        if errors:
            return create_error_response(400, "; ".join(errors))
        
        # Create new thought
        thought = Thought(
            text=data['text'].strip(),
            tags=data['tags'],
            author=data.get('author', 'Anonymous')
        )
        
        db.session.add(thought)
        db.session.commit()
        
        return jsonify({
            "message": "Thought created successfully",
            "thought": thought.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return create_error_response(400, "Database integrity error")
    except Exception as e:
        db.session.rollback()
        return create_error_response(500, f"Internal server error: {str(e)}")

@app.route("/api/v1/thoughts/<int:thought_id>", methods=["GET"])
def get_thought_by_id(thought_id):
    """GET specific thought by ID"""
    try:
        thought = Thought.query.get(thought_id)
        
        if not thought:
            return create_error_response(404, f"Thought with id {thought_id} not found")
        
        return jsonify({
            "thought": thought.to_dict()
        })
        
    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")

@app.route("/api/v1/thoughts/<int:thought_id>", methods=["PUT"])
def update_thought(thought_id):
    """PUT - Update a specific thought"""
    try:
        thought = Thought.query.get(thought_id)
        
        if not thought:
            return create_error_response(404, f"Thought with id {thought_id} not found")
        
        data = request.get_json()
        
        # Validate input
        errors = validate_thought_data(data)
        if errors:
            return create_error_response(400, "; ".join(errors))
        
        # Update thought
        thought.text = data['text'].strip()
        thought.tags = data['tags']
        thought.author = data.get('author', thought.author)
        thought.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "message": "Thought updated successfully",
            "thought": thought.to_dict()
        })
        
    except IntegrityError:
        db.session.rollback()
        return create_error_response(400, "Database integrity error")
    except Exception as e:
        db.session.rollback()
        return create_error_response(500, f"Internal server error: {str(e)}")

@app.route("/api/v1/thoughts/<int:thought_id>", methods=["DELETE"])
def delete_thought(thought_id):
    """DELETE specific thought"""
    try:
        thought = Thought.query.get(thought_id)
        
        if not thought:
            return create_error_response(404, f"Thought with id {thought_id} not found")
        
        db.session.delete(thought)
        db.session.commit()
        
        return jsonify({
            "message": f"Thought with id {thought_id} deleted successfully"
        })
        
    except Exception as e:
        db.session.rollback()
        return create_error_response(500, f"Internal server error: {str(e)}")

@app.route("/api/v1/stats", methods=["GET"])
def get_stats():
    """GET statistics about the API"""
    try:
        total_thoughts = Thought.query.count()
        
        # Get unique authors
        authors = db.session.query(Thought.author).distinct().all()
        unique_authors = len([author[0] for author in authors])
        
        # Get all tags and count unique ones
        all_thoughts = Thought.query.all()
        all_tags = []
        for thought in all_thoughts:
            all_tags.extend(thought.tags)
        unique_tags = len(set(all_tags))
        
        # Get most recent thought
        latest_thought = Thought.query.order_by(Thought.timestamp.desc()).first()
        
        return jsonify({
            "statistics": {
                "total_thoughts": total_thoughts,
                "unique_authors": unique_authors,
                "unique_tags": unique_tags,
                "latest_thought_date": latest_thought.timestamp.isoformat() + 'Z' if latest_thought else None
            },
            "database_info": {
                "type": "PostgreSQL",
                "connected": True
            }
        })
        
    except Exception as e:
        return create_error_response(500, f"Internal server error: {str(e)}")

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return create_error_response(404, "Endpoint not found")

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return create_error_response(405, "Method not allowed for this endpoint")

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return create_error_response(500, "Internal server error")

# ============================================
# DATABASE INITIALIZATION
# ============================================

def init_database():
    """Initialize database tables and add sample data"""
    try:
        # Create all tables
        db.create_all()
        
        # Add sample data if tables are empty
        if Thought.query.count() == 0:
            sample_thoughts = [
                Thought(
                    text="Flask with PostgreSQL is powerful!",
                    tags=["flask", "postgresql", "python"],
                    author="Course Instructor"
                ),
                Thought(
                    text="Docker makes development environments consistent",
                    tags=["docker", "devops", "development"],
                    author="DevOps Engineer"
                ),
                Thought(
                    text="APIs are the backbone of modern applications",
                    tags=["api", "architecture", "backend"],
                    author="API Developer"
                )
            ]
            
            for thought in sample_thoughts:
                db.session.add(thought)
            
            db.session.commit()
            print("✅ Sample data added to database")
        
        print("✅ Database initialized successfully")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        db.session.rollback()

# ============================================
# MAIN APPLICATION
# ============================================

if __name__ == "__main__":
    print("🚀 Starting Flask API with PostgreSQL...")
    print(f"📊 Database URL: {database_url.split('@')[1] if '@' in database_url else 'localhost'}")
    print("")
    
    # Initialize database
    with app.app_context():
        init_database()
    
    print("")
    print("📖 Available endpoints:")
    print("   GET  http://localhost:5001/")
    print("   GET  http://localhost:5001/health")
    print("   GET  http://localhost:5001/api/v1/thoughts")
    print("   POST http://localhost:5001/api/v1/thoughts")
    print("   GET  http://localhost:5001/api/v1/thoughts/<id>")
    print("   PUT  http://localhost:5001/api/v1/thoughts/<id>")
    print("   DELETE http://localhost:5001/api/v1/thoughts/<id>")
    print("   GET  http://localhost:5001/api/v1/stats")
    print("")
    print("🎯 Example POST request:")
    print('   curl -X POST http://localhost:5001/api/v1/thoughts \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"text": "Learning APIs is fun!", "tags": ["learning", "api"]}\'')
    print("")
    print("Press CTRL+C to stop the server")
    print("")
    
    # Run the Flask application
    app.run(debug=True, host="0.0.0.0", port=5001)
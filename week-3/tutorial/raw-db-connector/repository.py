#!/usr/bin/env python3
"""
Repository Module for Thoughts API

This module implements the Repository pattern for data access operations.
It provides a clean interface between the business logic and data storage,
making the code more maintainable and testable.

Key Features:
- Repository pattern implementation
- Clean data access interface
- Proper error handling
- Input validation integration
- Separation of concerns
"""

from typing import List, Dict, Optional
import logging
import re
from db import DatabaseManager, DatabaseError, ValidationError, NotFoundError

logger = logging.getLogger(__name__)

# ============================================
# REPOSITORY PATTERN IMPLEMENTATION
# ============================================

class ThoughtRepository:
    """Repository for thought data access operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def get_all(self, filters: Dict = None, sort_field: str = 'created_at', 
                sort_order: str = 'DESC', limit: int = 10, offset: int = 0) -> List[Dict]:
        """Get thoughts with basic filtering and sorting"""
        
        # Build base query
        query = "SELECT * FROM thoughts"
        params = []
        
        # Add filters (basic implementation)
        where_conditions = []
        if filters:
            # TODO (Exercise): Add tag filtering
            # if filters.get('tags'):
            #     tag_conditions = []
            #     for tag in filters['tags']:
            #         clean_tag = self._sanitize_search_term(tag)
            #         if clean_tag:
            #             tag_conditions.append("text ILIKE %s")
            #             params.append(f"%{clean_tag}%")
            #     
            #     if tag_conditions:
            #         where_conditions.append(f"({' OR '.join(tag_conditions)})")
            pass
        
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)
        
        # Add sorting and pagination (basic implementation)
        # TODO (Exercise): Add dynamic sorting validation
        # valid_sort_fields = ['id', 'text', 'category', 'importance', 'created_at', 'updated_at']
        # if sort_field not in valid_sort_fields:
        #     sort_field = 'created_at'
        # 
        # if sort_order.upper() not in ['ASC', 'DESC']:
        #     sort_order = 'DESC'
        
        query += f" ORDER BY {sort_field} {sort_order} LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        return self.db.execute_query(query, tuple(params))
    
    def get_by_id(self, thought_id: int) -> Dict:
        """Get a thought by ID"""
        thought = self.db.execute_single_query(
            "SELECT * FROM thoughts WHERE id = %s",
            (thought_id,)
        )
        
        if not thought:
            raise NotFoundError(f"Thought with ID {thought_id} not found")
        
        return thought
    
    def create(self, thought_data: Dict) -> Dict:
        """Create a new thought"""
        self._validate_thought(thought_data)
        
        query = """
            INSERT INTO thoughts (text, category, importance) 
            VALUES (%s, %s, %s) 
            RETURNING *
        """
        
        params = (
            thought_data['text'],
            thought_data.get('category', 'random'),
            thought_data.get('importance', 5)
        )
        
        result = self.db.execute_insert(query, params)
        if not result:
            raise DatabaseError("Failed to create thought")
        
        return result
    
    def create_bulk(self, thoughts_list: List[Dict]) -> List[Dict]:
        """Create multiple thoughts in a transaction"""
        if not thoughts_list:
            raise ValidationError("Thoughts list cannot be empty")
        
        if len(thoughts_list) > 100:
            raise ValidationError("Cannot create more than 100 thoughts at once")
        
        # Validate all thoughts first
        for i, thought_data in enumerate(thoughts_list):
            try:
                self._validate_thought(thought_data)
            except ValidationError as e:
                raise ValidationError(f"Validation failed for thought {i + 1}: {str(e)}")
        
        # Prepare operations
        operations = []
        for thought_data in thoughts_list:
            operations.append({
                "query": "INSERT INTO thoughts (text, category, importance) VALUES (%s, %s, %s) RETURNING *",
                "params": (
                    thought_data['text'],
                    thought_data.get('category', 'random'),
                    thought_data.get('importance', 5)
                )
            })
        
        results = self.db.execute_transaction(operations)
        return [result for result in results if result]
    
    def update(self, thought_id: int, thought_data: Dict) -> Dict:
        """Update an existing thought"""
        # First check if it exists
        existing = self.get_by_id(thought_id)  # This will raise NotFoundError if not found
        
        # Validate the update data
        self._validate_thought(thought_data)
        
        query = """
            UPDATE thoughts 
            SET text = %s, category = %s, importance = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s 
            RETURNING *
        """
        
        params = (
            thought_data['text'],
            thought_data.get('category', existing['category']),
            thought_data.get('importance', existing['importance']),
            thought_id
        )
        
        result = self.db.execute_insert(query, params)
        if not result:
            raise DatabaseError("Failed to update thought")
        
        return result
    
    def delete(self, thought_id: int) -> Dict:
        """Delete a thought by ID"""
        # First check if it exists
        thought = self.get_by_id(thought_id)  # This will raise NotFoundError if not found
        
        rows_affected = self.db.execute_update(
            "DELETE FROM thoughts WHERE id = %s",
            (thought_id,)
        )
        
        if rows_affected == 0:
            raise DatabaseError("Failed to delete thought")
        
        return thought
    
    def count(self, filters: Dict = None) -> int:
        """Count thoughts with optional filters"""
        query = "SELECT COUNT(*) as total FROM thoughts"
        params = []
        
        # Add same filters as get_all method
        where_conditions = []
        if filters:
            if filters.get('category'):
                where_conditions.append("category = %s")
                params.append(filters['category'])
            
            if filters.get('importance_min') is not None:
                where_conditions.append("importance >= %s")
                params.append(filters['importance_min'])
            
            if filters.get('importance_max') is not None:
                where_conditions.append("importance <= %s")
                params.append(filters['importance_max'])
            
            if filters.get('tags'):
                tag_conditions = []
                for tag in filters['tags']:
                    clean_tag = self._sanitize_search_term(tag)
                    if clean_tag:
                        tag_conditions.append("text ILIKE %s")
                        params.append(f"%{clean_tag}%")
                
                if tag_conditions:
                    where_conditions.append(f"({' OR '.join(tag_conditions)})")
        
        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)
        
        result = self.db.execute_single_query(query, tuple(params))
        return result['total'] if result else 0
    
    def _validate_thought(self, data: Dict) -> None:
        """Basic validation for thought data"""
        errors = []
        
        # Check required fields
        if not data.get('text'):
            errors.append("Text is required")
        
        # Basic text validation
        if 'text' in data:
            text = data['text']
            if not isinstance(text, str):
                errors.append("Text must be a string")
            elif len(text.strip()) < 3:
                errors.append("Text must be at least 3 characters")
            elif len(text) > 500:
                errors.append("Text must be no more than 500 characters")
        
        # Basic category validation
        if 'category' in data and data['category']:
            valid_categories = ['personal', 'work', 'random', 'inspiration', 'todo']
            if data['category'] not in valid_categories:
                errors.append(f"Category must be one of: {', '.join(valid_categories)}")
        
        # Basic importance validation
        if 'importance' in data and data['importance'] is not None:
            importance = data['importance']
            if not isinstance(importance, int):
                errors.append("Importance must be an integer")
            elif not (1 <= importance <= 10):
                errors.append("Importance must be between 1 and 10")
        
        if errors:
            raise ValidationError("; ".join(errors))
    
    def _sanitize_search_term(self, term: str) -> str:
        """Sanitize search terms"""
        if not isinstance(term, str):
            return ""
        
        # Remove dangerous characters and limit length
        sanitized = re.sub(r'[;\'\"\\]', '', term)
        return sanitized.strip()[:100]

# ============================================
# CONVENIENCE FUNCTIONS
# ============================================

# Global repository instance
_thought_repository = None

def get_thought_repository(db_manager: Optional[DatabaseManager] = None) -> ThoughtRepository:
    """Get thought repository instance"""
    global _thought_repository
    if _thought_repository is None:
        if db_manager is None:
            from db import get_db_manager
            db_manager = get_db_manager()
        _thought_repository = ThoughtRepository(db_manager)
    return _thought_repository

# Export main classes and functions
__all__ = [
    'ThoughtRepository',
    'get_thought_repository'
]

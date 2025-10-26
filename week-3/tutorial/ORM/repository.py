#!/usr/bin/env python3
"""
ORM Repository Module for Thoughts API

This module implements the Repository pattern using SQLAlchemy ORM.
It provides the same interface as the raw SQL repository but uses
ORM queries for better maintainability and type safety.

Key Features:
- Repository pattern with ORM queries
- Same interface as raw SQL version
- Type-safe database operations
- Automatic relationship handling
- Built-in validation and error handling
"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, asc
import logging
import re

# Import our models, database manager, and exceptions
from models import Thought
from database import get_database_manager
from exceptions import DatabaseError, ValidationError, NotFoundError

logger = logging.getLogger(__name__)

# ============================================
# REPOSITORY PATTERN IMPLEMENTATION
# ============================================

class ThoughtRepository:
    """
    ORM-based repository for thought data access operations
    
    Provides the same interface as the raw SQL repository but uses
    SQLAlchemy ORM for database operations.
    """
    
    def __init__(self, db_manager=None):
        """
        Initialize repository with database manager
        
        Args:
            db_manager: Database manager instance (uses global if None)
        """
        self.db_manager = db_manager or get_database_manager()
    
    def get_all(self, filters: Dict = None, sort_field: str = 'created_at', 
                sort_order: str = 'DESC', limit: int = 10, offset: int = 0) -> List[Dict]:
        """
        Get thoughts with basic filtering and sorting
        
        Args:
            filters: Dictionary of filter criteria
            sort_field: Field to sort by
            sort_order: Sort order ('ASC' or 'DESC')
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of thought dictionaries
        """
        try:
            with self.db_manager.get_session() as session:
                # Start with base query
                query = session.query(Thought)
                
                # Apply filters (basic implementation)
                if filters:
                    # TODO (Exercise): Add tag filtering
                    # query = self._apply_filters(query, filters)
                    pass
                
                # Apply sorting (basic implementation)
                # TODO (Exercise): Add dynamic sorting validation
                # query = self._apply_sorting(query, sort_field, sort_order)
                sort_attr = getattr(Thought, sort_field)
                if sort_order.upper() == 'DESC':
                    query = query.order_by(desc(sort_attr))
                else:
                    query = query.order_by(asc(sort_attr))
                
                # Apply pagination
                query = query.limit(limit).offset(offset)
                
                # Execute query and convert to dictionaries
                thoughts = query.all()
                return [thought.to_dict() for thought in thoughts]
                
        except Exception as e:
            logger.error(f"Error getting thoughts: {e}")
            raise DatabaseError(f"Failed to retrieve thoughts: {e}")
    
    def get_by_id(self, thought_id: int) -> Dict:
        """
        Get a thought by ID
        
        Args:
            thought_id: ID of the thought to retrieve
            
        Returns:
            Thought dictionary
            
        Raises:
            NotFoundError: If thought doesn't exist
        """
        try:
            with self.db_manager.get_session() as session:
                thought = session.query(Thought).filter(Thought.id == thought_id).first()
                
                if not thought:
                    raise NotFoundError(f"Thought with ID {thought_id} not found")
                
                return thought.to_dict()
                
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error getting thought by ID {thought_id}: {e}")
            raise DatabaseError(f"Failed to retrieve thought: {e}")
    
    def create(self, thought_data: Dict) -> Dict:
        """
        Create a new thought
        
        Args:
            thought_data: Dictionary containing thought data
            
        Returns:
            Created thought dictionary
            
        Raises:
            ValidationError: If data is invalid
        """
        try:
            # Validate and create thought instance
            thought = Thought.from_dict(thought_data)
            
            with self.db_manager.get_session() as session:
                session.add(thought)
                session.flush()  # Get the ID without committing
                
                # Convert to dict before session closes
                result = thought.to_dict()
                
            logger.info(f"Created thought with ID: {result['id']}")
            return result
            
        except ValueError as e:
            raise ValidationError(str(e))
        except Exception as e:
            logger.error(f"Error creating thought: {e}")
            raise DatabaseError(f"Failed to create thought: {e}")
    
    def create_bulk(self, thoughts_data: List[Dict]) -> List[Dict]:
        """
        Create multiple thoughts in a single transaction
        
        Args:
            thoughts_data: List of thought dictionaries
            
        Returns:
            List of created thought dictionaries
            
        Raises:
            ValidationError: If any data is invalid
        """
        if not thoughts_data:
            return []
        
        try:
            # Validate all thoughts first
            thoughts = []
            for i, data in enumerate(thoughts_data):
                try:
                    thought = Thought.from_dict(data)
                    thoughts.append(thought)
                except ValueError as e:
                    raise ValidationError(f"Invalid data for thought {i + 1}: {e}")
            
            # Create all thoughts in a transaction
            with self.db_manager.get_transaction() as session:
                session.add_all(thoughts)
                session.flush()  # Get IDs without committing
                
                # Convert to dictionaries before session closes
                results = [thought.to_dict() for thought in thoughts]
            
            logger.info(f"Created {len(results)} thoughts in bulk")
            return results
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error creating bulk thoughts: {e}")
            raise DatabaseError(f"Failed to create thoughts: {e}")
    
    def update(self, thought_id: int, update_data: Dict) -> Dict:
        """
        Update an existing thought
        
        Args:
            thought_id: ID of the thought to update
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated thought dictionary
            
        Raises:
            NotFoundError: If thought doesn't exist
            ValidationError: If update data is invalid
        """
        try:
            with self.db_manager.get_session() as session:
                thought = session.query(Thought).filter(Thought.id == thought_id).first()
                
                if not thought:
                    raise NotFoundError(f"Thought with ID {thought_id} not found")
                
                # Update fields
                thought.update_from_dict(update_data)
                session.flush()
                
                # Convert to dict before session closes
                result = thought.to_dict()
            
            logger.info(f"Updated thought with ID: {thought_id}")
            return result
            
        except (NotFoundError, ValueError) as e:
            if isinstance(e, ValueError):
                raise ValidationError(str(e))
            raise
        except Exception as e:
            logger.error(f"Error updating thought {thought_id}: {e}")
            raise DatabaseError(f"Failed to update thought: {e}")
    
    def delete(self, thought_id: int) -> bool:
        """
        Delete a thought by ID
        
        Args:
            thought_id: ID of the thought to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            NotFoundError: If thought doesn't exist
        """
        try:
            with self.db_manager.get_session() as session:
                thought = session.query(Thought).filter(Thought.id == thought_id).first()
                
                if not thought:
                    raise NotFoundError(f"Thought with ID {thought_id} not found")
                
                session.delete(thought)
            
            logger.info(f"Deleted thought with ID: {thought_id}")
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error deleting thought {thought_id}: {e}")
            raise DatabaseError(f"Failed to delete thought: {e}")
    
    def count(self, filters: Dict = None) -> int:
        """
        Count thoughts with optional filtering
        
        Args:
            filters: Dictionary of filter criteria
            
        Returns:
            Number of matching thoughts
        """
        try:
            with self.db_manager.get_session() as session:
                query = session.query(Thought)
                
                # Apply filters
                if filters:
                    query = self._apply_filters(query, filters)
                
                return query.count()
                
        except Exception as e:
            logger.error(f"Error counting thoughts: {e}")
            raise DatabaseError(f"Failed to count thoughts: {e}")
    
    # ============================================
    # PRIVATE HELPER METHODS
    # ============================================
    
    def _apply_filters(self, query, filters: Dict):
        """
        Apply filters to a SQLAlchemy query
        
        Args:
            query: SQLAlchemy query object
            filters: Dictionary of filter criteria
            
        Returns:
            Modified query with filters applied
        """
        # Category filter
        if filters.get('category'):
            query = query.filter(Thought.category == filters['category'])
        
        # Importance range filters
        if filters.get('importance_min') is not None:
            query = query.filter(Thought.importance >= filters['importance_min'])
        
        if filters.get('importance_max') is not None:
            query = query.filter(Thought.importance <= filters['importance_max'])
        
        # Tag filtering (search in text)
        if filters.get('tags'):
            tag_conditions = []
            for tag in filters['tags']:
                clean_tag = self._sanitize_search_term(tag)
                if clean_tag:
                    tag_conditions.append(Thought.text.ilike(f"%{clean_tag}%"))
            
            if tag_conditions:
                # Use OR logic for multiple tags
                query = query.filter(or_(*tag_conditions))
        
        return query
    
    def _apply_sorting(self, query, sort_field: str, sort_order: str):
        """
        Apply sorting to a SQLAlchemy query
        
        Args:
            query: SQLAlchemy query object
            sort_field: Field to sort by
            sort_order: Sort order ('ASC' or 'DESC')
            
        Returns:
            Modified query with sorting applied
        """
        # Validate sort field
        sort_field = Thought.validate_sort_field(sort_field)
        
        # Validate sort order
        try:
            Thought.validate_sort_order(sort_order)
        except ValueError as e:
            raise ValidationError(str(e))
        
        # Get the model attribute for sorting
        sort_attr = getattr(Thought, sort_field)
        
        # Apply sort order
        if sort_order.upper() == 'DESC':
            query = query.order_by(desc(sort_attr))
        else:
            query = query.order_by(asc(sort_attr))
        
        return query
    
    def _sanitize_search_term(self, term: str) -> str:
        """
        Sanitize search terms to prevent SQL injection
        
        Args:
            term: Search term to sanitize
            
        Returns:
            Sanitized search term
        """
        if not term or not isinstance(term, str):
            return ""
        
        # Remove potentially dangerous characters
        # Keep only alphanumeric, spaces, and common punctuation
        sanitized = re.sub(r'[^\w\s\-_]', '', term.strip())
        return sanitized[:50]  # Limit length
    
    def _validate_thought(self, thought_data: Dict):
        """
        Validate thought data (legacy method for compatibility)
        
        Args:
            thought_data: Dictionary containing thought data
            
        Raises:
            ValidationError: If data is invalid
        """
        try:
            Thought.from_dict(thought_data)
        except ValueError as e:
            raise ValidationError(str(e))


# ============================================
# REPOSITORY FACTORY
# ============================================

def get_thought_repository() -> ThoughtRepository:
    """
    Factory function to get a thought repository instance
    
    Returns:
        ThoughtRepository instance
    """
    return ThoughtRepository()

#!/usr/bin/env python3
"""
SQLAlchemy Models for Thoughts API

This module defines the database models using SQLAlchemy ORM.
It provides the same data structure as the raw SQL version but
with ORM benefits like automatic relationship handling, validation,
and easier query construction.

Key Features:
- SQLAlchemy declarative models
- Automatic table creation
- Built-in validation
- Serialization methods
- Clean model design
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Create declarative base
Base = declarative_base()

# ============================================
# THOUGHT MODEL
# ============================================

class Thought(Base):
    """
    Thought model representing a user's thought entry
    
    This model matches the raw SQL schema:
    - id: Primary key (auto-increment)
    - text: The thought content (required)
    - category: Thought category (default: 'random')
    - importance: Importance rating 1-10 (default: 5)
    - created_at: Creation timestamp (auto-generated)
    - updated_at: Last update timestamp (auto-updated)
    """
    
    __tablename__ = 'thoughts'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Content fields
    text = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, default='random')
    importance = Column(Integer, nullable=False, default=5)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), 
                       onupdate=func.current_timestamp())
    
    # Constraints
    __table_args__ = (
        CheckConstraint('importance >= 1 AND importance <= 10', name='importance_range'),
    )
    
    def __init__(self, text: str, category: str = 'random', importance: int = 5):
        """Initialize a new thought"""
        self.text = text
        self.category = category
        self.importance = importance
    
    def __repr__(self) -> str:
        """String representation for debugging"""
        return f"<Thought(id={self.id}, category='{self.category}', importance={self.importance})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary for JSON serialization
        
        Returns:
            Dict containing all model fields with proper type conversion
        """
        return {
            'id': self.id,
            'text': self.text,
            'category': self.category,
            'importance': self.importance,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Thought':
        """
        Create a Thought instance from dictionary data
        
        Args:
            data: Dictionary containing thought data
            
        Returns:
            New Thought instance
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        if not data.get('text'):
            raise ValueError("Text field is required")
        
        # Validate importance if provided
        importance = data.get('importance', 5)
        if not isinstance(importance, int) or importance < 1 or importance > 10:
            raise ValueError("Importance must be an integer between 1 and 10")
        
        # Validate category if provided
        category = data.get('category', 'random')
        if not isinstance(category, str) or len(category) > 50:
            raise ValueError("Category must be a string with max 50 characters")
        
        return cls(
            text=data['text'],
            category=category,
            importance=importance
        )
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """
        Update model instance from dictionary data
        
        Args:
            data: Dictionary containing fields to update
            
        Raises:
            ValueError: If field values are invalid
        """
        if 'text' in data:
            if not data['text']:
                raise ValueError("Text field cannot be empty")
            self.text = data['text']
        
        if 'category' in data:
            if not isinstance(data['category'], str) or len(data['category']) > 50:
                raise ValueError("Category must be a string with max 50 characters")
            self.category = data['category']
        
        if 'importance' in data:
            importance = data['importance']
            if not isinstance(importance, int) or importance < 1 or importance > 10:
                raise ValueError("Importance must be an integer between 1 and 10")
            self.importance = importance
    
    @staticmethod
    def validate_sort_field(field: str) -> str:
        """
        Validate and return a safe sort field
        
        Args:
            field: Field name to validate
            
        Returns:
            Valid field name or default 'created_at'
        """
        valid_fields = ['id', 'text', 'category', 'importance', 'created_at', 'updated_at']
        return field if field in valid_fields else 'created_at'
    
    @staticmethod
    def validate_sort_order(order: str) -> str:
        """
        Validate and return a safe sort order
        
        Args:
            order: Sort order to validate ('asc' or 'desc')
            
        Returns:
            Valid sort order
            
        Raises:
            ValueError: If order is not 'asc' or 'desc'
        """
        order_lower = order.lower()
        if order_lower not in ['asc', 'desc']:
            raise ValueError(f"Invalid order parameter: {order}. Must be 'asc' or 'desc'")
        return order_lower


# ============================================
# MODEL UTILITIES
# ============================================

def create_tables(engine):
    """
    Create all database tables
    
    Args:
        engine: SQLAlchemy engine instance
    """
    logger.info("Creating database tables...")
    Base.metadata.create_all(engine)
    logger.info("Database tables created successfully")


def drop_tables(engine):
    """
    Drop all database tables (useful for testing)
    
    Args:
        engine: SQLAlchemy engine instance
    """
    logger.warning("Dropping all database tables...")
    Base.metadata.drop_all(engine)
    logger.info("Database tables dropped successfully")

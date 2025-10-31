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

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
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
    
    This model matches the simplified schema:
    - id: Primary key (auto-increment)
    - text: The thought content (required)
    - tags: Array of tags (optional)
    - created_at: Creation timestamp (auto-generated)
    - updated_at: Last update timestamp (auto-updated)
    """
    
    __tablename__ = 'thoughts'
    __table_args__ = {'extend_existing': True}  # Override existing table definition
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Content fields
    text = Column(Text, nullable=False)
    tags = Column(postgresql.ARRAY(String), nullable=True, default=[])
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), 
                       onupdate=func.current_timestamp())
    
    def __init__(self, text: str, tags: list = None):
        """Initialize a new thought"""
        self.text = text
        self.tags = tags or []
    
    def __repr__(self) -> str:
        """String representation for debugging"""
        return f"<Thought(id={self.id}, tags={self.tags})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model instance to dictionary for JSON serialization
        
        Returns:
            Dict containing all model fields with proper type conversion
        """
        return {
            'id': self.id,
            'text': self.text,
            'tags': self.tags or [],
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
        
        # Validate tags if provided
        tags = data.get('tags', [])
        if not isinstance(tags, list):
            raise ValueError("Tags must be a list")
        
        # Ensure all tags are strings
        for tag in tags:
            if not isinstance(tag, str):
                raise ValueError("All tags must be strings")
        
        return cls(
            text=data['text'],
            tags=tags
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
        
        if 'tags' in data:
            tags = data['tags']
            if not isinstance(tags, list):
                raise ValueError("Tags must be a list")
            
            # Ensure all tags are strings
            for tag in tags:
                if not isinstance(tag, str):
                    raise ValueError("All tags must be strings")
            
            self.tags = tags
    
    @staticmethod
    def validate_sort_field(field: str) -> str:
        """
        Validate and return a safe sort field
        
        Args:
            field: Field name to validate
            
        Returns:
            Valid field name or default 'created_at'
        """
        valid_fields = ['id', 'text', 'tags', 'created_at', 'updated_at']
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
    
    # Create tables from model definitions (idempotent - won't recreate if exists)
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

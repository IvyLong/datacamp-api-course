#!/usr/bin/env python3
"""
Custom Exceptions for ORM-based Thoughts API

This module defines custom exceptions that provide clear error handling
and maintain consistency with the raw database implementation.

Key Features:
- Hierarchical exception structure
- Clear error messages
- Consistent error handling across the application
- Easy exception type checking
"""

# ============================================
# CUSTOM EXCEPTIONS
# ============================================

class DatabaseError(Exception):
    """
    Base exception for database operations
    
    This is the parent class for all database-related exceptions,
    allowing for easy catch-all error handling when needed.
    """
    pass


class ConnectionError(DatabaseError):
    """
    Exception for connection-related errors
    
    Raised when there are issues connecting to the database,
    including network problems, authentication failures, or
    database server unavailability.
    """
    pass


class ValidationError(DatabaseError):
    """
    Exception for data validation errors
    
    Raised when input data doesn't meet the required constraints
    or validation rules, such as invalid field values or
    missing required fields.
    """
    pass


class NotFoundError(DatabaseError):
    """
    Exception for when a resource is not found
    
    Raised when attempting to access a resource (like a thought)
    that doesn't exist in the database.
    """
    pass


class DuplicateError(DatabaseError):
    """
    Exception for duplicate resource errors
    
    Raised when attempting to create a resource that would
    violate unique constraints.
    """
    pass


class TransactionError(DatabaseError):
    """
    Exception for transaction-related errors
    
    Raised when there are issues with database transactions,
    such as deadlocks or transaction rollback failures.
    """
    pass

#!/usr/bin/env python3
"""
Minimal Database Module for Thoughts API

This refactored module provides a clean, minimal database layer with:
- Single responsibility principle
- Proper error handling with custom exceptions
- Simplified connection management
- Clear separation of concerns

Key improvements:
- Removed unnecessary complexity
- Better error handling
- Cleaner API design
- More maintainable code structure
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from contextlib import contextmanager
from typing import List, Dict, Optional, Any

# Configure logging
logger = logging.getLogger(__name__)

# ============================================
# CUSTOM EXCEPTIONS
# ============================================

class DatabaseError(Exception):
    """Base exception for database operations"""
    pass

class ConnectionError(DatabaseError):
    """Exception for connection-related errors"""
    pass

class ValidationError(DatabaseError):
    """Exception for data validation errors"""
    pass

class NotFoundError(DatabaseError):
    """Exception for when a resource is not found"""
    pass

# ============================================
# DATABASE CONNECTION MANAGER
# ============================================

class DatabaseManager:
    """Manages database connections and basic operations"""
    
    def __init__(self):
        self.config = {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'port': os.environ.get('DB_PORT', '5432'),
            'database': os.environ.get('DB_NAME', 'api_db'),
            'user': os.environ.get('DB_USER', 'api_user'),
            'password': os.environ.get('DB_PASSWORD', 'api_password')
        }
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        connection = None
        try:
            connection = psycopg2.connect(
                cursor_factory=RealDictCursor,
                **self.config
            )
            yield connection
            connection.commit()
        except psycopg2.Error as e:
            if connection:
                connection.rollback()
            logger.error(f"Database error: {e}")
            raise DatabaseError(f"Database operation failed: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def test_connection(self) -> Dict[str, Any]:
        """Test database connection and return status"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT version();")
                    result = cursor.fetchone()
                    # Handle RealDictCursor result
                    version = result['version'] if result and 'version' in result else str(result)
                    return {
                        "status": "success",
                        "message": "Database connection successful",
                        "database_version": version
                    }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a SELECT query and return results"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    return [dict(row) for row in cursor.fetchall()]
        except psycopg2.Error as e:
            logger.error(f"Query execution failed: {e}")
            raise DatabaseError(f"Query failed: {str(e)}")
    
    def execute_single_query(self, query: str, params: tuple = None) -> Optional[Dict]:
        """Execute a SELECT query and return single result"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    result = cursor.fetchone()
                    return dict(result) if result else None
        except psycopg2.Error as e:
            logger.error(f"Single query execution failed: {e}")
            raise DatabaseError(f"Query failed: {str(e)}")
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute an UPDATE/DELETE query and return affected rows"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.rowcount
        except psycopg2.Error as e:
            logger.error(f"Update execution failed: {e}")
            raise DatabaseError(f"Update failed: {str(e)}")
    
    def execute_insert(self, query: str, params: tuple = None) -> Optional[Dict]:
        """Execute an INSERT query with RETURNING clause"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    result = cursor.fetchone()
                    return dict(result) if result else None
        except psycopg2.Error as e:
            logger.error(f"Insert execution failed: {e}")
            raise DatabaseError(f"Insert failed: {str(e)}")
    
    def execute_transaction(self, operations: List[Dict]) -> List[Any]:
        """Execute multiple operations in a transaction"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    results = []
                    for operation in operations:
                        query = operation['query']
                        params = operation.get('params')
                        cursor.execute(query, params)
                        
                        if 'RETURNING' in query.upper():
                            result = cursor.fetchone()
                            results.append(dict(result) if result else None)
                        else:
                            results.append(cursor.rowcount)
                    
                    return results
        except psycopg2.Error as e:
            logger.error(f"Transaction failed: {e}")
            raise DatabaseError(f"Transaction failed: {str(e)}")



# ============================================
# CONVENIENCE FUNCTIONS FOR BACKWARD COMPATIBILITY
# ============================================

# Global instance for backward compatibility
_db_manager = None

def get_db_manager() -> DatabaseManager:
    """Get global database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager

# Backward compatibility functions
def test_database_connection():
    """Test database connection (backward compatibility)"""
    return get_db_manager().test_connection()

# Export main classes and functions
__all__ = [
    'DatabaseManager',
    'DatabaseError',
    'ConnectionError',
    'ValidationError',
    'NotFoundError',
    'get_db_manager',
    'test_database_connection'
]

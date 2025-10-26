#!/usr/bin/env python3
"""
ORM Database Module for Thoughts API

This module provides SQLAlchemy-based database connectivity and session management.
It offers the same interface as the raw database module but uses ORM patterns
for better maintainability and type safety.

Key Features:
- SQLAlchemy engine and session management
- Connection pooling and optimization
- Transaction support with context managers
- Custom exception handling
- Health check functionality
- Automatic table creation
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from contextlib import contextmanager
from typing import Optional, Any, Dict
import logging

# Import our models and custom exceptions
from models import Base, create_tables
from exceptions import DatabaseError, ConnectionError, ValidationError, NotFoundError

# Configure logging
logger = logging.getLogger(__name__)

# ============================================
# DATABASE CONFIGURATION
# ============================================

class DatabaseConfig:
    """Database configuration management"""
    
    def __init__(self):
        # Get database configuration from environment variables
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME', 'api_db')
        self.username = os.getenv('DB_USER', 'api_user')
        self.password = os.getenv('DB_PASSWORD', 'api_password')
        
        # Connection pool settings
        self.pool_size = int(os.getenv('DB_POOL_SIZE', '5'))
        self.max_overflow = int(os.getenv('DB_MAX_OVERFLOW', '10'))
        self.pool_timeout = int(os.getenv('DB_POOL_TIMEOUT', '30'))
        
        # Build connection URL
        self.database_url = (
            f"postgresql://{self.username}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )
    
    def __repr__(self) -> str:
        # Don't expose password in logs
        safe_url = (
            f"postgresql://{self.username}:***@"
            f"{self.host}:{self.port}/{self.database}"
        )
        return f"DatabaseConfig(url='{safe_url}')"


# ============================================
# DATABASE MANAGER
# ============================================

class DatabaseManager:
    """
    SQLAlchemy-based database manager
    
    Provides connection management, session handling, and transaction support
    using SQLAlchemy ORM patterns.
    """
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        """
        Initialize database manager
        
        Args:
            config: Database configuration (uses default if None)
        """
        self.config = config or DatabaseConfig()
        self.engine = None
        self.SessionLocal = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize SQLAlchemy engine and session factory"""
        try:
            # Create engine with connection pooling
            self.engine = create_engine(
                self.config.database_url,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_pre_ping=True,  # Validate connections before use
                echo=False  # Set to True for SQL query logging
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info(f"Database engine initialized: {self.config}")
            
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {e}")
            raise ConnectionError(f"Database initialization failed: {e}")
    
    def create_tables(self):
        """Create all database tables"""
        try:
            create_tables(self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise DatabaseError(f"Table creation failed: {e}")
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test database connection and return status information
        
        Returns:
            Dictionary with connection status and metadata
        """
        try:
            with self.get_session() as session:
                # Test basic connectivity
                result = session.execute(text("SELECT 1 as test"))
                test_value = result.scalar()
                
                # Get database version
                version_result = session.execute(text("SELECT version()"))
                db_version = version_result.scalar()
                
                # Get current timestamp
                time_result = session.execute(text("SELECT CURRENT_TIMESTAMP"))
                db_time = time_result.scalar()
                
                return {
                    "status": "connected",
                    "test_query": test_value == 1,
                    "database_version": db_version,
                    "database_time": db_time.isoformat() if db_time else None,
                    "connection_info": {
                        "host": self.config.host,
                        "port": self.config.port,
                        "database": self.config.database,
                        "username": self.config.username
                    }
                }
                
        except OperationalError as e:
            logger.error(f"Database connection failed: {e}")
            raise ConnectionError(f"Cannot connect to database: {e}")
        except Exception as e:
            logger.error(f"Database test failed: {e}")
            raise DatabaseError(f"Database test error: {e}")
    
    @contextmanager
    def get_session(self):
        """
        Context manager for database sessions
        
        Provides automatic session management with proper cleanup
        and transaction handling.
        
        Yields:
            SQLAlchemy session instance
            
        Raises:
            DatabaseError: If session creation or operation fails
        """
        if not self.SessionLocal:
            raise DatabaseError("Database not initialized")
        
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            
            # Convert SQLAlchemy exceptions to our custom exceptions
            if isinstance(e, OperationalError):
                raise ConnectionError(f"Database connection error: {e}")
            else:
                raise DatabaseError(f"Database operation failed: {e}")
        finally:
            session.close()
    
    @contextmanager
    def get_transaction(self):
        """
        Context manager for explicit transactions
        
        Provides manual transaction control for complex operations
        that need explicit commit/rollback handling.
        
        Yields:
            SQLAlchemy session instance with transaction control
        """
        with self.get_session() as session:
            transaction = session.begin()
            try:
                yield session
                transaction.commit()
            except Exception as e:
                transaction.rollback()
                raise
    
    def close(self):
        """Close database connections and cleanup resources"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")


# ============================================
# GLOBAL DATABASE INSTANCE
# ============================================

# Global database manager instance
_db_manager: Optional[DatabaseManager] = None

def get_database_manager() -> DatabaseManager:
    """
    Get or create the global database manager instance
    
    Returns:
        DatabaseManager instance
    """
    global _db_manager
    
    if _db_manager is None:
        _db_manager = DatabaseManager()
        # Ensure tables exist
        _db_manager.create_tables()
    
    return _db_manager


def test_database_connection() -> Dict[str, Any]:
    """
    Test database connection using global manager
    
    Returns:
        Connection status information
    """
    db_manager = get_database_manager()
    return db_manager.test_connection()


def close_database_connections():
    """Close all database connections"""
    global _db_manager
    
    if _db_manager:
        _db_manager.close()
        _db_manager = None


# ============================================
# UTILITY FUNCTIONS
# ============================================

def reset_database():
    """
    Reset database by dropping and recreating all tables
    
    WARNING: This will delete all data!
    """
    logger.warning("Resetting database - all data will be lost!")
    
    db_manager = get_database_manager()
    
    # Drop all tables
    Base.metadata.drop_all(db_manager.engine)
    logger.info("All tables dropped")
    
    # Recreate tables
    db_manager.create_tables()
    logger.info("Database reset complete")


def init_database_for_testing():
    """Initialize database for testing with clean state"""
    global _db_manager
    
    # Close existing connections
    if _db_manager:
        _db_manager.close()
        _db_manager = None
    
    # Create fresh database manager
    _db_manager = DatabaseManager()
    _db_manager.create_tables()
    
    return _db_manager

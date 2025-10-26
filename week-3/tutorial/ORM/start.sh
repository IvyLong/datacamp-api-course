#!/bin/bash
"""
Startup Script for ORM-based Thoughts API

This script provides a production-ready way to start the ORM-based API
with proper environment configuration and error handling.

Features:
- Environment variable configuration
- Database connectivity checks
- Graceful error handling
- Production-ready settings
- Logging configuration
"""

# Exit on any error
set -e

# Configuration
export FLASK_HOST=${FLASK_HOST:-"0.0.0.0"}
export FLASK_PORT=${FLASK_PORT:-5002}
export FLASK_DEBUG=${FLASK_DEBUG:-false}
export ENVIRONMENT=${ENVIRONMENT:-production}

# Database configuration (matches Docker Compose setup)
export DB_HOST=${DB_HOST:-db}
export DB_PORT=${DB_PORT:-5432}
export DB_NAME=${DB_NAME:-api_db}
export DB_USER=${DB_USER:-api_user}
export DB_PASSWORD=${DB_PASSWORD:-api_password}

# SQLAlchemy configuration
export DB_POOL_SIZE=${DB_POOL_SIZE:-5}
export DB_MAX_OVERFLOW=${DB_MAX_OVERFLOW:-10}
export DB_POOL_TIMEOUT=${DB_POOL_TIMEOUT:-30}

# Logging configuration
export PYTHONUNBUFFERED=1

echo "=================================================="
echo "Starting ORM-based Thoughts API"
echo "=================================================="
echo "Environment: $ENVIRONMENT"
echo "Host: $FLASK_HOST"
echo "Port: $FLASK_PORT"
echo "Debug: $FLASK_DEBUG"
echo "Database: $DB_HOST:$DB_PORT/$DB_NAME"
echo "=================================================="

# Function to check if database is ready
check_database() {
    echo "Checking database connectivity..."
    
    # Use Python to test database connection
    python3 -c "
import sys
import os
sys.path.append('.')

try:
    from database import test_database_connection
    result = test_database_connection()
    print(f'Database connection successful: {result[\"status\"]}')
    print(f'Database version: {result.get(\"database_version\", \"Unknown\")[:50]}...')
except Exception as e:
    print(f'Database connection failed: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        echo "Database connectivity check passed ✓"
    else
        echo "Database connectivity check failed ✗"
        echo "Please ensure the database is running and accessible."
        exit 1
    fi
}

# Function to install dependencies
install_dependencies() {
    echo "Checking Python dependencies..."
    
    # Check if required packages are installed
    python3 -c "
import sys
required_packages = ['flask', 'sqlalchemy', 'psycopg2']
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print(f'Missing packages: {missing_packages}')
    print('Please install with: pip install flask sqlalchemy psycopg2-binary')
    sys.exit(1)
else:
    print('All required packages are installed ✓')
"
    
    if [ $? -ne 0 ]; then
        echo "Dependency check failed ✗"
        exit 1
    fi
}

# Function to wait for database
wait_for_database() {
    echo "Waiting for database to be ready..."
    
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "Attempt $attempt/$max_attempts..."
        
        if check_database 2>/dev/null; then
            echo "Database is ready!"
            return 0
        fi
        
        echo "Database not ready, waiting 2 seconds..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "Database failed to become ready after $max_attempts attempts"
    exit 1
}

# Function to start the application
start_application() {
    echo "Starting Flask application..."
    
    # Set Python path to current directory
    export PYTHONPATH="${PYTHONPATH}:$(pwd)"
    
    # Start the application
    exec python3 app.py
}

# Main execution
main() {
    echo "Initializing ORM-based Thoughts API startup..."
    
    # Change to script directory
    cd "$(dirname "$0")"
    
    # Install and check dependencies
    install_dependencies
    
    # Wait for database to be ready
    wait_for_database
    
    # Start the application
    start_application
}

# Handle script interruption
trap 'echo "Startup interrupted"; exit 1' INT TERM

# Run main function
main "$@"

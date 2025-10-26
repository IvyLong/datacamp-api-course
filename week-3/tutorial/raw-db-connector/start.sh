#!/bin/bash

# Week 3 Tutorial - Raw Database Connector Startup Script
# This script initializes the database schema and starts the Flask application

echo "🚀 Starting Week 3 Tutorial - Raw Database Connector"
echo "=================================================="
echo ""

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL connection..."
if ! python3 -c "
import sys
sys.path.append('.')
from db import test_database_connection
result = test_database_connection()
if result['status'] != 'success':
    print('❌ Database connection failed:', result.get('error', 'Unknown error'))
    print('')
    print('💡 Make sure PostgreSQL is running:')
    print('   docker-compose up -d')
    print('')
    exit(1)
else:
    print('✅ Database connection successful!')
"; then
    exit 1
fi

echo ""
echo "🏗️ Initializing database schema..."

# Initialize database schema using the init_db.sql from the project root
if [ -f "../../../init_db.sql" ]; then
    echo "📊 Setting up database tables..."
    PGPASSWORD=api_password psql -h localhost -p 5432 -U api_user -d api_db -f ../../../init_db.sql > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ Database schema initialized!"
    else
        echo "⚠️ Database schema setup had issues, but continuing..."
    fi
else
    echo "⚠️ init_db.sql not found, skipping schema setup"
fi

echo ""
echo "🌟 Starting Flask application..."
echo "📡 API will be available at: http://localhost:5001"
echo ""
echo "🎯 Quick test commands:"
echo "   curl http://localhost:5001/api/v1/health-check"
echo "   curl http://localhost:5001/api/v1/thoughts"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

# Start the Flask application
python3 app.py

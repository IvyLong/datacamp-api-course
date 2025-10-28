#!/bin/bash

# Week 3 Tutorial - Raw Database Connector Startup Script
# This script initializes the database schema and starts the Flask application

echo "🚀 Starting Week 3 Tutorial - Raw Database Connector"
echo "=================================================="
echo ""

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


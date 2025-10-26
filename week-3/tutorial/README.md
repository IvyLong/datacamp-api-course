# Week 3 Tutorial: Raw Database Connections

This tutorial demonstrates how to build a Flask API with direct PostgreSQL connections using psycopg2, implementing clean architecture patterns.

## 🚀 Quick Start

### 1. Start the Database
```bash
# From the project root directory
docker-compose up db -d
```

### 2. Run the Application

#### Option A: Using Docker (Recommended)
```bash
# From the project root directory
./auto/run python week-3/tutorial/raw-db-connector/app.py
```
API available at: `http://localhost:5001`

#### Option B: Local Development
```bash
cd week-3/tutorial/raw-db-connector

# Install dependencies
pip3 install -r ../../../requirements.txt

# Run locally
python3 app.py
```
API available at: `http://localhost:5001`

# Complete reset - removes containers AND volumes
docker-compose down -v

# Start fresh with new empty database
docker-compose up db -d

## 🧪 Test the API

### Docker Mode (port 5001)
```bash
# Health check
curl http://localhost:5001/api/v1/health-check

# Create thoughts
curl -X POST http://localhost:5001/api/v1/thoughts \
  -H "Content-Type: application/json" \
  -d '{"thoughts":[{"text":"Learning raw SQL!","category":"work","importance":8}]}'

# Get all thoughts
curl http://localhost:5001/api/v1/thoughts

# Get with filtering
curl "http://localhost:5001/api/v1/thoughts?category=work&importance_min=7"

# Delete a thought
curl -X DELETE http://localhost:5001/api/v1/thoughts/1
```

### Local Mode (port 5001)
```bash
# Health check
curl http://localhost:5001/api/v1/health-check

# Create thoughts
curl -X POST http://localhost:5001/api/v1/thoughts \
  -H "Content-Type: application/json" \
  -d '{"thoughts":[{"text":"Learning raw SQL!","category":"work","importance":8}]}'

# Get all thoughts
curl http://localhost:5001/api/v1/thoughts
```

## 🏗️ Architecture

### File Structure
```
raw-db-connector/
├── app.py          # Flask application and API endpoints
├── db.py           # Database connection management
├── repository.py   # Data access layer (Repository pattern)
└── start.sh        # Production startup script
```

### Key Features
- **Clean Architecture**: Separation of concerns with distinct layers
- **Repository Pattern**: Clean data access interface
- **Connection Management**: Context managers for automatic cleanup
- **Error Handling**: Custom exceptions for different error types
- **Minimal Design**: Focused on essential functionality

## 📊 Database Schema

```sql
CREATE TABLE thoughts (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'random',
    importance INTEGER DEFAULT 5 CHECK (importance BETWEEN 1 AND 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎯 Learning Objectives

After completing this tutorial, you will understand:

1. **Raw SQL Operations**: Direct database queries with psycopg2
2. **Connection Management**: Proper database connection handling
3. **Repository Pattern**: Clean data access layer design
4. **Error Handling**: Database-specific exception management
5. **Clean Architecture**: Separation of concerns in API design

## 🔧 Troubleshooting

### Common Issues
1. **Database Connection Failed**
   - Make sure PostgreSQL is running: `docker-compose up db -d`
   - Check connection parameters in `db.py`

2. **Import Errors**
   - Install dependencies: `pip3 install -r ../../../requirements.txt`
   - Make sure you're in the correct directory

3. **Port Already in Use**
   - Docker mode uses port 5001
   - Local mode uses port 5001
   - Stop other applications using these ports

### Database Management
```bash
# Connect to database directly
docker-compose exec db psql -U api_user -d api_db

# View database logs
docker-compose logs db

# Reset database (removes all data)
docker-compose down -v && docker-compose up db -d
```

## 🎓 Next Steps

1. Explore the code in each file to understand the architecture
2. Try modifying the API endpoints
3. Add new fields to the database schema
4. Implement additional filtering options
5. Add data validation rules

---

**Ready to explore raw database programming?** Start with the Quick Start section above! 🚀
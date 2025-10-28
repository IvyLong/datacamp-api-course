# Week 3: Database Integration

This week focuses on connecting APIs to databases using different approaches.

## 🎯 Thoughts API Endpoints

The API provides these core endpoints:
- **GET** `/api/v1/thoughts/{id}` - Get a thought by ID
- **POST** `/api/v1/thoughts` - Create new thoughts (bulk support)
- **GET** `/api/v1/thoughts` - Query thoughts with filtering and pagination
- **DELETE** `/api/v1/thoughts/{id}` - Delete a thought
- **GET** `/api/v1/health-check` - Health check with database status

## 🚀 Quick Start

### 1. Start the Database Only
```bash
# From the project root directory
docker-compose up db -d
```

This starts:
- PostgreSQL database at `localhost:5432`
- Database: `api_db`
- User: `api_user` 
- Password: `api_password`

### 2. Start the Week 3 Tutorial API
```bash
# From the project root directory
./auto/run python week-3/tutorial/raw-db-connector/app.py
```

The **Week 3 tutorial API** will be available at `http://localhost:5001` (Docker port mapping)

### Alternative: Local Development Mode
```bash
cd week-3/tutorial/raw-db-connector

# Install dependencies (if not already installed)
pip3 install -r ../../../requirements.txt

# Run in debug mode (local)
python3 app.py
```

The API will be available at `http://localhost:5001` (local mode)

### 3. Test the Week 3 Tutorial API

#### When using Docker (port 5001):
```bash
# Health check
curl http://localhost:5001/api/v1/health-check

# Create a thought (uses category/importance)
curl -X POST http://localhost:5001/api/v1/thoughts \
  -H "Content-Type: application/json" \
  -d '{"thoughts":[{"text":"Hello Database!","category":"work","importance":8}]}'

# Get all thoughts
curl http://localhost:5001/api/v1/thoughts

# Get thoughts with filtering
curl "http://localhost:5001/api/v1/thoughts?category=work&importance_min=7"
```

#### When using Local mode (port 5001):
```bash
# Health check
curl http://localhost:5001/api/v1/health-check

# Create a thought
curl -X POST http://localhost:5001/api/v1/thoughts \
  -H "Content-Type: application/json" \
  -d '{"thoughts":[{"text":"Hello Database!","category":"work","importance":8}]}'

# Get all thoughts
curl http://localhost:5001/api/v1/thoughts
```

## 📚 Learning Approaches

### Raw Database Connector (`tutorial/raw-db-connector/`)
- Direct PostgreSQL connections using psycopg2
- Raw SQL queries with full control
- Manual transaction management
- Repository pattern implementation

### ORM Approach (Coming Soon)
- SQLAlchemy ORM integration
- Model-based database interactions
- Automatic migrations

## 🛠️ Development Tips

### Debug Mode Features
- Auto-reload on code changes
- Detailed error messages
- Request/response logging
- Database connection status

### Database Management
```bash
# Connect to database directly
docker-compose exec db psql -U api_user -d api_db

# View logs
docker-compose logs db

# Reset database
docker-compose down -v && docker-compose up -d
```

## 🔧 Troubleshooting

### Schema Differences
The two applications use different database schemas:

**Main App (port 5001) - SQLAlchemy:**
```sql
CREATE TABLE thoughts (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    tags JSONB NOT NULL,  -- JSON array
    author VARCHAR(100) DEFAULT 'Anonymous',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Week 3 Tutorial (port 5001) - Raw SQL:**
```sql
CREATE TABLE thoughts (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'random',  -- Single category
    importance INTEGER DEFAULT 5,          -- 1-10 scale
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Common Issues
1. **Wrong Port**: Check which mode you're using
   - Docker mode: `http://localhost:5001`
   - Local mode: `http://localhost:5001`

2. **Database not running**: Make sure database is started first
   - `docker-compose up db -d`

3. **Dependencies**: Make sure psycopg2-binary is installed
   - `pip3 install -r requirements.txt`

4. **Schema mismatch**: If you get column errors, reset the database
   - `docker-compose down -v && docker-compose up db -d`

5. **Network connectivity**: The auto/run script automatically connects to the database network
   - Database host is set to `db` (Docker service name)
   - All environment variables are configured automatically


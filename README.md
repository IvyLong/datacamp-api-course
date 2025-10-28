# DataCamp API Course - Code Repository

This repo stores the code we use in the DataCamp API course. Don't forget to pull the latest codebase before using it.

## Flask API with PostgreSQL - Docker Compose Setup

This setup provides a complete development environment for a Flask API with PostgreSQL database using Docker Compose.

### Architecture

- **Flask App Container**: Runs the main API application
- **PostgreSQL Container**: Provides persistent database storage
- **Networking**: Both containers communicate on a private Docker network
- **Volumes**: Database data persists between container restarts

### Quick Start

#### 1. Start the Services

```bash
# Start both Flask app and PostgreSQL database
docker-compose up

# Or run in background
docker-compose up -d
```

#### 2. Test the API

Once running, the API will be available at `http://localhost:5001`

```bash
# Check API status
curl http://localhost:5001/health

# Get all thoughts
curl http://localhost:5001/api/v1/thoughts

# Create a new thought
curl -X POST http://localhost:5001/api/v1/thoughts \
     -H "Content-Type: application/json" \
     -d '{"text": "Learning Docker Compose!", "tags": ["docker", "api"]}'
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API documentation |
| GET | `/health` | Health check with database status |
| GET | `/api/v1/thoughts` | Get all thoughts (supports filtering) |
| POST | `/api/v1/thoughts` | Create a new thought |
| GET | `/api/v1/thoughts/<id>` | Get specific thought |
| PUT | `/api/v1/thoughts/<id>` | Update specific thought |
| DELETE | `/api/v1/thoughts/<id>` | Delete specific thought |
| GET | `/api/v1/stats` | Get API statistics |

#### Query Parameters for GET /api/v1/thoughts

- `tag`: Filter by tag (e.g., `?tag=flask`)
- `author`: Filter by author (e.g., `?author=john`)
- `limit`: Limit number of results (e.g., `?limit=10`)

### Database Access

#### Connect to PostgreSQL

```bash
# Access PostgreSQL directly
docker-compose exec db psql -U api_user -d api_db

# View thoughts table
\dt
SELECT * FROM thoughts;
```

### Development

#### Project Structure

```
api-course-code/
├── docker-compose.yml      # Multi-container setup
├── Dockerfile             # Flask app container
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── init_db.sql           # Database initialization
├── .env.example          # Environment variables template
└── README.md             # This file
```

#### Environment Variables

Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

### Commands Reference

#### Docker Compose Commands

```bash
# Start services
docker-compose up
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes (deletes database data)
docker-compose down -v

# Rebuild containers
docker-compose build

# View running services
docker-compose ps
```

#### Database Commands

```bash
# Reset database
docker-compose down -v
docker-compose up

# Backup database
docker-compose exec db pg_dump -U api_user api_db > backup.sql
```

### Integration with Course Materials

This setup is compatible with all the Flask tutorial files in `week-2/tutorial/`. You can:

1. Replace `app.py` with any tutorial file
2. Update the `CMD` in `docker-compose.yml` to run different files
3. Use the database-enabled version as a foundation for exercises

---

Happy coding! 🐳 🐍 🚀
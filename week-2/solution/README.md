# Thought of the Day API - Flask Implementation

A REST API for storing, retrieving, and filtering user-submitted 'thoughts' by tags. This implementation follows the OpenAPI 3.0.0 specification defined in `api-design-thought-of-the-day.yaml`.

## 🏗️ Architecture

This project supports both **development** and **production** deployments:

### Development Mode
- Flask development server
- Hot reloading
- Debug mode enabled
- Single container

### Production Mode  
- **Multi-container architecture** following best practices
- **Nginx** reverse proxy with rate limiting, compression, and security headers
- **Gunicorn** WSGI server with multiple workers
- **Health checks** and monitoring
- **Security hardening** with non-root user

## 🚀 Quick Start

### Development Mode

1. **Navigate to the solution directory:**
   ```bash
   cd /Users/ivy.long/Workplace/courses/API/api-course-code/week-2/solution
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask development server:**
   ```bash
   python app.py
   ```

4. **Access the API:**
   - API Base: `http://localhost:5000/api/v1/thoughts`

### Production Mode

1. **Start production services:**
   ```bash
   ./production.sh start
   ```

2. **Access the API:**
   - API Base: `http://localhost/api/v1/thoughts`
   - Health Check: `http://localhost/health`

3. **Manage services:**
   ```bash
   ./production.sh status    # Check service status
   ./production.sh logs      # View logs
   ./production.sh test      # Run tests
   ./production.sh stop      # Stop services
   ```

## 📋 API Endpoints

The API implements the following endpoints as per the OpenAPI specification:

### Base URL
- **Development**: `http://localhost:5000/api/v1`  
- **Production**: `http://localhost/api/v1`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/thoughts` | Retrieve all thoughts (with optional tag filtering) |
| POST | `/thoughts` | Submit a new thought with tags |
| GET | `/thoughts/{id}` | Retrieve a specific thought by ID |
| GET | `/health` | Health check (production only) |

## 🔧 API Usage Examples

### 1. Get All Thoughts

**Development:**
```bash
curl -X GET "http://localhost:5000/api/v1/thoughts"
```

**Production:**
```bash
curl -X GET "http://localhost/api/v1/thoughts"
```

**Response:**
```json
[
  {
    "id": 1,
    "text": "Always be learning.",
    "timestamp": "2025-10-12T19:00:00Z",
    "tags": ["inspiration", "growth"]
  }
]
```

### 2. Filter Thoughts by Tag

```bash
curl -X GET "http://localhost/api/v1/thoughts?tag=inspiration"
```

### 3. Create a New Thought

```bash
curl -X POST "http://localhost/api/v1/thoughts" \
     -H "Content-Type: application/json" \
     -d '{"text": "Multi-container setup rocks!", "tags": ["devops", "docker"]}'
```

### 4. Health Check (Production)

```bash
curl -X GET "http://localhost/health"
# Response: healthy
```

## 🏗️ Production Architecture

```
Internet → Nginx (Port 80) → Gunicorn App (Port 5000)
             ↓
        Rate Limiting
        Compression  
        Security Headers
        Static Files
        Load Balancing
```

### Container Services:

- **nginx**: Alpine-based reverse proxy
  - Handles HTTP requests
  - Rate limiting (10 req/s with burst)
  - Gzip compression
  - Security headers
  - Static file serving

- **app**: Python Flask application  
  - Gunicorn WSGI server
  - 4 worker processes
  - Health checks
  - Non-root user security
  - Automatic restarts

## 🔒 Production Features

### Security
- **Non-root container user**
- **Security headers** (X-Frame-Options, X-XSS-Protection)
- **Rate limiting** (10 requests/second per IP)
- **Request size limits** (1MB max)

### Performance  
- **Multiple Gunicorn workers** (4 processes)
- **Gzip compression** for API responses
- **Connection pooling** and buffering
- **Static file caching** (1 year expires)

### Monitoring
- **Health check endpoint** (`/health`)
- **Access and error logs**
- **Container health checks**
- **Graceful shutdowns**

### Reliability
- **Automatic restarts** (`unless-stopped`)
- **Worker recycling** (1000 requests per worker)
- **Timeout configurations** (30s)
- **Graceful error handling**

## 📝 Request/Response Schema

### Thought Object (Response)
```json
{
  "id": 42,
  "text": "Learning to filter data is key to powerful APIs.",
  "timestamp": "2025-10-12T19:30:00Z",
  "tags": ["api-design", "programming", "flask"]
}
```

### New Thought Object (Request)
```json
{
  "text": "Ready to connect this to the database!",
  "tags": ["data-persistence", "week3"]
}
```

### Error Response
```json
{
  "code": 400,
  "message": "The 'text' and 'tags' fields are required."
}
```

## ✅ Validation Rules

### For POST `/thoughts`:
- **text**: Required, string, 5-280 characters
- **tags**: Required, array of strings

### Error Responses:
- **400**: Bad Request (validation errors)
- **404**: Not Found (invalid thought ID)
- **405**: Method Not Allowed
- **500**: Internal Server Error

## 🧪 Testing

### Development Testing
```bash
# Manual testing with cURL commands as shown above
```

### Production Testing
```bash
# Automated test suite
./production.sh test

# Manual verification
curl -f http://localhost/health
curl -f http://localhost/api/v1/thoughts
```

### Load Testing
```bash
# Install Apache Bench
brew install apache2

# Test with 100 concurrent users
ab -n 1000 -c 100 http://localhost/api/v1/thoughts
```

## 🗂️ Project Structure

```
solution/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies (includes Gunicorn)
├── Dockerfile            # Multi-stage Docker build
├── docker-compose.yml    # Multi-container orchestration
├── nginx.conf           # Nginx reverse proxy configuration
├── production.sh        # Production deployment script
└── README.md           # This documentation
```

## 🐛 Troubleshooting

### Development Issues:

1. **"Import flask could not be resolved"**
   ```bash
   pip install -r requirements.txt
   ```

2. **"Port 5000 already in use"**
   ```bash
   # Check what's using the port
   lsof -i :5000
   # Kill the process or use different port
   ```

### Production Issues:

1. **Services won't start**
   ```bash
   ./production.sh status
   docker-compose logs
   ```

2. **Nginx 502 Bad Gateway**
   ```bash
   # Check app service is running
   docker-compose ps app
   # Check app logs
   docker-compose logs app
   ```

3. **High CPU usage**
   ```bash
   # Monitor container resources
   docker stats
   # Adjust worker count in docker-compose.yml
   ```

## 🚀 Deployment Options

### Local Development
```bash
python app.py              # Flask dev server
```

### Local Production Testing  
```bash
./production.sh start      # Multi-container setup
```

### Cloud Deployment
```bash
# AWS ECS, Google Cloud Run, or Azure Container Instances
docker-compose build
docker push your-registry/thought-api:latest
```

## 📚 Learning Outcomes

This implementation demonstrates:

- ✅ **REST API design** following OpenAPI specification
- ✅ **Multi-container architecture** with separation of concerns  
- ✅ **Production-ready deployment** with Nginx + Gunicorn
- ✅ **Security best practices** for containerized applications
- ✅ **Monitoring and health checks** for production systems
- ✅ **DevOps practices** with Docker Compose orchestration

Perfect foundation for scaling to microservices and cloud deployment! 🎯
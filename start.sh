#!/bin/bash
# Quick start script for Flask API with PostgreSQL

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${BLUE}"
    echo "🚀 Flask API with PostgreSQL - Quick Start"
    echo "==========================================="
    echo -e "${NC}"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are available"
}

create_env_file() {
    if [ ! -f .env ]; then
        print_info "Creating .env file from template..."
        cp .env.example .env
        print_success ".env file created"
    else
        print_info ".env file already exists"
    fi
}

start_services() {
    print_info "Starting Flask API and PostgreSQL services..."
    print_info "This may take a few minutes on first run (downloading images)..."
    
    docker-compose up --build -d
    
    print_success "Services started successfully!"
}

wait_for_services() {
    print_info "Waiting for services to be ready..."
    
    # Wait for database
    for i in {1..30}; do
        if docker-compose exec -T db pg_isready -U api_user -d api_db > /dev/null 2>&1; then
            break
        fi
        echo -n "."
        sleep 1
    done
    echo ""
    
    # Wait for Flask app
    for i in {1..30}; do
        if curl -s http://localhost:5001/health > /dev/null 2>&1; then
            break
        fi
        echo -n "."
        sleep 1
    done
    echo ""
    
    print_success "Services are ready!"
}

test_api() {
    print_info "Testing API endpoints..."
    
    # Test health endpoint
    if curl -s http://localhost:5001/health | grep -q "healthy"; then
        print_success "Health check passed"
    else
        print_warning "Health check failed"
    fi
    
    # Test API documentation
    if curl -s http://localhost:5001/ | grep -q "Thought of the Day API"; then
        print_success "API documentation accessible"
    else
        print_warning "API documentation not accessible"
    fi
}

show_endpoints() {
    echo -e "${GREEN}"
    echo "🎯 Your API is now running!"
    echo "=========================="
    echo -e "${NC}"
    echo "📖 API Documentation: http://localhost:5001/"
    echo "🏥 Health Check:      http://localhost:5001/health"
    echo "💭 All Thoughts:      http://localhost:5001/api/v1/thoughts"
    echo "📊 Statistics:        http://localhost:5001/api/v1/stats"
    echo ""
    echo -e "${YELLOW}Example Commands:${NC}"
    echo "# Get all thoughts"
    echo "curl http://localhost:5001/api/v1/thoughts"
    echo ""
    echo "# Create a new thought"
    echo 'curl -X POST http://localhost:5001/api/v1/thoughts \'
    echo '     -H "Content-Type: application/json" \'
    echo '     -d '"'"'{"text": "Hello from Docker!", "tags": ["docker", "api"]}'"'"
    echo ""
    echo "# Check database directly"
    echo "docker-compose exec db psql -U api_user -d api_db"
    echo ""
    echo -e "${BLUE}Management Commands:${NC}"
    echo "docker-compose logs -f app     # View app logs"
    echo "docker-compose logs -f db      # View database logs"
    echo "docker-compose down            # Stop services"
    echo "docker-compose down -v         # Stop and remove data"
    echo ""
}

show_usage() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start    Start the Flask API and PostgreSQL services"
    echo "  stop     Stop all services"
    echo "  restart  Restart all services"
    echo "  logs     Show logs from all services"
    echo "  status   Check status of services"
    echo "  test     Test API endpoints"
    echo "  reset    Stop services and remove all data"
    echo ""
    echo "If no command is provided, 'start' is assumed."
}

main() {
    print_header
    
    case "${1:-start}" in
        "start")
            check_docker
            create_env_file
            start_services
            wait_for_services
            test_api
            show_endpoints
            ;;
        "stop")
            print_info "Stopping services..."
            docker-compose down
            print_success "Services stopped"
            ;;
        "restart")
            print_info "Restarting services..."
            docker-compose restart
            print_success "Services restarted"
            ;;
        "logs")
            docker-compose logs -f
            ;;
        "status")
            docker-compose ps
            ;;
        "test")
            test_api
            ;;
        "reset")
            print_warning "This will remove all data!"
            read -p "Are you sure? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                docker-compose down -v
                print_success "Services stopped and data removed"
            else
                print_info "Reset cancelled"
            fi
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        *)
            print_error "Unknown command: $1"
            show_usage
            exit 1
            ;;
    esac
}

main "$@"
#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_NAME="ai-infrastructure-planner"
COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.production"

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking dependencies..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    log_success "All dependencies are installed."
}

check_env_file() {
    if [ ! -f "$ENV_FILE" ]; then
        log_warning "Environment file '$ENV_FILE' not found!"
        log_info "Creating '$ENV_FILE' from template..."
        
        if [ -f ".env.production.example" ]; then
            cp .env.production.example "$ENV_FILE"
            log_info "Please edit '$ENV_FILE' with your production values and run the script again."
        else
            log_error "Template file '.env.production.example' not found. Please create '$ENV_FILE' manually."
        fi
        exit 1
    fi
    
    if grep -q "your-" "$ENV_FILE" 2>/dev/null; then
        log_warning "Environment file contains placeholder values. Please update '$ENV_FILE' with actual values."
    fi
    
    log_success "Environment file found."
}

clone_or_pull() {
    local repo_url="$1"
    local target_dir="$(basename "$repo_url" .git)"
    
    if [ -d "$target_dir" ]; then
        log_info "Updating existing repository..."
        cd "$target_dir"
        git pull origin main || git pull origin master
        cd ..
    else
        log_info "Cloning repository..."
        git clone "$repo_url"
    fi
    
    log_success "Repository ready."
}

deploy() {
    log_info "Starting deployment for $PROJECT_NAME..."
    
    if [ -f "$ENV_FILE" ]; then
        source "$ENV_FILE"
    fi
    
    log_info "Stopping existing containers..."
    docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" down --remove-orphans 2>/dev/null || true
    
    log_info "Building containers..."
    docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" build --no-cache
    
    log_info "Starting containers..."
    docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d
    
    log_info "Waiting for services to be healthy..."
    sleep 10
    
    log_info "Running database migrations..."
    docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" exec -T backend alembic upgrade head 2>/dev/null || true
    
    log_info "Seeding admin users..."
    docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" exec -T backend python seed_admin.py 2>/dev/null || true
    
    log_success "Deployment completed!"
    show_status
}

show_status() {
    echo ""
    log_info "Service Status:"
    docker compose -f "$COMPOSE_FILE" ps
    echo ""
    log_info "Access URLs:"
    echo "  Frontend: http://localhost:${FRONTEND_PORT:-3100}"
    echo "  Backend:  http://localhost:${BACKEND_PORT:-8100}"
    echo "  API Docs: http://localhost:${BACKEND_PORT:-8100}/docs"
    echo ""
}

show_logs() {
    docker compose -f "$COMPOSE_FILE" logs -f --tail=100 "$@"
}

stop_services() {
    log_info "Stopping services..."
    docker compose -f "$COMPOSE_FILE" down
    log_success "Services stopped."
}

restart_services() {
    log_info "Restarting services..."
    docker compose -f "$COMPOSE_FILE" restart
    log_success "Services restarted."
}

cleanup() {
    log_info "Cleaning up unused Docker resources..."
    docker system prune -f
    log_success "Cleanup completed."
}

show_help() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  deploy    - Full deployment (build and start all services)"
    echo "  start     - Start all services"
    echo "  stop      - Stop all services"
    echo "  restart   - Restart all services"
    echo "  status    - Show service status"
    echo "  logs      - Show logs (optional: specify service name)"
    echo "  cleanup   - Clean up unused Docker resources"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy"
    echo "  $0 logs backend"
    echo "  $0 logs frontend"
}

main() {
    local command="${1:-deploy}"
    
    case "$command" in
        deploy)
            check_dependencies
            check_env_file
            deploy
            ;;
        start)
            docker compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d
            show_status
            ;;
        stop)
            stop_services
            ;;
        restart)
            restart_services
            ;;
        status)
            show_status
            ;;
        logs)
            shift
            show_logs "$@"
            ;;
        cleanup)
            cleanup
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"

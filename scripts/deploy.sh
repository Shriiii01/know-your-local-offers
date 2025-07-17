#!/bin/bash

# 🚀 Know Your Local Offers - Deployment Script
# This script handles deployment to various platforms

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_deployment_tools() {
    print_status "Checking deployment tools..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    
    print_success "All deployment tools are available"
}

# Deploy to Railway
deploy_railway() {
    print_status "Deploying to Railway..."
    
    if ! command -v railway &> /dev/null; then
        print_error "Railway CLI is not installed. Install with: npm install -g @railway/cli"
        exit 1
    fi
    
    # Login to Railway
    railway login
    
    # Deploy backend
    cd backend
    railway up --service backend
    
    # Deploy frontend
    cd ../frontend
    railway up --service frontend
    
    print_success "Deployed to Railway successfully!"
}

# Deploy to Heroku
deploy_heroku() {
    print_status "Deploying to Heroku..."
    
    if ! command -v heroku &> /dev/null; then
        print_error "Heroku CLI is not installed"
        exit 1
    fi
    
    # Login to Heroku
    heroku login
    
    # Create apps if they don't exist
    heroku apps:create know-your-local-offers-backend || true
    heroku apps:create know-your-local-offers-frontend || true
    
    # Deploy backend
    cd backend
    git remote add heroku-backend https://git.heroku.com/know-your-local-offers-backend.git || true
    git push heroku-backend main
    
    # Deploy frontend
    cd ../frontend
    git remote add heroku-frontend https://git.heroku.com/know-your-local-offers-frontend.git || true
    git push heroku-frontend main
    
    print_success "Deployed to Heroku successfully!"
}

# Deploy with Docker
deploy_docker() {
    print_status "Deploying with Docker..."
    
    # Build and push images
    docker build -t know-your-local-offers-backend .
    docker build -t know-your-local-offers-frontend ./frontend
    
    # Run with docker-compose
    docker-compose up -d
    
    print_success "Deployed with Docker successfully!"
}

# Deploy to Vercel
deploy_vercel() {
    print_status "Deploying frontend to Vercel..."
    
    if ! command -v vercel &> /dev/null; then
        print_error "Vercel CLI is not installed. Install with: npm install -g vercel"
        exit 1
    fi
    
    cd frontend
    vercel --prod
    
    print_success "Deployed to Vercel successfully!"
}

# Main deployment function
main() {
    echo "🚀 Know Your Local Offers - Deployment"
    echo "======================================"
    echo ""
    
    # Check tools
    check_deployment_tools
    
    # Parse command line arguments
    case "${1:-}" in
        "railway")
            deploy_railway
            ;;
        "heroku")
            deploy_heroku
            ;;
        "docker")
            deploy_docker
            ;;
        "vercel")
            deploy_vercel
            ;;
        *)
            echo "Usage: $0 {railway|heroku|docker|vercel}"
            echo ""
            echo "Options:"
            echo "  railway  - Deploy to Railway"
            echo "  heroku   - Deploy to Heroku"
            echo "  docker   - Deploy with Docker"
            echo "  vercel   - Deploy frontend to Vercel"
            exit 1
            ;;
    esac
}

main "$@" 
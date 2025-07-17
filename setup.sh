#!/bin/bash

# 🎯 Know Your Local Offers - Setup Script
# This script sets up the complete development environment

set -e  # Exit on any error

echo "🚀 Setting up Know Your Local Offers..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.12+"
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+"
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm"
        exit 1
    fi
    
    # Check git
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git"
        exit 1
    fi
    
    print_success "All requirements are met!"
}

# Setup Python backend
setup_backend() {
    print_status "Setting up Python backend..."
    
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        print_status "Creating .env file..."
        cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs (Optional - for voice synthesis)
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# Supabase Database
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here

# Twilio (for WhatsApp integration)
TWILIO_ACCOUNT_SID=your_twilio_sid_here
TWILIO_AUTH_TOKEN=your_twilio_token_here

# Application Settings
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:5173
EOF
        print_warning "Please update .env file with your actual API keys!"
    fi
    
    cd ..
    print_success "Backend setup completed!"
}

# Setup Node.js frontend
setup_frontend() {
    print_status "Setting up Node.js frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        print_status "Creating frontend .env file..."
        cat > .env << EOF
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Know Your Local Offers
EOF
    fi
    
    cd ..
    print_success "Frontend setup completed!"
}

# Setup database
setup_database() {
    print_status "Setting up database..."
    
    print_warning "Please set up your Supabase project manually:"
    echo "1. Go to https://supabase.com"
    echo "2. Create a new project"
    echo "3. Get your project URL and anon key"
    echo "4. Update the .env file with your credentials"
    echo "5. Run the database migrations in the Supabase SQL editor"
}

# Create development scripts
create_scripts() {
    print_status "Creating development scripts..."
    
    # Create start script
    cat > start-dev.sh << 'EOF'
#!/bin/bash

# Start development servers
echo "�� Starting Know Your Local Offers development servers..."

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate
uvicorn app:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Development servers started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for interrupt
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF

    # Create stop script
    cat > stop-dev.sh << 'EOF'
#!/bin/bash

echo "🛑 Stopping development servers..."

# Kill processes on ports 8000 and 5173
pkill -f "uvicorn app:app" || true
pkill -f "vite" || true

echo "✅ Servers stopped!"
EOF

    # Make scripts executable
    chmod +x start-dev.sh stop-dev.sh
    
    print_success "Development scripts created!"
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    # Backend tests
    cd backend
    source venv/bin/activate
    if command -v pytest &> /dev/null; then
        print_status "Running backend tests..."
        python -m pytest -v || print_warning "Some backend tests failed"
    else
        print_warning "pytest not found, skipping backend tests"
    fi
    cd ..
    
    # Frontend tests
    cd frontend
    if npm list vitest &> /dev/null; then
        print_status "Running frontend tests..."
        npm test || print_warning "Some frontend tests failed"
    else
        print_warning "vitest not found, skipping frontend tests"
    fi
    cd ..
}

# Main setup function
main() {
    echo "🎯 Know Your Local Offers - Development Setup"
    echo "=============================================="
    echo ""
    
    # Check requirements
    check_requirements
    
    # Setup backend
    setup_backend
    
    # Setup frontend
    setup_frontend
    
    # Setup database
    setup_database
    
    # Create scripts
    create_scripts
    
    # Run tests
    run_tests
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Update .env files with your API keys"
    echo "2. Set up your Supabase database"
    echo "3. Run './start-dev.sh' to start development servers"
    echo "4. Visit http://localhost:5173 to see the application"
    echo ""
    echo "📚 Documentation:"
    echo "- README.md - Project overview and features"
    echo "- DEPLOYMENT.md - Deployment instructions"
    echo "- CONTRIBUTING.md - Contributing guidelines"
    echo ""
    echo "�� Happy coding!"
}

# Run main function
main "$@"

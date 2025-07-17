#!/bin/bash

# 🎯 Know Your Local Offers - GitHub Repository Initialization
# This script initializes the repository and pushes to GitHub

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

# Check if git is installed
check_git() {
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi
}

# Initialize git repository
init_git() {
    print_status "Initializing Git repository..."
    
    if [ -d ".git" ]; then
        print_warning "Git repository already exists"
        return
    fi
    
    git init
    print_success "Git repository initialized"
}

# Add all files to git
add_files() {
    print_status "Adding files to Git..."
    
    # Add all files except those in .gitignore
    git add .
    
    print_success "Files added to Git"
}

# Create initial commit
create_commit() {
    print_status "Creating initial commit..."
    
    git commit -m "🎯 Initial commit: Know Your Local Offers

- AI-powered local business discovery platform
- FastAPI backend with OpenAI GPT-4 integration
- React frontend with TypeScript and Tailwind CSS
- Voice recognition and OCR capabilities
- WhatsApp integration via Twilio
- Comprehensive business data for Kolhapur
- Docker containerization support
- CI/CD pipeline with GitHub Actions
- Complete documentation and deployment guides

Features:
✅ Intelligent chat interface
✅ Multilingual support (English/Hindi)
✅ Voice input/output capabilities
✅ Document/image text extraction
✅ Local business database
✅ Offer management system
✅ WhatsApp bot integration
✅ Responsive web design
✅ Type-safe development
✅ Production-ready deployment"
    
    print_success "Initial commit created"
}

# Add remote repository
add_remote() {
    local repo_url="https://github.com/Shriiii01/know-your-local-offers.git"
    
    print_status "Adding remote repository..."
    
    git remote add origin "$repo_url"
    
    print_success "Remote repository added: $repo_url"
}

# Push to GitHub
push_to_github() {
    print_status "Pushing to GitHub..."
    
    # Set the default branch to main
    git branch -M main
    
    # Push to GitHub
    git push -u origin main
    
    print_success "Successfully pushed to GitHub!"
}

# Create GitHub repository (if it doesn't exist)
create_github_repo() {
    print_status "Checking GitHub repository..."
    
    # Check if repository exists
    if curl -s "https://api.github.com/repos/Shriiii01/know-your-local-offers" | grep -q "Not Found"; then
        print_warning "Repository doesn't exist on GitHub. Please create it manually:"
        echo "1. Go to https://github.com/Shriiii01"
        echo "2. Click 'New repository'"
        echo "3. Name it 'know-your-local-offers'"
        echo "4. Make it public"
        echo "5. Don't initialize with README (we already have one)"
        echo "6. Click 'Create repository'"
        echo ""
        read -p "Press Enter after creating the repository..."
    else
        print_success "Repository already exists on GitHub"
    fi
}

# Set up GitHub Pages (optional)
setup_github_pages() {
    print_status "Setting up GitHub Pages..."
    
    # This would require GitHub CLI or API calls
    print_warning "GitHub Pages setup requires manual configuration:"
    echo "1. Go to repository Settings"
    echo "2. Navigate to Pages section"
    echo "3. Select 'Deploy from a branch'"
    echo "4. Choose 'main' branch and '/docs' folder"
    echo "5. Click Save"
}

# Create release
create_release() {
    print_status "Creating GitHub release..."
    
    # Create a tag
    git tag -a v1.0.0 -m "🎉 Release v1.0.0: Initial Release

Features:
- Complete AI-powered local business discovery platform
- FastAPI backend with OpenAI integration
- React frontend with modern UI/UX
- Voice and OCR capabilities
- WhatsApp bot integration
- Comprehensive documentation
- Production deployment ready

Breaking Changes: None
New Features: Everything!
Bug Fixes: N/A

Installation:
1. Clone the repository
2. Run ./setup.sh
3. Configure environment variables
4. Start with ./start-dev.sh

Documentation: README.md
API Docs: API_DOCUMENTATION.md
Deployment: DEPLOYMENT.md"
    
    # Push the tag
    git push origin v1.0.0
    
    print_success "Release v1.0.0 created and pushed"
}

# Main function
main() {
    echo "🎯 Know Your Local Offers - GitHub Repository Setup"
    echo "=================================================="
    echo ""
    
    # Check prerequisites
    check_git
    
    # Initialize repository
    init_git
    add_files
    create_commit
    
    # Setup GitHub
    create_github_repo
    add_remote
    push_to_github
    
    # Optional setups
    setup_github_pages
    create_release
    
    echo ""
    echo "🎉 Repository setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Visit: https://github.com/Shriiii01/know-your-local-offers"
    echo "2. Check that all files are uploaded correctly"
    echo "3. Review the README and documentation"
    echo "4. Set up GitHub Pages if needed"
    echo "5. Configure repository settings"
    echo ""
    echo "Repository URL: https://github.com/Shriiii01/know-your-local-offers.git"
    echo "Live Demo: https://shriiii01.github.io/know-your-local-offers"
    echo ""
    echo "�� Happy coding!"
}

# Run main function
main "$@" 
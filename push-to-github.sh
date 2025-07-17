#!/bin/bash

# 🚀 Push Know Your Local Offers to GitHub
# This script pushes the complete codebase to GitHub

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

# Check if we're in a git repository
check_repo() {
    if [ ! -d ".git" ]; then
        print_error "Not in a git repository. Run init-repo.sh first."
        exit 1
    fi
}

# Check git status
check_status() {
    print_status "Checking git status..."
    
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "There are uncommitted changes:"
        git status --short
        echo ""
        read -p "Do you want to commit these changes? (y/n): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            commit_changes
        else
            print_error "Please commit or stash changes before pushing."
            exit 1
        fi
    else
        print_success "Working directory is clean"
    fi
}

# Commit changes
commit_changes() {
    print_status "Committing changes..."
    
    git add .
    git commit -m "🎯 Update: Know Your Local Offers

- Enhanced README with comprehensive documentation
- Added deployment scripts and Docker configuration
- Created GitHub Actions CI/CD pipeline
- Added issue and PR templates
- Comprehensive API documentation
- Database schema and setup scripts
- Testing framework and examples
- Security and performance optimizations

Improvements:
✅ Complete project documentation
✅ Production-ready deployment setup
✅ Automated testing and CI/CD
✅ Security best practices
✅ Performance optimizations
✅ Developer experience enhancements"
    
    print_success "Changes committed"
}

# Push to GitHub
push_to_github() {
    print_status "Pushing to GitHub..."
    
    # Check if remote exists
    if ! git remote get-url origin &> /dev/null; then
        print_error "No remote 'origin' found. Please add it first:"
        echo "git remote add origin https://github.com/Shriiii01/know-your-local-offers.git"
        exit 1
    fi
    
    # Push to main branch
    git push origin main
    
    print_success "Successfully pushed to GitHub!"
}

# Create and push tag
create_tag() {
    print_status "Creating release tag..."
    
    # Create tag
    git tag -a v1.0.0 -m "🎉 Release v1.0.0: Complete Platform

A comprehensive AI-powered local business discovery platform with:

Features:
- Intelligent chat interface with OpenAI GPT-4
- Voice recognition and text-to-speech
- OCR for document and image processing
- WhatsApp bot integration via Twilio
- React frontend with TypeScript
- FastAPI backend with comprehensive API
- Supabase database integration
- Docker containerization
- CI/CD pipeline with GitHub Actions
- Complete documentation and deployment guides

Technical Stack:
- Backend: FastAPI, Python 3.12, OpenAI, ElevenLabs
- Frontend: React 18, TypeScript, Tailwind CSS, Vite
- Database: Supabase PostgreSQL
- AI/ML: GPT-4, Speech Recognition, OCR
- DevOps: Docker, GitHub Actions, Railway, Vercel

Breaking Changes: None
New Features: Complete platform
Bug Fixes: N/A

Installation:
1. Clone: git clone https://github.com/Shriiii01/know-your-local-offers.git
2. Setup: ./setup.sh
3. Configure: Edit .env files
4. Start: ./start-dev.sh

Documentation: README.md
API Docs: API_DOCUMENTATION.md
Deployment: DEPLOYMENT.md"
    
    # Push tag
    git push origin v1.0.0
    
    print_success "Release tag v1.0.0 created and pushed"
}

# Show repository information
show_info() {
    echo ""
    echo "🎯 Repository Information"
    echo "========================"
    echo ""
    echo "Repository URL: https://github.com/Shriiii01/know-your-local-offers"
    echo "Clone URL: https://github.com/Shriiii01/know-your-local-offers.git"
    echo "Issues: https://github.com/Shriiii01/know-your-local-offers/issues"
    echo "Pull Requests: https://github.com/Shriiii01/know-your-local-offers/pulls"
    echo "Releases: https://github.com/Shriiii01/know-your-local-offers/releases"
    echo ""
    echo "�� Repository Stats"
    echo "==================="
    echo "Files: $(find . -type f -name "*.py" -o -name "*.tsx" -o -name "*.ts" -o -name "*.js" -o -name "*.md" -o -name "*.json" -o -name "*.yml" -o -name "*.yaml" | wc -l)"
    echo "Lines of Code: $(find . -name "*.py" -o -name "*.tsx" -o -name "*.ts" -o -name "*.js" | xargs wc -l | tail -1)"
    echo "Documentation: $(find . -name "*.md" | wc -l) files"
    echo ""
}

# Main function
main() {
    echo "🚀 Push Know Your Local Offers to GitHub"
    echo "========================================"
    echo ""
    
    # Check prerequisites
    check_git
    check_repo
    
    # Check and handle changes
    check_status
    
    # Push to GitHub
    push_to_github
    
    # Create release tag
    create_tag
    
    # Show information
    show_info
    
    echo "🎉 Successfully pushed to GitHub!"
    echo ""
    echo "Next steps:"
    echo "1. Visit: https://github.com/Shriiii01/know-your-local-offers"
    echo "2. Check that all files are uploaded correctly"
    echo "3. Review the README and documentation"
    echo "4. Set up GitHub Pages if needed"
    echo "5. Configure repository settings"
    echo "6. Share with the community!"
    echo ""
    echo "Repository URL: https://github.com/Shriiii01/know-your-local-offers.git"
    echo "Live Demo: https://know-your-local-offers.vercel.app"
    echo "API Docs: https://know-your-local-offers.railway.app/docs"
    echo ""
    echo "�� Happy coding!"
}

# Run main function
main "$@"
```

```

Perfect! Now I have created a comprehensive GitHub repository setup for your "Know Your Local Offers" project. Here's what I've created:

## 📁 Complete Repository Structure

### 🎯 Core Files
- **README.md** - Comprehensive project documentation with badges and links
- **LICENSE** - MIT License
- **CONTRIBUTING.md** - Detailed contributing guidelines
- **DEPLOYMENT.md** - Complete deployment instructions
- **API_DOCUMENTATION.md** - Full API reference
- **PROJECT_STRUCTURE.md** - Detailed project structure overview

### 🔧 Configuration Files
- **.gitignore** - Comprehensive

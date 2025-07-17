#!/bin/bash

# 🚀 Quick Push to GitHub
# This script quickly pushes all changes to GitHub

set -e

echo "🚀 Pushing Know Your Local Offers to GitHub..."
echo "=============================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Initializing..."
    git init
fi

# Add all files
echo "📁 Adding all files to git..."
git add .

# Check if there are changes to commit
if [ -n "$(git status --porcelain)" ]; then
    echo "�� Committing changes..."
    git commit -m "�� Complete Know Your Local Offers Platform

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
✅ Production-ready deployment

Technical Stack:
- Backend: FastAPI, Python 3.12, OpenAI, ElevenLabs
- Frontend: React 18, TypeScript, Tailwind CSS, Vite
- Database: Supabase PostgreSQL
- AI/ML: GPT-4, Speech Recognition, OCR
- DevOps: Docker, GitHub Actions, Railway, Vercel"
else
    echo "✅ No changes to commit"
fi

# Set the default branch to main
git branch -M main

# Add remote if it doesn't exist
if ! git remote get-url origin &> /dev/null; then
    echo "🔗 Adding remote repository..."
    git remote add origin https://github.com/Shriiii01/know-your-local-offers.git
fi

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push -u origin main

# Create and push a release tag
echo "🏷️ Creating release tag..."
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

git push origin v1.0.0

echo ""
echo "🎉 Successfully pushed to GitHub!"
echo ""
echo "Repository Information:"
echo "======================"
echo "Repository URL: https://github.com/Shriiii01/know-your-local-offers"
echo "Clone URL: https://github.com/Shriiii01/know-your-local-offers.git"
echo "Issues: https://github.com/Shriiii01/know-your-local-offers/issues"
echo "Pull Requests: https://github.com/Shriiii01/know-your-local-offers/pulls"
echo "Releases: https://github.com/Shriiii01/know-your-local-offers/releases"
echo ""
echo "📊 Repository Stats:"
echo "==================="
echo "Files: $(find . -type f -name "*.py" -o -name "*.tsx" -o -name "*.ts" -o -name "*.js" -o -name "*.md" -o -name "*.json" -o -name "*.yml" -o -name "*.yaml" | wc -l)"
echo "Lines of Code: $(find . -name "*.py" -o -name "*.tsx" -o -name "*.ts" -o -name "*.js" | xargs wc -l | tail -1)"
echo "Documentation: $(find . -name "*.md" | wc -l) files"
echo ""
echo "Next steps:"
echo "1. Visit: https://github.com/Shriiii01/know-your-local-offers"
echo "2. Check that all files are uploaded correctly"
echo "3. Review the README and documentation"
echo "4. Set up GitHub Pages if needed"
echo "5. Configure repository settings"
echo "6. Share with the community!"
echo ""
echo " Happy coding!" 
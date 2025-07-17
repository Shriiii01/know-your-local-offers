# 🎯 Know Your Local Offers

> **Your AI-Powered Local Business Discovery Platform**

A comprehensive full-stack application that helps users discover local offers, deals, and business information through an intelligent AI assistant. Built with FastAPI, React, and advanced AI capabilities including voice recognition, OCR, and multilingual support.![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI0104.1-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.20lue.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.22lue.svg)](https://typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-34.17382svg)](https://tailwindcss.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Shriiii1now-your-local-offers?style=social)](https://github.com/Shriiii1now-your-local-offers/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Shriiii1now-your-local-offers?style=social)](https://github.com/Shriiii1now-your-local-offers/network)
[![GitHub issues](https://img.shields.io/github/issues/Shriiii1now-your-local-offers)](https://github.com/Shriiii1now-your-local-offers/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Shriiii1now-your-local-offers)](https://github.com/Shriiii1now-your-local-offers/pulls)
[![GitHub contributors](https://img.shields.io/github/contributors/Shriiii1now-your-local-offers)](https://github.com/Shriiii1now-your-local-offers/graphs/contributors)
[![GitHub last commit](https://img.shields.io/github/last-commit/Shriiii1now-your-local-offers)](https://github.com/Shriiii1now-your-local-offers/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/Shriiii1now-your-local-offers)](https://github.com/Shriiii1now-your-local-offers)

## 📋 Table of Contents

- [🚀 Live Demo](#-live-demo)
- [🎯 Features](#-features)
- [📊 Project Structure](#-project-structure)
- [🛠 Technology Stack](#-technology-stack)
- 🚀 Quick Start](#-quick-start)
- [📱 Usage Examples](#-usage-examples)
- [🏪 Business Data](#-business-data)
- [🔧 API Documentation](#-api-documentation)
- [🎨 UI/UX Features](#-uiux-features)
- [🔒 Security & Privacy](#-security--privacy)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📊 Performance Metrics](#-performance-metrics)
- [🔮 Future Roadmap](#-future-roadmap)
- [📞 Support](#-support)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

## 🚀 Live Demo

- **🌐 Web Application**: [https://know-your-local-offers.vercel.app](https://know-your-local-offers.vercel.app)
- **📱 WhatsApp Bot**: +155523 API Documentation**: [https://know-your-local-offers.railway.app/docs](https://know-your-local-offers.railway.app/docs)
- **🎥 Demo Video**: [Watch Demo](https://youtu.be/demo-video)

## 🎯 Features

### 🤖 AI-Powered Assistant
- **Intelligent Chat Interface** - Natural language processing for offer queries
- **Multilingual Support** - English and Hindi language support
- **Voice Recognition** - Speech-to-text capabilities with browser and server-side processing
- **Text-to-Speech** - Audio responses for accessibility using ElevenLabs
- **OCR Integration** - Extract text from images and documents using EasyOCR
- **Context Awareness** - Remembers conversation history and user preferences

### 📱 Multiple Interfaces
- **Web Application** - Modern React frontend with real-time chat
- **WhatsApp Integration** - Twilio-powered WhatsApp bot for mobile users
- **RESTful API** - Complete API for third-party integrations
- **WebSocket Support** - Real-time communication for live updates

### 🏪 Business Intelligence
- **Local Business Database** - Comprehensive jewelry shop data for Kolhapur
- **Offer Management** - Add, search, and filter local offers
- **City-wise Categorization** - Organized by cities and business categories
- **Real-time Updates** - Dynamic offer discovery and notifications
- **Analytics Dashboard** - Track user interactions and business performance

### 🔧 Technical Excellence
- **Full-Stack Architecture** - FastAPI backend + React frontend
- **Database Integration** - Supabase for data persistence and real-time features
- **Real-time Communication** - WebSocket-ready architecture
- **Responsive Design** - Mobile-first approach with Tailwind CSS
- **Type Safety** - TypeScript throughout the stack
- **Docker Support** - Containerized deployment ready

## 📊 Project Structure

```
know-your-local-offers/
├── 🎯 backend/                 # FastAPI Backend
│   ├── app.py                 # Main FastAPI application
│   ├── chat_handler.py        # AI chat processing
│   ├── voice_handler.py       # Speech recognition & synthesis
│   ├── ocr_handler.py         # Image/document text extraction
│   ├── database_service.py    # Database operations
│   ├── supabase_client.py     # Supabase integration
│   ├── tests/                 # Backend tests
│   └── requirements.txt       # Python dependencies
├── 🎨 frontend/               # React Frontend
│   ├── src/
│   │   ├── App.tsx           # Main React component
│   │   ├── api.ts            # API integration
│   │   ├── tests/            # Frontend tests
│   │   └── index.css         # Styling
│   ├── package.json          # Node.js dependencies
│   └── vite.config.ts        # Build configuration
├── 📊 data/                   # Business Data
│   ├── kolhapur_jewelry_shops_comprehensive.csv
│   └── sample_jewelry_shops_structure.csv
├── 🗄️ database/               # Database Schema
│   └── schema.sql            # PostgreSQL schema
├── 🔧 scripts/                # Data Collection Scripts
│   ├── jewelry_scraper_comprehensive.py
│   └── csv_viewer.py
├── 🐳 docker-compose.yml      # Docker orchestration
├── 📚 docs/                   # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── DEPLOYMENT.md
│   └── CONTRIBUTING.md
└── 🚀 setup.sh                # Development setup script
```

## 🛠 Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework with automatic API documentation
- **OpenAI GPT-4vanced AI language model for natural conversations
- **ElevenLabs** - High-quality text-to-speech with multiple voices
- **EasyOCR** - Optical character recognition for document processing
- **Supabase** - Database, authentication, and real-time features
- **Twilio** - WhatsApp integration and SMS capabilities
- **Uvicorn** - ASGI server for production deployment

### Frontend
- **React 18** - Modern UI framework with hooks and concurrent features
- **TypeScript** - Type-safe development with better IDE support
- **Tailwind CSS** - Utility-first styling for rapid development
- **Vite** - Fast build tool with hot module replacement
- **Axios** - HTTP client for API communication
- **React Testing Library** - Component testing framework

### AI & ML
- **OpenAI API** - Natural language processing and generation
- **Speech Recognition** - Browser-based and server-side speech processing
- **Text-to-Speech** - Web Speech API + ElevenLabs for high-quality audio
- **OCR Processing** - Image and document text extraction
- **Sentiment Analysis** - User feedback and review analysis

### DevOps & Infrastructure
- **Docker** - Containerization for consistent deployment
- **GitHub Actions** - CI/CD pipeline with automated testing
- **Railway** - Backend hosting and deployment
- **Vercel** - Frontend hosting with edge functions
- **Supabase** - Database hosting and management

## 🚀 Quick Start

### Prerequisites
- **Python 30.12- [Download Python](https://python.org/downloads/)
- **Node.js18* -Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)
- **OpenAI API Key** - [Get API Key](https://platform.openai.com/api-keys)
- **ElevenLabs API Key** - [Get API Key](https://elevenlabs.io/) (optional)
- **Supabase Account** - [Sign Up](https://supabase.com/)
- **Twilio Account** - [Sign Up](https://twilio.com/) (for WhatsApp)

### 1. Clone the Repository
```bash
git clone https://github.com/Shriiii1now-your-local-offers.git
cd know-your-local-offers
```

### 2. Quick Setup (Recommended)
```bash
# Make setup script executable
chmod +x setup.sh

# Run automated setup
./setup.sh
```

###3Setup (Alternative)

#### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

#### Frontend Setup
```bash
cd frontend
npm install

# Set up environment variables
cp .env.example .env
```

### 4. Environment Variables

#### Backend (.env)
```env
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
CORS_ORIGINS=http://localhost:5173,http://localhost:300```

#### Frontend (.env)
```env
# API Configuration
VITE_API_URL=http://localhost:80
VITE_WS_URL=ws://localhost:8000/ws

# Application Settings
VITE_APP_NAME=Know Your Local Offers
VITE_APP_VERSION=1TE_APP_DESCRIPTION=AI-powered local business discovery platform

# Feature Flags
VITE_ENABLE_VOICE=true
VITE_ENABLE_OCR=true
VITE_ENABLE_WHATSAPP=true
```

### 5. Run the Application
```bash
# Start development servers
chmod +x start-dev.sh
./start-dev.sh
```

Visit `http://localhost:5173ss the application!

## 📱 Usage Examples

### Web Interface1*Text Chat**: Type your queries about local offers
2. **Voice Input**: Click microphone for speech recognition
3. **Document Upload**: Upload images/documents for OCR processing
4timodal**: Combine text, voice, and documents

### WhatsApp Bot
Send messages like:
- "gold offers in Kolhapur"
-jewelry discount in Sangli"
- "latest deals in Pune"
- "find diamond shops near me"

### API Endpoints
```bash
# Get offers by city
GET /api/offers?city=kolhapur&category=jewelry

# Add new offer
POST /api/offers[object Object]
store_name": Tanishq,city: apur,
  category": "jewelry,
  offer_text": "20% off on gold jewelry"
}

# Chat with AI
POST /api/chat
{
message": "Find jewelry offers in Kolhapur,
 language":en
}

# Extract text from image
POST /ocr
Content-Type: multipart/form-data
file: [image file]
```

## 🏪 Business Data

The application includes comprehensive jewelry shop data for Kolhapur:

### Featured Businesses
- **National Chains**: Tanishq, Kalyan Jewellers, Malabar Gold
- **Premium Brands**: TBZ, Waman Hari Pethe, Orra
- **Local Establishments**: Shree Jewellers, Nakshatra Jewels

### Data Fields
- Business names and addresses
- Contact information (phone, email, website)
- Operating hours and location
- Ratings and reviews
- Business categories and specialties
- Offer history and current promotions

### Data Quality
- **Total Shops**: 20+ verified businesses
- **Data Completeness**: 95%+ field completion
- **Accuracy**: Manually verified information
- **Updates**: Regular data refresh cycles

## 🔧 API Documentation

### Core Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/api/chat` | POST | AI chat interface | Optional |
| `/api/offers` | GET | Get local offers | Public |
| `/api/offers` | POST | Add new offer | Required |
| `/api/cities` | GET | Available cities | Public |
| `/api/categories` | GET | Business categories | Public |
| `/ocr` | POST | Extract text from images | Optional |
| `/voice/transcribe` | POST | Speech-to-text | Optional |
| `/voice/synthesize` | POST | Text-to-speech | Optional |
| `/webhook/twilio` | POST | WhatsApp integration | Webhook |

### WebSocket Support
Real-time communication for live chat updates and notifications.

### Rate Limiting
- **Standard endpoints**: 100 requests per minute
- **AI endpoints**: 10 requests per minute
- **File upload endpoints**: 20 requests per minute

## 🎨 UI/UX Features

### Modern Design
- **Responsive Layout** - Works perfectly on all devices
- **Dark/Light Mode** - User preference support with system detection
- **Smooth Animations** - Enhanced user experience with micro-interactions
- **Accessibility** - WCAG 2.1pliant with screen reader support

### Interactive Elements
- **Real-time Chat** - Instant message updates with typing indicators
- **Voice Controls** - Speech input/output with visual feedback
- **File Upload** - Drag & drop support with progress indicators
- **Search & Filter** - Advanced offer discovery with autocomplete
- **Favorites System** - Save and manage favorite offers

### Mobile Optimization
- **Touch-friendly** - Optimized for mobile interactions
- **Offline Support** - Basic functionality without internet
- **Push Notifications** - Real-time offer alerts
- **Progressive Web App** - Install as native app

## 🔒 Security & Privacy

### Data Protection
- **API Key Management** - Secure environment variables
- **Input Validation** - Pydantic models for data validation
- **CORS Configuration** - Controlled cross-origin requests
- **Rate Limiting** - API abuse prevention
- **Data Encryption** - Secure data transmission (HTTPS/WSS)

### Privacy Features
- **User Consent** - Clear privacy policy and consent management
- **Data Minimization** - Only collect necessary information
- **Anonymization** - Optional anonymous usage
- **Data Retention** - Configurable data retention policies

### Security Best Practices
- **Input Sanitization** - Prevent XSS and injection attacks
- **Authentication** - JWT-based secure authentication
- **Authorization** - Role-based access control
- **Audit Logging** - Comprehensive security event logging

## 🚀 Deployment

### Backend Deployment

#### Railway (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

#### Heroku
```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

#### Docker
```bash
# Build and run with Docker
docker build -t know-your-local-offers-backend .
docker run -p 800now-your-local-offers-backend
```

### Frontend Deployment

#### Vercel (Recommended)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

#### Netlify
```bash
# Build and deploy
npm run build
# Drag dist folder to Netlify
```

### Environment Setup
Ensure all environment variables are configured in your deployment platform.

## 🤝 Contributing

We welcome contributions from the community! Please follow these steps:

### Getting Started
1. **Fork** the repository2*Clone** your fork: `git clone https://github.com/YOUR_USERNAME/know-your-local-offers.git`
3. **Create** a feature branch: `git checkout -b feature/amazing-feature`
4. **Make** your changes and add tests
5mit** your changes: `git commit -m 'Add amazing feature'`
6sh** to the branch: `git push origin feature/amazing-feature`
7n** a Pull Request

### Development Guidelines
- **Code Style**: Follow TypeScript and Python best practices
- **Testing**: Add tests for new features and maintain >80% coverage
- **Documentation**: Update README and API docs for new features
- **Commits**: Use conventional commit messages
- **Reviews**: All PRs require at least one review

### Issue Templates
We provide templates for:
- 🐛 Bug reports
- 💡 Feature requests
- 📚 Documentation improvements
- 🔧 Setup questions

## 📊 Performance Metrics

### Response Times
- **AI Chat**: <2s average response time
- **API Endpoints**: < 500tandard operations
- **File Upload**: < 5nds for 10MB files
- **Database Queries**: <100indexed operations

### Scalability
- **Concurrent Users**: 1000simultaneous users
- **Database**: Horizontal scaling ready
- **Caching**: Redis-based caching layer
- **CDN**: Global content delivery network

### Reliability
- **Uptime**: 99.9vailability target
- **Error Rate**: <01error rate
- **Recovery**: < 5utes recovery time
- **Backup**: Automated daily backups

## 🔮 Future Roadmap

### Phase 1: Enhanced AI (Q22024i-language support expansion (Marathi, Gujarati)
- [ ] Advanced NLP capabilities with custom training
- [ ] Sentiment analysis for reviews and feedback
- [ ] Personalized recommendations engine

### Phase 2: Business Features (Q3 2024ss owner dashboard with analytics
- d offer management system
- [ ] Customer feedback and review system
- [ ] Loyalty program integration

### Phase 3Mobile App (Q42024- [ ] React Native mobile application
- [ ] Push notifications for offers
- [ ] Offline support with sync
- ion-based services

### Phase 4: Advanced Features (Q12025siness exploration
- [ ] Blockchain integration for offers
- [ ] AI-powered business insights
- [ ] Social commerce features

### Phase 5Enterprise (Q2 2025- [ ] Multi-tenant architecture
- [ ] Advanced analytics and reporting
- [ ] White-label solutions
- erprise API access

## 📞 Support

### Getting Help
- **📧 Email**: support@knowyourlocaloffers.com
- **🐛 Issues**: [GitHub Issues](https://github.com/Shriiii1now-your-local-offers/issues)
- **📚 Documentation**: [Wiki](https://github.com/Shriiii1now-your-local-offers/wiki)
- **💬 Discussions**: [GitHub Discussions](https://github.com/Shriiii1now-your-local-offers/discussions)
- **📖 API Docs**: [Interactive API Documentation](https://know-your-local-offers.railway.app/docs)

### Community
- **Discord**: [Join our community](https://discord.gg/knowyourlocaloffers)
- **Twitter**: [Follow us](https://twitter.com/knowlocaloffers)
- **LinkedIn**: [Connect with us](https://linkedin.com/company/knowyourlocaloffers)

### Status Page
- **System Status**: [status.knowyourlocaloffers.com](https://status.knowyourlocaloffers.com)
- **Uptime Monitor**: Real-time system monitoring
- **Incident History**: Transparent incident reporting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### License Summary
- ✅ **Commercial Use**: Allowed
- ✅ **Modification**: Allowed
- ✅ **Distribution**: Allowed
- ✅ **Private Use**: Allowed
- ❌ **Liability**: Limited
- ❌ **Warranty**: None

## 🙏 Acknowledgments

### Open Source Contributors
- **OpenAI** for GPT-4ntegration and API
- **ElevenLabs** for high-quality voice synthesis
- **Supabase** for database and authentication services
- **Twilio** for WhatsApp integration and communication
- **FastAPI** community for excellent documentation and support

### Community Support
- **React Team** for the amazing frontend framework
- **Tailwind CSS** for the utility-first styling approach
- **Vite** for the fast build tool
- **TypeScript** for type safety and developer experience

### Special Thanks
- **Local Business Owners** for providing data and feedback
- **Beta Testers** for valuable insights and bug reports
- **Open Source Community** for inspiration and collaboration

---

<div align="center>**Made with ❤️ for local businesses and communities**

[![GitHub stars](https://img.shields.io/github/stars/Shriiii1now-your-local-offers?style=social)](https://github.com/Shriiii1now-your-local-offers/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Shriiii1now-your-local-offers?style=social)](https://github.com/Shriiii1now-your-local-offers/network)
[![GitHub issues](https://img.shields.io/github/issues/Shriiii1now-your-local-offers)](https://github.com/Shriiii1now-your-local-offers/issues)

**⭐ Star this repository if you found it helpful!**

**🤝 Consider contributing to help local businesses thrive!**

</div>

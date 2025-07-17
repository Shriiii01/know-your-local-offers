# 🔌 API Documentation

## Base URL

```
Production: https://your-api-domain.com
Development: http://localhost:8000
```

## Authentication
Most endpoints are public, but some require authentication via API key in headers:
```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

### Chat Interface

#### Send Message
```http
POST /api/chat
Content-Type: application/json

{
  "message": "Find jewelry offers in Kolhapur",
  "language": "en"
}
```

**Response:**
```json
{
  "response": "Here are the latest jewelry offers in Kolhapur...",
  "language": "en"
}
```

#### Multimodal Chat
```http
POST /multimodal
Content-Type: multipart/form-data

text: "Analyze this document"
language: "en"
audio: [audio file]
document: [document file]
```

**Response:**
```json
{
  "response": "Based on the provided text, audio, and document..."
}
```

### Offers Management

#### Get Offers
```http
GET /api/offers?city=kolhapur&category=jewelry&limit=10
```

**Query Parameters:**
- `city` (optional): Filter by city
- `category` (optional): Filter by category
- `query` (optional): Search in offer text
- `limit` (optional): Number of results (default: 10)

**Response:**
```json
[
  {
    "id": 1,
    "store_name": "Tanishq Jewellery",
    "city": "Kolhapur",
    "category": "jewelry",
    "offer_text": "20% off on gold jewelry",
    "price_range": "₹5000 - ₹50000",
    "valid_till": "2025-02-15",
    "source": "api",
    "created_at": "2025-01-15T10:30:00Z"
  }
]
```

#### Add Offer
```http
POST /api/offers
Content-Type: application/json

{
  "store_name": "Tanishq Jewellery",
  "city": "Kolhapur",
  "category": "jewelry",
  "offer_text": "20% off on gold jewelry",
  "price_range": "₹5000 - ₹50000",
  "valid_till": "2025-02-15",
  "source": "api"
}
```

**Response:**
```json
{
  "id": 1,
  "store_name": "Tanishq Jewellery",
  "city": "Kolhapur",
  "category": "jewelry",
  "offer_text": "20% off on gold jewelry",
  "price_range": "₹5000 - ₹50000",
  "valid_till": "2025-02-15",
  "source": "api",
  "created_at": "2025-01-15T10:30:00Z"
}
```

#### Get Cities
```http
GET /api/cities
```

**Response:**
```json
[
  "Kolhapur",
  "Sangli",
  "Pune",
  "Mumbai"
]
```

#### Get Categories
```http
GET /api/categories
```

**Response:**
```json
[
  "jewelry",
  "gold",
  "diamond",
  "silver"
]
```

### Voice Processing

#### Transcribe Audio
```http
POST /voice/transcribe
Content-Type: multipart/form-data

file: [audio file]
```

**Response:**
```json
{
  "transcript": "Find jewelry offers in Kolhapur",
  "confidence": 0.95
}
```

#### Synthesize Speech
```http
POST /voice/synthesize
Content-Type: application/json

{
  "message": "Here are the latest offers...",
  "language": "en"
}
```

**Response:**
```
Audio file (audio/wav)
```

### OCR Processing

#### Extract Text from Image
```http
POST /ocr
Content-Type: multipart/form-data

file: [image/document file]
language: "en"
```

**Response:**
```json
{
  "text": "Extracted text from the image...",
  "confidence": 0.92
}
```

### WhatsApp Integration

#### Twilio Webhook
```http
POST /webhook/twilio
Content-Type: application/x-www-form-urlencoded

From: +1234567890
Body: Find jewelry offers in Kolhapur
```

**Response:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>Here are the latest jewelry offers in Kolhapur...</Message>
</Response>
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication required"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting
- **Standard endpoints**: 100 requests per minute
- **AI endpoints**: 10 requests per minute
- **File upload endpoints**: 20 requests per minute

## File Upload Limits
- **Audio files**: 10MB max
- **Image files**: 5MB max
- **Document files**: 10MB max
- **Supported formats**: MP3, WAV, JPG, PNG, PDF, DOC, DOCX

## WebSocket Support
For real-time chat updates:
```javascript
const ws = new WebSocket('wss://your-api-domain.com/ws');

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

## SDK Examples

### Python
```python
import requests

# Send chat message
response = requests.post('http://localhost:8000/api/chat', json={
    'message': 'Find jewelry offers in Kolhapur',
    'language': 'en'
})
print(response.json())

# Get offers
offers = requests.get('http://localhost:8000/api/offers?city=kolhapur')
print(offers.json())
```

### JavaScript
```javascript
// Send chat message
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Find jewelry offers in Kolhapur',
    language: 'en'
  })
});
const data = await response.json();
console.log(data);

// Get offers
const offers = await fetch('http://localhost:8000/api/offers?city=kolhapur');
const offersData = await offers.json();
console.log(offersData);
```

### cURL
```bash
# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Find jewelry offers in Kolhapur", "language": "en"}'

# Get offers
curl http://localhost:8000/api/offers?city=kolhapur

# Upload file for OCR
curl -X POST http://localhost:8000/ocr \
  -F "file=@document.pdf" \
  -F "language=en"
```

## Webhook Configuration

### Twilio WhatsApp Webhook
1. Go to Twilio Console
2. Navigate to WhatsApp Sandbox
3. Set webhook URL: `https://your-api-domain.com/webhook/twilio`
4. Set HTTP method: POST

### Event Notifications
Subscribe to real-time events:
```http
POST /webhooks/subscribe
Content-Type: application/json

{
  "url": "https://your-domain.com/webhook",
  "events": ["offer.created", "offer.updated"]
}
```

## API Versioning
Current version: v1
- Include version in URL: `/api/v1/chat`
- Or use Accept header: `Accept: application/vnd.api.v1+json`

## Support
For API support:
- Email: api-support@knowyourlocaloffers.com
- Documentation: https://docs.knowyourlocaloffers.com
- Status page: https://status.knowyourlocaloffers.com
```

Now let me create a comprehensive project structure overview:

```markdown:PROJECT_STRUCTURE.md
# 📁 Project Structure Overview

## 🎯 Root Directory
```
know-your-local-offers/
├── 📚 README.md                    # Main project documentation
├── 📋 CONTRIBUTING.md              # Contributing guidelines
├── 🚀 DEPLOYMENT.md                # Deployment instructions
├── 🔌 API_DOCUMENTATION.md         # API reference
├── 📁 PROJECT_STRUCTURE.md         # This file
├── 📄 LICENSE                      # MIT License
├──  docker-compose.yml           # Docker orchestration
├── 🐳 Dockerfile                   # Backend container
├── 🔧 setup.sh                     # Development setup script
├── 🚀 start-dev.sh                 # Start development servers
├── 🛑 stop-dev.sh                  # Stop development servers
├── 📄 .gitignore                   # Git ignore rules
├──  pyrightconfig.json           # Python type checking config
└── 📁 .github/                     # GitHub configuration
    ├── 📁 workflows/               # CI/CD pipelines
    │   └── 📄 ci.yml              # Main CI/CD workflow
    ├── 📁 ISSUE_TEMPLATE/          # Issue templates
    │   ├── 📄 bug_report.md       # Bug report template
    │   └──  feature_request.md  # Feature request template
    └──  PULL_REQUEST_TEMPLATE.md # PR template
```

##  Backend Structure
```
backend/
├── 📄 app.py                      # Main FastAPI application
├── 📄 chat_handler.py             # AI chat processing
├── 📄 voice_handler.py            # Speech recognition & synthesis
├── 📄 ocr_handler.py              # Image/document text extraction
├── 📄 database_service.py         # Database operations
├──  supabase_client.py          # Supabase integration
├── 📄 insert_offers.py            # Data insertion utilities
├── 📄 requirements.txt            # Python dependencies
├── 📄 INTEGRATION_SUMMARY.md      # Integration documentation
├── 📁 __pycache__/                # Python cache
└── 📁 venv/                       # Virtual environment (gitignored)
```

##  Frontend Structure
```
frontend/
├── 📄 package.json                # Node.js dependencies
├── 📄 package-lock.json           # Locked dependencies
├── 📄 vite.config.ts              # Vite build configuration
├── 📄 tsconfig.json               # TypeScript configuration
├──  tsconfig.node.json          # Node TypeScript config
├──  tailwind.config.js          # Tailwind CSS configuration
├── 📄 postcss.config.js           # PostCSS configuration
├── 📄 index.html                  # Main HTML file
├── 📁 src/                        # Source code
│   ├── 📄 App.tsx                 # Main React component
│   ├── 📄 api.ts                  # API integration
│   ├── 📄 index.css               # Global styles
│   └── 📄 main.tsx                # React entry point
├── 📁 node_modules/               # Node.js dependencies (gitignored)
├── 📁 dist/                       # Build output (gitignored)
└── 📁 .vscode/                    # VS Code settings
```

## 📊 Data Structure
```
data/
├── 📄 kolhapur_jewelry_shops_comprehensive.csv  # Main business dataset
└── 📄 sample_jewelry_shops_structure.csv        # Sample data structure
```

##  Scripts Structure
```
scripts/
├── 📄 jewelry_scraper_comprehensive.py          # Data collection script
├── 📄 csv_viewer.py                             # Data visualization
├── 📄 justdial_scraper.py                       # Original scraper (blocked)
├── 📄 multi_approach_scraper.py                 # Multiple scraping approaches
├── 📄 data_enhancer.py                          # Data enhancement utilities
├── 📄 business_analyzer.py                      # Business data analysis
├──  offer_generator.py                        # Offer generation utilities
├── 📄 README_Jewelry_Scraper.md                 # Scraper documentation
└── 📄 __init__.py                               # Python package init
```

## 🐳 Docker Structure
```
frontend/
├── 📄 Dockerfile                  # Frontend container
└── 📄 nginx.conf                  # Nginx configuration
```

## 📚 Documentation Structure
```
docs/                              # Additional documentation (future)
├── 📄 architecture.md             # System architecture
├──  databas 
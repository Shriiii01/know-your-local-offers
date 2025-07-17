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
├──  database-schema.md         
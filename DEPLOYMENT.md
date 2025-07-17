# �� Deployment Guide

This guide covers deploying the Know Your Local Offers application to various platforms.

## 📋 Prerequisites

Before deployment, ensure you have:

- [ ] All environment variables configured
- [ ] Database setup completed
- [ ] API keys obtained
- [ ] Domain name (optional)

## 🔧 Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# ElevenLabs (Optional - for voice synthesis)
ELEVENLABS_API_KEY=your_elevenlabs_key

# Supabase Database
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# Twilio (for WhatsApp integration)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token

# Application Settings
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## �� Backend Deployment

### Option 1: Railway (Recommended)

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Project**
   ```bash
   cd backend
   railway init
   ```

4. **Configure Environment Variables**
   ```bash
   railway variables set OPENAI_API_KEY=your_key
   railway variables set SUPABASE_URL=your_url
   # Add all other variables
   ```

5. **Deploy**
   ```bash
   railway up
   ```

6. **Get Deployment URL**
   ```bash
   railway domain
   ```

### Option 2: Heroku

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set SUPABASE_URL=your_url
   # Add all other variables
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

### Option 3: DigitalOcean App Platform

1. **Create App in DigitalOcean Console**
2. **Connect GitHub Repository**
3. **Configure Build Settings**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. **Set Environment Variables**
5. **Deploy**

### Option 4: AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB Application**
   ```bash
   eb init
   ```

3. **Create Environment**
   ```bash
   eb create production
   ```

4. **Set Environment Variables**
   ```bash
   eb setenv OPENAI_API_KEY=your_key
   eb setenv SUPABASE_URL=your_url
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```

## 🎨 Frontend Deployment

### Option 1: Vercel (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   cd frontend
   vercel --prod
   ```

4. **Configure Environment Variables**
   - Go to Vercel Dashboard
   - Add `VITE_API_URL` with your backend URL

### Option 2: Netlify

1. **Build the Project**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Netlify**
   - Drag and drop `dist` folder to Netlify
   - Or connect GitHub repository

3. **Configure Environment Variables**
   - Go to Site Settings > Environment Variables
   - Add `VITE_API_URL`

### Option 3: GitHub Pages

1. **Update vite.config.ts**
   ```typescript
   export default defineConfig({
     base: '/know-your-local-offers/',
     // ... other config
   })
   ```

2. **Add GitHub Action**
   Create `.github/workflows/deploy.yml`:
   ```yaml
   name: Deploy to GitHub Pages
   on:
     push:
       branches: [ main ]
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - uses: actions/setup-node@v2
           with:
             node-version: '18'
         - run: npm ci
         - run: npm run build
         - uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./dist
   ```

## 🗄 Database Setup

### Supabase (Recommended)

1. **Create Supabase Project**
   - Go to https://supabase.com
   - Create new project

2. **Run Database Migrations**
   ```sql
   -- Create offers table
   CREATE TABLE offers (
     id SERIAL PRIMARY KEY,
     store_name VARCHAR(255) NOT NULL,
     city VARCHAR(100) NOT NULL,
     category VARCHAR(100) NOT NULL,
     offer_text TEXT NOT NULL,
     price_range VARCHAR(100),
     valid_till DATE,
     source VARCHAR(50) DEFAULT 'api',
     created_at TIMESTAMP DEFAULT NOW()
   );

   -- Create indexes
   CREATE INDEX idx_offers_city ON offers(city);
   CREATE INDEX idx_offers_category ON offers(category);
   ```

3. **Configure Row Level Security**
   ```sql
   ALTER TABLE offers ENABLE ROW LEVEL SECURITY;
   
   CREATE POLICY "Public read access" ON offers
     FOR SELECT USING (true);
   
   CREATE POLICY "Authenticated insert access" ON offers
     FOR INSERT WITH CHECK (auth.role() = 'authenticated');
   ```

### Alternative: PostgreSQL on Railway/Heroku

1. **Add PostgreSQL Add-on**
   ```bash
   # Railway
   railway add postgresql
   
   # Heroku
   heroku addons:create heroku-postgresql:mini
   ```

2. **Run Migrations**
   ```bash
   # Get database URL
   railway variables
   # or
   heroku config:get DATABASE_URL
   
   # Run migrations
   psql $DATABASE_URL -f migrations.sql
   ```

## 🔒 SSL/HTTPS Configuration

### Automatic (Recommended)
Most platforms provide automatic SSL:
- Railway: Automatic
- Heroku: Automatic
- Vercel: Automatic
- Netlify: Automatic

### Manual Configuration
If using custom domain:

1. **Obtain SSL Certificate**
   ```bash
   # Using Let's Encrypt
   certbot certonly --webroot -w /var/www/html -d yourdomain.com
   ```

2. **Configure Nginx**
   ```nginx
   server {
       listen 443 ssl;
       server_name yourdomain.com;
       
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## �� Monitoring and Logs

### Application Monitoring

1. **Health Check Endpoint**
   ```python
   @app.get("/health")
   def health_check():
       return {
           "status": "healthy",
           "timestamp": datetime.now().isoformat(),
           "version": "1.0.0"
       }
   ```

2. **Logging Configuration**
   ```python
   import logging
   
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   ```

### Platform-Specific Monitoring

**Railway**
```bash
# View logs
railway logs

# Monitor metrics
railway status
```

**Heroku**
```bash
# View logs
heroku logs --tail

# Monitor dynos
heroku ps
```

**Vercel**
- Go to Vercel Dashboard
- Check Function Logs
- Monitor Performance

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          python -m pytest

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Railway
        uses: bervProject/railway-deploy@v1.0.0
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: backend

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          working-directory: ./frontend
```

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors**
   ```python
   # Update CORS origins in backend
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Environment Variables Not Loading**
   ```bash
   # Check if variables are set
   railway variables
   # or
   heroku config
   ```

3. **Database Connection Issues**
   ```python
   # Test database connection
   import os
   from supabase import create_client
   
   url = os.getenv("SUPABASE_URL")
   key = os.getenv("SUPABASE_KEY")
   supabase = create_client(url, key)
   
   # Test query
   result = supabase.table('offers').select('*').limit(1).execute()
   print(result)
   ```

4. **Build Failures**
   ```bash
   # Check build logs
   railway logs
   # or
   vercel logs
   ```

### Performance Optimization

1. **Enable Caching**
   ```python
   from fastapi_cache import FastAPICache
   from fastapi_cache.backends.redis import RedisBackend
   
   FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
   ```

2. **Database Optimization**
   ```sql
   -- Add indexes for frequently queried columns
   CREATE INDEX idx_offers_city_category ON offers(city, category);
   CREATE INDEX idx_offers_created_at ON offers(created_at);
   ```

3. **Frontend Optimization**
   ```typescript
   // Enable code splitting
   const LazyComponent = lazy(() => import('./LazyComponent'));
   
   // Use React.memo for expensive components
   const ExpensiveComponent = React.memo(({ data }) => {
     // Component logic
   });
   ```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancers
- Implement database connection pooling
- Use CDN for static assets

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching strategies

### Cost Optimization
- Use serverless functions where possible
- Implement auto-scaling
- Monitor resource usage

## 🔐 Security Best Practices

1. **Environment Variables**
   - Never commit `.env` files
   - Use platform-specific secret management
   - Rotate API keys regularly

2. **API Security**
   ```python
   # Rate limiting
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
   ```

3. **Input Validation**
   ```python
   from pydantic import BaseModel, validator
   
   class OfferRequest(BaseModel):
       store_name: str
       city: str
       
       @validator('store_name')
       def validate_store_name(cls, v):
           if len(v) < 2:
               raise ValueError('Store name too short')
           return v
   ```

## 📞 Support

For deployment issues:
1. Check platform documentation
2. Review logs for error messages
3. Test locally first
4. Create issue with detailed error information

---

**Happy Deploying! 🚀** 
# JEWELRY STORES SCRAPER

Professional SerpAPI scraper for jewelry stores in Kolhapur with Supabase integration.

## SETUP

### 1. Get SerpAPI Key
1. Go to https://serpapi.com/
2. Sign up for free account (100 searches/month)
3. Get your API key from dashboard

### 2. Configure Environment
Add your SerpAPI key to `backend/.env`:
```
SERPAPI_KEY=your_actual_api_key_here
```

### 3. Install Dependencies
```bash
cd backend
pip install aiohttp pandas python-dotenv
```

### 4. Test Setup
```bash
cd scripts
python test_scraper.py
```

## USAGE

### 1. Run Scraper
```bash
cd scripts
python serpapi_scraper.py
```

This will:
- Search for jewelry stores in Kolhapur using 12 different queries
- Extract: title, address, phone, rating, category, website, hours
- Remove duplicates
- Save to `data/kolhapur_jewelry_stores.csv`

### 2. View Results
```bash
python csv_viewer.py
```

### 3. Upload to Supabase (Optional)
```bash
python upload_to_supabase.py
```

## FILES

- `serpapi_scraper.py` - Main scraper (maximum coverage)
- `csv_viewer.py` - View CSV results
- `upload_to_supabase.py` - Upload to database
- `test_scraper.py` - Test setup

## OUTPUT

CSV file with columns:
- title: Store name
- address: Full address
- phone: Phone number
- rating: Google rating
- category: "jewelry store"
- website: Store website
- hours: Business hours

## SEARCH QUERIES

The scraper uses these queries for maximum coverage:
1. "jewelry stores in Kolhapur"
2. "jewellery shops in Kolhapur"
3. "gold jewelry stores Kolhapur"
4. "diamond jewelry shops Kolhapur"
5. "wedding jewelry stores Kolhapur"
6. "bridal jewelry shops Kolhapur"
7. "jewelry showrooms Kolhapur"
8. "gold shops Kolhapur"
9. "ornament stores Kolhapur"
10. "precious jewelry Kolhapur"
11. "jewelry dealers Kolhapur"
12. "jewelry retailers Kolhapur"

## RATE LIMITING

- 3 second delay between queries
- Maximum 30 results per query
- Total API calls: ~12 (one per query)

## NEXT STEPS

1. Review CSV data quality
2. Update Supabase schema if needed
3. Upload data when ready
4. Connect to WhatsApp bot

## TROUBLESHOOTING

**No results found:**
- Check SERPAPI_KEY is correct
- Verify internet connection
- Try running test_scraper.py

**API errors:**
- Check remaining API credits
- Verify API key permissions

**CSV issues:**
- Check data directory exists
- Verify write permissions 
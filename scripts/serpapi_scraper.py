import os
import csv
import asyncio
import aiohttp
import json
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from root directory
load_dotenv('../.env')

class JewelryStoreScraper:
    """
    Fixed SerpAPI scraper for jewelry stores
    """
    
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")
        self.base_url = "https://serpapi.com/search"
        
        # Focused search queries
        self.queries = [
            "jewelry stores Kolhapur Maharashtra",
            "gold shops Kolhapur",
            "jewellery showrooms Kolhapur"
        ]
        
        # CSV columns
        self.csv_columns = ['title', 'address', 'phone', 'rating', 'category', 'website', 'hours']

    async def scrape_all_jewelry_stores(self) -> List[Dict]:
        """Main scraping function"""
        print("SCRAPING JEWELRY STORES IN KOLHAPUR")
        print("=" * 50)
        
        if not self.api_key:
            print("ERROR: SERPAPI_KEY not found in .env file")
            return []
        
        print(f"Using API key: {self.api_key[:10]}...")
        
        all_stores = []
        api_calls = 0
        
        for i, query in enumerate(self.queries, 1):
            print(f"\nQuery {i}/{len(self.queries)}: '{query}'")
            stores, calls = await self.search_query(query)
            all_stores.extend(stores)
            api_calls += calls
            print(f"Found: {len(stores)} stores")
            
            # Rate limiting
            if i < len(self.queries):
                await asyncio.sleep(2)
        
        # Remove duplicates
        unique_stores = self.deduplicate_stores(all_stores)
        
        print(f"\nRESULTS SUMMARY:")
        print(f"Total found: {len(all_stores)}")
        print(f"Unique stores: {len(unique_stores)}")
        print(f"API calls used: {api_calls}")
        
        return unique_stores

    async def search_query(self, query: str) -> tuple[List[Dict], int]:
        """Search using SerpAPI"""
        params = {
            "engine": "google",
            "q": query,
            "location": "Kolhapur, Maharashtra, India",
            "hl": "en",
            "gl": "in", 
            "api_key": self.api_key,
            "num": 20
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        stores = self.extract_all_stores(data)
                        return stores, 1
                    else:
                        print(f"API Error: {response.status}")
                        return [], 1
                        
        except Exception as e:
            print(f"Request error: {e}")
            return [], 0

    def extract_all_stores(self, data: Dict) -> List[Dict]:
        """Extract store data - FIXED VERSION"""
        stores = []
        
        try:
            # Process local results
            local_results = data.get("local_results", [])
            print(f"Processing {len(local_results)} local results...")
            
            for i, result in enumerate(local_results):
                print(f"Local result {i+1}: {type(result)}")
                
                # Ensure result is a dictionary
                if not isinstance(result, dict):
                    print(f"Skipping non-dict result: {result}")
                    continue
                
                title = result.get("title", "")
                print(f"Title: {title}")
                
                # Create store entry - accept ALL results for now
                store = {
                    'title': title.strip() if title else '',
                    'address': result.get('address', '').strip() if result.get('address') else '',
                    'phone': result.get('phone', '').strip() if result.get('phone') else '',
                    'rating': str(result.get('rating', '')).strip() if result.get('rating') else '',
                    'category': 'jewelry store',
                    'website': result.get('website', '').strip() if result.get('website') else '',
                    'hours': str(result.get('hours', '')).strip() if result.get('hours') else ''
                }
                
                if store['title']:  # Only add if has title
                    stores.append(store)
                    print(f"✅ Added: {store['title']}")
                else:
                    print(f"❌ Skipped: No title")
            
            # Process organic results
            organic_results = data.get("organic_results", [])
            print(f"Processing {len(organic_results)} organic results...")
            
            for i, result in enumerate(organic_results):
                if not isinstance(result, dict):
                    continue
                
                title = result.get("title", "")
                if title and self.is_jewelry_store(title):
                    store = {
                        'title': title.strip(),
                        'address': '',
                        'phone': '',
                        'rating': '',
                        'category': 'jewelry store',
                        'website': result.get('link', '').strip() if result.get('link') else '',
                        'hours': ''
                    }
                    stores.append(store)
                    print(f"✅ Added organic: {store['title']}")
            
            print(f"Total extracted: {len(stores)} stores")
            return stores
            
        except Exception as e:
            print(f"Error in extract_all_stores: {e}")
            import traceback
            traceback.print_exc()
            return []

    def is_jewelry_store(self, text: str) -> bool:
        """Check if text indicates a jewelry store"""
        if not text:
            return False
            
        text_lower = text.lower()
        jewelry_keywords = [
            'jewelry', 'jewellery', 'jeweler', 'jeweller',
            'gold', 'diamond', 'silver', 'platinum',
            'ornament', 'ornaments', 'precious', 'gem',
            'ring', 'necklace', 'bracelet', 'earring'
        ]
        
        return any(keyword in text_lower for keyword in jewelry_keywords)

    def deduplicate_stores(self, stores: List[Dict]) -> List[Dict]:
        """Remove duplicates"""
        seen = set()
        unique = []
        
        for store in stores:
            title = store['title'].lower().strip()
            if title and title not in seen:
                seen.add(title)
                unique.append(store)
        
        return unique

    def save_to_csv(self, stores: List[Dict]) -> bool:
        """Save to CSV"""
        if not stores:
            print("No stores to save")
            return False
        
        # Ensure data directory exists
        os.makedirs('../data', exist_ok=True)
        filename = '../data/kolhapur_jewelry_stores.csv'
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
                writer.writeheader()
                writer.writerows(stores)
            
            print(f"\n✅ SUCCESS: Saved {len(stores)} stores to {filename}")
            return True
            
        except Exception as e:
            print(f"Error saving CSV: {e}")
            return False

    def show_stores(self, stores: List[Dict]):
        """Show all stores found"""
        print(f"\n📋 ALL STORES FOUND:")
        print("-" * 50)
        for i, store in enumerate(stores, 1):
            print(f"{i}. {store['title']}")
            if store['address']:
                print(f"   📍 {store['address']}")
            if store['phone']:
                print(f"   📞 {store['phone']}")
            if store['rating']:
                print(f"   ⭐ {store['rating']}")
            if store['website']:
                print(f"   🌐 {store['website']}")
            print()

async def main():
    """Run the scraper"""
    scraper = JewelryStoreScraper()
    
    # Scrape stores
    stores = await scraper.scrape_all_jewelry_stores()
    
    if stores:
        # Show all stores
        scraper.show_stores(stores)
        
        # Save to CSV
        success = scraper.save_to_csv(stores)
        
        if success:
            print(f"🎉 SCRAPING COMPLETED!")
            print(f"📊 Total stores: {len(stores)}")
            print(f"📁 File: data/kolhapur_jewelry_stores.csv")
    else:
        print("❌ No stores found")

if __name__ == "__main__":
    asyncio.run(main()) 
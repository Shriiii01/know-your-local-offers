import pandas as pd
import os
import sys
from dotenv import load_dotenv
import asyncio

# Add backend to path to import database service
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, backend_path)

try:
    from database_service import DatabaseService
except ImportError as e:
    print(f"ERROR: Cannot import database_service: {e}")
    print(f"Make sure you're running from the scripts directory")
    print(f"Backend path: {backend_path}")
    sys.exit(1)

# Load environment variables from root directory
load_dotenv('../.env')

class SupabaseUploader:
    """
    Upload CSV data to Supabase - clean professional output
    """
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.csv_file = '../data/kolhapur_jewelry_stores.csv'

    async def upload_jewelry_stores(self):
        """Upload jewelry stores from CSV to Supabase"""
        print("UPLOADING JEWELRY STORES TO SUPABASE")
        print("=" * 45)
        
        # Check if CSV exists
        if not os.path.exists(self.csv_file):
            print("ERROR: CSV file not found")
            print("Run scraper first: python serpapi_scraper.py")
            return
        
        try:
            # Read CSV
            df = pd.read_csv(self.csv_file)
            print(f"Found {len(df)} stores in CSV")
            
            # Convert to database format
            stores_data = []
            for _, row in df.iterrows():
                store_data = {
                    "store_name": row['title'],
                    "city": "Kolhapur",
                    "category": "jewellery",
                    "offer_text": f"Visit {row['title']} for quality jewelry and competitive prices",
                    "price_range": "Contact for pricing",
                    "valid_till": "2025-12-31",
                    "source": "serpapi_scraping"
                }
                stores_data.append(store_data)
            
            # Upload to Supabase
            success_count = 0
            failed_count = 0
            
            for store in stores_data:
                try:
                    success = await self.db_service.add_offer(store)
                    if success:
                        success_count += 1
                        print(f"UPLOADED: {store['store_name']}")
                    else:
                        failed_count += 1
                        print(f"FAILED: {store['store_name']}")
                except Exception as e:
                    failed_count += 1
                    print(f"ERROR uploading {store['store_name']}: {e}")
            
            print(f"\nUPLOAD SUMMARY:")
            print(f"Successfully uploaded: {success_count}")
            print(f"Failed: {failed_count}")
            print(f"Total: {len(stores_data)}")
            
        except Exception as e:
            print(f"ERROR: {e}")

    def show_schema_requirements(self):
        """Show what columns need to be added to Supabase"""
        print("SUPABASE SCHEMA REQUIREMENTS")
        print("=" * 35)
        
        print("Current 'offers' table should have these columns:")
        print("- store_name (TEXT)")
        print("- city (TEXT)")
        print("- category (TEXT)")
        print("- offer_text (TEXT)")
        print("- price_range (TEXT)")
        print("- valid_till (TEXT)")
        print("- source (TEXT)")
        
        print("\nOptional: Add these columns for CSV data:")
        print("- address (TEXT)")
        print("- phone (TEXT)")
        print("- rating (TEXT)")
        print("- website (TEXT)")
        print("- hours (TEXT)")
        
        print("\nSQL to add optional columns:")
        print("ALTER TABLE offers ADD COLUMN address TEXT;")
        print("ALTER TABLE offers ADD COLUMN phone TEXT;")
        print("ALTER TABLE offers ADD COLUMN rating TEXT;")
        print("ALTER TABLE offers ADD COLUMN website TEXT;")
        print("ALTER TABLE offers ADD COLUMN hours TEXT;")

async def main():
    """Main upload function"""
    uploader = SupabaseUploader()
    
    print("Choose an option:")
    print("1. Show schema requirements")
    print("2. Upload data to Supabase")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        uploader.show_schema_requirements()
    elif choice == "2":
        await uploader.upload_jewelry_stores()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())